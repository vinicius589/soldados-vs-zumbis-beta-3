"""Soldados vs Zumbis — Beta 4.

Um tower defense original em Pygame. A Beta 4 preserva campanha, cartas,
munição com recarga própria, chefes, Núcleos de Ascensão e elencos temáticos por
região, mas introduz um sistema próprio de animação orientado por estados.
Nenhum código ou arte externa é incorporado: cada estado é atualizado por
tempo real e renderizado a partir dos recursos originais do projeto.
"""

from __future__ import annotations

import json
import math
import os
import random
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import pygame

from opengl_presenter import ActorCommand, OpenGLPresenter


ROOT = Path(__file__).resolve().parent
ASSET_DIR = ROOT / "assets" / "v7"
SAVE_PATH = ROOT / "campanha_v7.json"
WIDTH, HEIGHT = 1280, 720
FPS = 60
VERSION = "BETA 4"
CARD_RECHARGE_SECONDS = 10.0
ROWS, COLS = 4, 9
# Limite horizontal comum e extensão vertical total das três arenas. As
# faixas não usam uma grade vertical genérica: cada cenário possui limites
# calibrados a partir das pistas realmente pintadas na arte.
BOARD = pygame.Rect(164, 170, 1090, 540)
CELL_W = BOARD.width / COLS
CELL_H = BOARD.height / ROWS
LANE_BOUNDS: dict[str, tuple[int, int, int, int, int]] = {
    # As três pinturas e a lógica usam quatro faixas largas e idênticas.
    # Isso dá respiro a corpos inteiros e evita diferenças artificiais de
    # escala entre a primeira e a última linha.
    "city": (170, 305, 440, 575, 710),
    "desert": (170, 305, 440, 575, 710),
    "beach": (170, 305, 440, 575, 710),
}
BEACH_WATER_ROWS = frozenset({1, 2})
LANE_BOMB_HOME_X = BOARD.left + 42
WHITE = (242, 244, 239)
INK = (15, 20, 25)
GOLD = (240, 187, 72)
RED = (218, 68, 57)
TEAL = (72, 198, 192)
GRAY = (148, 160, 166)


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


@dataclass
class ActorMotion:
    """Estado visual temporizado de uma unidade em campo.

    A referência técnica analisada separava os sprites em sequências de
    caminhada e ataque. Aqui o mesmo princípio é refeito sem depender de uma
    contagem fixa de arquivos ou de um frame mágico: a simulação informa um
    estado, o estado avança com ``dt`` e o desenho calcula a pose correspondente.
    Isso mantém combate e animação sincronizados inclusive quando a taxa de
    quadros varia.
    """

    state: str = "spawn"
    state_elapsed: float = 0.0
    event_left: float = 0.28
    hit_flash: float = 0.0

    def advance(self, dt: float, fallback: str) -> None:
        self.state_elapsed += dt
        self.hit_flash = max(0.0, self.hit_flash - dt)
        if self.event_left > 0:
            self.event_left = max(0.0, self.event_left - dt)
            if self.event_left > 0:
                return
        if self.state != fallback:
            self.state = fallback
            self.state_elapsed = 0.0

    def trigger(self, state: str, duration: float) -> None:
        """Inicia uma ação curta (tiro, golpe, habilidade ou impacto)."""
        if self.state != state:
            self.state = state
            self.state_elapsed = 0.0
            # Uma ação nova não deve herdar o tempo que restava de outra
            # pose (por exemplo, o nascer da unidade não pode alongar um
            # disparo que acabou de acontecer).
            self.event_left = max(0.0, duration)
            return
        self.event_left = max(self.event_left, max(0.0, duration))

    def loop(self, state: str) -> None:
        """Troca para um estado contínuo que deve prevalecer neste quadro."""
        if self.state != state:
            self.state = state
            self.state_elapsed = 0.0
        self.event_left = 0.0

    def flash(self, seconds: float = 0.13) -> None:
        self.hit_flash = max(self.hit_flash, seconds)

    def phase(self, fps: float = 8.0, frames: int = 4) -> int:
        """Índice estável de um ciclo visual, independente do FPS real."""
        return int(self.state_elapsed * fps) % max(1, frames)


@dataclass
class VisualEffect:
    """Efeito curto de impacto/atividade, separado da lógica do projétil."""

    kind: str
    x: float
    y: float
    color: tuple[int, int, int]
    duration: float = 0.34
    elapsed: float = 0.0
    scale: float = 1.0


@dataclass
class DefeatAnimation:
    """Mantém a silhueta por alguns quadros depois da morte lógica."""

    sprite: pygame.Surface
    x: float
    y: float
    width: float
    height: float
    water: bool = False
    duration: float = 0.48
    elapsed: float = 0.0
    enemy: bool = False


def enemy_wave_scale(wave: int) -> float:
    """Mantém as primeiras ondas acolhedoras e endurece a reta final.

    A versão anterior começava com vida cheia e liberava ameaças depressa;
    assim, o primeiro contato parecia mais duro que a metade da campanha.
    """
    return 0.72 + max(0, wave - 1) * 0.10


def enemy_damage_scale(wave: int) -> float:
    """Escala separada para que o fim não seja só uma esponja de vida."""
    return 0.78 + wave * 0.07


def boss_wave_scale(wave: int) -> float:
    """Chefes escalam com a campanha sem virar paredes de vida.

    Um chefe deve mudar a montagem da linha, não exigir uma composição
    perfeita ou prender o jogador numa sequência infinita de atordoamentos.
    Por isso sua vida cresce mais devagar que a de uma horda comum.
    """
    # Chefes mantêm sua identidade, mas precisam cair com uma montagem boa
    # antes que a contenção de última linha vire o único plano viável.
    return 0.78 + max(0, wave - 1) * 0.030


def boss_damage_scale(wave: int) -> float:
    """Contém o dano físico dos chefes nas ondas altas."""
    return 0.62 + wave * 0.025


def lane_bounds(region: str, row: int) -> tuple[float, float]:
    """Limites reais da faixa desenhada no cenário selecionado."""
    bounds = LANE_BOUNDS.get(region, LANE_BOUNDS["city"])
    index = int(clamp(row, 0, ROWS - 1))
    return float(bounds[index]), float(bounds[index + 1])


def terrain_y(region: str, row: int, x: float) -> float:
    """Retorna a linha de contato dos pés, rodas ou casco com o terreno.

    ``x`` permanece na assinatura porque inimigos móveis consultam esta
    função a cada quadro. As rotas desta versão são horizontais: assim um
    zumbi nunca deriva verticalmente nem abandona a linha em que nasceu.
    """
    top, bottom = lane_bounds(region, row)
    return (top + bottom) / 2.0


def lane_depth(region: str, row: int) -> float:
    """Escala de perspectiva: faixas distantes menores, frente maior."""
    first = terrain_y(region, 0, BOARD.left)
    last = terrain_y(region, ROWS - 1, BOARD.left)
    position = terrain_y(region, row, BOARD.left)
    progress = 0.0 if last == first else (position - first) / (last - first)
    # O novo litoral foi pintado com projeção quase ortográfica; nele uma
    # variação extrema fazia a primeira faixa parecer miniatura e a última,
    # gigante. Cidade e Deserto preservam a perspectiva mais profunda.
    # A primeira faixa fica logo abaixo da aba superior: 0,58 também garante
    # que cabeça/arma não sejam cortadas pelo HUD. Na frente, 0,96 evita o
    # efeito de gigante observado no cenário costeiro anterior.
    rear, front = (0.86, 0.98) if region == "beach" else (0.84, 1.0)
    return lerp(rear, front, clamp(progress, 0.0, 1.0))


def cell_center(row: int, col: int, region: str = "city") -> tuple[float, float]:
    x = BOARD.left + (col + 0.5) * CELL_W
    return x, terrain_y(region, row, x)


def cell_rect(row: int, col: int, region: str = "city") -> pygame.Rect:
    top, bottom = lane_bounds(region, row)
    return pygame.Rect(
        int(BOARD.left + col * CELL_W),
        int(top),
        int(CELL_W),
        int(bottom - top),
    )


def title_case(value: str) -> str:
    return value.replace("_", " ").title()


REGIONS = {
    "city": {
        "name": "Cidade Quarentenada",
        "short": "CIDADE",
        "tag": "Tóxico urbano",
        "bg": "city_beta4_four_lanes.png",
        "soldiers": "city_soldiers_atlas.png",
        "soldiers_l2": "city_soldiers_l2_atlas_v74.png",
        "zombies": "city_zombies_atlas.png",
        "accent": (90, 207, 166),
        "unlock_after": None,
        "description": "Uma avenida de quarentena com quatro pistas largas de asfalto, base de emergência e ruínas tóxicas nas bordas.",
        "bosses": ("bruto_demolidor", "comandante_mortos", "cuspidor_alfa"),
    },
    "desert": {
        "name": "Deserto das Ruínas",
        "short": "DESERTO",
        "tag": "Magia e escavação",
        "bg": "desert_beta4_four_lanes.png",
        "soldiers": "desert_soldiers_atlas.png",
        "soldiers_l2": "desert_soldiers_l2_atlas_v74.png",
        "zombies": "desert_zombies_atlas.png",
        "accent": (235, 179, 76),
        "unlock_after": "city",
        "description": "Quatro trilhas largas de areia compactada cruzam uma expedição militar rumo às ruínas e pirâmides antigas.",
        "bosses": ("mutante_ruinas", "necromante", "colosso_mutante"),
    },
    "beach": {
        "name": "Praia de Maré Morta",
        "short": "PRAIA",
        "tag": "Maré e costa",
        "bg": "beach_beta4_four_lanes.png",
        "soldiers": "beach_soldiers_beta4_rebuilt.png",
        "soldiers_l2": "beach_soldiers_l2_beta4_rebuilt.png",
        "zombies": "beach_zombies_beta4_rebuilt.png",
        "accent": (78, 177, 232),
        "unlock_after": "desert",
        "description": "Uma faixa de areia, duas rotas de água e uma faixa de areia formam a defesa costeira em quatro linhas.",
        "bosses": ("tide_brute", "cacador_abissal", "leviata"),
    },
}


# Cada carta possui Nível 1 ou Nível 2. O terceiro nível é temporário e só
# existe quando um Núcleo de Ascensão, recebido ao derrotar um chefe, é usado.
DEFENSES = {
    "recruta": {
        "base": "Recruta",
        "role": "rifle",
        "level": 1,
        "cost": 45,
        "hp": 92,
        "damage": 11,
        "range": 2,
        "cooldown": 1.05,
        "ammo": 10,
        "sprite": 0,
        "ability": "Pistola: tiro cadenciado em até 2 blocos. Dez tiros derrubam um Caminhante.",
    },
    "soldado": {
        "base": "Soldado",
        "role": "rifle",
        "level": 2,
        "cost": 95,
        "hp": 128,
        "damage": 20,
        "range": 4,
        "cooldown": 0.60,
        "ammo": 18,
        "sprite": 1,
        "ability": "M16: quatro blocos de alcance e fogo sustentado. Ao esvaziar, executa uma recarga própria temporizada.",
    },
    "escopeteiro": {
        "base": "Espingarda de Mão",
        "role": "shotgun",
        "level": 1,
        "cost": 55,
        "hp": 122,
        "damage": 38,
        "range": 1,
        "cooldown": 1.10,
        "ammo": 2,
        "sprite": 3,
        "ability": "Dois cartuchos e alcance curto. Quanto mais perto, mais pellets acertam.",
    },
    "escopeteiro_regular": {
        "base": "Escopeteiro Regular",
        "role": "shotgun",
        "level": 2,
        "cost": 105,
        "hp": 150,
        "damage": 52,
        "range": 3,
        "cooldown": 0.95,
        "ammo": 5,
        "sprite": 3,
        "ability": "Espingarda regular de três blocos; segura os corredores antes da linha.",
    },
    "sniper": {
        "base": "Atirador de Vigia",
        "role": "sniper",
        "level": 1,
        "cost": 75,
        "hp": 82,
        "damage": 58,
        "range": 9,
        "cooldown": 2.10,
        "ammo": 5,
        "sprite": 4,
        "ability": "Mira instável: pode errar. Dano alto, sem execução instantânea.",
    },
    "sniper_regular": {
        "base": "Sniper Regular",
        "role": "sniper",
        "level": 2,
        "cost": 135,
        "hp": 95,
        "damage": 88,
        "range": 9,
        "cooldown": 1.85,
        "ammo": 6,
        "sprite": 4,
        "ability": "Mira garantida e dano alto; ainda não é um hit-kill.",
    },
    "bombardeiro": {
        "base": "Bombardeiro",
        "role": "grenade",
        "level": 1,
        "cost": 100,
        "hp": 112,
        "damage": 70,
        "range": 2,
        "cooldown": 2.25,
        "ammo": 3,
        "sprite": 5,
        "ability": "Granada curta em área. A explosão pode ferir aliados próximos.",
    },
    "granadeiro": {
        "base": "Granadeiro",
        "role": "grenade",
        "level": 2,
        "cost": 150,
        "hp": 124,
        "damage": 88,
        "range": 4,
        "cooldown": 1.75,
        "ammo": 5,
        "sprite": 5,
        "ability": "Lançador de granadas de quatro blocos; controla grupos, mas gasta muita munição.",
    },
    "morteiro": {
        "base": "Morteiro de Campo",
        "role": "mortar",
        "level": 2,
        "cost": 165,
        "hp": 105,
        "damage": 105,
        "range": 3,
        "cooldown": 2.30,
        "ammo": 4,
        "sprite": 5,
        "ability": "Bomba de arco com área ampla. Não mira o primeiro bloco da própria posição.",
    },
    "lanca_chamas": {
        "base": "Lança-Chamas",
        "role": "flame",
        "level": 2,
        "cost": 128,
        "hp": 144,
        "damage": 20,
        "range": 3,
        "cooldown": 0.35,
        "ammo": 14,
        "sprite": 9,
        "ability": "Exclusivo do Deserto. Cone de fogo reforçado até três blocos; aplica Queimadura contínua.",
    },
    "lanca_chamas_bolso": {
        "base": "Lança-Chamas de Mão",
        "role": "flame",
        "level": 1,
        "cost": 78,
        "hp": 108,
        "damage": 14,
        "range": 1,
        "cooldown": 0.62,
        "ammo": 8,
        "sprite": 9,
        "ability": "Exclusivo do Deserto. Jato de fogo curto de um bloco; causa dano maior e aplica Queimadura.",
    },
    "lancador_veneno": {
        "base": "Lançador de Veneno",
        "role": "poison",
        "level": 1,
        "cost": 82,
        "hp": 110,
        "damage": 12,
        "range": 1,
        "cooldown": 0.62,
        "ammo": 8,
        "sprite": 9,
        "ability": "Exclusivo da Cidade. Pulveriza veneno a um bloco e aplica Envenenado: dano contínuo e avanço 12% menor.",
    },
    "canhao_veneno": {
        "base": "Canhão de Veneno",
        "role": "poison",
        "level": 2,
        "cost": 132,
        "hp": 146,
        "damage": 18,
        "range": 3,
        "cooldown": 0.35,
        "ammo": 14,
        "sprite": 9,
        "ability": "Exclusivo da Cidade. Nuvem tóxica em área até três blocos; mantém grupos Envenenados e mais lentos.",
    },
    "lancador_agua": {
        "base": "Lançador de Água",
        "role": "waterjet",
        "level": 1,
        "cost": 78,
        "hp": 108,
        "damage": 9,
        "range": 1,
        "cooldown": 0.62,
        "ammo": 8,
        "sprite": 9,
        "ability": "Jato de água curto e pressurizado. Encharca o alvo, apaga queima e reduz o avanço por alguns segundos.",
    },
    "canhao_mare": {
        "base": "Canhão de Maré",
        "role": "waterjet",
        "level": 2,
        "cost": 128,
        "hp": 144,
        "damage": 12,
        "range": 3,
        "cooldown": 0.35,
        "ammo": 14,
        "sprite": 9,
        "ability": "Canhão de água de três blocos. Pulveriza pequenos grupos, apaga fogo e reduz a velocidade dos encharcados.",
    },
    "morteiro_basico": {
        "base": "Morteiro de Uma Bomba",
        "role": "mortar",
        "level": 1,
        "cost": 82,
        "hp": 88,
        "damage": 66,
        "range": 2,
        "cooldown": 4.35,
        "ammo": 1,
        "sprite": 5,
        "ability": "Lança uma única bomba em área e recarrega muito devagar. É o estágio inicial do morteiro.",
    },
    "radio": {
        "base": "Operador de Rádio",
        "role": "radio",
        "level": 1,
        "cost": 72,
        "hp": 90,
        "damage": 0,
        "range": 0,
        "cooldown": 7.00,
        "ammo": 0,
        "sprite": 7,
        "ability": "Pede suprimento à base: pouca quantidade e entrega lenta. É barato de manter.",
    },
    "torre_radio": {
        "base": "Torre de Rádio",
        "role": "radio",
        "level": 2,
        "cost": 128,
        "hp": 118,
        "damage": 0,
        "range": 0,
        "cooldown": 4.80,
        "ammo": 0,
        "sprite": 7,
        "ability": "Sinal reforçado: suprimento e ritmo médios, sem travar a economia no início.",
    },
    "barreira": {
        "base": "Barreira de Contenção",
        "role": "barrier",
        "level": 1,
        "cost": 58,
        "hp": 360,
        "damage": 0,
        "range": 0,
        "cooldown": 0,
        "ammo": 0,
        "sprite": 10,
        "ability": "Veículo estático com muita vida para atrasar a horda. Não possui armas.",
    },
    "barreira_reativa": {
        "base": "Barreira Reativa",
        "role": "barrier",
        "level": 2,
        "cost": 104,
        "hp": 470,
        "damage": 70,
        "range": 0,
        "cooldown": 0,
        "ammo": 0,
        "sprite": 10,
        "ability": "Ao ser destruída, explode e atinge inimigos adjacentes. Continua sem arma.",
    },
    "mina": {
        "base": "Mina de Pressão",
        "role": "mine",
        "level": 1,
        "cost": 42,
        "hp": 1,
        "damage": 105,
        "range": 0,
        "cooldown": 0,
        "ammo": 0,
        "sprite": 11,
        "ability": "Elimina um alvo, mas possui chance de falha. Um Núcleo transforma-a em limpeza de linha.",
    },
    "mina_segura": {
        "base": "Mina Segura",
        "role": "mine",
        "level": 2,
        "cost": 74,
        "hp": 1,
        "damage": 150,
        "range": 0,
        "cooldown": 0,
        "ammo": 0,
        "sprite": 11,
        "ability": "Disparo garantido contra um único invasor. Reage quando ele pisa na célula.",
    },
    "lancha": {
        "base": "Lancha Patrulha",
        "role": "boat",
        "level": 2,
        "cost": 125,
        "hp": 275,
        "damage": 38,
        "range": 4,
        "cooldown": 0.70,
        "ammo": 16,
        "sprite": 5,
        "water_only": True,
        "ability": "Carta marítima exclusiva da Praia; só pode ser posicionada nas faixas de água do canal.",
    },
    "atirador_lancha": {
        "base": "Atirador de Lancha",
        "role": "boat",
        "level": 1,
        "cost": 78,
        "hp": 158,
        "damage": 22,
        "range": 3,
        "cooldown": 0.86,
        "ammo": 10,
        "sprite": 5,
        "water_only": True,
        "ability": "Barquinho leve com rifle: cobre até três blocos do canal. Tem dez disparos e evolui para a Lancha Patrulha.",
    },
    "submarino": {
        "base": "Submarino",
        "role": "sub",
        "level": 2,
        "cost": 175,
        "hp": 235,
        "damage": 90,
        "range": 6,
        "cooldown": 1.80,
        "ammo": 6,
        "sprite": 6,
        "water_only": True,
        "ability": "Torpedos de grande alcance. Carta marítima exclusiva da Praia: fica indisponível em solo seco.",
    },
    "bomba_agua": {
        "base": "Bomba de Água",
        "role": "mine",
        "level": 2,
        "cost": 80,
        "hp": 1,
        "damage": 190,
        "range": 0,
        "cooldown": 0,
        "ammo": 0,
        "sprite": 11,
        "water_only": True,
        "ability": "Mina marítima segura: só pode ficar submersa e explode em pequenos grupos.",
    },
    "instrutor": {
        "base": "Sargento de Promoção",
        "role": "promoter",
        "level": 2,
        "cost": 135,
        "hp": 120,
        "damage": 0,
        "range": 3,
        "cooldown": 90.0,
        "ammo": 0,
        "sprite": 2,
        "ability": "Depois de 90 s no campo, promove uma defesa N1 próxima para sua versão N2. Promove uma por ciclo e não cria N3.",
    },
}


# Tempo de troca de carregador/cano por família de arma. A recarga automática
# só começa depois da última pose de disparo e deixa a unidade sem atacar. O
# intervalo intencional de 8 a 15 segundos substitui por completo a antiga
# dependência de Mecânico/Engenheiro de munição.
WEAPON_RELOAD_SECONDS: dict[str, tuple[float, float]] = {
    "rifle": (9.0, 8.0),
    "shotgun": (11.5, 9.5),
    "sniper": (13.0, 11.0),
    "grenade": (13.5, 11.5),
    "mortar": (15.0, 13.0),
    "flame": (10.5, 9.0),
    "poison": (10.5, 9.0),
    "waterjet": (10.0, 8.5),
    "boat": (10.5, 9.0),
    "sub": (14.5, 13.0),
}


def weapon_reload_seconds(stats: dict, ascended: bool = False) -> float:
    """Retorna a recarga visível da arma sem sair da faixa de 8–15 s."""
    role = str(stats.get("role", ""))
    level = 2 if int(stats.get("level", 1)) >= 2 else 1
    pair = WEAPON_RELOAD_SECONDS.get(role)
    if pair is None or int(stats.get("ammo", 0)) <= 0:
        return 0.0
    seconds = pair[level - 1]
    if ascended:
        seconds = max(8.0, seconds * 0.82)
    return float(clamp(seconds, 8.0, 15.0))


# Promoção permanente de campo. As cartas N1 e N2 continuam livres na seleção;
# o Sargento só economiza uma segunda colocação quando sobrevive ao ciclo inteiro.
PROMOTIONS = {
    "recruta": "soldado",
    "escopeteiro": "escopeteiro_regular",
    "sniper": "sniper_regular",
    "bombardeiro": "granadeiro",
    "morteiro_basico": "morteiro",
    "lanca_chamas_bolso": "lanca_chamas",
    "lancador_veneno": "canhao_veneno",
    "lancador_agua": "canhao_mare",
    "radio": "torre_radio",
    "barreira": "barreira_reativa",
    "mina": "mina_segura",
    "atirador_lancha": "lancha",
}


# A dificuldade não é um simples multiplicador escondido: ela decide quais
# cartas aparecem na montagem e regula, de maneira legível, a resistência,
# o dano e o ritmo da horda. O modo Difícil recebe um pouco mais de recurso
# inicial para continuar severo sem virar uma campanha impossível por falta
# de primeira defesa.
DIFFICULTIES = {
    "easy": {
        "label": "FÁCIL",
        "levels": (2,),
        "initial_supplies": 390,
        "initial_cores": 3,
        # Perfil definido pelo jogador: o arsenal N2, os três Núcleos e 390
        # suprimentos sustentam esta pressão sem retirar o caráter acessível.
        "enemy_hp": 1.20,
        "enemy_damage": 1.20,
        "boss_hp": 1.15,
        "boss_damage": 1.15,
        "spawn_count": 1.15,
        "spawn_wait": 0.90,
        "escort_count": 1.20,
        "skill_cooldown": 0.85,
        "accent": (112, 212, 139),
        "summary": "Cartas N2, 390 SUP e 3 Núcleos para uma campanha acessível.",
    },
    "medium": {
        "label": "MÉDIO",
        "levels": (1, 2),
        # Perfil definido pelo jogador: uma faixa central exigente, com N1/N2
        # e menos recurso para que posicionamento, recarga e counters importem.
        "initial_supplies": 128,
        "initial_cores": 0,
        # Pequeno degrau pedido para a Beta 4: aumenta a pressão em somente
        # dois pontos e encurta discretamente as entradas. O começo continua
        # legível; a diferença fica mais clara quando o elenco especial abre.
        "enemy_hp": 1.36,
        "enemy_damage": 1.36,
        "boss_hp": 1.24,
        "boss_damage": 1.24,
        "spawn_count": 1.24,
        "spawn_wait": 0.77,
        "escort_count": 1.36,
        "skill_cooldown": 0.86,
        "accent": GOLD,
        "summary": "Cartas N1/N2, pouco recurso e pressão constante de campanha.",
    },
    "hard": {
        "label": "DIFÍCIL",
        "levels": (1,),
        "initial_supplies": 105,
        "initial_cores": 0,
        # Degrau final: +4 pontos percentuais em todas as pressões do modo
        # veterano, ainda sem stuns infinitos ou vida de chefe sem teto.
        "enemy_hp": 1.66,
        "enemy_damage": 1.58,
        "boss_hp": 1.62,
        "boss_damage": 1.50,
        "spawn_count": 1.39,
        "spawn_wait": 0.68,
        "escort_count": 1.54,
        "skill_cooldown": 0.84,
        "accent": RED,
        "summary": "Apenas N1; economia curta, hordas densas e chefes realmente veteranos.",
    },
}


def difficulty_profile(key: str) -> dict:
    """Retorna sempre um modo válido, inclusive em salvamentos antigos."""
    return DIFFICULTIES.get(key, DIFFICULTIES["medium"])


REGION_ROSTERS = {
    "city": (
        ("recruta", "Patrulheiro Urbano"),
        ("soldado", "Fuzileiro de Asfalto"),
        ("escopeteiro_regular", "Escopeteiro de Brecha"),
        ("sniper_regular", "Vigia de Telhado"),
        ("bombardeiro", "Granadeiro de Quarentena"),
        ("radio", "Operador de Rádio"),
        ("canhao_veneno", "Canhão Tóxico Hazmat"),
        ("barreira_reativa", "Vanguarda Reativa"),
        ("mina_segura", "Mina de Sarjeta"),
        ("escopeteiro", "Espingarda de Mão"),
        ("sniper", "Vigia Recruta"),
        ("lancador_veneno", "Pulverizador de Veneno"),
        ("morteiro_basico", "Morteiro de Uma Bomba"),
        ("granadeiro", "Lançador de Quarentena"),
        ("barreira", "Barreira de Rua"),
        ("mina", "Mina Instável"),
        ("instrutor", "Sargento de Promoção Urbano"),
    ),
    "desert": (
        ("recruta", "Batedor do Oásis"),
        ("soldado", "Rifleiro das Dunas"),
        ("escopeteiro_regular", "Escopeteiro de Caravana"),
        ("sniper_regular", "Atirador das Dunas"),
        ("morteiro", "Morteiro de Ruínas"),
        ("granadeiro", "Granadeiro de Escavação"),
        ("torre_radio", "Torre de Rádio Solar"),
        ("lanca_chamas", "Lança-Chamas do Oásis"),
        ("barreira_reativa", "Caminhão de Contenção"),
        ("mina_segura", "Mina Solar"),
        ("escopeteiro", "Espingarda de Caravana"),
        ("sniper", "Vigia das Dunas"),
        ("bombardeiro", "Bombardeiro do Oásis"),
        ("morteiro_basico", "Morteiro de Uma Bomba"),
        ("radio", "Operador de Rádio de Campo"),
        ("barreira", "Barreira de Caravana"),
        ("instrutor", "Sargento de Promoção das Dunas"),
    ),
    "beach": (
        ("recruta", "Guarda-Costa Recruta"),
        ("soldado", "Fuzileiro Anfíbio"),
        ("escopeteiro_regular", "Escopeteiro de Resgate"),
        ("sniper_regular", "Sniper Costeiro"),
        ("bombardeiro", "Arpoador Explosivo"),
        ("morteiro_basico", "Morteiro de Salva Costeiro"),
        ("torre_radio", "Torre de Sinal Marítimo"),
        ("canhao_mare", "Canhão de Maré Costeiro"),
        ("barreira_reativa", "Boia de Contenção"),
        ("bomba_agua", "Bomba de Água"),
        ("atirador_lancha", "Atirador de Lancha"),
        ("lancha", "Lancha Patrulha"),
        ("submarino", "Submarino Costeiro"),
        ("escopeteiro", "Espingarda de Resgate"),
        ("sniper", "Vigia Costeiro"),
        ("granadeiro", "Granadeiro de Arpão"),
        ("radio", "Operador de Rádio Costeiro"),
        ("barreira", "Boia de Contenção Básica"),
        ("mina", "Mina de Areia"),
        ("instrutor", "Sargento de Promoção da Guarda-Costa"),
    ),
}


# Índices de atlas por carta, região e nível. Eles não podem ser inferidos
# apenas pelo "papel" da unidade: as três folhas de arte têm ordens próprias
# e uma célula N1 não representa automaticamente sua evolução N2. Esta é a
# única fonte usada pela seleção, pelo HUD, pelo dossiê e pela tropa em campo.
CARD_ATLAS_INDEX = {
    "city": {
        "recruta": 0, "soldado": 1, "instrutor": 2,
        "escopeteiro": 3, "escopeteiro_regular": 3,
        "sniper": 4, "sniper_regular": 4,
        "bombardeiro": 5, "granadeiro": 5,
        "morteiro_basico": 5, "morteiro": 5,
        "radio": 7, "torre_radio": 7,
        "lanca_chamas_bolso": 9, "lanca_chamas": 9,
        "lancador_veneno": 9, "canhao_veneno": 9,
        "barreira": 10, "barreira_reativa": 10,
        "mina": 11, "mina_segura": 11,
    },
    "desert": {
        "recruta": 0, "soldado": 1, "instrutor": 2,
        "escopeteiro": 3, "escopeteiro_regular": 3,
        "sniper": 4, "sniper_regular": 4,
        "morteiro_basico": 5, "morteiro": 5,
        "bombardeiro": 6, "granadeiro": 5,
        "radio": 8, "torre_radio": 7,
        "lanca_chamas_bolso": 10, "lanca_chamas": 9,
        "barreira": 11, "barreira_reativa": 10,
        "mina": 11, "mina_segura": 11,
    },
    "beach": {
        "recruta": 0, "soldado": 1, "instrutor": 2,
        "escopeteiro": 3, "escopeteiro_regular": 3,
        "sniper": 4, "sniper_regular": 4,
        "morteiro_basico": 5, "morteiro": 5,
        "bombardeiro": 7, "granadeiro": 5,
        "radio": 9, "torre_radio": 7,
        "lancador_agua": 9, "canhao_mare": 9,
        "barreira": 11, "barreira_reativa": 10,
        "mina": 11, "mina_segura": 11,
    },
}


# Estas cartas não possuíam um retrato exclusivo na folha regional. Cada uma
# recebe uma arte v7.8 que representa precisamente a classe indicada, em vez
# de reutilizar uma arte de outra carta só por ocupar a mesma célula do atlas.
CARD_ART_ASSETS = {
    ("city", "lancador_veneno"): "city_poison_sprayer_n1",
    ("city", "canhao_veneno"): "city_poison_cannon_n2",
    ("city", "morteiro_basico"): "city_mortar_n1",
    ("city", "morteiro"): "city_mortar_n2",
    ("desert", "mina"): "desert_mine_n1",
    ("desert", "morteiro"): "desert_mortar_n2",
    ("beach", "lancador_agua"): "beach_water_launcher_n1",
    ("beach", "canhao_mare"): "beach_water_cannon_n2",
    ("beach", "morteiro_basico"): "beach_mortar_n1",
    ("beach", "morteiro"): "beach_mortar_n2",
}


def regional_sprite_index(region: str, key: str) -> int:
    """Escolhe a célula correta da folha de artes para a região e o nível.

    A grade de seleção e o objeto posicionado usam esta mesma regra. Antes,
    a carta usava o índice genérico enquanto a tropa no campo recebia um
    remapeamento regional separado; daí surgiam N1 e N2 com artes trocadas
    em alguns mapas. Uma única fonte elimina essa mistura.
    """
    return int(CARD_ATLAS_INDEX.get(region, {}).get(key, DEFENSES[key]["sprite"]))


ENEMIES = {
    "caminhante": {
        "name": "Caminhante",
        "hp": 108,
        "speed": 12,
        "damage": 12,
        "attack": 1.2,
        "sprite": 0,
        "ability": "Lento, pouca vida e pouco dano. Pressiona apenas pelo número.",
    },
    "corredor": {
        "name": "Corredor",
        "hp": 94,
        "speed": 24,
        "damage": 27,
        "attack": 0.75,
        "sprite": 1,
        "ability": "Dá um arranque inicial; pune linhas sem escopeta, mina ou barreira.",
        "tags": ("dash",),
    },
    "rastejante": {
        "name": "Rastejante",
        "hp": 158,
        "speed": 9,
        "damage": 29,
        "attack": 1.05,
        "sprite": 1,
        "ability": "Mais lento que o Caminhante, mas morde com força quando alcança uma defesa.",
    },
    "conehead": {
        "name": "Blindado de Cone",
        "hp": 185,
        "speed": 11,
        "damage": 15,
        "attack": 1.0,
        "sprite": 2,
        "ability": "Cone e colete reflexivo absorvem fogo leve. Força foco ou explosão.",
        "armor": 0.18,
    },
    "policial": {
        "name": "Policial Infectado",
        "hp": 220,
        "speed": 10,
        "damage": 17,
        "attack": 1.0,
        "sprite": 3,
        "ability": "Colete balístico e tiros curtos contra a linha de defesa.",
        "armor": 0.25,
        "tags": ("gun",),
    },
    "militar": {
        "name": "Militar Infectado",
        "hp": 300,
        "speed": 9,
        "damage": 25,
        "attack": 0.9,
        "sprite": 4,
        "ability": "Armadura reforçada e arma de fogo. Exige dano concentrado ou corrosão controlada.",
        "armor": 0.38,
        "tags": ("gun",),
    },
    "escudo": {
        "name": "Porta-Escudo",
        "hp": 260,
        "speed": 8,
        "damage": 33,
        "attack": 1.05,
        "sprite": 5,
        "ability": "Escudo bloqueia boa parte do fogo frontal; a granada e o lança-chamas ajudam a quebrar a coluna.",
        "armor": 0.48,
        "tags": ("shield",),
    },
    "cuspidor": {
        "name": "Cuspidor Ácido",
        "hp": 178,
        "speed": 12,
        "damage": 14,
        "attack": 1.1,
        "sprite": 6,
        "ability": "Cospe até três blocos: corrosão reduz o desempenho e o ácido causa dano contínuo.",
        "tags": ("acid",),
    },
    "divisor": {
        "name": "Divisor",
        "hp": 300,
        "speed": 7,
        "damage": 34,
        "attack": 1.05,
        "sprite": 7,
        "ability": "Robusto e lento; sua morte explode em área, com dano físico e corrosivo.",
        "tags": ("acid", "explode_death"),
    },
    "gritador": {
        "name": "Gritador",
        "hp": 160,
        "speed": 11,
        "damage": 14,
        "attack": 1.1,
        "sprite": 8,
        "ability": "Acelera infectados próximos e pode chamar uma pequena horda.",
        "tags": ("scream",),
    },
    "saltador": {
        "name": "Saltador",
        "hp": 152,
        "speed": 16,
        "damage": 24,
        "attack": 0.9,
        "sprite": 9,
        "ability": "Ultrapassa somente a primeira defesa que bloquear seu caminho; depois precisa enfrentar a próxima.",
        "tags": ("jump",),
    },
    "bruto": {
        "name": "Bruto de Demolição",
        "hp": 450,
        "speed": 7,
        "damage": 48,
        "attack": 0.9,
        "sprite": 10,
        "ability": "Sub-chefe pesado; seus impactos deixam a linha vulnerável.",
        "tags": ("stomp",),
    },
    "digger": {
        "name": "Escavador",
        "hp": 185,
        "speed": 13,
        "damage": 42,
        "attack": 0.88,
        "sprite": 2,
        "ability": "Cava visivelmente sob o terreno e atravessa apenas a primeira defesa da frente, como um salto subterrâneo.",
        "tags": ("dig",),
    },
    "ladrao": {
        "name": "Ladrão de Suprimentos",
        "hp": 135,
        "speed": 14,
        "damage": 10,
        "attack": 1.2,
        "sprite": 3,
        "ability": "Mago das ruínas: rouba créditos. Clique nele antes que alcance a linha para recuperar a carga.",
        "tags": ("steal",),
    },
    "curandeiro": {
        "name": "Curandeiro Mortal",
        "hp": 190,
        "speed": 10,
        "damage": 12,
        "attack": 1.1,
        "sprite": 4,
        "ability": "Arremessa poções que curam aliados e pode devolver um derrotado à luta uma vez.",
        "tags": ("heal",),
    },
    "parasita": {
        "name": "Parasita das Dunas",
        "hp": 255,
        "speed": 9,
        "damage": 30,
        "attack": 1.0,
        "sprite": 5,
        "ability": "Agarra uma tropa, corta seu ataque e atordoa até dois blocos à frente.",
        "tags": ("parasite",),
    },
    "mutante": {
        "name": "Mutante de Ruínas",
        "hp": 400,
        "speed": 7,
        "damage": 42,
        "attack": 0.9,
        "sprite": 6,
        "ability": "Sub-chefe com hospedeiro armado nas costas e soco que atordoa uma área.",
        "tags": ("stomp", "gun"),
    },
    "necromante_minion": {
        "name": "Múmia Invocada",
        "hp": 130,
        "speed": 15,
        "damage": 18,
        "attack": 1.0,
        "sprite": 7,
        "ability": "Múmia fraca convocada pelo Necromante; existe para consumir munição e cobertura.",
    },
    "boia": {
        "name": "Turista de Boia",
        "hp": 135,
        "speed": 9,
        "damage": 15,
        "attack": 1.1,
        "sprite": 0,
        "ability": "Lento na água, mas a boia o protege de uma parte do dano.",
        "armor": 0.12,
    },
    "surfista": {
        "name": "Surfista Infectado",
        "hp": 122,
        "speed": 25,
        "damage": 25,
        "attack": 0.8,
        "sprite": 1,
        "ability": "A prancha cria um dash aquático, obrigando reação rápida nas faixas molhadas.",
        "tags": ("dash",),
    },
    "salva_vidas": {
        "name": "Salva-Vidas de Escudo",
        "hp": 225,
        "speed": 10,
        "damage": 25,
        "attack": 1.0,
        "sprite": 2,
        "ability": "Boia-escudo reduz o dano frontal e protege a maré atrás dele.",
        "armor": 0.40,
        "tags": ("shield",),
    },
    "mergulhador": {
        "name": "Mergulhador Blindado",
        "hp": 275,
        "speed": 10,
        "damage": 33,
        "attack": 0.92,
        "sprite": 3,
        "ability": "Armadura de mergulho espessa; pode atingir embarcações com força.",
        "armor": 0.30,
    },
    "cacador": {
        "name": "Caçador da Costa",
        "hp": 180,
        "speed": 15,
        "damage": 32,
        "attack": 0.85,
        "sprite": 4,
        "ability": "Persegue a defesa mais próxima com investida de arpão.",
        "tags": ("jump",),
    },
    "cowboy": {
        "name": "Cowboy da Maré",
        "hp": 205,
        "speed": 12,
        "damage": 18,
        "attack": 1.0,
        "sprite": 5,
        "ability": "Dispara de longe na costa e pressiona o rádio e a retaguarda.",
        "tags": ("gun",),
    },
    "sal_cuspidor": {
        "name": "Cuspidor de Sal",
        "hp": 182,
        "speed": 12,
        "damage": 15,
        "attack": 1.0,
        "sprite": 6,
        "ability": "Sal pressurizado corrói metal e descarrega as armas em contato.",
        "tags": ("acid",),
    },
    "mar_gritador": {
        "name": "Gritador de Maré",
        "hp": 175,
        "speed": 11,
        "damage": 15,
        "attack": 1.0,
        "sprite": 7,
        "ability": "O grito acelera nadadores e chama reforços vindos da arrebentação.",
        "tags": ("scream",),
    },
    "nadador": {
        "name": "Nadador",
        "hp": 180,
        "speed": 18,
        "damage": 25,
        "attack": 0.92,
        "sprite": 8,
        "ability": "Movimenta-se bem nas faixas de água e passa por minas terrestres.",
    },
}


BOSSES = {
    "bruto_demolidor": {
        "name": "BRUTO DEMOLIDOR",
        "hp": 1000,
        "speed": 6,
        "damage": 30,
        "attack": 1.05,
        "sprite": 10,
        "ability": "Entrada: paralisa militares por 3 s. Depois, o Martelo fecha só a própria faixa por 1,2 s a cada 18 s.",
        "type": "bruto_demolidor",
    },
    "comandante_mortos": {
        "name": "COMANDANTE DOS MORTOS",
        "hp": 1200,
        "speed": 9,
        "damage": 26,
        "attack": 0.88,
        "sprite": 11,
        "ability": "Entrada: dá fúria breve à escolta. Depois, dispara rajadas duplas leves e reacelera somente aliados próximos.",
        "type": "comandante",
    },
    "cuspidor_alfa": {
        "name": "CUSPIDADOR ALFA",
        "hp": 1600,
        "speed": 11,
        "damage": 28,
        "attack": 0.95,
        "sprite": 11,
        "ability": "Entrada: névoa ácida global de 1,2 s. Depois, cospe em um alvo na própria faixa, com corrosão curta.",
        "type": "alfa",
    },
    "mutante_ruinas": {
        "name": "MUTANTE DAS RUÍNAS",
        "hp": 1100,
        "speed": 6,
        "damage": 32,
        "attack": 0.98,
        "sprite": 6,
        "ability": "Entrada: abalo leve nas faixas vizinhas. Depois, golpeia somente tropas próximas por 1 s de atordoamento.",
        "type": "mutante",
    },
    "necromante": {
        "name": "NECROMANTE",
        "hp": 1350,
        "speed": 7,
        "damage": 23,
        "attack": 0.95,
        "sprite": 10,
        "ability": "Entrada: invoca uma múmia. Depois, invoca uma por ciclo e cura pouco os aliados próximos.",
        "type": "necromante",
    },
    "colosso_mutante": {
        "name": "COLOSSO MUTANTE",
        "hp": 1850,
        "speed": 4,
        "damage": 38,
        "attack": 1.05,
        "sprite": 11,
        "ability": "Entrada: tremor global de 1,2 s. Depois, arremessa uma rocha leve contra uma faixa-alvo.",
        "type": "colosso",
    },
    "tide_brute": {
        "name": "BRUTO DA MARÉ",
        "hp": 1050,
        "speed": 6,
        "damage": 34,
        "attack": 1.0,
        "sprite": 9,
        "ability": "Entrada: uma onda leve abala a faixa de água. Depois, golpeia boias e embarcações apenas perto da maré.",
        "type": "tide",
    },
    "cacador_abissal": {
        "name": "CAÇADOR ABISSAL",
        "hp": 1450,
        "speed": 11,
        "damage": 26,
        "attack": 0.95,
        "sprite": 10,
        "ability": "Entrada: avança uma distância curta no canal. Depois, mergulha pouco e ataca uma embarcação próxima.",
        "type": "hunter",
    },
    "leviata": {
        "name": "LEVIATÃ",
        "hp": 2050,
        "speed": 5,
        "damage": 42,
        "attack": 1.0,
        "sprite": 11,
        "ability": "Entrada: uma maré moderada atinge o canal. Depois, lança um jato concentrado numa embarcação da própria faixa.",
        "type": "leviathan",
    },
}


REGION_ENEMIES = {
    "city": ("caminhante", "corredor", "rastejante", "conehead", "policial", "militar", "escudo", "cuspidor", "divisor", "gritador", "saltador", "bruto"),
    "desert": ("caminhante", "rastejante", "conehead", "digger", "ladrao", "curandeiro", "parasita", "mutante", "necromante_minion", "escudo", "cuspidor"),
    "beach": ("boia", "surfista", "salva_vidas", "mergulhador", "cacador", "cowboy", "sal_cuspidor", "mar_gritador", "nadador", "saltador"),
}

# A Praia tem um canal real na terceira faixa. Criaturas de maré não podem
# simplesmente reaproveitar qualquer linha terrestre, pois isso quebraria a
# leitura do cenário e faria nadadores parecerem caminhar sobre a areia.
# Cowboy e Saltador são ameaças costeiras terrestres; o restante desta lista
# nasce exclusivamente no canal.
BEACH_WATER_ENEMIES = frozenset(
    {
        "boia",
        "surfista",
        "salva_vidas",
        "mergulhador",
        "cacador",
        "sal_cuspidor",
        "mar_gritador",
        "nadador",
    }
)


def wave_enemy_pool(region: str, wave: int) -> tuple[str, ...]:
    """Retorna o elenco regional já liberado em uma onda, sem sorteio.

    A função é usada pela diretoria e pelo teste de regressão. Isso garante
    que um inimigo apresentado no dossiê regional não fique preso fora da
    campanha por uma fórmula de aleatoriedade escondida.
    """
    roster = REGION_ENEMIES[region]
    clamped_wave = int(clamp(wave, 1, 15))
    unlocked_count = 1 + ((clamped_wave - 1) * (len(roster) - 1)) // 14
    return tuple(roster[:unlocked_count])


def make_save() -> dict:
    # As regiões são escolhas de estilo e desafio, não uma trava de conteúdo.
    return {"unlocked": list(REGIONS), "completed": [], "best_wave": {}}


def load_save() -> dict:
    try:
        data = json.loads(SAVE_PATH.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or "unlocked" not in data:
            raise ValueError
        data.setdefault("completed", [])
        data.setdefault("best_wave", {})
        # Atualiza saves antigos sem apagar os melhores resultados já gravados.
        data["unlocked"] = list(REGIONS)
        return data
    except (OSError, ValueError, json.JSONDecodeError):
        return make_save()


def save_campaign(data: dict) -> None:
    try:
        SAVE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        pass


class FontBook:
    def __init__(self) -> None:
        self.title = pygame.font.SysFont("arial", 45, bold=True)
        self.h1 = pygame.font.SysFont("arial", 28, bold=True)
        self.h2 = pygame.font.SysFont("arial", 20, bold=True)
        self.body = pygame.font.SysFont("arial", 16)
        self.small = pygame.font.SysFont("arial", 13)
        self.tiny = pygame.font.SysFont("arial", 11)


class Assets:
    """Carrega uma única fonte por quadro para manter a abertura leve."""

    def __init__(self) -> None:
        self.images: dict[str, pygame.Surface] = {}
        self.unit_sprites: dict[str, list[pygame.Surface]] = {}
        self.unit_l2_sprites: dict[str, list[pygame.Surface]] = {}
        self.zombie_sprites: dict[str, list[pygame.Surface]] = {}
        self.animation_frames: dict[str, list[pygame.Surface]] = {}
        self.effect_frames: dict[str, list[pygame.Surface]] = {}
        self.scale_cache: dict[tuple[int, int, int], pygame.Surface] = {}
        self.trim_cache: dict[int, pygame.Surface] = {}
        self.jobs: list[tuple[str, Path, str]] = []
        for region, info in REGIONS.items():
            self.jobs.extend(
                [
                    (f"{region}_bg", ASSET_DIR / info["bg"], "image"),
                    (f"{region}_units", ASSET_DIR / info["soldiers"], "units"),
                    (f"{region}_units_l2", ASSET_DIR / info["soldiers_l2"], "units_l2"),
                    (f"{region}_zombies", ASSET_DIR / info["zombies"], "zombies"),
                ]
            )
        # A referência enviada para a Beta 3 entra primeiro na fila. Assim a
        # tela de abertura já nasce com a arte correta enquanto os atlases
        # pesados continuam chegando um por quadro.
        self.jobs.insert(0, ("loading_beta3", ASSET_DIR / "loading_beta3_reference.png", "image"))
        self.jobs.insert(1, ("menu", ASSET_DIR / "menu.png", "image"))
        # Cada cenário usa sua própria contenção de última linha. Todas são
        # carregadas antes do menu, sem travar quando uma faixa é invadida.
        self.jobs[2:2] = [
            # O Caminhante urbano inaugura a cadeia de animação desenhada:
            # oito contatos/passagens originais, todos pré-carregados antes
            # da partida e ainda deformados suavemente pela malha OpenGL.
            ("city_walker_walk", ASSET_DIR / "city_walker_walk_sheet_beta4.png", "animation"),
            ("desert_digger_states", ASSET_DIR / "desert_digger_state_sheet_beta4.png", "animation"),
            ("beach_swimmer_walk", ASSET_DIR / "beach_swimmer_walk_sheet_beta4.png", "animation"),
            # Quatro poses inteiras por chefe: dois contatos de movimento,
            # ataque e poder. Ao contrário do atlas geral, nenhum martelo,
            # membro ou efeito atravessa o limite de outra célula.
            ("city_boss_actions", ASSET_DIR / "city_boss_actions_beta4.png", "animation_4x3"),
            ("desert_boss_actions", ASSET_DIR / "desert_boss_actions_beta4.png", "animation_4x3"),
            ("beach_boss_actions", ASSET_DIR / "beach_boss_actions_beta4.png", "animation_4x3"),
            # Matéria e impacto rasterizados substituem linhas, polígonos,
            # anéis e bolinhas usados como efeitos nas versões anteriores.
            ("elemental_effects", ASSET_DIR / "elemental_effects_sheet_beta4.png", "effects_4x3"),
            ("combat_effects", ASSET_DIR / "combat_effects_sheet_beta4.png", "effects_4x3"),
            ("ability_effects", ASSET_DIR / "ability_effects_sheet_beta4.png", "effects_4x3"),
            # Munições e projéteis são objetos pintados de verdade. Não há
            # mais círculos, riscos ou polígonos fingindo ser balas no campo.
            ("projectile_sprites", ASSET_DIR / "projectile_sprites_sheet_beta4.png", "effects_4x3"),
            # Retrato individual da Beta 3: o Saltador deixa de trazer uma
            # pilastra/obstáculo embutido e a animação faz o salto real.
            ("zombie_jumper_beta3", ASSET_DIR / "zombie_jumper_beta3.png", "sprite"),
            # O Rastejante urbano não compartilha mais a silhueta do Corredor:
            # é um infectado baixo, sem pernas funcionais, com arte própria.
            ("zombie_crawler_beta3", ASSET_DIR / "zombie_crawler_beta3.png", "sprite"),
            # A Cidade agora combate toxina com toxina. N1 e N2 têm silhuetas
            # próprias, sem reaproveitar o lança-chamas exclusivo do Deserto.
            ("city_poison_sprayer_n1", ASSET_DIR / "city_poison_sprayer_n1_beta3.png", "sprite"),
            ("city_poison_cannon_n2", ASSET_DIR / "city_poison_cannon_n2_beta3.png", "sprite"),
            # Efeito original da Beta 4: a animação de veneno tem uma arte de
            # impacto própria, em vez de repetir apenas círculos genéricos.
            ("beta4_toxic_impact", ASSET_DIR / "beta4_toxic_impact.png", "sprite"),
            ("lane_bomb_cart", ASSET_DIR / "lane_bomb_cart_v72.png", "sprite"),
            ("desert_lane_bomb_cart", ASSET_DIR / "desert_lane_bomb_cart_v73.png", "sprite"),
            ("beach_land_bomb_cart", ASSET_DIR / "beach_land_bomb_cart_v73.png", "sprite"),
            ("beach_water_bomb", ASSET_DIR / "beach_water_bomb_v73.png", "sprite"),
            # Minas posicionáveis não reutilizam caixas, suprimentos, ponte ou
            # carrinhos de contenção. Cada uma é um explosivo isolado legível.
            ("city_mine_n1", ASSET_DIR / "mine_city_n1_v75.png", "sprite"),
            ("city_mine_n2", ASSET_DIR / "mine_city_n2_v75.png", "sprite"),
            ("beach_mine_land_n1", ASSET_DIR / "mine_beach_land_n1_v75.png", "sprite"),
            ("beach_mine_land_n2", ASSET_DIR / "mine_beach_land_n2_v75.png", "sprite"),
            ("beach_mine_water", ASSET_DIR / "mine_beach_water_v75.png", "sprite"),
            # Recortes próprios v7.8: as cartas abaixo não compartilhavam
            # mais uma arte genérica com outra função ou outro nível.
            ("city_mortar_n1", ASSET_DIR / "city_mortar_n1_v78.png", "sprite"),
            ("city_mortar_n2", ASSET_DIR / "city_mortar_n2_v78.png", "sprite"),
            ("desert_mine_n1", ASSET_DIR / "desert_mine_n1_v78.png", "sprite"),
            ("desert_mortar_n2", ASSET_DIR / "desert_mortar_n2_v78.png", "sprite"),
            ("beach_water_launcher_n1", ASSET_DIR / "beach_water_launcher_n1_v79.png", "sprite"),
            ("beach_water_cannon_n2", ASSET_DIR / "beach_water_cannon_n2_v79.png", "sprite"),
            ("beach_mortar_n1", ASSET_DIR / "beach_mortar_n1_v78.png", "sprite"),
            ("beach_mortar_n2", ASSET_DIR / "beach_mortar_n2_v78.png", "sprite"),
            # O Atirador de Lancha continua aquático. A antiga Mecânica de
            # Drones não é mais carregada: a recarga agora pertence à arma.
            ("beach_boat_shooter", ASSET_DIR / "beach_boat_shooter_v76.png", "sprite"),
        ]
        self.loaded = 0
        self.error: str | None = None

    @property
    def total(self) -> int:
        return len(self.jobs)

    @property
    def complete(self) -> bool:
        return self.loaded >= self.total

    def load_next(self) -> None:
        if self.complete:
            return
        key, path, kind = self.jobs[self.loaded]
        try:
            source = pygame.image.load(str(path)).convert_alpha()
            if kind == "image":
                if key.endswith("_bg"):
                    self.images[key] = self.fit_four_lane_background(source, key.split("_")[0])
                else:
                    self.images[key] = pygame.transform.smoothscale(source, (WIDTH, HEIGHT))
            elif kind == "sprite":
                self.images[key] = source
            elif kind == "animation":
                self.animation_frames[key] = self.slice_grid(source, 4, 2)
            elif kind == "animation_4x3":
                self.animation_frames[key] = self.slice_grid(source, 4, 3)
            elif kind == "effects_4x3":
                self.effect_frames[key] = [self.trim_alpha(frame) for frame in self.slice_grid(source, 4, 3)]
            else:
                sprites = self.slice_atlas(source)
                if kind == "units":
                    self.unit_sprites[key.split("_")[0]] = sprites
                elif kind == "units_l2":
                    self.unit_l2_sprites[key.split("_")[0]] = sprites
                else:
                    self.zombie_sprites[key.split("_")[0]] = sprites
        except pygame.error as exc:
            self.error = f"Falha ao carregar {path.name}: {exc}"
            # Um arquivo ausente gera mensagem explícita na tela de carga. O
            # fallback fica transparente para nunca fingir uma animação com
            # círculo, bloco colorido ou outro símbolo provisório.
            placeholder = pygame.Surface((1, 1), pygame.SRCALPHA)
            if kind == "image":
                self.images[key] = pygame.transform.smoothscale(placeholder, (WIDTH, HEIGHT))
            elif kind == "sprite":
                self.images[key] = placeholder
            elif kind == "animation":
                self.animation_frames[key] = [placeholder] * 8
            elif kind == "animation_4x3":
                self.animation_frames[key] = [placeholder] * 12
            elif kind == "effects_4x3":
                self.effect_frames[key] = [placeholder] * 12
            elif kind == "units":
                self.unit_sprites[key.split("_")[0]] = [placeholder] * 12
            elif kind == "units_l2":
                self.unit_l2_sprites[key.split("_")[0]] = [placeholder] * 12
            else:
                self.zombie_sprites[key.split("_")[0]] = [placeholder] * 12
        self.loaded += 1

    @staticmethod
    def fit_four_lane_background(source: pygame.Surface, region: str) -> pygame.Surface:
        """Remapeia as quatro pistas pintadas para a geometria da simulação."""
        source_width, source_height = source.get_size()
        canvas = pygame.Surface((WIDTH, HEIGHT)).convert()
        proportions = {
            # topo, começo da pista 1, três divisões, fim da pista 4, rodapé
            "city": (0.0, 0.220, 0.369, 0.508, 0.732, 0.872, 1.0),
            "desert": (0.0, 0.335, 0.445, 0.566, 0.703, 0.822, 1.0),
            "beach": (0.0, 0.162, 0.298, 0.438, 0.583, 0.830, 1.0),
        }[region]
        source_breaks = tuple(int(source_height * value) for value in proportions[:-1]) + (source_height,)
        target_breaks = (0, *LANE_BOUNDS[region], HEIGHT)
        for source_top, source_bottom, target_top, target_bottom in zip(
            source_breaks,
            source_breaks[1:],
            target_breaks,
            target_breaks[1:],
        ):
            source_rect = pygame.Rect(0, source_top, source_width, max(1, source_bottom - source_top))
            target_size = (WIDTH, max(1, target_bottom - target_top))
            band = source.subsurface(source_rect)
            canvas.blit(pygame.transform.smoothscale(band, target_size), (0, target_top))
        return canvas

    @staticmethod
    def slice_atlas(source: pygame.Surface) -> list[pygame.Surface]:
        width, height = source.get_size()
        tiles: list[pygame.Surface] = []
        for row in range(3):
            for col in range(4):
                rect = pygame.Rect(col * width // 4, row * height // 3, width // 4, height // 3)
                tile = source.subsurface(rect).copy()
                if tile.get_flags() & pygame.SRCALPHA == 0:
                    tile.set_colorkey((0, 0, 0))
                tiles.append(tile)
        return tiles

    @staticmethod
    def slice_grid(source: pygame.Surface, columns: int, rows: int) -> list[pygame.Surface]:
        """Recorta uma folha regular preservando seu canal alfa original."""
        width, height = source.get_size()
        frames: list[pygame.Surface] = []
        for row in range(rows):
            for column in range(columns):
                rect = pygame.Rect(
                    column * width // columns,
                    row * height // rows,
                    width // columns,
                    height // rows,
                )
                frames.append(source.subsurface(rect).copy())
        return frames

    @staticmethod
    def trim_alpha(source: pygame.Surface) -> pygame.Surface:
        """Remove apenas a margem transparente de um VFX ou projétil."""
        bounds = source.get_bounding_rect(min_alpha=8)
        if bounds.width <= 0 or bounds.height <= 0:
            return pygame.Surface((1, 1), pygame.SRCALPHA)
        return source.subsurface(bounds).copy()

    def base_unit(self, region: str, index: int) -> pygame.Surface:
        sprites = self.unit_sprites.get(region, [])
        if not sprites:
            return pygame.Surface((1, 1), pygame.SRCALPHA)
        return sprites[index % len(sprites)]

    def unit(self, region: str, index: int, level: int = 1) -> pygame.Surface:
        """N1 usa o atlas base; N2 recebe silhueta e uniforme próprios."""
        if level >= 2:
            sprites = self.unit_l2_sprites.get(region, [])
            if sprites:
                return sprites[index % len(sprites)]
        return self.base_unit(region, index)

    def zombie(self, region: str, index: int) -> pygame.Surface:
        sprites = self.zombie_sprites.get(region, [])
        if not sprites:
            return pygame.Surface((1, 1), pygame.SRCALPHA)
        return sprites[index % len(sprites)]

    def scaled(self, sprite: pygame.Surface, width: float, height: float) -> pygame.Surface:
        """Evita redimensionar os mesmos retratos gigantes a cada quadro."""
        size = (max(1, int(width)), max(1, int(height)))
        key = (id(sprite), *size)
        cached = self.scale_cache.get(key)
        if cached is None:
            cached = pygame.transform.smoothscale(sprite, size)
            self.scale_cache[key] = cached
        return cached

    def trimmed(self, sprite: pygame.Surface) -> pygame.Surface:
        """Remove só a margem transparente do recorte usado no campo.

        Cartas continuam usando o enquadramento integral do atlas. Em batalha,
        o recorte justo garante que a última linha opaca da bota, roda ou casco
        coincida de verdade com a âncora do terreno.
        """
        key = id(sprite)
        cached = self.trim_cache.get(key)
        if cached is not None:
            return cached
        bounds = sprite.get_bounding_rect(min_alpha=8)
        if bounds.width <= 1 or bounds.height <= 1:
            self.trim_cache[key] = sprite
            return sprite
        bounds = bounds.inflate(4, 4).clip(sprite.get_rect())
        trimmed = sprite.subsurface(bounds).copy()
        self.trim_cache[key] = trimmed
        return trimmed

    def actor_sources(self) -> list[pygame.Surface]:
        """Lista exatamente os recortes que poderão virar atores OpenGL."""
        candidates: list[pygame.Surface] = []
        for store in (self.unit_sprites, self.unit_l2_sprites, self.zombie_sprites, self.animation_frames):
            for sprites in store.values():
                candidates.extend(sprites)
        for key, _path, kind in self.jobs:
            if kind == "sprite" and key != "beta4_toxic_impact" and key in self.images:
                candidates.append(self.images[key])
        unique: list[pygame.Surface] = []
        seen: set[int] = set()
        for sprite in candidates:
            trimmed = self.trimmed(sprite)
            if id(trimmed) not in seen:
                seen.add(id(trimmed))
                unique.append(trimmed)
        return unique


@dataclass
class Defender:
    key: str
    display_name: str
    row: int
    col: int
    stats: dict
    sprite_index: int
    hp: float = field(init=False)
    ammo: int = field(init=False)
    attack_timer: float = 0.0
    utility_timer: float = 0.0
    reload_timer: float = 0.0
    reload_total: float = 0.0
    stun: float = 0.0
    corrosion: float = 0.0
    ascended: float = 0.0
    drone_timer: float = 0.0
    turret_timer: float = 0.0
    pulse: float = 0.0
    region: str = "city"
    motion: ActorMotion = field(default_factory=ActorMotion)

    def __post_init__(self) -> None:
        self.hp = float(self.stats["hp"])
        self.ammo = int(self.stats["ammo"])
        if self.stats["role"] == "promoter":
            self.utility_timer = float(self.stats["cooldown"])

    @property
    def x(self) -> float:
        return cell_center(self.row, self.col, self.region)[0]

    @property
    def y(self) -> float:
        return cell_center(self.row, self.col, self.region)[1]

    @property
    def max_hp(self) -> float:
        return float(self.stats["hp"])

    @property
    def max_ammo(self) -> int:
        return int(self.stats["ammo"])

    def has_ammo(self) -> bool:
        return self.max_ammo == 0 or self.ammo > 0

    @property
    def reloading(self) -> bool:
        return self.max_ammo > 0 and self.ammo <= 0 and self.reload_timer > 0

    def hitbox(self) -> pygame.Rect:
        width, height = defender_render_scale(self)
        return pygame.Rect(int(self.x - width / 2), int(self.y - height), int(width), int(height + 12))


@dataclass
class Enemy:
    key: str
    row: int
    data: dict
    region: str
    wave: int
    difficulty: str = "medium"
    x: float = field(default_factory=lambda: BOARD.right + 100)
    hp: float = field(init=False)
    attack_timer: float = 0.0
    attack_windup: float = 0.0
    attack_target: Defender | None = None
    attack_damage: float = 0.0
    skill_timer: float = 1.8
    age: float = 0.0
    stun: float = 0.0
    burn: float = 0.0
    poisoned: float = 0.0
    soaked: float = 0.0
    corrosion: float = 0.0
    jump_used: bool = False
    burrowed: bool = False
    jump_state: str = ""
    jump_timer: float = 0.0
    jump_duration: float = 0.0
    jump_start_x: float = 0.0
    jump_end_x: float = 0.0
    dig_used: bool = False
    dig_state: str = ""
    dig_timer: float = 0.0
    dig_duration: float = 0.0
    dig_start_x: float = 0.0
    dig_end_x: float = 0.0
    stolen: float = 0.0
    revived: bool = False
    rage: float = 0.0
    boss_announced: bool = False
    step_timer: float = 0.0
    dot_timer: float = 0.0
    motion: ActorMotion = field(default_factory=ActorMotion)

    def __post_init__(self) -> None:
        profile = difficulty_profile(self.difficulty)
        scale = boss_wave_scale(self.wave) if self.key in BOSSES else enemy_wave_scale(self.wave)
        scale *= float(profile["boss_hp" if self.key in BOSSES else "enemy_hp"])
        self.hp = float(self.data["hp"]) * scale

    @property
    def y(self) -> float:
        return terrain_y(self.region, self.row, self.x)

    @property
    def max_hp(self) -> float:
        profile = difficulty_profile(self.difficulty)
        scale = boss_wave_scale(self.wave) if self.is_boss else enemy_wave_scale(self.wave)
        scale *= float(profile["boss_hp" if self.is_boss else "enemy_hp"])
        return float(self.data["hp"]) * scale

    @property
    def is_boss(self) -> bool:
        return self.key in BOSSES

    @property
    def tags(self) -> tuple:
        return tuple(self.data.get("tags", ()))

    def hitbox(self) -> pygame.Rect:
        width, height = enemy_render_scale(self, self.region)
        return pygame.Rect(int(self.x - width / 2), int(self.y - height), int(width), int(height + 10))


@dataclass
class Projectile:
    x: float
    y: float
    target: Enemy | Defender | None
    target_x: float
    target_y: float
    damage: float
    kind: str
    owner: Defender | Enemy | None
    radius: float = 0.0
    friendly: bool = True
    travel: float = 0.22
    elapsed: float = 0.0
    effect: str = ""

    def __post_init__(self) -> None:
        # Protege o loop de animação contra chamadas antigas que passaram o
        # efeito como último argumento posicional (onde elapsed ficava string).
        if isinstance(self.elapsed, str):
            if not self.effect:
                self.effect = self.elapsed
            self.elapsed = 0.0
        self.elapsed = float(self.elapsed)
        self.travel = max(0.01, float(self.travel))


@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    ttl: float
    size: float
    color: tuple[int, int, int]
    gravity: float = 0.0


@dataclass
class FloatingText:
    text: str
    x: float
    y: float
    color: tuple[int, int, int]
    ttl: float = 1.0


@dataclass
class SpawnOrder:
    wait: float
    key: str
    row: int
    boss: bool = False


@dataclass
class LaneBomb:
    """Carrinho-bomba de emergência, um por faixa de combate."""

    row: int
    x: float = field(default_factory=lambda: float(LANE_BOMB_HOME_X))
    state: str = "armed"  # armed -> rolling -> spent
    kills: int = 0
    motion: ActorMotion = field(default_factory=ActorMotion)


def defender_render_scale(defender: Defender) -> tuple[float, float]:
    """Tamanho visual único para a tropa ativa e sua animação de queda."""
    role = defender.stats["role"]
    if role == "mine":
        base = (76, 62) if defender.stats.get("water_only") else (82, 68)
        depth = lane_depth(defender.region, defender.row)
        return base[0] * depth, base[1] * depth
    if role in {"barrier", "boat", "sub"}:
        base = (105, 82)
    else:
        base = (86, 98)
    depth = lane_depth(defender.region, defender.row)
    return base[0] * depth, base[1] * depth


def enemy_render_scale(enemy: Enemy, region: str) -> tuple[float, float]:
    """Mantém infectados e soldados na mesma escala física do cenário.

    Os atlases terrestres têm mais respiro transparente e silhuetas mais
    estreitas que os atlases de tropas. Por isso o tamanho nominal anterior
    fazia um Caminhante parecer uma miniatura mesmo usando quase a mesma caixa
    de um soldado. Água já tinha uma leitura correta e preserva sua escala.
    """
    water_actor = region == "beach" and enemy.row in BEACH_WATER_ROWS
    if enemy.is_boss:
        base = (132, 142) if water_actor else (148, 158)
    elif enemy.key == "rastejante" and region == "city":
        base = (126, 88)
    elif enemy.key == "saltador":
        base = (100, 116)
    elif enemy.key == "nadador" and region == "beach":
        base = (126, 72)
    elif water_actor:
        base = (82, 96)
    else:
        # Um zumbi terrestre comum fica cerca de 14% mais alto que um
        # combatente humano, sem ultrapassar a altura da pista dianteira.
        base = (98, 112)
    depth = lane_depth(region, enemy.row)
    return base[0] * depth, base[1] * depth


def defender_animation_profile(defender: Defender) -> str:
    """Perfil corporal usado pelo shader sem alterar a ficha da carta."""
    return str(defender.stats.get("role", "humanoid"))


def enemy_animation_profile(enemy: Enemy) -> str:
    """Escolhe marcha, mordida e gesto de habilidade pela anatomia do ator."""
    boss_profiles = {
        "bruto_demolidor": "hammer_boss",
        "comandante": "commander_boss",
        "alfa": "toxic_boss",
        "mutante": "hammer_boss",
        "necromante": "necromancer_boss",
        "colosso": "colossus_boss",
        "tide": "sea_boss",
        "hunter": "sea_boss",
        "leviathan": "leviathan_boss",
    }
    if enemy.is_boss:
        return boss_profiles.get(str(enemy.data.get("type", "")), "heavy")
    if enemy.key == "rastejante":
        return "crawler"
    if "jump" in enemy.tags:
        return "jumper"
    if "dig" in enemy.tags:
        return "digger"
    if "dash" in enemy.tags:
        return "runner"
    if "gun" in enemy.tags or "acid" in enemy.tags:
        return "shooter"
    if "heal" in enemy.tags or "steal" in enemy.tags:
        return "caster"
    if "stomp" in enemy.tags or "parasite" in enemy.tags or "explode_death" in enemy.tags:
        return "heavy"
    return "walker"


def actor_pose(
    motion: ActorMotion,
    *,
    enemy: bool,
    profile: str = "generic",
    progress: float = 0.0,
) -> tuple[float, float, float, float, float]:
    """Converte um estado semântico em pose, inclinação e escala.

    As quatro fases de cada ciclo são calculadas de forma determinística. Na
    prática isso funciona como uma pequena folha de sprites, só que não perde
    sincronia quando a máquina cai de 60 para 30 FPS.
    """
    direction = -1.0 if enemy else 1.0
    cycle = math.sin(motion.state_elapsed * math.tau * 1.75)
    pulse = math.sin(motion.state_elapsed * math.tau * 3.2)
    state = motion.state
    dx, dy, angle, scale_x, scale_y = 0.0, 0.0, 0.0, 1.0, 1.0
    if state == "spawn":
        p = clamp(motion.state_elapsed / 0.28, 0.0, 1.0)
        scale_x = scale_y = 0.72 + p * 0.28
        dy = (1.0 - p) * 18
    elif state == "walk":
        stride = 1.45 if profile == "runner" else 1.0
        dx = cycle * 2.2 * stride
        dy = -abs(cycle) * 3.2 * stride
        angle = cycle * 3.4 * direction * stride
        scale_x = 1.0 + abs(cycle) * 0.022
    elif state in {"brace", "idle", "armed"}:
        dy = -abs(cycle) * 1.1
        angle = cycle * 0.75 * direction
    elif state == "attack":
        p = progress or clamp(motion.state_elapsed / 0.28, 0.0, 1.0)
        thrust = math.sin(p * math.pi)
        dx = direction * thrust * (8.5 if enemy else 3.6)
        dy = thrust * (1.8 if enemy else -1.4)
        angle = direction * thrust * (11.0 if enemy else -4.0)
        scale_x = 1.0 + thrust * (0.065 if enemy else 0.025)
    elif state in {"support", "promote"}:
        dy = -abs(pulse) * 4.0
        angle = pulse * 3.0
        scale_x = scale_y = 1.0 + abs(pulse) * 0.045
    elif state == "reload":
        # O fallback mostra os mesmos quatro tempos do shader; a mão e o pente
        # são completados pelo deformador de braços e arma no apresentador.
        action = clamp(progress, 0.0, 1.0)
        reach = math.sin(clamp(action / 0.45, 0.0, 1.0) * math.pi)
        insert = math.sin(clamp((action - 0.38) / 0.58, 0.0, 1.0) * math.pi)
        dx = direction * (reach - insert) * 2.5
        dy = (reach + insert) * 1.7
        angle = direction * (reach * 5.5 - insert * 3.0)
        scale_y = 1.0 - reach * 0.018
    elif state == "hit":
        impact = math.sin(clamp(motion.state_elapsed / 0.16, 0.0, 1.0) * math.pi)
        dx = -direction * impact * 8.0
        dy = -impact * 2.5
        angle = -direction * impact * 10.0
    elif state == "stunned":
        dx = math.sin(motion.state_elapsed * 16.0) * 2.5
        angle = math.sin(motion.state_elapsed * 11.0) * 9.0
    elif state == "jump":
        angle = -direction * 10.0
        scale_x = 1.06
        scale_y = 0.96
    elif state.startswith("dig"):
        angle = direction * cycle * 2.0
        scale_x = 1.0 + abs(cycle) * 0.03
    elif state == "skill":
        action = progress or clamp(motion.state_elapsed / 0.46, 0.0, 1.0)
        power = math.sin(action * math.pi)
        if profile in {"hammer_boss", "colossus_boss"}:
            dy = power * 5.5
            angle = direction * (12.0 - action * 25.0) * power
            scale_x, scale_y = 1.0 + power * 0.07, 1.0 - power * 0.07
        elif profile in {"sea_boss", "leviathan_boss"}:
            dx = direction * power * 7.0
            dy = -power * 7.0
            angle = direction * power * 7.0
        else:
            dy = -power * 4.5
            angle = direction * math.sin(action * math.tau) * 7.0
            scale_x = scale_y = 1.0 + power * 0.06
    elif state == "roll":
        dx = cycle * 0.8
        dy = -abs(cycle) * 1.7
        angle = cycle * 1.4
    elif state == "dead":
        p = clamp(motion.state_elapsed / 0.48, 0.0, 1.0)
        dx = direction * p * 10.0
        angle = -direction * p * 28.0
        scale_x = 1.0 + p * 0.08
        scale_y = 1.0 - p * 0.22
    return dx, dy, angle, scale_x, scale_y


class Battle:
    def __init__(self, app: "Game", region: str, selected: list[tuple[str, str]]) -> None:
        self.app = app
        self.region = region
        self.difficulty = getattr(app, "difficulty", "medium")
        self.difficulty_data = difficulty_profile(self.difficulty)
        self.selected = selected
        self.defenders: list[Defender] = []
        self.enemies: list[Enemy] = []
        self.projectiles: list[Projectile] = []
        self.particles: list[Particle] = []
        self.texts: list[FloatingText] = []
        self.effects: list[VisualEffect] = []
        self.fallen: list[DefeatAnimation] = []
        # O suficiente para experimentar a primeira formação, mas sem tornar
        # a economia da campanha irrelevante.
        self.supplies = int(self.difficulty_data["initial_supplies"])
        self.wave = 0
        self.wave_banner = 0.0
        self.intermission = 2.5
        self.orders: list[SpawnOrder] = []
        self.spawn_timer = 0.0
        self.started_wave = False
        self.finished = False
        self.lost = False
        self.victory = False
        self.message = f"Modo {self.difficulty_data['label']}: posicione a equipe."
        self.message_timer = 4.0
        self.selected_card = 0
        self.use_core = False
        self.remove_mode = False
        self.cores = int(self.difficulty_data["initial_cores"])
        self.boss_seen: set[int] = set()
        self.ambient_phase = 0.0
        self.shake = 0.0
        self.global_toxic = 0.0
        self.boss_warning = 0.0
        self.boss_banner_name = ""
        self.boss_banner_subtitle = ""
        self.boss_alert_pending = False
        self.paused = False
        self.dead_history: list[tuple[str, int, float]] = []
        # Quatro faixas: AREIA, ÁGUA, ÁGUA, AREIA. As duas faixas centrais
        # dividem o canal contínuo pintado na nova Praia.
        self.water_rows = set(BEACH_WATER_ROWS) if region == "beach" else set()
        self.lane_bombs = [LaneBomb(row) for row in range(ROWS)]
        self.card_cooldowns = [0.0 for _ in selected]

    def announce(self, message: str, seconds: float = 2.5, color: tuple[int, int, int] = WHITE) -> None:
        self.message = message
        self.message_timer = seconds
        # Alertas de interface são exibidos na aba superior. Assim eles não
        # atravessam as cartas nem reintroduzem uma faixa de texto na partida.

    def cell_is_water(self, row: int, col: int) -> bool:
        if self.region != "beach":
            return False
        # As duas linhas centrais pertencem ao canal da Praia.
        return row in self.water_rows

    def ground_cell_rect(self, row: int, col: int) -> pygame.Rect:
        return cell_rect(row, col, self.region).inflate(-14, -10)

    def board_cell_at(self, pos: tuple[int, int]) -> tuple[int, int] | None:
        """Traduz um clique somente quando ele está dentro da faixa pintada."""
        if not BOARD.left <= pos[0] <= BOARD.right:
            return None
        col = int(clamp((pos[0] - BOARD.left) / CELL_W, 0, COLS - 1))
        for row in range(ROWS):
            top, bottom = lane_bounds(self.region, row)
            if top <= pos[1] < bottom or (row == ROWS - 1 and pos[1] == bottom):
                return row, col
        return None

    def card(self) -> tuple[str, str]:
        return self.selected[self.selected_card]

    def can_place(self, key: str, row: int, col: int) -> tuple[bool, str]:
        if not (0 <= row < ROWS and 0 <= col < COLS):
            return False, "Fora da área de combate."
        if any(d.row == row and d.col == col for d in self.defenders):
            return False, "Este ponto já está ocupado."
        data = DEFENSES[key]
        water = self.cell_is_water(row, col)
        if data.get("water_only") and not water:
            return False, "Unidade aquática: só pode ser instalada nas faixas de água da Praia."
        # Minas de pressão são cargas de areia/rua: não usam a faixa do
        # canal. A Bomba de Água é a alternativa naval exclusiva.
        if water and not data.get("water_only") and key not in {"barreira", "barreira_reativa"}:
            return False, "Nesta faixa há água. Posicione uma embarcação, uma Bomba de Água ou uma barreira."
        if self.supplies < data["cost"]:
            return False, "Suprimentos insuficientes."
        return True, ""

    def place(self, row: int, col: int) -> None:
        key, display = self.card()
        allowed, reason = self.can_place(key, row, col)
        if not allowed:
            self.announce(reason, 1.7, RED)
            return
        data = DEFENSES[key]
        self.supplies -= data["cost"]
        sprite_index = regional_sprite_index(self.region, key)
        defender = Defender(key, display, row, col, data, sprite_index, region=self.region)
        self.defenders.append(defender)
        # Toda carta retorna após o mesmo intervalo legível: não há exceção
        # por mapa, nível ou função, e a barra conta os 10 segundos completos.
        self.card_cooldowns[self.selected_card] = CARD_RECHARGE_SECONDS
        self.pulse(defender.x, defender.y, self.region_color(), 20)
        self.announce(f"{display} em posição.", 1.2, self.region_color())

    def remove_defender(self, row: int, col: int) -> None:
        """Retira uma defesa por escolha do jogador e devolve parte do custo."""
        if self.difficulty == "easy":
            self.announce("No Fácil, as tropas posicionadas não podem ser removidas.", 1.8, GRAY)
            return
        defender = next((d for d in self.defenders if d.row == row and d.col == col), None)
        if defender is None:
            self.announce("Nenhuma tropa nesta faixa para remover.", 1.4, GRAY)
            return
        self.defenders.remove(defender)
        refund = max(1, math.ceil(float(defender.stats["cost"]) * 0.35))
        self.supplies += refund
        self.pulse(defender.x, defender.y, (188, 206, 214), 12)
        self.announce(f"{defender.display_name} recolhido: +{refund} SUP.", 1.8, TEAL)

    def trigger_lane_bomb(self, row: int) -> bool:
        cart = self.lane_bombs[row]
        if cart.state != "armed":
            return False
        cart.state = "rolling"
        cart.x = float(LANE_BOMB_HOME_X)
        cart.motion.loop("roll")
        self.shake = max(self.shake, 0.16)
        label, color = self.lane_bomb_info(row)
        self.announce(f"{label} — faixa {row + 1} ativada!", 1.8, color)
        self.pulse(cart.x + 24, cell_center(row, 0, self.region)[1], color, 16)
        return True

    def lane_bomb_info(self, row: int) -> tuple[str, tuple[int, int, int]]:
        """Retorna a contenção própria de cada terreno/faixa."""
        if self.region == "city":
            return "BOMBA URBANA", GOLD
        if self.region == "desert":
            return "CARGA DAS DUNAS", (235, 181, 88)
        if row in self.water_rows:
            return "BOIA-BOMBA", (95, 209, 236)
        return "CARGA COSTEIRA", (104, 201, 207)

    def lane_bomb_asset_key(self, row: int) -> str:
        if self.region == "city":
            return "lane_bomb_cart"
        if self.region == "desert":
            return "desert_lane_bomb_cart"
        return "beach_water_bomb" if row in self.water_rows else "beach_land_bomb_cart"

    def update_lane_bombs(self, dt: float) -> None:
        """Move o carrinho-bomba e limpa somente a faixa invadida uma vez."""
        for cart in self.lane_bombs:
            cart.motion.advance(dt, "roll" if cart.state == "rolling" else "armed")
            if cart.state != "rolling":
                continue
            previous_x = cart.x
            cart.x += 720 * dt
            y = cell_center(cart.row, 0, self.region)[1]
            for enemy in self.enemies[:]:
                swept_left = min(previous_x, cart.x) - 52
                swept_right = max(previous_x, cart.x) + 52
                if enemy.row == cart.row and swept_left <= enemy.x <= swept_right:
                    self.take_enemy_damage(enemy, 99999, "explosion")
                    cart.kills += 1
            if cart.x > BOARD.right + 82:
                cart.state = "spent"
                _, explosion_color = self.lane_bomb_info(cart.row)
                self.explosion(BOARD.right - 18, y, explosion_color, 22)

    @staticmethod
    def menu_rect() -> pygame.Rect:
        return pygame.Rect(16, 126, 90, 34)

    @staticmethod
    def pause_rect() -> pygame.Rect:
        return pygame.Rect(112, 126, 92, 34)

    @staticmethod
    def remove_rect() -> pygame.Rect:
        return pygame.Rect(210, 126, 112, 34)

    @staticmethod
    def core_rect() -> pygame.Rect:
        return pygame.Rect(328, 126, 118, 34)

    @staticmethod
    def next_wave_rect() -> pygame.Rect:
        return pygame.Rect(452, 126, 144, 34)

    def apply_core(self, row: int, col: int) -> None:
        target = next((d for d in self.defenders if d.row == row and d.col == col), None)
        if target is None:
            self.announce("Escolha uma tropa já posicionada para usar o Núcleo.", 1.8, RED)
            return
        if target.ascended > 0:
            self.announce("Esta tropa já está ascensionada.", 1.6, GOLD)
            return
        if self.cores <= 0:
            self.use_core = False
            return
        self.cores -= 1
        self.use_core = False
        target.ascended = 18.0
        target.ammo = target.max_ammo
        target.reload_timer = 0.0
        target.reload_total = 0.0
        target.stun = 0
        target.corrosion = 0
        self.announce(f"NÚCLEO DE ASCENSÃO: {target.display_name} no Nível 3!", 2.8, GOLD)
        self.pulse(target.x, target.y, GOLD, 38)

    def start_next_wave(self) -> None:
        if self.wave >= 15:
            return
        self.wave += 1
        self.started_wave = True
        self.wave_banner = 3.0
        self.orders = self.build_wave(self.wave)
        self.spawn_timer = 0.35
        self.intermission = 0.0
        if self.wave % 5 == 0:
            boss_key = REGIONS[self.region]["bosses"][self.wave // 5 - 1]
            self.boss_banner_name = BOSSES[boss_key]["name"]
            self.boss_banner_subtitle = "A ESCOLTA ABRE CAMINHO"
            self.announce(f"Onda {self.wave}: a escolta do chefe está a caminho.", 2.6, RED)
        else:
            self.announce(f"ONDA {self.wave}/15", 2.0, WHITE)

    def build_wave(self, wave: int) -> list[SpawnOrder]:
        pool = list(wave_enemy_pool(self.region, wave))
        # A escala precisa apresentar todos os inimigos que estão cadastrados
        # na região. A versão anterior parava antes dos últimos personagens;
        # agora a ordem continua leve no começo, mas a onda 15 alcança 100%
        # do elenco regional de forma uniforme e verificável.
        orders: list[SpawnOrder] = []
        base_count = 2 + wave + (wave * wave) // 11
        count = max(2, int(round(base_count * float(self.difficulty_data["spawn_count"]))))
        wave_progress = wave / 15
        for index in range(count):
            if index < 3:
                key = pool[min(index, len(pool) - 1)]
            else:
                weighted = pool.copy()
                if wave_progress > 0.35:
                    weighted.extend(pool[-min(3, len(pool)):])
                if wave_progress > 0.70:
                    weighted.extend(pool[-min(5, len(pool)):])
                key = random.choice(weighted)
            wait = (0.92 - min(0.58, wave * 0.038) + random.random() * 0.22) * float(self.difficulty_data["spawn_wait"])
            orders.append(SpawnOrder(wait, key, self.spawn_row_for(key)))
        if wave % 5 == 0:
            boss_key = REGIONS[self.region]["bosses"][wave // 5 - 1]
            # A escolta ainda impede que o chefe seja tratado como um alvo
            # solitário, mas não cria outra horda impossível na mesma entrada.
            escort_count = max(1, int(round((1 + wave // 5) * float(self.difficulty_data["escort_count"]))))
            for _ in range(escort_count):
                escort_key = random.choice(pool[-min(4, len(pool)):])
                orders.insert(random.randrange(len(orders) + 1), SpawnOrder(0.32, escort_key, self.spawn_row_for(escort_key)))
            orders.append(SpawnOrder(1.15, boss_key, self.spawn_row_for(boss_key, boss=True), True))
        return orders

    def spawn_row_for(self, enemy_key: str, boss: bool = False) -> int:
        """Escolhe uma faixa compatível com a natureza do invasor.

        Na Praia, chefes da maré e inimigos aquáticos entram nas duas rotas do
        canal central; ameaças costeiras terrestres usam as duas faixas secas.
        Desse modo, a posição de nascimento respeita tanto a mecânica quanto
        a perspectiva desenhada do mapa.
        """
        if self.region != "beach":
            return random.randrange(ROWS)
        if boss or enemy_key in BEACH_WATER_ENEMIES:
            return random.choice(tuple(self.water_rows))
        land_rows = tuple(row for row in range(ROWS) if row not in self.water_rows)
        return random.choice(land_rows)

    def spawn_enemy(self, order: SpawnOrder) -> None:
        data = BOSSES.get(order.key) or ENEMIES[order.key]
        enemy = Enemy(order.key, order.row, data, self.region, self.wave, difficulty=self.difficulty)
        if order.boss:
            enemy.x = BOARD.right + 110
            enemy.boss_announced = True
            self.shake = 0.38
        self.enemies.append(enemy)
        if order.boss:
            self.boss_banner_name = str(data["name"])
            self.boss_banner_subtitle = "ENTRADA ESPECIAL ATIVADA"
            self.boss_entrance(enemy)

    def region_color(self) -> tuple[int, int, int]:
        return REGIONS[self.region]["accent"]

    def scaled_enemy_damage(self, enemy: Enemy, amount: float) -> float:
        """Aplica o modo ao dano de mordidas, projéteis e habilidades inimigas."""
        key = "boss_damage" if enemy.is_boss else "enemy_damage"
        return float(amount) * float(self.difficulty_data[key])

    def target_in_range(self, defender: Defender, min_distance: float = 0) -> Enemy | None:
        """Retorna um inimigo no alcance, inclusive quem já travou combate.

        Um zumbi pode ultrapassar alguns pixels do centro da tropa antes de
        `blocker_for` congelar seu movimento. A antiga condição exigia que ele
        estivesse estritamente à direita, então armas como a espingarda
        deixavam de atirar justamente no invasor que as mordia. A pequena
        margem atrás da defesa só vale para esse contato corpo a corpo;
        morteiros continuam respeitando a distância mínima.
        """
        maximum = float(defender.stats["range"]) * CELL_W
        lower_bound = defender.x + min_distance if min_distance > 0 else defender.x - CELL_W * 0.55
        choices = [
            enemy
            for enemy in self.enemies
            if enemy.row == defender.row
            and enemy.x >= lower_bound
            and enemy.x - defender.x <= maximum
            and enemy.hp > 0
        ]
        return min(choices, key=lambda e: e.x) if choices else None

    def blocker_for(self, enemy: Enemy) -> Defender | None:
        choices = [
            defender
            for defender in self.defenders
            if defender.row == enemy.row and defender.hp > 0 and defender.x <= enemy.x + 38
        ]
        if not choices:
            return None
        nearest = max(choices, key=lambda d: d.x)
        if enemy.x - nearest.x < 55:
            return nearest
        return None

    def begin_jump(self, enemy: Enemy, blocker: Defender) -> None:
        """Inicia um único salto contínuo sobre a primeira defesa bloqueadora."""
        enemy.jump_used = True
        enemy.jump_state = "vault"
        enemy.jump_duration = 0.52
        enemy.jump_timer = enemy.jump_duration
        enemy.jump_start_x = enemy.x
        enemy.jump_end_x = max(BOARD.left + 8, blocker.x - 60)
        enemy.motion.trigger("jump", enemy.jump_duration)
        self.pulse(enemy.x, enemy.y + 16, GOLD, 9)
        self.announce(f"{enemy.data['name']}: ultrapassou uma única defesa.", 1.35, RED)

    def begin_dig(self, enemy: Enemy, blocker: Defender) -> None:
        """Inicia a escavação mostrada em três etapas, sem teleporte ou dano grátis."""
        enemy.dig_used = True
        enemy.burrowed = True
        enemy.dig_state = "enter"
        enemy.dig_duration = 0.34
        enemy.dig_timer = enemy.dig_duration
        enemy.dig_start_x = enemy.x
        # A saída fica logo depois da primeira defesa encontrada. O Escavador
        # não pode saltar uma fileira inteira nem escolher um alvo distante.
        enemy.dig_end_x = max(BOARD.left + 8, blocker.x - 60)
        enemy.motion.trigger("dig_enter", enemy.dig_duration)
        self.pulse(enemy.x, enemy.y + 17, (194, 160, 77), 12)
        self.announce("Escavador: começou a cavar sob a primeira defesa.", 1.55, (232, 198, 112))

    def update_enemy_motion(self, enemy: Enemy, dt: float) -> bool:
        """Atualiza movimentos especiais que devem ser vistos antes da próxima ação.

        Retorna ``True`` enquanto o inimigo estiver saltando ou escavando.
        Isso impede que o movimento normal transforme a animação num
        teleporte e também impede mordidas durante a travessia.
        """
        if enemy.jump_state:
            if enemy.motion.state != "jump":
                enemy.motion.trigger("jump", enemy.jump_timer)
            enemy.jump_timer = max(0.0, enemy.jump_timer - dt)
            progress = clamp(1.0 - enemy.jump_timer / max(0.01, enemy.jump_duration), 0.0, 1.0)
            enemy.x = lerp(enemy.jump_start_x, enemy.jump_end_x, progress)
            if enemy.jump_timer <= 0:
                enemy.x = enemy.jump_end_x
                enemy.jump_state = ""
                self.pulse(enemy.x, enemy.y + 17, GOLD, 10)
            return True

        if not enemy.dig_state:
            return False

        enemy.dig_timer = max(0.0, enemy.dig_timer - dt)
        if enemy.dig_state == "enter":
            if enemy.motion.state != "dig_enter":
                enemy.motion.trigger("dig_enter", enemy.dig_timer)
            if enemy.dig_timer <= 0:
                enemy.dig_state = "tunnel"
                enemy.dig_duration = 0.58
                enemy.dig_timer = enemy.dig_duration
                enemy.motion.trigger("dig_tunnel", enemy.dig_duration)
            return True

        if enemy.dig_state == "tunnel":
            if enemy.motion.state != "dig_tunnel":
                enemy.motion.trigger("dig_tunnel", enemy.dig_timer)
            progress = clamp(1.0 - enemy.dig_timer / max(0.01, enemy.dig_duration), 0.0, 1.0)
            enemy.x = lerp(enemy.dig_start_x, enemy.dig_end_x, progress)
            if enemy.dig_timer <= 0:
                enemy.x = enemy.dig_end_x
                enemy.dig_state = "emerge"
                enemy.dig_duration = 0.34
                enemy.dig_timer = enemy.dig_duration
                enemy.motion.trigger("dig_emerge", enemy.dig_duration)
                self.pulse(enemy.x, enemy.y + 17, (218, 185, 103), 11)
            return True

        # Etapa final: a silhueta cresce do chão no renderizador e só então
        # o Escavador volta a poder se mover ou atacar.
        if enemy.motion.state != "dig_emerge":
            enemy.motion.trigger("dig_emerge", enemy.dig_timer)
        if enemy.dig_timer <= 0:
            enemy.dig_state = ""
            enemy.burrowed = False
            self.pulse(enemy.x, enemy.y + 17, (226, 192, 112), 8)
        return True

    def take_enemy_damage(self, enemy: Enemy, amount: float, effect: str = "", source: Defender | None = None) -> None:
        if enemy.hp <= 0:
            return
        armor = float(enemy.data.get("armor", 0))
        if "shield" in enemy.tags and effect not in {"flame", "poison", "explosion", "mortar"}:
            armor = max(armor, 0.52)
        if source and source.ascended > 0:
            amount *= 1.55
        enemy.hp -= amount * (1 - armor)
        if effect not in {"status_tick", "acid"}:
            enemy.motion.flash()
            if not enemy.jump_state and not enemy.dig_state:
                enemy.motion.trigger("hit", 0.12)
        if effect == "flame":
            was_burning = enemy.burn > 0
            enemy.burn = max(enemy.burn, 3.3)
            if not was_burning:
                self.pulse(enemy.x, enemy.y - 20, (246, 142, 45), 6)
            self.effects.append(VisualEffect("flame_impact", enemy.x, enemy.y - 24, (246, 142, 45), 0.26, scale=0.72))
        elif effect == "poison":
            was_poisoned = enemy.poisoned > 0
            enemy.poisoned = max(enemy.poisoned, 4.2)
            if not was_poisoned:
                self.pulse(enemy.x, enemy.y - 20, (132, 239, 80), 7)
            self.effects.append(VisualEffect("toxic_impact", enemy.x, enemy.y - 24, (132, 239, 80), 0.34, scale=0.82))
        elif effect == "water":
            # Água não substitui o dano de fogo em força bruta: ela extingue
            # a queima e segura o avanço do alvo por uma janela curta.
            enemy.burn = 0.0
            soak_time = 3.6 if source and source.ascended > 0 else 2.4
            enemy.soaked = max(enemy.soaked, soak_time)
            self.effects.append(VisualEffect("water_impact", enemy.x, enemy.y - 20, (102, 224, 244), 0.30, scale=0.78))
        if effect == "acid":
            enemy.corrosion = max(enemy.corrosion, 2.5)
        self.texts.append(FloatingText(str(int(amount)), enemy.x, enemy.y - 52, GOLD if source and source.ascended else WHITE, 0.55))
        if enemy.hp <= 0:
            self.kill_enemy(enemy)

    def damage_defender(self, defender: Defender, amount: float, effect: str = "") -> None:
        if defender.hp <= 0:
            return
        defender.hp -= amount
        defender.motion.flash()
        defender.motion.trigger("hit", 0.12)
        if effect == "stun":
            defender.stun = max(defender.stun, 2.2)
        elif effect == "acid":
            defender.corrosion = max(defender.corrosion, 4.0)
        elif effect == "acid_brief":
            defender.corrosion = max(defender.corrosion, 1.8)
        if effect in {"acid", "acid_brief"}:
            self.effects.append(VisualEffect("toxic_impact", defender.x, defender.y - 28, (132, 239, 80), 0.28, scale=0.58))
        self.texts.append(FloatingText(str(int(amount)), defender.x, defender.y - 48, RED, 0.6))
        if defender.hp <= 0:
            self.kill_defender(defender)

    def kill_defender(self, defender: Defender) -> None:
        if defender not in self.defenders:
            return
        sprite = self.app.defender_sprite(self, defender)
        width, height = defender_render_scale(defender)
        self.fallen.append(DefeatAnimation(sprite, defender.x, defender.y, width, height, self.cell_is_water(defender.row, defender.col), 0.44))
        self.defenders.remove(defender)
        self.pulse(defender.x, defender.y, RED, 25)
        if defender.stats["role"] == "barrier" and defender.stats["level"] >= 2:
            for enemy in self.enemies[:]:
                if enemy.row == defender.row and abs(enemy.x - defender.x) < CELL_W * 1.35:
                    self.take_enemy_damage(enemy, defender.stats["damage"], "explosion")
            self.explosion(defender.x, defender.y, RED, 28)
        self.announce(f"{defender.display_name} foi perdido.", 1.5, RED)

    def kill_enemy(self, enemy: Enemy) -> None:
        if enemy not in self.enemies:
            return
        sprite = self.app.enemy_sprite(self, enemy)
        width, height = enemy_render_scale(enemy, self.region)
        self.fallen.append(
            DefeatAnimation(
                sprite,
                enemy.x,
                enemy.y,
                width,
                height,
                self.region == "beach" and enemy.row in self.water_rows,
                0.58 if enemy.is_boss else 0.42,
                enemy=True,
            )
        )
        self.enemies.remove(enemy)
        self.dead_history.append((enemy.key, enemy.row, enemy.x))
        if len(self.dead_history) > 12:
            self.dead_history.pop(0)
        color = (130, 230, 145) if not enemy.is_boss else GOLD
        self.explosion(enemy.x, enemy.y, color, 26 if enemy.is_boss else 12)
        if "explode_death" in enemy.tags:
            for defender in self.defenders[:]:
                if defender.row == enemy.row and abs(defender.x - enemy.x) < CELL_W * 1.15:
                    self.damage_defender(defender, self.scaled_enemy_damage(enemy, 52 + self.wave * 2), "acid")
            self.explosion(enemy.x, enemy.y, (114, 212, 99), 25)
        if enemy.is_boss:
            self.cores = min(3, self.cores + 1)
            self.supplies += 60
            self.boss_seen.add(self.wave)
            self.announce("Chefe neutralizado: +1 Núcleo de Ascensão e +60 suprimentos.", 3.4, GOLD)
            self.pulse(WIDTH / 2, HEIGHT / 2, GOLD, 75)
        else:
            self.supplies += 1 if self.wave < 8 else 2

    def pulse(self, x: float, y: float, color: tuple[int, int, int], amount: int) -> None:
        # Mantido como gancho de compatibilidade. A versão antiga espalhava
        # círculos; a Beta 4 reserva o desenho para sprites de VFX completos.
        return

    def explosion(
        self,
        x: float,
        y: float,
        color: tuple[int, int, int],
        amount: int,
        *,
        scale: float | None = None,
    ) -> None:
        if scale is None:
            scale = clamp(0.62 + amount / 44.0, 0.72, 1.58)
        self.effects.append(VisualEffect("explosion", x, y - 18, color, 0.46, scale=scale))
        self.shake = max(self.shake, 0.16)

    def fire_defender(self, defender: Defender, target: Enemy) -> None:
        role = defender.stats["role"]
        level = defender.stats["level"]
        ascending = defender.ascended > 0
        if role in {"radio", "promoter", "barrier", "mine"}:
            return
        if defender.max_ammo > 0:
            defender.ammo -= 1
        defender.attack_timer = float(defender.stats["cooldown"]) * (0.68 if ascending else 1.0)
        defender.motion.trigger(
            "attack",
            0.48 if role == "mortar" else (0.36 if role == "grenade" else 0.24),
        )
        if role == "sniper" and level == 1 and not ascending and random.random() < 0.28:
            self.texts.append(FloatingText("ERROU", target.x, target.y - 42, GRAY, 0.7))
            self.projectiles.append(Projectile(defender.x + 15, defender.y - 22, None, target.x, target.y - 18, 0, "tracer", defender, travel=0.22))
            return
        damage = float(defender.stats["damage"])
        kind = "bullet"
        radius = 0.0
        effect = ""
        if role == "rifle":
            kind = "rifle"
            if ascending:
                kind, radius = "fuzileiro", CELL_W * 0.72
                damage *= 1.25
        elif role == "shotgun":
            kind, radius = "shotgun", CELL_W * (0.45 if ascending else 0.25)
            distance = max(1, (target.x - defender.x) / CELL_W)
            damage *= 1.45 if distance < 1.2 else 0.9
            if ascending:
                damage *= 1.4
        elif role == "sniper":
            kind = "sniper"
            if ascending:
                damage *= 2.55
        elif role in {"grenade", "mortar"}:
            kind = "mortar" if role == "mortar" else "grenade"
            radius = CELL_W * (1.05 if ascending else 0.78)
            effect = "mortar"
            if ascending and role == "mortar":
                for offset in (-1, 1):
                    clone = self.closest_enemy_at(target.row + offset, target.x)
                    if clone:
                        self.projectiles.append(
                            Projectile(
                                defender.x,
                                defender.y - 24,
                                clone,
                                clone.x,
                                clone.y - 15,
                                damage * 0.72,
                                kind,
                                defender,
                                radius,
                                True,
                                0.45,
                                elapsed=-0.30,
                                effect=effect,
                            )
                        )
            if ascending and role == "grenade":
                kind, radius, damage = "bazooka", BOARD.width, damage * 1.45
        elif role == "flame":
            kind, radius, effect = "flame", CELL_W * 0.55, "flame"
            damage *= 0.70
        elif role == "poison":
            kind = "poison"
            radius = CELL_W * (0.48 if level == 1 else 0.62)
            effect = "poison"
            damage *= 0.62
        elif role == "waterjet":
            kind = "waterjet"
            radius = CELL_W * (0.38 if level == 1 else 0.50)
            effect = "water"
            damage *= 0.62
        elif role == "boat":
            kind = "boat"
        elif role == "sub":
            kind, radius = "torpedo", CELL_W * 0.42
        travel = 0.38 if kind in {"flame", "poison", "waterjet"} else (0.24 if kind == "rifle" else 0.42)
        projectile = Projectile(
            defender.x + 16,
            defender.y - 22,
            target,
            target.x,
            target.y - 16,
            damage,
            kind,
            defender,
            radius,
            True,
            travel,
            effect=effect,
        )
        if kind == "mortar":
            projectile.elapsed = -0.34
        elif kind in {"grenade", "bazooka"}:
            projectile.elapsed = -0.12
        self.projectiles.append(projectile)

    def closest_enemy_at(self, row: int, x: float) -> Enemy | None:
        candidates = [enemy for enemy in self.enemies if enemy.row == row and enemy.hp > 0]
        return min(candidates, key=lambda e: abs(e.x - x)) if candidates else None

    def promote_defender(self, instructor: Defender) -> bool:
        """Converte uma tropa N1 real em sua carta N2 correspondente.

        O alcance considera também as faixas vizinhas para não punir a posição
        visual do Sargento, mas o alvo mais perto ainda é previsível para quem
        quer escolher qual carta vai subir primeiro.
        """
        radius = float(instructor.stats["range"]) * CELL_W
        candidates = [
            defender
            for defender in self.defenders
            if defender is not instructor
            and defender.key in PROMOTIONS
            and int(defender.stats["level"]) == 1
            and defender.ascended <= 0
            and abs(defender.x - instructor.x) <= radius
            and abs(defender.row - instructor.row) <= 1
        ]
        if not candidates:
            # Não reinicia o minuto inteiro se ainda não houver uma tropa N1
            # válida por perto: o jogador ganha uma pequena janela para criar
            # ou reposicionar a candidata.
            instructor.utility_timer = 8.0
            return False

        target = min(candidates, key=lambda defender: (abs(defender.x - instructor.x), abs(defender.row - instructor.row)))
        target_key = PROMOTIONS[target.key]
        upgraded = DEFENSES[target_key]
        old_hp_ratio = target.hp / max(1.0, target.max_hp)
        old_ammo_ratio = target.ammo / max(1, target.max_ammo) if target.max_ammo else 1.0
        target.key = target_key
        target.stats = upgraded
        target.sprite_index = regional_sprite_index(self.region, target_key)
        target.hp = max(1.0, float(upgraded["hp"]) * max(0.55, old_hp_ratio))
        target.ammo = int(round(int(upgraded["ammo"]) * old_ammo_ratio)) if int(upgraded["ammo"]) else 0
        target.reload_timer = 0.0
        target.reload_total = 0.0
        target.attack_timer = 0.0
        target.utility_timer = 0.0
        target.stun = 0.0
        target.corrosion = 0.0
        target.display_name = self.display_name_for(target_key)
        instructor.utility_timer = float(instructor.stats["cooldown"])
        instructor.motion.trigger("support", 0.46)
        target.motion.trigger("promote", 0.60)
        self.announce(f"PROMOÇÃO CONCLUÍDA: {target.display_name} agora é N2!", 2.5, GOLD)
        self.pulse(target.x, target.y - 12, GOLD, 28)
        return True

    def display_name_for(self, key: str) -> str:
        """Mantém a nomenclatura regional quando uma carta muda de nível."""
        for roster_key, display in REGION_ROSTERS[self.region]:
            if roster_key == key:
                return display
        return str(DEFENSES[key]["base"])

    def utility_defender(self, defender: Defender, dt: float) -> None:
        role = defender.stats["role"]
        if role == "radio" and defender.utility_timer <= 0:
            gain = 14 if defender.stats["level"] == 1 else 28
            if defender.ascended:
                gain = 52
            self.supplies += gain
            defender.utility_timer = float(defender.stats["cooldown"]) * (0.48 if defender.ascended else 1.0)
            defender.motion.trigger("support", 0.48)
            self.texts.append(FloatingText(f"+{gain} SUP", defender.x, defender.y - 55, GOLD, 1.0))
            self.pulse(defender.x, defender.y - 18, GOLD, 8)
        elif role == "promoter" and defender.utility_timer <= 0:
            self.promote_defender(defender)

    def update_self_reload(self, defender: Defender, dt: float) -> bool:
        """Executa a recarga da própria arma e bloqueia o tiro nesse estado."""
        if defender.max_ammo <= 0 or defender.ammo > 0:
            defender.reload_timer = 0.0
            defender.reload_total = 0.0
            return False
        # A última rajada continua visualmente completa antes de a arma baixar.
        if defender.reload_timer <= 0 and defender.motion.state == "attack" and defender.motion.event_left > 0:
            return True
        if defender.reload_timer <= 0:
            defender.reload_total = weapon_reload_seconds(defender.stats, defender.ascended > 0)
            defender.reload_timer = defender.reload_total
            defender.motion.trigger("reload", defender.reload_total)
        defender.reload_timer = max(0.0, defender.reload_timer - dt)
        if defender.reload_timer <= 0:
            defender.ammo = defender.max_ammo
            defender.attack_timer = max(defender.attack_timer, 0.16)
            defender.motion.loop("idle")
            defender.reload_total = 0.0
            return True
        if defender.motion.state != "reload":
            defender.motion.trigger("reload", defender.reload_timer)
        return True

    def update_defenders(self, dt: float) -> None:
        for defender in self.defenders[:]:
            role = defender.stats["role"]
            defender.motion.advance(dt, "armed" if role == "mine" else "idle")
            defender.attack_timer -= dt
            defender.utility_timer -= dt
            defender.stun = max(0.0, defender.stun - dt)
            defender.corrosion = max(0.0, defender.corrosion - dt)
            defender.ascended = max(0.0, defender.ascended - dt)
            defender.pulse += dt
            if defender.corrosion > 0 and random.random() < dt * 1.6:
                self.damage_defender(defender, 1.6)
            if role == "mine":
                target = next((enemy for enemy in self.enemies if enemy.row == defender.row and abs(enemy.x - defender.x) < 49), None)
                if target:
                    is_safe = defender.stats["level"] >= 2
                    if is_safe or random.random() < 0.72:
                        if defender.ascended:
                            for enemy in self.enemies[:]:
                                if enemy.row == defender.row:
                                    self.take_enemy_damage(enemy, 9999, "explosion", defender)
                            self.announce("Mina ascensionada: linha inteira limpa!", 1.7, GOLD)
                        else:
                            radius = CELL_W * (0.82 if defender.key == "bomba_agua" else 0.35)
                            for enemy in self.enemies[:]:
                                if enemy.row == defender.row and abs(enemy.x - defender.x) < radius:
                                    self.take_enemy_damage(enemy, defender.stats["damage"], "explosion", defender)
                        self.effects.append(VisualEffect("explosion", defender.x, defender.y - 13, GOLD, 0.32, scale=0.95))
                        self.explosion(defender.x, defender.y, GOLD, 18)
                    else:
                        self.announce("A mina falhou!", 1.2, RED)
                    self.defenders.remove(defender)
                continue
            if defender.stun > 0:
                defender.motion.trigger("stunned", defender.stun)
                continue
            if self.update_self_reload(defender, dt):
                continue
            self.utility_defender(defender, dt)
            minimum = CELL_W * 1.05 if role == "mortar" else 0
            target = self.target_in_range(defender, minimum)
            if target and defender.attack_timer <= 0 and defender.has_ammo():
                self.fire_defender(defender, target)

    @staticmethod
    def is_military_defender(defender: Defender) -> bool:
        """Tropas humanas recebem os efeitos globais de entrada dos chefes.

        Minas e barreiras são equipamentos fixos; elas continuam como opção de
        contenção quando uma chegada especial fecha temporariamente os tiros.
        """
        return defender.stats["role"] not in {"barrier", "mine"}

    def boss_entrance(self, enemy: Enemy) -> None:
        """Executa uma única ação de entrada. Ela nunca é reutilizada no ciclo.

        Cada chefe ganha um impacto memorável ao aparecer, mas a ação recorrente
        que vem depois é menor, localizada e possui um intervalo legível.
        """
        boss_type = enemy.data.get("type", "")
        enemy.motion.trigger("skill", 0.72)
        self.shake = max(self.shake, 0.42)
        entrance_visuals = {
            "bruto_demolidor": ("ground_slam", (230, 91, 61)),
            "comandante": ("command_aura", (232, 77, 62)),
            "alfa": ("toxic_wave", (132, 239, 80)),
            "mutante": ("ground_slam", (225, 152, 70)),
            "necromante": ("arcane_cast", (197, 128, 238)),
            "colosso": ("ground_slam", (227, 163, 81)),
            "tide": ("tidal_surge", (95, 195, 239)),
            "hunter": ("tidal_surge", (95, 195, 239)),
            "leviathan": ("tidal_surge", (95, 195, 239)),
        }
        visual_kind, visual_color = entrance_visuals.get(str(boss_type), ("ground_slam", RED))
        self.effects.append(VisualEffect(visual_kind, enemy.x, enemy.y, visual_color, 0.92, scale=1.45))
        if boss_type == "bruto_demolidor":
            for defender in self.defenders:
                if self.is_military_defender(defender):
                    defender.stun = max(defender.stun, 3.0)
            enemy.skill_timer = 18.0
            self.announce("BRUTO DEMOLIDOR: tropas militares paralisadas por 3 s!", 2.8, RED)
        elif boss_type == "comandante":
            for other in self.enemies:
                if other is not enemy and abs(other.x - enemy.x) < CELL_W * 4.2:
                    other.rage = max(other.rage, 2.4)
            enemy.skill_timer = 14.0
            self.announce("Comandante dos Mortos: a escolta recebeu fúria!", 2.4, RED)
        elif boss_type == "alfa":
            self.global_toxic = 1.2
            for defender in self.defenders:
                defender.corrosion = max(defender.corrosion, 1.0)
            enemy.skill_timer = 14.0
            self.announce("Cuspidor Alfa: névoa ácida global por um instante!", 2.4, (150, 232, 112))
        elif boss_type == "mutante":
            for defender in self.defenders[:]:
                if abs(defender.row - enemy.row) <= 1 and abs(defender.x - enemy.x) < CELL_W * 2.25:
                    self.damage_defender(defender, self.scaled_enemy_damage(enemy, 8))
                    defender.stun = max(defender.stun, 1.15)
            enemy.skill_timer = 14.0
            self.announce("Mutante das Ruínas: o abalo atingiu apenas a vanguarda próxima.", 2.2, RED)
        elif boss_type == "necromante":
            self.enemies.append(Enemy("necromante_minion", enemy.row, ENEMIES["necromante_minion"], self.region, self.wave, difficulty=self.difficulty, x=enemy.x + 48))
            enemy.skill_timer = 15.0
            self.announce("Necromante: uma múmia foi invocada na chegada.", 2.3, (197, 128, 238))
        elif boss_type == "colosso":
            for defender in self.defenders:
                if self.is_military_defender(defender):
                    defender.stun = max(defender.stun, 1.2)
            enemy.skill_timer = 18.0
            self.announce("Colosso Mutante: tremor inicial interrompeu os tiros por 1,2 s.", 2.4, RED)
        elif boss_type == "tide":
            for defender in self.defenders[:]:
                if defender.row == enemy.row and defender.stats.get("water_only"):
                    self.damage_defender(defender, self.scaled_enemy_damage(enemy, 8))
                    defender.stun = max(defender.stun, 0.9)
            enemy.skill_timer = 14.0
            self.announce("Bruto da Maré: a primeira onda abalou o canal.", 2.1, (95, 195, 239))
        elif boss_type == "hunter":
            enemy.x = max(BOARD.left + CELL_W * 4.8, enemy.x - CELL_W * 0.7)
            enemy.skill_timer = 13.0
            self.announce("Caçador Abissal: mergulhou e surgiu mais perto no canal.", 2.1, (95, 195, 239))
        elif boss_type == "leviathan":
            for defender in self.defenders[:]:
                if defender.row == enemy.row and defender.stats.get("water_only"):
                    self.damage_defender(defender, self.scaled_enemy_damage(enemy, 14))
                    defender.stun = max(defender.stun, 1.2)
            enemy.skill_timer = 18.0
            self.announce("LEVIATÃ: uma onda de entrada atingiu a faixa de água.", 2.4, (95, 195, 239))
        else:
            enemy.skill_timer = 12.0

    def boss_skill(self, enemy: Enemy) -> None:
        """Habilidade recorrente, sempre mais justa que a entrada do chefe."""
        boss_type = enemy.data.get("type", "")
        cooldowns = {
            "bruto_demolidor": 18.0,
            "comandante": 14.0,
            "alfa": 14.0,
            "mutante": 14.0,
            "necromante": 15.0,
            "colosso": 18.0,
            "tide": 14.0,
            "hunter": 13.0,
            "leviathan": 18.0,
        }
        enemy.skill_timer = cooldowns.get(boss_type, 12.0) * float(self.difficulty_data["skill_cooldown"])
        enemy.motion.trigger("skill", 0.46)
        self.shake = max(self.shake, 0.24)
        skill_visuals = {
            "bruto_demolidor": ("ground_slam", (230, 91, 61)),
            "comandante": ("command_aura", (232, 77, 62)),
            "alfa": ("toxic_wave", (132, 239, 80)),
            "mutante": ("ground_slam", (225, 152, 70)),
            "necromante": ("arcane_cast", (197, 128, 238)),
            "colosso": ("ground_slam", (227, 163, 81)),
            "tide": ("tidal_surge", (95, 195, 239)),
            "hunter": ("tidal_surge", (95, 195, 239)),
            "leviathan": ("tidal_surge", (95, 195, 239)),
        }
        visual_kind, visual_color = skill_visuals.get(str(boss_type), ("ground_slam", RED))
        self.effects.append(VisualEffect(visual_kind, enemy.x, enemy.y, visual_color, 0.68, scale=1.0))

        if boss_type == "bruto_demolidor":
            # Regra central do primeiro chefe: sem stun global repetido. O
            # martelo fecha somente a faixa na qual o chefe está por 1,2 s.
            targets = [d for d in self.defenders if d.row == enemy.row and self.is_military_defender(d)]
            for defender in targets:
                defender.stun = max(defender.stun, 1.2)
                self.pulse(defender.x, defender.y - 22, RED, 7)
            self.announce(f"Martelo do Bruto: faixa {enemy.row + 1} interrompida por 1,2 s.", 2.0, RED)
        elif boss_type == "comandante":
            escorts = [
                other for other in self.enemies
                if other is not enemy and abs(other.row - enemy.row) <= 1 and abs(other.x - enemy.x) < CELL_W * 2.8
            ]
            for other in escorts:
                other.rage = max(other.rage, 2.2)
            targets = [d for d in self.defenders if d.row == enemy.row and d.x < enemy.x and enemy.x - d.x < CELL_W * 4.5]
            if targets:
                victim = max(targets, key=lambda defender: defender.x)
                for vertical in (-11, 9):
                    damage = self.scaled_enemy_damage(enemy, 10 + self.wave)
                    self.projectiles.append(Projectile(enemy.x - 14, enemy.y + vertical - 24, victim, victim.x, victim.y - 24, damage, "enemy_bullet", enemy, 0, False, 0.32))
            self.announce("Comandante: escolta próxima acelerada e rajada dupla disparada.", 1.9, RED)
        elif boss_type == "alfa":
            targets = [d for d in self.defenders if d.row == enemy.row and d.x < enemy.x and enemy.x - d.x < CELL_W * 4.0]
            for victim in sorted(targets, key=lambda defender: defender.x, reverse=True)[:1]:
                damage = self.scaled_enemy_damage(enemy, 10 + self.wave)
                self.projectiles.append(Projectile(enemy.x - 12, enemy.y - 27, victim, victim.x, victim.y - 18, damage, "acid", enemy, 0, False, 0.45, effect="acid_brief"))
            self.announce(f"Cuspidor Alfa: saliva corrosiva na faixa {enemy.row + 1}.", 1.8, (150, 232, 112))
        elif boss_type == "mutante":
            for defender in self.defenders[:]:
                if defender.row == enemy.row and abs(defender.x - enemy.x) < CELL_W * 2.15:
                    self.damage_defender(defender, self.scaled_enemy_damage(enemy, 12))
                    defender.stun = max(defender.stun, 1.0)
            self.announce(f"Mutante: punho de ruína na faixa {enemy.row + 1}.", 1.8, RED)
        elif boss_type == "necromante":
            self.enemies.append(Enemy("necromante_minion", enemy.row, ENEMIES["necromante_minion"], self.region, self.wave, difficulty=self.difficulty, x=enemy.x + 42))
            for other in self.enemies:
                if other is not enemy and abs(other.x - enemy.x) < CELL_W * 1.65:
                    other.hp = min(other.max_hp, other.hp + 28)
            self.announce("Necromante: novas múmias e cura localizada da escolta.", 2.0, (197, 128, 238))
        elif boss_type == "colosso":
            targets = [d for d in self.defenders if d.x < enemy.x and enemy.x - d.x < CELL_W * 4.0]
            if targets:
                victim = max(targets, key=lambda defender: defender.x)
                damage = self.scaled_enemy_damage(enemy, 18)
                self.projectiles.append(Projectile(enemy.x - 12, enemy.y - 34, victim, victim.x, victim.y - 24, damage, "mortar", enemy, 0, False, 0.52))
            self.announce("Colosso: rocha arremessada contra uma faixa-alvo.", 1.9, RED)
        elif boss_type == "tide":
            targets = [d for d in self.defenders if d.row == enemy.row and d.stats.get("water_only") and d.x < enemy.x]
            if targets:
                victim = max(targets, key=lambda defender: defender.x)
                self.damage_defender(victim, self.scaled_enemy_damage(enemy, 12))
                victim.stun = max(victim.stun, 0.8)
            self.announce("Bruto da Maré: golpe concentrado no canal.", 1.8, (95, 195, 239))
        elif boss_type == "hunter":
            enemy.x = max(BOARD.left + CELL_W * 3.4, enemy.x - CELL_W * 0.85)
            targets = [d for d in self.defenders if d.row == enemy.row and d.stats.get("water_only") and d.x < enemy.x]
            if targets:
                victim = max(targets, key=lambda defender: defender.x)
                self.damage_defender(victim, self.scaled_enemy_damage(enemy, 10))
                victim.stun = max(victim.stun, 0.7)
            self.announce("Caçador Abissal: mergulho ofensivo no canal.", 1.8, (95, 195, 239))
        elif boss_type == "leviathan":
            targets = [d for d in self.defenders if d.row == enemy.row and d.stats.get("water_only") and d.x < enemy.x]
            if targets:
                victim = max(targets, key=lambda defender: defender.x)
                damage = self.scaled_enemy_damage(enemy, 24)
                self.projectiles.append(Projectile(enemy.x - 22, enemy.y - 25, victim, victim.x, victim.y - 12, damage, "torpedo", enemy, 0, False, 0.42))
            self.announce("LEVIATÃ: jato de pressão concentrado na faixa de água.", 2.0, (95, 195, 239))

    def enemy_special(self, enemy: Enemy) -> None:
        enemy.motion.trigger("skill", 0.34 if not enemy.is_boss else 0.46)
        if enemy.is_boss:
            self.boss_skill(enemy)
            return
        # No Difícil os poderes inimigos retornam um pouco antes. No Fácil o
        # multiplicador é 1, portanto o equilíbrio aprovado não se altera.
        enemy.skill_timer = random.uniform(3.4, 5.8) * float(self.difficulty_data["skill_cooldown"])
        if "gun" in enemy.tags:
            targets = [d for d in self.defenders if d.row == enemy.row and d.x < enemy.x and enemy.x - d.x < CELL_W * 4]
            if targets:
                victim = max(targets, key=lambda d: d.x)
                damage = self.scaled_enemy_damage(enemy, 20 + self.wave * 1.3)
                self.projectiles.append(Projectile(enemy.x - 12, enemy.y - 25, victim, victim.x, victim.y - 20, damage, "enemy_bullet", enemy, 0, False, 0.30))
        if "acid" in enemy.tags:
            targets = [d for d in self.defenders if d.row == enemy.row and d.x < enemy.x and enemy.x - d.x < CELL_W * 3.2]
            if targets:
                victim = max(targets, key=lambda d: d.x)
                damage = self.scaled_enemy_damage(enemy, 16 + self.wave)
                self.projectiles.append(Projectile(enemy.x - 12, enemy.y - 22, victim, victim.x, victim.y - 18, damage, "acid", enemy, CELL_W * 0.34, False, 0.48, effect="acid"))
        if "scream" in enemy.tags:
            self.effects.append(VisualEffect("command_aura", enemy.x, enemy.y, RED, 0.58, scale=0.72))
            for other in self.enemies:
                if other.row == enemy.row and abs(other.x - enemy.x) < CELL_W * 2.6:
                    other.rage = max(other.rage, 3.5)
            if random.random() < 0.36:
                self.enemies.append(Enemy("caminhante" if self.region != "beach" else "boia", enemy.row, ENEMIES["caminhante" if self.region != "beach" else "boia"], self.region, self.wave, difficulty=self.difficulty, x=BOARD.right + 20))
            self.announce("Grito: a horda ganhou velocidade.", 1.2, RED)
        if "heal" in enemy.tags:
            self.effects.append(VisualEffect("arcane_cast", enemy.x, enemy.y, (154, 239, 134), 0.64, scale=0.76))
            nearby = [other for other in self.enemies if other is not enemy and abs(other.x - enemy.x) < CELL_W * 1.8]
            for other in nearby:
                other.hp = min(other.max_hp, other.hp + 42)
            if self.dead_history and not enemy.revived and random.random() < 0.4:
                key, row, x = self.dead_history[-1]
                if key in ENEMIES:
                    revived = Enemy(key, row, ENEMIES[key], self.region, self.wave, difficulty=self.difficulty, x=x + 42)
                    revived.hp = revived.max_hp * 0.40
                    self.enemies.append(revived)
                    enemy.revived = True
        if "parasite" in enemy.tags:
            self.effects.append(VisualEffect("ground_slam", enemy.x, enemy.y, (218, 106, 76), 0.54, scale=0.70))
            for defender in self.defenders:
                if defender.row == enemy.row and defender.x < enemy.x and enemy.x - defender.x < CELL_W * 2.1:
                    defender.stun = max(defender.stun, 2.6)
            self.announce("Parasita: tiro das tropas foi desabilitado.", 1.4, RED)
        if "stomp" in enemy.tags:
            self.effects.append(VisualEffect("ground_slam", enemy.x, enemy.y, (223, 132, 73), 0.60, scale=0.84))
            for defender in self.defenders:
                if defender.row == enemy.row and abs(defender.x - enemy.x) < CELL_W * 1.8:
                    self.damage_defender(defender, self.scaled_enemy_damage(enemy, 24), "stun")
        if "steal" in enemy.tags:
            self.effects.append(VisualEffect("arcane_cast", enemy.x, enemy.y, GOLD, 0.58, scale=0.68))
            stolen = min(18, self.supplies)
            self.supplies -= stolen
            enemy.stolen += stolen
            self.announce("Ladrão de Suprimentos roubou carga — clique nele!", 2.0, GOLD)

    def update_enemies(self, dt: float) -> None:
        for enemy in self.enemies[:]:
            enemy.age += dt
            enemy.motion.advance(dt, "walk")
            enemy.attack_timer -= dt
            enemy.skill_timer -= dt
            enemy.stun = max(0.0, enemy.stun - dt)
            enemy.burn = max(0.0, enemy.burn - dt)
            enemy.poisoned = max(0.0, enemy.poisoned - dt)
            enemy.soaked = max(0.0, enemy.soaked - dt)
            enemy.corrosion = max(0.0, enemy.corrosion - dt)
            enemy.rage = max(0.0, enemy.rage - dt)
            enemy.step_timer -= dt
            enemy.dot_timer -= dt
            if enemy.attack_windup > 0:
                enemy.attack_windup = max(0.0, enemy.attack_windup - dt)
                if enemy.attack_windup <= 0:
                    victim = enemy.attack_target
                    enemy.attack_target = None
                    if victim in self.defenders and victim.hp > 0 and abs(victim.row - enemy.row) == 0:
                        # O dano coincide com o contato da mordida/martelo, não
                        # com o primeiro quadro da preparação do ataque.
                        self.damage_defender(victim, enemy.attack_damage)
                    enemy.attack_damage = 0.0
            # Queimadura e Envenenado causam pulsos legíveis de dano. O dano
            # periódico não renova o próprio estado, portanto ambos acabam no
            # tempo previsto em vez de permanecerem ativos para sempre.
            if enemy.dot_timer <= 0 and (enemy.burn > 0 or enemy.poisoned > 0):
                dot_damage = (3.2 if enemy.burn > 0 else 0.0) + (2.25 if enemy.poisoned > 0 else 0.0)
                self.take_enemy_damage(enemy, dot_damage, "status_tick")
                enemy.dot_timer = 0.5
                if enemy not in self.enemies:
                    continue
            if enemy.corrosion > 0:
                self.take_enemy_damage(enemy, 2.0 * dt, "acid")
                if enemy not in self.enemies:
                    continue
            if enemy.skill_timer <= 0:
                self.enemy_special(enemy)
                if enemy not in self.enemies:
                    continue
            if self.update_enemy_motion(enemy, dt):
                continue
            if enemy.stun > 0:
                enemy.motion.trigger("stunned", enemy.stun)
                continue
            speed = float(enemy.data["speed"]) * (1.55 if enemy.rage > 0 else 1.0)
            if "dash" in enemy.tags and enemy.age < 1.7:
                speed *= 1.95
            if enemy.soaked > 0:
                speed *= 0.68
            if enemy.poisoned > 0:
                speed *= 0.88
            blocker = self.blocker_for(enemy)
            if blocker:
                if "dig" in enemy.tags and not enemy.dig_used:
                    self.begin_dig(enemy, blocker)
                    continue
                if "jump" in enemy.tags and not enemy.jump_used:
                    self.begin_jump(enemy, blocker)
                    continue
                if enemy.attack_timer <= 0 and enemy.attack_windup <= 0:
                    scale = boss_damage_scale(self.wave) if enemy.is_boss else enemy_damage_scale(self.wave)
                    damage = self.scaled_enemy_damage(enemy, float(enemy.data["damage"]) * scale)
                    attack_duration = 0.44 if enemy.is_boss else 0.34
                    enemy.attack_target = blocker
                    enemy.attack_damage = damage
                    enemy.attack_windup = attack_duration * 0.56
                    enemy.motion.trigger("attack", attack_duration)
                    enemy.attack_timer = float(enemy.data["attack"])
                elif enemy.motion.event_left <= 0:
                    enemy.motion.trigger("brace", min(0.28, max(0.08, enemy.attack_timer)))
                continue
            enemy.x -= speed * dt
            if enemy.x <= BOARD.left + 8:
                cart = self.lane_bombs[enemy.row]
                if cart.state == "armed":
                    self.trigger_lane_bomb(enemy.row)
                if cart.state == "rolling":
                    # O zumbi é segurado por um instante na saída, dando ao
                    # carrinho tempo para alcançá-lo visualmente na faixa.
                    enemy.x = max(enemy.x, BOARD.left - 2)
                    continue
            if enemy.x < BOARD.left - 42:
                self.lost = True
                self.finished = True
                self.announce("BASE INVADIDA", 10, RED)

    def update_projectiles(self, dt: float) -> None:
        for projectile in self.projectiles[:]:
            projectile.elapsed += dt
            if projectile.elapsed < 0:
                continue
            t = clamp(projectile.elapsed / projectile.travel, 0, 1)
            if t < 1:
                continue
            self.projectiles.remove(projectile)
            if projectile.friendly:
                target = projectile.target
                if isinstance(target, Enemy) and target in self.enemies:
                    self.take_enemy_damage(target, projectile.damage, projectile.effect, projectile.owner if isinstance(projectile.owner, Defender) else None)
                    if projectile.radius > 0:
                        for other in self.enemies[:]:
                            if other is target:
                                continue
                            if abs(other.y - target.y) < CELL_H * 0.75 and abs(other.x - target.x) < projectile.radius:
                                self.take_enemy_damage(other, projectile.damage * 0.72, projectile.effect, projectile.owner if isinstance(projectile.owner, Defender) else None)
                    if projectile.kind in {"grenade", "mortar", "bazooka", "torpedo"}:
                        scale = 1.35 if projectile.kind == "bazooka" else (1.12 if projectile.kind == "mortar" else 0.96)
                        self.explosion(projectile.target_x, projectile.target_y, GOLD, 16, scale=scale)
            else:
                target = projectile.target
                if isinstance(target, Defender) and target in self.defenders:
                    self.damage_defender(target, projectile.damage, projectile.effect)
                    if projectile.radius:
                        for other in self.defenders[:]:
                            if other is target:
                                continue
                            if abs(other.y - target.y) < CELL_H * 0.75 and abs(other.x - target.x) < projectile.radius:
                                self.damage_defender(other, projectile.damage * 0.5, projectile.effect)
                    if projectile.kind == "acid":
                        self.effects.append(VisualEffect("toxic_impact", projectile.target_x, projectile.target_y, (132, 239, 80), 0.30, scale=0.78))
                    elif projectile.kind == "torpedo":
                        self.effects.append(VisualEffect("water_impact", projectile.target_x, projectile.target_y, (102, 224, 244), 0.32, scale=0.92))
                    else:
                        # Tiros inimigos recebem um impacto curto de munição;
                        # não fabricam uma explosão de granada a cada acerto.
                        self.effects.append(VisualEffect("ballistic_impact", projectile.target_x, projectile.target_y, (241, 198, 122), 0.18, scale=0.30))

    def update_particles(self, dt: float) -> None:
        for particle in self.particles[:]:
            particle.ttl -= dt
            particle.x += particle.vx * dt
            particle.y += particle.vy * dt
            particle.vy += particle.gravity * dt
            if particle.ttl <= 0:
                self.particles.remove(particle)
        for text in self.texts[:]:
            text.ttl -= dt
            text.y -= 20 * dt
            if text.ttl <= 0:
                self.texts.remove(text)
        for effect in self.effects[:]:
            effect.elapsed += dt
            if effect.elapsed >= effect.duration:
                self.effects.remove(effect)
        for fallen in self.fallen[:]:
            fallen.elapsed += dt
            if fallen.elapsed >= fallen.duration:
                self.fallen.remove(fallen)

    def update_wave(self, dt: float) -> None:
        if self.finished:
            return
        if not self.started_wave:
            self.intermission -= dt
            if self.intermission <= 0:
                self.start_next_wave()
            return
        if self.orders:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                # O alerta grande pertence à chegada do chefe, e não ao início
                # genérico da onda. Enquanto ele está visível, a ordem fica
                # segurada; terminado o aviso, o chefe entra de fato.
                next_order = self.orders[0]
                if next_order.boss:
                    if not self.boss_alert_pending:
                        boss_data = BOSSES[next_order.key]
                        self.boss_alert_pending = True
                        self.boss_warning = 3.0
                        self.boss_banner_name = str(boss_data["name"])
                        self.boss_banner_subtitle = "CHEFE E ESCOLTA EM APROXIMAÇÃO"
                        self.announce(f"ALERTA: {self.boss_banner_name} chegando!", 3.0, RED)
                        return
                    if self.boss_warning > 0:
                        return
                    self.boss_alert_pending = False
                order = self.orders.pop(0)
                self.spawn_enemy(order)
                self.spawn_timer = order.wait
        elif not self.enemies:
            if self.wave >= 15:
                self.finished = True
                self.victory = True
                self.announce("REGIÃO PROTEGIDA!", 10, GOLD)
                return
            self.started_wave = False
            self.intermission = 5.0
            self.supplies += 10 + self.wave
            self.announce(f"Onda {self.wave} concluída. Prepare a próxima.", 2.4, GOLD)

    def update(self, dt: float) -> None:
        # Pausa congela relógios, recargas, projéteis, inimigos e contagens. A
        # interface continua recebendo clique para MENU ou para retomar.
        if self.paused:
            return
        self.ambient_phase += dt
        self.shake = max(0, self.shake - dt)
        self.global_toxic = max(0, self.global_toxic - dt)
        self.boss_warning = max(0, self.boss_warning - dt)
        self.message_timer = max(0, self.message_timer - dt)
        for index, value in enumerate(self.card_cooldowns):
            self.card_cooldowns[index] = max(0, value - dt)
        self.update_wave(dt)
        self.update_defenders(dt)
        self.update_enemies(dt)
        self.update_lane_bombs(dt)
        self.update_projectiles(dt)
        self.update_particles(dt)

    def enemy_at(self, pos: tuple[int, int]) -> Enemy | None:
        for enemy in reversed(self.enemies):
            if enemy.hitbox().inflate(16, 16).collidepoint(pos):
                return enemy
        return None

    def click_enemy(self, enemy: Enemy) -> bool:
        if "steal" not in enemy.tags:
            return False
        returned = int(enemy.stolen) + 28
        self.supplies += returned
        self.announce(f"Carga recuperada: +{returned} suprimentos!", 2.0, GOLD)
        self.kill_enemy(enemy)
        return True

    def handle_click(self, pos: tuple[int, int]) -> None:
        if self.finished:
            return
        if self.menu_rect().collidepoint(pos):
            self.app.leave_battle_to_title()
            return
        if self.pause_rect().collidepoint(pos):
            self.paused = not self.paused
            self.announce("Partida pausada." if self.paused else "Partida retomada.", 1.5, GOLD)
            return
        if self.paused:
            return
        if self.difficulty != "easy" and self.remove_rect().collidepoint(pos):
            self.remove_mode = not self.remove_mode
            self.use_core = False
            self.announce("Ferramenta de remoção ativada: clique em uma defesa." if self.remove_mode else "Ferramenta de remoção desativada.", 1.8, TEAL)
            return
        if self.next_wave_rect().collidepoint(pos):
            if not self.started_wave:
                self.intermission = 0
                self.start_next_wave()
            else:
                self.announce("A horda atual ainda está em andamento.", 1.3, GRAY)
            return
        thief = self.enemy_at(pos)
        if thief and self.click_enemy(thief):
            return
        for index, rect in enumerate(self.card_rects()):
            if rect.collidepoint(pos):
                if self.card_cooldowns[index] <= 0:
                    self.selected_card = index
                    self.use_core = False
                    self.remove_mode = False
                    key, display = self.selected[index]
                    # Confirmação breve, sem devolver a antiga barra fixa de
                    # descrição: a moldura dourada, a arte e o nome seguem a
                    # mesma chave que será usada por place().
                    self.announce(f"Selecionado: {display} (N{DEFENSES[key]['level']}).", 1.15, self.region_color())
                return
        if self.core_rect().collidepoint(pos):
            if self.cores > 0:
                self.use_core = not self.use_core
                self.remove_mode = False
                self.announce("Clique em uma defesa para ascensioná-la." if self.use_core else "Núcleo cancelado.", 1.5, GOLD)
            else:
                self.announce("Derrote um chefe para receber um Núcleo.", 1.6, GRAY)
            return
        cell = self.board_cell_at(pos)
        if cell:
            row, col = cell
            if self.use_core:
                self.apply_core(row, col)
            elif self.remove_mode:
                self.remove_defender(row, col)
            else:
                self.place(row, col)

    def card_rects(self) -> list[pygame.Rect]:
        count = len(self.selected)
        width = min(138, (WIDTH - 185) // max(1, count))
        return [pygame.Rect(10 + index * width, 8, width - 5, 102) for index in range(count)]


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(f"Soldados vs Zumbis — {VERSION}")
        self.presenter: OpenGLPresenter | None = None
        self.renderer_error = ""
        self.renderer_label = "Pygame · compatibilidade"
        self.actor_commands: list[ActorCommand] = []
        self.overlay_surface: pygame.Surface | None = None
        self.world_surface = self._create_display()
        self.screen = self.world_surface
        self.clock = pygame.time.Clock()
        self.fonts = FontBook()
        self.assets = Assets()
        self.gpu_preload_queue: list[pygame.Surface] = []
        self.gpu_preloaded = 0
        self.gpu_queue_ready = False
        self.running = True
        self.scene = "loading"
        self.scene_elapsed = 0.0
        self.save = load_save()
        self.region = "city"
        self.difficulty = "medium"
        self.selection: list[tuple[str, str]] = []
        self.battle: Battle | None = None
        self.dossier_kind = "units"
        self.dossier_page = 0
        self.hover_card: tuple[str, str] | None = None

    def _create_display(self) -> pygame.Surface:
        """Abre OpenGL quando há GPU e preserva um fallback Pygame completo."""
        requested = os.environ.get("SVZ_RENDERER", "opengl").strip().lower()
        dummy_driver = os.environ.get("SDL_VIDEODRIVER", "").strip().lower() == "dummy"
        if requested not in {"software", "pygame"} and not dummy_driver:
            try:
                pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 2)
                pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 1)
                pygame.display.gl_set_attribute(pygame.GL_DOUBLEBUFFER, 1)
                pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
                presenter = OpenGLPresenter(WIDTH, HEIGHT)
                self.presenter = presenter
                self.renderer_label = presenter.info.label
                self.overlay_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
                return pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
            except Exception as exc:  # driver ausente ou OpenGL muito antigo
                self.renderer_error = f"{type(exc).__name__}: {exc}"
                if self.presenter is not None:
                    self.presenter.close()
                    self.presenter = None
                pygame.display.quit()
                pygame.display.init()
                pygame.display.set_caption(f"Soldados vs Zumbis — {VERSION}")
        display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.overlay_surface = None
        return display

    def present_frame(self) -> None:
        """Entrega o quadro ao compositor escolhido sem duplicar a lógica."""
        if self.presenter is None:
            pygame.display.flip()
            return
        tint = REGIONS.get(self.battle.region if self.battle else self.region, REGIONS["city"])["accent"]
        self.presenter.present(
            self.world_surface,
            actors=self.actor_commands,
            overlay=self.overlay_surface,
            elapsed=self.scene_elapsed,
            tint=tint,
            strength=1.0 if self.scene == "battle" else 0.42,
        )

    def run(self) -> None:
        try:
            while self.running:
                dt = min(0.05, self.clock.tick(FPS) / 1000.0)
                self.scene_elapsed += dt
                self.handle_events()
                self.update(dt)
                self.draw()
                self.present_frame()
        finally:
            if self.presenter is not None:
                self.presenter.close()
            pygame.quit()

    def update(self, dt: float) -> None:
        if self.scene == "loading":
            if not self.assets.complete:
                self.assets.load_next()
            if self.assets.complete:
                if self.presenter is not None:
                    if not self.gpu_queue_ready:
                        self.gpu_preload_queue = self.assets.actor_sources()
                        self.gpu_queue_ready = True
                    batch_end = min(len(self.gpu_preload_queue), self.gpu_preloaded + 8)
                    if batch_end > self.gpu_preloaded:
                        self.presenter.preload_sprites(self.gpu_preload_queue[self.gpu_preloaded:batch_end])
                        self.gpu_preloaded = batch_end
                    if self.gpu_preloaded < len(self.gpu_preload_queue):
                        return
                self.scene = "title"
                self.scene_elapsed = 0
        elif self.scene == "battle" and self.battle:
            self.battle.update(dt)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_key(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_click(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                self.hover_card = None
                if self.scene == "select":
                    for key, display, rect in self.selection_cards():
                        if rect.collidepoint(event.pos):
                            self.hover_card = (key, display)

    def handle_key(self, key: int) -> None:
        if key == pygame.K_ESCAPE:
            if self.scene == "title":
                self.running = False
            elif self.scene == "battle":
                self.leave_battle_to_title()
            else:
                self.scene = "title"
            return
        if self.scene == "title" and key in (pygame.K_RETURN, pygame.K_SPACE):
            self.scene = "difficulty"
        elif self.scene == "difficulty" and key in (pygame.K_1, pygame.K_2, pygame.K_3):
            self.difficulty = ("easy", "medium", "hard")[key - pygame.K_1]
            self.scene = "campaign"
        elif self.scene == "campaign" and key in (pygame.K_1, pygame.K_2, pygame.K_3):
            target = ("city", "desert", "beach")[key - pygame.K_1]
            self.enter_selection(target)
        elif self.scene == "battle" and self.battle:
            if pygame.K_1 <= key <= pygame.K_8:
                choice = key - pygame.K_1
                if choice < len(self.battle.selected):
                    self.battle.selected_card = choice
                    self.battle.use_core = False
                    self.battle.remove_mode = False
            elif key == pygame.K_e:
                if self.battle.cores:
                    self.battle.use_core = not self.battle.use_core
                    self.battle.remove_mode = False
            elif key == pygame.K_r and self.battle.difficulty != "easy":
                self.battle.remove_mode = not self.battle.remove_mode
                self.battle.use_core = False
                self.battle.announce("Ferramenta de remoção ativada." if self.battle.remove_mode else "Ferramenta de remoção desativada.", 1.4, TEAL)
            elif key == pygame.K_p:
                self.battle.paused = not self.battle.paused
                self.battle.announce("Partida pausada." if self.battle.paused else "Partida retomada.", 1.4, GOLD)
            elif key == pygame.K_SPACE and not self.battle.started_wave:
                self.battle.intermission = 0
                self.battle.start_next_wave()
            elif self.battle.finished and key == pygame.K_RETURN:
                self.finish_battle()

    def handle_click(self, pos: tuple[int, int]) -> None:
        if self.scene == "loading":
            return
        if self.scene == "title":
            self.click_title(pos)
        elif self.scene == "difficulty":
            self.click_difficulty(pos)
        elif self.scene == "campaign":
            self.click_campaign(pos)
        elif self.scene == "select":
            self.click_selection(pos)
        elif self.scene.startswith("dossier"):
            self.click_dossier(pos)
        elif self.scene == "howto":
            if self.button_rect("Voltar", 50, 645, 170, 46).collidepoint(pos):
                self.scene = "title"
        elif self.scene == "battle" and self.battle:
            if self.battle.finished:
                if pygame.Rect(WIDTH // 2 - 145, HEIGHT // 2 + 100, 290, 50).collidepoint(pos):
                    self.finish_battle()
            else:
                self.battle.handle_click(pos)

    def title_buttons(self) -> list[tuple[str, pygame.Rect]]:
        return [
            ("JOGAR CAMPANHA", pygame.Rect(62, 282, 274, 54)),
            ("COMO JOGAR", pygame.Rect(62, 348, 274, 48)),
            ("SOLDADOS", pygame.Rect(62, 408, 130, 46)),
            ("ZUMBIS", pygame.Rect(206, 408, 130, 46)),
            ("SAIR", pygame.Rect(62, 468, 274, 42)),
        ]

    def click_title(self, pos: tuple[int, int]) -> None:
        for label, rect in self.title_buttons():
            if not rect.collidepoint(pos):
                continue
            if label == "JOGAR CAMPANHA":
                self.scene = "difficulty"
            elif label == "COMO JOGAR":
                self.scene = "howto"
            elif label == "SOLDADOS":
                self.scene, self.dossier_kind, self.dossier_page = "dossier_units", "units", 0
            elif label == "ZUMBIS":
                self.scene, self.dossier_kind, self.dossier_page = "dossier_zombies", "zombies", 0
            elif label == "SAIR":
                self.running = False

    def difficulty_buttons(self) -> list[tuple[str, pygame.Rect]]:
        return [
            ("easy", pygame.Rect(80, 500, 320, 48)),
            ("medium", pygame.Rect(480, 500, 320, 48)),
            ("hard", pygame.Rect(880, 500, 320, 48)),
        ]

    def click_difficulty(self, pos: tuple[int, int]) -> None:
        for key, rect in self.difficulty_buttons():
            if rect.collidepoint(pos):
                self.difficulty = key
                self.scene = "campaign"
                return
        if self.button_rect("Voltar", 50, 645, 170, 46).collidepoint(pos):
            self.scene = "title"

    def click_campaign(self, pos: tuple[int, int]) -> None:
        for index, region in enumerate(("city", "desert", "beach")):
            rect = pygame.Rect(72 + index * 402, 182, 360, 350)
            if rect.collidepoint(pos):
                self.enter_selection(region)
                return
        if self.button_rect("Voltar", 50, 645, 170, 46).collidepoint(pos):
            self.scene = "title"

    def enter_selection(self, region: str) -> None:
        self.region = region
        # A seleção inicial já respeita o modo escolhido. Assim o Fácil não
        # começa com N1 escondido e o Difícil nunca recebe N2 por acidente.
        available = self.available_selection_keys(region)
        self.selection = [(key, self.card_display_name(region, key)) for key in available[:8]]
        self.scene = "select"

    @staticmethod
    def _unique_keys(keys: list[str]) -> list[str]:
        seen: set[str] = set()
        return [key for key in keys if not (key in seen or seen.add(key))]

    def regional_card_keys(self, region: str) -> list[str]:
        """Lista o elenco temático e adiciona somente a evolução do seu par.

        As cartas marítimas pertencem somente à Praia: elas não aparecem como
        opção decorativa na Cidade nem no Deserto. Ainda assim, na Praia cada
        N1 recebe a N2 correspondente sem misturar as colunas de evolução.
        """
        keys = [key for key, _display in REGION_ROSTERS[region]]
        initial = set(keys)
        for level_one, level_two in PROMOTIONS.items():
            if level_one in initial or level_two in initial:
                keys.extend((level_one, level_two))
        if region == "beach":
            keys.extend(("submarino", "bomba_agua"))
        keys.append("instrutor")
        return self._unique_keys(keys)

    def available_selection_keys(self, region: str | None = None) -> list[str]:
        region = region or self.region
        allowed_levels = set(difficulty_profile(self.difficulty)["levels"])
        # O Sargento é a carta especial de compensação do Difícil. Ele deixa
        # de poluir as escolhas de Fácil/Médio e entra no Difícil mesmo sendo
        # N2, pois esse modo normalmente liberaria apenas as cartas N1.
        return [
            key
            for key in self.regional_card_keys(region)
            if (key == "instrutor" and self.difficulty == "hard")
            or (key != "instrutor" and int(DEFENSES[key]["level"]) in allowed_levels)
        ]

    @staticmethod
    def card_display_name(region: str, key: str) -> str:
        for roster_key, display in REGION_ROSTERS[region]:
            if roster_key == key:
                return display
        return str(DEFENSES[key]["base"])

    def selection_cards(self) -> list[tuple[str, str, pygame.Rect]]:
        """Monta uma grade sem sobreposição e sem níveis trocados.

        No Médio, cada par de evolução ocupa uma coluna vertical: N1 em cima,
        N2 correspondente embaixo. Nos modos que liberam um único nível, a
        própria regra mostra somente as cartas autorizadas, em grade simples.
        """
        keys = self.available_selection_keys()
        cards: list[tuple[str, str, pygame.Rect]] = []
        if tuple(difficulty_profile(self.difficulty)["levels"]) != (1, 2):
            for index, key in enumerate(keys):
                row, col = divmod(index, 7)
                rect = pygame.Rect(44 + col * 174, 100 + row * 126, 154, 116)
                cards.append((key, self.card_display_name(self.region, key), rect))
            return cards

        key_set = set(keys)
        pairs = [(l1, l2) for l1, l2 in PROMOTIONS.items() if l1 in key_set and l2 in key_set]
        paired_keys = {key for pair in pairs for key in pair}
        for pair_index, (level_one, level_two) in enumerate(pairs):
            # Cada bloco comporta até seis colunas de evolução. A sétima fica
            # reservada às cartas especiais N2, impedindo que o Sargento — e,
            # na Praia, Submarino/Bomba de Água — pareça ser a N2 de outra
            # carta.
            block, col = divmod(pair_index, 6)
            top_row = block * 2
            for row, key in ((top_row, level_one), (top_row + 1, level_two)):
                rect = pygame.Rect(44 + col * 174, 100 + row * 126, 154, 116)
                cards.append((key, self.card_display_name(self.region, key), rect))

        # Cartas sem contraparte vivem em uma coluna exclusiva: Sargento em
        # todos os mapas; Submarino e Bomba de Água apenas na Praia. Todas são
        # N2, portanto não misturam a leitura dos pares N1 -> N2.
        for row, key in enumerate(key for key in keys if key not in paired_keys):
            col = 6
            rect = pygame.Rect(44 + col * 174, 100 + row * 126, 154, 116)
            cards.append((key, self.card_display_name(self.region, key), rect))
        return cards

    def click_selection(self, pos: tuple[int, int]) -> None:
        for key, display, rect in self.selection_cards():
            if not rect.collidepoint(pos):
                continue
            item = (key, display)
            if item in self.selection:
                self.selection.remove(item)
            elif len(self.selection) < 8:
                self.selection.append(item)
            return
        launch = pygame.Rect(WIDTH - 290, 650, 240, 46)
        if launch.collidepoint(pos):
            if len(self.selection) == 8:
                self.battle = Battle(self, self.region, self.selection[:])
                self.scene = "battle"
            else:
                return
        if self.button_rect("Voltar", 45, 650, 160, 46).collidepoint(pos):
            self.scene = "campaign"

    def dossier_items(self) -> list[dict]:
        if self.dossier_kind == "units":
            regional_keys = set(self.regional_card_keys(self.region))
            items = [
                {"kind": "evolution", "l1": l1, "l2": l2}
                for l1, l2 in PROMOTIONS.items()
                if l1 in regional_keys and l2 in regional_keys
            ]
            if "instrutor" in regional_keys and self.difficulty == "hard":
                items.append({"kind": "promoter", "key": "instrutor"})
            return items
        return [
            {"name": data["name"], "sub": "Chefe" if key in BOSSES else "Inimigo", "ability": data["ability"], "hp": int(data["hp"]), "key": key}
            for key, data in {**ENEMIES, **BOSSES}.items()
        ]

    def click_dossier(self, pos: tuple[int, int]) -> None:
        if self.button_rect("Voltar", 40, 648, 160, 42).collidepoint(pos):
            self.scene = "title"
            return
        if pygame.Rect(WIDTH - 180, 648, 140, 42).collidepoint(pos):
            items = self.dossier_items()
            pages = max(1, math.ceil(len(items) / 6))
            self.dossier_page = (self.dossier_page + 1) % pages

    def finish_battle(self) -> None:
        if not self.battle:
            self.scene = "campaign"
            return
        if self.battle.victory:
            region = self.battle.region
            if region not in self.save["completed"]:
                self.save["completed"].append(region)
            self.save["unlocked"] = list(REGIONS)
            self.save["best_wave"][region] = max(self.save["best_wave"].get(region, 0), 15)
            save_campaign(self.save)
        self.battle = None
        self.scene = "campaign"

    def leave_battle_to_title(self) -> None:
        """Saída voluntária sem registrar vitória, derrota ou progresso falso."""
        self.battle = None
        self.scene = "title"
        self.scene_elapsed = 0.0

    def button_rect(self, label: str, x: int, y: int, w: int, h: int) -> pygame.Rect:
        return pygame.Rect(x, y, w, h)

    def draw_text(self, text: str, font: pygame.font.Font, color: tuple[int, int, int], pos: tuple[float, float], anchor: str = "topleft", shadow: bool = False) -> pygame.Rect:
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        setattr(rect, anchor, (int(pos[0]), int(pos[1])))
        if shadow:
            shadow_surface = font.render(text, True, (0, 0, 0))
            shadow_rect = shadow_surface.get_rect()
            setattr(shadow_rect, anchor, (int(pos[0] + 2), int(pos[1] + 2)))
            self.screen.blit(shadow_surface, shadow_rect)
        self.screen.blit(surface, rect)
        return rect

    def panel(self, rect: pygame.Rect, alpha: int = 210, border: tuple[int, int, int] = (91, 106, 112), radius: int = 10) -> None:
        surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(surface, (12, 20, 25, alpha), surface.get_rect(), border_radius=radius)
        pygame.draw.rect(surface, (*border, min(255, alpha + 25)), surface.get_rect(), width=2, border_radius=radius)
        self.screen.blit(surface, rect)

    def button(self, label: str, rect: pygame.Rect, accent: tuple[int, int, int], enabled: bool = True) -> None:
        hover = rect.collidepoint(pygame.mouse.get_pos()) and enabled
        outer = tuple(min(255, c + 25) for c in accent) if hover else accent
        color = outer if enabled else (67, 73, 76)
        pygame.draw.rect(self.screen, (8, 13, 17), rect.inflate(4, 4), border_radius=8)
        pygame.draw.rect(self.screen, color, rect, border_radius=7)
        pygame.draw.rect(self.screen, (228, 235, 228), rect, width=1, border_radius=7)
        self.draw_text(label, self.fonts.h2, INK if enabled else GRAY, rect.center, "center")

    def draw_loading(self) -> None:
        loading_art = self.assets.images.get("loading_beta3")
        if loading_art is not None:
            self.screen.blit(loading_art, (0, 0))
            veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            veil.fill((3, 8, 12, 54))
            self.screen.blit(veil, (0, 0))
        else:
            self.screen.fill((8, 13, 18))
        asset_progress = self.assets.loaded / max(1, self.assets.total)
        if self.presenter is not None:
            gpu_total = len(self.gpu_preload_queue)
            gpu_progress = (self.gpu_preloaded / gpu_total) if gpu_total else (1.0 if self.assets.complete else 0.0)
            progress = asset_progress * 0.74 + gpu_progress * 0.26
        else:
            progress = asset_progress
        # A arte entregue pelo usuário já contém o título. O painel discreto
        # abaixo não a redesenha nem esconde o logotipo central.
        panel = pygame.Rect(WIDTH // 2 - 282, HEIGHT - 150, 564, 108)
        self.panel(panel, 204, (166, 130, 62), 12)
        self.draw_text(f"{VERSION} — CARREGANDO", self.fonts.h2, WHITE, (panel.centerx, panel.y + 17), "center", True)
        bar = pygame.Rect(panel.x + 42, panel.y + 51, panel.width - 84, 18)
        pygame.draw.rect(self.screen, (31, 42, 47), bar, border_radius=9)
        pygame.draw.rect(self.screen, TEAL, (bar.x, bar.y, int(bar.width * progress), bar.height), border_radius=9)
        if self.presenter is not None and self.assets.complete:
            status = f"Enviando atores para a GPU  {self.gpu_preloaded}/{len(self.gpu_preload_queue)}"
        else:
            status = f"Preparando artes e animações  {self.assets.loaded}/{self.assets.total}"
        self.draw_text(status, self.fonts.small, WHITE, (panel.centerx, panel.y + 79), "center")
        if self.assets.error:
            self.draw_text(self.assets.error, self.fonts.small, RED, (panel.centerx, panel.y - 18), "center")

    def draw_title(self) -> None:
        self.screen.blit(self.assets.images["menu"], (0, 0))
        tint = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        tint.fill((3, 8, 12, 92))
        self.screen.blit(tint, (0, 0))
        self.panel(pygame.Rect(36, 80, 336, 462), 210, (166, 130, 62), 14)
        self.draw_text("SOLDADOS", self.fonts.title, (242, 239, 218), (62, 108), shadow=True)
        self.draw_text("VS", self.fonts.small, GOLD, (338, 153), "topright", True)
        self.draw_text("ZUMBIS", self.fonts.title, (154, 206, 127), (62, 166), shadow=True)
        self.draw_text("DEFENDA. RECARREGUE. RESISTA.", self.fonts.small, GRAY, (64, 224))
        for label, rect in self.title_buttons():
            accent = GOLD if label == "JOGAR CAMPANHA" else (81, 145, 137)
            self.button(label, rect, accent)
        self.draw_text(f"{VERSION} • Cidade • Deserto • Praia", self.fonts.small, WHITE, (40, HEIGHT - 28))
        self.draw_text("Artes originais • campanha de 15 ondas", self.fonts.small, WHITE, (WIDTH - 36, HEIGHT - 28), "topright")

    def draw_difficulty(self) -> None:
        self.screen.blit(self.assets.images["menu"], (0, 0))
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((3, 8, 12, 178))
        self.screen.blit(veil, (0, 0))
        self.draw_text("ESCOLHA A DIFICULDADE", self.fonts.title, WHITE, (WIDTH / 2, 42), "center", True)
        self.draw_text("O modo altera as cartas liberadas, a força dos inimigos e o ritmo das hordas.", self.fonts.body, GOLD, (WIDTH / 2, 91), "center")
        descriptions = {
            "easy": (
                "COMEÇAR TRANQUILO",
                ("Somente cartas N2", "3 Núcleos N3 logo no início", "Zumbis mais fracos e hordas menores"),
            ),
            "medium": (
                "CAMPANHA EQUILIBRADA",
                ("Cartas N1 e N2", "Dificuldade leve e progressiva", "15 ondas exigentes, mas justas"),
            ),
            "hard": (
                "SOBREVIVÊNCIA VETERANA",
                ("Somente cartas N1", "Hordas mais rápidas e resistentes", "Difícil, mas com recursos para vencer"),
            ),
        }
        for index, (key, button_rect) in enumerate(self.difficulty_buttons()):
            profile = difficulty_profile(key)
            card = pygame.Rect(button_rect.x - 25, 150, button_rect.width + 50, 370)
            self.panel(card, 235, profile["accent"], 14)
            subtitle, lines = descriptions[key]
            self.draw_text(profile["label"], self.fonts.title, profile["accent"], (card.centerx, card.y + 32), "center", True)
            self.draw_text(subtitle, self.fonts.small, WHITE, (card.centerx, card.y + 92), "center")
            for line_index, line in enumerate(lines):
                y = card.y + 148 + line_index * 53
                pygame.draw.circle(self.screen, profile["accent"], (card.x + 31, y + 8), 5)
                self.draw_wrapped(line, self.fonts.small, WHITE, pygame.Rect(card.x + 46, y - 7, card.width - 64, 31), 2)
            self.draw_wrapped(profile["summary"], self.fonts.tiny, GRAY, pygame.Rect(card.x + 23, card.bottom - 71, card.width - 46, 38), 2, center=True)
            self.button(f"ESCOLHER {profile['label']}", button_rect, profile["accent"])
        self.button("VOLTAR", self.button_rect("Voltar", 50, 645, 170, 46), (92, 126, 137))

    def draw_campaign(self) -> None:
        self.screen.blit(self.assets.images["menu"], (0, 0))
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((4, 11, 16, 170))
        self.screen.blit(veil, (0, 0))
        self.draw_text("MAPA DA CAMPANHA", self.fonts.title, WHITE, (WIDTH / 2, 38), "center", True)
        profile = difficulty_profile(self.difficulty)
        self.draw_text(f"Modo {profile['label']} — {profile['summary']}", self.fonts.body, profile["accent"], (WIDTH / 2, 84), "center")
        self.draw_text("Escolha livremente Cidade, Deserto ou Praia. Cada região possui 15 ondas e chefes nas ondas 5, 10 e 15.", self.fonts.small, GOLD, (WIDTH / 2, 111), "center")
        for index, region in enumerate(("city", "desert", "beach")):
            info = REGIONS[region]
            rect = pygame.Rect(72 + index * 402, 182, 360, 350)
            unlocked = True
            background = self.assets.images[f"{region}_bg"]
            crop = pygame.Rect(index * 160, 150, 360, 208)
            image = pygame.Surface((360, 210))
            image.blit(background, (0, 0), crop)
            self.screen.blit(image, rect)
            self.panel(rect, 105 if unlocked else 215, info["accent"] if unlocked else (75, 75, 75), 14)
            if not unlocked:
                lock = pygame.Rect(rect.centerx - 28, rect.y + 104, 56, 66)
                pygame.draw.rect(self.screen, (49, 54, 60), lock, border_radius=9)
                pygame.draw.arc(self.screen, GRAY, (lock.x + 9, lock.y - 27, 38, 40), 0, math.pi, 5)
                self.draw_text("BLOQUEADA", self.fonts.h2, GRAY, (rect.centerx, rect.y + 184), "center")
            else:
                self.draw_text(info["short"], self.fonts.h1, WHITE, (rect.centerx, rect.y + 222), "center", True)
                self.draw_text(info["tag"], self.fonts.small, info["accent"], (rect.centerx, rect.y + 252), "center")
                best = self.save["best_wave"].get(region, 0)
                status = "REGIÃO PROTEGIDA" if region in self.save["completed"] else f"Melhor: onda {best}/15"
                self.draw_text(status, self.fonts.small, GOLD if region in self.save["completed"] else WHITE, (rect.centerx, rect.y + 286), "center")
                self.button("PREPARAR CARTAS", pygame.Rect(rect.x + 55, rect.y + 304, 250, 34), info["accent"])
        self.button("VOLTAR", self.button_rect("Voltar", 50, 645, 170, 46), (92, 126, 137))

    def draw_selection(self) -> None:
        region = REGIONS[self.region]
        self.screen.blit(self.assets.images[f"{self.region}_bg"], (0, 0))
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((6, 11, 14, 157))
        self.screen.blit(shade, (0, 0))
        profile = difficulty_profile(self.difficulty)
        self.draw_text(f"SELEÇÃO DE CARTAS — {region['name'].upper()} — {profile['label']}", self.fonts.h1, WHITE, (WIDTH / 2, 22), "center", True)
        water_rule = "Cartas marítimas são exclusivas do canal da Praia." if self.region == "beach" else "Este mapa usa apenas cartas terrestres."
        if tuple(profile["levels"]) == (1, 2):
            selection_rule = f"Escolha 8 cartas. N1 fica exatamente sobre sua N2; {water_rule}"
        else:
            level_label = "N2" if profile["levels"] == (2,) else "N1"
            selection_rule = f"Modo {profile['label']}: somente cartas {level_label}. {water_rule}"
        self.draw_text(selection_rule, self.fonts.small, profile["accent"], (WIDTH / 2, 55), "center")
        self.draw_text(f"{len(self.selection)}/8 selecionadas", self.fonts.h2, region["accent"], (WIDTH - 48, 82), "topright")
        for key, display, rect in self.selection_cards():
            data = DEFENSES[key]
            chosen = (key, display) in self.selection
            self.panel(rect, 230, region["accent"] if chosen else (91, 105, 107), 10)
            sprite = self.card_sprite(self.region, key, int(data["sprite"]))
            self.blit_sprite(sprite, rect.x + 6, rect.y + 15, 54, 64)
            # O rosto da carta é uma ficha curta de decisão. Nome e habilidade
            # aparecem exclusivamente ao passar o mouse, sem texto duplicado.
            metric_a, metric_b = self.card_metrics(data)
            self.draw_text(f"{data['cost']} SUP", self.fonts.small, GOLD, (rect.x + 66, rect.y + 14))
            self.draw_text(metric_a, self.fonts.tiny, WHITE, (rect.x + 66, rect.y + 38))
            self.draw_text(metric_b, self.fonts.tiny, TEAL if data["ammo"] or data["role"] in {"radio", "promoter"} else (208, 218, 213), (rect.x + 66, rect.y + 55))
            special_n2 = (self.difficulty == "medium" and key in {"submarino", "bomba_agua"}) or (self.difficulty == "hard" and key == "instrutor")
            level = f"N{data['level']}" + (" • ESPECIAL" if special_n2 else "") + (" • ÁGUA" if data.get("water_only") else "")
            self.draw_text(level, self.fonts.tiny, TEAL if data.get("water_only") else region["accent"], (rect.x + 12, rect.y + 93))
            self.draw_text(f"HP {int(data['hp'])}", self.fonts.tiny, GRAY, (rect.right - 12, rect.y + 93), "topright")
            if chosen:
                self.draw_text("✓", self.fonts.h1, GOLD, (rect.right - 15, rect.y + 10), "topright")
        self.button("VOLTAR", self.button_rect("Voltar", 45, 650, 160, 46), (98, 126, 137))
        self.button("INICIAR MISSÃO", pygame.Rect(WIDTH - 290, 650, 240, 46), region["accent"], len(self.selection) == 8)
        if self.hover_card:
            key, display = self.hover_card
            data = DEFENSES[key]
            tooltip = pygame.Rect(250, 600, 780, 42)
            self.panel(tooltip, 235, region["accent"], 8)
            self.draw_text(display, self.fonts.tiny, GOLD, (tooltip.x + 12, tooltip.y + 7))
            self.draw_wrapped(data["ability"], self.fonts.tiny, WHITE, pygame.Rect(tooltip.x + 126, tooltip.y + 7, tooltip.width - 138, 27), 2)

    def draw_howto(self) -> None:
        self.screen.blit(self.assets.images["menu"], (0, 0))
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((4, 10, 14, 186))
        self.screen.blit(veil, (0, 0))
        card = pygame.Rect(116, 72, WIDTH - 232, 560)
        self.panel(card, 238, GOLD, 16)
        self.draw_text("COMO JOGAR", self.fonts.title, WHITE, (card.centerx, card.y + 30), "center")
        lines = [
            ("1. Escolha 8 cartas", "Antes da missão, monte uma equipe. Cada região tem uniformes, armas e funções próprias."),
            ("2. Posicione por alcance", "As tropas só atacam quando um zumbi entra no alcance de seus blocos. Escopetas seguram perto; snipers cobrem a linha."),
            ("3. Munição e recarga", "Ao esvaziar a arma, a tropa baixa o armamento e recarrega sozinha por 8 a 15 s. Ela não atira durante a animação."),
            ("4. Suprimentos", "Rádio gera créditos. Cada arma recarrega sozinha no seu próprio tempo, sem carta externa de munição."),
            ("5. Chefes e N3", "Nas ondas 5, 10 e 15 há chefes. Ao derrubá-los, use N3 em uma defesa para ativar o Nível 3 temporário."),
            ("6. Comandos e água", "A aba superior reúne MENU, PAUSA, REMOVER, N3 e PRÓXIMA. Cartas marítimas aparecem somente na Praia e entram apenas no canal."),
        ]
        y = card.y + 102
        for head, body in lines:
            self.draw_text(head, self.fonts.h2, GOLD, (card.x + 48, y))
            self.draw_wrapped(body, self.fonts.body, WHITE, pygame.Rect(card.x + 48, y + 27, card.width - 96, 46), 2)
            y += 76
        self.button("VOLTAR", self.button_rect("Voltar", 50, 645, 170, 46), (92, 126, 137))

    def draw_unit_evolution_dossier(self) -> None:
        """Mostra a progressão literalmente em duas faixas: N1 sobre N2."""
        self.screen.blit(self.assets.images["menu"], (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((5, 10, 14, 190))
        self.screen.blit(overlay, (0, 0))
        accent = REGIONS[self.region]["accent"]
        self.draw_text("EVOLUÇÃO DOS SOLDADOS", self.fonts.title, WHITE, (WIDTH / 2, 20), "center", True)
        self.draw_text("N1 em cima • N2 embaixo • N3 é prêmio de chefe • no Difícil, o Sargento promove uma N1 após 90 s", self.fonts.small, accent, (WIDTH / 2, 70), "center")
        items = self.dossier_items()
        start = self.dossier_page * 6
        for index, item in enumerate(items[start:start + 6]):
            row, col = divmod(index, 3)
            rect = pygame.Rect(52 + col * 404, 110 + row * 247, 372, 226)
            self.panel(rect, 238, accent, 12)
            if item["kind"] == "promoter":
                data = DEFENSES["instrutor"]
                sprite = self.card_sprite(self.region, "instrutor", int(data["sprite"]))
                self.blit_sprite(sprite, rect.x + 18, rect.y + 48, 106, 126)
                self.draw_text("CARTA DE PROMOÇÃO", self.fonts.tiny, GOLD, (rect.x + 140, rect.y + 25))
                self.draw_text(data["base"], self.fonts.h2, WHITE, (rect.x + 140, rect.y + 48))
                self.draw_text(f"Custo {data['cost']} SUP • HP {data['hp']}", self.fonts.tiny, GOLD, (rect.x + 140, rect.y + 78))
                self.draw_wrapped(data["ability"], self.fonts.small, (219, 229, 225), pygame.Rect(rect.x + 140, rect.y + 104, 210, 74), 4)
                continue
            for tier_index, key in enumerate((item["l1"], item["l2"])):
                data = DEFENSES[key]
                tier = pygame.Rect(rect.x + 10, rect.y + 27 + tier_index * 96, rect.width - 20, 88)
                tier_color = (102, 128, 135) if tier_index == 0 else GOLD
                self.panel(tier, 205, tier_color, 8)
                sprite = self.card_sprite(self.region, key, int(data["sprite"]))
                self.blit_sprite(sprite, tier.x + 5, tier.y + 8, 60, 72)
                self.draw_text(f"N{data['level']}", self.fonts.tiny, tier_color, (tier.x + 74, tier.y + 9), shadow=True)
                self.draw_text(str(data["base"]), self.fonts.small, WHITE, (tier.x + 103, tier.y + 7))
                self.draw_text(f"HP {int(data['hp'])} • DANO {int(data['damage'])} • ALC {int(data['range'])}", self.fonts.tiny, GOLD, (tier.x + 74, tier.y + 29))
                self.draw_wrapped(str(data["ability"]), self.fonts.tiny, (219, 229, 225), pygame.Rect(tier.x + 74, tier.y + 45, tier.width - 84, 34), 2)
        pages = max(1, math.ceil(len(items) / 6))
        self.draw_text(f"Página {self.dossier_page + 1}/{pages} • uniforme atual: {REGIONS[self.region]['short'].title()}", self.fonts.small, WHITE, (WIDTH / 2, 664), "center")
        self.button("VOLTAR", self.button_rect("Voltar", 40, 648, 160, 42), (92, 126, 137))
        self.button("PRÓXIMA", pygame.Rect(WIDTH - 180, 648, 140, 42), accent)

    def draw_dossier(self) -> None:
        is_units = self.dossier_kind == "units"
        if is_units:
            self.draw_unit_evolution_dossier()
            return
        self.screen.blit(self.assets.images["menu"], (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((5, 10, 14, 190))
        self.screen.blit(overlay, (0, 0))
        heading = "INFORMAÇÕES DOS SOLDADOS" if is_units else "INFORMAÇÕES DOS ZUMBIS"
        accent = TEAL if is_units else (139, 222, 106)
        self.draw_text(heading, self.fonts.title, WHITE, (WIDTH / 2, 24), "center", True)
        self.draw_text("As fichas abaixo mostram função, poder e contraponto tático.", self.fonts.body, accent, (WIDTH / 2, 70), "center")
        items = self.dossier_items()
        start = self.dossier_page * 6
        page_items = items[start:start + 6]
        for index, item in enumerate(page_items):
            row, col = divmod(index, 3)
            rect = pygame.Rect(52 + col * 404, 123 + row * 235, 372, 208)
            self.panel(rect, 236, accent, 12)
            icon_index = DEFENSES[item["key"]]["sprite"] if is_units else ({**ENEMIES, **BOSSES}[item["key"]]["sprite"])
            sprite_region = "city" if is_units else ("city" if item["key"] in {"caminhante", "corredor", "rastejante", "conehead", "policial", "militar", "escudo", "cuspidor", "divisor", "gritador", "saltador", "bruto", "bruto_demolidor", "comandante_mortos", "cuspidor_alfa"} else ("desert" if item["key"] in {"digger", "ladrao", "curandeiro", "parasita", "mutante", "necromante_minion", "mutante_ruinas", "necromante", "colosso_mutante"} else "beach"))
            # A ficha de zumbis deve usar exatamente o mesmo retrato que a
            # batalha. Antes esta tela ainda puxava o quadro antigo do atlas
            # urbano para o Saltador, que incluía uma pilastra de cenário.
            # O retrato exclusivo da Beta 3 não traz obstáculo algum.
            dossier_sheet = {
                ("city", "caminhante"): "city_walker_walk",
                ("desert", "digger"): "desert_digger_states",
                ("beach", "nadador"): "beach_swimmer_walk",
            }.get((sprite_region, item["key"])) if not is_units else None
            if not is_units and item["key"] in BOSSES:
                boss_frames = self.assets.animation_frames.get(f"{sprite_region}_boss_actions", [])
                boss_row = REGIONS[sprite_region]["bosses"].index(item["key"])
                sprite = boss_frames[boss_row * 4] if len(boss_frames) >= 12 else self.assets.zombie(sprite_region, int(icon_index))
            elif dossier_sheet and self.assets.animation_frames.get(dossier_sheet):
                sprite = self.assets.animation_frames[dossier_sheet][0]
            elif not is_units and item["key"] == "saltador" and "zombie_jumper_beta3" in self.assets.images:
                sprite = self.assets.images["zombie_jumper_beta3"]
            elif not is_units and item["key"] == "rastejante" and "zombie_crawler_beta3" in self.assets.images:
                sprite = self.assets.images["zombie_crawler_beta3"]
            else:
                sprite = self.card_sprite(sprite_region, item["key"], int(icon_index)) if is_units else self.assets.zombie(sprite_region, int(icon_index))
            self.blit_sprite(sprite, rect.x + 14, rect.y + 44, 105, 118)
            self.draw_text(item["name"], self.fonts.h2, WHITE, (rect.x + 132, rect.y + 22))
            self.draw_text(item["sub"], self.fonts.small, accent, (rect.x + 132, rect.y + 51))
            stat = f"Custo: {item['cost']} SUP • Nível {item['level']}" if is_units else f"Vida base: {item['hp']}"
            self.draw_text(stat, self.fonts.tiny, GOLD, (rect.x + 132, rect.y + 76))
            self.draw_wrapped(item["ability"], self.fonts.small, (219, 229, 225), pygame.Rect(rect.x + 132, rect.y + 100, 220, 83), 4)
        pages = max(1, math.ceil(len(items) / 6))
        self.draw_text(f"Página {self.dossier_page + 1}/{pages}", self.fonts.small, WHITE, (WIDTH / 2, 664), "center")
        self.button("VOLTAR", self.button_rect("Voltar", 40, 648, 160, 42), (92, 126, 137))
        self.button("PRÓXIMA", pygame.Rect(WIDTH - 180, 648, 140, 42), accent)

    def draw_battle(self) -> None:
        assert self.battle is not None
        battle = self.battle
        background = self.assets.images[f"{battle.region}_bg"]
        shake_x = int(math.sin(self.scene_elapsed * 55) * 4 * battle.shake)
        shake_y = int(math.cos(self.scene_elapsed * 37) * 3 * battle.shake)
        self.screen.blit(background, (shake_x, shake_y))
        # As quatro pistas já estão pintadas no próprio cenário. Nenhuma faixa
        # sintética é sobreposta à arte: pés, água, asfalto e areia coincidem.
        ambient = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        if battle.global_toxic > 0:
            ambient.fill((92, 202, 86, int(30 + battle.global_toxic * 8)))
        self.screen.blit(ambient, (0, 0))
        self.draw_lane_bombs(battle)
        mouse = pygame.mouse.get_pos()
        hovered_cell = battle.board_cell_at(mouse)
        if hovered_cell and not battle.finished:
            row, col = hovered_cell
            outline = battle.ground_cell_rect(row, col)
            color = RED if battle.remove_mode else (GOLD if battle.use_core else battle.region_color())
            pygame.draw.rect(self.screen, color, outline, 2, border_radius=12)
            if battle.cell_is_water(row, col):
                pygame.draw.arc(self.screen, (110, 213, 250), outline.inflate(-22, -28), 0, math.pi, 2)
        for defender in battle.defenders:
            self.draw_defender(defender)
        for enemy in battle.enemies:
            self.draw_enemy(enemy)
        self.draw_fallen(battle)
        if self.overlay_surface is not None:
            self.screen = self.overlay_surface
        self.draw_projectiles(battle)
        self.draw_visual_effects(battle)
        self.draw_particles(battle)
        self.draw_battle_top()
        self.draw_battle_status()
        if battle.finished:
            self.draw_result_overlay()

    def draw_lane_guides(self, battle: Battle) -> None:
        """Compatibilidade: os limites agora pertencem à própria pintura."""
        return

    def draw_lane_bombs(self, battle: Battle) -> None:
        """Mostra a contenção visual própria de cada terreno antes da invasão."""
        for cart in battle.lane_bombs:
            if cart.state == "spent":
                continue
            y = cell_center(cart.row, 0, battle.region)[1]
            x = cart.x if cart.state == "rolling" else float(LANE_BOMB_HOME_X)
            sprite = self.assets.images.get(battle.lane_bomb_asset_key(cart.row))
            is_water_buoy = battle.region == "beach" and cart.row in battle.water_rows
            depth = lane_depth(battle.region, cart.row)
            if sprite and sprite.get_width() > 1:
                # A contenção inteira fica dentro do terreno, antes da primeira
                # casa, e compartilha exatamente a linha de contato da pista.
                base_width, base_height = (54, 44) if is_water_buoy else (56, 42)
                width, height = base_width * depth, base_height * depth
                self.draw_actor_sprite(sprite, x, y, width, height, cart.motion, enemy=False)

    def draw_battle_top(self) -> None:
        assert self.battle is not None
        battle = self.battle
        rects = battle.card_rects()
        for index, ((key, display), rect) in enumerate(zip(battle.selected, rects)):
            data = DEFENSES[key]
            active = index == battle.selected_card and not battle.use_core
            self.panel(rect, 238, GOLD if active else battle.region_color(), 7)
            if battle.card_cooldowns[index] > 0:
                dark = pygame.Surface(rect.size, pygame.SRCALPHA)
                dark.fill((0, 0, 0, 125))
                self.screen.blit(dark, rect)
                self.draw_text(f"{math.ceil(battle.card_cooldowns[index])}s", self.fonts.small, WHITE, rect.center, "center", True)
            self.blit_sprite(self.card_sprite(battle.region, key, int(data["sprite"])), rect.x + 5, rect.y + 25, 44, 56)
            self.draw_text(str(index + 1), self.fonts.tiny, GOLD, (rect.x + 7, rect.y + 6))
            metric_a, metric_b = self.card_metrics(data)
            self.draw_text(f"{data['cost']} SUP", self.fonts.tiny, GOLD, (rect.x + 51, rect.y + 15))
            self.draw_text(metric_a, self.fonts.tiny, WHITE, (rect.x + 51, rect.y + 35))
            self.draw_text(metric_b, self.fonts.tiny, TEAL if data["ammo"] or data["role"] in {"radio", "promoter"} else GRAY, (rect.x + 51, rect.y + 54))
            if data.get("water_only"):
                self.draw_text("ÁGUA", self.fonts.tiny, TEAL, (rect.centerx, rect.bottom - 15), "center")
        self.panel(pygame.Rect(WIDTH - 176, 8, 166, 104), 230, battle.region_color(), 8)
        self.draw_text(f"{battle.supplies} SUP", self.fonts.h2, GOLD, (WIDTH - 93, 18), "center")
        self.draw_text(f"ONDA {battle.wave}/15", self.fonts.small, WHITE, (WIDTH - 93, 48), "center")
        self.draw_text(f"{len(battle.enemies) + len(battle.orders)} INVASORES", self.fonts.tiny, GRAY, (WIDTH - 93, 78), "center")

        # Comandos de missão em uma única aba, sempre acima do terreno.
        shelf = pygame.Rect(10, 118, WIDTH - 20, 50)
        self.panel(shelf, 221, battle.region_color(), 8)
        self.button("MENU", battle.menu_rect(), battle.region_color())
        self.button("PAUSA", battle.pause_rect(), GOLD)
        if battle.difficulty != "easy":
            self.button("REMOVER", battle.remove_rect(), RED if battle.remove_mode else (88, 125, 132))
        self.button(f"N3 x{battle.cores}", battle.core_rect(), GOLD if battle.cores else (70, 73, 75), battle.cores > 0)
        self.button("PRÓXIMA", battle.next_wave_rect(), battle.region_color(), not battle.started_wave)
        if battle.started_wave:
            tactical_status = f"HORDA ATIVA • {len(battle.enemies) + len(battle.orders)} invasores"
        else:
            tactical_status = f"INTERVALO TÁTICO • {max(0, math.ceil(battle.intermission))} s"
        ticker = battle.message if battle.message_timer > 0 else "Equipe em posição."
        if len(ticker) > 62:
            ticker = ticker[:59] + "..."
        self.draw_text(tactical_status, self.fonts.tiny, WHITE, (615, 127))
        self.draw_text(ticker, self.fonts.tiny, GOLD if battle.message_timer > 0 else GRAY, (615, 147))
        self.draw_text("P", self.fonts.tiny, GRAY, (WIDTH - 26, 136), "topright")

        # Ficha completa apenas por hover: remove a redundância sem esconder a
        # informação tática para quem quer comparar as cartas.
        mouse = pygame.mouse.get_pos()
        hovered = next(((key, display, rect) for (key, display), rect in zip(battle.selected, rects) if rect.collidepoint(mouse)), None)
        if hovered:
            key, display, rect = hovered
            data = DEFENSES[key]
            tooltip_x = int(clamp(rect.centerx - 170, 154, WIDTH - 350))
            tooltip = pygame.Rect(tooltip_x, 178, 340, 72)
            self.panel(tooltip, 239, battle.region_color(), 8)
            self.draw_text(display, self.fonts.small, GOLD, (tooltip.x + 13, tooltip.y + 9))
            self.draw_wrapped(data["ability"], self.fonts.tiny, WHITE, pygame.Rect(tooltip.x + 13, tooltip.y + 29, tooltip.width - 26, 35), 2)
        elif battle.core_rect().collidepoint(mouse):
            tooltip = pygame.Rect(365, 178, 362, 58)
            self.panel(tooltip, 239, GOLD, 8)
            self.draw_text("N3", self.fonts.small, GOLD, (tooltip.x + 13, tooltip.y + 9))
            self.draw_text("Prêmio do chefe: ascende uma defesa por 18 s e recarrega a munição.", self.fonts.tiny, WHITE, (tooltip.x + 13, tooltip.y + 30))

    def defender_sprite(self, battle: Battle, defender: Defender) -> pygame.Surface:
        """Fonte visual da defesa ativa e da animação de derrota."""
        return self.card_sprite(battle.region, defender.key, defender.sprite_index)

    def enemy_sprite(self, battle: Battle, enemy: Enemy) -> pygame.Surface:
        """Fonte visual do inimigo, centralizando os retratos especiais."""
        if enemy.is_boss:
            frames = self.assets.animation_frames.get(f"{battle.region}_boss_actions", [])
            if len(frames) >= 12:
                boss_row = REGIONS[battle.region]["bosses"].index(enemy.key)
                row_frames = frames[boss_row * 4:boss_row * 4 + 4]
                if enemy.motion.state == "skill":
                    return row_frames[3]
                if enemy.motion.state == "attack":
                    return row_frames[2]
                if enemy.motion.state in {"hit", "stunned"}:
                    return row_frames[1]
                return row_frames[enemy.motion.phase(fps=4.6, frames=2)]
        sheet_key = {
            ("city", "caminhante"): "city_walker_walk",
            ("desert", "digger"): "desert_digger_states",
            ("beach", "nadador"): "beach_swimmer_walk",
        }.get((battle.region, enemy.key))
        if sheet_key:
            frames = self.assets.animation_frames.get(sheet_key, [])
            if frames:
                if enemy.key == "digger" and enemy.motion.state == "walk":
                    frame_index = enemy.motion.phase(fps=5.5, frames=2)
                elif enemy.key == "digger" and enemy.motion.state == "dig_enter":
                    frame_index = min(4, 2 + int(enemy.motion.state_elapsed / 0.16))
                elif enemy.key == "digger" and enemy.motion.state == "dig_tunnel":
                    frame_index = 4
                elif enemy.key == "digger" and enemy.motion.state == "dig_emerge":
                    frame_index = 5
                elif enemy.key == "digger" and enemy.motion.state == "attack":
                    frame_index = 6
                elif enemy.motion.state == "walk":
                    frame_index = enemy.motion.phase(fps=10.0, frames=len(frames))
                elif enemy.motion.state == "attack":
                    frame_index = 2
                elif enemy.motion.state in {"hit", "stunned"}:
                    frame_index = 4
                else:
                    frame_index = 0
                return frames[frame_index % len(frames)]
        if enemy.key == "saltador" and "zombie_jumper_beta3" in self.assets.images:
            return self.assets.images["zombie_jumper_beta3"]
        if enemy.key == "rastejante" and battle.region == "city" and "zombie_crawler_beta3" in self.assets.images:
            return self.assets.images["zombie_crawler_beta3"]
        return self.assets.zombie(battle.region, int(enemy.data["sprite"]))

    def draw_actor_sprite(
        self,
        sprite: pygame.Surface,
        x: float,
        ground_y: float,
        width: float,
        height: float,
        motion: ActorMotion,
        *,
        enemy: bool,
        vertical_offset: float = 0.0,
        alpha: int = 255,
        progress: float = 0.0,
        state_override: str | None = None,
        profile: str = "generic",
    ) -> pygame.Rect:
        """Desenha uma pose articulada preservando os pés no terreno real."""
        if sprite.get_width() <= 1:
            return pygame.Rect(int(x), int(ground_y), 1, 1)
        sprite = self.assets.trimmed(sprite)
        action_progress = clamp(float(progress), 0.0, 1.0)
        if action_progress <= 0.0 and motion.event_left > 0:
            action_progress = clamp(
                motion.state_elapsed / max(0.001, motion.state_elapsed + motion.event_left),
                0.0,
                1.0,
            )
        if self.presenter is not None:
            self.actor_commands.append(
                ActorCommand(
                    sprite=sprite,
                    x=float(x),
                    ground_y=float(ground_y),
                    width=max(1.0, float(width)),
                    height=max(1.0, float(height)),
                    state=state_override or motion.state,
                    elapsed=motion.state_elapsed,
                    enemy=enemy,
                    vertical_offset=vertical_offset,
                    alpha=max(0, min(255, int(alpha))),
                    hit_flash=motion.hit_flash,
                    progress=action_progress,
                    profile=profile,
                )
            )
            return pygame.Rect(
                int(x - width / 2),
                int(ground_y + vertical_offset - height),
                max(1, int(width)),
                max(1, int(height)),
            )
        dx, dy, angle, scale_x, scale_y = actor_pose(
            motion,
            enemy=enemy,
            profile=profile,
            progress=action_progress,
        )
        size = (max(1, int(width * scale_x)), max(1, int(height * scale_y)))
        rendered = pygame.transform.rotate(self.assets.scaled(sprite, *size), angle)
        if alpha < 255:
            rendered.set_alpha(max(0, alpha))
        if motion.hit_flash > 0:
            flash_alpha = int(105 * clamp(motion.hit_flash / 0.13, 0.0, 1.0))
            flash = pygame.Surface(rendered.get_size(), pygame.SRCALPHA)
            flash.fill((255, 238, 210, flash_alpha))
            rendered.blit(flash, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        rect = rendered.get_rect(midbottom=(int(x + dx), int(ground_y + dy + vertical_offset)))
        self.screen.blit(rendered, rect)
        return rect

    def draw_fallen(self, battle: Battle) -> None:
        """Mostra uma queda curta antes de a silhueta sumir em partículas."""
        for fallen in battle.fallen:
            progress = clamp(fallen.elapsed / max(0.01, fallen.duration), 0.0, 1.0)
            alpha = int(255 * (1.0 - progress))
            motion = ActorMotion(state="dead", state_elapsed=fallen.elapsed, event_left=fallen.duration)
            self.draw_actor_sprite(
                fallen.sprite,
                fallen.x,
                fallen.y,
                fallen.width,
                fallen.height,
                motion,
                enemy=fallen.enemy,
                alpha=alpha,
                progress=progress,
            )

    def draw_visual_effects(self, battle: Battle) -> None:
        """Exibe somente quadros rasterizados de matéria e impacto reais."""
        styles = {
            "flame_impact": ("elemental_effects", 0, 118, 92),
            "water_impact": ("elemental_effects", 1, 132, 88),
            "toxic_impact": ("elemental_effects", 2, 126, 96),
            "toxic_wave": ("elemental_effects", 2, 212, 136),
            "ground_slam": ("ability_effects", 0, 236, 126),
            "arcane_cast": ("ability_effects", 1, 164, 174),
            "tidal_surge": ("ability_effects", 2, 260, 142),
            "explosion": ("combat_effects", 2, 184, 146),
            "ballistic_impact": ("combat_effects", 0, 92, 66),
        }
        for effect in battle.effects:
            # O gesto do Comandante já está no quadro de habilidade do próprio
            # chefe; um anel desenhado por cima voltaria a ser um substituto.
            if effect.kind == "command_aura":
                continue
            progress = clamp(effect.elapsed / max(0.01, effect.duration), 0.0, 1.0)
            stage = min(3, int(progress * 4.0))
            sheet, row, base_width, base_height = styles.get(
                effect.kind,
                ("combat_effects", 2, 184, 146),
            )
            growth = 0.80 + progress * 0.36
            fade = 1.0 - clamp((progress - 0.72) / 0.28, 0.0, 1.0)
            self.blit_effect_frame(
                sheet,
                row,
                stage,
                effect.x,
                effect.y,
                base_width * effect.scale * growth,
                base_height * effect.scale * growth,
                alpha=int(255 * fade),
            )

    def blit_effect_frame(
        self,
        sheet: str,
        row: int,
        stage: int,
        x: float,
        y: float,
        width: float,
        height: float,
        *,
        alpha: int = 255,
        angle: float = 0.0,
        midbottom: bool = False,
    ) -> pygame.Rect | None:
        """Desenha um quadro pré-pintado; jamais fabrica um símbolo geométrico."""
        frames = self.assets.effect_frames.get(sheet, [])
        index = row * 4 + max(0, min(3, int(stage)))
        if index >= len(frames) or frames[index].get_width() <= 1:
            return None
        rendered = self.assets.scaled(frames[index], width, height)
        if angle:
            rendered = pygame.transform.rotate(rendered, angle)
        elif alpha < 255:
            rendered = rendered.copy()
        if alpha < 255:
            rendered.set_alpha(max(0, min(255, int(alpha))))
        if midbottom:
            rect = rendered.get_rect(midbottom=(int(x), int(y)))
        else:
            rect = rendered.get_rect(center=(int(x), int(y)))
        self.screen.blit(rendered, rect)
        return rect

    @staticmethod
    def eased(value: float) -> float:
        """Curva suave usada por mãos, carregadores e munição visível."""
        value = clamp(value, 0.0, 1.0)
        return value * value * (3.0 - 2.0 * value)

    def draw_reload_action(
        self,
        defender: Defender,
        rect: pygame.Rect,
        scale: tuple[float, float],
        depth: float,
        progress: float,
    ) -> None:
        """Mostra a troca física de munição sem palavra, relógio ou ícone.

        A mão sai da arma, alcança o cinto, carrega um pente/cartucho/cilindro
        e o encaixa no equipamento. A barra de munição existente é o único
        indicador abstrato; todo o restante é movimento corporal.
        """
        # A Beta 4 executa esse gesto na malha corporal OpenGL. O antigo braço
        # de linhas e o carregador geométrico não devem voltar a ser exibidos.
        return
        role = str(defender.stats.get("role", ""))
        if role in {"radio", "promoter", "barrier", "mine"}:
            return
        p = clamp(progress, 0.0, 1.0)
        x, y = defender.x, defender.y
        shoulder = (x + 2 * depth, y - scale[1] * 0.61)
        receiver = (x + 22 * depth, y - scale[1] * 0.50)
        pocket = (x - 7 * depth, y - scale[1] * 0.29)

        if p < 0.22:
            q = self.eased(p / 0.22)
            hand = (lerp(receiver[0], pocket[0], q), lerp(receiver[1], pocket[1], q))
        elif p < 0.44:
            q = self.eased((p - 0.22) / 0.22)
            hand = (pocket[0] - 2 * depth, pocket[1] + math.sin(q * math.pi) * 3 * depth)
        elif p < 0.78:
            q = self.eased((p - 0.44) / 0.34)
            hand = (lerp(pocket[0], receiver[0], q), lerp(pocket[1], receiver[1], q))
        else:
            q = self.eased((p - 0.78) / 0.22)
            rest = (x + 10 * depth, y - scale[1] * 0.52)
            hand = (lerp(receiver[0], rest[0], q), lerp(receiver[1], rest[1], q))

        elbow = (
            lerp(shoulder[0], hand[0], 0.52) - 4 * depth,
            lerp(shoulder[1], hand[1], 0.52) + 7 * depth,
        )
        sleeve = {
            "city": (46, 69, 67),
            "desert": (135, 105, 65),
            "beach": (32, 72, 92),
        }[defender.region]
        pygame.draw.line(self.screen, sleeve, shoulder, elbow, max(2, int(6 * depth)))
        pygame.draw.line(self.screen, sleeve, elbow, hand, max(2, int(5 * depth)))
        pygame.draw.circle(self.screen, (198, 152, 111), (int(hand[0]), int(hand[1])), max(2, int(4 * depth)))

        # O objeto aparece apenas depois de ser retirado do cinto e desaparece
        # dentro da arma na fase de encaixe.
        if 0.30 <= p <= 0.84:
            alpha = int(255 * min(1.0, (p - 0.30) / 0.08, (0.84 - p) / 0.08))
            item = pygame.Surface((max(8, int(15 * depth)), max(10, int(24 * depth))), pygame.SRCALPHA)
            if role == "shotgun":
                for offset in (3, 8):
                    pygame.draw.rect(item, (172, 42, 38, alpha), (offset, 2, 4, item.get_height() - 4), border_radius=2)
                    pygame.draw.line(item, (238, 187, 72, alpha), (offset, 2), (offset + 3, 2), 2)
            elif role in {"mortar", "grenade"}:
                pygame.draw.ellipse(item, (91, 104, 69, alpha), (2, 1, item.get_width() - 4, item.get_height() - 2))
                pygame.draw.line(item, (231, 184, 78, alpha), (2, item.get_height() // 2), (item.get_width() - 2, item.get_height() // 2), 2)
            elif role in {"flame", "poison", "waterjet"}:
                canister = {
                    "flame": (207, 93, 43, alpha),
                    "poison": (91, 175, 74, alpha),
                    "waterjet": (67, 177, 220, alpha),
                }[role]
                pygame.draw.rect(item, canister, (2, 2, item.get_width() - 4, item.get_height() - 4), border_radius=4)
                pygame.draw.line(item, (225, 236, 228, alpha), (3, 6), (item.get_width() - 3, 6), 2)
            else:
                pygame.draw.rect(item, (48, 55, 55, alpha), (2, 1, item.get_width() - 4, item.get_height() - 2), border_radius=2)
                pygame.draw.line(item, (151, 165, 160, alpha), (4, 5), (item.get_width() - 4, 5), 2)
            rotated = pygame.transform.rotate(item, -18 + p * 26)
            self.screen.blit(rotated, rotated.get_rect(center=(int(hand[0] + 3 * depth), int(hand[1] + 5 * depth))))

    def draw_weapon_action(
        self,
        defender: Defender,
        rect: pygame.Rect,
        scale: tuple[float, float],
        depth: float,
    ) -> None:
        """Detalhe mecânico do disparo que não existe no retrato estático."""
        # O lançamento está no estado de ataque e o obus real aparece na folha
        # de projéteis. Não desenhar braços ou munição com primitivas.
        return
        if defender.stats.get("role") != "mortar":
            return
        total = max(0.001, defender.motion.state_elapsed + defender.motion.event_left)
        p = clamp(defender.motion.state_elapsed / total, 0.0, 1.0)
        q = self.eased(clamp(p / 0.72, 0.0, 1.0))
        start = (defender.x - 10 * depth, defender.y - scale[1] * 0.45)
        tube = (defender.x + 18 * depth, defender.y - scale[1] * 0.30)
        shell_x = lerp(start[0], tube[0], q)
        shell_y = lerp(start[1], tube[1], q) - math.sin(q * math.pi) * 13 * depth
        shoulder = (defender.x, defender.y - scale[1] * 0.60)
        hand = (shell_x - 2 * depth, shell_y)
        pygame.draw.line(self.screen, (87, 89, 69), shoulder, hand, max(2, int(5 * depth)))
        shell = pygame.Surface((max(7, int(11 * depth)), max(12, int(23 * depth))), pygame.SRCALPHA)
        pygame.draw.ellipse(shell, (101, 116, 73, 255), shell.get_rect())
        pygame.draw.line(shell, GOLD, (2, shell.get_height() // 2), (shell.get_width() - 2, shell.get_height() // 2), 2)
        self.screen.blit(shell, shell.get_rect(center=(int(shell_x), int(shell_y))))

    def draw_defender(self, defender: Defender) -> None:
        assert self.battle is not None
        battle = self.battle
        x, y = defender.x, defender.y
        role = defender.stats["role"]
        scale = defender_render_scale(defender)
        depth = lane_depth(battle.region, defender.row)
        shadow_width = max(28, int(scale[0] * (0.82 if role in {"barrier", "boat", "sub"} else 0.68)))
        shadow_height = max(6, int(13 * depth))
        shadow = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
        if battle.cell_is_water(defender.row, defender.col):
            pygame.draw.ellipse(shadow, (90, 220, 235, 105), shadow.get_rect(), width=2)
            pygame.draw.ellipse(shadow, (7, 36, 52, 85), shadow.get_rect().inflate(-10, -4))
        else:
            pygame.draw.ellipse(shadow, (0, 0, 0, 100), shadow.get_rect())
        self.screen.blit(shadow, shadow.get_rect(midbottom=(int(x), int(y + 3))))
        # A mesma fonte de arte atende carta, campo e queda. A pose em si
        # muda conforme o estado emitido pela lógica de combate.
        sprite = self.defender_sprite(battle, defender)
        reload_progress = (
            1.0 - defender.reload_timer / max(0.01, defender.reload_total)
            if defender.reloading
            else 0.0
        )
        rect = self.draw_actor_sprite(
            sprite,
            x,
            y,
            *scale,
            defender.motion,
            enemy=False,
            progress=reload_progress,
            profile=defender_animation_profile(defender),
        )
        world_target = self.screen
        if self.overlay_surface is not None:
            self.screen = self.overlay_surface
        if defender.motion.state == "attack":
            total = max(0.001, defender.motion.state_elapsed + defender.motion.event_left)
            attack_progress = clamp(defender.motion.state_elapsed / total, 0.0, 1.0)
            stage = min(3, int(attack_progress * 4.0))
            muzzle = (rect.right - 2, rect.centery - int(6 * depth))
            if role in {"flame", "waterjet", "poison"}:
                row = {"flame": 0, "waterjet": 1, "poison": 2}[role]
                self.blit_effect_frame(
                    "elemental_effects", row, min(2, stage), *muzzle,
                    58 * depth, 42 * depth,
                )
            elif role not in {"radio", "promoter", "barrier", "mine"}:
                row = 1 if role == "shotgun" else 0
                self.blit_effect_frame(
                    "combat_effects", row, stage, *muzzle,
                    (94 if role == "shotgun" else 68) * depth,
                    (62 if role == "shotgun" else 46) * depth,
                )
        if defender.corrosion > 0:
            self.blit_effect_frame(
                "elemental_effects", 2, int(defender.corrosion * 5.0) % 4,
                x, y - scale[1] * 0.38, scale[0] * 0.72, scale[1] * 0.62,
                alpha=168,
            )
        bar_width = max(42, int(76 * depth))
        self.health_bar(x - bar_width / 2, y + 7, bar_width, defender.hp / defender.max_hp, (89, 214, 144))
        if defender.max_ammo:
            ammo_width = max(34, int(60 * depth))
            ammo_ratio = (
                1.0 - defender.reload_timer / max(0.01, defender.reload_total)
                if defender.reloading
                else defender.ammo / max(1, defender.max_ammo)
            )
            self.ammo_bar(x - ammo_width / 2, y + 16, ammo_width, ammo_ratio)
        self.screen = world_target

    def draw_enemy(self, enemy: Enemy) -> None:
        assert self.battle is not None
        battle = self.battle
        water_enemy = battle.region == "beach" and enemy.row in battle.water_rows
        scale = enemy_render_scale(enemy, battle.region)
        depth = lane_depth(battle.region, enemy.row)
        shadow_width = max(28, int(scale[0] * (0.86 if enemy.is_boss else 0.68)))
        shadow_height = max(6, int(13 * depth))
        shadow = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
        if water_enemy:
            pygame.draw.ellipse(shadow, (91, 221, 238, 112), shadow.get_rect(), width=2)
            pygame.draw.ellipse(shadow, (8, 37, 50, 88), shadow.get_rect().inflate(-10, -4))
        else:
            pygame.draw.ellipse(shadow, (0, 0, 0, 115), shadow.get_rect())
        self.screen.blit(shadow, shadow.get_rect(midbottom=(int(enemy.x), int(enemy.y + 3))))
        sprite = self.enemy_sprite(battle, enemy)

        vertical_offset = 0.0
        alpha = 255
        top, bottom = lane_bounds(battle.region, enemy.row)
        lane_height = bottom - top
        if enemy.jump_state:
            progress = clamp(1.0 - enemy.jump_timer / max(0.01, enemy.jump_duration), 0.0, 1.0)
            vertical_offset = -math.sin(progress * math.pi) * lane_height * 0.78
        elif enemy.dig_state == "enter":
            progress = clamp(1.0 - enemy.dig_timer / max(0.01, enemy.dig_duration), 0.0, 1.0)
            vertical_offset = lane_height * 0.42 * progress
            alpha = int(255 * (1.0 - progress * 0.42))
        elif enemy.dig_state == "emerge":
            progress = clamp(1.0 - enemy.dig_timer / max(0.01, enemy.dig_duration), 0.0, 1.0)
            vertical_offset = lane_height * 0.42 * (1.0 - progress)
            alpha = int(146 + 109 * progress)
        state_override = (
            "swim"
            if water_enemy and enemy.motion.state == "walk"
            else None
        )
        rect = self.draw_actor_sprite(
            sprite,
            enemy.x,
            enemy.y,
            *scale,
            enemy.motion,
            enemy=True,
            vertical_offset=vertical_offset,
            alpha=alpha,
            state_override=state_override,
            profile=enemy_animation_profile(enemy),
        )
        world_target = self.screen
        if self.overlay_surface is not None:
            self.screen = self.overlay_surface
        if enemy.burn > 0:
            self.blit_effect_frame(
                "elemental_effects", 0, int(enemy.age * 11.0) % 4,
                enemy.x, enemy.y + 1, scale[0] * 0.94, scale[1] * 0.78,
                alpha=205, midbottom=True,
            )
        if enemy.poisoned > 0:
            self.blit_effect_frame(
                "elemental_effects", 2, int(enemy.age * 8.0) % 4,
                enemy.x, enemy.y - scale[1] * 0.42,
                scale[0] * 1.04, scale[1] * 0.72, alpha=176,
            )
        if enemy.soaked > 0:
            self.blit_effect_frame(
                "elemental_effects", 1, int(enemy.age * 9.0) % 4,
                enemy.x, enemy.y + 2, scale[0] * 1.15, scale[1] * 0.58,
                alpha=182, midbottom=True,
            )
        if enemy.corrosion > 0 and enemy.poisoned <= 0:
            self.blit_effect_frame(
                "elemental_effects", 2, int(enemy.age * 7.0) % 4,
                enemy.x, enemy.y - scale[1] * 0.46,
                scale[0] * 0.76, scale[1] * 0.54, alpha=154,
            )
        if "steal" in enemy.tags:
            self.blit_effect_frame(
                "ability_effects", 1, int(enemy.age * 6.0) % 4,
                enemy.x, enemy.y - scale[1] * 0.46,
                scale[0] * 1.28, scale[1] * 1.05, alpha=188,
            )
        width = (104 if enemy.is_boss else 64) * depth
        self.health_bar(enemy.x - width / 2, enemy.y + 7, width, enemy.hp / enemy.max_hp, RED)
        self.screen = world_target

    @staticmethod
    def flow_points(
        start: tuple[float, float],
        end: tuple[float, float],
        elapsed: float,
        amplitude: float,
        count: int = 18,
    ) -> list[tuple[int, int]]:
        """Constrói um jato contínuo ondulado entre bocal e frente do fluxo."""
        dx, dy = end[0] - start[0], end[1] - start[1]
        length = max(1.0, math.hypot(dx, dy))
        normal_x, normal_y = -dy / length, dx / length
        points: list[tuple[int, int]] = []
        for index in range(max(3, count)):
            q = index / max(1, count - 1)
            envelope = math.sin(q * math.pi)
            wave = math.sin(q * math.tau * 2.1 - elapsed * 31.0) * amplitude * envelope
            points.append(
                (
                    int(lerp(start[0], end[0], q) + normal_x * wave),
                    int(lerp(start[1], end[1], q) + normal_y * wave),
                )
            )
        return points

    @staticmethod
    def ribbon_polygon(
        points: list[tuple[int, int]],
        start_width: float,
        end_width: float,
        *,
        taper_tip: bool = False,
    ) -> list[tuple[int, int]]:
        """Cria as duas bordas de um fluxo para evitar o efeito de bolinhas."""
        if len(points) < 2:
            return points
        upper: list[tuple[int, int]] = []
        lower: list[tuple[int, int]] = []
        for index, point in enumerate(points):
            before = points[max(0, index - 1)]
            after = points[min(len(points) - 1, index + 1)]
            dx, dy = after[0] - before[0], after[1] - before[1]
            length = max(1.0, math.hypot(dx, dy))
            normal_x, normal_y = -dy / length, dx / length
            q = index / max(1, len(points) - 1)
            width = lerp(start_width, end_width, q)
            if taper_tip:
                tip = clamp((q - 0.68) / 0.32, 0.0, 1.0)
                smooth_tip = tip * tip * (3.0 - 2.0 * tip)
                width *= lerp(1.0, 0.08, smooth_tip)
            upper.append((int(point[0] + normal_x * width), int(point[1] + normal_y * width)))
            lower.append((int(point[0] - normal_x * width), int(point[1] - normal_y * width)))
        return upper + list(reversed(lower))

    def draw_elemental_stream(self, projectile: Projectile, x: float, y: float) -> None:
        """Alongamento de um quadro físico de chama, água ou veneno."""
        start_x, start_y = float(projectile.x), float(projectile.y)
        dx, dy = float(x) - start_x, float(y) - start_y
        distance = math.hypot(dx, dy)
        if distance < 3.0:
            return
        progress = clamp(projectile.elapsed / max(0.01, projectile.travel), 0.0, 1.0)
        row = {"flame": 0, "waterjet": 1, "poison": 2}[projectile.kind]
        stage = min(3, int(progress * 4.0))
        height = {"flame": 74.0, "waterjet": 58.0, "poison": 70.0}[projectile.kind]
        angle = -math.degrees(math.atan2(dy, dx))
        self.blit_effect_frame(
            "elemental_effects",
            row,
            stage,
            start_x + dx * 0.5,
            start_y + dy * 0.5,
            max(48.0, distance + 42.0),
            height,
            alpha=238,
            angle=angle,
        )

    def draw_projectiles(self, battle: Battle) -> None:
        projectile_art = {
            "rifle": (0, 0, 30, 9),
            "tracer": (0, 0, 27, 8),
            "shotgun": (0, 1, 28, 13),
            "sniper": (0, 2, 38, 10),
            "fuzileiro": (0, 3, 34, 10),
            "boat": (0, 3, 34, 10),
            "turret": (0, 3, 32, 10),
            "grenade": (1, 0, 28, 28),
            "mortar": (1, 1, 38, 24),
            "bazooka": (1, 2, 48, 22),
            "torpedo": (1, 3, 52, 23),
            "acid": (2, 0, 34, 24),
            "enemy_bullet": (2, 1, 31, 12),
            "drone": (2, 2, 38, 18),
        }
        for projectile in battle.projectiles:
            if projectile.elapsed < 0:
                continue
            t = clamp(projectile.elapsed / projectile.travel, 0, 1)
            x = lerp(projectile.x, projectile.target_x, t)
            y = lerp(projectile.y, projectile.target_y, t) - (math.sin(t * math.pi) * 46 if projectile.kind in {"grenade", "mortar", "bazooka"} else 0)
            if projectile.kind in {"flame", "poison", "waterjet"}:
                self.draw_elemental_stream(projectile, x, y)
                continue
            art = projectile_art.get(projectile.kind)
            if not art:
                continue
            row, column, width, height = art
            next_t = min(1.0, t + 0.025)
            next_x = lerp(projectile.x, projectile.target_x, next_t)
            next_y = lerp(projectile.y, projectile.target_y, next_t) - (
                math.sin(next_t * math.pi) * 46
                if projectile.kind in {"grenade", "mortar", "bazooka"}
                else 0
            )
            angle = -math.degrees(math.atan2(next_y - y, next_x - x))
            source_row = int(getattr(projectile.owner, "row", 0))
            depth = lane_depth(battle.region, source_row)
            self.blit_effect_frame(
                "projectile_sprites",
                row,
                column,
                x,
                y,
                width * depth,
                height * depth,
                alpha=176 if projectile.kind == "tracer" else 255,
                angle=angle,
            )

    def draw_particles(self, battle: Battle) -> None:
        # Partículas circulares foram retiradas. Impactos e matéria usam folhas
        # rasterizadas; textos de dano continuam sendo informação de HUD.
        for text in battle.texts:
            self.draw_text(text.text, self.fonts.tiny, text.color, (text.x, text.y), "center", True)

    def draw_battle_status(self) -> None:
        assert self.battle is not None
        battle = self.battle
        if battle.boss_warning > 0:
            banner = pygame.Rect(WIDTH // 2 - 330, 238, 660, 124)
            self.panel(banner, 244, RED, 12)
            self.draw_text("ALERTA: CHEFE CHEGANDO", self.fonts.h1, RED, (banner.centerx, banner.y + 16), "center", True)
            self.draw_text(battle.boss_banner_name, self.fonts.h2, WHITE, (banner.centerx, banner.y + 54), "center", True)
            self.draw_text(battle.boss_banner_subtitle, self.fonts.small, GOLD, (banner.centerx, banner.y + 85), "center")
        if battle.paused:
            veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            veil.fill((3, 8, 12, 132))
            self.screen.blit(veil, (0, 0))
            pause_card = pygame.Rect(WIDTH // 2 - 205, HEIGHT // 2 - 74, 410, 148)
            self.panel(pause_card, 246, GOLD, 12)
            self.draw_text("PAUSADO", self.fonts.title, GOLD, (pause_card.centerx, pause_card.y + 23), "center", True)
            self.draw_text("Clique em PAUSA ou pressione P para continuar.", self.fonts.small, WHITE, (pause_card.centerx, pause_card.y + 86), "center")

    def draw_result_overlay(self) -> None:
        assert self.battle is not None
        battle = self.battle
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((3, 6, 9, 188))
        self.screen.blit(overlay, (0, 0))
        heading = "REGIÃO PROTEGIDA" if battle.victory else "BASE INVADIDA"
        color = GOLD if battle.victory else RED
        self.panel(pygame.Rect(WIDTH // 2 - 265, HEIGHT // 2 - 130, 530, 285), 242, color, 16)
        self.draw_text(heading, self.fonts.title, color, (WIDTH / 2, HEIGHT / 2 - 85), "center", True)
        body = "Você venceu as 15 ondas. Todos os territórios continuam disponíveis para escolher sua próxima missão." if battle.victory else "Um infectado atravessou a linha final. Refaça a equipe e preserve munição para as ondas finais."
        self.draw_wrapped(body, self.fonts.body, WHITE, pygame.Rect(WIDTH // 2 - 205, HEIGHT // 2 - 30, 410, 55), 3, center=True)
        self.draw_text(f"Onda alcançada: {battle.wave}/15", self.fonts.small, GRAY, (WIDTH / 2, HEIGHT // 2 + 46), "center")
        self.button("VOLTAR AO MAPA", pygame.Rect(WIDTH // 2 - 145, HEIGHT // 2 + 100, 290, 50), color)

    def health_bar(self, x: float, y: float, width: float, ratio: float, color: tuple[int, int, int]) -> None:
        rect = pygame.Rect(int(x), int(y), int(width), 6)
        pygame.draw.rect(self.screen, (22, 26, 28), rect, border_radius=3)
        pygame.draw.rect(self.screen, color, (rect.x, rect.y, int(rect.width * clamp(ratio, 0, 1)), rect.height), border_radius=3)

    def ammo_bar(self, x: float, y: float, width: float, ratio: float) -> None:
        rect = pygame.Rect(int(x), int(y), int(width), 4)
        pygame.draw.rect(self.screen, (19, 28, 33), rect, border_radius=2)
        pygame.draw.rect(self.screen, TEAL, (rect.x, rect.y, int(rect.width * clamp(ratio, 0, 1)), rect.height), border_radius=2)

    def blit_sprite(self, sprite: pygame.Surface, x: float, y: float, width: float, height: float) -> None:
        if sprite.get_width() <= 1:
            return
        scaled = self.assets.scaled(sprite, width, height)
        self.screen.blit(scaled, (int(x), int(y)))

    def card_sprite(self, region: str, key: str, index: int) -> pygame.Surface:
        """Escolhe a silhueta da carta e do objeto já posicionado.

        Minas recebem sprites individuais onde a leitura do cenário importa:
        cidade usa duas cargas urbanas limpas, Praia usa duas minas de areia e
        a Bomba de Água é uma mina naval independente, sem plataforma.
        """
        custom_asset = CARD_ART_ASSETS.get((region, key))
        if custom_asset:
            return self.assets.images[custom_asset]
        terrain_mine_assets = {
            "city": {"mina": "city_mine_n1", "mina_segura": "city_mine_n2"},
            "beach": {"mina": "beach_mine_land_n1", "mina_segura": "beach_mine_land_n2"},
        }
        if key == "atirador_lancha":
            return self.assets.images["beach_boat_shooter"]
        asset_key = terrain_mine_assets.get(region, {}).get(key)
        if asset_key:
            return self.assets.images[asset_key]
        if key == "bomba_agua":
            return self.assets.images["beach_mine_water"]
        if DEFENSES.get(key, {}).get("water_only"):
            water_index = {"lancha": 5, "submarino": 6}[key]
            return self.assets.base_unit("beach", water_index)
        level = int(DEFENSES.get(key, {}).get("level", 1))
        return self.assets.unit(region, regional_sprite_index(region, key), level)

    @staticmethod
    def card_metrics(data: dict) -> tuple[str, str]:
        """Converte a função em dois números úteis para a face da carta.

        A descrição continua no hover/dossiê. Aqui entram apenas estatísticas
        que o jogador usa para decidir rápido entre custo, alcance, munição,
        cura, recarga e contenção.
        """
        role = str(data["role"])
        level = int(data["level"])
        if role == "radio":
            gain = 14 if level == 1 else 28
            return f"SUP +{gain}", f"CICLO {float(data['cooldown']):.1f}s"
        if role == "waterjet":
            return f"DANO {int(data['damage'])}", f"LENTO 32% • ALC {int(data['range'])}"
        if role == "poison":
            return f"DANO {int(data['damage'])}", f"VENENO 4.2s • ALC {int(data['range'])}"
        if role == "promoter":
            return "PROMOVE N1→N2", f"CICLO {int(data['cooldown'])}s"
        if role == "barrier":
            return f"HP {int(data['hp'])}", "EXPLODE" if level >= 2 else "BLOQUEIO"
        if role == "mine":
            area = "ÁREA" if data.get("water_only") else ("SEGURA" if level >= 2 else "1 ALVO")
            return f"DANO {int(data['damage'])}", area
        reload_time = weapon_reload_seconds(data)
        reload_label = f" • REC {reload_time:.0f}s" if reload_time else ""
        return f"DANO {int(data['damage'])}", f"MUN {int(data['ammo'])}{reload_label}"

    def draw_wrapped(self, text: str, font: pygame.font.Font, color: tuple[int, int, int], rect: pygame.Rect, lines: int, center: bool = False) -> None:
        words = text.split()
        built: list[str] = []
        current = ""
        for word in words:
            candidate = word if not current else current + " " + word
            if font.size(candidate)[0] <= rect.width:
                current = candidate
            else:
                built.append(current)
                current = word
        if current:
            built.append(current)
        for index, line in enumerate(built[:lines]):
            y = rect.y + index * (font.get_height() + 2)
            anchor = "midtop" if center else "topleft"
            x = rect.centerx if center else rect.x
            self.draw_text(line, font, color, (x, y), anchor)

    def draw(self) -> None:
        # Atores OpenGL ficam entre o mundo e o HUD. A cada quadro as duas
        # superfícies são reconstruídas; nenhuma animação deixa rastros.
        self.screen = self.world_surface
        self.world_surface.fill((0, 0, 0, 255))
        self.actor_commands.clear()
        if self.overlay_surface is not None:
            self.overlay_surface.fill((0, 0, 0, 0))
        if self.scene == "loading":
            self.draw_loading()
        elif self.scene == "title":
            self.draw_title()
        elif self.scene == "difficulty":
            self.draw_difficulty()
        elif self.scene == "campaign":
            self.draw_campaign()
        elif self.scene == "select":
            self.draw_selection()
        elif self.scene == "howto":
            self.draw_howto()
        elif self.scene.startswith("dossier"):
            self.draw_dossier()
        elif self.scene == "battle" and self.battle:
            self.draw_battle()


if __name__ == "__main__":
    Game().run()

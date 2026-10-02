import math
import random
import pygame

from core.base import Base

WIDTH, HEIGHT = 1280, 720
LANES, COLS = 5, 9
BOARD_X, BOARD_Y = 190, 176
CELL_W, CELL_H = 103, 86
BOARD_W, BOARD_H = COLS * CELL_W, LANES * CELL_H
BASE_X = 82
ZOMBIE_START_X = BOARD_X + BOARD_W + 42
MAX_WAVES = 15
START_SUPPLIES = 50
MAX_SUPPLIES = 600
SUPPLY_DROP_INTERVAL = 10.0
MAX_SELECTED_CARDS = 7
TOOL_RECT = pygame.Rect(10, 94, 90, 64)

FONT = "Arial"
WHITE = (244, 244, 234)
BLACK = (15, 17, 15)
PANEL = (24, 28, 27)
PANEL2 = (37, 43, 40)
PANEL3 = (56, 63, 58)
BORDER = (116, 126, 116)
TEXT = (224, 228, 218)
YELLOW = (246, 202, 62)
RED = (211, 56, 53)
RED_DARK = (135, 36, 37)
GREEN = (75, 184, 86)
BLUE = (66, 121, 184)
CYAN = (70, 176, 196)
ORANGE = (196, 106, 44)
PURPLE = (135, 80, 150)
SAND = (201, 174, 101)
STEEL = (109, 119, 116)
STEEL_LIGHT = (178, 184, 176)
STEEL_DARK = (45, 52, 49)
WOOD = (120, 79, 45)
WOOD_LIGHT = (164, 114, 63)
WOOD_DARK = (64, 43, 29)
SKIN = (197, 153, 111)
SKIN_LIGHT = (228, 189, 150)
SKIN_DARK = (122, 79, 52)
UNIFORM = (62, 83, 62)
UNIFORM_LIGHT = (94, 119, 83)
UNIFORM_DARK = (33, 47, 35)
MEDIC_RED = (211, 54, 60)
GRENADE = (77, 88, 67)
GRENADE_LIGHT = (174, 182, 144)
ZOMBIE_DARK = (54, 75, 53)

PHASES = {
    "grass": {
        "name": "FRONTE VERDE", "subtitle": "Operação Último Posto", "color": (80, 143, 70),
        "water_lane": None, "special": [], "ambience": "grass",
    },
    "snow": {
        "name": "PORTO CONGELADO", "subtitle": "Temperatura crítica", "color": (153, 191, 205),
        "water_lane": None, "special": ["cryo_operator"], "ambience": "snow",
    },
    "desert": {
        "name": "DESERTO VERMELHO", "subtitle": "Areia, calor e emboscadas", "color": (196, 143, 78),
        "water_lane": None, "special": ["mortar", "scout_buggy"], "ambience": "desert",
    },
    "water": {
        "name": "ZONA MARÍTIMA", "subtitle": "A linha central é ÁGUA", "color": (63, 143, 171),
        "water_lane": 2, "special": ["patrol_boat", "submarine", "water_bomb"], "ambience": "water",
    },
}

# Every new unit has its own mechanical identity rather than simply being a stronger copy.
SOLDIER_DATA = {
    "rifleman": {"name": "FUZILEIRO", "cost": 25, "hp": 120, "role": "SUPRIMENTOS", "color": UNIFORM, "phase": None},
    "lieutenant": {"name": "TENENTE", "cost": 100, "hp": 150, "role": "1 BALA", "color": (40, 70, 45), "phase": None},
    "general": {"name": "GENERAL", "cost": 150, "hp": 250, "role": "2 BALAS", "color": ORANGE, "phase": None},
    "vanguard": {"name": "VANGUARDA", "cost": 50, "hp": 470, "role": "ESCUDO", "color": UNIFORM_DARK, "phase": None},
    "bomber": {"name": "HOMEM-BOMBA", "cost": 200, "hp": 125, "role": "DETONAÇÃO", "color": RED, "phase": None},
    "sniper": {"name": "SNIPER", "cost": 225, "hp": 110, "role": "PRECISÃO", "color": (52, 72, 55), "phase": None},
    "grenadier": {"name": "GRANADEIRO", "cost": 275, "hp": 155, "role": "ÁREA", "color": GRENADE, "phase": None},
    "rambo": {"name": "RAMBO", "cost": 180, "hp": 235, "role": "FACAS", "color": (47, 50, 47), "phase": None},
    "special_forces": {"name": "FORÇAS ESPECIAIS", "cost": 320, "hp": 185, "role": "CAMUFLAGEM", "color": (33, 53, 58), "phase": None},
    "engineer": {"name": "ENGENHEIRO", "cost": 210, "hp": 145, "role": "TORRETA", "color": (130, 99, 53), "phase": None},
    "flamethrower": {"name": "INCENDIÁRIO", "cost": 235, "hp": 160, "role": "FOGO", "color": (142, 57, 36), "phase": None},
    "shotgunner": {"name": "ESCOPETEIRO", "cost": 190, "hp": 155, "role": "CHUMBO", "color": (82, 66, 51), "phase": None},
    "radio_operator": {"name": "OPERADOR DE RÁDIO", "cost": 260, "hp": 125, "role": "ATAQUE AÉREO", "color": (65, 74, 77), "phase": None},
    "drone_operator": {"name": "OPERADOR DE DRONE", "cost": 290, "hp": 135, "role": "DRONE", "color": (57, 72, 78), "phase": None},
    "cryo_operator": {"name": "OPERADOR CRIOGÊNICO", "cost": 240, "hp": 190, "role": "NITROGÊNIO LÍQUIDO", "color": (104, 150, 175), "phase": "snow"},
    "mortar": {"name": "MORTEIRO", "cost": 300, "hp": 130, "role": "ARCO", "color": (111, 88, 57), "phase": "desert"},
    "scout_buggy": {"name": "BUGGY DO DESERTO", "cost": 275, "hp": 260, "role": "ATROPELAR", "color": (148, 109, 56), "phase": "desert"},
    "patrol_boat": {"name": "LANCHA", "cost": 260, "hp": 230, "role": "CANHÃO", "color": (53, 91, 108), "phase": "water"},
    "submarine": {"name": "SUBMARINO", "cost": 340, "hp": 270, "role": "TORPEDO", "color": (55, 68, 74), "phase": "water"},
    "water_bomb": {"name": "BOMBA AQUÁTICA", "cost": 220, "hp": 90, "role": "MINA MARINHA", "color": (50, 101, 128), "phase": "water"},
}

ZOMBIE_DATA = {
    # Arquétipos inspirados nas funções clássicas de tower defense com zumbis,
    # mas com nomes e aparência próprios para o projeto.
    "normal": {"name": "ANDANTE", "hp": 105, "damage": 15, "speed": 18, "cooldown": .9, "reward": 10, "color": (91, 135, 79)},
    "runner": {"name": "CORREDOR", "hp": 62, "damage": 12, "speed": 46, "cooldown": .72, "reward": 18, "color": (133, 86, 68)},
    "brute": {"name": "BRUTO", "hp": 310, "damage": 28, "speed": 11, "cooldown": 1.0, "reward": 30, "color": (111, 83, 132)},
    "crawler": {"name": "RASTEJANTE", "hp": 80, "damage": 17, "speed": 38, "cooldown": .74, "reward": 22, "color": (73, 121, 76)},
    "toxic": {"name": "TÓXICO", "hp": 185, "damage": 21, "speed": 15, "cooldown": .95, "reward": 28, "color": (123, 160, 71)},
    "armored": {"name": "BLINDADO", "hp": 280, "damage": 25, "speed": 13, "cooldown": .95, "reward": 35, "color": (96, 104, 105)},
    "splitter": {"name": "DIVISOR", "hp": 235, "damage": 18, "speed": 12, "cooldown": .9, "reward": 42, "color": (116, 90, 116)},
    "feral": {"name": "FERAL", "hp": 190, "damage": 34, "speed": 25, "cooldown": .7, "reward": 36, "color": (121, 67, 64)},
    "screamer": {"name": "GRITADOR", "hp": 170, "damage": 14, "speed": 17, "cooldown": 1.1, "reward": 38, "color": (166, 123, 68)},
    "spitter": {"name": "CUSPIDOR", "hp": 150, "damage": 18, "speed": 10, "cooldown": 1.3, "reward": 40, "color": (83, 139, 85)},
    "leaper": {"name": "SALTADOR", "hp": 145, "damage": 30, "speed": 32, "cooldown": .85, "reward": 45, "color": (105, 76, 59)},
    "necromancer": {"name": "NECROMANTE", "hp": 330, "damage": 18, "speed": 8, "cooldown": 1.25, "reward": 65, "color": (77, 65, 96)},
    "sandstalker": {"name": "RASTEJANTE DE AREIA", "hp": 205, "damage": 22, "speed": 28, "cooldown": .85, "reward": 48, "color": (165, 129, 80), "phase": "desert"},
    "frostborn": {"name": "NASCIDO DO GELO", "hp": 240, "damage": 24, "speed": 12, "cooldown": .95, "reward": 52, "color": (119, 159, 185), "phase": "snow"},
    "swimmer": {"name": "NADADOR", "hp": 150, "damage": 22, "speed": 33, "cooldown": .8, "reward": 44, "color": (62, 118, 145), "phase": "water"},
    "tide_brute": {"name": "BRUTO DA MARÉ", "hp": 390, "damage": 35, "speed": 10, "cooldown": .95, "reward": 70, "color": (52, 91, 105), "phase": "water"},
    # Novos arquétipos com leitura visual e função próprias.
    "conehead": {"name": "ZUMBI DO CAPACETE", "hp": 210, "damage": 18, "speed": 16, "cooldown": .9, "reward": 25, "color": (108, 126, 79)},
    "flagger": {"name": "PORTA-BANDEIRA", "hp": 120, "damage": 15, "speed": 20, "cooldown": .9, "reward": 32, "color": (164, 74, 58)},
    "door_shield": {"name": "ESCUDO DE PORTA", "hp": 430, "damage": 23, "speed": 8, "cooldown": 1.0, "reward": 55, "color": (84, 87, 83)},
    "vaulting": {"name": "ZUMBI SALTADOR", "hp": 185, "damage": 27, "speed": 24, "cooldown": .82, "reward": 46, "color": (120, 92, 63)},
    "digging": {"name": "ESCAVADOR", "hp": 165, "damage": 20, "speed": 27, "cooldown": .86, "reward": 50, "color": (126, 103, 77), "phase": "desert"},
}


BOSS_DATA = {
    5: {"name": "DOUTOR ZUMBI", "hp": 1450, "damage": 42, "speed": 6.2, "reward": 500, "color": (100, 78, 72)},
    10: {"name": "GENERAL MORTO", "hp": 2200, "damage": 52, "speed": 6.0, "reward": 950, "color": (66, 94, 84)},
    15: {"name": "MUTANTE TITAN", "hp": 3300, "damage": 70, "speed": 5.2, "reward": 1700, "color": (122, 73, 138)},
}


def clamp(value, low, high):
    return max(low, min(high, value))


def txt(surface, content, font, color, pos, center=False):
    image = font.render(content, True, color)
    rect = image.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    surface.blit(image, rect)
    return rect


def panel(surface, rect, fill, border=BORDER, width=2, radius=10):
    pygame.draw.rect(surface, fill, rect, border_radius=radius)
    if border:
        pygame.draw.rect(surface, border, rect, width=width, border_radius=radius)


def health_bar(surface, rect, current, maximum, color=GREEN):
    pygame.draw.rect(surface, BLACK, rect, border_radius=4)
    inner = rect.inflate(-3, -3)
    ratio = 0 if maximum <= 0 else clamp(current / maximum, 0, 1)
    inner.width = int(inner.width * ratio)
    if inner.width:
        pygame.draw.rect(surface, color, inner, border_radius=3)


class FloatingText:
    def __init__(self, content, x, y, color):
        self.content, self.x, self.y, self.color = content, x, y, color
        self.life = 1.0

    def update(self, dt):
        self.life -= dt
        self.y -= 25 * dt

    def draw(self, screen, font):
        if self.life <= 0:
            return
        im = font.render(self.content, True, self.color)
        im.set_alpha(int(255 * clamp(self.life, 0, 1)))
        screen.blit(im, im.get_rect(center=(int(self.x), int(self.y))))


class Shell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.vx, self.vy, self.life = random.uniform(30, 80), random.uniform(-60, -25), .35

    def update(self, dt):
        self.life -= dt
        self.vy += 280 * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, screen):
        if self.life > 0:
            pygame.draw.rect(screen, YELLOW, (int(self.x), int(self.y), 5, 2))


class Explosion:
    def __init__(self, x, y, radius, label=""):
        self.x, self.y, self.radius, self.label = x, y, radius, label
        self.life = .48
        self.max_life = self.life

    def update(self, dt):
        self.life -= dt

    def draw(self, screen, font):
        if self.life <= 0:
            return
        p = 1 - self.life / self.max_life
        r = int(self.radius * (0.25 + p * .9))
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), r, 4)
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), max(4, r // 2), 3)
        if self.label:
            txt(screen, self.label, font, YELLOW, (self.x, self.y - r - 12), True)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, start, target, damage, speed=800, color=YELLOW, effect=None, radius=0):
        super().__init__()
        self.x, self.y = start
        self.target = target
        self.damage_value = damage
        self.speed = speed
        self.effect = effect
        self.radius = radius
        self.image = pygame.Surface((18, 8), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, color, (1, 1, 14, 5))
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def update(self, dt):
        if not self.target.alive():
            self.kill(); return
        tx, ty = self.target.target_point()
        dx, dy = tx - self.x, ty - self.y
        d = math.hypot(dx, dy)
        if d <= self.speed * dt + 6:
            self.target.damage(self.damage_value)
            if self.effect:
                self.effect(self.target)
            self.kill(); return
        if d:
            self.x += dx / d * self.speed * dt
            self.y += dy / d * self.speed * dt
        self.rect.center = (int(self.x), int(self.y))


class MineObject:
    def __init__(self, lane, column, owner):
        self.lane, self.column, self.owner = lane, column, owner
        self.x = BOARD_X + column * CELL_W + CELL_W // 2
        self.y = BOARD_Y + lane * CELL_H + CELL_H // 2 + 20
        self.armed = True
        self.cool = .2

    def update(self, dt, zombies, game):
        if not self.armed:
            return
        self.cool -= dt
        if self.cool > 0:
            return
        for z in list(zombies):
            if z.lane == self.lane and abs(z.x - self.x) < 75:
                for victim in list(zombies):
                    if victim.lane == self.lane and abs(victim.x - self.x) < 150:
                        victim.damage(99999)
                game.effects.append(Explosion(self.x, self.y, 130, "MINA"))
                self.armed = False
                return

    def draw(self, screen):
        pygame.draw.ellipse(screen, (38, 42, 37), (self.x - 24, self.y + 7, 48, 9))
        pygame.draw.circle(screen, STEEL_DARK, (int(self.x), int(self.y)), 20)
        pygame.draw.circle(screen, STEEL, (int(self.x), int(self.y)), 14)
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 4)
        for ang in range(0, 360, 45):
            ex = self.x + math.cos(math.radians(ang)) * 21
            ey = self.y + math.sin(math.radians(ang)) * 21
            pygame.draw.line(screen, STEEL_DARK, (self.x, self.y), (ex, ey), 2)


class Soldier(pygame.sprite.Sprite):
    def __init__(self, lane, column, kind):
        super().__init__()
        data = SOLDIER_DATA[kind]
        self.lane, self.column, self.kind = lane, column, kind
        self.x = BOARD_X + column * CELL_W + CELL_W // 2
        self.y = BOARD_Y + lane * CELL_H + CELL_H // 2
        self.max_hp = data["hp"]
        self.hp = float(self.max_hp)
        self.cost = data["cost"]
        self.attack_timer = random.uniform(.05, .35)
        self.special_timer = 4.0
        self.production_timer = SUPPLY_DROP_INTERVAL
        self.invulnerable_timer = 0.0
        self.burn_timer = 0.0
        self.anim = random.random() * math.tau
        self.flash = 0.0
        self.rect = pygame.Rect(self.x - 38, self.y - 45, 78, 82)

    def alive(self):
        return self.hp > 0

    def damage(self, amount):
        if self.invulnerable_timer > 0:
            return
        self.hp -= amount
        self.flash = .1

    def target_point(self):
        return self.x + 28, self.y - 10

    def find_target(self, zombies, distance=760):
        options = [z for z in zombies if z.lane == self.lane and z.x > self.x and z.x - self.x <= distance]
        return min(options, key=lambda z: z.x - self.x) if options else None

    def _burn(self, target):
        target.burn_timer = max(target.burn_timer, 2.5)

    def update(self, dt, zombies, projectiles, game):
        self.anim += dt * 3
        self.attack_timer -= dt
        self.special_timer -= dt
        self.production_timer -= dt
        self.flash -= dt
        self.invulnerable_timer -= dt

        if self.kind == "rifleman":
            if self.production_timer <= 0:
                game.supply_drops.append((self.lane, self.x + random.randint(-14, 14)))
                self.production_timer = SUPPLY_DROP_INTERVAL
                game.float_text("+25 SUP", self.x, self.y - 48, YELLOW)
            return

        target = self.find_target(zombies)

        if self.kind == "vanguard":
            return

        if self.kind == "bomber":
            blockers = [z for z in zombies if z.lane == self.lane and self.x < z.x < self.x + 58]
            if blockers:
                for z in list(zombies):
                    if z.lane == self.lane and abs(z.x - self.x) <= 155:
                        z.damage(99999)
                game.effects.append(Explosion(self.x, self.y, 160, "BOOM"))
                self.kill()
            else:
                self.x = min(self.x + 30 * dt, ZOMBIE_START_X - 20)
                self.rect.center = (int(self.x), int(self.y))
            return

        if self.kind == "rambo":
            target = next((z for z in zombies if z.lane == self.lane and 0 <= z.x - self.x <= 83), None)
            if target and self.attack_timer <= 0:
                target.damage(28)
                game.add_slash(self.x + 37, self.y - 14)
                target.damage(18)  # second knife hit, not an automatic bullet upgrade
                self.attack_timer = .52
            return

        if self.kind == "special_forces":
            if self.special_timer <= 0:
                self.invulnerable_timer = 2.0
                self.special_timer = 8.0
                game.effects.append(Explosion(self.x, self.y - 30, 35, "CAMUFLAGEM"))
            if target and self.attack_timer <= 0:
                for dy in (-9, -3, 3, 9):
                    projectiles.add(Projectile((self.x + 28, self.y - 10 + dy), target, 12, 940, YELLOW))
                self.attack_timer = .78
            return

        if self.kind == "engineer":
            if self.attack_timer <= 0:
                nearby = self.find_target(zombies, 420)
                if nearby:
                    projectiles.add(Projectile((self.x + 28, self.y - 5), nearby, 15, 840, STEEL_LIGHT))
                self.attack_timer = .85
            return

        if self.kind == "flamethrower":
            if self.attack_timer <= 0:
                targets = [z for z in zombies if z.lane == self.lane and 0 < z.x - self.x < 230]
                for z in targets[:4]:
                    z.damage(18)
                    self._burn(z)
                if targets:
                    game.effects.append(Explosion(self.x + 120, self.y - 12, 85, "FOGO"))
                self.attack_timer = 1.0
            return

        if self.kind == "shotgunner":
            if target and target.x - self.x < 280 and self.attack_timer <= 0:
                for offset in (-18, -9, 0, 9, 18):
                    projectiles.add(Projectile((self.x + 26, self.y - 12), target, 13, 720, STEEL_LIGHT))
                self.attack_timer = 1.25
            return

        if self.kind == "radio_operator":
            if self.special_timer <= 0:
                cluster = [z for z in zombies if z.lane == self.lane and z.x > self.x]
                if cluster:
                    center = min(cluster, key=lambda z: z.x).x + 100
                    for z in list(zombies):
                        if z.lane == self.lane and abs(z.x - center) < 115:
                            z.damage(150)
                    game.effects.append(Explosion(center, self.y - 10, 120, "ATAQUE AÉREO"))
                self.special_timer = 9.0
            return

        if self.kind == "drone_operator":
            if self.special_timer <= 0 and target:
                projectiles.add(Projectile((self.x + 20, self.y - 54), target, 48, 620, CYAN))
                self.special_timer = 1.55
            return

        if self.kind == "cryo_operator":
            if target and self.attack_timer <= 0:
                projectiles.add(Projectile((self.x + 28, self.y - 10), target, 35, 700, CYAN,
                                           effect=lambda z: setattr(z, "slow_timer", 2.7)))
                self.attack_timer = 1.35
            return

        if self.kind == "mortar":
            if target and self.attack_timer <= 0:
                projectiles.add(Projectile((self.x + 18, self.y - 30), target, 82, 500, ORANGE,
                                           effect=lambda z: game.area_damage(z.x, z.y, 105, 55)))
                self.attack_timer = 2.4
            return

        if self.kind == "scout_buggy":
            if self.attack_timer <= 0:
                close = [z for z in zombies if z.lane == self.lane and self.x < z.x < self.x + 120]
                for z in close:
                    z.damage(90)
                self.x = min(self.x + 54 * dt, ZOMBIE_START_X - 28)
                self.rect.center = (int(self.x), int(self.y))
                if close:
                    game.effects.append(Explosion(self.x + 25, self.y, 45, "ATROPELO"))
                self.attack_timer = .7
            return

        if self.kind == "patrol_boat":
            if target and self.attack_timer <= 0:
                projectiles.add(Projectile((self.x + 31, self.y - 20), target, 64, 760, CYAN))
                self.attack_timer = 1.25
            return

        if self.kind == "submarine":
            if self.special_timer <= 0:
                self.invulnerable_timer = 2.4
                self.special_timer = 7.5
                game.effects.append(Explosion(self.x, self.y + 22, 50, "MERGULHO"))
            if target and self.attack_timer <= 0:
                projectiles.add(Projectile((self.x + 30, self.y - 4), target, 105, 620, YELLOW))
                self.attack_timer = 2.05
            return

        if self.kind == "water_bomb":
            if target and self.attack_timer <= 0:
                projectiles.add(Projectile((self.x + 5, self.y - 8), target, 80, 480, CYAN,
                                           effect=lambda z: game.area_damage(z.x, z.y, 130, 70)))
                self.attack_timer = 2.0
            return

        if not target or self.attack_timer > 0:
            return

        if self.kind == "lieutenant":
            projectiles.add(Projectile((self.x + 30, self.y - 10), target, 38, 850))
            self.attack_timer = .92
        elif self.kind == "general":
            for dy in (-4, 4):
                projectiles.add(Projectile((self.x + 31, self.y - 10 + dy), target, 14, 850))
            self.attack_timer = .88
        elif self.kind == "sniper":
            projectiles.add(Projectile((self.x + 34, self.y - 14), target, 125, 1100, WHITE))
            self.attack_timer = 2.8
        elif self.kind == "grenadier":
            projectiles.add(Projectile((self.x + 26, self.y - 18), target, 55, 510, GRENADE_LIGHT,
                                       effect=lambda z: game.area_damage(z.x, z.y, 135, 58)))
            self.attack_timer = 1.65

    def draw(self, screen):
        x, y = int(self.x), int(self.y + math.sin(self.anim) * 1.5)
        data = SOLDIER_DATA[self.kind]
        body = WHITE if self.flash > 0 else data["color"]
        pygame.draw.ellipse(screen, (29, 35, 29), (x - 33, y + 24, 66, 13))
        # lower body
        pygame.draw.rect(screen, UNIFORM_DARK, (x - 19, y + 4, 13, 29), border_radius=5)
        pygame.draw.rect(screen, UNIFORM_DARK, (x + 6, y + 4, 13, 29), border_radius=5)
        pygame.draw.rect(screen, BLACK, (x - 21, y + 28, 18, 6), border_radius=2)
        pygame.draw.rect(screen, BLACK, (x + 6, y + 28, 18, 6), border_radius=2)
        # torso / tactical vest
        pygame.draw.rect(screen, body, (x - 25, y - 22, 50, 42), border_radius=9)
        pygame.draw.rect(screen, UNIFORM_DARK, (x - 17, y - 10, 34, 22), border_radius=4)
        pygame.draw.line(screen, UNIFORM_LIGHT, (x, y - 8), (x, y + 9), 2)
        # head and helmet
        pygame.draw.circle(screen, SKIN, (x, y - 36), 17)
        pygame.draw.circle(screen, SKIN_LIGHT, (x + 4, y - 39), 8)
        pygame.draw.ellipse(screen, UNIFORM_DARK, (x - 20, y - 52, 40, 22))
        pygame.draw.ellipse(screen, UNIFORM, (x - 15, y - 48, 30, 14))
        pygame.draw.rect(screen, UNIFORM, (x - 21, y - 40, 42, 7), border_radius=3)
        pygame.draw.circle(screen, BLACK, (x + 5, y - 37), 2)
        # distinctive silhouettes
        if self.kind == "rifleman":
            pygame.draw.rect(screen, SAND, (x - 31, y - 4, 22, 22), border_radius=4)
            pygame.draw.line(screen, WOOD_DARK, (x - 31, y - 4), (x - 9, y - 4), 4)
        elif self.kind == "vanguard":
            pygame.draw.polygon(screen, STEEL, [(x + 3, y - 27), (x + 38, y - 20), (x + 40, y + 20), (x + 15, y + 30), (x + 3, y + 10)])
            pygame.draw.line(screen, STEEL_LIGHT, (x + 11, y - 17), (x + 30, y + 14), 3)
        elif self.kind == "bomber":
            pygame.draw.circle(screen, RED_DARK, (x - 27, y - 20), 7)
            pygame.draw.rect(screen, BLACK, (x + 11, y - 4, 18, 14), border_radius=3)
        elif self.kind in ("lieutenant", "general", "sniper"):
            length = 66 if self.kind == "sniper" else 43
            thick = 7 if self.kind != "general" else 10
            pygame.draw.line(screen, STEEL_DARK, (x + 5, y - 7), (x + length, y - 16), thick)
            pygame.draw.line(screen, STEEL_LIGHT, (x + 9, y - 8), (x + length - 6, y - 15), 2)
            if self.kind == "sniper":
                pygame.draw.circle(screen, BLACK, (x + 31, y - 14), 4)
            if self.kind == "general":
                pygame.draw.rect(screen, BLACK, (x + 17, y - 1, 19, 9), border_radius=2)
        elif self.kind == "grenadier":
            pygame.draw.line(screen, STEEL_DARK, (x + 2, y - 5), (x + 36, y - 26), 7)
            pygame.draw.rect(screen, STEEL_DARK, (x + 10, y - 30, 13, 8), border_radius=2)
            pygame.draw.circle(screen, GRENADE_LIGHT, (x - 24, y - 10), 5)
            pygame.draw.circle(screen, GRENADE_LIGHT, (x - 14, y - 1), 5)
        elif self.kind == "rambo":
            pygame.draw.line(screen, STEEL_LIGHT, (x + 4, y - 4), (x + 26, y - 17), 3)
            pygame.draw.line(screen, STEEL_LIGHT, (x + 7, y + 2), (x + 27, y - 1), 3)
            pygame.draw.line(screen, SKIN_DARK, (x - 16, y - 18), (x - 31, y - 25), 4)
        elif self.kind == "special_forces":
            pygame.draw.rect(screen, BLACK, (x - 20, y - 45, 18, 12), border_radius=3)
            pygame.draw.line(screen, STEEL, (x + 5, y - 8), (x + 41, y - 20), 6)
            for yy in (-3, 4, 11):
                pygame.draw.line(screen, MEDIC_RED, (x - 25, y + yy), (x - 16, y + yy), 2)
        elif self.kind == "engineer":
            pygame.draw.rect(screen, SAND, (x - 31, y - 8, 16, 18), border_radius=3)
            pygame.draw.rect(screen, STEEL_DARK, (x + 10, y - 17, 24, 14), border_radius=4)
        elif self.kind == "flamethrower":
            pygame.draw.rect(screen, STEEL_DARK, (x - 31, y - 5, 18, 28), border_radius=4)
            pygame.draw.line(screen, ORANGE, (x + 10, y - 7), (x + 41, y - 15), 8)
        elif self.kind == "shotgunner":
            pygame.draw.line(screen, STEEL_DARK, (x + 4, y - 8), (x + 45, y - 14), 10)
        elif self.kind == "radio_operator":
            pygame.draw.rect(screen, STEEL_DARK, (x - 34, y - 6, 20, 26), border_radius=4)
            pygame.draw.line(screen, STEEL_LIGHT, (x - 24, y - 8), (x - 8, y - 36), 2)
        elif self.kind == "drone_operator":
            pygame.draw.circle(screen, STEEL, (x + 25, y - 39), 10)
            pygame.draw.line(screen, STEEL_DARK, (x + 18, y - 39), (x + 32, y - 39), 2)
        elif self.kind == "cryo_operator":
            pygame.draw.line(screen, CYAN, (x + 5, y - 9), (x + 40, y - 21), 7)
            pygame.draw.circle(screen, WHITE, (x - 24, y - 15), 5)
        elif self.kind == "mortar":
            pygame.draw.line(screen, STEEL_DARK, (x + 5, y + 5), (x + 25, y - 32), 9)
            pygame.draw.circle(screen, STEEL, (x + 28, y - 35), 7)
        elif self.kind == "scout_buggy":
            pygame.draw.rect(screen, body, (x - 36, y + 4, 72, 21), border_radius=8)
            pygame.draw.circle(screen, BLACK, (x - 23, y + 27), 9)
            pygame.draw.circle(screen, BLACK, (x + 23, y + 27), 9)
        elif self.kind == "patrol_boat":
            pygame.draw.polygon(screen, body, [(x - 34, y + 7), (x + 34, y + 7), (x + 20, y + 25), (x - 26, y + 25)])
            pygame.draw.rect(screen, STEEL_LIGHT, (x - 9, y - 6, 18, 12), border_radius=4)
            pygame.draw.line(screen, STEEL_DARK, (x + 4, y - 4), (x + 35, y - 10), 7)
        elif self.kind == "submarine":
            pygame.draw.ellipse(screen, body, (x - 35, y - 10, 72, 28))
            pygame.draw.rect(screen, STEEL, (x - 2, y - 25, 14, 10), border_radius=3)
            pygame.draw.line(screen, STEEL_DARK, (x + 22, y + 2), (x + 45, y - 4), 5)
        elif self.kind == "water_bomb":
            pygame.draw.circle(screen, STEEL_DARK, (x + 3, y + 2), 22)
            pygame.draw.circle(screen, CYAN, (x + 3, y + 2), 11)
        if self.invulnerable_timer > 0:
            pygame.draw.circle(screen, CYAN, (x, y - 5), 44, 2)
        health_bar(screen, pygame.Rect(x - 31, y - 63, 62, 7), self.hp, self.max_hp, GREEN)


class Zombie(pygame.sprite.Sprite):
    def __init__(self, lane, kind, wave):
        super().__init__()
        data = ZOMBIE_DATA[kind]
        self.lane, self.kind = lane, kind
        self.x = ZOMBIE_START_X + random.randint(0, 130)
        self.y = BOARD_Y + lane * CELL_H + CELL_H // 2
        scale = 1 + wave * .048
        self.max_hp = int(data["hp"] * scale)
        self.hp = float(self.max_hp)
        self.damage_value = int(data["damage"] * (1 + wave * .025))
        speed_scale = 1 + wave * .010
        if wave >= 4: speed_scale += .15
        if wave >= 7: speed_scale += .11
        if wave >= 10: speed_scale += .12
        if wave >= 13: speed_scale += .11
        self.speed = data["speed"] * speed_scale
        self.reward = data["reward"]
        self.attack_timer = random.uniform(0, .45)
        self.flash, self.burn_timer, self.slow_timer, self.anim = 0, 0, 0, random.random() * math.tau
        self.special_cool = random.uniform(2, 4)
        self.rect = pygame.Rect(self.x - 35, self.y - 42, 70, 82)
        self.moved_once = False

    def alive(self): return self.hp > 0
    def damage(self, amount): self.hp -= amount; self.flash = .1
    def target_point(self): return self.x - 28, self.y - 12

    def update(self, dt, soldiers, game):
        self.anim += dt * (4 if self.kind in ("runner", "crawler", "feral", "leaper", "swimmer") else 2.7)
        self.attack_timer -= dt; self.special_cool -= dt; self.flash -= dt; self.burn_timer -= dt; self.slow_timer -= dt
        if self.hp <= 0:
            game.on_zombie_killed(self); self.kill(); return
        targets = [s for s in soldiers if s.lane == self.lane and 0 <= self.x - s.x <= 52]
        target = min(targets, key=lambda s: self.x - s.x) if targets else None
        if target:
            if self.attack_timer <= 0:
                target.damage(self.damage_value)
                if self.kind == "toxic": target.damage(6)
                self.attack_timer = ZOMBIE_DATA[self.kind]["cooldown"]
        else:
            speed = self.speed
            if self.slow_timer > 0: speed *= .45
            if self.kind == "screamer" and self.special_cool <= 0:
                for z in soldiers:
                    if z.lane == self.lane:
                        pass
                # Screamer creates pressure by temporarily accelerating nearby zombies.
                for other in game.zombies:
                    if other is not self and other.lane == self.lane and abs(other.x - self.x) < 240:
                        other.speed *= 1.16
                self.special_cool = 6
            if self.kind == "leaper" and not self.moved_once and self.x - game.BOARD_X < 250 and targets:
                self.x -= 80
                self.moved_once = True
            self.x -= speed * dt
        if self.burn_timer > 0:
            self.hp -= 9 * dt
        self.rect.center = (int(self.x), int(self.y))
        if self.x <= BASE_X + 62:
            game.activate_base_defense(self.lane)
            self.kill()

    def draw(self, screen):
        x, y = int(self.x), int(self.y + math.sin(self.anim) * 2)
        body = WHITE if self.flash > 0 else ZOMBIE_DATA[self.kind]["color"]
        if self.kind == "crawler":
            pygame.draw.ellipse(screen, (36, 42, 35), (x - 31, y + 20, 62, 12))
            pygame.draw.ellipse(screen, body, (x - 30, y - 4, 59, 34))
            pygame.draw.circle(screen, body, (x + 20, y - 11), 13)
            pygame.draw.ellipse(screen, WHITE, (x + 16, y - 15, 8, 8)); pygame.draw.circle(screen, RED, (x + 20, y - 11), 2)
        else:
            pygame.draw.ellipse(screen, (38, 44, 38), (x - 34, y + 24, 68, 13))
            pygame.draw.rect(screen, (70, 70, 63), (x - 25, y - 1, 50, 36), border_radius=8)
            pygame.draw.polygon(screen, body, [(x - 24, y - 19), (x - 8, y - 30), (x + 20, y - 20), (x + 25, y + 15), (x + 6, y + 22), (x - 24, y + 14)])
            pygame.draw.line(screen, body, (x - 18, y - 8), (x - 41, y - 27), 10)
            pygame.draw.line(screen, body, (x + 17, y - 6), (x + 41, y + 10), 10)
            pygame.draw.circle(screen, body, (x, y - 38), 17 if self.kind not in ("brute", "tide_brute") else 22)
            pygame.draw.circle(screen, (144, 169, 101), (x - 3, y - 41), 10)
            pygame.draw.arc(screen, ZOMBIE_DARK, (x - 17, y - 59, 34, 23), math.pi, math.tau, 5)
            pygame.draw.ellipse(screen, WHITE, (x - 12, y - 45, 8, 8)); pygame.draw.ellipse(screen, WHITE, (x + 4, y - 45, 8, 8))
            pygame.draw.circle(screen, RED, (x - 8, y - 41), 2); pygame.draw.circle(screen, RED, (x + 8, y - 41), 2)
            pygame.draw.rect(screen, ZOMBIE_DARK, (x - 12, y - 32, 24, 11), border_radius=3)
            for dx in (-6, 0, 6): pygame.draw.rect(screen, WHITE, (x + dx - 2, y - 31, 4, 5))
        if self.kind == "armored":
            pygame.draw.rect(screen, STEEL_DARK, (x - 29, y - 16, 58, 36), border_radius=7)
            pygame.draw.line(screen, STEEL_LIGHT, (x - 13, y - 10), (x + 17, y + 10), 4)
        elif self.kind == "toxic":
            for bx, by in ((-22, -22), (22, -16), (12, -49)):
                pygame.draw.circle(screen, (164, 205, 76), (x + bx, y + by), 5)
        elif self.kind == "feral":
            pygame.draw.line(screen, RED_DARK, (x - 9, y - 51), (x - 15, y - 63), 4); pygame.draw.line(screen, RED_DARK, (x + 9, y - 51), (x + 15, y - 63), 4)
        elif self.kind == "screamer":
            pygame.draw.polygon(screen, YELLOW, [(x - 9, y - 59), (x - 1, y - 75), (x + 8, y - 59)])
        elif self.kind == "spitter":
            pygame.draw.circle(screen, (81, 201, 97), (x + 19, y - 28), 5)
            pygame.draw.line(screen, (81, 201, 97), (x + 19, y - 28), (x + 39, y - 20), 3)
        elif self.kind == "splitter":
            pygame.draw.line(screen, RED_DARK, (x - 8, y - 53), (x + 5, y - 30), 2); pygame.draw.line(screen, RED_DARK, (x + 5, y - 30), (x + 15, y - 50), 2)
        elif self.kind == "leaper":
            pygame.draw.line(screen, BLACK, (x - 20, y + 6), (x - 40, y - 9), 5); pygame.draw.line(screen, BLACK, (x + 18, y + 3), (x + 38, y - 9), 5)
        elif self.kind == "necromancer":
            pygame.draw.rect(screen, PURPLE, (x - 14, y - 68, 28, 11), border_radius=3)
        elif self.kind == "sandstalker":
            pygame.draw.arc(screen, SAND, (x - 25, y - 64, 50, 30), 0, math.pi, 6)
        elif self.kind == "frostborn":
            pygame.draw.circle(screen, WHITE, (x - 20, y - 21), 5); pygame.draw.circle(screen, WHITE, (x + 22, y - 16), 4)
        elif self.kind == "swimmer":
            pygame.draw.line(screen, CYAN, (x - 25, y + 24), (x + 30, y + 24), 3)
        elif self.kind == "tide_brute":
            pygame.draw.rect(screen, STEEL_DARK, (x - 33, y - 17, 66, 19), border_radius=4)
            pygame.draw.circle(screen, CYAN, (x, y - 62), 7)
        health_bar(screen, pygame.Rect(x - 33, y - 69, 66, 7), self.hp, self.max_hp, RED)


class BossZombie(Zombie):
    def __init__(self, lane, wave):
        data = BOSS_DATA[wave]
        pygame.sprite.Sprite.__init__(self)
        self.lane, self.wave, self.kind = lane, wave, "boss"
        self.boss_name = data["name"]
        self.x = ZOMBIE_START_X + 70
        self.y = BOARD_Y + lane * CELL_H + CELL_H // 2
        self.max_hp = data["hp"]; self.hp = float(self.max_hp); self.damage_value = data["damage"]
        self.speed = data["speed"]; self.reward = data["reward"]; self.attack_timer = 1.0; self.flash = 0
        self.anim = 0; self.rect = pygame.Rect(self.x - 58, self.y - 72, 116, 138)

    def target_point(self): return self.x - 45, self.y - 20
    def alive(self): return self.hp > 0
    def damage(self, amount): self.hp -= amount; self.flash = .08

    def update(self, dt, soldiers, game):
        self.anim += dt * 2; self.attack_timer -= dt; self.flash -= dt
        targets = [s for s in soldiers if s.lane == self.lane and 0 <= self.x - s.x <= 75]
        target = min(targets, key=lambda s: self.x - s.x) if targets else None
        if target:
            if self.attack_timer <= 0:
                target.damage(self.damage_value)
                if self.wave == 10 and random.random() < .25: target.damage(12)
                if self.wave == 15 and random.random() < .3: target.damage(18)
                self.attack_timer = .92
        else:
            self.x -= self.speed * dt
        self.rect.center = (int(self.x), int(self.y))
        if self.hp <= 0:
            game.on_boss_killed(self); self.kill(); return
        if self.x <= BASE_X + 62:
            game.base_hp = max(0, game.base_hp - 50); self.x = BASE_X + 63

    def draw(self, screen):
        x, y = int(self.x), int(self.y + math.sin(self.anim) * 2)
        body = WHITE if self.flash > 0 else BOSS_DATA[self.wave]["color"]
        pygame.draw.ellipse(screen, (28, 32, 28), (x - 64, y + 47, 128, 22))
        pygame.draw.rect(screen, body, (x - 47, y - 34, 94, 73), border_radius=16)
        pygame.draw.circle(screen, body, (x, y - 61), 34)
        pygame.draw.arc(screen, ZOMBIE_DARK, (x - 32, y - 88, 64, 33), math.pi, math.tau, 10)
        pygame.draw.ellipse(screen, WHITE, (x - 22, y - 70, 15, 13)); pygame.draw.ellipse(screen, WHITE, (x + 7, y - 70, 15, 13))
        pygame.draw.circle(screen, RED, (x - 14, y - 64), 4); pygame.draw.circle(screen, RED, (x + 14, y - 64), 4)
        pygame.draw.rect(screen, ZOMBIE_DARK, (x - 23, y - 43, 46, 20), border_radius=5)
        if self.wave == 5:
            pygame.draw.rect(screen, WHITE, (x - 20, y - 24, 40, 34), border_radius=4)
        elif self.wave == 10:
            pygame.draw.rect(screen, STEEL, (x - 30, y - 28, 60, 10), border_radius=4)
        else:
            pygame.draw.circle(screen, RED, (x, y - 94), 9)
        txt(screen, self.boss_name, pygame.font.SysFont(FONT, 13, True), YELLOW, (x, y - 111), True)
        health_bar(screen, pygame.Rect(x - 60, y - 100, 120, 9), self.hp, self.max_hp, RED)


class Game(Base):
    BOARD_X = BOARD_X

    def __init__(self):
        super().__init__((WIDTH, HEIGHT))
        self.font_xs = pygame.font.SysFont(FONT, 12)
        self.font_small = pygame.font.SysFont(FONT, 15)
        self.font = pygame.font.SysFont(FONT, 20, True)
        self.font_big = pygame.font.SysFont(FONT, 39, True)
        self.font_title = pygame.font.SysFont(FONT, 52, True)
        self.reset()

    def reset(self):
        self.mode = "title"
        self.phase_key = "grass"
        self.supplies = float(START_SUPPLIES)
        self.base_hp = 100.0
        self.wave = 1
        self.wave_target = 0
        self.wave_spawned = 0
        self.wave_time = 0
        self.spawn_timer = 1.5
        self.score = self.kills = 0
        self.selected_cards = []
        self.selection_candidates = []
        self.selected = None
        self.tool_selected = False
        self.soldiers = pygame.sprite.Group(); self.zombies = pygame.sprite.Group(); self.projectiles = pygame.sprite.Group()
        self.supply_drops = []
        self.shells = []
        self.effects = []
        self.field_mines = []
        self.base_defenses = [True] * LANES
        self.cards = {}
        self.message = ""; self.message_timer = 0; self.banner_timer = 0
        self.horde_active = False; self.horde_timer = 0; self.horde_left = 0
        self.campaign_choice = 0
        self.unlocked_phase_index = 0
        self.phase_select_rects = {}

    def initialize(self): self.mode = "title"

    def allowed_candidates(self):
        # A campanha usa um baralho global: todas as cartas ficam disponiveis
        # em qualquer fase. A fase muda o cenario e os inimigos, nao o catalogo.
        return list(SOLDIER_DATA.keys()) + ["mine"]

    def choose_phase(self, phase):
        order = list(PHASES.keys())
        phase_index = order.index(phase)
        if phase_index > self.unlocked_phase_index:
            self.message = "OPERAÇÃO BLOQUEADA — COMPLETE A ANTERIOR"
            self.message_timer = 1.5
            return
        self.phase_key = phase
        self.selection_candidates = self.allowed_candidates()
        defaults = ["rifleman", "lieutenant", "vanguard", "general", "bomber", "sniper", "grenadier"]
        self.selected_cards = [k for k in defaults if k in self.selection_candidates]
        self.mode = "select"
        self.message = f"{PHASES[phase]['name']}: monte seu esquadrão"
        self.message_timer = 1.5

    def toggle_card(self, kind):
        if kind in self.selected_cards:
            self.selected_cards.remove(kind); return
        if len(self.selected_cards) < MAX_SELECTED_CARDS:
            self.selected_cards.append(kind)
        else:
            self.message = "Máximo de 7 cartas."; self.message_timer = 1.2

    def start_battle(self):
        if len(self.selected_cards) != 7:
            self.message = "Escolha exatamente 7 cartas."; self.message_timer = 1.3; return
        self.cards = {}
        # First slot is always the MEDICAL TOOL, never a card and never replacing BOMBER/MINE.
        x = 108
        slot_w = 164
        for kind in self.selected_cards:
            self.cards[kind] = pygame.Rect(x, 94, slot_w, 64); x += slot_w + 2
        self.mode = "playing"
        self.selected = self.selected_cards[0]
        self.tool_selected = False
        self.supplies = float(START_SUPPLIES)
        self.wave = 1; self.wave_spawned = 0; self.wave_time = 0; self.wave_target = self.wave_quota(1)
        self.spawn_timer = 2.5; self.banner_timer = 2.1; self.horde_active = False
        self.message = f"{PHASES[self.phase_key]['name']} — DEFESA INICIADA"; self.message_timer = 1.6

    def wave_quota(self, wave):
        return 9 + wave * 5 + (wave // 3) * 5

    def allowed_zombies(self):
        phase = self.phase_key
        kinds = ["normal"]
        if self.wave >= 2: kinds += ["runner"]
        if self.wave >= 3: kinds += ["conehead", "crawler", "brute"]
        if self.wave >= 4: kinds += ["flagger"]
        if self.wave >= 5: kinds += ["toxic", "armored", "feral", "vaulting"]
        if self.wave >= 7: kinds += ["splitter", "screamer", "spitter", "door_shield"]
        if self.wave >= 9: kinds += ["leaper", "necromancer"]
        if self.wave >= 4 and phase == "desert": kinds += ["sandstalker", "digging"]
        if self.wave >= 4 and phase == "snow": kinds += ["frostborn"]
        if self.wave >= 4 and phase == "water": kinds += ["swimmer"]
        if self.wave >= 7 and phase == "water": kinds += ["tide_brute"]
        return [k for k in kinds if ZOMBIE_DATA.get(k, {}).get("phase") in (None, phase)]

    def choose_zombie(self):
        kinds = self.allowed_zombies()
        weights = []
        for kind in kinds:
            if kind == "normal": w = max(10, 34 - self.wave * 2)
            elif kind in ("runner", "crawler", "feral", "leaper", "vaulting", "swimmer", "flagger"): w = 17
            elif kind in ("conehead", "brute", "toxic", "armored", "frostborn", "sandstalker", "tide_brute", "door_shield", "digging"): w = 11
            else: w = 7
            weights.append(w)
        return random.choices(kinds, weights=weights, k=1)[0]

    def spawn_zombie(self, kind=None):
        kind = kind or self.choose_zombie()
        required_phase = ZOMBIE_DATA[kind].get("phase")
        if required_phase and required_phase != self.phase_key:
            kind = self.choose_zombie()
        lane = random.randrange(LANES)
        # Zumbis aquáticos só existem na fase de água e entram pela linha aquática.
        if ZOMBIE_DATA[kind].get("phase") == "water":
            if self.phase_key != "water":
                kind = self.choose_zombie()
            else:
                lane = PHASES[self.phase_key]["water_lane"]
        self.zombies.add(Zombie(lane, kind, self.wave)); self.wave_spawned += 1

    def spawn_boss(self):
        lane = PHASES[self.phase_key]["water_lane"] if self.phase_key == "water" else random.randrange(LANES)
        self.zombies.add(BossZombie(lane, self.wave)); self.message = "⚠ CHEFE DA HORDA ⚠"; self.message_timer = 2.0

    def advance_campaign(self):
        order = list(PHASES.keys())
        current_index = order.index(self.phase_key)
        if current_index >= len(order) - 1:
            self.mode = "victory"
            return
        self.unlocked_phase_index = min(len(order) - 1, current_index + 1)
        self.phase_key = order[current_index + 1]
        self.selection_candidates = self.allowed_candidates()
        # Preserve the previous loadout where possible, then let the player edit it.
        self.selected_cards = [k for k in self.selected_cards if k in self.selection_candidates]
        while len(self.selected_cards) < MAX_SELECTED_CARDS:
            for candidate in self.selection_candidates:
                if candidate not in self.selected_cards:
                    self.selected_cards.append(candidate)
                    if len(self.selected_cards) == MAX_SELECTED_CARDS:
                        break
        self.cards = {}
        self.soldiers.empty(); self.zombies.empty(); self.projectiles.empty()
        self.supply_drops.clear(); self.shells.clear(); self.effects.clear(); self.field_mines.clear()
        self.base_defenses = [True] * LANES
        self.supplies = float(START_SUPPLIES)
        self.base_hp = 100.0
        self.mode = "select"
        self.message = f"{PHASES[self.phase_key]['name']}: escolha suas 7 cartas"
        self.message_timer = 1.8

    def next_wave(self):
        self.wave += 1
        if self.wave > MAX_WAVES:
            self.advance_campaign(); return
        self.wave_spawned = 0; self.wave_time = 0; self.wave_target = self.wave_quota(self.wave)
        self.banner_timer = 2.0
        self.horde_active = self.wave in (4, 7, 9, 12, 14)
        self.horde_left = 18 + self.wave // 2 if self.horde_active else 0
        self.horde_timer = 0.0
        self.message = "HORDA MASSIVA!" if self.horde_active else f"ONDA {self.wave}"
        self.message_timer = 1.8

    def get_cell(self, pos):
        mx, my = pos
        if not (BOARD_X <= mx < BOARD_X + BOARD_W and BOARD_Y <= my < BOARD_Y + BOARD_H): return None
        return int((my - BOARD_Y) // CELL_H), int((mx - BOARD_X) // CELL_W)

    def water_lane(self): return PHASES[self.phase_key]["water_lane"]

    def is_occupied(self, lane, col):
        return any(s.lane == lane and s.column == col for s in self.soldiers) or any(m.lane == lane and m.column == col for m in self.field_mines)

    def place_selected(self):
        cell = self.get_cell(self.input.mouse_position)
        if cell is None or self.selected is None: return
        lane, col = cell
        if self.is_occupied(lane, col):
            self.toast("POSIÇÃO OCUPADA", RED); return
        if self.selected == "mine":
            cost = 75
            if self.supplies < cost: self.toast("75 SUP NECESSÁRIOS", RED); return
            if self.phase_key == "water" and lane == 2:
                # On water, the universal mine is disallowed; use Water Bomb instead.
                self.toast("NA ÁGUA USE A BOMBA AQUÁTICA", CYAN); return
            self.supplies -= cost; self.field_mines.append(MineObject(lane, col, self)); return
        data = SOLDIER_DATA[self.selected]
        phase_req = data.get("phase")
        if phase_req and phase_req != self.phase_key: self.toast("ESSA CARTA É DE OUTRA FASE", RED); return
        if self.phase_key == "water" and lane == 2 and phase_req != "water":
            self.toast("LINHA DE ÁGUA: USE CARTAS AQUÁTICAS", CYAN); return
        if self.phase_key == "water" and lane != 2 and phase_req == "water":
            self.toast("ESSA CARTA SÓ PODE IR NA LINHA DE ÁGUA", CYAN); return
        if self.supplies < data["cost"]: self.toast("SUPRIMENTOS INSUFICIENTES", RED); return
        self.supplies -= data["cost"]; self.soldiers.add(Soldier(lane, col, self.selected)); self.tool_selected = False

    def remove_selected(self):
        mx, my = self.input.mouse_position
        for soldier in list(self.soldiers):
            if soldier.rect.collidepoint(mx, my):
                refund = max(15, SOLDIER_DATA[soldier.kind]["cost"] // 2)
                self.supplies = min(MAX_SUPPLIES, self.supplies + refund); soldier.kill(); self.toast(f"UNIDADE REMOVIDA +{refund}", YELLOW); return
        for mine in self.field_mines[:]:
            if abs(mx - mine.x) < 42 and abs(my - mine.y) < 42:
                self.supplies = min(MAX_SUPPLIES, self.supplies + 35); self.field_mines.remove(mine); self.toast("MINA REMOVIDA +35", YELLOW); return

    def collect_supply(self):
        mx, my = self.input.mouse_position
        for drop in self.supply_drops[:]:
            lane, x = drop; y = BOARD_Y + lane * CELL_H + CELL_H // 2 + 25
            if abs(mx - x) < 36 and abs(my - y) < 34:
                self.supplies = min(MAX_SUPPLIES, self.supplies + 25); self.supply_drops.remove(drop); self.float_text("+25 SUP", x, y - 25, YELLOW); return True
        return False

    def float_text(self, content, x, y, color): self.effects.append(FloatingText(content, x, y, color))
    def toast(self, content, color=WHITE): self.message, self.message_timer = content, 1.2

    def area_damage(self, x, y, radius, damage):
        for z in list(self.zombies):
            if math.hypot(z.x - x, z.y - y) <= radius: z.damage(damage)
        self.effects.append(Explosion(x, y, radius, ""))

    def add_slash(self, x, y): self.effects.append(Explosion(x, y, 25, ""))

    def on_zombie_killed(self, z):
        self.score += z.reward; self.kills += 1
        if z.kind == "splitter" and random.random() < .6:
            for _ in range(2): self.spawn_zombie("crawler")
        if z.kind == "necromancer" and random.random() < .45 and self.wave < 15:
            for _ in range(2): self.spawn_zombie("normal")
        self.float_text(f"+{z.reward}", z.x, z.y - 43, YELLOW)

    def on_boss_killed(self, boss):
        self.score += boss.reward; self.kills += 1; self.effects.append(Explosion(boss.x, boss.y - 10, 120, "CHEFE DERROTADO"))

    def activate_base_defense(self, lane):
        if self.base_defenses[lane]:
            self.base_defenses[lane] = False
            for z in list(self.zombies):
                if z.lane == lane: z.damage(99999)
            self.effects.append(Explosion(BASE_X + 34, BOARD_Y + lane * CELL_H + 43, 105, "DEFESA DA BASE"))
        else:
            self.base_hp = max(0, self.base_hp - 24)
            if self.base_hp <= 0: self.mode = "defeat"

    def handle_events(self):
        keys = self.input.keys_pressed; mx, my = self.input.mouse_position
        if pygame.K_ESCAPE in keys:
            if self.mode == "playing": self.mode = "paused"
            elif self.mode == "paused": self.mode = "playing"
            else: self.running = False
        if self.mode == "title":
            if self.input.just_clicked:
                self.mode = "phases"
            return
        if self.mode == "phases":
            if self.input.just_clicked:
                for phase, rect in self.phase_select_rects.items():
                    if rect.collidepoint(mx, my):
                        self.choose_phase(phase)
                        return
            return
        if self.mode == "select":
            if self.input.just_clicked:
                rects = self.selection_rects()
                if pygame.Rect(WIDTH // 2 - 160, 652, 320, 48).collidepoint(mx, my): self.start_battle(); return
                for kind, rect in rects.items():
                    if rect.collidepoint(mx, my): self.toggle_card(kind); return
            return
        if self.mode in ("victory", "defeat"):
            end_rect = pygame.Rect(WIDTH // 2 - 180, 545, 360, 54)
            if self.input.just_clicked and end_rect.collidepoint(mx, my):
                if self.mode == "victory" and self.phase_key != "water":
                    self.advance_campaign()
                else:
                    self.reset()
                    self.mode = "phases"
            return
        if pygame.K_p in keys and self.mode in ("playing", "paused"): self.mode = "paused" if self.mode == "playing" else "playing"
        if self.mode == "paused": return
        shortcuts = {pygame.K_1:0,pygame.K_2:1,pygame.K_3:2,pygame.K_4:3,pygame.K_5:4,pygame.K_6:5,pygame.K_7:6}
        for key, idx in shortcuts.items():
            if key in keys and idx < len(self.selected_cards): self.selected = self.selected_cards[idx]; self.tool_selected = False
        if pygame.K_m in keys: self.tool_selected = True
        if self.input.just_clicked:
            if self.collect_supply(): return
            if TOOL_RECT.collidepoint(mx, my): self.tool_selected = not self.tool_selected; return
            for kind, rect in self.cards.items():
                if rect.collidepoint(mx, my): self.selected = kind; self.tool_selected = False; return
            if self.tool_selected: self.remove_selected()
            else: self.place_selected()
        if self.input.just_right_clicked: self.tool_selected = True

    def update(self, dt):
        self.handle_events()
        if self.message_timer > 0: self.message_timer -= dt
        for effect in self.effects[:]:
            effect.update(dt)
            if getattr(effect, "life", 0) <= 0: self.effects.remove(effect)
        if self.mode != "playing": return
        self.wave_time += dt
        if self.banner_timer > 0: self.banner_timer -= dt

        # Regular stream + short mass bursts. Pressure grows sharply from wave 4 onward.
        if self.horde_active:
            self.horde_timer -= dt
            if self.horde_left > 0 and self.horde_timer <= 0:
                burst = 2 if self.wave >= 7 else 1
                for _ in range(min(burst, self.horde_left)):
                    self.spawn_zombie("runner" if random.random() < .42 else None)
                    self.horde_left -= 1
                self.horde_timer = .22 if self.wave < 10 else .17
            else:
                self.horde_active = False
        elif self.wave_spawned < self.wave_target:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                burst = 1
                if self.wave >= 4 and random.random() < .42: burst += 1
                if self.wave >= 8 and random.random() < .35: burst += 1
                if self.wave >= 12 and random.random() < .25: burst += 1
                for _ in range(burst):
                    if self.wave_spawned < self.wave_target: self.spawn_zombie()
                if self.wave < 4: self.spawn_timer = 2.7
                elif self.wave < 7: self.spawn_timer = 1.45
                elif self.wave < 10: self.spawn_timer = 1.05
                elif self.wave < 13: self.spawn_timer = .78
                else: self.spawn_timer = .58

        if self.wave in (5, 10, 15) and self.wave_spawned >= self.wave_target and not any(isinstance(z, BossZombie) for z in self.zombies) and self.wave_time > 5:
            self.spawn_boss()

        for soldier in list(self.soldiers):
            soldier.update(dt, self.zombies, self.projectiles, self)
            if soldier.hp <= 0: soldier.kill(); self.effects.append(Explosion(soldier.x, soldier.y, 35, ""))
        for mine in self.field_mines[:]:
            mine.update(dt, self.zombies, self)
            if not mine.armed: self.field_mines.remove(mine)
        for z in list(self.zombies): z.update(dt, self.soldiers, self)
        self.projectiles.update(dt)
        for shell in self.shells[:]:
            shell.update(dt)
            if shell.life <= 0: self.shells.remove(shell)
        if self.wave_spawned >= self.wave_target and not self.zombies and not any(isinstance(z, BossZombie) for z in self.zombies) and self.wave_time > 5:
            self.next_wave()

    # ---------- drawing ----------
    def draw_background(self):
        phase = PHASES[self.phase_key] if hasattr(self, 'phase_key') else PHASES["grass"]
        top, bottom = {
            "grass": ((55, 92, 117), (182, 205, 210)), "snow": ((132, 167, 187), (218, 232, 235)),
            "desert": ((167, 112, 66), (220, 182, 117)), "water": ((47, 98, 124), (129, 193, 206)),
        }[phase["ambience"]]
        for y in range(0, HEIGHT, 6):
            t = y / HEIGHT
            c = tuple(int(top[i] * (1-t) + bottom[i] * t) for i in range(3))
            pygame.draw.rect(self.screen, c, (0, y, WIDTH, 6))
        # parallax hills / silhouettes
        pygame.draw.polygon(self.screen, (78, 109, 83), [(0, 490), (160, 390), (310, 490), (480, 365), (680, 490), (850, 385), (1030, 485), (1160, 390), (1280, 470), (1280, 720), (0, 720)])
        if self.phase_key == "snow":
            for x in range(20, WIDTH, 53): pygame.draw.circle(self.screen, WHITE, (x, 124 + (x % 31)), 2)
        elif self.phase_key == "desert":
            for x in range(20, WIDTH, 95):
                pygame.draw.line(self.screen, (196, 159, 96), (x, 510), (x + 15, 500), 2)
        elif self.phase_key == "water":
            for x in range(10, WIDTH, 72):
                pygame.draw.arc(self.screen, (176, 224, 229), (x, 515, 50, 14), math.pi, math.tau, 2)

    def draw_board(self):
        # Deep trench frame gives the flat Pygame scene a fake 3D/2.5D depth.
        pygame.draw.rect(self.screen, WOOD_DARK if self.phase_key != "water" else (32, 72, 86), (BOARD_X - 12, BOARD_Y - 10, BOARD_W + 24, BOARD_H + 24), border_radius=14)
        water_lane = self.water_lane()
        for lane in range(LANES):
            for col in range(COLS):
                rect = pygame.Rect(BOARD_X + col * CELL_W, BOARD_Y + lane * CELL_H, CELL_W, CELL_H)
                if lane == water_lane:
                    base = (48, 133, 158) if col % 2 else (55, 145, 171)
                    pygame.draw.rect(self.screen, base, rect)
                    for wy in (rect.y + 18, rect.y + 45, rect.y + 70):
                        pygame.draw.arc(self.screen, (114, 201, 210), (rect.x + 5, wy - 5, rect.width - 10, 9), math.pi, math.tau, 1)
                elif self.phase_key == "snow":
                    base = (224, 232, 232) if (lane + col) % 2 else (205, 220, 224)
                    pygame.draw.rect(self.screen, base, rect)
                    pygame.draw.line(self.screen, (169, 191, 200), (rect.x + 8, rect.bottom - 12), (rect.right - 10, rect.bottom - 9), 2)
                elif self.phase_key == "desert":
                    base = (196, 164, 97) if (lane + col) % 2 else (184, 149, 84)
                    pygame.draw.rect(self.screen, base, rect)
                    for k in range(3):
                        px = rect.x + 14 + k * 28; py = rect.y + 20 + ((lane + col + k) * 7) % 48
                        pygame.draw.line(self.screen, (224, 192, 128), (px, py), (px + 7, py - 2), 1)
                else:
                    base = (100, 154, 72) if (lane + col) % 2 else (87, 141, 62)
                    pygame.draw.rect(self.screen, base, rect)
                    for k in range(2):
                        px = rect.x + 14 + k * 38; py = rect.y + 20 + ((lane * 19 + col * 11 + k * 7) % 48)
                        pygame.draw.line(self.screen, (132, 174, 86), (px, py), (px + 3, py - 5), 1)
                pygame.draw.rect(self.screen, (65, 102, 56) if lane != water_lane else (36, 92, 105), rect, 1)
        for lane in range(LANES + 1):
            pygame.draw.line(self.screen, (43, 70, 43) if lane != water_lane else (30, 78, 91), (BOARD_X, BOARD_Y + lane * CELL_H), (BOARD_X + BOARD_W, BOARD_Y + lane * CELL_H), 2)
        if water_lane is not None:
            label_y = BOARD_Y + water_lane * CELL_H + 10
            txt(self.screen, "LINHA DE ÁGUA — SOMENTE CARTAS AQUÁTICAS", self.font_xs, WHITE, (BOARD_X + 12, label_y))

    def draw_base(self):
        panel_rect = pygame.Rect(BASE_X - 13, BOARD_Y - 8, 82, BOARD_H + 21)
        panel(self.screen, panel_rect, WOOD, WOOD_DARK, 3, 12)
        for lane in range(LANES):
            cy = BOARD_Y + lane * CELL_H + CELL_H // 2
            pygame.draw.ellipse(self.screen, (28, 31, 27), (BASE_X - 4, cy + 15, 52, 12))
            pygame.draw.circle(self.screen, BLACK, (BASE_X + 21, cy - 5), 15)
            pygame.draw.circle(self.screen, STEEL_DARK, (BASE_X + 21, cy - 10), 7)
            pygame.draw.circle(self.screen, RED if self.base_defenses[lane] else STEEL_DARK, (BASE_X + 21, cy - 10), 3)

    def draw_medical_tool(self):
        # Medical utility is a dedicated black slot before the cards. It is never a card.
        panel(self.screen, TOOL_RECT, BLACK, YELLOW if self.tool_selected else BORDER, 2, 9)
        cx, cy = TOOL_RECT.centerx, TOOL_RECT.y + 27
        pygame.draw.rect(self.screen, WHITE, (cx - 18, cy - 11, 36, 23), border_radius=4)
        pygame.draw.rect(self.screen, MEDIC_RED, (cx - 6, cy - 16, 12, 33), border_radius=2)
        pygame.draw.rect(self.screen, MEDIC_RED, (cx - 17, cy - 5, 34, 11), border_radius=2)
        txt(self.screen, "MÉDICO", self.font_xs, WHITE, (cx, TOOL_RECT.bottom - 15), True)

    def draw_hud(self):
        pygame.draw.rect(self.screen, PANEL, (0, 0, WIDTH, 78))
        pygame.draw.line(self.screen, BORDER, (0, 77), (WIDTH, 77), 2)
        txt(self.screen, "SOLDADOS VS ZUMBIS", self.font, WHITE, (16, 10))
        txt(self.screen, PHASES[self.phase_key]["name"], self.font_small, YELLOW, (16, 38))
        txt(self.screen, f"SUPRIMENTOS: {int(self.supplies)}", self.font_small, YELLOW, (16, 57))
        txt(self.screen, f"ONDA {self.wave}/{MAX_WAVES}", self.font, WHITE, (1030, 9))
        txt(self.screen, f"PONTOS {self.score}  |  BAIXAS {self.kills}", self.font_small, TEXT, (1030, 40))
        pygame.draw.rect(self.screen, BLACK, (730, 57, 270, 12), border_radius=5)
        pygame.draw.rect(self.screen, RED, (732, 59, int(266 * self.base_hp / 100), 8), border_radius=4)

    def draw_cards(self):
        self.draw_medical_tool()
        for index, kind in enumerate(self.selected_cards):
            rect = self.cards[kind]
            selected = self.selected == kind and not self.tool_selected
            panel(self.screen, rect, (46, 70, 51) if selected else PANEL2, GREEN if selected else BORDER, 2, 8)
            txt(self.screen, str(index + 1), self.font_small, YELLOW, (rect.x + 7, rect.y + 6))
            preview = pygame.Rect(rect.x + 24, rect.y + 8, 43, 45)
            self.draw_card_art(kind, preview, small=True)
            name = "MINA" if kind == "mine" else SOLDIER_DATA[kind]["name"]
            cost = 75 if kind == "mine" else SOLDIER_DATA[kind]["cost"]
            role = "EXPLOSÃO" if kind == "mine" else SOLDIER_DATA[kind]["role"]
            txt(self.screen, name, self.font_xs, WHITE, (rect.x + 72, rect.y + 5))
            txt(self.screen, f"{cost} SUP", self.font_xs, YELLOW, (rect.x + 72, rect.y + 23))
            txt(self.screen, role, self.font_xs, TEXT, (rect.x + 72, rect.y + 41))

    def draw_card_art(self, kind, rect, small=False):
        cx, cy = rect.centerx, rect.centery + 4
        if kind == "mine":
            pygame.draw.circle(self.screen, STEEL_DARK, (cx, cy), 20 if small else 28); pygame.draw.circle(self.screen, RED, (cx, cy), 5); return
        data = SOLDIER_DATA[kind]
        body = data["color"]
        pygame.draw.ellipse(self.screen, (32, 38, 32), (cx - 22, cy + 14, 44, 9))
        if kind in ("patrol_boat",):
            pygame.draw.polygon(self.screen, body, [(cx - 25, cy + 2), (cx + 26, cy + 2), (cx + 17, cy + 17), (cx - 20, cy + 17)])
            pygame.draw.rect(self.screen, WHITE, (cx - 7, cy - 12, 14, 12), border_radius=3)
            return
        if kind in ("submarine", "water_bomb"):
            if kind == "submarine": pygame.draw.ellipse(self.screen, body, (cx - 25, cy - 6, 50, 22)); pygame.draw.rect(self.screen, STEEL, (cx - 3, cy - 16, 10, 8), border_radius=2)
            else: pygame.draw.circle(self.screen, body, (cx, cy + 2), 22); pygame.draw.circle(self.screen, CYAN, (cx, cy + 2), 8)
            return
        if kind == "scout_buggy":
            pygame.draw.rect(self.screen, body, (cx - 28, cy - 4, 56, 20), border_radius=6); pygame.draw.circle(self.screen, BLACK, (cx - 19, cy + 17), 8); pygame.draw.circle(self.screen, BLACK, (cx + 19, cy + 17), 8); return
        if kind == "bomber": pygame.draw.rect(self.screen, body, (cx - 15, cy - 11, 30, 30), border_radius=5)
        else: pygame.draw.rect(self.screen, body, (cx - 14, cy - 12, 28, 27), border_radius=6)
        pygame.draw.circle(self.screen, SKIN, (cx, cy - 24), 11)
        pygame.draw.ellipse(self.screen, UNIFORM_DARK, (cx - 13, cy - 35, 26, 13))
        if kind in ("lieutenant", "general", "sniper", "grenadier", "special_forces", "engineer", "flamethrower", "shotgunner", "radio_operator", "drone_operator", "cryo_operator", "mortar"):
            length = 37 if kind != "sniper" else 50
            pygame.draw.line(self.screen, STEEL_DARK, (cx + 4, cy - 7), (cx + length, cy - 14), 5)
        if kind == "vanguard": pygame.draw.polygon(self.screen, STEEL, [(cx + 2, cy - 17), (cx + 23, cy - 13), (cx + 22, cy + 15), (cx + 5, cy + 20), (cx, cy + 3)])
        if kind == "rambo": pygame.draw.line(self.screen, STEEL_LIGHT, (cx + 3, cy - 2), (cx + 18, cy - 12), 3); pygame.draw.line(self.screen, STEEL_LIGHT, (cx + 5, cy + 3), (cx + 21, cy + 0), 3)
        if kind == "flamethrower": pygame.draw.line(self.screen, ORANGE, (cx + 8, cy - 7), (cx + 31, cy - 13), 7)
        if kind == "engineer": pygame.draw.rect(self.screen, SAND, (cx - 28, cy - 4, 13, 17), border_radius=2)
        if kind == "radio_operator": pygame.draw.rect(self.screen, STEEL_DARK, (cx - 29, cy - 3, 12, 18), border_radius=2)
        if kind == "drone_operator": pygame.draw.circle(self.screen, STEEL, (cx + 22, cy - 29), 6)
        if kind == "mortar": pygame.draw.line(self.screen, STEEL_DARK, (cx + 7, cy + 4), (cx + 20, cy - 22), 6)

    def phase_rects(self):
        result = {}
        for i, key in enumerate(PHASES):
            col = i % 2; row = i // 2
            result[key] = pygame.Rect(88 + col * 560, 165 + row * 215, 520, 185)
        return result

    def draw_title(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA); overlay.fill((5, 8, 7, 175)); self.screen.blit(overlay, (0, 0))
        txt(self.screen, "SOLDADOS VS ZUMBIS", self.font_title, WHITE, (WIDTH // 2, 145), True)
        txt(self.screen, "OPERAÇÃO ÚLTIMO POSTO", self.font, YELLOW, (WIDTH // 2, 212), True)
        txt(self.screen, "Estratégia por pistas • esquadrão • hordas • chefes • 4 operações", self.font_small, TEXT, (WIDTH // 2, 248), True)
        lines = ["Avance pela campanha: GRAMA → NEVE → DESERTO → ÁGUA.", "Antes de cada operação você pode trocar as 7 cartas do esquadrão.", "O MÉDICO é uma ferramenta de remoção no painel preto — não ocupa carta."]
        yy = 302
        for line in lines: txt(self.screen, line, self.font_small, TEXT, (WIDTH // 2, yy), True); yy += 28
        b = pygame.Rect(WIDTH // 2 - 180, 480, 360, 68); panel(self.screen, b, (52, 120, 67), YELLOW, 2, 12)
        txt(self.screen, "COMEÇAR OPERAÇÃO", self.font, WHITE, b.center, True)

    def draw_phases(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA); overlay.fill((8, 13, 11, 220)); self.screen.blit(overlay, (0, 0))
        txt(self.screen, "MAPA DA CAMPANHA", self.font_title, WHITE, (WIDTH // 2, 72), True)
        txt(self.screen, "As operações são desbloqueadas em sequência.", self.font_small, TEXT, (WIDTH // 2, 113), True)
        self.phase_select_rects = self.phase_rects()
        order = list(PHASES.keys())
        for key, rect in self.phase_select_rects.items():
            p = PHASES[key]
            locked = order.index(key) > self.unlocked_phase_index
            panel(self.screen, rect, PANEL2 if not locked else (28, 30, 29), p["color"] if not locked else (72, 76, 73), 3, 16)
            # miniature landscape
            art = pygame.Rect(rect.x + 18, rect.y + 18, 170, 148); pygame.draw.rect(self.screen, p["color"], art, border_radius=10)
            if key == "grass":
                pygame.draw.rect(self.screen, (82, 143, 67), (art.x, art.y + 86, art.w, 62), border_radius=8)
                for xx in range(art.x + 15, art.right, 35): pygame.draw.line(self.screen, (151, 184, 94), (xx, art.y + 100), (xx + 5, art.y + 91), 2)
            elif key == "snow":
                pygame.draw.rect(self.screen, (224, 235, 238), (art.x, art.y + 86, art.w, 62), border_radius=8)
                pygame.draw.polygon(self.screen, WHITE, [(art.x + 10, art.bottom - 8), (art.x + 70, art.y + 55), (art.x + 130, art.bottom - 8)])
            elif key == "desert":
                pygame.draw.rect(self.screen, (205, 163, 94), (art.x, art.y + 86, art.w, 62), border_radius=8)
                pygame.draw.circle(self.screen, YELLOW, (art.x + 130, art.y + 40), 18)
            else:
                pygame.draw.rect(self.screen, (46, 132, 159), (art.x, art.y + 65, art.w, 83), border_radius=8)
                pygame.draw.line(self.screen, WHITE, (art.x + 18, art.y + 98), (art.right - 20, art.y + 98), 2)
                pygame.draw.line(self.screen, WHITE, (art.x + 36, art.y + 120), (art.right - 35, art.y + 120), 2)
            txt(self.screen, p["name"], self.font, WHITE, (rect.x + 208, rect.y + 25))
            txt(self.screen, p["subtitle"], self.font_small, TEXT, (rect.x + 208, rect.y + 55))
            txt(self.screen, "CARTAS ESPECIAIS: " + (", ".join(SOLDIER_DATA[k]["name"] for k in p["special"]) if p["special"] else "NENHUMA"), self.font_xs, YELLOW, (rect.x + 208, rect.y + 92))
            if key == "water": txt(self.screen, "LINHA 3 = ÁGUA", self.font_small, CYAN, (rect.x + 208, rect.y + 122))
            if locked:
                shade = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA); shade.fill((0, 0, 0, 125)); self.screen.blit(shade, rect.topleft)
                txt(self.screen, "🔒 BLOQUEADA", self.font, WHITE, rect.center, True)
            else:
                txt(self.screen, "DISPONÍVEL", self.font_xs, GREEN, (rect.x + 208, rect.y + 157))
        txt(self.screen, "As operações são liberadas uma por vez. Clique na próxima operação disponível.", self.font_small, TEXT, (WIDTH // 2, 675), True)

    def selection_rects(self):
        rects = {}
        for idx, kind in enumerate(self.selection_candidates):
            col = idx % 5; row = idx // 5
            rects[kind] = pygame.Rect(24 + col * 247, 150 + row * 92, 237, 80)
        return rects

    def draw_selection(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA); overlay.fill((7, 12, 10, 235)); self.screen.blit(overlay, (0, 0))
        txt(self.screen, PHASES[self.phase_key]["name"], self.font_title, WHITE, (WIDTH // 2, 53), True)
        txt(self.screen, f"ESCOLHA 7 CARTAS — TODAS AS CARTAS DISPONÍVEIS — {len(self.selected_cards)}/7", self.font, YELLOW, (WIDTH // 2, 86), True)
        txt(self.screen, "Todas as cartas podem ser escolhidas em qualquer fase. A campanha é que avança em ordem.", self.font_small, TEXT, (WIDTH // 2, 112), True)
        rects = self.selection_rects()
        for kind, rect in rects.items():
            active = kind in self.selected_cards
            fill = (46, 69, 51) if active else PANEL2
            border = GREEN if active else BORDER
            panel(self.screen, rect, fill, border, 2 if not active else 3, 9)
            art = pygame.Rect(rect.x + 7, rect.y + 6, 58, 66)
            pygame.draw.rect(self.screen, BLACK, art, border_radius=8)
            self.draw_card_art(kind, art, small=False)
            name = "MINA" if kind == "mine" else SOLDIER_DATA[kind]["name"]
            cost = 75 if kind == "mine" else SOLDIER_DATA[kind]["cost"]
            role = "EXPLOSÃO" if kind == "mine" else SOLDIER_DATA[kind]["role"]
            phase_req = None if kind == "mine" else SOLDIER_DATA[kind].get("phase")
            restriction = "SÓ NA ÁGUA" if phase_req == "water" else ("SÓ NO DESERTO" if phase_req == "desert" else ("SÓ NA NEVE" if phase_req == "snow" else role))
            txt(self.screen, name, self.font_xs, WHITE, (rect.x + 74, rect.y + 7))
            txt(self.screen, f"{cost} SUP", self.font_xs, YELLOW, (rect.x + 74, rect.y + 28))
            txt(self.screen, restriction, self.font_xs, CYAN if phase_req else TEXT, (rect.x + 74, rect.y + 48))
            if active:
                pygame.draw.circle(self.screen, GREEN, (rect.right - 18, rect.y + 18), 10)
                pygame.draw.line(self.screen, WHITE, (rect.right - 24, rect.y + 18), (rect.right - 19, rect.y + 23), 2)
                pygame.draw.line(self.screen, WHITE, (rect.right - 19, rect.y + 23), (rect.right - 12, rect.y + 14), 2)
        button = pygame.Rect(WIDTH // 2 - 160, 664, 320, 44)
        panel(self.screen, button, (53, 123, 68) if len(self.selected_cards) == 7 else PANEL3, YELLOW if len(self.selected_cards) == 7 else BORDER, 2, 11)
        txt(self.screen, "IR PARA A BATALHA", self.font, WHITE, button.center, True)

    def draw_units(self):
        for mine in self.field_mines: mine.draw(self.screen)
        for soldier in self.soldiers: soldier.draw(self.screen)
        for z in self.zombies: z.draw(self.screen)
        for lane, x in self.supply_drops:
            y = BOARD_Y + lane * CELL_H + CELL_H // 2 + 25
            pygame.draw.ellipse(self.screen, (45, 52, 42), (x - 30, y + 12, 60, 12))
            pygame.draw.rect(self.screen, WOOD_DARK, (x - 27, y - 15, 54, 33), border_radius=4)
            pygame.draw.rect(self.screen, SAND, (x - 24, y - 12, 48, 27), border_radius=3)
            pygame.draw.line(self.screen, WOOD, (x, y - 12), (x, y + 15), 4)
            txt(self.screen, "+25", self.font_xs, WHITE, (x, y - 28), True)
        for projectile in self.projectiles: self.screen.blit(projectile.image, projectile.rect)
        for shell in self.shells: shell.draw(self.screen)
        for effect in self.effects: effect.draw(self.screen, self.font_xs if isinstance(effect, Explosion) else self.font_small)

    def draw_message(self):
        if self.message_timer <= 0: return
        box = pygame.Rect(WIDTH // 2 - 235, HEIGHT - 40, 470, 28); panel(self.screen, box, PANEL, BORDER, 1, 7); txt(self.screen, self.message, self.font_xs, WHITE, box.center, True)

    def draw_end(self, victory):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA); overlay.fill((0, 0, 0, 185)); self.screen.blit(overlay, (0, 0))
        txt(self.screen, "MISSÃO CUMPRIDA!" if victory else "A BASE CAIU!", self.font_title, YELLOW if victory else RED, (WIDTH // 2, 185), True)
        txt(self.screen, f"Operação: {PHASES[self.phase_key]['name']}", self.font, WHITE, (WIDTH // 2, 270), True)
        txt(self.screen, f"PONTOS: {self.score}  |  BAIXAS: {self.kills}", self.font_small, TEXT, (WIDTH // 2, 312), True)
        next_label = "PRÓXIMA OPERAÇÃO" if PHASES[self.phase_key] is not PHASES["water"] else "NOVA CAMPANHA"
        b = pygame.Rect(WIDTH // 2 - 180, 545, 360, 54); panel(self.screen, b, (54, 125, 73), YELLOW, 2, 10); txt(self.screen, next_label, self.font, WHITE, b.center, True)

    def draw(self):
        self.draw_background()
        if self.mode == "title": self.draw_title(); return
        if self.mode == "phases": self.draw_phases(); return
        if self.mode == "select": self.draw_selection(); return
        self.draw_board(); self.draw_base(); self.draw_hud(); self.draw_cards(); self.draw_units(); self.draw_message()
        if self.banner_timer > 0: txt(self.screen, f"ONDA {self.wave}", self.font_big, WHITE, (WIDTH // 2, 132), True)
        if self.horde_active: txt(self.screen, "HORDA!", self.font_big, RED, (WIDTH // 2, 163), True)
        if self.mode == "paused":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA); overlay.fill((0,0,0,150)); self.screen.blit(overlay,(0,0)); txt(self.screen,"PAUSADO",self.font_title,WHITE,(WIDTH//2,300),True); txt(self.screen,"P para continuar",self.font, TEXT,(WIDTH//2,355),True)
        elif self.mode == "victory": self.draw_end(True)
        elif self.mode == "defeat": self.draw_end(False)


def main():
    Game().run()


if __name__ == "__main__":
    main()

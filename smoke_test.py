"""Checks without opening a visible window.

Run with: python smoke_test.py
"""

import hashlib
import os
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from main import (
    ASSET_DIR,
    BOARD,
    CARD_RECHARGE_SECONDS,
    CELL_W,
    ROWS,
    LANE_BOUNDS,
    BOSSES,
    CARD_ART_ASSETS,
    CARD_ATLAS_INDEX,
    BEACH_WATER_ENEMIES,
    DEFENSES,
    DIFFICULTIES,
    ENEMIES,
    PROMOTIONS,
    REGION_ROSTERS,
    REGION_ENEMIES,
    REGIONS,
    VERSION,
    Assets,
    ActorMotion,
    Battle,
    Defender,
    Enemy,
    Game,
    Projectile,
    SpawnOrder,
    VisualEffect,
    boss_damage_scale,
    boss_wave_scale,
    cell_center,
    defender_render_scale,
    enemy_damage_scale,
    enemy_render_scale,
    enemy_wave_scale,
    lane_bounds,
    lane_depth,
    regional_sprite_index,
    terrain_y,
    weapon_reload_seconds,
    wave_enemy_pool,
)

from opengl_presenter import ActorCommand, OpenGLPresenter


def load_to_title(game: Game) -> None:
    assert game.scene == "loading"
    for _ in range(game.assets.total + 3):
        game.update(1 / 60)
        game.draw()
        if game.scene == "title":
            break
    assert game.scene == "title"
    assert game.assets.complete


def main() -> None:
    game = Game()
    load_to_title(game)

    # A abertura pré-carrega todos os cenários, atlases, cartas especiais,
    # estados de inimigo, ações completas dos nove chefes e folhas raster de
    # matéria, impacto e projéteis antes de liberar o menu.
    assert VERSION == "BETA 4"
    assert game.assets.total == 47
    assert {"loading_beta3", "zombie_jumper_beta3", "zombie_crawler_beta3"} <= set(game.assets.images)
    assert game.assets.images["loading_beta3"].get_size() == (1280, 720)
    assert hashlib.sha256((ASSET_DIR / "loading_beta3_reference.png").read_bytes()).hexdigest() == "39f4406767231aed591a1738d12c67be1d60b220ba782d58ad9f4edc275f548f"
    assert hashlib.sha256((ASSET_DIR / "zombie_jumper_beta3.png").read_bytes()).hexdigest() == "0364d9c3510540f2acc419a0b38fd59555c5b758c9b2d02b6f76e9d47364c262"
    assert hashlib.sha256((ASSET_DIR / "zombie_crawler_beta3.png").read_bytes()).hexdigest() == "a8cba9727cd36f606cdd5ae21534201caa1463dfbe11c7033e2d7a9606a635a5"
    assert hashlib.sha256((ASSET_DIR / "city_walker_walk_sheet_beta4.png").read_bytes()).hexdigest() == "310c3324dcafad90d73c78c57dc342d018d731a0c38c09d1bb7d3d0cf943500d"
    assert hashlib.sha256((ASSET_DIR / "desert_digger_state_sheet_beta4.png").read_bytes()).hexdigest() == "89fa24d2c1e81b7ca14a3337fe6d95aad9f518ec9df86b4043aa7963e1b82138"
    assert hashlib.sha256((ASSET_DIR / "beach_swimmer_walk_sheet_beta4.png").read_bytes()).hexdigest() == "5d29de9959f4a6a041ebbf65c0d8b78f2c47073f5022ac33c0fe0c9372ccf019"
    assert hashlib.sha256((ASSET_DIR / "city_beta4_four_lanes.png").read_bytes()).hexdigest() == "14b8b6a9aaf4ec67a2745271b529c64891c662b6e718ec422f558d2d7fc5f0b4"
    assert hashlib.sha256((ASSET_DIR / "desert_beta4_four_lanes.png").read_bytes()).hexdigest() == "2ee660499b1a77e1f618ba4496d79f6d093deebc9b124d80dfb63c602428997a"
    assert hashlib.sha256((ASSET_DIR / "beach_beta4_four_lanes.png").read_bytes()).hexdigest() == "d7c9b8ed8e9208c8e2db29d282213615471adb27fd4ca0a0d27b2c93e60ab80e"
    assert hashlib.sha256((ASSET_DIR / "city_boss_actions_beta4.png").read_bytes()).hexdigest() == "4f5b5ae219ae3c50f37b2d7287a14d19383c46e8693441783c39a43c8d3fc5ce"
    assert hashlib.sha256((ASSET_DIR / "desert_boss_actions_beta4.png").read_bytes()).hexdigest() == "1d1648621bdd3f06a6df3f11da45287927a0e8b284d820c05c6f4a355132b6a3"
    assert hashlib.sha256((ASSET_DIR / "beach_boss_actions_beta4.png").read_bytes()).hexdigest() == "93ecbacd7defa7855e9019a4217e4a9b104413a4f19445d129f7313fca373bd6"
    assert hashlib.sha256((ASSET_DIR / "elemental_effects_sheet_beta4.png").read_bytes()).hexdigest() == "a7715efd057d75fc7e7ce544f0c0785f18bc881e30005e4bac6684d42c3cabd3"
    assert hashlib.sha256((ASSET_DIR / "combat_effects_sheet_beta4.png").read_bytes()).hexdigest() == "994fe83dc19d4b1c84f0689c38309131dc4c6770825622a4f2b986f6a7ee08d9"
    assert hashlib.sha256((ASSET_DIR / "ability_effects_sheet_beta4.png").read_bytes()).hexdigest() == "84c58e3aa7845a1c5be90384074d182a39727e1ee845722142978f00f8932f7b"
    assert hashlib.sha256((ASSET_DIR / "projectile_sprites_sheet_beta4.png").read_bytes()).hexdigest() == "fe6e33b3971bcab54ae75cc68c7e0ecde0a27126a379b03c3c13ac18c3f42775"
    assert hashlib.sha256((ASSET_DIR / "beach_soldiers_beta4_rebuilt.png").read_bytes()).hexdigest() == "228cd15bb688445f185fd52558317945d2ffb8370d88e9b036b1b3f718b4507c"
    assert hashlib.sha256((ASSET_DIR / "beach_soldiers_l2_beta4_rebuilt.png").read_bytes()).hexdigest() == "3c2d49b830a8dfcfaf9fe4dbeb1e71d6b809a5ef210930dfb90d6c456d5723a8"
    assert hashlib.sha256((ASSET_DIR / "beach_zombies_beta4_rebuilt.png").read_bytes()).hexdigest() == "52210ba9ac0a959621ba9b05a360f42f08bf4ed094fc216f8c2a6f7881f76383"
    assert game.assets.images["zombie_crawler_beta3"] is not game.assets.images["zombie_jumper_beta3"]
    assert len(game.assets.animation_frames["city_walker_walk"]) == 8
    assert len(game.assets.animation_frames["desert_digger_states"]) == 8
    assert len(game.assets.animation_frames["beach_swimmer_walk"]) == 8
    assert all(len(game.assets.animation_frames[f"{region}_boss_actions"]) == 12 for region in REGIONS)
    assert all(len(game.assets.effect_frames[name]) == 12 for name in ("elemental_effects", "combat_effects", "ability_effects", "projectile_sprites"))
    assert all(
        frame.get_at((0, 0)).a == 0
        for name in ("city_walker_walk", "desert_digger_states", "beach_swimmer_walk")
        for frame in game.assets.animation_frames[name]
    )
    assert all(
        frame.get_bounding_rect(min_alpha=8).width > 0
        and frame.get_bounding_rect(min_alpha=8).height > 0
        for name in ("city_boss_actions", "desert_boss_actions", "beach_boss_actions")
        for frame in game.assets.animation_frames[name]
    )
    toxic_impact = game.assets.images["beta4_toxic_impact"]
    assert toxic_impact.get_width() > 128 and toxic_impact.get_height() > 128
    assert toxic_impact.get_at((0, 0)).a == 0
    assert all(f"{region}_bg" in game.assets.images for region in REGIONS)
    assert {REGIONS[region]["bg"] for region in REGIONS} == {
        "city_beta4_four_lanes.png",
        "desert_beta4_four_lanes.png",
        "beach_beta4_four_lanes.png",
    }
    assert REGIONS["beach"]["soldiers"] == "beach_soldiers_beta4_rebuilt.png"
    assert REGIONS["beach"]["soldiers_l2"] == "beach_soldiers_l2_beta4_rebuilt.png"
    assert REGIONS["beach"]["zombies"] == "beach_zombies_beta4_rebuilt.png"
    assert {"lane_bomb_cart", "desert_lane_bomb_cart", "beach_land_bomb_cart", "beach_water_bomb"} <= set(game.assets.images)
    assert {
        "city_mine_n1",
        "city_mine_n2",
        "beach_mine_land_n1",
        "beach_mine_land_n2",
        "beach_mine_water",
        "beach_boat_shooter",
        "beach_water_launcher_n1",
        "beach_water_cannon_n2",
        "city_poison_sprayer_n1",
        "city_poison_cannon_n2",
    } <= set(game.assets.images)
    assert set(CARD_ART_ASSETS.values()) <= set(game.assets.images)
    assert all(region in game.assets.unit_sprites for region in REGIONS)
    assert all(region in game.assets.unit_l2_sprites for region in REGIONS)
    assert all(region in game.assets.zombie_sprites for region in REGIONS)
    assert all(len(sprites) == 12 for sprites in game.assets.unit_sprites.values())
    assert all(len(sprites) == 12 for sprites in game.assets.unit_l2_sprites.values())
    assert all(len(sprites) == 12 for sprites in game.assets.zombie_sprites.values())
    assert game.assets.unit("city", 3, 1) is not game.assets.unit("city", 3, 2)
    assert game.card_sprite("city", "mina", 11) is game.assets.images["city_mine_n1"]
    assert game.card_sprite("city", "mina_segura", 11) is game.assets.images["city_mine_n2"]
    assert game.card_sprite("beach", "mina", 11) is game.assets.images["beach_mine_land_n1"]
    assert game.card_sprite("beach", "mina_segura", 11) is game.assets.images["beach_mine_land_n2"]
    assert game.card_sprite("beach", "bomba_agua", 11) is game.assets.images["beach_mine_water"]
    assert game.card_sprite("beach", "atirador_lancha", 5) is game.assets.images["beach_boat_shooter"]
    assert game.card_sprite("beach", "lancador_agua", 9) is game.assets.images["beach_water_launcher_n1"]
    assert game.card_sprite("beach", "canhao_mare", 9) is game.assets.images["beach_water_cannon_n2"]
    assert game.card_sprite("city", "lancador_veneno", 9) is game.assets.images["city_poison_sprayer_n1"]
    assert game.card_sprite("city", "canhao_veneno", 9) is game.assets.images["city_poison_cannon_n2"]
    for (region, key), asset_key in CARD_ART_ASSETS.items():
        assert game.card_sprite(region, key, regional_sprite_index(region, key)) is game.assets.images[asset_key]
    for region, mapping in CARD_ATLAS_INDEX.items():
        for key, expected_index in mapping.items():
            assert regional_sprite_index(region, key) == expected_index

    # A Beta 4 não usa contagem fixa de arquivos nem quadros amarrados a uma
    # animação específica: os estados passam por dt e retornam ao ciclo-base.
    motion = ActorMotion()
    motion.advance(0.10, "walk")
    assert motion.state == "spawn"
    motion.advance(0.20, "walk")
    assert motion.state == "walk"
    motion.trigger("attack", 0.24)
    motion.advance(0.10, "walk")
    assert motion.state == "attack" and motion.phase() in {0, 1, 2, 3}
    motion.advance(0.20, "walk")
    assert motion.state == "walk"

    # Cada cenário possui limites medidos na própria pintura. O contato com o
    # chão é horizontal, não deriva com X, e a escala cria profundidade sem
    # alterar a linha lógica na qual o inimigo nasceu.
    for region, bounds in LANE_BOUNDS.items():
        centers = [terrain_y(region, row, BOARD.left) for row in range(ROWS)]
        assert centers == sorted(centers) and len(set(centers)) == ROWS
        for row, center in enumerate(centers):
            top, bottom = lane_bounds(region, row)
            assert (top, bottom) == (float(bounds[row]), float(bounds[row + 1]))
            assert top < center < bottom
            assert terrain_y(region, row, BOARD.left) == terrain_y(region, row, BOARD.right)
            assert cell_center(row, 0, region)[1] == cell_center(row, 8, region)[1] == center
        assert lane_depth(region, 0) < lane_depth(region, ROWS - 1)
    assert LANE_BOUNDS["beach"] == (170, 305, 440, 575, 710)
    assert cell_center(2, 4, "beach")[1] == 507.5
    # A água já estava proporcional e preserva sua escala. Em terra, o recorte
    # dos atlases zumbis tem mais respiro, então a caixa agora fica claramente
    # maior que a humana sem escapar da própria faixa.
    for row in range(ROWS):
        defender = Defender("recruta", "Guarda-Costa", row, 3, DEFENSES["recruta"], 0, region="beach")
        lane_height = lane_bounds("beach", row)[1] - lane_bounds("beach", row)[0]
        assert defender_render_scale(defender)[1] <= lane_height * 0.94
        if row in {1, 2}:
            enemy = Enemy("boia", row, ENEMIES["boia"], "beach", 3)
            assert enemy_render_scale(enemy, "beach")[1] <= lane_height * 0.92
        else:
            enemy = Enemy("cowboy", row, ENEMIES["cowboy"], "beach", 3)
            assert enemy_render_scale(enemy, "beach")[1] >= defender_render_scale(defender)[1] * 1.12
            assert enemy_render_scale(enemy, "beach")[1] <= lane_height * 1.02
    for region in ("city", "desert"):
        for row in range(ROWS):
            defender = Defender("recruta", "Patrulheiro", row, 3, DEFENSES["recruta"], 0, region=region)
            enemy = Enemy("caminhante", row, ENEMIES["caminhante"], region, 3)
            assert enemy_render_scale(enemy, region)[1] >= defender_render_scale(defender)[1] * 1.12
    assert game.presenter is None  # SDL dummy sempre exercita o fallback seguro.
    assert game.renderer_label.startswith("Pygame")
    assert OpenGLPresenter.STATE_CODES["walk"] != OpenGLPresenter.STATE_CODES["attack"]
    assert OpenGLPresenter.STATE_CODES["reload"] not in {
        OpenGLPresenter.STATE_CODES["walk"],
        OpenGLPresenter.STATE_CODES["attack"],
    }
    actor_command = ActorCommand(
        game.assets.images["zombie_jumper_beta3"],
        900,
        cell_center(1, 4, "city")[1],
        80,
        96,
        "walk",
        0.25,
        enemy=True,
    )
    assert actor_command.ground_y == cell_center(1, 4, "city")[1]
    requirements = (Path(__file__).resolve().parent / "requirements.txt").read_text(encoding="utf-8")
    assert "pygame-ce==2.5.8" in requirements
    assert "PyOpenGL==3.1.10" in requirements
    assert "numpy==2.5.3" in requirements

    # The campaign intentionally has City, Desert and Beach only. Snow and
    # grass are not part of its regions, enemy families or asset loading.
    assert tuple(REGIONS) == ("city", "desert", "beach")
    assert "snow" not in REGIONS and "grass" not in REGIONS
    assert game.save["unlocked"] == list(REGIONS)
    assert all(len(roster) >= 10 for roster in REGION_ROSTERS.values())
    assert all(key in DEFENSES for roster in REGION_ROSTERS.values() for key, _ in roster)
    assert "mecanico" not in DEFENSES and "engenheiro" not in DEFENSES
    assert all(data["role"] != "medic" for data in DEFENSES.values())
    assert all(
        key not in {"mecanico", "engenheiro"}
        for roster in REGION_ROSTERS.values()
        for key, _display in roster
    )
    # O dossiê e as ondas usam o mesmo elenco: o primeiro encontro tem só a
    # ameaça-base, e até a onda 15 nenhum personagem regional fica de fora.
    for region, roster in REGION_ENEMIES.items():
        assert wave_enemy_pool(region, 1) == roster[:1]
        assert wave_enemy_pool(region, 15) == roster
        progression = [len(wave_enemy_pool(region, wave)) for wave in range(1, 16)]
        assert progression == sorted(progression)
    water_cards = {"atirador_lancha", "lancha", "submarino", "bomba_agua"}
    for ground_region in ("city", "desert"):
        assert water_cards.isdisjoint(game.regional_card_keys(ground_region))
        assert water_cards.isdisjoint(game.available_selection_keys(ground_region))
    assert water_cards <= set(game.regional_card_keys("beach"))
    assert water_cards <= set(game.available_selection_keys("beach"))
    fire_cards = {"lanca_chamas_bolso", "lanca_chamas"}
    poison_cards = {"lancador_veneno", "canhao_veneno"}
    assert fire_cards <= set(game.regional_card_keys("desert"))
    assert fire_cards.isdisjoint(game.regional_card_keys("city"))
    assert fire_cards.isdisjoint(game.regional_card_keys("beach"))
    assert poison_cards <= set(game.regional_card_keys("city"))
    assert poison_cards.isdisjoint(game.regional_card_keys("desert"))
    assert poison_cards.isdisjoint(game.regional_card_keys("beach"))
    game.region, game.dossier_kind = "city", "units"
    assert all(item.get("l1") not in water_cards and item.get("l2") not in water_cards for item in game.dossier_items())
    game.region = "beach"
    assert any(item.get("l1") == "atirador_lancha" and item.get("l2") == "lancha" for item in game.dossier_items())
    assert any(item.get("l1") == "lancador_agua" and item.get("l2") == "canhao_mare" for item in game.dossier_items())
    game.region = "beach"
    card_layout = {key: rect for key, _display, rect in game.selection_cards()}
    assert "atirador_lancha" in card_layout and "lancha" in card_layout
    assert card_layout["atirador_lancha"].x == card_layout["lancha"].x
    assert card_layout["atirador_lancha"].y + 126 == card_layout["lancha"].y
    assert len({(rect.x, rect.y, rect.width, rect.height) for rect in card_layout.values()}) == len(card_layout)

    # A escolha de modo acontece antes do mapa. Ela limita as cartas de fato,
    # não apenas o texto da interface; além disso, nenhuma grade mistura N1
    # com N1 ou sobrepõe cartas nos três cenários.
    game.scene = "title"
    game.click_title(game.title_buttons()[0][1].center)
    assert game.scene == "difficulty"
    game.click_difficulty(game.difficulty_buttons()[0][1].center)
    assert game.difficulty == "easy" and game.scene == "campaign"
    expected_levels = {"easy": {2}, "medium": {1, 2}, "hard": {1}}
    mode_wave_sizes = {}
    mode_opening_sizes = {}
    for mode, levels in expected_levels.items():
        game.difficulty = mode
        game.scene = "difficulty"
        game.draw()
        for region in REGIONS:
            selectable = game.available_selection_keys(region)
            assert selectable
            # O Sargento N2 é a única exceção deliberada do modo Difícil:
            # não existe nas telas de Fácil/Médio e compensa o elenco só N1.
            assert ("instrutor" in selectable) == (mode == "hard")
            assert {DEFENSES[key]["level"] for key in selectable if key != "instrutor"} <= levels
            game.enter_selection(region)
            assert len(game.selection) == 8
            assert {DEFENSES[key]["level"] for key, _display in game.selection if key != "instrutor"} <= levels
            cards = game.selection_cards()
            assert len({key for key, _display, _rect in cards}) == len(cards)
            for index, (_key, _display, rect) in enumerate(cards):
                assert all(not rect.colliderect(other) for _other_key, _other_display, other in cards[index + 1:])

            # Cada nível recebe uma silhueta própria. Este teste falha se uma
            # N2 voltar a apontar para a mesma superfície de outra carta, que
            # foi exatamente o defeito relatado na montagem dos três mapas.
            for level in levels:
                level_sprites = [
                    game.card_sprite(region, key, regional_sprite_index(region, key))
                    for key in selectable
                    if DEFENSES[key]["level"] == level
                ]
                assert len({id(sprite) for sprite in level_sprites}) == len(level_sprites)

            # A chave, o retrato, a ficha de hover e a unidade posicionada
            # precisam continuar sendo a mesma carta. Testamos todas as
            # cartas visíveis, não só as oito pré-selecionadas.
            for key, display, rect in cards:
                game.selection = []
                game.click_selection(rect.center)
                assert game.selection == [(key, display)]
                pygame.event.post(pygame.event.Event(pygame.MOUSEMOTION, {"pos": rect.center}))
                game.handle_events()
                assert game.hover_card == (key, display)
                assert DEFENSES[game.hover_card[0]]["ability"] == DEFENSES[key]["ability"]
                game.click_selection(rect.center)
                assert not game.selection

                card_surface = game.card_sprite(region, key, regional_sprite_index(region, key))
                placement = Battle(game, region, [(key, display)])
                placement.supplies = 9999
                placement.handle_click(placement.card_rects()[0].center)
                assert placement.card() == (key, display)
                assert placement.message.startswith(f"Selecionado: {display}")
                row = 2 if region == "beach" and DEFENSES[key].get("water_only") else 0
                allowed, _reason = placement.can_place(key, row, 2)
                # Uma carta visível agora sempre pertence ao mapa selecionado.
                # As marítimas aparecem somente na Praia e recebem a faixa de
                # canal; Cidade e Deserto nunca chegam a tentar uma carta de água.
                assert allowed
                placement.place(row, 2)
                assert placement.card_cooldowns[0] == CARD_RECHARGE_SECONDS == 10.0
                defender = placement.defenders[0]
                assert defender.key == key and defender.stats is DEFENSES[key]
                assert defender.sprite_index == regional_sprite_index(region, key)
                assert game.card_sprite(region, defender.key, defender.sprite_index) is card_surface
            if mode == "medium":
                layout = {key: rect for key, _display, rect in cards}
                for level_one, level_two in PROMOTIONS.items():
                    if level_one in layout and level_two in layout:
                        assert layout[level_one].x == layout[level_two].x
                        assert layout[level_two].y == layout[level_one].y + 126
        mode_selection = [
            (key, game.card_display_name("city", key))
            for key in game.available_selection_keys("city")[:8]
        ]
        mode_battle = Battle(game, "city", mode_selection)
        assert mode_battle.supplies == DIFFICULTIES[mode]["initial_supplies"]
        assert mode_battle.cores == DIFFICULTIES[mode]["initial_cores"]
        mode_opening_sizes[mode] = len(mode_battle.build_wave(1))
        mode_wave_sizes[mode] = len(mode_battle.build_wave(15))
    assert mode_wave_sizes["easy"] < mode_wave_sizes["medium"] < mode_wave_sizes["hard"]
    # A curva precisa continuar estritamente crescente, mas sem depender de
    # números congelados: os perfis podem ser refinados sem inverter Médio e
    # Difícil novamente.
    # A primeira onda usa quantidade inteira: Médio e Difícil podem ambos
    # arredondar para quatro invasores, mas nunca invertem a progressão.
    assert mode_opening_sizes["easy"] < mode_opening_sizes["medium"] <= mode_opening_sizes["hard"]
    easy_walker = Enemy("caminhante", 0, ENEMIES["caminhante"], "city", 8, difficulty="easy")
    medium_walker = Enemy("caminhante", 0, ENEMIES["caminhante"], "city", 8, difficulty="medium")
    hard_walker = Enemy("caminhante", 0, ENEMIES["caminhante"], "city", 8, difficulty="hard")
    assert easy_walker.max_hp < medium_walker.max_hp < hard_walker.max_hp
    difficulty_damage = {}
    for mode in expected_levels:
        game.difficulty = mode
        mode_damage_field = Battle(game, "city", mode_selection)
        mode_enemy = Enemy("caminhante", 0, ENEMIES["caminhante"], "city", 8, difficulty=mode)
        difficulty_damage[mode] = mode_damage_field.scaled_enemy_damage(mode_enemy, 100)
    difficulty_boss_hp = {
        mode: Enemy("bruto_demolidor", 0, BOSSES["bruto_demolidor"], "city", 5, difficulty=mode).max_hp
        for mode in expected_levels
    }
    assert difficulty_damage["easy"] < difficulty_damage["medium"] < difficulty_damage["hard"]
    assert difficulty_boss_hp["easy"] < difficulty_boss_hp["medium"] < difficulty_boss_hp["hard"]
    # Os três perfis preservam os valores fechados para a Beta 4.
    assert DIFFICULTIES["easy"]["initial_supplies"] == 390
    assert DIFFICULTIES["easy"]["enemy_hp"] == 1.20
    assert DIFFICULTIES["medium"]["initial_supplies"] == 128
    assert DIFFICULTIES["medium"]["enemy_hp"] == 1.36
    assert DIFFICULTIES["medium"]["enemy_damage"] == 1.36
    assert DIFFICULTIES["medium"]["boss_hp"] == 1.24
    assert DIFFICULTIES["medium"]["boss_damage"] == 1.24
    assert DIFFICULTIES["medium"]["spawn_count"] == 1.24
    assert DIFFICULTIES["medium"]["spawn_wait"] == 0.77
    assert DIFFICULTIES["medium"]["escort_count"] == 1.36
    assert DIFFICULTIES["medium"]["skill_cooldown"] == 0.86
    assert DIFFICULTIES["easy"]["skill_cooldown"] == 0.85
    assert DIFFICULTIES["hard"]["enemy_hp"] > 1.5
    assert DIFFICULTIES["hard"]["enemy_damage"] > 1.5
    # Os percentuais pedidos são preservados literalmente: 15% no Fácil,
    # 14% no Médio e uma frequência maior no Difícil. O Médio continua mais
    # exigente pelo conjunto de vida, dano, economia e tamanho das hordas.
    assert DIFFICULTIES["hard"]["skill_cooldown"] < DIFFICULTIES["easy"]["skill_cooldown"] < DIFFICULTIES["medium"]["skill_cooldown"]
    game.difficulty = "medium"
    game.region = "city"

    # All regions have a 15-wave director and boss milestones at 5, 10, 15.
    selection = list(REGION_ROSTERS["city"][:8])
    city = Battle(game, "city", selection)
    # A posição clicável usa os limites reais de cada faixa, inclusive o
    # canal estreito da Praia; nenhum clique no céu vira uma célula próxima.
    for region in REGIONS:
        click_field = Battle(game, region, selection)
        for row in range(ROWS):
            center = cell_center(row, 4, region)
            assert click_field.board_cell_at((int(center[0]), int(center[1]))) == (row, 4)
        assert click_field.board_cell_at((int(BOARD.centerx), int(LANE_BOUNDS[region][0] - 2))) is None
    first_wave = city.build_wave(1)
    final_wave = city.build_wave(15)
    assert len(first_wave) < len(final_wave)
    assert len(final_wave) >= 30 and enemy_wave_scale(15) > 2.0
    lane_locked = Enemy("caminhante", 3, ENEMIES["caminhante"], "city", 6, x=1020)
    locked_y = lane_locked.y
    city.enemies = [lane_locked]
    city.update_enemies(0.25)
    assert lane_locked.row == 3 and lane_locked.y == locked_y and lane_locked.x < 1020
    frames = game.assets.animation_frames["city_walker_walk"]
    lane_locked.motion.loop("walk")
    lane_locked.motion.state_elapsed = 0.0
    assert game.enemy_sprite(city, lane_locked) is frames[0]
    lane_locked.motion.state_elapsed = 0.21
    assert game.enemy_sprite(city, lane_locked) is not frames[0]
    for wave, boss_key in zip((5, 10, 15), REGIONS["city"]["bosses"]):
        wave_orders = city.build_wave(wave)
        assert any(order.boss and order.key == boss_key for order in wave_orders)
        assert boss_key in BOSSES

    # Marítimos são exclusivos da Praia e as duas faixas centrais são o único
    # lugar onde embarcações e bomba naval podem ser instaladas. As duas faixas
    # de areia seguem reservadas às tropas terrestres, inclusive ao novo
    # Lançador de Água, que combate da areia e não flutua no canal.
    assert "lancha" not in game.available_selection_keys("city")
    assert "lancha" not in game.available_selection_keys("desert")
    beach = Battle(game, "beach", [("lancha", "Lancha Patrulha"), ("recruta", "Guarda-Costa Recruta")])
    beach.supplies = 999
    assert beach.can_place("lancha", 2, 2)[0]
    assert not beach.can_place("lancha", 0, 2)[0]
    assert not beach.can_place("lancha", 4, 2)[0]
    assert not beach.can_place("recruta", 2, 2)[0]
    assert beach.can_place("recruta", 0, 2)[0]
    assert not beach.can_place("mina", 2, 2)[0]
    assert not beach.can_place("mina_segura", 2, 2)[0]
    assert beach.can_place("mina", 0, 2)[0]
    assert beach.can_place("bomba_agua", 2, 2)[0]
    assert not beach.can_place("bomba_agua", 0, 2)[0]
    assert beach.can_place("atirador_lancha", 2, 2)[0]
    assert not beach.can_place("atirador_lancha", 0, 2)[0]
    assert beach.can_place("lancador_agua", 0, 2)[0]
    assert not beach.can_place("lancador_agua", 2, 2)[0]
    boat_test = Battle(game, "beach", [("atirador_lancha", "Atirador de Lancha")])
    boat_test.supplies = 999
    boat_test.place(2, 2)
    assert boat_test.defenders[0].key == "atirador_lancha" and boat_test.defenders[0].stats["water_only"]
    # O cenário e a diretoria usam a mesma regra: todo zumbi aquático e todo
    # chefe da Praia nasce em uma das duas faixas do canal; as ameaças
    # costeiras terrestres nunca aparecem sobre a água.
    assert all(beach.spawn_row_for(key) in {1, 2} for key in BEACH_WATER_ENEMIES)
    beach_land_enemies = set(REGION_ENEMIES["beach"]) - BEACH_WATER_ENEMIES
    assert all(beach.spawn_row_for(key) not in {1, 2} for key in beach_land_enemies)
    for order in beach.build_wave(15):
        assert (order.row in {1, 2}) == (order.boss or order.key in BEACH_WATER_ENEMIES)

    # Containment is themed per region: City retains its urban cart, Desert
    # gets a dune charge, and Beach uses land carts plus a floating water mine.
    desert = Battle(game, "desert", list(REGION_ROSTERS["desert"][:8]))
    assert city.lane_bomb_asset_key(0) == "lane_bomb_cart"
    assert desert.lane_bomb_asset_key(0) == "desert_lane_bomb_cart"
    assert beach.lane_bomb_asset_key(0) == "beach_land_bomb_cart"
    assert beach.lane_bomb_asset_key(2) == "beach_water_bomb"

    # A placed defender can be deliberately recovered by the removal tool,
    # and every lane starts with a one-use bomb cart as final protection.
    beach.selected_card = 1
    beach.place(0, 2)
    placed = beach.defenders[0]
    supplies_before_remove = beach.supplies
    beach.remove_defender(0, 2)
    assert not beach.defenders and beach.supplies > supplies_before_remove
    emergency = Enemy("caminhante", 0, ENEMIES["caminhante"], "beach", 1, x=BOARD.left + 5)
    beach.enemies = [emergency]
    beach.update_enemies(0.1)
    beach.update_lane_bombs(0.1)
    assert len(beach.lane_bombs) == ROWS and beach.lane_bombs[0].state == "rolling"
    assert emergency not in beach.enemies

    # Pause freezes the simulation but remains immediately reversible through
    # the consolidated command shelf. The tactical-next button starts only an
    # intermission, never a second concurrent horde.
    frozen_intermission = beach.intermission
    beach.paused = True
    beach.update(0.5)
    assert beach.intermission == frozen_intermission
    beach.handle_click(beach.pause_rect().center)
    assert not beach.paused
    beach.handle_click(beach.next_wave_rect().center)
    assert beach.started_wave and beach.wave == 1

    # Ammunition remains finite, but each weapon now owns a long visible
    # reload. It cannot fire early and refills only when its 8–15 s cycle ends.
    recruit = Defender("recruta", "Recruta", 0, 1, DEFENSES["recruta"], 0)
    recruit.ammo = 0
    reload_time = weapon_reload_seconds(recruit.stats)
    assert reload_time == 9.0
    city.defenders = [recruit]
    city.update_defenders(0.1)
    assert recruit.reloading and recruit.motion.state == "reload" and recruit.ammo == 0
    reload_pose_start = recruit.motion.state_elapsed
    city.update_defenders(0.25)
    assert recruit.motion.state == "reload" and recruit.motion.state_elapsed > reload_pose_start
    city.update_defenders(reload_time - 0.45)
    assert recruit.reloading and recruit.ammo == 0
    city.update_defenders(0.2)
    assert not recruit.reloading and recruit.ammo == recruit.max_ammo
    assert weapon_reload_seconds(DEFENSES["morteiro_basico"]) == 15.0
    assert weapon_reload_seconds(DEFENSES["soldado"]) == 8.0
    assert all(
        8.0 <= weapon_reload_seconds(data) <= 15.0
        for data in DEFENSES.values()
        if int(data["ammo"]) > 0
    )

    # The new promotion card upgrades a nearby, real N1 card into the mapped
    # N2 card after its timer completes. It never grants the boss-only N3.
    promotion_field = Battle(game, "city", selection)
    instructor = Defender("instrutor", "Sargento", 1, 1, DEFENSES["instrutor"], 2)
    candidate = Defender("recruta", "Patrulheiro", 1, 2, DEFENSES["recruta"], 0)
    promotion_field.defenders = [instructor, candidate]
    instructor.utility_timer = 0
    promotion_field.update_defenders(0.1)
    assert PROMOTIONS["recruta"] == "soldado"
    assert candidate.key == "soldado" and candidate.stats["level"] == 2 and candidate.ascended == 0
    coastal_promotion = Battle(game, "beach", [("atirador_lancha", "Atirador de Lancha")])
    coastal_instructor = Defender("instrutor", "Sargento", 1, 1, DEFENSES["instrutor"], 2, region="beach")
    coastal_shooter = Defender("atirador_lancha", "Atirador de Lancha", 2, 2, DEFENSES["atirador_lancha"], 5, region="beach")
    coastal_promotion.defenders = [coastal_instructor, coastal_shooter]
    coastal_instructor.utility_timer = 0
    coastal_promotion.update_defenders(0.1)
    assert PROMOTIONS["atirador_lancha"] == "lancha"
    assert coastal_shooter.key == "lancha" and coastal_shooter.stats["level"] == 2

    # A Praia não recebe lança-chamas: sua dupla temática é Lançador de Água
    # -> Canhão de Maré. O jato extingue o fogo e aplica lentidão temporária,
    # sem reintroduzir cartas incendiárias fora do Deserto.
    water_promotion = Battle(game, "beach", [("lancador_agua", "Lançador de Água")])
    water_instructor = Defender("instrutor", "Sargento", 1, 1, DEFENSES["instrutor"], 2, region="beach")
    water_recruit = Defender("lancador_agua", "Lançador de Água", 1, 2, DEFENSES["lancador_agua"], 9, region="beach")
    water_promotion.defenders = [water_instructor, water_recruit]
    water_instructor.utility_timer = 0
    water_promotion.update_defenders(0.1)
    assert PROMOTIONS["lancador_agua"] == "canhao_mare"
    assert water_recruit.key == "canhao_mare" and water_recruit.stats["role"] == "waterjet"

    water_field = Battle(game, "beach", [("lancador_agua", "Lançador de Água")])
    water_launcher = Defender("lancador_agua", "Lançador de Água", 0, 2, DEFENSES["lancador_agua"], 9, region="beach")
    soaked_enemy = Enemy("caminhante", 0, ENEMIES["caminhante"], "beach", 4, x=water_launcher.x + CELL_W * 0.6)
    soaked_enemy.burn = 2.0
    water_field.defenders = [water_launcher]
    water_field.enemies = [soaked_enemy]
    water_field.update_defenders(0.1)
    assert any(projectile.kind == "waterjet" and projectile.effect == "water" for projectile in water_field.projectiles)
    water_field.update_projectiles(0.45)
    assert soaked_enemy.burn == 0 and soaked_enemy.soaked > 0
    assert any(effect.kind == "water_impact" for effect in water_field.effects)
    soaked_x = soaked_enemy.x
    water_field.update_enemies(1.0)
    assert 0 < soaked_x - soaked_enemy.x < float(soaked_enemy.data["speed"]) * 0.70

    # A Cidade possui agora uma dupla química independente. O projétil aplica
    # Envenenado, causa dano periódico e reduz o avanço em 12%, enquanto as
    # cartas de fogo ficam exclusivas do Deserto e receberam dano reforçado.
    assert PROMOTIONS["lancador_veneno"] == "canhao_veneno"
    assert DEFENSES["lanca_chamas_bolso"]["damage"] == 14
    assert DEFENSES["lanca_chamas"]["damage"] == 20
    poison_field = Battle(game, "city", [("lancador_veneno", "Pulverizador de Veneno")])
    poisoner = Defender("lancador_veneno", "Pulverizador de Veneno", 0, 2, DEFENSES["lancador_veneno"], 9, region="city")
    poisoned_enemy = Enemy("caminhante", 0, ENEMIES["caminhante"], "city", 4, x=poisoner.x + CELL_W * 0.6)
    poison_field.defenders = [poisoner]
    poison_field.enemies = [poisoned_enemy]
    poison_field.update_defenders(0.1)
    assert any(projectile.kind == "poison" and projectile.effect == "poison" for projectile in poison_field.projectiles)
    poison_field.update_projectiles(0.45)
    assert poisoned_enemy.poisoned > 4.0
    assert any(effect.kind == "toxic_impact" for effect in poison_field.effects)
    poisoned_hp = poisoned_enemy.hp
    poisoned_x = poisoned_enemy.x
    poison_field.defenders = []
    poison_field.update_enemies(0.5)
    assert poisoned_enemy.hp < poisoned_hp
    assert 0 < poisoned_x - poisoned_enemy.x < float(poisoned_enemy.data["speed"]) * 0.46

    flame_field = Battle(game, "desert", [("lanca_chamas_bolso", "Lança-Chamas de Mão")])
    burner = Defender("lanca_chamas_bolso", "Lança-Chamas de Mão", 0, 2, DEFENSES["lanca_chamas_bolso"], 10, region="desert")
    burning_enemy = Enemy("caminhante", 0, ENEMIES["caminhante"], "desert", 4, x=burner.x + CELL_W * 0.6)
    flame_field.defenders = [burner]
    flame_field.enemies = [burning_enemy]
    flame_field.update_defenders(0.1)
    assert any(projectile.kind == "flame" and projectile.effect == "flame" for projectile in flame_field.projectiles)
    flame_field.update_projectiles(0.45)
    burn_time = burning_enemy.burn
    assert any(effect.kind == "flame_impact" for effect in flame_field.effects)
    flame_field.defenders = []
    flame_field.update_enemies(0.5)
    assert 0 < burning_enemy.burn < burn_time

    # A melee contact cannot make a close-range weapon forget the target.
    # The enemy has slipped a few pixels past the defender's center, yet the
    # shotgun must still fire while the blocker is being attacked.
    contact_field = Battle(game, "city", selection)
    shotgun = Defender("escopeteiro", "Escopeteiro", 0, 2, DEFENSES["escopeteiro"], 3)
    engaged_enemy = Enemy("caminhante", 0, ENEMIES["caminhante"], "city", 4, x=shotgun.x - 35)
    contact_field.defenders = [shotgun]
    contact_field.enemies = [engaged_enemy]
    assert contact_field.target_in_range(shotgun) is engaged_enemy
    contact_field.update_defenders(0.1)
    assert any(projectile.friendly and projectile.target is engaged_enemy for projectile in contact_field.projectiles)
    mortar = Defender("morteiro_basico", "Morteiro", 0, 2, DEFENSES["morteiro_basico"], 5)
    contact_field.defenders = [mortar]
    assert contact_field.target_in_range(mortar, BOARD.width / 9 * 1.05) is None

    # O corpo a corpo também respeita a animação: iniciar a mordida não pode
    # retirar vida. O dano aparece somente quando o gesto alcança o contato.
    bite_field = Battle(game, "city", selection)
    bite_defender = Defender("soldado", "Fuzileiro", 1, 3, DEFENSES["soldado"], 1, region="city")
    bite_enemy = Enemy("caminhante", 1, ENEMIES["caminhante"], "city", 4, x=bite_defender.x + 28)
    bite_enemy.skill_timer = 999
    bite_field.defenders = [bite_defender]
    bite_field.enemies = [bite_enemy]
    hp_before_bite = bite_defender.hp
    bite_field.update_enemies(0.01)
    assert bite_enemy.attack_windup > 0 and bite_defender.hp == hp_before_bite
    bite_field.update_enemies(0.10)
    assert bite_defender.hp == hp_before_bite
    bite_field.update_enemies(0.12)
    assert bite_defender.hp < hp_before_bite

    # Saltador e Escavador não podem mais trocar de lugar instantaneamente.
    # O primeiro descreve um arco visível; o segundo entra, percorre o solo e
    # emerge após apenas a primeira defesa, sem causar dano grátis no salto.
    jump_field = Battle(game, "city", selection)
    jump_front = Defender("recruta", "Patrulheiro", 0, 6, DEFENSES["recruta"], 0)
    jumper = Enemy("saltador", 0, ENEMIES["saltador"], "city", 8, x=jump_front.x + 42)
    jump_field.defenders = [jump_front]
    jump_field.enemies = [jumper]
    jump_field.update_enemies(0.01)
    assert jumper.jump_state == "vault" and jumper.jump_used
    assert jumper.motion.state == "jump"
    jump_start, jump_end = jumper.jump_start_x, jumper.jump_end_x
    assert jumper.x == jump_start
    game.battle, game.scene = jump_field, "battle"
    game.draw()
    jump_pose_start = jumper.motion.state_elapsed
    jump_field.update_enemies(0.24)
    assert jump_end < jumper.x < jump_start and jumper.motion.state_elapsed > jump_pose_start
    jump_field.update_enemies(0.40)
    assert jumper.jump_state == "" and jumper.x == jump_end

    dig_field = Battle(game, "desert", list(REGION_ROSTERS["desert"][:8]))
    dig_front = Defender("recruta", "Batedor", 0, 6, DEFENSES["recruta"], 0, region="desert")
    dig_rear = Defender("recruta", "Batedor", 0, 3, DEFENSES["recruta"], 0, region="desert")
    digger = Enemy("digger", 0, ENEMIES["digger"], "desert", 8, x=dig_front.x + 42)
    dig_field.defenders = [dig_front, dig_rear]
    dig_field.enemies = [digger]
    front_hp, rear_hp = dig_front.hp, dig_rear.hp
    dig_field.update_enemies(0.01)
    assert digger.dig_state == "enter" and digger.dig_used and digger.burrowed
    assert digger.motion.state == "dig_enter"
    assert dig_front.hp == front_hp and dig_rear.hp == rear_hp
    game.battle, game.scene = dig_field, "battle"
    game.draw()
    dig_pose_start = digger.motion.state_elapsed
    dig_field.update_enemies(0.10)
    assert digger.motion.state == "dig_enter" and digger.motion.state_elapsed > dig_pose_start
    for _ in range(20):
        dig_field.update_enemies(0.10)
    assert digger.dig_state == "" and not digger.burrowed
    assert digger.x < dig_front.x - 55
    assert dig_front.hp == front_hp and dig_rear.hp == rear_hp

    # A morte remove o inimigo da lógica imediatamente, mas a silhueta ainda
    # cai por uma fração de segundo; isso evita desaparecimentos secos entre
    # um impacto e as partículas da explosão.
    fall_field = Battle(game, "city", selection)
    falling_enemy = Enemy("caminhante", 1, ENEMIES["caminhante"], "city", 4, x=760)
    fall_field.enemies = [falling_enemy]
    fall_field.kill_enemy(falling_enemy)
    assert not fall_field.enemies and len(fall_field.fallen) == 1
    game.battle, game.scene = fall_field, "battle"
    game.draw()
    fall_field.update_particles(0.60)
    assert not fall_field.fallen

    # A boss drops a bounded temporary N3 core, which then refills ammunition
    # and sets a timed ascension rather than permanently changing a card.
    boss = Enemy("bruto_demolidor", 0, BOSSES["bruto_demolidor"], "city", 5)
    city.enemies = [boss]
    city.kill_enemy(boss)
    assert city.cores == 1
    city.defenders = [recruit]
    city.use_core = True
    recruit.ammo = 0
    city.apply_core(0, 1)
    assert recruit.ascended > 0 and recruit.ammo == recruit.max_ammo and city.cores == 0

    # The first City boss has a powerful arrival but cannot stun-lock the game:
    # its repeat is confined to its own lane, lasts 1.2 seconds, and waits 18 s.
    boss_city = Battle(game, "city", selection)
    lane_troop = Defender("recruta", "Patrulheiro", 1, 1, DEFENSES["recruta"], 0)
    other_troop = Defender("recruta", "Patrulheiro", 2, 1, DEFENSES["recruta"], 0)
    fixed_barrier = Defender("barreira", "Barreira", 1, 0, DEFENSES["barreira"], 10)
    hammer_boss = Enemy("bruto_demolidor", 1, BOSSES["bruto_demolidor"], "city", 5)
    boss_city.defenders = [lane_troop, other_troop, fixed_barrier]
    boss_city.enemies = [hammer_boss]
    boss_city.boss_entrance(hammer_boss)
    assert lane_troop.stun >= 3 and other_troop.stun >= 3 and fixed_barrier.stun == 0
    assert hammer_boss.skill_timer == 18.0
    lane_troop.stun = other_troop.stun = 0
    boss_city.boss_skill(hammer_boss)
    assert lane_troop.stun >= 1.2 and other_troop.stun == 0 and hammer_boss.skill_timer == 18.0 * DIFFICULTIES["medium"]["skill_cooldown"]

    # The centered red warning happens directly before a queued boss. The
    # spawn order remains held during the announcement, then the boss enters.
    alert_city = Battle(game, "city", selection)
    alert_city.wave = 5
    alert_city.started_wave = True
    alert_city.orders = [SpawnOrder(0.0, "bruto_demolidor", 1, True)]
    alert_city.spawn_timer = 0.0
    alert_city.update_wave(0.1)
    assert alert_city.boss_alert_pending and alert_city.boss_warning == 3.0 and not alert_city.enemies
    alert_city.boss_warning = 0.0
    alert_city.update_wave(0.1)
    assert not alert_city.boss_alert_pending and len(alert_city.enemies) == 1 and alert_city.enemies[0].is_boss

    # Regression for the crash reported during live play: a legacy positional
    # effect must never turn projectile.elapsed into a string.
    legacy = Projectile(100, 320, None, 300, 320, 10, "mortar", None, 40, True, 0.2, "mortar")
    assert legacy.elapsed == 0.0 and legacy.effect == "mortar"
    city.projectiles = [legacy]
    city.update_projectiles(0.1)
    assert legacy.elapsed == 0.1

    # Difficulty starts below baseline and becomes more punishing by wave 15
    # in both durability and harm, rather than becoming easier after a few
    # rounds from excess supplies.
    early_walker = Enemy("caminhante", 0, ENEMIES["caminhante"], "city", 1)
    late_walker = Enemy("caminhante", 0, ENEMIES["caminhante"], "city", 15)
    assert early_walker.max_hp < ENEMIES["caminhante"]["hp"] < late_walker.max_hp

    # Bosses use their own gentler progression. Even the final boss remains
    # a meaningful encounter, rather than scaling as a normal horde sponge
    # that can only be solved by spending the final-containment cart.
    assert boss_wave_scale(15) < enemy_wave_scale(15)
    assert boss_damage_scale(15) < enemy_damage_scale(15)
    boss_limits = {
        "bruto_demolidor": 1175,
        "comandante_mortos": 1650,
        "cuspidor_alfa": 2500,
        "mutante_ruinas": 1300,
        "necromante": 1850,
        "colosso_mutante": 2900,
        "tide_brute": 1250,
        "cacador_abissal": 2000,
        "leviata": 3200,
    }
    for boss_key, maximum_hp in boss_limits.items():
        wave = 5 if boss_key in {"bruto_demolidor", "mutante_ruinas", "tide_brute"} else (10 if boss_key in {"comandante_mortos", "necromante", "cacador_abissal"} else 15)
        assert Enemy(boss_key, 0, BOSSES[boss_key], "city", wave).max_hp <= maximum_hp

    # Blindados, subchefes e ameaças marítimas resistentes perderam parte da
    # vida, mas os zumbis básicos permanecem com sua identidade inicial.
    assert ENEMIES["conehead"]["hp"] == 185
    assert ENEMIES["bruto"]["hp"] == 450
    assert ENEMIES["mutante"]["hp"] == 400
    assert ENEMIES["mergulhador"]["hp"] == 275

    # Enemy themes contain concrete abilities rather than display-only names.
    assert "acid" in ENEMIES["cuspidor"]["tags"]
    assert "dig" in ENEMIES["digger"]["tags"]
    assert "steal" in ENEMIES["ladrao"]["tags"]
    assert "dash" in ENEMIES["surfista"]["tags"]
    assert "leviathan" == BOSSES["leviata"]["type"]

    # Every visible screen can render after the staged cache is ready.
    game.scene = "difficulty"
    game.draw()
    game.scene = "campaign"
    game.draw()
    game.enter_selection("city")
    game.draw()
    game.scene, game.dossier_kind = "dossier_units", "units"
    game.draw()
    game.scene, game.dossier_kind = "dossier_zombies", "zombies"
    game.draw()
    game.scene = "howto"
    game.draw()
    game.battle = city
    game.scene = "battle"
    game.draw()
    game.handle_click(city.remove_rect().center)
    assert city.remove_mode
    game.handle_click(city.menu_rect().center)
    assert game.scene == "title" and game.battle is None

    # Fácil mantém N2/N3 e suprimentos, mas não oferece a ferramenta de
    # remoção: o botão some, o atalho R é ignorado e a API não devolve a tropa.
    game.difficulty = "easy"
    easy_field = Battle(game, "city", [("soldado", "Fuzileiro")])
    easy_field.defenders = [Defender("soldado", "Fuzileiro", 0, 1, DEFENSES["soldado"], 1)]
    supplies_before_easy_remove = easy_field.supplies
    easy_field.remove_defender(0, 1)
    assert len(easy_field.defenders) == 1 and easy_field.supplies == supplies_before_easy_remove
    game.battle = easy_field
    game.scene = "battle"
    game.handle_click(easy_field.remove_rect().center)
    assert not easy_field.remove_mode

    pygame.quit()
    print("OK: Beta 4 valida OpenGL, 47 recursos, quatro pistas, VFX raster, recarga própria, alinhamento, elenco regional e dificuldades.")


if __name__ == "__main__":
    main()

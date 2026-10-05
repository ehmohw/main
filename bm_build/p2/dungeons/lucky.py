"""THE GILDED ROOST: an abandoned white-and-gold henhouse-palace in flowery plains. Found only by assembling the
nine Lucky Map fragments. 50 x 34 x 86, ground at y4 (floors at y4, walkable air from y5).
  Foyer (trial spawner, lectern): P1 the slot machine (three reels in the east wall, a pull button) - three of a kind
  G1 -> Hall of Odds: P2 golden pressure-plate path; glowstone "lucky stars" in the ceiling mark the safe tiles
  G2 -> Counting House (trial spawner): P3 combat waves (the Gilded Guard)
  G3 -> Antechamber (spoils vault) -> battle door -> the Roost (arena: the Golden Goose and Lucky Jack)
Secret: Whiskers' Stash behind the foyer's west wall (a button tucked into the hay)."""
from p2.kit import DBuild
from p2.config import CODES, SEQS

WHITE = [('quartz_bricks', 4), ('smooth_quartz', 3), ('calcite', 1.5), ('diorite', 0.6)]
TRIM = 'gold_block'
FLOOR = [('smooth_quartz', 3), ('quartz_bricks', 2), ('calcite', 1)]
GY = 5
# P2 safe path on the 13 x 12 plate grid x21..33 (c 0..12), z22..33 (r 0..11)
PATH = [(6, 0), (6, 1), (5, 1), (4, 1), (3, 1), (3, 2), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (9, 4), (9, 5),
        (9, 6), (8, 6), (7, 6), (6, 6), (5, 6), (4, 6), (4, 7), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (8, 9), (8, 10), (8, 11)]
CODE = '7437'


def build():
    B = DBuild('lucky', 50, 34, 86, seed=7777)

    def room(x1, z1, x2, z2, top, floor=FLOOR):
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1):
                edge = x in (x1, x2) or z in (z1, z2)
                for y in range(0, 4): B.set(x, y, z, B.pick(WHITE))
                B.set(x, 4, z, B.pick(WHITE) if edge else B.pick(floor))
                for y in range(GY, top + 1):
                    B.set(x, y, z, (TRIM if y == top and (x + z) % 3 == 0 else B.pick(WHITE)) if edge else 'air')
                B.set(x, top + 1, z, B.pick(WHITE))
        for (cx, cz) in [(x1, z1), (x2, z1), (x1, z2), (x2, z2)]:        # gilded corner posts
            for y in range(GY, top + 3): B.set(cx, y, cz, 'quartz_pillar[axis=y]')
            B.set(cx, top + 3, cz, TRIM)

    def roof(x1, z1, x2, z2, base):
        w = (x2 - x1) // 2
        for i in range(0, w + 1):
            for x in range(x1 + i, x2 - i + 1):
                for z in (z1, z2) if i < w else range(z1, z2 + 1):
                    B.set(x, base + i, z, 'yellow_terracotta' if i % 2 else 'white_terracotta')
            for z in range(z1, z2 + 1):
                B.set(x1 + i, base + i, z, 'yellow_terracotta'); B.set(x2 - i, base + i, z, 'yellow_terracotta')

    # ================================================================ FOYER + P1 slot machine
    room(18, 6, 37, 19, 12)
    roof(18, 6, 37, 19, 14)
    for x in range(26, 29):
        B.set(x, 4, 4, 'quartz_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]')
        B.set(x, 4, 5, 'smooth_quartz')
        for y in range(GY, GY + 4): B.set(x, y, 6, 'air')
    for x in (25, 29):
        B.set(x, 4, 5, 'smooth_quartz'); B.set(x, 5, 5, 'quartz_pillar[axis=y]'); B.set(x, 6, 5, 'lantern[hanging=false,waterlogged=false]')
    B.sign(27, 10, 5, 'birch_wall_sign[facing=north,waterlogged=false]', ['THE GILDED', 'ROOST', 'all bets', 'are final'], color='gold', glow=True)
    B.entrance(27, GY, 5)
    B.trial_spawner(23, GY, 10, 'gold_zombies')
    B.lectern(32, GY, 8, 'north', 'House Rules', 'The Management', [
        "Welcome, lucky guest! The Roost belongs to the Golden Goose, who lays nothing but fortunes.",
        "Rule 1: Pull until three match.\nRule 2: Step only beneath the lucky stars.\nRule 3: Count your luck.",
        "Rule 4: Do not wake the Goose without bringing a friend.\n\nRule 5: Lucky Jack is NOT a jockey. Do not call him a jockey."])
    for i, z in enumerate((11, 13, 15), 1):          # reels in the east wall, framed
        for dz in (-1, 0, 1):
            for dy in (-1, 0, 1):
                B.set(37, 8 + dy, z + dz, 'smooth_quartz')
        B.reel(1, 37, 8, z, i)
    for z in range(10, 17): B.set(37, 10, z, TRIM); B.set(37, 6, z, TRIM)
    B.set(37, 6, 17, 'smooth_quartz')
    B.pull(1, 36, 6, 17, 'stone_button[face=wall,facing=west,powered=false]')
    B.sign(36, 7, 17, 'birch_wall_sign[facing=west,waterlogged=false]', ['PULL', 'three of a', 'kind opens', 'the door'], color='gold', glow=True)
    B.pz(1, 'slots', 37, 9, 13)
    # Whiskers' Stash (secret) west of the foyer; a button tucked into the hay
    for x in range(8, 19):
        for z in range(9, 17):
            edge = x in (8, 18) or z in (9, 16)
            for y in range(0, 4): B.set(x, y, z, B.pick(WHITE))
            B.set(x, 4, z, B.pick(WHITE) if edge else 'oak_planks')
            for y in range(GY, 9): B.set(x, y, z, B.pick(WHITE) if edge else 'air')
            B.set(x, 9, z, B.pick(WHITE))
    for (x, y, z) in [(19, 5, 17), (20, 5, 17), (19, 6, 17), (19, 5, 16), (20, 5, 18), (19, 5, 18)]:
        B.set(x, y, z, 'hay_block[axis=y]')
    B.sbutton(21, GY, 17, 'oak_button[face=wall,facing=east,powered=false]', 1)
    B.sdoor(18, GY, 12, 1)
    B.chest(10, GY, 12, 'east', loot='bm:p2/lucky/hidden')
    B.chest(10, GY, 14, 'east', loot='minecraft:chests/buried_treasure')
    B.lectern(15, GY, 10, 'south', "Whiskers' Ledger", 'Lucky Whiskers', [
        "Kept this nook for a rainy day. If you found it, you are either very lucky or very nosy. Both are good qualities.",
        "Take the horseshoe. It never did anything for me. I am a cat."])
    B.set(13, 8, 12, 'lantern[hanging=true,waterlogged=false]')
    B.fx(27, 8, 12); B.zone(27, 6, 12)

    # ================================================================ G1 -> HALL OF ODDS (P2 golden plate path)
    room(20, 19, 34, 36, 10)
    B.gate(27, GY, 19, 'x', 1)
    safe = set(PATH)
    for c in range(13):
        for r in range(12):
            x, z = 21 + c, 22 + r
            B.plate(x, GY, z, (c, r) not in safe, plate='minecraft:light_weighted_pressure_plate', safe_under='minecraft:white_concrete')
            B.set(x, 10, z, 'glowstone' if (c, r) in safe else B.pick([('smooth_quartz', 1)]))
    B.start(2, 27, GY, 21)
    B.goal(2, 29, GY, 34)
    B.sign(24, 7, 20, 'birch_wall_sign[facing=south,waterlogged=false]', ['Step only', 'beneath the', 'lucky stars.', ''], color='gold', glow=True)
    B.pz(2, 'path', 27, 2, 28)
    for z in range(22, 34, 3):                        # gilded window slits
        for x in (20, 34): B.set(x, 7, z, 'yellow_stained_glass_pane')
    B.fx(27, 8, 28); B.zone(27, 6, 28)

    # ================================================================ G2 -> COUNTING HOUSE (P3 keypad 7437), domed tower
    room(18, 36, 37, 48, 14)
    B.gate(27, GY, 36, 'x', 2)
    B.pz(3, 'waves', 27, GY, 42)
    B.el(3, 'wsp', 21, GY, 39)
    B.el(3, 'wsp', 34, GY, 39)
    B.el(3, 'wsp', 21, GY, 46)
    B.el(3, 'wsp', 34, GY, 46)
    B.sign(27, 9, 47, 'birch_wall_sign[facing=north,waterlogged=false]', ['The Gilded', 'Guard does not', 'share.', ''], color='gold', glow=True)
    B.trial_spawner(33, GY, 41, 'gold_husks')
    for (x, z) in [(22, 42), (32, 45)]:
        B.set(x, GY, z, 'gold_block'); B.set(x, GY + 1, z, 'decorated_pot[cracked=true,facing=north,waterlogged=false]')
    # gilded dome over the counting house
    for y in range(16, 26):
        r = max(0.5, 9.5 * (1 - ((y - 15) / 10.5) ** 2) ** 0.5)
        for x in range(18, 38):
            for z in range(36, 49):
                d = ((x - 27.5) ** 2 + (z - 42) ** 2) ** 0.5
                if r - 1.2 <= d <= r: B.set(x, y, z, 'gold_block' if y % 3 == 0 else 'yellow_terracotta')
    B.set(27, 26, 42, 'gold_block'); B.set(27, 27, 42, 'end_rod[facing=up]'); B.set(28, 27, 42, 'gold_block')
    B.fx(27, 9, 42); B.zone(27, 6, 42)

    # ================================================================ G3 -> ANTECHAMBER -> THE ROOST (arena)
    room(20, 48, 34, 54, 10)
    B.gate(31, GY, 48, 'x', 3)
    B.vault(21, GY, 51, 'east', 'vkey_lucky', 'bm:p2/lucky/vault')
    B.sign(24, 8, 49, 'birch_wall_sign[facing=south,waterlogged=false]', ['THE ROOST', 'Kneel at the', 'golden altar.', 'Bring friends.'], color='gold', glow=True)
    B.zone(27, 6, 51)
    room(13, 54, 41, 82, 17, floor=[('smooth_quartz', 1)])
    for x in range(14, 41):
        for z in range(55, 82):
            if (x + z) % 2 == 0: B.set(x, 4, z, 'quartz_bricks')
            if abs(((x - 27) ** 2 + (z - 68) ** 2) ** 0.5 - 6) < 0.5: B.set(x, 4, z, 'gold_block')
    roof(13, 54, 41, 82, 19)
    B.gate(27, GY, 54, 'x', 0, big=True)
    for (x, z) in [(19, 60), (35, 60), (19, 76), (35, 76)]:
        for y in range(GY, 17): B.set(x, y, z, 'quartz_pillar[axis=y]')
        B.set(x, 16, z, TRIM)
    for z in range(58, 80, 5):
        for x in (14, 40): B.set(x, GY, z, 'hay_block[axis=y]')
    B.arena(27, GY, 68)
    B.altar(27, GY, 57)
    B.set(27, 4, 57, 'gold_block')
    for x in (25, 29): B.set(x, GY, 57, 'gold_block'); B.set(x, GY + 1, 57, 'lantern[hanging=false,waterlogged=false]')
    for (x, z) in [(20, 64), (34, 64), (20, 74), (34, 74)]: B.mspawn(x, GY, z)
    B.vault(14, GY, 68, 'east', 'bkey_lucky', 'bm:p2/lucky/victor')
    B.xdoor(27, GY, 82)
    for x in range(26, 29): B.set(x, 4, 83, 'quartz_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]')
    for (x, z) in [(22, 62), (32, 62), (22, 74), (32, 74), (27, 79)]:
        B.set(x, 17, z, 'lantern[hanging=true,waterlogged=false]')
    B.fx(27, 10, 68); B.zone(27, 6, 68)
    B.controller(27, 10, 44)
    return B

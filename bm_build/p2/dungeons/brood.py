"""THE BROODMOTHER'S NEST: buried under forests, 64 x 26 x 64, one solid block of rock with carved caverns.
Flow: shaft -> Entrance cave -> ramp -> Hatchery (trial spawners) -> P1 Silk Loom (levers) -> G1 -> P2 Egg Chamber
(ordered egg sacs) -> G2 -> P3 Web Walk (pressure-plate path) -> G3 -> Antechamber (altar, spoils vault) -> battle door
-> Arena. Secrets: Weaver's Cache (off P1), Rat Gang hideout (off the entrance). Arena exit tunnel -> Hatchery."""
from p2.kit import DBuild, cave, tunnel, decorate_cave, lichen
from p2.config import CODES, SEQS

ROCK = [('deepslate', 6), ('tuff', 2), ('cobbled_deepslate', 1)]
FLOOR = [('packed_mud', 3), ('coarse_dirt', 2), ('mud_bricks', 1)]
WALL_BUILT = [('deepslate_bricks', 4), ('cracked_deepslate_bricks', 2), ('tuff_bricks', 1)]

# P3 safe path: (col, row) on the 11 x 10 plate grid x49..59, z52..61
PATH = [(5, 0), (5, 1), (6, 1), (7, 1), (7, 2), (7, 3), (8, 3), (9, 3), (9, 4), (9, 5), (8, 5), (7, 5), (6, 5), (5, 5), (4, 5),
        (4, 6), (4, 7), (3, 7), (2, 7), (2, 8), (2, 9), (1, 9), (0, 9)]


def build():
    B = DBuild('brood', 64, 26, 64, seed=4417)
    B.fillp(0, 0, 0, 63, 25, 63, ROCK)

    # ---------------- entrance shaft + entrance cave (floor y14)
    for y in range(15, 26):
        for x in range(2, 5):
            for z in range(3, 6):
                B.set(x, y, z, 'air')
    for y in range(15, 25):
        B.set(3, y, 3, 'ladder[facing=south,waterlogged=false]')
    cave(B, 2, 2, 13, 13, 14, 6, FLOOR)
    for x in range(2, 5):
        for z in range(3, 6): B.set(x, 14, z, B.pick(FLOOR))
    B.entrance(6, 15, 8)
    B.mb(3, 25, 4, ['bm.eshaft'])               # 2.13: the shaft is carried on up to the surface at runtime
    B.lectern(10, 15, 4, 'south', "Nest Warden's Warning", 'Unknown', [
        "Turn back.\n\nThe nest below belongs to the Broodmother. She does not hunt you. She does not need to. Her children do it for her.",
        "Three trials guard her den. Silk, egg, and web. The old weavers left their marks for anyone patient enough to read them.",
        "Patient. Not clever. Clever people try to rush the web walk. We buried the clever people in the Hatchery.",
        "If you wake her, kill her fast. And do not let her children reach the eggs."])
    B.set(5, 15, 10, 'deepslate_bricks')
    B.sign(5, 15, 11, 'dark_oak_wall_sign[facing=south,waterlogged=false]', ['Leave the', 'light behind.', '', '- the Weavers'], color='white', glow=True)
    tunnel(B, 8, 9, 8, 14, 14, FLOOR)
    # ramp down to the Hatchery: z14 (y13) .. z26 (y2), x7..9
    for i, z in enumerate(range(14, 27)):
        yf = max(2, 13 - i)
        for x in range(7, 10):
            B.set(x, yf, z, 'cobbled_deepslate_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]' if yf > 2 else B.pick(FLOOR))
            for y in range(yf + 1, yf + 5): B.set(x, y, z, 'air')

    # ---------------- Hatchery (combat): x2..22, z27..43
    cave(B, 2, 27, 22, 43, 2, 9, FLOOR)
    tunnel(B, 8, 25, 8, 30, 2, FLOOR)
    B.trial_spawner(7, 3, 35, 'spiders')
    B.trial_spawner(17, 3, 33, 'cave_spiders')
    for (x, z) in [(5, 31), (19, 39), (11, 41), (4, 39)]:
        B.set(x, 3, z, 'bone_block[axis=y]'); B.set(x, 4, z, 'skeleton_skull[rotation=%d]' % B.rnd.randrange(16))
    decorate_cave(B, 2, 27, 22, 43, 3, 12, web=0.07, lich=0.015, deco=[('cobweb', 0.03)])
    B.fx(12, 6, 35); B.zone(12, 4, 35)
    # exit tunnel from the arena arrives here (x12, z40..45)
    for z in range(40, 46):
        B.set(12, 2, z, B.pick(FLOOR)); B.set(12, 3, z, 'air'); B.set(12, 4, z, 'air')

    # ---------------- P1 Silk Loom (levers): x26..40, z28..42
    tunnel(B, 22, 35, 27, 35, 2, FLOOR)
    cave(B, 26, 28, 40, 42, 2, 8, FLOOR)
    # loom wall: flat built wall at z29 with 5 silk columns; white = pull, gray = leave
    WANT = [1, 0, 1, 1, 0]
    for x in range(28, 39):
        for y in range(3, 9): B.set(x, y, 29, B.pick(WALL_BUILT))
        for y in range(3, 9): B.set(x, y, 30, 'air')
    for i, x in enumerate(range(29, 39, 2)):
        for y in range(5, 9): B.set(x, y, 29, 'white_wool' if WANT[i] else 'gray_wool')
        B.lever(1, x, 3, 30, 'south', WANT[i])
        B.set(x, 4, 30, 'cobweb' if B.rnd.random() < 0.3 else 'air')
    B.sign(33, 4, 30, 'dark_oak_wall_sign[facing=south,waterlogged=false]', ['The loom', 'remembers which', 'strands were', 'pulled.'], color='white', glow=True)
    B.pz(1, 'levers', 33, 1, 32)
    # hidden button: under a bone ledge in a west alcove (face=ceiling)
    for z in range(29, 32):
        for x in (26, 27):
            B.set(x, 3, z, 'air'); B.set(x, 4, z, 'bone_block[axis=y]'); B.set(x, 2, z, B.pick(FLOOR))
    B.sbutton(26, 3, 30, 'stone_button[face=ceiling,facing=north,powered=false]', 1)
    decorate_cave(B, 26, 28, 40, 42, 3, 10, web=0.06, lich=0.02)
    # secret door in the south wall (z43, x33) -> Weaver's Cache x30..38, z45..50
    for z in (40, 41, 42):
        B.set(33, 2, z, B.pick(FLOOR)); B.set(33, 3, z, 'air'); B.set(33, 4, z, 'air')
    B.sdoor(33, 3, 43, 1)
    B.set(33, 2, 44, B.pick(FLOOR)); B.set(33, 3, 44, 'air'); B.set(33, 4, 44, 'air')
    B.shell(30, 2, 45, 38, 7, 50, ROCK, FLOOR, ROCK)
    B.set(33, 3, 45, 'air'); B.set(33, 4, 45, 'air')
    B.chest(31, 3, 49, 'north', loot='bm:p2/brood/hidden')
    B.chest(37, 3, 49, 'north', loot='minecraft:chests/simple_dungeon')
    B.set(34, 3, 49, 'skeleton_skull[rotation=0]'); B.set(32, 3, 49, 'bone_block[axis=y]')
    B.sign(35, 4, 49, 'dark_oak_wall_sign[facing=north,waterlogged=false]', ["Weaver's", 'Cache', '', 'Take. Then run.'], color='white', glow=True)
    for x, z in [(31, 46), (37, 47), (34, 48)]: lichen(B, x, 6, z)
    B.fx(33, 6, 35); B.zone(33, 4, 35)

    # ---------------- G1 -> P2 Egg Chamber: x46..61, z28..44
    tunnel(B, 39, 35, 47, 35, 2, FLOOR)
    B.gate(43, 3, 35, 'z', 1)
    cave(B, 46, 28, 61, 44, 2, 9, FLOOR)
    # egg sacs (mushroom stem) of size 1,2,4,8 with a button each; order = smallest -> largest
    sacs = [  # (blocks, button pos, button facing)
        ([(58, 3, 31)], (57, 3, 31), 'west'),
        ([(49, 3, 41), (49, 4, 41)], (50, 4, 41), 'east'),
        ([(58, 3, 40), (59, 3, 40), (58, 3, 41), (59, 3, 41)], (57, 3, 40), 'west'),
        ([(48, y, z) for y in (3, 4) for z in (30, 31)] + [(49, y, z) for y in (3, 4) for z in (30, 31)], (50, 3, 30), 'east'),
    ]
    for order, (blocks, (bx, by, bz), f) in enumerate(sacs, 1):
        for (x, y, z) in blocks: B.set(x, y, z, 'mushroom_stem[down=true,east=true,north=true,south=true,up=true,west=true]')
        B.set(bx, by, bz, 'air')
        B.seq_button(2, bx, by, bz, f'pale_oak_button[face=wall,facing={f},powered=false]', order, sound=order)
    B.pz(2, 'seq', 53, 1, 36)
    SEQS.setdefault('brood', {})[2] = 4
    B.set(50, 3, 36, 'deepslate_bricks'); B.set(50, 4, 36, 'deepslate_bricks')
    B.sign(51, 4, 36, 'dark_oak_wall_sign[facing=east,waterlogged=false]', ['Wake the brood', 'gently: from the', 'least of them to', 'the greatest.'], color='white', glow=True)
    decorate_cave(B, 46, 28, 61, 44, 3, 11, web=0.08, lich=0.02, deco=[('cobweb', 0.02)])
    B.fx(53, 6, 36); B.zone(53, 4, 36)

    # ---------------- G2 -> P3 Web Walk: plates x49..59, z52..61; start row z51
    tunnel(B, 54, 43, 54, 51, 2, FLOOR)
    B.gate(54, 3, 47, 'x', 2)
    B.fillp(48, 2, 50, 60, 9, 62, ROCK)
    for x in range(49, 60):
        for z in range(51, 62):
            for y in range(3, 9): B.set(x, y, z, 'air')
    for x in range(49, 60): B.set(x, 2, 51, 'mud_bricks')
    for x in range(53, 56): B.set(x, 2, 50, 'mud_bricks'); B.set(x, 3, 50, 'air'); B.set(x, 4, 50, 'air'); B.set(x, 5, 50, 'air'); B.set(x, 6, 50, 'air')
    safe = set(PATH)
    for c in range(11):
        for r in range(10):
            x, z = 49 + c, 52 + r
            B.set(x, 2, z, 'polished_tuff')
            B.plate(x, 3, z, trap=(c, r) not in safe)
            if (c, r) in safe: B.set(x, 8, z, 'cobweb')        # the clue: follow the silk above
    B.pz(3, 'path', 54, 1, 56)
    B.start(3, 54, 3, 51)
    tunnel(B, 42, 61, 48, 61, 2, FLOOR)
    B.goal(3, 47, 3, 61)
    B.gate(45, 3, 61, 'z', 3)
    B.sign(56, 4, 51, 'dark_oak_wall_sign[facing=south,waterlogged=false]', ['Only the strands', 'that hold above', 'will hold below.', ''], color='white', glow=True)
    B.fx(54, 6, 56)

    # ---------------- Antechamber: x30..44, z52..62 (built hall)
    B.shell(30, 2, 52, 44, 9, 62, WALL_BUILT, [('polished_deepslate', 3), ('deepslate_tiles', 2)], ROCK)
    for z in range(60, 63):
        B.set(44, 3, z, 'air'); B.set(44, 4, z, 'air'); B.set(44, 5, z, 'air'); B.set(44, 6, z, 'air')
    B.set(44, 2, 60, 'polished_deepslate'); B.set(44, 2, 61, 'polished_deepslate'); B.set(44, 2, 62, 'polished_deepslate')
    for (x, z) in [(35, 55), (39, 55), (35, 59), (39, 59)]:
        B.set(x, 3, z, 'red_candle[candles=3,lit=true,waterlogged=false]')
    B.vault(42, 3, 53, 'south', 'vkey_brood', 'bm:p2/brood/vault')
    B.sign(37, 5, 53, 'dark_oak_wall_sign[facing=south,waterlogged=false]', ['Enter her den.', 'Kneel at the bone', 'altar with her', 'key in hand.'], color='white', glow=True)
    B.fx(37, 6, 57); B.zone(37, 4, 57)
    decorate_cave(B, 31, 53, 43, 61, 3, 8, web=0.05, lich=0.03)

    # ---------------- battle door -> Arena: x3..26, z45..62
    tunnel(B, 25, 57, 31, 57, 2, [('polished_deepslate', 1)], w=5, h=5)
    B.gate(28, 3, 57, 'z', 0, big=True)
    cave(B, 3, 45, 26, 62, 2, 13, FLOOR, rough=0.08)
    B.arena(15, 3, 54)
    # bone altar just inside the battle door (summoners are inside when the doors seal)
    B.set(23, 2, 57, 'chiseled_deepslate'); B.set(23, 3, 56, 'bone_block[axis=y]'); B.set(23, 4, 56, 'skeleton_skull[rotation=4]')
    B.set(23, 3, 58, 'bone_block[axis=y]'); B.set(23, 4, 58, 'skeleton_skull[rotation=4]')
    B.altar(23, 3, 57)
    for (x, z) in [(8, 50), (22, 50), (8, 59), (21, 59)]: B.mspawn(x, 3, z)
    for (x, z) in [(6, 48), (24, 56), (10, 61), (19, 46)]:
        B.pillar(x, z, 3, 14, [('bone_block[axis=y]', 3), ('cobbled_deepslate', 1)])
    # victor's vault in a niche on the west side
    for y in (3, 4): B.set(3, y, 54, 'air'); B.set(4, y, 54, 'air')
    B.set(3, 2, 54, 'polished_deepslate'); B.set(4, 2, 54, 'polished_deepslate')
    B.vault(3, 3, 54, 'east', 'bkey_brood', 'bm:p2/brood/victor')
    decorate_cave(B, 3, 45, 26, 62, 3, 16, web=0.1, lich=0.02)
    for x in range(10, 21):        # keep the arena floor clear for the fight
        for z in range(49, 60):
            for y in range(3, 6):
                if B.get(x, y, z) == 'minecraft:cobweb': B.set(x, y, z, 'air')
    B.xdoor(12, 3, 44)
    B.fx(15, 7, 54); B.zone(15, 4, 54)

    # ---------------- Rat Gang hideout (secret, off the entrance cave): x17..25, z3..11
    for x in (3, 4):                          # a dark nook in the corner of the entrance cave
        for z in (11, 12):
            B.set(x, 14, z, B.pick(FLOOR)); B.set(x, 15, z, 'air'); B.set(x, 16, z, 'air')
    B.set(2, 15, 12, 'cobbled_deepslate')
    B.sbutton(3, 15, 12, 'stone_button[face=wall,facing=east,powered=false]', 2)
    for x in range(13, 17):
        B.set(x, 14, 7, B.pick(FLOOR)); B.set(x, 15, 7, 'air'); B.set(x, 16, 7, 'air')
    B.sdoor(14, 15, 7, 2)
    B.shell(17, 14, 3, 25, 19, 11, ROCK, [('spruce_planks', 1)], ROCK)
    B.set(17, 15, 7, 'air'); B.set(17, 16, 7, 'air')
    B.chest(23, 15, 5, 'west', loot='bm:p2/brood/rats')
    B.set(23, 15, 9, 'cake[bites=3]'); B.set(22, 15, 9, 'barrel[facing=up,open=false]')
    B.sign(24, 16, 7, 'spruce_wall_sign[facing=west,waterlogged=false]', ['RAT GANG', 'WUZ HERE', 'we took the', 'good cheese'], color='yellow', glow=True)
    B.m(20.5, 15, 8.5, ['bm.npc_spawn', 'bm.npc.deco_rat'], 0)
    B.set(19, 18, 7, 'lantern[hanging=true,waterlogged=false]')
    decorate_cave(B, 2, 2, 13, 13, 15, 20, web=0.06, lich=0.03)
    B.fx(7, 17, 7)

    B.controller(32, 8, 32)
    return B

"""WILFREY'S REST (2.5 - somber): a weathered islet drifting apart from the Hollow Throne. Dull tuff and old deepslate,
dead trees hung with pale moss, leaning standing stones with guttering candles, soul lanterns, a still black pool and
the plain stone tomb of a kind lord - quiet, creepy, respectful. Placed once by command beside the citadel
(data.GRAVE_OFFSET from HOLLOW_ORIGIN; re-placed over the 2.4 version). Only an elytra reaches it.
41 x 40 x 41, top surface y24 (walk 25). The tomb's interaction box gives Wilfrey's Locket to the Hollow King's
conqueror; a wayshrine pad (south-west) returns you to the arrival rock."""
import math
import random
from nbt import Int, F
from structures import Build

SX, SY, SZ = 41, 40, 41
TOP = 24
CX, CZ = 20, 20


def build():
    B = Build(SX, SY, SZ)
    rnd = random.Random(1311)
    S = B.set
    pick = lambda pal: rnd.choices([p for p, _ in pal], [w for _, w in pal])[0]
    SOIL = [('podzol', 3), ('coarse_dirt', 3), ('pale_moss_block', 2), ('rooted_dirt', 2), ('moss_block', 1)]
    UNDER = [('deepslate', 4), ('tuff', 4), ('cobbled_deepslate', 2), ('smooth_basalt', 1)]
    STONE = [('tuff_bricks', 4), ('cracked_stone_bricks', 1), ('mossy_cobblestone', 2), ('chiseled_tuff', 1)]

    # ---------------- the rock: dull crown, dark ragged underside with hanging moss and roots
    for x in range(SX):
        for z in range(SZ):
            d = math.hypot(x - CX, z - CZ) + rnd.uniform(-0.9, 0.9)
            if d > 15.5: continue
            depth = int((15.5 - d) ** 1.25 * 1.2) + 2 + rnd.randrange(2)
            for y in range(max(0, TOP - depth), TOP + 1):
                k = TOP - y
                S(x, y, z, pick(SOIL) if k == 0 else 'rooted_dirt' if k <= 2 else pick(UNDER))
            b = TOP - depth - 1
            if 6 < d < 14 and rnd.random() < 0.12 and b >= 3:
                for k in range(1 + rnd.randrange(4)): S(x, b - k, z, 'pale_hanging_moss[tip=false]' if rnd.random() < 0.6 else 'hanging_roots[waterlogged=false]')
    # ---------------- sparse, faded ground cover
    for x in range(SX):
        for z in range(SZ):
            if B.get(x, TOP, z) and math.hypot(x - CX, z - CZ) < 14 and rnd.random() < 0.22:
                r = rnd.random()
                S(x, TOP + 1, z, 'leaf_litter[facing=north,segment_amount=%d]' % rnd.randint(1, 4) if r < 0.35 else
                  'pale_moss_carpet[bottom=true,east=none,north=none,south=none,west=none]' if r < 0.6 else
                  'dead_bush' if r < 0.8 else 'short_grass' if r < 0.93 else 'lily_of_the_valley')
    # ---------------- the old path from the landing arch (south) to the tomb
    for z in range(23, 37):
        for x in range(19, 22):
            if rnd.random() < 0.85: S(x, TOP, z, pick(STONE)); S(x, TOP + 1, z, 'air')
    for x in (17, 23):                                                  # a weathered arch, one lantern hung from it
        for y in range(TOP + 1, TOP + 6): S(x, y, 34, 'tuff_bricks' if y < TOP + 5 else 'chiseled_tuff_bricks')
    for x in range(17, 24): S(x, TOP + 6, 34, 'tuff_brick_slab[type=bottom,waterlogged=false]' if x in (17, 23) else 'tuff_bricks')
    S(20, TOP + 5, 34, 'soul_lantern[hanging=true,waterlogged=false]')
    S(22, TOP + 6, 34, 'cobweb')
    # ---------------- eight standing stones, leaning and broken, guttering candles
    for k in range(8):
        a = k * math.pi / 4 + math.pi / 8
        x, z = round(CX + 10 * math.cos(a)), round(CZ + 10 * math.sin(a))
        h = [4, 2, 3, 1, 4, 3, 2, 3][k]
        S(x, TOP, z, 'polished_tuff')
        for y in range(TOP + 1, TOP + 1 + h): S(x, y, z, 'tuff_bricks' if y % 2 else 'chiseled_tuff')
        if k == 3:                                                       # one has fallen over
            for j in (1, 2): S(x + (1 if x < CX else -1) * j, TOP + 1, z, 'tuff_brick_wall')
        if h >= 3: S(x, TOP + 1 + h, z, 'gray_candle[candles=%d,lit=true,waterlogged=false]' % (1 + k % 3))
        if k in (1, 6): S(x, TOP + h, z + (1 if z < CZ else -1), 'cobweb')
    # ---------------- the tomb: low deepslate dais, plain tuff sarcophagus, mossy headstone, his sword, two banners
    for x in range(15, 26):
        for z in range(14, 23):
            inner = 16 <= x <= 24 and 15 <= z <= 21
            S(x, TOP + 1, z, ('deepslate_tiles' if (x in (16, 24) or z in (15, 21)) else 'polished_deepslate') if inner else 'air')
            if not inner: S(x, TOP, z, pick(STONE))
    for x in range(16, 25): S(x, TOP + 1, 22, 'polished_deepslate_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]')
    for x in range(18, 23):
        for z in range(16, 20):
            S(x, TOP + 2, z, 'chiseled_tuff_bricks' if x in (18, 22) or z in (16, 19) else 'tuff_bricks')
            S(x, TOP + 3, z, 'tuff_brick_slab[type=bottom,waterlogged=false]')
    S(20, TOP + 3, 17, 'polished_tuff_slab[type=bottom,waterlogged=false]'); S(20, TOP + 3, 18, 'polished_tuff_slab[type=bottom,waterlogged=false]')
    for y in range(TOP + 2, TOP + 6): S(20, y, 15, 'chiseled_tuff' if y == TOP + 5 else 'tuff_bricks')
    for x in (19, 21): S(x, TOP + 2, 15, 'tuff_bricks'); S(x, TOP + 3, 15, 'tuff_brick_stairs[facing=%s,half=bottom,shape=straight,waterlogged=false]' % ('east' if x == 19 else 'west'))
    S(20, TOP + 6, 15, 'pale_moss_carpet[bottom=true,east=none,north=none,south=none,west=none]')
    for x in (19, 21): S(x, TOP + 4, 15, 'pale_hanging_moss[tip=true]')
    B.sign(20, TOP + 3, 16, 'dark_oak_wall_sign[facing=south,waterlogged=false]', ['HERE LIES', 'WILFREY', 'the Kind Lord', 'Rest well.'], color='light_gray', glow=False)
    for (x, z) in ((19, 21), (21, 21)): S(x, TOP + 2, z, 'white_candle[candles=1,lit=true,waterlogged=false]')
    S(16, TOP + 2, 15, 'white_banner[rotation=8]')                       # his colours, and mourning grey
    S(24, TOP + 2, 15, 'gray_banner[rotation=8]')
    for x in (16, 24):
        S(x, TOP + 2, 21, 'polished_deepslate_wall'); S(x, TOP + 3, 21, 'soul_lantern[hanging=false,waterlogged=false]')
    sword = {'id': 'minecraft:item_display', 'item': {'id': 'minecraft:netherite_sword', 'count': Int(1)}, 'item_display': 'fixed',
             'brightness': {'block': Int(7), 'sky': Int(3)},
             'transformation': {'left_rotation': [F(0), F(0), F(0.9239), F(0.3827)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                'translation': [F(0), F(0.35), F(0)], 'scale': [F(1.3), F(1.3), F(1.3)]}}
    B.ents.append({'pos': [20.5, TOP + 2.0, 20.5], 'blockPos': [20, TOP + 2, 20], 'nbt': sword})

    # ---------------- two dead trees: a crooked dark oak (NE), a weeping pale oak (NW)
    def branch(x, y, z, dx, dz, n, log, axis):
        for i in range(1, n + 1):
            S(x + dx * i, y + (i // 2), z + dz * i, f'{log}[axis={axis}]')
        return x + dx * n, y + n // 2, z + dz * n
    tx, tz = 28, 11
    for y in range(TOP + 1, TOP + 8):
        if y == TOP + 4: tx += 1
        S(tx, y, tz, 'stripped_dark_oak_log[axis=y]')
    for (dx, dz, n, yy) in ((1, 0, 3, TOP + 6), (-1, 0, 2, TOP + 5), (0, -1, 3, TOP + 7), (0, 1, 2, TOP + 4)):
        ex, ey, ez = branch(tx, yy, tz, dx, dz, n, 'stripped_dark_oak_log', 'x' if dx else 'z')
        S(ex, ey + 1, ez, 'dark_oak_fence')
        if rnd.random() < 0.5: S(ex, ey - 1, ez, 'cobweb')
    for y in range(TOP + 1, TOP + 8): S(11, y, 12, 'pale_oak_log[axis=y]')
    for (dx, dz, n) in ((1, 0, 3), (-1, 0, 3), (0, 1, 2), (0, -1, 3)):
        ex, ey, ez = branch(11, TOP + 6, 12, dx, dz, n, 'pale_oak_log', 'x' if dx else 'z')
        for k in range(1, 3 + rnd.randrange(3)):
            if B.get(ex, ey - k, ez) is None: S(ex, ey - k, ez, 'pale_hanging_moss[tip=%s]' % ('true' if k > 2 else 'false'))
        S(ex, ey + 1, ez, 'pale_oak_leaves[distance=1,persistent=true,waterlogged=false]')
    if B.get(12, TOP + 6, 12): S(12, TOP + 5, 12, 'soul_lantern[hanging=true,waterlogged=false]')
    # ---------------- the still black pool (SE): mud rim, dark water, roots
    for x in range(26, 31):
        for z in range(25, 30):
            rim = x in (26, 30) or z in (25, 29)
            S(x, TOP, z, 'mud' if rim else 'water[level=0]')
            S(x, TOP + 1, z, 'air')
            if not rim: S(x, TOP - 1, z, 'mud')
    for (x, z) in ((25, 27), (31, 26), (28, 31), (24, 24), (32, 29)): S(x, TOP + 1, z, 'firefly_bush')
    # ---------------- wayshrine home (south-west) + markers
    S(12, TOP, 30, 'crying_obsidian'); S(12, TOP + 1, 30, 'air')
    S(13, TOP + 1, 30, 'soul_lantern[hanging=false,waterlogged=false]')
    B.marker(12.5, TOP + 1, 30.5, ['bm.isle_ret'], 0)
    B.marker(20.5, TOP + 2.0, 17.8, ['bm.npc_spawn', 'bm.npc.wil_grave'], 0)      # the click box covers the sarcophagus itself
    B.marker(20.5, TOP + 4, 20.5, ['bm.wgfx'], 0)
    return B

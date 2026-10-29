"""(3.0 draft) THE LOOM SANCTUARY - where the Keeper of Bonds waits (keeper_art): a small floating island high in the Overworld
sky, found with the Compass of Bonds once you have all 49 other followers.

A grassy crown about 25 across: a ring of eight white-and-gold arches (quartz pillars, chiselled capitals, a gold keystone, a
lantern hung under each), and between the arches the THREADS - two strands of coloured glass-pane thread strung from each arch
to the next, sagging a little, going round the colour wheel. In the middle a raised dais (two steps of smooth quartz, gold at its
heart) and on its north side the GREAT LOOM: birch uprights and beam, a half-woven tapestry of rainbow wool, its warp of fences
above, a loom and a little bench beside it. Four flowering trees (cherry and flowering azalea), petals and wildflowers in the
grass, a calcite path from the landing circle (south) to the dais. Under it, the rock tapers to a hanging point of dripstone;
lanterns hang from it on chains, and a few lights glow in the rock.

    B = keeper_sanctuary.build()                  # a structures.Build (B.b: {(x, y, z): 'minecraft:state'}, B.size)
    B.export(G.path('data', 'bm', 'structure', 'p250_loom.nbt'))     # as phase70 / phase203 save theirs

Coordinates are the template's own (x east, z south, y up; place it with its origin wherever the sky allows). SPAWN, DAIS and
ARRIVAL are block-centre points (floats) in them; BBOX is the template's box. build(markers=True) also puts markers at those
points (tags bm.kb_spawn, bm.kb_dais, bm.kb_arrive), in the way grave.py marks its own."""
import math
import random
from structures import Build

SX, SY, SZ = 27, 31, 27
CX, CZ = 13, 13
TOP = 19                                    # the grass's own y (stand on TOP + 1)
R = 12.3                                    # the crown's radius
SIZE = (SX, SY, SZ)
BBOX = ((0, 0, 0), (SX - 1, SY - 1, SZ - 1))
DAIS = (CX + 0.5, TOP + 3.0, CZ + 0.5)      # the top of the dais (its upper step stands at TOP + 2)
SPAWN = (CX + 0.5, TOP + 3.0, CZ + 0.5, 0.0)   # the Keeper: on the dais before its loom, facing south (yaw 0) toward the landing
ARRIVAL = (CX + 0.5, TOP + 1.0, CZ + 10.5)  # the landing circle, at the south edge, facing the dais
ARCHES = 8
# the threads' colours, round the wheel: two strands to each gap between arches
THREADS = [('red', 'orange'), ('orange', 'yellow'), ('yellow', 'lime'), ('lime', 'cyan'), ('cyan', 'light_blue'), ('light_blue', 'blue'),
           ('purple', 'magenta'), ('magenta', 'pink')]
TAPESTRY = ['red', 'orange', 'yellow', 'lime', 'light_blue', 'purple']


def _line4(a, b):
    """the cells of a 4-connected line from a to b (x, z) - a pane line that joins up"""
    (x0, z0), (x1, z1) = a, b
    out = [(x0, z0)]
    x, z = x0, z0
    while (x, z) != (x1, z1):
        dx, dz = x1 - x, z1 - z
        # step along whichever axis keeps nearest the true line
        tx, tz = (x + (1 if dx > 0 else -1), z), (x, z + (1 if dz > 0 else -1))
        def err(p):
            num = abs((z1 - z0) * (p[0] - x0) - (x1 - x0) * (p[1] - z0))
            return num
        if dx == 0: x, z = tz
        elif dz == 0: x, z = tx
        else: x, z = min((tx, tz), key=err)
        out.append((x, z))
    return out


def build(markers=False):
    B = Build(SX, SY, SZ)
    rnd = random.Random(5000)
    S = B.set
    pick = lambda pal: rnd.choices([p for p, _ in pal], [w for _, w in pal])[0]
    ROCK = [('calcite', 4), ('stone', 3), ('tuff', 2), ('dripstone_block', 2), ('smooth_basalt', 1)]
    wob = [rnd.uniform(-0.6, 0.6) for _ in range(12)]

    def edge(x, z):
        """the crown's radius toward (x, z): round, a little uneven"""
        a = math.atan2(z - CZ, x - CX)
        k = (a / (2 * math.pi) * 12) % 12
        i = int(k); t = k - i
        return R + wob[i] * (1 - t) + wob[(i + 1) % 12] * t

    # ---------------- the island: the grass crown, earth under it, the rock tapering to a hanging point
    bottom = {}
    for x in range(SX):
        for z in range(SZ):
            d = math.hypot(x - CX, z - CZ); e = edge(x, z)
            if d > e: continue
            f = 1 - d / e
            depth = 2 + int(17.5 * f ** 1.45 + rnd.uniform(0, 1.2))
            y0 = max(1, TOP - depth)
            for y in range(y0, TOP + 1):
                k = TOP - y
                S(x, y, z, 'grass_block[snowy=false]' if k == 0 else 'dirt' if k <= 2 else pick(ROCK))
            bottom[(x, z)] = y0
    # the hanging point: a dripstone spike under the middle
    yb = bottom[(CX, CZ)]
    for k, st in enumerate(['dripstone_block', 'dripstone_block', 'pointed_dripstone[thickness=base,vertical_direction=down,waterlogged=false]',
                            'pointed_dripstone[thickness=middle,vertical_direction=down,waterlogged=false]',
                            'pointed_dripstone[thickness=frustum,vertical_direction=down,waterlogged=false]',
                            'pointed_dripstone[thickness=tip,vertical_direction=down,waterlogged=false]']):
        if yb - 1 - k >= 0: S(CX, yb - 1 - k, CZ, st)
    # lights in the rock, and lanterns hung from it on chains
    for (x, z), y0 in bottom.items():
        d = math.hypot(x - CX, z - CZ)
        if 3 < d < 10 and rnd.random() < 0.05 and y0 > 2: S(x, y0, z, 'shroomlight' if rnd.random() < 0.5 else 'glowstone')
    for k in range(9):
        a = 2 * math.pi * k / 9 + 0.3
        r = 4.5 + 3.5 * (k % 3) / 2
        x, z = round(CX + r * math.cos(a)), round(CZ + r * math.sin(a))
        if (x, z) not in bottom: continue
        y = bottom[(x, z)] - 1
        n = 1 + (k * 5) % 3
        for j in range(n):
            if y - j >= 1: S(x, y - j, z, 'iron_chain[axis=y,waterlogged=false]')
        if y - n >= 0: S(x, y - n, z, 'lantern[hanging=true,waterlogged=false]')

    G = TOP + 1                                         # (the first block above the grass)
    used = set()                                        # (cells of the crown kept clear of flowers)

    # ---------------- the path from the landing circle to the dais, and the landing circle (gold-ringed calcite)
    for z in range(CZ + 3, CZ + 12):
        for x in range(CX - 1, CX + 2):
            if (x, z) in bottom: S(x, TOP, z, 'calcite' if (x + z) % 3 else 'smooth_quartz'); used.add((x, z))
    for x in range(CX - 2, CX + 3):
        for z in range(CZ + 8, CZ + 13):
            dd = math.hypot(x - CX, z - (CZ + 10))
            if dd <= 2.3 and (x, z) in bottom:
                S(x, TOP, z, 'gold_block' if 1.6 < dd else 'smooth_quartz' if dd < 0.6 else 'calcite'); used.add((x, z))

    # ---------------- the arches: eight, round the rim, each facing the middle
    tops = []
    for k in range(ARCHES):
        a = 2 * math.pi * k / ARCHES + math.pi / 8           # (none straight across the path)
        c = (CX + 9.0 * math.cos(a), CZ + 9.0 * math.sin(a)); t = (-math.sin(a), math.cos(a))
        ends = [(round(c[0] + s_ * 2.1 * t[0]), round(c[1] + s_ * 2.1 * t[1])) for s_ in (-1, 1)]
        for (x, z) in ends:
            S(x, TOP, z, 'chiseled_quartz_block')
            for y in range(G, G + 5): S(x, y, z, 'quartz_pillar[axis=y]')
            S(x, G + 5, z, 'chiseled_quartz_block')
            used.add((x, z))
        lint = _line4(ends[0], ends[1])
        mid = lint[len(lint) // 2]
        for (x, z) in lint:
            S(x, G + 6, z, 'gold_block' if (x, z) == mid else 'smooth_quartz')
        S(mid[0], G + 7, mid[1], 'smooth_quartz_slab[type=bottom,waterlogged=false]')
        S(mid[0], G + 5, mid[1], 'lantern[hanging=true,waterlogged=false]')
        tops.append(ends)
    # ---------------- the threads: from each arch to the next, two strands, sagging a little in the middle
    for k in range(ARCHES):
        a, b = tops[k][1], tops[(k + 1) % ARCHES][0]
        cells = _line4(a, b)[1:-1]
        n = len(cells)
        for s_, (hy, col) in enumerate(((G + 4, THREADS[k][0]), (G + 2, THREADS[k][1]))):
            for j, (x, z) in enumerate(cells):
                sag = 1 if 0.25 < (j + 0.5) / n < 0.75 else 0
                S(x, hy - sag, z, f'{col}_stained_glass_pane')

    # ---------------- the dais: two steps of smooth quartz, stairs round the lower one, gold at its heart
    for x in range(CX - 4, CX + 5):
        for z in range(CZ - 4, CZ + 5):
            dx, dz = abs(x - CX), abs(z - CZ)
            if dx + dz > 6: continue
            used.add((x, z))
            if dx <= 2 and dz <= 2 and dx + dz <= 3:
                S(x, G, z, 'smooth_quartz'); S(x, G + 1, z, 'gold_block' if (dx, dz) == (0, 0) else 'chiseled_quartz_block' if dx + dz == 3 else 'smooth_quartz')
            elif dx + dz <= 5 and max(dx, dz) <= 3:
                S(x, G, z, 'smooth_quartz' if dx + dz <= 4 else 'quartz_bricks')
            else:
                face = ('west' if x > CX else 'east') if dx >= dz else ('north' if z > CZ else 'south')
                S(x, G, z, f'quartz_stairs[facing={face},half=bottom,shape=straight,waterlogged=false]')
    # the upper step's own stairs: up from the path (south)
    for x in range(CX - 1, CX + 2):
        S(x, G + 1, CZ + 3, 'quartz_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]')

    # ---------------- the great loom, on the dais's north side: birch uprights and beam, a half-woven tapestry, its warp above
    L = G + 2; zl = CZ - 2
    for x in range(CX - 3, CX + 4): S(x, G + 1, zl, 'smooth_quartz')
    for x in (CX - 3, CX + 3):
        for y in range(L, L + 5): S(x, y, zl, 'stripped_birch_log[axis=y]')
    for x in range(CX - 3, CX + 4): S(x, L + 5, zl, 'stripped_birch_log[axis=x]')
    for x in range(CX - 2, CX + 3):
        S(x, L, zl, 'birch_slab[type=top,waterlogged=false]')                      # (the breast beam the cloth winds onto)
        for j, y in enumerate(range(L + 1, L + 3)):
            S(x, y, zl, f'{TAPESTRY[(x - CX + 2 + 2 * j) % len(TAPESTRY)]}_wool')   # (the woven part)
        S(x, L + 3, zl, f'{TAPESTRY[(x - CX + 2) % len(TAPESTRY)]}_stained_glass_pane')   # (the weft being drawn through)
        S(x, L + 4, zl, 'birch_fence')                                             # (the warp, still to weave)
    S(CX - 3, G + 1, zl + 1, 'loom[facing=south]')
    S(CX + 2, G + 2, zl + 1, 'birch_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]')   # (a bench before it)
    for x in (CX - 4, CX + 4):                          # (a lantern on the step either side of it)
        if B.get(x, G, zl): S(x, G + 1, zl, 'lantern[hanging=false,waterlogged=false]')

    # ---------------- four flowering trees, between the dais and the arches
    for k, a in enumerate((0.45, 2.0, 3.6, 5.2)):
        tx, tz = round(CX + 6.4 * math.cos(a)), round(CZ + 6.4 * math.sin(a))
        if abs(tx - CX) <= 2 and tz > CZ: tx += 3
        h = 4 + k % 2
        for y in range(G, G + h): S(tx, y, tz, 'cherry_log[axis=y]')
        used.add((tx, tz))
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                for dy in range(-1, 2):
                    rr = abs(dx) + abs(dz) + abs(dy) * 1.5
                    if rr > 3.2 or (dx == dz == 0 and dy < 1): continue
                    x, y, z = tx + dx, G + h - 1 + dy, tz + dz
                    if B.get(x, y, z) is None and rnd.random() < (0.95 if rr < 2.5 else 0.6):
                        S(x, y, z, 'flowering_azalea_leaves[distance=1,persistent=true,waterlogged=false]' if (dx + dz + k) % 4 == 0
                          else 'cherry_leaves[distance=1,persistent=true,waterlogged=false]')
        S(tx, G + h, tz, 'cherry_leaves[distance=1,persistent=true,waterlogged=false]')
        for dx, dz in ((1, 0), (-1, 1), (0, -1), (1, 1)):
            if (tx + dx, tz + dz) in bottom and (tx + dx, tz + dz) not in used and B.get(tx + dx, G, tz + dz) is None:
                S(tx + dx, G, tz + dz, f'pink_petals[facing=north,flower_amount={1 + (dx + dz) % 4}]'); used.add((tx + dx, tz + dz))

    # ---------------- the grass: wildflowers, daisies, cornflowers, alliums, a few tufts
    FLOWERS = [('short_grass', 5), ('wildflowers[facing=north,flower_amount=3]', 3), ('oxeye_daisy', 2), ('cornflower', 2), ('allium', 1),
               ('lily_of_the_valley', 2), ('pink_petals[facing=east,flower_amount=2]', 2), ('firefly_bush', 1)]
    for (x, z) in bottom:
        if (x, z) in used or B.get(x, TOP, z) != 'minecraft:grass_block[snowy=false]' or B.get(x, G, z) is not None: continue
        d = math.hypot(x - CX, z - CZ)
        if d > edge(x, z) - 0.8: continue
        if rnd.random() < 0.3: S(x, G, z, pick(FLOWERS))

    if markers:
        B.marker(SPAWN[0], SPAWN[1], SPAWN[2], ['bm.kb_spawn'], SPAWN[3])
        B.marker(DAIS[0], DAIS[1], DAIS[2], ['bm.kb_dais'], 0.0)
        B.marker(ARRIVAL[0], ARRIVAL[1], ARRIVAL[2], ['bm.kb_arrive'], 180.0)
    return B

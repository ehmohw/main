"""2.91: THE UNDERWATER KINGDOM - Emma's home castle on the deep sea floor, under a bubble dome (the datapack side is phase199).

From the owner's reference: a grey stone castle with light-blue cone roofs and blue bands, magenta flags on poles, ruined - cracks,
holes, a fallen turret lying on the grass, scorch marks and fire in the windows - an arched gate, on a green hill with a grey
path up to it and pink flowers. All of it under a dome of glass full of air at the bottom of the sea.

Template coordinates: x 0..SX-1, y 0..SY-1, z 0..SZ-1; the gate faces north (-z), the path runs up the hill from the dome's
Tide Door at the low z. Only the dome and what is in it are set: everything outside the dome's shell is left out of the
template, so the sea floor and the water around it stay as they were. The floor of the dome is FY (the seed's level); the
plateau the castle stands on is three blocks higher (walk P)."""
import math
import random

from structures import Build

SX, SY, SZ = 71, 32, 71
CX, CZ = 35, 35                          # the dome's middle
FY = 3                                   # the dome's floor (grass/sand at FY, walk FY+1); below it, the foundation
RA, RB = 34.0, 27.0                      # the dome: 34 across (each way), 27 high
P = FY + 4                               # the plateau's walk height (its grass at P-1)
WALL = (22, 48, 24, 46)                  # the curtain wall: x0, x1, z0, z1
TOWERS = [(22, 24), (48, 24), (22, 46), (48, 46)]
BROKEN = (48, 24)                        # the front-right tower: fallen (its roof lies on the grass outside)
GATE_T = [(31, 24), (39, 24)]            # the gatehouse's two little towers
KEEP = (35, 44)                          # the keep (the throne room) at the back
FOUNT = (35, 31)                         # the courtyard's fountain (the Dome Heart on its pillar)
ALCOVE = (33, 37, 52, 55)                # the Serpent's Alcove behind the keep: x0, x1, z0, z1 (walls; inside x34..36, z53..54)
SEAL = [(x, y, 51) for x in (34, 35, 36) for y in (P, P + 1, P + 2)]      # the carved stone between the keep and the alcove
CASTLE_BOX = (10, 60, 8, 60)             # what restoration rebuilds: x0, x1, z0, z1 (inside the dome only)

DOOR_Z = 1                               # the Tide Door in the dome's north side (x 34..36, walk FY+1)


def dome_d(x, y, z):
    return math.sqrt(((x - CX) / RA) ** 2 + ((y - FY) / RB) ** 2 + ((z - CZ) / RA) ** 2)


def in_dome(x, y, z):
    """inside the dome's skin (or the ground under it)"""
    return dome_d(x, max(y, FY), z) <= 1.0


def is_shell(x, y, z):
    if y < FY or not in_dome(x, y, z): return False
    return any(not in_dome(x + dx, y + dy, z + dz) for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, -1)))


def hill(x, z):
    r = math.hypot(x - CX, z - CZ)
    return 3 if r <= 19 else 2 if r <= 23 else 1 if r <= 27 else 0


STAIR = lambda m, f, half='bottom': f'{m}_stairs[facing={f},half={half},shape=straight,waterlogged=false]'


def build(ruined=True):
    B = Build(SX, SY, SZ)
    rnd = random.Random(29100 if ruined else 29101)
    S = B.set
    get = B.get
    pick = lambda pal: rnd.choices([p for p, _ in pal], [w for _, w in pal])[0]
    STONE = [('stone_bricks', 10), ('cracked_stone_bricks', 4 if ruined else 0), ('mossy_stone_bricks', 2 if ruined else 1),
             ('andesite', 1), ('polished_andesite', 1), ('stone', 1)]
    stone = lambda: pick(STONE)
    B.meta = {'fires': [], 'cracks': []}

    # ---------------------------------------------------------------- the dome, its floor, the hill
    for x in range(SX):
        for z in range(SZ):
            if not in_dome(x, FY, z): continue
            h = hill(x, z)
            for y in range(0, FY):
                S(x, y, z, 'stone' if y < FY - 1 else 'dirt')
            for y in range(FY, SY):
                if not in_dome(x, y, z): break
                if is_shell(x, y, z):
                    S(x, y, z, 'glass')
                elif y < FY + h:
                    S(x, y, z, 'dirt')
                elif y == FY + h:
                    S(x, y, z, 'grass_block[snowy=false]' if math.hypot(x - CX, z - CZ) < 31.5 else 'sand')
                else:
                    S(x, y, z, 'air')

    def surf(x, z):
        """the walk height at (x, z) on the hill"""
        return FY + hill(x, z) + 1

    # the path: three wide, grey, from the Tide Door up the hill to the gate (stairs where the hill steps up)
    for z in range(DOOR_Z + 1, WALL[2]):
        for x in (34, 35, 36):
            y = surf(x, z) - 1
            if get(x, y, z) in (None, 'minecraft:glass'): continue
            S(x, y, z, rnd.choice(['andesite', 'polished_andesite', 'cobblestone', 'gravel', 'andesite']))
            if hill(x, z + 1) > hill(x, z):
                S(x, y + 1, z, STAIR('stone_brick', 'south'))

    # ---------------------------------------------------------------- the castle
    def disc(cx, cz, r):
        return [(x, z) for x in range(int(cx - r - 1), int(cx + r + 2)) for z in range(int(cz - r - 1), int(cz + r + 2))
                if math.hypot(x - cx, z - cz) <= r]

    def cone(cx, cz, y0, radii, roof='light_blue_concrete', rim='blue_concrete'):
        for i, r in enumerate(radii):
            for (x, z) in disc(cx, cz, r):
                S(x, y0 + i, z, rim if i == 0 else roof)
        return y0 + len(radii)

    def flag(x, y, z, length=2):
        S(x, y, z, 'end_rod[facing=up]'); S(x, y + 1, z, 'end_rod[facing=up]')
        for i in range(1, length + 1):
            S(x + i, y + 1, z, 'magenta_wool')
            if i < length or length == 1: S(x + i, y, z, 'magenta_wool')

    def scorch(x, y, z, n=4):
        """soot round a window, on the wall's face"""
        for _ in range(n):
            px, py, pz = x + rnd.randint(-1, 1), y + rnd.randint(-1, 2), z + rnd.randint(-1, 1)
            st = get(px, py, pz)
            if st and ('brick' in st or 'andesite' in st or st == 'minecraft:stone'):
                S(px, py, pz, rnd.choice(['blackstone', 'coal_block', 'black_concrete', 'polished_blackstone', 'gilded_blackstone' if False else 'blackstone']))

    def window_fire(x, y, z):
        """a window that's burning: a campfire on its sill, soot round it, a marker for the flames and smoke"""
        if ruined:
            S(x, y, z, 'campfire[lit=true,signal_fire=false,facing=north,waterlogged=false]')
            scorch(x, y, z, 6)
            B.meta['fires'].append((x, y, z))
        else:
            S(x, y, z, 'air')

    # the plateau's floor inside the walls: stone flags with grass between
    x0, x1, z0, z1 = WALL
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            S(x, P - 1, z, rnd.choice(['stone_bricks', 'polished_andesite', 'grass_block[snowy=false]', 'grass_block[snowy=false]', 'andesite']))
            for y in range(P, P + 12):
                S(x, y, z, 'air')
    for z in range(z0, z1 + 1):                                         # the yard's paths (gate to keep, and across)
        for x in (34, 35, 36):
            S(x, P - 1, z, 'polished_andesite' if (x + z) % 3 else 'stone_bricks')
    for x in range(x0 + 2, x1 - 1):
        S(x, P - 1, FOUNT[1], 'polished_andesite' if x % 3 else 'stone_bricks')

    # the curtain wall: seven high, battlements, a blue band under them
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if not (x in (x0, x1) or z in (z0, z1)): continue
            top = P + 6
            if ruined and rnd.random() < 0.10: top = P + rnd.randint(3, 5)          # crumbled stretches
            for y in range(P - 1, top + 1):
                S(x, y, z, 'blue_terracotta' if y == P + 5 else stone())
            if top == P + 6 and (x + z) % 2 == 0: S(x, P + 7, z, stone())
    # holes knocked through (the ruin), and slits
    if ruined:
        for (x, y, z) in [(x0, P + 2, 30), (x0, P + 3, 30), (x0, P + 2, 31), (x1, P + 1, 38), (x1, P + 2, 38), (x1, P + 2, 39),
                          (27, P + 3, z1), (28, P + 3, z1), (28, P + 2, z1), (43, P + 2, z0), (44, P + 3, z0)]:
            S(x, y, z, 'air')
    for z in range(z0 + 3, z1 - 2, 4):
        for x in (x0, x1):
            S(x, P + 3, z, 'air')

    # the gate: an arched opening, a raised portcullis, magenta over it, the two gate towers
    for x in range(33, 38):
        for y in range(P - 1, P + 8):
            S(x, y, z0, stone())
    for x in (34, 35, 36):
        for y in range(P, P + 3):
            S(x, y, z0, 'air')
    S(35, P + 3, z0, 'air')
    S(34, P + 3, z0, STAIR('stone_brick', 'east', 'top')); S(36, P + 3, z0, STAIR('stone_brick', 'west', 'top'))
    S(35, P + 4, z0, 'chiseled_stone_bricks')
    S(34, P + 5, z0 - 1, 'magenta_wall_banner[facing=north]'); S(36, P + 5, z0 - 1, 'magenta_wall_banner[facing=north]')
    for (cx, cz) in GATE_T:
        for (x, z) in disc(cx, cz, 2.5):
            r = math.hypot(x - cx, z - cz)
            for y in range(P - 1, P + 10):
                S(x, y, z, ('blue_terracotta' if y == P + 8 else stone()) if r > 1.5 or y == P - 1 else 'air')
            S(x, P + 10, z, stone())
        top = cone(cx, cz, P + 11, [3.2, 2.5, 1.8, 1.2, 0.5])
        flag(cx, top, cz, 1)
        for (wx, wz) in ((cx, cz - 2),):
            S(wx, P + 5, wz, 'air')

    # the corner towers (one fallen): round, a blue band, a light-blue cone and a flag on each
    for (cx, cz) in TOWERS:
        fallen = ruined and (cx, cz) == BROKEN
        for (x, z) in disc(cx, cz, 3.5):
            r = math.hypot(x - cx, z - cz)
            S(x, P - 1, z, 'stone_bricks')
            top = P + 8
            if fallen: top = P + 1 + int(abs(math.sin(x * 1.7 + z * 2.3)) * 5)
            for y in range(P, top + 1):
                if r > 2.5:
                    S(x, y, z, 'blue_terracotta' if y == P + 7 else stone())
                else:
                    S(x, y, z, 'air')
        if not fallen:
            top = cone(cx, cz, P + 9, [4.6, 4.0, 3.3, 2.6, 1.9, 1.2, 0.5])
            flag(cx, top, cz, 2)
        # a door from the yard, windows out (some burning)
        dx = 1 if cx < CX else -1
        dz = 1 if cz < CZ else -1
        for y in (P, P + 1):
            S(cx + 3 * dx, y, cz, 'air') if (cx + 3 * dx, y, cz) and get(cx + 3 * dx, y, cz) else None
        for y in (P, P + 1):
            S(cx, y, cz + 3 * dz, 'air')
        if not fallen:
            window_fire(cx - 3 * dx, P + 4, cz)
            S(cx - 3 * dx, P + 5, cz, 'air')
            S(cx, P + 4, cz - 3 * dz, 'air'); S(cx, P + 5, cz - 3 * dz, 'air')
            # a chest of the kingdom's left-behinds inside
            S(cx - dx, P, cz - dz, 'chest[facing=%s,type=single,waterlogged=false]' % ('south' if dz < 0 else 'north'),
              {'id': 'minecraft:chest', 'LootTable': 'bm:chests/p199_tower'})
            S(cx + dx, P, cz - dz, 'barrel[facing=up,open=false]', {'id': 'minecraft:barrel', 'LootTable': 'bm:chests/p199_tower'})
            S(cx, P + 3, cz, 'lantern[hanging=false,waterlogged=false]'); S(cx, P + 2, cz, 'andesite_wall')
    # the fallen roof: lying on its side on the grass outside, its flag in the dirt
    if ruined:
        bx, bz = BROKEN
        ax, az = bx + 3, bz - 8                                          # where its rim came down
        y0 = surf(ax, az) + 3
        radii = [4.6, 4.0, 3.3, 2.6, 1.9, 1.2, 0.5]
        for i, r in enumerate(radii):
            x = ax + i
            for y in range(y0 - 5, y0 + 6):
                for z in range(az - 5, az + 6):
                    if math.hypot(y - y0 + i * 0.35, z - az) <= r and y >= surf(x, z) - 1:
                        S(x, y, z, 'blue_concrete' if i == 0 else 'light_blue_concrete')
        tip = ax + len(radii)
        S(tip, surf(tip, az), az, 'end_rod[facing=east]'); S(tip + 1, surf(tip + 1, az), az, 'end_rod[facing=east]')
        S(tip + 1, surf(tip + 1, az + 1) - 1, az + 1, 'magenta_wool'); S(tip + 2, surf(tip + 2, az + 1) - 1, az + 1, 'magenta_wool')
        # rubble round the broken tower and down the hill
        for _ in range(40):
            x, z = bx + rnd.randint(-7, 9), bz + rnd.randint(-11, 4)
            if not in_dome(x, surf(x, z), z) or (x0 <= x <= x1 and z0 <= z <= z1): continue
            y = surf(x, z)
            if get(x, y, z) == 'minecraft:air' and get(x, y - 1, z) not in (None, 'minecraft:glass', 'minecraft:air'):
                S(x, y, z, rnd.choice(['cobblestone', 'cracked_stone_bricks', 'stone_bricks', 'andesite', 'cobblestone_slab[type=bottom,waterlogged=false]',
                                       'stone_brick_slab[type=bottom,waterlogged=false]']))

    # the keep: the throne room, the tallest tower
    kx, kz = KEEP
    for (x, z) in disc(kx, kz, 6.5):
        r = math.hypot(x - kx, z - kz)
        S(x, P - 1, z, 'polished_diorite' if r < 5.5 else 'stone_bricks')
        for y in range(P, P + 11):
            S(x, y, z, ('blue_terracotta' if y == P + 9 else stone()) if r > 5.5 else 'air')
        S(x, P + 11, z, 'stone_bricks' if r > 5.5 else 'smooth_stone')
    top = cone(kx, kz, P + 12, [7.6, 6.4, 5.2, 4.0, 2.8, 1.6, 0.6])
    flag(kx, top, kz, 3)
    for x in (34, 35, 36):                                               # its door from the yard (arched)
        for y in range(P, P + 3):
            S(x, y, kz - 6, 'air')
    S(35, P + 3, kz - 6, 'air')
    for y in range(P, P + 3):                                            # (two blocks deep: the wall's ring is thick there)
        for x in (34, 35, 36):
            if math.hypot(x - kx, (kz - 5) - kz) > 5.5: S(x, y, kz - 5, 'air')
    for (wx, wz, fire) in ((kx - 6, kz, True), (kx + 6, kz, False), (kx - 4, kz - 5, False), (kx + 4, kz - 5, True), (kx - 5, kz + 3, False)):
        if fire:
            window_fire(wx, P + 5, wz)
        else:
            S(wx, P + 5, wz, 'air')
        S(wx, P + 6, wz, 'air')
    # inside: the aisle, the two thrones (the queen's, empty; the regent's), the Tide Font, the steward's corner, banners
    for z in range(kz - 5, kz + 5):
        S(35, P - 1, z, 'blue_wool' if False else 'polished_diorite')
        S(35, P, z, 'blue_carpet')
    for (tx, mat) in ((33, 'quartz'), (37, 'quartz')):
        tz = kz + 4
        S(tx, P, tz, STAIR(mat, 'north'))
        S(tx, P + 1, tz + 1, 'prismarine_bricks'); S(tx, P, tz + 1, 'prismarine_bricks'); S(tx, P + 2, tz + 1, 'sea_lantern')
        S(tx - 1, P, tz, 'quartz_slab[type=top,waterlogged=false]' if False else STAIR(mat, 'east')); S(tx + 1, P, tz, STAIR(mat, 'west'))
        S(tx, P - 1, tz, 'gold_block')
    S(35, P, kz, 'prismarine_bricks'); S(35, P + 1, kz, 'water_cauldron[level=3]')                # the Tide Font
    S(34, P - 1, kz, 'sea_lantern'); S(36, P - 1, kz, 'sea_lantern')
    S(30, P, kz - 2, 'barrel[facing=up,open=false]'); S(30, P, kz - 1, 'barrel[facing=up,open=false]')             # the steward's stock
    S(40, P, kz - 2, 'lectern[facing=west,has_book=false,powered=false]')                                         # the request stand
    for (x, z) in ((31, kz - 4), (39, kz - 4), (30, kz + 2), (40, kz + 2)):
        S(x, P, z, 'andesite_wall'); S(x, P + 1, z, 'lantern[hanging=false,waterlogged=false]')
    for x in (33, 37):
        S(x, P + 4, kz + 6, 'magenta_wall_banner[facing=north]')
    S(35, P + 6, kz + 6, 'magenta_wall_banner[facing=north]')
    for (x, z) in disc(kx, kz, 4.0):
        if (x + z) % 5 == 0: S(x, P + 10, z, 'lantern[hanging=true,waterlogged=false]')

    # the Serpent's Alcove: sealed behind the thrones (carved stone - a serpent's coil), a stone serpent coiled on a plinth
    ax0, ax1, az0, az1 = ALCOVE
    for x in range(ax0, ax1 + 1):
        for z in range(az0 - 1, az1 + 1):
            S(x, P - 1, z, 'polished_blackstone_bricks')
            for y in range(P, P + 4):
                edge = x in (ax0, ax1) or z == az1 or z == az0 - 1
                S(x, y, z, stone() if edge else 'air')
            S(x, P + 4, z, 'stone_bricks')
    for (x, y, z) in SEAL:
        S(x, y, z, 'chiseled_stone_bricks')
        if z - 1 >= 0 and get(x, y, z - 1) == 'minecraft:air': pass
    for (x, y, z) in [(x, y, kz + 6) for x in (34, 35, 36) for y in (P, P + 1, P + 2)]:     # the keep's own wall there: the same carving
        if get(x, y, z) and get(x, y, z) != 'minecraft:air': S(x, y, z, 'chiseled_stone_bricks')
    S(35, P, 54, 'polished_blackstone'); S(35, P + 1, 54, 'black_glazed_terracotta' if False else 'obsidian')
    S(34, P, 54, 'green_glazed_terracotta'); S(36, P, 54, 'green_glazed_terracotta')
    S(34, P + 1, 54, 'soul_lantern[hanging=false,waterlogged=false]'); S(36, P + 1, 54, 'soul_lantern[hanging=false,waterlogged=false]')

    # the courtyard: a fountain (the Dome Heart's pillar in it), flowers, a well-trodden yard
    fx, fz = FOUNT
    for (x, z) in disc(fx, fz, 2.6):
        r = math.hypot(x - fx, z - fz)
        S(x, P - 1, z, 'prismarine_bricks')
        S(x, P, z, 'prismarine_brick_slab[type=bottom,waterlogged=false]' if r > 1.6 else 'water')
    for y in range(P, P + 3):
        S(fx, y, fz, 'prismarine_bricks')
    S(fx, P + 3, fz, 'sea_lantern')
    for _ in range(14):
        x, z = rnd.randint(x0 + 1, x1 - 1), rnd.randint(z0 + 1, z1 - 1)
        if get(x, P - 1, z) == 'minecraft:grass_block[snowy=false]' and get(x, P, z) == 'minecraft:air':
            S(x, P, z, rnd.choice(['pink_tulip', 'pink_petals[facing=north,flower_amount=3]', 'allium', 'short_grass', 'short_grass']))

    # outside on the hill: pink flowers, grass, lights (sea lanterns set in the turf), rubble near the walls
    for x in range(SX):
        for z in range(SZ):
            y = surf(x, z) if in_dome(x, FY, z) else None
            if y is None or get(x, y - 1, z) != 'minecraft:grass_block[snowy=false]' or get(x, y, z) != 'minecraft:air': continue
            if x0 - 1 <= x <= x1 + 1 and z0 - 1 <= z <= z1 + 1: continue
            if (x % 8 == 3) and (z % 8 == 3) and not (33 <= x <= 37):
                S(x, y - 1, z, 'sea_lantern'); continue
            v = rnd.random()
            if v < 0.012: S(x, y, z, 'pink_tulip')
            elif v < 0.020: S(x, y, z, 'pink_petals[facing=%s,flower_amount=%d]' % (rnd.choice(['north', 'south', 'east', 'west']), rnd.randint(2, 4)))
            elif v < 0.024 and get(x, y + 1, z) == 'minecraft:air':
                S(x, y, z, 'peony[half=lower]'); S(x, y + 1, z, 'peony[half=upper]')
            elif v < 0.16: S(x, y, z, 'short_grass')
    for z in range(DOOR_Z + 3, WALL[2] - 1, 5):                          # lamp posts up the path
        for x in (32, 38):
            y = surf(x, z)
            if get(x, y, z) in ('minecraft:air', 'minecraft:short_grass', 'minecraft:pink_tulip') and get(x, y + 2, z) == 'minecraft:air':
                S(x, y, z, 'stone_brick_wall'); S(x, y + 1, z, 'lantern[hanging=false,waterlogged=false]')
    # lights inside the walls (no darkness for anything to crawl out of)
    for (x, z) in ((26, 28), (44, 28), (26, 40), (44, 40), (30, 34), (40, 34)):
        if get(x, P, z) in ('minecraft:air', 'minecraft:short_grass', 'minecraft:pink_tulip', 'minecraft:allium'):
            S(x, P, z, 'stone_brick_wall'); S(x, P + 1, z, 'lantern[hanging=false,waterlogged=false]')

    # ---------------------------------------------------------------- the Tide Door: a frame of prismarine round a shimmering pane
    for x in range(33, 38):
        for y in range(FY, FY + 5):
            if is_shell(x, y, DOOR_Z) or (get(x, y, DOOR_Z) == 'minecraft:glass'):
                inner = 34 <= x <= 36 and FY + 1 <= y <= FY + 3
                S(x, y, DOOR_Z, 'light_blue_stained_glass' if inner else 'prismarine_bricks')
    for x in range(33, 38):                                              # its threshold and a landing inside
        for z in range(DOOR_Z + 1, DOOR_Z + 3):
            if get(x, FY, z) not in (None, 'minecraft:glass'): S(x, FY, z, 'prismarine_bricks')

    # ---------------------------------------------------------------- markers (the datapack finds its pieces by these)
    B.marker(CX + 0.5, P, kz - 2.5, ['bm.kgnew', 'bm.kgcore'], 180)                       # the castle (the throne room's middle)
    B.marker(35.5, P, kz + 0.5, ['bm.kspot', 'bm.kspot_font'], 180)
    B.marker(31.5, P, kz - 1.5, ['bm.kspot', 'bm.kspot_steward'], -90)
    B.marker(40.5, P, kz - 2.5, ['bm.kspot', 'bm.kspot_board'], 90)
    B.marker(35.5, P, 54.5, ['bm.kspot', 'bm.kspot_alcove'], 0)
    B.marker(35.5, P, 51.5, ['bm.kspot', 'bm.kspot_seal'], 0)
    B.marker(fx + 0.5, P + 3, fz + 0.5, ['bm.kspot', 'bm.kspot_heart'], 180)
    B.marker(35.5, FY + 1, DOOR_Z - 0.5, ['bm.kspot', 'bm.kdoor_o'], 180)                # just outside the Tide Door
    B.marker(35.5, FY + 1, DOOR_Z + 3.5, ['bm.kspot', 'bm.kdoor_i'], 0)                  # just inside it
    for (x, y, z) in B.meta['fires']:
        B.marker(x + 0.5, y + 0.4, z + 0.5, ['bm.kspot', 'bm.kfire'], 0)
    # where the dome can crack: twelve spots round its foot (none at the door), just inside the glass at head height
    for i in range(12):
        a = math.radians(15 + 30 * i)
        best = None
        for t in range(10, 40):
            x, z = int(round(CX + 0.5 + t * math.sin(a) - 0.5)), int(round(CZ + 0.5 - t * math.cos(a) - 0.5))
            y = FY + 2
            if not (0 <= x < SX and 0 <= z < SZ) or not in_dome(x, y, z): break
            if is_shell(x, y, z): break
            if get(x, y, z) == 'minecraft:air' and get(x, y - 1, z) == 'minecraft:air' and not is_shell(x, y - 1, z): best = (x, y, z)
        if best and abs(best[0] - 35) > 4:
            B.meta['cracks'].append(best)
            B.marker(best[0] + 0.5, best[1] - 1, best[2] + 0.5, ['bm.kspot', 'bm.kcrack_spot'], 0)
    return B


def restored_crop():
    """the restored castle, cut to the castle's box and the dome's inside (the dome itself, and the hill beyond, stay)"""
    R = build(ruined=False)
    x0, x1, z0, z1 = CASTLE_BOX
    C = Build(x1 - x0 + 1, SY - (P - 2), z1 - z0 + 1)
    for (x, y, z), st in R.b.items():
        if not (x0 <= x <= x1 and z0 <= z <= z1 and y >= P - 1): continue
        if is_shell(x, y, z) or not in_dome(x, y, z): continue
        if math.hypot(x - CX, z - CZ) > 30: continue                     # (the hill's edge and the glass: left alone)
        C.set(x - x0, y - (P - 2), z - z0, st, R.nbt.get((x, y, z)))
    return C


def shell_columns():
    """per (x, z): the dome's skin as a run of y (for the mend/flood commands), and its inside's run of y above the floor"""
    cols = {}
    for x in range(SX):
        for z in range(SZ):
            ys = [y for y in range(FY, SY) if is_shell(x, y, z)]
            ins = [y for y in range(FY + 1, SY) if in_dome(x, y, z) and not is_shell(x, y, z)]
            if ys: cols[(x, z)] = (ys, ins)
    return cols


def check(B):
    """static proofs: watertight, reachable on foot from the Tide Door, nothing pokes through the glass"""
    import p2.verify as V
    from p2.verify import Grid
    errs = []
    # the skin is whole: every inside cell's six neighbours are inside or glass/solid
    for (x, y, z), st in B.b.items():
        if y <= FY or not in_dome(x, y, z) or is_shell(x, y, z): continue
        for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, -1)):
            n = (x + dx, y + dy, z + dz)
            if n not in B.b: errs.append(f'leak beside {n}'); break
    for (x, y, z), st in B.b.items():
        if is_shell(x, y, z) and st.split('[')[0] not in ('minecraft:glass', 'minecraft:light_blue_stained_glass', 'minecraft:prismarine_bricks'):
            errs.append(f'shell {(x, y, z)} is {st}')
    G = Grid(B, outside='solid')
    V.GRID = G
    seen = G.bfs([(35, FY + 1, DOOR_Z + 3)], margin=0)
    kx, kz = KEEP
    want = {'the gate': (35, P, WALL[2]), 'the fountain': (35, P, FOUNT[1] - 3), 'the throne room': (35, P, kz - 2),
            'the font': (35, P, kz - 1), 'the steward': (32, P, kz - 1), 'the request stand': (39, P, kz - 2)}
    for nm, p in want.items():
        if not any(abs(a - p[0]) <= 1 and abs(c - p[2]) <= 1 and b == p[1] for (a, b, c) in seen):
            errs.append(f'{nm} {p} not reachable on foot from the Tide Door')
    for (x, y, z), st in B.b.items():
        nm = st.split('[')[0].split(':')[1]
        if nm in ('lantern', 'soul_lantern'):
            hang = 'hanging=true' in st
            n = B.b.get((x, y + (1 if hang else -1), z), 'minecraft:air')
            if n == 'minecraft:air': errs.append(f'{nm} {(x, y, z)} hangs from air')
        if nm in ('pink_tulip', 'allium', 'short_grass', 'pink_petals', 'peony'):
            n = B.b.get((x, y - 1, z), 'minecraft:air')
            if n.split('[')[0] not in ('minecraft:grass_block', 'minecraft:dirt', 'minecraft:peony'): errs.append(f'{nm} {(x, y, z)} on {n}')
    return sorted(set(errs))


if __name__ == '__main__':
    B = build()
    print(len(B.b), 'blocks;', len(B.meta['fires']), 'fires;', len(B.meta['cracks']), 'crack spots')
    e = check(B)
    print(len(e), 'problems'); print('\n'.join(e[:30]))
    C = restored_crop()
    print('restored crop', C.size, len(C.b))

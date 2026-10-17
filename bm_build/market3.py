"""THE BLACK MARKET 3 (2.81): a rat town in a domed cavern - streets, districts, houses with roofs, landmarks.

The same 76 x 32 x 98 cavern, the same vault door and tunnel (south), the same rooms behind the north wall (the Dark
Auction's hall, the Gilded Gutter) and the same Rat Gang HQ behind its mouse hole - only the town inside is new.
The bm.mkt marker sits where it always did (template 38.5, 12, 46.5), so everything placed at run time relative to it
lands the same way in every market, turned or not.

Layout (x east, z south; walk level y10 unless noted):
  south   THE LOOKOUT: the vault door (walk y18) opens onto a rock terrace; a curling stair (west) and a ladder hoist
          (east) down to the ARRIVAL SQUARE and its gate arch. Under the terrace an arcade: Dennis's Assay Office and
          Pistachio's Pantry (their rooms are dug at run time, phase162).
  centre  FOUNTAIN PLAZA: round; the falls from the dome into Mike's pond; lamp posts, market stalls, the Bounty Board.
  north   PAWN ALLEY curves up to the Dark Auction's gate: Barnaby's pawn shop with THE STACKS on its top floor (walk y18,
          Prof. Whiskerton), Madame Velour's outfitters, THE FENCE (a roof terrace at y18 - the Gilded Gutter's gate opens
          off it; a rope bridge from the Stacks and an outside stair lead up), the clock tower.
  north-east  FURNACE ROW: Vinny's gunsmith, Steelwhisker's armory, THE FORGE PIT (lava behind bars, the great chimney),
          CURIO COURT (Fishy's Cabinet door, phase145).
  east    THE GNAWED FLAGON (Chef Fromage), a two-storey tavern on its own deck.
  south-east  NIGHT ALLEY: narrow and red-lit - Cecil's tent, THE BLOOD ALCOVE (a crimson keep behind a portcullis).
  west    THE WHARF: the river curves through; stilt docks, a crane, the stone bridge and The Drop; on the far bank
          Cheddarbeard's dock house (Salty Sal at its counter; the mouse hole into Rat Gang HQ in its back wall), the
          boathouse, and THE LUCKY DEN - a riverboat casino moored in the harbour basin.
Safety by construction, as in market2: every rock face touching open space is spring-safe, nothing flammable within
reach of lava, every walkable cell lit (spawnproof), no fluid touching the world outside, the market sealed."""
import re
import math
import random
from structures import Build
import market2 as M2
from market2 import (is_full, spawn_surface, spawnproof, support_lanterns, flammable, SPRING_SAFE, ROCK_IN, PLAZA, STREET,
                     FLOOR_BLOCKS, EMIT, light_map, walkable)

# blocks a market floor may be made of (bm:market_floor): market2's, and the new streets, quays and decks
FLOOR_BLOCKS = list(FLOOR_BLOCKS) + ['deepslate_tiles', 'cracked_deepslate_tiles', 'cracked_nether_bricks', 'stone_bricks', 'mossy_stone_bricks',
                                     'cracked_stone_bricks', 'polished_andesite', 'cobblestone', 'mossy_cobblestone', 'spruce_slab', 'polished_blackstone_brick_slab']
FLOOR_BLOCKS = sorted(set(FLOOR_BLOCKS))
SX, SY, SZ = 76, 32, 98
GF, W = 9, 10
BF = 17
CX, CZ, RX, RZ = 38, 46, 36.0, 35.0
WATER_TOP = 5
RIVER = (12, 22)              # (x range the curving river channel stays inside)
DOOR_BOX = M2.DOOR_BOX
VIP_SHELL, AUCTION_SEATS, CUSHIONS, COUNTERS, HOLES, LADDERS = [], [], [], [], [], []
TOWN_TAG = 'bm.m282'           # (on the town's marker: a market without it is rebuilt - 2.81a: the 2.81 towns too, for their counters;
                               #  2.82: and again, for the river's ladders and the clock tower's way out)
# water the market keeps (template boxes): the river and the harbour basin, the falls, Mike's pond and the falls into it
WATER_KEEP = [((11, 0, 8), (24, 17, 85)), ((4, 0, 59), (22, 9, 78)), ((CX - 7, 4, CZ - 7), (CX + 7, 11, CZ + 7)), ((CX - 1, 4, CZ - 1), (CX + 1, SY - 1, CZ + 1))]

# spots the run-time installs use (template coordinates), checked by the phases that use them (mgeo.need_floor / need_air)
SPOTS = {
    'board': (34, 36),                                   # the Bounty Board: posts x32/x36, board x33-35 at y11-12, z36, facing south
    'lectern': (34, BF + 1, 80),                         # the newcomers' lectern, on the Lookout beside the way in
    'bin': (33, 23),                                     # the Scrap Bin, by Barnaby's shop front
    'dock': ((9.5, W, 26.5), -90),                       # Salty Sal, behind the dock house counter
    'cecil': ((52.5, W, 70.5), -90),                     # Cecil, in his tent in Night Alley, facing the lane
    'slots': {'wall_x': 8, 'lever_x': 9, 'zs': {67: 'reg', 69: 'jp', 71: 'reg'}, 'pot_z': 69},    # the riverboat's machines
    'gates': {21: ((39.5, W, 15.5), 0, 'public', 'hall_in'), 22: ((39.5, W, 12.5), 180, 'hall', 'hall_out'),
              23: ((48.5, BF + 1, 15.5), 0, 'public', 'vip_in'), 24: ((47.5, BF + 1, 13.5), 180, 'gutter', 'vip_out'),
              25: ((5.5, W, 23.5), 0, 'public', 'den_in'), 26: ((5.5, W, 18.5), 180, 'den', 'den_out')},
    'gate_dest': {'hall_in': ((37.5, W, 12.5), 180, 'hall'), 'hall_out': ((37.5, W, 17.5), 0, 'public'),
                  'vip_in': ((46.5, BF + 1, 12.5), 180, 'gutter'), 'vip_out': ((46.5, BF + 1, 17.5), 0, 'public'),
                  'den_in': ((4.5, W, 16.5), 0, 'den'), 'den_out': ((3.5, W, 24.5), 0, 'public')},
    'floor_ledger': {},                     # (2.81a: none - every trader's back-room book lies on his own counter)
    'portraits': [((31.5, W, 41.5), -45), ((45.5, W, 41.5), 45), ((31.5, W, 51.5), -135), ((45.5, W, 51.5), 135)],
}
NPC_POS = {   # trader markers: (x, y, z, yaw)
    'fence': (46.5, W, 18.5, 90), 'pawn': (29.5, W, 20.5, -90), 'outfitter': (30.5, W, 29.5, -90), 'captain': (3.5, W, 17.5, 0),
    'lucky': (12.5, W, 72.5, 180), 'arms': (56.5, W, 24.5, -90), 'armory': (67.5, W, 30.5, 90), 'chef': (68.5, W, 45.5, 90),
    'blood': (63.5, W, 74.5, 180), 'professor': (30.5, BF + 1, 19.5, -90),
}


def xr(z):
    """the river channel's centre line"""
    return 17 + 3 * math.sin((z - 14) * 0.1)


def build():
    VIP_SHELL.clear(); CUSHIONS.clear(); COUNTERS.clear(); AUCTION_SEATS.clear(); HOLES.clear()
    rnd = random.Random(20261016)
    B = Build(SX, SY, SZ)
    S = B.set
    pick = rnd.choice
    ROCK = set()
    KEEP = set()                 # cells the town owns - clutter and stray fills leave them alone

    def rock(x, y, z):
        S(x, y, z, pick(ROCK_IN)); ROCK.add((x, y, z))

    def air(x, y, z):
        S(x, y, z, 'air'); ROCK.discard((x, y, z))

    def put(x, y, z, st):
        if not (0 <= x < SX and 0 <= y < SY and 0 <= z < SZ): return
        S(x, y, z, st); ROCK.discard((x, y, z))

    def g(x, y, z):
        return B.b.get((x, y, z), 'minecraft:air').split(':', 1)[1].split('[')[0]

    def fill(x1, y1, z1, x2, y2, z2, st):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1): put(x, y, z, st if isinstance(st, str) else pick(st))

    # ---------------------------------------------------------------- the cavern (market2's shell)
    def r_of(x, z):
        return (abs((x - CX) / RX) ** 6 + abs((z - CZ) / RZ) ** 6) ** (1 / 6)
    wrnd = random.Random(20261003)
    wob = {(x, z): math.sin(x * 0.37 + z * 0.11) * 0.6 + math.sin(z * 0.29 - x * 0.07) * 0.6 + wrnd.uniform(-0.25, 0.25) for x in range(SX) for z in range(SZ)}
    inside = {(x, z): (r_of(x, z) + wob[(x, z)] / 40 < 1.0) and not (24 <= x < 54 and z < 14) for x in range(SX) for z in range(SZ)}
    ceil = {k: min(SY - 5, int(W + 11 + 8 * (1 - min(1.0, r_of(*k)) ** 2) + wob[k])) for k, v in inside.items() if v}
    INS = lambda x, z: inside.get((x, z), False)
    near = set()
    for (x, z), ins in inside.items():
        if ins:
            for dx in range(-3, 4):
                for dz in range(-3, 4):
                    if 0 <= x + dx < SX and 0 <= z + dz < SZ: near.add((x + dx, z + dz))
    for (x, z) in near:
        for y in range(SY): rock(x, y, z)
    ROUGH = ['tuff'] * 3 + ['cobbled_deepslate'] * 2 + ['deepslate'] * 4
    for (x, z), ins in inside.items():
        if not ins: continue
        put(x, GF, z, pick(ROUGH))
        for y in range(W, ceil[(x, z)] + 1): air(x, y, z)

    def seal_room(x1, y1, z1, x2, y2, z2):
        closed = []
        for x in range(x1 - 1, x2 + 2):
            for z in range(z1 - 1, z2 + 2):
                for y in range(y1 - 1, y2 + 2):
                    if x1 <= x <= x2 and z1 <= z <= z2 and y1 <= y <= y2: continue
                    if not (0 <= x < SX and 0 <= z < SZ and 0 <= y < SY): continue
                    st = B.b.get((x, y, z))
                    if st is None or st.endswith(':air') or st.endswith(':light') or 'light[' in st:
                        S(x, y, z, ROCK_IN[(x * 7 + y * 13 + z * 31) % len(ROCK_IN)]); ROCK.add((x, y, z)); closed.append((x, y, z))
        return closed

    def carve_room(x1, y1, z1, x2, y2, z2, floor=None):
        for x in range(x1 - 3, x2 + 4):
            for z in range(z1 - 3, z2 + 4):
                if not (0 <= x < SX and 0 <= z < SZ): continue
                for y in range(max(0, y1 - 3), min(SY, y2 + 4)):
                    if (x, y, z) not in B.b: rock(x, y, z)
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1):
                if floor: put(x, y1 - 1, z, floor if isinstance(floor, str) else pick(floor))
                for y in range(y1, y2 + 1): air(x, y, z)

    def counter(cells, top=None):
        COUNTERS.extend(cells)
        axis = 'x' if len({z for _, z in cells}) == 1 else 'z'
        for (x, z) in cells: put(x, W, z, top or f'stripped_dark_oak_log[axis={axis}]')

    # ---------------------------------------------------------------- the river (curving) and the harbour basin
    QUAY = ['stone_bricks'] * 4 + ['mossy_stone_bricks'] * 2 + ['cracked_stone_bricks']
    WATER = set()

    def water_col(x, z, top):
        put(x, 2, z, pick(['gravel', 'mud', 'cobbled_deepslate']))
        for y in range(3, WATER_TOP + 1): put(x, y, z, 'water[level=0]')
        for y in range(WATER_TOP + 1, top + 1): air(x, y, z)
        WATER.add((x, z))
    for z in range(10, 84):
        c = xr(z)
        for x in range(round(c - 2.4), round(c + 2.4) + 1):
            water_col(x, z, ceil[(x, z)] if INS(x, z) else W + 4)
    for z in range(61, 77):
        for x in range(5, round(xr(z) + 2.4) + 1):
            if INS(x, z) and (x, z) not in WATER: water_col(x, z, ceil[(x, z)])
    for (x, z) in sorted(WATER):                        # chasm sides: dressed quays on the market side, raw rock on the far bank
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, z + dz)
            if n in WATER or not INS(*n): continue
            for y in range(3, GF): put(n[0], y, n[1], pick(QUAY) if (dx == 1 or n[1] >= 59) else pick(SPRING_SAFE))
            put(n[0], GF, n[1], pick(QUAY))
            KEEP.add(n)
    # the falls feeding the river from a crack in the north wall (market2's, moved to the new channel)
    fx_ = round(xr(10))
    for y in range(WATER_TOP + 1, 16): air(fx_, y, 10)
    for (dx, dz) in ((1, 0), (-1, 0)):
        for y in range(W + 5, 17): rock(fx_ + dx, y, 10 + dz)
    for (dx, dy, dz) in ((0, 0, -1), (1, 0, 0), (-1, 0, 0), (0, -1, 0), (0, 1, 0)): rock(fx_ + dx, 15 + dy, 9 + dz)
    put(fx_, 15, 9, 'water[level=0]')

    # ---------------------------------------------------------------- streets
    ROAD = set()

    def dseg(px, pz, ax, az, bx, bz):
        vx, vz = bx - ax, bz - az; L = vx * vx + vz * vz
        t = 0 if L == 0 else max(0, min(1, ((px - ax) * vx + (pz - az) * vz) / L))
        return math.hypot(px - ax - t * vx, pz - az - t * vz)

    def road(pts, w, mats, kerb='polished_deepslate'):
        for x in range(SX):
            for z in range(SZ):
                if not INS(x, z) or (x, z) in WATER: continue
                d = min(dseg(x + .5, z + .5, *pts[i], *pts[i + 1]) for i in range(len(pts) - 1)) if len(pts) > 1 else 99
                if d <= w / 2:
                    put(x, GF, z, kerb if (kerb and d > w / 2 - 1 and (x, z) not in ROAD) else pick(mats)); ROAD.add((x, z))
    LANE = ['mud_bricks'] * 6 + ['packed_mud'] * 3 + ['polished_blackstone']
    FORGE = ['cobbled_deepslate'] * 4 + ['deepslate_tiles'] * 3 + ['polished_basalt'] + ['cracked_deepslate_tiles']
    NIGHT = ['nether_bricks'] * 4 + ['blackstone'] * 3 + ['cracked_nether_bricks'] * 2 + ['red_nether_bricks']
    BOARDS = ['spruce_planks', 'spruce_planks', 'stripped_spruce_log[axis=z]']
    PAWN = [(38, 34), (36, 28), (37, 22), (38, 17), (38, 14)]
    FURN = [(47, 39), (54, 34), (60, 28), (63, 22), (63, 19)]
    NIGHT_L = [(45, 54), (50, 60), (52, 65), (56, 69), (58, 71)]
    road(PAWN, 5, LANE); road(FURN, 5, FORGE); road(NIGHT_L, 3, NIGHT, kerb=None)
    road([(27, 46), (20, 46)], 5, LANE)
    road([(31, 57), (42, 57), (42, 69), (31, 69), (31, 57)], 1, ['polished_deepslate'])
    for x in range(31, 43):
        for z in range(57, 70):
            if INS(x, z): put(x, GF, z, pick(['polished_deepslate'] * 3 + ['deepslate_tiles'] * 2 + ['polished_blackstone_bricks'])); ROAD.add((x, z))
    road([(23, 69), (31, 66)], 4, LANE); road([(42, 68), (49, 74)], 3, LANE)
    for x in range(51, 58):                                                 # the Flagon's deck
        for z in range(40, 53):
            if INS(x, z): put(x, GF, z, 'stripped_spruce_log[axis=x]' if z % 4 == 0 else 'spruce_planks'); ROAD.add((x, z))
    road([(51, 19), (62, 19)], 3, FORGE)
    road([(23, 18), (23, 41)], 3, BOARDS, kerb=None); road([(22, 49), (20, 60)], 3, BOARDS, kerb=None)
    road([(12, 46), (13, 38), (13, 31), (13, 21)], 3, QUAY, kerb=None); road([(12, 46), (10, 54), (11, 59)], 3, QUAY, kerb=None)
    road([(51, 31), (51, 38)], 2, FORGE, kerb=None)

    # ---------------------------------------------------------------- the plaza (market2's pond and falls, kept)
    for x in range(SX):
        for z in range(SZ):
            d = math.hypot(x + .5 - CX, z + .5 - CZ)
            if d < 13.2 and INS(x, z) and (x, z) not in WATER:
                put(x, GF, z, 'chiseled_polished_blackstone' if 6.6 <= d < 7.5 else 'polished_blackstone' if 11.6 <= d < 12.6 else pick(PLAZA)); ROAD.add((x, z))
    for x in range(CX - 6, CX + 7):
        for z in range(CZ - 6, CZ + 7):
            d = math.hypot(x - CX, z - CZ)
            if d < 5.2:
                put(x, 5, z, 'deepslate_tiles')
                for y in range(6, GF + 1): put(x, y, z, 'water[level=0]')
            elif d < 6.3:
                put(x, GF, z, 'polished_blackstone'); put(x, W, z, 'polished_blackstone_wall' if (x + z) % 3 else 'air')
    top = ceil[(CX, CZ)]
    for (dx, dz) in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
        for y in range(top + 1, top + 5): rock(CX + dx, y, CZ + dz)
    air(CX, top + 1, CZ); air(CX, top + 2, CZ); put(CX, top + 3, CZ, 'water[level=0]'); rock(CX, top + 4, CZ)
    for (x, z) in [(CX - 3, CZ + 2), (CX + 2, CZ - 3), (CX + 3, CZ + 3)]: put(x, W, z, 'lily_pad')

    def lamp(x, z, y=W, kind='lantern'):
        for k in range(3): put(x, y + k, z, 'polished_blackstone_wall')
        put(x, y + 3, z, f'{kind}[hanging=false,waterlogged=false]')
    for k in range(8):
        a = k * math.pi / 4 + math.pi / 8
        lx_, lz_ = round(CX + 10 * math.cos(a)), round(CZ + 10 * math.sin(a))
        if abs(lx_ - SPOTS['board'][0]) <= 3 and abs(lz_ - SPOTS['board'][1]) <= 2: continue      # (the Bounty Board stands there)
        lamp(lx_, lz_)

    def stall(x, z, face, c1, c2):
        if face in 'NS':
            cells = [(x + i, z + j) for i in (-1, 0, 1) for j in (0, 1)]; front = [(x + i, z + (0 if face == 'N' else 1)) for i in (-1, 0, 1)]
        else:
            cells = [(x + i, z + j) for i in (0, 1) for j in (-1, 0, 1)]; front = [(x + (0 if face == 'W' else 1), z + j) for j in (-1, 0, 1)]
        xs = [c[0] for c in cells]; zs = [c[1] for c in cells]
        for cx, cz in [(min(xs), min(zs)), (max(xs), min(zs)), (min(xs), max(zs)), (max(xs), max(zs))]:
            put(cx, W, cz, 'spruce_fence'); put(cx, W + 1, cz, 'spruce_fence')
        for (cx, cz) in cells:
            put(cx, W + 2, cz, f'{c1 if (cx + cz) % 2 else c2}_wool'); KEEP.add((cx, cz))
        for i, (cx, cz) in enumerate(front):
            if g(cx, W, cz) == 'air': put(cx, W, cz, ['barrel[facing=up,open=false]', 'stripped_spruce_log[axis=y]', 'barrel[facing=up,open=false]'][i])
            if i == 1: put(cx, W + 1, cz, 'lantern[hanging=false,waterlogged=false]')
    for ang, face, c1, c2 in [(20, 'S', 'red', 'white'), (68, 'N', 'yellow', 'brown'), (122, 'E', 'green', 'white'),
                              (208, 'E', 'orange', 'white'), (238, 'S', 'blue', 'white'), (296, 'S', 'red', 'black'), (336, 'W', 'lime', 'white')]:
        a = math.radians(ang)
        stall(round(CX + 15.5 * math.cos(a)), round(CZ + 15.5 * math.sin(a)), face, c1, c2)
    # the Bounty Board (its notice is a display, phase40): two posts and a board, facing south
    bx_, bz_ = SPOTS['board']
    for x in range(bx_ - 2, bx_ + 3):
        put(x, W, bz_, 'stripped_dark_oak_log[axis=x]' if x in (bx_ - 2, bx_ + 2) else 'air')
        for y in (W + 1, W + 2): put(x, y, bz_, 'dark_oak_planks' if x not in (bx_ - 2, bx_ + 2) else 'stripped_dark_oak_log[axis=y]')
        put(x, W + 3, bz_, 'dark_oak_slab[type=bottom,waterlogged=false]')
    busker = (29, 52)
    put(*busker[:1], W, busker[1], 'barrel[facing=up,open=false]') if False else put(busker[0], W, busker[1], 'barrel[facing=up,open=false]')
    put(busker[0] + 1, W, busker[1], 'spruce_slab[type=bottom,waterlogged=false]')
    for (x, z) in [(46, 39), (47, 40), (30, 39), (29, 40)]:                    # cushioned benches facing the falls
        put(x, W, z, 'dark_oak_slab[type=bottom,waterlogged=false]'); CUSHIONS.append((x, W, z, 'red'))
    for (x, z) in [(49, 43), (49, 44)]:                                        # a cheese cart
        put(x, W, z, 'honeycomb_block'); put(x, W + 1, z, 'yellow_carpet')

    # ---------------------------------------------------------------- the house generator
    PAL = {
        'alley': dict(base='cobbled_deepslate', frame='dark_oak_log', beam='stripped_dark_oak_log', fill=['calcite', 'smooth_sandstone', 'white_terracotta', 'mud_bricks'],
                      roof=['deepslate_tile', 'dark_oak', 'spruce'], floor='dark_oak_planks', stair='dark_oak'),
        'wharf': dict(base='mossy_cobblestone', frame='spruce_log', beam='stripped_spruce_log', fill=['spruce_planks', 'mangrove_planks', 'dark_oak_planks'],
                      roof=['mangrove', 'spruce', 'dark_oak'], floor='spruce_planks', stair='spruce'),
        'forge': dict(base='blackstone', frame='polished_basalt', beam='polished_basalt', fill=['bricks', 'deepslate_bricks', 'mud_bricks'],
                      roof=['blackstone', 'deepslate_tile'], floor='spruce_planks', stair='polished_blackstone_brick'),
        'tavern': dict(base='cobblestone', frame='dark_oak_log', beam='stripped_dark_oak_log', fill=['smooth_sandstone', 'calcite'], roof=['dark_oak'],
                       floor='dark_oak_planks', stair='dark_oak'),
        'night': dict(base='blackstone', frame='crimson_stem', beam='stripped_crimson_stem', fill=['nether_bricks', 'red_nether_bricks', 'crimson_planks'],
                      roof=['nether_brick', 'crimson'], floor='crimson_planks', stair='crimson'),
    }
    FULL = {'deepslate_tile': 'deepslate_tiles', 'dark_oak': 'dark_oak_planks', 'spruce': 'spruce_planks', 'mangrove': 'mangrove_planks',
            'blackstone': 'polished_blackstone', 'nether_brick': 'nether_bricks', 'crimson': 'crimson_planks', 'waxed_oxidized_cut_copper': 'waxed_oxidized_cut_copper',
            'stone_brick': 'stone_bricks', 'polished_blackstone_brick': 'polished_blackstone_bricks'}
    DIRS = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
    FACE = {'N': 'north', 'S': 'south', 'E': 'east', 'W': 'west'}
    OPP = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
    STAIR = lambda m, f, h='bottom': f'{m}_stairs[facing={f},half={h},shape=straight,waterlogged=false]'
    HOUSES = []

    def gable(x0, z0, x1, z1, yb, along, mat, fillmat, wall):
        """a gable roof over x0..x1, z0..z1 (overhang included); ridge along 'x' or 'z'; gable ends walled within `wall`. -> ridge y"""
        full = FULL[mat]; topy = yb; ax0, az0, ax1, az1 = wall
        span = (z0, z1) if along == 'x' else (x0, x1)
        for t in range(span[0], span[1] + 1):
            k = min(t - span[0], span[1] - t); y = yb + k
            if 2 * k == span[1] - span[0]: st = full
            else:
                low = t - span[0] < span[1] - t
                st = STAIR(mat, ('south' if low else 'north') if along == 'x' else ('east' if low else 'west'))
            for u in range((x0, x1)[0] if along == 'x' else z0, ((x1 if along == 'x' else z1)) + 1):
                cx, cz = (u, t) if along == 'x' else (t, u)
                if y < SY - 1: put(cx, y, cz, st); KEEP.add((cx, cz))
                ends = (ax0, ax1) if along == 'x' else (az0, az1)
                if u in ends and ((az0 <= cz <= az1) if along == 'x' else (ax0 <= cx <= ax1)):
                    for yy in range(yb, min(y, SY - 1)): put(cx, yy, cz, fillmat)
            topy = max(topy, y)
        return topy

    def house(x0, z0, x1, z1, front, storeys=2, pal='alley', style='eaves', shop=None, jetty=True, flat=False, chimney=True,
              sign=True, doorway='open', roofmat=None, fill_=None, lit=0.6, name=None):
        P = PAL[pal]; fillm = fill_ or pick(P['fill']); rm = roofmat or pick(P['roof'])
        dx, dz = DIRS[front]; fdir = FACE[front]
        HOUSES.append((x0, z0, x1, z1, front))

        def fp(s):
            a, b, c, d = x0, z0, x1, z1
            if s >= 1 and jetty:
                if front == 'E': c += 1
                if front == 'W': a -= 1
                if front == 'S': d += 1
                if front == 'N': b -= 1
            return a, b, c, d
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1): put(x, GF, z, P['base'] if (x in (x0, x1) or z in (z0, z1)) else P['floor']); KEEP.add((x, z))
        yb = GF
        for s in range(storeys):
            a, b, c, d = fp(s); fy = GF + 4 * s
            per = []
            for x in range(a, c + 1):
                for z in range(b, d + 1):
                    KEEP.add((x, z))
                    edge = x in (a, c) or z in (b, d)
                    for y in range(fy + 1, fy + 4): air(x, y, z)
                    if edge:
                        per.append((x, z))
                        ax = 'x' if z in (b, d) and x not in (a, c) else 'z' if x in (a, c) and z not in (b, d) else 'y'
                        put(x, fy + 4, z, f'{P["beam"]}[axis={ax}]' if ax != 'y' else P['frame'] + '[axis=y]')
                    else: put(x, fy + 4, z, P['floor'])
            for (x, z) in per:
                corner = x in (a, c) and z in (b, d)
                idx = (x - a) if z in (b, d) else (z - b)
                post = corner or idx % 3 == 0
                for y in range(fy + 1, fy + 4): put(x, y, z, P['frame'] + '[axis=y]' if post else fillm)
                if not post and idx % 3 == 1:
                    put(x, fy + 2, z, 'yellow_stained_glass_pane[waterlogged=false]' if rnd.random() < lit else 'glass_pane[waterlogged=false]')
            if s == 1 and jetty:                                   # the overhang's beam, and brackets under it
                a0, b0, c0, d0 = fp(0)
                for (x, z) in per:
                    if a0 <= x <= c0 and b0 <= z <= d0: continue
                    idx = (z - b) if front in 'EW' else (x - a)
                    put(x, fy, z, f'{P["beam"]}[axis={"z" if front in "EW" else "x"}]')
                    if idx % 3 == 0: put(x, fy - 1, z, STAIR(P['stair'], FACE[OPP[front]], 'top'))
            yb = fy + 4
        a, b, c, d = fp(0)
        if front in 'EW':
            fx = c if front == 'E' else a; mid = (b + d) // 2
            fcell = lambda t: (fx, t); out = lambda t, k=1: (fx + dx * k, t); lo_, hi_ = b, d
        else:
            fz = d if front == 'S' else b; mid = (a + c) // 2
            fcell = lambda t: (t, fz); out = lambda t, k=1: (t, fz + dz * k); lo_, hi_ = a, c
        if shop:
            c1, c2 = shop
            for t in (mid - 1, mid, mid + 1):
                x, z = fcell(t); air(x, W, z); air(x, W + 1, z)
                ix, iz = x - dx, z - dz
                put(ix, W, iz, f'stripped_dark_oak_log[axis={"z" if front in "EW" else "x"}]' if t == mid else 'barrel[facing=up,open=false]')
                COUNTERS.append((ix, iz))
                if not jetty or storeys == 1:
                    ox, oz = out(t); put(ox, W + 2, oz, f'spruce_trapdoor[facing={fdir},half=top,open=false,powered=false,waterlogged=false]'); put(ox, W + 3, oz, f'{c1 if t % 2 else c2}_carpet')
            x, z = fcell(mid - 1); put(x - dx, W + 1, z - dz, 'lantern[hanging=false,waterlogged=false]')
        elif doorway:
            ts = (mid,) if doorway == 'open' else (mid, mid + 1)
            for t in ts:
                x, z = fcell(t); air(x, W, z); air(x, W + 1, z)
        if sign:
            t = lo_ + 1
            k = 2 if (jetty and storeys > 1) else 1
            ox, oz = out(t, k)
            put(ox, W + 3, oz, 'dark_oak_fence'); put(ox, W + 2, oz, 'spruce_hanging_sign[attached=false,rotation=0,waterlogged=false]' if front in 'NS' else 'spruce_hanging_sign[attached=false,rotation=4,waterlogged=false]')
        if jetty and storeys > 1:                                  # lanterns hung from the overhang either side of the front
            for t in (lo_ + 2, hi_ - 2):
                if t in (mid - 1, mid, mid + 1): continue
                ox, oz = out(t); put(ox, W + 2, oz, 'lantern[hanging=true,waterlogged=false]')
        a, b, c, d = fp(storeys - 1)
        if flat:
            topy = yb + 1
        else:
            along = ('z' if front in 'EW' else 'x') if style == 'eaves' else ('x' if front in 'EW' else 'z')
            topy = gable(a - 1, b - 1, c + 1, d + 1, yb, along, rm, fillm, (a, b, c, d))
        if chimney and not flat:
            if front in 'EW': cx_, cz_ = (a + 1 if front == 'E' else c - 1), b + 1
            else: cx_, cz_ = a + 1, (b + 1 if front == 'S' else d - 1)
            cap = min(topy + 2, ceil.get((cx_, cz_), topy + 2) - 2)
            for y in range(W, cap + 1): put(cx_, y, cz_, 'bricks')
            put(cx_, cap + 1, cz_, 'campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]')
        return topy

    def spire(cx, cz, y0, r, mat, tip=None):
        full = FULL[mat]
        for k in range(r + 1):
            y = y0 + k; rr = r - k
            if y >= SY - 1: break
            for x in range(cx - rr, cx + rr + 1):
                for z in range(cz - rr, cz + rr + 1):
                    if max(abs(x - cx), abs(z - cz)) != rr: continue
                    if rr == 0: put(x, y, z, full); continue
                    f = 'east' if x == cx - rr else 'west' if x == cx + rr else 'south' if z == cz - rr else 'north'
                    put(x, y, z, STAIR(mat, f))
        if tip and y0 + r + 1 < SY - 1: put(cx, y0 + r + 1, cz, tip)

    def hang(x, z, bottom, light='lantern[hanging=true,waterlogged=false]'):
        t = ceil.get((x, z))
        if t is None or t <= bottom + 1 or g(x, bottom, z) != 'air': return
        for y in range(bottom + 1, t + 1):
            if g(x, y, z) != 'air': return
        for y in range(bottom + 1, t + 1): put(x, y, z, 'iron_chain[axis=y,waterlogged=false]')
        put(x, bottom, z, light)

    # ================================================================ PAWN ALLEY (north)
    house(27, 26, 33, 33, 'E', 2, 'alley', shop=('magenta', 'white'), jetty=False, fill_='calcite', roofmat='dark_oak')        # Madame Velour
    put(28, W, 32, 'loom[facing=east]'); put(28, W, 27, 'water_cauldron[level=3]')
    for i, col in enumerate(['white', 'pink', 'cyan', 'purple']): put(28, W, 28 + i, col + '_wool')
    house(26, 17, 32, 23, 'E', 3, 'alley', style='gable', shop=('orange', 'white'), fill_='smooth_sandstone', roofmat='deepslate_tile')  # Barnaby / the Stacks
    for (x, z) in [(27, 18), (27, 19), (28, 18)]: put(x, W, z, 'barrel[facing=up,open=false]')
    put(27, W, 22, 'anvil[facing=east]'); put(27, W, 21, 'chest[facing=east,type=single,waterlogged=false]')
    for z in range(18, 23): put(27, BF + 1, z, 'bookshelf'); put(27, BF + 2, z, 'bookshelf')
    for x in range(28, 31): put(x, BF + 1, 22, 'bookshelf'); put(x, BF + 2, 22, 'bookshelf') if x != 29 else put(x, BF + 2, 22, 'candle[candles=4,lit=true,waterlogged=false]')
    put(29, BF + 1, 18, 'lectern[facing=south,has_book=false,powered=false]')
    for z in (19, 20): air(33, BF + 1, z); air(33, BF + 2, z)               # the Stacks' door onto the rope bridge
    for z in (18, 19, 20): put(31, BF + 1, z, 'stripped_dark_oak_log[axis=z]')   # the Professor's desk (2.81a: his back-room book lies on it)
    for z in (18, 21): put(33, BF + 1, z, 'dark_oak_log[axis=y]')
    # the Stacks' tower, on the quay behind
    for y in range(W, 24):
        for x in range(22, 26):
            for z in range(14, 18):
                if x in (22, 25) or z in (14, 17):
                    put(x, y, z, 'dark_oak_log[axis=y]' if (x in (22, 25) and z in (14, 17)) else
                        ('yellow_stained_glass_pane[waterlogged=false]' if y % 4 == 1 and (x + z) % 2 else 'smooth_sandstone'))
                else: air(x, y, z)
                KEEP.add((x, z))
    gable(21, 13, 26, 18, 24, 'x', 'deepslate_tile', 'smooth_sandstone', (22, 14, 25, 17))
    # THE FENCE: flat-roofed, a terrace on top (walk y18) with the Gilded Gutter's gate
    house(43, 15, 50, 22, 'W', 2, 'alley', shop=('red', 'yellow'), flat=True, fill_='mud_bricks', sign=True)
    for (x, y) in [(49, W), (48, W), (49, W + 1)]: put(x, y, 16, 'gold_block')
    put(48, W, 21, 'chest[facing=west,type=single,waterlogged=false]'); put(49, W, 19, 'barrel[facing=up,open=false]'); put(49, W, 20, 'barrel[facing=up,open=false]')
    for x in range(42, 53):                                                 # the terrace floor (y17), and its landing over the stair
        for z in range(15, 23):
            if x <= 50 or z >= 21: put(x, BF, z, 'spruce_planks' if (x + z) % 4 else 'stripped_spruce_log[axis=x]'); KEEP.add((x, z))
    for (x, z) in [(51, 20), (52, 20)]: put(x, BF, z, 'spruce_planks')
    rail = [(x, 15) for x in range(42, 51) if not 44 <= x <= 48] + [(42, z) for z in range(15, 23) if z not in (19, 20)] + [(x, 23) for x in range(42, 51)] + \
           [(51, z) for z in range(15, 20)] + [(53, z) for z in range(20, 23)] + [(52, 19), (53, 19)]
    for (x, z) in rail: put(x, BF + 1, z, 'dark_oak_fence')
    for (x, z) in [(43, 16), (50, 16), (43, 22), (50, 22)]: put(x, BF + 1, z, 'lantern[hanging=false,waterlogged=false]')
    for (x, z) in [(45, 16), (47, 16), (46, 17)]: put(x, BF + 1, z, 'red_carpet')
    for x in (51, 52):                                                      # the outside stair up to the terrace (east of the Fence)
        for k, z in enumerate(range(30, 22, -1)):
            y = W + k
            for yy in range(GF, y): put(x, yy, z, 'spruce_planks')
            put(x, y, z, STAIR('spruce', 'north'))
            for yy in range(y + 1, y + 4):
                if yy < BF: air(x, yy, z)
            KEEP.add((x, z))
        for z in range(20, 23):
            for yy in range(GF, BF): put(x, yy, z, 'spruce_log[axis=y]' if z == 21 else 'air')
    for z in range(23, 31): put(53, W + (30 - z) + 1, z, 'spruce_fence') if z < 30 else None
    # the rope bridge: the Stacks -> the Fence's terrace (walk y18)
    for x in range(34, 42):
        for z in (19, 20): put(x, BF, z, 'spruce_slab[type=top,waterlogged=false]')
        put(x, BF + 1, 18, 'spruce_fence' if x % 3 == 1 else 'iron_chain[axis=x,waterlogged=false]')
        put(x, BF + 1, 21, 'spruce_fence' if x % 3 == 1 else 'iron_chain[axis=x,waterlogged=false]')
        KEEP.add((x, 19)); KEEP.add((x, 20))
    house(43, 24, 48, 29, 'W', 2, 'alley', style='gable', fill_='white_terracotta', roofmat='spruce', doorway='door', sign=False)   # lodgings
    # the Dark Auction's gate (market2's, kept exactly: the gate ledgers stand where they always did)
    for x in range(35, 40):
        for z in range(14, 16): put(x, GF, z, 'polished_blackstone_bricks' if (x + z) % 2 else 'polished_blackstone')
    for z in range(15, 17): put(37, W, z, 'red_carpet')
    for y in range(W, W + 5):
        for x in (34, 40): put(x, y, 14, 'chiseled_polished_blackstone')
    for x in range(35, 40):
        for y in range(W, W + 4): put(x, y, 14, 'iron_bars')
        put(x, W + 4, 14, 'gold_block')
    for x in range(33, 42): put(x, W + 5, 14, 'polished_blackstone_bricks')
    for x in (34, 40): put(x, W + 5, 13, 'gilded_blackstone') if False else None
    B.sign(37, W + 4, 15, 'dark_oak_wall_sign[facing=south,waterlogged=false]', ['THE DARK', 'AUCTION', 'Next sale:', 'soon.'], color='yellow', glow=True)
    for x in (33, 41): put(x, W, 15, 'polished_blackstone_wall'); put(x, W + 1, 15, 'lantern[hanging=false,waterlogged=false]')
    # rooms behind the north wall (market2's: the Auction Hall and the Gilded Gutter)
    carve_room(30, W, 2, 44, W + 5, 12, floor='dark_oak_planks')
    for x in range(35, 40):
        for z in (12, 13):
            put(x, GF, z, 'polished_blackstone')
            for y in range(W, W + 4): air(x, y, z)
    for r in range(3):
        zs, zw = 6 + 2 * r, 7 + 2 * r
        for x in range(31, 44):
            if 36 <= x <= 38: continue
            for z in (zs, zw):
                for y in range(W, W + r): put(x, y, z, 'dark_oak_planks')
                if r: put(x, W + r - 1, z, 'dark_oak_slab[type=double,waterlogged=false]' if z == zs else 'dark_oak_planks')
            AUCTION_SEATS.append((x, W + r, zs))
    for x in range(34, 41): put(x, W, 3, 'polished_blackstone_bricks'); put(x, W, 4, 'red_carpet')
    put(37, W + 1, 3, 'polished_blackstone_brick_wall'); put(37, W + 3, 3, 'end_rod[facing=down]')
    put(37, W + 5, 7, 'lantern[hanging=true,waterlogged=false]')
    carve_room(49, BF + 1, 2, 62, BF + 5, 12, floor='dark_oak_planks')
    VIP_SHELL.extend(seal_room(49, BF + 1, 2, 62, BF + 5, 12))
    for x in range(43, 52):
        for z in range(8, 15):
            for y in range(BF - 1, BF + 6):
                if (x, y, z) not in B.b: rock(x, y, z)
    for x in range(45, 48):
        for z in range(10, 15): put(x, BF, z, 'dark_oak_planks'); [air(x, y, z) for y in range(BF + 1, BF + 4)]
    for x in range(48, 50):
        for z in range(10, 13): put(x, BF, z, 'dark_oak_planks'); [air(x, y, z) for y in range(BF + 1, BF + 4)]
    for x in range(50, 62):
        for z in range(3, 12): put(x, BF + 1, z, 'red_carpet' if (x + z) % 6 else 'black_carpet')
    for z in range(3, 12): put(61, BF + 1, z, 'bookshelf'); put(61, BF + 2, z, 'bookshelf')
    put(55, BF + 1, 3, 'campfire[facing=south,lit=true,signal_fire=false,waterlogged=false]')
    for x in (54, 56): put(x, BF + 1, 3, 'bricks'); put(x, BF + 2, 3, 'bricks')
    put(55, BF + 2, 3, 'bricks')
    for (x, z) in [(52, 7), (58, 7)]: put(x, BF + 1, z, 'gold_block'); put(x, BF + 2, z, 'candle[candles=3,lit=true,waterlogged=false]')
    put(55, BF + 4, 7, 'lantern[hanging=true,waterlogged=false]')
    # the Gilded Gutter's gate, off the Fence's terrace
    for y in range(BF + 1, BF + 6):
        for x in (44, 48): put(x, y, 14, 'gold_block' if y == BF + 5 else 'chiseled_polished_blackstone')
    for x in range(45, 48):
        for y in range(BF + 1, BF + 4): put(x, y, 14, 'iron_bars')
        put(x, BF + 4, 14, 'gold_block'); put(x, BF + 5, 14, 'gold_block')
    # the clock tower
    for y in range(W, 24):
        for x in range(44, 49):
            for z in range(31, 36):
                KEEP.add((x, z))
                if x in (44, 48) or z in (31, 35):
                    put(x, y, z, 'polished_deepslate' if (x in (44, 48) and z in (31, 35)) or y in (13, 17) else 'stone_bricks')
                else: air(x, y, z)
    for (ax, az, xs, zs) in [(46, 30, (45, 47), (30, 30)), (46, 36, (45, 47), (36, 36)), (43, 33, (43, 43), (32, 34)), (49, 33, (49, 49), (32, 34))]:
        fill(xs[0], 19, zs[0], xs[1], 21, zs[1], 'smooth_quartz'); put(ax, 20, az, 'black_concrete'); put(ax, 21, az, 'gold_block')
    for y in (22, 23):
        for (x, z) in [(45, 31), (46, 31), (47, 31), (45, 35), (46, 35), (47, 35), (44, 32), (44, 33), (44, 34), (48, 32), (48, 33), (48, 34)]: air(x, y, z)
    put(46, 23, 33, 'bell[attachment=ceiling,facing=north,powered=false]')
    # (2.82) parkoured up and dropped in, nobody is stuck: hay to land on, a ladder up the inside, and a door out at the foot
    fill(45, GF, 32, 47, GF, 34, 'hay_block[axis=y]')
    for y in range(W, 22): put(46, y, 34, 'ladder[facing=north,waterlogged=false]')      # (to the belfry's sill: above it the wall behind is open)
    put(46, W, 31, 'dark_oak_door[facing=north,half=lower,hinge=left,open=false,powered=false]')
    put(46, W + 1, 31, 'dark_oak_door[facing=north,half=upper,hinge=left,open=false,powered=false]')
    spire(46, 33, 24, 3, 'waxed_oxidized_cut_copper')
    for y in range(24, 27): put(46, y, 33, 'waxed_oxidized_cut_copper')        # (from y 24: the bell hangs from it)
    put(46, 27, 33, 'lightning_rod[facing=up,powered=false,waterlogged=false]')
    put(46, W, 30, 'air'); put(46, W + 1, 30, 'air') if False else None

    # ================================================================ FURNACE ROW (north-east)
    house(53, 21, 59, 28, 'E', 2, 'forge', shop=('gray', 'black'), jetty=False, fill_='bricks', roofmat='blackstone')                   # Vinny
    put(54, W, 22, 'grindstone[face=floor,facing=east]'); put(54, W, 26, 'anvil[facing=north]'); put(54, W, 27, 'smithing_table')
    house(64, 27, 71, 34, 'W', 2, 'forge', shop=('light_gray', 'cyan'), fill_='deepslate_bricks', roofmat='deepslate_tile')            # Steelwhisker
    for z in (28, 33): put(70, W, z, 'iron_block')
    put(70, W, 30, 'anvil[facing=east]'); put(70, W, 31, 'blast_furnace[facing=west,lit=true]')
    put(62, W, 33, 'grindstone[face=floor,facing=east]'); put(61, W, 35, 'anvil[facing=east]')
    # THE FORGE PIT: an open smithy hall - the lava channel behind bars, the great chimney, steam vents
    for x in range(58, 72):
        for z in range(12, 23):
            if INS(x, z): put(x, GF, z, pick(FORGE)); KEEP.add((x, z))
    for x in range(60, 70):
        for z in range(13, 16):
            if INS(x, z): put(x, GF - 1, z, 'magma_block'); put(x, GF, z, 'lava[level=0]')
        if INS(x, 16): put(x, W, 16, 'iron_bars'); put(x, W + 1, 16, 'iron_bars')
    for (x, z) in [(59, 21), (62, 21), (66, 21), (70, 21), (59, 17), (70, 17)]:
        if INS(x, z): fill(x, W, z, x, 15, z, 'polished_blackstone')
    gable(58, 12, 71, 22, 16, 'x', 'deepslate_tile', 'polished_blackstone', (59, 13, 70, 21))
    for x in range(58, 72):
        for z in range(13, 22):
            for y in range(W, 16):
                if (x, y, z) in ROCK and INS(x, z): air(x, y, z)
    for y in range(W, ceil[(66, 14)] + 1):
        for x in range(65, 68):
            for z in range(12, 15): put(x, y, z, 'polished_blackstone' if y % 5 == 0 else 'bricks')
    put(66, W, 15, 'air'); put(66, GF, 15, 'lava[level=0]')
    for (x, z, b) in [(61, 18, 'anvil[facing=east]'), (63, 18, 'blast_furnace[facing=south,lit=true]'), (64, 18, 'blast_furnace[facing=south,lit=true]'),
                      (67, 19, 'lava_cauldron'), (68, 19, 'smithing_table'), (69, 18, 'anvil[facing=north]')]:
        put(x, W, z, b)
    for (x, z) in [(61, 20), (65, 20), (68, 21)]:
        put(x, GF - 1, z, 'magma_block'); put(x, GF, z, 'iron_trapdoor[facing=north,half=top,open=false,powered=false,waterlogged=false]')
    B.sign(62, W + 2, 21, 'dark_oak_wall_sign[facing=south,waterlogged=false]', ['DANGER', 'HOT FLOOR', 'Mind the vents.', '- mgmt'], color='red', glow=True)
    # CURIO COURT: Fishy's Cabinet door (dug at run time, phase145) and display plinths
    for x in range(52, 60):
        for z in range(11, 19):
            if INS(x, z): put(x, GF, z, 'polished_deepslate' if (x + z) % 2 else 'deepslate_tiles'); ROAD.add((x, z)); KEEP.add((x, z))
    for (x, z) in [(52, 13), (52, 15), (59, 13), (59, 15)]:
        if INS(x, z): put(x, W, z, 'polished_blackstone_wall'); put(x, W + 1, z, 'lantern[hanging=false,waterlogged=false]')

    # ================================================================ THE GNAWED FLAGON (east)
    house(59, 39, 71, 52, 'W', 2, 'tavern', jetty=True, fill_='smooth_sandstone', roofmat='dark_oak', lit=0.95, doorway='wide')
    counter([(67, z) for z in range(41, 51)])
    for z in range(40, 52): put(70, W, z, 'smoker[facing=west,lit=true]' if z % 4 == 1 else 'barrel[facing=west,open=false]')
    for (x, z) in [(70, 42), (70, 46)]: put(x, W + 1, z, 'honeycomb_block')          # (2.81a: on the back bar - nothing stands on the counter)
    for (cx, cz) in [(61, 41), (61, 48), (64, 50), (62, 44)]:
        put(cx, W, cz, 'dark_oak_fence'); put(cx, W + 1, cz, 'dark_oak_pressure_plate[powered=false]')
        for (sx, sz) in ((cx - 1, cz), (cx + 1, cz)):
            put(sx, W, sz, 'spruce_slab[type=bottom,waterlogged=false]'); CUSHIONS.append((sx, W, sz, 'brown'))
    for z in range(41, 52, 3):                                              # tables on the deck
        put(54, W, z, 'spruce_fence'); put(54, W + 1, z, 'spruce_pressure_plate[powered=false]')
        for (sx, f) in ((53, 'east'), (55, 'west')): put(sx, W, z, STAIR('spruce', f)); CUSHIONS.append((sx, W, z, 'orange'))
    for x in range(52, 57, 2): put(x, W, 52, 'barrel[facing=up,open=false]')

    # ================================================================ NIGHT ALLEY (south-east)
    house(53, 55, 59, 62, 'W', 2, 'night', fill_='nether_bricks', roofmat='nether_brick', lit=0.0, doorway='door', sign=False)
    house(44, 59, 48, 65, 'E', 2, 'night', style='gable', fill_='red_nether_bricks', roofmat='crimson', lit=0.0, doorway='door', sign=False)
    for z in range(56, 62, 2): put(53, W + 2, z, 'red_stained_glass_pane[waterlogged=false]')
    for z in range(60, 65, 2): put(48, W + 2, z, 'red_stained_glass_pane[waterlogged=false]')
    # Cecil's tent (a purple fortune teller's tent, open to the lane)
    for x in range(51, 55):
        for z in range(69, 73):
            put(x, GF, z, 'black_carpet') if False else None
            put(x, W + 4, z, ('purple' if (x + z) % 2 else 'black') + '_wool'); KEEP.add((x, z))
    for (x, z) in [(51, 69), (54, 69), (51, 72), (54, 72)]:
        for y in range(W, W + 4): put(x, y, z, 'dark_oak_fence')
    for z in range(69, 73):
        for y in range(W, W + 4): put(51, y, z, 'purple_wool')
    for x in range(52, 54):
        for y in range(W, W + 4): put(x, y, 69, 'purple_wool'); put(x, y, 72, 'purple_wool')
    put(52, W, 72, 'candle[candles=2,lit=true,waterlogged=false]') if False else None
    # THE BLOOD ALCOVE: a squat crimson keep, corner turrets with spires, a gatehouse with the raised portcullis
    for x in range(59, 70):
        for z in range(66, 78):
            KEEP.add((x, z))
            edge = x in (59, 69) or z in (66, 77)
            put(x, GF, z, 'red_nether_bricks' if (x * 3 + z) % 5 else 'nether_bricks')
            for y in range(W, 17): put(x, y, z, ('red_nether_bricks' if y == 16 else 'nether_bricks') if edge else 'air')
            put(x, 17, z, 'red_nether_bricks' if edge else 'nether_brick_slab[type=bottom,waterlogged=false]')
            if edge and (x + z) % 2 == 0: put(x, 18, z, 'red_nether_bricks')
    for (cx, cz) in [(59, 66), (69, 66), (59, 77), (69, 77)]:
        for x in range(cx - 1, cx + 2):
            for z in range(cz - 1, cz + 2):
                for y in range(W, 20): put(x, y, z, 'red_nether_bricks' if y in (16, 19) else 'nether_bricks')
                KEEP.add((x, z))
        spire(cx, cz, 20, 2, 'nether_brick', tip='soul_lantern[hanging=false,waterlogged=false]')
    for z in range(68, 75):                                                 # the gatehouse
        for y in range(W, 19): put(58, y, z, 'red_nether_bricks' if y in (16, 18) else 'nether_bricks')
        if z % 2 == 0: put(58, 19, z, 'red_nether_bricks')
        KEEP.add((58, z))
    for z in range(70, 73):
        for x in (58, 59):
            for y in range(W, W + 4): air(x, y, z)
            put(x, W + 4, z, 'iron_bars'); put(x, W + 5, z, 'iron_bars')
    counter([(x, 73) for x in range(60, 68)], top='red_nether_bricks')
    for (x, st) in [(60, 'crying_obsidian'), (62, 'chest[facing=north,type=single,waterlogged=false]'), (64, 'crying_obsidian'),
                    (65, 'brewing_stand[has_bottle_0=true,has_bottle_1=false,has_bottle_2=true]'), (67, 'crying_obsidian')]:
        put(x, W, 76, st)
    for (x, z) in [(61, 68), (66, 69), (63, 70)]:
        for y in range(W + 4, W + 7): put(x, y, z, 'iron_chain[axis=y,waterlogged=false]')
        put(x, W + 3, z, 'iron_bars'); put(x, W + 2, z, 'soul_lantern[hanging=true,waterlogged=false]')
    for (x, z) in [(61, 71), (64, 69), (66, 71)]: put(x, W, z, 'redstone_wire[east=none,north=none,power=0,south=none,west=none]')
    for (x, z) in [(60, 75), (68, 75)]:
        for y in range(W, W + 4): put(x, y, z, 'crimson_stem[axis=y]')
        put(x, W + 4, z, 'shroomlight')
    for x in (61, 66): put(x, W, 67, 'red_candle[candles=3,lit=true,waterlogged=false]')
    B.sign(57, W + 2, 69, 'crimson_wall_sign[facing=west,waterlogged=false]', ['THE', 'BLOODBROKER', 'Crystals bought', '& sold'], color='red', glow=True)
    for (x, z) in [(52, 60), (49, 64), (55, 67), (57, 64)]: hang(x, z, W + 4, 'soul_lantern[hanging=true,waterlogged=false]')

    # ================================================================ THE LOOKOUT, the arcade, the stair, the hoist, the arrival square
    TER = set()
    for x in range(28, 49):
        for z in range(68, 82):
            if ((x + .5 - 38) / 10.5) ** 2 + ((z + .5 - 81) / 11) ** 2 <= 1 or (35 <= x <= 41 and z >= 79): TER.add((x, z))
    for (x, z) in TER:
        KEEP.add((x, z))
        solid = z >= 74
        for y in range(W, BF):
            put(x, y, z, pick(['deepslate', 'tuff', 'cobbled_deepslate', 'deepslate']) if solid else 'air')
        if solid: put(x, GF, z, 'polished_deepslate')
        else: put(x, GF, z, pick(['polished_deepslate', 'deepslate_tiles'])); ROAD.add((x, z))
        put(x, BF, z, pick(['polished_deepslate', 'deepslate_tiles', 'polished_deepslate']))
        for y in range(BF + 1, BF + 6):
            if g(x, y, z) not in ('air',): air(x, y, z)
    rim = [(x, z) for (x, z) in TER if any((x + a, z + b) not in TER and INS(x + a, z + b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for (x, z) in rim:
        put(x, BF + 1, z, 'deepslate_brick_wall')
        put(x, BF, z, 'polished_deepslate')
        if z < 74 and (x % 4 == 2):                                             # pillars carry the terrace's front
            for y in range(W, BF): put(x, y, z, 'polished_deepslate')
        elif z >= 74 and z <= 76:
            for y in range(W, BF): put(x, y, z, 'deepslate_bricks' if (x * 3 + y * 7 + z) % 9 else 'cracked_deepslate_bricks')
    for (x, z) in rim:                                                     # the parapet opens onto the curling stair and the hoist
        if (x <= 30 and 76 <= z <= 78) or (x >= 46 and 75 <= z <= 77): air(x, BF + 1, z)
    for x in range(29, 48):                                                # the arcade's back wall (z74): the two rooms open off it
        if (x, 74) in TER:
            for y in range(W, BF): put(x, y, 74, 'deepslate_bricks' if (x * 3 + y * 7) % 9 else 'cracked_deepslate_bricks')
    for x in (32, 33, 42, 43):
        for y in range(W, W + 3): air(x, y, 74)
    for (x, z) in TER:
        if z < 74 and (x, z) not in rim and x % 4 == 0 and z % 3 == 1: put(x, BF - 1, z, 'lantern[hanging=true,waterlogged=false]')
    for (x, z) in [(31, 76), (45, 76), (38, 72), (34, 73), (42, 73)]:
        if (x, z) in TER and (x, z) not in rim: put(x, BF + 1, z, 'lantern[hanging=false,waterlogged=false]')
    for (x, z) in [(30, 77), (46, 77)]:
        put(x, BF + 1, z, 'moss_block'); put(x, BF + 2, z, 'flowering_azalea')
    for (x, z) in [(33, 76), (43, 76)]:
        put(x, BF + 1, z, 'dark_oak_slab[type=bottom,waterlogged=false]'); CUSHIONS.append((x, BF + 1, z, 'purple'))
    for (x, z) in rim:
        if z < 74 and x % 4 == 0 and (x, z - 1) not in TER and INS(x, z - 1):
            put(x, BF - 1, z - 1, 'red_wall_banner[facing=north]'); put(x, BF - 2, z - 1, 'air')
    # the vault door, its frame, the vestibule and the dig-in tunnel (market2's, kept exactly)
    for x in range(35, 42):
        for y in range(BF, BF + 6):
            for z in (82, 83): put(x, y, z, 'chiseled_deepslate')
    for x in range(35, 42):
        for z in range(79, 82):
            for y in range(BF + 1, BF + 6): air(x, y, z)
    vx1, vz1, vx2, vz2 = 33, 84, 43, 90
    for x in range(vx1 - 1, vx2 + 2):
        for z in range(vz1 - 1, vz2 + 2):
            for y in range(BF - 2, BF + 7): rock(x, y, z)
    for x in range(vx1, vx2 + 1):
        for z in range(vz1, vz2 + 1):
            put(x, BF, z, 'cobbled_deepslate')
            for y in range(BF + 1, BF + 6): air(x, y, z)
    for x in range(37, 40):
        for y in range(BF + 1, BF + 4): put(x, y, 82, 'iron_block'); air(x, y, 83)
        put(x, BF, 83, 'cobbled_deepslate')
    for z in range(vz2 + 1, SZ):
        for x in range(36, 41):
            for y in range(BF - 1, BF + 6): rock(x, y, z)
        for x in range(37, 40):
            put(x, BF, z, 'cobbled_deepslate')
            for y in range(BF + 1, BF + 4): air(x, y, z)
    put(vx1, BF + 4, 87, 'soul_lantern[hanging=true,waterlogged=false]'); put(vx2, BF + 4, 87, 'soul_lantern[hanging=true,waterlogged=false]')
    put(vx1, BF + 1, 89, 'cobweb'); put(vx2, BF + 3, 89, 'cobweb'); put(vx2, BF + 1, 85, 'skeleton_skull[powered=false,rotation=6]')
    for z in range(91, SZ, 3): put(38, BF + 3, z, 'soul_lantern[hanging=true,waterlogged=false]')
    B.sign(35, BF + 2, 84, 'dark_oak_wall_sign[facing=south,waterlogged=false]', ['THE BLACK', 'MARKET', 'Members only.', 'Carry your key.'], color='yellow', glow=True)
    B.sign(41, BF + 2, 84, 'dark_oak_wall_sign[facing=south,waterlogged=false]', ['Under new', 'management.', 'Rats welcome.', 'Cats NOT.'], color='white', glow=True)
    # the curling stair (west): down west from the terrace, a landing, down north to the street
    SB = 'stone_bricks'
    for i, x in enumerate(range(27, 24, -1)):                            # walk 17, 16, 15
        y = BF - 1 - i
        for z in range(76, 79):
            fill(x, GF, z, x, y - 1, z, SB); put(x, y, z, STAIR('stone_brick', 'east'))
            for yy in range(y + 1, y + 4): air(x, yy, z)
            KEEP.add((x, z))
        put(x, y + 1, 75, 'stone_brick_wall'); put(x, y + 1, 79, 'stone_brick_wall')
    for x in range(21, 25):                                               # the landing (walk 14)
        for z in range(75, 79):
            fill(x, GF, z, x, BF - 4, z, SB); put(x, BF - 4, z, 'polished_andesite')
            for yy in range(BF - 3, BF + 1): air(x, yy, z)
            KEEP.add((x, z))
    for z in range(75, 79): put(20, BF - 3, z, 'stone_brick_wall')
    for x in range(21, 25): put(x, BF - 3, 79, 'stone_brick_wall')
    put(20, BF - 2, 75, 'lantern[hanging=false,waterlogged=false]'); put(20, BF - 2, 78, 'lantern[hanging=false,waterlogged=false]')
    for k, z in enumerate(range(74, 70, -1)):                             # walk 13, 12, 11, 10
        y = BF - 5 - k
        for x in range(22, 25):
            fill(x, GF, z, x, y - 1, z, SB); put(x, y, z, STAIR('stone_brick', 'south'))
            for yy in range(y + 1, y + 4): air(x, yy, z)
            KEEP.add((x, z))
        put(21, y + 1, z, 'stone_brick_wall')
    # the hoist (east): a timber tower with a ladder, from the street up to the terrace
    for (x, z) in [(48, 75), (50, 75), (48, 77), (50, 77)]:
        for y in range(W, 23): put(x, y, z, 'stripped_spruce_log[axis=y]')
    for y in range(W, 23):
        put(49, y, 77, 'spruce_planks'); put(49, y, 76, 'ladder[facing=north,waterlogged=false]' if y <= BF + 1 else 'air')
        put(48, y, 76, 'spruce_planks' if not (BF + 1 <= y <= BF + 2) else 'air'); put(50, y, 76, 'spruce_planks')
        put(49, y, 75, 'air' if y <= W + 1 else 'spruce_planks')
    fill(48, 23, 75, 50, 23, 77, 'spruce_planks'); put(49, 24, 76, 'spruce_slab[type=bottom,waterlogged=false]')
    put(49, GF, 76, 'spruce_planks'); put(49, W - 1, 75, 'spruce_planks')
    for y in (BF + 1, BF + 2): air(47, y, 76)
    put(47, BF, 76, 'spruce_planks'); KEEP.update({(48, 75), (49, 75), (50, 75), (48, 76), (49, 76), (50, 76), (48, 77), (49, 77), (50, 77), (47, 76)})
    # the gate arch over the street into the plaza, the map board, signposts
    for x in (33, 43):
        fill(x, W, 59, x, W + 5, 60, 'polished_blackstone_bricks'); put(x, W + 6, 59, 'gilded_blackstone'); put(x, W + 6, 60, 'gilded_blackstone')
    fill(34, W + 5, 59, 42, W + 5, 60, 'polished_blackstone_bricks'); fill(35, W + 6, 59, 41, W + 6, 60, 'polished_blackstone_brick_slab[type=bottom,waterlogged=false]')
    fill(36, W + 4, 59, 40, W + 4, 59, 'dark_oak_planks'); put(38, W + 4, 60, 'gold_block')
    for x in (35, 41): put(x, W + 4, 60, 'lantern[hanging=true,waterlogged=false]')
    put(36, W, 64, 'dark_oak_fence'); fill(35, W + 1, 64, 37, W + 2, 64, 'dark_oak_planks')
    B.sign(36, W + 1, 65, 'dark_oak_wall_sign[facing=south,waterlogged=false]', ['THE MARKET', 'N: Pawn Alley', 'E: Flagon, Forge', 'W: Wharf, Lucky'], color='yellow', glow=True)
    for (x, z, lines) in [(40, 64, ['<- WHARF', 'PLAZA ^', 'NIGHT ALLEY ->', '']), (27, 48, ['WHARF <-', '', '-> PLAZA', '']), (47, 37, ['FURNACE ROW', '-> ', '', '']),
                          (44, 53, ['NIGHT ALLEY', '->', '', '']), (39, 33, ['PAWN ALLEY', '^', 'Dark Auction', ''])]:
        put(x, W, z, 'spruce_fence')
        B.sign(x, W + 1, z, 'spruce_sign[rotation=8,waterlogged=false]', lines, color='white', glow=True)

    # ================================================================ THE WHARF (west)
    # the stone bridge (Bridge Street to the far bank), humped in the middle
    for x in range(12, 22):
        hump = 1 if 15 <= x <= 19 else 0
        for z in range(44, 49):
            put(x, GF + hump, z, 'polished_blackstone_bricks')
            if hump: put(x, GF, z, 'polished_blackstone_bricks') if (x, z) not in WATER else None
            if hump and x in (15, 19): put(x, GF + 1, z, STAIR('polished_blackstone_brick', 'east' if x == 15 else 'west'))
            if (x, z) in WATER and 15 <= x <= 19:
                put(x, GF, z, 'polished_blackstone_bricks'); put(x, GF - 1, z, STAIR('polished_blackstone_brick', 'south' if z == 44 else 'north', 'top') if z in (44, 48) else 'polished_blackstone_bricks')
            KEEP.add((x, z))
        put(x, GF + hump + 1, 44, 'polished_blackstone_brick_wall'); put(x, GF + hump + 1, 48, 'polished_blackstone_brick_wall')
    for z in range(44, 49):
        for x in (15, 19):
            for zz in (45, 46, 47): air(x, GF + 2, zz)
    for (x, z) in [(12, 44), (12, 48), (21, 44), (21, 48)]:
        put(x, W, z, 'polished_blackstone_bricks'); put(x, W + 1, z, 'polished_blackstone_wall'); put(x, W + 2, z, 'lantern[hanging=false,waterlogged=false]')
    # THE DROP: rickety planks over the river (north), gaps and a chain for a rail
    for x in range(13, 24):
        if (x, 31) in WATER or (x, 32) in WATER:
            for z in (31, 32):
                if (x, z) in ((19, 31), (20, 32), (17, 32)): air(x, GF, z); continue
                put(x, GF, z, 'spruce_slab[type=top,waterlogged=false]'); KEEP.add((x, z))
    B.sign(24, W, 30, 'spruce_sign[rotation=4,waterlogged=false]', ['MIND THE', 'GAP', '(the river', 'is cold)'], color='red')
    # stilt docks off the east quay
    for (z0, z1) in [(22, 26), (52, 56)]:
        for z in range(z0, z1 + 1):
            e = round(xr(z) + 2.4)
            for x in range(e - 2, e + 1):
                put(x, GF, z, 'spruce_planks'); KEEP.add((x, z))
                if (x + z) % 3 == 0: fill(x, 2, z, x, GF - 1, z, 'stripped_spruce_log[axis=y]')
        for z in (z0, z1):
            e = round(xr(z) + 2.4); put(e - 2, W, z, 'spruce_fence'); put(e - 2, W + 1, z, 'lantern[hanging=false,waterlogged=false]')
    # the crane: a timber tower on the quay, its jib over the river, a crate on the hook
    for y in range(W, 21):
        for (x, z) in [(23, 41), (24, 41), (23, 42), (24, 42)]: put(x, y, z, 'stripped_spruce_log[axis=y]' if (x + z) % 2 else 'spruce_log[axis=y]')
    for x in range(16, 26): put(x, 21, 41, 'spruce_log[axis=x]')
    put(25, 20, 41, 'barrel[facing=up,open=false]'); put(25, 19, 41, 'barrel[facing=up,open=false]')
    for y in range(14, 21): put(17, y, 41, 'iron_chain[axis=y,waterlogged=false]')
    put(17, 13, 41, 'barrel[facing=up,open=false]')
    KEEP.update({(23, 41), (24, 41), (23, 42), (24, 42), (25, 41)})
    house(22, 50, 28, 57, 'W', 2, 'wharf', jetty=True, fill_='mangrove_planks', roofmat='spruce', doorway='door', sign=True)            # fish market
    for z in range(51, 57, 2): put(20, W, z, 'barrel[facing=up,open=false]')
    # the far bank: Cheddarbeard's dock house (Salty Sal's counter; the mouse hole into Rat Gang HQ in its back wall)
    house(2, 22, 11, 30, 'E', 2, 'wharf', shop=('blue', 'white'), jetty=True, fill_='spruce_planks', roofmat='spruce', chimney=False)
    put(3, W, 29, 'barrel[facing=up,open=false]'); put(3, W + 1, 29, 'barrel[facing=up,open=false]'); put(8, W, 29, 'gold_block')
    put(3, W, 27, 'chest[facing=east,type=single,waterlogged=false]'); put(7, W, 23, 'water_cauldron[level=3]')
    for z in range(25, 28):                                                  # his jetty, out over the river
        for x in range(12, round(xr(z) - 2.4) + 2): put(x, GF, z, 'spruce_planks'); KEEP.add((x, z))
    house(2, 33, 11, 42, 'E', 1, 'wharf', style='gable', jetty=False, fill_='dark_oak_planks', roofmat='mangrove', chimney=False, doorway='door', sign=False)
    # RAT GANG HQ (market2's): a den behind the dock house, reached only through the mouse hole
    carve_room(1, W, 12, 6, W + 3, 19, floor='dark_oak_planks')
    for z in range(11, 22):
        for y in range(W, W + 5): rock(0, y, z); rock(7, y, z)
    for x in range(0, 8):
        for y in range(W, W + 5): rock(x, y, 11)
        for z in range(11, 22): rock(x, W + 4, z)
    for x in range(1, 7):
        for z in range(20, 22):
            for y in range(W, W + 4): rock(x, y, z)
    for z in (20, 21, 22): put(4, W, z, 'deepslate_brick_slab[type=top,waterlogged=false]')
    put(4, W + 1, 22, 'spruce_planks')
    counter([(x, 18) for x in (2, 3, 4)])                                       # the Captain's counter (2.81a: his back-room book lies on it)
    put(1, W, 13, 'gold_block'); put(2, W, 13, 'gold_block'); put(1, W + 1, 13, 'gold_block'); put(1, W, 14, 'raw_gold_block')
    put(1, W, 16, 'chest[facing=east,type=single,waterlogged=false]'); put(5, W, 13, 'barrel[facing=up,open=false]'); put(5, W + 1, 13, 'cake')
    put(3, W + 3, 16, 'lantern[hanging=true,waterlogged=false]')
    B.sign(5, W + 1, 23, 'spruce_wall_sign[facing=south,waterlogged=false]', ['RAT GANG HQ', 'Crew & VIPs', 'only. No cats.', '(mouse hole)'], color='yellow', glow=True)
    # THE LUCKY DEN: a riverboat casino moored in the harbour basin - the cabin, the machines, a paddle wheel, smokestacks
    for x in range(7, 16):
        for z in range(62, 76):
            bow = z < 64 and abs(x + .5 - 11.5) > (z - 61) * 2.2
            if bow: continue
            edge = x in (7, 15) or z == 75 or (z < 64 and abs(x + .5 - 11.5) > (z - 62) * 2.2 - 0.5)
            for y in range(4, GF): put(x, y, z, 'dark_oak_planks' if edge or y == 4 else 'spruce_planks')
            put(x, GF, z, 'stripped_dark_oak_log[axis=z]' if edge else 'spruce_planks')
            for y in range(W, W + 5): air(x, y, z)
            if edge and not (z < 64 and x in (11, 12)): put(x, W, z, 'dark_oak_fence')
            KEEP.add((x, z))
    for x in range(8, 15):
        for z in range(65, 74):
            edge = x in (8, 14) or z in (65, 73)
            for y in range(W, W + 4):
                if edge: put(x, y, z, 'gold_block' if (x in (8, 14) and z in (65, 73)) else ('lime_stained_glass_pane[waterlogged=false]' if y == W + 2 and (x + z) % 2 and not x == 8 else 'dark_oak_planks'))
            put(x, W + 4, z, 'verdant_froglight' if edge and (x + z) % 2 else 'dark_oak_planks')
    for x in (11, 12):
        for y in (W, W + 1): air(x, y, 65)
    sl = SPOTS['slots']
    for z in sl['zs']:
        put(sl['wall_x'], W, z, 'redstone_block'); put(sl['wall_x'], W + 1, z, 'redstone_lamp[lit=true]'); air(sl['wall_x'], W + 2, z)
        put(sl['lever_x'], W + 1, z, 'lever[face=wall,facing=east,powered=false]')
    for z in (66, 68, 70, 72): put(sl['wall_x'], W, z, 'gold_block')
    counter([(x, 71) for x in range(10, 14)], top='gold_block')           # (2.81a: Lucky behind it at z 72)
    for (x, z) in [(12, 70), (13, 70)]: put(x, W, z, 'red_carpet' if (x + z) % 2 else 'black_carpet')
    put(13, W, 66, 'bell[attachment=floor,facing=west,powered=false]')
    put(11, W + 3, 69, 'lantern[hanging=true,waterlogged=false]')
    for x in range(10, 14):                                                     # the wheelhouse and the smokestacks
        for z in range(66, 69):
            e = x in (10, 13) or z in (66, 68)
            for y in range(W + 5, W + 7): put(x, y, z, ('lime_stained_glass_pane[waterlogged=false]' if y == W + 6 and (x + z) % 2 else 'dark_oak_planks') if e else 'air')
            put(x, W + 7, z, 'dark_oak_slab[type=bottom,waterlogged=false]')
    for (x, z) in [(10, 71), (13, 71)]:
        for y in range(W + 5, W + 10): put(x, y, z, 'polished_blackstone')
        put(x, W + 8, z, 'gold_block'); put(x, W + 10, z, 'campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]')
    for zz in range(66, 73):
        for yy in range(3, 12):
            d = math.hypot(zz - 69, yy - 7.5)
            if 2.3 <= d <= 3.6 or (d < 3.6 and (zz == 69 or yy in (7, 8))):
                put(6, yy, zz, 'stripped_dark_oak_log[axis=x]' if d > 2.3 else 'dark_oak_planks')
                KEEP.add((6, zz))
    for z in (60, 61):
        for x in (11, 12): put(x, GF, z, 'spruce_slab[type=top,waterlogged=false]'); KEEP.add((x, z))
    for x in range(9, 14): put(x, GF, 59, pick(QUAY))
    B.sign(11, W + 3, 64, 'dark_oak_wall_sign[facing=north,waterlogged=false]', ['THE LUCKY DEN', 'Scratch cards', 'Lucky Tokens', 'House always wins'], color='green', glow=True)
    put(11, W + 3, 65, 'dark_oak_planks') if g(11, W + 3, 65) == 'air' else None

    # ================================================================ lamps along the lanes, crates in the back lots, moss by the water
    for (pts, every) in [(PAWN, 6), (FURN, 6)]:
        for i in range(len(pts) - 1):
            (ax, az), (bx2, bz2) = pts[i], pts[i + 1]; L = math.hypot(bx2 - ax, bz2 - az)
            for t in range(0, int(L), every):
                px, pz = ax + (bx2 - ax) * t / L, az + (bz2 - az) * t / L
                nx, nz = -(bz2 - az) / L, (bx2 - ax) / L
                x, z = round(px + nx * 3), round(pz + nz * 3)
                if g(x, W, z) == 'air' and (x, z) in ROAD and (x, z) not in KEEP and math.hypot(x - CX, z - CZ) > 14: lamp(x, z); KEEP.add((x, z))
    lava_cells = [(x, z) for x in range(60, 70) for z in range(12, 17)]
    for _ in range(260):
        x, z = rnd.randrange(4, 72), rnd.randrange(14, 79)
        if not INS(x, z) or (x, z) in ROAD or (x, z) in WATER or (x, z) in KEEP or math.hypot(x - CX, z - CZ) < 14: continue
        if any(abs(x - a) <= 5 and abs(z - b) <= 5 for a, b in lava_cells): continue
        if g(x, W, z) != 'air' or g(x, GF, z) in ('air', 'water'): continue
        if not any(g(x + a, W, z + b) not in ('air', 'water', 'light') for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))): continue
        k = rnd.random()
        if k < .45:
            put(x, W, z, 'barrel[facing=up,open=false]')
            if rnd.random() < .35: put(x, W + 1, z, 'barrel[facing=up,open=false]')
        elif k < .6: put(x, W, z, 'decorated_pot[cracked=false,facing=north,waterlogged=false]')
        elif k < .75: put(x, W, z, 'spruce_planks'); put(x, W + 1, z, 'spruce_slab[type=bottom,waterlogged=false]') if rnd.random() < .5 else None
        else: put(x, W, z, 'hay_block[axis=y]')
    for (x, z), ins in inside.items():
        if ins and (x, z) not in WATER and (x, z) not in ROAD and (x, z) not in KEEP and g(x, GF, z) in ('tuff', 'cobbled_deepslate', 'deepslate'):
            if any((x + a, z + b) in WATER for a in (-2, -1, 0, 1, 2) for b in (-2, 0, 2)) and rnd.random() < .6: put(x, GF, z, 'moss_block')

    # ================================================================ dome dressing: chandeliers on long chains, dripstone, spore blossoms
    for k in range(10):
        a = k * math.pi / 5; r = 8.5 + (k % 2) * 3
        hang(round(CX + r * math.cos(a)), round(CZ + r * math.sin(a)), 17 + (k % 3))
    for (x, z, b) in [(38, 62, 20), (26, 40, 18), (19, 35, 16), (17, 56, 16), (12, 50, 16), (56, 46, 19), (60, 30, 20), (52, 66, 18), (30, 72, 21)]:
        hang(x, z, b)
    open_ceiling = [(x, z) for (x, z) in ceil if B.b.get((x, ceil[(x, z)], z)) == 'minecraft:air']
    for (x, z) in open_ceiling:
        t = ceil[(x, z)]
        if (x, t + 1, z) not in ROCK: continue
        r = rnd.random()
        if r < 0.05:
            n = rnd.choice((1, 2, 2, 3))
            seq = {1: ['tip'], 2: ['frustum', 'tip'], 3: ['base', 'frustum', 'tip']}[n]
            if all(B.b.get((x, t - i, z)) == 'minecraft:air' for i in range(n + 3)) and t - n > BF + 4:
                for i, th in enumerate(seq): put(x, t - i, z, f'pointed_dripstone[thickness={th},vertical_direction=down,waterlogged=false]')
        elif r < 0.07:
            put(x, t, z, 'spore_blossom')

    # ================================================================ the old market's cells: anything market2 built that this town doesn't is rock
    old = M2.build()
    for c in old.b:
        if c not in B.b: rock(*c)
    VIP_SHELL[:] = [c for c in VIP_SHELL]

    # ---------------------------------------------------------------- skin: every rock face touching open space is spring-safe; lichen
    OPEN = ('minecraft:air', 'minecraft:water[level=0]', 'minecraft:lava[level=0]')
    for (x, y, z) in list(ROCK):
        for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            n = B.b.get((x + dx, y + dy, z + dz))
            if n is not None and (x + dx, y + dy, z + dz) not in ROCK and (n in OPEN or not is_full(n)):
                S(x, y, z, pick(SPRING_SAFE)); break
    for (x, y, z) in list(ROCK):
        if not (W + 1 <= y <= W + 7) or rnd.random() > 0.05: continue
        for d, (dx, dz) in {'east': (-1, 0), 'west': (1, 0), 'south': (0, -1), 'north': (0, 1)}.items():
            ax, az = x + dx, z + dz
            if B.b.get((ax, y, az)) == 'minecraft:air' and (ax, y, az) not in ROCK and (ax, az) not in WATER:
                props = {k: 'false' for k in ('down', 'east', 'north', 'south', 'up', 'west', 'waterlogged')}
                props[d] = 'true'
                put(ax, y, az, 'glow_lichen[' + ','.join(f'{k}={v}' for k, v in sorted(props.items())) + ']')
                break
    for (x, y, z) in list(ROCK):                                           # a few shroomlights glowing in the walls
        if W + 3 <= y <= 20 and (x * 7 + y * 3 + z * 11) % 97 == 0 and 0 < x < SX - 1 and 0 < z < SZ - 1 and all((x + a, y + b, z + c) in B.b for a, b, c in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))) and any(B.b.get((x + a, y, z + b)) == 'minecraft:air' for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            S(x, y, z, 'minecraft:shroomlight'); ROCK.discard((x, y, z))

    # ================================================================ markers
    M = B.marker
    for k, (x, y, z, yaw) in NPC_POS.items(): M(x, y, z, ['bm.npc_spawn', f'bm.npc.{k}'], yaw)
    M(CX + 2.5, 7.2, CZ + 0.5, ['bm.npc_spawn', 'bm.npc.mike'], 0)
    M(2.5, W, 14.5, ['bm.npc_spawn', 'bm.npc.deco_rat'], 0)
    M(5.5, W, 15.5, ['bm.npc_spawn', 'bm.npc.deco_rat'], 0)
    M(CX + 0.5, W + 7, CZ + 0.5, ['bm.mfx'], 0)
    M(CX - 2.5, 7.5, CZ - 1.5, ['bm.mfx2'], 0)
    M(38.5, BF + 2.0, 82.5, ['bm.market_door'], 0)
    M(38.5, BF + 1, 88.5, ['bm.market_exit'], 0)
    for (x, y, z) in [(38, W + 2, 46), (20, W + 2, 46), (58, W + 2, 46), (38, W + 2, 22), (38, BF + 2, 76), (8, W + 2, 26), (11, W + 2, 66),
                      (63, W + 2, 24), (63, W + 2, 70), (38, W + 2, 8), (55, BF + 2, 8), (46, BF + 2, 18), (30, BF + 2, 20), (12, W + 2, 40)]:
        M(x + 0.5, y, z + 0.5, ['bm.market_hall', 'bm.zone_m'], 0)
    M(CX + 0.5, W + 2, CZ + 0.5, ['bm.mkt', TOWN_TAG], 0)
    for (x, y, z, yaw, nid) in [(11.5, W + 6.0, 63.6, 180, 'lucky'), (38.5, BF + 4.0, 72.4, 0, 'welcome'), (57.45, W + 5.6, 45.5, 90, 'flagon'),
                                (63.5, W + 5.5, 22.6, 0, 'forge'), (57.45, W + 7.2, 71.5, 90, 'blood'), (37.5, W + 5.4, 15.4, 0, 'auction'),
                                (46.5, BF + 4.4, 15.3, 0, 'vip'), (13.05, W + 5.2, 26.5, -90, 'docks'), (38.5, W + 7.5, 24.5, 0, 'alley')]:
        M(x, y, z, ['bm.npc_spawn', 'bm.npc.neon', f'bm.neon_{nid}'], yaw)
    crowd = [(60.5, W, 41.5, -90, 'pirate'), (62.5, W, 41.5, 90, 'prof'), (60.5, W, 48.5, -90, 'lucky'), (62.5, W, 48.5, 90, 'chef'),
             (63.5, W, 50.5, -90, 'pirate'), (68.5, W, 44.5, 90, 'soldier'),                                   # tavern regulars
             (9.5, W, 63.5, 0, 'lucky'), (14.5, W, 63.5, 0, 'pirate'), (10.5, W, 74.0, 180, 'prof'),        # card sharps on deck
             (12.5, W, 62.8, 0, 'soldier'),                                                                     # the Den's bouncer (at the bow)
             (34.5, BF + 1, 72.5, 180, 'soldier'), (42.5, BF + 1, 72.5, 180, 'soldier'),                        # Lookout guards
             (49.5, BF + 1, 17.5, 90, 'soldier'),                                                               # terrace watch
             (21.5, W, 24.5, 90, 'pirate'), (15.5, W, 26.5, 0, 'pirate'),                                       # dock hands
             (busker[0] + 0.5, W + 1, busker[1] + 0.5, 0, 'lucky'),                                             # the busker
             (63.5, W, 19.5, 0, 'soldier')]                                                                     # forge hand
    for (x, y, z, yaw, v) in crowd:
        st = B.b.get((int(x // 1), int(y // 1), int(z // 1)), '')
        if ('stairs' in st and 'half=bottom' in st) or ('slab' in st and 'type=bottom' in st): y += 0.5
        M(x, y, z, ['bm.npc_spawn', 'bm.npc.crowd', f'bm.cv_{v}'], yaw)
    M(busker[0] + 0.5, W + 1, busker[1] + 0.5, ['bm.busker'], 0)
    for (x, y, z) in AUCTION_SEATS: CUSHIONS.append((x, y, z, 'red'))
    for (x, y, z, col) in CUSHIONS:
        st = B.b.get((x, y, z), '')
        M(x + 0.5, y + (0.5 if 'slab' in st and 'type=bottom' in st else 0.0), z + 0.5, ['bm.npc_spawn', 'bm.npc.cushion', f'bm.cu_{col}'], 0)
    routes = {'a': [(round(CX + 8.5 * math.cos(k * math.pi / 4)), round(CZ + 8.5 * math.sin(k * math.pi / 4))) for k in range(8)],
              'b': [(37, 31), (37, 19)],
              'c': [(13, 39), (13, 23)]}
    for rid, pts in routes.items():
        for i, (x, z) in enumerate(pts): M(x + 0.5, W, z + 0.5, ['bm.wp', f'bm.route_{rid}', f'bm.wpi_{i}'], 0)
        x, z = pts[0]
        M(x + 0.5, W, z + 0.5, ['bm.npc_spawn', 'bm.npc.walker', f'bm.route_{rid}', 'bm.cv_' + {'a': 'chef', 'b': 'pirate', 'c': 'lucky'}[rid]], 0)
    for (x, z) in [(61, 20), (65, 20), (68, 21)]: M(x + 0.5, W, z + 0.5, ['bm.vent'], 0)
    # mouse holes: a 1x1 notch at the foot of a house's side wall, open floor in front (decoration)
    for (x0, z0, x1, z1, front) in HOUSES:
        if len(HOLES) >= 7: break
        for (hx, hz, fx2, fz2) in [(x0, (z0 + z1) // 2 + 1, x0 - 1, (z0 + z1) // 2 + 1), (x1, (z0 + z1) // 2 + 1, x1 + 1, (z0 + z1) // 2 + 1),
                                   ((x0 + x1) // 2 + 1, z1, (x0 + x1) // 2 + 1, z1 + 1)]:
            st = B.b.get((hx, W, hz), ''); fl = B.b.get((fx2, GF, fz2), '')
            if st and is_full(st) and 'log' not in st and B.b.get((fx2, W, fz2)) == 'minecraft:air' and fl and spawn_surface(fl) \
                    and B.b.get((hx - (fx2 - hx), W, hz - (fz2 - hz))) == 'minecraft:air':
                put(hx, W, hz, 'air'); HOLES.append(((hx, hz), (fx2, fz2))); break
    for (x, y, z, k) in [(CX, W + 2, CZ, 'plaza'), (64, W + 2, 18, 'forge'), (65, W + 2, 46, 'tavern'), (64, W + 2, 71, 'blood'),
                         (11, W + 2, 69, 'den'), (14, W + 2, 28, 'docks'), (38, W + 2, 24, 'alley')]:
        M(x + 0.5, y, z + 0.5, ['bm.amb', f'bm.amb_{k}'], 0)

    # (2.82) a way out of the water: the quays stand four blocks over it, and a player who fell in had no way back up. A ladder
    #  up a wall wherever the top opens onto a street (solid quay, two blocks of air over it - never up into the far bank's
    #  rock or a house wall), no two within a few blocks of each other; the column it climbs left clear by the docks.
    FACE = {(1, 0): 'west', (-1, 0): 'east', (0, 1): 'north', (0, -1): 'south'}
    LADDERS.clear()
    for (x, z) in sorted(WATER, key=lambda c: (c[1], c[0])):
        if any(abs(x - lx) + abs(z - lz) < 6 for lx, lz in LADDERS): continue
        if any(g(x, y, z) not in ('water', 'air') for y in range(4, W + 2)): continue
        for (dx, dz), face in FACE.items():
            n = (x + dx, z + dz)
            if n in WATER or not INS(*n): continue
            if not is_full(B.b.get((n[0], GF, n[1]), 'minecraft:air')) or g(n[0], W, n[1]) != 'air' or g(n[0], W + 1, n[1]) != 'air': continue
            for y in range(4, GF + 1): put(x, y, z, f'ladder[facing={face},waterlogged={"true" if y <= WATER_TOP else "false"}]')
            LADDERS.append((x, z)); break
    B.water_cells = sorted(WATER)
    support_lanterns(B, put)
    lights = spawnproof(B, fix=True, forbid=DOOR_BOX)
    B.meta = {'lights_added': lights, 'ceil': ceil}
    return B


def check(B):
    """Static proofs (run at build), market2's, for this town: every trader reachable on foot from the vault, nothing
    flammable within reach of lava, nothing dark, no fluid touching the outside, sealed, the Captain secret."""
    import p2.verify as V
    from p2.verify import Grid, reach
    errs = []
    G = Grid(B, outside='solid')
    V.GRID = G
    for x in range(37, 40):
        for y in range(BF + 1, BF + 4): G.override[(x, y, 82)] = 'minecraft:air'
    seen = G.bfs([(38, BF + 1, 88)], margin=0)
    for e in B.ents:
        t = e['nbt']['Tags']; x, y, z = e['pos']
        if not any(k.startswith('bm.npc.') and k not in ('bm.npc.deco_rat', 'bm.npc.mike', 'bm.npc.neon', 'bm.npc.walker', 'bm.npc.captain', 'bm.npc.cushion') for k in t): continue
        if 'bm.npc.crowd' in t: continue
        if not reach(seen, int(x), int(y), int(z), 4.5):
            errs.append(f'{[k for k in t if k.startswith("bm.npc.")][0]} at {(x, y, z)} is not reachable on foot from the vault')
    for (x, y, z), st in B.b.items():
        if not st.startswith('minecraft:lava'): continue
        for dx in range(-4, 5):
            for dz in range(-4, 5):
                for dy in range(-1, 5):
                    n = B.b.get((x + dx, y + dy, z + dz))
                    if n and flammable(n.split(':')[1].split('[')[0]):
                        errs.append(f'flammable {n} at {(x + dx, y + dy, z + dz)} within reach of lava at {(x, y, z)}'); break
    dark = spawnproof(B, fix=False)
    if dark: errs.append(f'{len(dark)} dark walkable cells, e.g. {dark[:5]}')
    for (x, y, z), st in B.b.items():
        if st.startswith(('minecraft:water', 'minecraft:lava')):
            for d in ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1), (0, -1, 0)):
                if (x + d[0], y + d[1], z + d[2]) not in B.b: errs.append(f'fluid at {(x, y, z)} touches the outside world'); break
    for (x, y, z), st in B.b.items():
        if is_full(st) or (37 <= x <= 39 and z == SZ - 1): continue
        for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            if (x + d[0], y + d[1], z + d[2]) not in B.b: errs.append(f'open cell {(x, y, z)} {st} touches the world outside the market'); break
    # (a hanging or standing thing needs something to hang from or stand on - an unsupported bell or lantern pops off at
    #  the first block update, as the clock tower's bell did)
    BACK = {'north': (0, 0, 1), 'south': (0, 0, -1), 'east': (-1, 0, 0), 'west': (1, 0, 0)}
    for (x, y, z), st in B.b.items():
        nm = st.split(':')[1].split('[')[0]; need = None
        if nm == 'bell': need = (0, 1, 0) if 'attachment=ceiling' in st else (0, -1, 0) if 'attachment=floor' in st else None
        elif nm in ('lantern', 'soul_lantern'): need = (0, 1, 0) if 'hanging=true' in st else (0, -1, 0)
        elif nm in ('torch', 'soul_torch', 'redstone_torch'): need = (0, -1, 0)
        elif nm in ('wall_torch', 'soul_wall_torch', 'redstone_wall_torch'):
            f = re.search(r'facing=(\w+)', st); need = BACK.get(f.group(1)) if f else None
        if need is None: continue
        n = B.b.get((x + need[0], y + need[1], z + need[2]), 'minecraft:stone')
        if n.split('[')[0] in ('minecraft:air', 'minecraft:cave_air', 'minecraft:water', 'minecraft:lava'):
            errs.append(f'{nm} at {(x, y, z)} hangs from (or stands on) {n}')
    for (hx, hz), _ in HOLES:
        if B.b.get((hx, W, hz)) != 'minecraft:air': errs.append(f'mouse hole {(hx, hz)} missing')
    # (2.82) nobody stranded in the water: every cell of the river and the basin within reach of a ladder out
    far = [c for c in B.water_cells if not any(abs(c[0] - lx) + abs(c[1] - lz) <= 9 for lx, lz in LADDERS)]
    if far: errs.append(f'{len(far)} water cells more than 9 blocks from a ladder out, e.g. {far[:4]}')
    cap = next(e['pos'] for e in B.ents if 'bm.npc.captain' in e['nbt']['Tags'])
    if reach(seen, int(cap[0]), int(cap[1]), int(cap[2]), 2.5): errs.append('the Captain can be reached without shrinking')
    if not all(B.b.get((4, W, z), '').startswith('minecraft:deepslate_brick_slab[type=top') for z in (20, 21, 22)):
        errs.append('the mouse hole is not a half-block gap')
    for p in DOOR_BOX:
        if B.b.get(p, '').startswith('minecraft:light'): errs.append(f'light block {p} inside the vault door fill box')
    # (2.81a) no slab as or on a counter, nor between a trader and his customers: a slab hides the trader and the book on it
    for (x, z) in COUNTERS:
        for y in (W, W + 1):
            if 'slab' in B.b.get((x, y, z), ''): errs.append(f'slab at the counter {(x, y, z)}')
    for nm, (x, y, z, yaw) in NPC_POS.items():
        fx, fz = round(-math.sin(math.radians(yaw))), round(math.cos(math.radians(yaw)))
        for df in (1, 2):
            for ds in (-1, 0, 1):
                cx, cz = int(math.floor(x + fx * df + fz * ds)), int(math.floor(z + fz * df - fx * ds))
                for yy in (int(y), int(y) + 1):
                    if 'slab' in B.b.get((cx, yy, cz), ''): errs.append(f'slab in front of {nm} at {(cx, yy, cz)}')
    return sorted(set(errs))

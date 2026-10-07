"""THE BLACK MARKET 2.0 (1.13): a lived-in rat bazaar in a domed cavern.

Layout (x east, z south; walk level y10 unless noted):
  south   the vault door (walk y18) opens onto a BALCONY overlooking the whole cavern; twin stairs down to the plaza
  centre  FOUNTAIN PLAZA - a waterfall falls from a crack in the dome into Mike's pond; notice board, a busker's barrel
  west    an underground RIVER (x19-23) in a chasm; the DOCKS (Capt. Cheddarbeard, Rat Gang HQ behind a mouse hole)
          and THE LUCKY DEN (Lucky Whiskers) on the far bank, reached by a stone bridge or THE DROP (rickety planks)
  north   PAWN ALLEY (the Fence, Old Barnaby; Madame Velour on the plaza corner) under a timber TERRACE (walk y17) with
          THE STACKS (Prof. Whiskerton); behind the north wall: the AUCTION HALL (gated) and the GILDED GUTTER (VIP, gated)
  east    THE FORGE PIT (Vinny, Steelwhisker; a lava channel behind bars, steam vents), THE GNAWED FLAGON (Chef Fromage,
          a crowded tavern), THE BLOOD ALCOVE (the Bloodbroker, red-lit behind a raised portcullis)
Safety by construction: every rock face that touches open space is a non-'spring' stone (no lava/water springs, glow
lichen or dripstone features can attach after placement); nothing flammable within 4 blocks of lava; every walkable
cell is lit (light >= 2, checked by spawnproof()); the worldgen structure also forbids natural monster spawns.
Runtime markers (NPCs, crowd, neon, walkers, vents, rat holes, emitters, zones) are listed at the end."""
import math
import random
from structures import Build

SX, SY, SZ = 76, 32, 98
GF, W = 9, 10                 # plaza floor block / walk level
BF = 17                       # balcony & terrace floor (walk 18)
CX, CZ, RX, RZ = 38, 46, 36.0, 35.0
RIVER = (19, 23)              # x range of the river channel
HOLES = [((5, 52), (5, 51)), ((58, 36), (58, 35)), ((62, 58), (62, 57)), ((35, 74), (35, 73)), ((9, 22), (9, 23)), ((34, 14), (34, 15))]
DOOR_BOX = {(x, y, z) for x in range(36, 41) for y in range(16, 22) for z in range(80, 85)}   # keep lights out of the vault door's fill box
VIP_SHELL = []          # 1.17: cells closed round the Gilded Gutter (the world patch for older markets is built from these)
AUCTION_SEATS = []      # 2.13: cushion cells in the auction hall (feet level)
CUSHIONS = []           # 2.13: (x, y, z, colour) - every cushion seat in the market
COUNTERS = []           # 2.24: every counter cell (x, z) - old markets had a slab on top of each
WATER_TOP = 5                 # water y3..5
SPRING_SAFE = ['cobbled_deepslate'] * 5 + ['smooth_basalt'] * 2 + ['blackstone', 'mossy_cobblestone', 'cracked_deepslate_bricks', 'cobblestone']
ROCK_IN = ['deepslate'] * 6 + ['stone'] * 2 + ['tuff']
PLAZA = ['polished_blackstone_bricks'] * 14 + ['polished_blackstone'] * 6 + ['cracked_polished_blackstone_bricks'] * 4 + ['gilded_blackstone']
STREET = ['mud_bricks'] * 5 + ['packed_mud'] * 2 + ['polished_blackstone']
WOODS = ('oak', 'spruce', 'birch', 'jungle', 'acacia', 'mangrove', 'cherry', 'bamboo')       # (dark_oak, pale_oak match 'oak'; nether woods don't burn)
WOOD_PARTS = ('planks', 'slab', 'stairs', 'fence', 'log', 'wood', 'shelf')
BURNS = ('wool', 'carpet', 'bookshelf', 'hay_block', 'leaves', 'scaffolding', 'lectern', 'composter', 'target', 'tnt', 'vine', 'moss_block', 'moss_carpet',
         'spore_blossom', 'beehive', 'coal_block', 'dried_kelp', 'azalea')


def flammable(n):
    """Blocks vanilla fire can catch (FireBlock flammability), by name."""
    return any(k in n for k in BURNS) or (any(w in n for w in WOODS) and any(p in n for p in WOOD_PARTS))
# blocks a market floor may be made of (bm:market_floor) - distinctive, never natural terrain near a buried market
FLOOR_BLOCKS = ['polished_blackstone_bricks', 'polished_blackstone', 'cracked_polished_blackstone_bricks', 'gilded_blackstone',
                'chiseled_polished_blackstone', 'mud_bricks', 'packed_mud', 'spruce_planks', 'dark_oak_planks', 'polished_basalt',
                'red_nether_bricks', 'nether_bricks', 'crimson_planks', 'gold_block', 'spruce_slab', 'dark_oak_slab',
                'polished_blackstone_brick_slab', 'polished_blackstone_brick_stairs', 'spruce_stairs', 'dark_oak_stairs',
                'stripped_spruce_log', 'stripped_dark_oak_log', 'red_carpet', 'black_carpet', 'purple_carpet', 'green_carpet',
                'yellow_carpet', 'brown_carpet', 'iron_trapdoor', 'polished_deepslate']

EMIT = {'lantern': 15, 'soul_lantern': 10, 'copper_lantern': 15, 'waxed_copper_lantern': 15, 'campfire': 15, 'soul_campfire': 10,
        'shroomlight': 15, 'ochre_froglight': 15, 'pearlescent_froglight': 15, 'verdant_froglight': 15, 'glowstone': 15, 'sea_lantern': 15,
        'waxed_copper_bulb': 15, 'end_rod': 14, 'lava': 15, 'glow_lichen': 7, 'redstone_wall_torch': 7, 'redstone_torch': 7,
        'crying_obsidian': 10, 'magma_block': 3, 'lava_cauldron': 15, 'jack_o_lantern': 15, 'torch': 14, 'wall_torch': 14,
        'redstone_lamp': 15, 'smoker': 13, 'blast_furnace': 13, 'furnace': 13, 'firefly_bush': 2, 'enchanting_table': 7}


def build():
    VIP_SHELL.clear(); CUSHIONS.clear()
    rnd = random.Random(20261003)
    B = Build(SX, SY, SZ)
    S = B.set
    pick = rnd.choice
    ROCK = set()

    def rock(x, y, z):
        S(x, y, z, pick(ROCK_IN)); ROCK.add((x, y, z))

    def air(x, y, z):
        S(x, y, z, 'air'); ROCK.discard((x, y, z))

    def put(x, y, z, st):
        S(x, y, z, st); ROCK.discard((x, y, z))

    def fill(x1, y1, z1, x2, y2, z2, st):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1): put(x, y, z, st)

    # ---------------------------------------------------------------- the cavern
    def r_of(x, z):
        return (abs((x - CX) / RX) ** 6 + abs((z - CZ) / RZ) ** 6) ** (1 / 6)
    wob = {}
    for x in range(SX):
        for z in range(SZ):
            wob[(x, z)] = math.sin(x * 0.37 + z * 0.11) * 0.6 + math.sin(z * 0.29 - x * 0.07) * 0.6 + rnd.uniform(-0.25, 0.25)
    inside = {}
    for x in range(SX):
        for z in range(SZ):
            r = r_of(x, z) + wob[(x, z)] / 40
            inside[(x, z)] = r < 1.0
    for x in range(24, 54):
        for z in range(0, 14): inside[(x, z)] = False
    ceil = {}
    for (x, z), ins in inside.items():
        if not ins: continue
        r = min(1.0, r_of(x, z))
        ceil[(x, z)] = min(SY - 5, int(W + 11 + 8 * (1 - r * r) + wob[(x, z)]))
    # mark every cell near the cavern as rock first, then carve
    near = set()
    for (x, z), ins in inside.items():
        if ins:
            for dx in range(-3, 4):
                for dz in range(-3, 4):
                    if 0 <= x + dx < SX and 0 <= z + dz < SZ: near.add((x + dx, z + dz))
    for (x, z) in near:
        for y in range(0, SY):
            rock(x, y, z)
    for (x, z), ins in inside.items():
        if not ins: continue
        put(x, GF, z, pick(PLAZA))
        for y in range(W, ceil[(x, z)] + 1): air(x, y, z)

    def seal_room(x1, y1, z1, x2, y2, z2):
        """Force a solid one-block shell round a carved room, even where the cavern was already open (carve_room only
        fills cells nobody has set yet). Returns the cells it closed."""
        closed = []
        for x in range(x1 - 1, x2 + 2):
            for z in range(z1 - 1, z2 + 2):
                for y in range(y1 - 1, y2 + 2):
                    if x1 <= x <= x2 and z1 <= z <= z2 and y1 <= y <= y2: continue
                    if not (0 <= x < SX and 0 <= z < SZ and 0 <= y < SY): continue
                    st = B.b.get((x, y, z))
                    if st is None or st.endswith(':air') or st.endswith(':light') or 'light[' in st:
                        S(x, y, z, ROCK_IN[(x * 7 + y * 13 + z * 31) % len(ROCK_IN)]); ROCK.add((x, y, z))   # (no rnd: the rest of the build stays identical)
                        closed.append((x, y, z))
        return closed

    def carve_room(x1, y1, z1, x2, y2, z2, floor=None):
        """A room cut into the rock (keeps a rock shell around it)."""
        for x in range(x1 - 3, x2 + 4):
            for z in range(z1 - 3, z2 + 4):
                if not (0 <= x < SX and 0 <= z < SZ): continue
                for y in range(max(0, y1 - 3), min(SY, y2 + 4)):
                    if (x, y, z) not in B.b: rock(x, y, z)
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1):
                if floor: put(x, y1 - 1, z, floor if isinstance(floor, str) else pick(floor))
                for y in range(y1, y2 + 1): air(x, y, z)

    # ---------------------------------------------------------------- river + chasm (west)
    x1, x2 = RIVER
    for z in range(10, 84):
        for x in range(x1, x2 + 1):
            put(x, 2, z, pick(['gravel', 'mud', 'cobbled_deepslate']))
            for y in range(3, WATER_TOP + 1): put(x, y, z, 'water[level=0]')
            for y in range(WATER_TOP + 1, W): air(x, y, z)
            if (x, z) in ceil:
                for y in range(W, ceil[(x, z)] + 1): air(x, y, z)
            else:                                            # the river runs on into tunnels at both ends
                for y in range(W, W + 5): air(x, y, z)
    # waterfall feeding the river from a crack in the north wall
    for y in range(WATER_TOP + 1, 16): air(21, y, 10)
    for (dx, dz) in ((1, 0), (-1, 0)):
        for y in range(W + 5, 17): rock(21 + dx, y, 10 + dz)
    for (dx, dy, dz) in ((0, 0, -1), (1, 0, 0), (-1, 0, 0), (0, -1, 0), (0, 1, 0)): rock(21 + dx, 15 + dy, 9 + dz)
    put(21, 15, 9, 'water[level=0]')

    # ---------------------------------------------------------------- the fountain plaza
    for x in range(CX - 12, CX + 13):
        for z in range(CZ - 14, CZ + 15):
            if inside.get((x, z)) and not (x1 - 1 <= x <= x2 + 1):
                d = math.hypot(x - CX, z - CZ)
                put(x, GF, z, 'chiseled_polished_blackstone' if 6.5 <= d < 7.5 else pick(PLAZA))
    for x in range(CX - 6, CX + 7):                          # Mike's pond (radius 5), the waterfall's plunge pool
        for z in range(CZ - 6, CZ + 7):
            d = math.hypot(x - CX, z - CZ)
            if d < 5.2:
                put(x, 5, z, 'deepslate_tiles')
                for y in range(6, GF + 1): put(x, y, z, 'water[level=0]')
            elif d < 6.3:
                put(x, GF, z, 'polished_blackstone'); put(x, W, z, 'polished_blackstone_wall' if (x + z) % 3 else 'air')
    # the waterfall: a source hidden in a shaft in the dome, falling into the pond
    top = ceil[(CX, CZ)]
    for (dx, dz) in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
        for y in range(top + 1, top + 5): rock(CX + dx, y, CZ + dz)
    air(CX, top + 1, CZ); air(CX, top + 2, CZ); put(CX, top + 3, CZ, 'water[level=0]'); rock(CX, top + 4, CZ)
    for (x, z) in [(CX - 3, CZ + 2), (CX + 2, CZ - 3), (CX + 3, CZ + 3)]: put(x, W, z, 'lily_pad')
    # lamp posts around the plaza ring
    for k in range(8):
        a = k * math.pi / 4 + math.pi / 8
        x, z = round(CX + 10.5 * math.cos(a)), round(CZ + 10.5 * math.sin(a))
        if not inside.get((x, z)) or x1 - 1 <= x <= x2 + 1: continue
        for y in range(W, W + 3): put(x, y, z, 'polished_blackstone_wall')
        put(x, W + 3, z, 'lantern[hanging=false,waterlogged=false]')
    # notice board (2.24: the Bounty Board - its notice is a display, see phase40), the busker's barrel stage, benches, a cart
    for x in range(CX - 2, CX + 3):
        put(x, W, CZ - 11, 'stripped_dark_oak_log[axis=x]' if x in (CX - 2, CX + 2) else 'air')
        for y in (W + 1, W + 2): put(x, y, CZ - 11, 'dark_oak_planks' if x not in (CX - 2, CX + 2) else 'stripped_dark_oak_log[axis=y]')
    bx, bz = CX + 9, CZ + 8                                  # the busker
    put(bx, W, bz, 'barrel[facing=up,open=false]')
    put(bx + 1, W, bz, 'spruce_slab[type=bottom,waterlogged=false]'); put(bx, W, bz + 1, 'spruce_slab[type=bottom,waterlogged=false]')
    for (x, z, f) in [(CX - 9, CZ + 6, 'east'), (CX - 9, CZ + 7, 'east'), (CX + 6, CZ - 9, 'south'), (CX + 7, CZ - 9, 'south')]:
        put(x, W, z, 'dark_oak_slab[type=bottom,waterlogged=false]'); CUSHIONS.append((x, W, z, 'red'))              # 2.13: cushioned benches
    for (x, z) in [(CX - 10, CZ - 6), (CX - 10, CZ - 5)]:  # a cheese cart
        put(x, W, z, 'honeycomb_block'); put(x, W + 1, z, 'yellow_carpet')
    put(CX - 11, W, CZ - 6, 'dark_oak_fence'); put(CX - 11, W, CZ - 5, 'dark_oak_fence')

    # decorative market stalls round the plaza (no traders - just life)
    def awning(x1, z1, x2, z2, y, cols):
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1): put(x, y, z, f'{cols[(x + z) % len(cols)]}_wool')
        for (x, z) in ((x1, z1), (x1, z2), (x2, z1), (x2, z2)):
            for yy in range(W, y): put(x, yy, z, 'spruce_fence')
    awning(49, 37, 51, 40, W + 3, ['green', 'lime'])                      # a shady potion stall
    put(50, W, 38, 'brewing_stand[has_bottle_0=true,has_bottle_1=true,has_bottle_2=false]'); put(50, W, 39, 'water_cauldron[level=2]')
    put(51, W, 38, 'barrel[facing=up,open=false]'); put(49, W, 39, 'decorated_pot[cracked=false,facing=west,waterlogged=false]')
    awning(49, 51, 51, 54, W + 3, ['red', 'orange', 'yellow'])            # a rug seller
    for z in (52, 53): put(51, W, z, 'spruce_fence'); put(51, W + 1, z, ['red_carpet', 'cyan_carpet'][z % 2])
    for (x, z, c) in [(49, 52, 'magenta'), (50, 52, 'orange'), (49, 53, 'light_blue'), (50, 53, 'lime')]: put(x, W, z, f'{c}_carpet')
    awning(26, 51, 29, 54, W + 4, ['purple', 'black'])                    # a fortune teller's tent
    for z in range(51, 55):
        for y in range(W, W + 4):
            if z != 53: put(26, y, z, 'purple_wool')
    put(28, W, 52, 'dark_oak_fence'); put(28, W + 1, 52, 'amethyst_cluster[facing=up,waterlogged=false]'); put(27, W, 54, 'candle[candles=2,lit=true,waterlogged=false]')
    put(30, W, 60, 'campfire[facing=east,lit=true,signal_fire=false,waterlogged=false]')           # skewer grill
    for (x, z) in [(31, 59), (31, 61)]: put(x, W, z, 'spruce_slab[type=bottom,waterlogged=false]'); CUSHIONS.append((x, W, z, 'orange'))
    for (x, z) in [(48, 31), (49, 31), (48, 32), (27, 41), (27, 42), (52, 45), (52, 46), (52, 47), (33, 62), (43, 62)]:
        put(x, W, z, rnd.choice(['barrel[facing=up,open=false]', 'barrel[facing=north,open=false]', 'spruce_planks', 'hay_block[axis=y]']))
        if rnd.random() < 0.4: put(x, W + 1, z, rnd.choice(['barrel[facing=up,open=false]', 'decorated_pot[cracked=true,facing=north,waterlogged=false]', 'honeycomb_block']))
    # ---------------------------------------------------------------- PAWN ALLEY + terrace (north)
    for x in range(25, 53):
        for z in range(22, 27): put(x, GF, z, pick(STREET))
    def stall_roof(x1, z1, x2, z2, y, cols):
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1): put(x, y, z, f'{cols[(x + z) % len(cols)]}_wool')
    def counter(cells, top=None):
        """2.13: a waist-high counter, one block tall (it used to be a log under a top-half slab, which floated and stood
        two blocks high). Wood counters are a horizontal beam along the counter's run; the others are the stall's stone."""
        COUNTERS.extend(cells)
        axis = 'x' if len({z for _, z in cells}) == 1 else 'z'
        for (x, z) in cells:
            put(x, W, z, top or f'stripped_dark_oak_log[axis={axis}]')
    # carve the north band (stalls under the terrace, the terrace, and the rooms behind the wall)
    carve_room(25, W, 14, 52, 22, 21, floor=STREET)
    # terrace floor (y17) over the stalls, posts at the street edge
    for x in range(25, 53):
        for z in range(14, 22): put(x, BF, z, 'spruce_planks' if (x + z) % 4 else 'stripped_spruce_log[axis=x]')
    for x in range(25, 53, 4):
        for y in range(W, BF): put(x, y, 21, 'stripped_dark_oak_log[axis=y]')
    for x in range(25, 53):
        if x not in (49, 50): put(x, BF + 1, 21, 'dark_oak_fence')
    for x in range(27, 52, 4): put(x, BF - 1, 21, 'lantern[hanging=true,waterlogged=false]')   # 1.19: under the terrace edge, between the posts (z22 hung from nothing)
    # terrace stair (east end): x49-50 from the street (z27, y10) up north to the terrace edge (z21, y17)
    for k, z in enumerate(range(28, 21, -1)):
        y = W + k
        for x in (49, 50):
            for yy in range(GF, y): put(x, yy, z, 'spruce_planks')
            put(x, y, z, 'spruce_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]')
            for yy in range(y + 1, y + 4):
                if (x, yy, z) in B.b and yy < BF: air(x, yy, z)
    # OLD BARNABY (west stall, under the terrace)
    stall_x = (26, 33)
    counter([(x, 20) for x in range(27, 33)])
    for x in range(26, 34): put(x, W, 14, 'chest[facing=south,type=single,waterlogged=false]' if x % 2 else 'barrel[facing=south,open=false]')
    put(26, W, 17, 'anvil[facing=east]'); put(32, W + 1, 20, 'candle[candles=3,lit=true,waterlogged=false]')   # 2.20: on the counter, not above it
    for (x, z) in [(29, 15), (30, 15), (31, 16)]: put(x, W, z, 'barrel[facing=up,open=false]')
    put(28, W + 4, 17, 'lantern[hanging=true,waterlogged=false]'); put(28, W + 5, 17, 'iron_chain[axis=y,waterlogged=false]'); put(28, W + 6, 17, 'iron_chain[axis=y,waterlogged=false]')
    B.sign(29, W + 2, 22, 'dark_oak_wall_sign[facing=south,waterlogged=false]', ["OLD BARNABY'S", 'Pawn & Refunds', 'Half back.', 'No questions.'], color='white', glow=True)
    # the Auction Hall passage (x35-39) - gated
    for x in range(35, 40):
        for z in range(14, 22): put(x, GF, z, 'polished_blackstone_bricks' if (x + z) % 2 else 'polished_blackstone')
    for z in range(15, 21): put(37, W, z, 'red_carpet'); put(36, W, z, 'red_carpet') if z % 2 else None
    for y in range(W, W + 5):
        for x in (34, 40): put(x, y, 14, 'chiseled_polished_blackstone')
    for x in range(35, 40):
        for y in range(W, W + 4): put(x, y, 14, 'iron_bars')
        put(x, W + 4, 14, 'gold_block')
    B.sign(37, W + 4, 15, 'dark_oak_wall_sign[facing=south,waterlogged=false]', ['THE DARK', 'AUCTION', 'Next sale:', 'soon.'], color='yellow', glow=True)
    # THE FENCE (east stall, the biggest)
    counter([(x, 20) for x in range(41, 49)])
    for x in range(41, 49): put(x, W, 14, 'barrel[facing=south,open=false]'); put(x, W + 1, 14, 'barrel[facing=up,open=false]')
    for (x, y) in [(44, W), (45, W), (44, W + 1)]: put(x, y, 15, 'gold_block')
    put(47, W, 16, 'chest[facing=west,type=single,waterlogged=false]'); put(42, W + 1, 20, 'gold_block')
    put(46, W + 4, 17, 'lantern[hanging=true,waterlogged=false]'); put(46, W + 5, 17, 'iron_chain[axis=y,waterlogged=false]'); put(46, W + 6, 17, 'iron_chain[axis=y,waterlogged=false]')
    B.sign(45, W + 2, 22, 'dark_oak_wall_sign[facing=south,waterlogged=false]', ['~ THE FENCE ~', 'Currency', 'Exchange', '& Maps'], color='yellow', glow=True)
    # laundry lines + crates along the street
    for x in range(26, 48, 2):
        if rnd.random() < 0.6: put(x, W, 26 if x % 4 else 22, 'barrel[facing=up,open=false]' if x % 3 else 'decorated_pot[cracked=true,facing=south,waterlogged=false]')
    # THE STACKS (on the terrace, x26-44): shelves, lecterns, candles
    for x in range(26, 45):
        for y in range(BF + 1, BF + 5): put(x, y, 14, 'bookshelf')
    for (x0, x1_) in ((27, 31), (33, 37), (39, 43)):
        for x in range(x0, x1_ + 1): put(x, BF + 1, 17, 'bookshelf'); put(x, BF + 2, 17, 'bookshelf') if x in (x0, x1_) else None
    put(34, BF + 1, 19, 'lectern[facing=south,has_book=false,powered=false]'); put(41, BF + 1, 19, 'enchanting_table')
    for (x, z) in [(29, 19), (38, 19), (43, 16)]: put(x, BF + 1, z, 'candle[candles=4,lit=true,waterlogged=false]')
    for x in (30, 40): put(x, BF + 5, 18, 'lantern[hanging=true,waterlogged=false]')
    B.sign(33, BF + 2, 18, 'dark_oak_wall_sign[facing=south,waterlogged=false]', ['THE STACKS', 'Prof. Whiskerton', 'Books * Maps', 'Skin Scrolls'], color='light_blue', glow=True)
    # Gilded Gutter door (terrace, x45-47 into the north wall) - gated
    for y in range(BF + 1, BF + 6):
        for x in (44, 48): put(x, y, 14, 'gold_block' if y == BF + 5 else 'chiseled_polished_blackstone')
    for x in range(45, 48):
        for y in range(BF + 1, BF + 4): put(x, y, 14, 'iron_bars')
        put(x, BF + 4, 14, 'gold_block'); put(x, BF + 5, 14, 'gold_block')
    for x in (45, 47): put(x, BF + 1, 16, 'red_carpet')
    put(46, BF + 1, 17, 'red_carpet')
    # rooms behind the north wall (built now so later updates can open them)
    carve_room(30, W, 2, 44, W + 5, 12, floor='dark_oak_planks')            # AUCTION HALL
    for x in range(35, 40):
        for z in (12, 13): put(x, GF, z, 'polished_blackstone'); [air(x, y, z) for y in range(W, W + 4)]
    # 2.13: three tiers rising AWAY from the podium (north), each a row of cushions on a dark-oak step with a walkway behind
    # (1.18's rows climbed toward the podium, so the back row sat lowest). Cushions are spawned from the bm.npc.cushion markers.
    AUCTION_SEATS.clear()
    for r in range(3):
        zs, zw = 6 + 2 * r, 7 + 2 * r                                             # seat row, walkway behind it
        for x in range(31, 44):
            if 36 <= x <= 38: continue
            for z in (zs, zw):
                for y in range(W, W + r): put(x, y, z, 'dark_oak_planks')
                if r: put(x, W + r - 1, z, 'dark_oak_slab[type=double,waterlogged=false]' if z == zs else 'dark_oak_planks')
            AUCTION_SEATS.append((x, W + r, zs))
    for x in range(34, 41):
        put(x, W, 3, 'polished_blackstone_bricks'); put(x, W, 4, 'red_carpet')
    put(37, W + 1, 3, 'polished_blackstone_brick_wall'); put(37, W + 3, 3, 'end_rod[facing=down]')
    put(37, W + 5, 7, 'lantern[hanging=true,waterlogged=false]')
    carve_room(49, BF + 1, 2, 62, BF + 5, 12, floor='dark_oak_planks')       # GILDED GUTTER (VIP)
    VIP_SHELL.extend(seal_room(49, BF + 1, 2, 62, BF + 5, 12))                 # 1.17: its south wall was open to the cavern
    for x in range(43, 52):                                                       # rock shell round the VIP corridor
        for z in range(8, 15):
            for y in range(BF - 1, BF + 6):
                if (x, y, z) not in B.b: rock(x, y, z)
    for x in range(45, 48):
        for z in range(10, 14): put(x, BF, z, 'dark_oak_planks'); [air(x, y, z) for y in range(BF + 1, BF + 4)]
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

    # ---------------------------------------------------------------- MADAME VELOUR (plaza NW corner, facing north onto the street)
    for x in range(27, 35):
        for z in range(28, 34): put(x, GF, z, 'spruce_planks')
    counter([(x, 28) for x in range(27, 35)])
    for y in range(W, W + 4): put(27, y, 28, 'dark_oak_fence'); put(34, y, 28, 'dark_oak_fence')
    stall_roof(27, 28, 34, 33, W + 4, ['purple', 'white'])
    put(28, W, 33, 'loom[facing=north]'); put(33, W, 33, 'water_cauldron[level=3]')
    for i, col in enumerate(['white', 'pink', 'cyan', 'purple', 'lime', 'orange']):         # bolts of cloth, every other one stacked (2.20)
        put(29 + i, W, 33, col + '_wool')
        if i % 2: put(29 + i, W + 1, 33, ['yellow', 'red', 'blue'][i // 2] + '_wool')
    put(30, W + 3, 31, 'lantern[hanging=true,waterlogged=false]')
    B.sign(31, W + 4, 27, 'dark_oak_wall_sign[facing=north,waterlogged=false]', ['OUTFITTER', 'Madame Velour', 'Armor * Gear * Hooks', 'Wings * Style'], color='magenta', glow=True)

    # ---------------------------------------------------------------- BRIDGES over the river
    for z in range(40, 45):                                   # the stone bridge (safe)
        for x in range(x1 - 1, x2 + 2):
            put(x, GF, z, 'polished_blackstone_bricks')
            if z in (40, 44): put(x, W, z, 'polished_blackstone_brick_wall')
            else: air(x, W, z)
        for x in range(x1, x2 + 1): put(x, GF - 1, z, 'polished_blackstone_brick_stairs[facing=%s,half=top,shape=straight,waterlogged=false]' % ('south' if z == 40 else 'north') if z in (40, 44) else 'polished_blackstone_bricks')
    for z in (40, 44):
        for x in (x1 - 1, x2 + 1):
            put(x, W, z, 'polished_blackstone_bricks'); put(x, W + 1, z, 'polished_blackstone_wall'); put(x, W + 2, z, 'lantern[hanging=false,waterlogged=false]')
    for z in (66, 67):                                        # THE DROP: rickety planks, two missing, no rail
        for x in range(x1 - 1, x2 + 2):
            if (x, z) in ((21, 66), (20, 67), (22, 67)): air(x, GF, z); continue
            put(x, GF, z, 'spruce_slab[type=top,waterlogged=false]')
    for (x, z) in ((x1 - 1, 65), (x2 + 1, 65), (x1 - 1, 68), (x2 + 1, 68)):
        put(x, W, z, 'spruce_fence'); put(x, W + 1, z, 'spruce_fence')
    put(x2 + 1, W + 2, 65, 'cobweb')
    B.sign(x2 + 2, W, 64, 'spruce_sign[rotation=12,waterlogged=false]', ['MIND THE', 'GAP', '(the river', 'is cold)'], color='red')     # 2.13: faces the walkway
    # railings along the plaza bank, with gaps (it's a black market, not a nursery)
    for z in range(12, 80):
        if inside.get((x2 + 1, z)) and not (39 <= z <= 45 or 64 <= z <= 69) and (z % 9) not in (0, 1):
            put(x2 + 1, W, z, 'dark_oak_fence')
    for z in range(12, 80):
        if inside.get((x1 - 1, z)) and not (39 <= z <= 45 or 64 <= z <= 69 or 20 <= z <= 34) and (z % 7) not in (0,):
            put(x1 - 1, W, z, 'dark_oak_fence')

    # ---------------------------------------------------------------- THE DOCKS (west bank, north)
    for x in range(4, 18):
        for z in range(18, 37):
            if inside.get((x, z)): put(x, GF, z, 'spruce_planks' if x > 12 else pick(STREET))
    for x in range(x1, x1 + 3):                                # pier over the water (walk y7)
        for z in range(22, 32): put(x, WATER_TOP + 1, z, 'spruce_planks' if (x + z) % 5 else 'stripped_spruce_log[axis=z]')
    for k, x in enumerate(range(x1 - 3, x1)):                # steps down from the bank (y10) east to the pier (y7) - 2.20: they ran backwards
        for z in (26, 27):
            put(x, W - 1 - k, z, 'spruce_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]')
            for y in range(W - k, W + 3): air(x, y, z)
            for y in range(WATER_TOP + 1, W - 1 - k): put(x, y, z, 'spruce_planks')
    for (x, z) in [(x1, 22), (x1 + 2, 22), (x1, 31), (x1 + 2, 31)]:
        for y in range(3, WATER_TOP + 3): put(x, y, z, 'stripped_spruce_log[axis=y]')
    def rowboat(xa, za):                                      # a moored rowboat made of slabs and stairs
        put(xa, WATER_TOP + 1, za, 'spruce_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]')
        put(xa, WATER_TOP + 1, za + 1, 'spruce_slab[type=bottom,waterlogged=false]')
        put(xa, WATER_TOP + 1, za + 2, 'spruce_slab[type=bottom,waterlogged=false]')
        put(xa, WATER_TOP + 1, za + 3, 'spruce_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]')
        put(xa, WATER_TOP + 2, za + 2, 'barrel[facing=up,open=false]')
    rowboat(x2 - 1, 18); rowboat(x2, 33)
    for y in range(W, W + 9): put(16, y, 20, 'stripped_dark_oak_log[axis=y]')       # the crane
    for x in range(17, 22): put(x, W + 8, 20, 'stripped_dark_oak_log[axis=x]')
    for y in range(W + 3, W + 8): put(21, y, 20, 'iron_chain[axis=y,waterlogged=false]')
    put(21, W + 2, 20, 'barrel[facing=up,open=false]')
    # Cheddarbeard's dock office (x6-12, z22-31), open to the river
    for x in range(6, 13):
        for z in range(22, 32):
            if x == 6 or z in (22, 31):
                for y in range(W, W + 5): put(x, y, z, 'spruce_planks' if y < W + 4 else 'stripped_spruce_log[axis=x]')
            put(x, W + 5, z, 'spruce_slab[type=bottom,waterlogged=false]')
    counter([(12, z) for z in range(24, 30)])
    for z in (23, 30): put(7, W, z, 'barrel[facing=up,open=false]'); put(7, W + 1, z, 'barrel[facing=up,open=false]')
    put(7, W, 26, 'chest[facing=east,type=single,waterlogged=false]'); put(8, W, 23, 'gold_block')
    put(9, W + 4, 27, 'lantern[hanging=true,waterlogged=false]')
    B.sign(12, W + 4, 27, 'spruce_hanging_sign[attached=false,rotation=12,waterlogged=false]', ['DOCKMASTER', 'The Captain', 'is in. Look', 'low. Think small.'], color='yellow', glow=True)
    # RAT GANG HQ: a den carved behind the dock office, reached only through a mouse hole
    carve_room(1, W, 12, 6, W + 3, 19, floor='dark_oak_planks')
    for z in range(11, 22):
        for y in range(W, W + 5): rock(0, y, z); rock(7, y, z)
    for x in range(0, 8):
        for y in range(W, W + 5): rock(x, y, 11)
        for z in range(11, 22): rock(x, W + 4, z)
    for x in range(1, 7):
        for z in range(20, 22): rock(x, W, z); rock(x, W + 1, z); rock(x, W + 2, z); rock(x, W + 3, z)
    put(4, W, 20, 'deepslate_brick_slab[type=top,waterlogged=false]'); put(4, W, 21, 'deepslate_brick_slab[type=top,waterlogged=false]')
    put(1, W, 13, 'gold_block'); put(2, W, 13, 'gold_block'); put(1, W + 1, 13, 'gold_block'); put(1, W, 14, 'raw_gold_block')
    put(1, W, 16, 'chest[facing=east,type=single,waterlogged=false]'); put(5, W, 13, 'barrel[facing=up,open=false]'); put(5, W + 1, 13, 'cake')
    put(3, W + 3, 16, 'lantern[hanging=true,waterlogged=false]')
    B.sign(5, W + 1, 22, 'spruce_wall_sign[facing=south,waterlogged=false]', ['RAT GANG HQ', 'Crew & VIPs', 'only. No cats.', '(mouse hole)'], color='yellow', glow=True)

    # ---------------------------------------------------------------- THE LUCKY DEN (west bank, south)
    lx1, lz1, lx2, lz2 = 3, 52, 16, 73
    for x in range(lx1, lx2 + 1):
        for z in range(lz1, lz2 + 1):
            put(x, GF, z, 'gold_block' if (x + z) % 2 == 0 else 'polished_blackstone')
            edge = x in (lx1, lx2) or z in (lz1, lz2)
            for y in range(W, W + 6):
                if edge: put(x, y, z, 'polished_blackstone_bricks' if y < W + 5 else 'gold_block')
                else: air(x, y, z)
            put(x, W + 6, z, 'polished_blackstone_bricks')
    for x in range(8, 12):                                   # front door (north) and back door (east, to The Drop)
        for y in range(W, W + 3): air(x, y, lz1)
    for z in (66, 67):
        for y in range(W, W + 3): air(lx2, y, z)
    for x in (7, 12):
        for y in range(W, W + 4): put(x, y, lz1, 'waxed_copper_bulb[lit=true,powered=false]' if y == W + 3 else 'gold_block')
    counter([(x, 70) for x in range(5, 13)], top='gold_block')
    for x in range(4, 16): put(x, W, 72, 'waxed_copper_bulb[lit=true,powered=false]' if x % 2 else 'gold_block'); put(x, W + 1, 72, 'gold_block' if x % 2 else 'waxed_copper_bulb[lit=true,powered=false]')
    for z in (56, 59, 62):
        put(4, W, z, 'gold_block'); put(4, W + 1, z, 'redstone_lamp[lit=true]'); put(3, W + 1, z, 'redstone_block')
        put(5, W + 1, z, 'lever[face=wall,facing=east,powered=false]')
    for (tx, tz) in [(9, 57), (12, 61)]:                     # card tables
        put(tx, W, tz, 'dark_oak_fence'); put(tx, W + 1, tz, 'green_carpet')
    put(13, W, 56, 'dark_oak_fence'); put(13, W + 1, 56, 'green_carpet')                # roulette wheel
    for (x, z) in [(10, 64), (11, 64), (10, 65), (11, 65)]: put(x, W, z, 'red_carpet' if (x + z) % 2 else 'black_carpet')
    put(15, W, 54, 'bell[attachment=floor,facing=west,powered=false]'); put(15, W, 60, 'jukebox[has_record=false]')
    put(9, W + 4, 61, 'lantern[hanging=true,waterlogged=false]'); put(9, W + 5, 61, 'iron_chain[axis=y,waterlogged=false]')
    B.sign(10, W + 3, lz1 - 1, 'dark_oak_wall_sign[facing=north,waterlogged=false]', ['THE LUCKY DEN', 'Scratch cards', 'Lucky Tokens', 'House always wins'], color='green', glow=True)

    # ---------------------------------------------------------------- THE FORGE PIT (east, north): lava channel, steam vents
    fx1, fz1, fx2, fz2 = 54, 16, 72, 34
    for x in range(fx1, fx2 + 1):
        for z in range(fz1, fz2 + 1):
            if inside.get((x, z)) or x <= 70: put(x, GF, z, 'polished_basalt[axis=y]')
    carve_room(fx1, W, fz1, fx2 - 1, W + 8, fz2, floor='polished_basalt[axis=y]')
    for z in range(fz1 + 1, fz2 - 2):                         # the lava channel along the east wall, behind bars
        for x in (68, 69):
            put(x, GF - 1, z, 'magma_block'); put(x, GF, z, 'lava[level=0]')
        put(70, GF, z, 'polished_basalt[axis=y]')
        put(67, W, z, 'iron_bars'); put(67, W + 1, z, 'iron_bars')
    for x in (67, 68, 69):                                    # the hot catwalk over the lava to the old furnace
        put(x, GF, 25, 'polished_blackstone_brick_slab[type=top,waterlogged=false]')
    air(67, W, 25); air(67, W + 1, 25)
    put(70, W, 25, 'blast_furnace[facing=west,lit=true]'); put(70, W + 1, 25, 'blast_furnace[facing=west,lit=true]')
    # Vinny (west part) and Steelwhisker (south part)
    counter([(60, z) for z in range(18, 24)], top='polished_blackstone_bricks')
    put(55, W, 19, 'grindstone[face=floor,facing=east]'); put(55, W, 22, 'anvil[facing=north]'); put(56, W, 18, 'smithing_table')
    put(55, W, 20, 'blast_furnace[facing=east,lit=true]'); put(55, W + 1, 20, 'blast_furnace[facing=east,lit=true]')
    # 2.20: the floating iron-bar rail at x54 (nothing under it) is gone
    put(60, W + 1, 21, 'polished_blackstone_bricks'); put(60, W + 2, 21, 'polished_blackstone_bricks')
    B.sign(61, W + 2, 21, 'dark_oak_wall_sign[facing=east,waterlogged=false]', ["VINNY'S ARMS", 'Blades * Picks', 'Axes * Bows', 'Upgrades'], color='red', glow=True)
    counter([(x, 29) for x in range(56, 64)], top='polished_andesite')
    for x in range(56, 64): put(x, W, 33, 'iron_block' if x % 3 == 0 else 'anvil[facing=east]' if x % 3 == 1 else 'blast_furnace[facing=north,lit=true]')
    put(60, W + 1, 29, 'polished_blackstone_bricks'); put(60, W + 2, 29, 'polished_blackstone_bricks')
    B.sign(60, W + 2, 28, 'dark_oak_wall_sign[facing=north,waterlogged=false]', ["STEELWHISKER'S", 'Specialist', 'Armor Sets', '(3 tiers)'], color='light_gray', glow=True)
    for (x, z) in [(58, 25), (64, 21), (63, 26)]:            # steam vents: grates over a hot pit
        put(x, GF - 1, z, 'magma_block'); put(x, GF, z, 'iron_trapdoor[facing=north,half=top,open=false,powered=false,waterlogged=false]')
    for (x, z) in [(58, 21), (65, 30)]:
        for y in range(W + 4, W + 8): put(x, y, z, 'iron_chain[axis=y,waterlogged=false]')
        put(x, W + 3, z, 'lava_cauldron')                         # hanging crucibles
    put(67, W + 2, 24, 'polished_blackstone_bricks')
    B.sign(66, W + 2, 24, 'dark_oak_wall_sign[facing=west,waterlogged=false]', ['DANGER', 'HOT FLOOR', 'Mind the vents.', '- mgmt'], color='red', glow=True)

    # ---------------------------------------------------------------- THE GNAWED FLAGON (east, middle): Chef Fromage's tavern
    tx1, tz1, tx2, tz2 = 54, 37, 72, 55
    carve_room(tx1, W, tz1, tx2 - 1, W + 7, tz2, floor='spruce_planks')
    for x in range(tx1, tx2):
        for z in range(tz1, tz2 + 1): put(x, GF, z, 'spruce_planks' if (x + z) % 5 else 'stripped_spruce_log[axis=x]')
    for z in range(tz1 + 1, tz2): put(70, W, z, 'barrel[facing=west,open=false]') if z % 3 else put(70, W, z, 'smoker[facing=west,lit=true]')
    for z in range(tz1 + 1, tz2): put(68, W, z, 'stripped_spruce_log[axis=z]'); put(68, W + 1, z, 'spruce_slab[type=bottom,waterlogged=false]')
    for z in (40, 50): put(69, W, z, 'campfire[facing=west,lit=true,signal_fire=false,waterlogged=false]')
    for (x, z) in [(68, 41), (68, 44), (68, 48)]: put(x, W + 1, z, 'honeycomb_block')       # cheese wheels on the bar (2.20: sat on the slab's air gap)
    for (x, z) in [(70, 42), (70, 46), (70, 52)]: put(x, W + 1, z, 'honeycomb_block')
    for (cx, cz) in [(58, 41), (58, 47), (63, 44), (63, 51)]:   # tables and stools
        put(cx, W, cz, 'dark_oak_fence'); put(cx, W + 1, cz, 'dark_oak_pressure_plate[powered=false]')
        put(cx - 1, W, cz, 'spruce_slab[type=bottom,waterlogged=false]'); CUSHIONS.append((cx - 1, W, cz, 'brown'))     # 2.13: cushioned stools
        put(cx + 1, W, cz, 'spruce_slab[type=bottom,waterlogged=false]'); CUSHIONS.append((cx + 1, W, cz, 'brown'))
    for (x, z) in [(60, 39), (65, 47), (60, 53)]: put(x, W + 5, z, 'lantern[hanging=true,waterlogged=false]'); put(x, W + 6, z, 'iron_chain[axis=y,waterlogged=false]')
    for y in range(W, W + 6):
        for z in (tz1, tz2): put(tx1, y, z, 'stripped_spruce_log[axis=y]')
    for x in range(tx1, 73):
        for y in range(W, W + 9):
            for z in (tz1 - 1, tz2 + 1): put(x, y, z, 'mud_bricks' if y < W + 8 else 'dark_oak_planks')
        for z in range(tz1 - 1, tz2 + 2): put(x, W + 8, z, 'dark_oak_planks')
    for z in range(tz1, tz2 + 1):
        for y in range(W, W + 8): put(72, y, z, 'mud_bricks')
        put(tx1, W + 7, z, 'stripped_spruce_log[axis=z]')
    B.sign(tx1, W + 6, 46, 'spruce_hanging_sign[attached=false,rotation=4,waterlogged=false]', ['THE GNAWED', 'FLAGON', 'Chef Fromage', 'cooks today'], color='orange', glow=True)

    # ---------------------------------------------------------------- THE BLOOD ALCOVE (east, south)
    bx1, bz1, bx2, bz2 = 54, 59, 70, 76
    carve_room(bx1 + 1, W, bz1, bx2, W + 6, bz2, floor='red_nether_bricks')
    for x in range(bx1, bx2 + 1):
        for z in range(bz1, bz2 + 1): put(x, GF, z, 'red_nether_bricks' if (x * 3 + z) % 5 else 'nether_bricks')
    for x in range(bx1, bx2 + 2):
        for y in range(W, W + 8):
            for z in (bz1 - 1, bz2 + 1): put(x, y, z, 'red_nether_bricks')
        for z in range(bz1 - 1, bz2 + 2): put(x, W + 7, z, 'red_nether_bricks')
    for z in range(bz1, bz2 + 1):
        for y in range(W, W + 7): put(bx2 + 1, y, z, 'red_nether_bricks')
    for z in range(bz1, bz2 + 1):                             # the front: pillars, and the raised portcullis in the arch
        if z in (bz1, bz2):
            for y in range(W, W + 7): put(bx1, y, z, 'red_nether_bricks')
        else:
            for y in range(W, W + 5): air(bx1, y, z)
            put(bx1, W + 5, z, 'iron_bars'); put(bx1, W + 6, z, 'iron_bars')
    counter([(x, 72) for x in range(59, 67)], top='red_nether_bricks')
    for (x, st) in [(59, 'crying_obsidian'), (61, 'chest[facing=north,type=single,waterlogged=false]'), (63, 'crying_obsidian'),
                    (64, 'brewing_stand[has_bottle_0=true,has_bottle_1=false,has_bottle_2=true]'), (66, 'crying_obsidian')]:
        put(x, W, 75, st)
    for (x, z) in [(58, 63), (66, 64), (62, 67)]:            # hanging cages with bones
        for y in range(W + 5, W + 7): put(x, y, z, 'iron_chain[axis=y,waterlogged=false]')
        put(x, W + 3, z, 'iron_bars'); put(x, W + 4, z, 'iron_bars'); put(x, W + 2, z, 'soul_lantern[hanging=true,waterlogged=false]')   # 2.20: a lantern hangs under the cage (the skull floated)
    for (x, z) in [(57, 61), (60, 66), (63, 62), (65, 69), (58, 70)]: put(x, W, z, 'redstone_wire[east=none,north=none,power=0,south=none,west=none]')   # blood
    for z in (61, 66, 71): put(bx2, W + 2, z, 'redstone_wall_torch[facing=west,lit=true]')
    for x in (57, 67): put(x, W, 60, 'red_candle[candles=3,lit=true,waterlogged=false]')
    for (x, z) in [(56, 74), (68, 74)]:
        for y in range(W, W + 4): put(x, y, z, 'crimson_stem[axis=y]')
        put(x, W + 4, z, 'shroomlight')
    B.sign(bx1 - 1, W + 2, bz1, 'crimson_wall_sign[facing=west,waterlogged=false]', ['THE', 'BLOODBROKER', 'Crystals bought', '& sold'], color='red', glow=True)
    B.sign(bx2, W + 1, 68, 'crimson_wall_sign[facing=west,waterlogged=false]', ['DEBTORS:', 'B. West', 'Gerald (ear)', 'You?'], color='red')

    # ---------------------------------------------------------------- the BALCONY, twin stairs, vault door, vestibule, tunnel (south)
    for x in range(30, 47):
        for z in range(71, 82):
            put(x, BF, z, 'dark_oak_planks' if (x + z) % 4 else 'polished_blackstone_bricks')
            for y in range(GF, BF):
                if z >= 74 or x in (30, 46): put(x, y, z, 'polished_blackstone_bricks' if y > W else pick(SPRING_SAFE))
            for y in range(BF + 1, BF + 5): air(x, y, z)
    for x in range(33, 44): put(x, BF + 1, 71, 'dark_oak_fence')
    for x in range(32, 46, 3): put(x, BF - 1, 71, 'lantern[hanging=true,waterlogged=false]')   # 1.19: under the balcony edge (z70 hung from nothing)
    for side in (0, 1):                                       # twin stairs: down from the balcony edge (z71, y17) north to z63 (y10)
        xs = (30, 31, 32) if side == 0 else (44, 45, 46)
        for k in range(7):
            z = 70 - k
            y = BF - 1 - k
            for x in xs:
                put(x, y, z, 'polished_blackstone_brick_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]')
                for yy in range(GF, y): put(x, yy, z, 'polished_blackstone_bricks')
                for yy in range(y + 1, y + 4): air(x, yy, z)
        for x in xs: put(x, BF, 71, 'dark_oak_planks')
    # vault door (3x3 iron, opened by bm:market/door) in a chiseled frame, then the vestibule and the dig-in tunnel
    for x in range(35, 42):
        for y in range(BF, BF + 6):
            for z in (82, 83): put(x, y, z, 'chiseled_deepslate')
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

    # ---------------------------------------------------------------- rooflines and vertical detail
    for x in range(lx1, lx2 + 1):                            # Lucky Den: a marquee of bulbs round the roof edge
        for z in range(lz1, lz2 + 1):
            if x in (lx1, lx2) or z in (lz1, lz2):
                put(x, W + 7, z, 'waxed_copper_bulb[lit=true,powered=false]' if (x + z) % 2 else 'gold_block')
    for x in range(lx1 + 4, lx2 - 3):
        put(x, W + 8, lz1, 'gold_block' if x % 2 else 'waxed_copper_bulb[lit=true,powered=false]')
    for x in range(tx1, 73):                                  # Gnawed Flagon: eaves, a brick chimney
        for z in (tz1 - 1, tz2 + 1):
            put(x, W + 9, z, 'dark_oak_stairs[facing=%s,half=bottom,shape=straight,waterlogged=false]' % ('south' if z == tz1 - 1 else 'north'))
    for z in range(tz1 - 1, tz2 + 2): put(tx1 - 1, W + 8, z, 'dark_oak_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]')
    for y in range(W + 9, W + 12):
        for (x, z) in ((69, 40), (70, 40), (69, 41), (70, 41)): put(x, y, z, 'bricks')
    put(69, W + 12, 40, 'campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]')
    for x in range(bx1, bx2 + 2):                             # Blood Alcove: battlements with iron spikes
        for z in range(bz1 - 1, bz2 + 2):
            if (x in (bx1, bx2 + 1) or z in (bz1 - 1, bz2 + 1)) and (x + z) % 2 == 0:
                put(x, W + 8, z, 'red_nether_bricks'); put(x, W + 9, z, 'iron_bars')
    for (x, z) in [(50, 62), (50, 72)]:                       # gibbet cages hanging outside the Alcove
        hang_y = W + 4
        t = ceil.get((x, z))
        if t:
            for y in range(hang_y + 3, t + 1): put(x, y, z, 'iron_chain[axis=y,waterlogged=false]')
            put(x, hang_y + 2, z, 'iron_bars'); put(x, hang_y + 1, z, 'iron_bars'); put(x, hang_y, z, 'iron_bars')
            put(x, hang_y + 1, z, 'skeleton_skull[powered=false,rotation=%d]' % rnd.randrange(16))
    for i, x in enumerate(range(27, 52, 4)):                  # banners on the terrace posts, over the alley
        if (x, W + 5, 21) in B.b and 'log' in B.b[(x, W + 5, 21)]:
            put(x, W + 5, 22, ['red', 'black', 'purple', 'black'][i % 4] + '_wall_banner[facing=south]')
    for x in range(26, 49):                                   # festoon lanterns strung over Pawn Alley
        put(x, W + 6, 24, 'iron_chain[axis=y,waterlogged=false]' if x % 3 == 0 else 'iron_chain[axis=x,waterlogged=false]')   # a lantern needs an upright link
        if x % 3 == 0: put(x, W + 5, 24, 'lantern[hanging=true,waterlogged=false]')
    for y in range(W, W + 7): put(25, y, 24, 'polished_blackstone_wall'); put(48, y, 24, 'polished_blackstone_wall') if y < W + 6 else None
    put(48, W + 6, 24, 'polished_blackstone_bricks'); put(25, W + 6, 24, 'polished_blackstone_bricks')

    # ---------------------------------------------------------------- dome dressing: chandeliers, dripstone, spore blossoms
    def hang(x, z, bottom, light='lantern[hanging=true,waterlogged=false]'):
        t = ceil.get((x, z))
        if t is None or t <= bottom + 1: return
        for y in range(bottom + 1, t + 1): put(x, y, z, 'iron_chain[axis=y,waterlogged=false]')
        put(x, bottom, z, light)
    for (x, z, b) in [(32, 40, 19), (44, 40, 19), (32, 52, 19), (44, 52, 19), (38, 60, 21), (38, 32, 22), (21, 30, 16), (21, 55, 16),
                      (12, 44, 16), (64, 36, 17), (62, 58, 17), (48, 66, 19)]:
        hang(x, z, b)
    open_ceiling = [(x, z) for (x, z) in ceil if (x, ceil[(x, z)], z) in B.b and B.b[(x, ceil[(x, z)], z)] == 'minecraft:air']
    for (x, z) in open_ceiling:
        t = ceil[(x, z)]
        if (x, t + 1, z) not in ROCK: continue
        r = rnd.random()
        if r < 0.05:
            n = rnd.choice((1, 2, 2, 3))
            seq = {1: ['tip'], 2: ['frustum', 'tip'], 3: ['base', 'frustum', 'tip']}[n]
            if all((x, t - i, z) in B.b and B.b[(x, t - i, z)] == 'minecraft:air' for i in range(n)) and t - n > BF + 3:
                for i, th in enumerate(seq): put(x, t - i, z, f'pointed_dripstone[thickness={th},vertical_direction=down,waterlogged=false]')
        elif r < 0.07:
            put(x, t, z, 'spore_blossom')

    # ---------------------------------------------------------------- skin: every rock face touching open space is spring-safe
    OPEN = ('minecraft:air', 'minecraft:water[level=0]', 'minecraft:lava[level=0]')
    for (x, y, z) in list(ROCK):
        for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            n = B.b.get((x + dx, y + dy, z + dz))
            if n is not None and (x + dx, y + dy, z + dz) not in ROCK and (n in OPEN or not is_full(n)):
                S(x, y, z, pick(SPRING_SAFE)); break
    # glow lichen on the walls near the floor (placed by us: the skin stops worldgen lichen)
    for (x, y, z) in list(ROCK):
        if not (W + 1 <= y <= W + 7) or rnd.random() > 0.06: continue
        for d, (dx, dz) in {'east': (-1, 0), 'west': (1, 0), 'south': (0, -1), 'north': (0, 1)}.items():
            ax, az = x + dx, z + dz
            if B.b.get((ax, y, az)) == 'minecraft:air' and (ax, y, az) not in ROCK:
                props = {k: 'false' for k in ('down', 'east', 'north', 'south', 'up', 'west', 'waterlogged')}
                props[d] = 'true'
                put(ax, y, az, 'glow_lichen[' + ','.join(f'{k}={v}' for k, v in sorted(props.items())) + ']')
                break

    # ---------------------------------------------------------------- markers
    M = B.marker
    # traders (same kinds as the 1.7 market, so every existing system finds them)
    M(44.5, W, 17.5, ['bm.npc_spawn', 'bm.npc.fence'], 0)
    M(29.5, W, 17.5, ['bm.npc_spawn', 'bm.npc.pawn'], 0)
    M(30.5, W, 30.5, ['bm.npc_spawn', 'bm.npc.outfitter'], 180)
    M(3.5, W, 17.5, ['bm.npc_spawn', 'bm.npc.captain'], 0)       # secret: behind the mouse hole (Minish Cap)
    M(8.5, W, 69.5, ['bm.npc_spawn', 'bm.npc.lucky'], 180)           # 1.16: in front of his counter (a rat hides behind it)
    M(57.5, W, 21.5, ['bm.npc_spawn', 'bm.npc.arms'], -90)
    M(59.5, W, 31.5, ['bm.npc_spawn', 'bm.npc.armory'], 180)
    M(67.5, W, 44.5, ['bm.npc_spawn', 'bm.npc.chef'], 90)            # 1.16: in front of the bar
    M(62.5, W, 74.5, ['bm.npc_spawn', 'bm.npc.blood'], 180)
    M(30.5, BF + 1, 19.5, ['bm.npc_spawn', 'bm.npc.professor'], -90)
    M(CX + 2.5, 7.2, CZ + 0.5, ['bm.npc_spawn', 'bm.npc.mike'], 0)
    M(2.5, W, 14.5, ['bm.npc_spawn', 'bm.npc.deco_rat'], 0)
    M(5.5, W, 15.5, ['bm.npc_spawn', 'bm.npc.deco_rat'], 0)
    # market fx (p18 uses mfx ~7 above the floor, and mfx2 must sit IN Mike's pond - he swims home to it)
    M(CX + 0.5, W + 7, CZ + 0.5, ['bm.mfx'], 0)
    M(CX - 2.5, 7.5, CZ - 1.5, ['bm.mfx2'], 0)
    # key door, exit, guard/zone/market control markers
    M(38.5, BF + 2.0, 82.5, ['bm.market_door'], 0)
    M(38.5, BF + 1, 88.5, ['bm.market_exit'], 0)
    for (x, y, z) in [(38, W + 2, 46), (20, W + 2, 46), (58, W + 2, 46), (38, W + 2, 22), (38, BF + 2, 76), (10, W + 2, 26), (10, W + 2, 62),
                      (62, W + 2, 25), (62, W + 2, 67), (38, W + 2, 8), (55, BF + 2, 8), (38, BF + 2, 17)]:
        M(x + 0.5, y, z + 0.5, ['bm.market_hall', 'bm.zone_m'], 0)
    M(CX + 0.5, W + 2, CZ + 0.5, ['bm.mkt'], 0)
    # neon signs (text displays, spawned by phase23)
    for (x, y, z, yaw, nid) in [(10.5, W + 6.6, lz1 - 0.45, 180, 'lucky'), (38.5, BF + 5.2, 70.6, 0, 'welcome'), (tx1 - 0.45, W + 6.0, 46.5, 90, 'flagon'),
                                (fx1 + 0.5, W + 6.5, 25.5, 90, 'forge'), (bx1 - 0.45, W + 7.0, 67.5, 90, 'blood'), (37.5, W + 5.4, 14.6, 0, 'auction'),
                                (46.5, BF + 4.4, 15.3, 0, 'vip'), (12.6, W + 6.0, 26.5, -90, 'docks'), (38.5, BF + 1.5, 22.0, 0, 'alley')]:
        M(x, y, z, ['bm.npc_spawn', 'bm.npc.neon', f'bm.neon_{nid}'], yaw)
    # the crowd (static, they idle-animate and watch you) - variant tag picks the outfit
    crowd = [(57.5, W, 41.5, 90, 'pirate'), (59.5, W, 41.5, -90, 'prof'), (62.5, W, 44.5, 90, 'lucky'), (64.5, W, 51.5, -90, 'chef'),
             (62.5, W, 51.5, 90, 'pirate'), (66.5, W, 47.5, 90, 'soldier'),                        # tavern regulars
             (8.5, W, 57.5, 0, 'lucky'), (10.5, W, 57.5, 0, 'pirate'), (11.5, W, 61.5, 90, 'prof'),     # card sharps
             (12.5, W, 52.5 - 1.2, 180, 'soldier'),                                                     # Den bouncer (outside)
             (34.5, BF + 1, 72.5, 180, 'soldier'), (42.5, BF + 1, 72.5, 180, 'soldier'),                # balcony guards
             (27.5, BF + 1, 20.5, 180, 'soldier'),                                                      # terrace watch
             (20.5, WATER_TOP + 2, 27.5, -90, 'pirate'), (15.5, W, 21.5, 0, 'pirate'),                        # dock hands (2.13: the Dockmaster trades)
             (bx + 0.5, W + 1, bz + 0.5, 180, 'lucky'),                                                 # the busker
             (63.5, W, 23.5, 90, 'soldier')]                                                            # forge hand (1.17: the Void Rat customer is gone - Void Rats are End-only finds)
    for (x, y, z, yaw, v) in crowd:
        st = B.b.get((int(x // 1), int(y // 1), int(z // 1)), '')
        if ('stairs' in st and 'half=bottom' in st) or ('slab' in st and 'type=bottom' in st): y += 0.5     # 1.16: sit ON the seat, not inside it
        M(x, y, z, ['bm.npc_spawn', 'bm.npc.crowd', f'bm.cv_{v}'], yaw)
    M(bx + 0.5, W + 1, bz + 0.5, ['bm.busker'], 0)
    for (x, y, z) in AUCTION_SEATS: CUSHIONS.append((x, y, z, 'red'))
    for (x, y, z, col) in CUSHIONS:                                  # 2.13: cushion seats (26.3 entities)
        st = B.b.get((x, y, z), '')
        M(x + 0.5, y + (0.5 if 'slab' in st and 'type=bottom' in st else 0.0), z + 0.5, ['bm.npc_spawn', 'bm.npc.cushion', f'bm.cu_{col}'], 0)
    # walkers + their routes (waypoints by index)
    routes = {'a': [(round(CX + 8.5 * math.cos(k * math.pi / 4)), round(CZ + 8.5 * math.sin(k * math.pi / 4))) for k in range(8)],          # round the fountain
              'b': [(27, 24), (47, 24)],                                                  # Pawn Alley
              'c': [(10, 38), (10, 49)]}                                                  # the far bank
    for rid, pts in routes.items():
        for i, (x, z) in enumerate(pts):
            M(x + 0.5, W, z + 0.5, ['bm.wp', f'bm.route_{rid}', f'bm.wpi_{i}'], 0)
        x, z = pts[0]
        M(x + 0.5, W, z + 0.5, ['bm.npc_spawn', 'bm.npc.walker', f'bm.route_{rid}', 'bm.cv_' + {'a': 'chef', 'b': 'pirate', 'c': 'lucky'}[rid]], 0)
    # steam vents, mouse holes, ambience emitters
    for (x, z) in [(58, 25), (64, 21), (63, 26)]: M(x + 0.5, W, z + 0.5, ['bm.vent'], 0)
    # mouse holes: a 1x1 notch at the foot of a built wall (decoration)
    for (hole, front) in HOLES:
        hx, hz = hole; fx_, fz_ = front
        st = B.b.get((hx, W, hz)); fl = B.b.get((fx_, GF, fz_))
        if not st or not is_full(st): raise RuntimeError(f'rat hole {hole}: no wall there ({st})')
        if B.b.get((fx_, W, fz_)) != 'minecraft:air' or not fl or not spawn_surface(fl): raise RuntimeError(f'rat hole {hole}: front {front} not open floor')
        put(hx, W, hz, 'air')                                # (1.13.1: just a mouse hole now - no pickpockets)
    for (x, y, z, k) in [(CX, W + 2, CZ, 'plaza'), (60, W + 2, 24, 'forge'), (62, W + 2, 46, 'tavern'), (61, W + 2, 67, 'blood'),
                         (10, W + 2, 62, 'den'), (14, W + 2, 28, 'docks'), (38, W + 2, 24, 'alley')]:
        M(x + 0.5, y, z + 0.5, ['bm.amb', f'bm.amb_{k}'], 0)

    support_lanterns(B, put)
    # ---------------------------------------------------------------- light: every walkable cell gets >= 2 (spawn-proof)
    lights = spawnproof(B, fix=True, forbid=DOOR_BOX)
    B.meta = {'lights_added': lights, 'ceil': ceil}
    return B


LANTERN = ('minecraft:lantern', 'minecraft:soul_lantern', 'minecraft:copper_lantern', 'minecraft:waxed_copper_lantern')


def holds_from_above(st):
    """Can a hanging lantern hang under this block? (its bottom face must cover the block's centre)"""
    if not st: return False
    n = st.split('[')[0]
    if is_full(st): return True
    if n.endswith('_chain') and 'axis=y' in st: return True
    if n.endswith('_slab') and 'type=top' not in st: return True
    if n.endswith('_stairs') and 'half=bottom' in st: return True
    return n.endswith(('_fence', '_wall', 'iron_bars'))


def holds_from_below(st):
    """Can a standing lantern stand on this block? (its top face must cover the centre)"""
    if not st: return False
    n = st.split('[')[0]
    if is_full(st): return True
    if n.endswith('_chain') and 'axis=y' in st: return True
    if n.endswith('_slab') and 'type=bottom' not in st: return True
    if n.endswith('_stairs') and 'half=top' in st: return True
    return n.endswith(('_fence', '_wall', 'iron_bars'))


def support_lanterns(B, put, reach=4):
    """1.19: every lantern must be held up, or the first block update in the market drops it as an item (26.3's
    /place template updates every block, so placing a market knocked down all 23 that hung from air or a sideways chain).
    A hanging lantern with open air above gets an upright chain up to the nearest solid block (at most `reach` links)."""
    for (x, y, z), st in sorted(B.b.items()):
        if st.split('[')[0] not in LANTERN: continue
        if 'hanging=true' in st:
            if holds_from_above(B.b.get((x, y + 1, z))): continue
            k = 1
            while k <= reach and B.b.get((x, y + k, z)) == 'minecraft:air': k += 1
            if k > reach or not holds_from_above(B.b.get((x, y + k, z))):
                raise RuntimeError(f'hanging lantern at {(x, y, z)} has nothing to hang from (above: {B.b.get((x, y + 1, z))})')
            for j in range(1, k): put(x, y + j, z, 'iron_chain[axis=y,waterlogged=false]')
        elif not holds_from_below(B.b.get((x, y - 1, z))):
            raise RuntimeError(f'standing lantern at {(x, y, z)} has nothing under it ({B.b.get((x, y - 1, z))})')


def is_full(st):
    from structures import NOT_SOLID
    n = st.split(':', 1)[-1].split('[')[0]
    if NOT_SOLID.search(n): return False
    return not any(k in n for k in ('glass', 'leaves', 'bars', 'chain', 'dripstone', 'spore', 'lichen', 'end_rod', 'lever', 'wire',
                                     'skull', 'brewing', 'pad'))


def spawn_surface(st):
    """Can a monster stand on top of this block? (full blocks, top slabs, upside-down stairs, closed top trapdoors)"""
    n = st.split(':', 1)[-1].split('[')[0]
    if 'slab' in n: return 'type=top' in st or 'type=double' in st
    if 'stairs' in n: return 'half=top' in st
    if 'trapdoor' in n: return 'half=top' in st and 'open=false' in st
    return is_full(st)


def light_map(B):
    """Block light (BFS from emitters; full blocks stop it)."""
    from collections import deque
    L = {}
    q = deque()
    for p, st in B.b.items():
        n = st.split(':', 1)[-1].split('[')[0]
        lv = EMIT.get(n)
        if n == 'light':
            lv = int(st.split('level=')[1].split(']')[0].split(',')[0])
        if n in ('campfire', 'soul_campfire', 'furnace', 'smoker', 'blast_furnace', 'redstone_lamp', 'waxed_copper_bulb', 'redstone_wall_torch') and 'lit=false' in st:
            lv = None
        if n.endswith('candle') and 'lit=true' in st:
            lv = 3 * int(st.split('candles=')[1][0])
        if lv:
            L[p] = lv; q.append(p)
    while q:
        p = q.popleft(); lv = L[p] - 1
        if lv <= 0: continue
        x, y, z = p
        for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            n = (x + d[0], y + d[1], z + d[2])
            st = B.b.get(n)
            if st is None or is_full(st): continue
            if L.get(n, 0) < lv:
                L[n] = lv; q.append(n)
    return L


def walkable(B):
    """Cells a mob could stand in: open (not full) cell, not liquid, with a full block under it, inside the build."""
    out = []
    for (x, y, z), st in B.b.items():
        if is_full(st) or 'water' in st or 'lava' in st: continue
        below = B.b.get((x, y - 1, z))
        if below and spawn_surface(below):
            out.append((x, y, z))
    return out


def spawnproof(B, fix=False, need=2, forbid=frozenset()):
    """Every walkable cell must have block light >= need. With fix=True, invisible light blocks are added at the darkest
    open cells (one above the floor) until that holds; returns how many were added."""
    added = 0
    for _ in range(12):
        L = light_map(B)
        dark = [p for p in walkable(B) if L.get(p, 0) < need]
        if not dark: return added
        if not fix: return dark
        todo = sorted(dark)
        while todo:
            x, y, z = todo[0]
            spot = (x, y + 1, z) if B.b.get((x, y + 1, z)) == 'minecraft:air' else (x, y, z)
            if B.b.get(spot) != 'minecraft:air' or spot in forbid:
                spot = next(((x + dx, y + dy, z + dz) for dx in (-2, -1, 0, 1, 2) for dy in (0, 1, 2) for dz in (-2, -1, 0, 1, 2)
                             if B.b.get((x + dx, y + dy, z + dz)) == 'minecraft:air' and (x + dx, y + dy, z + dz) not in forbid), None)
                if spot is None: raise RuntimeError(f'no air to light dark cell {(x, y, z)}')
            B.set(*spot, 'light[level=8,waterlogged=false]'); added += 1
            todo = [q for q in todo if abs(q[0] - spot[0]) + abs(q[1] - spot[1]) + abs(q[2] - spot[2]) > 5]
    raise RuntimeError('spawnproof: could not light the market')


def check(B):
    """Static proofs for the new market (run at build): returns a list of problems.
    - every trader, the busker and every crowd rat on the floor can be walked to from the vault (door open);
    - nothing flammable is within reach of lava (lava lights fire up to 3 blocks across and 4 up);
    - no walkable cell is dark (block light >= 2), so nothing spawns even without the structure's spawn rules;
    - no lava or water touches a cell outside the market (no leaks into natural caves)."""
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
        if 'bm.npc.crowd' in t and y < W: continue
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
    # sealed: no open cell touches the world outside the template, except the end of the dig-in tunnel
    for (x, y, z), st in B.b.items():
        if is_full(st) or (37 <= x <= 39 and z == SZ - 1): continue
        for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            if (x + d[0], y + d[1], z + d[2]) not in B.b: errs.append(f'open cell {(x, y, z)} {st} touches the world outside the market'); break
    for (hx, hz), _ in HOLES:
        if B.b.get((hx, W, hz)) != 'minecraft:air': errs.append(f'mouse hole {(hx, hz)} missing')
    # the Captain is secret: unreachable at full size, through a half-block mouse hole into his den
    cap = next(e['pos'] for e in B.ents if 'bm.npc.captain' in e['nbt']['Tags'])
    if reach(seen, int(cap[0]), int(cap[1]), int(cap[2]), 2.5): errs.append('the Captain can be reached without shrinking')
    if not (B.b.get((4, W, 20), '').startswith('minecraft:deepslate_brick_slab[type=top') and B.b.get((4, W, 21), '').startswith('minecraft:deepslate_brick_slab[type=top')):
        errs.append('the mouse hole is not a half-block gap')
    for p in DOOR_BOX:
        if B.b.get(p, '').startswith('minecraft:light'): errs.append(f'light block {p} inside the vault door fill box')
    return sorted(set(errs))

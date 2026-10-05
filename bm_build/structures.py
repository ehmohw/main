"""Structure templates for the Black Market and the Haunted Graveyard/Crypt.
Coordinates are template-local. Yaw: 0=south(+z), 90=west(-x), 180=north(-z), -90=east(+x)."""
import random, re
from nbt import Int, Float, Double, Byte, IntArray, write_nbt_gz
from items import GRAVE_BOOK

DATA_VERSION = 4903  # Java 26.2

MARKET_FLOOR = ['minecraft:spruce_stairs', 'minecraft:spruce_slab', 'minecraft:dark_oak_slab', 'minecraft:chiseled_polished_blackstone',
                'minecraft:polished_blackstone_bricks', 'minecraft:polished_blackstone', 'minecraft:gilded_blackstone',
                'minecraft:red_carpet', 'minecraft:purple_carpet', 'minecraft:black_carpet', 'minecraft:yellow_carpet',
                'minecraft:gold_block', 'minecraft:dark_oak_planks', 'minecraft:spruce_planks', 'minecraft:chiseled_polished_blackstone',
                'minecraft:cracked_polished_blackstone_bricks', 'minecraft:stripped_dark_oak_log', 'minecraft:stripped_spruce_log',
                'minecraft:crimson_planks', 'minecraft:polished_andesite', 'minecraft:red_nether_bricks']
CRYPT_FLOOR = ['minecraft:deepslate_tile_slab', 'minecraft:deepslate_brick_slab', 'minecraft:polished_deepslate_slab',
               'minecraft:cobbled_deepslate_slab', 'minecraft:polished_deepslate', 'minecraft:deepslate_tiles', 'minecraft:cracked_deepslate_tiles',
               'minecraft:deepslate_bricks', 'minecraft:sculk', 'minecraft:gravel', 'minecraft:gray_carpet',
               'minecraft:deepslate_brick_stairs', 'minecraft:chiseled_deepslate', 'minecraft:dark_oak_trapdoor',
               'minecraft:cobbled_deepslate']

_STATE = re.compile(r'^([a-z0-9_:]+)(?:\[(.*)\])?$')


def parse_state(s):
    m = _STATE.match(s)
    name = m.group(1)
    if ':' not in name: name = 'minecraft:' + name
    props = {}
    if m.group(2):
        for kv in m.group(2).split(','):
            k, v = kv.split('=')
            props[k.strip()] = v.strip()
    return name, props


def state_str(name, props):
    if not props: return name
    return name + '[' + ','.join(f'{k}={v}' for k, v in sorted(props.items())) + ']'


FENCES = re.compile(r'fence$|fence_gate$')
WALLS = re.compile(r'_wall$')
PANES = re.compile(r'iron_bars$|_pane$')
NOT_SOLID = re.compile(r'air$|light$|carpet|slab|stairs|lantern|candle|torch|skull|sign|banner|trapdoor|ladder|button|'
                       r'pressure_plate|fence|_wall$|iron_bars|cobweb|dead_bush|fern|water|lava|cake|pot|chest|lectern|'
                       r'campfire|cauldron|anvil|grindstone|bell|enchanting|bubble|flower|sapling|bed$|rail|door|structure_void')


class Build:
    def __init__(self, sx, sy, sz):
        self.size = (sx, sy, sz)
        self.b = {}
        self.nbt = {}
        self.ents = []

    def set(self, x, y, z, state, nbt=None):
        sx, sy, sz = self.size
        if not (0 <= x < sx and 0 <= y < sy and 0 <= z < sz):
            raise ValueError(f'out of bounds {x},{y},{z} {state}')
        if not state.startswith('minecraft:'): state = 'minecraft:' + state
        self.b[(x, y, z)] = state
        if nbt is not None:
            self.nbt[(x, y, z)] = nbt
        elif (x, y, z) in self.nbt:
            del self.nbt[(x, y, z)]

    def get(self, x, y, z):
        return self.b.get((x, y, z))

    def fill(self, x1, y1, z1, x2, y2, z2, state):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    self.set(x, y, z, state)

    def room(self, x1, y1, z1, x2, y2, z2, wall, floor=None, ceil=None, inner='air'):
        """Walls on the box shell, air inside."""
        self.fill(x1, y1, z1, x2, y2, z2, inner)
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1):
                self.set(x, y1, z, floor or wall)
                self.set(x, y2, z, ceil or wall)
        for y in range(y1 + 1, y2):
            for x in range(x1, x2 + 1):
                self.set(x, y, z1, wall); self.set(x, y, z2, wall)
            for z in range(z1, z2 + 1):
                self.set(x1, y, z, wall); self.set(x2, y, z, wall)

    def marker(self, x, y, z, tags, yaw=0.0):
        self.ents.append({'pos': [Double(x), Double(y), Double(z)],
                          'blockPos': [Int(int(x // 1)), Int(int(y // 1)), Int(int(z // 1))],
                          'nbt': {'id': 'minecraft:marker', 'Tags': list(tags),
                                  'Rotation': [Float(yaw), Float(0.0)], 'data': {}}})

    def sign(self, x, y, z, state, lines, color='black', glow=False):
        msgs = [{'text': l} for l in (list(lines) + ['', '', '', ''])[:4]]
        side = {'messages': msgs, 'color': color, 'has_glowing_text': Byte(1 if glow else 0)}
        empty = {'messages': [{'text': ''}] * 4, 'color': 'black', 'has_glowing_text': Byte(0)}
        sid = 'minecraft:hanging_sign' if 'hanging' in state else 'minecraft:sign'
        self.set(x, y, z, state, {'id': sid, 'front_text': side, 'back_text': empty, 'is_waxed': Byte(1)})

    def connect(self):
        """Compute fence/wall/bars side connections."""
        dirs = {'north': (0, -1), 'south': (0, 1), 'east': (1, 0), 'west': (-1, 0)}
        for (x, y, z), st in list(self.b.items()):
            name, props = parse_state(st)
            short = name.split(':')[1]
            kind = 'fence' if (short.endswith('_fence') and 'gate' not in short) else \
                   'wall' if short.endswith('_wall') and 'sign' not in short and 'banner' not in short and 'torch' not in short and 'skull' not in short and 'head' not in short and 'fan' not in short else \
                   'bars' if (short == 'iron_bars' or short.endswith('_pane')) else None
            if not kind: continue
            for d, (dx, dz) in dirs.items():
                n = self.b.get((x + dx, y, z + dz))
                c = False
                if n:
                    nn = parse_state(n)[0].split(':')[1]
                    if kind == 'fence': c = nn.endswith('_fence') or nn.endswith('fence_gate')
                    elif kind == 'wall': c = nn.endswith('_wall') or nn.endswith('fence_gate')
                    else: c = nn == 'iron_bars' or nn.endswith('_pane')
                    if not c and not NOT_SOLID.search(nn): c = True
                if kind == 'wall':
                    props[d] = 'low' if c else 'none'
                else:
                    props[d] = 'true' if c else 'false'
            if kind == 'wall':
                props['up'] = 'true'
            self.b[(x, y, z)] = state_str(name, props)

    def export(self, path):
        self.connect()
        palette, pidx, blocks = [], {}, []
        for pos in sorted(self.b, key=lambda p: (p[1], p[2], p[0])):
            st = self.b[pos]
            if st not in pidx:
                pidx[st] = len(palette)
                name, props = parse_state(st)
                e = {'Name': name}
                if props: e['Properties'] = props
                palette.append(e)
            blk = {'pos': [Int(pos[0]), Int(pos[1]), Int(pos[2])], 'state': Int(pidx[st])}
            if pos in self.nbt:
                blk['nbt'] = self.nbt[pos]
            blocks.append(blk)
        root = {'DataVersion': Int(DATA_VERSION), 'size': [Int(s) for s in self.size],
                'palette': palette, 'blocks': blocks, 'entities': self.ents}
        write_nbt_gz(path, root)
        return len(blocks), len(palette)


def book_nbt(title, author, pages):
    return {'id': 'minecraft:written_book', 'count': Int(1),
            'components': {'minecraft:written_book_content': {'title': title, 'author': author, 'pages': pages}}}


# =====================================================================
#  HAUNTED GRAVEYARD + CRYPT (31 x 27 x 62). Ground level = y17
# =====================================================================
def build_graveyard():
    rnd = random.Random(4242)
    SX, SY, SZ = 31, 32, 65
    B = Build(SX, SY, SZ)
    G = 17
    # solid foundation under the whole footprint (v1.9): the template used to stop 1 block below the grass, so on
    # cliffs/riverbanks the yard hung in the air. Now every column is soil over stone right down to the template floor;
    # the crypt and catacombs below are carved out of this afterwards. Own RNG so the rest of the layout is unchanged.
    frnd = random.Random(9091)
    for x in range(SX):
        for z in range(SZ):
            for y in range(0, G - 1):
                r = frnd.random()
                if y >= G - 4: s = 'dirt' if r < 0.8 else 'coarse_dirt'
                elif y >= G - 6: s = 'dirt' if r < 0.4 else 'stone' if r < 0.85 else 'gravel'
                else: s = 'stone' if r < 0.7 else 'andesite' if r < 0.85 else 'tuff' if r < 0.95 else 'cobblestone'
                B.set(x, y, z, s)
    # ground & clearance
    for x in range(SX):
        for z in range(SZ):
            B.set(x, G - 1, z, 'dirt')
            r = rnd.random()
            B.set(x, G, z, 'dirt_path' if r < 0.55 else 'packed_mud' if r < 0.75 else 'podzol' if r < 0.9 else 'coarse_dirt')
            for y in range(G + 1, SY):
                B.set(x, y, z, 'air')
    # gravel path: gate -> the mausoleum at the back
    for z in range(1, 49):
        for x in range(14, 17):
            B.set(x, G, z, 'gravel')
    # ---------------- gothic wall: 3-high stone-brick piers with iron bars between, capped
    PIER = ['stone_bricks', 'stone_bricks', 'mossy_stone_bricks', 'cracked_stone_bricks']
    def wall_cell(x, z, pier):
        if pier:
            for y in range(G + 1, G + 4): B.set(x, y, z, rnd.choice(PIER))
            B.set(x, G + 4, z, 'stone_brick_slab[type=bottom,waterlogged=false]')
        else:
            for y in range(G + 1, G + 4): B.set(x, y, z, 'iron_bars')
    for x in range(1, 30):
        for z in (1, 60):
            if z == 1 and 13 <= x <= 17: continue
            wall_cell(x, z, x % 4 == 1 or x in (1, 29))
    for z in range(2, 60):
        for x in (1, 29):
            wall_cell(x, z, z % 4 == 0)
    # gatehouse arch over the path
    for x in (13, 17):
        for y in range(G + 1, G + 6): B.set(x, y, 1, 'polished_deepslate' if y < G + 5 else 'chiseled_stone_bricks')
        B.set(x, G + 6, 1, 'soul_lantern[hanging=false,waterlogged=false]')
    for x in range(14, 17):
        B.set(x, G + 5, 1, 'stone_bricks'); B.set(x, G + 4, 1, 'iron_bars')
    B.set(15, G + 6, 1, 'stone_brick_wall'); B.set(15, G + 7, 1, 'skeleton_skull[rotation=0,powered=false]')
    for x in (14, 16): B.set(x, G + 6, 1, 'stone_brick_slab[type=bottom,waterlogged=false]')
    B.sign(12, G + 2, 0, 'dark_oak_wall_sign[facing=north,waterlogged=false]', ['Here rest the', 'VELVET HAND', 'Rest uneasy.', ''], color='gray')
    B.set(12, G + 2, 1, 'stone_bricks')
    # warning lectern shrine
    for x, z in [(10, 5), (10, 7), (12, 5), (12, 7)]:
        B.fill(x, G + 1, z, x, G + 2, z, 'dark_oak_fence')
    B.fill(10, G + 3, 5, 12, G + 3, 7, 'dark_oak_slab[type=bottom]')
    pages = [p for p in GRAVE_BOOK['pages']]
    B.set(11, G + 1, 6, 'lectern[facing=east,has_book=true]',
          {'id': 'minecraft:lectern', 'Book': book_nbt(GRAVE_BOOK['title'], GRAVE_BOOK['author'], pages), 'Page': Int(0)})
    B.set(11, G, 6, 'polished_deepslate')
    # lantern posts along the path
    for z in (5, 13, 21, 29, 37, 45):
        for x in (13, 17):
            B.fill(x, G + 1, z, x, G + 2, z, 'dark_oak_fence'); B.set(x, G + 3, z, 'soul_lantern[hanging=false]')

    # graves (some wear a funny epitaph)
    EPITAPHS = [['RIP', "Micah's", 'Free Time', ''], ['RIP', "River's", 'Second Monitor', ''],
                ['RIP', "Emi's Ability", 'to Finish', 'Houses'], ['RIP', "Tim's Desire", 'to be Kind', ''],
                ['RIP', "Jacky's", 'Nice-Looking', 'Houses']]
    # 2.13: plenty more (each used once, so a graveyard reads like a crowd, not a loop); about half the graves stay nameless
    EPITAPHS += [['RIP', 'Steve', 'Dug Straight', 'Down'], ['Here Lies', 'Bob', 'Hugged a', 'Creeper'], ['RIP', 'My Diamonds', 'Lava Took', 'Them All'],
                 ['RIP', 'Gary', '"It\'s Just', 'One Zombie"'], ['RIP', 'Mining at 3AM', 'Was Fun.', 'Mostly.'], ['Here Lies', 'A Good Wolf', 'Best Boy', 'Forever'],
                 ['RIP', 'Elytra Pilot', 'Forgot', 'Rockets'], ['RIP', 'The Last', 'Totem', ''], ['RIP', 'Phil', 'Slept in', 'the Nether'],
                 ['RIP', 'Fall Damage', 'Victim #47', ''], ['RIP', 'Dave', 'Punched a', 'Golem'], ['RIP', 'Hardcore', 'World #12', ''],
                 ['RIP', 'Iron Pickaxe', 'Died Doing', 'What It Loved'], ['RIP', 'Sheep #3', 'It Was Pink', ''], ['Here Lies', 'Someone Who', 'Said "Watch', 'This"'],
                 ['RIP', 'The Anvil', 'Too Expensive', ''], ['RIP', 'The Warden', 'Was NOT', 'Asleep'], ['RIP', 'Larry', 'Gravel', 'Happened'],
                 ['RIP', 'Lost Map', 'Never', 'Found'], ['RIP', 'Rat Gang', 'Snitch', '(squeak)'], ['RIP', 'Bought a Fake', 'Lucky Ticket', ''],
                 ['RIP', "Didn't Read", 'the House', 'Rules'], ['RIP', 'Ate the', 'Suspicious', 'Stew']]
    epi = list(EPITAPHS)
    rnd.shuffle(epi)
    def grave(x, z, sign=None):
        k = rnd.randrange(5)
        B.set(x, G, z + 1, 'podzol'); B.set(x, G, z + 2, 'podzol')
        if rnd.random() < 0.5: B.set(x, G + 1, z + 2, 'dead_bush')
        if sign:
            B.set(x, G + 1, z, rnd.choice(['chiseled_stone_bricks', 'mossy_stone_bricks', 'cracked_stone_bricks']))
            B.set(x, G + 2, z, rnd.choice(['stone_brick_slab[type=bottom,waterlogged=false]', 'mossy_stone_brick_wall', 'skeleton_skull[rotation=0,powered=false]']))
            B.sign(x, G + 1, z - 1, 'dark_oak_wall_sign[facing=north,waterlogged=false]', sign, color='white')
            return
        if k == 0:
            B.set(x, G + 1, z, 'mossy_stone_brick_wall'); B.set(x, G + 2, z, 'skeleton_skull[rotation=0]')
        elif k == 1:
            B.set(x, G + 1, z, 'cobblestone_wall'); B.set(x, G + 2, z, 'candle[candles=1,lit=true]')
        elif k == 2:
            B.set(x, G + 1, z, 'mossy_stone_brick_wall'); B.set(x, G + 2, z, 'mossy_stone_brick_wall')
        elif k == 3:
            B.set(x, G + 1, z, 'chiseled_stone_bricks'); B.set(x, G + 2, z, 'stone_brick_slab[type=bottom]')
        else:
            B.set(x, G + 1, z, 'cracked_stone_bricks'); B.set(x, G + 1, z + 1, 'mossy_cobblestone_slab[type=bottom]')
    spots = [(x, z) for z in (4, 10, 16, 22, 28, 34, 40, 46) for x in (4, 7, 23, 26)] + \
            [(x, z) for z in (17, 23, 29, 35, 41) for x in (10, 20)] + [(4, 52), (7, 52), (23, 52), (26, 52)]
    signed = set(rnd.sample(range(len(spots)), len(epi)))
    for n, (x, z) in enumerate(spots):
        if x in (10,) and z in (4,): continue
        grave(x, z, epi.pop() if n in signed and epi else None)
    # dead tree
    B.fill(5, G + 1, 56, 5, G + 6, 56, 'dark_oak_log[axis=y]')
    B.set(6, G + 4, 56, 'dark_oak_log[axis=x]'); B.set(7, G + 5, 56, 'dark_oak_log[axis=x]')
    B.set(4, G + 5, 56, 'dark_oak_log[axis=x]'); B.set(5, G + 5, 57, 'dark_oak_log[axis=z]')
    B.set(7, G + 4, 56, 'cobweb'); B.set(3, G + 1, 57, 'skeleton_skull[rotation=3]')

    # ---------------- gothic mausoleum at the BACK of the graveyard: x10..20, z48..58 ----------------
    MX1, MX2, MZ1, MZ2 = 10, 20, 48, 58
    DS = ['deepslate_bricks', 'deepslate_bricks', 'cracked_deepslate_bricks', 'deepslate_tiles']
    for x in range(MX1, MX2 + 1):
        for z in range(MZ1, MZ2 + 1):
            B.set(x, G, z, 'polished_deepslate')
            edge = x in (MX1, MX2) or z in (MZ1, MZ2)
            for y in range(G + 1, G + 7):
                B.set(x, y, z, rnd.choice(DS) if edge else 'air')
            B.set(x, G + 7, z, 'deepslate_tiles')
    for i in range(0, 6):                                  # steep gabled roof (ridge along z)
        for z in range(MZ1 - 1, MZ2 + 2):
            B.set(MX1 - 1 + i, G + 7 + i, z, 'deepslate_tile_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]')
            B.set(MX2 + 1 - i, G + 7 + i, z, 'deepslate_tile_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]')
            for x in range(MX1 + i, MX2 + 1 - i):
                if z in (MZ1, MZ2) and i < 5: B.set(x, G + 7 + i, z, rnd.choice(DS))       # gable ends
        if i == 5:
            for z in range(MZ1 - 1, MZ2 + 2): B.set(15, G + 12, z, 'deepslate_tile_slab[type=bottom,waterlogged=false]')
    for x, z in [(MX1, MZ1), (MX2, MZ1), (MX1, MZ2), (MX2, MZ2)]:        # corner buttress-pinnacles
        for y in range(G + 1, G + 10): B.set(x, y, z, 'polished_deepslate')
        B.set(x, G + 10, z, 'polished_deepslate_wall'); B.set(x, G + 11, z, 'soul_lantern[hanging=false,waterlogged=false]')
    # pointed doorway, iron-barred transom, rose window, skull keystone
    for x in (14, 15, 16):
        for y in range(G + 1, G + 4): B.set(x, y, MZ1, 'air')
    B.set(14, G + 4, MZ1, 'iron_bars'); B.set(16, G + 4, MZ1, 'iron_bars'); B.set(15, G + 4, MZ1, 'iron_bars')
    B.set(15, G + 5, MZ1, 'chiseled_deepslate')
    for (x, y) in [(15, G + 8), (14, G + 8), (16, G + 8), (15, G + 9), (15, G + 7)]: B.set(x, y, MZ1, 'black_stained_glass_pane')
    B.set(15, G + 6, MZ1 - 1, 'skeleton_wall_skull[facing=north,powered=false]')
    for x in (13, 17): B.set(x, G + 1, MZ1 - 1, 'soul_lantern[hanging=false,waterlogged=false]')
    for z in (51, 54):                                     # barred side windows
        for x in (MX1, MX2):
            B.set(x, G + 3, z, 'iron_bars'); B.set(x, G + 4, z, 'iron_bars')
    B.set(12, G + 1, 50, 'candle[candles=4,lit=true]'); B.set(18, G + 1, 50, 'candle[candles=4,lit=true]')
    B.set(15, G + 6, 53, 'soul_lantern[hanging=true]')
    B.sign(15, G + 3, MZ2 - 1, 'dark_oak_wall_sign[facing=north,waterlogged=false]', ['THE VELVET HAND', 'Below lies the', 'master, and', 'his key.'], color='gray')
    for y in range(G + 1, G + 6): B.set(15, y, MZ2, 'polished_deepslate')

    # ---------------- way down: stairs (south, under the mausoleum) -> landing -> catacomb gallery (north, above the maze)
    # -> stairs (south) into the antechamber. Floors are bottom slabs (no spawns); the walk is sealed in solid rock.
    for x in range(12, 25):
        for z in range(18, 63):
            for y in range(8, 16): B.set(x, y, z, rnd.choice(['deepslate', 'cobbled_deepslate', 'tuff']))
    TS = 'deepslate_tile_slab[type=bottom,waterlogged=false]'
    for i in range(8):                                     # z52..59, stair block y17..10
        z, ys = 52 + i, G - i
        for x in (14, 15, 16):
            B.set(x, ys, z, 'deepslate_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]')
            B.set(x, ys - 1, z, 'deepslate_bricks')
            for y in range(ys + 1, max(ys + 5, G + 1) if z <= MZ2 - 1 else ys + 5): B.set(x, y, z, 'air')
        if z > MZ2 - 1:
            for x in (14, 15, 16): B.set(x, ys + 5, z, 'deepslate_bricks')
    for z in range(52, 58):                                # railings round the stairwell
        for x in (13, 17): B.set(x, G + 1, z, 'deepslate_brick_wall')
    def gallery(x1, z1, x2, z2):
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1):
                B.set(x, 10, z, TS)
                for y in range(11, 15): B.set(x, y, z, 'air')
    gallery(14, 60, 22, 61)                                # landing
    gallery(20, 20, 22, 61)                                # catacomb gallery (north)
    gallery(14, 20, 22, 22)                                # turn west
    gallery(14, 23, 16, 24)
    for i in range(8):                                     # z25..32, stair block y9..2, down into the antechamber
        z, ys = 25 + i, 9 - i
        for x in (14, 15, 16):
            B.set(x, ys, z, 'deepslate_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]')
            for y in range(ys + 1, ys + 5): B.set(x, y, z, 'air')
    # catacomb dressing: skull niches, bone shelves, lanterns, cobwebs
    for z in range(24, 60, 3):
        for (x, xn, f) in ((19, 18, 'east'), (23, 24, 'west')):
            if rnd.random() < 0.55:
                B.set(x, 12, z, 'air'); B.set(xn, 12, z, 'deepslate_bricks')
                B.set(x, 12, z, f'skeleton_wall_skull[facing={f},powered=false]' if rnd.random() < 0.6 else 'air')
    for z in range(26, 60, 8): B.set(21, 14, z, 'soul_lantern[hanging=true,waterlogged=false]')
    for (x, y, z) in [(20, 14, 30), (22, 14, 44), (20, 14, 57), (16, 14, 21)]: B.set(x, y, z, 'cobweb')
    B.sign(21, 12, 19, 'dark_oak_wall_sign[facing=south,waterlogged=false]', ['Walk soft.', 'It is listening.', '', '- the Gravedigger'], color='gray')
    B.marker(21.5, 11, 40.5, ['bm.zone_c'], 0)

    # ---------------- the crypt: antechamber + an 8x8-cell LABYRINTH with the altar chamber at its heart ----------------
    # Every crypt floor is a BOTTOM SLAB: no mob can spawn down here to distract the Warden.
    SLAB = ['deepslate_tile_slab[type=bottom,waterlogged=false]', 'deepslate_brick_slab[type=bottom,waterlogged=false]',
            'polished_deepslate_slab[type=bottom,waterlogged=false]', 'cobbled_deepslate_slab[type=bottom,waterlogged=false]']
    WALLS = ['deepslate_bricks', 'deepslate_bricks', 'deepslate_tiles', 'polished_deepslate', 'cobbled_deepslate']   # never cracked bricks (that's the escape door)
    def slab(): return SLAB[0] if rnd.random() < 0.55 else rnd.choice(SLAB[1:])
    def wall(): return rnd.choice(WALLS)
    # solid rock under the whole crypt footprint, y0..8
    for x in range(2, 29):
        for z in range(32, 64):
            for y in range(0, 9):
                B.set(x, y, z, wall() if y not in (0, 8) else 'deepslate_bricks')
    # antechamber: interior x11..19, z33..37, walk y2 (slab floor y1), ceiling y8
    for x in range(11, 20):
        for z in range(33, 38):
            B.set(x, 1, z, slab())
            for y in range(2, 8): B.set(x, y, z, 'air')
    for x in (14, 15, 16):                  # last step of the stairway, so you can always climb back out
        B.set(x, 1, 32, 'deepslate_bricks'); B.set(x, 2, 32, 'deepslate_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]')
        for y in range(3, 7): B.set(x, y, 32, 'air')
    # labyrinth: cell (i, j) interior = x 4+3i..5+3i, z 39+3j..40+3j; walls on the 3-grid; corridors 2 wide, 3 high
    N = 8
    CHAMBER = {(3, 3), (4, 3), (3, 4), (4, 4)}
    ENTRY = (3, 0)

    def make_maze(seed):
        r = random.Random(seed)
        oe, os_ = set(), set()
        seen, stack = {ENTRY} | CHAMBER, [ENTRY]
        while stack:
            i, j = stack[-1]
            nb = [(i + di, j + dj) for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1))
                  if 0 <= i + di < N and 0 <= j + dj < N and (i + di, j + dj) not in seen]
            if not nb:
                stack.pop(); continue
            ni, nj = r.choice(nb)
            (oe.add((min(i, ni), j)) if ni != i else os_.add((i, min(j, nj))))
            seen.add((ni, nj)); stack.append((ni, nj))
        k = 0
        while k < 3:                         # three small loops, never into the chamber
            i, j = r.randrange(N - 1), r.randrange(N - 1)
            e = r.random() < 0.5
            a, b = (i, j), ((i + 1, j) if e else (i, j + 1))
            if a in CHAMBER or b in CHAMBER: continue
            (oe if e else os_).add((i, j)); k += 1
        return oe, os_

    def graph(oe, os_):
        adj = {}
        for (i, j) in oe: adj.setdefault((i, j), set()).add((i + 1, j)); adj.setdefault((i + 1, j), set()).add((i, j))
        for (i, j) in os_: adj.setdefault((i, j), set()).add((i, j + 1)); adj.setdefault((i, j + 1), set()).add((i, j))
        return adj

    def bfs(adj, a):
        d, q = {a: 0}, [a]
        for c in q:
            for n in adj.get(c, ()):
                if n not in d: d[n] = d[c] + 1; q.append(n)
        return d

    # pick the layout with the longest walk to the chamber door and from it to the escape corner
    best = None
    for seed in range(1, 400):
        oe, os_ = make_maze(seed)
        adj = graph(oe, os_)
        d0 = bfs(adj, ENTRY)
        doors = [((c, n), d0.get(n, -1)) for c in CHAMBER for n in [(c[0] + 1, c[1]), (c[0] - 1, c[1]), (c[0], c[1] + 1), (c[0], c[1] - 1)]
                 if n not in CHAMBER and 0 <= n[0] < N and 0 <= n[1] < N]
        (door, dd) = max(doors, key=lambda t: t[1])
        dn = bfs(adj, door[1])
        corner = max([(0, 7), (7, 7)], key=lambda c: dn.get(c, -1))
        score = dd + dn.get(corner, 0)
        if best is None or score > best[0]: best = (score, seed, oe, os_, door, corner, dd, dn.get(corner, 0))
    _, _, open_e, open_s, door, ESC, D_IN, D_OUT = best
    (c, n) = door
    if c[0] != n[0]: open_e.add((min(c[0], n[0]), c[1]))
    else: open_s.add((c[0], min(c[1], n[1])))
    for i in (3,):                          # the altar chamber: cells (3..4, 3..4) merged
        for j in (3, 4): open_e.add((i, j))
    for j in (3,):
        for i in (3, 4): open_s.add((i, j))
    mrnd = random.Random(1337)
    cx0, cz0 = 3, 38
    for i in range(N):
        for j in range(N):
            x1, z1 = cx0 + 1 + 3 * i, cz0 + 1 + 3 * j
            for x in (x1, x1 + 1):
                for z in (z1, z1 + 1):
                    B.set(x, 1, z, slab())
                    for y in range(2, 5): B.set(x, y, z, 'air')
            if (i, j) in open_e:
                for z in (z1, z1 + 1):
                    B.set(x1 + 2, 1, z, slab())
                    for y in range(2, 5): B.set(x1 + 2, y, z, 'air')
            if (i, j) in open_s:
                for x in (x1, x1 + 1):
                    B.set(x, 1, z1 + 2, slab())
                    for y in range(2, 5): B.set(x, y, z1 + 2, 'air')
    # altar chamber x13..17, z48..52 (centre post removed, taller ceiling)
    for x in range(13, 18):
        for z in range(48, 53):
            B.set(x, 1, z, 'polished_deepslate_slab[type=bottom,waterlogged=false]')
            for y in range(2, 7): B.set(x, y, z, 'air')
    # maze entrance from the antechamber (top wall z38, over cells 3 and 4)
    for x in (13, 14):
        B.set(x, 1, 38, slab())
        for y in range(2, 5): B.set(x, y, 38, 'air')
    # ---- decoration: sculk veins on walls, cobwebs in dead ends, skulls, candles, a few dim lanterns
    def is_air(x, y, z): return B.get(x, y, z) == 'minecraft:air'
    for i in range(N):
        for j in range(N):
            x1, z1 = cx0 + 1 + 3 * i, cz0 + 1 + 3 * j
            exits = sum([(i, j) in open_e, (i - 1, j) in open_e, (i, j) in open_s, (i, j - 1) in open_s]) + ((i, j) == ENTRY)
            if 3 <= i <= 4 and 3 <= j <= 4: continue
            if exits == 1 and (i, j) != ESC:           # dead end: cobwebs and a skull mounted on the wall
                B.set(x1 + mrnd.randrange(2), 4, z1 + mrnd.randrange(2), 'cobweb')
                for (wx, wz, f) in [(x1 - 1, z1, 'east'), (x1 + 2, z1 + 1, 'west'), (x1, z1 - 1, 'south'), (x1 + 1, z1 + 2, 'north')]:
                    ax, az = wx + {'east': 1, 'west': -1}.get(f, 0), wz + {'south': 1, 'north': -1}.get(f, 0)
                    if B.get(wx, 3, wz) not in (None, 'minecraft:air') and B.get(ax, 3, az) == 'minecraft:air' and mrnd.random() < 0.7:
                        B.set(ax, 3, az, f'skeleton_wall_skull[facing={f},powered=false]'); break
            elif mrnd.random() < 0.12:
                B.set(x1, 4, z1, 'soul_lantern[hanging=true,waterlogged=false]')
    for x in range(3, 28):
        for z in range(38, 63):
            for y in (2, 3, 4):
                if is_air(x, y, z) and mrnd.random() < 0.05:
                    faces = {f: not is_air(x + dx, y, z + dz) and 'slab' not in (B.get(x + dx, y, z + dz) or '')
                             for f, (dx, dz) in {'north': (0, -1), 'south': (0, 1), 'east': (1, 0), 'west': (-1, 0)}.items()}
                    if any(faces.values()):
                        B.set(x, y, z, 'sculk_vein[' + ','.join(f'{f}={"true" if faces.get(f) else "false"}' for f in ('down', 'east', 'north', 'south', 'up', 'west')) + ',waterlogged=false]')
    # sculk creeping through the ceilings and walls (blocks that face a tunnel), and veins hanging from the ceiling
    srnd = random.Random(99)
    for x in range(3, 28):
        for z in range(33, 63):
            for y in range(2, 8):
                if B.get(x, y, z) != 'minecraft:air': continue
                if B.get(x, y + 1, z) in ('minecraft:deepslate_bricks', 'minecraft:deepslate_tiles', 'minecraft:polished_deepslate', 'minecraft:cobbled_deepslate') and srnd.random() < 0.22:
                    B.set(x, y + 1, z, 'sculk')
                for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    w = B.get(x + dx, y, z + dz)
                    if w in ('minecraft:deepslate_bricks', 'minecraft:deepslate_tiles', 'minecraft:cobbled_deepslate') and srnd.random() < 0.06:
                        B.set(x + dx, y, z + dz, 'sculk')
                if y >= 4 and B.get(x, y + 1, z) not in (None, 'minecraft:air') and 'slab' not in B.get(x, y + 1, z) and srnd.random() < 0.08:
                    B.set(x, y, z, 'sculk_vein[down=false,east=false,north=false,south=false,up=true,west=false,waterlogged=false]')
    # antechamber dressing
    for x, z in [(11, 33), (19, 33), (11, 37), (19, 37)]:
        B.fill(x, 2, z, x, 7, z, 'polished_deepslate')
    B.set(15, 7, 35, 'soul_lantern[hanging=true,waterlogged=false]')
    B.set(12, 2, 34, 'cobweb'); B.set(18, 7, 36, 'cobweb')
    B.sign(15, 4, 37, 'dark_oak_wall_sign[facing=north,waterlogged=false]', ['The master sleeps', 'at the heart.', 'So does what', 'guards him.'], color='gray')
    # altar at the chamber's south side; candles and bones
    B.set(15, 2, 52, 'chiseled_deepslate'); B.set(15, 3, 52, 'skeleton_skull[rotation=8,powered=false]')
    B.set(14, 2, 52, 'polished_deepslate'); B.set(16, 2, 52, 'polished_deepslate')
    B.set(14, 3, 52, 'candle[candles=4,lit=true,waterlogged=false]'); B.set(16, 3, 52, 'candle[candles=4,lit=true,waterlogged=false]')
    B.set(13, 2, 52, 'polished_deepslate_wall'); B.set(17, 2, 52, 'polished_deepslate_wall')   # walls: nothing can spawn on them
    B.set(13, 3, 48, 'skeleton_wall_skull[facing=south,powered=false]'); B.set(17, 3, 48, 'skeleton_wall_skull[facing=south,powered=false]')
    B.set(15, 6, 50, 'soul_lantern[hanging=true,waterlogged=false]')
    # escape: the bottom corner cell farthest from the chamber -> a cracked door in the south wall -> ladder shaft to a well
    # behind the graveyard fence
    EX = 4 if ESC == (0, 7) else 26
    for y in range(1, 4): B.set(EX, y, 62, 'deepslate_bricks')
    B.set(EX, 2, 62, 'cracked_deepslate_bricks'); B.set(EX, 3, 62, 'cracked_deepslate_bricks')
    for y in range(1, G + 1):
        for (x, z) in [(EX - 1, 63), (EX + 1, 63), (EX, 64)]:
            B.set(x, y, z, 'deepslate_bricks' if y < G else 'mossy_cobblestone')
        B.set(EX, y, 63, 'deepslate_brick_slab[type=bottom,waterlogged=false]' if y == 1 else 'ladder[facing=north,waterlogged=false]')
    for y in range(4, G + 1): B.set(EX, y, 62, 'deepslate_bricks' if y < G else 'mossy_cobblestone')
    for x in (EX - 1, EX, EX + 1):
        for z in (62, 63, 64):
            if (x, z) != (EX, 63): B.set(x, G + 1, z, 'mossy_cobblestone_slab[type=bottom,waterlogged=false]')
    B.set(EX, G + 1, 63, 'air')
    B.meta_maze = dict(walk_in=D_IN, walk_out=D_OUT, escape=ESC)
    # markers (the controller is where the Warden digs out: the middle of the altar chamber)
    B.marker(15.5, 2, 49.5, ['bm.crypt_ctrl', 'bm.zone_c'], 0)
    B.marker(15.5, 2, 35.5, ['bm.crypt_trigger'], 0)
    B.marker(15.5, 2, 51.5, ['bm.key_altar'], 0)
    B.marker(EX + 0.5, 2.0, 62.5, ['bm.crypt_escape'], 0)
    B.marker(15.5, 3.6, 52.5, ['bm.npc_spawn', 'bm.npc.deco_key'], 180)
    return B


if __name__ == '__main__':
    import sys
    for nm, fn in [('graveyard', build_graveyard)]:     # (the 1.7 market builder was retired in 2.15; market2.py builds the market)
        b = fn()
        print(nm, b.export(f'/tmp/{nm}.nbt'))


def build_frog_hut():
    """1.10: Frog with Mustache's stilt hut in swamps and mangrove swamps. 15 x 18 x 16. Template y4 sits at the first air
    above the water (structure start_height -4 + WORLD_SURFACE_WG); the stilts reach 4 blocks down into the mud.
    Floor y6 (walk 7). The frog (a 3D figure with an interaction box) sits on a mossy dais facing the door (south)."""
    rnd = random.Random(1717)
    B = Build(15, 18, 16)
    F = 6
    for (x, z) in ((2, 2), (2, 12), (12, 2), (12, 12), (7, 2), (2, 7), (12, 7), (7, 13), (5, 13), (9, 13)):
        for y in range(0, F): B.set(x, y, z, 'mangrove_log[axis=y]')
    for x in range(2, 13):                                   # floor + porch
        for z in range(2, 15):
            if z <= 12 or 4 <= x <= 10: B.set(x, F, z, 'mangrove_planks' if rnd.random() > 0.15 else 'stripped_mangrove_log[axis=x]')
    for x in range(4, 11):                                   # porch rail
        if x not in (6, 7, 8): B.set(x, F + 1, 14, 'mangrove_fence')
    for z in (13, 14): B.set(4, F + 1, z, 'mangrove_fence'); B.set(10, F + 1, z, 'mangrove_fence')
    for y in range(0, F): B.set(7, y, 14, 'mangrove_log[axis=y]')    # ladder post at the end of the dock
    for y in range(1, F + 1): B.set(7, y, 15, 'ladder[facing=south,waterlogged=false]')
    # walls x3..11, z3..11, y7..10, log corners
    for y in range(F + 1, F + 5):
        for x in range(3, 12):
            for z in range(3, 12):
                edge = x in (3, 11) or z in (3, 11)
                if not edge: B.set(x, y, z, 'air'); continue
                corner = x in (3, 11) and z in (3, 11)
                win = (y in (F + 2, F + 3)) and ((x in (3, 11) and z in (6, 8)) or (z == 3 and x in (5, 9)) or (z == 11 and x in (4, 10)))
                B.set(x, y, z, 'mangrove_log[axis=y]' if corner else 'brown_stained_glass' if win else 'mangrove_planks')
    B.set(7, F + 1, 11, 'mangrove_door[facing=south,half=lower,hinge=left,open=false,powered=false]')
    B.set(7, F + 2, 11, 'mangrove_door[facing=south,half=upper,hinge=left,open=false,powered=false]')
    # mossy roof (stepped, overhanging), a chimney
    for k in range(5):
        y = F + 5 + k
        for x in range(2 + k, 13 - k):
            for z in range(2 + k, 13 - k):
                if x in (2 + k, 12 - k) or z in (2 + k, 12 - k): B.set(x, y, z, 'moss_block' if rnd.random() > 0.2 else 'mud_bricks')
    B.set(7, F + 10, 7, 'moss_block')
    for y in range(F + 5, F + 11): B.set(10, y, 4, 'mud_bricks')
    B.set(10, F + 11, 4, 'campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]')
    for (x, z) in ((2, 2), (12, 2), (2, 12), (12, 12)):
        B.set(x, F + 5, z, 'moss_block')
    # interior: the dais, a brewing corner, barrels, a lantern on a chain
    for x in range(5, 10):
        for z in range(4, 7): B.set(x, F + 1, z, 'moss_carpet')
    B.set(7, F + 1, 5, 'moss_block')
    B.set(4, F + 1, 4, 'brewing_stand[has_bottle_0=true,has_bottle_1=false,has_bottle_2=true]')
    B.set(4, F + 1, 5, 'water_cauldron[level=3]')
    B.set(10, F + 1, 4, 'barrel[facing=up,open=false]'); B.set(10, F + 1, 5, 'barrel[facing=up,open=false]')
    B.set(10, F + 1, 10, 'decorated_pot[cracked=false,facing=north,waterlogged=false]')
    B.set(4, F + 1, 10, 'lectern[facing=east,has_book=true,powered=false]',
          {'id': 'minecraft:lectern', 'Book': book_nbt('Memoirs of a Frog Knight', 'Frog with Mustache', [
              "I was knighted by a king who no longer remembers me, for a deed no one else saw. The moustache came later.",
              "I have fought rats, wardens and one very rude heron. I fear nothing but dry weather.",
              "For one Medallion I will follow you anywhere. Hand me a blade and I will use it. Hand me a helmet and I will wear it with pride.",
              "Right-click me with nothing in hand to have me wait. Sneak and right-click to take your gear back. Feed me meat when I'm hurt - any meat. I am not proud."]),
           'Page': Int(0)})
    for y in range(F + 4, F + 5): B.set(7, y, 7, 'iron_chain[axis=y,waterlogged=false]')
    B.set(7, F + 3, 7, 'lantern[hanging=true,waterlogged=false]')
    # porch dressing + sign
    for (x, z) in ((4, 12), (10, 12)): B.set(x, F, z, 'moss_block'); B.set(x, F + 1, z, 'firefly_bush')   # 1.19: a mossy planter (bushes can't root in planks)
    B.set(5, F + 1, 12, 'lantern[hanging=false,waterlogged=false]'); B.set(9, F + 1, 12, 'lantern[hanging=false,waterlogged=false]')
    B.sign(6, F + 2, 12, 'mangrove_wall_sign[facing=south,waterlogged=false]', ['FROG WITH', 'MUSTACHE', 'For hire:', '1 Medallion'], color='lime', glow=True)
    B.marker(7.5, F + 2.0, 5.5, ['bm.npc_spawn', 'bm.npc.frog_hut'], 0)
    return B

"""2.65: the vault's new architecture - a look of its own for every tier, the passages between rooms (up, down, left,
right, a shaft, a drop, a chasm), and the den and dial room put right.

THEMES: every room is built once per tier from the same plan, its stone swapped for the tier's own:
  I   The Copper Strongroom  tuff and cut copper, copper lanterns and bulbs, raw copper piles
  II  The Silver Vaults      andesite and iron, quartz pillars, cold soul-lanterns
  III The Gold Reserve       blackstone and gold (as it always was)
  IV  The Diamond Deposit    deepslate and prismarine, sea lanterns, diamond
  V   The Gutter King's Hoard deep bricks, gold trim, crying-obsidian pillars, red carpets
CONNECTORS: a room's exit door (x 24, z 11-13, y 4-7) opens into a passage, and the passage into the next room's entry
door. Each passage has an entry and an exit reference cell (where you stand, door centre): placed so its entry meets
the door, the next room goes where its exit points. CONN[kind] = (template size, entry ref, exit ref)."""
from structures import Build, parse_state, state_str
import phase70_rooms as RM

TIERS = (1, 2, 3, 4, 5)
BASE = {'wall': 'minecraft:polished_blackstone_bricks', 'trim': 'minecraft:gilded_blackstone', 'pillar': 'minecraft:chiseled_polished_blackstone',
        'floor': 'minecraft:polished_blackstone', 'ceil': 'minecraft:blackstone', 'lantern': 'minecraft:lantern', 'chain': 'minecraft:iron_chain',
        'metal': 'minecraft:gold_block', 'raw': 'minecraft:raw_gold_block', 'carpet': 'minecraft:yellow_carpet',
        'stairs': 'minecraft:polished_blackstone_brick_stairs', 'slab': 'minecraft:polished_blackstone_brick_slab',
        'glow': 'minecraft:shroomlight'}
THEMES = {
    1: dict(wall='minecraft:tuff_bricks', trim='minecraft:waxed_cut_copper', pillar='minecraft:chiseled_tuff_bricks', floor='minecraft:polished_tuff',
            ceil='minecraft:tuff', lantern='minecraft:waxed_copper_lantern', chain='minecraft:waxed_copper_chain', metal='minecraft:waxed_copper_block',
            raw='minecraft:raw_copper_block', carpet='minecraft:orange_carpet', stairs='minecraft:tuff_brick_stairs', slab='minecraft:tuff_brick_slab',
            glow='minecraft:waxed_copper_bulb[lit=true]'),
    2: dict(wall='minecraft:polished_andesite', trim='minecraft:iron_block', pillar='minecraft:quartz_pillar', floor='minecraft:smooth_stone',
            ceil='minecraft:andesite', lantern='minecraft:soul_lantern', chain='minecraft:iron_chain', metal='minecraft:iron_block',
            raw='minecraft:raw_iron_block', carpet='minecraft:light_gray_carpet', stairs='minecraft:polished_andesite_stairs',
            slab='minecraft:polished_andesite_slab', glow='minecraft:sea_lantern'),
    3: dict(BASE),
    4: dict(wall='minecraft:deepslate_tiles', trim='minecraft:prismarine_bricks', pillar='minecraft:chiseled_deepslate', floor='minecraft:polished_deepslate',
            ceil='minecraft:cobbled_deepslate', lantern='minecraft:sea_lantern', chain='minecraft:iron_chain', metal='minecraft:diamond_block',
            raw='minecraft:deepslate_diamond_ore', carpet='minecraft:light_blue_carpet', stairs='minecraft:deepslate_tile_stairs',
            slab='minecraft:deepslate_tile_slab', glow='minecraft:sea_lantern'),
    5: dict(wall='minecraft:deepslate_bricks', trim='minecraft:gold_block', pillar='minecraft:crying_obsidian', floor='minecraft:polished_blackstone',
            ceil='minecraft:obsidian', lantern='minecraft:soul_lantern', chain='minecraft:iron_chain', metal='minecraft:gold_block',
            raw='minecraft:raw_gold_block', carpet='minecraft:red_carpet', stairs='minecraft:deepslate_brick_stairs', slab='minecraft:deepslate_brick_slab',
            glow='minecraft:shroomlight'),
}
FULL_LANTERN = {'minecraft:sea_lantern'}         # (a block, not a lantern: no 'hanging' state)


def theme_of(t, key):
    return THEMES[t][key]


def retheme(b, t, protect=()):
    """swap the base (tier III) materials for tier t's, in place; cells in `protect` keep theirs"""
    if t == 3: return b
    th = THEMES[t]
    by_name = {parse_state(BASE[k])[0]: k for k in BASE}
    protect = set(protect)
    for pos, st in list(b.b.items()):
        if pos in protect: continue
        name, props = parse_state(st)
        k = by_name.get(name)
        if not k: continue
        new = th[k]
        nname, nprops = parse_state(new)
        if k == 'lantern' and nname in FULL_LANTERN: b.b[pos] = nname; continue
        if k in ('stairs', 'slab', 'lantern', 'chain'): nprops = dict(props, **nprops)
        b.b[pos] = state_str(nname, nprops)
    return b


def wall_glow(b, length=RM.W):
    """light blocks set into the walls (base 'glow', themed later)"""
    for x in (6, length - 7):
        for z in (0, RM.D - 1):
            b.set(x, 6, z, BASE['glow']); b.set(x, 11, z, BASE['glow'])
    for z in (4, RM.D - 5):
        b.set(0, 11, z, BASE['glow']); b.set(length - 1, 11, z, BASE['glow'])
    return b


# ===================================================================== connectors
#  local coords: x along the way, the floor block under the standing cell; entry/exit refs are standing cells (door centre)
W5 = 5


def _solid(L, H, Wd):
    b = Build(L, H, Wd)
    b.fill(0, 0, 0, L - 1, H - 1, Wd - 1, BASE['wall'])
    return b


def _hall(b, x1, x2, s, z1, z2, h=4):
    """floor under standing level s, air s..s+h-1, a ceiling over it"""
    for x in range(x1, x2 + 1):
        for z in range(z1, z2 + 1):
            b.set(x, s - 1, z, BASE['floor'] if z in (z1, z2) or z2 - z1 < 2 else 'minecraft:polished_blackstone_bricks')
            for y in range(s, s + h):
                b.set(x, y, z, 'minecraft:air')
            b.set(x, s + h, z, BASE['ceil'])
    for x in range(x1, x2 + 1):                              # a gold edge to the walk, like the rooms' runner
        if z2 - z1 >= 2:
            b.set(x, s - 1, z1, BASE['trim']); b.set(x, s - 1, z2, BASE['trim'])


def cn_st():
    b = _solid(5, 6, W5)
    _hall(b, 0, 4, 1, 1, 3)
    b.set(2, 4, 2, BASE['lantern'] + '[hanging=true]')
    for x in (1, 3):
        b.set(x, 3, 0, BASE['trim']); b.set(x, 3, 4, BASE['trim'])
    return b


def cn_up(down=False):
    L, H = 9, 11
    b = _solid(L, H, W5)
    for x in range(L):
        s = 1 if x <= 1 else (6 if x >= 6 else x)           # standing level: 1,1,2,3,4,5,6,6,6
        if down: s = 7 - s
        for z in (1, 2, 3):
            for y in range(s, min(H - 1, s + 5)):
                b.set(x, y, z, 'minecraft:air')
    for x in range(L):
        s = 1 if x <= 1 else (6 if x >= 6 else x)
        if down: s = 7 - s
        for z in (1, 2, 3):
            stepping = (2 <= x <= 6) if not down else (2 <= x <= 6)
            if not down and 2 <= x <= 6:
                b.set(x, s - 1, z, BASE['stairs'] + '[facing=east,half=bottom,shape=straight]')
            elif down and 2 <= x <= 6:
                b.set(x, s - 1, z, BASE['stairs'] + '[facing=west,half=bottom,shape=straight]')
            else:
                b.set(x, s - 1, z, BASE['floor'] if z != 2 else 'minecraft:polished_blackstone_bricks')
    b.set(4, 9, 2, BASE['lantern'] + '[hanging=true]')
    b.set(4, 5 if not down else 5, 0, BASE['glow']); b.set(4, 5, 4, BASE['glow'])
    return b


def cn_bend(right=False):
    L, H, Wd = 9, 6, 13
    b = _solid(L, H, Wd)
    ez, xz = (10, 2) if not right else (2, 10)
    zl = lambda zc: (zc - 1, zc + 1)
    _hall(b, 0, 2, 1, *zl(ez))
    _hall(b, 3, 5, 1, 1, 11)
    _hall(b, 6, 8, 1, *zl(xz))
    b.set(4, 4, 6, BASE['lantern'] + '[hanging=true]')
    b.set(6, 3, 6, BASE['glow'])
    return b


def cn_shaft():
    b = _solid(5, 16, W5)
    _hall(b, 0, 1, 1, 1, 3)
    for y in range(1, 15):
        for z in (1, 2, 3): b.set(2, y, z, 'minecraft:air')
    for z in (1, 2, 3): b.set(2, 0, z, BASE['floor']); b.set(2, 15, z, BASE['ceil'])
    _hall(b, 3, 4, 11, 1, 3)
    for y in range(1, 11):
        b.set(2, y, 2, 'minecraft:ladder[facing=west,waterlogged=false]')
    b.set(2, 14, 2, BASE['lantern'] + '[hanging=true]')
    b.set(2, 7, 0, BASE['glow']); b.set(2, 7, 4, BASE['glow'])
    return b


def cn_drop():
    b = _solid(5, 16, W5)
    _hall(b, 0, 1, 11, 1, 3)
    for y in range(2, 15):
        for z in (1, 2, 3): b.set(2, y, z, 'minecraft:air')
    for z in (1, 2, 3):
        b.set(2, 0, z, BASE['floor']); b.set(2, 1, z, 'minecraft:water'); b.set(2, 15, z, BASE['ceil'])
    _hall(b, 3, 4, 2, 1, 3)
    for y in range(2, 11):
        b.set(2, y, 3, 'minecraft:ladder[facing=north,waterlogged=false]')
    b.set(2, 14, 1, BASE['lantern'] + '[hanging=true]')
    b.set(2, 7, 0, BASE['glow']); b.set(2, 7, 4, BASE['glow'])
    return b


def cn_bridge():
    L, H, Wd = 11, 11, 7
    b = _solid(L, H, Wd)
    _hall(b, 0, 1, 6, 2, 4)
    _hall(b, 9, 10, 6, 2, 4)
    for x in range(2, 9):
        for z in range(1, 6):
            b.set(x, 0, z, BASE['floor'])
            for y in range(1, 10): b.set(x, y, z, 'minecraft:air')
            b.set(x, 1, z, 'minecraft:water'); b.set(x, 2, z, 'minecraft:water')
            b.set(x, 10, z, BASE['ceil'])
    for (x, z) in ((2, 3), (3, 3), (5, 3), (6, 2), (8, 3)):         # stepping stones (two easy jumps)
        b.set(x, 5, z, BASE['trim'])
    for y in range(1, 6):
        b.set(2, y, 2, 'minecraft:ladder[facing=east,waterlogged=' + ('true' if y <= 2 else 'false') + ']')
    b.set(5, 9, 3, BASE['lantern'] + '[hanging=true]')
    for x in (3, 7):
        b.set(x, 7, 0, BASE['glow']); b.set(x, 7, Wd - 1, BASE['glow'])
    return b


# kind: (builder, size, entry ref, exit ref, weight)
CONN = {
    'st': (cn_st, (5, 6, 5), (0, 1, 2), (4, 1, 2), 3),
    'up': (lambda: cn_up(False), (9, 11, 5), (0, 1, 2), (8, 6, 2), 2),
    'dn': (lambda: cn_up(True), (9, 11, 5), (0, 6, 2), (8, 1, 2), 2),
    'lf': (lambda: cn_bend(False), (9, 6, 13), (0, 1, 10), (8, 1, 2), 2),
    'rt': (lambda: cn_bend(True), (9, 6, 13), (0, 1, 2), (8, 1, 10), 2),
    'sh': (cn_shaft, (5, 16, 5), (0, 1, 2), (4, 11, 2), 1),
    'dp': (cn_drop, (5, 16, 5), (0, 11, 2), (4, 2, 2), 1),
    'br': (cn_bridge, (11, 11, 7), (0, 6, 3), (10, 6, 3), 1),
}


def conn_move(kind):
    """(connector origin offset from the room origin, next room origin offset)"""
    _b, size, (ex, ey, ez), (xx, xy, xz), _w = CONN[kind]
    return (25, 4 - ey, 12 - ez), (25 + size[0], xy - ey, xz - ez)


# ===================================================================== the den, put right
def lobby2():
    b = RM.lobby()
    for x in range(9, 16):                                  # the old counter (under the sheet, right before the clockwork door) goes...
        b.set(x, 4, 2, 'minecraft:air')
    for x in range(3, 9):                                   # ...and the heist sheet's counter stands to the west, clear of the door
        b.set(x, 4, 2, 'minecraft:dark_oak_planks')
    b.set(21, 4, 5, 'minecraft:heavy_weighted_pressure_plate'); b.set(21, 3, 5, 'minecraft:emerald_block')   # back to the crew
    b.set(22, 4, 20, 'minecraft:gold_block'); b.set(22, 5, 20, 'minecraft:decorated_pot')                   # the Lucky pool's urn
    wall_glow(b)
    return b


def dial2():
    b = RM.dial()
    b.set(16, 5, 22, 'minecraft:pale_oak_button[face=wall,facing=north,powered=false]')
    wall_glow(b)
    return b


def glowing(fn):
    def f():
        return wall_glow(fn())
    return f


VAULT_DOOR = {(24, y, z) for y in range(4, 9) for z in range(9, 16)}


def tiered_rooms(extra=None):
    """{template name: builder} for every room in every tier"""
    rooms = {'lobby': lobby2, 'dial': dial2}
    for k in ('levers', 'plates', 'lasers', 'tiles', 'guards', 'coffers', 'cache'):
        rooms[k] = glowing(RM.BUILDERS[k])
    rooms['vault'] = lambda: wall_glow(RM.vault(), RM.VAULT_LEN)
    if extra: rooms.update(extra)
    out = {}
    for k, f in rooms.items():
        for t in TIERS:
            out[f'{k}_t{t}'] = (lambda f=f, t=t, k=k: retheme(f(), t, VAULT_DOOR if k == 'vault' else ()))
    for k, (f, *_r) in CONN.items():
        for t in TIERS:
            out[f'cn_{k}_t{t}'] = (lambda f=f, t=t: retheme(f(), t))
    return out

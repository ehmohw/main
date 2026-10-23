"""Score and render how structures really sit in generated terrain (sites from tools/bots/placecheck.js, /tmp/placecheck.json).

    python3 placecheck.py [sid ...] [--world ~/bm_srv/world] [--out /tmp/placecheck]

For each site: the structure's blocks (anything the terrain doesn't make) are found in a box around it, then per footprint column
  float  - air/water under the structure's lowest block, down to the ground (a floating corner)
  bury   - terrain blocks standing inside the footprint above the floor (sunk into a hill)
  plinth - a raw dirt/stone column under the footprint's edge rising above the terrain beside it (the jagged blocky skirt)
and an isometric picture of the site is written beside the numbers."""
import os, sys, json, hashlib
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from worldread import World
import structiso

NAT = ('stone', 'deepslate', 'dirt', 'grass_block', 'coarse_dirt', 'rooted_dirt', 'podzol', 'mycelium', 'sand', 'red_sand', 'gravel', 'clay',
       'granite', 'diorite', 'andesite', 'tuff', 'calcite', 'sandstone', 'red_sandstone', 'terracotta', 'snow_block', 'powder_snow', 'ice',
       'packed_ice', 'blue_ice', 'mud', 'moss_block', 'pale_moss_block', 'dripstone_block', 'netherrack', 'soul_sand', 'soul_soil', 'basalt',
       'blackstone', 'magma_block', 'end_stone', 'crimson_nylium', 'warped_nylium', 'nether_gold_ore', 'nether_quartz_ore', 'bedrock',
       'smooth_basalt', 'dirt_path', 'farmland', 'suspicious_sand', 'suspicious_gravel', 'obsidian', 'amethyst_block', 'budding_amethyst')
SOFT = ('air', 'cave_air', 'void_air', 'water', 'lava', 'snow', 'short_grass', 'tall_grass', 'fern', 'large_fern', 'seagrass', 'tall_seagrass',
        'kelp', 'kelp_plant', 'dead_bush', 'vine', 'glow_lichen', 'bubble_column', 'sugar_cane', 'lily_pad', 'pointed_dripstone', 'moss_carpet',
        'pale_moss_carpet', 'leaf_litter', 'bush', 'firefly_bush', 'short_dry_grass', 'tall_dry_grass', 'cactus', 'sweet_berry_bush',
        'crimson_roots', 'warped_roots', 'nether_sprouts', 'crimson_fungus', 'warped_fungus', 'weeping_vines', 'weeping_vines_plant',
        'twisting_vines', 'twisting_vines_plant', 'chorus_plant', 'chorus_flower', 'brown_mushroom', 'red_mushroom', 'mangrove_roots',
        'muddy_mangrove_roots', 'mangrove_propagule', 'hanging_roots', 'spore_blossom', 'big_dripleaf', 'big_dripleaf_stem', 'small_dripleaf',
        'azalea', 'flowering_azalea', 'cobweb', 'pink_petals', 'wildflowers', 'sea_pickle', 'snow')
TREE = ('_log', '_leaves', '_wood', 'mushroom_block', 'mushroom_stem', 'wart_block', 'shroomlight', 'coral', 'bamboo', 'pumpkin', 'melon',
        'bee_nest', 'creaking_heart', 'resin_clump', 'pale_hanging_moss', 'cocoa')
FLOWERS = ('dandelion', 'poppy', 'blue_orchid', 'allium', 'azure_bluet', 'tulip', 'oxeye_daisy', 'cornflower', 'lily_of_the_valley',
           'sunflower', 'lilac', 'rose_bush', 'peony', 'torchflower', 'pitcher', 'eyeblossom', 'cactus_flower', 'open_eyeblossom', 'closed_eyeblossom')
ORE = ('_ore',)


def kind(b):
    if b is None: return '?'
    n = b.split(':')[-1]
    if n in SOFT or any(f in n for f in FLOWERS): return 'soft'
    if n in NAT or n.endswith(ORE) or n.endswith('_terracotta') and not n.startswith('glazed') and n != 'terracotta' and False: return 'nat'
    if n.endswith('_terracotta') and n.split('_')[0] in ('white', 'orange', 'yellow', 'brown', 'red', 'light') and 'glazed' not in n: return 'nat'
    if any(t in n for t in TREE): return 'tree'
    return 'build'


_base = structiso.color
NCOL = {'deepslate': (70, 70, 76), 'podzol': (110, 80, 40), 'coarse_dirt': (120, 86, 60), 'snow_block': (240, 245, 250), 'ice': (160, 190, 250),
        'packed_ice': (140, 170, 240), 'tuff': (100, 102, 94), 'granite': (150, 104, 86), 'diorite': (190, 190, 190), 'mud': (60, 56, 60),
        'oak_leaves': (60, 120, 40), 'spruce_leaves': (50, 90, 50), 'birch_leaves': (90, 130, 60), 'clay': (160, 165, 178), 'red_sand': (190, 100, 40),
        'terracotta': (152, 94, 68), 'calcite': (220, 220, 215), 'moss_block': (90, 120, 50), 'bedrock': (40, 40, 40)}


def color(st):
    n = st.split(':', 1)[-1]
    if n in NCOL: return NCOL[n]
    if n.endswith('_leaves'): return (60, 110, 45)
    if n.endswith('_log'): return (100, 80, 50)
    c = _base(st)
    if c != (200, 0, 200): return c
    h = hashlib.md5(n.encode()).digest()
    return (60 + h[0] % 160, 60 + h[1] % 160, 60 + h[2] % 160)


structiso.color = color


class FakeB:
    def __init__(self, size, b): self.size, self.b = size, b


def analyse(W, x0, z0, R=44, ylo=-10, yhi=200, surface=True):
    hm, gnd, cols = {}, {}, {}
    for dx in range(-R, R + 1):
        for dz in range(-R, R + 1):
            x, z = x0 + dx, z0 + dz
            got, g = [], None
            for y in range(yhi, ylo - 1, -1):
                b = W.block(x, y, z)
                if b is None: break
                k = kind(b)
                if k == 'nat' and g is None: g = y
                if k == 'build': got.append(y)
                if surface and g is not None and y < g - 8: break
            gnd[(dx, dz)] = g if g is not None else ylo
            cols[(dx, dz)] = [y for y in got if not surface or g is None or y > g - 8]
    cand = {c for c, v in cols.items() if v}
    if not cand: return None
    # the main cluster (8-connected), from the column nearest the site's centre
    seen, best = set(), set()
    for c0 in sorted(cand, key=lambda c: c[0] ** 2 + c[1] ** 2):
        if c0 in seen: continue
        comp, st = set(), [c0]
        while st:
            c = st.pop()
            if c in seen or c not in cand: continue
            seen.add(c); comp.add(c)
            st += [(c[0] + i, c[1] + j) for i in (-1, 0, 1) for j in (-1, 0, 1)]
        if len(comp) > len(best): best = comp
    foot = best
    lo = {c: min(cols[c]) for c in foot}
    floor_y = Counter(lo.values()).most_common(1)[0][0]
    fl, bu, pl, cl = [], [], [], []
    for c in foot:
        x, z = x0 + c[0], z0 + c[1]
        y = lo[c]
        if y <= floor_y + 1 and kind(W.block(x, y - 1, z)) in ('soft', 'tree'):
            gap = 0
            while gap < 40 and kind(W.block(x, y - 1 - gap, z)) in ('soft', 'tree'): gap += 1
            fl.append((c, gap))
        if gnd[c] >= floor_y + 2 and gnd[c] > max(cols[c]) - 0 or any(kind(W.block(x, yy, z)) == 'nat' for yy in range(floor_y + 2, floor_y + 5)):
            bu.append(c)
        for e in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (c[0] + e[0], c[1] + e[1]); n2 = (c[0] + 3 * e[0], c[1] + 3 * e[1])
            if n in foot or n2 not in gnd or n2 in foot: continue
            if gnd[n] >= floor_y - 2 and gnd[n] - gnd[n2] >= 3: pl.append(n)
            if gnd[n] >= floor_y + 3: cl.append(n)
    build = {(c[0], y, c[1]): 1 for c in foot for y in cols[c]}
    return dict(build=build, foot=foot, floor_y=floor_y, gnd=gnd, float=len(fl), bury=len(bu), plinth=len(set(pl)), cliff=len(set(cl)),
                fl=fl, bu=bu, pl=pl, cl=cl, maxgap=max([g for _, g in fl] or [0]))


def render_site(W, x0, z0, A, path):
    xs = [c[0] for c in A['foot']]; zs = [c[1] for c in A['foot']]
    m = 8
    X0, X1, Z0, Z1 = min(xs) - m, max(xs) + m, min(zs) - m, max(zs) + m
    ys = [y for (_, y, _) in A['build']]
    y_lo, y_hi = A['floor_y'] - 7, max(ys) + 2
    b = {}
    for dx in range(X0, X1 + 1):
        for dz in range(Z0, Z1 + 1):
            for y in range(y_lo, y_hi + 1):
                bl = W.block(x0 + dx, y, z0 + dz)
                if bl is None: continue
                k = kind(bl)
                if k == 'soft' and not bl.endswith('water'): continue
                if bl.endswith('water'):
                    up = W.block(x0 + dx, y + 1, z0 + dz)
                    if up and up.endswith('water'): continue
                b[(dx - X0, y - y_lo, dz - Z0)] = bl
    structiso.render(FakeB((X1 - X0 + 1, y_hi - y_lo + 1, Z1 - Z0 + 1), b), path, scale=6)


def main():
    args = sys.argv[1:]
    world = os.path.expanduser('~/bm_srv/world'); out = '/tmp/placecheck'
    if '--world' in args: i = args.index('--world'); world = args[i + 1]; del args[i:i + 2]
    if '--out' in args: i = args.index('--out'); out = args[i + 1]; del args[i:i + 2]
    os.makedirs(out, exist_ok=True)
    sites = json.load(open('/tmp/placecheck.json'))
    Ws = {}
    for sid, lst in sites.items():
        if args and sid not in args: continue
        for i, s in enumerate(lst):
            W = Ws.setdefault(s['dim'], World(world, s['dim']))
            yr = (32, 118) if s['dim'] == 'the_nether' else (-10, 230)
            A = analyse(W, s['x'], s['z'], ylo=yr[0], yhi=yr[1], surface=s['dim'] != 'the_nether')
            if not A: print(f'{sid:22} #{i + 1} {s["x"]} {s["z"]}: nothing built'); continue
            print(f'{sid:22} #{i + 1} {s["x"]:>7} {s["z"]:>7}  floor {A["floor_y"]:>4}  cols {len(A["foot"]):>5}  float {A["float"]:>4} (gap {A["maxgap"]:>2})  bury {A["bury"]:>4}  plinth {A["plinth"]:>4}  cliff {A["cliff"]:>4}')
            render_site(W, s['x'], s['z'], A, f'{out}/{sid}_{i + 1}.png')


if __name__ == '__main__':
    main()

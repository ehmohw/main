"""2.92: settling structures into the land - one pass for everything built on the ground.

A structure's footprint is a rectangle (w x d) whose floor (the first layer above the ground it stands on) is y. Settling it:
  - cuts the terrain above it into a slope, one block up per ring out (no sheer walls of dirt where a hill met the box),
    and gives the new ground its biome's top (grass, sand, snow...);
  - banks a skirt of soil under its edges, one block down per ring out (no floating corners, no square stone plinth);
  - optionally clears terrain inside the footprint above the floor (a hill pushing through a courtyard) and fills holes
    under it (under its template, for one that reaches `base` blocks into the ground).
Only terrain and plants are ever cut, only air (and, where asked, water) is ever filled, so the structure itself is safe.

    settle.make(G, 'keep', 72, 78, ...)        -> function bm:settle/keep/a and /b (the footprint turned a quarter), run at
                                                 the footprint's low (north-west) corner, on the floor, with storage bm:settle
    settle.corners(Bd, 'keep', x0, z0, x1, z1, y)   markers at a jigsaw template's four corners: the pass runs once someone
                                                 comes near, whichever way the piece was turned
    settle.run('keep', ox, oy, oz)             -> the command a runtime builder uses (offset of the low corner from where it runs)
"""
CUT = ['stone', 'deepslate', 'dirt', 'grass_block', 'coarse_dirt', 'podzol', 'mycelium', 'rooted_dirt', 'sand', 'red_sand', 'gravel', 'clay',
       'granite', 'diorite', 'andesite', 'tuff', 'calcite', 'snow_block', 'powder_snow', 'mud', 'moss_block', 'pale_moss_block', 'sandstone',
       'red_sandstone', 'terracotta', 'white_terracotta', 'orange_terracotta', 'yellow_terracotta', 'brown_terracotta', 'red_terracotta',
       'light_gray_terracotta', 'dripstone_block', 'smooth_basalt', 'coal_ore', 'iron_ore', 'copper_ore', 'deepslate_coal_ore', 'deepslate_iron_ore',
       'deepslate_copper_ore', 'netherrack', 'soul_sand', 'soul_soil', 'basalt', 'blackstone', 'crimson_nylium', 'warped_nylium', 'nether_gold_ore',
       'nether_quartz_ore', 'magma_block', 'end_stone', 'packed_ice', 'ice', 'dirt_path', 'suspicious_sand', 'suspicious_gravel', 'muddy_mangrove_roots',
       'mangrove_roots']
PLANTS = ['#minecraft:replaceable', '#minecraft:logs', '#minecraft:leaves', 'minecraft:cactus', 'minecraft:sugar_cane', 'minecraft:bamboo',
          'minecraft:pumpkin', 'minecraft:melon', 'minecraft:sweet_berry_bush', 'minecraft:brown_mushroom_block', 'minecraft:red_mushroom_block',
          'minecraft:mushroom_stem', 'minecraft:bee_nest', 'minecraft:moss_carpet', 'minecraft:pale_moss_carpet', 'minecraft:pale_hanging_moss',
          'minecraft:cocoa', 'minecraft:vine', 'minecraft:snow', 'minecraft:crimson_fungus', 'minecraft:warped_fungus', 'minecraft:nether_wart_block',
          'minecraft:warped_wart_block', 'minecraft:shroomlight', 'minecraft:weeping_vines', 'minecraft:weeping_vines_plant', 'minecraft:twisting_vines',
          'minecraft:twisting_vines_plant', 'minecraft:creaking_heart', 'minecraft:resin_clump']
WET = ['minecraft:kelp', 'minecraft:kelp_plant', 'minecraft:seagrass', 'minecraft:tall_seagrass']
HOLE = ['minecraft:air', 'minecraft:cave_air', '#minecraft:replaceable', 'minecraft:snow']
# what the new ground is made of, by biome (top, under): the first that matches
SOILS = [('#minecraft:is_ocean', 'sand', 'sand'), ('#minecraft:is_river', 'sand', 'sand'), ('#minecraft:is_badlands', 'red_sand', 'terracotta'), ('minecraft:desert', 'sand', 'sandstone'),
         ('#minecraft:is_beach', 'sand', 'sand'), ('minecraft:snowy_beach', 'sand', 'sand'), ('minecraft:mushroom_fields', 'mycelium', 'dirt'),
         ('minecraft:old_growth_pine_taiga', 'podzol', 'dirt'), ('minecraft:old_growth_spruce_taiga', 'podzol', 'dirt'),
         ('minecraft:mangrove_swamp', 'mud', 'mud'), ('minecraft:soul_sand_valley', 'soul_soil', 'soul_soil'), ('minecraft:basalt_deltas', 'basalt', 'blackstone'),
         ('minecraft:crimson_forest', 'crimson_nylium', 'netherrack'), ('minecraft:warped_forest', 'warped_nylium', 'netherrack'),
         ('#minecraft:is_nether', 'netherrack', 'netherrack'), ('#minecraft:is_end', 'end_stone', 'end_stone'),
         ('minecraft:snowy_plains', 'snow_block', 'dirt'), ('minecraft:ice_spikes', 'snow_block', 'dirt'), ('minecraft:snowy_slopes', 'snow_block', 'dirt'),
         ('minecraft:grove', 'snow_block', 'dirt'), ('minecraft:frozen_peaks', 'snow_block', 'stone'), ('minecraft:jagged_peaks', 'snow_block', 'stone'),
         ('minecraft:snowy_taiga', 'snow_block', 'dirt'), ('minecraft:stony_shore', 'stone', 'stone'), ('minecraft:stony_peaks', 'stone', 'stone')]

_G = None
DONE = {}


def setup(G):
    """the shared pieces: tags, the soil picker, the loop that settles templates' corner markers"""
    global _G
    if _G is G: return
    _G = G
    G.wjson('bm/tags/block/settle_cut.json', {'values': [f'minecraft:{b}' for b in CUT] + PLANTS})
    G.wjson('bm/tags/block/settle_plant.json', {'values': PLANTS})
    # (3.0h) what a cut to WATER takes: the terrain and the sea's own plants - never air (#replaceable has it), so a cut that
    # reaches over the sea's surface leaves the air there air, not water standing in it
    G.wjson('bm/tags/block/settle_wet.json', {'values': [f'minecraft:{b}' for b in CUT] + WET})
    G.wjson('bm/tags/block/settle_hole.json', {'values': HOLE})
    G.wjson('bm/tags/block/settle_hole_w.json', {'values': HOLE + ['minecraft:water', 'minecraft:seagrass', 'minecraft:tall_seagrass', 'minecraft:kelp',
                                                                   'minecraft:kelp_plant', 'minecraft:bubble_column']})
    pick = ['data modify storage bm:settle top set value "minecraft:grass_block"', 'data modify storage bm:settle sub set value "minecraft:dirt"',
            # (3.0g) the dimension's own ground first, whatever the biome: a pack biome (the Undercrown's, filled over its box) is in
            # no vanilla tag, and the Nether's outposts settled there on grass and banked dirt into the halls below
            'execute if dimension minecraft:the_nether run data modify storage bm:settle top set value "minecraft:netherrack"',
            'execute if dimension minecraft:the_nether run data modify storage bm:settle sub set value "minecraft:netherrack"',
            'execute if dimension minecraft:the_end run data modify storage bm:settle top set value "minecraft:end_stone"',
            'execute if dimension minecraft:the_end run data modify storage bm:settle sub set value "minecraft:end_stone"']
    for b, top, sub in reversed(SOILS):          # (the first match wins, so it's written last)
        pick.append(f'execute if biome ~ ~ ~ {b} run data modify storage bm:settle top set value "minecraft:{top}"')
        pick.append(f'execute if biome ~ ~ ~ {b} run data modify storage bm:settle sub set value "minecraft:{sub}"')
    G.fn('settle/pick', pick)


def _strips(x0, z0, x1, z1, d):
    """the ring d blocks outside the rectangle, as four strips (x0, z0, x1, z1)"""
    a, b, c, e = x0 - d, z0 - d, x1 + d, z1 + d
    return [(a, b, c, b), (a, e, c, e), (a, b + 1, a, e - 1), (c, b + 1, c, e - 1)]


def _body(w, d, *, cut=12, fill=8, deep=16, high=28, water=False, inside=None, under=False, base=0, clear='air', cutset='#bm:settle_cut',
          steep=None, cap=None, sub=None):
    # (3.1c) steep: past that ring, the slope rises two a ring (a deep pit's sides reach the sea floor); cap: every ring is cleared
    # up to that height over the floor (a ridge standing over the slope is cut back too), not just `high` over the slope
    rise = lambda r: r - 1 if steep is None or r <= steep else steep - 1 + 2 * (r - steep)
    # sub: what fills the holes under the floor (not the biome's own: an ocean's is sand, and under a deep sea floor's caves and
    # ravines every block of it fell - thousands of falling blocks at once)
    SUB = sub or '$(sub)'
    x0, z0, x1, z1 = 0, 0, w - 1, d - 1
    hole = '#bm:settle_hole_w' if water else '#bm:settle_hole'
    F = lambda a, y0, y1, blk, rep: f'$fill ~{a[0]} ~{y0} ~{a[1]} ~{a[2]} ~{y1} ~{a[3]} {blk} replace {rep}'
    def slabs(y0, y1):                  # (a fill is at most 32768 blocks: the footprint in slices along x)
        n = max(1, 32768 // ((z1 - z0 + 1) * (y1 - y0 + 1)))
        return [(a, z0, min(a + n - 1, x1), z1) for a in range(x0, x1 + 1, n)]
    out = []
    if inside:      # terrain standing in the footprint above the floor (a hill through a courtyard)
        out += [F(a, 0, high, f'minecraft:{clear}', inside).replace('$fill', 'fill', 1) for a in slabs(0, high)]
    if under:       # holes under the floor
        if base:    # (under the template's own underground part)
            out += [F(a, -base - deep, -base - 1, SUB, hole) for a in slabs(-base - deep, -base - 1)]
        else:
            out += [F(a, -deep, -2, SUB, hole) for a in slabs(-deep, -2)]
            out += [F(a, -1, -1, '$(top)', hole) for a in slabs(-1, -1)]
    for r in range(1, max(cut, fill) + 1):
        for s in _strips(x0, z0, x1, z1, r):
            if r <= cut and (cap is None or rise(r) <= cap):
                out.append(F(s, rise(r), cap if cap is not None else rise(r) + high, f'minecraft:{clear}', cutset).replace('$fill', 'fill', 1))
                if clear == 'air': out.append(F(s, r - 2, r - 2, '$(top)', 'minecraft:dirt'))
            if r <= fill:      # (3.1c: the layers under first, then the top: sand set over a hole fell, a column at a time)
                if r < deep: out.append(F(s, -deep, -r - 1, SUB, hole))
                out.append(F(s, -r, -r, '$(top)', hole))
    return [l[1:] if l.startswith('$') and '$(' not in l else l for l in out]      # (a macro line must use a macro: a fixed `sub` doesn't)


def make(G, name, w, d, turn=False, **kw):
    """bm:settle/<name>/a (w x d), and for a template that may be turned /b (d x w); run at the low corner, on the floor,
    `with storage bm:settle`"""
    setup(G)
    G.fn(f'settle/{name}/a', _body(w, d, **kw))
    if turn: G.fn(f'settle/{name}/b', _body(d, w, **kw) if w != d else [f'$function bm:settle/{name}/a {{top:"$(top)",sub:"$(sub)"}}'])
    DONE[name] = (w, d, max(kw.get('cut', 12), kw.get('fill', 8)), turn)


def run(name, ox, oy, oz):
    """the commands a runtime builder adds (from where it runs: the low corner is at ~ox ~oy ~oz)"""
    return [f'execute positioned ~{ox} ~{oy} ~{oz} run function bm:settle/pick',
            f'execute positioned ~{ox} ~{oy} ~{oz} run function bm:settle/{name}/a with storage bm:settle']


def mark(Bd, name, x0, z0, x1, z1, y):
    """the template's four corner markers"""
    for x in (x0, x1):
        for z in (z0, z1):
            Bd.marker(x + 0.5, y, z + 0.5, ['bm.settle', f'bm.st_{name}'], 0)


def corners(G, Bd, name, x0, z0, x1, z1, y, second):
    """a jigsaw template's footprint: a marker at each corner (Bd None: the caller marks it later, with mark()); when someone
    is near, the one at the low corner settles it"""
    w, d = x1 - x0 + 1, z1 - z0 + 1
    assert DONE.get(name, ())[:2] == (w, d) and DONE[name][3], f'settle/{name} must be made first, with turn=True'
    R = DONE[name][2]
    tag = f'bm.st_{name}'
    if Bd is not None: mark(Bd, name, x0, z0, x1, z1, y)
    G.fn(f'settle/{name}/try', [
        f'execute unless loaded ~-{R} ~ ~-{R} run return 0',
        f'execute positioned ~{w - 1} ~ ~{d - 1} if loaded ~{R} ~ ~{R} if entity @e[type=minecraft:marker,tag={tag},distance=..0.8] run return run function bm:settle/{name}/go_a',
        f'execute positioned ~{d - 1} ~ ~{w - 1} if loaded ~{R} ~ ~{R} if entity @e[type=minecraft:marker,tag={tag},distance=..0.8] run return run function bm:settle/{name}/go_b'])
    for k, (a, b) in (('a', (w, d)), ('b', (d, w))):
        G.fn(f'settle/{name}/go_{k}', ['function bm:settle/pick', f'function bm:settle/{name}/{k} with storage bm:settle',
                                       f'kill @e[type=minecraft:marker,tag={tag},dx={a - 1},dy=1,dz={b - 1}]'])
    second.append(f'execute as @e[type=minecraft:marker,tag={tag}] at @s if entity @a[distance=..96] run function bm:settle/{name}/try')

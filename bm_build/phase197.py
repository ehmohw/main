"""2.88: THE DREAD BOSSES - three hard-mode horrors, each waiting at its own ruin for someone who brings the right three friends.
(snowbeast_art.py, witch_art.py, sawshark_art.py, after the owner's drawings.)

THE MALEVOLENT SNOWBEAST (the Frozen Folly, in snowy lands). Pistachio's living top hat took fright and came down on a snowman -
  and made a monster of it. It hurls volleys of ice shards that slow and freeze, slams a frost nova into the ground, stares
  a beam of cold out of the hat's eyes, and at half health it roars up a blizzard and calls strays out of the snow.
  Its altar wakes for PISTACHIO, CELI and TULLIUS (his hat; the snow; the ice).
THE WATCHFUL WITCH (the Hexen Hollow, in dark forests and swamps). An old acquaintance of Cecil's who studied dark magic a little
  too hard, and was swallowed by it. She drifts out of reach throwing hex bolts that wither, blinks away from anyone who
  closes in, rings you with curse circles that burst (step out!), and at half health she drains the life out of you and
  calls up her shades. Her altar wakes for CECIL, APOPHISS and KING OMEGA (her old friend; the serpent; the dead).
THE CHOMPING SAWSHARK (the Drowned Gate, on the deep sea floor). Woken in the great war; it has kept the Underwater Kingdom from
  surfacing ever since, and they say it swallowed Democratus whole. It chomps, rakes with its saw, charges through the water,
  drags you into a whirlpool, and at half health it calls guardians to its side. Its altar wakes for EMMA, BONES and QUEEN PEARL
  (the kingdom's own).
Hard mode only. The altar (right-click it) says who's missing. Beat one and everyone near gets its TOKEN, Dread Tokens and spoils.

THE TOKENS: carried (anywhere on you), a strong blessing; set down on a block (sneak + use), a ward around it for everyone
  (sneak + punch to take it back); or Vesper scraps one for 12 Dread Tokens.
  Frostbitten Token  carried: Resistance, and cold can't slow or freeze you. Set down: monsters within 16 slowed and weakened; Resistance for all.
  Hexbound Token     carried: Strength, Night Vision; monsters within 6 of you weakened. Set down: monsters within 16 seared and lit up; Strength and Regeneration for all.
  Sawtooth Token     carried: Water Breathing, Dolphin's Grace, Conduit Power, Strength in water. Set down: in water within 24, Conduit Power,
                     Dolphin's Grace and Regeneration - and monsters in the water take a bite.
THE MAPS: Vesper, now and then, sells a sealed map to each ruin (dear: 20 Dread Tokens)."""
import math
from items import item, T, TOTEM, ITEMS, consumable
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import rigfol as RF
import phase177 as P177
import snowbeast_art, witch_art, sawshark_art

DREAD = '#b0102a'
holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
FLOOR = 200          # (each host's health above its "real" pool: at this, it falls - no lucky blow kills it outright)

BOSSES = {
    'snow': dict(NAME='The Malevolent Snowbeast', COL='#9ad8ff', A=snowbeast_art, host='husk', hp=720, scale=2.6, armor=10, move='ground', speed=0.17,
                 bar='blue', token='tok_frost', ruin='Frozen Folly', ruin_col='#bfe8ff', map='sealed_map_db_snow', mapname='Frostbitten Map',
                 trio=[('Pistachio', 'bm.pipet'), ('Celi', 'bm.celipet'), ('Tullius', 'bm.tupet')],
                 biomes=['minecraft:snowy_plains', 'minecraft:ice_spikes', 'minecraft:snowy_taiga', 'minecraft:grove', 'minecraft:snowy_slopes',
                         'minecraft:frozen_peaks', 'minecraft:jagged_peaks', 'minecraft:snowy_beach'],
                 rise=('The snow on the altar heaves...', 'Somewhere, a hat screams.'),
                 lore='Pistachio\'s living hat, frightened, came down on a snowman - and made a monster of it.'),
    'witch': dict(NAME='The Watchful Witch', COL='#7aff5a', A=witch_art, host='husk', hp=640, scale=1.5, armor=6, move='float', speed=0.2,
                  bar='green', token='tok_hex', ruin='Hexen Hollow', ruin_col='#a8ff8a', map='sealed_map_db_witch', mapname='Hexed Map',
                  trio=[('Cecil', 'bm.cecilpet'), ('Apophiss', 'bm.appet'), ('King Omega', 'bm.ompet')],
                  biomes=['minecraft:dark_forest', 'minecraft:swamp', 'minecraft:mangrove_swamp', 'minecraft:pale_garden', 'minecraft:old_growth_spruce_taiga'],
                  rise=('The cauldron boils over with shadow...', 'Someone is watching. Someone has always been watching.'),
                  lore='An old acquaintance of Cecil\'s who studied dark magic a little too hard - and was swallowed by it.'),
    'shark': dict(NAME='The Chomping Sawshark', COL='#ffd21a', A=sawshark_art, host='drowned', hp=820, scale=3.4, armor=12, move='swim', speed=0.3,
                  bar='white', token='tok_saw', ruin='Drowned Gate', ruin_col='#8ae8d8', map='sealed_map_db_shark', mapname='Drowned Map',
                  trio=[('Emma', 'bm.emmapet'), ('Bones', 'bm.bjpet'), ('Queen Pearl', 'bm.pqpet')],
                  biomes=['minecraft:deep_ocean', 'minecraft:deep_cold_ocean', 'minecraft:deep_lukewarm_ocean', 'minecraft:deep_frozen_ocean',
                          'minecraft:ocean', 'minecraft:cold_ocean', 'minecraft:lukewarm_ocean'],
                  rise=('The water at the gate goes still. Then it doesn\'t.', 'Teeth. So many teeth.'),
                  lore='Woken in the great war, it has kept the Underwater Kingdom from surfacing ever since. They say it swallowed Democratus whole.'),
}
TOKENS = {
    'tok_frost': ('Frostbitten Token', '#9ad8ff', 'snow', ['A disc of ice that never melts, a top hat stamped into it.', 'It is cold enough to burn.'],
                  'Carried: Resistance; cold can\'t slow or freeze you.', 'Set down: monsters within 16 slowed and weakened; Resistance for all.'),
    'tok_hex': ('Hexbound Token', '#7aff5a', 'witch', ['A coin of black glass. A green eye opens in it when you look away.'],
                'Carried: Strength and Night Vision; monsters within 6 of you weakened.', 'Set down: monsters within 16 seared and lit up; Strength and Regeneration for all.'),
    'tok_saw': ('Sawtooth Token', '#ffd21a', 'shark', ['One of its saw\'s teeth, as long as your hand, set in old gold.'],
                'Carried: Water Breathing, Dolphin\'s Grace, Conduit Power - and Strength in water.',
                'Set down: in the water within 24, Conduit Power, Dolphin\'s Grace and Regeneration - and monsters there take a bite.'),
}
for iid, (nm, col, k, lore, carried, placed) in TOKENS.items():
    item(iid, TOTEM, nm, col, lore + [(carried, 'blue'), (placed, 'blue'), ('Sneak + use on a block: set it down. Sneak + punch: take it back.', 'gray'),
                                     ('Vesper scraps it for 12 Dread Tokens.', 'gray'), (f'Dropped by {BOSSES[k]["NAME"]}.', 'dark_gray')],
         model=f'bm:{iid}', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
    HOLD[iid] = f'bm:p197/tok/{k}/use'
for k, b in BOSSES.items():
    item(b['map'], TOTEM, f'Sealed {b["mapname"]}', b['COL'],
         ['Hold right-click to break the seal.', f'Marks the nearest {b["ruin"]} -', f'where {b["NAME"]} waits.', ('Hard mode only.', 'dark_red')],
         model='minecraft:map', glint=True, stack=16, comps={'minecraft:consumable': consumable(0.8, 'none', 'minecraft:item.book.page_turn', False)}, cat='map')
P177.STOCK += [(b['map'], 1, 20) for b in BOSSES.values()]
P177.EXTRA += [((iid, 1), ('dread_token', 12)) for iid in TOKENS]


def extend_offers(O, offer):
    pass


def _icons():
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    out = {}
    for iid, (outer, inner, mark) in {'tok_frost': ('#5aa8d8', '#dff6ff', '#1e1a22'), 'tok_hex': ('#0a060e', '#2a1a3a', '#7aff5a'),
                                      'tok_saw': ('#b8862a', '#ffe08a', '#f4f0e0')}.items():
        im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.ellipse((1, 1, 14, 14), fill=hexc(outer)); d.ellipse((3, 3, 12, 12), fill=hexc(inner))
        if iid == 'tok_frost':                                                          # a little top hat stamped in the ice
            d.rectangle((5, 5, 10, 9), fill=hexc(mark)); d.rectangle((4, 9, 11, 10), fill=hexc(mark)); d.point((6, 7), fill=hexc('#f4f0e8')); d.point((9, 7), fill=hexc('#f4f0e8'))
        elif iid == 'tok_hex':                                                          # the green eye
            d.ellipse((4, 6, 11, 9), fill=hexc(mark)); d.rectangle((7, 6, 8, 9), fill=hexc('#0a060e'))
        else:                                                                           # the saw tooth
            d.polygon([(7, 3), (10, 12), (5, 12)], fill=hexc(mark), outline=hexc('#9a8e70'))
        d.point((4, 4), fill=hexc('#ffffff'))
        out[iid] = im
    return out


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    for k, b in BOSSES.items():
        A = b['A']
        for name, (tex, els) in A.models().items():
            R.HATS[name] = (tex, els)
        R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (A.PREFIX,)
    R.ICONS.update(_icons())


def textures():
    out = {}
    for b in BOSSES.values():
        out.update(b['A'].textures())
    return out


def generate_early(G):
    pass


def generate(G):
    fn, wjson, tellraw, title, give = G.fn, G.wjson, G.tellraw, G.title, G.give
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    tick, fast, second = [], [], []
    objs = ['bm.dbid', 'bm.dbs', 'bm.dbf', 'bm.dbx', 'bm.dba', 'bm.dbph', 'bm.dbgone', 'bm.dbk7', 'bm.dbk8', 'bm.dbk9', 'bm.dbk11', 'bm.dbk12', 'bm.dbt',
            'bm.dbwin_snow', 'bm.dbwin_witch', 'bm.dbwin_shark']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + ['scoreboard players set #2 bm.rng 2', 'scoreboard players set #9 bm.rng 9',
                                                                                     'scoreboard players set #5 bm.rng 5', 'scoreboard players set #10 bm.rng 10']
    G.OBJECTIVES += objs
    foe_tgt = '@a[tag=bm.dbtgt,limit=1]'
    me = '@e[tag=bm.dbme,limit=1]'
    hit = lambda n, extra='': f'damage @s {n} minecraft:mob_attack by {me}' + extra

    # ================================================================== the ruins: rare, built when someone first comes near
    wjson('bm/tags/block/db_clear.json', {'values': ['#minecraft:replaceable', 'minecraft:snow', 'minecraft:ice', 'minecraft:cactus', 'minecraft:sugar_cane',
                                                     'minecraft:kelp', 'minecraft:kelp_plant', 'minecraft:seagrass', 'minecraft:tall_seagrass', '#minecraft:leaves',
                                                     '#minecraft:logs', 'minecraft:mangrove_roots', 'minecraft:vine', 'minecraft:powder_snow']})
    from structures import Build
    for i, (k, b) in enumerate(BOSSES.items()):
        wjson(f'bm/tags/worldgen/biome/has_structure/db_{k}.json', {'values': b['biomes']})
        wjson(f'bm/tags/worldgen/structure/db_{k}_ruin.json', {'values': [f'bm:db_{k}']})
        wjson(f'bm/worldgen/structure/db_{k}.json', {'type': 'minecraft:jigsaw', 'biomes': f'#bm:has_structure/db_{k}', 'step': 'surface_structures',
                                                     'spawn_overrides': {}, 'terrain_adaptation': 'none', 'start_pool': f'bm:db_{k}/start', 'size': 1,
                                                     'start_height': {'absolute': 0},
                                                     'project_start_to_heightmap': 'OCEAN_FLOOR_WG' if b['move'] == 'swim' else 'WORLD_SURFACE_WG',
                                                     'max_distance_from_center': 80, 'use_expansion_hack': False, 'liquid_settings': 'ignore_waterlogging'})
        wjson(f'bm/worldgen/template_pool/db_{k}/start.json', {'fallback': 'minecraft:empty', 'elements': [
            {'weight': 1, 'element': {'element_type': 'minecraft:single_pool_element', 'location': f'bm:db_{k}', 'projection': 'rigid', 'processors': 'minecraft:empty'}}]})
        wjson(f'bm/worldgen/structure_set/db_{k}.json', {'structures': [{'structure': f'bm:db_{k}', 'weight': 1}],
                                                         'placement': {'type': 'minecraft:random_spread', 'spacing': 56, 'separation': 24, 'salt': 88197310 + i * 7919}})
        Bd = Build(1, 1, 1)
        Bd.marker(0.5, 0.0, 0.5, [f'bm.db{k}_seed'], 0)
        Bd.export(G.path('data', 'bm', 'structure', f'db_{k}.nbt'))
        second.append(f'execute as @e[type=minecraft:marker,tag=bm.db{k}_seed] at @s if entity @a[distance=..96] if loaded ~-11 ~ ~-11 if loaded ~11 ~ ~11 run function bm:p197/{k}/ruin/seed')
        fn(f'p197/{k}/ruin/seed', ['kill @s', f'function bm:p197/{k}/ruin/build'])
        # the sealed map (Vesper's): the nearest of these ruins
        G.consume_adv(b['map'], f'bm:maps/open_db_{k}')
        G.sealed_map(b['map'], f'db_{k}', f'#bm:db_{k}_ruin', title('@s', 'actionbar', T(f'The seal cracks... the map marks the {b["ruin"]}.', b['COL'])))
        wjson(f'bm/loot_table/maps/db_{k}.json', {'type': 'minecraft:command', 'pools': [{'rolls': 1, 'entries': [{
            'type': 'minecraft:item', 'name': 'minecraft:filled_map', 'functions': [
                {'function': 'minecraft:exploration_map', 'destination': f'#bm:db_{k}_ruin', 'decoration': 'minecraft:red_x', 'zoom': 2,
                 'search_radius': 100, 'skip_existing_chunks': False},
                {'function': 'minecraft:set_name', 'target': 'item_name', 'name': T(b['mapname'], b['COL'])}]}]}]})
        fn(f'admin/db_{k}_ruin', [f'function bm:p197/{k}/ruin/build', tellraw('@s', G.PREFIX + [T(f'The {b["ruin"]} is built here.', 'gray')])])

    def ring(r, n, blk, y0, heights, ox=0, oz=0):
        """a broken ring of pillars: n of them round radius r, each its own height"""
        out = []
        for j in range(n):
            a = 2 * math.pi * j / n
            x, z = round(ox + r * math.cos(a)), round(oz + r * math.sin(a))
            h = heights[j % len(heights)]
            if h > 0:
                out.append(f'fill ~{x} ~{y0} ~{z} ~{x} ~{y0 + h - 1} ~{z} minecraft:{blk}')
        return out
    altar = lambda k: [f'summon minecraft:interaction ~ ~1 ~ {{Tags:["bm.dbaltar","bm.dbaltar_{k}"],width:1.6f,height:2.2f,response:1b}}',
                       f'summon minecraft:marker ~ ~ ~ {{Tags:["bm.dbruin","bm.dbruin_{k}"]}}']
    # -- the Frozen Folly: a frozen court of broken ice pillars, a dais of quartz and blue ice, the altar a frozen hat-stand
    fn('p197/snow/ruin/build', ['fill ~-11 ~ ~-11 ~11 ~10 ~11 minecraft:air replace #bm:db_clear',
                                'fill ~-10 ~-4 ~-10 ~10 ~-2 ~10 minecraft:snow_block replace #bm:p96_fill',
                                'fill ~-10 ~-1 ~-10 ~10 ~-1 ~10 minecraft:packed_ice', 'fill ~-7 ~-1 ~-7 ~7 ~-1 ~7 minecraft:snow_block',
                                'fill ~-3 ~-1 ~-3 ~3 ~-1 ~3 minecraft:quartz_bricks', 'fill ~-1 ~ ~-1 ~1 ~ ~1 minecraft:blue_ice',
                                'setblock ~ ~1 ~ minecraft:chiseled_quartz_block', 'setblock ~ ~2 ~ minecraft:black_carpet'] +
       ring(9, 10, 'packed_ice', 0, [5, 2, 6, 0, 4, 3, 6, 1, 5, 2]) + ring(9, 10, 'blue_ice', 0, [1, 0, 2, 0, 1, 0, 2, 0, 1, 0]) +
       ['fill ~-9 ~6 ~-1 ~-9 ~6 ~3 minecraft:packed_ice', 'fill ~6 ~5 ~6 ~8 ~5 ~6 minecraft:packed_ice',                 # (broken lintels)
        'setblock ~-2 ~ ~-2 minecraft:soul_lantern', 'setblock ~2 ~ ~-2 minecraft:soul_lantern', 'setblock ~-2 ~ ~2 minecraft:soul_lantern', 'setblock ~2 ~ ~2 minecraft:soul_lantern',
        'fill ~-10 ~ ~-10 ~10 ~ ~10 minecraft:snow[layers=2] replace minecraft:air', 'fill ~-3 ~ ~-3 ~3 ~ ~3 minecraft:air replace minecraft:snow',
        'setblock ~-2 ~ ~-2 minecraft:soul_lantern', 'setblock ~2 ~ ~-2 minecraft:soul_lantern', 'setblock ~-2 ~ ~2 minecraft:soul_lantern', 'setblock ~2 ~ ~2 minecraft:soul_lantern'] + altar('snow'))
    # -- the Hexen Hollow: a ring of mossy walls and blackstone, crooked posts with skulls, cobwebs, the cauldron altar
    fn('p197/witch/ruin/build', ['fill ~-11 ~ ~-11 ~11 ~10 ~11 minecraft:air replace #bm:db_clear',
                                 'fill ~-10 ~-4 ~-10 ~10 ~-2 ~10 minecraft:dirt replace #bm:p96_fill',
                                 'fill ~-10 ~-1 ~-10 ~10 ~-1 ~10 minecraft:podzol', 'fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 minecraft:coarse_dirt',
                                 'fill ~-3 ~-1 ~-3 ~3 ~-1 ~3 minecraft:polished_blackstone_bricks', 'fill ~-1 ~-1 ~-1 ~1 ~-1 ~1 minecraft:crying_obsidian',
                                 'setblock ~ ~ ~ minecraft:cauldron', 'setblock ~ ~-1 ~ minecraft:soul_campfire'] +
       ring(9, 12, 'mossy_cobblestone', 0, [3, 1, 4, 2, 0, 3, 2, 4, 1, 0, 3, 2]) + ring(9, 12, 'blackstone', 0, [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0]) +
       ring(6, 6, 'dark_oak_fence', 0, [2, 2, 2, 2, 2, 2]) +
       ['setblock ~6 ~2 ~0 minecraft:skeleton_skull', 'setblock ~-3 ~2 ~5 minecraft:skeleton_skull', 'setblock ~-3 ~2 ~-5 minecraft:wither_skeleton_skull',
        'setblock ~-6 ~2 ~0 minecraft:skeleton_skull', 'setblock ~3 ~2 ~5 minecraft:wither_skeleton_skull', 'setblock ~3 ~2 ~-5 minecraft:skeleton_skull',
        'setblock ~-8 ~1 ~-4 minecraft:cobweb', 'setblock ~7 ~1 ~5 minecraft:cobweb', 'setblock ~4 ~ ~-8 minecraft:cobweb',
        'setblock ~-2 ~ ~2 minecraft:soul_lantern', 'setblock ~2 ~ ~-2 minecraft:soul_lantern', 'setblock ~5 ~ ~5 minecraft:dead_bush', 'setblock ~-5 ~ ~-5 minecraft:dead_bush'] + altar('witch'))
    # -- the Drowned Gate: a sunken court of prismarine on the sea floor, a broken arch, sea lanterns, the gate's altar
    fn('p197/shark/ruin/build', ['fill ~-11 ~ ~-11 ~11 ~12 ~11 minecraft:water replace #bm:db_clear',
                                 'fill ~-10 ~-3 ~-10 ~10 ~-2 ~10 minecraft:prismarine replace #bm:p96_fill',
                                 'fill ~-10 ~-1 ~-10 ~10 ~-1 ~10 minecraft:dark_prismarine', 'fill ~-3 ~-1 ~-3 ~3 ~-1 ~3 minecraft:prismarine_bricks',
                                 'fill ~-1 ~ ~-1 ~1 ~ ~1 minecraft:prismarine_bricks', 'setblock ~ ~1 ~ minecraft:sea_lantern'] +
       ring(9, 10, 'prismarine_bricks', 0, [6, 3, 7, 0, 5, 2, 7, 4, 1, 5]) +
       ['fill ~-3 ~ ~-10 ~-3 ~8 ~-10 minecraft:prismarine_bricks', 'fill ~3 ~ ~-10 ~3 ~8 ~-10 minecraft:prismarine_bricks',          # the gate's arch (broken)
        'fill ~-3 ~9 ~-10 ~1 ~9 ~-10 minecraft:prismarine_bricks', 'setblock ~-2 ~8 ~-10 minecraft:sea_lantern', 'setblock ~2 ~8 ~-10 minecraft:sea_lantern',
        'setblock ~-6 ~-1 ~6 minecraft:sea_lantern', 'setblock ~6 ~-1 ~-6 minecraft:sea_lantern', 'setblock ~6 ~-1 ~6 minecraft:sea_lantern', 'setblock ~-6 ~-1 ~-6 minecraft:sea_lantern',
        'fill ~-8 ~ ~-8 ~8 ~ ~8 minecraft:tall_seagrass[half=lower] replace minecraft:water', 'fill ~-8 ~1 ~-8 ~8 ~1 ~8 minecraft:tall_seagrass[half=upper] replace minecraft:water',
        'fill ~-4 ~ ~-4 ~4 ~1 ~4 minecraft:water replace minecraft:tall_seagrass'] + altar('shark'))

    # ================================================================== the altar: right-click it - the trio, or not
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.dbaltar] if data entity @s interaction at @s run function bm:p197/altar/click')
    fn('p197/altar/click', ['tag @s add bm.dbhere', 'execute on target run function bm:p197/altar/ask', 'tag @s remove bm.dbhere', 'data remove entity @s interaction'])
    fn('p197/altar/ask', [f'execute if entity @e[tag=bm.dbhere,tag=bm.dbaltar_{k}] run return run function bm:p197/{k}/ask' for k in BOSSES])
    for k, b in BOSSES.items():
        trio = b['trio']
        lines = ['execute unless score #hard bm.cfg matches 1 run return run ' + say(f'The altar is cold. (Hard mode only.)', '#c8a0a0'),
                 f'execute at @e[tag=bm.dbhere,limit=1] if entity @e[tag=bm.db_{k},distance=..96] run return run ' + say(f'{b["NAME"]} is already awake.', b['COL']),
                 'scoreboard players operation #me bm.pid = @s bm.pid']
        for j, (nm, tag) in enumerate(trio):
            lines += [f'scoreboard players set #t{j} bm.rng 0', f'execute as @e[tag={tag},distance=..24] if score @s bm.pid = #me bm.pid run scoreboard players set #t{j} bm.rng 1']
        lines += ['scoreboard players set #tn bm.rng 0'] + [f'scoreboard players operation #tn bm.rng += #t{j} bm.rng' for j in range(3)]
        lines += [f'execute if score #tn bm.rng matches 3 at @e[tag=bm.dbhere,limit=1] run return run function bm:p197/{k}/rise']
        names = []
        for j, (nm, tag) in enumerate(trio):
            fn(f'p197/{k}/who{j}', [f'execute if score #t{j} bm.rng matches 1 run return run ' + tellraw('@s', [T('  ✔ ', 'green'), T(nm, 'green')]),
                                    tellraw('@s', [T('  ✘ ', 'dark_gray'), T(nm, 'gray'), T(' (not with you)', 'dark_gray')])])
            names.append(f'function bm:p197/{k}/who{j}')
        lines += ['playsound minecraft:block.respawn_anchor.deplete block @s ~ ~ ~ 0.6 0.6',
                  tellraw('@s', [T(f'The {b["ruin"]}: ', b['ruin_col'], bold=True), T(f'the altar will wake {b["NAME"]} only for these three, together:', 'gray')])] + names
        fn(f'p197/{k}/ask', lines)

    # ================================================================== each boss: its rig, its mind, its fall
    for k, b in BOSSES.items():
        build_boss(G, k, b, tick, second, fast)

    # ================================================================== the tokens: carried, set down, taken back
    for iid, (nm, col, k, *_r) in TOKENS.items():
        second += [f'execute as @a if items entity @s container.* {holds(iid)} at @s run function bm:p197/tok/{k}/carry',
                   f'execute as @a unless items entity @s container.* {holds(iid)} if items entity @s weapon.offhand {holds(iid)} at @s run function bm:p197/tok/{k}/carry']
        fn(f'p197/tok/{k}/use', ['execute unless predicate bm:p20/sneaking run return run ' + say(f'Sneak + use on a block: set the {nm} down - a ward for everyone near it.', col),
                                 'scoreboard players set #placed bm.rng 0', 'scoreboard players set #ray bm.rng 25', 'tag @s add bm.placer',
                                 f'execute anchored eyes positioned ^ ^ ^ run function bm:p197/tok/{k}/ray', 'tag @s remove bm.placer',
                                 'execute if score #placed bm.rng matches 0 run return run ' + say('Look at the top of a block within 5 blocks.'),
                                 f'clear @s {holds(iid)} 1'])
        fn(f'p197/tok/{k}/ray', [f'execute unless block ~ ~ ~ #minecraft:replaceable run return run function bm:p197/tok/{k}/hit',
                                 'scoreboard players remove #ray bm.rng 1', f'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p197/tok/{k}/ray'])
        fn(f'p197/tok/{k}/hit', ['execute align xyz positioned ~0.5 ~1 ~0.5 unless block ~ ~ ~ #minecraft:replaceable run return 0',
                                 'execute align xyz positioned ~0.5 ~1 ~0.5 if entity @e[type=minecraft:interaction,tag=bm.dbshrine,distance=..0.6] run return 0',
                                 f'execute align xyz positioned ~0.5 ~1 ~0.5 run function bm:p197/tok/{k}/place', 'scoreboard players set #placed bm.rng 1'])
        ident = [F(0), F(0), F(0), F(1)]
        fn(f'p197/tok/{k}/place', ['summon minecraft:item_display ~ ~ ~ ' + snbt({'Tags': ['bm.dbshrined', f'bm.dbshrined_{k}', 'bm.hnew'],
                                                                                   'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:{iid}'}},
                                                                                   'item_display': 'fixed', 'billboard': 'vertical', 'brightness': {'sky': Int(15), 'block': Int(15)},
                                                                                   'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.6), F(0)],
                                                                                                      'scale': [F(0.9)] * 3}}),
                                   'summon minecraft:interaction ~ ~ ~ ' + snbt({'Tags': ['bm.dbshrine', f'bm.dbshrine_{k}', 'bm.gvdeco', 'bm.hnew'], 'width': F(0.7), 'height': F(1.0), 'response': B(1)}),
                                   'tag @e[tag=bm.hnew,distance=..0.5] remove bm.hnew',
                                   f'particle minecraft:end_rod ~ ~0.6 ~ 0.3 0.3 0.3 0.05 20', 'playsound minecraft:block.beacon.activate block @a[distance=..16] ~ ~ ~ 0.8 1.4',
                                   title('@a[tag=bm.placer]', 'actionbar', T(f'The {nm} wards this place. (Sneak + punch it to take it back.)', col))])
        G.FUNCS['p71/deco/pick'][0:0] = [f'execute if entity @e[type=minecraft:interaction,tag=bm.gvdme,tag=bm.dbshrine_{k}] at @e[type=minecraft:interaction,tag=bm.gvdme,limit=1] '
                                         f'run function bm:p197/tok/{k}/take']
        fn(f'p197/tok/{k}/take', [give(iid), f'kill @e[type=minecraft:item_display,tag=bm.dbshrined_{k},distance=..0.6]',
                                  'playsound minecraft:block.beacon.deactivate block @a[distance=..16] ~ ~ ~ 0.8 1.4'])
        second.append(f'execute as @e[type=minecraft:interaction,tag=bm.dbshrine_{k}] at @s run function bm:p197/tok/{k}/ward')
    foe = 'type=#bm:hostile,tag=!bm.npc'
    fn('p197/tok/snow/carry', ['effect give @s minecraft:resistance 3 0 true', 'effect clear @s minecraft:slowness', 'data modify entity @s TicksFrozen set value 0'])
    fn('p197/tok/witch/carry', ['effect give @s minecraft:strength 3 0 true', 'effect give @s minecraft:night_vision 15 0 true',
                                f'effect give @e[{foe},distance=..6] minecraft:weakness 3 0'])
    fn('p197/tok/shark/carry', ['effect give @s minecraft:water_breathing 3 0 true', 'effect give @s minecraft:dolphins_grace 3 0 true',
                                'effect give @s minecraft:conduit_power 3 0 true', 'execute if predicate bm:swim run effect give @s minecraft:strength 3 0 true',
                                'execute if block ~ ~ ~ minecraft:water run effect give @s minecraft:strength 3 0 true'])
    fn('p197/tok/snow/ward', [f'effect give @e[{foe},distance=..16] minecraft:slowness 3 1', f'effect give @e[{foe},distance=..16] minecraft:weakness 3 0',
                              'effect give @a[distance=..16] minecraft:resistance 3 0 true', 'particle minecraft:snowflake ~ ~0.8 ~ 0.4 0.4 0.4 0.01 4'])
    fn('p197/tok/witch/ward', [f'execute as @e[{foe},distance=..16] run damage @s 2 minecraft:magic', f'effect give @e[{foe},distance=..16] minecraft:glowing 3 0',
                               'effect give @a[distance=..16] minecraft:strength 3 0 true', 'effect give @a[distance=..16] minecraft:regeneration 3 0 true',
                               'particle minecraft:dust{color:[0.48,1.0,0.35],scale:1.0} ~ ~0.8 ~ 0.4 0.4 0.4 0 4'])
    fn('p197/tok/shark/ward', ['execute as @a[distance=..24] at @s if block ~ ~ ~ minecraft:water run function bm:p197/tok/shark/blessed',
                               f'execute as @e[{foe},distance=..24] at @s if block ~ ~ ~ minecraft:water run damage @s 2 minecraft:mob_attack',
                               'particle minecraft:nautilus ~ ~1.2 ~ 0.5 0.5 0.5 0.3 3'])
    fn('p197/tok/shark/blessed', ['effect give @s minecraft:conduit_power 3 0 true', 'effect give @s minecraft:dolphins_grace 3 0 true', 'effect give @s minecraft:regeneration 3 0 true'])

    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.dbr]', 'execute as @e[tag=bm.db] run tp @s ~ -400 ~',
                                       'kill @e[type=minecraft:marker,tag=bm.dbshot]', 'kill @e[type=minecraft:marker,tag=bm.dbcurse]'] + \
                                      [f'bossbar remove bm:db_{k}' for k in BOSSES]
    _shots(G, tick)
    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    f[-1:-1] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


def build_boss(G, k, b, tick, second, fast):
    fn, tellraw, title, give = G.fn, G.tellraw, G.title, G.give
    A = b['A']; S = A.RIG_SCALE; U = S / 16; pfx = f'p197/{k}'
    me = '@e[tag=bm.dbme,limit=1]'
    tgt = '@a[tag=bm.dbtgt,limit=1]'
    hp_max = b['hp'] + FLOOR
    psel = lambda p=None: f'@e[type=minecraft:item_display,tag=bm.dbsel' + (f',tag=bm.dbr_{k}_{p}]' if p else ']')

    # ---- the rig and its poses (the head's model per expression)
    G.FUNCS['load'][-1:-1] = [f'bossbar add bm:db_{k} {snbt(T(b["NAME"], b["COL"]))}', f'bossbar set bm:db_{k} color {b["bar"]}',
                              f'bossbar set bm:db_{k} max {b["hp"]}', f'bossbar set bm:db_{k} style notched_10']
    rig = [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, ["bm.dbr", f"bm.dbr_{k}", f"bm.dbr_{k}_{p}", "bm.dbnew"], S, extra=dict(view_range=F(2.5), brightness={"block": Int(12), "sky": Int(12)}))}'
           for p in A.PARTS]
    fn(f'{pfx}/place', RF.place(A, U, psel))
    poses = sorted({p for _per, fr in CYC[k].values() for _t, p in fr})
    for name in poses:
        fn(f'{pfx}/pose/{name}', RF.pose(A, A.POSES[name], S, DUR.get(name, 6), psel, swap=('head',)))
    RF.cycles(fn, pfx, CYC[k], 'bm.dbf', 'bm.dbs', lambda p: f'{pfx}/pose/{p}')
    G.FUNCS['load'][-1:-1] = [f'scoreboard players set #{n} bm.rng {n}' for n in RF.periods(CYC[k])]

    # ---- rising at its altar
    host = {'Tags': ['bm.db', f'bm.db_{k}', 'bm.dbnew', 'bm.boss', 'bm.seen'], 'NoAI': B(1), 'Silent': B(1), 'PersistenceRequired': B(1),
            'CustomName': T(b['NAME'], b['COL']), 'Invulnerable': B(1), 'NoGravity': B(1 if b['move'] != 'ground' else 0),
            'attributes': [{'id': 'minecraft:max_health', 'base': D(hp_max)}, {'id': 'minecraft:scale', 'base': D(b['scale'])},
                           {'id': 'minecraft:armor', 'base': D(b['armor'])}, {'id': 'minecraft:knockback_resistance', 'base': D(1.0)},
                           {'id': 'minecraft:follow_range', 'base': D(48)}],
            'Health': F(hp_max), 'active_effects': [{'id': 'minecraft:invisibility', 'duration': Int(-1), 'amplifier': B(0), 'show_particles': B(0)},
                                                    {'id': 'minecraft:fire_resistance', 'duration': Int(-1), 'amplifier': B(0), 'show_particles': B(0)}]}
    off = {'snow': '~ ~ ~5', 'witch': '~ ~1 ~5', 'shark': '~ ~2 ~6'}[k]
    fn(f'{pfx}/rise', [f'execute positioned {off} run summon minecraft:{b["host"]} ~ ~ ~ {snbt(host)}',
                       f'execute positioned {off} run function bm:{pfx}/rig'] +
       [f'title @a[distance=..48] times 10 70 20', f'title @a[distance=..48] subtitle {snbt(T(b["rise"][1], "gray", italic=True))}',
        f'title @a[distance=..48] title {snbt(T(b["NAME"], b["COL"], bold=True))}',
        tellraw('@a[distance=..48]', [T(b['rise'][0], b['ruin_col'], italic=True)]),
        'playsound minecraft:entity.wither.spawn hostile @a[distance=..64] ~ ~ ~ 0.7 0.7', 'playsound minecraft:ambient.cave hostile @a[distance=..64] ~ ~ ~ 1 0.5'])
    fn(f'{pfx}/rig', rig + ['scoreboard players add #dbid bm.rng 1',
                            f'scoreboard players operation @e[tag=bm.dbnew,distance=..2] bm.dbid = #dbid bm.rng',
                            f'execute as @e[tag=bm.db_{k},tag=bm.dbnew,distance=..2] at @s run function bm:{pfx}/init',
                            'tag @e[tag=bm.dbnew,distance=..2] remove bm.dbnew'])
    fn(f'{pfx}/init', ['scoreboard players set @s bm.dbs -1', 'scoreboard players set @s bm.dbf 0', 'scoreboard players set @s bm.dba 30',
                       'scoreboard players set @s bm.dbx 60', 'scoreboard players set @s bm.dbph 0', 'scoreboard players set @s bm.dbgone 0',
                       'scoreboard players set @s bm.dbk7 40', 'scoreboard players set @s bm.dbk8 80', 'scoreboard players set @s bm.dbk9 120',
                       'scoreboard players set @s bm.dbk11 160', 'scoreboard players set @s bm.dbk12 200',
                       'scoreboard players operation #id bm.rng = @s bm.dbid',
                       f'execute as @e[type=minecraft:item_display,tag=bm.dbr_{k}] if score @s bm.dbid = #id bm.rng run tag @s add bm.dbsel',
                       f'execute rotated as @s rotated ~ 0 run function bm:{pfx}/place', f'function bm:{pfx}/pose/spawn', 'tag @e[tag=bm.dbsel] remove bm.dbsel'])

    # ---- its mind, every tick
    tick.append(f'execute as @e[tag=bm.db_{k}] at @s run function bm:{pfx}/tick')
    A_ = ATTACKS[k]
    choose = []
    for st, cd, cond, phase2 in [(a['st'], a['cd'], a['cond'], a.get('p2', False)) for a in A_]:
        choose.append(' '.join(x for x in [f'execute unless score @s bm.dbx matches 1.. unless score @s bm.dbk{st} matches 1..',
                                           'if score @s bm.dbph matches 1' if phase2 else '', cond, f'run function bm:{pfx}/go{st}'] if x))
    for a in A_:
        fn(f'{pfx}/go{a["st"]}', [f'scoreboard players set @s bm.dba {a["st"]}', f'scoreboard players set @s bm.dbx {a["dur"]}',
                                  f'scoreboard players set @s bm.dbk{a["st"]} {a["cd"]}', f'execute facing entity {tgt} feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~'] + a.get('start', []))
    beats = []
    for a in A_:
        for x, f_ in a['beats'].items():
            cond = f'matches {x}' if isinstance(x, int) else f'matches {x}'
            beats.append(f'execute if score @s bm.dba matches {a["st"]} if score @s bm.dbx {cond} run function bm:{pfx}/{f_}')
    fn(f'{pfx}/tick', ['tag @s add bm.dbme', 'scoreboard players operation #id bm.rng = @s bm.dbid',
                       f'execute as @e[type=minecraft:item_display,tag=bm.dbr_{k}] if score @s bm.dbid = #id bm.rng run tag @s add bm.dbsel',
                       f'tag @a[tag=bm.dbtgt] remove bm.dbtgt',
                       'tag @p[distance=..36,gamemode=!spectator,gamemode=!creative] add bm.dbtgt',
                       # (its health: below the floor, it falls)
                       'execute store result score #hp bm.rng run data get entity @s Health',
                       f'execute unless score @s bm.dba matches 30..31 if score #hp bm.rng matches ..{FLOOR} run function bm:{pfx}/falling',
                       f'execute unless score @s bm.dba matches 30..31 if score @s bm.dbph matches 0 if score #hp bm.rng matches ..{FLOOR + b["hp"] // 2} run function bm:{pfx}/phase2',
                       'execute if score @s bm.dbx matches 1.. run scoreboard players remove @s bm.dbx 1'] +
       [f'execute if score @s bm.dbk{st} matches 1.. run scoreboard players remove @s bm.dbk{st} 1' for st in (7, 8, 9, 11, 12)] +
       [f'execute if score @s bm.dbph matches 1 if score @s bm.dbk{st} matches 1.. run scoreboard players remove @s bm.dbk{st} 1' for st in (7, 8, 9, 11)] +
       beats +
       ['execute if score @s bm.dba matches 30 if score @s bm.dbx matches 1 run function bm:{pfx}/awake'.replace('{pfx}', pfx),
        'execute if score @s bm.dba matches 31 if score @s bm.dbx matches 1 run function bm:{pfx}/fall'.replace('{pfx}', pfx),
        f'execute if entity {tgt} unless score @s bm.dba matches 30..31 run function bm:{pfx}/mind',
        f'function bm:{pfx}/state',
        'execute if score #st bm.rng = @s bm.dbs run scoreboard players add @s bm.dbf 1',
        'execute unless score #st bm.rng = @s bm.dbs run scoreboard players set @s bm.dbf 0',
        'scoreboard players operation @s bm.dbs = #st bm.rng',
        f'function bm:{pfx}/anim',
        f'execute rotated as @s rotated ~ 0 run function bm:{pfx}/place',
        'tag @e[tag=bm.dbsel] remove bm.dbsel', 'tag @s remove bm.dbme'])
    fn(f'{pfx}/mind', choose + [f'execute unless score @s bm.dbx matches 1.. run function bm:{pfx}/move'])
    fn(f'{pfx}/state', ['execute if score @s bm.dbx matches 1.. run return run scoreboard players operation #st bm.rng = @s bm.dba',
                        f'execute if entity @s[tag=bm.dbmoving] run return run scoreboard players set #st bm.rng 1', 'scoreboard players set #st bm.rng 0'])
    # (and out of its rising: the mind - and its fall - skip a boss still rising, so it never fought and couldn't be felled)
    fn(f'{pfx}/awake', ['data modify entity @s Invulnerable set value 0b', 'scoreboard players set @s bm.dba 0', f'bossbar set bm:db_{k} visible true',
                        'playsound minecraft:entity.ravager.roar hostile @a[distance=..48] ~ ~ ~ 1.2 0.6'])
    # ---- moving: toward its quarry (it keeps to its ruin)
    mv = {'ground': [f'execute facing entity {tgt} feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~', 'tag @s remove bm.dbmoving',
                     f'execute if entity {tgt[:-1]},distance=5..] rotated as @s rotated ~ 0 if block ^ ^ ^1.6 #bm:grap_pass if block ^ ^1 ^1.6 #bm:grap_pass if block ^ ^2 ^1.6 #bm:grap_pass run function bm:{pfx}/step',
                     f'execute if entity {tgt[:-1]},distance=5..] unless entity @s[tag=bm.dbmoving] rotated as @s rotated ~ 0 if block ^ ^1 ^1.6 #bm:grap_pass if block ^ ^2 ^1.6 #bm:grap_pass if block ^ ^3 ^1.6 #bm:grap_pass run function bm:{pfx}/stepup'],
          'float': [f'execute facing entity {tgt} eyes rotated ~ 0 run tp @s ~ ~ ~ ~ ~', 'tag @s remove bm.dbmoving',
                    f'execute if entity {tgt[:-1]},distance=8..] facing entity {tgt} eyes positioned ^ ^ ^0.6 if block ~ ~1 ~ #bm:grap_pass run function bm:{pfx}/step',
                    f'execute if entity {tgt[:-1]},distance=..4] facing entity {tgt} eyes positioned ^ ^ ^-0.6 if block ~ ~1 ~ #bm:grap_pass run function bm:{pfx}/back',
                    f'execute at {tgt} if entity @s[dy=-30] run tp @s ~ ~-0.06 ~'],
          'swim': [f'execute facing entity {tgt} eyes rotated ~ 0 run tp @s ~ ~ ~ ~ ~', 'tag @s remove bm.dbmoving',
                   f'execute if entity {tgt[:-1]},distance=3.5..] facing entity {tgt} eyes positioned ^ ^ ^1.4 if block ~ ~ ~ minecraft:water run function bm:{pfx}/step']}[b['move']]
    fn(f'{pfx}/move', [f'execute unless entity @e[type=minecraft:interaction,tag=bm.dbaltar_{k},distance=..34] if entity @e[type=minecraft:interaction,tag=bm.dbaltar_{k},distance=..128] run return run function bm:{pfx}/home'] + mv)
    sp = b['speed']
    if b['move'] == 'ground':
        fn(f'{pfx}/step', ['tag @s add bm.dbmoving', f'execute rotated as @s rotated ~ 0 run tp @s ^ ^ ^{sp} ~ ~'])
        fn(f'{pfx}/stepup', ['tag @s add bm.dbmoving', f'execute rotated as @s rotated ~ 0 run tp @s ^ ^1 ^{sp} ~ ~'])
    elif b['move'] == 'float':
        fn(f'{pfx}/step', ['tag @s add bm.dbmoving', f'execute facing entity {tgt} eyes run tp @s ^ ^0.02 ^{sp} ~ 0'])
        fn(f'{pfx}/back', ['tag @s add bm.dbmoving', f'execute facing entity {tgt} eyes run tp @s ^ ^0.06 ^-{sp} ~ 0'])
    else:
        fn(f'{pfx}/step', ['tag @s add bm.dbmoving', f'execute facing entity {tgt} eyes run tp @s ^ ^ ^{sp}', f'execute facing entity {tgt} eyes rotated ~ 0 run tp @s ~ ~ ~ ~ ~'])
    fn(f'{pfx}/home', ['tag @s add bm.dbmoving', 'particle minecraft:reverse_portal ~ ~1 ~ 1 1 1 0.05 30',
                       f'tp @s @e[type=minecraft:interaction,tag=bm.dbaltar_{k},sort=nearest,limit=1]', f'execute at @s run tp @s ~ ~{1 if k != "snow" else 0} ~4',
                       'playsound minecraft:entity.enderman.teleport hostile @a[distance=..32] ~ ~ ~ 1 0.5'])
    # ---- half health: phase two
    fn(f'{pfx}/phase2', ['scoreboard players set @s bm.dbph 1', 'scoreboard players set @s bm.dbk12 0', f'bossbar set bm:db_{k} color red',
                         'playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..64] ~ ~ ~ 1 0.6',
                         tellraw('@a[distance=..48]', [T(b['NAME'], b['COL'], bold=True), T(' is enraged!', 'red')])])
    # ---- every second: the bossbar, and if nobody's near for 30 s, it sinks back into its ruin
    second.append(f'execute as @e[tag=bm.db_{k}] at @s run function bm:{pfx}/sec')
    fn(f'{pfx}/sec', ['execute store result score #hp bm.rng run data get entity @s Health', f'scoreboard players remove #hp bm.rng {FLOOR}',
                      'execute if score #hp bm.rng matches ..-1 run scoreboard players set #hp bm.rng 0',
                      f'execute store result bossbar bm:db_{k} value run scoreboard players get #hp bm.rng',
                      f'bossbar set bm:db_{k} players @a[distance=..64]',
                      'execute if entity @a[distance=..64,gamemode=!spectator] run scoreboard players set @s bm.dbgone 0',
                      'execute unless entity @a[distance=..64,gamemode=!spectator] run scoreboard players add @s bm.dbgone 1',
                      f'execute if score @s bm.dbgone matches 30.. run function bm:{pfx}/sink'] + AMBIENT[k])
    fn(f'{pfx}/sink', ['scoreboard players operation #id bm.rng = @s bm.dbid',
                       f'execute as @e[type=minecraft:item_display,tag=bm.dbr_{k}] if score @s bm.dbid = #id bm.rng run kill @s',
                       'kill @e[tag=bm.dbminion,distance=..48]', f'bossbar set bm:db_{k} players', 'tp @s ~ -400 ~', 'kill @s'])
    # ---- the fall
    fn(f'{pfx}/falling', ['data modify entity @s Invulnerable set value 1b', 'scoreboard players set @s bm.dba 31', 'scoreboard players set @s bm.dbx 60',
                          'kill @e[tag=bm.dbminion,distance=..48]', f'bossbar set bm:db_{k} value 0',
                          'playsound minecraft:entity.wither.death hostile @a[distance=..64] ~ ~ ~ 0.6 0.8'])
    fn(f'{pfx}/fall', [f'execute as @a[distance=..64,gamemode=!spectator] at @s run function bm:{pfx}/reward', 'particle minecraft:explosion_emitter ~ ~1 ~ 0 0 0 0 1',
                       DEATH[k], f'function bm:{pfx}/sink'])
    G.wjson(f'bm/loot_table/p197/{k}_spoils.json', {'type': 'minecraft:chest', 'pools': [
        {'rolls': 1, 'entries': [G.loot_entry('dread_token', G.uni(3, 6))]},
        {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:emerald', 'functions': [{'function': 'minecraft:set_count', 'count': {'type': 'minecraft:uniform', 'min': 4, 'max': 10}}]}]},
        {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:diamond', 'functions': [{'function': 'minecraft:set_count', 'count': {'type': 'minecraft:uniform', 'min': 1, 'max': 3}}]}]}]})
    adv = {'snow': ('Hat Trick', 'Defeat the Malevolent Snowbeast at the Frozen Folly'), 'witch': ('Old Acquaintance', 'Defeat the Watchful Witch at the Hexen Hollow'),
           'shark': ('Bigger Teeth', 'Defeat the Chomping Sawshark at the Drowned Gate')}[k]
    G.wjson(f'bm/advancement/story/db_{k}.json', {'parent': 'bm:story/root', 'criteria': {'won': {'trigger': 'minecraft:impossible'}},
                                                  'display': {'icon': {'id': 'minecraft:paper', 'components': {'minecraft:item_model': f'bm:{b["token"]}'}},
                                                              'title': T(adv[0], 'yellow'), 'description': T(adv[1], 'gray'), 'frame': 'challenge'}})
    fn(f'{pfx}/reward', [give(b['token']), f'loot give @s loot bm:p197/{k}_spoils', f'scoreboard players add @s bm.dbwin_{k} 1',
                         f'advancement grant @s only bm:story/db_{k}',
                         tellraw('@s', G.PREFIX + [T(f'{b["NAME"]} has fallen! ', b['COL'], bold=True), T('Its token is yours - carry it, set it down, or let Vesper scrap it.', 'gray')])])
    fn(f'admin/db_{k}', [f'execute rotated ~ 0 positioned ^ ^ ^8 run function bm:{pfx}/rise'])

    # ---- its attacks
    for f_, lines in ATTACK_FNS[k](me, tgt).items():
        fn(f'{pfx}/{f_}', lines)


# ---------------------------------------------------------------------------------------------------- the three bosses' moves
# states: 0 idle, 1 moving, 7/8/9/11/12 attacks, 30 rising, 31 falling
CYC = {
    'snow': {0: (80, [(0, 'idle_a'), (40, 'idle_b')]), 1: (16, [(0, 'walk_0'), (4, 'walk_1'), (8, 'walk_2'), (12, 'walk_3')]),
             7: (None, [(0, 'throw_up'), (8, 'throw')]), 8: (None, [(0, 'slam_up'), (10, 'slam')]), 9: (None, [(0, 'roar'), (24, 'idle_a')]),
             11: (None, [(0, 'roar')]), 12: (None, [(0, 'roar'), (30, 'slam_up'), (40, 'slam')]), 30: (None, [(0, 'spawn'), (20, 'roar'), (50, 'idle_a')]),
             31: (None, [(0, 'hurt'), (16, 'die')])},
    'witch': {0: (80, [(0, 'idle_a'), (40, 'idle_b')]), 1: (16, [(0, 'float_0'), (4, 'float_1'), (8, 'float_2'), (12, 'float_3')]),
              7: (None, [(0, 'cast_up'), (8, 'cast')]), 8: (None, [(0, 'fold'), (8, 'idle_a')]), 9: (None, [(0, 'summon')]),
              11: (None, [(0, 'drain')]), 12: (None, [(0, 'summon'), (20, 'cast')]), 30: (None, [(0, 'spawn'), (20, 'summon'), (50, 'idle_a')]),
              31: (None, [(0, 'hurt'), (16, 'die')])},
    'shark': {0: (16, [(2 * i, f'swim_{i}') for i in range(8)]), 1: (12, [(i * 3 // 2, f'swim_{i}') for i in range(8)]),
              7: (None, [(0, 'chomp_open'), (6, 'chomp')]), 8: (None, [(0, 'saw_l'), (6, 'saw_r'), (12, 'saw_l'), (18, 'saw_r')]),
              9: (None, [(0, 'chomp_open'), (4, 'charge'), (16, 'chomp')]), 11: (None, [(5 * i, ('roll_a', 'roll_b')[i % 2]) for i in range(10)]),
              12: (None, [(0, 'chomp_open'), (20, 'idle_b')]), 30: (None, [(0, 'spawn'), (20, 'chomp_open'), (40, 'idle_a')]),
              31: (None, [(0, 'hurt'), (16, 'die')])},
}
DUR = {'idle_a': 30, 'idle_b': 30, 'walk_0': 4, 'walk_1': 4, 'walk_2': 4, 'walk_3': 4, 'float_0': 4, 'float_1': 4, 'float_2': 4, 'float_3': 4,
       'throw_up': 6, 'throw': 3, 'slam_up': 8, 'slam': 3, 'roar': 8, 'hurt': 6, 'die': 20, 'spawn': 2, 'cast_up': 6, 'cast': 3, 'summon': 10, 'fold': 6,
       'drain': 8, 'chomp_open': 5, 'chomp': 2, 'saw_l': 5, 'saw_r': 5, 'charge': 4, 'roll_a': 5, 'roll_b': 5, **{f'swim_{i}': 3 for i in range(8)}}
T_ = '@a[tag=bm.dbtgt,limit=1]'
ATTACKS = {
    'snow': [dict(st=12, dur=60, cd=600, p2=True, cond='', beats={50: 'blizzard', 40: 'blizzard', 30: 'strays', 20: 'blizzard', 10: 'blizzard'}),
             dict(st=8, dur=24, cd=160, cond=f'if entity {T_[:-1]},distance=..7]', beats={12: 'nova'}),
             dict(st=11, dur=30, cd=220, cond=f'if entity {T_[:-1]},distance=6..26]', beats={14: 'glare'}),
             dict(st=7, dur=18, cd=50, cond=f'if entity {T_[:-1]},distance=..30]', beats={9: 'volley'})],
    'witch': [dict(st=12, dur=40, cd=600, p2=True, cond='', beats={20: 'shades'}),
              dict(st=11, dur=40, cd=260, p2=True, cond=f'if entity {T_[:-1]},distance=..14]', beats={35: 'drain', 30: 'drain', 25: 'drain', 20: 'drain', 15: 'drain', 10: 'drain', 5: 'drain'}),
              dict(st=8, dur=16, cd=120, cond=f'if entity {T_[:-1]},distance=..5]', beats={8: 'blink'}),
              dict(st=9, dur=30, cd=180, cond=f'if entity {T_[:-1]},distance=..24]', beats={26: 'curse'}),
              dict(st=7, dur=14, cd=36, cond=f'if entity {T_[:-1]},distance=..30]', beats={6: 'bolt'})],
    'shark': [dict(st=12, dur=30, cd=600, p2=True, cond='', beats={15: 'guards'}),
              dict(st=11, dur=50, cd=300, cond=f'if entity {T_[:-1]},distance=..14]', beats={**{x: 'pull' for x in range(45, 5, -5)}, 3: 'spin'}),
              dict(st=9, dur=20, cd=140, cond=f'if entity {T_[:-1]},distance=6..22]', beats={**{x: 'dash' for x in range(16, 5, -1)}}),
              dict(st=8, dur=22, cd=80, cond=f'if entity {T_[:-1]},distance=..7]', beats={16: 'rake', 10: 'rake', 4: 'rake'}),
              dict(st=7, dur=10, cd=30, cond=f'if entity {T_[:-1]},distance=..5]', beats={4: 'chomp'})],
}


def _snow(me, tgt):
    shot = lambda dy: f'execute rotated as @s positioned ^-2.6 ^5.4 ^1.4 facing entity {tgt} eyes rotated ~{dy} ~ positioned ^ ^ ^0.5 summon minecraft:marker run function bm:p197/shot/ice'
    return {
        'volley': [shot(0), shot(10), shot(-10),
                   'playsound minecraft:entity.snow_golem.shoot hostile @a[distance=..32] ~ ~ ~ 1.4 0.5', 'playsound minecraft:block.glass.break hostile @a[distance=..32] ~ ~ ~ 0.6 1.6'],
        'nova': ['particle minecraft:snowflake ~ ~0.4 ~ 3.5 0.3 3.5 0.1 200', 'particle minecraft:explosion ~ ~0.5 ~ 2.5 0.2 2.5 0 6',
                 'playsound minecraft:block.glass.break hostile @a[distance=..32] ~ ~ ~ 1.4 0.6', 'playsound minecraft:entity.generic.explode hostile @a[distance=..32] ~ ~ ~ 0.8 0.8',
                 'execute as @a[distance=..7,gamemode=!spectator] run function bm:p197/snow/frozen'],
        'frozen': [f'damage @s 10 minecraft:freeze by {me}', 'effect give @s minecraft:slowness 3 3', 'data modify entity @s TicksFrozen set value 260'],
        'glare': ['playsound minecraft:block.beacon.activate hostile @a[distance=..32] ~ ~ ~ 1.4 1.8', 'scoreboard players set #gb bm.rng 0',
                  f'execute rotated as @s positioned ^ ^{50 * snowbeast_art.RIG_SCALE / 16:.1f} ^0.6 facing entity {tgt} eyes run function bm:p197/snow/beam'],
        'beam': ['particle minecraft:dust{color:[0.6,0.9,1.0],scale:2.0} ~ ~ ~ 0.1 0.1 0.1 0 3', 'particle minecraft:snowflake ~ ~ ~ 0.1 0.1 0.1 0.01 2',
                 'execute as @a[distance=..1.5,tag=!bm.dbhitb] run function bm:p197/snow/beamed', 'scoreboard players add #gb bm.rng 1',
                 'execute unless block ~ ~ ~ #bm:grap_pass run return run tag @a remove bm.dbhitb',
                 'execute if score #gb bm.rng matches 24.. run return run tag @a remove bm.dbhitb', 'execute positioned ^ ^ ^1 run function bm:p197/snow/beam'],
        'beamed': ['tag @s add bm.dbhitb', 'damage @s 9 minecraft:freeze by @e[tag=bm.dbme,limit=1]', 'effect give @s minecraft:slowness 4 2', 'data modify entity @s TicksFrozen set value 200'],
        'blizzard': ['particle minecraft:snowflake ~ ~4 ~ 12 4 12 0.05 300', 'playsound minecraft:item.elytra.flying hostile @a[distance=..32] ~ ~ ~ 0.4 0.4',
                     'execute as @a[distance=..20,gamemode=!spectator] run function bm:p197/snow/chilled'],
        'chilled': [f'damage @s 3 minecraft:freeze by {me}', 'effect give @s minecraft:slowness 3 0', 'data modify entity @s TicksFrozen set value 160'],
        'strays': [f'execute positioned ^4 ^ ^2 run summon minecraft:stray ~ ~ ~ {{Tags:["bm.dbminion","bm.seen"],PersistenceRequired:1b,CustomName:"Snowbound"}}',
                   f'execute positioned ^-4 ^ ^2 run summon minecraft:stray ~ ~ ~ {{Tags:["bm.dbminion","bm.seen"],PersistenceRequired:1b,CustomName:"Snowbound"}}',
                   'particle minecraft:snowflake ~ ~1 ~ 4 1 4 0.1 80'],
    }


def _witch(me, tgt):
    return {
        'bolt': [f'execute rotated as @s positioned ^-1.6 ^2.6 ^1.2 facing entity {tgt} eyes positioned ^ ^ ^0.5 summon minecraft:marker run function bm:p197/shot/hex',
                 'playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..32] ~ ~ ~ 1 1.2', 'particle minecraft:witch ~ ~3 ~ 0.4 0.4 0.4 0.1 10'],
        'blink': ['particle minecraft:large_smoke ~ ~1.5 ~ 0.6 1 0.6 0.02 40', 'playsound minecraft:entity.illusioner.mirror_move hostile @a[distance=..32] ~ ~ ~ 1 0.8',
                  'execute store result score #r bm.rng run random value 1..4',
                  f'execute if score #r bm.rng matches 1 at {tgt} positioned ~9 ~2 ~ if block ~ ~ ~ #bm:grap_pass run tp @s ~ ~ ~',
                  f'execute if score #r bm.rng matches 2 at {tgt} positioned ~-9 ~2 ~ if block ~ ~ ~ #bm:grap_pass run tp @s ~ ~ ~',
                  f'execute if score #r bm.rng matches 3 at {tgt} positioned ~ ~2 ~9 if block ~ ~ ~ #bm:grap_pass run tp @s ~ ~ ~',
                  f'execute if score #r bm.rng matches 4 at {tgt} positioned ~ ~2 ~-9 if block ~ ~ ~ #bm:grap_pass run tp @s ~ ~ ~',
                  'execute at @s run particle minecraft:large_smoke ~ ~1.5 ~ 0.6 1 0.6 0.02 40'],
        'curse': ['playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..32] ~ ~ ~ 1 0.7',
                  'execute as @a[distance=..24,gamemode=!spectator] at @s run summon minecraft:marker ~ ~ ~ {Tags:["bm.dbcurse"]}'],
        'drain': [f'execute at {tgt} run particle minecraft:dust{{color:[0.48,1.0,0.35],scale:1.4}} ~ ~1 ~ 0.3 0.6 0.3 0 10',
                  f'execute as {tgt} run damage @s 3 minecraft:magic by {me}',
                  'execute store result score #hp bm.rng run data get entity @s Health', 'scoreboard players add #hp bm.rng 5',
                  'execute store result entity @s Health float 1 run scoreboard players get #hp bm.rng',
                  'playsound minecraft:entity.vex.charge hostile @a[distance=..24] ~ ~ ~ 0.6 0.6'],
        'shades': [f'execute positioned ^3 ^2 ^ run summon minecraft:vex ~ ~ ~ {{Tags:["bm.dbminion","bm.seen"],PersistenceRequired:1b,CustomName:"Shade",life_ticks:1200}}',
                   f'execute positioned ^-3 ^2 ^ run summon minecraft:vex ~ ~ ~ {{Tags:["bm.dbminion","bm.seen"],PersistenceRequired:1b,CustomName:"Shade",life_ticks:1200}}',
                   f'execute positioned ^ ^3 ^-3 run summon minecraft:vex ~ ~ ~ {{Tags:["bm.dbminion","bm.seen"],PersistenceRequired:1b,CustomName:"Shade",life_ticks:1200}}',
                   'playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..32] ~ ~ ~ 1 0.5', 'particle minecraft:witch ~ ~2 ~ 2 1 2 0.1 60'],
    }


def _shark(me, tgt):
    return {
        'chomp': ['execute rotated as @s rotated ~ 0 positioned ^ ^1 ^4 as @a[distance=..3.5,gamemode=!spectator] at @s run function bm:p197/shark/bitten',
                  'playsound minecraft:entity.evoker_fangs.attack hostile @a[distance=..32] ~ ~ ~ 1.4 0.5', 'playsound minecraft:entity.player.attack.crit hostile @a[distance=..32] ~ ~ ~ 1 0.6'],
        'bitten': [f'damage @s 14 minecraft:mob_attack by {me}', 'effect give @s minecraft:wither 3 0', 'particle minecraft:damage_indicator ~ ~1 ~ 0.3 0.3 0.3 0.1 8'],
        'rake': ['execute rotated as @s rotated ~ 0 positioned ^ ^1 ^5 as @a[distance=..4.5,gamemode=!spectator] run damage @s 9 minecraft:mob_attack by @e[tag=bm.dbme,limit=1]',
                 'execute rotated as @s rotated ~ 0 positioned ^ ^1 ^5 run particle minecraft:sweep_attack ~ ~ ~ 2 0.5 2 0 4',
                 'playsound minecraft:entity.player.attack.sweep hostile @a[distance=..32] ~ ~ ~ 1.4 0.5'],
        'dash': [f'execute facing entity {tgt} eyes positioned ^ ^ ^1.4 if block ~ ~ ~ minecraft:water run tp @s ^ ^ ^1.4',
                 'particle minecraft:bubble ~ ~1 ~ 1 0.6 1 0.1 20',
                 'execute as @a[distance=..3,gamemode=!spectator,tag=!bm.dbhitb] at @s run function bm:p197/shark/rammed',
                 'execute if score @s bm.dbx matches 6 run tag @a remove bm.dbhitb'],
        'rammed': ['tag @s add bm.dbhitb', 'damage @s 16 minecraft:mob_attack by @e[tag=bm.dbme,limit=1]', 'effect give @s minecraft:slowness 2 1',
                   'playsound minecraft:entity.player.attack.knockback hostile @a[distance=..24] ~ ~ ~ 1.2 0.6'],
        'pull': ['particle minecraft:bubble_column_up ~ ~1 ~ 6 2 6 0.1 60', 'playsound minecraft:block.bubble_column.whirlpool_inside hostile @a[distance=..32] ~ ~ ~ 1 0.6',
                 'execute as @a[distance=2..14,gamemode=!spectator] at @s facing entity @e[tag=bm.dbme,limit=1] feet if block ^ ^ ^0.7 #bm:swim_pass run tp @s ^ ^ ^0.7',
                 'effect give @a[distance=..14] minecraft:mining_fatigue 3 1'],
        'spin': ['execute as @a[distance=..5,gamemode=!spectator] run damage @s 8 minecraft:mob_attack by @e[tag=bm.dbme,limit=1]',
                 'particle minecraft:bubble_pop ~ ~1 ~ 3 1 3 0.2 80'],
        'guards': ['execute positioned ^4 ^1 ^ run summon minecraft:guardian ~ ~ ~ {Tags:["bm.dbminion","bm.seen"],PersistenceRequired:1b}',
                   'execute positioned ^-4 ^1 ^ run summon minecraft:guardian ~ ~ ~ {Tags:["bm.dbminion","bm.seen"],PersistenceRequired:1b}',
                   'playsound minecraft:entity.elder_guardian.curse hostile @a[distance=..48] ~ ~ ~ 1 0.6'],
    }


ATTACK_FNS = {'snow': _snow, 'witch': _witch, 'shark': _shark}
AMBIENT = {
    'snow': ['particle minecraft:snowflake ~ ~5 ~ 2 2 2 0.02 12'],
    'witch': ['particle minecraft:witch ~ ~2.5 ~ 0.6 0.8 0.6 0.02 4', 'particle minecraft:dust{color:[0.48,1.0,0.35],scale:1.0} ~ ~3 ~ 0.4 0.3 0.4 0 2'],
    'shark': ['particle minecraft:bubble ~ ~1 ~ 2 1 2 0.02 10'],
}
DEATH = {
    'snow': 'execute if entity @e[tag=bm.pipet,distance=..32] run tellraw @a[distance=..48] ' + snbt([T('Pistachio: ', '#7ae890', bold=True), T('"MY HAT! There you are! Oh, you poor thing - come here, come here. Never again. Never, ever again."', '#d8ffe0')]),
    'witch': 'execute if entity @e[tag=bm.cecilpet,distance=..32] run tellraw @a[distance=..48] ' + snbt([T('Cecil: ', '#a07aff', bold=True), T('"...I told you the old books would eat you. I\'m sorry. I\'m so sorry I didn\'t stop you."', '#e0d8ff')]),
    'shark': 'tellraw @a[distance=..48] ' + snbt([T('As it rolls over and sinks, something glints in its belly - ', '#8ae8d8', italic=True), T('a scrap of a black storm-cloak, and a broken scythe-tip. No body.', 'gray', italic=True)]),
}


def _shots(G, tick):
    """(called from generate) the projectiles both ranged bosses throw: ice shards and hex bolts, and the witch's curse rings.
    A shot is a marker summoned facing its mark (execute summon keeps the rotation); it flies 0.8 a tick for 2 seconds."""
    fn = G.fn
    for kind in ('ice', 'hex'):
        fn(f'p197/shot/{kind}', [f'tag @s add bm.dbshot', f'tag @s add bm.dbshot_{kind}', 'tp @s ~ ~ ~ ~ ~', 'scoreboard players set @s bm.dbt 0'])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.dbshot] at @s run function bm:p197/shot/fly')
    fn('p197/shot/fly', ['scoreboard players add @s bm.dbt 1', 'execute if score @s bm.dbt matches 40.. run return run kill @s',
                         'execute positioned ^ ^ ^0.8 unless block ~ ~ ~ #bm:grap_pass run return run function bm:p197/shot/pop',
                         'tp @s ^ ^ ^0.8',
                         'execute at @s if entity @s[tag=bm.dbshot_ice] run particle minecraft:snowflake ~ ~ ~ 0.08 0.08 0.08 0 3',
                         'execute at @s if entity @s[tag=bm.dbshot_ice] run particle minecraft:item{item:"minecraft:ice"} ~ ~ ~ 0.05 0.05 0.05 0 1',
                         'execute at @s if entity @s[tag=bm.dbshot_hex] run particle minecraft:dust{color:[0.48,1.0,0.35],scale:1.4} ~ ~ ~ 0.08 0.08 0.08 0 3',
                         'execute at @s if entity @s[tag=bm.dbshot_hex] run particle minecraft:witch ~ ~ ~ 0.05 0.05 0.05 0 1',
                         # (to the feet and to the middle of a player: either counts)
                         'execute at @s if entity @a[distance=..1.1,gamemode=!spectator] run return run function bm:p197/shot/hit',
                         'execute at @s positioned ~ ~-1 ~ if entity @a[distance=..1.1,gamemode=!spectator] run return run function bm:p197/shot/hit'])
    fn('p197/shot/hit', ['execute if entity @s[tag=bm.dbshot_ice] as @a[distance=..2.2,gamemode=!spectator,limit=1,sort=nearest] at @s run function bm:p197/shot/hurt_ice',
                         'execute if entity @s[tag=bm.dbshot_hex] as @a[distance=..2.2,gamemode=!spectator,limit=1,sort=nearest] at @s run function bm:p197/shot/hurt_hex',
                         'function bm:p197/shot/pop'])
    fn('p197/shot/hurt_ice', ['damage @s 6 minecraft:freeze by @e[tag=bm.db_snow,limit=1,sort=nearest]', 'effect give @s minecraft:slowness 3 1',
                              'data modify entity @s TicksFrozen set value 180'])
    fn('p197/shot/hurt_hex', ['damage @s 7 minecraft:magic by @e[tag=bm.db_witch,limit=1,sort=nearest]', 'effect give @s minecraft:wither 4 0'])
    fn('p197/shot/pop', ['execute if entity @s[tag=bm.dbshot_ice] run particle minecraft:item{item:"minecraft:ice"} ~ ~ ~ 0.2 0.2 0.2 0.1 10',
                         'execute if entity @s[tag=bm.dbshot_ice] run playsound minecraft:block.glass.break hostile @a[distance=..16] ~ ~ ~ 0.6 1.8',
                         'execute if entity @s[tag=bm.dbshot_hex] run particle minecraft:witch ~ ~ ~ 0.3 0.3 0.3 0.1 14',
                         'kill @s'])
    # the curse: a green ring under each player, 1.5 s to step out, then it bursts
    tick.append('execute as @e[type=minecraft:marker,tag=bm.dbcurse] at @s run function bm:p197/curse/tick')
    fn('p197/curse/tick', ['scoreboard players add @s bm.dbt 1'] +
       [f'execute if score @s bm.dbt matches ..29 positioned ^{2.5 * math.sin(a * math.pi / 4):.2f} ^0.1 ^{2.5 * math.cos(a * math.pi / 4):.2f} run particle minecraft:dust{{color:[0.48,1.0,0.35],scale:1.2}} ~ ~ ~ 0 0 0 0 1'
        for a in range(8)] +
       ['execute if score @s bm.dbt matches 30.. run function bm:p197/curse/burst'])
    fn('p197/curse/burst', ['particle minecraft:witch ~ ~0.6 ~ 1.4 0.6 1.4 0.2 60', 'particle minecraft:explosion ~ ~0.5 ~ 0.6 0.2 0.6 0 2',
                            'playsound minecraft:entity.evoker_fangs.attack hostile @a[distance=..24] ~ ~ ~ 1 0.6',
                            'execute as @a[distance=..2.5,gamemode=!spectator] run damage @s 12 minecraft:magic by @e[tag=bm.db_witch,limit=1,sort=nearest]',
                            'kill @s'])


def generate_late(G):
    pass

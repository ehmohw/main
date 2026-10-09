"""Phase 2.45: Pearlman, the Traveling Salespenguin, and his elemental gems.

- PEARLMAN: a dapper penguin in a top hat and a blue bow tie, a globe-gem on his belly and a briefcase in his flipper.
  Like the wandering trader (2.46: rarer - one roll an in-game day, 10% rising to 30%, about one visit in 4 days) he
  waddles up to a player out under the open sky in the Overworld, sets up shop for 8 minutes, then tips his hat and leaves. He sells three of his nine gems
  each visit (a different three each time), 3 Medallions apiece. He chatters, and drops hints.
- THE NINE GEMS (fire, water, poison, earth, electric, rock, air, grass, ice): polished trophies.
  Use: the gem glints toward the nearest biome of its element (direction + distance, a sparkling trail).
  Sneak + use: set it on display (a small spinning gem; punch it to take it back). It hums when its kin are near.
- THE SECRET (not spelled out anywhere in game): set all nine on display within 4 blocks of each other and they rise,
  circle and fuse into the ETHEREAL GEM. Use it to set it down: a prismatic, singing shrine. Everyone within 30 blocks
  of it is ETHEREAL - light as air (low gravity, high leaps, no fall damage), +3 attack, +4 armour, Regeneration, faster,
  with shimmering wings of light - and every melee blow unleashes one of the nine elements on the target.
  Sneak + punch the shrine to take it back."""
import math
from items import item, T, TOTEM
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D

PEARL = '#5ac8ff'
ETH = '#e8b8ff'
# key: (name, colour, dust rgb, finder text, overworld/nether biomes, gem lore)
GEMS = {
    'fire': ('Fire Gem', '#ff7a2a', (1.0, 0.45, 0.12), 'the badlands and deserts (or the Nether)',
             ['desert', 'badlands', 'eroded_badlands', 'wooded_badlands', 'nether_wastes', 'basalt_deltas', 'crimson_forest'],
             'A flame caught in glass. It is warm to hold.'),
    'water': ('Water Gem', '#3a9cff', (0.2, 0.55, 1.0), 'the sea and the rivers',
              ['ocean', 'deep_ocean', 'warm_ocean', 'lukewarm_ocean', 'deep_lukewarm_ocean', 'cold_ocean', 'deep_cold_ocean', 'river', 'beach'],
              'A drop of the deep sea, polished smooth.'),
    'poison': ('Poison Gem', '#a64ce8', (0.65, 0.3, 0.9), 'the swamps',
               ['swamp', 'mangrove_swamp'], 'Violet and venom-green. Do not lick it.'),
    'earth': ('Earth Gem', '#2e9ad0', (0.2, 0.62, 0.45), 'the deep old woods',
              ['dark_forest', 'pale_garden', 'old_growth_pine_taiga', 'old_growth_spruce_taiga', 'mushroom_fields'],
              'A whole little world - seas and green lands - inside.'),
    'electric': ('Electric Gem', '#ffe23a', (1.0, 0.9, 0.2), 'the stormy savannas',
                 ['savanna', 'savanna_plateau', 'windswept_savanna'], 'It crackles if you rub it on wool.'),
    'rock': ('Rock Gem', '#b09070', (0.65, 0.55, 0.45), 'stony peaks and shores',
             ['stony_peaks', 'stony_shore', 'windswept_gravelly_hills', 'dripstone_caves'], 'Heavy, honest, and very, very shiny.'),
    'air': ('Air Gem', '#d8f2ff', (0.88, 0.96, 1.0), 'the windswept heights',
            ['windswept_hills', 'windswept_forest', 'jagged_peaks'], 'Almost weightless. Mist swirls inside.'),
    'grass': ('Grass Gem', '#52d24a', (0.35, 0.85, 0.3), 'green plains and meadows',
              ['plains', 'sunflower_plains', 'meadow', 'flower_forest', 'cherry_grove', 'forest', 'birch_forest'], 'Smells faintly of a summer field.'),
    'ice': ('Ice Gem', '#a8ecff', (0.65, 0.92, 1.0), 'the frozen north',
            ['snowy_plains', 'ice_spikes', 'frozen_peaks', 'snowy_slopes', 'grove', 'snowy_taiga', 'frozen_ocean', 'deep_frozen_ocean',
             'frozen_river', 'snowy_beach'], 'Never melts. Never even sweats.'),
}
KEYS = list(GEMS)
GEM_PRICE = ('medallion', 3)
STAY_SECONDS, DAY = 480, 1200          # he stays 8 min; one chance of a visit per in-game day (20 min of play)
CHANCE0, CHANCE_STEP, CHANCE_MAX = 10, 10, 30     # like the wandering trader: 10%, then 20%, then 30% a day until he comes

for _k, (_n, _c, _rgb, _where, _b, _flav) in GEMS.items():
    item(f'gem_{_k}', TOTEM, _n, _c,
         [_flav, ('Use: it glints toward ' + _where + '.', 'blue'), ('Sneak + use: set it on display (punch to take it back).', 'blue'),
          ('Odd... it hums when its kin are near.', 'dark_gray'), ('From Pearlman, the Traveling Salespenguin.', 'dark_gray')],
         model=f'bm:gem_{_k}', stack=16, cat='fun', glint=False, comps=hold('none'))
    HOLD[f'gem_{_k}'] = f'bm:p60/gem/use_{_k}'
item('ethereal_gem', TOTEM, 'Ethereal Gem', ETH,
     ['Nine made one. It is warm, and it sings.', ('Carried: a shimmer of the nine follows you.', 'light_purple'),
      ('Use: set it down. All within 30 blocks', 'light_purple'), ('of it become Ethereal.', 'light_purple'),
      ('Sneak + punch it to take it back.', 'gray')],
     model='bm:ethereal_gem', stack=1, cat='relic', glint=True, tier=3, comps=hold('none'))
HOLD['ethereal_gem'] = 'bm:p60/eth/use'


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    from phase46 import COMPANIONS
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    tick, second, fast = [], [], []
    objs = ['bm.gmcd', 'bm.pmt', 'bm.gft', 'bm.esht', 'bm.etcd', 'bm.etdl', 'bm.etvp']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + [
        f'execute unless score #pmcd bm.bm matches -2147483648.. run scoreboard players set #pmcd bm.bm {DAY}',
        f'execute unless score #pmch bm.bm matches -2147483648.. run scoreboard players set #pmch bm.bm {CHANCE0}',
        f'execute if score #pmcd bm.bm matches {DAY + 1}.. run scoreboard players set #pmcd bm.bm {DAY}',
        'scoreboard players set #-1 bm.rng -1', 'scoreboard players set #5 bm.rng 5', 'scoreboard players set #12 bm.rng 12', 'scoreboard players set #9 bm.rng 9']
    G.OBJECTIVES += objs
    holds = '*[minecraft:custom_data~{bm:"%s"}]'
    mob = 'type=!#bm:p44_nonmob,type=!minecraft:player,tag=!bm.npc,' + COMPANIONS
    tick.append('scoreboard players remove @a[scores={bm.gmcd=1..}] bm.gmcd 1')
    tick.append('scoreboard players remove @a[scores={bm.etcd=1..}] bm.etcd 1')
    dust = lambda rgb, s=0.9: f'minecraft:dust{{color:[{rgb[0]},{rgb[1]},{rgb[2]}],scale:{s}}}'
    def take_held(iid):            # one off the stack in whichever hand holds it
        return [f'execute if items entity @s weapon.mainhand {holds % iid} run return run item modify entity @s weapon.mainhand {{function:"minecraft:set_count",count:-1,add:true}}',
                f'item modify entity @s weapon.offhand {{function:"minecraft:set_count",count:-1,add:true}}']

    # ================================================================== the gems find their biomes
    for k, (name, col, rgb, where, biomes, _f) in GEMS.items():
        wjson(f'bm/tags/worldgen/biome/p60/{k}.json', {'values': [{'id': f'minecraft:{b}', 'required': False} for b in biomes]})
        fn(f'p60/gem/use_{k}', ['execute if predicate bm:p20/sneaking run return run function bm:p60/deco/try_' + k,
                                'execute if score @s bm.gmcd matches 1.. run return 0', 'scoreboard players set @s bm.gmcd 60',
                                f'playsound minecraft:block.amethyst_block.chime player @a[distance=..12] ~ ~ ~ 1 1.4',
                                f'execute anchored eyes positioned ^ ^ ^0.6 run particle {dust(rgb)} ~ ~ ~ 0.15 0.15 0.15 0 10',
                                f'function bm:p60/gem/find_{k}'])
        tag = f'#bm:p60/{k}'
        fn(f'p60/gem/find_{k}', [
            f'execute store success score #ok bm.rng store result score #d0 bm.rng run locate biome {tag}',
            'execute if score #ok bm.rng matches 0 run return run ' + title('@s', 'actionbar', T(f'The {name} stays dark - none of its kind within reach.', 'gray')),
            'execute if score #d0 bm.rng matches ..12 run return run ' + title('@s', 'actionbar', T(f'The {name} glows warm and bright - you are standing in it!', col)),
            f'execute positioned ~48 ~ ~ store result score #de bm.rng run locate biome {tag}',
            f'execute positioned ~ ~ ~48 store result score #ds bm.rng run locate biome {tag}',
            'scoreboard players operation #dx bm.rng = #d0 bm.rng', 'scoreboard players operation #dx bm.rng -= #de bm.rng',
            'scoreboard players operation #dz bm.rng = #d0 bm.rng', 'scoreboard players operation #dz bm.rng -= #ds bm.rng',
            'function bm:p60/gem/dir',
            f'function bm:p60/gem/say_{k}',
            f'function bm:p60/gem/trail_{k}'])
        msg = lambda d: [T(f'The {name} glints ', 'gray'), T(d, col, bold=True), T(' - about ', 'gray'),
                         {'score': {'name': '#d0', 'objective': 'bm.rng'}, 'color': 'white'}, T(' blocks.', 'gray')]
        fn(f'p60/gem/say_{k}', [f'execute if score #dir bm.rng matches {i} run ' + title('@s', 'actionbar', msg(d))
                                for i, d in enumerate(('north', 'north-east', 'east', 'south-east', 'south', 'south-west', 'west', 'north-west', 'somewhere near'))])
        fn(f'p60/gem/trail_{k}', ['execute store result score #px bm.rng run data get entity @s Pos[0]', 'execute store result score #pz bm.rng run data get entity @s Pos[2]',
                                  'scoreboard players operation #px bm.rng += #dx bm.rng', 'scoreboard players operation #pz bm.rng += #dz bm.rng',
                                  'summon minecraft:marker ~ ~1.3 ~ {Tags:["bm.gmk"]}',
                                  'execute store result entity @e[type=minecraft:marker,tag=bm.gmk,limit=1] Pos[0] double 1 run scoreboard players get #px bm.rng',
                                  'execute store result entity @e[type=minecraft:marker,tag=bm.gmk,limit=1] Pos[2] double 1 run scoreboard players get #pz bm.rng',
                                  'execute unless score #dir bm.rng matches 8 positioned ~ ~1.3 ~ facing entity @e[type=minecraft:marker,tag=bm.gmk,limit=1] feet run function bm:p60/gem/line_' + k,
                                  'kill @e[type=minecraft:marker,tag=bm.gmk]'])
        fn(f'p60/gem/line_{k}', [f'particle {dust(rgb, 1.1)} ^ ^ ^{1 + i * 0.6:.1f} 0.02 0.02 0.02 0 2' for i in range(12)] +
           ['particle minecraft:end_rod ^ ^ ^8 0.1 0.1 0.1 0.02 6'])
    # the compass point from the distance gradient (#dx east+, #dz south+): 0 N, 1 NE ... 7 NW, 8 unclear
    fn('p60/gem/dir', ['scoreboard players set #dir bm.rng 8',
                       'execute if score #dx bm.rng matches 0 if score #dz bm.rng matches 0 run return 0',
                       'scoreboard players operation #ax bm.rng = #dx bm.rng', 'execute if score #ax bm.rng matches ..-1 run scoreboard players operation #ax bm.rng *= #-1 bm.rng',
                       'scoreboard players operation #az bm.rng = #dz bm.rng', 'execute if score #az bm.rng matches ..-1 run scoreboard players operation #az bm.rng *= #-1 bm.rng',
                       'scoreboard players operation #a5 bm.rng = #ax bm.rng', 'scoreboard players operation #a5 bm.rng *= #5 bm.rng',
                       'scoreboard players operation #a12 bm.rng = #ax bm.rng', 'scoreboard players operation #a12 bm.rng *= #12 bm.rng',
                       'scoreboard players operation #z5 bm.rng = #az bm.rng', 'scoreboard players operation #z5 bm.rng *= #5 bm.rng',
                       'scoreboard players operation #z12 bm.rng = #az bm.rng', 'scoreboard players operation #z12 bm.rng *= #12 bm.rng',
                       # mostly east-west
                       'execute if score #a5 bm.rng > #z12 bm.rng if score #dx bm.rng matches 1.. run return run scoreboard players set #dir bm.rng 2',
                       'execute if score #a5 bm.rng > #z12 bm.rng run return run scoreboard players set #dir bm.rng 6',
                       # mostly north-south
                       'execute if score #z5 bm.rng > #a12 bm.rng if score #dz bm.rng matches 1.. run return run scoreboard players set #dir bm.rng 4',
                       'execute if score #z5 bm.rng > #a12 bm.rng run return run scoreboard players set #dir bm.rng 0',
                       # diagonals
                       'execute if score #dx bm.rng matches 1.. if score #dz bm.rng matches ..-1 run return run scoreboard players set #dir bm.rng 1',
                       'execute if score #dx bm.rng matches 1.. run return run scoreboard players set #dir bm.rng 3',
                       'execute if score #dz bm.rng matches 1.. run return run scoreboard players set #dir bm.rng 5',
                       'scoreboard players set #dir bm.rng 7'])

    # ================================================================== gems on display (and the ethereal shrine): placing
    fn('p60/ray', ['execute unless block ~ ~ ~ #minecraft:replaceable run return run function bm:p60/hit',
                   'scoreboard players remove #ray bm.rng 1',
                   'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p60/ray'])
    fn('p60/hit', ['execute align xyz positioned ~0.5 ~1 ~0.5 unless block ~ ~ ~ #minecraft:replaceable run return 0',
                   'execute align xyz positioned ~0.5 ~1 ~0.5 if entity @e[type=minecraft:interaction,tag=bm.gplaced,distance=..0.6] run return 0',
                   'execute align xyz positioned ~0.5 ~1 ~0.5 run function bm:p60/place'])
    fn('p60/place', [f'execute if score #gk bm.rng matches {i} run return run function bm:p60/spawn/{k}' for i, k in enumerate(KEYS + ['ethereal'])])
    def placer(k, iid):
        return [f'scoreboard players set #gk bm.rng {(KEYS + ["ethereal"]).index(k)}', 'scoreboard players set #placed bm.rng 0', 'scoreboard players set #ray bm.rng 25',
                'tag @s add bm.placer', 'execute anchored eyes positioned ^ ^ ^ run function bm:p60/ray', 'tag @s remove bm.placer',
                'execute if score #placed bm.rng matches 0 run return run ' + say('Look at the top of a block within 5 blocks to set it down.'),
                f'execute unless entity @s[gamemode=creative] run function bm:p60/take/{iid}']
    def disp(model, tags, sc, ty, bright=15, spin=True):
        return {'Tags': tags, 'teleport_duration': Int(5), 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': model}},
                'item_display': 'fixed', 'brightness': {'block': Int(bright), 'sky': Int(15)}, 'interpolation_duration': Int(20),
                'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                   'translation': [F(0), F(ty), F(0)], 'scale': [F(sc)] * 3}}
    for k, (name, col, rgb, *_r) in GEMS.items():
        fn(f'p60/deco/try_{k}', placer(k, f'gem_{k}'))
        fn(f'p60/take/gem_{k}', take_held(f'gem_{k}'))
        box = {'Tags': ['bm.gplaced', 'bm.gdeco_hit', f'bm.gh_{k}', 'bm.new'], 'width': F(0.5), 'height': F(0.7), 'response': B(1)}
        fn(f'p60/spawn/{k}', [f'summon minecraft:item_display ~ ~ ~ {snbt(disp(f"bm:gem_{k}", ["bm.gdeco", f"bm.gd_{k}", "bm.new"], 0.55, 0.32))}',
                              f'summon minecraft:interaction ~ ~ ~ {snbt(box)}',
                              'execute rotated as @a[tag=bm.placer,limit=1] run tp @e[tag=bm.new,distance=..0.5] ~ ~ ~ ~180 0',
                              'tag @e[tag=bm.new,distance=..0.5] remove bm.new', 'scoreboard players set #placed bm.rng 1',
                              'playsound minecraft:block.amethyst_block.place block @a[distance=..16] ~ ~ ~ 1 1.2',
                              f'particle {dust(rgb)} ~ ~0.4 ~ 0.2 0.2 0.2 0 12', 'function bm:p60/deco/kin'])
        fn(f'p60/deco/pick_{k}', [f'loot spawn ~ ~0.3 ~ loot bm:items/gem_{k}', f'kill @e[type=minecraft:item_display,tag=bm.gd_{k},distance=..0.3]',
                                  'particle minecraft:poof ~ ~0.4 ~ 0.1 0.1 0.1 0.02 4', 'playsound minecraft:block.amethyst_block.break block @a[distance=..16] ~ ~ ~ 1 1.2',
                                  'kill @s'])
        fast.append(f'execute as @e[type=minecraft:interaction,tag=bm.gh_{k}] if data entity @s attack at @s run function bm:p60/deco/pick_{k}')
        second.append(f'execute as @e[type=minecraft:item_display,tag=bm.gd_{k}] at @s if entity @a[distance=..20] run particle {dust(rgb, 0.6)} ~ ~0.35 ~ 0.12 0.12 0.12 0 1')
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.gdeco_hit] if data entity @s interaction at @s run function bm:p60/deco/hum')
    fast.append('execute as @e[type=minecraft:item_display,tag=bm.gdeco,tag=!bm.gfuse] at @s if entity @a[distance=..24] run tp @s ~ ~ ~ ~12 0')
    fn('p60/deco/hum', ['data remove entity @s interaction', 'function bm:p60/deco/kin'])
    # (at a gem on display) count its kin within 4 blocks: they hum together, louder the more there are - all nine: they fuse
    fn('p60/deco/kin', ['scoreboard players set #kin bm.rng 0'] +
       [f'execute if entity @e[type=minecraft:item_display,tag=bm.gd_{k},tag=!bm.gfuse,distance=..4] run scoreboard players add #kin bm.rng 1' for k in KEYS] +
       ['execute if score #kin bm.rng matches 9 run return run function bm:p60/fuse/start',
        'execute if score #kin bm.rng matches 2..4 run playsound minecraft:block.amethyst_block.resonate block @a[distance=..12] ~ ~ ~ 0.6 1.2',
        'execute if score #kin bm.rng matches 5..8 run playsound minecraft:block.amethyst_block.resonate block @a[distance=..16] ~ ~ ~ 1 1.6',
        'execute if score #kin bm.rng matches 5..8 run particle minecraft:end_rod ~ ~0.5 ~ 0.6 0.3 0.6 0.01 6',
        'execute if score #kin bm.rng matches 1 run playsound minecraft:block.amethyst_block.chime block @a[distance=..12] ~ ~ ~ 0.8 1.0'])

    # ================================================================== the fusion: the nine rise, circle in, and become one
    fn('p60/fuse/start', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.gfm"]}', 'scoreboard players set @e[type=minecraft:marker,tag=bm.gfm,distance=..0.5] bm.gft 0'] +
       [f'tag @e[type=minecraft:item_display,tag=bm.gd_{k},tag=!bm.gfuse,distance=..4,sort=nearest,limit=1] add bm.gfuse' for k in KEYS] +
       ['execute as @e[type=minecraft:item_display,tag=bm.gfuse,distance=..4] run data merge entity @s {start_interpolation:0,interpolation_duration:30,transformation:{translation:[0f,1.6f,0f],scale:[0.7f,0.7f,0.7f]}}',
        'execute as @e[type=minecraft:item_display,tag=bm.gfuse,distance=..4] at @s run kill @e[type=minecraft:interaction,tag=bm.gdeco_hit,distance=..0.3]',
        'playsound minecraft:block.beacon.power_select block @a[distance=..32] ~ ~ ~ 1 1.4',
        'playsound minecraft:block.amethyst_block.resonate block @a[distance=..32] ~ ~ ~ 1 0.6'])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.gfm] at @s run function bm:p60/fuse/tick')
    fn('p60/fuse/tick', ['scoreboard players add @s bm.gft 1',
                         'execute if score @s bm.gft matches 30 as @e[type=minecraft:item_display,tag=bm.gfuse,distance=..5] run data modify entity @s teleport_duration set value 25',
                         'execute if score @s bm.gft matches 31 as @e[type=minecraft:item_display,tag=bm.gfuse,distance=..5] run tp @s ~ ~ ~',
                         'execute if score @s bm.gft matches 31 run playsound minecraft:block.portal.trigger block @a[distance=..32] ~ ~ ~ 0.5 2',
                         'execute if score @s bm.gft matches 1..55 run function bm:p60/fuse/swirl',
                         'execute if score @s bm.gft matches 58 run function bm:p60/fuse/done'])
    fn('p60/fuse/swirl', ['execute store result score #a bm.rng run scoreboard players get @s bm.gft', 'scoreboard players operation #a bm.rng *= #12 bm.rng',
                          'execute store result entity @s Rotation[0] float 1 run scoreboard players get #a bm.rng'] +
       [f'execute rotated as @s rotated ~{i * 40} 0 positioned ^ ^1.9 ^1.2 run particle {dust(GEMS[k][2], 1.2)} ~ ~ ~ 0 0 0 0 1 force @a[distance=..48]'
        for i, k in enumerate(KEYS)] + ['particle minecraft:end_rod ~ ~1.9 ~ 0.4 0.4 0.4 0.03 2'])
    fn('p60/fuse/done', ['kill @e[type=minecraft:item_display,tag=bm.gfuse,distance=..5]',
                         'loot spawn ~ ~1.9 ~ loot bm:items/ethereal_gem',
                         'data merge entity @e[type=minecraft:item,distance=..3,sort=nearest,limit=1] {Glowing:1b,PickupDelay:20s,Motion:[0.0d,0.15d,0.0d]}',
                         'particle minecraft:flash{color:[1.0,0.9,1.0,1.0]} ~ ~1.9 ~ 0 0 0 0 1 force @a[distance=..64]',
                         'particle minecraft:end_rod ~ ~1.9 ~ 0.2 0.2 0.2 0.25 60 force @a[distance=..64]',
                         'particle minecraft:totem_of_undying ~ ~1.9 ~ 0.3 0.3 0.3 0.6 60 force @a[distance=..64]',
                         'playsound minecraft:block.end_portal.spawn block @a[distance=..48] ~ ~ ~ 0.6 1.6',
                         'playsound minecraft:block.amethyst_block.break block @a[distance=..48] ~ ~ ~ 1 0.5',
                         tellraw('@a[distance=..24]', [T('The nine gems sing, circle... and become one.', ETH, italic=True)]),
                         'advancement grant @a[distance=..12] only bm:story/ethereal_gem', 'kill @s'])

    # ================================================================== the Ethereal Gem's shrine
    fn('p60/eth/use', ['execute if entity @e[type=minecraft:item_display,tag=bm.eshr,distance=..60] run return run ' +
                       say('Another Ethereal Gem already sings nearby.', ETH)] + placer('ethereal', 'ethereal_gem'))
    fn('p60/take/ethereal_gem', take_held('ethereal_gem'))
    sbox = {'Tags': ['bm.gplaced', 'bm.eshr_hit', 'bm.new'], 'width': F(0.7), 'height': F(1.3), 'response': B(1)}
    fn('p60/spawn/ethereal', [f'summon minecraft:item_display ~ ~ ~ {snbt(disp("bm:ethereal_gem", ["bm.eshr", "bm.new"], 0.95, 0.75))}',
                              f'summon minecraft:interaction ~ ~ ~ {snbt(sbox)}', 'tag @e[tag=bm.new,distance=..0.5] remove bm.new', 'scoreboard players set #placed bm.rng 1',
                              'playsound minecraft:block.beacon.activate block @a[distance=..32] ~ ~ ~ 1 1.6',
                              'playsound minecraft:block.amethyst_block.resonate block @a[distance=..32] ~ ~ ~ 1 1.2',
                              'particle minecraft:end_rod ~ ~0.8 ~ 0.2 0.4 0.2 0.15 40', tellraw('@a[distance=..30]', [T('The air turns to light.', ETH, italic=True)])])
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.eshr_hit] if data entity @s attack at @s run function bm:p60/eth/punch')
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.eshr_hit] if data entity @s interaction at @s run function bm:p60/eth/touch')
    fn('p60/eth/punch', ['scoreboard players set #sn bm.rng 0', 'execute on attacker if predicate bm:p20/sneaking run scoreboard players set #sn bm.rng 1',
                         'data remove entity @s attack', 'execute if score #sn bm.rng matches 0 run return 0',
                         'loot spawn ~ ~0.6 ~ loot bm:items/ethereal_gem', 'kill @e[type=minecraft:item_display,tag=bm.eshr,distance=..0.3]',
                         'playsound minecraft:block.beacon.deactivate block @a[distance=..32] ~ ~ ~ 1 1.6', 'particle minecraft:end_rod ~ ~0.8 ~ 0.2 0.3 0.2 0.1 20', 'kill @s'])
    fn('p60/eth/touch', ['data remove entity @s interaction', 'playsound minecraft:block.amethyst_block.chime block @a[distance=..16] ~ ~ ~ 1 2',
                         'particle minecraft:end_rod ~ ~0.9 ~ 0.3 0.3 0.3 0.05 8'])
    # every tick near a player: it turns; nine motes of the elements circle it; light rises; a ring marks the 30-block edge
    tick.append('execute as @e[type=minecraft:item_display,tag=bm.eshr] at @s if entity @a[distance=..48] run function bm:p60/eth/shrine')
    fn('p60/eth/shrine', ['scoreboard players add @s bm.esht 1', 'tp @s ~ ~ ~ ~4 0',
                          'scoreboard players operation #t bm.rng = @s bm.esht', 'scoreboard players operation #t bm.rng %= #2 bm.rng',
                          'execute if score #t bm.rng matches 0 run function bm:p60/eth/motes',
                          'scoreboard players operation #t bm.rng = @s bm.esht', 'scoreboard players operation #t bm.rng %= #40 bm.rng',
                          'execute if score #t bm.rng matches 0 run function bm:p60/eth/pulse',
                          'execute if score #t bm.rng matches 20 run particle minecraft:end_rod ~ ~0.7 ~ 0.25 0.5 0.25 0.02 3',
                          'execute if score @s bm.esht matches 240.. run function bm:p60/eth/ring'])
    fn('p60/eth/motes', [f'execute rotated ~{i * 40} 0 positioned ^ ^{0.55 + 0.25 * math.sin(i * 0.7):.2f} ^1.15 run particle {dust(GEMS[k][2], 0.8)} ~ ~ ~ 0 0 0 0 1 force @a[distance=..48]'
                         for i, k in enumerate(KEYS)] + ['particle minecraft:glow ~ ~0.75 ~ 0.3 0.3 0.3 0 1'])
    fn('p60/eth/pulse', ['playsound minecraft:block.amethyst_block.resonate ambient @a[distance=..30] ~ ~ ~ 0.5 1.8',
                         'execute store result score #n bm.rng run random value 0..3',
                         'execute if score #n bm.rng matches 0 run playsound minecraft:block.note_block.chime ambient @a[distance=..30] ~ ~ ~ 0.5 1.19',
                         'execute if score #n bm.rng matches 1 run playsound minecraft:block.note_block.chime ambient @a[distance=..30] ~ ~ ~ 0.5 1.5',
                         'execute if score #n bm.rng matches 2 run playsound minecraft:block.note_block.chime ambient @a[distance=..30] ~ ~ ~ 0.5 1.78',
                         'execute if score #n bm.rng matches 3 run playsound minecraft:block.beacon.ambient ambient @a[distance=..30] ~ ~ ~ 0.6 1.8',
                         'particle minecraft:end_rod ~ ~0.8 ~ 0 1.2 0 0.04 6',
                         'particle minecraft:dust{color:[0.95,0.85,1.0],scale:2.0} ~ ~0.1 ~ 0.6 0 0.6 0 8'])
    fn('p60/eth/ring', ['scoreboard players set @s bm.esht 0'] +
       [f'particle minecraft:end_rod ^{30 * math.sin(math.radians(a)):.2f} ^0.3 ^{30 * math.cos(math.radians(a)):.2f} 0 0.4 0 0.01 1 force @a[distance=..48]' for a in range(0, 360, 6)])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #2 bm.rng 2', 'scoreboard players set #40 bm.rng 40']

    # ================================================================== Ethereal: everyone within 30 blocks of a shrine
    MODS = [('gravity', -0.045, 'add_value'), ('safe_fall_distance', 40, 'add_value'), ('jump_strength', 0.25, 'add_value'),
            ('attack_damage', 3, 'add_value'), ('armor', 4, 'add_value'), ('movement_speed', 0.2, 'add_multiplied_base')]
    second += ['execute as @e[type=minecraft:item_display,tag=bm.eshr] at @s as @a[distance=..30,gamemode=!spectator] at @s run function bm:p60/eth/keep',
               'execute as @a[tag=bm.eth] at @s unless entity @e[type=minecraft:item_display,tag=bm.eshr,distance=..30] run function bm:p60/eth/off',
               'execute as @a[tag=bm.eth,gamemode=spectator] run function bm:p60/eth/off']
    fn('p60/eth/keep', ['execute unless entity @s[tag=bm.eth] run function bm:p60/eth/on',
                        'effect give @s minecraft:regeneration 3 0 true', 'effect give @s minecraft:resistance 3 0 true'])
    fn('p60/eth/on', ['tag @s add bm.eth'] + [f'attribute @s minecraft:{a} modifier add bm:ethereal_{a} {v} {op}' for a, v, op in MODS] +
       [say('You feel light as air. Ethereal.', ETH), 'playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 1.6',
        'particle minecraft:end_rod ~ ~1 ~ 0.3 0.6 0.3 0.05 20'])
    fn('p60/eth/off', ['tag @s remove bm.eth'] + [f'attribute @s minecraft:{a} modifier remove bm:ethereal_{a}' for a, _v, _o in MODS] +
       [say('The lightness fades.', 'gray')])
    G.FUNCS['load'][-1:-1] = ['tag @a remove bm.eth']        # (a reload clears the status; the next second puts it back if you're still near)
    # (2.47) carrying the Ethereal Gem anywhere in your inventory: a shimmer of the nine drifts about you
    gem = holds % 'ethereal_gem'
    fast += ['scoreboard players add #eo bm.rng 1', 'execute if score #eo bm.rng matches 9.. run scoreboard players set #eo bm.rng 0',
             f'execute as @a[gamemode=!spectator] if items entity @s container.* {gem} at @s run function bm:p60/eth/carry',
             f'execute as @a[gamemode=!spectator] unless items entity @s container.* {gem} if items entity @s weapon.offhand {gem} at @s run function bm:p60/eth/carry']
    fn('p60/eth/carry', [f'execute if score #eo bm.rng matches {i} run particle {dust(GEMS[k][2], 0.7)} ~ ~1.1 ~ 0.45 0.55 0.45 0 2' for i, k in enumerate(KEYS)] +
       [f'execute if score #eo bm.rng matches {(i + 4) % 9} run particle {dust(GEMS[k][2], 0.5)} ~ ~0.6 ~ 0.4 0.3 0.4 0 1' for i, k in enumerate(KEYS)] +
       ['particle minecraft:end_rod ~ ~1.2 ~ 0.35 0.5 0.35 0.005 1', 'execute if score #eo bm.rng matches 0 run particle minecraft:glow ~ ~1 ~ 0.3 0.4 0.3 0 1'])
    # wings of light, every other tick
    tick.append('execute if score #t2 bm.rng matches 0 as @a[tag=bm.eth,gamemode=!spectator] at @s rotated ~ 0 run function bm:p60/eth/wings')
    G.FUNCS['tick'].insert(0, 'scoreboard players add #t2 bm.rng 1')
    G.FUNCS['tick'].insert(1, 'execute if score #t2 bm.rng matches 2.. run scoreboard players set #t2 bm.rng 0')
    WING = [(0.32, 1.42, -0.3), (0.62, 1.62, -0.42), (0.95, 1.78, -0.5), (1.2, 1.7, -0.55), (0.95, 1.38, -0.5), (0.7, 1.12, -0.42), (0.45, 1.0, -0.34)]
    fn('p60/eth/wings', [f'particle minecraft:dust{{color:[0.92,0.82,1.0],scale:0.55}} ^{s * x} ^{y} ^{z} 0 0 0 0 1' for x, y, z in WING for s in (1, -1)] +
       ['particle minecraft:end_rod ^0.9 ^1.5 ^-0.5 0.05 0.1 0.05 0 0', 'particle minecraft:end_rod ^-0.9 ^1.5 ^-0.5 0.05 0.1 0.05 0 0'])
    # every melee blow unleashes one of the nine elements (a beat apart: its own damage would fire this again)
    wjson('bm/advancement/p60/eth_hit.json', {'criteria': {'hit': {'trigger': 'minecraft:player_hurt_entity', 'conditions': {'player': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["bm.eth"]}'}}]}}},
        'rewards': {'function': 'bm:p60/eth/hit'}})
    fn('p60/eth/hit', ['advancement revoke @s only bm:p60/eth_hit', 'execute if score @s bm.etcd matches 1.. run return 0',
                       'scoreboard players set @s bm.etcd 12', 'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                       'scoreboard players operation #me bm.pid = @s bm.pid',
                       f'execute at @s as @e[{mob},distance=..8,nbt={{HurtTime:10s}},sort=nearest,limit=1] at @s run function bm:p60/eth/mark',
                       'scoreboard players set @s bm.etdl 11'])
    fn('p60/eth/mark', ['tag @s add bm.etv', 'scoreboard players operation @s bm.etvp = #me bm.pid', 'particle minecraft:end_rod ~ ~1 ~ 0.2 0.3 0.2 0.05 6'])
    # (half a second on, once the blow's hurt-immunity has passed - the element lands in full)
    tick.append('execute as @a[scores={bm.etdl=1..}] at @s run function bm:p60/eth/delay')
    fn('p60/eth/delay', ['scoreboard players remove @s bm.etdl 1', 'execute if score @s bm.etdl matches 1.. run return 0',
                         'tag @s add bm.ethme', 'scoreboard players operation #me bm.pid = @s bm.pid',
                         'execute store result score #el bm.rng run random value 0..8',
                         'execute as @e[tag=bm.etv,distance=..12] if score @s bm.etvp = #me bm.pid at @s run function bm:p60/eth/strike',
                         'execute as @e[tag=bm.etv] if score @s bm.etvp = #me bm.pid run tag @s remove bm.etv', 'tag @s remove bm.ethme'])
    me = '@a[tag=bm.ethme,limit=1]'
    EL = {
        'fire': [f'damage @s 5 minecraft:in_fire by {me}', 'data merge entity @s {Fire:160s}', 'particle minecraft:flame ~ ~1 ~ 0.3 0.5 0.3 0.05 20',
                 'playsound minecraft:item.firecharge.use player @a[distance=..16] ~ ~ ~ 1 1'],
        'water': [f'damage @s 6 minecraft:magic by {me}', 'effect give @s minecraft:slowness 3 1', 'particle minecraft:splash ~ ~1 ~ 0.4 0.6 0.4 0.2 40',
                  'playsound minecraft:entity.generic.splash player @a[distance=..16] ~ ~ ~ 1 1.2'],
        'poison': [f'damage @s 4 minecraft:magic by {me}', 'execute unless entity @s[type=#minecraft:undead] run effect give @s minecraft:poison 6 1',
                   'execute if entity @s[type=#minecraft:undead] run effect give @s minecraft:wither 6 1', 'particle minecraft:witch ~ ~1 ~ 0.3 0.5 0.3 0.05 20',
                   'playsound minecraft:entity.witch.throw player @a[distance=..16] ~ ~ ~ 1 0.8'],
        'earth': [f'damage @s 8 minecraft:magic by {me}', 'effect give @s minecraft:slowness 3 3', 'particle minecraft:block{block_state:"minecraft:dirt"} ~ ~0.5 ~ 0.4 0.3 0.4 0 30',
                  'playsound minecraft:block.rooted_dirt.break player @a[distance=..16] ~ ~ ~ 1 0.6'],
        'electric': [f'damage @s 6 minecraft:lightning_bolt by {me}', 'particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.4 30',
                     f'execute as @e[type=#bm:hostile,tag=!bm.npc,distance=0.5..5,sort=nearest,limit=2] run damage @s 4 minecraft:lightning_bolt by {me}',
                     'playsound minecraft:entity.lightning_bolt.impact player @a[distance=..16] ~ ~ ~ 0.6 1.6'],
        'rock': [f'damage @s 10 minecraft:magic by {me}', 'particle minecraft:block{block_state:"minecraft:stone"} ~ ~1 ~ 0.4 0.4 0.4 0 30',
                 'playsound minecraft:block.stone.break player @a[distance=..16] ~ ~ ~ 1 0.5'],
        'air': [f'damage @s 4 minecraft:magic by {me}', 'effect give @s minecraft:levitation 1 6', 'particle minecraft:cloud ~ ~0.5 ~ 0.3 0.2 0.3 0.1 20',
                'playsound minecraft:entity.breeze.wind_burst player @a[distance=..16] ~ ~ ~ 1 1.2'],
        'grass': [f'damage @s 5 minecraft:magic by {me}', f'effect give {me} minecraft:instant_health 1 0', 'particle minecraft:happy_villager ~ ~1 ~ 0.4 0.5 0.4 0 16',
                  'playsound minecraft:block.azalea_leaves.break player @a[distance=..16] ~ ~ ~ 1 1'],
        'ice': [f'damage @s 6 minecraft:freeze by {me}', 'effect give @s minecraft:slowness 4 3', 'data merge entity @s {TicksFrozen:300}',
                'particle minecraft:snowflake ~ ~1 ~ 0.3 0.5 0.3 0.05 30', 'playsound minecraft:block.glass.break player @a[distance=..16] ~ ~ ~ 1 1.6'],
    }
    fn('p60/eth/strike', [f'execute if score #el bm.rng matches {i} run return run function bm:p60/eth/el/{k}' for i, k in enumerate(KEYS)])
    for i, k in enumerate(KEYS):
        fn(f'p60/eth/el/{k}', EL[k] + [f'particle {dust(GEMS[k][2], 1.4)} ~ ~1.2 ~ 0.3 0.4 0.3 0 12'])

    # ================================================================== Pearlman
    offers = [G.offer(GEM_PRICE, (f'gem_{k}', 1)) for k in KEYS]
    for o in offers: o['maxUses'] = Int(3)
    G.FUNCS['load'][-1:-1] = [f'data modify storage bm:p60 offers set value {snbt(offers)}']
    pm = {'NoAI': B(1), 'Invulnerable': B(1), 'PersistenceRequired': B(1), 'Silent': B(1),
          'Tags': ['bm.npc', 'bm.pearl', 'bm.seen', 'bm.pnew'], 'CustomName': T('Pearlman, the Traveling Salespenguin', PEARL, bold=True), 'CustomNameVisible': B(0),
          'VillagerData': {'type': 'minecraft:snow', 'profession': 'minecraft:librarian', 'level': Int(5)}, 'Xp': Int(250), 'VillagerDataFinalized': B(1),
          'Offers': {'Recipes': []}, 'attributes': [{'id': 'minecraft:scale', 'base': D(0.8)}],
          'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}]}
    PS = 0.76
    pmd = disp('bm:pearlman', ['bm.pearld', 'bm.pnew'], PS, round(PS / 2, 3), 13)
    pmd['brightness'] = {'block': Int(12), 'sky': Int(13)}
    fn('p60/pm/spawn', [f'summon minecraft:villager ~ ~ ~ {snbt(pm)}', f'summon minecraft:item_display ~ ~ ~ {snbt(pmd)}',
                        f'scoreboard players set @e[type=minecraft:villager,tag=bm.pnew,distance=..1] bm.pmt {STAY_SECONDS}',
                        # three of the nine, a different three each visit
                        'execute store result score #s bm.rng run random value 0..8', 'execute store result score #k bm.rng run random value 1..4',
                        'scoreboard players operation #i bm.rng = #s bm.rng', 'function bm:p60/pm/stock1',
                        'scoreboard players operation #i bm.rng += #k bm.rng', 'function bm:p60/pm/stock1',
                        'scoreboard players operation #i bm.rng += #k bm.rng', 'function bm:p60/pm/stock1',
                        'execute as @e[type=minecraft:item_display,tag=bm.pnew,distance=..1] at @s facing entity @p feet run tp @s ~ ~ ~ ~ 0',
                        'tag @e[tag=bm.pnew,distance=..1] remove bm.pnew',
                        'particle minecraft:snowflake ~ ~1 ~ 0.4 0.6 0.4 0.02 30', 'particle minecraft:poof ~ ~0.6 ~ 0.3 0.4 0.3 0.02 10',
                        'playsound minecraft:block.note_block.bell neutral @a[distance=..24] ~ ~ ~ 1 1.6',
                        tellraw('@a[distance=..24]', [T('Pearlman: ', PEARL, bold=True),
                                                      T('"Pearlman, Traveling Salespenguin, at your service! Gems, my friend - the finest polish this side of the iceberg."', 'white')])])
    fn('p60/pm/stock1', ['scoreboard players operation #i bm.rng %= #9 bm.rng', 'execute store result storage bm:p60 pick.i int 1 run scoreboard players get #i bm.rng',
                         'function bm:p60/pm/stock with storage bm:p60 pick'])
    fn('p60/pm/stock', ['$data modify entity @e[type=minecraft:villager,tag=bm.pnew,limit=1,sort=nearest] Offers.Recipes append from storage bm:p60 offers[$(i)]'])
    # visits, like the wandering trader's: once an in-game day there's a roll (10%, then 20%, then 30%... reset when he comes);
    # he picks a random player out under the open sky in the Overworld
    second += ['scoreboard players remove #pmcd bm.bm 1', 'execute if score #pmcd bm.bm matches ..0 run function bm:p60/pm/day',
               'execute as @e[type=minecraft:villager,tag=bm.pearl] at @s run function bm:p60/pm/sec']
    fn('p60/pm/day', [f'scoreboard players set #pmcd bm.bm {DAY}', 'execute if entity @e[type=minecraft:villager,tag=bm.pearl] run return 0',
                      'execute store result score #r bm.rng run random value 1..100', 'scoreboard players set #placed bm.rng 0',
                      'execute if score #r bm.rng <= #pmch bm.bm as @a[gamemode=survival,sort=random,limit=1] at @s if dimension minecraft:overworld positioned ~ ~1.6 ~ if predicate bm:sees_sky positioned ~ ~-1.6 ~ run function bm:p60/pm/arrive',
                      f'execute if score #placed bm.rng matches 1 run return run scoreboard players set #pmch bm.bm {CHANCE0}',
                      f'scoreboard players add #pmch bm.bm {CHANCE_STEP}',
                      f'execute if score #pmch bm.bm matches {CHANCE_MAX + 1}.. run scoreboard players set #pmch bm.bm {CHANCE_MAX}'])
    fn('p60/pm/arrive', ['execute if entity @e[type=minecraft:villager,tag=bm.pearl] run return 0',
                         'summon minecraft:marker ~ ~ ~ {Tags:["bm.psp"]}',
                         'execute as @e[type=minecraft:marker,tag=bm.psp,distance=..1,limit=1] store result entity @s Rotation[0] float 1 run random value 0..359',
                         'scoreboard players set #placed bm.rng 0',
                         'execute as @e[type=minecraft:marker,tag=bm.psp,distance=..1,limit=1] rotated as @s positioned ^ ^ ^6 positioned over motion_blocking_no_leaves run function bm:p60/pm/land',
                         'kill @e[type=minecraft:marker,tag=bm.psp]'])
    fn('p60/pm/land', ['execute unless block ~ ~ ~ #minecraft:replaceable run return 0', 'execute if block ~ ~ ~ minecraft:water run return 0',
                       'execute if block ~ ~-1 ~ #minecraft:replaceable run return 0', 'execute if block ~ ~-1 ~ minecraft:water run return 0',
                       'execute align xz positioned ~0.5 ~ ~0.5 run function bm:p60/pm/spawn', 'scoreboard players set #placed bm.rng 1'])
    LINES = ['"Splendid choice! Flipper-buffed, every one."', '"Each of them hums a little tune, you know. Not that anybody listens."',
             '"Nine of them there are. Nine! A funny number, nine."', '"Hold one up and let it find its home. They always know the way."',
             '"Laid side by side, they say, the nine... ah, but I talk too much. Bad for business!"', '"Pearlman never forgets a customer. Or a tip."',
             '"Pleasure doing business! Mind the briefcase."', '"I had all nine once. Long ago. Long story. Penguins do not like to talk about it."']
    fn('p60/pm/sec', ['scoreboard players remove @s bm.pmt 1', 'execute if score @s bm.pmt matches ..0 run return run function bm:p60/pm/leave',
                      'execute unless entity @a[distance=..64] run return run function bm:p60/pm/leave',
                      # (2.49: only his model turns to face you - teleporting the villager itself, even in place, ends any open trade)
                      'execute if entity @p[distance=..10] facing entity @p[distance=..10] feet as @e[type=minecraft:item_display,tag=bm.pearld,distance=..0.6,limit=1] run rotate @s ~ 0',
                      'scoreboard players operation #t bm.rng = @s bm.pmt', 'scoreboard players operation #t bm.rng %= #2 bm.rng',
                      'execute if score #t bm.rng matches 0 as @e[type=minecraft:item_display,tag=bm.pearld,distance=..0.6,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:20,transformation:{left_rotation:[0f,0f,0.04f,0.9992f]}}',
                      'execute if score #t bm.rng matches 1 as @e[type=minecraft:item_display,tag=bm.pearld,distance=..0.6,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:20,transformation:{left_rotation:[0f,0f,-0.04f,0.9992f]}}',
                      'execute store result score #r bm.rng run random value 0..30',
                      'execute if score #r bm.rng matches 0 run playsound minecraft:entity.parrot.ambient neutral @a[distance=..16] ~ ~ ~ 0.6 0.6',
                      'execute if score #r bm.rng matches 1 run particle minecraft:snowflake ~ ~1.2 ~ 0.3 0.4 0.3 0.01 4',
                      'execute if score @s bm.pmt matches 60 run ' + tellraw('@a[distance=..24]', [T('Pearlman: ', PEARL, bold=True), T('"Last call! Pearlman waddles on in a minute, friends."', 'white')])])
    fn('p60/pm/leave', [tellraw('@a[distance=..24]', [T('Pearlman ', PEARL, bold=True), T('tips his top hat and waddles off. "Toodle-oo!"', 'gray', italic=True)]),
                        'particle minecraft:snowflake ~ ~1 ~ 0.4 0.6 0.4 0.02 30', 'particle minecraft:poof ~ ~0.6 ~ 0.3 0.4 0.3 0.02 10',
                        'playsound minecraft:block.note_block.bell neutral @a[distance=..24] ~ ~ ~ 1 1.2',
                        'kill @e[type=minecraft:item_display,tag=bm.pearld,distance=..0.6]', 'tp @s ~ -400 ~', 'kill @s'])
    wjson('bm/advancement/p60/pm_trade.json', {'criteria': {'t': {'trigger': 'minecraft:villager_trade', 'conditions': {'villager': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["bm.pearl"]}'}}]}}}, 'rewards': {'function': 'bm:p60/pm/traded'}})
    fn('p60/pm/traded', ['advancement revoke @s only bm:p60/pm_trade', 'advancement grant @s only bm:story/pearlman',
                         'execute store result score #r bm.rng run random value 0..%d' % (len(LINES) - 1)] +
       [f'execute if score #r bm.rng matches {i} run ' + tellraw('@s', [T('Pearlman: ', PEARL, bold=True), T(ln, 'white')]) for i, ln in enumerate(LINES)] +
       ['execute at @e[type=minecraft:villager,tag=bm.pearl,distance=..8,limit=1] run particle minecraft:happy_villager ~ ~1.2 ~ 0.3 0.3 0.3 0 6',
        'playsound minecraft:block.note_block.chime neutral @s ~ ~ ~ 0.8 1.6'])

    # ================================================================== achievements, admin
    def adv(key, ico, ttl, desc, frame='task', hidden=False):
        wjson(f'bm/advancement/story/{key}.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
              'display': {'icon': {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': f'bm:{ico}'}},
                          'title': T(ttl, 'gold' if frame == 'challenge' else 'yellow'), 'description': T(desc, 'gray'),
                          'frame': frame, 'show_toast': True, 'announce_to_chat': True, 'hidden': hidden}})
    adv('pearlman', 'gem_earth', 'A Dapper Deal', 'Buy a gem from Pearlman, the Traveling Salespenguin')
    adv('ethereal_gem', 'ethereal_gem', 'Nine Made One', 'Join the nine elemental gems into one', 'challenge', hidden=True)
    fn('admin/pearlman', ['execute rotated ~ 0 positioned ^ ^ ^3 align xz positioned ~0.5 ~ ~0.5 run function bm:p60/pm/spawn'])
    fn('admin/elemental_gems', [give(f'gem_{k}') for k in KEYS])
    fn('admin/ethereal_gem', [give('ethereal_gem')])
    G.FUNCS['admin/uninstall'][0:0] = ['execute as @a[tag=bm.eth] run function bm:p60/eth/off']

    G.FUNCS['tick'] += tick
    s = G.FUNCS['loop/second']
    s[-1:-1] = second
    f = G.FUNCS['loop/fast']
    f[-1:-1] = fast


# ===================================================================== resource pack: Pearlman, the nine gems, the Ethereal Gem
GEM_DISP = {'gui': {'rotation': [25, 30, 0], 'translation': [0, 0, 0], 'scale': [1.25, 1.25, 1.25]},
            'ground': {'rotation': [0, 0, 0], 'translation': [0, 2, 0], 'scale': [0.6, 0.6, 0.6]},
            'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]},
            'thirdperson_righthand': {'rotation': [0, 0, 0], 'translation': [0, 2.5, 1.5], 'scale': [0.6, 0.6, 0.6]},
            'thirdperson_lefthand': {'rotation': [0, 0, 0], 'translation': [0, 2.5, 1.5], 'scale': [0.6, 0.6, 0.6]},
            'firstperson_righthand': {'rotation': [0, -20, 0], 'translation': [1, 3, 0], 'scale': [0.7, 0.7, 0.7]},
            'firstperson_lefthand': {'rotation': [0, -20, 0], 'translation': [1, 3, 0], 'scale': [0.7, 0.7, 0.7]},
            'head': {'rotation': [0, 0, 0], 'translation': [0, 14, 0], 'scale': [1, 1, 1]}}
FIXED = {'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]},
         'gui': {'rotation': [20, 200, 0], 'translation': [0, -6, 0], 'scale': [0.42, 0.42, 0.42]}}


def textures():
    import random
    from PIL import Image
    from gen_rp import hexc
    rnd = random.Random(60)
    h3 = lambda v: tuple(hexc(v)[:3])
    def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
    def noise(base, var):
        im = Image.new('RGBA', (16, 16)); b = hexc(base)
        for y in range(16):
            for x in range(16):
                d = rnd.randint(-var, var); im.putpixel((x, y), tuple(max(0, min(255, c + d)) for c in b[:3]) + (255,))
        return im
    def facet(dark, mid, light):
        """a polished cut: a diagonal light-to-dark sweep, facet seams, a few white glints"""
        im = Image.new('RGBA', (16, 16)); d_, m_, l_ = h3(dark), h3(mid), h3(light)
        for y in range(16):
            for x in range(16):
                t = (x + (15 - y)) / 30
                c = lerp(d_, m_, t * 2) if t < 0.5 else lerp(m_, l_, (t - 0.5) * 2)
                if (x - y) % 6 == 0 or (x + y) % 8 == 0: c = lerp(c, d_, 0.35)
                im.putpixel((x, y), c + (255,))
        for gx, gy in ((11, 3), (12, 4), (3, 10), (12, 3)):
            im.putpixel((gx, gy), (255, 255, 255, 255))
        return im
    PAL = {'fire': ('#9a1404', '#ff6a1a', '#ffe070'), 'water': ('#0c3c9a', '#2f8cff', '#bfe6ff'), 'poison': ('#3a0f5a', '#9a3ce0', '#8cff6a'),
           'earth': ('#0c3a6a', '#2e8ad0', '#7ad0ff'), 'electric': ('#9a6a00', '#ffd21a', '#fffbd0'), 'rock': ('#4a3a2c', '#9a7e62', '#e8d8c0'),
           'air': ('#7aa8c0', '#d0eeff', '#ffffff'), 'grass': ('#14601a', '#3ec43a', '#d8ff9a'), 'ice': ('#3a8ab0', '#9ae6ff', '#ffffff')}
    T_ = {}
    for k, (d_, m_, l_) in PAL.items():
        T_[f'gm_{k}'] = facet(d_, m_, l_)
        T_[f'gm_{k}_lt'] = facet(m_, l_, '#ffffff')
    # earth: blue seas with green lands, as on Pearlman's own
    for y in range(16):
        for x in range(16):
            if (math.sin(x * 0.7) + math.cos(y * 0.6 + x * 0.2)) > 0.7 or (6 <= x <= 9 and 9 <= y <= 13):
                g = h3('#3cb04a' if (x + y) % 3 else '#62d26a')
                T_['gm_earth'].putpixel((x, y), g + (255,)); T_['gm_earth_lt'].putpixel((x, y), h3('#8ae08a') + (255,))
    # poison: venom-green flecks in the violet
    for _ in range(18):
        T_['gm_poison'].putpixel((rnd.randrange(16), rnd.randrange(16)), h3('#6aff4a') + (255,))
    # the ethereal gem: a pastel prism of all nine
    eth = Image.new('RGBA', (16, 16)); eth_lt = Image.new('RGBA', (16, 16))
    hues = ['#ffb0c8', '#ffd0a0', '#fff0a0', '#c0ffc0', '#a8f0ff', '#b8c8ff', '#e0b8ff']
    for y in range(16):
        for x in range(16):
            t = ((x * 0.8 + y * 1.3 + 3 * math.sin(x * 0.5)) / 6) % len(hues)
            a, b = h3(hues[int(t)]), h3(hues[(int(t) + 1) % len(hues)])
            c = lerp(a, b, t - int(t))
            if (x - y) % 5 == 0: c = lerp(c, (255, 255, 255), 0.5)
            eth.putpixel((x, y), c + (255,)); eth_lt.putpixel((x, y), lerp(c, (255, 255, 255), 0.55) + (255,))
    for gx, gy in ((3, 3), (12, 5), (7, 11), (13, 13)):
        eth.putpixel((gx, gy), (255, 255, 255, 255))
    T_['gm_eth'], T_['gm_eth_lt'] = eth, eth_lt
    # Pearlman
    T_.update({'pm_black': noise('#23272e', 5), 'pm_white': noise('#d4e2e4', 5), 'pm_orange': noise('#de8a52', 8), 'pm_yellow': noise('#d6c062', 8),
               'pm_blue': noise('#2aa6da', 8), 'pm_dblue': noise('#1a6c9e', 6), 'pm_gold': noise('#d8b040', 12), 'pm_eye': noise('#0e1c2c', 3),
               'pm_teeth': noise('#f4f4ee', 3), 'pm_case': noise('#1a1a1e', 4)})
    for y in range(16):
        for x in range(16):
            if y < 3 and (x + y) % 4 == 0: T_['pm_black'].putpixel((x, y), h3('#3c434e') + (255,))   # a sheen
            if x % 4 == 3: T_['pm_teeth'].putpixel((x, y), h3('#9a9a96') + (255,))                   # the grin
    return T_


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    cube = R.cube
    def c(fr, to, t, rot=None):
        e = cube(fr, to, t)
        if rot: e['rotation'] = {'origin': list(rot[2]), 'axis': rot[0], 'angle': rot[1]}
        return e
    def post(R2):
        def model(name, tex, els, disp):
            t = {k: (v if ':' in v else f'bm:block/{v}') for k, v in tex.items()}; t['particle'] = list(t.values())[0]
            R2.wj(f'assets/bm/models/item/{name}.json', {'textures': t, 'elements': els, 'display': disp})
            R2.wj(f'assets/bm/items/{name}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/{name}'}})
        def y45(fr, to, t):
            return c(fr, to, t, ('y', 45, ((fr[0] + to[0]) / 2, (fr[1] + to[1]) / 2, (fr[2] + to[2]) / 2)))
        # a brilliant cut, centred on (8, 8, 8): pavilion, girdle, crown, table - shaped a little per element
        SHAPE = {'fire': (1.0, 1.35, 'flame'), 'water': (1.0, 1.15, 'drop'), 'poison': (0.95, 1.0, 'spikes'), 'earth': (1.1, 1.0, 'orb'),
                 'electric': (0.9, 1.3, 'bolt'), 'rock': (1.15, 0.95, 'chunk'), 'air': (1.0, 1.0, 'swirl'), 'grass': (0.95, 1.1, 'leaf'), 'ice': (0.9, 1.3, 'spikes')}
        for k, (w, h, acc) in SHAPE.items():
            m, l = 'm', 'l'
            def bx(r, y0, y1, t, rot=True):
                fr, to = (8 - r * w, 8 + (y0 - 8) * h, 8 - r * w), (8 + r * w, 8 + (y1 - 8) * h, 8 + r * w)
                return y45(fr, to, t) if rot else c(fr, to, t)
            els = [bx(0.6, 3.6, 4.6, m), bx(1.4, 4.4, 6.0, m), bx(2.3, 5.8, 7.2, m), bx(3.0, 7.0, 8.4, m, False), bx(2.9, 7.0, 8.4, m),
                   bx(2.4, 8.4, 9.6, l, False), bx(1.7, 9.4, 10.4, l)]
            top = 8 + (10.4 - 8) * h
            if acc == 'flame':
                els += [c((7.2, top - 0.2, 7.2), (8.8, top + 2.4, 8.8), l, ('y', 45, (8, top, 8))), c((7.6, top + 2.2, 7.6), (8.4, top + 3.8, 8.4), l)]
            elif acc == 'drop':
                els += [c((7.0, top - 0.2, 7.0), (9.0, top + 1.6, 9.0), m, ('y', 45, (8, top, 8))), c((7.5, top + 1.4, 7.5), (8.5, top + 3.0, 8.5), l)]
            elif acc == 'spikes':
                for dx, dz, a in ((-2, 0, 'z'), (2, 0, 'z'), (0, -2, 'x'), (0, 2, 'x')):
                    ang = 22.5 if dx < 0 or dz > 0 else -22.5
                    els.append(c((8 + dx - 0.5, 8, 8 + dz - 0.5), (8 + dx + 0.5, top + 1.5, 8 + dz + 0.5), l, (a, ang, (8 + dx, 8, 8 + dz))))
                els.append(c((7.4, top - 0.5, 7.4), (8.6, top + 2.6, 8.6), l))
            elif acc == 'orb':
                els += [c((5.6, 5.2, 5.6), (10.4, 10.6, 10.4), m), c((6.2, 4.6, 6.2), (9.8, 11.2, 9.8), l, ('y', 45, (8, 8, 8)))]
            elif acc == 'bolt':
                els += [c((7.4, top - 0.4, 7.4), (8.6, top + 2.2, 8.6), l, ('z', 22.5, (8, top, 8))), c((7.4, top + 1.6, 7.4), (8.4, top + 3.6, 8.4), l, ('z', -22.5, (8, top + 2, 8)))]
            elif acc == 'chunk':
                els += [c((5.4, 7.4, 5.8), (8.6, 10.2, 9.6), m, ('z', 22.5, (7, 8.8, 7.7))), c((8.2, 6.6, 6.6), (10.8, 9.6, 10.4), l, ('x', 22.5, (9.5, 8, 8.5)))]
            elif acc == 'swirl':
                els += [c((4.4, 8.4, 7.6), (11.6, 8.9, 8.4), l, ('y', 22.5, (8, 8.6, 8))), c((7.6, 9.4, 4.4), (8.4, 9.9, 11.6), l, ('y', 22.5, (8, 9.6, 8)))]
            elif acc == 'leaf':
                els += [c((7.6, 4.0, 4.4), (8.4, 12.4, 11.6), l, ('x', 22.5, (8, 8, 8))), c((7.8, 3.0, 7.8), (8.2, 13.4, 8.2), m)]
            model(f'gem_{k}', {'m': f'gm_{k}', 'l': f'gm_{k}_lt'}, els, GEM_DISP)
        # the Ethereal Gem: a tall prismatic star-crystal ringed by four lesser crystals
        e = [y45((5.6, 2.0, 5.6), (10.4, 4.0, 10.4), 'm'), y45((4.6, 4.0, 4.6), (11.4, 9.0, 11.4), 'm'), c((5.2, 4.4, 5.2), (10.8, 8.6, 10.8), 'l'),
             y45((5.4, 9.0, 5.4), (10.6, 11.6, 10.6), 'l'), y45((6.4, 11.6, 6.4), (9.6, 14.0, 9.6), 'l'), c((7.2, 13.8, 7.2), (8.8, 15.8, 8.8), 'l'),
             y45((7.0, 0.4, 7.0), (9.0, 2.2, 9.0), 'm')]
        for dx, dz, ax, ang in ((-4.4, 0, 'z', 22.5), (4.4, 0, 'z', -22.5), (0, -4.4, 'x', -22.5), (0, 4.4, 'x', 22.5)):
            e.append(c((8 + dx - 0.7, 3.5, 8 + dz - 0.7), (8 + dx + 0.7, 9.5, 8 + dz + 0.7), 'l', (ax, ang, (8 + dx, 3.5, 8 + dz))))
        model('ethereal_gem', {'m': 'gm_eth', 'l': 'gm_eth_lt'}, e, GEM_DISP)
        # Pearlman (faces model north): an egg of a penguin, white belly, globe-gem in gold, blue bow tie, a grin,
        # a top hat with a blue band he's tipping with one flipper, a briefcase in the other
        P = {'k': 'pm_black', 'w': 'pm_white', 'o': 'pm_orange', 'y': 'pm_yellow', 'b': 'pm_blue', 'd': 'pm_dblue', 'g': 'pm_gold',
             'e': 'pm_eye', 't': 'pm_teeth', 'c': 'pm_case', 'r': 'gm_earth'}
        pm = [c((3, 0, 0.5), (7, 1.5, 6.5), 'y'), c((9, 0, 0.5), (13, 1.5, 6.5), 'y'),
              c((2.5, 1.5, 3.5), (13.5, 14, 12.5), 'k'), c((3.5, 14, 4.5), (12.5, 19, 11.5), 'k'), c((4.5, 19, 5), (11.5, 24, 11), 'k'),
              c((4, 2.5, 3.1), (12, 13.2, 3.5), 'w'), c((5, 13, 4.1), (11, 14.6, 4.5), 'w'),
              c((6.2, 5.5, 2.7), (9.8, 9.1, 3.15), 'g'), c((6.7, 6.0, 2.45), (9.3, 8.6, 2.8), 'r'),
              c((5, 14.6, 3.8), (7.6, 16.4, 4.5), 'b'), c((8.4, 14.6, 3.8), (11, 16.4, 4.5), 'b'), c((7.4, 14.9, 3.6), (8.6, 16.1, 4.3), 'd'),
              c((6.3, 18.6, 2.4), (9.7, 20.4, 5.1), 'o'), c((6.6, 17.9, 2.8), (9.4, 18.6, 5.0), 't'), c((6.8, 17.2, 3.2), (9.2, 17.9, 5.0), 'o'),
              c((4.7, 20.3, 4.75), (7.2, 23.6, 5.05), 'e'), c((8.8, 20.3, 4.75), (11.3, 23.6, 5.05), 'e'),
              c((5.1, 22.3, 4.7), (6.1, 23.2, 4.76), 't'), c((9.2, 22.3, 4.7), (10.2, 23.2, 4.76), 't'), c((6.3, 20.7, 4.7), (6.7, 21.1, 4.76), 't'), c((10.4, 20.7, 4.7), (10.8, 21.1, 4.76), 't'),
              c((2.5, 24, 3), (13.5, 24.8, 13), 'k'), c((4.5, 24.8, 5), (11.5, 31.5, 11), 'k'), c((4.4, 24.8, 4.9), (11.6, 26.2, 11.1), 'b'),
              # the flipper tipping the hat, and the one with the briefcase
              c((12.6, 13.5, 6.4), (14.2, 24.4, 8.6), 'k', ('z', 7, (13.4, 13.5, 7.5))), c((12.0, 23.4, 6.6), (13.6, 24.2, 8.4), 'k'),
              c((1.6, 6, 6.2), (3.2, 14, 8.8), 'k', ('z', -22.5, (2.4, 14, 7.5))),
              c((-3.6, 0.4, 5.2), (1.4, 5.6, 9.8), 'c'), c((-2.2, 5.6, 7.1), (0.0, 6.8, 7.9), 'c')]
        model('pearlman', P, pm, FIXED)
    R.POST.append(post)

"""2.67: THE FRISBEE SHIELD, arrows for the Ranged kit, and the crew's health over their heads.

THE FRISBEE SHIELD   a rare find in the Gilded Gutter (rare foes, loose bricks, champions, the Rat King - and now and then a
                     Shooting Gallery won). A shield like any other, until you SNEAK AND USE it: then it flies. It skips off
                     walls and floors and off monsters (each one hit once a throw - and after a hit it heads for the next
                     monster near), five skips at most, then it comes home to your hand. Goes through the coat check with you.
RANGED KIT           the loaned Fairy Bow has no Infinity now, so the spectral arrows really get shot: 64 arrows and 32
                     spectral to start (Fletcher: 64 spectral). Every room you walk into has a quiver waiting just inside
                     the door for each Ranged raider (only they can pick it up), and every room beaten slips them 8 more.
CREW HEALTH          in a heist every raider has their health floating over their head (the heart goes yellow, then red,
                     as they get hurt) - so the crew can see who needs a hand. Hidden while you're invisible.
"""
from PIL import Image, ImageDraw
from items import item, T, ITEMS, ench
from nbt import snbt, B, F, Int
import phase72 as P72
from useitem import HOLD_REPEAT

FRZ = '#ff8a2a'
item('frisbee_shield', 'minecraft:shield', 'Frisbee Shield', FRZ,
     ['Shield, plate, frisbee - all three.', ('Sneak + use: throw it. It skips off walls', 'blue'), ('and monsters, five times at most, then', 'blue'),
      ('comes home. Each monster is hit once a throw.', 'blue'), ('Found only in the Gilded Gutter.', 'dark_gray')],
     model='bm:frisbee_shield', stack=1, comps={'minecraft:enchantments': ench(unbreaking=5, mending=1)}, cat='gear', tier=2)
HOLD_REPEAT['frisbee_shield'] = 'bm:p92/frz/hold'
P72.KEEP.append('frisbee_shield')

HOSTILE = ['zombie', 'husk', 'drowned', 'zombie_villager', 'skeleton', 'stray', 'bogged', 'wither_skeleton', 'spider', 'cave_spider', 'creeper', 'witch',
           'vindicator', 'pillager', 'evoker', 'vex', 'ravager', 'illusioner', 'piglin', 'piglin_brute', 'zombified_piglin', 'hoglin', 'zoglin', 'blaze',
           'ghast', 'magma_cube', 'slime', 'endermite', 'enderman', 'shulker', 'silverfish', 'phantom', 'guardian', 'elder_guardian', 'warden', 'breeze',
           'creaking', 'giant', 'wither']
SOFT = ['#minecraft:replaceable', '#minecraft:flowers', '#minecraft:saplings', '#minecraft:buttons', '#minecraft:pressure_plates', '#minecraft:all_signs',
        '#minecraft:wool_carpets', '#minecraft:rails', '#minecraft:banners', 'minecraft:torch', 'minecraft:wall_torch', 'minecraft:soul_torch',
        'minecraft:soul_wall_torch', 'minecraft:redstone_torch', 'minecraft:redstone_wall_torch', 'minecraft:ladder', 'minecraft:lever', 'minecraft:redstone_wire',
        'minecraft:tripwire', 'minecraft:tripwire_hook', 'minecraft:light', 'minecraft:end_rod', 'minecraft:lantern', 'minecraft:soul_lantern']
SKIPS = 5           # bounces before it turns for home
OUT = 22            # ticks out at most (about 20 blocks)
STEP = 0.45         # blocks a half-tick (two steps a tick)
DMG = 8


# ===================================================================== the art: a flying disc, blocky but round
ORANGE, RIM, HI, GROOVE, UNDER = (255, 122, 26), (255, 164, 80), (255, 214, 150), (196, 78, 14), (214, 92, 18)
GOLD, GOLD_D, GOLD_L = (255, 207, 64), (196, 150, 32), (255, 244, 170)


def textures():
    top = Image.new('RGBA', (16, 16), RIM + (255,))
    bot = Image.new('RGBA', (16, 16), RIM + (255,))
    for y in range(16):
        for x in range(16):
            dx, dy = x + 0.5 - 8, y + 0.5 - 8
            r = (dx * dx + dy * dy) ** 0.5
            if r < 2.4: c = GOLD_D if r > 1.7 else GOLD
            elif 4.4 <= r < 5.3: c = GROOVE
            elif r >= 6.6: c = HI if (dx + dy) < -5 else RIM
            else: c = ORANGE
            top.putpixel((x, y), c + (255,))
            bot.putpixel((x, y), (RIM if r >= 6.6 else UNDER) + (255,))
    for (x, y) in ((7, 6), (8, 6), (6, 7), (9, 7), (6, 8), (9, 8), (7, 9), (8, 9)):     # (a little star struck on the coin)
        pass
    for (x, y) in ((7, 7), (8, 8), (8, 7), (7, 8)):
        top.putpixel((x, y), GOLD_L + (255,))
    side = Image.new('RGBA', (16, 16), ORANGE + (255,))
    for x in range(16):
        side.putpixel((x, 7), HI + (255,)); side.putpixel((x, 8), (255, 240, 224, 255))
        for y in range(9, 16): side.putpixel((x, y), UNDER + (255,))
    return {'frisbee_top': top, 'frisbee_bottom': bot, 'frisbee_side': side}


# strips across the disc (no two overlap, so nothing z-fights): (z0, z1, x0, x1)
STRIPS = [(7, 9, 0, 16), (5, 7, 0.5, 15.5), (9, 11, 0.5, 15.5), (4, 5, 1, 15), (11, 12, 1, 15), (3, 4, 1.5, 14.5), (12, 13, 1.5, 14.5),
          (2, 3, 2.5, 13.5), (13, 14, 2.5, 13.5), (1, 2, 3.5, 12.5), (14, 15, 3.5, 12.5), (0, 1, 5.5, 10.5), (15, 16, 5.5, 10.5)]
Y0, Y1 = 7.25, 8.75


def disc_elements():
    els = []
    for (z0, z1, x0, x1) in STRIPS:
        els.append({'from': [x0, Y0, z0], 'to': [x1, Y1, z1], 'faces': {
            'up': {'uv': [x0, z0, x1, z1], 'texture': '#t'}, 'down': {'uv': [x0, 16 - z1, x1, 16 - z0], 'texture': '#b'},
            'north': {'uv': [x0, 7, x1, 8.5], 'texture': '#s'}, 'south': {'uv': [x0, 7, x1, 8.5], 'texture': '#s'},
            'east': {'uv': [z0, 7, z1, 8.5], 'texture': '#s'}, 'west': {'uv': [z0, 7, z1, 8.5], 'texture': '#s'}}})
    return els


def display(block=False):
    fp = ([85, 0, 0], [-3, 3.5, -2], 0.7) if block else ([70, 0, 12], [1.5, 1.5, -1], 0.6)
    tp = ([90, 90, 0], [-1, 3, 1.5], 0.8) if block else ([75, 90, 0], [0, 2, 1], 0.75)
    mirror = lambda r: [r[0], -r[1], -r[2]]
    return {'firstperson_righthand': {'rotation': fp[0], 'translation': fp[1], 'scale': [fp[2]] * 3},
            'firstperson_lefthand': {'rotation': mirror(fp[0]), 'translation': fp[1], 'scale': [fp[2]] * 3},
            'thirdperson_righthand': {'rotation': tp[0], 'translation': tp[1], 'scale': [tp[2]] * 3},
            'thirdperson_lefthand': {'rotation': mirror(tp[0]), 'translation': tp[1], 'scale': [tp[2]] * 3},
            'gui': {'rotation': [90, 0, 0], 'translation': [0, 0, 0], 'scale': [0.95] * 3},
            'ground': {'rotation': [0, 0, 0], 'translation': [0, 2, 0], 'scale': [0.5] * 3},
            'fixed': {'rotation': [-90, 0, 0], 'translation': [0, 0, 0], 'scale': [0.9] * 3},
            'head': {'rotation': [0, 0, 0], 'translation': [0, 6, 0], 'scale': [1.0] * 3}}


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    R.POST.append(rp_post)


def rp_post(R):
    tex = {'t': 'bm:block/frisbee_top', 'b': 'bm:block/frisbee_bottom', 's': 'bm:block/frisbee_side', 'particle': 'bm:block/frisbee_top'}
    for name, blk in (('frisbee_shield', False), ('frisbee_shield_block', True)):
        R.wj(f'assets/bm/models/item/{name}.json', {'textures': tex, 'elements': disc_elements(), 'display': display(blk)})
    mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
    R.wj('assets/bm/items/frisbee_shield.json', {'model': {'type': 'minecraft:condition', 'property': 'minecraft:using_item',
                                                           'on_true': mdl('frisbee_shield_block'), 'on_false': mdl('frisbee_shield')}})


def extend_offers(O, offer):
    pass


def generate(G):
    import os, json
    fn, wjson, tellraw, title = G.fn, G.wjson, G.tellraw, G.title
    ident = [F(0), F(0), F(0), F(1)]
    P = [T('[', 'dark_gray'), T('Heist', '#ffcf40', bold=True), T('] ', 'dark_gray')]
    objs = ['bm.frzx', 'bm.frzy', 'bm.frzz', 'bm.frzu', 'bm.frzv', 'bm.frzw', 'bm.frzt', 'bm.frzb', 'bm.frzp', 'bm.frzo', 'bm.frzh', 'bm.hpc', 'bm.hpl']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs if o != 'bm.hpc'] + ['scoreboard objectives add bm.hpc health',
                                                                                                        'scoreboard players set #-1 bm.rng -1', 'scoreboard players set #10 bm.rng 10']
    G.OBJECTIVES += objs
    wjson('bm/tags/entity_type/frz_target.json', {'values': [f'minecraft:{h}' for h in HOSTILE]})
    wjson('bm/tags/block/frz_soft.json', {'values': SOFT})
    wjson('bm/predicate/p92/invisible.json', {'condition': 'minecraft:entity_properties', 'entity': 'this',
                                              'predicate': {'minecraft:effects': {'minecraft:invisibility': {}}}})
    wjson('bm/predicate/p92/one_in_20.json', {'condition': 'minecraft:random_chance', 'chance': 0.05})
    foe = 'type=#bm:frz_target,tag=!bm.frzhit,tag=!bm.npc,tag=!bm.fvault'

    # ================================================================== THE FRISBEE SHIELD
    disc = {'Tags': ['bm.frz', 'bm.frznew'], 'item_display': 'none', 'teleport_duration': Int(1), 'interpolation_duration': Int(1),
            'item': {'id': 'minecraft:shield', 'count': Int(1)},
            'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0)] * 3, 'scale': [F(0.8)] * 3}}
    fn('p92/frz/hold', ['execute unless score #first bm.hnow matches 1 run return 0', 'execute unless predicate bm:p20/sneaking run return 0',
                        'function bm:p92/frz/throw'])
    hold = '*[minecraft:custom_data~{bm:"frisbee_shield"}]'
    fn('p92/frz/throw', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                         'scoreboard players set #h bm.rng 0', f'execute unless items entity @s weapon.mainhand {hold} run scoreboard players set #h bm.rng 1',
                         f'execute if score #h bm.rng matches 1 unless items entity @s weapon.offhand {hold} run return 0',
                         f'execute anchored eyes positioned ^ ^ ^0.7 run summon minecraft:item_display ~ ~ ~ {snbt(disc)}',
                         'execute anchored eyes positioned ^ ^ ^0.7 run summon minecraft:marker ~ ~ ~ {Tags:["bm.frzm0"]}',
                         f'execute anchored eyes positioned ^ ^ ^{0.7 + STEP} run summon minecraft:marker ~ ~ ~ {{Tags:["bm.frzm1"]}}',
                         'execute if score #h bm.rng matches 0 run item replace entity @e[type=minecraft:item_display,tag=bm.frznew,limit=1] contents from entity @s weapon.mainhand',
                         'execute if score #h bm.rng matches 1 run item replace entity @e[type=minecraft:item_display,tag=bm.frznew,limit=1] contents from entity @s weapon.offhand',
                         'execute if score #h bm.rng matches 0 run item replace entity @s weapon.mainhand with minecraft:air',
                         'execute if score #h bm.rng matches 1 run item replace entity @s weapon.offhand with minecraft:air',
                         'scoreboard players operation #o bm.rng = @s bm.pid',
                         'execute as @e[type=minecraft:item_display,tag=bm.frznew,limit=1] run function bm:p92/frz/setup',
                         'kill @e[type=minecraft:marker,tag=bm.frzm0]', 'kill @e[type=minecraft:marker,tag=bm.frzm1]',
                         'playsound minecraft:entity.breeze.shoot player @a[distance=..16] ~ ~ ~ 0.8 1.6', 'playsound minecraft:item.trident.throw player @a[distance=..16] ~ ~ ~ 0.6 1.4'])
    fn('p92/frz/setup', ['tag @s remove bm.frznew', 'scoreboard players operation @s bm.frzo = #o bm.rng', 'scoreboard players operation @s bm.frzh = #h bm.rng'] +
       [f'execute store result score @s bm.frz{a} run data get entity @e[type=minecraft:marker,tag=bm.frzm0,limit=1] Pos[{i}] 1000' for i, a in enumerate('xyz')] +
       sum(([f'execute store result score @s bm.frz{v} run data get entity @e[type=minecraft:marker,tag=bm.frzm1,limit=1] Pos[{i}] 1000',
             f'scoreboard players operation @s bm.frz{v} -= @s bm.frz{a}'] for i, (a, v) in enumerate(zip('xyz', 'uvw'))), []) +
       ['scoreboard players set @s bm.frzt 0', 'scoreboard players set @s bm.frzb 0', 'scoreboard players set @s bm.frzp 0'])
    spin = [[F(0), F(0), F(0), F(1)], [F(0), F(0.7071), F(0), F(0.7071)], [F(0), F(1), F(0), F(0)], [F(0), F(0.7071), F(0), F(-0.7071)]]
    fn('p92/frz/fly', ['scoreboard players add @s bm.frzt 1', 'scoreboard players operation #o bm.rng = @s bm.frzo',
                       'execute as @a if score @s bm.pid = #o bm.rng run tag @s add bm.frzme',
                       'execute unless entity @a[tag=bm.frzme,distance=..96] run return run function bm:p92/frz/drop',
                       'execute if score @s bm.frzt matches 300.. run return run function bm:p92/frz/drop',
                       'scoreboard players operation #q bm.rng = @s bm.frzt', 'scoreboard players operation #q bm.rng %= #4 bm.rng'] +
       [f'execute if score #q bm.rng matches {i} run data merge entity @s ' + snbt({'start_interpolation': Int(0), 'transformation': {'left_rotation': q}}) for i, q in enumerate(spin)] +
       ['execute if score @s bm.frzp matches 0 run function bm:p92/frz/out', 'execute if score @s bm.frzp matches 1 run function bm:p92/frz/back',
        'tag @a[tag=bm.frzme] remove bm.frzme'])
    fn('p92/frz/out', ['function bm:p92/frz/check', 'function bm:p92/frz/move', 'execute at @s run function bm:p92/frz/check', 'function bm:p92/frz/move',
                       f'execute if score @s bm.frzb matches {SKIPS}.. run scoreboard players set @s bm.frzp 1',
                       f'execute if score @s bm.frzt matches {OUT}.. run scoreboard players set @s bm.frzp 1',
                       'execute at @s run particle minecraft:dust{color:[1.0,0.55,0.15],scale:0.8} ~ ~ ~ 0 0 0 0 1'])
    # (as the disc, at it) the walls ahead on each axis (the rim reaches 0.45 out; it is thin, so 0.2 up and down), then a monster in its way
    fn('p92/frz/check', ['execute if score @s bm.frzp matches 1 run return 0',
                         'execute if score @s bm.frzu matches 1.. unless block ~0.45 ~ ~ #bm:frz_soft run function bm:p92/frz/flip_u',
                         'execute if score @s bm.frzu matches ..-1 unless block ~-0.45 ~ ~ #bm:frz_soft run function bm:p92/frz/flip_u',
                         'execute if score @s bm.frzw matches 1.. unless block ~ ~ ~0.45 #bm:frz_soft run function bm:p92/frz/flip_w',
                         'execute if score @s bm.frzw matches ..-1 unless block ~ ~ ~-0.45 #bm:frz_soft run function bm:p92/frz/flip_w',
                         'execute if score @s bm.frzv matches 1.. unless block ~ ~0.2 ~ #bm:frz_soft run function bm:p92/frz/flip_v',
                         'execute if score @s bm.frzv matches ..-1 unless block ~ ~-0.2 ~ #bm:frz_soft run function bm:p92/frz/flip_v',
                         'scoreboard players set #hit bm.rng 0',
                         f'execute positioned ~-0.5 ~-0.5 ~-0.5 as @e[{foe},dx=0,dy=0,dz=0,limit=1] at @s run function bm:p92/frz/hitmob',
                         'execute if score #hit bm.rng matches 1 run function bm:p92/frz/retarget'])
    for ax in 'uvw':
        fn(f'p92/frz/flip_{ax}', [f'scoreboard players operation @s bm.frz{ax} *= #-1 bm.rng', 'scoreboard players add @s bm.frzb 1',
                                  'playsound minecraft:block.wood.hit player @a[distance=..16] ~ ~ ~ 0.9 1.6', 'particle minecraft:crit ~ ~ ~ 0.1 0.1 0.1 0.1 4',
                                  f'execute if score @s bm.frzb matches {SKIPS}.. run scoreboard players set @s bm.frzp 1'])
    fn('p92/frz/move', ['execute if score @s bm.frzp matches 1 run return 0'] +
       sum(([f'scoreboard players operation @s bm.frz{a} += @s bm.frz{v}',
             f'execute store result entity @s Pos[{i}] double 0.001 run scoreboard players get @s bm.frz{a}'] for i, (a, v) in enumerate(zip('xyz', 'uvw'))), []))
    fn('p92/frz/hitmob', ['scoreboard players set #hit bm.rng 1', 'tag @s add bm.frzhit', f'damage @s {DMG} minecraft:player_attack by @a[tag=bm.frzme,limit=1]',
                          'execute at @s run particle minecraft:crit ~ ~1 ~ 0.3 0.4 0.3 0.2 12',
                          'execute at @s run playsound minecraft:item.shield.block player @a[distance=..16] ~ ~ ~ 1 1.5'])
    # after a hit: off to the nearest monster it hasn't hit yet (or straight back the way it came)
    fn('p92/frz/retarget', ['scoreboard players add @s bm.frzb 1', f'execute if score @s bm.frzb matches {SKIPS}.. run return run scoreboard players set @s bm.frzp 1',
                            'tag @e[tag=bm.frztgt] remove bm.frztgt', f'tag @e[{foe},distance=..10,limit=1,sort=nearest] add bm.frztgt',
                            'execute unless entity @e[tag=bm.frztgt] run return run function bm:p92/frz/reverse',
                            f'execute facing entity @e[tag=bm.frztgt,limit=1] eyes run summon minecraft:marker ^ ^ ^{STEP} {{Tags:["bm.frzm1"]}}'] +
       sum(([f'execute store result score @s bm.frz{v} run data get entity @e[type=minecraft:marker,tag=bm.frzm1,limit=1] Pos[{i}] 1000',
             f'scoreboard players operation @s bm.frz{v} -= @s bm.frz{a}'] for i, (a, v) in enumerate(zip('xyz', 'uvw'))), []) +
       ['kill @e[type=minecraft:marker,tag=bm.frzm1]', 'tag @e[tag=bm.frztgt] remove bm.frztgt'])
    fn('p92/frz/reverse', [f'scoreboard players operation @s bm.frz{v} *= #-1 bm.rng' for v in 'uvw'])
    # home again: straight to the thrower's eyes, through anything (hitting monsters it hasn't yet on the way)
    fn('p92/frz/back', ['execute facing entity @a[tag=bm.frzme,limit=1] eyes run tp @s ^ ^ ^0.9',
                        'execute at @s if entity @a[tag=bm.frzme,distance=..1.9] run return run function bm:p92/frz/catch',
                        f'execute at @s positioned ~-0.5 ~-0.5 ~-0.5 as @e[{foe},dx=0,dy=0,dz=0,limit=1] at @s run function bm:p92/frz/hitmob',
                        'execute at @s run particle minecraft:dust{color:[1.0,0.55,0.15],scale:0.8} ~ ~ ~ 0 0 0 0 1'])
    fn('p92/frz/catch', ['tag @s add bm.frzc', 'scoreboard players set #ok bm.rng 0',
                         'execute if score @s bm.frzh matches 1 as @a[tag=bm.frzme,limit=1] unless items entity @s weapon.offhand * run function bm:p92/frz/to_off',
                         'execute if score #ok bm.rng matches 0 as @a[tag=bm.frzme,limit=1] unless items entity @s weapon.mainhand * run function bm:p92/frz/to_main',
                         'execute if score #ok bm.rng matches 0 as @a[tag=bm.frzme,limit=1] unless items entity @s weapon.offhand * run function bm:p92/frz/to_off',
                         'execute if score #ok bm.rng matches 0 at @a[tag=bm.frzme,limit=1] run function bm:p92/frz/to_ground',
                         'execute at @a[tag=bm.frzme,limit=1] run playsound minecraft:item.armor.equip_leather player @a[distance=..16] ~ ~ ~ 1 1.4',
                         'function bm:p92/frz/gone'])
    fn('p92/frz/to_off', ['item replace entity @s weapon.offhand from entity @e[type=minecraft:item_display,tag=bm.frzc,limit=1] contents', 'scoreboard players set #ok bm.rng 1'])
    fn('p92/frz/to_main', ['item replace entity @s weapon.mainhand from entity @e[type=minecraft:item_display,tag=bm.frzc,limit=1] contents', 'scoreboard players set #ok bm.rng 1'])
    fn('p92/frz/to_ground', ['summon minecraft:item ~ ~0.5 ~ {Item:{id:"minecraft:shield",count:1},PickupDelay:0,Age:-32768,Tags:["bm.frzi"]}',
                             'data modify entity @e[type=minecraft:item,tag=bm.frzi,limit=1] Item set from entity @e[type=minecraft:item_display,tag=bm.frzc,limit=1] item',
                             'tag @e[type=minecraft:item,tag=bm.frzi] remove bm.frzi'])
    # its thrower gone (logged off, far away, another world) or flying too long: it drops where it is, and waits
    fn('p92/frz/drop', ['tag @s add bm.frzc', 'function bm:p92/frz/to_ground', 'particle minecraft:poof ~ ~ ~ 0.1 0.1 0.1 0.02 4', 'function bm:p92/frz/gone'])
    fn('p92/frz/gone', ['tag @a[tag=bm.frzme] remove bm.frzme', 'tag @s add bm.frzdead', 'kill @s',
                        'execute unless entity @e[type=minecraft:item_display,tag=bm.frz,tag=!bm.frzdead] run tag @e[tag=bm.frzhit] remove bm.frzhit'])
    G.FUNCS['tick'].append('execute as @e[type=minecraft:item_display,tag=bm.frz,tag=!bm.frzdead] at @s run function bm:p92/frz/fly')
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #4 bm.rng 4']

    # where it's found: the vault's rare tables, and one Shooting Gallery won in twenty
    wjson('bm/loot_table/p92/frisbee.json', {'pools': [{'rolls': 1, 'entries': [G.loot_entry('frisbee_shield')]}]})
    for tb, w in (('shiny', 2), ('ratking', 0), ('secret', 1), ('champion', 1)):
        pth = G.path('data', 'bm', 'loot_table', 'p76', f'{tb}.json')
        if not os.path.exists(pth): continue
        lt = json.load(open(pth))
        if tb == 'ratking':
            lt['pools'].append({'rolls': 1, 'entries': [dict(G.loot_entry('frisbee_shield'), weight=1), {'type': 'minecraft:empty', 'weight': 7}]})
        else:
            lt['pools'][0]['entries'].append(dict(G.loot_entry('frisbee_shield'), weight=w))
        wjson(f'bm/loot_table/p76/{tb}.json', lt)
    G.FUNCS['p91/gallery/won'] += ['execute as @a[tag=bm.gvp,distance=..24] if predicate bm:p92/one_in_20 run function bm:p92/frz/gallery']
    fn('p92/frz/gallery', ['function bm:p81/defer {t:"bm:p92/frisbee"}',
                           tellraw('@s', P + [T('Behind the last target, something round and orange... ', FRZ, bold=True), T('(it\'s in your haul)', 'gray')])])
    fn('admin/frisbee', [G.give('frisbee_shield')])

    # ================================================================== THE RANGED KIT'S ARROWS
    arrow = lambda iid: f'{iid}[minecraft:custom_data={{bm_kit:1b}},minecraft:lore=[{snbt(T("Loaned by the Fixer - stays in the vault.", "dark_gray"))}]]'
    quiver = lambda iid, n: snbt({'Item': {'id': iid, 'count': Int(n), 'components': {'minecraft:custom_data': {'bm_kit': B(1)},
                                                                                     'minecraft:lore': [T('Loaned by the Fixer - stays in the vault.', 'dark_gray')]}},
                                  'PickupDelay': Int(10), 'Age': Int(-32768), 'Glowing': B(1), 'Tags': ['bm.gvprop', 'bm.qvnew']})
    # (as a room's marker, the first time anyone walks in) a quiver just inside the door for each Ranged raider here - theirs alone
    G.FUNCS['p76/first_visit'] += ['tag @a[tag=bm.gvp,scores={bm.gvrole=3},distance=..30] add bm.qvwho', 'execute if entity @a[tag=bm.qvwho] run function bm:p92/quiver']
    fn('p92/quiver', ['tag @a[tag=bm.qvwho,limit=1] add bm.qvme', f'summon minecraft:item ~-10 ~0.5 ~ {quiver("minecraft:arrow", 16)}',
                      f'execute if predicate bm:p76/half run summon minecraft:item ~-10 ~0.5 ~ {quiver("minecraft:spectral_arrow", 6)}',
                      'execute as @e[type=minecraft:item,tag=bm.qvnew,distance=..16] run data modify entity @s Owner set from entity @a[tag=bm.qvme,limit=1] UUID',
                      'tag @e[type=minecraft:item,tag=bm.qvnew] remove bm.qvnew', 'tag @a[tag=bm.qvme] remove bm.qvwho', 'tag @a[tag=bm.qvme] remove bm.qvme',
                      'execute if entity @a[tag=bm.qvwho] run function bm:p92/quiver'])
    wjson('bm/predicate/p76/half.json', {'condition': 'minecraft:random_chance', 'chance': 0.5})
    G.FUNCS['p70/solved'] += ['execute as @a[tag=bm.gvp,scores={bm.gvrole=3},distance=..300] if score @s bm.gvi = #gi bm.rng run give @s ' + arrow('minecraft:arrow') + ' 8']

    # ================================================================== THE CREW'S HEALTH, OVER THEIR HEADS
    bar = {'Tags': ['bm.hpbar', 'bm.hpnew'], 'billboard': 'center', 'see_through': B(0), 'shadow': B(1), 'background': Int(0x40000000), 'teleport_duration': Int(1),
           'text': '', 'line_width': Int(200), 'view_range': F(0.6),
           'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0)] * 3, 'scale': [F(0.55)] * 3}}
    # every tick: each raider's bar to just above their name (tucked away while they're invisible)
    G.FUNCS['tick'].append('execute in bm:gutter as @a[tag=bm.gvp,distance=0..] at @s run function bm:p92/hp/follow')
    fn('p92/hp/follow', ['scoreboard players operation #p bm.rng = @s bm.pid',
                         'execute if predicate bm:p92/invisible as @e[type=minecraft:text_display,tag=bm.hpbar,distance=0..] if score @s bm.pid = #p bm.rng run return run tp @s ~ ~-6 ~',
                         'execute as @e[type=minecraft:text_display,tag=bm.hpbar,distance=0..] if score @s bm.pid = #p bm.rng run tp @s ~ ~2.45 ~'])
    # every quarter second: a bar for anyone without one, the number if it changed, and bars nobody owns any more cleared away
    G.FUNCS['loop/fast'][-1:-1] = ['execute in bm:gutter run function bm:p92/hp/all']
    fn('p92/hp/all', ['tag @e[type=minecraft:text_display,tag=bm.hpbar,distance=0..] add bm.hpold',
                      'execute as @a[tag=bm.gvp,distance=0..] at @s run function bm:p92/hp/me',
                      'kill @e[type=minecraft:text_display,tag=bm.hpold,distance=0..]'])
    fn('p92/hp/me', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                     'scoreboard players operation #p bm.rng = @s bm.pid', 'scoreboard players set #has bm.rng 0',
                     'execute as @e[type=minecraft:text_display,tag=bm.hpbar,distance=0..] if score @s bm.pid = #p bm.rng run function bm:p92/hp/mine',
                     'execute if score #has bm.rng matches 0 run function bm:p92/hp/new',
                     'execute if score @s bm.hpc = @s bm.hpl run return 0', 'scoreboard players operation @s bm.hpl = @s bm.hpc',
                     'execute store result storage bm:gv hp.h int 1 run scoreboard players get @s bm.hpc',
                     'execute store result score #m bm.rng run attribute @s minecraft:max_health get',
                     'execute store result storage bm:gv hp.m int 1 run scoreboard players get #m bm.rng',
                     'scoreboard players operation #f bm.rng = @s bm.hpc', 'scoreboard players operation #f bm.rng *= #10 bm.rng', 'scoreboard players operation #f bm.rng /= #m bm.rng',
                     'data modify storage bm:gv hp.c set value "#5ad84a"', 'execute if score #f bm.rng matches ..6 run data modify storage bm:gv hp.c set value "#ffd040"',
                     'execute if score #f bm.rng matches ..3 run data modify storage bm:gv hp.c set value "#ff4a4a"',
                     'execute as @e[type=minecraft:text_display,tag=bm.hpbar,distance=0..] if score @s bm.pid = #p bm.rng run function bm:p92/hp/set with storage bm:gv hp'])
    fn('p92/hp/mine', ['execute if score #has bm.rng matches 1 run return run kill @s', 'scoreboard players set #has bm.rng 1', 'tag @s remove bm.hpold'])
    fn('p92/hp/new', [f'summon minecraft:text_display ~ ~2.45 ~ {snbt(bar)}', 'scoreboard players operation @e[type=minecraft:text_display,tag=bm.hpnew] bm.pid = #p bm.rng',
                      'tag @e[type=minecraft:text_display,tag=bm.hpnew] remove bm.hpnew', 'scoreboard players set @s bm.hpl -1'])
    fn('p92/hp/set', ['$data modify entity @s text set value [{text:"❤ ",color:"$(c)"},{text:"$(h)",color:"white",bold:true},{text:" / $(m)",color:"gray"}]'])
    G.FUNCS['p70/unraid'][0:0] = ['scoreboard players operation #p bm.rng = @s bm.pid',
                                  'execute as @e[type=minecraft:text_display,tag=bm.hpbar] if score @s bm.pid = #p bm.rng run kill @s']

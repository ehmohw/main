"""2.85b: ANGELIC FORGING - the Hollow King's Regalia and Apophiss's crowns, purified with a Golden Cross.

THE FORGE      toss a piece of the Regalia (the Deathmask, the Ribcage, the Greaves, the Treads), one of the King's tools (the
               Soulreaver, the Gravedigger's Maw, the Headsman's Grief, the Barrow Spade, the Witherstring), Sepulchre, or
               Apophiss's True or Unbound Crown down beside a Golden Cross. Light gathers for four seconds and the thing comes up
               ANGELIC: white and gold, the same item - its enchantments, Dread tunings and infusions kept - with no more power
               than before. The cross is spent.
WHAT CHANGES   the look (white and gold; the armour's trims turn gold), the light round it (a halo, motes of sun, feathers of
               light instead of souls and smoke), and WHEN IT WAKES: by day instead of by night - sunlight wakes it as night
               did (+15% damage), high noon as the moons did (+30% damage, +10% speed). The Blood Moon still wakes it fully (holy
               things burn against the moon's monsters). Night, the moons and an invasion no longer do; at home in the Nether or
               the Hollow it is as strong as ever. A crown's night gift (Strength II and Regeneration) comes by day instead - and
               on a Blood Moon. Sepulchre and the Mace's wrath gather by the same light when you wear the angelic set (or hold
               angelic Sepulchre without the Regalia on).
               The set is angelic when every piece of the Regalia you wear is; one corrupt piece and it's the old Regalia again.
CORRUPTION     toss an angelic thing onto Apophiss's seal in the Hollow's throne room: black fire takes it back.
A RE-SYNC      (a new item version) keeps it angelic.
"""
import json
import math
from items import T, ITEMS
from nbt import snbt, B, F, Int

HOLY, HOLY_D = '#fff2b8', '#e8c860'
ANGEL_IDS = ['conq_helmet', 'conq_chestplate', 'conq_leggings', 'conq_boots', 'conq_blade', 'conq_pick', 'conq_axe', 'conq_shovel',
             'conq_hoe', 'conq_bow', 'sepulchre', 'apo_true_crown', 'apo_unbound_crown']
ARMOR = {'conq_helmet': 'head', 'conq_chestplate': 'chest', 'conq_leggings': 'legs', 'conq_boots': 'feet'}
VANILLA = {'conq_helmet': 'netherite_helmet', 'conq_chestplate': 'netherite_chestplate', 'conq_leggings': 'netherite_leggings',
           'conq_boots': 'netherite_boots', 'conq_blade': 'netherite_sword', 'conq_pick': 'netherite_pickaxe', 'conq_axe': 'netherite_axe',
           'conq_shovel': 'netherite_shovel', 'conq_hoe': 'netherite_hoe', 'conq_bow': 'bow', 'sepulchre': 'mace'}
holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
ANGEL = '*[minecraft:custom_data~{bm_angel:1b}]'
PURE = [T('✦ Purified: it wakes by day, not by night.', HOLY_D), T('  (A Blood Moon still wakes it.)', HOLY_D)]


def ids():
    return [i for i in ANGEL_IDS if i in ITEMS]


def angel_name(iid):
    return {'text': '', 'italic': False, 'extra': [{'text': '✦ ', 'color': HOLY_D}, {'text': 'Angelic ' + ITEMS[iid]['name'], 'color': HOLY, 'bold': True},
                                                   {'text': ' ✦', 'color': HOLY_D}]}


def generate(G):
    fn, wjson, title, tellraw, give = G.fn, G.wjson, G.title, G.tellraw, G.give
    P = [T('[', 'dark_gray'), T('Black Market', 'dark_purple', bold=True), T('] ', 'dark_gray')]
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    second, fast = G.FUNCS['loop/second'], G.FUNCS['loop/fast']
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.angf dummy']
    G.OBJECTIVES += ['bm.angf']
    IDS = ids()
    assert len(IDS) >= 12, IDS

    # ================================================================== the two changes, as item modifiers (one per item: its own look back)
    for iid in IDS:
        c = ITEMS[iid]['comps']
        model = c.get('minecraft:item_model') or f'minecraft:{VANILLA[iid]}'
        up = {'minecraft:item_name': angel_name(iid), 'minecraft:item_model': f'bm:angel_{iid}'}
        down = {'minecraft:item_name': c['minecraft:item_name'], 'minecraft:item_model': model}
        if iid in ARMOR:
            up['minecraft:equippable'] = {'slot': ARMOR[iid], 'asset_id': 'bm:angelic', 'equip_sound': 'minecraft:item.armor.equip_gold'}
            down['minecraft:equippable'] = c.get('minecraft:equippable') or {'slot': ARMOR[iid], 'asset_id': 'minecraft:netherite',
                                                                             'equip_sound': 'minecraft:item.armor.equip_netherite'}
            up['minecraft:trim'] = {'material': 'minecraft:gold', 'pattern': 'minecraft:silence'}
            down['minecraft:trim'] = {'material': 'minecraft:quartz', 'pattern': 'minecraft:silence'}
        wjson(f'bm/item_modifier/p182/up_{iid}.json', [{'function': 'minecraft:set_custom_data', 'tag': '{bm_angel:1b}'},
                                                       {'function': 'minecraft:set_components', 'components': up},
                                                       {'function': 'minecraft:set_lore', 'mode': 'insert', 'offset': 0, 'lore': PURE}])
        wjson(f'bm/item_modifier/p182/down_{iid}.json', [{'function': 'minecraft:set_custom_data', 'tag': '{bm_angel:0b}'},
                                                         {'function': 'minecraft:set_components', 'components': down},
                                                         {'function': 'minecraft:set_lore', 'mode': 'replace_section', 'offset': 0, 'size': len(PURE), 'lore': []}])
    fn('p182/up', [f'execute if items entity @s contents {holds(i)} run return run item modify entity @s contents bm:p182/up_{i}' for i in IDS])
    fn('p182/down', [f'execute if items entity @s contents {holds(i)} run return run item modify entity @s contents bm:p182/down_{i}' for i in IDS])

    # ================================================================== THE FORGE: beside a Golden Cross on the ground
    cross = holds('golden_cross')
    for i in IDS:
        second.append(f'execute as @e[type=minecraft:item,tag=!bm.angf] if items entity @s contents {holds(i)} unless items entity @s contents {ANGEL} '
                      f'at @s if entity @e[type=minecraft:item,distance=..2.5,tag=!bm.angf] run function bm:p182/f/try')
    fn('p182/f/try', [f'execute as @e[type=minecraft:item,distance=..2.5,tag=!bm.angf] if items entity @s contents {cross} run tag @s add bm.angq',
                      'execute unless entity @e[type=minecraft:item,tag=bm.angq,distance=..2.5] run return 0',
                      'tag @s add bm.angf', 'scoreboard players set @s bm.angf 4', 'data modify entity @s PickupDelay set value 32767s',
                      'data modify entity @s Motion set value [0.0d, 0.0d, 0.0d]',
                      'execute as @e[type=minecraft:item,tag=bm.angq,distance=..2.5,sort=nearest,limit=1] run function bm:p182/f/hold',
                      'tag @e[type=minecraft:item,tag=bm.angq] remove bm.angq',
                      'playsound minecraft:block.beacon.activate block @a[distance=..16] ~ ~ ~ 1 1.6',
                      'playsound minecraft:block.bell.resonate block @a[distance=..16] ~ ~ ~ 1 1.4',
                      'execute as @a[distance=..12] run ' + title('@s', 'actionbar', T('Light gathers round the cross...', HOLY, italic=True))])
    fn('p182/f/hold', ['tag @s add bm.angf', 'tag @s add bm.angc', 'data modify entity @s PickupDelay set value 32767s'])
    second.append('execute as @e[type=minecraft:item,tag=bm.angf,tag=!bm.angc] at @s run function bm:p182/f/tick')
    fn('p182/f/tick', ['execute unless entity @e[type=minecraft:item,tag=bm.angc,distance=..3] run return run function bm:p182/f/fail',
                       'scoreboard players remove @s bm.angf 1',
                       'particle minecraft:end_rod ~ ~0.6 ~ 0.08 1.2 0.08 0.02 20', 'particle minecraft:wax_on ~ ~0.8 ~ 0.6 0.6 0.6 0 12',
                       'particle minecraft:dust{color:[1.0,0.92,0.55],scale:1.4} ~ ~1.5 ~ 0.4 1.0 0.4 0 16',
                       'playsound minecraft:block.amethyst_block.chime block @a[distance=..16] ~ ~ ~ 1 1.8',
                       'execute if score @s bm.angf matches ..0 run function bm:p182/f/done'])
    fn('p182/f/fail', ['tag @s remove bm.angf', 'data modify entity @s PickupDelay set value 0s', 'scoreboard players reset @s bm.angf',
                       'tag @e[type=minecraft:item,tag=bm.angc,distance=..6] remove bm.angf', 'tag @e[type=minecraft:item,tag=bm.angc,distance=..6] remove bm.angc'])
    fn('p182/f/done', ['function bm:p182/up', 'tag @s remove bm.angf', 'scoreboard players reset @s bm.angf', 'data modify entity @s PickupDelay set value 10s',
                       'data modify entity @s Motion set value [0.0d, 0.25d, 0.0d]',
                       'execute as @e[type=minecraft:item,tag=bm.angc,distance=..3,limit=1] run function bm:p182/f/spend',
                       'particle minecraft:flash{color:[1.0,1.0,0.9,1.0]} ~ ~0.7 ~ 0 0 0 0 1', 'particle minecraft:end_rod ~ ~0.7 ~ 0.3 0.3 0.3 0.25 50',
                       'particle minecraft:totem_of_undying ~ ~0.8 ~ 0.3 0.4 0.3 0.4 40',
                       'playsound minecraft:item.totem.use block @a[distance=..16] ~ ~ ~ 0.7 1.4',
                       'playsound minecraft:ui.toast.challenge_complete block @a[distance=..16] ~ ~ ~ 0.8 1.3',
                       'execute as @a[distance=..12] run ' + title('@s', 'actionbar', T('It comes up white and gold - purified.', HOLY, bold=True))])
    fn('p182/f/spend', ['tag @s remove bm.angf', 'tag @s remove bm.angc', 'data modify entity @s PickupDelay set value 0s',
                        'execute store result score #n bm.rng run data get entity @s Item.count',
                        'execute if score #n bm.rng matches ..1 run return run kill @s',
                        'item modify entity @s contents {function:"minecraft:set_count",count:-1,add:true}'])

    # ================================================================== CORRUPTION: tossed onto Apophiss's seal
    second.append('execute in bm:hollow_throne as @e[type=minecraft:marker,tag=bm.apseal] at @s as @e[type=minecraft:item,distance=..3] '
                  f'if items entity @s contents {ANGEL} at @s run function bm:p182/corrupt')
    fn('p182/corrupt', ['function bm:p182/down', 'data modify entity @s Motion set value [0.0d, 0.3d, 0.0d]',
                        'particle minecraft:soul_fire_flame ~ ~0.5 ~ 0.3 0.6 0.3 0.04 40', 'particle minecraft:squid_ink ~ ~0.5 ~ 0.3 0.3 0.3 0.05 30',
                        'particle minecraft:sculk_soul ~ ~0.6 ~ 0.3 0.5 0.3 0.03 16',
                        'playsound minecraft:entity.wither.ambient block @a[distance=..24] ~ ~ ~ 1 0.6',
                        'playsound minecraft:entity.evoker.prepare_summon block @a[distance=..24] ~ ~ ~ 0.8 0.6',
                        'execute as @a[distance=..16] run ' + title('@s', 'actionbar', T('Black fire takes it back. The serpent remembers its own.', '#5ac87a', italic=True))])

    # ================================================================== A RE-SYNC KEEPS IT ANGELIC
    rs = G.FUNCS['p18/refresh/slot']
    k = next(i for i, l in enumerate(rs) if 'rf.iid set from entity' in l)
    rs[k + 1:k + 1] = ['$data modify storage bm:tmp rf.ang set from entity @s $(path).components."minecraft:custom_data".bm_angel']
    rs += ['execute if data storage bm:tmp rf.iid if data storage bm:tmp {rf:{ang:1b}} run function bm:p182/rs with storage bm:tmp rf']
    fn('p182/rs', [f'$execute if data storage bm:tmp {{rf:{{iid:"{i}"}}}} run return run item modify entity @s $(slot) bm:p182/up_{i}' for i in IDS])

    # ================================================================== WHO IS ANGELIC: every Regalia piece they wear is
    some = f'*[minecraft:custom_data~{{bm_set:"conqueror"}}]'
    corrupt = f'*[minecraft:custom_data~{{bm_set:"conqueror"}},!minecraft:custom_data~{{bm_angel:1b}}]'
    k = next(i for i, l in enumerate(second) if 'function bm:p2/rg/second' in l)
    second[k:k] = ['execute as @a[tag=bm.angel] unless items entity @s armor.* ' + some + ' run function bm:p182/unangel',
                   'execute as @a[gamemode=!spectator] if items entity @s armor.* ' + some + ' run function bm:p182/angel_tag']
    fn('p182/angel_tag', ['scoreboard players set #an bm.rng 0',
                          f'execute if items entity @s armor.* {ANGEL} unless items entity @s armor.* {corrupt} run scoreboard players set #an bm.rng 1',
                          'execute if score #an bm.rng matches 1 unless entity @s[tag=bm.angel] run return run function bm:p182/angel_on',
                          'execute if score #an bm.rng matches 0 if entity @s[tag=bm.angel] run function bm:p182/unangel'])
    fn('p182/angel_on', ['tag @s add bm.angel', 'scoreboard players reset @s bm.rgt'])
    fn('p182/unangel', ['tag @s remove bm.angel', 'scoreboard players reset @s bm.rgt'])
    fn('p182/is_angel', ['execute if entity @s[tag=bm.angel] run return 1', 'execute if entity @s[tag=bm.rgon] run return 0',
                         f'execute if items entity @s weapon.mainhand {ANGEL} run return 1', 'return 0'])
    # its waking by day: sunlight is the old night (1), high noon the old moons (2); the Blood Moon (3) and home (5) as before
    G.FUNCS['p2/rg/tier'].append('execute if function bm:p182/is_angel run function bm:p182/tier')
    fn('p182/tier', ['execute if score #rg bm.rng matches 1..2 run scoreboard players set #rg bm.rng 0',
                     'execute if score #rg bm.rng matches 4 run scoreboard players set #rg bm.rng 0',
                     'execute if dimension minecraft:overworld if score #tod bm.bm matches 0..12999 run scoreboard players set #rg bm.rng 1',
                     'execute if dimension minecraft:overworld if score #tod bm.bm matches 4500..7500 unless predicate bm:p182/storm run scoreboard players set #rg bm.rng 2'])
    wjson('bm/predicate/p182/storm.json', {'condition': 'minecraft:weather_check', 'raining': True})
    # its trims and words when it wakes, and its light
    G.FUNCS['p2/rg/wake'].insert(0, 'execute if entity @s[tag=bm.angel] run return run function bm:p182/wake')
    msgs = {0: ('The purified Regalia rests.', 'gray', 'quartz'), 1: ('The sun finds the Regalia. It shines.', HOLY, 'gold'),
            2: ('High noon: the Regalia blazes white.', HOLY, 'gold'), 3: ('The purified Regalia burns against the Blood Moon!', '#ff8a6a', 'redstone'),
            5: ('The Regalia remembers this place - and serves you here all the same.', HOLY_D, 'gold')}
    slots = {'helmet': 'armor.head', 'chestplate': 'armor.chest', 'leggings': 'armor.legs', 'boots': 'armor.feet'}
    for t, (msg, col, mat) in msgs.items():
        comps = '{"minecraft:trim":{material:"minecraft:%s",pattern:"minecraft:silence"}}' % mat
        fn(f'p182/wake_{t}', [f'execute if items entity @s {sl} {ANGEL} run item modify entity @s {sl} {{function:"minecraft:set_components",components:{comps}}}'
                              for sl in slots.values()] + [title('@s', 'actionbar', T(msg, col, italic=True))])
    fn('p182/wake', [f'execute if score #rg bm.rng matches {t} run function bm:p182/wake_{t}' for t in msgs] +
       ['scoreboard players operation @s bm.rgt = #rg bm.rng',
        'execute if score #rg bm.rng matches 1.. run playsound minecraft:block.beacon.power_select player @s ~ ~ ~ 0.5 1.6',
        'execute if score #rg bm.rng matches 1.. run particle minecraft:end_rod ~ ~1 ~ 0.4 0.8 0.4 0.03 20'])
    G.FUNCS['p2/rg/fast'].insert(0, 'execute if entity @s[tag=bm.angel] run return run function bm:p182/fast')
    halo = [f'particle minecraft:dust{{color:[1.0,0.9,0.45],scale:0.6}} ~{0.3 * math.cos(2 * math.pi * i / 8):.2f} ~2.3 ~{0.3 * math.sin(2 * math.pi * i / 8):.2f} 0 0 0 0 1'
            for i in range(8)]
    fn('p182/fx_0', ['particle minecraft:wax_on ~ ~1.2 ~ 0.3 0.5 0.3 0 1'])
    fn('p182/fx_1', halo + ['particle minecraft:end_rod ~ ~1 ~ 0.3 0.6 0.3 0.005 1'])
    fn('p182/fx_2', halo + ['particle minecraft:end_rod ~ ~1 ~ 0.35 0.7 0.35 0.01 2', 'particle minecraft:wax_on ~ ~1.4 ~ 0.4 0.6 0.4 0 2'])
    fn('p182/fx_3', halo + ['particle minecraft:dust{color:[1.0,0.35,0.2],scale:1.1} ~ ~1.2 ~ 0.3 0.5 0.3 0 2', 'particle minecraft:end_rod ~ ~1 ~ 0.3 0.6 0.3 0.01 1'])
    fn('p182/fx_5', halo + ['particle minecraft:wax_on ~ ~1 ~ 0.4 0.6 0.4 0 2'])
    fn('p182/fast', [f'execute if score @s bm.rgt matches {t} run function bm:p182/fx_{t}' for t in (0, 1, 2, 3, 5)] + ['function bm:p2/rg/gesture'])

    # ================================================================== THE CROWNS: their gift by day (and on a Blood Moon), and their light
    cs = G.FUNCS['p131/crown/sec']
    k = next(i for i, l in enumerate(cs) if 'function bm:p131/crown/night' in l)
    cs[k] = 'execute unless items entity @s armor.head ' + ANGEL + ' unless score #tod bm.bm matches 0..12999 run function bm:p131/crown/night'
    cs.insert(k + 1, 'execute if items entity @s armor.head ' + ANGEL + ' run function bm:p182/crown')
    fn('p182/crown', ['execute if score #tod bm.bm matches 0..12999 run function bm:p131/crown/night',
                      'execute if score #active bm.bm matches 1 run function bm:p131/crown/night'] + halo)
    G.FUNCS['p131/crown/glow'].insert(0, f'execute if items entity @s contents {ANGEL} run return run function bm:p182/crown_glow')
    bob = lambda y: f'data merge entity @s {{start_interpolation:0,interpolation_duration:20,transformation:{{translation:[0f,{y}f,0f]}}}}'
    fn('p182/crown_glow', ['scoreboard players add @s bm.apt 1', 'tp @s ~ ~ ~ ~4 ~',
                           'particle minecraft:dust{color:[1.0,0.92,0.55],scale:0.6} ~ ~0.45 ~ 0.22 0.14 0.22 0 2',
                           'execute store result score #r bm.rng run random value 0..5',
                           'execute if score #r bm.rng matches 0..2 run particle minecraft:end_rod ~ ~0.75 ~ 0.18 0.1 0.18 0.01 1',
                           'execute if score #r bm.rng matches 3 run particle minecraft:wax_on ~ ~0.6 ~ 0.25 0.1 0.25 0 2',
                           'execute if score #r bm.rng matches 4 run particle minecraft:totem_of_undying ~ ~0.6 ~ 0.15 0.1 0.15 0.05 1',
                           'scoreboard players operation #f bm.rng = @s bm.apt', 'scoreboard players operation #f bm.rng %= #8 bm.rng',
                           'execute if score #f bm.rng matches 0 run ' + bob(0.14), 'execute if score #f bm.rng matches 4 run ' + bob(0.03),
                           'execute if score #f bm.rng matches 0 if score #r bm.rng matches 0..2 run playsound minecraft:block.amethyst_block.chime block @a[distance=..10] ~ ~ ~ 0.5 1.6'])

    # ================================================================== operators
    fn('admin/angelic', [give(i) for i in IDS] + [give('golden_cross', 16)])
    if 'admin/help' in G.FUNCS:
        G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/angelic', 'yellow'), T('  the Regalia, its tools, the crowns and 16 Golden Crosses', 'gray')]))
    print(f'2.85b: {len(IDS)} things can be purified')


# ================================================================== THE ART: white and gold
LO, HI = (206, 160, 62), (255, 255, 250)


def _recolor(im, lo=LO, hi=HI, stretch=2.4):
    from PIL import Image
    out = Image.new('RGBA', im.size, (0, 0, 0, 0)); px, po = im.load(), out.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a == 0: continue
            t = min(1.0, ((0.3 * r + 0.59 * g + 0.11 * b) / 255) * stretch)
            po[x, y] = tuple(int(lo[i] + (hi[i] - lo[i]) * t) for i in range(3)) + (a,)
    return out


def rp(R):
    from PIL import Image
    VAN = '/home/claude/mc263/client/assets/minecraft'

    def post(R2):
        import copy, os
        tex_dir = R2.p('assets', 'bm', 'textures', 'item')
        os.makedirs(tex_dir, exist_ok=True)

        def save(name, im):
            im.save(os.path.join(tex_dir, name + '.png'))
            return f'bm:item/{name}'
        for iid in ids():
            if iid in ('apo_true_crown', 'apo_unbound_crown'): continue
            if iid == 'conq_bow':
                tex = {s: save(f'angel_conq_bow{s}', _recolor(Image.open(f'{VAN}/textures/item/bow{s}.png').convert('RGBA'))) for s in ('', '_pulling_0', '_pulling_1', '_pulling_2')}
                for s, t in tex.items():
                    R2.wj(f'assets/bm/models/item/angel_conq_bow{s}.json', {'parent': f'minecraft:item/bow{s}', 'textures': {'layer0': t}})
                m = lambda s: {'type': 'minecraft:model', 'model': f'bm:item/angel_conq_bow{s}'}
                R2.wj('assets/bm/items/angel_conq_bow.json', {'model': {'type': 'minecraft:condition', 'property': 'minecraft:using_item', 'on_false': m(''),
                                                                         'on_true': {'type': 'minecraft:range_dispatch', 'property': 'minecraft:use_duration', 'scale': 0.05,
                                                                                     'fallback': m('_pulling_0'),
                                                                                     'entries': [{'threshold': 0.65, 'model': m('_pulling_1')}, {'threshold': 0.9, 'model': m('_pulling_2')}]}}})
                continue
            src = f'{VAN}/textures/item/{VANILLA[iid]}.png'
            t = save(f'angel_{iid}', _recolor(Image.open(src).convert('RGBA')))
            parent = 'minecraft:item/generated' if iid in ARMOR else 'minecraft:item/handheld'
            R2.wj(f'assets/bm/models/item/angel_{iid}.json', {'parent': parent, 'textures': {'layer0': t}})
            R2.wj(f'assets/bm/items/angel_{iid}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/angel_{iid}'}})
        # the crowns: their own models, every texture on them turned to white gold
        done, atlas = {}, []

        def holy_tex(ref):
            if ref in done: return done[ref]
            ns, path = ref.split(':', 1) if ':' in ref else ('minecraft', ref)
            src = R2.p('assets', 'bm', 'textures', *path.split('/')) + '.png' if ns == 'bm' else f'{VAN}/textures/{path}.png'
            im = _recolor(Image.open(src).convert('RGBA'), (214, 168, 64), (255, 255, 250), 2.0)
            if im.width != im.height:
                n = max(im.size); im = im.resize((n, n), Image.NEAREST)
            nm = 'angel_' + path.replace('/', '_')
            folder = 'block' if path.startswith(('block/', 'item/')) else 'entity'
            im.save(R2.p('assets', 'bm', 'textures', folder, nm + '.png'))
            done[ref] = f'bm:{folder}/{nm}'
            if folder == 'entity': atlas.append(done[ref])
            return done[ref]
        for iid in ('apo_true_crown', 'apo_unbound_crown'):
            idef = json.load(open(R2.p('assets', 'bm', 'items', ITEMS[iid]['comps']['minecraft:item_model'].split(':', 1)[1] + '.json')))
            m = json.load(open(R2.p('assets', 'bm', 'models', *idef['model']['model'].split(':', 1)[1].split('/')) + '.json'))
            g = copy.deepcopy(m)
            g['textures'] = {t: (holy_tex(v) if not v.startswith('#') else v) for t, v in m.get('textures', {}).items()}
            R2.wj(f'assets/bm/models/item/angel_{iid}.json', g)
            R2.wj(f'assets/bm/items/angel_{iid}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/angel_{iid}'}})
        if atlas:
            ap = R2.p('assets', 'minecraft', 'atlases', 'blocks.json')
            cur = json.load(open(ap)) if os.path.exists(ap) else {'sources': []}
            have = {x.get('resource') for x in cur['sources']}
            cur['sources'] += [{'type': 'minecraft:single', 'resource': r} for r in atlas if r not in have]
            R2.wj('assets/minecraft/atlases/blocks.json', cur)
        # the armour on the body: netherite turned to white, gold in its shadows
        for layer in ('humanoid', 'humanoid_leggings'):
            im = _recolor(Image.open(f'{VAN}/textures/entity/equipment/{layer}/netherite.png').convert('RGBA'), (214, 170, 70), (255, 255, 250), 2.6)
            d = R2.p('assets', 'bm', 'textures', 'entity', 'equipment', layer)
            os.makedirs(d, exist_ok=True)
            im.save(os.path.join(d, 'angelic.png'))
        R2.wj('assets/bm/equipment/angelic.json', {'layers': {'humanoid': [{'texture': 'bm:angelic'}], 'humanoid_leggings': [{'texture': 'bm:angelic'}]}})
    R.POST.append(post)

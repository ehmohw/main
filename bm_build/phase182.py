"""2.85b: HOLY FORGING (2.88: "angelic" renamed Holy; its light and its weapons' effects turned to fire and gleaming light) - the Hollow King's Regalia (2.88: and the Wings of the Damned) and Apophiss's crowns, purified with a Golden Cross.

THE FORGE      toss a piece of the Regalia (the Deathmask, the Ribcage, the Greaves, the Treads), one of the King's tools (the
               Soulreaver, the Gravedigger's Maw, the Headsman's Grief, the Barrow Spade, the Witherstring), Sepulchre, or
               Apophiss's True or Unbound Crown down beside a Golden Cross. Light gathers for four seconds and the thing comes up
               ANGELIC: pearl white, royal purple and blue, with gold, the same item - its enchantments, Dread tunings and infusions kept - with no more power
               than before. The cross is spent.
WHAT CHANGES   the look (pearl, royal purple and blue, gold grips and gems of sapphire and amethyst; the armour's trims turn gold), the light round it (a halo, motes of sun, feathers of
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

HOLY, HOLY_D = '#e8e4ff', '#9a7aff'          # (2.85d: pearl and royal purple - no more washed-out yellow)
ROYAL = '#5a7cff'
ANGEL_IDS = ['conq_helmet', 'conq_chestplate', 'conq_leggings', 'conq_boots', 'conq_blade', 'conq_pick', 'conq_axe', 'conq_shovel',
             'conq_hoe', 'conq_bow', 'sepulchre', 'apo_true_crown', 'apo_unbound_crown', 'hollow_wings']
WINGS = 'hollow_wings'                        # (2.88: the Wings of the Damned purify too - pearl and gold feathers, the same wings)
ARMOR = {'conq_helmet': 'head', 'conq_chestplate': 'chest', 'conq_leggings': 'legs', 'conq_boots': 'feet'}
VANILLA = {'conq_helmet': 'netherite_helmet', 'conq_chestplate': 'netherite_chestplate', 'conq_leggings': 'netherite_leggings',
           'conq_boots': 'netherite_boots', 'conq_blade': 'netherite_sword', 'conq_pick': 'netherite_pickaxe', 'conq_axe': 'netherite_axe',
           'conq_shovel': 'netherite_shovel', 'conq_hoe': 'netherite_hoe', 'conq_bow': 'bow', 'sepulchre': 'mace', 'hollow_wings': 'elytra'}
UP_X, DOWN_X, OWN_ART = {}, {}, set()     # (2.93: a module's own pieces - extra components either way, and art it draws itself)
holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
ANGEL = '*[minecraft:custom_data~{bm_angel:1b}]'
PURE = [T('✦ Holy: it wakes by day, not by night.', HOLY_D), T('  (A Blood Moon still wakes it.)', HOLY_D),
        T('✦ What withered now burns: fire and light.', HOLY_D)]


def ids():
    return [i for i in ANGEL_IDS if i in ITEMS]


HOLY_PART = [('minecraft:soul_fire_flame', 'minecraft:flame'), ('minecraft:sculk_soul', 'minecraft:end_rod'), ('minecraft:large_smoke', 'minecraft:flame'),
             ('minecraft:smoke', 'minecraft:small_flame'), ('minecraft:soul ', 'minecraft:wax_on '), ('minecraft:ash', 'minecraft:end_rod'),
             ('minecraft:squid_ink', 'minecraft:flame'), ('minecraft:crimson_spore', 'minecraft:wax_on')]
HOLY_SOUND = [('entity.wither.shoot', 'entity.blaze.shoot'), ('entity.wither.spawn', 'block.beacon.activate'), ('entity.wither.ambient', 'block.beacon.power_select'),
              ('entity.wither.break_block', 'item.firecharge.use'), ('entity.warden.heartbeat', 'block.bell.resonate')]
HOLY_WORD = [('WITHER NOVA', 'SOLAR NOVA'), ('still gathering death', 'still gathering light'), ('Soul Rend', 'Sun Rend')]


def holy_line(l):
    """a line of a Regalia effect, made holy: souls and smoke to flame and glinting light, dark dust to gold, wither to burning"""
    import re
    for a, b in HOLY_PART + HOLY_SOUND + HOLY_WORD:
        l = l.replace(a, b)
    def gold(m):
        r, g, b = (float(v) for v in m.group(1).split(','))
        return m.group(0) if r + g + b > 0.9 else m.group(0).replace(m.group(1), '1.0,0.8,0.32')
    l = re.sub(r'dust\{color:\[([\d.]+,[\d.]+,[\d.]+)\]', gold, l)
    l = re.sub(r'effect give @s minecraft:wither (\d+) \d+', lambda m: f'function bm:p182/burn_{int(m.group(1))}', l)
    return l


def holy_twins(G):
    """(2.88) Holy, not angelic: the Regalia's own effects (the Wither Nova, Sepulchre's quake), the Hollow tools' (the dig, the felling,
    the Soul Rend, the arrows), and the Wings of the Damned's trail, each with a holy twin - the same thing in fire and gleaming light,
    and what withered burns. A root runs its twin when what it comes from is holy; everything it calls is twinned with it."""
    import re
    F, fn = G.FUNCS, G.fn
    holy_wings = '*[minecraft:custom_data~{bm:"hollow_wings",bm_angel:1b}]'
    ROOTS = {'p2/rg/gesture': 'if function bm:p182/is_angel', 'p2/rg/mace_use': 'if function bm:p182/is_angel',
             'p2/rg/smash': 'if function bm:p182/is_angel', 'p2/rg/kill': 'if entity @s[tag=bm.angel]',
             'p2/ht/pick': f'if items entity @s weapon.mainhand {ANGEL}', 'p2/ht/shovel': f'if items entity @s weapon.mainhand {ANGEL}',
             'p2/ht/axe': f'if items entity @s weapon.mainhand {ANGEL}', 'p2/ht/hoe': f'if items entity @s weapon.mainhand {ANGEL}',
             'p2/ht/blade': f'if items entity @s weapon.mainhand {ANGEL}', 'p2/ht/arrow_fx': 'if entity @s[tag=bm.harrow]',
             'p2/ht/wings': f'if items entity @s armor.chest {holy_wings}', 'p2/ht/burn': f'if items entity @s armor.chest {holy_wings}'}
    ref = re.compile(r'function bm:(p2/(?:rg|ht)/[\w/]+)')
    memo = {}
    def lit(f, seen=()):                        # (does it, or anything it calls, show or do something to make holy)
        if f in memo: return memo[f]
        if f not in F or f in seen: return False
        own = any('particle ' in l or 'minecraft:wither' in l or 'playsound minecraft:entity.wither' in l for l in F[f])
        memo[f] = own or any(lit(g, seen + (f,)) for l in F[f] for g in ref.findall(l))
        return memo[f]
    twins = set()
    def twin(f):
        if f in twins: return
        twins.add(f)
        for l in F[f]:
            for g in ref.findall(l):
                if lit(g): twin(g)
    for r in ROOTS:
        assert r in F, r
        twin(r)
    for f in sorted(twins):
        body = [holy_line(l) for l in F[f]]
        body = [ref.sub(lambda m: f'function bm:{m.group(1)}_holy' if m.group(1) in twins else m.group(0), l) for l in body]
        fn(f'{f}_holy', body)
    for r, cond in ROOTS.items():
        F[r].insert(0, f'execute {cond} run return run function bm:{r}_holy')
    # what withered burns (a mob set alight; anyone lit up), for as long as the wither would have lasted
    for n in sorted({int(m) for f in twins for l in F[f] for m in re.findall(r'effect give @s minecraft:wither (\d+)', l)}):
        fn(f'p182/burn_{n}', [f'execute unless entity @s[type=minecraft:player] run data merge entity @s {{Fire:{n * 20}s}}',
                              f'effect give @s minecraft:glowing {n} 0 true', 'particle minecraft:flame ~ ~1 ~ 0.3 0.5 0.3 0.02 6'])
    # the holy bow's arrows: marked at the string, so their trail is light
    F['p2/ht/arrow'] += ['execute store success score #hb bm.rng on origin if items entity @s weapon.* *[minecraft:custom_data~{bm:"conq_bow",bm_angel:1b}]',
                         'execute if score #hb bm.rng matches 1 run tag @s add bm.harrow']
    G.wjson('bm/enchantment/p182/searing_shot.json', {
        'description': {'text': 'Searing Shot', 'color': '#ffc84a'}, 'anvil_cost': 8, 'max_level': 1, 'weight': 1, 'slots': ['mainhand'],
        'min_cost': {'base': 1, 'per_level_above_first': 0}, 'max_cost': {'base': 1, 'per_level_above_first': 0},
        'supported_items': '#minecraft:enchantable/bow',
        'effects': {'minecraft:projectile_spawned': [{'effect': {'type': 'minecraft:run_function', 'function': 'bm:p2/ht/arrow'}}],
                    'minecraft:post_attack': [{'affected': 'victim', 'enchanted': 'attacker', 'effect': {'type': 'minecraft:ignite', 'duration': 6.0}}]}})
    return len(twins)


def angel_name(iid):
    return {'text': '', 'italic': False, 'extra': [{'text': '✦ ', 'color': HOLY_D}, {'text': 'Holy ', 'color': ROYAL, 'bold': True}, {'text': ITEMS[iid]['name'], 'color': HOLY, 'bold': True},
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
        if iid == WINGS:                                   # (on your back: the angelic wings, or the elytra's own again)
            up['minecraft:equippable'] = {'slot': 'chest', 'asset_id': 'bm:angelic_wings', 'equip_sound': 'minecraft:item.armor.equip_elytra', 'damage_on_hurt': False}
            down['minecraft:equippable'] = {'slot': 'chest', 'asset_id': 'minecraft:elytra', 'equip_sound': 'minecraft:item.armor.equip_elytra', 'damage_on_hurt': False}
        up.update(UP_X.get(iid, {})); down.update(DOWN_X.get(iid, {}))
        up, down = ({k: v for k, v in d.items() if v is not None} for d in (up, down))     # (None: that component isn't set at all)
        bow_up = [{'function': 'minecraft:set_enchantments', 'enchantments': {'bm:withering_shot': 0, 'bm:p182/searing_shot': 1}}] if iid == 'conq_bow' else []
        bow_down = [{'function': 'minecraft:set_enchantments', 'enchantments': {'bm:p182/searing_shot': 0, 'bm:withering_shot': 1}}] if iid == 'conq_bow' else []
        wjson(f'bm/item_modifier/p182/up_{iid}.json', bow_up + [{'function': 'minecraft:set_custom_data', 'tag': '{bm_angel:1b}'},
                                                       {'function': 'minecraft:set_components', 'components': up},
                                                       {'function': 'minecraft:set_lore', 'mode': 'insert', 'offset': 0, 'lore': PURE}])
        wjson(f'bm/item_modifier/p182/down_{iid}.json', bow_down + [{'function': 'minecraft:set_custom_data', 'tag': '{bm_angel:0b}'},
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
                       'particle minecraft:flame ~ ~0.4 ~ 0.4 0.2 0.4 0.02 8', 'particle minecraft:small_flame ~ ~1.2 ~ 0.3 0.6 0.3 0.01 6',
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
                       'execute as @a[distance=..12] run ' + title('@s', 'actionbar', T('It comes up in pearl, purple and gold - holy.', HOLY, bold=True))])
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
    wings_corrupt = f'*[minecraft:custom_data~{{bm:"{WINGS}"}},!minecraft:custom_data~{{bm_angel:1b}}]'
    k = next(i for i, l in enumerate(second) if 'function bm:p2/rg/second' in l)
    second[k:k] = ['execute as @a[tag=bm.angel] unless items entity @s armor.* ' + some + ' run function bm:p182/unangel',
                   'execute as @a[gamemode=!spectator] if items entity @s armor.* ' + some + ' run function bm:p182/angel_tag']
    fn('p182/angel_tag', ['scoreboard players set #an bm.rng 0',
                          f'execute if items entity @s armor.* {ANGEL} unless items entity @s armor.* {corrupt} unless items entity @s armor.chest {wings_corrupt} run scoreboard players set #an bm.rng 1',
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
        # (2.94: never on a piece with its own art - the Seraph's: a trim has no texture for its own equipment, and by day the
        #  carapace's wings and the plate showed the missing-texture checks)
        own = ''.join(f' unless items entity @s {{sl}} *[minecraft:custom_data~{{{{bm:"{i}"}}}}]' for i in sorted(OWN_ART))
        fn(f'p182/wake_{t}', [f'execute if items entity @s {sl} {ANGEL}{own.format(sl=sl)} run item modify entity @s {sl} {{function:"minecraft:set_components",components:{comps}}}'
                              for sl in slots.values()] + [title('@s', 'actionbar', T(msg, col, italic=True))])
    # (2.94: and a trim already put on one - before this fix - taken off again)
    unt = [f'execute if items entity @s {sl} *[minecraft:custom_data~{{bm:"{i}"}},minecraft:trim] run item modify entity @s {sl} '
           '{function:"minecraft:set_components",components:{"!minecraft:trim":{}}}' for sl in slots.values() for i in sorted(OWN_ART)]
    fn('p182/wake', unt + [f'execute if score #rg bm.rng matches {t} run function bm:p182/wake_{t}' for t in msgs] +
       ['scoreboard players operation @s bm.rgt = #rg bm.rng',
        'execute if score #rg bm.rng matches 1.. run playsound minecraft:block.beacon.power_select player @s ~ ~ ~ 0.5 1.6',
        'execute if score #rg bm.rng matches 1.. run particle minecraft:end_rod ~ ~1 ~ 0.4 0.8 0.4 0.03 20'])
    G.FUNCS['p2/rg/fast'].insert(0, 'execute if entity @s[tag=bm.angel] run return run function bm:p182/fast')
    halo = [f'particle {("minecraft:small_flame", "minecraft:end_rod")[i % 2]} ~{0.3 * math.cos(2 * math.pi * i / 8):.2f} ~2.3 ~{0.3 * math.sin(2 * math.pi * i / 8):.2f} 0 0 0 0 1'
            for i in range(8)]     # (2.88: a halo of fire and light - little flames between glints)
    fn('p182/fx_0', ['particle minecraft:end_rod ~ ~1.2 ~ 0.3 0.5 0.3 0.002 1'])
    fn('p182/fx_1', halo + ['particle minecraft:flame ~ ~0.5 ~ 0.3 0.3 0.3 0.005 1'])
    fn('p182/fx_2', halo + ['particle minecraft:flame ~ ~0.6 ~ 0.35 0.4 0.35 0.01 2', 'particle minecraft:end_rod ~ ~1 ~ 0.35 0.7 0.35 0.01 2',
                            'particle minecraft:wax_on ~ ~1.4 ~ 0.4 0.6 0.4 0 2'])
    fn('p182/fx_3', halo + ['particle minecraft:flame ~ ~1 ~ 0.3 0.5 0.3 0.02 3', 'particle minecraft:lava ~ ~1.2 ~ 0.3 0.4 0.3 0 1'])
    fn('p182/fx_5', halo + ['particle minecraft:wax_on ~ ~1 ~ 0.4 0.6 0.4 0 2', 'particle minecraft:small_flame ~ ~0.6 ~ 0.3 0.3 0.3 0.005 1'])
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
                           'particle minecraft:small_flame ~ ~0.45 ~ 0.2 0.12 0.2 0.003 1',
                           'execute store result score #r bm.rng run random value 0..5',
                           'execute if score #r bm.rng matches 0..2 run particle minecraft:end_rod ~ ~0.75 ~ 0.18 0.1 0.18 0.01 1',
                           'execute if score #r bm.rng matches 3 run particle minecraft:wax_on ~ ~0.6 ~ 0.25 0.1 0.25 0 2',
                           'execute if score #r bm.rng matches 4 run particle minecraft:totem_of_undying ~ ~0.6 ~ 0.15 0.1 0.15 0.05 1',
                           'scoreboard players operation #f bm.rng = @s bm.apt', 'scoreboard players operation #f bm.rng %= #8 bm.rng',
                           'execute if score #f bm.rng matches 0 run ' + bob(0.14), 'execute if score #f bm.rng matches 4 run ' + bob(0.03),
                           'execute if score #f bm.rng matches 0 if score #r bm.rng matches 0..2 run playsound minecraft:block.amethyst_block.chime block @a[distance=..10] ~ ~ ~ 0.5 1.6'])

    holy_twins(G)

    # ================================================================== operators
    fn('admin/angelic', [give(i) for i in IDS] + [give('golden_cross', 16)])
    if 'admin/help' in G.FUNCS:
        G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/angelic', 'yellow'), T('  the Regalia, its tools, the wings, the crowns and 16 Golden Crosses (to make holy)', 'gray')]))
    print(f'2.85b: {len(IDS)} things can be purified')


# ================================================================== THE ART: pearl, royal purple and blue, gold
# (2.85d: the owner found the white-gold washed out and yellow - now metal runs from royal blue in its shadows through a
#  royal purple to pearl white, wood and grips turn to rich gold, and gems to sapphire and amethyst)
MAIN = [(0.0, (16, 18, 64)), (0.25, (38, 58, 168)), (0.45, (104, 70, 200)), (0.66, (196, 180, 240)), (0.85, (244, 240, 255)), (1.0, (255, 255, 255))]
GOLD = [(0.0, (92, 52, 14)), (0.45, (196, 138, 36)), (0.75, (240, 196, 74)), (1.0, (255, 236, 150))]
SAPPHIRE = [(0.0, (14, 26, 96)), (0.5, (52, 104, 228)), (1.0, (176, 212, 255))]
AMETHYST = [(0.0, (48, 14, 92)), (0.5, (146, 76, 222)), (1.0, (230, 196, 255))]


def _ramp(stops, t):
    t = max(0.0, min(1.0, t))
    for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
        if t <= t1:
            k = (t - t0) / (t1 - t0) if t1 > t0 else 0
            return tuple(int(c0[i] + (c1[i] - c0[i]) * k) for i in range(3))
    return stops[-1][1]


def _recolor(im, lift=0.18):
    """holy colours by what each pixel was: plain metal or stone by its brightness (stretched over the picture's own range),
    wood and grips to gold, green and cyan gems to sapphire, purple, blue and red ones to amethyst"""
    import colorsys
    from PIL import Image
    px = im.load()
    lum = sorted(0.3 * r + 0.59 * g + 0.11 * b for (r, g, b, a) in im.getdata() if a)
    if not lum: return im.copy()
    lo, hi = lum[len(lum) // 20], lum[-1 - len(lum) // 20]
    hi = max(hi, lo + 1)
    out = Image.new('RGBA', im.size, (0, 0, 0, 0)); po = out.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a == 0: continue
            h, sat, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            hue = h * 360
            if (hue <= 60 or hue >= 300) and sat > 0.35 and v > 0.22:
                c = _ramp(GOLD, 0.2 + v * 1.25)                            # (grips, staves, the bow's wood, red jewels: gold)
            elif sat > 0.35 and v > 0.18:
                if 15 <= hue <= 60: c = _ramp(GOLD, v * 1.1)
                elif 60 < hue <= 200: c = _ramp(SAPPHIRE, v)
                else: c = _ramp(AMETHYST, v)
            else:
                t = max(0.0, min(1.0, ((0.3 * r + 0.59 * g + 0.11 * b) - lo) / (hi - lo)))
                c = _ramp(MAIN, lift + (1 - lift) * t ** 0.5)           # (lifted: mostly pearl, the purple and blue down in its shadows)
            po[x, y] = c + (a,)
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
            if iid in ('apo_true_crown', 'apo_unbound_crown') or iid in OWN_ART: continue
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
            parent = 'minecraft:item/generated' if iid in ARMOR or iid == WINGS else 'minecraft:item/handheld'
            R2.wj(f'assets/bm/models/item/angel_{iid}.json', {'parent': parent, 'textures': {'layer0': t}})
            R2.wj(f'assets/bm/items/angel_{iid}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/angel_{iid}'}})
        # the crowns: their own models, every texture on them turned to white gold
        done, atlas = {}, []

        def holy_tex(ref):
            if ref in done: return done[ref]
            ns, path = ref.split(':', 1) if ':' in ref else ('minecraft', ref)
            src = R2.p('assets', 'bm', 'textures', *path.split('/')) + '.png' if ns == 'bm' else f'{VAN}/textures/{path}.png'
            im = _recolor(Image.open(src).convert('RGBA'), 0.3)
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
            im = _recolor(Image.open(f'{VAN}/textures/entity/equipment/{layer}/netherite.png').convert('RGBA'), 0.22)
            d = R2.p('assets', 'bm', 'textures', 'entity', 'equipment', layer)
            os.makedirs(d, exist_ok=True)
            im.save(os.path.join(d, 'angelic.png'))
        R2.wj('assets/bm/equipment/angelic.json', {'layers': {'humanoid': [{'texture': 'bm:angelic'}], 'humanoid_leggings': [{'texture': 'bm:angelic'}]}})
        # (2.88) the Wings of the Damned, purified: the elytra's feathers in pearl, purple and gold
        d = R2.p('assets', 'bm', 'textures', 'entity', 'equipment', 'wings')
        os.makedirs(d, exist_ok=True)
        _recolor(Image.open('/home/claude/bm_build/vendor/elytra_wings.png').convert('RGBA'), 0.3).save(os.path.join(d, 'angelic_wings.png'))
        R2.wj('assets/bm/equipment/angelic_wings.json', {'layers': {'wings': [{'texture': 'bm:angelic_wings'}]}})
    R.POST.append(post)

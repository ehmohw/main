"""2.93: THE DREADBORNE - the armour the Dread monsters wear, won from the three Dread bosses (and its holy twin, the Seraph's
Raiment, from a Golden Cross).

  THE DREAD VISAGE   (the Malevolent Snowbeast's)  the Dread's own horned, many-eyed helm. Worn: night vision; Darkness and
                     Blindness can't take you.  FROSTBITE: one blow in four freezes the thing you hit - 6 more, slowed.
  THE DREAD GREAVES  (the Watchful Witch's)  Poison and Wither can't take you.  HEX: one blow in four - 5 more through its armour,
                     weakened, withering.
  THE DREAD TREADS   (the Chomping Sawshark's)  no fall damage; Dolphin's Grace in water.  FRENZY: one blow in four - 5 more,
                     and Strength for you.
  THE DREAD CARAPACE (beat all three)  the fourth piece: each player who has beaten all three bosses is given a DREAD HEART;
                     dropped on the ground beside a netherite chestplate and an elytra, it forges them into the Carapace - plate
                     and wings in one (it glides). +4 health; at low health, Resistance II (once a minute).  LEECH: one blow in
                     four heals you 3.
  DREAD RENDING      the whole set: sneak and strike - 24 through every armour to the thing you hit, 8 to every monster round
                     it, and it withers. Then 45 s to gather again.
  THE SERAPH'S RAIMENT  each piece made holy at a Golden Cross (phase182): the same powers in fire and light; the Visage becomes
                     the Seraph's Gaze (two wings over its face, eyes, a burning halo), the Carapace the Seraph's Wings, the
                     Treads feathered over the feet.  SERAPHIC JUDGMENT (the whole holy set): sneak and strike - a pillar of holy
                     fire, 24 through every armour (and 10 more to the undead), 8 to every monster round, alight; you healed.
                     45 s. (One holy piece and three dread ones is neither set.)"""
import math
from items import item, T, ITEMS, attr
import phase182 as P182

RED, HOLY, HOLY_D, ROYAL = '#d0182e', '#e8e4ff', '#9a7aff', '#5a7cff'
CD = 45
UNBR = {'minecraft:unbreakable': {}}
holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
ANGEL = '*[minecraft:custom_data~{bm_angel:1b}]'
PIECES = {  # iid: (base, slot, armour, name, holy name, asset, boss)
    'dread_visage': ('netherite_helmet', 'head', 4, 'Dread Visage', "Seraph's Gaze", None, 'snow'),
    'dread_carapace': ('netherite_chestplate', 'chest', 9, 'Dread Carapace', "Seraph's Wings", 'bm:dread_carapace', None),
    'dread_greaves': ('netherite_leggings', 'legs', 7, 'Dread Greaves', "Seraph's Greaves", 'bm:dread', 'witch'),
    'dread_treads': ('netherite_boots', 'feet', 4, 'Dread Treads', "Seraph's Treads", 'bm:dread', 'shark'),
}
SLOT = {'head': 'armor.head', 'chest': 'armor.chest', 'legs': 'armor.legs', 'feet': 'armor.feet'}
LORE = {
    'dread_visage': [('The Dread\'s own helm, horned and many-eyed.', 'gray'), ('Worn: night vision; Darkness and', 'blue'), ('Blindness can\'t take you.', 'blue'),
                     ('FROSTBITE: one blow in four freezes', 'aqua'), ('the thing you hit (6 more, slowed).', 'aqua')],
    'dread_carapace': [('Void-plate and black wings in one.', 'gray'), ('It glides. +4 health; at low health,', 'blue'), ('Resistance II (once a minute).', 'blue'),
                       ('LEECH: one blow in four heals you 3.', 'aqua')],
    'dread_greaves': [('Cracked void-plate, bone at the knee.', 'gray'), ('Worn: Poison and Wither can\'t take you.', 'blue'),
                      ('HEX: one blow in four - 5 more through', 'aqua'), ('its armour, weakened and withering.', 'aqua')],
    'dread_treads': [('Clawed boots of the deep Dread.', 'gray'), ('Worn: no fall damage; Dolphin\'s Grace.', 'blue'),
                     ('FRENZY: one blow in four - 5 more,', 'aqua'), ('and Strength for you.', 'aqua')],
}
SET_LORE = [('THE SET - DREAD RENDING: sneak and strike:', RED), ('24 through every armour, 8 round it (45 s).', RED),
            ('A Golden Cross makes it holy: the Seraph.', '#9a7aff')]

for _iid, (_base, _slot, _arm, _nm, _hn, _asset, _boss) in PIECES.items():
    eq = {'slot': _slot, 'equip_sound': 'minecraft:item.armor.equip_netherite'}
    if _asset: eq['asset_id'] = _asset
    mods = [attr('armor', _arm, _slot, ident=f'bm:{_iid}_armor'), attr('armor_toughness', 3, _slot, ident=f'bm:{_iid}_tough'),
            attr('knockback_resistance', 0.1, _slot, ident=f'bm:{_iid}_kb')]
    if _iid == 'dread_carapace': mods.append(attr('max_health', 4, _slot, ident='bm:dread_carapace_hp'))
    if _iid == 'dread_treads': mods.append(attr('fall_damage_multiplier', -1, _slot, op='add_multiplied_total', ident='bm:dread_treads_fall'))
    comps = dict(UNBR, **{'minecraft:item_model': 'bm:dread_helm' if _iid == 'dread_visage' else f'bm:{_iid}',
                          'minecraft:equippable': eq, 'minecraft:attribute_modifiers': mods})
    if _iid == 'dread_carapace': comps['minecraft:glider'] = {}
    item(_iid, f'minecraft:{_base}', _nm, RED, LORE[_iid] + SET_LORE + ([('Won from the ' + {'snow': 'Malevolent Snowbeast', 'witch': 'Watchful Witch',
                                                                                         'shark': 'Chomping Sawshark'}[_boss] + '.', 'dark_gray')] if _boss else
                                                                     [('Forged from a Dread Heart, a netherite chestplate', 'dark_gray'), ('and an elytra.', 'dark_gray')]),
         stack=1, cat='armor', tier=3, bold=True, comps=comps)
item('dread_heart', 'minecraft:paper', 'Dread Heart', RED,
     ['What the three Dread bosses had in common.', ('Drop it on the ground beside a netherite', 'yellow'), ('chestplate and an elytra: the Dread Carapace.', 'yellow')],
     model='bm:dread_heart', stack=1, cat='misc', tier=3)

# the holy twin, by the Golden Cross: phase182's forge, with these pieces' own looks
for _iid, (_base, _slot, _arm, _nm, _hn, _asset, _boss) in PIECES.items():
    P182.ANGEL_IDS.append(_iid)
    P182.ARMOR[_iid] = _slot
    P182.VANILLA[_iid] = _base
    P182.OWN_ART.add(_iid)
    holy_eq = {'slot': _slot, 'equip_sound': 'minecraft:item.armor.equip_gold'}
    if _slot != 'head': holy_eq['asset_id'] = 'bm:seraph_wings' if _iid == 'dread_carapace' else 'bm:seraph'
    P182.UP_X[_iid] = {'minecraft:item_name': {'text': '', 'italic': False, 'extra': [{'text': '✦ ', 'color': HOLY_D}, {'text': _hn, 'color': HOLY, 'bold': True},
                                                                                       {'text': ' ✦', 'color': HOLY_D}]},
                       'minecraft:equippable': holy_eq, 'minecraft:trim': None}
    P182.DOWN_X[_iid] = {'minecraft:trim': None}


def generate(G):
    fn, title, tellraw, give, P = G.fn, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    second = G.FUNCS['loop/second']
    objs = ['bm.dscd', 'bm.dcres']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    # its own damage: through armour (the strikes) and never lost to a blow struck the same moment (strikes and procs alike)
    import json, os
    DT = {'dread_rend': ('bypasses_armor', 'bypasses_enchantments', 'bypasses_shield', 'bypasses_cooldown'),
          'seraph_fire': ('bypasses_armor', 'bypasses_enchantments', 'bypasses_shield', 'bypasses_cooldown'),
          'dread_proc': ('bypasses_cooldown',), 'dread_hex': ('bypasses_armor', 'bypasses_cooldown')}
    for dt, tags in DT.items():
        G.wjson(f'bm/damage_type/{dt}.json', {'exhaustion': 0.0, 'message_id': f'bm.{dt}', 'scaling': 'never', 'effects': 'hurt'})
    for tg in sorted({t for ts in DT.values() for t in ts}):
        f_ = G.path('data', 'minecraft', 'tags', 'damage_type', f'{tg}.json')
        vals = json.load(open(f_))['values'] if os.path.exists(f_) else []
        add = [f'bm:{dt}' for dt, ts in DT.items() if tg in ts]
        G.wjson(f'minecraft/tags/damage_type/{tg}.json', {'replace': False, 'values': [v for v in vals if v not in add] + add})
    wear = lambda iid: f'items entity @s {SLOT[PIECES[iid][1]]} {holds(iid)}'

    # ---------------------------------------------------------------- the bosses' pieces, the Dread Heart
    for iid, (*_r, boss) in PIECES.items():
        if boss:
            G.FUNCS[f'p197/{boss}/reward'] += [give(iid), tellraw('@s', [T('  + ', 'gray'), T(PIECES[iid][3], RED, bold=True),
                                                                       T(' - a piece of what the Dread wear.', 'gray')])]
    beat_all = '@a[tag=!bm.dheart,scores={bm.dbwin_snow=1..,bm.dbwin_witch=1..,bm.dbwin_shark=1..}]'
    second.append(f'execute as {beat_all} at @s run function bm:p206/heart')
    fn('p206/heart', ['tag @s add bm.dheart', give('dread_heart'),
                      tellraw('@s', P + [T('All three Dread bosses have fallen to you. ', RED, bold=True), T('Their hearts beat as one: a ', 'gray'),
                                         T('Dread Heart', RED, bold=True), T(' - drop it beside a netherite chestplate and an elytra.', 'gray')]),
                      'playsound minecraft:entity.warden.heartbeat player @s ~ ~ ~ 1 0.6'])
    # the forge: on the ground, the three together
    plate, wings = 'minecraft:netherite_chestplate[!minecraft:custom_data]', 'minecraft:elytra[!minecraft:custom_data]'
    second.append(f'execute as @e[type=minecraft:item] if items entity @s contents {holds("dread_heart")} at @s '
                  f'if entity @e[type=minecraft:item,distance=..2.5,nbt={{Item:{{id:"minecraft:netherite_chestplate"}}}}] run function bm:p206/forge')
    fn('p206/forge', ['scoreboard players set #fp bm.rng 0', 'scoreboard players set #fw bm.rng 0',
                      f'execute as @e[type=minecraft:item,distance=..2.5] if items entity @s contents {plate} run scoreboard players set #fp bm.rng 1',
                      f'execute as @e[type=minecraft:item,distance=..2.5] if items entity @s contents {wings} run scoreboard players set #fw bm.rng 1',
                      'execute unless score #fp bm.rng matches 1 run return 0', 'execute unless score #fw bm.rng matches 1 run return 0',
                      f'execute as @e[type=minecraft:item,distance=..2.5,limit=1] if items entity @s contents {plate} run function bm:p206/spend',
                      f'execute as @e[type=minecraft:item,distance=..2.5,limit=1] if items entity @s contents {wings} run function bm:p206/spend',
                      'function bm:p206/spend', 'loot spawn ~ ~0.4 ~ loot bm:items/dread_carapace',
                      'particle minecraft:squid_ink ~ ~0.6 ~ 0.4 0.4 0.4 0.08 40', 'particle minecraft:dust{color:[0.82,0.1,0.18],scale:1.8} ~ ~0.8 ~ 0.6 0.6 0.6 0 40',
                      'particle minecraft:sculk_soul ~ ~0.8 ~ 0.5 0.5 0.5 0.03 20',
                      'playsound minecraft:entity.warden.emerge block @a[distance=..16] ~ ~ ~ 0.8 1.2', 'playsound minecraft:block.anvil.use block @a[distance=..16] ~ ~ ~ 1 0.5',
                      'execute as @a[distance=..12] run ' + title('@s', 'actionbar', T('The heart beats into the plate - wings unfold from it: the Dread Carapace.', RED, bold=True))])
    fn('p206/spend', ['execute store result score #n bm.rng run data get entity @s Item.count',
                      'execute if score #n bm.rng matches ..1 run return run kill @s',
                      'item modify entity @s contents {function:"minecraft:set_count",count:-1,add:true}'])

    # ---------------------------------------------------------------- worn: the passives (each second)
    second.append('execute as @a[gamemode=!spectator] at @s run function bm:p206/sec')
    fn('p206/sec', ['execute if score @s bm.dscd matches 1.. run scoreboard players remove @s bm.dscd 1',
                    'execute if score @s bm.dscd matches 1 run function bm:p206/ready',
                    'execute if score @s bm.dcres matches 1.. run scoreboard players remove @s bm.dcres 1',
                    f'execute if {wear("dread_visage")} run function bm:p206/w/visage',
                    f'execute if {wear("dread_carapace")} run function bm:p206/w/carapace',
                    f'execute if {wear("dread_greaves")} run function bm:p206/w/greaves',
                    f'execute if {wear("dread_treads")} run function bm:p206/w/treads'])
    fn('p206/ready', ['execute if function bm:p206/holy_set run return run ' + say('Seraphic Judgment is ready.', HOLY),
                      'execute if function bm:p206/dread_set run ' + say('Dread Rending is ready.', RED)])
    fn('p206/w/visage', ['effect give @s minecraft:night_vision 16 0 true', 'effect clear @s minecraft:darkness', 'effect clear @s minecraft:blindness'])
    fn('p206/w/carapace', ['execute if score @s bm.dcres matches 1.. run return 0', 'execute store result score #hp bm.rng run data get entity @s Health',
                           'execute unless score #hp bm.rng matches ..7 run return 0', 'scoreboard players set @s bm.dcres 60',
                           'effect give @s minecraft:resistance 6 1', 'particle minecraft:squid_ink ~ ~1 ~ 0.4 0.6 0.4 0.03 20',
                           'playsound minecraft:item.armor.equip_netherite player @s ~ ~ ~ 1 0.6', say('The Carapace closes round you.', RED)])
    fn('p206/w/greaves', ['effect clear @s minecraft:poison', 'effect clear @s minecraft:wither'])
    fn('p206/w/treads', ['execute if block ~ ~1 ~ minecraft:water run effect give @s minecraft:dolphins_grace 3 0 true'])
    # (2.94) THEIR AURAS - each set worn whole shows it: the Dread, crimson motes and drifting souls round you; the Seraph,
    # gold light and white glints, and a ring of light at your crown. Gliding in the carapace leaves a trail of its own.
    G.FUNCS['loop/fast'][-1:-1] = [f'execute as @a[gamemode=!spectator] if {wear("dread_carapace")} at @s run function bm:p206/aura']
    G.wjson('bm/predicate/p206/gliding.json', {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:flags': {'is_fall_flying': True}}})
    fn('p206/aura', ['execute if predicate bm:p206/gliding run return run function bm:p206/aura_glide',
                     'execute if function bm:p206/holy_set run return run function bm:p206/aura_holy',
                     'execute if function bm:p206/dread_set run function bm:p206/aura_dread'])
    fn('p206/aura_dread', ['particle minecraft:dust{color:[0.72,0.06,0.14],scale:0.9} ~ ~1.1 ~ 0.35 0.6 0.35 0 3',
                           'particle minecraft:dust{color:[0.15,0.02,0.05],scale:1.3} ~ ~0.3 ~ 0.4 0.15 0.4 0 2',
                           'particle minecraft:sculk_soul ~ ~1.6 ~ 0.3 0.3 0.3 0.01 1'])
    fn('p206/aura_holy', ['particle minecraft:dust{color:[1.0,0.86,0.42],scale:0.8} ~ ~1.1 ~ 0.35 0.6 0.35 0 3',
                          'particle minecraft:end_rod ~ ~1.3 ~ 0.3 0.5 0.3 0.005 1', 'particle minecraft:wax_off ~ ~1.8 ~ 0.4 0.3 0.4 0 1'] +
       [f'particle minecraft:dust{{color:[1.0,0.95,0.7],scale:0.5}} ^{0.3 * math.cos(2 * math.pi * i / 6):.2f} ^2.25 ^{0.3 * math.sin(2 * math.pi * i / 6):.2f} 0 0 0 0 1' for i in range(6)])
    fn('p206/aura_glide_holy', ['particle minecraft:end_rod ^0.5 ^0.6 ^-0.6 0.1 0.1 0.1 0.01 2', 'particle minecraft:end_rod ^-0.5 ^0.6 ^-0.6 0.1 0.1 0.1 0.01 2',
                                'particle minecraft:dust{color:[1.0,0.86,0.42],scale:1.0} ^ ^0.6 ^-0.8 0.2 0.1 0.2 0 3'])
    fn('p206/aura_glide', [f'execute if items entity @s armor.chest {ANGEL} run return run function bm:p206/aura_glide_holy',
                           'particle minecraft:dust{color:[0.72,0.06,0.14],scale:1.1} ^0.5 ^0.6 ^-0.6 0.1 0.1 0.1 0 3',
                           'particle minecraft:dust{color:[0.72,0.06,0.14],scale:1.1} ^-0.5 ^0.6 ^-0.6 0.1 0.1 0.1 0 3',
                           'particle minecraft:squid_ink ^ ^0.6 ^-0.8 0.1 0.1 0.1 0.01 1'])
    # the sets: all four pieces, every one holy or none
    fn('p206/dread_set', [f'execute unless {wear(i)} run return 0' for i in PIECES] + [f'execute if items entity @s armor.* {ANGEL} run return 0', 'return 1'])
    fn('p206/holy_set', [f'execute unless {wear(i)} run return 0' for i in PIECES] +
       [f'execute unless items entity @s {SLOT[PIECES[i][1]]} {ANGEL} run return 0' for i in PIECES] + ['return 1'])

    # ---------------------------------------------------------------- a blow struck in it: the procs, and the set's strike
    pred = [{'condition': 'minecraft:any_of', 'terms': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'equipment': {k: {'predicates': {'minecraft:custom_data': f'{{bm:"{i}"}}'}}}}}
        for i, k in (('dread_visage', 'head'), ('dread_carapace', 'chest'), ('dread_greaves', 'legs'), ('dread_treads', 'feet'))]}]
    G.wjson('bm/advancement/p206/hit.json', {'criteria': {'hit': {'trigger': 'minecraft:player_hurt_entity', 'conditions': {'player': pred}}},
                                             'rewards': {'function': 'bm:p206/hit'}})
    vic = '@e[type=!minecraft:player,distance=..7,nbt={HurtTime:10s},sort=nearest,limit=1]'
    fn('p206/hit', ['advancement revoke @s only bm:p206/hit', 'tag @s add bm.dsme',
                    f'execute as {vic} run tag @s add bm.dsv',
                    'execute if predicate bm:p20/sneaking if function bm:p206/any_set run function bm:p206/strike',
                    f'execute if {wear("dread_visage")} if predicate bm:p206/quarter as @e[tag=bm.dsv] at @s run function bm:p206/p/frost',
                    f'execute if {wear("dread_greaves")} if predicate bm:p206/quarter as @e[tag=bm.dsv] at @s run function bm:p206/p/hex',
                    f'execute if entity @e[tag=bm.dsv] if {wear("dread_treads")} if predicate bm:p206/quarter run function bm:p206/p/frenzy',
                    f'execute if entity @e[tag=bm.dsv] if {wear("dread_carapace")} if predicate bm:p206/quarter run function bm:p206/p/leech',
                    'tag @e[tag=bm.dsv] remove bm.dsv', 'tag @s remove bm.dsme'])
    fn('p206/strike', ['execute if score @s bm.dscd matches 1.. run return run function bm:p206/gathering',
                       'execute unless entity @e[tag=bm.dsv] run return 0',
                       'execute if function bm:p206/holy_set run return run function bm:p206/judgment', 'function bm:p206/rending'])
    G.wjson('bm/predicate/p206/quarter.json', {'condition': 'minecraft:random_chance', 'chance': 0.25})
    fn('p206/any_set', ['execute if function bm:p206/dread_set run return 1', 'execute if function bm:p206/holy_set run return 1', 'return 0'])
    fn('p206/gathering', ['scoreboard players operation #s bm.rng = @s bm.dscd',
                          'execute if function bm:p206/holy_set run return run title @s actionbar [{"text":"The light is still gathering... ","color":"#e8e4ff"},{"score":{"name":"#s","objective":"bm.rng"},"color":"white"},{"text":" s","color":"gray"}]',
                          'title @s actionbar [{"text":"The Dread is still gathering... ","color":"#d0182e"},{"score":{"name":"#s","objective":"bm.rng"},"color":"white"},{"text":" s","color":"gray"}]'])
    me = '@p[tag=bm.dsme]'
    fn('p206/p/frost', ['damage @s 6 bm:dread_proc by ' + me, 'effect give @s minecraft:slowness 3 2', 'data merge entity @s {TicksFrozen:200}',
                        'particle minecraft:snowflake ~ ~1 ~ 0.4 0.6 0.4 0.03 20'])
    fn('p206/p/hex', ['damage @s 5 bm:dread_hex by ' + me, 'effect give @s minecraft:weakness 4 1', 'effect give @s minecraft:wither 4 1',
                      'particle minecraft:witch ~ ~1 ~ 0.4 0.6 0.4 0.03 16'])
    fn('p206/p/frenzy', ['execute as @e[tag=bm.dsv] run damage @s 5 bm:dread_proc by ' + me, 'effect give @s minecraft:strength 4 0',
                         'execute at @e[tag=bm.dsv] run particle minecraft:damage_indicator ~ ~1 ~ 0.3 0.4 0.3 0.1 6'])
    fn('p206/p/leech', ['effect give @s minecraft:instant_health 1 0', 'execute at @e[tag=bm.dsv] run particle minecraft:dust{color:[0.82,0.1,0.18],scale:1.2} ~ ~1 ~ 0.3 0.5 0.3 0 12',
                        'particle minecraft:heart ~ ~1.8 ~ 0.3 0.2 0.3 0 2'])
    fn('p206/rending', ['scoreboard players set @s bm.dscd ' + str(CD),
                        'execute as @e[tag=bm.dsv] at @s run function bm:p206/rend_hit',
                        'playsound minecraft:entity.warden.sonic_boom player @a[distance=..24] ~ ~ ~ 0.8 0.7',
                        'playsound minecraft:entity.wither.shoot player @a[distance=..24] ~ ~ ~ 0.8 0.5',
                        say('DREAD RENDING', RED)])
    fn('p206/rend_hit', ['damage @s 24 bm:dread_rend by ' + me, 'effect give @s minecraft:wither 5 1',
                         'particle minecraft:sweep_attack ~ ~1 ~ 0.6 0.4 0.6 0 6', 'particle minecraft:squid_ink ~ ~1 ~ 0.6 0.8 0.6 0.1 40',
                         'particle minecraft:dust{color:[0.82,0.1,0.18],scale:2.0} ~ ~1 ~ 1.5 0.6 1.5 0 60',
                         'execute as @e[type=#bm:hostile,distance=0.1..4,tag=!bm.dsv] run damage @s 8 bm:dread_rend by ' + me])
    fn('p206/judgment', ['scoreboard players set @s bm.dscd ' + str(CD),
                         'execute as @e[tag=bm.dsv] at @s run function bm:p206/judge_hit', 'effect give @s minecraft:instant_health 1 1',
                         'playsound minecraft:block.beacon.activate player @a[distance=..24] ~ ~ ~ 1 1.6',
                         'playsound minecraft:entity.lightning_bolt.thunder player @a[distance=..24] ~ ~ ~ 0.6 1.6',
                         say('SERAPHIC JUDGMENT', HOLY)])
    fn('p206/judge_hit', ['execute if entity @s[type=#minecraft:undead] run damage @s 34 bm:seraph_fire by ' + me,
                          'execute unless entity @s[type=#minecraft:undead] run damage @s 24 bm:seraph_fire by ' + me,
                          'data merge entity @s {Fire:120s}',
                          'particle minecraft:end_rod ~ ~4 ~ 0.15 4 0.15 0.01 80', 'particle minecraft:flame ~ ~2 ~ 0.3 2 0.3 0.02 60',
                          'particle minecraft:flash{color:[1.0,0.95,0.8,1.0]} ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:totem_of_undying ~ ~1 ~ 1.2 0.5 1.2 0.2 40',
                          'execute as @e[type=#bm:hostile,distance=0.1..4,tag=!bm.dsv] run function bm:p206/judge_splash'])
    fn('p206/judge_splash', ['damage @s 8 bm:seraph_fire by ' + me, 'data merge entity @s {Fire:60s}'])

    fn('admin/dreadborne', [give(i) for i in PIECES] + [give('dread_heart'), give('golden_cross', 4)])
    G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/dreadborne', 'yellow'), T('  the Dreadborne set, a Dread Heart and Golden Crosses (for the Seraph)', 'gray')]))

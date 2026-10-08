"""Phase 2.40: relics of an old adventure - Cecil sells them.

- KILLERWATT'S TENDRILS: the storm-alien's lightning arms. Use: a tendril lashes out 24 blocks - a monster is struck for
  10 lightning damage that arcs to two more (5 each); an item is snatched back to you; a block: the tendril grabs it and
  flings you toward it. Sneak + use: grab - a monster is yanked to you; at a wall, the tendril heaves you up it.
  Held: 15% faster, a taller step, and no fall damage.
- APOPHISS'S CROWN: the serpent king's grey crown with its great emerald. Worn: you grow a size, hit harder (+3), reach
  further (+1.5), +4 health, +2 armour; your blows wither. Sneak + jump: SERPENT'S FANGS - a line of dark fangs bursts
  from the ground ahead (6 seconds to recover).
- LEO'S TRIDENT (the vanilla trident and spear, enchanted): Sir Leo's weapon, a TRIDENT (loyalty, impaling: throw it and it comes back) that becomes a SPEAR
  (lunge) - press swap-hands (F) to change it. Both are quick to swing, carry you 15% faster, and every hit gives a
  burst of Speed II.
- CECIL'S STAFF: a lesser copy of his own. Use: a poisoned bolt at what you're looking at (5 + Poison). Sneak + use:
  a mending charm for you and friends within 5 (20 seconds to recover). Not as strong as Cecil himself.
All four are sold by Cecil."""
from items import item, T, TOTEM, attr
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D

YEL, GRN, BLU, PUR = '#ffe23a', '#30d070', '#7ac8ff', '#b48cff'
UNBR = {'minecraft:unbreakable': {}}

item('killerwatt_tendrils', TOTEM, "KillerWatt's Tendrils", YEL,
     ['The storm-alien\'s lightning arms, still crackling.', ('Use: lash out 24 blocks - a monster is struck', 'blue'),
      ('(10, arcing to two more); an item is snatched;', 'blue'), ('a block: you are flung toward it.', 'blue'),
      ('Sneak + use: yank a monster to you,', 'blue'), ('or heave yourself up a wall.', 'blue'),
      ('Held: +15% speed, taller step, no fall damage.', 'blue')],
     model='bm:killerwatt_tendrils', stack=1, cat='weapon', glint=False, tier=3,
     comps=hold('none', {'minecraft:attribute_modifiers': [attr('movement_speed', 0.15, 'mainhand', 'add_multiplied_base'), attr('step_height', 0.5, 'mainhand')],
                         'minecraft:enchantments': {'bm:kw_tendrils': 1}}))
HOLD['killerwatt_tendrils'] = 'bm:p59/kw/use'
item('apophiss_crown', TOTEM, "Apophiss's Crown", GRN,
     ['The serpent king\'s grey crown. The emerald watches you.', ('Worn: you grow a size, +3 damage, +1.5 reach,', 'blue'),
      ('+4 health, +2 armour; your blows wither', 'blue'), ('(+3 against the undead).', 'blue'), ('Sneak + jump: Serpent\'s Fangs (6 s).', 'blue'),
      ('Taken from Apophiss by Cecil, Leo and Emma.', 'dark_gray')],
     model='bm:apophiss_crown', stack=1, cat='relic', glint=False, tier=3,
     comps={'minecraft:equippable': {'slot': 'head', 'swappable': True, 'equip_sound': 'minecraft:item.armor.equip_netherite'},
            'minecraft:attribute_modifiers': [attr('scale', 0.2, 'head'), attr('attack_damage', 3, 'head'), attr('entity_interaction_range', 1.5, 'head'),
                                              attr('block_interaction_range', 1.0, 'head'), attr('max_health', 4, 'head'), attr('armor', 2, 'head')],
            'minecraft:enchantments': {'bm:serpent_venom': 1}})
LEO_LORE = [('Press swap-hands (F) to change its form.', 'blue'), ('Swift; +15% speed held; hits give Speed II.', 'blue'),
            ('Sir Leo\'s own. He fought Apophiss with it.', 'dark_gray')]
item('leo_trident', 'minecraft:trident', "Leo's Trident", BLU,
     ['A knight\'s trident of blue steel and sea-glass.', ('Trident form: throw it - it comes back.', 'blue')] + LEO_LORE,
     stack=1, cat='weapon', tier=3,
     comps=dict(UNBR, **{'minecraft:enchantments': {'minecraft:loyalty': 3, 'minecraft:impaling': 3, 'bm:leo_swift': 1},
                         'minecraft:attribute_modifiers': [attr('attack_damage', 9, 'mainhand', ident='minecraft:base_attack_damage'),
                                                           attr('attack_speed', -2.1, 'mainhand', ident='minecraft:base_attack_speed'),
                                                           attr('movement_speed', 0.15, 'mainhand', 'add_multiplied_base')]}))
item('leo_spear', 'minecraft:netherite_spear', "Leo's Trident", BLU,
     ['A knight\'s trident of blue steel and sea-glass.', ('Spear form: charge and lunge.', 'blue')] + LEO_LORE,
     stack=1, cat='weapon', tier=3,
     comps=dict(UNBR, **{'minecraft:enchantments': {'minecraft:lunge': 3, 'bm:leo_swift': 1},
                         'minecraft:attribute_modifiers': [attr('attack_damage', 7, 'mainhand', ident='minecraft:base_attack_damage'),
                                                           attr('attack_speed', -1.4, 'mainhand', ident='minecraft:base_attack_speed'),
                                                           attr('movement_speed', 0.15, 'mainhand', 'add_multiplied_base')]}))
item('cecil_staff', TOTEM, "Cecil's Staff", PUR,
     ['A copy of the wizard\'s crescent staff. Lesser,', 'he insists, "but adequate for apprentices."',
      ('Use: a poisoned bolt (5 + Poison).', 'blue'), ('Sneak + use: mend yourself and friends near you', 'blue'), ('(20 seconds to recover).', 'blue')],
     model='bm:cecil_staff', stack=1, cat='magic', glint=False, tier=2, comps=hold('none'))
HOLD['cecil_staff'] = 'bm:p59/staff/use'


def extend_offers(O, offer):
    O['wizard'] += [offer(('trophy', 6), ('killerwatt_tendrils', 1)), offer(('trophy', 7), ('apophiss_crown', 1)),
                    offer(('trophy', 5), ('leo_trident', 1)), offer(('trophy', 2), ('cecil_staff', 1))]


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    from phase46 import COMPANIONS
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    tick, fast = [], []
    objs = ['bm.kwcd dummy', 'bm.crcd dummy', 'bm.stcd dummy', 'bm.sthc dummy', 'bm.crj minecraft.custom:minecraft.jump']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o}' for o in objs]
    G.OBJECTIVES += [o.split()[0] for o in objs]
    holds = '*[minecraft:custom_data~{bm:"%s"}]'
    mob = 'type=!#bm:p44_nonmob,type=!minecraft:player,tag=!bm.npc,' + COMPANIONS
    tick.append('scoreboard players remove @a[scores={bm.kwcd=1..}] bm.kwcd 1')
    tick.append('scoreboard players remove @a[scores={bm.stcd=1..}] bm.stcd 1')
    tick.append('scoreboard players remove @a[scores={bm.sthc=1..}] bm.sthc 1')
    tick.append('scoreboard players remove @a[scores={bm.crcd=1..}] bm.crcd 1')

    # ------------------------------------------------------------------ enchantments: the tendrils' fling, the crown's venom, Leo's swiftness
    def ench(desc, col, items, slot, effects):
        return {'anvil_cost': 8, 'description': T(desc, col), 'max_level': 1, 'weight': 1, 'min_cost': {'base': 1, 'per_level_above_first': 0},
                'max_cost': {'base': 1, 'per_level_above_first': 0}, 'slots': [slot], 'supported_items': items, 'effects': effects}
    tagged = lambda t: {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["%s"]}' % t}}
    def fling(tagname, direction, scale, mag):
        return {'requirements': tagged(tagname), 'effect': {'type': 'minecraft:all_of', 'effects': [
            {'type': 'minecraft:apply_impulse', 'direction': direction, 'coordinate_scale': scale, 'magnitude': mag},
            {'type': 'minecraft:run_function', 'function': f'bm:p59/kw/flung'}]}}
    wjson('bm/enchantment/kw_tendrils.json', ench('Storm Tendrils', YEL, 'minecraft:totem_of_undying', 'mainhand', {
        'minecraft:tick': [fling('bm.kwl1', [0, 0, 1], [1, 1, 1], 1.25), fling('bm.kwl2', [0, 0, 1], [1, 1, 1], 1.85), fling('bm.kwl3', [0, 0, 1], [1, 1, 1], 2.45),
                           fling('bm.kwup', [0, 1, 0], [0.2, 1, 0.2], 1.15)],
        'minecraft:damage_immunity': [{'requirements': {'condition': 'minecraft:damage_source_properties', 'predicate': {'tags': [{'id': '#minecraft:is_fall', 'expected': True}]}},
                                       'effect': {}}]}))
    fn('p59/kw/flung', ['tag @s remove bm.kwl1', 'tag @s remove bm.kwl2', 'tag @s remove bm.kwl3', 'tag @s remove bm.kwup'])
    tick.append('execute as @a[tag=bm.kwarm] run function bm:p59/kw/disarm')                      # a fling that never landed (tendrils let go of)
    wjson('bm/enchantment/serpent_venom.json', ench("Serpent's Venom", GRN, 'minecraft:totem_of_undying', 'head', {
        # (the undead shrug off Wither - the serpent's dark magic bites them harder instead)
        'minecraft:damage': [{'effect': {'type': 'minecraft:add', 'value': 3.0}, 'requirements': {
            'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:entity_type': '#minecraft:sensitive_to_smite'}}}]}))
    wjson('bm/enchantment/leo_swift.json', ench('Swiftness', BLU, ['minecraft:trident', 'minecraft:netherite_spear'], 'mainhand', {
        'minecraft:post_attack': [{'enchanted': 'attacker', 'affected': 'attacker', 'effect': {'type': 'minecraft:apply_mob_effect', 'to_apply': 'minecraft:speed',
                                                                                                'min_duration': 3.0, 'max_duration': 3.0, 'min_amplifier': 1.0, 'max_amplifier': 1.0}}]}))

    # ------------------------------------------------------------------ KILLERWATT'S TENDRILS
    fn('p59/kw/use', ['execute if score @s bm.kwcd matches 1.. run return 0',
                      'execute if entity @s[tag=bm.adv] run return run ' + say('The tendrils go limp in here.'),
                      'tag @s add bm.kwme', 'scoreboard players set #kr bm.rng 48', 'scoreboard players set #kh bm.rng 0',
                      'execute anchored eyes positioned ^ ^ ^ run function bm:p59/kw/ray',
                      'execute if score #kh bm.rng matches 0 run function bm:p59/kw/miss',
                      'tag @s remove bm.kwme', 'kill @e[type=minecraft:marker,tag=bm.kwend]'])
    hit_mob = f'@e[{mob},distance=..1.25,tag=!bm.kwme,sort=nearest,limit=1]'
    fn('p59/kw/ray', [f'execute positioned ~ ~-0.9 ~ if entity {hit_mob} positioned ~ ~0.9 ~ run return run function bm:p59/kw/at_mob',
                      'execute positioned ~ ~-0.4 ~ if entity @e[type=minecraft:item,distance=..1.3] run return run function bm:p59/kw/at_item',
                      'execute unless block ~ ~ ~ #bm:grap_pass run return run function bm:p59/kw/at_block',
                      'particle minecraft:dust{color:[1.0,0.9,0.25],scale:0.7} ~ ~ ~ 0.02 0.02 0.02 0 1',
                      'scoreboard players remove #kr bm.rng 1',
                      'execute if score #kr bm.rng matches 1.. positioned ^ ^ ^0.5 run function bm:p59/kw/ray'])
    fn('p59/kw/miss', ['scoreboard players set @s bm.kwcd 8', 'playsound minecraft:entity.breeze.shoot player @a[distance=..16] ~ ~ ~ 0.7 1.6'])
    # a monster: struck (or, sneaking, yanked to you)
    fn('p59/kw/at_mob', ['scoreboard players set #kh bm.rng 1', 'particle minecraft:electric_spark ~ ~ ~ 0.3 0.3 0.3 0.3 20',
                         f'execute positioned ~ ~-0.9 ~ as {hit_mob} at @s run function bm:p59/kw/mob'])
    fn('p59/kw/mob', ['execute if entity @a[tag=bm.kwme,limit=1,predicate=bm:p20/sneaking] run return run function bm:p59/kw/yank',
                      'tag @s add bm.kwhit', 'damage @s 10 minecraft:lightning_bolt by @a[tag=bm.kwme,limit=1]',
                      'particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.4 30', 'particle minecraft:flash{color:[1.0,0.95,0.5,1.0]} ~ ~1 ~ 0 0 0 0 1',
                      'playsound minecraft:entity.lightning_bolt.thunder player @a[distance=..24] ~ ~ ~ 0.4 1.8',
                      'playsound minecraft:block.copper_bulb.turn_on player @a[distance=..16] ~ ~ ~ 1 0.6',
                      f'execute as @e[{mob},distance=..5,tag=!bm.kwhit,sort=nearest,limit=2] at @s run function bm:p59/kw/arc',
                      'tag @e[tag=bm.kwhit] remove bm.kwhit',
                      'execute as @a[tag=bm.kwme,limit=1] run scoreboard players set @s bm.kwcd 12'])
    fn('p59/kw/arc', ['tag @s add bm.kwhit', 'damage @s 5 minecraft:lightning_bolt by @a[tag=bm.kwme,limit=1]',
                      'particle minecraft:electric_spark ~ ~1 ~ 0.3 0.5 0.3 0.3 16',
                      'execute facing entity @e[tag=bm.kwhit,distance=0.1..6,limit=1,sort=nearest] feet run function bm:p59/kw/arcline'])
    fn('p59/kw/arcline', [f'particle minecraft:dust{{color:[1.0,0.95,0.4],scale:0.8}} ^ ^1 ^{d / 2} 0.05 0.05 0.05 0 1' for d in range(1, 10)])
    # (as the monster: pulled toward the player with Motion)
    fn('p59/kw/yank', ['execute as @a[tag=bm.kwme,limit=1] run scoreboard players set @s bm.kwcd 20',
                       'execute facing entity @a[tag=bm.kwme,limit=1] feet positioned ^ ^ ^1.6 positioned ~ ~0.55 ~ run function bm:p59/kw/vec',
                       'particle minecraft:electric_spark ~ ~1 ~ 0.3 0.5 0.3 0.2 16', 'playsound minecraft:item.trident.riptide_1 player @a[distance=..16] ~ ~ ~ 0.8 1.6'])
    # Motion = (here - mob): a marker reads the point, as the grappling hook does
    fn('p59/kw/vec', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.kwvec"]}'] +
       [f'execute store result score #v{a} bm.rng run data get entity @e[type=minecraft:marker,tag=bm.kwvec,limit=1] Pos[{i}] 1000' for i, a in enumerate('xyz')] +
       ['kill @e[type=minecraft:marker,tag=bm.kwvec]'] +
       [f'execute store result score #c{a} bm.rng run data get entity @s Pos[{i}] 1000' for i, a in enumerate('xyz')] +
       [f'scoreboard players operation #v{a} bm.rng -= #c{a} bm.rng' for a in 'xyz'] +
       [f'execute store result entity @s Motion[{i}] double 0.001 run scoreboard players get #v{a} bm.rng' for i, a in enumerate('xyz')])
    # an item: snatched back to you
    fn('p59/kw/at_item', ['scoreboard players set #kh bm.rng 1', 'execute positioned ~ ~-0.4 ~ run tp @e[type=minecraft:item,distance=..1.3] @a[tag=bm.kwme,limit=1]',
                          'particle minecraft:electric_spark ~ ~ ~ 0.2 0.2 0.2 0.2 10',
                          'execute as @a[tag=bm.kwme,limit=1] at @s run playsound minecraft:entity.item.pickup player @s ~ ~ ~ 0.8 0.8',
                          'execute as @a[tag=bm.kwme,limit=1] run scoreboard players set @s bm.kwcd 6'])
    # a block: flung toward it - how hard depends on how far (sneaking at a wall: heaved up it)
    fn('p59/kw/at_block', ['scoreboard players set #kh bm.rng 1', 'particle minecraft:electric_spark ~ ~ ~ 0.2 0.2 0.2 0.2 12',
                           'playsound minecraft:block.chain.place player @a[distance=..16] ~ ~ ~ 1 1.4',
                           'execute as @a[tag=bm.kwme,limit=1] at @s run function bm:p59/kw/fling'])
    fn('p59/kw/fling', ['scoreboard players set @s bm.kwcd 20', 'tag @s add bm.kwarm',
                        'execute if predicate bm:p20/sneaking run return run tag @s add bm.kwup',
                        'execute if score #kr bm.rng matches 33.. run return run tag @s add bm.kwl1',
                        'execute if score #kr bm.rng matches 17.. run return run tag @s add bm.kwl2',
                        'tag @s add bm.kwl3'])
    fn('p59/kw/disarm', ['execute unless items entity @s weapon.mainhand ' + holds % 'killerwatt_tendrils' + ' run function bm:p59/kw/flung',
                                'execute unless entity @s[tag=bm.kwl1] unless entity @s[tag=bm.kwl2] unless entity @s[tag=bm.kwl3] unless entity @s[tag=bm.kwup] run tag @s remove bm.kwarm'])
    # held: a faint crackle
    fast.append(f'execute as @a[gamemode=!spectator] if items entity @s weapon.mainhand {holds % "killerwatt_tendrils"} at @s run particle minecraft:electric_spark ^-0.4 ^1.1 ^0.3 0.1 0.1 0.1 0.05 1')

    # ------------------------------------------------------------------ APOPHISS'S CROWN: Serpent's Fangs on sneak + jump
    tick.append(f'execute as @a[scores={{bm.crj=1..}}] at @s run function bm:p59/crown/jump')
    fn('p59/crown/jump', ['scoreboard players reset @s bm.crj', f'execute unless items entity @s armor.head {holds % "apophiss_crown"} run return 0',
                          'execute unless predicate bm:p20/sneaking run return 0',
                          'execute if score @s bm.crcd matches 1.. run return run ' + say("The crown's power is still gathering."),
                          'execute if entity @s[tag=bm.adv] run return 0',
                          'scoreboard players set @s bm.crcd 120', 'execute at @s rotated ~ 0 run function bm:p59/crown/fangs'])
    fn('p59/crown/fangs', [f'summon minecraft:evoker_fangs ^ ^ ^{1.6 + i * 1.25:.2f} {{Warmup:{i * 2},Tags:["bm.cfnew"]}}' for i in range(12)] +
       ['execute as @e[type=minecraft:evoker_fangs,tag=bm.cfnew,distance=..20] run data modify entity @s Owner set from entity @a[tag=bm.crme,limit=1] UUID',
        'tag @e[type=minecraft:evoker_fangs,tag=bm.cfnew] remove bm.cfnew',
        'particle minecraft:squid_ink ~ ~1 ~ 0.5 0.6 0.5 0.05 30', 'particle minecraft:witch ~ ~1.4 ~ 0.5 0.6 0.5 0.1 20',
        'playsound minecraft:entity.evoker.cast_spell player @a[distance=..24] ~ ~ ~ 1 0.6', 'playsound minecraft:entity.ender_dragon.growl player @a[distance=..24] ~ ~ ~ 0.4 1.6'])
    G.FUNCS['p59/crown/fangs'].insert(0, 'tag @s add bm.crme'); G.FUNCS['p59/crown/fangs'].append('tag @s remove bm.crme')
    G.FUNCS['loop/second'][-1:-1] = [f'execute as @a[gamemode=!spectator] if items entity @s armor.head {holds % "apophiss_crown"} at @s run particle minecraft:dust{{color:[0.2,0.8,0.35],scale:0.8}} ~ ~2.3 ~ 0.25 0.1 0.25 0 2']

    # (a worn crown's enchantment can't touch what its wearer hits, so the wither rides a hit advancement)
    wjson('bm/advancement/p59/crown_hit.json', {'criteria': {'hit': {'trigger': 'minecraft:player_hurt_entity', 'conditions': {'player': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'equipment': {'head': {'predicates': {'minecraft:custom_data': '{bm:"apophiss_crown"}'}}}}}]}}},
        'rewards': {'function': 'bm:p59/crown/hit'}})
    fn('p59/crown/hit', ['advancement revoke @s only bm:p59/crown/hit',
                         f'execute at @s as @e[{mob},distance=..8,nbt={{HurtTime:10s}}] at @s run function bm:p59/crown/venom'])
    G.FUNCS['p59/crown/hit'][0] = 'advancement revoke @s only bm:p59/crown_hit'
    fn('p59/crown/venom', ['effect give @s minecraft:wither 3 0', 'particle minecraft:squid_ink ~ ~1 ~ 0.3 0.4 0.3 0.02 6'])

    # ------------------------------------------------------------------ LEO'S TRIDENT: swap-hands changes its form
    tick += [f'execute as @a if items entity @s weapon.offhand {holds % "leo_trident"} at @s run function bm:p59/leo/to_spear',
             f'execute as @a if items entity @s weapon.offhand {holds % "leo_spear"} at @s run function bm:p59/leo/to_trident']
    for frm, to, msg in (('trident', 'spear', 'Spear form.'), ('spear', 'trident', 'Trident form.')):
        fn(f'p59/leo/to_{to}', ['item replace entity @s weapon.offhand from entity @s weapon.mainhand',
                                f'item replace entity @s weapon.mainhand with {G.item_arg("leo_" + to)}',
                                'execute at @s run particle minecraft:bubble_pop ~ ~1.2 ~ 0.3 0.3 0.3 0.05 16',
                                'execute at @s run playsound minecraft:item.trident.return player @a[distance=..12] ~ ~ ~ 1 1.5', say(msg, BLU)])

    # ------------------------------------------------------------------ CECIL'S STAFF
    fn('p59/staff/use', ['execute if predicate bm:p20/sneaking run return run function bm:p59/staff/mend',
                         'execute if score @s bm.stcd matches 1.. run return 0', 'scoreboard players set @s bm.stcd 30',
                         'tag @s add bm.stme', 'scoreboard players set #sr bm.rng 32',
                         'execute anchored eyes positioned ^ ^ ^ run function bm:p59/staff/ray', 'tag @s remove bm.stme',
                         'playsound minecraft:entity.evoker.cast_spell player @a[distance=..16] ~ ~ ~ 0.7 1.5'])
    st_mob = f'@e[{mob},distance=..1.25,tag=!bm.stme,sort=nearest,limit=1]'
    fn('p59/staff/ray', [f'execute positioned ~ ~-0.9 ~ as {st_mob} at @s run return run function bm:p59/staff/hit',
                         'execute unless block ~ ~ ~ #bm:grap_pass run return 0',
                         'particle minecraft:dust{color:[0.6,0.3,0.9],scale:0.8} ~ ~ ~ 0 0 0 0 1',
                         'scoreboard players remove #sr bm.rng 1', 'execute if score #sr bm.rng matches 1.. positioned ^ ^ ^0.5 run function bm:p59/staff/ray'])
    fn('p59/staff/hit', ['damage @s 5 minecraft:magic by @a[tag=bm.stme,limit=1]', 'effect give @s minecraft:poison 4 0',
                         'particle minecraft:dust{color:[0.45,0.9,0.2],scale:1.2} ~ ~1 ~ 0.3 0.4 0.3 0 12', 'particle minecraft:item_slime ~ ~1 ~ 0.3 0.4 0.3 0 6'])
    fn('p59/staff/mend', ['execute if score @s bm.sthc matches 1.. store result score #m bm.rng run scoreboard players get @s bm.sthc',
                          'execute if score @s bm.sthc matches 1.. run scoreboard players operation #m bm.rng /= #20 bm.rng',
                          'execute if score @s bm.sthc matches 1.. run return run ' + title('@s', 'actionbar', [T('The staff is still mending itself: ', 'gray'),
                                                                                                             {'score': {'name': '#m', 'objective': 'bm.rng'}, 'color': 'white'}, T(' s', 'gray')]),
                          'scoreboard players set @s bm.sthc 400',
                          'execute at @s as @a[distance=..5,gamemode=!spectator] at @s run function bm:p59/staff/mend1',
                          'execute at @s run playsound minecraft:block.amethyst_block.chime player @a[distance=..16] ~ ~ ~ 1 1.4'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #20 bm.rng 20']
    fn('p59/staff/mend1', ['effect give @s minecraft:instant_health 1 0 true', 'effect give @s minecraft:regeneration 4 0 true',
                           'particle minecraft:heart ~ ~2 ~ 0.4 0.3 0.4 0 4', 'particle minecraft:witch ~ ~1 ~ 0.4 0.6 0.4 0.05 10'])

    fn('admin/cecil_relics', [give('killerwatt_tendrils'), give('apophiss_crown'), give('leo_trident'), give('cecil_staff'),
                              tellraw('@s', PREFIX + [T("KillerWatt's Tendrils, Apophiss's Crown, Leo's Trident and Cecil's Staff.", 'gray')])])
    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast


# ===================================================================== resource pack: four 3D models
HELD = {'gui': {'rotation': [30, 225, 0], 'translation': [0, 0, 0], 'scale': [0.6, 0.6, 0.6]},
        'ground': {'rotation': [0, 0, 0], 'translation': [0, 2, 0], 'scale': [0.35, 0.35, 0.35]},
        'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [0.6, 0.6, 0.6]},
        'thirdperson_righthand': {'rotation': [0, -90, 10], 'translation': [0, 3, 0.5], 'scale': [0.85, 0.85, 0.85]},
        'thirdperson_lefthand': {'rotation': [0, 90, -10], 'translation': [0, 3, 0.5], 'scale': [0.85, 0.85, 0.85]},
        'firstperson_righthand': {'rotation': [0, -90, 15], 'translation': [1.13, 3.2, 1.13], 'scale': [0.68, 0.68, 0.68]},
        'firstperson_lefthand': {'rotation': [0, 90, -15], 'translation': [1.13, 3.2, 1.13], 'scale': [0.68, 0.68, 0.68]}}
LONG = dict(HELD, gui={'rotation': [0, 0, -45], 'translation': [0, 0, 0], 'scale': [0.42, 0.42, 0.42]})


def textures():
    import random
    from PIL import Image
    from gen_rp import hexc
    rnd = random.Random(59)
    def noise(base, var, size=16, streak=None):
        im = Image.new('RGBA', (size, size)); b = hexc(base)
        for y in range(size):
            for x in range(size):
                d = rnd.randint(-var, var) - (var * 2 if streak and x in streak else 0)
                im.putpixel((x, y), tuple(max(0, min(255, c + d)) for c in b[:3]) + (255,))
        return im
    T_ = {'kw_yellow': noise('#f2d42c', 14), 'kw_yellow_lt': noise('#fff27a', 10), 'kw_green': noise('#2e9a4a', 10), 'kw_teal': noise('#1d7a5c', 8),
          'ap_grey': noise('#8c9096', 8, streak=(4, 11)), 'ap_grey_dk': noise('#5c6066', 6), 'ap_emerald': noise('#2ad060', 16), 'ap_ruby': noise('#d02030', 14),
          'ap_fur': noise('#f0ece0', 8)}
    for y in range(16):
        for x in range(16):
            if (x + y) % 6 == 0: T_['ap_emerald'].putpixel((x, y), hexc('#a8ffc8'))
    return T_


def rp(R):
    import sys, math
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
        # KillerWatt's tendrils: a green gauntlet grip, three jagged yellow tendrils fanning up and out, barbed
        kw = [c((6, 0, 6), (10, 6, 10), 'g'), c((5.5, 5, 5.5), (10.5, 7, 10.5), 't')]
        for k, (dx, lean) in enumerate(((-1, 22), (0, 0), (1, -22))):
            x, y = 8 + dx * 1.2, 6.5
            for seg, (L, ang, w) in enumerate(((6, lean, 1.6), (6, lean * 1.6 + 12, 1.3), (5, lean * 2 - 20, 1.0), (4, lean * 2 + 25, 0.8))):
                kw.append(c((x - w / 2, y, 7.4), (x + w / 2, y + L, 8.6), 'y' if seg % 2 == 0 else 'l', ('z', max(-45, min(45, ang)), (x, y, 8))))
                a = math.radians(ang); x, y = x - L * math.sin(a), y + L * math.cos(a)
            kw.append(c((x - 0.4, y - 1, 7.6), (x + 0.4, y + 2.5, 8.4), 'l', ('z', 22.5, (x, y, 8))))
        model('killerwatt_tendrils', {'y': 'kw_yellow', 'l': 'kw_yellow_lt', 'g': 'kw_green', 't': 'kw_teal'}, kw, HELD)
        # Apophiss's crown (worn): grey band, fur trim, spikes with ball tips, a great emerald and a ruby
        cr = [c((2.6, 14.2, 2.6), (13.4, 15.4, 13.4), 'f'),
              c((3, 15.2, 3), (13, 18.4, 4), 'g'), c((3, 15.2, 12), (13, 18.4, 13), 'g'), c((3, 15.2, 4), (4, 18.4, 12), 'g'), c((12, 15.2, 4), (13, 18.4, 12), 'g')]
        for (x, z) in ((3, 3), (12, 3), (3, 12), (12, 12), (7.5, 3), (7.5, 12), (3, 7.5), (12, 7.5)):
            hh = 3.6 if (x, z) in ((3, 3), (12, 3), (3, 12), (12, 12)) else 2.4
            cr += [c((x, 18.4, z), (x + 1, 18.4 + hh, z + 1), 'g', ('y', 45, (x + 0.5, 19, z + 0.5))), c((x + 0.1, 18.4 + hh, z + 0.1), (x + 0.9, 19.2 + hh, z + 0.9), 'd')]
        cr += [c((6, 15.6, 2.3), (10, 19.4, 3.1), 'e'), c((6.6, 19.4, 2.4), (9.4, 20.6, 3.0), 'e'), c((7.4, 16.6, 1.9), (8.6, 18.4, 2.4), 'r'),
               c((4.4, 16.4, 2.6), (5.2, 17.2, 3.1), 'r'), c((10.8, 16.4, 2.6), (11.6, 17.2, 3.1), 'r')]
        model('apophiss_crown', {'g': 'ap_grey', 'd': 'ap_grey_dk', 'e': 'ap_emerald', 'r': 'ap_ruby', 'f': 'ap_fur'}, cr, R2.GUI_3D)
        # Cecil's staff: his own crescent staff, a little smaller
        import json, os
        arm = json.load(open(R2.p('assets', 'bm', 'models', 'item', 'cec_arm.json')))
        els = [e for e in arm['elements'] if e['faces'][next(iter(e['faces']))]['texture'] in ('#w', '#g', '#p')]
        def shrink(e, k=0.78, dy=-6):
            e = json.loads(json.dumps(e))
            e['from'] = [8 + (v - 8) * k + (dy if i == 1 else 0) for i, v in enumerate(e['from'])]
            e['to'] = [8 + (v - 8) * k + (dy if i == 1 else 0) for i, v in enumerate(e['to'])]
            if 'rotation' in e: e['rotation']['origin'] = [8 + (v - 8) * k + (dy if i == 1 else 0) for i, v in enumerate(e['rotation']['origin'])]
            for f in e['faces'].values(): f['uv'] = [max(0, min(16, u)) for u in f['uv']]
            return e
        model('cecil_staff', {k: v for k, v in arm['textures'].items() if k in ('w', 'g', 'p')}, [shrink(e) for e in els], LONG)
    R.POST.append(post)

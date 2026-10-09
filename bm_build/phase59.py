"""Phase 2.40: relics of an old adventure - Cecil sells them.

- KILLERWATT'S TENDRILS: the storm-alien's lightning arms. Use: a tendril lashes out 24 blocks - a monster is struck for
  10 lightning damage that arcs to two more (5 each); an item is snatched back to you; a block: the tendril grabs it and
  flings you toward it. Sneak + use: grab - a monster is yanked to you; at a wall, the tendril heaves you up it.
  Held: 15% faster, a taller step, and no fall damage.
- APOPHISS'S CROWN: the serpent king's black crown with its great emerald. Worn: you grow a size, hit harder (+3), reach
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
     ['The storm-alien\'s lightning arms. Worn in place of', 'a chestplate (no armour): four tendrils from your back.',
      ('Double-tap sneak: switch RANGED / OFFENSE.', 'gold'),
      ('Ranged: they lash monsters ahead of you (up to', 'blue'), ('20 blocks) - 10 lightning, arcing to two more.', 'blue'),
      ('Offense: +2 reach; your blows bring a double', 'blue'), ('stab (+6, piercing), and they drag monsters in.', 'blue'),
      ('Sneak + jump: fling yourself where you look,', 'blue'), ('or up the wall in front of you.', 'blue'),
      ('They snatch up dropped items near you.', 'blue'), ('+15% speed, taller step, no fall damage.', 'blue'),
      ('Rain: stronger, faster. Thunderstorm: far stronger,', 'aqua'), ('and they call down lightning.', 'aqua')],
     model='bm:killerwatt_tendrils', stack=1, cat='weapon', glint=False, tier=3,
     comps={'minecraft:equippable': {'slot': 'chest', 'swappable': True, 'equip_sound': 'minecraft:item.armor.equip_chain'},
            'minecraft:attribute_modifiers': [attr('movement_speed', 0.15, 'chest', 'add_multiplied_base'), attr('step_height', 0.5, 'chest'),
                                                attr('entity_interaction_range', 2, 'chest')],
            'minecraft:enchantments': {'bm:kw_tendrils': 1}})
item('apophiss_crown', TOTEM, "Apophiss's Crown", GRN,
     ['The serpent king\'s black crown. The emerald watches you.', ('Worn: you grow a size, +3 damage, +1.5 reach,', 'blue'),
      ('+4 health; your blows wither (+3 vs the undead).', 'blue'), ('No protection - it is a crown, not a helm.', 'gray'),
      ('Night: Strength, Night Vision; the fangs come', 'dark_purple'), ('twice as often, and more of them.', 'dark_purple'), ('Sneak + jump: Serpent\'s Fangs (6 s).', 'blue'),
      ('Taken from Apophiss by Cecil, Leo and Emma.', 'dark_gray')],
     model='bm:apophiss_crown', stack=1, cat='relic', glint=False, tier=3,
     comps={'minecraft:equippable': {'slot': 'head', 'swappable': True, 'equip_sound': 'minecraft:item.armor.equip_netherite'},
            'minecraft:attribute_modifiers': [attr('scale', 0.2, 'head'), attr('attack_damage', 3, 'head'), attr('entity_interaction_range', 1.5, 'head'),
                                              attr('block_interaction_range', 1.0, 'head'), attr('max_health', 4, 'head')],
            'minecraft:enchantments': {'bm:serpent_venom': 1}})
LEO_LORE = [('Press swap-hands (F) to change its form.', 'blue'), ('Swift; +15% speed held; hits give Speed II.', 'blue'),
            ('In water, in the rain or by the sea: Strength,', 'aqua'), ("Dolphin's Grace and Conduit Power.", 'aqua'),
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
    wjson('bm/enchantment/kw_tendrils.json', ench('Storm Tendrils', YEL, 'minecraft:totem_of_undying', 'chest', {
        'minecraft:tick': [fling('bm.kwl1', [0, 0, 1], [1, 1, 1], 1.25), fling('bm.kwl2', [0, 0, 1], [1, 1, 1], 1.85), fling('bm.kwl3', [0, 0, 1], [1, 1, 1], 2.45),
                           fling('bm.kwup', [0, 1, 0], [0.2, 1, 0.2], 1.15)],
        'minecraft:damage_immunity': [{'requirements': {'condition': 'minecraft:damage_source_properties', 'predicate': {'tags': [{'id': '#minecraft:is_fall', 'expected': True}]}},
                                       'effect': {}}]}))
    wjson('bm/enchantment/serpent_venom.json', ench("Serpent's Venom", GRN, 'minecraft:totem_of_undying', 'head', {
        # (the undead shrug off Wither - the serpent's dark magic bites them harder instead)
        'minecraft:damage': [{'effect': {'type': 'minecraft:add', 'value': 3.0}, 'requirements': {
            'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:entity_type': '#minecraft:sensitive_to_smite'}}}]}))
    wjson('bm/enchantment/leo_swift.json', ench('Swiftness', BLU, ['minecraft:trident', 'minecraft:netherite_spear'], 'mainhand', {
        'minecraft:post_attack': [{'enchanted': 'attacker', 'affected': 'attacker', 'effect': {'type': 'minecraft:apply_mob_effect', 'to_apply': 'minecraft:speed',
                                                                                                'min_duration': 3.0, 'max_duration': 3.0, 'min_amplifier': 1.0, 'max_amplifier': 1.0}}]}))

    # ------------------------------------------------------------------ KILLERWATT'S TENDRILS (worn on the chest)
    wjson('bm/predicate/p59/rain.json', {'condition': 'minecraft:all_of', 'terms': [{'condition': 'minecraft:weather_check', 'raining': True},
                                                                                   {'condition': 'minecraft:location_check', 'offsetY': 1.6, 'predicate': {'can_see_sky': True}}]})
    wjson('bm/predicate/p59/storm.json', {'condition': 'minecraft:all_of', 'terms': [{'condition': 'minecraft:weather_check', 'thundering': True},
                                                                                    {'condition': 'minecraft:location_check', 'offsetY': 1.6, 'predicate': {'can_see_sky': True}}]})
    worn = f'items entity @s armor.chest {holds % "killerwatt_tendrils"}'
    # the four tendrils: display entities that stand at your back every tick (players can't carry passengers)
    import math as _m
    def qfrom(d):
        """the rotation taking the model's +y (the tendril) to direction d, in the display frame (your front is +z, your right -x)"""
        n = _m.sqrt(sum(v * v for v in d)); d = [v / n for v in d]
        ax = [d[2], 0.0, -d[0]]; s_ = _m.sqrt(ax[0] ** 2 + ax[2] ** 2); c_ = d[1]
        if s_ < 1e-6: return [F(0), F(0), F(0), F(1)]
        h = _m.acos(max(-1, min(1, c_))) / 2; k = _m.sin(h) / s_
        return [F(round(ax[0] * k, 4)), F(0), F(round(ax[2] * k, 4)), F(round(_m.cos(h), 4))]
    # (2.42: two blade segments per tendril, a sharp elbow between - poses and the clipping-checked lunge in phase59_tendrils)
    import phase59_tendrils as TD
    TEN = TD.TENDRILS
    L1 = TD.L1_UNITS * TD.SCALE / 16
    def unit(v):
        n = _m.sqrt(sum(a * a for a in v)); return [a / n for a in v]
    def seg_xf(k, pose):
        b, t = TEN[k][1][pose]
        jb = [round(L1 * a, 4) for a in unit(b)]
        return (f'left_rotation:{snbt(qfrom(b))},translation:[0f,0f,0f]', f'left_rotation:{snbt(qfrom(t))},translation:[{jb[0]}f,{jb[1]}f,{jb[2]}f]')
    def tnbt(k, sg):
        b, t = TEN[k][1]['idle']; jb = [F(round(L1 * a, 4)) for a in unit(b)]
        return snbt({'Tags': ['bm.kwt', f'bm.kwt_{k}', f'bm.kws_{sg}', 'bm.kwtnew'],
                     'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:kw_t{sg}'}},
                     'item_display': 'fixed', 'teleport_duration': Int(1), 'interpolation_duration': Int(10), 'brightness': {'block': Int(12), 'sky': Int(15)},
                     'transformation': {'left_rotation': qfrom(b if sg == 'b' else t), 'right_rotation': [F(0), F(0), F(0), F(1)],
                                        'translation': [F(0)] * 3 if sg == 'b' else jb, 'scale': [F(TD.SCALE)] * 3}})
    tick.append(f'execute as @a[gamemode=!spectator] if {worn} at @s run function bm:p59/kw/tick')
    tick.append('execute as @e[type=minecraft:item_display,tag=bm.kwt,tag=!bm.kwok] run kill @s')       # nobody wears them any more
    tick.append('tag @e[type=minecraft:item_display,tag=bm.kwok] remove bm.kwok')
    KEYS = list(TEN)
    fn('p59/kw/tick', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                       'execute as @e[type=minecraft:item_display,tag=bm.kwt] if score @s bm.pid = #me bm.pid run tag @s add bm.kwok',
                       'execute store result score #n bm.rng if entity @e[type=minecraft:item_display,tag=bm.kwok,distance=..4]',
                       'execute unless score #n bm.rng matches 8 run function bm:p59/kw/sprout',
                       # (2.49) the displays are placed a tick ahead - where you'll be next tick - so they keep up at any speed
                       'function bm:p59/kw/lead',
                       'scoreboard players add @s bm.kwt 1',
                       'scoreboard players operation #f4 bm.rng = @s bm.kwt', 'scoreboard players operation #f4 bm.rng %= #4 bm.rng',
                       # double-tap sneak: RANGED <-> OFFENSE
                       'execute if predicate bm:p20/sneaking unless entity @s[tag=bm.kwsn] run function bm:p59/kw/tap',
                       'execute if predicate bm:p20/sneaking run tag @s add bm.kwsn', 'execute unless predicate bm:p20/sneaking run tag @s remove bm.kwsn',
                       'execute unless score @s bm.kwst matches 100.. run scoreboard players add @s bm.kwst 1',
                       'execute if score @s bm.kwmd matches 1 if score #f4 bm.rng matches 0 unless score @s bm.kwcd matches 1.. unless score @s bm.kwlk matches 4 run function bm:p59/kw/aim',
                       'execute unless score @s bm.kwmd matches 1 if score #f4 bm.rng matches 2 unless score @s bm.kwyc matches 1.. unless score @s bm.kwlk matches 4 run function bm:p59/kw/grab',
                       'execute if score @s bm.kwyc matches 1.. run scoreboard players remove @s bm.kwyc 4',
                       'execute if score @s bm.kwlk matches 4 unless score @s bm.kwlt matches 1.. run scoreboard players set @s bm.kwlk 0',
                       'execute if score @s bm.kwlt matches 1.. run function bm:p59/kw/lunge_tick',
                       'execute if score @s bm.kwjt matches 1.. run function bm:p59/kw/fling_tick',
                       'execute if score @s bm.kwmc matches 1.. run scoreboard players remove @s bm.kwmc 1'])
    fn('p59/kw/lead', ['execute store result score #cx bm.rng run data get entity @s Pos[0] 100', 'execute store result score #cy bm.rng run data get entity @s Pos[1] 100',
                       'execute store result score #cz bm.rng run data get entity @s Pos[2] 100',
                       'scoreboard players operation #dx bm.rng = #cx bm.rng', 'scoreboard players operation #dx bm.rng -= @s bm.kwpx',
                       'scoreboard players operation #dy bm.rng = #cy bm.rng', 'scoreboard players operation #dy bm.rng -= @s bm.kwpy',
                       'scoreboard players operation #dz bm.rng = #cz bm.rng', 'scoreboard players operation #dz bm.rng -= @s bm.kwpz',
                       'scoreboard players operation @s bm.kwpx = #cx bm.rng', 'scoreboard players operation @s bm.kwpy = #cy bm.rng', 'scoreboard players operation @s bm.kwpz = #cz bm.rng',
                       # (a teleport isn't movement - no lead)
                       'execute unless score #dx bm.rng matches -250..250 run scoreboard players set #dx bm.rng 0', 'execute unless score #dy bm.rng matches -250..250 run scoreboard players set #dy bm.rng 0',
                       'execute unless score #dz bm.rng matches -250..250 run scoreboard players set #dz bm.rng 0',
                       'execute store result storage bm:tmp kw.dx double 0.01 run scoreboard players get #dx bm.rng',
                       'execute store result storage bm:tmp kw.dy double 0.01 run scoreboard players get #dy bm.rng',
                       'execute store result storage bm:tmp kw.dz double 0.01 run scoreboard players get #dz bm.rng',
                       'function bm:p59/kw/lead1 with storage bm:tmp kw'])
    fn('p59/kw/lead1', ['$execute positioned ~$(dx) ~$(dy) ~$(dz) run function bm:p59/kw/place0'])
    fn('p59/kw/place0', ['execute if predicate bm:p20/sneaking rotated ~ 0 positioned ~ ~-0.3 ~ run function bm:p59/kw/place',
                         'execute unless predicate bm:p20/sneaking rotated ~ 0 run function bm:p59/kw/place'])
    fn('p59/kw/place', [f'execute positioned ^{m[0]} ^{m[1]} ^{m[2]} run tp @e[type=minecraft:item_display,tag=bm.kwok,tag=bm.kwt_{k},distance=..4] ~ ~ ~ ~ 0'
                        for k, (m, _p) in TEN.items()])
    fn('p59/kw/sprout', ['execute as @e[type=minecraft:item_display,tag=bm.kwok,distance=..6] run kill @s'] +
       [f'summon minecraft:item_display ~ ~1 ~ {tnbt(k, sg)}' for k in TEN for sg in ('b', 't')] +
       ['scoreboard players operation @e[type=minecraft:item_display,tag=bm.kwtnew] bm.pid = #me bm.pid',
        'tag @e[type=minecraft:item_display,tag=bm.kwtnew] add bm.kwok', 'tag @e[type=minecraft:item_display,tag=bm.kwtnew] remove bm.kwtnew',
        'playsound minecraft:block.copper_bulb.turn_on player @a[distance=..12] ~ ~ ~ 1 0.6', 'particle minecraft:electric_spark ~ ~1.2 ~ 0.3 0.4 0.3 0.2 20',
        'execute if score @s bm.kwmd matches 1 run ' + title('@s', 'actionbar', [T('Tendrils: ', YEL, bold=True), T('RANGED', '#7ac8ff', bold=True), T(' (double-tap sneak to switch)', 'gray')]),
        'execute unless score @s bm.kwmd matches 1 run ' + title('@s', 'actionbar', [T('Tendrils: ', YEL, bold=True), T('OFFENSE', '#ff6a5a', bold=True), T(' (double-tap sneak to switch)', 'gray')])])
    # poses: (as the wearer) both segments of tendril k take a pose over `d` ticks
    POSE_DUR = {'idle': (5,), 'sway_a': (20,), 'sway_b': (20,), 'mid': (2,), 'lunge': (2,), 'fling': (2,)}
    for k in TEN:
        for pose, durs in POSE_DUR.items():
            for d in durs:
                xb, xt = seg_xf(k, pose)
                fn(f'p59/kw/pose/{k}/{pose}', [
                    f'execute as @e[type=minecraft:item_display,tag=bm.kwok,tag=bm.kwt_{k},tag=bm.kws_b,distance=..4] run data merge entity @s {{start_interpolation:0,interpolation_duration:{d},transformation:{{{xb}}}}}',
                    f'execute as @e[type=minecraft:item_display,tag=bm.kwok,tag=bm.kwt_{k},tag=bm.kws_t,distance=..4] run data merge entity @s {{start_interpolation:0,interpolation_duration:{d},transformation:{{{xt}}}}}'])
    # idle: each tendril drifts on its own slow beat (not while one is striking)
    G.FUNCS['p59/kw/tick'] += ['scoreboard players operation #f bm.rng = @s bm.kwt', 'scoreboard players operation #f bm.rng %= #40 bm.rng'] + \
        [f'execute if score #f bm.rng matches {t} unless score @s bm.kwlt matches 1.. unless score @s bm.kwjt matches 1.. run function bm:p59/kw/pose/{k}/sway_{ab}'
         for k, t0 in zip(KEYS, (0, 10, 5, 15)) for t, ab in ((t0, 'a'), (t0 + 20, 'b'))]
    # a strike: the chosen tendril climbs past your head (or out past your arm), lunges forward, pulls back, settles
    fn('p59/kw/lunge_tick', ['scoreboard players remove @s bm.kwlt 1'] +
       [f'execute if score @s bm.kwlk matches {i} if score @s bm.kwlt matches {at} run function bm:p59/kw/pose/{k}/{pose}'
        for i, k in enumerate(KEYS) for at, pose in ((8, 'lunge'), (3, 'mid'), (0, 'idle'))] +
       [f'execute if score @s bm.kwlk matches 4 if score @s bm.kwlt matches {at} run function bm:p59/kw/pose/{k}/{pose}'          # the melee stab: both upper ones
        for k in ('ul', 'ur') for at, pose in ((5, 'lunge'), (1, 'idle'))] +
       ['execute if score @s bm.kwlk matches 4 if score @s bm.kwlt matches 3 run function bm:p59/kw/stab_now'])
    # a charged jump: the upper pair reach up and ahead, the lower pair plant down and push - then they settle
    fn('p59/kw/fling_tick', ['scoreboard players remove @s bm.kwjt 1'] + [f'execute if score @s bm.kwjt matches 0 run function bm:p59/kw/pose/{k}/idle' for k in KEYS])
    fn('p59/kw/fling_pose', ['scoreboard players set @s bm.kwjt 12', 'scoreboard players set @s bm.kwlt 0'] + [f'function bm:p59/kw/pose/{k}/fling' for k in KEYS])

    # RANGED (2.49): no aiming needed - every lash goes to the nearest monster ahead of you (a wide cone, ~20 blocks) you can see
    tgt = 'type=#bm:hostile,tag=!bm.npc'
    fn('p59/kw/aim', ['tag @s add bm.kwme', 'scoreboard players set #kh bm.rng 0',
                      f'execute anchored eyes positioned ^ ^ ^7 as @e[{tgt},distance=..7.5,sort=nearest,limit=1] run tag @s add bm.kwtgt',
                      f'execute unless entity @e[tag=bm.kwtgt] anchored eyes positioned ^ ^ ^15.5 as @e[{tgt},distance=..6.5,sort=nearest,limit=1] run tag @s add bm.kwtgt',
                      'execute if entity @e[tag=bm.kwtgt] run function bm:p59/kw/sighted',
                      'execute if score #kh bm.rng matches 1 run function bm:p59/kw/lash',
                      'execute if score #kh bm.rng matches 1 as @e[tag=bm.kwtgt,limit=1] at @s run function bm:p59/kw/mob',
                      'tag @e[tag=bm.kwtgt] remove bm.kwtgt', 'tag @s remove bm.kwme'])
    # (line of sight: a ray from your eyes to it; #kr = steps left when it arrives, so the beam can be drawn the same length)
    fn('p59/kw/sighted', ['scoreboard players set #kr bm.rng 48',
                          'execute anchored eyes positioned ^ ^ ^ facing entity @e[tag=bm.kwtgt,limit=1] eyes run function bm:p59/kw/ray'])
    fn('p59/kw/ray', ['scoreboard players remove #kr bm.rng 1',
                      'execute if entity @e[tag=bm.kwtgt,distance=..1.4] run return run scoreboard players set #kh bm.rng 1',
                      'execute positioned ~ ~-1 ~ if entity @e[tag=bm.kwtgt,distance=..0.9] run return run scoreboard players set #kh bm.rng 1',
                      'execute unless block ~ ~ ~ #bm:grap_pass run return 0',
                      'execute if score #kr bm.rng matches 1.. positioned ^ ^ ^0.5 run function bm:p59/kw/ray'])
    # OFFENSE (2.49): every 3 s a tendril shoots out and drags the nearest monster 4-12 blocks ahead right up to you
    fn('p59/kw/grab', ['tag @s add bm.kwme', 'scoreboard players set #kh bm.rng 0',
                       f'execute anchored eyes positioned ^ ^ ^8 as @e[{tgt},distance=..4.5,sort=nearest,limit=1] if entity @a[tag=bm.kwme,distance=4..] run tag @s add bm.kwtgt',
                       'execute if entity @e[tag=bm.kwtgt] run function bm:p59/kw/sighted',
                       'execute if score #kh bm.rng matches 1 run function bm:p59/kw/grab_go',
                       'tag @e[tag=bm.kwtgt] remove bm.kwtgt', 'tag @s remove bm.kwme'])
    fn('p59/kw/grab_go', ['scoreboard players set @s bm.kwyc 60', 'execute store result score @s bm.kwlk run random value 0..3', 'scoreboard players set @s bm.kwlt 10'] +
       [f'execute if score @s bm.kwlk matches {i} run function bm:p59/kw/pose/{k}/mid' for i, k in enumerate(KEYS)] +
       ['execute anchored eyes positioned ^ ^ ^ facing entity @e[tag=bm.kwtgt,limit=1] eyes run function bm:p59/kw/beam',
        'execute as @e[tag=bm.kwtgt,limit=1] at @s run function bm:p59/kw/drag'])
    # (as the monster) a short arcing tug that lands it a couple of blocks in front of you, however far it was
    fn('p59/kw/drag', [f'execute store result score #v{a} bm.rng run data get entity @a[tag=bm.kwme,limit=1] Pos[{i}] 1000' for i, a in ((0, 'x'), (2, 'z'))] +
       [f'execute store result score #c{a} bm.rng run data get entity @s Pos[{i}] 1000' for i, a in ((0, 'x'), (2, 'z'))] +
       [f'scoreboard players operation #v{a} bm.rng -= #c{a} bm.rng' for a in 'xz'] +
       ['execute store result entity @s Motion[0] double 0.00009 run scoreboard players get #vx bm.rng',
        'execute store result entity @s Motion[2] double 0.00009 run scoreboard players get #vz bm.rng',
        'data modify entity @s Motion[1] set value 0.42d',
        'particle minecraft:electric_spark ~ ~1 ~ 0.3 0.5 0.3 0.2 16', 'playsound minecraft:item.trident.riptide_1 player @a[distance=..16] ~ ~ ~ 0.8 1.6'])
    # the switch
    fn('p59/kw/tap', ['scoreboard players operation #t bm.rng = @s bm.kwst', 'scoreboard players set @s bm.kwst 0',
                      'execute if score #t bm.rng matches ..9 run function bm:p59/kw/toggle'])
    fn('p59/kw/toggle', ['scoreboard players set @s bm.kwst 100',
                         'execute store result score #m bm.rng run scoreboard players get @s bm.kwmd',
                         'execute if score #m bm.rng matches 1 run return run function bm:p59/kw/mode_off',
                         'scoreboard players set @s bm.kwmd 1', 'function bm:p59/kw/fling_pose',
                         'playsound minecraft:block.copper_bulb.turn_on player @s ~ ~ ~ 1 1.6',
                         title('@s', 'actionbar', [T('Tendrils: ', YEL, bold=True), T('RANGED', '#7ac8ff', bold=True), T(' - they lash monsters ahead of you (double-tap sneak to switch)', 'gray')])])
    fn('p59/kw/mode_off', ['scoreboard players set @s bm.kwmd 0', 'function bm:p59/kw/fling_pose',
                           'playsound minecraft:block.copper_bulb.turn_off player @s ~ ~ ~ 1 0.8',
                           title('@s', 'actionbar', [T('Tendrils: ', YEL, bold=True), T('OFFENSE', '#ff6a5a', bold=True), T(' - melee stabs, and they drag monsters in (double-tap sneak to switch)', 'gray')])])
    fn('p59/kw/lash', ['scoreboard players set #lv bm.rng 0', 'execute if predicate bm:p59/rain run scoreboard players set #lv bm.rng 1',
                       'execute if predicate bm:p59/storm run scoreboard players set #lv bm.rng 2',
                       'execute if score #lv bm.rng matches 0 run scoreboard players set @s bm.kwcd 24', 'execute if score #lv bm.rng matches 1 run scoreboard players set @s bm.kwcd 18',
                       'execute if score #lv bm.rng matches 2 run scoreboard players set @s bm.kwcd 12',
                       'execute store result score @s bm.kwlk run random value 0..3', 'scoreboard players set @s bm.kwlt 10'] +
       [f'execute if score @s bm.kwlk matches {i} run function bm:p59/kw/pose/{k}/mid' for i, k in enumerate(KEYS)] +
       ['execute anchored eyes positioned ^ ^ ^ facing entity @e[tag=bm.kwtgt,limit=1] eyes run function bm:p59/kw/beam'])
    fn('p59/kw/beam', ['scoreboard players set #kb bm.rng 48', 'function bm:p59/kw/beam1'])
    fn('p59/kw/beam1', ['particle minecraft:dust{color:[1.0,0.92,0.3],scale:0.9} ~ ~ ~ 0.03 0.03 0.03 0 1', 'particle minecraft:electric_spark ~ ~ ~ 0.05 0.05 0.05 0.02 1',
                        'scoreboard players remove #kb bm.rng 1', 'execute if score #kb bm.rng > #kr bm.rng positioned ^ ^ ^0.5 run function bm:p59/kw/beam1'])
    fn('p59/kw/mob', ['tag @s add bm.kwhit',
                      'execute if score #lv bm.rng matches 0 run damage @s 10 minecraft:lightning_bolt by @a[tag=bm.kwme,limit=1]',
                      'execute if score #lv bm.rng matches 1 run damage @s 13 minecraft:lightning_bolt by @a[tag=bm.kwme,limit=1]',
                      'execute if score #lv bm.rng matches 2 run damage @s 16 minecraft:lightning_bolt by @a[tag=bm.kwme,limit=1]',
                      'execute if score #lv bm.rng matches 2 unless entity @a[tag=bm.kwme,distance=..6] run summon minecraft:lightning_bolt ~ ~ ~',
                      'particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.4 30', 'particle minecraft:flash{color:[1.0,0.95,0.5,1.0]} ~ ~1 ~ 0 0 0 0 1',
                      'playsound minecraft:block.copper_bulb.turn_on player @a[distance=..16] ~ ~ ~ 1 0.6',
                      'playsound minecraft:entity.lightning_bolt.impact player @a[distance=..24] ~ ~ ~ 0.5 1.6',
                      'execute if score #lv bm.rng matches 0 as @e[type=#bm:hostile,tag=!bm.npc,distance=..5,tag=!bm.kwhit,sort=nearest,limit=2] at @s run function bm:p59/kw/arc',
                      'execute if score #lv bm.rng matches 1.. as @e[type=#bm:hostile,tag=!bm.npc,distance=..6,tag=!bm.kwhit,sort=nearest,limit=3] at @s run function bm:p59/kw/arc',
                      'tag @e[tag=bm.kwhit] remove bm.kwhit'])
    fn('p59/kw/arc', ['tag @s add bm.kwhit', 'execute if score #lv bm.rng matches 0 run damage @s 5 minecraft:lightning_bolt by @a[tag=bm.kwme,limit=1]',
                      'execute if score #lv bm.rng matches 1.. run damage @s 7 minecraft:lightning_bolt by @a[tag=bm.kwme,limit=1]',
                      'particle minecraft:electric_spark ~ ~1 ~ 0.3 0.5 0.3 0.3 16',
                      'execute facing entity @e[tag=bm.kwhit,distance=0.1..7,limit=1,sort=nearest] feet run function bm:p59/kw/arcline'])
    fn('p59/kw/arcline', [f'particle minecraft:dust{{color:[1.0,0.95,0.4],scale:0.8}} ^ ^1 ^{d / 2} 0.05 0.05 0.05 0 1' for d in range(1, 12)])
    # (as the monster: pulled toward the player with Motion)
    fn('p59/kw/yank', ['execute facing entity @a[tag=bm.kwme,limit=1] feet positioned ^ ^ ^1.6 positioned ~ ~0.55 ~ run function bm:p59/kw/vec',
                       'particle minecraft:electric_spark ~ ~1 ~ 0.3 0.5 0.3 0.2 16', 'playsound minecraft:item.trident.riptide_1 player @a[distance=..16] ~ ~ ~ 0.8 1.6'])
    fn('p59/kw/vec', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.kwvec"]}'] +
       [f'execute store result score #v{a} bm.rng run data get entity @e[type=minecraft:marker,tag=bm.kwvec,limit=1] Pos[{i}] 1000' for i, a in enumerate('xyz')] +
       ['kill @e[type=minecraft:marker,tag=bm.kwvec]'] +
       [f'execute store result score #c{a} bm.rng run data get entity @s Pos[{i}] 1000' for i, a in enumerate('xyz')] +
       [f'scoreboard players operation #v{a} bm.rng -= #c{a} bm.rng' for a in 'xyz'] +
       [f'execute store result entity @s Motion[{i}] double 0.001 run scoreboard players get #v{a} bm.rng' for i, a in enumerate('xyz')])
    # sneak + jump: fling where you look (up the wall if one is right in front of you)
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.kwj minecraft.custom:minecraft.jump', 'scoreboard objectives add bm.kwt dummy',
                              'scoreboard objectives add bm.kwf dummy', 'scoreboard objectives add bm.kwlt dummy', 'scoreboard objectives add bm.kwlk dummy',
                              'scoreboard objectives add bm.kwjt dummy', 'scoreboard objectives add bm.kwmc dummy', 'scoreboard objectives add bm.kwvp dummy',
                              'scoreboard objectives add bm.kwmd dummy', 'scoreboard objectives add bm.kwst dummy', 'scoreboard objectives add bm.kwyc dummy',
                              'scoreboard objectives add bm.kwpx dummy', 'scoreboard objectives add bm.kwpy dummy', 'scoreboard objectives add bm.kwpz dummy',
                              'scoreboard players set #40 bm.rng 40', 'scoreboard players set #4 bm.rng 4']
    G.OBJECTIVES += ['bm.kwj', 'bm.kwt', 'bm.kwf', 'bm.kwlt', 'bm.kwlk', 'bm.kwjt', 'bm.kwmc', 'bm.kwvp', 'bm.kwmd', 'bm.kwst', 'bm.kwyc', 'bm.kwpx', 'bm.kwpy', 'bm.kwpz']
    tick.append(f'execute as @a[scores={{bm.kwj=1..}}] at @s run function bm:p59/kw/jump')
    tick.append('scoreboard players remove @a[scores={bm.kwf=1..}] bm.kwf 1')
    fn('p59/kw/jump', ['scoreboard players reset @s bm.kwj', f'execute unless {worn} run return 0', 'execute unless predicate bm:p20/sneaking run return 0',
                       'execute if score @s bm.kwf matches 1.. run return 0', 'execute if entity @s[tag=bm.adv] run return 0',
                       'scoreboard players set #kr bm.rng 48', 'scoreboard players set #kh bm.rng 0',
                       'execute anchored eyes positioned ^ ^ ^ run function bm:p59/kw/fray',
                       'execute if score #kh bm.rng matches 0 run scoreboard players set #kr bm.rng 32',
                       'scoreboard players set @s bm.kwf 20', 'execute if predicate bm:p59/rain run scoreboard players set @s bm.kwf 14',
                       'execute if predicate bm:p59/storm run scoreboard players set @s bm.kwf 10',
                       'tag @s add bm.kwarm', 'function bm:p59/kw/fling_pose',
                       'execute rotated ~ 0 positioned ^ ^1 ^1.2 unless block ~ ~ ~ #bm:grap_pass run return run function bm:p59/kw/fling_up',
                       'execute if score #kr bm.rng matches 33.. run tag @s add bm.kwl1',
                       'execute if score #kr bm.rng matches 17..32 run tag @s add bm.kwl2',
                       'execute if score #kr bm.rng matches ..16 run tag @s add bm.kwl3',
                       'playsound minecraft:block.chain.place player @a[distance=..16] ~ ~ ~ 1 1.4', 'particle minecraft:electric_spark ~ ~1 ~ 0.4 0.5 0.4 0.3 20'])
    fn('p59/kw/fling_up', ['tag @s add bm.kwup', 'playsound minecraft:block.chain.place player @a[distance=..16] ~ ~ ~ 1 1.2'])
    fn('p59/kw/fray', ['execute unless block ~ ~ ~ #bm:grap_pass run return run scoreboard players set #kh bm.rng 1',
                       'scoreboard players remove #kr bm.rng 1', 'execute if score #kr bm.rng matches 1.. positioned ^ ^ ^0.5 run function bm:p59/kw/fray'])
    fn('p59/kw/flung', ['tag @s remove bm.kwl1', 'tag @s remove bm.kwl2', 'tag @s remove bm.kwl3', 'tag @s remove bm.kwup', 'tag @s remove bm.kwarm'])
    tick.append(f'execute as @a[tag=bm.kwarm] unless {worn} run function bm:p59/kw/flung')
    # the snatch: dropped items within 8 drift to you; in the rain or a storm: Speed
    G.FUNCS['loop/second'][-1:-1] = [f'execute as @a[gamemode=!spectator] if {worn} at @s run function bm:p59/kw/sec']
    fn('p59/kw/sec', ['execute as @e[type=minecraft:item,distance=2..8,nbt={PickupDelay:0s}] at @s run function bm:p59/kw/snatch',
                      'execute if predicate bm:p59/rain run effect give @s minecraft:speed 2 0 true',
                      'execute if predicate bm:p59/storm run effect give @s minecraft:speed 2 1 true',
                      'execute if predicate bm:p59/storm run effect give @s minecraft:strength 2 0 true'])
    fn('p59/kw/snatch', ['particle minecraft:electric_spark ~ ~0.3 ~ 0.1 0.1 0.1 0.05 4', 'tp @s @p[distance=..9]'])

    # melee (2.43): your reach grows by 2, and each hand-to-hand blow brings both upper tendrils lunging over your shoulders -
    # a lightning stab on the one you hit (6 / rain 8 / storm 10) that pierces through to one behind it (half), about once every 0.7 s
    wjson('bm/advancement/p59/kw_melee.json', {'criteria': {'hit': {'trigger': 'minecraft:player_hurt_entity', 'conditions': {
        'player': [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'equipment': {'chest': {'predicates': {'minecraft:custom_data': '{bm:"killerwatt_tendrils"}'}}}}}],
        'damage': {'type': {'is_direct': True, 'tags': [{'id': '#minecraft:is_lightning', 'expected': False}, {'id': '#minecraft:is_projectile', 'expected': False},
                                                        {'id': '#minecraft:is_explosion', 'expected': False}]}}}}},
        'rewards': {'function': 'bm:p59/kw/melee'}})
    fn('p59/kw/melee', ['advancement revoke @s only bm:p59/kw_melee', 'execute if score @s bm.kwmc matches 1.. run return 0', 'execute if score @s bm.kwmd matches 1 run return 0',
                        'scoreboard players set @s bm.kwmc 14', 'scoreboard players operation #me bm.pid = @s bm.pid',
                        'scoreboard players set @s bm.kwlk 4', 'scoreboard players set @s bm.kwlt 14', 'scoreboard players set @s bm.kwjt 0',
                        'function bm:p59/kw/pose/ul/mid', 'function bm:p59/kw/pose/ur/mid',
                        f'execute at @s as @e[{mob},distance=..7,nbt={{HurtTime:10s}},sort=nearest,limit=1] run function bm:p59/kw/mark'])
    fn('p59/kw/mark', ['tag @s add bm.kwtg', 'scoreboard players operation @s bm.kwvp = #me bm.pid'])
    # (half a second on - once the blow's hurt-immunity has passed, so the stab adds its full damage)
    fn('p59/kw/stab_now', ['tag @s add bm.kwme',
                           'scoreboard players set #lv bm.rng 0', 'execute if predicate bm:p59/rain run scoreboard players set #lv bm.rng 1',
                           'execute if predicate bm:p59/storm run scoreboard players set #lv bm.rng 2',
                           'execute as @e[tag=bm.kwtg,distance=..8] if score @s bm.kwvp = #me bm.pid at @s run function bm:p59/kw/stab',
                           'execute as @e[tag=bm.kwtg] if score @s bm.kwvp = #me bm.pid run tag @s remove bm.kwtg', 'tag @s remove bm.kwme'])
    fn('p59/kw/stab', ['tag @s add bm.kwhit',
                       'execute if score #lv bm.rng matches 0 run damage @s 6 minecraft:lightning_bolt by @a[tag=bm.kwme,limit=1]',
                       'execute if score #lv bm.rng matches 1 run damage @s 8 minecraft:lightning_bolt by @a[tag=bm.kwme,limit=1]',
                       'execute if score #lv bm.rng matches 2 run damage @s 10 minecraft:lightning_bolt by @a[tag=bm.kwme,limit=1]',
                       'particle minecraft:electric_spark ~ ~1 ~ 0.3 0.5 0.3 0.3 20', 'particle minecraft:crit ~ ~1 ~ 0.3 0.4 0.3 0.3 10',
                       'playsound minecraft:item.trident.hit player @a[distance=..16] ~ ~ ~ 1 1.4',
                       'playsound minecraft:block.copper_bulb.turn_on player @a[distance=..16] ~ ~ ~ 0.8 1.2',
                       # the stab drives on through: one more monster just behind it
                       f'execute facing entity @a[tag=bm.kwme,limit=1] feet positioned ^ ^ ^-1.5 as @e[type=#bm:hostile,tag=!bm.npc,tag=!bm.kwhit,distance=..1.6,sort=nearest,limit=1] at @s run function bm:p59/kw/pierce',
                       'tag @e[tag=bm.kwhit] remove bm.kwhit'])
    fn('p59/kw/pierce', ['execute if score #lv bm.rng matches 0 run damage @s 3 minecraft:lightning_bolt by @a[tag=bm.kwme,limit=1]',
                         'execute if score #lv bm.rng matches 1 run damage @s 4 minecraft:lightning_bolt by @a[tag=bm.kwme,limit=1]',
                         'execute if score #lv bm.rng matches 2 run damage @s 5 minecraft:lightning_bolt by @a[tag=bm.kwme,limit=1]',
                         'particle minecraft:electric_spark ~ ~1 ~ 0.2 0.4 0.2 0.2 10'])

    # ------------------------------------------------------------------ APOPHISS'S CROWN: Serpent's Fangs on sneak + jump
    tick.append(f'execute as @a[scores={{bm.crj=1..}}] at @s run function bm:p59/crown/jump')
    fn('p59/crown/jump', ['scoreboard players reset @s bm.crj', f'execute unless items entity @s armor.head {holds % "apophiss_crown"} run return 0',
                          'execute unless predicate bm:p20/sneaking run return 0',
                          'execute if score @s bm.crcd matches 1.. run return run ' + say("The crown's power is still gathering."),
                          'execute if entity @s[tag=bm.adv] run return 0',
                          'scoreboard players set @s bm.crcd 120', 'execute unless score #tod bm.bm matches 0..12999 run scoreboard players set @s bm.crcd 60',
                          'execute at @s rotated ~ 0 run function bm:p59/crown/fangs',
                          'execute unless score #tod bm.bm matches 0..12999 at @s rotated ~ 0 run function bm:p59/crown/fangs_more'])
    fn('p59/crown/fangs', [f'summon minecraft:evoker_fangs ^ ^ ^{1.6 + i * 1.25:.2f} {{Warmup:{i * 2},Tags:["bm.cfnew"]}}' for i in range(12)] +
       ['execute as @e[type=minecraft:evoker_fangs,tag=bm.cfnew,distance=..20] run data modify entity @s Owner set from entity @a[tag=bm.crme,limit=1] UUID',
        'tag @e[type=minecraft:evoker_fangs,tag=bm.cfnew] remove bm.cfnew',
        'particle minecraft:squid_ink ~ ~1 ~ 0.5 0.6 0.5 0.05 30', 'particle minecraft:witch ~ ~1.4 ~ 0.5 0.6 0.5 0.1 20',
        'playsound minecraft:entity.evoker.cast_spell player @a[distance=..24] ~ ~ ~ 1 0.6', 'playsound minecraft:entity.ender_dragon.growl player @a[distance=..24] ~ ~ ~ 0.4 1.6'])
    fn('p59/crown/fangs_more', ['tag @s add bm.crme'] + [f'summon minecraft:evoker_fangs ^{side} ^ ^{2.2 + i * 1.4:.2f} {{Warmup:{4 + i * 2},Tags:["bm.cfnew"]}}' for side in (-1.3, 1.3) for i in range(2)] +
       ['execute as @e[type=minecraft:evoker_fangs,tag=bm.cfnew,distance=..20] run data modify entity @s Owner set from entity @a[tag=bm.crme,limit=1] UUID',
        'tag @e[type=minecraft:evoker_fangs,tag=bm.cfnew] remove bm.cfnew', 'tag @s remove bm.crme'])
    G.FUNCS['p59/crown/fangs'].insert(0, 'tag @s add bm.crme'); G.FUNCS['p59/crown/fangs'].append('tag @s remove bm.crme')
    # night: Strength, Night Vision, and the fangs come twice as often (16 of them)
    G.FUNCS['loop/second'][-1:-1] = [f'execute unless score #tod bm.bm matches 0..12999 as @a[gamemode=!spectator] if items entity @s armor.head {holds % "apophiss_crown"} run function bm:p59/crown/night']
    fn('p59/crown/night', ['effect give @s minecraft:strength 2 0 true', 'effect give @s minecraft:night_vision 15 0 true'])
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

    # in water, in the rain, or in a sea/river/beach/swamp biome: Strength, Dolphin's Grace, Conduit Power
    wjson('bm/predicate/p59/watery.json', {'condition': 'minecraft:any_of', 'terms': [
        {'condition': 'minecraft:location_check', 'predicate': {'fluid': {'fluids': '#minecraft:water'}}},
        {'condition': 'minecraft:location_check', 'offsetY': 1, 'predicate': {'fluid': {'fluids': '#minecraft:water'}}},
        {'condition': 'minecraft:all_of', 'terms': [{'condition': 'minecraft:weather_check', 'raining': True}, {'condition': 'minecraft:location_check', 'offsetY': 1.6, 'predicate': {'can_see_sky': True}}]},
        {'condition': 'minecraft:location_check', 'predicate': {'biomes': '#minecraft:is_ocean'}},
        {'condition': 'minecraft:location_check', 'predicate': {'biomes': '#minecraft:is_river'}},
        {'condition': 'minecraft:location_check', 'predicate': {'biomes': '#minecraft:is_beach'}},
        {'condition': 'minecraft:location_check', 'predicate': {'biomes': ['minecraft:swamp', 'minecraft:mangrove_swamp']}}]})
    G.FUNCS['loop/second'][-1:-1] = [f'execute as @a[gamemode=!spectator] if items entity @s weapon.mainhand {holds % "leo_trident"} at @s if predicate bm:p59/watery run function bm:p59/leo/tide',
                                     f'execute as @a[gamemode=!spectator] if items entity @s weapon.mainhand {holds % "leo_spear"} at @s if predicate bm:p59/watery run function bm:p59/leo/tide']
    fn('p59/leo/tide', ['effect give @s minecraft:strength 2 0 true', 'effect give @s minecraft:dolphins_grace 2 0 true', 'effect give @s minecraft:conduit_power 12 0 true',
                        'particle minecraft:bubble_pop ~ ~1 ~ 0.4 0.6 0.4 0.02 4'])

    # ------------------------------------------------------------------ EMMA'S BLOOMHEART (the 2.24 Bloomheart is hers): stronger by day or with her beside you
    bh = G.FUNCS['p45/bloomheart_gem/use']
    k = next(i for i, l in enumerate(bh) if l.startswith('effect give @a[distance=..8'))
    bh[k:k] = ['scoreboard players set #bb bm.rng 0', 'execute if score #tod bm.bm matches 0..12999 run scoreboard players add #bb bm.rng 1',
               'tag @s add bm.bhme', 'execute as @e[type=minecraft:cat,tag=bm.emmapet] on owner if entity @s[tag=bm.bhme] run scoreboard players set #be bm.rng 1',
               'tag @s remove bm.bhme', 'execute if score #be bm.rng matches 1 run scoreboard players add #bb bm.rng 1', 'scoreboard players set #be bm.rng 0',
               'execute if score #bb bm.rng matches 1.. run return run function bm:p59/bloom/boosted']
    fn('p59/bloom/boosted', ['effect give @a[distance=..12,gamemode=!spectator] minecraft:regeneration 12 1', 'effect give @a[distance=..12,gamemode=!spectator] minecraft:absorption 12 0',
                             'execute as @e[type=#bm:p42_ally,distance=..12] run effect give @s minecraft:regeneration 12 1',
                             'execute if score #bb bm.rng matches 2 run effect give @a[distance=..12,gamemode=!spectator] minecraft:resistance 12 0',
                             'execute if score #bb bm.rng matches 1 run scoreboard players remove @s bm.mcd4 200',
                             'execute if score #bb bm.rng matches 2 run scoreboard players remove @s bm.mcd4 400'] +
       [f'particle minecraft:cherry_leaves ^{12 * _m.sin(_m.radians(a)):.2f} ^0.3 ^{12 * _m.cos(_m.radians(a)):.2f} 0.4 0.2 0.4 0 3' for a in range(0, 360, 15)] +
       ['particle minecraft:spore_blossom_air ~ ~1 ~ 6 1 6 0 90', 'particle minecraft:heart ~ ~1.5 ~ 4 0.5 4 0 18', 'particle minecraft:end_rod ~ ~1.5 ~ 3 1 3 0.02 20',
        'playsound minecraft:block.spore_blossom.place player @a[distance=..24] ~ ~ ~ 1 0.8', 'playsound minecraft:block.amethyst_block.resonate player @a[distance=..24] ~ ~ ~ 1 1.4',
        'execute if score #bb bm.rng matches 1 run ' + say("Emma's Bloomheart flowers brightly: everyone near heals (and is shielded).", '#ff7ae0'),
        'execute if score #bb bm.rng matches 2 run ' + say("Emma's Bloomheart blazes with her beside you and the sun up!", '#ff7ae0')])

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
    T_ = {'kw_yellow': noise('#f2d42c', 18), 'kw_yellow_lt': noise('#ffec5a', 14), 'kw_white': noise('#fffbd8', 6), 'kw_green': noise('#2e9a4a', 10), 'kw_teal': noise('#1d7a5c', 8),
          'ap_black': noise('#1c1a20', 6), 'ap_emerald': noise('#1fae4c', 10), 'ap_emerald_lt': noise('#5cf08a', 10), 'ap_ruby': noise('#c81828', 10),
          'ap_ruby_lt': noise('#ff6a70', 8), 'ap_gold': noise('#e0b030', 14), 'ap_fur': noise('#f2f0ea', 6)}
    # sparks on the yellow, a sheen on the black, facets on the gems, grey speckles in the fur
    for y in range(16):
        for x in range(16):
            if rnd.random() < 0.10: T_['kw_yellow'].putpixel((x, y), hexc('#fff8b0'))
            if rnd.random() < 0.06: T_['kw_yellow'].putpixel((x, y), hexc('#c89a10'))
            if (x + y) % 7 == 0: T_['ap_black'].putpixel((x, y), hexc('#3a3842'))
            if (x + y) % 5 == 0 or (x - y) % 5 == 0: T_['ap_emerald'].putpixel((x, y), hexc('#0d6a2c' if (x + y) % 2 else '#7affa8'))
            if (x - y) % 4 == 0: T_['ap_ruby'].putpixel((x, y), hexc('#ff5060'))
            if rnd.random() < 0.12: T_['ap_fur'].putpixel((x, y), hexc(rnd.choice(('#8a8a90', '#a8a8ae', '#6c6c72'))))
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
        KT = {'y': 'kw_yellow', 'l': 'kw_yellow_lt', 'g': 'kw_green', 't': 'kw_teal', 'w': 'kw_white'}
        # a flat electric blade from point p to q (x,y in the z-plane at depth z): width w, thickness d, rotated about z at p
        def blade(p, q, w, t, z=8, d=1.0):
            L = math.hypot(q[0] - p[0], q[1] - p[1]); a = math.degrees(math.atan2(-(q[0] - p[0]), q[1] - p[1]))
            return c((p[0] - w / 2, p[1], z - d / 2), (p[0] + w / 2, p[1] + L + 0.3, z + d / 2), t, ('z', round(a, 2), (p[0], p[1], z)))
        def bolt(pts, ws, z=8, d=1.0, tex='yl'):
            return [blade(pts[n], pts[n + 1], ws[n], tex[n % len(tex)], z, d) for n in range(len(pts) - 1)]
        def barb(p, ang, L=2.4, t='w', z=8):
            return c((p[0] - 0.3, p[1], z - 0.3), (p[0] + 0.3, p[1] + L, z + 0.3), t, ('z', ang, (p[0], p[1], z)))
        # KillerWatt's tendrils (GUI): a green spine plate, four jagged lightning blades fanning out of it
        kw = [c((5.5, 1, 6.5), (10.5, 7, 9.5), 'g'), c((6.5, 2, 9.4), (9.5, 6, 10), 't'), c((7.3, 2.6, 9.9), (8.7, 5.4, 10.3), 'w')]
        for sx in (-1, 1):
            for up, pts in ((1, [(8, 6), (10.5, 9), (9.5, 10.5), (12.5, 13.5), (11.8, 15), (14.5, 15.8)]),
                            (0, [(8, 3), (11, 4), (10.5, 5.5), (13.5, 6), (13, 7.5), (15.5, 7.2)])):
                P = [(8 + sx * (x - 8), y) for x, y in pts]
                kw += bolt(P, (1.6, 1.0, 1.4, 0.9, 0.8), 8, 1.0)
                kw.append(barb(P[2], -sx * 60, 1.8))
        model('killerwatt_tendrils', KT, kw, HELD)
        # worn: each tendril is two blades with a sharp elbow between - kw_tb (base, 12 long) and kw_tt (tip, 17 long) along +y from (8,8,8)
        # each is a zig-zag bolt: sharp kinks, white-hot barbs on the corners, endpoints back on the axis so the elbow joins
        tb = [c((6.4, 6.4, 6.4), (9.6, 9.0, 9.6), 'g'), c((6.9, 8.8, 6.9), (9.1, 9.8, 9.1), 't')]
        P = [(8, 9), (10.0, 12.6), (6.8, 15.2), (9.2, 18.4), (8, 20)]
        tb += bolt(P, (2.6, 1.8, 2.4, 1.8)); tb += [barb(P[1], -55), barb(P[2], 60), barb(P[3], -50, 2.0)]
        tb.append(c((7, 19.2, 7), (9, 20.6, 9), 't'))                                           # elbow knuckle
        model('kw_tb', KT, tb, {'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]}})
        tt = []
        P = [(8, 8.2), (6.0, 12.4), (9.6, 15.6), (6.6, 19.8), (9.4, 22.2), (8.6, 24.0), (6.8, 25.2)]
        tt += bolt(P, (2.2, 1.7, 2.0, 1.5, 1.0, 0.7)); tt += [barb(P[1], 55), barb(P[2], -60), barb(P[3], 55, 2.0), barb(P[4], -40, 1.6)]
        tt.append(c((6.4, 24.6, 7.6), (7.2, 25.8, 8.4), 'w'))                                   # the hooked point
        model('kw_tt', KT, tt, {'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]}})
        # Apophiss's crown (worn): black band on speckled white fur, ball-tipped spikes of uneven height,
        # a great faceted emerald set inside rising over the band, a diamond ruby on the tall front spike, oval rubies in gold
        cr = [c((2.4, 13.6, 2.4), (13.6, 15.2, 13.6), 'f'),                                    # fur trim
              c((3, 15.0, 3), (13, 18.0, 3.8), 'k'), c((3, 15.0, 12.2), (13, 18.0, 13), 'k'),
              c((3, 15.0, 3.8), (3.8, 18.0, 12.2), 'k'), c((12.2, 15.0, 3.8), (13, 18.0, 12.2), 'k'),
              c((3.4, 17.6, 3.4), (12.6, 18.2, 12.6), 'k')]                                      # inner floor
        # emerald: a stacked faceted gem inside, rising above the band
        cr += [c((5.2, 17.8, 5.2), (10.8, 20.6, 10.8), 'e'), c((5.8, 20.4, 5.8), (10.2, 22.0, 10.2), 'e', ('y', 45, (8, 21, 8))),
               c((6.6, 21.8, 6.6), (9.4, 23.2, 9.4), 'v'), c((7.3, 23.0, 7.3), (8.7, 23.8, 8.7), 'v', ('y', 45, (8, 23.4, 8)))]
        # spikes round the band (front is model north, z=3): (x, z, height)
        SP = [(8, 3.4, 6.6), (5.0, 3.4, 4.0), (11.0, 3.4, 4.0), (3.4, 5.6, 5.0), (12.6, 5.6, 5.0), (3.4, 10.0, 3.4), (12.6, 10.0, 3.4),
              (5.0, 12.6, 4.4), (11.0, 12.6, 4.4), (8, 12.6, 5.4)]
        for x, z, h in SP:                                                              # a tapering spike, then a ball
            w = 1.3 if h > 6 else 1.1
            cr += [c((x - w / 2, 17.8, z - w / 2), (x + w / 2, 17.8 + h * 0.55, z + w / 2), 'k'),
                   c((x - 0.35, 17.8 + h * 0.55, z - 0.35), (x + 0.35, 17.8 + h, z + 0.35), 'k'),
                   c((x - 0.75, 17.6 + h, z - 0.75), (x + 0.75, 19.0 + h, z + 0.75), 'k'), c((x - 0.55, 17.4 + h, z - 0.95), (x + 0.55, 19.2 + h, z + 0.95), 'k'),
                   c((x - 0.95, 17.4 + h, z - 0.55), (x + 0.95, 19.2 + h, z + 0.55), 'k')]
        # the diamond ruby on the tall front spike, gold-set oval rubies on the band
        cr += [c((7.0, 19.0, 2.3), (9.0, 21.0, 2.9), 'r', ('z', 45, (8, 20, 2.6))), c((7.45, 19.45, 2.05), (8.55, 20.55, 2.35), 'o', ('z', 45, (8, 20, 2.2)))]
        for x, z, face in ((5.0, 2.9, 'n'), (11.0, 2.9, 'n'), (2.9, 7.5, 'w'), (13.1, 7.5, 'e'), (8.0, 13.1, 's')):
            if face in 'ns':
                dz = -0.35 if face == 'n' else 0.35
                cr += [c((x - 1.0, 15.6, z + dz - 0.2), (x + 1.0, 17.6, z + dz + 0.2), 'a'), c((x - 0.6, 15.9, z + 2 * dz - 0.2), (x + 0.6, 17.3, z + 2 * dz + 0.2), 'r')]
            else:
                dx = -0.35 if face == 'w' else 0.35
                cr += [c((x + dx - 0.2, 15.6, z - 1.0), (x + dx + 0.2, 17.6, z + 1.0), 'a'), c((x + 2 * dx - 0.2, 15.9, z - 0.6), (x + 2 * dx + 0.2, 17.3, z + 0.6), 'r')]
        model('apophiss_crown', {'k': 'ap_black', 'e': 'ap_emerald', 'v': 'ap_emerald_lt', 'r': 'ap_ruby', 'o': 'ap_ruby_lt', 'a': 'ap_gold', 'f': 'ap_fur'}, cr, R2.GUI_3D)
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

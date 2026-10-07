"""2.23: the Hollow King's tools wake up - abilities for the blade, pick, axe, spade and bow, plus the Reaper's Sickle (hoe) and
the Wings of the Damned (elytra). All of them are in the Hollow King's vault.

- SOULREAVER (sword): right-click - Soul Rend: a sweep that tears at everything in front of you (5 blocks), withering it and
  healing you a little for each one it hits. 8 s.
- GRAVEDIGGER'S MAW (pickaxe) and BARROW SPADE (shovel): right-click - Excavate the 3 x 3 face you're looking at (whatever the
  tool can dig; containers are left alone). Sneak + right-click: switch Fortune / Silk Touch.
- HEADSMAN'S GRIEF (axe): a real weapon (Sharpness, Smite, Looting V, Fire Aspect III). Chop the bottom of a tree and the whole
  tree falls (natural trees only - log houses are safe). Sneak + right-click: switch Fortune / Silk Touch.
- REAPER'S SICKLE (hoe): right-click - Harvest Moon: crops within 6 blocks ripen at once. 30 s. Sneak + right-click: Fortune /
  Silk Touch. A fine scythe in a fight, too.
- WITHERSTRING (bow): arrows trail souls and wither what they hit (Wither II).
- WINGS OF THE DAMNED (elytra): unbreakable, as tough as a chestplate (+6 armour), and you never take damage from flying into a
  wall. Hold sneak while gliding: the wings drive you on (no rockets needed). On the ground, crouch and look straight up for a
  second: launch. A trail of souls, wither-smoke and flame follows you."""
import math
from items import ITEMS, gear, attr, ench, T, weapon_attrs
from useitem import hold, HOLD
from p2.regalia import COL, evil_name

MODES = {  # iid: (fortune-mode enchantments, silk-mode enchantments)
    'conq_pick': (ench(efficiency=10, fortune=6), ench(efficiency=10, silk_touch=1)),
    'conq_axe': (ench(sharpness=10, efficiency=10, smite=8, looting=5, fire_aspect=3, fortune=4),
                 ench(sharpness=10, efficiency=10, smite=8, looting=5, fire_aspect=3, silk_touch=1)),
    'conq_shovel': (ench(efficiency=10, fortune=4), ench(efficiency=10, silk_touch=1)),
    'conq_hoe': (ench(efficiency=10, fortune=5), ench(efficiency=10, silk_touch=1)),
}
LOGS = ['oak_log', 'spruce_log', 'birch_log', 'jungle_log', 'acacia_log', 'dark_oak_log', 'mangrove_log', 'cherry_log', 'pale_oak_log',
        'crimson_stem', 'warped_stem']
CROPS = [('wheat', 7), ('carrots', 7), ('potatoes', 7), ('beetroots', 3), ('nether_wart', 3), ('melon_stem', 7), ('pumpkin_stem', 7),
         ('sweet_berry_bush', 3), ('pitcher_crop', 4)]
TOOL_INFO = {
    'conq_blade': ('netherite_sword', 'Soulreaver', ["Wrenched from the Hollow King's throne.", ('Strength I while held. Unbreakable.', 'blue'),
                   ('Right-click: Soul Rend - wither everything', 'blue'), ('in front of you, and drink a little of it. (8 s)', 'blue')]),
    'conq_pick': ('netherite_pickaxe', "Gravedigger's Maw", ["Wrenched from the Hollow King's throne.", ('Haste II while held. Unbreakable.', 'blue'),
                  ('Right-click: Excavate the 3 x 3 face you look at.', 'blue'), ('Sneak + right-click: Fortune / Silk Touch.', 'blue')]),
    'conq_axe': ('netherite_axe', "Headsman's Grief", ["Wrenched from the Hollow King's throne.", ('Strength I while held. Unbreakable.', 'blue'),
                 ('Chop a tree at its foot: the whole tree falls.', 'blue'), ('Sneak + right-click: Fortune / Silk Touch.', 'blue'),
                 ('Looting V and Fire Aspect III in a fight.', 'blue')]),
    'conq_shovel': ('netherite_shovel', 'Barrow Spade', ["Wrenched from the Hollow King's throne.", ('Haste II while held. Unbreakable.', 'blue'),
                    ('Right-click: Excavate the 3 x 3 face you look at.', 'blue'), ('Sneak + right-click: Fortune / Silk Touch.', 'blue')]),
    'conq_hoe': ('netherite_hoe', "Reaper's Sickle", ["The Hollow King's harvest blade.", ('Unbreakable.', 'blue'),
                 ('Right-click: Harvest Moon - crops within', 'blue'), ('6 blocks ripen at once. (30 s)', 'blue'),
                 ('Sneak + right-click: Fortune / Silk Touch.', 'blue')]),
}


def register():
    from p2.p2items import CONQ_TOOLS
    base_en = {iid: en for iid, _b, _n, en, _w, _x in CONQ_TOOLS}
    for iid, (base, nm, lore) in TOOL_INFO.items():
        en = MODES[iid][0] if iid in MODES else base_en[iid]
        if iid == 'conq_hoe':
            attrs = [attr('attack_damage', 8, 'mainhand', ident='minecraft:base_attack_damage'), attr('attack_speed', -2.6, 'mainhand', ident='minecraft:base_attack_speed')]
        else:
            wb = {'conq_blade': ('netherite_sword', 5), 'conq_pick': ('netherite_pickaxe', 0), 'conq_axe': ('netherite_axe', 4), 'conq_shovel': None}[iid]
            attrs = weapon_attrs(*wb) if wb else None
        gear(iid, base, nm, COL, lore, en, 3, attrs=attrs, extra=dict(hold('none'), **{'minecraft:unbreakable': {}}),
             custom_extra={'bm_held': iid}, bold=True)
        evil_name(iid, nm)
        HOLD[iid] = f'bm:p2/ht/{iid[5:]}'
    bow = ITEMS['conq_bow']['comps']
    bow['minecraft:enchantments'] = dict(bow['minecraft:enchantments'], **{'bm:withering_shot': 1})
    bow['minecraft:lore'][1:1] = [T('Its arrows trail souls and wither', 'blue'), T('what they strike (Wither II).', 'blue')]
    gear('hollow_wings', 'elytra', 'Wings of the Damned', COL,
         ['Torn from the Hollow King\'s back.', ('+6 Armour. Unbreakable. Flying into a wall', 'blue'), ('never hurts you.', 'blue'),
          ('Hold sneak while gliding: the wings drive you on.', 'blue'), ('On the ground, crouch and look straight up', 'blue'),
          ('for a second: launch.', 'blue'), ('A trail of souls, wither-smoke and flame.', 'dark_purple')],
         {'bm:damned_wings': 1}, 3, attrs=[attr('armor', 6, 'chest', ident='minecraft:armor.chestplate'), attr('armor_toughness', 2, 'chest', ident='minecraft:armor.chestplate_toughness')],
         extra={'minecraft:unbreakable': {}}, bold=True)
    evil_name('hollow_wings', 'Wings of the Damned')


register()


def generate(G, B=None):
    fn, wjson, title = G.fn, G.wjson, G.title
    holds = '*[minecraft:custom_data~{bm:"%s"}]'
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    near = 'gamemode=!creative,gamemode=!spectator'
    fast, second, load, tick = [], [], [], []
    objs = ['bm.htc', 'bm.hhoe', 'bm.ewb', 'bm.ewl', 'bm.ewg'] + [f'bm.ml_{l[:6]}' for l in LOGS]
    load += [f'scoreboard objectives add {o} dummy' for o in objs[:5]]
    load += [f'scoreboard objectives add bm.ml_{l[:6]} minecraft.mined:minecraft.{l}' for l in LOGS]
    G.OBJECTIVES += objs

    # ---------------- Fortune / Silk Touch (sneak + right-click on the pick, axe, spade, sickle)
    for iid, (fort, silk) in MODES.items():
        for name, en, flag in (('silk', silk, 1), ('fortune', fort, 0)):
            wjson(f'bm/item_modifier/p2/ht/{iid}_{name}.json', [
                {'function': 'minecraft:set_components', 'components': {'minecraft:enchantments': en}},
                {'function': 'minecraft:set_custom_data', 'tag': f'{{bm_silk:{flag}b}}'}])
        fn(f'p2/ht/mode_{iid}', [f'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{{bm_silk:1b}}] run return run function bm:p2/ht/mode_{iid}_f',
                                 f'item modify entity @s weapon.mainhand bm:p2/ht/{iid}_silk', 'playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1.4',
                                 say('Silk Touch.', '#c8a0ff')])
        fn(f'p2/ht/mode_{iid}_f', [f'item modify entity @s weapon.mainhand bm:p2/ht/{iid}_fortune', 'playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 0.9',
                                   say('Fortune.', '#ffd23f')])

    # ---------------- Excavate (pick / spade): the 3 x 3 face in front, mined with the tool in hand (its Fortune or Silk Touch)
    for iid, tag in (('conq_pick', 'pickaxe'), ('conq_shovel', 'shovel')):
        short = iid[5:]
        fn(f'p2/ht/{short}', [f'execute unless items entity @s weapon.mainhand {holds % iid} run return 0',
                              f'execute if predicate bm:p20/sneaking run return run function bm:p2/ht/mode_{iid}',
                              'execute unless function bm:p37/allowed run return run ' + say('The walls here are warded.'),
                              'scoreboard players set #ray bm.rng 24', 'scoreboard players set #dug bm.rng 0',
                              f'execute anchored eyes positioned ^ ^ ^ run function bm:p2/ht/ray_{tag}',
                              'execute if score #dug bm.rng matches 0 run return run ' + say('Look at something to dig (within 5 blocks).'),
                              'playsound minecraft:block.stone.break player @a[distance=..16] ~ ~ ~ 1 0.6'])
        fn(f'p2/ht/ray_{tag}', [f'execute unless block ~ ~ ~ #bm:grap_pass run return run function bm:p2/ht/face_{tag}',
                                'scoreboard players remove #ray bm.rng 1', f'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p2/ht/ray_{tag}'])
        fn(f'p2/ht/face_{tag}', [f'execute positioned ^{dx} ^{dy} ^ align xyz positioned ~0.5 ~0.5 ~0.5 run function bm:p2/ht/dig_{tag}' for dx in (-1, 0, 1) for dy in (-1, 0, 1)])
        fn(f'p2/ht/dig_{tag}', [f'execute unless block ~ ~ ~ #minecraft:mineable/{tag} run return 0', 'execute if data block ~ ~ ~ id run return 0',
                                'loot spawn ~ ~ ~ mine ~ ~ ~ mainhand', 'setblock ~ ~ ~ minecraft:air', 'scoreboard players add #dug bm.rng 1',
                                'particle minecraft:sculk_soul ~ ~ ~ 0.3 0.3 0.3 0.01 2'])

    # ---------------- Timber (axe): a natural tree falls whole when its foot is chopped
    fn('p2/ht/axe', ['execute unless items entity @s weapon.mainhand ' + holds % 'conq_axe' + ' run return 0',
                     'execute if predicate bm:p20/sneaking run return run function bm:p2/ht/mode_conq_axe',
                     say('Chop a tree at its foot to fell it. Sneak + right-click: Fortune / Silk Touch.')])
    chopped = ' '.join(f'unless score @s bm.ml_{l[:6]} matches 1..' for l in LOGS)
    tick.append('execute as @a[gamemode=!spectator] if items entity @s weapon.mainhand ' + holds % 'conq_axe' + ' at @s run function bm:p2/ht/axe_tick')
    fn('p2/ht/axe_tick', [f'execute {chopped} run return 0'] + [f'scoreboard players reset @s bm.ml_{l[:6]}' for l in LOGS] +
       ['execute unless function bm:p37/allowed run return 0', 'scoreboard players set #ray bm.rng 30',
        'execute anchored eyes positioned ^ ^ ^ run function bm:p2/ht/tray'])
    # the chopped log is gone: the first log just above the line of sight is the rest of the trunk
    fn('p2/ht/tray', ['execute if block ~ ~1 ~ #minecraft:logs align xyz positioned ~0.5 ~1.5 ~0.5 run return run function bm:p2/ht/tree',
                      'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p2/ht/tray'])
    fn('p2/ht/tree', ['scoreboard players set #lf bm.rng 0', 'scoreboard players set #ty bm.rng 0', 'function bm:p2/ht/leafy',
                      'execute if score #lf bm.rng matches 0 run return 0',
                      'scoreboard players set #tc bm.rng 0', 'function bm:p2/ht/fell',
                      'playsound minecraft:block.wood.break player @a[distance=..24] ~ ~ ~ 1.5 0.5', 'playsound minecraft:entity.wither.break_block player @a[distance=..24] ~ ~ ~ 0.4 1.2'])
    fn('p2/ht/leafy', [f'execute positioned ~{dx} ~ ~{dz} if block ~ ~ ~ #minecraft:leaves[persistent=false] run return run scoreboard players set #lf bm.rng 1'
        for dx in (-2, -1, 0, 1, 2) for dz in (-2, -1, 0, 1, 2)] +
       ['scoreboard players add #ty bm.rng 1', 'execute if score #ty bm.rng matches ..14 positioned ~ ~1 ~ run function bm:p2/ht/leafy'])
    nb = [(dx, dy, dz) for dy in (0, 1) for dx in (-1, 0, 1) for dz in (-1, 0, 1) if (dx, dy, dz) != (0, 0, 0)] + [(0, -1, 0)]
    fn('p2/ht/fell', ['execute unless block ~ ~ ~ #minecraft:logs run return 0', 'execute if score #tc bm.rng matches 200.. run return 0',
                      'loot spawn ~ ~ ~ mine ~ ~ ~ mainhand', 'setblock ~ ~ ~ minecraft:air', 'scoreboard players add #tc bm.rng 1',
                      'particle minecraft:sculk_soul ~ ~ ~ 0.3 0.3 0.3 0.01 1'] +
       [f'execute positioned ~{dx} ~{dy} ~{dz} if block ~ ~ ~ #minecraft:logs run function bm:p2/ht/fell' for dx, dy, dz in nb])

    # ---------------- Harvest Moon (sickle)
    fn('p2/ht/hoe', ['execute unless items entity @s weapon.mainhand ' + holds % 'conq_hoe' + ' run return 0',
                     'execute if predicate bm:p20/sneaking run return run function bm:p2/ht/mode_conq_hoe',
                     'execute if score @s bm.hhoe matches 1.. run return run ' + title('@s', 'actionbar', [T('The harvest moon is still rising... ', 'gray'),
                                                                                                         {'score': {'name': '@s', 'objective': 'bm.hhoe'}, 'color': 'white'}, T(' s', 'gray')]),
                     'scoreboard players set @s bm.hhoe 30'] +
       [f'fill ~-6 ~-2 ~-6 ~6 ~2 ~6 minecraft:{c}[age={a}] replace minecraft:{c}' for c, a in CROPS] +
       ['particle minecraft:happy_villager ~ ~0.5 ~ 5 1 5 0 80', 'particle minecraft:sculk_soul ~ ~0.5 ~ 5 0.5 5 0.01 30',
        'playsound minecraft:item.bone_meal.use player @a[distance=..16] ~ ~ ~ 1 0.6', 'playsound minecraft:block.sculk_catalyst.bloom player @a[distance=..16] ~ ~ ~ 1 0.8',
        say('The harvest moon rises: everything ripens.', '#9a5ae0')])
    second.append('scoreboard players remove @a[scores={bm.hhoe=1..}] bm.hhoe 1')

    # ---------------- Soul Rend (blade)
    arc = [f'particle minecraft:sculk_soul ^{r * math.sin(math.radians(a)):.2f} ^1.1 ^{r * math.cos(math.radians(a)):.2f} 0.05 0.05 0.05 0.01 1'
           for r in (2.0, 3.5, 5.0) for a in range(-60, 61, 15)]
    fn('p2/ht/blade', ['execute unless items entity @s weapon.mainhand ' + holds % 'conq_blade' + ' run return 0',
                       'execute if score @s bm.htc matches 1.. run return run ' + title('@s', 'actionbar', [T('Soul Rend gathers... ', 'gray'),
                                                                                                          {'score': {'name': '@s', 'objective': 'bm.htc'}, 'color': 'white'}, T(' s', 'gray')]),
                       'scoreboard players set @s bm.htc 8', 'tag @s add bm.htme', 'scoreboard players set #rend bm.rng 0',
                       'execute rotated ~ 0 run function bm:p2/ht/rend_arc',
                       f'execute rotated ~ 0 positioned ^ ^ ^2.5 as @e[distance=..3,type=!minecraft:player,type=!#bm:p44_nonmob,tag=!bm.npc,tag=!bm.wilfrey,tag=!bm.wil_body,tag=!bm.frogpet,tag=!bm.merc,tag=!bm.cecilpet] at @s run function bm:p2/ht/rend_hit',
                       f'execute rotated ~ 0 positioned ^ ^ ^2.5 as @a[distance=..3,tag=!bm.htme,{near}] at @s run function bm:p2/ht/rend_hit',
                       'tag @s remove bm.htme',
                       'playsound minecraft:entity.wither.shoot player @a[distance=..24] ~ ~ ~ 0.8 1.4', 'playsound minecraft:item.trident.riptide_1 player @a[distance=..24] ~ ~ ~ 0.8 0.6'])
    fn('p2/ht/rend_arc', arc)
    fn('p2/ht/rend_hit', ['damage @s 12 minecraft:magic by @a[tag=bm.htme,limit=1]', 'effect give @s minecraft:wither 6 1',
                          'execute as @a[tag=bm.htme,limit=1] run effect give @s minecraft:instant_health 1 0 true',
                          'particle minecraft:soul ~ ~1 ~ 0.3 0.5 0.3 0.03 8'])
    second.append('scoreboard players remove @a[scores={bm.htc=1..}] bm.htc 1')

    # ---------------- Witherstring: soul-trailing, withering arrows
    base = {'anvil_cost': 8, 'max_level': 1, 'weight': 1, 'min_cost': {'base': 1, 'per_level_above_first': 0}, 'max_cost': {'base': 1, 'per_level_above_first': 0}}
    wjson('bm/enchantment/withering_shot.json', dict(base, description=T('Withering Shot', COL), slots=['mainhand'], supported_items='#minecraft:enchantable/bow', effects={
        'minecraft:projectile_spawned': [{'effect': {'type': 'minecraft:run_function', 'function': 'bm:p2/ht/arrow'}}],
        'minecraft:post_attack': [{'affected': 'victim', 'enchanted': 'attacker', 'effect': {'type': 'minecraft:apply_mob_effect', 'to_apply': 'minecraft:wither',
                                   'min_duration': 6.0, 'max_duration': 6.0, 'min_amplifier': 1.0, 'max_amplifier': 1.0}}]}))
    fn('p2/ht/arrow', ['tag @s add bm.wsarrow'])
    fast.append('execute as @e[tag=bm.wsarrow] at @s run function bm:p2/ht/arrow_fx')
    fn('p2/ht/arrow_fx', ['execute if entity @s[nbt={inGround:1b}] run return run tag @s remove bm.wsarrow',
                          'particle minecraft:soul ~ ~ ~ 0.05 0.05 0.05 0.01 2', 'particle minecraft:smoke ~ ~ ~ 0.05 0.05 0.05 0.01 1'])

    # ---------------- Wings of the Damned: wall-proof, sneak-boost, crouch-and-look-up launch, a trail
    flying = {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:flags': {'is_fall_flying': True}}}
    wjson('bm/enchantment/damned_wings.json', dict(base, description=T('Damned Wings', COL), slots=['chest'], supported_items='#minecraft:enchantable/chest_armor', effects={
        'minecraft:damage_immunity': [{'effect': {}, 'requirements': {'condition': 'minecraft:damage_source_properties', 'predicate': {
            'tags': [{'id': '#bm:p44_wall', 'expected': True}]}}}],
        'minecraft:tick': [
            {'effect': {'type': 'minecraft:apply_impulse', 'direction': [0.0, 0.0, 1.0], 'coordinate_scale': [1.0, 1.0, 1.0], 'magnitude': 0.07},
             'requirements': {'condition': 'minecraft:all_of', 'terms': [flying, {'condition': 'minecraft:entity_scores', 'entity': 'this', 'scores': {'bm.ewb': 1}},
                                                                         {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:movement': {'speed': {'max': 30.0}}}}]}},
            {'effect': {'type': 'minecraft:apply_impulse', 'direction': [0.0, 0.0, 1.0], 'coordinate_scale': [0.0, 1.0, 0.0], 'magnitude': 0.7},   # along the look (straight up), vertical part only
             'requirements': {'condition': 'minecraft:entity_scores', 'entity': 'this', 'scores': {'bm.ewl': {'min': 1}}}}]}))
    wjson('bm/tags/damage_type/p44_wall.json', {'values': ['minecraft:fly_into_wall']})
    wings = holds % 'hollow_wings'
    tick += [f'execute as @a[gamemode=!spectator] if items entity @s armor.chest {wings} at @s run function bm:p2/ht/wings',
             'scoreboard players remove @a[scores={bm.ewl=1..}] bm.ewl 1']
    fn('p2/ht/wings', ['scoreboard players set @s bm.ewb 0',
                       'execute if predicate bm:p2/ht_gliding if predicate bm:p20/sneaking run scoreboard players set @s bm.ewb 1',
                       'execute if predicate bm:p2/ht_gliding run function bm:p2/ht/trail',
                       'execute if predicate bm:p2/ht_gliding run return run scoreboard players set @s bm.ewg 0',
                       'execute unless predicate bm:p20/sneaking run return run scoreboard players set @s bm.ewg 0',
                       'execute unless entity @s[x_rotation=-90..-60] run return run scoreboard players set @s bm.ewg 0',
                       'scoreboard players add @s bm.ewg 1', 'execute if score @s bm.ewg matches 5..19 run particle minecraft:soul ~ ~0.2 ~ 0.4 0.1 0.4 0.02 2',
                       'execute if score @s bm.ewg matches 20 run function bm:p2/ht/launch'])
    wjson('bm/predicate/p2/ht_gliding.json', flying)
    fn('p2/ht/launch', ['scoreboard players set @s bm.ewl 2', 'particle minecraft:soul_fire_flame ~ ~0.2 ~ 0.6 0.1 0.6 0.1 40', 'particle minecraft:large_smoke ~ ~0.2 ~ 0.6 0.1 0.6 0.05 20',
                        'playsound minecraft:entity.wither.shoot player @a[distance=..24] ~ ~ ~ 1 0.6', 'playsound minecraft:entity.phantom.flap player @a[distance=..24] ~ ~ ~ 1.5 0.6',
                        say('The wings throw you skyward - jump to glide.', COL)])
    fn('p2/ht/trail', ['particle minecraft:soul ^ ^0.6 ^-0.8 0.15 0.15 0.15 0.01 2', 'particle minecraft:soul_fire_flame ^0.4 ^0.8 ^-0.6 0.05 0.05 0.05 0.01 1',
                       'particle minecraft:soul_fire_flame ^-0.4 ^0.8 ^-0.6 0.05 0.05 0.05 0.01 1', 'particle minecraft:flame ^ ^0.6 ^-1 0.1 0.1 0.1 0.01 1',
                       'particle minecraft:dust{color:[0.1,0.05,0.12],scale:1.6} ^ ^0.7 ^-1.2 0.2 0.2 0.2 0 2',
                       'execute if score @s bm.ewb matches 1 run particle minecraft:large_smoke ^ ^0.6 ^-1.2 0.1 0.1 0.1 0.02 2'])
    return {'fast': fast, 'second': second, 'load': load, 'tick': tick}

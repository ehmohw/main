"""Phase 1.27 / 2.20 (part 2): the Headless Horseman, and his head.

THE HEADLESS HORSEMAN - a roaming boss of the Overworld night
- Nobody sees him for the first 15 days of a world. After that he rides out very rarely on an ordinary night, and far more
  often under a full moon or a new moon. He appears about 24 blocks from someone standing under open sky; everyone within
  30 blocks hears the cave stir and feels it: "You sense an evil presence nearby..."
- A towering, headless rider (bigger than any player, 360 health, Resistance and Fire Resistance) on a huge, fast
  Hellsteed. He hunts from 96 blocks away, breathes fire from the stump of his neck, charges with his spear, and calls up
  Pumpkin Thralls (skeletons with lit pumpkin heads). At half health his fire roars higher: Strength, more speed, a ring of
  flame. Flames, smoke and falling ash follow him and his steed; the night around him laughs and moans.
- He rides away at dawn (or when nobody is left within 128 blocks). Kill him for Tokens, Medallions, a Trophy - and,
  always (2.34), HIS HEAD.

THE HORSEMAN'S HEAD - a weapon in four classes (2.32); it can't be placed
- OFFENSE, the Horseman's Head: heavy melee that sets victims alight; hold right-click for a short, fierce stream of fire
  (5 s, then 10 s to rekindle); sneak + hold to charge a FIRE BLAST (let go to loose it; it never breaks blocks).
- DEFENSE, the Soulfire Head: blows slow and weaken; hold right-click for a FROST WARD (Resistance II, no knockback,
  attackers chilled); sneak + hold: a Frost Blast.
- RANGED, the Venomfire Head: a weak club; hold right-click for VENOM BOLTS (40 blocks, poison / wither for the undead);
  sneak + hold, let go: a lobbed PLAGUE BURST that leaves a poison cloud.
- SUPPORT, the Hallowed Head: a healing beam (or you, if nobody's in it), a Regeneration circle, a burst of life.
- Kill monsters with it to stoke it; when it's full, sneak + look straight down + right-click: a NOVA (Hellfire hits
  harder, Glacial freezes for 3 s and shields you, Venom poisons). Undead killed with it drop extra experience.
- Night: Night Vision, x1.5 damage. Full/new moon: x2, faster cooldowns. Blood Moon: x2.5, reach, Strength, Speed, Regen.
- Off hand + look straight up + right-click with a catalyst: Blaze Rod - Offense, Armadillo Scute - Defense, Breeze Rod -
  Ranged, Heartstone - Support (the old lanterns still work: Lantern, Soul Lantern, Copper Lantern)."""
import math
from items import item, attr, T, TOTEM
from useitem import hold, HOLD_REPEAT
from nbt import snbt, B, F, D, Int

HP = 360
GRACE_DAYS = 15
ODDS_NIGHT, ODDS_MOON = 1500, 90            # 1 in N, every 20 seconds of night
ORANGE = '#ff7a1a'
HEAD = '*[minecraft:custom_data~{bm_head:1b}]'
# variant: (iid, name, colour, enchantment, ray particles, damage type)
VARIANTS = {1: ('horseman_head', "Horseman's Head", ORANGE, 'hellfire_edge', 'minecraft:flame', 'bm:hellfire'),
            2: ('soul_head', 'Soulfire Head', '#5ad8ff', 'soulfrost_edge', 'minecraft:soul_fire_flame', 'bm:soulfrost'),
            3: ('venom_head', 'Venomfire Head', '#7aff4a', 'venom_edge', 'minecraft:copper_fire_flame', 'bm:venomfire'),
            4: ('hallowed_head', 'Hallowed Head', '#ff8ac8', None, 'minecraft:end_rod', 'bm:hallowed')}
COPPER = ['copper_lantern', 'exposed_copper_lantern', 'weathered_copper_lantern', 'oxidized_copper_lantern', 'waxed_copper_lantern',
          'waxed_exposed_copper_lantern', 'waxed_weathered_copper_lantern', 'waxed_oxidized_copper_lantern']
FOES_EXTRA = ['zombified_piglin', 'piglin', 'warden', 'wither', 'elder_guardian', 'ender_dragon']
ALLIES = ['villager', 'wandering_trader', 'iron_golem', 'snow_golem', 'allay', 'wolf', 'cat', 'parrot', 'horse', 'donkey', 'mule', 'llama',
          'trader_llama', 'camel', 'happy_ghast', 'axolotl', 'fox', 'ocelot', 'nautilus', 'sniffer', 'armadillo', 'turtle', 'frog', 'goat']

_melee = lambda dmg: [attr('attack_damage', dmg, 'mainhand', ident='minecraft:base_attack_damage'),
                      attr('attack_speed', -3.0, 'mainhand', ident='minecraft:base_attack_speed')]
_catalyst = [('Off hand + look up + right-click to turn it:', 'dark_gray'), ('Blaze Rod - Offense, Armadillo Scute - Defense,', 'dark_gray'),
             ('Breeze Rod - Ranged, Heartstone - Support.', 'dark_gray'), ('(Lanterns still work: Lantern, Soul, Copper.)', 'dark_gray')]
_nova = ('Kill monsters to stoke it, then sneak, look down', 'blue')
_moon = ('Night: x1.5. Full & new moon: x2. Blood Moon: x2.5.', 'gold')
# 2.32: four classes - Offense, Defense, Ranged, Support
item('horseman_head', TOTEM, "Horseman's Head", ORANGE,
     ["The Headless Horseman's own grinning head.", ('OFFENSE', 'red'), ('Hits harder than netherite, swings slowly,', 'gray'), ('and sets its victims alight.', 'gray'),
      ('Hold right-click: a short, fierce stream of fire', 'blue'), ('(5 s), then 10 s to rekindle.', 'blue'),
      ('Sneak + hold right-click: charge a Fire Blast;', 'blue'), ('let go to loose it.', 'blue'),
      _nova, ('and right-click: a HELLFIRE NOVA (10 blocks).', 'blue'), ('Undead it kills drop extra experience.', 'gray'), _moon] + _catalyst +
     [('Some say a beating heart could tame its fire...', 'dark_purple')],
     model='bm:horseman_head', stack=1, cat='relic', glint=False, bold=True,
     custom_extra={'bm_head': B(1)}, comps=dict(hold('none'), **{'minecraft:attribute_modifiers': _melee(9),
                                                                 'minecraft:enchantments': {'bm:hellfire_edge': Int(1)}}))
item('soul_head', TOTEM, 'Soulfire Head', '#5ad8ff',
     ['The Horseman\'s head, burning cold with soul fire.', ('DEFENSE', 'aqua'), ('Its blows slow and weaken their victims.', 'gray'),
      ('Hold right-click: a FROST WARD (10 s) - take less', 'blue'), ('damage, no knockback, and whoever hits you is', 'blue'),
      ('chilled to the bone.', 'blue'), ('Sneak + hold right-click: charge a Frost Blast.', 'blue'),
      _nova, ('and right-click: a GLACIAL NOVA freezes all', 'blue'), ('around for 3 s and shields you (Absorption).', 'blue'), _moon] + _catalyst,
     model='bm:soul_head', stack=1, cat='relic', glint=False, bold=True,
     custom_extra={'bm_head': B(1)}, comps=dict(hold('none'), **{'minecraft:attribute_modifiers': _melee(6),
                                                                 'minecraft:enchantments': {'bm:soulfrost_edge': Int(1)}}))
item('venom_head', TOTEM, 'Venomfire Head', '#7aff4a',
     ['The Horseman\'s head, guttering green with copper fire.', ('RANGED', 'green'), ('A weak club - its poison works from afar.', 'gray'),
      ('Hold right-click: VENOM BOLTS (40 blocks) that', 'blue'), ('poison (wither the undead). 10 s, then 10 s rest.', 'blue'),
      ('Sneak + hold right-click: charge a PLAGUE BURST;', 'blue'), ('let go to lob it - it leaves a poison cloud.', 'blue'),
      _nova, ('and right-click: a Venom Nova (10 blocks).', 'blue'), _moon] + _catalyst,
     model='bm:venom_head', stack=1, cat='relic', glint=False, bold=True,
     custom_extra={'bm_head': B(1)}, comps=dict(hold('none'), **{'minecraft:attribute_modifiers': _melee(4),
                                                                 'minecraft:enchantments': {'bm:venom_edge': Int(1)}}))
item('hallowed_head', TOTEM, 'Hallowed Head', '#ff8ac8',
     ['The Horseman\'s head, its fire tamed by a living heart.', ('SUPPORT', 'light_purple'), ('A poor club.', 'gray'),
      ('Hold right-click: a healing beam (heals you when', 'blue'), ('nobody is in it; it sears the undead). 10 s, then', 'blue'),
      ('10 s to rekindle.', 'blue'), ('Sneak + right-click: a circle of Regeneration (10 s).', 'blue'),
      ('Heal or slay to stoke it, then sneak, look down', 'blue'), ('and right-click: everyone near is filled with life.', 'blue'),
      ('Night: stronger. Full & new moon: faster.', 'gold'), ('Blood Moon: strongest of all.', 'gold')] + _catalyst,
     model='bm:hallowed_head', stack=1, cat='relic', glint=False, bold=True,
     custom_extra={'bm_head': B(1)}, comps=dict(hold('none'), **{'minecraft:attribute_modifiers': _melee(1)}))
for _v, (_iid, *_r) in VARIANTS.items():
    HOLD_REPEAT[_iid] = 'bm:p42/use'

FIRE_RES = {'id': 'minecraft:fire_resistance', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0)}
RESIST = {'id': 'minecraft:resistance', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0)}
NO_DROP = {k: F(0.0) for k in ['head', 'chest', 'legs', 'feet', 'mainhand', 'offhand', 'body', 'saddle']}
at = lambda i, b: {'id': f'minecraft:{i}', 'base': D(b)}
RIDER = {'id': 'minecraft:wither_skeleton', 'Tags': ['bm.seen', 'bm.tiered', 'bm.hhm', 'bm.hh_new'], 'PersistenceRequired': B(1),
         'CustomName': T('The Headless Horseman', ORANGE, bold=True), 'Health': F(HP), 'DeathLootTable': 'bm:p42/horseman',
         'attributes': [at('max_health', HP), at('attack_damage', 6), at('armor', 4), at('armor_toughness', 4), at('follow_range', 96),
                        at('movement_speed', 0.3), at('scale', 1.25), at('knockback_resistance', 1.0), at('step_height', 1.5),
                        at('safe_fall_distance', 40)],
         'active_effects': [FIRE_RES, RESIST, {'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0)}],
         'equipment': {'chest': {'id': 'minecraft:leather_chestplate', 'count': Int(1), 'components': {
                           'minecraft:dyed_color': 0x1c1418, 'minecraft:trim': {'material': 'minecraft:quartz', 'pattern': 'minecraft:rib'}}},
                       'legs': {'id': 'minecraft:netherite_leggings', 'count': Int(1), 'components': {
                           'minecraft:trim': {'material': 'minecraft:redstone', 'pattern': 'minecraft:silence'}}},
                       'feet': {'id': 'minecraft:netherite_boots', 'count': Int(1)},
                       'mainhand': {'id': 'minecraft:netherite_spear', 'count': Int(1), 'components': {
                           'minecraft:enchantments': {'minecraft:fire_aspect': Int(2)}}},
                       'offhand': {'id': 'minecraft:jack_o_lantern', 'count': Int(1)}},
         'drop_chances': NO_DROP}
STEED = {'Tags': ['bm.seen', 'bm.hhs', 'bm.hh_new'], 'Tame': B(1), 'PersistenceRequired': B(1), 'Health': F(160),
         'CustomName': T('Hellsteed', '#c84a1a'),
         'attributes': [at('max_health', 160), at('movement_speed', 0.36), at('jump_strength', 1.0), at('scale', 1.3), at('armor', 8),
                        at('knockback_resistance', 0.8), at('step_height', 1.5), at('safe_fall_distance', 40), at('follow_range', 96)],
         'active_effects': [FIRE_RES, RESIST],
         'equipment': {'saddle': {'id': 'minecraft:saddle', 'count': Int(1)}, 'body': {'id': 'minecraft:netherite_horse_armor', 'count': Int(1)}},
         'drop_chances': NO_DROP, 'Passengers': [RIDER]}
THRALL = {'Tags': ['bm.seen', 'bm.tiered', 'bm.hhmin'], 'CustomName': T('Pumpkin Thrall', '#e8902a'), 'Health': F(26),
          'attributes': [at('max_health', 26), at('follow_range', 48)], 'active_effects': [FIRE_RES],
          'DeathLootTable': 'minecraft:entities/skeleton', 'drop_chances': NO_DROP}
THRALL_BOW = dict(THRALL, equipment={'head': {'id': 'minecraft:jack_o_lantern', 'count': Int(1)}, 'mainhand': {'id': 'minecraft:bow', 'count': Int(1)}})
THRALL_SWORD = dict(THRALL, equipment={'head': {'id': 'minecraft:carved_pumpkin', 'count': Int(1)}, 'mainhand': {'id': 'minecraft:iron_sword', 'count': Int(1)}})


def ring(r, n, y, part):
    return [f'particle {part} ~{r * math.cos(2 * math.pi * i / n):.2f} ~{y} ~{r * math.sin(2 * math.pi * i / n):.2f} 0.05 0.05 0.05 0.01 1' for i in range(n)]


def generate(G):
    fn, wjson, title, give, tellraw, PREFIX = G.fn, G.wjson, G.title, G.give, G.tellraw, G.PREFIX
    holds = '*[minecraft:custom_data~{bm:"%s"}]'
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    near = 'gamemode=!creative,gamemode=!spectator'
    tick, fast, second = [], [], []
    objs = ['bm.hht dummy', 'bm.hhb dummy', 'bm.hhl dummy', 'bm.hhx dummy', 'bm.hhv dummy', 'bm.hfu dummy', 'bm.hcd dummy', 'bm.hid dummy',
            'bm.hch dummy', 'bm.hbc dummy', 'bm.hkl dummy', 'bm.hpw dummy', 'bm.hzc dummy', 'bm.hzt dummy', 'bm.hrg dummy', 'bm.hpl dummy']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o}' for o in objs] + [
        'scoreboard players set #8 bm.bm 8', 'scoreboard players set #5 bm.rng 5', 'scoreboard players set #10 bm.rng 10',
        'scoreboard players set #20 bm.rng 20',
        f'bossbar add bm:hhm {snbt(T("The Headless Horseman", ORANGE, bold=True))}', 'bossbar set bm:hhm color yellow',
        'bossbar set bm:hhm style notched_10', f'bossbar set bm:hhm max {HP}', 'bossbar set bm:hhm visible false']
    G.OBJECTIVES += [o.split()[0] for o in objs]

    # ------------------------------------------------------------------ registry bits
    for name, msg, extra in [('hellfire', 'bm.hellfire', {'effects': 'burning'}), ('soulfrost', 'bm.soulfrost', {'effects': 'freezing'}),
                             ('venomfire', 'bm.venomfire', {}), ('hallowed', 'bm.hallowed', {})]:
        wjson(f'bm/damage_type/{name}.json', dict({'exhaustion': 0.1, 'message_id': msg, 'scaling': 'when_caused_by_living_non_player'}, **extra))
    wjson('minecraft/tags/damage_type/is_freezing.json', {'replace': False, 'values': ['bm:soulfrost']})
    wjson('bm/tags/entity_type/p42_foe.json', {'values': ['#bm:hostile'] + [{'id': f'minecraft:{e}', 'required': False} for e in FOES_EXTRA]})
    wjson('bm/tags/entity_type/p42_ally.json', {'values': [{'id': f'minecraft:{e}', 'required': False} for e in ALLIES]})
    wjson('bm/tags/item/p42_copper.json', {'values': [f'minecraft:{c}' for c in COPPER]})
    wjson('bm/predicate/p42/burning.json', {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:flags': {'is_on_fire': True}}})
    ench = lambda desc, col, effs: {'anvil_cost': 8, 'description': T(desc, col), 'max_level': 1, 'weight': 1,
                                    'min_cost': {'base': 1, 'per_level_above_first': 0}, 'max_cost': {'base': 1, 'per_level_above_first': 0},
                                    'slots': ['mainhand'], 'supported_items': '#minecraft:enchantable/weapon',
                                    'effects': {'minecraft:post_attack': [dict({'affected': 'victim', 'enchanted': 'attacker'}, **e) for e in effs]}}
    mob_eff = lambda e, s, a: {'type': 'minecraft:apply_mob_effect', 'to_apply': f'minecraft:{e}', 'min_duration': float(s), 'max_duration': float(s),
                               'min_amplifier': float(a), 'max_amplifier': float(a)}
    undead = {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:entity_type': '#minecraft:undead'}}
    wjson('bm/enchantment/hellfire_edge.json', ench('Hellfire', ORANGE, [{'effect': {'type': 'minecraft:ignite', 'duration': 5}}]))
    wjson('bm/enchantment/soulfrost_edge.json', ench('Soulfrost', '#5ad8ff', [
        {'effect': {'type': 'minecraft:all_of', 'effects': [mob_eff('slowness', 3, 2), mob_eff('weakness', 3, 0),
                                                             {'type': 'minecraft:damage_entity', 'damage_type': 'bm:soulfrost', 'min_damage': 2.0, 'max_damage': 2.0}]}}]))
    wjson('bm/enchantment/venom_edge.json', ench('Venomfire', '#7aff4a', [
        {'effect': mob_eff('poison', 5, 1), 'requirements': {'condition': 'minecraft:inverted', 'term': undead}},
        {'effect': mob_eff('wither', 4, 0), 'requirements': undead}]))

    # ================================================================== the head
    # which head is in the main hand (#hv), the holder's power tier and the values that hang on it
    fn('p42/hv', ['scoreboard players set #hv bm.rng 0'] +
       [f'execute if items entity @s weapon.mainhand {holds % iid} run return run scoreboard players set #hv bm.rng {v}' for v, (iid, *_r) in VARIANTS.items()])
    fn('p42/tier', ['scoreboard players set @s bm.hpw 0', 'execute if dimension minecraft:overworld run scoreboard players operation @s bm.hpw = #hpw bm.bm',
                    'scoreboard players set #cdv bm.rng 200', 'scoreboard players set #chg bm.rng 40', 'scoreboard players set #nov bm.rng 20',
                    'scoreboard players set #bcd bm.rng 160', 'scoreboard players set #zcd bm.rng 600', 'scoreboard players set #hpi bm.rng 20',
                    'execute if score @s bm.hpw matches 1 run scoreboard players set #hpi bm.rng 15',
                    'execute if score @s bm.hpw matches 2.. run function bm:p42/tier_moon'])
    fn('p42/tier_moon', ['scoreboard players set #cdv bm.rng 120', 'scoreboard players set #chg bm.rng 24', 'scoreboard players set #nov bm.rng 12',
                         'scoreboard players set #bcd bm.rng 100', 'scoreboard players set #zcd bm.rng 400', 'scoreboard players set #hpi bm.rng 12',
                         'execute if score @s bm.hpw matches 3 run scoreboard players set #hpi bm.rng 10'])
    # damage for this hit: base (tenths) x (1 + tier/2), and the head's damage type
    fn('p42/dmg', ['$scoreboard players set #dm bm.rng $(b)', 'scoreboard players operation #mul bm.rng = @s bm.hpw',
                   'scoreboard players operation #mul bm.rng *= #5 bm.rng', 'scoreboard players add #mul bm.rng 10',
                   'scoreboard players operation #dm bm.rng *= #mul bm.rng', 'scoreboard players operation #dm bm.rng /= #10 bm.rng',
                   'execute store result storage bm:tmp p42.d double 0.1 run scoreboard players get #dm bm.rng'])

    fn('p42/use', ['function bm:p42/hv',
                   'execute if score #hv bm.rng matches 0 run return run execute if score #first bm.hnow matches 1 run ' + say('Hold the head in your main hand.'),
                   'execute if score #first bm.hnow matches 1 run tag @s remove bm.p42lock',
                   'execute if entity @s[tag=bm.p42lock] run return 0',
                   'execute unless score @s bm.hfu matches -2147483648.. run function bm:p42/init',
                   'function bm:p42/tier',
                   'execute if score #first bm.hnow matches 1 if entity @s[x_rotation=-90..-55] if function bm:p42/up/has run return run function bm:p42/up/try',
                   'execute if score #first bm.hnow matches 1 if entity @s[x_rotation=55..90] if predicate bm:p20/sneaking run return run function bm:p42/nova/try',
                   'execute if score #hv bm.rng matches 4 run return run function bm:p42/heal/use',
                   'execute if predicate bm:p20/sneaking run return run function bm:p42/blast/charge',
                   'execute if score #hv bm.rng matches 2 run return run function bm:p42/ward/use',
                   'execute if score #hv bm.rng matches 3 run return run function bm:p42/bolt/use',
                   'function bm:p42/flame/use'])
    fn('p42/init', ['scoreboard players set @s bm.hfu 200', 'scoreboard players set @s bm.hcd 0', 'scoreboard players set @s bm.hbc 0',
                    'scoreboard players set @s bm.hzc 0', 'scoreboard players set @s bm.hid 0',
                    'execute unless score @s bm.hkl matches 0.. run scoreboard players set @s bm.hkl 0'])

    # ---------------- the stream of fire (and the beam's fuel): 200 ticks, the reach shrinking with it
    bar = lambda lab: [{'text': ''}, T(lab, ORANGE), {'score': {'name': '#fs', 'objective': 'bm.rng'}, 'color': 'white'}, T(' s', ORANGE)]
    fn('p42/flame/use', ['execute if entity @s[tag=bm.p42chg] run function bm:p42/blast/fizzle',
                         'execute if score @s bm.hcd matches 1.. run return run function bm:p42/flame/hot',
                         'scoreboard players set @s bm.hid 0', 'scoreboard players remove @s bm.hfu 2',
                         'execute if score @s bm.hfu matches ..0 run return run function bm:p42/flame/out',
                         'scoreboard players operation #st bm.rng = @s bm.hfu', 'scoreboard players operation #st bm.rng /= #20 bm.rng',
                         'scoreboard players add #st bm.rng 3',
                         'execute store result score #g bm.rng run time query gametime', 'scoreboard players operation #g bm.rng %= #10 bm.rng',
                         'scoreboard players set #hit bm.rng 0',
                         'execute if score #g bm.rng matches 0 run scoreboard players set #hit bm.rng 1',
                         'execute if score #hit bm.rng matches 1 run function bm:p42/dmg {b:60}',
                         'tag @s add bm.p42me', 'scoreboard players set #k bm.rng 0'] +
       [f'execute if score #hv bm.rng matches {v} anchored eyes positioned ^ ^-0.3 ^0.8 run function bm:p42/flame/ray_{v}' for v in (1,)] +
       ['tag @s remove bm.p42me', 'execute if score #hit bm.rng matches 1 run tag @e[tag=bm.p42hit,distance=..24] remove bm.p42hit',
        'execute if score #g bm.rng matches 0 run function bm:p42/flame/sound',
        'execute if score #g bm.rng matches 5 run function bm:p42/flame/sound',
        'execute if score #g bm.rng matches 0 run function bm:p42/flame/bar'])
    fn('p42/flame/sound', ['execute if score #hv bm.rng matches 1 run playsound minecraft:entity.blaze.burn player @a[distance=..16] ~ ~ ~ 0.5 0.7',
                           'execute if score #hv bm.rng matches 2 run playsound minecraft:block.fire.ambient player @a[distance=..16] ~ ~ ~ 1 1.7',
                           'execute if score #hv bm.rng matches 2 run playsound minecraft:entity.player.hurt_freeze player @a[distance=..16] ~ ~ ~ 0.15 1.4',
                           'execute if score #hv bm.rng matches 3 run playsound minecraft:block.fire.ambient player @a[distance=..16] ~ ~ ~ 1 0.6',
                           'execute if score #hv bm.rng matches 3 run playsound minecraft:block.brewing_stand.brew player @a[distance=..16] ~ ~ ~ 0.3 1.6',
                           'execute if score #hv bm.rng matches 4 run playsound minecraft:block.beacon.ambient player @a[distance=..16] ~ ~ ~ 0.6 1.8'])
    fn('p42/flame/bar', ['scoreboard players operation #fs bm.rng = @s bm.hfu', 'scoreboard players add #fs bm.rng 19', 'scoreboard players operation #fs bm.rng /= #20 bm.rng',
                         'execute unless score #hv bm.rng matches 4 run ' + title('@s', 'actionbar', bar('Fire ')),
                         'execute if score #hv bm.rng matches 4 run ' + title('@s', 'actionbar', bar('Light '))])
    fn('p42/flame/hot', ['execute unless score #first bm.hnow matches 1 run return 0',
                         'scoreboard players operation #fs bm.rng = @s bm.hcd', 'scoreboard players add #fs bm.rng 19', 'scoreboard players operation #fs bm.rng /= #20 bm.rng',
                         title('@s', 'actionbar', [T('Still smouldering... ', 'gray'), {'score': {'name': '#fs', 'objective': 'bm.rng'}, 'color': 'white'}, T(' s', 'gray')])])
    fn('p42/flame/out', ['scoreboard players set @s bm.hfu 0', 'scoreboard players operation @s bm.hcd = #cdv bm.rng',
                         'playsound minecraft:block.fire.extinguish player @a[distance=..16] ~ ~ ~ 1 0.8',
                         'execute anchored eyes positioned ^ ^-0.3 ^0.8 run particle minecraft:large_smoke ~ ~ ~ 0.2 0.2 0.2 0.02 12',
                         say('The head gutters out. It needs a moment to rekindle.')])
    fn('p42/cool', ['scoreboard players remove @s bm.hcd 5', 'execute if score @s bm.hcd matches ..0 run function bm:p42/ready'])
    fn('p42/ready', ['scoreboard players set @s bm.hcd 0', 'scoreboard players set @s bm.hfu 200',
                     'execute if items entity @s weapon.mainhand ' + HEAD + ' at @s run playsound minecraft:item.firecharge.use player @s ~ ~ ~ 0.5 1.4',
                     'execute if items entity @s weapon.mainhand ' + HEAD + ' run ' + title('@s', 'actionbar', T('The head\'s fire is rekindled.', ORANGE))])
    # recovering on its own: after a second without use, back at 1 tick of fire per tick
    fn('p42/refuel', ['scoreboard players add @s bm.hid 5', 'execute if score @s bm.hid matches 20.. run scoreboard players add @s bm.hfu 5',
                      'execute if score @s bm.hfu matches 201.. run scoreboard players set @s bm.hfu 200'])
    spread = [(3, 0.08, 2), (7, 0.2, 3), (99, 0.35, 3)]
    extra = {1: ['execute if score #k bm.rng matches 6.. run particle minecraft:smoke ~ ~0.2 ~ 0.2 0.2 0.2 0.01 1'],
             2: ['particle minecraft:snowflake ~ ~ ~ 0.2 0.2 0.2 0.02 1'],
             3: ['execute if score #k bm.rng matches 4.. run particle minecraft:dust{color:[0.35,0.85,0.2],scale:1.2} ~ ~ ~ 0.25 0.25 0.25 0 1']}
    for v in (1,):
        part = VARIANTS[v][4]
        lines = ['execute unless block ~ ~ ~ #bm:grap_pass run return 0',
                 'execute if block ~ ~ ~ minecraft:water run return run particle minecraft:cloud ~ ~ ~ 0.2 0.2 0.2 0.02 3',
                 'scoreboard players add #k bm.rng 1']
        lo = 1
        for hi, s, n in spread:
            lines.append(f'execute if score #k bm.rng matches {lo}..{hi} run particle {part} ~ ~ ~ {s} {s} {s} 0.03 {n}')
            lo = hi + 1
        lines += extra[v] + ['execute if score #hit bm.rng matches 1 run function bm:p42/hit/near_1',
                             'execute if score #k bm.rng >= #st bm.rng run return 0', f'execute positioned ^ ^ ^0.6 run function bm:p42/flame/ray_{v}']
        fn(f'p42/flame/ray_{v}', lines)

    # ---------------- who the head's fire can hurt: any mob (2.23: animals too - and they come out cooked), the Hellsteed, other players (never its user)
    for name, r in [('near_1', 1.6), ('near_4', 4), ('near_10', 10)]:
        fn(f'p42/hit/{name}', [f'execute as @e[type=!#bm:p44_nonmob,type=!minecraft:player,tag=!bm.npc,tag=!bm.wilfrey,tag=!bm.wil_body,tag=!bm.frogpet,tag=!bm.merc,tag=!bm.cecilpet,tag=!bm.emmapet,distance=..{r},tag=!bm.p42hit] run function bm:p42/hit/one',
                               f'execute as @e[type=minecraft:skeleton_horse,tag=bm.hhs,distance=..{r + 0.6},tag=!bm.p42hit] run function bm:p42/hit/one',
                               f'execute as @a[distance=..{r},tag=!bm.p42hit,tag=!bm.p42me,{near}] run function bm:p42/hit/one'])
    fn('p42/hit/one', ['tag @s add bm.p42hit'] + [f'execute if score #hv bm.rng matches {v} run function bm:p42/hit/apply_{v} with storage bm:tmp p42' for v in (1, 2, 3)] + [
                       'execute if score #hv bm.rng matches 1 at @s run function bm:p42/fx/burn',
                       'execute if score #hv bm.rng matches 2 at @s run function bm:p42/fx/freeze',
                       'execute if score #hv bm.rng matches 3 at @s run function bm:p42/fx/venom'])
    for v in (1, 2, 3):
        fn(f'p42/hit/apply_{v}', [f'$damage @s $(d) {VARIANTS[v][5]} by @a[tag=bm.p42me,limit=1]'])
    # setting alight: mobs directly; a player through a flicker of real fire at their feet (taken away 2 ticks later)
    fn('p42/fx/burn', ['execute if entity @s[type=!minecraft:player] run return run data merge entity @s {Fire:100s}',
                       'execute if predicate bm:p42/burning run return 0',
                       'execute if block ~ ~ ~ #minecraft:air run function bm:p42/fx/flicker'])
    fn('p42/fx/flicker', ['setblock ~ ~ ~ minecraft:fire', 'summon minecraft:marker ~ ~ ~ {Tags:["bm.p42fire"]}',
                          'schedule function bm:p42/fx/unflicker 2t replace'])
    fn('p42/fx/unflicker', ['execute as @e[type=minecraft:marker,tag=bm.p42fire] at @s run function bm:p42/fx/unflicker1'])
    fn('p42/fx/unflicker1', ['execute if block ~ ~ ~ minecraft:fire run setblock ~ ~ ~ minecraft:air', 'kill @s'])
    second.append('execute as @e[type=minecraft:marker,tag=bm.p42fire] at @s run function bm:p42/fx/unflicker1')
    fn('p42/fx/freeze', ['effect give @s minecraft:slowness 3 2 true',
                         'execute if entity @s[type=!minecraft:player] run data merge entity @s {TicksFrozen:300}',
                         'particle minecraft:snowflake ~ ~1 ~ 0.3 0.5 0.3 0.02 6'])
    fn('p42/fx/venom', ['execute if entity @s[type=#minecraft:undead] run return run effect give @s minecraft:wither 4 0',
                        'effect give @s minecraft:poison 4 1', 'particle minecraft:item_slime ~ ~1 ~ 0.3 0.4 0.3 0 4'])

    # ---------------- the Fire Blast: sneak and hold to charge, let go to loose it
    fn('p42/blast/charge', ['execute if score @s bm.hbc matches 1.. run return run function bm:p42/blast/wait',
                            'tag @s add bm.p42chg', 'scoreboard players add @s bm.hch 1',
                            'execute if score #hv bm.rng matches 1 anchored eyes positioned ^ ^-0.3 ^0.9 run particle minecraft:flame ~ ~ ~ 0.25 0.25 0.25 0.01 2',
                            'execute if score #hv bm.rng matches 2 anchored eyes positioned ^ ^-0.3 ^0.9 run particle minecraft:soul_fire_flame ~ ~ ~ 0.25 0.25 0.25 0.01 2',
                            'execute if score #hv bm.rng matches 3 anchored eyes positioned ^ ^-0.3 ^0.9 run particle minecraft:copper_fire_flame ~ ~ ~ 0.25 0.25 0.25 0.01 2',
                            'execute if score @s bm.hch = #chg bm.rng run function bm:p42/blast/full',
                            'execute if score @s bm.hch < #chg bm.rng run function bm:p42/blast/progress'])
    fn('p42/blast/progress', ['scoreboard players operation #pc bm.rng = @s bm.hch', 'scoreboard players operation #pc bm.rng *= #100 bm.rng',
                              'scoreboard players operation #pc bm.rng /= #chg bm.rng',
                              'execute store result score #g bm.rng run time query gametime', 'scoreboard players operation #g bm.rng %= #5 bm.rng',
                              'execute unless score #g bm.rng matches 0 run return 0',
                              'playsound minecraft:block.fire.ambient player @a[distance=..12] ~ ~ ~ 0.6 1.2',
                              title('@s', 'actionbar', [{'text': ''}, T('Charging... ', ORANGE), {'score': {'name': '#pc', 'objective': 'bm.rng'}, 'color': 'white'}, T('%', ORANGE)])])
    fn('p42/blast/full', ['playsound minecraft:block.respawn_anchor.charge player @s ~ ~ ~ 0.8 1.2',
                          title('@s', 'actionbar', T('FIRE BLAST READY - let go!', ORANGE, bold=True))])
    fn('p42/blast/wait', ['execute unless score #first bm.hnow matches 1 run return 0',
                          'scoreboard players operation #fs bm.rng = @s bm.hbc', 'scoreboard players add #fs bm.rng 19', 'scoreboard players operation #fs bm.rng /= #20 bm.rng',
                          title('@s', 'actionbar', [T('The next blast is building... ', 'gray'), {'score': {'name': '#fs', 'objective': 'bm.rng'}, 'color': 'white'}, T(' s', 'gray')])])
    fn('p42/blast/fizzle', ['tag @s remove bm.p42chg', 'scoreboard players set @s bm.hch 0',
                            'playsound minecraft:block.fire.extinguish player @s ~ ~ ~ 0.4 1.6'])
    # let go (the hold wrapper stamps bm.huse every tick the button is down)
    fn('p42/blast/check', ['execute store result score #now bm.hnow run time query gametime',
                           'scoreboard players operation #gap bm.rng = #now bm.hnow', 'scoreboard players operation #gap bm.rng -= @s bm.huse',
                           'execute if score #gap bm.rng matches ..2 run return 0',
                           'tag @s remove bm.p42chg',
                           'execute unless items entity @s weapon.mainhand ' + HEAD + ' run return run scoreboard players set @s bm.hch 0',
                           'function bm:p42/hv', 'function bm:p42/tier',
                           'execute if score @s bm.hch < #chg bm.rng run return run function bm:p42/blast/fizzle',
                           'scoreboard players set @s bm.hch 0', 'execute at @s run function bm:p42/blast/fire'])
    fn('p42/blast/fire', ['scoreboard players operation @s bm.hbc = #bcd bm.rng',
                          'execute if score #hv bm.rng matches 3 run return run function bm:p42/plague/fire', 'function bm:p42/dmg {b:140}',
                          'tag @s add bm.p42me', 'scoreboard players set #k bm.rng 0',
                          'playsound minecraft:entity.blaze.shoot player @a[distance=..24] ~ ~ ~ 1.2 0.6',
                          'playsound minecraft:item.firecharge.use player @a[distance=..24] ~ ~ ~ 1 0.5',
                          'execute anchored eyes positioned ^ ^-0.2 ^1 run function bm:p42/blast/step',
                          'tag @s remove bm.p42me', 'tag @e[tag=bm.p42hit,distance=..48] remove bm.p42hit'])
    fn('p42/blast/step', ['scoreboard players add #k bm.rng 1'] +
       [f'execute if score #hv bm.rng matches {v} run particle {VARIANTS[v][4]} ~ ~ ~ 0.12 0.12 0.12 0.01 4' for v in (1, 2, 3)] +
       ['particle minecraft:smoke ~ ~ ~ 0.05 0.05 0.05 0.01 1',
        'execute if entity @e[type=!#bm:p44_nonmob,type=!minecraft:player,tag=!bm.npc,tag=!bm.wilfrey,tag=!bm.wil_body,tag=!bm.frogpet,tag=!bm.merc,tag=!bm.cecilpet,tag=!bm.emmapet,distance=..1.3] run return run function bm:p42/blast/boom',
        'execute if entity @e[type=minecraft:skeleton_horse,tag=bm.hhs,distance=..1.9] run return run function bm:p42/blast/boom',
        f'execute if entity @a[distance=..1.3,tag=!bm.p42me,{near}] run return run function bm:p42/blast/boom',
        'execute unless block ~ ~ ~ #bm:grap_pass run return run function bm:p42/blast/boom',
        'execute if block ~ ~ ~ minecraft:water run return run function bm:p42/blast/boom',
        'execute if score #k bm.rng matches 70.. run return run function bm:p42/blast/boom',
        'execute positioned ^ ^ ^0.5 run function bm:p42/blast/step'])
    fn('p42/blast/boom', ['particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 1'] +
       [f'execute if score #hv bm.rng matches {v} run particle {VARIANTS[v][4]} ~ ~ ~ 1.4 1.4 1.4 0.12 70' for v in (1, 2, 3)] +
       ['execute if score #hv bm.rng matches 1 run particle minecraft:lava ~ ~ ~ 1 1 1 0 10',
        'execute if score #hv bm.rng matches 2 run particle minecraft:snowflake ~ ~ ~ 1.5 1.5 1.5 0.05 40',
        'execute if score #hv bm.rng matches 3 run particle minecraft:item_slime ~ ~ ~ 1.5 1.5 1.5 0 30',
        'playsound minecraft:entity.generic.explode player @a[distance=..40] ~ ~ ~ 1.6 0.8',
        'function bm:p42/hit/near_4'])

    # ---------------- 2.32 DEFENSE (the Soulfire Head): hold right-click for a Frost Ward, on the same 10 s of fire
    fn('p42/ward/use', ['execute if score @s bm.hcd matches 1.. run return run function bm:p42/flame/hot',
                        'scoreboard players set @s bm.hid 0', 'scoreboard players remove @s bm.hfu 1',
                        'execute if score @s bm.hfu matches ..0 run return run function bm:p42/ward/out',
                        'execute unless entity @s[tag=bm.p42ward] run function bm:p42/ward/on',
                        'effect give @s minecraft:resistance 1 1 true',
                        'execute store result score #g bm.rng run time query gametime', 'scoreboard players operation #g bm.rng %= #10 bm.rng',
                        'execute if score #g bm.rng matches 0 run function bm:p42/ward/fx', 'execute if score #g bm.rng matches 0 run function bm:p42/flame/bar'])
    fn('p42/ward/on', ['tag @s add bm.p42ward', 'attribute @s minecraft:knockback_resistance modifier add bm:p42_ward 1.0 add_value',
                       'playsound minecraft:block.glass.place player @a[distance=..16] ~ ~ ~ 1 0.6',
                       'playsound minecraft:entity.player.hurt_freeze player @a[distance=..16] ~ ~ ~ 0.6 0.8'])
    fn('p42/ward/fx', [*ring(1.3, 14, 1.0, 'minecraft:snowflake'), 'particle minecraft:soul_fire_flame ~ ~1 ~ 0.5 0.6 0.5 0.01 3',
                       'playsound minecraft:block.powder_snow.step player @a[distance=..16] ~ ~ ~ 0.8 0.7'])
    fn('p42/ward/off', ['tag @s remove bm.p42ward', 'attribute @s minecraft:knockback_resistance modifier remove bm:p42_ward'])
    fn('p42/ward/out', ['function bm:p42/ward/off', 'function bm:p42/flame/out'])
    # let go: the ward drops (the hold wrapper stamps bm.huse every tick the button is down)
    fn('p42/ward/check', ['execute store result score #now bm.hnow run time query gametime',
                          'scoreboard players operation #gap bm.rng = #now bm.hnow', 'scoreboard players operation #gap bm.rng -= @s bm.huse',
                          'execute if score #gap bm.rng matches 3.. run function bm:p42/ward/off'])
    # whoever hurts a warded player (anything hostile within 4 blocks) is chilled to the bone
    wjson('bm/advancement/p42/ward_hit.json', {'criteria': {'h': {'trigger': 'minecraft:entity_hurt_player', 'conditions': {'player': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["bm.p42ward"]}'}}]}}},
        'rewards': {'function': 'bm:p42/ward/chill'}})
    fn('p42/ward/chill', ['advancement revoke @s only bm:p42/ward_hit', 'tag @s add bm.p42me',
                          'execute as @e[type=#bm:p42_foe,distance=..4] at @s run function bm:p42/ward/chill1',
                          'tag @s remove bm.p42me', 'particle minecraft:snowflake ~ ~1 ~ 1.2 0.8 1.2 0.05 30',
                          'playsound minecraft:block.glass.break player @a[distance=..16] ~ ~ ~ 0.8 1.4'])
    fn('p42/ward/chill1', ['damage @s 3 bm:soulfrost by @a[tag=bm.p42me,limit=1]', 'effect give @s minecraft:slowness 3 3', 'effect give @s minecraft:weakness 3 0',
                           'data merge entity @s {TicksFrozen:300}', 'particle minecraft:snowflake ~ ~1 ~ 0.3 0.5 0.3 0.02 8'])
    # the Glacial Nova's shield (the freeze itself is in nova/extra)
    fn('p42/ward/glacial', ['effect give @s minecraft:absorption 30 2 true', 'effect give @s minecraft:resistance 5 1 true',
                            *ring(3, 20, 0.2, 'minecraft:snowflake'), 'playsound minecraft:block.glass.break player @a[distance=..32] ~ ~ ~ 1.4 0.6'])

    # ---------------- 2.32 RANGED (the Venomfire Head): hold right-click for Venom Bolts, four a second, 40 blocks
    fn('p42/bolt/use', ['execute if score @s bm.hcd matches 1.. run return run function bm:p42/flame/hot',
                        'scoreboard players set @s bm.hid 0', 'scoreboard players remove @s bm.hfu 1',
                        'execute if score @s bm.hfu matches ..0 run return run function bm:p42/flame/out',
                        'execute store result score #g bm.rng run time query gametime', 'scoreboard players operation #g bm.rng %= #5 bm.rng',
                        'execute if score #g bm.rng matches 0 run function bm:p42/bolt/fire',
                        'scoreboard players operation #g bm.rng = @s bm.hfu', 'scoreboard players operation #g bm.rng %= #10 bm.rng',
                        'execute if score #g bm.rng matches 0 run function bm:p42/flame/bar'])
    fn('p42/bolt/fire', ['function bm:p42/dmg {b:35}', 'tag @s add bm.p42me', 'scoreboard players set #k bm.rng 0',
                         'playsound minecraft:entity.llama.spit player @a[distance=..24] ~ ~ ~ 1 1.3',
                         'playsound minecraft:block.brewing_stand.brew player @a[distance=..16] ~ ~ ~ 0.3 1.8',
                         'execute anchored eyes positioned ^ ^-0.2 ^1 run function bm:p42/bolt/step',
                         'tag @s remove bm.p42me', 'tag @e[tag=bm.p42hit,distance=..48] remove bm.p42hit'])
    fn('p42/bolt/step', ['scoreboard players add #k bm.rng 1', 'particle minecraft:copper_fire_flame ~ ~ ~ 0.04 0.04 0.04 0.005 1',
                         'execute if score #k bm.rng matches 2.. run particle minecraft:dust{color:[0.35,0.85,0.2],scale:0.9} ~ ~ ~ 0.05 0.05 0.05 0 1',
                         f'execute positioned ~ ~-0.9 ~ if entity @e[type=!#bm:p44_nonmob,type=!minecraft:player,tag=!bm.npc,tag=!bm.wilfrey,tag=!bm.wil_body,tag=!bm.frogpet,tag=!bm.merc,tag=!bm.cecilpet,tag=!bm.emmapet,distance=..1.2] run return run function bm:p42/bolt/hit',
                         'execute positioned ~ ~-1 ~ if entity @e[type=minecraft:skeleton_horse,tag=bm.hhs,distance=..1.8] run return run function bm:p42/bolt/hit',
                         f'execute positioned ~ ~-0.9 ~ if entity @a[distance=..1.2,tag=!bm.p42me,{near}] run return run function bm:p42/bolt/hit',
                         'execute unless block ~ ~ ~ #bm:grap_pass run return run particle minecraft:item_slime ~ ~ ~ 0.1 0.1 0.1 0 3',
                         'execute if score #k bm.rng matches 40.. run return 0', 'execute positioned ^ ^ ^1 run function bm:p42/bolt/step'])
    fn('p42/bolt/hit', ['particle minecraft:item_slime ~ ~ ~ 0.2 0.2 0.2 0 6', 'function bm:p42/hit/near_1'])

    # ---------------- 2.32 the Plague Burst (the Venomfire Head's charged shot): a lobbed glob that leaves a poison cloud
    fn('p42/plague/fire', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                           'playsound minecraft:entity.witch.throw player @a[distance=..24] ~ ~ ~ 1.2 0.7',
                           'playsound minecraft:block.brewing_stand.brew player @a[distance=..24] ~ ~ ~ 1 0.6',
                           'execute anchored eyes positioned ^ ^-0.1 ^1 run summon minecraft:snowball ~ ~ ~ {Tags:["bm.plg","bm.plgnew"],Item:{id:"minecraft:slime_ball",count:1},'
                           'Passengers:[{id:"minecraft:item_display",Tags:["bm.plgm","bm.plgnew"]}]}',
                           'execute anchored eyes positioned ^ ^ ^ run summon minecraft:marker ^ ^ ^1 {Tags:["bm.hhvec"]}',
                           'execute anchored eyes positioned ^ ^ ^ run summon minecraft:marker ~ ~ ~ {Tags:["bm.hhvec0"]}'] +
       [f'execute store result score #a{a} bm.rng run data get entity @e[type=minecraft:marker,tag=bm.hhvec,limit=1] Pos[{i}] 1000' for i, a in enumerate('xyz')] +
       [f'execute store result score #s{a} bm.rng run data get entity @e[type=minecraft:marker,tag=bm.hhvec0,limit=1] Pos[{i}] 1000' for i, a in enumerate('xyz')] +
       [f'scoreboard players operation #a{a} bm.rng -= #s{a} bm.rng' for a in 'xyz'] +
       ['kill @e[type=minecraft:marker,tag=bm.hhvec]', 'kill @e[type=minecraft:marker,tag=bm.hhvec0]', 'scoreboard players add #ay bm.rng 220',
        'execute as @e[type=minecraft:snowball,tag=bm.plgnew] run function bm:p42/plague/aim',
        'scoreboard players operation @e[type=minecraft:item_display,tag=bm.plgnew] bm.pid = @s bm.pid',
        'scoreboard players set @e[type=minecraft:item_display,tag=bm.plgnew] bm.hzt 100',
        'tag @e[tag=bm.plgnew] remove bm.plgnew'])
    fn('p42/plague/aim', [f'execute store result entity @s Motion[{i}] double 0.0012 run scoreboard players get #a{a} bm.rng' for i, a in enumerate('xyz')])
    fn('p42/plague/riding', ['execute on vehicle run return 1', 'return 0'])
    fn('p42/plague/fly', ['particle minecraft:dust{color:[0.35,0.85,0.2],scale:1.4} ~ ~ ~ 0.1 0.1 0.1 0 2', 'particle minecraft:item_slime ~ ~ ~ 0.05 0.05 0.05 0 1',
                          'scoreboard players remove @s bm.hzt 1', 'execute if score @s bm.hzt matches ..0 run return run function bm:p42/plague/burst',
                          'execute unless function bm:p42/plague/riding run function bm:p42/plague/burst'])
    fn('p42/plague/burst', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.plgc","bm.plgcn"]}',
                            'scoreboard players operation @e[type=minecraft:marker,tag=bm.plgcn] bm.pid = @s bm.pid',
                            'scoreboard players set @e[type=minecraft:marker,tag=bm.plgcn] bm.hzt 120', 'tag @e[tag=bm.plgcn] remove bm.plgcn',
                            'particle minecraft:item_slime ~ ~0.5 ~ 1 0.5 1 0 40', 'particle minecraft:dust{color:[0.35,0.85,0.2],scale:2.0} ~ ~0.5 ~ 1.5 0.5 1.5 0 40',
                            'playsound minecraft:entity.splash_potion.break player @a[distance=..32] ~ ~ ~ 1.4 0.6',
                            'playsound minecraft:block.slime_block.break player @a[distance=..32] ~ ~ ~ 1 0.6',
                            'execute on vehicle run kill @s', 'kill @s'])
    # the cloud: 6 s, 3 blocks round; once a second it poisons (withers the undead) and hurts all but its thrower
    fn('p42/plague/cloud', ['scoreboard players remove @s bm.hzt 5', 'execute if score @s bm.hzt matches ..0 run return run kill @s',
                            'particle minecraft:dust{color:[0.35,0.85,0.2],scale:2.0} ~ ~0.6 ~ 2 0.4 2 0 12', 'particle minecraft:item_slime ~ ~0.3 ~ 2 0.2 2 0 4',
                            'particle minecraft:copper_fire_flame ~ ~0.2 ~ 2 0.1 2 0.01 2',
                            'scoreboard players operation #zt bm.rng = @s bm.hzt', 'scoreboard players operation #zt bm.rng %= #20 bm.rng',
                            'execute unless score #zt bm.rng matches 0 run return 0',
                            'scoreboard players operation #cp bm.pid = @s bm.pid', 'execute as @a if score @s bm.pid = #cp bm.pid run tag @s add bm.p42me',
                            f'execute as @e[type=!#bm:p44_nonmob,type=!minecraft:player,tag=!bm.npc,tag=!bm.wilfrey,tag=!bm.wil_body,tag=!bm.frogpet,tag=!bm.merc,tag=!bm.cecilpet,tag=!bm.emmapet,distance=..3.2] at @s run function bm:p42/plague/sick',
                            f'execute as @a[distance=..3.2,tag=!bm.p42me,tag=!bm.nopvp,{near}] at @s run function bm:p42/plague/sick',
                            'tag @a remove bm.p42me', 'playsound minecraft:block.bubble_column.upwards_ambient player @a[distance=..16] ~ ~ ~ 0.6 0.6'])
    fn('p42/plague/sick', ['execute if entity @s[type=#minecraft:undead] run effect give @s minecraft:wither 3 1',
                           'execute unless entity @s[type=#minecraft:undead] run effect give @s minecraft:poison 3 1',
                           'execute if entity @a[tag=bm.p42me] run return run damage @s 2 bm:venomfire by @a[tag=bm.p42me,limit=1]', 'damage @s 2 bm:venomfire'])
    tick += ['execute as @a[tag=bm.p42ward] run function bm:p42/ward/check',
             'execute as @e[type=minecraft:item_display,tag=bm.plgm] at @s run function bm:p42/plague/fly']
    fast += ['execute as @e[type=minecraft:marker,tag=bm.plgc] at @s run function bm:p42/plague/cloud']

    # ---------------- stoking: kills while holding the head; the Nova
    holding = [{'condition': 'minecraft:entity_properties', 'entity': 'this',
                'predicate': {'minecraft:equipment': {'mainhand': {'predicates': {'minecraft:custom_data': '{bm_head:1b}'}}}}}]
    for name, cond in [('kill', {'minecraft:entity_type': '#bm:p42_foe'}),
                       ('kill_blood', {'minecraft:entity_type': '#bm:p42_foe', 'minecraft:nbt': '{Tags:["bm.blood"]}'}),
                       ('kill_undead', {'minecraft:entity_type': '#minecraft:undead'})]:
        wjson(f'bm/advancement/p42/{name}.json', {'criteria': {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {
            'player': holding, 'entity': [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': cond}]}}},
            'rewards': {'function': f'bm:p42/{name}'}})
    fn('p42/kill', ['advancement revoke @s only bm:p42/kill', 'function bm:p42/stoke'])
    fn('p42/kill_blood', ['advancement revoke @s only bm:p42/kill_blood', 'function bm:p42/stoke'])
    fn('p42/stoke', ['function bm:p42/tier', 'execute if score @s bm.hkl >= #nov bm.rng run return 0',
                     'scoreboard players add @s bm.hkl 1',
                     'execute if score @s bm.hkl >= #nov bm.rng run return run function bm:p42/stoked',
                     title('@s', 'actionbar', [{'text': ''}, T('Stoked ', ORANGE), {'score': {'name': '@s', 'objective': 'bm.hkl'}, 'color': 'white'},
                                               T(' / ', 'gray'), {'score': {'name': '#nov', 'objective': 'bm.rng'}, 'color': 'white'}])])
    fn('p42/stoked', ['playsound minecraft:block.respawn_anchor.set_spawn player @s ~ ~ ~ 0.8 1.4',
                      title('@s', 'actionbar', T('NOVA READY - sneak, look down, right-click!', ORANGE, bold=True))])
    # undead: extra experience where they fell (or at your feet)
    fn('p42/kill_undead', ['advancement revoke @s only bm:p42/kill_undead', 'function bm:p42/tier',
                           'tag @e[type=#minecraft:undead,distance=..40,nbt={Health:0.0f},sort=nearest,limit=1] add bm.p42xp',
                           'execute at @e[tag=bm.p42xp,limit=1] run function bm:p42/xp',
                           'execute unless entity @e[tag=bm.p42xp] run function bm:p42/xp', 'tag @e[tag=bm.p42xp] remove bm.p42xp'])
    fn('p42/xp', ['summon minecraft:experience_orb ~ ~0.5 ~ {Value:5s}',
                  'execute if score @s bm.hpw matches 1.. run summon minecraft:experience_orb ~ ~0.5 ~ {Value:3s}',
                  'execute if score @s bm.hpw matches 2.. run summon minecraft:experience_orb ~ ~0.5 ~ {Value:4s}',
                  'particle minecraft:soul ~ ~0.6 ~ 0.3 0.3 0.3 0.02 5'])
    nova_ring = {v: [l for r, n in [(2, 12), (4, 20), (6, 28), (8, 36), (10, 44)] for l in ring(r, n, 0.3, VARIANTS[v][4])] for v in (1, 2, 3, 4)}
    for v in (1, 2, 3, 4):
        fn(f'p42/nova/ring_{v}', nova_ring[v])
    fn('p42/nova/try', ['tag @s add bm.p42lock',
                        'execute if score @s bm.hkl < #nov bm.rng run return run ' +
                        title('@s', 'actionbar', [{'text': ''}, T('Not stoked enough: ', 'gray'), {'score': {'name': '@s', 'objective': 'bm.hkl'}, 'color': 'white'},
                                                  T(' / ', 'gray'), {'score': {'name': '#nov', 'objective': 'bm.rng'}, 'color': 'white'}]),
                        'scoreboard players set @s bm.hkl 0',
                        'execute if score #hv bm.rng matches 4 run return run function bm:p42/heal/nova',
                        'function bm:p42/dmg {b:160}', 'execute if score #hv bm.rng matches 1 run function bm:p42/dmg {b:220}',
                        'execute if score #hv bm.rng matches 2 run function bm:p42/dmg {b:100}',
                        'execute if score #hv bm.rng matches 2 run function bm:p42/ward/glacial', 'tag @s add bm.p42me'] +
       [f'execute if score #hv bm.rng matches {v} run function bm:p42/nova/ring_{v}' for v in (1, 2, 3)] +
       ['particle minecraft:explosion_emitter ~ ~1 ~ 0 0 0 0 1',
        'playsound minecraft:entity.wither.shoot player @a[distance=..40] ~ ~ ~ 1.2 0.6',
        'playsound minecraft:entity.generic.explode player @a[distance=..40] ~ ~ ~ 1.4 0.6',
        'function bm:p42/hit/near_10',
        'execute as @e[tag=bm.p42hit,distance=..12] at @s run function bm:p42/nova/extra',
        'tag @s remove bm.p42me', 'tag @e[tag=bm.p42hit,distance=..16] remove bm.p42hit',
        title('@s', 'actionbar', T('NOVA!', ORANGE, bold=True))])
    # the Nova's afterburn is longer than a stream's
    fn('p42/nova/extra', ['execute if score #hv bm.rng matches 1 if entity @s[type=!minecraft:player] run data merge entity @s {Fire:160s}',
                          'execute if score #hv bm.rng matches 2 run effect give @s minecraft:slowness 3 9 true',
                          'execute if score #hv bm.rng matches 2 run effect give @s minecraft:mining_fatigue 3 2 true',
                          'execute if score #hv bm.rng matches 2 if entity @s[type=!minecraft:player] run data merge entity @s {TicksFrozen:420}',
                          'execute if score #hv bm.rng matches 2 at @s run particle minecraft:block{block_state:"minecraft:packed_ice"} ~ ~1 ~ 0.3 0.6 0.3 0 12',
                          'execute if score #hv bm.rng matches 3 unless entity @s[type=#minecraft:undead] run effect give @s minecraft:poison 8 1',
                          'execute if score #hv bm.rng matches 3 if entity @s[type=#minecraft:undead] run effect give @s minecraft:wither 6 1'])

    # ---------------- turning the fire: off hand + look up + right-click
    fn('p42/up/has', ['execute if items entity @s weapon.offhand #bm:p42_catalyst run return 1',
                      'execute if items entity @s weapon.offhand minecraft:soul_lantern run return 1',
                      'execute if items entity @s weapon.offhand #bm:p42_copper run return 1',
                      'execute if items entity @s weapon.offhand minecraft:lantern run return 1',
                      'execute if items entity @s weapon.offhand ' + holds % 'heartstone' + ' run return 1', 'return 0'])
    wjson('bm/tags/item/p42_catalyst.json', {'values': ['minecraft:blaze_rod', 'minecraft:armadillo_scute', 'minecraft:breeze_rod']})
    fn('p42/up/try', ['tag @s add bm.p42lock',
                      'execute if items entity @s weapon.offhand minecraft:blaze_rod run return run function bm:p42/up/to_1',
                      'execute if items entity @s weapon.offhand minecraft:armadillo_scute run return run function bm:p42/up/to_2',
                      'execute if items entity @s weapon.offhand minecraft:breeze_rod run return run function bm:p42/up/to_3',
                      'execute if items entity @s weapon.offhand minecraft:soul_lantern run return run function bm:p42/up/to_2',
                      'execute if items entity @s weapon.offhand #bm:p42_copper run return run function bm:p42/up/to_3',
                      'execute if items entity @s weapon.offhand minecraft:lantern run return run function bm:p42/up/to_1',
                      'execute if items entity @s weapon.offhand ' + holds % 'heartstone' + ' run return run function bm:p42/up/to_4'])
    up_fx = {1: (['particle minecraft:flame ~ ~1.2 ~ 0.4 0.6 0.4 0.05 40', 'playsound minecraft:item.firecharge.use player @a[distance=..16] ~ ~ ~ 1 0.8'],
                 'The head\'s own hellfire flares back up. OFFENSE.', ORANGE),
             2: (['particle minecraft:soul_fire_flame ~ ~1.2 ~ 0.4 0.6 0.4 0.05 40', 'particle minecraft:soul ~ ~1.2 ~ 0.4 0.6 0.4 0.03 15',
                  'playsound minecraft:particle.soul_escape player @a[distance=..16] ~ ~ ~ 2 0.8', 'playsound minecraft:block.soul_sand.place player @a[distance=..16] ~ ~ ~ 1 0.6'],
                 'Soul fire takes the head: it burns cold. DEFENSE.', '#5ad8ff'),
             3: (['particle minecraft:copper_fire_flame ~ ~1.2 ~ 0.4 0.6 0.4 0.05 40', 'playsound minecraft:block.copper.place player @a[distance=..16] ~ ~ ~ 1 0.6',
                  'playsound minecraft:block.brewing_stand.brew player @a[distance=..16] ~ ~ ~ 1 0.8'],
                 'Copper fire takes the head: venom from afar. RANGED.', '#7aff4a'),
             4: (['particle minecraft:heart ~ ~1.4 ~ 0.5 0.5 0.5 0 12', 'particle minecraft:end_rod ~ ~1.2 ~ 0.4 0.6 0.4 0.05 30',
                  'playsound minecraft:entity.warden.heartbeat player @a[distance=..16] ~ ~ ~ 1.5 1', 'playsound minecraft:block.beacon.power_select player @a[distance=..16] ~ ~ ~ 1 1.2'],
                 'The heart beats inside the head... its fire turns gentle. SUPPORT.', '#ff8ac8')}
    for v, (iid, *_r) in VARIANTS.items():
        fx, msg, col = up_fx[v]
        fn(f'p42/up/to_{v}', [f'execute if score #hv bm.rng matches {v} run return run ' + say('It already burns that way.'),
                              f'item replace entity @s weapon.mainhand with {G.item_arg(iid)}',
                              'item modify entity @s weapon.offhand {function:"minecraft:set_count",count:-1,add:true}',
                              'tag @s remove bm.p42chg', 'scoreboard players set @s bm.hch 0'] + fx + [title('@s', 'actionbar', T(msg, col))])

    # ---------------- the Hallowed Head: a healing beam, a circle of Regeneration, a burst of life
    fn('p42/heal/use', ['execute if predicate bm:p20/sneaking run return run execute if score #first bm.hnow matches 1 run function bm:p42/zone/try',
                        'execute if score @s bm.hcd matches 1.. run return run function bm:p42/flame/hot',
                        'scoreboard players set @s bm.hid 0', 'scoreboard players remove @s bm.hfu 1',
                        'execute if score @s bm.hfu matches ..0 run return run function bm:p42/flame/out',
                        'scoreboard players add @s bm.hpl 1', 'scoreboard players set #hit bm.rng 0',
                        'execute if score @s bm.hpl >= #hpi bm.rng run scoreboard players set #hit bm.rng 1',
                        'execute if score #hit bm.rng matches 1 run scoreboard players set @s bm.hpl 0',
                        'tag @s add bm.p42me', 'scoreboard players set #k bm.rng 0', 'scoreboard players set #healed bm.rng 0',
                        'execute anchored eyes positioned ^ ^-0.3 ^0.8 run function bm:p42/heal/ray',
                        'tag @s remove bm.p42me',
                        # nobody in the beam: it heals you, at half the pace
                        'execute if score #hit bm.rng matches 1 if score #healed bm.rng matches 0 run function bm:p42/heal/self',
                        'execute store result score #g bm.rng run time query gametime', 'scoreboard players operation #g bm.rng %= #10 bm.rng',
                        'execute if score #g bm.rng matches 0 run function bm:p42/flame/sound', 'execute if score #g bm.rng matches 0 run function bm:p42/flame/bar'])
    fn('p42/heal/ray', ['execute unless block ~ ~ ~ #bm:grap_pass run return 0', 'scoreboard players add #k bm.rng 1',
                        'particle minecraft:dust{color:[1.0,0.55,0.8],scale:0.9} ~ ~ ~ 0.03 0.03 0.03 0 1',
                        'execute if score #k bm.rng matches 3.. run particle minecraft:end_rod ~ ~ ~ 0.05 0.05 0.05 0.005 0',
                        f'execute as @a[distance=..1.2,tag=!bm.p42me,gamemode=!spectator] at @s run return run function bm:p42/heal/ally',
                        'execute as @e[type=!#bm:p44_nonmob,type=!minecraft:player,type=!#minecraft:undead,tag=!bm.hhm,distance=..1.2,limit=1,sort=nearest] at @s run return run function bm:p42/heal/ally',
                        'execute as @e[type=#minecraft:undead,distance=..1.3,limit=1,sort=nearest] at @s run return run function bm:p42/heal/sear',
                        'execute if score #k bm.rng matches 40.. run return 0', 'execute positioned ^ ^ ^0.6 run function bm:p42/heal/ray'])
    fn('p42/heal/ally', ['scoreboard players set #healed bm.rng 1', 'execute if score #hit bm.rng matches 0 run return 1',
                         'effect give @s minecraft:instant_health 1 0 true',
                         'execute if score @a[tag=bm.p42me,limit=1] bm.hpw matches 3 run effect give @s minecraft:regeneration 3 1 true',
                         'execute at @s run particle minecraft:heart ~ ~1.8 ~ 0.3 0.2 0.3 0 2',
                         'execute at @s run playsound minecraft:block.amethyst_block.chime player @a[distance=..16] ~ ~ ~ 1 1.4',
                         'execute as @a[tag=bm.p42me,limit=1] at @s run function bm:p42/heal/stoke', 'return 1'])
    fn('p42/heal/sear', ['scoreboard players set #healed bm.rng 1', 'execute if score #hit bm.rng matches 0 run return 1',
                         'effect give @s minecraft:instant_health 1 0 true', 'execute at @s run particle minecraft:end_rod ~ ~1 ~ 0.3 0.5 0.3 0.05 6',
                         'execute at @s run playsound minecraft:entity.generic.burn hostile @a[distance=..16] ~ ~ ~ 0.6 1.4', 'return 1'])
    fn('p42/heal/self', ['scoreboard players add @s bm.hrg 1', 'execute unless score @s bm.hrg matches 2.. run return 0', 'scoreboard players set @s bm.hrg 0',
                         'effect give @s minecraft:instant_health 1 0 true', 'particle minecraft:heart ~ ~2 ~ 0.3 0.2 0.3 0 1',
                         'playsound minecraft:block.amethyst_block.chime player @a[distance=..16] ~ ~ ~ 0.6 1.6'])
    fn('p42/heal/stoke', ['execute if score @s bm.hkl >= #nov bm.rng run return 0', 'scoreboard players add @s bm.hkl 1',
                          'execute if score @s bm.hkl >= #nov bm.rng run function bm:p42/stoked'])
    fn('p42/heal/nova', [*nova_ring[4], 'particle minecraft:totem_of_undying ~ ~1 ~ 2 1 2 0.4 80',
                         'playsound minecraft:item.totem.use player @a[distance=..32] ~ ~ ~ 0.8 1.3',
                         'playsound minecraft:block.beacon.activate player @a[distance=..32] ~ ~ ~ 1.2 1.2',
                         'execute as @a[distance=..10,gamemode=!spectator] at @s run function bm:p42/heal/blessed',
                         'execute as @e[type=!#bm:p44_nonmob,type=!minecraft:player,type=!#minecraft:undead,tag=!bm.hhm,distance=..10] at @s run function bm:p42/heal/blessed',
                         'execute as @e[type=#minecraft:undead,distance=..10] run effect give @s minecraft:instant_health 1 1',
                         title('@s', 'actionbar', T('Life floods out of the head!', '#ff8ac8', bold=True))])
    fn('p42/heal/blessed', ['effect give @s minecraft:instant_health 1 1 true', 'effect give @s minecraft:regeneration 6 1 true',
                            'effect give @s minecraft:absorption 30 1 true', 'execute at @s run particle minecraft:heart ~ ~2 ~ 0.4 0.3 0.4 0 3'])
    fn('p42/zone/try', ['tag @s add bm.p42lock',
                        'execute if score @s bm.hzc matches 1.. run return run ' +
                        title('@s', 'actionbar', [T('The circle is still gathering... ', 'gray'), {'score': {'name': '#fs', 'objective': 'bm.rng'}, 'color': 'white'}, T(' s', 'gray')]),
                        'scoreboard players operation @s bm.hzc = #zcd bm.rng',
                        'summon minecraft:marker ~ ~ ~ {Tags:["bm.hzone","bm.hz_new"]}',
                        'scoreboard players set @e[type=minecraft:marker,tag=bm.hz_new] bm.hzt 200',
                        'execute if score @s bm.hpw matches 3 run scoreboard players set @e[type=minecraft:marker,tag=bm.hz_new] bm.hzt 300',
                        'scoreboard players operation @e[type=minecraft:marker,tag=bm.hz_new] bm.hpw = @s bm.hpw',
                        'tag @e[type=minecraft:marker,tag=bm.hz_new] remove bm.hz_new',
                        'playsound minecraft:block.beacon.activate player @a[distance=..24] ~ ~ ~ 1 1.4',
                        'particle minecraft:end_rod ~ ~0.5 ~ 2 0.3 2 0.05 40'])
    G.FUNCS['p42/zone/try'].insert(1, 'scoreboard players operation #fs bm.rng = @s bm.hzc')
    G.FUNCS['p42/zone/try'].insert(2, 'scoreboard players add #fs bm.rng 19')
    G.FUNCS['p42/zone/try'].insert(3, 'scoreboard players operation #fs bm.rng /= #20 bm.rng')
    fn('p42/zone/tick', ['scoreboard players remove @s bm.hzt 5', 'execute if score @s bm.hzt matches ..0 run return run kill @s',
                         *ring(5, 24, 0.15, 'minecraft:dust{color:[1.0,0.55,0.8],scale:1.0}'),
                         'particle minecraft:happy_villager ~ ~0.5 ~ 2.5 0.3 2.5 0 2',
                         'scoreboard players operation #zt bm.rng = @s bm.hzt', 'scoreboard players operation #zt bm.rng %= #20 bm.rng',
                         'execute unless score #zt bm.rng matches 0 run return 0',
                         'execute if score @s bm.hpw matches ..2 as @a[distance=..5,gamemode=!spectator] run effect give @s minecraft:regeneration 3 1 true',
                         'execute if score @s bm.hpw matches ..2 as @e[type=!#bm:p44_nonmob,type=!minecraft:player,type=!#minecraft:undead,tag=!bm.hhm,distance=..5] run effect give @s minecraft:regeneration 3 1 true',
                         'execute if score @s bm.hpw matches 3 as @a[distance=..5,gamemode=!spectator] run effect give @s minecraft:regeneration 3 2 true',
                         'execute if score @s bm.hpw matches 3 as @e[type=!#bm:p44_nonmob,type=!minecraft:player,type=!#minecraft:undead,tag=!bm.hhm,distance=..5] run effect give @s minecraft:regeneration 3 2 true',
                         'particle minecraft:heart ~ ~1 ~ 2 0.5 2 0 3'])

    # ---------------- holding it: the night's power (checked every second; dropped within 5 ticks of letting go)
    fn('p42/held', ['tag @s add bm.p42on', 'function bm:p42/tier', 'function bm:p42/hv',
                    'attribute @s minecraft:attack_damage modifier remove bm:p42_power',
                    'attribute @s minecraft:entity_interaction_range modifier remove bm:p42_reach',
                    'execute unless score #hv bm.rng matches 4 if score @s bm.hpw matches 1 run attribute @s minecraft:attack_damage modifier add bm:p42_power 0.5 add_multiplied_total',
                    'execute unless score #hv bm.rng matches 4 if score @s bm.hpw matches 2 run attribute @s minecraft:attack_damage modifier add bm:p42_power 1.0 add_multiplied_total',
                    'execute unless score #hv bm.rng matches 4 if score @s bm.hpw matches 3 run attribute @s minecraft:attack_damage modifier add bm:p42_power 1.5 add_multiplied_total',
                    'execute if score @s bm.hpw matches 3 run attribute @s minecraft:entity_interaction_range modifier add bm:p42_reach 1.5 add_value',
                    'execute if score @s bm.hpw matches 1.. run effect give @s minecraft:night_vision 15 0 true',
                    'execute if score @s bm.hpw matches 1.. run tag @s add bm.p42nv',
                    'execute if score @s bm.hpw matches 0 if entity @s[tag=bm.p42nv] run function bm:p42/nv_off',
                    'execute if score @s bm.hpw matches 3 run function bm:p42/blood',
                    'execute unless score @s bm.hfu matches -2147483648.. run function bm:p42/init'])
    fn('p42/blood', ['effect give @s minecraft:strength 3 1 true', 'effect give @s minecraft:speed 3 1 true',
                     'scoreboard players add @s bm.hrg 1', 'execute if score @s bm.hrg matches 5.. run effect give @s minecraft:regeneration 6 0 true',
                     'execute if score @s bm.hrg matches 5.. run scoreboard players set @s bm.hrg 0'])
    fn('p42/nv_off', ['effect clear @s minecraft:night_vision', 'tag @s remove bm.p42nv'])
    fn('p42/unheld', ['tag @s remove bm.p42on', 'attribute @s minecraft:attack_damage modifier remove bm:p42_power',
                      'attribute @s minecraft:entity_interaction_range modifier remove bm:p42_reach',
                      'execute if entity @s[tag=bm.p42nv] run function bm:p42/nv_off',
                      'tag @s remove bm.p42chg', 'scoreboard players set @s bm.hch 0', 'execute if entity @s[tag=bm.p42ward] run function bm:p42/ward/off'])
    aura = {1: ['particle minecraft:flame ~ ~1 ~ 0.35 0.5 0.35 0.01 2', 'particle minecraft:small_flame ~ ~0.3 ~ 0.3 0.1 0.3 0.01 1'],
            2: ['particle minecraft:soul_fire_flame ~ ~1 ~ 0.35 0.5 0.35 0.01 2', 'particle minecraft:snowflake ~ ~0.4 ~ 0.3 0.2 0.3 0.01 1'],
            3: ['particle minecraft:copper_fire_flame ~ ~1 ~ 0.35 0.5 0.35 0.01 2', 'particle minecraft:dust{color:[0.35,0.85,0.2],scale:1.0} ~ ~0.5 ~ 0.3 0.3 0.3 0 1'],
            4: ['particle minecraft:end_rod ~ ~1 ~ 0.35 0.5 0.35 0.01 1', 'particle minecraft:dust{color:[1.0,0.55,0.8],scale:1.0} ~ ~0.8 ~ 0.35 0.5 0.35 0 2']}
    for v in (1, 2, 3, 4):
        fn(f'p42/aura_{v}', aura[v] + [f'execute if score @s bm.hpw matches 2.. run particle {VARIANTS[v][4]} ~ ~2.1 ~ 0.25 0.05 0.25 0.01 2'])
    fn('p42/aura', ['function bm:p42/hv'] + [f'execute if score #hv bm.rng matches {v} run function bm:p42/aura_{v}' for v in (1, 2, 3, 4)] +
       ['execute if score @s bm.hpw matches 3 run particle minecraft:dust{color:[0.7,0.0,0.05],scale:1.3} ~ ~1.1 ~ 0.4 0.6 0.4 0 3'])

    # ================================================================== the Headless Horseman
    fn('p42/boss/summon', [f'summon minecraft:skeleton_horse ~ ~ ~ {snbt(STEED)}',
                           'execute as @e[type=minecraft:wither_skeleton,tag=bm.hh_new] run function bm:p42/boss/init',
                           'tag @e[tag=bm.hh_new] remove bm.hh_new',
                           'execute store result score #hhseen bm.bm run time query gametime',
                           'particle minecraft:large_smoke ~ ~1.5 ~ 1 1.5 1 0.05 60', 'particle minecraft:flame ~ ~1 ~ 1 1 1 0.08 60',
                           'particle minecraft:soul ~ ~0.3 ~ 1.5 0.2 1.5 0.03 30',
                           'execute as @a[distance=..30,gamemode=!spectator] at @s run function bm:p42/boss/sense'])
    fn('p42/boss/init', ['scoreboard players set @s bm.hht 0', 'scoreboard players set @s bm.hhb 0', 'scoreboard players set @s bm.hhl 0',
                         'scoreboard players set @s bm.hhx 0', 'bossbar set bm:hhm color yellow'])
    fn('p42/boss/sense', ['tag @s add bm.hhsensed', 'title @s times 10 70 30', title('@s', 'subtitle', T('You sense an evil presence nearby...', 'dark_red', italic=True)),
                          title('@s', 'title', T('', 'dark_red')), 'playsound minecraft:ambient.cave ambient @s ~ ~ ~ 1 0.9',
                          'playsound minecraft:entity.lightning_bolt.thunder weather @s ~ ~ ~ 0.4 0.5',
                          # his song: disc 13 for everyone he comes near, over any other music
                          'stopsound @s music', 'stopsound @s record', 'playsound minecraft:music_disc.13 record @s ~ ~ ~ 1 1 1'])
    fn('p42/boss/second', ['execute store result score #hhseen bm.bm run time query gametime',
                           'execute unless score #tod bm.bm matches 13000..23199 run return run function bm:p42/boss/retreat',
                           f'execute if entity @a[distance=..128,{near}] run scoreboard players set @s bm.hhx 0',
                           f'execute unless entity @a[distance=..128,{near}] run scoreboard players add @s bm.hhx 1',
                           'execute if score @s bm.hhx matches 90.. run return run function bm:p42/boss/retreat',
                           'execute as @a[distance=..30,tag=!bm.hhsensed,gamemode=!spectator] at @s run function bm:p42/boss/sense',
                           'stopsound @a[tag=bm.hhsensed] music',      # keep the background music quiet while his song plays
                           'bossbar set bm:hhm players @a[distance=..64]', 'bossbar set bm:hhm visible true',
                           'execute store result bossbar bm:hhm value run data get entity @s Health',
                           'execute store result score #hh bm.rng run data get entity @s Health',
                           f'execute if score #hh bm.rng matches ..{HP // 2} unless entity @s[tag=bm.hh_rage] run function bm:p42/boss/enrage',
                           'function bm:p42/boss/ambience',
                           f'execute unless entity @a[distance=..24,{near}] run return 0',
                           'scoreboard players add @s bm.hht 1',
                           'execute if score @s bm.hht matches 3 run function bm:p42/boss/breath_start',
                           'execute if score @s bm.hht matches 6 run function bm:p42/boss/lunge',
                           'execute if score @s bm.hht matches 9 run function bm:p42/boss/minions',
                           'execute if score @s bm.hht matches 11 run function bm:p42/boss/breath_start',
                           'execute if score @s bm.hht matches 13 if entity @s[tag=bm.hh_rage] run function bm:p42/boss/ring',
                           'execute if score @s bm.hht matches 14 run function bm:p42/boss/lunge',
                           'execute if score @s bm.hht matches 16.. run scoreboard players set @s bm.hht 0'])
    fn('p42/boss/fast', ['execute anchored eyes positioned ^ ^-0.4 ^ run particle minecraft:flame ~ ~ ~ 0.12 0.12 0.12 0.02 4',
                         'execute anchored eyes positioned ^ ^-0.2 ^ run particle minecraft:soul_fire_flame ~ ~ ~ 0.08 0.1 0.08 0.01 1',
                         'execute anchored eyes run particle minecraft:large_smoke ~ ~0.1 ~ 0.08 0.15 0.08 0.01 1',
                         'particle minecraft:smoke ~ ~1.4 ~ 0.35 0.7 0.35 0.01 2',
                         'particle minecraft:ash ~ ~2 ~ 6 2 6 0 10',
                         'execute if entity @s[tag=bm.hh_rage] run particle minecraft:flame ~ ~1.6 ~ 0.5 0.9 0.5 0.02 5',
                         'execute if score @s bm.hhb matches 1.. run function bm:p42/boss/breath',
                         'execute if score @s bm.hhl matches 1.. run function bm:p42/boss/lunge_hit'])
    fn('p42/steed/fast', ['particle minecraft:flame ~ ~0.15 ~ 0.55 0.05 0.55 0.02 3', 'particle minecraft:small_flame ~ ~1.5 ~ 0.4 0.4 0.4 0.01 2',
                          'particle minecraft:large_smoke ~ ~0.3 ~ 0.45 0.1 0.45 0.01 1',
                          'execute store result score #r bm.rng run random value 1..6',
                          'execute if score #r bm.rng matches 1 run particle minecraft:lava ~ ~0.2 ~ 0.4 0.05 0.4 0 1',
                          'execute if score #r bm.rng matches 2 run particle minecraft:soul ~ ~0.1 ~ 0.8 0.05 0.8 0.01 1'])
    fn('p42/steed/ridden', ['execute on passengers if entity @s[type=minecraft:wither_skeleton,tag=bm.hhm] run return 1', 'return 0'])
    fn('p42/steed/second', ['execute if function bm:p42/steed/ridden run return run scoreboard players set @s bm.hhx 0',
                            'execute unless score #tod bm.bm matches 13000..23199 run return run function bm:p42/steed/vanish',
                            'scoreboard players add @s bm.hhx 1', 'execute if score @s bm.hhx matches 3.. run function bm:p42/steed/vanish'])
    fn('p42/steed/vanish', ['execute on passengers run ride @s dismount',
                            'particle minecraft:large_smoke ~ ~1 ~ 0.8 1 0.8 0.05 40', 'particle minecraft:flame ~ ~0.5 ~ 0.8 0.5 0.8 0.05 30',
                            'playsound minecraft:entity.skeleton_horse.death hostile @a[distance=..32] ~ ~ ~ 1.2 0.5', 'tp @s ~ -400 ~', 'kill @s'])
    fn('p42/boss/ambience', ['execute store result score #r bm.rng run random value 1..14',
                             'execute if score #r bm.rng matches 1 run playsound minecraft:entity.skeleton_horse.ambient hostile @a[distance=..48] ~ ~ ~ 1.5 0.6',
                             'execute if score #r bm.rng matches 2 run playsound minecraft:entity.witch.celebrate hostile @a[distance=..48] ~ ~ ~ 1.4 0.5',
                             'execute if score #r bm.rng matches 3 run playsound minecraft:ambient.soul_sand_valley.mood ambient @a[distance=..40] ~ ~ ~ 1 1',
                             'execute if score #r bm.rng matches 4 run playsound minecraft:entity.wither.ambient hostile @a[distance=..40] ~ ~ ~ 0.5 0.5',
                             'execute if score #r bm.rng matches 5 run playsound minecraft:block.fire.ambient hostile @a[distance=..24] ~ ~ ~ 2 0.6',
                             'execute if score #r bm.rng matches 6 as @a[distance=..40] at @s run playsound minecraft:ambient.cave ambient @s ~ ~ ~ 0.7 0.7',
                             'execute if score #r bm.rng matches 7 run playsound minecraft:entity.ghast.ambient hostile @a[distance=..40] ~ ~ ~ 0.8 0.5',
                             'execute if score #r bm.rng matches 8 run playsound minecraft:entity.horse.angry hostile @a[distance=..40] ~ ~ ~ 1.2 0.5',
                             'execute if score #r bm.rng matches 9 as @a[distance=..20] at @s run playsound minecraft:entity.warden.heartbeat ambient @s ~ ~ ~ 0.8 0.8'])
    # fire breath from the stump of his neck, at the nearest player (2.5 s)
    fn('p42/boss/breath_start', [f'execute unless entity @a[distance=..14,{near}] run return 0', 'scoreboard players set @s bm.hhb 10',
                                 'playsound minecraft:entity.blaze.shoot hostile @a[distance=..32] ~ ~ ~ 1.5 0.5',
                                 'playsound minecraft:entity.ghast.warn hostile @a[distance=..32] ~ ~ ~ 0.8 0.6'])
    fn('p42/boss/breath', ['scoreboard players remove @s bm.hhb 1', f'execute unless entity @a[distance=..16,{near}] run return 0',
                           'tag @s add bm.hhme', 'scoreboard players set #k bm.rng 0',
                           f'execute anchored eyes positioned ^ ^-0.4 ^0.6 facing entity @p[distance=..18,{near}] eyes run function bm:p42/boss/breath_ray',
                           'tag @s remove bm.hhme', 'tag @a[tag=bm.hhhit] remove bm.hhhit',
                           'playsound minecraft:block.fire.ambient hostile @a[distance=..24] ~ ~ ~ 1.5 0.7'])
    fn('p42/boss/breath_ray', ['scoreboard players add #k bm.rng 1', 'execute unless block ~ ~ ~ #bm:grap_pass run return 0',
                               'execute if score #k bm.rng matches ..4 run particle minecraft:flame ~ ~ ~ 0.1 0.1 0.1 0.03 3',
                               'execute if score #k bm.rng matches 5..10 run particle minecraft:flame ~ ~ ~ 0.25 0.25 0.25 0.04 4',
                               'execute if score #k bm.rng matches 11.. run particle minecraft:flame ~ ~ ~ 0.4 0.4 0.4 0.04 4',
                               'execute if score #k bm.rng matches 8.. run particle minecraft:large_smoke ~ ~0.3 ~ 0.3 0.2 0.3 0.01 1',
                               f'execute as @a[distance=..1.9,tag=!bm.hhhit,{near}] at @s run function bm:p42/boss/burn',
                               'execute if score #k bm.rng matches 18.. run return 0', 'execute positioned ^ ^ ^0.6 run function bm:p42/boss/breath_ray'])
    fn('p42/boss/burn', ['tag @s add bm.hhhit', 'damage @s 4 minecraft:in_fire by @e[type=minecraft:wither_skeleton,tag=bm.hhme,limit=1]',
                         'execute unless predicate bm:p42/burning if block ~ ~ ~ #minecraft:air run function bm:p42/fx/flicker'])
    # the spear charge: the Hellsteed (or he, on foot) lunges at the target; the spear tip hurts for a moment
    fn('p42/boss/lunge', [f'execute unless entity @a[distance=3..18,{near}] run return 0',
                          f'execute if function bm:p42/boss/mounted on vehicle facing entity @p[distance=..20,{near}] feet run function bm:p42/boss/dash',
                          f'execute unless function bm:p42/boss/mounted facing entity @p[distance=..20,{near}] feet run function bm:p42/boss/dash',
                          'scoreboard players set @s bm.hhl 6',
                          'playsound minecraft:item.spear.use hostile @a[distance=..32] ~ ~ ~ 1.5 0.6',
                          'playsound minecraft:entity.horse.angry hostile @a[distance=..32] ~ ~ ~ 1.2 0.6'])
    fn('p42/boss/mounted', ['execute on vehicle if entity @s[type=minecraft:skeleton_horse,tag=bm.hhs] run return 1', 'return 0'])
    fn('p42/boss/dash', ['execute positioned as @s run summon minecraft:marker ^ ^ ^1.6 {Tags:["bm.hhvec"]}',
                         'execute store result score #ax bm.rng run data get entity @e[type=minecraft:marker,tag=bm.hhvec,limit=1] Pos[0] 1000',
                         'execute store result score #az bm.rng run data get entity @e[type=minecraft:marker,tag=bm.hhvec,limit=1] Pos[2] 1000',
                         'execute store result score #sx bm.rng run data get entity @s Pos[0] 1000',
                         'execute store result score #sz bm.rng run data get entity @s Pos[2] 1000',
                         'scoreboard players operation #ax bm.rng -= #sx bm.rng', 'scoreboard players operation #az bm.rng -= #sz bm.rng',
                         'kill @e[type=minecraft:marker,tag=bm.hhvec]',
                         'execute store result entity @s Motion[0] double 0.001 run scoreboard players get #ax bm.rng',
                         'execute store result entity @s Motion[2] double 0.001 run scoreboard players get #az bm.rng',
                         'data modify entity @s Motion[1] set value 0.3d',
                         'particle minecraft:large_smoke ~ ~0.5 ~ 0.6 0.3 0.6 0.05 15'])
    fn('p42/boss/lunge_hit', ['scoreboard players remove @s bm.hhl 1', 'tag @s add bm.hhme',
                              'particle minecraft:crit ^ ^1.4 ^1.6 0.3 0.3 0.3 0.1 5',
                              f'execute positioned ^ ^1 ^1.6 as @a[distance=..2.8,tag=!bm.hhspear,{near}] at @s run function bm:p42/boss/impale',
                              'tag @s remove bm.hhme', 'execute if score @s bm.hhl matches ..0 run tag @a[tag=bm.hhspear] remove bm.hhspear'])
    fn('p42/boss/impale', ['tag @s add bm.hhspear', 'damage @s 9 minecraft:spear by @e[type=minecraft:wither_skeleton,tag=bm.hhme,limit=1]',
                           'execute at @s run playsound minecraft:item.spear.hit hostile @a[distance=..24] ~ ~ ~ 1.4 0.8',
                           'execute at @s run particle minecraft:damage_indicator ~ ~1 ~ 0.3 0.3 0.3 0.1 6'])
    # Pumpkin Thralls (at most 6 near him)
    fn('p42/boss/minions', ['execute store result score #mc bm.rng if entity @e[type=minecraft:skeleton,tag=bm.hhmin,distance=..40]',
                            'execute if score #mc bm.rng matches 6.. run return 0',
                            'playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..32] ~ ~ ~ 1.5 0.6',
                            'playsound minecraft:entity.skeleton.ambient hostile @a[distance=..32] ~ ~ ~ 1.2 0.5',
                            'execute if function bm:p42/boss/mounted on vehicle at @s run function bm:p42/boss/minions_at',
                            'execute unless function bm:p42/boss/mounted run function bm:p42/boss/minions_at'])
    fn('p42/boss/minions_at', ['execute positioned ^2.5 ^ ^-1 run function bm:p42/boss/try_bow',
                               'execute positioned ^-2.5 ^ ^-1 run function bm:p42/boss/try_sword',
                               'execute if entity @e[type=minecraft:wither_skeleton,tag=bm.hhm,tag=bm.hh_rage,distance=..4] positioned ^ ^ ^-3 run function bm:p42/boss/try_bow'])
    for k, nbt in (('bow', THRALL_BOW), ('sword', THRALL_SWORD)):
        fn(f'p42/boss/try_{k}', [f'execute if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:p42/boss/thrall_{k}',
                                 f'execute positioned ~ ~1 ~ if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:p42/boss/thrall_{k}'])
        fn(f'p42/boss/thrall_{k}', [f'summon minecraft:skeleton ~ ~ ~ {snbt(nbt)}', 'particle minecraft:soul ~ ~0.5 ~ 0.4 0.5 0.4 0.03 12',
                                    'particle minecraft:large_smoke ~ ~0.5 ~ 0.4 0.5 0.4 0.03 10'])
    fn('p42/boss/ring', ['playsound minecraft:entity.blaze.shoot hostile @a[distance=..32] ~ ~ ~ 2 0.4',
                         'playsound minecraft:entity.wither.shoot hostile @a[distance=..32] ~ ~ ~ 1 0.5',
                         'execute if function bm:p42/boss/mounted on vehicle at @s run function bm:p42/boss/ring_at',
                         'execute unless function bm:p42/boss/mounted run function bm:p42/boss/ring_at',
                         'tag @s add bm.hhme', f'execute as @a[distance=..8,{near}] at @s run function bm:p42/boss/burn',
                         'tag @s remove bm.hhme', 'tag @a[tag=bm.hhhit] remove bm.hhhit'])
    fn('p42/boss/ring_at', [l for r, n in [(3, 18), (5, 28), (7, 38)] for l in ring(r, n, 0.2, 'minecraft:flame')])
    fn('p42/boss/enrage', ['tag @s add bm.hh_rage', 'effect give @s minecraft:strength infinite 0 true',
                           'attribute @s minecraft:movement_speed modifier add bm:hh_rage 0.25 add_multiplied_base',
                           'execute on vehicle run attribute @s minecraft:movement_speed modifier add bm:hh_rage 0.2 add_multiplied_base',
                           'bossbar set bm:hhm color red',
                           title('@a[distance=..48]', 'actionbar', T('The Horseman\'s fire roars higher!', ORANGE, bold=True)),
                           'playsound minecraft:entity.witch.celebrate hostile @a[distance=..48] ~ ~ ~ 2 0.4',
                           'particle minecraft:flame ~ ~1.5 ~ 1 1.5 1 0.1 80', 'function bm:p42/boss/minions'])
    fn('p42/boss/retreat', [title('@a[distance=..64]', 'actionbar', T('The Headless Horseman rides back into the dark...', ORANGE, italic=True)),
                            'playsound minecraft:entity.witch.celebrate hostile @a[distance=..64] ~ ~ ~ 1.5 0.4',
                            'playsound minecraft:entity.skeleton_horse.ambient hostile @a[distance=..64] ~ ~ ~ 1.5 0.5',
                            'particle minecraft:large_smoke ~ ~1.5 ~ 1 1.5 1 0.05 80', 'particle minecraft:flame ~ ~1 ~ 1 1 1 0.05 40',
                            'function bm:p42/boss/cleanup', 'execute on vehicle run function bm:p42/steed/vanish', 'tp @s ~ -400 ~', 'kill @s'])
    fn('p42/boss/cleanup', ['stopsound @a[tag=bm.hhsensed] record minecraft:music_disc.13',
                            'execute as @e[type=minecraft:skeleton,tag=bm.hhmin,distance=..96] at @s run function bm:p42/boss/crumble',
                            'tag @a remove bm.hhsensed', 'bossbar set bm:hhm visible false'])
    fn('p42/boss/crumble', ['particle minecraft:soul ~ ~1 ~ 0.3 0.6 0.3 0.03 10', 'particle minecraft:large_smoke ~ ~1 ~ 0.3 0.6 0.3 0.03 8', 'tp @s ~ -400 ~', 'kill @s'])

    # his fall: the loot (his head, always - 2.34), a cheer for everyone near
    wjson('bm/loot_table/p42/horseman.json', {'type': 'minecraft:entity', 'pools': [
        {'rolls': 1, 'entries': [G.loot_entry('horseman_head')], 'conditions': [G.KILLED]},
        {'rolls': 1, 'entries': [G.loot_entry('token', G.uni(10, 16))], 'conditions': [G.KILLED]},
        {'rolls': 1, 'entries': [G.loot_entry('medallion', G.uni(2, 4))], 'conditions': [G.KILLED]},
        {'rolls': 1, 'entries': [G.loot_entry('trophy')], 'conditions': [G.KILLED, G.chance(0.4)]},
        {'rolls': 1, 'entries': [G.loot_entry('heartstone')], 'conditions': [G.KILLED, G.chance(0.15)]},
        # (no vanilla jack o'lanterns: they were mistaken for his head)
        {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:pumpkin_pie', 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(2, 5)}]}]},
        {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:netherite_scrap'}], 'conditions': [G.KILLED, G.chance(0.5)]}]})
    wjson('bm/advancement/p42/slain.json', {'criteria': {'slain': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["bm.hhm"]}'}}]}}},
        'rewards': {'function': 'bm:p42/slain'}})
    fn('p42/slain', ['advancement revoke @s only bm:p42/slain',
                     tellraw('@a[distance=..160]', PREFIX + [T('The Headless Horseman has fallen to ', ORANGE), {'selector': '@s', 'color': 'gold'}, T('!', ORANGE)]),
                     'scoreboard players set @a[distance=..64] bm.hhv 20',
                     'execute as @e[type=minecraft:skeleton,tag=bm.hhmin,distance=..96] at @s run function bm:p42/boss/crumble',
                     'stopsound @a[tag=bm.hhsensed] record minecraft:music_disc.13', 'tag @a remove bm.hhsensed', 'bossbar set bm:hhm visible false',
                     'summon minecraft:experience_orb ~ ~1 ~ {Value:60s}', 'summon minecraft:experience_orb ~ ~1 ~ {Value:60s}',
                     'summon minecraft:experience_orb ~ ~1 ~ {Value:60s}'])
    fn('p42/victory', ['scoreboard players reset @s bm.hhv', 'title @s times 10 70 20',
                       title('@s', 'subtitle', T('...but somewhere, a head is still grinning.', 'gray', italic=True)),
                       title('@s', 'title', T('THE HORSEMAN FALLS', ORANGE, bold=True)),
                       'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1'])
    tick += ['execute as @a[scores={bm.hhv=1}] at @s run function bm:p42/victory', 'scoreboard players remove @a[scores={bm.hhv=2..}] bm.hhv 1',
             'execute as @a[tag=bm.p42chg] at @s run function bm:p42/blast/check']

    # ---------------- when he rides: the Overworld night, after the grace days, rarely (far less rarely under a full or new moon)
    fn('p42/spawn/check', ['scoreboard players set #hhchk bm.bm 0',
                           'execute unless score #tod bm.bm matches 13000..21999 run return 0',
                           f'execute if score #day bm.bm matches ..{GRACE_DAYS - 1} run return 0',
                           'execute if entity @e[type=minecraft:wither_skeleton,tag=bm.hhm] run return 0',
                           # still out there in a chunk nobody has loaded? wait for him to show or ride off
                           'execute store result score #now bm.rng run time query gametime',
                           'scoreboard players operation #gap bm.rng = #now bm.rng', 'scoreboard players operation #gap bm.rng -= #hhseen bm.bm',
                           'execute if score #hhseen bm.bm matches 1.. if score #gap bm.rng matches 0..2399 run return 0',
                           f'execute store result score #r bm.rng run random value 1..{ODDS_NIGHT}',
                           f'execute if score #mph bm.bm matches 0 store result score #r bm.rng run random value 1..{ODDS_MOON}',
                           f'execute if score #mph bm.bm matches 4 store result score #r bm.rng run random value 1..{ODDS_MOON}',
                           'execute unless score #r bm.rng matches 1 run return 0',
                           f'execute in minecraft:overworld positioned 0 0 0 as @r[distance=0..,{near}] at @s run function bm:p42/spawn/try'])
    fn('p42/spawn/try', ['execute positioned ~ ~1.6 ~ unless predicate bm:sees_sky run return 0',
                         'execute store result storage bm:tmp hh.a int 1 run random value 0..359',
                         'function bm:p42/spawn/at with storage bm:tmp hh'])
    fn('p42/spawn/at', ['$execute rotated $(a) 0 positioned ^ ^ ^24 positioned over motion_blocking_no_leaves run function bm:p42/spawn/place'])
    fn('p42/spawn/place', ['execute if block ~ ~-1 ~ minecraft:water run return 0', 'execute if block ~ ~-1 ~ minecraft:lava run return 0',
                           'execute if block ~ ~-1 ~ #minecraft:leaves run return 0'] +
       [f'execute unless block ~ ~{y} ~ #bm:grap_pass run return 0' for y in range(4)] +
       ['execute if block ~ ~ ~ minecraft:water run return 0', 'execute unless function bm:p37/allowed run return 0', 'function bm:p42/boss/summon'])

    # ---------------- the clock: power tier, holders, the Horseman, the spawn roll
    second += ['scoreboard players set #hpw bm.bm 0',
               'execute if score #tod bm.bm matches 13000..22999 run scoreboard players set #hpw bm.bm 1',
               'scoreboard players operation #mph bm.bm = #day bm.bm', 'scoreboard players operation #mph bm.bm %= #8 bm.bm',
               'execute if score #hpw bm.bm matches 1 if score #mph bm.bm matches 0 run scoreboard players set #hpw bm.bm 2',
               'execute if score #hpw bm.bm matches 1 if score #mph bm.bm matches 4 run scoreboard players set #hpw bm.bm 2',
               'execute if score #active bm.bm matches 1 run scoreboard players set #hpw bm.bm 3',
               'execute as @a[gamemode=!spectator] if items entity @s weapon.mainhand ' + HEAD + ' at @s run function bm:p42/held',
               'execute as @e[type=minecraft:wither_skeleton,tag=bm.hhm] at @s run function bm:p42/boss/second',
               'execute as @e[type=minecraft:skeleton_horse,tag=bm.hhs] at @s run function bm:p42/steed/second',
               'execute unless entity @e[type=minecraft:wither_skeleton,tag=bm.hhm] run bossbar set bm:hhm visible false',
               'scoreboard players add #hhchk bm.bm 1', 'execute if score #hhchk bm.bm matches 20.. run function bm:p42/spawn/check']
    fast += ['execute as @a[tag=bm.p42on] unless items entity @s weapon.mainhand ' + HEAD + ' run function bm:p42/unheld',
             'execute as @a[tag=bm.p42on,scores={bm.hpw=1..}] at @s run function bm:p42/aura',
             'execute as @a[scores={bm.hcd=1..}] at @s run function bm:p42/cool',
             'execute as @a[scores={bm.hfu=..199,bm.hcd=..0}] run function bm:p42/refuel',
             'scoreboard players remove @a[scores={bm.hbc=1..}] bm.hbc 5', 'scoreboard players remove @a[scores={bm.hzc=1..}] bm.hzc 5',
             'execute as @e[type=minecraft:wither_skeleton,tag=bm.hhm] at @s run function bm:p42/boss/fast',
             'execute as @e[type=minecraft:skeleton_horse,tag=bm.hhs] at @s run function bm:p42/steed/fast',
             'execute as @e[type=minecraft:marker,tag=bm.hzone] at @s run function bm:p42/zone/tick']

    # ---------------- admin
    fn('admin/horseman', ['execute rotated ~ 0 positioned ^ ^ ^10 positioned over motion_blocking_no_leaves run function bm:p42/boss/summon',
                          tellraw('@s', PREFIX + [T('The Headless Horseman rides out 10 blocks ahead. He leaves at dawn.', 'gray')])])
    fn('admin/horseman_heads', [give(VARIANTS[v][0]) for v in (1, 2, 3, 4)])
    G.FUNCS['admin/help'] += [tellraw('@s', [T('/function bm:admin/horseman', 'yellow'), T('  the Headless Horseman, 10 blocks ahead', 'gray')]),
                              tellraw('@s', [T('/function bm:admin/horseman_heads', 'yellow'), T('  all four of his heads', 'gray')])]
    G.FUNCS['admin/uninstall'].insert(0, 'bossbar remove bm:hhm')

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


# ===================================================================== resource pack: four carved heads
FACE = ['................', '................', '................', '...#........#...', '...##......##...', '...###....###...',
        '....###..###....', '................', '.......##.......', '..#..........#..', '..##.#.##.#.##..', '..############..',
        '...##.#..#.##...', '................', '................', '................']
SKIN = {1: None, 2: ('#26303a', '#8ea6b8'), 3: ('#1d3a30', '#5ab08a'), 4: ('#a89878', '#fff6e4')}
GLOW = {1: ('#c85a00', '#ffb000', '#fff2a0'), 2: ('#1a7a98', '#40e0ff', '#e0ffff'), 3: ('#2e8a18', '#8aff3a', '#eeffb8'),
        4: ('#b82a5a', '#ff6aa8', '#ffe4f2')}
VANILLA = '/home/claude/mc263/client.jar'


def _vanilla(name):
    import io, zipfile
    from PIL import Image
    with zipfile.ZipFile(VANILLA) as z:
        return Image.open(io.BytesIO(z.read(f'assets/minecraft/textures/block/{name}.png'))).convert('RGBA')


def _hex(c):
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


def _reskin(im, v):
    if SKIN[v] is None:
        return im.copy()
    lo, hi = _hex(SKIN[v][0]), _hex(SKIN[v][1])
    out = im.copy()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = im.getpixel((x, y))
            t = min(1.0, max(0.0, (0.3 * r + 0.59 * g + 0.11 * b - 50) / 170))
            out.putpixel((x, y), tuple(int(lo[i] + (hi[i] - lo[i]) * t) for i in range(3)) + (a,))
    return out


def textures():
    from PIL import Image
    side, top = _vanilla('pumpkin_side'), _vanilla('pumpkin_top')
    out = {}
    for v in (1, 2, 3, 4):
        sk = _reskin(side, v)
        out[f'hh_side_{v}'] = sk
        out[f'hh_top_{v}'] = _reskin(top, v)
        face, glow = sk.copy(), Image.new('RGBA', (16, 16), (0, 0, 0, 0))
        edge, mid, core = (_hex(c) for c in GLOW[v])
        on = lambda x, y: 0 <= x < 16 and 0 <= y < 16 and FACE[y][x] == '#'
        for y in range(16):
            for x in range(16):
                if not on(x, y):
                    continue
                n = sum(on(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                c = core if n >= 3 else (mid if n == 2 else edge)
                if y >= 10 and n >= 2:
                    c = mid
                face.putpixel((x, y), c + (255,))
                glow.putpixel((x, y), c + (255,))
        out[f'hh_face_{v}'] = face
        out[f'hh_glow_{v}'] = glow
    return out


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    R.LANG.update({'death.attack.bm.hellfire': '%1$s was consumed by hellfire', 'death.attack.bm.hellfire.player': '%1$s was consumed by %2$s\'s hellfire',
                   'death.attack.bm.soulfrost': '%1$s was frozen by soul fire', 'death.attack.bm.soulfrost.player': '%1$s was frozen solid by %2$s\'s soul fire',
                   'death.attack.bm.venomfire': '%1$s was melted by venomous fire', 'death.attack.bm.venomfire.player': '%1$s was melted by %2$s\'s venomous fire',
                   'death.attack.bm.hallowed': '%1$s was seared by holy light', 'death.attack.bm.hallowed.player': '%1$s was seared by %2$s\'s holy light'})

    def post(R2):
        full = [0, 0, 16, 16]
        disp = {'gui': {'rotation': [30, 225, 0], 'translation': [0, 0, 0], 'scale': [0.95, 0.95, 0.95]},
                'ground': {'rotation': [0, 0, 0], 'translation': [0, 3, 0], 'scale': [0.4, 0.4, 0.4]},
                'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [0.8, 0.8, 0.8]},
                'thirdperson_righthand': {'rotation': [75, 45, 0], 'translation': [0, 2.5, 0], 'scale': [0.6, 0.6, 0.6]},
                'thirdperson_lefthand': {'rotation': [75, 45, 0], 'translation': [0, 2.5, 0], 'scale': [0.6, 0.6, 0.6]},
                'firstperson_righthand': {'rotation': [0, 45, 0], 'translation': [0, 1, 0], 'scale': [0.64, 0.64, 0.64]},
                'firstperson_lefthand': {'rotation': [0, 225, 0], 'translation': [0, 1, 0], 'scale': [0.64, 0.64, 0.64]}}
        for v, (iid, *_r) in VARIANTS.items():
            sides = {f: {'uv': full, 'texture': '#side'} for f in ('south', 'east', 'west')}
            model = {'textures': {'face': f'bm:block/hh_face_{v}', 'glow': f'bm:block/hh_glow_{v}', 'side': f'bm:block/hh_side_{v}',
                                  'top': f'bm:block/hh_top_{v}', 'particle': f'bm:block/hh_side_{v}'},
                     'elements': [{'from': [3, 3, 3], 'to': [13, 13, 13], 'faces': dict(sides, north={'uv': full, 'texture': '#face'},
                                                                                       up={'uv': full, 'texture': '#top'}, down={'uv': full, 'texture': '#top'})},
                                  {'from': [3, 3, 2.95], 'to': [13, 13, 2.95], 'shade': False, 'light_emission': 15,
                                   'faces': {'north': {'uv': full, 'texture': '#glow'}}},
                                  {'from': [7, 13, 7], 'to': [9, 15, 9],
                                   'faces': {f: {'uv': [7, 7, 9, 9], 'texture': '#top'} for f in ('north', 'south', 'east', 'west', 'up')}}],
                     'display': disp}
            R2.wj(f'assets/bm/models/item/{iid}.json', model)
            R2.wj(f'assets/bm/items/{iid}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/{iid}'}})
    R.POST.append(post)

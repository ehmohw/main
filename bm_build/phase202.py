"""2.92: THE UNDERWATER KINGDOM'S ARMOURY - endgame gear for the castle under the sea (art: kingdom_art.py, from the owner's art).

LEO'S AEGIS (shield)    Sir Leo's own, the kingdom's insignia on its face. Bring LEO to the Tide Font once you're a KNIGHT OF
                        THE TIDE: he gives it to you. A shield that hits back:
                          a weapon too - 12 damage swung (and +4 armour, +2 toughness, Resistance, held in either hand);
                          RIPOSTE - a blow you block on it is paid back: 10 damage and a shove to whoever struck (and Strength);
                          TIDAL CHARGE - sneak + jump with it: you charge 7 blocks behind it, 14 damage and a hurl to every
                          monster in your way (6 s);
                          its BULWARK - your followers near you share its Resistance.
EMMA'S CRESCENT (axe)   Emma's own crescent axe from her ethereal days. Bring EMMA to the Font once the castle is RESTORED
                        and you're a ROYAL CHAMPION: she gives it to you. 20 damage, quick on its feet (+10% speed held):
                          every third blow looses an ETHEREAL CRESCENT - a wave of light 8 blocks ahead (10 to each monster);
                          use: ETHEREAL STEP - a blink 6 blocks where you look (4 s);
                          sneak + use: BLOOM SLAM - a crash of petals round you: 16 to monsters within 5 (tossed in the
                          air), Regeneration II and Absorption for you and your friends (12 s).
                        (Lost either? The Font calls it back for 32 Royal Pearls, with the same friend beside you.)
THE CROWN OF THE DEEP   now its own crown, as drawn: sea-gold, four arches, a violet diamond, sea-blue gems (kingdom_art.py).
TIDEWARDEN PLATE        Leo's knights' armour: steel-blue plate trimmed in sea-glass, the insignia on the breast, a great
                        helm with a fin crest. Heavy: 4/10/8/4 armour, 4 toughness and +2 health a piece; the whole set:
                        Resistance; in water Water Breathing, Dolphin's Grace and Conduit Power; TIDEWALL - hurt below 4
                        hearts, a wall of water: Absorption III and every monster near you thrown back (90 s).
PEARLGUARD REGALIA      the royal family's guard: pearl-white scale trimmed in rose, a pearl tiara with Emma's flower.
                        Light: 3/8/6/3 armour, 3 toughness, +1 damage and +7% speed a piece; the whole set: Strength, Jump
                        Boost, Regeneration in water; PEARL'S GRACE - hurt below 4 hearts, you vanish in a burst of pearls:
                        Invisibility, Speed III and Regeneration II (90 s).
  Both sets are the Royal Steward's (Royal Pearls, TIDE SCALES and netherite for the chest and legs).
TIDE SCALES             the kingdom's armoury coin: 3 for everyone who holds off a dome breach, 1 from each Tide Raider,
                        1-2 in the daily tribute, a few in the towers' chests.
FROM CECIL TO THE STEWARD   LEO'S TRIDENT (stronger now: 12/10 damage, Impaling V; in water Strength II and Resistance) and
                        EMMA'S BLOOMHEART (Regeneration III, Absorption, a 30 s recharge) are the Royal Steward's now."""
from items import item, T, TOTEM, ITEMS, attr, ench
from useitem import hold, HOLD
from nbt import snbt, B, F, Int
import math

KC, GLASS, ROSE, GOLD = '#5ac8ff', '#a6dcea', '#ff5ac8', '#ffd66a'
UNBR = {'minecraft:unbreakable': {}}
holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'

item('tide_scale', TOTEM, 'Tide Scale', GLASS,
     ['A scale of sea-glass from the kingdom\'s armoury.', ('The Royal Steward takes them for the', 'aqua'), ('Tidewarden and Pearlguard armour.', 'aqua'),
      ('Won holding off dome breaches, from Tide', 'gray'), ('Raiders, the tribute and the towers.', 'gray')],
     model='bm:tide_scale', stack=64, cat='currency')

item('leo_aegis', 'minecraft:shield', "Leo's Aegis", '#86a6c4',
     ['Sir Leo\'s shield, the kingdom\'s insignia on its face.', ('A weapon too: 12 damage swung. Held: +4 armour,', 'blue'),
      ('+2 toughness, Resistance - your followers near', 'blue'), ('you share it.', 'blue'),
      ('RIPOSTE: a blow blocked on it is paid back -', 'aqua'), ('10 damage and a shove (and Strength for you).', 'aqua'),
      ('TIDAL CHARGE: sneak + jump - charge 7 blocks,', 'aqua'), ('14 to every monster in the way (6 s).', 'aqua'),
      ('Given by Leo at the Tide Font.', 'dark_gray')],
     stack=1, cat='weapon', tier=3, bold=True,
     comps=dict(UNBR, **{'minecraft:item_model': 'bm:leo_aegis',
                         'minecraft:attribute_modifiers': [attr('attack_damage', 11, 'mainhand', ident='minecraft:base_attack_damage'),
                                                           attr('attack_speed', -2.7, 'mainhand', ident='minecraft:base_attack_speed'),
                                                           attr('armor', 4, 'hand'), attr('armor_toughness', 2, 'hand'), attr('knockback_resistance', 0.2, 'hand')]}))
item('emma_crescent', 'minecraft:netherite_axe', "Emma's Crescent", '#ff7ae0',
     ['Emma\'s crescent axe, from her ethereal days.', ('20 damage; +10% speed held.', 'blue'),
      ('Every third blow: an ETHEREAL CRESCENT - a wave', 'aqua'), ('of light 8 blocks ahead (10 to each monster).', 'aqua'),
      ('Use: ETHEREAL STEP - a blink where you look (4 s).', 'aqua'),
      ('Sneak + use: BLOOM SLAM - 16 to monsters round', 'aqua'), ('you, tossed high; Regeneration II and Absorption', 'aqua'),
      ('for you and your friends (12 s).', 'aqua'), ('Given by Emma at the Tide Font.', 'dark_gray')],
     stack=1, cat='weapon', tier=3, bold=True,
     comps=dict(UNBR, **hold('none'), **{'minecraft:item_model': 'bm:emma_crescent', 'minecraft:enchantments': ench(sharpness=5),
                                          'minecraft:attribute_modifiers': [attr('attack_damage', 16, 'mainhand', ident='minecraft:base_attack_damage'),
                                                                            attr('attack_speed', -2.8, 'mainhand', ident='minecraft:base_attack_speed'),
                                                                            attr('movement_speed', 0.1, 'mainhand', 'add_multiplied_base')]}))
HOLD['emma_crescent'] = 'bm:p202/cres/use'

# the armour: (key, name, colour, set) per piece
SETS = {
    'tidewarden': ('Tidewarden', '#86a6c4', {'head': (4, 4), 'chest': (10, 4), 'legs': (8, 4), 'feet': (4, 4)},
                   [('Leo\'s knights\' plate, trimmed in sea-glass.', 'gray')],
                   [('Whole set: Resistance; in water Water Breathing,', 'aqua'), ("Dolphin's Grace, Conduit Power. TIDEWALL: hurt", 'aqua'),
                    ('below 4 hearts - Absorption III, monsters thrown', 'aqua'), ('back (90 s).', 'aqua')]),
    'pearlguard': ('Pearlguard', '#ece6f0', {'head': (3, 3), 'chest': (8, 3), 'legs': (6, 3), 'feet': (3, 3)},
                   [('The royal family\'s guard: pearl-white, rose-trimmed.', 'gray')],
                   [('Whole set: Strength, Jump Boost; Regeneration in', 'aqua'), ("water. PEARL'S GRACE: hurt below 4 hearts - you", 'aqua'),
                    ('vanish in pearls: Invisibility, Speed III,', 'aqua'), ('Regeneration II (90 s).', 'aqua')])}
PIECE = {'head': ('helmet', 'Helm'), 'chest': ('chestplate', 'Breastplate'), 'legs': ('leggings', 'Greaves'), 'feet': ('boots', 'Sabatons')}
ARMOR_IDS = []
for _s, (_nm, _col, _st, _lore, _bonus) in SETS.items():
    for _slot, (_a, _t) in _st.items():
        _base, _pn = PIECE[_slot]
        if _s == 'pearlguard' and _slot == 'head': _pn = 'Tiara'
        _iid = f'{_s}_{_slot}'
        ARMOR_IDS.append(_iid)
        _mods = [attr('armor', _a, _slot, ident=f'minecraft:armor.{_base}'), attr('armor_toughness', _t, _slot, ident=f'minecraft:armor.{_base}_toughness')]
        if _s == 'tidewarden':
            _mods += [attr('knockback_resistance', 0.15, _slot, ident=f'minecraft:armor.{_base}_kb'), attr('max_health', 2, _slot)]
        else:
            _mods += [attr('attack_damage', 1, _slot), attr('movement_speed', 0.07, _slot, 'add_multiplied_base')]
        if _slot == 'head':
            _eq = {'slot': 'head', 'equip_sound': 'minecraft:item.armor.equip_netherite'}
            _model = 'bm:tidewarden_helm' if _s == 'tidewarden' else 'bm:pearlguard_tiara'
        else:
            _eq = {'slot': _slot, 'asset_id': f'bm:{_s}', 'equip_sound': 'minecraft:item.armor.equip_netherite'}
            _model = f'bm:{_s}_{_slot if _slot != "feet" else "boots"}'
        item(_iid, f'minecraft:netherite_{_base}', f'{_nm} {_pn}', _col,
             _lore + [(f'{_a} armour, {_t} toughness, ' + ('+2 health.' if _s == 'tidewarden' else '+1 damage, +7% speed.'), 'blue')] + _bonus +
             [('Unbreakable. The Royal Steward\'s.', 'dark_gray')],
             stack=1, cat='gear', tier=3, custom_extra={'bm_set': _s},
             comps=dict(UNBR, **{'minecraft:item_model': _model, 'minecraft:equippable': _eq, 'minecraft:attribute_modifiers': _mods,
                                 'minecraft:enchantments': ench(protection=4)}))

# the Crown of the Deep: its own 3D crown now (still a turtle helmet underneath - its Water Breathing - but drawn as the crown)
_cr = ITEMS['crown_of_the_deep']['comps']
_cr['minecraft:item_model'] = 'bm:crown_of_the_deep'
_cr['minecraft:equippable'] = {'slot': 'head', 'equip_sound': 'minecraft:item.armor.equip_gold'}

# Leo's Trident and Emma's Bloomheart, stronger, and the Steward's now
for _i, _d, _imp in (('leo_trident', 12, True), ('leo_spear', 10, False)):
    _c = ITEMS[_i]['comps']
    for m in _c['minecraft:attribute_modifiers']:
        if m['type'] == 'minecraft:attack_damage': m['amount'] = float(_d - 1)
    if _imp: _c['minecraft:enchantments']['minecraft:impaling'] = 5
    _c['minecraft:lore'][0:0] = [T('Kingdom-forged anew: stronger, sharper.', '#5ac8ff')]


ITEMS['bloomheart_gem']['comps']['minecraft:lore'][2:5] = [T('Right-click: a ring of blossom - you and', 'blue'), T('everyone within 8 blocks get Regeneration III', 'blue'),
                                                           T('and Absorption II for 10 seconds. 30 second', 'blue'), T('recharge. (Kingdom-blessed, 2.92)', 'blue')]


def extend_offers(O, offer):
    O['wizard'] = [o for o in O['wizard'] if o['sell'].get('components', {}).get('minecraft:custom_data', {}).get('bm') not in ('leo_trident', 'bloomheart_gem')]


# the Steward's armoury trades (phase199 adds them to his shop)
def steward_offers(offer):
    out = [offer(('royal_pearl', 30), ('leo_trident', 1), ('heartstone', 2)), offer(('royal_pearl', 20), ('bloomheart_gem', 1))]
    price = {'head': (20, 6, None), 'chest': (32, 10, ('netherite_ingot', 1)), 'legs': (28, 8, ('netherite_ingot', 1)), 'feet': (18, 6, None)}
    for s in SETS:
        for slot, (pp, sc, extra) in price.items():
            out.append(offer(('royal_pearl', pp), (f'{s}_{slot}', 1), extra or ('tide_scale', sc)))
    return out


def generate(G):
    fn, title, tellraw, give, P, wjson = G.fn, G.title, G.tellraw, G.give, G.PREFIX, G.wjson
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    tick, second = G.FUNCS['tick'], G.FUNCS['loop/second']
    foe = 'type=#bm:hostile,tag=!bm.npc'
    objs = ['bm.agblk minecraft.custom:minecraft.damage_blocked_by_shield',
            'bm.agcd dummy', 'bm.crh dummy', 'bm.crcd2 dummy', 'bm.crst dummy', 'bm.twcd dummy', 'bm.pgcd dummy']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o}' for o in objs]
    G.OBJECTIVES += [o.split()[0] for o in objs]
    for o in ('bm.agcd', 'bm.crcd2', 'bm.crst', 'bm.twcd', 'bm.pgcd'):
        tick.append(f'scoreboard players remove @a[scores={{{o}=1..}}] {o} 1')
    aegis = lambda slot: f'items entity @s {slot} {holds("leo_aegis")}'

    # ---------------------------------------------------------------- LEO'S AEGIS
    second += [f'execute as @a if {aegis("weapon.mainhand")} at @s run function bm:p202/aegis/held',
               f'execute as @a unless {aegis("weapon.mainhand")} if {aegis("weapon.offhand")} at @s run function bm:p202/aegis/held']
    fn('p202/aegis/held', ['effect give @s minecraft:resistance 2 0 true', 'scoreboard players operation #me bm.pid = @s bm.pid',
                           'execute as @e[type=#bm:p42_ally,distance=..10] if score @s bm.pid = #me bm.pid run effect give @s minecraft:resistance 2 0 true'])
    tick.append('execute as @a[scores={bm.agblk=1..}] at @s run function bm:p202/aegis/blocked')
    fn('p202/aegis/blocked', ['scoreboard players reset @s bm.agblk',
                              f'execute unless {aegis("weapon.mainhand")} unless {aegis("weapon.offhand")} run return 0',
                              'tag @s add bm.agme', f'execute as @e[{foe},distance=..5,sort=nearest,limit=1] at @s run function bm:p202/aegis/riposte',
                              'tag @s remove bm.agme', 'effect give @s minecraft:strength 3 0 true',
                              'playsound minecraft:item.shield.block player @a[distance=..16] ~ ~ ~ 1 0.7',
                              'playsound minecraft:entity.player.splash.high_speed player @a[distance=..16] ~ ~ ~ 0.6 1.4'])
    fn('p202/aegis/riposte', ['damage @s 10 minecraft:player_attack by @p[tag=bm.agme]', 'particle minecraft:splash ~ ~1 ~ 0.4 0.6 0.4 0.2 30',
                              'particle minecraft:bubble_pop ~ ~1 ~ 0.3 0.5 0.3 0.05 16',
                              'execute facing entity @p[tag=bm.agme] feet rotated ~180 0 run tp @s ^ ^0.4 ^1.6'])
    # sneak + jump: the jump key pressed while the sneak key is held (the client's own input; once per press)
    wjson('bm/predicate/p202/sneak_jump.json', {'condition': 'minecraft:entity_properties', 'entity': 'this',
                                                 'predicate': {'minecraft:type_specific/player': {'input': {'jump': True, 'sneak': True}}}})
    tick += ['execute as @a[tag=bm.kgjd] unless predicate bm:p202/sneak_jump run tag @s remove bm.kgjd',
             'execute as @a[tag=!bm.kgjd] if predicate bm:p202/sneak_jump at @s run function bm:p202/jump']
    fn('p202/jump', ['tag @s add bm.kgjd',
                     f'execute if {aegis("weapon.mainhand")} run return run function bm:p202/aegis/charge',
                     f'execute if {aegis("weapon.offhand")} run return run function bm:p202/aegis/charge'])
    wjson('bm/tags/block/p202_pass.json', {'values': ['#minecraft:air', 'minecraft:water', 'minecraft:short_grass', 'minecraft:tall_grass', 'minecraft:snow',
                                                     'minecraft:seagrass', 'minecraft:tall_seagrass', 'minecraft:kelp', 'minecraft:kelp_plant', '#minecraft:flowers',
                                                     'minecraft:fern', 'minecraft:large_fern', 'minecraft:dead_bush', 'minecraft:light']})
    fn('p202/aegis/charge', ['execute if score @s bm.agcd matches 1.. run return run ' + say('The Aegis is still steadying...', '#86a6c4'),
                             'scoreboard players set @s bm.agcd 120', 'tag @s add bm.agme', 'scoreboard players set #ag bm.rng 0',
                             'playsound minecraft:item.trident.riptide_1 player @a[distance=..20] ~ ~ ~ 1 0.8',
                             'execute rotated ~ 0 run function bm:p202/aegis/step',
                             'tag @e[tag=bm.aghit] remove bm.aghit', 'tag @s remove bm.agme',
                             'particle minecraft:splash ~ ~1 ~ 0.6 0.6 0.6 0.3 50', 'playsound minecraft:entity.generic.splash player @a[distance=..20] ~ ~ ~ 1 0.7'])
    fn('p202/aegis/step', ['scoreboard players add #ag bm.rng 1', 'execute if score #ag bm.rng matches 8.. run return 0',
                           'execute positioned ^ ^ ^1 unless block ~ ~ ~ #bm:p202_pass run return 0',
                           'execute positioned ^ ^ ^1 unless block ~ ~1 ~ #bm:p202_pass run return 0',
                           'tp @s ^ ^ ^1', 'particle minecraft:bubble_pop ~ ~1 ~ 0.4 0.5 0.4 0.05 10', 'particle minecraft:cloud ~ ~0.5 ~ 0.3 0.2 0.3 0.02 4',
                           f'execute as @e[{foe},tag=!bm.aghit,distance=..2.2] at @s run function bm:p202/aegis/rammed',
                           'execute at @s run function bm:p202/aegis/step'])
    fn('p202/aegis/rammed', ['tag @s add bm.aghit', 'damage @s 14 minecraft:player_attack by @p[tag=bm.agme]',
                             'execute facing entity @p[tag=bm.agme] feet rotated ~180 0 run tp @s ^ ^0.6 ^2.5', 'particle minecraft:crit ~ ~1 ~ 0.3 0.4 0.3 0.2 12',
                             'playsound minecraft:item.shield.block neutral @a[distance=..16] ~ ~ ~ 1 0.5'])

    # ---------------------------------------------------------------- EMMA'S CRESCENT
    wjson('bm/advancement/p202/crescent_hit.json', {'criteria': {'hit': {'trigger': 'minecraft:player_hurt_entity', 'conditions': {'player': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'equipment': {'mainhand': {'predicates': {'minecraft:custom_data': '{bm:"emma_crescent"}'}}}}}]}}},
        'rewards': {'function': 'bm:p202/cres/hit'}})
    fn('p202/cres/hit', ['advancement revoke @s only bm:p202/crescent_hit', 'scoreboard players add @s bm.crh 1',
                         'execute if score @s bm.crh matches 3.. at @s run function bm:p202/cres/wave'])
    fn('p202/cres/wave', ['scoreboard players set @s bm.crh 0', 'tag @s add bm.crme', 'scoreboard players set #cw bm.rng 0',
                          'playsound minecraft:entity.player.attack.sweep player @a[distance=..20] ~ ~ ~ 1 0.6',
                          'playsound minecraft:block.amethyst_block.chime player @a[distance=..20] ~ ~ ~ 1 1.6',
                          'execute anchored eyes positioned ^ ^-0.4 ^1 run function bm:p202/cres/wstep', 'tag @e[tag=bm.crhit] remove bm.crhit', 'tag @s remove bm.crme'])
    fn('p202/cres/wstep', ['scoreboard players add #cw bm.rng 1', 'execute if score #cw bm.rng matches 9.. run return 0',
                           'particle minecraft:end_rod ^-1 ^ ^ 0 0 0 0 1', 'particle minecraft:end_rod ^1 ^ ^ 0 0 0 0 1', 'particle minecraft:end_rod ^ ^ ^ 0 0 0 0 1',
                           'particle minecraft:cherry_leaves ^ ^ ^ 0.8 0.3 0.2 0 3', 'particle minecraft:dust{color:[1.0,0.55,0.9],scale:1.4} ^-0.6 ^0.2 ^ 0 0 0 0 1',
                           'particle minecraft:dust{color:[0.65,0.86,0.92],scale:1.4} ^0.6 ^0.2 ^ 0 0 0 0 1',
                           f'execute as @e[{foe},tag=!bm.crhit,distance=..1.8] run function bm:p202/cres/cut',
                           'execute positioned ^ ^ ^1 run function bm:p202/cres/wstep'])
    fn('p202/cres/cut', ['tag @s add bm.crhit', 'damage @s 10 minecraft:magic by @p[tag=bm.crme]'])
    fn('p202/cres/use', [f'execute unless items entity @s weapon.mainhand {holds("emma_crescent")} run return 0',
                         'execute if predicate bm:p20/sneaking run return run function bm:p202/cres/slam', 'function bm:p202/cres/step'])
    fn('p202/cres/step', ['execute if score @s bm.crst matches 1.. run return 0', 'scoreboard players set @s bm.crst 80',
                          'particle minecraft:dust{color:[0.9,0.7,1.0],scale:1.6} ~ ~1 ~ 0.3 0.6 0.3 0 20', 'scoreboard players set #cs bm.rng 0',
                          'execute rotated ~ 0 run function bm:p202/cres/blink', 'particle minecraft:end_rod ~ ~1 ~ 0.3 0.6 0.3 0.05 20',
                          'playsound minecraft:entity.illusioner.mirror_move player @a[distance=..16] ~ ~ ~ 1 1.4'])
    fn('p202/cres/blink', ['scoreboard players add #cs bm.rng 1', 'execute if score #cs bm.rng matches 7.. run return 0',
                           'execute positioned ^ ^ ^1 unless block ~ ~ ~ #bm:p202_pass run return 0',
                           'execute positioned ^ ^ ^1 unless block ~ ~1 ~ #bm:p202_pass run return 0', 'tp @s ^ ^ ^1',
                           'execute at @s run function bm:p202/cres/blink'])
    fn('p202/cres/slam', ['execute if score @s bm.crcd2 matches 1.. run return run ' + say('The Crescent is still gathering its bloom...', '#ff7ae0'),
                          'scoreboard players set @s bm.crcd2 240', 'tag @s add bm.crme',
                          f'execute as @e[{foe},distance=..5] at @s run function bm:p202/cres/slammed',
                          'effect give @a[distance=..8,gamemode=!spectator] minecraft:regeneration 6 1', 'effect give @a[distance=..8,gamemode=!spectator] minecraft:absorption 10 1',
                          'execute as @e[type=#bm:p42_ally,distance=..8] run effect give @s minecraft:regeneration 6 1',
                          'tag @s remove bm.crme'] +
       [f'particle minecraft:cherry_leaves ^{4 * math.sin(math.radians(a)):.2f} ^0.3 ^{4 * math.cos(math.radians(a)):.2f} 0.3 0.3 0.3 0 4'
        for a in range(0, 360, 24)] +
       ['particle minecraft:flash{color:[1.0,0.8,1.0,1.0]} ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:end_rod ~ ~0.5 ~ 2.5 0.3 2.5 0.1 60',
        'playsound minecraft:entity.generic.explode player @a[distance=..24] ~ ~ ~ 0.6 1.4', 'playsound minecraft:block.spore_blossom.place player @a[distance=..24] ~ ~ ~ 1 0.7'])
    fn('p202/cres/slammed', ['damage @s 16 minecraft:magic by @p[tag=bm.crme]', 'effect give @s minecraft:levitation 1 6 true',
                             'particle minecraft:cherry_leaves ~ ~1 ~ 0.3 0.5 0.3 0 8'])

    # ---------------------------------------------------------------- the sets: whole-set bonuses, Tidewall and Pearl's Grace
    for s in SETS:
        whole = ' '.join(f'if items entity @s armor.{sl} *[minecraft:custom_data~{{bm_set:"{s}"}}]' for sl in ('head', 'chest', 'legs', 'feet'))
        second.append(f'execute as @a {whole} at @s run function bm:p202/set/{s}')
        fn(f'p202/set/has_{s}', [f'return run execute {whole}'])
    fn('p202/set/tidewarden', ['effect give @s minecraft:resistance 2 0 true',
                               'execute if block ~ ~1 ~ minecraft:water run effect give @s minecraft:water_breathing 12 0 true',
                               'execute if block ~ ~1 ~ minecraft:water run effect give @s minecraft:dolphins_grace 2 0 true',
                               'execute if block ~ ~1 ~ minecraft:water run effect give @s minecraft:conduit_power 12 0 true'])
    fn('p202/set/pearlguard', ['effect give @s minecraft:strength 2 0 true', 'effect give @s minecraft:jump_boost 2 0 true',
                               'execute if block ~ ~ ~ minecraft:water run effect give @s minecraft:regeneration 2 0 true'])
    wjson('bm/advancement/p202/hurt.json', {'criteria': {'hurt': {'trigger': 'minecraft:entity_hurt_player'}}, 'rewards': {'function': 'bm:p202/hurt'}})
    fn('p202/hurt', ['advancement revoke @s only bm:p202/hurt', 'execute store result score #hp bm.rng run data get entity @s Health',
                     'execute if score #hp bm.rng matches 9.. run return 0',
                     'execute if function bm:p202/set/has_tidewarden unless score @s bm.twcd matches 1.. at @s run return run function bm:p202/set/tidewall',
                     'execute if function bm:p202/set/has_pearlguard unless score @s bm.pgcd matches 1.. at @s run return run function bm:p202/set/grace'])
    fn('p202/set/tidewall', ['scoreboard players set @s bm.twcd 1800', 'effect give @s minecraft:absorption 10 2 true', 'tag @s add bm.twme',
                             f'execute as @e[{foe},distance=..6] at @s facing entity @p[tag=bm.twme] feet rotated ~180 0 run tp @s ^ ^0.5 ^3',
                             f'execute as @e[{foe},distance=..8] run effect give @s minecraft:slowness 4 1', 'tag @s remove bm.twme',
                             'particle minecraft:splash ~ ~1 ~ 2 1 2 0.3 160', 'particle minecraft:bubble_column_up ~ ~0.5 ~ 2 0.5 2 0.1 80',
                             'playsound minecraft:entity.generic.splash player @a[distance=..20] ~ ~ ~ 1 0.6', say('TIDEWALL!', '#86a6c4')])
    fn('p202/set/grace', ['scoreboard players set @s bm.pgcd 1800', 'effect give @s minecraft:invisibility 5 0 true', 'effect give @s minecraft:speed 5 2 true',
                          'effect give @s minecraft:regeneration 6 1 true', 'particle minecraft:end_rod ~ ~1 ~ 0.6 0.8 0.6 0.1 60',
                          'particle minecraft:dust{color:[1.0,0.95,1.0],scale:1.6} ~ ~1 ~ 0.6 0.8 0.6 0 40',
                          'playsound minecraft:block.amethyst_block.resonate player @a[distance=..20] ~ ~ ~ 1 1.5', say("PEARL'S GRACE!", '#ff7ae0')])

    # ---------------------------------------------------------------- Leo's Trident and Emma's Bloomheart, stronger
    G.FUNCS['p59/leo/tide'] = ['effect give @s minecraft:strength 2 1 true', 'effect give @s minecraft:resistance 2 0 true',
                               'effect give @s minecraft:dolphins_grace 2 0 true', 'effect give @s minecraft:conduit_power 12 0 true',
                               'particle minecraft:bubble_pop ~ ~1 ~ 0.4 0.6 0.4 0.02 4']
    bh = G.FUNCS['p45/bloomheart_gem/use']
    bh[:] = [l.replace('bm.mcd4 900', 'bm.mcd4 600').replace('regeneration 8 1', 'regeneration 10 2') for l in bh]
    bh += ['effect give @a[distance=..8,gamemode=!spectator] minecraft:absorption 10 1']
    G.FUNCS['p59/bloom/boosted'] = [l.replace('regeneration 12 1', 'regeneration 12 2') for l in G.FUNCS['p59/bloom/boosted']]

    # ---------------------------------------------------------------- at the Font: Leo gives his Aegis; Emma her Crescent
    lpet = '@e[type=minecraft:wolf,tag=bm.leopet,distance=..24]'
    G.FUNCS['p199/font/ask'][1:1] = [      # (before 'nobody royal here': Leo alone is enough)
        'scoreboard players set #r_leo bm.rng 0', f'execute as {lpet} if score @s bm.pid = #me bm.pid run scoreboard players set #r_leo bm.rng 1',
        'execute if score #r_leo bm.rng matches 1 unless entity @s[tag=bm.kg_aegis] run function bm:p202/give/aegis',
        f'execute if score #r_leo bm.rng matches 1 if entity @s[tag=bm.kg_aegis] if predicate bm:p20/sneaking unless items entity @s container.* {holds("leo_aegis")} unless items entity @s weapon.offhand {holds("leo_aegis")} run function bm:p202/again/aegis']
    G.FUNCS['p199/font/ask'] += [         # (Emma's, last: after the full court has restored the castle, in the same visit)
        'execute if score #r_emma bm.rng matches 1 unless entity @s[tag=bm.kg_cres] run function bm:p202/give/cres',
        f'execute if score #r_emma bm.rng matches 1 if entity @s[tag=bm.kg_cres] if predicate bm:p20/sneaking unless items entity @s container.* {holds("emma_crescent")} run function bm:p202/again/cres']
    line = lambda who, col, txt: tellraw('@a[distance=..24]', [T(who + ': ', col, bold=True), T(txt, 'white')])
    core = '@e[type=minecraft:marker,tag=bm.kingdom,distance=..70,sort=nearest,limit=1]'
    fn('p202/give/aegis', ['execute unless score @s bm.krank matches 2.. run return run ' +
                           tellraw('@s', [T('Leo: ', '#5ab8e0', bold=True), T('"My shield hangs in this hall, waiting for a knight of the Tide. Earn that, and it\'s yours."', 'white'),
                                          T(' (Knight of the Tide: 12 favour)', 'dark_gray')]),
                           'tag @s add bm.kg_aegis', give('leo_aegis'),
                           line('Leo', '#5ab8e0', 'I carried Emma out of here behind this shield, the night the palace fell.'),
                           line('Leo', '#5ab8e0', 'You stand where I stood now. Take it - and hold the line for her.'),
                           'playsound minecraft:item.shield.block player @a[distance=..24] ~ ~ ~ 1 0.6', 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1',
                           tellraw('@s', [T('  + ', 'gray'), T("Leo's Aegis", '#86a6c4', bold=True)])])
    fn('p202/give/cres', ['scoreboard players set #kr bm.rng 0', f'execute as {core} if score @s bm.kgst matches 1 run scoreboard players set #kr bm.rng 1',
                          'execute unless score #kr bm.rng matches 1 run return 0',
                          'execute unless score @s bm.krank matches 3.. run return run ' +
                          tellraw('@s', [T('Emma: ', '#ff8ad8', bold=True), T('"There\'s something of mine I want you to have... when you\'re the kingdom\'s champion. Soon!"', 'white'),
                                         T(' (Royal Champion: 25 favour)', 'dark_gray')]),
                          'tag @s add bm.kg_cres', give('emma_crescent'),
                          line('Emma', '#ff8ad8', 'My crescent! I hid it in the throne room wall before the war. Nobody ever found it. Not even Pearl.'),
                          line('Emma', '#ff8ad8', "It's... a lot of axe. It suits you. Swing it like you mean it!"),
                          'particle minecraft:cherry_leaves ~ ~2 ~ 1 1 1 0 60', 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1.2',
                          tellraw('@s', [T('  + ', 'gray'), T("Emma's Crescent", '#ff7ae0', bold=True)])])
    for k, iid, nm, col in (('aegis', 'leo_aegis', "Leo's Aegis", '#86a6c4'), ('cres', 'emma_crescent', "Emma's Crescent", '#ff7ae0')):
        fn(f'p202/again/{k}', [f'execute store result score #c bm.rng run clear @s {holds("royal_pearl")} 0',
                               'execute unless score #c bm.rng matches 32.. run return run ' + say(f'The Font can call {nm} back for 32 Royal Pearls.', KC),
                               f'clear @s {holds("royal_pearl")} 32', give(iid), 'particle minecraft:bubble_pop ~ ~1.5 ~ 0.4 0.6 0.4 0.05 30',
                               tellraw('@s', P + [T('The Font ripples, and gives back ', KC), T(nm, col, bold=True), T(' (32 Royal Pearls).', KC)])])

    # ---------------------------------------------------------------- Tide Scales: breaches, raiders, the tribute, the towers
    G.FUNCS['p199/breach/hero'].append(give('tide_scale', 3))
    G.FUNCS['p199/trib/ask'].insert(-2, 'loot give @s loot bm:p202/tribute_scales')
    E = G.loot_entry
    wjson('bm/loot_table/p202/tribute_scales.json', {'type': 'minecraft:command', 'pools': [{'rolls': 1, 'entries': [E('tide_scale', G.uni(1, 2))]}]})
    wjson('bm/loot_table/p202/raider.json', {'type': 'minecraft:entity', 'pools': [{'rolls': 1, 'entries': [E('tide_scale')]},
                                                                                     {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:rotten_flesh'}]}]})
    G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/kingdom_gear', 'yellow'), T("  the kingdom's armoury: the Aegis, the Crescent, both sets, scales", 'gray')]))
    fn('admin/kingdom_gear', [give('leo_aegis'), give('emma_crescent'), give('crown_of_the_deep')] + [give(i) for i in ARMOR_IDS] + [give('tide_scale', 32)])


def rp(R):
    import kingdom_art
    kingdom_art.rp(R, '/home/claude/mc263/client/assets/minecraft/textures')       # (phase180.VAN; importing phase180 here wants its dolls)

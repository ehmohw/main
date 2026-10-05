"""Phase 1.5: specialty armor sets, set-bonus particle displays, Blood Moon, blood mobs, Blood Moon Crystals,
Crimson Revenant (undead minions), Vampire Lord (life drain), legendary elytra.
Importing this module registers the new items; generate(G) writes the logic using gen_dp helpers."""
import items as I
from items import item, gear, attr, ench, T, TOTEM, ITEMS, PRICES, CATEGORY, UPGRADES, consumable, ARMOR_SLOT
from nbt import snbt, B, F, D, L, Int

PIECES = I.PIECES
SLOT = {'helmet': 'armor.head', 'chestplate': 'armor.chest', 'leggings': 'armor.legs', 'boots': 'armor.feet'}
T1_PRICE = [8, 12, 10, 8]
SETS = {}   # set id -> dict(color, particle info, bonus text)


def base_armor(piece, armor, tough=0.0, kb=0.0):
    s = ARMOR_SLOT[piece]
    m = [attr('armor', armor, s, ident=f'minecraft:armor.{piece}'),
         attr('armor_toughness', tough, s, ident=f'minecraft:armor.{piece}_toughness')]
    if kb: m.append(attr('knockback_resistance', kb, s, ident=f'minecraft:armor.{piece}_kb'))
    return m


ARMOR_V = {'helmet': (2, 3, 3), 'chestplate': (5, 7, 8), 'leggings': (4, 5, 6), 'boots': (2, 3, 3)}
ROMAN = {1: 'I', 2: 'II', 3: 'III'}

# ===================================================================== SPECIALTY SETS (3 tiers)
SPECIAL = {
    'shadowstep': dict(title='Shadowstep', names=['Hood', 'Cloak', 'Leggings', 'Treads'], colors=['dark_gray', 'dark_purple', '#7b3fd1'],
                       blurb='Fast as a rumor. Hits like one, too.',
                       bonus='Full set: invisible while sneaking + shadow wisps'),
    'juggernaut': dict(title='Juggernaut', names=['Greathelm', 'Breastplate', 'Tassets', 'Sabatons'], colors=['gray', 'red', '#c0392b'],
                       blurb='Unstoppable. Also unhurried.',
                       bonus='Full set: Resistance + ember ring'),
    'architect': dict(title='Architect', names=['Hard Hat', 'Work Vest', 'Toolbelt', 'Work Boots'], colors=['yellow', 'aqua', '#2e86de'],
                      blurb='Measure twice, place once.',
                      bonus='Full set: Haste + blueprint aura'),
    'tidecaller': dict(title='Tidecaller', names=['Crown', 'Scale Mail', 'Fins', 'Flippers'], colors=['dark_aqua', 'aqua', '#1abc9c'],
                       blurb='The sea remembers you.',
                       bonus='Full set: Conduit Power + Dolphin\'s Grace in water'),
}
for sid, d in SPECIAL.items():
    for i, piece in enumerate(PIECES):
        s = ARMOR_SLOT[piece]
        for tier in (1, 2, 3):
            t = tier - 1
            armor = ARMOR_V[piece][t]
            perks, cons = [], []
            trim = None
            if sid == 'shadowstep':
                base = f'leather_{piece}'
                mods = base_armor(piece, armor - 1 if tier == 1 else armor, [0, 1, 2][t])
                mods += [attr('movement_speed', [0.06, 0.08, 0.10][t], s, 'add_multiplied_base'),
                         attr('attack_damage', -0.5, s)]
                perks.append(f'+{[6, 8, 10][t]}% Speed'); cons.append('-0.5 Attack')
                if piece == 'leggings': mods.append(attr('sneaking_speed', [0.15, 0.2, 0.3][t], s)); perks.append('Faster sneaking')
                if piece == 'boots':
                    mods += [attr('jump_strength', [0.04, 0.06, 0.08][t], s), attr('safe_fall_distance', [2, 3, 4][t], s)]
                    perks.append('Higher jumps')
                en = ench(protection=3 + t, unbreaking=4 + 2 * t)
                if tier > 1: en.update(ench(mending=1))
                extra = {'minecraft:dyed_color': [0x1E1B26, 0x2B1D3F, 0x120E18][t]}
            elif sid == 'juggernaut':
                base = f'iron_{piece}' if tier == 1 else f'netherite_{piece}'
                mods = base_armor(piece, armor + [1, 2, 3][t], [1, 3, 4][t], [0.1, 0.15, 0.2][t])
                mods += [attr('attack_damage', [1, 1.5, 2][t], s), attr('max_health', [1, 2, 3][t], s),
                         attr('movement_speed', -[0.05, 0.04, 0.03][t], s, 'add_multiplied_base')]
                perks.append(f'+{[1, 1.5, 2][t]} Attack, +{[1, 2, 3][t]} Health'); cons.append(f'-{[5, 4, 3][t]}% Speed')
                en = ench(protection=5 + t, unbreaking=4 + 3 * t)
                if tier > 1: en.update(ench(mending=1))
                if tier == 2: trim = {'material': 'minecraft:iron', 'pattern': 'minecraft:ward'}
                if tier == 3: trim = {'material': 'minecraft:gold', 'pattern': 'minecraft:silence'}
                extra = {}
            elif sid == 'architect':
                base = f'golden_{piece}' if tier == 1 else f'diamond_{piece}'
                mods = base_armor(piece, armor, [0, 2, 3][t])
                mods += [attr('block_interaction_range', [0.75, 1.25, 1.75][t], s),
                         attr('block_break_speed', [0.05, 0.08, 0.12][t], s, 'add_multiplied_base')]
                # a builder, not a brawler: weaker swings and shorter melee reach
                mods += [attr('attack_damage', -0.5, s), attr('entity_interaction_range', -0.25, s)]
                perks.append(f'+{[0.75, 1.25, 1.75][t]} Reach, +{[5, 8, 12][t]}% Mining'); cons.append('-0.5 Attack, -0.25 Melee reach')
                if piece == 'boots':
                    mods += [attr('step_height', [0.5, 0.6, 1.0][t], s), attr('safe_fall_distance', [6, 10, 16][t], s)]
                    perks.append('Step up blocks, softer falls')
                en = ench(protection=4 + t, unbreaking=6 + 2 * t)
                if tier > 1: en.update(ench(mending=1))
                if tier == 2: trim = {'material': 'minecraft:lapis', 'pattern': 'minecraft:shaper'}
                if tier == 3: trim = {'material': 'minecraft:gold', 'pattern': 'minecraft:shaper'}
                extra = {}
            else:  # tidecaller
                base = f'chainmail_{piece}' if tier == 1 else f'diamond_{piece}'
                mods = base_armor(piece, armor, [0, 2, 3][t])
                # a fish out of water: slower on land (applied live, see tide_land) and dries out / burns longer
                mods += [attr('water_movement_efficiency', [0.08, 0.12, 0.18][t], s), attr('burning_time', 0.25, s)]
                perks.append('Faster swimming'); cons.append('-5% Speed on land, burns 25% longer')
                if piece == 'helmet':
                    mods += [attr('oxygen_bonus', [1, 2, 3][t], s), attr('submerged_mining_speed', [0.3, 0.6, 1.0][t], s)]
                    perks.append('Longer breath, fast underwater mining')
                en = ench(protection=4 + t, unbreaking=4 + 2 * t)
                if piece == 'helmet': en.update(ench(respiration=3 + t, aqua_affinity=1))
                if piece == 'boots': en.update(ench(depth_strider=3))
                if tier > 1: en.update(ench(mending=1))
                if tier == 2: trim = {'material': 'minecraft:lapis', 'pattern': 'minecraft:tide'}
                if tier == 3: trim = {'material': 'minecraft:quartz', 'pattern': 'minecraft:tide'}
                extra = {}
            if trim: extra['minecraft:trim'] = trim
            iid = f'{sid}_{piece}_{tier}'
            name = f"{d['title']} {d['names'][i]}" + ('' if tier == 1 else f' {ROMAN[tier]}')
            lore = [d['blurb'], (', '.join(perks), 'blue'), (', '.join(cons), 'red'), (d['bonus'], 'dark_aqua')]
            kw = dict(attrs=mods, extra=extra, custom_extra={'bm_set': sid}, bold=tier == 3)
            if tier == 1:
                gear(iid, base, name, d['colors'][t], lore, en, tier, price=('token', T1_PRICE[i]), **kw)
            else:
                gear(iid, base, name, d['colors'][t], lore, en, tier,
                     upgrade_from=(f'{sid}_{piece}_{tier - 1}', 'medallion' if tier == 2 else 'trophy', 4 if tier == 2 else 2), **kw)

# ===================================================================== BLOOD MOON GOODS
item('blood_crystal', TOTEM, 'Blood Moon Crystal', 'dark_red',
     ['Cut from a Blood Moon horror.', 'Still warm. Still humming.', ('Trade with the Bloodbroker.', 'gray')],
     model='bm:blood_crystal', stack=64, cat='currency')
item('bloodforge_sigil', TOTEM, 'Bloodforge Sigil', 'red',
     ['Put a tool, weapon or armor piece', 'in your OFF hand, then use this.', ('Makes it UNBREAKABLE forever.', 'gold'),
      ('Only wakes under a Blood Moon, in the Overworld.', 'red'), ('Blood price: one max heart, forever', 'dark_red'), ('(never below one). Heartstones restore it.', 'dark_red')],
     model='bm:bloodforge_sigil', glint=True, stack=16,
     comps={'minecraft:consumable': consumable(2.0, 'spyglass', 'minecraft:block.smithing_table.use', False)}, cat='blood')
item('blood_almanac', TOTEM, 'Blood Moon Almanac', 'dark_red',
     ['Use to see how many nights remain', 'until the next Blood Moon.', ('Reusable.', 'gray'),
      ('The last page warns of a beast too large', 'dark_gray'), ('for any night but a red one...', 'dark_gray')],
     model='bm:blood_almanac', comps={'minecraft:consumable': consumable(0.6, 'none', 'minecraft:item.book.page_turn', False)}, cat='blood')
item('crimson_effigy', TOTEM, 'Crimson Effigy', 'dark_red',
     ['Use to call a Blood Moon TONIGHT.', ('Every player will know you did it.', 'red')],
     model='bm:crimson_effigy', glint=True, stack=4,
     comps={'minecraft:consumable': consumable(3.0, 'toot_horn', 'minecraft:particle.soul_escape', True)}, cat='blood')
item('sanguine_tonic', TOTEM, 'Sanguine Tonic', 'red',
     ['A thick red drink. Do not ask.', ('Instant Health II, Strength II (1:00),', 'blue'), ('Absorption I (0:30)', 'blue')],
     model='bm:sanguine_tonic', stack=16,
     comps={'minecraft:consumable': consumable(1.2, 'drink', 'minecraft:entity.generic.drink', False, effects=[
         {'type': 'minecraft:apply_effects', 'effects': [
             {'id': 'minecraft:instant_health', 'amplifier': 1, 'duration': 1},
             {'id': 'minecraft:strength', 'amplifier': 1, 'duration': 1200},
             {'id': 'minecraft:absorption', 'amplifier': 0, 'duration': 600}]}])}, cat='blood')

# Crimson Revenant (summons undead) and Vampire Lord (life drain)
CRIMSON_NAMES = ['Skullhelm', 'Ribcage', 'Legbones', 'Gravewalkers']
VAMP_NAMES = ['Cowl', 'Mantle', 'Breeches', 'Boots']
for i, piece in enumerate(PIECES):
    s = ARMOR_SLOT[piece]
    gear(f'crimson_{piece}', f'netherite_{piece}', f'Crimson Revenant {CRIMSON_NAMES[i]}', 'dark_red',
         ['Forged from Blood Moon crystals.', ('+2 Max Health', 'blue'),
          ('Full set: when hurt, 3 undead revenants', 'dark_aqua'), ('rise to fight for you (45s cooldown)', 'dark_aqua')],
         ench(protection=6, unbreaking=6, mending=1), 2,
         attrs=I.armor_attrs('netherite', piece, [attr('max_health', 2, s)]),
         extra={'minecraft:trim': {'material': 'minecraft:redstone', 'pattern': 'minecraft:rib'}},
         custom_extra={'bm_set': 'crimson'}, price=('blood_crystal', [10, 14, 12, 10][i]))
    en = ench(protection=6, unbreaking=6, mending=1)
    if piece == 'chestplate': en['bm:vampiric'] = 1
    gear(f'vampire_{piece}', f'netherite_{piece}', f'Vampire Lord {VAMP_NAMES[i]}', '#8b0000',
         ['Elegant. Hungry. Eternal.', ('+1 Max Health', 'blue'),
          ('Full set: hitting monsters drains their life', 'dark_aqua'), ('Night Vision; Weakness in direct sunlight', 'dark_aqua')],
         en, 2, attrs=I.armor_attrs('netherite', piece, [attr('max_health', 1, s)]),
         extra={'minecraft:trim': {'material': 'minecraft:redstone', 'pattern': 'minecraft:vex'}},
         custom_extra={'bm_set': 'vampire'}, price=('blood_crystal', [12, 16, 14, 12][i]))

# Legendary elytra
item('golden_wings', 'minecraft:elytra', 'Wings of the Golden Rat', '#ffd700',
     ['Woven from smuggled gold thread.', ('Unbreakable. +4 Armor, +2 Toughness.', 'blue'), ('Leaves a golden trail while gliding.', 'dark_aqua')],
     model='bm:golden_wings', bold=True, tier=3,
     comps={'minecraft:unbreakable': {},
            'minecraft:equippable': {'slot': 'chest', 'asset_id': 'bm:golden_wings', 'equip_sound': 'minecraft:item.armor.equip_elytra',
                                     'damage_on_hurt': False},
            'minecraft:enchantments': ench(protection=4),
            'minecraft:attribute_modifiers': [attr('armor', 4, 'chest'), attr('armor_toughness', 2, 'chest')]},
     cat='gear', price=('trophy', 4))

# ===================================================================== SET EFFECTS (particles + bonuses)
# set id -> (bonus commands, orbit particle, extra particle line)
SET_FX = {
    'smuggler': (['effect give @s minecraft:luck 11 0 true'], 'minecraft:wax_off', 'particle minecraft:electric_spark ~ ~0.2 ~ 0.3 0 0.3 0 1'),
    'kingpin': (['effect give @s minecraft:fire_resistance 11 0 true'], 'minecraft:dust{color:[0.62,0.25,0.95],scale:1.1}',
                'particle minecraft:enchant ~ ~1.6 ~ 0.3 0.3 0.3 0.6 2'),
    'hero': (['effect give @s minecraft:regeneration 11 0 true'], 'minecraft:glow', 'particle minecraft:dust{color:[1.0,0.85,0.2],scale:0.9} ~ ~2.3 ~ 0.15 0.05 0.15 0 3'),
    'shadowstep': (['execute if score @s bm.sneak matches 1.. run effect give @s minecraft:invisibility 1 0 true'],
                   'minecraft:smoke', 'execute unless score @s bm.sneak matches 1.. run particle minecraft:large_smoke ~ ~0.1 ~ 0.2 0 0.2 0 1'),
    'juggernaut': (['effect give @s minecraft:resistance 11 0 true'], 'minecraft:crit', 'particle minecraft:dust{color:[0.75,0.1,0.05],scale:1.3} ~ ~0.2 ~ 0.4 0 0.4 0 3'),
    'architect': (['effect give @s minecraft:haste 11 0 true'], 'minecraft:dust{color:[0.2,0.55,1.0],scale:1.0}',
                  'particle minecraft:end_rod ~ ~2.2 ~ 0.2 0.05 0.2 0 1'),
    'tidecaller': (['execute if block ~ ~1 ~ minecraft:water run effect give @s minecraft:conduit_power 11 0 true',
                    'execute if block ~ ~1 ~ minecraft:water run effect give @s minecraft:dolphins_grace 2 0 true'],
                   'minecraft:bubble_pop', 'particle minecraft:nautilus ~ ~1.8 ~ 0.4 0.3 0.4 0.5 2'),
    'crimson': ([], 'minecraft:dust{color:[0.55,0.0,0.0],scale:1.4}', 'particle minecraft:soul ~ ~0.3 ~ 0.3 0.1 0.3 0.01 1'),
    'vampire': (['effect give @s minecraft:night_vision 15 0 true',
                 'execute if score #tod bm.bm matches 0..12000 positioned ~ ~1.6 ~ if predicate bm:sees_sky run effect give @s minecraft:weakness 2 0 true'],
                'minecraft:dust{color:[0.45,0.0,0.05],scale:0.8}', 'particle minecraft:falling_dust{block_state:"minecraft:redstone_block"} ~ ~1.2 ~ 0.3 0.4 0.3 0 1'),
}


# ===================================================================== GENERATION
def generate(G):
    fn, wjson, give, offer, T_, title, tellraw, loot_entry, uni, KILLED, chance = (
        G.fn, G.wjson, G.give, G.offer, G.T, G.title, G.tellraw, G.loot_entry, G.uni, G.KILLED, G.chance)
    PREFIX = G.PREFIX

    # ---------------- set detection + effects
    fast = []
    fast += ['scoreboard players add #ang bm.fx 30', 'scoreboard players operation #ang bm.fx %= #360 bm.fx',
             'execute store result storage bm:fx a int 1 run scoreboard players get #ang bm.fx',
             'scoreboard players operation #angb bm.fx = #ang bm.fx', 'scoreboard players add #angb bm.fx 180',
             'execute store result storage bm:fx b int 1 run scoreboard players get #angb bm.fx']
    for sid, (bonus, orbit, extra) in SET_FX.items():
        fn(f'sets/has/{sid}', ['return run execute ' + ' '.join(
            f'if items entity @s {SLOT[p]} *[minecraft:custom_data~{{bm_set:"{sid}"}}]' for p in PIECES)])
        fn(f'sets/{sid}', bonus + [extra, f'function bm:fx/{sid} with storage bm:fx'])
        fn(f'fx/{sid}', [f'$execute rotated $(a) 0 positioned ^ ^1.1 ^0.85 run particle {orbit} ~ ~ ~ 0 0 0 0 1',
                         f'$execute rotated $(b) 0 positioned ^ ^1.1 ^0.85 run particle {orbit} ~ ~ ~ 0 0 0 0 1',
                         f'$execute rotated $(a) 0 positioned ^ ^0.4 ^-0.7 run particle {orbit} ~ ~ ~ 0 0 0 0 1'])
        fast.append(f'execute as @a[gamemode=!spectator] if function bm:sets/has/{sid} at @s run function bm:sets/{sid}')
    # Tidecaller: slower on land, per piece worn (removed the moment you're in water)
    fast += ['scoreboard players set @a bm.tide 0'] + [
        f'execute as @a if items entity @s {SLOT[p]} *[minecraft:custom_data~{{bm_set:"tidecaller"}}] run scoreboard players add @s bm.tide 1' for p in PIECES] + [
        'execute as @a[tag=bm.tidepen] run attribute @s minecraft:movement_speed modifier remove bm:tide_land',
        'tag @a remove bm.tidepen',
        'execute as @a[scores={bm.tide=1..}] at @s unless block ~ ~ ~ minecraft:water unless block ~ ~1 ~ minecraft:water run tag @s add bm.tidepen'] + [
        f'execute as @a[tag=bm.tidepen,scores={{bm.tide={n}}}] run attribute @s minecraft:movement_speed modifier add bm:tide_land -{0.05 * n:.2f} add_multiplied_base' for n in range(1, 5)]
    # elytra trail
    fast.append('execute as @a[gamemode=!spectator] if items entity @s armor.chest *[minecraft:custom_data~{bm:"golden_wings"}] if predicate bm:gliding at @s run function bm:sets/wings_trail')
    fn('sets/wings_trail', ['particle minecraft:wax_on ~ ~0.5 ~ 0.4 0.2 0.4 0 4', 'particle minecraft:end_rod ~ ~0.5 ~ 0.2 0.1 0.2 0.01 1'])
    wjson('bm/predicate/gliding.json', {'condition': 'minecraft:entity_properties', 'entity': 'this',
                                        'predicate': {'minecraft:flags': {'is_fall_flying': True}}})
    wjson('bm/predicate/sees_sky.json', {'condition': 'minecraft:location_check', 'predicate': {'can_see_sky': True}})

    # ---------------- Crimson Revenant minions
    fast += ['execute as @a[scores={bm.dmg=1..},gamemode=!spectator] unless score @s bm.ccd matches 1.. if function bm:sets/has/crimson at @s run function bm:sets/crimson_summon',
             'scoreboard players reset @a bm.dmg',
             'execute as @a[team=bm.necro] unless function bm:sets/has/crimson run team leave @s']
    minion = lambda t, w: {'Tags': ['bm.seen', 'bm.revenant', 'bm.new_rev'], 'DeathLootTable': 'bm:entities/empty',
                           'CustomName': T('Crimson Revenant', 'dark_red'), 'PersistenceRequired': B(0), 'Health': F(30),
                           'attributes': [{'id': 'minecraft:max_health', 'base': D(30)}, {'id': 'minecraft:attack_damage', 'base': D(6)},
                                          {'id': 'minecraft:follow_range', 'base': D(24)}],
                           'active_effects': [{'id': 'minecraft:fire_resistance', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0)}],
                           'equipment': {'head': {'id': 'minecraft:netherite_helmet', 'count': Int(1), 'components': {
                               'minecraft:trim': {'material': 'minecraft:redstone', 'pattern': 'minecraft:rib'}}},
                                         'mainhand': {'id': w, 'count': Int(1)}},
                           'drop_chances': {k: F(0.0) for k in ['head', 'chest', 'legs', 'feet', 'mainhand', 'offhand']}}
    fn('sets/crimson_summon', [
        'scoreboard players set @s bm.ccd 45',
        'execute if entity @s[team=] run team join bm.necro @s',
        f'summon minecraft:zombie ^1.5 ^ ^ {snbt(minion("zombie", "minecraft:iron_sword"))}',
        f'summon minecraft:zombie ^-1.5 ^ ^ {snbt(minion("zombie", "minecraft:iron_axe"))}',
        f'summon minecraft:skeleton ^ ^ ^-1.5 {snbt(minion("skeleton", "minecraft:bow"))}',
        'team join bm.necro @e[tag=bm.new_rev,distance=..4]',
        'scoreboard players set @e[tag=bm.new_rev,distance=..4] bm.life 30',
        'tag @e[tag=bm.new_rev,distance=..4] remove bm.new_rev',
        'particle minecraft:soul ~ ~0.5 ~ 1.2 0.3 1.2 0.02 30',
        'playsound minecraft:entity.evoker.prepare_summon player @a[distance=..16] ~ ~ ~ 1 0.7',
        title('@s', 'actionbar', T('Three Crimson Revenants rise to defend you!', 'dark_red'))])
    wjson('bm/loot_table/entities/empty.json', {'type': 'minecraft:entity', 'pools': []})
    second = ['scoreboard players remove @a[scores={bm.ccd=1..}] bm.ccd 1',
              'scoreboard players remove @a[scores={bm.vcd=1..}] bm.vcd 1',
              'scoreboard players remove @e[tag=bm.revenant] bm.life 1',
              'execute as @e[tag=bm.revenant,scores={bm.life=..0}] at @s run function bm:sets/revenant_fade',
              'execute as @e[tag=bm.revenant] at @s if entity @e[type=#bm:hostile,tag=!bm.revenant,tag=!bm.wil_body,distance=..14] run damage @s 0.01 minecraft:mob_attack by @e[type=#bm:hostile,tag=!bm.revenant,tag=!bm.wil_body,distance=..14,sort=nearest,limit=1]']
    fn('sets/revenant_fade', ['particle minecraft:soul ~ ~1 ~ 0.3 0.6 0.3 0.02 12', 'tp @s ~ -400 ~'])

    # ---------------- Vampire Lord drain (custom enchantment runs this)
    fn('sets/vampire_drain', [
        'execute unless entity @s[type=minecraft:player] run return 0',
        'execute unless function bm:sets/has/vampire run return 0',
        'execute if score @s bm.vcd matches 1.. run return 0',
        'scoreboard players set @s bm.vcd 2',
        'effect give @s minecraft:instant_health 1 0 true',
        'particle minecraft:dust{color:[0.6,0.0,0.05],scale:1.2} ~ ~1 ~ 0.4 0.6 0.4 0 14',
        'playsound minecraft:entity.generic.drink player @a[distance=..12] ~ ~ ~ 0.6 0.6'])
    wjson('bm/enchantment/vampiric.json', {
        'anvil_cost': 8, 'description': T('Vampiric', 'dark_red'), 'max_level': 1, 'weight': 1,
        'min_cost': {'base': 1, 'per_level_above_first': 0}, 'max_cost': {'base': 1, 'per_level_above_first': 0},
        'slots': ['chest'], 'supported_items': '#minecraft:enchantable/chest_armor',
        'effects': {'minecraft:post_attack': [{
            'affected': 'attacker', 'enchanted': 'attacker',
            'effect': {'type': 'minecraft:run_function', 'function': 'bm:sets/vampire_drain'},
            'requirements': {'condition': 'minecraft:entity_properties', 'entity': 'this',
                             'predicate': {'minecraft:entity_type': '#bm:hostile'}}}]}})
    # Blood Curse: on blood moon mob weapons. True damage that ignores armor & enchantments + Wither.
    wjson('bm/enchantment/blood_curse.json', {
        'anvil_cost': 8, 'description': T('Blood Curse', 'dark_red'), 'max_level': 1, 'weight': 1,
        'min_cost': {'base': 1, 'per_level_above_first': 0}, 'max_cost': {'base': 1, 'per_level_above_first': 0},
        'slots': ['mainhand'], 'supported_items': '#minecraft:enchantable/weapon',
        'effects': {'minecraft:post_attack': [{
            'affected': 'victim', 'enchanted': 'attacker',
            'effect': {'type': 'minecraft:all_of', 'effects': [
                {'type': 'minecraft:damage_entity', 'damage_type': 'bm:blood_drain', 'min_damage': 3.0, 'max_damage': 3.0},
                {'type': 'minecraft:apply_mob_effect', 'to_apply': 'minecraft:wither', 'min_duration': 4.0, 'max_duration': 4.0,
                 'min_amplifier': 0.0, 'max_amplifier': 0.0}]},
            'requirements': {'condition': 'minecraft:entity_properties', 'entity': 'this',
                             'predicate': {'minecraft:entity_type': 'minecraft:player'}}}]}})
    wjson('bm/damage_type/blood_drain.json', {'exhaustion': 0.1, 'message_id': 'bm.blood_drain', 'scaling': 'never'})
    for tg in ('bypasses_armor', 'bypasses_enchantments'):
        wjson(f'minecraft/tags/damage_type/{tg}.json', {'replace': False, 'values': ['bm:blood_drain']})

    # ---------------- Blood Moon clock
    fn('bloodmoon/tick', [
        'execute store result score #t bm.bm run time of minecraft:overworld query time',
        'scoreboard players operation #day bm.bm = #t bm.bm', 'scoreboard players operation #day bm.bm /= #24000 bm.bm',
        'scoreboard players operation #tod bm.bm = #t bm.bm', 'scoreboard players operation #tod bm.bm %= #24000 bm.bm',
        'scoreboard players operation #cyc bm.bm = #day bm.bm', 'scoreboard players operation #cyc bm.bm %= #30 bm.bm',
        'scoreboard players set #bday bm.bm 0',
        'execute if score #cyc bm.bm matches 29 run scoreboard players set #bday bm.bm 1',
        'execute if score #forced bm.bm matches 1 run scoreboard players set #bday bm.bm 1',
        'scoreboard players set #want bm.bm 0',
        'execute if score #bday bm.bm matches 1 if score #tod bm.bm matches 13000..22999 run scoreboard players set #want bm.bm 1',
        'execute if score #want bm.bm matches 1 unless score #active bm.bm matches 1 run function bm:bloodmoon/start',
        'execute if score #want bm.bm matches 0 if score #active bm.bm matches 1 run function bm:bloodmoon/end',
        'execute if score #active bm.bm matches 1 run function bm:bloodmoon/during',
        'execute if score #bday bm.bm matches 1 if score #tod bm.bm matches 11000..11019 run function bm:bloodmoon/warn',
        'execute if score #bday bm.bm matches 1 if score #tod bm.bm matches 12000.. as @a if data entity @s sleeping_pos at @s run function bm:bloodmoon/wake'])
    fn('bloodmoon/warn', [
        tellraw('@a', PREFIX + [T('The sky is turning red... a ', 'red'), T('Blood Moon', 'dark_red', bold=True), T(' rises at dusk.', 'red')]),
        'execute as @a at @s run playsound minecraft:ambient.cave ambient @s ~ ~ ~ 1 0.5'])
    fn('bloodmoon/start', [
        'scoreboard players set #active bm.bm 1',
        'title @a times 20 100 30',
        title('@a', 'subtitle', T('Monsters grow stronger. You cannot sleep.', 'red', italic=True)),
        title('@a', 'title', T('The Blood Moon Rises', 'dark_red', bold=True)),
        'execute as @a at @s run playsound minecraft:event.raid.horn ambient @s ~ ~ ~ 1 0.6',
        'scoreboard players set #bmint bm.bm 5',
        'bossbar set bm:bloodmoon players @a', 'bossbar set bm:bloodmoon visible true',
        tellraw('@a', PREFIX + [T('A Blood Moon has risen! Elite and Champion monsters are everywhere, Blood Moon horrors walk the night, and the Nether bleeds through.', 'red')])])
    fn('bloodmoon/during', [
        'scoreboard players remove #bmint bm.bm 1',
        'execute if score #bmint bm.bm matches 3 as @a at @s run playsound minecraft:entity.wither.spawn ambient @s ~ ~ ~ 0.4 0.5',
        'scoreboard players operation #prog bm.bm = #tod bm.bm', 'scoreboard players remove #prog bm.bm 13000',
        'execute store result bossbar bm:bloodmoon value run scoreboard players get #prog bm.bm',
        'bossbar set bm:bloodmoon players @a',
        'execute as @a[gamemode=!spectator] at @s if dimension minecraft:overworld if predicate bm:sees_sky run particle minecraft:dust{color:[0.55,0.0,0.0],scale:2.5} ~ ~10 ~ 14 4 14 0 30 normal @s',
        'execute store result score #r bm.rng run random value 1..20',
        'execute if score #r bm.rng matches 1 if score #bmint bm.bm matches ..0 as @a at @s if dimension minecraft:overworld run playsound minecraft:entity.warden.heartbeat ambient @s ~ ~ ~ 0.5 0.6'])
    fn('bloodmoon/end', [
        'scoreboard players set #active bm.bm 0', 'scoreboard players set #forced bm.bm 0',
        'bossbar set bm:bloodmoon visible false',
        'title @a times 20 60 30', title('@a', 'subtitle', T('', 'white')),
        title('@a', 'title', T('The Blood Moon Sets', 'gold', italic=True)),
        'execute as @a at @s run playsound minecraft:block.beacon.deactivate ambient @s ~ ~ ~ 1 0.6',
        tellraw('@a', PREFIX + [T('Dawn breaks. The Blood Moon has passed... for now.', 'gold')])])
    fn('bloodmoon/wake', ['tp @s ~ ~0.6 ~', title('@s', 'actionbar', T("You can't sleep during a Blood Moon!", 'red'))])

    # ---------------- Blood Moon mobs
    for t in list(G.ARMORED) + list(G.UNARMORED):
        fn(f'mobs/blood_roll/{t}', [
            'execute store result score #r bm.rng run random value 1..1000',
            f'execute if score #r bm.rng matches 1..6 run return run function bm:mobs/lucky/{t}',
            f'execute if score #r bm.rng matches 7..86 run return run function bm:mobs/blood/{t}',       # 8% horrors (v1.9: was 3%)
            f'execute if score #r bm.rng matches 87..286 run return run function bm:mobs/champion/{t}',  # 20% champions (was 5%)
            f'execute if score #r bm.rng matches 287..636 run return run function bm:mobs/elite/{t}'])   # 35% elites (was 15%)
        hp = G.ARMORED[t][0] if t in G.ARMORED else G.UNARMORED[t]
        mhp = hp * 5
        lines = [f'data merge entity @s {snbt(dict(G.NO_DROPS, Glowing=B(1), PersistenceRequired=B(0), DeathLootTable=f"bm:entities/blood/{t}", CustomName=G.mob_name("Blood Moon ", "dark_red", t, True)))}',
                 'tag @s add bm.blood', 'tag @s add bm.tiered', 'team join bm.blood @s']
        curse = '"bm:blood_curse":1'
        if t in G.ARMORED:
            for slot, piece in [('head', 'helmet'), ('chest', 'chestplate'), ('legs', 'leggings'), ('feet', 'boots')]:
                lines.append(f'item replace entity @s armor.{slot} with minecraft:netherite_{piece}[enchantments={{"minecraft:protection":4,"minecraft:unbreaking":3}},trim={{material:"minecraft:redstone",pattern:"minecraft:rib"}}]')
            w = G.WEAPON['champion'][G.ARMORED[t][1]]
            w = w.replace('enchantments={', 'enchantments={' + curse + ',')
            lines.append(f'item replace entity @s weapon.mainhand with {w}')
        else:
            lines.append(f'item replace entity @s weapon.mainhand with minecraft:netherite_sword[enchantments={{{curse}}}]')
        for e, a in [('strength', 1), ('resistance', 0), ('speed', 0), ('fire_resistance', 0)]:
            lines.append(f'effect give @s minecraft:{e} infinite {a} true')
        if t == 'creeper':
            lines.append('data merge entity @s {powered:1b,ExplosionRadius:3b}')
        lines += [f'attribute @s minecraft:max_health base set {mhp}', f'data modify entity @s Health set value {mhp}.0f',
                  'attribute @s minecraft:follow_range base set 96', 'attribute @s minecraft:knockback_resistance base set 0.8',
                  'attribute @s minecraft:scale base set 1.2',
                  'attribute @s minecraft:movement_speed modifier add bm:blood 0.2 add_multiplied_base',
                  'particle minecraft:dust{color:[0.6,0.0,0.0],scale:2.0} ~ ~1 ~ 0.5 1 0.5 0 20']
        fn(f'mobs/blood/{t}', lines)
        wjson(f'bm/loot_table/entities/blood/{t}.json', {'type': 'minecraft:entity', 'pools': [
            {'rolls': 1, 'entries': [{'type': 'minecraft:loot_table', 'value': f'minecraft:entities/{t}'}]},
            {'rolls': 1, 'entries': [loot_entry('blood_crystal', uni(1, 2))]},
            {'rolls': 1, 'entries': [loot_entry('token', uni(2, 4))], 'conditions': [KILLED]},
            {'rolls': 1, 'entries': [loot_entry('medallion')], 'conditions': [KILLED, chance(0.15)]}]})
    second.append('execute as @e[tag=bm.blood] at @s run particle minecraft:dust{color:[0.6,0.0,0.0],scale:1.5} ~ ~1.2 ~ 0.3 0.6 0.3 0 3')

    # ---------------- crystal items logic
    G.consume_adv('bloodforge_sigil', 'bm:blood/sigil')
    wjson('bm/item_modifier/unbreakable.json', {'function': 'minecraft:set_components', 'components': {'minecraft:unbreakable': {}}})
    fn('blood/sigil_fail', [give('bloodforge_sigil'), title('@s', 'actionbar', T('Hold a tool, weapon or armor piece in your OFF hand! (Refunded)', 'red'))])
    fn('blood/sigil_dup', [give('bloodforge_sigil'), title('@s', 'actionbar', T('That item is already unbreakable. (Refunded)', 'gray'))])
    fn('blood/sigil', ['advancement revoke @s only bm:consume/bloodforge_sigil',
                       'execute unless items entity @s weapon.offhand *[minecraft:max_damage] run return run function bm:blood/sigil_fail',
                       'execute if items entity @s weapon.offhand *[minecraft:unbreakable] run return run function bm:blood/sigil_dup',
                       'item modify entity @s weapon.offhand bm:unbreakable',
                       'playsound minecraft:block.anvil.use player @s ~ ~ ~ 1 0.6',
                       'scoreboard players set @s bm.sig 8',
                       'particle minecraft:dust{color:[0.7,0.0,0.0],scale:1.5} ~ ~1 ~ 0.5 0.6 0.5 0 40',
                       title('@s', 'actionbar', T('Bloodforged! Your item will never break.', 'red'))])
    fn('blood/sigil_infuse', ['scoreboard players reset @s bm.sig', 'playsound minecraft:block.respawn_anchor.charge player @s ~ ~ ~ 1 0.8'])
    G.consume_adv('blood_almanac', 'bm:blood/almanac')
    fn('blood/almanac', ['advancement revoke @s only bm:consume/blood_almanac', give('blood_almanac'),
                         'execute if score #active bm.bm matches 1 run return run ' + tellraw('@s', PREFIX + [T('The Blood Moon is risen RIGHT NOW.', 'dark_red', bold=True)]),
                         'execute if score #forced bm.bm matches 1 run return run ' + tellraw('@s', PREFIX + [T('An effigy has called the Blood Moon. It rises TONIGHT.', 'red')]),
                         'scoreboard players set #left bm.bm 29', 'scoreboard players operation #left bm.bm -= #cyc bm.bm',
                         'execute if score #left bm.bm matches 0 run return run ' + tellraw('@s', PREFIX + [T('The Blood Moon rises TONIGHT.', 'red', bold=True)]),
                         tellraw('@s', PREFIX + [T('The next Blood Moon rises in ', 'gray'), {'score': {'name': '#left', 'objective': 'bm.bm'}, 'color': 'red', 'bold': True}, T(' days.', 'gray')])])
    G.consume_adv('crimson_effigy', 'bm:blood/effigy')
    fn('blood/effigy', ['advancement revoke @s only bm:consume/crimson_effigy',
                        'execute if score #active bm.bm matches 1 run return run ' + give('crimson_effigy'),
                        'scoreboard players set #forced bm.bm 1',
                        tellraw('@a', PREFIX + [{'selector': '@s', 'color': 'red'}, T(' has raised a Crimson Effigy. ', 'gray'), T('The Blood Moon will rise tonight!', 'dark_red', bold=True)]),
                        'execute as @a at @s run playsound minecraft:entity.wither.ambient ambient @s ~ ~ ~ 0.6 0.5'])

    # ---------------- blood moon objectives / teams / bossbar
    G.FUNCS['load'][-1:-1] = [
        'scoreboard objectives add bm.bm dummy', 'scoreboard objectives add bm.fx dummy',
        'scoreboard objectives add bm.dmg minecraft.custom:minecraft.damage_taken',
        'scoreboard objectives add bm.ccd dummy', 'scoreboard objectives add bm.vcd dummy', 'scoreboard objectives add bm.life dummy',
        'scoreboard objectives add bm.tide dummy',
        'scoreboard players set #24000 bm.bm 24000', 'scoreboard players set #30 bm.bm 30', 'scoreboard players set #360 bm.fx 360',
        'team add bm.blood', 'team modify bm.blood color red',
        'team add bm.necro', 'team modify bm.necro color dark_red', 'team modify bm.necro friendlyFire false',
        'bossbar add bm:bloodmoon {text:"Blood Moon",color:"dark_red",bold:true}',
        'bossbar set bm:bloodmoon color red', 'bossbar set bm:bloodmoon style notched_10', 'bossbar set bm:bloodmoon max 10000']
    G.OBJECTIVES += ['bm.bm', 'bm.fx', 'bm.dmg', 'bm.ccd', 'bm.vcd', 'bm.life', 'bm.tide']
    # insert into loops (before reset of sneak score so shadowstep can read it)
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[0:0] = ['function bm:bloodmoon/tick']
    s[-1:-1] = second


# ===================================================================== TRADES
def extend_offers(O, offer):
    O['outfitter'].append(offer(('trophy', 4), ('golden_wings', 1)))
    arm = []
    for sid in SPECIAL:
        for p, n in zip(PIECES, T1_PRICE):
            arm.append(offer(('token', n), (f'{sid}_{p}_1', 1)))
    for f, cur, n, to in UPGRADES:
        if to.split('_')[0] in SPECIAL:
            arm.append(offer((f, 1), (to, 1), (cur, n)))
    O['armory'] = arm
    blood = [offer(('blood_crystal', 1), ('token', 3)), offer(('blood_crystal', 8), ('medallion', 1)),
             offer(('blood_crystal', 24), ('trophy', 1)), offer(('blood_crystal', 2), ('sanguine_tonic', 1)),
             offer(('blood_crystal', 2), ('blood_almanac', 1)), offer(('blood_crystal', 16), ('bloodforge_sigil', 1)),
             offer(('blood_crystal', 24), ('crimson_effigy', 1))]
    for p in PIECES:
        blood.append(offer(PRICES[f'crimson_{p}'], (f'crimson_{p}', 1), ('medallion', 3)))
    for p in PIECES:
        blood.append(offer(PRICES[f'vampire_{p}'], (f'vampire_{p}', 1), ('medallion', 4)))
    O['blood'] = blood


NEW_NPCS = {
    'armory': ('rat', 'Sgt. Steelwhisker', 'gray', 'armorer', 'plains', 'bm:rat_soldier'),
    'blood': ('villager', 'The Bloodbroker', 'dark_red', 'cleric', 'snow', None),
}

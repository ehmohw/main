"""Phase 2.35: honest gear - the Xenite Altar rewards vanilla gear, and Relic Essences.

ONLY VANILLA GEAR TAKES SOCKETS OR INFUSIONS. Black Market goods (and vanilla gear bought from a trader) are refused at the
altar; anything socketed before keeps its socket. How many sockets an item has depends on what it's made of:
  leather, wood, stone, chainmail: none          copper, iron: 1          gold: 1, and its shards count double
  diamond, trident, mace: 2                      netherite: 2, plus a MASTERWORK socket
  bow, crossbow, shield, elytra, fishing rod, shears, turtle shell, flint and steel, brush...: 1
Right-click the altar with the item in your hand and a shard in your off hand to fill the next socket:
  green +1.5 Attack Damage   violet +3 Safe Fall, +10% Knockback Resistance   cyan +1.5 Luck, +0.5 Reach
  RED (new) Vitality: +2 Max Health. (Sneak + right-click with a red shard cycles a red-socketed item's size: off, grow, shrink.)
PAIRS - two shards in one item add a combo:
  green+green Ferocity (+15% attack speed)          violet+violet Featherweight (-20% gravity, +3 safe fall)
  cyan+cyan Farsight (+1 reach)                     red+red Lifeblood (+4 max health)
  green+violet Juggernaut (+2 toughness, +10% kb)   green+cyan Precision (+1 damage, +0.5 reach)
  green+red Bloodlust (every kill heals 2 hearts)   violet+cyan Wayfarer (+10% speed)
  violet+red Second Wind (below 3 hearts: Regeneration II + Speed; 1 minute recharge)
  cyan+red Fortune's Favour (+2 luck, +2 mining efficiency)
MASTERWORK (netherite, both sockets full): 4 shards + a Medallion. Weapons: Cleave (green), Relentless (violet), Reaver
  (cyan), Vampiric (red). Tools: Haste, Aqua Miner, Deep Reach, Prospector. Armour: Bulwark, Fleet, Ember-proof, Stalwart.
RELIC ESSENCE - scrap a spare relic in the Scrap Bin: 10 Tokens, 2 Medallions and its boss's Essence. Sneak + right-click
  the altar to infuse it (one per item) into NETHERITE gear:
  weapons (sword, axe, spear): Horseman (hits ignite), Pharaoh (+3 damage in daylight), Roc (1 in 10 hits calls a bolt)
  chestplates: Treant (slow regeneration), Colossus (attackers burn), Voidwalker (1 in 10 hits blinks you away)
  RESONANCE - the Essence plus a socket of its colour on the same item awakens an AoE power and an aura:
  Horseman + green: Hellfire (a burst of flame round the target)    Pharaoh + cyan: Sunburst (a blaze of light)
  Roc + violet: Stormcall (bolts leap to two more foes)              Treant + green: Thornmail (attackers are torn and rooted)
  Colossus + red: Magma Aura (burns everything close)               Voidwalker + cyan: Void Shroud (you blink, foes float)"""
from items import item, T, TOTEM
from nbt import snbt, B, F, Int

GEAR = ['sword', 'axe', 'pickaxe', 'shovel', 'hoe', 'spear', 'helmet', 'chestplate', 'leggings', 'boots']
TOOLS = ['sword', 'axe', 'pickaxe', 'shovel', 'hoe', 'spear']
ARMOR = ['helmet', 'chestplate', 'leggings', 'boots']
SOCK1 = ([f'copper_{g}' for g in GEAR] + [f'iron_{g}' for g in GEAR] + [f'golden_{g}' for g in GEAR] +
         ['bow', 'crossbow', 'shield', 'elytra', 'fishing_rod', 'shears', 'turtle_helmet', 'flint_and_steel', 'brush', 'carrot_on_a_stick',
          'warped_fungus_on_a_stick', 'wolf_armor'])
SOCK2 = [f'diamond_{g}' for g in GEAR] + ['trident', 'mace']
SOCK3 = [f'netherite_{g}' for g in GEAR]
ORDER = ['green', 'violet', 'cyan', 'red']
SHORT = {'green': 'g', 'violet': 'v', 'cyan': 'c', 'red': 'r'}
NAME = {'green': ('Green Xenite', '#7dff6a'), 'violet': ('Violet Xenite', '#c27dff'), 'cyan': ('Cyan Xenite', '#6af2ff'), 'red': ('Red Xenite', '#ff4a4a')}
# colour: [(attribute, amount, operation)], lore
SHARD = {'green': ([('attack_damage', 1.5, 'add_value')], '+{0} Attack Damage', [1.5]),
         'violet': ([('safe_fall_distance', 3.0, 'add_value'), ('knockback_resistance', 0.1, 'add_value')], '+{0} Safe Fall, +{1}% Knockback Resistance', [3, 10]),
         'cyan': ([('luck', 1.5, 'add_value'), ('block_interaction_range', 0.5, 'add_value'), ('entity_interaction_range', 0.5, 'add_value')], '+{0} Luck, +{1} Reach', [1.5, 0.5]),
         'red': ([('max_health', 2.0, 'add_value')], 'Vitality: +{0} Max Health', [2])}
COMBOS = {  # key: (name, lore, attributes)
    'gg': ('Ferocity', '+15% Attack Speed', [('attack_speed', 0.15, 'add_multiplied_base')]),
    'vv': ('Featherweight', '-20% Gravity, +3 Safe Fall', [('gravity', -0.2, 'add_multiplied_base'), ('safe_fall_distance', 3.0, 'add_value')]),
    'cc': ('Farsight', '+1 Reach', [('block_interaction_range', 1.0, 'add_value'), ('entity_interaction_range', 1.0, 'add_value')]),
    'rr': ('Lifeblood', '+4 Max Health', [('max_health', 4.0, 'add_value')]),
    'gv': ('Juggernaut', '+2 Armor Toughness, +10% Knockback Resistance', [('armor_toughness', 2.0, 'add_value'), ('knockback_resistance', 0.1, 'add_value')]),
    'gc': ('Precision', '+1 Attack Damage, +0.5 Reach', [('attack_damage', 1.0, 'add_value'), ('entity_interaction_range', 0.5, 'add_value')]),
    'gr': ('Bloodlust', 'every kill heals you 2 hearts', []),
    'vc': ('Wayfarer', '+10% Speed', [('movement_speed', 0.1, 'add_multiplied_base')]),
    'vr': ('Second Wind', 'below 3 hearts: Regeneration II and Speed (1 min recharge)', []),
    'cr': ("Fortune's Favour", '+2 Luck, +2 Mining Efficiency', [('luck', 2.0, 'add_value'), ('mining_efficiency', 2.0, 'add_value')])}
MASTER = {  # category: colour: (name, lore, attributes, enchantment)
    'weapon': {'green': ('Cleave', 'sweeping hits carry +50% damage', [('sweeping_damage_ratio', 0.5, 'add_value')], None),
               'violet': ('Relentless', '+0.4 Attack Speed', [('attack_speed', 0.4, 'add_value')], None),
               'cyan': ('Reaver', '+1 Reach', [('entity_interaction_range', 1.0, 'add_value')], None),
               'red': ('Vampiric', '1 hit in 4 heals you', [], 'mw_vampiric')},
    'tool': {'green': ('Haste', '+30% Mining Speed', [('block_break_speed', 0.3, 'add_multiplied_base')], None),
             'violet': ('Aqua Miner', 'mines underwater at full speed', [('submerged_mining_speed', 0.8, 'add_value')], None),
             'cyan': ('Deep Reach', '+1.5 Block Reach', [('block_interaction_range', 1.5, 'add_value')], None),
             'red': ('Prospector', '+3 Luck', [('luck', 3.0, 'add_value')], None)},
    'armor': {'green': ('Bulwark', '+2 Armor Toughness', [('armor_toughness', 2.0, 'add_value')], None),
              'violet': ('Fleet', '+5% Speed', [('movement_speed', 0.05, 'add_multiplied_base')], None),
              'cyan': ('Ember-proof', 'fire barely takes hold, blasts barely push you',
                       [('burning_time', -0.75, 'add_multiplied_base'), ('explosion_knockback_resistance', 0.5, 'add_value')], None),
              'red': ('Stalwart', '+4 Max Health', [('max_health', 4.0, 'add_value')], None)}}
# boss: (name, colour, target ('weapon'/'chest'), essence lore, resonance colour, resonance name, resonance lore, relic iids)
ESSENCE = {
    'horseman': ("Horseman's Essence", '#ff7a1a', 'weapon', 'hits set the target alight', 'green', 'Hellfire', 'hits may burst into flame round the target',
                 ['horseman_head', 'soul_head', 'venom_head', 'hallowed_head']),
    'pharaoh': ("Pharaoh's Essence", '#e8b923', 'weapon', '+3 damage in daylight', 'cyan', 'Sunburst', 'hits may blaze with sunlight round the target',
                ['pharaoh_crook', 'crook_sands', 'crook_sun', 'crook_ra']),
    'roc': ("Roc's Essence", '#7ab8ff', 'weapon', '1 hit in 10 calls down a thunderbolt', 'violet', 'Stormcall', 'hits may send bolts to two more foes',
            ['storm_talon', 'talon_static', 'talon_chain', 'talon_wind']),
    'treant': ("Treant's Essence", '#6fae3a', 'chest', 'slow, steady regeneration', 'green', 'Thornmail', 'whoever hits you is torn and rooted',
               ['heartwood_branch', 'branch_bark', 'branch_seed', 'branch_bloom']),
    'colossus': ("Colossus's Essence", '#ff6a1a', 'chest', 'whoever hits you burns', 'red', 'Magma Aura', 'everything close to you burns',
                 ['molten_gauntlet', 'gauntlet_obsidian', 'gauntlet_magma', 'gauntlet_hearth']),
    'voidwalker': ("Voidwalker's Essence", '#c27dff', 'chest', '1 hit in 10 blinks you away', 'cyan', 'Void Shroud', 'when hit you blink away and foes float',
                   ['void_scepter', 'scepter_phase', 'scepter_star', 'scepter_rift'])}
for _b, (_n, _c, _t, _l, *_r) in ESSENCE.items():
    item(f'essence_{_b}', TOTEM, _n, _c, ['The distilled power of a roaming boss.', (f'Infuse it into netherite {"weapons" if _t == "weapon" else "chestplates"}', 'blue'),
                                          ('at a Xenite Altar (sneak + right-click):', 'blue'), (_l + '.', 'blue'), ('Comes from scrapping its relic.', 'dark_gray')],
         model=f'bm:essence_{_b}', stack=16, cat='relic', glint=True)

N = lambda v: (str(int(v)) if float(v).is_integer() else str(v))


def generate(G):
    fn, wjson, title, give, tellraw, PREFIX = G.fn, G.wjson, G.title, G.give, G.tellraw, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    second, fast = [], []
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.r55cd dummy']
    G.OBJECTIVES += ['bm.r55cd']
    MH = 'SelectedItem.components."minecraft:custom_data"'       # (a player's held item: equipment.mainhand is only a mob's)
    shard = lambda c: f'*[minecraft:custom_data~{{bm:"xenite_{c}"}}]'
    has = lambda k, v: f'*[minecraft:custom_data~{{{k}:"{v}"}}]'
    tags = {'p55_sock1': SOCK1, 'p55_sock2': SOCK2, 'p55_sock3': SOCK3, 'p55_gilded': [f'golden_{g}' for g in GEAR],
            'p55_mw_weapon': [f'netherite_{g}' for g in ('sword', 'axe', 'spear')], 'p55_mw_tool': [f'netherite_{g}' for g in ('pickaxe', 'shovel', 'hoe')],
            'p55_mw_armor': [f'netherite_{g}' for g in ARMOR]}
    for t, ids in tags.items():
        wjson(f'bm/tags/item/{t}.json', {'values': [f'minecraft:{i}' for i in ids]})
    mods = lambda pre, at: {'function': 'minecraft:set_attributes', 'replace': False,
                            'modifiers': [{'attribute': f'minecraft:{a}', 'id': f'bm:{pre}_{i}', 'amount': amt, 'operation': op, 'slot': 'any'} for i, (a, amt, op) in enumerate(at)]}

    # ================================================================ item modifiers: sockets (by index, x2 for gold), combos, masterworks
    for i in (1, 2):
        for c, (at, lore, vals) in SHARD.items():
            for x, mul in (('', 1), ('_x2', 2)):
                l = lore.format(*[N(v * mul) for v in vals])
                wjson(f'bm/item_modifier/p55/sock{i}_{c}{x}.json', [mods(f's{i}_{c}', [(a, amt * mul, op) for a, amt, op in at]),
                                                                    {'function': 'minecraft:set_custom_data', 'tag': f'{{bm_sn:{i},bm_s{i}:"{c}"}}'},
                                                                    {'function': 'minecraft:set_lore', 'mode': 'append',
                                                                     'lore': [T(f'◆ Socket {i} - {NAME[c][0]}: {l}' + (' (gilded)' if mul == 2 else ''), NAME[c][1])]}])
    for c in ORDER:     # sockets from before 2.35 (one per item, bm_sockc) count as socket 1
        wjson(f'bm/item_modifier/p55/legacy_{c}.json', {'function': 'minecraft:set_custom_data', 'tag': f'{{bm_sn:1,bm_s1:"{c}"}}'})
    for k, (name, lore, at) in COMBOS.items():
        wjson(f'bm/item_modifier/p55/combo_{k}.json', ([mods(f'cmb_{k}', at)] if at else []) + [
            {'function': 'minecraft:set_custom_data', 'tag': f'{{bm_cmb:"{k}"}}'},
            {'function': 'minecraft:set_lore', 'mode': 'append', 'lore': [T(f'✦ Combo - {name}: {lore}', '#ffe14a')]}])
    for cat, cols in MASTER.items():
        for c, (name, lore, at, ench) in cols.items():
            wjson(f'bm/item_modifier/p55/mw_{cat}_{c}.json', ([mods(f'mw_{cat}', at)] if at else []) +
                  ([{'function': 'minecraft:set_enchantments', 'add': True, 'enchantments': {f'bm:{ench}': 1}}] if ench else []) + [
                      {'function': 'minecraft:set_custom_data', 'tag': f'{{bm_mw:"{name.lower()}"}}'},
                      {'function': 'minecraft:set_lore', 'mode': 'append', 'lore': [T(f'★ Masterwork - {name}: {lore}', '#ff9a3c')]}])
    for b, (name, col, tgt, lore, rc, rname, rlore, _) in ESSENCE.items():
        wjson(f'bm/item_modifier/p55/ess_{b}.json', [{'function': 'minecraft:set_enchantments', 'add': True, 'enchantments': {f'bm:ess_{b}': 1}},
                                                     {'function': 'minecraft:set_custom_data', 'tag': f'{{bm_ess:"{b}"}}'},
                                                     {'function': 'minecraft:set_lore', 'mode': 'append', 'lore': [T(f'❖ {name}: {lore}', col)]}])
        wjson(f'bm/item_modifier/p55/res_{b}.json', [{'function': 'minecraft:set_enchantments', 'add': True, 'enchantments': {f'bm:res_{b}': 1}},
                                                     {'function': 'minecraft:set_custom_data', 'tag': f'{{bm_res:"{b}"}}'},
                                                     {'function': 'minecraft:set_lore', 'mode': 'append', 'lore': [T(f'❖ Resonance - {rname}: {rlore}', col)]}])
    for k, v in (('off', 'off'), ('grow', 'grow'), ('shrink', 'shrink')):
        wjson(f'bm/item_modifier/p55/red_{k}.json', {'function': 'minecraft:set_custom_data', 'tag': f'{{bm_red:"{v}"}}'})

    # ================================================================ enchantments: Masterwork Vampiric, the Essences and their Resonances
    def ench(desc, col, items, slot, effects):
        return {'anvil_cost': 8, 'description': T(desc, col), 'max_level': 1, 'weight': 1, 'min_cost': {'base': 1, 'per_level_above_first': 0},
                'max_cost': {'base': 1, 'per_level_above_first': 0}, 'slots': [slot], 'supported_items': items, 'effects': effects}
    WEAP, CHEST = [f'minecraft:netherite_{g}' for g in ('sword', 'axe', 'spear')], 'minecraft:netherite_chestplate'
    chance = lambda p: {'condition': 'minecraft:random_chance', 'chance': p}
    hit_fn = lambda f, p, who='victim', by='attacker': {'minecraft:post_attack': [{'enchanted': by, 'affected': who, 'effect': {'type': 'minecraft:run_function', 'function': f},
                                                                                  'requirements': chance(p)}]}
    regen = lambda d, a: {'type': 'minecraft:apply_mob_effect', 'to_apply': 'minecraft:regeneration', 'min_duration': float(d), 'max_duration': float(d),
                          'min_amplifier': float(a), 'max_amplifier': float(a)}
    wjson('bm/enchantment/mw_vampiric.json', ench('Vampiric', '#ff9a3c', WEAP, 'mainhand', {'minecraft:post_attack': [
        {'enchanted': 'attacker', 'affected': 'attacker', 'effect': regen(2, 2), 'requirements': chance(0.25)}]}))
    E = {'horseman': {'minecraft:post_attack': [{'enchanted': 'attacker', 'affected': 'victim', 'effect': {'type': 'minecraft:ignite', 'duration': 4}}]},
         'pharaoh': {'minecraft:damage': [{'effect': {'type': 'minecraft:add', 'value': 3}, 'requirements': {
             'condition': 'minecraft:location_check', 'predicate': {'can_see_sky': True, 'light': {'light': {'min': 13}}}}}]},
         'roc': hit_fn('bm:p53/talon/mark', 0.1),
         'treant': {'minecraft:tick': [{'effect': regen(3, 0), 'requirements': chance(0.025)}]},
         'colossus': {'minecraft:post_attack': [{'enchanted': 'victim', 'affected': 'attacker', 'effect': {'type': 'minecraft:ignite', 'duration': 4}}]},
         'voidwalker': hit_fn('bm:p55/blink', 0.1, 'victim', 'victim')}
    R = {'horseman': hit_fn('bm:p55/res/hellfire', 0.25), 'pharaoh': hit_fn('bm:p55/res/sunburst', 0.2), 'roc': hit_fn('bm:p55/res/storm', 0.25),
         'treant': hit_fn('bm:p55/res/thorns', 1.0, 'attacker', 'victim'),
         'colossus': {'minecraft:tick': [{'effect': {'type': 'minecraft:run_function', 'function': 'bm:p55/res/magma'}, 'requirements': chance(0.025)}]},
         'voidwalker': hit_fn('bm:p55/res/void', 1.0, 'victim', 'victim')}
    for b, (name, col, tgt, lore, rc, rname, rlore, _) in ESSENCE.items():
        items, slot = (WEAP, 'mainhand') if tgt == 'weapon' else (CHEST, 'chest')
        wjson(f'bm/enchantment/ess_{b}.json', ench(name, col, items, slot, E[b]))
        wjson(f'bm/enchantment/res_{b}.json', ench(rname, col, items, slot, R[b]))
    # (the resonances: run as the one struck / the wearer, at them)
    foe = 'type=#bm:p42_foe'
    fn('p55/blink', ['execute rotated ~ 0 positioned ^ ^ ^-4 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass unless block ~ ~-1 ~ #bm:grap_pass run tp @s ~ ~ ~',
                     'particle minecraft:portal ~ ~1 ~ 0.4 0.8 0.4 0.5 30', 'playsound minecraft:entity.enderman.teleport player @a[distance=..16] ~ ~ ~ 0.8 1.2'])
    fn('p55/res/hellfire', [f'execute as @e[{foe},distance=..3.5] run damage @s 4 bm:hellfire by @p[distance=..6,gamemode=!spectator]',
                            f'execute as @e[{foe},distance=..3.5] run data merge entity @s {{Fire:80s}}',
                            *[f'particle minecraft:flame ~{dx} ~0.5 ~{dz} 0.2 0.3 0.2 0.05 6' for dx, dz in ((2, 0), (-2, 0), (0, 2), (0, -2), (1.4, 1.4), (-1.4, -1.4), (1.4, -1.4), (-1.4, 1.4))],
                            'playsound minecraft:item.firecharge.use player @a[distance=..16] ~ ~ ~ 1 0.8'])
    fn('p55/res/sunburst', [f'execute as @e[{foe},distance=..4] run damage @s 4 bm:sunbeam by @p[distance=..7,gamemode=!spectator]',
                            f'execute as @e[{foe},distance=..4] run data merge entity @s {{Fire:60s}}',
                            'particle minecraft:flash{color:[1.0,0.9,0.5,1.0]} ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:end_rod ~ ~1 ~ 2 1 2 0.05 30',
                            'playsound minecraft:block.beacon.power_select player @a[distance=..16] ~ ~ ~ 1 1.6'])
    fn('p55/res/storm', [f'execute as @e[{foe},distance=0.5..6,sort=nearest,limit=2] at @s run function bm:p53/talon/smite'])
    fn('p55/res/thorns', ['damage @s 3 bm:bramble by @p[distance=0.1..6,gamemode=!spectator]', 'effect give @s minecraft:slowness 3 3',
                          f'execute as @e[{foe},distance=..3] run effect give @s minecraft:slowness 3 3',
                          'particle minecraft:block{block_state:"minecraft:sweet_berry_bush"} ~ ~1 ~ 0.5 0.5 0.5 0 20'])
    fn('p55/res/magma', ['tag @s add bm.r55w', f'execute as @e[{foe},distance=..3.5] run damage @s 2 bm:magma by @a[tag=bm.r55w,limit=1]',
                         f'execute as @e[{foe},distance=..3.5] run data merge entity @s {{Fire:60s}}', 'tag @s remove bm.r55w',
                         'particle minecraft:lava ~ ~0.5 ~ 1.5 0.3 1.5 0 6'])
    fn('p55/res/void', ['function bm:p55/blink', f'execute as @e[{foe},distance=..5] run effect give @s minecraft:levitation 2 1',
                        'particle minecraft:reverse_portal ~ ~1 ~ 2 1 2 0.05 40'])
    # their auras, while held / worn
    aura = {'horseman': 'minecraft:flame ~ ~1 ~ 0.3 0.5 0.3 0.01 2', 'pharaoh': 'minecraft:end_rod ~ ~1.2 ~ 0.35 0.5 0.35 0.01 1',
            'roc': 'minecraft:electric_spark ~ ~1 ~ 0.35 0.6 0.35 0.05 3', 'treant': 'minecraft:happy_villager ~ ~1 ~ 0.35 0.5 0.35 0 1',
            'colossus': 'minecraft:lava ~ ~0.6 ~ 0.3 0.3 0.3 0 1', 'voidwalker': 'minecraft:portal ~ ~1 ~ 0.3 0.6 0.3 0.3 4'}
    for b, (name, col, tgt, *_r) in ESSENCE.items():
        slot = 'weapon.mainhand' if tgt == 'weapon' else 'armor.chest'
        fast.append(f'execute as @a[gamemode=!spectator] if items entity @s {slot} {has("bm_res", b)} at @s run particle {aura[b]}')

    # ================================================================ the altar: honest gear only
    refuse = [f'execute if data entity @s {MH}.bm run return run ' + say('Black Market goods take no sockets or infusions - only honest vanilla gear.', '#ff6a6a'),
              f'execute if data entity @s {MH}.bm_from run return run ' + say("Bought gear takes no sockets or infusions - earn it yourself.", '#ff6a6a')]
    G.FUNCS['p24/altar/use'][:] = ['execute if predicate bm:p20/sneaking run return run function bm:p24/altar/infuse', 'function bm:p55/use']
    fn('p55/use', ['execute unless items entity @s weapon.mainhand * run return run function bm:p24/altar/help'] + refuse +
       [f'execute if items entity @s weapon.offhand *[minecraft:custom_data~{{bm:"essence_{b}"}}] run return run ' + say('Essences are infused: sneak + right-click.', '#c27dff')
        for b in ESSENCE] +
       ['scoreboard players set #c bm.rng 0'] + [f'execute if items entity @s weapon.offhand {shard(c)} run scoreboard players set #c bm.rng {i + 1}' for i, c in enumerate(ORDER)] +
       ['execute if score #c bm.rng matches 0 run return run function bm:p24/altar/help',
        'scoreboard players set #cap bm.rng 0', 'execute if items entity @s weapon.mainhand #bm:p55_sock1 run scoreboard players set #cap bm.rng 1',
        'execute if items entity @s weapon.mainhand #bm:p55_sock2 run scoreboard players set #cap bm.rng 2',
        'execute if items entity @s weapon.mainhand #bm:p55_sock3 run scoreboard players set #cap bm.rng 3',
        'execute if score #cap bm.rng matches 0 run return run ' + say('Too flimsy to hold a crystal: leather, wood, stone and chainmail take no sockets.'),
        # sockets from before 2.35 count as the first
        *[f'execute unless data entity @s {MH}.bm_sn if items entity @s weapon.mainhand {has("bm_sockc", c)} run item modify entity @s weapon.mainhand bm:p55/legacy_{c}' for c in ORDER],
        f'execute store result score #sn bm.rng run data get entity @s {MH}.bm_sn',
        'scoreboard players operation #sh bm.rng = #cap bm.rng', 'execute if score #sh bm.rng matches 3 run scoreboard players set #sh bm.rng 2',
        'execute if score #sn bm.rng < #sh bm.rng run return run function bm:p55/sock',
        f'execute if score #cap bm.rng matches 3 unless data entity @s {MH}.bm_mw run return run function bm:p55/mw',
        say('Every socket in it is full.')])
    sock = ['scoreboard players add #sn bm.rng 1', 'data modify storage bm:tmp p55 set value {x:""}',
            'execute store result storage bm:tmp p55.i int 1 run scoreboard players get #sn bm.rng',
            'execute if items entity @s weapon.mainhand #bm:p55_gilded run data modify storage bm:tmp p55.x set value "_x2"'] + \
           [f'execute if score #c bm.rng matches {i + 1} run data modify storage bm:tmp p55.c set value "{c}"' for i, c in enumerate(ORDER)] + \
           [f'execute if score #sn bm.rng matches {i} if score #c bm.rng matches {ci + 1} {g} items entity @s weapon.mainhand #bm:p55_gilded run item modify entity @s weapon.mainhand bm:p55/sock{i}_{c}{x}'
            for i in (1, 2) for ci, c in enumerate(ORDER) for g, x in (('if', '_x2'), ('unless', ''))]
    for k in COMBOS:      # the pair (socket 1 + this shard)
        a, b = [c for c in ORDER if SHORT[c] == k[0]][0], [c for c in ORDER if SHORT[c] == k[1]][0]
        for s1, s2 in {(a, b), (b, a)}:
            sock.append(f'execute if score #sn bm.rng matches 2 if score #c bm.rng matches {ORDER.index(s2) + 1} if items entity @s weapon.mainhand {has("bm_s1", s1)} '
                        f'run item modify entity @s weapon.mainhand bm:p55/combo_{k}')
    sock += ['item modify entity @s weapon.offhand bm:p24/take_1', 'function bm:p55/res_check',
             'playsound minecraft:block.amethyst_block.resonate player @a[distance=..12] ~ ~ ~ 1 1.2', 'particle minecraft:end_rod ~ ~1.2 ~ 0.3 0.3 0.3 0.05 20',
             'execute if score #sn bm.rng matches 2 if data entity @s ' + MH + '.bm_cmb run return run ' + say('Socketed - and the two crystals combine!', '#ffe14a'),
             title('@s', 'actionbar', [T('Socketed! ', '#7dff6a'), {'score': {'name': '#sn', 'objective': 'bm.rng'}, 'color': 'white'}, T(' of ', 'gray'),
                                        {'score': {'name': '#sh', 'objective': 'bm.rng'}, 'color': 'white'}, T(' sockets filled.', 'gray')])]
    fn('p55/sock', sock)
    # masterwork: netherite with both sockets full, 4 shards + a Medallion
    MED = '*[minecraft:custom_data~{bm:"medallion"}]'
    mw = ['execute store result score #n bm.rng run data get entity @s equipment.offhand.count',
          'execute if score #n bm.rng matches ..3 run return run ' + say('A Masterwork takes 4 shards in your off hand and a Medallion.', '#ff9a3c'),
          f'execute store result score #md bm.rng run clear @s {MED} 0',
          'execute if score #md bm.rng matches 0 run return run ' + say('A Masterwork takes 4 shards in your off hand and a Medallion.', '#ff9a3c'),
          'scoreboard players set #mc bm.rng 0']
    for cat, cols in MASTER.items():
        for i, c in enumerate(ORDER):
            mw.append(f'execute if score #mc bm.rng matches 0 if score #c bm.rng matches {i + 1} if items entity @s weapon.mainhand #bm:p55_mw_{cat} '
                      f'run function bm:p55/mw/{cat}_{c}')
            fn(f'p55/mw/{cat}_{c}', ['scoreboard players set #mc bm.rng 1', f'execute store result score #md bm.rng run clear @s {MED} 0',
                                     'execute if score #md bm.rng matches 0 run return 0', f'item modify entity @s weapon.mainhand bm:p55/mw_{cat}_{c}',
                                     'item modify entity @s weapon.offhand bm:p24/take_4', f'clear @s {MED} 1',
                                     'playsound minecraft:block.anvil.use player @a[distance=..12] ~ ~ ~ 0.8 1.2',
                                     'playsound minecraft:block.beacon.power_select player @a[distance=..12] ~ ~ ~ 1 1.4', 'particle minecraft:wax_on ~ ~1.2 ~ 0.4 0.4 0.4 0 30',
                                     title('@s', 'actionbar', [T('Masterwork: ', '#ff9a3c', bold=True), T(f'{cols[c][0]} - {cols[c][1]}', '#ffd23f')])])
    fn('p55/mw', mw)
    # resonance: an Essence and a socket of its colour on one item
    rc_ = []
    for b, (name, col, tgt, lore, rc, *_r) in ESSENCE.items():
        for s in ('bm_s1', 'bm_s2'):
            rc_.append(f'execute unless data entity @s {MH}.bm_res if items entity @s weapon.mainhand {has("bm_ess", b)} if items entity @s weapon.mainhand {has(s, rc)} '
                       f'run function bm:p55/res_apply/{b}')
        fn(f'p55/res_apply/{b}', [f'item modify entity @s weapon.mainhand bm:p55/res_{b}', 'playsound minecraft:block.end_portal.spawn player @a[distance=..16] ~ ~ ~ 0.5 1.6',
                                  'particle minecraft:totem_of_undying ~ ~1.2 ~ 0.4 0.6 0.4 0.3 40', title('@s', 'subtitle', T('The essence and the crystal sing together.', 'gray', italic=True)),
                                  title('@s', 'title', T('RESONANCE', '#ffd23f', bold=True))])
    fn('p55/res_check', rc_)
    # sneak + right-click: Essences, and the red crystal's size
    inf = G.FUNCS['p24/altar/infuse']
    ess = [f'execute if items entity @s weapon.offhand *[minecraft:custom_data~{{bm:"essence_{b}"}}] run return run function bm:p55/ess/{b}' for b in ESSENCE]
    red = [f'execute if items entity @s weapon.offhand {shard("red")} if items entity @s weapon.mainhand {has(k, "red")} run return run function bm:p55/red_cycle'
           for k in ('bm_s1', 'bm_s2', 'bm_sockc')]
    inf[0:0] = ['execute if items entity @s weapon.mainhand * run function bm:p55/refuse_check', 'execute if score #rf bm.rng matches 1 run return 0'] + ess + red
    fn('p55/refuse_check', ['scoreboard players set #rf bm.rng 0',
       f'execute if data entity @s {MH}.bm unless items entity @s weapon.mainhand {has("bm", "gravity_boots")} run scoreboard players set #rf bm.rng 1',
        f'execute if data entity @s {MH}.bm_from run scoreboard players set #rf bm.rng 1',
        'execute if score #rf bm.rng matches 1 run ' + say('Black Market goods take no sockets or infusions - only honest vanilla gear.', '#ff6a6a')])
    fn('p55/red_cycle', [f'execute if items entity @s weapon.mainhand {has("bm_red", "grow")} run return run function bm:p55/red_to/shrink',
                         f'execute if items entity @s weapon.mainhand {has("bm_red", "shrink")} run return run function bm:p55/red_to/off',
                         'function bm:p55/red_to/grow'])
    for m, w in (('grow', 'GROWTH'), ('shrink', 'SHRINK'), ('off', 'no size change')):
        fn(f'p55/red_to/{m}', [f'item modify entity @s weapon.mainhand bm:p55/red_{m}', 'item modify entity @s weapon.offhand bm:p24/take_1',
                               'playsound minecraft:block.amethyst_block.resonate player @a[distance=..12] ~ ~ ~ 1 0.6', say(f'The red crystal shifts: {w}.', '#ff4a4a')])
    for b, (name, col, tgt, lore, *_r) in ESSENCE.items():
        ok_ = '#bm:p55_mw_weapon' if tgt == 'weapon' else 'minecraft:netherite_chestplate'
        what = 'a netherite sword, axe or spear' if tgt == 'weapon' else 'a netherite chestplate'
        fn(f'p55/ess/{b}', [f'execute unless items entity @s weapon.mainhand {ok_} run return run ' + say(f'{name} only takes to {what}.', col),
                            f'execute if data entity @s {MH}.bm_ess run return run ' + say('It already carries an essence.', 'gray'),
                            f'item modify entity @s weapon.mainhand bm:p55/ess_{b}', 'item modify entity @s weapon.offhand bm:p24/take_1', 'function bm:p55/res_check',
                            'playsound minecraft:block.beacon.activate player @a[distance=..12] ~ ~ ~ 1 1.2', f'particle minecraft:dust{{color:[1.0,0.8,0.4],scale:1.5}} ~ ~1.2 ~ 0.3 0.4 0.3 0 30',
                            say(f'Infused: {name} - {lore}.', col)])
    G.FUNCS['p24/altar/help'][:] = [tellraw('@s', PREFIX + [T('Xenite Altar: ', '#7dff6a', bold=True), T('honest vanilla gear only. ', '#ff6a6a'),
                                                            T('Hold the item, a shard in your off hand, right-click to fill its next socket. ', 'gray'),
                                                            T('Sockets: copper/iron/gold 1 (gold doubles), diamond/trident/mace 2, netherite 2 + a Masterwork (4 shards + a Medallion). ', 'gray'),
                                                            T('Two shards in one item combine. ', '#ffe14a'),
                                                            T('Sneak + right-click: infusions (boots + 6 violet, compass + 6 cyan, crossbow + 8 green, bottle + 4 cyan, pearl + 6 violet), ', 'gray'),
                                                            T('Relic Essences into netherite gear, and a red shard cycles a red socket\'s size.', '#c27dff')])]

    # ================================================================ combo abilities: Bloodlust (kills heal), Second Wind (low health)
    wjson('bm/advancement/p55/kill.json', {'criteria': {'k': {'trigger': 'minecraft:player_killed_entity'}}, 'rewards': {'function': 'bm:p55/bloodlust'}})
    fn('p55/bloodlust', ['advancement revoke @s only bm:p55/kill',
                         f'execute if items entity @s weapon.mainhand {has("bm_cmb", "gr")} run return run function bm:p55/bl_heal',
                         f'execute if items entity @s armor.* {has("bm_cmb", "gr")} run function bm:p55/bl_heal'])
    fn('p55/bl_heal', ['effect give @s minecraft:instant_health 1 0 true', 'particle minecraft:dust{color:[0.8,0.05,0.05],scale:1.2} ~ ~1 ~ 0.3 0.5 0.3 0 12'])
    second += ['scoreboard players remove @a[scores={bm.r55cd=1..}] bm.r55cd 1',
               f'execute as @a[gamemode=!spectator] unless score @s bm.r55cd matches 1.. if items entity @s armor.* {has("bm_cmb", "vr")} at @s run function bm:p55/sw',
               f'execute as @a[gamemode=!spectator] unless score @s bm.r55cd matches 1.. if items entity @s weapon.mainhand {has("bm_cmb", "vr")} at @s run function bm:p55/sw']
    fn('p55/sw', ['execute store result score #h bm.rng run data get entity @s Health', 'execute if score #h bm.rng matches 7.. run return 0',
                  'effect give @s minecraft:regeneration 5 1', 'effect give @s minecraft:speed 5 1', 'scoreboard players set @s bm.r55cd 60',
                  'execute at @s run particle minecraft:totem_of_undying ~ ~1 ~ 0.4 0.6 0.4 0.2 20',
                  'execute at @s run playsound minecraft:item.totem.use player @a[distance=..12] ~ ~ ~ 0.4 1.6', say('Second Wind!', '#ffe14a')])

    # ================================================================ the Scrap Bin takes spare relics: Tokens, Medallions and the boss's Essence
    load = G.FUNCS['load']
    load[-1:-1] = [f'data modify storage bm:scrap money.essence_{b} set value {snbt({k: v for k, v in G.stack(f"essence_{b}", 1).items() if k != "count"})}' for b in ESSENCE]
    for b, (*_r, relics) in ESSENCE.items():
        for r in relics:
            load.insert(-1, f'data modify storage bm:scrap table.{r} set value ' +
                        snbt({'k': Int(1), 'r': [{'c': 'token', 'n': Int(10)}, {'c': 'medallion', 'n': Int(2)}, {'c': f'essence_{b}', 'n': Int(1)}]}))
            G.SCRAP_TABLE[r] = (1, [('token', 10), ('medallion', 2), (f'essence_{b}', 1)])
    fn('admin/essences', [give(f'essence_{b}', 2) for b in ESSENCE] + [give(f'xenite_{c}', 16) for c in ORDER] + [give('medallion', 4)])

    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


# ===================================================================== resource pack: the Essences' icons
def rp(R):
    from PIL import Image
    def hx(c): return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))
    for b, (name, col, *_r) in ESSENCE.items():
        im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
        base = hx(col)
        for y in range(16):
            for x in range(16):
                d = ((x - 7.5) ** 2 + (y - 8.5) ** 2) ** 0.5
                if d <= 5.6:
                    k = max(0.0, 1 - d / 6.5)
                    im.putpixel((x, y), tuple(min(255, int(c * (0.55 + 0.6 * k)) + int(90 * k * k)) for c in base) + (255,))
        for (x, y) in [(6, 6), (7, 6), (6, 7)]:
            im.putpixel((x, y), (255, 255, 255, 255))
        for (x, y) in [(7, 1), (7, 2), (8, 2), (12, 4), (3, 4)]:
            im.putpixel((x, y), base + (200,))
        R.ICONS[f'essence_{b}'] = im

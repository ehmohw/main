"""2.60: the Gilded Gutter Vault's treasures (phase70 is the heist itself).

CURRENCY & TOOLS OF THE TRADE
- GUTTER COIN: the vault's own money - every haul, every guard. Spent only with Goldtooth in the Fixer's Den (never in the
  market, never counted for standing).
- HEIST PLANS (the Fence, 6 Tokens, reusable): start a heist, or join your party's.
- SMOKE BOMB: in a heist, the alarm drops by 20 and everyone near turns invisible for 8 seconds.
- SKELETON LOCKPICK: in a heist, beat the puzzle room you're standing in (no trophy for it, though).
ARMOUR
- THE GILDED SET (one piece for the first clear of each of tiers I-IV; sometimes in later hauls): diamond-grade armour that
  brings luck. All four: no fall damage, and nearby drops fly to you.
- THIEF'S COWL: while you sneak you're invisible, and quick on your feet.
- SMUGGLER'S BOOTS: faster, longer strides (step up a block), and you fall further unhurt.
- CIPHER MONOCLE (worn on the head): shows pressure plates and tripwires within 6 blocks; in the vault, also the tiles that
  won't hold and the coffers that bite.
WEAPONS
- HEISTER'S SHIV: a quick dagger. AMBUSH: a monster that isn't after you takes a second, hidden stab (+6).
- VAULT BREAKER: a heavy hammer. Each blow sends a shockwave through the monsters around the one you hit.
- COINSLINGER: a crossbow (quick, piercing, three bolts). Bolts burst into coins: damage all round the target.
- GUTTER KING'S CUTLASS: bleeding cuts; now and then a slain monster coughs up a Gutter Coin.
- THE TREASURER'S SCEPTER (first clear of tier V): COIN STORM - gold rains on every monster within 6 (12 damage, flung up).
TOGETHER
- BOND SIGIL (every member of a party of 2+, bound to that heist): carry it near someone holding a sigil from the same heist
  and you both regenerate, with a little absorption now and then.
- RAID BANNER (I-V, one per first clear, each finer than the last): set it down - your party (or you) nearby is healed and
  quickened; tier III+ also strengthens, tier V also resists.
PUZZLES
- CLOCKWORK KEY FRAGMENT (a chance whenever a room is beaten): use four to make a CLOCKWORK KEY; use it by the copper door
  in the den and the CLOCKWORK CACHE opens (three more shares each).
- PUZZLE TROPHIES: beat a room cleanly (no mistakes / quickly) for its trophy - seven to collect, each a little statue you can
  set down (sneak + punch to take it back).
FOLLOWERS
- GILDED STAFF TOPPER: use it near your Cecil - his crescent is gilded for good (every element).
- GOLDEN SPEAR: use it near Celi - her spear turns gold and diamond.
- FROG'S MONOCLE: use it near the Frog with Mustache - a distinguished monocle.
- VAULT HOUND WHISTLE: a gold-collared hound that follows you and sniffs out unopened loot chests within 12 blocks.
FOR THE FASTEST - the GUTTER LAUREL: a crown of golden light (keep it in your inventory).
SPECIAL NIGHTS' PRIZES - CRIMSON LEDGER (Blood Moon: every monster you kill heals you), GAMBLER'S COIN (Lucky Night: flip
it - heads, Luck II for two minutes), VORN CRACKING RIG (Invasion: a reusable lockpick for the vault, every 10 minutes)."""
from items import item, T, TOTEM, ITEMS, DYNAMIC, ITEM_VERSION
from useitem import hold, HOLD
from nbt import snbt, B, F, D, Int

GOLD = '#ffcf40'
UNBR = {'minecraft:unbreakable': {}}
KINDS = ['levers', 'plates', 'lasers', 'tiles', 'dial', 'guards', 'coffers']
TROPHY_NAME = {'levers': 'Combination', 'plates': 'Scales', 'lasers': 'Gauntlet', 'tiles': 'Tile Floor', 'dial': 'Dial Lock',
               'guards': 'Counting House', 'coffers': 'Honest Coffer'}


def attr(a, amt, slot, op='add_value', n=''):
    return {'type': f'minecraft:{a}', 'amount': amt, 'operation': op, 'slot': slot, 'id': f'bm:gv_{a}_{slot}{n}'}


# ---------------------------------------------------------------- currency, tools
item('gutter_coin', TOTEM, 'Gutter Coin', GOLD, ['A heavy coin stamped with a grinning rat.', ('Goldtooth takes them in the Fixer\'s Den.', 'gray'),
                                                ('Good nowhere else - and that\'s the point.', 'dark_gray')], model='bm:gutter_coin', stack=64, cat='currency')
item('smoke_bomb', TOTEM, 'Smoke Bomb', '#9a9aa8', ['A clay ball that fizzes when shaken.', ('Use in a heist: the alarm drops by 20,', 'blue'),
                                                    ('and everyone near is invisible for 8 s.', 'blue')], model='bm:smoke_bomb', stack=16, cat='misc', comps=hold('none'))
HOLD['smoke_bomb'] = 'bm:p71/smoke'
item('skeleton_lockpick', TOTEM, 'Skeleton Lockpick', '#e8e0c8', ['It opens anything. Once.', ('Use in a heist room: beat its puzzle', 'blue'),
                                                                  ('(no trophy for that room).', 'gray')], model='bm:skeleton_lockpick', stack=8, cat='misc', comps=hold('none'))
HOLD['skeleton_lockpick'] = 'bm:p71/pick'

# ---------------------------------------------------------------- armour
GILD = [('helmet', 'head', 3, 'Gilded Crown-Helm'), ('chestplate', 'chest', 8, 'Gilded Cuirass'), ('leggings', 'legs', 6, 'Gilded Greaves'), ('boots', 'feet', 3, 'Gilded Sabatons')]
for _p, _slot, _arm, _nm in GILD:
    item(f'gilded_{_p}', f'minecraft:golden_{_p}', _nm, GOLD,
         ['Vault gold over blackstone plate.', ('+1 Luck.', 'blue'), ('Full Gilded set: no fall damage,', 'light_purple'), ('and nearby drops fly to you.', 'light_purple')],
         model=f'bm:gilded_{_p}', stack=1, cat='armor', tier=3, comps=dict(UNBR, **{
             'minecraft:attribute_modifiers': [attr('armor', _arm, _slot), attr('armor_toughness', 2, _slot), attr('luck', 1, _slot)],
             'minecraft:equippable': {'slot': _slot, 'asset_id': 'bm:gilded', 'equip_sound': 'minecraft:item.armor.equip_gold'}}))
item('thiefs_cowl', 'minecraft:leather_helmet', "Thief's Cowl", '#5a5a6a', ['Soft black wool, deep in the hood.', ('While you sneak: invisible, and quick.', 'blue')],
     stack=1, cat='armor', tier=2, comps=dict(UNBR, **{'minecraft:dyed_color': 0x26262e, 'minecraft:attribute_modifiers': [attr('armor', 2, 'head')]}))
item('smugglers_boots', 'minecraft:leather_boots', "Smuggler's Boots", '#8a6a4a', ['Soft soles, deep pockets.', ('Faster; step up a whole block;', 'blue'), ('fall further unhurt.', 'blue')],
     stack=1, cat='armor', tier=2, comps=dict(UNBR, **{'minecraft:dyed_color': 0x5a3e28, 'minecraft:attribute_modifiers': [
         attr('armor', 2, 'feet'), attr('movement_speed', 0.12, 'feet', 'add_multiplied_base'), attr('step_height', 0.5, 'feet'), attr('safe_fall_distance', 4, 'feet')]}))
item('cipher_monocle', TOTEM, 'Cipher Monocle', '#a8e0ff', ['A lens etched with tiny ciphers.', ('Worn: pressure plates and tripwires glint', 'blue'),
                                                            ('within 6 blocks. In the vault: the tiles that', 'blue'), ("won't hold, and the coffers that bite.", 'blue')],
     model='bm:cipher_monocle', stack=1, cat='cosmetic', tier=2, comps={'minecraft:equippable': {'slot': 'head', 'swappable': True, 'equip_sound': 'minecraft:item.armor.equip_gold'}})

# ---------------------------------------------------------------- weapons
def wpn(dmg, spd, slot='mainhand'):
    return [{'type': 'minecraft:attack_damage', 'amount': dmg - 1, 'operation': 'add_value', 'slot': slot, 'id': 'minecraft:base_attack_damage'},
            {'type': 'minecraft:attack_speed', 'amount': spd - 4, 'operation': 'add_value', 'slot': slot, 'id': 'minecraft:base_attack_speed'}]
item('heisters_shiv', 'minecraft:iron_sword', "Heister's Shiv", '#c8c8d8', ['Short, sharp, quiet.', ('AMBUSH: a monster that isn\'t after you', 'blue'), ('takes a second, hidden stab (+6).', 'blue')],
     model='bm:heisters_shiv', stack=1, cat='weapon', tier=2, comps=dict(UNBR, **{'minecraft:attribute_modifiers': wpn(5, 2.2)}))
item('vault_breaker', 'minecraft:netherite_axe', 'Vault Breaker', '#ffb84a', ['A safecracker\'s sledge, gold-banded.', ('Each blow: a shockwave through the', 'blue'),
                                                                            ('monsters around the one you hit.', 'blue')],
     model='bm:vault_breaker', stack=1, cat='weapon', tier=3, comps=dict(UNBR, **{'minecraft:attribute_modifiers': wpn(12, 0.8)}))
item('coinslinger', 'minecraft:crossbow', 'Coinslinger', GOLD, ['It fires bolts wrapped in coin.', ('Bolts burst into coins: damage all', 'blue'), ('round the target.', 'blue')],
     stack=1, cat='weapon', tier=3, comps=dict(UNBR, **{'minecraft:enchantments': {'minecraft:quick_charge': 2, 'minecraft:piercing': 3, 'minecraft:multishot': 1}}))
item('gutter_cutlass', 'minecraft:diamond_sword', "Gutter King's Cutlass", '#ff8a4a', ['A pirate king\'s blade, gold at the hilt.', ('Cuts bleed (Wither).', 'blue'),
                                                                                    ('Slain monsters may cough up a Gutter Coin.', 'blue')],
     model='bm:gutter_cutlass', stack=1, cat='weapon', tier=3, comps=dict(UNBR, **{'minecraft:attribute_modifiers': wpn(8, 1.6), 'minecraft:enchantments': {'minecraft:sweeping_edge': 3}}))
item('treasurers_scepter', 'minecraft:carrot_on_a_stick', "The Treasurer's Scepter", GOLD, ['The vault\'s own sceptre. It rattles with coin.', ('Use: COIN STORM - gold rains on every', 'blue'),
                                                                                         ('monster within 6 (12 damage, flung up).', 'blue'), ('Every 20 seconds.', 'gray')],
     model='bm:treasurers_scepter', stack=1, cat='weapon', tier=3, bold=True, comps=dict(UNBR, **hold('none')))
HOLD['treasurers_scepter'] = 'bm:p71/scepter'

# ---------------------------------------------------------------- together
item('bond_sigil', TOTEM, 'Bond Sigil', '#ff9ad8', ['A gold sigil, warm when a friend is near.', ('Near someone carrying a sigil from the same', 'blue'),
                                                    ('heist: you both regenerate.', 'blue'), ('Bound to one heist.', 'gray')], model='bm:bond_sigil', stack=1, cat='magic')
DYNAMIC.add('bond_sigil')         # (a re-sync keeps its bond)
BANNER_LOOKS = {
    1: [('minecraft:border', 'black')],
    2: [('minecraft:border', 'black'), ('minecraft:stripe_middle', 'black')],
    3: [('minecraft:gradient', 'orange'), ('minecraft:border', 'black'), ('minecraft:rhombus', 'black')],
    4: [('minecraft:gradient', 'orange'), ('minecraft:stripe_downleft', 'black'), ('minecraft:stripe_downright', 'black'), ('minecraft:border', 'black'), ('minecraft:circle', 'yellow')],
    5: [('minecraft:gradient_up', 'black'), ('minecraft:rhombus', 'yellow'), ('minecraft:circle', 'black'), ('minecraft:flower', 'yellow'), ('minecraft:border', 'black'),
        ('minecraft:curly_border', 'black')]}
for _t, _pats in BANNER_LOOKS.items():
    _num = ['I', 'II', 'III', 'IV', 'V'][_t - 1]
    item(f'raid_banner_{_t}', 'minecraft:yellow_banner', f'Raid Banner {_num}', GOLD,
         [f'Raised over a tier {_num} vault.', ('Sneak + use on a block: set it down.', 'blue'), ('Your party nearby is healed and quickened' + (',' if _t >= 3 else '.'), 'blue')] +
         ([('and strengthened' + (', and resists.' if _t == 5 else '.'), 'blue')] if _t >= 3 else []) + [('Punch it while sneaking: pick it up.', 'gray')],
         stack=1, cat='magic', tier=2, comps=dict(hold('none'), **{'minecraft:banner_patterns': [{'pattern': p, 'color': c} for p, c in _pats],
                                                                   'minecraft:tooltip_display': {'hidden_components': ['minecraft:banner_patterns']}}))
    HOLD[f'raid_banner_{_t}'] = f'bm:p71/banner/place{_t}'

# ---------------------------------------------------------------- puzzles
item('clockwork_fragment', TOTEM, 'Clockwork Key Fragment', '#d9a066', ['A cog-toothed sliver of brass.', ('Use with four: make a Clockwork Key.', 'blue')],
     model='bm:clockwork_fragment', stack=16, cat='misc', comps=hold('none'))
HOLD['clockwork_fragment'] = 'bm:p71/assemble'
item('clockwork_key', TOTEM, 'Clockwork Key', '#e8b070', ['It ticks.', ('Use by the copper door in the Fixer\'s Den:', 'blue'), ('the Clockwork Cache opens.', 'blue')],
     model='bm:clockwork_key', stack=1, cat='misc', comps=hold('none'))
HOLD['clockwork_key'] = 'bm:p71/key'
for _k in KINDS:
    item(f'trophy_{_k}', TOTEM, f'{TROPHY_NAME[_k]} Trophy', GOLD, ['A little gold statue of a vault room, beaten cleanly.', ('Sneak + use on a block: set it down.', 'blue'),
                                                                  ('Sneak + punch: pick it up.', 'gray')], model=f'bm:trophy_{_k}', stack=1, cat='fun', comps=hold('none'))
    HOLD[f'trophy_{_k}'] = f'bm:p71/deco/place_trophy_{_k}'

# ---------------------------------------------------------------- followers
item('gilded_staff_topper', TOTEM, 'Gilded Staff Topper', GOLD, ['A gold crescent cap for a wizard\'s staff.', ('Use near your Cecil: his crescent is', 'blue'),
                                                                  ('gilded for good (in every element).', 'blue')], model='bm:gilded_staff_topper', stack=1, cat='cosmetic', comps=hold('none'))
HOLD['gilded_staff_topper'] = 'bm:p71/topper'
item('golden_spear', TOTEM, 'Golden Spearhead', GOLD, ['Gold and diamond, sharpened for an elf.', ('Use near Celi: her spear turns gold.', 'blue')],
     model='bm:golden_spear', stack=1, cat='cosmetic', comps=hold('none'))
HOLD['golden_spear'] = 'bm:p71/gspear'
item('frog_monocle', TOTEM, "Frog's Monocle", '#d8e8ff', ['A monocle for a very distinguished frog.', ('Use near the Frog with Mustache.', 'blue')],
     model='bm:frog_monocle', stack=1, cat='cosmetic', comps=hold('none'))
HOLD['frog_monocle'] = 'bm:p71/fmono'
item('vault_hound_whistle', TOTEM, 'Vault Hound Whistle', GOLD, ['A gold whistle on a chain.', ('Use: your Vault Hound comes (use again: it', 'blue'),
                                                                 ('comes to you; sneak + use: home it goes).', 'blue'), ('It sniffs out unopened loot chests nearby.', 'blue'),
                                                                 ('If it faints, just whistle again.', 'gray')], model='bm:vault_hound_whistle', stack=1, cat='magic', tier=3, comps=hold('none'))
HOLD['vault_hound_whistle'] = 'bm:p71/hound/use'
item('gutter_laurel', TOTEM, 'Gutter Laurel', GOLD, ['For the fastest heist of the week.', ('In your inventory: a crown of golden light.', 'blue')],
     model='bm:gutter_laurel', stack=1, cat='cosmetic', tier=3, glint=True)

# ---------------------------------------------------------------- special nights
item('crimson_ledger', TOTEM, 'Crimson Ledger', '#ff3030', ['The Treasurer\'s book, written in blood.', ('In your inventory: every monster you kill', 'blue'),
                                                            ('heals you a heart.', 'blue'), ('From a Blood Moon heist.', 'dark_red')], model='bm:crimson_ledger', stack=1, cat='magic', tier=3)
item('gamblers_coin', TOTEM, "Gambler's Coin", '#7dff6a', ['Double-headed? Let\'s find out.', ('Use: flip it - heads, Luck II for two minutes.', 'blue'),
                                                           ('Every 5 minutes.', 'gray'), ('From a Lucky Night heist.', 'dark_green')], model='bm:gamblers_coin', stack=1, cat='magic', tier=3, comps=hold('none'))
HOLD['gamblers_coin'] = 'bm:p71/flip'
item('vorn_cracking_rig', TOTEM, 'Vorn Cracking Rig', '#b6ff3c', ['Vorn safecracking tech, beeping softly.', ('Use in a heist room: beat its puzzle', 'blue'),
                                                                  ('(no trophy). Every 10 minutes.', 'blue'), ('From an Invasion heist.', '#6a9a2a')],
     model='bm:vorn_cracking_rig', stack=1, cat='alien', tier=3, comps=hold('none'))
HOLD['vorn_cracking_rig'] = 'bm:p71/rig'


def extend_offers(O, offer):
    O['fence'].insert(0, offer(('token', 6), ('fixers_ledger', 1)))     # (2.75: the Ledger - it plans heists now; 2.76: first on his list)


def generate(G):
    fn, wjson, title, tellraw, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    objs = ['bm.gvcd', 'bm.gvsc', 'bm.gvrg', 'bm.gvfl', 'bm.cpgild', 'bm.cegold', 'bm.frmono', 'bm.vhcd', 'bm.vhs', 'bm.gvamb']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    tick, fast, second = [], [], []
    clear1 = lambda i: f'execute unless entity @s[gamemode=creative] run clear @s {holds(i)} 1'
    PL = [T('[Heist] ', GOLD, bold=True)]

    # ------------------------------------------------------------------ tools of the trade
    fn('p71/smoke', ['execute unless entity @s[tag=bm.gvp] run return run ' + say('Save it for a heist.'),
                     clear1('smoke_bomb'), 'effect give @a[distance=..5,gamemode=!spectator] minecraft:invisibility 8 0', 'particle minecraft:campfire_cosy_smoke ~ ~1 ~ 1.5 1 1.5 0.02 80',
                     'particle minecraft:large_smoke ~ ~1 ~ 1.5 1 1.5 0.05 40', 'playsound minecraft:entity.generic.extinguish_fire player @a[distance=..16] ~ ~ ~ 1 0.6',
                     'scoreboard players operation #gi bm.rng = @s bm.gvi', 'execute as @e[type=marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run function bm:p71/hush'])
    fn('p71/hush', ['scoreboard players remove @s bm.gva 20', 'execute if score @s bm.gva matches ..-1 run scoreboard players set @s bm.gva 0', 'function bm:p70/bar'])
    # (a room you're in, unbeaten, that a lockpick can beat)
    PICKABLE = ['levers', 'plates', 'lasers', 'tiles', 'dial', 'coffers']
    sel_room = '@e[type=marker,tag=bm.gvr,distance=..16,sort=nearest,limit=1]'
    fn('p71/pick', ['execute unless entity @s[tag=bm.gvp] run return run ' + say('Save it for a heist.'),
                    'scoreboard players set #ok bm.rng 0',
                    'execute as ' + sel_room + ' unless score @s bm.gvs matches 3 if entity @s[' + ','.join(f'tag=!bm.gvr_{k}' for k in ('guards', 'vault', 'lobby', 'cache')) + '] run scoreboard players set #ok bm.rng 1',
                    'execute if score #ok bm.rng matches 0 run return run ' + say('No lock here to pick.'),
                    clear1('skeleton_lockpick'), 'function bm:p71/crack'])
    fn('p71/crack', ['execute as ' + sel_room + ' at @s run function bm:p71/crack1', 'playsound minecraft:block.iron_trapdoor.open player @a[distance=..16] ~ ~ ~ 1 1.6',
                     say('Click... click... clunk. Open.', GOLD)])
    fn('p71/crack1', ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'scoreboard players set @s bm.gvf 1', 'function bm:p70/solved'])
    fn('p71/rig', ['execute unless entity @s[tag=bm.gvp] run return run ' + say('Save it for a heist.'),
                   'execute if score @s bm.gvrg matches 1.. run return run ' + say('The rig is still recharging.', '#b6ff3c'),
                   'scoreboard players set #ok bm.rng 0',
                   'execute as ' + sel_room + ' unless score @s bm.gvs matches 3 if entity @s[' + ','.join(f'tag=!bm.gvr_{k}' for k in ('guards', 'vault', 'lobby', 'cache')) + '] run scoreboard players set #ok bm.rng 1',
                   'execute if score #ok bm.rng matches 0 run return run ' + say('No lock here to crack.'),
                   'scoreboard players set @s bm.gvrg 600', 'particle minecraft:dust{color:[0.5,1.0,0.3],scale:1.2} ~ ~1 ~ 0.5 0.5 0.5 0 30', 'function bm:p71/crack'])
    second.append('scoreboard players remove @a[scores={bm.gvrg=1..}] bm.gvrg 1')

    # ------------------------------------------------------------------ the Gilded set: luck in every piece; all four - no fall damage, drops fly to you
    full = ' '.join(f'if items entity @s armor.{s} {holds("gilded_" + p)}' for p, s, _a, _n in GILD)
    fast.append(f'execute as @a {full} at @s run function bm:p71/gilded')
    fast.append(f'execute as @a[tag=bm.gvgild] unless entity @s[tag=bm.gvgild2] run function bm:p71/gilded_off')
    fast.append('tag @a remove bm.gvgild2')
    fn('p71/gilded', ['tag @s add bm.gvgild', 'tag @s add bm.gvgild2', 'attribute @s minecraft:fall_damage_multiplier modifier add bm:gv_gilded -1 add_multiplied_total',
                      'tp @e[type=minecraft:item,distance=1.2..6,nbt=!{PickupDelay:32767s}] @s', 'tp @e[type=minecraft:experience_orb,distance=1.2..6] @s'])
    G.FUNCS['p71/gilded'][3] = 'execute as @e[type=minecraft:item,distance=1.2..6] unless data entity @s {PickupDelay:32767s} run tp @s ~ ~0.3 ~'
    fn('p71/gilded_off', ['tag @s remove bm.gvgild', 'attribute @s minecraft:fall_damage_multiplier modifier remove bm:gv_gilded'])
    # Thief's Cowl: sneaking - invisible and quick
    fast.append(f'execute as @a if items entity @s armor.head {holds("thiefs_cowl")} if predicate bm:p20/sneaking run function bm:p71/cowl')
    fn('p71/cowl', ['effect give @s minecraft:invisibility 1 0 true', 'effect give @s minecraft:speed 1 1 true'])
    # Cipher Monocle: plates and tripwires glint within 6; in the vault, the tiles that won't hold and the coffers that bite
    scan = []
    for dx in range(-6, 7):
        for dz in range(-6, 7):
            if dx * dx + dz * dz > 40: continue
            for dy in (-1, 0, 1):
                scan.append(f'execute if block ~{dx} ~{dy} ~{dz} #bm:p71_traps run particle minecraft:wax_off ~{dx} ~{dy + 0.2} ~{dz} 0.15 0.05 0.15 0 1 normal @s')
    fn('p71/mono_scan', scan)
    wjson('bm/tags/block/p71_traps.json', {'values': ['#minecraft:pressure_plates', 'minecraft:tripwire', 'minecraft:tripwire_hook']})
    second.append(f'execute as @a if items entity @s armor.head {holds("cipher_monocle")} at @s run function bm:p71/monocle')
    fn('p71/monocle', ['function bm:p71/mono_scan',
                       'execute as @e[type=marker,tag=bm.gvtile,distance=..12,scores={bm.gvsafe=0}] at @s run particle minecraft:dust{color:[1.0,0.2,0.2],scale:1} ~ ~0.15 ~ 0.6 0 0.6 0 3 normal @a[tag=bm.gvmono]',
                       'execute as @e[type=marker,tag=bm.gvr_coffers,distance=..16] at @s run function bm:p71/mono_cof',
                       'execute as @e[type=minecraft:rabbit,tag=bm.mimic,distance=..12] on passengers run data merge entity @s {Glowing:1b}'])
    G.FUNCS['p71/monocle'].insert(0, 'tag @s add bm.gvmono'); G.FUNCS['p71/monocle'].append('tag @s remove bm.gvmono')
    CZ = [6, 10, 14, 18]
    import phase70_rooms as RM
    fn('p71/mono_cof', [f'execute unless score @s bm.gvc matches {i} positioned {RM.rel(19, 6, z)} run particle minecraft:angry_villager ~ ~ ~ 0.1 0.1 0.1 0 1 normal @a[tag=bm.gvmono]' for i, z in enumerate(CZ)])

    # ------------------------------------------------------------------ weapons
    def melee_adv(name, iid, fn_name, proj=False):
        dmg = {'type': {'is_direct': not proj, 'tags': [{'id': '#minecraft:is_projectile', 'expected': proj}]}}
        wjson(f'bm/advancement/p71/{name}.json', {'criteria': {'hit': {'trigger': 'minecraft:player_hurt_entity', 'conditions': {
            'player': [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'equipment': {'mainhand': {'predicates': {'minecraft:custom_data': f'{{bm:"{iid}"}}'}}}}}],
            'damage': dmg}}}, 'rewards': {'function': f'bm:{fn_name}'}})
    mob = 'type=#bm:hostile,tag=!bm.npc'
    # the shiv: an ambush stab half a second on (once its blow's hurt-immunity has passed), if the monster wasn't after you
    melee_adv('shiv', 'heisters_shiv', 'p71/shiv')
    fn('p71/shiv', ['advancement revoke @s only bm:p71/shiv', 'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                    'scoreboard players operation #me bm.pid = @s bm.pid', 'tag @s add bm.gvatk',
                    f'execute at @s as @e[{mob},distance=..6,nbt={{HurtTime:10s}},sort=nearest,limit=1] at @s run function bm:p71/shiv_mark', 'tag @s remove bm.gvatk'])
    fn('p71/shiv_mark', ['scoreboard players set #after bm.rng 0', 'execute on target if entity @s[tag=bm.gvatk] run scoreboard players set #after bm.rng 1',
                         'execute if score #after bm.rng matches 1 run return 0', 'scoreboard players operation @s bm.gvsc = #me bm.pid', 'scoreboard players set @s bm.gvamb 11',
                         'particle minecraft:crit ~ ~1 ~ 0.3 0.4 0.3 0.2 10'])
    tick.append('execute as @e[scores={bm.gvamb=1..}] at @s run function bm:p71/shiv_tick')
    fn('p71/shiv_tick', ['scoreboard players remove @s bm.gvamb 1', 'execute if score @s bm.gvamb matches 1.. run return 0',
                         'scoreboard players operation #me bm.pid = @s bm.gvsc', 'execute as @a if score @s bm.pid = #me bm.pid run tag @s add bm.gvatk',
                         'execute if entity @a[tag=bm.gvatk] run damage @s 6 minecraft:player_attack by @a[tag=bm.gvatk,limit=1]',
                         'execute at @s run particle minecraft:damage_indicator ~ ~1 ~ 0.2 0.3 0.2 0 6', 'execute at @s run playsound minecraft:entity.player.attack.crit player @a[distance=..12] ~ ~ ~ 1 1.4',
                         'tag @a[tag=bm.gvatk] remove bm.gvatk'])
    # the hammer: a shockwave through the others (not the one hit - it already felt it)
    melee_adv('breaker', 'vault_breaker', 'p71/breaker')
    fn('p71/breaker', ['advancement revoke @s only bm:p71/breaker', 'execute if score @s bm.gvcd matches 1.. run return 0', 'scoreboard players set @s bm.gvcd 6',
                       'tag @s add bm.gvatk',
                       f'execute at @s as @e[{mob},distance=..6,nbt={{HurtTime:10s}},sort=nearest,limit=1] at @s run function bm:p71/quake', 'tag @s remove bm.gvatk'])
    fn('p71/quake', ['tag @s add bm.gvhit', f'execute as @e[{mob},distance=..3.5,tag=!bm.gvhit] run damage @s 4 minecraft:player_attack by @a[tag=bm.gvatk,limit=1]',
                     f'execute as @e[{mob},distance=..3.5,tag=!bm.gvhit,tag=!bm.boss,tag=!bm.vboss,tag=!bm.gvboss] at @s facing entity @e[tag=bm.gvhit,limit=1] feet rotated ~180 0 run tp @s ^ ^0.3 ^0.8',
                     'particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~0.2 ~ 1.5 0.1 1.5 0 30', 'particle minecraft:explosion ~ ~0.3 ~ 0 0 0 0 1',
                     'playsound minecraft:block.anvil.land player @a[distance=..16] ~ ~ ~ 0.6 0.8', 'tag @s remove bm.gvhit'])
    fast.append('scoreboard players remove @a[scores={bm.gvcd=1..}] bm.gvcd 1')
    # the crossbow: a coin burst round whatever the bolt hit
    melee_adv('sling', 'coinslinger', 'p71/sling', proj=True)
    fn('p71/sling', ['advancement revoke @s only bm:p71/sling', 'tag @s add bm.gvatk',
                     f'execute as @e[{mob},distance=..64,nbt={{HurtTime:10s}}] at @s run function bm:p71/burst', 'tag @s remove bm.gvatk'])
    fn('p71/burst', ['tag @s add bm.gvhit', f'execute as @e[{mob},distance=..3,tag=!bm.gvhit] run damage @s 4 minecraft:player_attack by @a[tag=bm.gvatk,limit=1]',
                     'particle minecraft:wax_on ~ ~1 ~ 1 0.5 1 0 25', 'particle minecraft:item{item:"minecraft:gold_nugget"} ~ ~1 ~ 0.6 0.4 0.6 0.15 20',
                     'playsound minecraft:entity.experience_orb.pickup player @a[distance=..16] ~ ~ ~ 1 0.6', 'tag @s remove bm.gvhit'])
    # the cutlass: bleeding; a coin from the slain now and then
    melee_adv('cutlass', 'gutter_cutlass', 'p71/cutlass')
    fn('p71/cutlass', ['advancement revoke @s only bm:p71/cutlass', f'execute at @s as @e[{mob},distance=..6,nbt={{HurtTime:10s}},sort=nearest,limit=1] at @s run function bm:p71/bleed'])
    fn('p71/bleed', ['effect give @s minecraft:wither 3 0', 'particle minecraft:dust{color:[0.6,0.0,0.0],scale:1} ~ ~1 ~ 0.3 0.4 0.3 0 8'])
    wjson('bm/advancement/p71/cutlass_kill.json', {'criteria': {'kill': {'trigger': 'minecraft:player_killed_entity', 'conditions': {
        'player': [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'equipment': {'mainhand': {'predicates': {'minecraft:custom_data': '{bm:"gutter_cutlass"}'}}}}}],
        'entity': [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:entity_type': '#bm:hostile'}}]}}}, 'rewards': {'function': 'bm:p71/cutlass_kill'}})
    fn('p71/cutlass_kill', ['advancement revoke @s only bm:p71/cutlass_kill', 'execute store result score #r bm.rng run random value 1..100',
                            'execute if score #r bm.rng matches ..15 run loot give @s loot bm:items/gutter_coin',
                            'execute if score #r bm.rng matches ..15 run playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.8 0.6'])
    # the scepter: COIN STORM
    fn('p71/scepter', ['execute if score @s bm.gvsc matches 1.. run return run ' + say('The scepter is still counting its coins.', GOLD),
                       'scoreboard players set @s bm.gvsc 20', 'tag @s add bm.gvatk',
                       f'execute as @e[{mob},distance=..6] at @s run function bm:p71/storm1', 'tag @s remove bm.gvatk',
                       'particle minecraft:wax_on ~ ~4 ~ 4 0.5 4 0 120', 'particle minecraft:item{item:"minecraft:gold_nugget"} ~ ~5 ~ 4 0.5 4 0 80',
                       'playsound minecraft:block.chain.break player @a[distance=..24] ~ ~ ~ 1 0.6', 'playsound minecraft:entity.experience_orb.pickup player @a[distance=..24] ~ ~ ~ 1 0.5',
                       say('COIN STORM!', GOLD)])
    G.FUNCS['p71/scepter'] = [l.replace('bm.gvsc matches 1..', 'bm.gvfl matches 1..').replace('set @s bm.gvsc 20', 'set @s bm.gvfl 20') for l in G.FUNCS['p71/scepter']]
    fn('p71/storm1', ['damage @s 12 minecraft:magic by @a[tag=bm.gvatk,limit=1]', 'effect give @s[tag=!bm.boss,tag=!bm.vboss,tag=!bm.gvboss] minecraft:levitation 1 4',
                      'particle minecraft:item{item:"minecraft:gold_ingot"} ~ ~2 ~ 0.3 1 0.3 0.1 10'])
    second.append('scoreboard players remove @a[scores={bm.gvfl=1..}] bm.gvfl 1')

    # ------------------------------------------------------------------ the Bond Sigil: near another sigil from the same heist - regeneration (and absorption now and then)
    second.append('execute as @a if items entity @s container.* ' + holds('bond_sigil') + ' run function bm:p71/bond_read')
    fn('p71/bond_read', ['execute store result score @s bm.bond run data get entity @s Inventory[{components:{"minecraft:custom_data":{bm:"bond_sigil"}}}].components."minecraft:custom_data".bond',
                         'tag @s add bm.gvbonded'])
    second.append('execute as @a[tag=bm.gvbonded] at @s run function bm:p71/bond')
    second.append('tag @a remove bm.gvbonded')
    fn('p71/bond', ['execute unless score @s bm.bond matches 1.. run return 0', 'scoreboard players operation #b bm.rng = @s bm.bond', 'tag @s add bm.gvself',
                    'scoreboard players set #near bm.rng 0',
                    'execute as @a[tag=bm.gvbonded,tag=!bm.gvself,distance=..16] if score @s bm.bond = #b bm.rng run scoreboard players set #near bm.rng 1',
                    'tag @s remove bm.gvself', 'execute if score #near bm.rng matches 0 run return 0',
                    'effect give @s minecraft:regeneration 3 0 true', 'execute store result score #r bm.rng run random value 1..20',
                    'execute if score #r bm.rng matches 1 run effect give @s minecraft:absorption 20 0 true',
                    'particle minecraft:heart ~ ~2.1 ~ 0.2 0.1 0.2 0 1'])

    # ------------------------------------------------------------------ placeables (banners and trophies): sneak + use on a block; sneak + punch to take back
    def placer(name, iid, spawn):
        fn(f'p71/{name}', ['execute unless predicate bm:p20/sneaking run return run ' + say('Sneak + use on a block to set it down.'),
                           'scoreboard players set #placed bm.rng 0', 'scoreboard players set #ray bm.rng 25', 'tag @s add bm.placer',
                           f'execute anchored eyes positioned ^ ^ ^ run function bm:p71/{name}_ray', 'tag @s remove bm.placer',
                           'execute if score #placed bm.rng matches 0 run return run ' + say('Look at the top of a block within 5 blocks.'), clear1(iid)])
        fn(f'p71/{name}_ray', [f'execute unless block ~ ~ ~ #minecraft:replaceable run return run function bm:p71/{name}_hit',
                               'scoreboard players remove #ray bm.rng 1', f'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p71/{name}_ray'])
        fn(f'p71/{name}_hit', ['execute align xyz positioned ~0.5 ~1 ~0.5 unless block ~ ~ ~ #minecraft:replaceable run return 0',
                               'execute align xyz positioned ~0.5 ~1 ~0.5 if entity @e[type=minecraft:interaction,tag=bm.gvdeco,distance=..0.6] run return 0',
                               f'execute align xyz positioned ~0.5 ~1 ~0.5 rotated as @a[tag=bm.placer,limit=1] rotated ~180 0 run function bm:p71/{spawn}',
                               'scoreboard players set #placed bm.rng 1'])
    def deco_nbt(it, tags, ty, sc, bill='fixed'):
        return snbt({'Tags': tags, 'item': G.stack(it) if it in ITEMS else {'id': it, 'count': Int(1)}, 'item_display': 'fixed', 'billboard': bill,
                     'transformation': {'left_rotation': [F(0)] * 3 + [F(1)], 'right_rotation': [F(0)] * 3 + [F(1)], 'translation': [F(0), F(ty), F(0)], 'scale': [F(sc)] * 3}})
    for k in KINDS:
        placer(f'deco/place_trophy_{k}', f'trophy_{k}', f'deco/spawn_trophy_{k}')
        fn(f'p71/deco/spawn_trophy_{k}', [f'summon minecraft:item_display ~ ~ ~ {deco_nbt(f"trophy_{k}", ["bm.gvdecod", "bm.gvdnew"], 0.45, 0.9)}',
                                          f'summon minecraft:interaction ~ ~ ~ {snbt({"Tags": ["bm.gvdeco", "bm.gvdnew", "bm.gvdk_trophy_" + k], "width": F(0.7), "height": F(0.9), "response": B(1)})}',
                                          'tp @e[tag=bm.gvdnew,distance=..0.5] ~ ~ ~ ~ 0', 'tag @e[tag=bm.gvdnew,distance=..0.5] remove bm.gvdnew',
                                          'playsound minecraft:block.metal.place block @a[distance=..16] ~ ~ ~ 1 1', 'particle minecraft:wax_on ~ ~0.5 ~ 0.3 0.3 0.3 0 10'])
    for t in range(1, 6):
        placer(f'banner/place{t}', f'raid_banner_{t}', f'banner/spawn{t}')
        fn(f'p71/banner/spawn{t}', [f'summon minecraft:item_display ~ ~ ~ {deco_nbt(f"raid_banner_{t}", ["bm.gvdecod", "bm.gvdnew", "bm.gvban"], 1.0, 1.4)}',
                                    f'summon minecraft:interaction ~ ~ ~ {snbt({"Tags": ["bm.gvdeco", "bm.gvdnew", "bm.gvdk_raid_banner_" + str(t), "bm.gvbanhit"], "width": F(0.8), "height": F(2.0), "response": B(1)})}',
                                    f'scoreboard players set @e[tag=bm.gvdnew,distance=..0.5] bm.vhs {t}',
                                    'execute unless score @a[tag=bm.placer,limit=1] bm.pid matches 1.. as @a[tag=bm.placer,limit=1] run function bm:p21/pid',
                                    'scoreboard players operation @e[tag=bm.gvdnew,distance=..0.5] bm.pid = @a[tag=bm.placer,limit=1] bm.pid',
                                    'scoreboard players set @e[tag=bm.gvdnew,distance=..0.5] bm.pty 0',
                                    'execute if score @a[tag=bm.placer,limit=1] bm.pty matches 1.. run scoreboard players operation @e[tag=bm.gvdnew,distance=..0.5] bm.pty = @a[tag=bm.placer,limit=1] bm.pty',
                                    'tp @e[tag=bm.gvdnew,distance=..0.5] ~ ~ ~ ~ 0', 'tag @e[tag=bm.gvdnew,distance=..0.5] remove bm.gvdnew',
                                    'playsound minecraft:block.wool.place block @a[distance=..16] ~ ~ ~ 1 0.8', 'particle minecraft:wax_on ~ ~1 ~ 0.3 0.6 0.3 0 16'])
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.gvdeco] if data entity @s attack at @s run function bm:p71/deco/punch')
    fn('p71/deco/punch', ['tag @s add bm.gvdme', 'execute on attacker if predicate bm:p20/sneaking run function bm:p71/deco/pick', 'tag @s remove bm.gvdme', 'data remove entity @s attack'])
    fn('p71/deco/pick', [f'execute if entity @e[type=minecraft:interaction,tag=bm.gvdme,tag=bm.gvdk_{i}] run loot give @s loot bm:items/{i}' for i in [f'trophy_{k}' for k in KINDS] + [f'raid_banner_{t}' for t in range(1, 6)]] +
       ['execute as @e[type=minecraft:interaction,tag=bm.gvdme] at @s run function bm:p71/deco/gone', 'playsound minecraft:entity.item.pickup player @s ~ ~ ~ 1 1'])
    fn('p71/deco/gone', ['kill @e[type=minecraft:item_display,tag=bm.gvdecod,distance=..0.6]', 'particle minecraft:poof ~ ~0.4 ~ 0.2 0.2 0.2 0.02 6', 'kill @s'])
    # the banner's aura: its party (or its owner) within 8 - regeneration and speed; III+ strength; V resistance
    second.append('execute as @e[type=minecraft:interaction,tag=bm.gvbanhit] at @s run function bm:p71/banner/aura')
    fn('p71/banner/aura', ['scoreboard players operation #p bm.rng = @s bm.pty', 'scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players operation #t bm.rng = @s bm.vhs',
                           'execute if score #p bm.rng matches 1.. as @a[distance=..8,gamemode=!spectator] if score @s bm.pty = #p bm.rng run tag @s add bm.gvaura',
                           'execute as @a[distance=..8,gamemode=!spectator] if score @s bm.pid = #me bm.pid run tag @s add bm.gvaura',
                           'effect give @a[tag=bm.gvaura] minecraft:regeneration 3 0 true', 'effect give @a[tag=bm.gvaura] minecraft:speed 3 0 true',
                           'execute if score #t bm.rng matches 3.. run effect give @a[tag=bm.gvaura] minecraft:strength 3 0 true',
                           'execute if score #t bm.rng matches 5 run effect give @a[tag=bm.gvaura] minecraft:resistance 3 0 true',
                           'particle minecraft:wax_on ~ ~2 ~ 0.4 0.4 0.4 0 3', 'tag @a[tag=bm.gvaura] remove bm.gvaura'])

    # ------------------------------------------------------------------ Clockwork: four fragments make a key; the key opens the den's copper door
    fn('p71/assemble', ['execute store result score #n bm.rng run clear @s ' + holds('clockwork_fragment') + ' 0',
                        'execute if score #n bm.rng matches ..3 run return run ' + say('Four fragments make a key - you have fewer.', '#d9a066'),
                        'clear @s ' + holds('clockwork_fragment') + ' 4', 'loot give @s loot bm:items/clockwork_key',
                        'playsound minecraft:block.copper_bulb.turn_on player @s ~ ~ ~ 1 0.8', 'playsound minecraft:block.chain.place player @s ~ ~ ~ 1 1.2',
                        say('Click, click, whirr - a Clockwork Key!', '#e8b070')])
    fn('p71/key', ['execute unless entity @s[tag=bm.gvp] run return run ' + say('It fits only one door: the copper one in the Fixer\'s Den.', '#e8b070'),
                   'scoreboard players set #ok bm.rng 0',
                   'execute as @e[type=marker,tag=bm.gvr_lobby,distance=..16,sort=nearest,limit=1] at @s positioned ' + RM.rel(12, 5, 0) + ' if entity @a[tag=bm.gvp,distance=..5] run scoreboard players set #ok bm.rng 1',
                   'execute if score #ok bm.rng matches 0 run return run ' + say('Stand by the copper door in the den.', '#e8b070'),
                   clear1('clockwork_key'),
                   'execute as @e[type=marker,tag=bm.gvr_lobby,distance=..16,sort=nearest,limit=1] at @s run fill ' + RM.rel(11, 4, 0) + ' ' + RM.rel(13, 6, 0) + ' minecraft:air replace minecraft:waxed_oxidized_copper',
                   'playsound minecraft:block.iron_door.open player @a[distance=..16] ~ ~ ~ 1 0.6', 'playsound minecraft:block.copper_bulb.turn_on player @a[distance=..16] ~ ~ ~ 1 0.6',
                   say('The clockwork door grinds open - the Clockwork Cache!', '#e8b070')])

    # ------------------------------------------------------------------ follower finery
    fn('p71/topper', ['execute unless score @s bm.pid matches 1.. run return run ' + say('Use it near your Cecil.'),
                      'scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #ok bm.rng 0',
                      'execute as @e[type=minecraft:wolf,tag=bm.cecilpet,distance=..8] if score @s bm.pid = #me bm.pid run scoreboard players set #ok bm.rng 1',
                      'execute if score #ok bm.rng matches 0 run return run ' + say('Use it near your Cecil.'),
                      'execute if score @s bm.cpgild matches 1 run return run ' + say('His staff is already gilded.', GOLD),
                      clear1('gilded_staff_topper'), 'scoreboard players set @s bm.cpgild 1',
                      'scoreboard players set #el bm.rng 0', 'execute if score @s bm.cpel matches 1.. run scoreboard players operation #el bm.rng = @s bm.cpel', 'function bm:p46/pet/dress',
                      'execute at @e[type=minecraft:wolf,tag=bm.cecilpet,distance=..8,sort=nearest,limit=1] run particle minecraft:wax_on ~ ~2 ~ 0.4 0.6 0.4 0 30',
                      'playsound minecraft:block.anvil.use player @a[distance=..12] ~ ~ ~ 0.6 1.6', say('Cecil admires his gilded staff. "Ooh. Fancy."', '#b48cff')])
    # (dress: the gilded staff, for its owner)
    import phase46 as P46
    import phase69 as P69
    d = P46.EL_KEYS
    G.FUNCS['p46/pet/dress'] += ['scoreboard players set #gild bm.rng 0', 'execute as @a if score @s bm.pid = #me bm.pid if score @s bm.cpgild matches 1 run scoreboard players set #gild bm.rng 1'] + \
        [f'execute if score #gild bm.rng matches 1 if score #el bm.rng matches {n} as @e[type=minecraft:item_display,tag=bm.cpet,tag=bm.cp_arm] if score @s bm.pid = #me bm.pid run data modify entity @s item.components."minecraft:item_model" set value "bm:cec2_arm{sfx}_gild"'
         for n, sfx in [(0, '')] + [(i + 1, f'_{k}') for i, k in enumerate(d)] + [(P69.ETH_I, '_ethereal')]]
    fn('p71/gspear', ['execute unless score @s bm.pid matches 1.. run return run ' + say('Use it near Celi.'), 'scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #ok bm.rng 0',
                      'execute as @e[type=minecraft:wolf,tag=bm.celipet,distance=..8] if score @s bm.pid = #me bm.pid run scoreboard players set #ok bm.rng 1',
                      'execute if score #ok bm.rng matches 0 run return run ' + say('Use it near Celi.'),
                      'execute if score @s bm.cegold matches 1 run return run ' + say('Her spear is already golden.', GOLD),
                      clear1('golden_spear'), 'scoreboard players set @s bm.cegold 1', 'function bm:p71/gspear_set',
                      'playsound minecraft:block.anvil.use player @a[distance=..12] ~ ~ ~ 0.6 1.6', say('Celi twirls the golden spear. "...Fine. It suits me."', '#bfe8ff')])
    fn('p71/gspear_set', ['execute as @e[type=minecraft:item_display,tag=bm.cp6_spear] if score @s bm.pid = #me bm.pid run data modify entity @s item.components."minecraft:item_model" set value "bm:ce_spear_gold"'])
    second.append('execute as @a[scores={bm.cegold=1}] run function bm:p71/gspear_keep')
    fn('p71/gspear_keep', ['scoreboard players operation #me bm.pid = @s bm.pid', 'function bm:p71/gspear_set',
                           'execute as @e[type=minecraft:item_display,tag=bm.cesp] if score @s bm.pid = #me bm.pid run data modify entity @s item.components."minecraft:item_model" set value "bm:ce_spear_gold"'])
    fn('p71/fmono', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #ok bm.rng 0',
                     'execute as @e[type=minecraft:wolf,tag=bm.frogpet,distance=..8] if score @s bm.pid = #me bm.pid run scoreboard players set #ok bm.rng 1',
                     'execute if score #ok bm.rng matches 0 run return run ' + say('Use it near the Frog with Mustache.'),
                     'execute if score @s bm.frmono matches 1 run return run ' + say('He already wears one.', GOLD),
                     clear1('frog_monocle'), 'scoreboard players set @s bm.frmono 1',
                     'execute as @e[type=minecraft:wolf,tag=bm.frogpet,distance=..8] if score @s bm.pid = #me bm.pid run function bm:p63/frog/headmodel',
                     say('"Ribbit. Most distinguished." The Frog adjusts his monocle.', 'green')])
    hm = G.FUNCS['p63/frog/headmodel']
    hm.insert(0, 'scoreboard players set #mono bm.rng 0')
    hm.insert(1, 'execute on owner if score @s bm.frmono matches 1 run scoreboard players set #mono bm.rng 1')
    hm.append('execute if score #mono bm.rng matches 1 on passengers if entity @s[tag=bm.frr_head] run function bm:p71/frog_mono')
    fn('p71/frog_mono', ['data modify storage bm:tmp fm.m set from entity @s item.components."minecraft:item_model"', 'function bm:p71/frog_mono2 with storage bm:tmp fm'])
    fn('p71/frog_mono2', ['$data modify entity @s item.components."minecraft:item_model" set value "$(m)_mono"'])

    # ------------------------------------------------------------------ the Vault Hound
    hound = {'Tags': ['bm.vhound', 'bm.vhnew', 'bm.seen'], 'PersistenceRequired': B(1), 'CustomName': T('Vault Hound', GOLD, bold=True), 'CollarColor': B(4),
             'attributes': [{'id': 'minecraft:max_health', 'base': D(40)}, {'id': 'minecraft:movement_speed', 'base': D(0.34)}, {'id': 'minecraft:attack_damage', 'base': D(5)}],
             'Health': F(40), 'variant': 'minecraft:ashen', 'equipment': {'body': {'id': 'minecraft:wolf_armor', 'count': Int(1), 'components': {'minecraft:dyed_color': 0xffc832}}}}
    sel_h = 'execute as @e[type=minecraft:wolf,tag=bm.vhound] if score @s bm.pid = #me bm.pid'
    fn('p71/hound/use', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                         f'{sel_h} run tag @s add bm.vhsel',
                         'execute if entity @e[tag=bm.vhsel] if predicate bm:p20/sneaking run function bm:p71/hound/home',
                         'execute if entity @e[tag=bm.vhsel] unless predicate bm:p20/sneaking run function bm:p71/hound/recall',
                         'execute unless entity @e[tag=bm.vhsel] unless predicate bm:p20/sneaking run function bm:p71/hound/call',
                         'tag @e[tag=bm.vhsel] remove bm.vhsel'])
    fn('p71/hound/call', [f'summon minecraft:wolf ^ ^ ^1.2 {snbt(hound)}', 'data modify entity @e[type=minecraft:wolf,tag=bm.vhnew,limit=1,sort=nearest] Owner set from entity @s UUID',
                          'scoreboard players operation @e[type=minecraft:wolf,tag=bm.vhnew,limit=1,sort=nearest] bm.pid = @s bm.pid', 'tag @e[tag=bm.vhnew] remove bm.vhnew',
                          'playsound minecraft:entity.wolf.ambient neutral @a[distance=..16] ~ ~ ~ 1 1', say('*a gold-collared hound bounds up, nose to the ground*', GOLD)])
    fn('p71/hound/recall', ['tp @e[tag=bm.vhsel,limit=1] @s', 'data modify entity @e[tag=bm.vhsel,limit=1] Sitting set value 0b'])
    fn('p71/hound/home', ['execute as @e[tag=bm.vhsel] at @s run particle minecraft:poof ~ ~0.5 ~ 0.3 0.3 0.3 0.02 10', 'tp @e[tag=bm.vhsel] ~ -500 ~', 'kill @e[tag=bm.vhsel]',
                          say('The Vault Hound trots off home.', GOLD)])
    # the nose: each tick it sniffs one slice of the 25 x 7 x 25 block box round it for an unopened loot chest
    tick.append('execute as @e[type=minecraft:wolf,tag=bm.vhound] at @s run function bm:p71/hound/sniff')
    fn('p71/hound/sniff', ['scoreboard players add @s bm.vhs 1', 'execute if score @s bm.vhs matches 25.. run scoreboard players set @s bm.vhs 0',
                           'execute if entity @s[tag=bm.vhfound] run return run function bm:p71/hound/point'] +
       [f'execute if score @s bm.vhs matches {i} run function bm:p71/hound/slice{i}' for i in range(25)])
    for i in range(25):
        dx = i - 12
        fn(f'p71/hound/slice{i}', [f'execute positioned ~{dx} ~{dy} ~{dz} if data block ~ ~ ~ LootTable run return run function bm:p71/hound/found' for dz in range(-12, 13) for dy in range(-3, 4)])
    fn('p71/hound/found', ['execute unless entity @e[type=minecraft:marker,tag=bm.vhmark,distance=..0.9] run summon minecraft:marker ~ ~ ~ {Tags:["bm.vhmark"]}', 'tag @s add bm.vhfound',
                           'scoreboard players set @s bm.gvx 100'])
    fn('p71/hound/point', ['scoreboard players remove @s bm.gvx 1', 'execute unless entity @e[type=minecraft:marker,tag=bm.vhmark,distance=..20] run return run function bm:p71/hound/lost',
                           'execute if score @s bm.gvx matches ..0 run return run function bm:p71/hound/lost',
                           'scoreboard players operation #q bm.rng = @s bm.gvx', 'scoreboard players operation #q bm.rng %= #20 bm.rng',
                           'execute if score #q bm.rng matches 0 run playsound minecraft:entity.wolf.ambient neutral @a[distance=..16] ~ ~ ~ 1 1.2',
                           'execute if score #q bm.rng matches 0 facing entity @e[type=minecraft:marker,tag=bm.vhmark,distance=..20,sort=nearest,limit=1] feet run function bm:p71/hound/trail',
                           'execute if score #q bm.rng matches 0 at @e[type=minecraft:marker,tag=bm.vhmark,distance=..20,sort=nearest,limit=1] run particle minecraft:wax_on ~0.5 ~1 ~0.5 0.3 0.3 0.3 0 12',
                           'execute if score #q bm.rng matches 0 on owner run ' + title('@s', 'actionbar', T('The Vault Hound smells treasure - follow the gold!', GOLD))])
    fn('p71/hound/trail', [f'particle minecraft:dust{{color:[1.0,0.85,0.2],scale:0.9}} ^ ^0.6 ^{d * 0.6:.1f} 0 0 0 0 1' for d in range(1, 20)])
    fn('p71/hound/lost', ['tag @s remove bm.vhfound', 'kill @e[type=minecraft:marker,tag=bm.vhmark,distance=..30,sort=nearest,limit=1]', 'scoreboard players set @s bm.vhs 0'])
    # (a found chest that's been opened since: forget it)
    second.append('execute as @e[type=minecraft:marker,tag=bm.vhmark] at @s unless data block ~ ~ ~ LootTable run kill @s')

    # ------------------------------------------------------------------ the Gutter Laurel; the nights' prizes
    second.append('execute as @a if items entity @s container.* ' + holds('gutter_laurel') + ' at @s run function bm:p71/laurel')
    import math
    fn('p71/laurel', [f'particle minecraft:dust{{color:[1.0,0.82,0.25],scale:0.6}} ~{0.32 * math.cos(a * math.pi / 6):.2f} ~2.15 ~{0.32 * math.sin(a * math.pi / 6):.2f} 0 0 0 0 1' for a in range(12)] +
       ['particle minecraft:wax_on ~ ~2.3 ~ 0.15 0.05 0.15 0 1'])
    wjson('bm/advancement/p71/ledger.json', {'criteria': {'kill': {'trigger': 'minecraft:player_killed_entity', 'conditions': {
        'entity': [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:entity_type': '#bm:hostile'}}]}}}, 'rewards': {'function': 'bm:p71/ledger'}})
    fn('p71/ledger', ['advancement revoke @s only bm:p71/ledger', 'execute unless items entity @s container.* ' + holds('crimson_ledger') + ' run return 0',
                      'effect give @s minecraft:instant_health 1 0 true', 'particle minecraft:dust{color:[0.8,0.0,0.0],scale:1} ~ ~1 ~ 0.3 0.5 0.3 0 10'])
    G.FUNCS['p71/ledger'][2] = 'execute unless items entity @s container.* ' + holds('crimson_ledger') + ' unless items entity @s weapon.offhand ' + holds('crimson_ledger') + ' run return 0'
    G.FUNCS['p71/ledger'].insert(3, 'execute store result score #h bm.rng run data get entity @s Health')
    G.FUNCS['p71/ledger'][-2] = 'execute if score #h bm.rng matches ..18 run effect give @s minecraft:regeneration 2 2 true'
    fn('p71/flip', ['execute if score @s bm.gvsc matches 1.. run return run ' + say('The coin needs a rest.', '#7dff6a'), 'scoreboard players set @s bm.gvsc 300',
                    'execute store result score #r bm.rng run random value 0..1', 'playsound minecraft:block.chain.hit player @a[distance=..12] ~ ~ ~ 1 2',
                    'execute if score #r bm.rng matches 1 run effect give @s minecraft:luck 120 1', 'execute if score #r bm.rng matches 1 run ' + say('Heads! Luck II for two minutes.', '#7dff6a'),
                    'execute if score #r bm.rng matches 0 run ' + say('Tails. Better luck next time.', 'gray')])
    second.append('scoreboard players remove @a[scores={bm.gvsc=1..}] bm.gvsc 1')

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    f[-1:-1] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


# ===================================================================== resource pack
def rp(R):
    import sys, copy
    from PIL import Image, ImageDraw
    VAN = '/home/claude/mc263/client/assets/minecraft/textures'
    hexc = R.hexc
    def tint(path, mul, accent=None):
        im = Image.open(path).convert('RGBA'); px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                r, g, b, a = px[x, y]
                if not a: continue
                lum = (r + g + b) / 3
                if lum < 90:                         # the dark edges: blackstone
                    px[x, y] = (34, 28, 30, a)
                else:
                    px[x, y] = (min(255, int(r * mul[0])), min(255, int(g * mul[1])), min(255, int(b * mul[2])), a)
        if accent:
            for (x, y) in accent:
                if x < im.width and y < im.height and px[x, y][3]: px[x, y] = (200, 30, 60, 255)
        return im
    G2 = sys.modules['gen_rp'] if 'gen_rp' in sys.modules else R
    # icons
    for p, _s, _a, _n in GILD:
        R.ICONS[f'gilded_{p}'] = tint(f'{VAN}/item/golden_{p}.png', (1.05, 0.95, 0.6), [(7, 4), (8, 4)])
    g = lambda rows, pal: R.grid(rows, pal)
    GP = dict(Y='#ffd84a', y='#c8961e', o='#8a5a10', k='#2a1e10', w='#fff2b0', r='#d83a4a', b='#5a7ad8', g='#7dff6a', s='#c8c8d8', d='#6a6a7a', c='#d9a066', e='#e8b070',
              p='#ff9ad8', a='#a8e0ff', v='#b6ff3c', R='#ff3030', W='#ffffff', n='#5a3e28')
    R.ICONS['gutter_coin'] = g(['................', '.....oooooo.....', '...ooYYYYYYoo...', '..oYYwwYYYYYYo..', '..oYwYYkYYkYYo..', '.oYYYYkkkkYYYYo.',
                                '.oYYYkYkkYkYYyo.', '.oYYYkkkkkkYYyo.', '.oYYYYkYYkYYYyo.', '.oYYYYYkkYYYyyo.', '..oYYYYYYYYyyo..', '..oyYYYYYYyyyo..',
                                '...ooyyyyyyoo...', '.....oooooo.....', '................', '................'], GP)
    R.ICONS['smoke_bomb'] = g(['................', '.......dd.......', '......d.d.......', '.......kk.......', '.....dddddd.....', '....dssssssd....', '...dsswsssssd...',
                              '...dswssssssd...', '...dssssssssd...', '...dssssssssd...', '....dssssssd....', '.....dddddd.....', '................', '................', '................', '................'], GP)
    R.ICONS['skeleton_lockpick'] = g(['................', '............ww..', '...........wsw..', '..........wsw...', '.........wsw....', '........wsw.....', '.......wsw......',
                                      '......wsw.......', '.....wsw........', '....wsw.........', '...wwsw.........', '..ws.ww.........', '..wsw...........', '...w............', '................', '................'], GP)
    R.ICONS['cipher_monocle'] = g(['................', '................', '.....yyyyyy.....', '....y.aaaa.y....', '...y.aawaaa.y...', '...y.awaaaa.y...', '...y.aaaaaa.y...',
                                   '...y.aaaaaa.y...', '....y.aaaa.y....', '.....yyyyyy.....', '........y.......', '.........y......', '..........y.....', '...........y....', '................', '................'], GP)
    R.ICONS['heisters_shiv'] = g(['................', '................', '................', '............ws..', '...........wss..', '..........wss...', '.........wss....',
                                  '........wss.....', '.......wss......', '....y.wss.......', '.....yss........', '.....oy.........', '....oo.y........', '...oo...........', '..oo............', '................'], GP)
    R.ICONS['vault_breaker'] = g(['................', '.........yyyy...', '........yddddy..', '.......yddddddy.', '.......yddyddy..', '........ydddy...', '.......oyyyy....',
                                  '......oo........', '.....oo.........', '....oo..........', '...oo...........', '..yo............', '.yo.............', '................', '................', '................'], GP)
    R.ICONS['gutter_cutlass'] = g(['................', '..............w.', '.............ws.', '............wss.', '...........wss..', '..........wss...', '.........wss....',
                                   '........wss.....', '.......wss......', '..yy..wss.......', '..y.yss.........', '...yyy..........', '..oyy...........', '.oo.............', 'oo..............', '................'], GP)
    R.ICONS['treasurers_scepter'] = g(['................', '..........rYr...', '.........YwYY...', '........yYYYYy..', '.........yYYy...', '........oyyy....', '.......oo.......',
                                       '......oo........', '.....oo.........', '....oo..........', '...yo...........', '..oo............', '.oo.............', '................', '................', '................'], GP)
    R.ICONS['bond_sigil'] = g(['................', '......yyyy......', '....yyppppyy....', '...ypppwppppy...', '..ypppppppppy...', '..yppYYppYYpy...', '..ypYYYYYYYpy...',
                               '..yppYYYYYppy...', '..ypppYYYpppy...', '...yppppYpppy...', '....yyppppyy....', '......yyyy......', '................', '................', '................', '................'], GP)
    R.ICONS['clockwork_fragment'] = g(['................', '................', '......cc........', '.....cecc.......', '....ceeecc......', '...cceeeec......', '....ccekcc......',
                                       '.....ccecc......', '......cec.......', '.......cc.......', '................', '................', '................', '................', '................', '................'], GP)
    R.ICONS['clockwork_key'] = g(['................', '...cccc.........', '..ceeeec........', '..cekkec........', '..cekkec........', '..ceeeec........', '...cccccc.......',
                                  '........cc......', '.........cc.....', '..........cc....', '...........ccc..', '..........c.cc..', '...........cc...', '................', '................', '................'], GP)
    trophy = ['................', '...yyyyyyyyyy...', '..yYYYYYYYYYYy..', '..yYwYYYYYYYYy..', '..yYYYYYYYYYYy..', '...yYYYYYYYYy...', '....yYYYYYYy....',
              '.....yYYYYy.....', '.......yy.......', '.......yy.......', '.....yyyyyy.....', '....kkkkkkkk....', '....kYYYYYYk....', '....kkkkkkkk....', '................', '................']
    SYMBOL = {'levers': [(7, 3), (8, 4), (9, 3)], 'plates': [(6, 4), (7, 4), (8, 4), (9, 4)], 'lasers': [(5, 3), (7, 3), (9, 3), (11, 3)], 'tiles': [(6, 3), (8, 3), (7, 4), (9, 4)],
              'dial': [(7, 2), (8, 3), (8, 4)], 'guards': [(7, 3), (8, 3), (7, 4)], 'coffers': [(6, 3), (7, 3), (8, 3), (7, 4)]}
    for k in KINDS:
        im = g(trophy, GP)
        for (x, y) in SYMBOL[k]: im.putpixel((x, y), hexc('#8a2a10'))
        R.ICONS[f'trophy_{k}'] = im
    R.ICONS['gilded_staff_topper'] = g(['................', '................', '...y........y...', '...yy......yy...', '....yy....yy....', '.....yyrryy.....', '......yrry......',
                                        '.......yy.......', '.......yy.......', '......yyyy......', '................', '................', '................', '................', '................', '................'], GP)
    R.ICONS['golden_spear'] = g(['................', '.............a..', '............aWa.', '...........aWa..', '..........aYa...', '.........yYy....', '........oy......',
                                 '.......oo.......', '......oo........', '.....oo.........', '....oo..........', '...oo...........', '..oo............', '................', '................', '................'], GP)
    R.ICONS['frog_monocle'] = g(['................', '................', '................', '.....yyyy.......', '....y.aa.y......', '....yaWaay......', '....yaaaay......',
                                 '....y.aa.y......', '.....yyyy.......', '........y.......', '.........y......', '..........y.....', '...........y....', '................', '................', '................'], GP)
    R.ICONS['vault_hound_whistle'] = g(['................', '................', '..........yy....', '.........y..y...', '........y....y..', '.......y.....y..', '.yyyyyyy.....y..',
                                        'yYYYYYYYYy..y...', 'yYwYYYkYYyyy....', 'yYYYYYYYYy......', '.yyyyyyyy.......', '................', '................', '................', '................', '................'], GP)
    R.ICONS['gutter_laurel'] = g(['................', '................', '...g........g...', '..gYg......gYg..', '..gYYg....gYYg..', '...gYYgyygYYg...', '....gYYYYYYg....',
                                  '.....gYYYYg.....', '......yyyy......', '................', '................', '................', '................', '................', '................', '................'],
                                 dict(GP, g='#c8961e'))
    R.ICONS['crimson_ledger'] = g(['................', '..kkkkkkkkkkk...', '..kRRRRRRRRRRk..', '..kRyRRRRRRRRk..', '..kRyRRwwwwRRk..', '..kRyRRRRRRRRk..', '..kRyRRwwwRRRk..',
                                   '..kRyRRRRRRRRk..', '..kRyRRRRRRRRk..', '..kRyRRRRRRRRk..', '..kRRRRRRRRRRk..', '..kkkkkkkkkkkk..', '................', '................', '................', '................'], GP)
    R.ICONS['gamblers_coin'] = g(['................', '.....oooooo.....', '...ooggggggoo...', '..oggwwggggggo..', '..ogwgg7gggggo..', '.oggggggggggggo.', '.ogggg777ggggyo.',
                                  '.oggggggggggggo.', '.oggg7ggg7gggyo.', '.ogggggggggggyo.', '..oggggggggggo..', '..oyggggggggyo..', '...ooyyyyyyoo...', '.....oooooo.....', '................', '................'],
                                 dict(GP, g='#5ad84a', **{'7': '#ffffff'}))
    R.ICONS['vorn_cracking_rig'] = g(['................', '................', '...kkkkkkkkkk...', '..kddddddddddk..', '..kdvvvvvvvvdk..', '..kdvkvvkvvvdk..', '..kdvvvvvvvvdk..',
                                      '..kddddddddddk..', '..kdgdgdgdgddk..', '..kddddddddddk..', '...kkkkkkkkkk...', '.....v....v.....', '.....v....v.....', '................', '................', '................'], GP)
    R.HANDHELD_EXTRA |= {'heisters_shiv', 'vault_breaker', 'gutter_cutlass', 'treasurers_scepter', 'skeleton_lockpick', 'golden_spear'}

    # the Cipher Monocle on the head: a gold-rimmed lens over the right eye, a chain to the ear
    gold, lens = 'minecraft:block/gold_block', 'minecraft:block/light_blue_stained_glass'
    c = R.cube
    R.HATS['cipher_monocle_head'] = ({'g': gold, 'l': lens}, [c((9.4, 7.0, 1.0), (12.9, 7.4, 1.4), 'g'), c((9.4, 10.4, 1.0), (12.9, 10.8, 1.4), 'g'),
                                                             c((9.4, 7.4, 1.0), (9.8, 10.4, 1.4), 'g'), c((12.5, 7.4, 1.0), (12.9, 10.4, 1.4), 'g'),
                                                             c((9.8, 7.4, 1.15), (12.5, 10.4, 1.25), 'l'), c((12.7, 4.6, 1.2), (13.0, 7.0, 1.5), 'g')])
    # item definitions: the monocle - an icon in the inventory, the lens on the head
    def post(R2):
        R2.wj('assets/bm/items/cipher_monocle.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:display_context',
                                                                 'cases': [{'when': 'head', 'model': {'type': 'minecraft:model', 'model': 'bm:item/cipher_monocle_head'}}],
                                                                 'fallback': {'type': 'minecraft:model', 'model': 'bm:item/cipher_monocle'}}})
        # the Gilded armour on the body: vanilla gold, darkened with blackstone, a ruby at the brow
        for layer in ('humanoid', 'humanoid_leggings'):
            im = tint(f'{VAN}/entity/equipment/{layer}/gold.png', (1.05, 0.92, 0.55), [(11, 10), (12, 10)] if layer == 'humanoid' else None)
            out = R2.p('assets', 'bm', 'textures', 'entity', 'equipment', layer, 'gilded.png'); im.save(out)
        R2.wj('assets/bm/equipment/gilded.json', {'layers': {'humanoid': [{'texture': 'bm:gilded'}], 'humanoid_leggings': [{'texture': 'bm:gilded'}]}})
    R.POST.append(post)
    # Cecil's gilded staff (every element): the crescent and collar in bright gilt with a ruby glint
    import phase46 as P46
    gl = Image.new('RGBA', (16, 16), hexc('#ffd84a'))
    for y in range(16):
        for x in range(16):
            if (x * 3 + y) % 7 == 0: gl.putpixel((x, y), hexc('#fff6c0'))
            elif (x + y * 5) % 11 == 0: gl.putpixel((x, y), hexc('#c8961e'))
    gl.putpixel((7, 7), hexc('#e0304a')); gl.putpixel((8, 8), hexc('#e0304a'))
    GTEX['cec_gilded'] = gl
    R.TEXTURE_MODS.append(sys.modules[__name__])
    for nm in ['cec2_arm'] + [f'cec2_arm_{k}' for k in P46.EL_KEYS] + ['cec2_arm_ethereal']:
        ct, els = R.HATS[nm]
        R.HATS[nm + '_gild'] = (dict(ct, g='bm:block/cec_gilded'), els)
    # Celi's golden spear: gold shaft, diamond head
    ct, els = R.HATS['ce_spear']
    R.HATS['ce_spear_gold'] = ({k: ('minecraft:block/gold_block' if k in ('ce_steel', 'ce_band', 'ce_star') else 'minecraft:block/diamond_block' if k == 'ce_ice' else v)
                                for k, v in ct.items()}, els)
    # the Frog's monocle: every head (each helm, blinking or not) also comes with one
    def frog_post(R2):
        import phase63 as P63
        import gen_rp as G3
        fr = P63.frog_rig()
        head = fr.parts['head'][2]
        blink = [cc for i, cc in enumerate(head) if i not in (5, 6)] + [G3.cube((3.45, 9.05, 4.85), (6.55, 11.45, 4.95), 'e'), G3.cube((9.45, 9.05, 4.85), (12.55, 11.45, 4.95), 'e')]
        mono = [G3.cube((9.1, 8.7, 4.6), (12.9, 9.05, 4.8), 'm'), G3.cube((9.1, 11.45, 4.6), (12.9, 11.8, 4.8), 'm'), G3.cube((9.1, 9.05, 4.6), (9.45, 11.45, 4.8), 'm'),
                G3.cube((12.55, 9.05, 4.6), (12.9, 11.45, 4.8), 'm'), G3.cube((12.7, 6.5, 4.7), (12.9, 8.7, 4.9), 'm')]
        def model(name, tex, els):
            t = dict(tex); t['particle'] = list(t.values())[0]
            R2.wj(f'assets/bm/models/item/{name}.json', {'textures': t, 'elements': els, 'display': {'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]}}})
            R2.wj(f'assets/bm/items/{name}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/{name}'}})
        for m in ['none'] + list(G3.HELM_TEX):
            t = dict(G3.FROG_TEX, h=G3.HELM_TEX.get(m, 'minecraft:block/iron_block'), m='minecraft:block/gold_block')
            model(f'frr_head_{m}_mono', t, fr.shifted('head', head + G3.frog_helm(m, 0, 0) + mono))
            model(f'frr_head_{m}_blink_mono', t, fr.shifted('head', blink + G3.frog_helm(m, 0, 0) + mono))
    R.POST.append(frog_post)


GTEX = {}


def textures():
    return dict(GTEX)

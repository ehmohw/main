"""2.84a (part two): VESPER, THE DREAD BROKER - hard mode's trader, in the Fountain Plaza's red-and-white stall, and DREAD TOKENS.

DREAD TOKENS   5 Black Market Trophies make one, and one breaks back into 5 (Vesper, or the Banker's Card's Exchange page
               once the world has turned). The Rat Bank keeps them like any currency - savings pay 2% a day (1 per 50
               kept), never more than 2 a day. Dread mobs never drop them.
VESPER         stands in the stall only while hard mode is on. Right-click him to trade; the black book on his counter
               (VESPER'S LEDGER) opens his services. What he deals in:
  THE LEDGER   FOLLOWERS' WARDS   Ward I-III (+3 armour, +1 toughness a level) and Vigor I-III (+10% health a level) on every
                                  follower you call - at home and on a heist - and Swift Return I-II (a faint rests 80 s,
                                  then 45 s, instead of 2 minutes).
               TUNING             the weapon, tool or armour piece in your hand takes a tuning of your choice - damage,
                                  swing speed, reach, luck; mining speed and efficiency; armour, toughness, health,
                                  knockback resistance, speed (boots) - a Dread Token a level, 2 levels of any one kind
                                  and 4 in all on any item (3 of damage or speed). Unbind it all for every token back.
               REFORGING          past the old maximum: hold a piece of Hero of Time, Juggernaut III, Shadowstep III,
                                  Architect III, Tidecaller III, Crimson Revenant or Vampire Lord armour, a Biggoron's
                                  Sword, Kong Krusher, Giga Koopa's Greataxe, Bow of Light or Ultra Hammer - or any
                                  Shifting weapon, tool or armour - and he reforges it into its dread-forged successor
                                  (the old set's own power stays; the new adds its own).
  HIS STOCK    conversions; a Sealed Map to the Omega Palace; the Auctioneer's Writ (a Dark Auction tonight); the Serpent's
               Summons (Apophiss's next defeat surely leaves his crown AND mace); the Echo of the Hollow King (fight him
               again - his vault opens to you again); the long work: the Tome of Eternity, the Mender's Altar, the Dread
               Lantern, the Harvest Scythe, the Bottomless Bucket, the Dawnbreaker Hourglass; the Dread Compass; and two
               dread cosmetics.
"""
import math
from items import item, gear, attr, ench, T, TOTEM, ITEMS, ARMOR_SLOT, consumable, armor_attrs, weapon_attrs, hat, trail, COSMETICS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int
import items as I
import mgeo
import market3
import phase15 as P15
import phase62 as P62

DREAD = '#b0102a'
DREAD_D = '#5a0812'
BONE = '#d8c8b0'
VESPER_POS = (53.5, market3.W, 51.5)            # behind the counter of the red-and-white stall on the Fountain Plaza's ring (its east side), facing south
LEDGER_POS = (52.5, market3.W + 1.0, 52.5)      # his book, on the counter's left barrel
LANTERN_POS = (53.5, market3.W + 1.0, 52.5)     # the counter's lantern (a soul lantern while he's there)
for _p, _w in ((VESPER_POS, 'Vesper'), ((53.5, market3.W, 53.5), "Vesper's customers")): mgeo.need_air(_p, _w)
MENU = 3200                                     # (his block: 3200-3299)
TPD = 5                                         # Trophies to a Dread Token

# ================================================================== the currency
I.ITEM_SYMBOL['dread_token'] = '☠'
item('dread_token', TOTEM, 'Dread Token', DREAD,
     ['Cold to the touch, and heavier than it looks.', (f'{TPD} Black Market Trophies make one - and it', 'blue'),
      ('breaks back into them, at Vesper or the Rat Bank.', 'blue'), ('Hard mode currency. The bank keeps it.', 'dark_gray')],
     model='bm:dread_token', stack=16, cat='currency', glint=True)
import phase31 as _P31
_P31.BANK.append(('dread_token', 'bm.bk_dread', 'Dread Tokens', DREAD))
_P31.SAVE_CAP['dread_token'] = 2
_P31.SAVE_PER_OF['dread_token'] = 50
_P31.XS_EXTRA += [('bm.bk_tro', TPD, 'bm.bk_dread', 1, f'{TPD} Trophies', '1 Dread Token', 4080, '#ffb300', DREAD, 'execute unless score #hard bm.cfg matches 1'),
                  ('bm.bk_dread', 1, 'bm.bk_tro', TPD, '1 Dread Token', f'{TPD} Trophies', 4081, DREAD, '#ffb300', None)]

# ================================================================== his goods
item('sealed_map_omega', TOTEM, 'Sealed Palace Map', '#9fb4ff',
     ['Hold right-click to break the seal.', 'Marks the nearest Omega Palace,', 'where a king of the dead keeps court.'],
     model='minecraft:map', glint=True, stack=16, comps={'minecraft:consumable': consumable(0.8, 'none', 'minecraft:item.book.page_turn', False)}, cat='map')
item('auction_writ', TOTEM, "Auctioneer's Writ", '#ffcf40',
     ['A summons the Auctioneer cannot refuse.', ('Hold right-click: a Dark Auction opens', 'blue'), ('at dusk tonight (one a day).', 'blue')],
     model='bm:auction_writ', stack=8, comps={'minecraft:consumable': consumable(1.2, 'bow', 'minecraft:item.book.page_turn', False)}, cat='misc')
item('serpent_summons', TOTEM, "Serpent's Summons", '#3ad06a',
     ['A green-black scale on a silver chain.', ('Hold right-click: the next time you beat', 'blue'),
      ('Apophiss, his True Crown AND his Mace are yours.', 'blue'), ('(One use. Kept until that fight.)', 'dark_gray')],
     model='bm:serpent_summons', stack=1, comps={'minecraft:consumable': consumable(1.6, 'bow', 'minecraft:entity.evoker.prepare_summon', False)}, cat='misc')
item('hollow_echo', TOTEM, 'Echo of the Hollow King', '#9a5ae0',
     ['A crown-shaped hollow in the air.', ('Hold right-click: the Hollow Throne wakes for', 'blue'),
      ('you again - beat its King once more, and', 'blue'), ('his first victory pays again (the Regalia).', 'blue')],
     model='bm:hollow_echo', stack=1, comps={'minecraft:consumable': consumable(1.6, 'bow', 'minecraft:entity.wither.ambient', False)}, cat='misc')
# the long work: functional, slow to save for, nothing like them anywhere else
item('tome_eternity', TOTEM, 'Tome of Eternity', '#e8d8a0',
     ['Every page reads: "and it endured."', ('Hold the item to bless in your OFF hand,', 'blue'),
      ('then hold right-click with the tome: it never', 'blue'), ('breaks again (Unbreakable). One use.', 'blue')],
     model='bm:tome_eternity', stack=1, glint=True, comps={'minecraft:consumable': consumable(2.0, 'bow', 'minecraft:block.enchantment_table.use', False)}, cat='book')
item('menders_altar', TOTEM, "Mender's Altar", '#7ad8b0',
     ['A little stone altar that hums like a hearth.', ('Sneak + use on a block: set it down.', 'blue'),
      ('Within 5 blocks, your armour and the tools in', 'blue'), ('your hands slowly mend.', 'blue'), ('Punch it: pick it up.', 'gray')],
     model='bm:menders_altar', stack=1, comps=hold('none'), cat='builder')
item('dread_lantern', TOTEM, 'Dread Lantern', DREAD,
     ['A lantern lit with something that frightens', 'the frightening.', ('Sneak + use on a block: set it down.', 'blue'),
      ('No monster rises within 48 blocks of it.', 'blue'), ('Punch it: pick it up.', 'gray')],
     model='bm:dread_lantern', stack=1, comps=hold('none'), cat='builder')
item('harvest_scythe', 'minecraft:netherite_hoe', 'Harvest Scythe', '#d8b040',
     ['Bends the whole field at once.', ('Right-click among your crops: every ripe one', 'blue'),
      ('within 3 blocks is reaped - and replanted.', 'blue')],
     comps=dict(hold('none'), **{'minecraft:unbreakable': {}, 'minecraft:enchantments': {'minecraft:efficiency': 5, 'minecraft:fortune': 3}}), cat='builder')
item('bottomless_bucket', 'minecraft:water_bucket', 'Bottomless Bucket', '#5ac8ff',
     ['There is always a little more.', ('Pour it out - it fills itself again.', 'blue')], glint=True, stack=1, cat='builder')
item('dawn_hourglass', TOTEM, 'Dawnbreaker Hourglass', '#ffd27a',
     ['The sand runs up.', ('Hold right-click at night: the sun rises', 'blue'), ('for everyone. Once every 3 days; never on a', 'blue'),
      ('Blood Moon, an invasion or any special night.', 'blue')],
     model='bm:dawn_hourglass', stack=1, comps={'minecraft:consumable': consumable(2.0, 'bow', 'minecraft:block.beacon.activate', False)}, cat='builder')
item('dread_compass', TOTEM, 'Dread Compass', DREAD,
     ['Its needle shivers toward the worst thing near.', ('Hold it: which way the nearest Dread', 'blue'), ('monster is, and how far (160 blocks).', 'blue')],
     model='bm:dread_compass', stack=1, cat='builder')
# dread cosmetics (the hat and boots tables: items.hat / items.trail)
hat('dread_halo', 'Halo of Thorns', DREAD, 'bm:halo', 'minecraft:dust{color:[0.55,0.02,0.08],scale:0.9} ~ ~2.3 ~ 0.25 0.03 0.25 0 2', None,
    ['A ring of black thorns that bleeds light.'])
trail('dread_boots', "Dreadwalker's Boots", DREAD, 0x2a0a0e, 'minecraft:soul_fire_flame ~ ~0.1 ~ 0.15 0 0.15 0.01 1', None, ['Every step a little cold.'])

STOCK = [  # (iid, n, price in Dread Tokens)
    ('sealed_map_omega', 1, 1), ('auction_writ', 1, 2), ('dread_compass', 1, 1), ('dread_halo', 1, 2), ('dread_boots', 1, 2),
    ('serpent_summons', 1, 6), ('hollow_echo', 1, 6),
    ('bottomless_bucket', 1, 6), ('harvest_scythe', 1, 10), ('dawn_hourglass', 1, 12), ('dread_lantern', 1, 16), ('menders_altar', 1, 18),
    ('tome_eternity', 1, 24)]
EXTRA = []   # (buy, sell) trades later phases add to his window (2.85a: what Dread Essence buys)

# ================================================================== REFORGING: past the old maximum
OLD_NAME = {'hero': 'Hero of Time', 'juggernaut': 'Juggernaut III', 'shadowstep': 'Shadowstep III', 'architect': 'Architect III',
            'tidecaller': 'Tidecaller III', 'crimson': 'Crimson Revenant', 'vampire': 'Vampire Lord'}
SETS = {  # old set: (new set, base ids by piece, name, piece names, colour, trim, extra per piece (armor, tough, hp, kb, speed%), set bonus, cost)
    'hero': ('deity', 'hero_{p}', 'Fierce Deity', ['Mask', 'Tunic', 'Greaves', 'Boots'], '#e8ecff', ('diamond', 'wild'), (0, 2, 5, 0.05, 0),
             'Full set: Regeneration II and Strength I; under a third of your health, Resistance II for 6 s (90 s rest)', 4),
    'juggernaut': ('bastion', 'juggernaut_{p}_3', 'Bastion', ['Greathelm', 'Bulwark', 'Tassets', 'Sabatons'], '#c8462e', ('netherite', 'silence'), (4, 5, 4, 0.25, -2),
                   'Full set: Resistance (as Juggernaut) - and Resistance II while you crouch', 3),
    'shadowstep': ('umbral', 'shadowstep_{p}_3', 'Umbral', ['Veil', 'Shroud', 'Leggings', 'Treads'], '#5a3a8a', None, (0, 3, 0, 0, 12),
                   'Full set: Speed I and Night Vision; Strength I in the dark of night (and still unseen when you crouch)', 3),
    'architect': ('mason', 'architect_{p}_3', 'Master Mason', ['Crown', 'Apron', 'Toolbelt', 'Boots'], '#3a8ae0', ('gold', 'shaper'), (0, 3, 0, 0, 0),
                  'Full set: Haste II and +1 Luck (and the Architect\'s reach)', 3),
    'tidecaller': ('leviathan', 'tidecaller_{p}_3', 'Leviathan', ['Crown', 'Scale Mail', 'Fins', 'Flippers'], '#1ac8b0', ('diamond', 'tide'), (0, 3, 2, 0, 0),
                   'Full set: no slowness on land; Strength I and Resistance I in water or rain (and the Tidecaller\'s gifts)', 3),
    'crimson': ('sanguine', 'crimson_{p}', 'Sanguine Lord', ['Skullcrown', 'Ribcage', 'Legbones', 'Gravewalkers'], '#c80018', ('redstone', 'rib'), (0, 2, 3, 0, 0),
                'Full set: Regeneration I (and the Revenants still rise for you)', 3),
    'vampire': ('nosferatu', 'vampire_{p}', 'Nosferatu', ['Cowl', 'Mantle', 'Breeches', 'Boots'], '#9a0010', ('redstone', 'vex'), (0, 2, 2, 0, 0),
                'Full set: at night, Speed I and Strength I (and every kill still heals)', 3),
}
PIECES = ['helmet', 'chestplate', 'leggings', 'boots']
REFORGE = {}      # old iid -> (new iid, price)
for old, (new, fmt, nm, pn, col, trim, (ea, et, eh, ek, es), bonus, price) in SETS.items():
    for i, p in enumerate(PIECES):
        src = ITEMS[fmt.format(p=p)]
        s = ARMOR_SLOT[p]
        comps = {k: v for k, v in src['comps'].items() if k not in ('minecraft:item_name', 'minecraft:lore', 'minecraft:custom_data')}
        en = dict(comps.get('minecraft:enchantments', {}))
        for k in list(en):
            if k == 'minecraft:protection': en[k] = max(en[k] + 1, 7)
            if k == 'minecraft:unbreaking': en[k] = max(en[k], 10)
        comps['minecraft:enchantments'] = en
        mods = list(comps.get('minecraft:attribute_modifiers', []))
        extra = []
        if ea: extra.append(attr('armor', ea * (1 if p == 'chestplate' else 0.5), s))
        if et: extra.append(attr('armor_toughness', et / 2, s))
        if eh: extra.append(attr('max_health', eh / (1 if p == 'chestplate' else 2), s))
        if ek: extra.append(attr('knockback_resistance', ek / 4, s))
        if es: extra.append(attr('movement_speed', es / 100 / 4, s, 'add_multiplied_base'))
        for m in extra:                          # (one id per kind, so they stack with the base piece's own)
            m['id'] = f'bm:df_{m["type"].split(":")[-1]}_{p}'
        comps['minecraft:attribute_modifiers'] = mods + extra
        if trim: comps['minecraft:trim'] = {'material': f'minecraft:{trim[0]}', 'pattern': f'minecraft:{trim[1]}'}
        if old == 'shadowstep': comps['minecraft:dyed_color'] = 0x0c0814
        perks = []
        if eh: perks.append(f'+{eh / (1 if p == "chestplate" else 2):g} Max Health')
        if et: perks.append(f'+{et / 2:g} Toughness')
        if es: perks.append(f'{es / 4:+g}% Speed')
        if ea: perks.append(f'+{ea * (1 if p == "chestplate" else 0.5):g} Armor')
        iid = f'{new}_{p}'
        item(iid, src['base'], f'{nm} {pn[i]}', col,
             ['Dread-forged by Vesper, past what it was.'] + ([(', '.join(perks), 'blue')] if perks else []) + [(bonus, 'dark_aqua')],
             comps=comps, custom_extra={'bm_set': new, 'bm_up': old}, cat='gear', bold=True)
        REFORGE[fmt.format(p=p)] = (iid, price)
WEAPONS = {  # old iid: (new iid, name, colour, enchantments raised or added, extra attack damage, extra modifiers, lore, price)
    'biggoron_sword': ('oathbreaker', 'Oathbreaker', '#e8e8ff', dict(fire_aspect=3), 2, [attr('entity_interaction_range', 0.5, 'mainhand', ident='bm:df_reach')],
                       ['It broke every promise but one.', ("+2 Attack Damage, +0.5 Reach over Biggoron's Sword", 'blue'), ('Every kill heals two hearts.', 'dark_aqua')], 6),
    'kong_krusher': ('abyssal_excavator', 'Abyssal Excavator', '#7ad0ff', {}, 0,
                     [attr('block_break_speed', 0.5, 'mainhand', 'add_multiplied_base', ident='bm:df_break'), attr('luck', 2, 'mainhand', ident='bm:df_luck')],
                     ['Digs as though the stone were afraid.', ('+50% Break Speed, +2 Luck', 'blue'), ('Haste II while held; Night Vision below y 40.', 'dark_aqua')], 6),
    'giga_greataxe': ('worldfeller', 'Worldfeller', '#ff8a5a', {}, 2, [attr('sweeping_damage_ratio', 0.6, 'mainhand', ident='bm:df_sweep'),
                                                                     attr('entity_interaction_range', 0.5, 'mainhand', ident='bm:df_reach')],
                      ['Fells the forest. Fells the army.', ('+2 Attack Damage, +0.5 Reach', 'blue'), ('Every swing cleaves (sweeping 60%).', 'dark_aqua')], 6),
    'light_bow': ('starpiercer', 'Starpiercer', '#fff0a0', {}, 0, [], ['Its arrows remember the stars they were.', ('Speed I and Night Vision while held.', 'dark_aqua')], 6),
    'ultra_hammer': ('meteor_maul', 'Meteor Maul', '#ffb070', dict(fire_aspect=2), 2, [],
                     ['Falls like what it is named for.', ('+2 Attack Damage', 'blue'), ('Resistance I while held.', 'dark_aqua')], 6),
}
KEEP_LEVEL = {'minecraft:mending', 'minecraft:infinity', 'minecraft:flame', 'minecraft:silk_touch', 'minecraft:channeling', 'minecraft:multishot'}
for old, (new, nm, col, add, dmg, more, lore, price) in WEAPONS.items():
    oc = ITEMS[old]['comps']
    en = {k: (v if k in KEEP_LEVEL else v + 1) for k, v in oc.get('minecraft:enchantments', {}).items()}
    for k, v in ench(**add).items(): en[k] = max(en.get(k, 0), v)
    at = [dict(m) for m in oc.get('minecraft:attribute_modifiers', [])]
    for m in at:
        if m['type'] == 'minecraft:attack_damage' and m['id'] == 'minecraft:base_attack_damage': m['amount'] += dmg
    if dmg and not any(m['type'] == 'minecraft:attack_damage' for m in at):
        at = weapon_attrs(ITEMS[old]['base'].split(':')[-1], dmg)
    gear(new, ITEMS[old]['base'].split(':')[-1], nm, col, lore, en, 3, attrs=(at + more) or None, bold=True)
    REFORGE[old] = (new, price)
# Shifting gear, dread-forged: every form a little sharper / sturdier
SHIFT_X = {}
BOOST = {'minecraft:sharpness': 8, 'minecraft:smite': 8, 'minecraft:impaling': 8, 'minecraft:power': 8, 'minecraft:density': 7,
         'minecraft:protection': 6, 'minecraft:efficiency': 7, 'minecraft:fortune': 4, 'minecraft:looting': 4}
for _fam, (_name, _col, _flav, _forms) in P62.ARMS.items():
    _all = ' · '.join(f[1] for f in _forms)
    _arm = _fam.startswith('armor_')
    SHIFT_X[_fam] = []
    for _f in _forms:
        _key, _fname, _base, _ench = _f[:4]
        _extra = _f[4] if len(_f) > 4 else {}
        _en = {k: max(v, BOOST.get(k, v)) for k, v in _ench.items()}
        iid = f'shiftx_{_fam}_{_key}'
        item(iid, _base, f'Dread-forged {_name}: {_fname}', DREAD,
             [_flav, ('Hold it and press swap-hands (F): the next ' + ('look.' if _arm else 'form.'), 'blue'), ('Sneak + F: the one before.', 'blue'), (_all, 'gray'),
              (('Protection VI under every look.' if _arm else 'Every form carries its best enchantments - higher.'), 'dark_purple'), ('Never breaks.', 'dark_purple')],
             stack=1, cat='weapon', tier=3, custom_extra={'bm_shift': B(1)}, comps=dict(P62.UNBR, **{'minecraft:enchantments': _en}, **_extra))
        SHIFT_X[_fam].append((_key, _fname))
        REFORGE[f'shift_{_fam}_{_key}'] = (iid, 4)

# ================================================================== the set bonuses (phase15's table: added before it is written)
P15.SET_FX.update({
    'deity': (['effect give @s minecraft:regeneration 11 1 true', 'effect give @s minecraft:strength 11 0 true', 'function bm:p177/set/deity'],
              'minecraft:end_rod', 'particle minecraft:dust{color:[0.95,0.95,1.0],scale:1.0} ~ ~2.3 ~ 0.2 0.05 0.2 0 3'),
    'bastion': (['execute if predicate bm:p20/sneaking run effect give @s minecraft:resistance 2 1 true'],
                'minecraft:dust{color:[0.8,0.25,0.15],scale:1.4}', 'particle minecraft:lava ~ ~0.2 ~ 0.3 0 0.3 0 1'),
    'umbral': (['effect give @s minecraft:speed 11 0 true', 'effect give @s minecraft:night_vision 15 0 true',
                'execute if score #tod bm.bm matches 13000..23000 run effect give @s minecraft:strength 11 0 true'],
               'minecraft:dust{color:[0.25,0.1,0.4],scale:1.2}', 'particle minecraft:portal ~ ~0.6 ~ 0.3 0.4 0.3 0.2 2'),
    'mason': (['effect give @s minecraft:haste 11 1 true', 'effect give @s minecraft:luck 11 0 true'],
              'minecraft:dust{color:[0.2,0.6,1.0],scale:1.1}', 'particle minecraft:wax_on ~ ~2.2 ~ 0.2 0.05 0.2 0 1'),
    'leviathan': (['execute if block ~ ~1 ~ minecraft:water run effect give @s minecraft:strength 11 0 true',
                   'execute if block ~ ~1 ~ minecraft:water run effect give @s minecraft:resistance 11 0 true',
                   'execute if predicate bm:p177/in_rain run effect give @s minecraft:strength 11 0 true',
                   'execute if predicate bm:p177/in_rain run effect give @s minecraft:resistance 11 0 true'],
                  'minecraft:nautilus', 'particle minecraft:dolphin ~ ~1 ~ 0.4 0.5 0.4 0 3'),
    'sanguine': (['effect give @s minecraft:regeneration 11 0 true'], 'minecraft:dust{color:[0.8,0.0,0.1],scale:1.3}',
                 'particle minecraft:falling_dust{block_state:"minecraft:redstone_block"} ~ ~1.5 ~ 0.3 0.3 0.3 0 1'),
    'nosferatu': (['execute if score #tod bm.bm matches 13000..23000 run effect give @s minecraft:speed 11 0 true',
                   'execute if score #tod bm.bm matches 13000..23000 run effect give @s minecraft:strength 11 0 true'],
                  'minecraft:dust{color:[0.5,0.0,0.05],scale:1.0}', 'particle minecraft:smoke ~ ~1.2 ~ 0.3 0.4 0.3 0 2'),
})

# ================================================================== TUNING: what can be tuned, how far
TUNE = {  # class: [(key, label, attribute, step, operation, max)]
    'weapon': [('dmg', 'Attack Damage', 'attack_damage', 0.75, 'add_value', 3), ('spd', 'Swing Speed', 'attack_speed', 0.1, 'add_value', 3),
               ('rch', 'Reach', 'entity_interaction_range', 0.25, 'add_value', 2), ('lck', 'Luck', 'luck', 1, 'add_value', 2)],
    'tool': [('brk', 'Mining Speed', 'block_break_speed', 0.1, 'add_multiplied_base', 3), ('eff', 'Mining Efficiency', 'mining_efficiency', 3, 'add_value', 2),
             ('brc', 'Block Reach', 'block_interaction_range', 0.5, 'add_value', 2), ('lck', 'Luck', 'luck', 1, 'add_value', 2)],
    'armor': [('arm', 'Armor', 'armor', 1, 'add_value', 2), ('tgh', 'Toughness', 'armor_toughness', 1, 'add_value', 2),
              ('hp', 'Max Health', 'max_health', 1, 'add_value', 2), ('kb', 'Knockback Resistance', 'knockback_resistance', 0.05, 'add_value', 2),
              ('mv', 'Speed (boots)', 'movement_speed', 0.02, 'add_multiplied_base', 2)],
}
TUNE_CAP = 4
TUNE_BARREL = '-196 64 -197'           # (bm:gutter, the coat check's kept-loaded chunk: where an item goes to have its tunings taken off)
WEAPON_ITEMS = ['#minecraft:swords', '#minecraft:axes', 'minecraft:mace', 'minecraft:trident', 'minecraft:netherite_spear', 'minecraft:diamond_spear',
                'minecraft:iron_spear', 'minecraft:golden_spear', 'minecraft:stone_spear', 'minecraft:wooden_spear', 'minecraft:copper_spear']
TOOL_ITEMS = ['#minecraft:pickaxes', '#minecraft:shovels', '#minecraft:hoes']
ARMOR_SLOTS = [('#minecraft:head_armor', 'head'), ('#minecraft:chest_armor', 'chest'), ('#minecraft:leg_armor', 'legs'), ('#minecraft:foot_armor', 'feet')]

# ================================================================== FOLLOWERS' WARDS
WARD = [3, 4, 5]          # Dread Tokens for level 1..3 (Ward and Vigor alike)
RETURN = [(80, 3), (45, 5)]   # Swift Return: (faint seconds, price) for level 1..2


def ring(r, n, y=0.15):
    return [(round(r * math.cos(2 * math.pi * i / n), 2), y, round(r * math.sin(2 * math.pi * i / n), 2)) for i in range(n)]


def generate(G):
    fn, wjson, title, tellraw, give = G.fn, G.wjson, G.title, G.tellraw, G.give

    def offer(buy, sell):           # (G.offer rescales Trophy prices - his are exact)
        o = G.offer(buy, sell)
        o['buy']['count'] = Int(buy[1]); o['sell']['count'] = Int(sell[1])
        return o
    import phase28 as P28
    import phase173 as P173
    P = [T('[', 'dark_gray'), T('Vesper', DREAD, bold=True), T('] ', 'dark_gray')]
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    second, fast, tick = G.FUNCS['loop/second'], G.FUNCS['loop/fast'], G.FUNCS['tick']
    objs = ['bm.bk_dread', 'bm.fward', 'bm.fvig', 'bm.fret', 'bm.fwl', 'bm.fvl', 'bm.hgday', 'bm.bbu', 'bm.dkcd', 'bm.dyl']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs if o != 'bm.bbu'] + \
        ['scoreboard objectives add bm.bbu minecraft.used:minecraft.water_bucket']
    G.OBJECTIVES += objs

    # ---------------------------------------------------------------- paying in Dread Tokens: pockets first, then the bank
    fn('p177/pay', [   # (#need bm.pay set by the caller: execute if function takes no arguments)
                    f'execute store result score #inv bm.pay run clear @s {holds("dread_token")} 0',
                    'execute unless score @s bm.bk_dread matches 0.. run scoreboard players set @s bm.bk_dread 0',
                    'scoreboard players operation #all bm.pay = #inv bm.pay', 'scoreboard players operation #all bm.pay += @s bm.bk_dread',
                    'execute if score #all bm.pay < #need bm.pay run return 0',
                    'scoreboard players operation #ti bm.pay = #need bm.pay', 'scoreboard players operation #ti bm.pay < #inv bm.pay',
                    'execute store result storage bm:ui p177.k int 1 run scoreboard players get #ti bm.pay', 'function bm:p177/pay_inv with storage bm:ui p177',
                    'scoreboard players operation #need bm.pay -= #ti bm.pay', 'scoreboard players operation @s bm.bk_dread -= #need bm.pay',
                    'playsound minecraft:block.chain.place player @s ~ ~ ~ 0.8 0.7', 'return 1'])
    fn('p177/pay_inv', [f'$clear @s {holds("dread_token")} $(k)'])
    fn('p177/poor', [say('Not enough Dread Tokens (in your pockets and the Rat Bank together).', 'red'),
                     'playsound minecraft:entity.villager.no player @s ~ ~ ~ 0.8 0.7'])
    fn('p177/refund', ['$give @s ' + G.item_arg('dread_token') + ' $(n)'])
    fn('p177/wallet', [f'execute store result score #dw bm.pay run clear @s {holds("dread_token")} 0',
                       'execute unless score @s bm.bk_dread matches 0.. run scoreboard players set @s bm.bk_dread 0',
                       'scoreboard players operation #dw bm.pay += @s bm.bk_dread', 'execute store result storage bm:ui vs.dt int 1 run scoreboard players get #dw bm.pay'])

    # ---------------------------------------------------------------- Vesper and his stall (only while the world is in hard mode)
    vpos, lpos, lnpos = mgeo.rel(VESPER_POS), mgeo.rel(LEDGER_POS), mgeo.rel(LANTERN_POS)
    vesper = {'Tags': ['bm.npc', 'bm.vesper', 'bm.npc_dread'], 'NoAI': B(1), 'Invulnerable': B(1), 'Silent': B(1), 'PersistenceRequired': B(1),
              'CustomName': T('Vesper, the Dread Broker', DREAD, bold=True), 'CustomNameVisible': B(1),
              'VillagerData': {'type': 'minecraft:swamp', 'profession': 'minecraft:cleric', 'level': Int(5)},
              'Offers': {'Recipes': [offer(('trophy', TPD), ('dread_token', 1)), offer(('dread_token', 1), ('trophy', TPD))] +
                                    [offer(('dread_token', p), (iid, n)) for iid, n, p in STOCK] + [offer(b, s_) for b, s_ in EXTRA]}}
    ident = [F(0), F(0), F(0), F(1)]
    book = {'Tags': ['bm.vledger_d', 'bm.npc'], 'item': {'id': 'minecraft:written_book', 'count': Int(1)}, 'item_display': 'fixed',
            'transformation': {'left_rotation': [F(-0.7071), F(0), F(0), F(0.7071)], 'right_rotation': ident, 'translation': [F(0), F(0.03), F(0)], 'scale': [F(0.55)] * 3}}
    box = {'Tags': ['bm.vledger', 'bm.npc'], 'width': F(0.7), 'height': F(0.5), 'response': B(1)}
    sign = {'Tags': ['bm.vledger_t', 'bm.npc'], 'billboard': 'center', 'background': Int(0x70000000), 'view_range': F(0.3),
            'text': [T("VESPER'S LEDGER\n", DREAD, bold=True), T('right-click: services', 'gray')],
            'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.55), F(0)], 'scale': [F(0.4)] * 3}}
    fn('p177/spawn', [f'summon minecraft:villager ~ ~ ~ {snbt(vesper)}', 'tp @e[type=minecraft:villager,tag=bm.vesper,distance=..1,limit=1] ~ ~ ~ ~ 0',
                      'playsound minecraft:ambient.soul_sand_valley.mood ambient @a[distance=..24] ~ ~ ~ 1 0.7',
                      'particle minecraft:soul ~ ~1 ~ 0.4 0.8 0.4 0.02 30'])
    fn('p177/ledger_spawn', [f'summon minecraft:item_display ~ ~ ~ {snbt(book)}', f'summon minecraft:interaction ~ ~ ~ {snbt(box)}',
                             f'summon minecraft:text_display ~ ~ ~ {snbt(sign)}'])
    patch = G.FUNCS['p35/patch']
    patch += [f'execute if score #hard bm.cfg matches 1 positioned {vpos} unless entity @e[type=minecraft:villager,tag=bm.vesper,distance=..3] rotated ~ 0 run function bm:p177/spawn',
              f'execute if score #hard bm.cfg matches 1 positioned {vpos} as @e[type=minecraft:villager,tag=bm.vesper,distance=..3] run data modify entity @s Offers set value {snbt(vesper["Offers"])}',
              f'execute if score #hard bm.cfg matches 1 positioned {lpos} unless entity @e[type=minecraft:interaction,tag=bm.vledger,distance=..1] run function bm:p177/ledger_spawn',
              f'execute if score #hard bm.cfg matches 1 positioned {lnpos} if block ~ ~ ~ minecraft:lantern run setblock ~ ~ ~ minecraft:soul_lantern',
              f'execute unless score #hard bm.cfg matches 1 positioned {lnpos} if block ~ ~ ~ minecraft:soul_lantern run setblock ~ ~ ~ minecraft:lantern',
              f'execute unless score #hard bm.cfg matches 1 positioned {vpos} run kill @e[tag=bm.vesper,distance=..3]',
              f'execute unless score #hard bm.cfg matches 1 positioned {lpos} run kill @e[tag=bm.vledger,distance=..1]',
              f'execute unless score #hard bm.cfg matches 1 positioned {lpos} run kill @e[tag=bm.vledger_d,distance=..1]',
              f'execute unless score #hard bm.cfg matches 1 positioned {lpos} run kill @e[tag=bm.vledger_t,distance=..1]']
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[tag=bm.vesper]', 'kill @e[tag=bm.vledger]', 'kill @e[tag=bm.vledger_d]', 'kill @e[tag=bm.vledger_t]']
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.vledger] if data entity @s interaction at @s run function bm:p177/ledger_click',
             'execute as @e[type=minecraft:interaction,tag=bm.vledger] if data entity @s attack run data remove entity @s attack']
    fn('p177/ledger_click', ['execute on target run function bm:p177/open', 'data remove entity @s interaction'])
    # his voice, now and then, to anyone at the stall
    lines = ['"Trophies? Splendid. Bring five."', '"The King had debts. I collect them."', '"Something hunts the dark now. I sell to those it hasn\'t caught."',
             '"Your followers look... breakable. I can fix that."', '"Everything is for sale. Especially time."']
    second.append(f'execute as @e[type=minecraft:villager,tag=bm.vesper] at @s if entity @a[distance=..5] run function bm:p177/mutter')
    fn('p177/mutter', ['execute store result score #vm bm.rng run random value 1..40'] +
       [f'execute if score #vm bm.rng matches {i + 1} run ' + tellraw('@a[distance=..6]', P + [T(l, '#c8a0a0', italic=True)]) for i, l in enumerate(lines)])

    # ---------------------------------------------------------------- the Ledger: his services
    B_ = lambda lbl, code, w=180, tip=None: P28.btn(lbl, code, tooltip=tip, width=w)
    main = P28.multi([T("VESPER'S LEDGER", DREAD, bold=True), T('  ·  the Dread Broker', 'gray')],
                     [P28.body([T('"Sit. Sign nothing yet. Read."', '#c8a0a0', italic=True)], 320),
                      P28.body([T('You have ', 'gray'), T('$(dt)', DREAD, bold=True), T(' Dread Tokens (pockets and Rat Bank).', 'gray')], 320),
                      P28.body([T(f'Trade with Vesper himself (right-click him): {TPD} Trophies for a Dread Token and back, maps, writs, summonses and the long work.', 'dark_gray')], 320)],
                     [B_([T("Followers' Wards", '#ffb0b0', bold=True)], MENU + 1, tip=T('Armour, health and a quicker return for every follower you call', 'gray')),
                      B_([T('Tuning', '#ffd27a', bold=True)], MENU + 2, tip=T('The weapon, tool or armour in your hand: a tuning of your choice', 'gray')),
                      B_([T('Reforging', DREAD, bold=True)], MENU + 3, tip=T('Past the old maximum: sets, legendary weapons, Shifting gear', 'gray')),
                      B_([T('About the Dread', 'gray')], MENU + 4)], columns=2)
    fn('p177/open', ['execute unless score #hard bm.cfg matches 1 run return 0', f'scoreboard players set @s bm.menu {MENU}', 'function bm:p177/wallet',
                     'function bm:p177/open_dlg with storage bm:ui vs', 'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.7'])
    fn('p177/open_dlg', [f'$dialog show @s {P28.inline(main)}'])
    about = P28.multi([T('About the Dread', DREAD, bold=True)],
                      [P28.body([T('Something older than the Hollow King put its strength in him. With him gone, it reaches for the world itself: '
                                   'Dread monsters walk the night - they gather themselves before they strike (a red ring at their feet, or souls '
                                   'falling where you stand): move, and the blow misses.', 'gray')], 320),
                       P28.body([T('Every Dread you kill is counted. Kill enough of them, and the thing that made them will come looking.', '#c8a0a0', italic=True)], 320)],
                      [B_(T('« The Ledger', 'gray'), MENU + 9)], columns=1)
    fn('p177/about', [f'scoreboard players set @s bm.menu {MENU}', f'dialog show @s {snbt(about)}'])

    # ---- followers' wards
    fol = P28.multi([T("Followers' Wards", '#ffb0b0', bold=True), T('  ·  Vesper', 'gray')],
                    [P28.body([T('Every follower you call - at home and on a heist - carries what you buy here, for good.', 'gray')], 320),
                     P28.body([T('Ward ', '#ffb0b0'), T('$(w)/3', 'white'), T('   +3 armour and +1 toughness a level', 'dark_gray')], 320),
                     P28.body([T('Vigor ', '#ffb0b0'), T('$(v)/3', 'white'), T('   +10% health a level', 'dark_gray')], 320),
                     P28.body([T('Swift Return ', '#ffb0b0'), T('$(r)/2', 'white'), T('   a faint rests 80 s, then 45 s (not 2 minutes)', 'dark_gray')], 320),
                     P28.body([T('You have ', 'gray'), T('$(dt)', DREAD, bold=True), T(' Dread Tokens.', 'gray')], 320)],
                    [B_([T('Ward +1', '#ffb0b0'), T(f'  ({"/".join(map(str, WARD))} DT)', 'gray')], MENU + 11),
                     B_([T('Vigor +1', '#ffb0b0'), T(f'  ({"/".join(map(str, WARD))} DT)', 'gray')], MENU + 12),
                     B_([T('Swift Return +1', '#ffb0b0'), T(f'  ({"/".join(str(p) for _s, p in RETURN)} DT)', 'gray')], MENU + 13),
                     B_(T('« The Ledger', 'gray'), MENU + 9)], columns=2)
    fn('p177/fol', [f'scoreboard players set @s bm.menu {MENU}', 'function bm:p177/wallet'] +
       [f'execute unless score @s {o} matches 0.. run scoreboard players set @s {o} 0' for o in ('bm.fward', 'bm.fvig', 'bm.fret')] +
       ['execute store result storage bm:ui vs.w int 1 run scoreboard players get @s bm.fward', 'execute store result storage bm:ui vs.v int 1 run scoreboard players get @s bm.fvig',
        'execute store result storage bm:ui vs.r int 1 run scoreboard players get @s bm.fret', 'function bm:p177/fol_dlg with storage bm:ui vs'])
    fn('p177/fol_dlg', [f'$dialog show @s {P28.inline(fol)}'])
    for k, obj, nm in (('w', 'bm.fward', 'Ward'), ('v', 'bm.fvig', 'Vigor')):
        fn(f'p177/buy_{k}', [f'execute if score @s {obj} matches 3.. run return run function bm:p177/fol_max'] +
           [f'execute if score @s {obj} matches {lv} run return run function bm:p177/buy_{k}{lv + 1}' for lv in range(3)])
        for lv in range(1, 4):
            fn(f'p177/buy_{k}{lv}', [f'scoreboard players set #need bm.pay {WARD[lv - 1]}', 'execute unless function bm:p177/pay run return run function bm:p177/poor',
                                     f'scoreboard players set @s {obj} {lv}', 'playsound minecraft:block.beacon.power_select player @s ~ ~ ~ 0.8 0.6',
                                     tellraw('@s', P + [T(f'{nm} {"I" * lv} - your followers will feel it the next moment they stand beside you.', 'gray')]),
                                     'function bm:p177/fol'])
    fn('p177/buy_r', ['execute if score @s bm.fret matches 2.. run return run function bm:p177/fol_max',
                      'execute if score @s bm.fret matches 1 run return run function bm:p177/buy_r2', 'function bm:p177/buy_r1'])
    for lv, (secs, price) in enumerate(RETURN, 1):
        fn(f'p177/buy_r{lv}', [f'scoreboard players set #need bm.pay {price}', 'execute unless function bm:p177/pay run return run function bm:p177/poor', f'scoreboard players set @s bm.fret {lv}',
                               'playsound minecraft:block.beacon.power_select player @s ~ ~ ~ 0.8 0.8',
                               tellraw('@s', P + [T(f'Swift Return {"I" * lv}: a faint now rests {secs} seconds.', 'gray')]), 'function bm:p177/fol'])
    fn('p177/fol_max', [say('That is as far as it goes.', '#c8a0a0'), 'function bm:p177/fol'])
    # the wards on every follower you call: checked a second, re-applied when you buy more
    for w, (cd, typ, tag, call) in P173.AR.items():
        second.append(f'execute as @e[type=minecraft:{typ},tag={tag}] at @s run function bm:p177/fb/check')
    fn('p177/fb/check', ['execute unless score @s bm.pid matches 1.. run return 0', 'scoreboard players operation #me bm.pid = @s bm.pid',
                         'scoreboard players set #wl bm.rng 0', 'scoreboard players set #vl bm.rng 0',
                         'execute as @a if score @s bm.pid = #me bm.pid run function bm:p177/fb/owner',
                         'execute unless score @s bm.fwl = #wl bm.rng run function bm:p177/fb/ward',
                         'execute unless score @s bm.fvl = #vl bm.rng run function bm:p177/fb/vigor'])
    fn('p177/fb/owner', ['scoreboard players operation #wl bm.rng = @s bm.fward', 'scoreboard players operation #vl bm.rng = @s bm.fvig'])
    fn('p177/fb/ward', ['scoreboard players operation @s bm.fwl = #wl bm.rng', 'attribute @s minecraft:armor modifier remove bm:dread_ward',
                        'attribute @s minecraft:armor_toughness modifier remove bm:dread_ward'] +
       [f'execute if score #wl bm.rng matches {lv} run function bm:p177/fb/ward{lv}' for lv in (1, 2, 3)])
    for lv in (1, 2, 3):
        fn(f'p177/fb/ward{lv}', [f'attribute @s minecraft:armor modifier add bm:dread_ward {3 * lv} add_value',
                                 f'attribute @s minecraft:armor_toughness modifier add bm:dread_ward {lv} add_value',
                                 'particle minecraft:soul ~ ~1 ~ 0.3 0.4 0.3 0.02 6'])
        fn(f'p177/fb/vigor{lv}', [f'attribute @s minecraft:max_health modifier add bm:dread_vigor {0.1 * lv:.1f} add_multiplied_base',
                                  'particle minecraft:heart ~ ~1.2 ~ 0.3 0.3 0.3 0 2'])
    fn('p177/fb/vigor', ['scoreboard players operation @s bm.fvl = #vl bm.rng', 'attribute @s minecraft:max_health modifier remove bm:dread_vigor'] +
       [f'execute if score #vl bm.rng matches {lv} run function bm:p177/fb/vigor{lv}' for lv in (1, 2, 3)])
    # Swift Return: after a faint (2 minutes), the rest is cut short
    for w, (cd, typ, tag, call) in P173.AR.items():
        second += [f'execute as @a[scores={{bm.fret=1,{cd}=81..}}] run scoreboard players set @s {cd} 80',
                   f'execute as @a[scores={{bm.fret=2,{cd}=46..}}] run scoreboard players set @s {cd} 45']

    # ---- tuning
    cls_lines = ['scoreboard players set #tc bm.rng 0'] + \
        [f'execute if items entity @s weapon.mainhand {it} run scoreboard players set #tc bm.rng 1' for it in WEAPON_ITEMS] + \
        [f'execute if items entity @s weapon.mainhand {it} run scoreboard players set #tc bm.rng 2' for it in TOOL_ITEMS] + \
        [f'execute if items entity @s weapon.mainhand {it} run scoreboard players set #tc bm.rng {3 + i}' for i, (it, sl) in enumerate(ARMOR_SLOTS)]
    fn('p177/tclass', cls_lines)
    fn('p177/tune', [f'scoreboard players set @s bm.menu {MENU}', 'function bm:p177/tclass',
                     'execute if score #tc bm.rng matches 0 run return run function bm:p177/tune_none',
                     'execute if score #tc bm.rng matches 1 run return run function bm:p177/tp/weapon',
                     'execute if score #tc bm.rng matches 2 run return run function bm:p177/tp/tool',
                     'function bm:p177/tp/armor'])
    fn('p177/tune_none', [say('Hold the weapon, tool or armour piece to tune in your main hand, then open the Ledger.', '#c8a0a0'), 'function bm:p177/open'])
    code = MENU + 20
    TCODE = {}
    for cls, opts in TUNE.items():
        btns = []
        for key, lbl, at_, step, op, mx in opts:
            TCODE[(cls, key)] = code
            mxx = mx if not (cls == 'weapon' and key in ('dmg', 'spd')) else 3
            btns.append(B_([T(lbl, '#ffd27a'), T(f'  +{step * 100:g}%' if op != 'add_value' else f'  +{step:g}', 'gray'), T(f'  (max {mxx})', 'gray')], code, w=210))
            code += 1
        TCODE[(cls, 'unbind')] = code; code += 1
        btns += [B_([T('Unbind all tunings', 'red'), T('  (every token back)', 'gray')], TCODE[(cls, 'unbind')], w=210), B_(T('« The Ledger', 'gray'), MENU + 9, w=210)]
        page = P28.multi([T('Tuning', '#ffd27a', bold=True), T(f'  ·  {"a weapon" if cls == "weapon" else "a tool" if cls == "tool" else "an armour piece"}', 'gray')],
                         [P28.body([T('A Dread Token a level. Any one kind up to its max; ', 'gray'), T(f'{TUNE_CAP} levels in all', 'white'), T(' on any item.', 'gray')], 320),
                          P28.body([T('This one carries ', 'gray'), T('$(tn)', 'white', bold=True), T(f'/{TUNE_CAP}.  You have ', 'gray'), T('$(dt)', DREAD, bold=True),
                                    T(' Dread Tokens.', 'gray')], 320)], btns, columns=1)
        fn(f'p177/tp/{cls}', ['function bm:p177/wallet', 'execute store result storage bm:ui vs.tn int 1 run data get entity @s SelectedItem.components."minecraft:custom_data".bm_tune.n',
                              f'function bm:p177/tp/{cls}_dlg with storage bm:ui vs'])
        fn(f'p177/tp/{cls}_dlg', [f'$dialog show @s {P28.inline(page)}'])
    assert code <= MENU + 60, code
    # a tuning: the item still in hand and still of its kind; under its caps; paid; the modifier added (its level's own id)
    for cls, opts in TUNE.items():
        cno = {'weapon': '1', 'tool': '2', 'armor': '3..6'}[cls]
        for key, lbl, at_, step, op, mx in opts:
            mxx = 3 if (cls == 'weapon' and key in ('dmg', 'spd')) else mx
            path = f'SelectedItem.components."minecraft:custom_data".bm_tune.{key}'
            lines_ = ['function bm:p177/tclass', f'execute unless score #tc bm.rng matches {cno} run return run function bm:p177/tune_none',
                      f'execute store result score #tl bm.rng run data get entity @s {path}',
                      'execute store result score #tn bm.rng run data get entity @s SelectedItem.components."minecraft:custom_data".bm_tune.n',
                      f'execute if score #tl bm.rng matches {mxx}.. run return run function bm:p177/tune_max',
                      f'execute if score #tn bm.rng matches {TUNE_CAP}.. run return run function bm:p177/tune_full']
            if key == 'mv':
                lines_.append(f'execute unless score #tc bm.rng matches 6 run return run function bm:p177/tune_boots')
            lines_ += ['scoreboard players set #need bm.pay 1', 'execute unless function bm:p177/pay run return run function bm:p177/poor',
                       'scoreboard players add #tl bm.rng 1', 'scoreboard players add #tn bm.rng 1',
                       'execute store result storage bm:ui tu.l int 1 run scoreboard players get #tl bm.rng',
                       'execute store result storage bm:ui tu.n int 1 run scoreboard players get #tn bm.rng']
            if cls == 'armor':
                for i, (it, sl) in enumerate(ARMOR_SLOTS):
                    lines_.append(f'execute if score #tc bm.rng matches {3 + i} run data modify storage bm:ui tu.s set value "{sl}"')
            else:
                lines_.append('data modify storage bm:ui tu.s set value "mainhand"')
            lines_ += [f'function bm:p177/tset/{cls}_{key} with storage bm:ui tu', 'playsound minecraft:block.smithing_table.use player @s ~ ~ ~ 0.8 0.8',
                       'particle minecraft:enchant ~ ~1.2 ~ 0.3 0.4 0.3 0.6 20', title('@s', 'actionbar', [T('Tuned: ', '#ffd27a'), T(lbl, 'white')]),
                       f'function bm:p177/tp/{cls}']
            fn(f'p177/tune/{cls}_{key}', lines_)
            fn(f'p177/tset/{cls}_{key}', [
                f'$item modify entity @s weapon.mainhand {{function:"minecraft:set_attributes",replace:false,modifiers:[{{attribute:"minecraft:{at_}",'
                f'id:"bm:tune_{key}_$(l)",amount:{step},operation:"{op}",slot:"$(s)"}}]}}',
                f'$item modify entity @s weapon.mainhand {{function:"minecraft:set_custom_data",tag:"{{bm_tune:{{{key}:$(l),n:$(n)}}}}"}}'])
    fn('p177/tune_max', [say('That kind is tuned as far as it goes on this item.', '#c8a0a0'), 'function bm:p177/tune'])
    fn('p177/tune_full', [say(f'This item carries all {TUNE_CAP} tunings it can. Unbind them to choose again.', '#c8a0a0'), 'function bm:p177/tune'])
    fn('p177/tune_boots', [say('Speed tunes only onto boots.', '#c8a0a0'), 'function bm:p177/tune'])
    # unbind: the item goes to a barrel in the kept-loaded gutter for a moment, every bm:tune_* modifier comes off, it comes back
    ids = sorted({f'bm:tune_{k}_{l}' for opts in TUNE.values() for k, *_r, mx in opts for l in range(1, 4)})
    fn('p177/unbind', ['function bm:p177/tclass', 'execute if score #tc bm.rng matches 0 run return run function bm:p177/tune_none',
                       'execute store result score #tn bm.rng run data get entity @s SelectedItem.components."minecraft:custom_data".bm_tune.n',
                       'execute if score #tn bm.rng matches ..0 run return run function bm:p177/unbind_none',
                       f'execute in bm:gutter unless block {TUNE_BARREL} minecraft:barrel run setblock {TUNE_BARREL} minecraft:barrel',
                       f'execute in bm:gutter run item replace block {TUNE_BARREL} container.0 from entity @s weapon.mainhand'] +
       [f'execute in bm:gutter run data remove block {TUNE_BARREL} Items[0].components."minecraft:attribute_modifiers"[{{id:"{i}"}}]' for i in ids] +
       [f'execute in bm:gutter run data remove block {TUNE_BARREL} Items[0].components."minecraft:custom_data".bm_tune',
        f'execute in bm:gutter run item replace entity @s weapon.mainhand from block {TUNE_BARREL} container.0',
        f'execute in bm:gutter run item replace block {TUNE_BARREL} container.0 with minecraft:air',
        'execute store result storage bm:ui p177.n int 1 run scoreboard players get #tn bm.rng', 'function bm:p177/refund with storage bm:ui p177',
        'playsound minecraft:block.grindstone.use player @s ~ ~ ~ 0.8 0.8',
        tellraw('@s', P + [T('Unbound. ', 'gray'), {'score': {'name': '#tn', 'objective': 'bm.rng'}, 'color': DREAD}, T(' Dread Tokens back in your hand.', 'gray')]),
        'function bm:p177/tune'])
    fn('p177/unbind_none', [say('Nothing tuned on this item.', '#c8a0a0'), 'function bm:p177/tune'])

    # ---- reforging
    price_lines = [P28.body([T('Hold the piece in your main hand and press Reforge. ', 'gray'), T('Tunings must be unbound first.', 'dark_gray')], 330)] + \
        [P28.body([T(f'{nm}', col, bold=True), T(f'  ← {OLD_NAME[old]}', 'gray'), T(f'   {price} DT a piece', DREAD)], 330)
         for old, (new, fmt, nm, pn, col, trim, ex, bonus, price) in SETS.items()] + \
        [P28.body([T('Oathbreaker, Abyssal Excavator, Worldfeller, Starpiercer, Meteor Maul', '#e8e8ff', bold=True), T('  6 DT each', DREAD)], 330),
         P28.body([T('Dread-forged Shifting gear', DREAD, bold=True), T('  any form, 4 DT', DREAD)], 330),
         P28.body([T('You have ', 'gray'), T('$(dt)', DREAD, bold=True), T(' Dread Tokens.', 'gray')], 330)]
    rf = P28.multi([T('Reforging', DREAD, bold=True), T('  ·  past the old maximum', 'gray')], price_lines,
                   [B_([T('Reforge what I hold', DREAD, bold=True)], MENU + 5, w=200), B_(T('« The Ledger', 'gray'), MENU + 9, w=200)], columns=2)
    fn('p177/rf', [f'scoreboard players set @s bm.menu {MENU}', 'function bm:p177/wallet', 'function bm:p177/rf_dlg with storage bm:ui vs'])
    fn('p177/rf_dlg', [f'$dialog show @s {P28.inline(rf)}'])
    rfl = ['execute if data entity @s SelectedItem.components."minecraft:custom_data".bm_tune.n run return run function bm:p177/rf_tuned']
    for old, (new, price) in REFORGE.items():
        rfl.append(f'execute if items entity @s weapon.mainhand {holds(old)} run return run function bm:p177/rfx/{old}')
        fn(f'p177/rfx/{old}', [f'scoreboard players set #need bm.pay {price}', 'execute unless function bm:p177/pay run return run function bm:p177/poor',
                               f'item replace entity @s weapon.mainhand with {G.item_arg(new)}',
                               'playsound minecraft:block.anvil.use player @s ~ ~ ~ 0.8 0.6', 'playsound minecraft:entity.wither.break_block player @s ~ ~ ~ 0.4 1.6',
                               'particle minecraft:soul_fire_flame ~ ~1.2 ~ 0.3 0.4 0.3 0.05 30', 'particle minecraft:enchant ~ ~1.2 ~ 0.4 0.5 0.4 0.8 40',
                               tellraw('@s', P + [T('Reforged: ', 'gray'), T(ITEMS[new]['name'], DREAD, bold=True), T('.', 'gray')]),
                               'function bm:p177/rf'])
    rfl.append('function bm:p177/rf_none')
    fn('p177/reforge', rfl)
    fn('p177/rf_none', [say('Hold something he can reforge in your main hand (see the list).', '#c8a0a0'), 'function bm:p177/rf'])
    fn('p177/rf_tuned', [say('Unbind its tunings first (Tuning, in the Ledger).', '#c8a0a0'), 'function bm:p177/rf'])
    # (the old set's power stays with its successor: phase15's set checks take either)
    for old, (new, *_r) in SETS.items():
        nm = f'sets/has/{old}' if f'sets/has/{old}' in G.FUNCS else None
        if not nm: continue
        L = G.FUNCS[nm]
        L[:] = [l.replace(f'*[minecraft:custom_data~{{bm_set:"{old}"}}]', f'*[minecraft:custom_data~{{bm_set:"{old}"}}|minecraft:custom_data~{{bm_up:"{old}"}}]') for l in L]
    G.wjson('bm/predicate/p177/in_rain.json', {'condition': 'minecraft:all_of', 'terms': [
        {'condition': 'minecraft:weather_check', 'raining': True}, {'condition': 'minecraft:location_check', 'predicate': {'can_see_sky': True}}]})
    # Fierce Deity's last stand: under a third of your health, Resistance II for 6 s - then it rests 90 s
    fn('p177/set/deity', ['execute if score @s bm.dyl matches 1.. run return 0', 'execute store result score #hh bm.rng run data get entity @s Health',
                          'execute store result score #hm bm.rng run attribute @s minecraft:max_health get', 'scoreboard players operation #hh bm.rng *= #3 bm.p177',
                          'execute if score #hh bm.rng > #hm bm.rng run return 0', 'effect give @s minecraft:resistance 6 1 true', 'scoreboard players set @s bm.dyl 90',
                          'playsound minecraft:item.totem.use player @s ~ ~ ~ 0.4 1.6', 'particle minecraft:end_rod ~ ~1 ~ 0.4 0.6 0.4 0.1 30'])
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.p177 dummy'] + [f'scoreboard players set #{n} bm.p177 {n}' for n in (2, 3, 5, -1)]
    G.OBJECTIVES += ['bm.p177']
    second.append('scoreboard players remove @a[scores={bm.dyl=1..}] bm.dyl 1')
    # the legendary weapons' own gifts
    second += [f'execute as @a if items entity @s weapon.mainhand {holds("abyssal_excavator")} run effect give @s minecraft:haste 2 1 true',
               f'execute as @a at @s if items entity @s weapon.mainhand {holds("abyssal_excavator")} if entity @s[y=-64,dy=103] run effect give @s minecraft:night_vision 12 0 true',
               f'execute as @a if items entity @s weapon.mainhand {holds("starpiercer")} run effect give @s minecraft:speed 2 0 true',
               f'execute as @a if items entity @s weapon.mainhand {holds("starpiercer")} run effect give @s minecraft:night_vision 12 0 true',
               f'execute as @a if items entity @s weapon.mainhand {holds("meteor_maul")} run effect give @s minecraft:resistance 2 0 true']
    wjson('bm/advancement/p177/oath_kill.json', {'criteria': {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {
        'player': [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {
            'equipment': {'mainhand': {'predicates': {'minecraft:custom_data': '{bm:"oathbreaker"}'}}}}}]}}}, 'rewards': {'function': 'bm:p177/oath_kill'}})
    fn('p177/oath_kill', ['advancement revoke @s only bm:p177/oath_kill', 'effect give @s minecraft:instant_health 1 0 true', 'particle minecraft:heart ~ ~1.8 ~ 0.3 0.2 0.3 0 3'])
    # Dread-forged Shifting gear changes form like the rest (phase62's swap, for the new families)
    sx = []
    for fam, forms in SHIFT_X.items():
        n = len(forms)
        name, col = P62.ARMS[fam][0], DREAD
        for i, (key, fname) in enumerate(forms):
            iid = f'shiftx_{fam}_{key}'
            for d, nm in ((1, 'next'), (-1, 'prev')):
                to = forms[(i + d) % n]
                fn(f'p177/sx/{iid}_{nm}', ['item replace entity @s weapon.offhand from entity @s weapon.mainhand',
                                           f'item replace entity @s weapon.mainhand with {G.item_arg(f"shiftx_{fam}_{to[0]}")}',
                                           'particle minecraft:soul_fire_flame ~ ~1.2 ~ 0.3 0.4 0.3 0.03 12',
                                           'playsound minecraft:item.armor.equip_netherite player @a[distance=..12] ~ ~ ~ 0.8 1.2',
                                           title('@s', 'actionbar', [T('Dread-forged ' + name + ': ', col, bold=True), T(to[1], 'white', bold=True)])])
            sx += [f'execute if items entity @s weapon.offhand {holds(iid)} if predicate bm:p20/sneaking run return run function bm:p177/sx/{iid}_prev',
                   f'execute if items entity @s weapon.offhand {holds(iid)} run return run function bm:p177/sx/{iid}_next']
    G.FUNCS['p62/shift'][0:0] = sx

    # ---- the Ledger's router
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {MENU}..{MENU + 99} run return run function bm:p177/act')
    act = [f'execute unless score @s bm.menu matches {MENU} run return run function bm:p28/stale',
           'execute unless score #hard bm.cfg matches 1 run return run function bm:p28/stale',
           f'execute unless entity @e[type=minecraft:interaction,tag=bm.vledger,distance=..8] run return run function bm:p28/stale',
           f'execute if score #act bm.pay matches {MENU + 1} run return run function bm:p177/fol',
           f'execute if score #act bm.pay matches {MENU + 2} run return run function bm:p177/tune',
           f'execute if score #act bm.pay matches {MENU + 3} run return run function bm:p177/rf',
           f'execute if score #act bm.pay matches {MENU + 4} run return run function bm:p177/about',
           f'execute if score #act bm.pay matches {MENU + 5} run return run function bm:p177/reforge',
           f'execute if score #act bm.pay matches {MENU + 9} run return run function bm:p177/open',
           f'execute if score #act bm.pay matches {MENU + 11} run return run function bm:p177/buy_w',
           f'execute if score #act bm.pay matches {MENU + 12} run return run function bm:p177/buy_v',
           f'execute if score #act bm.pay matches {MENU + 13} run return run function bm:p177/buy_r']
    for (cls, key), c in TCODE.items():
        act.append(f'execute if score #act bm.pay matches {c} run return run function bm:p177/{"unbind" if key == "unbind" else f"tune/{cls}_{key}"}')
    fn('p177/act', act)

    # ================================================================== his goods at work
    # the Omega Palace map
    wjson('bm/tags/worldgen/structure/om_palace_map.json', {'values': ['bm:om_palace']})
    G.consume_adv('sealed_map_omega', 'bm:maps/open_omega')
    G.sealed_map('sealed_map_omega', 'omega', '#bm:om_palace_map', title('@s', 'actionbar', T('The seal cracks... the map marks an Omega Palace.', '#9fb4ff')))
    wjson('bm/loot_table/maps/omega.json', {'type': 'minecraft:command', 'pools': [{'rolls': 1, 'entries': [{
        'type': 'minecraft:item', 'name': 'minecraft:filled_map', 'functions': [
            {'function': 'minecraft:exploration_map', 'destination': '#bm:om_palace_map', 'decoration': 'minecraft:red_x', 'zoom': 2, 'search_radius': 100, 'skip_existing_chunks': False},
            {'function': 'minecraft:set_name', 'target': 'item_name', 'name': T('Palace Map', '#9fb4ff')}]}]}]})
    # the Auctioneer's Writ
    G.consume_adv('auction_writ', 'bm:p177/writ')
    fn('p177/writ', ['advancement revoke @s only bm:consume/auction_writ',
                     'execute unless score #state bm.auc matches 0 run return run function bm:p177/writ_no',
                     'execute if score #saled bm.auc = #day bm.bm run return run function bm:p177/writ_no',
                     'execute if score #owed bm.auc matches 1 run return run function bm:p177/writ_no',
                     'scoreboard players set #owed bm.auc 1',
                     tellraw('@a', P + [T('A writ has been served. ', '#ffcf40', bold=True), T('The Dark Auction opens at dusk tonight.', 'gray')]),
                     'playsound minecraft:block.bell.use player @a ~ ~ ~ 0.6 0.6'])
    fn('p177/writ_no', [give('auction_writ'), say('The Auctioneer is already sitting tonight - or has sat today. (Your writ is returned.)', '#c8a0a0')])
    # the Serpent's Summons: the next defeat of Apophiss leaves both relics for you
    G.consume_adv('serpent_summons', 'bm:p177/summons')
    fn('p177/summons', ['advancement revoke @s only bm:consume/serpent_summons', 'tag @s add bm.apsure', 'playsound minecraft:entity.evoker.prepare_summon player @s ~ ~ ~ 0.8 0.6',
                        tellraw('@s', P + [T('The scale goes cold in your hand. ', '#3ad06a'), T('The next time Apophiss falls to you, his crown and his mace stay with you.', 'gray')])])
    cl = G.FUNCS['p131/d/claim']
    cl += ['execute if entity @s[tag=bm.apsure] run tag @s add bm.apmace', 'execute if entity @s[tag=bm.apsure] run tag @s add bm.apcrown', 'tag @s remove bm.apsure']
    # the Echo of the Hollow King: a challenger once more, and his vault forgets you
    G.consume_adv('hollow_echo', 'bm:p177/echo')
    fn('p177/echo', ['advancement revoke @s only bm:consume/hollow_echo',
                     'execute unless score @s bm.conq matches 6.. run return run function bm:p177/echo_no',
                     'execute if function bm:p137/renew_fight run return run function bm:p177/echo_fight',
                     'scoreboard players set @s bm.conq 5',
                     'playsound minecraft:entity.wither.spawn player @s ~ ~ ~ 0.5 0.6',
                     tellraw('@s', P + [T('The Hollow stirs. ', '#9a5ae0', bold=True),
                                        T('Its King will rise for you again - and his first victory pays again: his Regalia, his lore. '
                                          '(What you earned stays yours: the Warpstone, Wilfrey, the Serpent\'s Den.)', 'gray')])])
    fn('p177/echo_fight', [give('hollow_echo'), say('Not now - finish the fight first. (Returned.)', '#c8a0a0')])
    fn('p177/echo_no', [give('hollow_echo'), say('Only one who has beaten the Hollow King can call his echo. (Returned.)', '#c8a0a0')])
    # the Tome of Eternity
    G.consume_adv('tome_eternity', 'bm:p177/tome')
    fn('p177/tome', ['advancement revoke @s only bm:consume/tome_eternity',
                     'execute unless items entity @s weapon.offhand *[minecraft:max_damage] run return run function bm:p177/tome_no',
                     'execute if items entity @s weapon.offhand *[minecraft:unbreakable] run return run function bm:p177/tome_no',
                     'item modify entity @s weapon.offhand {function:"minecraft:set_components",components:{"minecraft:unbreakable":{}}}',
                     'playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 1 0.6', 'particle minecraft:enchant ~ ~1 ~ 0.4 0.6 0.4 1 60',
                     tellraw('@s', P + [T('It will endure. ', '#e8d8a0', bold=True), T('(The item in your off hand is unbreakable now.)', 'gray')])])
    fn('p177/tome_no', [give('tome_eternity'), say('Hold something that can break - and isn\'t already unbreakable - in your off hand. (Returned.)', '#c8a0a0')])
    # the Dawnbreaker Hourglass
    G.consume_adv('dawn_hourglass', 'bm:p177/dawn')
    special = ['#active bm.bm', '#inv bm.bm', '#lnight bm.bm']
    fn('p177/dawn', ['advancement revoke @s only bm:consume/dawn_hourglass', give('dawn_hourglass'),
                     'execute unless score #tod bm.bm matches 12500..23500 run return run ' + say('The sand only runs up at night.', '#c8a0a0')] +
       [f'execute if score {s} matches 1 run return run ' + say('Not tonight - this night has its own plans.', '#c8a0a0') for s in special] +
       ['execute if score #dread bm.dn matches 1 run return run ' + say('Not tonight. Something is holding the dark in place.', DREAD),
        'scoreboard players operation #hg bm.rng = #day bm.bm', 'scoreboard players operation #hg bm.rng -= @s bm.hgday',
        'execute if score @s bm.hgday matches 0.. if score #hg bm.rng matches ..2 run return run ' + say('The hourglass is still filling - once every 3 days.', '#c8a0a0'),
        'scoreboard players operation @s bm.hgday = #day bm.bm',
        'scoreboard players set #td bm.rng 24000', 'scoreboard players operation #td bm.rng -= #tod bm.bm',
        'scoreboard players add #td bm.rng 1000', 'execute store result storage bm:ui p177.t int 1 run scoreboard players get #td bm.rng',
        'function bm:p177/dawn_go with storage bm:ui p177',
        tellraw('@a', P + [T('The sand runs up the glass - ', '#ffd27a'), T('and the sun rises early.', 'gray')]),
        'execute as @a at @s run playsound minecraft:block.beacon.activate ambient @s ~ ~ ~ 0.8 1.4'])
    fn('p177/dawn_go', ['$time add $(t)'])
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.dn dummy']
    G.OBJECTIVES += ['bm.dn']
    # the Dread Compass: held, the nearest Dread within 160 blocks
    fast.append(f'execute as @a if items entity @s weapon.* {holds("dread_compass")} at @s run function bm:p177/compass')
    dirs = [('south', 0), ('south-west', 45), ('west', 90), ('north-west', 135), ('north', 180), ('north-east', -135), ('east', -90), ('south-east', -45)]
    fn('p177/compass', ['execute unless entity @e[tag=bm.dread,distance=..160] run return run ' + title('@s', 'actionbar', T('The needle rests. Nothing Dread within 160 blocks.', 'gray')),
                        'execute store result score #cx bm.rng run data get entity @s Pos[0]', 'execute store result score #cz bm.rng run data get entity @s Pos[2]',
                        'execute as @e[tag=bm.dread,distance=..160,sort=nearest,limit=1] run function bm:p177/compass_at', 'function bm:p177/compass_dir'])
    fn('p177/compass_at', ['execute store result score #dx bm.rng run data get entity @s Pos[0]', 'execute store result score #dz bm.rng run data get entity @s Pos[2]',
                           'scoreboard players operation #dx bm.rng -= #cx bm.rng', 'scoreboard players operation #dz bm.rng -= #cz bm.rng'])
    # 8 ways: a direction is "straight" while the other axis is under 2/5 of it (tan 22.5 = 0.41)
    fn('p177/compass_dir', ['scoreboard players operation #ax bm.rng = #dx bm.rng', 'execute if score #ax bm.rng matches ..-1 run scoreboard players operation #ax bm.rng *= #-1 bm.p177',
                            'scoreboard players operation #az bm.rng = #dz bm.rng', 'execute if score #az bm.rng matches ..-1 run scoreboard players operation #az bm.rng *= #-1 bm.p177',
                            'scoreboard players operation #a5 bm.rng = #ax bm.rng', 'scoreboard players operation #a5 bm.rng *= #5 bm.p177',
                            'scoreboard players operation #z5 bm.rng = #az bm.rng', 'scoreboard players operation #z5 bm.rng *= #5 bm.p177',
                            'scoreboard players operation #a2 bm.rng = #ax bm.rng', 'scoreboard players operation #a2 bm.rng *= #2 bm.p177',
                            'scoreboard players operation #z2 bm.rng = #az bm.rng', 'scoreboard players operation #z2 bm.rng *= #2 bm.p177',
                            'data modify storage bm:ui p177.ns set value ""', 'data modify storage bm:ui p177.ew set value ""', 'data modify storage bm:ui p177.j set value ""',
                            'execute unless score #a5 bm.rng < #z2 bm.rng if score #dx bm.rng matches 1.. run data modify storage bm:ui p177.ew set value "east"',
                            'execute unless score #a5 bm.rng < #z2 bm.rng if score #dx bm.rng matches ..-1 run data modify storage bm:ui p177.ew set value "west"',
                            'execute unless score #z5 bm.rng < #a2 bm.rng if score #dz bm.rng matches 1.. run data modify storage bm:ui p177.ns set value "south"',
                            'execute unless score #z5 bm.rng < #a2 bm.rng if score #dz bm.rng matches ..-1 run data modify storage bm:ui p177.ns set value "north"',
                            'execute unless score #a5 bm.rng < #z2 bm.rng unless score #z5 bm.rng < #a2 bm.rng run data modify storage bm:ui p177.j set value "-"',
                            'scoreboard players operation #ax bm.rng > #az bm.rng', 'execute store result storage bm:ui p177.m int 1 run scoreboard players get #ax bm.rng',
                            'function bm:p177/compass_say with storage bm:ui p177'])
    fn('p177/compass_say', ['$' + title('@s', 'actionbar', [T('The needle shivers ', 'gray'), T('$(ns)$(j)$(ew)', DREAD, bold=True),
                                                            T(' - something Dread, ~$(m) blocks.', 'gray')])])
    # the Bottomless Bucket: poured out, it fills itself again
    tick += ['tag @a remove bm.bbh2', 'tag @a[tag=bm.bbh] add bm.bbh2', 'tag @a remove bm.bbh',
             f'execute as @a if items entity @s weapon.mainhand {holds("bottomless_bucket")} run tag @s add bm.bbh',
             'execute as @a[tag=bm.bbh2,scores={bm.bbu=1..}] if items entity @s weapon.mainhand minecraft:bucket run function bm:p177/bucket',
             'scoreboard players reset @a[scores={bm.bbu=1..}] bm.bbu']
    fn('p177/bucket', [f'item replace entity @s weapon.mainhand with {G.item_arg("bottomless_bucket")}', 'tag @s add bm.bbh'])
    # the Harvest Scythe: ripe crops within 3 blocks reaped and replanted
    HOLD['harvest_scythe'] = 'bm:p177/scythe'
    crops = [('wheat', 7), ('carrots', 7), ('potatoes', 7), ('beetroots', 3), ('nether_wart', 3)]
    reap = []
    for dx in range(-3, 4):
        for dz in range(-3, 4):
            for dy in (0, -1):
                for c, a in crops:
                    reap.append(f'execute positioned ~{dx} ~{dy} ~{dz} if block ~ ~ ~ minecraft:{c}[age={a}] run function bm:p177/reap/{c}')
    fn('p177/scythe', ['execute if score @s bm.dkcd matches 1.. run return 0', 'scoreboard players set @s bm.dkcd 1', 'scoreboard players set #rp bm.rng 0'] + reap +
       ['execute if score #rp bm.rng matches 0 run ' + say('Nothing ripe within 3 blocks.', 'gray'),
        'execute if score #rp bm.rng matches 1.. run playsound minecraft:item.hoe.till player @a[distance=..12] ~ ~ ~ 1 0.8'])
    for c, a in crops:
        fn(f'p177/reap/{c}', ['loot spawn ~ ~0.5 ~ mine ~ ~ ~ minecraft:netherite_hoe', f'setblock ~ ~ ~ minecraft:{c}[age=0]', 'scoreboard players add #rp bm.rng 1',
                              'particle minecraft:happy_villager ~ ~0.4 ~ 0.2 0.2 0.2 0 3'])
    second.append('scoreboard players remove @a[scores={bm.dkcd=1..}] bm.dkcd 1')
    # the Mender's Altar and the Dread Lantern: set down, picked up, at work
    PLACED = {'menders_altar': ('bm.malt', "Mender's Altar"), 'dread_lantern': ('bm.dlan', 'Dread Lantern')}
    for iid, (tag, nm) in PLACED.items():
        placeable(G, 'p177', iid, tag)
    second += ['execute as @e[type=minecraft:marker,tag=bm.maltm] at @s as @a[distance=..5,gamemode=!spectator] run function bm:p177/mend',
               'execute as @e[type=minecraft:marker,tag=bm.maltm] at @s if entity @a[distance=..5] run particle minecraft:happy_villager ~ ~0.8 ~ 0.3 0.2 0.3 0 2',
               'execute as @e[type=minecraft:marker,tag=bm.dlanm] at @s run particle minecraft:soul_fire_flame ~ ~0.7 ~ 0.08 0.1 0.08 0.005 1']
    mend = {'function': 'minecraft:set_damage', 'damage': 0.015, 'add': True}
    wjson('bm/item_modifier/p177/mend.json', mend)
    fn('p177/mend', [f'item modify entity @s {sl} bm:p177/mend' for sl in ('armor.head', 'armor.chest', 'armor.legs', 'armor.feet', 'weapon.mainhand', 'weapon.offhand')])
    # (no monster rises within 48 blocks of a Dread Lantern: a monster first seen there is gone before it acts)
    import gen_dp as _G
    for t in list(G.ARMORED) + list(G.UNARMORED):
        L = G.FUNCS[f'mobs/init/{t}']
        L.insert(1, 'execute if entity @e[type=minecraft:marker,tag=bm.dlanm,distance=..48] unless data entity @s CustomName unless entity @s[tag=bm.minion] run return run function bm:p177/lantern_ward')
    fn('p177/lantern_ward', ['tp @s ~ -200 ~', 'kill @s'])
    G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/dread_tokens', 'yellow'), T('  gives you 10 Dread Tokens', 'gray')]))
    fn('admin/dread_tokens', [f'give @s {G.item_arg("dread_token")} 10'])



def placeable(G, ns, iid, tag, scale=0.9, sound='minecraft:block.stone'):
    """A thing set down on a block (sneak + use) and picked back up (punch it): its display (tag+'d'), its click box (tag) and a
    marker (tag+'m') where it works. Functions under <ns>/pl/<iid>."""
    fn, give = G.fn, G.give
    say = lambda txt: G.title('@s', 'actionbar', T(txt, 'gray'))
    ident = [F(0), F(0), F(0), F(1)]
    fast = G.FUNCS['loop/fast']
    HOLD[iid] = f'bm:{ns}/pl/{iid}'
    fn(f'{ns}/pl/{iid}', ['execute unless predicate bm:p20/sneaking run return run ' + say('Sneak + use on a block to set it down.'),
                          'scoreboard players set #placed bm.rng 0', 'scoreboard players set #ray bm.rng 25', 'tag @s add bm.placer',
                          f'execute anchored eyes positioned ^ ^ ^ run function bm:{ns}/pl/{iid}_ray', 'tag @s remove bm.placer',
                          'execute if score #placed bm.rng matches 0 run return run ' + say('Look at the top of a block within 5 blocks.'),
                          'execute unless entity @s[gamemode=creative] run item replace entity @s weapon.mainhand with minecraft:air'])
    fn(f'{ns}/pl/{iid}_ray', [f'execute unless block ~ ~ ~ #minecraft:replaceable run return run function bm:{ns}/pl/{iid}_hit',
                              'scoreboard players remove #ray bm.rng 1', f'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:{ns}/pl/{iid}_ray'])
    disp = {'Tags': [f'{tag}d', 'bm.plnew'], 'item_display': 'fixed', 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:{iid}'}},
            'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.45), F(0)], 'scale': [F(scale)] * 3},
            'brightness': {'block': Int(12), 'sky': Int(12)}}
    fn(f'{ns}/pl/{iid}_hit', ['execute align xyz positioned ~0.5 ~1 ~0.5 unless block ~ ~ ~ #minecraft:replaceable run return 0',
                              f'execute align xyz positioned ~0.5 ~1 ~0.5 if entity @e[type=minecraft:interaction,tag={tag},distance=..0.6] run return 0',
                              f'execute align xyz positioned ~0.5 ~1 ~0.5 run summon minecraft:item_display ~ ~ ~ {snbt(disp)}',
                              f'execute align xyz positioned ~0.5 ~1 ~0.5 run summon minecraft:interaction ~ ~ ~ {{Tags:["{tag}","bm.plnew"],width:0.8f,height:0.9f,response:1b}}',
                              f'execute align xyz positioned ~0.5 ~1 ~0.5 run summon minecraft:marker ~ ~ ~ {{Tags:["{tag}m","bm.plnew"]}}',
                              'tag @e[tag=bm.plnew] remove bm.plnew', 'scoreboard players set #placed bm.rng 1',
                              f'playsound {sound}.place block @a[distance=..16] ~ ~ ~ 1 0.8'])
    fast.append(f'execute as @e[type=minecraft:interaction,tag={tag}] if data entity @s attack at @s run function bm:{ns}/pl/{iid}_pick')
    fast.append(f'execute as @e[type=minecraft:interaction,tag={tag}] if data entity @s interaction run data remove entity @s interaction')
    fn(f'{ns}/pl/{iid}_pick', [f'execute on attacker run {give(iid)}', f'kill @e[type=minecraft:item_display,tag={tag}d,distance=..0.6]',
                               f'kill @e[type=minecraft:marker,tag={tag}m,distance=..0.6]', f'playsound {sound}.break block @a[distance=..16] ~ ~ ~ 1 0.8', 'kill @s'])
    G.FUNCS['admin/uninstall'][0:0] = [f'kill @e[tag={tag}]', f'kill @e[tag={tag}d]', f'kill @e[tag={tag}m]']

def rp(R):
    g = R.grid
    R.ICONS['dread_token'] = g(['................', '.....kkkkkk.....', '....kRRRRRRk....', '...kRrrrrrrRk...', '..kRrwwrrwwrRk..', '..kRrwkrrwkrRk..', '..kRrrrrrrrrRk..',
                                '..kRrrwwwwrrRk..', '..kRrrwrwwrrRk..', '..kRrrrrrrrrRk..', '...kRrrrrrrRk...', '....kRRRRRRk....', '.....kkkkkk.....', '................',
                                '................', '................'],
                               dict(k='#1a0205', R='#5a0812', r='#b0102a', w='#e8d0c0'))
    R.ICONS['auction_writ'] = g(['................', '...pppppppppp...', '..pWWWWWWWWWWp..', '..pWkkkkkkkkWp..', '..pWWWWWWWWWWp..', '..pWkkkkkWWWWp..', '..pWWWWWWWWWWp..',
                                 '..pWkkkkkkkWWp..', '..pWWWWWWWWWWp..', '..pWWWWWWrrWWp..', '..pWWWWWrRRrWp..', '..pWWWWWWrrWWp..', '...pppppppppp...', '........y.......',
                                 '.......yy.......', '................'],
                                dict(p='#8a6a3a', W='#f0e4c0', k='#4a3a2a', r='#a01010', R='#e02020', y='#ffcf40'))
    R.ICONS['serpent_summons'] = g(['................', '.......ss.......', '......s..s......', '.....s....s.....', '.....s....s.....', '......s..s......', '.......gg.......',
                                    '......gGGg......', '.....gGkkGg.....', '.....gGkkGg.....', '.....gGGGGg.....', '......gGGg......', '.......gg.......', '................',
                                    '................', '................'],
                                   dict(s='#c0c8d0', g='#0a3a1a', G='#3ad06a', k='#0a1a0a'))
    R.ICONS['hollow_echo'] = g(['................', '................', '..p..p....p..p..', '..pp.pp..pp.pp..', '..ppppp..ppppp..', '..pPPPPPPPPPPp..', '..pP........Pp..',
                                '..pP..wwww..Pp..', '..pP..w..w..Pp..', '..pP..wwww..Pp..', '..pP........Pp..', '..pPPPPPPPPPPp..', '..pppppppppppp..', '................',
                                '................', '................'],
                               dict(p='#4a2a7a', P='#9a5ae0', w='#e8d8ff'))
    R.ICONS['tome_eternity'] = g(['................', '..bbbbbbbbbbb...', '..bGGGGGGGGGbw..', '..bGyyyyyyyGbw..', '..bGy.....yGbw..', '..bGy.yyy.yGbw..', '..bGy.y.y.yGbw..',
                                  '..bGy.yyy.yGbw..', '..bGy.....yGbw..', '..bGyyyyyyyGbw..', '..bGGGGGGGGGbw..', '..bbbbbbbbbbbw..', '...wwwwwwwwwww..', '................',
                                  '................', '................'],
                                 dict(b='#5a3a1a', G='#8a5a2a', y='#ffd870', w='#f0e8d0'))
    R.ICONS['menders_altar'] = g(['................', '................', '......gggg......', '.....gGGGGg.....', '......gggg......', '................', '...ssssssssss...',
                                  '...sSSSSSSSSs...', '....sSSSSSSs....', '.....sSSSSs.....', '.....sSSSSs.....', '....sSSSSSSs....', '...ssssssssss...', '................',
                                  '................', '................'],
                                 dict(g='#2a8a6a', G='#7ad8b0', s='#4a4a52', S='#8a8a96'))
    R.ICONS['dread_lantern'] = g(['................', '.......kk.......', '......k..k......', '.....kkkkkk.....', '.....kRrrRk.....', '.....kryyrk.....', '.....krYYrk.....',
                                  '.....kryyrk.....', '.....kRrrRk.....', '.....kkkkkk.....', '................', '................', '................', '................',
                                  '................', '................'],
                                 dict(k='#1a1a22', R='#5a0812', r='#b0102a', y='#ff6a40', Y='#ffe0a0'))
    R.ICONS['dawn_hourglass'] = g(['................', '....oooooooo....', '.....g....g.....', '.....gyyyyg.....', '......gyyg......', '.......yg.......', '.......gy.......',
                                   '......g..g......', '.....g.yy.g.....', '.....gyyyyg.....', '....oooooooo....', '................', '................', '................',
                                   '................', '................'],
                                  dict(o='#8a5a2a', g='#c8e8ff', y='#ffd27a'))
    R.ICONS['dread_compass'] = g(['................', '.....kkkkkk.....', '....kssssssk....', '...kss.rr.ssk...', '...ks..rr..sk...', '...ks..rr..sk...', '...ks..kk..sk...',
                                  '...ks..ww..sk...', '...ks..ww..sk...', '...kss.ww.ssk...', '....kssssssk....', '.....kkkkkk.....', '................', '................',
                                  '................', '................'],
                                 dict(k='#1a1a22', s='#6a6a72', r='#b0102a', w='#d8d8d8'))

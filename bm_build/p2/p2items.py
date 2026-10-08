"""Phase 2 items. Importing this registers them in items.ITEMS (only in a --phase2 build)."""
import items as I
from items import item, gear, attr, ench, T, TOTEM, consumable, weapon_attrs, armor_attrs, PRICES, ARMOR_SLOT
from p2.config import D, ORDER

# ===================================================================== BOSS KEYS (sold by The Fence)
KEYS = {
    'brood': ('Silkbound Key', '#c9d6a3', ['Sticky. Smells of old mutton.'], ('token', 16)),
    'frost': ('Rimeglass Key', '#a8d8ff', ['Cold enough to burn.'], ('token', 28)),
    'tide': ('Coral Throne Key', '#2fa39b', ['Still dripping, somehow.'], ('medallion', 4)),
    'hex': ('Hexed Key', '#b06be0', ['It whispers when no one is holding it.'], ('medallion', 6)),
    'keep': ("Wilfrey's Signet", '#c0392b', ['The seal of a kind lord,', 'stolen by an unkind cousin.'], ('trophy', 2)),
}
for d, (name, color, lore, price) in KEYS.items():
    item(f'key_{d}', TOTEM, name, color,
         lore + [(f'Summons {D[d]["boss"]} at the altar of', 'gray'), (D[d]['title'] + '.', 'gray'),
                 ('Consumed when used. Requires every', 'dark_gray'), ('earlier conquest on your record.', 'dark_gray')],
         model=f'bm:key_{d}', glint=True, stack=16, cat='p2key', price=price)

# ===================================================================== SEALED DUNGEON MAPS
MAPS = {'brood': ("Sealed Nest Map", 'Marks the nearest Broodmother\'s Nest.'),
        'frost': ("Sealed Spire Map", 'Marks the nearest Frostbound Spire.'),
        'tide': ("Sealed Tidal Chart", 'Marks the nearest Sunken Throne.'),
        'hex': ("Sealed Hexed Map", 'Marks the nearest Hexbound Cathedral.'),
        'keep': ("Sealed Keep Map", "Marks the nearest Wilfrey's Keep.")}
for d, (name, lore) in MAPS.items():
    item(f'sealed_map_{d}', TOTEM, name, D[d]['color'], ['Hold right-click to break the seal.', lore],
         model='minecraft:map', glint=True, stack=16,
         comps={'minecraft:consumable': consumable(0.8, 'none', 'minecraft:item.book.page_turn', False)}, cat='p2map')

item('hollow_summons', TOTEM, 'Shard of the Hollow Throne', '#7f8c9d',
     ['A splinter of a throne beyond the world.', ('It is crumbling. Use it: it reforms', 'gray'),
      ('as a Hollow Gate.', 'gray')],
     model='bm:hollow_summons', glint=True,
     comps={'minecraft:consumable': consumable(2.5, 'toot_horn', 'minecraft:particle.soul_escape', True)}, cat='p2map')

item('hollow_warpstone', TOTEM, 'Warpstone of the Hollow Throne', '#e5e4e2',
     ['The Hollow King\'s own key, taken from his throne.', ('Use it anywhere to step into the Hollow Throne;', 'gray'),
      ('use it there to return where you came from.', 'gray'), ('Never used up. 10 s cooldown.', 'dark_gray')],
     model='bm:hollow_summons', glint=True, stack=1, bold=True,
     comps={'minecraft:consumable': consumable(1.2, 'toot_horn', 'minecraft:block.respawn_anchor.set_spawn', False)}, cat='p2map')
item('wilfrey_locket', TOTEM, "Wilfrey's Locket", '#f4f4f4',
     ['A silver locket from a quiet grave.', ('Use it to call Wilfrey, the Kind Lord, to your side.', 'gray'),
      ('Use it again to call him back to you;', 'gray'), ('sneak + use to let him rest.', 'gray'),
      ('If he falls, his spirit needs 30 minutes.', 'dark_gray')],
     model='bm:wilfrey_locket', glint=True, stack=1, bold=True,
     comps={'minecraft:consumable': consumable(1.0, 'none', 'minecraft:block.amethyst_block.resonate', False)}, cat='p2emblem')

# ===================================================================== CONQUEST EMBLEMS
# Each emblem carries a numeral. The Hollow Throne's keypad wants the five numerals in conquest order.
EMBLEM_NUM = {'brood': 4, 'frost': 7, 'tide': 1, 'hex': 9, 'keep': 3}
ROMAN = {1: 'I', 3: 'III', 4: 'IV', 7: 'VII', 9: 'IX'}
for d in ORDER:
    if d == 'hollow':
        item('emblem_hollow', TOTEM, 'Crown of Conquest', '#e5e4e2',
             ['Proof that the Hollow King has fallen.', ('Every seal broken. Every throne empty.', 'gray')],
             model='bm:emblem_hollow', glint=True, stack=1, bold=True, cat='p2emblem')
        continue
    item(f'emblem_{d}', TOTEM, f'Conquest Emblem: {D[d]["boss"]}', D[d]['color'],
         [f'Proof of victory over {D[d]["boss"]}.', (f'An old numeral is cut into the back: {ROMAN[EMBLEM_NUM[d]]}', 'dark_gray')],
         model=f'bm:emblem_{d}', glint=True, stack=1, bold=True, cat='p2emblem')

# ===================================================================== VAULT KEYS
VKEY = {'brood': 'Nest Key', 'frost': 'Rime Key', 'tide': 'Coral Key', 'hex': 'Grimoire Key', 'keep': 'Keep Key',
        'hollow': 'Hollow Key', 'lucky': 'Gilded Key'}
for d, name in VKEY.items():
    item(f'vkey_{d}', 'minecraft:trial_key', name, D[d]['color'],
         [f'Opens the spoils vault of {D[d]["title"]}.', ('Dropped by its trial spawners.', 'dark_gray')],
         model=f'bm:vkey_{d}', stack=16, cat='p2vkey')
    item(f'bkey_{d}', 'minecraft:ominous_trial_key', f"Victor's Key: {D[d]['boss']}", D[d]['color'],
         [f'Opens the victor\'s vault in {D[d]["title"]}.', ('Earned by defeating its master.', 'dark_gray')],
         model=f'bm:bkey_{d}', glint=True, stack=16, cat='p2vkey')

# ===================================================================== PLACEABLE BOSS TROPHIES (victor's vaults, 2.1)
for d in D:
    item(f'trophy_{d}', TOTEM, f'{D[d]["boss"]} Trophy', D[d]['color'],
         [f'Proof you conquered {D[d]["title"]}.', ('Use it on a block to set it on top.', 'gray'),
          ('Right-click it to turn it; punch it', 'dark_gray'), ('to pick it back up.', 'dark_gray')],
         model=f'bm:trophy3d_{d}', stack=16, cat='p2emblem',
         comps={'minecraft:consumable': consumable(0.35, 'none', 'minecraft:block.stone.place', False)})

# ===================================================================== PUZZLE PROPS
for k, (nm, col) in enumerate([('Pearl Sigil of the Moon', '#dfe6f0'), ('Pearl Sigil of the Tide', '#5fd1c8'),
                               ('Pearl Sigil of the Deep', '#1f4e79')], 1):
    item(f'pearl_sigil_{k}', TOTEM, nm, col, ['One of three sigils the Tyrant demands.', ('Drop it on the tribute altar.', 'gray')],
         model=f'bm:pearl_sigil_{k}', glint=True, stack=1, cat='p2prop')

# ===================================================================== CUSTOM ENCHANTMENTS USED BY ITEMS (defined in logic)
# bm:venom (poison), bm:frostbite (slow + freeze), bm:arcane (levitation), bm:fortune_favor (luck XP)

# ===================================================================== BOSS DROPS
gear('broodfang', 'netherite_sword', 'Broodfang', '#7d8f3a',
     ['A fang the size of a forearm.', ('Poisons whatever it cuts.', 'blue')],
     {**ench(sharpness=7, bane_of_arthropods=8, looting=4, sweeping_edge=4, unbreaking=6, mending=1), 'bm:venom': 1}, 3,
     attrs=weapon_attrs('netherite_sword', 2))
gear('frost_longbow', 'bow', 'Rimefall Longbow', '#a8d8ff',
     ['Strung with frozen sinew.', ('Arrows slow and freeze their target.', 'blue')],
     {**ench(power=8, punch=2, infinity=1, unbreaking=6, mending=1), 'bm:frostbite': 1}, 3)
gear('tyrant_trident', 'trident', "Tyrant's Tide", '#2fa39b',
     ['It returns. It always returns.', ('+2 Attack Damage', 'blue')],
     ench(impaling=8, loyalty=3, channeling=1, unbreaking=6, mending=1), 3, attrs=weapon_attrs('trident', 2))
gear('archmage_staff', 'mace', "Archmage's Grimstaff", '#9b59d0',
     ['Heavier than it looks. Angrier, too.', ('Struck foes float helplessly.', 'blue')],
     {**ench(density=5, breach=4, wind_burst=2, unbreaking=6, mending=1), 'bm:arcane': 1}, 3, model='minecraft:breeze_rod')
gear('bobbery_axe', 'netherite_axe', "Bobbery's Axe", '#5b3a3a',
     ['The general\'s own axe. Every edge enchanted', 'to the sixth degree.', ('+2 Attack Damage', 'blue')],
     ench(sharpness=6, smite=6, bane_of_arthropods=6, fire_aspect=6, looting=6, efficiency=6, unbreaking=6, mending=1), 3,
     attrs=weapon_attrs('netherite_axe', 2), bold=True)

# ===================================================================== HIDDEN THEMED GEAR (secret rooms)
gear('silkstrider_boots', 'diamond_boots', 'Silkstrider Boots', '#c9d6a3',
     ['Woven from Broodmother silk.', ('Softer landings, quieter steps, higher jumps', 'blue')],
     ench(feather_falling=6, protection=5, unbreaking=6, mending=1), 2,
     attrs=armor_attrs('diamond', 'boots', [attr('safe_fall_distance', 6, 'feet'), attr('sneaking_speed', 0.3, 'feet'),
                                            attr('jump_strength', 0.05, 'feet'), attr('movement_speed', 0.05, 'feet', 'add_multiplied_base')]))
gear('frostwarden_hood', 'leather_helmet', 'Frostwarden Hood', '#dff3ff',
     ['Lined with stray fur. Never freezes.', ('+2 Max Health, immune to powder snow', 'blue')],
     ench(protection=6, unbreaking=8, mending=1), 2,
     attrs=[attr('armor', 3, 'head', ident='minecraft:armor.helmet'), attr('max_health', 2, 'head')],
     extra={'minecraft:dyed_color': 0xDFF3FF})
gear('abyssal_helm', 'turtle_helmet', 'Abyssal Diving Helm', '#2fa39b',
     ['Salvaged from a drowned captain.', ('+4 Oxygen, fast underwater mining & swimming', 'blue')],
     ench(respiration=5, aqua_affinity=1, protection=5, unbreaking=6, mending=1), 2,
     attrs=[attr('armor', 3, 'head', ident='minecraft:armor.helmet'), attr('oxygen_bonus', 4, 'head'),
            attr('submerged_mining_speed', 1.0, 'head'), attr('water_movement_efficiency', 0.2, 'head')])
gear('hexwoven_robe', 'leather_chestplate', 'Hexwoven Robe', '#9b59d0',
     ['Stitched with warding runes.', ('+4 Max Absorption, Protection VII', 'blue')],
     ench(protection=7, unbreaking=8, mending=1), 2,
     attrs=[attr('armor', 7, 'chest', ident='minecraft:armor.chestplate'), attr('armor_toughness', 2, 'chest'),
            attr('max_absorption', 4, 'chest')], extra={'minecraft:dyed_color': 0x3B1F5C})
item('blink_tome', TOTEM, 'Tome of Blinking', '#b06be0',
     ['Use to blink a short way forward.', ('Only works outside dungeons.', 'gray'), ('8 second cooldown.', 'dark_gray')],
     model='minecraft:enchanted_book', glint=True,
     comps={'minecraft:consumable': consumable(0.4, 'none', 'minecraft:entity.enderman.teleport', False),
            'minecraft:use_cooldown': {'seconds': 8.0, 'cooldown_group': 'bm:blink'}}, cat='p2hidden')
gear('oathblade', 'netherite_sword', "Wilfrey's Oathblade", '#e8e8ff',
     ['"I chose the world."', ('+3 Attack Damage', 'blue')],
     ench(smite=10, sharpness=6, knockback=2, looting=4, unbreaking=10, mending=1), 3, attrs=weapon_attrs('netherite_sword', 3), bold=True)
item('wilfrey_aegis', 'minecraft:shield', "Wilfrey's Aegis", '#e8e8ff',
     ['It held the line against the Hollow King.', ('+2 Armor, +30% Knockback Resistance in off hand', 'blue')],
     comps={'minecraft:enchantments': ench(unbreaking=10, mending=1),
            'minecraft:attribute_modifiers': [attr('armor', 2, 'offhand'), attr('knockback_resistance', 0.3, 'offhand')]},
     tier=3, cat='p2hidden')
gear('hollow_crown', 'netherite_helmet', 'Crown of the Hollow King', '#e5e4e2',
     ['It is lighter than it should be.', ('+4 Max Health, sees in the dark', 'blue')],
     ench(protection=8, unbreaking=10, mending=1), 3,
     attrs=armor_attrs('netherite', 'helmet', [attr('max_health', 4, 'head')], bonus_tough=2), model='bm:crown', bold=True,
     custom_extra={'bm_fx': 'hollow_crown'})
item('horseshoe_charm', TOTEM, 'Lucky Horseshoe', '#ffd700',
     ['Hold in your off hand.', ('+3 Luck, +5% Speed', 'blue')], model='bm:horseshoe',
     comps={'minecraft:attribute_modifiers': [attr('luck', 3, 'offhand'), attr('movement_speed', 0.05, 'offhand', 'add_multiplied_base')]},
     cat='p2hidden')

# ===================================================================== LUCKY: TROPHY, FORTUNA, MAP FRAGMENTS
item('lucky_trophy', TOTEM, 'Lucky Trophy', '#ffd700',
     ['Taken from the Golden Goose itself.', ('Lucky Whiskers will trade you', 'gray'), ('something legendary for it.', 'gray')],
     model='bm:lucky_trophy', glint=True, stack=16, bold=True, cat='p2lucky')
gear('fortuna', 'netherite_sword', "Fortuna's Favor", '#ffd700',
     ['Luck is a weapon. This one is sharp.', ('+5 Luck and +2 Attack Damage while held', 'blue')],
     ench(sharpness=8, looting=7, sweeping_edge=5, unbreaking=8, mending=1), 3,
     attrs=weapon_attrs('netherite_sword', 2, [attr('luck', 5, 'mainhand')]), bold=True)
for k in range(1, 10):
    item(f'lucky_fragment_{k}', TOTEM, f'Lucky Map Fragment ({k}/9)', '#e8c547',
         ['A torn piece of a golden map.', ('Collect all nine, then use one', 'gray'), ('to piece the map together.', 'gray')],
         model=f'bm:lucky_fragment_{k}', stack=16,
         comps={'minecraft:consumable': consumable(0.8, 'none', 'minecraft:item.book.page_turn', False)}, cat='p2lucky')

# ===================================================================== CONQUEROR'S SET (Hollow King's vault)
CONQ_FX = {'helmet': 'Night Vision, Water Breathing', 'chestplate': 'Strength I, Resistance I',
           'leggings': 'Regeneration I, Haste I', 'boots': 'Speed I, Fire Resistance'}
CONQ_ARMOR = {'helmet': (4, 'Visage'), 'chestplate': (10, 'Aegis'), 'leggings': (8, 'Greaves'), 'boots': (4, 'Treads')}
for p, (armor, nm) in CONQ_ARMOR.items():
    s = ARMOR_SLOT[p]
    gear(f'conq_{p}', f'netherite_{p}', f"Conqueror's {nm}", '#e5e4e2',
         ['Forged from the Hollow King\'s throne.', (f'While worn: {CONQ_FX[p]}', 'blue'), ('+4 Max Health. Unbreakable.', 'blue'),
          ('Full set: the dead keep their distance.', 'dark_aqua')],
         {**ench(protection=10, thorns=3), **({'boots': ench(feather_falling=6), 'helmet': ench(respiration=5),
                                               'leggings': ench(swift_sneak=5)}.get(p, {}))},
         3, attrs=[attr('armor', armor, s, ident=f'minecraft:armor.{p}'), attr('armor_toughness', 5, s, ident=f'minecraft:armor.{p}_toughness'),
                   attr('knockback_resistance', 0.2, s, ident=f'minecraft:armor.{p}_kb'), attr('max_health', 4, s)],
         extra={'minecraft:unbreakable': {}, 'minecraft:trim': {'material': 'minecraft:quartz', 'pattern': 'minecraft:silence'}},
         custom_extra={'bm_set': 'conqueror'}, bold=True)
CONQ_TOOLS = [('conq_blade', 'netherite_sword', "Conqueror's Blade",
               ench(sharpness=10, smite=10, bane_of_arthropods=10, looting=6, fire_aspect=3, sweeping_edge=6, knockback=2), 'netherite_sword', 5),
              ('conq_pick', 'netherite_pickaxe', "Conqueror's Pick", ench(efficiency=10, fortune=6), 'netherite_pickaxe', 0),
              ('conq_axe', 'netherite_axe', "Conqueror's Axe", ench(sharpness=10, efficiency=10, smite=8), 'netherite_axe', 4),
              ('conq_shovel', 'netherite_shovel', "Conqueror's Spade", ench(efficiency=10, fortune=4), None, 0),
              ('conq_bow', 'bow', "Conqueror's Longbow", ench(power=10, punch=3, flame=2, infinity=1), None, 0)]
for iid, base, nm, en, wb, bonus in CONQ_TOOLS:
    held = {'conq_pick': 'Haste II while held', 'conq_shovel': 'Haste II while held', 'conq_blade': 'Strength I while held',
            'conq_axe': 'Strength I while held', 'conq_bow': 'Speed I while held'}[iid]
    gear(iid, base, nm, '#e5e4e2', ['Forged from the Hollow King\'s throne.', (held + '. Unbreakable.', 'blue')], en, 3,
         attrs=weapon_attrs(wb, bonus) if wb else None, extra={'minecraft:unbreakable': {}}, custom_extra={'bm_held': iid}, bold=True)

# ===================================================================== LORE BOOKS (boss drops)
LORE = {
    'brood': ('Silk and Bone', 'A Velvet Hand Courier', [
        "Delivery log, Velvet Hand.\n\nThe nest under the old forest makes a fine vault. Nobody robs a spider. The big one, the Broodmother, takes her fee in mutton and leaves our crates alone.",
        "Strange visitor tonight. A wither skeleton in black iron, taller than a door. Called himself General Bobbery. Paid in gold that smelled of brimstone, and wanted every crate we had sent north, to the ice.",
        "The Broodmother hisses whenever his name comes up. I don't blame her.\n\nIf this log is found: the north crates went to a tower in the snow. A marksman guards it. Don't.",
        "P.S. Found tiny tracks in the egg chamber again. Rat-sized. Wearing boots?"]),
    'frost': ("The Huntsman's Oath", 'The Frost Marksman', [
        "I swore an oath to Bobbery when the snows were young: watch the north road, and shoot anything that is not a skeleton.",
        "I have kept it for two hundred winters. My fingers are frozen to the string now. I could not let go if I wished.",
        "His treasure fleet sails from a drowned temple in the deep. The Tyrant takes a tithe of every ship. If you have beaten me, you will meet him next. He is less polite.",
        "Something keeps stealing my arrows. The fletching comes back nibbled."]),
    'tide': ("The Tyrant's Ledger", 'The Drowned Tyrant', [
        "Ledger of the Sunken Throne.\n\nTithe from General Bobbery: 40 crates gold, 12 crates diamonds, 1 crate cheese (?).\nTithe owed to the Cathedral: half of everything.",
        "The Archmage demands more every tide. He speaks of a 'Hollow Pact', and of a king who sleeps beyond the world. The sea goes quiet when he says it. I do not like that.",
        "Note: cheese crate missing. Small wet footprints lead to the vents. Investigate rats."]),
    'hex': ('The Hollow Pact', 'The Archmage', [
        "Before the Velvet Hand, before the markets, there was a war. The Hollow King, eldest of the wither-born, marched on the Overworld to make it one great graveyard.",
        "His own grandson stood against him. Wilfrey, the gentle one, who liked flowers and villagers, led the living and sealed the King away on a throne beyond the world.",
        "Wilfrey's cousin Bobbery never forgave him. He took Wilfrey's keep in the dark forest, and he pays me to find the way back to the Hollow Throne.",
        "The way is five seals: five numerals, spoken in the order they were broken. I have hidden mine on the back of my emblem. The others you must earn."]),
    'keep': ("Wilfrey's Last Letter", 'Wilfrey', [
        "To whoever stands in my hall,\n\nIf you are reading this, my cousin has fallen. I am glad of it, and I am sorry too. Bobbery was not always cruel.",
        "We were boys in the Nether together. He laughed louder than anyone. When Grandfather marched, Bobbery chose the crown and I chose the world. I sealed Grandfather away. Bobbery never forgave me.",
        "He came for my keep when I was old and tired. I did not fight him. I hid the way to the Hollow Throne in a gate of old stone, and the gate is yours now. Set the five emblems in it.",
        "Speak the five numerals at his door, in the order you earned them. Grandfather will wake. Do not let him leave.\n\nBe kind to the rats. They were the only ones who visited.\n\n- Wilfrey"]),
    'hollow': ('The Crown Unmade', 'Unknown', [
        "The Hollow King is broken. The throne is cold. Somewhere, a gentle wither skeleton rests easier than he has in a thousand years.",
        "As for the Crown of the Hollow King: it was right here a moment ago.\n\nThe rats are very sorry.\n\nThe rats are not sorry."]),
    'lucky': ('The Golden Ledger', 'Lucky Whiskers', [
        "Every rat knows the story of the Roost: a goose that lays nothing but luck, and a jockey who never once lost a bet.",
        "Nobody has a map. Nobody ever will, unless they find the nine pieces we hid. We hid them very well.\n\nWe also lost three. Good luck!"]),
}
for d, (title, author, pages) in LORE.items():
    # registered directly (items.book() would also list them for sale at the Professor - these are boss drops only)
    content = {'title': title, 'author': author, 'pages': [{'text': pg} for pg in pages]}
    I.ITEMS[f'lore_{d}'] = {'base': 'minecraft:written_book', 'custom': {'bm': f'lore_{d}'}, 'name': title,
                            'comps': {'minecraft:written_book_content': content,
                                      'minecraft:custom_data': {'bm': f'lore_{d}', 'bmv': I.ITEM_VERSION}}}
    I.CATEGORY[f'lore_{d}'] = 'p2lore'

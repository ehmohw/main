"""2.99: THE VORN ARMADA's items (registered on import - p2/armadacfg imports this, so the builder's vaults can name their keys).
What they do is phase241's (the fleet), phase242's (the Admiral's spoils, the Starforged set) and phase243's (Vexis).

THE STARFORGED SET - the top tier of alien gear, above Zorp's Warplate: worked at the Starforge bench aboard the Armada's Dock
from a Warplate piece, Star-Cores and red Xenite (phase242)."""
from items import item, gear, attr, ench, T, TOTEM, consumable, weapon_attrs, ARMOR_SLOT
import armada_lore as L

N = lambda k: L.ITEMS[k][0]
LO = lambda k: list(L.ITEMS[k][1])
GREEN, RED, STAR = L.VX_COL, L.RED, L.STAR
SF = '#ffb14a'                                 # (Starforged gold-orange)

# ---- the way in
item('hive_coords', 'minecraft:paper', N('coords'), STAR, LO('coords') + [('Hard mode.', 'dark_gray')], model='bm:hive_coords', glint=True, stack=1,
     cat='map', comps={'minecraft:consumable': consumable(1.6, 'spyglass', 'minecraft:block.beacon.activate', False)})
for k in (1, 2, 3):
    item(f'cipher_{k}', TOTEM, N(f'cipher_{k}'), GREEN, LO(f'cipher_{k}') + [('Drop it (Q) on its slot at the Command Lock.', 'gray')],
         model=f'bm:cipher_{k}', glint=True, stack=1, cat='p2prop')
item('hive_sigil', TOTEM, N('hive_sigil'), '#9adf8a', LO('hive_sigil'), model='bm:hive_sigil', stack=6, cat='p2prop')
item('akey', 'minecraft:trial_key', 'Armada Key', GREEN, ['Opens a vault aboard the Vorn Armada.', ('Each guardian, and the Command Lock, gives one.', 'dark_gray')],
     model='bm:akey', stack=16, cat='p2vkey')
item('akey_victor', 'minecraft:ominous_trial_key', "Victor's Key: Admiral Vexis", GREEN, ['Opens the victor\'s vault aboard the Flagship.', ('Earned by its fall.', 'dark_gray')],
     model='bm:akey_victor', glint=True, stack=16, cat='p2vkey')
item('star_core', TOTEM, N('star_core'), STAR, LO('star_core'), model='bm:star_core', glint=True, stack=16, cat='magic')

# ---- the hidden rooms' relics (once a player, ever)
item('squad_jetpack', TOTEM, "Zib's Squad Jetpack", L.TEAL, ['Left behind by Zib\'s lost squad.', ('In your off hand: sneak in the air for a burst upward', 'blue'),
                                                             ('(every 5 seconds). No fall damage while you hold it.', 'blue')], model='bm:squad_jetpack', stack=1, cat='magic')
item('hover_collar', TOTEM, "Specimen 117's Collar", '#e8d29a', ['Donado\'s, from before. He slipped it in the vent.', ('Carried: your followers within 16 have', 'blue'),
                                                                ('Speed and Resistance.', 'blue')], model='bm:hover_collar', stack=1, cat='magic')
item('hive_override', TOTEM, 'Hive Override Chip', GREEN, ['The Cursor dragged it out of the mainframe.', ('Use it: every Vorn within 12 freezes,', 'blue'),
                                                         ('confused, for 6 seconds (once a minute).', 'blue')], model='bm:hive_override', stack=1, cat='magic',
     comps={'minecraft:consumable': consumable(0.6, 'none', 'minecraft:block.beacon.deactivate', False)})
item('stardust_kite', TOTEM, 'Stardust Kite', '#bfe8ff', ['The Sky Buddies found it snagged on the hull.', ('In your off hand: you fall slowly, and', 'blue'),
                                                          ('see in the dark.', 'blue')], model='bm:stardust_kite', stack=1, cat='magic')
RELICS = ('squad_jetpack', 'hover_collar', 'hive_override', 'stardust_kite')

# ---- the Admiral's spoils (phase242)
gear('starfire_lance', 'netherite_sword', 'Starfire Lance', SF, ['A lance of cooled star, still burning at the tip.', ('+5 Attack Damage. A full-strength swing', 'blue'),
                                                              ('fires a bolt of starfire along your aim.', 'blue')],
     ench(sharpness=8, fire_aspect=3, looting=4, unbreaking=10, mending=1), 3, attrs=weapon_attrs('netherite_sword', 5), model='bm:starfire_lance', bold=True,
     custom_extra={'bm_fx': 'starfire_lance'})
gear('hive_breaker', 'netherite_axe', 'Hive-Breaker', RED, ['The axe that cut the hive-link.', ('+6 Attack Damage. Its blows shatter Vorn', 'blue'),
                                                          ('shields and deal double to the Vorn.', 'blue')],
     ench(sharpness=8, efficiency=6, unbreaking=10, mending=1), 3, attrs=weapon_attrs('netherite_axe', 6), model='bm:hive_breaker', bold=True,
     custom_extra={'bm_fx': 'hive_breaker'})
item('singularity_launcher', 'minecraft:crossbow', 'Singularity Launcher', '#c08aff', ['Fires a bolt that becomes a small, hungry star.', ('Where it lands, monsters within 6', 'blue'),
                                                                                    ('are dragged together and crushed.', 'blue')],
     model='bm:singularity_launcher', stack=1, cat='gear', bold=True,
     comps={'minecraft:enchantments': ench(quick_charge=3, multishot=1, unbreaking=10, mending=1)}, custom_extra={'bm_fx': 'singularity'})
gear('admiral_crown', 'netherite_helmet', "The Admiral's Crown", GREEN, ['The crown of antennae the hive spoke through.', ('+4 Max Health, +3 Toughness.', 'blue'),
                                                                      ('Vorn near you are slowed: the hive hesitates.', 'blue')],
     ench(protection=8, respiration=3, unbreaking=10, mending=1), 3, model='bm:admiral_crown', bold=True,
     attrs=[attr('armor', 3, 'head', ident='minecraft:armor.helmet'), attr('armor_toughness', 6, 'head', ident='minecraft:armor.helmet_toughness'),
            attr('max_health', 4, 'head')],
     custom_extra={'bm_fx': 'admiral_crown'}, extra={'minecraft:equippable': {'slot': 'head', 'equip_sound': 'minecraft:item.armor.equip_netherite'}})

# ---- the Starforged set (the Starforge bench, phase242): above the Warplate
SF_NAMES = {'helmet': 'Starforged Helm', 'chestplate': 'Starforged Exoplate', 'leggings': 'Starforged Greaves', 'boots': 'Starforged Thrusters'}
SF_A = {'helmet': 4, 'chestplate': 9, 'leggings': 7, 'boots': 4}
for _p, _nm in SF_NAMES.items():
    _s = ARMOR_SLOT[_p]
    _e = ench(protection=8, unbreaking=10, mending=1)
    if _p == 'helmet': _e.update(ench(respiration=3, aqua_affinity=1))
    if _p == 'boots': _e.update(ench(feather_falling=10))
    item(f'starforged_{_p}', f'minecraft:netherite_{_p}', _nm, SF,
         ['Warplate, reforged in the Hive-Star\'s heat.', ('+4 Max Health', 'blue'), ('Full set: hover-jets (you fall slowly; sneak', 'dark_aqua'),
          ('in the air for a burst) and a star-shield', 'dark_aqua'), ('that soaks a heavy blow (a minute\'s rest).', 'dark_aqua'), ('The Starforge.', 'dark_gray')],
         model=f'bm:starforged_{_p}', stack=1, cat='gear',
         comps={'minecraft:enchantments': _e,
                'minecraft:attribute_modifiers': [attr('armor', SF_A[_p], _s, ident=f'minecraft:armor.{_p}'),
                                                  attr('armor_toughness', 5, _s, ident=f'minecraft:armor.{_p}_toughness'), attr('max_health', 4, _s),
                                                  attr('knockback_resistance', 0.2, _s, ident=f'minecraft:armor.{_p}_kb')],
                'minecraft:equippable': {'slot': _s, 'asset_id': 'bm:starforged', 'equip_sound': 'minecraft:item.armor.equip_netherite'}},
         custom_extra={'bm_set': 'starforged'})

# ---- what's left of the Admiral (phase243): Vexis's summoning item
item('vexis_link', TOTEM, N('link'), GREEN, LO('link') + [('Right-click: Vexis, the Unlinked.', 'blue')], model='bm:vexis_link', glint=True, stack=1, cat='pet')

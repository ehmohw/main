"""Every custom item in the Black Market pack, defined once.
Each item -> base id + component patch. Generators turn these into loot tables,
trade offers (SNBT) and give commands."""
from nbt import B, F, D, L

NS = 'bm'
TOTEM = 'minecraft:totem_of_undying'

ITEMS = {}      # id -> dict(base, comps, custom)
DYNAMIC = set()  # 1.18: items whose custom_data/model/lore change in use (a jar's creature, a rift's charges): re-sync keeps those
PRICES = {}     # id -> (currency_id, count)  (top-tier currency paid; used for pawn refunds)
CATEGORY = {}   # id -> category label


def T(text, color='white', bold=False, italic=False, **kw):
    d = {'text': text, 'color': color, 'italic': italic}
    if bold: d['bold'] = True
    d.update(kw)
    return d


def ench(**kw):
    return {f'minecraft:{k}': int(v) for k, v in kw.items()}


def attr(kind, amount, slot, op='add_value', ident=None):
    return {'type': f'minecraft:{kind}', 'id': ident or f'bm:{kind}_{slot}',
            'amount': float(amount), 'operation': op, 'slot': slot}


WEAPON_BASE = {
    'diamond_sword': (6, -2.4), 'netherite_sword': (7, -2.4),
    'diamond_pickaxe': (4, -2.8), 'netherite_pickaxe': (5, -2.8),
    'diamond_axe': (8, -3.0), 'netherite_axe': (9, -3.0),
    'mace': (5, -3.4), 'trident': (8, -2.9),
}


def weapon_attrs(base, bonus_damage=0.0, extra=()):
    dmg, spd = WEAPON_BASE[base]
    mods = [attr('attack_damage', dmg + bonus_damage, 'mainhand', ident='minecraft:base_attack_damage'),
            attr('attack_speed', spd, 'mainhand', ident='minecraft:base_attack_speed')]
    return mods + list(extra)


ARMOR_SLOT = {'helmet': 'head', 'chestplate': 'chest', 'leggings': 'legs', 'boots': 'feet'}
ARMOR_BASE = {  # piece -> (armor, toughness, knockback_res)
    ('diamond', 'helmet'): (3, 2, 0), ('diamond', 'chestplate'): (8, 2, 0),
    ('diamond', 'leggings'): (6, 2, 0), ('diamond', 'boots'): (3, 2, 0),
    ('netherite', 'helmet'): (3, 3, 0.1), ('netherite', 'chestplate'): (8, 3, 0.1),
    ('netherite', 'leggings'): (6, 3, 0.1), ('netherite', 'boots'): (3, 3, 0.1),
}


def armor_attrs(mat, piece, extra=(), bonus_armor=0, bonus_tough=0, bonus_kb=0.0):
    a, t, k = ARMOR_BASE[(mat, piece)]
    s = ARMOR_SLOT[piece]
    mods = [attr('armor', a + bonus_armor, s, ident=f'minecraft:armor.{piece}'),
            attr('armor_toughness', t + bonus_tough, s, ident=f'minecraft:armor.{piece}_toughness')]
    if k + bonus_kb:
        mods.append(attr('knockback_resistance', k + bonus_kb, s, ident=f'minecraft:armor.{piece}_kb'))
    return mods + list(extra)


TIER_TAG = {1: ('✦ Tier I — Token goods', 'gold'), 2: ('✦✦ Tier II — Medallion goods', 'light_purple'),
            3: ('✦✦✦ Tier III — Trophy goods', '#ffb300')}


ITEM_VERSION = 24      # stamped into every item's custom_data (bmv); older copies are re-synced to the current definition
CAT_SYMBOL = {'currency': '❖', 'lucky': '☘', 'key': '⚿', 'map': '⚑', 'meat': '♨', 'feast': '♨', 'food': '♨', 'jackpot': '★',
              'builder': '⚒', 'cosmetic': '✿', 'skin': '✎', 'book': '☙', 'blood': '☽', 'weather': '☁', 'relic': '♥',
              'p2key': '⚿', 'p2map': '⚑', 'p2emblem': '♛', 'p2vkey': '⚿', 'p2prop': '✦', 'p2hidden': '✧', 'p2lucky': '☘',
              'p2lore': '☙', 'misc': '✦'}
ITEM_SYMBOL = {'token': '⛃', 'medallion': '✪', 'trophy': '♛', 'lucky_token': '☘', 'blood_crystal': '♦', 'market_key': '⚿',
               'heartstone': '❤', 'ravenous_heart': '❤', 'charm_eclipse': '☾'}


def item_symbol(iid, base, cat):
    if iid in ITEM_SYMBOL: return ITEM_SYMBOL[iid]
    b = base.split(':')[-1]
    if b.endswith(('_sword', '_axe', 'mace', 'trident')): return '⚔'
    if b.endswith(('_pickaxe', '_shovel', '_hoe')): return '⛏'
    if b in ('bow', 'crossbow'): return '➶'
    if b.endswith(('_helmet', '_chestplate', '_leggings', '_boots', 'shield', 'turtle_helmet')): return '⛨'
    if b == 'elytra': return '✈'
    return CAT_SYMBOL.get(cat, '✦')


def fancy_name(name, color, sym, legendary=False):
    """Bold name framed by a themed symbol; legendary (tier III / boss) items also get gold stars."""
    parts = [{'text': sym + ' ', 'color': color}, {'text': name, 'color': color, 'bold': True}, {'text': ' ' + sym, 'color': color}]
    if legendary:
        parts = [{'text': '✦ ', 'color': 'gold'}] + parts + [{'text': ' ✦', 'color': 'gold'}]
    return {'text': '', 'italic': False, 'extra': parts}


def item(iid, base, name, color, lore=(), model=None, glint=None, stack=None, comps=None,
         custom_extra=None, bold=False, tier=None, cat='misc', price=None):
    c = {}
    c['minecraft:item_name'] = fancy_name(name, color, item_symbol(iid, base, cat), legendary=bold or tier == 3)
    lines = []
    for ln in lore:
        if isinstance(ln, tuple):
            lines.append(T(ln[0], ln[1]))
        else:
            lines.append(T(ln, 'gray'))
    if tier:
        lines.append(T(TIER_TAG[tier][0], TIER_TAG[tier][1]))
    lines.append(T('Black Market goods — no refunds, no questions', 'dark_gray', italic=True))
    c['minecraft:lore'] = lines
    if base == TOTEM:
        c['!minecraft:death_protection'] = {}
    if model:
        c['minecraft:item_model'] = model
    if glint is not None:
        c['minecraft:enchantment_glint_override'] = glint
    if stack:
        c['minecraft:max_stack_size'] = stack
    if comps:
        c.update(comps)
    custom = {'bm': iid}
    if custom_extra:
        custom.update(custom_extra)
    c['minecraft:custom_data'] = dict(custom, bmv=ITEM_VERSION)
    ITEMS[iid] = {'base': base, 'comps': c, 'custom': custom, 'name': name}
    CATEGORY[iid] = cat
    if price:
        PRICES[iid] = price
    return iid


def consumable(seconds=1.6, anim='eat', sound='minecraft:entity.generic.eat', particles=True, effects=None):
    d = {'consume_seconds': float(seconds), 'animation': anim, 'sound': sound,
         'has_consume_particles': particles}
    if effects:
        d['on_consume_effects'] = effects
    return d


# ======================= CURRENCY =======================
item('token', TOTEM, 'Black Market Token', 'gold',
     ['A heavy coin stamped with a grinning rat.', 'Spend it at any Black Market.'],
     model='bm:token', stack=64, cat='currency')
item('medallion', TOTEM, 'Black Market Medallion', 'light_purple',
     ['Worth nine Tokens to the right buyer.', 'Buys Tier II goods and upgrades.'],
     model='bm:medallion', stack=64, cat='currency')
item('trophy', TOTEM, 'Black Market Trophy', '#ffb300',
     ['Only the boldest smugglers own one.', 'Buys Tier III goods and upgrades.'],
     model='bm:trophy', stack=16, bold=True, cat='currency')
item('lucky_token', TOTEM, 'Lucky Token', 'green',
     ['Dropped by Lucky creatures.', 'Spend it at a Chance Corner.'],
     model='bm:lucky_token', stack=64, cat='currency')
item('scratch_card', TOTEM, 'Lucky Scratch Card', 'yellow',
     ['Hold right-click to scratch!', ('Prizes: Tokens, Medallions, Trophies...', 'gold'),
      ('...and the legendary Lucky 7.', 'gold'), ('(Sometimes you win nothing. That\'s gambling.)', 'dark_gray')],
     model='bm:scratch_card', stack=64,
     comps={'minecraft:consumable': consumable(1.0, 'brush', 'minecraft:item.brush.brushing.generic', False)},
     cat='lucky')
item('market_key', TOTEM, 'Black Market Key', '#a96bff',
     ['Taken from the crypt of the Velvet Hand.', 'Keep it in your inventory to open', 'Black Market vault doors.',
      ('Lose it and the rats won\'t let you in.', 'dark_gray')],
     model='bm:market_key', glint=True, cat='key')
item('sealed_map_market', TOTEM, "Sealed Smuggler's Map", 'aqua',
     ['Hold right-click to break the seal.', 'Marks the nearest Black Market.'],
     model='minecraft:map', glint=True, stack=16,
     comps={'minecraft:consumable': consumable(0.8, 'none', 'minecraft:item.book.page_turn', False)}, cat='map')
item('sealed_map_graveyard', TOTEM, "Sealed Gravedigger's Map", 'gray',
     ['Hold right-click to break the seal.', 'Marks the nearest haunted graveyard.'],
     model='minecraft:map', glint=True, stack=16,
     comps={'minecraft:consumable': consumable(0.8, 'none', 'minecraft:item.book.page_turn', False)}, cat='map')

# ======================= PRIME MEATS =======================
for mid, model, nm in [('prime_pork', 'minecraft:porkchop', 'Prime Porkchop'), ('prime_beef', 'minecraft:beef', 'Prime Beef'),
                       ('prime_mutton', 'minecraft:mutton', 'Prime Mutton'), ('prime_chicken', 'minecraft:chicken', 'Prime Chicken'),
                       ('prime_rabbit', 'minecraft:rabbit', 'Prime Rabbit')]:
    item(mid, TOTEM, nm, 'gold', ['Rare meat from a Prime animal.', 'Chef Fromage turns it into', 'permanent feasts.'],
         model=model, glint=True, stack=64, cat='meat')

# ======================= FEASTS (permanent buffs) =======================
FEASTS = []  # (id, buff, tier, effect, amp, meat)
FEAST_DEF = [
    ('health', 'minecraft:health_boost', 'prime_beef', 'Health Boost',
     ('Super Mushroom Stew', 'minecraft:mushroom_stew', 'red'), ('Life Mushroom Stew', 'minecraft:rabbit_stew', 'light_purple')),
    ('strength', 'minecraft:strength', 'prime_pork', 'Strength',
     ("Kong's Banana Porkchop", 'minecraft:cooked_porkchop', 'yellow'), ('Golden Banana Feast', 'minecraft:golden_carrot', 'gold')),
    ('resistance', 'minecraft:resistance', 'prime_mutton', 'Resistance',
     ('Goron Spice Mutton', 'minecraft:cooked_mutton', 'dark_red'), ('Goron Rock Roast', 'minecraft:baked_potato', 'red')),
    ('haste', 'minecraft:haste', 'prime_chicken', 'Haste',
     ('Cucco Drumstick', 'minecraft:cooked_chicken', 'white'), ('Cucco Cluster Feast', 'minecraft:pumpkin_pie', 'aqua')),
    ('speed', 'minecraft:speed', 'prime_rabbit', 'Speed',
     ('Hasty Rabbit Skewer', 'minecraft:cooked_rabbit', 'aqua'), ('Pegasus Rabbit Stew', 'minecraft:beetroot_soup', 'blue')),
]
ROMAN = {1: 'I', 2: 'II'}
for buff, eff, meat, ename, t1, t2 in FEAST_DEF:
    for tier, (nm, model, col) in ((1, t1), (2, t2)):
        fid = f'feast_{buff}_{tier}'
        lore = [(f'Permanent {ename} {ROMAN[tier]}', 'blue'), 'Lasts until you die.']
        if tier == 2:
            lore.append((f'Requires the {t1[0]} blessing first!', 'red'))
        item(fid, TOTEM, nm, col, lore, model=model, glint=True, stack=16,
             comps={'minecraft:food': {'nutrition': 8, 'saturation': 10.0, 'can_always_eat': True},
                    'minecraft:consumable': consumable(2.0)}, cat='feast')
        FEASTS.append((fid, buff, tier, eff, tier - 1, meat, ename, t1[0]))

item('aged_cheddar', TOTEM, 'Wheel of Aged Cheddar', 'yellow',
     ['The Rat Gang\'s finest. Smells illegal.', ('Absorption II (3:00), Regeneration I (0:30)', 'blue')],
     model='minecraft:cake', stack=16,
     comps={'minecraft:food': {'nutrition': 10, 'saturation': 14.0, 'can_always_eat': True},
            'minecraft:consumable': consumable(2.4, effects=[{'type': 'minecraft:apply_effects', 'effects': [
                {'id': 'minecraft:absorption', 'amplifier': 1, 'duration': 3600},
                {'id': 'minecraft:regeneration', 'amplifier': 0, 'duration': 600}]}])}, cat='food',
     price=('token', 2))

# ======================= WEAPONS & TOOLS =======================
UPGRADES = []  # (from_id, currency, count, to_id)


def gear(iid, base, name, color, lore, enchants, tier, attrs=None, model=None, extra=None, price=None, upgrade_from=None, bold=False,
         custom_extra=None):
    comps = {'minecraft:enchantments': enchants}
    if attrs:
        comps['minecraft:attribute_modifiers'] = attrs
    if extra:
        comps.update(extra)
    item(iid, f'minecraft:{base}', name, color, lore, model=model, comps=comps, tier=tier, cat='gear', price=price, bold=bold,
         custom_extra=custom_extra)
    if upgrade_from:
        f, cur, n = upgrade_from
        UPGRADES.append((f, cur, n, iid))
        PRICES[iid] = (cur, n)


# Swords — Hero's Blade line
gear('kokiri_sword', 'diamond_sword', 'Kokiri Sword', 'green', ['"It\'s dangerous to go alone."'],
     ench(sharpness=6, looting=4, sweeping_edge=4, unbreaking=4), 1, price=('token', 12))
gear('master_sword', 'netherite_sword', 'Master Sword', 'aqua', ['The blade of evil\'s bane.', ('+1 Attack Damage', 'blue')],
     ench(sharpness=8, smite=7, looting=5, sweeping_edge=5, unbreaking=6, mending=1), 2,
     attrs=weapon_attrs('netherite_sword', 1), upgrade_from=('kokiri_sword', 'medallion', 8))
gear('biggoron_sword', 'netherite_sword', "Biggoron's Sword", '#ffb300',
     ['Forged by a giant. Swings like one, too.', ('+4 Attack Damage, +1.5 Reach', 'blue')],
     ench(sharpness=10, smite=10, looting=6, sweeping_edge=6, fire_aspect=3, unbreaking=10, mending=1), 3,
     attrs=weapon_attrs('netherite_sword', 4, [attr('entity_interaction_range', 1.5, 'mainhand')]),
     upgrade_from=('master_sword', 'trophy', 4), bold=True)
# Pickaxes — Mine Cart line
gear('cranky_pick', 'diamond_pickaxe', "Cranky's Pick", 'gold', ['"Back in MY day, Fortune', 'stopped at three!"'],
     ench(fortune=4, efficiency=6, unbreaking=4), 1, price=('token', 10))
gear('minecart_pick', 'netherite_pickaxe', 'Mine Cart Madness', 'light_purple', ['Hold on to your hat.'],
     ench(fortune=5, efficiency=8, unbreaking=6, mending=1), 2, upgrade_from=('cranky_pick', 'medallion', 6))
gear('kong_krusher', 'netherite_pickaxe', 'Kong Krusher', '#ffb300', ['Turns mountains into bananas.', ('+50% Block Break Speed, +1 Luck', 'blue')],
     ench(fortune=6, efficiency=10, unbreaking=10, mending=1), 3,
     attrs=weapon_attrs('netherite_pickaxe', 0, [attr('block_break_speed', 0.5, 'mainhand', 'add_multiplied_base'),
                                                 attr('luck', 1, 'mainhand')]),
     upgrade_from=('minecart_pick', 'trophy', 3), bold=True)
# Axes — Koopa line
gear('hammer_bro_hatchet', 'diamond_axe', 'Hammer Bro Hatchet', 'green', ['Lost by a turtle. Found by you.'],
     ench(sharpness=6, efficiency=6, unbreaking=4), 1, price=('token', 10))
gear('koopa_cleaver', 'netherite_axe', "Koopa King's Cleaver", 'red', ['Smells faintly of lava and castles.'],
     ench(sharpness=8, smite=6, efficiency=8, unbreaking=6, mending=1), 2, upgrade_from=('hammer_bro_hatchet', 'medallion', 6))
gear('giga_greataxe', 'netherite_axe', "Giga Koopa's Greataxe", '#ffb300', ['Fell the forest. Fell the castle.', ('+3 Attack Damage', 'blue')],
     ench(sharpness=10, efficiency=10, fire_aspect=2, unbreaking=10, mending=1), 3,
     attrs=weapon_attrs('netherite_axe', 3), upgrade_from=('koopa_cleaver', 'trophy', 3), bold=True)
# Bows — Fairy line
gear('fairy_bow', 'bow', 'Fairy Bow', 'light_purple', ['Fairies not included.'],
     ench(power=6, infinity=1, unbreaking=4), 1, price=('token', 10))
gear('heros_bow', 'bow', "Hero's Bow", 'aqua', ['Infinity AND Mending? Shh.'],
     ench(power=8, punch=3, flame=1, infinity=1, unbreaking=6, mending=1), 2, upgrade_from=('fairy_bow', 'medallion', 6))
gear('light_bow', 'bow', 'Bow of Light', '#ffb300', ['Seals evil. Also creepers.'],
     ench(power=10, punch=4, flame=2, infinity=1, unbreaking=10, mending=1), 3, upgrade_from=('heros_bow', 'trophy', 3), bold=True)
# Hammers
gear('super_hammer', 'mace', 'Super Hammer', 'yellow', ['Smashes rocks, blocks and egos.'],
     ench(density=6, breach=5, wind_burst=2, unbreaking=5), 2, price=('medallion', 8))
gear('ultra_hammer', 'mace', 'Ultra Hammer', '#ffb300', ['For when Super isn\'t enough.', ('+2 Attack Damage', 'blue')],
     ench(density=10, breach=6, wind_burst=3, unbreaking=10, mending=1), 3,
     attrs=weapon_attrs('mace', 2), upgrade_from=('super_hammer', 'trophy', 3), bold=True)
# Singles
gear('hylian_shield', 'shield', 'Hylian Shield', 'blue', ['Never melts. Never burns.', 'Rarely cracks.'],
     ench(unbreaking=10, mending=1), 1, price=('token', 14))
gear('zora_trident', 'trident', "Zora's Trident", 'dark_aqua', ['Returns faster than a boomerang.'],
     ench(impaling=6, loyalty=4, channeling=1, unbreaking=6, mending=1), 1, price=('token', 12))

# Armor sets
ARMOR_NAMES = {
    'smuggler': ("Smuggler's", ['Hood', 'Vest', 'Trousers', 'Boots'], 'gold'),
    'kingpin': ("Kingpin's", ['Helm', 'Coat', 'Slacks', 'Loafers'], 'light_purple'),
    'hero': ('Hero of Time', ['Cap', 'Tunic', 'Leggings', 'Boots'], '#ffb300'),
}
PIECES = ['helmet', 'chestplate', 'leggings', 'boots']
SMUGGLER_PRICE = [8, 12, 10, 8]
for i, piece in enumerate(PIECES):
    s = ARMOR_SLOT[piece]
    # Tier I
    e1 = ench(protection=5, unbreaking=4)
    if piece == 'helmet': e1.update(ench(respiration=3))
    if piece == 'leggings': e1.update(ench(swift_sneak=4))
    if piece == 'boots': e1.update(ench(feather_falling=5))
    gear(f'smuggler_{piece}', f'diamond_{piece}', f"Smuggler's {ARMOR_NAMES['smuggler'][1][i]}", 'gold',
         ['Pockets for every occasion.', ('Full set: Luck + golden sparks', 'dark_aqua')], e1, 1, price=('token', SMUGGLER_PRICE[i]),
         custom_extra={'bm_set': 'smuggler'})
    # Tier II
    e2 = ench(protection=6, unbreaking=6, mending=1)
    if piece == 'helmet': e2.update(ench(respiration=4, aqua_affinity=1))
    if piece == 'leggings': e2.update(ench(swift_sneak=5))
    if piece == 'boots': e2.update(ench(feather_falling=6, depth_strider=3))
    gear(f'kingpin_{piece}', f'netherite_{piece}', f"Kingpin's {ARMOR_NAMES['kingpin'][1][i]}", 'light_purple',
         ['Crime pays. Literally.', ('+2 Max Health', 'blue'), ('Full set: Fire Resistance + violet aura', 'dark_aqua')], e2, 2,
         attrs=armor_attrs('netherite', piece, [attr('max_health', 2, s)]),
         upgrade_from=(f'smuggler_{piece}', 'medallion', 5), custom_extra={'bm_set': 'kingpin'},
         extra={'minecraft:trim': {'material': 'minecraft:amethyst', 'pattern': 'minecraft:eye'}})
    # Tier III
    e3 = ench(protection=8, unbreaking=10, mending=1)
    extra3 = [attr('max_health', 4, s)]
    perk = '+4 Max Health'
    if piece == 'helmet': e3.update(ench(respiration=5, aqua_affinity=1))
    if piece == 'chestplate': e3.update(ench(thorns=4))
    if piece == 'leggings':
        e3.update(ench(swift_sneak=5)); extra3.append(attr('step_height', 0.5, s)); perk += ', +0.5 Step Height'
    if piece == 'boots':
        e3.update(ench(feather_falling=10, depth_strider=3)); extra3.append(attr('movement_speed', 0.1, s, 'add_multiplied_base')); perk += ', +10% Speed'
    gear(f'hero_{piece}', f'netherite_{piece}', f"Hero of Time {ARMOR_NAMES['hero'][1][i]}", '#ffb300',
         ['Worn by a legend. Smells like grass.', (perk, 'blue'), ('Full set: Regeneration + triforce glow', 'dark_aqua')], e3, 3,
         attrs=armor_attrs('netherite', piece, extra3, bonus_tough=1, bonus_kb=0.05),
         upgrade_from=(f'kingpin_{piece}', 'trophy', 3), bold=True, custom_extra={'bm_set': 'hero'},
         extra={'minecraft:trim': {'material': 'minecraft:gold', 'pattern': 'minecraft:wayfinder'}})

# Lucky 7 (scratch-card jackpot only)
gear('lucky_seven', 'netherite_sword', 'Lucky 7', '#ffd700',
     ['Seven sevens. Pure luck.', ('+7 Luck while held', 'blue')],
     ench(sharpness=7, smite=7, bane_of_arthropods=7, looting=7, fire_aspect=7, sweeping_edge=7,
          knockback=2, unbreaking=7, mending=1), 3,
     attrs=weapon_attrs('netherite_sword', 0, [attr('luck', 7, 'mainhand')]),
     model='minecraft:golden_sword', bold=True)
CATEGORY['lucky_seven'] = 'jackpot'

# Rat Gang secret weapon
gear('cheese_grater', 'netherite_sword', 'The Cheese Grater', 'yellow',
     ['Rat Gang standard issue.', 'Shreds mobs like aged cheddar.'],
     ench(sharpness=7, looting=6, sweeping_edge=6, unbreaking=7, mending=1), 2, price=('medallion', 6))

# ======================= BUILDER GEAR =======================
def offhand_charm(iid, name, color, lore, model, mods, price, glint=True):
    item(iid, TOTEM, name, color, lore, model=model, glint=glint,
         comps={'minecraft:attribute_modifiers': mods}, cat='builder', price=price)


offhand_charm('architect_gauntlet', "Architect's Gauntlet", 'gold', ['Hold in your off hand.', ('+3 Block Reach', 'blue')],
              'bm:gauntlet', [attr('block_interaction_range', 3, 'offhand')], ('token', 14), glint=False)
offhand_charm('rocs_feather', "Roc's Feather", 'white', ['Hold in your off hand.', ('Higher jumps, softer landings', 'blue')],
              'minecraft:feather', [attr('jump_strength', 0.2, 'offhand'), attr('safe_fall_distance', 8, 'offhand')], ('token', 12))
offhand_charm('super_leaf', 'Super Leaf', 'green', ['Hold in your off hand.', ('Floaty jumps, no fall damage worries', 'blue')],
              'minecraft:oak_leaves', [attr('gravity', -0.04, 'offhand'), attr('safe_fall_distance', 20, 'offhand')], ('medallion', 2))
offhand_charm('mini_mushroom', 'Mini Mushroom', 'aqua', ['Hold in your off hand.', ('Shrink to half size', 'blue')],
              'minecraft:brown_mushroom', [attr('scale', -0.5, 'offhand', 'add_multiplied_base')], ('token', 10))
offhand_charm('mega_mushroom', 'Mega Mushroom', 'red', ['Hold in your off hand.', ('Double size, +3 reach, +1 step', 'blue')],
              'minecraft:red_mushroom', [attr('scale', 1.0, 'offhand', 'add_multiplied_base'), attr('block_interaction_range', 3, 'offhand'),
                                         attr('entity_interaction_range', 2, 'offhand'), attr('step_height', 1, 'offhand')], ('medallion', 3))
offhand_charm('lucky_charm', 'Four-Leaf Charm', 'green', ['Hold in your off hand.', ('+2 Luck', 'blue')],
              'bm:lucky_token', [attr('luck', 2, 'offhand')], ('lucky_token', 3))

HEAD = {'slot': 'head', 'swappable': True, 'equip_sound': 'minecraft:item.armor.equip_leather'}
item('lens_of_truth', TOTEM, 'Lens of Truth', 'aqua', ['Wear on your head.', ('Night Vision while worn', 'blue')],
     model='bm:lens_goggles', comps={'minecraft:equippable': HEAD}, cat='builder', price=('token', 10))
item('minish_cap', TOTEM, 'Minish Cap', 'green', ['Wear on your head to shrink to', 'rat size. Fits through mouse holes!',
                                                  ('The Rat Gang\'s VIP pass.', 'dark_gray')],
     model='bm:minish_cap', comps={'minecraft:equippable': HEAD,
                                   'minecraft:attribute_modifiers': [attr('scale', -0.75, 'head', 'add_multiplied_base')]},
     cat='builder', price=('token', 6))
item('pegasus_boots', 'minecraft:leather_boots', 'Pegasus Boots', 'gold', ['Dash like a hero.', ('+35% Speed, +0.6 Step Height', 'blue')],
     comps={'minecraft:dyed_color': 0xD4A017, 'minecraft:unbreakable': {},
            'minecraft:attribute_modifiers': [attr('armor', 3, 'feet', ident='minecraft:armor.boots'),
                                              attr('movement_speed', 0.35, 'feet', 'add_multiplied_base'),
                                              attr('step_height', 0.6, 'feet')]}, cat='builder', price=('token', 16))
item('bouncy_boots', 'minecraft:leather_boots', 'Boing Boots', 'green', ['Boing.', ('Bouncy landings, no fall damage up to 12', 'blue')],
     comps={'minecraft:dyed_color': 0x7CFC00, 'minecraft:unbreakable': {},
            'minecraft:attribute_modifiers': [attr('armor', 1, 'feet', ident='minecraft:armor.boots'),
                                              attr('bounciness', 0.6, 'feet'), attr('safe_fall_distance', 12, 'feet')]},
     cat='builder', price=('token', 8))

# ======================= COSMETICS =======================
COSMETICS = {}  # id -> (slot, particle command suffix)
def hat(iid, name, color, model, fx, price, lore=(), mods=None):
    comps = {'minecraft:equippable': HEAD}
    if mods: comps['minecraft:attribute_modifiers'] = mods
    item(iid, TOTEM, name, color, list(lore) + [('Cosmetic — wear on your head', 'dark_aqua')], model=model,
         comps=comps, cat='cosmetic', price=price, custom_extra={'bm_fx': iid})
    COSMETICS[iid] = ('armor.head', fx)


hat('crown', 'Golden Crown', 'gold', 'bm:crown', 'minecraft:wax_on ~ ~2.2 ~ 0.25 0.05 0.25 0 1', ('medallion', 2), ['Heavy is the head.'])
hat('party_hat', 'Party Hat', 'light_purple', 'bm:party_hat', 'minecraft:note ~ ~2.4 ~ 0.3 0.1 0.3 1 1', ('token', 6), ['It\'s always somebody\'s birthday.'])
hat('top_hat', 'Dapper Top Hat', 'dark_gray', 'bm:top_hat', 'minecraft:enchant ~ ~2.3 ~ 0.2 0.2 0.2 0.3 2', ('token', 6), ['Monocle sold separately.'])
hat('halo', 'Angel Halo', 'yellow', 'bm:halo', 'minecraft:end_rod ~ ~2.3 ~ 0.2 0.02 0.2 0 1', ('medallion', 2), ['Totally innocent. Promise.'])
hat('pirate_hat', "Captain's Tricorn", 'dark_red', 'bm:pirate_hat', 'minecraft:bubble_pop ~ ~2.2 ~ 0.3 0.1 0.3 0 1', ('medallion', 3), ['Yarr. Squeak.'])
hat('rat_king_crown', "Rat King's Crown", '#ffb300', 'bm:crown', 'minecraft:dust{color:[0.9,0.75,0.1],scale:0.8} ~ ~2.2 ~ 0.3 0.1 0.3 0 2',
    ('trophy', 1), ['Long live the Rat King.', ('+1 Luck', 'blue')], mods=[attr('luck', 1, 'head')])


def trail(iid, name, color, dye, fx, price, lore):
    item(iid, 'minecraft:leather_boots', name, color, list(lore) + [('Cosmetic — leaves a trail', 'dark_aqua')],
         comps={'minecraft:dyed_color': dye, 'minecraft:unbreakable': {}}, cat='cosmetic', price=price,
         custom_extra={'bm_fx': iid})
    COSMETICS[iid] = ('armor.feet', fx)


trail('flame_boots', 'Blazing Trail Boots', 'red', 0xE03C1E, 'minecraft:small_flame ~ ~0.1 ~ 0.15 0 0.15 0 2', ('token', 8), ['Hot stuff.'])
trail('heart_boots', 'Sweetheart Boots', 'light_purple', 0xFF7FC8, 'minecraft:heart ~ ~0.3 ~ 0.2 0 0.2 0 1', ('token', 8), ['Spread the love.'])
trail('soul_boots', 'Soulwalker Boots', 'dark_aqua', 0x2A7F8F, 'minecraft:soul ~ ~0.1 ~ 0.2 0 0.2 0.01 1', ('token', 10), ['Spooky footsteps.'])

# ======================= SKIN SCROLLS =======================
SKINS = [  # id, label, model
    ('rotten_flesh', 'Rotten Flesh', 'minecraft:rotten_flesh'), ('fish', 'Fish Slap', 'minecraft:cod'),
    ('bone', 'Bone Club', 'minecraft:bone'), ('baguette', 'Baguette', 'minecraft:bread'),
    ('twig', 'Humble Twig', 'minecraft:stick'), ('blaze_staff', 'Blaze Staff', 'minecraft:blaze_rod'),
    ('golden_carrot', 'Golden Carrot', 'minecraft:golden_carrot'), ('rubber_chicken', 'Rubber Chicken', 'bm:rubber_chicken'),
    ('frying_pan', 'Frying Pan', 'bm:frying_pan'),
    ('bag_of_rocks', 'Bag of Rocks', 'bm:bag_of_rocks'), ('rpg_launcher', 'RPG Launcher', 'bm:rpg_launcher'),
    ('butter_sock', 'Butter Sock', 'bm:butter_sock'), ('pool_noodle', 'Pool Noodle', 'bm:pool_noodle'),
    ('rubber_duck', 'Rubber Duck', 'bm:rubber_duck'),
]
for sid, label, model in SKINS:
    item(f'skin_{sid}', TOTEM, f'Skin Scroll: {label}', 'aqua',
         ['Put the item to reskin in your OFF hand,', 'then use this scroll in your main hand.',
          ('Your item keeps all its enchantments.', 'dark_gray')],
         model='minecraft:paper', glint=True, stack=16,
         comps={'minecraft:consumable': consumable(1.0, 'spyglass', 'minecraft:item.book.page_turn', False)},
         cat='skin', price=('token', 3))
item('skin_restore', TOTEM, 'Skin Scroll: Restore', 'white',
     ['Put a reskinned item in your OFF hand,', 'then use this scroll to restore its look.'],
     model='minecraft:paper', glint=False, stack=16,
     comps={'minecraft:consumable': consumable(1.0, 'spyglass', 'minecraft:item.book.page_turn', False)},
     cat='skin', price=('token', 1))

# ======================= LORE BOOKS =======================
BOOKS = {}


def book(bid, title, author, pages, price=('token', 1)):
    comps = {'minecraft:written_book_content': {'title': title, 'author': author,
                                                'pages': [p if isinstance(p, dict) else {'text': p} for p in pages]}}
    c = {'minecraft:written_book_content': comps['minecraft:written_book_content'],
         'minecraft:custom_data': {'bm': bid, 'bmv': ITEM_VERSION}}
    ITEMS[bid] = {'base': 'minecraft:written_book', 'comps': c, 'custom': {'bm': bid}, 'name': title}
    CATEGORY[bid] = 'book'
    BOOKS[bid] = title
    return bid


book('book_velvet_hand', 'The Velvet Hand', 'An Anonymous Archivist', [
    "THE VELVET HAND\n\nLong before the rats, before the dust, there was a guild of thieves who called themselves the Velvet Hand.\n\nThey robbed no farmers and no villagers. They robbed the rules.",
    "Every enchanter knows the old limits: Fortune III, Sharpness V, Protection IV, and no further.\n\nThe Velvet Hand found ways past them. Nobody knows how. Some say they bribed the books themselves.",
    "They dug their markets deep below the world, sealed with vault doors only a guild key could open.\n\nTheir coins were stamped with a grinning rat, a joke about being 'vermin' that aged very strangely.",
    "At their height the Hand traded in blades that never dulled and boots that ran like the wind.\n\nThen came the Night of Broken Locks.\n\n(See: 'The Night of Broken Locks', also available at this counter. Very reasonable price.)",
])
book('book_broken_locks', 'The Night of Broken Locks', 'An Anonymous Archivist', [
    "THE NIGHT OF\nBROKEN LOCKS\n\nThe Velvet Hand feared no sheriff and no golem. They should have feared Blaine West.",
    "Blaine West was a wandering adventurer with a battered hat, an honest smile and a terrible habit of finding things out.\n\nHe spent a year pretending to be a lost miner, buying nothing and watching everything.",
    "On the night the guild gathered to divide its treasure, West swapped the Guildmaster's key for a clever fake.\n\nWhen the vaults were opened, every alarm in the market rang at once.",
    "The guild scattered into the dark. The Guildmaster fled to the old graveyard crypts with the real keys, and was never seen alive again.\n\nSomething guards those crypts now. Something that listens.",
    "As for Blaine West, nobody knows where he went. Some say he still checks on the markets.\n\nThe rats certainly seem to think so.",
])
book('book_new_management', 'Under New Management', 'Capt. Cheddarbeard', [
    "UNDER NEW\nMANAGEMENT\n\nAttention customers. This market has been ACQUIRED by the Rat Gang, finest pirate crew of the Underdark.",
    "We did not steal this market. We FOUND it. Finders keepers is legally binding (rat law, section 1).\n\nAll prior debts to the Velvet Hand are cancelled. All prior cheese now belongs to us.",
    "The humans behind the counters work for us now. They are paid in cheese. They seem fine with it.\n\nComplaints may be submitted through the mouse hole. Mind your head. Actually, shrink your head.",
    "If anyone named Blaine West asks: we are ordinary rats. We do not run a market. We cannot read.\n\nThis book was not written by a rat.\n\n- Management",
])
book('book_rat_code', 'Rat Gang Code of Conduct', 'The Rat Gang', [
    "RAT GANG\nCODE OF CONDUCT\n\nArticle I:\nNo cats. No exceptions. Not even 'nice' cats.\n\nArticle II:\nCheese is split equally among the crew. The Captain's equal share is larger.",
    "Article III:\nAny rat who sees Blaine West must squeak twice and pretend to be a regular rat.\n\nArticle IV:\nThe mouse hole is for crew and VIP customers in Minish Caps only.",
    "Article V:\nNo gambling on the job. (Exception: the Chance Corner, which is not gambling, it is 'investing in luck'.)\n\nArticle VI:\nThe Captain is always right, especially when wrong.",
    "Article VII:\nIf a human asks why the coins have rats on them, say 'tradition' and change the subject.\n\nSigned,\nThe Crew (paw prints)",
])
book('book_field_guide', 'Field Guide to Unusual Creatures', 'Prof. Whiskerton', [
    "FIELD GUIDE TO\nUNUSUAL CREATURES\nby Prof. Whiskerton\n\nThe world is getting stranger, dear customer. Here is what to watch for.",
    "ELITE creatures wear maxed-out armor or glow with potion power. They drop 1 Black Market Token, sometimes 2 or 3.\n\nCHAMPIONS are bigger, faster, nastier, and bring friends. They drop several Tokens and sometimes a Medallion.",
    "LUCKY creatures sparkle with gold. Rare! They drop Lucky Tokens, which my colleague Lucky Whiskers will happily exchange for Scratch Cards.\n\nWatch for the LUCKY GOLDEN GOOSE, a warm-climate chicken blessed with absurd fortune.",
    "PRIME animals (pigs, cows, sheep, chickens, rabbits) are fat, glossy and rare. They drop Prime meat, which Chef Fromage cooks into permanent feasts.\n\nTokens can also hide in old chests. Look closely.",
])
book('book_chefs_ledger', "The Chef's Ledger", 'Chef Fromage', [
    "THE CHEF'S LEDGER\n\nBonjour! I am Chef Fromage. I cook only with PRIME meat. Bring me Prime cuts and Tokens, and I will make you a feast whose blessing lasts... until you die.",
    "RULE ONE:\nA blessing lasts until death. Milk will not wash it away for long. Death will.\n\nRULE TWO:\nYou must eat the first course before the second. A Tier II feast on an unseasoned stomach does nothing.",
    "(If you try, I will refund your dish, and also judge you.)\n\nRULE THREE:\nOne blessing of each kind. Health, Strength, Resistance, Haste and Speed may all be enjoyed together. Bon appetit!",
])
book('book_wanted', 'WANTED: Blaine West', 'The Rat Gang', [
    "WANTED\n\nBLAINE WEST\n\nFor crimes against the Velvet Hand, the Rat Gang, and good cheese.\n\nReward: 1 wheel of cheese (slightly nibbled).",
    "Description: tall, honest-looking, battered hat, suspiciously good at noticing things.\n\nIf seen, do NOT approach. Squeak twice. Pretend to be a regular rat.\n\nThis poster was not made by rats.",
])
GRAVE_BOOK = {'title': 'To Whoever Finds This', 'author': 'The Gravedigger', 'pages': [
    {'text': "To whoever finds this,\n\nBeneath these stones sleep the last of the Velvet Hand, and their master's keys sleep with them.\n\nYou are not the first to come looking. Most do not come back up."},
    {'text': "I have dug these graves for forty years, and I will tell you what I know.\n\nWalk soft. Do not run. Do not shout. Sound carries down there, and something is always listening."},
    {'text': "The moment you set foot below, it wakes. The dark comes, your legs go heavy. Do not panic. Crouch. Breathe. Keep moving.\n\nThe tunnels below were dug to confuse grave robbers. They still do."},
    {'text': "The old master lies at the very heart of the maze, the key still in his grip. Kneel to him and he may let go.\n\nThat is also where IT sleeps."},
    {'text': "They say that when he lets go, a way out opens in a far corner of the maze for those who are worthy.\n\nI never found out. I was never brave enough.\n\nGood luck.\n- The Gravedigger"},
]}

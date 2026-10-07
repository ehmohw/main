"""Generates the Black Market data pack."""
import json, os, shutil, sys
from nbt import snbt, to_json, B, F, D, L, Int
import items as I
from items import ITEMS, PRICES, CATEGORY, UPGRADES, FEASTS, COSMETICS, SKINS, BOOKS, T, TOTEM
import structures as S
import phase15 as P
import phase16 as Q
import phase17 as R
import phase18 as R18
import phase19 as R19
import phase20 as R20
import phase21 as R21
import phase22 as R22
import phase23 as R23
import phase24 as R24
import phase25 as R25
import phase26 as R26
import phase27 as R27
import phase28 as R28        # 1.18: Standing, keys, gates, back rooms (+ menus, payments)
import phase29 as R29        # 1.18: the new goods
import phase30 as R30        # 1.18: the Dark Auction
import phase31 as R31        # 1.18: the Gilded Gutter + Rat Bank
import phase32 as R32        # 2.13: the Vorn - invasion nights, crash sites carved at runtime, the Dreadnought, red Xenite
import phase33 as R33        # 2.13: new goods (satchel, fusion, shifter, jump boots, void totem, flask, pocket ender chest...)
import phase34 as R34        # 2.13: the market overhaul, the Dockmaster, the Gilded Roost's treasures
import phase35 as R35        # 2.14: the Vorn Skiff, the Dawnbringer set, the drill, rat portraits, the newcomers' lectern
import phase36 as R36        # 2.15: marlin, storm balls, coffee, skiff kits, the restless dead, mailboxes
import phase37 as R37        # 2.16: Specter Sheets and the Specter Charm
import phase38 as R38        # 2.17: Surface/Lava/Rainbow charms, rare monsters
import phase39 as R39        # 2.18: world treasure: accessories, Mimics, Fallen Stars, crates, shrines
import phase40 as R40        # 2.19: the Bounty Board
import phase41 as R41        # 2.20: market fixes + shafts, the Vorn fixes, the Rat Gang's prizes
import phase42 as R42        # 2.20: the Headless Horseman and his head
import phase43 as R43        # 2.21: night cosmetics, Hollow wings, the Experience Charm
import phase44 as R44        # 2.23: glow range, satchel barrel, mailbox repair, soul vials, bounty board
import phase45 as R45        # 2.24: Cecil the Wizard, the chef's dishes, goofy goods, music, the Vorn walk
import phase46 as R46        # 2.24: Cecil the companion, the chef's portrait, the Emma doll
import phase47 as R47
import phase48 as R48
import phase49 as R49
import phase50 as R50
import phase51 as R51
import phase52 as R52
import phase55 as R55        # 2.35: honest gear - sockets by material, combos, Masterworks, Relic Essences
import phase54 as R54        # 2.33: the Elder Treant, the Magma Colossus, the Voidwalker and their relics
import phase53 as R53        # 2.32: the Horseman's Head in four classes, the Sand Pharaoh, the Storm Roc, their relics, WANTED posters
#       # 2.31: night ambience, Happy Hour, slots + jackpot, the Leprechaun Rat, Defend the Mothership, the reactor, invasion goods        # 2.30: the sunrise day count, the Scrap Bin (Old Barnaby's buy-backs move into it)        # 2.29: the newcomers' book from the trade lists, advancements, recipes, settings, the Grave Charm        # 2.28: tinkering - filter/vacuum hoppers, compactor, wireless, clock, breaker, placer, sorting chest, lens, wrench        # 2.27: the Vorn Skiff's tractor beam; the skiff's hull fits its pilot        # 2.26: Moon Pact, Thirsting Blade, Vampire's Mirror, Crimson Hourglass, the Blood Moon disc
import optimize              # 2.15: the final selector/gating pass (optimize.py)
import useitem               # 2.13: hold-to-use items (using_item trigger)
import market2 as M2
import economy as ECON
import mig263
PHASE2 = '--phase2' in sys.argv
if PHASE2:
    import p2  # registers Phase 2 items on import

OUT = None
FUNCS = {}


def path(*p):
    full = os.path.join(OUT, *p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    return full


def wjson(rel, obj):
    obj = mig263.convert(rel, to_json(mig263.custom_data_snbt(obj)))   # 26.3 shapes; custom_data as SNBT text (mig263.py)
    with open(path('data', *rel.split('/')), 'w') as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)


def fn(name, lines):
    """Register a function bm:<name>."""
    if isinstance(lines, str):
        lines = lines.strip('\n').split('\n')
    FUNCS[name] = [l.rstrip() for l in lines]


# ---------------------------------------------------------------- item helpers
def item_arg(iid):
    it = ITEMS[iid]
    parts = []
    for k, v in it['comps'].items():
        parts.append(k if k.startswith('!') else f'{k}={snbt(v)}')
    return f"{it['base']}[{','.join(parts)}]"


def give(iid, n=1, who='@s'):
    return f'give {who} {item_arg(iid)} {n}'


def stack(iid, n=1):
    if iid in ITEMS:
        return {'id': ITEMS[iid]['base'], 'count': Int(n), 'components': ITEMS[iid]['comps']}
    return {'id': iid if ':' in iid else 'minecraft:' + iid, 'count': Int(n)}


# Components a trade cost must match exactly. custom_data identifies the item; the others make the trade screen show the
# real icon, name and glint, and max_stack_size stops the game clamping the price to the base item's stack size (a
# totem's is 1, which turned every price into 1). Lore, enchantments and damage are NOT matched, so an upgraded or
# worn previous-tier item is still accepted.
COST_KEYS = ('minecraft:custom_data', 'minecraft:item_model', 'minecraft:item_name', 'minecraft:max_stack_size')   # 1.16: no glint override (Xenite trades refused real shards)


def exact_comps(iid):
    """Every component the item is sold/given with (minus removals, which a cost can't express, and item_model for
    gear so a reskinned piece still counts). Used for trade-ins and for re-syncing old copies."""
    c = ITEMS[iid]['comps']
    return {k: v for k, v in c.items() if not k.startswith('!') and not (k == 'minecraft:item_model' and ITEMS[iid]['base'] != TOTEM)}


def cost(iid, n=1):
    if iid in ITEMS:
        c = ITEMS[iid]['comps']
        if ITEMS[iid]['base'] != TOTEM and not c.get('minecraft:max_stack_size'):
            comps = exact_comps(iid)          # a trade-in: the EXACT item as it was sold (name, lore, enchantments, attributes)
        else:
            comps = {k: c[k] for k in COST_KEYS if k in c}
        return {'id': ITEMS[iid]['base'], 'count': Int(n), 'components': comps}
    return {'id': iid if ':' in iid else 'minecraft:' + iid, 'count': Int(n)}


CURRENCY = {'token', 'medallion', 'trophy', 'lucky_token', 'blood_crystal', 'diamond', 'emerald', 'netherite_ingot'}
PRICE_SCALE = {'token': 1.5, 'medallion': 1.5}      # 1.7 economy: goods cost 50% more (currency exchanges unchanged)


def scaled(c, sell):
    iid, n = c[0], (c[1] if len(c) > 1 else 1)
    if sell[0] in CURRENCY or iid not in PRICE_SCALE: return (iid, n)
    return (iid, max(1, -(-int(n * PRICE_SCALE[iid] * 2) // 2)))       # x1.5, rounded up


def offer(buy, sell, buyB=None):
    buy, buyB, sa, sb = ECON.apply(buy, sell, buyB)          # 1.10 rebalance (economy.py)
    if sa: buy = scaled(buy, sell)
    if buyB and sb: buyB = scaled(buyB, sell)
    o = {'buy': cost(*buy), 'sell': stack(*sell), 'maxUses': Int(2147483647), 'uses': Int(0),
         'rewardExp': B(0), 'xp': Int(0), 'priceMultiplier': F(0.0), 'specialPrice': Int(0), 'demand': Int(0)}
    if buyB:
        o['buyB'] = cost(*buyB)
    s = sell[0].split(':')[-1]
    if sell[0] not in ITEMS and s not in CURRENCY:                 # 2.30: a vanilla purchase is marked so the Scrap Bin knows it was bought
        o['sell']['components'] = {'minecraft:custom_data': {'bm_from': B(1)}}
    return o


def loot_entry(iid, count=None, extra_fn=()):
    it = ITEMS[iid]
    fns = [{'function': 'minecraft:set_components', 'components': it['comps']}]
    if count is not None:
        fns.append({'function': 'minecraft:set_count', 'count': count})
    return {'type': 'minecraft:item', 'name': it['base'], 'functions': fns + list(extra_fn)}


def uni(a, b):
    return {'type': 'minecraft:uniform', 'min': a, 'max': b}


KILLED = {'condition': 'minecraft:killed_by_player'}


def chance(p):
    return {'condition': 'minecraft:random_chance', 'chance': p}


def tellraw(who, parts):
    return f'tellraw {who} {snbt(parts)}'


def title(who, kind, comp):
    return f'title {who} {kind} {snbt(comp)}'


PREFIX = [T('[', 'dark_gray'), T('Black Market', 'dark_purple', bold=True), T('] ', 'dark_gray')]


# ================================================================ NPCs / TRADES
def npc_offers():
    O = {}
    O['fence'] = [
        offer(('diamond', 4), ('token', 1)),
        offer(('emerald', 24), ('token', 1)),
        offer(('netherite_ingot', 1), ('token', 3)),
        offer(('token', 9), ('medallion', 1)),
        offer(('medallion', 6), ('trophy', 1)),
        offer(('token', 2), ('sealed_map_market', 1)),
        offer(('token', 1), ('sealed_map_graveyard', 1)),
    ]
    arms_buy = ['kokiri_sword', 'cranky_pick', 'hammer_bro_hatchet', 'hylian_shield',      # 2.24: the Fairy Bow is Cecil's
                'zora_trident', 'super_hammer']
    arms_ids = set(arms_buy) | {'master_sword', 'biggoron_sword', 'minecart_pick', 'kong_krusher', 'koopa_cleaver',
                                'giga_greataxe', 'ultra_hammer'}      # 2.24: the Hero's Bow and Bow of Light are Cecil's now
    O['arms'] = [offer(PRICES[i], (i, 1)) for i in arms_buy]
    O['arms'] += [offer((f, 1), (to, 1), (cur, n)) for f, cur, n, to in UPGRADES if to in arms_ids]
    O['outfitter'] = [offer(PRICES[f'smuggler_{p}'], (f'smuggler_{p}', 1)) for p in I.PIECES]
    O['outfitter'] += [offer((f, 1), (to, 1), (cur, n)) for f, cur, n, to in UPGRADES if to.startswith(('kingpin_', 'hero_'))]
    for i in ['architect_gauntlet', 'rocs_feather', 'super_leaf', 'mini_mushroom', 'mega_mushroom', 'lens_of_truth',
              'pegasus_boots', 'bouncy_boots', 'crown', 'party_hat', 'top_hat', 'halo', 'flame_boots', 'heart_boots', 'soul_boots']:
        O['outfitter'].append(offer(PRICES[i], (i, 1)))
    O['chef'] = []
    for fid, buff, tier, eff, amp, meat, ename, t1 in FEASTS:
        if tier == 1:
            O['chef'].append(offer((meat, 3), (fid, 1), ('token', 4)))
        else:
            O['chef'].append(offer((meat, 6), (fid, 1), ('medallion', 2)))
    for meat in ['prime_beef', 'prime_pork', 'prime_mutton', 'prime_chicken', 'prime_rabbit']:
        O['chef'].append(offer((meat, 2), ('token', 1)))
    O['professor'] = [offer(('token', 1), (b, 1)) for b in BOOKS]
    O['professor'] += [offer(('token', 1), ('sealed_map_graveyard', 1)), offer(('token', 2), ('sealed_map_market', 1))]
    O['professor'] += [offer(('token', 3), (f'skin_{s}', 1)) for s, _, _ in SKINS] + [offer(('token', 1), ('skin_restore', 1))]
    O['lucky'] = [
        offer(('lucky_token', 1), ('scratch_card', 1)),
        offer(('lucky_token', 4), ('scratch_card', 5)),
        offer(('token', 5), ('lucky_token', 1)),
        offer(('token', 6), ('minish_cap', 1)),
        offer(('lucky_token', 3), ('lucky_charm', 1)),
    ]
    pawn = [offer(('medallion', 1), ('token', 6)), offer(('trophy', 1), ('medallion', 4)), offer(('token', 1), ('diamond', 2))]
    for iid, (cur, n) in PRICES.items():
        if CATEGORY.get(iid) in ('gear', 'builder', 'cosmetic') and iid != 'lucky_seven':
            pawn.append(offer((iid, 1), ECON.pawn(iid, (cur, n))))
    pawn.append(offer(('lucky_seven', 1), ('trophy', 3)))
    O['pawn'] = pawn
    O['captain'] = [
        offer(('gold_block', 4), ('token', 1)),
        offer(('token', 8), ('medallion', 1)),
        offer(('lucky_token', 4), ('scratch_card', 6)),
        offer(('token', 2), ('aged_cheddar', 1)),
        offer(('medallion', 3), ('pirate_hat', 1)),
        offer(('medallion', 6), ('cheese_grater', 1), ('lucky_token', 1)),
        offer(('trophy', 1), ('rat_king_crown', 1)),
    ]
    return O


NPCS = {
    # tag: (kind, display name, color, profession, villager type, sprite)
    'fence': ('wandering', 'The Fence', 'gold', None, None, None),
    'arms': ('villager', "Vinny 'Two-Blades'", 'red', 'weaponsmith', 'swamp', None),
    'outfitter': ('villager', 'Madame Velour, Outfitter', 'light_purple', 'armorer', 'taiga', None),
    'pawn': ('villager', 'Old Barnaby', 'white', 'cleric', 'swamp', None),
    'chef': ('rat', 'Chef Fromage', 'gold', 'butcher', 'plains', 'bm:rat_chef'),
    'professor': ('rat', 'Prof. Whiskerton', 'aqua', 'librarian', 'plains', 'bm:rat_prof'),
    'lucky': ('rat', 'Lucky Whiskers', 'green', 'cartographer', 'plains', 'bm:rat_lucky'),
    'captain': ('rat', 'Capt. Cheddarbeard', 'yellow', 'fisherman', 'plains', 'bm:rat_pirate'),
}
NPCS.update(P.NEW_NPCS)
NPCS.update(R34.NEW_NPCS)
NPCS.update(R45.NEW_NPCS)


def all_offers():
    """Every trader's complete, current offer list (one source of truth for spawning AND for refreshing old traders)."""
    O = npc_offers()
    P.extend_offers(O, offer)
    if PHASE2: p2.extend_offers(O, offer)
    R.extend_offers(O, offer)
    R20.extend_offers(O, offer)
    R21.extend_offers(O, offer)
    R33.extend_offers(O, offer)
    R34.extend_offers(O, offer)
    R35.extend_offers(O, offer)
    R36.extend_offers(O, offer)
    R38.extend_offers(O, offer)
    R39.extend_offers(O, offer)
    R41.extend_offers(O, offer)
    R43.extend_offers(O, offer)
    R45.extend_offers(O, offer)
    R46.extend_offers(O, offer)
    R47.extend_offers(O, offer)
    R49.extend_offers(O, offer)
    R50.extend_offers(O, offer)
    R51.extend_offers(O, offer)
    return O


def gen_npcs():
    O = all_offers()
    disp = ['execute if entity @s[tag=bm.npc.%s] run function bm:npc/%s' % (k, k) for k in list(NPCS) + ['deco_rat', 'deco_key']]
    fn('npc/spawn', disp + ['kill @s'])
    fin = ['execute rotated as @s run tp @e[tag=bm.new,distance=..2] ~ ~ ~ ~ 0',
           'tag @e[tag=bm.new,distance=..2] remove bm.new']
    for k, (kind, name, color, prof, vtype, sprite) in NPCS.items():
        base = {'NoAI': B(1), 'Invulnerable': B(1), 'PersistenceRequired': B(1),
                'Tags': ['bm.npc', 'bm.new', f'bm.npc_{k}'],
                'CustomName': T(name, color, bold=True), 'CustomNameVisible': B(0),     # name shows only when you look at them
                'Offers': {'Recipes': O[k]}}
        cmds = []
        if kind == 'wandering':
            base['DespawnDelay'] = Int(0)
            cmds.append(f'summon minecraft:wandering_trader ~ ~ ~ {snbt(base)}')
        else:
            base['VillagerData'] = {'type': f'minecraft:{vtype}', 'profession': f'minecraft:{prof}', 'level': Int(5)}
            base['Xp'] = Int(250)
            base['VillagerDataFinalized'] = B(1)
            if kind == 'custom':                  # 2.24: an invisible hitbox; the NPC's own module builds the model
                base['Silent'] = B(1)
                base['active_effects'] = [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1),
                                           'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}]
            if kind == 'rat':
                base['Silent'] = B(1)
                base['active_effects'] = [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1),
                                           'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}]
                base['attributes'] = [{'id': 'minecraft:scale', 'base': D(0.7)}]      # 2.15: was 0.5 - trader rats read as traders now
            cmds.append(f'summon minecraft:villager ~ ~ ~ {snbt(base)}')
            if kind == 'rat':
                cmds.append(rat_sprite(sprite, ['bm.npc', 'bm.new', 'bm.rat_sprite']))
            if kind == 'custom':
                cmds.append(f'function bm:p45/cecil/rig')
        fn(f'npc/{k}', cmds + fin)
    fn('npc/deco_rat', [rat_sprite('bm:rat_pirate', ['bm.npc', 'bm.new', 'bm.rat_sprite'], 0.7)] + fin)
    key = {'Tags': ['bm.npc', 'bm.new', 'bm.key_display'], 'item': stack('market_key'), 'item_display': 'ground',
           'billboard': 'vertical',
           'brightness': {'block': Int(15), 'sky': Int(15)},
           'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                              'translation': [F(0), F(0), F(0)], 'scale': [F(1.2), F(1.2), F(1.2)]}}
    fn('npc/deco_key', [f'summon minecraft:item_display ~ ~ ~ {snbt(key)}'] + fin)
    return O


def rat_sprite(model, tags, scale=1.26):          # 2.15: traders are 1.4x the old 0.9 (crowd/walkers pass their own)
    """A 3D block-model rat (1.7) standing where the trader is, facing the trader's way (the NPC fin step copies the
    marker's yaw). Model ids: bm:rat_<v> -> bm:rat3d_<v>."""
    model = model.replace('bm:rat_', 'bm:rat3d_')
    scale = round(scale * 0.95, 3)
    d = {'Tags': tags, 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': model}},
         'item_display': 'fixed', 'billboard': 'fixed', 'teleport_duration': Int(6), 'brightness': {'block': Int(12), 'sky': Int(8)},
         'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                            'translation': [F(0), F(scale / 2), F(0)], 'scale': [F(scale), F(scale), F(scale)]}}
    return f'summon minecraft:item_display ~ ~ ~ {snbt(d)}'


# ================================================================ MOBS
ARMORED = {  # type: (base hp, weapon kind)
    'zombie': (20, 'sword'), 'husk': (20, 'sword'), 'drowned': (20, 'trident'), 'skeleton': (20, 'bow'),
    'stray': (20, 'bow'), 'bogged': (16, 'bow'), 'parched': (20, 'bow'), 'wither_skeleton': (20, 'sword'),   # 1.17: + parched (26.x desert skeleton)
    'pillager': (24, 'crossbow'), 'vindicator': (24, 'axe'),
    'zombie_villager': (20, 'sword'), 'zombified_piglin': (20, 'sword'), 'piglin': (16, 'sword'), 'piglin_brute': (50, 'axe'),
}
UNARMORED = {'spider': 16, 'cave_spider': 12, 'creeper': 20, 'enderman': 40, 'witch': 26, 'blaze': 20,
             'hoglin': 40, 'ghast': 10, 'shulker': 30, 'phantom': 20, 'breeze': 30}
ANIMALS = {'pig': 'prime_pork', 'cow': 'prime_beef', 'mooshroom': 'prime_beef', 'sheep': 'prime_mutton',
           'chicken': 'prime_chicken', 'rabbit': 'prime_rabbit'}
ANIMAL_HP = {'pig': 10, 'cow': 10, 'mooshroom': 10, 'sheep': 8, 'chicken': 4, 'rabbit': 3}

WEAPON = {
    'elite': {'sword': 'minecraft:diamond_sword[enchantments={"minecraft:sharpness":5}]',
              'bow': 'minecraft:bow[enchantments={"minecraft:power":5}]',
              'crossbow': 'minecraft:crossbow[enchantments={"minecraft:quick_charge":3,"minecraft:piercing":4}]',
              'axe': 'minecraft:diamond_axe[enchantments={"minecraft:sharpness":5}]',
              'trident': 'minecraft:trident[enchantments={"minecraft:impaling":5}]'},
    'champion': {'sword': 'minecraft:netherite_sword[enchantments={"minecraft:sharpness":6,"minecraft:fire_aspect":2}]',
                 'bow': 'minecraft:bow[enchantments={"minecraft:power":6,"minecraft:punch":2,"minecraft:flame":1}]',
                 'crossbow': 'minecraft:crossbow[enchantments={"minecraft:quick_charge":3,"minecraft:multishot":1}]',
                 'axe': 'minecraft:netherite_axe[enchantments={"minecraft:sharpness":6}]',
                 'trident': 'minecraft:trident[enchantments={"minecraft:impaling":6}]'},
}
NO_DROPS = {'drop_chances': {k: F(0.0) for k in ['head', 'chest', 'legs', 'feet', 'mainhand', 'offhand']}}


def mob_name(prefix, color, t, bold=False):
    d = {'text': prefix, 'color': color, 'extra': [{'translate': f'entity.minecraft.{t}'}]}
    if bold: d['bold'] = True
    return d


def gen_mobs():
    second = []
    for t in list(ARMORED) + list(UNARMORED):
        second.append(f'execute as @e[type=minecraft:{t},tag=!bm.seen] at @s run function bm:mobs/init/{t}')
        fn(f'mobs/init/{t}', [
            'tag @s add bm.seen',
            f'execute if score #active bm.bm matches 1 if dimension minecraft:overworld run return run function bm:mobs/blood_roll/{t}',
            'execute store result score #r bm.rng run random value 1..1000',
            f'execute if score #r bm.rng matches 1..6 run return run function bm:mobs/lucky/{t}',
            f'execute if score #r bm.rng matches 7..18 run return run function bm:mobs/champion/{t}',
            f'execute if score #r bm.rng matches 19..68 run return run function bm:mobs/elite/{t}',
        ])
        hp = ARMORED[t][0] if t in ARMORED else UNARMORED[t]
        # ---- elite
        lines = [f'data merge entity @s {snbt(dict(NO_DROPS, DeathLootTable=f"bm:entities/elite/{t}", CustomName=mob_name("Elite ", "gold", t)))}',
                 'tag @s add bm.elite', 'tag @s add bm.tiered']
        if t in ARMORED:
            for slot, piece in [('head', 'helmet'), ('chest', 'chestplate'), ('legs', 'leggings'), ('feet', 'boots')]:
                lines.append(f'item replace entity @s armor.{slot} with minecraft:diamond_{piece}[enchantments={{"minecraft:protection":4,"minecraft:unbreaking":3}}]')
            lines.append(f'item replace entity @s weapon.mainhand with {WEAPON["elite"][ARMORED[t][1]]}')
            mhp = hp * 2
        else:
            for e in ['strength', 'resistance', 'speed']:
                lines.append(f'effect give @s minecraft:{e} infinite 0 true')
            lines.append('attribute @s minecraft:scale base set 1.15')
            mhp = hp * 2
        lines += [f'attribute @s minecraft:max_health base set {mhp}', f'data modify entity @s Health set value {mhp}.0f',
                  'attribute @s minecraft:follow_range base set 40']
        fn(f'mobs/elite/{t}', lines)
        # ---- champion
        lines = [f'data merge entity @s {snbt(dict(NO_DROPS, DeathLootTable=f"bm:entities/champion/{t}", CustomName=mob_name("Champion ", "red", t, True)))}',
                 'tag @s add bm.champion', 'tag @s add bm.tiered']
        if t in ARMORED:
            for slot, piece in [('head', 'helmet'), ('chest', 'chestplate'), ('legs', 'leggings'), ('feet', 'boots')]:
                lines.append(f'item replace entity @s armor.{slot} with minecraft:netherite_{piece}[enchantments={{"minecraft:protection":5,"minecraft:unbreaking":5,"minecraft:thorns":2}}]')
            lines.append(f'item replace entity @s weapon.mainhand with {WEAPON["champion"][ARMORED[t][1]]}')
            lines.append('attribute @s minecraft:scale base set 1.3')
            mhp = hp * 4
        else:
            for e, a in [('strength', 1), ('resistance', 1), ('speed', 1), ('regeneration', 0)]:
                lines.append(f'effect give @s minecraft:{e} infinite {a} true')
            lines.append('attribute @s minecraft:scale base set 1.4')
            mhp = hp * 3
        if t == 'creeper':
            lines.append('data merge entity @s {ExplosionRadius:4b}')
        lines += [f'attribute @s minecraft:max_health base set {mhp}', f'data modify entity @s Health set value {mhp}.0f',
                  'attribute @s minecraft:movement_speed modifier add bm:champion 0.15 add_multiplied_base',
                  'attribute @s minecraft:knockback_resistance base set 0.6',
                  'attribute @s minecraft:follow_range base set 48',
                  f'execute positioned ~1 ~ ~ run summon minecraft:{t} ~ ~ ~ {{Tags:["bm.seen","bm.minion"]}}',
                  f'execute positioned ~-1 ~ ~1 run summon minecraft:{t} ~ ~ ~ {{Tags:["bm.seen","bm.minion"]}}',
                  'execute as @a[distance=..24] unless score @s bm.csnd matches 1 run playsound minecraft:entity.wither.ambient hostile @s ~ ~ ~ 0.4 1.6',
                  'scoreboard players set @a[distance=..24] bm.csnd 1']
        fn(f'mobs/champion/{t}', lines)
        # ---- lucky
        lhp = int(hp * 1.5)
        fn(f'mobs/lucky/{t}', [
            f'data merge entity @s {snbt({"DeathLootTable": f"bm:entities/lucky/{t}", "CustomName": mob_name("Lucky ", "yellow", t, True)})}',
            'tag @s add bm.lucky', 'tag @s add bm.tiered',
            f'attribute @s minecraft:max_health base set {lhp}', f'data modify entity @s Health set value {lhp}.0f'])
        # ---- loot tables
        vanilla = {'rolls': 1, 'entries': [{'type': 'minecraft:loot_table', 'value': f'minecraft:entities/{t}'}]}
        wjson(f'bm/loot_table/entities/elite/{t}.json', {'type': 'minecraft:entity', 'pools': [
            vanilla,
            {'rolls': 1, 'entries': [loot_entry('token')], 'conditions': [KILLED]},
            {'rolls': 1, 'entries': [loot_entry('token', uni(1, 2))], 'conditions': [KILLED, chance(0.35)]}]})
        wjson(f'bm/loot_table/entities/champion/{t}.json', {'type': 'minecraft:entity', 'pools': [
            vanilla,
            {'rolls': 1, 'entries': [loot_entry('token', uni(3, 5))], 'conditions': [KILLED]},
            {'rolls': 1, 'entries': [loot_entry('medallion')], 'conditions': [KILLED, chance(0.3)]},
            {'rolls': 1, 'entries': [loot_entry('lucky_token')], 'conditions': [KILLED, chance(0.1)]}]})
        wjson(f'bm/loot_table/entities/lucky/{t}.json', {'type': 'minecraft:entity', 'pools': [
            vanilla,
            {'rolls': 1, 'entries': [loot_entry('lucky_token')], 'conditions': [KILLED]},
            {'rolls': 1, 'entries': [loot_entry('lucky_token')], 'conditions': [KILLED, chance(0.4)]}]})
    # ---- animals
    for a, meat in ANIMALS.items():
        second.append(f'execute as @e[type=minecraft:{a},tag=!bm.seen] at @s run function bm:mobs/init/{a}')
        lines = ['tag @s add bm.seen']
        if a == 'chicken':
            lines += ['execute if data entity @s {variant:"minecraft:warm"} store result score #r bm.rng run random value 1..30',
                      'execute if data entity @s {variant:"minecraft:warm"} if score #r bm.rng matches 1 run return run function bm:mobs/goose']
        lines += ['execute store result score #r bm.rng run random value 1..100',
                  f'execute if score #r bm.rng matches 1 run function bm:mobs/prime/{a}']
        fn(f'mobs/init/{a}', lines)
        hp = ANIMAL_HP[a] * 2
        fn(f'mobs/prime/{a}', [
            f'data merge entity @s {snbt({"DeathLootTable": f"bm:entities/prime/{a}", "CustomName": mob_name("Prime ", "gold", a)})}',
            'tag @s add bm.prime', 'attribute @s minecraft:scale base set 1.15',
            f'attribute @s minecraft:max_health base set {hp}', f'data modify entity @s Health set value {hp}.0f'])
        wjson(f'bm/loot_table/entities/prime/{a}.json', {'type': 'minecraft:entity', 'pools': [
            {'rolls': 1, 'entries': [{'type': 'minecraft:loot_table', 'value': f'minecraft:entities/{a}'}]},
            {'rolls': 1, 'entries': [loot_entry(meat, uni(1, 2))]}]})
    fn('mobs/goose', [
        f'data merge entity @s {snbt({"DeathLootTable": "bm:entities/lucky_goose", "PersistenceRequired": B(1), "CustomName": T("Lucky Golden Goose", "gold", bold=True)})}',
        'tag @s add bm.goose', 'attribute @s minecraft:scale base set 1.25',
        'attribute @s minecraft:max_health base set 20', 'data modify entity @s Health set value 20.0f'])
    wjson('bm/loot_table/entities/lucky_goose.json', {'type': 'minecraft:entity', 'pools': [
        {'rolls': 1, 'entries': [{'type': 'minecraft:loot_table', 'value': 'minecraft:entities/chicken'}]},
        {'rolls': 1, 'entries': [loot_entry('lucky_token', uni(2, 4))]},
        {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:gold_nugget',
                                  'functions': [{'function': 'minecraft:set_count', 'count': uni(3, 8)}]}]}]})
    return second


# ================================================================ FEASTS / BUFFS
BUFFS = ['health', 'strength', 'resistance', 'haste', 'speed']
BUFF_EFF = {'health': 'minecraft:health_boost', 'strength': 'minecraft:strength', 'resistance': 'minecraft:resistance',
            'haste': 'minecraft:haste', 'speed': 'minecraft:speed'}


def consume_adv(iid, func):
    wjson(f'bm/advancement/consume/{iid}.json', {
        'criteria': {'ate': {'trigger': 'minecraft:consume_item', 'conditions': {
            'item': {'items': ITEMS[iid]['base'], 'predicates': {'minecraft:custom_data': snbt(ITEMS[iid]['custom'])}}}}},
        'rewards': {'function': func}})


def gen_feasts():
    for fid, buff, tier, eff, amp, meat, ename, t1 in FEASTS:
        consume_adv(fid, f'bm:feast/{fid}')
        sc = f'bm.b_{buff}'
        refund = [give(fid)]
        fn(f'feast/{fid}_dup', refund + [title('@s', 'actionbar', T(f'You already carry this blessing. (Refunded)', 'gray'))])
        body = [f'advancement revoke @s only bm:consume/{fid}']
        if tier == 2:
            fn(f'feast/{fid}_need', refund + [
                title('@s', 'actionbar', T(f'Eat the {t1} first! (Refunded)', 'red')),
                'playsound minecraft:entity.villager.no player @s ~ ~ ~ 1 1'])
            body.append(f'execute unless score @s {sc} matches 1.. run return run function bm:feast/{fid}_need')
        body += [f'execute if score @s {sc} matches {tier}.. run return run function bm:feast/{fid}_dup',
                 f'scoreboard players set @s {sc} {tier}',
                 f'effect give @s {eff} infinite {amp} true',
                 title('@s', 'actionbar', T(f'Blessing of {ename} {"I" if tier == 1 else "II"} — until death', 'gold')),
                 'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.7 1.4',
                 'particle minecraft:happy_villager ~ ~1 ~ 0.4 0.6 0.4 0 20']
        fn(f'feast/{fid}', body)
    re = []
    for b in BUFFS:
        re.append(f'effect give @a[scores={{bm.b_{b}=1}}] {BUFF_EFF[b]} infinite 0 true')
        re.append(f'effect give @a[scores={{bm.b_{b}=2}}] {BUFF_EFF[b]} infinite 1 true')
    fn('buffs/reapply', re)
    od = [f'execute if score @s bm.b_{b} matches 1.. run tag @s add bm.hadbuff' for b in BUFFS]
    od.append(tellraw('@s[tag=bm.hadbuff]', PREFIX + [T('Your feast blessings fade with your last breath...', 'gray', italic=True)]))
    od += [f'scoreboard players set @s bm.b_{b} 0' for b in BUFFS]
    od += ['tag @s remove bm.hadbuff', 'scoreboard players set @s bm.deaths 0']
    fn('buffs/on_death', od)


# ================================================================ LUCKY SCRATCH CARDS
def gen_lucky():
    consume_adv('scratch_card', 'bm:lucky/scratch')
    fn('lucky/scratch', ['advancement revoke @s only bm:consume/scratch_card', 'scoreboard players set @s bm.sct 10'])
    fn('lucky/reveal', [
        'scoreboard players reset @s bm.sct',
        'execute store result score @s bm.rng run random value 1..1000',
        'execute if score @s bm.rng matches 1..80 run return run function bm:lucky/win_nothing',
        'execute if score @s bm.rng matches 81..470 run return run function bm:lucky/win_tokens',
        'execute if score @s bm.rng matches 471..680 run return run function bm:lucky/win_lucky',
        'execute if score @s bm.rng matches 681..860 run return run function bm:lucky/win_medallion',
        'execute if score @s bm.rng matches 861..955 run return run function bm:lucky/win_medallions',
        'execute if score @s bm.rng matches 956..994 run return run function bm:lucky/win_trophy',
        'function bm:lucky/win_lucky7'])
    def win(name, rewards, msg, color, sound='minecraft:block.note_block.pling', pitch=1.6):
        fn(f'lucky/{name}', rewards + [
            'title @s times 5 40 10', title('@s', 'title', T('', 'white')),
            title('@s', 'subtitle', T(msg, color)),
            f'playsound {sound} player @s ~ ~ ~ 1 {pitch}',
            'particle minecraft:wax_on ~ ~1.2 ~ 0.4 0.5 0.4 0 12'])
    win('win_nothing', ['playsound minecraft:block.note_block.bass player @s ~ ~ ~ 1 0.5'], 'Nothing... better luck next time!', 'gray', 'minecraft:entity.villager.no', 1)
    fn('lucky/win_tokens_n', ['execute store result score @s bm.rng run random value 1..3',
                              'execute if score @s bm.rng matches 1 run ' + give('token', 1),
                              'execute if score @s bm.rng matches 2 run ' + give('token', 2),
                              'execute if score @s bm.rng matches 3 run ' + give('token', 3)])
    win('win_tokens', ['function bm:lucky/win_tokens_n'], 'Winner! Black Market Tokens!', 'gold', 'minecraft:entity.experience_orb.pickup', 0.8)
    win('win_lucky', [give('lucky_token', 2)], 'Winner! 2 Lucky Tokens!', 'green', 'minecraft:block.amethyst_block.chime', 1.2)
    win('win_medallion', [give('medallion', 1)], 'Winner! A Medallion!', 'light_purple', 'minecraft:block.note_block.pling', 1.4)
    win('win_medallions', [give('medallion', 3)], 'BIG WIN! 3 Medallions!', 'light_purple', 'minecraft:block.bell.use', 1.0)
    win('win_trophy', [give('trophy', 1), tellraw('@a', PREFIX + [{'selector': '@s', 'color': 'yellow'}, T(' scratched a ', 'gray'), T('Black Market Trophy', '#ffb300', bold=True), T('!', 'gray')])],
        'JACKPOT! A Black Market Trophy!', '#ffb300', 'minecraft:entity.player.levelup', 0.8)
    # fanfare first (winner only); one second later the winner's own fireworks (bm.l7 timer in tick)
    win('win_lucky7', [give('lucky_seven', 1),
                       tellraw('@a', PREFIX + [{'selector': '@s', 'color': 'yellow'}, T(' hit the legendary ', 'gray'), T('LUCKY 7', '#ffd700', bold=True), T('!!!', 'gold')]),
                       'scoreboard players set @s bm.l7 20',
                       'particle minecraft:totem_of_undying ~ ~1 ~ 0.6 1 0.6 0.4 120'],
        '7 7 7  —  LUCKY 7!!!', '#ffd700', 'minecraft:ui.toast.challenge_complete', 1.0)
    fn('lucky/l7_fireworks', ['scoreboard players reset @s bm.l7',
                              'playsound minecraft:entity.firework_rocket.large_blast player @s ~ ~ ~ 1 1',
                              'playsound minecraft:entity.firework_rocket.twinkle player @s ~ ~ ~ 0.8 1',
                              'particle minecraft:firework ~ ~3 ~ 1.2 1.2 1.2 0.1 60'])


# ================================================================ MAPS / SKINS
def gen_maps_skins():
    for iid, table, label in [('sealed_map_market', 'market', 'a Black Market'), ('sealed_map_graveyard', 'graveyard', 'a haunted graveyard'),
                              ('sealed_map_frog', 'frog_hut', "the Frog with Mustache's hut")]:
        consume_adv(iid, f'bm:maps/open_{table}')
        fn(f'maps/open_{table}', [f'advancement revoke @s only bm:consume/{iid}',
                                  f'loot give @s loot bm:maps/{table}',
                                  title('@s', 'actionbar', T(f'The seal cracks... the map reveals {label}.', 'aqua'))])
    for table, dest, nm, deco in [('market', 'bm:black_market', "Smuggler's Map", 'minecraft:red_x'),
                                  ('graveyard', 'bm:graveyard', "Gravedigger's Map", 'minecraft:red_x'),
                                  ('frog_hut', 'bm:frog_hut', "Croaker's Map", 'minecraft:swamp_hut')]:
        wjson(f'bm/loot_table/maps/{table}.json', {'type': 'minecraft:command', 'pools': [{'rolls': 1, 'entries': [{
            'type': 'minecraft:item', 'name': 'minecraft:filled_map', 'functions': [     # 26.3: exploration_map stamps the input item, so start from a filled map
                {'function': 'minecraft:exploration_map', 'destination': dest, 'decoration': deco, 'zoom': 2,
                 'search_radius': 100, 'skip_existing_chunks': False},
                {'function': 'minecraft:set_name', 'target': 'item_name', 'name': T(nm, 'aqua')}]}]}]})
    for sid, label, model in SKINS:
        iid = f'skin_{sid}'
        consume_adv(iid, f'bm:skins/{sid}')
        wjson(f'bm/item_modifier/skins/{sid}.json', {'function': 'minecraft:set_components', 'components': {'minecraft:item_model': model}})
        fn(f'skins/{sid}_fail', [give(iid), title('@s', 'actionbar', T('Hold a tool, weapon or armor piece in your OFF hand! (Refunded)', 'red'))])
        fn(f'skins/{sid}', [f'advancement revoke @s only bm:consume/{iid}',
                            f'execute unless items entity @s weapon.offhand *[minecraft:max_damage] run return run function bm:skins/{sid}_fail',
                            f'item modify entity @s weapon.offhand bm:skins/{sid}',
                            'playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 1 1.2',
                            'particle minecraft:enchant ~ ~1 ~ 0.4 0.6 0.4 0.5 30',
                            title('@s', 'actionbar', T(f'Reskinned: {label}!', 'aqua'))])
    consume_adv('skin_restore', 'bm:skins/restore')
    fn('skins/restore_fail', [give('skin_restore'), title('@s', 'actionbar', T('Hold the reskinned item in your OFF hand! (Refunded)', 'red'))])
    fn('skins/restore', ['advancement revoke @s only bm:consume/skin_restore',
                         'execute unless items entity @s weapon.offhand *[minecraft:max_damage] run return run function bm:skins/restore_fail',
                         'data remove storage bm:tmp item',
                         'data modify storage bm:tmp item set from entity @s equipment.offhand',
                         'execute unless data storage bm:tmp item.id run return run function bm:skins/restore_fail',
                         'function bm:skins/restore_m with storage bm:tmp item',
                         'playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 1 0.8',
                         title('@s', 'actionbar', T('Original look restored.', 'white'))])
    fn('skins/restore_m', ['$item modify entity @s weapon.offhand {function:"minecraft:set_components",components:{"minecraft:item_model":"$(id)"}}'])


# ================================================================ CHEST LOOT BONUS
CHESTS = {  # table: (token chance %, max tokens, medallion chance %, lucky chance %)
    'simple_dungeon': (20, 1, 0, 5), 'abandoned_mineshaft': (15, 1, 0, 3), 'desert_pyramid': (25, 2, 0, 5),
    'jungle_temple': (25, 2, 0, 5), 'stronghold_corridor': (30, 2, 3, 5), 'stronghold_crossing': (30, 2, 3, 5),
    'stronghold_library': (35, 2, 5, 5), 'buried_treasure': (50, 3, 5, 10), 'shipwreck_treasure': (30, 2, 0, 5),
    'ruined_portal': (15, 1, 0, 3), 'bastion_treasure': (60, 3, 15, 10), 'bastion_other': (25, 2, 3, 5),
    'nether_bridge': (25, 2, 3, 5), 'end_city_treasure': (40, 3, 10, 10), 'woodland_mansion': (40, 3, 8, 8),
    'pillager_outpost': (25, 2, 0, 5), 'ancient_city': (40, 3, 10, 8), 'igloo_chest': (20, 1, 0, 5),
}


def gen_chest_loot():
    for t, (tc, tmax, mc, lc) in CHESTS.items():
        wjson(f'bm/advancement/loot/{t}.json', {
            'criteria': {'opened': {'trigger': 'minecraft:player_generates_container_loot',
                                    'conditions': {'loot_table': f'minecraft:chests/{t}'}}},
            'rewards': {'function': f'bm:loot/{t}'}})
        lines = [f'advancement revoke @s only bm:loot/{t}',
                 'execute store result score @s bm.rng run random value 1..100',
                 f'execute if score @s bm.rng matches 1..{tc} run function bm:loot/tokens_{tmax}']
        if mc:
            lines += ['execute store result score @s bm.rng run random value 1..100',
                      f'execute if score @s bm.rng matches 1..{mc} run function bm:loot/medallion']
        lines += ['execute store result score @s bm.rng run random value 1..100',
                  f'execute if score @s bm.rng matches 1..{lc} run function bm:loot/lucky']
        fn(f'loot/{t}', lines)
    for n in (1, 2, 3):
        fn(f'loot/tokens_{n}', ['execute store result score @s bm.rng run random value 1..%d' % n] +
           [f'execute if score @s bm.rng matches {k} run ' + give('token', k) for k in range(1, n + 1)] +
           [title('@s', 'actionbar', T('You find Black Market Tokens hidden under the loot!', 'gold')),
            'playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.6 0.7'])
    fn('loot/medallion', [give('medallion'), tellraw('@s', PREFIX + [T('A Medallion was tucked inside the chest!', 'light_purple')])])
    fn('loot/lucky', [give('lucky_token'), tellraw('@s', PREFIX + [T('A Lucky Token glints at the bottom of the chest!', 'green')])])


# ================================================================ STRUCTURE LOGIC
def gen_structures_logic():
    # ---- zones (adventure mode inside markets & crypts)
    fn('zone/enter', ['gamemode adventure @s', 'tag @s add bm.adv',
                      title('@s', 'actionbar', T('Protected ground: blocks cannot be broken or placed here.', 'dark_aqua'))])
    fn('zone/exit', ['execute if entity @s[gamemode=adventure] run gamemode survival @s', 'tag @s remove bm.adv'])
    # ---- market door
    fn('market/door', [
        'execute if entity @a[tag=bm.haskey,distance=..3.5,gamemode=!spectator] run return run function bm:market/door_open',
        'execute unless entity @a[distance=..4.5] run function bm:market/door_tryclose'])
    fn('market/door_open', [
        'scoreboard players set @s bm.timer 0',
        'execute if block ~ ~ ~ minecraft:iron_block run playsound minecraft:block.iron_door.open block @a[distance=..16] ~ ~ ~ 1 0.6',
        'execute if block ~ ~ ~ minecraft:iron_block run particle minecraft:wax_off ~ ~ ~ 1 1 0.2 0 20',
        'fill ~-1 ~-1 ~-1 ~1 ~1 ~1 minecraft:light[level=9] replace minecraft:iron_block'])
    fn('market/door_tryclose', [
        'execute unless block ~ ~ ~ minecraft:light run return 0',
        'scoreboard players add @s bm.timer 1',
        'execute if score @s bm.timer matches 8.. run function bm:market/door_close'])
    fn('market/door_close', [
        'fill ~-1 ~-1 ~-1 ~1 ~1 ~1 minecraft:iron_block replace minecraft:light',
        'playsound minecraft:block.iron_door.close block @a[distance=..16] ~ ~ ~ 1 0.6',
        'scoreboard players set @s bm.timer 0'])
    fn('market/kick', [
        'tp @s @e[type=minecraft:marker,tag=bm.market_exit,sort=nearest,limit=1]',
        'title @s times 5 50 15',
        title('@s', 'subtitle', T('Members only. Earn a Black Market Key in a haunted crypt.', 'gray')),
        title('@s', 'title', T('A rat bouncer tosses you out!', 'dark_red')),
        'playsound minecraft:entity.silverfish.hurt hostile @s ~ ~ ~ 1 1.4'])
    # ---- crypt
    # entering wakes the Warden - also during the cool-down after it left (state 3); a looted crypt (4) stays quiet
    fn('crypt/trigger', ['execute as @e[type=minecraft:marker,tag=bm.crypt_ctrl,distance=..24,sort=nearest,limit=1,scores={bm.state=0}] at @s run function bm:crypt/begin',
                         'execute as @e[type=minecraft:marker,tag=bm.crypt_ctrl,distance=..24,sort=nearest,limit=1,scores={bm.state=3}] at @s run function bm:crypt/begin'])
    # Audience: players inside the crypt only (a 29x10x29 box around the controller - covers any rotation,
    # stays below the graveyard surface ~15 blocks up, so people walking the graveyard hear nothing).
    fn('crypt/aud', ['tag @a remove bm.inc', 'execute positioned ~-19 ~-2 ~-19 run tag @a[dx=38,dy=9,dz=38] add bm.inc'])
    fn('crypt/begin', [
        'scoreboard players set @s bm.state 1', 'scoreboard players set @s bm.timer 0',
        'function bm:crypt/aud',
        'effect give @a[tag=bm.inc,gamemode=!spectator,gamemode=!creative] minecraft:darkness 18 0 true',
        'effect give @a[tag=bm.inc,gamemode=!spectator,gamemode=!creative] minecraft:slowness 9 1 true',
        'title @a[tag=bm.inc] times 10 70 25',
        title('@a[tag=bm.inc]', 'subtitle', T('Keep quiet. Keep moving.', 'gray', italic=True)),
        title('@a[tag=bm.inc]', 'title', T('Something is approaching...', 'dark_red', italic=True)),
        'execute as @a[tag=bm.inc] at @s run playsound minecraft:entity.warden.nearby_close hostile @s ~ ~ ~ 1 1'])
    # timeline (ticks): 0 close; 8 shriek from the heart of the maze; 20 the Warden starts digging out of the altar
    # chamber (the game plays its own emerge rumble, ~7 s), so it is already hunting while you are still in the maze.
    beats = [(8, 'minecraft:block.sculk_shrieker.shriek', 0.8, 0.8), (14, 'minecraft:entity.warden.heartbeat', 0.7, 1)]
    fn('crypt/seq', ['scoreboard players add @s bm.timer 1', 'function bm:crypt/aud'] +
       [f'execute if score @s bm.timer matches {t} as @a[tag=bm.inc] at @s run playsound {snd} hostile @s ~ ~ ~ {v} {p}' for t, snd, v, p in beats] +
       ['execute if score @s bm.timer matches 20.. run function bm:crypt/spawn_warden'])
    warden = {'PersistenceRequired': B(1), 'Tags': ['bm.crypt_warden', 'bm.seen'],
              'Brain': {'memories': {'minecraft:is_emerging': {'value': {}, 'ttl': L(134)},
                                     'minecraft:dig_cooldown': {'value': {}, 'ttl': L(72000)}}}}   # never burrows away mid-hunt
    fn('crypt/spawn_warden', [
        f'summon minecraft:warden ~ ~ ~ {snbt(warden)}',
        'particle minecraft:sculk_soul ~ ~0.5 ~ 1 0.2 1 0.02 30',
        'scoreboard players set @s bm.state 2', 'scoreboard players set @s bm.timer 0'])
    # the Warden stays until every player has left the crypt itself (the maze, antechamber and altar chamber),
    # then sinks back into the floor 8 seconds later
    fn('crypt/watch', [
        'function bm:crypt/aud',
        'execute unless entity @e[type=minecraft:warden,tag=bm.crypt_warden,distance=..64] run return run function bm:crypt/to_cooldown',
        'execute if entity @a[tag=bm.inc,gamemode=!spectator] run return run scoreboard players set @s bm.timer 0',
        'scoreboard players add @s bm.timer 1',
        'execute if score @s bm.timer matches 8.. run function bm:crypt/warden_leave'])
    fn('crypt/warden_leave', [
        'execute at @e[type=minecraft:warden,tag=bm.crypt_warden,distance=..64] run particle minecraft:sculk_soul ~ ~1 ~ 0.6 0.6 0.6 0.02 30',
        'execute at @e[type=minecraft:warden,tag=bm.crypt_warden,distance=..64] run playsound minecraft:entity.warden.dig hostile @a[distance=..24] ~ ~ ~ 1 0.8',
        'tp @e[type=minecraft:warden,tag=bm.crypt_warden,distance=..64] ~ -500 ~',
        'function bm:crypt/to_cooldown'])
    # a looted crypt (key taken) is spent for good: state 4, no Warden, no key
    fn('crypt/to_cooldown', ['scoreboard players set @s bm.state 3', 'scoreboard players set @s bm.timer 0',
                             'execute if entity @s[tag=bm.looted] run scoreboard players set @s bm.state 4'])
    fn('crypt/cooldown', [
        'execute if entity @a[distance=..40,gamemode=!spectator] run return run scoreboard players set @s bm.timer 0',
        'scoreboard players add @s bm.timer 1',
        'execute if score @s bm.timer matches 180.. run scoreboard players set @s bm.state 0'])
    fn('crypt/take_key', [
        'execute if entity @e[type=minecraft:marker,tag=bm.crypt_ctrl,tag=bm.looted,distance=..40] run return run function bm:crypt/looted',
        'execute unless entity @e[type=minecraft:marker,tag=bm.crypt_ctrl,distance=..40,scores={bm.state=2}] run return run function bm:crypt/too_early',
        'tag @e[type=minecraft:marker,tag=bm.crypt_ctrl,distance=..40,sort=nearest,limit=1] add bm.looted',
        'execute at @e[type=minecraft:marker,tag=bm.key_altar,distance=..4,sort=nearest,limit=1] run kill @e[type=minecraft:item_display,tag=bm.key_display,distance=..4]',
        give('market_key'), give('sealed_map_market'),
        'tag @s add bm.haskey',
        'title @s times 10 70 20',
        title('@s', 'subtitle', T('A Black Market Key is yours. Now find the way out.', 'gray')),
        title('@s', 'title', T("The skeleton's grip loosens...", '#a96bff')),
        'playsound minecraft:block.end_portal_frame.fill player @s ~ ~ ~ 1 0.6',
        tellraw('@s', PREFIX + [T('Somewhere in the far corner of the maze, stone grinds open. ', 'gray'), T('Find it - quietly.', 'gold', bold=True)]),
        'execute as @e[type=minecraft:marker,tag=bm.crypt_escape,distance=..40,sort=nearest,limit=1] at @s run function bm:crypt/escape_open'])
    fn('crypt/looted', [title('@s', 'actionbar', T("The skeleton's hands are empty. Someone already took this key. Find another crypt.", 'dark_gray'))])
    fn('crypt/too_early', [
        title('@s', 'actionbar', T("The skeleton's grip will not loosen... You feel watched.", 'dark_gray')),
        'execute as @e[type=minecraft:marker,tag=bm.crypt_ctrl,distance=..40,sort=nearest,limit=1,scores={bm.state=0}] at @s run function bm:crypt/begin',
        'execute as @e[type=minecraft:marker,tag=bm.crypt_ctrl,distance=..40,sort=nearest,limit=1,scores={bm.state=3}] at @s run function bm:crypt/begin'])
    fn('crypt/escape_open', [
        'fill ~-1 ~-1 ~-1 ~1 ~1 ~1 minecraft:light[level=6] replace minecraft:cracked_deepslate_bricks',
        'tag @s add bm.open', 'scoreboard players set @s bm.timer 0',
        'playsound minecraft:block.piston.contract block @a[distance=..16] ~ ~ ~ 1 0.5',
        'particle minecraft:dust_plume ~ ~0.5 ~ 0.4 0.6 0.4 0.01 25'])
    fn('crypt/escape_tick', [
        'scoreboard players add @s bm.timer 1',
        'execute if score @s bm.timer matches 10.. unless entity @a[distance=..1.4] run function bm:crypt/escape_close'])
    fn('crypt/escape_close', [
        'fill ~-1 ~-1 ~-1 ~1 ~1 ~1 minecraft:cracked_deepslate_bricks replace minecraft:light',
        'tag @s remove bm.open', 'playsound minecraft:block.piston.extend block @a[distance=..16] ~ ~ ~ 1 0.5'])


# ================================================================ ADMIN
def gen_admin():
    cats = {}
    for iid, c in CATEGORY.items():
        cats.setdefault(c, []).append(iid)
    allc = []
    for c, ids in cats.items():
        fn(f'admin/give/{c}', [give(i, 64 if ITEMS[i]['comps'].get('minecraft:max_stack_size') == 64 else 1) if c == 'currency' else give(i) for i in ids])
        allc.append(c)
    fn('admin/help', [tellraw('@s', PREFIX + [T('Admin commands', 'gold')]),
                      tellraw('@s', [T('/function bm:admin/give/<category>', 'yellow'), T('  categories: ' + ', '.join(sorted(allc)), 'gray')]),
                      tellraw('@s', [T('/function bm:admin/place_market', 'yellow'), T('  builds a Black Market at your feet', 'gray')]),
                      tellraw('@s', [T('/function bm:admin/place_graveyard', 'yellow'), T('  builds a graveyard + crypt at your feet', 'gray')]),
                      tellraw('@s', [T('/function bm:admin/place_frog_hut', 'yellow'), T("  builds the Frog with Mustache's swamp hut at your feet", 'gray')]),
                      tellraw('@s', [T('/locate structure bm:black_market', 'yellow'), T('  /  ', 'gray'), T('bm:graveyard', 'yellow'), T('  /  ', 'gray'), T('bm:frog_hut', 'yellow')]),
                      tellraw('@s', [T('/function bm:admin/uninstall', 'yellow'), T('  stops all loops before removing the pack', 'gray')])])
    fn('admin/place_market', ['place template bm:black_market ~-38 ~-18 ~-96',
                              'tag @e[type=minecraft:marker,tag=bm.mkt,distance=..120] add bm.mclean',     # hand-placed: leave nearby spawners alone
                              tellraw('@s', PREFIX + [T("Market placed: you're at the end of its entrance tunnel. Walk north to the vault door.", 'gray')])])
    fn('admin/place_graveyard', ['place template bm:graveyard ~-15 ~-18 ~-2',
                                 tellraw('@s', PREFIX + [T('Graveyard placed (gate is at your feet, facing south).', 'gray')])])
    fn('admin/uninstall', ['schedule clear bm:loop/fast', 'schedule clear bm:loop/second',
                           *[f'scoreboard objectives remove {o}' for o in OBJECTIVES],
                           tellraw('@s', PREFIX + [T('Loops stopped. Now disable the data pack.', 'gray')])])


# per-player delayed effects: (countdown objective, function run when it reaches 1)
DELAYED = [('bm.sct', 'bm:lucky/reveal'), ('bm.l7', 'bm:lucky/l7_fireworks'), ('bm.sig', 'bm:blood/sigil_infuse')]
OBJECTIVES = ['bm.rng', 'bm.state', 'bm.timer', 'bm.deaths', 'bm.sneak', 'bm.csnd'] + [o for o, f in DELAYED] + [f'bm.b_{b}' for b in BUFFS]


# ================================================================ LOOPS
def gen_loops(second_mob_lines):
    fn('load', [
        'scoreboard objectives add bm.rng dummy', 'scoreboard objectives add bm.state dummy',
        'scoreboard objectives add bm.timer dummy', 'scoreboard objectives add bm.deaths deathCount',
        'scoreboard objectives add bm.sneak minecraft.custom:minecraft.sneak_time', 'scoreboard objectives add bm.csnd dummy',
        *[f'scoreboard objectives add {o} dummy' for o, f in DELAYED],
        *[f'scoreboard objectives add bm.b_{b} dummy' for b in BUFFS],
        'schedule function bm:loop/fast 5t replace', 'schedule function bm:loop/second 20t replace',
        tellraw('@a[tag=!bm.quiet]', PREFIX + [T(('v2.35' if PHASE2 else 'v1.29') + ' loaded. Ops: ', 'gray'), T('/function bm:admin/help', 'yellow')])])
    fn('tick', ['execute as @e[type=minecraft:marker,tag=bm.crypt_ctrl,scores={bm.state=1}] at @s run function bm:crypt/seq',
                *[f'execute as @a[scores={{{o}=1}}] at @s run function {f}' for o, f in DELAYED],
                *[f'scoreboard players remove @a[scores={{{o}=2..}}] {o} 1' for o, f in DELAYED]])
    fast = [
        'tag @a remove bm.haskey',
        'execute as @a if items entity @s container.* *[minecraft:custom_data~{bm:"market_key"}] run tag @s add bm.haskey',
        'execute as @a[tag=!bm.haskey] if items entity @s weapon.offhand *[minecraft:custom_data~{bm:"market_key"}] run tag @s add bm.haskey',
        # zones
        'execute as @a[gamemode=survival,tag=!bm.adv] at @s if block ~ ~-0.2 ~ #bm:zone_floor if entity @e[type=minecraft:marker,tag=bm.zone_m,distance=..28] run function bm:zone/enter',
        'execute as @a[gamemode=survival,tag=!bm.adv] at @s if block ~ ~-0.2 ~ #bm:zone_floor if entity @e[type=minecraft:marker,tag=bm.zone_c,distance=..30] run function bm:zone/enter',
        'execute as @a[tag=bm.adv] at @s unless entity @e[type=minecraft:marker,tag=bm.zone_m,distance=..30] unless entity @e[type=minecraft:marker,tag=bm.zone_c,distance=..32] run function bm:zone/exit',
        'tag @a[tag=bm.adv,gamemode=!adventure] remove bm.adv',
        # market
        'execute as @e[type=minecraft:marker,tag=bm.market_door] at @s run function bm:market/door',
        'execute as @e[type=minecraft:marker,tag=bm.market_hall] at @s as @a[distance=..27,tag=!bm.haskey,gamemode=!creative,gamemode=!spectator] at @s if block ~ ~-0.2 ~ #bm:market_floor run function bm:market/kick',
        # crypt
        'execute as @e[type=minecraft:marker,tag=bm.crypt_trigger] at @s if entity @a[distance=..6,gamemode=!spectator] run function bm:crypt/trigger',
        'execute as @e[type=minecraft:marker,tag=bm.key_altar] at @s as @a[distance=..2,scores={bm.sneak=1..},tag=!bm.haskey,gamemode=!spectator] at @s run function bm:crypt/take_key',
        'scoreboard players reset @a bm.sneak',
    ]
    for cid, (slot, fx) in COSMETICS.items():
        fast.append(f'execute as @a[gamemode=!spectator] if items entity @s {slot} *[minecraft:custom_data~{{bm_fx:"{cid}"}}] at @s run particle {fx}')
    fast.append('schedule function bm:loop/fast 5t replace')
    fn('loop/fast', fast)
    second = ['scoreboard players reset @a bm.csnd'] + list(second_mob_lines) + [
        'execute as @e[tag=bm.tiered,tag=!bm.hhm] at @s unless entity @a[distance=..100] run tp @s ~ -400 ~',
        'execute as @e[tag=bm.lucky] at @s run particle minecraft:wax_on ~ ~1 ~ 0.3 0.5 0.3 0 3',
        'execute as @e[tag=bm.goose] at @s run particle minecraft:wax_on ~ ~0.5 ~ 0.3 0.3 0.3 0 5',
        'execute as @e[tag=bm.prime] at @s run particle minecraft:happy_villager ~ ~0.8 ~ 0.3 0.3 0.3 0 1',
        'execute as @e[type=minecraft:marker,tag=bm.npc_spawn] at @s run function bm:npc/spawn',
        'execute as @e[type=minecraft:marker,tag=bm.market_hall] at @s run tp @e[type=#bm:hostile,distance=..26,tag=!bm.wil_body] ~ -400 ~',
        'execute as @e[type=minecraft:marker,tag=bm.crypt_ctrl] unless score @s bm.state = @s bm.state run scoreboard players set @s bm.state 0',
        'execute as @e[type=minecraft:marker,tag=bm.crypt_ctrl] at @s run effect give @a[distance=..26,gamemode=survival,tag=!bm.adv] minecraft:mining_fatigue 3 2 true',
        'execute as @e[type=minecraft:marker,tag=bm.crypt_ctrl,scores={bm.state=2}] at @s run function bm:crypt/watch',
        'execute as @e[type=minecraft:marker,tag=bm.crypt_ctrl,scores={bm.state=3}] at @s run function bm:crypt/cooldown',
        # 1.7: altar keys placed by older versions stop glowing through walls
        'execute as @e[type=minecraft:item_display,tag=bm.key_display,tag=!bm.kfix] run data merge entity @s {Glowing:0b}',
        'tag @e[type=minecraft:item_display,tag=bm.key_display,tag=!bm.kfix] add bm.kfix',
        'function bm:buffs/reapply',
        'execute as @a[scores={bm.deaths=1..}] run function bm:buffs/on_death',
        'execute as @a if items entity @s armor.head *[minecraft:custom_data~{bm:"lens_of_truth"}] run effect give @s minecraft:night_vision 15 0 true',
        'schedule function bm:loop/second 20t replace',
    ]
    fn('loop/second', second)


# ================================================================ TAGS / WORLDGEN / META
MARKET_BIOMES = ['badlands', 'bamboo_jungle', 'beach', 'birch_forest', 'cherry_grove', 'cold_ocean', 'dark_forest', 'deep_cold_ocean',
                 'deep_frozen_ocean', 'deep_lukewarm_ocean', 'deep_ocean', 'desert', 'dripstone_caves', 'eroded_badlands', 'flower_forest',
                 'forest', 'frozen_ocean', 'frozen_peaks', 'frozen_river', 'grove', 'ice_spikes', 'jagged_peaks', 'jungle', 'lukewarm_ocean',
                 'lush_caves', 'mangrove_swamp', 'meadow', 'mushroom_fields', 'ocean', 'old_growth_birch_forest', 'old_growth_pine_taiga',
                 'old_growth_spruce_taiga', 'pale_garden', 'plains', 'river', 'savanna', 'savanna_plateau', 'snowy_beach', 'snowy_plains',
                 'snowy_slopes', 'snowy_taiga', 'sparse_jungle', 'stony_peaks', 'stony_shore', 'sulfur_caves', 'sunflower_plains', 'swamp',
                 'taiga', 'warm_ocean', 'windswept_forest', 'windswept_gravelly_hills', 'windswept_hills', 'windswept_savanna',
                 'wooded_badlands']        # every Overworld biome except the Deep Dark (no sculk shriekers in market walls)
HOSTILE = ['zombie', 'husk', 'drowned', 'skeleton', 'stray', 'bogged', 'wither_skeleton', 'spider', 'cave_spider', 'creeper',
           'enderman', 'witch', 'blaze', 'slime', 'magma_cube', 'phantom', 'pillager', 'vindicator', 'evoker', 'silverfish',
           'endermite', 'zombie_villager', 'breeze', 'creaking', 'piglin_brute', 'hoglin', 'zoglin', 'ghast', 'shulker',
           'parched', 'ravager', 'vex', 'guardian']


def gen_tags_worldgen():
    wjson('minecraft/tags/function/load.json', {'values': ['bm:load']})
    wjson('minecraft/tags/function/tick.json', {'values': ['bm:tick']})
    wjson('bm/tags/block/market_floor.json', {'values': sorted(set(S.MARKET_FLOOR) | {'minecraft:' + b for b in M2.FLOOR_BLOCKS})})
    wjson('bm/tags/block/zone_floor.json', {'values': sorted(set(S.MARKET_FLOOR + S.CRYPT_FLOOR) | {'minecraft:' + b for b in M2.FLOOR_BLOCKS})})
    wjson('bm/tags/entity_type/hostile.json', {'values': [{'id': f'minecraft:{h}', 'required': False} for h in HOSTILE]})
    # structures
    wjson('bm/tags/worldgen/biome/has_structure/black_market.json', {'values': [f'minecraft:{b}' for b in MARKET_BIOMES]})
    wjson('bm/tags/worldgen/biome/has_structure/graveyard.json', {'values': [
        {'id': f'minecraft:{b}', 'required': False} for b in
        ['plains', 'sunflower_plains', 'forest', 'flower_forest', 'birch_forest', 'dark_forest', 'taiga', 'snowy_taiga',
         'snowy_plains', 'swamp', 'meadow', 'savanna', 'pale_garden', 'old_growth_spruce_taiga', 'old_growth_pine_taiga']]})
    wjson('bm/tags/worldgen/structure/black_market.json', {'values': ['bm:black_market']})
    wjson('bm/tags/worldgen/structure/graveyard.json', {'values': ['bm:graveyard']})
    wjson('bm/tags/worldgen/structure/frog_hut.json', {'values': ['bm:frog_hut']})
    wjson('bm/tags/worldgen/structure/crash_site.json', {'values': ['bm:crash_site']})
    wjson('bm/tags/worldgen/biome/has_structure/crash_site.json', {'values': [f'minecraft:{b}' for b in (
        'plains', 'sunflower_plains', 'desert', 'savanna', 'savanna_plateau', 'badlands', 'wooded_badlands', 'snowy_plains', 'meadow',
        'taiga', 'snowy_taiga', 'forest', 'birch_forest', 'windswept_hills', 'cherry_grove', 'pale_garden')]})
    wjson('bm/tags/worldgen/biome/has_structure/frog_hut.json', {'values': ['minecraft:swamp', 'minecraft:mangrove_swamp']})
    # 1.15: motherships hover ~200 up over open land and sea (not over the high peaks, which reach the hull)
    wjson('bm/tags/worldgen/structure/mothership.json', {'values': ['bm:mothership']})
    wjson('bm/tags/worldgen/biome/has_structure/mothership.json', {'values': [f'minecraft:{b}' for b in MARKET_BIOMES if b not in (
        'dripstone_caves', 'lush_caves', 'sulfur_caves', 'jagged_peaks', 'frozen_peaks', 'stony_peaks', 'snowy_slopes', 'grove')]})
    wjson('bm/tags/worldgen/structure/red_mothership.json', {'values': ['bm:red_mothership']})
    wjson('bm/tags/worldgen/biome/has_structure/red_mothership.json', {'values': [f'minecraft:{b}' for b in MARKET_BIOMES if b not in (
        'dripstone_caves', 'lush_caves', 'sulfur_caves', 'jagged_peaks', 'frozen_peaks', 'stony_peaks', 'snowy_slopes', 'grove')]})
    for sid, step, height, proj, adapt, spacing, sep, salt in [
            ('black_market', 'underground_structures',
             {'type': 'minecraft:uniform', 'min_inclusive': {'absolute': -40}, 'max_inclusive': {'absolute': -14}}, None, 'none', 36, 14, 73519421),
            ('graveyard', 'surface_structures', {'absolute': -17}, 'WORLD_SURFACE_WG', 'beard_thin', 64, 28, 19840313),
            ('frog_hut', 'surface_structures', {'absolute': -4}, 'WORLD_SURFACE_WG', 'none', 40, 14, 31415926),
            ('crash_site', 'surface_structures', {'absolute': 0}, 'WORLD_SURFACE_WG', 'none', 44, 16, 70707070),        # 2.13: a seed marker; carved at runtime
            ('mothership', 'surface_structures', {'absolute': R25.SKY_Y}, None, 'none', 200, 80, 19470708),          # 2.13: ~3x rarer again (was 120/50)
            ('red_mothership', 'surface_structures', {'absolute': R25.SKY_Y + 6}, None, 'none', 420, 160, 66613013)]:  # 2.13: the Vorn Dreadnought
        # 1.13: no natural monster spawns anywhere inside a market's bounds
        so = {'monster': {'bounding_box': 'full', 'spawns': []}} if sid in ('black_market', 'mothership', 'red_mothership') else {}
        s = {'type': 'minecraft:jigsaw', 'biomes': f'#bm:has_structure/{sid}', 'step': step, 'spawn_overrides': so,
             'terrain_adaptation': adapt, 'start_pool': f'bm:{sid}/start', 'size': 1, 'start_height': height,
             'max_distance_from_center': 80, 'use_expansion_hack': False, 'liquid_settings': 'ignore_waterlogging'}
        if proj: s['project_start_to_heightmap'] = proj
        wjson(f'bm/worldgen/structure/{sid}.json', s)
        wjson(f'bm/worldgen/template_pool/{sid}/start.json', {'fallback': 'minecraft:empty', 'elements': [
            {'weight': 1, 'element': {'element_type': 'minecraft:single_pool_element', 'location': f'bm:{sid}',
                                      'projection': 'rigid', 'processors': 'minecraft:empty'}}]})
        wjson(f'bm/worldgen/structure_set/{sid}.json', {'structures': [{'structure': f'bm:{sid}', 'weight': 1}],
                                                         'placement': {'type': 'minecraft:random_spread', 'spacing': spacing,
                                                                       'separation': sep, 'salt': salt}})
    # templates
    MB = M2.build()                              # 1.13: the Black Market 2.0 cavern bazaar (market2.py)
    MB.export(path('data', 'bm', 'structure', 'black_market.nbt'))
    # its static proofs run in a separate interpreter: they borrow the Phase 2 walker, whose package registers items
    import subprocess
    r = subprocess.run([sys.executable, '-c', 'import market2, sys; e = market2.check(market2.build()); print("\\n".join(e)); sys.exit(1 if e else 0)'],
                       cwd=os.path.dirname(os.path.abspath(__file__)), capture_output=True, text=True)
    if r.returncode: raise SystemExit('market2 check failed:\n' + r.stdout + r.stderr)
    S.build_graveyard().export(path('data', 'bm', 'structure', 'graveyard.nbt'))
    S.build_frog_hut().export(path('data', 'bm', 'structure', 'frog_hut.nbt'))
    R32.build_crash_seed().export(path('data', 'bm', 'structure', 'crash_site.nbt'))         # 2.13: the crater is carved at runtime
    R32.build_crash_saucer().export(path('data', 'bm', 'structure', 'crash_saucer.nbt'))
    R25.build_mothership().export(path('data', 'bm', 'structure', 'mothership.nbt'))
    R32.build_dreadnought().export(path('data', 'bm', 'structure', 'red_mothership.nbt'))
    for red in (False, True):
        r = subprocess.run([sys.executable, '-c', f'import phase25, sys; e = phase25.check_mothership(phase25.build_mothership(red={red})); print("\\n".join(e)); sys.exit(1 if e else 0)'],
                           cwd=os.path.dirname(os.path.abspath(__file__)), capture_output=True, text=True)
        if r.returncode: raise SystemExit(f'mothership check failed (red={red}):\n' + r.stdout + r.stderr)
    # item loot tables (handy for /loot and for other packs)
    for iid in ITEMS:
        wjson(f'bm/loot_table/items/{iid}.json', {'pools': [{'rolls': 1, 'entries': [loot_entry(iid)]}]})


def build(out_dir):
    global OUT
    OUT = out_dir
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    with open(path('pack.mcmeta'), 'w') as f:
        json.dump({'pack': {'description': [{'text': 'Black Market ', 'color': 'dark_purple', 'bold': True},
                                            {'text': ('v2.35 (Java 26.3)' if PHASE2 else 'v1.28 (Java 26.3)'), 'color': 'gray'}],
                            'min_format': [121, 0], 'max_format': 121}}, f, indent=1)
    gen_npcs()
    second = gen_mobs()
    gen_feasts()
    gen_lucky()
    gen_maps_skins()
    gen_chest_loot()
    gen_structures_logic()
    gen_loops(second)
    P.generate(sys.modules[__name__])
    Q.generate(sys.modules[__name__])
    R.generate(sys.modules[__name__])
    R18.generate(sys.modules[__name__])
    R19.generate(sys.modules[__name__])
    R20.generate(sys.modules[__name__])
    R21.generate(sys.modules[__name__])
    R22.generate(sys.modules[__name__])
    R23.generate(sys.modules[__name__])
    R24.generate(sys.modules[__name__])
    R25.generate(sys.modules[__name__])
    R26.generate(sys.modules[__name__])
    R27.generate(sys.modules[__name__])
    R32.generate(sys.modules[__name__])
    if PHASE2: p2.generate(sys.modules[__name__])
    gen_admin()
    Q.post_admin(sys.modules[__name__])
    R22.post_admin(sys.modules[__name__])
    R24.post_admin(sys.modules[__name__])
    R25.post_admin(sys.modules[__name__])
    R27.post_admin(sys.modules[__name__])
    R32.post_admin(sys.modules[__name__])
    if PHASE2: p2.post_admin(sys.modules[__name__])
    # 1.18: after everything they hook into exists (trader offers, Phase 2 credits, admin help/uninstall)
    R28.generate(sys.modules[__name__])
    R29.generate(sys.modules[__name__])
    R30.generate(sys.modules[__name__])
    R31.generate(sys.modules[__name__])
    R33.generate(sys.modules[__name__])          # 2.13: after the 1.18 menus it adds to (p28/act)
    R34.generate(sys.modules[__name__])
    R35.generate(sys.modules[__name__])
    R36.generate(sys.modules[__name__])
    R37.generate(sys.modules[__name__])
    R38.generate(sys.modules[__name__])
    R39.generate(sys.modules[__name__])
    R40.generate(sys.modules[__name__])
    R41.generate(sys.modules[__name__])
    R42.generate(sys.modules[__name__])
    R43.generate(sys.modules[__name__])
    R44.generate(sys.modules[__name__])
    R45.generate(sys.modules[__name__])
    R46.generate(sys.modules[__name__])
    R47.generate(sys.modules[__name__])
    R48.generate(sys.modules[__name__])
    R49.generate(sys.modules[__name__])
    R50.generate(sys.modules[__name__])
    R51.generate(sys.modules[__name__])
    R52.generate(sys.modules[__name__])
    R53.generate(sys.modules[__name__])
    R54.generate(sys.modules[__name__])
    R55.generate(sys.modules[__name__])
    R28.finalize(sys.modules[__name__])
    useitem.generate(sys.modules[__name__])
    if hasattr(sys.modules[__name__], 'HELP_BUILDER'): FUNCS['admin/help'] = HELP_BUILDER()      # 2.29: lists every admin command
    gen_tags_worldgen()
    for line in optimize.optimize(sys.modules[__name__]): print('optimize:', line)      # 2.15: cheaper entity selectors, quiet dungeons/markets
    # 1.13: every objective is created before any line of load uses it (phases prepend their own lines to load, and a
    # constant set before its objective exists silently fails - the 1.11 rat-pillar bug on brand-new worlds)
    ld = FUNCS['load']
    adds = [l for l in ld if l.startswith('scoreboard objectives add ')]
    FUNCS['load'] = adds + [l for l in ld if not l.startswith('scoreboard objectives add ')]
    for name, lines in FUNCS.items():
        with open(path('data', 'bm', 'function', name + '.mcfunction'), 'w') as f:
            f.write('\n'.join(mig263.inline_modifier(l) for l in lines) + '\n')     # 26.3: inline loot functions/conditions key on `type`
    return FUNCS


if __name__ == '__main__':
    f = build('/home/claude/bm_build/' + ('out_p2' if PHASE2 else 'out') + '/BlackMarket_DP')
    print(len(f), 'functions;', len(ITEMS), 'items')

"""2.68: CURRENCY WINS - a won heist pays in money, not clutter; vanilla goods move to coin-bought crates; tip-offs call the
next heist's kind; a laurel and an achievement for each tier's first clear; and three new finds.

WHAT A WIN PAYS NOW: Black Market Tokens (your fee back and a few more), Gutter Coins (your shares - every share is coins
  now - the pot, the Fixer's cash), the vault's spoils and Captain's Insignia (straight to your Gutter Bank, as before),
  the 3D Gutter Trophies you earn, BM Medallions and the rare BM Trophy (the Fixer's prize, as before), a Shifting Core
  (1 in 100), and the night's own currency: Blood Moon Crystals (a Blood Moon heist), Lucky Tokens (a Lucky Night heist,
  or a Lucky Raid), Green Xenite (an Alien heist) - more at the higher tiers. No more piles of ingots, supplies and food,
  and no more heist gear Goldtooth sells anyway. The haul lectern's three kinds of haul are retired: every haul is this.
THE VAULT'S OWN TREASURES stay, rarer: one roll a win (6% at Tier I up to 10% at Tier V) for a piece of the tier's raid-only
  gear (the Heister's Shiv, the Vault Breaker, the Coinslinger, the Gutter Cutlass, the Treasurer's Scepter). Hidden vaults,
  the Gutter Gentry and the rare guards keep their treasures.
THREE NEW FINDS, for every raider on every win (any tier): FORGEHEART (rare, 5%) - carry it and the raw iron, gold and
  copper in your pack smelt themselves (now and then an extra ingot, and the furnace's experience); THE ALIBI (legendary,
  3%) - use it to snap back to where you stood five seconds ago, the hurt of those seconds mended and any fire out (once a
  minute); THE COUNTERFEITER'S PRESS (mythical, 1%) - set it down and it prints a Black Market Token a day, up to seven
  waiting, for whoever set it there (one press per crook).
THE CRATE DESK (the old haul lectern in the den, and the Office): RAW MATERIALS CRATES (16 coins), ADVENTURER'S CRATES
  (32) and MINERAL CRATES (48) - set one down and open it: a few stacks from the haul's old pools, you don't know which until
  it's open (walk away and what's left folds up into your pack, like The Haul). And TIP-OFFS (64 coins each): the CRIMSON
  TIP-OFF makes your next heist a Blood Moon heist, the VORN SIGNAL an Alien heist. Use one to call it; it counts when you
  plan your next heist yourself. A Lucky Raid can't be called - it's the luck of the draw.
LAURELS: the first clear of each tier gives its own laurel - COPPER (I), SILVER (II), GILDED (III), PEARL (IV), EMBER (V)
  - and its own achievement. Hold a laurel in your off hand for a crown of its light. (Tiers cleared before 2.68 are
  honoured the next time you're on: the laurels and the achievements arrive by themselves.)
"""
import math
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int
import phase28 as P28
import phase70 as P70
import phase70_rooms as RM

GOLD = '#ffcf40'
ROMAN = ['', 'I', 'II', 'III', 'IV', 'V']
LAUREL = {1: ('copper', 'Copper Laurel', '#d9824a', (0.85, 0.51, 0.29)), 2: ('silver', 'Silver Laurel', '#c8d0d8', (0.78, 0.82, 0.85)),
          3: ('gilded', 'Gilded Laurel', GOLD, (1.0, 0.81, 0.25)), 4: ('pearl', 'Pearl Laurel', '#4ad0c0', (0.29, 0.82, 0.75)),
          5: ('ember', 'Ember Laurel', '#ff8a30', (1.0, 0.54, 0.19))}
TIER_ADV = {1: ('Into the Gutter', 'Clear a Tier I heist in the Gilded Gutter Vault'), 2: ('Silver Tongued', 'Clear a Tier II heist'),
            3: ('Gilt-Edged', 'Clear a Tier III heist'), 4: ('Pearl Diver', 'Clear a Tier IV heist'), 5: ('Keeper of the Hoard', 'Clear a Tier V heist - the deepest vault')}
SHARE_COINS = {1: (2, 3), 2: (3, 4), 3: (4, 6), 4: (5, 8), 5: (7, 10)}                   # Gutter Coins a share
NIGHT_AMT = {t: (2 + t, 4 + 2 * t) for t in range(1, 6)}                                  # the night's own currency, by tier
RARE_CHANCE = {1: 6, 2: 7, 3: 8, 4: 9, 5: 10}                                             # % a win: a piece of the tier's raid-only gear
RARE_POOL = {1: ['heisters_shiv'], 2: ['heisters_shiv', 'vault_breaker'], 3: ['vault_breaker', 'coinslinger'],
             4: ['coinslinger', 'gutter_cutlass'], 5: ['gutter_cutlass', 'treasurers_scepter']}
FIND_RARE, FIND_LEGEND, FIND_MYTH = 5, 3, 1                                               # % a win, every raider, any tier
CORE_PERMILLE = 10                                                                        # a Shifting Core: 1 in 100
DESK = 8500
PRICES = {'crate_raw': 16, 'crate_adventure': 32, 'crate_mineral': 48, 'tip_bloodmoon': 64, 'tip_alien': 64}
PRESS_MAX = 7
ALIBI_CD = 60
RARE_TAG, LEGEND_TAG, MYTH_TAG = ('◆ Rare raid find', '#5ab0ff'), ('◆◆ Legendary raid find', '#ffb300'), ('◆◆◆ Mythical raid find', '#e080ff')

# ---------------------------------------------------------------- the items
for _t, (_k, _nm, _col, _rgb) in LAUREL.items():
    item(f'laurel_t{_t}', TOTEM, _nm, _col, [f'Tier {ROMAN[_t]} of the Gilded Gutter Vault - cleared.', ('Given once, for the first clear.', 'gray'),
                                             (f'In your off hand: a crown of {_k} light.', 'blue')], model=f'bm:laurel_t{_t}', stack=1, cat='cosmetic')
for _iid, _nm, _col, _lore in (('crate_raw', 'Raw Materials Crate', '#c8a070', 'Iron, copper, coal, redstone, lumber, stone...'),
                               ('crate_adventure', "Adventurer's Crate", '#7ad0ea', 'Bottled experience, books, pearls, apples...'),
                               ('crate_mineral', 'Mineral Crate', '#ffd870', 'Gold, emeralds, metal blocks - and now and then a diamond.')):
    item(_iid, 'minecraft:barrel', _nm, _col, [_lore, ('Set it down and open it - you won\'t know', 'blue'), ('what\'s inside until you do.', 'blue'),
                                                ('Walk away and what\'s left folds up into your pack.', 'gray')],
         model=f'bm:{_iid}', stack=16, custom_extra={'bm_haul': B(1), 'bm_crate': _iid, 'bm_cr': B(1)}, cat='builder')
item('tip_bloodmoon', TOTEM, 'Crimson Tip-off', '#d02020', ['A smudged note, in something red: "Tonight the vault bleeds."',
                                                           ('Use it: the next heist you plan', 'blue'), ('will be a Blood Moon heist.', 'blue')],
     model='bm:tip_bloodmoon', stack=16, comps=hold(), cat='blood')
item('tip_alien', TOTEM, 'Vorn Signal', '#5ad84a', ['A ticking little beacon, tuned to the Vorn.', ('Use it: the next heist you plan', 'blue'),
                                                   ('will be an Alien heist.', 'blue')], model='bm:tip_alien', stack=16, comps=hold(), cat='misc')
item('forgeheart', TOTEM, 'Forgeheart', '#ff7a30', ['A coal heart from the Hoard. It never cools.', ('Carry it: the raw iron, gold and copper', 'blue'),
                                                    ('in your pack smelt themselves - now and', 'blue'), ('then into an extra ingot.', 'blue'), RARE_TAG],
     model='bm:forgeheart', stack=1, cat='relic')
item('the_alibi', TOTEM, 'The Alibi', GOLD, ['"I was never there."', ('Use it: back to where you stood five', 'blue'), ('seconds ago - the hurt of those seconds', 'blue'),
                                             ('mended, any fire put out. Once a minute.', 'blue'), LEGEND_TAG],
     model='bm:the_alibi', stack=1, comps=hold(), cat='relic', glint=True)
item('counterfeiters_press', TOTEM, "The Counterfeiter's Press", '#e080ff', ['A little iron press, still inky.', ('Use it on a floor to set it down: it prints', 'blue'),
                                                                            ('a Black Market Token a day for you - up to', 'blue'),
                                                                            (f'{PRESS_MAX} waiting. Right-click it to collect.', 'blue'),
                                                                            ('One press per crook. Sneak + punch: pick it up.', 'gray'), MYTH_TAG],
     model='bm:press3d', stack=1, comps=hold(), cat='relic', glint=True)
HOLD['tip_bloodmoon'] = 'bm:p105/tip/blood'
HOLD['tip_alien'] = 'bm:p105/tip/alien'
HOLD['the_alibi'] = 'bm:p105/alibi/use'
HOLD['counterfeiters_press'] = 'bm:p105/press/place'


def generate(G):
    fn, wjson, tellraw, title = G.fn, G.wjson, G.tellraw, G.title
    import phase74 as P74
    HA, HB = '-200 64 -197', '-198 64 -197'
    P = [T('[', 'dark_gray'), T('Heist', GOLD, bold=True), T('] ', 'dark_gray')]
    say = lambda txt, col='gray': tellraw('@s', P + [T(txt, col)])
    holds = lambda iid: f'*[minecraft:custom_data~{{bm:"{iid}"}}]'
    num = lambda n, col='white': {'score': {'name': n, 'objective': 'bm.rng'}, 'color': col, 'bold': True}
    rel = RM.rel
    tick, fast, second = [], [], []
    objs = ['bm.gvfz', 'bm.lr68', 'bm.aliq', 'bm.prso', 'bm.prsd', 'bm.prs', 'bm.fgt']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs

    def ins(table, cond=''):
        return [f'execute {cond}in bm:gutter unless data block {HA} Items[26] run loot insert {HA} loot {table}',
                f'execute {cond}in bm:gutter if data block {HA} Items[26] run loot insert {HB} loot {table}']
    def ent(i, w, c=None, fns=()):
        if i in ITEMS:
            return dict(G.loot_entry(i, G.uni(*c) if isinstance(c, tuple) else c), weight=w)
        e = {'type': 'minecraft:item', 'name': i if ':' in i else 'minecraft:' + i, 'weight': w, 'functions': list(fns)}
        if c: e['functions'].append({'function': 'minecraft:set_count', 'count': G.uni(*c) if isinstance(c, tuple) else c})
        return e

    # ================================================================== WHAT A WIN PAYS: money
    haul = G.FUNCS['p70/haul']
    k = haul.index('scoreboard players operation #th bm.rng = @s bm.gvth')
    haul[k] = 'scoreboard players set #th bm.rng 2'                       # (the haul lectern's kinds of haul: retired - every haul is the Black Market's)
    cp = G.FUNCS['p70/r/cache/pay']
    cp[:] = ['scoreboard players set #th bm.rng 2' if l == 'scoreboard players operation #th bm.rng = @s bm.gvth' else l for l in cp]
    n0 = len(haul)
    haul[:] = [l for l in haul if 'loot bm:p84/supplies' not in l and l != 'function bm:p80/scrap']
    assert n0 - len(haul) == 13, n0 - len(haul)                           # (12 supply lines, the netherite scrap roll)
    for f_ in ('p80/scrap', 'p80/scrap_clean'):
        G.FUNCS.pop(f_, None)                                              # (netherite scrap: in the Mineral Crate now)
    # (every share is coins - all three kinds of haul table, in case anything still asks for one)
    for t, (lo, hi) in SHARE_COINS.items():
        coins = {'pools': [{'rolls': 1, 'entries': [ent('gutter_coin', 1, (lo, hi))]}]}
        for pre in ('t', 'v', 'g'):
            wjson(f'bm/loot_table/gv/{pre}{t}.json', coins)
    # (a Shifting Core: 1 in 100, every tier)
    ks = [i for i, l in enumerate(haul) if l.endswith('run function bm:p70/core')]
    assert len(ks) == 3, ks
    haul[ks[0]:ks[-1] + 1] = [f'execute if score #r bm.rng matches ..{CORE_PERMILLE} run function bm:p70/core']
    # (the night's own currency, more at the higher tiers - and a Lucky Raid pays Lucky Tokens too)
    night = {'night_blood': ('blood_crystal', 'crimson_ledger'), 'night_lucky': ('lucky_token', 'gamblers_coin'), 'night_inv': ('xenite_green', 'vorn_cracking_rig')}
    for nm, (cur, rare) in night.items():
        for t, (lo, hi) in NIGHT_AMT.items():
            pools = [{'rolls': 1, 'entries': [ent(cur, 1, (lo, hi))]}, {'rolls': 1, 'entries': [ent(rare, 8), {'type': 'minecraft:empty', 'weight': 92}]}]
            if nm == 'night_lucky':
                pools.insert(1, {'rolls': 1, 'entries': [ent('gutter_coin', 1, (2 + 2 * t, 4 + 3 * t))]})
            wjson(f'bm/loot_table/gv/{nm}_t{t}.json', {'pools': pools})
    out = []
    for l in haul:
        hit = next((nm for nm in night if l.endswith(f'loot bm:gv/{nm}')), None)
        if not hit:
            out.append(l); continue
        out += [l.replace('execute ', f'execute if score #gt bm.rng matches {t} ', 1) + f'_t{t}' for t in range(1, 6)]
    haul[:] = out
    kp = haul.index('function bm:p75/prize')
    haul[kp + 1:kp + 1] = sum((ins(f'bm:gv/night_lucky_t{t}', f'if score #plu bm.rng matches 1 unless score #gn bm.rng matches 2 if score #gt bm.rng matches {t} ')
                               for t in range(1, 6)), [])
    # (the rarer finds, just before the haul's packed)
    kh = haul.index('function bm:p74/haul_pack')
    haul.insert(kh, 'function bm:p105/finds')
    for t, pool in RARE_POOL.items():
        wjson(f'bm/loot_table/p105/rare_t{t}.json', {'pools': [{'rolls': 1, 'entries': [ent(i, 1) for i in pool]}]})
    fn('p105/finds', ['execute store result score #r bm.rng run random value 1..100'] +
       [f'execute if score #gt bm.rng matches {t} if score #r bm.rng matches ..{c} run function bm:p105/find_gear{t}' for t, c in RARE_CHANCE.items()] +
       ['execute store result score #r bm.rng run random value 1..100', f'execute if score #r bm.rng matches ..{FIND_RARE} run function bm:p105/find_rare',
        'execute store result score #r bm.rng run random value 1..100', f'execute if score #r bm.rng matches ..{FIND_LEGEND} run function bm:p105/find_legend',
        'execute store result score #r bm.rng run random value 1..100', f'execute if score #r bm.rng matches ..{FIND_MYTH} run function bm:p105/find_myth'])
    for t in RARE_POOL:
        fn(f'p105/find_gear{t}', ins(f'bm:p105/rare_t{t}') + [tellraw('@s', P + [T('A vault treasure in your haul! ', '#9ae8ff', bold=True),
                                                                                  T(f'A piece of Tier {ROMAN[t]}\'s own gear.', 'gray')])])
    fn('p105/find_rare', ins('bm:items/forgeheart') + [tellraw('@s', P + [T('Rare find! ', RARE_TAG[1], bold=True), T('A ', 'gray'), T('Forgeheart', '#ff7a30', bold=True),
                                                                         T(' in your haul.', 'gray')]),
                                                     'playsound minecraft:block.furnace.fire_crackle player @s ~ ~ ~ 1 1'])
    fn('p105/find_legend', ins('bm:items/the_alibi') + [tellraw('@a', P + [{'selector': '@s', 'color': 'white'}, T(' found a legendary ', 'gray'), T('Alibi', GOLD, bold=True),
                                                                           T(' in a won heist!', 'gray')]),
                                                      'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1.3'])
    fn('p105/find_myth', ins('bm:items/counterfeiters_press') + [tellraw('@a', P + [{'selector': '@s', 'color': 'white'}, T(' found a mythical ', 'gray'),
                                                                                    T("Counterfeiter's Press", '#e080ff', bold=True), T(' in a won heist!', 'gray')]),
                                                               'playsound minecraft:ui.toast.challenge_complete player @a ~ ~ ~ 0.7 0.7',
                                                               'execute at @s run particle minecraft:totem_of_undying ~ ~1 ~ 0.5 1 0.5 0.4 60'])
    # (the lectern and the Office: no more kinds of haul to pick - the Crate Desk instead)
    li = G.FUNCS['p70/r/lobby/init']
    kl = next(i for i, l in enumerate(li) if 'plain, Black Market or gutter' in l)
    li[kl] = li[kl].replace('plain, Black Market or gutter', 'crates and tip-offs, for coins').replace('YOUR HAUL', 'THE CRATE DESK')

    # ================================================================== LAURELS AND ACHIEVEMENTS: each tier's first clear
    for t, (k_, nm, col, rgb) in LAUREL.items():
        ttl, desc = TIER_ADV[t]
        wjson(f'bm/advancement/story/raid_t{t}.json', {'parent': 'bm:story/root' if t == 1 else f'bm:story/raid_t{t - 1}', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
              'display': {'icon': {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': f'bm:laurel_t{t}'}},
                          'title': T(ttl, 'gold' if t == 5 else 'yellow'), 'description': T(desc, 'gray'),
                          'frame': 'challenge' if t == 5 else ('goal' if t >= 3 else 'task'), 'show_toast': True, 'announce_to_chat': True, 'hidden': False}})
    fc = G.FUNCS['p70/first_clear']
    kf = next(i for i, l in enumerate(fc) if l.startswith('tellraw'))
    fc[kf:kf] = sum((ins(f'bm:items/laurel_t{t}', f'if score #gt bm.rng matches {t} ') for t in range(1, 6)), []) + \
        [f'execute if score #gt bm.rng matches {t} run advancement grant @s only bm:story/raid_t{t}' for t in range(1, 6)]
    fc[:] = [l.replace('A Gilded prize and a finer Raid Banner.', 'A Gilded prize, a finer Raid Banner and the tier\'s own Laurel.') for l in fc]
    # (tiers cleared before 2.68: honoured once, the next time each player's about)
    second.append('execute as @a unless score @s bm.lr68 matches 1 run function bm:p105/retro')
    fn('p105/retro', ['scoreboard players set @s bm.lr68 1', 'execute unless score @s bm.gvcl matches 1.. run return 0'] +
       sum(([f'scoreboard players operation #q bm.rng = @s bm.gvcl', f'scoreboard players set #bit bm.rng {2 ** t}', 'scoreboard players operation #q bm.rng /= #bit bm.rng',
             'scoreboard players operation #q bm.rng %= #2 bm.rng', f'execute if score #q bm.rng matches 1 run function bm:p105/retro{t}'] for t in range(1, 6)), []))
    for t in range(1, 6):
        fn(f'p105/retro{t}', [f'advancement grant @s only bm:story/raid_t{t}', G.give(f'laurel_t{t}'),
                              tellraw('@s', P + [T(f'For clearing Tier {ROMAN[t]}: ', 'gray'), T(LAUREL[t][1], LAUREL[t][2], bold=True), T('.', 'gray')])])
    # (the crown: a laurel in the off hand - a ring of its colour over your head)
    for t, (k_, nm, col, (r, g, b)) in LAUREL.items():
        second.append(f'execute as @a if items entity @s weapon.offhand {holds(f"laurel_t{t}")} at @s run function bm:p105/crown{t}')
        fn(f'p105/crown{t}', [f'particle minecraft:dust{{color:[{r},{g},{b}],scale:0.6}} ~{0.3 * math.cos(a * math.pi / 5):.2f} ~2.12 ~{0.3 * math.sin(a * math.pi / 5):.2f} 0 0 0 0 1'
                              for a in range(10)] + ['particle minecraft:wax_on ~ ~2.25 ~ 0.12 0.04 0.12 0 1'])

    # ================================================================== TIP-OFFS: call the next heist's kind (never a Lucky Raid)
    fn('p105/tip/blood', ['execute if score @s bm.gvfz matches 1 run return run ' + say('Your next heist is a Blood Moon heist already.', 'gray'),
                          'scoreboard players set @s bm.gvfz 1', f'execute unless entity @s[gamemode=creative] run clear @s {holds("tip_bloodmoon")} 1',
                          tellraw('@s', P + [T('Crimson tip-off: ', '#d02020', bold=True), T('the next heist you plan will be a ', 'gray'), T('BLOOD MOON HEIST', '#ff4040', bold=True),
                                             T('.', 'gray')]), 'playsound minecraft:entity.wither.ambient player @s ~ ~ ~ 0.4 1.6'])
    fn('p105/tip/alien', ['execute if score @s bm.gvfz matches 3 run return run ' + say('Your next heist is an Alien heist already.', 'gray'),
                          'scoreboard players set @s bm.gvfz 3', f'execute unless entity @s[gamemode=creative] run clear @s {holds("tip_alien")} 1',
                          tellraw('@s', P + [T('Vorn signal: ', '#5ad84a', bold=True), T('the next heist you plan will be an ', 'gray'), T('ALIEN HEIST', '#5ad84a', bold=True),
                                             T('.', 'gray')]), 'playsound minecraft:block.beacon.activate player @s ~ ~ ~ 0.6 1.6'])
    for s in range(P70.SLOTS):
        G.FUNCS[f'p70/s{s}/claim'] += [f'scoreboard players operation #fz{s} bm.gvv = @s bm.gvfz', 'scoreboard players set @s bm.gvfz 0',
                                       f'execute if score #fz{s} bm.gvv matches 3 run scoreboard players set #sf{s} bm.gvv 1',
                                       f'execute if score #fz{s} bm.gvv matches 1 run ' + tellraw('@a[tag=bm.gvwait]', P + [T('The tip-off pays: ', 'gray'),
                                                                                                                        T('a BLOOD MOON HEIST.', '#ff4040', bold=True)]),
                                       f'execute if score #fz{s} bm.gvv matches 3 run ' + tellraw('@a[tag=bm.gvwait]', P + [T('The signal pays: ', 'gray'),
                                                                                                                        T('an ALIEN HEIST.', '#5ad84a', bold=True)])]
        b = G.FUNCS[f'p70/s{s}/build']
        kk = b.index('scoreboard players operation #gk bm.rng = #gt bm.rng')
        b[kk:kk] = [f'execute if score #fz{s} bm.gvv matches 1 run scoreboard players set #gn bm.rng 1',
                    f'execute if score #fz{s} bm.gvv matches 3 run scoreboard players set #gn bm.rng 3',
                    f'execute if score #fz{s} bm.gvv matches 3 run scoreboard players set #gsf bm.rng 1',
                    f'execute if score #fz{s} bm.gvv matches 1 run scoreboard players set #gsf bm.rng 0']

    # ================================================================== THE CRATE DESK
    def lt_raw():
        return {'pools': [{'rolls': G.uni(4, 5), 'entries': [
            ent('iron_ingot', 14, (8, 16)), ent('copper_ingot', 12, (16, 32)), ent('coal', 12, (16, 32)), ent('redstone', 10, (16, 32)), ent('lapis_lazuli', 8, (8, 16)),
            ent('quartz', 7, (16, 32)), ent('oak_log', 6, (16, 32)), ent('spruce_log', 5, (16, 32)), ent('cobblestone', 6, (32, 64)), ent('stone_bricks', 4, (32, 64)),
            ent('glass', 5, (16, 32)), ent('string', 4, (8, 16)), ent('leather', 4, (4, 8)), ent('obsidian', 3, (4, 8)), ent('clay_ball', 3, (16, 32)),
            ent('slime_ball', 2, (4, 8)), ent('arrow', 4, (16, 32)), ent('amethyst_shard', 2, (8, 16)), ent('gunpowder', 3, (8, 16))]}]}
    def lt_adv():
        book = {'type': 'minecraft:item', 'name': 'minecraft:book', 'weight': 8, 'functions': [{'function': 'minecraft:enchant_with_levels', 'levels': G.uni(15, 30)}]}
        return {'pools': [{'rolls': G.uni(2, 3), 'entries': [
            ent('experience_bottle', 12, (4, 10)), book, ent('golden_apple', 6, (1, 2)), ent('ender_pearl', 8, (2, 4)), ent('blaze_rod', 6, (2, 4)),
            ent('golden_carrot', 8, (8, 16)), ent('name_tag', 3), ent('saddle', 2), ent('spectral_arrow', 4, (8, 16)), ent('firework_rocket', 5, (8, 16)),
            ent('cooked_beef', 6, (8, 16)), ent('enchanted_golden_apple', 1)]}]}
    def lt_min():
        return {'pools': [{'rolls': G.uni(3, 4), 'entries': [
            ent('gold_ingot', 16, (4, 10)), ent('emerald', 12, (3, 8)), ent('iron_block', 10, (1, 3)), ent('lapis_block', 7, (1, 3)), ent('redstone_block', 7, (2, 4)),
            ent('gold_block', 6, (1, 2)), ent('diamond', 4, (1, 2)), ent('emerald_block', 2), ent('netherite_scrap', 1), ent('ancient_debris', 1)]}]}
    wjson('bm/loot_table/p105/crate_raw.json', lt_raw())
    wjson('bm/loot_table/p105/crate_adventure.json', lt_adv())
    wjson('bm/loot_table/p105/crate_mineral.json', lt_min())
    # (an emptied Haul is swept out of pockets every second - a crate, unopened and empty by design, isn't one)
    sec = G.FUNCS['loop/second']
    old_sweep = 'clear @a minecraft:barrel[minecraft:custom_data~{bm_haul:1b},minecraft:container=[]]'
    assert old_sweep in sec, 'the empty-Haul sweep moved'
    sec[sec.index(old_sweep)] = 'clear @a minecraft:barrel[minecraft:custom_data~{bm_haul:1b},minecraft:container=[],!minecraft:custom_data~{bm_cr:1b}]'
    # (a crate set down - The Haul's machinery finds it - is filled the vanilla way: by its loot table, when it's opened)
    G.FUNCS['p74/haul/mark'].append('execute if data block ~ ~ ~ components."minecraft:custom_data".bm_crate run function bm:p105/crate/fill')
    fn('p105/crate/fill', [f'execute if data block ~ ~ ~ {{components:{{"minecraft:custom_data":{{bm_crate:"{c}"}}}}}} run data modify block ~ ~ ~ LootTable set value "bm:p105/{c}"'
                           for c in ('crate_raw', 'crate_adventure', 'crate_mineral')])
    # (walked away from unopened: it goes back in your pack as it was)
    G.FUNCS['p74/haul/fold'].insert(0, 'execute if data block ~ ~ ~ LootTable run return run function bm:p105/crate/unopened')
    fn('p105/crate/unopened', ['data modify storage bm:tmp crate set value ""', 'data modify storage bm:tmp crate set from block ~ ~ ~ components."minecraft:custom_data".bm_crate',
                               'data remove block ~ ~ ~ LootTable', 'setblock ~ ~ ~ minecraft:air', 'particle minecraft:poof ~ ~ ~ 0.3 0.3 0.3 0.02 8'] +
       [f'execute if data storage bm:tmp {{crate:"{c}"}} as @a if score @s bm.pid = #hp bm.rng run ' + G.give(c) for c in ('crate_raw', 'crate_adventure', 'crate_mineral')] +
       ['kill @s'])
    desk = P28.multi([T('THE CRATE DESK', GOLD, bold=True), T('  ·  paid from your bank and pockets', 'gray')],
                     [P28.body([T('You have ', 'gray'), T('$(w)', GOLD, bold=True), T(' Gutter Coins (bank + pockets; Medallions 16, Trophies 128).', 'gray')], 320),
                      P28.body([T('Crates: set one down and open it - a few stacks, and you won\'t know which until you do. ', 'gray'),
                                T('Tip-offs: the next heist you plan is that kind.', 'dark_gray')], 320)],
                     [P28.btn([T('Raw Materials Crate  ', '#c8a070', bold=True), T(f'{PRICES["crate_raw"]} coins', 'white')], DESK + 1, width=300,
                              tooltip=T('Iron, copper, coal, redstone, lapis, quartz, lumber, stone, glass...', 'gray')),
                      P28.btn([T("Adventurer's Crate  ", '#7ad0ea', bold=True), T(f'{PRICES["crate_adventure"]} coins', 'white')], DESK + 2, width=300,
                              tooltip=T('Experience bottles, enchanted books, pearls, golden apples, rockets...', 'gray')),
                      P28.btn([T('Mineral Crate  ', '#ffd870', bold=True), T(f'{PRICES["crate_mineral"]} coins', 'white')], DESK + 3, width=300,
                              tooltip=T('Gold, emeralds, metal blocks - now and then a diamond, rarely netherite.', 'gray')),
                      P28.btn([T('Crimson Tip-off  ', '#d02020', bold=True), T(f'{PRICES["tip_bloodmoon"]} coins', 'white')], DESK + 4, width=300,
                              tooltip=T('Your next heist: a Blood Moon heist (Blood Moon Crystals in the haul).', 'gray')),
                      P28.btn([T('Vorn Signal  ', '#5ad84a', bold=True), T(f'{PRICES["tip_alien"]} coins', 'white')], DESK + 5, width=300,
                              tooltip=T('Your next heist: an Alien heist (Green Xenite in the haul).', 'gray'))],
                     columns=1, exit_label='Done')
    G.FUNCS['p86/theme/menu'] = ['function bm:p103/wallet', f'scoreboard players set @s bm.menu {DESK}', 'function bm:p105/desk/show with storage bm:ui tl']
    fn('p105/desk/show', [f'$dialog show @s {P28.inline(desk)}'])
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {DESK + 1}..{DESK + 5} run return run function bm:p105/desk/buy')
    order = ['crate_raw', 'crate_adventure', 'crate_mineral', 'tip_bloodmoon', 'tip_alien']
    fn('p105/desk/buy', [f'execute unless score @s bm.menu matches {DESK} run return run function bm:p28/stale', 'function bm:p103/wallet'] +
       [f'execute if score #act bm.pay matches {DESK + 1 + i} run scoreboard players set #need bm.rng {PRICES[c]}' for i, c in enumerate(order)] +
       ['execute if score #tw bm.rng < #need bm.rng run return run function bm:p105/desk/poor', 'function bm:p103/spend'] +
       [f'execute if score #act bm.pay matches {DESK + 1 + i} run ' + G.give(c) for i, c in enumerate(order)] +
       ['playsound minecraft:entity.villager.yes player @s ~ ~ ~ 0.8 1.1', 'function bm:p86/theme/menu'])
    fn('p105/desk/poor', ['scoreboard players operation #short bm.rng = #need bm.rng', 'scoreboard players operation #short bm.rng -= #tw bm.rng',
                          tellraw('@s', P + [T('Not enough - ', 'red'), num('#short'), T(' coins short.', 'red')]), 'playsound minecraft:entity.villager.no player @s ~ ~ ~ 0.8 1'])

    # ================================================================== FORGEHEART: carried, it smelts your raw metal
    second += ['scoreboard players add #fgt bm.fgt 1', 'execute if score #fgt bm.fgt matches 3.. run function bm:p105/forge/all']
    fn('p105/forge/all', ['scoreboard players set #fgt bm.fgt 0', f'execute as @a if items entity @s container.* {holds("forgeheart")} at @s run function bm:p105/forge/me',
                          f'execute as @a unless items entity @s container.* {holds("forgeheart")} if items entity @s weapon.offhand {holds("forgeheart")} at @s run function bm:p105/forge/me'])
    METALS = [('raw_iron', 'iron_ingot', 7, True), ('raw_gold', 'gold_ingot', 10, True), ('raw_copper', 'copper_ingot', 7, True),
              ('raw_iron_block', 'iron_block', 60, False), ('raw_gold_block', 'gold_block', 90, False), ('raw_copper_block', 'copper_block', 60, False)]
    fn('p105/forge/me', ['scoreboard players set #fsum bm.rng 0'] +
       sum(([f'execute store result score #n bm.rng run clear @s minecraft:{raw}[!minecraft:custom_data] 0',
             f'execute if score #n bm.rng matches 1.. run function bm:p105/forge/{raw}'] for raw, *_r in METALS), []) +
       ['execute if score #fsum bm.rng matches 1.. run particle minecraft:flame ~ ~1 ~ 0.3 0.4 0.3 0.02 12',
        'execute if score #fsum bm.rng matches 1.. run playsound minecraft:block.furnace.fire_crackle player @s ~ ~ ~ 0.8 1.2',
        'execute if score #fsum bm.rng matches 1.. run ' + title('@s', 'actionbar', [T('Forgeheart: ', '#ff7a30', bold=True), num('#fsum'), T(' smelted', 'gray')])])
    for raw, out_, xp10, bonus in METALS:
        fn(f'p105/forge/{raw}', ['scoreboard players operation #fsum bm.rng += #n bm.rng', 'execute store result storage bm:ui fg.n int 1 run scoreboard players get #n bm.rng',
                                 'scoreboard players operation #o bm.rng = #n bm.rng'] +
           (['scoreboard players operation #b bm.rng = #n bm.rng', 'scoreboard players set #k5 bm.rng 5', 'scoreboard players operation #b bm.rng /= #k5 bm.rng',
             'scoreboard players operation #m bm.rng = #n bm.rng', 'scoreboard players operation #m bm.rng %= #k5 bm.rng',
             'execute store result score #r bm.rng run random value 1..5', 'execute if score #r bm.rng <= #m bm.rng run scoreboard players add #b bm.rng 1',
             'scoreboard players operation #o bm.rng += #b bm.rng'] if bonus else []) +
           ['execute store result storage bm:ui fg.o int 1 run scoreboard players get #o bm.rng',
            f'scoreboard players set #x bm.rng {xp10}', 'scoreboard players operation #x bm.rng *= #n bm.rng', 'execute store result score #r bm.rng run random value 0..9',
            'scoreboard players operation #x bm.rng += #r bm.rng', 'scoreboard players set #k10 bm.rng 10', 'scoreboard players operation #x bm.rng /= #k10 bm.rng',
            'execute store result storage bm:ui fg.x int 1 run scoreboard players get #x bm.rng', f'function bm:p105/forge/{raw}2 with storage bm:ui fg'])
        fn(f'p105/forge/{raw}2', [f'$clear @s minecraft:{raw}[!minecraft:custom_data] $(n)', f'$give @s minecraft:{out_} $(o)', '$xp add @s $(x) points'])

    # ================================================================== THE ALIBI: five seconds back
    second += ['scoreboard players remove @a[scores={bm.aliq=1..}] bm.aliq 1', 'tag @a remove bm.alr',
               f'execute as @a if items entity @s container.* {holds("the_alibi")} run tag @s add bm.alr',
               f'execute as @a if items entity @s weapon.offhand {holds("the_alibi")} run tag @s add bm.alr',
               'execute as @a[tag=bm.alr] at @s run function bm:p105/alibi/rec']
    fn('p105/alibi/rec', ['execute store result storage bm:ali tmp.pid int 1 run scoreboard players get @s bm.pid', 'data modify storage bm:ali tmp.e set value {}',
                          'data modify storage bm:ali tmp.e.x set from entity @s Pos[0]', 'data modify storage bm:ali tmp.e.y set from entity @s Pos[1]',
                          'data modify storage bm:ali tmp.e.z set from entity @s Pos[2]', 'data modify storage bm:ali tmp.e.r set from entity @s Rotation[0]',
                          'data modify storage bm:ali tmp.e.d set from entity @s Dimension', 'execute store result storage bm:ali tmp.e.h int 1 run data get entity @s Health',
                          'function bm:p105/alibi/rec2 with storage bm:ali tmp'])
    fn('p105/alibi/rec2', ['$data modify storage bm:ali h.p$(pid) append from storage bm:ali tmp.e', '$execute if data storage bm:ali h.p$(pid)[6] run data remove storage bm:ali h.p$(pid)[0]'])
    fn('p105/alibi/use', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                          'execute if score @s bm.aliq matches 1.. run return run ' + title('@s', 'actionbar', [T('The Alibi needs ', 'gray'),
                                                                                                         {'score': {'name': '@s', 'objective': 'bm.aliq'}, 'color': 'white', 'bold': True},
                                                                                                         T(' more seconds.', 'gray')]),
                          'execute store result storage bm:ali tmp.pid int 1 run scoreboard players get @s bm.pid', 'function bm:p105/alibi/use2 with storage bm:ali tmp'])
    fn('p105/alibi/use2', ['$execute unless data storage bm:ali h.p$(pid)[0] run return run ' + title('@s', 'actionbar', T('Nothing to take back yet.', 'gray')),
                           '$data modify storage bm:ali go set from storage bm:ali h.p$(pid)[0]', 'data modify storage bm:ali cur set from entity @s Dimension',
                           'execute store success score #dd bm.rng run data modify storage bm:ali cur set from storage bm:ali go.d',
                           'execute if score #dd bm.rng matches 1 run return run ' + title('@s', 'actionbar', T('The Alibi won\'t cross between worlds.', 'gray')),
                           '$data remove storage bm:ali h.p$(pid)', f'scoreboard players set @s bm.aliq {ALIBI_CD}',
                           'execute store result score #hn bm.rng run data get entity @s Health', 'execute store result score #ho bm.rng run data get storage bm:ali go.h',
                           'scoreboard players operation #ho bm.rng -= #hn bm.rng',
                           'particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.6 0.3 0.05 40', 'playsound minecraft:block.bell.resonate player @a[distance=..16] ~ ~ ~ 0.6 1.8',
                           'function bm:p105/alibi/go with storage bm:ali go',
                           'execute if score #ho bm.rng matches 12.. run effect give @s minecraft:instant_health 1 2 true',
                           'execute if score #ho bm.rng matches 6..11 run effect give @s minecraft:instant_health 1 1 true',
                           'execute if score #ho bm.rng matches 2..5 run effect give @s minecraft:instant_health 1 0 true',
                           'effect give @s minecraft:fire_resistance 3 0 true', 'effect give @s minecraft:invisibility 2 0 true',
                           'execute at @s run particle minecraft:wax_on ~ ~1 ~ 0.3 0.6 0.3 0 20', 'execute at @s run particle minecraft:end_rod ~ ~1 ~ 0.2 0.5 0.2 0.02 12',
                           'execute at @s run playsound minecraft:item.trident.return player @a[distance=..16] ~ ~ ~ 1 1.4',
                           title('@s', 'actionbar', [T('You were never there.', GOLD, bold=True)])])
    fn('p105/alibi/go', ['$tp @s $(x) $(y) $(z) $(r) ~'])

    # ================================================================== THE COUNTERFEITER'S PRESS: a Token a day
    fn('p105/press/place', ['execute unless function bm:p37/allowed run return run ' + say('Not here.'),
                            'execute if score @s bm.prs matches 1 run return run ' + say('You have a press set up already - one press per crook. (Sneak + punch it to pick it up.)', 'red'),
                            'scoreboard players set #placed bm.rng 0', 'scoreboard players set #ray bm.rng 50', 'tag @s add bm.placer',
                            'execute anchored eyes positioned ^ ^ ^ run function bm:p105/press/ray', 'tag @s remove bm.placer',
                            'execute if score #placed bm.rng matches 0 run return run ' + say('Look at the floor within 5 blocks.'),
                            'execute if score #placed bm.rng matches 2 run return run ' + say('Something is in the way there.'),
                            'execute if score #placed bm.rng matches 3 run return run ' + say('On a floor - not a wall or a ceiling.'),
                            f'execute unless entity @s[gamemode=creative] run clear @s {holds("counterfeiters_press")} 1', 'scoreboard players set @s bm.prs 1',
                            say('The press is set up. It prints a Token a day for you - right-click it to collect.', '#e080ff'),
                            'playsound minecraft:block.anvil.place block @a[distance=..16] ~ ~ ~ 0.6 1.3'])
    fn('p105/press/ray', ['execute unless block ^ ^ ^0.1 #minecraft:replaceable run return run function bm:p105/press/hit',
                          'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.1 run function bm:p105/press/ray'])
    fn('p105/press/hit', ['execute positioned ^ ^ ^0.1 align xyz positioned ~0.5 ~0.5 ~0.5 run summon minecraft:marker ~ ~ ~ {Tags:["bm.prm"]}',
                          'execute align xyz positioned ~0.5 ~0.5 ~0.5 positioned ~ ~-1 ~ if entity @e[type=minecraft:marker,tag=bm.prm,distance=..0.1] positioned ~ ~1 ~ run function bm:p105/press/floor',
                          'execute if score #placed bm.rng matches 0 run scoreboard players set #placed bm.rng 3', 'kill @e[type=minecraft:marker,tag=bm.prm]'])
    press_disp = snbt({'Tags': ['bm.press', 'bm.prnew'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:press3d'}},
                       'item_display': 'fixed', 'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                                                   'translation': [F(0), F(0.5), F(0)], 'scale': [F(1)] * 3}})
    press_hit = snbt({'Tags': ['bm.presshit', 'bm.prnew'], 'width': F(0.9), 'height': F(1.0), 'response': B(1)})
    fn('p105/press/floor', ['execute unless block ~ ~ ~ #minecraft:replaceable run return run scoreboard players set #placed bm.rng 2',
                            'execute positioned ~ ~-0.5 ~ if entity @e[type=minecraft:interaction,tag=bm.presshit,distance=..0.8] run return run scoreboard players set #placed bm.rng 2',
                            f'execute positioned ~ ~-0.5 ~ rotated as @a[tag=bm.placer,limit=1] rotated ~180 0 run summon minecraft:item_display ~ ~ ~ {press_disp}',
                            f'execute positioned ~ ~-0.5 ~ run summon minecraft:interaction ~ ~ ~ {press_hit}',
                            'execute positioned ~ ~-0.5 ~ run scoreboard players operation @e[tag=bm.prnew,distance=..0.1] bm.prso = @a[tag=bm.placer,limit=1] bm.pid',
                            'execute positioned ~ ~-0.5 ~ run scoreboard players operation @e[tag=bm.prnew,distance=..0.1] bm.prsd = #day bm.bm',
                            'execute positioned ~ ~-0.5 ~ rotated as @a[tag=bm.placer,limit=1] run tp @e[type=minecraft:item_display,tag=bm.prnew,distance=..0.1] ~ ~ ~ ~180 0',
                            'execute positioned ~ ~-0.5 ~ run tag @e[tag=bm.prnew,distance=..0.1] remove bm.prnew', 'particle minecraft:wax_on ~ ~ ~ 0.3 0.3 0.3 0 10',
                            'scoreboard players set #placed bm.rng 1'])
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.presshit] if data entity @s interaction at @s run function bm:p105/press/click',
             'execute as @e[type=minecraft:interaction,tag=bm.presshit] if data entity @s attack at @s run function bm:p105/press/punch']
    fn('p105/press/click', ['scoreboard players operation #po bm.rng = @s bm.prso', 'scoreboard players operation #pd bm.rng = @s bm.prsd', 'tag @s add bm.prme',
                            'execute on target run function bm:p105/press/who', 'tag @s remove bm.prme', 'data remove entity @s interaction'])
    fn('p105/press/who', ['execute unless score @s bm.pid = #po bm.rng run return run ' + say('Somebody else\'s press - it prints for them.'),
                          'function bm:p105/press/collect'])
    fn('p105/press/collect', ['scoreboard players operation #n bm.rng = #day bm.bm', 'scoreboard players operation #n bm.rng -= #pd bm.rng',
                              f'execute if score #n bm.rng matches {PRESS_MAX + 1}.. run scoreboard players set #n bm.rng {PRESS_MAX}',
                              'execute if score #n bm.rng matches ..0 run return run ' + title('@s', 'actionbar', T('The ink\'s still wet - come back tomorrow.', 'gray')),
                              'scoreboard players operation @e[type=minecraft:interaction,tag=bm.prme,limit=1] bm.prsd = #day bm.bm',
                              tellraw('@s', P + [T('The press clacks out ', '#e080ff'), num('#n'), T(' Black Market Token(s).', '#e080ff')]),
                              'function bm:p105/press/pay', 'playsound minecraft:block.anvil.use block @a[distance=..12] ~ ~ ~ 0.5 1.6'])
    fn('p105/press/pay', ['execute if score #n bm.rng matches ..0 run return 0', 'loot give @s loot bm:items/token', 'scoreboard players remove #n bm.rng 1', 'function bm:p105/press/pay'])
    fn('p105/press/punch', ['scoreboard players operation #po bm.rng = @s bm.prso', 'scoreboard players operation #pd bm.rng = @s bm.prsd', 'tag @s add bm.prme',
                            'execute on attacker if predicate bm:p20/sneaking if score @s bm.pid = #po bm.rng run function bm:p105/press/take',
                            'tag @s remove bm.prme', 'data remove entity @s attack'])
    fn('p105/press/take', ['function bm:p105/press/collect', 'scoreboard players set @s bm.prs 0', G.give('counterfeiters_press'),
                           'execute as @e[type=minecraft:interaction,tag=bm.prme,limit=1] at @s run kill @e[type=minecraft:item_display,tag=bm.press,distance=..0.6]',
                           'kill @e[type=minecraft:interaction,tag=bm.prme]', 'playsound minecraft:block.anvil.break block @a[distance=..12] ~ ~ ~ 0.5 1.4',
                           say('You fold the press up and take it with you.')])
    # (a press with Tokens waiting puffs a little paper, for whoever's near)
    second.append('execute as @e[type=minecraft:interaction,tag=bm.presshit] at @s if entity @a[distance=..16] unless score @s bm.prsd = #day bm.bm run '
                  'particle minecraft:white_ash ~ ~1.1 ~ 0.15 0.05 0.15 0.01 6')
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:interaction,tag=bm.presshit]', 'kill @e[type=minecraft:item_display,tag=bm.press]']
    fn('admin/raid_finds', [G.give(i) for i in ('forgeheart', 'the_alibi', 'counterfeiters_press', 'crate_raw', 'crate_adventure', 'crate_mineral', 'tip_bloodmoon', 'tip_alien')] +
       [G.give(f'laurel_t{t}') for t in range(1, 6)])

    G.FUNCS['admin/help'] += [tellraw('@s', [T('/function bm:admin/raid_finds', 'yellow'), T('  the 2.68 raid items: crates, tip-offs, laurels, Forgeheart, the Alibi, the Press', 'gray')]),
                              tellraw('@s', [T('/function bm:admin/heist_plans_anywhere', 'yellow'), T('  the Heist Plans work from anywhere (', 'gray'),
                                             T('heist_plans_safe', 'yellow'), T(' restores the safe-ground rule)', 'gray')])]

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    f[-1:-1] = fast
    s_ = G.FUNCS['loop/second']
    s_[-1:-1] = second


def rp(R):
    g = R.grid
    LP = {'.': None}
    for t, (k_, nm, col, rgb) in LAUREL.items():
        dark = '#%02x%02x%02x' % tuple(int(c * 255 * 0.62) for c in rgb)
        lit = '#%02x%02x%02x' % tuple(min(255, int(c * 255 * 1.08)) for c in rgb)
        R.ICONS[f'laurel_t{t}'] = g(['................', '................', '...g........g...', '..gYg......gYg..', '..gYYg....gYYg..', '..gYYYg..gYYYg..', '...gYYYggYYYg...',
                                     '....gYYYYYYg....', '.....gYYYYg.....', '......gggg......', '.......rr.......', '......rRRr......', '.......rr.......', '................', '................', '................'],
                                    dict(g=dark, Y=lit, r='#8a1010', R='#d03030'))
    R.ICONS['crate_raw'] = g(['................', '..kkkkkkkkkkkk..', '..kwwwwwwwwwwk..', '..kwbbbbbbbbwk..', '..kwbwwwwwwbwk..', '..kwbwiiccwbwk..', '..kwbwiiccwbwk..', '..kwbwllsswbwk..',
                              '..kwbwllsswbwk..', '..kwbwwwwwwbwk..', '..kwbbbbbbbbwk..', '..kwwwwwwwwwwk..', '..kkkkkkkkkkkk..', '................', '................', '................'],
                             dict(k='#3a2410', w='#8a5a30', b='#5a3a18', i='#d8d8d8', c='#e07a4a', l='#6a4a2a', s='#8a8a8a'))
    R.ICONS['crate_adventure'] = g(['................', '..kkkkkkkkkkkk..', '..kwwwwwwwwwwk..', '..kwbbbbbbbbwk..', '..kwbwwwwwwbwk..', '..kwbweeppwbwk..', '..kwbweeppwbwk..', '..kwbwggaawbwk..',
                                    '..kwbwggaawbwk..', '..kwbwwwwwwbwk..', '..kwbbbbbbbbwk..', '..kwwwwwwwwwwk..', '..kkkkkkkkkkkk..', '................', '................', '................'],
                                   dict(k='#1a3040', w='#3a7090', b='#204a60', e='#7aff4a', p='#2a8a7a', g='#ffd040', a='#d03030'))
    R.ICONS['crate_mineral'] = g(['................', '..kkkkkkkkkkkk..', '..kwwwwwwwwwwk..', '..kwbbbbbbbbwk..', '..kwbwwwwwwbwk..', '..kwbwggeewbwk..', '..kwbwggeewbwk..', '..kwbwdd..wbwk..',
                                  '..kwbwddyywbwk..', '..kwbwwwwwwbwk..', '..kwbbbbbbbbwk..', '..kwwwwwwwwwwk..', '..kkkkkkkkkkkk..', '................', '................', '................'],
                                 dict(k='#4a3808', w='#c8a040', b='#8a6a18', g='#ffd840', e='#3ad070', d='#6ae8e0', y='#ffeaa0'))
    R.ICONS['tip_bloodmoon'] = g(['................', '..pppppppppp....', '..pwwwwwwwwwp...', '..pwRRwwwwwwwp..', '..pwRRRwkkkkwp..', '..pwwRwwwwwwwp..', '..pwwwwkkkkkwp..', '..pwwwwwwwwwwp..',
                                  '..pwkkkkwwRwwp..', '..pwwwwwwRRRwp..', '..pwkkkwwwRwwp..', '..pwwwwwwwwwwp..', '..pppppppppppp..', '................', '................', '................'],
                                 dict(p='#8a7a5a', w='#e8dcc0', k='#5a4a3a', R='#c01010'))
    R.ICONS['tip_alien'] = g(['................', '.......gg.......', '......g..g......', '.....g.gg.g.....', '.......gg.......', '......kkkk......', '.....kGGGGk.....', '.....kGwwGk.....',
                              '.....kGGGGk.....', '.....kkkkkk.....', '....kssssssk....', '....kssssssk....', '....kkkkkkkk....', '................', '................', '................'],
                             dict(g='#7aff6a', k='#202a20', G='#3ad04a', w='#d0ffd0', s='#6a7a6a'))
    R.ICONS['forgeheart'] = g(['................', '................', '...kk.....kk....', '..kRRk...kRRk...', '.kRooRk.kRooRk..', '.kRoyoRkRoyyoRk.', '.kRoyyoooyyyoRk.', '.kRooyyyyyyooRk.',
                               '..kRooyyyyooRk..', '...kRooyyooRk...', '....kRooooRk....', '.....kRooRk.....', '......kRRk......', '.......kk.......', '................', '................'],
                              dict(k='#2a1008', R='#8a2010', o='#ff6a20', y='#ffd060'))
    R.ICONS['the_alibi'] = g(['.......cc.......', '......c..c......', '.....c....c.....', '......c..c......', '......oYYo......', '....ooYYYYoo....', '...oYwwwwwwYo...', '..oYwwwkwwwwYo..',
                              '..oYwwwkwwwwYo..', '..oYwwwkkkwwYo..', '..oYwwwwwwwwYo..', '...oYwwwwwwYo...', '....ooYYYYoo....', '......oooo......', '................', '................'],
                             dict(c='#ffd870', o='#7a5410', Y='#ffcf40', w='#fff6dc', k='#3a2410'))
    # the press: a little 3D iron-and-oak press (in the hand and set down)
    c = R.cube
    R.HATS['press3d'] = ({'o': 'minecraft:block/dark_oak_planks', 'i': 'minecraft:block/iron_block', 'g': 'minecraft:block/gold_block', 'p': 'minecraft:block/white_concrete',
                          'k': 'minecraft:block/polished_blackstone'}, [
        c((2, 0, 4), (14, 2, 12), 'o'), c((2.5, 2, 7), (4, 13, 9), 'i'), c((12, 2, 7), (13.5, 13, 9), 'i'), c((2, 13, 6.5), (14, 15, 9.5), 'o'),
        c((7.5, 8, 7.5), (8.5, 13, 8.5), 'g'), c((5, 7, 5), (11, 8, 11), 'i'), c((5.5, 2, 5.5), (10.5, 2.3, 10.5), 'p'),
        c((4.5, 15, 7.6), (11.5, 15.6, 8.4), 'g'), c((7.6, 15, 4.5), (8.4, 15.6, 11.5), 'g'), c((3, 0.5, 3.5), (13, 1.5, 4), 'k')])
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + ('press3d',)

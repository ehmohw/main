"""2.66: TROPHIES IN SIX METALS, and THE BOND SIGILS.

TROPHIES: twelve vault rooms (the seven first ones and the Signal Lamps, the Lamp Floor, the Tumbler Lock, the Bell Tower
  and the Crumbling Rafters), each in six metals - COPPER for a flawless clear on Tier I, IRON on II, GOLD on III, EMERALD
  on IV, DIAMOND on V, and NETHERITE on Tier V with three tries and nobody knocked out all heist. A flawless room only
  PROMISES the trophy: it's yours when the crew gets out, and lost if you're knocked out on the way. One of each kind and
  metal - another gets 3 coins in your Gutter Bank. They're little 3D statues now, bigger and grander metal by metal, the
  room's emblem on the plinth; sneak + use to set one down, sneak + punch to take it back. A full shelf of one metal
  (all twelve rooms) pays once, into your Gutter Bank: copper 48 coins + 1 Insignia, iron 96 + 2, gold 160 + 3,
  emerald 240 + 4, diamond 320 + 6, netherite 640 + 10. (2.67: never BM Trophies - those aren't a raid prize.)
  The old gold trophies stay what they were (and look like the new gold ones).
THE BOND SIGILS: eight now, and each a different power. When the heist begins, the sigils the crew carries are attuned -
  off-hands first, then pockets - TWO AT MOST, and their power is the whole crew's for that heist:
  MENDING (regeneration), FURY (Strength), BULWARK (Resistance), SWIFTNESS (Speed), WARDING (no poison, wither,
  slowness or burning), FORTUNE (+1 coin a guard, and more spoils), VIGOR (+2 hearts), SIGHT (see in the dark; guards
  glow). Mending still comes free with your first party heist; Goldtooth sells the rest (coins and Captain's Insignia),
  and champions and hidden stashes sometimes give one up. Out of the vault, Mending still mends your party."""
from items import item, T, TOTEM, ITEMS, fancy_name, item_symbol
from useitem import hold, HOLD
from nbt import snbt, B, F, Int
import phase28 as P28
import phase70 as P70
import phase70_rooms as RM
import phase71 as P71
import phase76_rooms as R6
import phase80 as P80

GOLD = '#ffcf40'
TK = RM.KINDS + ['lamps', 'lightsout', 'tumbler', 'climb', 'rafters']
NAMES = dict(RM.NAMES, **R6.NAMES)
TSHORT = dict(P71.TROPHY_NAME, lamps='Signal Lamps', lightsout='Lamp Floor', tumbler='Tumbler Lock', climb='Bell Tower', rafters='Rafters')
METALS = [  # (key, name, colour, block texture, how)
    ('copper', 'Copper', '#e0864e', 'minecraft:block/copper_block', 'a flawless room on Tier I'),
    ('iron', 'Iron', '#dcdcdc', 'minecraft:block/iron_block', 'a flawless room on Tier II'),
    ('gold', 'Gold', GOLD, 'minecraft:block/gold_block', 'a flawless room on Tier III'),
    ('emerald', 'Emerald', '#3ce07a', 'minecraft:block/emerald_block', 'a flawless room on Tier IV'),
    ('diamond', 'Diamond', '#62ece4', 'minecraft:block/diamond_block', 'a flawless room on Tier V'),
    ('netherite', 'Netherite', '#a08090', 'minecraft:block/netherite_block', 'Tier V, three tries, nobody knocked out')]
NMET = len(METALS)
SET_PRIZE = {1: (48, 1), 2: (96, 2), 3: (160, 3), 4: (240, 4), 5: (320, 6), 6: (640, 10)}      # (2.67) a full shelf: coins banked, Captain's Insignia
SIGILS = [  # (n, iid, name, colour, the crew gets..., Goldtooth's price in coins, insignia)
    (1, 'bond_sigil', 'Mending', '#ff9ad8', 'regeneration', 48, 1),
    (2, 'sigil_fury', 'Fury', '#ff5a4a', 'Strength - every blow harder', 72, 2),
    (3, 'sigil_bulwark', 'Bulwark', '#8ab0ff', 'Resistance - every blow softer', 72, 2),
    (4, 'sigil_swift', 'Swiftness', '#7affd8', 'Speed - quicker on your feet', 56, 1),
    (5, 'sigil_warding', 'Warding', '#fff07a', 'no poison, wither, slowness or burning', 56, 1),
    (6, 'sigil_fortune', 'Fortune', GOLD, '+1 coin into the pot a guard, and more spoils', 64, 2),
    (7, 'sigil_vigor', 'Vigor', '#ff8a3a', '+2 hearts', 64, 2),
    (8, 'sigil_sight', 'Sight', '#c8a0ff', 'night vision, and every guard near you glows', 48, 1)]
NS = len(SIGILS)

for _k in TK:
    for _m, (_mk, _mn, _col, _tex, _how) in enumerate(METALS, 1):
        item(f'trophy_{_k}_{_mk}', TOTEM, f'{_mn} {TSHORT[_k]} Trophy', _col,
             [f'{NAMES[_k]}, beaten without a slip.', (f'{_mn}: {_how}.', _col), ('Sneak + use on a block: set it down.', 'blue'), ('Sneak + punch: pick it up.', 'gray')],
             model=f'bm:trophy3d_{_k}_{_m}', stack=1, cat='fun', comps=hold('none'), bold=_m == NMET)
        HOLD[f'trophy_{_k}_{_mk}'] = 'bm:p81/place'
for _k in RM.KINDS:                                    # the old gold statues look like the new gold ones
    ITEMS[f'trophy_{_k}']['comps']['minecraft:item_model'] = f'bm:trophy3d_{_k}_3'
for _n, _iid, _nm, _col, _what, _c, _i in SIGILS[1:]:
    item(_iid, TOTEM, f'Bond Sigil of {_nm}', _col, [f'A sigil that hums with {_nm.lower()}.', ('Carry it into a heist: when it begins, the', 'blue'),
                                                    (f'whole crew gets {_what}.', 'blue'), ('Two sigils at most are attuned a heist', 'gray'),
                                                    ('(off-hands first, then pockets).', 'gray')], model=f'bm:{_iid}', stack=1, cat='magic')
ITEMS['bond_sigil']['comps']['minecraft:item_name'] = fancy_name('Bond Sigil of Mending', '#ff9ad8', item_symbol('bond_sigil', TOTEM, 'magic'))
MENDING_LORE = [T('A gold sigil, warm when a friend is near.', 'gray'), T('In a heist: the whole crew regenerates', 'blue'),
                                                  T('(two sigils at most are attuned a heist).', 'gray'), T('Out of one: near a party member who', 'blue'),
                                                  T('carries one too, you both regenerate.', 'blue')] + ITEMS['bond_sigil']['comps']['minecraft:lore'][-1:]
ITEMS['bond_sigil']['comps']['minecraft:lore'] = MENDING_LORE

_prev_goldtooth = P70.goldtooth


def _goldtooth():
    from gen_dp import offer
    d = _prev_goldtooth()
    d['Offers']['Recipes'] += [offer(('gutter_coin', c), (iid, 1), ('captains_insignia', i)) for n, iid, nm, col, what, c, i in SIGILS]
    return d


P70.goldtooth = _goldtooth


def extend_offers(O, offer):
    pass


def generate(G):
    fn, wjson, title, tellraw, give = G.fn, G.wjson, G.title, G.tellraw, G.give
    ITEMS['bond_sigil']['comps']['minecraft:lore'] = MENDING_LORE           # (phase75 rewrote it since)
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    P = [T('[Vault] ', GOLD, bold=True)]
    tick, fast, second = [], [], []
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    tro = [f'bm.tr{m}' for m in range(1, NMET + 1)]
    objs = tro + ['bm.tpd', 'bm.trset', 'bm.gvsa', 'bm.gvsb']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    inst = lambda f: f'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run function {f}'
    bit = lambda obj, b, who='@s': [f'scoreboard players operation #q bm.rng = {who} {obj}', f'scoreboard players set #bit bm.rng {2 ** b}',
                                    'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng']

    # ================================================================== TROPHIES: promised by a flawless room...
    for j, k in enumerate(TK):
        fn(f'p81/flaw/{k}', bit('bm.tpd', j) + ['execute if score #q bm.rng matches 1 run return 0', f'scoreboard players add @s bm.tpd {2 ** j}',
                                                tellraw('@s', P + [T('Flawless! ', GOLD, bold=True), T(f'{NAMES[k]}: its trophy is promised to you - ', 'gray'),
                                                                   T('get out with the crew, and don\'t get knocked out.', 'white')])])
    for k in RM.KINDS:
        G.FUNCS[f'p70/trophy/{k}'] = [f'function bm:p81/flaw/{k}']               # (no more trophy in your hand on the spot, nor phase75's coins)
    G.FUNCS['p70/solved'] += [f'execute if entity @s[tag=bm.gvr_{k}] if score @s bm.gvf matches 0 as @a[tag=bm.gvp,distance=..300] if score @s bm.gvi = #gi bm.rng '
                              f'run function bm:p81/flaw/{k}' for k in TK[len(RM.KINDS):]]
    # ...lost to a knock-out, or a heist that fails or is left
    fn('p81/lose', ['execute unless score @s bm.tpd matches 1.. run return 0', 'scoreboard players set @s bm.tpd 0',
                    tellraw('@s', P + [T('Your promised trophies are gone. ', 'red'), T('(Flawless rooms only count if you see it through on your feet.)', 'gray')])])
    G.FUNCS['p70/revive'].append('function bm:p81/lose')
    G.FUNCS['p75/after_fail'].append('function bm:p81/lose')
    G.FUNCS['p70/unraid'].append('scoreboard players set @s bm.tpd 0')
    for s in range(P70.SLOTS):
        for f in (f'p70/s{s}/enter', f'p70/s{s}/join'):
            G.FUNCS[f].append('scoreboard players set @s bm.tpd 0')
    # ...and paid out with the haul: the metal from the tier (netherite: Tier V, three tries, nobody knocked out)
    pay = G.FUNCS['p70/payout_inst']
    k_ = next(i for i, l in enumerate(pay) if 'function bm:p70/haul' in l)
    pay[k_:k_] = ['scoreboard players operation #tmet bm.rng = @s bm.gvt', 'execute if score #tmet bm.rng matches ..0 run scoreboard players set #tmet bm.rng 1',
                  'execute if score #tmet bm.rng matches 6.. run scoreboard players set #tmet bm.rng 5',
                  'execute if score #tmet bm.rng matches 5 if score @s bm.gvdc matches 0 if score @s bm.gvlc matches ..3 run scoreboard players set #tmet bm.rng 6']
    G.FUNCS['p70/haul'].append('function bm:p81/award')
    fn('p81/init_me', [f'execute unless score @s {o} matches 0.. run scoreboard players set @s {o} 0' for o in tro + ['bm.tpd', 'bm.trset']])
    fn('p81/award', ['function bm:p81/init_me', 'execute if score @s bm.tpd matches 0 run return 0'] +
       sum((bit('bm.tpd', j) + [f'execute if score #q bm.rng matches 1 run function bm:p81/aw/{k}'] for j, k in enumerate(TK)), []) +
       ['scoreboard players set @s bm.tpd 0', 'function bm:p81/sets'])
    for j, k in enumerate(TK):
        fn(f'p81/aw/{k}', [f'execute if score #tmet bm.rng matches {m} run return run function bm:p81/aw/{k}_{m}' for m in range(1, NMET + 1)])
        for m, (mk, mn, col, tex, how) in enumerate(METALS, 1):
            fn(f'p81/aw/{k}_{m}', bit(f'bm.tr{m}', j) +
               ['execute if score #q bm.rng matches 1 run scoreboard players add @s bm.gbc 3',
                'execute if score #q bm.rng matches 1 run return run ' + tellraw('@s', P + [T(f'{mn} {TSHORT[k]} Trophy', col), T(' - you have it already: ', 'gray'),
                                                                                         T('+3 coins in your Gutter Bank.', GOLD)]),
                f'scoreboard players add @s bm.tr{m} {2 ** j}', f'loot give @s loot bm:items/trophy_{k}_{mk}',
                tellraw('@s', P + [T('TROPHY! ', col, bold=True), T(f'{mn} {TSHORT[k]} Trophy', col), T(' - for your shelf.', 'gray')]),
                'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.8 1.3'])
    # (as a player) #c1..#c6: trophies of each metal; #tro: all of them
    cnt = ['function bm:p81/init_me', 'scoreboard players set #tro bm.rng 0']
    for m in range(1, NMET + 1):
        cnt += [f'scoreboard players set #c{m} bm.rng 0', f'scoreboard players operation #x bm.rng = @s bm.tr{m}']
        cnt += sum((['scoreboard players operation #q bm.rng = #x bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng',
                     f'scoreboard players operation #c{m} bm.rng += #q bm.rng', 'scoreboard players operation #x bm.rng /= #2 bm.rng'] for _ in TK), [])
        cnt.append(f'scoreboard players operation #tro bm.rng += #c{m} bm.rng')
    fn('p81/count_all', cnt)
    # a full shelf of one metal: BM Trophies, once
    fn('p81/sets', ['function bm:p81/count_all'] + [f'execute if score #c{m} bm.rng matches {len(TK)}.. run function bm:p81/set_{m}' for m in range(1, NMET + 1)])
    for m, (mk, mn, col, tex, how) in enumerate(METALS, 1):
        coins, ins = SET_PRIZE[m]
        fn(f'p81/set_{m}', bit('bm.trset', m) + ['execute if score #q bm.rng matches 1 run return 0', f'scoreboard players add @s bm.trset {2 ** m}',
                                                 'function bm:p80/init_me', f'scoreboard players add @s bm.gbc {coins}', f'scoreboard players add @s bm.gb6 {ins}',
                                                 'title @s times 10 60 20', title('@s', 'title', T(f'{mn.upper()} SHELF', col, bold=True)),
                                                 title('@s', 'subtitle', T(f'Every room in {mn.lower()} - {coins} coins and {ins} Insignia into your bank', 'gray')),
                                                 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 0.8',
                                                 tellraw('@a', P + [{'selector': '@s', 'color': 'white'}, T(f' has every vault trophy in {mn.lower()}!', col)])])

    # ---- placing and taking (every metal trophy alike: the statue keeps the very item)
    fn('p81/place', ['execute unless predicate bm:p20/sneaking run return run ' + say('Sneak + use on a block to set it down.'),
                     'scoreboard players set #placed bm.rng 0', 'scoreboard players set #ray bm.rng 25', 'tag @s add bm.placer',
                     'execute anchored eyes positioned ^ ^ ^ run function bm:p81/place_ray', 'tag @s remove bm.placer',
                     'execute if score #placed bm.rng matches 0 run return run ' + say('Look at the top of a block within 5 blocks.'),
                     'execute unless entity @s[gamemode=creative] run item replace entity @s weapon.mainhand with minecraft:air'])
    fn('p81/place_ray', ['execute unless block ~ ~ ~ #minecraft:replaceable run return run function bm:p81/place_hit',
                         'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p81/place_ray'])
    fn('p81/place_hit', ['execute align xyz positioned ~0.5 ~1 ~0.5 unless block ~ ~ ~ #minecraft:replaceable run return 0',
                         'execute align xyz positioned ~0.5 ~1 ~0.5 if entity @e[type=minecraft:interaction,tag=bm.gvdeco,distance=..0.6] run return 0',
                         'execute align xyz positioned ~0.5 ~1 ~0.5 rotated as @a[tag=bm.placer,limit=1] rotated ~180 0 run function bm:p81/spawn',
                         'scoreboard players set #placed bm.rng 1'])
    ident = [F(0), F(0), F(0), F(1)]
    fn('p81/spawn', ['summon minecraft:item_display ~ ~ ~ ' + snbt({'Tags': ['bm.gvdecod', 'bm.gvdnew'], 'item_display': 'fixed',
                                                                   'transformation': {'left_rotation': ident, 'right_rotation': ident,
                                                                                      'translation': [F(0), F(0.42), F(0)], 'scale': [F(0.84)] * 3}}),
                     'item replace entity @e[type=minecraft:item_display,tag=bm.gvdnew,distance=..0.5,limit=1] contents from entity @a[tag=bm.placer,limit=1] weapon.mainhand',
                     'summon minecraft:interaction ~ ~ ~ ' + snbt({'Tags': ['bm.gvdeco', 'bm.gvdnew', 'bm.gvdk_mtro'], 'width': F(0.7), 'height': F(0.9), 'response': B(1)}),
                     'tp @e[tag=bm.gvdnew,distance=..0.5] ~ ~ ~ ~ 0', 'tag @e[tag=bm.gvdnew,distance=..0.5] remove bm.gvdnew',
                     'playsound minecraft:block.metal.place block @a[distance=..16] ~ ~ ~ 1 1', 'particle minecraft:wax_on ~ ~0.5 ~ 0.3 0.3 0.3 0 10'])
    G.FUNCS['p71/deco/pick'][0:0] = ['execute if entity @e[type=minecraft:interaction,tag=bm.gvdme,tag=bm.gvdk_mtro] at @e[type=minecraft:interaction,tag=bm.gvdme,limit=1] '
                                     'run function bm:p81/pick']
    fn('p81/pick', ['summon minecraft:item ~ ~0.3 ~ {Tags:["bm.trnew"],Item:{id:"minecraft:stone",count:1},PickupDelay:0s}',
                    'data modify entity @e[type=minecraft:item,tag=bm.trnew,distance=..1,limit=1] Item set from entity @e[type=minecraft:item_display,tag=bm.gvdecod,distance=..0.6,limit=1] item',
                    'tp @e[type=minecraft:item,tag=bm.trnew,distance=..1] @s', 'tag @e[type=minecraft:item,tag=bm.trnew] remove bm.trnew'])

    # ---- THE TROPHY CASE (the office's third door)
    case = ['function bm:p81/count_all', 'data remove storage bm:ui tc', f'scoreboard players set @s bm.menu {P80.MENU_CODE + 3}']
    for m in range(1, NMET + 1):
        case.append(f'execute store result storage bm:ui tc.c{m} int 1 run scoreboard players get #c{m} bm.rng')
    for j, k in enumerate(TK):
        for m, (mk, mn, col, tex, how) in enumerate(METALS, 1):
            case += [f'data modify storage bm:ui tc.r_k{j}m{m} set value {snbt(T("■", "#3a3a3a"))}'] + bit(f'bm.tr{m}', j) + \
                    [f'execute if score #q bm.rng matches 1 run data modify storage bm:ui tc.r_k{j}m{m} set value {snbt(T("■", col))}']
    case += ['function bm:p81/case_dlg with storage bm:ui tc']
    fn('p81/case', case)
    raw = lambda n: f'@@RAW:{n}@@'
    row = lambda j: [T(f'{TSHORT[TK[j]]:<16}', 'gray')] + [raw(f'r_k{j}m{m}') for m in range(1, NMET + 1)]
    half = (len(TK) + 1) // 2
    rows = []
    for j in range(half):
        line = row(j)
        if j + half < len(TK):
            line += [T('      ', 'gray')] + row(j + half)
        rows.append(P28.body(line, 380))
    cdlg = P28.multi([T('THE TROPHY CASE', GOLD, bold=True), T('  ·  twelve rooms, six metals', 'gray')],
                     [P28.body([T('Clear a room without a slip; get out with the crew, on your feet. The tier sets the metal:', 'gray')], 380),
                      P28.body(sum(([T(f'{mn} ', col, bold=True), T(f'{"V+" if m == NMET else ["I", "II", "III", "IV", "V"][m - 1]}  ', 'dark_gray')]
                                    for m, (mk, mn, col, tex, how) in enumerate(METALS, 1)), []) + [T('(netherite: Tier V, 3 tries, nobody knocked out)', 'dark_gray')], 380)] +
                     rows +
                     [P28.body(sum(([T(f'{mn} ', col), T(f'$(c{m})', 'white', bold=True), T(f'/{len(TK)}   ', 'dark_gray')]
                                    for m, (mk, mn, col, tex, how) in enumerate(METALS, 1)), []), 380),
                      P28.body([T('A full shelf of one metal pays once - coins and Captain\'s Insignia into your bank: ', 'gray')] +
                               sum(([T(f'{mn.lower()} {SET_PRIZE[m][0]} + {SET_PRIZE[m][1]}', col), T(', ' if m < NMET else '.', 'gray')] for m, (mk, mn, col, tex, how) in enumerate(METALS, 1)), []), 380)],
                     [P28.btn(T('« Office', 'gray'), P80.MENU_CODE, width=120)], columns=1)
    fn('p81/case_dlg', [f'$dialog show @s {P28.inline(cdlg)}'])

    # ================================================================== THE BOND SIGILS: two attuned when the heist begins
    beg = G.FUNCS['p70/begin']
    k_ = max(i for i, l in enumerate(beg) if l.startswith('tag @a[tag=bm.gvme] remove bm.gvme'))
    beg.insert(k_, 'function bm:p81/attune')
    fn('p81/attune', ['scoreboard players set #sa bm.rng 0', 'scoreboard players set #sb bm.rng 0', 'scoreboard players set #sx bm.rng 0',
                      'execute as @a[tag=bm.gvme] run function bm:p81/att_off', 'execute as @a[tag=bm.gvme] run function bm:p81/att_inv',
                      inst('bm:p81/att_set'), 'execute as @a[tag=bm.gvme] run function bm:p81/att_say'])
    fn('p81/att_off', [f'execute if items entity @s weapon.offhand {holds(iid)} run function bm:p81/att_add_{n}' for n, iid, *_r in SIGILS])
    fn('p81/att_inv', [f'execute if items entity @s container.* {holds(iid)} run function bm:p81/att_add_{n}' for n, iid, *_r in SIGILS])
    for n, iid, *_r in SIGILS:
        fn(f'p81/att_add_{n}', [f'execute if score #sa bm.rng matches {n} run return 0', f'execute if score #sb bm.rng matches {n} run return 0',
                                f'execute if score #sa bm.rng matches 0 run return run scoreboard players set #sa bm.rng {n}',
                                f'execute if score #sb bm.rng matches 0 run return run scoreboard players set #sb bm.rng {n}', 'scoreboard players set #sx bm.rng 1'])
    fn('p81/att_set', ['scoreboard players operation @s bm.gvsa = #sa bm.rng', 'scoreboard players operation @s bm.gvsb = #sb bm.rng'])
    att = []
    for slot in ('#sa', '#sb'):
        att += [f'execute if score {slot} bm.rng matches {n} run ' + tellraw('@s', P + [T('Bond Sigil attuned: ', '#e8b8ff'), T(nm, col, bold=True), T(f' - the crew gets {what}.', 'gray')])
                for n, iid, nm, col, what, c, i in SIGILS]
    att += ['execute if score #sx bm.rng matches 1 run ' + tellraw('@s', P + [T('(More sigils in the crew\'s pockets - only two are attuned a heist.)', 'dark_gray')])]
    fn('p81/att_say', att)
    # each second: the crew of every running heist wears its sigils' tags, and the powers follow them
    tags = [f'bm.sg{n}' for n in range(1, NS + 1)]
    second += [f'tag @a[tag={t}] remove {t}' for t in tags] + \
              ['execute as @e[type=minecraft:marker,tag=bm.gvinst,scores={bm.gvst=2..3}] unless score @s bm.gvsa matches 0 run function bm:p81/sg/inst']
    fn('p81/sg/inst', ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'scoreboard players operation #sa bm.rng = @s bm.gvsa', 'scoreboard players operation #sb bm.rng = @s bm.gvsb',
                       'execute as @a[tag=bm.gvp] if score @s bm.gvi = #gi bm.rng run function bm:p81/sg/me'])
    fn('p81/sg/me', [f'execute if score #sa bm.rng matches {n} run tag @s add bm.sg{n}' for n in range(1, NS + 1)] +
       [f'execute if score #sb bm.rng matches {n} run tag @s add bm.sg{n}' for n in range(1, NS + 1)])
    bad = ['poison', 'wither', 'slowness']
    second += ['effect give @a[tag=bm.sg1] minecraft:regeneration 3 0 true', 'effect give @a[tag=bm.sg2] minecraft:strength 3 0 true',
               'effect give @a[tag=bm.sg3] minecraft:resistance 3 0 true', 'effect give @a[tag=bm.sg4] minecraft:speed 3 0 true'] + \
              [f'effect clear @a[tag=bm.sg5] minecraft:{e}' for e in bad] + \
              ['effect give @a[tag=bm.sg5] minecraft:fire_resistance 3 0 true', 'execute as @a[tag=bm.sg5] run data modify entity @s Fire set value -20s',
               'execute as @a[tag=bm.sg7] run attribute @s minecraft:max_health modifier add bm:sig_vigor 4 add_value', 'tag @a[tag=bm.sg7] add bm.sghb',
               'execute as @a[tag=bm.sghb,tag=!bm.sg7] run function bm:p81/sg/unvigor',
               'effect give @a[tag=bm.sg8] minecraft:night_vision 15 0 true',
               'execute as @a[tag=bm.sg8] at @s run effect give @e[tag=bm.gvg,distance=..24] minecraft:glowing 2 0 true']
    fn('p81/sg/unvigor', ['attribute @s minecraft:max_health modifier remove bm:sig_vigor', 'tag @s remove bm.sghb'])
    # Fortune: a coin more a guard, and a better chance of spoils
    kg = G.FUNCS['p75/kill_guard']
    k_ = next(i for i, l in enumerate(kg) if 'bm:p75/pot_add' in l)
    kg.insert(k_, 'execute if entity @s[tag=bm.sg6] run scoreboard players add #c bm.rng 1')
    dg = G.FUNCS['p80/drop_guard']
    k_ = next(i for i, l in enumerate(dg) if 'matches 34.. run return 0' in l)
    dg.insert(k_, 'execute if entity @s[tag=bm.sg6] if score #r bm.rng matches 34..50 run scoreboard players set #r bm.rng 1')
    # Mending outside the vault stays the party's own; inside, the attuned sigils rule
    G.FUNCS['p71/bond'].insert(0, 'execute if entity @s[tag=bm.gvp] run return 0')
    # champions and hidden stashes sometimes give one up (with the haul)
    from gen_dp import loot_entry
    wjson('bm/loot_table/p81/sigil.json', {'pools': [{'rolls': 1, 'entries': [dict(loot_entry(iid), weight=1) for n, iid, *_r in SIGILS[1:]]}]})
    rc = G.FUNCS['p76/roll_champion']
    rc.append('execute if score #r bm.rng matches 26..37 run function bm:p76/find {t:"bm:p81/sigil"}')
    sh = G.FUNCS['p76/secret/share']
    sh.append('execute if score #r bm.rng matches 16..21 run function bm:p76/find {t:"bm:p81/sigil"}')

    # ---- the Bond Sigils page (the office's fourth door)
    sp = ['data remove storage bm:ui sg', f'scoreboard players set @s bm.menu {P80.MENU_CODE + 4}', 'scoreboard players set #gi bm.rng 0',
          'scoreboard players operation #gi bm.rng = @s[tag=bm.gvp] bm.gvi', 'scoreboard players set #sa bm.rng 0', 'scoreboard players set #sb bm.rng 0',
          'execute if score #gi bm.rng matches 1.. as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run function bm:p81/sg/read']
    for n, iid, nm, col, what, c, i in SIGILS:
        sp += [f'data modify storage bm:ui sg.r_s{n} set value {snbt(T("—", "dark_gray"))}',
               f'execute if items entity @s container.* {holds(iid)} run data modify storage bm:ui sg.r_s{n} set value {snbt(T("✔ carried", "green"))}',
               f'execute if items entity @s weapon.offhand {holds(iid)} run data modify storage bm:ui sg.r_s{n} set value {snbt(T("✔ off-hand", "green", bold=True))}',
               f'execute if score #sa bm.rng matches {n} run data modify storage bm:ui sg.r_s{n} set value {snbt(T("✦ ATTUNED", GOLD, bold=True))}',
               f'execute if score #sb bm.rng matches {n} run data modify storage bm:ui sg.r_s{n} set value {snbt(T("✦ ATTUNED", GOLD, bold=True))}']
    sp.append('function bm:p81/sigils_dlg with storage bm:ui sg')
    fn('p81/sigils', sp)
    fn('p81/sg/read', ['scoreboard players operation #sa bm.rng = @s bm.gvsa', 'scoreboard players operation #sb bm.rng = @s bm.gvsb'])
    sdlg = P28.multi([T('THE BOND SIGILS', '#e8b8ff', bold=True), T('  ·  two at most, each heist', 'gray')],
                     [P28.body([T('When the heist begins, the sigils the crew carries are attuned - off-hands first, then pockets - ', 'gray'),
                                T('two at most', 'white', bold=True), T(', and their power is the whole crew\'s.', 'gray')], 380)] +
                     [P28.body([T(f'{nm}: ', col, bold=True), T(what + '   ', 'gray'), raw(f'r_s{n}')], 380) for n, iid, nm, col, what, c, i in SIGILS] +
                     [P28.body([T('Mending comes with your first party heist. Goldtooth sells the rest; champions and hidden stashes hide a few.', 'dark_gray')], 380)],
                     [P28.btn(T('« Office', 'gray'), P80.MENU_CODE, width=120)], columns=1)
    fn('p81/sigils_dlg', [f'$dialog show @s {P28.inline(sdlg)}'])

    fn('admin/trophies_all', [f'scoreboard players set @s bm.tr{m} {2 ** len(TK) - 1}' for m in range(1, NMET + 1)] + ['function bm:p81/sets'])
    fn('admin/sigils', [give(iid) for n, iid, *_r in SIGILS])

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    f[-1:-1] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second

    # ================================================================== (2.67) EVERY PRIZE IN THE HAUL - nothing loose in your pockets or on the floor
    #  run-time finds (the Clockwork Cache, key fragments) wait in your pot like any other find (lost if the heist fails);
    #  the payout's extras (the contract's purse, the laurel, the Bond Sigil, vault trophies, netherite scrap) go in the crate
    HA, HB = '-200 64 -197', '-198 64 -197'
    def ins(table):
        return (f'execute in bm:gutter unless data block {HA} Items[26] run loot insert {HA} loot {table}', f'execute in bm:gutter if data block {HA} Items[26] run loot insert {HB} loot {table}')
    def rewrite(fname, how):
        out = []
        for l in G.FUNCS[fname]:
            m = l.find('loot give @s loot ')
            if m < 0: out.append(l); continue
            pre, table = l[:m], l[m + len('loot give @s loot '):]
            if how == 'defer':
                out.append(pre + f'function bm:p81/defer {{t:"{table}"}}')
                continue
            for a_ in ins(table):
                if pre:
                    assert pre.startswith('execute ') and pre.endswith(' run '), l
                    out.append(pre[:-len('run ')] + a_[len('execute '):])
                else:
                    out.append(a_)
        G.FUNCS[fname][:] = out
    fn('p81/defer', ['$data modify storage bm:gv pf.t set value "$(t)"', 'function bm:p75/pot_item'])
    for f_ in ('p70/r/cache/pay', 'p70/frag', 'p70/laurel', 'p75/laurel_again', 'p70/payout_inst'):
        rewrite(f_, 'defer')
    G.FUNCS['p70/r/cache/pay'] = [l.replace('three shares, and a fistful of coins.', 'three shares and a fistful of coins - into your haul.') for l in G.FUNCS['p70/r/cache/pay']]
    G.FUNCS['p70/frag'] = [l.replace('ticks in the lock\'s workings - you pocket it.', 'ticks in the lock\'s workings - it goes into your haul.') for l in G.FUNCS['p70/frag']]
    # (the weekly record - and its laurel - is settled before the haul is packed, so the laurel rides in it)
    pay = G.FUNCS['p70/payout_inst']
    rec = 'execute if score @s bm.gvmd matches 0 run function bm:p70/record'
    hl = 'execute as @a[tag=bm.gvme] at @s run function bm:p70/haul'
    assert rec in pay and hl in pay
    pay.remove(rec); pay.insert(pay.index(hl), rec)
    for f_ in [f for f in G.FUNCS if f.startswith('p81/aw/')] + ['p80/scrap']:
        rewrite(f_, 'insert')
    G.FUNCS['p70/bond'] = [l for l in G.FUNCS['p70/bond'] if 'bm.gvbond' not in l and 'summon minecraft:item' not in l] + list(ins('bm:p81/bond_sigil')) + \
        [f'execute in bm:gutter store result block {b} Items[{{components:{{"minecraft:custom_data":{{bm:"bond_sigil"}}}}}}].components."minecraft:custom_data".bond int 1 '
         'run scoreboard players get #grun bm.rng' for b in (HA, HB)]
    wjson('bm/loot_table/p81/bond_sigil.json', {'pools': [{'rolls': 1, 'entries': [G.loot_entry('bond_sigil')]}]})
    haul = G.FUNCS['p70/haul']
    for f_ in ('function bm:p80/scrap', 'function bm:p81/award'):
        haul.remove(f_); haul.insert(haul.index('function bm:p74/haul_pack'), f_)


# ====================================================================== the 3D trophies
EMBLEM = {  # 10 x 8 symbol per room, on the plinth's plaque
    'levers': ['..........', '.y..y..y..', '.y..y..y..', '..y..y..y.', '..y..y..y.', '.kkkkkkkk.', '.kkkkkkkk.', '..........'],
    'plates': ['....yy....', '....yy....', 'yyyyyyyyyy', '.y......y.', 'yyy....yyy', 'yyy....yyy', '..........', '..........'],
    'lasers': ['r.r.r.r.r.', 'r.r.r.r.r.', 'r.r.r.r.r.', 'r.r.r.r.r.', 'r.r.r.r.r.', 'r.r.r.r.r.', 'kkkkkkkkkk', '..........'],
    'tiles': ['yy.yy.yy..', 'yy.yy.yy..', '..........', 'yy.kk.yy..', 'yy.kk.yy..', '..........', 'yy.yy.yy..', 'yy.yy.yy..'],
    'dial': ['..yyyyy...', '.y.....y..', 'y...y...y.', 'y...yy..y.', 'y.......y.', '.y.....y..', '..yyyyy...', '..........'],
    'guards': ['.yyyyyyy..', '.yyyyyyy..', '.yyrryyy..', '.yyrryyy..', '..yyyyy...', '...yyy....', '....y.....', '..........'],
    'coffers': ['.yyyyyyyy.', 'y.y.y.y.y.', 'yyyyyyyyyy', 'y........y', 'y...kk...y', 'y........y', 'yyyyyyyyyy', '..........'],
    'lamps': ['.y..y..y..', 'yyyyyyyyyy', 'y.ww.ww.ww', 'y.ww.ww.ww', 'yyyyyyyyyy', '..........', '..........', '..........'],
    'lightsout': ['ww.kk.ww..', 'ww.kk.ww..', '..........', 'kk.ww.kk..', 'kk.ww.kk..', '..........', 'ww.kk.ww..', 'ww.kk.ww..'],
    'tumbler': ['...yyyy...', '..y....y..', '..y....y..', '.yyyyyyyy.', '.yyykkyyy.', '.yyyykyyy.', '.yyyyyyyy.', '..........'],
    'climb': ['....yy....', '...yyyy...', '..yyyyyy..', '..yyyyyy..', '.yyyyyyyy.', '....kk....', '..........', '..........'],
    'rafters': ['yyyyyyyyyy', '.y..y..y..', 'y.yy.yy.y.', 'yyyyyyyyyy', '...k......', '.....k....', '..k.......', '..........']}


def textures():
    from PIL import Image
    out = {}
    pal = {'y': (255, 207, 64, 255), 'k': (30, 22, 16, 255), 'r': (230, 50, 40, 255), 'w': (255, 244, 200, 255)}
    for k, rows in EMBLEM.items():
        im = Image.new('RGBA', (16, 16), (46, 34, 26, 255))
        for i in range(16):                                                       # a gold frame round a dark plaque
            for e in ((i, 0), (i, 15), (0, i), (15, i)): im.putpixel(e, (200, 150, 40, 255))
            for e in ((i, 1), (i, 14), (1, i), (14, i)): im.putpixel(e, (120, 84, 30, 255))
        for y, r in enumerate(rows):
            for x, ch in enumerate(r):
                if ch in pal: im.putpixel((3 + x, 4 + y), pal[ch])
        out[f'temb_{k}'] = im
    return out


def trophy_model(k, m):
    """a plinth with the room's plaque, and a cup that grows grander metal by metal"""
    from gen_rp import cube
    L = m
    tex = {'b': 'minecraft:block/polished_blackstone', 'm': METALS[m - 1][3], 'e': f'bm:block/temb_{k}',
           'a': {4: 'minecraft:block/emerald_block', 5: 'minecraft:block/diamond_block', 6: 'minecraft:block/shroomlight'}.get(m, METALS[m - 1][3]),
           't': 'minecraft:block/gold_block'}
    els = [cube((3, 0, 3), (13, 1.5, 13), 'b'), cube((3.5, 1.5, 3.5), (12.5, 2, 12.5), 'm' if m < 6 else 't'),
           cube((4.5, 2, 4.5), (11.5, 5.5, 11.5), 'b', faces=('east', 'west', 'up', 'down'))]
    plaque = cube((4.5, 2, 4.5), (11.5, 5.5, 11.5), 'e', faces=('north', 'south'))
    for f in ('north', 'south'): plaque['faces'][f]['uv'] = [0, 0, 16, 16]
    els.append(plaque)
    hs = 1.5 + 0.25 * L                                                            # stem
    els += [cube((7, 5.5, 7), (9, 5.5 + hs, 9), 'm'), cube((6, 5.5 + hs, 6), (10, 6.25 + hs, 10), 'm')]
    y0 = 6.25 + hs
    w = 4.6 + 0.4 * L
    hb = 3 + 0.4 * L
    a, b = 8 - w / 2, 8 + w / 2
    els += [cube((a + 0.5, y0, a + 0.5), (b - 0.5, y0 + 1, b - 0.5), 'm'), cube((a, y0 + 1, a), (b, y0 + hb, b), 'm'),
            cube((a - 0.4, y0 + hb, a - 0.4), (b + 0.4, y0 + hb + 0.6, b + 0.4), 'm' if m < 6 else 't')]
    top = y0 + hb + 0.6
    if L >= 2:                                                                     # handles
        for x1, x2, xo in ((a - 1.6, a - 0.6, a - 1.6), (b + 0.6, b + 1.6, b)):
            els += [cube((x1, y0 + 1.4, 7.4), (x2, y0 + hb - 0.4, 8.6), 'm'),
                    cube((min(xo, x1), y0 + hb - 1.2, 7.4), (max(xo + 1.6, x2), y0 + hb - 0.4, 8.6), 'm'),
                    cube((min(xo, x1), y0 + 1.4, 7.4), (max(xo + 1.6, x2), y0 + 2.2, 8.6), 'm')]
    if L >= 3:                                                                     # a finial
        els.append(cube((7.2, top, 7.2), (8.8, top + 1, 8.8), 'm' if m < 6 else 't'))
    if L >= 4:                                                                     # a gem on the bowl, front and back
        els += [cube((7, y0 + 1.6, a - 0.5), (9, y0 + hb - 1, a), 'a'), cube((7, y0 + 1.6, b), (9, y0 + hb - 1, b + 0.5), 'a')]
    if L >= 5:                                                                     # a star on top
        st = cube((7, top + 1, 7), (9, top + 3, 9), 'a')
        st['rotation'] = {'angle': 45, 'axis': 'y', 'origin': [8, top + 2, 8]}
        els.append(st)
    if L >= 6:                                                                     # a crown of spikes round the rim, an ember inside
        for x, z in ((a - 0.4, a - 0.4), (b - 0.6, a - 0.4), (a - 0.4, b - 0.6), (b - 0.6, b - 0.6), (7.5, a - 0.4), (7.5, b - 0.6), (a - 0.4, 7.5), (b - 0.6, 7.5)):
            els.append(cube((x, top, z), (x + 1, top + 1.4, z + 1), 't'))
        els.append(cube((a + 0.8, top - 0.7, a + 0.8), (b - 0.8, top - 0.1, b - 0.8), 'a'))
    return tex, els


def rp(R):
    if __import__('sys').modules[__name__] not in R.TEXTURE_MODS:
        R.TEXTURE_MODS.append(__import__('sys').modules[__name__])
    for k in TK:
        for m in range(1, NMET + 1):
            R.HATS[f'trophy3d_{k}_{m}'] = trophy_model(k, m)
    # the new sigils: the old one's face, each in its own colours and with its own mark
    g = R.grid
    face = ['................', '......yyyy......', '....yyppppyy....', '...ypppwppppy...', '..ypppppppppy...', '..ypppppppppy...', '..ypppppppppy...',
            '..ypppppppppy...', '..ypppppppppy...', '...yppppppppy...', '....yyppppyy....', '......yyyy......', '................', '................', '................', '................']
    marks = {'sigil_fury': [(6, 4), (7, 5), (8, 6), (7, 7), (8, 8), (9, 9)], 'sigil_bulwark': [(5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (5, 6), (9, 6), (6, 7), (8, 7), (7, 8)],
             'sigil_swift': [(5, 5), (6, 6), (7, 7), (6, 8), (5, 9), (8, 5), (9, 6), (10, 7), (9, 8), (8, 9)],
             'sigil_warding': [(7, 4), (6, 5), (8, 5), (5, 6), (9, 6), (5, 7), (9, 7), (6, 8), (8, 8), (7, 9)],
             'sigil_fortune': [(6, 5), (7, 5), (8, 5), (5, 6), (5, 7), (6, 7), (7, 7), (8, 7), (9, 8), (8, 9), (7, 9), (6, 9), (7, 4), (7, 10)],
             'sigil_vigor': [(6, 5), (8, 5), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6), (6, 7), (7, 7), (8, 7), (7, 8)],
             'sigil_sight': [(5, 7), (6, 6), (7, 6), (8, 6), (9, 7), (6, 8), (7, 8), (8, 8), (7, 7)]}
    for n, iid, nm, col, what, c, i in SIGILS[1:]:
        h = col.lstrip('#')
        rgb = tuple(int(h[x:x + 2], 16) for x in (0, 2, 4))
        dark = '#%02x%02x%02x' % tuple(int(v * 0.55) for v in rgb)
        im = g(face, dict(y='#c8961e', p=col, w='#ffffff'))
        for xy in marks[iid]: im.putpixel(xy, R.hexc(dark))
        R.ICONS[iid] = im

"""2.94o: THE RAID REWARD OVERHAUL - rarer finds that rise with the tier (a Tier V heist is 10-15 minutes), and three promises.

THE ODDS (per raider, per won heist; the numbers live where they're rolled - phase105, phase138, phase148, phase75):
                    I     II    III   IV    V      (was)
  rare find         6%    8%    10%   13%   16%    5% flat
  legendary         3%    4%    6%    8%    10%    3% flat
  MYTHIC            1%    2%    3%    5%    7%     1% flat     (Tier V: about one in fourteen wins - three hours)
  aura              -     -     2%    4%    6%     0.8 / 1.5 / 2.5%
  boss summon       -     -     3%    6%    10%    1 / 3 / 5%
  the tier's gear   8%    10%   12%   15%   18%    6-10%
  BM Medallion      -     -     8%    20%   35%    5 / 12 / 22%
  BM Trophy         -     -     -     -     5%     1.5%
  Gutter Coins a share at Tiers IV and V: half again (8-12, 11-15).
NO DUPLICATES       a rare, legendary or mythic find gives the one of its pair (the vault's own, or the tier's own) you haven't
                    found yet (the Codex knows); the tier's gear, a piece you haven't had from a heist yet; an aura, one
                    you don't own. Once you have them all, any.
BAD-LUCK PROTECTION every won Tier IV or V heist without a mythic counts; after 20 in a row the next one brings a mythic for
                    certain. (Any mythic - a press on its own night too - starts the count again.) The count shows at the
                    end of every Tier IV-V win.
FIRST TIER V WIN OF THE DAY a legendary at least: if the haul has no legendary or mythic, one is added.
THE ODDS IN THE LEDGER the Office's Codex has a RAID ODDS page: the table above, your mythic count, today's Tier V bonus."""
from items import T
from nbt import snbt
import phase28 as P28
import phase75 as P75
import phase80 as P80
import phase105 as P105
import phase117 as P117
import phase138 as P138
import phase148 as P148

PITY = 20
ODDS_CODE = P117.C_SEC + 5                       # (7866: the Codex's RAID ODDS button)
MYTH_COL, LEG_COL, GOLD = '#e080ff', '#ffcf40', '#ffcf40'
ROMAN = ['', 'I', 'II', 'III', 'IV', 'V']


def generate(G):
    fn, tellraw = G.fn, G.tellraw
    P = [T('[', 'dark_gray'), T('Black Market', 'dark_purple', bold=True), T('] ', 'dark_gray')]
    gear = sorted({i for pool in P105.RARE_POOL.values() for i in pool})
    objs = ['bm.mpity', 'bm.t5day', 'bm.flg'] + [f'bm.rg_{i}' for i in gear]
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    HA, HB = P148.HA, P148.HB
    ins = lambda table: [f'execute in bm:gutter unless data block {HA} Items[26] run loot insert {HA} loot {table}',
                         f'execute in bm:gutter if data block {HA} Items[26] run loot insert {HB} loot {table}']

    # ================================================================== NO DUPLICATES: a find's pair - the one you haven't found
    for kind, glob, j in (('rare', 'forgeheart', 0), ('legend', 'the_alibi', 1), ('myth', 'counterfeiters_press', 2)):
        L = G.FUNCS[f'p105/find_{kind}']
        old = 'execute store result score #fz bm.rng run random value 0..1'
        assert L[0] == old, (kind, L[0])
        L[0] = f'function bm:p218/pair/{kind}'
        fn(f'p218/pair/{kind}', [old, 'scoreboard players set #go bm.rng 0', 'scoreboard players set #to bm.rng 0',
                                 f'execute if score @s bm.cx_f_{glob} matches 1 run scoreboard players set #go bm.rng 1'] +
           [f'execute if score #gt bm.rng matches {t} if score @s bm.cx_f_{row[j][0]} matches 1 run scoreboard players set #to bm.rng 1' for t, row in P117.TIER_FINDS.items()] +
           ['execute if score #go bm.rng matches 1 if score #to bm.rng matches 0 run scoreboard players set #fz bm.rng 1',      # (1: the tier's own)
            'execute if score #go bm.rng matches 0 if score #to bm.rng matches 1 run scoreboard players set #fz bm.rng 0'])
        # (legendary or better: today's first Tier V win is satisfied; a mythic: the bad-luck count starts again)
        L.insert(0, 'scoreboard players set @s bm.flg 1')
        if kind == 'myth':
            L.insert(0, 'scoreboard players set @s bm.mpity 0')
    for k in P105.PRESSES:                       # (the mythical presses, on their own nights, are mythics too)
        L = G.FUNCS[f'p105/find_press_{k}']
        L[0:0] = ['scoreboard players set @s bm.flg 1', 'scoreboard players set @s bm.mpity 0']

    # ---- the tier's own gear: a piece you haven't had from a heist yet
    for t, pool in P105.RARE_POOL.items():
        L = G.FUNCS[f'p105/find_gear{t}']
        k = [i for i, l in enumerate(L) if f'loot bm:p105/rare_t{t}' in l]
        assert len(k) == 2, (t, L)
        L[k[0]:k[-1] + 1] = [f'function bm:p218/gear{t}']
        n = len(pool)
        lines = ['scoreboard players set #n bm.rng 0'] + [f'execute unless score @s bm.rg_{i} matches 1 run scoreboard players add #n bm.rng 1' for i in pool]
        lines += [f'execute if score #n bm.rng matches 0 store result score #pk bm.rng run random value 1..{n}',
                  f'execute if score #n bm.rng matches 0 run function bm:p218/gear{t}_any',
                  'execute if score #n bm.rng matches 0 run return 0',
                  'execute store result storage bm:tmp p218.n int 1 run scoreboard players get #n bm.rng',
                  'scoreboard players set #pk bm.rng 1', 'execute if score #n bm.rng matches 2.. run function bm:p218/roll with storage bm:tmp p218']
        for i in pool:
            lines += [f'execute unless score @s bm.rg_{i} matches 1 run scoreboard players remove #pk bm.rng 1',
                      f'execute unless score @s bm.rg_{i} matches 1 if score #pk bm.rng matches 0 run return run function bm:p218/give_gear/{i}']
        fn(f'p218/gear{t}', lines)
        fn(f'p218/gear{t}_any', [f'execute if score #pk bm.rng matches {n0 + 1} run return run function bm:p218/give_gear/{i}' for n0, i in enumerate(pool)])
    fn('p218/roll', ['$execute store result score #pk bm.rng run random value 1..$(n)'])        # (only for two or more: random value 1..1 is refused)
    for i in gear:
        fn(f'p218/give_gear/{i}', [f'scoreboard players set @s bm.rg_{i} 1'] + ins(f'bm:items/{i}'))

    # ---- an aura: one you don't own (any, once you own them all)
    order = P138.ORDER
    L = ['scoreboard players set #n bm.rng 0'] + [f'execute unless entity @s[tag=bm.auown_{w}] run scoreboard players add #n bm.rng 1' for w in order]
    L += ['execute if score #n bm.rng matches 0 run return run function bm:p218/aura_any',
          'execute store result storage bm:tmp p218.n int 1 run scoreboard players get #n bm.rng', 'scoreboard players set #pk bm.rng 1', 'execute if score #n bm.rng matches 2.. run function bm:p218/roll with storage bm:tmp p218']
    for w in order:
        L += [f'execute unless entity @s[tag=bm.auown_{w}] run scoreboard players remove #pk bm.rng 1',
              f'execute unless entity @s[tag=bm.auown_{w}] if score #pk bm.rng matches 0 run return run function bm:p138/find_{w}']
    G.FUNCS['p218/aura_any'] = list(G.FUNCS['p138/find'])
    G.FUNCS['p138/find'] = L

    # ================================================================== BAD-LUCK PROTECTION and THE FIRST TIER V WIN OF THE DAY
    # (#mythnow: a mythic this win - a find or a press; bm.flg: a legendary or better this win. Twenty dry Tier IV-V wins behind
    #  you: this one's mythic roll can't miss.)
    F = G.FUNCS['p105/finds']
    km = next(i for i, l in enumerate(F) if 'run function bm:p105/find_myth' in l)
    assert F[km - 1] == 'execute store result score #r bm.rng run random value 1..100', F[km - 1]
    F.insert(km, f'execute if score #gt bm.rng matches 4.. if score @s bm.mpity matches {PITY}.. run scoreboard players set #r bm.rng 1')
    F[0:0] = ['scoreboard players set #mythnow bm.rng 0', 'scoreboard players set @s bm.flg 0',
              'execute unless score @s bm.mpity matches 0.. run scoreboard players set @s bm.mpity 0']
    F += ['execute if score #gt bm.rng matches 4.. if score #mythnow bm.rng matches 0 run scoreboard players add @s bm.mpity 1',
          'execute if score #gt bm.rng matches 5 unless score @s bm.t5day = #day bm.bm run function bm:p218/t5first',
          'execute if score #gt bm.rng matches 4.. run function bm:p218/pity_say']
    G.FUNCS['p105/find_myth'].insert(0, 'scoreboard players set #mythnow bm.rng 1')
    for k in P105.PRESSES:
        G.FUNCS[f'p105/find_press_{k}'].insert(0, 'scoreboard players set #mythnow bm.rng 1')
    fn('p218/t5first', ['scoreboard players operation @s bm.t5day = #day bm.bm',
                        'execute if score @s bm.flg matches 1 run return run ' + tellraw('@s', P + [T('Your first Tier V win today ', GOLD, bold=True),
                                                                                                     T('- and a legendary in the haul already.', 'gray')]),
                        'function bm:p105/find_legend',
                        tellraw('@s', P + [T('Your first Tier V win today: ', GOLD, bold=True), T('a legendary find, the Fixer\'s compliments.', 'gray')])])
    fn('p218/pity_say', ['execute if score @s bm.mpity matches 0 run return 0',
                         tellraw('@s', P + [T('Mythic luck: ', MYTH_COL), {'score': {'name': '@s', 'objective': 'bm.mpity'}, 'color': 'white', 'bold': True},
                                            T(f'/{PITY}', 'gray'), T(f' Tier IV-V wins without a mythic. At {PITY}, the next one brings one for certain.', 'dark_gray')])])

    # ================================================================== RAID ODDS: a page off the Codex
    def row(name, col, vals):
        return [T('\n' + name, col, bold=True)] + [x for t in range(1, 6) for x in (T(f'   {ROMAN[t]} ', 'dark_gray'), T(vals.get(t, '-'), 'white'))]
    pct = lambda d: {t: f'{v}%' for t, v in d.items()}
    body = [T('"What a won heist puts in each raider\'s haul - Tier I to V."\n', '#d8c8a8', italic=True)]
    body += row('Rare find', '#7ad0ff', pct(P105.FIND_RARE)) + row('Legendary', LEG_COL, pct(P105.FIND_LEGEND)) + row('MYTHIC', MYTH_COL, pct(P105.FIND_MYTH))
    body += row('Aura', '#ff9ad8', {t: f'{v / 10:g}%' for t, v in P138.FIND.items()}) + row('Boss summon', '#ff7a5a', pct(P148.BOSS_CHANCE))
    body += row("Tier's gear", '#9ae8ff', pct(P105.RARE_CHANCE)) + row('BM Medallion', '#c8a0ff', {t: f'{v[0]}%' for t, v in P75.PRIZE_MED.items()})
    body += row('BM Trophy', GOLD, {t: f'{v / 10:g}%' for t, v in P75.PRIZE_TRO.items()})
    body += [T('\n\nNo duplicates: ', 'white', bold=True), T('finds, gear and auras you already have are skipped while there are others.', 'gray'),
             T(f'\nMythic luck: ', MYTH_COL, bold=True), T('$(p)', 'white', bold=True), T(f'/{PITY}', 'gray'),
             T(f' Tier IV-V wins without one - at {PITY}, the next is certain.', 'gray'),
             T('\nToday\'s first Tier V win: ', GOLD, bold=True), T('$(d)', 'white'), T(' (a legendary at least)', 'gray')]
    dlg = P28.multi([T('RAID ODDS', GOLD, bold=True), T('  ·  per raider, per won heist', 'gray')], [P28.body(body, 340)],
                    [P28.btn([T('◀ ', P117.CODEX), T('The Codex', 'white')], P117.C_CODEX, width=150)], columns=1)
    fn('p218/odds', [f'scoreboard players set @s bm.menu {P117.C_CODEX}', 'data remove storage bm:ui ro',
                     'execute unless score @s bm.mpity matches 0.. run scoreboard players set @s bm.mpity 0',
                     'execute store result storage bm:ui ro.p int 1 run scoreboard players get @s bm.mpity',
                     'data modify storage bm:ui ro.d set value "still to come"',
                     'execute if score @s bm.t5day = #day bm.bm run data modify storage bm:ui ro.d set value "claimed"',
                     'function bm:p218/odds_dlg with storage bm:ui ro'])
    fn('p218/odds_dlg', [f'$dialog show @s {P28.inline(dlg)}'])

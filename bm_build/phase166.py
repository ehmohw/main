"""2.80h: THE HEIST'S REWARDS, REWORKED - sealed crates, a prize roll, streaks, crew bonuses and the Fixer's mercy.

HAUL CRATES  carrying on used to unpack your haul one slot each: whatever isn't Tokens, coins or spoils went stack by stack
             into your locker, then your pack. Now it's SEALED in one Haul Crate per run (27 stacks to a crate), labelled
             with the heist's tier and how much is inside, and put in your locker (or your pack). Set it down and open it
             like The Haul, wherever you can place a block; it's never unpacked again on the next carry-on. (No room
             anywhere for a crate: the old way, stack by stack, as a last resort.)
THE PRIZE ROLL  after the payout your rewards come up one at a time across the screen, every second and a half: the haul
             (tier, shares, coins), the Tokens, any Medallions or BM Trophy, each bonus - and the rare, legendary and
             mythical finds last, their announcements held back until then.
WIN STREAKS  every heist you win without going home raises your streak. Each step of it (up to five) is a 40% chance of
             one more Token on the next win. A failed heist, or going home, ends it.
CREW BONUSES  a crew of two or more: one more share of the haul for each raider past the first (up to three), and a CLEAN
             CREW (nobody knocked out all heist) is a Token more for everyone.
THE FIXER'S MERCY  on your last try a skip would end the heist, so it was refused. Now the Fixer opens the way once a heist
             on the last try for part of the prize instead: half the pot so far, and a share of the haul. Asks first.
"""
import re
from items import T
from nbt import snbt, B, Int
import phase28 as P28

GOLD = '#ffcf40'
MERCY = 7736
CRATE_N = 27
STREAK_CAP, STREAK_PCT = 5, 40
CREW_CAP = 3
STEP = 6                                     # fast-loop passes (5 ticks each) between reveal steps: 1.5 s
ROMAN = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V'}
RARITY = (('r', 'rare', 'RARE FIND', '#5ab0ff'), ('l', 'legend', 'LEGENDARY FIND', '#ff9a2a'), ('m', 'myth', 'MYTHICAL FIND', '#e060ff'))
RV = ['bm.rv1', 'bm.rv2', 'bm.rv3', 'bm.rv4', 'bm.rv5', 'bm.rv6', 'bm.rv7', 'bm.rv8']   # tokens, medallions, trophy, shares, coins, streak +, clean +, crew +


def generate(G):
    fn, tellraw, title, wjson = G.fn, G.tellraw, G.title, G.wjson
    P = [T('[', 'dark_gray'), T('Heist', GOLD, bold=True), T('] ', 'dark_gray')]
    objs = ['bm.gstk', 'bm.hlt', 'bm.gvmcy', 'bm.rvs', 'bm.rvt', 'bm.rvr', 'bm.rvl', 'bm.rvm'] + RV
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    sc = lambda o, col='white': {'score': {'name': '@s', 'objective': o}, 'color': col, 'bold': True}
    haul = G.FUNCS['p70/haul']
    pay = G.FUNCS['p70/payout_inst']
    kh = next(i for i, l in enumerate(pay) if l.endswith('run function bm:p70/haul'))

    # ================================================================== CREW BONUSES and the mercy's share (as the instance, before the haul)
    pay[kh:kh] = ['scoreboard players operation #csh bm.rng = #np bm.rng', 'scoreboard players remove #csh bm.rng 1',
                  f'execute if score #csh bm.rng matches {CREW_CAP + 1}.. run scoreboard players set #csh bm.rng {CREW_CAP}',
                  'execute if score #csh bm.rng matches ..0 run scoreboard players set #csh bm.rng 0',
                  'scoreboard players operation #sh bm.rng += #csh bm.rng',
                  'scoreboard players set #ccb bm.rng 0', 'execute if score #np bm.rng matches 2.. if score @s bm.gvdc matches ..0 run scoreboard players set #ccb bm.rng 1',
                  'scoreboard players operation #mcy bm.rng = @s bm.gvmcy',
                  'execute if score #mcy bm.rng matches 1 run scoreboard players remove #sh bm.rng 1',
                  'execute if score #sh bm.rng matches ..0 run scoreboard players set #sh bm.rng 1']

    # ================================================================== WIN STREAKS (as the player, in the Fixer's prize - before the Tokens go in)
    pz = G.FUNCS['p75/prize']
    kt = next(i for i, l in enumerate(pz) if 'loot bm:p75/prize_tokens' in l)
    pz[kt:kt] = ['function bm:p166/bonus']
    fn('p166/bonus', ['scoreboard players set #stb bm.rng 0', 'scoreboard players operation #s bm.rng = @s bm.gstk',
                      f'execute if score #s bm.rng matches {STREAK_CAP + 1}.. run scoreboard players set #s bm.rng {STREAK_CAP}', 'function bm:p166/stk_roll',
                      'scoreboard players operation #ptk bm.rng += #stb bm.rng', 'scoreboard players operation #ptk bm.rng += #ccb bm.rng',
                      'execute unless score @s bm.gstk matches 99.. run scoreboard players add @s bm.gstk 1'])
    fn('p166/stk_roll', ['execute if score #s bm.rng matches ..0 run return 0', 'scoreboard players remove #s bm.rng 1',
                         'execute store result score #r bm.rng run random value 1..100', f'execute if score #r bm.rng matches ..{STREAK_PCT} run scoreboard players add #stb bm.rng 1',
                         'function bm:p166/stk_roll'])
    # (a failed heist ends it; so does going home - the coat check handing your things back)
    fl = G.FUNCS['p75/fail']
    fl.insert(next(i for i, l in enumerate(fl) if 'function bm:p75/pot_clear' in l) + 1, 'scoreboard players set @a[tag=bm.gvme] bm.gstk 0')
    G.FUNCS['p72/bag/restore2'].append('scoreboard players set @s bm.gstk 0')

    # ================================================================== THE CARD: the bonuses, after how it went
    kr = haul.index('function bm:p103/res_won')
    haul[kr + 1:kr + 1] = ['function bm:p166/res_more']
    ins = lambda txt, col, bold=False: f'$data modify storage bm:gv res.p$(pid) insert -1 value {snbt(T(txt, col, bold=bold))}'
    fn('p166/res_more', ['execute store result storage bm:gv rs.stb int 1 run scoreboard players get #stb bm.rng',
                         'execute store result storage bm:gv rs.st int 1 run scoreboard players get @s bm.gstk',
                         'execute store result storage bm:gv rs.csh int 1 run scoreboard players get #csh bm.rng',
                         'execute if score @s bm.gstk matches 2.. run function bm:p166/res/st with storage bm:gv rs',
                         'execute if score #stb bm.rng matches 1.. run function bm:p166/res/stb with storage bm:gv rs',
                         'execute if score #ccb bm.rng matches 1.. run function bm:p166/res/ccb with storage bm:gv rs',
                         'execute if score #csh bm.rng matches 1.. run function bm:p166/res/csh with storage bm:gv rs',
                         'execute if score #mcy bm.rng matches 1 run function bm:p166/res/mcy with storage bm:gv rs'])
    fn('p166/res/st', [ins(', win streak x$(st)', '#ff9a2a', True)])
    fn('p166/res/stb', [ins(' (+$(stb) Token)', '#ff9a2a')])
    fn('p166/res/ccb', [ins(', clean crew +1 Token', '#7aff7a')])
    fn('p166/res/csh', [ins(', crew +$(csh) share(s)', '#7ad0ff')])
    fn('p166/res/mcy', [ins(' (the Fixer\'s mercy took half the pot and a share)', '#ff7a7a')])

    # ================================================================== THE PRIZE ROLL
    # (the finds' announcements wait for their turn: each find remembers which it was, and says it when the roll gets there)
    say = {k: [] for k, *_r in RARITY}
    for name in sorted(G.FUNCS):
        m = re.fullmatch(r'p105/find_(rare|legend|myth)|p117/find/(rare|legend|myth)\d', name)
        if not m: continue
        kind = m.group(1) or m.group(2)
        k = next(r[0] for r in RARITY if r[1] == kind)
        L = G.FUNCS[name]
        held = [l for l in L if l.startswith(('tellraw ', 'playsound ', 'execute at @s run particle '))]
        if not held: continue
        say[k].append(held)
        n = len(say[k])
        first = L.index(held[0])
        G.FUNCS[name] = [l for l in L if l not in held]
        G.FUNCS[name].insert(first, f'scoreboard players set @s bm.rv{k} {n}')
        fn(f'p166/say/{k}{n}', held)
    assert all(say.values()), {k: len(v) for k, v in say.items()}
    for k, lines in say.items():
        fn(f'p166/say_{k}', [f'execute if score @s bm.rv{k} matches {n} run function bm:p166/say/{k}{n}' for n in range(1, len(lines) + 1)])
    # (each find on a new haul starts unremembered)
    haul[0:0] = [f'scoreboard players set @s bm.rv{k} 0' for k, *_r in RARITY]
    haul += ['scoreboard players operation @s bm.hlt = #gt bm.rng',
             'scoreboard players operation @s bm.rv1 = #rtk bm.rng', 'scoreboard players operation @s bm.rv2 = #pmd bm.rng',
             'scoreboard players operation @s bm.rv3 = #ptr bm.rng', 'scoreboard players operation @s bm.rv4 = #sh bm.rng',
             'scoreboard players operation @s bm.rv5 = #pot bm.rng', 'scoreboard players operation @s bm.rv6 = #stb bm.rng',
             'scoreboard players operation @s bm.rv7 = #ccb bm.rng', 'scoreboard players operation @s bm.rv8 = #csh bm.rng',
             'scoreboard players set @s bm.rvs 0', f'scoreboard players set @s bm.rvt {-STEP // 2}', 'tag @s add bm.rv']
    G.FUNCS['loop/fast'].append('execute as @a[tag=bm.rv] at @s run function bm:p166/rv_tick')
    fn('p166/rv_tick', ['scoreboard players add @s bm.rvt 1', f'execute if score @s bm.rvt matches ..{STEP - 1} run return 0',
                        'scoreboard players set @s bm.rvt 0', 'function bm:p166/rv/next'])
    show = lambda big, small, snd, pitch: ['title @s times 4 26 8', title('@s', 'subtitle', small), title('@s', 'title', big),
                                           f'playsound {snd} player @s ~ ~ ~ 1 {pitch}']
    steps = [
        (None, show(T('THE HAUL', GOLD, bold=True), [T('Tier ', 'gray'), sc('bm.hlt'), T(' - ', 'gray'), sc('bm.rv4'), T(' shares, ', 'gray'),
                                                       sc('bm.rv5', '#c8a050'), T(' coins in the pot', 'gray')], 'minecraft:block.chest.open', 0.8)),
        ('bm.rv1', show([T('+', GOLD), sc('bm.rv1', GOLD), T(' Tokens', GOLD, bold=True)], T('Black Market Tokens - your fee back, and more', 'gray'),
                        'minecraft:entity.experience_orb.pickup', 1.2)),
        ('bm.rv2', show([T('+', 'light_purple'), sc('bm.rv2', 'light_purple'), T(' Medallion(s)', 'light_purple', bold=True)], T('Black Market Medallions', 'gray'),
                        'minecraft:block.amethyst_block.chime', 1.0)),
        ('bm.rv3', show(T('A BM TROPHY!', '#ffb300', bold=True), T('from a Tier V vault', 'gray'), 'minecraft:ui.toast.challenge_complete', 1.4)),
        ('streak', None),
        ('bm.rv7', show(T('CLEAN CREW', '#7aff7a', bold=True), T('nobody knocked out all heist: +1 Token', 'gray'), 'minecraft:entity.player.levelup', 1.2)),
        ('bm.rv8', show([T('CREW OF ', '#7ad0ff', bold=True), {'score': {'name': '#csh1', 'objective': 'bm.rng'}, 'color': '#7ad0ff', 'bold': True}],
                        [T('+', 'gray'), sc('bm.rv8'), T(' share(s) of the haul for the company', 'gray')], 'minecraft:entity.villager.celebrate', 1.1)),
    ] + [(f'bm.rv{k}', show(T(head, col, bold=True), T('...in your haul', 'gray'), 'minecraft:block.note_block.bell', 0.7 + 0.25 * i) + [f'function bm:p166/say_{k}'])
         for i, (k, _kind, head, col) in enumerate(RARITY)]
    nx = ['scoreboard players add @s bm.rvs 1']
    for i, (cond, body) in enumerate(steps, 1):
        nx.append(f'execute if score @s bm.rvs matches {i} run return run function bm:p166/rv/s{i}')
        if cond == 'streak':
            fn(f'p166/rv/s{i}', ['execute unless score @s bm.gstk matches 2.. run return run function bm:p166/rv/next',
                                 'execute if score @s bm.rv6 matches 1.. run return run function bm:p166/rv/stk_win', 'function bm:p166/rv/stk_try'])
            fn('p166/rv/stk_win', show([T('WIN STREAK x', '#ff9a2a', bold=True), sc('bm.gstk', '#ff9a2a')], [T('+', 'gray'), sc('bm.rv6'), T(' Token(s) for not going home', 'gray')],
                                       'minecraft:entity.firework_rocket.twinkle', 1.0))
            fn('p166/rv/stk_try', show([T('WIN STREAK x', '#ff9a2a', bold=True), sc('bm.gstk', '#ff9a2a')], T('no extra Token this time - the odds grow each win', 'gray'),
                                       'minecraft:entity.firework_rocket.launch', 1.0))
            continue
        pre = [] if cond is None else [f'execute unless score @s {cond} matches 1.. run return run function bm:p166/rv/next']
        if cond == 'bm.rv8':
            pre += ['scoreboard players operation #csh1 bm.rng = @s bm.rv8', 'scoreboard players add #csh1 bm.rng 1']
        fn(f'p166/rv/s{i}', pre + body)
    fn('p166/rv/next', nx + ['function bm:p166/rv/done'])
    fn('p166/rv/done', ['tag @s remove bm.rv', 'scoreboard players set @s bm.rvs 0'] + [f'scoreboard players set @s bm.rv{k} 0' for k, *_r in RARITY])

    # ================================================================== HAUL CRATES (carrying on: what's left sealed, one crate a run)
    up = G.FUNCS['p102/unpack']
    up[up.index('function bm:p102/place')] = 'function bm:p166/seal'
    crate = {'id': 'minecraft:barrel', 'count': Int(1), 'Slot': B(0), 'components': {
        'minecraft:custom_name': T('Haul Crate', GOLD, bold=True), 'minecraft:custom_data': {'bm_haul': B(2)}, 'minecraft:enchantment_glint_override': True,
        'minecraft:lore': [T('Sealed by the Fixer when you carried on.', 'gray')]}}
    fn('p166/seal', ['data modify storage bm:up fb set value []', 'scoreboard players set #ucl bm.rng 0', 'scoreboard players set #ucp bm.rng 0',
                     'data modify storage bm:up lab set value {t:"?"}'] +
       [f'execute if score @s bm.hlt matches {t} run data modify storage bm:up lab.t set value "{r}"' for t, r in ROMAN.items()] +
       ['function bm:p166/seal_one', 'data modify storage bm:up rest set from storage bm:up fb', 'function bm:p102/place',
        'execute if score #ucl bm.rng matches 1.. run ' + tellraw('@s', [T('  Sealed in ', 'gray'), {'score': {'name': '#ucl', 'objective': 'bm.rng'}, 'color': 'white', 'bold': True},
                                                                       T(' Haul Crate(s), into your locker', GOLD)]),
        'execute if score #ucp bm.rng matches 1.. run ' + tellraw('@s', [T('  Sealed in ', 'gray'), {'score': {'name': '#ucp', 'objective': 'bm.rng'}, 'color': 'white', 'bold': True},
                                                                       T(' Haul Crate(s), into your pack', GOLD)])])
    fn('p166/seal_one', ['execute unless data storage bm:up rest[0] run return 0',
                         'data modify storage bm:up ch set value []', 'data modify storage bm:up raw set value []', 'scoreboard players set #ci bm.rng 0',
                         'function bm:p166/take',
                         f'execute in bm:gutter run data modify block -200 64 -200 Items set value [{snbt(crate)}]',
                         'execute in bm:gutter run data modify block -200 64 -200 Items[0].components."minecraft:container" set from storage bm:up ch',
                         'execute store result storage bm:up lab.n int 1 run scoreboard players get #ci bm.rng',
                         'function bm:p166/seal_lore with storage bm:up lab',
                         'execute store result score #ok bm.rng run function bm:p102/lk/put',
                         'execute if score #ok bm.rng matches 1 run scoreboard players add #ucl bm.rng 1',
                         'execute if score #ok bm.rng matches 0 store result score #ok bm.rng run function bm:p102/pk/put',
                         'execute if score #ok bm.rng matches 1 unless score #ucl bm.rng matches 1.. run scoreboard players add #ucp bm.rng 1',
                         'execute if score #ok bm.rng matches 0 run data modify storage bm:up fb append from storage bm:up raw[]',
                         'execute in bm:gutter run data modify block -200 64 -200 Items set value []',
                         'function bm:p166/seal_one'])
    fn('p166/take', [f'execute if score #ci bm.rng matches {CRATE_N}.. run return 0', 'execute unless data storage bm:up rest[0] run return 0',
                     'data modify storage bm:up e set value {}', 'execute store result storage bm:up e.slot int 1 run scoreboard players get #ci bm.rng',
                     'data modify storage bm:up e.item set from storage bm:up rest[0]', 'data modify storage bm:up ch append from storage bm:up e',
                     'data modify storage bm:up raw append from storage bm:up rest[0]', 'data remove storage bm:up rest[0]',
                     'scoreboard players add #ci bm.rng 1', 'function bm:p166/take'])
    lore = lambda txt, col: f'$execute in bm:gutter run data modify block -200 64 -200 Items[0].components."minecraft:lore" append value {snbt(T(txt, col))}'
    fn('p166/seal_lore', [lore('A Tier $(t) haul: $(n) stack(s) inside.', GOLD), lore('Set it down and open it, like The Haul.', 'blue')[1:],
                          lore('Walk away and what\'s left folds up into your pack.', 'gray')[1:]])
    # (set down, it's a Haul: found by the same placing advancement, minded by the same marker; broken by hand, no barrel drops)
    wjson('bm/advancement/p74/haul_placed.json', {'criteria': {
        p: {'trigger': 'minecraft:placed_block', 'conditions': {'location': [
            {'condition': 'minecraft:match_tool', 'predicate': {'items': 'minecraft:barrel', 'predicates': {'minecraft:custom_data': f'{{bm_haul:{b}b}}'}}}]}}
        for p, b in (('p', 1), ('q', 2))}, 'requirements': [['p', 'q']], 'rewards': {'function': 'bm:p74/haul/placed'}})
    G.FUNCS['p74/haul/broke'].insert(0, 'kill @e[type=minecraft:item,distance=..1.5,nbt={Item:{id:"minecraft:barrel",components:{"minecraft:custom_name":{text:"Haul Crate"}}}}]')

    # ================================================================== THE FIXER'S MERCY (the last try: one skip a heist, for part of the prize)
    G.FUNCS['p70/inst_init'].append('scoreboard players set @s bm.gvmcy 0')
    ask = G.FUNCS['p122/ask']
    k = next(i for i, l in enumerate(ask) if l.startswith('execute if score #lv bm.rng matches ..1 run return run '))
    ask[k] = 'execute if score #lv bm.rng matches ..1 run return run function bm:p166/m_ask'
    sayf = lambda txt, col='gray': tellraw('@s', P + [T(txt, col)])
    inst = 'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run '
    fn('p166/m_state', ['scoreboard players set #mu bm.rng 1', 'scoreboard players set #mp bm.rng 0',
                        inst + 'scoreboard players operation #mu bm.rng = @s bm.gvmcy', inst + 'scoreboard players operation #mp bm.rng = @s bm.gvpot'])
    dlg = P28.multi([T('The Fixer\'s mercy', '#ff9a7a', bold=True)],
                    [P28.body([T('Your last try - a skip would end the heist. ', 'gray'), T('The Fixer will open the way once', 'white', bold=True),
                               T(', and take part of the prize instead of a try:', 'gray')]),
                     P28.body([T('Half the pot', '#c8a050', bold=True), T(' ($(half) of $(pot) coins so far) ', 'gray'), T('and a share', '#c8a050', bold=True),
                               T(' of the haul. No flawless trophy.', 'gray')]),
                     P28.body([T('Once a heist. The crew keeps its last try.', 'dark_gray')])],
                    [P28.btn([T('Pay the Fixer  ', '#ff9a7a', bold=True), T('(half the pot, a share)', 'gray')], MERCY, width=240),
                     P28.btn([T('Keep at it', 'white')], None, width=240)], columns=1, exit_label='Back')
    dlg['actions'][1]['action'] = {'type': 'minecraft:run_command', 'command': f'/trigger bm.act set {P28.NOOP}'}
    fn('p166/m_dlg', [f'$dialog show @s {P28.inline(dlg)}'])
    fn('p166/m_ask', ['function bm:p166/m_state',
                      'execute if score #mu bm.rng matches 1 run return run ' + sayf('Your last try, and the Fixer\'s mercy is spent for this heist - solve it, or it\'s over.', 'red'),
                      'execute store result storage bm:ui mc.pot int 1 run scoreboard players get #mp bm.rng',
                      'scoreboard players operation #mp bm.rng /= #2 bm.rng', 'execute store result storage bm:ui mc.half int 1 run scoreboard players get #mp bm.rng',
                      'function bm:p166/m_dlg with storage bm:ui mc'])
    fn('p166/m_yes', ['execute unless entity @s[tag=bm.gvp] run return 0', 'function bm:p122/find',
                      'execute if score #sk bm.rng matches 0 run return run ' + sayf('No unsolved puzzle here to skip.'),
                      'function bm:p122/tries',
                      'execute if score #lv bm.rng matches 2.. run return run ' + sayf('You have tries to spare - an ordinary skip costs one of those.'),
                      'function bm:p166/m_state',
                      'execute if score #mu bm.rng matches 1 run return run ' + sayf('The Fixer\'s mercy is spent for this heist.', 'red'),
                      'tag @s add bm.skwho', inst + 'function bm:p166/m_pay',
                      'execute as @e[type=minecraft:marker,tag=bm.skroom,limit=1] at @s run function bm:p122/open',
                      'tag @s remove bm.skwho', 'tag @e[type=minecraft:marker,tag=bm.skroom] remove bm.skroom'])
    fn('p166/m_pay', ['scoreboard players set @s bm.gvmcy 1', 'scoreboard players operation @s bm.gvpot /= #2 bm.rng', 'function bm:p70/bar', 'function bm:p70/tag_mine',
                      tellraw('@a[tag=bm.gvme]', P + [{'selector': '@a[tag=bm.skwho]', 'color': 'white'}, T(' called in the Fixer\'s mercy - ', 'gray'),
                                                      T('half the pot and a share of the haul', '#ff9a7a', bold=True), T(' for the way on. Still one try left.', 'gray')]),
                      'tag @a[tag=bm.gvme] remove bm.gvme'])
    act = G.FUNCS['p28/act']                 # (after the click is read - phase126 put the read first; above it, the line would see the last click)
    act.insert(act.index('scoreboard players set @s bm.act 0') + 1, f'execute if score #act bm.pay matches {MERCY} run return run function bm:p166/m_yes')

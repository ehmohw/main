"""2.67: THE RAID CREW, AND THE VAULT'S OWN RULES.

THE RAID CREW (the Fixer's Ledger -> Raid Crew): your followers' own summoning items stay at the coat check now - the
  ledger is how your crew comes into the vault. Every follower you've signed a Raid Contract for, the Frog with Mustache
  and Donado once their contract is filed, and every hireling you've hired are listed there, each ON or OFF. On a heist
  the ones that are ON come along by themselves (and back again after a faint, once they've recovered); turn one OFF
  and it goes home. Hirelings: one at a time, as before. A party raids light - ONE FOLLOWER EACH when two or more of you
  go in, TWO when you raid alone (a hireling doesn't count). Leave the heist, any way at all, and the raid crew goes home.
  (A hireling's or vault hire's contract, used once, is filed in the ledger - it's not needed after.)
THE KIT IS ON LOAN: loaned armour is bound to you until the heist is over (Curse of Binding); loaned weapons and the rest
  of the kit bounce straight back into your hands if dropped, and are pulled out of lockers, your ender chest, bundles,
  boxes and The Haul. Only the paperweights and food can be put down.
THE LOCKER HALL: an unclaimed bay is locked - claim it first.
VAULT GEMS: the gems Goldtooth sells are the vault's - they stay in it. They're taken at the door on the way out, can't be
  set down as decorations, and handed to Cecil or KillerWatt they come back as vault gems; leave the vault and the
  element they gave him fades.
"""
from items import T, ITEMS
from nbt import snbt, B
import re
import phase28 as P28
import phase72 as P72
import phase60 as P60

GOLD = '#ffcf40'
CREW = '#9ad0ff'
# (key, name, colour, host, tag, select tag, cooldown, try (as you), dismiss (as you, select tag on him), recall, goes away (as him))
CALLED = [('cecil', 'Cecil', '#b48cff', 'wolf', 'bm.cecilpet', 'bm.cpsel', 'bm.cpcd', 'p46/pet/try_summon', 'p46/pet/dismiss', 'p46/pet/recall', 'p62/cecil_go'),
          ('emma', 'Emma', '#ff8ad8', 'cat', 'bm.emmapet', 'bm.emsel2', 'bm.emcd', 'p57/try_summon', 'p57/dismiss', 'p57/recall', 'p62/emma_go'),
          ('celi', 'Celi', '#bfe8ff', 'wolf', 'bm.celipet', 'bm.cesel2', 'bm.cecd', 'p66/try_summon', 'p66/dismiss', 'p66/recall', 'p66/go'),
          ('zib', 'Zib', '#7ad87a', 'wolf', 'bm.zibpet', 'bm.zbsel', 'bm.zbcd', 'p72/zb/try_summon', 'p72/zb/dismiss', 'p72/zb/recall', 'p72/zb/beamup'),
          ('killerwatt', 'KillerWatt', '#ffe040', 'wolf', 'bm.kxpet', 'bm.kxsel2', 'bm.kxcd', 'p79/pet/try', 'p79/pet/home', 'p79/pet/recall', 'p79/pet/vanish'),
          ('leo', 'Leo', '#5ab8e0', 'wolf', 'bm.leopet', 'bm.lesel2', 'bm.lecd', 'p96/try_summon', 'p96/dismiss', 'p96/recall', 'p96/go'),
          ('demo', 'Democratus', '#7ad06a', 'wolf', 'bm.dmpet', 'bm.dmsel2', 'bm.dmcd', 'p97/try_summon', 'p97/dismiss', 'p97/recall', 'p97/go'),
          ('escort', 'Skiff Escort', '#c8c8ff', 'bat', 'bm.eskhost', None, 'bm.eskcd', None, None, None, None)]
HIRED = [('frog', 'The Frog with Mustache', '#6ac850', 'bm.frogpet', 'bm.fvcf'), ('donado', 'Donado', '#e8d29a', 'bm.donado', 'bm.fvcn')]
USES = ['p46/pet/use', 'p57/use', 'p66/use', 'p72/zb/use', 'p79/spark', 'p96/use', 'p97/use'] + [f'p72/esk/use_{i}' for i in range(len(P72.ART.ESCORT_COLS))]
ITEMS_OUT = ['cecil_gem', 'emma_ribbon', 'celi_charm', 'donadian_medal', 'kw_spark', 'leo_crest', 'demo_seal'] + [f'skiff_escort_{c}' for c in P72.ART.ESCORT_COLS]
P72.KEEP[:] = [k for k in P72.KEEP if k not in ITEMS_OUT]        # (the coat check keeps them now)
CODE = 7900                       # (the ledger's: followers 7900+, vault hires 7920+, hirelings 7930+; the page itself 7807)
VAULT = '#e8b8ff'


def generate(G):
    import phase77 as P77
    import phase80 as P80
    import phase89 as P89
    import phase84 as P84
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    tick, fast, second = [], [], []
    objs = ['bm.crew', 'bm.crewoff', 'bm.eskl']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    P = PREFIX
    BIT = P89.BIT
    init = ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
            'execute unless score @s bm.fcon matches 0.. run scoreboard players set @s bm.fcon 0', 'execute unless score @s bm.crew matches 0.. run scoreboard players set @s bm.crew 0',
            'execute unless score @s bm.crewoff matches 0.. run scoreboard players set @s bm.crewoff 0']
    fn('p98/init', init)
    def bit(obj, b):
        return [f'scoreboard players operation #q bm.rng = @s {obj}', f'scoreboard players set #bit bm.rng {b}',
                'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng']
    OFF = {k: 2 ** i for i, (k, *_r) in enumerate(CALLED)}
    OFF.update({k: 2 ** (12 + j) for j, (k, *_r) in enumerate(HIRED)})
    FILED = {k: 2 ** j for j, (k, *_r) in enumerate(HIRED)}
    FILED.update({i: 2 ** (1 + i) for i in P77.HIRE})
    in_heist = 'execute if entity @s[tag=bm.gvp] if dimension bm:gutter'

    # ================================================================== who's yours, who's on, who's here (as you, #me set)
    def mine(host, tag, extra=''):
        return f'@e[type=minecraft:{host},tag={tag}{extra}]'
    for k, nm, col, host, tag, sel, cd, try_, dis, rec, go in CALLED:
        fn(f'p98/signed/{k}', bit('bm.fcon', BIT[k]) + ['return run scoreboard players get #q bm.rng'])
        fn(f'p98/on/{k}', [f'execute unless function bm:p98/signed/{k} run return 0'] + bit('bm.crewoff', OFF[k]) +
           ['execute if score #q bm.rng matches 1 run return 0', 'return 1'])
        fn(f'p98/has/{k}', [f'execute as {mine(host, tag)} if score @s bm.pid = #me bm.pid run return 1', 'return 0'])
    for k, nm, col, tag, cd in HIRED:
        fn(f'p98/filed/{k}', bit('bm.crew', FILED[k]) + ['return run scoreboard players get #q bm.rng'])
        fn(f'p98/on/{k}', [f'execute unless function bm:p98/filed/{k} run return 0'] + bit('bm.crewoff', OFF[k]) +
           ['execute if score #q bm.rng matches 1 run return 0', 'return 1'])
        fn(f'p98/has/{k}', [f'execute as {mine("wolf", tag, ",tag=bm.fvault")} if score @s bm.pid = #me bm.pid run return 1', 'return 0'])
    for i in P77.HIRE:
        fn(f'p98/filed/h{i}', bit('bm.crew', FILED[i]) + ['return run scoreboard players get #q bm.rng'])
    # room for one more? one follower each in a party, two alone (hirelings aside)
    count = ['scoreboard players set #fc bm.rng 0'] + \
        [f'execute as {mine(host, tag)} if score @s bm.pid = #me bm.pid run scoreboard players add #fc bm.rng 1' for k, nm, col, host, tag, *_r in CALLED] + \
        [f'execute as {mine("wolf", tag, ",tag=bm.fvault")} if score @s bm.pid = #me bm.pid run scoreboard players add #fc bm.rng 1' for k, nm, col, tag, cd in HIRED] + \
        ['scoreboard players set #np bm.rng 0', 'scoreboard players operation #mi bm.rng = @s bm.gvi',
         'execute as @a[tag=bm.gvp] if score @s bm.gvi = #mi bm.rng run scoreboard players add #np bm.rng 1',
         'scoreboard players set #lim bm.rng 1', 'execute if score #np bm.rng matches ..1 run scoreboard players set #lim bm.rng 2']
    fn('p98/count', count)
    fn('p98/room', ['function bm:p98/count', 'execute if score #fc bm.rng < #lim bm.rng run return 1', 'return 0'])
    full = say('Your crew is full - one follower each in a party, two when you raid alone. (Turn one OFF in the ledger.)', '#ff9a5a')

    # ---- calling one in (as you, on a heist); sending one home
    for k, nm, col, host, tag, sel, cd, try_, dis, rec, go in CALLED:
        if k == 'escort':
            fn('p98/call/escort', ['execute if function bm:p98/has/escort run return 0', 'execute unless function bm:p98/room run return run ' + full,
                                   'execute unless score @s bm.eskl matches 0.. run scoreboard players set @s bm.eskl 0',
                                   'scoreboard players operation #ec bm.rng = @s bm.eskl', 'function bm:p72/esk/use'])
            fn('p98/home/escort', ['function bm:p72/esk/send_home'])
            continue
        fn(f'p98/call/{k}', [f'execute as {mine(host, tag)} if score @s bm.pid = #me bm.pid run tag @s add {sel}',
                             f'execute if entity @e[tag={sel}] run function bm:{rec}', f'execute if entity @e[tag={sel}] run return run tag @e[tag={sel}] remove {sel}',
                             'execute unless function bm:p98/room run return run ' + full, f'function bm:{try_}'])
        fn(f'p98/home/{k}', [f'execute as {mine(host, tag)} if score @s bm.pid = #me bm.pid run tag @s add {sel}',
                             f'execute if entity @e[tag={sel}] run function bm:{dis}', f'tag @e[tag={sel}] remove {sel}'])
    for k, nm, col, tag, cd in HIRED:
        fn(f'p98/call/{k}', [f'execute if function bm:p98/has/{k} run return 0', 'execute unless function bm:p98/room run return run ' + full,
                             f'execute if score @s {cd} matches 1.. run return run ' + say(f'{nm} is still recovering.', col), f'function bm:p89/fv/summon_{k}',
                             tellraw('@s', P + [T(nm, col, bold=True), T(' signs on for the heist - in the vault\'s own kit.', 'gray')])])
        fn(f'p98/home/{k}', [f'execute as {mine("wolf", tag, ",tag=bm.fvault")} if score @s bm.pid = #me bm.pid at @s run function bm:p89/fv/dismiss'])

    # ---- every second, on a heist: whoever's ON and not here (and recovered) comes; a crew over the limit sends one home
    second.append('execute in bm:gutter as @a[tag=bm.gvp,tag=!bm.gvdead,distance=0..] at @s run function bm:p98/roster')
    roster = ['function bm:p98/init', 'function bm:p98/count', 'execute if score #fc bm.rng > #lim bm.rng run function bm:p98/bench']
    # (called only once they've been missing a full second: a faint is noticed and its cooldown set first, so a follower who
    #  just fell isn't called straight back)
    for k, cd in [(v[0], v[6]) for v in CALLED] + [(v[0], v[4]) for v in HIRED]:
        roster += [f'execute if entity @s[tag=bm.crw_{k}] if function bm:p98/has/{k} run tag @s remove bm.crw_{k}',
                   f'execute if entity @s[tag=bm.crw_{k}] if function bm:p98/on/{k} unless score @s {cd} matches 1.. unless function bm:p98/has/{k} if function bm:p98/room run function bm:p98/call/{k}',
                   f'execute if function bm:p98/on/{k} unless score @s {cd} matches 1.. unless function bm:p98/has/{k} run tag @s add bm.crw_{k}']
    fn('p98/roster', roster)
    # (a "missing" mark that never got its call - the crew was full - is cleared going in and coming out, so the next
    #  heist starts the queue fresh: top of the list first)
    crw_clear = [f'tag @s remove bm.crw_{k}' for k in [v[0] for v in CALLED] + [v[0] for v in HIRED]]
    fn('p98/crw_clear', crw_clear)
    for f_ in [f for f in G.FUNCS if re.fullmatch(r'p70/s\d+/enter', f)]:
        G.FUNCS[f_].append('function bm:p98/crw_clear')
    order = [k for k, *_r in HIRED[::-1]] + [k for k, *_r in CALLED[::-1]]
    fn('p98/bench', [f'execute if function bm:p98/has/{k} run return run function bm:p98/bench_{k}' for k in order])
    for k in order:
        nm = next(v[1] for v in CALLED + HIRED if v[0] == k)
        fn(f'p98/bench_{k}', [f'function bm:p98/home/{k}', tellraw('@s', P + [T('A party raids light - one follower each. ', CREW), T(f'{nm} heads home.', 'gray')])])

    # ---- leaving the heist (every way out passes p70/unraid): the raid crew goes home, there and then
    leave = ['function bm:p98/init']
    for k, nm, col, host, tag, sel, cd, try_, dis, rec, go in CALLED:
        if k == 'escort': leave.append('function bm:p72/esk/vanish'); continue
        leave.append(f'execute as {mine(host, tag)} if score @s bm.pid = #me bm.pid at @s run function bm:{go}')
    leave += [f'function bm:p98/home/{k}' for k, *_r in HIRED] + ['function bm:p77/hire/dismiss', 'function bm:p98/crw_clear']
    fn('p98/leave', leave)
    G.FUNCS['p70/unraid'][0:0] = ['function bm:p98/leave']

    # ---- in the vault the summoning items don't call anyone (the ledger does); followers there don't need theirs on you
    for f_ in USES:
        G.FUNCS[f_].insert(0, f'{in_heist} run return run ' + say('In the vault your crew answers the Fixer\'s Ledger - Raid Crew.', CREW))
    for k_ in ('cecil', 'emma', 'celi', 'zib', 'kw', 'leo', 'demo'):
        L = G.FUNCS[f'p73/fol/{k_}']
        j = next(i for i, l in enumerate(L) if ' if items entity ' in l)
        L.insert(j, 'execute if entity @a[tag=bm.fown,tag=bm.gvp] run return run scoreboard players set @s bm.fmis 0')
    L = G.FUNCS['p73/fol/esk']
    j = next(i for i, l in enumerate(L) if ' if items entity ' in l)
    L.insert(j, 'execute if entity @a[tag=bm.fown,tag=bm.gvp] run return run scoreboard players set @s bm.fmis 0')
    for i in range(len(P72.ART.ESCORT_COLS)):          # (the ledger launches the colour you flew last)
        G.FUNCS[f'p72/esk/use_{i}'].insert(1, f'scoreboard players set @s bm.eskl {i}')

    # ---- contracts: a hireling's (or a vault hire's), used once, is filed in the ledger
    for i, (hk, hnm, rat, hcol, *_r) in P77.HIRE.items():
        fn(f'p98/file_h{i}', ['function bm:p98/init'] + bit('bm.crew', FILED[i]) + ['execute if score #q bm.rng matches 1 run return 0',
                              f'scoreboard players add @s bm.crew {FILED[i]}', f'clear @s *[minecraft:custom_data~{{bm:"contract_{hk}"}}] 1',
                              'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.8',
                              tellraw('@s', P + [T(hnm, hcol, bold=True), T(' is filed in your ', 'gray'), T("Fixer's Ledger", GOLD),
                                                 T(' - Raid Crew: switch them on or off there.', 'gray')])])
        L = G.FUNCS[f'p77/hire/use{i}']
        j = next(n for n, l in enumerate(L) if l.startswith('scoreboard players set @s bm.gvhc'))
        L.insert(j + 1, f'function bm:p98/file_h{i}')
    for k, nm, col, tag, cd in HIRED:
        fn(f'p98/file_{k}', ['function bm:p98/init'] + bit('bm.crew', FILED[k]) + ['execute if score #q bm.rng matches 1 run return 0',
                             f'scoreboard players add @s bm.crew {FILED[k]}', f'clear @s *[minecraft:custom_data~{{bm:"fcontract_{k}"}}] 1',
                             'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.8',
                             tellraw('@s', P + [T(nm, col, bold=True), T(' is filed in your ', 'gray'), T("Fixer's Ledger", GOLD),
                                                T(' - Raid Crew: on a heist he signs on by himself (switch him off there).', 'gray')]),
                             'return 1'])
        L = G.FUNCS[f'p89/call/{k}']
        j = next(n for n, l in enumerate(L) if l.startswith('scoreboard players set @s bm.gvhc'))
        L.insert(j + 1, f'execute if function bm:p98/file_{k} run return 0')
    for k in BIT:
        if f'p89/sign/{k}' in G.FUNCS:
            G.FUNCS[f'p89/sign/{k}'].append(tellraw('@s', [T('  (Switch them on or off in your Fixer\'s Ledger - Raid Crew.)', 'dark_gray')]))

    # ---- (2.67) Celi, Leo and Democratus count toward the three-follower limit too (they slipped past it)
    G.FUNCS['p58/count'][-1:-1] = [f'execute as @e[type=minecraft:wolf,tag={t}] on owner if entity @s[tag=bm.fcme] run scoreboard players add #fc bm.rng 1'
                                   for t in ('bm.celipet', 'bm.leopet', 'bm.dmpet')]
    for f_ in ('p66/try_summon', 'p96/try_summon', 'p97/try_summon'):
        G.FUNCS[f_].insert(0, 'execute if function bm:p58/full run return 0')

    # ================================================================== the ledger's page
    MC = P80.MENU_CODE
    page = ['function bm:p98/init', f'scoreboard players set @s bm.menu {MC + 7}', 'data remove storage bm:ui crew']
    st = lambda key, txt, col: f'data modify storage bm:ui crew.r_{key} set value {snbt(T(txt, col, bold=True))}'
    for k, nm, col, host, tag, sel, cd, *_r in CALLED:
        page += [st(k, 'no contract', 'dark_gray'), f'execute if function bm:p98/on/{k} run {st(k, "ON", "#7aff7a")}',
                 f'execute if function bm:p98/signed/{k} unless function bm:p98/on/{k} run {st(k, "OFF", "#ff7a7a")}']
    for k, nm, col, tag, cd in HIRED:
        page += [st(k, 'no contract', 'dark_gray'), f'execute if function bm:p98/on/{k} run {st(k, "ON", "#7aff7a")}',
                 f'execute if function bm:p98/filed/{k} unless function bm:p98/on/{k} run {st(k, "OFF", "#ff7a7a")}']
    for i in P77.HIRE:
        page += [st(f'h{i}', 'not hired', 'dark_gray'), f'execute if function bm:p98/filed/h{i} run {st(f"h{i}", "OFF", "#ff7a7a")}',
                 f'execute if function bm:p98/filed/h{i} if score @s bm.gvhr matches {i} run {st(f"h{i}", "ON", "#7aff7a")}']
    page.append('function bm:p98/page_dlg with storage bm:ui crew')
    fn('p98/crew', page)
    btns = [P28.btn([T(nm, col, bold=True), T('  '), f'@@RAW:r_{k}@@'], CODE + i, width=180) for i, (k, nm, col, *_r) in enumerate(CALLED)] + \
           [P28.btn([T(nm if k != 'frog' else 'The Frog', col, bold=True), T('  '), f'@@RAW:r_{k}@@'], CODE + 20 + j, width=180) for j, (k, nm, col, *_r) in enumerate(HIRED)] + \
           [P28.btn([T(hnm, hcol, bold=True), T('  '), f'@@RAW:r_h{i}@@'], CODE + 30 + i, width=180) for i, (hk, hnm, rat, hcol, *_r) in P77.HIRE.items()] + \
           [P28.btn([T('« The Office', 'gray')], MC, width=180)]
    dlg = P28.multi([T('RAID CREW', CREW, bold=True), T('  ·  who comes into the vault with you', 'gray')],
                    [P28.body([T('Click to switch on or off. On a heist, everyone switched ', 'gray'), T('ON', '#7aff7a', bold=True),
                               T(' comes along by themselves - ', 'gray'), T('one follower each in a party, two when you raid alone', 'white'),
                               T('. Hirelings: one at a time. Summoning items stay at the coat check; leave the heist and the crew goes home.', 'gray')], 360),
                     P28.body([T('Followers sign on with a Raid Contract; hirelings and vault hires with theirs (used once, filed here). Goldtooth sells them all.',
                                 'dark_gray', italic=True)], 360)],
                    btns, columns=2, exit_label='Close')
    fn('p98/page_dlg', [f'$dialog show @s {P28.inline(dlg)}'])
    # (the clicks)
    for i, (k, nm, col, host, tag, sel, cd, *_r) in enumerate(CALLED):
        fn(f'p98/t/{k}', ['function bm:p98/init', f'execute unless function bm:p98/signed/{k} run return run ' +
                          say(f'No contract for {nm} yet - Goldtooth sells Raid Contracts in the den.', col)] + bit('bm.crewoff', OFF[k]) +
           [f'execute if score #q bm.rng matches 0 run return run function bm:p98/t/{k}_off', f'function bm:p98/t/{k}_on'])
        fn(f'p98/t/{k}_off', [f'scoreboard players add @s bm.crewoff {OFF[k]}', f'{in_heist} run function bm:p98/home/{k}',
                              say(f'{nm}: OFF - stays home on heists.', col), 'function bm:p98/crew'])
        fn(f'p98/t/{k}_on', [f'scoreboard players remove @s bm.crewoff {OFF[k]}', f'{in_heist} unless score @s {cd} matches 1.. run function bm:p98/call/{k}',
                             say(f'{nm}: ON - comes along on heists.', col), 'function bm:p98/crew'])
    for j, (k, nm, col, tag, cd) in enumerate(HIRED):
        fn(f'p98/t/{k}', ['function bm:p98/init', f'execute unless function bm:p98/filed/{k} run return run ' +
                          say(f'No contract for {nm} filed - Goldtooth sells them; use it once.', col)] + bit('bm.crewoff', OFF[k]) +
           [f'execute if score #q bm.rng matches 0 run return run function bm:p98/t/{k}_off', f'function bm:p98/t/{k}_on'])
        fn(f'p98/t/{k}_off', [f'scoreboard players add @s bm.crewoff {OFF[k]}', f'{in_heist} run function bm:p98/home/{k}',
                              say(f'{nm}: OFF - stays home on heists.', col), 'function bm:p98/crew'])
        fn(f'p98/t/{k}_on', [f'scoreboard players remove @s bm.crewoff {OFF[k]}', f'{in_heist} run function bm:p98/call/{k}',
                             say(f'{nm}: ON - signs on for every heist.', col), 'function bm:p98/crew'])
    for i, (hk, hnm, rat, hcol, *_r) in P77.HIRE.items():
        fn(f'p98/t/h{i}', ['function bm:p98/init', f'execute unless function bm:p98/filed/h{i} run return run ' +
                           say(f'{hnm} isn\'t hired - Goldtooth sells the contract; use it once.', hcol),
                           f'execute if score @s bm.gvhr matches {i} run return run function bm:p98/t/h{i}_off', f'function bm:p98/t/h{i}_on'])
        fn(f'p98/t/h{i}_off', ['scoreboard players set @s bm.gvhr 0', 'function bm:p77/hire/dismiss', say(f'{hnm}: OFF - off duty.', hcol), 'function bm:p98/crew'])
        fn(f'p98/t/h{i}_on', [f'scoreboard players set @s bm.gvhr {i}', 'function bm:p77/hire/dismiss', 'scoreboard players set @s bm.gvhd 0',
                              f'{in_heist} run function bm:p77/hire/summon{i}', say(f'{hnm}: ON - meets you on every heist.', hcol), 'function bm:p98/crew'])
    act = G.FUNCS['p80/act']
    act += [f'execute if score #act bm.pay matches {MC + 7} run return run function bm:p98/crew'] + \
        [f'execute if score #act bm.pay matches {CODE + i} run return run function bm:p98/t/{k}' for i, (k, *_r) in enumerate(CALLED)] + \
        [f'execute if score #act bm.pay matches {CODE + 20 + j} run return run function bm:p98/t/{k}' for j, (k, *_r) in enumerate(HIRED)] + \
        [f'execute if score #act bm.pay matches {CODE + 30 + i} run return run function bm:p98/t/h{i}' for i in P77.HIRE]

    # ================================================================== THE KIT IS ON LOAN
    kit = '*[minecraft:custom_data~{bm_kit:1b}]'
    kit_nbt = '{components:{"minecraft:custom_data":{bm_kit:1b}}}'
    vlt_nbt = '{components:{"minecraft:custom_data":{bm_vault:1b}}}'
    # dropped (Q): straight back to whoever threw it - unless it's a paperweight or food
    fast.append(f'execute in bm:gutter as @e[type=minecraft:item,distance=0..] if items entity @s contents {kit} '
                'unless items entity @s contents *[minecraft:custom_data~{bm:"paperweight"}] unless items entity @s contents *[minecraft:food] run function bm:p98/kit/bounce')
    fn('p98/kit/bounce', ['execute on origin run tag @s[type=minecraft:player] add bm.kthr', 'execute unless entity @a[tag=bm.kthr] run return 0',
                          'tp @s @a[tag=bm.kthr,limit=1]', 'data modify entity @s PickupDelay set value 0s', 'data modify entity @s Owner set from entity @a[tag=bm.kthr,limit=1] UUID',
                          'execute as @a[tag=bm.kthr] run ' + say('The kit is on loan - it stays with you. (Only paperweights and food can be put down.)', GOLD),
                          'tag @a[tag=bm.kthr] remove bm.kthr'])
    # put away somewhere: lockers (while someone's in the hall), your ender chest - back into your hands
    fn('p98/kit/back', ['execute unless data storage bm:tmp kout[0] run return 0', 'data modify storage bm:tmp k1 set from storage bm:tmp kout[0]', 'data remove storage bm:tmp kout[0]',
                        'data remove storage bm:tmp k1.Slot', 'summon minecraft:item ~ ~0.3 ~ {Item:{id:"minecraft:stone",count:1},PickupDelay:0s,Tags:["bm.knew"]}',
                        'data modify entity @e[type=minecraft:item,tag=bm.knew,limit=1,sort=nearest] Item set from storage bm:tmp k1',
                        'data modify entity @e[type=minecraft:item,tag=bm.knew,limit=1,sort=nearest] Owner set from entity @s UUID',
                        'tag @e[type=minecraft:item,tag=bm.knew] remove bm.knew', 'function bm:p98/kit/back'])
    cells = [(cx, cy, cz) for n, cs, _p in P84.bays() for cx, cy, cz, _s in cs]
    second.append(f'execute in bm:gutter positioned {P84.HX} 60 {P84.HZ} if entity @a[dx=15,dy=12,dz=15] run function bm:p98/kit/lockers')
    fn('p98/kit/lockers', [f'execute if data block {x} {y} {z} Items[{kit_nbt}] positioned {x} {y} {z} run function bm:p98/kit/cell' for x, y, z in cells])
    fn('p98/kit/cell', ['data modify storage bm:tmp kout set value []', f'data modify storage bm:tmp kout append from block ~ ~ ~ Items[{kit_nbt}]',
                        f'data remove block ~ ~ ~ Items[{kit_nbt}]',
                        'execute as @p[distance=..16] at @s run function bm:p98/kit/back',
                        'execute as @p[distance=..16] run ' + say('Loaned kit can\'t go in a locker - it\'s back in your hands.', GOLD)])
    second.append(f'execute in bm:gutter as @a[tag=bm.gvp,distance=0..] if items entity @s enderchest.* {kit} at @s run function bm:p98/kit/ender')
    fn('p98/kit/ender', ['data modify storage bm:tmp kout set value []', f'data modify storage bm:tmp kout append from entity @s EnderItems[{kit_nbt}]'] +
       [f'execute if items entity @s enderchest.{n} {kit} run item replace entity @s enderchest.{n} with minecraft:air' for n in range(27)] +
       ['function bm:p98/kit/back', say('Loaned kit can\'t go in your ender chest - it\'s back in your hands.', GOLD)])
    # the way out: nothing of the kit's (or the vault's) leaves inside anything you carry - a bundle, a box, The Haul
    vault = '*[minecraft:custom_data~{bm_vault:1b}]'
    strip = []
    for tagn in (kit_nbt, vlt_nbt):
        strip += [f'$data remove storage bm:gv cb.p$(pid)[{tagn}]',
                  f'$data remove storage bm:gv cb.p$(pid)[].components."minecraft:bundle_contents"[{tagn}]',
                  f'$data remove storage bm:gv cb.p$(pid)[].components."minecraft:container"[{{item:{tagn}}}]']
    L = G.FUNCS['p72/bag/restore2']
    j = max(n for n, l in enumerate(L) if 'cb.p$(pid) append from' in l)
    L[j + 1:j + 1] = strip
    G.FUNCS['p70/unraid'][0:0] = [f'clear @s {vault}'] + \
        [f'execute if items entity @s enderchest.{n} {kit} run item replace entity @s enderchest.{n} with minecraft:air' for n in range(27)] + \
        [f'execute if items entity @s enderchest.{n} {vault} run item replace entity @s enderchest.{n} with minecraft:air' for n in range(27)]
    second.append(f'clear @a[tag=!bm.gvp,tag=!bm.gvdead] {vault}')
    # (a Haul set down in the vault and folded back up: no kit in it)
    G.FUNCS['p74/haul/fold'].insert(1, f'data remove storage bm:tmp haul.in[{kit_nbt}]')

    # ================================================================== THE LOCKER HALL: unclaimed bays are locked (phase84 sets the lock)
    # ================================================================== VAULT GEMS
    gems = list(P60.KEYS)
    for g in gems:
        wjson(f'bm/loot_table/items/vgem_{g}.json', {'pools': [{'rolls': 1, 'entries': [G.loot_entry(f'gem_{g}', None, (
            {'function': 'minecraft:set_custom_data', 'tag': '{bm_vault:1b}'},
            {'function': 'minecraft:set_lore', 'mode': 'append', 'lore': [T("Bought in the vault - it stays in the vault.", VAULT, italic=True)]}))]}]})
        G.FUNCS[f'p60/deco/try_{g}'].insert(0, f'execute if items entity @s weapon.* *[minecraft:custom_data~{{bm:"gem_{g}",bm_vault:1b}}] run return run ' +
                                            say('A vault gem can\'t be set down - it belongs to the vault.', VAULT))
    # Cecil (bm.cpel) and KillerWatt (bm.kxel) remember whether the gem in them is the vault's (bm.vgc / bm.vgk)
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.vgc dummy', 'scoreboard objectives add bm.vgk dummy']
    G.OBJECTIVES += ['bm.vgc', 'bm.vgk']
    ETH_C = len(gems) + 1
    for who, el_obj, flag, back in (('cecil', 'bm.cpel', 'bm.vgc', 'p69/give_back'), ('kw', 'bm.kxel', 'bm.vgk', 'p79/el/give_back')):
        L = G.FUNCS[back]
        for n, l in enumerate(L):
            for g in gems:
                if l.endswith(f'loot give @s loot bm:items/gem_{g}'):
                    L[n] = l.replace(' run loot give', f' unless score @s {flag} matches 1 run loot give')
                    L.insert(n + 1, l.replace(' run loot give', f' if score @s {flag} matches 1 run loot give').replace(f'bm:items/gem_{g}', f'bm:items/vgem_{g}'))
                    break
        L.append(f'scoreboard players set @s {flag} 0')
        mark = (f'execute store success score @s {flag} if items entity @s weapon.mainhand *[minecraft:custom_data~{{bm_vault:1b}}]')
        if who == 'cecil':
            for g in gems:
                F_ = G.FUNCS[f'p46/el/{g}']
                j = next(n for n, l in enumerate(F_) if l == 'function bm:p69/give_back')
                F_.insert(j + 1, mark)
        else:
            F_ = G.FUNCS['p79/el/set']
            j = next(n for n, l in enumerate(F_) if l == 'function bm:p79/el/give_back')
            F_.insert(j + 1, mark)
    fn('p98/vgem_out', ['execute if score @s bm.vgc matches 1 run scoreboard players set @s bm.cpel 0',
                        'execute if score @s bm.vgc matches 1 run ' + tellraw('@s', P + [T('The vault\'s gem stays in the vault - ', VAULT), T('Cecil\'s robes are his own again.', 'gray')]),
                        'scoreboard players set @s bm.vgc 0',
                        'execute if score @s bm.vgk matches 1 run scoreboard players set @s bm.kxel 0',
                        'execute if score @s bm.vgk matches 1 run ' + tellraw('@s', P + [T('The vault\'s gem stays in the vault - ', VAULT), T('KillerWatt\'s lightning is his own again.', 'gray')]),
                        'scoreboard players set @s bm.vgk 0'])
    G.FUNCS['p70/unraid'].insert(0, 'function bm:p98/vgem_out')

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second

"""3.0i: THE PARTNER WHEEL'S TEAMS, SORTING AND SIT-ALL; SENDING FROM THE RAT BANK; THE HEIST HAUL; BAGS THAT SAY WHAT'S IN THEM.

TEAMS        the wheel's Teams page (3505): three line-ups, Team 1-3 (fixed names - a dialog's text input can only hand a number
             to /trigger, so a typed name can't reach the pack; each team's members are listed under its name instead).
             "Save the followers out now as Team N" keeps who's out; "Call Team N" sends home anyone out who isn't in it and
             calls the rest, each their own way (their item's try - its three-follower limit, the Keeper's fourth). A member
             whose item is neither on the wheel nor on you is skipped, with a word. Kept per player (storage bm:pw p<pid>.t<N>).
SHOW / SORT  two switches on the wheel (kept on you: tags bm.pwfo, bm.pwaz): Show All / Out now (only those out with you), and
             Sort Met order / A-Z. Met order is the order you met them (each bm:met/<kind> advancement stamps bm.pwmo<i> with
             your own count, bm.pwmc); anyone met before 3.0i has no stamp and comes first, in the wheel's own order.
SIT / STAND ALL  one button, shown while any follower is out: if any of yours out is standing, all sit; if all sit, all stand.
             Each one by their own sit toggle (the function their menu's Sit button runs, found in the build - their line, their
             seated pose; KillerWatt's runs as him); the six with only a click toggle (Emma, Celi, Zib, Cecil, Leo, Democratus) have
             their Sitting set as that click sets it, Leo's and Democratus's settling flourish too. One riding or being ridden is
             left as they are.
THE BANK     Send to a player (the account page, 4093): pick someone online (a button per player, code 10000000 + their pid),
             a currency (every one the bank keeps, Royal Pearls too), an amount (1, 10, 64, all, or typed: the dialog's text box
             hands it to /trigger bm.bsam), then confirm. Never to yourself, never more than you have; both of you are told.
             (block 5300-5399, menu 5300)
THE HAUL     every heist's end (won or lost - p70/unraid, before the coat check hands your pack back): one dialog of everything you
             came out with that you didn't go in with (by item: Tokens, coins, gems, gear...) and what went into your Rat Bank,
             each with its worth in Tokens and the total. Worth: the Scrap Bin's buy-back (phase51's refund table - half what a
             trader sells it for, Old Barnaby's buy-backs for found gear), currencies at the Fence's ladder (a Medallion 5 Tokens,
             a Trophy 20, a Lucky Token 5, a Blood Crystal 1, a Dread Token 100) and the gutter's own coins at the Gutter Bank's
             rate (32 Gutter Coins a Token). Anything nobody buys is listed without a price.
BAG PREVIEW  every bag (phase248.BAGS) writes what it holds into its lore whenever it folds (and the Vacuum Satchel whenever it
             picks something up): "Contains: N stacks", the first six ("- 32x Cobblestone") and "...and 4 more". Its own lore
             (the item's lines) is kept as it is; only the lines after it are rewritten.
"""
import json
import os
import re

from items import T, ITEMS
from nbt import snbt, Int, B
import phase31 as P31

PURPLE = '#b48cff'
GOLD = '#ffcf40'

# ----------------------------------------------------------------------------------------- codes
TEAMS, SITALL, SHOW, SORT, BACK = 3505, 3506, 3507, 3508, 3509      # (3505-3599: p259/w/act; menus 3350 the wheel, 3505 its Teams page)
CALL_T, SAVE_T = 3510, 3520                                           # (+1..+3)
TMENU = 3505
NT = 3

BS_ACCT = 4093                                                        # (the bank's account page - its router, P31.ACCT_EXTRA)
BS_MENU = 5300                                                        # (5300-5399: p259/bs/act)
BS_WHO, BS_ACC, BS_CUR, BS_PRE, BS_CURBACK, BS_SEND, BS_AMTBACK = 5301, 5302, 5310, 5331, 5335, 5340, 5341
BS_PID = 10000000                                                     # (a recipient's button: 10000000 + their pid)
P31.ACCT_EXTRA.append(([T('Send to a player', '#7ad8ff')], BS_ACCT,
                       T('Send some of your account to someone online - into their account', 'gray'), 'p259/bs/who'))


def _pw():
    """the wheel's partners in its own order (phase179's PW): (key, name, colour, host, tag, try, home, item)"""
    import phase125 as P125
    import phase179 as P179
    out = []
    for w in list(P179.SLOTS) + [w for w in P125.WHO if w not in P179.SLOTS]:
        nm, pron, col, host, tag, try_, home = P125.WHO[w]
        e = P179.FOLLOW.get(tag.split(',')[0])
        iid = e[3] if e else ('wilfrey_locket' if w == 'wil' else None)
        out.append((w, nm, col, host, tag, try_, home, iid))
    return out


cap = lambda s: s[0].upper() + s[1:]
holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'


# ========================================================================================= the wheel
SIT_MANUAL = {'don': ('p136/dn/sit', 'bm.dnsel'), 'frog': ('p136/fg/sit', 'bm.fgsel'), 'wil': ('p2/wil/sit', 'bm.fsel')}
SIT_AS_HOST = {'kw': 'p125/kw/sit'}
SIT_PLAIN = {'emma': None, 'celi': None, 'zib': None, 'cecil': None, 'leo': 'p96/sat', 'demo': 'p97/sat'}
_SIT_RX = [re.compile(r'^execute store (?:success|result) score #s0? bm\.rng (?:if data|run data get) entity '
                      r'@e\[(?:type=minecraft:\w+,)?tag=([\w.]+)(?:,limit=1)?(?:,sort=nearest)?\] ?(?:\{Sitting:1b\}|Sitting)$'),
           re.compile(r'^execute as @e\[(?:type=minecraft:\w+,)?tag=([\w.]+)\] store success score #s0? bm\.rng if data entity @s \{Sitting:1b\}$')]


def _sit_toggles(G, PW):
    """each follower's own sit toggle, run as you with their host tagged: {key: (function, tag)}"""
    found = {}
    for name, L in G.FUNCS.items():
        if not name.endswith('/sit') or not L: continue
        for rx in _SIT_RX:
            m = rx.match(L[0])
            if not m: continue
            mm = re.match(r'^bm\.(\w+?)(?:sel2|sel|clk)$', m.group(1))
            if mm:
                found.setdefault(f'bm.{mm.group(1)}pet', (name, m.group(1)))
    out = {}
    for w, nm, col, host, tag, *_r in PW:
        if w in SIT_MANUAL:
            out[w] = SIT_MANUAL[w]
        elif tag.split(',')[0] in found:
            out[w] = found[tag.split(',')[0]]
    for w, (f, t) in SIT_MANUAL.items():
        assert f in G.FUNCS and t in ' '.join(G.FUNCS[f]), (w, f, t)
    for w, f in SIT_AS_HOST.items():
        assert G.FUNCS[f][0].startswith('execute store success score #s bm.rng if data entity @s {Sitting:1b}'), f
    for f in SIT_PLAIN.values():
        assert f is None or f in G.FUNCS, f
    missing = [w for w, *_r in PW if w not in out and w not in SIT_AS_HOST and w not in SIT_PLAIN]
    assert not missing, f'3.0i Sit all: no sit toggle found for {missing}'
    return out


def wheel(G):
    """after phase179 (the wheel) and phase220 (its gallery button)"""
    import phase28 as P28
    import phase179 as P179
    import phase220 as P220
    fn, title, tellraw = G.fn, G.title, G.tellraw
    PRE = [T('[', 'dark_gray'), T('Black Market', 'dark_purple', bold=True), T('] ', 'dark_gray')]
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    PW = _pw()
    N = len(PW)
    W = P179.WMENU
    for i in range(N):
        assert f'p179/w/row{i}' in G.FUNCS, i
    objs = [f'bm.pwmo{i}' for i in range(N)] + ['bm.pwmc']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    mine = lambda host, tag: f'@e[type=minecraft:{host},tag={tag}]'

    # ---------------------------------------------------------------- who's out (#pwo<i>), as you
    fn('p259/w/outs', ['scoreboard players operation #me bm.pid = @s bm.pid'] +
       [l for i, (w, nm, col, host, tag, *_r) in enumerate(PW) for l in
        (f'scoreboard players set #pwo{i} bm.rng 0',
         f'execute as {mine(host, tag)} if score @s bm.pid = #me bm.pid run scoreboard players set #pwo{i} bm.rng 1')])

    # ---------------------------------------------------------------- met order: a stamp when you meet them
    for i, (w, *_r) in enumerate(PW):
        key = P220.MET_KEY.get(w, w)
        p = G.path('data', 'bm', 'advancement', 'met', f'{key}.json')
        adv = json.load(open(p))
        adv['rewards'] = {'function': f'bm:p259/met/{i}'}
        json.dump(adv, open(p, 'w'), indent=1, ensure_ascii=False)
        fn(f'p259/met/{i}', [f'execute if score @s bm.pwmo{i} matches 1.. run return 0', 'scoreboard players add @s bm.pwmc 1',
                             f'scoreboard players operation @s bm.pwmo{i} = @s bm.pwmc'])

    # ---------------------------------------------------------------- the rows: filtered, sorted
    op = G.FUNCS['p179/w/open']
    rows = [f'execute if score @s bm.pw{i} matches 1 run function bm:p179/w/row{i}' for i in range(N)]
    k = op.index(rows[0])
    assert op[k:k + N] == rows, 'the wheel\'s rows moved'
    op[k:k + N] = ['function bm:p259/w/rows']
    for i in range(N):                                   # (Show: Out now - a row only for one out with you)
        R = G.FUNCS[f'p179/w/row{i}']
        j = next(n for n, l in enumerate(R) if 'run scoreboard players set #pwon bm.rng 1' in l)
        R.insert(j + 1, 'execute if entity @s[tag=bm.pwfo] if score #pwon bm.rng matches 0 run return 0')
    skey = lambda e: re.sub(r'^the ', '', e[1].lower())
    az = sorted(range(N), key=lambda i: (skey(PW[i]), i))
    nobody = P28.btn([T('Nobody\'s out right now - ', 'gray'), T('show everyone', 'white')], SHOW, width=150,
                     tooltip=T('Show: All', 'gray'))
    fn('p259/w/rows', ['execute if entity @s[tag=bm.pwaz] run function bm:p259/w/rows_az',
                       'execute unless entity @s[tag=bm.pwaz] run function bm:p259/w/rows_met',
                       'execute unless entity @s[tag=bm.pwfo] run return 0',
                       'execute if data storage bm:tmp pw.acts[0] run return 0',
                       'scoreboard players set #pwany bm.rng 0'] +
       [f'execute if score @s bm.pw{i} matches 1 run scoreboard players set #pwany bm.rng 1' for i in range(N)] +
       [f'execute if score #pwany bm.rng matches 1 run data modify storage bm:tmp pw.acts append value {snbt(nobody)}'])
    fn('p259/w/rows_az', [f'execute if score @s bm.pw{i} matches 1 run function bm:p179/w/row{i}' for i in az])
    # (met order: a selection, lowest stamp first - unstamped (0) first, in the wheel's order: a strict < keeps the earlier)
    fn('p259/w/rows_met', [l for i in range(N) for l in
                           (f'scoreboard players set #pwd{i} bm.rng 0',
                            f'execute if score @s bm.pw{i} matches 1 unless score @s bm.pwmo{i} matches 1.. run scoreboard players set @s bm.pwmo{i} 0')] +
       ['function bm:p259/w/pick'])
    fn('p259/w/pick', ['scoreboard players set #pwbv bm.rng 2147483647', 'scoreboard players set #pwbi bm.rng -1'] +
       [f'execute if score #pwd{i} bm.rng matches 0 if score @s bm.pw{i} matches 1 if score @s bm.pwmo{i} < #pwbv bm.rng run function bm:p259/w/best{i}'
        for i in range(N)] +
       ['execute if score #pwbi bm.rng matches ..-1 run return 0',
        'execute store result storage bm:tmp pwp.i int 1 run scoreboard players get #pwbi bm.rng',
        'function bm:p259/w/emit with storage bm:tmp pwp', 'function bm:p259/w/pick'])
    for i in range(N):
        fn(f'p259/w/best{i}', [f'scoreboard players operation #pwbv bm.rng = @s bm.pwmo{i}', f'scoreboard players set #pwbi bm.rng {i}'])
    fn('p259/w/emit', ['$scoreboard players set #pwd$(i) bm.rng 1', '$function bm:p179/w/row$(i)'])

    # ---------------------------------------------------------------- the buttons, last on the wheel's page
    def sw(lbl, on_txt, code, tip):
        return P28.btn([T(lbl, 'gray'), T(on_txt, 'white', bold=True)], code, width=150, tooltip=T(tip, 'gray'))
    b_teams = P28.btn([T('\u2691 ', PURPLE), T('Teams', 'white')], TEAMS, width=150,
                      tooltip=T('Three line-ups of yours: save who\'s out now, and call a whole team with one button', 'gray'))
    b_all = sw('Show: ', 'All', SHOW, 'Every partner on your wheel (press: only those out with you now)')
    b_out = sw('Show: ', 'Out now', SHOW, 'Only the partners out with you now (press: all of them)')
    b_met = sw('Sort: ', 'Met order', SORT, 'In the order you met them (press: A-Z)')
    b_az = sw('Sort: ', 'A-Z', SORT, 'By name, A to Z (press: the order you met them)')
    b_sit = P28.btn([T('\u2b07 ', '#9ad8ff'), T('Sit all', 'white')], SITALL, width=150,
                    tooltip=T('Every follower of yours out sits down (one is standing)', 'gray'))
    b_stand = P28.btn([T('\u2b06 ', '#9ad8ff'), T('Stand all', 'white')], SITALL, width=150,
                      tooltip=T('Every follower of yours out stands up (they\'re all sitting)', 'gray'))
    add = lambda b: f'data modify storage bm:tmp pw.acts append value {snbt(b)}'
    k = op.index('function bm:p179/w/show with storage bm:tmp pw')
    op[k:k] = [add(b_teams),
               'execute unless entity @s[tag=bm.pwfo] run ' + add(b_all), 'execute if entity @s[tag=bm.pwfo] run ' + add(b_out),
               'execute unless entity @s[tag=bm.pwaz] run ' + add(b_met), 'execute if entity @s[tag=bm.pwaz] run ' + add(b_az),
               'function bm:p259/s/scan',
               'execute if score #pwso bm.rng matches 1 if score #pwst bm.rng matches 1 run ' + add(b_sit),
               'execute if score #pwso bm.rng matches 1 if score #pwst bm.rng matches 0 run ' + add(b_stand)]

    # ---------------------------------------------------------------- SIT / STAND ALL
    tog = _sit_toggles(G, PW)
    busy = ['execute if function bm:p20/frog/has_vehicle run return 1',
            'execute on passengers if entity @s[type=minecraft:player] run return 1', 'return 0']
    assert 'p20/frog/has_vehicle' in G.FUNCS
    fn('p259/s/busy', busy)
    # (#pwso: any of yours out; #pwst: one of them standing - as you)
    fn('p259/s/scan', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #pwso bm.rng 0', 'scoreboard players set #pwst bm.rng 0'] +
       [f'execute as {m} if score @s bm.pid = #me bm.pid unless function bm:p259/s/busy run function bm:p259/s/seen'
        for m in dict.fromkeys(mine(host, tag) for w, nm, col, host, tag, *_r in PW)])
    fn('p259/s/seen', ['scoreboard players set #pwso bm.rng 1', 'execute unless data entity @s {Sitting:1b} run scoreboard players set #pwst bm.rng 1'])
    sa = ['function bm:p259/s/scan', 'execute if score #pwso bm.rng matches 0 run return run ' + say('None of your followers are out.'),
          'scoreboard players operation #pwsit bm.rng = #pwst bm.rng', 'scoreboard players set #pwsn bm.rng 0', 'tag @s add bm.pwme']
    for i, (w, nm, col, host, tag, *_r) in enumerate(PW):
        sa.append(f'execute as {mine(host, tag)} if score @s bm.pid = #me bm.pid unless function bm:p259/s/busy at @s run function bm:p259/s/h{i}')
        L = ['execute store success score #pwis bm.rng if data entity @s {Sitting:1b}',
             'execute if score #pwis bm.rng = #pwsit bm.rng run return 0', 'scoreboard players add #pwsn bm.rng 1']
        if w in tog:
            f, t = tog[w]
            L += [f'tag @s add {t}', f'execute as @a[tag=bm.pwme,limit=1] at @s run function bm:{f}', f'tag @s remove {t}']
        elif w in SIT_AS_HOST:
            L += [f'function bm:{SIT_AS_HOST[w]}']
        else:
            L += ['execute if score #pwsit bm.rng matches 1 run data modify entity @s Sitting set value 1b',
                  'execute if score #pwsit bm.rng matches 0 run data modify entity @s Sitting set value 0b']
            if SIT_PLAIN[w]:
                L.append(f'execute if score #pwsit bm.rng matches 1 run function bm:{SIT_PLAIN[w]}')
        fn(f'p259/s/h{i}', L)
    sa += ['tag @s remove bm.pwme', 'playsound minecraft:entity.wolf.ambient player @s ~ ~ ~ 0.4 1.4',
           'execute if score #pwsit bm.rng matches 1 run ' + say('Everyone sits down.', PURPLE),
           'execute if score #pwsit bm.rng matches 0 run ' + say('Everyone\'s up - let\'s go.', PURPLE),
           'function bm:p179/w/open']
    fn('p259/s/all', sa)

    # ---------------------------------------------------------------- TEAMS
    tp = P28.multi([T('Teams', PURPLE, bold=True), T('  \u00b7  Partner Wheel', 'gray')],
                   [P28.body([T('Save the followers out with you now as a team - then call the whole team with one button: anyone out who '
                                'isn\'t in it goes home, the rest come.', 'gray')], 300)] +
                   [P28.body([T(f'Team {t}: ', GOLD, bold=True), f'@@RAW:r_t{t}@@'], 300) for t in range(1, NT + 1)],
                   [b for t in range(1, NT + 1) for b in
                    (P28.btn([T('\u27a4 ', GOLD), T(f'Call Team {t}', 'white', bold=True)], CALL_T + t, width=150,
                             tooltip=T(f'Team {t} comes - anyone out who isn\'t in it goes home', 'gray')),
                     P28.btn(T(f'Save who\'s out as Team {t}', 'gray'), SAVE_T + t, width=150,
                             tooltip=T(f'The followers out with you right now become Team {t}', 'gray')))] +
                   [P28.btn(T('\u00ab Partner Wheel', 'gray'), BACK, width=150)], columns=2)
    fn('p259/t/show', ['$dialog show @s ' + P28.inline(tp)])
    none = T('(not saved yet)', 'dark_gray', italic=True)
    fn('p259/t/page', [f'scoreboard players set @s bm.menu {TMENU}', 'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                       'data remove storage bm:tmp pwt', 'execute store result storage bm:tmp pwt.pid int 1 run scoreboard players get @s bm.pid',
                       'function bm:p259/t/page2 with storage bm:tmp pwt', 'function bm:p259/t/show with storage bm:tmp pwt',
                       'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 0.8 1.3'])
    fn('p259/t/page2', [l for t in range(1, NT + 1) for l in
                        (f'data modify storage bm:tmp pwt.r_t{t} set value {snbt(none)}',
                         f'$execute if data storage bm:pw p$(pid).n{t} run data modify storage bm:tmp pwt.r_t{t} set from storage bm:pw p$(pid).n{t}')])
    # save: who's out now
    sv = ['$data remove storage bm:pw p$(pid).t$(t)', '$data remove storage bm:pw p$(pid).n$(t)',
          '$data modify storage bm:pw p$(pid).n$(t) set value {text:"",color:"white",italic:false}', 'scoreboard players set #pwtn bm.rng 0']
    for i, (w, nm, col, *_r) in enumerate(PW):
        sv += [f'$execute if score #pwo{i} bm.rng matches 1 run data modify storage bm:pw p$(pid).t$(t) append value {{i:{i}}}',
               f'$execute if score #pwo{i} bm.rng matches 1 if score #pwtn bm.rng matches 1.. run data modify storage bm:pw p$(pid).n$(t).extra append value {snbt(T(", ", "gray"))}',
               f'$execute if score #pwo{i} bm.rng matches 1 run data modify storage bm:pw p$(pid).n$(t).extra append value {snbt(T(cap(nm), col))}',
               f'execute if score #pwo{i} bm.rng matches 1 run scoreboard players add #pwtn bm.rng 1']
    sv += ['$execute if score #pwtn bm.rng matches 0 run data remove storage bm:pw p$(pid).n$(t)']
    fn('p259/t/save_m', sv)
    for t in range(1, NT + 1):
        fn(f'p259/t/save{t}', ['function bm:p259/w/outs', 'scoreboard players set #pwtn bm.rng 0', 'data remove storage bm:tmp pwt',
                               'execute store result storage bm:tmp pwt.pid int 1 run scoreboard players get @s bm.pid', f'data modify storage bm:tmp pwt.t set value {t}',
                               'function bm:p259/t/save_m with storage bm:tmp pwt',
                               'execute if score #pwtn bm.rng matches 0 run ' + say(f'None of your followers are out - Team {t} is empty now.'),
                               'execute if score #pwtn bm.rng matches 1.. run playsound minecraft:block.note_block.chime player @s ~ ~ ~ 0.6 1.5',
                               'execute if score #pwtn bm.rng matches 1.. run ' + tellraw('@s', PRE + [T(f'Team {t} saved: ', GOLD, bold=True),
                                                                                                        {'score': {'name': '#pwtn', 'objective': 'bm.rng'}, 'color': 'white'},
                                                                                                        T(' of them.', 'gray')]),
                               'function bm:p259/t/page'])
    # call: who's in it (#pwin<i>), home the rest, call them
    fn('p259/t/in_m', [l for i in range(N) for l in
                       (f'scoreboard players set #pwin{i} bm.rng 0',
                        f'$execute if data storage bm:pw p$(pid).t$(t)[{{i:{i}}}] run scoreboard players set #pwin{i} bm.rng 1')])
    for t in range(1, NT + 1):
        fn(f'p259/t/call{t}', ['data remove storage bm:tmp pwt', 'execute store result storage bm:tmp pwt.pid int 1 run scoreboard players get @s bm.pid',
                               f'data modify storage bm:tmp pwt.t set value {t}',
                               'function bm:p259/t/in_m with storage bm:tmp pwt',
                               'function bm:p259/t/go'])
    go = ['function bm:p259/w/outs', 'scoreboard players set #pwtn bm.rng 0'] + \
         [f'execute if score #pwin{i} bm.rng matches 1 run scoreboard players add #pwtn bm.rng 1' for i in range(N)] + \
         ['execute if score #pwtn bm.rng matches 0 run return run ' + say('That team is empty - save the followers out with you as it first.'),
          'scoreboard players set #pwth bm.rng 0', 'scoreboard players set #pwtc bm.rng 0']
    for i, (w, nm, col, host, tag, try_, home, iid) in enumerate(PW):
        go.append(f'execute if score #pwo{i} bm.rng matches 1 if score #pwin{i} bm.rng matches 0 run function bm:p259/t/h{i}')
        fn(f'p259/t/h{i}', ['scoreboard players add #pwth bm.rng 1', f'function bm:{home}'])
    for i, (w, nm, col, host, tag, try_, home, iid) in enumerate(PW):
        go.append(f'execute if score #pwin{i} bm.rng matches 1 if score #pwo{i} bm.rng matches 0 run function bm:p259/t/c{i}')
        Hh = holds(iid)
        fn(f'p259/t/c{i}', [f'execute unless score @s bm.pw{i} matches 1 unless items entity @s container.* {Hh} unless items entity @s weapon.offhand {Hh} run return run ' +
                            tellraw('@s', PRE + [T(cap(nm), col), T(f' stays put - {ITEMS[iid]["name"]} isn\'t on your wheel or on you.', 'gray')]),
                            'scoreboard players add #pwtc bm.rng 1', 'scoreboard players set @s bm.gvhc 0', 'scoreboard players operation #me bm.pid = @s bm.pid',
                            f'function bm:{try_}'])
    go += ['playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.7 1.6', 'particle minecraft:enchant ~ ~1.2 ~ 0.4 0.5 0.4 0.8 30',
           ]
    fn('p259/t/go', go)
    for t in range(1, NT + 1):
        G.FUNCS[f'p259/t/call{t}'].append('execute if score #pwtn bm.rng matches 1.. run ' +
                                           title('@s', 'actionbar', [T(f'Team {t}', GOLD, bold=True), T(' - the wheel turns.', PURPLE)]))

    # ---------------------------------------------------------------- the router
    act = [f'execute if score #act bm.pay matches {BACK} if score @s bm.menu matches {TMENU} run return run function bm:p179/w/open',
           f'execute unless score @s bm.menu matches {W} unless score @s bm.menu matches {TMENU} run return run function bm:p28/stale',
           f'execute if score #act bm.pay matches {TEAMS} run return run function bm:p259/t/page',
           f'execute unless score @s bm.menu matches {W} run return run function bm:p259/w/act_t',
           f'execute if score #act bm.pay matches {SITALL} run return run function bm:p259/s/all',
           f'execute if score #act bm.pay matches {SHOW} if entity @s[tag=bm.pwfo] run return run function bm:p259/w/fo_off',
           f'execute if score #act bm.pay matches {SHOW} run return run function bm:p259/w/fo_on',
           f'execute if score #act bm.pay matches {SORT} if entity @s[tag=bm.pwaz] run return run function bm:p259/w/az_off',
           f'execute if score #act bm.pay matches {SORT} run return run function bm:p259/w/az_on',
           'function bm:p28/stale']
    fn('p259/w/act', act)
    fn('p259/w/act_t', [f'execute if score #act bm.pay matches {CALL_T + t} run return run function bm:p259/t/call{t}' for t in range(1, NT + 1)] +
       [f'execute if score #act bm.pay matches {SAVE_T + t} run return run function bm:p259/t/save{t}' for t in range(1, NT + 1)] +
       ['function bm:p28/stale'])
    click = 'playsound minecraft:ui.button.click player @s ~ ~ ~ 0.5 1.4'
    fn('p259/w/fo_on', ['tag @s add bm.pwfo', click, 'function bm:p179/w/open'])
    fn('p259/w/fo_off', ['tag @s remove bm.pwfo', click, 'function bm:p179/w/open'])
    fn('p259/w/az_on', ['tag @s add bm.pwaz', click, 'function bm:p179/w/open'])
    fn('p259/w/az_off', ['tag @s remove bm.pwaz', click, 'function bm:p179/w/open'])
    G.FUNCS['p28/act'].append('execute if score #act bm.pay matches 3505..3599 run return run function bm:p259/w/act')

    # ---------------------------------------------------------------- (b) PEARLMAN: his card again only if you've lost it
    pearl = next(i for i, e in enumerate(PW) if e[0] == 'pearl')
    rq = G.FUNCS['p128/reissue']
    k = next(i for i, l in enumerate(rq) if l.startswith('execute if score #has bm.rng matches 0 run give') and 'pearl_card' in l)
    bag = lambda iid: (f'execute if items entity @s container.* *[minecraft:container~{{items:{{contains:[{{predicates:{{"minecraft:custom_data":{{bm:"{iid}"}}}}}}]}}}}] '
                       'run scoreboard players set #has bm.rng 1')
    rq[k:k] = [f'execute if score @s bm.pw{pearl} matches 1 run scoreboard players set #has bm.rng 1',          # (on the wheel - carried or not)
               f'execute if items entity @s player.cursor {holds("pearl_card")} run scoreboard players set #has bm.rng 1',
               bag('pearl_card'),                                                                                  # (in a bag or a shulker box on you)
               'execute if score #has bm.rng matches 1 run ' + title('@s', 'actionbar', [T('Pearlman: ', '#5ac8ff', bold=True),
                                                                                       T('"You still have my card, I see. Splendid - do keep it close."', 'white')])]
    k = next(i for i, l in enumerate(rq) if l.startswith('execute if score #has bm.rng matches 0 run give') and 'pearl_statue' in l)
    rq[k:k] = [f'execute if items entity @s player.cursor {holds("pearl_statue")} run scoreboard players set #has bm.rng 1', bag('pearl_statue')]

    # ---------------------------------------------------------------- (a) the Gallery's pages: from the roster, codes reserved
    pages = -(-len(P125_WHO()) // P220.PER)
    assert P220.pg_code(pages - 1) <= 3425 and pages <= 10, 'the Gallery has outgrown its codes (3353-3358, 3422-3425)'
    assert all(f'p220/view{i}' in G.FUNCS for i in range(pages))


def P125_WHO():
    import phase125 as P125
    return P125.WHO


# ========================================================================================= the bank: send to a player
def bank(G):
    import phase28 as P28
    fn, title, tellraw, PREFIX = G.fn, G.title, G.tellraw, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    BK = P31.BANK
    assert len(BK) <= 20, 'the bank send page has codes for 20 currencies (5310-5329)'
    objs = ['bm.bst', 'bm.bsc', 'bm.bsn']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + ['scoreboard objectives add bm.bsam trigger']
    G.OBJECTIVES += objs + ['bm.bsam']
    G.FUNCS['loop/fast'] += ['execute as @a[scores={bm.bsam=1..}] at @s run function bm:p259/bs/typed',
                             'execute as @a[scores={bm.bsam=..-1}] run scoreboard players set @s bm.bsam 0',
                             'scoreboard players enable @a bm.bsam']
    gate = [f'execute unless score @s bm.menu matches {BS_MENU} run return run function bm:p28/stale',
            'execute unless function bm:p31/bank/can run return run function bm:p28/stale']
    # ---- 1: who to
    fn('p259/bs/who', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'tag @s add bm.bsme',
                       'data modify storage bm:bs acts set value []',
                       'execute as @a[tag=!bm.bsme] at @s run function bm:p259/bs/btn', 'tag @s remove bm.bsme',
                       'execute unless data storage bm:bs acts[0] run return run ' + say('Nobody else is online to send to.'),
                       f'data modify storage bm:bs acts append value {snbt(P28.btn(T("« Your account", "gray"), BS_ACC, width=150))}',
                       f'scoreboard players set @s bm.menu {BS_MENU}', 'function bm:p259/bs/who_show with storage bm:bs',
                       'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 0.8 1.3'])
    d = P28.multi([T('Send to a player', '#7ad8ff', bold=True), T('  \u00b7  The Rat Bank', 'gray')],
                  [P28.body([T('Who gets it? It goes from your account straight into theirs.', 'gray')], 300)], '@@ACTS@@', columns=2)
    fn('p259/bs/who_show', ['$dialog show @s ' + snbt(d).replace('"@@ACTS@@"', '$(acts)')])
    fn('p259/bs/name', ['summon minecraft:item_display ~ ~-64 ~ {Tags:["bm.bsnm"],item:{id:"minecraft:paper",count:1}}',
                        'item modify entity @e[type=minecraft:item_display,tag=bm.bsnm,limit=1] contents {function:"minecraft:set_name",target:"custom_name",entity:"this",name:{selector:"@s"}}',
                        'data modify storage bm:bs nm set from entity @e[type=minecraft:item_display,tag=bm.bsnm,limit=1] item.components."minecraft:custom_name"',
                        'kill @e[type=minecraft:item_display,tag=bm.bsnm]'])
    fn('p259/bs/btn', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'function bm:p259/bs/name',
                       f'scoreboard players operation #c bm.rng = @s bm.pid', f'scoreboard players add #c bm.rng {BS_PID}',
                       'execute store result storage bm:bs code int 1 run scoreboard players get #c bm.rng', 'function bm:p259/bs/btn2 with storage bm:bs'])
    fn('p259/bs/btn2', ['$data modify storage bm:bs acts append value {label:$(nm),width:150,tooltip:{text:"Send to them",color:"gray"},'
                        'action:{type:"minecraft:run_command",command:"/trigger bm.act set $(code)"}}'])
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {BS_PID + 1}..{BS_PID + 999999} run return run function bm:p259/bs/pick')
    fn('p259/bs/pick', gate + ['scoreboard players operation #t bm.rng = #act bm.pay', f'scoreboard players remove #t bm.rng {BS_PID}',
                               'execute if score #t bm.rng = @s bm.pid run return run ' + say('That\'s you - pick someone else.'),
                               'tag @a remove bm.bstg', 'execute as @a if score @s bm.pid = #t bm.rng run tag @s add bm.bstg',
                               'execute unless entity @a[tag=bm.bstg] run return run ' + say('They\'ve gone offline.'),
                               'execute store result storage bm:bs pid int 1 run scoreboard players get @s bm.pid',
                               'execute as @a[tag=bm.bstg,limit=1] at @s run function bm:p259/bs/name',
                               'function bm:p259/bs/keep_nm with storage bm:bs', 'tag @a remove bm.bstg',
                               'scoreboard players operation @s bm.bst = #t bm.rng', 'scoreboard players set @s bm.bsc -1', 'scoreboard players set @s bm.bsn 0',
                               'function bm:p259/bs/cur'])
    fn('p259/bs/keep_nm', ['$data modify storage bm:bs p$(pid).nm set from storage bm:bs nm'])
    # (every page reads its recipient's name and the currency back from your own scores and storage)
    pg = ['data remove storage bm:ui bs', 'execute store result storage bm:ui bs.pid int 1 run scoreboard players get @s bm.pid',
          'data modify storage bm:ui bs.r_nm set value {text:"them",color:"white"}', 'function bm:p259/bs/get_nm with storage bm:ui bs',
          'data modify storage bm:ui bs.r_cn set value {text:"-",color:"gray"}', 'data modify storage bm:ui bs.have set value 0']
    for i, (cur, obj, nm, col) in enumerate(BK):
        pg += [f'execute if score @s bm.bsc matches {i} run data modify storage bm:ui bs.r_cn set value {snbt(T(nm, col, bold=True))}',
               f'execute if score @s bm.bsc matches {i} store result storage bm:ui bs.have int 1 run scoreboard players get @s {obj}']
    pg += ['execute store result storage bm:ui bs.n int 1 run scoreboard players get @s bm.bsn', 'data modify storage bm:ui bs.amt set value "$(amt)"',
           f'scoreboard players set @s bm.menu {BS_MENU}']
    fn('p259/bs/fill', pg)
    fn('p259/bs/get_nm', ['$execute if data storage bm:bs p$(pid).nm run data modify storage bm:ui bs.r_nm set from storage bm:bs p$(pid).nm'])
    # ---- 2: which currency
    cbtn = [P28.btn([T(nm, col), T(f'   $(b{i})', 'white')], BS_CUR + i, width=150, tooltip=T(f'Send some of your {nm}', 'gray'))
            for i, (cur, obj, nm, col) in enumerate(BK)]
    cbtn += [P28.btn(T('\u00ab Someone else', 'gray'), BS_WHO, width=150), P28.btn(T('\u00ab Your account', 'gray'), BS_ACC, width=150)]
    cd = P28.multi([T('Send to ', '#7ad8ff', bold=True), '@@RAW:r_nm@@'],
                   [P28.body([T('Which currency? (What\'s in your account beside each.)', 'gray')], 300)], cbtn, columns=2)
    fn('p259/bs/cur', ['function bm:p259/bs/fill'] +
       [f'execute unless score @s {obj} matches 0.. run scoreboard players set @s {obj} 0' for cur, obj, nm, col in BK] +
       [f'execute store result storage bm:ui bs.b{i} int 1 run scoreboard players get @s {obj}' for i, (cur, obj, nm, col) in enumerate(BK)] +
       ['function bm:p259/bs/cur_show with storage bm:ui bs'])
    fn('p259/bs/cur_show', ['$dialog show @s ' + P28.inline(cd)])
    for i, (cur, obj, nm, col) in enumerate(BK):
        fn(f'p259/bs/c{i}', [f'execute unless score @s {obj} matches 1.. run return run ' + say(f'You have no {nm} in your account.'),
                             f'scoreboard players set @s bm.bsc {i}', 'scoreboard players set @s bm.bsn 0', 'function bm:p259/bs/amt'])
    # ---- 3: how many (presets, or typed into the box: /trigger bm.bsam)
    PRESETS = [(1, '1'), (10, '10'), (64, '64'), (-1, 'All')]
    abtn = [P28.btn(T(lbl, 'white'), BS_PRE + k, width=72) for k, (n, lbl) in enumerate(PRESETS)]
    ad = P28.multi([T('Send ', '#7ad8ff', bold=True), '@@RAW:r_cn@@', T(' to ', '#7ad8ff', bold=True), '@@RAW:r_nm@@'],
                   [P28.body([T('In your account: ', 'gray'), T('$(have)', 'white', bold=True), T('. How many?', 'gray')], 300)],
                   abtn + [{'label': T('Send the typed amount', GOLD), 'width': Int(150),
                            'action': {'type': 'minecraft:dynamic/run_command', 'template': 'trigger bm.bsam set $(amt)'}},
                           P28.btn(T('\u00ab Another currency', 'gray'), BS_CURBACK, width=150)], columns=4)
    ad['inputs'] = [{'type': 'minecraft:text', 'key': 'amt', 'label': T('Or type an amount', GOLD), 'width': Int(150), 'max_length': Int(7)}]
    fn('p259/bs/amt', ['function bm:p259/bs/fill', 'function bm:p259/bs/amt_show with storage bm:ui bs'])
    fn('p259/bs/amt_show', ['$dialog show @s ' + P28.inline(ad)])
    for k, (n, lbl) in enumerate(PRESETS):
        fn(f'p259/bs/pre{k}', (['function bm:p259/bs/have', 'scoreboard players operation @s bm.bsn = #bsh bm.rng'] if n < 0 else
                               [f'scoreboard players set @s bm.bsn {n}']) + ['function bm:p259/bs/check'])
    fn('p259/bs/have', ['scoreboard players set #bsh bm.rng 0'] +
       [f'execute if score @s bm.bsc matches {i} run scoreboard players operation #bsh bm.rng = @s {obj}' for i, (cur, obj, nm, col) in enumerate(BK)])
    fn('p259/bs/typed', ['scoreboard players operation #bst bm.rng = @s bm.bsam', 'scoreboard players set @s bm.bsam 0',
                         f'execute unless score @s bm.menu matches {BS_MENU} run return 0', 'execute unless score @s bm.bsc matches 0.. run return 0',
                         'execute unless function bm:p31/bank/can run return 0',
                         'scoreboard players operation @s bm.bsn = #bst bm.rng', 'function bm:p259/bs/check'])
    fn('p259/bs/check', ['function bm:p259/bs/have',
                         'execute if score @s bm.bsn matches ..0 run return run function bm:p259/bs/amt',
                         'execute if score @s bm.bsn > #bsh bm.rng run ' + title('@s', 'actionbar', [T('You only have ', 'gray'),
                                                                                                       {'score': {'name': '#bsh', 'objective': 'bm.rng'}, 'color': 'white'},
                                                                                                       T(' in your account.', 'gray')]),
                         'execute if score @s bm.bsn > #bsh bm.rng run return run function bm:p259/bs/amt',
                         'function bm:p259/bs/conf'])
    # ---- 4: are you sure?
    cf = P28.multi([T('Send it?', '#7ad8ff', bold=True), T('  \u00b7  The Rat Bank', 'gray')],
                   [P28.body([T('Send ', 'gray'), T('$(n) ', 'white', bold=True), '@@RAW:r_cn@@', T(' to ', 'gray'), '@@RAW:r_nm@@',
                              T('? It leaves your account and goes into theirs.', 'gray')], 300)],
                   [P28.btn([T('\u2714 ', '#7aff7a'), T('Send it', 'white', bold=True)], BS_SEND, width=150),
                    P28.btn(T('\u00ab Change the amount', 'gray'), BS_AMTBACK, width=150)], columns=2)
    fn('p259/bs/conf', ['function bm:p259/bs/fill', 'function bm:p259/bs/conf_show with storage bm:ui bs'])
    fn('p259/bs/conf_show', ['$dialog show @s ' + P28.inline(cf)])
    fn('p259/bs/send', ['execute unless score @s bm.bsn matches 1.. run return run function bm:p259/bs/amt',
                        'scoreboard players operation #t bm.rng = @s bm.bst',
                        'execute if score #t bm.rng = @s bm.pid run return run ' + say('You can\'t send to yourself.'),
                        'tag @a remove bm.bstg', 'execute as @a if score @s bm.pid = #t bm.rng run tag @s add bm.bstg',
                        'execute unless entity @a[tag=bm.bstg] run return run ' + say('They\'ve gone offline - nothing was sent.'),
                        'scoreboard players operation #n bm.pay = @s bm.bsn'] +
       [f'execute if score @s bm.bsc matches {i} run return run function bm:p259/bs/do{i}' for i in range(len(BK))])
    for i, (cur, obj, nm, col) in enumerate(BK):
        n = {'score': {'name': '#n', 'objective': 'bm.pay'}, 'color': col, 'bold': True}
        fn(f'p259/bs/do{i}', [f'execute unless score @s {obj} matches 0.. run scoreboard players set @s {obj} 0',
                              f'execute if score #n bm.pay > @s {obj} run tag @a remove bm.bstg',
                              f'execute if score #n bm.pay > @s {obj} run return run function bm:p259/bs/check',
                              f'scoreboard players operation @s {obj} -= #n bm.pay',
                              f'execute as @a[tag=bm.bstg] unless score @s {obj} matches 0.. run scoreboard players set @s {obj} 0',
                              f'scoreboard players operation @a[tag=bm.bstg] {obj} += #n bm.pay',
                              tellraw('@s', PREFIX + [T('The Rat Bank: ', 'gold', bold=True), T('sent ', 'gray'), n, T(f' {nm}', col),
                                                      T(' to ', 'gray'), {'selector': '@a[tag=bm.bstg]', 'color': 'white'}, T(' from your account.', 'gray')]),
                              tellraw('@a[tag=bm.bstg]', PREFIX + [T('The Rat Bank: ', 'gold', bold=True), {'selector': '@s', 'color': 'white'},
                                                                   T(' sent you ', 'gray'), n, T(f' {nm}', col), T(' - it\'s in your account.', 'gray')]),
                              'playsound minecraft:block.chain.place player @s ~ ~ ~ 0.8 1.4',
                              'execute as @a[tag=bm.bstg] at @s run playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.6 1.2',
                              'tag @a remove bm.bstg', 'scoreboard players set @s bm.bsn 0', 'function bm:p31/bank/open'])
    act = gate + [f'execute if score #act bm.pay matches {BS_WHO} run return run function bm:p259/bs/who',
                  f'execute if score #act bm.pay matches {BS_ACC} run return run function bm:p31/bank/open',
                  f'execute if score #act bm.pay matches {BS_CURBACK} run return run function bm:p259/bs/cur',
                  f'execute if score #act bm.pay matches {BS_AMTBACK} run return run function bm:p259/bs/amt',
                  f'execute if score #act bm.pay matches {BS_SEND} run return run function bm:p259/bs/send'] + \
          [f'execute if score #act bm.pay matches {BS_CUR + i} run return run function bm:p259/bs/c{i}' for i in range(len(BK))] + \
          [f'execute if score #act bm.pay matches {BS_PRE}..{BS_PRE + len(PRESETS) - 1} unless score @s bm.bsc matches 0.. run return run function bm:p28/stale'] + \
          [f'execute if score #act bm.pay matches {BS_PRE + k} run return run function bm:p259/bs/pre{k}' for k in range(len(PRESETS))]
    fn('p259/bs/act', act)
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {BS_MENU}..{BS_MENU + 99} run return run function bm:p259/bs/act')


# ========================================================================================= naming an item (for the haul and the bags)
def _namer(G):
    """storage bm:tmp nmi (an item stack) -> bm:tmp nmo (its name: its own item_name / custom_name, else the game's, through an
    item entity's name read off a scratch display - p73's trick). Run at a spot in a loaded chunk."""
    G.fn('p259/nm/get', ['data remove storage bm:tmp nmo',
                         'data modify storage bm:tmp nmo set from storage bm:tmp nmi.components."minecraft:item_name"',
                         'data modify storage bm:tmp nmo set from storage bm:tmp nmi.components."minecraft:custom_name"',
                         'execute if data storage bm:tmp nmo run return 1',
                         'summon minecraft:item ~ ~ ~ {Tags:["bm.nmi"],PickupDelay:32767s,NoGravity:1b,Item:{id:"minecraft:stone",count:1}}',
                         'data modify entity @e[type=minecraft:item,tag=bm.nmi,limit=1] Item set from storage bm:tmp nmi',
                         'summon minecraft:item_display ~ ~ ~ {Tags:["bm.nmd"],item:{id:"minecraft:paper",count:1}}',
                         'item modify entity @e[type=minecraft:item_display,tag=bm.nmd,limit=1] contents {function:"minecraft:set_name",target:"custom_name",'
                         'entity:"this",name:{selector:"@e[type=minecraft:item,tag=bm.nmi,limit=1]"}}',
                         'data modify storage bm:tmp nmo set from entity @e[type=minecraft:item_display,tag=bm.nmd,limit=1] item.components."minecraft:custom_name"',
                         'kill @e[type=minecraft:item,tag=bm.nmi]', 'kill @e[type=minecraft:item_display,tag=bm.nmd]',
                         'data remove storage bm:tmp nmo.hover_event', 'data remove storage bm:tmp nmo.insertion',
                         'execute unless data storage bm:tmp nmo run data modify storage bm:tmp nmo set value {text:"?"}', 'return 1'])


# ========================================================================================= the heist haul
def haul(G):
    import phase28 as P28
    import phase80 as P80
    fn, title = G.fn, G.title
    _namer(G)
    PER = 1000                                       # (worth in thousandths of a Token)
    TV = {'token': 1, 'medallion': 5, 'trophy': 20, 'lucky_token': 5, 'blood_crystal': 1, 'dread_token': 100}
    val = {k: v * PER for k, v in TV.items()}
    val.update({'gutter_coin': PER // P80.TOKEN_COINS, 'gutter_medallion': 16 * PER // P80.TOKEN_COINS, 'gutter_trophy': 128 * PER // P80.TOKEN_COINS})
    for s, (kk, pay) in G.SCRAP_TABLE.items():
        if s in val or not all(c in TV for c, _n in pay): continue
        v = sum(n * TV[c] for c, n in pay) * PER // kk
        if v > 0: val[s] = v
    G.FUNCS['load'][-1:-1] = [f'data modify storage bm:hl val set value {snbt({k: Int(v) for k, v in sorted(val.items())})}']
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.hlw dummy', f'scoreboard players set #{PER} bm.rng {PER}']
    G.OBJECTIVES.append('bm.hlw')
    BK = P31.BANK
    # ---- going in (a heist's enter or join, before the coat check takes anything): what you carry, what's in your account
    fn('p259/hl/start', ['execute if entity @s[tag=bm.hlon] run return 0', 'tag @s add bm.hlon', 'data remove storage bm:tmp hls',
                         'execute store result storage bm:tmp hls.pid int 1 run scoreboard players get @s bm.pid', 'function bm:p259/hl/start_m with storage bm:tmp hls'])
    fn('p259/hl/start_m', ['$data modify storage bm:hl p$(pid) set value {a:[],bk:{}}', '$data modify storage bm:hl p$(pid).a set from entity @s Inventory'] +
       [f'$execute store result storage bm:hl p$(pid).bk.{cur} int 1 run scoreboard players get @s {obj}' for cur, obj, nm, col in BK])
    hooked = 0
    for name, L in G.FUNCS.items():
        if re.match(r'^p70/s\d+/(enter|join)$', name):
            L.insert(0, 'function bm:p259/hl/start'); hooked += 1
    assert hooked >= 2, hooked
    # ---- coming out (p70/unraid, before the coat check gives your pack back): what's new, by item
    un = G.FUNCS['p70/unraid']
    k = un.index('execute unless entity @s[tag=bm.lgbag] at @s run function bm:p72/bag/restore')
    un.insert(k, 'execute if entity @s[tag=bm.hlon] run function bm:p259/hl/end')
    fn('p259/hl/end', ['tag @s remove bm.hlon', 'data remove storage bm:tmp hls',
                       'execute store result storage bm:tmp hls.pid int 1 run scoreboard players get @s bm.pid', 'function bm:p259/hl/end_m with storage bm:tmp hls'])
    em = ['$data modify storage bm:hl a set from storage bm:hl p$(pid).a', '$data modify storage bm:hl bk set from storage bm:hl p$(pid).bk',
          '$data remove storage bm:hl p$(pid)',
          'data modify storage bm:hl b set from entity @s Inventory', 'data modify storage bm:hl t set value {}', 'data modify storage bm:hl keys set value []',
          'function bm:p259/hl/add', 'function bm:p259/hl/sub',
          'data modify storage bm:hl rows set value [{text:"",color:"gray"}]', 'scoreboard players set #hlv bm.rng 0', 'scoreboard players set #hlr bm.rng 0',
          'function bm:p259/hl/emit']
    for cur, obj, nm, col in BK:                      # (and what went straight into your account)
        em += [f'execute store result score #hb bm.rng run data get storage bm:hl bk.{cur}', f'scoreboard players operation #hn bm.rng = @s {obj}',
               'scoreboard players operation #hn bm.rng -= #hb bm.rng', f'execute if score #hn bm.rng matches 1.. run function bm:p259/hl/bk_{cur}']
        G.fn(f'p259/hl/bk_{cur}', ['scoreboard players set #hu bm.rng 0', f'execute store result score #hu bm.rng run data get storage bm:hl val.{cur}',
                                   'data modify storage bm:tmp nmo set value ' + snbt(T(nm, col)), 'function bm:p259/hl/bank'])
    em += ['execute store result storage bm:tmp hlo.v int 1 run scoreboard players operation #hlv bm.rng /= #1000 bm.rng',
           'execute store result storage bm:tmp hlo.r int 1 run scoreboard players get #hlr bm.rng',
           '$data modify storage bm:hl p$(pid).rows set from storage bm:hl rows', '$data modify storage bm:hl p$(pid).v set from storage bm:tmp hlo.v',
           '$data modify storage bm:hl p$(pid).r set from storage bm:tmp hlo.r', 'scoreboard players set @s bm.hlw 3']
    fn('p259/hl/end_m', em)
    # the tally: t."<key>" counts (a Black Market item by its bm id, the rest by item id); keys lists each once, with a stack to name
    def walker(name, src, sign):
        fn(f'p259/hl/{name}', [f'execute unless data storage bm:hl {src}[0] run return 0', f'data modify storage bm:hl e set from storage bm:hl {src}[0]',
                               f'data remove storage bm:hl {src}[0]', 'data modify storage bm:hl x set value {n:1}',
                               'data modify storage bm:hl x.k set from storage bm:hl e.id',
                               'data modify storage bm:hl x.k set from storage bm:hl e.components."minecraft:custom_data".bm',
                               'execute if data storage bm:hl e.count store result storage bm:hl x.n int 1 run data get storage bm:hl e.count',
                               f'function bm:p259/hl/{name}1 with storage bm:hl x', f'function bm:p259/hl/{name}'])
    walker('add', 'b', 1)
    walker('sub', 'a', -1)
    fn('p259/hl/add1', ['$execute unless data storage bm:hl t."$(k)" run function bm:p259/hl/newkey',
                        '$execute store result score #hc bm.rng run data get storage bm:hl t."$(k)"', '$scoreboard players add #hc bm.rng $(n)',
                        '$execute store result storage bm:hl t."$(k)" int 1 run scoreboard players get #hc bm.rng'])
    fn('p259/hl/newkey', ['data modify storage bm:hl keys append value {}', 'data modify storage bm:hl keys[-1].k set from storage bm:hl x.k',
                          'data modify storage bm:hl keys[-1].it set from storage bm:hl e', 'data remove storage bm:hl keys[-1].it.Slot'])
    fn('p259/hl/sub1', ['$execute unless data storage bm:hl t."$(k)" run return 0',
                        '$execute store result score #hc bm.rng run data get storage bm:hl t."$(k)"', '$scoreboard players remove #hc bm.rng $(n)',
                        '$execute store result storage bm:hl t."$(k)" int 1 run scoreboard players get #hc bm.rng'])
    fn('p259/hl/emit', ['execute unless data storage bm:hl keys[0] run return 0', 'data modify storage bm:hl y set value {}',
                        'data modify storage bm:hl y.k set from storage bm:hl keys[0].k', 'function bm:p259/hl/emit1 with storage bm:hl y',
                        'data remove storage bm:hl keys[0]', 'function bm:p259/hl/emit'])
    fn('p259/hl/emit1', ['$execute store result score #hn bm.rng run data get storage bm:hl t."$(k)"', 'execute if score #hn bm.rng matches ..0 run return 0',
                         'scoreboard players set #hu bm.rng 0', '$execute store result score #hu bm.rng run data get storage bm:hl val."$(k)"',
                         'data modify storage bm:tmp nmi set from storage bm:hl keys[0].it', 'function bm:p259/nm/get', 'function bm:p259/hl/row'])
    fn('p259/hl/bank', ['function bm:p259/hl/row', 'data modify storage bm:hl rows[-1].extra append value ' + snbt(T(' (into your account)', 'dark_gray'))])
    # (a row: "- 32x <name>  ~ 12 Tokens", and the worth added to the total)
    fn('p259/hl/row', ['scoreboard players add #hlr bm.rng 1', 'scoreboard players operation #hw bm.rng = #hn bm.rng', 'scoreboard players operation #hw bm.rng *= #hu bm.rng',
                       'scoreboard players operation #hlv bm.rng += #hw bm.rng', 'scoreboard players operation #hw bm.rng /= #1000 bm.rng',
                       'data modify storage bm:tmp hlr set value {}', 'execute store result storage bm:tmp hlr.n int 1 run scoreboard players get #hn bm.rng',
                       'execute store result storage bm:tmp hlr.w int 1 run scoreboard players get #hw bm.rng',
                       'function bm:p259/hl/row_m with storage bm:tmp hlr',
                       'data modify storage bm:hl rows[-1].extra append from storage bm:tmp nmo',
                       'execute if score #hu bm.rng matches 1.. if score #hw bm.rng matches 1.. run function bm:p259/hl/row_w with storage bm:tmp hlr',
                       'execute if score #hu bm.rng matches 1.. if score #hw bm.rng matches 0 run data modify storage bm:hl rows[-1].extra append value ' +
                       snbt(T('  (under a Token)', 'dark_gray'))])
    fn('p259/hl/row_m', ['$data modify storage bm:hl rows append value {text:"\\n\u2022 $(n)\u00d7 ",color:"white",italic:false,extra:[]}'])
    fn('p259/hl/row_w', ['$data modify storage bm:hl rows[-1].extra append value {text:"  \u2248 $(w) Tokens",color:"' + GOLD + '"}'])
    # ---- the card, a moment after you're home
    G.FUNCS['loop/second'].append('execute as @a[scores={bm.hlw=1..}] at @s run function bm:p259/hl/tick')
    fn('p259/hl/tick', ['scoreboard players remove @s bm.hlw 1', 'execute if score @s bm.hlw matches 1.. run return 0',
                        'execute if dimension bm:gutter run return 0',
                        'data remove storage bm:tmp hls', 'execute store result storage bm:tmp hls.pid int 1 run scoreboard players get @s bm.pid',
                        'function bm:p259/hl/show_m with storage bm:tmp hls'])
    nothing = T('\nNothing new came out with you this time.', 'gray', italic=True)
    fn('p259/hl/show_m', ['$execute unless data storage bm:hl p$(pid).rows run return 0',
                          'data remove storage bm:ui hl', '$data modify storage bm:ui hl.r_rows set from storage bm:hl p$(pid).rows',
                          '$data modify storage bm:ui hl.v set from storage bm:hl p$(pid).v', '$data modify storage bm:ui hl.r set from storage bm:hl p$(pid).r',
                          '$data remove storage bm:hl p$(pid)',
                          f'execute if data storage bm:ui {{hl:{{r:0}}}} run data modify storage bm:ui hl.r_rows append value {snbt(nothing)}',
                          'function bm:p259/hl/show with storage bm:ui hl', 'playsound minecraft:item.armor.equip_gold player @s ~ ~ ~ 0.7 1.2'])
    d = P28.notice([T('The Haul', GOLD, bold=True), T('  \u00b7  this heist', 'gray')],
                   [P28.body([T('What you came out with', 'white', bold=True), T(' (that you didn\'t take in):', 'gray'),
                              {'text': '', 'extra': '@@RAW:r_rows@@'}], 300),
                    P28.body([T('Worth about ', 'gray'), T('$(v) Tokens', GOLD, bold=True), T(' in all', 'gray')], 300),
                    P28.body([T('(At the Scrap Bin\'s buy-back, the Fence\'s rates for currencies, and the Gutter Bank\'s for its coins.)', 'dark_gray')], 300)])
    fn('p259/hl/show', ['$dialog show @s ' + P28.inline(d)])


# ========================================================================================= the bags: what's inside, in the lore
def bags(G):
    import phase248 as P248
    fn = G.fn
    SHOW = 6
    L0 = {b: len(ITEMS[b]['comps'].get('minecraft:lore', [])) for b in P248.BAGS if b in ITEMS}
    assert set(L0) == set(P248.BAGS), set(P248.BAGS) - set(L0)
    # (in: storage bm:tmp bl.it - the bag's stack - and bl.c - its container list; out: bl.it's lore, and bl.lore / bl.k)
    fn('p259/bag/lore', ['scoreboard players set #bl0 bm.rng -1'] +
       [f'execute if data storage bm:tmp {{bl:{{it:{{components:{{"minecraft:custom_data":{{bm:"{b}"}}}}}}}}}} run scoreboard players set #bl0 bm.rng {n}' for b, n in L0.items()] +
       ['execute if score #bl0 bm.rng matches ..-1 run return 0',
        'execute unless data storage bm:tmp bl.it.components."minecraft:lore" run data modify storage bm:tmp bl.it.components."minecraft:lore" set value []',
        'function bm:p259/bag/trim',
        'execute store result score #bln bm.rng run data get storage bm:tmp bl.c',
        'execute store result storage bm:tmp blx.n int 1 run scoreboard players get #bln bm.rng',
        'execute if score #bln bm.rng matches 0 run data modify storage bm:tmp bl.it.components."minecraft:lore" append value ' + snbt(T('Contains: nothing', 'gray')),
        'execute if score #bln bm.rng matches 1 run data modify storage bm:tmp bl.it.components."minecraft:lore" append value ' + snbt(T('Contains: 1 stack', 'gray')),
        'execute if score #bln bm.rng matches 2.. run function bm:p259/bag/head with storage bm:tmp blx',
        'data modify storage bm:tmp blw set from storage bm:tmp bl.c', 'scoreboard players set #blk bm.rng 0', 'function bm:p259/bag/each',
        f'scoreboard players remove #bln bm.rng {SHOW}',
        'execute store result storage bm:tmp blx.m int 1 run scoreboard players get #bln bm.rng',
        'execute if score #bln bm.rng matches 1.. run function bm:p259/bag/more with storage bm:tmp blx',
        'data modify storage bm:tmp bl.lore set from storage bm:tmp bl.it.components."minecraft:lore"', 'return 1'])
    fn('p259/bag/trim', ['execute store result score #blh bm.rng run data get storage bm:tmp bl.it.components."minecraft:lore"',
                         'execute if score #blh bm.rng <= #bl0 bm.rng run return 0', 'data remove storage bm:tmp bl.it.components."minecraft:lore"[-1]',
                         'function bm:p259/bag/trim'])
    fn('p259/bag/head', ['$data modify storage bm:tmp bl.it.components."minecraft:lore" append value {text:"Contains: $(n) stacks",color:"gray",italic:false}'])
    fn('p259/bag/more', ['$data modify storage bm:tmp bl.it.components."minecraft:lore" append value {text:"\u2026and $(m) more",color:"dark_gray",italic:false}'])
    fn('p259/bag/each', [f'execute if score #blk bm.rng matches {SHOW}.. run return 0', 'execute unless data storage bm:tmp blw[0] run return 0',
                         'data modify storage bm:tmp nmi set from storage bm:tmp blw[0].item', 'function bm:p259/nm/get',
                         'data modify storage bm:tmp blx.c set value 1',
                         'execute if data storage bm:tmp blw[0].item.count run data modify storage bm:tmp blx.c set from storage bm:tmp blw[0].item.count',
                         'function bm:p259/bag/line with storage bm:tmp blx',
                         'data modify storage bm:tmp bl.it.components."minecraft:lore"[-1].extra append from storage bm:tmp nmo',
                         'data remove storage bm:tmp blw[0]', 'scoreboard players add #blk bm.rng 1', 'function bm:p259/bag/each'])
    fn('p259/bag/line', ['$data modify storage bm:tmp bl.it.components."minecraft:lore" append value {text:"\u2022 $(c)\u00d7 ",color:"white",italic:false,extra:[]}'])
    # folding (every box kind: the stack waits in storage bm:pbox p<pid> with its contents set)
    bk = G.FUNCS['p33/box/back']
    assert bk[0] == '$data modify storage bm:pbox p$(pid).components."minecraft:container" set from storage bm:tmp bx.out', bk[0]
    bk[1:1] = ['$data modify storage bm:tmp bl.it set from storage bm:pbox p$(pid)', 'data modify storage bm:tmp bl.c set from storage bm:tmp bx.out',
               '$execute if function bm:p259/bag/lore run data modify storage bm:pbox p$(pid) set from storage bm:tmp bl.it']
    # the satchel's pick-up (its container written into the stack in your inventory)
    vw = G.FUNCS['p33/vac/write']
    assert vw[0].startswith('$item modify entity @s container.$(n) '), vw[0]
    vw[1:1] = ['$data modify storage bm:tmp bl.it set from entity @s Inventory[{Slot:$(n)b}]', 'data modify storage bm:tmp bl.c set from storage bm:tmp vac.c',
               '$data modify storage bm:tmp bl.n set value $(n)',
               'execute if function bm:p259/bag/lore run function bm:p259/bag/apply with storage bm:tmp bl']
    fn('p259/bag/apply', ['$item modify entity @s container.$(n) {function:"minecraft:set_lore",entity:"this",mode:"replace_all",lore:$(lore)}'])

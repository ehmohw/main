"""3.0k: THE MENUS, TIDIED (menu_proposal.md, approved) - long lists in pages, the bank card in groups, one word for one action,
a tooltip on every follower-menu verb, the crew page's rules in a tooltip. Nothing removed: every button that moves keeps its code
and its router (tools/menu_inventory.py checks that on every build).

PAGES (12 a page, the wheel 8 partners - 24): the Recruiter's book (p137/rc/main), the Tailor's followers (p103/tl/main) and its
            auras (p103/tl/auras), the Outfits page off the Ledger (p119/page), the Partner Wheel's partners (p179/w/open). Each list
            is still built as before; a pager (p261/pg/<key>) cuts the page you're on out of it and adds "‹ Previous" / "Next ›"
            (the page is remembered per player - bm.pg_<key> - so a purchase or a call brings you back to the same page). The
            page is clamped to the list, so a shorter list never leaves you past its end.
THE WHEEL   Chatter and Keep up leave the wheel: both are on "⚙ Your settings" (and on every follower's Settings page).
THE RAT BANK CARD   the account page: your four main balances at a glance, then Currencies ›, Deposit everything, Auto-deposit,
            Savings, the Exchange, Community Pots, Send to a player. Currencies › (4094) is the list of the 13, each to its own page.
THE RAID CREW   its title says how many are switched on; the two paragraphs of rules went into a "? How the crew works" tooltip.
WORDS       on every follower's own menu: "Call <name>" (it was "Call for <name>" / "Call <name>" / "Call him over"), "Sit / follow"
            (Pearlman's "Wait here / follow me"), and a tooltip on Sit, Send home and Call where there was none. Your settings and
            the Particle Toggler close with "Close" like every other page.
Codes: pagers - the Recruiter 8098/8099, Outfits 7966/7967, the Tailor 8450/8451, its auras 8452/8453, the wheel 3440/3441 (each
routed in the page's own router, under its menu); the bank's Currencies 4094."""
import re
from items import T
from nbt import snbt
import phase260 as P260

N = 12
# key: (function, storage path of the list, anchor (insert the pager before the first line containing it; None: after `after`),
#       after, per page, prev code, next code, router, its first line to keep above ours, reopen, columns)
PAGERS = {
    'rc': ('p137/rc/main', 'bm:ui rc.acts', '"/trigger bm.act set 8040"', None, N, 8098, 8099, 'p137/rc/act', 1, 'p137/rc/main', 2),
    'ow': ('p119/page', 'bm:ui crx.acts', '"/trigger bm.act set 7961"', None, N, 7966, 7967, 'p119/act', 0, 'p119/page', 2),
    'tl': ('p103/tl/main', 'bm:ui tl.acts', '"/trigger bm.act set 7748"', None, N, 8450, 8451, 'p103/tl/act', 0, 'p103/tl/main', 2),
    'ta': ('p103/tl/auras', 'bm:ui tl.acts', '"/trigger bm.act set 7740"', None, N, 8452, 8453, 'p103/tl/act', 0, 'p103/tl/auras', 2),
    'wh': ('p179/w/open', 'bm:tmp pw.acts', None, 'function bm:p259/w/rows', 24, 3440, 3441, 'p179/w/act', 1, 'p179/w/open', 3),
}
CUR = 4094
TIP = {'sit': 'Sit down where they stand - or get up and follow you again.',
       'home': 'They go home. Call them again with their item or the wheel.',
       'call': 'They come to your side - unless they\'re still resting after a faint.'}


def generate(G):
    import phase28 as P28
    import phase31 as P31
    fn = G.fn
    F = G.FUNCS
    rep = {}
    objs = [f'bm.pg_{k}' for k in PAGERS]
    F['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs

    # ================================================================== THE PAGER
    fn('p261/pg/run', ['execute store result score #pgt bm.rng run data get storage bm:ui pg.src',
                       'scoreboard players operation #pgn bm.rng = #pgt bm.rng', 'scoreboard players operation #pgn bm.rng += #pgN bm.rng',
                       'scoreboard players remove #pgn bm.rng 1', 'scoreboard players operation #pgn bm.rng /= #pgN bm.rng',
                       'execute if score #pgn bm.rng matches ..0 run scoreboard players set #pgn bm.rng 1',
                       'execute if score #pgp bm.rng >= #pgn bm.rng run scoreboard players operation #pgp bm.rng = #pgn bm.rng',
                       'execute if score #pgp bm.rng = #pgn bm.rng run scoreboard players remove #pgp bm.rng 1',
                       'execute if score #pgp bm.rng matches ..-1 run scoreboard players set #pgp bm.rng 0',
                       'scoreboard players operation #pgs bm.rng = #pgp bm.rng', 'scoreboard players operation #pgs bm.rng *= #pgN bm.rng',
                       'scoreboard players operation #pge bm.rng = #pgs bm.rng', 'scoreboard players operation #pge bm.rng += #pgN bm.rng',
                       'scoreboard players operation #pgl bm.rng = #pgn bm.rng', 'scoreboard players remove #pgl bm.rng 1',
                       'scoreboard players set #pgi bm.rng 0', 'data modify storage bm:ui pg.out set value []', 'function bm:p261/pg/step',
                       'execute store result storage bm:ui pg.p int 1 run scoreboard players add #pgp bm.rng 1', 'scoreboard players remove #pgp bm.rng 1',
                       'execute store result storage bm:ui pg.n int 1 run scoreboard players get #pgn bm.rng'])
    fn('p261/pg/step', ['execute unless data storage bm:ui pg.src[0] run return 0',
                        'execute if score #pgi bm.rng >= #pgs bm.rng if score #pgi bm.rng < #pge bm.rng run data modify storage bm:ui pg.out append from storage bm:ui pg.src[0]',
                        'data remove storage bm:ui pg.src[0]', 'scoreboard players add #pgi bm.rng 1', 'function bm:p261/pg/step'])
    dim = lambda txt, w: snbt(P28.btn([T(txt, 'dark_gray')], None, width=w, tooltip=T('(no more this way)', 'dark_gray')))
    for key, (fname, S, anchor, after, per, prv, nxt, rtr, keep, reopen, cols) in PAGERS.items():
        L = F[fname]
        if anchor:
            k = next(i for i, l in enumerate(L) if anchor in l)
        else:
            k = L.index(after) + 1
        L.insert(k, f'function bm:p261/pg/{key}')
        w = 150 if cols == 3 else 180
        a_prev = snbt(P28.btn([T('‹ Previous', 'white')], prv, width=w, tooltip=T('The page before.', 'gray')))
        a_next = P28.btn([T('Next ›', 'white'), T('  $(p)/$(n)', 'gray')], nxt, width=w, tooltip=T('The next page.', 'gray'))
        nav = ['execute if score #pgp bm.rng matches 1.. run data modify storage bm:ui pg.out append value ' + a_prev,
               'execute if score #pgp bm.rng matches ..0 run data modify storage bm:ui pg.out append value ' + dim('‹ Previous', w)]
        if cols == 3:
            nav.append('$data modify storage bm:ui pg.out append value ' + snbt(P28.btn([T('Page $(p) of $(n)', 'gray')], None, width=w)))
            a_next = P28.btn([T('Next ›', 'white')], nxt, width=w, tooltip=T('The next page.', 'gray'))
        nav += ['$execute if score #pgp bm.rng < #pgl bm.rng run data modify storage bm:ui pg.out append value ' + snbt(a_next),
                'execute if score #pgp bm.rng >= #pgl bm.rng run data modify storage bm:ui pg.out append value ' + dim('Next ›', w)]
        fn(f'p261/pg/nav_{key}', [l if l[0] != '$' or '$(' in l else l[1:] for l in nav])
        fn(f'p261/pg/{key}', [f'scoreboard players operation #pgp bm.rng = @s bm.pg_{key}', f'scoreboard players set #pgN bm.rng {per}',
                              f'data modify storage bm:ui pg.src set from storage {S}', 'function bm:p261/pg/run',
                              f'scoreboard players operation @s bm.pg_{key} = #pgp bm.rng',
                              f'execute if score #pgn bm.rng matches 2.. run function bm:p261/pg/nav_{key} with storage bm:ui pg',
                              f'data modify storage {S} set from storage bm:ui pg.out'])
        fn(f'p261/pg/{key}_prev', [f'scoreboard players remove @s bm.pg_{key} 1', 'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 0.6 1.2', f'function bm:{reopen}'])
        fn(f'p261/pg/{key}_next', [f'scoreboard players add @s bm.pg_{key} 1', 'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 0.6 1.2', f'function bm:{reopen}'])
        R = F[rtr]
        R[keep:keep] = [f'execute if score #act bm.pay matches {prv} run return run function bm:p261/pg/{key}_prev',
                        f'execute if score #act bm.pay matches {nxt} run return run function bm:p261/pg/{key}_next']
    rep['pagers'] = len(PAGERS)

    # ================================================================== THE WHEEL: its global switches are on Your settings
    op = F['p179/w/open']
    n0 = len(op)
    op[:] = [l for l in op if not (('Chatter: ' in l or 'Keep up: ' in l) and 'pw.acts append value' in l)]
    assert n0 - len(op) == 4, n0 - len(op)

    # ================================================================== THE RAT BANK CARD: currencies on a page of their own
    BANK = P31.BANK
    page_code = lambda i: 4060 + i if i < 11 else 4090 + i - 11
    pcs = {page_code(i) for i in range(len(BANK))}
    d = F['p31/bank/dlg']
    sp = P260.actions(d[0])
    cur_btns = [b for b in sp[2] if P260.code_of(b) in pcs]
    rest = [b for b in sp[2] if P260.code_of(b) not in pcs]
    assert len(cur_btns) == len(BANK), len(cur_btns)
    b_cur = snbt(P28.btn([T('Currencies ›', 'gold', bold=True)], CUR, width=150, tooltip=T(f'All {len(BANK)} currencies: deposit or take out each', 'gray')))
    line = P260.set_actions(d[0], sp, [b_cur] + rest)
    names = {c: (nm, col) for c, _o, nm, col in BANK}
    summary = [T('Tokens ', names['token'][1]), T('$(token)', 'white', bold=True), T('   Lucky Tokens ', names['lucky_token'][1]), T('$(lucky_token)', 'white', bold=True),
               T('\nMedallions ', names['medallion'][1]), T('$(medallion)', 'white', bold=True), T('   Trophies ', names['trophy'][1]), T('$(trophy)', 'white', bold=True)]
    k = line.index('body:[') + len('body:[')
    line = line[:k] + snbt(P28.body(summary, 300)) + ',' + line[k:]
    d[0] = line
    back = P28.btn([T('« Your account', 'gray')], 4072, width=150)
    cd = P28.multi([T('The Rat Bank', 'gold', bold=True), T('  ·  currencies', 'gray')],
                   [P28.body([T('Pick one: deposit, take 1, take 10 or take all.', 'gray')], 300)], ['@@C@@'], columns=2)
    s_ = P28.inline(cd).replace('"@@C@@"', ','.join(cur_btns + [snbt(back)]))
    fn('p261/bank/cur_dlg', [f'$dialog show @s {s_}'])
    O = F['p31/bank/open']
    assert O[-1] == 'function bm:p31/bank/dlg with storage bm:ui bk', O[-1]
    fn('p261/bank/cur', O[:-1] + ['function bm:p261/bank/cur_dlg with storage bm:ui bk'])
    A = F['p31/bank/act']
    k = max(i for i, l in enumerate(A) if 'run return run function bm:p28/stale' in l) + 1
    A.insert(k, f'execute if score #act bm.pay matches {CUR} run return run function bm:p261/bank/cur')

    # ================================================================== THE RAID CREW: how many are on, the rules in a tooltip
    crew = F['p98/crew']
    k = crew.index('data modify storage bm:ui crew.more set value []')
    crew.insert(k + 1, 'scoreboard players set #crn bm.rng 0')
    n_on = 0
    for name in [n for n in F if n.startswith('p103/crew/row_')]:
        L = F[name]
        for i, l in enumerate(L):
            m = re.match(r'execute if (function bm:p98/on/\w+) run data modify storage bm:ui crew\.st set value \{text:"ON"', l)
            if m:
                L.insert(i + 1, f'execute if {m.group(1)} run scoreboard players add #crn bm.rng 1'); n_on += 1; break
    k = next(i for i, l in enumerate(crew) if 'crew.nmore int 1' in l)
    crew.insert(k, 'execute store result storage bm:ui crew.non int 1 run scoreboard players get #crn bm.rng')
    so = F['p103/crew/show_out']
    s0 = so[0]
    a = s0.index('body:[') + len('body:[') - 1
    b = P260._close(s0, a)
    bodies = []
    i = a + 1
    while i < b - 1:
        if s0[i] == '{':
            j = P260._close(s0, i); bodies.append(s0[i:j]); i = j
        else: i += 1
    assert len(bodies) == 3, len(bodies)
    tip = ' '.join(m.group(1) for bd in bodies[1:] for m in re.finditer(r'text:"((?:[^"\\]|\\.)*)"', bd))
    s0 = s0[:a] + '[' + bodies[0] + ']' + s0[b:]
    s0 = s0.replace('{text:"  ·  who comes into the vault with you",color:"gray",italic:false}',
                    '{text:"  ·  ",color:"gray",italic:false},{text:"$(non) on",color:"white",italic:false,bold:true},{text:" - who comes into the vault with you",color:"gray",italic:false}')
    assert '$(non) on' in s0, 'the crew page title'
    how = snbt(P28.btn([T('? How the crew works', 'gray')], 7807, width=180, tooltip=T(tip.replace('\\"', '"'), 'gray')))
    sp = P260.actions(s0)
    if sp is None:                                               # (its actions are $(acts): the button goes in with the rows)
        k = next(i for i, l in enumerate(crew) if 'function bm:p103/crew/show_in' in l)
        crew.insert(k - 1, 'execute unless entity @s[tag=bm.crmore] run data modify storage bm:ui crew.acts append value ' + how)
    so[0] = s0
    rep['crew rows counted on'] = n_on

    # ================================================================== WORDS AND TOOLTIPS on every follower's own menu
    n_w = n_t = 0
    tipped = lambda b: 'tooltip:' in b
    def tip_of(w):
        if w in ('Sit / follow', 'Wait here / follow me'): return TIP['sit']
        if P260.HOME_W.match(w): return TIP['home']
        if P260.CALL_W.match(w): return TIP['call']
        return None
    for name in [n for n, L in F.items() if any('dialog show' in l and f'/trigger bm.act set {P260.B_SET}"' in l for l in L) and not n.startswith('p99/')]:
        L = F[name]
        for j, l in enumerate(L):
            sp = P260.actions(l) if 'dialog show' in l else None
            if not sp: continue
            items = []
            for bt in sp[2]:
                w = P260.words_of(bt)
                nb = bt.replace('text:"Wait here / follow me"', 'text:"Sit / follow"').replace('text:"Call for ', 'text:"Call ')
                if w == 'Call him over': nb = nb.replace('text:"Call him over"', 'text:"Call Wilfrey over"')
                n_w += nb != bt
                t = tip_of(w)
                if t and not tipped(nb):
                    nb = '{tooltip:' + snbt(T(t, 'gray')) + ',' + nb[1:]; n_t += 1
                items.append(nb)
            L[j] = P260.set_actions(l, sp, items)
    rep['labels made one'] = n_w
    rep['tooltips added'] = n_t
    # (every page I touch closes the same way)
    for name in [n for n in F if n.startswith(('np/dlg/', 'p260/ps/dlg'))]:
        F[name] = [l.replace('exit_action:{label:"Done"}', 'exit_action:{label:"Close"}') for l in F[name]]
    return rep

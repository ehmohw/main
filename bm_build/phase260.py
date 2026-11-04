"""3.0j: THE HANDBOOK, ONE SETTINGS PAGE PER FOLLOWER, YOUR OWN SETTINGS - and the menus tidied without losing a button.

THE BLACK MARKET HANDBOOK (the Fence, 1 Token; given once to everyone on joining; or craft a book with a gold nugget) - right-click:
            a dialog that keeps track by itself, from what the pack already knows about you: FOLLOWERS met (bm:met/*, with the
            Follower Gallery's hint for the next three you haven't), BOSSES beaten and DUNGEONS & HEISTS cleared (the story
            advancements), PLACES found (the Black Market, the Gilded Gutter, the Hollow Throne, the Undercrown, the Vorn
            Armada - noted the first time you're in them - and the Loom Sanctuary, by its Keeper), and CURRENCIES: what each
            is and which traders take it (read from the trades themselves). Sneak + right-click: Your settings.
FOLLOWER SETTINGS   every follower has one Settings page (code block 6100 + 11 i, its menu the block's first code): chatter,
            keep up, back after a faint, their aura - and the switches that used to crowd their menus and wardrobes (forms,
            elements and giving them back, companion size, Ophanim, joke forms). Each of those runs exactly what its old button
            ran (a proxy: the old menu and code, through the old router). A "Settings" button (5661) takes the chatter switch's
            place on every follower's menu and wardrobe. (A "Stay here" anchor was tried and dropped: the frame gimmick - their
            item in an item frame - already stations a follower at a spot. 5662 and slot 1 of each block are free.)
YOUR SETTINGS (from the Handbook, the Partner Wheel and the Particle Toggler) - per player, each a tag on you: Music (every track
            of the pack's own - market, ships, bosses, dungeons, the vault), Market music and Ship music on their own (they
            were only the operators' switches), follower chatter (bm.hush - it always was yours alone), screen shake (the
            ground shaking under big steps and blows - it was on for everyone), keep up (bm.pwkeep, yours already), and the
            Particle Toggler's switches (np/open - already yours; linked, not copied).
THE RAID CREW PAGE   followers without a contract and hirelings not hired go to their own page ("Not signed yet", 5681): the
            crew page lists who can come - on first, then off - and the rest are one press away.

Codes: 5660-5699 (p260/act; each line checks the menu it's for), 6100-6660 (p260/fs/act -> p260/fs/r/<who>, menu-checked).
tools/menu_inventory.py checks that every function a button reached before still has a button."""
import re
import os
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, Int
import economy as ECON

ITEM = 'bm_handbook'
COL = '#e8c070'
PRICE = ('token', 1)
ECON.DIRECT[ITEM] = (PRICE, None)
HB, B_SET = 5660, 5661                                       # (the handbook's menu and "« Handbook"; Settings)
B_FOL, B_BOSS, B_DUN, B_PLC, B_CUR, B_PS = 5663, 5664, 5665, 5666, 5667, 5668
PS = 5670                                                    # (Your settings: its menu; its rows 5671-5679)
PS_ROWS = {'mus': 5671, 'mkt': 5672, 'shp': 5673, 'chat': 5674, 'shk': 5675, 'keep': 5676, 'np': 5677, 'back': 5679}
B_NPBACK, B_MORE = 5680, 5681                                # ("« Your settings" on the Particle Toggler; the crew's "Not signed yet")
FS0, FSN = 6100, 11                                          # (a follower's settings block: 6100 + 11 i .. +10)
FS_W = 200                                                   # (3.0p: a settings row's width - two columns)
S_BACK, S_KEEP, S_WD, S_PX = 0, 2, 3, 4                      # (its slots: back (and the menu), keep up, wardrobe, proxies 4..10; 1 free)
TAGS = {'mus': 'bm.nomus', 'mkt': 'bm.nomkm', 'shp': 'bm.noshp', 'shk': 'bm.noshk'}

item(ITEM, TOTEM, 'Black Market Handbook', COL,
     ['Everything you\'ve done, and what\'s left.', ('Right-click: your followers, bosses,', 'blue'), ('dungeons, places and what each', 'blue'),
      ('currency is for. It keeps itself up to date.', 'blue'), ('Sneak + right-click: your settings.', 'blue'),
      ('Lost it? A book and a gold nugget,', 'gray'), ('or a Token at the Fence\'s.', 'gray')],
     model='minecraft:book', stack=1, cat='misc', comps=hold())
HOLD[ITEM] = 'bm:p260/hb/use'
_O = {}


def extend_offers(O, offer):
    O['fence'].append(offer(PRICE, (ITEM, 1)))
    _O['O'] = O                                               # (read again in generate, once every phase has added its trades)


# ===================================================================================== SNBT surgery on dialog lines
def _close(s, i):
    """s[i] is { or [: the index just past its partner (quoted strings skipped)"""
    depth, q, j = 0, None, i
    while j < len(s):
        c = s[j]
        if q:
            if c == '\\': j += 2; continue
            if c == q: q = None
        elif c in '"\'': q = c
        elif c in '{[': depth += 1
        elif c in '}]':
            depth -= 1
            if depth == 0: return j + 1
        j += 1
    raise ValueError('unbalanced: ' + s[i:i + 80])


def actions(line):
    """(start, end, [button snbt]) of a dialog line's actions:[...] - None if it has none (or they're a macro)"""
    k = line.find('dialog show')
    if k < 0: return None
    a = line.find('actions:[', k)
    if a < 0: return None
    a += len('actions:')
    b = _close(line, a)
    inner, out, i = line[a + 1:b - 1], [], 0
    while i < len(inner):
        if inner[i] == '{':
            j = _close(inner, i); out.append(inner[i:j]); i = j
        else: i += 1
    return a, b, out


def set_actions(line, span, items):
    a, b, _ = span
    return line[:a] + '[' + ','.join(items) + ']' + line[b:]


CODE = re.compile(r'/trigger bm\.act set (\d+)')


def code_of(btn):
    m = CODE.search(btn)
    return int(m.group(1)) if m else None


def words_of(btn):
    """the words of a button's label (its text:"..." parts, up to its tooltip / action)"""
    k = btn.find('label:')
    seg = btn[k:]
    for stop in (',tooltip:', ',action:', ',width:'):
        j = seg.find(stop)
        if j > 0: seg = seg[:j]
    return re.sub(r'\s+', ' ', ''.join(m.group(1) for m in re.finditer(r'text:"((?:[^"\\]|\\.)*)"', seg))).strip()


def with_code(btn, code):
    return CODE.sub(f'/trigger bm.act set {code}', btn, count=1)


def merge_words(vs):
    """'Form: Herald (he)' / 'Form: Herald (she)' -> 'Form: Herald (he) / (she)' - one label for the variants of one button"""
    vs = list(dict.fromkeys(vs))
    if len(vs) == 1: return vs[0]
    ws = [v.split(' ') for v in vs]
    pre = 0
    while all(len(w) > pre for w in ws) and len({w[pre] for w in ws}) == 1: pre += 1
    suf = 0
    while all(len(w) > pre + suf for w in ws) and len({w[-1 - suf] for w in ws}) == 1: suf += 1
    mid = ' / '.join(' '.join(w[pre:len(w) - suf]) for w in ws)
    return ' '.join(ws[0][:pre] + [mid] + (ws[0][len(ws[0]) - suf:] if suf else []))


# (a main-menu button that's a setting - it goes to the Settings page; everything else stays where it was)
SETTING = re.compile(r'(Companion size|Ophanim|^Form\b|Form: on|form: on|Element:|^Give back|^Take back|Living / ghostly|Casual / regal|'
                     r'Gentry / chibi|Unbound / Bound|Grown / Little)')
SHORT = {'Take back the Ethereal Gem / Wraithfire Heart': 'Take back the gem / heart', 'Ethereal / Wraithfire Form: on / off': 'Ethereal / Wraithfire form'}
# (3.0p) followers met outside the roster (phase125.WHO) - their bm:met/ key: (name, colour, the Handbook's hint)
MET_EXTRA = {'escort': ('The Skiff Escort', '#9ad0ff', 'A Vorn Dreadnought\'s reactor, beaten on an invasion night.')}
WD_MOVE = ('efm', 'efg', 'pmf', 'pmg')                        # (wardrobe rows that are switches, not looks: phase99.ROWS keys)
HOME_W = re.compile(r'^Send (him|her|it|them|.+) home$')
CALL_W = re.compile(r'^(Call for|Call him over|Call )')
LAST_W = re.compile(r"(ways$|^Wardrobe$|powers$|^⚙ Settings$)")


def generate(G):
    import phase28 as P28
    import phase99 as P99
    import phase123 as P123
    import phase125 as P125
    import phase173 as P173
    import phase179 as P179
    import phase220 as P220
    import phase31 as P31
    import phase50 as P50
    import buttons as BT
    fn, title, tellraw = G.fn, G.title, G.tellraw
    F = G.FUNCS
    PRE = [T('[', 'dark_gray'), T('Black Market', 'dark_purple', bold=True), T('] ', 'dark_gray')]
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col)) if isinstance(txt, str) else title('@s', 'actionbar', txt)
    click = 'playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.4'
    WHO = P125.WHO
    WS = list(WHO)
    objs = ['bm.fsb', 'bm.psb']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    act = []                                                  # (p260/act: the 5660-5699 block)
    F['p28/act'].append(f'execute if score #act bm.pay matches {HB}..{HB + 39} run return run function bm:p260/act')
    fast, second = F['loop/fast'], F['loop/second']
    report = {}

    # ---------------------------------------------------------------- the routes of the built pack (for the proxies)
    top = [m for m in (BT.ROUTE.match(l) for l in F['p28/act']) if m]

    def router(code, menu):
        """the function p28/act hands `code` to, for a player in `menu`"""
        for m in top:
            a, dots, b, conds, rest = m.groups()
            lo = int(a) if a else -2 ** 31
            hi = (int(b) if b else 2 ** 31 - 1) if dots else lo
            if not lo <= code <= hi: continue
            mm = re.findall(r'bm\.menu matches (\d+)(?:\.\.(\d+))?', conds)
            if mm and not any(int(x) <= menu <= int(y or x) for x, y in mm): continue
            f = BT._fn_of(rest)
            if f: return f
        raise AssertionError(f'no route for {code} (menu {menu})')

    # ================================================================== which menus are whose
    pfx = {w: WHO[w][5].rsplit('/', 1)[0] + '/' for w in WS}
    pfx_more = {'emma': ['p127/em/'], 'wil': ['p173/wil/']}
    def owner(name):
        got = [w for w in WS if name.startswith(pfx[w]) or any(name.startswith(p) for p in pfx_more.get(w, ()))]
        return got[0] if len(got) == 1 else None
    MENU_SET = re.compile(r'^scoreboard players set @s bm\.menu (\d+)$')
    menu_of = lambda L: next((int(x.group(1)) for x in (MENU_SET.match(l) for l in L) if x), None)
    hits = sorted(n for n, L in F.items() if not n.startswith(('p99/', 'p119/', 'p123/', 'p179/', 'p260/', 'p259/'))
                  and any('dialog show' in l and f'/trigger bm.act set {P123.CHAT}"' in l for l in L))
    MAIN = {}                                                 # who -> {menu: open function}
    DLG = {}                                                  # who -> [dialog functions of their main menus]
    for name in hits:
        L = F[name]
        m = menu_of(L) if not any(l.startswith('$') for l in L) else None
        opener = name if m is not None else None
        if m is None:
            for caller in sorted(F):
                CL = F[caller]
                if caller.startswith(('p99/', 'p119/', 'p123/')) or any(l.startswith('$') for l in CL): continue
                if any(re.search(rf'function bm:{re.escape(name)}(\s|$)', l) for l in CL) and menu_of(CL) is not None:
                    m, opener = menu_of(CL), caller; break
        w = owner(name) or (owner(opener) if opener else None)
        assert w and m is not None, ('a follower menu nobody owns', name, opener, m)
        MAIN.setdefault(w, {}).setdefault(m, opener)
        DLG.setdefault(w, []).append(name)
    assert len(MAIN) >= 40, f'only {len(MAIN)} followers\' menus found'

    def sel_of(fn_name):
        """the tag a menu function checks its follower by (bm.<x>sel2...) - set it before calling the menu, as their item does"""
        for l in F[fn_name]:
            mm = re.search(r'@e\[type=minecraft:(?:wolf|cat),tag=(bm\.[a-z0-9_]*sel[a-z0-9_]*)\]', l)
            if mm: return mm.group(1)
        return None
    def reopen(w, opener):
        host, tag = WHO[w][3], WHO[w][4]
        s = sel_of(opener)
        if not s: return [f'function bm:{opener}']
        return ['scoreboard players operation #me bm.pid = @s bm.pid',
                f'execute as @e[type=minecraft:{host},tag={tag}] if score @s bm.pid = #me bm.pid run tag @s add {s}',
                f'function bm:{opener}', f'tag @e[tag={s}] remove {s}']
    for w, ms in MAIN.items():
        for m, opener in ms.items():
            fn(f'p260/main/{w}_{m}', reopen(w, opener))

    ORDER = list(P179.SLOTS) + [w for w in WHO if w not in P179.SLOTS]
    widx = {w: i for i, w in enumerate(WS)}
    cap = lambda s: s[0].upper() + s[1:]


    # ================================================================== THE FOLLOWERS' MENUS: settings out, Settings in
    b_set = lambda col: snbt(P28.btn([T('⚙ ', col), T('Settings', 'white', bold=True)], B_SET, width=150,
                                     tooltip=T('Their switches in one place: chatter, keep up, forms, aura...', 'gray')))
    moved = {w: {} for w in WS}                               # who -> {code: (menu, [button variants])}
    msrc = {}                                                 # (3.0p) (who, code) -> the dialog functions it was found in
    HUSH = '@s[tag=bm.hush]'
    n_lines = 0
    for w in sorted(DLG):
        col = WHO[w][2]
        for name in DLG[w]:
            L = F[name]
            m_here = menu_of(L) or next(iter(MAIN[w]))
            mm = next((mm for mm, op in MAIN[w].items() if op == name or any(f'function bm:{name}' in l for l in F[op])), m_here)
            out = []
            for l in L:
                sp = actions(l) if 'dialog show' in l else None
                if not sp or not any(code_of(b) == P123.CHAT for b in sp[2]):
                    out.append(l); continue
                items = sp[2]
                hush = HUSH in l
                keep, home_at = [], None
                for b in items:
                    c, wd = code_of(b), words_of(b)
                    if c == P123.CHAT: continue
                    if c is not None and SETTING.search(wd):
                        moved[w].setdefault(c, (mm, []))[1].append(b); msrc.setdefault((w, c), set()).add(name); continue
                    keep.append(b)
                first = [b for b in keep if HOME_W.match(words_of(b)) or CALL_W.match(words_of(b)) or words_of(b) in ('Sit / follow', 'Wait here / follow me')]
                last = [b for b in keep if LAST_W.search(words_of(b))]
                mid = [b for b in keep if b not in first and b not in last]
                if hush:
                    continue                                   # (the copy for a hushed player: the same buttons now)
                new = set_actions(l, sp, first + mid + last + [b_set(col)])
                out.append(new); n_lines += 1
            F[name][:] = out
    report['main menu lines'] = n_lines
    # (the wardrobes: their chatter switch is the Settings button now; the switches among the looks go to Settings)
    wd_rows = {w: [] for w in WS}                             # who -> [(code, button snbt)]
    for w in WS:
        if w not in P99.BASE: continue
        movec = {c for c, key, *_r in P99.ROWS.get(w, ()) if key in WD_MOVE}
        if w in P173.AR_IDX: movec.add(P173.ar_code(P173.AR_IDX[w]))
        name = f'p99/dlg/{w}'
        for j, l in enumerate(F[name]):
            sp = actions(l)
            if not sp: continue
            items = []
            for b in sp[2]:
                c = code_of(b)
                if c == P123.CHAT: items.append(b_set(WHO[w][2])); continue
                if c in movec:
                    if all(c != x for x, _b in wd_rows[w]): wd_rows[w].append((c, b))
                    continue
                if c == P99.TOP[w] and all(c != x for x, _b in wd_rows[w]): wd_rows[w].append((c, b))     # (the aura: in both)
                items.append(b)
            if not any(code_of(b) == B_SET for b in items): items.append(b_set(WHO[w][2]))
            F[name][j] = set_actions(l, sp, items)

    # (3.0p) a switch moved off a menu shown only now and then (Emma's Wraithfire menu: only while she holds the heart) is shown on
    #  the Settings page only then too - the condition its menu is opened under (scores of the player's own; anything else: always)
    GATE = re.compile(r'^execute ((?:(?:if|unless) score @s \S+ matches \S+ )+)run (?:return run )?function bm:(\S+)(?: with .*)?$')
    calls = {}                                                # (who calls whom: function -> the lines that call it)
    for caller, CL in F.items():
        if caller.startswith('p260/'): continue
        for l in CL:
            if 'function bm:' in l:
                for t in re.findall(r'function bm:([\w/.\-]+)', l):
                    calls.setdefault(t, []).append(l)
    def gate(name):
        conds = set()
        for l in calls.get(name, ()):
            mg = GATE.match(l)
            if not mg or mg.group(2) != name: return None
            conds.add(mg.group(1).strip())
        return conds.pop() if len(conds) == 1 else None
    def row_gate(w, c):
        gs = {gate(n_) for n_ in msrc.get((w, c), ())}
        return gs.pop() if len(gs) == 1 else None
    report['settings rows shown only when unlocked'] = 0

    # ================================================================== THE SETTINGS PAGE, one per follower
    fs_act = []
    froms = []
    for w in WS:
        i = widx[w]
        B = FS0 + FSN * i
        nm, pr, col, host, tag, try_, home = WHO[w]
        pi = ORDER.index(w)
        rows = []                                              # (slot, button snbt, handler lines)
        btn = lambda label, slot, tip: snbt(P28.btn(label, B + slot, width=FS_W, tooltip=T(tip, 'gray')))
        rows.append((None, snbt(P28.btn([T('Chatter: ', 'gray'), '@@RAW:r_chat@@', T('  ✦', 'dark_gray')], P123.CHAT, width=FS_W,
                                        tooltip=T('Quips and banter from all your followers - yours alone (other players choose their own).', 'gray'))), None))
        rows.append((S_KEEP, btn([T('Keep up: ', 'gray'), '@@RAW:r_keep@@', T('  ✦', 'dark_gray')], S_KEEP,
                                 'A partner left behind comes back to your side once you\'re on the ground or in water - for all your partners.'),
                     ['function bm:p179/k/toggle']))
        slot = S_PX
        prox = []
        gates = {}                                             # (3.0p) slot -> the condition it's shown under (None: always)
        for c, b in wd_rows[w]:
            prox.append((c, P99.BASE[w], re.sub(r'(?<=[{,])width:\d+', f'width:{FS_W}', with_code(b, B + slot)), slot)); slot += 1
        for c, (mm, vs) in sorted(moved[w].items()):
            wds = [words_of(v) for v in vs]
            base = vs[0]
            if len(set(wds)) > 1 or '$(' in base:
                tip = re.search(r'tooltip:(\{(?:[^{}]|\{[^{}]*\})*\})', base)
                mw = merge_words(wds)
                mw = SHORT.get(mw, mw)
                lab = snbt(P28.btn(T(mw, col, bold=True), B + slot, width=150))
                if tip and '$(' not in tip.group(1): lab = lab[:-1] + ',tooltip:' + tip.group(1) + '}'
                base = lab
            prox.append((c, mm, re.sub(r'(?<=[{,])width:\d+', f'width:{FS_W}', with_code(base, B + slot)), slot)); slot += 1      # (3.0p: every row FS_W wide - a 120 from its menu, or a look and its state, scrolled)
            gates[slot - 1] = row_gate(w, c)
        assert slot <= FSN, (w, f'{slot - S_PX} switches for the settings page - the block holds {FSN - S_PX}')
        for c, mm, b, s in prox:
            R = router(c, mm)
            rows.append((s, b, [f'scoreboard players set @s bm.menu {mm}', f'scoreboard players set #act bm.pay {c}', f'function bm:{R}']))
        rows.append((S_WD, btn([T('Wardrobe ›', col, bold=True)], S_WD, f'{nm}\'s looks.'), [f'function bm:p99/menu/{w}'] if w in P99.BASE else None))
        rows.append((S_BACK, btn([T('« Back', 'gray')], S_BACK, 'The menu you came from.'), [f'function bm:p260/fs/back/{w}']))
        report.setdefault('settings rows', 0)
        report['settings rows'] += len(rows)
        if w not in P99.BASE: rows = [r for r in rows if r[0] != S_WD]
        # the page: the wardrobe's own state (its labels read it), then ours
        st = lambda key, comp: f'data modify storage bm:ui wd.{key} set value {snbt(comp)}'
        opn = [f'function bm:p99/wdst/{w}'] if w in P99.BASE else ['data remove storage bm:ui wd']
        opn += [                st('r_chat', T('on', 'white', bold=True)), 'execute if entity @s[tag=bm.hush] run ' + st('r_chat', T('off', '#ff8a8a', bold=True)),
                st('r_keep', T('off', '#ff8a8a', bold=True)), 'execute if entity @s[tag=bm.pwkeep] run ' + st('r_keep', T('on', 'white', bold=True)),
                f'scoreboard players set @s bm.menu {B}', f'function bm:p260/fs/dlg/{w} with storage bm:ui wd']
        # (3.0p: a row shown only when unlocked - one page for each set of what's unlocked: bit j for its j-th condition)
        gl = sorted({g for s, *_r in rows for g in [gates.get(s)] if g})
        assert len(gl) <= 3, (w, gl)
        report['settings rows shown only when unlocked'] += sum(1 for s, *_r in rows if gates.get(s))
        if gl:
            opn[-1:] = ['scoreboard players set #fsv bm.rng 0'] + [f'execute {g} run scoreboard players add #fsv bm.rng {1 << j}' for j, g in enumerate(gl)] + \
                       [f'execute if score #fsv bm.rng matches {m} run return run function bm:p260/fs/dlg/{w}' + (f'_{m}' if m else '') + ' with storage bm:ui wd'
                        for m in range(1 << len(gl))]
        fn(f'p260/fs/open/{w}', opn)
        for m in range(1 << len(gl)):
            ph = {}
            acts = []
            for n_, (s, b, _h) in enumerate(rows):
                g = gates.get(s)
                if g and not m >> gl.index(g) & 1: continue
                ph[f'@@B{n_}@@'] = b; acts.append(f'@@B{n_}@@')
            d = P28.multi([T(cap(nm), col, bold=True), T('  ·  settings', 'gray')],
                          [P28.body([T('Switches for ', 'gray'), T(nm, col), T(' in one place. ', 'gray'), T('✦ = the same for all your followers.', 'dark_gray')], 300)],
                          acts, columns=2, exit_label='Close')
            s_ = snbt(d)
            for k, b in ph.items():
                s_ = s_.replace(f'"{k}"', b)
            s_ = re.sub(r'"@@RAW:(\w+)@@"', r'$(\1)', s_)
            fn(f'p260/fs/dlg/{w}' + (f'_{m}' if m else ''), [f'$dialog show @s {s_}'])
        # its router: the page's own menu, then exact codes
        lines = [f'execute unless score @s bm.menu matches {B} run return run function bm:p28/stale']
        for s, b, h in rows:
            if s is None or h is None: continue
            fn(f'p260/fs/do/{w}_{s}', h + ([f'function bm:p260/fs/open/{w}'] if s not in (S_WD, S_BACK) else []))
            lines.append(f'execute if score #act bm.pay matches {B + s} run return run function bm:p260/fs/do/{w}_{s}')
        fn(f'p260/fs/r/{w}', lines)
        fs_act.append(f'execute if score #act bm.pay matches {B}..{B + FSN - 1} run return run function bm:p260/fs/r/{w}')
        # in: from their own menu or their wardrobe (remembered, for « Back)
        srcs = dict(MAIN.get(w, {}))
        if w in P99.BASE: srcs[P99.BASE[w]] = f'p99/menu/{w}'
        for m in srcs:
            froms.append(f'execute if score @s bm.menu matches {m} run return run function bm:p260/fs/in/{w}')
        fn(f'p260/fs/in/{w}', ['scoreboard players operation @s bm.fsb = @s bm.menu', f'function bm:p260/fs/open/{w}'])
        back = [f'execute if score @s bm.fsb matches {m} run return run function bm:p260/main/{w}_{m}' for m in MAIN.get(w, {})]
        back += ([f'function bm:p99/menu/{w}'] if w in P99.BASE else [f'function bm:p260/main/{w}_{m}' for m in list(MAIN.get(w, {}))[:1]])
        fn(f'p260/fs/back/{w}', back)
    assert FS0 + FSN * len(WS) <= 6900, 'the followers\' settings blocks ran into the Particle Toggler (6900)'
    F['p28/act'].append(f'execute if score #act bm.pay matches {FS0}..{FS0 + FSN * len(WS) - 1} run return run function bm:p260/fs/act')
    fn('p260/fs/act', fs_act)
    fn('p260/fs/from', froms + ['function bm:p28/stale'])
    act.append(f'execute if score #act bm.pay matches {B_SET} run return run function bm:p260/fs/from')
    # (the wardrobe's state on its own, so the Settings page reads the same labels: the menu is "set the menu, the state, show")
    for w in P99.BASE:
        L = F[f'p99/menu/{w}']
        k = next(n for n, l in enumerate(L) if l == f'scoreboard players set @s bm.menu {P99.BASE[w]}')
        assert L[-1] == f'function bm:p99/dlg/{w} with storage bm:ui wd', (w, L[-1])
        shows = [l for l in L[:-1] if 'dialog show' in l or 'function bm:p119/dlg/' in l]      # (the Ledger's copy, shown instead - stays here)
        fn(f'p99/wdst/{w}', [l for n, l in enumerate(L[:-1]) if n != k and l not in shows])
        F[f'p99/menu/{w}'] = [L[k], f'function bm:p99/wdst/{w}'] + shows + [L[-1]]
    # (the chatter switch, pressed on a settings page, brings that page back - as on every menu it's on)
    F['p123/chat'] += [f'execute if score @s bm.menu matches {FS0 + FSN * widx[w]} run return run function bm:p260/fs/open/{w}' for w in WS] + \
        [f'execute if score @s bm.menu matches {PS} run return run function bm:p260/ps/show']
    # (keep up, switched off the wheel: only the wheel comes back)
    for k in ('p179/k/toggle', 'p179/k/off'):
        L = F[k]
        j = L.index('function bm:p179/w/open')
        L[j] = f'execute if score @s bm.menu matches {P179.WMENU} run function bm:p179/w/open'
    report['moved off the menus'] = sum(len(v) for v in moved.values())
    report['moved off the wardrobes'] = sum(1 for w in WS for c, _b in wd_rows[w] if c != P99.TOP.get(w))

    # ================================================================== THE RAID CREW PAGE: who can come, then "Not signed yet"
    crew = F['p98/crew']
    k = crew.index('data modify storage bm:ui crew.acts set value []')
    crew.insert(k + 1, 'data modify storage bm:ui crew.more set value []')
    n_more = 0
    for name in [n for n in F if n.startswith('p103/crew/row_')] + ['p103/crew/hire_rows']:
        L, out, cond = F[name], [], None
        for l in L:
            mo = re.match(r'execute if function (bm:p98/(?:signed|filed)/\w+) run data modify storage bm:ui crew\.st set value \{text:"OFF"', l)
            if mo: cond = mo.group(1)
            if l == 'data modify storage bm:ui crew.acts append from storage bm:ui crew.row':
                assert cond, ('a crew row with no contract test', name)
                out.append(f'execute unless function {cond} run return run data modify storage bm:ui crew.more append from storage bm:ui crew.row'
                           if name != 'p103/crew/hire_rows' else
                           f'execute unless function {cond} run data modify storage bm:ui crew.more append from storage bm:ui crew.row')
                if name == 'p103/crew/hire_rows':
                    out.append(f'execute if function {cond} run ' + l); cond = None; n_more += 1; continue
                n_more += 1
            out.append(l)
        F[name][:] = out
    more_btn = P28.btn([T('Not signed yet (', 'gray'), T('$(nmore)', 'white'), T(') ›', 'gray')], B_MORE, width=180,
                       tooltip=T('Followers you\'ve met without a Raid Contract, and hirelings you haven\'t hired - and where to get them.', 'gray'))
    fn('p260/crew/more_btn', [f'$data modify storage bm:ui crew.acts append value {snbt(more_btn)}'])
    k = next(n for n, l in enumerate(crew) if '"/trigger bm.act set 7950"' in l)
    crew[k:k] = ['execute store result storage bm:ui crew.nmore int 1 run data get storage bm:ui crew.more',
                 'execute if data storage bm:ui crew.more[0] run function bm:p260/crew/more_btn with storage bm:ui crew']
    k = next(n for n, l in enumerate(crew) if 'function bm:p103/crew/show_in' in l)
    crew.insert(k, 'execute if entity @s[tag=bm.crmore] run return run function bm:p260/crew/more_show')
    more = P28.multi([T('RAID CREW', '#9ad0ff', bold=True), T('  ·  not signed yet', 'gray')],
                     [P28.body([T('Met, but not on a contract yet. ', 'white'),
                                T('Followers sign on with a Raid Contract; hirelings and vault hires with theirs (used once, filed here). The Recruiter in the den sells them all.', 'gray')], 340)],
                     '@@ACTS@@', columns=2)
    fn('p260/crew/more_show', ['tag @s remove bm.crmore', 'data modify storage bm:ui crew.more append value ' +
                               snbt(P28.btn(T('« Raid Crew', 'gray'), 7807, width=180)),
                               'data modify storage bm:ui crewm.acts set from storage bm:ui crew.more',
                               'function bm:p260/crew/show_more with storage bm:ui crewm'])
    fn('p260/crew/show_more', ['$dialog show @s ' + snbt(more).replace('"@@ACTS@@"', '$(acts)')])
    fn('p260/crew/more', ['tag @s add bm.crmore', 'function bm:p98/crew', 'tag @s remove bm.crmore'])
    act.append(f'execute if score #act bm.pay matches {B_MORE} if score @s bm.menu matches 7807 run return run function bm:p260/crew/more')
    report['crew rows that move when unsigned'] = n_more

    # ================================================================== YOUR SETTINGS (per player)
    # music: every track of the pack's own answers to bm.nomus; the market's and the ships' to their own tag too
    MUS = re.compile(r'(playsound (bm:music\.[\w.]+) \w+ )(@[aspen])(\[[^\]]*\])?')
    ids, n_mus = set(), 0
    for name, L in F.items():
        for j, l in enumerate(L):
            if 'playsound bm:music.' not in l: continue
            def sub(m):
                sid = m.group(2); ids.add(sid)
                tags = ['tag=!bm.nomus'] + (['tag=!bm.nomkm'] if sid.startswith('bm:music.market_') else []) + \
                       (['tag=!bm.noshp'] if sid.startswith('bm:music.ship_') else [])
                inner = m.group(4)[1:-1] + ',' if m.group(4) else ''
                return f'{m.group(1)}{m.group(3)}[{inner}{",".join(tags)}]'
            nl = MUS.sub(sub, l)
            if nl != l: L[j] = nl; n_mus += 1
    assert n_mus >= 40, f'only {n_mus} music lines found'
    report['music lines'] = n_mus
    stop = lambda pick: [f'stopsound @s * {s}' for s in sorted(ids) if pick(s)]
    fn('p260/ps/stop_mus', stop(lambda s: True))
    fn('p260/ps/stop_mkt', stop(lambda s: s.startswith('bm:music.market_')))
    fn('p260/ps/stop_shp', stop(lambda s: s.startswith('bm:music.ship_')))
    # screen shake: yours to turn off
    F['p125/shake'].insert(0, 'execute if entity @s[tag=bm.noshk] run return run scoreboard players reset @s bm.shk')
    onoff = lambda key, on: T('on', 'white', bold=True) if on else T('off', '#ff8a8a', bold=True)
    st = lambda key, comp: f'data modify storage bm:ui ps.r_{key} set value {snbt(comp)}'
    ps_state = ['data remove storage bm:ui ps']
    for key, tg in TAGS.items():
        ps_state += [st(key, onoff(key, True)), f'execute if entity @s[tag={tg}] run ' + st(key, onoff(key, False))]
    ps_state += [st('chat', onoff('chat', True)), 'execute if entity @s[tag=bm.hush] run ' + st('chat', onoff('chat', False)),
                 st('keep', onoff('keep', False)), 'execute if entity @s[tag=bm.pwkeep] run ' + st('keep', onoff('keep', True)),
                 st('np', T('all on', 'white', bold=True)),
                 'execute if entity @s[tag=bm.np_charm] run ' + st('np', T('some off', 'gold', bold=True)),
                 'execute if entity @s[tag=bm.np_armor] run ' + st('np', T('some off', 'gold', bold=True)),
                 'execute if entity @s[tag=bm.np_weap] run ' + st('np', T('some off', 'gold', bold=True)),
                 'execute if entity @s[tag=bm.np_charm,tag=bm.np_armor,tag=bm.np_weap] run ' + st('np', T('all off', '#ff8a8a', bold=True)),
                 st('srv', T('', 'gray')),
                 'execute if score #mktmus bm.cfg matches 0 run ' + st('srv', T('\nThe server has the market music switched off for everyone.', 'dark_gray')),
                 'execute if score #shpmus bm.cfg matches 0 run ' + st('srv', T('\nThe server has the ship music switched off for everyone.', 'dark_gray')),
                 f'scoreboard players set @s bm.menu {PS}']
    rows = [('mus', [T('Music: ', 'gray'), '@@RAW:r_mus@@'], 'Every track of the Black Market\'s own: the market, the ships, the bosses, the dungeons, the vault.'),
            ('mkt', [T('Market music: ', 'gray'), '@@RAW:r_mkt@@'], 'The Black Market\'s own swing, inside a market.'),
            ('shp', [T('Ship music: ', 'gray'), '@@RAW:r_shp@@'], 'The mothership\'s and the Dreadnought\'s music, aboard.'),
            ('chat', [T('Follower chatter: ', 'gray'), '@@RAW:r_chat@@'], 'Your followers\' quips and banter.'),
            ('shk', [T('Screen shake: ', 'gray'), '@@RAW:r_shk@@'], 'The ground shaking under big steps and blows.'),
            ('keep', [T('Keep up: ', 'gray'), '@@RAW:r_keep@@'], 'A partner left behind comes back to your side once you\'re on the ground or in water.'),
            ('np', [T('Gear particles: ', 'gray'), '@@RAW:r_np@@', T(' ›', 'gray')], 'The Particle Toggler\'s switches: charms, armour, weapons, 3D wings.'),
            ('back', [T('« Back', 'gray')], 'Where you came from.')]
    d = P28.multi([T('YOUR SETTINGS', COL, bold=True), T('  ·  yours alone', 'gray')],
                  [P28.body([T('Switches for you alone - everyone else keeps their own.', 'gray'), '@@RAW:r_srv@@'], 300)],
                  [P28.btn(lab, PS_ROWS[k], width=150, tooltip=T(tip, 'gray')) for k, lab, tip in rows], columns=2, exit_label='Done')
    fn('p260/ps/dlg', [f'$dialog show @s {P28.inline(d)}'])
    fn('p260/ps/show', ps_state + ['function bm:p260/ps/dlg with storage bm:ui ps'])
    for key, tg in TAGS.items():
        nm_k = {'mus': 'Music', 'mkt': 'Market music', 'shp': 'Ship music', 'shk': 'Screen shake'}[key]
        fn(f'p260/ps/t_{key}', [f'execute if entity @s[tag={tg}] run return run function bm:p260/ps/on_{key}', f'tag @s add {tg}', click] +
           ([f'function bm:p260/ps/stop_{key}'] if key != 'shk' else ['scoreboard players reset @s bm.shk']) +
           [say([T(f'{nm_k}: ', COL, bold=True), T('off', 'red'), T(' - for you', 'gray')]), 'function bm:p260/ps/show'])
        fn(f'p260/ps/on_{key}', [f'tag @s remove {tg}', click.replace('1.4', '1.8'),
                                 say([T(f'{nm_k}: ', COL, bold=True), T('on', 'green')] + ([T(' - with the next track', 'gray')] if key != 'shk' else [])),
                                 'function bm:p260/ps/show'])
    fn('p260/ps/t_chat', ['function bm:p123/chat'])                       # (it brings this page back: see p123/chat)
    fn('p260/ps/t_keep', ['function bm:p179/k/toggle', 'function bm:p260/ps/show'])
    fn('p260/ps/t_np', ['function bm:np/open'])
    fn('p260/ps/back', ['execute if score @s bm.psb matches 2 run return run function bm:p179/w/open',
                        'execute if score @s bm.psb matches 1 run return run function bm:p260/hb/open', 'function bm:p28/stale'])
    for key, code in PS_ROWS.items():
        act.append(f'execute if score #act bm.pay matches {code} if score @s bm.menu matches {PS} run return run function bm:p260/ps/t_{key}'
                   if key != 'back' else f'execute if score #act bm.pay matches {code} if score @s bm.menu matches {PS} run return run function bm:p260/ps/back')
    fn('p260/ps/from_hb', ['scoreboard players set @s bm.psb 1', 'function bm:p260/ps/show'])
    fn('p260/ps/from_wh', ['scoreboard players set @s bm.psb 2', 'function bm:p260/ps/show'])
    act += [f'execute if score #act bm.pay matches {B_PS} if score @s bm.menu matches {HB} run return run function bm:p260/ps/from_hb',
            f'execute if score #act bm.pay matches {B_PS} if score @s bm.menu matches {P179.WMENU} run return run function bm:p260/ps/from_wh',
            f'execute if score #act bm.pay matches {B_NPBACK} if score @s bm.menu matches 6900 run return run function bm:p260/ps/show']
    # (on the wheel, beside chatter and keep up; on the Particle Toggler, the way back)
    op = F['p179/w/open']
    k = op.index('function bm:p179/w/show with storage bm:tmp pw')
    op.insert(k, 'data modify storage bm:tmp pw.acts append value ' +
              snbt(P28.btn([T('⚙ ', COL), T('Your settings', 'white')], B_PS, tooltip=T('Music, chatter, screen shake, keep up, particles - yours alone.', 'gray'))))
    npb = snbt(P28.btn([T('« Your settings', 'gray')], B_NPBACK, width=150, tooltip=T('Music, chatter, screen shake and more - yours alone.', 'gray')))
    n_np = 0
    for name in [n for n in F if n.startswith('np/dlg/')]:
        L = F[name]
        for j, l in enumerate(L):
            sp = actions(l)
            if sp: L[j] = set_actions(l, sp, sp[2] + [npb]); n_np += 1
    assert n_np == 16, n_np
    G.FUNCS['admin/uninstall'][0:0] = [f'tag @a remove {t}' for t in TAGS.values()]

    # ================================================================== THE HANDBOOK
    adv_ok = lambda a: os.path.exists(G.path('data', 'bm', 'advancement', *a.split('/')) + '.json')
    has = lambda a: f'@s[advancements={{bm:{a}=true}}]'
    MET = {w: 'met/' + P220.MET_KEY.get(w, w) for w in WS}
    for w, a in MET.items(): assert adv_ok(a), ('no met advancement', w, a)
    # (3.0p) every follower there is to meet: every bm:met/ advancement the pack has (read from what's built, so a new follower is
    #  counted the day it's added) - the roster's, and those met outside it (the Skiff Escort: eight colours, its own wheel slot)
    met_dir = G.path('data', 'bm', 'advancement', 'met')
    met_all = sorted(f[:-5] for f in os.listdir(met_dir) if f.endswith('.json'))
    extra = [k for k in met_all if 'met/' + k not in MET.values()]
    assert set(extra) <= set(MET_EXTRA), ('a bm:met/ advancement the Handbook has no name for (MET_EXTRA)', sorted(set(extra) - set(MET_EXTRA)))
    for k in extra:
        MET[k] = 'met/' + k
    FOLK = WS + extra                                          # (who the Handbook counts: len(FOLK) == every bm:met/ there is)
    fname = lambda w: WHO[w][0] if w in WHO else MET_EXTRA[w][0]
    fcol = lambda w: WHO[w][2] if w in WHO else MET_EXTRA[w][1]
    fhint = lambda w: P220.HINT[w] if w in WHO else MET_EXTRA[w][2]
    assert len(FOLK) == len(met_all), (len(FOLK), len(met_all))
    BOSSES = [('story/treant', 'The Elder Treant'), ('story/colossus', 'The Magma Colossus'), ('story/voidwalker', 'The Voidwalker'),
              ('story/horseman', 'The Headless Horseman'), ('story/pharaoh', 'The Sand Pharaoh'), ('story/storm_roc', 'The Storm Roc'),
              ('story/monstrosity', 'The Blood Moon Monstrosity'), ('story/overseer', 'A Vorn mothership\'s boss'),
              ('story/demo_duel', 'Democratus, in a duel'), ('story/tullius', 'Tullius, the Drowned Captain'),
              ('story/apophiss', 'Apophiss, the Serpent Beneath'), ('story/px_crown', 'The 8-Bit Serpent King'),
              ('story/sovereign', 'The Dread Sovereign'), ('story/sovereign_unbound', 'The Dread Sovereign, Unbound'),
              ('story/vexis', 'Admiral Vexis'), ('story/vexis_warframe', 'Admiral Vexis, the Warframe')]
    DUNGEONS = [('story/boss_brood', 'The Broodmother\'s Nest', 'the Broodmother'), ('story/boss_frost', 'The Frostbound Spire', 'the Frost Marksman'),
                ('story/boss_tide', 'The Sunken Throne', 'the Drowned Tyrant'), ('story/boss_hex', 'The Hexbound Cathedral', 'the Archmage'),
                ('story/boss_keep', 'Wilfrey\'s Keep', 'Bobbery'), ('story/boss_hollow', 'The Hollow Throne', 'the Hollow King'),
                ('story/db_shark', 'The Drowned Gate', 'the Chomping Sawshark'), ('story/db_snow', 'The Frozen Folly', 'the Malevolent Snowbeast'),
                ('story/db_witch', 'The Hexen Hollow', 'the Watchful Witch'), ('story/sovereign', 'The Undercrown', 'the Dread Sovereign'),
                ('story/vexis', 'The Vorn Armada', 'Admiral Vexis')] + \
               [(f'story/raid_t{t}', f'A Tier {r} heist', 'the Gilded Gutter Vault') for t, r in ((1, 'I'), (2, 'II'), (3, 'III'), (4, 'IV'), (5, 'V'))]
    for a, *_r in BOSSES + DUNGEONS: assert adv_ok(a), ('no such advancement', a)
    # places: noted the first time you're in one (from what the pack already knows each second: the market's, the Undercrown's
    # and the Armada's own "inside" tags, and the two worlds of its own)
    PLACES = [('bm.hb_mk', 'The Black Market', 'A market, deep under a village - a Market Key lets you in.'),
              ('bm.hb_gg', 'The Gilded Gutter', 'Behind the market\'s Gold Key gate: the den, the Fixer, the vault.'),
              ('bm.hb_ht', 'The Hollow Throne', 'Five Conquest Emblems open the Hollow Gate.'),
              ('bm.hb_uc', 'The Undercrown', 'Hard mode: deep in the Nether.'),
              ('bm.hb_ar', 'The Vorn Armada', 'Hard mode: out in the End.'),
              (None, 'The Loom Sanctuary', 'Meet every other friend - then follow the Compass of Bonds, up into the sky.')]
    second[-1:-1] = ['tag @a[tag=bm.mkhere,tag=!bm.hb_mk] add bm.hb_mk', 'tag @a[tag=bm.uin,tag=!bm.hb_uc] add bm.hb_uc',
                     'tag @a[tag=bm.ain,tag=!bm.hb_ar] add bm.hb_ar',
                     'execute as @a[tag=!bm.hb_gg] at @s if dimension bm:gutter run tag @s add bm.hb_gg',
                     'execute as @a[tag=!bm.hb_ht] at @s if dimension bm:hollow_throne run tag @s add bm.hb_ht',
                     'execute as @a[tag=!bm.hbgot] run function bm:p260/hb/first']
    place_has = lambda tg: f'@s[tag={tg}]' if tg else has(MET['keeper'])
    hbs = lambda key, comp: f'data modify storage bm:ui hb.r_{key} append value {snbt(comp)}'
    count = lambda name, conds: [f'scoreboard players set #hbn bm.rng 0'] + [f'execute if entity {c} run scoreboard players add #hbn bm.rng 1' for c in conds] + \
        [f'execute store result storage bm:ui hb.{name} int 1 run scoreboard players get #hbn bm.rng']
    sums = ['data remove storage bm:ui hb'] + count('fm', [has(MET[w]) for w in FOLK]) + count('bb', [has(a) for a, _n in BOSSES]) + \
        count('dc', [has(a) for a, *_r in DUNGEONS]) + count('pf', [place_has(tg) for tg, *_r in PLACES])
    fn('p260/hb/sums', sums)
    line = lambda lab, key, n: [T(lab, 'white'), T(f'$({key})', COL, bold=True), T(f' of {n}\n', 'gray')]
    main = P28.multi([T('BLACK MARKET HANDBOOK', COL, bold=True)],
                     [P28.body(line('Followers met: ', 'fm', len(FOLK)) + line('Bosses beaten: ', 'bb', len(BOSSES)) +
                               line('Dungeons & heists cleared: ', 'dc', len(DUNGEONS)) + line('Places found: ', 'pf', len(PLACES)) +
                               [T('It keeps itself up to date - open a page for the details.', 'dark_gray')], 300)],
                     [P28.btn([T('Followers ›', COL)], B_FOL, width=150, tooltip=T('Who you\'ve met - and where to look for the next.', 'gray')),
                      P28.btn([T('Bosses ›', COL)], B_BOSS, width=150, tooltip=T('The great foes you\'ve beaten, and the rest.', 'gray')),
                      P28.btn([T('Dungeons & heists ›', COL)], B_DUN, width=150, tooltip=T('Every dungeon cleared, every heist tier.', 'gray')),
                      P28.btn([T('Places ›', COL)], B_PLC, width=150, tooltip=T('The key places you\'ve found.', 'gray')),
                      P28.btn([T('Currencies ›', COL)], B_CUR, width=150, tooltip=T('What each currency is for - and who takes it.', 'gray')),
                      P28.btn([T('⚙ ', COL), T('Your settings', 'white')], B_PS, width=150, tooltip=T('Music, chatter, screen shake, keep up, particles - yours alone.', 'gray'))],
                     columns=2, exit_label='Close')
    fn('p260/hb/main_dlg', [f'$dialog show @s {snbt(main)}'])
    fn('p260/hb/open', ['function bm:p260/hb/sums', f'scoreboard players set @s bm.menu {HB}', 'function bm:p260/hb/main_dlg with storage bm:ui hb',
                        'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 0.8 1.1'])
    fn('p260/hb/use', ['execute if predicate bm:p20/sneaking run return run function bm:p260/ps/from_hb', 'function bm:p260/hb/open'])
    back_hb = P28.btn([T('« Handbook', 'gray')], HB, width=150)
    def page(key, titl, intro, rows_fn, extra=()):
        """a page: its list built in storage (hb.<key>), shown as one block of text"""
        d = P28.multi([T('HANDBOOK', COL, bold=True), T(f'  ·  {titl}', 'gray')],
                      [P28.body(intro, 340), P28.body('@@RAW:r_' + key + '@@', 340)] + list(extra), [back_hb], columns=1, exit_label='Close')
        fn(f'p260/hb/{key}_dlg', [f'$dialog show @s {P28.inline(d)}'])
        fn(f'p260/hb/{key}', ['function bm:p260/hb/sums', f'data modify storage bm:ui hb.r_{key} set value [{{text:""}}]'] + rows_fn() +
           [f'scoreboard players set @s bm.menu {HB}', f'function bm:p260/hb/{key}_dlg with storage bm:ui hb'])
    def fol_rows():
        L = []
        for w in FOLK:
            L.append(f'execute if entity {has(MET[w])} run ' + hbs('fol', T(f'{fname(w)}   ', fcol(w))))
        L += ['execute if score #hbn bm.rng matches 0 run ' + hbs('fol', T('(nobody yet)', 'dark_gray')),
              'data modify storage bm:ui hb.r_hint set value [{text:"Where to look next:",color:"white"}]', 'scoreboard players set #hbh bm.rng 0']
        for n, w in enumerate(FOLK):
            L.append(f'execute if score #hbh bm.rng matches ..2 unless entity {has(MET[w])} run function bm:p260/hb/hint/{w}')
            fn(f'p260/hb/hint/{w}', [hbs('hint', T(f'\n#{n + 1:02d} ??? ', '#8a8a8a', bold=True)), hbs('hint', T(fhint(w), 'gray', italic=True)),
                                     'scoreboard players add #hbh bm.rng 1'])
        L.append('execute if score #hbh bm.rng matches 0 run data modify storage bm:ui hb.r_hint set value [{text:"Every friend there is - met.",color:"gold"}]')
        return count('fm', [has(MET[w]) for w in FOLK])[:-1] + L
    page('fol', 'followers', [T('Met: ', 'white'), T('$(fm)', COL, bold=True), T(f' of {len(FOLK)}', 'gray'),
                              T('  (the Follower Gallery, on the Partner Wheel, has them all)', 'dark_gray')], fol_rows,
         extra=[P28.body('@@RAW:r_hint@@', 340)])
    def tick_rows(key, items, label):
        L = []
        for it in items:
            a = it[0]
            L += [f'execute if entity {has(a) if not a.startswith("bm.") else "@s[tag=" + a + "]"} run ' + hbs(key, T(f'✔ {label(it)}\n', '#7aff7a')),
                  f'execute unless entity {has(a) if not a.startswith("bm.") else "@s[tag=" + a + "]"} run ' + hbs(key, T(f'✘ {label(it)}\n', '#8a8a8a'))]
        return L
    page('boss', 'bosses', [T('Beaten: ', 'white'), T('$(bb)', COL, bold=True), T(f' of {len(BOSSES)}', 'gray')],
         lambda: tick_rows('boss', BOSSES, lambda it: it[1]))
    page('dun', 'dungeons & heists', [T('Cleared: ', 'white'), T('$(dc)', COL, bold=True), T(f' of {len(DUNGEONS)}', 'gray')],
         lambda: tick_rows('dun', DUNGEONS, lambda it: f'{it[1]}  ({it[2]})'))
    def plc_rows():
        L = []
        for tg, nm, hint in PLACES:
            c = place_has(tg)
            L += [f'execute if entity {c} run ' + hbs('plc', T(f'✔ {nm}\n', '#7aff7a')),
                  f'execute unless entity {c} run ' + hbs('plc', T(f'✘ {nm}', '#8a8a8a')),
                  f'execute unless entity {c} run ' + hbs('plc', T(f' - {hint}\n', 'dark_gray', italic=True))]
        return L
    page('plc', 'places', [T('Found: ', 'white'), T('$(pf)', COL, bold=True), T(f' of {len(PLACES)}', 'gray')], plc_rows)
    # currencies: what each is (its own lore), and who takes it (the trades)
    O = _O.get('O', {})
    tname = dict(P28.TRADER_NAME)
    tname.update({k: n for k, n, _w in P50.TRADERS})
    tname.update({'zorp': 'Zorp', 'dock': 'Salty Sal', 'steward': 'the Royal Steward', 'wizard': 'Cecil'})
    def takes(iid):
        who = []
        for k, offers in O.items():
            for o in offers:
                ids = [x.get('components', {}).get('minecraft:custom_data', {}).get('bm') for x in (o.get('buy', {}), o.get('buyB', {})) if isinstance(x, dict)]
                if iid in ids:
                    who.append(tname.get(k, k.replace('_', ' ').title())); break
        return who
    cur = []
    for iid, _sc, nm, colr in P31.BANK:
        lore = ITEMS[iid]['comps'].get('minecraft:lore', [])
        what = next((x['text'] for x in lore if isinstance(x, dict) and x.get('text') and not x['text'].startswith('Black Market goods')), '')
        who = takes(iid)
        cur += [T(f'{nm}', colr, bold=True), T(f' - {what}', 'gray')]
        cur += [T(f'\n   taken by: {", ".join(who[:6])}{" and more" if len(who) > 6 else ""}\n', 'dark_gray')] if who else [T('\n')]
    cur += [T('Gutter Coins, Medallions & Trophies', '#ffcf40', bold=True),
            T(' - the Gilded Gutter Vault\'s own money: kept at the Gutter Bank, spent in the Fixer\'s Office.\n', 'gray'),
            T('All of them (but the Gutter\'s) keep at the Rat Bank - the Teller, in the market.', 'dark_gray')]
    curd = P28.multi([T('HANDBOOK', COL, bold=True), T('  ·  currencies', 'gray')], [P28.body(cur, 360)], [back_hb], columns=1, exit_label='Close')
    fn('p260/hb/cur', [f'scoreboard players set @s bm.menu {HB}', f'dialog show @s {snbt(curd)}'])
    report['currencies with traders'] = sum(1 for iid, *_r in P31.BANK if takes(iid))
    act += [f'execute if score #act bm.pay matches {c} if score @s bm.menu matches {HB} run return run function bm:p260/hb/{k}'
            for c, k in ((HB, 'open'), (B_FOL, 'fol'), (B_BOSS, 'boss'), (B_DUN, 'dun'), (B_PLC, 'plc'), (B_CUR, 'cur'))]
    # easy to get: once to everyone (the next second after joining), at the Fence's, and a book with a gold nugget
    fn('p260/hb/first', ['tag @s add bm.hbgot', G.give(ITEM),
                         tellraw('@s', PRE + [T('A Black Market Handbook', COL, bold=True), T(' - right-click it: what you\'ve done, what\'s left, your settings.', 'gray')])])
    it = ITEMS[ITEM]
    G.wjson(f'bm/recipe/{ITEM}.json', {'type': 'minecraft:crafting_shapeless', 'category': 'misc', 'ingredients': ['minecraft:book', 'minecraft:gold_nugget'],
                                       'result': {'id': it['base'], 'count': 1, 'components': it['comps']}})
    G.wjson(f'bm/advancement/recipes/{ITEM}.json', {'criteria': {'book': {'trigger': 'minecraft:inventory_changed', 'conditions': {'items': [{'items': 'minecraft:book'}]}}},
                                                    'rewards': {'recipes': [f'bm:{ITEM}']}})
    G.FUNCS['admin/help'] += [tellraw('@s', [T('/function bm:admin/handbook', 'yellow'), T('  a Black Market Handbook', 'gray')])]
    fn('admin/handbook', [G.give(ITEM)])
    fn('p260/act', act + ['function bm:p28/stale'])
    return report

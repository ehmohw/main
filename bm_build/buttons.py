"""The button-code legend, BUTTON_CODES.md: every menu button and chat link that sends `/trigger bm.act set N` - its words,
where it's shown, the menu it needs, the way the routers send it - the blocks each router owns, the codes still free, what
looks wrong, a revision log (what each version added, removed or reworded) and a notes section kept as written.

Rebuilt at the end of every phase-2 build (gen_dp). On any build's output:  python3 buttons.py <BlackMarket_DP dir> <version>

How a press travels: the button runs `/trigger bm.act set N`; the tick hands every player with bm.act >= 1 to p28/act, which
copies the code into #act bm.pay and routes it - `execute if score #act bm.pay matches N(..M) run [return run] function ...`
lines, the first that returns wins - into a feature's router (p57/act, p80/act, ...), which usually checks that the player's
open menu (bm.menu) is the one with that button, then routes again or handles it. Buttons live in function lines (dialog
show, storage rows, chat links) and in dialog files (data/bm/dialog)."""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(ROOT, 'BUTTON_CODES.md')
SPAN = (1, 9999)                     # (where new codes are picked from)
ACT = re.compile(r'/trigger bm\.act set (\d+|\$\(\w+\))')
ROUTE = re.compile(r'^\$?execute if score #act bm\.pay matches (-?\d+)?(\.\.)?(-?\d+)?((?: (?!run )\S+)*) run (.*)$')
GUARD = re.compile(r'^\$?execute unless score @s bm\.menu matches (\S+) run return')
MENU_SET = re.compile(r'scoreboard players set @s bm\.menu (\d+)')
SHOW = re.compile(r'dialog show @\S+ bm:(\S+)')
NOTES0 = """- 2.75: the Gutter Bank's exchange page routed the range 7875..7883 into its own router - and with it the Fixer's Lounge
  (7880) and Skip this puzzle (7881), which sat in that block. Route exact codes; claim a range only over a block you own.
  (phase129.check now fails the build on a shadowed route.)
- 2.76: the Rat Bank's Red Xenite buttons (deposit, take 1, take 10) and the Armory's Adrenaline used codes another line
  caught first - found by the same check.
- A code may sit on buttons in several menus only when the router checks bm.menu first (the 77xx end-of-heist codes are on
  the results card and on chat links - the same action, both ways in).
- Testing: press what the client was shown (bots: `A.press(/words/)` sends that button's own command); open the menu the
  way a player does, so bm.menu is the one the router expects."""


# ===================================================================== a tolerant SNBT reader (just enough for our lines)
class _R:
    def __init__(s, t, i): s.t, s.i = t, i

    def ws(s):
        while s.i < len(s.t) and s.t[s.i] in ' \t': s.i += 1

    def val(s, parent):
        s.ws(); c = s.t[s.i]
        if c == '{': return s.comp(parent)
        if c == '[': return s.lst(parent)
        if c in '"\'': return s.string()
        return s.bare()

    def string(s):
        q = s.t[s.i]; s.i += 1; out = []
        while s.t[s.i] != q:
            if s.t[s.i] == '\\': s.i += 1
            out.append(s.t[s.i]); s.i += 1
        s.i += 1
        return ''.join(out)

    def bare(s):
        j = s.i
        while s.i < len(s.t) and s.t[s.i] not in ',}]: \t': s.i += 1
        if s.i == j: raise ValueError('empty value')
        return s.t[j:s.i]

    def comp(s, parent):
        d = {'^': parent}; s.i += 1; s.ws()
        if s.t[s.i] == '}': s.i += 1; return d
        while True:
            s.ws(); k = s.string() if s.t[s.i] in '"\'' else s.bare()
            s.ws()
            if s.t[s.i] != ':': raise ValueError('no colon')
            s.i += 1; d[k] = s.val(d); s.ws()
            if s.t[s.i] == ',': s.i += 1; continue
            if s.t[s.i] != '}': raise ValueError('no close')
            s.i += 1; return d

    def lst(s, parent):
        s.i += 1; s.ws(); out = []
        if s.t[s.i:s.i + 2] in ('I;', 'B;', 'L;'): s.i += 2; s.ws()
        if s.t[s.i] == ']': s.i += 1; return out
        while True:
            out.append(s.val(parent)); s.ws()          # (a list's items answer to the compound holding the list)
            if s.t[s.i] == ',': s.i += 1; continue
            if s.t[s.i] != ']': raise ValueError('no close')
            s.i += 1; return out


def _blobs(line):
    """every SNBT value in a command line: a { or [ that follows a space (a selector's [ never does)"""
    out, i = [], 0
    while i < len(line):
        if line[i] in '{[' and i > 0 and line[i - 1] == ' ':
            try:
                r = _R(line, i); v = r.val(None); out.append(v); i = r.i; continue
            except (ValueError, IndexError):
                pass
        i += 1
    return out


def _parent_links(v, parent=None):
    """JSON (dialog files) gets the same '^' links the SNBT reader makes"""
    if isinstance(v, dict):
        v['^'] = parent
        for k, x in list(v.items()):
            if k != '^': _parent_links(x, v)
    elif isinstance(v, list):
        for x in v: _parent_links(x, parent)
    return v


def _walk(v):
    if isinstance(v, dict):
        yield v
        for k, x in v.items():
            if k != '^': yield from _walk(x)
    elif isinstance(v, list):
        for x in v: yield from _walk(x)


def _text(c):
    """the words of a text component"""
    if isinstance(c, str): return c
    if isinstance(c, list): return ''.join(_text(x) for x in c)
    if isinstance(c, dict):
        t = c.get('text', c.get('translate', ''))
        t = _text(t) if isinstance(t, (list, dict)) else str(t)
        if 'selector' in c: t += '<' + str(c['selector']) + '>'
        return t + ''.join(_text(x) for x in c.get('extra', []))
    return ''


def _clean(s):
    return re.sub(r'\s+', ' ', s).strip()


def _same(w):
    """words as a reader compares them: letters and digits only, no case, no leading 'the'"""
    w = ' '.join(re.findall(r'[^\W_]+', w.lower()))
    return w[4:] if w.startswith('the ') else w


def _buttons_in(tree, where, menus, title=''):
    """(code, words, kind, title) for every action / click_event in a parsed value carrying /trigger bm.act set N"""
    out = []
    for d in _walk(tree):
        act = d.get('action') if isinstance(d.get('action'), dict) else d.get('click_event') if isinstance(d.get('click_event'), dict) else None
        cmd = act.get('command') if act else None
        m = ACT.search(cmd) if isinstance(cmd, str) else None
        if not m: continue
        kind = 'button' if 'label' in d else 'link'
        words = _text(d['label']) if 'label' in d else _text(d.get('text', ''))
        t, p = title, d.get('^')
        while not t and p is not None:
            if isinstance(p, dict) and 'title' in p and 'type' in p: t = _text(p['title']); break
            p = p.get('^') if isinstance(p, dict) else None
        out.append(dict(code=m.group(1), words=_clean(words) or '?', fn=where, title=_clean(t), kind=kind, menus=menus))
    return out


# ===================================================================== reading a build
def load(dp_dir):
    """every function (name -> lines) and dialog file (id -> parsed JSON) of a built datapack"""
    F, D = {}, {}
    for sub, ext, into in (('function', '.mcfunction', F), ('dialog', '.json', D)):
        base = os.path.join(dp_dir, 'data', 'bm', sub)
        for d, _, fs in os.walk(base):
            for f in fs:
                if not f.endswith(ext): continue
                p = os.path.join(d, f); key = os.path.relpath(p, base)[:-len(ext)].replace(os.sep, '/')
                with open(p, encoding='utf-8') as h:
                    into[key] = h.read().split('\n') if ext == '.mcfunction' else json.load(h)
    return F, D


def _fn_of(target):
    m = re.match(r'(?:return run )?function bm:(\S+)', target)
    return m.group(1) if m else None


def scan(F, D):
    buttons = []                     # {code, words, fn, title, kind, menus}
    own = {name: {int(x) for l in lines for x in MENU_SET.findall(l)} for name, lines in F.items()}
    callers = {}
    for name, lines in F.items():
        for l in lines:
            for c in re.findall(r'function bm:([\w/]+)', l): callers.setdefault(c, set()).add(name)

    def menus_for(name, depth=0):
        if own.get(name) or depth >= 2: return own.get(name, set())
        return set().union(*[menus_for(c, depth + 1) for c in callers.get(name, ())] or [set()])
    menus_of = {name: sorted(menus_for(name)) for name in F}
    shown_by = {}                    # dialog file -> the functions that show it
    for name in sorted(F):
        for l in F[name]:
            for did in SHOW.findall(l): shown_by.setdefault(did, set()).add(name)
            if 'bm.act set' not in l: continue
            got = []
            for blob in _blobs(l): got += _buttons_in(blob, name, menus_of[name])
            buttons += got
            left = [b['code'] for b in got]
            for c in ACT.findall(l):                     # (a code the reader couldn't place: listed all the same)
                if c in left: left.remove(c); continue
                buttons.append(dict(code=c, words='?', fn=name, title='', kind='?', menus=menus_of[name]))
    for did in sorted(D):
        tree = _parent_links(D[did])
        ms = sorted({m for f in shown_by.get(did, ()) for m in menus_of.get(f, [])})
        buttons += _buttons_in(tree, f'dialog {did}', ms, _clean(_text(tree.get('title', ''))))
    routes, guards, body = {}, {}, {}     # router -> [(lo, hi, conds, returns, rest, fn, line)]; its bm.menu guards; lines past its routes?
    for name, lines in F.items():
        for i, l in enumerate(lines):
            g = GUARD.match(l)
            if g and name not in routes: guards.setdefault(name, []).append(g.group(1))
            m = ROUTE.match(l)
            if m:
                a, dots, b, conds, rest = m.groups()
                lo = int(a) if a else -2 ** 31
                hi = (int(b) if b else 2 ** 31 - 1) if dots else lo
                routes.setdefault(name, []).append((lo, hi, conds.strip(), rest.startswith('return'), rest, _fn_of(rest), i + 1))
            elif name in routes and l.strip() and not g and not MENU_SET.search(l):
                body[name] = True                         # (a code no route takes falls through to these)
    return buttons, routes, guards, body


def path_of(routes, guards, body, code, fn='p28/act', depth=0):
    """the ways a press of `code` goes on from `fn`: a list of hop lists ([] when no line of `fn` takes it)"""
    if depth > 8: return [['…']]
    ways = []
    for lo, hi, conds, ret, rest, tfn, ln in routes.get(fn, []):
        if not lo <= code <= hi: continue
        if tfn:
            g = guards.get(tfn)
            hop = '`' + tfn + '`' + (f' [menu {g[0]}]' if g else '') + (f' (if {conds})' if conds else '')
            if tfn in routes:                                    # (another router: on through it)
                sub = path_of(routes, guards, body, code, tfn, depth + 1)
                ways += [[hop] + w for w in sub] if sub else [[hop] if body.get(tfn) else [hop, '(no line for it)']]
            else:
                ways.append([hop])
        else:
            head = rest[len('return run '):] if rest.startswith('return run ') else rest
            what = '(does nothing)' if re.fullmatch(r'return( -?\d+| fail)?', rest.strip()) else f'(inline: {head.split()[0]})' if head.split() else '(inline)'
            ways.append([what + (f' (if {conds})' if conds else '')])
        if ret and not conds: break
    return ways


# ===================================================================== the legend
def legend(F, D, version, doc=DOC):
    buttons, routes, guards, body = scan(F, D)
    by_code = {}
    for b in buttons: by_code.setdefault(b['code'], []).append(b)
    static = sorted((c for c in by_code if c.isdigit()), key=int)
    dynamic = sorted(c for c in by_code if not c.isdigit())
    top = routes.get('p28/act', [])
    rows, dead, no_line, multi = [], [], [], []
    for c in static:
        bs = by_code[c]; hops = path_of(routes, guards, body, int(c))
        if not hops: dead.append(c)
        elif any(hop == '(no line for it)' for way in hops for hop in way): no_line.append(c)
        words = sorted({b['words'] for b in bs}, key=lambda w: (_same(w), w))
        if len({_same(w) for w in words}) > 1: multi.append((c, words))
        where = sorted({b['title'] + f" ({b['fn']})" if b['title'] else b['fn'] for b in bs})
        menus = sorted({m for b in bs for m in b['menus']})
        link = all(b['kind'] == 'link' for b in bs)
        rows.append((c, ' / '.join(words), '; '.join(where[:3]) + (f' (+{len(where) - 3} more)' if len(where) > 3 else ''), ', '.join(map(str, menus)) or '—',
                     ' / '.join(' → '.join(w) for w in hops) if hops else '**not routed**', link))
    blocks = []                      # (the ranges p28/act hands whole to one router)
    for lo, hi, conds, ret, rest, tfn, ln in top:
        if lo < hi < lo + 100000:
            used = [c for c in static if lo <= int(c) <= hi]
            blocks.append((lo, hi, tfn or rest[:40], len(used), (hi - lo + 1) - len(used), (guards.get(tfn) or [''])[0] if tfn else ''))
    blocks.sort()
    taken = {int(c) for c in static}
    for lo, hi, *_ in top:
        if hi < lo + 100000: taken.update(range(max(lo, SPAN[0]), min(hi, SPAN[1]) + 1))
    free, run_ = [], None
    for n in range(SPAN[0], SPAN[1] + 2):
        if n <= SPAN[1] and n not in taken: run_ = [n, n] if run_ is None else [run_[0], n]
        elif run_: free.append(tuple(run_)); run_ = None
    menus = {}
    for name, lines in F.items():
        for l in lines:
            for x in MENU_SET.findall(l): menus.setdefault(int(x), set()).add(name)
    titles = {}
    for b in buttons:
        for m in (b['menus'] if b['title'] else ()): titles.setdefault(m, set()).add(b['title'])
    # ---- the revision log: what changed since the version before (the base: that version's last legend)
    old = open(doc, encoding='utf-8').read() if os.path.exists(doc) else ''
    md = re.search(r'<!-- legend-data (\{.*\}) -->', old, re.S)
    prev = json.loads(md.group(1)) if md else None
    sig = lambda c: f"{' / '.join(sorted({b['words'] for b in by_code[c]}))} — {', '.join(sorted({b['title'] or b['fn'] for b in by_code[c]}))}"
    now = {c: sig(c) for c in static}
    base = now if prev is None else prev['base'] if prev['version'] == version else prev['now']
    entry = []
    for c in sorted(set(base) | set(now), key=int):
        if c not in base: entry.append(f'- **{c}** added: {now[c]}')
        elif c not in now: entry.append(f'- **{c}** removed (was: {base[c]})')
        elif base[c] != now[c]: entry.append(f'- **{c}** changed: {base[c]} → {now[c]}')
    entries, order = {}, []
    lg = re.search(r'## Revision log\n(.*?)(?=\n<!-- legend-data|\Z)', old, re.S)
    for blk in re.split(r'\n(?=### )', lg.group(1).strip()) if lg else []:
        if blk.startswith('### '):
            v, _, txt = blk.partition('\n'); v = v[4:].strip(); entries[v] = txt.strip(); order.append(v)
    if prev is None: entries[version] = f'- legend started: {len(static)} codes, {len(dynamic)} built at run time'
    elif entry: entries[version] = '\n'.join(entry)
    elif not entries.get(version, '').startswith('- legend started'): entries[version] = '- no button changes'
    if version not in order: order.insert(0, version)
    nt = re.search(r'<!-- notes -->\n(.*?)\n<!-- /notes -->', old, re.S)
    notes = nt.group(1) if nt else NOTES0
    # ---- write it
    esc = lambda s: str(s).replace('|', '\\|')
    problems = [f'- **{c}** is on a button but no line of `p28/act` routes it - pressing it does nothing.' for c in dead] + \
               [f'- **{c}** reaches a router with no line for it and nothing below its routes - pressing it does nothing.' for c in no_line]
    out = [f'# Button codes (`/trigger bm.act set N`) - {version}', '',
           'Written by `buttons.py` at the end of every build (`python3 gen_dp.py --phase2`); for any build: '
           '`python3 buttons.py <BlackMarket_DP dir> <version>`. Edit only the **Notes** - they are kept as written.', '',
           f'**{len(static)} codes** on {sum(1 for b in buttons if b["code"].isdigit())} buttons and chat links ({len(dynamic)} more built at run time) · '
           f'{len(top)} routes in `p28/act` · **{sum(b - a + 1 for a, b in free)} codes free** in {SPAN[0]}-{SPAN[1]} · problems: **{len(problems)}**', '',
           '## Adding a button', '',
           "1. Pick a code: a free one inside your feature's block (**Blocks**), or a fresh run from **Free codes**.",
           "2. Route it with an exact `matches N` line - a range only over a block your router owns - and have the router check "
           "`bm.menu` (the menu that shows the button) before it acts.",
           '3. Build: phase129 refuses a shadowed route; this file rewrites itself; **Problems** should say none.',
           '4. Test by pressing the button the client was shown (bots: `A.press(/words/)` sends exactly its command).', '',
           '## Problems', ''] + (problems or ['None.']) + ['']
    if multi:
        out += ['Same code, different words (fine when each menu\'s router checks `bm.menu`): ' +
                '; '.join(f'**{c}** {" / ".join(w)}' for c, w in multi[:60]), '']
    out += ['## Blocks', '', 'Ranges `p28/act` hands whole to one router (the exact-code routes are in **All codes**).', '',
            '| Block | Router | Menu | Buttons | Free inside |', '|---|---|---|---:|---:|']
    out += [f'| {a}-{b} | `{esc(t)}` | {esc(g) or "—"} | {u} | {f} |' for a, b, t, u, f, g in blocks]
    out += ['', '## All codes', '', '"Shown in" is the dialog title (or the function, for chat links and rows built in storage); '
            '"Menu" is the `bm.menu` that function opens; the route reads `p28/act` → router [the menu it insists on] → handler.', '',
            '| Code | Words | Shown in | Menu | Route |', '|---:|---|---|---|---|']
    out += [f'| {c}{" (link)" if k else ""} | {esc(w)} | {esc(s)} | {esc(m)} | {esc(r)} |' for c, w, s, m, r, k in rows]
    out += ['', '## Built at run time', '', 'Codes a function fills in with a macro - check these by hand.', '',
            '| Code | Words | Shown in |', '|---|---|---|']
    out += [f'| `{esc(c)}` | {esc(" / ".join(sorted({b["words"] for b in by_code[c]})))} | {esc(", ".join(sorted({b["fn"] for b in by_code[c]})))} |' for c in dynamic]
    out += ['', '## Menus', '', '`scoreboard players set @s bm.menu N` - the menu a player has open; the routers check it.', '',
            '| Menu | Set by | Dialog |', '|---:|---|---|']
    out += [f'| {m} | {esc(", ".join(sorted(menus[m])[:5]) + (f" (+{len(menus[m]) - 5})" if len(menus[m]) > 5 else ""))} | '
            f'{esc(" / ".join(sorted(titles.get(m, []))[:3]))} |' for m in sorted(menus)]
    out += ['', '## Free codes', '', f'In {SPAN[0]}-{SPAN[1]}, outside every route of `p28/act` and on no button.', '',
            ', '.join(f'{a}-{b}' if b > a else f'{a}' for a, b in free), '',
            '## Notes', '', '<!-- notes -->', notes, '<!-- /notes -->', '', '## Revision log', '']
    out += [f'### {v}\n{entries[v]}\n' for v in order]
    out += ['<!-- legend-data ' + json.dumps(dict(version=version, base=base, now=now), ensure_ascii=False, sort_keys=True).replace('-->', '-- >') + ' -->', '']
    with open(doc, 'w', encoding='utf-8') as h:
        h.write('\n'.join(out))
    return dict(codes=len(static), dynamic=len(dynamic), problems=problems, changes=len(entry), checks=no_line)


def write(dp_dir, version, doc=DOC):
    F, D = load(dp_dir)
    return legend(F, D, version, doc)


if __name__ == '__main__':
    if len(sys.argv) < 3: sys.exit('usage: python3 buttons.py <BlackMarket_DP dir> <version> [BUTTON_CODES.md]')
    r = write(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else DOC)
    print(f"button legend: {r['codes']} codes, {r['dynamic']} built at run time, {len(r['problems'])} problems, {r['changes']} changes")
    for p in r['problems']: print('  ' + p)

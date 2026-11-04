"""(3.0j) THE MENU INVENTORY - every button of a built pack, what it says, where it's shown, the menu it needs and the function
its press ends in - and a check that a menu change lost nothing.

    python3 tools/menu_inventory.py [DP dir] --save FILE     write the inventory (JSON) - the baseline, before a change
    python3 tools/menu_inventory.py [DP dir] --check FILE    compare with a saved one: every function a button used to reach must
                                                             still be reached by some button (exit 1 and list them if not)
    python3 tools/menu_inventory.py [DP dir] --list [WHAT]   print the inventory (WHAT: followers / wardrobes / crew / all, or a
                                                             word of a dialog title)

The DP dir defaults to $BM_OUT/BlackMarket_DP (or out_p2/BlackMarket_DP). gen_dp runs --check against
tools/menu_baseline.json at the end of a phase-2 build when that file exists, and fails the build on a lost route.

"Reached": a function is still reached when it's the end of some button's route, or called (up to CALL_DEPTH calls down) from
one - a button moved to a Settings page that runs a small wrapper still reaches what the old button ran. The router functions
themselves (`.../act`, `p28/act`) don't count as reached; only what they route to."""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import buttons as BT                                   # (the legend's reader: the same scan, the same routes)

CALL_DEPTH = 3
BASELINE = os.path.join(ROOT, 'tools', 'menu_baseline.json')
ROUTERS = re.compile(r'(^p28/act$|/act$|/act_\d+$|/act/[\w]+$)')
# (what the owner asked to keep whole, by the menus that show the buttons: every follower's own menu and its wardrobe, the
#  wheel, the heist crew pages; the scope only sorts the report - the check covers every button of the pack)
WARDROBE_FN = re.compile(r'^p99/')


def _ends(ways):
    """the functions (and inline actions) a press ends in, one per way"""
    out = []
    for way in ways:
        fns = [re.match(r'`([^`]+)`', h).group(1) for h in way if h.startswith('`')]
        tail = way[-1] if way else ''
        if tail.startswith('(does nothing)'): out.append('(nothing)')
        elif tail.startswith('(inline'): out.append(tail.split(' (if')[0])
        elif tail == '(no line for it)': out.append('(no line)')
        elif fns: out.append(fns[-1])
    return out


def inventory(dp):
    F, D = BT.load(dp)
    buttons, routes, guards, body = BT.scan(F, D)
    rows = []
    for b in buttons:
        code = b['code']
        ways = BT.path_of(routes, guards, body, int(code)) if code.isdigit() else []
        rows.append(dict(code=code, words=b['words'], title=b['title'], fn=b['fn'], menus=b['menus'], ends=sorted(set(_ends(ways)))))
    return F, rows, (routes, guards, body)


PROXY = re.compile(r'^scoreboard players set #act bm\.pay (\d+)$')


def reached(F, rows, R):
    """every function some button's press reaches: its route's ends and what they call, CALL_DEPTH deep. A router is never
    followed by its calls (that would reach everything it routes); a proxy - `scoreboard players set #act bm.pay N` then
    `function bm:<router>` (the Settings pages' way of pressing an old button) - is followed through that router for N only."""
    routes, guards, body = R
    calls = {n: set(re.findall(r'function bm:([\w/]+)', '\n'.join(L))) for n, L in F.items()}
    seen, front = set(), {e for r in rows for e in r['ends'] if not e.startswith('(')}
    for _ in range(CALL_DEPTH + 1):
        seen |= front
        nxt = set()
        for f in front:
            L = F.get(f, ())
            codes = [int(m.group(1)) for m in (PROXY.match(l) for l in L) if m]
            for c in codes:
                for tgt in calls.get(f, ()):
                    if tgt in routes:
                        nxt |= {e for e in _ends(BT.path_of(routes, guards, body, c, tgt)) if not e.startswith('(')}
            if f not in routes:
                nxt |= calls.get(f, set()) - set(routes)
        front = nxt - seen
    return seen


def lint(dp):
    """(3.0k) the proposal's rules, as warnings: a static dialog with more than 12 buttons, one with no way out (no exit and no
    « button), a follower-menu verb without a tooltip - counts, and the worst offenders"""
    F, D = BT.load(dp)
    big, noexit, notip = [], [], 0
    for name, L in F.items():
        for l in L:
            if 'dialog show' not in l or 'multi_action' not in l: continue
            n = len(BT.ACT.findall(l))
            if n > 12 and '$(acts)' not in l: big.append((n, name))
            if 'exit_action' not in l and '\u00ab' not in l and '«' not in l: noexit.append(name)
    big.sort(reverse=True)
    return dict(over_12=len(big), worst=[f'{n} {f}' for n, f in big[:5]], no_way_out=len(set(noexit)))


def _scope(r):
    t = (r['title'] or '') + ' ' + r['fn']
    if WARDROBE_FN.match(r['fn']) or 'wardrobe' in t.lower(): return 'wardrobes'
    if re.search(r'crew|raid crew|p98/|p119/', t, re.I): return 'crew'
    return 'all'


def save(dp, path):
    F, rows, R = inventory(dp)
    ends = {}
    for r in rows:
        for e in r['ends']: ends.setdefault(e, f"{r['code']} \"{r['words']}\" ({r['title'] or r['fn']})")
    data = dict(ends=ends, buttons=len(rows))
    with open(path, 'w', encoding='utf-8') as h:
        json.dump(data, h, indent=0, ensure_ascii=False, sort_keys=True)
    return len(rows), len(ends)


def check(dp, path):
    """{old end: the old button that reached it} - every function a button used to end in that no button reaches now"""
    old = json.load(open(path, encoding='utf-8'))
    F, rows, R = inventory(dp)
    now = reached(F, rows, R)
    ends_now = {e for r in rows for e in r['ends']}
    lost = {}
    for e, was in old['ends'].items():
        if e.startswith('('):
            if e.startswith('(inline') and e not in ends_now: lost[e] = was
            continue
        if e in now or e not in F: continue              # (still reached - or gone from the pack altogether: not a menu change)
        lost[e] = was
    return lost, rows


def main(argv):
    dp = next((a for a in argv if not a.startswith('-') and os.path.isdir(a)), None) or \
        os.path.join(os.environ.get('BM_OUT', os.path.join(ROOT, 'out_p2')), 'BlackMarket_DP')
    if '--save' in argv:
        p = argv[argv.index('--save') + 1]
        n, e = save(dp, p)
        print(f'menu inventory: {n} buttons, {e} distinct ends -> {p}')
        return 0
    if '--check' in argv:
        p = argv[argv.index('--check') + 1]
        lost, rows = check(dp, p)
        print(f'menu inventory: {len(rows)} buttons now; {len(lost)} functions no button reaches any more')
        for e, was in sorted(lost.items()):
            print(f'  LOST {e}: was {was}')
        return 1 if lost else 0
    what = argv[argv.index('--list') + 1] if '--list' in argv and argv.index('--list') + 1 < len(argv) else 'all'
    F, rows, _R = inventory(dp)
    for r in sorted(rows, key=lambda r: (r['title'] or r['fn'], int(r['code']) if r['code'].isdigit() else 0)):
        if what != 'all' and _scope(r) != what and what.lower() not in (r['title'] + r['fn']).lower(): continue
        print(f"{r['code']:>5} | {r['words'][:44]:44} | {(r['title'] or r['fn'])[:40]:40} | {','.join(map(str, r['menus'])) or '-':9} | {', '.join(r['ends'])}")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

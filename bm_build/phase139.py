"""2.78: THE FIXER'S OFFICE, TIDIED - one even grid of same-sized buttons in a sensible order (Plan a Heist first, in gold),
one quiet icon colour, plain names ("Armory", not "The Armory"), and the standing card set out as two neat lines.

A last pass over the finished Office dialogs (off a heist and on one): later phases add their buttons to the dialog text
(the Lounge, the Codex, Skip this puzzle, Leave the heist), so the restyle works on what they built - every button and its
code, tooltip and command are kept; only the order, the width and the label's dress change."""
import re
from items import T
from nbt import snbt
import phase28 as P28

W = 172                                             # every button (two columns)
ICON = '#b9a57e'                                    # one muted brass for every icon
GOLD = '#ffcf40'
ORDER = ['Plan a Heist', 'Raid Crew', 'Armory', 'Gutter Bank', 'Locker Hall', 'Crate Desk', 'Trophy Case', 'Bond Sigils', 'Codex', "Fixer's Lounge"]


def split_top(s):
    """the top-level elements of an SNBT list body (no brackets): quotes and nesting respected"""
    out, depth, cur, q, esc = [], 0, [], None, False
    for ch in s:
        if q:
            cur.append(ch)
            if esc: esc = False
            elif ch == '\\': esc = True
            elif ch == q: q = None
            continue
        if ch in '"\'':
            q = ch
        elif ch in '[{':
            depth += 1
        elif ch in ']}':
            depth -= 1
        if ch == ',' and depth == 0:
            out.append(''.join(cur)); cur = []
            continue
        cur.append(ch)
    if cur:
        out.append(''.join(cur))
    return out


def span(s, key):
    """(start, end) of the list after `key:[` - end at its closing bracket"""
    i = s.index(key + ':[') + len(key) + 2
    depth, q, esc = 1, None, False
    for j in range(i, len(s)):
        ch = s[j]
        if q:
            if esc: esc = False
            elif ch == '\\': esc = True
            elif ch == q: q = None
            continue
        if ch in '"\'':
            q = ch
        elif ch in '[{':
            depth += 1
        elif ch in ']}':
            depth -= 1
            if depth == 0:
                return i, j
    raise ValueError(key)


COMP = re.compile(r'\{text:"((?:[^"\\]|\\.)*)",color:"([^"]+)"[^{}]*\}')


def restyle_button(a):
    """one button: its label re-dressed (icon in brass, name plain and bold - gold for Plan a Heist), the width even"""
    i, j = span(a, 'label')
    comps = COMP.findall(a[i:j])
    name = None
    if len(comps) >= 2 and len(comps[0][0].strip()) <= 2:
        icon, (name, col) = comps[0][0].strip(), comps[1]
        name = re.sub(r'^The ', '', name)
        if name in ORDER:
            colour = GOLD if name == 'Plan a Heist' else 'white'
            label = [T(icon + '  ', GOLD if name == 'Plan a Heist' else ICON), T(name, colour, bold=True)]
            a = a[:i] + ','.join(snbt(c) for c in label) + a[j:]
    a = re.sub(r'width:\d+', f'width:{W}', a) if 'width:' in a else a[:-1] + f',width:{W}}}'
    return name, a


def restyle(line):
    i, j = span(line, 'actions')
    acts = [restyle_button(a) for a in split_top(line[i:j])]
    known = sorted([x for x in acts if x[0] in ORDER], key=lambda x: ORDER.index(x[0]))
    rest = [x for x in acts if x[0] not in ORDER]
    line = line[:i] + ','.join(a for _n, a in known + rest) + line[j:]
    # the standing card: two lines, labels quiet, figures bright
    sep = T('    ', 'dark_gray')
    card = P28.body([T('"Sit. Here\'s where you stand."\n', '#8a7e6a', italic=True),
                     T('Gutter Bank  ', 'gray'), T('$(c)', GOLD, bold=True), T(' coins', 'gray'), sep,
                     T('Tiers cleared  ', 'gray'), T('$(clr)', 'white', bold=True), T(' / 5', 'gray'), sep,
                     T('Trophies  ', 'gray'), T('$(tro)', GOLD, bold=True),
                     T('\nKit ranks   ', 'gray'), T('Tank ', '#d06a5a'), T('$(r1)', 'white', bold=True), sep,
                     T('Offense ', '#e8955a'), T('$(r2)', 'white', bold=True), sep, T('Ranged ', '#7ad06a'), T('$(r3)', 'white', bold=True), sep,
                     T('Support ', '#7ac8e8'), T('$(r4)', 'white', bold=True), T('   (of 6)', 'dark_gray')], 380)
    bi, bj = span(line, 'body')
    old = line[bi:bj]
    assert '$(c)' in old and '$(r4)' in old, 'the Office card moved'
    first = split_top(old)
    return line[:bi] + ','.join([snbt(card)] + first[1:]) + line[bj:]


def generate(G):
    n = 0
    for name in ('p80/office_dlg', 'p104/office_dlg'):
        L = G.FUNCS[name]
        assert len(L) == 1 and L[0].startswith('$dialog show') and "THE FIXER'S OFFICE" in L[0], name
        L[0] = restyle(L[0])
        n += 1
    assert n == 2

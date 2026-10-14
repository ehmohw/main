"""2.76 (urgent): the Ledger.

'Plan a Heist' had fallen off the Office: phase117 rebuilt the Office from phase80's HUB (the copy kept for the heist
Office), which never carried it - fixed there. Here: every Ledger players already have is re-issued as the current one
(custom_data bmlv), and the build refuses to ship an Office without its planning and lounge buttons again.
"""
from items import ITEMS
import phase18 as P18
import phase80 as P80
import phase121 as P121

LV = 276


def generate(G):
    fn = G.fn
    second = []
    # ---- every Ledger out there becomes the current one (its lore, its use) - in any pocket, the off hand included
    assert ITEMS['fixers_ledger']['custom'].get('bmlv') == LV
    old = f'*[minecraft:custom_data~{{bm:"fixers_ledger"}},!minecraft:custom_data~{{bmlv:{LV}}}]'
    fn('p129/ledger/scan', [f'execute if items entity @s {slot} {old} run item modify entity @s {slot} bm:refresh/fixers_ledger' for slot, _ in P18.SLOTS])
    second += [f'execute as @a if items entity @s container.* {old} run function bm:p129/ledger/scan',
               f'execute as @a unless items entity @s container.* {old} if items entity @s weapon.offhand {old} run function bm:p129/ledger/scan']
    s_ = G.FUNCS['loop/second']; s_[-1:-1] = second

    # ---- the Office off a heist: planning on top, the lounge, everything else; the heist Office: no planning, Leave the heist
    MC = P80.MENU_CODE
    off = G.FUNCS['p80/office_dlg'][0]
    for code in (MC + 9, P121.TRIP, MC + 1, MC + 2, MC + 5):
        assert f'/trigger bm.act set {code}"' in off, f'the Office lost its button {code}'
    assert off.index(f'set {MC + 9}"') < off.index(f'set {MC + 1}"'), 'Plan a Heist heads the Office'
    hz = G.FUNCS['p104/office_dlg'][0]
    assert f'set {MC + 9}"' not in hz and f'set {P121.TRIP}"' not in hz, 'the heist Office plans nothing and goes nowhere'
    for code in (MC + 9, P121.TRIP):
        assert any(f'matches {code} run' in l for l in G.FUNCS['p80/act']), f'the Office button {code} leads nowhere'
    # ---- every end-of-heist screen offers the lounge (the cards as first shown, and as the Ledger reopens them)
    for f, code in (('p101/ask_dlg', P121.C_LEAD), ('p103/mem_dlg', P121.C_MEM), ('p101/offer', P121.C_OUT), ('p103/offer_show', P121.C_OUT)):
        assert any('dialog show' in l and f'/trigger bm.act set {code}"' in l for l in G.FUNCS[f]), f'{f}: no "Go to the Lounge" ({code})'


def check(G):
    """after every phase: no menu button is shadowed - a router line catching a code (or a range) that a later line in the
    same function was meant to handle (2.75's bank exchange caught 7875..7883 and with it the Lounge and the puzzle skip)"""
    import re
    pat = re.compile(r'^execute if score (\S+) (\S+) matches (-?\d*)(\.\.)?(-?\d*) (.*)$')
    bad = []
    for name, lines in G.FUNCS.items():
        seen = {}
        for i, l in enumerate(lines):
            m = pat.match(l)
            if not m:
                if l.startswith('scoreboard players ') and any(k[0] in l for k in seen): seen = {}       # (the score changed: start over)
                continue
            h, o, a, dots, b, rest = m.groups()
            lo = int(a) if a else -2 ** 31
            hi = (int(b) if b else 2 ** 31) if dots else lo
            caught = seen.setdefault((h, o), [])
            if hi - lo < 4096 and all(any(x <= c <= y for x, y in caught) for c in range(lo, hi + 1)):
                bad.append(f'{name}:{i + 1}: {l[:110]}')
            if rest.startswith('run return run '):
                caught.append((lo, hi))
    assert not bad, 'shadowed routes (an earlier line catches these codes first):\n  ' + '\n  '.join(bad[:40])

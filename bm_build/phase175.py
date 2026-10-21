"""2.83b: WHAT THE DEN SELLS PASSES THE COAT CHECK.

The coat check (and the Locker Hall's way back to the den) let in only the heist tools on one list (phase72's KEEP). Much
of what the den's own shopkeepers sell was never on it: seven of the eight Bond Sigils (only Mending was), the Fixer's
Lamp and Card, and Goldtooth's plain goods (golden apples, pearls, totems...). A sigil bought from Goldtooth stayed with the
Fixer at the next heist's door - and on a heist, the Locker Hall's way back to the den refused anyone carrying one ("only
heist tools go back into the vault"), so a player with no locker to put it in was stuck in the hall.

Now everything Goldtooth, the Recruiter and the Tailor sell passes, wherever the coat check stands:
  - their Black Market items by kind - read from their real stock, so whatever they sell next passes too;
  - their plain (vanilla) goods by a mark the sale puts on them ({bm_gt:1b}: the same apple from outside still waits);
  - the vault's own goods ({bm_vault:1b}, the gems) - they never leave the vault, so they're only ever bought inside.
A final pass: every coat-check selector and bag filter was built from the KEEP list; each is widened the same way."""
import re
from nbt import snbt, B

MARK = 'bm_gt'
MARKS = [f'minecraft:custom_data~{{{MARK}:1b}}', 'minecraft:custom_data~{bm_vault:1b}']
MARK_NBT = [f'{{components:{{"minecraft:custom_data":{{{MARK}:1b}}}}}}', '{components:{"minecraft:custom_data":{bm_vault:1b}}}']
CURRENCY = {'gutter_coin', 'gutter_medallion', 'gutter_trophy', 'token'}


def _bm(st):
    return (st.get('components') or {}).get('minecraft:custom_data', {}).get('bm')


def _block(s, i):
    d, q = 0, False
    for j in range(i, len(s)):
        c = s[j]
        if c == '"' and s[j - 1] != '\\':
            q = not q
        if q:
            continue
        if c == '{':
            d += 1
        elif c == '}':
            d -= 1
            if d == 0:
                return j + 1
    raise ValueError('unbalanced')


def _mark_sells(l):
    """every sell:{...} without a Black Market id gets {bm_gt:1b} in its custom data"""
    out, pos = [], 0
    for m in re.finditer(r'\bsell:\{', l):
        a = m.end() - 1
        if a < pos:
            continue
        b = _block(l, a)
        blk = l[a:b]
        if 'bm:"' not in blk and MARK not in blk:
            if '"minecraft:custom_data":{' in blk:
                blk = blk.replace('"minecraft:custom_data":{', '"minecraft:custom_data":{%s:1b,' % MARK, 1)
            elif 'components:{' in blk:
                blk = blk.replace('components:{', 'components:{"minecraft:custom_data":{%s:1b},' % MARK, 1)
            else:
                blk = blk[:-1] + ',components:{"minecraft:custom_data":{%s:1b}}}' % MARK
        out.append(l[pos:a] + blk); pos = b
    return ''.join(out) + l[pos:]


def generate(G):
    import phase70 as P70
    import phase72 as P72
    import phase103 as P103
    from items import ITEMS

    # ---- Goldtooth's plain goods carry the mark: every offer list of his in the build (the den, the Lounge), edited in place
    #      (later phases rework his summon, so it's found by its tag, not rebuilt)
    n, seen = 0, set()
    for k, L in G.FUNCS.items():
        for i, l in enumerate(L):
            if 'bm.gvgt' in l and 'Recipes' in l:
                l2 = _mark_sells(l)
                for m in re.finditer(r'\bsell:\{', l2):
                    blk = l2[m.end() - 1:_block(l2, m.end() - 1)]
                    k_ = re.search(r'bm:"([a-z0-9_]+)"', blk)
                    if k_ and 'bm_vault' not in blk:
                        seen.add(k_.group(1))
                if l2 != l:
                    L[i] = l2; n += 1
    assert n >= 2, f"Goldtooth's offers found {n} times (the den and the Lounge)"
    gtd = P70.goldtooth()

    # ---- what the three sell, by kind (the vault's own goods go by their flag instead)
    sold = set(seen)
    for o in list(gtd['Offers']['Recipes']) + list(P103.RECRUITER_OFFERS):
        k = _bm(o['sell'])
        if k and not (o['sell'].get('components') or {}).get('minecraft:custom_data', {}).get('bm_vault'):
            sold.add(k)
    sold |= {k for k in ITEMS if k.startswith('display_case')}                      # (the Tailor's cases)
    assert 'sigil_fury' in sold and 'fixers_lamp' in sold, sorted(sold)
    add = sorted(sold - set(P72.KEEP) - CURRENCY)
    KEEP = P72.KEEP
    one = lambda t: f'minecraft:custom_data~{{bm:"{t}"}}'
    any_old = '*[' + '|'.join(one(t) for t in KEEP)
    not_old = '*[' + ','.join('!' + one(t) for t in KEEP)
    any_new = any_old + ''.join('|' + one(t) for t in add) + ''.join('|' + m for m in MARKS)
    not_new = not_old + ''.join(',!' + one(t) for t in add) + ''.join(',!' + m for m in MARKS)
    rm = lambda t: f'[{{components:{{"minecraft:custom_data":{{bm:"{t}"}}}}}}]'
    na = nn = nr = 0
    pa = re.compile(re.escape(any_old) + r'(?=[\],])')
    pn = re.compile(re.escape(not_old) + r'(?=[\],])')
    for k, L in G.FUNCS.items():
        out = []
        for i, l in enumerate(L):
            l, c1 = pa.subn(any_new.replace('\\', '\\\\'), l)
            l, c2 = pn.subn(not_new.replace('\\', '\\\\'), l)
            na += c1; nn += c2
            out.append(l)
            # (a bag filter: one line per kept kind, the last kind last - the new kinds and the marks follow it)
            if rm(KEEP[-1]) in l and i > 0 and rm(KEEP[-2]) in L[i - 1]:
                out += [l.replace(rm(KEEP[-1]), rm(t)) for t in add] + [l.replace(rm(KEEP[-1]), f'[{m}]') for m in MARK_NBT]
                nr += 1
        L[:] = out
    assert na >= 5 and nn >= 4 and nr >= 2, (na, nn, nr)
    return len(add), na + nn + nr

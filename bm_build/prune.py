"""2.67: drop the functions later phases left behind.

Many phases rewrite an earlier one's feature in place (the altar in 2.35, the Lucky slot table in 2.21, the trophies in 2.66, the
frog and Donado rigs in 2.63...), and the old function bodies stayed in the pack with nothing calling them. check_xref.py lists
them; this pass removes those in the families below - only while nothing references them (a command, a macro pattern, an
advancement, a dialog or an item), repeated until nothing changes, so a chain of leftovers goes together.
2.79c: the same for data files (loot tables, item modifiers) a later phase stopped using - RETIRED_DATA, by path under data/bm/.
"""
import glob, os, re

RETIRED = [r'p21/frog/.*', r'p25/don/.*', r'p63/(don|frog)/p/.*',                    # rigs and pose x length combos never played
           r'p57/pose/(run|walk)_(a|b|up)',                                       # Emma's walk before her 2.67 stride
           r'crypt/escape_(tick|close)',                                          # (the crypt's way out stays open once the key is taken)
           r'lucky/win_medallions', r'p24/altar/sock_.*', r'p32/altar/.*', r'p29/statue/age', r'p32/crash/dep_red',
           r'p42/nova/ring_\d+', r'p59/kw/(yank|vec)', r'p71/bond_read', r'p75/trophy_again', r'p79/pet/uhit\d+',
           r'p2/[a-z]+/pz\d+_fail',
           r'p79/(boss|pet)/pose/.*', r'p88/pose/bat_roost']                         # poses a rig has but never plays (Batty is summoned roosting)
_RX = re.compile('^(?:' + '|'.join(RETIRED) + ')$')
RETIRED_DATA = [r'loot_table/gv/night_(blood|inv|lucky)',                          # (phase105 rolls the per-tier gv/<night>_t<n>)
                r'loot_table/p80/scrap1', r'loot_table/p84/supplies_(one|t\d)',     # (the Scrap Box and the supply crates moved on)
                r'item_modifier/p24/take_\d+', r'item_modifier/p32/sock_red_.*']    # (the old altar's sockets)
_RXD = re.compile('^(?:' + '|'.join(RETIRED_DATA) + ')$')


def prune(G):
    disk = []
    for f in glob.glob(G.path('data') + '/**/*.json', recursive=True):
        try: disk.append(open(f, encoding='utf-8').read())
        except (OSError, UnicodeDecodeError): pass
    disk = '\n'.join(disk)
    gone = []
    while True:
        text = '\n'.join('\n'.join(v) for v in G.FUNCS.values()) + '\n' + disk
        refs = set(re.findall(r'bm:([a-z0-9_/.\-]+)', text))
        dyn = [re.escape(r.split('$(')[0]) for r in re.findall(r'bm:([a-z0-9_/.\-]*\$\([a-z_]+\)[a-z0-9_/.\-]*)', text)]
        dyn = re.compile('^(?:' + '|'.join(dyn) + ')') if dyn else None
        drop = [n for n in G.FUNCS if _RX.match(n) and n not in refs and not (dyn and dyn.match(n))]
        if not drop: break
        for n in drop:
            del G.FUNCS[n]
            p = G.path('data', 'bm', 'function', n + '.mcfunction')
            if os.path.exists(p): os.remove(p)
        gone += drop
    # data files: a retired one goes when no function and no other data file names it
    root = G.path('data', 'bm')
    files = {os.path.relpath(f, root)[:-5].replace(os.sep, '/'): f for f in glob.glob(root + '/**/*.json', recursive=True)}
    text = '\n'.join('\n'.join(v) for v in G.FUNCS.values()) + '\n' + disk
    dyn = [re.escape(r.split('$(')[0]) for r in re.findall(r'bm:([a-z0-9_/.\-]*\$\([a-z_]+\)[a-z0-9_/.\-]*)', text)]
    for rel, f in files.items():
        kind, _, name = rel.partition('/')
        if not _RXD.match(rel) or any(re.match(d, name) for d in dyn): continue     # (a macro may build its name)
        if not re.search(r'bm:' + re.escape(name) + r'(?![a-z0-9_/.\-])', text):
            os.remove(f); gone.append(rel)
    for d, subs, fs in sorted(os.walk(root), key=lambda w: -len(w[0])):        # (and the folders that leaves empty)
        if d != root and not os.listdir(d): os.rmdir(d)
    return gone

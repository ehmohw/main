"""Usage: python3 tradediff.py <old build dir> <new build dir> [components,to,ignore]
Compare every trader's offers between two builds: report offers added/removed and changes per field."""
import sys, json, glob, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('BM_OUT', 'out')
import check262 as C
def offers(root):
    O = {}
    for f in glob.glob(root + '/BlackMarket_DP/data/bm/function/p17/npc/*.mcfunction'):
        for line in open(f, encoding='utf-8'):
            if 'Offers.Recipes set value ' in line:
                O[os.path.basename(f)[:-11]] = C.parse_snbt(line.split('Offers.Recipes set value ', 1)[1].strip(), 0)[1]
    return O
def strip(c, keys):
    c = json.loads(json.dumps(c, default=str))
    for k in ('buy', 'buyB'):
        if k in c and 'components' in c[k]:
            for kk in keys: c[k]['components'].pop(kk, None)
    return json.dumps(c, sort_keys=True, default=str)
a, b = offers(sys.argv[1]), offers(sys.argv[2])
ignore = sys.argv[3].split(',') if len(sys.argv) > 3 else []
for k in sorted(set(a) | set(b)):
    A = [strip(o, ignore) for o in a.get(k, [])]; Bv = [strip(o, ignore) for o in b.get(k, [])]
    if A == Bv: print(f'{k:12} unchanged ({len(A)} offers)'); continue
    added = [x for x in Bv if x not in A]; removed = [x for x in A if x not in Bv]
    print(f'{k:12} CHANGED: +{len(added)} -{len(removed)}')
    for x in added: print('    +', json.loads(x)['sell'].get('components', {}).get('minecraft:custom_data', json.loads(x)['sell'].get('id')))
    for x in removed: print('    -', json.loads(x)['sell'].get('components', {}).get('minecraft:custom_data', json.loads(x)['sell'].get('id')))

import sys, json, glob, os
sys.path.insert(0, '/home/claude/bm_build')
import items as I
import p2.p2items
from p2 import builds
from p2.kit import stack_nbt
DP = '/home/claude/bm_build/out_p2/BlackMarket_DP/data/bm'
B = builds()
bad = []
def fn(name): return open(f'{DP}/function/{name}.mcfunction').read()
for d, Bd in B.items():
    vs = Bd.meta['vaults']
    kinds = sorted(v[3] for v in vs)
    if kinds != sorted([f'bkey_{d}', f'vkey_{d}']): bad.append(f'{d}: vault keys {kinds}')
    for (x, y, z, key, loot, facing) in vs:
        st, nbt = Bd.b[(x, y, z)], Bd.nbt[(x, y, z)]
        want_loot = f'bm:p2/{d}/' + ('victor' if key.startswith('bkey') else 'vault')
        om = 'ominous=true' in st
        if loot != want_loot or nbt['config']['loot_table'] != want_loot: bad.append(f'{d}: {key} vault loot {loot}')
        if om != key.startswith('bkey'): bad.append(f'{d}: {key} vault ominous={om}')
        if nbt['config']['key_item'] != stack_nbt(key): bad.append(f'{d}: {key} vault key differs from the item definition')
        if nbt['config']['key_item']['components'] != I.ITEMS[key]['comps']: bad.append(f'{d}: {key} components differ')
        if not os.path.exists(f'{DP}/loot_table/p2/{d}/' + want_loot.split('/')[-1] + '.json'): bad.append(f'{d}: {want_loot} missing')
        # the patch that re-syncs vaults already in the world
        i = vs.index((x, y, z, key, loot, facing))
        if not os.path.exists(f'{DP}/function/p2/{d}/vaultfix{i}.mcfunction'): bad.append(f'{d}: no vaultfix{i}')
    # spoils key: dropped by this dungeon's trial spawners
    sp = json.load(open(f'{DP}/loot_table/p2/{d}/spawner.json'))
    if f'bm:\\"vkey_{d}\\"' not in json.dumps(sp) and f'"bm": "vkey_{d}"' not in json.dumps(sp): bad.append(f'{d}: spawner loot lacks vkey_{d}')   # 26.3: custom_data is SNBT text
    cfgs = [json.load(open(f)) for f in glob.glob(f'{DP}/trial_spawner/{d}/*.json')]
    for c in cfgs:
        if f'bm:p2/{d}/spawner' not in json.dumps(c): bad.append(f'{d}: a trial spawner config does not eject bm:p2/{d}/spawner')
    if not cfgs: bad.append(f'{d}: no trial spawner configs found')
    # victor's key: given on every boss victory
    if f'"vkey_{d}"' in fn(f'p2/{d}/credit') or f'bkey_{d}' not in fn(f'p2/{d}/credit'): bad.append(f'{d}: credit does not give bkey_{d}')
    print(f'{d}: vaults {[(v[3], "ominous" if "ominous=true" in Bd.b[v[:3]] else "regular") for v in vs]}, spawner configs {len(cfgs)}')
print('PROBLEMS:', bad or 'none')

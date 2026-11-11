"""(3.1t) writes active.json for sweep.js: every item an advancement fires on when it's used, eaten or used on a block -
from the built pack (BM_OUT, or ../../out_p2). Run after a build: python3 active_json.py"""
import glob, json, os, re
OUT = os.environ.get('BM_OUT') or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'out_p2')
DP = os.path.join(OUT, 'BlackMarket_DP', 'data', 'bm')
ids = set()
for f in glob.glob(os.path.join(DP, 'advancement', '**', '*.json'), recursive=True):
    for c in json.load(open(f)).get('criteria', {}).values():
        if c.get('trigger') in ('minecraft:using_item', 'minecraft:consume_item', 'minecraft:item_used_on_block'):
            ids |= set(re.findall(r'bm:\s*\\"([a-z0-9_]+)\\"', json.dumps(c)))
items = {os.path.basename(p)[:-5] for p in glob.glob(os.path.join(DP, 'loot_table', 'items', '*.json'))}
act = sorted(ids & items)
json.dump(act, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'active.json'), 'w'))
print(len(act), 'items')

"""Build mc263/ (same layout as mc262/) from the 26.3 server data generator output and client.jar assets."""
import json, os, glob, shutil
S = '/tmp/claude-0/-home-claude/3b068e51-eb2f-56d1-b54d-7ae7b9353a7e/scratchpad'
OLD, NEW = f'{S}/mc262', f'{S}/mc263'
REP, DATA, AST = f'{S}/gen263/out/reports', f'{S}/gen263/out/data/minecraft', f'{S}/client263/assets/minecraft'
os.makedirs(NEW, exist_ok=True)
old = json.load(open(f'{OLD}/registries.json'))
st = lambda s: s.split(':', 1)[1] if s.startswith('minecraft:') else s
reg = {}

# built-in registries
for k, v in json.load(open(f'{REP}/registries.json')).items():
    reg[st(k)] = sorted(st(e) for e in v['entries'])


def files(base, exts):
    out = []
    for f in glob.glob(f'{base}/**/*', recursive=True):
        if os.path.isfile(f) and any(f.endswith(e) for e in exts):
            r = os.path.relpath(f, base)
            out.append(r.rsplit('.', 1)[0])
    return sorted(out)


# data-driven registries + tags (vanilla data pack)
for k in old:
    if k.startswith('tag/') or k.startswith('experiment/'): continue
    d = f'{DATA}/{k}'
    if os.path.isdir(d) and k not in reg:
        reg[k] = files(d, ('.json', '.nbt'))
# any data dir not in the old list (new registries in 26.3)
for d in glob.glob(f'{DATA}/*') + glob.glob(f'{DATA}/worldgen/*'):
    k = os.path.relpath(d, DATA)
    if k in ('tags', 'worldgen', 'datapacks') or k in reg or not os.path.isdir(d): continue
    reg[k] = files(d, ('.json', '.nbt'))
tagroot = f'{DATA}/tags'
for d in glob.glob(f'{tagroot}/*') + glob.glob(f'{tagroot}/worldgen/*'):
    k = os.path.relpath(d, tagroot)
    if k == 'worldgen' or not os.path.isdir(d): continue
    reg['tag/' + k] = files(d, ('.json',))
# experiments (trade_rebalance) live under datapacks/
for k in old:
    if k.startswith('experiment/'):
        sub = k[len('experiment/'):]
        name, rest = sub.split('/', 1)
        d = f'{DATA}/datapacks/{name}/data/minecraft/{rest.replace("tag/", "tags/", 1) if rest.startswith("tag/") else rest}'
        if os.path.isdir(d): reg[k] = files(d, ('.json',))

# client assets
ASSET = {'atlas': ('atlases', '.json'), 'item_definition': ('items', '.json'), 'model': ('models', '.json'), 'texture': ('textures', '.png'),
         'font': ('font', '.json'), 'lang': ('lang', '.json'), 'post_effect': ('post_effect', '.json'), 'block_definition': ('blockstates', '.json'),
         'equipment': ('equipment', '.json')}
for k, (sub, ext) in ASSET.items():
    reg[k] = files(f'{AST}/{sub}', (ext,))
reg['structure'] = files(f'{S}/srv263/data/minecraft/structure', ('.nbt',))
reg['lang'] = sorted(set(old['lang']) | set(reg['lang']))   # client.jar only ships en_us; the rest come from the asset index
# keys we cannot rebuild from the jars (sounds index lives outside the jar; pack lists): keep 26.2
for k in old:
    if k not in reg:
        reg[k] = old[k]; print('kept 26.2 list for', k)
json.dump(reg, open(f'{NEW}/registries.json', 'w'))

# blocks.json -> {block: [{prop: [values]}, {default}]}
blocks = {}
for b, v in json.load(open(f'{REP}/blocks.json')).items():
    dflt = next((s.get('properties', {}) for s in v['states'] if s.get('default')), {})
    blocks[st(b)] = [v.get('properties', {}), dflt]
json.dump(blocks, open(f'{NEW}/blocks.json', 'w'))
shutil.copy(f'{REP}/commands.json', f'{NEW}/commands.json')
comps = {}
for f in glob.glob(f'{REP}/minecraft/components/item/*.json'):
    comps[os.path.basename(f)[:-5]] = json.load(open(f))['components']
json.dump(comps, open(f'{NEW}/item_components.json', 'w'))
# sounds: sound_event registry (sounds.json is not in client.jar); keep 26.2 sound definitions where they exist
oldsnd = json.load(open(f'{OLD}/sounds.json'))
json.dump({s: oldsnd.get(s, {}) for s in reg['sound_event']}, open(f'{NEW}/sounds.json', 'w'))
# vanilla copies used by checks
for f in glob.glob(f'{OLD}/van_*.json'):
    rel = os.path.basename(f)[4:-5]
    cands = [p for p in glob.glob(f'{DATA}/**/*.json', recursive=True)
             if os.path.relpath(p, DATA)[:-5].replace('/', '_') == rel]
    if cands: shutil.copy(cands[0], f'{NEW}/van_{rel}.json')
    else: print('no 26.3 counterpart for', rel)
for d in ('van',):
    for f in glob.glob(f'{OLD}/{d}/**/*.json', recursive=True):
        rel = os.path.relpath(f, f'{OLD}/{d}')
        src = f'{DATA}/{rel}'
        os.makedirs(os.path.dirname(f'{NEW}/{d}/{rel}'), exist_ok=True)
        if os.path.exists(src): shutil.copy(src, f'{NEW}/{d}/{rel}')
        else: print('no 26.3 counterpart for', rel)
# asset subset (elytra equipment/item/model + textures root)
os.makedirs(f'{NEW}/ast', exist_ok=True)
if not os.path.exists(f'{NEW}/ast/assets'):
    os.symlink(f'{S}/client263/assets', f'{NEW}/ast/assets')
for f in glob.glob(f'{OLD}/ast/**/*', recursive=True):
    if os.path.isfile(f) and '/assets/' not in f:
        rel = os.path.relpath(f, f'{OLD}/ast')
        src = f'{AST}/{rel}'
        os.makedirs(os.path.dirname(f'{NEW}/ast/{rel}'), exist_ok=True)
        if os.path.exists(src): shutil.copy(src, f'{NEW}/ast/{rel}')
        else: print('no 26.3 asset for', rel)

# report differences
for k in sorted(set(old) | set(reg)):
    a, b = set(old.get(k, [])), set(reg.get(k, []))
    if a != b:
        print(f'{k}: {len(a)} -> {len(b)}  removed {sorted(a - b)[:8]}{"..." if len(a - b) > 8 else ""}  added {len(b - a)}')

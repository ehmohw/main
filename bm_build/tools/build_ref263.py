"""Build the static checkers' 26.3 reference data from the jars alone (no 26.2 copy needed).

usage: python3 tools/build_ref263.py
  expects $BM_MC/server.jar and $BM_MC/client.jar (default /home/claude/mc263); runs the data generator if needed.
"""
import json, os, glob, subprocess, sys, zipfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import MC
MC = MC.rstrip('/')
JAVA = '/usr/lib/jvm/java-25-openjdk-amd64/bin/java'
GEN = f'{MC}/gen/out'
if not os.path.exists(f'{GEN}/reports/registries.json'):
    os.makedirs(f'{MC}/gen', exist_ok=True)
    subprocess.run([JAVA, '-DbundlerMainClass=net.minecraft.data.Main', '-jar', f'{MC}/server.jar', '--reports', '--server', '--output', 'out'],
                   cwd=f'{MC}/gen', check=True, stdout=subprocess.DEVNULL)
if not os.path.exists(f'{MC}/client/assets'):
    with zipfile.ZipFile(f'{MC}/client.jar') as z:
        z.extractall(f'{MC}/client', [n for n in z.namelist() if n.startswith('assets/')])
REP, DATA, AST = f'{GEN}/reports', f'{GEN}/data/minecraft', f'{MC}/client/assets/minecraft'
st = lambda s: s.split(':', 1)[1] if s.startswith('minecraft:') else s
reg = {}
for k, v in json.load(open(f'{REP}/registries.json')).items():
    reg[st(k)] = sorted(st(e) for e in v['entries'])


def files(base, exts):
    out = []
    for f in glob.glob(f'{base}/**/*', recursive=True):
        if os.path.isfile(f) and any(f.endswith(e) for e in exts):
            out.append(os.path.relpath(f, base).rsplit('.', 1)[0])
    return sorted(out)


for d in glob.glob(f'{DATA}/*') + glob.glob(f'{DATA}/worldgen/*'):
    k = os.path.relpath(d, DATA)
    if k in ('tags', 'worldgen', 'datapacks') or k in reg or not os.path.isdir(d): continue
    reg[k] = files(d, ('.json', '.nbt'))
for d in glob.glob(f'{DATA}/tags/*') + glob.glob(f'{DATA}/tags/worldgen/*'):
    k = os.path.relpath(d, f'{DATA}/tags')
    if k == 'worldgen' or not os.path.isdir(d): continue
    reg['tag/' + k] = files(d, ('.json',))
for d in glob.glob(f'{GEN}/data/minecraft/datapacks/*/data/minecraft/*'):
    name = d.split('/datapacks/')[1].split('/')[0]
    reg[f'experiment/{name}/{os.path.basename(d)}'] = files(d, ('.json',))
ASSET = {'atlas': ('atlases', '.json'), 'item_definition': ('items', '.json'), 'model': ('models', '.json'), 'texture': ('textures', '.png'),
         'font': ('font', '.json'), 'lang': ('lang', '.json'), 'post_effect': ('post_effect', '.json'), 'block_definition': ('blockstates', '.json'),
         'equipment': ('equipment', '.json')}
for k, (sub, ext) in ASSET.items():
    reg[k] = files(f'{AST}/{sub}', (ext,))
with zipfile.ZipFile(f'{MC}/server.jar') as z:     # bundled: the real jar is inside META-INF/versions
    inner = [n for n in z.namelist() if n.startswith('META-INF/versions/') and n.endswith('.jar')]
    names = zipfile.ZipFile(z.open(inner[0])).namelist() if inner else z.namelist()
reg['structure'] = sorted(n[len('data/minecraft/structure/'):-4] for n in names if n.startswith('data/minecraft/structure/') and n.endswith('.nbt'))
json.dump(reg, open(f'{MC}/registries.json', 'w'))

blocks = {}
for b, v in json.load(open(f'{REP}/blocks.json')).items():
    dflt = next((s.get('properties', {}) for s in v['states'] if s.get('default')), {})
    blocks[st(b)] = [v.get('properties', {}), dflt]
json.dump(blocks, open(f'{MC}/blocks.json', 'w'))
json.dump(json.load(open(f'{REP}/commands.json')), open(f'{MC}/commands.json', 'w'))
comps = {}
for f in glob.glob(f'{REP}/minecraft/components/item/*.json'):
    comps[os.path.basename(f)[:-5]] = json.load(open(f))['components']
json.dump(comps, open(f'{MC}/item_components.json', 'w'))
json.dump({s: {} for s in reg['sound_event']}, open(f'{MC}/sounds.json', 'w'))
os.makedirs(f'{MC}/ast', exist_ok=True)
if not os.path.exists(f'{MC}/ast/assets'): os.symlink(f'{MC}/client/assets', f'{MC}/ast/assets')
if not os.path.exists(f'{MC}/van'): os.symlink(DATA, f'{MC}/van')
print(len(reg), 'registries;', len(blocks), 'blocks;', len(comps), 'items with components')

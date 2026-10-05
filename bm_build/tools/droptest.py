"""Place every structure template with /place template (exactly like the admin commands) in the 26.3 server and record
every item that drops: anything that can't survive a block update (unsupported lanterns, torches, ...).
   python3 droptest.py build <out|out_p2>   then   gt263.sh <out> <pack> 'bm_test:*'   then   python3 droptest.py check <out>"""
import sys, os, json, glob, shutil, collections
import nbtlib
S = '/tmp/claude-0/-home-claude/3b068e51-eb2f-56d1-b54d-7ae7b9353a7e/scratchpad'
mode, OUT = sys.argv[1], sys.argv[2]
ROOT = f'/home/claude/bm_build/{OUT}/BlackMarket_DP/data'
PK = f'{S}/droptest_pack'
Y = -40
tpls = []
x = 0
for f in sorted(glob.glob(f'{ROOT}/bm/structure/**/*.nbt', recursive=True)):
    t = os.path.relpath(f, f'{ROOT}/bm/structure')[:-4]
    sx, sy, sz = map(int, nbtlib.load(f)['size'])
    tpls.append((t, x, sx, sy, sz)); x += sx + 8
if mode == 'build':
    shutil.rmtree(PK, ignore_errors=True)
    for d in ('function', 'test_environment', 'test_instance'): os.makedirs(f'{PK}/data/bm_test/{d}')
    json.dump({'pack': {'description': 'drop test', 'min_format': [121, 0], 'max_format': 121}}, open(f'{PK}/pack.mcmeta', 'w'))
    W = lambda n, l: open(f'{PK}/data/bm_test/function/{n}.mcfunction', 'w').write('\n'.join(l) + '\n')
    maxz = max(t[4] for t in tpls)
    setup = []
    for x0 in range(-16, x + 16, 256):          # forceload in strips of <=256 chunks
        setup.append(f'forceload add {x0} -16 {min(x0 + 255, x + 16)} {maxz + 16}')
    W('setup', setup + ['say DT setup'])
    go = ['say DT begin', 'data modify storage bm_test:o drops set value {}']
    for t, x0, sx, sy, sz in tpls:
        go += [f'execute unless loaded {x0} 0 0 run say DT|{t}|NOT LOADED', f'execute unless loaded {x0 + sx} 0 {sz} run say DT|{t}|NOT LOADED',
               f'place template bm:{t} {x0} {Y} 0', f'data modify storage bm_test:o drops.{t} set value []',
               f'execute as @e[type=minecraft:item,x={x0 - 2},y=-64,z=-2,dx={sx + 4},dy=200,dz={sz + 4}] run data modify storage bm_test:o drops.{t} append from entity @s {{}}',
               f'kill @e[type=minecraft:item,x={x0 - 2},y=-64,z=-2,dx={sx + 4},dy=200,dz={sz + 4}]', f'say DT|{t}|placed']
    W('go', go + ['say DT end'])
    json.dump({'type': 'minecraft:function', 'setup': 'bm_test:setup', 'teardown': 'bm_test:go'}, open(f'{PK}/data/bm_test/test_environment/main.json', 'w'))
    json.dump({'type': 'minecraft:function', 'environment': 'bm_test:main', 'function': 'minecraft:always_pass', 'max_ticks': 20,
               'setup_ticks': 300, 'structure': 'minecraft:empty', 'required': False}, open(f'{PK}/data/bm_test/test_instance/main.json', 'w'))
    print(len(tpls), 'templates laid out over', x, 'blocks')
else:
    log = open(f'{S}/gt/run.log').read()
    if 'DT end' not in log: print('✗ drop test did not finish'); sys.exit(1)
    if 'NOT LOADED' in log: print('✗ some template areas were not loaded:', [l for l in log.split('\n') if 'NOT LOADED' in l][:3])
    o = nbtlib.load(f'{S}/gt/uni/gametestworld/data/bm_test/command_storage.dat')['data']['contents']['o']['drops']
    total = 0
    for t, x0, sx, sy, sz in tpls:
        items = o.get(t, [])
        c = collections.Counter()
        where = collections.defaultdict(list)
        for e in items:
            iid = str(e['Item']['id']); c[iid] += int(e['Item'].get('count', 1))
            p = [float(v) for v in e['Pos']]; where[iid].append((int(p[0] - x0), int(p[1] - Y), int(p[2])))
        total += sum(c.values())
        print(f'{"✗" if c else "✓"} {t}: {dict(c) if c else "nothing dropped"}')
        for k, v in where.items(): print('     ', k, sorted(v)[:30])
    print(f'{total} items dropped across {len(tpls)} templates')

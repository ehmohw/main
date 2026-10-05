"""Deep compare: offers the pack writes vs offers the 26.3 server stores (from the harness' saved command storage)."""
import sys, os, re, json, glob, collections
sys.path.insert(0, '/home/claude/bm_build'); sys.path.insert(0, os.path.dirname(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else 'out'
os.environ['BM_OUT'] = OUT
import nbtlib, check262 as C
sys.argv = ['harness', 'x', OUT]
S = os.environ.get('BM_SCRATCH', '/tmp/claude-0/-home-claude/3b068e51-eb2f-56d1-b54d-7ae7b9353a7e/scratchpad')   # 2.15: set BM_SCRATCH
import importlib.util
spec = importlib.util.spec_from_file_location('h', f'{S}/harness.py'); H = importlib.util.module_from_spec(spec)
src = open(f'{S}/harness.py').read().replace("build() if mode == 'build' else check()", '')
exec(compile(src, 'harness', 'exec'), H.__dict__)


def py(t):
    if isinstance(t, nbtlib.Compound): return {k: py(v) for k, v in t.items()}
    if isinstance(t, (nbtlib.List, nbtlib.IntArray, nbtlib.ByteArray, nbtlib.LongArray)): return [py(v) for v in t]
    if isinstance(t, nbtlib.String): return str(t)
    if isinstance(t, (nbtlib.Float, nbtlib.Double)): return float(t)
    return int(t)


got = py(nbtlib.load(f'{S}/gt/uni/gametestworld/data/bm_test/command_storage.dat')['data']['contents']['o']['got'])
ROOT = H.ROOT
written = {}
for f in sorted(glob.glob(f'{ROOT}/bm/function/**/*.mcfunction', recursive=True)):
    rel = f[len(ROOT) + len('/bm/function/'):-len('.mcfunction')]
    for line in open(f).read().split('\n'):
        if 'Offers' not in line or line.startswith('$'): continue
        if 'Offers.Recipes set value ' in line:
            i = line.index('Offers.Recipes set value ') + len('Offers.Recipes set value ')
            written[rel] = C.parse_snbt(line, i)[1]
        elif 'summon ' in line:
            t, nbt = H.summon_parts(line)
            written[rel] = C.parse_snbt(nbt, 0)[1]['Offers']['Recipes']

ZERO = (0, 0.0, False, '', [], {})
pat = collections.Counter(); ex = {}


def norm(v):
    if isinstance(v, str) and re.fullmatch(r'#[0-9a-fA-F]{6}', v): return v.upper()
    if isinstance(v, bool): return int(v)
    return v


def diff(w, g, path, out):
    if isinstance(w, dict):
        if not isinstance(g, dict):
            # a plain-text component may be stored as a string
            out.append((path, 'type', w, g)); return
        for k, v in w.items():
            if k not in g:
                if v in ZERO: continue
                out.append((f'{path}.{k}', 'dropped', v, None)); continue
            diff(v, g[k], f'{path}.{k}', out)
        for k in g:
            if k not in w: out.append((f'{path}.{k}', 'added', None, g[k]))
    elif isinstance(w, list):
        if not isinstance(g, list) or len(g) != len(w): out.append((path, 'list', w, g)); return
        for i, (a, b) in enumerate(zip(w, g)): diff(a, b, f'{path}[]', out)
    else:
        a, b = norm(w), norm(g)
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            if abs(a - b) > 1e-4: out.append((path, 'value', w, g))
        elif a != b: out.append((path, 'value', w, g))


tot = 0
for n, recs in sorted(written.items()):
    g = got.get(n)
    if g is None: print('✗', n, 'not read back'); continue
    if len(g) != len(recs): print('✗', n, f'{len(recs)} -> {len(g)} recipes')
    for i, (w, gg) in enumerate(zip(recs, g)):
        tot += 1
        out = []
        diff(w, gg, 'r', out)
        for p, kind, a, b in out:
            key = (re.sub(r'\[\]', '', p), kind)
            pat[key] += 1
            ex.setdefault(key, (n, i, a, b))
print(f'{tot} recipes compared')
for (p, kind), c in pat.most_common():
    n, i, a, b = ex[(p, kind)]
    print(f'{c:4d} {kind:8s} {p}   e.g. {n}#{i}: {json.dumps(a, ensure_ascii=False)[:150]}  ->  {json.dumps(b, ensure_ascii=False)[:150]}')


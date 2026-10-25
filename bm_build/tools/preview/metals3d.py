"""2.94s: every follower's figurine in its plain look and its gilded, diamond and netherite ones (the metal looks' textures put
on the plain model - the shapes a look adds aren't shown), front-ish and three-quarter.
    python3 tools/preview/metals3d.py [out.png] [followers,comma,separated]     (needs a built out_p2 and its metal_looks.json)"""
import sys, os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [HERE, ROOT, os.path.join(ROOT, 'tools')]
from PIL import Image
from render import Scene
import draftkit as K
import gen_dp  # noqa: F401  (every phase imported: the figures' list complete)
import phase134 as P134
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(K.OUT, 'metals3d.png')
only = sys.argv[2].split(',') if len(sys.argv) > 2 else None
rp = os.path.join(ROOT, 'out_p2', 'BlackMarket_RP')
looks = json.load(open(os.path.join(ROOT, 'out_p2', 'metal_looks.json')))
by_tier = {t: sorted(n for n, x in looks.items() if x == t) for t in ('gold', 'diamond', 'netherite')}
FIG = P134.figures()
MD = os.path.join(rp, 'assets', 'bm', 'models', 'item')
MODELS = sorted(os.listdir(MD))
TEXREF = {}
for f in MODELS:
    try: TEXREF[f] = {str(v).split('/')[-1] for v in json.load(open(os.path.join(MD, f))).get('textures', {}).values()}
    except Exception: pass
tiles = []
for iid, (name, parts) in FIG.items():
    if only and name.lower() not in [o.lower() for o in only] and iid not in only: continue
    lo, h, x0, x1, z0, z1 = P134.FIT[iid]
    for t in (None, 'gold', 'diamond', 'netherite'):
        s = Scene(rp)
        if t:
            base_tex = s.texture
            def tex(tid, _b=base_tex, _t=t):
                n = tid.split('/')[-1]
                cand = [m for m in by_tier[_t] if m.startswith(n + '_')]
                return _b(tid.rsplit('/', 1)[0] + '/' + min(cand, key=len)) if cand else _b(tid)
            s.texture = tex
        for model, tr, L, R, sc in parts:
            mid = model.replace('bm:', 'bm:item/')
            if t:                                    # (the look's own model, when it has one: its fittings cast in the metal)
                base = mid.split('/')[-1]
                c = [f[:-5] for f in MODELS if f.startswith(base + '_') and any(x in TEXREF.get(f, ()) for x in by_tier[t])]
                if c: mid = 'bm:item/' + min(c, key=len)
            s.display(mid, translation=tr, scale=sc, left=L, right=R, yaw=200)
        try: im = s.render((2.2 * h * 0.6, h * 0.65, -2.6 * h), size=230, span=h * 1.25, center=(0, lo + h / 2, 0))
        except Exception as e: im = Image.new('RGBA', (230, 230), (90, 0, 0, 255))
        tiles.append(K.label(im, name, t or 'plain'))
K.sheet(tiles, out, cols=8, title='Metal looks, built in (2.94s)')
print(out)

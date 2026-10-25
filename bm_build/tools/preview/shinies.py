"""2.94t: every follower's figurine, plain beside its shiny look (shiny.py) - the look's own models where it has them, else the
plain model wearing the look's textures.     python3 tools/preview/shinies.py [out.png]   (needs a built out_p2)"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [HERE, ROOT, os.path.join(ROOT, 'tools')]
from render import Scene
import draftkit as K
import gen_dp  # noqa: F401
import phase134 as P134, phase125 as P125, phase179 as P179, shiny
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(K.OUT, 'shinies.png')
rp = os.path.join(ROOT, 'out_p2', 'BlackMarket_RP')
MD = os.path.join(rp, 'assets', 'bm', 'models', 'item'); TB = os.path.join(rp, 'assets', 'bm', 'textures', 'block')
FIG = P134.figures()
import phase137  # noqa: F401
BYNAME = {n.lower().replace('the ', ''): iid for iid, (n, _p) in FIG.items()}
ITEM = {}
for w, (nm, *_r) in P125.WHO.items():
    key = nm.lower().replace('the ', '')
    ITEM[w] = BYNAME.get(key) or next((i for n, i in BYNAME.items() if key in n or n in key), None)
tiles = []
for w, k in shiny.KEY.items():
    if w not in ITEM or ITEM[w] not in FIG: continue
    name, parts = FIG[ITEM[w]]
    lo, h, x0, x1, z0, z1 = P134.FIT[ITEM[w]]
    sufs = [f'_c{k}', f'_d{k}', f'_o{k}', f'_u{k}', f'_d{k}_m4']
    for shiny_on in (False, True):
        s = Scene(rp)
        if shiny_on:
            base_tex = s.texture
            def tex(tid, _b=base_tex):
                n = tid.split('/')[-1]
                for sf in sufs:
                    if os.path.exists(os.path.join(TB, n + sf + '.png')): return _b(tid + sf)
                return _b(tid)
            s.texture = tex
        for model, tr, L, R, sc in parts:
            mid = model.replace('bm:', 'bm:item/')
            if shiny_on:
                for sf in sufs:
                    if os.path.exists(os.path.join(MD, mid.split('/')[-1] + sf + '.json')): mid += sf; break
            s.display(mid, translation=tr, scale=sc, left=L, right=R, yaw=200)
        im = s.render((1.3 * h, h * 0.65, -2.6 * h), size=200, span=h * 1.25, center=(0, lo + h / 2, 0))
        tiles.append(K.label(im, name, shiny.LOOKS.get(w, (shiny.KW[0] if w == 'kw' else {'emma': shiny.EMMA, 'celi': shiny.CELI, 'zib': shiny.ZIB}.get(w, ('',))[0],))[0] if shiny_on else 'plain'))
K.sheet(tiles, out, cols=8, title='Shiny followers (2.94t)')
print(out)

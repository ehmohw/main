"""The Keeper of Bonds' preview sheets (rigkit).  python3 tools/preview/keeper.py [lineup,poses,faces,items,doll,sanctuary,clip,fit]
Writes to $BM_PREVIEW_DIR (default: previews/v300_keeper). The dark tile: tools/render has no light, so each face is tinted after
the scene is built - unlit faces dimmed to night, faces of elements with light_emission kept bright in proportion to their level
(as tools/preview/pale_dryad.py does it). 'clip' prints, per pose, every pair of parts whose boxes cut into each other beyond
the joints meant to meet, and how far its lowest point is off the floor. 'fit' measures phase134's FIT for the display case."""
import sys, os, json, math, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM)
os.environ.setdefault('BM_PREVIEW_DIR', os.path.join(os.path.dirname(BM), 'previews', 'v300_keeper'))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import draftkit as K, keeper_art as A, rigkit
from tools import render as R
OUT = os.environ['BM_PREVIEW_DIR']; os.makedirs(OUT, exist_ok=True)
SCRATCH = os.environ.get('BM_SCRATCH', '/tmp/bm_previews')
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['lineup', 'poses', 'faces', 'items', 'doll', 'sanctuary', 'clip']
ROOT = K.pack(A, f'{SCRATCH}/rp_kb')
I = A.POSES['idle_a']
NIGHT_BG, NIGHT_GRID = (16, 18, 34), (34, 38, 52)


def tile(pose, view=(-30, 10), span=3.0, center=(0, 1.25, 0), size=360, label='', sub=None, night=False):
    s = night_scene() if night else K.multi_scene(ROOT)
    rigkit.render(s, A, pose, scale=A.RIG_SCALE)
    im = s.render(view, size=size, span=span, center=center)
    if night: im = darken(im)
    return dark_label(im, label, sub) if night else K.label(im, label, sub)


def night_scene(*roots):
    """a Scene whose display() tints every face by its element's light_emission (dim night when 0)"""
    s = K.multi_scene(*(roots or (ROOT,))); base = s.display

    def display(mid, **kw):
        n0 = len(s.faces); base(mid, **kw)
        lights = [e.get('light_emission', 0) for e in s.model(mid).get('elements', []) for _ in e.get('faces', {})]
        for i, L in enumerate(lights):
            f = s.faces[n0 + i]
            k = 0.22 + 0.78 * (L / 15) ** 0.8 if L else None
            tint = np.array([0.16, 0.17, 0.27]) if not L else np.array([k, k * 0.98, k * 0.92])
            s.faces[n0 + i] = (f[0], f[1], f[2], False if L else f[3], tint)
    s.display = display

    def solid(lo, hi, color='#c08060'):                     # (a player in the dark: moonlit)
        c = tuple(int(int(color[i:i + 2], 16) * 0.22) for i in (1, 3, 5))
        R.Scene.solid(s, lo, hi, '#%02x%02x%02x' % c)
    s.solid = solid
    return s


def darken(im):
    a = np.asarray(im).astype(np.float32)
    sky = (np.abs(a - np.array([199, 219, 242])).sum(axis=2) < 8)
    grid = (np.abs(a - np.array([140, 158, 140])).sum(axis=2) < 10) | (np.abs(a - np.array([51, 127, 51])).sum(axis=2) < 10)
    a[sky] = NIGHT_BG; a[grid] = NIGHT_GRID
    return Image.fromarray(a.astype(np.uint8))


def font(sz, bold=True):
    try: return ImageFont.truetype(f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if bold else ""}.ttf', sz)
    except OSError: return None


def dark_label(im, text, sub=None):
    d = ImageDraw.Draw(im); d.text((8, 6), text, fill=(235, 228, 210), font=font(15))
    if sub: d.text((8, 25), sub, fill=(170, 170, 190), font=font(12, False))
    return im


# ---------------------------------------------------------------------------------------------------- clipping, floor, fit
class _Rec:
    def __init__(self): self.d = []
    def display(self, mid, pos, yaw, translation, scale, left): self.d.append((mid, pos, yaw, translation, scale, left))


def boxes(pose):
    rec = _Rec(); rigkit.render(rec, A, pose, scale=A.RIG_SCALE)
    out = []
    for (mid, pos, yaw, tr, sc, left), p in zip(rec.d, [p for p in A.PARTS if not A.HIDDEN(p, pose)]):
        m = json.load(open(f'{ROOT}/assets/bm/models/item/{mid.split("/")[-1]}.json'))
        Q = R.quat(left); E = R.ry(math.radians(-yaw))
        for e in m['elements']:
            f, t = e['from'], e['to']
            cs = [np.array((x, y, z), float) for x in (f[0], t[0]) for y in (f[1], t[1]) for z in (f[2], t[2])]
            r = e.get('rotation')
            if r:
                o = np.array(r['origin'])
                M = {'x': R.rx, 'y': R.ry, 'z': R.rz}[r['axis']](math.radians(r['angle'])) if 'axis' in r else \
                    R.rz(math.radians(r.get('z', 0))) @ R.ry(math.radians(r.get('y', 0))) @ R.rx(math.radians(r.get('x', 0)))
                cs = [M @ (c - o) + o for c in cs]
            w = [E @ (Q @ (sc * (R.ry(math.pi) @ (c / 16 - 0.5))) + np.array(tr)) + np.array(pos) for c in cs]
            out.append((p, np.array(w), e))
    return out


def _sat(a, b):
    def axes(c): return [c[4] - c[0], c[2] - c[0], c[1] - c[0]]
    ax = [v for v in axes(a) + axes(b) if np.linalg.norm(v) > 1e-6]
    for u, v in itertools.product(axes(a), axes(b)):
        x = np.cross(u, v)
        if np.linalg.norm(x) > 1e-6: ax.append(x)
    depth = 1e9
    for v in ax:
        v = v / np.linalg.norm(v); pa, pb = a @ v, b @ v
        d = min(pa.max(), pb.max()) - max(pa.min(), pb.min())
        if d <= 0: return 0.0
        depth = min(depth, d)
    return depth


MEET = {frozenset(p) for p in [('body', 'head'), ('body', 'armr'), ('body', 'arml'), ('armr', 'forer'), ('arml', 'forel'), ('forer', 'threadr'),
                               ('forel', 'threadl'), ('body', 'skirt'), ('body', 'loom'), ('body', 'pool'), ('skirt', 'pool')]}
FREE = ('motes', 'motesb', 'web')            # (the orbit and the web pass through and round it: light, not cloth)


def clip_report(names, tol=0.2):
    lines, U = [], A.RIG_SCALE / 16
    for n in names:
        pose = A.POSES[n]; bx = boxes(pose); hits = {}
        for (pa, ca, ea), (pb, cb, eb) in itertools.combinations(bx, 2):
            if pa == pb or frozenset((pa, pb)) in MEET or pa in FREE or pb in FREE: continue
            d = _sat(ca, cb) / U
            if d > tol:
                k = tuple(sorted((pa, pb))); hits[k] = max(hits.get(k, 0), d)
        low = min(c[:, 1].min() for p, c, e in bx if p not in ('pool',)) / U
        lines.append(f'{n:12s} floor {low:+6.2f}  ' + ('  '.join(f'{a}/{b} {d:.2f}' for (a, b), d in sorted(hits.items())) or 'clean'))
    return lines


def fit():
    """phase134.FIT for the Keeper: (lowest y, height, x0, x1, z0, z1) in blocks, idle_a at RIG_SCALE"""
    s = K.multi_scene(ROOT)
    rigkit.render(s, A, I, scale=A.RIG_SCALE)
    pts = np.array([v for f in s.faces for v in f[0]])
    lo, hi = pts.min(0), pts.max(0)
    return (round(lo[1], 3), round(hi[1] - lo[1], 3), round(lo[0], 3), round(hi[0], 3), round(lo[2], 3), round(hi[2], 3))


# ---------------------------------------------------------------------------------------------------- sheets
if 'lineup' in what:
    tiles = []
    for v, l in (('front', 'front'), ((-38, 10), 'three-quarter'), ('back', 'back')):
        s = K.multi_scene(ROOT); rigkit.render(s, A, I, scale=A.RIG_SCALE); K.person(s, (1.15, 0, 0.1))
        tiles.append(K.label(s.render(v, size=440, span=3.3, center=(0.5, 1.3, 0)), l, 'beside a player (1.8)'))
    s = night_scene(); rigkit.render(s, A, A.POSES['idle_b'], scale=A.RIG_SCALE); K.person(s, (1.15, 0, 0.1))
    tiles.append(dark_label(darken(s.render((-30, 14), size=440, span=3.3, center=(0.5, 1.3, 0))), 'at night', 'its glow, and the 49 bonds round it'))
    K.sheet(tiles, OUT + '/keeper_lineup.png', cols=4, title='The Keeper of Bonds - front, three-quarter, back, and by night (idle)')
    s = night_scene(); rigkit.render(s, A, A.POSES['weave'], scale=A.RIG_SCALE)
    t2 = [dark_label(darken(s.render((-20, 18), size=440, span=3.6, center=(0, 1.4, 0))), 'by night: the weave', 'the web of every bond between its hands')]
    s = night_scene(); rigkit.render(s, A, I, scale=A.RIG_SCALE)
    t2.append(dark_label(darken(s.render((-30, 62), size=440, span=3.6, center=(0, 1.3, 0))), 'by night, from above', 'the two rings of motes'))
    s = K.multi_scene(ROOT); rigkit.render(s, A, I, scale=A.RIG_SCALE)
    t2.append(K.label(s.render('front', size=440, span=1.1, center=(0, 2.0, 0)), 'the hood, close', 'a soft glowing face, two calm eyes'))
    s = K.multi_scene(ROOT); rigkit.render(s, A, I, scale=A.RIG_SCALE)
    t2.append(K.label(s.render((-25, 8), size=440, span=1.1, center=(0, 1.32, -0.1)), 'the loom at its heart', 'a spindle of light, rainbow warps'))
    K.sheet(t2, OUT + '/keeper_details.png', cols=4, title='The Keeper of Bonds - details')
if 'poses' in what:
    names = A.DRAFT
    K.sheet([tile(A.POSES[n], (-60, 20) if n.startswith('swim') else (-32, 10), label=n,
                  sub={'tired': 'fainted', 'rise': 'getting up', 'weave': 'charged: the weave', 'tug': 'a thread cast', 'mend': 'support',
                       'gift': 'kind', 'tend_a': 'by its loom (encounter)', 'sit_a': 'sit', 'sit_b': 'sit (idle beat)'}.get(n))
             for n in names], OUT + '/keeper_poses.png', cols=7, title='The Keeper of Bonds - every pose')
if 'faces' in what:
    tiles = []
    for f in (None,) + A.FACES:
        pose = {k: v for k, v in dict(I, _face=f, head=rigkit.I).items() if v is not None}
        tiles.append(tile(pose, 'front', span=0.8, center=(0, 2.0, 0), size=240, label=f or 'calm (default)'))
    K.sheet(tiles, OUT + '/keeper_faces.png', cols=8, title='The Keeper of Bonds - faces')
if 'items' in what:
    icons = [(n, f()) for n, f in A.ICONS.items()]
    W = 40 + sum(16 + 32 + 128 + 60 for _ in icons) + 40
    sh = Image.new('RGB', (980, 330), (198, 198, 198)); d = ImageDraw.Draw(sh)
    d.text((12, 8), 'The Keeper of Bonds - its items at 1x, 2x and 8x', fill=(20, 20, 20), font=font(20))
    x = 20
    for n, im in icons:
        d.text((x, 44), {'bond_thread': 'bond_thread - the Thread of Bonds', 'bond_compass': 'bond_compass - the Compass of Bonds'}[n], fill=(30, 30, 30), font=font(14))
        y = 80
        for k in (1, 2, 8):
            big = im.resize((16 * k, 16 * k), Image.NEAREST)
            sh.paste(big, (x, y + (128 - 16 * k) // 2), big)
            x += 16 * k + 24
        slot = Image.new('RGB', (36, 36), (139, 139, 139)); ImageDraw.Draw(slot).rectangle((0, 0, 35, 35), outline=(55, 55, 55))
        slot.paste(im.resize((32, 32), Image.NEAREST), (2, 2), im.resize((32, 32), Image.NEAREST))
        sh.paste(slot, (x, 126)); d.text((x - 4, 166), 'in a slot', fill=(50, 50, 50), font=font(11, False))
        x += 90
    # and both on a dark background, as at night in the hotbar
    for i, (n, im) in enumerate(icons):
        bg = Image.new('RGB', (150, 80), (40, 40, 50)); big = im.resize((64, 64), Image.NEAREST); bg.paste(big, (43, 8), big)
        sh.paste(bg, (20 + i * 170, 230))
    sh.save(OUT + '/keeper_items.png')
if 'doll' in what:
    import dolls_bake as DB, phase134 as P134
    # the doll is baked exactly as phase141 bakes the others: from the figurine's parts (the real rig at rest), the default warp
    parts = P134._rigkit(A, I, A.RIG_SCALE)
    lo = fit()[0]
    tex, els = DB.bake(ROOT, parts, ground=lo, **A.DOLL)
    os.makedirs(f'{ROOT}/assets/bm/models/item', exist_ok=True)
    json.dump({'textures': {k: v for k, v in tex.items()}, 'elements': els}, open(f'{ROOT}/assets/bm/models/item/doll_keeper.json', 'w'))
    dolls = ['doll_emma', 'doll_lightbringer', 'doll_dryad', 'doll_vexis', 'doll_fishy', 'doll_bender', 'doll_henry']
    dolls = [d for d in dolls if os.path.exists(f'{K.REAL}/assets/bm/models/item/{d}.json')]
    tiles = []
    for view, l in (((-20, 10), 'front 3/4'), ((160, 10), 'back 3/4')):
        s = K.multi_scene(ROOT, K.REAL)
        xs = [-1.4 + 0.42 * i for i in range(len(dolls) + 1)]
        row = dolls[:len(dolls) // 2] + ['doll_keeper'] + dolls[len(dolls) // 2:]
        for x, dname in zip(xs, row):
            s.display(f'bm:item/{dname}', pos=(x, 0.5, 0), yaw=180)
        tiles.append(K.label(s.render(view, size=820, span=3.4, center=(-0.1, 0.55, 0)), l, '   '.join(d[5:] for d in row)))
    s = K.multi_scene(ROOT); s.display('bm:item/doll_keeper', pos=(0, 0.5, 0), yaw=180)
    s2 = K.multi_scene(ROOT); s2.display('bm:item/doll_keeper', pos=(0, 0.5, 0), yaw=180)
    close = [K.label(s.render((-25, 12), size=410, span=1.25, center=(0, 0.62, 0)), 'the Keeper doll, close'),
             K.label(s2.render((150, 12), size=410, span=1.25, center=(0, 0.62, 0)), 'from behind')]
    sheet = Image.new('RGB', (820 + 410, 820 * 2 + 40), 'white')
    ImageDraw.Draw(sheet).text((12, 8), "The Keeper of Bonds - Cecil's doll (baked from its real model, the default chibi warp), beside the others", fill=(20, 20, 20), font=font(20))
    for i, t in enumerate(tiles): sheet.paste(t, (0, 40 + 820 * i))
    for i, t in enumerate(close): sheet.paste(t, (820, 40 + 410 * i))
    sheet.save(OUT + '/keeper_doll.png')
    print('doll elements', len(els))
if 'fit' in what:
    print('FIT =', fit())
if 'clip' in what:
    names = [n for n in A.POSES if not n.startswith('swim_') or n in ('swim_0', 'swim_2', 'swim_4', 'swim_6')]
    txt = '\n'.join(clip_report(names))
    open(f'{SCRATCH}/keeper_clip.txt', 'w').write(txt + '\n'); print(txt)
if 'sanctuary' in what:
    import keeper_sanctuary as KS
    import sanctuary_view as SV
    SV.sheet(KS, OUT + '/sanctuary.png')

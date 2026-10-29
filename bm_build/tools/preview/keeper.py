"""The Keeper of Bonds' preview sheets (rigkit).  python3 tools/preview/keeper.py [lineup,poses,faces,items,doll,sanctuary,clip,fit,looks,shimmer,zfight]
Writes to $BM_PREVIEW_DIR (default: previews/v300_keeper). The dark tile: tools/render has no light, so each face is tinted after
the scene is built - unlit faces dimmed to night, faces of elements with light_emission kept bright in proportion to their level
(as tools/preview/pale_dryad.py does it). 'clip' prints, per pose, every pair of parts whose boxes cut into each other beyond
the joints meant to meet, and how far its lowest point is off the floor. 'fit' measures phase134's FIT for the display case.
(3.0b) The animated strips (the pearl cloth, its trim, the wings) render at frame FRAME[0] (tools/render alone shows frame 0):
'shimmer' shows the iridescence over a cycle; 'looks' the wardrobe's looks (as phase138 recolours them: the luminance ramp, or
gild's metals) and the shiny, by day and by night; 'zfight' runs zfix's own test over every model of the scratch pack."""
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
FRAME = [0]                                  # (the animation frame the strips render at)


def _texture(self, tid):
    """tools/render's Scene.texture, but an animated strip shows frame FRAME[0] (its frames interpolated, as the game does)"""
    key = (tid, FRAME[0])
    if tid.startswith('#'):
        if tid not in self.tex: self.tex[tid] = np.array([[[int(tid[i:i + 2], 16) / 255 for i in (1, 3, 5)] + [1.0]]], np.float32)
        return self.tex[tid]
    if key not in self.tex:
        im = Image.open(self._path(tid, 'textures', '.png')).convert('RGBA')
        w, h = im.size
        if h > w:
            n = h // w; f = FRAME[0] % n
            im = im.crop((0, f * w, w, f * w + w))
        self.tex[key] = np.asarray(im).astype(np.float32) / 255.0
    return self.tex[key]


R.Scene.texture = _texture
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
    sky = (np.abs(a - np.array([199, 219, 242])).sum(axis=2) < 2)          # (3.0b: exact - the pearl cloth comes near the grid)
    grid = (np.abs(a - np.array([140, 158, 140])).sum(axis=2) < 2) | (np.abs(a - np.array([51, 127, 51])).sum(axis=2) < 2)
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


_MC = {}


def _model(n):
    if n not in _MC: _MC[n] = json.load(open(f'{ROOT}/assets/bm/models/item/{n}.json'))
    return _MC[n]


def boxes(pose):
    rec = _Rec(); rigkit.render(rec, A, pose, scale=A.RIG_SCALE)
    out = []
    for (mid, pos, yaw, tr, sc, left), p in zip(rec.d, [p for p in A.PARTS if not A.HIDDEN(p, pose)]):
        m = _model(mid.split('/')[-1])
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
                               ('forel', 'threadl'), ('body', 'skirt'), ('body', 'loom'), ('body', 'pool'), ('skirt', 'pool')] +
        [('body', f'wing_{t}{s}') for t in 'uml' for s in 'rl']}
FREE = ('motes', 'motesb', 'web')            # (the orbit and the web pass through and round it: light, not cloth)


def clip_report(names, tol=0.2):
    lines, U = [], A.RIG_SCALE / 16
    for n in names:
        pose = A.POSES[n]; bx = boxes(pose); hits = {}
        for (pa, ca, ea), (pb, cb, eb) in itertools.combinations(bx, 2):
            if pa == pb or frozenset((pa, pb)) in MEET: continue
            if (pa in FREE or pb in FREE) and not ({pa, pb} & {'motes', 'motesb'} and (pa.startswith('wing') or pb.startswith('wing'))): continue
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


# ---------------------------------------------------------------------------------------------------- the sanctuary
VTEX = os.path.join(R.VANILLA, 'minecraft', 'textures', 'block')
TINT = {'grass_block': '#79b04a', 'short_grass': '#6ea844'}
_CC = {}


def block_colour(name, top=False):
    """a block's colour: its vanilla texture's average (the top's, for top faces), tinted where the game tints it"""
    key = (name, top)
    if key in _CC: return _CC[key]
    if name in TINT and (top or name != 'grass_block'):
        _CC[key] = TINT[name]; return TINT[name]
    base = name.replace('_stained_glass_pane', '_stained_glass').replace('quartz_pillar', 'quartz_pillar_top' if top else 'quartz_pillar')
    base = {'smooth_quartz': 'quartz_block_bottom', 'smooth_quartz_slab': 'quartz_block_bottom', 'quartz_stairs': 'quartz_block_side',
            'birch_slab': 'birch_planks', 'birch_stairs': 'birch_planks', 'birch_fence': 'birch_planks', 'iron_chain': 'iron_chain',
            'grass_block': 'grass_block_side', 'stripped_birch_log': 'stripped_birch_log_top' if top else 'stripped_birch_log',
            'cherry_log': 'cherry_log_top' if top else 'cherry_log', 'pointed_dripstone': 'pointed_dripstone_down_tip',
            'loom': 'loom_top' if top else 'loom_front', 'chiseled_quartz_block': 'chiseled_quartz_block_top' if top else 'chiseled_quartz_block',
            'wildflowers': 'wildflowers', 'pink_petals': 'pink_petals', 'firefly_bush': 'firefly_bush', 'smooth_basalt': 'smooth_basalt'}.get(base, base)
    for cand in (base, base + '_top', base + '_side', base + '_front', base.rstrip('s')):
        f = os.path.join(VTEX, cand + '.png')
        if os.path.exists(f):
            im = np.asarray(Image.open(f).convert('RGBA')).astype(float)[:16]
            m = im[..., 3] > 30
            c = im[m][:, :3].mean(0) if m.any() else np.array([200, 0, 200])
            if name in ('wildflowers', 'pink_petals'): c = c * 0.6 + np.array([250, 170, 210]) * 0.4
            _CC[key] = '#%02x%02x%02x' % tuple(int(v) for v in c); return _CC[key]
    _CC[key] = '#c800c8'; return _CC[key]


def _quad(s, pts, col):
    s.faces.append((pts, [(0, 0), (1, 0), (1, 1), (0, 1)], col))


def _box(s, lo, hi, col, top=None, skip=()):
    (x0, y0, z0), (x1, y1, z1) = lo, hi
    Q = {'down': [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], 'up': [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)],
         'north': [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], 'south': [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)],
         'west': [(x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0)], 'east': [(x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0)]}
    for f, q in Q.items():
        if f not in skip: _quad(s, q, top if (f == 'up' and top) else col)


def voxels(s, B, at):
    """a structures.Build into a Scene: full blocks as cubes (only the faces open to the air), the rest as their rough shapes"""
    from structures import parse_state
    cells = {p: parse_state(st) for p, st in B.b.items()}
    THIN = ('pane', 'fence', 'chain', 'lantern', 'stairs', 'slab', 'petals', 'flowers', 'short_grass', 'daisy', 'cornflower', 'allium', 'valley', 'bush',
            'pointed', 'loom')
    full = lambda p: p in cells and not any(k in cells[p][0] for k in THIN)
    ox, oy, oz = at
    for (x, y, z), (name, props) in cells.items():
        n = name.split(':')[1]
        if n == 'air': continue
        wx, wy, wz = x + ox, y + oy, z + oz
        col, topc = block_colour(n), block_colour(n, True)
        if full((x, y, z)):
            skip = [f for f, d in (('up', (0, 1, 0)), ('down', (0, -1, 0)), ('north', (0, 0, -1)), ('south', (0, 0, 1)), ('west', (-1, 0, 0)), ('east', (1, 0, 0)))
                    if full((x + d[0], y + d[1], z + d[2]))]
            _box(s, (wx, wy, wz), (wx + 1, wy + 1, wz + 1), col, topc, skip)
        elif 'pane' in n or 'fence' in n:
            w = 0.07 if 'pane' in n else 0.12
            _box(s, (wx + 0.5 - w, wy, wz + 0.5 - w), (wx + 0.5 + w, wy + 1, wz + 0.5 + w), col)
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = cells.get((x + dx, y, z + dz))
                if q and q[0].split(':')[1] != 'air' and ('pane' in q[0] or 'fence' in q[0] or full((x + dx, y, z + dz)) or 'log' in q[0]):
                    lo = (wx + 0.5 + min(0, dx * 0.5) - (w if dx == 0 else 0), wy + (0.0 if 'pane' in n else 0.4), wz + 0.5 + min(0, dz * 0.5) - (w if dz == 0 else 0))
                    hi = (wx + 0.5 + max(0, dx * 0.5) + (w if dx == 0 else 0), wy + (1.0 if 'pane' in n else 0.8), wz + 0.5 + max(0, dz * 0.5) + (w if dz == 0 else 0))
                    _box(s, lo, hi, col)
        elif 'stairs' in n:
            f = props.get('facing', 'north')
            _box(s, (wx, wy, wz), (wx + 1, wy + 0.5, wz + 1), col, topc)
            lo, hi = {'north': ((0, 0.5, 0), (1, 1, 0.5)), 'south': ((0, 0.5, 0.5), (1, 1, 1)), 'west': ((0, 0.5, 0), (0.5, 1, 1)), 'east': ((0.5, 0.5, 0), (1, 1, 1))}[f]
            _box(s, (wx + lo[0], wy + lo[1], wz + lo[2]), (wx + hi[0], wy + hi[1], wz + hi[2]), col, topc)
        elif 'slab' in n:
            y0 = 0.5 if props.get('type') == 'top' else 0.0
            _box(s, (wx, wy + y0, wz), (wx + 1, wy + y0 + 0.5, wz + 1), col, topc)
        elif 'chain' in n:
            _box(s, (wx + 0.44, wy, wz + 0.44), (wx + 0.56, wy + 1, wz + 0.56), '#4a4e58')
        elif 'lantern' in n:
            y0 = 0.3 if props.get('hanging') == 'true' else 0.0
            _box(s, (wx + 0.31, wy + y0, wz + 0.31), (wx + 0.69, wy + y0 + 0.45, wz + 0.69), '#ffd27a', '#ffe9b0')
            if y0: _box(s, (wx + 0.45, wy + 0.75, wz + 0.45), (wx + 0.55, wy + 1, wz + 0.55), '#4a4e58')
        elif 'pointed' in n:
            k = {'base': 0.4, 'middle': 0.3, 'frustum': 0.22, 'tip': 0.12}.get(props.get('thickness'), 0.3)
            _box(s, (wx + 0.5 - k, wy, wz + 0.5 - k), (wx + 0.5 + k, wy + 1, wz + 0.5 + k), col)
        elif 'petals' in n or 'wildflowers' in n:
            _box(s, (wx + 0.1, wy, wz + 0.1), (wx + 0.9, wy + 0.08, wz + 0.9), col)
        elif 'loom' in n:
            _box(s, (wx, wy, wz), (wx + 1, wy + 1, wz + 1), col, topc)
        else:                                                    # (flowers, grass: a small tuft)
            h = 0.55 if 'grass' in n else 0.7
            fc = {'oxeye_daisy': '#f4f0e0', 'cornflower': '#4a6ad8', 'allium': '#b06ad8', 'lily_of_the_valley': '#f8f8f0', 'firefly_bush': '#5a7a3a'}.get(n, col)
            _box(s, (wx + 0.38, wy, wz + 0.38), (wx + 0.62, wy + h * 0.7, wz + 0.62), '#5a9a3a')
            _box(s, (wx + 0.3, wy + h * 0.7, wz + 0.3), (wx + 0.7, wy + h, wz + 0.7), fc)


def sanctuary_sheet(path):
    import keeper_sanctuary as KS
    B = KS.build(); B.connect()
    at = (-KS.CX - 0.5, -(KS.TOP + 1), -KS.CZ - 0.5)              # (the dais's centre over the origin; the grass's top at y 0)
    def scene():
        s = K.multi_scene(ROOT)
        voxels(s, B, at)
        sx, sy, sz = KS.SPAWN[0] + at[0], KS.SPAWN[1] + at[1], KS.SPAWN[2] + at[2]
        rigkit.render(s, A, A.POSES['tend_a'], at=(sx, sy, sz - 0.4), scale=A.RIG_SCALE, yaw=180)       # (the Keeper at its loom)
        ax, ay, az = KS.ARRIVAL[0] + at[0], KS.ARRIVAL[1] + at[1], KS.ARRIVAL[2] + at[2]
        K.person(s, (ax, ay, az))
        return s
    tiles = []
    for v, sp, c, l, sub in (((-35, 24), 34, (0, -4, 0), 'from the south-west', 'a player on the landing circle; the Keeper by its loom'),
                            ((40, -12), 34, (0, -7, 0), 'from below', 'the hanging point, lanterns on chains'),
                            ((0, 55), 30, (0, 0, 0), 'from above', 'the arches, the threads, the dais'),
                            ((-28, 20), 11, (0, 1.6, -0.5), 'the dais and the great loom, close', 'the Keeper at its loom (tend_a)')):
        s = scene()
        im = s.render(v, size=700, span=sp, center=c)
        tiles.append(K.label(im, l, sub))
    K.sheet(tiles, path, cols=2, title='The Loom Sanctuary - a floating island high in the sky (keeper_sanctuary, %d x %d x %d)' % KS.SIZE)


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
    t2.append(K.label(s.render('front', size=440, span=1.1, center=(0, 1.8, 0)), 'the hood, close', 'smiling eyes of light, a glowing blush'))
    s = K.multi_scene(ROOT); rigkit.render(s, A, I, scale=A.RIG_SCALE)
    t2.append(K.label(s.render((-25, 8), size=440, span=1.1, center=(0, 1.18, -0.1)), 'the loom at its heart', 'a spindle of light, rainbow warps'))
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
        tiles.append(tile(pose, 'front', span=0.8, center=(0, 1.8, 0), size=240, label=f or 'calm (default)'))
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
    dolls = ['doll_lightbringer', 'doll_dryad', 'doll_ava', 'doll_nia', 'doll_henry', 'doll_cecil']
    dolls = [d for d in dolls if os.path.exists(f'{K.REAL}/assets/bm/models/item/{d}.json')]
    tiles = []
    for view, l in (((-20, 10), 'front 3/4'), ((160, 10), 'back 3/4')):
        s = K.multi_scene(ROOT, K.REAL)
        xs = [-1.5 + 0.5 * i for i in range(len(dolls) + 1)]
        row = dolls[:len(dolls) // 2] + ['doll_keeper'] + dolls[len(dolls) // 2:]
        for x, dname in zip(xs, row):
            s.display(f'bm:item/{dname}', pos=(x, 0.5, 0), yaw=0)
        tiles.append(K.label(s.render(view, size=820, span=3.6, center=(0.0, 0.55, 0)), l, '   '.join(d[5:] for d in row)))
    s = K.multi_scene(ROOT); s.display('bm:item/doll_keeper', pos=(0, 0.5, 0), yaw=0)
    s2 = K.multi_scene(ROOT); s2.display('bm:item/doll_keeper', pos=(0, 0.5, 0), yaw=0)
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
    sanctuary_sheet(OUT + '/sanctuary.png')
def world_zfight(m, ztol=0.03, amin=0.05):
    """z-fighting in the model's own space: pairs of faces facing the same way, in one plane (within ztol) and overlapping by
    more than amin both ways - every element's rotation applied (zfix compares x/y/z-rotated elements in their local frames,
    so it flags feathers of different turns that never meet, and misses ones that do)"""
    N = {'north': (0, 0, -1), 'south': (0, 0, 1), 'east': (1, 0, 0), 'west': (-1, 0, 0), 'up': (0, 1, 0), 'down': (0, -1, 0)}
    quads = []
    for i, e in enumerate(m['elements']):
        f, t = np.array(e['from'], float), np.array(e['to'], float)
        r = e.get('rotation'); M, o = np.eye(3), np.zeros(3)
        if r:
            o = np.array(r['origin'], float)
            M = {'x': R.rx, 'y': R.ry, 'z': R.rz}[r['axis']](math.radians(r['angle'])) if 'axis' in r else \
                R.rz(math.radians(r.get('z', 0))) @ R.ry(math.radians(r.get('y', 0))) @ R.rx(math.radians(r.get('x', 0)))
        for fn in e['faces']:
            n = np.array(N[fn], float); ax = int(np.argmax(np.abs(n)))
            c = [np.array(v) for v in itertools.product(*[(f[k], t[k]) if k != ax else ((t[k],) if n[ax] > 0 else (f[k],)) for k in range(3)])]
            w = [M @ (p - o) + o for p in c]
            quads.append((i, fn, M @ n, np.array(w)))
    hits = []
    for (ia, fa, na, wa), (ib, fb, nb, wb) in itertools.combinations(quads, 2):
        if ia == ib or na @ nb < 0.9999 or abs(na @ (wa[0] - wb[0])) > ztol: continue
        u = wa[1] - wa[0] if np.linalg.norm(wa[1] - wa[0]) > 1e-9 else wa[2] - wa[0]
        u = u / np.linalg.norm(u); v = np.cross(na, u)
        A2, B2 = np.c_[wa @ u, wa @ v], np.c_[wb @ u, wb @ v]
        def hull(P):
            P = sorted(map(tuple, P)); return P
        ok = True
        for poly in (A2, B2):
            Q = np.array([poly[0], poly[1], poly[3], poly[2]])          # (corners in order round the quad)
            for k in range(4):
                ed = Q[(k + 1) % 4] - Q[k]; nn = np.array([-ed[1], ed[0]])
                if np.linalg.norm(nn) < 1e-9: continue
                nn = nn / np.linalg.norm(nn); pa, pb = A2 @ nn, B2 @ nn
                if min(pa.max(), pb.max()) - max(pa.min(), pb.min()) <= amin: ok = False; break
            if not ok: break
        if ok: hits.append((ia, fa, ib, fb))
    return hits


if 'zfight' in what:
    import zfix
    nw = 0
    for f in sorted(os.listdir(f'{ROOT}/assets/bm/models/item')):
        if not f.startswith(A.PREFIX): continue
        h = world_zfight(json.load(open(f'{ROOT}/assets/bm/models/item/{f}')))
        if h: print('z-fighting (model space):', f, len(h), h[:4])
        nw += len(h)
    print('zfight: model-space pairs =', nw)
    n = 0
    for f in sorted(os.listdir(f'{ROOT}/assets/bm/models/item')):
        if not f.startswith(A.PREFIX): continue
        m = json.load(open(f'{ROOT}/assets/bm/models/item/{f}'))
        k = zfix.fix_model(f'{ROOT}/assets', m)
        if k: print('z-fighting:', f, k)
        n += k
    print('zfight: faces zfix would move =', n)
if 'shimmer' in what:
    # the iridescence over one cycle: four frames of the pearl cloth's sheen (and the wings', the gold's) - the same pose and view
    tiles = []
    for f in (0, 4, 8, 12):
        FRAME[0] = f
        s = K.multi_scene(ROOT); rigkit.render(s, A, I, scale=A.RIG_SCALE)
        tiles.append(K.label(s.render((-30, 10), size=420, span=1.7, center=(0, 1.55, 0)), f'frame {f} of {A.FRAMES}', f'{f * 5 / 20:.0f} s - the sheen flowing over the pearl'))
    for f in (0, 4, 8, 12):
        FRAME[0] = f
        s = K.multi_scene(ROOT); rigkit.render(s, A, I, scale=A.RIG_SCALE)
        tiles.append(K.label(s.render((150, 10), size=420, span=2.6, center=(0, 1.6, 0)), f'frame {f}, from behind', 'the wings shimmering with it'))
    FRAME[0] = 0
    K.sheet(tiles, OUT + '/keeper_shimmer.png', cols=4, title='The Keeper of Bonds - the iridescence: animated strips (interpolated), four frames of one cycle')
    # and the strips themselves, every fourth frame at 2x
    names = list(A.ANIMATED)
    T = A.textures()
    sh = Image.new('RGB', (len(names) * 140 + 10, 4 * 140 + 50), (40, 40, 50)); d = ImageDraw.Draw(sh)
    d.text((10, 8), 'the animated strips (frames 0, 4, 8, 12)', fill=(235, 235, 235), font=font(16))
    for i, n in enumerate(names):
        d.text((10 + i * 140, 30), n, fill=(220, 220, 220), font=font(11, False))
        for j, f in enumerate((0, 4, 8, 12)):
            sh.paste(T[n].crop((0, 64 * f, 64, 64 * f + 64)).resize((128, 128), Image.NEAREST), (10 + i * 140, 48 + j * 140))
    sh.save(OUT + '/keeper_strips.png')
if 'looks' in what:
    # the wardrobe's looks, made exactly as phase138.textures makes them (LOOK_TEX through phase99._recolour, or gild's metal)
    import phase99 as P99, gild
    base = A.textures()
    looks = [(0, 'its own pearl', None)] + [(k, n, pal) for k, (n, pal) in P99.NEW['keeper'][3].items()]
    tiles, ntiles = [], []
    for k, name, pal in looks:
        root = ROOT
        if pal is not None:
            root = K.pack(A, f'{SCRATCH}/rp_kb_look')
            if gild.is_gilded('keeper', k): ims = {n: gild.dress('keeper', k, base[n]) for n in A.LOOK_TEX}
            else: ims = P99._recolour({n: base[n] for n in A.LOOK_TEX}, pal)
            for n, im in ims.items():
                assert im.size == base[n].size, (n, im.size)
                im.save(f'{root}/assets/bm/textures/block/{n}.png')
        for night in (False, True):
            FRAME[0] = 6
            s = night_scene(root) if night else K.multi_scene(root)
            rigkit.render(s, A, I, scale=A.RIG_SCALE)
            im = s.render((-30, 10), size=300, span=2.9, center=(0, 1.3, 0))
            (ntiles if night else tiles).append(dark_label(darken(im), name, 'at night') if night else K.label(im, name, f'look {k}' if k else 'no look'))
    FRAME[0] = 0
    K.sheet(tiles + ntiles, OUT + '/keeper_looks.png', cols=len(tiles), title="The Keeper of Bonds - its wardrobe (phase138's recolours of the animated pearl: kb_robe, kb_hood), by day and by night")

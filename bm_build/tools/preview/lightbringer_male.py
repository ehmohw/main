"""(3.0) The Lightbringer's male form - preview sheets.  python3 tools/preview/lightbringer_male.py [both,faces,oph,night,looks,clip]
Writes to $BM_PREVIEW_DIR (default: previews/v300_lightbringer/male); the throwaway packs go to $BM_SCRATCH (default /tmp/bm_previews).
both   lb_male_both.png: both forms side by side beside a player - front, three-quarter, back
faces  lb_male_faces.png: his faces (every one the rig has), close
oph    lb_male_oph.png: the Ophanim's charged attack as he begins it - the wheel above him (it hides and restores whichever form)
night  lb_male_night.png: both forms by night (tools/render has no light: unlit faces dimmed, lit ones kept by their level)
looks  lb_male_looks.png: every wardrobe look (as phase138 recolours lb_robe / lb_bodice; gild for the metals) and the shiny, on him
clip   lb_male_clip.txt: per pose, every pair of his parts cutting into each other beyond their joints (and his lowest point)"""
import sys, os, json, math, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM)
os.environ.setdefault('BM_PREVIEW_DIR', os.path.join(os.path.dirname(BM), 'previews', 'v300_lightbringer', 'male'))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import draftkit as K, lightbringer_art as A, rigkit
from tools import render as R
OUT = os.environ['BM_PREVIEW_DIR']; os.makedirs(OUT, exist_ok=True)
SCRATCH = os.environ.get('BM_SCRATCH', '/tmp/bm_previews'); os.makedirs(SCRATCH, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['both', 'faces', 'oph', 'night', 'looks', 'clip']
ROOT = K.pack(A, f'{SCRATCH}/rp_lb_m')
M = A.MALE
I = A.POSES['idle_a']
NIGHT_BG, NIGHT_GRID = (16, 18, 34), (34, 38, 52)


def font(sz, bold=True):
    try: return ImageFont.truetype(f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if bold else ""}.ttf', sz)
    except OSError: return None


def cull_render(s, view, **kw):
    """Scene.render with the herald's own faces culled when they face away (the game culls a translucent item's back faces)"""
    V = view if isinstance(view, tuple) else {'front': (0, 0), 'back': (180, 0), 'side': (90, 0)}[view]
    yw, pt = math.radians(V[0]), math.radians(V[1])
    fwd = np.array([-math.sin(yw) * math.cos(pt), -math.sin(pt), -math.cos(yw) * math.cos(pt)])
    keep = []
    for f in s.faces:
        if f[0] != 'box' and isinstance(f[2], str) and f[2].startswith('bm:block/lb_'):
            p = [np.array(v) for v in f[0]]
            if np.cross(p[1] - p[0], p[3] - p[0]) @ fwd < -1e-9: continue
        keep.append(f)
    allf, s.faces = s.faces, keep
    try: return s.render(view, **kw)
    finally: s.faces = allf


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

    def solid(lo, hi, color='#c08060'):
        c = tuple(int(int(color[i:i + 2], 16) * 0.22) for i in (1, 3, 5))
        R.Scene.solid(s, lo, hi, '#%02x%02x%02x' % c)
    s.solid = solid
    return s


def darken(im):
    a = np.asarray(im).astype(np.float32)
    sky = (np.abs(a - np.array([199, 219, 242])).sum(axis=2) < 2)
    grid = (np.abs(a - np.array([140, 158, 140])).sum(axis=2) < 2) | (np.abs(a - np.array([51, 127, 51])).sum(axis=2) < 2)
    a[sky] = NIGHT_BG; a[grid] = NIGHT_GRID
    return Image.fromarray(a.astype(np.uint8))


def dark_label(im, text, sub=None):
    d = ImageDraw.Draw(im); d.text((8, 6), text, fill=(235, 228, 210), font=font(15))
    if sub: d.text((8, 25), sub, fill=(170, 170, 190), font=font(12, False))
    return im


def pair(view, label, sub=None, night=False, size=520, root=None, pose=I):
    """her (left), a player (middle), him (right)"""
    s = night_scene(root or ROOT) if night else K.multi_scene(root or ROOT)
    rigkit.render(s, A, pose, at=(-1.15, 0, 0), scale=A.RIG_SCALE)
    rigkit.render(s, A, pose, at=(1.15, 0, 0), scale=A.RIG_SCALE, suffix=M)
    K.person(s, (0.0, 0, 0.0))
    im = cull_render(s, view, size=size, span=3.8, center=(0, 1.05, 0))
    if night: return dark_label(darken(im), label, sub)
    return K.label(im, label, sub)


def tile(pose, view=(-30, 12), span=2.6, center=(0, 1.0, 0), size=340, label='', sub=None, sfx=M, root=None, night=False):
    s = night_scene(root or ROOT) if night else K.multi_scene(root or ROOT)
    rigkit.render(s, A, pose, scale=A.RIG_SCALE, suffix=sfx)
    im = cull_render(s, view, size=size, span=span, center=center)
    return dark_label(darken(im), label, sub) if night else K.label(im, label, sub)


if 'both' in what:
    K.sheet([pair('front', 'front', 'her - a player - him'), pair((-35, 12), '3/4'), pair((180, 6), 'back'), pair((145, 12), 'back 3/4')],
            OUT + '/lb_male_both.png', cols=2, title='The Lightbringer - both forms (herald: she / he), beside a player')
    K.sheet([tile(A.POSES[n], label=n) for n in A.DRAFT], OUT + '/lb_male_poses.png', cols=5, title='The Lightbringer (he) - every pose, unchanged rig')
if 'faces' in what:
    tiles = []
    for f in (None,) + A.FACES:
        pose = {k: v for k, v in dict(I, _face=f, head=rigkit.I).items() if v is not None}
        tiles.append(tile(pose, 'front', span=0.5, center=(0, 1.57, 0), size=360, label=f or 'default (serene)'))
    for f in (None, 'happy', 'fierce'):
        pose = {k: v for k, v in dict(I, _face=f).items() if v is not None}
        tiles.append(tile(pose, (-30, 8), span=0.75, center=(0, 1.62, 0), size=360, label=(f or 'default') + ', 3/4'))
    K.sheet(tiles, OUT + '/lb_male_faces.png', cols=5, title='The Lightbringer (he) - faces (the moods: happy, surprised, hurt, blink, fierce; sad on the tired pose)')
if 'oph' in what:
    import ophan_art as OA
    from rigkit import qs
    ro = K.pack(OA, f'{SCRATCH}/rp_oph')
    tiles = []
    for night in (False, True):
        s = (night_scene if night else K.multi_scene)(ROOT, ro)
        rigkit.render(s, A, A.POSES['wings_spread'], at=(0, 0, 0), scale=A.RIG_SCALE, suffix=M)      # (the moment it begins: the wheel opens over him)
        pose = {'ring_a': qs(('y', 28)), 'ring_b': qs(('x', 38)), 'ring_c': qs(('z', -35)), 'core': qs(('y', 20))}
        for p in OA.PARTS:                                                     # (phase236: summoned at ~ ~3.9 ~ over the host)
            s.display(f'bm:item/{OA.model_id(p)}', pos=(0, 3.9, 0), scale=OA.SCALE, left=tuple(pose.get(p, rigkit.I)))
        K.person(s, (2.0, 0, 0.5))
        im = cull_render(s, (-24, 10), size=620, span=8.5, center=(0.4, 3.3, 0))
        tiles.append(dark_label(darken(im), 'the Ophanim, by night') if night else K.label(im, 'the Ophanim (he begins it: wings_spread)', 'his rig shrinks away while the wheel turns; then wings_spread again - his own models'))
    K.sheet(tiles, OUT + '/lb_male_oph.png', cols=2, title='The Lightbringer (he) - the Ophanim, unaffected')
if 'night' in what:
    K.sheet([pair('front', 'by night', 'her - a player - him', night=True), pair((-35, 12), 'by night, 3/4', night=True),
             pair((-35, 12), 'by night, sitting', night=True, pose=A.POSES['sit_b'])],
            OUT + '/lb_male_night.png', cols=3, title='The Lightbringer - both forms by night (the halo, the wing tips, the staff and the eyes glow)')
if 'looks' in what:
    import phase99 as P99, gild
    tiles = [tile(I, label='Pearl and gold', sub='(his own)')]
    T0 = A.textures()
    for k, (name, pal) in P99.NEW['lightbringer'][3].items():
        root = f'{SCRATCH}/rp_lb_m_c{k}'
        if not os.path.exists(root + '/assets'):
            import shutil; shutil.copytree(ROOT, root)
        keys = ('lb_robe', 'lb_bodice')
        if gild.is_gilded('lightbringer', k): ims = {n: gild.dress('lightbringer', k, T0[n]) for n in keys}
        else: ims = P99._recolour({n: T0[n] for n in keys}, pal)
        for n, im in ims.items(): im.save(f'{root}/assets/bm/textures/block/{n}.png')
        tiles.append(tile(I, label=name, root=root))
    K.sheet(tiles, OUT + '/lb_male_looks.png', cols=3, title='The Lightbringer (he) - the wardrobe looks and the shiny (they recolour his tunic and surcoat)')


# ---------------------------------------------------------------------------------------------------- clipping and floor
class _Rec:
    def __init__(self): self.d = []
    def display(self, mid, pos, yaw, translation, scale, left): self.d.append((mid, pos, yaw, translation, scale, left))


def boxes(pose, sfx=M):
    rec = _Rec(); rigkit.render(rec, A, pose, scale=A.RIG_SCALE, suffix=sfx)
    out = []
    for (mid, pos, yaw, tr, sc, left), p in zip(rec.d, [p for p in A.PARTS if not A.HIDDEN(p, pose)]):
        nm = mid.split('/')[-1]
        m = json.load(open(f'{ROOT}/assets/bm/models/item/{nm}.json'))
        Q = R.quat(left); E = R.ry(math.radians(-yaw))
        jk = nm.split('_x')[0] + (sfx if '_x' in nm else '')
        for i, e in enumerate(m['elements']):
            f, t = e['from'], e['to']
            cs = [np.array((x, y, z), float) for x in (f[0], t[0]) for y in (f[1], t[1]) for z in (f[2], t[2])]
            r = e.get('rotation')
            if r:
                o = np.array(r['origin'])
                Mx = {'x': R.rx, 'y': R.ry, 'z': R.rz}[r['axis']](math.radians(r['angle'])) if 'axis' in r else \
                    R.rz(math.radians(r.get('z', 0))) @ R.ry(math.radians(r.get('y', 0))) @ R.rx(math.radians(r.get('x', 0)))
                cs = [Mx @ (c - o) + o for c in cs]
            w = [E @ (Q @ (sc * (R.ry(math.pi) @ (c / 16 - 0.5))) + np.array(tr)) + np.array(pos) for c in cs]
            out.append((p, np.array(w), dict(e, _joint=A.JOINTS.get(jk, {}).get(i, ()))))
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


MEET = {frozenset(p) for p in [('body', 'head'), ('body', 'armr'), ('body', 'arml'), ('armr', 'forer'), ('arml', 'forel'), ('forer', 'staff'),
                               ('hair', 'hairlo'), ('body', 'skirt'), ('head', 'hair'), ('legr', 'skirt'), ('legl', 'skirt'),
                               ('body', 'pool'), ('pool', 'legr'), ('pool', 'legl')]}


def clip_report(names, sfx=M, tol=0.15):
    lines = []
    U = A.RIG_SCALE / 16
    for n in names:
        bx = boxes(A.POSES[n], sfx); hits = {}
        for (pa, ca, ea), (pb, cb, eb) in itertools.combinations(bx, 2):
            if pa == pb or frozenset((pa, pb)) in MEET: continue
            if (pb in ea['_joint'] or pa in eb['_joint']) and _sat(ca, cb) / U < 0.8: continue
            if ca[:, 1].max() < cb[:, 1].min() or cb[:, 1].max() < ca[:, 1].min(): continue
            d = _sat(ca, cb) / U
            if d > tol:
                k = tuple(sorted((pa, pb))); hits[k] = max(hits.get(k, 0), d)
        low = min(c[:, 1].min() for p, c, e in bx if p != 'pool') / U
        lines.append(f'{n:18s} floor {low:+6.2f}  ' + ('  '.join(f'{a}/{b} {d:.2f}' for (a, b), d in sorted(hits.items())) or 'clean'))
    return lines


if 'clip' in what:
    names = [n for n in A.POSES if not n.startswith('swim_') or n in ('swim_0', 'swim_2', 'swim_4', 'swim_6')]
    rep_m, rep_f = clip_report(names, M), clip_report(names, '')
    txt = '\n'.join(f'{a}\n{"":18s} (hers:  {b[18:].strip()})' for a, b in zip(rep_m, rep_f))
    open(OUT + '/lb_male_clip.txt', 'w').write(txt + '\n'); print(txt)

"""The Lightbringer's preview sheets (rigkit).  python3 tools/preview/lightbringer.py [views,poses,faces,lineup,clip]
Writes to $BM_PREVIEW_DIR. She is translucent: the game draws a translucent item's faces with back-face culling, so these
renders cull too (render() below) - what shows through her robe and wings is what the game would show.
'clip' prints, per pose, every pair of parts whose boxes cut into each other (beyond the joints that are meant to meet) and
how far her lowest point is off the floor."""
import sys, os, json, math, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import numpy as np
import draftkit as K, lightbringer_art as A, bender_art as BD, rigkit
from tools import render as R
OUT = K.OUT; os.makedirs(OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['views', 'poses', 'faces', 'lineup', 'clip']
root = K.pack(A, OUT + '/rp_lb')


def render(s, view, **kw):
    """Scene.render with her own faces culled when they face away (as the game culls a translucent item's back faces)"""
    V = view if isinstance(view, tuple) else {'front': (0, 0), 'back': (180, 0), 'side': (90, 0), 'iso': (35, 25), 'top': (0, 89)}[view]
    yw, pt = math.radians(V[0]), math.radians(V[1])
    fwd = np.array([-math.sin(yw) * math.cos(pt), -math.sin(pt), -math.cos(yw) * math.cos(pt)])
    keep = []
    for f in s.faces:
        if f[0] != 'box' and isinstance(f[2], str) and f[2].startswith('bm:block/lb_'):
            p = [np.array(v) for v in f[0]]
            n = np.cross(p[1] - p[0], p[3] - p[0])                  # (points inward, by the quads' winding)
            if n @ fwd < -1e-9: continue                            # (its outside faces away from us)
        keep.append(f)
    allf, s.faces = s.faces, keep
    try: return s.render(view, **kw)
    finally: s.faces = allf


def tile(pose, view=(-30, 12), span=2.6, center=(0, 1.0, 0), size=340, label='', sub=None):
    s = K.multi_scene(root); rigkit.render(s, A, pose, scale=A.RIG_SCALE)
    return K.label(render(s, view, size=size, span=span, center=center), label, sub)


# ---------------------------------------------------------------------------------------------------- clipping and floor
class _Rec:
    def __init__(self): self.d = []
    def display(self, mid, pos, yaw, translation, scale, left): self.d.append((mid, pos, yaw, translation, scale, left))


def boxes(pose):
    """every visible element of hers in this pose as (part, corners (8 x 3, blocks, world))"""
    rec = _Rec(); rigkit.render(rec, A, pose, scale=A.RIG_SCALE)
    out = []
    for (mid, pos, yaw, tr, sc, left), p in zip(rec.d, [p for p in A.PARTS if not A.HIDDEN(p, pose)]):
        m = json.load(open(f'{root}/assets/bm/models/item/{mid.split("/")[-1]}.json'))
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
            out.append((p, np.array(w), dict(e, _joint=A.JOINTS.get(mid.split('/')[-1].split('_x')[0], {}).get(m['elements'].index(e), ()))))
    return out


def _sat(a, b):
    """how deep two boxes (8 corners each, ordered x-major) cut into each other (0 if apart)"""
    def axes(c):
        return [c[4] - c[0], c[2] - c[0], c[1] - c[0]]
    ax = [v for v in axes(a) + axes(b) if np.linalg.norm(v) > 1e-6]
    for u, v in itertools.product(axes(a), axes(b)):
        x = np.cross(u, v)
        if np.linalg.norm(x) > 1e-6: ax.append(x)
    depth = 1e9
    for v in ax:
        v = v / np.linalg.norm(v)
        pa, pb = a @ v, b @ v
        d = min(pa.max(), pb.max()) - max(pa.min(), pb.min())
        if d <= 0: return 0.0
        depth = min(depth, d)
    return depth


MEET = {frozenset(p) for p in [('body', 'head'), ('body', 'armr'), ('body', 'arml'), ('armr', 'forer'), ('arml', 'forel'), ('forer', 'staff'),
                               ('hair', 'hairlo'), ('body', 'skirt'), ('head', 'hair'), ('legr', 'skirt'), ('legl', 'skirt'),
                               ('body', 'pool'), ('pool', 'legr'), ('pool', 'legl')]}


def clip_report(names, tol=0.15):
    lines = []
    U = A.RIG_SCALE / 16
    for n in names:
        pose = A.POSES[n]; bx = boxes(pose)
        hits = {}
        for (pa, ca, ea), (pb, cb, eb) in itertools.combinations(bx, 2):
            ha, hb = (any(f['texture'].startswith('#lb_hair') for f in e['faces'].values()) for e in (ea, eb))
            if pa == pb or (frozenset((pa, pb)) in MEET and ha == hb): continue     # (hair against anything but hair is always checked)
            if (pb in ea['_joint'] or pa in eb['_joint']) and _sat(ca, cb) / U < 0.8: continue    # (where a wing or a lock grows out of her)
            if ca[:, 1].max() < min(cb[:, 1]) or cb[:, 1].max() < ca[:, 1].min(): continue
            d = _sat(ca, cb) / U
            if d > tol:
                k = tuple(sorted((pa, pb))); hits[k] = max(hits.get(k, 0), d)
        low = min(c[:, 1].min() for p, c, e in bx if p != 'pool') / U
        lines.append(f'{n:18s} floor {low:+6.2f}  ' + ('  '.join(f'{a}/{b} {d:.2f}' for (a, b), d in sorted(hits.items())) or 'clean'))
    return lines


# ---------------------------------------------------------------------------------------------------- sheets
I = A.POSES['idle_a']
if 'views' in what:
    K.sheet([tile(I, v, label=l) for v, l in (('front', 'front'), ((-35, 12), '3/4'), ('side', 'side'), ((145, 12), 'back 3/4'), ('back', 'back'),
                                              ((-30, 40), 'from above'))],
            OUT + '/lightbringer_turnaround.png', cols=3, title='The Lightbringer - turnaround (translucent; idle_a, hovering)')
if 'poses' in what:
    K.sheet([tile(A.POSES[n], label=n) for n in A.DRAFT], OUT + '/lightbringer_poses.png', cols=5, title='The Lightbringer - poses')
    K.sheet([tile(A.POSES[n], v, label=f'{n}', sub=l) for n in ('ward', 'wings_spread', 'smite', 'run_0', 'pray', 'tired')
             for v, l in (((60, 10), 'side 3/4'), ((160, 14), 'back 3/4'))],
            OUT + '/lightbringer_poses_back.png', cols=4, title='The Lightbringer - the big poses from behind')
if 'hair' in what or 'views' in what:
    K.sheet([tile(I, v, span=2.1, center=(0, 1.05, 0), size=420, label=l) for v, l in (('back', 'back'), ((150, 10), 'back 3/4'), ('side', 'side'),
                                                                                    ((-25, 8), 'front 3/4'))] +
            [tile(A.POSES[n], v, span=2.5, center=(0, 0.85, 0), size=420, label=n, sub=l)
             for n, v, l in (('run_0', (120, 10), 'streaming back'), ('pray', (130, 12), 'draped back over the robe'),
                             ('tired', (100, 10), 'kneeling, slumped'), ('swim_2', (120, 25), 'laid back'))],
            OUT + '/lightbringer_hair.png', cols=4, title='The Lightbringer - her hair, close')
if 'faces' in what:
    tiles = []
    for f in (None,) + A.FACES:
        pose = {k: v for k, v in dict(I, _face=f).items() if v is not None}
        tiles.append(tile(pose, 'front', span=0.72, center=(0, 1.7, 0), size=260, label=f or 'default (serene)'))
    K.sheet(tiles, OUT + '/lightbringer_faces.png', cols=4, title='The Lightbringer - faces')
    tiles = []                                                                         # (and close: just the face, large)
    for f in (None,) + A.FACES:
        pose = {k: v for k, v in dict(I, _face=f, head=rigkit.I).items() if v is not None}
        tiles.append(tile(pose, 'front', span=0.5, center=(0, 1.57, 0), size=360, label=f or 'default (serene)'))
    K.sheet(tiles, OUT + '/lightbringer_faces_close.png', cols=4, title='The Lightbringer - faces, close')
if 'lineup' in what:
    rb = K.pack(BD, OUT + '/rp_bender')
    s = K.multi_scene(root, rb)
    rigkit.render(s, A, A.POSES['idle_a'], at=(0.0, 0, 0), scale=A.RIG_SCALE)
    rigkit.render(s, A, A.POSES['bless'], at=(1.6, 0, 0.3), scale=A.RIG_SCALE, yaw=-30)
    rigkit.render(s, BD, BD.POSES['idle_a'], at=(3.0, 0, 0.5), scale=BD.RIG_SCALE, yaw=110)
    K.person(s, (-1.3, 0, 0.3))
    K.sheet([K.label(render(s, (-12, 8), size=760, span=5.6, center=(0.7, 1.1, 0)), 'size', 'a player, the Lightbringer (and again, blessing), Bender')],
            OUT + '/lightbringer_lineup.png', cols=1, title='The Lightbringer - to scale')
if 'clip' in what:
    names = [n for n in A.POSES if not n.startswith('swim_') or n in ('swim_0', 'swim_2', 'swim_4', 'swim_6')]
    txt = '\n'.join(clip_report(names))
    open(OUT + '/lightbringer_clip.txt', 'w').write(txt + '\n'); print(txt)

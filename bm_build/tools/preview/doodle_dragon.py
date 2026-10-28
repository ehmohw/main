"""The Doodle Dragon preview sheets (rigkit) - and a check that no card cuts through another, and he stands on the floor.
python3 tools/preview/doodle_dragon.py [views,poses,faces,lineup,fire,tex,check]"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import numpy as np
from PIL import Image
import draftkit as K, doodle_dragon_art as A, kettle_art as KA, rigkit
OUT = K.OUT; os.makedirs(OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['views', 'poses', 'faces', 'lineup', 'fire', 'tex', 'check']
root = K.pack(A, OUT + '/rp_dd')


def tile(pose, view=(-30, 12), span=2.4, center=(0, 0.85, 0), size=340, label='', sub=None):
    s = K.multi_scene(root); rigkit.render(s, A, pose, scale=A.RIG_SCALE)
    return K.label(s.render(view, size=size, span=span, center=center), label, sub)


# ---------------------------------------------------------------------------------------------------- the check
def _cards(pose):
    """every card shown in this pose: (part, world corners p0 p1 p3, uv box, texture alpha)"""
    T, M = A.textures(), A.models()
    xf = rigkit.solve(A.PIVOT, A.PARENT, pose); out = []
    for p in A.PARTS:
        if A.HIDDEN(p, pose): continue
        _tex, els = M[A.model_name(p, pose)]
        q, t = xf[p]; pv = A.PIVOT[p]; Dp = rigkit.D(pv); W = tuple(t[i] + Dp[i] for i in range(3)); k = A.PART_K.get(p, 1.0)
        def world(m):
            d = tuple((m[i] - 8) * k + pv[i] for i in range(3)); r = rigkit.qrot(q, tuple(rigkit.D(d)[i] - Dp[i] for i in range(3)))
            return np.array([W[i] + r[i] for i in range(3)])
        for e in els:
            (x1, y1, z1), (x2, y2, z2) = e['from'], e['to']
            Q = {'north': [(x2, y2, z1), (x1, y2, z1), (x1, y1, z1), (x2, y1, z1)], 'south': [(x1, y2, z2), (x2, y2, z2), (x2, y1, z2), (x1, y1, z2)],
                 'east': [(x2, y2, z2), (x2, y2, z1), (x2, y1, z1), (x2, y1, z2)], 'west': [(x1, y2, z1), (x1, y2, z2), (x1, y1, z2), (x1, y1, z1)],
                 'up': [(x1, y2, z1), (x2, y2, z1), (x2, y2, z2), (x1, y2, z2)], 'down': [(x1, y1, z2), (x2, y1, z2), (x2, y1, z1), (x1, y1, z1)]}
            for fc, f in e['faces'].items():
                if fc in ('south', 'west', 'down'): continue           # (a card's other face: the same shape)
                al = np.asarray(T[f['texture'][1:]])[..., 3] > 0
                c = [world(v) for v in Q[fc]]
                out.append((p, c[0], c[1], c[3], f['uv'], al))
    return out


def _opaque(card, X):
    """is world point X (n x 3, on the card's plane) on a coloured pixel of this card?"""
    _p, p0, p1, p3, uv, al = card
    e1, e2 = p1 - p0, p3 - p0; d = X - p0
    a = d @ e1 / (e1 @ e1); b = d @ e2 / (e2 @ e2)
    u = uv[0] + a * (uv[2] - uv[0]); v = uv[1] + b * (uv[3] - uv[1])
    H, W = al.shape; ok = (a >= 0) & (a <= 1) & (b >= 0) & (b <= 1)
    ui = np.clip((u / 16 * W).astype(int), 0, W - 1); vi = np.clip((v / 16 * H).astype(int), 0, H - 1)
    return ok & al[vi, ui]


def check(name, pose):
    cards = _cards(pose); clips = {}
    for i in range(len(cards)):
        for j in range(i + 1, len(cards)):
            a, b = cards[i], cards[j]
            if a[0] == b[0]: continue
            na = np.cross(a[2] - a[1], a[3] - a[1]); nb = np.cross(b[2] - b[1], b[3] - b[1])
            na, nb = na / np.linalg.norm(na), nb / np.linalg.norm(nb); d = np.cross(na, nb)
            if np.linalg.norm(d) < 1e-4:                               # (parallel: only a worry if they share the plane)
                if abs((b[1] - a[1]) @ na) < 0.06:
                    g = np.stack(np.meshgrid(np.linspace(0, 1, 64), np.linspace(0, 1, 64)), -1).reshape(-1, 2)
                    X = a[1] + g[:, :1] * (a[2] - a[1]) + g[:, 1:] * (a[3] - a[1])
                    n = int((_opaque(a, X) & _opaque(b, X)).sum())
                    if n: clips[(a[0], b[0], 'same plane')] = n
                continue
            d = d / np.linalg.norm(d)
            # a point on both planes
            Mx = np.array([na, nb, d]); rhs = np.array([na @ a[1], nb @ b[1], 0.0]); x0 = np.linalg.solve(Mx, rhs)
            X = x0 + np.arange(-48, 48, 0.04)[:, None] * d
            n = int((_opaque(a, X) & _opaque(b, X)).sum())
            if n: clips[(a[0], b[0])] = clips.get((a[0], b[0]), 0) + n
    low = 1e9
    for c in cards:
        if c[0] in A.FX: continue
        _p, p0, p1, p3, uv, al = c; H, W = al.shape
        vi, ui = np.nonzero(al)
        a = ((ui + 0.5) / W * 16 - uv[0]) / (uv[2] - uv[0]); b = ((vi + 0.5) / H * 16 - uv[1]) / (uv[3] - uv[1])
        Y = p0[1] + a * (p1 - p0)[1] + b * (p3 - p0)[1]
        if len(Y): low = min(low, float(Y.min()))
    return clips, low


if 'check' in what:
    bad = 0
    for n in A.POSES:
        clips, low = check(n, A.POSES[n])
        exp = 0.8 if n in ('run_1', 'run_3') else 0.0                  # (a run's airborne frames: a little off the floor)
        flag = '' if (n in A.AIRBORNE or n.startswith('swim_') or abs(low - exp) < 0.35) else '  <- FLOOR'
        if clips or flag: bad += 1
        print(f'{n:12s} lowest {low:6.2f}{flag}  ' + ('  '.join(f'{k}:{v}' for k, v in clips.items()) if clips else 'clean'))
    print('poses with problems:', bad)

if 'views' in what:
    I = A.POSES['idle_a']
    K.sheet([tile(I, v, label=l) for v, l in (('front', 'front'), ((-35, 18), '3/4'), ('side', 'side (flat!)'), ('back', 'back'), ((150, 15), 'back 3/4'))],
            OUT + '/doodle_dragon_turnaround.png', cols=5, title='The Doodle Dragon - turnaround')
if 'poses' in what:
    K.sheet([tile(A.POSES[n], label=n, sub=(A.POSES[n].get('_face') or '')) for n in A.DRAFT], OUT + '/doodle_dragon_poses.png', cols=6,
            title='The Doodle Dragon - poses')
if 'faces' in what:
    tiles = []
    for f in (None,) + A.FACES:
        pose = {k: v for k, v in dict(A.POSES['idle_a'], _face=f).items() if v is not None}
        s = K.multi_scene(root); rigkit.render(s, A, pose, scale=A.RIG_SCALE)
        tiles.append(K.label(s.render('front', size=260, span=0.85, center=(0, 1.15, 0)), f or 'default'))
    K.sheet(tiles, OUT + '/doodle_dragon_faces.png', cols=5, title='The Doodle Dragon - faces')
if 'fire' in what:                                     # (the side view looks along the flame: framed further forward)
    views = (((-30, 12), '3/4', 0.5), ('front', 'front', 0.5), ((-80, 8), 'side', 1.0), ((-40, 50), 'from above', 0.5))
    tiles = [tile(A.POSES[n], v, span=3.4, center=(0, 0.9, cz), label=n, sub=l) for n in ('breathe_up', 'breathe') for v, l, cz in views]
    K.sheet(tiles, OUT + '/doodle_dragon_fire.png', cols=4, title='The Doodle Dragon - crayon fire')
if 'tex' in what:
    T = A.textures(); ims = []
    for k, im in T.items():
        big = Image.new('RGBA', (256, 256), (255, 255, 255, 255))
        im2 = im.resize((256, 256), Image.NEAREST); big.alpha_composite(im2)
        ims.append(K.label(big.convert('RGB'), k, f'{im.width}x{im.height}'))
    K.sheet(ims, OUT + '/doodle_dragon_textures.png', cols=7, title='The Doodle Dragon - textures (the crayon pictures)')
if 'lineup' in what:
    rk = K.pack(KA, OUT + '/rp_kt')
    s = K.multi_scene(root, rk)
    rigkit.render(s, A, A.POSES['idle_a'], at=(0.0, 0, 0), scale=A.RIG_SCALE)
    rigkit.render(s, KA, KA.POSES['idle_a'], at=(1.25, 0, 0.2), scale=KA.RIG_SCALE)
    K.person(s, (-1.2, 0, 0.3))
    K.sheet([K.label(s.render((-12, 8), size=620, span=3.4, center=(0, 1.1, 0)), 'size', 'a player, the Doodle Dragon, Kettle (who drew him)')],
            OUT + '/doodle_dragon_lineup.png', cols=1, title='The Doodle Dragon - next to Kettle')

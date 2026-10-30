"""2.99 (v299): THE SOVEREIGN'S WINGS - its spoils, two elytra with the Wings of the Damned's powers (phase238: sov_wings,
sov_wings_holy) and all their art. The same wings, fallen and unfallen - ONE SILHOUETTE, two materials:
  THE LAST NIGHT (sov_wings)        the Dread Sovereign's own: black void membrane hung in strips from bone (its ds_ textures,
                                    dread_sovereign_art), red eyes open in it and glowing, the torn edge smouldering, clawed
                                    finger-bones; a burning crown-halo of eyes behind the head. A slow, menacing beat.
  THE FIRST LIGHT (sov_wings_holy)  Aurel's, before the dark (the Divine One's dvn_ textures, divine_art): white-gold feathers
                                    in the same envelope, white fire at their ends, a glowing gold leading edge, gems of light
                                    where the Last Night has eyes; a triple halo of light. A gentler, radiant beat.
THREE PAIRS OF WINGS in four item displays per wearer (seraph_wings' runtime - its sets() table - the same states, swaps
and cleanup as the Seraph's and the Dread's):
  w1r, w1l   the great wings, each its upper wing and the middle one under it (one display: they move together) - folded
             down the back as a layered cloak (the upper the outer, longest, its arch over the shoulder; the middle peeking
             out beneath at the side), open: spread, the upper raised over the middle - bigger than the Seraph's (~2.3 blocks
             a side)
  lw         the lower pair, both sides in one display (symmetric: only ever tilted) - round the legs at rest, fanned beneath
             in flight
  halo       behind the head: the Last Night's burning ring of eyes, or the First Light's three rings of light - it turns and
             swells with the breath of the idle
Their idle BREATHES: a slow 60-tick cycle - the wings ease out and settle, the halo turns and swells (a pose's '_k_<part>'
scales a display - seraph_wings.xforms).
Their icons: a 2D sprite in the hand and on the ground; in the inventory and item frames a small 3D model of the spread wings.
Their elytra 'wings' layers: 3.0c - the whole elytra painted (flat_wings) by default; the mantle (cut back, the Seraph's way)
only under the 3D wings, for a player who switched them on.
Design units: 1/16 block, feet at y 0, facing -z, the wearer's right +x (seraph_wings')."""
import math
import random
from PIL import Image

import rigkit
import seraph_art as SA
from seraph_wings import wing, CROUCH, GLIDE, dq

S, U = 1.0, 1.0 / 16
UP, BACK = (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)
PIVOT = {'body': (0.0, 22.5, 0.0), 'w1r': (1.6, 21.0, 3.4), 'w1l': (-1.6, 21.0, 3.4), 'lw': (0.0, 12.8, 3.4), 'halo': (0.0, 27.6, 6.2)}
PARENT = {'body': None, 'w1r': 'body', 'w1l': 'body', 'lw': 'body', 'halo': 'body'}
PARTS = ('w1r', 'w1l', 'lw', 'halo')
OPEN_K, LOW_K = 2.1, 1.3
ITEMS = {'night': 'sov_wings', 'light': 'sov_wings_holy'}


# ---------------------------------------------------------------------------------------------------- materials
_rs = random.Random(1)
FULL = SA.FULL


def _win(w, L, k):
    """a strip's uv on a cell texture (two texels a unit): a window as big as the strip, its own place on the texture"""
    wu, lu = max(0.5, min(16.0, w)), max(0.5, min(16.0, L))
    u0, v0 = (k * 3.7) % (16.0 - wu + 1e-6), (k * 5.3) % (16.0 - lu + 1e-6)
    r = lambda a, b, c, d: [round(a, 3), round(b, 3), round(c, 3), round(d, 3)]
    return {'up': r(u0, v0, u0 + wu, v0 + lu), 'down': r(u0, v0 + lu, u0 + wu, v0), 'east': [0, 0, 0.4, lu], 'west': [0, 0, 0.4, lu],
            'north': [0, 0, wu, 0.4], 'south': [0, 0, wu, 0.4]}


class Mat:
    """how one material builds the shared envelope: a strip of wing from the bone to the edge, the bone, a claw/primary at a
    finger, an eye, the edge's end"""
    def __init__(self, kind):
        self.kind = kind

    def strip(self, A, B, w, pv, up, k):
        out = []
        if self.kind == 'night':                               # black void membrane, the torn end smouldering, tatters
            L = math.dist(A, B)
            out.append(SA.SEG(A, B, w, 0.3, 'ds_membrane_t' if k % 4 == 0 else 'ds_membrane', pv, up, uv=_win(w, L, k)))
            d = tuple((B[i] - A[i]) / max(L, 1e-6) for i in range(3))
            if _rs.random() < 0.22:
                T = tuple(B[i] + d[i] * _rs.uniform(1.0, 2.6) for i in range(3))
                out.append(SA.SEG(B, T, w * 0.45, 0.25, 'ds_membrane_t', pv, up, uv=_win(w * 0.45, 2.0, k + 7)))
            if k % 6 == 2:
                out.append(SA.GEM(B, 0.55, 'ds_red_l', pv, light=12))
        else:                                                  # white-gold feathers, white fire at their ends
            M = tuple(A[i] + (B[i] - A[i]) * 0.76 for i in range(3))
            T = tuple(B[i] + (B[i] - A[i]) * 0.1 for i in range(3))
            out.append(SA.SEG(A, M, w * 1.1, 0.4, 'dvn_feather' if k % 2 else 'dvn_feather_d', pv, up, uv=FULL()))
            e = SA.SEG(M, T, w * 1.0, 0.36, 'dvn_ftip', pv, up, light=15, uv=FULL()); e['shade'] = False
            out.append(e)
        return out

    def bone(self, pts, w0, w1, pv, up):
        out = []; n = len(pts) - 1
        for i in range(n):
            w = w0 + (w1 - w0) * i / max(1, n - 1)
            if self.kind == 'night':
                out.append(SA.SEG(pts[i], pts[i + 1], w, w * 0.85, 'ds_wbone', pv, up, ext=0.2, uv=_win(w, math.dist(pts[i], pts[i + 1]), i)))
            else:
                out.append(SA.SEG(pts[i], pts[i + 1], w, w * 0.85, 'dvn_gold', pv, up, ext=0.2, light=12, uv=_win(w, math.dist(pts[i], pts[i + 1]), i)))
        return out

    def claw(self, A, B, w, pv, up):
        """past the edge at a finger: a clawed finger-bone (night), a long primary burning (light) - the same point"""
        if self.kind == 'night':
            M = tuple(A[i] + (B[i] - A[i]) * 0.55 for i in range(3))
            return [SA.SEG(A, M, w, w, 'ds_wbone', pv, up, uv=_win(w, math.dist(A, M), 3)), SA.SEG(M, B, w * 0.7, w * 0.7, 'ds_horn_r', pv, up, uv=FULL())]
        M = tuple(A[i] + (B[i] - A[i]) * 0.6 for i in range(3))
        e = SA.SEG(M, B, w * 1.9, 0.34, 'dvn_ftip', pv, up, light=15, uv=FULL()); e['shade'] = False
        return [SA.SEG(A, M, w * 2.0, 0.38, 'dvn_feather', pv, up, uv=FULL()), e]

    def eye(self, c, s, pv, n):
        if self.kind == 'night':
            return [SA.SEG(*_across(c, s * 1.5, n), s, 0.4, 'ds_eye', pv, n, light=15,
                           uv={'up': [0, 0, 16, 16], 'down': [0, 16, 16, 0], 'north': [0, 0, 1, 1], 'south': [0, 0, 1, 1], 'east': [0, 0, 1, 1], 'west': [0, 0, 1, 1]})]
        return [SA.GEM(c, s * 0.8, 'dvn_gem', pv, light=15)]


def _across(c, w, n):
    side = rigkit._unit(rigkit._cross(n, (0.0, 1.0, 0.0) if abs(n[1]) < 0.9 else (1.0, 0.0, 0.0)))
    return tuple(c[i] - side[i] * w / 2 for i in range(3)), tuple(c[i] + side[i] * w / 2 for i in range(3))


# ---------------------------------------------------------------------------------------------------- the envelope (both materials)
FING = [0.0, 0.24, 0.44, 0.62, 0.79, 0.92, 1.0]


def _open_wing(m, sx, pv, L, D0, lift, rot, root, z0, step, claws, eyes):
    """one open wing in its plane (u out, v up from `root`, turned `rot` degrees in that plane): the arm's curve, the trailing
    edge scalloped between the fingers - hung with strips (membrane or feathers) from the arm to the edge, claws/primaries
    past the edge at the fingers, eyes/gems between"""
    c, s_ = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    X, Y, Z = pv
    def P(u, v, w=0.0):
        uu, vv = u * c - v * s_, u * s_ + v * c
        return (X + sx * (root[0] + uu), Y + root[1] + vv, Z + z0 + 0.05 * u + w)
    arm = lambda u: lift * math.sin(math.pi * min(1.0, u / L * 1.15)) + 1.2 * u / L
    def edge(u):
        t = u / L; dist = min(abs(t - f) for f in FING)
        return arm(u) - D0 * (1 - 0.5 * t) * (1 - 2.0 * dist)
    W = []
    n = int(L / step)
    for k in range(n):
        u = L * (k + 0.5) / n
        W += m.strip(P(u, arm(u) - 0.3, 0.0), P(u + 0.15 * u / L * 3, edge(u), 0.0), L / n * 1.18, pv, BACK, k)
    W += m.bone([P(L * t, arm(L * t), 0.35) for t in (0.0, 0.25, 0.5, 0.75, 1.0)], 2.0, 0.9, pv, BACK)
    for f in FING[1:]:
        u = L * f
        if f in claws:
            W += m.claw(P(u, arm(u), 0.4), P(u + 2.2, edge(u) - 3.4, 0.4), 0.7, pv, BACK)
    for t in eyes:
        u = L * t
        W += m.eye(P(u, (arm(u) + edge(u)) / 2 + 0.5, 0.45), 1.3, pv, BACK)
    return W


def great_open(m, sx, raise_=0.0):
    """the upper wing over the middle one, both spread (as it glides: out along x, toward the feet -y, its back +z); raise_:
    both turned up in their plane (the inventory model's V)"""
    pv = PIVOT['w1r' if sx > 0 else 'w1l']
    W = _open_wing(m, sx, pv, 36.0, 17.0, 7.0, 10.0 + raise_, (0.0, 0.0), 4.8, 2.0, (FING[2], FING[4], FING[6]), (0.18, 0.4, 0.58, 0.76))
    W += _open_wing(m, sx, pv, 30.0, 13.0, 4.0, -22.0 + raise_, (0.6, -4.0), 4.2, 2.1, (FING[3], FING[6]), (0.35, 0.7))
    return W


def great_folded(m, sx):
    """the upper and middle wings folded down the back: a layered cloak - the upper outer and longest, its bone arching over
    the shoulder to a claw/plume above it and down the outer edge to the hem; the middle beneath it, peeking out at the side"""
    pv = PIVOT['w1r' if sx > 0 else 'w1l']
    Pz = lambda x, y, d: (sx * x, y, 3.8 + 0.4 * x + 0.22 * max(0.0, 21.0 - y) + d)
    W = []
    for layer, (arch, hem, d, n, w) in enumerate((
            ([(1.4, 21.4), (3.0, 26.6), (5.0, 30.2), (7.0, 31.2), (8.6, 28.6), (9.8, 21.0), (11.0, 12.0), (12.2, 3.6)],
             [(0.0, 5.0), (2.0, 4.4), (4.2, 3.8), (6.4, 3.4), (8.6, 3.2), (10.6, 3.4), (12.4, 3.8)], 1.2, 7, 2.6),
            ([(2.6, 22.0), (5.2, 25.0), (8.4, 25.4), (10.8, 22.0), (12.6, 14.0), (13.6, 6.0)],
             [(4.6, 8.0), (7.0, 7.0), (9.4, 6.0), (11.6, 5.4), (13.4, 5.6)], 0.4, 5, 2.4))):
        top = [rigkit_poly(arch[:4] if layer == 0 else arch[:3], (k + 0.5) / n) for k in range(n)]
        for k in range(n):
            bx, by = hem[min(k, len(hem) - 1)]
            W += m.strip(Pz(*top[k], d + 0.08 * k), Pz(bx, by, d + 0.08 * k), w, pv, BACK, k + 10 * layer)
        W += m.bone([Pz(x, y, d + 0.9) for x, y in arch], 1.5 - 0.4 * layer, 0.7, pv, BACK)
    W += m.claw(Pz(7.0, 31.2, 2.2), Pz(7.6, 34.6, 2.4), 0.8, pv, BACK)                     # (the claw / plume over the shoulder)
    for (x, y) in ((8.6, 13.0), (4.8, 18.0), (6.6, 7.0), (12.4, 10.0)):
        W += m.eye(Pz(x, y, 2.2), 1.2, pv, rigkit._unit((0.35 * sx, 0.0, 1.0)))
    return W


def rigkit_poly(pts, t):
    L = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]; s = t * sum(L)
    for i, l in enumerate(L):
        if s <= l or i == len(L) - 1:
            k = min(1.0, s / l); return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * k, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * k)
        s -= l


def lower(m, opened):
    """the lower pair, both sides: round the legs to the feet at rest; fanned out beneath in flight"""
    pv = PIVOT['lw']; W = []
    for sx in (1, -1):
        if not opened:
            lead = [(1.6, 12.6, 3.8), (4.2, 12.0, 4.4), (6.4, 10.2, 3.6), (7.4, 7.6, 1.6), (7.6, 5.0, -0.6), (7.2, 3.0, -2.2)]
            for k in range(6):
                t = (k + 0.5) / 6
                i = min(4, int(t * 5)); f = t * 5 - i
                r = tuple(lead[i][j] + (lead[i + 1][j] - lead[i][j]) * f for j in range(3))
                out = rigkit._unit((r[0] - 0.5, 0.0, r[2] + 0.6))
                W += m.strip((sx * r[0], r[1], r[2]), (sx * (r[0] + out[0] * 1.2), 2.0 + 0.2 * k, r[2] + out[2] * 1.2), 2.3, pv,
                             rigkit._unit((sx * out[0], 0.0, out[2])), k + 3 * (sx > 0))
            W += m.bone([(sx * x, y, z + 0.5) for x, y, z in lead], 1.0, 0.5, pv, rigkit._unit((0.4 * sx, 0.0, 1.0)))
        else:
            W += _open_wing(m, sx, pv, 22.0, 9.0, 2.0, -48.0, (1.2, 0.0), 4.6, 2.0, FING[3:], (0.5,))
    return W


def halo(m):
    """behind the head: the Last Night's burning ring of eyes (black iron, embers, spikes) / the First Light's three rings"""
    pv = PIVOT['halo']; X, Y, Z = pv; W = []
    ring = lambda r, n, w, h, tex, light, a0=0.0: [SA.SEG((X + r * math.cos(a0 + 2 * math.pi * i / n), Y + r * math.sin(a0 + 2 * math.pi * i / n), Z),
                                                           (X + r * math.cos(a0 + 2 * math.pi * (i + 1) / n), Y + r * math.sin(a0 + 2 * math.pi * (i + 1) / n), Z),
                                                           w, h, tex, pv, (0.0, 0.0, 1.0), ext=0.12, light=light) for i in range(n)]
    if m.kind == 'night':
        W += ring(6.2, 20, 0.9, 0.6, 'ds_iron', 0)
        W += ring(5.4, 20, 0.35, 0.5, 'ds_red_l', 13)
        for i in range(10):
            a = 2 * math.pi * i / 10
            p0 = (X + 6.4 * math.cos(a), Y + 6.4 * math.sin(a), Z)
            p1 = (X + (8.4 + 0.8 * (i % 2)) * math.cos(a), Y + (8.4 + 0.8 * (i % 2)) * math.sin(a), Z)
            W.append(SA.SEG(p0, p1, 0.5, 0.5, 'ds_horn_r', pv, (0.0, 0.0, 1.0), uv=FULL()))
        for i in range(6):
            a = 2 * math.pi * (i + 0.25) / 6
            W += m.eye((X + 6.2 * math.cos(a), Y + 6.2 * math.sin(a), Z + 0.45), 1.0, pv, (0.0, 0.0, 1.0))
    else:
        W += ring(4.4, 18, 0.7, 0.45, 'dvn_halo', 15)
        W += ring(6.0, 22, 0.45, 0.4, 'dvn_halo_w', 15, 0.07)
        W += ring(7.6, 26, 0.6, 0.45, 'dvn_halo', 15, 0.03)
        for i in range(16):
            a = 2 * math.pi * i / 16; r0, r1 = 8.2, 9.4 + 1.2 * (i % 2)
            e = SA.SEG((X + r0 * math.cos(a), Y + r0 * math.sin(a), Z), (X + r1 * math.cos(a), Y + r1 * math.sin(a), Z), 0.35, 0.35, 'dvn_light', pv,
                       (0.0, 0.0, 1.0), light=15); e['shade'] = False; W.append(e)
        for i in range(8):
            a = 2 * math.pi * (i + 0.5) / 8
            W.append(SA.GEM((X + 6.0 * math.cos(a), Y + 6.0 * math.sin(a), Z + 0.2), 0.7, 'dvn_gem', pv, light=15))
    for e in W:
        if 'shade' not in e and any(f['texture'][1:].startswith('dvn_halo') for f in e['faces'].values()): e['shade'] = False
    return W


# ---------------------------------------------------------------------------------------------------- the two arts (seraph_wings' API)
_RAW = {}


def _build(kind):
    if kind in _RAW: return _RAW[kind]
    m = Mat(kind); p = {'night': 'svn_', 'light': 'svl_'}[kind]
    _rs.seed(7 if kind == 'night' else 8); SA._rs.seed(2999)
    R = {}
    for sx, s in ((1, 'r'), (-1, 'l')):
        R[f'{p}w1{s}'] = (great_folded(m, sx), 1.0)
        R[f'{p}w1{s}_o'] = (great_open(m, sx), OPEN_K)
    R[f'{p}lw'] = (lower(m, False), 1.0)
    R[f'{p}lw_o'] = (lower(m, True), LOW_K)
    R[f'{p}halo'] = (halo(m), 1.0)
    _RAW[kind] = R
    return R


def models(kind):
    M = {}
    for name, (els, k) in _build(kind).items():
        els = rigkit.shrink(els, k) if k != 1.0 else els
        for e in els:
            for v in e['from'] + e['to']:
                assert -16 <= v <= 32, (name, e['from'], e['to'])
            for fc in e['faces'].values():
                fc['uv'] = [max(0.0, min(16.0, c)) for c in fc['uv']]
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)
    return M


def _spin(deg, tilt=0.0):
    return dq(('x', tilt), ('z', deg))


def _poses(slow):
    """the poses (both arts share them: the same wings). slow: the Last Night's heavier beat"""
    lw = lambda tilt: dq(('x', tilt))
    P = lambda b, w1, l, h, opened=False, **kw: dict(dict(b), w1r=w1[0], w1l=w1[1], lw=l, halo=h, _open=opened, **kw)
    pr = lambda **kw: (wing(1, **kw), wing(-1, **kw))
    return {
        'rest_a': P({}, pr(), lw(0.0), _spin(0.0)),
        'rest_b': P({}, pr(raise_=3.5, tilt=4.0), lw(5.0), _spin(-24.0 if slow else 24.0), _k_halo=1.08),     # (the breath)
        'sneak': P(dict(CROUCH, _o_lw=(0.0, 2.6, -1.0)), pr(raise_=15.0, back=-4.0, tilt=4.0), lw(32.0), _spin(0.0, 0.0)),
        'ride': P({}, pr(raise_=-1.0, tilt=-2.0), lw(70.0), _spin(0.0)),
        'glide_a': P(GLIDE, pr(raise_=36.0, back=6.0, tilt=10.0), lw(-6.0), _spin(20.0, -15.0), True),
        'glide_b': P(GLIDE, pr(raise_=(10.0 if slow else 18.0), back=10.0, tilt=18.0), lw(4.0), _spin(-20.0, -15.0), True),
        'fall_a': P({}, pr(raise_=52.0, back=18.0, tilt=10.0), lw(18.0), _spin(30.0), True),
        'fall_b': P({}, pr(raise_=14.0, back=8.0, tilt=-6.0), lw(8.0), _spin(-30.0), True),
        'furl': P({}, pr(raise_=-78.0, back=10.0), lw(0.0), _spin(0.0), True),
        'furl_glide': P(GLIDE, pr(raise_=-78.0, back=10.0), lw(0.0), _spin(0.0, -15.0), True),
    }


class Art:
    """one set's art for seraph_wings' runtime: PIVOT, PARENT, PARTS, POSES, STATES, model_of, model_k, S, U"""
    def __init__(self, kind):
        self.kind, self.PREFIX = kind, {'night': 'svn_', 'light': 'svl_'}[kind]
        self.PIVOT, self.PARENT, self.PARTS, self.S, self.U = PIVOT, PARENT, PARTS, S, U
        slow = kind == 'night'
        self.POSES = _poses(slow)
        self.STATES = {1: ('rest', 'rest_a', 6, False, (60, 'rest_a', 'rest_b')),
                       2: ('sneak', 'sneak', 4, False, None),
                       3: ('glide', 'glide_a', 8, True, ((26, 'glide_a', 'glide_b') if slow else (18, 'glide_a', 'glide_b'))),
                       4: ('fall', 'fall_a', 6, True, ((10, 'fall_a', 'fall_b') if slow else (7, 'fall_a', 'fall_b'))),
                       5: ('ride', 'ride', 5, False, None)}

    def model_of(self, p, pz):
        if p in ('w1r', 'w1l', 'lw') and pz.get('_open'): return f'{self.PREFIX}{p}_o'
        return f'{self.PREFIX}{p}'

    def model_k(self, name):
        return OPEN_K if name.endswith('w1r_o') or name.endswith('w1l_o') else (LOW_K if name.endswith('lw_o') else 1.0)


NIGHT, LIGHT = Art('night'), Art('light')


# ---------------------------------------------------------------------------------------------------- icons, the 3D gui model, the elytra layers
SPR = {'k': (8, 6, 10), 'v': (22, 16, 26), 'V': (40, 28, 46), 'l': (64, 46, 72), 'r': (208, 24, 46), 'R': (255, 90, 100), 'w': (255, 196, 170),
       'b': (90, 70, 96), 'e': (236, 226, 216),
       'W': (255, 255, 255), 'p': (250, 246, 232), 'P': (232, 224, 206), 's': (198, 186, 160), 'g': (255, 222, 118), 'G': (234, 184, 58),
       'h': (170, 116, 28), 'f': (255, 245, 200), 'y': (255, 250, 232)}
ICON_ROWS = [  # (one silhouette for both: two great wings raised in a V on bones, eyes / gems in them, the halo between, the lower pair)
    'b..............b',
    'Vb....rRRr....bV',
    'vVb..R....R..bVv',
    'vrVb.R....R.bVrv',
    'vvvVbkrRRrkbVvvv',
    'kvRvVbkwwkbVvRvk',
    '.vvvvVbkkbVvvvv.',
    '.kvrvvVbbVvvrvk.',
    '..kvvvvVVvvvvk..',
    '..k.kvvkkvvk.k..',
    '.....kvbbvk.....',
    '....kvVkkVvk....',
    '...kvrk..krvk...',
    '...kk......kk...',
    '................',
    '................']
NIGHT_PAL = {'b': (96, 74, 104), 'V': (46, 32, 54), 'v': (24, 16, 28), 'k': (8, 6, 10), 'r': (208, 24, 46), 'R': (255, 90, 100), 'w': (255, 196, 170)}
LIGHT_PAL = {'b': (255, 222, 118), 'V': (255, 253, 246), 'v': (236, 230, 216), 'k': (170, 116, 28), 'r': (255, 245, 200), 'R': (255, 250, 232), 'w': (255, 255, 255)}


def icons():
    out = {}
    for iid, pal in (('sov_wings', NIGHT_PAL), ('sov_wings_holy', LIGHT_PAL)):
        im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); px = im.load()
        for y, row in enumerate(ICON_ROWS):
            for x, ch in enumerate(row):
                if ch != '.': px[x, y] = pal[ch] + (255,)
        out[iid] = im
    return out


def gui_model(kind):
    """the spread wings, both sides, small enough for the inventory and a frame: the open great wings (as they glide, seen from
    behind - their textured side) and the halo between them, scaled about the body into the model box"""
    m = Mat(kind); _rs.seed(7 if kind == 'night' else 8); SA._rs.seed(2999)
    k, c = 0.235, (0.0, 30.0, 5.0)
    out = []
    for part, els in (('w1r', great_open(m, 1, 30.0)), ('w1l', great_open(m, -1, 30.0)), ('halo', halo(m))):
        pv = PIVOT[part]
        out += rigkit.transform(els, lambda v, pv=pv: [8 + (v[i] - 8 + pv[i] - c[i]) * k for i in range(3)])
    return out


def wings_layer(kind):
    """the elytra mesh cut back to a mantle (7 of its 20 rows), as the Seraph's"""
    im = Image.new('RGBA', (64, 32), (0, 0, 0, 0)); px = im.load()
    rows = {'night': ['bkvVvlvVrv', 'bkvRwRvVvl', 'bkVvrvlVvV', 'lkvVvVrvlv', 'lkvlRwRvVv', 'lkVvvrvVvl', 'k.r.v.r.v.'],
            'light': ['gGpWpPpWpP', 'gGpPpfpPpW', 'gGWpPpWpPp', 'hGpPgPpWpP', 'hGpWpPpfpW', 'hGPpPpPpgP', 'h.f.y.f.y.']}[kind]
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch != '.': px[36 + c, 2 + r] = SPR[ch] + (255,)
    return im


GUI_DISPLAY = {'gui': {'rotation': [-12, 0, 0], 'translation': [0, 0, 0], 'scale': [1.0, 1.0, 1.0]},
               'fixed': {'rotation': [0, 180, 0], 'translation': [0, 0, 0], 'scale': [1.0, 1.0, 1.0]}}


def rp(R):
    """gen_rp (phase 2: the ds_ and dvn_ textures are the Sovereign's and the Divine One's): the 3D wings, the halo, the icons
    (a sprite, and a 3D model in the inventory and in frames), the equipment assets"""
    for kind in ('night', 'light'):
        for name, (tex, els) in models(kind).items():
            R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + ('svn_', 'svl_')
    R.ICONS.update({f'{iid}_sprite': im for iid, im in ((ITEMS[k], icons()[ITEMS[k]]) for k in ITEMS)})
    def post(R2):
        for kind, iid in ITEMS.items():
            els = gui_model(kind)
            for e in els:
                for v in e['from'] + e['to']: assert -16 <= v <= 32, (iid, e)
                for fc in e['faces'].values(): fc['uv'] = [max(0.0, min(16.0, c)) for c in fc['uv']]
            used = sorted({f['texture'][1:] for e in els for f in e['faces'].values()})
            R2.wj(f'assets/bm/models/item/{iid}_3d.json', {'textures': dict({t: f'bm:block/{t}' for t in used}, particle=f'bm:block/{used[0]}'),
                                                          'elements': els, 'display': GUI_DISPLAY})
            sel = {'type': 'minecraft:select', 'property': 'minecraft:display_context',
                   'cases': [{'when': ['gui', 'fixed'], 'model': {'type': 'minecraft:model', 'model': f'bm:item/{iid}_3d'}}],
                   'fallback': {'type': 'minecraft:model', 'model': f'bm:item/{iid}_sprite'}}
            R2.wj(f'assets/bm/items/{iid}.json', {'model': sel})
            # (3.0c - flat_wings: the whole elytra by default; this mantle under the 3D wings when they're switched on)
            import flat_wings as FW
            (FW.sov_night if kind == 'night' else FW.sov_light)().save(R2.p('assets', 'bm', 'textures', 'entity', 'equipment', 'wings', f'{iid}.png'))
            wings_layer(kind).save(R2.p('assets', 'bm', 'textures', 'entity', 'equipment', 'wings', f'{iid}_mantle.png'))
            R2.wj(f'assets/bm/equipment/{iid}.json', {'layers': {'wings': [{'texture': f'bm:{iid}'}]}})
            R2.wj(f'assets/bm/equipment/{iid}_mantle.json', {'layers': {'wings': [{'texture': f'bm:{iid}_mantle'}]}})
    R.POST.append(post)

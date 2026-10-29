"""2.99 (v299): THE DREAD CARAPACE'S WINGS IN 3D - the dark mirror of the Seraph's (seraph_wings.py runs both: its SETS table).
Four item displays per wearer, the same parts, states, swaps and cleanup as the Seraph's:
  w1r, w1l  the great wings - tattered black membrane on bone spars, red veins in it, eyes in it. FOLDED like a bat's at rest:
            the arm-spar rises from the shoulder blade to a hooked claw above the shoulder (higher than the Seraph's arch: they
            stand up behind the head like horns), the finger-spars run down the back, the membrane hangs between them in torn
            scallops to the calves. OPEN for flight: the arm out to the wrist and its claw, four fingers fanned from it, the
            membrane stretched between in scallops, torn at its edge. A slower, heavier beat than the Seraph's.
  w2r, w2l  the Dread's answer to the lower pair: a ragged TAIL behind the legs - streamers of torn membrane from the small of
            the back, chains swagged between them, a bone spur at the root - in two halves, so it sways and parts.
Poses, models and transforms in the Seraph's own conventions (design units of 1/16 block, feet at y 0, facing -z, the wearer's
right +x); seraph_wings.xforms / render take this module as `art`."""
import math

import rigkit
import seraph_art as SA
import dread_art as DK
from seraph_art import SEG, GEM, FULL
from seraph_wings import PIVOT, PARENT, PARTS, S, U, wing, pose, pair, CROUCH, GLIDE

PREFIX = 'dkw_'
OPEN_K = 1.5
BACK = (0.0, 0.0, 1.0)


def _P(sx, p):
    return (sx * p[0], p[1], p[2])


def _win(w, k):
    """a membrane strip's uv: the whole length (its torn end at the end), a window across as wide as the strip (two texels a
    unit, as the rest of the pack's 3D art) - each strip its own, so the veins don't repeat strip by strip"""
    wu = max(1.0, min(16.0, w))
    u0 = round((k * 5.3 + w * 3.1) % (16.0 - wu + 1e-6), 3)
    return {'up': [u0, 0, u0 + wu, 16], 'down': [u0, 16, u0 + wu, 0], 'east': [0, 0, 0.5, 16], 'west': [0, 0, 0.5, 16], 'north': [0, 0, 1, 0.5], 'south': [0, 0, 1, 0.5]}


def _fan(W, A, B, n, sag, tex, pv, up, z0=0.0, dz=0.05, w_k=1.25, light=0):
    """membrane between two spars from a common joint W to their tips A and B: n strips fanned from W to points along A..B,
    the edge sagging toward W between the tips (a bat wing's scallop) - each strip a little proud of the last (no z-fight)"""
    out = []
    span = math.dist(A, B)
    for k in range(n):
        t = (k + 0.5) / n
        P_ = tuple(A[i] + (B[i] - A[i]) * t for i in range(3))
        s = sag * math.sin(math.pi * t)
        P_ = tuple(P_[i] + (W[i] - P_[i]) * s for i in range(3))
        off = tuple(up[i] * (z0 + dz * k) for i in range(3))
        w = span / n * w_k
        out.append(SEG(tuple(W[i] + off[i] for i in range(3)), tuple(P_[i] + off[i] for i in range(3)), w, 0.22,
                       'dk_membrane' if k % 2 == 0 else 'dk_membrane_b', pv, up, uv=_win(w, k), light=light))
    return out


def _spar(pts, w, pv, up):
    return DK.CHAIN(pts, w, 'dk_horn', pv, up)


def great_folded(sx):
    """FOLDED like a bat's: the arm-spar up from the shoulder blade to a hooked claw over the shoulder, four finger-spars down
    the back to the calves (the outer flaring out and back, an A-line over the elytra mesh as the Seraph's), the membrane
    hanging between them in torn scallops, eyes in it"""
    pv = PIVOT['w1r' if sx > 0 else 'w1l']; P = lambda p: _P(sx, p)
    z = lambda x, y: 3.6 + 0.36 * x + 0.2 * max(0.0, 21.0 - y)
    Z = lambda x, y, d=0.0: P((x, y, z(x, y) + d))
    root, wrist = Z(1.5, 20.4, 0.9), Z(6.4, 31.4, 1.0)
    W = _spar([root, Z(3.6, 25.6, 1.0), wrist], (1.5, 1.0), pv, BACK)
    W += _spar([wrist, Z(6.9, 33.2, 1.1), Z(5.9, 34.4, 1.2)], (0.8, 0.3), pv, BACK)            # the hooked claw
    tips = [Z(10.9, 1.8, 0.95), Z(8.2, 1.2, 0.9), Z(5.2, 2.0, 0.85), Z(2.2, 4.2, 0.8)]
    for k, t in enumerate(tips):                                                                  # the finger-spars, bowed out
        mid = Z((6.4 + (t[0] * sx)) / 2 + 1.2 - 0.3 * k, (31.4 + t[1]) / 2, 1.0)
        W += _spar([wrist, mid, t], (0.75, 0.35), pv, BACK)
    inner = Z(1.0, 12.0, 0.7)
    for k, (A, B) in enumerate(zip(tips, tips[1:] + [inner])):                                   # the membrane between them
        W += _fan(wrist, A, B, 3, 0.16, 'dk_membrane', pv, BACK, z0=-0.15 - 0.04 * k, dz=0.04)
    W += _fan(wrist, inner, root, 2, 0.05, 'dk_membrane', pv, BACK, z0=-0.3, dz=0.04)            # (and down to the root)
    for (x, y) in ((8.2, 12.5), (4.6, 16.0), (6.8, 6.0)):
        W += DK.EYE(Z(x, y, 1.0), 1.5, 0.9, (0.32 * sx, 0.0, 1.0), pv, d=0.28, light=12)
    return W


# the open wing: (u out along the span, v up) from the root - the wrist, its claw, four finger tips, the low body point
OPEN = dict(wrist=(10.0, 7.0), claw=(11.0, 10.0), tips=[(29.0, 3.5), (26.0, -7.0), (19.5, -14.0), (12.0, -16.0)], low=(1.5, -12.0))


def great_open(sx):
    """OPEN (built spread as it glides: out along x, toward the feet -y, its back +z): the arm out to the wrist and its claw,
    four fingers fanned from it, membrane stretched between them in torn scallops, red eyes in it"""
    pv = PIVOT['w1r' if sx > 0 else 'w1l']; X, Y, Z0 = pv
    Pt = lambda u, v, w=0.0: (X + sx * u, Y + v, Z0 + 4.5 + 0.04 * u + w)
    root, wrist = Pt(0, 0, 0.3), Pt(*OPEN['wrist'], 0.3)
    W = _spar([root, Pt(5.0, 4.6, 0.3), wrist], (1.8, 1.2), pv, BACK)
    W += _spar([wrist, Pt(*OPEN['claw'], 0.35), Pt(10.2, 11.6, 0.4)], (0.9, 0.35), pv, BACK)
    tips = [Pt(*t, 0.25) for t in OPEN['tips']]
    for k, (tu, tv) in enumerate(OPEN['tips']):
        mu, mv = (OPEN['wrist'][0] + tu) / 2, (OPEN['wrist'][1] + tv) / 2 + 1.0
        W += _spar([wrist, Pt(mu, mv, 0.25), tips[k]], (0.9, 0.4), pv, BACK)
    low = Pt(*OPEN['low'], 0.1)
    for k, (A, B) in enumerate(zip(tips, tips[1:] + [low])):
        W += _fan(wrist, A, B, 4 if k < 3 else 3, 0.2, 'dk_membrane', pv, BACK, z0=-0.1 - 0.05 * k, dz=0.04)
    W += _fan(wrist, low, root, 2, 0.06, 'dk_membrane', pv, BACK, z0=-0.35, dz=0.04)
    for (u, v) in ((16.0, -4.0), (22.0, -6.5), (8.0, -6.5), (13.5, -10.5)):
        W += DK.EYE(Pt(u, v, 0.35), 1.6, 1.0, BACK, pv, d=0.28, light=12)
    return W


def tail(sx):
    """half the ragged tail: streamers of torn membrane from the small of the back, a chain swagged between them, a spur"""
    pv = PIVOT['w2r' if sx > 0 else 'w2l']; P = lambda p: _P(sx, p)
    W = []
    for k, (x, z, L, lean) in enumerate(((0.5, 4.2, 10.8, 0.1), (2.4, 4.8, 9.6, 0.5), (4.2, 5.0, 8.0, 0.9))):
        A = P((x, 12.4, z)); B = P((x + lean, 12.4 - L, z + 0.9 + 0.3 * k))
        W.append(SEG(A, B, 2.2 - 0.25 * k, 0.22, 'dk_membrane' if k % 2 == 0 else 'dk_membrane_b', pv, BACK, uv=_win(2.2 - 0.25 * k, k + 3)))
    for k, (y0, y1, x1) in enumerate(((11.6, 7.2, 4.4), (8.6, 4.6, 3.0))):                        # chains swagged between
        a, m, b = P((0.4, y0, 5.6 + 0.2 * k)), P(((0.4 + x1) / 2, y1, 6.2 + 0.2 * k)), P((x1, y0 - 1.2, 6.0 + 0.2 * k))
        W += [SEG(a, m, 0.7, 0.7, 'dk_chain', pv, BACK, uv=FULL()), SEG(m, b, 0.7, 0.7, 'dk_chain', pv, BACK, uv=FULL())]
    W += DK.CHAIN([P((1.4, 12.6, 3.6)), P((1.8, 11.4, 6.2)), P((2.0, 10.2, 7.6))], (0.9, 0.3), 'dk_horn', pv, (0.0, 1.0, 0.0))  # the spur
    W.append(GEM(P((2.6, 2.0, 5.8)), 0.5, 'dk_ember', pv, light=13))
    return W


_RAW = {}


def _build():
    if _RAW: return _RAW
    SA._rs.seed(4199)
    for sx, s in ((1, 'r'), (-1, 'l')):
        _RAW[f'{PREFIX}w1{s}'] = (great_folded(sx), 1.0)
        _RAW[f'{PREFIX}w1{s}_o'] = (great_open(sx), OPEN_K)
        _RAW[f'{PREFIX}w2{s}'] = (tail(sx), 1.0)
    return _RAW


def models():
    M = {}
    for name, (els, k) in _build().items():
        els = rigkit.shrink(els, k) if k != 1.0 else els
        for e in els:
            for v in e['from'] + e['to']:
                assert -16 <= v <= 32, (name, e['from'], e['to'])
            for fc in e['faces'].values():
                fc['uv'] = [max(0.0, min(16.0, c)) for c in fc['uv']]
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)
    return M


def model_k(name):
    return OPEN_K if name.endswith('_o') else 1.0


def model_of(p, pz):
    if p.startswith('w1') and pz.get('_open'): return f'{PREFIX}{p}_o'
    return f'{PREFIX}{p}'


# a slower, heavier beat than the Seraph's; the tail swaying, trailing, flung up when falling
POSES = {
    'rest_a': pose({}, pair(wing), pair(wing)),
    'rest_b': pose({}, pair(wing, raise_=2.0, tilt=2.5), pair(wing, raise_=4.0, back=3.0, tilt=5.0)),
    'sneak': pose(dict(CROUCH, _o_w2r=(0.0, 2.6, -1.0), _o_w2l=(0.0, 2.6, -1.0)), pair(wing, raise_=17.0, back=-4.0, tilt=4.0), pair(wing, raise_=6.0, tilt=34.0)),
    'ride': pose({}, pair(wing, raise_=-1.5, tilt=-2.0), pair(wing, raise_=8.0, tilt=70.0)),
    'glide_a': pose(GLIDE, pair(wing, raise_=38.0, back=6.0, tilt=10.0), pair(wing, raise_=10.0, tilt=-8.0), True),
    'glide_b': pose(GLIDE, pair(wing, raise_=14.0, back=10.0, tilt=18.0), pair(wing, raise_=4.0, tilt=6.0), True),
    'fall_a': pose({}, pair(wing, raise_=55.0, back=20.0, tilt=12.0), pair(wing, raise_=16.0, tilt=38.0), True),
    'fall_b': pose({}, pair(wing, raise_=12.0, back=8.0, tilt=-6.0), pair(wing, raise_=10.0, tilt=24.0), True),
    'furl': pose({}, pair(wing, raise_=-78.0, back=10.0), pair(wing), True),
    'furl_glide': pose(GLIDE, pair(wing, raise_=-78.0, back=10.0), pair(wing), True),
}
STATES = {1: ('rest', 'rest_a', 6, False, (50, 'rest_a', 'rest_b')),
          2: ('sneak', 'sneak', 4, False, None),
          3: ('glide', 'glide_a', 8, True, (22, 'glide_a', 'glide_b')),
          4: ('fall', 'fall_a', 6, True, (9, 'fall_a', 'fall_b')),
          5: ('ride', 'ride', 5, False, None)}


def textures():
    return {}                                             # (dread_art's dk_ textures are written with the Visage - dread_armor.rp)


def rp(R):
    for name, (tex, els) in models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (PREFIX,)

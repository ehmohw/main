"""2.99 (v299): THE SERAPH'S WINGS IN 3D - what others see on a player wearing the Seraph's Wings (the holy Dread Carapace).
"With two they covered their faces (the helm's), with two they covered their feet, and with two they were flying."

A player can't carry passengers (/ride refuses players), so the wings are item displays the data pack keeps on the wearer:
FOUR PER WEARER (w1r, w1l: the great flying wings; w2r, w2l: the lower wings over the legs and feet), summoned at the
wearer's feet and teleported there every tick (teleport_duration 3, the same lerp the game gives a remote player, so the two
move together), turned to the wearer's yaw (Rotation[0]: a body's own yaw isn't readable) - and while gliding to the wearer's
pitch too (the body lies along the flight: the game turns the gliding model about the feet by the look pitch). Each wing's
place and turn is its display's transformation (a rigkit pose solved about a virtual 'body' root - the lean of a crouch, the
lie of a glide - and interpolated by the client), so a pose costs one data merge per display, only when it changes.

THE STATES (bm.sws on the wearer; bm:p206w/<set>/pick each tick)
  0 hidden    invisible, spectating, sleeping, swimming - or not wearing it (the displays are killed; back when it ends)
  1 rest      the great wings FOLDED down the back (their arch over the shoulders, the hem burning at the calves), the lower
              wings round the legs to the feet; a slow idle sway (rest_a / rest_b, 40 ticks each way)
  2 sneak     the body's lean (as the game crouches it), the great wings drawn round the body like a mantle (the vanilla
              elytra mesh flares wide in a crouch - out to 1 block each side - and a tighter fold would leave it showing; the
              mantle closes over it), the lower wings drawn up clear of the crouched legs
  3 glide     the body along the flight (pitched with the look), the great wings OPEN, spread wide, beating slowly
              (glide_a / glide_b, 15 ticks each way), the lower wings trailing along the legs
  4 fall      upright, falling (fall distance over 3.5): the great wings open, raised in a V and beating fast (6 ticks each)
  5 ride      on a mount: folded close, the lower wings swept back along the mount
The great wings have two models each - folded (sw_w1r) and open (sw_w1r_o): a folded wing's feathers hang down its length,
an open wing's down from its leading edge, and no turn makes one the other. They swap on the way between folded and open
states: opening, the open model is shown furled (pointing down the back, a tick) and then opens (6 ticks); closing, it furls
(5 ticks) and the folded model takes its place.

CHEAP: per wearer per tick, one items check, one pick (a few predicates), one selector pass over its own four displays (an
AABB lookup, 12 blocks) to teleport them. Poses only on a state change and at the cycle's keys. Orphans (the wearer logged
out, died, changed dimension, was teleported away) are swept four times a second: a display whose wearer (bm.pid) isn't
alive within 12 blocks is killed; a wearer whose displays are gone gets a new set (loop/fast).

GLOW (CLAUDE.md): nothing here glows - the displays never take Glowing (an invisible host's outline rule doesn't apply: the
wearer is a visible player, and the wings are hidden whenever the wearer is invisible).

GENERIC: sets() is the table of wing sets - each its worn conditions (on the chest slot), its art module (parts, pivots, poses,
models: this module for the Seraph, dread_wings.py for the Dread Carapace - the carapace NOT made holy) and its states; each
gets its own bm:p206w/<set>/... and its own display tags (bm.swd_<set>), so a set's sweep never touches another's.

Design units: 1/16 block (the player model's pixels x 0.9375), feet at y=0, facing -z, the wearer's right +x."""
import math
import random
import sys

import rigkit
from rigkit import qs, D, qrot
import seraph_art as A
from seraph_art import SEG, GEM, FULL, EYEBOX

PREFIX = 'sw_'
S = 1.0                                         # (the displays' scale: a design unit is 1/16 block)
U = S / 16
K = 0.9375                                      # (player px -> design units)
PIVOT = {'body': (0.0, 24 * K, 0.0),
         'w1r': (1.5, 20.4, 3.3), 'w1l': (-1.5, 20.4, 3.3),
         'w2r': (1.7, 12.2, 3.1), 'w2l': (-1.7, 12.2, 3.1)}
PARENT = {'body': None, 'w1r': 'body', 'w1l': 'body', 'w2r': 'body', 'w2l': 'body'}
PARTS = ('w1r', 'w1l', 'w2r', 'w2l')            # (the displays: 'body' is only the root they turn about)
PART_K = {'w1r': 1.0, 'w1l': 1.0, 'w2r': 1.0, 'w2l': 1.0}
OPEN_K = 1.45                                   # (the open wings are built at full size, kept inside the model box)
UP, FRONT, BACK = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0), (0.0, 0.0, 1.0)


# ---------------------------------------------------------------------------------------------------- the textures (seraph_art's, and two long quills)
def _quill(seed, dark=False):
    """a long feather (whole uv, its length down v - drawn for a feather ~8x as long as it's wide, so the barbs, nearly level
    here, slant at 45 degrees on the feather): a gold-white shaft, the vane lit on one side, shaded on the other, darker edges,
    the root tucked in shadow, a faint gold flush toward the tip"""
    lo, mid, hi = (A.P3, A.P2, A.P1) if dark else (A.P2, A.P1, A.WHITE)
    def c(x, y, r):
        if x in (15, 16): return A._c(A._mix(A.G1, A.WHITE, 0.5) if y > 1 else A.G2)
        if x <= 2 or x >= 29: return A._c(A._mix(lo, A.P4, 0.55))
        left = x < 15
        u = x if left else 31 - x
        if (y * 6 + (15 - u)) % 22 < 3: return A._c(A._mix(lo, A.P4, 0.3))                   # (the barbs)
        b = (hi if r.random() > 0.2 else mid) if left else (mid if r.random() > 0.25 else lo)
        if y < 3: b = A._mix(b, A.P4, 0.45)
        if y > 26: b = A._mix(b, A.G0, (y - 26) / 10)
        return A._c(b)
    return A._paint(c, seed)


def textures():
    """(seraph_art's textures are registered by dread_set_art; these are the wings' own)"""
    return {'sr_quill': _quill(3101), 'sr_quill_d': _quill(3102, True)}


# ---------------------------------------------------------------------------------------------------- building
def _P(sx, p):
    return (sx * p[0], p[1], p[2])


def _lerp(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(len(a)))


def _poly(pts, t):
    """a point t (0..1) along a polyline"""
    L = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]; s = t * sum(L)
    for i, l in enumerate(L):
        if s <= l or i == len(L) - 1: return _lerp(pts[i], pts[i + 1], min(1.0, s / l))
        s -= l


def _feather(root, tip, w, tex, pv, up, burn=0.2, h=0.4):
    return A.FEATHER(root, tip, w, tex, pv, up, burn=burn, h=h)


def _lead(pts, w0, w1, pv, up, light=6):
    """the gold leading edge along a polyline, tapering"""
    n = len(pts) - 1; out = []
    for i in range(n):
        w = w0 + (w1 - w0) * i / max(1, n - 1)
        out.append(SEG(pts[i], pts[i + 1], w, w * 0.85, 'sr_gold', pv, up, ext=0.25, light=light))
    return out


def great_folded(sx):
    """a great wing FOLDED down the back (built in place, at rest): the leading edge rises from the root on the shoulder blade
    to an arch over the shoulder (a sapphire at the wrist), then runs down the outer edge to the hem at the calf, flaring
    out and back (an A-line: it closes over the elytra mesh's folded wing); seven long feathers hang from the arch to the
    hem, the outer ones laid over the inner, burning at their ends; two rows of coverts over the upper wing; eyes in them"""
    pv = PIVOT['w1r' if sx > 0 else 'w1l']; P = lambda p: _P(sx, p)
    z = lambda x, y: 3.5 + 0.36 * x + 0.2 * max(0.0, 21.0 - y)                    # (the wing's sheet: back from the body, flaring at the hem)
    lead = [(1.5, 20.4), (3.0, 25.2), (4.8, 28.6), (6.3, 29.9), (7.7, 27.6), (8.6, 21.5), (9.7, 13.5), (10.7, 5.5), (11.2, 1.6)]
    L3 = [P((x, y, z(x, y) + 0.9)) for x, y in lead]
    W = _lead(L3, 1.25, 0.6, pv, BACK)
    W.append(GEM(P((6.3, 29.9, z(6.3, 29.9) + 1.1)), 1.15, 'sr_saph', pv, light=12))
    # the long feathers: roots along the arch (outer first), tips along the hem
    n = 7
    for k in range(n):
        t = k / (n - 1)
        rx, ry = _poly([(7.4, 26.8), (6.2, 28.6), (4.6, 27.4), (3.2, 24.6), (2.2, 22.2), (1.4, 20.8)], t)
        tx, ty = 10.5 - 1.75 * k, 1.7 + 0.3 * k                                   # (the innermost crosses the spine: the two wings meet)
        lay = 0.1 * (n - 1 - k) + (0.12 if sx > 0 and k == n - 1 else 0.0)        # (the outer feathers over the inner; right over left)
        r = P((rx, ry, z(rx, ry) + lay)); tp = P((tx, ty, z(tx, ty) + lay))
        W += _feather(r, tp, 2.55, 'sr_quill' if k % 2 == 0 else 'sr_quill_d', pv, BACK, burn=0.16)
    # coverts: two rows over the upper wing, under the arch (lit, gold-tipped scales)
    for row, (y0, ln, cnt) in enumerate(((26.0, 4.8, 4), (21.8, 4.4, 4))):
        for j in range(cnt):
            x = 2.2 + 1.75 * j + (0.6 if row else 0.0) + (0.0 if j < 3 else 0.3)
            y = y0 + (0.9 if row == 0 and 0 < j < 3 else 0.0) - (1.4 if j == 3 and row == 0 else 0.0)
            zz = z(x, y) + 0.85 + 0.08 * row
            tex = 'sr_covert_eye' if (row, j) in ((0, 1), (1, 3)) else 'sr_covert'
            W.append(SEG(P((x, y, zz)), P((x + 0.4, y - ln, zz)), 2.0, 0.35, tex, pv, BACK, uv=FULL()))
    # eyes in the feathers, facing out
    for (x, y) in ((7.6, 10.5), (4.4, 14.0), (8.9, 4.5), (5.5, 6.2)):
        W.append(EYEBOX(P((x, y, z(x, y) + 0.9)), 1.6, 1.0, rigkit._unit((0.32 * sx, 0.0, 1.0)), pv, d=0.3, light=11))
    return W


# the open wing: its leading edge (u out along the span, v up) - the secondaries (u, length, lean) and primaries
OPEN = dict(lead=[(0.0, 0.0), (3.0, 2.6), (7.0, 4.6), (12.0, 5.3), (17.0, 4.8), (22.0, 3.2), (27.0, 0.8)],
            sec=[(1.6 + 2.0 * i, 8.6 + 0.4 * i, 0.03 + 0.01 * i) for i in range(6)],
            prim=[(13.4 + 2.3 * i, 11.5 + 0.7 * i - (0.7 * (i - 4) ** 2 if i > 4 else 0), 0.12 + 0.07 * i) for i in range(7)])


def _lead_v(u):
    for (u0, v0), (u1, v1) in zip(OPEN['lead'], OPEN['lead'][1:]):
        if u <= u1: return v0 + (v1 - v0) * (u - u0) / (u1 - u0)
    return OPEN['lead'][-1][1]


def great_open(sx):
    """a great wing OPEN (built spread, as it glides: out along x, its feathers hanging toward the feet, its back to +z): a
    gold leading edge, two rows of coverts with eyes, six secondaries and seven primaries leaning out, burning tips"""
    pv = PIVOT['w1r' if sx > 0 else 'w1l']; X, Y, Z = pv
    Pt = lambda u, v, w=0.0: (X + sx * u, Y + v, Z + 4.5 + 0.05 * u + w)          # (clear of the elytra mesh, a little back toward the tip)
    lead = OPEN['lead']
    W = _lead([Pt(u, v, 0.3) for u, v in lead], 1.5, 0.7, pv, BACK)
    W.append(GEM(Pt(12.0, 5.3, 0.6), 1.2, 'sr_saph', pv, light=12))
    for row, (dv, ln, tex) in enumerate(((0.7, 3.8, 'sr_covert'), (2.6, 4.4, 'sr_covert'))):
        us = [0.8 + 1.9 * k for k in range(int((lead[-1][0] - 2.0) / 1.9))]
        for k, u in enumerate(us):
            v = _lead_v(u) - dv
            t = 'sr_covert_eye' if (k + row) % 4 == 1 else tex
            W.append(SEG(Pt(u, v, 0.15 - 0.1 * row), Pt(u + 0.4 + 0.05 * u, v - ln, 0.15 - 0.1 * row), 2.2, 0.35, t, pv, BACK, uv=FULL()))
    for k, (u, L, lean) in enumerate(OPEN['sec'] + OPEN['prim']):
        v0 = _lead_v(u) - (4.6 if u < 12 else 3.6)
        dx, dy = lean, -1.0; m = math.hypot(dx, dy); dx, dy = dx / m, dy / m
        lay = -0.3 - 0.12 * (k % 2)
        W += _feather(Pt(u, v0, lay), Pt(u + dx * L, v0 + dy * L, lay), 2.4, 'sr_quill' if k % 2 == 0 else 'sr_quill_d', pv, BACK, burn=0.22)
    for (u, v) in ((6.0, -3.6), (16.5, -5.0), (22.5, -7.5), (10.5, -8.0)):
        W.append(EYEBOX(Pt(u, v, 0.05), 1.7, 1.05, BACK, pv, d=0.3, light=11))
    return W


def lower(sx):
    """a lower wing - with two they covered their feet: from the small of the back it curves out and round the side of the
    leg toward the front of the ankle, its feathers hanging to the feet in a skirt behind and beside the legs (never in
    front, where the legs swing), burning at the hem just over the ground"""
    pv = PIVOT['w2r' if sx > 0 else 'w2l']; P = lambda p: _P(sx, p)
    lead = [(1.7, 12.2, 3.6), (3.8, 11.8, 4.4), (5.8, 10.6, 3.9), (7.0, 8.6, 2.2), (7.4, 6.6, 0.0), (7.2, 4.8, -1.6)]
    W = _lead([P((x, y, z + 0.5)) for x, y, z in lead], 1.0, 0.55, pv, (0.5, 0.0, 1.0), light=6)
    n = 6
    for k in range(n):
        t = k / (n - 1)
        rx, ry, rz = _poly(lead, 0.04 + t * 0.9)
        out = rigkit._unit((rx - 0.5, 0.0, rz + 0.6))                            # (outward from the legs, round their back and side)
        tip = (rx + out[0] * 1.4 + 0.2, 0.9 + 0.2 * k, rz + out[2] * 1.4)
        root = (rx, ry - 0.3, rz)
        lay = 0.08 * k
        W += _feather(P((root[0] + out[0] * lay, root[1], root[2] + out[2] * lay)), P((tip[0] + out[0] * lay, tip[1], tip[2] + out[2] * lay)),
                      2.3, 'sr_quill' if k % 2 == 0 else 'sr_quill_d', pv, rigkit._unit((sx * out[0], 0.0, out[2])), burn=0.2)
    for j, t in enumerate((0.15, 0.45)):                                          # coverts at the root, an eye in one
        rx, ry, rz = _poly(lead, t); out = rigkit._unit((rx - 0.5, 0.0, rz + 0.6))
        c = (rx + out[0] * 0.5, ry - 0.2, rz + out[2] * 0.5)
        W.append(SEG(P(c), P((c[0] + out[0] * 0.2, c[1] - 3.6, c[2] + out[2] * 0.2)), 2.1, 0.35, 'sr_covert_eye' if j == 0 else 'sr_covert', pv,
                     rigkit._unit((sx * out[0], 0.0, out[2])), uv=FULL()))
    for (t, y) in ((0.25, 6.0), (0.7, 4.0)):
        rx, ry, rz = _poly(lead, t); out = rigkit._unit((rx - 0.5, 0.0, rz + 0.6))
        W.append(EYEBOX(P((rx + out[0] * 0.85, y, rz + out[2] * 0.85)), 1.5, 0.95, rigkit._unit((sx * out[0], 0.0, out[2])), pv, d=0.3, light=11))
    return W


_RAW = {}


def _build():
    if _RAW: return _RAW
    A._rs.seed(299)
    R = {}
    for sx, s in ((1, 'r'), (-1, 'l')):
        R[f'{PREFIX}w1{s}'] = (f'w1{s}', great_folded(sx), 1.0)
        R[f'{PREFIX}w1{s}_o'] = (f'w1{s}', great_open(sx), OPEN_K)
        R[f'{PREFIX}w2{s}'] = (f'w2{s}', lower(sx), 1.0)
    _RAW.update(R)
    return _RAW


def models():
    """{model name: ({texture key: id}, elements)} - every element inside -16..32, every uv inside 0..16"""
    M = {}
    for name, (part, els, k) in _build().items():
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


# ---------------------------------------------------------------------------------------------------- poses
# (rigkit's display frame: design x and z flipped - dq turns design-frame rotations into it)
def dq(*rots):
    """a rotation from design-frame (axis, degrees) pairs, applied in order, as a display-frame quaternion"""
    return qs(*[(ax, -d if ax in ('x', 'z') else d) for ax, d in rots])


def wing(sx, raise_=0.0, back=0.0, tilt=0.0):
    """a wing's own turn about its root (design frame): raised (+ its span up / its tips out), swept back (+ tips back),
    tilted (+ its lower edge back)"""
    return dq(('y', -back * sx), ('z', raise_ * sx), ('x', tilt))


def body(lean=0.0, about=(0.0, 0.0, 0.0), to=None):
    """the virtual root: leaning forward by `lean` degrees about the design point `about`, that point carried to `to` - as
    {'body': q, '_off': design offset} for rigkit.solve"""
    q = qs(('x', lean))                                                           # (display frame: + leans the top forward)
    to = to or about
    P_ = D(PIVOT['body']); C = D(about); C2 = D(to)
    r = qrot(q, tuple(P_[i] - C[i] for i in range(3)))
    off = tuple(C2[i] - P_[i] + r[i] for i in range(3))
    return {'body': q, '_off': D(off)}


def pose(b, w1, w2, opened=False):
    p = dict(b); p.update(w1r=w1[0], w1l=w1[1], w2r=w2[0], w2l=w2[1]); p['_open'] = opened
    return p


def pair(fn, **kw):
    return (fn(1, **kw), fn(-1, **kw))


CROUCH = body(28.65, about=(0.0, 24 * K, 0.0), to=(0.0, (24 - 3.2) * K - 2.0, 0.0))     # (the game's crouch: the body leans 0.5 rad about the neck, set down)
GLIDE = body(90.0)                                                                       # (lying along the flight, about the feet)
POSES = {
    'rest_a': pose({}, pair(wing), pair(wing)),
    'rest_b': pose({}, pair(wing, raise_=2.5, tilt=3.0), pair(wing, raise_=1.5, tilt=2.0)),
    'sneak': pose(dict(CROUCH, _o_w2r=(0.0, 2.6, -1.0), _o_w2l=(0.0, 2.6, -1.0)), pair(wing, raise_=17.0, back=-4.0, tilt=4.0), pair(wing, raise_=9.0, tilt=30.0)),
    'ride': pose({}, pair(wing, raise_=-1.5, tilt=-2.0), pair(wing, raise_=10.0, tilt=75.0)),
    'glide_a': pose(GLIDE, pair(wing, raise_=34.0, back=4.0, tilt=10.0), pair(wing, raise_=16.0, tilt=-6.0), True),
    'glide_b': pose(GLIDE, pair(wing, raise_=20.0, back=8.0, tilt=16.0), pair(wing, raise_=10.0, tilt=-2.0), True),
    'fall_a': pose({}, pair(wing, raise_=52.0, back=18.0, tilt=10.0), pair(wing, raise_=14.0, tilt=10.0), True),
    'fall_b': pose({}, pair(wing, raise_=18.0, back=10.0, tilt=-4.0), pair(wing, raise_=8.0, tilt=4.0), True),
    'furl': pose({}, pair(wing, raise_=-78.0, back=10.0), pair(wing), True),             # (an open wing pointed down the back: on the way in and out)
}
POSES['furl_glide'] = pose(GLIDE, pair(wing, raise_=-78.0, back=10.0), pair(wing), True)


def model_of(p, pz):
    if p.startswith('w1') and pz.get('_open'): return f'{PREFIX}{p}_o'
    return f'{PREFIX}{p}'


def xforms(pz, art=None):
    """{display part: (left_rotation (display frame), translation (blocks, the display at the wearer's feet), scale)} - for this
    module's wings or another wing set's art module (the same names: PIVOT, PARENT, PARTS, model_of, model_k, S, U)"""
    art = art or sys.modules[__name__]
    xf = rigkit.solve(art.PIVOT, art.PARENT, pz)
    out = {}
    for p in art.PARTS:
        q, t = xf[p]; dp = D(art.PIVOT[p])
        k = art.model_k(art.model_of(p, pz)) * art.S * pz.get('_k_' + p, 1.0)        # (a pose's '_k_<part>': that display swollen or shrunk)
        out[p] = (q, tuple((dp[i] + t[i]) * art.U for i in range(3)), k)
    return out


def render(scene, name, at=(0.0, 0.0, 0.0), yaw=0.0, pitch=0.0, art=None):
    """a pose drawn into a tools.render Scene as the game shows it: each display at the wearer's feet (`at`), turned to the
    wearer's yaw (and, gliding, pitch), its transformation the pose's"""
    art = art or sys.modules[__name__]
    pz = art.POSES[name]
    for p, (q, t, k) in xforms(pz, art).items():
        scene.display(f'bm:item/{art.model_of(p, pz)}', pos=at, yaw=yaw, pitch=pitch, translation=t, scale=k, left=tuple(q))


# ---------------------------------------------------------------------------------------------------- the runtime (bm:p206w/<set>/...)
CARAPACE = '*[minecraft:custom_data~{bm:"dread_carapace"}]'
ANGEL = '*[minecraft:custom_data~{bm_angel:1b}]'
# STATES: number -> (name, first pose, interpolation into it, open models?, cycle: (half period, pose a, pose b) or None)
STATES = {1: ('rest', 'rest_a', 5, False, (40, 'rest_a', 'rest_b')),
          2: ('sneak', 'sneak', 4, False, None),
          3: ('glide', 'glide_a', 6, True, (15, 'glide_a', 'glide_b')),
          4: ('fall', 'fall_a', 5, True, (6, 'fall_a', 'fall_b')),
          5: ('ride', 'ride', 5, False, None)}


def sets():
    """THE WING SETS: {name: worn (the execute conditions on the wearer's chest slot), art (the module with the parts, pivots,
    poses and models), states}. A player wears one chest piece, so one set at a time."""
    import dread_wings, sov_wings
    return {'seraph': dict(worn=[f'if items entity @s armor.chest {CARAPACE}', f'if items entity @s armor.chest {ANGEL}'],
                           art=sys.modules[__name__], states=STATES),
            'dread': dict(worn=[f'if items entity @s armor.chest {CARAPACE}', f'unless items entity @s armor.chest {ANGEL}'],
                          art=dread_wings, states=dread_wings.STATES),
            # (the Dread Sovereign's spoils, phase238: the Last Night and the First Light - sov_wings.py)
            'sovn': dict(worn=['if items entity @s armor.chest *[minecraft:custom_data~{bm:"sov_wings"}]'], art=sov_wings.NIGHT, states=sov_wings.NIGHT.STATES),
            'sovl': dict(worn=['if items entity @s armor.chest *[minecraft:custom_data~{bm:"sov_wings_holy"}]'], art=sov_wings.LIGHT, states=sov_wings.LIGHT.STATES)}


GLIDE_STATE = 3
REACH = 12                                       # (blocks: how far a wearer's displays can be from them and still be theirs)


def _q(q):
    return '[' + ','.join(f'{v:.5f}f' for v in q) + ']'


def _xf_nbt(q, t, k):
    return f'left_rotation:{_q(q)},right_rotation:[0f,0f,0f,1f],translation:[{t[0]:.4f}f,{t[1]:.4f}f,{t[2]:.4f}f],scale:[{k:.4f}f,{k:.4f}f,{k:.4f}f]'


def _item(model):
    return f'item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"bm:{model}"}}}}'


def generate(G):
    """the 3D wings' runtime (call once, after phase206.generate - phase206 does)"""
    if getattr(G, '_p206w_done', False): return
    G._p206w_done = True
    fn = G.fn
    objs = ['bm.sws', 'bm.swt', 'bm.swo', 'bm.swn']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    G.wjson('bm/predicate/p206w/riding.json', {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:vehicle': {}}})
    G.wjson('bm/predicate/p206w/falling.json', {'condition': 'minecraft:entity_properties', 'entity': 'this',
                                                'predicate': {'minecraft:movement': {'fall_distance': {'min': 3.5}}}})
    G.wjson('bm/predicate/p206w/swimming.json', {'condition': 'minecraft:entity_properties', 'entity': 'this',
                                                 'predicate': {'minecraft:flags': {'is_swimming': True}}})
    # asleep in a bed (once a second: a player's sleeping_pos is only in its saved data)
    G.FUNCS['loop/second'].append('execute as @a[tag=bm.sww] run function bm:p206w/sleep')
    fn('p206w/sleep', ['tag @s remove bm.swsl', 'execute if data entity @s sleeping_pos run tag @s add bm.swsl'])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.swd]']
    S_ = sets()
    for name, st in S_.items():
        _set(G, name, st, [o for o in S_ if o != name])


def _set(G, name, ST, others):
    fn = G.fn; P = f'p206w/{name}'
    mine = lambda part=None: (f'@e[type=minecraft:item_display,tag=bm.swd_{name}' + (f',tag=bm.sw_{part}' if part else '') + f',distance=..{REACH}]')
    each = lambda part=None: f'execute as {mine(part)} if score @s bm.pid = #me bm.rng run '
    art, states = ST['art'], ST['states']
    POSES_, first_part = art.POSES, art.PARTS[0]
    # ---- worn: the set's conditions on the chest slot, as a function (1: worn)
    fn(f'{P}/worn', [f'execute {" ".join(ST["worn"])} run return 1', 'return 0'])
    # ---- who wears them (found four times a second; the per-tick work is theirs alone)
    G.FUNCS['loop/fast'][-1:-1] = [f'execute as @e[type=minecraft:player,tag=!bm.sww_{name}] if function bm:{P}/worn run function bm:{P}/on',
                                   f'execute as @e[type=minecraft:player,tag=bm.sww_{name},scores={{bm.swn=1,bm.sws=1..}}] at @s run function bm:{P}/ensure',
                                   # (the displays left behind - the wearer logged out, died, changed dimension, went too far: gone)
                                   f'execute as @e[type=minecraft:item_display,tag=bm.swd_{name}] at @s run function bm:{P}/orphan']
    fn(f'{P}/orphan', ['scoreboard players operation #me bm.rng = @s bm.pid', 'scoreboard players set #f bm.rng 0',
                       f'execute as @e[type=minecraft:player,tag=bm.sww_{name},distance=..{REACH}] if score @s bm.pid = #me bm.rng if score @s bm.swn matches 1 '
                       'run scoreboard players set #f bm.rng 1',
                       'execute if score #f bm.rng matches 0 run kill @s'])
    fn(f'{P}/on', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', f'tag @s add bm.sww_{name}', 'tag @s add bm.sww',
                   'scoreboard players set @s bm.sws -1', 'scoreboard players set @s bm.swn 0', 'scoreboard players set @s bm.swo 0'])
    fn(f'{P}/off', [f'function bm:{P}/kill', 'scoreboard players set @s bm.sws 0', f'tag @s remove bm.sww_{name}',
                    ('execute ' + ' '.join(f'unless entity @s[tag=bm.sww_{o}]' for o in others) + ' run ' if others else '') + 'tag @s remove bm.sww'])
    fn(f'{P}/kill', ['scoreboard players operation #me bm.rng = @s bm.pid', each() + 'kill @s',
                     'scoreboard players set @s bm.swn 0', 'scoreboard players set @s bm.swo 0'])
    # ---- every tick, as each wearer, at them
    G.FUNCS['tick'].append(f'execute as @e[type=minecraft:player,tag=bm.sww_{name}] at @s run function bm:{P}/tick')
    gl = GLIDE_STATE
    keys = [f'execute if score @s bm.sws matches {n} run function bm:{P}/k{n}' for n in states]
    fn(f'{P}/tick', [f'execute unless function bm:{P}/worn run return run function bm:{P}/off',
                     'scoreboard players operation #me bm.rng = @s bm.pid',
                     f'execute store result score #st bm.rng run function bm:{P}/pick',
                     f'execute unless score #st bm.rng = @s bm.sws run function bm:{P}/enter',
                     'execute if score @s bm.sws matches 0 run return 0',
                     'scoreboard players add @s bm.swt 1'] + keys +
       [f'execute if score @s bm.sws matches {gl} {each()[8:]}tp @s ~ ~ ~ ~ ~',             # (gliding: turned to the look's pitch too)
        f'execute unless score @s bm.sws matches {gl} {each()[8:]}tp @s ~ ~ ~ ~ 0'])
    fn(f'{P}/pick', ['execute if entity @s[gamemode=spectator] run return 0', 'execute if predicate bm:p44/invis run return 0',
                     'execute if entity @s[tag=bm.swsl] run return 0', 'execute if predicate bm:p206w/swimming run return 0',
                     f'execute if predicate bm:p206/gliding run return {gl}', 'execute if predicate bm:p206w/riding run return 5',
                     'execute if predicate bm:p20/sneaking run return 2', 'execute if predicate bm:p206w/falling run return 4', 'return 1'])
    assert set(states) == {1, 2, 3, 4, 5}, 'pick returns these states'
    fn(f'{P}/enter', ['scoreboard players operation @s bm.sws = #st bm.rng',
                      f'execute if score #st bm.rng matches ..0 run return run function bm:{P}/kill'] +
       [f'execute if score #st bm.rng matches {n} unless score @s bm.swn matches 1 run return run function bm:{P}/summon{n}' for n in states] +
       [f'execute if score #st bm.rng matches {n} run return run function bm:{P}/to{n}' for n in states])
    fn(f'{P}/ensure', ['scoreboard players operation #me bm.rng = @s bm.pid', 'scoreboard players set #n bm.rng 0',
                       each(first_part) + 'scoreboard players add #n bm.rng 1',
                       f'execute if score #n bm.rng matches 0 run function bm:{P}/kill'] +
       [f'execute if score #n bm.rng matches 0 if score @s bm.sws matches {n} run function bm:{P}/summon{n}' for n in states])

    made = set()
    def pose_fn(pname, dur, swap=False):
        """the four displays to a pose (in dur ticks); swap: their models set to the pose's (folded / open) too"""
        f = f'{P}/pose/{pname}_{dur}{"_s" if swap else ""}'
        if f not in made:
            made.add(f); pz = POSES_[pname]
            lines = []
            for part, (q, t, k) in xforms(pz, art).items():
                extra = (',' + _item(art.model_of(part, pz))) if swap else ''
                lines.append(each(part) + f'data merge entity @s {{start_interpolation:0,interpolation_duration:{dur},transformation:{{{_xf_nbt(q, t, k)}}}{extra}}}')
            fn(f, lines)
        return f'function bm:{f}'
    for n, (sname, first, dur_in, opened, cyc) in states.items():
        pz = POSES_[first]
        # summoned straight into this state's first pose (a wearer with no displays: just put it on, or back from hidden)
        summon = []
        for part, (q, t, k) in xforms(pz, art).items():
            summon.append(f'summon minecraft:item_display ~ ~ ~ {{Tags:["bm.swd","bm.swd_{name}","bm.sw_{part}","bm.swnew"],{_item(art.model_of(part, pz))},'
                          f'item_display:"fixed",teleport_duration:3,interpolation_duration:0,transformation:{{{_xf_nbt(q, t, k)}}}}}')
        fn(f'{P}/summon{n}', summon + ['scoreboard players operation @e[type=minecraft:item_display,tag=bm.swnew,distance=..1] bm.pid = @s bm.pid',
                                       'tag @e[type=minecraft:item_display,tag=bm.swnew,distance=..1] remove bm.swnew',
                                       'scoreboard players set @s bm.swn 1', f'scoreboard players set @s bm.swo {1 if opened else 0}',
                                       'scoreboard players set @s bm.swt 0'])
        # into this state from another: folded <-> open swaps the great wings' models by way of the furl
        if opened:
            furl = 'furl_glide' if n == GLIDE_STATE else 'furl'
            fn(f'{P}/to{n}', [f'execute if score @s bm.swo matches 0 run return run function bm:{P}/open{n}', 'scoreboard players set @s bm.swt -1'])
            fn(f'{P}/open{n}', [pose_fn(furl, 0, swap=True), 'scoreboard players set @s bm.swo 1', 'scoreboard players set @s bm.swt -2'])
        else:
            fn(f'{P}/to{n}', [f'execute if score @s bm.swo matches 1 run return run function bm:{P}/close{n}', 'scoreboard players set @s bm.swt -1'])
            fn(f'{P}/close{n}', [pose_fn('furl', 4), 'scoreboard players set @s bm.swt -5'])
        k = []
        if not opened:
            k.append(f'execute if score @s bm.swt matches -1 if score @s bm.swo matches 1 run function bm:{P}/fold{n}')
            fn(f'{P}/fold{n}', [pose_fn(first, 0, swap=True), 'scoreboard players set @s bm.swo 0'])
        k.append(f'execute if score @s bm.swt matches 0 run {pose_fn(first, dur_in)}')
        if cyc:
            half, a, b = cyc
            k.append(f'execute if score @s bm.swt matches {half} run {pose_fn(b, half)}')
            k.append(f'execute if score @s bm.swt matches {2 * half}.. run function bm:{P}/wrap{n}')
            fn(f'{P}/wrap{n}', [pose_fn(a, half), 'scoreboard players set @s bm.swt 0'])
        fn(f'{P}/k{n}', k)


def rp(R):
    """gen_rp: the wings' models (3D, at display scale) and their own textures (dread_set_art registers seraph_art's)"""
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    for name, (tex, els) in models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (PREFIX,)
    if getattr(R, 'PHASE2', True):                          # (the Sovereign's wings: phase 2's, on its and the Divine One's textures)
        import sov_wings
        sov_wings.rp(R)

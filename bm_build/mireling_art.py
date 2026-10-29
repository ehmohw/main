"""3.00: THE MIRELING (art) - the 50th follower: a young Dread Mire that has bonded to you. The same creature as mire_art's,
small and follower-sized - creepy, but endearing.

THE LOOK. A shimmering reddish-black puddle (~1.1 blocks across) with a squat mound in it, rising into a short, fat, worm-like
black mass ~1.75 blocks tall: two pinched worm rings and a round, swollen head-mass - a baby's proportions, the head big for
its body. Glowing red veins up every ring, across the crown and through the puddle. On the head's front the MAW - the Mire's
jagged pointed beak, stubbier: four spined petals closing to a point, the top one a little hooked beak. It splits open into
four fanged petals round a single big ORANGE-RED EYE with a black slit pupil, set in the throat - and the eye peeks out,
curious, whenever the maw opens. TWO SHORT TENTACLES grow from the upper ring (three ringed segments each, glowing pores down
the inner side, a small barbed hook) and wave. Black goo drips off the rings and the jaw. Its textures are the Mire's own
patterns (mire_art's hide, ribs, folds, the oily pool, the vein glow, the eye) under its own names (ml_*), so its wardrobe
can recolour them without touching the Mire.

IT MOVES as a creature that slides along as a small puddle and rears up when it stops: walking and running it is MOSTLY
SUNK - a low mound gliding along, just the top of the head and the shut beak above the puddle, the tentacles trailing back,
a little wave running through it; standing still it RISES, swaying, the maw half open and the eye looking about. Sitting, it
settles into the puddle with only the eye-maw poking up, blinking.

THE RIG (rigkit, as rigpet / rigfol / rigface take it):
  body                          the root: the puddle (three thin terraced layers, veins, spatters, bubbles) and the mound in it
  seg1, seg2                    the trunk: two worm rings (seg2 carries the tentacles' sockets)
  head                          the head-mass: crown folds, hood, pustules, the throat and its fang ring, and THE EYE (the face:
                                head_x<face> per expression - the eye open, half-lidded, shut, smiling, wide, squeezed, narrowed)
  maw_u maw_r jaw maw_l         the four petals of the maw (children of head), hinged round the maw's base ring: MAWOPEN(a)
                                splays them about a degrees (0: shut in a point)
  t1a t1b t1c / t2a t2b t2c     the two tentacles, base to tip (t1 its right, t2 its left; tNa a child of seg2)
Fourteen displays. Design units: the ground at y=0, facing -z, its right is +x. RIG_SCALE 0.8: the risen crown ~1.75 blocks.
No PART_K (every part fits its model box at k 1).
HIDDEN(p, pose): the pose's '_hide'. The sunk poses (walk, run, sit, swim, the faint) hide seg1 and seg2 - they are under
the ground there - so they melt down into the puddle as it sinks and grow back up out of it as it rises.

POSES (POSES[name]; rigpet's cycles need idle_a, walk_0..3, run_0..3, jump, swim_0..7, sit_a / sit_b, happy):
  idle_a, idle_b, idle_c        risen and swaying; the maw half open, the eye peeking; idle_c tilts its head, curious
  walk_0..3, run_0..3           sunk, a low mound gliding (a wave through it, the tentacles trailing); run lower, streaming
  jump                          half risen, tentacles flung up
  swim_0..7                     a floating puddle bobbing, the eye up out of the water, tentacles paddling
  sit_a, sit_b                  settled as a puddle, only the eye-maw poking up (sit_b: the lid drooping - its idle blink)
  happy, happy_b                tentacles waving high, the maw fluttering open (alternate them)
  hurt                          flinching away, the maw clamped shut, the eye squeezed
  tired, getup                  fainted - melted flat, the head on its side in the puddle; half risen, propped on its tentacles
  lash_up, lash                 the attack: t1 cocked high and back - then whipped down ~1.1 blocks ahead
  grab_up, grab, grab_pull      the ability: both tentacles raised - shot out ~1.3 blocks ahead - hauled back to the open maw
DRAFT lists them in sheet order. Each pose's '_face' names the eye it shows in previews, figurines and dolls; in the game the
face is the mood's (rigface: FACE_MAP for Cfg.FACE).

FACES ('happy', 'half', 'shut', 'wide', 'hurt', 'fierce'); FACE_MAP {phase95 mood: face}. model_name(p, pose, suffix): the
head wears its face (ml_head_x<face>), every other part its one model.

WARDROBE (phase99 NEW / phase138 RECOL, as every recoloured follower): WARDROBE = (slot name, {k: (look, (dark, mid, light))})
- Ember Mire (orange veins), Void Mire (purple), Frost Mire (pale blue); then the gilded / diamond / netherite looks.
RECOL_KEYS (the textures a look recolours) = LOOK_TEX (the black hide: main) + LOOK_SIDE (the veins: phase138.SIDE - they
take the light end of the hide's range, so a look's light colour IS its vein colour, and the hide's wet glints catch it).
The eye, the throat and the maw's lining stay ember-red in every look. look_textures(pal) previews a look exactly as
phase138 builds it. SHINY = (name, palette, dye) for shiny.LOOKS: a pale bone-white Mire with gold veins.
Wiring:  P99.NEW['mireling'] = ('The Mireling', COL, A.WARDROBE[0], dict(A.WARDROBE[1]));
         P138.RECOL['mireling'] = ('mireling_art', A.RECOL_KEYS); P138.SIDE |= set(A.LOOK_SIDE);
         shiny.LOOKS['mireling'] = A.SHINY.

DOLL (phase141.DOLL_FROM's kwargs): the default chibi warp; its "head" is the head and the maw's four petals (groups).
FIT (phase134): measured from idle_a at RIG_SCALE (fit() re-measures).
ICON: ITEM 'mire_seed' ("a Mireling's Seed"), icon_raw() -> the raw 16x16 (outlined; vanilla.process finishes it), icon() as shipped.
"""
import math
import random
from PIL import Image

import rigkit
from rigkit import qs, el, seg, D, qrot, qmul
import mire_art as MA

PREFIX = 'ml_'
RIG_SCALE = 0.8
SCALE = RIG_SCALE
ITEM = 'mire_seed'
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)

# ---------------------------------------------------------------------------------------------------- the rig
HZ = 1.0                                         # (the head-mass's centre, front to back)
CY, ZB, MR, ML, MN, MT = 25.4, -4.35, 4.3, 7.0, 4, 1.25     # the maw: centre height, base plane, half-size, length, steps, plate
PETAL = {'maw_u': 0, 'maw_r': 1, 'jaw': 2, 'maw_l': 3}
MAW = tuple(PETAL)
TENT = ('t1', 't2')
SEGS = ('a', 'b', 'c')
LEN = {'a': 5.2, 'b': 4.6}
APEX = (0.0, 4.8, -1.7)                          # (the hook's apex on the c segment, from its joint)
ROOT = {'t1': (3.75, 16.0, -0.9), 't2': (-3.75, 16.2, -0.9)}
OUT = {'t1': (0.86, 0.0, -0.51), 't2': (-0.86, 0.0, -0.51)}

PIVOT = {'body': (0.0, 0.0, 0.0), 'seg1': (0.0, 4.0, 0.0), 'seg2': (0.0, 11.5, 0.3), 'head': (0.0, 18.5, 0.6)}
PARENT = {'body': None, 'seg1': 'body', 'seg2': 'seg1', 'head': 'seg2'}


def _qt(dx, dy, k):
    """(dx, dy) about the maw's axis turned k quarter turns: the top -> its right -> the bottom -> its left"""
    for _ in range(k % 4): dx, dy = dy, -dx
    return dx, dy


for _m, _k in PETAL.items():
    _dx, _dy = _qt(0.0, MR, _k); PIVOT[_m] = (_dx, CY + _dy, ZB); PARENT[_m] = 'head'
for _t in TENT:
    _x, _y, _z = ROOT[_t]
    PIVOT[_t + 'a'] = (_x, _y, _z); PIVOT[_t + 'b'] = (_x, _y + LEN['a'], _z); PIVOT[_t + 'c'] = (_x, _y + LEN['a'] + LEN['b'], _z)
    PARENT[_t + 'a'] = 'seg2'; PARENT[_t + 'b'] = _t + 'a'; PARENT[_t + 'c'] = _t + 'b'
PARTS = tuple(PIVOT)
TPARTS = tuple(t + s for t in TENT for s in SEGS)
PART_K = {}
FACES = ('happy', 'half', 'shut', 'wide', 'hurt', 'fierce')
FACE_MAP = {'happy': 'happy', 'surprised': 'wide', 'hurt': 'hurt', 'sleepy': 'half', 'blink': 'shut', 'squint': 'happy', 'serious': 'fierce'}
SUNK = ('seg1', 'seg2')                          # (hidden in the sunk poses: under the ground)
TIP = {t: (t + 'c', tuple(PIVOT[t + 'c'][i] + APEX[i] for i in range(3))) for t in TENT}
EYE = ('head', (0.0, CY, ZB - 1.3))


def HIDDEN(p, pose):
    return p in pose.get('_hide', ())


def model_name(p, pose=None, suffix=''):
    face = f'_x{pose["_face"]}' if (p == 'head' and pose and pose.get('_face')) else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def _drip():
    """the Mire's goo drop, its brightest glint a step down (so the look's recolour ranges over the hide, not the goo)"""
    im = MA._drip(); px = im.load(); k6 = MA.K6 + (255,)
    for y in range(16):
        for x in range(16):
            if px[x, y] == k6: px[x, y] = MA.K5 + (255,)
    return im


LID = ['2222222222222222',
       '2333333333333332',
       '2344444444444432',
       '2333333333333332',
       '2222222222222222',
       '22222oo222222222',
       '2222oOOo22222222',
       '22222oo222222oo2',
       '22222222222oOO22',
       '2222222222222222',
       '2111111111111112',
       '2222222222222222',
       '222oo22222222222',
       '22oOOo2222222222',
       '2222222222222222',
       '1111111111111111']


def textures():
    """{name: RGBA} for assets/bm/textures/block (all 16x16, none animated: the looks recolour them)"""
    spine = MA._grid(['aaaaaaaaaaaaaaaa', 'aaaaaaaaaaaaaaaa'] + ['OOOOOOOOOOOOOOOO'] * 2 + ['oooooooooooooooo'] * 3 +
                     ['3333333333333333'] * 3 + ['2222222222222222'] * 5 + ['1111111111111111'])
    hot = MA._grid(['f' * 16] * 2 + ['ffeeeeeeeeeeeeff'] + ['feeeeeeeeeeeeeef'] * 11 + ['ffeeeeeeeeeeeeff'] + ['f' * 16])
    return {'ml_hide': MA._grid(MA.HIDE), 'ml_rib': MA._grid(MA.RIB), 'ml_fold': MA._grid(MA.FOLD), 'ml_pool': MA._pool_frame(0, 8),
            'ml_drip': _drip(), 'ml_spine': spine, 'ml_lid': MA._grid(LID), 'ml_glow': MA._vein_frame(1.0), 'ml_hot': hot,
            'ml_barb': MA._barb(), 'ml_fang': MA._fang(), 'ml_maw': MA._grid(MA.MAWT), 'ml_ember': MA._grid(MA.EMBER),
            'ml_iris': MA._grid(MA.IRIS, MA.EYEPAL), 'ml_irisr': MA._grid(MA.IRISR, MA.EYEPAL), 'ml_void': MA._grid(['0' * 16] * 16)}


# ---- the wardrobe (phase99 / phase138) and the shiny (shiny.py)
LOOK_TEX = ('ml_hide', 'ml_rib', 'ml_fold', 'ml_pool', 'ml_drip', 'ml_spine', 'ml_lid')
LOOK_SIDE = ('ml_glow', 'ml_hot', 'ml_barb')
RECOL_KEYS = LOOK_TEX + LOOK_SIDE
WARDROBE = ('Veins', {1: ('Ember Mire', ('#0a0504', '#2e130b', '#ff8a2a')),
                      2: ('Void Mire', ('#07040c', '#1f1032', '#b46aff')),
                      3: ('Frost Mire', ('#04070c', '#122030', '#9ad8ff')),
                      4: ('Gilded Mire', ('#3a2806', '#c8962a', '#ffe08a')),
                      5: ('Diamond Mire', ('#06323a', '#1a9aa0', '#a8fff4')),
                      6: ('Netherite Mire', ('#141014', '#4a4046', '#9a8c94'))})
SHINY = ('Shiny Bone Mire', ('#5a5246', '#cdc3ad', '#ffcc3a'), 'white')


def look_textures(pal):
    """{name: RGBA} - a look's recoloured textures, as phase138 builds them (the hide through the palette, the veins on the hide's
    range: their light end); the names without the '_c<k>' suffix"""
    import phase99 as P99
    base = textures()
    main = {n: base[n] for n in LOOK_TEX}
    out = P99._recolour(main, pal)
    out.update(P99._recolour({n: base[n] for n in LOOK_SIDE}, pal, rng=P99._lumrange(main)))
    return out


# ---------------------------------------------------------------------------------------------------- building helpers
MATS = ('hide', 'rib', 'fold', 'pool', 'drip', 'spine', 'lid', 'glow', 'hot', 'barb', 'fang', 'maw', 'ember', 'iris', 'irisr', 'void')
LIGHT = {'glow': 12, 'hot': 13, 'ember': 13, 'maw': 9, 'iris': 15, 'irisr': 14}     # (light_emission: softer than the Mire's)
FULL = {'fang', 'drip', 'barb', 'spine'}
F6 = ('north', 'south', 'east', 'west', 'up', 'down')
_rs = random.Random(7)
_PV = [None]


def E(fr, to, mat, faces=None, uv=None, light=None, rot=None):
    fr, to = tuple(min(a, b) for a, b in zip(fr, to)), tuple(max(a, b) for a, b in zip(fr, to))
    if mat in FULL and uv is None: uv = {f: [0, 0, 16, 16] for f in F6}
    shift = None if uv else (_rs.random(), _rs.random())
    return el(fr, to, PREFIX + mat, _PV[0], rot=rot, uv=uv, faces=faces, light=LIGHT.get(mat, 0) if light is None else light, shift=shift)


def SEG(a, b, w, mat, up=FRONT, ext=0.0, h=None):
    e = seg(a, b, w, h or w, PREFIX + mat, _PV[0], up, ext, light=LIGHT.get(mat, 0), shift=None if mat in FULL else (_rs.random(), _rs.random()))
    if mat in FULL:
        for fc in e['faces'].values(): fc['uv'] = [0, 0, 16, 16]
    return e


def OCT(cx, cz, y0, y1, rx, rz, mat, k=0.72, inset=0.06):
    return [E((cx - rx, y0, cz - rz * k), (cx + rx, y1, cz + rz * k), mat),
            E((cx - rx * k, y0 + inset, cz - rz), (cx + rx * k, y1 - inset, cz + rz), mat)]


def VEIN(path, axis, at, out, w=0.5, d=0.16, mat='glow'):
    """a glowing vein laid on a face (as mire_art.VEIN): path of axis-aligned steps in the face's plane"""
    els = []
    lo, hi = (at - 0.06, at + d) if out > 0 else (at - d, at + 0.06)
    for (u0, v0), (u1, v1) in zip(path, path[1:]):
        a0, a1 = sorted((u0, u1)); b0, b1 = sorted((v0, v1))
        a0, a1, b0, b1 = a0 - w / 2, a1 + w / 2, b0 - w / 2, b1 + w / 2
        if axis == 'x': fr, to = (lo, a0, b0), (hi, a1, b1)
        elif axis == 'z': fr, to = (a0, b0, lo), (a1, b1, hi)
        else: fr, to = (a0, lo, b0), (a1, hi, b1)
        els.append(E(fr, to, mat))
    return els


def DRIP(x, y, z, ln, w=0.45, ball=0.8):
    return [E((x - w / 2, y - ln, z - w / 2), (x + w / 2, y + 0.15, z + w / 2), 'drip'),
            E((x - ball / 2, y - ln - ball * 0.8, z - ball / 2), (x + ball / 2, y - ln + ball * 0.2, z + ball / 2), 'drip')]


# ---------------------------------------------------------------------------------------------------- the body: puddle and mound
CELL = 1.0
PUDDLE_Y = (0.0, 0.15, 0.3, 0.45)
PUDDLE_LIGHT = (2, 3, 4)


def _r(th, layer):
    r = 9.6 + 1.1 * math.sin(3 * th + 0.4) + 0.8 * math.sin(5 * th + 2.0) + 0.45 * math.sin(8 * th + 1.3)
    if layer == 1: r += -2.2 + 0.6 * math.sin(4 * th + 0.7)
    if layer == 2: r += -4.6 + 0.8 * math.sin(2 * th + 1.9)
    return r * (1.0 + 0.06 * math.cos(2 * th))


def _mask(layer):
    n = 13; out = set()
    for i in range(-n, n):
        for j in range(-n, n):
            cx, cz = (i + 0.5) * CELL, (j + 0.5) * CELL
            if math.hypot(cx, cz) < _r(math.atan2(cz, cx), layer): out.add((i, j))
    return out


def _layer_at(x, z, masks):
    c = (math.floor(x / CELL), math.floor(z / CELL)); lv = -1
    for L in range(3):
        if c in masks[L]: lv = L
    return lv


def _body():
    P = []; masks = [_mask(L) for L in range(3)]
    for L in range(3):
        for (i, j, w, h) in MA._rects(masks[L], cap=16):
            P.append(E((i * CELL, PUDDLE_Y[L], j * CELL), ((i + w) * CELL, PUDDLE_Y[L + 1], (j + h) * CELL), 'pool',
                       faces=('north', 'south', 'east', 'west', 'up'), light=PUDDLE_LIGHT[L]))
    rnd = random.Random(29)
    for k in range(7):                                                   # (spatters round the rim)
        th = 2 * math.pi * k / 7 + rnd.uniform(-0.25, 0.25); r = _r(th, 0) + rnd.uniform(0.9, 1.8); s = rnd.choice((0.7, 1.0, 1.3))
        x, z = round(r * math.cos(th) * 2) / 2, round(r * math.sin(th) * 2) / 2
        P.append(E((x - s / 2, 0.0, z - s / 2), (x + s / 2, 0.12, z + s / 2), 'pool', faces=('north', 'south', 'east', 'west', 'up'), light=2))
    for (x, z, s) in ((-5.2, 3.0, 1.0), (4.0, -5.6, 0.8), (6.8, 3.4, 0.9), (-2.6, -7.2, 0.7)):     # (bubbles)
        y = PUDDLE_Y[_layer_at(x, z, masks) + 1]
        P.append(E((x - s / 2, y - 0.08, z - s / 2), (x + s / 2, y + s * 0.45, z + s / 2), 'drip', faces=('north', 'south', 'east', 'west', 'up')))
    # veins of red light out through the puddle, in square steps
    def run(x, z, dirs):
        pts = [(x, z)]
        for (dx, dz, n) in dirs: x += dx * n; z += dz * n; pts.append((x, z))
        return pts
    paths = [run(5, 0, [(1, 0, 2), (0, -1, 1), (1, 0, 2)]), run(0, 5, [(0, 1, 2), (1, 0, 1), (0, 1, 2)]),
             run(-5, 0, [(-1, 0, 2), (0, 1, 2), (-1, 0, 1)]), run(0, -5, [(0, -1, 2), (-1, 0, 2), (0, -1, 1)]),
             run(4, 4, [(1, 0, 1), (0, 1, 2), (1, 0, 1)]), run(-4, -4, [(-1, 0, 2), (0, -1, 1)]), run(-4, 4, [(0, 1, 2), (-1, 0, 2)])]
    for pts in paths:
        for (x0, z0), (x1, z1) in zip(pts, pts[1:]):
            n = int(round(max(abs(x1 - x0), abs(z1 - z0)))) * 2
            for k in range(n):
                a = (x0 + (x1 - x0) * k / n, z0 + (z1 - z0) * k / n); b = (x0 + (x1 - x0) * (k + 1) / n, z0 + (z1 - z0) * (k + 1) / n)
                L = _layer_at((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, masks)
                if L < 0: continue
                xa, xb = sorted((a[0], b[0])); za, zb = sorted((a[1], b[1]))
                if xa == xb: xa, xb = xa - 0.35, xb + 0.35
                if za == zb: za, zb = za - 0.35, zb + 0.35
                top = PUDDLE_Y[L + 1]
                P.append(E((xa, top - 0.06, za), (xb, top + 0.08, zb), 'glow', faces=('north', 'south', 'east', 'west', 'up')))
    # the mound: a squat tiered heap, lobes oozing out, veins climbing it
    P += OCT(0, 0, 0.35, 2.2, 6.4, 6.1, 'hide')
    P += OCT(0, 0.1, 2.0, 4.4, 5.3, 5.1, 'hide')
    for k, (th, s) in enumerate(((0.3, 2.8), (1.6, 2.4), (2.6, 3.0), (3.7, 2.4), (4.7, 2.7), (5.6, 2.2))):
        x, z = 6.2 * math.cos(th), 6.0 * math.sin(th)
        P.append(E((x - s / 2, 0.05, z - s / 2), (x + s / 2, 1.0 + 0.15 * (k % 2), z + s / 2), 'hide'))
    for axis, sg, off in (('x', 1, -1.4), ('x', -1, 1.6), ('z', -1, 1.0), ('z', 1, -1.8)):
        for i, (r, y0, y1) in enumerate(((6.4, 0.35, 2.2), (5.3, 2.2, 4.4))):
            P += VEIN([(y0, off), (y1, off)], 'x', sg * r, sg) if axis == 'x' else VEIN([(off, y0), (off, y1)], 'z', sg * r, sg)
            if i == 0:
                P += VEIN([(sg * 6.4, off), (sg * 5.3, off)], 'y', 2.2, 1) if axis == 'x' else VEIN([(off, sg * 6.4), (off, sg * 5.3)], 'y', 2.2, 1)
    P += [E((-5.6, 1.4, -3.4), (-4.0, 2.2, -2.0), 'drip'), E((3.6, 3.2, 2.2), (4.8, 3.9, 3.4), 'drip')]
    return P


# ---------------------------------------------------------------------------------------------------- the trunk
def _segment(y0, y1, r, cz=0.0, lumps=(), veins=(), drips=()):
    """a fat worm ring (mire_art._segment, smaller): a ringed pinched neck down into the one below, the swollen belly, a lip"""
    h = y1 - y0; yb = y0 + 0.6 * h; S = []
    S += OCT(0, cz, y0 - 1.0, y0 + 0.7, r - 1.2, r - 1.2, 'rib')
    S += OCT(0, cz, y0 + 0.5, y0 + 1.2, r - 0.5, r - 0.5, 'hide')
    S += OCT(0, cz, y0 + 1.1, yb, r, r, 'hide')
    S += OCT(0, cz, yb - 0.15, y1 - 0.4, r - 0.6, r - 0.6, 'hide')
    S += OCT(0, cz, y1 - 0.55, y1 + 0.3, r - 1.15, r - 1.15, 'hide')
    for (x, y, z, sx, sy, sz) in lumps:
        S.append(E((x - sx / 2, y - sy / 2, z - sz / 2), (x + sx / 2, y + sy / 2, z + sz / 2), 'hide'))
    ya, ym, yc = y0 + 1.3, y0 + 0.36 * h, yb - 0.3
    for (axis, sd, u, jog) in veins:
        if axis == 'x': S += VEIN([(ya, cz + u), (ym, cz + u), (ym, cz + u + jog), (yc, cz + u + jog)], 'x', sd * r, sd)
        else: S += VEIN([(u, ya), (u, ym), (u + jog, ym), (u + jog, yc)], 'z', cz + sd * r, sd)
    for (x, z, ln) in drips: S += DRIP(x, y0 + 1.15, cz + z, ln)
    return S


def _seg1():
    r = 4.7
    return _segment(4.0, 12.2, r, 0.0, lumps=[(4.6, 8.2, -0.8, 1.0, 1.8, 1.8)],
                    veins=[('x', 1, -1.0, 1.8), ('x', -1, 1.4, -1.8), ('z', -1, 1.2, -1.0), ('z', 1, -1.6, 1.6)],
                    drips=[(r - 0.25, -1.6, 1.4), (-1.4, r - 0.25, 1.8)])


def _seg2():
    r = 4.15
    S = _segment(11.5, 19.2, r, 0.3, lumps=[(-1.8, 14.0, 0.3 + r + 0.2, 1.8, 1.4, 1.0)],
                 veins=[('x', 1, 1.0, -1.6), ('x', -1, -0.8, 1.6), ('z', -1, -0.8, 1.6)], drips=[(-(r - 0.25), -1.2, 1.6)])
    for t in TENT:                                                  # (the tentacles' sockets: swollen, ringed)
        x, y, z = ROOT[t]; o = OUT[t]
        S.append(SEG((x - o[0] * 1.8, y, z - o[2] * 1.8), (x + o[0] * 0.35, y, z + o[2] * 0.35), 3.0, 'hide', up=UP))
        S.append(SEG((x - o[0] * 0.3, y, z - o[2] * 0.3), (x + o[0] * 0.65, y, z + o[2] * 0.65), 3.4, 'rib', up=UP))
    return S


# ---------------------------------------------------------------------------------------------------- the head and the eye
EYE_Z = ZB - 0.05                                 # (the eye's back: just in front of the throat)


def _eye(face=None):
    """the eye in the throat, its expression: the ball (rim and iris, a black slit pupil, a hot glint) and, closing over it, a
    dark membrane lid with a glowing seam where it meets - half (drooping), shut, happy (a smiling arch), hurt (squeezed to a
    sliver), fierce (narrowed to a band); wide: the pupil round and dilated"""
    z0, z1 = EYE_Z, EYE_Z - 1.2
    e = [E((-2.45, CY - 1.8, z0), (2.45, CY + 1.8, z1), 'irisr'), E((-1.8, CY - 2.45, z0 - 0.05), (1.8, CY + 2.45, z1 - 0.05), 'irisr'),
         E((-1.8, CY - 1.2, z1), (1.8, CY + 1.2, z1 - 0.25), 'iris'), E((-1.2, CY - 1.8, z1 - 0.05), (1.2, CY + 1.8, z1 - 0.3), 'iris')]
    zf = z1 - 0.3                                   # (the eye's front)
    if face == 'wide':
        e += [E((-0.9, CY - 0.9, zf), (0.9, CY + 0.9, zf - 0.12), 'void'), E((-0.4, CY - 1.5, zf), (0.4, CY + 1.5, zf - 0.1), 'void'),
              E((-1.5, CY + 0.65, zf - 0.05), (-0.8, CY + 1.35, zf - 0.17), 'hot'), E((0.7, CY - 1.2, zf - 0.05), (1.05, CY - 0.85, zf - 0.17), 'hot')]
    else:
        e += [E((-0.38, CY - 1.6, zf), (0.38, CY + 1.6, zf - 0.12), 'void'), E((-1.45, CY + 0.6, zf - 0.05), (-0.85, CY + 1.2, zf - 0.17), 'hot')]
    zl0, zl1 = z0 + 0.02, zf - 0.22                  # (a lid: wraps the eye, just proud of its front)
    lid = lambda y0, y1: E((-2.53, y0, zl0), (2.53, y1, zl1), 'lid')
    seam = lambda x0, x1, y: E((x0, y - 0.13, zl1 + 0.02), (x1, y + 0.13, zl1 - 0.06), 'glow')
    if face == 'half':
        e += [lid(CY + 0.15, CY + 2.53), seam(-2.1, 2.1, CY + 0.15)]
    elif face == 'shut':
        e += [lid(CY - 2.53, CY + 2.53), seam(-2.0, 2.0, CY)]
    elif face == 'happy':                            # (a smiling arch, high in the middle)
        e += [lid(CY - 2.53, CY + 2.53), seam(-2.1, -1.3, CY - 0.75), seam(-1.45, -0.6, CY - 0.15), seam(-0.75, 0.75, CY + 0.3),
              seam(0.6, 1.45, CY - 0.15), seam(1.3, 2.1, CY - 0.75)]
    elif face == 'hurt':                             # (squeezed: a sliver of the eye, a zigzag of a seam)
        e += [lid(CY + 0.3, CY + 2.53), lid(CY - 2.53, CY - 0.3), seam(-2.2, -0.6, CY + 0.3), seam(-0.8, 0.8, CY), seam(0.6, 2.2, CY - 0.3)]
    elif face == 'fierce':                           # (narrowed: the lids close in to a band round the slit)
        e += [lid(CY + 0.75, CY + 2.53), lid(CY - 2.53, CY - 0.95), seam(-2.2, 2.2, CY + 0.75)]
    return e


def _head(face=None):
    """the round young head-mass behind the maw: a swollen dome, small folds on its crown, a short hood down the back, a pustule
    or two; on its front the throat (lit), a ring of little black fangs round it, and the eye"""
    H = []
    H += OCT(0, HZ, 18.6, 30.6, 6.0, 5.2, 'hide')
    H += [E((-6.6, 20.8, HZ - 2.2), (6.6, 28.4, HZ + 3.2), 'hide')]                        # (swollen cheeks)
    H += OCT(0, HZ + 0.5, 30.4, 32.6, 4.8, 4.2, 'hide')                                     # (the crown)
    for (x0, x1, z0, z1, hh) in ((-3.8, -0.5, -1.2, 0.2, 0.7), (0.6, 3.7, -0.7, 0.7, 0.6), (-4.0, -1.2, 1.4, 2.8, 0.6),
                                 (0.0, 3.9, 1.7, 3.1, 0.75), (-3.0, 0.7, 3.6, 4.9, 0.6)):
        H.append(E((x0, 32.5, HZ + z0), (x1, 32.6 + hh, HZ + z1), 'fold'))
    H += [E((-4.2, 19.4, HZ + 5.0), (4.2, 25.6, HZ + 6.1), 'rib'), E((-3.0, 18.6, HZ + 5.4), (3.0, 21.4, HZ + 6.8), 'rib')]   # (the hood)
    H += [E((6.5, 24.4, HZ + 0.6), (7.4, 26.2, HZ + 2.4), 'hide'), E((7.35, 25.0, HZ + 1.1), (7.52, 25.6, HZ + 1.8), 'glow'),   # (pustules)
          E((-7.3, 22.6, HZ + 0.2), (-6.5, 24.0, HZ + 1.8), 'hide'), E((-7.45, 23.0, HZ + 0.7), (-7.28, 23.6, HZ + 1.3), 'glow')]
    H += VEIN([(22.2, HZ - 1.8), (22.2, HZ + 0.4), (23.4, HZ + 0.4), (23.4, HZ + 2.8)], 'x', 6.6, 1)
    H += VEIN([(27.0, HZ - 1.8), (27.0, HZ - 0.4), (25.6, HZ - 0.4), (25.6, HZ + 2.6)], 'x', -6.6, -1)
    H += VEIN([(-1.4, 20.0), (-1.4, 22.6), (1.4, 22.6), (1.4, 25.0)], 'z', HZ + 6.1, 1)
    H += VEIN([(-1.6, HZ - 2.8), (-1.6, HZ - 0.6), (1.2, HZ - 0.6), (1.2, HZ + 2.0)], 'y', 32.6, 1)
    # the throat: a red well (lit), its ember heart; a ring of short black fangs
    zf = HZ - 5.2
    H += [E((-3.6, CY - 3.6, zf - 0.08), (3.6, CY + 3.6, zf), 'maw'), E((-2.7, CY - 2.7, zf - 0.12), (2.7, CY + 2.7, zf - 0.08), 'ember')]
    dark = {f: [0, 0, 16, 5] for f in F6}
    for k, ln in enumerate((0.8, 0.5, 0.9, 0.6, 0.75, 0.5)):
        an = 2 * math.pi * k / 6 + 0.5; x, y = 3.15 * math.cos(an), CY + 3.15 * math.sin(an)
        H.append(E((x - 0.25, y - 0.25, zf - 0.08 - ln), (x + 0.25, y + 0.25, zf - 0.08), 'fang', uv=dark))
    for (x, y) in ((5.3, 27.4), (6.0, 26.6), (-5.6, 21.9)):                                   # (pinprick eyes on the cheeks' fronts)
        H.append(E((x - 0.2, y - 0.2, HZ - 2.32), (x + 0.2, y + 0.2, HZ - 2.18), 'hot'))
    return H + _eye(face)


def _petal(name):
    """one petal of the maw (mire_art._petal, stubbier and a touch softer): a stepped plate sloping to the point, its lining lit,
    little fangs off its inside, a few spines on its back, the top one hooked at its point"""
    k = PETAL[name]; rnd = random.Random(53 + 19 * k); B = []
    for i in range(MN):
        h = MR * (1 - i / MN); z0 = ZB - i * ML / MN; z1 = z0 - ML / MN; zc = (z0 + z1) / 2; tt = min(MT, h); inner = h - tt
        B.append(((-h + 0.05, inner, z1), (h - 0.05, h, z0), 'hide'))
        if inner > 0.3:
            B.append(((-inner + 0.08, inner - 0.1, z1 + 0.02), (inner - 0.08, inner, z0 - 0.02), 'maw'))
            for sx in (-1, 1):
                if rnd.random() < 0.8:
                    ln = min(rnd.uniform(0.5, 1.4), 2 * inner - 0.25)
                    if ln > 0.35:
                        x = sx * rnd.uniform(0.25, max(0.3, inner - 0.35))
                        B.append(((x - 0.22, inner - 0.08 - ln, zc - 0.22), (x + 0.22, inner - 0.08, zc + 0.22), 'fang'))
        if i in (0, 2) or (i == 1 and k == 0):                                         # (a few spines on its back)
            sp = rnd.uniform(0.6, 1.2) * (1.0 - 0.15 * i); x = rnd.uniform(-0.5, 0.5) * h / MR
            B.append(((x - 0.3, h - 0.08, zc - 0.4), (x + 0.3, h + sp, zc + 0.2), 'spine'))
        for sx in (-1, 1):                                                             # (a serrated corner here and there)
            if rnd.random() < (0.35 if i % 2 == 0 else 0.1):
                ln = rnd.uniform(0.5, 1.0)
                x0, x1 = (h - 0.2, h + ln) if sx > 0 else (-h - ln, -h + 0.2)
                B.append(((x0, h - 0.45, zc - 0.3), (x1, h + 0.12, zc + 0.25), 'spine'))
    zt = ZB - ML
    if k == 0:                                                                         # (the beak: a little hooked point, lit at the tip)
        B += [((-0.5, -0.2, zt - 1.4), (0.5, 0.75, zt + 0.15), 'barb'), ((-0.36, -1.1, zt - 1.9), (0.36, 0.0, zt - 1.3), 'barb'),
              ((-0.2, -1.5, zt - 1.8), (0.2, -1.05, zt - 1.45), 'glow')]
    else:
        off = (0.15, -0.12, 0.06)[k - 1]
        B.append(((-0.32 + off, 0.0, zt - (1.3, 1.0, 0.7)[k - 1]), (0.32 + off, 0.6, zt + 0.12), 'barb'))
    out = []
    for (lo, hi, mat) in B:
        ax, ay = _qt(lo[0], lo[1], k); bx, by = _qt(hi[0], hi[1], k)
        fr = (min(ax, bx), CY + min(ay, by), lo[2]); to = (max(ax, bx), CY + max(ay, by), hi[2])
        uv = {f: [0, 16, 16, 0] for f in F6} if (mat == 'fang' and k == 2) else None
        out.append(E(fr, to, mat, uv=uv))
    if name == 'jaw':                                                                  # (goo hanging off the jaw)
        for (x, i, ln) in ((-1.4, 0, 1.6), (1.2, 1, 1.1), (0.2, 0, 2.0)):
            h = MR * (1 - i / MN); zc = ZB - (i + 0.5) * ML / MN
            out += DRIP(x, CY - h + 0.08, zc, ln)
    return out


def MAWOPEN(a, ragged=1.0):
    """the maw's petals splayed open by about a degrees each - a little uneven (0: shut in a point)"""
    if not a: return {}
    return {'maw_u': qs(('x', -a * 1.0), ('z', 3 * ragged)), 'jaw': qs(('x', a * 1.1), ('z', -4 * ragged)),
            'maw_r': qs(('y', -a * 0.9), ('x', 3 * ragged)), 'maw_l': qs(('y', a * 0.95), ('x', -2 * ragged))}


def _tentacle_seg(t, s):
    """one segment of a tentacle, up its own +y from its joint; the inner side (pores, the hook) toward -z"""
    x, y, z = PIVOT[t + s]; T = []
    if s == 'a': knuck, boxes, rings, pores = (2.7, -0.9, 0.7), [(2.3, 0.4, 2.9), (2.1, 2.7, 5.4)], (2.8,), (1.4, 3.6)
    elif s == 'b': knuck, boxes, rings, pores = (2.4, -0.7, 0.6), [(1.9, 0.3, 2.5), (1.7, 2.3, 4.8)], (2.4,), (1.2, 3.4)
    else: knuck, boxes, rings, pores = (2.0, -0.6, 0.5), [(1.5, 0.3, 2.2), (1.3, 2.0, 3.4)], (), (1.3,)
    w, k0, k1 = knuck
    T.append(E((x - w / 2, y + k0, z - w / 2), (x + w / 2, y + k1, z + w / 2), 'rib'))
    for i, (bw, b0, b1) in enumerate(boxes):
        ox = 0.12 if i % 2 else -0.12
        T.append(E((x + ox - bw / 2, y + b0, z - bw / 2), (x + ox + bw / 2, y + b1, z + bw / 2), 'hide'))
    for ry in rings:
        bw = [b for b in boxes if b[1] <= ry <= b[2]][0][0] + 0.35
        T.append(E((x - bw / 2, y + ry - 0.25, z - bw / 2), (x + bw / 2, y + ry + 0.25, z + bw / 2), 'rib'))
    for py in pores:
        bw = [b for b in boxes if b[1] <= py <= b[2]][0][0]
        T.append(E((x - 0.32, y + py - 0.32, z - bw / 2 - 0.12), (x + 0.32, y + py + 0.32, z - bw / 2 + 0.06), 'glow'))
    if s != 'c':                                                     # (a barb down its outer side)
        bw = boxes[1][0]
        T.append(SEG((x, y + boxes[1][1] + 0.6, z + bw / 2 - 0.2), (x, y + boxes[1][1] - 0.2, z + bw / 2 + 0.75), 0.45, 'barb', up=UP))
    else:                                                            # (the hook, curling to the inner side, lit at its point)
        T += [SEG((x, y + 3.2, z), (x, y + 4.4, z - 0.5), 1.1, 'hide', up=FRONT, ext=0.2),
              SEG((x, y + 4.4, z - 0.5), (x, y + 4.9, z - 1.4), 0.85, 'barb', up=FRONT, ext=0.18),
              SEG((x, y + 4.9, z - 1.4), (x, y + 4.5, z - 2.2), 0.6, 'barb', up=FRONT, ext=0.12),
              E((x - 0.2, y + 4.15, z - 2.5), (x + 0.2, y + 4.6, z - 2.1), 'glow')]
        for sx in (1, -1):
            T.append(SEG((x + sx * 0.5, y + 2.6, z), (x + sx * 1.3, y + 1.8, z + 0.3), 0.4, 'barb', up=UP))
    return T


# ---------------------------------------------------------------------------------------------------- models
_RAW = {}


def _build():
    if _RAW: return _RAW
    _rs.seed(7)
    fns = {'body': _body, 'seg1': _seg1, 'seg2': _seg2, 'head': _head}
    fns.update({m: (lambda m=m: _petal(m)) for m in MAW})
    for p in PARTS:
        _PV[0] = PIVOT[p]
        _RAW[p] = fns[p]() if p in fns else _tentacle_seg(p[:2], p[2])
    _PV[0] = PIVOT['head']
    for f in FACES:
        _RAW['head_x' + f] = _head(f)
    return _RAW


def models():
    """{model id: (textures, elements)} - one per part, and a head per face"""
    M = {}
    for part, els in _build().items():
        for e in els:
            for v in e['from'] + e['to']:
                assert -16 <= v <= 32, (part, e['from'], e['to'])
            for fc in e['faces'].values():
                assert all(0.0 <= t <= 16.0 for t in fc['uv']), (part, fc['uv'])
        used = sorted({fc['texture'][1:] for e in els for fc in e['faces'].values()})
        M[PREFIX + part] = ({t: f'bm:block/{t}' for t in used}, els)
    return M


# ---------------------------------------------------------------------------------------------------- world geometry
def world_boxes(pose, parts=None, xf=None):
    """{part: [(centre, axes, half extents)]} - each element as an oriented box in the world (display frame, design units)"""
    raw = _build(); xf = xf or rigkit.solve(PIVOT, PARENT, pose); out = {}
    for p in (parts or PARTS):
        if HIDDEN(p, pose): continue
        Q, t = xf[p]; pv = PIVOT[p]; dp = D(pv); W = tuple(t[i] + dp[i] for i in range(3)); bl = []
        key = 'head_x' + pose['_face'] if (p == 'head' and pose.get('_face')) else p
        for e in raw[key]:
            f, to = e['from'], e['to']
            c = [(f[i] + to[i]) / 2 for i in range(3)]; h = [abs(to[i] - f[i]) / 2 for i in range(3)]
            ax = [(1.0, 0, 0), (0, 1.0, 0), (0, 0, 1.0)]
            if 'rotation' in e:
                R = MA._rotm(e['rotation']); o = e['rotation']['origin']
                c = [sum(R[i][k] * (c[k] - o[k]) for k in range(3)) + o[i] for i in range(3)]
                ax = [tuple(R[i][j] for i in range(3)) for j in range(3)]
            cd = tuple(c[i] - 8 + pv[i] for i in range(3))
            cw = qrot(Q, tuple(D(cd)[i] - dp[i] for i in range(3)))
            bl.append((tuple(W[i] + cw[i] for i in range(3)), tuple(qrot(Q, D(a)) for a in ax), tuple(h), e))
        out[p] = bl
    return out


def extent(pose, parts=None):
    """(lowest y, highest y) of the posed parts, design units"""
    lo, hi = 1e9, -1e9
    for bl in world_boxes(pose, parts).values():
        for c, ax, h, _e in bl:
            ey = sum(abs(ax[i][1]) * h[i] for i in range(3))
            lo = min(lo, c[1] - ey); hi = max(hi, c[1] + ey)
    return lo, hi


def at(pose, part, p, xf=None):
    """where a design point carried by `part` stands in the world (design units)"""
    xf = xf or rigkit.solve(PIVOT, PARENT, pose); Q, t = xf[part]; pv = D(PIVOT[part])
    r = qrot(Q, tuple(D(p)[i] - pv[i] for i in range(3)))
    return D(tuple(t[i] + pv[i] + r[i] for i in range(3)))


def tip(pose, t):
    return at(pose, TIP[t][0], TIP[t][1])


def fit(pose=None):
    """phase134.FIT: (lowest y, height, x0, x1, z0, z1) in blocks - idle_a at RIG_SCALE, as the figurine stands"""
    pose = pose or POSES['idle_a']; U = RIG_SCALE / 16; pts = []
    for bl in world_boxes(pose).values():
        for c, ax, h, _e in bl:
            for sx in (-1, 1):
                for sy in (-1, 1):
                    for sz in (-1, 1):
                        pts.append(tuple(c[i] + sx * ax[0][i] * h[0] + sy * ax[1][i] * h[1] + sz * ax[2][i] * h[2] for i in range(3)))
    lo = [min(p[i] for p in pts) * U for i in range(3)]; hi = [max(p[i] for p in pts) * U for i in range(3)]
    return (round(lo[1], 3), round(hi[1] - lo[1], 3), round(lo[0], 3), round(hi[0], 3), round(lo[2], 3), round(hi[2], 3))


# ---------------------------------------------------------------------------------------------------- posing kit
def T(lean=0.0, twist=0.0, side=0.0):
    """a trunk joint's bend: lean + forward (- back), twist + turns its right forward, side + to its left"""
    return qs(('y', twist), ('x', lean), ('z', side))


_unit, _add, _sub, _dot, _cross, _conj = MA._unit, MA._add, MA._sub, MA._dot, MA._cross, MA._conj
SEG_AXIS = {'a': (0.0, 1.0, 0.0), 'b': (0.0, 1.0, 0.0), 'c': _unit(APEX)}
SEG_LEN = {'a': LEN['a'], 'b': LEN['b'], 'c': math.sqrt(sum(v * v for v in APEX))}


def _aim(local_axis, local_in, world_axis, world_in):
    lx, ly, lz = MA._frame(D(local_axis), D(local_in)); wx, wy, wz = MA._frame(D(world_axis), D(world_in))
    L = [[lx[i], ly[i], lz[i]] for i in range(3)]; W = [[wx[i], wy[i], wz[i]] for i in range(3)]
    M = [[sum(W[i][k] * L[j][k] for k in range(3)) for j in range(3)] for i in range(3)]
    return MA._mat2q(M)


def lay(pose, t, dirs, inner=None):
    """tentacle t's three segments along world directions dirs (design frame), the inner side (pores, hook) toward the curl"""
    p = dict(pose)
    for i, s in enumerate(SEGS):
        d = _unit(dirs[i])
        if inner is not None: inn = inner
        else:
            nb = _sub(dirs[min(i + 1, 2)], dirs[max(i - 1, 0)])
            inn = _sub(nb, tuple(_dot(nb, d) * c for c in d))
            if _dot(inn, inn) < 1e-4: inn = (0.0, -1.0, 0.0) if abs(d[1]) < 0.9 else (0.0, 0.0, -1.0)
        Qw = _aim(SEG_AXIS[s], (0.0, 0.0, -1.0), d, inn)
        Qp = rigkit.solve(PIVOT, PARENT, p)[PARENT[t + s]][0]
        p[t + s] = qmul(_conj(Qp), Qw)
    return p


def curl(d0, toward, bends):
    """three directions: d0, then turned toward `toward` by each bend in turn"""
    return MA.curl(d0, toward, bends)


def reach(pose, t, target, guide, inner=None, iters=60):
    """tentacle t bent (FABRIK) so its hook's apex comes to target (design units); guide: two points it starts from"""
    R = at(pose, 'seg2', PIVOT[t + 'a']); L = [SEG_LEN[s] for s in SEGS]
    pts = [R]
    for g in list(guide) + [target]:
        pts.append(_add(pts[-1], _unit(_sub(g, pts[-1])), L[len(pts) - 1]))
    for _ in range(iters):
        pts[3] = target
        for i in (2, 1, 0): pts[i] = _add(pts[i + 1], _unit(_sub(pts[i], pts[i + 1])), L[i])
        pts[0] = R
        for i in (0, 1, 2): pts[i + 1] = _add(pts[i], _unit(_sub(pts[i + 1], pts[i])), L[i])
    return lay(pose, t, [_sub(pts[i + 1], pts[i]) for i in range(3)], inner)


def sx_of(t):
    return 1 if t == 't1' else -1


def wave(p, t, up, out, fwd=0.0, bends=(30, 30), swing=0.0, toward=None):
    """a tentacle out from its socket: `up` (its first segment's rise), `out` (sideways), `fwd` (forward), each further segment
    curling by bends toward `toward` (default: back in over the top, a beckoning curl)"""
    s = sx_of(t)
    d0 = _unit((s * out, up, -fwd))
    if swing: d0 = MA._rod(d0, UP, swing * s)
    tw = toward or _unit((-s * 0.6, 0.4, -0.5))
    return lay(p, t, curl(d0, tw, bends))


def trail(p, t, spread=0.6, lift=0.15, ripple=0.0):
    """a tentacle trailing back over the puddle (walking): up out of it from the sunk socket, then flat behind, a ripple through it"""
    s = sx_of(t)
    return lay(p, t, [_unit((s * spread, 0.8, 0.45)), _unit((s * (spread - 0.2) + ripple, lift, 1.0)), _unit((s * 0.15 - ripple, -0.05, 1.0))],
               inner=(0.0, -1.0, 0.0))


def P(**kw):
    return kw


SINK = lambda dy: {'_o_seg1': (0.0, -dy, 0.0), '_hide': SUNK}


def _pose(name):
    s = math.sin
    if name in ('idle_a', 'idle_b', 'idle_c'):              # (risen, swaying; the maw half open, the eye peeking out)
        if name == 'idle_a':
            p = P(seg1=T(2, 0, 3), seg2=T(2, 4, -2), head=T(-8, 6, 2), **MAWOPEN(26))
            p = wave(p, 't1', 0.35, 0.8, 0.35, (36, 40)); p = wave(p, 't2', 0.1, 0.9, 0.2, (40, 46))
        elif name == 'idle_b':
            p = P(seg1=T(2, 0, -3), seg2=T(3, -5, 3), head=T(-4, -6, -3), **MAWOPEN(18), _face='half')
            p = wave(p, 't1', 0.05, 0.9, 0.2, (44, 40)); p = wave(p, 't2', 0.4, 0.75, 0.4, (34, 44))
        else:                                               # (curious: the head tilted right over, the maw open, the eye wide)
            p = P(seg1=T(4, 0, 2), seg2=T(6, 10, -6), head=T(-12, 16, -18), **MAWOPEN(40), _face='wide')
            p = wave(p, 't1', 0.75, 0.5, 0.6, (30, 50)); p = wave(p, 't2', -0.05, 0.9, 0.1, (46, 40))
    elif name.startswith('walk_') or name.startswith('run_'):      # (sunk: a low mound gliding, a wave through it)
        k = int(name[-1]); ph = math.pi * k / 2; run = name.startswith('run_')
        dy = 20.0 if run else 18.5
        p = dict(SINK(dy + 0.6 * s(2 * ph)))
        p.update(seg2=T(10 if run else 4, 0, 0), head=T((22 if run else 12) + 3 * s(2 * ph), 8 * s(ph), 7 * s(ph)), **MAWOPEN(0))
        for t in TENT:
            p = trail(p, t, 0.85 if run else 0.7, 0.2, (0.18 if run else 0.25) * s(ph + (0 if t == 't1' else math.pi)))
    elif name == 'jump':
        p = P(_off=(0.0, 3.0, 0.0), _o_seg1=(0.0, -6.0, 0.0), seg1=T(4), seg2=T(-4), head=T(-14), **MAWOPEN(30), _face='wide')
        p = wave(p, 't1', 0.85, 0.5, 0.0, (20, 20)); p = wave(p, 't2', 0.85, 0.5, 0.0, (20, 20))
    elif name.startswith('swim_'):                          # (a floating puddle bobbing, the eye up out of the water, paddling)
        k = int(name.split('_')[1]); ph = 2 * math.pi * k / 8
        p = dict(SINK(17.0 - 0.8 * s(ph)))
        p.update(seg2=T(-6, 0, 0), head=T(-14 + 4 * s(ph), 0, 6 * s(ph)), **MAWOPEN(14))
        for t in TENT:
            a = s(ph + (0 if t == 't1' else math.pi))
            p = lay(p, t, curl(_unit((sx_of(t) * 0.9, 0.05, -0.2 + 0.6 * a)), _unit((0.0, -0.3, 1.0)), (20, 25)), inner=(0.0, -1.0, 0.0))
        if k in (3, 4): p['_face'] = 'half'
    elif name in ('sit_a', 'sit_b'):                        # (settled into the puddle, only the eye-maw poking up)
        b = name == 'sit_b'
        p = dict(SINK(21.5))
        p.update(seg2=T(-4, 0, 0), head=T(-20 if not b else -14, 0 if not b else 8, 0 if not b else -10), **MAWOPEN(20 if not b else 14))
        if b: p['_face'] = 'half'
        for t in TENT:                                      # (curled on the puddle round it, like a cat's tail)
            sg = sx_of(t)
            p = lay(p, t, [_unit((sg * 0.25, 1.0, -0.1)), _unit((sg * 0.7, 0.5, -0.5)), _unit((sg * 0.1, -0.45, -1.0))], inner=(0.0, -1.0, 0.0))
    elif name in ('happy', 'happy_b'):                      # (tentacles waving high, the maw fluttering)
        b = name == 'happy_b'
        p = P(seg1=T(-2, 0, 3 if b else -3), seg2=T(-3, 5 if b else -5, 2 if b else -2), head=T(-7, 8 if b else -8, 6 if b else -6),
              **MAWOPEN(48 if b else 30, 1.4), _face='happy')
        up = lambda t: _unit((-sx_of(t) * 0.35, 1.0, -0.25))
        p = wave(p, 't1', 0.75, 0.75, 0.15, (30, 34) if b else (14, 18), swing=12 if b else -8, toward=up('t1'))
        p = wave(p, 't2', 0.75, 0.75, 0.15, (14, 18) if b else (30, 34), swing=-8 if b else 12, toward=up('t2'))
    elif name == 'hurt':                                    # (flinching away, the maw clamped shut, the eye squeezed)
        p = P(seg1=T(-5, 10, -5), seg2=T(-9, 14, -6), head=T(12, 22, -10), _face='hurt')
        p = wave(p, 't1', 0.6, 0.4, -0.2, (70, 60), toward=_unit((-1.0, -0.6, 0.0)))
        p = wave(p, 't2', 0.6, 0.4, -0.2, (70, 60), toward=_unit((1.0, -0.6, 0.0)))
    elif name == 'tired':                                   # (fainted: melted flat, the head on its side in the puddle)
        p = dict(SINK(15.0)); p.update(seg2=T(76, 0, 18), head=T(8, 10, 62), **MAWOPEN(6), _face='shut')
        for t in TENT:
            sg = sx_of(t)
            p = lay(p, t, [_unit((sg * 0.9, -0.15, -0.1)), _unit((sg * 0.8, -0.05, 0.6)), _unit((sg * 0.2, 0.0, 1.0))], inner=(0.0, -1.0, 0.0))
    elif name == 'getup':                                   # (half up out of the puddle, bowed, propped on its tentacles)
        p = dict(_o_seg1=(0.0, -9.0, 0.0), seg1=T(12, 0, 6), seg2=T(18, 0, 4), head=T(18, 0, 8), **MAWOPEN(8), _face='half')
        for t in TENT:
            R = at(p, 'seg2', PIVOT[t + 'a']); sg = sx_of(t); tg = (sg * 9.0, 0.6, -4.0)
            p = reach(p, t, tg, (_add(R, (sg * 3.5, 1.5, -1.0)), (sg * 7.5, 3.0, -3.0)), inner=(0.0, -1.0, 0.0))
    elif name == 'lash_up':                                 # (t1 cocked high and back, twisted round to throw it)
        p = P(seg1=T(-2, -6), seg2=T(-6, -10), head=T(-8, 4), **MAWOPEN(34), _face='fierce')
        p = lay(p, 't1', curl(_unit((0.45, 0.85, 0.35)), _unit((-0.2, -0.3, 1.0)), (40, 50)))
        p = wave(p, 't2', 0.3, 0.7, 0.4, (50, 50))
    elif name == 'lash':                                    # (whipped down and forward: the hook strikes ~1.1 blocks ahead)
        p = P(seg1=T(5, 6), seg2=T(10, 12), head=T(6, 4), **MAWOPEN(50), _face='fierce')
        R = at(p, 'seg2', PIVOT['t1a']); tg = (1.5, 2.0, -22.0)
        p = reach(p, 't1', tg, (_add(R, (2.0, 4.0, -3.0)), (2.5, 10.0, -14.0)), inner=(0.0, -1.0, 0.0))
        p = wave(p, 't2', 0.2, 0.7, 0.5, (50, 50))
    elif name == 'grab_up':                                 # (both tentacles raised, the maw wide, the eye wide)
        p = P(seg1=T(-3), seg2=T(-6), head=T(-12), **MAWOPEN(56), _face='wide')
        for t in TENT:
            p = lay(p, t, curl(_unit((sx_of(t) * 0.45, 0.85, -0.3)), _unit((0.0, 0.0, -1.0)), (40, 40)))
    elif name == 'grab':                                    # (both shot out ~1.3 blocks ahead at chest height)
        p = P(seg1=T(6), seg2=T(9), head=T(4), **MAWOPEN(46), _face='fierce')
        for t in TENT:
            R = at(p, 'seg2', PIVOT[t + 'a']); tg = (sx_of(t) * 1.6, 15.0, -26.0)
            p = reach(p, t, tg, (_add(R, _unit(_sub(tg, R)), 5.0), _add(R, _unit(_sub(tg, R)), 10.0)), inner=(0.0, -1.0, 0.0))
    elif name == 'grab_pull':                               # (hauled back in, curled round its catch, to the open maw)
        p = P(seg1=T(1), seg2=T(-3), head=T(6), **MAWOPEN(64, 1.3), _face='fierce')
        for t in TENT:
            sg = sx_of(t); R = at(p, 'seg2', PIVOT[t + 'a'])
            p = reach(p, t, (sg * 1.4, 21.0, -15.0), (_add(R, (sg * 3.0, 0.5, -2.5)), (sg * 4.5, 16.0, -11.0)))
    else:
        raise KeyError(name)
    return p


POSE_NAMES = (('idle_a', 'idle_b', 'idle_c') + tuple(f'walk_{k}' for k in range(4)) + tuple(f'run_{k}' for k in range(4)) + ('jump',) +
              tuple(f'swim_{k}' for k in range(8)) + ('sit_a', 'sit_b', 'happy', 'happy_b', 'hurt', 'tired', 'getup',
                                                       'lash_up', 'lash', 'grab_up', 'grab', 'grab_pull'))


class _Lazy(dict):
    """POSES, solved on first use"""
    def _f(self):
        if not dict.__len__(self): dict.update(self, {n: _pose(n) for n in POSE_NAMES})
    def __getitem__(self, k): self._f(); return dict.__getitem__(self, k)
    def __iter__(self): self._f(); return dict.__iter__(self)
    def __len__(self): self._f(); return dict.__len__(self)
    def __contains__(self, k): self._f(); return dict.__contains__(self, k)
    def keys(self): self._f(); return dict.keys(self)
    def items(self): self._f(); return dict.items(self)
    def values(self): self._f(); return dict.values(self)
    def get(self, k, d=None): self._f(); return dict.get(self, k, d)


POSES = _Lazy()
DRAFT = ['idle_a', 'idle_b', 'idle_c', 'walk_0', 'walk_1', 'run_0', 'jump', 'swim_0', 'sit_a', 'sit_b', 'happy', 'happy_b', 'hurt',
         'tired', 'getup', 'lash_up', 'lash', 'grab_up', 'grab', 'grab_pull']
# the cycles' durations (rigpet DUR: phase235._DUR plus these)
DUR = {'happy_b': 6, 'getup': 10, 'lash_up': 4, 'lash': 2, 'grab_up': 5, 'grab': 3, 'grab_pull': 6}

# ---------------------------------------------------------------------------------------------------- the doll, the case
DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62, 'groups': {f'bm:{PREFIX}{m}': 'head' for m in MAW}}   # (its head: the head and the maw)
FIT = None                                       # (set below, measured from the geometry)


# ---------------------------------------------------------------------------------------------------- the item
SEED = ['................',
        '........4.......',
        '.......454......',
        '.......4w4......',
        '......45w43.....',
        '......4w5433....',
        '.....455433c....',
        '.....4543332c...',
        '....44433333c...',
        '....4333333c32..',
        '....433oOo3c32..',
        '....3333o33c22..',
        '....3333333c21..',
        '.....3322cc221..',
        '......222222....',
        '........11......']
SEED_PAL = dict(MA.REMNANT_PAL, c='#d8283a', o='#ff7a1a', O='#ffd070')


def icon_raw():
    """a Mireling's Seed: a small black glossy droplet-seed, its tip curling up, a wet glint top left, a red vein running down
    its side, and low in it a tiny orange eye-glint looking out"""
    from sprites280 import hx
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); px = im.load()
    for y, row in enumerate(SEED):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch != '.': px[x, y] = hx(SEED_PAL[ch])
    return MA._outline(im)


def icon():
    import vanilla
    return vanilla.process(ITEM, icon_raw())


ICONS = {ITEM: icon_raw}

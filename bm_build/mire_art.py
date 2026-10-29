"""2.99a: THE DREAD MIRE (art) - a lesser manifestation of the Dread, loose in the world in hard mode (phase246 runs it).

THE LOOK. From a distance a shimmering puddle of reddish-black shadow on the ground, 4 blocks across, its red veins glowing.
When someone comes near it RISES: a worm-like black mass rearing ~5 blocks out of the puddle - a thick mound in the puddle,
three pinched worm segments tapering up to a blind, eyeless head-mass (Gravemind-like: folds across its crown, a hood flaring
down its back, swollen pustules) that splits open into a ring-mouth: an upper lip and a lower jaw, each set with a row of
fangs, and deep in its throat a ring of black fangs round a red glow. FOUR TENTACLES grow from its upper trunk (the shoulder
segment, seg3), each three ringed segments with glowing red pores along the inner side, ending in a barbed hook. Black goo
hangs in drips from its segments and its jaw. The palette is the Dread's (dread_sovereign_art: void, RED (208, 24, 46),
RED_L (255, 90, 100), EMBER) - but wet: near-black with deep oily reds, glossy square highlights, no speckle.

THE RIG (rigkit): PARTS =
  puddle                        the root: the flat irregular puddle (three terraced layers, veins, spatters, bubbles)
  mound                         the thick base mound standing in the puddle (child of puddle)
  seg1, seg2, seg3              the trunk, three worm segments (seg3 is the shoulder the tentacles grow from)
  head                          the head-mass with the upper lip, the throat and its fang ring, the hood (child of seg3)
  jaw                           the lower jaw, hinged at the back of the mouth (child of head; it drops to open the mouth)
  t1a t1b t1c ... t4a t4b t4c   the four tentacles, base to tip (tNa child of seg3, tNb of tNa, tNc of tNb). t1 front-right,
                                t2 front-left, t3 back-right, t4 back-left. Each about 50 design units (6.2 blocks) long.
Nineteen displays. Design units: the ground at y=0, facing -z, its right is +x. A design unit is 1/16 block at display scale
1.0 and one texel of the 16 px textures.

SCALE = RIG_SCALE = 2.0: the runtime passes SCALE to all three - a design unit is then 1/8 block and the sizes are the ones
asked for: the puddle ~4.4 x 4 blocks, the risen Mire ~5.3 blocks to the crown of its head (rise_2 / idle ~5 blocks), each
tentacle ~6.2 blocks long (grab_0's hook reaches 6 blocks ahead at chest height, stab_1's tips strike the ground ~4 blocks
ahead). As phase245 does with the knights:
    RF.part_nbt(A, p, tags, SCALE, model=A.model_id(p), scale0=(p != 'puddle'))
    RF.place(A, SCALE / 16, sel)
    RF.pose(A, A.POSES[name], SCALE, dur, sel)
(No PART_K: every part fits its model box at k 1.) A different SCALE scales the whole Mire (1.6: a 4-block one).

THE POSES (POSES[name]): dormant, rise_0, rise_1, rise_2, idle_a, idle_b, shriek, grab_0, grab_1, stab_0, stab_1, recoil,
sink_0, death_0, death_1. HIDDEN(part, pose): the pose's '_hide' (dormant: all but the puddle; rise_0: all but the puddle and
the mound) - rigfol shrinks those to scale 0 where they stand. A part rigfol hides isn't moved, so: summon every part but the
puddle at scale 0 (scale0=True), and before the first dormant run the dormant pose once with hide=False (it moves every part
into its sunk place under the puddle without touching scale) - then rise_0 / rise_1 grow them up out of the ground, not out of
the air. sink_0 leaves them sunk, so the dormant that follows hides them there.
  Long swings (stab_0 -> stab_1, grab_0 -> grab_1) are short (3-8 ticks) so the straight-line interpolation of each display
  barely cuts the arc; rigkit.mid(a, b) gives an in-between key if one looks wrong.

POINTS for the runtime (design units, on the part named): TIP[t] = (part, point) - the apex of tentacle t's hook; MOUTH =
('head', point) - the throat; DRIPS = [(part, point)] - where goo hangs (falling_dust of black_concrete looks right).
rigkit.point(A, A.POSES[name], part, point, scale=SCALE) -> blocks, relative to the host (yaw 0 = facing south, +z).

NAMES: model_id(part) -> 'mr_<part>' (RF.part_nbt's model=); model_name(part, pose=None, suffix='') -> the same (rigfol /
rigkit call it with a pose: one model per part, no per-pose swaps).

GLOW. The veins (every vein, pore and the hook tips: material 'glow', a slow pulsing animated texture), the mouth (the throat,
its roof and floor: 'ember') carry light_emission 15 - they are lit in the dark whatever the display's light. The puddle's
surface glows faintly itself (light_emission 3 / 5 / 7, outer rim to centre; its texture is a slow oily shimmer, animated),
"a puddle of glowing shadow". GLOW (the parts phase246 gives brightness {block:15, sky:15}) is EVERY PART: the hide is painted
near-black, so drawn at full brightness it still reads as shadow, but its wet square highlights and its silhouette show in a
pitch-dark cave instead of vanishing (unlit, only the veins and mouth would show and the tentacles would be invisible). If that
reads too bright in play, set GLOW = () - the light_emission glow stays.

SOUNDS: tools/mire_sfx.py synthesises vendor/mire_<name>.ogg (mono, 1.2-3.6 s); rp() ships them as assets/bm/sounds/mire/<name>.ogg
and registers bm:mire.<name> (with subtitles): bubble, rise, idle, lash, shriek, death. SOUNDS = {name: 'bm:mire.<name>'}
(only those whose .ogg exists) - phase246 falls back to vanilla for any missing.

ITEMS: ICONS = {'shadow_remnant', 'shadow_musk'} (raw 16x16, outlined; gen_rp's ICONS loop finishes them with vanilla.process).

gen_rp hook (PHASE2 block, after phase245):   import phase246; phase246.rp(sys.modules[__name__])
(phase246.rp is mire_art.rp(R); call one of them, not both.)
"""
import math
import os
import random
from PIL import Image

import rigkit
from rigkit import qs, el, seg, D, qrot, qmul

PREFIX = 'mr_'
RIG_SCALE = 2.0                                 # (a design unit = 1/8 block: ~5 blocks risen, the puddle 4 across)
SCALE = RIG_SCALE                               # (what the runtime passes to RF.part_nbt / RF.place (SCALE / 16) / RF.pose)
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------------------------------- the rig
TENT = ('t1', 't2', 't3', 't4')
SEGS = ('a', 'b', 'c')
LEN = {'a': 17.0, 'b': 16.0}                    # (a tentacle segment's length, joint to joint, along its own +y)
APEX = (0.0, 17.0, -2.2)                        # (the hook's apex on the c segment, from its joint)
ROOT = {'t1': (3.9, 29.4, -2.4), 't2': (-3.9, 29.6, -2.4), 't3': (4.3, 26.6, 2.0), 't4': (-4.3, 26.8, 2.0)}
OUT = {t: tuple(v / math.hypot(*d) for v in d) for t, d in
       {'t1': (0.8, 0.0, -0.6), 't2': (-0.8, 0.0, -0.6), 't3': (0.8, 0.0, 0.6), 't4': (-0.8, 0.0, 0.6)}.items()}

PIVOT = {'puddle': (0.0, 0.0, 0.0), 'mound': (0.0, 1.0, 0.0), 'seg1': (0.0, 8.0, 0.0), 'seg2': (0.0, 16.0, 0.3),
         'seg3': (0.0, 24.0, 0.5), 'head': (0.0, 31.5, 1.0), 'jaw': (0.0, 35.2, -1.0)}
PARENT = {'puddle': None, 'mound': 'puddle', 'seg1': 'mound', 'seg2': 'seg1', 'seg3': 'seg2', 'head': 'seg3', 'jaw': 'head'}
for _t in TENT:
    _x, _y, _z = ROOT[_t]
    PIVOT[_t + 'a'] = (_x, _y, _z); PIVOT[_t + 'b'] = (_x, _y + LEN['a'], _z); PIVOT[_t + 'c'] = (_x, _y + LEN['a'] + LEN['b'], _z)
    PARENT[_t + 'a'] = 'seg3'; PARENT[_t + 'b'] = _t + 'a'; PARENT[_t + 'c'] = _t + 'b'
PARTS = tuple(PIVOT)
TRUNK = ('mound', 'seg1', 'seg2', 'seg3', 'head', 'jaw')
TPARTS = tuple(t + s for t in TENT for s in SEGS)
PART_K = {}                                     # (every part fits its model box at its own size)
GLOW = PARTS                                    # (phase246: brightness 15 on these - see the docstring)
TIP = {t: (t + 'c', tuple(PIVOT[t + 'c'][i] + APEX[i] for i in range(3))) for t in TENT}
MOUTH = ('head', (0.0, 34.3, -3.0))


def model_id(part):
    """the model's id without the namespace (RF.part_nbt's model=)"""
    assert part in PIVOT, part
    return PREFIX + part


def model_name(part, pose=None, suffix=''):
    """rigfol / rigkit: the part's model, without 'bm:' (one model per part)"""
    return model_id(part) + (suffix or '')


def scale_of(pose=None):
    return RIG_SCALE


def HIDDEN(p, pose):
    return p in pose.get('_hide', ())


# ---------------------------------------------------------------------------------------------------- the palette
K0, K1, K2, K3, K4, K5, K6 = (8, 3, 6), (18, 7, 12), (30, 12, 19), (46, 18, 28), (72, 30, 42), (118, 56, 72), (176, 112, 124)
O1, O2 = (50, 10, 22), (80, 16, 32)                                     # (the oily reds in the black)
R0, R1, R2, R3, R4, R5 = (96, 8, 22), (150, 14, 32), (208, 24, 46), (255, 90, 100), (255, 170, 150), (255, 228, 210)
PAL = {'0': K0, '1': K1, '2': K2, '3': K3, '4': K4, '5': K5, '6': K6, 'o': O1, 'O': O2,
       'a': R0, 'b': R1, 'c': R2, 'd': R3, 'e': R4, 'f': R5}


def _grid(rows, pal=PAL):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 255)); px = im.load()
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            px[x, y] = tuple(pal[ch]) + (255,)
    return im


# the hide: wet black, a few glossy square highlights (a lit rim, a hot glint), recessed squares, oily red patches
HIDE = ['2222222222222222',
        '2344322222221122',
        '2456432222211112',
        '2443332222221122',
        '2333322222222222',
        '2222222oo2222222',
        '222222oOo2222222',
        '2222222o22223332',
        '1122222222234432',
        '1112222222235532',
        '2112222222233332',
        '2222222222222222',
        '22233322222o2222',
        '2234432222oOo122',
        '2234532222oo1112',
        '2223332222222122']
# the rings of a segment / the knuckles of a tentacle: two ridges, each a lit lip, a glossy line, the wet flank, a deep crease
RIB = ['3333333333333333',
       '4445444444454444',
       '3333333333333333',
       '2222222222222222',
       '22222o2222222222',
       '1111111111111111',
       '0000000000000000',
       '1111111111111111',
       '3333333333333333',
       '4444444544444444',
       '3333333333333333',
       '2222222222222222',
       '222222222222o222',
       '1111111111111111',
       '0000000000000000',
       '1111111111111111']
# the head's folds: vertical, each a lit left edge, a glossy ridge, its shadowed flank and a crease
FOLD = [''.join('34421010'[(x + (y // 8) * 4) % 8] for x in range(16)) for y in range(16)]
FOLD[2] = FOLD[2][:1] + '5' + FOLD[2][2:]
FOLD[11] = FOLD[11][:5] + '5' + FOLD[11][6:]
# the throat's glow, the lips' fire
EMBER = ['dddddddddddddddd',
         'deeddddddddddeed',
         'deeddddcdddddddd',
         'ddddddcccddddddd',
         'dddddddcdddeeddd',
         'dddeeddddddeeddd',
         'dddeeddddddddddd',
         'ddddddddcddddddd',
         'dddddddcccdddeed',
         'ddeeddddcddddeed',
         'ddeedddddddddddd',
         'ddddddddddeedddd',
         'dcddddddddeedddd',
         'cccddeeddddddddd',
         'dcdddeeddddddcdd',
         'dddddddddddddddd']
ANIMATED = {}                                                       # {texture: its .png.mcmeta}


def _vein_frame(k):
    """the veins' glow, frame k of the pulse: a red line with a hot square core every few texels"""
    lo, mid, hi = [tuple(round(c * k + d * (1 - k)) for c, d in zip(col, R0)) for col in (R1, R2, R3)]
    im = Image.new('RGBA', (16, 16), mid + (255,)); px = im.load()
    for y in range(16):
        for x in range(16):
            if (x // 4 + y // 4) % 2 == 0 and 1 <= x % 4 <= 2 and 1 <= y % 4 <= 2: px[x, y] = hi + (255,)
            elif x % 8 == 0 or y % 8 == 7: px[x, y] = lo + (255,)
    return im


def _pool_frame(i, n):
    """the puddle's surface, frame i of n: black with oily red pools; a glossy streak of shimmer drifts across it"""
    base = ['1111111111111111',
            '11oo111111111111',
            '1oOo11110111o111',
            '11o1111000111111',
            '1111111101111111',
            '111111111111oo11',
            '11101111111oOo11',
            '1100011111111o11',
            '1110111oo1111111',
            '111111oOOo111111',
            '1111111oo1111011',
            '1o11111111110001',
            'oOo1111111111011',
            '1o11110111111111',
            '1111100011111oo1',
            '1111110111111111']
    im = _grid(base); px = im.load()
    sh = 2 * i * 16 // (2 * n)
    for (x, y, c) in ((0, 3, K3), (1, 3, K4), (2, 3, K4), (3, 3, K3), (1, 2, K3), (2, 2, K5), (4, 10, K3), (5, 10, K4), (6, 10, K3),
                      (5, 9, K3), (9, 6, K3), (10, 6, K3), (10, 5, K4), (11, 13, K3), (12, 13, K4), (13, 13, K3), (12, 12, K3)):
        px[(x + sh) % 16, y] = c + (255,)
    return im


def _strip(frames):
    im = Image.new('RGBA', (16, 16 * len(frames))); [im.paste(f, (0, 16 * i)) for i, f in enumerate(frames)]
    return im


def _fang():
    """a fang, the whole of it on every face: dark at its root (top), pale at its point (bottom)"""
    cols = [(52, 26, 32), (66, 34, 40), (84, 48, 54), (104, 66, 70), (128, 92, 94), (154, 122, 120), (184, 156, 150), (206, 184, 176)]
    im = Image.new('RGBA', (16, 16)); px = im.load()
    for y in range(16):
        for x in range(16):
            c = cols[y // 2]
            if x >= 12: c = tuple(max(0, v - 18) for v in c)
            if x <= 3 and y >= 4: c = tuple(min(255, v + 14) for v in c)
            px[x, y] = c + (255,)
    return im


def _drip():
    """a drop of goo, the whole of it on every face: wet black, a glossy square glint top left"""
    return _grid(['1111111111111111', '1222222222222211', '1255432222222221', '1256542222222221', '1245432222222221',
                  '1234332222222221', '1233222222222221', '1222222222222221', '1222222222222221', '1222222222222221',
                  '1222222222222221', '1222222222222111', '1122222222221101', '1112222222211001', '1111111111110001',
                  '1111111111100011'])


def _barb():
    """a barb or hook: red-hot at its point (the top), black at its root"""
    rows = ['dddddddddddddddd', 'cccccccccccccccc', 'cccccccccccccccc', 'bbbbbbbbbbbbbbbb', 'bbbbbbbbbbbbbbbb', 'aaaaaaaaaaaaaaaa',
            'aaaaaaaaaaaaaaaa', 'OOOOOOOOOOOOOOOO', 'OOOOOOOOOOOOOOOO', 'oooooooooooooooo', 'oooooooooooooooo', '3333333333333333',
            '3333333333333333', '2222222222222222', '2222222222222222', '1111111111111111']
    return _grid(rows)


def textures():
    """{name: RGBA} for assets/bm/textures/block (the animated ones are strips; rp's post writes their .mcmeta)"""
    T = {'mr_hide': _grid(HIDE), 'mr_rib': _grid(RIB), 'mr_fold': _grid(FOLD), 'mr_ember': _grid(EMBER),
         'mr_fang': _fang(), 'mr_drip': _drip(), 'mr_barb': _barb(), 'mr_void': _grid(['0' * 16] * 16)}
    pulse = [1.0, 0.94, 0.82, 0.68, 0.58, 0.68, 0.82, 0.94]
    T['mr_glow'] = _strip([_vein_frame(k) for k in pulse])
    T['mr_pool'] = _strip([_pool_frame(i, 8) for i in range(8)])
    ANIMATED.update({'mr_glow': {'animation': {'frametime': 5, 'interpolate': True}},
                     'mr_pool': {'animation': {'frametime': 6, 'interpolate': True}}})
    return T


MATS = ('hide', 'rib', 'fold', 'ember', 'fang', 'drip', 'barb', 'void', 'glow', 'pool')
LIGHT = {'glow': 15, 'ember': 15}                                   # (light_emission by material; the puddle's layers set their own)
FULL = {'fang', 'drip', 'barb'}                                     # (the whole texture on every face)
F6 = ('north', 'south', 'east', 'west', 'up', 'down')

# ---------------------------------------------------------------------------------------------------- building helpers
_rs = random.Random(11)
_PV = [None]


def E(fr, to, mat, faces=None, uv=None, light=None, rot=None):
    """an element of a material (texture 'mr_<mat>') about the current part's joint; its texture window shifted at random"""
    fr, to = tuple(min(a, b) for a, b in zip(fr, to)), tuple(max(a, b) for a, b in zip(fr, to))
    if mat in FULL and uv is None: uv = {f: [0, 0, 16, 16] for f in F6}
    shift = None if uv else (_rs.random(), _rs.random())
    e = el(fr, to, PREFIX + mat, _PV[0], rot=rot, uv=uv, faces=faces, light=LIGHT.get(mat, 0) if light is None else light, shift=shift)
    return e


def SEG(a, b, w, mat, up=FRONT, ext=0.0, h=None, light=None):
    """a square box along the line a -> b (rigkit.seg)"""
    e = seg(a, b, w, h or w, PREFIX + mat, _PV[0], up, ext, light=LIGHT.get(mat, 0) if light is None else light,
            shift=None if mat in FULL else (_rs.random(), _rs.random()))
    if mat in FULL:
        for fc in e['faces'].values(): fc['uv'] = [0, 0, 16, 16]
    return e


def OCT(cx, cz, y0, y1, rx, rz, mat, k=0.72, inset=0.06, faces=None):
    """a rounded (octagonal) prism: two crossed boxes"""
    return [E((cx - rx, y0, cz - rz * k), (cx + rx, y1, cz + rz * k), mat, faces=faces),
            E((cx - rx * k, y0 + inset, cz - rz), (cx + rx * k, y1 - inset, cz + rz), mat, faces=faces)]


def VEIN(path, axis, at, out, w=0.6, d=0.22, mat='glow'):
    """a glowing vein laid on a face: path [(u, v), ...] of axis-aligned steps in the face's plane - (y, z) on an x face, (x, y)
    on a z face, (x, z) on a y face; `at` the face's plane, `out` (+1 / -1) its outward side"""
    els = []
    lo, hi = (at - 0.08, at + d) if out > 0 else (at - d, at + 0.08)
    for (u0, v0), (u1, v1) in zip(path, path[1:]):
        a0, a1 = sorted((u0, u1)); b0, b1 = sorted((v0, v1))
        if a0 == a1: a0, a1 = a0 - w / 2, a1 + w / 2
        else: a0, a1 = a0 - w / 2, a1 + w / 2
        if b0 == b1: b0, b1 = b0 - w / 2, b1 + w / 2
        else: b0, b1 = b0 - w / 2, b1 + w / 2
        if axis == 'x': fr, to = (lo, a0, b0), (hi, a1, b1)
        elif axis == 'z': fr, to = (a0, b0, lo), (a1, b1, hi)
        else: fr, to = (a0, lo, b0), (a1, hi, b1)
        els.append(E(fr, to, mat))
    return els


def DRIP(x, y, z, ln, w=0.7, ball=1.3):
    """a strand of goo hanging from (x, y, z), ln long, a drop at its end"""
    return [E((x - w / 2, y - ln, z - w / 2), (x + w / 2, y + 0.2, z + w / 2), 'drip'),
            E((x - ball / 2, y - ln - ball * 0.8, z - ball / 2), (x + ball / 2, y - ln + ball * 0.2, z + ball / 2), 'drip')]


# ---------------------------------------------------------------------------------------------------- the puddle
def _r(th, layer):
    r = 15.6 + 1.8 * math.sin(3 * th + 0.4) + 1.2 * math.sin(5 * th + 2.0) + 0.7 * math.sin(8 * th + 1.3)
    if layer == 1: r += -3.6 + 1.0 * math.sin(4 * th + 0.7)
    if layer == 2: r += -8.2 + 1.3 * math.sin(2 * th + 1.9)
    return r * (1.0 + 0.06 * math.cos(2 * th))                       # (a little wider than deep)


CELL = 2.0
PUDDLE_Y = (0.0, 0.25, 0.5, 0.75)                                  # (each layer's floor and roof)
PUDDLE_LIGHT = (3, 5, 7)


def _mask(layer):
    n = 11; out = set()
    for i in range(-n, n):
        for j in range(-n, n):
            cx, cz = (i + 0.5) * CELL, (j + 0.5) * CELL
            if math.hypot(cx, cz) < _r(math.atan2(cz, cx), layer): out.add((i, j))
    return out


def _rects(cells, cap=8):
    """greedy rectangles over a set of cells (no side over cap cells: no face over 16 texels)"""
    left = set(cells); out = []
    for j in sorted({c[1] for c in cells}):
        for i in sorted({c[0] for c in cells}):
            if (i, j) not in left: continue
            w = 1
            while (i + w, j) in left and w < cap: w += 1
            h = 1
            while h < cap and all((i + k, j + h) in left for k in range(w)): h += 1
            for k in range(w):
                for m in range(h): left.discard((i + k, j + m))
            out.append((i, j, w, h))
    return out


def _layer_at(x, z, masks):
    c = (math.floor(x / CELL), math.floor(z / CELL)); lv = -1
    for L in range(3):
        if c in masks[L]: lv = L
    return lv


def _puddle():
    P = []; masks = [_mask(L) for L in range(3)]
    for L in range(3):
        for (i, j, w, h) in _rects(masks[L]):
            P.append(E((i * CELL, PUDDLE_Y[L], j * CELL), ((i + w) * CELL, PUDDLE_Y[L + 1], (j + h) * CELL), 'pool',
                       faces=('north', 'south', 'east', 'west', 'up'), light=PUDDLE_LIGHT[L]))
    rnd = random.Random(23)
    # spatters round the rim (goo flung out of it)
    for k in range(9):
        th = 2 * math.pi * k / 9 + rnd.uniform(-0.2, 0.2); r = _r(th, 0) + rnd.uniform(1.4, 3.0); s = rnd.choice((1.0, 1.5, 2.0))
        x, z = r * math.cos(th), r * math.sin(th)
        x, z = round(x * 2) / 2, round(z * 2) / 2
        P.append(E((x - s / 2, 0.0, z - s / 2), (x + s / 2, 0.18, z + s / 2), 'pool', faces=('north', 'south', 'east', 'west', 'up'), light=3))
    # bubbles and blisters (glossy, swelling on the surface)
    for (x, z, s) in ((-6.5, 3.5, 1.6), (4.5, -6.0, 1.2), (8.5, 4.5, 1.4), (-3.0, -9.0, 1.0), (-10.0, -2.5, 1.2), (2.0, 9.5, 1.0)):
        y = PUDDLE_Y[_layer_at(x, z, masks) + 1]
        P.append(E((x - s / 2, y - 0.1, z - s / 2), (x + s / 2, y + s * 0.45, z + s / 2), 'drip', faces=('north', 'south', 'east', 'west', 'up')))
    # the veins: cracks of red light running out from the middle, in square steps, branching
    def run(x, z, dirs):
        pts = [(x, z)]
        for (dx, dz, n) in dirs:
            x += dx * n; z += dz * n; pts.append((x, z))
        return pts
    paths = [run(1, 0, [(1, 0, 4), (0, -1, 2), (1, 0, 5), (0, -1, 3), (1, 0, 3)]),
             run(0, 1, [(0, 1, 3), (1, 0, 2), (0, 1, 5), (-1, 0, 2), (0, 1, 3)]),
             run(-1, 0, [(-1, 0, 5), (0, 1, 3), (-1, 0, 4), (0, 1, 2)]),
             run(0, -1, [(0, -1, 4), (-1, 0, 3), (0, -1, 4), (-1, 0, 3), (0, -1, 2)]),
             run(1, 1, [(1, 0, 2), (0, 1, 4), (1, 0, 4), (0, 1, 2), (1, 0, 3)]),
             run(-1, -1, [(-1, 0, 3), (0, -1, 2), (-1, 0, 4), (0, -1, 3)]),
             run(7, -3, [(0, -1, 2), (1, 0, 2), (0, -1, 3)]),                 # (branches)
             run(-6, 1, [(0, -1, 3), (-1, 0, 3)]),
             run(2, 8, [(-1, 0, 3), (0, 1, 3)]),
             run(-5, -6, [(1, 0, 2), (0, -1, 4)])]
    for pts in paths:
        for (x0, z0), (x1, z1) in zip(pts, pts[1:]):
            # split each run where the surface steps, so the vein sits just proud of the layer it crosses
            n = int(round(max(abs(x1 - x0), abs(z1 - z0))))
            cells = [(x0 + (x1 - x0) * (k + 0.5) / n, z0 + (z1 - z0) * (k + 0.5) / n) for k in range(n)]
            k = 0
            while k < n:
                L = _layer_at(*cells[k], masks); m = k
                while m + 1 < n and _layer_at(*cells[m + 1], masks) == L: m += 1
                if L >= 0:
                    a = (x0 + (x1 - x0) * k / n, z0 + (z1 - z0) * k / n); b = (x0 + (x1 - x0) * (m + 1) / n, z0 + (z1 - z0) * (m + 1) / n)
                    top = PUDDLE_Y[L + 1]
                    xa, xb = sorted((a[0], b[0])); za, zb = sorted((a[1], b[1]))
                    if xa == xb: xa, xb = xa - 0.5, xb + 0.5
                    if za == zb: za, zb = za - 0.5, zb + 0.5
                    P.append(E((xa, top - 0.1, za), (xb, top + 0.12, zb), 'glow', faces=('north', 'south', 'east', 'west', 'up')))
                k = m + 1
    return P


# ---------------------------------------------------------------------------------------------------- the trunk
def _mound():
    M = []
    M += OCT(0, 0, 0.3, 2.8, 10.6, 10.0, 'hide')
    M += OCT(0, 0, 2.6, 5.8, 8.6, 8.2, 'hide')
    M += OCT(0, 0.2, 5.6, 9.4, 7.2, 7.0, 'hide')
    for k, (th, s) in enumerate(((0.3, 4.4), (1.5, 3.6), (2.5, 4.8), (3.6, 3.8), (4.6, 4.2), (5.6, 3.4))):    # (lobes: it oozes out)
        x, z = 10.4 * math.cos(th), 10.0 * math.sin(th)
        M.append(E((x - s / 2, 0.05, z - s / 2), (x + s / 2, 1.6 + 0.2 * (k % 2), z + s / 2), 'hide'))
    M += [E((-8.0, 2.4, -6.4), (-5.0, 3.6, -3.4), 'drip'), E((5.6, 5.4, 3.0), (7.6, 6.4, 5.0), 'drip'), E((2.0, 9.0, -5.8), (4.0, 9.8, -4.4), 'drip')]
    # veins climbing the tiers: up a face, across a ledge, up again
    def climb(axis, sgn, off, steps=((10.6, 0.3, 2.8), (8.6, 2.8, 5.8), (7.2, 5.8, 9.4))):
        els = []
        for i, (r, y0, y1) in enumerate(steps):
            if axis == 'x': els += VEIN([(y0, off), (y1, off)], 'x', sgn * r, sgn)
            else: els += VEIN([(off, y0), (off, y1)], 'z', sgn * r, sgn)
            if i + 1 < len(steps):
                r2 = steps[i + 1][0]
                if axis == 'x': els += VEIN([(sgn * r, off), (sgn * r2, off)], 'y', y1, 1)
                else: els += VEIN([(off, sgn * r), (off, sgn * r2)], 'y', y1, 1)
        return els
    M += climb('x', 1, -2.2) + climb('x', -1, 2.6) + climb('z', -1, 1.4) + climb('z', 1, -3.0)
    return M


def _segment(y0, y1, r, cz=0.0, lumps=(), veins=(), drips=()):
    """a worm segment: a pinched neck (ringed) at its foot down into the one below, the swollen body, a narrower shoulder"""
    S = []
    S += OCT(0, cz, y0 - 1.8, y0 + 1.4, r - 1.0, r - 1.0, 'rib')
    S += OCT(0, cz, y0 + 1.0, y1 - 1.0, r, r, 'hide')
    S += OCT(0, cz, y1 - 1.2, y1 + 0.3, r - 0.8, r - 0.8, 'hide')
    for (x, y, z, sx, sy, sz) in lumps:                              # (cysts swelling out of it)
        S.append(E((x - sx / 2, y - sy / 2, z - sz / 2), (x + sx / 2, y + sy / 2, z + sz / 2), 'hide'))
    for v in veins: S += VEIN(*v)
    for d in drips: S += DRIP(*d)
    return S


def _seg1():
    r = 6.4; y0, y1 = 8.0, 16.6
    return _segment(y0, y1, r, 0.0,
                    lumps=[(6.6, 12.6, -1.0, 1.6, 3.0, 3.0), (-2.2, 11.0, -6.4, 3.4, 2.6, 1.4)],
                    veins=[([(9.6, -1.4), (12.0, -1.4), (12.0, 1.0), (15.4, 1.0)], 'x', r, 1),
                           ([(9.6, 2.0), (11.4, 2.0), (11.4, -0.6), (15.4, -0.6)], 'x', -r, -1),
                           ([(1.6, 9.6), (1.6, 12.6), (3.0, 12.6), (3.0, 15.4)], 'z', -r, -1),
                           ([(-2.4, 9.6), (-2.4, 13.4), (0.0, 13.4), (0.0, 15.4)], 'z', r, 1)],
                    drips=[(4.8, 9.1, -4.4, 2.2), (-5.0, 9.1, 2.6, 3.0)])


def _seg2():
    r = 5.8; y0, y1 = 16.0, 24.6; cz = 0.3
    return _segment(y0, y1, r, cz,
                    lumps=[(-6.0, 20.6, 1.8, 1.4, 2.6, 2.6), (2.4, 19.4, -5.8, 2.4, 2.0, 1.4)],
                    veins=[([(17.6, 0.8), (20.4, 0.8), (20.4, -1.6), (23.4, -1.6)], 'x', r, 1),
                           ([(17.6, -1.0), (21.6, -1.0), (21.6, 1.4), (23.4, 1.4)], 'x', -r, -1),
                           ([(-1.2, 17.6), (-1.2, 21.0), (1.2, 21.0), (1.2, 23.4)], 'z', -r + cz, -1)],
                    drips=[(-4.2, 17.1, -3.6, 2.6), (3.8, 17.1, 3.8, 1.8)])


def _seg3():
    r = 5.6; y0, y1 = 24.0, 32.4; cz = 0.5
    S = _segment(y0, y1, r, cz, lumps=[(0.0, 27.8, 6.2, 3.2, 2.4, 1.2)],
                 veins=[([(-1.0, 25.6), (-1.0, 28.6), (1.4, 28.6), (1.4, 31.4)], 'z', -r + cz, -1)],
                 drips=[(1.6, 25.1, -4.8, 2.0)])
    for t in TENT:                                                  # (the sockets the tentacles grow from: swollen, ringed)
        x, y, z = ROOT[t]; o = OUT[t]
        a = (x - o[0] * 2.4, y, z - o[2] * 2.4); b = (x + o[0] * 0.6, y, z + o[2] * 0.6)
        S.append(SEG(a, b, 5.6, 'hide', up=UP))
        S.append(SEG((x - o[0] * 0.4, y, z - o[2] * 0.4), (x + o[0] * 1.0, y, z + o[2] * 1.0), 6.2, 'rib', up=UP))
    return S


def _head():
    H = []
    # the mass: a tall dome over the throat, the hood flaring down its back
    H += [E((-6.2, 32.6, -1.6), (6.2, 41.0, 7.0), 'hide'), E((-5.2, 31.6, -2.0), (5.2, 42.0, 7.6), 'hide'),
          E((-5.6, 28.4, 5.8), (5.6, 34.4, 8.6), 'rib'), E((-4.4, 27.2, 6.6), (4.4, 30.0, 9.0), 'rib'),       # (the hood)
          E((-6.6, 29.6, 3.2), (-5.4, 34.6, 7.2), 'rib'), E((5.4, 29.6, 3.2), (6.6, 34.6, 7.2), 'rib')]
    # the upper lip, over the mouth: the brow, folded
    H += [E((-5.8, 36.6, -8.2), (5.8, 41.0, -1.6), 'hide'), E((-4.8, 40.8, -7.4), (4.8, 41.8, -1.6), 'hide'),
          E((-5.2, 39.4, -8.8), (5.2, 41.2, -8.2), 'fold')]
    for z0, z1 in ((-6.8, -5.4), (-3.6, -2.2), (-0.4, 1.0), (2.8, 4.2), (5.4, 6.6)):                 # (folds across the crown)
        w = 5.6 if z0 < 4 else 4.8
        H.append(E((-w, 41.6, z0), (w, 42.8, z1), 'fold'))
    H += [E((-0.9, 42.4, -7.0), (0.9, 43.6, 6.2), 'fold'), E((-3.6, 42.6, -1.6), (-2.2, 43.2, 4.4), 'fold'), E((2.2, 42.6, -4.4), (3.6, 43.2, 2.6), 'fold')]
    # pustules, swollen and glossy, a crack of light in each
    H += [E((6.0, 36.8, 0.4), (7.4, 39.6, 3.6), 'hide'), E((7.35, 37.8, 1.6), (7.55, 38.5, 2.6), 'glow'),
          E((-7.2, 38.4, -0.6), (-6.0, 40.4, 1.8), 'hide'), E((-7.35, 39.0, 0.2), (-7.15, 39.8, 0.9), 'glow'),
          E((-3.0, 37.8, 7.4), (0.2, 40.2, 8.6), 'hide'), E((-1.8, 38.6, 8.55), (-0.8, 39.2, 8.75), 'glow')]
    # veins from the mouth's corners back over the head
    for s in (1, -1):
        H += VEIN([(36.8, -7.6), (36.8, -4.0), (38.6, -4.0), (38.6, -0.4), (40.2, -0.4), (40.2, 4.0)], 'x', s * 6.2, s)
    H += VEIN([(-3.0, -1.6), (-3.0, 2.0), (-1.4, 2.0)], 'y', 41.8, 1) + VEIN([(2.6, 4.6), (2.6, 6.8)], 'y', 41.8, 1)
    H += VEIN([(-1.6, 33.0), (-1.6, 36.0), (1.6, 36.0), (1.6, 39.0)], 'z', 7.6, 1)
    # inside: the roof of the mouth and the throat (lit), a ring of black fangs round the throat's hole
    H += [E((-5.0, 36.45, -7.4), (5.0, 36.62, -1.6), 'ember'),
          E((-4.4, 31.9, -1.9), (4.4, 36.6, -1.55), 'ember'),
          E((-1.5, 32.8, -1.95), (1.5, 35.8, -1.85), 'void')]
    for k in range(8):
        a = 2 * math.pi * k / 8; x, y = 2.6 * math.cos(a), 34.3 + 2.2 * math.sin(a)
        H.append(E((x - 0.35, y - 0.35, -3.3), (x + 0.35, y + 0.35, -1.9), 'fang', uv={f: [6, 0, 10, 16] for f in F6}))
    # the upper fangs, hanging from the lip; and down its sides (the ring's upper half)
    for x in (-4.4, -2.2, 0.0, 2.2, 4.4):
        H.append(E((x - 0.45, 34.6, -7.8), (x + 0.45, 36.6, -6.9), 'fang'))
    for s in (1, -1):
        for z in (-5.6, -3.4):
            H.append(E((s * 5.3 - 0.4, 35.0, z - 0.4), (s * 5.3 + 0.4, 36.6, z + 0.4), 'fang'))
    return H


def _jaw():
    J = [E((-5.6, 31.2, -8.6), (5.6, 36.3, -1.0), 'hide'), E((-4.8, 30.6, -8.0), (4.8, 31.4, -1.6), 'hide'),
         E((-5.0, 36.0, -7.4), (5.0, 36.36, -1.2), 'ember'),                                         # (the floor of the mouth, lit)
         E((-5.0, 33.0, -9.1), (5.0, 35.0, -8.6), 'fold')]
    lower = {f: [0, 16, 16, 0] for f in F6}                                                           # (point up: the texture flipped)
    for x in (-3.3, -1.1, 1.1, 3.3):
        J.append(E((x - 0.45, 36.3, -7.8), (x + 0.45, 38.0, -6.9), 'fang', uv=lower))
    for s in (1, -1):
        for z in (-4.6, -2.4):
            J.append(E((s * 5.0 - 0.4, 36.3, z - 0.4), (s * 5.0 + 0.4, 37.6, z + 0.4), 'fang', uv=lower))
    for s in (1, -1):
        J += VEIN([(32.0, -8.0), (32.0, -5.2), (34.4, -5.2), (34.4, -2.0)], 'x', s * 5.6, s)
    J += DRIP(-3.4, 31.0, -7.6, 3.4) + DRIP(1.6, 31.0, -8.0, 2.2, 0.6, 1.1) + DRIP(4.2, 31.4, -6.4, 4.4)
    return J


def _tentacle_seg(t, s):
    """one segment of a tentacle, built up its own +y from its joint (the inner side, with its glowing pores, toward -z)"""
    x, y, z = PIVOT[t + s]; T = []
    if s == 'a': knuck, boxes, rings, pores = (5.4, -2.2, 1.6), [(4.6, 1.0, 6.4), (4.2, 6.0, 11.8), (3.8, 11.4, 17.8)], (6.0, 11.6), (3.0, 5.6, 8.4, 11.0, 13.8)
    elif s == 'b': knuck, boxes, rings, pores = (4.6, -1.8, 1.2), [(3.6, 0.6, 6.0), (3.2, 5.6, 11.2), (2.8, 10.8, 16.8)], (5.6, 10.8), (2.6, 5.2, 7.8, 10.2, 12.8)
    else: knuck, boxes, rings, pores = (3.4, -1.4, 1.0), [(2.6, 0.4, 5.4), (2.2, 5.0, 10.0), (1.8, 9.6, 13.6)], (5.0,), (2.4, 4.8, 7.2, 9.4)
    w, k0, k1 = knuck
    T.append(E((x - w / 2, y + k0, z - w / 2), (x + w / 2, y + k1, z + w / 2), 'rib'))
    for i, (bw, b0, b1) in enumerate(boxes):
        ox = 0.25 if i % 2 else -0.25
        T.append(E((x + ox - bw / 2, y + b0, z - bw / 2), (x + ox + bw / 2, y + b1, z + bw / 2), 'hide'))
    for ry in rings:                                                 # (a ring where it narrows)
        bw = [b for b in boxes if b[1] <= ry <= b[2]][0][0] + 0.5
        T.append(E((x - bw / 2, y + ry - 0.4, z - bw / 2), (x + bw / 2, y + ry + 0.4, z + bw / 2), 'rib'))
    for py in pores:                                                 # (pores of red light down its inner side)
        bw = [b for b in boxes if b[1] <= py <= b[2]][0][0]
        T.append(E((x - 0.55, y + py - 0.55, z - bw / 2 - 0.18), (x + 0.55, y + py + 0.55, z - bw / 2 + 0.1), 'glow'))
    for py in pores[1::2]:                                           # (and barbs down its outer side)
        bw = [b for b in boxes if b[1] <= py <= b[2]][0][0]
        T.append(SEG((x, y + py - 0.6, z + bw / 2 - 0.3), (x, y + py - 1.6, z + bw / 2 + 1.0 + (0.4 if s == 'a' else 0.0)), 0.6 if s == 'c' else 0.8, 'barb', up=UP))
    if s == 'c':                                                     # (the hook, curling to the inner side; side barbs; its point lit)
        T += [SEG((x, y + 13.0, z), (x, y + 15.6, z - 0.8), 1.7, 'hide', up=FRONT, ext=0.3),
              SEG((x, y + 15.6, z - 0.8), (x, y + 16.9, z - 2.6), 1.4, 'barb', up=FRONT, ext=0.3),
              SEG((x, y + 16.9, z - 2.6), (x, y + 16.2, z - 4.4), 1.05, 'barb', up=FRONT, ext=0.2),
              E((x - 0.35, y + 15.4, z - 5.0), (x + 0.35, y + 16.2, z - 4.3), 'glow')]
        for sx in (1, -1):
            T.append(SEG((x + sx * 0.8, y + 11.0, z), (x + sx * 2.6, y + 9.2, z + 0.5), 0.7, 'barb', up=UP))
            T.append(SEG((x + sx * 1.0, y + 6.6, z), (x + sx * 2.6, y + 5.2, z + 0.4), 0.6, 'barb', up=UP))
    return T


# ---------------------------------------------------------------------------------------------------- models
_RAW = {}


def _build():
    """{part: [elements]} - the geometry"""
    if _RAW: return _RAW
    _rs.seed(11)
    fns = {'puddle': _puddle, 'mound': _mound, 'seg1': _seg1, 'seg2': _seg2, 'seg3': _seg3, 'head': _head, 'jaw': _jaw}
    for p in PARTS:
        _PV[0] = PIVOT[p]
        _RAW[p] = fns[p]() if p in fns else _tentacle_seg(p[:2], p[2])
    return _RAW


def models():
    """{model id: (textures, elements)} - one per part, as gen_rp's HATS take them"""
    M = {}
    for part, els in _build().items():
        for e in els:
            for v in e['from'] + e['to']:
                assert -16 <= v <= 32, (part, e['from'], e['to'])
            for fc in e['faces'].values():
                assert all(0.0 <= t <= 16.0 for t in fc['uv']), (part, fc['uv'])
        used = sorted({fc['texture'][1:] for e in els for fc in e['faces'].values()})
        M[model_id(part)] = ({t: f'bm:block/{t}' for t in used}, els)
    return M


# ---------------------------------------------------------------------------------------------------- world geometry (checks)
def _rotm(r):
    def rx(a): c, s = math.cos(a), math.sin(a); return [[1, 0, 0], [0, c, -s], [0, s, c]]
    def ry(a): c, s = math.cos(a), math.sin(a); return [[c, 0, s], [0, 1, 0], [-s, 0, c]]
    def rz(a): c, s = math.cos(a), math.sin(a); return [[c, -s, 0], [s, c, 0], [0, 0, 1]]
    def mm(A, B): return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    if 'axis' in r: return {'x': rx, 'y': ry, 'z': rz}[r['axis']](math.radians(r['angle']))
    return mm(mm(rz(math.radians(r.get('z', 0))), ry(math.radians(r.get('y', 0)))), rx(math.radians(r.get('x', 0))))


def world_boxes(pose, parts=None, xf=None):
    """{part: [(centre, axes, half extents)]} - each element as an oriented box in the world (display frame, design units)"""
    raw = _build(); xf = xf or rigkit.solve(PIVOT, PARENT, pose); out = {}
    for p in (parts or PARTS):
        if HIDDEN(p, pose): continue
        Q, t = xf[p]; pv = PIVOT[p]; dp = D(pv); W = tuple(t[i] + dp[i] for i in range(3)); bl = []
        for e in raw[p]:
            f, to = e['from'], e['to']
            c = [(f[i] + to[i]) / 2 for i in range(3)]; h = [abs(to[i] - f[i]) / 2 for i in range(3)]
            ax = [(1.0, 0, 0), (0, 1.0, 0), (0, 0, 1.0)]
            if 'rotation' in e:
                R = _rotm(e['rotation']); o = e['rotation']['origin']
                c = [sum(R[i][k] * (c[k] - o[k]) for k in range(3)) + o[i] for i in range(3)]
                ax = [tuple(R[i][j] for i in range(3)) for j in range(3)]
            cd = tuple(c[i] - 8 + pv[i] for i in range(3))
            cw = qrot(Q, tuple(D(cd)[i] - dp[i] for i in range(3)))
            bl.append((tuple(W[i] + cw[i] for i in range(3)), tuple(qrot(Q, D(a)) for a in ax), tuple(h)))
        out[p] = bl
    return out


def extent(pose, parts=None):
    """(lowest y, highest y, nearest z, farthest-forward z) of the posed parts, design units (front is -z)"""
    lo, hi, zf = 1e9, -1e9, 1e9
    for bl in world_boxes(pose, parts).values():
        for c, ax, h in bl:
            ey = sum(abs(ax[i][1]) * h[i] for i in range(3)); ez = sum(abs(ax[i][2]) * h[i] for i in range(3))
            lo = min(lo, c[1] - ey); hi = max(hi, c[1] + ey); zf = min(zf, -(c[2] + ez))      # (display z -> design z)
    return lo, hi, zf


def at(pose, part, p, xf=None):
    """where a design point carried by `part` stands in the world (design units)"""
    xf = xf or rigkit.solve(PIVOT, PARENT, pose); Q, t = xf[part]; pv = D(PIVOT[part])
    r = qrot(Q, tuple(D(p)[i] - pv[i] for i in range(3)))
    return D(tuple(t[i] + pv[i] + r[i] for i in range(3)))


# ---------------------------------------------------------------------------------------------------- posing kit
def T(lean=0.0, twist=0.0, side=0.0):
    """a trunk joint's bend (display frame): lean + forward (- back), twist + turns its right forward, side + to its left"""
    return qs(('y', twist), ('x', lean), ('z', side))


def JAW(open_):
    return qs(('x', open_))


def _unit(v):
    n = math.sqrt(sum(c * c for c in v)); return tuple(c / n for c in v)


def _add(a, b, k=1.0): return tuple(a[i] + k * b[i] for i in range(3))
def _sub(a, b): return tuple(a[i] - b[i] for i in range(3))
def _dot(a, b): return sum(a[i] * b[i] for i in range(3))
def _cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def _conj(q): return (-q[0], -q[1], -q[2], q[3])


def _mat2q(m):
    tr = m[0][0] + m[1][1] + m[2][2]
    if tr > 0:
        s = math.sqrt(tr + 1.0) * 2; return ((m[2][1] - m[1][2]) / s, (m[0][2] - m[2][0]) / s, (m[1][0] - m[0][1]) / s, 0.25 * s)
    if m[0][0] > m[1][1] and m[0][0] > m[2][2]:
        s = math.sqrt(1.0 + m[0][0] - m[1][1] - m[2][2]) * 2; return (0.25 * s, (m[0][1] + m[1][0]) / s, (m[0][2] + m[2][0]) / s, (m[2][1] - m[1][2]) / s)
    if m[1][1] > m[2][2]:
        s = math.sqrt(1.0 + m[1][1] - m[0][0] - m[2][2]) * 2; return ((m[0][1] + m[1][0]) / s, 0.25 * s, (m[1][2] + m[2][1]) / s, (m[0][2] - m[2][0]) / s)
    s = math.sqrt(1.0 + m[2][2] - m[0][0] - m[1][1]) * 2; return ((m[0][2] + m[2][0]) / s, (m[1][2] + m[2][1]) / s, 0.25 * s, (m[1][0] - m[0][1]) / s)


def _frame(a, b):
    """columns (x, y, z) of a right-handed frame (display frame): y along a, z as near b as it can be"""
    y = _unit(a); z = _sub(b, tuple(_dot(b, y) * c for c in y))
    if _dot(z, z) < 1e-8: z = _cross(y, (1.0, 0.0, 0.0) if abs(y[0]) < 0.9 else (0.0, 0.0, 1.0))
    z = _unit(z); x = _cross(y, z)
    return x, y, z


def _aim(local_axis, local_in, world_axis, world_in):
    """the world turn (display frame) laying a part's local axis along world_axis, its local inner side toward world_in (design)"""
    lx, ly, lz = _frame(D(local_axis), D(local_in)); wx, wy, wz = _frame(D(world_axis), D(world_in))
    L = [[lx[i], ly[i], lz[i]] for i in range(3)]; W = [[wx[i], wy[i], wz[i]] for i in range(3)]
    M = [[sum(W[i][k] * L[j][k] for k in range(3)) for j in range(3)] for i in range(3)]      # (W L^T)
    return _mat2q(M)


def _rod(v, axis, deg):
    """v turned deg about axis (Rodrigues)"""
    k = _unit(axis); a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    kv = _cross(k, v); kd = _dot(k, v)
    return tuple(v[i] * c + kv[i] * s + k[i] * kd * (1 - c) for i in range(3))


def curl(d0, toward, bends):
    """three directions: d0, then turned toward `toward` by each bend in turn (a tentacle curling)"""
    d0 = _unit(d0); ax = _cross(d0, _unit(toward))
    if _dot(ax, ax) < 1e-8: ax = (1.0, 0.0, 0.0)
    out = [d0]
    for b in bends: out.append(_unit(_rod(out[-1], ax, b)))
    return out


SEG_AXIS = {'a': (0.0, 1.0, 0.0), 'b': (0.0, 1.0, 0.0), 'c': _unit(APEX)}
SEG_LEN = {'a': LEN['a'], 'b': LEN['b'], 'c': math.sqrt(sum(v * v for v in APEX))}


def _root(pose, t):
    """the world place of tentacle t's root (design units), as the trunk stands in the pose"""
    return at(pose, 'seg3', PIVOT[t + 'a'])


def lay(pose, t, dirs, inner=None):
    """set tentacle t's three segments along world directions dirs (design frame); each segment's inner side (its pores, its
    hook) turned to the concave side of the chain (or to `inner`)"""
    p = dict(pose)
    for i, s in enumerate(SEGS):
        d = _unit(dirs[i])
        if inner is not None: inn = inner
        else:
            nb = _sub(dirs[min(i + 1, 2)], dirs[max(i - 1, 0)])
            inn = _sub(nb, tuple(_dot(nb, d) * c for c in d))
            if _dot(inn, inn) < 1e-4: inn = (0.0, -1.0, 0.0) if abs(d[1]) < 0.9 else (0.0, 0.0, -1.0)
        Qw = _aim(SEG_AXIS[s], (0.0, 0.0, -1.0), d, inn)
        par = PARENT[t + s]; Qp = rigkit.solve(PIVOT, PARENT, p)[par][0]
        p[t + s] = qmul(_conj(Qp), Qw)
    return p


def reach(pose, t, target, guide, inner=None, iters=60):
    """tentacle t's chain bent (FABRIK) so its hook's apex comes to target (design units); guide: two points the chain starts
    from (the shape it bends from - an arc up and over, a dip down)"""
    R = _root(pose, t); L = [SEG_LEN[s] for s in SEGS]
    pts = [R]
    for g in list(guide) + [target]:
        pts.append(_add(pts[-1], _unit(_sub(g, pts[-1])), L[len(pts) - 1]))
    for _ in range(iters):
        pts[3] = target
        for i in (2, 1, 0):
            pts[i] = _add(pts[i + 1], _unit(_sub(pts[i], pts[i + 1])), L[i])
        pts[0] = R
        for i in (0, 1, 2):
            pts[i + 1] = _add(pts[i], _unit(_sub(pts[i + 1], pts[i])), L[i])
    return lay(pose, t, [_sub(pts[i + 1], pts[i]) for i in range(3)], inner)


def tip(pose, t):
    return at(pose, TIP[t][0], TIP[t][1])


def P(**kw):
    return kw


TRUNK_HIDE = tuple(p for p in PARTS if p != 'puddle')
OUTD = lambda t, up=0.0, k=1.0: _unit((OUT[t][0] * k, up, OUT[t][2] * k))
DOWN = (0.0, -1.0, 0.0)


def coiled(p, ts, tight=1.0):
    """tentacles drawn in: out a little, then curled down and in against the trunk"""
    for t in ts:
        o = OUT[t]
        p = lay(p, t, curl(_unit((o[0] * 0.8, 0.35, o[2] * 0.8)), _unit((-o[0], -1.0, -o[2])), (80 * tight, 75 * tight)))
    return p


def draped(p, ts, r=26.0, swing=0.0):
    """tentacles fallen limp on the ground round it, r out from the trunk"""
    for t in ts:
        R = _root(p, t); o = _unit(_rod(OUT[t], UP, swing))
        target = (o[0] * r, 1.4, o[2] * r + 0.5)
        mid1 = _add(R, (o[0] * 8, 2.0, o[2] * 8)); mid2 = (o[0] * (r - 9), 2.0, o[2] * (r - 9))
        p = reach(p, t, target, (mid1, mid2))
    return p


def _pose(name):
    sunk = P(_o_mound=(0, -6.0, 0), _o_seg1=(0, -30.0, 0), seg1=T(10), seg2=T(20), seg3=T(10), head=T(20))
    if name == 'dormant':                                     # (the puddle alone; the rest sunk under it, hidden)
        p = coiled(dict(sunk), TENT, 1.1); p['_hide'] = TRUNK_HIDE
    elif name == 'rise_0':                                    # (the mound swelling up out of the puddle; the rest still under)
        p = coiled(dict(sunk, _o_mound=(0, -3.2, 0)), TENT, 1.1); p['_hide'] = tuple(x for x in TRUNK_HIDE if x != 'mound')
    elif name == 'rise_1':                                    # (the trunk half up out of the mound, bowed, its tentacles curled tight)
        p = P(_o_seg1=(0, -15.0, 0), seg1=T(6, 0, 3), seg2=T(10, -6, -2), seg3=T(16, 4), head=T(34), jaw=JAW(4))
        p = coiled(p, TENT, 1.15)
    elif name == 'rise_2':                                    # (fully up, rearing back, its mouth open, its tentacles flaring)
        p = P(seg1=T(-3), seg2=T(-6), seg3=T(-5), head=T(-24), jaw=JAW(38))
        for t in TENT:
            o = OUT[t]; p = lay(p, t, curl(_unit((o[0] * 0.75, 0.75, o[2] * 0.75)), _unit((o[0], -0.9, o[2])), (38, 52)))
    elif name in ('idle_a', 'idle_b'):                        # (swaying, breathing; the tentacles drifting)
        b = name == 'idle_b'; sg = -1 if b else 1
        p = P(seg1=T(3, 0, 4 * sg), seg2=T(4, 5 * sg, -3 * sg), seg3=T(5 if not b else 3, -4 * sg, -3 * sg), head=T(12 if not b else 4, 6 * sg, 5 * sg),
              jaw=JAW(12 if not b else 24))
        bends = {'t1': (28, 42), 't2': (36, 30), 't3': (24, 50), 't4': (42, 34)}
        for i, t in enumerate(TENT):
            o = OUT[t]; up = 0.32 if (i % 2 == 0) != b else 0.12
            sw = (10 if (i % 2 == 0) == b else -10)
            d0 = _rod(_unit((o[0], up, o[2])), UP, sw)
            p = lay(p, t, curl(d0, _unit((o[0], -1.0, o[2])), bends[t] if not b else bends[t][::-1]))
    elif name == 'shriek':                                    # (the head thrown back, the mouth wide, the tentacles spread high)
        p = P(seg1=T(-5), seg2=T(-9), seg3=T(-12), head=T(-42), jaw=JAW(56))
        for t in TENT:
            o = OUT[t]; p = lay(p, t, curl(_unit((o[0] * 0.55, 0.85, o[2] * 0.55)), _unit((o[0], 0.0, o[2])), (24, 34)))
    elif name == 'grab_0':                                    # (t1 shot straight out ~6 blocks ahead at chest height; the others coiled)
        p = P(seg1=T(6), seg2=T(8), seg3=T(8, 8), head=T(10), jaw=JAW(30))
        p = coiled(p, ('t2', 't3', 't4'))
        R = _root(p, 't1'); tg = (1.0, 10.5, -48.0)
        p = reach(p, 't1', tg, (_add(R, _unit(_sub(tg, R)), 17.0), _add(R, _unit(_sub(tg, R)), 33.0)), inner=DOWN)
    elif name == 'grab_1':                                    # (t1 hauling back in, curled round as if dragging something to it)
        p = P(seg1=T(2), seg2=T(-3), seg3=T(-6, 10), head=T(8), jaw=JAW(42))
        p = coiled(p, ('t2', 't3', 't4'))
        p = lay(p, 't1', curl(_unit((0.2, -0.38, -1.0)), (0.0, 1.0, 0.25), (95, 85)))
    elif name == 'stab_0':                                    # (the wind-up: leaning back, t2 and t3 raised high and cocked)
        p = P(seg1=T(-4), seg2=T(-9), seg3=T(-10), head=T(-10), jaw=JAW(22))
        p = coiled(p, ('t1', 't4'))
        for t in ('t2', 't3'):
            o = OUT[t]; p = lay(p, t, curl(_unit((o[0] * 0.3, 1.0, 0.15)), (0.0, -0.2, 1.0), (52, 70)))
    elif name == 'stab_1':                                    # (the strike: lunging, t2 and t3 driven down 4 blocks ahead)
        p = P(seg1=T(9), seg2=T(14), seg3=T(12), head=T(22), jaw=JAW(44))
        p = coiled(p, ('t1', 't4'))
        for t, x in (('t2', -4.5), ('t3', 4.5)):
            R = _root(p, t); tg = (x, 0.4, -32.0)
            p = reach(p, t, tg, (_add(R, (x * 0.4, 12.0, -10.0)), (x * 0.9, 16.0, -24.0)), inner=(0.0, 0.0, 1.0))
    elif name == 'recoil':                                    # (flinching from the light: twisted away, ducking, tentacles pulled in)
        p = P(seg1=T(-6, 10, -6), seg2=T(-12, 18, -8), seg3=T(-8, 14, -6), head=T(16, 26, -10), jaw=JAW(30))
        p = coiled(p, TENT, 1.25)
    elif name == 'sink_0':                                    # (half sunk, bowed; its tentacles limp on the ground)
        p = P(_o_mound=(0, -2.0, 0), _o_seg1=(0, -17.0, 0), seg1=T(6), seg2=T(12, 0, 6), seg3=T(12), head=T(32), jaw=JAW(8))
        p = draped(p, TENT, 24.0, 8.0)
    elif name == 'death_0':                                   # (collapsing: buckling, lolling, its tentacles flopping down)
        p = P(_o_seg1=(0, -3.0, 0), seg1=T(14, 0, 8), seg2=T(22, 10, 10), seg3=T(18, -10, 8), head=T(30, 15, 12), jaw=JAW(36))
        p = draped(p, ('t1', 't3', 't4'), 30.0, -6.0)
        p = lay(p, 't2', curl(_unit((-0.7, 0.4, -0.4)), (-0.3, -1.0, 0.0), (60, 50)))
    elif name == 'death_1':                                   # (a melted heap on the puddle)
        p = P(_o_mound=(0, -3.6, 0), _o_seg1=(0, -11.0, 0), seg1=T(62, 0, 10), seg2=T(30, 30, 24), seg3=T(16, -24, 18), head=T(10, 10, -20), jaw=JAW(50))
        p = draped(p, TENT, 28.0, 14.0)
    else:
        raise KeyError(name)
    return p


POSE_NAMES = ('dormant', 'rise_0', 'rise_1', 'rise_2', 'idle_a', 'idle_b', 'shriek', 'grab_0', 'grab_1', 'stab_0', 'stab_1', 'recoil',
              'sink_0', 'death_0', 'death_1')


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
DRIPS = [('jaw', (-3.4, 26.4, -7.6)), ('jaw', (4.2, 25.8, -6.4)), ('seg1', (-5.0, 5.0, 2.6)), ('seg2', (-4.2, 13.6, -3.6)),
         ('head', (0.0, 28.0, 8.0))]


# ---------------------------------------------------------------------------------------------------- the items
def _icon_kit():
    from sprites280 import S
    return S


GOO = ['#120a0e', '#22111a', '#361a26', '#5a2a3c', '#8c4a60']             # (dark -> light: the lit shades over 40 luminance)
REDS = ['#6a0a18', '#a8142a', '#e0303c', '#ff7a7a', '#ffc8b8']


def _outline(im):
    px = im.load()
    add = [(x, y) for y in range(16) for x in range(16) if px[x, y][3] == 0 and
           any(0 <= x + dx < 16 and 0 <= y + dy < 16 and px[x + dx, y + dy][3] > 0 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for x, y in add: px[x, y] = (18, 14, 14, 255)
    return im


def remnant_raw():
    """a Shadow Remnant: a quivering blob of black shadow-goo, three lumps trembling up off it, a red glint deep inside, a glossy
    highlight top left, and a drip running off it"""
    S = _icon_kit(); s = S()
    s.disc(8.0, 10.2, 5.6, GOO, sq=0.78)                                   # (the body, slumped)
    s.disc(5.2, 6.6, 2.6, GOO); s.disc(9.6, 5.4, 2.8, GOO); s.disc(12.2, 7.8, 2.0, GOO)     # (the lumps, quivering up)
    s.g(['.ab.', 'abcb', 'bcdc', '.cc.'], {'a': REDS[0], 'b': REDS[1], 'c': REDS[2], 'd': REDS[4]}, 7, 9)      # (the glint inside)
    s.px(8, 10, REDS[3])
    s.g(['ff', 'f.'], {'f': '#c08098'}, 4, 5); s.px(8, 3, '#a86880'); s.px(9, 3, '#a86880')                     # (wet highlights)
    s.px(4, 9, GOO[4]); s.px(4, 10, GOO[3])
    for y in (13, 14): s.px(12, y, GOO[2])                                 # (the drip)
    s.px(12, 15, GOO[3]); s.px(13, 15, GOO[2])
    return _outline(s.image())


def musk_raw():
    """Shadow Musk: a stoppered glass vial (round-bellied) of black salve glowing faintly red, a cork, and a curl of dark smoke
    rising from the stopper"""
    S = _icon_kit(); s = S()
    GL = ['#2c3a46', '#4a6274', '#7a98aa', '#bcd8e4', '#eefaff']
    WOOD = ['#3d2614', '#5e3b1f', '#80522c', '#a26d3c', '#c48e58']
    s.disc(7.5, 11.0, 4.6, GL)                                             # (the glass belly)
    for y in range(16):                                                    # (the salve inside: black, a red glow low in it)
        for x in range(16):
            if (x, y) in s.p and math.hypot(x + 0.5 - 7.5, y + 0.5 - 11.0) < 3.7:
                d = math.hypot(x + 0.5 - 7.0, y + 0.5 - 12.4)
                s.px(x, y, REDS[1] if d < 1.2 else '#5a1424' if d < 2.4 else GOO[1] if y > 8 else GOO[2])
    s.px(7, 12, REDS[2]); s.px(6, 12, REDS[2])
    for x in (5, 6, 7, 8, 9): s.px(x, 8, GOO[3] if x < 7 else GOO[2])     # (the salve's surface, oily)
    for y in (5, 6, 7): s.px(6, y, GL[2]); s.px(7, y, GL[1]); s.px(8, y, GL[1])       # (the neck)
    s.g(['abbc', 'abbc'], {'a': WOOD[3], 'b': WOOD[2], 'c': WOOD[1]}, 5, 3)            # (the cork)
    s.px(5, 3, WOOD[4])
    s.px(4, 9, GL[4]); s.px(4, 10, GL[3]); s.px(5, 8, GL[3])               # (a glint on the glass)
    im = _outline(s.image()); px = im.load()
    SM = [(144, 120, 140), (110, 86, 108), (88, 66, 86), (70, 50, 70)]      # (the smoke: laid on after the outline - a thread, no outline)
    for (x, y, c) in ((8, 2, 0), (9, 1, 1), (9, 0, 2), (10, 1, 2), (11, 0, 3), (7, 1, 1), (6, 0, 2)):
        if px[x, y][3] == 0: px[x, y] = SM[c] + (255,)
    return im


ICONS = {'shadow_remnant': None, 'shadow_musk': None}


def icons():
    return {'shadow_remnant': remnant_raw(), 'shadow_musk': musk_raw()}


def icon(name):
    """the icon as the pack ships it"""
    import vanilla
    return vanilla.process(name, icons()[name])


# ---------------------------------------------------------------------------------------------------- sounds
SFX = ('bubble', 'rise', 'idle', 'lash', 'shriek', 'death')
SUBTITLE = {'bubble': 'Shadow bubbles', 'rise': 'Dread Mire rises', 'idle': 'Dread Mire whispers', 'lash': 'Tentacle lashes',
            'shriek': 'Dread Mire shrieks', 'death': 'Dread Mire dissolves'}
RANGE = {'shriek': 40, 'rise': 32, 'death': 32, 'lash': 24, 'idle': 20, 'bubble': 16}
SOUNDS = {n: f'bm:mire.{n}' for n in SFX if os.path.exists(os.path.join(HERE, 'vendor', f'mire_{n}.ogg'))}


# ---------------------------------------------------------------------------------------------------- gen_rp
def rp(R):
    """gen_rp: the mr_ block textures (TEXTURE_MODS) and their animations, every part as a 3D model at display scale (HATS,
    DISPLAY_3D_EXTRA 'mr_'), the two item icons (ICONS), and in a post pass the .mcmeta of the animated textures and the
    sounds (assets/bm/sounds/mire/*.ogg, registered in sounds.json as mire.<name>, with subtitles)"""
    import sys, json, shutil
    R.TEXTURE_MODS.append(sys.modules[__name__])
    for name, (tex, els) in models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (PREFIX,)
    R.ICONS.update(icons())
    R.LANG.update({f'subtitles.bm.mire.{n}': SUBTITLE[n] for n in SOUNDS})

    def post(R2):
        textures()                                                  # (fills ANIMATED)
        for k, meta in ANIMATED.items():
            R2.wj(f'assets/bm/textures/block/{k}.png.mcmeta', meta)
        if not SOUNDS: return
        sj = R2.p('assets', 'bm', 'sounds.json')
        snd = json.load(open(sj)) if os.path.exists(sj) else {}
        os.makedirs(R2.p('assets', 'bm', 'sounds', 'mire'), exist_ok=True)
        for n in SOUNDS:
            shutil.copy(os.path.join(HERE, 'vendor', f'mire_{n}.ogg'), R2.p('assets', 'bm', 'sounds', 'mire', f'{n}.ogg'))
            snd[f'mire.{n}'] = {'subtitle': f'subtitles.bm.mire.{n}', 'sounds': [{'name': f'bm:mire/{n}', 'attenuation_distance': RANGE[n]}]}
        R2.wj('assets/bm/sounds.json', snd)
    R.POST.append(post)

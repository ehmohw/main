"""3.0e: THE BROOD-MIRE (art; phase258 runs it, on mirekit) - the Vorn's alien cousin of the Dread Mire. The hive took a Dread
Mire aboard the Brood-Carrier and "improved" it ("EVERYTHING HERE WAS SOMETHING ELSE, ONCE."): a grotesque tentacle monster in deep
purples and sickly alien greens, bioluminescent green veins, and EYES - clusters of yellow slit-pupilled eyes of every size all
over it, blinking out of step.

THE LOOK. A puddle of purple-green slime, 4 blocks across, green veins pulsing through it and a few yellow eyes open on its surface,
blinking up at you. Risen (~5-6 blocks) it is a heap of swollen sacs, not a worm: a lumpy purple base and three bulging, blistered
body-sacs (green-bellied, green cysts glowing through the skin), stacked up to a great swollen brain-sac of a head - folds across
its crown, three EYESTALKS sprouting from it (each ending in a big yellow eye), and the head's front crowded with eyes round its MAW:
four fleshy lamprey flaps lined in glowing green and rows of pale yellow teeth, an eye on each flap's back; open, three more yellow
eyes stare out of the green throat. FOUR TENTACLES (the Dread Mire's own, same joints and length): purple above, green below, a row of
pale suckers down the inner side, green glow-spots, little eyes along their flanks, and each ends in a bulb with an eye of its own,
three claws round it.

THE RIG. The Dread Mire's rig, exactly (mire_art: PIVOT, PARENT, the same 23 parts, the same pose names) - so phase246's runtime,
the death squash, the grown Mireling's giant (phase252._grown) and every pose built by mire_art's posing kit work unchanged - plus
three eyestalks (es1 es2 es3, children of head). POSES[name] = the Dread Mire's pose, with the eyestalks' sway added and a few poses
of its own: idle_c (a writhe), beam (balled up in a tractor beam: its arrival), spit_0 / spit_1 (rearing, the maw and every eye
aimed - then the spit).
SCALE 2.0 (a design unit is 1/8 block), as the Dread Mire. GLOW: every part (as mire_art). Its textures are its own (bx_*), and the
eyes are animated: eye1 / eye2 / eye3 each blink (and glance aside) on their own timing, so the eyes never all blink together.
The melt's goop and bubbles are recoloured (phase257's dfx_bgoop / bbubble / bpop, drawn here: _goop, _bubble, _pop; bx_goop,
bx_bubble and bx_pop are the previews' own). Its item icons: brood_ichor, hive_scent, brood_pod (icons()). rp(R): gen_rp, through
phase258.rp."""
import math
import random
from PIL import Image

import rigkit
from rigkit import qs, el, seg, D, qrot, qmul
import mire_art as MA

PREFIX = 'bx_'
NAME = 'Brood-Mire'
RIG_SCALE = 2.0
SCALE = RIG_SCALE
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)

# ---------------------------------------------------------------------------------------------------- the rig: the Dread Mire's, + eyestalks
TENT, SEGS, LEN, APEX, ROOT, OUT = MA.TENT, MA.SEGS, MA.LEN, MA.APEX, MA.ROOT, MA.OUT
CY, ZB, MR, ML, MN, MT = MA.CY, MA.ZB, MA.MR, MA.ML, MA.MN, MA.MT
PETAL, MAW = MA.PETAL, MA.MAW
PL = 8.0                                        # (its maw's flaps: stubbier than the Dread Mire's spearhead, ML 14)
PIVOT = dict(MA.PIVOT)
PARENT = dict(MA.PARENT)
STALK = {'es1': (-4.6, 47.4, 3.4), 'es2': (3.8, 47.6, 4.4), 'es3': (-0.4, 47.2, 7.6)}     # (their roots on the crown)
STALK_LEN = {'es1': 9.0, 'es2': 11.0, 'es3': 7.0}
for _s, _p in STALK.items():
    PIVOT[_s] = _p; PARENT[_s] = 'head'
EXTRA = tuple(STALK)
PARTS = tuple(PIVOT)
TPARTS = MA.TPARTS
PART_K = {}
GLOW = PARTS
TIP, MOUTH = MA.TIP, MA.MOUTH


def model_id(part):
    assert part in PIVOT, part
    return PREFIX + part


def model_name(part, pose=None, suffix=''):
    return model_id(part) + (suffix or '')


def scale_of(pose=None):
    return RIG_SCALE


def HIDDEN(p, pose):
    return p in pose.get('_hide', ())


# ---------------------------------------------------------------------------------------------------- the palette
V0, V1, V2, V3, V4, V5, V6 = (20, 8, 30), (46, 16, 66), (76, 28, 108), (108, 42, 146), (144, 66, 180), (182, 108, 210), (218, 164, 236)
G0, G1, G2, G3, G4, G5 = (34, 62, 12), (78, 128, 22), (122, 180, 32), (164, 222, 46), (204, 255, 84), (236, 255, 176)
Y0, Y1, Y2, Y3, Y4 = (110, 64, 0), (196, 132, 6), (250, 196, 30), (255, 230, 100), (255, 250, 210)
KP = (10, 4, 6)
PAL = {'0': V0, '1': V1, '2': V2, '3': V3, '4': V4, '5': V5, '6': V6, 'o': G1, 'O': G2,
       'a': G1, 'b': G2, 'c': G3, 'd': G4, 'e': G5, 'f': (246, 255, 220)}


def _grid(rows, pal=PAL):
    return MA._grid(rows, pal)


def _noise_tex(seed, base, blots, gloss=(), size=16):
    """a mottled skin: base colour, blotches [(colour, count, max radius)], glossy square highlights"""
    rs = random.Random(seed); im = Image.new('RGBA', (size, size), base + (255,)); px = im.load()
    for col, n, rmax in blots:
        for _ in range(n):
            cx, cy, r = rs.randrange(size), rs.randrange(size), rs.uniform(0.8, rmax)
            for y in range(size):
                for x in range(size):
                    dx = min(abs(x - cx), size - abs(x - cx)); dy = min(abs(y - cy), size - abs(y - cy))
                    if dx * dx + dy * dy <= r * r: px[x, y] = col + (255,)
    for (x, y, w, h, col) in gloss:
        for yy in range(y, y + h):
            for xx in range(x, x + w): px[xx % size, yy % size] = col + (255,)
    return im


def _hide():
    return _noise_tex(41, V2, [(V1, 6, 2.2), (V3, 7, 2.2), (G1, 1, 1.0), (V1, 5, 1.0), (V4, 4, 0.9)],
                      [(2, 2, 2, 1, V5), (3, 1, 1, 1, V6), (11, 9, 2, 1, V4), (12, 9, 1, 1, V5), (6, 13, 1, 1, V4)])


def _belly():
    return _noise_tex(43, G2, [(G1, 7, 2.2), (G3, 6, 1.8), (G0, 3, 1.0), (V3, 3, 1.2)], [(3, 3, 2, 1, G5), (10, 11, 1, 1, G4)])


def _cyst():
    """a swollen green cyst glowing through the skin: a hot core, a glossy glint"""
    im = Image.new('RGBA', (16, 16)); px = im.load()
    for y in range(16):
        for x in range(16):
            d = math.hypot(x + 0.5 - 8, y + 0.5 - 8) / 8
            c = G4 if d < 0.45 else G3 if d < 0.8 else G2
            px[x, y] = c + (255,)
    for (x, y) in ((4, 4), (5, 4), (4, 5)): px[x, y] = G5 + (255,)
    return im


def _sucker():
    """a sucker: a pale lilac ring round a dark wet centre"""
    im = Image.new('RGBA', (16, 16), V4 + (255,)); px = im.load()
    for y in range(16):
        for x in range(16):
            d = math.hypot(x + 0.5 - 8, y + 0.5 - 8)
            px[x, y] = (V1 if d < 3.2 else V2 if d < 4.6 else V6 if d < 6.4 else V5) + (255,)
    return im


def _lid():
    return _noise_tex(47, V3, [(V2, 6, 1.6), (V4, 5, 1.4)], [(2, 2, 2, 1, V5)])


def _eye_frame(state, look=0):
    """a yellow alien eye, 16x16: a dark amber rim, gold iris, a paler ring round a black slit pupil, a glint. state: 'open', 'half'
    (the lid down to the middle), 'shut' (a purple lid, a seam of yellow light), 'squint'; look: the pupil shifted (-3..3)"""
    im = Image.new('RGBA', (16, 16)); px = im.load()
    for y in range(16):
        for x in range(16):
            d = math.hypot(x + 0.5 - 8, (y + 0.5 - 8) * 1.08) / 8
            c = V2 if d > 1.06 else Y0 if d > 0.9 else Y1 if d > 0.76 else Y2
            if d < 0.42: c = Y3
            px[x, y] = c + (255,)
    cx = 8 + look
    for y in range(3, 13):
        w = 1 if y in (3, 4, 11, 12) else 2
        for x in range(cx - w, cx + w): px[x, y] = KP + (255,)
    for (x, y) in ((4, 3), (5, 3), (4, 4)): px[x, y] = Y4 + (255,)
    if state in ('half', 'shut', 'squint'):
        rows = {'half': range(0, 7), 'shut': range(0, 16), 'squint': list(range(0, 6)) + list(range(10, 16))}[state]
        for y in rows:
            for x in range(16): px[x, y] = (V3 if y in (min(rows),) else V2 if (x + y) % 5 else V3) + (255,)
        if state == 'half':
            for x in range(16): px[x, 7] = V1 + (255,)
        if state == 'shut':
            for x in range(2, 14): px[x, 8] = Y2 + (255,); px[x, 7] = V1 + (255,)
    return im


EYE_SEQ = {'eye1': [(0, 70), (3, 22), (0, 30), (1, 2), (2, 4), (1, 2), (0, 46), (4, 18)],
           'eye2': [(0, 41), (1, 2), (2, 3), (1, 2), (0, 64), (4, 26), (0, 18), (3, 12)],
           'eye3': [(0, 23), (4, 9), (0, 52), (1, 2), (2, 6), (1, 3), (0, 31), (3, 15), (0, 12), (1, 2), (2, 3), (1, 2)]}
EYE_FRAMES = [('open', 0), ('half', 0), ('shut', 0), ('open', -3), ('open', 3)]


def _strip(frames):
    im = Image.new('RGBA', (16, 16 * len(frames))); [im.paste(f, (0, 16 * i)) for i, f in enumerate(frames)]
    return im


def _vein_frame(k):
    lo, mid, hi = [tuple(round(c * k + d * (1 - k)) for c, d in zip(col, G1)) for col in (G2, G3, G5)]
    im = Image.new('RGBA', (16, 16), mid + (255,)); px = im.load()
    for y in range(16):
        for x in range(16):
            if (x // 4 + y // 4) % 2 == 0 and 1 <= x % 4 <= 2 and 1 <= y % 4 <= 2: px[x, y] = hi + (255,)
            elif x % 8 == 0 or y % 8 == 7: px[x, y] = lo + (255,)
    return im


def _pool_frame(i, n):
    """the puddle's surface: purple slime, green oily pools, a sheen drifting across"""
    base = ['1111111111111111', '11oo111111111111', '1oOo11112111o111', '11o1111222111111', '1111111121111111', '111111111111oo11',
            '11121111111oOo11', '1122211111111o11', '1112111oo1111111', '111111oOOo111111', '1111111oo1111211', '1o11111111112221',
            'oOo1111111111211', '1o11112111111111', '1111122211111oo1', '1111112111111111']
    pal = dict(PAL, **{'1': V2, '2': V1, 'o': G1, 'O': G2})
    im = _grid(base, pal); px = im.load()
    sh = i * 16 // n
    for (x, y, c) in ((0, 3, V4), (1, 3, V5), (2, 3, V5), (3, 3, V4), (1, 2, V4), (2, 2, V6), (4, 10, V4), (5, 10, V5), (6, 10, V4),
                      (5, 9, V4), (9, 6, G3), (10, 6, G3), (10, 5, G4), (11, 13, V4), (12, 13, V5), (13, 13, V4), (12, 12, V4)):
        px[(x + sh) % 16, y] = c + (255,)
    return im


def _ramp(cols, rows=16):
    """a top-to-bottom gradient, the whole of it on every face (teeth, spines, claws)"""
    im = Image.new('RGBA', (16, rows)); px = im.load()
    for y in range(rows):
        c = cols[min(len(cols) - 1, y * len(cols) // rows)]
        for x in range(16):
            cc = tuple(max(0, v - 16) for v in c) if x >= 12 else tuple(min(255, v + 12) for v in c) if x <= 3 else c
            px[x, y] = cc + (255,)
    return im


def _drip():
    pal = dict(PAL, **{'1': G0, '2': G1, '3': G2, '4': G3, '5': G4, '6': G5})
    return _grid(['1111111111111111', '1222222222222211', '1255432222222221', '1256542222222221', '1245432222222221',
                  '1234332222222221', '1233222222222221', '1222222222222221', '1222222222222221', '1222222222222221',
                  '1222222222222221', '1222222222222111', '1122222222221101', '1112222222211001', '1111111111110001',
                  '1111111111100011'], pal)


# ---- the melt (phase257's goop, bubble and pop, recoloured: purple slime, green swirls, green-lit bubbles)
def _goop(i, n=8):
    rs = random.Random(247)
    im = Image.new('RGBA', (16, 16), V1 + (255,)); px = im.load()
    for y in range(16):
        for x in range(16):
            v = math.sin(x * 0.9 + i * 0.6) + math.cos(y * 0.7 - i * 0.4) + math.sin((x + y) * 0.5)
            if v > 1.4: px[x, y] = G2 + (255,)
            elif v > 0.7: px[x, y] = V3 + (255,)
    sx = (i * 2) % 16
    for k in range(5): px[(sx + k) % 16, (3 + k // 2) % 16] = V6 + (255,)
    for (bx, by, ph) in [(rs.randrange(2, 14), rs.randrange(2, 14), rs.randrange(n)) for _ in range(5)]:
        age = (i - ph) % n
        if age < 3:
            r = 1 + age
            for yy in range(by - r, by + r + 1):
                for xx in range(bx - r, bx + r + 1):
                    if 0 <= xx < 16 and 0 <= yy < 16 and (xx - bx) ** 2 + (yy - by) ** 2 <= r * r: px[xx, yy] = G3 + (255,)
            if 0 <= bx - 1 < 16 and 0 <= by - 1 < 16: px[bx - 1, by - 1] = G5 + (255,)
        elif age == 3:
            for (dx, dy) in ((-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (1, -1), (-1, 1)):
                if 0 <= bx + dx < 16 and 0 <= by + dy < 16: px[bx + dx, by + dy] = G4 + (255,)
    return im


def _bubble():
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); px = im.load()
    for y in range(16):
        for x in range(16):
            dd = math.hypot(x + 0.5 - 8, y + 0.5 - 8) / 7.2
            if dd > 1: continue
            c = V3 if dd < 0.78 else G3
            if dd < 0.6: c = V2
            px[x, y] = c + (235 if dd < 0.85 else 255,)
    for (x, y, a) in ((5, 4, 255), (6, 4, 230), (4, 5, 230), (5, 5, 200), (10, 11, 120)): px[x, y] = G5 + (a,)
    return im


def _pop():
    from PIL import ImageDraw
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((1, 1, 14, 14), outline=G3 + (255,), width=2)
    for a in range(0, 360, 45):
        d.point((round(8 + 7 * math.cos(math.radians(a))), round(8 + 7 * math.sin(math.radians(a)))), fill=V5 + (255,))
    return im


ANIMATED = {}


def textures():
    T = {'bx_hide': _hide(), 'bx_belly': _belly(), 'bx_cyst': _cyst(), 'bx_sucker': _sucker(), 'bx_lid': _lid(),
         'bx_rib': _grid(MA.RIB, dict(PAL, o=G1, O=G2)), 'bx_fold': _grid(MA.FOLD, dict(PAL, **{'1': V1, '2': V3, '3': V4, '4': V5, '5': V6})),
         'bx_maw': _grid(MA.MAWT, dict(PAL, a=G2, b=G3, O=V3)), 'bx_ember': _grid(MA.EMBER, dict(PAL, c=G3, d=G4, e=G5)),
         'bx_tooth': _ramp([(150, 156, 96), (178, 184, 118), (204, 208, 146), (226, 228, 176), (240, 240, 206)]),
         'bx_spine': _ramp([V2, V3, V4, G2, G3, G4]), 'bx_claw': _ramp([V1, V2, (190, 170, 120), (226, 214, 170)]),
         'bx_drip': _drip(), 'bx_void': _grid(['0' * 16] * 16, {'0': KP}),
         'bx_goop': _strip([_goop(i) for i in range(8)]), 'bx_bubble': _bubble(), 'bx_pop': _pop()}
    T['bx_glow'] = _strip([_vein_frame(k) for k in (1.0, 0.94, 0.82, 0.68, 0.58, 0.68, 0.82, 0.94)])
    T['bx_pool'] = _strip([_pool_frame(i, 8) for i in range(8)])
    frames = [_eye_frame(s, l) for s, l in EYE_FRAMES]
    for k in EYE_SEQ: T['bx_' + k] = _strip(frames)
    ANIMATED.update({'bx_glow': {'animation': {'frametime': 5, 'interpolate': True}}, 'bx_pool': {'animation': {'frametime': 6, 'interpolate': True}},
                     'bx_goop': {'animation': {'frametime': 4, 'interpolate': True}}})
    for k, seq in EYE_SEQ.items():
        ANIMATED['bx_' + k] = {'animation': {'frames': [{'index': i, 'time': t} for i, t in seq]}}
    return T


def eye_textures(frame):
    """the eyes' textures fixed on one frame (previews: tools/render draws a strip's first frame)"""
    f = _eye_frame(*EYE_FRAMES[frame])
    return {'bx_' + k: f for k in EYE_SEQ}


LIGHT = {'glow': 15, 'cyst': 11, 'maw': 13, 'ember': 15, 'eye1': 15, 'eye2': 15, 'eye3': 15}
FULL = {'tooth', 'spine', 'claw', 'drip', 'sucker', 'cyst', 'eye1', 'eye2', 'eye3'}
F6 = ('north', 'south', 'east', 'west', 'up', 'down')
NORMAL = {'x+': 'east', 'x-': 'west', 'y+': 'up', 'y-': 'down', 'z+': 'south', 'z-': 'north'}

# ---------------------------------------------------------------------------------------------------- building helpers
_rs = random.Random(29)
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
    return [E((cx - rx, y0, cz - rz * k), (cx + rx, y1, cz + rz * k), mat), E((cx - rx * k, y0 + inset, cz - rz), (cx + rx * k, y1 - inset, cz + rz), mat)]


def VEIN(path, axis, at, out, w=0.6, d=0.22, mat='glow'):
    els = []
    lo, hi = (at - 0.08, at + d) if out > 0 else (at - d, at + 0.08)
    for (u0, v0), (u1, v1) in zip(path, path[1:]):
        a0, a1 = sorted((u0, u1)); b0, b1 = sorted((v0, v1))
        a0, a1, b0, b1 = a0 - w / 2, a1 + w / 2, b0 - w / 2, b1 + w / 2
        if axis == 'x': fr, to = (lo, a0, b0), (hi, a1, b1)
        elif axis == 'z': fr, to = (a0, b0, lo), (a1, b1, hi)
        else: fr, to = (a0, lo, b0), (a1, hi, b1)
        els.append(E(fr, to, mat))
    return els


_EYEN = [0]


def EYE(c, s, n, var=None, proud=None):
    """an eye of size s set into a surface: its centre c on the surface plane, n the outward normal ('x+', 'z-', ...): a dark
    socket rim round a ball bulging proud of the skin, the eye's face (an animated, blinking texture) on its outer face. var picks
    the blink timing (eye1/2/3), else they take turns"""
    if var is None: _EYEN[0] += 1; var = 'eye' + '123'[_EYEN[0] % 3]
    ax = 'xyz'.index(n[0]); sg = 1 if n[1] == '+' else -1
    pr = proud if proud is not None else s * 0.42
    lo, hi = [c[i] - s / 2 for i in range(3)], [c[i] + s / 2 for i in range(3)]
    rim_lo, rim_hi = [c[i] - s / 2 - 0.25 for i in range(3)], [c[i] + s / 2 + 0.25 for i in range(3)]
    out_plane = c[ax] + sg * pr
    lo[ax], hi[ax] = sorted((c[ax] - sg * 0.3, out_plane))
    rim_lo[ax], rim_hi[ax] = sorted((c[ax] - sg * 0.3, c[ax] + sg * min(0.3, pr * 0.5)))
    face = NORMAL[n]
    side = tuple(f for f in F6 if f not in (face, NORMAL[n[0] + ('-' if sg > 0 else '+')]))
    els = [E(rim_lo, rim_hi, 'lid', faces=side + (face,)), E(lo, hi, 'lid', faces=side)]
    plo, phi = list(lo), list(hi)
    plo[ax], phi[ax] = sorted((out_plane, out_plane + sg * 0.06))
    els.append(E(plo, phi, var, faces=(face,), uv={face: [0, 0, 16, 16]}))
    return els


def CYST(c, s, n):
    ax = 'xyz'.index(n[0]); sg = 1 if n[1] == '+' else -1
    lo, hi = [c[i] - s / 2 for i in range(3)], [c[i] + s / 2 for i in range(3)]
    lo[ax], hi[ax] = sorted((c[ax] - sg * s * 0.3, c[ax] + sg * s * 0.45))
    return [E(lo, hi, 'cyst')]


def DRIP(x, y, z, ln, w=0.7, ball=1.3):
    return [E((x - w / 2, y - ln, z - w / 2), (x + w / 2, y + 0.2, z + w / 2), 'drip'),
            E((x - ball / 2, y - ln - ball * 0.8, z - ball / 2), (x + ball / 2, y - ln + ball * 0.2, z + ball / 2), 'drip')]


# ---------------------------------------------------------------------------------------------------- the puddle
def _puddle():
    P = []; masks = [MA._mask(L) for L in range(3)]; Y = MA.PUDDLE_Y
    for L in range(3):
        for (i, j, w, h) in MA._rects(masks[L]):
            P.append(E((i * MA.CELL, Y[L], j * MA.CELL), ((i + w) * MA.CELL, Y[L + 1], (j + h) * MA.CELL), 'pool',
                       faces=('north', 'south', 'east', 'west', 'up'), light=MA.PUDDLE_LIGHT[L]))
    rnd = random.Random(31)
    for k in range(10):                                             # (slime flung out round the rim)
        th = 2 * math.pi * k / 10 + rnd.uniform(-0.2, 0.2); r = MA._r(th, 0) + rnd.uniform(1.4, 3.0); s = rnd.choice((1.0, 1.5, 2.0))
        x, z = round(r * math.cos(th) * 2) / 2, round(r * math.sin(th) * 2) / 2
        P.append(E((x - s / 2, MA.LIFT, z - s / 2), (x + s / 2, MA.LIFT + 0.18, z + s / 2), 'pool', faces=('north', 'south', 'east', 'west', 'up'), light=3))
    for (x, z, s) in ((-6.5, 3.5, 1.6), (8.5, 4.5, 1.4), (-3.0, -9.0, 1.0), (2.0, 9.5, 1.0), (-11, 6, 1.2)):     # (green blisters)
        y = Y[MA._layer_at(x, z, masks) + 1]
        P.append(E((x - s / 2, y - 0.1, z - s / 2), (x + s / 2, y + s * 0.5, z + s / 2), 'cyst', faces=('north', 'south', 'east', 'west', 'up')))
    for (x, z, s) in ((4.5, -6.0, 2.2), (-9.5, -3.0, 1.6), (9.5, -1.0, 1.2), (-4.0, 8.0, 1.8), (6.0, 9.5, 1.0), (0.5, -11.5, 1.3), (-12, -7.5, 0.9)):
        y = Y[MA._layer_at(x, z, masks) + 1]                         # (eyes open on its surface, blinking up)
        P += EYE((x, y, z), s, 'y+', proud=0.3)
    for (x, z, th, ln) in ((12, 2, 0.2, 5), (-13, -1, 3.0, 6), (3, 13, 1.6, 4), (-6, -12, 4.3, 5), (10, -9, 5.6, 4)):     # (little tendrils)
        a = (x, 0.64, z); b = (x + ln * math.cos(th), 0.48, z + ln * math.sin(th)); c = (b[0] + 1.6 * math.cos(th + 0.9), 0.48, b[2] + 1.6 * math.sin(th + 0.9))
        P += [SEG(a, b, 0.9, 'spine', up=UP), SEG(b, c, 0.6, 'spine', up=UP)]
    def run(x, z, dirs):
        pts = [(x, z)]
        for (dx, dz, n) in dirs: x += dx * n; z += dz * n; pts.append((x, z))
        return pts
    paths = [run(1, 0, [(1, 0, 4), (0, -1, 2), (1, 0, 5), (0, -1, 3), (1, 0, 3)]), run(0, 1, [(0, 1, 3), (1, 0, 2), (0, 1, 5), (-1, 0, 2), (0, 1, 3)]),
             run(-1, 0, [(-1, 0, 5), (0, 1, 3), (-1, 0, 4), (0, 1, 2)]), run(0, -1, [(0, -1, 4), (-1, 0, 3), (0, -1, 4), (-1, 0, 3), (0, -1, 2)]),
             run(1, 1, [(1, 0, 2), (0, 1, 4), (1, 0, 4), (0, 1, 2), (1, 0, 3)]), run(-1, -1, [(-1, 0, 3), (0, -1, 2), (-1, 0, 4), (0, -1, 3)])]
    for pts in paths:
        for (x0, z0), (x1, z1) in zip(pts, pts[1:]):
            n = int(round(max(abs(x1 - x0), abs(z1 - z0))))
            for k in range(n):
                xa = x0 + (x1 - x0) * k / n; za = z0 + (z1 - z0) * k / n; xb = x0 + (x1 - x0) * (k + 1) / n; zb = z0 + (z1 - z0) * (k + 1) / n
                L = MA._layer_at((xa + xb) / 2, (za + zb) / 2, masks)
                if L < 0: continue
                xa, xb = sorted((xa, xb)); za, zb = sorted((za, zb))
                if xa == xb: xa, xb = xa - 0.5, xb + 0.5
                if za == zb: za, zb = za - 0.5, zb + 0.5
                P.append(E((xa, Y[L + 1] - 0.1, za), (xb, Y[L + 1] + 0.12, zb), 'glow', faces=('north', 'south', 'east', 'west', 'up')))
    return P


# ---------------------------------------------------------------------------------------------------- the body: a heap of swollen sacs
def _sacs(y0, y1, r, cz, seed, n=6, eyes=(), cysts=4, belly=True):
    """a body-sac: a lumpy core, sacs bulging out of it at random round its girth (some green-bellied), green cysts, eyes"""
    rs = random.Random(seed); S = []
    h = y1 - y0
    S += OCT(0, cz, y0 - 1.2, y0 + 1.4, r - 1.6, r - 1.6, 'rib')               # (the pinch into the one below)
    S += OCT(0, cz, y0 + 1.0, y1 - 1.0, r, r * 0.95, 'hide')
    S += OCT(0, cz, y1 - 1.4, y1 + 0.5, r - 1.8, r - 1.9, 'hide')
    if belly: S += [E((-r * 0.5, y0 + 1.6, cz - r - 0.2), (r * 0.5, y0 + h * 0.5, cz - r + 1.0), 'belly')]      # (a green belly low in front)
    for k in range(n):                                                         # (bulging sacs, turned to follow its girth, tilted)
        th = 2 * math.pi * (k + rs.uniform(-0.3, 0.3)) / n; s = rs.uniform(3.4, 5.4); yc = y0 + rs.uniform(0.25, 0.8) * h
        x, z = (r - 0.4) * math.cos(th), cz + (r - 0.4) * math.sin(th); sy = s * rs.uniform(0.85, 1.3)
        rot = ((rs.uniform(-20, 20), -math.degrees(th), rs.uniform(-18, 18)), (x, yc, z))
        S.append(E((x - s / 2, yc - sy / 2, z - s * 0.4), (x + s / 2, yc + sy / 2, z + s * 0.4), 'belly' if k % 3 == 0 else 'hide', rot=rot))
        if k % 3 == 1:
            S.append(E((x - s * 0.22, yc - s * 0.22, z - s * 0.22), (x + s * 0.22, yc + s * 0.22, z + s * 0.22), 'cyst',
                       rot=((0, -math.degrees(th), 0), (x - (s * 0.42) * math.cos(th) * 0, yc, z))))
    for k in range(cysts):
        th = 2 * math.pi * (k + 0.5) / cysts + rs.uniform(-0.3, 0.3); yc = y0 + rs.uniform(0.25, 0.8) * h
        if abs(math.cos(th)) > abs(math.sin(th)): S += CYST(((r) * (1 if math.cos(th) > 0 else -1), yc, cz + rs.uniform(-2, 2)), rs.uniform(1.2, 2.0), 'x+' if math.cos(th) > 0 else 'x-')
        else: S += CYST((rs.uniform(-2, 2), yc, cz + r * (1 if math.sin(th) > 0 else -1) * 0.95), rs.uniform(1.2, 2.0), 'z+' if math.sin(th) > 0 else 'z-')
    for (n_, u, v, s) in eyes:                                                 # (eyes: (normal, across, up, size))
        if n_[0] == 'x': S += EYE(((r + 0.05) * (1 if n_[1] == '+' else -1), y0 + v, cz + u), s, n_)
        else: S += EYE((u, y0 + v, cz + (r * 0.95 + 0.05) * (1 if n_[1] == '+' else -1)), s, n_)
    return S


def _mound():
    M = []
    M += OCT(0, 0, 0.3, 3.0, 11.6, 11.0, 'hide')
    M += OCT(0, 0, 2.8, 6.2, 10.2, 9.8, 'belly', k=0.8)
    M += OCT(0, 0.2, 5.8, 9.4, 9.0, 8.8, 'hide')
    for k, (th, s) in enumerate(((0.3, 4.4), (1.2, 3.4), (2.1, 4.8), (3.0, 3.6), (3.9, 4.6), (4.8, 3.8), (5.6, 4.2))):
        x, z = 10.8 * math.cos(th), 10.2 * math.sin(th)
        M.append(E((x - s / 2, 0.05, z - s / 2), (x + s / 2, 1.8 + 0.5 * (k % 3), z + s / 2), 'belly' if k % 2 else 'hide'))
    for (th, ln) in ((0.7, 6), (1.9, 5), (2.8, 7), (3.7, 5), (4.5, 6), (5.3, 5), (6.0, 7)):   # (stubby tendrils sprawling off it)
        a = (9.5 * math.cos(th), 1.0, 9.0 * math.sin(th)); b = ((9.5 + ln) * math.cos(th + 0.12), 0.6, (9.0 + ln) * math.sin(th + 0.12))
        c = (b[0] + 2.5 * math.cos(th + 1.0), 0.5, b[2] + 2.5 * math.sin(th + 1.0))
        M += [SEG(a, b, 1.5, 'hide', up=UP), SEG(b, c, 0.9, 'spine', up=UP)]
        M.append(E((b[0] - 0.4, 1.2, b[2] - 0.4), (b[0] + 0.4, 1.5, b[2] + 0.4), 'glow'))
    M += CYST((11.6, 1.8, -3.0), 1.8, 'x+') + CYST((-11.6, 1.6, 2.4), 2.0, 'x-') + CYST((1.0, 4.6, -9.8), 1.6, 'z-') + CYST((-2.0, 7.8, 8.8), 1.4, 'z+')
    M += EYE((-4.5, 4.4, -9.85), 2.6, 'z-') + EYE((5.4, 7.6, -8.85), 1.8, 'z-') + EYE((10.25, 4.2, 4.0), 2.2, 'x+') + EYE((-10.25, 4.8, -3.0), 1.6, 'x-')
    M += EYE((-2.0, 3.05, -10.4), 1.3, 'y+') + EYE((-8.5, 6.25, 6.6), 1.2, 'y+') + EYE((3.0, 4.4, 9.85), 1.8, 'z+')
    M += VEIN([(0.3, -2.2), (3.0, -2.2)], 'x', 11.6, 1) + VEIN([(3.0, -2.2), (6.2, -2.2)], 'x', 10.2, 1) + VEIN([(6.2, -2.2), (9.4, -2.2)], 'x', 9.0, 1)
    M += VEIN([(0.3, 1.4), (3.0, 1.4)], 'z', -11.0, -1) + VEIN([(3.0, 0.4), (6.2, 0.4)], 'z', -9.8, -1)
    M += VEIN([(0.3, 2.6), (3.0, 2.6)], 'x', -11.6, -1) + VEIN([(6.2, 1.4), (9.4, 1.4)], 'x', -9.0, -1)
    return M


def _seg1():
    S = _sacs(8.0, 16.6, 9.0, 0.0, 101, n=11, eyes=(('z-', -3.6, 5.2, 4.2), ('x+', -1.0, 3.6, 2.4), ('x-', 2.0, 6.0, 1.8), ('z-', 3.6, 2.4, 1.4), ('z+', 1.0, 4.6, 2.2), ('x+', 3.4, 6.8, 1.1)))
    S += VEIN([(9.4, -1.4), (12.0, -1.4), (12.0, 1.6), (15.4, 1.6)], 'x', 9.0, 1) + VEIN([(9.4, 2.0), (13.0, 2.0), (13.0, -1.6), (15.6, -1.6)], 'x', -9.0, -1)
    S += VEIN([(5.0, 10.0), (5.0, 13.2), (6.2, 13.2), (6.2, 15.6)], 'z', -8.55, -1)
    S += DRIP(7.8, 9.4, -3.0, 2.6) + DRIP(-2.4, 9.4, 8.0, 3.2)
    return S


def _seg2():
    S = _sacs(16.0, 24.6, 8.0, 0.3, 202, n=10, eyes=(('z-', 2.8, 5.0, 2.6), ('z-', -3.8, 2.8, 1.5), ('x-', 0.0, 4.2, 3.6), ('x+', 1.6, 6.0, 1.4), ('z+', -1.0, 4.4, 2.0), ('x+', -2.6, 2.6, 2.0)))
    S += VEIN([(17.4, 0.8), (20.4, 0.8), (20.4, -1.6), (23.6, -1.6)], 'x', 8.0, 1)
    S += DRIP(-7.2, 17.4, -1.6, 2.4)
    return S


def _seg3():
    S = _sacs(24.0, 32.4, 7.2, 0.5, 303, n=8, eyes=(('z-', -1.0, 3.0, 2.2), ('z+', 1.4, 5.0, 2.4), ('z-', 3.4, 5.6, 1.2)), cysts=4)
    for t in TENT:                                                  # (the sockets the tentacles grow from: swollen, green-lipped)
        x, y, z = ROOT[t]; o = OUT[t]
        a = (x - o[0] * 2.4, y, z - o[2] * 2.4); b = (x + o[0] * 0.6, y, z + o[2] * 0.6)
        S.append(SEG(a, b, 5.8, 'hide', up=UP))
        S.append(SEG((x - o[0] * 0.4, y, z - o[2] * 0.4), (x + o[0] * 1.0, y, z + o[2] * 1.0), 6.4, 'belly', up=UP))
    return S


def _head():
    """the brain-sac: swollen, lumpy, its crown folded; the face crowded with eyes round the maw; a big eye on each cheek;
    the throat behind the maw lit green, ringed with teeth"""
    H = []
    H += [E((-8.6, 32.0, ZB), (8.6, 43.0, 9.0), 'hide'), E((-7.4, 31.2, ZB + 0.4), (7.4, 44.4, 10.2), 'hide'),
          E((-9.4, 34.0, -0.4), (9.4, 41.6, 7.4), 'hide')]
    H += [E((-7.2, 43.0, -0.8), (7.2, 46.6, 9.4), 'hide'), E((-5.6, 46.4, 0.4), (5.6, 48.0, 8.2), 'hide')]          # (the swollen crown)
    for (x0, x1, z0, z1, hh) in ((-5.4, -0.8, -0.6, 1.4, 1.0), (0.4, 5.4, -0.2, 1.8, 0.8), (-5.6, -1.4, 2.6, 4.4, 0.9), (-0.2, 5.4, 2.8, 4.6, 1.1),
                                 (-4.8, 0.4, 5.2, 7.0, 1.0), (1.2, 5.4, 5.6, 7.4, 0.8)):
        H.append(E((x0, 47.8, z0), (x1, 48.0 + hh, z1), 'fold'))
    H += [E((-6.0, 28.6, 8.6), (6.0, 35.6, 11.6), 'rib'), E((-4.8, 27.4, 9.6), (4.8, 30.4, 12.0), 'belly')]            # (the hood: sacs down its back)
    H += [E((-10.6, 35.0, 1.0), (-9.0, 40.6, 6.0), 'belly'), E((9.0, 36.0, 0.4), (10.6, 41.2, 5.4), 'belly'),          # (cheek sacs, hanging jowls)
          E((-8.4, 30.6, -0.6), (-5.0, 34.0, 3.4), 'belly'), E((5.0, 30.4, -0.6), (8.4, 33.8, 3.0), 'belly')]
    H += CYST((6.4, 45.0, 7.6), 2.6, 'z+') + CYST((-9.4, 42.0, 6.0), 1.8, 'x-') + CYST((4.0, 48.0, 1.2), 1.8, 'y+') + CYST((-2.8, 33.0, 10.2), 2.0, 'z+')
    H += CYST((9.4, 42.6, 6.4), 1.6, 'x+') + CYST((-6.4, 47.6, 6.8), 1.4, 'y+')
    # the eyes: a crowd on the face round the maw, of every size; a big one on each cheek; a few on the crown and behind
    for (x, y, s) in ((-4.4, 42.4, 4.4), (4.8, 41.8, 3.6), (0.4, 44.8, 2.0), (-6.8, 37.8, 1.8), (6.8, 37.0, 2.2), (2.8, 45.6, 1.4),
                      (-2.2, 45.8, 1.6), (-6.8, 33.8, 1.3), (6.8, 33.0, 1.5), (-1.6, 32.2, 1.2), (2.6, 32.0, 1.0), (-7.6, 41.4, 1.0), (7.8, 40.8, 1.1)):
        H += EYE((x, y, ZB), s, 'z-')
    H += EYE((-10.6, 37.8, 3.5), 4.4, 'x-') + EYE((10.6, 38.6, 2.9), 3.8, 'x+')
    H += EYE((9.4, 34.6, 6.0), 1.4, 'x+') + EYE((-9.4, 42.4, 3.0), 1.3, 'x-') + EYE((-4.6, 48.0, 4.6), 1.2, 'y+') + EYE((1.4, 48.0, 6.2), 1.6, 'y+')
    H += EYE((1.6, 39.0, 10.2), 3.2, 'z+') + EYE((-3.6, 42.0, 9.0), 1.3, 'z+') + EYE((4.4, 36.0, 10.2), 1.1, 'z+')
    H += VEIN([(35.0, -0.4), (35.0, 2.0), (36.4, 2.0), (36.4, 6.6)], 'x', 9.4, 1) + VEIN([(38.2, -0.4), (38.2, 0.8), (40.0, 0.8), (40.0, 6.6)], 'x', -9.4, -1)
    H += VEIN([(-1.6, 33.0), (-1.6, 35.4), (1.6, 35.4), (1.6, 41.0)], 'z', 10.2, 1) + VEIN([(-3.0, 0.2), (-3.0, 4.0), (0.6, 4.0), (0.6, 8.0)], 'y', 48.0, 1)
    # the throat: green-lit, its hot centre; a ring of pale teeth
    H += [E((-3.7, CY - 3.7, ZB - 0.1), (3.7, CY + 3.7, ZB), 'maw'), E((-2.4, CY - 2.2, ZB - 0.18), (2.2, CY + 2.4, ZB - 0.1), 'ember')]
    for k, ln in enumerate((1.4, 0.9, 1.7, 1.1, 1.5, 0.8, 1.8, 1.0, 1.2, 0.9)):
        an = 2 * math.pi * k / 10 + 0.2; x, y = 3.1 * math.cos(an), CY + 3.1 * math.sin(an)
        H.append(E((x - 0.35, y - 0.35, ZB - 0.1 - ln), (x + 0.35, y + 0.35, ZB - 0.1), 'tooth'))
    H += DRIP(-3.0, 31.8, -0.6, 2.6) + DRIP(4.0, 32.0, 1.4, 1.8)
    return H


def _eye():
    """in the throat: not one eye but three, staring out of the green (seen as the flaps open)"""
    return EYE((0.0, CY + 0.2, ZB - 0.6), 2.6, 'z-', 'eye1', proud=0.4) + EYE((-1.9, CY - 1.7, ZB - 0.4), 1.2, 'z-', 'eye2', proud=0.3) + \
        EYE((1.9, CY - 1.4, ZB - 0.4), 1.0, 'z-', 'eye3', proud=0.3)


def _petal(name):
    """one flap of the maw: a fleshy lamprey flap (stepped, a little shorter and broader than the Dread Mire's spearhead), green-lit
    inside with rows of pale teeth, its back purple and blistered with an eye; its point a soft hooked lip"""
    k = PETAL[name]; rnd = random.Random(911 + 13 * k); B = []
    for i in range(MN):
        h = MR * (1 - i / MN) + 0.7; z0 = ZB - i * PL / MN; z1 = z0 - PL / MN; zc = (z0 + z1) / 2; tt = min(MT + 0.2, h); inner = h - tt
        B.append(((-h + 0.06, inner, z1), (h - 0.06, h, z0), 'hide'))
        if inner > 0.4:
            B.append(((-inner + 0.1, inner - 0.12, z1 + 0.02), (inner - 0.1, inner, z0 - 0.02), 'maw'))
            for j in range(3 if inner > 2 else 2):
                x = (-1 + 2 * (j + 0.5) / (3 if inner > 2 else 2)) * (inner - 0.4)
                ln = min(rnd.uniform(0.7, 1.9), 2 * inner - 0.4)
                if ln > 0.4: B.append(((x - 0.3, inner - 0.1 - ln, zc - 0.3), (x + 0.3, inner - 0.1, zc + 0.3), 'tooth'))
        if i in (1, 3) and h > 1.6:
            B.append(((-1.0 + rnd.uniform(-0.5, 0.5), h - 0.1, zc - 0.8), (1.0 + rnd.uniform(-0.5, 0.5), h + 0.6, zc + 0.8), 'cyst'))
    tip = ZB - PL
    B.append(((-0.8, 0.3, tip - 1.6), (0.8, 1.4, tip + 0.2), 'spine'))
    out = []
    for (fr, to, mat) in B:
        corners = [(x, y, z) for x in (fr[0], to[0]) for y in (fr[1], to[1]) for z in (fr[2], to[2])]
        rot = [MA._qt(x, y, k) for (x, y, z) in corners]
        xs = [r[0] for r in rot]; ys = [r[1] for r in rot]
        out.append(E((min(xs), CY + min(ys), fr[2]), (max(xs), CY + max(ys), to[2]), mat))
    # (the eye on its back, facing out from the flap's side of the maw)
    ex, ey = MA._qt(0.0, MR * 0.72 + 1.0, k)
    nrm = {0: 'y+', 1: 'x+', 2: 'y-', 3: 'x-'}[k]
    out += EYE((ex, CY + ey, ZB - PL * 0.3), 1.3 if k % 2 else 1.6, nrm, proud=0.35)
    return out


def _tentacle_seg(t, s):
    """purple above, green below; suckers down the inner side (-z), green glow-spots and the odd eye on its flanks; the tip a bulb
    with an eye, three claws round it"""
    x, y, z = PIVOT[t + s]; T = []
    if s == 'a': knuck, boxes, suck = (5.6, -2.2, 1.6), [(4.8, 1.0, 6.4), (4.4, 6.0, 11.8), (4.0, 11.4, 17.8)], (3.0, 6.0, 9.0, 12.0, 15.0)
    elif s == 'b': knuck, boxes, suck = (4.8, -1.8, 1.2), [(3.8, 0.6, 6.0), (3.4, 5.6, 11.2), (3.0, 10.8, 16.8)], (2.6, 5.4, 8.2, 11.0, 13.8)
    else: knuck, boxes, suck = (3.6, -1.4, 1.0), [(2.8, 0.4, 5.4), (2.4, 5.0, 10.0)], (2.4, 4.8, 7.2, 9.2)
    w, k0, k1 = knuck
    T.append(E((x - w / 2, y + k0, z - w / 2), (x + w / 2, y + k1, z + w / 2), 'hide'))
    for i, (bw, b0, b1) in enumerate(boxes):
        ox = 0.25 if i % 2 else -0.25
        T.append(E((x + ox - bw / 2, y + b0, z - bw / 2 + 0.5), (x + ox + bw / 2, y + b1, z + bw / 2), 'hide'))
        T.append(E((x + ox - bw / 2 + 0.3, y + b0 + 0.2, z - bw / 2), (x + ox + bw / 2 - 0.3, y + b1 - 0.2, z - bw / 2 + 0.6), 'belly'))
    for j, py in enumerate(suck):                                   # (suckers down the inner side, in pairs, shrinking to the tip)
        bw = [b for b in boxes if b[1] <= py <= b[2]][0][0]; sw = min(1.5, bw * 0.38)
        for sx in ((-1, 1) if bw > 3.2 else (0,)):
            cx = x + sx * bw * 0.22
            T.append(E((cx - sw / 2, y + py - sw / 2, z - bw / 2 - 0.3), (cx + sw / 2, y + py + sw / 2, z - bw / 2 + 0.1), 'sucker'))
    for j, py in enumerate(suck[::2]):                              # (glow-spots on its back)
        bw = [b for b in boxes if b[1] <= py <= b[2]][0][0]
        T.append(E((x - 0.5, y + py - 0.5, z + bw / 2 - 0.1), (x + 0.5, y + py + 0.5, z + bw / 2 + 0.18), 'glow'))
    rs = random.Random(hash((t, s)) % 1000)
    if s in ('a', 'b'):                                             # (an eye on a flank)
        py = rs.uniform(5.0, 12.0); bw = [b for b in boxes if b[1] <= py <= b[2]][0][0]; sd = rs.choice((1, -1))
        T += EYE((x + sd * (bw / 2 + 0.1), y + py, z + 0.2), 1.2 if s == 'a' else 0.9, 'x+' if sd > 0 else 'x-')
    if s == 'c':                                                    # (the tip: a bulb with an eye, three claws round it)
        T += [E((x - 1.9, y + 10.0, z - 2.1), (x + 1.9, y + 14.4, z + 1.7), 'hide'), E((x - 1.5, y + 14.4, z - 1.7), (x + 1.5, y + 15.4, z + 1.3), 'belly')]
        T += EYE((x, y + 12.4, z - 2.1), 2.4, 'z-', proud=0.45)
        T += EYE((x, y + 15.4, z - 0.2), 1.3, 'y+', proud=0.3)
        for k3 in range(3):
            an = 2 * math.pi * k3 / 3 + 0.5; ox, oz = math.cos(an), math.sin(an)
            T.append(SEG((x + ox * 1.4, y + 14.6, z + oz * 1.4 - 0.2), (x + ox * 2.6, y + 17.0, z + oz * 2.4 - 1.4), 0.7, 'claw', up=UP))
    return T


def _stalk(name):
    """an eyestalk: a ringed purple-green stalk up its own +y, a big yellow eye at the top, staring forward"""
    x, y, z = PIVOT[name]; L = STALK_LEN[name]; S = []
    S.append(E((x - 1.6, y - 1.0, z - 1.6), (x + 1.6, y + 1.2, z + 1.6), 'hide'))
    S.append(SEG((x, y, z), (x + 0.3, y + L * 0.5, z + 0.3), 1.5, 'belly', up=FRONT, ext=0.2))
    S.append(SEG((x + 0.3, y + L * 0.5, z + 0.3), (x, y + L, z), 1.2, 'belly', up=FRONT, ext=0.2))
    for f in (0.3, 0.62):
        S.append(E((x - 0.95, y + L * f - 0.3, z - 0.95), (x + 0.95, y + L * f + 0.3, z + 0.95), 'rib'))
    b = 3.4 if name == 'es2' else 3.0 if name == 'es1' else 2.6
    S.append(E((x - b / 2, y + L, z - b / 2 + 0.3), (x + b / 2, y + L + b, z + b / 2 + 0.3), 'lid'))
    S += EYE((x, y + L + b / 2, z - b / 2 + 0.3), b * 0.86, 'z-', proud=0.4)
    S.append(E((x - 0.6, y + L + b - 0.1, z - 0.4), (x + 0.6, y + L + b + 0.35, z + 0.8), 'cyst'))
    return S


# ---------------------------------------------------------------------------------------------------- models
_RAW = {}


def _build():
    if _RAW: return _RAW
    _rs.seed(29); _EYEN[0] = 0
    fns = {'puddle': _puddle, 'mound': _mound, 'seg1': _seg1, 'seg2': _seg2, 'seg3': _seg3, 'head': _head, 'eye': _eye}
    fns.update({m: (lambda m=m: _petal(m)) for m in MAW}); fns.update({s: (lambda s=s: _stalk(s)) for s in STALK})
    for p in PARTS:
        _PV[0] = PIVOT[p]
        _RAW[p] = fns[p]() if p in fns else _tentacle_seg(p[:2], p[2])
    return _RAW


def models():
    M = {}
    for part, els in _build().items():
        for e in els:
            for v in e['from'] + e['to']:
                assert -16 <= v <= 32, (part, e['from'], e['to'])
            for fc in e['faces'].values():
                assert all(0.0 <= t <= 16.0 for t in fc['uv']), (part, fc['uv'])
        used = sorted({fc['texture'][1:] for e in els for fc in e['faces'].values()})
        M[model_id(part)] = ({t: f'bm:block/{t}' for t in used}, els)
    M['bx_goop'] = ({'g': 'bm:block/bx_goop'}, _goop_els())
    for k in ('bubble', 'pop'):                                     # (the sprites: phase257's flat billboard quad)
        M['bx_' + k] = ({'t': f'bm:block/bx_{k}'}, [{'from': [0, 0, 8], 'to': [16, 16, 8], 'faces': {'north': {'uv': [0, 0, 16, 16], 'texture': '#t'}, 'south': {'uv': [0, 0, 16, 16], 'texture': '#t'}}}])
    return M


def _goop_els():
    import phase257 as DFX
    return DFX._goop_model()[1]


# ---------------------------------------------------------------------------------------------------- poses: the Dread Mire's, + its own
def ES(a, b, c):
    """the three eyestalks' bends (lean forward +, turn, lean to its left +), degrees"""
    return {'es1': qs(('y', a[1]), ('x', a[0]), ('z', a[2])), 'es2': qs(('y', b[1]), ('x', b[0]), ('z', b[2])), 'es3': qs(('y', c[1]), ('x', c[0]), ('z', c[2]))}


STALKS = {'dormant': ES((60, 0, 0), (60, 0, 0), (60, 0, 0)), 'rise_0': ES((60, 0, 0), (60, 0, 0), (60, 0, 0)),
          'rise_1': ES((40, 10, 20), (30, -10, -25), (50, 0, 0)), 'rise_2': ES((-10, 15, 30), (-15, -10, -30), (-25, 0, 5)),
          'idle_a': ES((10, 20, 22), (-5, -25, -18), (-14, 10, 10)), 'idle_b': ES((-6, -10, 30), (12, 15, -26), (4, -20, -12)),
          'idle_c': ES((24, 30, 10), (-12, 0, -34), (-20, -25, 18)), 'shriek': ES((-30, 20, 40), (-35, -20, -40), (-45, 0, 0)),
          'grab_0': ES((30, -10, 10), (28, -14, -6), (20, -12, 0)), 'grab_1': ES((18, 0, 18), (10, -6, -16), (6, 0, 0)),
          'stab_0': ES((-20, 10, 25), (-25, -10, -25), (-30, 0, 0)), 'stab_1': ES((35, 0, 12), (40, 0, -12), (30, 0, 0)),
          'recoil': ES((-35, 40, 35), (-40, 30, -30), (-50, 20, 10)), 'sink_0': ES((50, 0, 30), (55, 0, -30), (60, 0, 0)),
          'death_0': ES((60, 20, 50), (40, -20, -60), (70, 0, 20)), 'death_1': ES((80, 30, 70), (70, -20, -80), (85, 0, 30)),
          'beam': ES((70, 0, 20), (70, 0, -20), (75, 0, 0)), 'spit_0': ES((-25, 18, 20), (-30, -18, -20), (-35, 0, 0)),
          'spit_1': ES((30, 12, 8), (34, -12, -8), (38, 0, 0))}


def _pose(name):
    if name in MA.POSE_NAMES:
        p = dict(MA.POSES[name])
    elif name == 'idle_c':                                     # (a writhe: the trunk twisting, every tentacle in an S, crossing)
        T = MA.T
        p = MA.P(seg1=T(2, 8, -3), seg2=T(5, -10, 4), seg3=T(4, 12, 2), head=T(8, -14, -5), **MA.MAWOPEN(24))
        for i, t in enumerate(TENT):
            o = OUT[t]; sw = (-24, 30, 20, -28)[i]
            d0 = MA._rod(MA._unit((o[0], 0.5 - 0.25 * (i % 2), o[2])), UP, sw)
            p = MA.lay(p, t, MA.curl(d0, MA._unit((-o[0] * 0.4, -0.5, -o[2] * 0.4 + (0.6 if i % 2 else -0.6))), (55, -48)))
    elif name == 'beam':                                       # (its arrival: balled up tight, hanging in the tractor beam)
        T = MA.T
        p = MA.P(_o_seg1=(0, -9.0, 0), _o_mound=(0, 2.0, 0), seg1=T(8), seg2=T(10, 0, 4), seg3=T(10), head=T(24), **MA.MAWOPEN(8))
        for i, t in enumerate(TENT):                           # (its tentacles dangling limp below it, a little curled, swaying)
            o = OUT[t]; p = MA.lay(p, t, MA.curl(MA._unit((o[0] * 0.55, -0.8, o[2] * 0.55)), MA._unit((-o[0], -0.2, -o[2])), (18 + 8 * i, 26 - 5 * i)))
        p['_hide'] = ('puddle',)
    elif name == 'spit_0':                                     # (rearing, the head thrown back, the maw wide, eyes on you)
        T = MA.T
        p = MA.P(seg1=T(-4), seg2=T(-8), seg3=T(-10), head=T(-24), **MA.MAWOPEN(70))
        for t in TENT:
            o = OUT[t]; p = MA.lay(p, t, MA.curl(MA._unit((o[0] * 0.7, 0.55, o[2] * 0.7 + 0.2)), MA._unit((o[0], -1.0, o[2])), (40, 40)))
    elif name == 'spit_1':                                     # (the spit: lunging forward, the maw at you)
        T = MA.T
        p = MA.P(seg1=T(6), seg2=T(10), seg3=T(10), head=T(18), **MA.MAWOPEN(62))
        for t in TENT:
            o = OUT[t]; p = MA.lay(p, t, MA.curl(MA._unit((o[0] * 0.8, 0.2, o[2] * 0.8 + 0.3)), MA._unit((o[0], -1.0, o[2])), (50, 30)))
    else:
        raise KeyError(name)
    p.update(STALKS.get(name, {}))
    if 'head' in p.get('_hide', ()): p['_hide'] = tuple(p['_hide']) + EXTRA
    return p


POSE_NAMES = MA.POSE_NAMES + ('idle_c', 'beam', 'spit_0', 'spit_1')


class _Lazy(MA._Lazy):
    def _f(self):
        if not dict.__len__(self): dict.update(self, {n: _pose(n) for n in POSE_NAMES})


POSES = _Lazy()
look = MA.look
DUR = {'beam': 10, 'idle_c': 20, 'spit_0': 10, 'spit_1': 4}


def extent(pose, parts=None):
    """(lowest y, highest y, nearest z) - measured as mire_art measures (the shared parts; the stalks add ~1.5 blocks over the head)"""
    return MA.extent(pose, parts)


# ---------------------------------------------------------------------------------------------------- the items (phase258)
ICHOR = ['................',
         '......444.......',
         '....44w5443.....',
         '...4w54333433...',
         '..45433g3333..3.',
         '..4333gG3yy33.3.',
         '.433333gyKKy332.',
         '.43g33333yy3322.',
         '.433G3333g33322.',
         '..33gg333gG3221.',
         '..3333333g33221.',
         '...222223322211.',
         '....222222111...',
         '......1111......',
         '.......G........',
         '......GgG.......']
ICHOR_PAL = {'1': '#140620', '2': '#2e1046', '3': '#4c1c70', '4': '#6e2e98', '5': '#9a58c4', 'w': '#dcb0f0',
             'g': '#8ad024', 'G': '#c8ff50', 'y': '#fac41e', 'K': '#140a04'}
POD = ['................',
       '.......44.......',
       '......4w54......',
       '.....45543......',
       '....4533g33.....',
       '....43yyyy3.....',
       '...43yyKKyy3....',
       '...43gyyyyg3....',
       '...433g3G332....',
       '...3333g3332....',
       '....33G33322....',
       '....3g333322....',
       '.....333221.....',
       '......2221......',
       '.......g........',
       '......gGg.......']


def _paint(rows, pal):
    from sprites280 import hx
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); px = im.load()
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch != '.': px[x, y] = hx(pal[ch])
    return MA._outline(im)


def ichor_raw():
    """Brood Ichor: a quivering glob of purple slime, green veins glowing through it, a yellow eye peering out of it, a green drop
    falling from it"""
    return _paint(ICHOR, ICHOR_PAL)


def pod_raw():
    """a Brood Pod: sixteen ichors grown into a purple pod, green veins pulsing up it, a yellow slit-eye open in its middle"""
    return _paint(POD, ICHOR_PAL)


def scent_raw():
    """Hive Scent: a round-bellied vial of glowing green ichor with purple swirls, a purple cork, a thread of green vapour"""
    S = MA._icon_kit(); s = S()
    GL = ['#2c3a46', '#4a6274', '#7a98aa', '#bcd8e4', '#eefaff']
    CORK = ['#2e1046', '#4c1c70', '#6e2e98', '#9a58c4', '#dcb0f0']
    s.disc(7.5, 11.0, 4.6, GL)
    for y in range(16):
        for x in range(16):
            if (x, y) in s.p and math.hypot(x + 0.5 - 7.5, y + 0.5 - 11.0) < 3.7:
                d = math.hypot(x + 0.5 - 8.0, y + 0.5 - 12.0)
                s.px(x, y, '#c8ff50' if d < 1.3 else '#8ad024' if d < 2.6 else '#4e8a14' if y > 8 else '#6e2e98')
    s.px(6, 12, '#9a58c4'); s.px(9, 11, '#9a58c4')
    for x in (5, 6, 7, 8, 9): s.px(x, 8, '#9a58c4' if x < 7 else '#6e2e98')
    for y in (5, 6, 7): s.px(6, y, GL[2]); s.px(7, y, GL[1]); s.px(8, y, GL[1])
    s.g(['abbc', 'abbc'], {'a': CORK[3], 'b': CORK[2], 'c': CORK[1]}, 5, 3)
    s.px(5, 3, CORK[4])
    s.px(4, 9, GL[4]); s.px(4, 10, GL[3]); s.px(5, 8, GL[3])
    im = MA._outline(s.image()); px = im.load()
    for (x, y, c) in ((6, 1, (200, 255, 120)), (7, 0, (170, 236, 90)), (8, 1, (140, 210, 60)), (9, 0, (120, 190, 50)), (10, 1, (100, 170, 40))):
        if px[x, y][3] == 0: px[x, y] = c + (255,)
    return im


def icons():
    return {'brood_ichor': ichor_raw(), 'hive_scent': scent_raw(), 'brood_pod': pod_raw()}


def icon(name):
    import vanilla
    return vanilla.process(name, icons()[name])


# ---------------------------------------------------------------------------------------------------- gen_rp
FX_ONLY = ('bx_goop', 'bx_bubble', 'bx_pop')                     # (previews only: the shipped goop and sprites are phase257's dfx_b*)


def rp(R):
    """gen_rp: the bx_ textures (TEXTURE_MODS; the eyes, veins and pool animated - their .mcmeta in a post pass), every part as a 3D
    model at display scale (HATS, DISPLAY_3D_EXTRA 'bx_'), the three item icons"""
    import sys
    mod = sys.modules[__name__]

    class _Tex:
        @staticmethod
        def textures():
            return {k: v for k, v in mod.textures().items() if k not in FX_ONLY}
    R.TEXTURE_MODS.append(_Tex)
    for name, (tex, els) in models().items():
        if name in FX_ONLY: continue
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (PREFIX,)
    R.ICONS.update(icons())

    def post(R2):
        textures()
        for k, meta in ANIMATED.items():
            if k not in FX_ONLY: R2.wj(f'assets/bm/textures/block/{k}.png.mcmeta', meta)
    R.POST.append(post)

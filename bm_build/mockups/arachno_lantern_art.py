"""2.65 test model (mockup only): the SCORCHING ARACHNO-LANTERN - a jack-o'-lantern the size of a house, carried high on eight
long black legs, so tall it walks over the trees.

The body is a great ribbed pumpkin (about five blocks across) with a carved face lit from inside - two triangle eyes and two
small spider eyes above them, a jagged grin - flames licking up both cheeks, a fat purple tongue lolling out of the grin, a
curled stem with a leaf on top, and a charred collar underneath where the legs come out. Each leg is three black segments
(femur, tibia, tarsus) on ember-cracked joints: the knees ride about thirteen blocks up, the feet land ten blocks out.

Same rig kit as KillerWatt (phase57_art): one item model per part, its joint at model (8, 8, 8), placed and posed by item
displays. Body, tongue, stem and the two flames are separate parts (the tongue can wag, the flames flicker by scale); each
leg segment is one display aimed from joint to joint. 29 displays.
    python3 mockups/arachno_lantern_art.py <out.png>     renders a preview: the whole beast among oaks and a player, and the face
"""
import math
import os
import random
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from phase57_art import _cloth, _el, hexc, qa, qmul

BODY_S = 2.6                      # the pumpkin: 40 units across -> 6.5 blocks
BODY_Y = 8.2                      # its centre, in blocks above the ground
FLAME_S = 3.0                     # the cheek fires, drawn bigger than the pumpkin's own scale
ORANGE, ORANGE_DK, ORANGE_LT = '#e8761c', '#a8460c', '#f8a848'
GLOW_IN, GLOW_MID, GLOW_OUT, CUT = '#fff4a8', '#ffc030', '#ff7a14', '#4a1804'
PURPLE, PURPLE_DK, PURPLE_LT = '#8a2ac8', '#561488', '#b866f2'
CHITIN, CHITIN_LT, EMBER = '#16111b', '#3a3046', '#ff5a1a'


# ---------------------------------------------------------------------------------------------------- textures
def _skin(seed, grooves=True):
    """pumpkin rind: warm orange, deep vertical grooves with a highlight beside each, a little mottling"""
    rnd = random.Random(seed); im = _cloth(ORANGE, seed, var=0.05); px = im.load()
    if grooves:
        for x in range(64):
            g = x % 16
            k = 0.62 if g in (0, 15) else 0.78 if g in (1, 14) else 1.12 if g in (3, 4) else 1.0
            for y in range(64):
                r, gg, b, a = px[x, y]; px[x, y] = (min(255, int(r * k)), min(255, int(gg * k)), min(255, int(b * k)), 255)
    d = ImageDraw.Draw(im)
    for _ in range(18):
        x, y = rnd.randint(0, 63), rnd.randint(0, 63)
        d.point((x, y), fill=hexc(rnd.choice((ORANGE_DK, ORANGE_LT, '#d0661a'))))
    return im


def _skin_top():
    """the top and bottom: ribs running out from the middle, darker toward the stem"""
    im = _skin(12, grooves=False); d = ImageDraw.Draw(im)
    for k in range(12):
        a = k * math.pi / 6
        d.line((32, 32, 32 + 46 * math.cos(a), 32 + 46 * math.sin(a)), fill=hexc(ORANGE_DK), width=2)
    for r, c in ((10, '#c05a12'), (5, '#8a3a0a')):
        d.ellipse((32 - r, 32 - r, 32 + r, 32 + r), fill=hexc(c))
    return im


def _carve(im, holes, teeth=()):
    """carved holes, lit from inside: a dark cut wall round each edge, then deep orange fading to pale yellow toward the middle
    (the colour follows the distance from the edge, so every shape glows evenly); teeth: rind left standing in a hole"""
    from PIL import ImageFilter
    mask = Image.new('L', im.size, 0); md = ImageDraw.Draw(mask)
    for kind, shape in holes:
        (md.polygon if kind == 'poly' else md.ellipse)(shape, fill=255)
    for box in teeth:
        md.rectangle(box, fill=0)
    layers, m = [], mask
    for _ in range(8):
        layers.append(m); m = m.filter(ImageFilter.MinFilter(3))
    cols = [CUT, '#8a3008', GLOW_OUT, '#ff9a20', GLOW_MID, '#ffd84a', '#ffe878', GLOW_IN]
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            depth = sum(1 for L in layers if L.getpixel((x, y)))
            if depth: px[x, y] = hexc(cols[min(depth, len(cols)) - 1])
    d = ImageDraw.Draw(im)
    for x0, y0, x1, y1 in teeth:                                                              # (the teeth: rind, a lit edge)
        d.line((x0, y1 + 1, x1, y1 + 1), fill=hexc(GLOW_OUT)); d.line((x0, y0, x0, y1), fill=hexc(ORANGE_DK))


def _face():
    """the carved face, 64 x 64 over a 27 x 22 unit plate: big slanting triangle eyes, two small round spider eyes over each,
    a little nose, and a wide jagged grin with two teeth hanging down and one standing up"""
    im = _skin(13, grooves=False)
    holes = []
    for sx in (-1, 1):
        cx = 32 + sx * 15
        holes.append(('poly', [(cx - 12, 30), (cx + 11, 30), (cx + sx * 7, 9)]))              # (slanting in: a scowl)
        for k, ey in ((0, 3), (1, 5)):
            ex = cx + sx * (2 + 6 * k)
            holes.append(('ellipse', (ex - 2, ey - 2, ex + 2, ey + 2)))
    holes.append(('poly', [(27, 39), (37, 39), (32, 31)]))
    holes.append(('poly', [(1, 40), (9, 44), (15, 41), (22, 45), (28, 42), (32, 45), (36, 42), (42, 45), (49, 41), (55, 44), (63, 40),
                           (61, 50), (55, 58), (47, 62), (40, 59), (32, 63), (24, 59), (17, 62), (9, 58), (3, 50)]))
    _carve(im, holes, teeth=((15, 44, 20, 50), (44, 44, 49, 50), (22, 56, 26, 61), (38, 56, 42, 61)))
    d = ImageDraw.Draw(im)
    for x in range(0, 64, 16):                                                                # faint grooves over the rind only
        for y in range(64):
            r, g, b, a = im.getpixel((x, y))
            if (r, g, b) != hexc(CUT)[:3] and g < 150: im.putpixel((x, y), (int(r * 0.8), int(g * 0.8), int(b * 0.8), 255))
    return im


def _flame(seed):
    """fire from the bottom up: a white-yellow root, orange, a red tip; ragged flicker at the sides"""
    rnd = random.Random(seed); im = Image.new('RGBA', (64, 64)); px = im.load()
    stops = [(0.0, '#e0361a'), (0.35, '#ff7a1a'), (0.65, '#ffc838'), (1.0, '#fff8c8')]
    def col(t):
        for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
            if t <= t1:
                a, b = hexc(c0), hexc(c1); f = (t - t0) / (t1 - t0)
                return tuple(int(a[i] + (b[i] - a[i]) * f) for i in range(3))
        return hexc(stops[-1][1])[:3]
    for y in range(64):
        for x in range(64):
            t = y / 63 + rnd.uniform(-0.06, 0.06) - (0.12 if x in (0, 1, 62, 63) else 0)
            px[x, y] = col(max(0, min(1, t))) + (255,)
    return im


def _tongue():
    im = _cloth(PURPLE, 14, var=0.05); d = ImageDraw.Draw(im)
    d.rectangle((29, 0, 34, 63), fill=hexc(PURPLE_DK))
    for x0 in (8, 48):
        d.line((x0, 0, x0, 63), fill=hexc(PURPLE_LT), width=2)
    rnd = random.Random(15)
    for _ in range(40):
        x, y = rnd.randint(0, 63), rnd.randint(0, 63); d.point((x, y), fill=hexc(PURPLE_LT))
    return im


def _stem():
    im = _cloth('#5e7a2c', 16, var=0.06); d = ImageDraw.Draw(im)
    for x in range(0, 64, 6):
        d.line((x, 0, x + 2, 63), fill=hexc('#3c5418'), width=2)
    for x in range(3, 64, 12):
        d.line((x, 0, x, 63), fill=hexc('#86a246'))
    return im


def _leaf():
    im = _cloth('#3e9a30', 17, var=0.05); d = ImageDraw.Draw(im)
    d.line((32, 0, 32, 63), fill=hexc('#2a6a20'), width=2)
    for y in range(6, 60, 10):
        d.line((32, y, 6, y - 8), fill=hexc('#2a6a20')); d.line((32, y, 58, y - 8), fill=hexc('#2a6a20'))
    return im


def _chitin(seed):
    """black chitin: a faint violet sheen running along it, glints, and bristles"""
    rnd = random.Random(seed); im = _cloth(CHITIN, seed, var=0.05); d = ImageDraw.Draw(im)
    for x in (14, 15, 40):
        d.line((x, 0, x, 63), fill=hexc('#241c2e'))
    for _ in range(30):
        x, y = rnd.randint(0, 63), rnd.randint(0, 63); d.line((x, y, x + 1, y - 2), fill=hexc(CHITIN_LT))
    return im


def _joint():
    """the knuckles: charred black, split by glowing ember cracks"""
    im = _cloth('#1c1010', 18, var=0.05); d = ImageDraw.Draw(im)
    rnd = random.Random(19)
    for _ in range(7):
        x, y = rnd.randint(0, 63), rnd.randint(0, 63); pts = [(x, y)]
        for _k in range(5):
            x += rnd.randint(-8, 8); y += rnd.randint(-8, 8); pts.append((x, y))
        d.line(pts, fill=hexc('#9a2a0a'), width=3); d.line(pts, fill=hexc(EMBER), width=1)
    return im


def _collar():
    im = _cloth('#2a1810', 20, var=0.06); d = ImageDraw.Draw(im)
    rnd = random.Random(21)
    for _ in range(26):
        x, y = rnd.randint(0, 63), rnd.randint(0, 63); d.point((x, y), fill=hexc(rnd.choice((EMBER, '#c04010', '#4a2a1a'))))
    return im


def textures():
    return {'sal_skin': _skin(11), 'sal_top': _skin_top(), 'sal_face': _face(), 'sal_flame': _flame(22), 'sal_tongue': _tongue(),
            'sal_stem': _stem(), 'sal_leaf': _leaf(), 'sal_leg': _chitin(23), 'sal_joint': _joint(), 'sal_collar': _collar()}


# ---------------------------------------------------------------------------------------------------- models
O = (0, 0, 0)


def _box(fr, to, tex, rot=None, uv=None, tex_y=None):
    """an element around the joint (design units = model units - 8); tex_y: a different texture for the top/bottom faces"""
    e = _el(fr, to, tex, O, rot, uv)
    if tex_y:
        for f in ('up', 'down'): e['faces'][f]['texture'] = '#' + tex_y
    return e


def _band(e, v0, v1):
    """map every face of an element onto rows v0..v1 (of 16) of its texture"""
    for f in e['faces'].values():
        u1, _a, u2, _b = f['uv']; f['uv'] = [u1, round(v0, 3), u2, round(v1, 3)]
    return e


def body():
    """the pumpkin: eight slices, each a rough octagon (a cross and a diamond), widest at the middle, flattened top and bottom;
    the face plate on the front (-z) in three bands that follow the curve"""
    els = []
    R, H = 20.0, 17.0
    rf = lambda yc: R * max(0.0, 1 - abs(yc / (H + 0.5)) ** 2.6) ** 0.5
    for y0 in range(-16, 16, 4):
        yc = y0 + 2; r = rf(yc)
        els.append(_box((-r, y0, -0.62 * r), (r, y0 + 4, 0.62 * r), 'sal_skin', tex_y='sal_top'))
        els.append(_box((-0.7 * r, y0, -r), (0.7 * r, y0 + 4, r), 'sal_skin', tex_y='sal_top'))
        q = 0.7 * r
        els.append(_box((-q, y0, -q), (q, y0 + 4, q), 'sal_skin', ('y', 45, (0, yc, 0)), tex_y='sal_top'))
    for (y0, y1), (v0, v1) in (((4, 11), (0, 5.1)), ((-4, 4), (5.1, 10.9)), ((-11, -4), (10.9, 16))):  # (three bands down the curve)
        r = max(rf(l + 2) for l in range(-16, 16, 4) if l < y1 and l + 4 > y0)           # (in front of every slice it crosses)
        e = _box((-13.5, y0, -r - 0.45), (13.5, y1, -r + 0.6), 'sal_skin', uv={'north': [0, v0, 16, v1]})
        e['faces']['north']['texture'] = '#sal_face'
        els.append(e)
    return els


def tongue():
    """from the grin's lower lip: out, down, and curling back up at the tip (joint = where it leaves the mouth)"""
    return [_box((-2.4, -1.6, -3.5), (2.4, 1.0, 0.5), 'sal_tongue'),
            _box((-2.7, -6.0, -6.2), (2.7, -1.4, -2.6), 'sal_tongue', ('x', 22.5, (0, -3.7, -4.4))),
            _box((-2.4, -10.0, -8.0), (2.4, -5.6, -4.8), 'sal_tongue', ('x', 22.5, (0, -7.8, -6.4))),
            _box((-2.1, -12.4, -8.1), (2.1, -9.6, -5.3), 'sal_tongue', ('x', -22.5, (0, -11, -6.7))),
            _box((-1.6, -12.6, -6.0), (1.6, -10.6, -3.6), 'sal_tongue', ('x', -45, (0, -11.6, -4.8)))]


def flame(sx):
    """a cheek fire: three wavering tongues rising beside the grin and up past the eye, leaning a little outward;
    yellow at the root, red at the tips (sx: which cheek)"""
    out = []
    for dx, dz, h, sway in ((0.0, 0.0, 18.0, 1.0), (3.4 * sx, 1.2, 13.0, -1.0), (-2.6 * sx, 0.8, 11.0, 1.0)):
        n = 5
        for k in range(n):
            y0, y1 = h * k / n, h * (k + 1) / n + 0.4
            w = 2.6 * (1 - k / (n + 0.6)) + 0.3
            x = dx + sx * 0.5 * k + sway * (0.9 if k % 2 else -0.6) * (k > 0)
            out.append(_band(_box((x - w, y0, dz - w * 0.6), (x + w, y1, dz + w * 0.6), 'sal_flame'), 16 * (1 - (k + 1) / n), 16 * (1 - k / n)))
    return out


def stem():
    """thick and ribbed, bending over and curling at the end; a broad leaf and a corkscrew vine at its foot"""
    els = [_box((-3, 0, -3), (3, 5, 3), 'sal_stem'), _box((-2.6, 4.5, -2.2), (2.6, 9, 3.0), 'sal_stem', ('x', 22.5, (0, 4.5, 0))),
           _box((-2.2, 8, 0.5), (2.2, 11.5, 6.0), 'sal_stem', ('x', 45, (0, 8, 1.5))), _box((-1.8, 7.5, 5.0), (1.8, 10.5, 8.5), 'sal_stem'),
           _box((-1.5, 6.0, 7.2), (1.5, 8.5, 9.4), 'sal_stem')]
    els.append(_box((2.5, 0.4, -5), (12, 1.0, 4), 'sal_leaf', ('z', -22.5, (2.5, 0.7, 0))))
    for k in range(5):                                                                               # the vine: a little corkscrew
        a = k * 1.3; x, z = -4 - 2.2 * math.cos(a), 2.2 * math.sin(a)
        els.append(_box((x - 0.5, 1 + k * 1.6, z - 0.5), (x + 0.5, 2.4 + k * 1.6, z + 0.5), 'sal_stem'))
    return els


def collar():
    """the charred ring under the pumpkin the legs come out of (8 sockets)"""
    els = [_box((-14, -3, -6), (14, 3, 6), 'sal_collar'), _box((-6, -3, -14), (6, 3, 14), 'sal_collar'),
           _box((-9.5, -3, -9.5), (9.5, 3, 9.5), 'sal_collar', ('y', 45, (0, 0, 0))), _box((-8, -6, -8), (8, -3, 8), 'sal_collar')]
    return els


SEG_LEN = 24.0                     # every leg segment is modelled 24 units long, joint at its root, along +y; scaled to fit


def segment(w0, w1, knob, tip=False, spikes=()):
    """a leg segment: a knob at the joint, a tapering shaft (w0 -> w1 units thick), bristles/spikes; tip: ends in a point"""
    els = [_box((-knob, -knob * 0.7, -knob), (knob, knob * 0.9, knob), 'sal_joint')]
    n = 4
    for k in range(n):
        y0, y1 = SEG_LEN * k / n, min(SEG_LEN, SEG_LEN * (k + 1) / n + 0.3)
        w = (w0 + (w1 - w0) * (k + 0.5) / n) / 2
        if tip and k == n - 1:
            els += [_box((-w, y0, -w), (w, y0 + 3.5, w), 'sal_leg'), _box((-w * 0.55, y0 + 3.4, -w * 0.55), (w * 0.55, SEG_LEN - 0.4, w * 0.55), 'sal_leg')]
        else:
            els.append(_box((-w, y0, -w), (w, y1, w), 'sal_leg'))
    for y, side in spikes:                                                                            # bristles, raked back
        w = (w0 + (w1 - w0) * y / SEG_LEN) / 2
        lo, hi = sorted((side * w, side * (w + 1.5)))
        els.append(_box((lo, y, -0.3), (hi, y + 0.6, 0.3), 'sal_leg', ('z', 22.5 * side, (side * w, y, 0))))
    return els


def models():
    M = {}
    TX = {k: f'bm:block/{k}' for k in textures()}
    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({k: TX[k] for k in used}, els)
    part('sal_body', body()); part('sal_tongue', tongue()); part('sal_flame_r', flame(1)); part('sal_flame_l', flame(-1))
    part('sal_stem', stem()); part('sal_collar', collar())
    part('sal_femur', segment(1.9, 1.45, 1.2, spikes=((8, 1), (14, -1), (19, 1))))
    part('sal_tibia', segment(1.75, 1.2, 1.4, spikes=((6, -1), (11, 1), (16, -1), (20, 1))))
    part('sal_tarsus', segment(1.5, 0.45, 1.15, tip=True, spikes=((7, 1), (13, -1))))
    return M


# ---------------------------------------------------------------------------------------------------- the stance (world blocks)
LEGS = [  # yaw from his front (+z), hip / knee / ankle / foot (radius, height)
    (46, (2.9, 6.3), (7.9, 13.9), (11.2, 6.4), (12.8, 0)), (80, (3.0, 6.1), (8.2, 14.8), (11.0, 6.6), (12.4, 0)),
    (113, (3.0, 6.1), (8.0, 14.6), (10.8, 6.4), (12.2, 0)), (146, (2.9, 6.3), (7.6, 13.6), (10.6, 6.0), (12.4, 0))]


def q_aim(d, twist):
    """the rotation that turns +y to direction d (after a twist about y)"""
    n = math.sqrt(sum(c * c for c in d)); dx, dy, dz = (c / n for c in d)
    ax, az = dz, -dx; s = math.hypot(ax, az)
    ang = math.acos(max(-1.0, min(1.0, dy)))
    tilt = (0.0, 0.0, 0.0, 1.0) if s < 1e-9 else (ax / s * math.sin(ang / 2), 0.0, az / s * math.sin(ang / 2), math.cos(ang / 2))
    return qmul(tilt, qa('y', twist))


def place(scene):
    """every part, posed in the standing stance"""
    U = BODY_S / 16
    at = lambda x, y, z: (-x * U, BODY_Y + y * U, -z * U)                         # design (body units) -> world, his front +z
    scene.display('bm:item/sal_body', pos=at(0, 0, 0), scale=BODY_S)
    scene.display('bm:item/sal_collar', pos=at(0, -17.0, 0), scale=BODY_S * 0.9)
    scene.display('bm:item/sal_stem', pos=at(0, 15.5, 0), scale=BODY_S)
    scene.display('bm:item/sal_tongue', pos=at(0, -9.4, -19.0), scale=BODY_S)
    for sx in (1, -1):
        scene.display(f'bm:item/sal_flame_{"r" if sx > 0 else "l"}', pos=at(16.0 * sx, -8.0, -14.6), scale=FLAME_S)
    for side in (1, -1):
        for yaw, hip, knee, ankle, foot in LEGS:
            a = math.radians(yaw * side)
            P = lambda rh: (math.sin(a) * rh[0], rh[1], math.cos(a) * rh[0])
            pts = [P(hip), P(knee), P(ankle), P(foot)]
            for (A, B), name in zip(zip(pts, pts[1:]), ('sal_femur', 'sal_tibia', 'sal_tarsus')):
                d = tuple(b - a_ for a_, b in zip(A, B)); L = math.sqrt(sum(c * c for c in d))
                scene.display(f'bm:item/{name}', pos=A, scale=L * 16 / SEG_LEN, left=q_aim(d, yaw * side))


def trees(scene):
    """oaks for scale (the tallest about seven blocks), a birch, and the meadow"""
    scene.solid((-17, -0.25, -17), (17, 0, 17), '#6aa84f')
    for (x, z, h) in ((-7.5, 7.5, 6), (8.5, -6.5, 7), (-10.5, -8.5, 5), (13.5, 8.0, 6), (-14.0, 1.0, 7)):
        scene.solid((x - 0.5, 0, z - 0.5), (x + 0.5, h - 1, z + 0.5), '#6b4a2a')
        scene.solid((x - 2.5, h - 3, z - 2.5), (x + 2.5, h - 1, z + 2.5), '#3f8a2e')
        scene.solid((x - 1.5, h - 1, z - 1.5), (x + 1.5, h + 0.6, z + 1.5), '#357a26')
    scene.solid((3.5, 0, 9.0), (4.3, 6, 9.8), '#e8e4d8')                                          # a birch
    scene.solid((1.8, 4, 7.3), (6.0, 6.6, 11.5), '#6aa83a'); scene.solid((2.8, 6.6, 8.3), (5.0, 7.6, 10.5), '#5c9a30')


def write_preview_pack(root):
    import json
    os.makedirs(f'{root}/assets/bm/models/item', exist_ok=True); os.makedirs(f'{root}/assets/bm/textures/block', exist_ok=True)
    for k, im in textures().items(): im.save(f'{root}/assets/bm/textures/block/{k}.png')
    for name, (tex, els) in models().items():
        t = dict(tex); t['particle'] = next(iter(tex.values()))
        json.dump({'textures': t, 'elements': els, 'display': {'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]}}},
                  open(f'{root}/assets/bm/models/item/{name}.json', 'w'))


def check_bounds():
    """every element inside a model's -16..32 box"""
    bad = []
    for name, (_t, els) in models().items():
        for e in els:
            for c in e['from'] + e['to']:
                if not -16 <= c <= 32: bad.append((name, c))
    return bad


def render(out):
    from tools.render import Scene
    root = os.path.join(os.path.dirname(os.path.abspath(out)), 'sal_rp'); write_preview_pack(root)
    tiles = []
    for view, span, center, label, scenery in (((24, 8), 32, (0, 7.6, 0), 'among the oaks (red box: a player)', True),
                                               ('front', 30, (0, 7.6, 0), 'front', True), ('side', 30, (0, 7.6, 0), 'side', True),
                                               ((10, 3), 10.5, (0, BODY_Y - 0.8, 2.0), 'the face', False)):
        s = Scene(rp=root)
        if scenery: trees(s)
        place(s)
        s.player_box((3.2, 0, 6.5))
        im = s.render(view, size=620, span=span, center=center)
        ImageDraw.Draw(im).text((10, 10), label, fill=(0, 0, 0)); tiles.append(im)
    W, H = tiles[0].size
    sheet = Image.new('RGB', (W * 2, H * 2), 'white')
    for i, t in enumerate(tiles): sheet.paste(t, ((i % 2) * W, (i // 2) * H))
    sheet.save(out)


if __name__ == '__main__':
    print('out of bounds:', check_bounds() or 'none')
    render(sys.argv[1])

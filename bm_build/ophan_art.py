"""2.99a draft: THE OPHANIM - the Lightbringer's "Biblically accurate" form, for her powerful charged attack. "Their appearance and
their work was as it were a wheel in the middle of a wheel ... and their rings were full of eyes round about them four"
(Ezekiel 1:16-18). She becomes a giant floating construct of gold and light, ~5.8 blocks across at SCALE.

THE LOOK (the Seraph's holy style, seraph_art: square pixel eyes in gold lids, square tongues of fire, flat fields, no speckle)
  ring_a  the great outer wheel: a thick gold annulus (16 straight segments), its two flat faces set all round with EYES (16 a
          face), eight more eyes round its rim, and between them eight tongues of white-gold fire licking out off the rim. A
          royal blue line runs round its inner edge, a royal purple line round the middle of its rim.
  ring_b  the wheel within it, at right angles: a narrower gold annulus (12 segments), 12 eyes a face and 12 round its rim. No
          fire (there's no room between it and ring_a when both spin).
  ring_c  the innermost: a ring of white-gold LIGHT (10 segments), five eyes a face.
  core    the blazing heart: a white star (two crossed cubes of light) in a translucent gold glow, rays of light out along the
          six axes and the eight diagonals, and HER HALO (the Lightbringer's gold ring) tilted round it.
  The eye: white, a square royal-blue iris lit at its top left, gold lids (light at the top, dark below) - one box each.
  The eyes on a face look out from the wheel like a mandala: the bright upper lid on the outer side all the way round.

PARTS AND AXES (each its own item_display; every model is centred on (8, 8, 8), the display's origin, so a left_rotation turns
it in place - all four displays stand at the same point, the construct's centre)
  ring_a  rests in the XY plane (it faces the front, z): SPIN IT ABOUT Y (vertical) - it tumbles like a coin spun on a table
  ring_b  rests in the XZ plane (lying flat): SPIN IT ABOUT X (horizontal) - it tumbles over the other way
  ring_c  rests in the YZ plane (side-on): SPIN IT ABOUT Z
  core    a sphere-ish star: turn it slowly about Y (or not at all)
  The rings are NESTED so they never touch whatever their angles: each part fits in a ball, inside the hole of the next one out
  (check(): ring_c's ball 10.2 < ring_b's hole 11.2; ring_b's 15.1 < ring_a's 15.6; the core's 7.0 < ring_c's 7.2 (design units)).
  So the runtime may spin every part about ANY axis at any speed; the axes above are what reads best (three gyroscope rings).
  Recommended: ring_a +6 deg/tick about Y, ring_b -9 about X, ring_c +14 about Z, core +2 about Y; the whole construct may lean.

SCALE   2.2: a design unit is 2.2/16 block. ring_a is 40 units across its gold (5.5 blocks), 46.6 to its flames' tips (6.4);
        ring_b 30 (4.1 blocks), ring_c 20 (2.75), the core's star 14 (1.9). Every element is inside the model box (-16..32).
GLOW    light_emission 15 on every eye, every flame, the core (its star, rays, glow and halo) and ring_c's band of light. The gold
        of ring_a / ring_b is unlit (0): in the dark the eyes and the fire carry it. GLOW = the parts worth a brightness
        override (block 15, sky 15) for a being of light - all four; set GLOW = () to let light_emission alone show.
TEXTURES (32 x 32, drawn on coarse grids and blown up, as the Seraph's): oph_band (a wheel's face: u across the band, outer
        edge at u 0), oph_rim, oph_rim_in, oph_eye, oph_flame, oph_lightband, oph_light, oph_ray, oph_halo, oph_aura (translucent)."""
import math
from PIL import Image

import rigkit
from rigkit import el

PREFIX = 'oph_'
PARTS = ('ring_a', 'ring_b', 'ring_c', 'core')
SCALE = 2.2
SPIN_AXIS = {'ring_a': 'y', 'ring_b': 'x', 'ring_c': 'z', 'core': 'y'}
SPIN_RATE = {'ring_a': 6.0, 'ring_b': -9.0, 'ring_c': 14.0, 'core': 2.0}         # (deg / tick, a suggestion)
GLOW = PARTS                                                                    # (brightness 15 on these, if the runtime wants it)
LIGHT = 15                                                                      # (light_emission of the eyes, flames, core)


def model_id(part):
    """the model's id without the namespace (bm:item/<id>)"""
    assert part in PARTS, part
    return PREFIX + part


def model_name(part, pose=None, suffix=''):
    return model_id(part) + (suffix or '')


# ---------------------------------------------------------------------------------------------------- the palette (the Seraph's)
WHITE = (255, 255, 255)
G0, G1, G2, G3, G4 = (255, 246, 196), (252, 214, 96), (228, 172, 50), (172, 114, 28), (110, 66, 18)        # gold
S0, S1, S2, S3 = (176, 218, 255), (82, 142, 242), (58, 90, 216), (32, 48, 126)                          # royal blue
U1, U2 = (106, 60, 192), (62, 30, 122)                                                                  # royal purple
EYE_W, PUPIL = (250, 250, 255), (14, 16, 44)
F0, F1, F2 = (255, 250, 222), (255, 226, 120), (255, 184, 64)                                           # holy fire
PAL = {'W': WHITE, 'y': G0, 'g': G1, 'G': G2, 'h': G3, 'H': G4, 'b': S0, 'B': S1, 'n': S2, 'N': S3, 'u': U1, 'U': U2,
       'e': EYE_W, 'k': PUPIL, 'f': F0, 'F': F1, 'r': F2}


def _grid(rows, size=32, alpha=255):
    """a texture drawn on a coarse grid (PAL letters, '.' clear), blown up NEAREST"""
    im = Image.new('RGBA', (len(rows[0]), len(rows)), (0, 0, 0, 0)); px = im.load()
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != '.': px[x, y] = PAL[ch] + (alpha,)
    return im.resize((size, size), Image.NEAREST)


def _T(rows):
    """rows drawn as seen (across, then down) -> stored transposed (a face's u runs down the drawing)"""
    return [''.join(r[i] for r in rows) for i in range(len(rows[0]))]


# a wheel's face: u across the band (u 0 the outer edge), v along it. Drawn as seen with the outer edge at the TOP:
BAND = ['yyyyyyyy',        # the outer lip, lit
        'gggggggg',
        'GGGGGGGG',
        'GGGGGGGG',
        'GGGGGGGG',
        'hhhhhhhh',
        'nnnnnnnn',        # a royal blue line round the inner edge
        'HHHHHHHH']
RIM = ['yyyyyyyy',         # the outer rim (u along it, v across its depth): lit edges, a royal purple line round its middle
       'gggggggg',
       'GGGGGGGG',
       'uuuuuuuu',
       'GGGGGGGG',
       'hhhhhhhh']
RIM_IN = ['GGGGGGGG', 'hhhhhhhh', 'hhhhhhhh', 'HHHHHHHH']
LIGHTBAND = ['gggggggg',   # ring_c: a band of light, gold-edged
             'yyyyyyyy',
             'WWWWWWWW',
             'WWWWWWWW',
             'yyyyyyyy',
             'gggggggg']
EYE = ['yyyyyy',           # the eye as seen (the upper lid on top): the Seraph's, a royal-blue iris
       'geBneh',
       'genNeh',
       'hhhhhH']
FLAME = ['gggggg',         # a tongue of holy fire, root (top) to tips: gold into white-gold, two square tongues, cut out
         'FFFFFF',
         'FfFFfF',
         'rffrff',
         'rWfrWf',
         'rWf.Wf',
         '.Wf.W.',
         '.W....']


def textures():
    return {'oph_band': _grid(_T(BAND)),
            'oph_rim': _grid(RIM),
            'oph_rim_in': _grid(RIM_IN),
            'oph_lightband': _grid(_T(LIGHTBAND)),
            'oph_eye': _grid(_T(EYE)),
            'oph_flame': _grid(FLAME),
            'oph_light': _grid(['Wyy', 'WWy', 'WWW']),
            'oph_ray': _grid(['yWy']),
            'oph_halo': _grid(['yyyy', 'gggg', 'gggg', 'GGGG']),
            'oph_aura': _grid(['ffff', 'fWWf', 'fWWf', 'ffff'], alpha=96)}


# ---------------------------------------------------------------------------------------------------- building (design units,
# the construct's centre at the origin -> model (8, 8, 8))
PV = (0.0, 0.0, 0.0)


def _sub(a, b): return tuple(a[i] - b[i] for i in range(3))
def _add(a, b): return tuple(a[i] + b[i] for i in range(3))
def _mul(a, k): return tuple(v * k for v in a)


def SEG(A, B, w, h, tex, up, ext=0.0, light=0, shade=True, uv=None):
    """a box w across by h (toward `up`) from A to B: its 'up' face the broad one (u across it, v from A to B)"""
    x, y, z = rigkit.frame(_sub(B, A), up)
    L = math.sqrt(sum(v * v for v in _sub(B, A))) / 2 + ext; m = _mul(_add(A, B), 0.5)
    ang = rigkit.euler([[x[0], y[0], z[0]], [x[1], y[1], z[1]], [x[2], y[2], z[2]]])
    fr, to = (m[0] - w / 2, m[1] - h / 2, m[2] - L), (m[0] + w / 2, m[1] + h / 2, m[2] + L)
    e = el(fr, to, tex, PV, light=light, uv=uv, rot=None if max(abs(v) for v in ang) < 1e-3 else (ang, m))
    if not shade: e['shade'] = False
    return e


WHOLE = {f: [0, 0, 16, 16] for f in ('up', 'down', 'north', 'south', 'east', 'west')}
FULL = {'up': [0, 0, 16, 16], 'down': [0, 16, 16, 0], 'east': [0, 0, 1, 16], 'west': [0, 0, 1, 16], 'north': [0, 0, 16, 1], 'south': [0, 0, 16, 1]}
EYE_UV = {'up': [0, 0, 16, 16], 'down': [0, 0, 16, 16], 'north': [0, 0, 16, 1], 'south': [0, 0, 16, 1], 'east': [0, 15, 16, 16], 'west': [0, 0, 16, 1]}
PLANE = {'xy': ((1, 0, 0), (0, 1, 0), (0, 0, 1)),      # (the ring's two in-plane axes and its normal)
         'xz': ((1, 0, 0), (0, 0, -1), (0, 1, 0)),
         'yz': ((0, 1, 0), (0, 0, 1), (1, 0, 0))}


def _eye(c, n, t, along, across, d=0.34):
    """an eye on a surface facing n, its width along t (the upper lid toward -cross(n, t)... laid so the lid is outward), lit"""
    A, B = _sub(c, _mul(t, along / 2)), _add(c, _mul(t, along / 2))
    c2 = _add(c, _mul(n, d / 2))
    A, B = _add(A, _mul(n, d / 2)), _add(B, _mul(n, d / 2))
    return SEG(A, B, across, d, 'oph_eye', n, light=LIGHT, uv=EYE_UV)


def ring(plane, n, r0, r1, depth, band, rim, rim_in, eyes=(1, 1), rim_eyes=0, flames=0, phase=0.0, eye_size=None, flame_len=3.2):
    """a wheel in `plane` of n straight segments, from radius r0 to r1, `depth` thick: eyes on its two faces (every eyes[0]-th
    segment, starting at eyes[1]-1), rim_eyes (every k-th segment round the rim), flames (every k-th, between the rim eyes)"""
    P, Q, N = PLANE[plane]
    w, rm = r1 - r0, (r0 + r1) / 2
    ext = (w / 2) * math.tan(math.pi / n) + 0.02                       # (closes the wedge at the outer edge)
    pt = lambda a, r: _add(_mul(P, r * math.cos(a)), _mul(Q, r * math.sin(a)))
    out = []
    uv_band = {'up': [0, 0, 16, 16], 'down': [0, 0, 16, 16], 'west': [0, 0, 16, 16], 'east': [0, 0, 16, 16],
               'north': [0, 0, 16, 2], 'south': [0, 0, 16, 2]}
    ew, eh = eye_size or (w * 0.86, w * 0.66)                          # (along, across)
    for i in range(n):
        a0, a1 = phase + 2 * math.pi * i / n, phase + 2 * math.pi * (i + 1) / n
        am = (a0 + a1) / 2
        A, B = pt(a0, rm), pt(a1, rm)
        seg = SEG(A, B, w, depth, band, N, ext=ext, light=15 if band == 'oph_lightband' else 0,
                  shade=band != 'oph_lightband', uv=uv_band)
        seg['faces']['west']['texture'] = '#' + rim                    # (west: the outer rim; east: the inner face)
        seg['faces']['east']['texture'] = '#' + rim_in
        for f in ('north', 'south'): seg['faces'][f]['texture'] = '#' + rim_in
        out.append(seg)
        t = rigkit._unit(_sub(B, A))
        mid = _mul(_add(A, B), 0.5)
        radial = rigkit._unit(mid)
        if eyes and i % eyes[0] == eyes[1] - 1:
            for s in (1, -1):                                          # the two faces (each eye's upper lid outward)
                nn = _mul(N, s); tt = _mul(t, s)
                c = _add(mid, _mul(nn, depth / 2))
                out.append(_eye(c, nn, tt, ew, eh))
        rim_c = _add(mid, _mul(radial, w / 2))
        if rim_eyes and i % rim_eyes == 0:
            out.append(_eye(rim_c, radial, _mul(t, 1), min(ew, 3.0), depth * 0.78))
        if flames and i % flames == flames - 1:
            tip = _add(rim_c, _mul(radial, flame_len))
            base = _add(rim_c, _mul(radial, -0.3))
            out.append(SEG(base, tip, 2.3, 0.2, 'oph_flame', N, light=LIGHT, shade=False, uv=FULL))          # (crossed slabs:
            out.append(SEG(base, tip, depth * 0.9, 0.2, 'oph_flame', t, light=LIGHT, shade=False, uv=FULL))  #  a tongue from any side)
    return out


# the wheels' sizes (design units): nested, each ball inside the next one's hole (check())
RA = dict(plane='xy', n=16, r0=16.0, r1=20.0, depth=2.6)
RB = dict(plane='xz', n=12, r0=11.6, r1=14.8, depth=2.3)
RC = dict(plane='yz', n=10, r0=7.7, r1=9.9, depth=1.7)


def ring_a():
    return ring(**RA, band='oph_band', rim='oph_rim', rim_in='oph_rim_in', rim_eyes=2, flames=2, eye_size=(3.6, 2.7))


def ring_b():
    return ring(**RB, band='oph_band', rim='oph_rim', rim_in='oph_rim_in', rim_eyes=1, eye_size=(3.2, 2.3), phase=math.pi / 12)


def ring_c():
    return ring(**RC, band='oph_lightband', rim='oph_lightband', rim_in='oph_lightband', eyes=(2, 1), eye_size=(2.6, 1.8))


def core():
    """the blazing heart: a star of light (two crossed cubes), a translucent glow round it, rays along the six axes and the
    eight diagonals, her gold halo tilted round it"""
    C = []
    s = 3.6
    C.append(el((-s / 2,) * 3, (s / 2,) * 3, 'oph_light', PV, rot=((35.264, 45.0, 0.0), (0, 0, 0)), uv=WHOLE, light=LIGHT))
    s2 = 3.0
    C.append(el((-s2 / 2,) * 3, (s2 / 2,) * 3, 'oph_light', PV, rot=((0.0, 45.0, 45.0), (0, 0, 0)), uv=WHOLE, light=LIGHT))
    a = 6.0
    C.append(el((-a / 2,) * 3, (a / 2,) * 3, 'oph_aura', PV, rot=((0.0, 45.0, 0.0), (0, 0, 0)), uv=WHOLE, light=LIGHT))
    for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):     # the six long rays
        up = (0, 0, 1) if d[2] == 0 else (0, 1, 0)
        C.append(SEG(_mul(d, 1.2), _mul(d, 6.7), 0.8, 0.8, 'oph_ray', up, light=LIGHT, shade=False, uv=WHOLE))
    for sx in (1, -1):                                                                  # the eight short ones
        for sy in (1, -1):
            for sz in (1, -1):
                d = rigkit._unit((sx, sy, sz))
                C.append(SEG(_mul(d, 1.2), _mul(d, 4.9), 0.55, 0.55, 'oph_ray', (0, 1, 0) if sy == 0 else (1, 0, 0), light=LIGHT, shade=False, uv=WHOLE))
    tilt = math.radians(22)                                                             # her halo, tilted round the star
    n, R = 14, 5.0
    up_t = (0.0, math.cos(tilt), math.sin(tilt))
    hp = lambda a: (R * math.cos(a), -R * math.sin(a) * math.sin(tilt), R * math.sin(a) * math.cos(tilt))
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        C.append(SEG(hp(a0), hp(a1), 0.9, 0.55, 'oph_halo', up_t, ext=0.1, light=LIGHT, shade=False, uv=WHOLE))
    return C


BUILD = {'ring_a': ring_a, 'ring_b': ring_b, 'ring_c': ring_c, 'core': core}


def models():
    """{model id: (textures, elements)} - every element inside the model box, every uv on its texture"""
    M = {}
    for p in PARTS:
        els = BUILD[p]()
        for e in els:
            for v in e['from'] + e['to']:
                assert -16 <= v <= 32, (p, e['from'], e['to'])
            for fc in e['faces'].values():
                fc['uv'] = [max(0.0, min(16.0, c)) for c in fc['uv']]
        used = sorted({f['texture'][1:] for e in els for f in e['faces'].values()})
        M[model_id(p)] = ({t: f'bm:block/{t}' for t in used}, els)
    return M


# ---------------------------------------------------------------------------------------------------- the nesting check
def _corners(e):
    """an element's 8 corners (model units), turned by its rotation"""
    f, t = e['from'], e['to']
    cs = [(x, y, z) for x in (f[0], t[0]) for y in (f[1], t[1]) for z in (f[2], t[2])]
    r = e.get('rotation')
    if not r: return cs
    M = _rot(r)
    o = r['origin']
    return [tuple(sum(M[i][j] * (c[j] - o[j]) for j in range(3)) + o[i] for i in range(3)) for c in cs]


def _rot(r):
    ax, ay, az = (math.radians(r.get(k, 0)) for k in 'xyz')
    Rx = [[1, 0, 0], [0, math.cos(ax), -math.sin(ax)], [0, math.sin(ax), math.cos(ax)]]
    Ry = [[math.cos(ay), 0, math.sin(ay)], [0, 1, 0], [-math.sin(ay), 0, math.cos(ay)]]
    Rz = [[math.cos(az), -math.sin(az), 0], [math.sin(az), math.cos(az), 0], [0, 0, 1]]
    mm = lambda A, B: [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    return mm(Rz, mm(Ry, Rx))


def _ball(els):
    """the radius of the ball (about the centre, design units) each part's elements fit in"""
    return max(math.sqrt(sum((c[i] - 8) ** 2 for i in range(3))) for e in els for c in _corners(e))


def _hole(els):
    """the nearest any of a part's elements comes to the centre (design units)"""
    best = 1e9
    for e in els:
        f, t = e['from'], e['to']
        r = e.get('rotation')
        o = r['origin'] if r else (8, 8, 8)
        M = _rot(r) if r else [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        q = [8 - o[i] for i in range(3)]
        q = [sum(M[j][i] * q[j] for j in range(3)) + o[i] for i in range(3)]       # (the centre in the box's own frame)
        d = math.sqrt(sum((q[i] - max(f[i], min(t[i], q[i]))) ** 2 for i in range(3)))
        best = min(best, d)
    return best


def check():
    """every texture drawn, every element and uv in range, and the wheels nested (each part's ball inside the next one's hole,
    so they can turn independently, any way, and never cut each other). Returns {part: (hole, ball)}."""
    tex = textures(); M = models(); out = {}
    for name, (t, els) in M.items():
        for k in t: assert k in tex, (name, k)
        for e in els:
            assert all(-16 <= v <= 32 for v in e['from'] + e['to']), (name, e)
            assert all(e['to'][i] > e['from'][i] for i in range(3)), (name, e)
            for fc in e['faces'].values():
                assert all(0 <= v <= 16 for v in fc['uv']), (name, fc)
                assert fc['texture'][1:] in t, (name, fc)
        out[name[len(PREFIX):]] = (_hole(els), _ball(els))
    order = ['core', 'ring_c', 'ring_b', 'ring_a']
    for a, b in zip(order, order[1:]):
        assert out[a][1] < out[b][0], (a, out[a], b, out[b])
    return out


def rp(R):
    """gen_rp: the oph_ block textures (TEXTURE_MODS), the four parts as 3D models at display scale (HATS, DISPLAY_3D_EXTRA)"""
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    for name, (tex, els) in models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (PREFIX,)


if __name__ == '__main__':
    for p, (h, b) in check().items():
        print(f'{p:7s} hole {h:6.2f}  ball {b:6.2f}  elements {len(BUILD[p]())}')

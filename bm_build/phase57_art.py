"""2.37: Emma's rig - textures and item models (normal form + ethereal form).

Each part is its own item model with its joint at model (8, 8, 8), so a display entity at the joint turns the part
about it. Design units: feet at y=0, facing -z, her right is +x (a design unit is 1/16 of a block at scale 1; the rig
is drawn at RIG_SCALE)."""
import math
import random
from PIL import Image, ImageDraw

RES = 4                                   # texels per design unit: every texture is 64 x 64 (16 units)
RIG_SCALE = 0.85
PIVOT = {'body': (0, 11, 0), 'head': (0, 24, 0), 'armr': (4.0, 22.4, 0), 'arml': (-4.0, 22.4, 0),
         'legr': (1.7, 11, 0), 'legl': (-1.7, 11, 0), 'wingr': (1.0, 21.5, 2.2), 'wingl': (-1.0, 21.5, 2.2)}
PIVOT['wingro'], PIVOT['winglo'] = PIVOT['wingr'], PIVOT['wingl']      # (the outer halves stand at the wing roots; a translation reaches the mid-joint)
PARTS = ('body', 'head', 'armr', 'arml', 'legr', 'legl', 'wingr', 'wingl', 'wingro', 'winglo')
WING_LIFT = 30
WING_SPLIT = 11.0                                                    # design units along the leading edge where the outer half hinges


def wing_mid(sx):
    px, py, pz = PIVOT['wingr' if sx > 0 else 'wingl']
    return (px + sx * WING_SPLIT * math.cos(math.radians(WING_LIFT)), py + WING_SPLIT * math.sin(math.radians(WING_LIFT)), pz)


def hexc(h, a=255):
    h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


# ---------------------------------------------------------------------------------------------------- textures
def _cloth(c, seed, var=0.035, stripes=None, edge=None, grain=None):
    rnd = random.Random(seed); base = hexc(c)[:3]
    im = Image.new('RGBA', (64, 64))
    for y in range(64):
        for x in range(64):
            k = 1 + rnd.uniform(-var, var)
            if stripes and (x % stripes[0]) in stripes[1]: k *= stripes[2]
            if grain and (y % grain[0]) == 0: k *= grain[1]
            im.putpixel((x, y), tuple(int(max(0, min(255, v * k))) for v in base) + (255,))
    return im


def _hair(seed, pal):
    rnd = random.Random(seed); P = [hexc(x) for x in pal]
    im = Image.new('RGBA', (64, 64))
    for x in range(64):
        o = 0 if rnd.random() < 0.7 else rnd.choice((-1, 1))
        for y in range(64):
            if rnd.random() < 0.06: o = 0 if o else rnd.choice((-1, 1))
            im.putpixel((x, y), P[max(0, min(len(P) - 1, 2 + o))])
    return im


HAIR = ('#6e3616', '#7a3e1a', '#86461e', '#925024', '#a05a2a')


def _face(eye_dark, eye_mid, eye_light, eye_glow, pupil):
    """36 x 32 on a 64 x 64 sheet: big anime eyes, soft brows, a small smile, blush and freckles, bangs on top."""
    im = Image.new('RGBA', (64, 64), hexc('#f7d7bf')); d = ImageDraw.Draw(im); P = hexc
    for y in range(9):
        for x in range(36): im.putpixel((x, y), P('#efc4a6'))
    def eye(cx, flip):
        x0, y0 = cx - 5, 13
        d.ellipse((x0, y0, x0 + 10, y0 + 13), fill=P('#ffffff'))
        d.ellipse((x0 + 1, y0 + 1, x0 + 9, y0 + 13), fill=P(eye_dark))
        d.ellipse((x0 + 1, y0 + 5, x0 + 9, y0 + 13), fill=P(eye_mid))
        d.ellipse((x0 + 2, y0 + 8, x0 + 8, y0 + 13), fill=P(eye_light))
        d.ellipse((x0 + 3, y0 + 4, x0 + 7, y0 + 10), fill=P(pupil))
        hx = x0 + 2 if not flip else x0 + 5
        d.ellipse((hx, y0 + 2, hx + 3, y0 + 5), fill=P('#ffffff'))
        d.point((x0 + (6 if not flip else 3), y0 + 10), fill=P('#ffffff')); d.point((x0 + (7 if not flip else 2), y0 + 10), fill=P('#ffffff'))
        d.arc((x0 - 1, y0 - 1, x0 + 11, y0 + 10), 195, 345, fill=P('#2a1610'), width=2)
        ox = x0 + 10 if not flip else x0; sx = 1 if not flip else -1
        d.line((ox, y0 + 2, ox + 2 * sx, y0), fill=P('#2a1610'), width=1); d.point((ox + sx, y0 + 4), fill=P('#2a1610'))
        if eye_glow: d.point((cx, y0 + 11), fill=P(eye_glow))
    eye(9, False); eye(27, True)
    for cx in (8, 28):
        d.ellipse((cx - 4, 26, cx + 4, 29), fill=P('#f6b4aa'))
        for fx, fy in ((-2, 27), (0, 28), (2, 27)): im.putpixel((cx + fx, fy), P('#c8705c'))
    for yy, row in enumerate(('m....m', '.mmmm.')):
        for xx, ch in enumerate(row):
            if ch == 'm': im.putpixel((15 + xx, 28 + yy), P('#8a3428'))
    hair_c = [P('#74391a'), P('#8a4a1e'), P('#a0582a')]; rnd = random.Random(5)
    for x in range(36):
        edge = 6 + int(3 * math.sin(x / 3.2)) + (2 if x < 12 else 0) + rnd.choice((0, 0, 1))
        if 4 <= x <= 14 or 22 <= x <= 32: edge = min(edge, 8)
        for y in range(edge): im.putpixel((x, y), hair_c[(x // 3 + y // 4) % 3])
    for cx, s in ((9, 1), (27, -1)):
        for dx, y in ((-3, 11), (-2, 10), (-1, 10), (0, 10), (1, 10), (2, 11)): im.putpixel((cx + dx * s, y), P('#6e3618'))
    return im


def _chest():
    im = _cloth('#3f8fd0', 11)
    for x in range(24): im.putpixel((x, 0), hexc('#5aa6e0'))
    for y in range(15, 23):                                            # lace band at the waist (the face is 24 x 22.4)
        for x in range(64):
            if (x + (y % 2) * 2) % 4 == 0 or y == 15: im.putpixel((x, y), hexc('#2c6aa8'))
    d = ImageDraw.Draw(im)                                             # the pink flower brooch
    d.polygon([(12, 2), (13.5, 5), (17, 5.5), (14.5, 7.5), (15.5, 11), (12, 9), (8.5, 11), (9.5, 7.5), (7, 5.5), (10.5, 5)], fill=hexc('#d84aa8'))
    d.rectangle((11, 6, 12, 7), fill=hexc('#f4d040'))
    return im


def _skirt(seed):
    im = _cloth('#3d72aa', seed, stripes=(9, (0,), 0.86))
    for x in range(64):
        for y in range(64):
            if x % 9 == 4 and y % 16 > 6: im.putpixel((x, y), hexc('#2a5182'))
    return im


def _buckle():
    im = _cloth('#f2f2f6', 3)
    ImageDraw.Draw(im).ellipse((1, 1, 7, 5), outline=hexc('#b8b8c4'))
    return im


def _shoe():
    im = _cloth('#2e3c74', 4)
    for x in range(64): im.putpixel((x, 0), hexc('#3a4a88'))
    return im


def _ee_chest():
    """Ethereal breastplate front (27 x 16 texels used): steel with a light-blue teardrop and a pink star gem."""
    im = _cloth('#8a9bb4', 21, var=0.03)
    d = ImageDraw.Draw(im)
    for x in range(64): im.putpixel((x, 0), hexc('#c8d2e0'))
    d.line((2, 3, 6, 4), fill=hexc('#c8d2e0')); d.line((25, 3, 21, 4), fill=hexc('#c8d2e0'))
    d.ellipse((10, 5, 17, 14), fill=hexc('#a8dcec'), outline=hexc('#5aa8c4'))
    d.polygon([(13.5, 1), (11, 7), (16, 7)], fill=hexc('#a8dcec'))
    d.polygon([(13.5, 6), (14.6, 9), (17, 9.5), (14.6, 10.5), (13.5, 13), (12.4, 10.5), (10, 9.5), (12.4, 9)], fill=hexc('#e040b0'))
    d.point((13, 9), fill=hexc('#ff9ae0'))
    for y in range(14, 17):
        for x in range(64): im.putpixel((x, y), hexc('#6a7a94'))
    return im


def _scales():
    im = _cloth('#2a3a5e', 22)
    for y in range(64):
        for x in range(64):
            if (y % 3 == 2) or ((x + (y // 3) * 2) % 4 == 0 and y % 3 == 1): im.putpixel((x, y), hexc('#1a2440'))
    return im


def _crown():
    im = _cloth('#dfe4ec', 23)
    d = ImageDraw.Draw(im)
    d.polygon([(0, 0), (2, 3), (4, 0), (6.5, 3), (9, 0), (11, 3), (13, 0), (13, 8), (0, 8)], fill=hexc('#eef2f8'), outline=hexc('#9aa4b4'))
    d.polygon([(6.5, 3), (8, 5), (6.5, 7), (5, 5)], fill=hexc('#d02aa0'))
    d.point((2, 5), fill=hexc('#2a6ad8')); d.point((11, 5), fill=hexc('#2a6ad8'))
    return im


def _magenta():
    im = Image.new('RGBA', (64, 64))
    for y in range(64):
        for x in range(64):
            t = (y % 16) / 15
            c = tuple(int(a * (1 - t) + b * t) for a, b in zip(hexc('#e050b8')[:3], hexc('#8a1460')[:3]))
            im.putpixel((x, y), c + (255,))
    for x in range(2, 5):
        for y in range(1, 3): im.putpixel((x, y), hexc('#ff9ae4'))
    return im


def _feather(seed, tip):
    """White feathers: a grey shaft line every 8 texels along their length, greying toward the tips."""
    rnd = random.Random(seed); im = Image.new('RGBA', (64, 64))
    for y in range(64):
        for x in range(64):
            g = 248 - (int(30 * (y / 63)) if tip else 0) + rnd.randint(-4, 4)
            if x % 8 == 0: g -= 36
            elif x % 8 in (1, 7): g -= 12
            im.putpixel((x, y), (g, g, min(255, g + 4), 255))
    return im


def _blade():
    im = Image.new('RGBA', (64, 64))
    for y in range(64):
        for x in range(64):
            t = min(1, (y % 32) / 18)
            c = tuple(int(a * (1 - t) + b * t) for a, b in zip(hexc('#f4fbff')[:3], hexc('#9ad6ea')[:3]))
            im.putpixel((x, y), c + (255,))
    return im


def textures():
    T = {}
    T['em2_skin'] = _cloth('#f7d7bf', 12, var=0.02)
    T['em2_cheek'] = _cloth('#efc4a6', 13, var=0.02)
    T['em2_hair'] = _hair(1, HAIR)
    T['em2_blue'] = _cloth('#3f8fd0', 14)
    T['em2_chest'] = _chest()
    T['em2_skirt'] = _skirt(15)
    T['em2_scarf'] = _cloth('#80d8e4', 16)
    T['em2_scarf2'] = _cloth('#6cc8d6', 17)
    T['em2_white'] = _cloth('#f4f4f8', 18, var=0.02)
    T['em2_belt'] = _cloth('#5a3a1e', 19)
    T['em2_buckle'] = _buckle()
    T['em2_shoe'] = _shoe()
    T['em2_pink'] = _cloth('#d04aa8', 20)
    T['em2_pinkdark'] = _cloth('#a83288', 24)
    T['em2_face'] = _face('#155d6e', '#22a2b2', '#5ad8dc', None, '#0a2630')
    T['ee_face'] = _face('#4a1a7a', '#8a3ad0', '#c48af0', '#f0d0ff', '#1a0630')
    T['ee_steel'] = _cloth('#8a9bb4', 25, var=0.03)
    T['ee_steel_lt'] = _cloth('#c4cedc', 26, var=0.025)
    T['ee_steel_dk'] = _cloth('#5c6c88', 27, var=0.03)
    T['ee_navy'] = _cloth('#24345a', 28, grain=(5, 0.85))
    T['ee_glove'] = _cloth('#1c1c22', 29)
    T['ee_magenta'] = _magenta()
    T['ee_chest'] = _ee_chest()
    T['ee_scales'] = _scales()
    T['ee_belt'] = _cloth('#202024', 30)
    T['ee_crown'] = _crown()
    T['ee_feather'] = _feather(31, True)
    T['ee_down'] = _feather(32, False)
    T['ee_blade'] = _blade()
    T['ee_shaft'] = _cloth('#3a4a6a', 33, grain=(6, 0.8))
    return T


# ---------------------------------------------------------------------------------------------------- models
def _el(fr, to, tex, piv, rot=None, uv=None, faces=None):
    """An element in design units -> model units (joint at 8,8,8). uv: {face: [u1,v1,u2,v2]} overrides."""
    off = [8 - piv[i] for i in range(3)]
    f = [round(fr[i] + off[i], 4) for i in range(3)]; t = [round(to[i] + off[i], 4) for i in range(3)]
    w, h, d = to[0] - fr[0], to[1] - fr[1], to[2] - fr[2]
    sz = {'north': (w, h), 'south': (w, h), 'east': (d, h), 'west': (d, h), 'up': (w, d), 'down': (w, d)}
    out = {}
    for fc in (faces or ('north', 'south', 'east', 'west', 'up', 'down')):
        a, b = sz[fc]
        u = (uv or {}).get(fc) or [0, 0, round(min(16, max(a, 0.25)), 4), round(min(16, max(b, 0.25)), 4)]
        out[fc] = {'uv': u, 'texture': '#' + tex}
    e = {'from': f, 'to': t, 'faces': out}
    if rot:
        ax, ang, org = rot
        e['rotation'] = {'origin': [round(org[i] + off[i], 4) for i in range(3)], 'axis': ax, 'angle': ang}
    return e


def models():
    """{name: (textures, elements)} for every rig part."""
    M = {}
    TX = {k: f'bm:block/{k}' for k in textures()}
    def part(name, pv, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({k: TX[k] for k in used}, els)

    # ---- legs (normal): socks, lace, knees, Mary Janes
    def leg(sx):
        pv = PIVOT['legr' if sx > 0 else 'legl']
        x0, x1 = (0.7, 2.7) if sx > 0 else (-2.7, -0.7)
        return [_el((x0, 1.6, -1.0), (x1, 7.4, 1.0), 'em2_white', pv), _el((x0 - 0.1, 7.0, -1.1), (x1 + 0.1, 7.6, 1.1), 'em2_white', pv),
                _el((x0, 7.6, -1.0), (x1, 12.0, 1.0), 'em2_skin', pv),
                _el((x0 - 0.3, 0, -2.6), (x1 + 0.3, 1.6, 1.2), 'em2_shoe', pv),
                _el((x0 - 0.32, 0.9, -1.4), (x1 + 0.32, 1.2, -0.9), 'em2_belt', pv)]
    part('em_legr', PIVOT['legr'], leg(1)); part('em_legl', PIVOT['legl'], leg(-1))

    # ---- body (normal): skirt, belt, torso with the brooch, scarf, collar, neck
    pv = PIVOT['body']
    sk = lambda fr, to, rot=None: _el(fr, to, 'em2_skirt', pv, rot)
    body = [sk((-3.6, 14.6, -2.6), (3.6, 16.2, 2.6)), sk((-4.4, 13.0, -3.2), (4.4, 14.8, 3.2)), sk((-5.2, 11.6, -3.9), (5.2, 13.2, 3.9)),
            sk((-5.6, 9.2, -4.8), (5.6, 13.0, -3.8), ('x', 22.5, (0, 13.0, -4.3))), sk((-5.6, 9.2, 3.8), (5.6, 13.0, 4.8), ('x', -22.5, (0, 13.0, 4.3))),
            sk((4.8, 9.2, -4.6), (5.8, 13.0, 4.6), ('z', 22.5, (5.3, 13.0, 0))), sk((-5.8, 9.2, -4.6), (-4.8, 13.0, 4.6), ('z', -22.5, (-5.3, 13.0, 0))),
            _el((-3.3, 15.8, -2.3), (3.3, 17.0, 2.3), 'em2_belt', pv),
            _el((-1.1, 15.6, -2.6), (1.1, 17.2, -2.25), 'em2_buckle', pv, uv={'north': [0, 0, 2.2, 1.6]}),
            _el((-3.0, 17.0, -2.0), (3.0, 22.6, 2.0), 'em2_chest', pv, uv={'north': [0, 0, 6, 5.6], 'south': [6, 2, 12, 7.6], 'east': [6, 2, 10, 7.6], 'west': [6, 2, 10, 7.6]}),
            _el((-3.3, 22.2, -2.3), (3.3, 23.5, 2.3), 'em2_scarf', pv),
            _el((1.0, 20.2, -2.6), (2.6, 22.4, -2.25), 'em2_scarf2', pv, ('z', -22.5, (1.8, 22.4, -2.4))),
            _el((-1.0, 22.6, -2.45), (1.0, 23.6, -2.3), 'em2_white', pv),
            _el((-1.0, 23.4, -1.0), (1.0, 24.4, 1.0), 'em2_skin', pv)]
    part('em_body', pv, body)

    # ---- head (normal + ethereal share the shape; hair differs)
    def head(face, ethereal):
        pv = PIVOT['head']; hr = lambda fr, to, rot=None: _el(fr, to, 'em2_hair', pv, rot)
        els = [_el((-4.5, 24.0, -4.0), (4.5, 32.0, 4.0), 'em2_skin', pv, uv={'north': [0, 0, 9, 8]}),
               _el((4.5, 26.2, -0.6), (5.0, 28.0, 0.6), 'em2_cheek', pv), _el((-5.0, 26.2, -0.6), (-4.5, 28.0, 0.6), 'em2_cheek', pv),
               hr((-4.9, 30.6, -4.4), (4.9, 32.9, 4.4)), hr((-4.9, 25.0, 3.4), (4.9, 30.8, 4.6)),
               hr((4.5, 25.6, -2.4), (5.2, 30.8, 4.4)), hr((-5.2, 25.6, -2.4), (-4.5, 30.8, 4.4)),
               hr((-4.9, 30.0, -4.6), (4.9, 30.8, -4.0)), hr((-4.9, 29.7, -4.6), (-1.2, 30.2, -4.0)), hr((1.8, 29.7, -4.6), (4.9, 30.2, -4.0)),
               hr((4.2, 24.4, -3.4), (5.4, 28.6, -2.0)), hr((3.6, 23.6, -3.4), (5.4, 24.6, -2.0)), hr((-5.4, 25.4, -3.4), (-4.2, 28.6, -2.0))]
        els[0]['faces']['north']['texture'] = '#' + face
        if not ethereal:
            els += [hr((-1.6, 29.6, 4.2), (1.6, 32.6, 6.2)),
                    hr((-2.6, 26.0, 5.0), (0.4, 31.2, 7.6), ('z', -22.5, (-1.0, 31.0, 6.3))),
                    hr((-4.0, 22.4, 5.3), (-1.8, 27.4, 7.3), ('z', -45, (-2.9, 26.8, 6.3))),
                    _el((-0.8, 31.4, 6.0), (0.8, 32.8, 6.9), 'em2_pinkdark', pv),
                    _el((-3.0, 31.0, 6.1), (-0.8, 33.4, 6.7), 'em2_pink', pv), _el((0.8, 31.0, 6.1), (3.0, 33.4, 6.7), 'em2_pink', pv)]
        else:
            # long hair down her back, a lock over her left shoulder, a high ponytail flicking out to her left with a flower tie
            els += [hr((-4.7, 18.5, 3.2), (4.7, 25.2, 4.8)), hr((-5.6, 17.0, -1.6), (-4.4, 25.8, 0.6), ('z', -8, (-5.0, 25.8, -0.5))),
                    hr((-2.4, 32.4, 0.4), (1.2, 35.4, 3.6)),
                    hr((-6.6, 33.0, 0.8), (-1.6, 35.8, 3.2), ('z', 30, (-1.6, 34.4, 2.0))),
                    hr((-10.4, 33.6, 1.0), (-6.0, 35.8, 3.0), ('z', 50, (-6.0, 34.6, 2.0))),
                    _el((-1.8, 34.6, 0.2), (0.6, 36.4, 3.8), 'em2_pink', pv), _el((-1.0, 35.2, -0.1), (-0.2, 36.0, 0.3), 'ee_magenta', pv)]
        return els
    part('em_head', PIVOT['head'], head('em2_face', False))
    part('ee_head', PIVOT['head'], head('ee_face', True))

    # ---- arms (normal): sleeve, white cuff, hand
    def arm(sx, ethereal):
        nm = 'armr' if sx > 0 else 'arml'; pv = PIVOT[nm]; cx = pv[0]
        if not ethereal:
            return [_el((cx - 1, 15.8, -1), (cx + 1, 22.8, 1), 'em2_blue', pv), _el((cx - 1.1, 14.6, -1.1), (cx + 1.1, 15.8, 1.1), 'em2_white', pv),
                    _el((cx - 0.9, 13.0, -0.9), (cx + 0.9, 14.6, 0.9), 'em2_skin', pv)]
        els = [_el((cx - 0.95, 14.8, -0.95), (cx + 0.95, 22.4, 0.95), 'ee_navy', pv), _el((cx - 1.05, 12.6, -1.05), (cx + 1.05, 14.9, 1.05), 'ee_glove', pv),
               _el((cx - 1.5, 20.6, -1.5), (cx + 1.5, 23.0, 1.5), 'ee_steel', pv), _el((cx - 1.2, 22.6, -1.2), (cx + 1.2, 23.6, 1.2), 'ee_magenta', pv),
               _el((cx - 1.6, 20.2, -1.6), (cx + 1.6, 20.7, 1.6), 'ee_steel_lt', pv)]
        if sx > 0:      # her right hand carries the crescent axe (shaft through the fist, blade out to her right)
            els += [_el((cx - 0.4, 3.0, -0.4), (cx + 0.4, 31.0, 0.4), 'ee_shaft', pv),
                    _el((cx - 0.6, 3.6, -0.6), (cx + 0.6, 5.0, 0.6), 'ee_steel', pv), _el((cx - 0.25, 1.4, -0.25), (cx + 0.25, 3.6, 0.25), 'ee_steel_lt', pv),
                    _el((cx - 0.55, 18.0, -0.55), (cx + 0.55, 19.4, 0.55), 'ee_steel_dk', pv),
                    _el((cx - 0.3, 30.8, -0.3), (cx + 0.3, 34.0, 0.3), 'ee_steel_lt', pv, ('z', 0, (cx, 31, 0))),
                    # the crescent: a broad back, two horns sweeping out and round
                    _el((cx + 0.4, 23.6, -0.3), (cx + 3.4, 31.4, 0.3), 'ee_blade', pv),
                    _el((cx + 3.0, 20.0, -0.28), (cx + 5.6, 24.6, 0.28), 'ee_blade', pv, ('z', 32, (cx + 3.0, 24.6, 0))),
                    _el((cx + 3.0, 30.4, -0.28), (cx + 5.6, 35.0, 0.28), 'ee_blade', pv, ('z', -32, (cx + 3.0, 30.4, 0))),
                    _el((cx + 3.2, 23.0, -0.26), (cx + 5.4, 32.0, 0.26), 'ee_blade', pv),
                    _el((cx + 5.2, 24.6, -0.2), (cx + 6.4, 30.4, 0.2), 'ee_steel_lt', pv),
                    _el((cx - 1.6, 26.0, -0.7), (cx + 1.6, 29.2, 0.7), 'em2_pink', pv, ('z', 45, (cx, 27.6, 0))),
                    _el((cx - 0.7, 27.0, -0.9), (cx + 0.7, 28.2, 0.9), 'ee_magenta', pv)]
        else:           # her open left hand: a thumb out
            els += [_el((cx + 0.6, 13.4, -0.6), (cx + 1.5, 14.6, 0.2), 'ee_glove', pv)]
        return els
    part('em_armr', PIVOT['armr'], arm(1, False)); part('em_arml', PIVOT['arml'], arm(-1, False))
    part('ee_armr', PIVOT['armr'], arm(1, True)); part('ee_arml', PIVOT['arml'], arm(-1, True))

    # ---- ethereal body: undersuit, breastplate with the teardrop emblem, scale mail, belt with the crown buckle
    pv = PIVOT['body']
    M_body = [_el((-3.0, 15.4, -2.0), (3.0, 22.6, 2.0), 'ee_navy', pv),
              _el((-3.4, 18.4, -2.5), (3.4, 22.4, 2.4), 'ee_steel', pv, uv={'north': [0, 0, 6.8, 4.0]}),
              _el((-3.6, 22.0, -2.6), (3.6, 22.6, 2.5), 'ee_steel_lt', pv),
              _el((-2.4, 17.7, -2.45), (2.4, 18.5, -2.15), 'ee_steel', pv),
              _el((-3.15, 15.6, -2.2), (3.15, 17.8, 2.2), 'ee_scales', pv),
              _el((-3.4, 14.4, -2.4), (3.4, 15.8, 2.4), 'ee_belt', pv),
              _el((-1.7, 14.2, -2.7), (1.7, 16.4, -2.35), 'ee_crown', pv, uv={'north': [0, 0, 3.4, 2.2]}),
              _el((-1.4, 22.4, -2.2), (1.4, 23.6, 1.6), 'ee_navy', pv),
              _el((-1.0, 23.4, -1.0), (1.0, 24.4, 1.0), 'em2_skin', pv)]
    M_body[1]['faces']['north']['texture'] = '#ee_chest'
    part('ee_body', pv, M_body)

    # ---- ethereal legs: steel greaves, magenta shin plates, armoured boots
    def eleg(sx):
        pv = PIVOT['legr' if sx > 0 else 'legl']
        x0, x1 = (0.5, 2.9) if sx > 0 else (-2.9, -0.5)
        return [_el((x0, 7.4, -1.2), (x1, 14.6, 1.2), 'ee_steel', pv), _el((x0 - 0.15, 6.4, -1.45), (x1 + 0.15, 8.0, 1.3), 'ee_steel_lt', pv),
                _el((x0, 1.2, -1.2), (x1, 6.6, 1.2), 'ee_steel', pv),
                _el((x0 + 0.2, 2.4, -1.55), (x1 - 0.2, 6.8, -1.15), 'ee_magenta', pv),
                _el((x0 - 0.15, 0, -2.8), (x1 + 0.15, 1.5, 1.4), 'ee_steel_dk', pv)]
    part('ee_legr', PIVOT['legr'], eleg(1)); part('ee_legl', PIVOT['legl'], eleg(-1))

    # ---- wings: a covert bar and fanned primaries, built for her left; the right is the mirror
    def wing(sx, half):
        """A leading edge sweeping up and out, coverts under it, primaries hanging from it - longer and splayed toward the tip.
        Split at WING_SPLIT: the inner half turns at the root, the outer half at the mid-joint (so the wing can ripple)."""
        nm = 'wingr' if sx > 0 else 'wingl'; px, py, pz = PIVOT[nm]
        pv = PIVOT[nm] if half == 'in' else wing_mid(sx)
        lift = WING_LIFT; ca, sa = math.cos(math.radians(lift)), math.sin(math.radians(lift))
        lo, hi = (0, WING_SPLIT) if half == 'in' else (WING_SPLIT, 22)
        def bar(u0, u1, y0, y1, z0, z1, tex):
            u0, u1 = max(u0, lo), min(u1, hi)
            a, b = px + sx * u0, px + sx * u1
            return _el((min(a, b), py + y0, pz + z0), (max(a, b), py + y1, pz + z1), tex, pv, ('z', sx * lift, (px, py, pz)))
        els = [bar(0, 22, -0.6, 1.8, 0.0, 1.6, 'ee_down'), bar(1.5, 19, -4.2, -0.4, 0.3, 1.3, 'ee_down')]
        for i, u in enumerate(range(3, 23, 2)):
            if not lo <= u < hi: continue
            tx, ty = px + sx * u * ca, py + u * sa - 0.8
            L = 6.5 + i * 1.15; ang = 4 + i * 3.6
            els.append(_el((tx - 1.0, ty - L, pz + 0.45 + 0.04 * i), (tx + 1.0, ty, pz + 1.0 + 0.04 * i), 'ee_feather', pv, ('z', sx * ang, (tx, ty, pz))))
        return els
    part('ee_wingr', PIVOT['wingr'], wing(1, 'in')); part('ee_wingl', PIVOT['wingl'], wing(-1, 'in'))
    part('ee_wingro', wing_mid(1), wing(1, 'out')); part('ee_winglo', wing_mid(-1), wing(-1, 'out'))
    return M


def ribbon_icon(R):
    return R.grid(['................', '................', '...PP......PP...', '..PLLP....PLLP..', '..PLLLP..PLLLP..', '..PLLLPPPPLLLP..',
                   '..PPLLPDDPLLPP..', '...PPPPDDPPPP...', '......PDDP......', '.....PP..PP.....', '....PP....PP....', '...PP......PP...',
                   '...P........P...', '................', '................', '................'],
                  dict(P='#c8389a', L='#ff8ad0', D='#8a1a66'))


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    for name, (tex, els) in models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + ('em_', 'ee_')
    R.ICONS['emma_ribbon'] = ribbon_icon(R)


# ---------------------------------------------------------------------------------------------------- poses
# In the display transform's frame the model is turned 180 degrees: her front is +z and her right is -x. A hanging limb
# swings forward with a negative x rotation; her right limb swings out with a negative z rotation, her left with a positive.
def qa(axis, deg):
    s, c = math.sin(math.radians(deg) / 2), math.cos(math.radians(deg) / 2)
    return (s if axis == 'x' else 0.0, s if axis == 'y' else 0.0, s if axis == 'z' else 0.0, c)


def qmul(a, b):
    ax, ay, az, aw = a; bx, by, bz, bw = b
    return (aw * bx + ax * bw + ay * bz - az * by, aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw, aw * bw - ax * bx - ay * by - az * bz)


def limb(side, fwd=0.0, out=0.0):
    """side +1 = her right, -1 = her left."""
    return qmul(qa('x', -fwd), qa('z', -out * side))


def torso(lean=0.0, tilt=0.0, turn=0.0):
    return qmul(qa('y', turn), qmul(qa('x', lean), qa('z', tilt)))


I = (0.0, 0.0, 0.0, 1.0)
FOLD = dict(armr=limb(1, 24, -22), arml=limb(-1, 24, -22))
def wings(inner, outer, lift=0.0):
    """Wing beat: the inner halves sweep (about y) and lift (about z); the outer halves follow at their own angle."""
    return dict(wingr=qmul(qa('y', -inner), qa('z', -lift)), wingl=qmul(qa('y', inner), qa('z', lift)),
                wingro=qmul(qa('y', -outer), qa('z', -lift * 0.6)), winglo=qmul(qa('y', outer), qa('z', lift * 0.6)))


WINGS_UP = wings(28, 20, 0)
WINGS_DN = wings(-14, -24, -10)


def P(dy=0.0, **parts):
    d = {k: I for k in PARTS}; d.update(parts); d['_dy'] = dy
    return d


POSES = {
    # idle: arms politely folded in front, a little side-to-side sway with the head tilting the other way
    'idle_a': P(body=torso(tilt=3), head=torso(lean=5, tilt=-7), **FOLD),
    'idle_b': P(body=torso(tilt=-3), head=torso(lean=5, tilt=7), **FOLD),
    'idle_hop': P(0.07, body=torso(), head=torso(lean=-4), legr=limb(1, -12), legl=limb(-1, -12), **FOLD),
    # walk: small steps, hands swinging a little out to the sides, a bounce between steps
    'walk_a': P(body=torso(tilt=4), head=torso(tilt=-5), legr=limb(1, 24), legl=limb(-1, -24), armr=limb(1, -16, 16), arml=limb(-1, 16, 16)),
    'walk_up': P(0.05, body=torso(), head=torso(lean=-3), armr=limb(1, 0, 20), arml=limb(-1, 0, 20)),
    'walk_b': P(body=torso(tilt=-4), head=torso(tilt=5), legr=limb(1, -24), legl=limb(-1, 24), armr=limb(1, 16, 16), arml=limb(-1, -16, 16)),
    # run: a skipping run, leaning in, arms out wide
    'run_a': P(0.02, body=torso(lean=10, tilt=5), head=torso(lean=-8, tilt=-4), legr=limb(1, 44), legl=limb(-1, -40), armr=limb(1, -45, 30), arml=limb(-1, 40, 30)),
    'run_up': P(0.12, body=torso(lean=10), head=torso(lean=-10), legr=limb(1, 10), legl=limb(-1, -30), armr=limb(1, -10, 45), arml=limb(-1, -10, 45)),
    'run_b': P(0.02, body=torso(lean=10, tilt=-5), head=torso(lean=-8, tilt=4), legr=limb(1, -40), legl=limb(-1, 44), armr=limb(1, 40, 30), arml=limb(-1, -45, 30)),
    # jump: arms up in a cheer, one heel kicked up behind
    'jump': P(body=torso(), head=torso(lean=-10), legr=limb(1, 18), legl=limb(-1, -60), armr=limb(1, 10, 145), arml=limb(-1, 10, 145)),
    # sit: legs out in front, hands in her lap, swinging her feet, head tilting
    'sit_a': P(-0.42, body=torso(lean=-4), head=torso(lean=4, tilt=9), legr=limb(1, 84), legl=limb(-1, 74), armr=limb(1, 42, -14), arml=limb(-1, 42, -14)),
    'sit_b': P(-0.42, body=torso(lean=-4), head=torso(lean=4, tilt=-9), legr=limb(1, 72), legl=limb(-1, 86), armr=limb(1, 42, -14), arml=limb(-1, 42, -14)),
    # cast (a buff): a little cheer
    'cast': P(0.03, body=torso(), head=torso(lean=-8), armr=limb(1, 20, 150), arml=limb(-1, 20, 150)),
    # wave at Cecil
    'wave_a': P(body=torso(tilt=-3), head=torso(tilt=8), armr=limb(1, 24, -22), arml=limb(-1, 10, 150)),
    'wave_b': P(body=torso(tilt=-3), head=torso(tilt=8), armr=limb(1, 24, -22), arml=limb(-1, 10, 118)),
    # ethereal: hovering, legs trailing, axe at the ready, wings beating
    'strike_up': P(0.12, body=torso(lean=-6, turn=-15), head=torso(lean=-6), legr=limb(1, -10), legl=limb(-1, -30), armr=limb(1, 165, 15), arml=limb(-1, 20, 60), **WINGS_UP),
    'strike_dn': P(0.0, body=torso(lean=16, turn=15), head=torso(lean=6), legr=limb(1, -30), legl=limb(-1, -10), armr=limb(1, 50, -8), arml=limb(-1, -10, 50), **WINGS_DN),
}


# ---- ethereal flight: 8 frames a beat, the outer halves a beat behind the inner (a ripple root to tip)
FLY_FRAMES = 8
for _i in range(FLY_FRAMES):
    _p = 2 * math.pi * _i / FLY_FRAMES
    _inner = 7 + 21 * math.sin(_p); _outer = 4 + 30 * math.sin(_p - 1.1); _lift = -6 * math.cos(_p)
    POSES[f'fly_{_i}'] = P(0.02 + 0.08 * math.sin(_p + 0.6), body=torso(lean=6, tilt=1.5 * math.sin(_p)), head=torso(lean=-4),
                          legr=limb(1, -14 - 5 * math.sin(_p + 1)), legl=limb(-1, -24 + 5 * math.sin(_p + 1)),
                          armr=limb(1, 30, 12), arml=limb(-1, 24, 48 + 4 * math.sin(_p)), **wings(_inner, _outer, _lift))


# ---- walking <-> running: one cycle, blended by how fast she moves (bucket 1 = a slow amble ... 8 = a full run)
def _slerp(a, b, t):
    d = sum(x * y for x, y in zip(a, b))
    if d < 0: b, d = tuple(-x for x in b), -d
    if d > 0.9995:
        r = tuple(x + t * (y - x) for x, y in zip(a, b)); n = math.sqrt(sum(x * x for x in r)); return tuple(x / n for x in r)
    th = math.acos(d); s0, s1 = math.sin((1 - t) * th) / math.sin(th), math.sin(t * th) / math.sin(th)
    return tuple(s0 * x + s1 * y for x, y in zip(a, b))


# (speed bucket: upper bound of v^2 in (blocks/tick * 1000)^2, typical speed v, run weight, step amplitude)
LOCO = [(2500, 0.035, 0.0, 0.55), (6400, 0.065, 0.0, 0.85), (12100, 0.095, 0.12, 1.0), (19600, 0.125, 0.32, 1.0),
        (28900, 0.155, 0.55, 1.0), (44100, 0.19, 0.8, 1.0), (72900, 0.24, 1.0, 1.0), (None, 0.30, 1.0, 1.05)]
WALK4, RUN4 = ('walk_a', 'walk_up', 'walk_b', 'walk_up'), ('run_a', 'run_up', 'run_b', 'run_up')
LOCO_STEP = {}            # bucket -> (phase per tick in thousandths of a frame, frame duration in ticks)
for _b, (_v2, _v, _w, _amp) in enumerate(LOCO, 1):
    _stride = 0.30 + 0.22 * _w                                        # blocks per quarter-cycle (a step = 2 quarters)
    LOCO_STEP[_b] = (round(1000 * _v / _stride), max(2, min(8, round(_stride / _v))))
    for _f in range(4):
        wk, rn = POSES[WALK4[_f]], POSES[RUN4[_f]]
        d = {k: _slerp(I, _slerp(wk[k], rn[k], _w), _amp) if k in PARTS else None for k in PARTS}
        d['_dy'] = (wk['_dy'] + (rn['_dy'] - wk['_dy']) * _w) * _amp
        POSES[f'loco_{_b}_{_f}'] = d


# ---- what each pose sends a part: its rotation, and its translation (the shared lift; the outer wing halves also reach
# out to their mid-joint, carried round by the inner half's turn)
def _qrot(q, v):
    x, y, z, w = q
    ux, uy, uz = x, y, z; vx, vy, vz = v
    cx, cy, cz = uy * vz - uz * vy + w * vx, uz * vx - ux * vz + w * vy, ux * vy - uy * vx + w * vz
    return (vx + 2 * (uy * cz - uz * cy), vy + 2 * (uz * cx - ux * cz), vz + 2 * (ux * cy - uy * cx))


def part_xf(pose, p):
    dy = pose['_dy']
    if p in ('wingro', 'winglo'):
        sx = 1 if p == 'wingro' else -1
        inner = pose['wingr' if sx > 0 else 'wingl']
        root, mid = PIVOT['wingr' if sx > 0 else 'wingl'], wing_mid(sx)
        U = RIG_SCALE / 16
        off = (-(mid[0] - root[0]) * U, (mid[1] - root[1]) * U, -(mid[2] - root[2]) * U)   # design -> display frame
        t = _qrot(inner, off)
        return qmul(inner, pose[p]), (t[0], t[1] + dy, t[2])
    return pose[p], (0.0, dy, 0.0)

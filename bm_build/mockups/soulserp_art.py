"""SOUL SERPENTS - King Omega's undead soldiers (a draft for approval: rig, textures, faces, poses; not in the pack).

From the owner's art: small ghastly serpents left over from the war between Apophiss and Omega - soldiers once, mischievous
now. Each is a round grey head on a teardrop body that thins into a ghost's tail, a blue soul flame burning at its tip; two
thin clawed arms; glowing yellow eyes (slanted, gleeful-wicked) and a purple mouth with little fangs and a long purple tongue
that loves to hang out; dark spikes on the head. Translucent like their king (the body texture is see-through; the eyes,
mouth, claws, spikes and flame are solid, the eyes and flame glow). Two-tone, as the art: a pale front, a darker side.

Three crests (the art's three soldiers - mixed in a squad so they aren't clones):
  a: three dark spikes swept back off the back of the head (the left and right soldiers)
  b: one tall dark horn on top, a short spike each side (the middle one)
  c: two big black horns curving back (the lone one)
Faces: cackle (the default - mouth open, tongue lolling), grin (a wide toothy grin, mouth shut), shriek (eyes wide, mouth
wide), sly (one eye narrowed).

Rig (rigkit): body - head - jaw - tongue; arms (upper, fore) off the body; tail1 - tail2 - tail3 - flame. Design units: facing
-z, his right +x; he floats (no feet), the tail's lowest point near y=0. About 1.8 blocks tall to the tip of a horn at RIG_SCALE 1.3 (a player's height)."""
import math
import os
import random
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from phase57_art import hexc
from rigkit import qs, el, seg, chain, I, mid, solve, qmul

PREFIX = 'ss_'
RIG_SCALE = 1.3
PIVOT = {'body': (0, 9.0, 0), 'head': (0, 15.4, 0.2), 'jaw': (0, 17.0, 2.8), 'tongue': (-0.8, 16.9, -3.8),
         'armr': (3.5, 13.4, -0.2), 'forer': (5.6, 10.8, -0.9), 'arml': (-3.5, 13.4, -0.2), 'forel': (-5.6, 10.8, -0.9),
         'tail1': (0, 6.2, 0.4), 'tail2': (2.2, 1.8, 0.6), 'tail3': (8.0, 2.2, -0.4), 'flame': (9.2, 6.6, -0.4)}
PARENT = {'body': None, 'head': 'body', 'jaw': 'head', 'tongue': 'jaw', 'armr': 'body', 'forer': 'armr', 'arml': 'body', 'forel': 'arml',
          'tail1': 'body', 'tail2': 'tail1', 'tail3': 'tail2', 'flame': 'tail3'}
PARTS = tuple(PIVOT)
PART_K = {}
CRESTS = ('a', 'b', 'c')
FACES = ('grin', 'shriek', 'sly')
UP, FRONT, SIDE = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0), (1.0, 0.0, 0.0)
GHOST_A = 200                      # (see-through, but solid enough that his own insides don't stripe him)


def HIDDEN(p, pose):
    return p == 'tongue' and pose.get('_face') == 'grin'


def model_name(p, pose, suffix=''):
    if p == 'head':
        face = f'_x{pose["_face"]}' if pose.get('_face') else ''
        return f'{PREFIX}head_{pose.get("_crest", "a")}{face}{suffix}'
    return f'{PREFIX}{p}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def _noise(base, seed, var=6, a=255):
    rnd = random.Random(seed); b = hexc(base)[:3]; im = Image.new('RGBA', (64, 64))
    for y in range(64):
        for x in range(64):
            d = rnd.randint(-var, var)
            im.putpixel((x, y), tuple(max(0, min(255, v + d)) for v in b) + (a,))
    return im


def _ghost(base, seed, a=GHOST_A):
    """the ghost's hide: smooth grey, a soft sheen, see-through"""
    im = _noise(base, seed, 4, a)
    for y in range(64):
        for x in range(20, 30):
            k = 1 - abs(x - 25) / 5
            p = im.getpixel((x, y)); im.putpixel((x, y), tuple(min(255, int(v + 26 * k)) for v in p[:3]) + (a,))
    return im


def _flame(seed, a=215):
    im = Image.new('RGBA', (64, 64)); rnd = random.Random(seed)
    for y in range(64):
        for x in range(64):
            t = abs(x - 32) / 32
            c = tuple(int(u * (1 - t) + v * t) for u, v in zip((226, 246, 255), (72, 162, 246)))
            j = rnd.randint(-12, 12)
            im.putpixel((x, y), tuple(max(0, min(255, v + j)) for v in c) + (a,))
    return im


def _eye(kind='angry', side=1):
    """a glowing yellow eye on nothing (the rest of the face shows round it): slanted down to the nose - angry-gleeful;
    'wide' round, 'narrow' a slit, 'happy' an upturned arc"""
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    Y, Yl = hexc('#fff45a'), hexc('#fffde8')
    if kind == 'wide':
        d.ellipse((2, 2, 13, 13), fill=Y); d.ellipse((4, 3, 7, 6), fill=Yl)
    elif kind == 'narrow':
        d.polygon([(1, 9), (14, 7), (14, 10), (1, 11)][::side] if side > 0 else [(14, 9), (1, 7), (1, 10), (14, 11)], fill=Y)
    elif kind == 'happy':
        d.arc((2, 4, 13, 15), 200, 340, fill=Y, width=3)
    else:                                                       # (the slant: high at the outer corner, down to the nose)
        pts = [(0, 3), (15, 9), (13, 14), (3, 14), (0, 9)]
        if side < 0: pts = [(15 - x, y) for x, y in pts]
        d.polygon(pts, fill=Y)
        d.line([(3, 7), (8, 8)] if side > 0 else [(12, 7), (7, 8)], fill=Yl, width=1)
    return im


def _grin():
    """a wide shut grin: a dark line, a row of sharp white teeth along it"""
    im = Image.new('RGBA', (32, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.arc((1, -10, 30, 13), 25, 155, fill=hexc('#2a2a30'), width=2)
    for x in range(5, 27, 3):
        y = 9 + int(2.4 * math.sin(math.pi * (x - 2) / 28))
        d.polygon([(x, y - 2), (x + 2, y - 2), (x + 1, y + 1)], fill=hexc('#f4f4f0'))
    return im


def textures():
    return {'ss_ghost': _ghost('#c8c8ca', 1501), 'ss_ghost_dk': _ghost('#8e8e92', 1502, GHOST_A + 10), 'ss_spike': _noise('#3c3c42', 1503, 5),
            'ss_spike_bk': _noise('#18181c', 1504, 4), 'ss_claw': _noise('#55555c', 1505, 4), 'ss_mouth': _noise('#3a1648', 1506, 6),
            'ss_tongue': _noise('#8e2cc0', 1507, 8), 'ss_fang': _noise('#f2f2ec', 1508, 3), 'ss_brow': _noise('#4a4a50', 1509, 4),
            'ss_ghost_fade': _ghost('#b4b4b8', 1511, 120), 'ss_flame': _flame(1510), 'ss_flame_core': Image.new('RGBA', (64, 64), (236, 250, 255, 240)),
            'ss_eye_r': _eye('angry', 1), 'ss_eye_l': _eye('angry', -1), 'ss_eye_wide': _eye('wide'), 'ss_eye_narrow_l': _eye('narrow', -1),
            'ss_grin': _grin()}


GLOW = {'ss_eye_r': 14, 'ss_eye_l': 14, 'ss_eye_wide': 14, 'ss_eye_narrow_l': 14, 'ss_flame': 15, 'ss_flame_core': 15}


# ---------------------------------------------------------------------------------------------------- models
def _two_tone(e, dark=('east', 'south')):
    """the art's two tones: the pale front, a darker band down his right side and back"""
    e = dict(e, faces={f: (dict(v, texture='#ss_ghost_dk') if f in dark and v['texture'] == '#ss_ghost' else v) for f, v in e['faces'].items()})
    return e


def _bands(rows, tex, pv, shift0=0.0):
    """a rounded solid of stacked boxes that never overlap (he's see-through: an inner face would show): (y0, y1, half-width,
    front z, back z) per band"""
    return [_two_tone(el((-w, y0, z0), (w, y1, z1), tex, pv, shift=(shift0 + 0.23 * i, 0.31 * i))) for i, (y0, y1, w, z0, z1) in enumerate(rows)]


def _round(rows, tex, pv, c=0.9, shift0=0.0):
    """a rounded solid: per band (y0, y1, half-width, front z, back z) two boxes - one full width, one full depth - so its
    corners are cut off (he's only lightly see-through: where they cross barely shows)"""
    out = []
    for i, (y0, y1, w, z0, z1) in enumerate(rows):
        out += [_two_tone(el((-w, y0, z0 + c), (w, y1, z1 - c), tex, pv, shift=(shift0 + 0.23 * i, 0.31 * i))),
                _two_tone(el((-w + c, y0, z0), (w - c, y1, z1), tex, pv, shift=(shift0 + 0.57 * i, 0.13 * i)))]
    return out


def models():
    M = {}
    def part(name, els):
        for e in els:
            g = max([GLOW.get(v['texture'][1:], 0) for v in e['faces'].values()] + [0])
            if g: e['light_emission'] = g
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)

    # ---- the body: a teardrop - narrow under the head, full in the middle, thinning into the tail
    pv = PIVOT['body']
    part('ss_body', _round([(12.4, 14.4, 2.5, -2.2, 2.3), (10.2, 12.4, 3.2, -2.6, 2.7), (8.0, 10.2, 3.3, -2.7, 2.8), (6.4, 8.0, 2.8, -2.4, 2.5),
                            (5.4, 6.4, 2.3, -2.0, 2.2)], 'ss_ghost', pv, 0.8))

    # ---- the tail: curling down, round and up behind him (to his right), thinning; the flame sits on its tip
    for name, pts, ws, tex in (('tail1', [(0, 6.2, 0.4), (0.3, 4.4, 0.6), (0.9, 2.8, 0.7), (2.2, 1.8, 0.6)], [4.2, 3.8, 3.4], 'ss_ghost'),
                               ('tail2', [(2.2, 1.8, 0.6), (4.0, 1.1, 0.4), (6.0, 1.2, 0.0), (8.0, 2.2, -0.4)], [3.2, 2.8, 2.4], 'ss_ghost'),
                               ('tail3', [(8.0, 2.2, -0.4), (8.9, 3.6, -0.6), (9.3, 5.0, -0.5), (9.2, 6.4, -0.4)], [2.1, 1.7, 1.3], 'ss_ghost_fade')):
        part(f'ss_{name}', [_two_tone(e) for e in chain(pts, ws, ws[0] * 0.9, tex, PIVOT[name], SIDE, hs=[w * 0.9 for w in ws])])

    # ---- the flame: soul fire burning up off the tail's tip
    pv = PIVOT['flame']; c = (9.2, 6.0, -0.4); rnd = random.Random(1520)
    fl = chain([c, (c[0], c[1] + 2.2, c[2]), (c[0] + 0.2, c[1] + 4.2, c[2])], [1.4, 0.7], 1.4, 'ss_flame_core', pv, FRONT, hs=[1.4, 0.7])
    for ring, (r, h, w, n) in enumerate(((1.8, 5.0, 1.3, 7), (1.1, 7.0, 1.0, 4))):
        for i in range(n):
            a = math.radians(360 * i / n + 25 * ring); ca, sa = math.cos(a), math.sin(a); hh = h * (0.8 + 0.4 * rnd.random())
            pts = [(c[0] + r * ca, c[1] - 0.3, c[2] + r * sa), (c[0] + 1.05 * r * ca, c[1] + 0.4 * hh, c[2] + 1.05 * r * sa),
                   (c[0] + 0.3 * r * ca + rnd.uniform(-0.4, 0.4), c[1] + hh, c[2] + 0.3 * r * sa)]
            fl += chain(pts, [w, 0.5 * w], w * 0.8, 'ss_flame', pv, (ca, 0.0, sa), ext=0.2, hs=[w * 0.8, w * 0.4])
    for k in range(3):
        x, z = c[0] + rnd.uniform(-1.0, 1.0), c[2] + rnd.uniform(-1.0, 1.0); y = c[1] + 7.6 + 1.1 * k
        fl.append(el((x - 0.25, y, z - 0.25), (x + 0.25, y + 0.6, z + 0.25), 'ss_flame', pv, ('y', 45, (x, y, z))))
    part('ss_flame', fl)

    # ---- the head: a big round dome over a wide face; a little hooked beak of a lip at the front; the eyes slanted under a
    #      brow ridge; the roof of the mouth purple, two fangs at its front corners; the crest
    pv = PIVOT['head']
    def head(crest='a', face=None):
        h = _round([(17.0, 22.8, 5.6, -5.4, 4.0), (22.8, 24.2, 5.0, -4.9, 3.6), (24.2, 25.2, 4.0, -4.0, 2.8),
                    (25.2, 25.8, 2.6, -2.8, 1.6)], 'ss_ghost', pv, 1.1, 0.1)
        h += [_two_tone(el((-0.85, 18.7, -6.0), (0.85, 19.9, -5.4), 'ss_ghost', pv)),                         # the little hooked beak
              _two_tone(el((-0.55, 18.1, -6.1), (0.55, 18.8, -5.7), 'ss_ghost_dk', pv))]
        # the eyes: big, glowing, slanted down to the beak (the scowl is in their shape - no brows), per face
        er, elf = {None: ('ss_eye_r', 'ss_eye_l'), 'grin': ('ss_eye_r', 'ss_eye_l'), 'shriek': ('ss_eye_wide', 'ss_eye_wide'),
                   'sly': ('ss_eye_r', 'ss_eye_narrow_l')}[face]
        for sx, t in ((1, er), (-1, elf)):
            h.append(el((sx * 2.65 - 2.3, 19.8, -5.47), (sx * 2.65 + 2.3, 23.0, -5.41), t, pv, faces=('north',), uv={'north': [0, 0, 16, 16]}))
        # the mouth: wide - its purple roof and two fangs at the front (the jaw drops away below)
        h += [el((-4.9, 16.95, -5.0), (4.9, 17.0, 3.4), 'ss_mouth', pv, faces=('down',))]
        for sx in (1, -1):
            h.append(el((sx * 3.4 - 0.45, 15.8, -5.35), (sx * 3.4 + 0.45, 17.0, -4.75), 'ss_fang', pv))
        if face == 'grin':
            h.append(el((-4.6, 16.4, -5.47), (4.6, 18.6, -5.41), 'ss_grin', pv, faces=('north',), uv={'north': [0, 0, 16, 16]}))
        # the crest
        if crest == 'a':                                                    # three broad dark spikes swept back off the back of his head
            for i, (y, z, L) in enumerate(((24.8, 1.4, 5.0), (22.8, 3.6, 4.4), (20.2, 4.2, 3.4))):
                h += chain([(0, y, z), (0, y + L * 0.35, z + L * 0.65), (0, y + L * 0.5, z + L * 1.25)], [3.0, 1.4], 1.6, 'ss_spike', pv, SIDE, ext=0.2,
                           hs=[1.6, 0.7])
        elif crest == 'b':
            h += chain([(0, 25.0, -0.2), (0, 28.6, 0.2), (0, 31.6, 0.8)], [2.0, 0.9], 2.0, 'ss_spike', pv, FRONT, hs=[2.0, 0.9])
            for sx in (1, -1):
                h += chain([(sx * 4.4, 23.0, 0.6), (sx * 5.8, 25.0, 1.6), (sx * 6.4, 26.4, 2.8)], [1.4, 0.6], 1.4, 'ss_spike', pv, FRONT, hs=[1.4, 0.6])
        else:
            for sx in (1, -1):
                h += chain([(sx * 2.2, 24.4, -0.6), (sx * 3.0, 28.0, 0.4), (sx * 3.2, 31.0, 2.4), (sx * 2.8, 32.6, 4.6)], [2.2, 1.6, 0.8], 2.2, 'ss_spike_bk', pv,
                           FRONT, hs=[2.2, 1.6, 0.8])
            h += chain([(0, 21.4, 3.8), (0, 23.2, 6.0), (0, 23.8, 7.6)], [1.6, 0.7], 0.7, 'ss_spike_bk', pv, SIDE, ext=0.2)
        return h
    for cr in CRESTS:
        part(f'ss_head_{cr}', head(cr))
        for f in FACES:
            part(f'ss_head_{cr}_x{f}', head(cr, f))

    # ---- the jaw: hinged at the back, its purple floor and two little fangs; dropped open it shows the whole purple mouth
    pv = PIVOT['jaw']
    jaw = _round([(13.8, 14.6, 3.4, -3.6, 2.2), (14.6, 15.6, 4.6, -4.7, 3.3), (15.6, 16.95, 5.5, -5.3, 3.9)], 'ss_ghost', pv, 1.0, 0.4)   # (the round chin)
    jaw += [el((-4.6, 16.93, -4.6), (4.6, 17.0, 3.2), 'ss_mouth', pv, faces=('up',))]
    for sx in (1, -1):
        jaw.append(el((sx * 2.6 - 0.3, 16.95, -5.0), (sx * 2.6 + 0.3, 17.7, -4.6), 'ss_fang', pv))
    part('ss_jaw', jaw)

    # ---- the tongue: long, purple, forked - out over his lip and hanging (the poses swing and curl it)
    pv = PIVOT['tongue']
    tg = chain([(-0.8, 17.1, -3.8), (-1.2, 17.2, -5.8), (-1.8, 16.4, -7.0), (-2.6, 14.8, -7.4), (-3.4, 13.6, -7.0)], [1.2, 1.1, 1.0, 0.9], 0.5, 'ss_tongue', pv, UP)
    tg += chain([(-3.4, 13.6, -7.0), (-3.0, 12.6, -7.2)], [0.45], 0.4, 'ss_tongue', pv, UP) + chain([(-3.4, 13.6, -7.0), (-4.2, 12.8, -6.8)], [0.45], 0.4, 'ss_tongue', pv, UP)
    part('ss_tongue', tg)

    # ---- the arms: thin, the elbow bent, three long claws (dark tips)
    for sx in (1, -1):
        s = 'r' if sx > 0 else 'l'; pv = PIVOT['arm' + s]; fv = PIVOT['fore' + s]
        part('ss_arm' + s, [_two_tone(e) for e in chain([pv, fv], [1.5], 1.5, 'ss_ghost', pv, FRONT, ext=0.3)])
        wr = (sx * 6.0, 8.0, -2.6)
        f = [_two_tone(e) for e in chain([fv, wr], [1.3], 1.3, 'ss_ghost', fv, FRONT, ext=0.25)]
        f.append(_two_tone(el((wr[0] - 0.8, wr[1] - 0.9, wr[2] - 0.8), (wr[0] + 0.8, wr[1] + 0.3, wr[2] + 0.8), 'ss_ghost', fv)))
        for u in (-0.55, 0.0, 0.55):
            base = (wr[0] + u, wr[1] - 0.8, wr[2] - 0.4)
            f += chain([base, (base[0] + u * 0.4, base[1] - 1.4, base[2] - 0.6), (base[0] + u * 0.6, base[1] - 2.4, base[2] - 0.2)], [0.35, 0.25], 0.35, 'ss_claw', fv, FRONT, ext=0.1)
        part('ss_fore' + s, f)
    return M


# ---------------------------------------------------------------------------------------------------- poses
# body: +x leans forward, +y turns to his left, +z rolls to his right; head +x nods down; jaw +x opens; tongue +x down, +y to
# his left; arms -x swing forward/up, -z (right) / +z (left) out; tail +x lifts it, +y swings it to his right.
def P(**kw):
    return kw


def arm(sx, fwd=0.0, out=0.0):
    return qs(('x', -fwd), ('z', -out * sx))


HOVER = 3.0
POSES = {
    # idle: bobbing in the air, a lazy cackle, tongue hanging, the tail curling (a/b)
    'idle_a': P(_off=(0, HOVER, 0), jaw=qs(('x', 22)), head=qs(('z', -6)), armr=arm(1, 10, 24), forer=arm(1, 30), arml=arm(-1, 14, 20), forel=arm(-1, 40),
                tail1=qs(('y', 10)), tail2=qs(('y', 8)), tongue=qs(('y', 6))),
    'idle_b': P(_off=(0, HOVER + 1.4, 0), jaw=qs(('x', 18)), head=qs(('z', 4), ('y', 8)), armr=arm(1, 16, 20), forer=arm(1, 44), arml=arm(-1, 8, 24), forel=arm(-1, 30),
                tail1=qs(('y', -8)), tail2=qs(('y', -12)), tail3=qs(('y', 10)), tongue=qs(('y', -8), ('x', 10))),
    # float (on the move): leaning in, the tail streaming behind, arms trailing
    'float_a': P(_off=(0, HOVER + 0.6, 0), body=qs(('x', 22), ('z', 6)), head=qs(('x', -18)), jaw=qs(('x', 14)), armr=arm(1, -30, 16), forer=arm(1, 20), arml=arm(-1, -20, 16), forel=arm(-1, 20),
                 tail1=qs(('x', -30), ('y', 14)), tail2=qs(('x', -10), ('y', -16)), tail3=qs(('y', -10)), tongue=qs(('x', -20))),
    'float_b': P(_off=(0, HOVER + 1.6, 0), body=qs(('x', 22), ('z', -6)), head=qs(('x', -18)), jaw=qs(('x', 10)), armr=arm(1, -20, 16), forer=arm(1, 20), arml=arm(-1, -30, 16), forel=arm(-1, 20),
                 tail1=qs(('x', -30), ('y', -14)), tail2=qs(('x', -10), ('y', 16)), tail3=qs(('y', 10)), tongue=qs(('x', -24), ('y', 10))),
    # the cackle: head thrown back, jaw wide, claws up and grasping, tongue flailing
    'cackle': P(_off=(0, HOVER + 0.8, 0), body=qs(('x', -12)), head=qs(('x', -24)), jaw=qs(('x', 40)), armr=arm(1, 70, 40), forer=arm(1, 70), arml=arm(-1, 80, 30), forel=arm(-1, 60),
                tail1=qs(('x', 20)), tail2=qs(('y', 20)), tongue=qs(('x', -30), ('y', 20))),
    # the grin: the art's right soldier - mouth shut on a toothy grin, arms tucked in, head cocked (plotting something)
    'grin': P(_face='grin', _off=(0, HOVER, 0), head=qs(('z', 12), ('y', -10)), armr=arm(1, 30, 6), forer=arm(1, 80), arml=arm(-1, 30, 6), forel=arm(-1, 80),
              tail1=qs(('y', 20)), tail2=qs(('y', 30)), tail3=qs(('y', 30))),
    # sneak: low, hunched, claws together - tiptoeing on the air up behind you
    'sneak': P(_face='sly', _off=(0, HOVER - 1.6, 0), body=qs(('x', 28)), head=qs(('x', -20), ('y', 10)), jaw=qs(('x', 6)), armr=arm(1, 60, -10), forer=arm(1, 70), arml=arm(-1, 60, -10), forel=arm(-1, 70),
               tail1=qs(('x', -10)), tail2=qs(('x', 10)), tongue=qs(('x', 20))),
    # boo!: popping up big - arms flung wide, eyes wide, mouth wide
    'boo': P(_face='shriek', _off=(0, HOVER + 3.0, 0), body=qs(('x', -6)), head=qs(('x', -10)), jaw=qs(('x', 46)), armr=arm(1, 90, 80), forer=arm(1, 10), arml=arm(-1, 90, 80), forel=arm(-1, 10),
              tail1=qs(('x', 30)), tail2=qs(('x', 20)), tongue=qs(('x', -40))),
    # the swipe (attack): wound up, then raked across
    'swipe_up': P(_off=(0, HOVER, 0), body=qs(('y', -20), ('x', 6)), head=qs(('y', 12)), jaw=qs(('x', 30)), armr=arm(1, 130, 30), forer=arm(1, 40), arml=arm(-1, 20, 30), forel=arm(-1, 40),
                  tail1=qs(('y', -20)), tail2=qs(('y', 10)), tongue=qs(('y', 20))),
    'swipe': P(_off=(0, HOVER - 0.4, -1.0), body=qs(('y', 24), ('x', 16)), head=qs(('y', -14), ('x', -10)), jaw=qs(('x', 36)), armr=arm(1, 80, -20), forer=arm(1, 10), arml=arm(-1, 30, 40), forel=arm(-1, 50),
               tail1=qs(('y', 24)), tail2=qs(('y', -10)), tongue=qs(('y', -20))),
    # the bite: a lunge, jaw gaping, the tongue lashing out first
    'lunge': P(_face='shriek', _off=(0, HOVER - 1.0, -3.0), body=qs(('x', 34)), head=qs(('x', -30)), jaw=qs(('x', 50)), armr=arm(1, 80, 20), forer=arm(1, 20), arml=arm(-1, 80, 20), forel=arm(-1, 20),
               tail1=qs(('x', -20)), tail2=qs(('x', -10)), tongue=qs(('x', -60))),
    # the soul spit: the tail whipped up over the head and the flame flicked forward (the game throws a little fireball)
    'flick_up': P(_off=(0, HOVER, 0), body=qs(('x', -8)), head=qs(('x', -6)), jaw=qs(('x', 20)), armr=arm(1, 20, 30), forer=arm(1, 40), arml=arm(-1, 20, 30), forel=arm(-1, 40),
                  tail1=qs(('x', 60)), tail2=qs(('x', 60)), tail3=qs(('x', 40))),
    'flick': P(_off=(0, HOVER - 0.4, 0), body=qs(('x', 18)), head=qs(('x', -16)), jaw=qs(('x', 30)), armr=arm(1, 30, 30), forer=arm(1, 30), arml=arm(-1, 30, 30), forel=arm(-1, 30),
               tail1=qs(('x', 90)), tail2=qs(('x', 50)), tail3=qs(('x', 30))),
    # hurt / dissolving: reeling, then sagging as it fades into wisps
    'hurt': P(_face='shriek', _off=(0, HOVER + 0.6, 1.0), body=qs(('x', -20), ('z', 10)), head=qs(('x', -16), ('z', 12)), jaw=qs(('x', 28)), armr=arm(1, 40, 60), forer=arm(1, 30),
              arml=arm(-1, 40, 60), forel=arm(-1, 30), tail1=qs(('x', 20)), tongue=qs(('x', -20))),
    'fade': P(_off=(0, 0.4, 0), body=qs(('x', 26), ('z', -10)), head=qs(('x', 24), ('z', -8)), jaw=qs(('x', 14)), armr=arm(1, -6, 4), forer=arm(1, 4), arml=arm(-1, -6, 4), forel=arm(-1, 4),
              tail1=qs(('x', -20)), tail2=qs(('y', 20)), tongue=qs(('x', 40))),
    # saluting their king (they were soldiers once - and they still mean it, mostly)
    'salute': P(_face='grin', _off=(0, HOVER + 0.4, 0), body=qs(('x', -4)), head=qs(('x', -8)), armr=arm(1, 150, 50), forer=arm(1, 100), arml=arm(-1, 0, 6), forel=arm(-1, 10),
                tail1=qs(('x', -10)), tail2=qs(('x', 10))),
}


def _upright(pose, tilt=6.0):
    """fire rises: the flame's own turn undoes the body's and the tail's"""
    q = solve(PIVOT, PARENT, dict(pose, flame=I))['tail3'][0]
    return qmul((-q[0], -q[1], -q[2], q[3]), qs(('x', tilt)))


for _p in POSES.values():
    _p['flame'] = _upright(_p)
POSES['float_m'] = mid(POSES['float_a'], POSES['float_b'])
for _p in (POSES['float_m'],):
    _p['flame'] = _upright(_p)
DRAFT = ['idle_a', 'float_a', 'cackle', 'grin', 'sneak', 'boo', 'swipe_up', 'swipe', 'lunge', 'flick', 'hurt', 'fade', 'salute']
ANIMS = {'idle': [('idle_a', 14), ('idle_b', 14), ('idle_a', 14)],
         'float': [('float_a', 6), ('float_m', 6), ('float_b', 6), ('float_m', 6), ('float_a', 6)],
         'cackle': [('idle_a', 6), ('cackle', 6), ('idle_b', 4), ('cackle', 4), ('idle_a', 6)],
         'sneak_boo': [('sneak', 12), ('sneak', 10), ('boo', 3), ('boo', 10), ('cackle', 8), ('idle_a', 8)],
         'swipe': [('idle_a', 6), ('swipe_up', 6), ('swipe', 3), ('idle_a', 6)],
         'lunge': [('idle_a', 6), ('sneak', 6), ('lunge', 3), ('idle_a', 8)],
         'flick': [('idle_a', 6), ('flick_up', 8), ('flick', 3), ('idle_a', 8)],
         'fade': [('hurt', 4), ('hurt', 8), ('fade', 14), ('fade', 8)],
         'salute': [('idle_a', 8), ('salute', 8), ('salute', 14), ('idle_a', 8)]}

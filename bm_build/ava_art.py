"""Queen Ava (2.87): Emma's mother - from the owner's art. A gentle, shy-smiling queen: brown hair swept across her brow and down
to the jaw, a round bun high on her left; big teal eyes, a blush and a few freckles; a gold crown set with blue stones, a green
one at the front and a violet diamond on top. A navy gown: the high pointed collar, pale-blue shoulder caps, the kingdom's
teardrop insignia (a magenta gem in it) on the bodice, a dark sash at the waist, long sleeves and long white gloves with
scalloped cuffs; a full ballgown skirt to the floor, open at the front over a pale aqua underskirt banded with lace.

Her GHOSTLY FORM (she was killed by Apophiss): the same queen, every texture turned to pale, see-through spectral blue
(the '_g' models: each part's model with its '_g' textures).

A rigkit rig like the Neighbor's: body (the skirt with it), head (a model per expression - the face painted on), arms bent at
the elbow, the feet under the hem. Design units: feet at y=0, facing -z, her right is +x."""
import math
import random
from PIL import Image, ImageDraw

from phase57_art import hexc
from tullius_art import _noise, _shine
from rigkit import qs, el, chain
import royal_face as RF

PREFIX = 'av_'
RIG_SCALE = 0.92
PIVOT = {'body': (0, 13.0, 0), 'legr': (1.5, 6.0, 0), 'legl': (-1.5, 6.0, 0), 'head': (0, 24.4, 0),
         'armr': (4.2, 23.0, 0), 'forer': (4.7, 18.6, 0), 'arml': (-4.2, 23.0, 0), 'forel': (-4.7, 18.6, 0)}
PARENT = {'body': None, 'legr': None, 'legl': None, 'head': 'body', 'armr': 'body', 'forer': 'armr', 'arml': 'body', 'forel': 'arml'}
PARTS = tuple(PIVOT)
PART_K = {}
FACES = ('happy', 'shout', 'hurt', 'blink')
SKIN, SKIN_DK, SKIN_LT = '#f4c6a4', '#d89c7c', '#ffe0c8'
HAIR, HAIR_DK, HAIR_LT = '#6a3e1e', '#45260f', '#93603a'
NAVY, NAVY_DK, NAVY_LT = '#2e5f8e', '#1b3c66', '#4f86b8'
ICE, ICE_DK = '#9ad8e6', '#6aaec4'
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)
GHOST = ('#0e2a4a', '#5aa8e0', '#e8fbff')            # the spectre's ramp: dark - mid - light
GHOST_A = 150                                       # (her see-through: alpha out of 255)


def HIDDEN(p, pose):
    return False


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    form = '_g' if pose.get('_g') else ''
    return f'{PREFIX}{p}{face}{form}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def _px(im):
    return im.load()


def ghostly(im, alpha=GHOST_A):
    """a texture as the spectre wears it: its brightness through the ghost ramp, see-through (the eyes and gold stay a touch
    stronger - the darkest and brightest texels keep more of their alpha)"""
    o = im.convert('RGBA').copy(); px = o.load()
    s = [hexc(c)[:3] for c in GHOST]
    for y in range(o.height):
        for x in range(o.width):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            L = (0.3 * r + 0.59 * g + 0.11 * b) / 255
            L = 0.12 + 0.86 * L
            c = tuple(int(s[0][i] + (s[1][i] - s[0][i]) * L / 0.5) for i in range(3)) if L < 0.5 else \
                tuple(int(s[1][i] + (s[2][i] - s[1][i]) * (L - 0.5) / 0.5) for i in range(3))
            k = alpha + int(60 * abs(L - 0.55) / 0.45)
            px[x, y] = c + (min(a, max(70, min(235, k))),)
    return o


def _cloth(base, seed, dark, light, folds=5, var=4):
    """satin: vertical folds - a dark crease with a light sheen beside it"""
    im = _noise(base, seed, var); d = ImageDraw.Draw(im); rnd = random.Random(seed + 7)
    for _ in range(folds):
        x = rnd.randrange(2, 62)
        d.line((x, 0, x + rnd.randint(-3, 3), 63), fill=hexc(dark), width=2)
        d.line((x + 2, 0, x + 2 + rnd.randint(-3, 3), 63), fill=hexc(light), width=1)
    return im


def _skirt(seed):
    """the ballgown's skirt: deep navy satin, long folds and a scatter of short brush-strokes (as the art's texture)"""
    im = _cloth(NAVY, seed, NAVY_DK, NAVY_LT, folds=6); d = ImageDraw.Draw(im); rnd = random.Random(seed + 3)
    for _ in range(70):
        x, y = rnd.randrange(64), rnd.randrange(64)
        d.line((x, y, x + rnd.randint(-2, 2), y + rnd.randint(2, 5)), fill=hexc(rnd.choice([NAVY_DK, '#264f7c', '#3a6c9c'])))
    return im


def _under(seed):
    """the underskirt: pale aqua, three bands of lace across it"""
    im = _noise('#bfe6e6', seed, 3); d = ImageDraw.Draw(im)
    lace, lace_dk = hexc('#7ab6bc'), hexc('#5a969c')
    for y0 in (6, 30, 54):
        d.line((0, y0, 63, y0), fill=lace_dk, width=1); d.line((0, y0 + 6, 63, y0 + 6), fill=lace_dk, width=1)
        for x in range(0, 64, 6):
            d.arc((x, y0 - 2, x + 6, y0 + 4), 0, 180, fill=lace)
            d.point((x + 3, y0 + 3), fill=lace_dk)
        for x in range(0, 64, 3):
            d.point((x, y0 + 5), fill=lace)
    return im


def _bodice(seed):
    """the bodice's front: navy, the pointed high collar's V at the top, the insignia - a pale teardrop with two horns and a
    magenta gem - on the breast, a soft fold under the bust"""
    im = _cloth(NAVY, seed, NAVY_DK, NAVY_LT, folds=2); d = ImageDraw.Draw(im)
    d.polygon([(22, 0), (32, 12), (42, 0)], fill=hexc(NAVY_DK))                    # the collar's V, in shadow
    d.line((22, 0, 32, 12), fill=hexc('#14304f'), width=2); d.line((42, 0, 32, 12), fill=hexc('#14304f'), width=2)
    pale, line = hexc('#e8fbff'), hexc('#7ab8d0')
    d.ellipse((27, 21, 37, 33), outline=pale, width=2)                              # the teardrop...
    d.polygon([(28, 23), (32, 14), (36, 23)], outline=pale)
    d.line((32, 14, 30, 22), fill=pale); d.line((32, 14, 34, 22), fill=pale)
    d.ellipse((30, 25, 34, 29), fill=hexc('#d0287a'))                               # ...and the gem
    d.point((31, 26), fill=hexc('#ff9ad0'))
    d.arc((16, 34, 48, 46), 200, 340, fill=hexc(NAVY_DK), width=2)                  # under the bust
    d.line((0, 62, 63, 62), fill=line)
    return im


def _glove(seed):
    im = _noise('#f2fbff', seed, 3); d = ImageDraw.Draw(im)
    for x in range(0, 64, 9):
        d.line((x, 0, x + 2, 63), fill=hexc('#cfe4ee'))
    return im


def _cuff(seed):
    """the glove's scalloped cuff: white with pale-blue points along its top edge"""
    im = _noise('#f2fbff', seed, 3); d = ImageDraw.Draw(im)
    for x in range(0, 64, 8):
        d.polygon([(x, 0), (x + 4, 10), (x + 8, 0)], fill=hexc('#cfe8f2'))
    d.line((0, 62, 63, 62), fill=hexc('#b8d4e0'), width=2)
    return im


def _gold(seed):
    im = _noise('#e8c33a', seed, 6); px = im.load()
    for y in range(64):
        for x in range(64):
            if (x + y) % 11 == 0: px[x, y] = hexc('#fff3a8')
            elif (x - 2 * y) % 17 == 0: px[x, y] = hexc('#a8841a')
    return im


def _gem(base, light, dark, seed):
    im = _noise(base, seed, 6); d = ImageDraw.Draw(im)
    d.polygon([(0, 0), (63, 0), (32, 63)], fill=hexc(dark))
    d.polygon([(16, 0), (48, 0), (32, 40)], fill=hexc(base))
    d.ellipse((20, 6, 34, 20), fill=hexc(light))
    return im


def _hair(seed):
    im = _noise(HAIR, seed, 5); rnd = random.Random(seed); d = ImageDraw.Draw(im)
    for _ in range(26):
        x = rnd.randrange(64)
        d.line((x, rnd.randrange(64), x + rnd.randint(-4, 4), rnd.randrange(64)), fill=hexc(rnd.choice([HAIR_DK, HAIR_LT, '#5a321a'])))
    return im


def _face(kind=None):
    """the front of her head, 64 x 64, from the art: brown bangs swept across her brow (to her left - the viewer's right); thin
    brows; big teal eyes - a dark upper lash, a teal iris with a dark pupil and two white glints, a small lower lash - looking
    straight out; a blush on each cheek and a few freckles; a small nose and a soft closed smile."""
    im = _noise(SKIN, 1601, 4); d = ImageDraw.Draw(im)
    ink, white, lash = hexc('#2a1810'), hexc('#ffffff'), hexc('#24140c')
    hair, hair_dk, hair_lt = hexc(HAIR), hexc(HAIR_DK), hexc(HAIR_LT)
    # the bangs: a heavy sweep from her right temple down across to her left cheek
    d.polygon([(0, 0), (63, 0), (63, 26), (58, 20), (50, 15), (40, 13), (28, 12), (16, 12), (8, 14), (0, 18)], fill=hair)
    d.polygon([(0, 14), (6, 13), (3, 28), (0, 34)], fill=hair)                          # a lock down her right temple
    d.polygon([(54, 16), (63, 22), (63, 40), (58, 30)], fill=hair)                      # the sweep's end at her left cheek
    for x in range(2, 62, 5):
        d.line((x, 0, x + 6, 11), fill=hair_dk if x % 2 else hair_lt)
    d.line((8, 14, 28, 12, 50, 15, 62, 25), fill=hair_dk, width=1)
    # the brows
    for sx in (-1, 1):
        cx = 32 + sx * 13
        d.line((cx - 5, 21, cx + 5, 20) if sx < 0 else (cx - 5, 20, cx + 5, 21), fill=hexc('#5a3218'), width=1)
    # the eyes
    E = ((19, 30), (45, 30))
    for cx, cy in E:
        if kind == 'happy':
            d.arc((cx - 7, cy - 4, cx + 7, cy + 6), 200, 340, fill=lash, width=3); continue
        if kind == 'blink':
            d.arc((cx - 7, cy - 6, cx + 7, cy + 4), 30, 150, fill=lash, width=2); continue
        if kind == 'hurt':
            d.line((cx - 6, cy - 2, cx + 6, cy + 2) if cx < 32 else (cx - 6, cy + 2, cx + 6, cy - 2), fill=lash, width=2)
            d.line((cx - 5, cy + 3, cx + 5, cy + 3), fill=lash, width=1); continue
        ry = 8 if kind == 'shout' else 7
        d.ellipse((cx - 7, cy - ry, cx + 7, cy + ry - 1), fill=white)
        d.ellipse((cx - 5, cy - ry + 2, cx + 5, cy + ry - 1), fill=hexc('#1a8a90'))         # the iris
        d.ellipse((cx - 4, cy - ry + 4, cx + 4, cy + ry - 2), fill=hexc('#2ac0c0'))
        d.ellipse((cx - 3, cy + 1, cx + 3, cy + ry - 2), fill=hexc('#7ae8e0'))
        d.ellipse((cx - 2, cy - 2, cx + 2, cy + 3), fill=hexc('#0c3a40'))                   # the pupil
        d.rectangle((cx - 4, cy - 4, cx - 2, cy - 2), fill=white); d.point((cx + 2, cy + 3), fill=white)
        d.arc((cx - 8, cy - ry - 1, cx + 8, cy + ry), 200, 340, fill=lash, width=2)         # the upper lash
        d.line((cx + (7 if cx > 32 else -7), cy - 3, cx + (9 if cx > 32 else -9), cy - 5), fill=lash, width=1)
        d.arc((cx - 6, cy - 2, cx + 6, cy + ry + 1), 60, 120, fill=hexc('#8a5a40'))
    # the blush and the freckles
    for cx in (12, 52):
        d.ellipse((cx - 5, 40, cx + 5, 44), fill=hexc('#f4a0a0'))
    rnd = random.Random(1602)
    for cx in (14, 50):
        for _ in range(5):
            d.point((cx + rnd.randint(-5, 5), 38 + rnd.randint(-1, 3)), fill=hexc('#c07a5a'))
    # the nose and the mouth
    d.line((32, 37, 33, 41), fill=hexc(SKIN_DK)); d.point((31, 42), fill=hexc(SKIN_DK))
    if kind == 'shout':
        d.ellipse((28, 47, 36, 55), fill=hexc('#7a2a2a'), outline=ink); d.ellipse((30, 51, 34, 54), fill=hexc('#e07070'))
    elif kind == 'happy':
        d.chord((25, 44, 39, 54), 0, 180, fill=hexc('#7a2a2a'), outline=ink); d.rectangle((27, 49, 37, 50), fill=white)
    elif kind == 'hurt':
        d.arc((26, 49, 38, 56), 200, 340, fill=ink, width=2)
    else:
        d.arc((26, 44, 38, 51), 30, 150, fill=ink, width=1)                                 # the soft smile
        d.point((26, 46), fill=ink)
    return im


def textures():
    T = {'av_skin': _noise(SKIN, 1603, 4), 'av_skin_dk': _noise(SKIN_DK, 1604, 4), 'av_hair': _hair(1605), 'av_hair_dk': _noise(HAIR_DK, 1619, 4),
         'av_navy': _cloth(NAVY, 1606, NAVY_DK, NAVY_LT, folds=3), 'av_navy_dk': _noise(NAVY_DK, 1607, 4), 'av_bodice': _bodice(1608),
         'av_skirt': _skirt(1609), 'av_under': _under(1610), 'av_ice': _shine(ICE, '#e8fbff', 1611), 'av_glove': _glove(1612), 'av_cuff': _cuff(1613),
         'av_gold': _gold(1614), 'av_blue': _gem('#2a8ae0', '#bfe8ff', '#1a4a9a', 1615), 'av_green': _gem('#2aa060', '#bff0d0', '#14603a', 1616),
         'av_violet': _gem('#b02ae0', '#f0c0ff', '#5a1490', 1617), 'av_shoe': _shine('#1b3c66', '#5a86b8', 1618), 'av_face': RF.ava_face()}
    for k in FACES:
        T[f'av_face_{k}'] = RF.ava_face(k)
    for k in list(T):
        T[f'{k}_g'] = ghostly(T[k])
    return T


# ---------------------------------------------------------------------------------------------------- models
def _ghost_els(els):
    out = []
    for e in els:
        e2 = dict(e, faces={f: dict(v, texture=v['texture'] + '_g') for f, v in e['faces'].items()})
        out.append(e2)
    return out


def models():
    M = {}
    def part(name, els):
        for nm, ee in ((name, els), (name + '_g', _ghost_els(els))):
            used = sorted({e['faces'][f]['texture'][1:] for e in ee for f in e['faces']})
            M[nm] = ({t: f'bm:block/{t}' for t in used}, ee)

    # ---- the body: the ballgown - a skirt in widening tiers to the floor, open at the front over the laced underskirt; the
    #      dark sash; the bodice (the insignia on it); the pale shoulder caps; the high pointed collar, the neck
    pv = PIVOT['body']
    body = []
    tiers = []
    for i in range(9):                                                                      # (9 tiers: a bell from the sash to the floor)
        t0, t1 = i / 9, (i + 1) / 9
        y1, y0 = 13.4 - t0 * 13.1, 13.4 - t1 * 13.1 - 0.15
        f = lambda t: t ** 0.8
        tiers.append((max(0.3, y0), y1, 3.4 + 3.8 * f(t1), 2.7 + 2.9 * f(t1)))
    for i, (y0, y1, hw, hd) in enumerate(tiers):
        gap = 0.45 + 0.28 * i                                                               # the opening at the front, widening
        body += [el((-hw, y0, -hd + 0.6), (hw, y1, hd), 'av_skirt', pv, shift=(0.2 * i, 0.3 * i)),
                 el((-hw, y0, -hd), (-gap, y1, -hd + 0.6), 'av_skirt', pv, shift=(0.1 * i, 0.5)),
                 el((gap, y0, -hd), (hw, y1, -hd + 0.6), 'av_skirt', pv, shift=(0.4 * i, 0.5)),
                 el((-gap, y0, -hd + 0.3), (gap, y1, -hd + 0.45), 'av_under', pv, faces=('north',),
                    uv={'north': [8 - gap * 1.5, 16 - (y1 / 13.4) * 16, 8 + gap * 1.5, 16 - (y0 / 13.4) * 16]})]
    body += [el((-7.15, 0.25, -5.65), (7.15, 0.55, 5.65), 'av_navy_dk', pv),                    # the hem's edge
             el((-3.3, 13.2, -2.5), (3.3, 14.4, 2.5), 'av_navy_dk', pv),                          # the sash
             el((-3.4, 14.2, -2.4), (3.4, 21.6, 2.4), 'av_navy', pv, shift=(0.3, 0.2)),           # the bodice
             el((-3.4, 14.2, -2.42), (3.4, 21.6, -2.4), 'av_bodice', pv, faces=('north',), uv={'north': [0, 0, 16, 16]}),
             el((-3.6, 21.2, -2.6), (3.6, 22.6, 2.6), 'av_navy', pv),                             # the shoulders
             el((-1.3, 22.4, -1.3), (1.3, 24.9, 1.3), 'av_skin', pv),                             # the neck
             el((-1.9, 22.4, -1.9), (1.9, 24.0, -1.2), 'av_navy_dk', pv),                         # the high collar: front...
             el((-1.9, 22.4, 1.2), (1.9, 24.6, 1.9), 'av_navy_dk', pv),                           # ...back
             el((-1.95, 22.4, -1.9), (-1.3, 24.4, 1.9), 'av_navy_dk', pv), el((1.3, 22.4, -1.9), (1.95, 24.4, 1.9), 'av_navy_dk', pv)]
    for sx in (-1, 1):                                                                          # the pale shoulder caps
        body.append(el((sx * 2.4 - 1.6, 21.6, -2.8), (sx * 2.4 + 1.6, 22.9, 2.8), 'av_ice', pv, rot=('z', -12 * sx, (sx * 2.4, 22.2, 0))))
        body.append(el((sx * 3.6 - 0.9, 20.6, -2.7), (sx * 3.6 + 0.9, 22.2, 2.7), 'av_ice', pv, rot=('z', -40 * sx, (sx * 3.6, 21.4, 0))))
    part('av_body', body)

    # ---- the head: Emma's head (9 x 8 x 8, the face in Emma's own pixel scale); a chin-length bob - the bangs swept across her
    #      brow to her left, a longer lock at her left cheek, a short one at her right; the bun high on her left; the crown tipped
    #      toward her right. (+x is her right: the viewer's left from the front.)
    pv = PIVOT['head']
    HB = pv[1]; HT = HB + 8.0
    def head(face=None):
        tex = 'av_face' if face is None else f'av_face_{face}'
        hr = lambda fr, to, rot=None, sh=None: el(fr, to, 'av_hair', pv, rot=rot, shift=sh)
        h = [el((-4.5, HB, -4.0), (4.5, HT, 4.0), 'av_skin', pv, faces=('south', 'east', 'west', 'up', 'down')),
             el((-4.5, HB, -4.0), (4.5, HT, -4.0), tex, pv, faces=('north',), uv={'north': [0, 0, 9, 8]}),
             hr((-4.9, HT - 1.4, -4.4), (4.9, HT + 0.9, 4.4), sh=(0.2, 0.1)),                          # the top
             hr((-4.9, HB + 0.4, 3.4), (4.9, HT - 1.2, 4.6), sh=(0.5, 0.3)),                           # the back, to the nape
             hr((4.5, HB + 1.0, -2.6), (5.2, HT - 1.2, 4.4), sh=(0.1, 0.4)),                           # the sides
             hr((-5.2, HB + 0.2, -2.6), (-4.5, HT - 1.2, 4.4), sh=(0.6, 0.2)),
             hr((-4.9, HT - 2.0, -4.6), (4.9, HT - 1.2, -4.0), sh=(0.3, 0.6)),                         # the fringe's edge
             hr((-4.9, HT - 2.9, -4.7), (1.2, HT - 1.9, -4.05), rot=('z', -11.25, (1.2, HT - 2.4, -4.4)), sh=(0.7, 0.2)),   # the sweep over her brow
             hr((4.1, HB + 1.6, -3.4), (5.3, HT - 1.6, -2.0), sh=(0.2, 0.7)),                          # her right lock, to the cheek
             hr((-5.4, HB - 0.6, -3.5), (-4.0, HT - 1.6, -1.9), sh=(0.8, 0.5)),                        # her left: the sweep's long end
             hr((-5.2, HB - 1.2, -3.3), (-4.2, HB - 0.4, -2.1))]                                       # (its tip, curling in)
        # the bun: a round knot high on her left, a navy band round its root
        bx, by, bz = -2.6, HT + 0.4, 1.0
        h += [hr((bx - 1.7, by, bz - 1.7), (bx + 1.7, by + 3.2, bz + 1.7), sh=(0.3, 0.6)),
              hr((bx - 1.3, by + 3.0, bz - 1.3), (bx + 1.3, by + 3.7, bz + 1.3)),
              hr((bx - 2.0, by + 0.6, bz - 1.3), (bx + 2.0, by + 2.6, bz + 1.3), sh=(0.7, 0.2)),
              hr((bx - 1.3, by + 0.6, bz - 2.0), (bx + 1.3, by + 2.6, bz + 2.0), sh=(0.5, 0.8)),
              el((bx - 1.75, by - 0.05, bz - 1.75), (bx + 1.75, by + 0.4, bz + 1.75), 'av_navy_dk', pv)]
        # the crown: a gold band, four arches meeting in a peak (blue stones in them), a green stone at the front, the violet
        # diamond on top - perched forward of the bun, tipped toward her right
        cx, cy = 1.2, HT + 0.7
        rz = ('z', -8, (cx, cy, 0))
        h += [el((cx - 2.4, cy, -2.6), (cx + 2.4, cy + 1.1, 2.2), 'av_gold', pv, rot=rz)]
        for ax, az in ((0, -2.4), (0, 2.0), (-2.2, -0.2), (2.2, -0.2)):
            h.append(el((cx + ax - (0.35 if ax else 1.1), cy + 0.9, az - (1.1 if ax else 0.35)), (cx + ax + (0.35 if ax else 1.1), cy + 2.5, az + (1.1 if ax else 0.35)),
                        'av_gold', pv, rot=rz))
        h += [el((cx - 1.6, cy + 0.7, -1.8), (cx + 1.6, cy + 2.1, 1.4), 'av_blue', pv, rot=rz),
              el((cx - 0.55, cy + 0.15, -2.75), (cx + 0.55, cy + 1.0, -2.5), 'av_green', pv, rot=rz),
              el((cx - 0.5, cy + 2.3, -0.7), (cx + 0.5, cy + 2.9, 0.3), 'av_gold', pv, rot=rz),
              el((cx - 0.5, cy + 2.8, -0.55), (cx + 0.5, cy + 4.4, 0.15), 'av_violet', pv, rot=('z', -8 + 45, (cx, cy + 3.6, -0.2)))]
        return h
    part('av_head', head())
    for fc in FACES:
        part(f'av_head_x{fc}', head(fc))

    # ---- the arms: long navy sleeves to the elbow; white gloves to above the elbow's crook, the scalloped cuffs
    def upper(sx):
        pv = PIVOT['armr' if sx > 0 else 'arml']; x0, y0, _ = pv
        return chain([(x0, y0 + 0.4, 0), (sx * 4.7, 18.6, 0)], [2.3], 2.3, 'av_navy', pv, FRONT, ext=0.3)
    def lower(sx):
        pv = PIVOT['forer' if sx > 0 else 'forel']; ex, ey, _ = pv
        wx, wy = sx * 4.9, 14.4
        a = chain([(ex, ey, 0), (wx, wy, 0)], [2.05], 2.05, 'av_glove', pv, FRONT, ext=0.25)
        a += [el((ex - 1.25, ey - 1.6, -1.25), (ex + 1.25, ey - 0.4, 1.25), 'av_cuff', pv, uv={f: [0, 0, 16, 4] for f in ('north', 'south', 'east', 'west')}),
              el((wx - 1.05, wy - 1.9, -1.15), (wx + 1.05, wy + 0.2, 1.05), 'av_glove', pv),        # the hand, gloved
              el((wx - 0.9, wy - 2.3, -1.2), (wx + 0.9, wy - 1.6, -0.6), 'av_glove', pv)]
        return a
    part('av_armr', upper(1)); part('av_arml', upper(-1)); part('av_forer', lower(1)); part('av_forel', lower(-1))

    # ---- the feet: navy slippers peeking out under the hem (a leg moves only a little: the gown hides the rest)
    def leg(sx):
        pv = PIVOT['legr' if sx > 0 else 'legl']; cx = pv[0]
        return [el((cx - 1.1, 0.0, -2.2), (cx + 1.1, 1.0, 1.0), 'av_shoe', pv),
                el((cx - 0.9, 0.0, -3.0), (cx + 0.9, 0.7, -2.1), 'av_shoe', pv, shift=(0.5, 0.5)),
                el((cx - 0.9, 0.8, -1.0), (cx + 0.9, 6.0, 0.9), 'av_navy_dk', pv)]
    part('av_legr', leg(1)); part('av_legl', leg(-1))
    return M


# ---------------------------------------------------------------------------------------------------- poses
def limb(sx, fwd=0.0, out=0.0, turn=0.0):
    return qs(('y', turn * sx), ('x', -fwd), ('z', -out * sx))


def P(**kw):
    return kw


CLASP = dict(armr=limb(1, 18, 4), forer=limb(1, 70, 0, 40), arml=limb(-1, 18, 4), forel=limb(-1, 70, 0, 40))   # her hands folded before her
IDLE = dict(CLASP, head=qs(('y', -8), ('z', 5)))
POSES = {
    # idle: hands folded at her waist, a shy tilt of the head; then she glances the other way
    'idle_a': P(**IDLE),
    'idle_b': P(_off=(0, -0.08, 0), **dict(CLASP, head=qs(('y', 8), ('z', -3), ('x', -4)))),
    # walk: a stately glide - the gown sways, the feet barely show
    'walk_a': P(_off=(0, 0.1, 0), body=qs(('z', 2), ('y', 3)), legr=limb(1, 16), legl=limb(-1, -14), head=qs(('z', -2)), **CLASP),
    'walk_up': P(_off=(0, 0.25, 0), legr=limb(1, 2), legl=limb(-1, -2), **CLASP),
    'walk_b': P(_off=(0, 0.1, 0), body=qs(('z', -2), ('y', -3)), legr=limb(1, -14), legl=limb(-1, 16), head=qs(('z', 2)), **CLASP),
    # run: skirts gathered in both hands
    'run_a': P(_off=(0, 0.3, 0), body=qs(('x', 8)), head=qs(('x', -6)), legr=limb(1, 28), legl=limb(-1, -24), armr=limb(1, 4, 16), forer=limb(1, 30, -10),
               arml=limb(-1, 4, 16), forel=limb(-1, 30, -10)),
    'run_up': P(_off=(0, 0.7, 0), body=qs(('x', 8)), head=qs(('x', -6)), legr=limb(1, 6), legl=limb(-1, -6), armr=limb(1, 4, 18), forer=limb(1, 34, -10),
                arml=limb(-1, 4, 18), forel=limb(-1, 34, -10)),
    'run_b': P(_off=(0, 0.3, 0), body=qs(('x', 8)), head=qs(('x', -6)), legr=limb(1, -24), legl=limb(-1, 28), armr=limb(1, 4, 16), forer=limb(1, 30, -10),
               arml=limb(-1, 4, 16), forel=limb(-1, 30, -10)),
    'jump': P(_face='happy', _off=(0, 1.2, 0), legr=limb(1, 20), legl=limb(-1, 6), armr=limb(1, 40, 40), forer=limb(1, 30), arml=limb(-1, 40, 40), forel=limb(-1, 30)),
    # the royal ward (her shield): one gloved hand raised, palm out - the tide answers
    'ward_a': P(_face='happy', body=qs(('y', -8)), head=qs(('x', -6), ('y', 8)), armr=limb(1, 100, 10), forer=limb(1, 20), arml=limb(-1, 30, 20), forel=limb(-1, 50)),
    'ward_b': P(_face='happy', _off=(0, 0.2, 0), body=qs(('y', 6)), head=qs(('x', -10)), armr=limb(1, 150, 24), forer=limb(1, 10), arml=limb(-1, 150, 24), forel=limb(-1, 10)),
    # the tidal strike: the hand drawn back, then flung forward - water at the foe
    'cast_up': P(_face='shout', body=qs(('y', -18)), armr=limb(1, 60, 40), forer=limb(1, 70), arml=limb(-1, 20, 10), forel=limb(-1, 40)),
    'cast': P(_face='shout', _off=(0, -0.1, 0), body=qs(('y', 14), ('x', 6)), head=qs(('x', -4)), armr=limb(1, 92, -4), forer=limb(1, 4), arml=limb(-1, -10, 20), forel=limb(-1, 30)),
    # the Tide of Crowns (her great move): both arms swept up and wide, rising off the ground
    'tide': P(_face='shout', _off=(0, 1.0, 0), body=qs(('x', -8)), head=qs(('x', -14)), armr=limb(1, 120, 60), forer=limb(1, 10), arml=limb(-1, 120, 60), forel=limb(-1, 10)),
    # a curtsey
    'curtsey': P(_face='happy', _off=(0, -1.2, 0), body=qs(('x', 14)), head=qs(('x', 12)), legr=limb(1, 30), legl=limb(-1, -24), armr=limb(1, 10, 34), forer=limb(1, 20),
                 arml=limb(-1, 10, 34), forel=limb(-1, 20)),
    'wave_a': P(_face='happy', **dict(IDLE, arml=limb(-1, 10, 120), forel=limb(-1, 50), head=qs(('y', 8)))),
    # sitting: on the ground, the gown spread round her (the body sinks; the skirt folds down into the floor with it)
    # (2.88: her legs only part-way out, so just the slipper toes peek from under the hem - not up through the skirt's front)
    'sit_a': P(_off=(0, -5.6, 0), legr=limb(1, 68, 8), legl=limb(-1, 68, 8), head=qs(('y', -8), ('z', 4)), **CLASP),
    'sit_b': P(_face='blink', _off=(0, -5.7, 0), body=qs(('x', 4)), legr=limb(1, 64, 10), legl=limb(-1, 72, 6), head=qs(('x', 10), ('z', -6)), **CLASP),
    'hurt': P(_face='hurt', body=qs(('x', -8)), head=qs(('x', -12)), armr=limb(1, 40, 30), forer=limb(1, 60), arml=limb(-1, 40, 30), forel=limb(-1, 60)),
    'tired': P(_face='hurt', _off=(0, -0.8, 0), body=qs(('x', 12), ('z', -4)), head=qs(('x', 16)), armr=limb(1, 0, 6), arml=limb(-1, 0, 6),
               forer=limb(1, 10), forel=limb(-1, 10)),
}
SWIM_FRAMES = 8
for _i in range(SWIM_FRAMES):                                            # (at home in the water: a slow, graceful stroke)
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(_off=(0, -6.0 + 0.4 * math.sin(2 * _p), 0), body=qs(('x', 70)), head=qs(('x', -50)),
                            armr=limb(1, 150 + 30 * math.sin(_p), 20 + 20 * math.cos(_p)), forer=limb(1, 20),
                            arml=limb(-1, 150 + 30 * math.sin(_p), 20 + 20 * math.cos(_p)), forel=limb(-1, 20),
                            legr=limb(1, 10 * math.sin(2 * _p)), legl=limb(-1, -10 * math.sin(2 * _p)))
for _k in list(POSES):                                                   # her ghostly form wears the '_g' models
    POSES[f'{_k}_g'] = dict(POSES[_k], _g=True)
DRAFT = ['idle_a', 'walk_a', 'run_a', 'ward_b', 'cast_up', 'cast', 'tide', 'curtsey', 'sit_a', 'hurt', 'idle_a_g', 'tide_g', 'sit_a_g']

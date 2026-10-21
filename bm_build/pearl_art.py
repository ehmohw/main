"""Queen Pearl (2.87): Emma's fun aunt, queen regent since Ava's death - from the owner's art. Quirky and easy: long brown hair
to the middle of her back, a great swoop of mint fringe over her right eye, the royal crown (gold, blue stones, a violet diamond)
perched on top; one big blue eye (the other winks under the swoop when she's pleased), rosy cheeks, pearl earrings and a pearl
necklace. A sleeveless aqua shift to the knee, deepening to teal at the hem; bare arms and legs; dark teal flats.

Her REGAL outfit (which she can't stand): a floor-length teal gown with gold trim and a white underskirt, white gloves, a pale
cape, and a taller crown - the '_r' models (each part's model in its regal cut).

A rigkit rig like the Neighbor's. Design units: feet at y=0, facing -z, her right is +x."""
import math
import random
from PIL import Image, ImageDraw

from phase57_art import hexc
from tullius_art import _noise, _shine
from rigkit import qs, el, chain
import ava_art as AV
import royal_face as RF

PREFIX = 'pq_'
RIG_SCALE = 0.92
PIVOT = {'body': (0, 13.0, 0), 'legr': (1.5, 13.0, 0), 'legl': (-1.5, 13.0, 0), 'head': (0, 24.4, 0),
         'armr': (4.0, 23.0, 0), 'forer': (4.5, 18.4, 0), 'arml': (-4.0, 23.0, 0), 'forel': (-4.5, 18.4, 0), 'cape': (0, 23.4, 2.2)}
PARENT = {'body': None, 'legr': None, 'legl': None, 'head': 'body', 'armr': 'body', 'forer': 'armr', 'arml': 'body', 'forel': 'arml', 'cape': 'body'}
PARTS = tuple(PIVOT)
PART_K = {}
FACES = ('happy', 'shout', 'hurt', 'blink', 'wink', 'pout')
SKIN, SKIN_DK = '#ecc0a0', '#cc9678'
HAIR, HAIR_DK, HAIR_LT = '#6e4420', '#4a2c12', '#93643a'
MINT, MINT_DK, MINT_LT = '#a8dcd6', '#78b4b0', '#d8f6f2'
AQUA, AQUA_DK = '#4ad6dc', '#1a9a9c'
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)


def HIDDEN(p, pose):
    return False                        # (her cape is its own model in each outfit: a real one in her regal outfit, a speck inside her casual one)


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    form = '_r' if pose.get('_r') else ''
    return f'{PREFIX}{p}{face}{form}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def _dress(seed, top=AQUA, bottom=AQUA_DK, h=64):
    """the shift: aqua at the top, deepening to teal toward the hem in two soft waves (as the art's shading)"""
    im = _noise(top, seed, 3); px = im.load(); a, b = hexc(top)[:3], hexc(bottom)[:3]
    for y in range(64):
        for x in range(64):
            wave = 6 * math.sin(x / 9.0 + seed)
            t = min(1.0, max(0.0, (y + wave - 18) / 46))
            t = 0.0 if t < 0.25 else (0.5 if t < 0.62 else 1.0) * 0.9 + 0.1 * t
            p = px[x, y]
            px[x, y] = tuple(int(a[i] * (1 - t) + b[i] * t) + (p[i] - a[i]) for i in range(3)) + (255,)
    return im


def _hair(seed, base=HAIR, dk=HAIR_DK, lt=HAIR_LT):
    im = _noise(base, seed, 5); rnd = random.Random(seed); d = ImageDraw.Draw(im)
    for _ in range(26):
        x = rnd.randrange(64)
        d.line((x, rnd.randrange(64), x + rnd.randint(-2, 2), rnd.randrange(64)), fill=hexc(rnd.choice([dk, lt])))
    return im


def _pearls(seed):
    im = _noise('#f4f2ec', seed, 3); d = ImageDraw.Draw(im)
    for x in range(0, 64, 8):
        for y in range(0, 64, 8):
            d.ellipse((x, y, x + 7, y + 7), fill=hexc('#fffef8'), outline=hexc('#c8c4b8'))
            d.point((x + 2, y + 2), fill=hexc('#ffffff'))
    return im


def _gown(seed):
    """the regal gown: deep teal satin, a gold hem-band and a gold seam down each side"""
    im = AV._cloth('#1a8a90', seed, '#0e5a60', '#4ac0c4', folds=5); d = ImageDraw.Draw(im)
    d.rectangle((0, 56, 63, 63), fill=hexc('#e0b83a')); d.line((0, 57, 63, 57), fill=hexc('#fff0a0'))
    return im


def _face(kind=None):
    """the front of her head, 64 x 64: the mint swoop sweeping down over her right eye (the viewer's left) and curling out at
    her cheek, brown hair parted under it; her left eye big and blue - a heavy lash, a starry blue iris, two glints - looking
    straight out; her right eye a closed wink-curve half under the swoop; rosy cheeks; a small nose; a sly closed smile"""
    im = _noise(SKIN, 1701, 4); d = ImageDraw.Draw(im)
    ink, white, lash = hexc('#241410'), hexc('#ffffff'), hexc('#20120c')
    hair, mint, mint_dk, mint_lt = hexc(HAIR), hexc(MINT), hexc(MINT_DK), hexc(MINT_LT)
    d.rectangle((0, 0, 63, 8), fill=hair)
    d.polygon([(40, 0), (63, 0), (63, 30), (58, 12), (48, 8)], fill=hair)                 # brown, parted to her left
    # the swoop: from the crown, across and down over her right eye, its tip curling out past her cheek
    d.polygon([(0, 0), (44, 0), (50, 6), (36, 14), (24, 24), (16, 36), (6, 44), (0, 46)], fill=mint)
    d.line((44, 0, 50, 6, 36, 14, 24, 24, 16, 36, 6, 44, 0, 46), fill=mint_dk, width=2)
    for i in range(5):
        d.line((8 + i * 7, 0, 2 + i * 5, 30 - i * 4), fill=mint_lt if i % 2 else mint_dk)
    # her left eye (the viewer's right): big and blue, straight ahead
    cx, cy = 44, 29
    if kind in ('happy',):
        d.arc((cx - 7, cy - 4, cx + 7, cy + 6), 200, 340, fill=lash, width=3)
    elif kind == 'blink':
        d.arc((cx - 7, cy - 6, cx + 7, cy + 4), 30, 150, fill=lash, width=2)
    elif kind == 'hurt':
        d.line((cx - 6, cy + 2, cx + 6, cy - 2), fill=lash, width=2); d.line((cx - 5, cy + 3, cx + 5, cy + 3), fill=lash)
    else:
        ry = 8 if kind == 'shout' else 7
        top = cy - ry + (2 if kind == 'pout' else 0)                                       # (pouting: the lid lowered)
        d.ellipse((cx - 7, cy - ry, cx + 7, cy + ry - 1), fill=white)
        d.ellipse((cx - 5, cy - ry + 2, cx + 5, cy + ry - 1), fill=hexc('#1a3aa0'))
        d.ellipse((cx - 4, cy - ry + 3, cx + 4, cy + ry - 2), fill=hexc('#2a6ae0'))
        d.ellipse((cx - 2, cy - 2, cx + 2, cy + 3), fill=hexc('#0a1440'))
        for px_, py_ in ((cx - 3, cy + 3), (cx + 3, cy + 1), (cx + 1, cy + 4)):          # (the stars in it)
            d.point((px_, py_), fill=hexc('#9ad0ff'))
        d.rectangle((cx - 4, cy - 4, cx - 2, cy - 2), fill=white); d.point((cx + 3, cy - 2), fill=white)
        if kind == 'pout':
            d.rectangle((cx - 7, cy - ry, cx + 7, top), fill=hexc(SKIN))
        d.arc((cx - 8, top - 1, cx + 8, cy + ry), 200, 340, fill=lash, width=2)
        d.line((cx + 7, cy - 3, cx + 9, cy - 6), fill=lash)
    # her right eye, half under the swoop: the wink (or open, peeking, when she shouts)
    rx, ry_ = 20, 31
    if kind in ('shout', 'hurt'):
        d.ellipse((rx - 5, ry_ - 5, rx + 5, ry_ + 4), fill=white); d.ellipse((rx - 3, ry_ - 3, rx + 3, ry_ + 4), fill=hexc('#2a6ae0'))
    else:
        d.arc((rx - 6, ry_ - 2, rx + 6, ry_ + 6), 200, 340, fill=lash, width=2)
        d.line((rx - 6, ry_ + 1, rx - 8, ry_ - 1), fill=lash)
    d.polygon([(0, 30), (12, 22), (24, 24), (16, 36), (6, 44), (0, 46)], fill=mint)      # (the swoop over the wink's outer half)
    d.line((24, 24, 16, 36, 6, 44, 0, 46), fill=mint_dk, width=2)
    # brows, cheeks, nose, mouth
    d.line((38, 18, 50, 17), fill=hexc('#5a3418'), width=1)
    for cx_ in (14, 52):
        d.ellipse((cx_ - 5, 40, cx_ + 5, 45), fill=hexc('#f0a0a8'))
    d.line((32, 36, 30, 40, 33, 41), fill=hexc(SKIN_DK))
    if kind == 'shout':
        d.ellipse((28, 47, 37, 55), fill=hexc('#7a2a2a'), outline=ink); d.ellipse((30, 51, 35, 54), fill=hexc('#e07070'))
    elif kind == 'happy':
        d.chord((25, 44, 41, 55), 0, 180, fill=hexc('#7a2a2a'), outline=ink); d.rectangle((27, 49, 39, 50), fill=white)
    elif kind == 'hurt':
        d.line((26, 51, 30, 49, 34, 51, 38, 49), fill=ink, width=1)
    elif kind == 'pout':
        d.arc((28, 50, 38, 56), 200, 340, fill=ink, width=2); d.point((37, 49), fill=ink)
    else:
        d.arc((26, 45, 40, 51), 20, 160, fill=ink, width=1)                                # the sly smile, a touch up at one end
        d.line((39, 47, 41, 45), fill=ink)
    return im


def textures():
    T = {'pq_skin': _noise(SKIN, 1702, 4), 'pq_skin_dk': _noise(SKIN_DK, 1703, 4), 'pq_hair': _hair(1704),
         'pq_mint': _hair(1705, MINT, MINT_DK, MINT_LT), 'pq_dress': _dress(1706), 'pq_dress_top': _noise(AQUA, 1707, 3),
         'pq_flat': _shine('#0e3a40', '#3a7a80', 1708), 'pq_pearl': _pearls(1709), 'pq_gold': AV._gold(1710),
         'pq_blue': AV._gem('#2a8ae0', '#bfe8ff', '#1a4a9a', 1711), 'pq_violet': AV._gem('#b02ae0', '#f0c0ff', '#5a1490', 1712),
         'pq_gown': _gown(1713), 'pq_gown_top': AV._cloth('#1a8a90', 1714, '#0e5a60', '#4ac0c4', folds=2),
         'pq_under': AV._under(1715), 'pq_glove': AV._glove(1716), 'pq_cape': AV._cloth('#cfeeee', 1717, '#9ac8cc', '#f4ffff', folds=4),
         'pq_face': RF.pearl_face()}
    for k in FACES:
        T[f'pq_face_{k}'] = RF.pearl_face(k)
    return T


# ---------------------------------------------------------------------------------------------------- models
def models():
    M = {}
    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)

    # ---- the body: casual - the aqua shift (straps, the square neckline, the A-line skirt to the knee), the pearl necklace;
    #      regal - the teal gown to the floor over a white underskirt, gold at the waist
    pv = PIVOT['body']
    def torso(regal):
        top = 'pq_gown_top' if regal else 'pq_dress_top'
        b = [el((-3.2, 14.0, -2.3), (3.2, 20.8, 2.3), top, pv, shift=(0.3, 0.2)),                                    # the bodice
             el((-3.3, 18.6, -2.45), (3.3, 20.8, 2.3), top, pv, shift=(0.6, 0.1)),                                   # (the bust)
             el((-3.0, 20.6, -1.9), (3.0, 22.8, 1.9), 'pq_skin', pv),                                                # bare shoulders
             el((-1.2, 22.4, -1.2), (1.2, 24.9, 1.2), 'pq_skin', pv)]                                                # the neck
        if not regal:
            b += [el((-2.6, 20.8, -2.05), (-1.6, 22.9, 2.05), top, pv), el((1.6, 20.8, -2.05), (2.6, 22.9, 2.05), top, pv)]   # the straps
            b += [el((-2.2, 22.6, -1.5), (2.2, 23.1, -1.3), 'pq_pearl', pv, uv={'north': [0, 0, 16, 2]}),          # the necklace
                  el((-2.2, 22.6, 1.3), (2.2, 23.1, 1.5), 'pq_pearl', pv), el((-2.2, 22.6, -1.5), (-1.7, 23.1, 1.5), 'pq_pearl', pv),
                  el((1.7, 22.6, -1.5), (2.2, 23.1, 1.5), 'pq_pearl', pv)]
            for i, (y0, y1, hw, hd) in enumerate([(11.4, 14.2, 3.5, 2.6), (9.2, 11.6, 4.0, 3.0), (7.4, 9.4, 4.5, 3.4)]):   # the skirt, to the knee
                b.append(el((-hw, y0, -hd), (hw, y1, hd), 'pq_dress', pv, uv={f: [0, 16 - y1 / 14.2 * 16, 16, 16 - y0 / 14.2 * 16] for f in ('north', 'south', 'east', 'west')}))
        else:
            b += [el((-3.3, 13.6, -2.4), (3.3, 14.4, 2.4), 'pq_gold', pv),                                         # the gold sash
                  el((-0.6, 18.0, -2.55), (0.6, 21.0, -2.4), 'pq_gold', pv),                                       # a gold placket
                  el((-2.6, 22.4, -1.6), (2.6, 22.9, 1.6), 'pq_pearl', pv)]                                        # (her pearls, still)
            for i in range(8):
                t0, t1 = i / 8, (i + 1) / 8
                y1, y0 = 13.6 - t0 * 13.3, max(0.3, 13.6 - t1 * 13.3 - 0.15)
                hw, hd = 3.4 + 3.4 * t1 ** 0.8, 2.6 + 2.6 * t1 ** 0.8
                gap = 0.4 + 0.25 * i
                b += [el((-hw, y0, -hd + 0.5), (hw, y1, hd), 'pq_gown', pv, uv={f: [0, 16 - y1 / 13.6 * 16, 16, 16 - y0 / 13.6 * 16] for f in ('north', 'south', 'east', 'west')}),
                      el((-hw, y0, -hd), (-gap, y1, -hd + 0.5), 'pq_gown', pv, uv={f: [0, 16 - y1 / 13.6 * 16, 8, 16 - y0 / 13.6 * 16] for f in ('north', 'south', 'east', 'west')}),
                      el((gap, y0, -hd), (hw, y1, -hd + 0.5), 'pq_gown', pv, uv={f: [8, 16 - y1 / 13.6 * 16, 16, 16 - y0 / 13.6 * 16] for f in ('north', 'south', 'east', 'west')}),
                      el((-gap, y0, -hd + 0.25), (gap, y1, -hd + 0.4), 'pq_under', pv, faces=('north',))]
        return b
    part('pq_body', torso(False)); part('pq_body_r', torso(True))

    # ---- the head: Emma's head (9 x 8 x 8, the face in Emma's own pixel scale); long brown hair down her back and over her
    #      shoulders; the mint swoop - a thick wave from a parting high on her left, sweeping down across her right eye and curling
    #      out past her right cheek; the crown perched on top (taller in her regal outfit); pearl earrings. (+x: her right)
    pv = PIVOT['head']
    HB = pv[1]; HT = HB + 8.0
    def head(face=None, regal=False):
        tex = 'pq_face' if face is None else f'pq_face_{face}'
        hr = lambda fr, to, rot=None, sh=None: el(fr, to, 'pq_hair', pv, rot=rot, shift=sh)
        mt = lambda fr, to, rot=None, sh=None: el(fr, to, 'pq_mint', pv, rot=rot, shift=sh)
        h = [el((-4.5, HB, -4.0), (4.5, HT, 4.0), 'pq_skin', pv, faces=('south', 'east', 'west', 'up', 'down')),
             el((-4.5, HB, -4.0), (4.5, HT, -4.0), tex, pv, faces=('north',), uv={'north': [0, 0, 9, 8]}),
             hr((-4.9, HT - 1.6, -4.4), (4.9, HT + 0.8, 4.4), sh=(0.2, 0.1)),                          # the top
             hr((-4.9, HB - 7.4, 3.4), (4.9, HT - 1.4, 4.7), sh=(0.5, 0.3)),                           # long, down her back
             hr((4.5, HB - 0.4, -2.8), (5.2, HT - 1.4, 4.4), sh=(0.1, 0.4)),                           # the sides
             hr((-5.2, HB - 0.4, -2.8), (-4.5, HT - 1.4, 4.4), sh=(0.6, 0.2)),
             hr((-5.4, HB - 6.0, -1.8), (-4.4, HB + 1.0, 1.4), sh=(0.3, 0.7)),                         # over her left shoulder
             hr((4.4, HB - 3.0, -1.8), (5.4, HB + 1.0, 1.4), sh=(0.8, 0.5)),                           # (and behind her right)
             hr((-4.9, HT - 2.0, -4.6), (-0.6, HT - 1.4, -4.0), sh=(0.3, 0.6)),                        # the brown at her parting
             # the swoop: over the top from the parting, down across her right eye, out past her right cheek in a curl
             mt((-1.6, HT - 2.2, -4.8), (5.0, HT + 1.1, 1.2), sh=(0.2, 0.4)),
             mt((1.0, HT - 4.6, -4.75), (5.2, HT - 1.8, -3.9), rot=('z', -11.25, (5.0, HT - 2.0, -4.3)), sh=(0.6, 0.1)),
             mt((4.4, HB + 1.4, -4.4), (5.8, HT - 2.0, -1.0), sh=(0.4, 0.6)),
             mt((5.0, HB + 0.4, -4.0), (6.6, HB + 2.2, -1.6), rot=('z', -22.5, (5.6, HB + 1.4, -2.8)), sh=(0.8, 0.3)),
             mt((-0.6, HT + 0.6, -4.2), (3.6, HT + 1.6, -0.2), rot=('z', -11.25, (1.4, HT + 1.0, -2.0)), sh=(0.1, 0.8))]   # (its crest)
        for sx in (-1, 1):                                                                          # pearl earrings
            h.append(el((sx * 4.7 - 0.3, HB - 0.2, -3.5), (sx * 4.7 + 0.3, HB + 0.6, -2.9), 'pq_pearl', pv))
        cx, cy = -0.8, HT + 0.9
        rz = ('z', 6, (cx, cy, 0))
        tall = 1.0 if regal else 0.0
        h += [el((cx - 2.3, cy, -2.3), (cx + 2.3, cy + 1.0 + tall * 0.4, 2.3), 'pq_gold', pv, rot=rz)]
        for ax, az in ((0, -2.1), (0, 2.1), (-2.1, 0), (2.1, 0)):
            h.append(el((cx + ax - (0.35 if ax else 1.0), cy + 0.9, az - (1.0 if ax else 0.35)), (cx + ax + (0.35 if ax else 1.0), cy + 2.3 + tall, az + (1.0 if ax else 0.35)),
                        'pq_gold', pv, rot=rz))
        h += [el((cx - 1.5, cy + 0.6, -1.5), (cx + 1.5, cy + 1.9 + tall * 0.6, 1.5), 'pq_blue', pv, rot=rz),        # the blue stones inside the arches
              el((cx - 0.5, cy + 2.5 + tall, -0.35), (cx + 0.5, cy + 4.2 + tall, 0.35), 'pq_violet', pv, rot=('z', 6 + 45, (cx, cy + 3.4 + tall, 0)))]
        return h
    for regal, sfx in ((False, ''), (True, '_r')):
        part(f'pq_head{sfx}', head(None, regal))
        for fc in FACES:
            part(f'pq_head_x{fc}{sfx}', head(fc, regal))

    # ---- the arms: bare (casual) or long white gloves (regal)
    def upper(sx, regal):
        pv = PIVOT['armr' if sx > 0 else 'arml']; x0, y0, _ = pv
        return chain([(x0, y0 + 0.2, 0), (sx * 4.5, 18.4, 0)], [1.9], 1.9, 'pq_glove' if regal else 'pq_skin', pv, FRONT, ext=0.3)
    def lower(sx, regal):
        pv = PIVOT['forer' if sx > 0 else 'forel']; ex, ey, _ = pv
        wx, wy = sx * 4.7, 14.4
        t = 'pq_glove' if regal else 'pq_skin'
        return chain([(ex, ey, 0), (wx, wy, 0)], [1.75], 1.75, t, pv, FRONT, ext=0.25) + \
            [el((wx - 0.95, wy - 1.8, -1.0), (wx + 0.95, wy + 0.2, 0.9), t, pv), el((wx - 0.8, wy - 2.2, -1.05), (wx + 0.8, wy - 1.5, -0.5), t, pv)]
    for regal, sfx in ((False, ''), (True, '_r')):
        part(f'pq_armr{sfx}', upper(1, regal)); part(f'pq_arml{sfx}', upper(-1, regal))
        part(f'pq_forer{sfx}', lower(1, regal)); part(f'pq_forel{sfx}', lower(-1, regal))

    # ---- the legs: bare to the dark flats (casual); hidden under the gown, only the slippers peeking out (regal)
    def leg(sx, regal):
        pv = PIVOT['legr' if sx > 0 else 'legl']; cx = pv[0]
        L = [el((cx - 1.0, 0.0, -2.2), (cx + 1.0, 0.9, 1.0), 'pq_flat', pv),
             el((cx - 0.85, 0.0, -3.1), (cx + 0.85, 0.6, -2.1), 'pq_flat', pv, shift=(0.5, 0.5))]
        if regal:
            L.append(el((cx - 0.9, 0.8, -1.0), (cx + 0.9, 12.0, 0.9), 'pq_gown_top', pv))
        else:
            L += [el((cx - 0.95, 0.8, -0.95), (cx + 0.95, 7.8, 0.95), 'pq_skin', pv),
                  el((cx - 1.0, 7.6, -1.0), (cx + 1.0, 13.2, 1.0), 'pq_skin', pv, shift=(0.3, 0.3))]
        return L
    for regal, sfx in ((False, ''), (True, '_r')):
        part(f'pq_legr{sfx}', leg(1, regal)); part(f'pq_legl{sfx}', leg(-1, regal))

    # ---- the cape (regal only): pale, from the shoulders to the floor
    pv = PIVOT['cape']
    cape = [el((-3.6, 0.6, 2.2), (3.6, 23.2, 2.6), 'pq_cape', pv), el((-3.9, 22.4, -1.6), (3.9, 23.6, 2.7), 'pq_gold', pv)]
    part('pq_cape_r', cape)
    part('pq_cape', [el((-0.05, 18.0, 0.0), (0.05, 18.1, 0.1), 'pq_dress_top', pv)])   # (the casual look: a speck inside her, never seen)
    return M


# ---------------------------------------------------------------------------------------------------- poses
def limb(sx, fwd=0.0, out=0.0, turn=0.0):
    return qs(('y', turn * sx), ('x', -fwd), ('z', -out * sx))


def P(**kw):
    return kw


HIP = dict(armr=limb(1, -14, 38), forer=limb(1, 14, -100))               # her right hand on her hip (as the art)
IDLE = dict(HIP, arml=limb(-1, 10, 18), forel=limb(-1, 30), head=qs(('y', 10), ('z', -6)), legl=limb(-1, -6, 4))
POSES = {
    # idle: a hand on her hip, the other out, weight on one foot, a cocky tilt; then a little bounce on her toes
    'idle_a': P(**IDLE),
    'idle_b': P(_face='wink', _off=(0, 0.15, 0), **dict(IDLE, arml=limb(-1, 30, 30), forel=limb(-1, 40), head=qs(('y', -6), ('z', 8)))),
    # walk: a skipping, swinging walk
    'walk_a': P(_off=(0, 0.25, 0), legr=limb(1, 26), legl=limb(-1, -24), armr=limb(1, -22, 10), forer=limb(1, 20), arml=limb(-1, 26, 10), forel=limb(-1, 24),
                head=qs(('z', -5))),
    'walk_up': P(_off=(0, 0.7, 0), legr=limb(1, 6), legl=limb(-1, -18), armr=limb(1, 2, 14), forer=limb(1, 20), arml=limb(-1, 2, 14), forel=limb(-1, 20)),
    'walk_b': P(_off=(0, 0.25, 0), legr=limb(1, -24), legl=limb(-1, 26), armr=limb(1, 26, 10), forer=limb(1, 24), arml=limb(-1, -22, 10), forel=limb(-1, 20),
                head=qs(('z', 5))),
    'run_a': P(_off=(0, 0.4, 0), body=qs(('x', 10)), head=qs(('x', -8)), legr=limb(1, 44), legl=limb(-1, -38), armr=limb(1, -34, 12), forer=limb(1, 60),
               arml=limb(-1, 40, 12), forel=limb(-1, 60)),
    'run_up': P(_off=(0, 1.0, 0), body=qs(('x', 10)), head=qs(('x', -8)), legr=limb(1, 12), legl=limb(-1, -18), armr=limb(1, 4, 14), forer=limb(1, 60),
                arml=limb(-1, 4, 14), forel=limb(-1, 60)),
    'run_b': P(_off=(0, 0.4, 0), body=qs(('x', 10)), head=qs(('x', -8)), legr=limb(1, -38), legl=limb(-1, 44), armr=limb(1, 40, 12), forer=limb(1, 60),
               arml=limb(-1, -34, 12), forel=limb(-1, 60)),
    'jump': P(_face='happy', _off=(0, 1.4, 0), legr=limb(1, 50), legl=limb(-1, -20), armr=limb(1, 150, 30), forer=limb(1, 10), arml=limb(-1, 150, 30), forel=limb(-1, 10)),
    # the flick (her attack): a pearl flicked off her thumb at the foe
    'flick_up': P(_face='wink', body=qs(('y', -14)), armr=limb(1, 40, 20), forer=limb(1, 100, 0, -20), **dict(arml=limb(-1, 10, 18), forel=limb(-1, 30))),
    'flick': P(_face='happy', body=qs(('y', 10)), armr=limb(1, 90, -4), forer=limb(1, 10), arml=limb(-1, -10, 20), forel=limb(-1, 20)),
    # the wink (her charm): a hand up to frame it, the eye shut - and the foe forgets what it was doing
    'wink': P(_face='wink', body=qs(('z', 6)), head=qs(('z', 12), ('y', 6)), armr=limb(1, 120, -30), forer=limb(1, 100, 0, -30), **dict(arml=limb(-1, 10, 18), forel=limb(-1, 30))),
    # the Royal Proclamation (her great move): both arms flung out - "I declare a HOLIDAY!"
    'proclaim': P(_face='shout', _off=(0, 0.6, 0), body=qs(('x', -8)), head=qs(('x', -12)), armr=limb(1, 120, 70), forer=limb(1, 10), arml=limb(-1, 120, 70), forel=limb(-1, 10)),
    # a twirl and a bow
    'twirl': P(_face='happy', body=qs(('y', 90)), armr=limb(1, 10, 80), forer=limb(1, 10), arml=limb(-1, 10, 80), forel=limb(-1, 10), legl=limb(-1, 30)),
    'bow': P(_face='wink', body=qs(('x', 24)), head=qs(('x', 6)), armr=limb(1, -20, 40), forer=limb(1, 30), arml=limb(-1, 40, -20), forel=limb(-1, 60, 0, 30),
             legr=limb(1, -10), legl=limb(-1, 20)),
    'wave_a': P(_face='happy', **dict(IDLE, arml=limb(-1, 10, 130), forel=limb(-1, 50), head=qs(('y', -8)))),
    'sit_a': P(_off=(0, -6.0, 0), legr=limb(1, 84, 4), legl=limb(-1, 84, 4), armr=limb(1, 20, 20), forer=limb(1, 40), arml=limb(-1, 20, 20), forel=limb(-1, 40),
               head=qs(('y', 10), ('z', -6))),
    'sit_b': P(_face='blink', _off=(0, -6.1, 0), body=qs(('x', -6)), legr=limb(1, 70, 4), legl=limb(-1, 88, 4), armr=limb(1, -30, 30), forer=limb(1, 10),
               arml=limb(-1, -30, 30), forel=limb(-1, 10), head=qs(('x', -12), ('z', 8))),
    'hurt': P(_face='hurt', body=qs(('x', -8)), head=qs(('x', -12)), armr=limb(1, 30, 30), forer=limb(1, 60), arml=limb(-1, 30, 30), forel=limb(-1, 60)),
    'tired': P(_face='hurt', _off=(0, -0.8, 0), body=qs(('x', 12), ('z', -4)), head=qs(('x', 14)), armr=limb(1, 0, 8), arml=limb(-1, 0, 8),
               forer=limb(1, 8), forel=limb(-1, 8), legr=limb(1, 4), legl=limb(-1, -4)),
    'pout': P(_face='pout', **dict(IDLE, armr=limb(1, 30, -20), forer=limb(1, 100, 0, 70), arml=limb(-1, 30, -20), forel=limb(-1, 100, 0, 70), head=qs(('y', -14), ('x', 4)))),
}
SWIM_FRAMES = 8
for _i in range(SWIM_FRAMES):                                            # (a frog-kick, the hair streaming)
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(_off=(0, -6.0 + 0.4 * math.sin(2 * _p), 0), body=qs(('x', 70)), head=qs(('x', -50)),
                            armr=limb(1, 140 + 34 * math.sin(_p), 30 + 24 * math.cos(_p)), forer=limb(1, 24),
                            arml=limb(-1, 140 + 34 * math.sin(_p), 30 + 24 * math.cos(_p)), forel=limb(-1, 24),
                            legr=limb(1, -6 + 24 * math.sin(2 * _p), 4), legl=limb(-1, -6 - 24 * math.sin(2 * _p), 4))
for _k in list(POSES):                                                   # her regal outfit wears the '_r' models
    POSES[f'{_k}_r'] = dict(POSES[_k], _r=True)
DRAFT = ['idle_a', 'idle_b', 'walk_a', 'flick_up', 'wink', 'proclaim', 'bow', 'sit_a', 'hurt', 'idle_a_r', 'walk_a_r', 'pout_r', 'sit_a_r']

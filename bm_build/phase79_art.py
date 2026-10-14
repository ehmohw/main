"""2.65: KillerWatt (from the approved mockup, mockups/killerwatt_art.py): the boss and the follower share this rig.
KillerWatt - a towering, glassy green brute with a jagged violet grin, a lime breastplate,
claws, spiked shins, curled golden toes and four great golden scythe-tendrils behind him.

Same rig kit as Emma, Celi and Leo (phase57_art): one item model per part, its joint at model (8, 8, 8). Design units: feet
at y=0, facing -z, his right is +x. Drawn at RIG_SCALE 1.55 - about four blocks tall, the tendrils higher still.
    python3 mockups/killerwatt_art.py <out.png>     renders a preview, Leo and a player box beside him for scale
"""
import math
import os
import random
import sys
from PIL import Image, ImageDraw

from phase57_art import _cloth, _el, hexc, qa, qmul

RIG_SCALE = 1.55
PIVOT = {'body': (0, 15, 0), 'head': (0, 29, 0), 'armr': (7.4, 26.6, 0), 'arml': (-7.4, 26.6, 0), 'legr': (2.7, 15, 0), 'legl': (-2.7, 15, 0),
         'tend': (0, 27, 7.5), 'tendl': (0, 22.5, 7.0)}        # (2.67: the pairs move apart; their joints sit back off his spine, so a forward
                                                               #  strike swings them over his shoulders, never through his chest)
PARTS = tuple(PIVOT)
G, G_LT, G_DK, TEAL = '#3cab4c', '#74d462', '#258a46', '#1e7458'
LIME, GOLD, GOLD_LT, VIOLET = '#86e01e', '#f6dc30', '#fcf09a', '#3a1650'


# ---------------------------------------------------------------------------------------------------- textures
def _slime(base, seed, light, dark, gloss=True):
    """the glassy, mottled hide: soft blotches of lighter and darker green, a few bright glints"""
    rnd = random.Random(seed); im = _cloth(base, seed, var=0.03); d = ImageDraw.Draw(im)
    for _ in range(26):
        x, y, r = rnd.randint(0, 63), rnd.randint(0, 63), rnd.randint(3, 8)
        d.ellipse((x - r, y - r, x + r, y + r), fill=hexc(rnd.choice((light, dark, base))))
    im2 = im.copy()
    for y in range(64):                                                                     # (soften the blotches)
        for x in range(64):
            p = [im.getpixel(((x + dx) % 64, (y + dy) % 64)) for dx, dy in ((0, 0), (1, 0), (0, 1), (-1, 0), (0, -1))]
            im2.putpixel((x, y), tuple(sum(c[i] for c in p) // 5 for i in range(3)) + (255,))
    if gloss:
        for _ in range(7):
            x, y = rnd.randint(2, 61), rnd.randint(2, 61)
            im2.putpixel((x, y), hexc('#e8fff0')); im2.putpixel((x, y + 1), hexc('#b8f4c8'))
    return im2


def _cracked():
    """the dark belly: deep teal, split by a jagged black-green crack down the middle and two curved ones at the sides"""
    im = _slime(TEAL, 91, '#2a8a66', '#145a46', gloss=False); d = ImageDraw.Draw(im)
    pts = [(32, 0), (30, 10), (34, 18), (29, 28), (33, 38), (30, 50), (32, 64)]
    d.line(pts, fill=hexc('#0a3424'), width=3); d.line(pts, fill=hexc('#0e4430'), width=1)
    for sx in (-1, 1):
        d.arc((32 + sx * 14 - 10, 20, 32 + sx * 14 + 10, 48), 90 + sx * 60 - 30, 90 + sx * 60 + 30, fill=hexc('#0a3424'), width=2)
    return im


MAW_EXPR = ('snarl', 'hurt', 'roar', 'smug')          # (2.67) his face is his maw: it snarls in a fight, clenches when hit, gapes, smirks
_MAWS = {
    None: [(2, 9), (8, 12), (13, 7), (18, 12), (24, 9), (24, 17), (21, 22), (19, 18), (16, 24), (13, 19), (10, 24), (7, 18), (5, 22), (2, 17)],
    # wider, teeth down from the top as well as up from the bottom
    'snarl': [(1, 8), (4, 11), (7, 8), (10, 11), (13, 6), (16, 11), (19, 8), (22, 11), (25, 8), (25, 18), (22, 24), (19, 19), (16, 25), (13, 20),
              (10, 25), (7, 19), (4, 24), (1, 18)],
    # clenched: the jaws ground shut, a thin jagged seam
    'hurt': [(2, 12), (5, 14), (8, 12), (11, 14), (13, 11), (15, 14), (18, 12), (21, 14), (24, 12), (24, 15), (21, 17), (18, 15), (15, 18), (13, 15),
             (11, 18), (8, 15), (5, 17), (2, 15)],
    # gaping: the whole maw thrown open
    'roar': [(1, 6), (5, 9), (9, 5), (13, 8), (17, 5), (21, 9), (25, 6), (25, 15), (24, 22), (20, 25), (17, 22), (13, 26), (9, 22), (6, 25), (2, 22), (1, 15)],
    # a lopsided grin: his right corner hitched up
    'smug': [(2, 12), (8, 14), (13, 9), (18, 12), (24, 6), (24, 14), (21, 19), (19, 16), (16, 22), (13, 18), (10, 23), (7, 18), (5, 22), (2, 18)],
}


def _face(expr=None):
    """the head's front, 26 x 27 texels: green helm, a violet maw - pointed at the top, a jag of teeth at the bottom"""
    P = hexc
    im = _slime(G, 92, G_LT, G_DK)
    d = ImageDraw.Draw(im)
    maw = _MAWS[expr]
    d.polygon(maw, fill=P('#1a0828'))
    if expr is None:
        inner = [(4, 11), (8, 14), (13, 10), (18, 14), (22, 11), (22, 16), (20, 19), (13, 15), (6, 19), (4, 16)]
    else:                                                                                    # (the throat: the maw drawn in toward its middle)
        cx = sum(x for x, _ in maw) / len(maw); cy = sum(y for _, y in maw) / len(maw)
        inner = [(cx + (x - cx) * 0.72, cy + (y - cy) * (0.45 if expr == 'hurt' else 0.6)) for x, y in maw]
    d.polygon(inner, fill=P(VIOLET))
    if expr != 'hurt':
        cx = sum(x for x, _ in inner) / len(inner); cy = sum(y for _, y in inner) / len(inner)
        d.polygon([(cx - 5, cy + 1), (cx, cy - 2), (cx + 5, cy + 1), (cx, cy)], fill=P('#5a2a7a'))   # a sheen inside
    d.line(maw + [maw[0]], fill=P('#0e3a24'), width=1)
    return im


def _gold(seed):
    return _slime(GOLD, seed, GOLD_LT, '#d6b41c', gloss=False)


def _emblem():
    """the breastplate badge (12 x 10 texels): a dark green crescent, a golden one nested in it, a swirl"""
    P = hexc
    im = _cloth(LIME, 93, var=0.02); d = ImageDraw.Draw(im)
    d.ellipse((0, 0, 12, 10), fill=P('#2a7a2a')); d.ellipse((2, -2, 12, 6), fill=P(LIME))
    d.ellipse((2, 2, 10, 9), fill=P(GOLD)); d.ellipse((3, 1, 10, 6), fill=P('#2a7a2a'))
    d.arc((5, 2, 9, 6), 200, 520, fill=P(GOLD_LT), width=1)
    return im


def textures():
    T = {}
    T['kw_hide'] = _slime(G, 81, G_LT, G_DK)
    T['kw_hide_dk'] = _slime(G_DK, 82, G, TEAL)
    T['kw_belly'] = _cracked()
    T['kw_lime'] = _slime(LIME, 83, '#a8f040', '#6cc014', gloss=False)
    T['kw_emblem'] = _emblem()
    T['kw_face'] = _face()
    for e in MAW_EXPR: T[f'kw_face_x{e}'] = _face(e)
    T['kw_gold'] = _gold(84)
    T['kw_spike'] = _cloth('#16503a', 85, var=0.04)
    T['kw_claw'] = _cloth('#2e8a62', 86, var=0.04)
    if not _BASE_ONLY: T.update(variant_textures(T))                   # 2.66: the follower's elements
    return T


_BASE_ONLY = False


# ---------------------------------------------------------------------------------------------------- models
def _seg(p0, p1, w, t, tex, pv, z0):
    """a straight piece of a curved blade, from p0 to p1 (x, y), w wide and t thick, tilted to follow the line (the
    tilt split between an axis-aligned box and an element rotation of at most 45 degrees)"""
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0) + w * 0.35; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    a = math.degrees(math.atan2(y1 - y0, x1 - x0))
    while a > 90: a -= 180
    while a <= -90: a += 180
    if abs(a) <= 45:
        fr, to, rot = (cx - L / 2, cy - w / 2, z0), (cx + L / 2, cy + w / 2, z0 + t), a
    else:
        fr, to, rot = (cx - w / 2, cy - L / 2, z0), (cx + w / 2, cy + L / 2, z0 + t), a - 90 if a > 0 else a + 90
    rot = max(-45, min(45, round(rot / 22.5) * 22.5)) if os.environ.get('KW_VANILLA_ANGLES') else rot
    return _el(fr, to, tex, pv, ('z', rot, (cx, cy, z0)) if abs(rot) > 0.01 else None)


def _blade(path, w0, w1, pv, z0, sx=1):
    out = []
    n = len(path) - 1
    for i in range(n):
        w = w0 + (w1 - w0) * i / max(1, n - 1)
        p0, p1 = (path[i][0] * sx, path[i][1]), (path[i + 1][0] * sx, path[i + 1][1])
        out.append(_seg(p0, p1, w, 1.0, 'kw_gold', pv, z0))
    return out


def models():
    M = {}
    global _BASE_ONLY
    _BASE_ONLY = True
    try: TX = {k: f'bm:block/{k}' for k in textures()}
    finally: _BASE_ONLY = False
    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({k: TX[k] for k in used}, els)

    # ---- legs: thick thighs, long shins with jagged fins at the knee, the foot curling up into a golden point
    def leg(sx):
        pv = PIVOT['legr' if sx > 0 else 'legl']
        x0, x1 = (0.3, 5.1) if sx > 0 else (-5.1, -0.3)
        cx = (x0 + x1) / 2; ox = x1 if sx > 0 else x0                    # (the outside edge)
        fin = lambda y, l, ang: _el((ox - 0.2 * sx if sx > 0 else ox - l, y, -0.3), (ox + l if sx > 0 else ox + 0.2, y + 0.8, 0.5), 'kw_spike', pv,
                                    ('z', ang * sx, (ox, y + 0.4, 0)))
        return [_el((x0, 9.0, -2.4), (x1, 15.6, 2.4), 'kw_hide', pv),                                        # thigh
                _el((x0 + 0.4, 2.0, -2.0), (x1 - 0.4, 9.6, 2.0), 'kw_hide', pv),                              # shin
                _el((x0 + 0.7, 4.0, 0.6), (x1 - 0.7, 8.6, 2.6), 'kw_hide_dk', pv),                            # calf
                _el((x0 + 0.6, 8.2, -2.5), (x1 - 0.6, 10.2, -1.8), 'kw_hide_dk', pv),                         # the knee
                fin(8.6, 2.2, 30), fin(7.2, 1.8, 15), fin(5.8, 1.4, 35),
                fin(4.6, 1.6, 50),
                _el((x0 + 0.2, 0, -3.6), (x1 - 0.2, 2.4, 2.0), 'kw_hide', pv),                                # the foot
                _el((cx - 1.4, 0, -5.4), (cx + 1.4, 1.6, -3.4), 'kw_gold', pv),                               # the toe, curling up
                _el((cx - 0.9, 0.9, -6.6), (cx + 0.9, 2.4, -5.0), 'kw_gold', pv, ('x', 22.5, (cx, 1.2, -5.4))),
                _el((cx - 0.5, 2.0, -7.2), (cx + 0.5, 3.6, -6.2), 'kw_gold', pv, ('x', 45, (cx, 2.4, -6.4)))]
    part('kw_legr', leg(1)); part('kw_legl', leg(-1))

    # ---- body: narrow hips, the cracked dark belly, a broad lime breastplate (the badge on it), a thick neck
    pv = PIVOT['body']
    body = [_el((-4.6, 13.4, -2.7), (4.6, 17.6, 2.7), 'kw_hide', pv),                                         # hips
            _el((-4.8, 17.4, -2.9), (4.8, 22.8, 2.6), 'kw_belly', pv),
            _el((-6.4, 22.4, -3.4), (6.4, 28.4, 3.0), 'kw_lime', pv),                                         # the breastplate
            _el((-7.0, 27.4, -3.5), (-4.6, 29.4, 2.9), 'kw_lime', pv), _el((4.6, 27.4, -3.5), (7.0, 29.4, 2.9), 'kw_lime', pv),
            _el((-6.8, 28.4, -1.0), (-5.6, 30.6, 0.4), 'kw_lime', pv, ('z', 22.5, (-6.2, 28.4, 0))),          # its points over the shoulders
            _el((5.6, 28.4, -1.0), (6.8, 30.6, 0.4), 'kw_lime', pv, ('z', -22.5, (6.2, 28.4, 0))),
            _el((-1.9, 24.2, -3.55), (1.9, 27.2, -3.4), 'kw_emblem', pv, uv={'north': [0, 0, 3.0, 2.5]}),
            _el((-6.0, 21.6, -2.0), (6.0, 26.0, 2.8), 'kw_hide_dk', pv),                                       # lats, flaring under the plate
            _el((-2.0, 28.0, -1.8), (2.0, 30.4, 1.8), 'kw_hide', pv),                                         # neck
            # spurs at the plate's lower corners, curving in over the belly
            _el((-5.8, 20.8, -3.2), (-4.2, 22.6, -2.6), 'kw_spike', pv, ('z', -22.5, (-5.0, 22.6, -2.9))),
            _el((4.2, 20.8, -3.2), (5.8, 22.6, -2.6), 'kw_spike', pv, ('z', 22.5, (5.0, 22.6, -2.9))),
            _el((-3.6, 13.0, -2.9), (3.6, 13.8, -2.4), 'kw_hide_dk', pv, ('x', 0, (0, 13.4, -2.6)))]          # the V of the hips
    part('kw_body', body)

    # ---- head: a smooth helm of a skull, a long crest curling back, spines at the sides, a pointed chin, the violet maw
    pv = PIVOT['head']; h = lambda fr, to, t='kw_hide', rot=None: _el(fr, to, t, pv, rot)
    head = [h((-3.3, 29.6, -3.1), (3.3, 36.4, 3.1)),
            h((-1.7, 28.4, -3.1), (1.7, 30.0, -1.3)),                                                          # chin
            h((3.0, 32.4, -0.6), (5.6, 33.4, 0.6), 'kw_hide_dk', ('z', 22.5, (3.0, 32.9, 0))),               # side spines
            h((-5.6, 32.4, -0.6), (-3.0, 33.4, 0.6), 'kw_hide_dk', ('z', -22.5, (-3.0, 32.9, 0))),
            h((3.0, 34.6, -0.4), (4.8, 35.4, 0.4), 'kw_hide_dk', ('z', 45, (3.0, 35.0, 0))),
            h((-4.8, 34.6, -0.4), (-3.0, 35.4, 0.4), 'kw_hide_dk', ('z', -45, (-3.0, 35.0, 0))),
            # the crest: up from the brow and curling back, gold along its tip
            h((-0.7, 35.8, -2.2), (0.7, 38.2, -0.4)), h((-0.6, 37.6, -1.4), (0.6, 39.8, 0.4), rot=('x', -22.5, (0, 37.6, -0.5))),
            h((-0.5, 38.8, -0.2), (0.5, 40.6, 1.4), rot=('x', -45, (0, 38.8, 0.6))),
            h((-0.4, 39.2, 1.4), (0.4, 40.0, 3.6), 'kw_gold', ('x', -22.5, (0, 39.6, 1.4))),
            h((-0.5, 34.0, 2.8), (0.5, 36.0, 4.4), 'kw_hide_dk', ('x', 22.5, (0, 35, 3.0)))]                 # a spine at the back
    head[0]['faces']['north'] = {'uv': [0, 0, 6.6, 6.8], 'texture': '#kw_face'}
    part('kw_head', head)

    # ---- arms: huge shoulders and biceps, jagged fins down the forearm; one hand a claw, one a fist. The 'flex' arms
    #      bend at the elbow (the forearm folds 45 degrees back up), as in the art
    def arm(sx, flex=False, fist=False):
        nm = 'armr' if sx > 0 else 'arml'; pv = PIVOT[nm]; cx = pv[0] + 0.4 * sx; ey = 18.6
        up = (lambda y0, y1: (2 * ey - y1, 2 * ey - y0)) if flex else (lambda y0, y1: (y0, y1))
        fa = ('z', -45 * sx, (cx, ey, 0)) if flex else None
        def F(fr, to, tex):                                                                                  # a forearm piece
            y0, y1 = up(fr[1], to[1])
            return _el((fr[0], y0, fr[2]), (to[0], y1, to[2]), tex, pv, fa)
        ox = cx + 2.1 * sx
        els = [_el((cx - 3.0, 23.4, -3.0), (cx + 3.0, 28.8, 3.0), 'kw_hide', pv),                          # the shoulder
               _el((cx - 2.4, 18.0, -2.4), (cx + 2.4, 24.0, 2.6), 'kw_hide', pv),                          # the arm
               _el((cx - 1.6 + 0.6 * sx, 19.0, -2.9), (cx + 1.6 + 0.6 * sx, 23.0, -2.2), 'kw_hide_dk', pv),  # the bicep's bulge
               F((cx - 2.1, 11.6, -2.1), (cx + 2.1, 18.6, 2.1), 'kw_hide'),
               F((min(ox, ox + 2.2 * sx), 15.0, -0.3), (max(ox, ox + 2.2 * sx), 15.8, 0.5), 'kw_spike'),      # fins
               F((min(ox, ox + 1.8 * sx), 13.4, -0.3), (max(ox, ox + 1.8 * sx), 14.2, 0.5), 'kw_spike'),
               F((min(ox, ox + 1.4 * sx), 16.6, -0.3), (max(ox, ox + 1.4 * sx), 17.4, 0.5), 'kw_spike'),
               F((cx - 2.0, 8.6, -1.8), (cx + 2.0, 11.8, 1.8), 'kw_hide')]                                   # the hand
        if fist:
            els += [F((cx - 2.1, 7.6, -2.2), (cx + 2.1, 9.4, 1.0), 'kw_hide_dk')]                              # knuckles
        else:
            for i in range(4):                                                                                 # long claws
                x = cx - 1.7 + i * 1.1
                els += [F((x, 5.4, -1.9), (x + 0.7, 8.8, -1.1), 'kw_claw'), F((x + 0.1, 4.2, -2.4), (x + 0.6, 5.6, -1.7), 'kw_spike')]
            tx = cx - 2.4 * sx
            els += [F((min(tx, tx - 1.4 * sx), 7.4, -1.6), (max(tx, tx - 1.4 * sx), 10.2, -0.6), 'kw_claw')]  # the thumb
        return els
    part('kw_armr', arm(1)); part('kw_arml', arm(-1))
    part('kw_armr_flex', arm(1, True, True)); part('kw_arml_flex', arm(-1, True))

    # ---- the tendrils: four golden bolts of lightning from his back - hard, jagged angles, each with a fork. Two rear up
    #      and out over his shoulders, two sweep down past his legs to the ground. (2.67: they run straight out sideways
    #      before they climb, behind his shoulders, so struck forward they pass outside him)
    pv, pvl = PIVOT['tend'], PIVOT['tendl']; z0 = PIVOT['tend'][2]; zl = PIVOT['tendl'][2]
    upper = [(1.0, 27.0), (6.0, 28.2), (4.8, 29.2), (11.5, 30.8), (10.2, 32.0), (14.5, 37.5), (13.0, 38.8), (16.5, 45.0), (15.0, 46.0), (17.5, 50.0)]
    upper_fork = [(11.5, 30.8), (14.6, 29.2), (13.7, 28.1)]
    lower = [(1.0, 22.5), (6.5, 21.3), (5.2, 20.2), (11.5, 18.2), (10.0, 17.0), (14.0, 11.5), (12.5, 10.3), (15.5, 4.5), (14.0, 3.3), (16.0, 0.3)]
    lower_fork = [(11.5, 18.2), (14.2, 20.0), (13.4, 21.2)]
    tend, tendl = [], []
    for sx in (1, -1):
        tend += _blade(upper, 3.4, 0.8, pv, z0, sx) + _blade(upper_fork, 1.8, 0.6, pv, z0 + 0.1, sx)
        tendl += _blade(lower, 3.4, 0.8, pvl, zl, sx) + _blade(lower_fork, 1.6, 0.6, pvl, zl + 0.1, sx)
    tend += [_el((-1.8, 25.2, 2.6), (1.8, 28.6, z0 + 1.1), 'kw_gold', pv)]                                   # where they root, off his spine
    tendl += [_el((-1.6, 20.8, 2.8), (1.6, 23.8, zl + 1.1), 'kw_gold', pvl)]
    part('kw_tend', _shrink(tend, TEND_K)); part('kw_tendl', _shrink(tendl, TEND_K))
    M.update(variant_models(M))
    return M


TEND_PARTS = ('tend', 'tendl')
TEND_K = 2.0      # the tendrils reach past a model's -16..32 box: built at half size about the joint, shown at double scale


def _shrink(els, k):
    sc = lambda v: [round(8 + (c - 8) / k, 4) for c in v]
    out = []
    for e in els:
        e = dict(e, **{'from': sc(e['from']), 'to': sc(e['to'])})
        if 'rotation' in e:
            e['rotation'] = dict(e['rotation'], origin=sc(e['rotation']['origin']))
        out.append(e)
    return out


# ---------------------------------------------------------------------------------------------------- poses
# (the display frame: his front is +z, his right -x; a limb swings forward with negative x, his right arm out with negative z)
I = (0.0, 0.0, 0.0, 1.0)
UP_R, UP_L = qmul(qa('y', 15), qa('z', -78)), qmul(qa('y', -15), qa('z', 78))
# (the 2.66 poses and their flat part_xf gave way to the 2.67 skeleton below)


# ---------------------------------------------------------------------------------------------------- 2.66: the follower's elements
# Hand the follower a gem and his hide takes its element (a gradient map of the same textures); the Ethereal Gem makes him
# metallic black with iridescent tendrils, glowing seams and a crown of jagged spikes.
EL_KEYS = ['fire', 'water', 'poison', 'earth', 'electric', 'rock', 'air', 'grass', 'ice']        # (phase46's order: bm.kxel 1..9; 10 ethereal)
EL_PAL = {  # body (dark, mid, light), accents for the tendrils (dark, light)
    'fire': (('#3a0a04', '#c4361a', '#ff9a4a'), ('#b04a08', '#ffe060')),
    'water': (('#06244e', '#1e6ad0', '#7ad0ff'), ('#2a8ab0', '#d8f8ff')),
    'poison': (('#220834', '#7a2ab8', '#d09aff'), ('#3e9014', '#d0ff6a')),
    'earth': (('#24160a', '#6a4a22', '#c09a5c'), ('#2e6e22', '#a0e070')),
    'rock': (('#222226', '#6e6a68', '#c8c0b8'), ('#7a5a2e', '#ecd49a')),
    'air': (('#4e6a7a', '#b0d4e6', '#ffffff'), ('#7aaed0', '#f4ffff')),
    'grass': (('#0c320c', '#3a9a2a', '#b4f47a'), ('#c43a7a', '#ffd0e8')),
    'ice': (('#16405e', '#7ac8f0', '#f0feff'), ('#3e9ed0', '#ffffff'))}
# (2.67) his wardrobe (phase99): his own look in other colours - worn when no gem is in him (a gem's element always shows)
COS_PAL = {'c1': ('Midnight', (('#04060e', '#16224a', '#4a6ab0'), ('#1a8ac0', '#bff4ff'))),
           'c2': ('Bone', (('#3a3428', '#a89c80', '#f0e8d4'), ('#8a1a1a', '#ff6a5a'))),
           'c3': ('Neon', (('#08040c', '#2a1a34', '#5a4a6a'), ('#c0108a', '#ff8ae8'))),
           'c4': ('Golden Thunder', (('#2a1a04', '#a07018', '#ffd870'), ('#c88a10', '#fff4b0')))}
EL_PAL.update({k: pal for k, (_n, pal) in COS_PAL.items()})
VARIANTS = [k for k in EL_KEYS if k != 'electric'] + ['eth', 'wf'] + list(COS_PAL)      # (2.76: wf - the Wraithfire Heart's form)
BODY_TEX = ['kw_hide', 'kw_hide_dk', 'kw_belly', 'kw_lime', 'kw_emblem', 'kw_face', 'kw_spike', 'kw_claw']


def _lum(p):
    return (0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) / 255


def _mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _gmap(im, stops):
    """recolour by luminance through (dark, mid, light) - the grain and the blotches stay, the colour is the element's"""
    s = [hexc(c)[:3] for c in stops]
    out = im.copy()
    for y in range(im.height):
        for x in range(im.width):
            p = im.getpixel((x, y))
            L = max(0.0, min(1.0, (_lum(p) - 0.08) / 0.84))
            c = _mix(s[0], s[1], L / 0.5) if L < 0.5 else _mix(s[1], s[2], (L - 0.5) / 0.5)
            out.putpixel((x, y), c + (p[3],))
    return out


def _irid(im, seed=0):
    """iridescence: the hue slides across the surface, brighter where the base is bright"""
    import colorsys
    out = im.copy()
    for y in range(im.height):
        for x in range(im.width):
            p = im.getpixel((x, y)); L = _lum(p)
            r, g, b = colorsys.hsv_to_rgb(((x * 0.9 + y * 1.3) / 64 + L * 0.35 + seed) % 1.0, 0.55, 0.45 + 0.55 * L)
            out.putpixel((x, y), (int(r * 255), int(g * 255), int(b * 255), p[3]))
    return out


def _metal(im, seed):
    """black chrome: near-black, a cool sheen, a few long diagonal glints"""
    out = _gmap(im, ('#040406', '#18181f', '#4a4a5c'))
    rnd = random.Random(seed)
    for _ in range(5):
        x0, y0, ln = rnd.randint(0, 63), rnd.randint(0, 63), rnd.randint(6, 16)
        for i in range(ln):
            x, y = (x0 + i) % 64, (y0 + i) % 64
            out.putpixel((x, y), hexc('#8a8aa8')[:3] + (255,))
            out.putpixel(((x + 1) % 64, y), hexc('#5a5a74')[:3] + (255,))
    return out


def _eth_tex(name, im):
    if name == 'kw_belly':                                       # its cracks glow
        out = _metal(im, 191)
        for y in range(64):
            for x in range(64):
                if _lum(im.getpixel((x, y))) < 0.13:
                    out.putpixel((x, y), hexc('#b070ff' if (x + y) % 9 < 5 else '#70f0ff')[:3] + (255,))
        return out
    if name == 'kw_face':                                        # the maw burns cyan-white
        out = _metal(im, 192)
        for y in range(im.height):
            for x in range(im.width):
                r, g, b, a = im.getpixel((x, y))
                if b > g and r > g and b > 30:                   # (the violet maw)
                    out.putpixel((x, y), _mix(hexc('#40c8ff')[:3], (240, 255, 255), min(1.0, b / 140)) + (a,))
        return out
    if name in ('kw_emblem', 'kw_claw'):
        return _irid(im, 0.3 if name == 'kw_claw' else 0.6)
    if name == 'kw_spike':
        return _gmap(im, ('#000000', '#14141c', '#6a6a88'))
    if name == 'kw_lime':
        return _gmap(im, ('#0c0c12', '#2a2a36', '#7a7a94'))
    return _metal(im, 190 + len(name))


def _wf_tex(name, im):
    """(2.76) the Wraithfire form: charred black steel, its seams and cracks burning soul-blue"""
    if name == 'kw_belly':                                       # its cracks burn
        out = _gmap(im, ('#020608', '#0a1c26', '#2a4a5c'))
        for y in range(64):
            for x in range(64):
                if _lum(im.getpixel((x, y))) < 0.13:
                    out.putpixel((x, y), hexc('#5ae8ff' if (x * 2 + y) % 7 < 4 else '#e0ffff')[:3] + (255,))
        return out
    if name == 'kw_face':                                        # the maw is a furnace of blue fire
        out = _gmap(im, ('#020608', '#0c1e28', '#38566a'))
        for y in range(im.height):
            for x in range(im.width):
                r, g, b, a = im.getpixel((x, y))
                if b > g and r > g and b > 30:
                    out.putpixel((x, y), _mix(hexc('#1aa8e0')[:3], (230, 255, 255), min(1.0, b / 140)) + (a,))
        return out
    if name in ('kw_emblem', 'kw_claw'):                         # soul fire: teal to white-hot
        return _gmap(im, ('#04304a', '#16b4e8', '#c8fcff'))
    if name == 'kw_gold':                                        # his lightning tendrils: blue flame, not ice
        return _gmap(im, ('#04283c', '#0e8cc4', '#3adcff'))
    if name == 'kw_spike':
        return _gmap(im, ('#000000', '#08303e', '#5ae0ff'))
    if name == 'kw_lime':                                        # his plate and tendrils: the brightest flame
        return _gmap(im, ('#02283a', '#0a96c8', '#48ecff'))
    return _gmap(im, ('#010406', '#071a26', '#1e4e66'))


def variant_textures(base):
    out = {}
    for v in VARIANTS:
        for name in BODY_TEX + ['kw_gold'] + [f'kw_face_x{e}' for e in MAW_EXPR]:
            im = base[name]
            if v == 'eth':
                out[f'{name}_{v}'] = _irid(im) if name == 'kw_gold' else _eth_tex('kw_face' if name.startswith('kw_face') else name, im)
            elif v == 'wf':
                out[f'{name}_{v}'] = _wf_tex('kw_face' if name.startswith('kw_face') else name, im)
            else:
                body, acc = EL_PAL[v]
                mid = '#%02x%02x%02x' % _mix(hexc(acc[0])[:3], hexc(acc[1])[:3], 0.55)
                out[f'{name}_{v}'] = _gmap(im, (acc[0], mid, acc[1])) if name == 'kw_gold' else _gmap(im, body)
    return out


def eth_spikes(name):
    """the Ethereal form's jagged spikes, by part (design units, about each part's joint)"""
    sp = lambda fr, to, axis, ang, org, pv: _el(fr, to, 'kw_spike', pv, (axis, ang, org))
    if name == 'kw_body':
        pv = PIVOT['body']
        out = [sp((-0.5, y, 2.2), (0.5, y + 2.6, 3.0), 'x', -22.5, (0, y, 2.6), pv) for y in (17.0, 20.0, 23.0, 26.0)]
        out += [sp((-7.6, 28.0, -0.5), (-6.6, 32.4, 0.5), 'z', 22.5, (-7.1, 28.0, 0), pv), sp((6.6, 28.0, -0.5), (7.6, 32.4, 0.5), 'z', -22.5, (7.1, 28.0, 0), pv)]
        return out
    if name == 'kw_head':
        pv = PIVOT['head']
        return [sp((1.6, 35.4, -0.5), (2.6, 39.4, 0.5), 'z', -22.5, (2.1, 35.4, 0), pv), sp((-2.6, 35.4, -0.5), (-1.6, 39.4, 0.5), 'z', 22.5, (-2.1, 35.4, 0), pv)]
    for nm, sx in (('armr', 1), ('arml', -1)):
        if name.startswith(f'kw_{nm}'):
            pv = PIVOT[nm]; cx = pv[0] + 0.4 * sx
            return [sp((cx - 0.6, 28.4, -0.6), (cx + 0.6, 32.6, 0.6), 'z', -30 * sx, (cx, 28.4, 0), pv),
                    sp((cx + 1.0 * sx - 0.4, 27.6, -1.8), (cx + 1.0 * sx + 0.4, 30.6, -1.0), 'z', -45 * sx, (cx + sx, 27.6, -1.4), pv)]
    for nm, sx in (('legr', 1), ('legl', -1)):
        if name == f'kw_{nm}':
            pv = PIVOT[nm]; cx = 2.7 * sx
            return [sp((cx - 0.5, 9.6, -3.8), (cx + 0.5, 10.6, -2.4), 'x', -45, (cx, 10.1, -2.6), pv)]
    return []


def variant_models(base_models):
    """(name -> (tex, els)) the same parts, re-textured for each element; the ethereal ones spiked"""
    import copy
    M = {}
    for name, (tex, els) in base_models.items():
        if not name.startswith('kw_') or name == 'kw_spark':
            continue
        for v in VARIANTS:
            e2 = copy.deepcopy(els) + (copy.deepcopy(eth_spikes(name)) if v in ('eth', 'wf') and name != 'kw_tend' else [])
            for e in e2:
                for f in e['faces'].values():
                    f['texture'] = f['texture'] + f'_{v}'
                if v == 'wf':                                    # (burning: a glow of its own, whatever the light)
                    e['light_emission'] = max(e.get('light_emission', 0), 8)
            used = sorted({e['faces'][f]['texture'][1:] for e in e2 for f in e['faces']})
            M[f'{name}_{v}'] = ({k: f'bm:block/{k}' for k in used}, e2)
    return M





# ---------------------------------------------------------------------------------------------------- 2.67: a skeleton, not a pile of parts
# The head, the arms and both pairs of tendrils hang off the torso: their joints swing with it (the old rig left the head
# behind when he leaned - in the fall it ended up behind his neck) and their rotations are relative to it. Poses below give
# the torso and legs as before, the children relative to the torso; the arms keep their old orientation in the world.
CHILD = ('head', 'armr', 'arml', 'tend', 'tendl')


def qconj(q):
    return (-q[0], -q[1], -q[2], q[3])


def qrot(q, v):
    """rotate vector v (x, y, z) by quaternion q"""
    x, y, z, w = q
    vx, vy, vz = v
    tx, ty, tz = 2 * (y * vz - z * vy), 2 * (z * vx - x * vz), 2 * (x * vy - y * vx)
    return (vx + w * tx + (y * tz - z * ty), vy + w * ty + (z * tx - x * tz), vz + w * tz + (x * ty - y * tx))


def part_xf(pose, p):
    """(rotation, joint offset in design units in the display frame, the whole-rig drop dy)"""
    B = pose['body']
    if p not in CHILD:
        return pose[p], (0.0, 0.0, 0.0), pose['_dy']
    bx, by, bz = PIVOT['body']; px, py, pz = PIVOT[p]
    d = (-(px - bx), py - by, -(pz - bz))                                 # (design -> display frame: his right is -x, his front +z)
    r = qrot(B, d)
    return qmul(B, pose[p]), (r[0] - d[0], r[1] - d[1], r[2] - d[2]), pose['_dy']


def _P2(dy=0.0, body=I, head=I, arms=None, armr=None, arml=None, tend=I, tendl=I, **legs):
    """a pose: arms given in the world's frame (arms=(r, l)) are made relative to the torso"""
    d = {p: I for p in PARTS}; d['_dy'] = dy; d['body'] = body; d['head'] = head; d['tend'] = tend; d['tendl'] = tendl
    ar, al = arms if arms else (armr or I, arml or I)
    d['armr'], d['arml'] = qmul(qconj(body), ar), qmul(qconj(body), al)
    d.update(legs)
    return d


X = lambda a: qa('x', a)
POSES = {
    'idle_a': _P2(body=X(2), head=X(3), arms=(qa('z', -8), qa('z', 8)), tend=X(-5), tendl=X(4)),
    'idle_b': _P2(0.04, body=X(-1), head=qmul(qa('y', 8), X(2)), arms=(qmul(qa('z', -12), X(-6)), qmul(qa('z', 12), X(-4))), tend=qmul(X(4), qa('z', 3)),
                  tendl=qmul(X(-4), qa('z', -2))),
    'walk_a': _P2(0.06, body=qa('y', 5), head=X(4), legr=X(-26), legl=X(22), arms=(qmul(qa('z', -8), X(20)), qmul(qa('z', 8), X(-20))), tend=qmul(X(8), qa('z', 4)),
                  tendl=X(-7)),
    'walk_b': _P2(0.06, body=qa('y', -5), head=X(4), legr=X(22), legl=X(-26), arms=(qmul(qa('z', -8), X(-20)), qmul(qa('z', 8), X(20))), tend=qmul(X(2), qa('z', -4)),
                  tendl=X(7)),
    # THUNDER SLAM: rear up, scythes drawn back - then down, the upper scythes striking past his shoulders, the lower whipping forward
    'slam_up': _P2(0.1, body=X(-6), head=X(-6), arms=(UP_R, UP_L), tend=X(-32), tendl=X(26), legl=X(-8)),
    'slam_dn': _P2(-0.25, body=X(20), head=X(-8), arms=(X(-78), X(-78)), tend=X(58), tendl=X(-52), legr=X(-18), legl=X(12)),
    'sweep_a': _P2(body=qa('y', 30), head=qa('y', -10), arms=(qa('z', -30), qa('z', 30)), tend=qmul(qa('y', 40), X(-12)), tendl=qmul(qa('y', 40), X(12))),
    'sweep_b': _P2(body=qa('y', -35), head=qa('y', 15), arms=(qa('z', -45), qa('z', 20)), tend=qmul(qa('y', -70), X(40)), tendl=qmul(qa('y', -70), X(-34))),
    'roar': _P2(0.05, body=X(-10), head=X(-12), arms=(qmul(qa('z', -50), X(10)), qmul(qa('z', 50), X(10))), tend=X(-36), tendl=X(28)),
    'call': _P2(0.12, body=X(-8), head=X(-10), arms=(qa('z', -160), qa('z', 160)), tend=X(-26), tendl=X(20)),
    'fall': _P2(-0.55, body=X(30), head=X(12), arms=(X(-40), X(-30)), legr=X(-40), legl=X(-34), tend=X(22), tendl=X(-8)),
    # the follower's
    'stab': _P2(0.02, body=X(14), head=X(-6), arms=(qmul(qa('z', -20), X(25)), qmul(qa('z', 20), X(25))), tend=X(66), tendl=X(-70)),
    'punch_r': _P2(body=qmul(qa('y', -22), X(8)), head=qa('y', 12), arms=(X(-92), qmul(qa('z', 14), X(30))), tend=X(34), tendl=X(-22)),
    'punch_l': _P2(body=qmul(qa('y', 22), X(8)), head=qa('y', -12), arms=(qmul(qa('z', -14), X(30)), X(-92)), tend=X(34), tendl=X(-22)),
    'crouch': _P2(-0.4, body=X(24), head=X(-28), legr=X(-34), legl=X(-34), arms=(qmul(qa('z', -16), X(30)), qmul(qa('z', 16), X(30))), tend=X(-30), tendl=X(34)),
    'hover': _P2(0.12, body=X(4), head=X(2), legr=X(10), legl=X(-6), arms=(qa('z', -38), qa('z', 38)), tend=qmul(X(-24), qa('z', 4)), tendl=X(18)),
    'climb': _P2(body=X(10), head=X(-24), arms=(X(-150), X(-135)), legr=X(-30), legl=X(10), tend=X(60), tendl=X(-40)),
    # the boss's TENDRIL LUNGE: coiled back, then all four scythes drive at you
    'lunge_a': _P2(0.02, body=X(-8), head=X(-4), arms=(qmul(qa('z', -30), X(20)), qmul(qa('z', 30), X(20))), tend=X(-46), tendl=X(40)),
    'lunge_b': _P2(-0.1, body=X(18), head=X(-12), arms=(X(-30), X(-30)), tend=X(82), tendl=X(-80), legr=X(-14), legl=X(10)),
    # the follower's CHARGED attack: gathering (arms up and out, every scythe raised), then the release
    # (2.67) a blow lands: thrown back a moment, arms flung out, tendrils whipping up
    'flinch': _P2(-0.05, body=X(-14), head=X(-20), arms=(qmul(qa('z', -34), X(-18)), qmul(qa('z', 34), X(-18))), tend=X(-38), tendl=X(30),
                  legr=X(8), legl=X(-6)),
    'charge': _P2(0.1, body=X(-6), head=X(-12), arms=(qa('z', -125), qa('z', 125)), tend=X(-40), tendl=X(36)),
    'release': _P2(-0.12, body=X(14), head=X(-10), arms=(X(-85), X(-85)), tend=X(52), tendl=X(-48), legr=X(-16), legl=X(12)),
    # (2.67) swimming: a powerful four-armed breaststroke - arms reach, sweep out and haul back, the tendrils stroking
    # with them a beat behind, a frog kick at the end of each pull
    'swim_a': _P2(-1.0, body=X(16), head=X(-16), arms=(qmul(qa('z', -18), X(-112)), qmul(qa('z', 18), X(-112))), tend=X(-28), tendl=X(26),
                  legr=X(16), legl=X(16)),
    'swim_b': _P2(-0.98, body=X(14), head=X(-14), arms=(qmul(qa('z', -68), X(-62)), qmul(qa('z', 68), X(-62))), tend=qmul(qa('y', 20), X(6)),
                  tendl=qmul(qa('y', -20), X(-6)), legr=X(-8), legl=X(-8)),
    'swim_c': _P2(-1.02, body=X(18), head=X(-18), arms=(qmul(qa('z', -32), X(12)), qmul(qa('z', 32), X(12))), tend=X(40), tendl=X(-38),
                  legr=X(24), legl=X(24)),
    'swim_d': _P2(-1.0, body=X(16), head=X(-16), arms=(qmul(qa('z', -12), X(-44)), qmul(qa('z', 12), X(-44))), tend=X(4), tendl=X(-4),
                  legr=X(2), legl=X(2)),
    # (2.75) sitting (right-click him): down on his haunches, legs out in front, hands on his knees, the tendrils fanned out behind
    'sit_a': _P2(-1.19, body=X(-8), head=X(6), legr=X(-90), legl=X(-87), arms=(qmul(qa('z', -14), X(-48)), qmul(qa('z', 14), X(-48))), tend=X(-50), tendl=X(84)),
    'sit_b': _P2(-1.18, body=X(-10), head=qmul(qa('y', 14), X(2)), legr=X(-90), legl=X(-86), arms=(qmul(qa('z', -14), X(-46)), qmul(qa('z', 16), X(-50))),
                 tend=X(-56), tendl=X(86)),
    'sit_look': _P2(-1.19, body=qmul(qa('y', -6), X(-8)), head=qmul(qa('y', -28), X(8)), legr=X(-89), legl=X(-87),
                    arms=(qmul(qa('z', -14), X(-48)), qmul(qa('z', 14), X(-48))), tend=X(-48), tendl=X(82)),
}
FLEX = {'slam_up', 'roar'}

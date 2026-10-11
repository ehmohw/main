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
         'tend': (0, 24, 3)}
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


def _face():
    """the head's front, 26 x 27 texels: green helm, a violet maw - pointed at the top, a jag of teeth at the bottom"""
    P = hexc
    im = _slime(G, 92, G_LT, G_DK)
    d = ImageDraw.Draw(im)
    maw = [(2, 9), (8, 12), (13, 7), (18, 12), (24, 9), (24, 17), (21, 22), (19, 18), (16, 24), (13, 19), (10, 24), (7, 18), (5, 22), (2, 17)]
    d.polygon(maw, fill=P('#1a0828'))
    inner = [(4, 11), (8, 14), (13, 10), (18, 14), (22, 11), (22, 16), (20, 19), (13, 15), (6, 19), (4, 16)]
    d.polygon(inner, fill=P(VIOLET))
    d.polygon([(8, 15), (13, 12), (18, 15), (13, 14)], fill=P('#5a2a7a'))                   # a sheen inside
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
    T['kw_gold'] = _gold(84)
    T['kw_spike'] = _cloth('#16503a', 85, var=0.04)
    T['kw_claw'] = _cloth('#2e8a62', 86, var=0.04)
    return T


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
    TX = {k: f'bm:block/{k}' for k in textures()}
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

    # ---- the tendrils: four golden scythes from his back - two rearing up and out over his shoulders, two sweeping
    #      down past his legs to the ground, each with an inner hook
    pv = PIVOT['tend']; z0 = 3.0
    upper = [(1.5, 26.5), (5.5, 27.6), (9.5, 30.0), (12.6, 33.6), (14.8, 38.0), (16.0, 42.5), (16.4, 46.5), (16.0, 48.8)]
    upper_hook = [(6.0, 28.2), (7.2, 32.0), (6.6, 35.6), (5.0, 38.0)]
    lower = [(1.5, 22.0), (5.5, 21.2), (9.5, 19.6), (12.6, 16.6), (14.6, 12.0), (15.6, 7.0), (15.6, 2.6), (14.8, 0.2)]
    lower_hook = [(8.4, 20.2), (9.6, 23.4), (9.0, 26.4)]
    tend = []
    for sx in (1, -1):
        tend += _blade(upper, 5.2, 0.8, pv, z0, sx) + _blade(upper_hook, 2.6, 0.6, pv, z0 + 0.1, sx)
        tend += _blade(lower, 5.2, 0.8, pv, z0 + 0.2, sx) + _blade(lower_hook, 2.4, 0.6, pv, z0 + 0.3, sx)
    tend += [_el((-2.2, 20.4, 2.6), (2.2, 28.4, 3.6), 'kw_gold', pv)]                                       # where they root, down his spine
    part('kw_tend', _shrink(tend, TEND_K))
    return M


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
def P(dy=0.0, **parts):
    d = {p: I for p in PARTS}; d.update(parts); d['_dy'] = dy
    return d
UP_R, UP_L = qmul(qa('y', 15), qa('z', -78)), qmul(qa('y', -15), qa('z', 78))
POSES = {
    'idle_a': P(body=qa('x', 2), head=qa('x', 6), armr=qa('z', -8), arml=qa('z', 8), tend=qa('x', -4)),
    'idle_b': P(0.04, body=qa('x', -1), head=qmul(qa('y', 8), qa('x', 2)), armr=qmul(qa('z', -12), qa('x', -6)), arml=qmul(qa('z', 12), qa('x', -4)), tend=qa('x', 5)),
    'walk_a': P(0.06, body=qa('y', 5), head=qa('x', 6), legr=qa('x', -26), legl=qa('x', 22), armr=qmul(qa('z', -8), qa('x', 20)), arml=qmul(qa('z', 8), qa('x', -20)), tend=qa('x', 7)),
    'walk_b': P(0.06, body=qa('y', -5), head=qa('x', 6), legr=qa('x', 22), legl=qa('x', -26), armr=qmul(qa('z', -8), qa('x', -20)), arml=qmul(qa('z', 8), qa('x', 20)), tend=qa('x', 3)),
    'slam_up': P(0.1, body=qa('x', -6), head=qa('x', -12), armr=UP_R, arml=UP_L, tend=qa('x', -14), legl=qa('x', -8)),
    'slam_dn': P(-0.25, body=qa('x', 20), head=qa('x', 14), armr=qa('x', -78), arml=qa('x', -78), tend=qa('x', 18), legr=qa('x', -18), legl=qa('x', 12)),
    'sweep_a': P(body=qa('y', 30), head=qa('y', 20), armr=qa('z', -30), arml=qa('z', 30), tend=qmul(qa('y', 40), qa('x', -10))),
    'sweep_b': P(body=qa('y', -35), head=qa('y', -20), armr=qa('z', -45), arml=qa('z', 20), tend=qmul(qa('y', -70), qa('x', 40))),
    'roar': P(0.05, body=qa('x', -10), head=qa('x', -28), armr=qmul(qa('z', -50), qa('x', 10)), arml=qmul(qa('z', 50), qa('x', 10)), tend=qa('x', -22)),
    'call': P(0.12, body=qa('x', -8), head=qa('x', -24), armr=qa('z', -160), arml=qa('z', 160), tend=qa('x', -18)),
    'fall': P(-0.55, body=qa('x', 30), head=qa('x', 38), armr=qa('x', -40), arml=qa('x', -30), legr=qa('x', -40), legl=qa('x', -34), tend=qa('x', 30)),
}
FLEX = {'slam_up', 'roar'}             # (these wear the bent-elbow arms, as in the art)


def part_xf(pose, p):
    return pose[p], (0.0, pose['_dy'], 0.0)

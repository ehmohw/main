"""The Malevolent Snowbeast (2.88), a Dread boss - after the owner's drawing: Pistachio's living top hat, frightened, came down
on a snowman and made a monster of it. A huge bottom ball, a bulky middle ball with three coal buttons and a dark-blue bow tie,
and a round head: angry slanted eyes, a crooked curling carrot, and a great jagged maw of cyan ice that splits the face and
hangs down over the neck. Thick, angular branch arms with twig claws (one flung up). On top, the tall dark-grey top hat with
its red band, flaring a little at the crown - and its own small angry eyes and a fanged scowl.

A rigkit rig: body (the two lower balls, the buttons, the bow tie), head (the face per expression), the ice jaw (it drops to
roar), the hat (it bobs on its own), the two arms. Design units: feet at y=0, facing -z, its right is +x."""
import math
import random
from PIL import Image, ImageDraw

from phase57_art import hexc
from tullius_art import _noise, _shine
from rigkit import shrink, qs, el, chain

PREFIX = 'sb_'
RIG_SCALE = 1.5
PIVOT = {'body': (0, 0.0, 0), 'head': (0, 27.0, 0), 'jaw': (0, 32.4, -4.6), 'hat': (0, 40.5, 0), 'armr': (7.4, 23.5, 0), 'arml': (-7.4, 23.5, 0)}
PARENT = {'body': None, 'head': 'body', 'jaw': 'head', 'hat': 'head', 'armr': 'body', 'arml': 'body'}
PARTS = tuple(PIVOT)
PART_K = {'body': 1.25}                    # (the great body built at full size, kept inside the model box)
FACES = ('roar', 'squint')
SNOW, SNOW_SH, ICE, ICE_LT, ICE_DK, COAL, HAT, BAND = '#e8ecee', '#c4ccd2', '#3ed8f0', '#9ae6f8', '#1a90b8', '#222224', '#46463f', '#c8392b'
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)


def HIDDEN(p, pose):
    return False


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def _snow(seed, base=SNOW):
    im = _noise(base, seed, 4); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for _ in range(30):
        x, y = rnd.randrange(64), rnd.randrange(64)
        d.point((x, y), fill=hexc(rnd.choice(['#ffffff', '#dfe5e8', '#d2dade'])))
    return im


def _under():
    im = _snow(2881, SNOW_SH); px = im.load()
    for y in range(64):
        for x in range(64):
            r, g, b, a = px[x, y]; k = y / 63 * 0.2
            px[x, y] = (int(r * (1 - k)), int(g * (1 - k)), int(b * (1 - k * 0.5)), a)
    return im


def _face(kind=None):
    """the front of the head: two angry slanted eyes - a black wedge each, a white glint - with hard brows, and the top of the
    ice maw: a cyan gash with white fangs at its corners, running down off the bottom"""
    im = _snow(2882); d = ImageDraw.Draw(im)
    squint = kind == 'squint'
    for sx in (-1, 1):                                                                                   # the eyes: angry wedges
        cx = 32 + sx * 14
        inner, outer = cx - sx * 9, cx + sx * 9
        top_in, top_out = (18, 12) if not squint else (19, 15)
        d.polygon([(inner, top_in + 2), (outer, top_out), (outer, top_out + 6), (cx, 26 if not squint else 23), (inner, top_in + 6)], fill=hexc(COAL))
        d.polygon([(cx - sx * 3, 20), (cx + sx * 3, 18), (cx + sx * 2, 21)], fill=hexc('#f4f8fa'))     # (the glint)
        d.line((inner + sx * 1, top_in - 2, outer, top_out - 6), fill=hexc('#9aa4ac'), width=2)          # (a creased brow)
    top = 38 if kind != 'roar' else 36
    pts = [(10, top + 6), (16, top), (22, top + 8), (32, top + 14), (42, top + 8), (48, top), (54, top + 6), (58, 64), (6, 64)]
    d.polygon(pts, fill=hexc(ICE))                                                                     # the maw (its top half)
    for x0 in (12, 20, 40, 48):
        d.line((x0, top + 6, x0 + 3, 63), fill=hexc(ICE_LT), width=2)
    d.line(pts[:7], fill=hexc('#14181c'), width=2)
    for x, y in ((14, top + 3), (50, top + 3)):                                                         # white fangs at its corners
        d.polygon([(x - 3, y), (x + 3, y), (x, y + 9)], fill=hexc('#f4f8fa'), outline=hexc('#14181c'))
    return im


def _ice(seed):
    """the ice of the maw: cyan, cracked with pale streaks"""
    im = _noise(ICE, seed, 7); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for _ in range(8):
        x, y = rnd.randrange(64), rnd.randrange(64)
        d.line((x, y, x + rnd.randint(-4, 4), y + rnd.randint(6, 16), x + rnd.randint(-6, 6), y + rnd.randint(16, 26)), fill=hexc(ICE_LT), width=2)
    for _ in range(4):
        x, y = rnd.randrange(64), rnd.randrange(64)
        d.line((x, y, x + rnd.randint(-5, 5), y + rnd.randint(8, 14)), fill=hexc(ICE_DK))
    return im


def _jaw_front():
    """the maw's lower half, hanging over the neck: cyan ice with a jagged snow lower lip and two white fangs standing up"""
    im = _ice(2883); d = ImageDraw.Draw(im)
    d.polygon([(0, 64), (0, 50), (14, 58), (32, 40), (50, 58), (64, 50), (64, 64)], fill=hexc(SNOW))
    d.line([(0, 50), (14, 58), (32, 40), (50, 58), (64, 50)], fill=hexc('#14181c'), width=2)
    for x in (12, 52):
        d.polygon([(x - 3, 56), (x + 3, 56), (x, 44)], fill=hexc('#f4f8fa'), outline=hexc('#14181c'))
    return im


def _hat():
    im = _noise(HAT, 2884, 4); d = ImageDraw.Draw(im); rnd = random.Random(2884)
    for _ in range(14):
        x = rnd.randrange(64); d.line((x, 0, x + rnd.randint(-2, 2), 63), fill=hexc('#3e3e38'))
    return im


def _hat_top():
    """the hat's upper front (the crown): its small angry eyes, up near the top"""
    im = _hat(); d = ImageDraw.Draw(im)
    for sx in (-1, 1):
        cx = 32 + sx * 18
        d.ellipse((cx - 3, 28, cx + 3, 38), fill=hexc('#121212'))
        d.point((cx - 1, 30), fill=hexc('#ffffff'))
        d.line((cx - sx * 5, 22, cx + sx * 6, 26), fill=hexc('#121212'), width=2)                     # (cross little brows)
    return im


def _hat_low():
    """the hat's lower front: a jagged scowl with one fang"""
    im = _hat(); d = ImageDraw.Draw(im)
    d.line([(14, 34), (18, 30), (22, 33), (28, 26), (38, 22), (48, 24), (54, 30)], fill=hexc('#121212'), width=2)
    d.polygon([(44, 24), (49, 25), (46, 34)], fill=hexc('#f4f4ee'), outline=hexc('#121212'))
    return im


def _carrot():
    im = _noise('#b8641c', 2886, 6); d = ImageDraw.Draw(im)
    for y in range(4, 64, 10):
        d.arc((-8, y - 8, 72, y + 8), 20, 160, fill=hexc('#7a3e10'))
    return im


def _branch(seed):
    im = _noise('#5c472c', seed, 6); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for _ in range(10):
        x = rnd.randrange(64); d.line((x, 0, x + rnd.randint(-3, 3), 63), fill=hexc('#46361f'))
    return im


def textures():
    return {'sb_snow': _snow(2887), 'sb_snow2': _snow(2888), 'sb_under': _under(), 'sb_face': _face(), 'sb_ice': _ice(2889), 'sb_jaw': _jaw_front(),
            'sb_hat': _hat(), 'sb_hat_top': _hat_top(), 'sb_hat_low': _hat_low(), 'sb_brim': _noise('#141412', 2885, 3), 'sb_band': _noise(BAND, 2890, 5),
            'sb_carrot': _carrot(), 'sb_tie': _noise('#0e1696', 2891, 5), 'sb_branch': _branch(2892), 'sb_twig': _noise('#3e2e18', 2893, 5),
            'sb_coal': _noise(COAL, 2894, 4), **{f'sb_face_{k}': _face(k) for k in FACES}}


# ---------------------------------------------------------------------------------------------------- models
def models():
    M = {}
    def part(name, els):
        k_ = PART_K.get(name[len(PREFIX):], 1.0)
        els = shrink(els, k_) if k_ != 1.0 else els
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)

    def ball(y0, y1, r, pv, tex='sb_snow', top_r=None):
        """a blocky snowball (a core and crossed boxes round its corners off); top_r narrows its upper part"""
        h = y1 - y0; c = r * 0.78; tr = top_r or r
        return [el((-r, y0 + h * 0.14, -c), (r, y0 + h * 0.6, c), tex, pv, shift=(0.3, 0.2)),
                el((-tr, y0 + h * 0.58, -tr * 0.78), (tr, y1 - h * 0.14, tr * 0.78), tex, pv, shift=(0.5, 0.6)),
                el((-c, y0 + h * 0.14, -r), (c, y1 - h * 0.14, r), tex, pv, shift=(0.6, 0.4)),
                el((-c, y0, -c), (c, y1, c), tex, pv, shift=(0.1, 0.7)),
                el((-c + 0.4, y0 - 0.02, -c + 0.4), (c - 0.4, y0, c - 0.4), 'sb_under', pv, faces=('down',))]

    # ---- the body: the great bottom ball (narrowing at its top), the bulky middle ball, three coal buttons, the bow tie
    pv = PIVOT['body']
    body = ball(0.0, 17.0, 10.5, pv, top_r=8.4) + ball(15.6, 28.0, 8.6, pv, 'sb_snow2')
    for y, z in ((19.4, -8.8), (17.2, -8.6), (14.6, -8.4)):                                               # coal buttons
        body.append(el((-1.0, y, z - 0.6), (1.0, y + 1.8, z + 0.4), 'sb_coal', pv))
    body += [el((-4.2, 20.6, -9.2), (-1.0, 23.6, -8.4), 'sb_tie', pv, rot=('z', 14, (-1.0, 22.1, -8.8))),          # the bow tie
             el((1.0, 20.6, -9.2), (4.2, 23.6, -8.4), 'sb_tie', pv, rot=('z', -14, (1.0, 22.1, -8.8))),
             el((-1.3, 21.0, -9.6), (1.3, 23.4, -8.4), 'sb_tie', pv)]
    part('sb_body', body)

    # ---- the head: the round top ball, its face, the crooked curling carrot
    pv = PIVOT['head']
    def head(face=None):
        ft = 'sb_face' if face is None else f'sb_face_{face}'
        h = ball(26.6, 41.0, 8.2, pv)
        h += [el((-6.4, 28.6, -8.22), (6.4, 39.2, -8.2), ft, pv, faces=('north',), uv={'north': [0, 0, 16, 16]})]
        h += chain([(0, 35.4, -8.2), (0.4, 35.6, -11.0), (1.8, 34.4, -13.0), (3.0, 32.6, -13.2), (3.4, 31.0, -12.2)], [2.0, 1.6, 1.2, 0.8], 2.1, 'sb_carrot', pv, FRONT, ext=0.1)
        return h
    part('sb_head', head())
    for fc in FACES:
        part(f'sb_head_x{fc}', head(fc))

    # ---- the ice jaw: the maw's lower half - a wedge of cyan ice hanging down over the neck
    pv = PIVOT['jaw']
    part('sb_jaw', [el((-6.8, 23.4, -9.8), (6.8, 32.4, -4.4), 'sb_ice', pv, shift=(0.4, 0.2)),
                    el((-6.8, 23.4, -9.82), (6.8, 32.4, -9.8), 'sb_jaw', pv, faces=('north',), uv={'north': [0, 0, 16, 16]}),
                    el((-5.0, 21.6, -9.0), (5.0, 23.6, -5.0), 'sb_ice', pv),                                         # (its point)
                    el((-7.6, 27.0, -8.6), (-6.6, 32.4, -5.4), 'sb_ice', pv), el((6.6, 27.0, -8.6), (7.6, 32.4, -5.4), 'sb_ice', pv)])

    # ---- the hat: the wide brim (its ends curling up, black under), the crown flaring toward the top, the red band
    pv = PIVOT['hat']
    hat = [el((-8.4, 40.00, -7.4), (8.4, 41.40, 7.4), 'sb_hat', pv, shift=(0.2, 0.4)),
           el((-8.4, 39.98, -7.4), (8.4, 40.00, 7.4), 'sb_brim', pv, faces=('down',)),
           el((-10.4, 40.60, -6.2), (-8.2, 42.60, 6.2), 'sb_hat', pv, rot=('z', -22.5, (-8.4, 41.00, 0))),             # (its curled-up ends)
           el((8.2, 40.60, -6.2), (10.4, 42.60, 6.2), 'sb_hat', pv, rot=('z', 22.5, (8.4, 41.00, 0))),
           el((-5.2, 41.40, -4.8), (5.2, 49.40, 4.8), 'sb_hat', pv, shift=(0.5, 0.1)),
           el((-5.2, 41.40, -4.82), (5.2, 49.40, -4.8), 'sb_hat_low', pv, faces=('north',), uv={'north': [0, 0, 16, 16]}),
           el((-5.8, 49.20, -5.4), (5.8, 57.00, 5.4), 'sb_hat', pv, shift=(0.3, 0.6)),
           el((-5.8, 49.20, -5.42), (5.8, 57.00, -5.4), 'sb_hat_top', pv, faces=('north',), uv={'north': [0, 0, 16, 16]}),
           el((-5.35, 41.40, -4.95), (5.35, 43.40, 4.95), 'sb_band', pv)]
    part('sb_hat', hat)

    # ---- the arms: thick, crooked branches - a bend at the elbow, a spur, and three long twig claws
    def arm(sx):
        pv = PIVOT['armr' if sx > 0 else 'arml']; x0, y0, _ = pv
        ex, ey = sx * 14.5, 28.0
        wx, wy = sx * 19.0, 20.0
        a = chain([(x0 - sx * 0.6, y0, 0), (ex, ey, -0.4)], [3.0], 3.2, 'sb_branch', pv, FRONT, ext=0.4)
        a += chain([(ex, ey, -0.4), (wx, wy, -1.4)], [2.4], 2.5, 'sb_branch', pv, FRONT, ext=0.3)
        a += chain([(ex * 0.82, ey - 0.6, -0.2), (ex * 0.92, ey + 4.6, 0.2), (ex * 0.86, ey + 6.6, 0.4)], [0.9, 0.6], 0.9, 'sb_twig', pv, FRONT, ext=0.1)   # (a spur)
        for dx, dy, dz in ((2.6, -2.0, -1.6), (0.6, -4.6, -2.4), (-1.6, -3.6, -1.2)):                             # twig claws
            a += chain([(wx, wy, -1.4), (wx + sx * dx, wy + dy, -1.4 + dz), (wx + sx * dx * 1.3, wy + dy * 1.5, -1.4 + dz * 1.4)], [0.8, 0.5], 0.8, 'sb_twig', pv, FRONT, ext=0.05)
        return a
    part('sb_armr', arm(1)); part('sb_arml', arm(-1))
    return M


# ---------------------------------------------------------------------------------------------------- poses
def P(**kw):
    return kw


def arm(sx, up=0.0, fwd=0.0, twist=0.0):
    """raise (up: out and over, away from the body), swing forward (fwd), twist"""
    return qs(('y', twist * sx), ('x', -fwd), ('z', -up * sx))


# the drawing: its right arm flung up high, the left angled down and out, the hat tipped, leaning in
IDLE = dict(body=qs(('x', 4)), armr=arm(1, 70, 10), arml=arm(-1, -10, 14), hat=qs(('z', 6)), head=qs(('x', 6)))
POSES = {
    'idle_a': P(**IDLE),
    'idle_b': P(_face='squint', _off=(0, -0.4, 0), body=qs(('x', 4), ('z', -3)), head=qs(('x', 4), ('z', 8)), hat=qs(('z', -6), ('x', -4)),
                jaw=qs(('x', 8)), armr=arm(1, 80, 20), arml=arm(-1, -4, 22)),
    # it can't step - it lurches, rocking from ball to ball
    **{f'walk_{k}': P(_off=(0, 0.6 * abs(math.sin(math.pi * k / 2)), 0), body=qs(('z', 7 * math.sin(math.pi * k / 2)), ('x', 6)),
                      head=qs(('z', -5 * math.sin(math.pi * k / 2))), hat=qs(('z', 6 * math.sin(math.pi * k / 2 + 0.6))),
                      armr=arm(1, 30, 20 * math.sin(math.pi * k / 2)), arml=arm(-1, 0, -20 * math.sin(math.pi * k / 2))) for k in range(4)},
    # the throw (ice shards): the right arm wound back high - and flung
    'throw_up': P(_face='squint', body=qs(('y', 18)), head=qs(('y', -10)), armr=arm(1, 110, -40), arml=arm(-1, -6, 30), hat=qs(('x', -8))),
    'throw': P(_face='roar', body=qs(('y', -16), ('x', 6)), head=qs(('y', 8)), jaw=qs(('x', 18)), armr=arm(1, 30, 90), arml=arm(-1, -10, -10), hat=qs(('x', 6))),
    # the slam (frost nova): both arms high - and down into the ground
    'slam_up': P(_face='roar', _off=(0, 1.0, 0), body=qs(('x', -8)), head=qs(('x', -14)), jaw=qs(('x', 24)), armr=arm(1, 140, 10), arml=arm(-1, 140, 10), hat=qs(('x', -12))),
    'slam': P(_face='roar', _off=(0, -1.4, 0), body=qs(('x', 14)), head=qs(('x', 10)), jaw=qs(('x', 10)), armr=arm(1, -20, 90), arml=arm(-1, -20, 90), hat=qs(('x', 14))),
    # the roar (the blizzard): head back, the ice jaw dropped wide, arms flung out, the hat lifting with it
    'roar': P(_face='roar', body=qs(('x', -6)), head=qs(('x', -22)), jaw=qs(('x', 34)), hat=qs(('x', -16)), armr=arm(1, 90, 0, 20), arml=arm(-1, 90, 0, 20)),
    'hurt': P(_face='roar', body=qs(('x', -10), ('z', 6)), head=qs(('x', -12)), jaw=qs(('x', 20)), armr=arm(1, 60, -20), arml=arm(-1, 40, -10), hat=qs(('z', -14))),
    # rising out of the snow
    'spawn': P(_off=(0, -12.0, 0), body=qs(('x', 20)), head=qs(('x', 24)), armr=arm(1, -30, 40), arml=arm(-1, -30, 40)),
    # falling apart: the head slumps, the arms drop, the hat tips off
    'die': P(_face='squint', _off=(0, -3.0, 0), body=qs(('x', 18), ('z', 10)), head=qs(('x', 30), ('z', -20)), jaw=qs(('x', 30)), hat=qs(('z', 50), ('x', 30)),
             armr=arm(1, -50, 0), arml=arm(-1, -60, 10)),
}
DRAFT = ['idle_a', 'idle_b', 'walk_1', 'throw_up', 'throw', 'slam_up', 'slam', 'roar', 'hurt', 'die']

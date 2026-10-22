"""The Watchful Witch (2.88), a Dread boss - after the owner's drawing: an old acquaintance of Cecil's who went too deep into dark
magic and was swallowed by it. A deep wine-red hooded robe, hourglass in shape, flowing down to a hem that curls out into
points; two curly pigtails springing out of the top of the hood, a fringe of hair under it; no face left inside - only a dark
purple shadow, two almond green eyes glowing, and a dark jagged grin with lines running down from its corners; wide straight
sleeves held out, and thin black spiky hands. She doesn't walk. She drifts.

A rigkit rig: body (the robe and its curling hem), head (the hood, the face per expression, the pigtails), the arms in two
pieces (the sleeve to the elbow, then the wide cuff and the claws). Design units: hem at y=0, facing -z, her right is +x."""
import math
import random
from PIL import Image, ImageDraw

from phase57_art import hexc
from tullius_art import _noise, _shine
from rigkit import qs, el, chain

PREFIX = 'ww_'
RIG_SCALE = 1.15
PIVOT = {'body': (0, 8.0, 0), 'head': (0, 26.0, 0), 'armr': (4.4, 24.6, 0), 'forer': (9.8, 24.0, 0), 'arml': (-4.4, 24.6, 0), 'forel': (-9.8, 24.0, 0)}
PARENT = {'body': None, 'head': 'body', 'armr': 'body', 'forer': 'armr', 'arml': 'body', 'forel': 'arml'}
PARTS = tuple(PIVOT)
PART_K = {}
FACES = ('cackle', 'glare')
ROBE, ROBE_DK, ROBE_LT, HAIR, HAIR_DK, SHADE, GREEN = '#4c1428', '#2c0a18', '#6e2238', '#7a2c4a', '#4e1a30', '#1e1028', '#4aff3a'
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)


def HIDDEN(p, pose):
    return False


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def _robe(seed, base=ROBE):
    """heavy wine-red cloth: faint long folds and a mottled weave"""
    im = _noise(base, seed, 5); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for _ in range(10):
        x = rnd.randrange(64)
        d.line((x, 0, x + rnd.randint(-3, 3), 63), fill=hexc(ROBE_DK if rnd.random() < 0.6 else ROBE_LT))
    for _ in range(60):
        d.point((rnd.randrange(64), rnd.randrange(64)), fill=hexc('#5a1a30'))
    return im


def _face(kind=None):
    """the shadow inside the hood (uv [0, 0, 16, 16] of 7 x 6.4): dark purple, almond green eyes with lashes, and the dark jagged
    grin - wide, its lower edge toothed - with a line running down from each corner"""
    im = Image.new('RGBA', (64, 64), hexc(SHADE)); d = ImageDraw.Draw(im); rnd = random.Random(2903)
    for _ in range(60):
        d.point((rnd.randrange(64), rnd.randrange(64)), fill=hexc('#281636'))
    ey = 20 if kind != 'glare' else 22
    for cx in (19, 45):                                                                                  # almond eyes
        if kind == 'glare':
            d.polygon([(cx - 9, ey), (cx + 9, ey - 1), (cx + 6, ey + 4), (cx - 6, ey + 4)], fill=hexc(GREEN))
        else:
            d.polygon([(cx - 10, ey + 1), (cx - 4, ey - 5), (cx + 4, ey - 5), (cx + 10, ey + 1), (cx + 4, ey + 6), (cx - 4, ey + 6)], fill=hexc('#1e8a16'))
            d.polygon([(cx - 7, ey + 1), (cx - 3, ey - 3), (cx + 3, ey - 3), (cx + 7, ey + 1), (cx + 3, ey + 4), (cx - 3, ey + 4)], fill=hexc(GREEN))
            d.rectangle((cx - 1, ey - 2, cx, ey - 1), fill=hexc('#eaffd8'))
        for k in (-1, 1):                                                                                # (lashes)
            d.line((cx + k * 9, ey - 2, cx + k * 11, ey - 5), fill=hexc('#0a0612'))
    top = 36 if kind != 'cackle' else 34
    bot = top + (10 if kind != 'cackle' else 16)
    d.polygon([(6, top - 4), (32, top + 2), (58, top - 4), (52, bot - 2), (12, bot - 2)], fill=hexc('#0a0410'))   # the grin
    for i, x in enumerate(range(14, 52, 6)):                                                            # its jagged lower edge
        d.polygon([(x, bot - 2), (x + 6, bot - 2), (x + 3, bot - 7)], fill=hexc(SHADE))
    d.line((6, top - 4, 32, top + 2, 58, top - 4), fill=hexc('#0a0410'), width=2)
    for x0 in (16, 48):                                                                                 # the lines down from its corners
        d.line((x0, top + 2, x0 + (2 if x0 < 32 else -2), 63), fill=hexc('#0a0410'), width=2)
    return im


def _fringe():
    """the fringe under the hood's rim: hair locks hanging in points"""
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 63, 30), fill=hexc(HAIR))
    for x in range(0, 64, 10):
        d.polygon([(x, 30), (x + 10, 30), (x + 6, 50)], fill=hexc(HAIR))
        d.line((x + 2, 4, x + 6, 44), fill=hexc(HAIR_DK))
    return im


def _hair():
    im = _noise(HAIR, 2904, 6); d = ImageDraw.Draw(im)
    for y in range(0, 64, 9):
        d.arc((-10, y - 6, 74, y + 10), 10, 170, fill=hexc(HAIR_DK), width=2)
    return im


def _hem():
    """the hem's curling points: the robe colour, a lighter fold down each"""
    im = _robe(2901, ROBE); d = ImageDraw.Draw(im)
    for x in range(4, 64, 16):
        d.line((x, 0, x + 6, 63), fill=hexc(ROBE_LT), width=3)
    return im


def textures():
    return {'ww_robe': _robe(2906), 'ww_robe_dk': _robe(2907, ROBE_DK), 'ww_hem': _hem(), 'ww_face': _face(), 'ww_hair': _hair(), 'ww_fringe': _fringe(),
            'ww_cuff': _noise(ROBE_DK, 2908, 4), 'ww_inner': _noise('#14081a', 2909, 3), 'ww_claw': _shine('#06040a', '#3a2a4a', 2905),
            'ww_button': _noise('#8a3a5a', 2910, 4), **{f'ww_face_{k}': _face(k) for k in FACES}}


# ---------------------------------------------------------------------------------------------------- models
def models():
    M = {}
    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)

    # ---- the body: an hourglass robe - the bodice, the waist, the hips, then narrowing again before the hem flares out and
    #      curls up into points all round
    pv = PIVOT['body']
    body = [el((-4.0, 19.0, -2.8), (4.0, 26.6, 2.8), 'ww_robe', pv, shift=(0.3, 0.1)),                 # the bodice
            el((-3.2, 14.0, -2.4), (3.2, 19.2, 2.4), 'ww_robe', pv, shift=(0.5, 0.4)),                 # the waist
            el((-4.4, 8.0, -3.2), (4.4, 14.2, 3.2), 'ww_robe', pv, shift=(0.2, 0.6)),                  # the hips
            el((-4.6, 3.0, -3.4), (4.6, 8.2, 3.4), 'ww_robe', pv, shift=(0.7, 0.2)),                   # flaring toward the hem
            el((-6.8, 0.0, -5.2), (6.8, 3.4, 5.2), 'ww_robe', pv, shift=(0.4, 0.8)),                   # the hem's wide swell
            el((-7.8, 0.0, -3.6), (7.8, 2.2, 3.6), 'ww_robe_dk', pv), el((-5.0, 0.0, -6.2), (5.0, 2.2, 6.2), 'ww_robe_dk', pv),
            el((-0.4, 22.0, -3.0), (0.4, 23.0, -2.8), 'ww_button', pv)]                                # (the robe's one button)
    for j in range(8):                                                                                  # the curling points of the hem
        a = 2 * math.pi * (j + 0.5) / 8
        cx, cz = 6.6 * math.cos(a), 5.0 * math.sin(a)
        ox, oz = 10.4 * math.cos(a), 8.4 * math.sin(a)
        body += chain([(cx, 1.2, cz), (ox, 0.8, oz), (ox * 0.92, 3.6, oz * 0.92)], [2.4, 1.2], 2.2, 'ww_hem', pv, FRONT, ext=0.1)
    part('ww_body', body)

    # ---- the head: the deep hood, the dark face inside, a fringe under its rim, and the two curly pigtails springing out of
    #      the top of the hood (and a stray curl at one side)
    pv = PIVOT['head']
    def head(face=None):
        ft = 'ww_face' if face is None else f'ww_face_{face}'
        h = [el((-6.0, 26.2, -5.2), (6.0, 38.6, 4.6), 'ww_robe', pv, shift=(0.4, 0.2)),                          # the hood, deep and big
             el((-5.0, 38.4, -4.0), (5.0, 40.0, 3.6), 'ww_robe', pv, shift=(0.8, 0.5)),
             el((-6.02, 26.2, -5.6), (-4.6, 37.6, -4.2), 'ww_robe_dk', pv), el((4.6, 26.2, -5.6), (6.02, 37.6, -4.2), 'ww_robe_dk', pv),   # its rim
             el((-6.02, 35.8, -5.6), (6.02, 38.0, -4.2), 'ww_robe_dk', pv),
             el((-4.6, 26.6, -5.22), (4.6, 35.8, -5.2), ft, pv, faces=('north',), uv={'north': [0, 0, 16, 16]}),
             el((-4.6, 33.0, -5.26), (4.6, 35.8, -5.22), 'ww_fringe', pv, faces=('north',), uv={'north': [0, 0, 16, 10]}),
             el((-5.0, 25.4, -4.6), (5.0, 27.0, 4.0), 'ww_robe_dk', pv)]                                              # (the collar, bunched)
        for sx in (-1, 1):                                                                                          # the pigtails: puffy curly bunches
            h += [el((sx * 5.4 - 2.0, 35.6, -2.2), (sx * 5.4 + 2.0, 39.6, 2.0), 'ww_hair', pv, shift=(0.3, 0.3)),
                  el((sx * 7.4 - 2.0, 37.6, -1.8), (sx * 7.4 + 2.0, 41.4, 1.8), 'ww_hair', pv, shift=(0.6, 0.1), rot=('z', -22.5 * sx, (sx * 7.4, 39.5, 0))),
                  el((sx * 9.2 - 1.4, 36.4, -1.4), (sx * 9.2 + 1.4, 39.4, 1.4), 'ww_hair', pv, shift=(0.1, 0.6))]
            h += chain([(sx * 10.0, 37.0, 0.0), (sx * 10.8, 35.0, 0.0), (sx * 10.0, 33.6, 0.0)], [1.2, 0.8], 1.4, 'ww_hair', pv, FRONT, ext=0.1)   # (its curl)
        h += chain([(5.6, 29.0, -3.4), (6.8, 27.4, -3.6), (7.2, 25.6, -3.2), (6.2, 24.6, -3.0)], [1.2, 1.0, 0.7], 1.3, 'ww_hair', pv, FRONT, ext=0.1)   # (a stray curl)
        return h
    part('ww_head', head())
    for fc in FACES:
        part(f'ww_head_x{fc}', head(fc))

    # ---- the arms: straight wide sleeves, held out; a dark cuff, the dark inside, a thin black wrist and a spiky claw hand
    def upper(sx):
        pv = PIVOT['armr' if sx > 0 else 'arml']; x0, y0, _ = pv
        return chain([(x0, y0, 0), (sx * 9.8, 24.0, 0)], [2.6], 2.8, 'ww_robe', pv, (0.0, 1.0, 0.0), ext=0.4)
    def lower(sx):
        pv = PIVOT['forer' if sx > 0 else 'forel']; ex, ey, ez = pv
        cx = sx * 15.2
        a = chain([(ex, ey, ez), (cx, ey - 0.2, ez)], [3.4], 3.0, 'ww_robe', pv, (0.0, 1.0, 0.0), ext=0.1)
        a += chain([(cx - sx * 1.0, ey - 0.2, ez), (cx + sx * 0.1, ey - 0.2, ez)], [3.6], 3.6, 'ww_cuff', pv, (0.0, 1.0, 0.0), ext=0.0)
        a += chain([(cx, ey - 0.4, ez), (cx + sx * 2.2, ey - 0.6, ez)], [0.5], 0.5, 'ww_claw', pv, (0.0, 1.0, 0.0), ext=0.0)     # the thin wrist
        hx = cx + sx * 2.2
        for dy, dz, ln in ((1.6, -0.6, 2.2), (0.6, -1.0, 2.8), (-0.4, -0.6, 2.6), (-1.4, 0.2, 2.0), (1.0, 0.8, 1.8)):          # spiky fingers
            a += chain([(hx, ey - 0.6, ez), (hx + sx * ln * 0.7, ey - 0.6 + dy, ez + dz), (hx + sx * ln, ey - 0.6 + dy * 1.4, ez + dz * 1.3)],
                       [0.34, 0.22], 0.36, 'ww_claw', pv, FRONT, ext=0.05)
        return a
    part('ww_armr', upper(1)); part('ww_arml', upper(-1)); part('ww_forer', lower(1)); part('ww_forel', lower(-1))
    return M


# ---------------------------------------------------------------------------------------------------- poses
def P(**kw):
    return kw


def limb(sx, fwd=0.0, down=0.0, turn=0.0):
    """the arms are built held straight out: fwd swings them forward, down lowers them"""
    return qs(('y', fwd * sx + turn), ('z', down * sx))


HOVER = 3.0                                                                    # (she floats this far up off the ground)
# the drawing: arms held out wide and a little low, the hood tipped
IDLE = dict(armr=limb(1, 0, 18), forer=limb(1, 0, 4), arml=limb(-1, 0, 18), forel=limb(-1, 0, 4), head=qs(('x', 6)))
POSES = {
    'idle_a': P(_off=(0, HOVER, 0), **IDLE),
    'idle_b': P(_face='glare', _off=(0, HOVER + 1.0, 0), body=qs(('z', 3)), head=qs(('x', 4), ('z', -12)),
                armr=limb(1, 10, 10), forer=limb(1, 10, 6), arml=limb(-1, -6, 24), forel=limb(-1, 0, 6)),
    # drifting: leaning into it, the hem trailing, a slow bob, the arms swept back
    **{f'float_{k}': P(_off=(0, HOVER + 0.8 * math.sin(math.pi * k / 2), 0), body=qs(('x', 14), ('z', 3 * math.sin(math.pi * k / 2))),
                       head=qs(('x', -8)), armr=limb(1, -30, 30), forer=limb(1, -10, 6), arml=limb(-1, -30, 30), forel=limb(-1, -10, 6)) for k in range(4)},
    # the hex bolt: one hand drawn back, gathering green fire - then thrust out at you
    'cast_up': P(_face='glare', _off=(0, HOVER, 0), body=qs(('y', 16)), head=qs(('y', -10)), armr=limb(1, -40, -20), forer=limb(1, -30, 0), arml=limb(-1, 10, 20), forel=limb(-1, 0, 6)),
    'cast': P(_face='cackle', _off=(0, HOVER, -1.0), body=qs(('y', -14), ('x', 8)), head=qs(('y', 8)), armr=limb(1, 80, 0), forer=limb(1, 6, 0), arml=limb(-1, -20, 30), forel=limb(-1, 0, 10)),
    # the summoning (the curse circles, her shades): both arms flung up high, head thrown back, cackling
    'summon': P(_face='cackle', _off=(0, HOVER + 2.0, 0), body=qs(('x', -8)), head=qs(('x', -24)), armr=limb(1, 0, -50), forer=limb(1, 0, -20), arml=limb(-1, 0, -50), forel=limb(-1, 0, -20)),
    # the blink: folding into herself before she's gone
    'fold': P(_face='glare', _off=(0, HOVER - 2.0, 0), body=qs(('x', 30)), head=qs(('x', 30)), armr=limb(1, 80, 30), forer=limb(1, 60, 0), arml=limb(-1, 80, 30), forel=limb(-1, 60, 0)),
    # the drain: both claws reaching for you
    'drain': P(_face='glare', _off=(0, HOVER, -1.0), body=qs(('x', 12)), head=qs(('x', -6)), armr=limb(1, 75, 4), forer=limb(1, 10, 0), arml=limb(-1, 75, 4), forel=limb(-1, 10, 0)),
    'hurt': P(_face='glare', _off=(0, HOVER + 0.6, 1.0), body=qs(('x', -14)), head=qs(('x', -20)), armr=limb(1, -20, -20), forer=limb(1, 0, -10), arml=limb(-1, -20, -20), forel=limb(-1, 0, -10)),
    # rising out of a pool of shadow
    'spawn': P(_off=(0, -14.0, 0), body=qs(('x', 10)), head=qs(('x', 20)), armr=limb(1, 0, -70), forer=limb(1, 0, -10), arml=limb(-1, 0, -70), forel=limb(-1, 0, -10)),
    # unravelling: sinking, arms falling, the hood bowed
    'die': P(_face='glare', _off=(0, -3.0, 0), body=qs(('x', 20)), head=qs(('x', 40)), armr=limb(1, 10, 70), forer=limb(1, 0, 10), arml=limb(-1, 10, 70), forel=limb(-1, 0, 10)),
}
DRAFT = ['idle_a', 'idle_b', 'float_1', 'cast_up', 'cast', 'summon', 'fold', 'drain', 'hurt', 'die']

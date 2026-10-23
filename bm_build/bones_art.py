"""Bones (2.88): Emma's loyal pet shark, a guardian of the Underwater Kingdom - from the owner's art. A stout grey shark, a
pale belly sweeping up under his jaw, a heavy brow over a small black eye (a stitched scar across the left one), a big
grin of white triangle teeth, a faded skull-and-crossbones on his right flank, nicked fins. On land he swims inside a
ball of water held up by magic - the BUBBLE part, hidden in every swimming pose.

A rigkit rig: body (with the dorsal fin), head (an eye model per expression), jaw (it opens to bite), the two pectoral fins,
the tail in two pieces (it swishes) and the bubble. Design units: belly at y~4, facing -z, his right is +x."""
import math
import random
from PIL import Image, ImageDraw

from phase57_art import hexc
from tullius_art import _noise, _shine
from rigkit import shrink, qs, el, chain

PREFIX = 'bn_'
RIG_SCALE = 0.85
CY = 14.0                                                    # (the body's centre line, design units above the ground)
PIVOT = {'body': (0, CY, 0), 'head': (0, CY, -8.0), 'jaw': (0, CY - 3.0, -9.0), 'finr': (5.6, CY - 3.0, -3.0), 'finl': (-5.6, CY - 3.0, -3.0),
         'tail': (0, CY + 0.5, 9.0), 'tail2': (0, CY + 1.0, 18.0), 'bubble': (0, CY + 1.0, 2.0)}
PARENT = {'body': None, 'head': 'body', 'jaw': 'head', 'finr': 'body', 'finl': 'body', 'tail': 'body', 'tail2': 'tail', 'bubble': None}
PARTS = tuple(PIVOT)
PART_K = {'bubble': 1.25}                  # (the bubble built at full size, kept inside the model box)
FACES = ('happy', 'blink', 'angry')
GREY, GREY_DK, GREY_LT, BELLY = '#8a8e94', '#5c6066', '#a8acb2', '#d8dade'
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)


def HIDDEN(p, pose):
    return p == 'bubble' and not pose.get('_bubble', True)


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def _skin(seed, base=GREY):
    im = _noise(base, seed, 5); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for _ in range(10):
        x, y = rnd.randrange(64), rnd.randrange(64)
        d.line((x, y, x + rnd.randint(4, 10), y + rnd.randint(-1, 1)), fill=hexc(GREY_DK if base != GREY_DK else '#44484e'))
    return im


def _flank():
    """his right flank: grey above, the pale belly below, and the faded skull-and-crossbones"""
    im = _skin(2881); d = ImageDraw.Draw(im)
    d.rectangle((0, 44, 63, 63), fill=hexc(BELLY))
    for x in range(0, 64, 3):
        d.line((x, 44 - (x % 6) // 3, x + 3, 44), fill=hexc(BELLY))
    fade = hexc('#b4b6ba')
    d.line((20, 18, 44, 34), fill=fade, width=4); d.line((44, 18, 20, 34), fill=fade, width=4)       # the crossbones
    for cx, cy in ((19, 17), (45, 17), (19, 35), (45, 35)):
        d.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), fill=fade)
    d.ellipse((24, 12, 40, 28), fill=fade); d.rectangle((27, 24, 37, 31), fill=fade)                 # the skull
    d.ellipse((27, 17, 31, 21), fill=hexc('#70747a')); d.ellipse((33, 17, 37, 21), fill=hexc('#70747a'))
    d.polygon([(32, 22), (30, 25), (34, 25)], fill=hexc('#70747a'))
    return im


def _side(seed):
    im = _skin(seed); d = ImageDraw.Draw(im)
    d.rectangle((0, 44, 63, 63), fill=hexc(BELLY))
    for x in range(0, 64, 3):
        d.line((x, 44 - (x % 6) // 3, x + 3, 44), fill=hexc(BELLY))
    for k in range(4):                                                                             # gill slits
        d.line((6 + k * 4, 22, 4 + k * 4, 38), fill=hexc(GREY_DK), width=1)
    return im


def _face(kind=None):
    """the side of his head (each side mirrors it), after the owner's art (2.93b): a big black eye, its top cut flat by a heavy
    lid under a jutting brow - a grumpy half-lidded glare - a sliver of white glint low in it, and (2.93c) the red stitched
    scar running under the eye (the brow's ridge is a block of its own, on the model)"""
    im = _skin(2882); d = ImageDraw.Draw(im)
    d.rectangle((0, 50, 63, 63), fill=hexc(BELLY))
    ex, ey = 17, 21                                                  # (high, and forward over the snout's root, as drawn)
    INK, LID, LID_DK, SCAR = hexc('#101014'), hexc(GREY), hexc('#3a3d42'), hexc('#8a2a2a')
    # the lid's lower edge: how far down it comes (front and back of the eye), by mood
    lf, lb = {'angry': (ey + 1, ey - 3), 'happy': (ey + 1, ey + 1), 'blink': (ey + 5, ey + 5)}.get(kind, (ey - 1, ey - 2))
    if kind == 'blink':
        d.line((ex - 8, ey + 5, ex + 8, ey + 5), fill=INK, width=2)
    else:
        d.ellipse((ex - 10, ey - 7, ex + 10, ey + 9), fill=INK)                                      # the eye
        if kind == 'happy':                                                                        # (a pleased squint: the lower lid up)
            d.chord((ex - 9, ey + 2, ex + 9, ey + 12), 180, 360, fill=hexc(GREY))
        d.polygon([(ex - 3, ey + 1), (ex, ey + 1), (ex - 2, ey + 7)], fill=hexc('#ffffff'))       # the glint, a sliver
    d.polygon([(ex - 12, ey - 9), (ex + 12, ey - 9), (ex + 12, lb), (ex - 12, lf)], fill=LID)       # the heavy lid over it
    d.line((ex - 11, lf, ex + 11, lb), fill=INK, width=3)                                       # (its edge, inked)
    d.line((ex - 11, ey - 9, ex + 11, ey - 9), fill=LID_DK, width=1)                             # (under the brow)
    d.line((ex - 9, ey + 12, ex + 7, ey + 17), fill=SCAR, width=2)                               # the scar, under the eye...
    for t in range(5):
        cx, cy = ex - 7 + t * 3.5, ey + 12.6 + t * 1.1
        d.line((cx - 1, cy - 3, cx + 1, cy + 3), fill=SCAR)                                       # ...and its stitches across it
    return im


def _teeth():
    im = Image.new('RGBA', (64, 64), hexc('#7a2a2a')[:3] + (255,)); d = ImageDraw.Draw(im)
    for x in range(0, 64, 8):
        d.polygon([(x, 0), (x + 8, 0), (x + 4, 22)], fill=hexc('#f4f4f4'), outline=hexc('#b8b8b8'))
    d.rectangle((0, 40, 63, 63), fill=hexc('#c85a5a'))                                             # the tongue
    return im


def _bubble():
    """the water he swims in on land: each face a round pane of clear pale blue (clear outside the circle, so the box reads as
    a ball from any side), a brighter rim, a highlight and a few small bubbles"""
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((1, 1, 62, 62), fill=(120, 190, 240, 40), outline=(205, 238, 255, 120), width=1)
    d.ellipse((13, 10, 24, 17), fill=(255, 255, 255, 80))
    for x, y in ((42, 42), (48, 32), (36, 50)):
        d.ellipse((x - 2, y - 2, x + 2, y + 2), outline=(230, 250, 255, 150))
    return im


def textures():
    T = {'bn_skin': _skin(2883), 'bn_skin_dk': _skin(2884, GREY_DK), 'bn_belly': _noise(BELLY, 2885, 3), 'bn_flank': _flank(), 'bn_side': _side(2886),
         'bn_teeth': _teeth(), 'bn_bubble': _bubble(), 'bn_face': _face()}
    for k in FACES:
        T[f'bn_face_{k}'] = _face(k)
    return T


# ---------------------------------------------------------------------------------------------------- models
def models():
    M = {}
    def part(name, els):
        k_ = PART_K.get(name[len(PREFIX):], 1.0)
        els = shrink(els, k_) if k_ != 1.0 else els
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)
    y0 = CY
    # ---- the body: stout and rounded (a wide middle, tapering to the tail), the belly pale underneath; the skull on his right
    #      flank; the dorsal fin, swept back and nicked
    pv = PIVOT['body']
    body = [el((-5.4, y0 - 5.0, -8.0), (5.4, y0 + 5.0, 4.0), 'bn_skin', pv, shift=(0.3, 0.1)),
            el((-4.6, y0 - 4.4, 3.8), (4.6, y0 + 4.4, 9.4), 'bn_skin', pv, shift=(0.6, 0.4)),
            el((-5.42, y0 - 5.0, -8.0), (-5.4, y0 + 5.0, 4.0), 'bn_side', pv, faces=('west',), uv={'west': [0, 0, 16, 16]}),
            el((5.4, y0 - 5.0, -8.0), (5.42, y0 + 5.0, 4.0), 'bn_flank', pv, faces=('east',), uv={'east': [16, 0, 0, 16]}),
            el((-5.0, y0 - 5.4, -7.6), (5.0, y0 - 4.9, 3.6), 'bn_belly', pv),
            el((-4.2, y0 - 4.8, 3.6), (4.2, y0 - 4.3, 9.0), 'bn_belly', pv)]
    # (2.93c) the dorsal fin, by its side profile as drawn: a broad root along the back, the leading edge curving back, the
    #      trailing edge hollowed (a nick out of it low down), up to a point swept well back - stacked thin, thinner as it rises
    for i in range(8):
        t = i / 7
        zf, zb = -3.8 + 7.0 * t ** 1.25, 3.0 + 3.0 * t ** 2.2
        if i == 1: zb -= 0.9                                       # (the nick)
        hx = 0.85 - 0.45 * t
        body.append(el((-hx, y0 + 4.4 + 0.85 * i, zf), (hx, y0 + 4.4 + 0.85 * (i + 1) + 0.05, max(zb, zf + 0.6)), 'bn_skin_dk', pv, shift=(0.3 * i, 0.2 * i)))
    part('bn_body', body)
    # ---- the head: blunt and broad, the snout overhanging; the eyes on its sides; the upper teeth under the snout
    pv = PIVOT['head']
    def head(face=None):
        ft = 'bn_face' if face is None else f'bn_face_{face}'
        h = [el((-5.2, y0 - 2.6, -16.0), (5.2, y0 + 4.8, -7.6), 'bn_skin', pv, shift=(0.1, 0.3)),
             el((-4.2, y0 - 1.6, -19.6), (4.2, y0 + 3.6, -15.8), 'bn_skin', pv, shift=(0.5, 0.5)),            # the snout
             el((-3.0, y0 - 0.8, -21.0), (3.0, y0 + 2.6, -19.4), 'bn_skin', pv, shift=(0.7, 0.2)),
             el((-1.8, y0 + 0.4, -22.8), (1.8, y0 + 2.4, -20.8), 'bn_skin', pv, shift=(0.2, 0.7)),                  # (the pointed tip)
             el((-5.22, y0 - 2.6, -16.0), (-5.2, y0 + 4.8, -7.6), ft, pv, faces=('west',), uv={'west': [0, 0, 16, 14.2]}),
             el((5.2, y0 - 2.6, -16.0), (5.22, y0 + 4.8, -7.6), ft, pv, faces=('east',), uv={'east': [16, 0, 0, 14.2]}),
             # (the jutting brow over each eye: face texel row r is y0 + 4.8 - 0.13 r, column c is z -16 + 0.131 c)
             el((-5.6, y0 + 2.9, -15.5), (-5.2, y0 + 3.8, -12.4), 'bn_skin_dk', pv), el((5.2, y0 + 2.9, -15.5), (5.6, y0 + 3.8, -12.4), 'bn_skin_dk', pv),
             el((-4.0, y0 - 3.4, -19.2), (4.0, y0 - 1.6, -16.0), 'bn_teeth', pv, faces=('north', 'east', 'west', 'down'), uv={'north': [0, 0, 16, 6]}),
             el((-4.9, y0 - 3.0, -16.0), (4.9, y0 - 2.6, -8.0), 'bn_teeth', pv, faces=('down',), uv={'down': [0, 0, 16, 6]})]
        return h
    part('bn_head', head())
    for fc in FACES:
        part(f'bn_head_x{fc}', head(fc))
    # ---- the jaw: the pale lower jaw with its row of teeth standing up (it drops open to bite)
    pv = PIVOT['jaw']
    part('bn_jaw', [el((-4.6, y0 - 5.2, -18.6), (4.6, y0 - 3.0, -8.2), 'bn_belly', pv),
                    el((-4.4, y0 - 3.0, -18.4), (4.4, y0 - 1.8, -16.6), 'bn_teeth', pv, faces=('north', 'east', 'west', 'up'), uv={'north': [0, 0, 16, 5]}),
                    el((-4.4, y0 - 3.02, -16.6), (4.4, y0 - 3.0, -8.6), 'bn_teeth', pv, faces=('up',), uv={'up': [0, 10, 16, 16]})])
    # ---- the pectoral fins: long, swept back and down
    for sx, n in ((1, 'finr'), (-1, 'finl')):
        pv = PIVOT[n]; x0, fy, fz = pv
        part(f'bn_{n}', chain([(x0, fy, fz), (x0 + sx * 5.0, fy - 3.0, fz + 3.0), (x0 + sx * 8.4, fy - 6.0, fz + 7.6)], [(4.4, 1.6)][0], 0.8, 'bn_skin_dk', pv, FRONT, ext=0.3))
    # ---- the tail: the narrowing stalk, then the big crescent fin (upper lobe long)
    pv = PIVOT['tail']
    part('bn_tail', [el((-3.4, y0 - 3.0, 9.0), (3.4, y0 + 3.8, 14.0), 'bn_skin', pv, shift=(0.2, 0.6)),
                     el((-2.4, y0 - 1.8, 13.6), (2.4, y0 + 2.8, 18.4), 'bn_skin', pv, shift=(0.7, 0.3)),
                     el((-3.2, y0 - 3.1, 9.0), (3.2, y0 - 2.9, 14.0), 'bn_belly', pv)])
    pv = PIVOT['tail2']; tz = pv[2]; ty = pv[1]
    t2 = [el((-1.6, ty - 1.6, tz - 0.6), (1.6, ty + 1.8, tz + 2.4), 'bn_skin', pv)]
    t2 += chain([(0, ty + 0.4, tz + 1.0), (0, ty + 5.4, tz + 3.6), (0, ty + 9.4, tz + 6.2)], [(3.6, 1.0)][0], 1.0, 'bn_skin_dk', pv, FRONT, ext=0.3)
    t2 += chain([(0, ty - 0.4, tz + 1.0), (0, ty - 4.4, tz + 3.4), (0, ty - 7.0, tz + 5.4)], [(3.0, 0.8)][0], 1.0, 'bn_skin_dk', pv, FRONT, ext=0.3)
    part('bn_tail2', t2)
    # ---- the bubble: a rounded ball of water (a stack of boxes, clear blue), big enough to hold him curled
    pv = PIVOT['bubble']; by, bz = pv[1], pv[2]
    bub = [el((-16.0, by - 15.0, bz - 27.0), (16.0, by + 15.0, bz + 27.0), 'bn_bubble', pv, uv={f: [0, 0, 16, 16] for f in ('north', 'south', 'east', 'west', 'up', 'down')})]
    part('bn_bubble', bub)
    return M


# ---------------------------------------------------------------------------------------------------- poses
def P(**kw):
    return kw


def swish(a, b=0.0):
    return dict(tail=qs(('y', a)), tail2=qs(('y', b if b else a * 1.4)))


def fins(dn=0.0, back=0.0):
    return dict(finr=qs(('z', dn), ('y', back)), finl=qs(('z', -dn), ('y', -back)))


LAND = (0, 6.0, 0)                                        # (on land he floats in his bubble, a little up off the ground)
POSES = {
    'idle_a': P(_off=LAND, **swish(10), **fins(4)),
    'idle_b': P(_face='angry', _off=(0, 6.4, 0), **swish(-10), **fins(-4), head=qs(('y', 8))),
    **{f'walk_{k}': P(_off=(0, 6.0 + 0.4 * math.sin(math.pi * k / 2), 0), **swish(22 * math.sin(math.pi * k / 2)), **fins(6 * math.cos(math.pi * k / 2)),
                      body=qs(('y', -6 * math.sin(math.pi * k / 2)))) for k in range(4)},
    **{f'run_{k}': P(_off=(0, 6.0 + 0.6 * math.sin(math.pi * k / 2), 0), **swish(34 * math.sin(math.pi * k / 2)), **fins(12, 10),
                     body=qs(('y', -10 * math.sin(math.pi * k / 2)), ('x', 6))) for k in range(4)},
    'jump': P(_off=(0, 9.0, 0), body=qs(('x', -20)), **swish(0), **fins(16, 14)),
    # the bite: a lunge forward with the jaw dropped wide - then it snaps shut
    'bite_open': P(_face='angry', _off=(0, 6.0, -2.0), body=qs(('x', -8)), head=qs(('x', -14)), jaw=qs(('x', 38)), **swish(-20), **fins(10)),
    'bite': P(_face='angry', _off=(0, 6.0, -6.0), body=qs(('x', 6)), head=qs(('x', 4)), jaw=qs(('x', 0)), **swish(26), **fins(-6)),
    # the thrash (his charged move): rolling and tearing
    'thrash_a': P(_face='angry', _off=(0, 6.2, 0), body=qs(('z', 40), ('y', 20)), jaw=qs(('x', 30)), **swish(40)),
    'thrash_b': P(_face='angry', _off=(0, 6.2, 0), body=qs(('z', -40), ('y', -20)), jaw=qs(('x', 10)), **swish(-40)),
    # the charge: head down, tail driving
    'charge': P(_face='angry', _off=(0, 5.6, -4.0), body=qs(('x', 10)), head=qs(('x', 6)), jaw=qs(('x', 20)), **swish(30), **fins(14, 20)),
    # happy: a roll onto his back for Emma
    'happy': P(_face='happy', _off=(0, 6.4, 0), body=qs(('z', 150)), jaw=qs(('x', 18)), **swish(14), **fins(-20)),
    'wave_a': P(_face='happy', _off=LAND, finl=qs(('z', -40)), **swish(14)),
    # sitting: settled on the ground (in his bubble), resting, the jaw a little open; asleep on the second beat
    'sit_a': P(_off=(0, 2.0, 0), body=qs(('x', 4)), jaw=qs(('x', 8)), **swish(8), **fins(-10)),
    'sit_b': P(_face='blink', _off=(0, 1.8, 0), body=qs(('x', 4), ('z', 6)), jaw=qs(('x', 4)), **swish(-8), **fins(-12)),
    'hurt': P(_face='angry', _off=(0, 6.6, 0), body=qs(('x', -14), ('z', 12)), jaw=qs(('x', 24)), **swish(-24)),
    'tired': P(_face='blink', _off=(0, 2.0, 0), body=qs(('z', 30)), **swish(4)),
}
SWIM_FRAMES = 8
# (2.88b) on land his bubble rests on the ground - it used to hang half a block up (QC: every follower flush on the ground):
# every bubbled pose comes down 9 units, none below -3.0 (the bubble's bottom at the host's feet); a jump still leaves it
for _k, _v in POSES.items():
    if _v.get('_bubble', True) and '_off' in _v:
        _o = _v['_off']; _v['_off'] = (_o[0], max(_o[1] - 9.0, -3.0), _o[2])
for _i in range(SWIM_FRAMES):                             # (in water: no bubble - he's home; a long, easy S-wave)
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(_bubble=False, _off=(0, -4.0 + 0.6 * math.sin(_p), 0), body=qs(('y', 8 * math.sin(_p))),
                            head=qs(('y', -6 * math.sin(_p))), **swish(26 * math.sin(_p + 0.8), 40 * math.sin(_p + 1.6)), **fins(6 * math.sin(_p)))
DRAFT = ['idle_a', 'idle_b', 'walk_1', 'run_1', 'jump', 'bite_open', 'bite', 'thrash_a', 'charge', 'happy', 'sit_a', 'hurt', 'swim_2']

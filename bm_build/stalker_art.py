"""The Stalker (2.87) as a follower: the Dread Night's hunter (phase181's drawing), tamed - after the owner's drawing.
2.88: remodelled and repainted closer to it - the drawing's flat sage with its olive shadow side (no blotches); a big round bald
skull with two small black eyes, red at the centre, and pointed ears; a huge jagged maw gaping down the front of the face, the
jaw hanging, crooked teeth top and bottom round a dark red throat and a lolling tongue; a chest widening to bony shoulders,
the pecs and the ribs down its flanks; arms far too long, ending in three long hooked olive claws; long legs that now bend at
the knee (the shins their own parts) on long three-toed feet. And it can go on all fours: a crawl and a flat-out sprint.

A rigkit rig: body, head (the jaw a model per expression: shut-ish, gaping wide), the arms bent at the elbow, the legs at the
knee. Design units: feet at y=0, facing -z, its right is +x."""
import math
import random
from PIL import Image, ImageDraw

from phase57_art import hexc
from tullius_art import _noise, _shine
from rigkit import qs, el, chain

PREFIX = 'st_'
RIG_SCALE = 0.95
PIVOT = {'body': (0, 20.0, 0), 'legr': (1.5, 20.0, 0), 'legl': (-1.5, 20.0, 0), 'shinr': (1.5, 11.0, 0), 'shinl': (-1.5, 11.0, 0),
         'head': (0, 36.0, 0.6), 'armr': (4.6, 31.0, 0), 'forer': (5.0, 19.6, 0), 'arml': (-4.6, 31.0, 0), 'forel': (-5.0, 19.6, 0)}
PARENT = {'body': None, 'legr': None, 'legl': None, 'shinr': 'legr', 'shinl': 'legl', 'head': 'body', 'armr': 'body', 'forer': 'armr',
          'arml': 'body', 'forel': 'arml'}
PARTS = tuple(PIVOT)
PART_K = {}
FACES = ('wide', 'shut')
SKIN, SKIN_DK, SKIN_LT, INK = '#b8bc92', '#888d58', '#cdd0a8', '#22241a'   # (the drawing's sage, its olive shadow side)
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)


def HIDDEN(p, pose):
    return False


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
# (2.88: redrawn after the owner's drawing - the flat cartoon two-tone of it: clean sage with a soft olive shading, no
#  blotches; the shadow side its own darker texture; ink lines only where the drawing has them)
def _skin(seed, base=SKIN, n=0):
    """smooth skin: the faintest grain, a soft fall-off to the shadow tone at the bottom of each tile"""
    im = _noise(base, seed, 3); px = im.load(); lo = hexc(SKIN_DK if base != SKIN_DK else '#70744a')[:3]
    for y in range(64):
        k = max(0.0, (y - 40) / 24) * 0.35
        for x in range(64):
            p = px[x, y]
            px[x, y] = tuple(int(p[i] * (1 - k) + lo[i] * k) for i in range(3)) + (255,)
    return im


def _ribs(seed):
    """the chest's front, as drawn: the collarbones, the line of the pecs, the ribs showing down each flank, a navel"""
    im = _skin(seed); d = ImageDraw.Draw(im); ink, sh = hexc('#3e4228'), hexc(SKIN_DK)
    d.line((6, 7, 26, 11), fill=ink, width=2); d.line((58, 7, 38, 11), fill=ink, width=2)          # the collarbones
    d.arc((4, 6, 32, 30), 20, 160, fill=ink, width=2); d.arc((32, 6, 60, 30), 20, 160, fill=ink, width=2)   # the pecs
    for k, y in enumerate((30, 37, 44)):                                                           # ribs down each flank
        d.line((2, y, 12 - k, y + 4), fill=ink, width=2); d.line((61, y, 51 + k, y + 4), fill=ink, width=2)
    d.rectangle((2, 26, 9, 60), fill=sh)                                                           # (the shadowed flank)
    d.arc((29, 50, 35, 58), 0, 300, fill=ink, width=2)                                             # the navel
    return im


def _back(seed):
    """the back: the spine, the shoulder blades"""
    im = _skin(seed, SKIN_DK); d = ImageDraw.Draw(im); ink = hexc('#4a4e30')
    d.line((32, 2, 32, 62), fill=ink, width=2)
    d.arc((6, 6, 28, 30), 180, 330, fill=ink, width=2); d.arc((36, 6, 58, 30), 210, 360, fill=ink, width=2)
    return im


def _face(kind=None):
    """the front of the skull: smooth and bald, lit from the left (the drawing's light), the shading down its right"""
    im = _skin(1931, SKIN_LT); px = im.load(); dk = hexc(SKIN)[:3]
    for y in range(64):
        for x in range(64):
            k = max(0.0, (x - 40) / 24) * 0.6
            p = px[x, y]; px[x, y] = tuple(int(p[i] * (1 - k) + dk[i] * k) for i in range(3)) + (255,)
    return im


def _eye():
    """a small round black eye with a red pinpoint (the drawing's), a thin dark rim"""
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((0, 0, 63, 63), fill=hexc('#3a3c24')); d.ellipse((5, 5, 58, 58), fill=(8, 6, 6, 255))
    d.ellipse((24, 22, 38, 36), fill=hexc('#d01818')); d.ellipse((28, 26, 33, 31), fill=hexc('#ff6a5a'))
    return im


def _teeth():
    """jagged, crooked teeth - off-white, uneven - on the dark red gum"""
    im = Image.new('RGBA', (64, 64), hexc('#5a0c14')[:3] + (255,)); d = ImageDraw.Draw(im); rnd = random.Random(1939)
    x = 0
    while x < 64:
        w = rnd.randint(5, 9); h = rnd.randint(24, 54)
        d.polygon([(x, 0), (x + w, 0), (x + w // 2 + rnd.randint(-2, 2), h)], fill=hexc('#e6dfc0'), outline=hexc('#8a8468'))
        x += w - 1
    return im


def _maw():
    """the throat: dark red going black, the tongue lolling"""
    im = _noise('#6a141c', 1932, 6); d = ImageDraw.Draw(im)
    d.ellipse((10, 4, 54, 50), fill=hexc('#2c0408'))
    d.ellipse((14, 34, 50, 70), fill=hexc('#a8303a')); d.line((32, 40, 32, 63), fill=hexc('#7a1a22'), width=2)   # the tongue
    return im


def _claw():
    """a long hooked claw: olive like the hand, darkening to the point"""
    im = _noise(SKIN_DK, 1937, 3); px = im.load(); tip = hexc('#3c3e26')[:3]
    for y in range(64):
        k = y / 63
        for x in range(64):
            p = px[x, y]; px[x, y] = tuple(int(p[i] * (1 - k) + tip[i] * k) for i in range(3)) + (255,)
    return im


def textures():
    return {'st_skin': _skin(1933), 'st_shade': _skin(1934, SKIN_DK), 'st_ribs': _ribs(1935), 'st_back': _back(1936), 'st_face': _face(),
            'st_eye': _eye(), 'st_teeth': _teeth(), 'st_maw': _maw(), 'st_claw': _claw(), 'st_nail': _shine('#4a4c32', '#8a8c64', 1938)}


# ---------------------------------------------------------------------------------------------------- models
def models():
    M = {}
    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)

    # ---- the body (the drawing's): narrow hips, a pinched waist, a chest that widens up to bony shoulders - the pecs and the
    #      ribs down the flanks on its front, the spine and blades behind - and a thin neck rising from the back of them
    pv = PIVOT['body']
    body = [el((-2.6, 19.2, -1.4), (2.6, 22.0, 1.4), 'st_skin', pv, shift=(0.2, 0.4)),                 # the hips
            el((-1.7, 21.8, -1.1), (1.7, 25.0, 1.1), 'st_skin', pv, shift=(0.6, 0.1)),                 # the pinched waist
            el((-2.6, 24.8, -1.5), (2.6, 27.2, 1.5), 'st_skin', pv, shift=(0.1, 0.6)),                 # the lower ribs
            el((-3.6, 27.0, -1.8), (3.6, 31.2, 1.8), 'st_skin', pv, shift=(0.5, 0.2)),                 # the chest
            el((-3.6, 24.8, -1.82), (3.6, 31.2, -1.8), 'st_ribs', pv, faces=('north',), uv={'north': [0, 0, 16, 16]}),
            el((-3.6, 24.8, 1.8), (3.6, 31.2, 1.82), 'st_back', pv, faces=('south',), uv={'south': [0, 0, 16, 16]}),
            el((-5.0, 30.4, -1.3), (5.0, 31.8, 1.3), 'st_skin', pv, shift=(0.1, 0.7)),                 # the bony shoulders
            el((-0.75, 31.4, -0.2), (0.75, 37.0, 1.3), 'st_skin', pv, shift=(0.8, 0.1))]               # the thin neck
    body.append(el((2.6, 24.8, -1.3), (3.0, 31.0, 1.3), 'st_shade', pv))                              # (the shadowed flank)
    part('st_body', body)

    # ---- the head: a big round bald skull (stepped round), two small black eyes with red points, a pointed ear each side,
    #      and the maw - a huge jagged mouth gaping down the front of the face, the jaw hanging, crooked teeth top and bottom
    pv = PIVOT['head']
    def head(face=None):
        drop = {'wide': 2.4, 'shut': -1.6}.get(face, 0.0)                                              # (how far the jaw hangs)
        h = [el((-3.0, 39.0, -3.2), (3.0, 44.6, 3.0), 'st_skin', pv, shift=(0.3, 0.2)),               # the dome
             el((-3.4, 39.6, -2.8), (3.4, 43.8, 2.6), 'st_skin', pv, shift=(0.5, 0.5)),               # (rounded out at the temples)
             el((-2.6, 44.6, -2.6), (2.6, 45.6, 2.4), 'st_skin', pv, shift=(0.6, 0.6)),               # its crown
             el((-1.8, 45.6, -1.8), (1.8, 46.0, 1.6), 'st_skin', pv, shift=(0.2, 0.8)),
             el((-2.8, 38.2, -1.0), (2.8, 39.2, 3.0), 'st_shade', pv),                                # the back of the skull, under
             el((-3.0, 39.0, -3.22), (3.0, 44.6, -3.2), 'st_face', pv, faces=('north',), uv={'north': [0, 0, 16, 16]}),
             el((-2.2, 42.0, -3.28), (-0.9, 43.3, -3.22), 'st_eye', pv, faces=('north',), uv={'north': [0, 0, 16, 16]}),     # the eyes
             el((0.9, 42.0, -3.28), (2.2, 43.3, -3.22), 'st_eye', pv, faces=('north',), uv={'north': [0, 0, 16, 16]}),
             el((-2.7, 37.8, -4.2), (2.7, 39.4, 1.0), 'st_skin', pv, shift=(0.4, 0.5)),               # the upper jaw, jutting
             el((-2.7, 37.8, -4.22), (2.7, 39.4, -4.2), 'st_teeth', pv, faces=('north',), uv={'north': [0, 0, 16, 9]}),
             el((-2.7, 37.78, -4.2), (2.7, 37.8, 0.6), 'st_teeth', pv, faces=('down',), uv={'down': [0, 0, 16, 9]})]
        gap = 3.2 + drop
        if gap > 0.3:
            h += [el((-2.3, 37.8 - gap, -3.4), (2.3, 37.8, 0.8), 'st_maw', pv, faces=('north', 'east', 'west'), uv={'north': [0, 0, 16, 16]})]   # the throat
            for sx in (-1, 1):                                                                         # the stretched cheeks
                h.append(el((sx * 2.6 - 0.15, 37.8 - gap, -3.6), (sx * 2.6 + 0.15, 37.9, 0.4), 'st_shade', pv, faces=('east', 'west')))
        lo = 37.8 - gap
        h += [el((-2.5, lo - 1.1, -4.6), (2.5, lo, 0.8), 'st_skin', pv, shift=(0.2, 0.7)),             # the lower jaw, thrust out
              el((-2.5, lo - 1.1, -4.62), (2.5, lo - 0.6, -4.6), 'st_shade', pv, faces=('north',)),
              el((-2.3, lo, -4.4), (2.3, lo + 0.02, 0.6), 'st_maw', pv, faces=('up',), uv={'up': [0, 6, 16, 16]}),
              el((-2.3, lo, -4.42), (2.3, lo + 1.3, -4.4), 'st_teeth', pv, faces=('north',), uv={'north': [0, 16, 16, 7]})]
        for sx in (-1, 1):                                                                             # the ears, pointed, swept back and up
            h.append(el((sx * 3.3 - (0.0 if sx > 0 else 2.8), 40.6, 0.0), (sx * 3.3 + (2.8 if sx > 0 else 0.0), 41.6, 1.4), 'st_skin', pv,
                        rot=('z', 30.0 * sx, (sx * 3.3, 41.1, 0.7))))
            h.append(el((sx * 3.3 - (0.0 if sx > 0 else 1.4), 41.6, 0.2), (sx * 3.3 + (1.4 if sx > 0 else 0.0), 42.4, 1.2), 'st_shade', pv,
                        rot=('z', 30.0 * sx, (sx * 3.3, 41.1, 0.7))))
        return h
    part('st_head', head())
    for fc in FACES:
        part(f'st_head_x{fc}', head(fc))

    # ---- the arms: far too long - thin upper arms, a knob of an elbow, thin forearms reaching past the knee, a bony hand,
    #      and three long hooked claws curling up at the points (the outer one splayed), olive like the rest of it
    def upper(sx):
        pv = PIVOT['armr' if sx > 0 else 'arml']; x0, y0, _ = pv
        tex = 'st_skin' if sx > 0 else 'st_shade'
        return [el((x0 - 1.0, y0 - 1.2, -1.1), (x0 + 1.0, y0 + 0.9, 1.1), tex, pv)] + \
            chain([(x0, y0, 0), (sx * 5.0, 19.6, 0)], [1.2], 1.2, tex, pv, FRONT, ext=0.3)
    def lower(sx):
        pv = PIVOT['forer' if sx > 0 else 'forel']; ex, ey, _ = pv
        tex = 'st_skin' if sx > 0 else 'st_shade'
        wx, wy = sx * 5.2, 8.0
        a = [el((ex - 0.85, ey - 0.85, -0.85), (ex + 0.85, ey + 0.85, 0.85), tex, pv)]                   # the elbow's knob
        a += chain([(ex, ey, 0), (wx, wy, 0)], [1.0], 1.0, tex, pv, FRONT, ext=0.2)
        a += [el((wx - 0.9, wy - 2.2, -0.8), (wx + 0.9, wy + 0.2, 0.8), tex, pv, shift=(0.3, 0.6))]       # the hand, bony
        for k, dz in enumerate((-0.5, 0.0, 0.5)):
            out = (sx * 1.0 if k == 2 else sx * 0.2 * (k - 1))
            a += chain([(wx + out * 0.3, wy - 2.0, dz), (wx + out, wy - 5.6, dz - 0.5), (wx + out * 1.3, wy - 8.4, dz - 2.0),
                        (wx + out * 1.4, wy - 9.4, dz - 3.6)], [0.46, 0.38, 0.28], 0.46, 'st_claw', pv, FRONT, ext=0.05)
        return a
    part('st_armr', upper(1)); part('st_arml', upper(-1)); part('st_forer', lower(1)); part('st_forel', lower(-1))

    # ---- the legs: a long thigh down to a knotted knee (the shin its own part, so it can crouch and crawl); a long shin, a
    #      knobbly ankle, a long narrow foot with three long splayed toes and a spur of a heel
    def thigh(sx):
        pv = PIVOT['legr' if sx > 0 else 'legl']; cx = pv[0]
        tex = 'st_skin' if sx > 0 else 'st_shade'
        return [el((cx - 1.0, 11.4, -1.0), (cx + 1.0, 20.4, 1.0), tex, pv, shift=(0.2, 0.3)),
                el((cx - 1.15, 17.0, -1.15), (cx + 1.15, 20.6, 1.15), tex, pv, shift=(0.5, 0.1)),
                el((cx - 1.1, 10.4, -1.15), (cx + 1.1, 12.2, 1.0), tex, pv)]                             # the knee, knotted
    def shin(sx):
        pv = PIVOT['shinr' if sx > 0 else 'shinl']; cx = pv[0]
        tex = 'st_skin' if sx > 0 else 'st_shade'
        L = [el((cx - 0.7, 1.8, -0.7), (cx + 0.7, 10.8, 0.7), tex, pv, shift=(0.6, 0.2)),
             el((cx - 0.9, 1.2, -0.9), (cx + 0.9, 2.4, 0.9), tex, pv),                                 # the ankle
             el((cx - 0.95, 0.0, -3.0), (cx + 0.95, 1.2, 1.4), tex, pv, shift=(0.4, 0.8)),              # the long foot
             el((cx - 0.4, 0.0, 1.2), (cx + 0.4, 0.8, 2.2), tex, pv)]                                   # the heel's spur
        for dx, ln in ((-0.65, 2.2), (0.0, 2.8), (0.65, 2.2)):                                          # three long toes
            L.append(el((cx + dx - 0.25, 0.0, -3.0 - ln), (cx + dx + 0.25, 0.5, -2.9), tex, pv))
            L.append(el((cx + dx - 0.18, 0.0, -3.5 - ln), (cx + dx + 0.18, 0.35, -2.9 - ln), 'st_nail', pv))
        return L
    part('st_legr', thigh(1)); part('st_legl', thigh(-1)); part('st_shinr', shin(1)); part('st_shinl', shin(-1))
    return M


# ---------------------------------------------------------------------------------------------------- poses
def limb(sx, fwd=0.0, out=0.0, turn=0.0):
    return qs(('y', turn * sx), ('x', -fwd), ('z', -out * sx))


def P(**kw):
    return kw


# idle (the drawing): a forward stoop, the head tipped back over the gaping maw, one arm hanging long, the other's forearm
# raised with its claws up - and it sways
IDLE = dict(body=qs(('x', 10)), head=qs(('x', -30)), legr=limb(1, -4, 4), legl=limb(-1, -4, 4),
            armr=limb(1, 4, 8), forer=limb(1, 10), arml=limb(-1, 14, 22), forel=limb(-1, 112, -10))
POSES = {
    'idle_a': P(**IDLE),
    'idle_b': P(_face='wide', _off=(0, -0.2, 0), **dict(IDLE, body=qs(('x', 12), ('z', -4)), head=qs(('x', -38), ('z', 10)),
                                                        arml=limb(-1, 18, 26), forel=limb(-1, 120, -14), armr=limb(1, 6, 10), forer=limb(1, 16))),
    # walk: stilted, too-long strides, the claws swinging low
    'walk_a': P(_off=(0, 0.2, 0), body=qs(('x', 12), ('y', 6)), head=qs(('x', -28)), legr=limb(1, 26), legl=limb(-1, -24), armr=limb(1, -18, 8), forer=limb(1, 14),
                arml=limb(-1, 22, 8), forel=limb(-1, 14)),
    'walk_up': P(_off=(0, 0.7, 0), body=qs(('x', 12)), head=qs(('x', -30)), legr=limb(1, 4), legl=limb(-1, -4), armr=limb(1, 2, 8), forer=limb(1, 14), arml=limb(-1, 2, 8), forel=limb(-1, 14)),
    'walk_b': P(_off=(0, 0.2, 0), body=qs(('x', 12), ('y', -6)), head=qs(('x', -28)), legr=limb(1, -24), legl=limb(-1, 26), armr=limb(1, 22, 8), forer=limb(1, 14),
                arml=limb(-1, -18, 8), forel=limb(-1, 14)),
    # run: a lurching sprint, bent low, the claws flung out ahead
    'run_a': P(_off=(0, 0.2, 0), body=qs(('x', 34)), head=qs(('x', -44)), legr=limb(1, 52), legl=limb(-1, -40), armr=limb(1, 60, 18), forer=limb(1, 30),
               arml=limb(-1, 30, 18), forel=limb(-1, 30)),
    'run_up': P(_off=(0, 1.2, 0), body=qs(('x', 34)), head=qs(('x', -44)), legr=limb(1, 18), legl=limb(-1, -18), armr=limb(1, 46, 22), forer=limb(1, 40),
                arml=limb(-1, 46, 22), forel=limb(-1, 40)),
    'run_b': P(_off=(0, 0.2, 0), body=qs(('x', 34)), head=qs(('x', -44)), legr=limb(1, -40), legl=limb(-1, 52), armr=limb(1, 30, 18), forer=limb(1, 30),
               arml=limb(-1, 60, 18), forel=limb(-1, 30)),
    'jump': P(_off=(0, 1.6, 0), body=qs(('x', 16)), head=qs(('x', -30)), legr=limb(1, 50), legl=limb(-1, 30), armr=limb(1, 70, 40), forer=limb(1, 50),
              arml=limb(-1, 70, 40), forel=limb(-1, 50)),
    # the rend (its blow): a claw drawn up high behind - and raked down through
    'rend_up': P(_face='wide', body=qs(('x', 4), ('y', -18)), head=qs(('x', -20)), armr=limb(1, 160, 30), forer=limb(1, 40), arml=limb(-1, 10, 20), forel=limb(-1, 30)),
    'rend': P(_off=(0, -0.4, 0), body=qs(('x', 24), ('y', 20)), head=qs(('x', -18)), armr=limb(1, 40, -10, 20), forer=limb(1, 10), arml=limb(-1, -10, 24),
              forel=limb(-1, 30)),
    # stepping out of the dark: hunched to nothing - then unfolding mid-strike, both claws high
    'fold': P(_face='shut', _off=(0, -6.0, 0), body=qs(('x', 50)), head=qs(('x', 10)), legr=limb(1, 80), legl=limb(-1, 80), armr=limb(1, -20, 6), forer=limb(1, 90),
              arml=limb(-1, -20, 6), forel=limb(-1, 90)),
    'unfold': P(_face='wide', _off=(0, 0.6, 0), body=qs(('x', -10)), head=qs(('x', -46)), armr=limb(1, 170, 24), forer=limb(1, 20), arml=limb(-1, 170, 24),
                forel=limb(-1, 20), legr=limb(1, 10), legl=limb(-1, -10)),
    # the scream (the gaze): head thrown all the way back, maw wide, arms spread
    'scream': P(_face='wide', body=qs(('x', -6)), head=qs(('x', -60)), armr=limb(1, 30, 80), forer=limb(1, 40), arml=limb(-1, 30, 80), forel=limb(-1, 40)),
    # still, watching you, the head cocked (summoned; at rest)
    'tilt': P(_face='shut', **dict(IDLE, head=qs(('x', -12), ('z', 28)), arml=limb(-1, 4, 8), forel=limb(-1, 10))),
    'wave_a': P(**dict(IDLE, arml=limb(-1, 10, 70), forel=limb(-1, 50), head=qs(('x', -16), ('z', -14)))),
    # sitting: squatting on its heels, knees up past its shoulders, the claws draped over them
    # sitting: on the ground, its long legs straight out and splayed, hunched over them, the claws draped across its shins
    'sit_a': P(_face='shut', _off=(0, -18.6, 0), body=qs(('x', 22)), head=qs(('x', -24)), legr=limb(1, 88, 12), legl=limb(-1, 88, 12),
               armr=limb(1, 50, 10), forer=limb(1, 60), arml=limb(-1, 50, 10), forel=limb(-1, 60)),   # (2.88b: hands on his knees - they hung into the floor)
    'sit_b': P(_off=(0, -18.7, 0), body=qs(('x', 26)), head=qs(('x', -34), ('z', 16)), legr=limb(1, 88, 12), legl=limb(-1, 88, 12),
               armr=limb(1, 60, 12), forer=limb(1, 70), arml=limb(-1, 26, 10), forel=limb(-1, 100)),
    'hurt': P(_face='wide', body=qs(('x', -8)), head=qs(('x', -50)), armr=limb(1, 40, 50), forer=limb(1, 60), arml=limb(-1, 40, 50), forel=limb(-1, 60)),
    'tired': P(_face='shut', _off=(0, -1.0, 0), body=qs(('x', 30)), head=qs(('x', 20)), armr=limb(1, 6, 4), arml=limb(-1, 6, 4), forer=limb(1, 4), forel=limb(-1, 4),
               legr=limb(1, 12), legl=limb(-1, -6)),
}
CRAWL = dict(body=80, off=-4.0, arm=115, fore=50, leg=30, shin=-112, head=-64)


# (2.88) ON ALL FOURS - the Dread Night's hunter closing in (and the follower at a run): pitched flat over the ground, the
# long arms its front legs and the claws striking down like feet, the legs folded at the knee behind, the head craned up out
# of the shoulders to keep its eyes - and its maw - on you. A trot (crawl) and a flat-out lope (sprint), four frames each.
LIFT = 1.0
def _gait(k, n, body, off, arm, arm_sw, fore, leg, leg_sw, shin, head, roll):
    ph = 2 * math.pi * k / n; s, c = math.sin(ph), math.cos(ph)
    return P(_face='wide', _off=(0, off + 0.6 * abs(c), 0), body=qs(('x', body), ('z', roll * s)), head=qs(('x', head), ('z', -roll * s)),
             armr=limb(1, arm + arm_sw * s, 10), forer=limb(1, fore + LIFT * max(0.0, -s) * arm_sw), arml=limb(-1, arm - arm_sw * s, 10),
             forel=limb(-1, fore + LIFT * max(0.0, s) * arm_sw),
             legr=limb(1, leg - leg_sw * s, 6), shinr=limb(1, shin + 12 * c), legl=limb(-1, leg + leg_sw * s, 6), shinl=limb(-1, shin - 12 * c))
for _k in range(4):
    POSES[f'crawl_{_k}'] = _gait(_k, 4, CRAWL['body'], CRAWL['off'], CRAWL['arm'], 22, CRAWL['fore'], CRAWL['leg'], 20, CRAWL['shin'], CRAWL['head'], 4)
    POSES[f'sprint_{_k}'] = _gait(_k, 4, CRAWL['body'] + 6, CRAWL['off'] - 0.6, CRAWL['arm'] + 6, 40, CRAWL['fore'], CRAWL['leg'] + 8, 34, CRAWL['shin'], CRAWL['head'] - 6, 7)
# standing still: drawn up to its full, wrong height on its hind legs, arms hanging past its knees, the head cocked - eerie
POSES['stand_a'] = P(**dict(IDLE, body=qs(('x', 4)), head=qs(('x', -22), ('z', 12)), armr=limb(1, 2, 6), forer=limb(1, 6), arml=limb(-1, 2, 6), forel=limb(-1, 6),
                            legr=limb(1, 0, 3), legl=limb(-1, 0, 3)))
POSES['stand_b'] = P(**dict(POSES['stand_a'], head=qs(('x', -26), ('z', -16)), armr=limb(1, 4, 8), forer=limb(1, 14), forel=limb(-1, 10)))

SWIM_FRAMES = 8
for _i in range(SWIM_FRAMES):                                            # (it swims like something drowned: long, slow, wrong strokes)
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(_off=(0, -14.0 + 0.6 * math.sin(2 * _p), 0), body=qs(('x', 70)), head=qs(('x', -50)),
                            armr=limb(1, 140 + 40 * math.sin(_p), 20), forer=limb(1, 20 + 20 * math.cos(_p)),
                            arml=limb(-1, 140 - 40 * math.sin(_p), 20), forel=limb(-1, 20 - 20 * math.cos(_p)),
                            legr=limb(1, -6 + 24 * math.sin(2 * _p)), legl=limb(-1, -6 - 24 * math.sin(2 * _p)))
DRAFT = ['idle_a', 'idle_b', 'walk_a', 'run_a', 'rend_up', 'rend', 'fold', 'unfold', 'scream', 'tilt', 'sit_a', 'hurt', 'swim_2']

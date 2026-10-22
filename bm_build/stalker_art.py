"""The Stalker (2.87) as a follower: the Dread Night's hunter (phase181's drawing), tamed - after the owner's drawing: tall and
starved thin, sage-olive skin with a darker shadow side, ribs showing, a pinched waist, legs too long and knotted at the knee,
arms that hang past where arms should end into long hooked claws, and a bald head tipped back over a gaping maw - no brow, no
nose, no eyes: two empty hollows in a blank face, and something dark run down from each, long ago.

A rigkit rig: body, head (the jaw a model per expression: shut-ish, gaping wide), the arms bent at the elbow, the legs. Design
units: feet at y=0, facing -z, its right is +x."""
import math
import random
from PIL import Image, ImageDraw

from phase57_art import hexc
from tullius_art import _noise, _shine
from rigkit import qs, el, chain

PREFIX = 'st_'
RIG_SCALE = 0.95
PIVOT = {'body': (0, 20.0, 0), 'legr': (1.4, 20.0, 0), 'legl': (-1.4, 20.0, 0), 'head': (0, 35.6, 0.9),
         'armr': (4.3, 31.0, 0), 'forer': (4.9, 19.4, 0), 'arml': (-4.3, 31.0, 0), 'forel': (-4.9, 19.4, 0)}
PARENT = {'body': None, 'legr': None, 'legl': None, 'head': 'body', 'armr': 'body', 'forer': 'armr', 'arml': 'body', 'forel': 'arml'}
PARTS = tuple(PIVOT)
PART_K = {}
FACES = ('wide', 'shut')
SKIN, SKIN_DK, SKIN_LT, INK = '#a8ac70', '#858a54', '#c0c294', '#22241a'
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)


def HIDDEN(p, pose):
    return False


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def _skin(seed, base=SKIN, n=40):
    """mottled, sickly skin: blotches a shade darker, a few veins"""
    im = _noise(base, seed, 7); rnd = random.Random(seed)
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    for _ in range(n):
        x, y, r = rnd.randrange(64), rnd.randrange(64), rnd.randint(2, 5)
        dl.ellipse((x - r, y - r, x + r, y + r), fill=hexc(SKIN_DK if base != SKIN_DK else '#6e7244')[:3] + (90,))
    im = Image.alpha_composite(im.convert('RGBA'), lay); d = ImageDraw.Draw(im)
    for _ in range(4):
        x, y = rnd.randrange(64), rnd.randrange(64)
        d.line((x, y, x + rnd.randint(-6, 6), y + rnd.randint(6, 14), x + rnd.randint(-8, 8), y + rnd.randint(14, 22)), fill=hexc('#6a6e4a'))
    return im


def _ribs(seed):
    """the chest's front: collarbones, the breastbone, ribs down each side, the sunken belly and a navel"""
    im = _skin(seed); d = ImageDraw.Draw(im); ink, sh = hexc('#4a4e30'), hexc(SKIN_DK)
    d.line((8, 6, 28, 10), fill=ink, width=2); d.line((56, 6, 36, 10), fill=ink, width=2)          # the collarbones
    d.line((32, 10, 32, 34), fill=sh, width=2)                                                    # the breastbone
    for k, y in enumerate((14, 21, 28, 35, 42)):                                                   # ribs, curving down and out
        w = 22 - k * 2
        d.arc((32 - w - 8, y - 4, 30, y + 8), 200, 300, fill=ink, width=2)
        d.arc((34, y - 4, 32 + w + 8, y + 8), 240, 340, fill=ink, width=2)
    d.ellipse((30, 54, 34, 58), fill=hexc(INK))                                                    # the navel
    d.line((26, 46, 24, 62), fill=sh); d.line((38, 46, 40, 62), fill=sh)                           # the sunken belly
    return im


def _back(seed):
    """the back: a ridge of spine, the shoulder blades standing out"""
    im = _skin(seed, SKIN_DK); d = ImageDraw.Draw(im); ink = hexc('#4a4e30')
    for y in range(4, 64, 6):
        d.rectangle((30, y, 33, y + 3), fill=hexc(SKIN))
    d.arc((6, 6, 28, 30), 180, 330, fill=ink, width=2); d.arc((36, 6, 58, 30), 210, 360, fill=ink, width=2)
    return im


def _face(kind=None):
    """the front of the skull (24 x 28 texels at uv [0, 0, 6, 7]): smooth, no brow and no nose; sunken under the cheekbones
    and round the sockets (the hollows are their own boxes); a dark streak run down from each"""
    im = _skin(1931, SKIN_LT, 10); px = im.load()
    for y in range(28):
        for x in range(24):
            dx = abs(x - 11.5)
            k = 1.0 + 0.06 * (1 - dx / 12) - (0.12 if 15 <= y <= 22 and 3 <= dx <= 9 else 0) - (0.1 if 6 <= y <= 16 and 3 <= dx <= 9 else 0)
            px[x, y] = tuple(max(0, min(255, int(c * k))) for c in px[x, y][:3]) + (255,)
    for cx in (6, 17):
        for y in range(15, 28):
            px[cx, y] = tuple(int(c * (0.42 + 0.03 * (y - 15))) for c in px[cx, y][:3]) + (255,)
            if y % 4 == 1: px[cx + (1 if cx < 12 else -1), y] = tuple(int(c * 0.62) for c in px[cx, y][:3]) + (255,)
    return im


def _eye():
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)       # an empty hollow: a dark rim, black all the way down
    d.ellipse((0, 0, 63, 63), fill=hexc('#46442c')); d.ellipse((6, 4, 57, 63), fill=hexc('#1a180e')); d.ellipse((14, 10, 49, 63), fill=(0, 0, 0, 255))
    return im


def _teeth():
    im = Image.new('RGBA', (64, 64), hexc('#46080e')[:3] + (255,)); d = ImageDraw.Draw(im)   # jagged teeth, top and bottom, round a black-red throat
    d.ellipse((14, 14, 50, 54), fill=hexc('#240306'))
    for x in range(0, 64, 8):
        d.polygon([(x, 0), (x + 8, 0), (x + 4 + (x % 3), 22)], fill=hexc('#dcd4b0'), outline=hexc('#8a8468'))
        d.polygon([(x + 4, 63), (x + 12, 63), (x + 7, 44)], fill=hexc('#dcd4b0'), outline=hexc('#8a8468'))
    for x, y in ((18, 22), (40, 18), (30, 26)):                                  # drool
        d.line((x, y, x, y + 14), fill=hexc('#c8bcc8'), width=2)
    return im


def _maw():
    im = _noise('#60121a', 1932, 9); d = ImageDraw.Draw(im)
    d.ellipse((16, 12, 48, 52), fill=hexc('#2c0408'))
    for x in range(0, 64, 8):
        d.polygon([(x, 63), (x + 8, 63), (x + 4, 46)], fill=hexc('#dcd4b0'))
    return im


def textures():
    return {'st_skin': _skin(1933), 'st_shade': _skin(1934, SKIN_DK), 'st_ribs': _ribs(1935), 'st_back': _back(1936), 'st_face': _face(),
            'st_eye': _eye(), 'st_teeth': _teeth(), 'st_maw': _maw(), 'st_claw': _shine('#1c1e12', '#5e6044', 1937),
            'st_nail': _shine('#2a2c1e', '#7a7c5a', 1938)}


# ---------------------------------------------------------------------------------------------------- models
def models():
    M = {}
    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)

    # ---- the body: narrow hips, a starved waist, the ribcage (ribs on the front, the spine and blades behind), bony
    #      shoulders, and a long thin neck rising out of the back of them
    pv = PIVOT['body']
    body = [el((-2.4, 19.0, -1.3), (2.4, 21.6, 1.3), 'st_skin', pv, shift=(0.2, 0.4)),                 # the hips
            el((-1.3, 21.4, -0.9), (1.3, 24.2, 0.9), 'st_shade', pv),                                  # the pinched waist
            el((-3.2, 24.0, -1.6), (3.2, 31.0, 1.6), 'st_skin', pv, shift=(0.5, 0.2)),                 # the ribcage
            el((-3.2, 24.0, -1.62), (3.2, 31.0, -1.6), 'st_ribs', pv, faces=('north',), uv={'north': [0, 0, 16, 16]}),
            el((-3.2, 24.0, 1.6), (3.2, 31.0, 1.62), 'st_back', pv, faces=('south',), uv={'south': [0, 0, 16, 16]}),
            el((-4.6, 30.2, -1.2), (4.6, 31.6, 1.2), 'st_skin', pv, shift=(0.1, 0.7)),                 # bony shoulders
            el((-0.8, 31.2, 0.1), (0.8, 36.4, 1.7), 'st_skin', pv, shift=(0.8, 0.1))]                  # the long thin neck
    for sx in (-1, 1):                                                                                 # (hip bones jutting)
        body.append(el((sx * 2.4 - 0.5, 20.4, -1.5), (sx * 2.4 + 0.5, 21.4, -0.9), 'st_shade', pv))
    part('st_body', body)

    # ---- the head: a long, narrow, bald skull, tipped back; the blank face with its two long hollows; the upper jaw jutting
    #      with its teeth hanging; the maw wide open below it; the lower jaw thrust out; pointed ears swept back
    pv = PIVOT['head']
    def head(face=None):
        drop = {'wide': 1.6, 'shut': -1.0}.get(face, 0.0)                                              # (how far the jaw hangs)
        h = [el((-2.6, 37.4, -2.8), (2.6, 44.4, 2.4), 'st_skin', pv, shift=(0.3, 0.2)),               # the skull
             el((-2.2, 44.4, -2.4), (2.2, 45.2, 2.0), 'st_skin', pv, shift=(0.6, 0.6)),               # its crown, rounding off
             el((-2.6, 37.4, -2.82), (2.6, 44.4, -2.8), 'st_face', pv, faces=('north',), uv={'north': [0, 0, 6, 7]}),
             el((-1.95, 41.0, -2.86), (-0.75, 43.6, -2.82), 'st_eye', pv, faces=('north',), uv={'north': [0, 0, 16, 16]}),   # the hollows
             el((0.75, 41.0, -2.86), (1.95, 43.6, -2.82), 'st_eye', pv, faces=('north',), uv={'north': [0, 0, 16, 16]}),
             el((-2.4, 36.0, -4.0), (2.4, 37.6, 2.0), 'st_skin', pv, shift=(0.4, 0.5)),               # the upper jaw, jutting
             el((-2.4, 36.0, -4.02), (2.4, 37.6, -4.0), 'st_teeth', pv, faces=('north',), uv={'north': [0, 0, 16, 5]})]
        gap = 2.0 + drop
        if gap > 0.3:
            h += [el((-2.0, 36.0 - gap, -3.0), (2.0, 36.0, 1.4), 'st_maw', pv, faces=('north', 'east', 'west'), uv={'north': [0, 0, 16, 16]})]   # the throat
        lo = 36.0 - gap
        h += [el((-2.3, lo - 0.9, -4.4), (2.3, lo, 1.6), 'st_shade', pv, shift=(0.2, 0.7)),            # the lower jaw, thrust out
              el((-2.1, lo, -4.3), (2.1, lo + 0.02, 1.4), 'st_maw', pv, faces=('up',), uv={'up': [0, 8, 16, 16]}),
              el((-2.3, lo, -4.42), (2.3, lo + 0.9, -4.4), 'st_teeth', pv, faces=('north',), uv={'north': [0, 11, 16, 16]})]
        for sx in (-1, 1):                                                                             # the ears, pointed, swept back
            h.append(el((sx * 2.6 - (0.0 if sx > 0 else 2.6), 40.2, 0.4), (sx * 2.6 + (2.6 if sx > 0 else 0.0), 41.0, 1.6), 'st_skin', pv,
                        rot=('z', 22.5 * sx, (sx * 2.6, 40.6, 1.0))))
        return h
    part('st_head', head())
    for fc in FACES:
        part(f'st_head_x{fc}', head(fc))

    # ---- the arms: far too long - thin upper arms, a knob of an elbow, thin forearms reaching down past the knee, a bony
    #      hand, and three long hooked claws (the outer one splayed)
    def upper(sx):
        pv = PIVOT['armr' if sx > 0 else 'arml']; x0, y0, _ = pv
        tex = 'st_skin' if sx > 0 else 'st_shade'
        return [el((x0 - 0.9, y0 - 1.0, -1.0), (x0 + 0.9, y0 + 0.8, 1.0), tex, pv)] + \
            chain([(x0, y0, 0), (sx * 4.9, 19.4, 0)], [1.2], 1.2, tex, pv, FRONT, ext=0.3)
    def lower(sx):
        pv = PIVOT['forer' if sx > 0 else 'forel']; ex, ey, _ = pv
        tex = 'st_skin' if sx > 0 else 'st_shade'
        wx, wy = sx * 5.1, 7.6
        a = [el((ex - 0.8, ey - 0.8, -0.8), (ex + 0.8, ey + 0.8, 0.8), tex, pv)]                       # the elbow's knob
        a += chain([(ex, ey, 0), (wx, wy, 0)], [1.0], 1.0, tex, pv, FRONT, ext=0.2)
        a += [el((wx - 0.8, wy - 2.0, -0.7), (wx + 0.8, wy + 0.2, 0.7), tex, pv, shift=(0.3, 0.6))]     # the hand, bony
        for k, dz in enumerate((-0.45, 0.0, 0.45)):
            out = (sx * 0.9 if k == 2 else sx * 0.2 * (k - 1))
            a += chain([(wx + out * 0.3, wy - 1.8, dz), (wx + out, wy - 6.0, dz - 0.6), (wx + out * 1.2, wy - 8.6, dz - 2.6)], [0.42, 0.34], 0.42,
                       'st_claw', pv, FRONT, ext=0.05)
        return a
    part('st_armr', upper(1)); part('st_arml', upper(-1)); part('st_forer', lower(1)); part('st_forel', lower(-1))

    # ---- the legs: long and thin, knotted at the knee and the ankle; long feet with three splayed toes
    def leg(sx):
        pv = PIVOT['legr' if sx > 0 else 'legl']; cx = pv[0]
        tex = 'st_skin' if sx > 0 else 'st_shade'
        L = [el((cx - 0.8, 11.0, -0.8), (cx + 0.8, 20.4, 0.8), tex, pv, shift=(0.2, 0.3)),
             el((cx - 1.05, 10.2, -1.05), (cx + 1.05, 12.0, 1.0), tex, pv),                                # the knee, knotted
             el((cx - 0.65, 1.6, -0.65), (cx + 0.65, 10.6, 0.65), tex, pv, shift=(0.6, 0.2)),
             el((cx - 0.85, 1.2, -0.85), (cx + 0.85, 2.3, 0.85), tex, pv),                                 # the ankle
             el((cx - 0.9, 0.0, -3.4), (cx + 0.9, 1.2, 1.0), tex, pv, shift=(0.4, 0.8))]                   # the long foot
        for dx in (-0.6, 0.0, 0.6):
            L.append(el((cx + dx - 0.18, 0.0, -5.2), (cx + dx + 0.18, 0.35, -3.3), 'st_nail', pv))
        return L
    part('st_legr', leg(1)); part('st_legl', leg(-1))
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
SWIM_FRAMES = 8
for _i in range(SWIM_FRAMES):                                            # (it swims like something drowned: long, slow, wrong strokes)
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(_off=(0, -14.0 + 0.6 * math.sin(2 * _p), 0), body=qs(('x', 70)), head=qs(('x', -50)),
                            armr=limb(1, 140 + 40 * math.sin(_p), 20), forer=limb(1, 20 + 20 * math.cos(_p)),
                            arml=limb(-1, 140 - 40 * math.sin(_p), 20), forel=limb(-1, 20 - 20 * math.cos(_p)),
                            legr=limb(1, -6 + 24 * math.sin(2 * _p)), legl=limb(-1, -6 - 24 * math.sin(2 * _p)))
DRAFT = ['idle_a', 'idle_b', 'walk_a', 'run_a', 'rend_up', 'rend', 'fold', 'unfold', 'scream', 'tilt', 'sit_a', 'hurt', 'swim_2']

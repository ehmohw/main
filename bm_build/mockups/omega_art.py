"""KING OMEGA - the ghastly spirit king (a draft for approval: rig, textures, faces, poses; not in the pack).

From the owner's art: Apophiss's dead elder brother, once the benevolent ruler of the Omega Palace on Omega Island - and well
aware that "King Omega of the Omega Palace on Omega Island" is a bit much. A grey serpent spirit, see-through, built like
his brother (the same great round head, the same rearing coils - they are brothers) but nothing like him in manner:
  - grey scales with a dark stripe down his front (his brother's light belly, dark on him), light grey fins and spines
    swept back from his head and down his back;
  - yellow eyes with black slit pupils under heavy black brows, a gold MONOCLE on his left eye on a little chain;
  - stitch scars on his brow and cheek, the freckles and honeycomb marks the brothers share, and a red GASH down his chest
    (the wound from the war with Apophiss);
  - a gold crown with a purple orb and red gems; a purple maw and long purple tongue (his warmest grin and his war cry both
    show it); clawed arms, the claws faintly blue;
  - no mace: his tail ends in a BLUE SOUL FLAME (his light to lead his soldiers - and to throw).
He is translucent (his hide's texture is see-through, as Pistachio's body); his crown, monocle, eyes, claws and flame are
solid, and his eyes and flame glow.

The rig is Apophiss's (apophiss_art: coil - body - chest - head - jaw, arms off the chest, tail1-4), his geometry re-skinned
and the parts his brother lacks added: the monocle and its chain, the stitches, the gash; the tail's end carries the flame
instead of the mace. Design units as there: the coil on y=0, facing -z, his right +x."""
import math
import os
import random
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import apophiss_art as A
from phase57_art import hexc
from rigkit import qs, el, seg, chain, I, mid

PREFIX = 'om_'
BOSS_SCALE = PET_SCALE = A.BOSS_SCALE
PIVOT = {('flame' if k == 'mace' else k): v for k, v in A.PIVOT.items() if k not in ('wingr', 'wingl')}
PARENT = {('flame' if k == 'mace' else k): ('flame' if v == 'mace' else v) for k, v in A.PARENT.items() if k not in ('wingr', 'wingl')}
PARTS = tuple(PIVOT)
PART_K = {}
FACES = ('warm', 'shock', 'tired', 'blink', 'roar')
_AFACE = {'warm': 'smug', 'shock': 'shock', 'tired': 'tired', 'blink': 'blink', 'roar': 'hurt'}     # (the brother's lids/brows each borrows)
GHOST_A = 142                              # (his hide: see-through, as Pistachio's)


def HIDDEN(p, pose):
    return False


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def _ghost(im, a=GHOST_A):
    px = im.load()
    for x in range(im.width):
        for y in range(im.height):
            r, g, b, al = px[x, y]
            px[x, y] = (r, g, b, min(al, a))
    return im


def _stitch(seed):
    """a scar sewn shut: a dark seam across, stitches crossing it"""
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.line((1, 8, 14, 7), fill=hexc('#3a3a3c'), width=1)
    for x in (3, 6, 9, 12):
        d.line((x - 1, 5, x + 1, 10), fill=hexc('#2a2a2c'), width=1)
    return im


def _gash(seed):
    """the wound from the war: a long ragged red cut, darker at its heart"""
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    pts = [(8 + rnd.randint(-1, 1), y) for y in range(0, 16, 2)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d.line((x0, y0, x1, y1), fill=hexc('#7a1214'), width=4)
        d.line((x0, y0, x1, y1), fill=hexc('#3e0608'), width=1)
    return im


def _flame(seed, a=215):
    """soul fire: white-blue at the heart, out to sky blue, flickering streaks"""
    im = Image.new('RGBA', (64, 64)); rnd = random.Random(seed)
    for y in range(64):
        for x in range(64):
            t = abs(x - 32) / 32
            c = tuple(int(u * (1 - t) + v * t) for u, v in zip((226, 246, 255), (72, 162, 246)))
            j = rnd.randint(-12, 12)
            im.putpixel((x, y), tuple(max(0, min(255, v + j)) for v in c) + (a,))
    d = ImageDraw.Draw(im)
    for _ in range(9):
        x = rnd.randrange(64); d.line((x, 63, x + rnd.randint(-6, 6), rnd.randrange(30)), fill=(240, 252, 255, a))
    return im


def _grey_hex(seed):
    """the honeycomb marks the brothers share - dark grey on him"""
    im = A._hex(seed); px = im.load()
    for x in range(im.width):
        for y in range(im.height):
            if px[x, y][3]: px[x, y] = (58, 58, 60, px[x, y][3])
    return im


def textures():
    T = {'om_body': _ghost(A._scales('#9c9c9e', '#7a7a7c', '#c4c4c6', 801)), 'om_body_dk': _ghost(A._scales('#727274', '#58585a', '#8e8e90', 802)),
         'om_stripe': _ghost(A._bands('#3a3a3c', '#262628', 803)), 'om_fin': _ghost(A._fin('#c6c6ca', '#ececf0', '#9a9aa0', 804), 118),
         'om_claw': A._noise('#4a4e5a', 805, 6), 'om_mouth': A._noise('#3a1446', 806, 8), 'om_tongue': A._noise('#9a3ac8', 807, 8),
         'om_fang': A._noise('#f0eee6', 808, 5), 'om_eye': A._eye('#e8d42e', '#fffbe0', 809), 'om_pupil': A._noise('#0c0c0e', 810, 2),
         'om_lid': A._scales('#8e8e90', '#727274', '#b0b0b2', 811), 'om_brow': A._brush('#121214', '#26262a', 812), 'om_lash': A._noise('#08080a', 813, 2),
         'om_dot': A._noise('#3e3e40', 814, 3), 'om_hex': _grey_hex(815),
         'om_gold': A._noise('#d8a838', 816, 14), 'om_gold_dk': A._noise('#9a7420', 817, 10), 'om_orb': A._noise('#5a2a78', 818, 10),
         'om_orb_lt': A._noise('#9a62c8', 819, 10), 'om_ruby': A._noise('#a8202a', 820, 10), 'om_ruby_lt': A._noise('#e85660', 821, 10),
         'om_lens': _ghost(A._noise('#f2f0d8', 822, 4), 90), 'om_stitch': _stitch(823), 'om_gash': _gash(824),
         'om_flame': _flame(825), 'om_flame_core': Image.new('RGBA', (64, 64), (236, 250, 255, 240))}
    return T


# apophiss's textures -> his (the crown's black and emerald become gold and the purple orb; the brother's purple bags under
# his eyes are only shading on Omega)
TEXMAP = {'apo_scale': 'om_body', 'apo_scale_dk': 'om_body_dk', 'apo_belly': 'om_stripe', 'apo_fin': 'om_fin', 'apo_claw': 'om_claw',
          'apo_mouth': 'om_mouth', 'apo_tongue': 'om_tongue', 'apo_fang': 'om_fang', 'apo_eye': 'om_eye', 'apo_pupil': 'om_pupil',
          'apo_bag': 'om_body_dk', 'apo_lash': 'om_lash', 'apo_lid': 'om_lid', 'apo_brow': 'om_brow', 'apo_dot': 'om_dot', 'apo_hex': 'om_hex',
          'ap_black': 'om_gold', 'ap_emerald': 'om_orb', 'ap_emerald_lt': 'om_orb_lt', 'ap_ruby': 'om_ruby', 'ap_ruby_lt': 'om_ruby_lt',
          'ap_gold': 'om_gold_dk', 'ap_fur': 'om_gold_dk'}
GLOW = {'om_eye': 12, 'om_pupil': 12, 'om_flame': 15, 'om_flame_core': 15, 'om_lens': 6}


# ---------------------------------------------------------------------------------------------------- models
def _retex(els):
    out = []
    for e in els:
        if any(v['texture'] == '#apo_dot' for v in e['faces'].values()) and e['from'][2] > 8 - 9.6 + A.PIVOT['head'][2] and e['from'][0] > 8 + 5:
            e = dict(e, **{'from': [16 - e['to'][0], e['from'][1], e['from'][2]], 'to': [16 - e['from'][0], e['to'][1], e['to'][2]]})
        faces = {f: dict(v, texture='#' + TEXMAP.get(v['texture'][1:], v['texture'][1:])) for f, v in e['faces'].items()}
        e2 = dict(e, faces=faces)
        g = max([GLOW.get(v['texture'][1:], 0) for v in faces.values()] + [e.get('light_emission', 0)])
        if g: e2['light_emission'] = g
        out.append(e2)
    return out


def _monocle(pv):
    """the gold monocle over his left eye (-x), its lens faintly glassy, and the little chain looping down off it to his cheek"""
    cx, cy, cz, r = -4.1, 39.05, -9.92, 2.35
    els = []
    for i in range(12):
        a0, a1 = math.radians(30 * i), math.radians(30 * (i + 1))
        A0, A1 = (cx + r * math.cos(a0), cy + r * math.sin(a0), cz), (cx + r * math.cos(a1), cy + r * math.sin(a1), cz)
        els.append(seg(A0, A1, 0.42, 0.42, 'om_gold', pv, (0.0, 0.0, -1.0), 0.12))
    els.append(el((cx - r + 0.3, cy - r + 0.3, cz + 0.02), (cx + r - 0.3, cy + r - 0.3, cz + 0.08), 'om_lens', pv, faces=('north',)))
    els += chain([(cx + 0.3, cy - r, cz), (cx + 0.9, cy - r - 1.6, cz + 0.05), (cx + 0.5, cy - r - 3.0, cz + 0.15), (cx - 0.5, cy - r - 3.8, cz + 0.6),
                  (cx - 1.8, cy - r - 4.0, cz + 1.4)], [0.2, 0.2, 0.2, 0.2], 0.2, 'om_gold', pv, (0.0, 0.0, -1.0), ext=0.05)
    els.append(el((cx - 2.2, cy - r - 4.4, cz + 1.2), (cx - 1.5, cy - r - 3.6, cz + 1.9), 'om_gold', pv))          # (its clip)
    return els


def _scars(pv):
    """stitch scars, as the art: one slanting over his right brow toward the crown, one across his right cheek"""
    st = lambda fr, to, ang, c: el(fr, to, 'om_stitch', pv, ('z', ang, c), faces=('north',), uv={'north': [0, 0, 16, 16]})
    return [st((3.4, 42.2, -9.36), (8.0, 43.2, -9.3), -16, (5.7, 42.7, -9.33)),
            st((5.2, 35.3, -9.36), (8.6, 36.3, -9.3), 12, (6.9, 35.8, -9.33))]


def models():
    src = A.models()
    M = {}
    def part(name, els):
        els = _retex(els)
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)
    for p in ('coil', 'body', 'jaw', 'armr', 'arml', 'tail1', 'tail2', 'tail3', 'tail4'):
        part(f'om_{p}', src[f'apo_{p}'][1])
    # the chest: his brother's, the gash down the dark stripe
    pv = PIVOT['chest']
    gash = [el((-2.2, 19.6, -7.84), (2.2, 26.0, -7.78), 'om_gash', pv, ('z', 18, (0.0, 22.8, -7.8)), faces=('north',), uv={'north': [0, 0, 16, 16]}),
            el((-0.9, 22.6, -7.86), (1.6, 24.6, -7.8), 'om_gash', pv, ('z', 32, (0.3, 23.6, -7.83)), faces=('north',), uv={'north': [0, 16, 16, 0]})]
    part('om_chest', src['apo_chest'][1] + gash)
    # the head (and its faces): his brother's dome, re-skinned, the monocle and the scars on it
    pv = PIVOT['head']
    extra = _monocle(pv) + _scars(pv)
    part('om_head', src['apo_head'][1] + extra)
    for f in FACES:
        part(f'om_head_x{f}', src[f'apo_head_x{_AFACE[f]}'][1] + extra)
    # the flame: where his brother's mace is, the soul fire burning up off the tail's tip - a white heart, blue tongues out
    # and up round it, wisps above
    pv = PIVOT['flame']; c = (2.75, 2.0, 56.6)
    fl = [seg((2.75, 3.0, 53.6), (2.75, 3.0, 55.0), 2.4, 2.4, 'om_body_dk', pv, (0.0, 1.0, 0.0))]
    fl += chain([(c[0], c[1], c[2]), (c[0], c[1] + 4.0, c[2]), (c[0] + 0.4, c[1] + 8.0, c[2] - 0.3), (c[0] + 0.2, c[1] + 10.5, c[2])], [2.6, 1.8, 0.8],
                2.6, 'om_flame_core', pv, (0.0, 0.0, -1.0), hs=[2.6, 1.8, 0.8])                        # (the white heart)
    rnd = random.Random(860)
    for ring, (r, h, w, n) in enumerate(((3.6, 9.0, 2.4, 8), (2.4, 13.0, 1.9, 6), (1.2, 16.0, 1.3, 3))):   # tongues licking up round it
        for i in range(n):
            a = math.radians(360 * i / n + 23 * ring); ca, sa = math.cos(a), math.sin(a)
            hh = h * (0.8 + 0.4 * rnd.random())
            pts = [(c[0] + r * ca, c[1] - 0.6, c[2] + r * sa), (c[0] + 1.05 * r * ca, c[1] + 0.35 * hh, c[2] + 1.05 * r * sa),
                   (c[0] + 0.6 * r * ca + rnd.uniform(-0.6, 0.6), c[1] + 0.7 * hh, c[2] + 0.6 * r * sa), (c[0] + 0.2 * r * ca + rnd.uniform(-1, 1), c[1] + hh, c[2] + 0.2 * r * sa)]
            fl += chain(pts, [w, 0.75 * w, 0.4 * w], w * 0.8, 'om_flame', pv, (ca, 0.0, sa), ext=0.3, hs=[w * 0.8, w * 0.6, w * 0.3])
    for k in range(5):                                                                  # wisps breaking off the top
        x, z = c[0] + rnd.uniform(-2.0, 2.0), c[2] + rnd.uniform(-2.0, 2.0); y = c[1] + 14.0 + 1.6 * k
        fl.append(el((x - 0.4, y, z - 0.4), (x + 0.4, y + 0.9, z + 0.4), 'om_flame', pv, ('y', 45, (x, y, z))))
    part('om_flame', fl)
    return M


# ---------------------------------------------------------------------------------------------------- poses
# Display-frame rotations, as Apophiss's: body/chest/head +x leans forward (head nods down), +y turns to his left; jaw +x
# opens; arms -x forward/up, -z (right) / +z (left) out to the side; the tail +x lifts it, +y swings it to his right.
def P(**kw):
    return kw


def _ren(p):
    return {('flame' if k == 'mace' else k): v for k, v in p.items()}


FLAME_UP = dict(tail1=qs(('x', 28), ('y', -22)), tail2=qs(('x', 38), ('y', -10)), tail3=qs(('x', 40)), tail4=qs(('x', 30)), flame=qs(('x', -60)))   # (the art: the flame held up beside him)
HOVER = 8.0                                 # (a spirit: he never quite touches the ground)
POSES = {
    # idle: reared up, regal and kindly - a slight smile, one claw raised, the flame held high beside him like a lamp (a/b: a
    # slow drift up and down)
    'idle_a': P(_face='warm', _off=(0, HOVER, 0), body=qs(('x', -3)), chest=qs(('x', 5)), head=qs(('x', 4), ('z', -4)), jaw=qs(('x', 4)),
                armr=qs(('x', -30), ('z', -18)), arml=qs(('x', -50), ('z', 20)), **FLAME_UP),
    'idle_b': P(_face='warm', _off=(0, HOVER + 1.2, 0), body=qs(('x', -1)), chest=qs(('x', 7)), head=qs(('x', 6), ('y', 6), ('z', -2)), jaw=qs(('x', 6)),
                armr=qs(('x', -26), ('z', -16)), arml=qs(('x', -46), ('z', 18)),
                tail1=qs(('x', 26), ('y', -16)), tail2=qs(('x', 36), ('y', -4)), tail3=qs(('x', 40)), tail4=qs(('x', 32)), flame=qs(('x', -64))),
    # glide (on the move): drifting low and forward, the tail streaming out behind, the flame trailing
    'glide_a': P(_off=(0, HOVER + 0.6, 0), coil=qs(('y', 6)), body=qs(('x', 24), ('y', -6)), chest=qs(('x', 10)), head=qs(('x', -26), ('y', -4)), jaw=qs(('x', 6)),
                 armr=qs(('x', -40), ('z', -14)), arml=qs(('x', -30), ('z', 14)), tail1=qs(('x', -6), ('y', -20)), tail2=qs(('y', 24)), tail3=qs(('y', 22)), tail4=qs(('y', 10)), flame=qs(('x', 20))),
    'glide_b': P(_off=(0, HOVER + 1.4, 0), coil=qs(('y', -6)), body=qs(('x', 24), ('y', 6)), chest=qs(('x', 10)), head=qs(('x', -26), ('y', 4)), jaw=qs(('x', 6)),
                 armr=qs(('x', -30), ('z', -14)), arml=qs(('x', -40), ('z', 14)), tail1=qs(('x', -6), ('y', 20)), tail2=qs(('y', -24)), tail3=qs(('y', -22)), tail4=qs(('y', -10)), flame=qs(('x', 20))),
    # the monocle: his left claw up to it, head tilted - inspecting you (or adjusting it, a little self-conscious)
    'monocle': P(_face='warm', _off=(0, HOVER, 0), body=qs(('x', -2)), chest=qs(('x', 6), ('y', 8)), head=qs(('x', 10), ('z', 10), ('y', -6)), jaw=qs(('x', 2)),
                 armr=qs(('x', -20), ('z', -14)), arml=qs(('x', -150), ('z', 52)), **FLAME_UP),
    # the bow: a king's gracious nod - head and chest bowed, a claw to his chest, the flame lowered politely behind him
    'bow': P(_face='blink', _off=(0, HOVER - 0.6, 0), body=qs(('x', 14)), chest=qs(('x', 18)), head=qs(('x', 20)), jaw=qs(('x', 2)),
             armr=qs(('x', -70), ('z', 30)), arml=qs(('x', -10), ('z', 10)), tail1=qs(('x', 6)), tail2=qs(('x', 10)), tail3=qs(('x', 10)), tail4=qs(('x', 10)), flame=qs(('x', -10))),
    # the welcome: both arms open wide, head up, a broad grin (the purple maw showing)
    'welcome': P(_face='warm', _off=(0, HOVER + 0.6, 0), body=qs(('x', -6)), chest=qs(('x', -4)), head=qs(('x', -8)), jaw=qs(('x', 22)),
                 armr=qs(('x', -70), ('z', -70)), arml=qs(('x', -70), ('z', 70)), **FLAME_UP),
    # battle: risen tall, claws spread, maw open, the flame swung up over his head ready to throw
    'battle': P(_off=(0, HOVER + 0.4, 0), body=qs(('x', 10)), chest=qs(('x', 10)), head=qs(('x', -10)), jaw=qs(('x', 26)), armr=qs(('x', -50), ('z', -40)), arml=qs(('x', -50), ('z', 40)),
                tail1=qs(('x', 80)), tail2=qs(('x', 30)), tail3=I, tail4=I, flame=qs(('x', -20))),
    # the soul flame thrown: wound back over his head, then lashed forward (the game launches the fireball from the tip)
    'flame_up': P(_off=(0, HOVER, 0), body=qs(('x', -12)), chest=qs(('x', -4)), head=qs(('x', -6)), jaw=qs(('x', 20)), armr=qs(('x', -40), ('z', -30)), arml=qs(('x', -40), ('z', 30)),
                  tail1=qs(('x', 56), ('y', 20)), tail2=qs(('x', 44)), tail3=qs(('x', 20)), tail4=qs(('x', 10)), flame=qs(('x', -30))),
    'flame_throw': P(_off=(0, HOVER - 0.4, 0), body=qs(('x', 18), ('y', -8)), chest=qs(('x', 14), ('y', -6)), head=qs(('x', -14), ('y', 6)), jaw=qs(('x', 30)),
                     armr=qs(('x', -60), ('z', -40)), arml=qs(('x', -60), ('z', 40)), tail1=qs(('x', 70), ('y', 30)), tail2=qs(('x', 50), ('y', 20)), tail3=qs(('x', 50)),
                     tail4=qs(('x', 40)), flame=qs(('x', 20))),
    # the claw rake (as his brother's), and the war cry - the old soldiers' rally (head back, maw wide, tongue out)
    'claw_up': P(_off=(0, HOVER, 0), body=qs(('x', 6), ('y', -14)), chest=qs(('y', -16), ('x', 4)), head=qs(('y', 8)), jaw=qs(('x', 16)), armr=qs(('x', -120), ('z', -50)),
                 arml=qs(('x', -30), ('z', 40)), **FLAME_UP),
    'claw': P(_off=(0, HOVER, 0), body=qs(('x', 16), ('y', 18)), chest=qs(('y', 20), ('x', 8)), head=qs(('y', -14), ('x', -20)), jaw=qs(('x', 14)), armr=qs(('x', -80), ('z', 14)),
              arml=qs(('x', -40), ('z', 40)), tail1=qs(('x', 20), ('y', -20)), tail2=qs(('x', 26), ('y', -10)), tail3=qs(('x', 30)), tail4=qs(('x', 30)), flame=qs(('x', -30))),
    'rally': P(_face='roar', _off=(0, HOVER + 1.0, 0), body=qs(('x', -10)), chest=qs(('x', -12)), head=qs(('x', -30)), jaw=qs(('x', 50)), armr=qs(('x', -150), ('z', -40)),
               arml=qs(('x', -70), ('z', 70)), tail1=qs(('x', 30), ('y', 24)), tail2=qs(('x', 40), ('y', 10)), tail3=qs(('x', 40)), tail4=qs(('x', 30)), flame=qs(('x', -50))),
    # summoning his soul serpents: claws low and spread, palms up, the flame flaring overhead
    'summon': P(_face='shock', _off=(0, HOVER + 0.8, 0), body=qs(('x', -6)), chest=qs(('x', -4)), head=qs(('x', -14)), jaw=qs(('x', 34)),
                armr=qs(('x', -30), ('z', -60)), arml=qs(('x', -30), ('z', 60)), tail1=qs(('x', 70)), tail2=qs(('x', 50)), tail3=qs(('x', 10)), tail4=I, flame=qs(('x', -40))),
    # tired: sinking low over his coils, the flame guttering at the ground, monocle askew (the head rolled)
    'tired': P(_face='tired', _off=(0, 0.6, 0), body=qs(('x', 16)), chest=qs(('x', 14), ('z', 4)), head=qs(('x', -10), ('z', 12)), jaw=qs(('x', 16)),
               armr=qs(('x', 4), ('z', -2)), arml=qs(('x', 8), ('z', 4)), tail1=qs(('y', 16)), tail2=qs(('y', 20)), tail3=qs(('y', 24)), tail4=qs(('y', 24)), flame=qs(('y', 10))),
    # sit (a follower at rest): coiled on the air, arms folded, the flame curled round in front like a lantern on the ground
    'sit': P(_face='warm', _off=(0, 0.4, 0), body=qs(('x', -4)), chest=qs(('x', 4)), head=qs(('x', 6), ('y', 14)), jaw=qs(('x', 2)),
             armr=qs(('x', -56), ('z', 14)), arml=qs(('x', -50), ('z', -14)), tail1=qs(('x', 2), ('y', 54)), tail2=qs(('y', 56)), tail3=qs(('y', 50)), tail4=qs(('y', 50)), flame=qs(('y', 30))),
    # fading (beaten, or dismissed): slumped, head down - the game fades him out in soul-fire wisps
    'fade': P(_face='blink', _off=(0, -0.8, 0), body=qs(('x', 26), ('z', 6)), chest=qs(('x', 18), ('z', 6)), head=qs(('x', 4), ('z', 12)), jaw=qs(('x', 6)),
              armr=qs(('x', 20), ('z', -8)), arml=qs(('x', 28), ('z', 10)), tail1=qs(('y', -20)), tail2=qs(('y', -24)), tail3=qs(('y', -18)), tail4=qs(('y', -18)), flame=qs(('y', -10))),
}
for _p in POSES.values():
    if 'tail4' not in _p and 'tail3' in _p: _p['tail4'] = _p['tail3']


def _upright(pose, tilt=8.0):
    """fire rises: the flame's own turn undoes everything the coil and tail have done to it (leaning back a little)"""
    from rigkit import solve
    q = solve(PIVOT, PARENT, dict(pose, flame=I))['tail4'][0]
    inv = (-q[0], -q[1], -q[2], q[3])
    from rigkit import qmul
    return qmul(inv, qs(('x', tilt)))


for _n, _p in POSES.items():
    _p['flame'] = _upright(_p)
POSES['glide_m'] = mid(POSES['glide_a'], POSES['glide_b'])
POSES['flame_swing'] = mid(POSES['flame_up'], POSES['flame_throw'])
POSES['shock'] = dict(POSES['idle_a'], _face='shock', head=qs(('x', -10)), jaw=qs(('x', 30)), arml=qs(('x', -90), ('z', 40)))
DRAFT = ['idle_a', 'glide_a', 'monocle', 'bow', 'welcome', 'battle', 'flame_up', 'flame_throw', 'claw', 'rally', 'summon', 'tired', 'sit', 'fade', 'shock']
ANIMS = {'idle': [('idle_a', 30), ('idle_b', 30), ('idle_a', 30)],
         'glide': [('glide_a', 6), ('glide_m', 6), ('glide_b', 6), ('glide_m', 6), ('glide_a', 6)],
         'monocle': [('idle_a', 10), ('monocle', 10), ('monocle', 16), ('idle_a', 10)],
         'greet': [('idle_a', 10), ('bow', 12), ('bow', 10), ('welcome', 10), ('welcome', 12), ('idle_a', 10)],
         'flame': [('battle', 6), ('flame_up', 10), ('flame_swing', 2), ('flame_throw', 3), ('flame_throw', 6), ('battle', 8)],
         'claw': [('battle', 6), ('claw_up', 7), ('claw', 3), ('battle', 6)],
         'rally': [('idle_a', 8), ('rally', 8), ('rally', 16), ('idle_a', 10)],
         'summon': [('battle', 6), ('summon', 12), ('summon', 14), ('battle', 8)],
         'tired': [('idle_a', 20), ('tired', 20), ('tired', 30)], 'fade': [('tired', 16), ('fade', 18), ('fade', 10)],
         'rest': [('idle_a', 20), ('sit', 20), ('sit', 20)]}

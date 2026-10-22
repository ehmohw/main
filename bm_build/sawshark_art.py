"""The Chomping Sawshark (2.88), a Dread boss - after the owner's drawing: a vile shark woken in the great war, that has kept the
Underwater Kingdom from surfacing ever since (they say it swallowed Democratus whole). Slate-blue grey, pale underneath; a huge
blocky, skull-like head - heavy brow ridges, small glowing yellow eyes sunk under them - and an enormous gaping maw ringed with
long jagged teeth; long pectoral fins sweeping out to the sides like horns; a tall, curved dorsal fin; and every fin torn and
notched into saw-teeth. A great crescent tail.

A rigkit rig: body (the torn dorsal and the saw-notched back), head (the eyes per expression), jaw, the pectoral fins, the tail
in two pieces. Design units: belly at y~2, facing -z, its right is +x."""
import math
import random
from PIL import Image, ImageDraw

from phase57_art import hexc
from tullius_art import _noise, _shine
from rigkit import qs, el, chain

PREFIX = 'ss_'
RIG_SCALE = 2.4
CY = 10.0
PIVOT = {'body': (0, CY, 0), 'head': (0, CY, -9.0), 'jaw': (0, CY - 3.6, -10.0),
         'finr': (6.6, CY - 2.4, -5.0), 'finl': (-6.6, CY - 2.4, -5.0), 'tail': (0, CY + 0.5, 12.0), 'tail2': (0, CY + 1.0, 21.0)}
PARENT = {'body': None, 'head': 'body', 'jaw': 'head', 'finr': 'body', 'finl': 'body', 'tail': 'body', 'tail2': 'tail'}
PARTS = tuple(PIVOT)
PART_K = {}
FACES = ('rage', 'shut')
GREY, GREY_DK, GREY_LT, BELLY = '#8e9ea6', '#52626a', '#b0bcc2', '#e2e6e6'
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)


def HIDDEN(p, pose):
    return False


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def _skin(seed, base=GREY, scars=2):
    """smooth slate hide, a lighter sheen along the top, a few old scars"""
    im = _noise(base, seed, 4); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for y in range(0, 14):
        for x in range(64):
            if rnd.random() < 0.5: d.point((x, y), fill=hexc(GREY_LT))
    for _ in range(scars):
        x, y = rnd.randrange(10, 50), rnd.randrange(16, 44)
        d.line((x, y, x + 12, y + rnd.randint(-3, 3)), fill=hexc(GREY_DK), width=1)
    return im


def _side(seed):
    im = _skin(seed); d = ImageDraw.Draw(im)
    d.rectangle((0, 46, 63, 63), fill=hexc(BELLY))
    for x in range(0, 64, 4):
        d.line((x, 46 - (x % 8) // 4 * 2, x + 4, 46), fill=hexc(BELLY))
    for k in range(4):                                                                                 # gill slits, dark
        d.line((8 + k * 5, 18, 5 + k * 5, 38), fill=hexc('#2a343a'), width=2)
    return im


def _brow(kind=None):
    """the brow ridge's front: the two small glowing yellow eyes under it (uv [0, 0, 16, 16])"""
    im = _noise(GREY_DK, 2951, 4); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 63, 8), fill=hexc(GREY))
    for cx in (12, 52):
        if kind == 'shut':
            d.line((cx - 7, 20, cx + 7, 22), fill=hexc('#1a2024'), width=3)
            continue
        d.polygon([(cx - 8, 16), (cx + 8, 14), (cx + 6, 26), (cx - 6, 26)], fill=hexc('#3a2a06'))
        d.polygon([(cx - 6, 17), (cx + 6, 16), (cx + 4, 24), (cx - 4, 24)], fill=hexc('#ffd21a' if kind != 'rage' else '#fff06a'))
        d.rectangle((cx - 1, 17, cx + 1, 24), fill=hexc('#a87a08'))
        d.line((cx - 9, 12 - (4 if kind == 'rage' else 0), cx + 9, 10), fill=hexc('#2a343a'), width=3)       # (the brow's hard edge)
    return im


def _teeth():
    """the maw: long jagged teeth over a dark gullet and a red tongue"""
    im = Image.new('RGBA', (64, 64), hexc('#1a0a0c')[:3] + (255,)); d = ImageDraw.Draw(im); rnd = random.Random(2952)
    for x in range(-2, 64, 7):
        d.polygon([(x, 0), (x + 7, 0), (x + 3 + rnd.randint(-1, 1), 22 + rnd.randint(-5, 5))], fill=hexc(rnd.choice(['#eef0ec', '#dfe4e2'])), outline=hexc('#8a9496'))
    d.ellipse((10, 36, 54, 70), fill=hexc('#7a2a2e')); d.ellipse((18, 42, 46, 66), fill=hexc('#9a3a3e'))   # (the tongue)
    return im


def textures():
    return {'ss_skin': _skin(2954), 'ss_skin_dk': _skin(2955, GREY_DK, 1), 'ss_belly': _noise(BELLY, 2956, 3), 'ss_side': _side(2957),
            'ss_teeth': _teeth(), 'ss_brow': _brow(), 'ss_tooth': _shine('#c8ccc8', '#ffffff', 2958), 'ss_gum': _noise('#5a1a1e', 2959, 3),
            **{f'ss_brow_{k}': _brow(k) for k in FACES}}


# ---------------------------------------------------------------------------------------------------- models
def models():
    M = {}
    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)
    y0 = CY
    # ---- the body: heavy at the shoulders, tapering; the tall curved dorsal fin, torn; saw-notches down the back and belly
    pv = PIVOT['body']
    body = [el((-7.0, y0 - 6.4, -9.0), (7.0, y0 + 6.4, 4.0), 'ss_skin', pv, shift=(0.3, 0.1)),
            el((-5.4, y0 - 5.0, 3.8), (5.4, y0 + 5.0, 12.4), 'ss_skin', pv, shift=(0.6, 0.4)),
            el((-7.02, y0 - 6.4, -9.0), (-7.0, y0 + 6.4, 4.0), 'ss_side', pv, faces=('west',), uv={'west': [0, 0, 16, 16]}),
            el((7.0, y0 - 6.4, -9.0), (7.02, y0 + 6.4, 4.0), 'ss_side', pv, faces=('east',), uv={'east': [16, 0, 0, 16]}),
            el((-6.6, y0 - 6.9, -8.6), (6.6, y0 - 6.3, 3.6), 'ss_belly', pv),
            el((-5.0, y0 - 5.6, 3.6), (5.0, y0 - 4.9, 12.0), 'ss_belly', pv)]
    body += chain([(0, y0 + 6.0, -4.0), (0, y0 + 13.0, 0.0), (0, y0 + 19.0, 5.6), (0, y0 + 21.0, 9.6)], [9.0, 5.0, 2.0], 1.6, 'ss_skin_dk', pv, (1.0, 0.0, 0.0), ext=0.2)
    for k, (z, h) in enumerate(((5.6, 4.0), (8.4, 3.0), (11.0, 2.4))):                                # the saw-notched back: torn spikes
        body += chain([(0, y0 + 4.6 - k * 0.4, z), (0, y0 + 4.6 + h, z + 1.8)], [2.2], 0.8, 'ss_skin_dk', pv, (1.0, 0.0, 0.0), ext=0.1)
    for k, (z, h) in enumerate(((2.0, 3.0), (6.0, 3.6), (9.6, 2.6))):                                  # ...and the belly's
        body += chain([(0, y0 - 5.6, z), (0, y0 - 5.6 - h, z + 2.2)], [2.0], 0.8, 'ss_skin_dk', pv, (1.0, 0.0, 0.0), ext=0.1)
    part('ss_body', body)
    # ---- the head: huge and blocky like a skull - the brow ridges jutting over the eyes, the blunt snout, the upper teeth
    pv = PIVOT['head']
    def head(face=None):
        ft = 'ss_brow' if face is None else f'ss_brow_{face}'
        h = [el((-7.6, y0 - 3.4, -21.0), (7.6, y0 + 6.6, -8.8), 'ss_skin', pv, shift=(0.1, 0.3)),               # the skull
             el((-6.2, y0 - 2.6, -24.6), (6.2, y0 + 2.0, -20.8), 'ss_skin', pv, shift=(0.5, 0.5)),              # the blunt snout
             el((-7.6, y0 + 2.6, -21.6), (7.6, y0 + 6.8, -18.0), 'ss_skin_dk', pv, shift=(0.3, 0.6)),            # the brow ridges, jutting
             el((-7.62, y0 - 1.0, -21.62), (7.62, y0 + 6.8, -21.6), ft, pv, faces=('north',), uv={'north': [0, 0, 16, 16]}),
             el((-6.0, y0 + 6.6, -20.0), (-2.4, y0 + 8.0, -14.0), 'ss_skin_dk', pv), el((2.4, y0 + 6.6, -20.0), (6.0, y0 + 8.0, -14.0), 'ss_skin_dk', pv),   # (the ridges' crests)
             el((-6.0, y0 - 4.2, -24.4), (6.0, y0 - 2.6, -20.6), 'ss_teeth', pv, faces=('north', 'east', 'west', 'down'), uv={'north': [0, 0, 16, 6]}),
             el((-7.4, y0 - 4.0, -21.0), (7.4, y0 - 3.4, -9.4), 'ss_gum', pv)]
        for k in range(6):                                                                                  # long fangs hanging from the upper jaw
            x = -5.4 + k * 2.16
            h += chain([(x, y0 - 3.6, -23.8 + abs(k - 2.5) * 0.4), (x + 0.2, y0 - 7.2 + abs(k - 2.5) * 0.5, -24.0 + abs(k - 2.5) * 0.4)], [0.5], 0.8, 'ss_tooth', pv, FRONT, ext=0.0)
        for sx in (-1, 1):
            for k in range(3):
                z = -20.0 + k * 3.4
                h += chain([(sx * 7.0, y0 - 3.6, z), (sx * 7.2, y0 - 6.6, z - 0.2)], [0.5], 0.7, 'ss_tooth', pv, FRONT, ext=0.0)
        return h
    part('ss_head', head())
    for fc in FACES:
        part(f'ss_head_x{fc}', head(fc))
    # ---- the jaw: huge, wide, teeth standing all round its rim
    pv = PIVOT['jaw']
    jaw = [el((-7.2, y0 - 7.6, -23.6), (7.2, y0 - 4.2, -9.6), 'ss_belly', pv),
           el((-6.8, y0 - 4.22, -23.2), (6.8, y0 - 4.2, -10.0), 'ss_teeth', pv, faces=('up',), uv={'up': [0, 6, 16, 16]})]
    for k in range(6):
        x = -5.4 + k * 2.16
        jaw += chain([(x, y0 - 4.2, -22.8), (x - 0.1, y0 - 0.8, -22.6)], [0.5], 0.8, 'ss_tooth', pv, FRONT, ext=0.0)
    for sx in (-1, 1):
        for k in range(3):
            z = -19.0 + k * 3.4
            jaw += chain([(sx * 6.6, y0 - 4.2, z), (sx * 6.6, y0 - 1.4, z + 0.2)], [0.5], 0.7, 'ss_tooth', pv, FRONT, ext=0.0)
    part('ss_jaw', jaw)
    # ---- the pectoral fins: long, sweeping out to the sides and forward like horns, notched on the trailing edge
    for sx, n in ((1, 'finr'), (-1, 'finl')):
        pv = PIVOT[n]; x0, fy, fz = pv
        f_ = chain([(x0, fy, fz), (x0 + sx * 5.0, fy + 2.0, fz - 3.6), (x0 + sx * 9.0, fy + 6.4, fz - 8.6), (x0 + sx * 10.6, fy + 10.8, fz - 13.0)],
                   [5.6, 3.6, 1.6], 1.0, 'ss_skin_dk', pv, UP, ext=0.3)
        f_ += chain([(x0 + sx * 6.0, fy + 3.0, fz - 4.0), (x0 + sx * 8.0, fy + 2.4, fz - 1.6)], [2.0], 0.8, 'ss_skin_dk', pv, (1.0, 0.0, 0.0), ext=0.1)   # (a torn notch)
        part(f'ss_{n}', f_)
    # ---- the tail: the stalk, then the great crescent (both lobes long)
    pv = PIVOT['tail']
    part('ss_tail', [el((-4.0, y0 - 3.4, 12.0), (4.0, y0 + 4.2, 17.4), 'ss_skin', pv, shift=(0.2, 0.6)),
                     el((-2.8, y0 - 2.0, 17.0), (2.8, y0 + 3.0, 22.0), 'ss_skin', pv, shift=(0.7, 0.3)),
                     el((-3.8, y0 - 3.5, 12.0), (3.8, y0 - 3.3, 17.4), 'ss_belly', pv)])
    pv = PIVOT['tail2']; tz = pv[2]; ty = pv[1]
    t2 = [el((-1.8, ty - 1.8, tz - 0.6), (1.8, ty + 2.0, tz + 2.6), 'ss_skin', pv)]
    t2 += chain([(0, ty + 0.4, tz + 1.0), (0, ty + 8.0, tz + 4.0), (0, ty + 15.0, tz + 8.6)], [7.0, 3.0], 1.2, 'ss_skin_dk', pv, (1.0, 0.0, 0.0), ext=0.3)
    t2 += chain([(0, ty - 0.4, tz + 1.0), (0, ty - 6.4, tz + 4.6), (0, ty - 11.0, tz + 8.6)], [6.0, 2.4], 1.0, 'ss_skin_dk', pv, (1.0, 0.0, 0.0), ext=0.3)
    part('ss_tail2', t2)
    return M


# ---------------------------------------------------------------------------------------------------- poses
def P(**kw):
    return kw


def swish(a, b=0.0):
    return dict(tail=qs(('y', a)), tail2=qs(('y', b if b else a * 1.4)))


def fins(dn=0.0, back=0.0):
    return dict(finr=qs(('z', dn), ('y', back)), finl=qs(('z', -dn), ('y', -back)))


POSES = {
    'idle_a': P(**swish(12), **fins(4), jaw=qs(('x', 18))),
    'idle_b': P(_face='rage', _off=(0, 0.4, 0), **swish(-12), **fins(-4), head=qs(('y', 8)), jaw=qs(('x', 26))),
    # swimming: a long, heavy S-wave, the maw always a little open
    **{f'swim_{i}': P(_off=(0, 0.6 * math.sin(2 * math.pi * i / 8), 0), body=qs(('y', 8 * math.sin(2 * math.pi * i / 8))),
                      head=qs(('y', -6 * math.sin(2 * math.pi * i / 8))), **swish(28 * math.sin(2 * math.pi * i / 8 + 0.8), 42 * math.sin(2 * math.pi * i / 8 + 1.6)),
                      **fins(6 * math.sin(2 * math.pi * i / 8)), jaw=qs(('x', 16))) for i in range(8)},
    # the chomp: the jaw dropped impossibly wide - then slammed shut
    'chomp_open': P(_face='rage', _off=(0, 0, -2.0), body=qs(('x', -10)), head=qs(('x', -16)), jaw=qs(('x', 55)), **swish(-24), **fins(12)),
    'chomp': P(_face='rage', _off=(0, 0, -7.0), body=qs(('x', 8)), head=qs(('x', 6)), jaw=qs(('x', 0)), **swish(30), **fins(-6)),
    # the rake: thrashing its head side to side, the torn fins slashing
    'saw_l': P(_face='rage', head=qs(('y', 34), ('z', 10)), body=qs(('y', -10), ('z', 20)), jaw=qs(('x', 30)), **swish(-30), **fins(20)),
    'saw_r': P(_face='rage', head=qs(('y', -34), ('z', -10)), body=qs(('y', 10), ('z', -20)), jaw=qs(('x', 30)), **swish(30), **fins(-20)),
    # the charge: streamlined, fins swept back, tail driving, jaws wide
    'charge': P(_face='rage', _off=(0, 0, -4.0), body=qs(('x', 6)), head=qs(('x', 4)), jaw=qs(('x', 40)), **swish(36), **fins(10, 30)),
    # the whirlpool: rolling over and over
    'roll_a': P(_face='rage', body=qs(('z', 90)), jaw=qs(('x', 36)), **swish(40)),
    'roll_b': P(_face='rage', body=qs(('z', -90)), jaw=qs(('x', 36)), **swish(-40)),
    'hurt': P(_face='shut', _off=(0, 0.8, 0), body=qs(('x', -14), ('z', 14)), jaw=qs(('x', 36)), **swish(-26)),
    'spawn': P(_face='rage', _off=(0, -16.0, 0), body=qs(('x', -40)), head=qs(('x', -20)), jaw=qs(('x', 50)), **swish(20)),
    'die': P(_face='shut', _off=(0, -2.0, 0), body=qs(('z', 160)), jaw=qs(('x', 40)), **swish(6), **fins(-20)),
}
SWIM_FRAMES = 8
DRAFT = ['idle_a', 'idle_b', 'swim_2', 'chomp_open', 'chomp', 'saw_l', 'charge', 'roll_a', 'hurt', 'die']

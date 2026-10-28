"""Kettle (2.95): the first Buddy the Gem of Creativity ever made - the embodiment of childlike simplicity and fun. From the owner's art:
a tall stick figure, completely flat like Mr. Capshun (a drawing come to life), with a big round head - pale, shaded off at one side
like pencil on paper, a bold black outline - and a sweep of fine strands springing off the top of it; two big tall oval eyes and a
small happy smile. One hand on his hip, the other held out palm-up, as if to say "well, what shall we play?". Everything else is a
line of ink - and long ones: he's a head taller than Capshun.

He plays. His toys (PixelLab, ref/pixellab/kettle): a jump rope, a paper plane, a red playground ball - one in his right hand at a
time, as each pose says (_tool).

A rigkit rig like Capshun's: body, head (a model per expression), arms bent at the elbow, legs bent at the knee, the toy in his right
hand. Design units: feet at y=0, facing -z, his right is +x."""
import math
from PIL import Image, ImageDraw

from phase57_art import hexc
import sys
from rigkit import qs, el, seg, point

PREFIX = 'kt_'
RIG_SCALE = 0.78                                   # (2.95e: as tall as Mr. Capshun - his head tops out where Capshun's does)
PIVOT = {'body': (0, 14.0, 0), 'head': (0, 25.4, 0),
         'armr': (0.3, 24.0, 0), 'forer': (3.0, 17.4, 0), 'arml': (-0.3, 24.0, 0), 'forel': (-3.0, 17.4, 0),
         'legr': (0.25, 14.0, 0), 'shinr': (1.7, 7.2, 0), 'legl': (-0.25, 14.0, 0), 'shinl': (-1.7, 7.2, 0), 'tool': (3.4, 10.6, 0)}
PARENT = {'body': None, 'head': 'body', 'armr': 'body', 'forer': 'armr', 'arml': 'body', 'forel': 'arml',
          'legr': None, 'shinr': 'legr', 'legl': None, 'shinl': 'legl', 'tool': 'forer'}
TOOLS = ('rope', 'plane', 'ball', 'none')
TOOL_S, TOOL_GRIP = 12.0, (34, 34)                 # (the toy's square, design units; where in its 64-pixel picture his hand holds it)
PARTS = tuple(PIVOT)
PART_K = {}
FACES = ('happy', 'surprised', 'blink', 'determined', 'grin', 'puzzled')
INK = '#161616'
LW, LD = 0.72, 0.3
HEAD_C, HEAD_R = (0.0, 31.0), 5.8                 # (the disc; its square is wider - the strands spring out past it)
HEAD_K = 1.3                                      # (the head's square, as a share of the disc's radius: room for the strands)
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)


def HIDDEN(p, pose):
    return p == 'tool' and pose.get('_tool', 'none') == 'none'


def model_name(p, pose, suffix=''):
    if p == 'tool':
        return f'{PREFIX}tool_{pose.get("_tool", "none")}{suffix}'
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
SS = 4
N = 128


def _disc(shade=True):
    """the head's page: a pale disc lit from the upper left (pencil on paper), the outline bold - and his strands, springing up and
    over to his left (our right) off the top, past the disc's edge -> (image at SS x, draw)"""
    S = N * SS; cx = cy = S / 2; r = S / 2 / HEAD_K - 2 * SS
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); px = im.load()
    hx, hy = cx - r * 0.35, cy - r * 0.45
    for y in range(S):
        for x in range(S):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                t = min(1.0, math.hypot(x - hx, y - hy) / (r * 1.9)) ** 1.6 if shade else 0
                v = round(252 - t * 58)
                px[x, y] = (v, v, v, 255)
    d = ImageDraw.Draw(im)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=hexc(INK), width=5 * SS)
    # the strands: six fine curls out of the crown, sweeping over to our right (as in the art)
    for i, a0 in enumerate((-100, -85, -70, -55, -40, -25)):
        a = math.radians(a0)
        x0, y0 = cx + r * math.cos(a), cy + r * math.sin(a)
        L = r * (0.32 + 0.06 * (i % 3))
        bend = math.radians(a0 + 28)
        x1, y1 = x0 + L * 0.6 * math.cos(a), y0 + L * 0.6 * math.sin(a)
        x2, y2 = x1 + L * 0.5 * math.cos(bend), y1 + L * 0.5 * math.sin(bend)
        d.line((x0, y0, x1, y1, x2, y2), fill=hexc(INK), width=3 * SS, joint='curve')
    return im, d


def _down(im):
    im = im.resize((N, N), Image.LANCZOS); px = im.load()
    for y in range(N):
        for x in range(N):
            r, g, b, a = px[x, y]
            px[x, y] = (r, g, b, 255 if a >= 128 else 0)
    return im


def _face(kind=None):
    """the face (in the disc's own 128 frame, squeezed to the disc): two big tall ovals, his left a touch bigger and higher; light
    brows; a small smile, low and to one side. Each expression redraws them."""
    im, d = _disc(); k = SS; ink = hexc(INK); W5, W4 = 5 * k, 4 * k
    S = N * SS; r = S / 2 / HEAD_K - 2 * SS; o = S / 2 - r                        # (the disc's box inside the square)
    E = lambda b: tuple(o + v / 128 * 2 * r for v in b)                       # (the face's 128-grid, on the disc)

    def eye(box, white=True):
        d.ellipse(E(box), fill=(255, 255, 255, 255) if white else None, outline=ink, width=W4)

    def arc(box, a0, a1, w=W5):
        d.arc(E(box), a0, a1, fill=ink, width=w)
    le, re = (30, 34, 56, 78), (68, 28, 98, 78)
    if kind == 'blink':
        arc((30, 50, 56, 66), 200, 340); arc((68, 46, 98, 62), 200, 340)
    elif kind == 'happy':
        arc((30, 46, 56, 68), 190, 350); arc((68, 42, 98, 64), 190, 350)
    elif kind == 'surprised':
        eye((27, 28, 59, 82)); eye((65, 22, 101, 80))
    elif kind == 'determined':
        eye((30, 42, 56, 76)); eye((68, 38, 98, 74))
    else:
        eye(le); eye(re)
    if kind == 'determined':
        d.line(E((28, 30, 56, 38)), fill=ink, width=W5); d.line(E((70, 34, 98, 24)), fill=ink, width=W5)
    elif kind == 'puzzled':
        arc((26, 20, 58, 36), 215, 330); arc((66, 8, 100, 30), 195, 320)
    else:
        arc((28, 16, 58, 30), 205, 335); arc((66, 10, 100, 26), 205, 335)
    if kind in ('happy', None):
        arc((60, 84, 92, 104), 15, 165)                                         # (his small smile, off to one side)
    elif kind == 'grin':
        d.chord(E((52, 82, 92, 110)), 0, 180, fill=ink); d.chord(E((62, 96, 82, 108)), 0, 180, fill=hexc('#e05a6a'))
    elif kind == 'surprised':
        d.ellipse(E((66, 90, 78, 104)), outline=ink, width=W4)
    elif kind == 'determined':
        arc((58, 88, 90, 100), 20, 160)
    else:
        arc((60, 92, 86, 104), 200, 340)
    return _down(im)


def _back():
    im, _d = _disc()
    return _down(im)


def _solid(c):
    return Image.new('RGBA', (16, 16), hexc(c)[:3] + (255,))


def textures():
    T = {'kt_face': _face(), 'kt_back': _back(), 'kt_ink': _solid(INK)}
    for k in FACES:
        T[f'kt_face_{k}'] = _face(k)
    import os
    D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ref', 'pixellab', 'kettle')
    for k in TOOLS[:-1]:
        T[f'kt_t_{k}'] = Image.open(os.path.join(D, f'{k}.png')).convert('RGBA')
    return T


# ---------------------------------------------------------------------------------------------------- models
def line(a, b, pv, w=LW, tex='kt_ink'):
    return seg((a[0], a[1], 0.0), (b[0], b[1], 0.0), w, LD, tex, pv, up=(0.0, 0.0, -1.0), ext=w * 0.4)


def models():
    M = {}

    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)
    part('kt_body', [line((0, 25.4), (0, 13.8), PIVOT['body'])])
    pv = PIVOT['head']; (hx, hy), r = HEAD_C, HEAD_R * HEAD_K

    def head(face=None):
        ft = 'kt_face' if face is None else f'kt_face_{face}'
        return [el((hx - r, hy - r, -LD / 2 - 0.01), (hx + r, hy + r, -LD / 2 - 0.01), ft, pv, faces=('north',), uv={'north': [0, 0, 16, 16]}),
                el((hx - r, hy - r, LD / 2 + 0.01), (hx + r, hy + r, LD / 2 + 0.01), 'kt_back', pv, faces=('south',), uv={'south': [16, 0, 0, 16]})]
    part('kt_head', head())
    for fc in FACES:
        part(f'kt_head_x{fc}', head(fc))
    for s, sx in (('r', 1), ('l', -1)):
        ap, fp = PIVOT[f'arm{s}'], PIVOT[f'fore{s}']
        part(f'kt_arm{s}', [line(ap[:2], fp[:2], ap)])
        part(f'kt_fore{s}', [line(fp[:2], (sx * 3.4, 10.6), fp)])
        lp, sp = PIVOT[f'leg{s}'], PIVOT[f'shin{s}']
        part(f'kt_leg{s}', [line(lp[:2], sp[:2], lp)])
        part(f'kt_shin{s}', [line(sp[:2], (sx * 2.6, 0.36), sp)])
    tp = PIVOT['tool']
    x1, y1 = tp[0] + TOOL_GRIP[0] * TOOL_S / 64, tp[1] + TOOL_GRIP[1] * TOOL_S / 64
    for k in TOOLS[:-1]:
        e = el((x1 - TOOL_S, y1 - TOOL_S, -0.01), (x1, y1, 0.01), f'kt_t_{k}', tp, faces=('north', 'south'), uv={'north': [0, 0, 16, 16], 'south': [16, 0, 0, 16]})
        part(f'kt_tool_{k}', [e])
    # (no toy: a speck of nothing at the hand)
    part('kt_tool_none', [el((tp[0] - 0.01, tp[1] - 0.01, -0.01), (tp[0] + 0.01, tp[1] + 0.01, 0.01), 'kt_ink', tp, faces=('north',))])
    M['kt_tool'] = M['kt_tool_none']
    return M


# ---------------------------------------------------------------------------------------------------- poses
def limb(sx, fwd=0.0, out=0.0, turn=0.0):
    return qs(('y', turn * sx), ('x', -fwd), ('z', -out * sx))


def P(**kw):
    return kw


# the art: his left hand on his hip, his right held out palm-up - "well, what shall we play?"
WHATNOW = dict(arml=limb(-1, 0, 34), forel=limb(-1, 0, -81), armr=limb(1, 10, 40), forer=limb(1, 30, 40),
               legr=limb(1, 0, -3), shinr=limb(1, 0, 4), legl=limb(-1, 0, 3), shinl=limb(-1, 0, -2))
LOOSE = dict(armr=limb(1, 0, 8), forer=limb(1, 6, -4), arml=limb(-1, 0, 8), forel=limb(-1, 6, -4))


def walk(k, a=26.0, lift=0.0):
    s = math.sin(math.pi * k / 2)
    return dict(legr=limb(1, a * s), shinr=limb(1, -max(0.0, -s) * 44), legl=limb(-1, -a * s), shinl=limb(-1, -max(0.0, s) * 44),
                armr=limb(1, -a * 0.9 * s, 10), forer=limb(1, 24, -4), arml=limb(-1, a * 0.9 * s, 10), forel=limb(-1, 24, -4),
                _off=(0, lift * abs(math.cos(math.pi * k / 2)), 0))


POSES = {
    'idle_a': P(head=qs(('z', -4)), **WHATNOW),
    # a little hop on the spot, arms up - he can't keep still for long
    'idle_b': P(_face='grin', _off=(0, 1.2, 0), legr=limb(1, 20), shinr=limb(1, -40), legl=limb(-1, 20), shinl=limb(-1, -40),
                armr=limb(1, 0, 108), forer=limb(1, 0, 30), arml=limb(-1, 0, 108), forel=limb(-1, 0, 30)),
    # gazing up at the sky, hands behind his back, rocking on his heels
    'idle_c': P(_face='happy', head=qs(('x', -24)), armr=limb(1, -30, 4), forer=limb(1, -60), arml=limb(-1, -30, 4), forel=limb(-1, -60)),
    # wondering - head on one side, a finger at his chin
    'idle_d': P(_face='puzzled', head=qs(('z', 12)), **dict(WHATNOW, armr=limb(1, 40, 20), forer=limb(1, 100, -10))),
    # a skippy walk: a hop in every step
    **{f'walk_{k}': P(head=qs(('z', 4 * math.sin(math.pi * k / 2))), **walk(k, lift=0.8)) for k in range(4)},
    **{f'run_{k}': P(_face='grin', body=qs(('x', 10)), head=qs(('x', -8)), **dict(walk(k, 44, 1.4), forer=limb(1, 70, -6), forel=limb(-1, 70, -6))) for k in range(4)},
    'jump': P(_face='grin', _off=(0, 2.0, 0), legr=limb(1, 40), shinr=limb(1, -70), legl=limb(-1, 10), shinl=limb(-1, -40),
              armr=limb(1, 0, 112), forer=limb(1, 0, 30), arml=limb(-1, 0, 112), forel=limb(-1, 0, 30)),
    # TAG: drawn back - then a quick poke ("you're it!")
    'tag_up': P(_face='grin', body=qs(('y', -18)), armr=limb(1, -30, 20), forer=limb(1, 40), arml=limb(-1, 20, 30), forel=limb(-1, 30)),
    'tag': P(_face='happy', body=qs(('y', 16), ('x', 6)), armr=limb(1, 92, 0), forer=limb(1, 0), arml=limb(-1, -20, 30), forel=limb(-1, 20)),
    # CARTWHEEL: four quarter-turns about his middle, arms and legs a star
    **{f'cart_{k}': P(_face='grin', body=qs(('z', -90 * k)), _off=(0, 6.0 if k % 2 else 3.0, 0),
                      legr=qs(('z', -90 * k - 30)), legl=qs(('z', -90 * k + 30)), shinr=limb(1, 0), shinl=limb(-1, 0),
                      armr=limb(1, 0, 100), forer=limb(1, 0), arml=limb(-1, 0, 100), forel=limb(-1, 0)) for k in range(4)},
    # PAPER PLANES: the plane held up by his ear - then let fly
    'throw_up': P(_tool='plane', _face='determined', body=qs(('y', -20)), armr=limb(1, -30, 50), forer=limb(1, 80), arml=limb(-1, 40, 10), forel=limb(-1, 20)),
    'throw': P(_tool='none', _face='grin', body=qs(('y', 16), ('x', 4)), armr=limb(1, 100, 0), forer=limb(1, 0), arml=limb(-1, -20, 24), forel=limb(-1, 20)),
    # KICKBALL: the ball dropped - and a big kick
    'kick_up': P(_tool='ball', _face='determined', body=qs(('x', -6)), legr=limb(1, -40), shinr=limb(1, -60), armr=limb(1, 30, 10), forer=limb(1, 30),
                 arml=limb(-1, 0, 40), forel=limb(-1, 0, 20)),
    'kick': P(_tool='none', _face='grin', body=qs(('x', -14)), legr=limb(1, 90), shinr=limb(1, 0), legl=limb(-1, -10), armr=limb(1, -20, 50), forer=limb(1, 10),
              arml=limb(-1, 20, 60), forel=limb(-1, 10)),
    # JUMP ROPE: skipping - the rope over his head, then under his feet
    'rope_a': P(_tool='rope', _face='happy', _off=(0, 1.4, 0), legr=limb(1, 10), shinr=limb(1, -30), legl=limb(-1, 10), shinl=limb(-1, -30),
                armr=limb(1, 0, 60), forer=limb(1, 0, 40), arml=limb(-1, 0, 60), forel=limb(-1, 0, 40)),
    'rope_b': P(_tool='rope', _face='grin', _off=(0, 0.2, 0), armr=limb(1, 20, 30), forer=limb(1, 20), arml=limb(-1, 20, 30), forel=limb(-1, 20)),
    # RECESS! (charged): a great leap, arms flung wide
    'recess_a': P(_face='determined', _off=(0, -1.4, 0), body=qs(('x', 10)), legr=limb(1, 50), shinr=limb(1, -90), legl=limb(-1, 50), shinl=limb(-1, -90),
                  armr=limb(1, -40, 20), forer=limb(1, 20), arml=limb(-1, -40, 20), forel=limb(-1, 20)),
    'recess_b': P(_face='grin', _off=(0, 3.0, 0), legr=limb(1, 0, 34), legl=limb(-1, 0, 34), armr=limb(1, 0, 150), forer=limb(1, 0), arml=limb(-1, 0, 150), forel=limb(-1, 0)),
    'happy': P(_face='happy', _off=(0, 0.8, 0), armr=limb(1, 0, 110), forer=limb(1, 0, 40), arml=limb(-1, 0, 110), forel=limb(-1, 0, 40)),
    'wave_a': P(_face='happy', **dict(LOOSE, arml=limb(-1, 0, 110), forel=limb(-1, 0, 60), head=qs(('z', -6)))),
    'wave_b': P(_face='happy', **dict(LOOSE, arml=limb(-1, 0, 110), forel=limb(-1, 0, 20), head=qs(('z', -6)))),
    # sitting cross-legged...
    'sit_a': P(body=qs(('x', -4)), legr=limb(1, 84, 50), shinr=limb(1, 0, -120), legl=limb(-1, 84, 50), shinl=limb(-1, 0, -120),
               armr=limb(1, 10, 10), forer=limb(1, 40), arml=limb(-1, 10, 10), forel=limb(-1, 40), head=qs(('z', 6))),
    # ...and lying back, watching the clouds
    'sit_b': P(_face='happy', body=qs(('x', -80)), head=qs(('x', 10)), legr=limb(1, 90, 6), shinr=limb(1, 0), legl=limb(-1, 70, 6), shinl=limb(-1, 30),
               armr=limb(1, -150, 10), forer=limb(1, -60), arml=limb(-1, -150, 10), forel=limb(-1, -60)),
    # (2.96c) riding Bender: astride, legs down either side, one hand on Bender's neck - the other up in the air: WHEEE
    'ride': P(_face='grin', _tool='none', body=qs(('x', -6)), head=qs(('z', -6)), legr=limb(1, 26, 70), shinr=limb(1, -16, -54), legl=limb(-1, 26, 70), shinl=limb(-1, -16, -54),
              armr=limb(1, 0, 150), forer=limb(1, 0, 20), arml=limb(-1, 40, 30), forel=limb(-1, 36)),
    'hurt': P(_face='surprised', body=qs(('x', -10)), head=qs(('x', -10)), armr=limb(1, 20, 60), forer=limb(1, 0, 40), arml=limb(-1, 20, 60), forel=limb(-1, 0, 40)),
    'tired': P(_face='blink', _off=(0, -0.6, 0), body=qs(('x', 16), ('z', -6)), head=qs(('x', 22)), armr=limb(1, 0, 2), forer=limb(1, 4), arml=limb(-1, 0, 2), forel=limb(-1, 4)),
}
SWIM_FRAMES = 8
for _i in range(SWIM_FRAMES):                              # (a doggy paddle, big splashy strokes)
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(_face='grin', _off=(0, -8.0 + 0.4 * math.sin(2 * _p), 0), body=qs(('x', 70)), head=qs(('x', -50)),
                            armr=limb(1, 120 + 50 * math.sin(_p), 10), forer=limb(1, 30), arml=limb(-1, 120 - 50 * math.sin(_p), 10), forel=limb(-1, 30),
                            legr=limb(1, 20 * math.sin(2 * _p)), legl=limb(-1, -20 * math.sin(2 * _p)), shinr=limb(1, -20), shinl=limb(-1, -20))

_ME = sys.modules[__name__]
_FEET = [('shinr', (2.6, 0.36)), ('shinl', (-2.6, 0.36)), ('legr', (1.7, 7.2)), ('legl', (-1.7, 7.2))]
_SEAT = [('body', (0, 13.8))]
_HEAD = [('body', (0, 25.4))]
_HANDS = [('forer', (3.4, 10.6)), ('forel', (-3.4, 10.6))]


def _ground(pose, refs, lift=0.0):
    pose = dict(pose); pose.pop('_off', None)
    low = min(point(_ME, pose, p, (x, y, 0.0))[1] * 16 for p, (x, y) in refs)
    pose['_off'] = (0.0, round(lift - low + 0.32, 3), 0.0)
    return pose


for _k in list(POSES):
    if _k.startswith('swim_') or _k == 'jump' or _k in ('idle_b', 'rope_a', 'recess_b'):
        continue
    if _k.startswith('cart_'):                             # (a cartwheel: whichever of hands, feet or head is lowest touches the ground)
        POSES[_k] = _ground(POSES[_k], _FEET + _HANDS + [('body', (0, 25.4)), ('head', (0, 37.0))])
        continue
    _sit = _k.startswith('sit_')
    POSES[_k] = _ground(POSES[_k], _FEET + _SEAT + (_HEAD if _k == 'sit_b' else []) if _sit else _FEET,
                        lift=(1.2 if _k in ('run_1', 'run_3') else 0.6 if _k in ('walk_1', 'walk_3') else 0.0))
DRAFT = ['idle_a', 'idle_b', 'idle_c', 'idle_d', 'walk_1', 'run_1', 'jump', 'tag_up', 'tag', 'cart_0', 'cart_1', 'cart_2', 'cart_3', 'throw_up', 'kick_up', 'kick',
         'rope_a', 'rope_b', 'recess_a', 'recess_b', 'happy', 'sit_a', 'sit_b', 'hurt', 'swim_2']

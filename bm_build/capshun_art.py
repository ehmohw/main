"""Mr. Capshun (2.90): a stick figure - and completely flat - from the owner's sketch. One of the Buddies, the strange folk born of
pure imagination. A big round head, pale grey and shaded at one side like pencil on paper, a bold black outline; two tall empty
oval eyes, one a little bigger than the other; worried brows (one arched high); a small frown. Everything else is a line:
the body, the long thin arms, the long thin legs, all in black ink. He fights with a paintbrush (its bristles in the three primary
colours) and a pencil - (2.94) one at a time, in his right hand, swapped for whatever he's doing (PixelLab drew them both).

FLAT: the head is a disc with no depth (seen edge-on it's a sliver), the lines are thin strips of ink. Turned side-on he all but
vanishes - and he knows it (one of his idles).

A rigkit rig like Queen Ava's: body (the line from neck to hips), head (a model per expression - the face drawn on), arms bent
at the elbow (the brush in his right hand, the pencil in his left), legs bent at the knee. Design units: feet at y=0, facing -z, his right is +x."""
import math
from PIL import Image, ImageDraw

from phase57_art import hexc
import sys
from rigkit import qs, el, seg, point

PREFIX = 'mz_'
RIG_SCALE = 0.95
PIVOT = {'body': (0, 11.2, 0), 'head': (0, 21.0, 0),
         'armr': (0.3, 19.6, 0), 'forer': (2.6, 13.6, 0), 'arml': (-0.3, 19.6, 0), 'forel': (-2.6, 13.6, 0),
         'legr': (0.25, 11.2, 0), 'shinr': (1.5, 5.8, 0), 'legl': (-0.25, 11.2, 0), 'shinl': (-1.5, 5.8, 0), 'tool': (3.1, 6.8, 0)}
PARENT = {'body': None, 'head': 'body', 'armr': 'body', 'forer': 'armr', 'arml': 'body', 'forel': 'arml',
          'legr': None, 'shinr': 'legr', 'legl': None, 'shinl': 'legl', 'tool': 'forer'}
# (2.94) ONE TOOL AT A TIME, in his right hand (PixelLab's pencil and paintbrush, ref/pixellab/capshun): the pencil for what he draws,
# the brush for what he paints - each pose says which (_tool), and the part's model swaps with it
TOOLS = ('pencil', 'brush')
TOOL_S, TOOL_GRIP = 8.5, (40, 24)                 # (the tool's square, design units; where in its 64-pixel picture his hand holds it)
PARTS = tuple(PIVOT)
PART_K = {}
FACES = ('happy', 'surprised', 'blink', 'determined', 'grin', 'puzzled')
INK = '#161616'
LW, LD = 0.72, 0.3                              # (a line: its width on the page, and its depth - he's flat)
HEAD_C, HEAD_R = (0.0, 25.6), 4.6
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)
PAINT = {'red': '#ff3a3a', 'yellow': '#ffd02a', 'blue': '#2a7aff'}


def HIDDEN(p, pose):
    return False


def model_name(p, pose, suffix=''):
    if p == 'tool':
        return f'{PREFIX}tool_{pose.get("_tool", "pencil")}{suffix}'
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
SS = 4                                           # (drawn 4x over, brought down smooth; the outline's edge kept hard)
N = 128


def _disc():
    """the head's page: a pale grey disc, lit from the upper left and shaded off to the lower right (pencil on paper),
    with its bold outline. -> (image at SS x, draw)"""
    S = N * SS; cx = cy = S / 2; r = S / 2 - 2 * SS
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); px = im.load()
    hx, hy = S * 0.36, S * 0.32
    for y in range(S):
        for x in range(S):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                t = min(1.0, math.hypot(x - hx, y - hy) / (S * 0.78)) ** 1.6
                v = round(250 - t * 62)
                px[x, y] = (v, v, v, 255)
    d = ImageDraw.Draw(im)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=hexc(INK), width=5 * SS)
    return im, d


def _down(im):
    im = im.resize((N, N), Image.LANCZOS); px = im.load()
    for y in range(N):
        for x in range(N):
            r, g, b, a = px[x, y]
            px[x, y] = (r, g, b, 255 if a >= 128 else 0)
    return im


def _face(kind=None):
    """(2.94: his default is a smile, eyes open - the worried look of the sketch is 'puzzled', for an idle) the face, after the sketch: two tall empty ovals for eyes (his left a touch bigger, set higher), worried brows - the left
    one arched high - and a small frown. Each expression redraws the eyes, brows and mouth."""
    im, d = _disc(); k = SS; ink = hexc(INK); W5, W4 = 5 * k, 4 * k
    E = lambda b: tuple(v * k for v in b)

    def eye(box, white=True):
        d.ellipse(E(box), fill=(255, 255, 255, 255) if white else None, outline=ink, width=W4)

    def arc(box, a0, a1, w=W5):
        d.arc(E(box), a0, a1, fill=ink, width=w)
    le, re = (30, 38, 54, 74), (66, 32, 94, 72)                                  # (his right eye on our left)
    if kind == 'blink':
        arc((30, 50, 54, 64), 200, 340); arc((66, 46, 94, 60), 200, 340)
    elif kind == 'happy':
        arc((30, 46, 54, 66), 190, 350); arc((66, 42, 94, 62), 190, 350)
    elif kind == 'surprised':
        eye((27, 32, 55, 76)); eye((64, 26, 96, 74))
    elif kind == 'determined':
        eye((30, 44, 54, 72)); eye((66, 40, 94, 70))
    else:
        eye(le); eye(re)
    # the brows (2.94: the default - kind None - relaxed and level; the sketch's worried ones are 'puzzled')
    if kind == 'determined':
        d.line(E((28, 34, 54, 42)), fill=ink, width=W5); d.line(E((68, 38, 96, 28)), fill=ink, width=W5)
    elif kind in ('happy', 'grin', 'surprised'):
        arc((28, 18, 56, 34), 200, 340); arc((64, 12, 96, 30), 200, 340)
    elif kind is None:
        arc((28, 22, 56, 36), 205, 335); arc((64, 18, 96, 32), 205, 335)
    else:
        arc((26, 24, 56, 40), 215, 330); arc((64, 10, 98, 34), 195, 320)          # (worried: the left one arched high)
    # the mouth
    if kind in ('happy', None):
        arc((46, 78, 82, 100), 20, 160)
    elif kind == 'grin':
        d.chord(E((44, 80, 84, 108)), 0, 180, fill=ink); d.chord(E((54, 94, 74, 106)), 0, 180, fill=hexc('#e05a6a'))
    elif kind == 'surprised':
        d.ellipse(E((58, 88, 70, 102)), outline=ink, width=W4)
    elif kind == 'determined':
        d.line(E((50, 94, 78, 92)), fill=ink, width=W5)
    else:
        arc((50, 90, 76, 104), 200, 340)                                          # (the frown)
    return _down(im)


def _back():
    im, _d = _disc()
    return _down(im)


def _solid(c):
    return Image.new('RGBA', (16, 16), hexc(c)[:3] + (255,))


def textures():
    T = {'mz_face': _face(), 'mz_back': _back(), 'mz_ink': _solid(INK), 'mz_wood': _solid('#b07a3e'), 'mz_steel': _solid('#c0c4cc'),
         'mz_pink': _solid('#f08aa0'), 'mz_pencil': _solid('#f6c83a'), 'mz_wood_lt': _solid('#e8c49a'), 'mz_lead': _solid('#3a3a40')}
    for k, c in PAINT.items():
        T[f'mz_{k}'] = _solid(c)
    for k in FACES:
        T[f'mz_face_{k}'] = _face(k)
    import os
    D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ref', 'pixellab', 'capshun')
    for k in TOOLS:
        T[f'mz_t_{k}'] = Image.open(os.path.join(D, f'{k}.png')).convert('RGBA')
    return T


# ---------------------------------------------------------------------------------------------------- models
def line(a, b, pv, w=LW, tex='mz_ink'):
    """a stroke of ink from a to b (on the page: z = 0)"""
    return seg((a[0], a[1], 0.0), (b[0], b[1], 0.0), w, LD, tex, pv, up=(0.0, 0.0, -1.0), ext=w * 0.4)


def models():
    M = {}

    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)
    part('mz_body', [line((0, 21.3), (0, 11.0), PIVOT['body'])])
    pv = PIVOT['head']; (hx, hy), r = HEAD_C, HEAD_R

    def head(face=None):
        ft = 'mz_face' if face is None else f'mz_face_{face}'
        # (2.94: no edges on the disc - a square slab's sides showed as stray lines round his round head, seen at an angle)
        return [el((hx - r, hy - r, -LD / 2 - 0.01), (hx + r, hy + r, -LD / 2 - 0.01), ft, pv, faces=('north',), uv={'north': [0, 0, 16, 16]}),
                el((hx - r, hy - r, LD / 2 + 0.01), (hx + r, hy + r, LD / 2 + 0.01), 'mz_back', pv, faces=('south',), uv={'south': [16, 0, 0, 16]})]
    part('mz_head', head())
    for fc in FACES:
        part(f'mz_head_x{fc}', head(fc))
    for s, sx in (('r', 1), ('l', -1)):
        ap, fp = PIVOT[f'arm{s}'], PIVOT[f'fore{s}']
        part(f'mz_arm{s}', [line(ap[:2], fp[:2], ap)])
        hand = (sx * 3.1, 6.8)
        els = [line(fp[:2], hand, fp)]
        part(f'mz_fore{s}', els)
        lp, sp = PIVOT[f'leg{s}'], PIVOT[f'shin{s}']
        part(f'mz_leg{s}', [line(lp[:2], sp[:2], lp)])
        part(f'mz_shin{s}', [line(sp[:2], (sx * 2.3, 0.36), sp)])
    # the tool: a flat picture in his right hand (front and back), the grip at his hand
    tp = PIVOT['tool']
    x1, y1 = tp[0] + TOOL_GRIP[0] * TOOL_S / 64, tp[1] + TOOL_GRIP[1] * TOOL_S / 64
    for k in TOOLS:
        e = el((x1 - TOOL_S, y1 - TOOL_S, -0.01), (x1, y1, 0.01), f'mz_t_{k}', tp, faces=('north', 'south'), uv={'north': [0, 0, 16, 16], 'south': [16, 0, 0, 16]})
        part(f'mz_tool_{k}', [e])
    M['mz_tool'] = M['mz_tool_pencil']
    return M


# ---------------------------------------------------------------------------------------------------- poses
def limb(sx, fwd=0.0, out=0.0, turn=0.0):
    """fwd: swung forward (out of the page); out: swung out to his side, on the page (negative: in, across him)"""
    return qs(('y', turn * sx), ('x', -fwd), ('z', -out * sx))


def P(**kw):
    return kw


# the sketch: a hand on his hip, the pencil in the other, his head tilted - wondering, a little worried
# (2.94: his hand on his hip, the pencil held loosely in the other - the hand at his chin went through his head)
PONDER = dict(arml=limb(-1, 0, 34), forel=limb(-1, 0, -81), armr=limb(1, 0, 10), forer=limb(1, 0, 22),
              legr=limb(1, 0, -3), shinr=limb(1, 0, 4), legl=limb(-1, 0, 3), shinl=limb(-1, 0, -2))
LOOSE = dict(armr=limb(1, 0, 8), forer=limb(1, 6, -4), arml=limb(-1, 0, 8), forel=limb(-1, 6, -4))


def walk(k, a=24.0, lift=0.0):
    s = math.sin(math.pi * k / 2)
    return dict(legr=limb(1, a * s), shinr=limb(1, -max(0.0, -s) * 40), legl=limb(-1, -a * s), shinl=limb(-1, -max(0.0, s) * 40),
                armr=limb(1, -a * 0.8 * s, 6), forer=limb(1, 20, -4), arml=limb(-1, a * 0.8 * s, 6), forel=limb(-1, 20, -4),
                _off=(0, lift * abs(math.cos(math.pi * k / 2)), 0))


POSES = {
    'idle_a': P(head=qs(('z', 4)), **PONDER),
    # (2.94) now and then the sketch's own look: puzzled, the head tilted further, wondering
    'idle_d': P(_face='puzzled', head=qs(('z', 10)), **PONDER),
    # a shrug - and a worried look at you
    'idle_b': P(_face='surprised', head=qs(('z', -4), ('x', -4)), armr=limb(1, 0, 34), forer=limb(1, 0, 70), arml=limb(-1, 0, 34), forel=limb(-1, 0, 70)),
    # side-on: he turns - and all but vanishes (he's flat). He peeks round to check you're still there.
    'idle_c': P(_face='blink', body=qs(('y', 86)), legr=qs(('y', 86)), legl=qs(('y', 86))),
    **{f'walk_{k}': P(head=qs(('z', 3 * math.sin(math.pi * k / 2))), **walk(k, lift=0.3)) for k in range(4)},
    **{f'run_{k}': P(body=qs(('x', 10)), head=qs(('x', -8)), **dict(walk(k, 40, 1.0), forer=limb(1, 70, -6), forel=limb(-1, 70, -6))) for k in range(4)},
    'jump': P(_face='surprised', _off=(0, 1.6, 0), legr=limb(1, 40), shinr=limb(1, -70), legl=limb(-1, 10), shinl=limb(-1, -40),
              armr=limb(1, 0, 95), forer=limb(1, 0, 55), arml=limb(-1, 0, 95), forel=limb(-1, 0, 55)),
    # the brush swipe: up over his shoulder - then down through the foe
    'swipe_up': P(_tool='brush', _face='determined', body=qs(('y', -14)), armr=limb(1, 150, 55), forer=limb(1, 40), arml=limb(-1, 10, 26), forel=limb(-1, 30)),
    'swipe': P(_tool='brush', _face='determined', body=qs(('y', 18), ('x', 6)), armr=limb(1, 50, -16), forer=limb(1, 10), arml=limb(-1, -10, 30), forel=limb(-1, 20)),
    # the paint splat: drawn back - then flung
    'fling_up': P(_tool='brush', _face='determined', body=qs(('y', -20)), armr=limb(1, -40, 34), forer=limb(1, 70), arml=limb(-1, 50, 10), forel=limb(-1, 20)),
    'fling': P(_tool='brush', _face='grin', body=qs(('y', 16), ('x', 4)), armr=limb(1, 112, 0), forer=limb(1, 0), arml=limb(-1, -20, 24), forel=limb(-1, 20)),
    # a fresh coat (painting you): quick strokes in the air
    'paint_a': P(_tool='brush', _face='grin', armr=limb(1, 80, 34), forer=limb(1, 30), arml=limb(-1, 0, 20), forel=limb(-1, 0, 30)),
    'paint_b': P(_tool='brush', _face='grin', armr=limb(1, 80, -20), forer=limb(1, 30), arml=limb(-1, 0, 20), forel=limb(-1, 0, 30)),
    # wet paint: down on one knee, the brush slapped across the ground
    'splash': P(_tool='brush', _face='determined', _off=(0, -2.0, 0), body=qs(('x', 18)), head=qs(('x', -12)), legr=limb(1, 70), shinr=limb(1, -90), legl=limb(-1, -10), shinl=limb(-1, -80),
                armr=limb(1, 60, 50), forer=limb(1, 20), arml=limb(-1, 20, 40), forel=limb(-1, 20)),
    # THE RAINBOW STROKE (charged): the brush raised high, swept over in a great arc
    'rainbow_a': P(_tool='brush', _face='grin', _off=(0, 0.4, 0), body=qs(('z', 8)), armr=limb(1, 10, 98), forer=limb(1, 0, 70), arml=limb(-1, 0, 40), forel=limb(-1, 0, 20)),
    'rainbow_b': P(_tool='brush', _face='grin', _off=(0, 0.6, 0), armr=limb(1, 60, 110), forer=limb(1, 0), arml=limb(-1, 0, 40), forel=limb(-1, 0, 20)),
    'rainbow_c': P(_tool='brush', _face='grin', _off=(0, 0.2, 0), body=qs(('z', -10)), armr=limb(1, 40, -50), forer=limb(1, 0), arml=limb(-1, 0, 60), forel=limb(-1, 0, 30)),
    # the sketch: quick scribbles in the air with the pencil - an outline drawn round the foe
    'scribble_a': P(_face='grin', armr=limb(1, 84, 30), forer=limb(1, 34), arml=limb(-1, 0, 20), forel=limb(-1, 0, 30)),
    'scribble_b': P(_face='grin', armr=limb(1, 70, -10), forer=limb(1, 50), arml=limb(-1, 0, 20), forel=limb(-1, 0, 30)),
    # (2.94) drawn to life: a quick sketch in the air - then he tosses it, and it's real
    'toss_up': P(_face='determined', body=qs(('y', -20)), armr=limb(1, -40, 34), forer=limb(1, 70), arml=limb(-1, 50, 10), forel=limb(-1, 20)),
    'toss': P(_face='grin', body=qs(('y', 16), ('x', 4)), armr=limb(1, 112, 0), forer=limb(1, 0), arml=limb(-1, -20, 24), forel=limb(-1, 20)),
    'happy': P(_face='happy', _off=(0, 0.6, 0), armr=limb(1, 0, 95), forer=limb(1, 0, 60), arml=limb(-1, 0, 95), forel=limb(-1, 0, 60)),
    'wave_a': P(_face='happy', **dict(LOOSE, arml=limb(-1, 0, 100), forel=limb(-1, 0, 60), head=qs(('z', -6)))),
    'wave_b': P(_face='happy', **dict(LOOSE, arml=limb(-1, 0, 100), forel=limb(-1, 0, 20), head=qs(('z', -6)))),
    # sitting on the ground, legs out in front, leaning back on his hands
    'sit_a': P(body=qs(('x', -12)), legr=limb(1, 88, 4), shinr=limb(1, 0), legl=limb(-1, 88, 4), shinl=limb(-1, 0),
               armr=limb(1, -25, 6), forer=limb(1, 90), arml=limb(-1, -25, 6), forel=limb(-1, 90), head=qs(('z', 6))),
    # ...and hugging his knees
    'sit_b': P(_face='blink', body=qs(('x', 8)), legr=limb(1, 118, 6), shinr=limb(1, -128), legl=limb(-1, 118, 6), shinl=limb(-1, -128),
               armr=limb(1, 84, 10), forer=limb(1, 30, -20), arml=limb(-1, 84, 10), forel=limb(-1, 30, -20), head=qs(('x', 14), ('z', -4))),
    # (2.96c) riding Bender: astride his back, his legs straddling down either side of him (out, then straight down past his flanks),
    #  his hands forward on Bender's shoulders - the pencil still in his right
    'ride': P(_face='happy', body=qs(('x', -4)), head=qs(('z', 4)), legr=limb(1, 26, 70), shinr=limb(1, -16, -54), legl=limb(-1, 26, 70), shinl=limb(-1, -16, -54),
              armr=limb(1, 40, 30), forer=limb(1, 36), arml=limb(-1, 40, 30), forel=limb(-1, 36)),
    'hurt': P(_face='surprised', body=qs(('x', -10)), head=qs(('x', -10)), armr=limb(1, 20, 60), forer=limb(1, 0, 40), arml=limb(-1, 20, 60), forel=limb(-1, 0, 40)),
    'tired': P(_face='blink', _off=(0, -0.6, 0), body=qs(('x', 16), ('z', -6)), head=qs(('x', 22)), armr=limb(1, 0, 2), forer=limb(1, 4), arml=limb(-1, 0, 2), forel=limb(-1, 4)),
}
SWIM_FRAMES = 8
for _i in range(SWIM_FRAMES):                              # (a flat swimmer: a breaststroke, like a paper doll in a bath)
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(_off=(0, -6.0 + 0.4 * math.sin(2 * _p), 0), body=qs(('x', 70)), head=qs(('x', -50)),
                            armr=limb(1, 150 + 30 * math.sin(_p), 30 + 30 * math.cos(_p)), forer=limb(1, 20),
                            arml=limb(-1, 150 + 30 * math.sin(_p), 30 + 30 * math.cos(_p)), forel=limb(-1, 20),
                            legr=limb(1, 14 * math.sin(2 * _p)), legl=limb(-1, -14 * math.sin(2 * _p)), shinr=limb(1, -20), shinl=limb(-1, -20))


# every pose stands (or sits) on the floor: its lowest point - a foot, or his seat - put just on it (a run's airborne frames a little off it)
_ME = sys.modules[__name__]
_FEET = [('shinr', (2.3, 0.36)), ('shinl', (-2.3, 0.36)), ('legr', (1.5, 5.8)), ('legl', (-1.5, 5.8))]
_SEAT = [('body', (0, 11.0))]
_HANDS = [('forer', (3.1, 6.8)), ('forer', (4.24, 2.0)), ('forel', (-3.1, 6.8))]


def _ground(pose, refs, lift=0.0):
    pose = dict(pose); pose.pop('_off', None)
    low = min(point(_ME, pose, p, (x, y, 0.0))[1] * 16 for p, (x, y) in refs)
    pose['_off'] = (0.0, round(lift - low + 0.32, 3), 0.0)
    return pose


for _k in list(POSES):
    if _k.startswith('swim_') or _k == 'jump':
        continue
    _sit = _k.startswith('sit_')
    POSES[_k] = _ground(POSES[_k], _FEET + _SEAT + (_HANDS if _k in ('splash',) else []) if _sit or _k == 'splash' else _FEET,
                        lift=(0.8 if _k in ('run_1', 'run_3') else 0.25 if _k in ('walk_1', 'walk_3') else 0.0))
DRAFT = ['idle_a', 'idle_b', 'idle_c', 'walk_1', 'run_1', 'jump', 'swipe_up', 'swipe', 'fling', 'toss_up', 'toss', 'scribble_a', 'paint_a', 'splash', 'rainbow_a', 'rainbow_c',
         'happy', 'sit_a', 'sit_b', 'hurt', 'swim_2']

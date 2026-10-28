"""The Cursor (draft): it came out of the Glitched Cartridge - the pack's 8-bit side, where Emma, Leo and Cecil have their pixel
twins and MissingNo lurks in the static. It is the "player's hand" Mr. Capshun always suspected was there: the thing on the other
side of the screen that points, clicks and drags. Curious, eager, a little glitchy - it clicks things (chests, buttons, foes, you).

THE LOOK: a classic computer mouse pointer - the white arrow with a black outline and its little tail (the stem) - in crisp pixel
art: hard pixel edges, no smoothing, like a real 32 x 32 cursor sprite scaled up (a pixel is half a design unit). FLAT like a
sprite, but with a little thickness (two pixels deep): every row of solid pixels is a box, the sprite on its front, a plain back on
its back, its outline on its edges - a cursor you can walk round. A small pixel face on the arrow's broad part (two pixel eyes, a
tiny mouth, pink blush pixels), and a light grey bevel down its lower-right edges, as the old cursors had.
It HOVERS - it has no feet: about half a player tall, floating at a player's chest height (its tail end some 0.6 blocks up), and it
only comes down to the floor to sit or to faint.

ITS FORMS (_shape, a model per form, each with every face): 'arrow' (the default, with its tail), 'hand' (the pointing link hand -
it selects things), 'wait' (the hourglass - it loads; 'wait_turn' is the same hourglass mid-turn, its sand running), 'ibeam' (the
text cursor - it blinks, the face squeezed onto its bar) and 'move' (the four-way cross - a stretch).

THE RIG (rigkit): body (the root - the sprite, a model per form x face), tail (the arrow's stem, jointed where it leaves the arrow
so it can wag and trail; hidden in the other forms - it is thinner than the body, so its root stays inside it as it turns) and fx
(a root of its own, shown only when a pose asks: the click's burst of pixel dashes at its hotspot, or a dashed marching-ants
selection box being dragged out behind it - carried to the hotspot by its own shift, '_o_fx', worked out per pose below).
Design units: hovering, facing -z, its right is +x (the arrow's tip points up and to its right - on your left, facing it)."""
import math
import sys
from PIL import Image

from phase57_art import hexc
from rigkit import qs, el, point

PREFIX = 'cu_'
RIG_SCALE = 1.0
PX = 0.5                                  # (design units a pixel: the arrow, 29 pixels tall, is 14.5 - about half a player)
DEP, TDEP = 1.0, 0.8                      # (the sprite's depth - two pixels - and the tail's, a touch thinner: its root hides in the body)
HOVER = 17.5                              # (the sprite's middle: chest height - the arrow spans 0.6 to 1.5 blocks)
PIVOT = {'body': (0.0, HOVER, 0.0), 'tail': None, 'fx': None}        # (tail and fx filled in below, from the arrow's pixels)
PARENT = {'body': None, 'tail': 'body', 'fx': None}
PARTS = ('body', 'tail', 'fx')
PART_K = {}
FACES = ('happy', 'surprised', 'blink', 'determined', 'hurt', 'glitch')
SHAPES = ('arrow', 'hand', 'wait', 'ibeam', 'move')
FORMS = SHAPES + ('wait_turn',)           # (the models: every shape, and the hourglass mid-turn)
FX = ('click', 'drag', 'drag2')
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)

PAL = {'K': '#14141c', 'W': '#ffffff', 'G': '#c3c8d8', 'B': '#9a6630', 'b': '#6a4220', 'L': '#d8efff', 'l': '#a6cbe6',
       'S': '#f2c24a', 's': '#c8962a', 'P': '#ff9ec2', 'R': '#e8445e', 'C': '#30e6ff', 'M': '#ff38d8', 'Y': '#ffe23a', 'y': '#e09a10'}


def HIDDEN(p, pose):
    if p == 'tail':
        return pose.get('_shape', 'arrow') != 'arrow'
    if p == 'fx':
        return not pose.get('_fx')
    return False


def model_name(p, pose, suffix=''):
    if p == 'body':
        shape = pose.get('_shape', 'arrow')
        form = '' if shape == 'arrow' else f'_{shape}'
        face = f'_x{pose["_face"]}' if pose.get('_face') else ''
        return f'{PREFIX}body{form}{face}{suffix}'
    if p == 'fx':
        return f'{PREFIX}fx_{pose["_fx"]}{suffix}' if pose.get('_fx') else f'{PREFIX}fx{suffix}'
    return f'{PREFIX}{p}{suffix}'


# ---------------------------------------------------------------------------------------------------- the sprites (pixel grids)
def _inside(poly, x, y):
    n, c = len(poly), False
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c


def _raster(poly, w, h):
    return {(x, y) for y in range(h) for x in range(w) if _inside(poly, x + 0.5, y + 0.5)}


def _outline(mask, fill='W'):
    """{pixel: char}: the mask's edge pixels (any side open) the outline, the rest the fill - and a bevel: a fill pixel with the
    outline just right of it or just below it, grey"""
    g = {}
    for (x, y) in mask:
        edge = any((x + dx, y + dy) not in mask for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        g[(x, y)] = 'K' if edge else fill
    for (x, y), c in list(g.items()):
        if c == 'W' and (g.get((x + 1, y)) == 'K' or g.get((x, y + 1)) == 'K'):
            g[(x, y)] = 'G'
    return g


# the arrow: the classic pointer - its left edge straight down, its right edge at 45 degrees, the wing, the notch, the stem at 2:1
ARROW = [(0, 0), (18, 18), (10, 18), (14.5, 27), (10.5, 28.8), (6, 19.6), (0, 25.6)]
STEM = [(5.2, 19.9), (10.5, 17.4), (15.6, 27.4), (10.2, 29.8)]                 # (the stem's pixels - the tail part)
TAIL_JOINT = (8.0, 18.8)                                                       # (where the stem leaves the arrow, in pixels)


def _arrow():
    m = _raster(ARROW, 19, 29)
    return _outline(m), (19, 29)


def _hand():
    """the pointing hand (the link cursor): the index finger up, three fingers folded, the thumb out to the side"""
    m = set()
    for x0, top in ((6, 0), (9, 5), (12, 6), (15, 7)):                  # (the fingers: four pixels wide, rounded tops)
        for y in range(top, 13):
            for x in range(x0, x0 + 4):
                if y == top and x in (x0, x0 + 3):
                    continue
                m.add((x, y))
    thumb = {8: (2, 3), 9: (1, 4), 10: (1, 5), 11: (2, 6), 12: (2, 6), 13: (3, 6)}
    for y, (a, b) in thumb.items():
        m |= {(x, y) for x in range(a, b + 1)}
    palm = {12: (6, 18), 13: (3, 18), 14: (3, 18), 15: (4, 18), 16: (4, 17), 17: (5, 17), 18: (5, 16), 19: (5, 16), 20: (5, 16), 21: (5, 16)}
    for y, (a, b) in palm.items():
        m |= {(x, y) for x in range(a, b + 1)}
    g = _outline(m)
    for x in (9, 12, 15):                                               # (the folds between the fingers)
        for y in range(6, 11):
            if (x, y) in g:
                g[(x, y)] = 'K'
    for y in (9, 10):                                                   # (the thumb's crease)
        g[(5, y)] = 'K'
    for x in range(6, 16):                                              # (the cuff)
        g[(x, 19)] = 'K'
    for x in range(6, 16):
        g[(x, 20)] = 'G'
    return g, (19, 22)


def _hourglass(turn=False):
    """the hourglass (the wait cursor): a wooden bar top and bottom, the glass between - the sand in its top bulb, or (turn) running"""
    W_, H_ = 17, 28
    half = {3: 7, 4: 7, 5: 7, 6: 7, 7: 7, 8: 7, 9: 6, 10: 5, 11: 4, 12: 3, 13: 2}
    half.update({27 - y: v for y, v in half.items()})
    g = {}
    for y in list(range(0, 3)) + list(range(25, 28)):                   # (the bars)
        for x in range(W_):
            edge = y in (0, 27) or x in (0, W_ - 1) or y in (2, 25)
            g[(x, y)] = 'K' if edge else 'B'
    glass = {(x, y) for y, hw in half.items() for x in range(8 - hw, 9 + hw)}
    gl = _outline(glass, 'L')
    for k, c in gl.items():
        if c == 'G':
            gl[k] = 'l'
        if k[1] in (3, 24):
            gl[k] = 'K'
    g.update(gl)

    def sand(y0, y1):
        for (x, y), c in list(g.items()):
            if y0 <= y <= y1 and c in ('L', 'l'):
                g[(x, y)] = 'S' if (x + 2 * y) % 5 else 's'
    if turn:
        sand(13, 13); sand(20, 23)
        for y in range(14, 20):
            if g.get((8, y)) in ('L', 'l'):
                g[(8, y)] = 'S'
    else:
        sand(11, 13); sand(23, 23)
    return g, (W_, H_)


def _ibeam():
    """the text cursor: a bar with a flared serif at each end (a nick in the middle of each, as the real one has)"""
    m = {(x, y) for y in range(0, 3) for x in range(0, 15)} | {(x, y) for y in range(3, 23) for x in range(3, 12)} | \
        {(x, y) for y in range(23, 26) for x in range(0, 15)}
    m -= {(0, 0), (14, 0), (0, 25), (14, 25), (7, 0), (7, 25)}
    return _outline(m), (15, 26)


def _move():
    """the four-way cross: an arrowhead each way on a short neck, off a square hub (the face on the hub)"""
    m = {(x, y) for y in range(7, 18) for x in range(7, 18)}
    for r in range(6):                                                   # (the heads: one pixel at the tip, eleven at the base)
        for k in range(12 - r, 13 + r):
            m |= {(k, r), (k, 24 - r), (r, k), (24 - r, k)}
    for k in range(10, 15):                                              # (the necks)
        m |= {(k, 6), (k, 18), (6, k), (18, k)}
    return _outline(m), (25, 25)


# the faces: drawn on a 9 x 6 pixel grid (a 5 x 4 one on the I-beam's narrow bar). K ink, P blush, R tongue, C/M the glitch's colours
FACE_BIG = {
    None: ['.KK...KK.', '.KK...KK.', 'P.......P', '..K...K..', '...KKK...', '.........'],
    'happy': ['..K...K..', '.K.K.K.K.', 'P.......P', '..KKKKK..', '..KRRRK..', '...KKK...'],
    'surprised': ['.KK...KK.', '.KK...KK.', '.KK...KK.', '.........', '...KKK...', '...KKK...'],
    'blink': ['.........', '.KK...KK.', 'P.......P', '..K...K..', '...KKK...', '.........'],
    'determined': ['.K.....K.', '.KK...KK.', '.KK...KK.', '.........', '..KKKKK..', '.........'],
    'hurt': ['.K.K.K.K.', '..K...K..', '.K.K.K.K.', '.........', '..K.K.K..', '.K.K.K.K.'],
    'glitch': ['.KKM..KK.', '.KKM.CKK.', 'P...C...P', '..K....M.', '...KK.K..', '.M.......'],
}
FACE_SMALL = {
    None: ['K...K', 'K...K', '.....', '.KKK.'],
    'happy': ['.....', 'K...K', '.....', '.KKK.'],
    'surprised': ['K...K', 'K...K', '..K..', '..K..'],
    'blink': ['.....', 'K...K', '.....', '.KKK.'],
    'determined': ['K...K', 'K...K', '.....', 'KKKKK'],
    'hurt': ['K...K', '.K.K.', '.....', 'K.K.K'],
    'glitch': ['KM..K', 'K..CK', '.M...', '.KK.K'],
}
FACE_AT = {'arrow': (1, 11), 'hand': (6, 12), 'wait': (4, 5), 'wait_turn': (4, 5), 'ibeam': (5, 10), 'move': (8, 9)}
# (the hotspot - the pixel corner a cursor clicks with: the arrow's tip, the hand's fingertip)
HOT = {'arrow': (0.0, 0.0), 'hand': (8.0, 0.0), 'wait': (8.5, 14.0), 'wait_turn': (8.5, 14.0), 'ibeam': (7.5, 13.0), 'move': (12.5, 12.5)}
SPRITE = {'arrow': _arrow, 'hand': _hand, 'wait': _hourglass, 'wait_turn': lambda: _hourglass(True), 'ibeam': _ibeam, 'move': _move}


def _with_face(g, form, face):
    g = dict(g)
    pat = (FACE_SMALL if form == 'ibeam' else FACE_BIG)[face]
    fx, fy = FACE_AT[form]
    for j, row in enumerate(pat):
        for i, c in enumerate(row):
            k = (fx + i, fy + j)
            if c != '.' and k in g and g[k] != 'K':
                g[k] = c
    return g


# ---------------------------------------------------------------------------------------------------- textures
TN = 64                                   # (a sprite's texture: its front at the left, its back from column 32)


def _paint(front, back, size):
    im = Image.new('RGBA', (TN, TN), (0, 0, 0, 0)); px = im.load()
    for (x, y), c in front.items():
        px[x, y] = hexc(PAL[c])
    for (x, y), c in back.items():
        px[32 + x, y] = hexc(PAL[c])
    return im


def _sprite(form):
    g, size = SPRITE[form]()
    return g, size


def _fx_click():
    """the click: a burst of pixel dashes out of the hotspot - up, up-left and left (the arrow itself lies down and to the right)"""
    g = {}
    for i in range(3):
        for (dx, dy) in ((0, -1), (-1, -1), (-1, 0), (1, -1), (-1, 1)):
            r = 3 + i
            g[(8 + dx * r, 8 + dy * r)] = 'Y' if i < 2 else 'y'
    return g, (9, 9)


def _fx_drag(w, h):
    """a selection box being dragged out: its outline in marching ants (black and white, two pixels each)"""
    g = {}
    ring = [(x, 0) for x in range(w)] + [(w - 1, y) for y in range(1, h)] + [(x, h - 1) for x in range(w - 2, -1, -1)] + \
           [(0, y) for y in range(h - 2, 0, -1)]
    for i, k in enumerate(ring):
        g[k] = 'K' if (i // 2) % 2 == 0 else 'W'
    return g, (w, h)


FXS = {'click': _fx_click, 'drag': lambda: _fx_drag(14, 10), 'drag2': lambda: _fx_drag(24, 16)}


def textures():
    T = {}
    for form in FORMS:
        g, size = _sprite(form)
        back = {k: ('W' if c not in ('K', 'G', 'B', 'b', 'L', 'l', 'S', 's') else c) for k, c in g.items()}
        for face in (None,) + FACES:
            T[f'{PREFIX}{form}' + (f'_{face}' if face else '')] = _paint(_with_face(g, form, face), back, size)
    for k, fn in FXS.items():
        g, size = fn()
        T[f'{PREFIX}fx_{k}'] = _paint(g, g, size)
    return T


# ---------------------------------------------------------------------------------------------------- models
def _xy(form, px, py):
    """a pixel corner of a form's sprite -> design (x, y): the sprite's middle at (0, HOVER), its left (as you face it) at its right (+x)"""
    w, h = SPRITE_SIZE[form]
    return (w / 2 - px) * PX, HOVER + (h / 2 - py) * PX


def _voxel(g, size, tex, piv, xy, dep, keep=None, zc=0.0):
    """every row's runs of solid pixels a box (the sprite on its north face, its back on the south, its edge pixels round its sides)"""
    w, h = size; u = 16.0 / TN
    els = []
    for y in range(h):
        x = 0
        while x < w:
            if (x, y) not in g or (keep and not keep(x, y)):
                x += 1; continue
            x0 = x
            while x < w and (x, y) in g and (not keep or keep(x, y)):
                x += 1
            (ax, ay), (bx_, by) = xy(x, y + 1), xy(x0, y)
            v0, v1 = y * u, (y + 1) * u
            row = lambda c0, c1: [round(c0 * u, 4), v0, round(c1 * u, 4), v1]
            uv = {'north': row(x0, x), 'south': row(32 + x, 32 + x0), 'up': row(x0, x), 'down': row(x0, x),
                  'east': row(x0, x0 + 1), 'west': row(x - 1, x)}
            e = el((ax, ay, zc - dep / 2), (bx_, by, zc + dep / 2), 't', piv, uv=uv)
            e['shade'] = False                     # (a sprite: its white stays white, as on a screen - the edges are outline-black anyway)
            els.append(e)
    return els


SPRITE_SIZE = {f: SPRITE[f]()[1] for f in FORMS}
_tx, _ty = _xy('arrow', *TAIL_JOINT)
PIVOT['tail'] = (round(_tx, 3), round(_ty, 3), 0.0)
_hx, _hy = _xy('arrow', *HOT['arrow'])
PIVOT['fx'] = (round(_hx, 3), round(_hy, 3), -1.2)                     # (the hotspot at rest, a little in front of the sprite)
FX_AT = {'click': (8, 8), 'drag': (13, 9), 'drag2': (23, 15)}          # (the pixel of each fx that sits on the hotspot)
FX_Z = {'click': 0.0, 'drag': 2.0, 'drag2': 2.0}                       # (the selection box a little behind the cursor, the click in front)


def models():
    M = {}

    def part(name, tex, els):
        M[name] = ({'t': f'bm:block/{tex}'}, els)
    stem = lambda x, y: _inside(STEM, x + 0.5, y + 0.5)
    for form in FORMS:
        g, size = SPRITE[form]()
        xy = lambda px_, py_, f=form: _xy(f, px_, py_)
        keep = (lambda x, y: not stem(x, y)) if form == 'arrow' else None
        els = _voxel(g, size, None, PIVOT['body'], xy, DEP, keep)
        nm = '' if form == 'arrow' else f'_{form}'
        for face in (None,) + FACES:
            tex = f'{PREFIX}{form}' + (f'_{face}' if face else '')
            part(f'{PREFIX}body{nm}' + (f'_x{face}' if face else ''), tex, els)
        if form == 'arrow':
            part(f'{PREFIX}tail', f'{PREFIX}arrow', _voxel(g, size, None, PIVOT['tail'], lambda a, b: _xy('arrow', a, b), TDEP, stem))
    fp = PIVOT['fx']
    for k, fn in FXS.items():
        g, size = fn()
        ax, ay = FX_AT[k]

        def xy(px_, py_, ax=ax, ay=ay):
            return fp[0] + (ax - px_) * PX, fp[1] + (ay - py_) * PX
        els = _voxel(g, size, None, fp, xy, 0.4, zc=fp[2] + FX_Z[k])
        part(f'{PREFIX}fx_{k}', f'{PREFIX}fx_{k}', els)
    # (no fx: a speck of nothing at the hotspot)
    part(f'{PREFIX}fx', f'{PREFIX}fx_click', [el((fp[0] - 0.01, fp[1] - 0.01, fp[2] - 0.01), (fp[0] + 0.01, fp[1] + 0.01, fp[2] + 0.01), 't', fp,
                                                  faces=('north',), uv={'north': [0, 0, 0.25, 0.25]})])
    return M


# ---------------------------------------------------------------------------------------------------- poses
def tilt(pitch=0.0, roll=0.0, yaw=0.0):
    """pitch: its top tipped toward its front (the way it clicks); roll: turned in its own plane, its top toward its right (+x - the
    way its tip points); yaw: turned to look to its right"""
    return qs(('y', yaw), ('x', pitch), ('z', roll))


def wag(a):
    """the tail swung about its root, in the sprite's plane (+: out toward its right, the way the stem leans)"""
    return qs(('z', a))


def P(**kw):
    return kw


def bob(k, n=4, amp=0.6):
    return amp * math.sin(2 * math.pi * k / n)


POSES = {
    # hovering, a gentle list to one side - looking at you
    'idle_a': P(body=tilt(0, -4)),
    # glitching: a stutter sideways, the face scrambled for a moment
    'idle_b': P(_face='glitch', _off=(0.6, 0.3, 0), body=tilt(0, 6, -10), tail=wag(-8)),
    # a blinking text cursor - waiting for you to type something
    'idle_c': P(_shape='ibeam', _face='blink', body=tilt(0, 0)),
    # a stretch: it goes into the four-way cross, arms (well, arrows) out
    'idle_d': P(_shape='move', _face='happy', _off=(0, 0.6, 0), body=tilt(-6, 0)),
    # curious: it leans in to look at something, its tail up behind it
    'idle_e': P(_face='surprised', body=tilt(18, -8, 14), tail=wag(10)),
    # it glides along: a little bob, leaning into the way it goes, the tail swaying
    **{f'walk_{k}': P(_off=(0, bob(k, 4, 0.5), 0), body=tilt(10, -4 + 2 * math.sin(math.pi * k / 2)), tail=wag(6 * math.sin(math.pi * k / 2)))
       for k in range(4)},
    # ...and zips: leaning hard, the tail streaming out behind
    **{f'run_{k}': P(_face='determined', _off=(0, bob(k, 4, 0.7), 0.8), body=tilt(30, -8 + 3 * math.sin(math.pi * k / 2)),
                     tail=wag(-6 + 8 * math.sin(math.pi * k / 2))) for k in range(4)},
    'jump': P(_face='happy', _off=(0, 3.0, 0), body=tilt(-12, 6), tail=wag(-14)),
    # CLICK: it rears back - then dips its tip down onto the foe (and the click goes off at its tip)
    'click_up': P(_face='determined', _off=(0, 1.2, 1.0), body=tilt(-24, -6), tail=wag(-10)),
    'click': P(_face='determined', _fx='click', _off=(0, 1.0, -3.0), body=tilt(118, -4), tail=wag(12)),
    # DRAG: it grabs the foe and drags it - tilted, sliding across, a selection box stretched out behind its tip
    'drag_0': P(_face='happy', _fx='drag', _off=(-1.4, 0.2, 0), body=tilt(6, -18, -10), tail=wag(14)),
    'drag_1': P(_face='determined', _fx='drag2', _off=(2.2, -0.6, 0), body=tilt(10, -30, 12), tail=wag(20)),
    # SELECT: the pointing hand, its finger out at the foe - this one
    'select': P(_shape='hand', _face='determined', _fx='click', _off=(0, -0.8, -2.4), body=tilt(30, -8, -12)),
    # WAIT: the hourglass - it loads (turning over, the sand running)
    'wait_0': P(_shape='wait', _face='blink', body=tilt(0, 0)),
    'wait_1': P(_shape='wait_turn', _face='blink', _off=(0, 0.4, 0), body=tilt(0, -90)),
    'happy': P(_face='happy', _off=(0, 1.6, 0), body=tilt(-8, 10, -16), tail=wag(-16)),
    'wave_a': P(_shape='hand', _face='happy', body=tilt(0, 14)),
    'wave_b': P(_shape='hand', _face='happy', body=tilt(0, -14)),
    # sitting: it comes down to the floor and leans back on its tail, its tip in the air...
    'sit_a': P(_face='happy', body=tilt(-40, -6), tail=wag(-14)),
    # ...or lies over on its side, tail curled, half asleep
    'sit_b': P(_face='blink', body=tilt(-8, 62), tail=wag(-22)),
    'hurt': P(_face='hurt', _off=(0, 0.6, 1.4), body=tilt(-26, 14), tail=wag(-20)),
    # it faints: dropped flat on its back on the floor, X'd out
    'tired': P(_face='hurt', body=tilt(-90, 18), tail=wag(10)),
}
SWIM_FRAMES = 8
for _i in range(SWIM_FRAMES):                              # (it skims the water: low, leaning forward, rocking, the tail a rudder)
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(_face='determined' if _i % 4 else None, _off=(0, -6.0 + 0.5 * math.sin(_p), 0),
                            body=tilt(34 + 4 * math.sin(_p), -6 + 6 * math.sin(_p)), tail=wag(18 * math.sin(_p)))

# ---- after the poses: what touches the floor, and where the fx goes
_ME = sys.modules[__name__]
_MODELS = None


def _corners(part, pose):
    global _MODELS
    if _MODELS is None:
        _MODELS = models()
    pv = PIVOT[part]
    for e in _MODELS[model_name(part, pose)][1]:
        for x in (e['from'][0], e['to'][0]):
            for y in (e['from'][1], e['to'][1]):
                for z in (e['from'][2], e['to'][2]):
                    yield (x - 8 + pv[0], y - 8 + pv[1], z - 8 + pv[2])


def low(pose):
    """its lowest point in this pose (design units)"""
    return min(point(_ME, pose, p, c)[1] * 16 for p in ('body', 'tail') if not HIDDEN(p, pose) for c in _corners(p, pose))


def _ground(pose, lift=0.0):
    pose = dict(pose); off = pose.pop('_off', (0.0, 0.0, 0.0))
    pose['_off'] = (off[0], round(off[1] + lift - low(pose), 3), off[2])
    return pose


def hotspot(pose):
    """where its hotspot is in this pose (design units)"""
    shape = pose.get('_shape', 'arrow')
    hx, hy = _xy(shape, *HOT[shape])
    v = point(_ME, pose, 'body', (hx, hy, -DEP / 2))
    return (-v[0] * 16, v[1] * 16, -v[2] * 16)


for _k in ('sit_a', 'sit_b', 'tired'):                     # (down on the floor: its lowest pixel just on it)
    POSES[_k] = _ground(POSES[_k], 0.05)
for _k, _p in POSES.items():                               # (the fx carried to the hotspot)
    if _p.get('_fx'):
        h, off = hotspot(_p), _p.get('_off', (0.0, 0.0, 0.0))
        _p['_o_fx'] = tuple(round(h[i] - PIVOT['fx'][i] - off[i] + (-0.6 if i == 2 else 0.0), 3) for i in range(3))

DRAFT = ['idle_a', 'idle_b', 'idle_c', 'idle_d', 'idle_e', 'walk_1', 'run_1', 'jump', 'click_up', 'click', 'drag_0', 'drag_1', 'select',
         'wait_0', 'wait_1', 'happy', 'wave_a', 'sit_a', 'sit_b', 'hurt', 'tired', 'swim_2']

"""2.67: the followers' faces - an expression set for each, drawn over the same 36 x 32 face plate as their own faces.

EMMA (cheerful): blink, wink, happy (closed ^^ eyes, open smile), sad (raised inner brows, a tear, a frown), hurt (> < eyes,
  an "ow" mouth), serious (lowered lids, brows set, a small firm mouth) - in her own eyes and in her ethereal violet ones.
CELI (impatient, blunt): blink, tsk (eyes cut to the side, mouth twisted), huff (eyes shut, cheeks puffed, a pout), hurt
  (an angry squint, gritted teeth), serious (fierce: brows down hard, both fangs bared).
CECIL (dry, sarcastic): his eyes are their own glowing slits - blink, deadpan (half-lidded, flat), roll (the eyes rolled up),
  sly (one narrowed, one raised), hurt (squeezed > <), serious (narrow and steep).
2.67, everyone: surprised (wide eyes, brows up, a little "o" - startled when a monster first shows) and sleepy (heavy lids -
  sitting, at night).
LEO's are drawn with him (phase96_art)."""
import math, random
from PIL import Image, ImageDraw
from phase57_art import hexc

EMMA_EXPR = ('blink', 'wink', 'happy', 'sad', 'hurt', 'serious', 'surprised', 'sleepy', 'panic', 'angry')      # (2.94m: panic and angry - her Easter eggs)
CELI_EXPR = ('blink', 'tsk', 'huff', 'hurt', 'serious', 'surprised', 'sleepy')
CECIL_EXPR = ('blink', 'deadpan', 'roll', 'sly', 'hurt', 'serious', 'surprised', 'sleepy', 'blush')     # (2.94m: blush - Emma's hug)


# ===================================================================== EMMA
def emma_face(expr, eye_dark, eye_mid, eye_light, eye_glow, pupil):
    """phase57_art._face, with an expression (None = her own face, exactly as before)"""
    P = hexc
    im = Image.new('RGBA', (64, 64), P('#f7d7bf')); d = ImageDraw.Draw(im)
    for y in range(9):
        for x in range(36): im.putpixel((x, y), P('#efc4a6'))
    LASH = '#2a1610'
    def eye_open(cx, flip, lid=0):
        x0, y0 = cx - 5, 13
        d.ellipse((x0, y0, x0 + 10, y0 + 13), fill=P('#ffffff'))
        d.ellipse((x0 + 1, y0 + 1, x0 + 9, y0 + 13), fill=P(eye_dark))
        d.ellipse((x0 + 1, y0 + 5, x0 + 9, y0 + 13), fill=P(eye_mid))
        d.ellipse((x0 + 2, y0 + 8, x0 + 8, y0 + 13), fill=P(eye_light))
        d.ellipse((x0 + 3, y0 + 4, x0 + 7, y0 + 10), fill=P(pupil))
        hx = x0 + 2                                                                 # (the shines sit the same way in both eyes: one light)
        d.ellipse((hx, y0 + 2, hx + 3, y0 + 5), fill=P('#ffffff'))
        d.point((x0 + 6, y0 + 10), fill=P('#ffffff')); d.point((x0 + 7, y0 + 10), fill=P('#ffffff'))
        if lid:                                                                     # (serious: the upper lid comes down)
            d.rectangle((x0 - 1, y0 - 1, x0 + 11, y0 + lid), fill=P('#f7d7bf'))
            d.line((x0 - 1, y0 + lid, x0 + 11, y0 + lid), fill=P(LASH), width=2)
        else:
            d.arc((x0 - 1, y0 - 1, x0 + 11, y0 + 10), 195, 345, fill=P(LASH), width=2)
        ox = x0 + 10 if not flip else x0; sx = 1 if not flip else -1
        d.line((ox, y0 + 2 + lid, ox + 2 * sx, y0 + lid), fill=P(LASH), width=1); d.point((ox + sx, y0 + 4 + lid), fill=P(LASH))
        if eye_glow: d.point((cx, y0 + 11), fill=P(eye_glow))
    def eye_closed(cx, flip, happy=False):
        x0, y0 = cx - 5, 13
        if happy:                                                                    # ^ - a smiling closed eye
            d.arc((x0, y0 + 4, x0 + 10, y0 + 14), 200, 340, fill=P(LASH), width=2)
        else:                                                                        # a soft closed curve, lashes down
            d.arc((x0, y0 + 2, x0 + 10, y0 + 10), 20, 160, fill=P(LASH), width=2)
            for lx in (x0 + 2, x0 + 5, x0 + 8): d.point((lx, y0 + 10), fill=P(LASH))
        ox = x0 + 10 if not flip else x0; sx = 1 if not flip else -1
        d.line((ox, y0 + 6, ox + 2 * sx, y0 + 4), fill=P(LASH), width=1)
    def eye_wide(cx, flip):                                                          # (2.67) startled: round, the iris small in the white
        x0, y0 = cx - 5, 13
        d.ellipse((x0 - 1, y0 - 1, x0 + 11, y0 + 13), fill=P('#ffffff'))
        d.ellipse((x0 + 2, y0 + 3, x0 + 8, y0 + 11), fill=P(eye_dark))
        d.ellipse((x0 + 2, y0 + 6, x0 + 8, y0 + 11), fill=P(eye_mid))
        d.ellipse((x0 + 4, y0 + 5, x0 + 6, y0 + 8), fill=P(pupil))
        d.point((x0 + 3, y0 + 4), fill=P('#ffffff'))
        d.arc((x0 - 2, y0 - 2, x0 + 12, y0 + 10), 195, 345, fill=P(LASH), width=2)
        ox = x0 + 11 if not flip else x0 - 1; sx = 1 if not flip else -1
        d.line((ox, y0 + 1, ox + 2 * sx, y0 - 1), fill=P(LASH), width=1)
    def eye_hurt(cx, flip):                                                          # > <
        x0, y0 = cx - 5, 13; sx = 1 if not flip else -1
        a, b = (x0 + 2, x0 + 8) if not flip else (x0 + 8, x0 + 2)
        d.line((a, y0 + 3, b, y0 + 7), fill=P(LASH), width=2); d.line((b, y0 + 7, a, y0 + 11), fill=P(LASH), width=2)
    if expr in (None, 'sad', 'serious', 'sleepy'):
        lid = {'serious': 4, 'sleepy': 7}.get(expr, 0)                               # (sleepy: the lids heavy, half down)
        eye_open(9, False, lid); eye_open(27, True, lid)
    elif expr == 'surprised':
        eye_wide(9, False); eye_wide(27, True)
    elif expr == 'panic':                                                            # (2.94m) wide, swimming with tears
        eye_wide(9, False); eye_wide(27, True)
        for cx in (9, 27):
            d.ellipse((cx - 5, 22, cx - 2, 25), fill=P('#bfe6ff')); d.ellipse((cx + 2, 22, cx + 5, 25), fill=P('#bfe6ff'))
            im.putpixel((cx - 4, 23), P('#ffffff')); im.putpixel((cx + 3, 23), P('#ffffff'))
    elif expr == 'angry':                                                            # (2.94m) a glare: the lids down a little, the iris small
        eye_open(9, False, 3); eye_open(27, True, 3)
    elif expr == 'blink':
        eye_closed(9, False); eye_closed(27, True)
    elif expr == 'wink':
        eye_open(9, False); eye_closed(27, True, happy=True)
    elif expr == 'happy':
        eye_closed(9, False, happy=True); eye_closed(27, True, happy=True)
    elif expr == 'hurt':
        eye_hurt(9, False); eye_hurt(27, True)
    for cx in (8, 28):                                                               # blush and freckles (more of it when happy or hurt)
        r = 5 if expr in ('happy', 'wink', 'hurt', 'panic', 'angry') else 4
        d.ellipse((cx - r, 26, cx + r, 29), fill=P('#ee8c86' if expr == 'angry' else '#f6b4aa'))
        for fx, fy in ((-2, 27), (0, 28), (2, 27)): im.putpixel((cx + fx, fy), P('#c8705c'))
    MOUTH = '#8a3428'
    if expr in (None, 'blink'):
        for yy, row in enumerate(('m....m', '.mmmm.')):
            for xx, ch in enumerate(row):
                if ch == 'm': im.putpixel((15 + xx, 28 + yy), P(MOUTH))
    elif expr in ('happy', 'wink'):                                                  # an open smile, a little tongue
        d.chord((14, 26, 21, 31), 0, 180, fill=P(MOUTH)); d.chord((16, 29, 19, 31), 0, 180, fill=P('#f07a8a'))
    elif expr == 'sad':
        for yy, row in enumerate(('.mmmm.', 'm....m')):
            for xx, ch in enumerate(row):
                if ch == 'm': im.putpixel((15 + xx, 28 + yy), P(MOUTH))
        d.ellipse((4, 25, 6, 28), fill=P('#9ad8ff')); im.putpixel((5, 24), P('#9ad8ff'))   # a tear
    elif expr == 'hurt':
        d.ellipse((16, 27, 20, 31), fill=P(MOUTH)); d.ellipse((17, 29, 19, 31), fill=P('#5a1a14'))
    elif expr == 'serious':
        d.line((15, 29, 20, 29), fill=P(MOUTH))
    elif expr == 'surprised':                                                        # a little "o"
        d.ellipse((16, 27, 19, 31), fill=P(MOUTH)); d.ellipse((17, 28, 18, 30), fill=P('#5a1a14'))
    elif expr == 'sleepy':                                                           # soft, barely parted
        d.line((16, 29, 19, 29), fill=P(MOUTH)); im.putpixel((17, 30), P(MOUTH))
    elif expr == 'panic':                                                            # (2.94m) a wobbling wail, the tongue curled
        d.polygon([(13, 29), (15, 27), (17, 28), (19, 27), (21, 28), (23, 27), (23, 31), (13, 31)], fill=P('#4a1410'))
        d.ellipse((16, 29, 22, 32), fill=P('#c04a58'))
    elif expr == 'angry':                                                            # (2.94m) "Frik you!" - a shout
        d.ellipse((14, 26, 22, 32), fill=P('#4a1410')); d.chord((15, 29, 21, 33), 180, 360, fill=P('#c04a58'))
        d.line((15, 27, 21, 27), fill=P('#ffffff'))
    hair_c = [P('#74391a'), P('#8a4a1e'), P('#a0582a')]; rnd = random.Random(5)
    for x in range(36):
        edge = 6 + int(3 * math.sin(x / 3.2)) + (2 if x < 12 else 0) + rnd.choice((0, 0, 1))
        if 4 <= x <= 14 or 22 <= x <= 32: edge = min(edge, 8)
        for y in range(edge): im.putpixel((x, y), hair_c[(x // 3 + y // 4) % 3])
    BROW = '#6e3618'
    for cx, s in ((9, 1), (27, -1)):
        if expr == 'sad':                                                            # inner ends raised
            pts = ((-3, 11), (-2, 11), (-1, 10), (0, 10), (1, 9), (2, 9))
        elif expr in ('serious', 'hurt'):                                            # inner ends lowered, set
            pts = ((-3, 9), (-2, 9), (-1, 10), (0, 10), (1, 11), (2, 11))
        elif expr == 'surprised':                                                    # high arches
            pts = ((-3, 10), (-2, 9), (-1, 8), (0, 8), (1, 8), (2, 9))
        elif expr == 'sleepy':                                                       # slack, low
            pts = ((-3, 12), (-2, 11), (-1, 11), (0, 11), (1, 11), (2, 12))
        elif expr == 'panic':                                                        # (2.94m) inner ends high, worried
            pts = ((-3, 11), (-2, 11), (-1, 10), (0, 9), (1, 8), (2, 8))
        elif expr == 'angry':                                                        # (2.94m) a hard V, two rows thick
            pts = ((-3, 8), (-2, 8), (-1, 9), (0, 10), (1, 11), (2, 12), (-3, 9), (-2, 9), (-1, 10), (0, 11), (1, 12))
        else:
            pts = ((-3, 11), (-2, 10), (-1, 10), (0, 10), (1, 10), (2, 11))
        for dx, y in pts: im.putpixel((cx + dx * s, y), P(BROW))
    return im


EMMA_EYES = ('#155d6e', '#22a2b2', '#5ad8dc', None, '#0a2630')
EMMA_EYES_KW = ('#0a4a3a', '#1ec890', '#9affd0', '#eaffa0', '#04201a')


def emma_kw_face(expr):
    """(2.94m) her KillerWatt look: the same face, gone glassy green - green bangs and brows, a pale green skin, glowing eyes;
    her own mouth, every expression"""
    im = emma_face(expr, *EMMA_EYES_KW)
    P = hexc
    swap = {P('#f7d7bf'): P('#dcebc0'), P('#efc4a6'): P('#c6dca2'), P('#74391a'): P('#2e8a2a'), P('#8a4a1e'): P('#46b03a'),
            P('#a0582a'): P('#66d04a'), P('#6e3618'): P('#1a5418'), P('#f6b4aa'): P('#b4e08a'), P('#ee8c86'): P('#9ad86a'),
            P('#c8705c'): P('#5a9a3a')}
    px = im.load()
    for y in range(32):
        for x in range(36):
            if px[x, y] in swap: px[x, y] = swap[px[x, y]]
    return im
EMMA_EYES_ETH = ('#4a1a7a', '#8a3ad0', '#c48af0', '#f0d0ff', '#1a0630')


# ===================================================================== CELI
CELI_SKIN, CELI_SKIN_DK = '#8ec6e8', '#6aa6d0'


def celi_face(expr):
    """phase66_art._face with an expression (None = her own)"""
    P = hexc
    im = Image.new('RGBA', (64, 64), P(CELI_SKIN)); d = ImageDraw.Draw(im)
    LID = '#2a1a3a'
    def eye(cx, flip, look=0, squint=False):
        x0, y0 = cx - 5, 14
        d.ellipse((x0 - 1, y0 - 2, x0 + 11, y0 + 6), fill=P('#a888d8'))                 # violet eyeshadow
        if squint:
            d.chord((x0, y0 + 3, x0 + 10, y0 + 8), 0, 180, fill=P('#fff6c0'))
            d.chord((x0 + 3 + look, y0 + 4, x0 + 7 + look, y0 + 8), 0, 180, fill=P('#c88a10'))
        else:
            d.chord((x0, y0, x0 + 10, y0 + 10), 0, 180, fill=P('#fff6c0'))               # the lower half shows: heavy lids
            d.chord((x0 + 1 + look, y0 + 1, x0 + 9 + look, y0 + 9), 0, 180, fill=P('#f4c830'))
            d.chord((x0 + 3 + look, y0 + 2, x0 + 7 + look, y0 + 8), 0, 180, fill=P('#c88a10'))
        d.line((x0 - 1, y0 + 5, x0 + 11, y0 + 5), fill=P(LID), width=2)
        ox = x0 + 11 if not flip else x0 - 1; sx = 1 if not flip else -1
        d.line((ox, y0 + 5, ox + 2 * sx, y0 + 3), fill=P(LID), width=1)
        if not squint: d.point((cx + 2 + look, y0 + 7), fill=P('#ffffff'))
    def shut(cx, flip, down=True):
        x0, y0 = cx - 5, 14
        d.ellipse((x0 - 1, y0 - 2, x0 + 11, y0 + 6), fill=P('#a888d8'))
        if down: d.arc((x0, y0 + 1, x0 + 10, y0 + 9), 20, 160, fill=P(LID), width=2)
        else: d.line((x0, y0 + 5, x0 + 10, y0 + 5), fill=P(LID), width=2)
        ox = x0 + 11 if not flip else x0 - 1; sx = 1 if not flip else -1
        d.line((ox, y0 + 5, ox + 2 * sx, y0 + 4), fill=P(LID), width=1)
    def wide(cx, flip):                                                                   # (2.67) caught off guard: both lids up
        x0, y0 = cx - 5, 14
        d.ellipse((x0 - 1, y0 - 4, x0 + 11, y0 + 5), fill=P('#a888d8'))
        d.ellipse((x0, y0 - 2, x0 + 10, y0 + 9), fill=P('#fff6c0'))
        d.ellipse((x0 + 3, y0 + 1, x0 + 7, y0 + 6), fill=P('#f4c830')); d.ellipse((x0 + 4, y0 + 2, x0 + 6, y0 + 5), fill=P('#c88a10'))
        d.arc((x0 - 1, y0 - 3, x0 + 11, y0 + 8), 200, 340, fill=P(LID), width=2)
        d.point((x0 + 4, y0 + 2), fill=P('#ffffff'))
    if expr in (None, 'serious'):
        eye(9, False); eye(27, True)
    elif expr == 'surprised':
        wide(9, False); wide(27, True)
    elif expr == 'sleepy':                                                                # the heavy lids heavier still
        for cx, fl in ((9, False), (27, True)):
            eye(cx, fl); x0, y0 = cx - 5, 14
            d.rectangle((x0 - 1, y0 + 4, x0 + 11, y0 + 6), fill=P('#a888d8')); d.line((x0, y0 + 7, x0 + 10, y0 + 7), fill=P(LID), width=1)
    elif expr == 'tsk':
        eye(9, False, look=2); eye(27, True, look=2)
    elif expr == 'blink':
        shut(9, False, down=False); shut(27, True, down=False)
    elif expr == 'huff':
        shut(9, False); shut(27, True)
    elif expr == 'hurt':
        eye(9, False, squint=True); eye(27, True, squint=True)
    BROW = '#d06a20'
    for cx, s in ((9, 1), (27, -1)):
        if expr in ('serious', 'hurt'):
            pts = ((-4, 9), (-3, 9), (-2, 10), (-1, 10), (0, 11), (1, 11), (2, 12))       # down hard toward the nose
        elif expr == 'surprised':
            pts = ((-4, 9), (-3, 8), (-2, 8), (-1, 7), (0, 7), (1, 8), (2, 8))
        elif expr == 'tsk':
            pts = ((-4, 10), (-3, 10), (-2, 10), (-1, 10), (0, 10), (1, 10), (2, 10)) if s > 0 else ((-4, 11), (-3, 10), (-2, 10), (-1, 9), (0, 9), (1, 9), (2, 10))
        else:
            pts = ((-4, 11), (-3, 10), (-2, 10), (-1, 10), (0, 10), (1, 10), (2, 11))
        for dx, y in pts: im.putpixel((cx + dx * s, y), P(BROW))
    for cx in (7, 29):                                                                     # blush (puffed when she huffs)
        r = 5 if expr == 'huff' else 4
        d.ellipse((cx - r, 24 - (1 if expr == 'huff' else 0), cx + r, 27), fill=P('#b49ae0'))
        for fx in (-2, 0, 2): im.putpixel((cx + fx, 25), P('#d88ac8'))
    M = '#3a2a5a'
    if expr in (None, 'blink'):
        d.line((16, 28, 20, 28), fill=P(M), width=1); d.point((15, 29), fill=P(M)); d.point((21, 29), fill=P(M))
        d.polygon([(19, 28), (20, 28), (19.5, 30)], fill=P('#ffffff'))
    elif expr == 'tsk':
        d.line((15, 29, 21, 27), fill=P(M), width=1); d.polygon([(19, 28), (20, 27.6), (19.6, 29.6)], fill=P('#ffffff'))
    elif expr == 'huff':
        d.ellipse((17, 27, 20, 30), fill=P(M)); d.ellipse((18, 28, 19, 29), fill=P('#5a3a7a'))
    elif expr == 'hurt':
        d.rectangle((15, 27, 21, 30), fill=P(M)); d.rectangle((16, 28, 20, 29), fill=P('#ffffff'))
        for x in (17, 19): d.line((x, 28, x, 29), fill=P('#9a8aaa'))
    elif expr == 'surprised':
        d.ellipse((17, 27, 20, 30), fill=P(M)); d.ellipse((18, 28, 19, 29), fill=P('#5a3a7a'))
    elif expr == 'sleepy':
        d.line((17, 28, 20, 28), fill=P(M)); d.polygon([(19, 28), (20, 28), (19.5, 29.5)], fill=P('#ffffff'))
    elif expr == 'serious':
        d.line((15, 27, 21, 27), fill=P(M)); d.line((15, 27, 15, 29), fill=P(M)); d.line((21, 27, 21, 29), fill=P(M))
        for fx in (16, 20): d.polygon([(fx, 28), (fx + 1, 28), (fx + 0.5, 30)], fill=P('#ffffff'))
    d.line((18, 21, 18, 24), fill=P(CELI_SKIN_DK)); d.point((19, 24), fill=P(CELI_SKIN_DK))   # nose
    return im


# ===================================================================== CECIL's glowing eyes, reshaped
def cecil_eyes(base_els, expr):
    """from the built cec2_eyes elements (two slanted slits, ±22.5 degrees): a new pair for an expression"""
    import copy
    out = []
    for i, e0 in enumerate(base_els):
        e = copy.deepcopy(e0)
        (x0, y0, z0), (x1, y1, z1) = e['from'], e['to']
        cy = (y0 + y1) / 2; h = y1 - y0
        ang = e['rotation']['angle'] if 'rotation' in e else 0.0
        side = 1 if ang < 0 else -1                                   # (which eye)
        def setv(hk=1.0, dy=0.0, a=None, wk=1.0, dx=0.0):
            cx = (x0 + x1) / 2 + dx; w = (x1 - x0) * wk
            nh = max(0.18, h * hk)
            e['from'] = [round(cx - w / 2, 4), round(cy + dy - nh / 2, 4), z0]; e['to'] = [round(cx + w / 2, 4), round(cy + dy + nh / 2, 4), z1]
            if 'rotation' in e:
                o = e['rotation']['origin']
                e['rotation'] = dict(e['rotation'], angle=ang if a is None else a, origin=[round(o[0] + dx, 4), round(o[1] + dy, 4), o[2]])
        if expr == 'blink': setv(0.2)
        elif expr == 'deadpan': setv(0.5, -0.12, 8.0 * (-1 if ang < 0 else 1))
        elif expr == 'roll': setv(0.55, 0.45, 0.0, 0.8)
        elif expr == 'sly': setv(0.45 if side > 0 else 0.95, -0.1 if side > 0 else 0.25, ang * (0.5 if side > 0 else 1.4))
        elif expr == 'serious': setv(0.6, -0.05, ang * 1.4 if abs(ang * 1.4) <= 45 else ang)
        elif expr == 'surprised': setv(1.45, 0.12, ang * 0.4, 0.9)                 # (2.67) wide, the slant all but gone
        elif expr == 'sleepy': setv(0.28, -0.22, ang * 0.3)                         # a drowsy sliver
        elif expr == 'blush':                                         # (2.94m) put out - but secretly pleased: narrowed, glancing
            setv(0.55, -0.08, ang * 0.5, 0.9, 0.45)                     # aside, and a pink squiggle on each cheek (texture z)
            out.append(e)
            cx = (x0 + x1) / 2; zf = round(z0 - 0.04, 4)
            for k in range(3):
                sx = cx - 0.6 + 0.6 * k; sy = cy - h * 1.35
                out.append({'from': [round(sx - 0.38, 4), round(sy - 0.11, 4), zf], 'to': [round(sx + 0.38, 4), round(sy + 0.11, 4), round(zf + 0.08, 4)],
                            'faces': {f: {'uv': [0, 0, 4, 4], 'texture': '#z'} for f in ('north', 'south', 'east', 'west', 'up', 'down')},
                            'rotation': {'axis': 'z', 'angle': 45.0 if k % 2 else -45.0, 'origin': [round(sx, 4), round(sy, 4), zf]}})
            continue
        elif expr == 'hurt':                                          # > < : each eye two short strokes
            cx = (x0 + x1) / 2; w = (x1 - x0); L = w * 0.62
            dy = L / 2 * math.sin(math.radians(30))                 # (the two strokes meet at the inner end: a chevron)
            a = copy.deepcopy(e); b = copy.deepcopy(e)
            for k, (yy, an) in enumerate(((cy + dy, 30.0), (cy - dy, -30.0))):
                p = (a, b)[k]
                p['from'] = [round(cx - L / 2, 4), round(yy - 0.12, 4), z0]; p['to'] = [round(cx + L / 2, 4), round(yy + 0.12, 4), z1]
                p['rotation'] = {'axis': 'z', 'angle': -an * side, 'origin': [round(cx, 4), round(yy, 4), z0]}
            out += [a, b]; continue
        out.append(e)
    return out

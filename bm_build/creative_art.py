"""2.96a: THE CREATIVE FORMS' OUTFITS - the art (creative.py wears them). One outfit for each, made for who they are:

  FISHY      Rainbow Fin        a betta's tail flowing out behind his tank, fins sweeping up off his shoulders
  BATTY      Prism Wings        his own wings turned to stained glass (their bones the lead), a prism on a gold chain
  EGGBERT    Golden Yolk        a Faberge egg: his shell in ruby enamel, a gold lattice, pearls, his spots set sapphires; a jewelled finial
  THE COUNT  Starlit Gentleman  a midnight opera cape strewn with stars, red satin within, its collar high; a starlit band on his topper
  CAPSHUN    Full Colour        drawn like he is - flat, in thick ink lines, coloured in: a beret, a neckerchief
  KETTLE     First Sketch       drawn like he is - in crayon: a paper crown, a scribbled hero's cape
  SKY        Aurora             pixel art like they are: the aurora's ribbons behind them, little twinkling stars about the moon
  EMMA       Dream Petals       a crown of flowers in her hair, fairy wings of great pink petals on her back
  AVA        Living Tide        a train of living water from her shoulders, pooling behind her; a necklace of shells and pearls
  DEMOCRATUS Painted Reaper     a garland of marigolds round his shoulders, marigolds tucked in his hood
  KILLERWATT Rainbow Current    his lightning running through every colour, rainbow current crackling down his arms
  PEARL      Pearlescent        two strands of pearls at her collar; a pearlescent overskirt in three tiers, pearls along each hem

Some restyle a part's own texture (RETEX - drawn from it: DERIVE). A piece is a box in WORLD units on the follower as they stand in their figure (facing +z): dict(c=centre, h=half extents, tex,
R=orientation, sprite=only its two broad faces (a flat drawing), glow=light). design(w, B) -> [(part, [pieces], host)] - B: every
part's world bounds."""
import colorsys
import math
import random

import numpy as np
from PIL import Image, ImageDraw


# ---------------------------------------------------------------------------------------------------- textures
def _hex(c):
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


def _hsv(h, s, v, a=255):
    r, g, b = colorsys.hsv_to_rgb(h % 1, s, v)
    return int(r * 255), int(g * 255), int(b * 255), a


def _fin():
    """a betta's fin: a fan from its root (top middle), rays running out, magenta at the root through violet to teal, a pale ruffled hem"""
    S = 32; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); px = im.load()
    for y in range(S):
        for x in range(S):
            dx, dy = (x + 0.5 - S / 2) / (S / 2), (y + 0.5) / S
            r = math.hypot(dx, dy); a = math.atan2(dx, dy)
            edge = 1.0 - 0.06 * (1 + math.sin(a * 14))
            if r > edge or abs(a) > 1.05: continue
            ray = abs(math.sin(a * 9)) < 0.18
            v = 0.95 if ray else 0.8
            px[x, y] = _hsv(0.88 - 0.42 * r, 0.65 - (0.35 if r > edge - 0.12 else 0), v)
    return im


def _crest():
    S = 32; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); px = im.load()
    for y in range(S):
        for x in range(S):
            u, v = (x + 0.5) / S, 1 - (y + 0.5) / S              # (a sail: tall at the front, sweeping back)
            top = 0.95 * (1 - u) ** 0.6 * (0.9 + 0.1 * math.sin(u * 30))
            if v > top: continue
            ray = (int(u * 10) % 2 == 0) and v < top - 0.06
            px[x, y] = _hsv(0.86 - 0.4 * v, 0.6, 0.95 if ray else 0.8)
    return im


def _glass(mirror):
    """a bat wing in stained glass: its scalloped trailing edge, the panes between its fingers each a colour, leaded in black"""
    S = 32; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); px = im.load()
    rnd = random.Random(77)
    hue = {}
    for y in range(S):
        for x in range(S):
            u, v = (x + 0.5) / S, (y + 0.5) / S                   # (u from the body out, v top down)
            scallop = 0.62 + 0.28 * u + 0.08 * abs(math.sin(u * math.pi * 3.5))
            if v > scallop or v < 0.12 * (1 - u): continue
            cell = (int(u * 3.5), int(v * 4 + u * 2))
            if cell not in hue: hue[cell] = rnd.random()
            lead = (abs((u * 3.5) % 1) < 0.1) or (abs((v * 4 + u * 2) % 1) < 0.1) or v > scallop - 0.04
            px[x, y] = (20, 16, 24, 255) if lead else _hsv(hue[cell], 0.7, 0.95)
    return im.transpose(Image.FLIP_LEFT_RIGHT) if mirror else im


def _prism():
    S = 16; im = Image.new('RGBA', (S, S)); px = im.load()
    for y in range(S):
        for x in range(S):
            px[x, y] = _hsv((x + y) / 24, 0.45, 1.0 if (x + y) % 5 else 0.8)
    return im


def _solid(col, shade=0.0, seed=0):
    rnd = random.Random(seed)
    im = Image.new('RGBA', (16, 16)); px = im.load()
    for y in range(16):
        for x in range(16):
            k = 1 - shade * rnd.random()
            px[x, y] = tuple(int(v * k) for v in _hex(col)) + (255,)
    return im


def _gold():
    """Faberge filigree: gold, curls scratched in, a jewel every few pixels"""
    im = Image.new('RGBA', (16, 16), (214, 166, 52, 255)); d = ImageDraw.Draw(im)
    for x in range(0, 16, 4):
        d.arc((x - 2, 3, x + 4, 12), 200, 340, fill=(250, 220, 120, 255))
        d.arc((x, 4, x + 6, 13), 20, 160, fill=(150, 104, 24, 255))
    d.line((0, 0, 15, 0), fill=(150, 104, 24, 255)); d.line((0, 15, 15, 15), fill=(150, 104, 24, 255))
    for i, (x, col) in enumerate(((3, '#d02040'), (8, '#2a6ae0'), (13, '#20b060'))):
        d.rectangle((x - 1, 7, x, 8), fill=_hex(col) + (255,)); d.point((x - 1, 7), fill=(255, 255, 255, 255))
    return im


def _ruby():
    im = Image.new('RGBA', (16, 16), (170, 16, 40, 255)); d = ImageDraw.Draw(im)
    d.polygon([(8, 1), (15, 8), (8, 15), (1, 8)], fill=(220, 40, 70, 255)); d.polygon([(8, 4), (11, 8), (8, 11), (5, 8)], fill=(255, 120, 140, 255))
    return im


def _starcape(seed=5):
    rnd = random.Random(seed)
    im = Image.new('RGBA', (16, 16)); px = im.load()
    for y in range(16):
        for x in range(16):
            k = 0.85 + 0.15 * math.sin((x + y * 0.3) * 0.7)
            px[x, y] = (int(18 * k), int(22 * k), int(64 * k), 255)
    for _ in range(9):
        x, y = rnd.randrange(16), rnd.randrange(16)
        px[x, y] = (230, 236, 255, 255)
        if rnd.random() < 0.4:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if 0 <= x + dx < 16 and 0 <= y + dy < 16: px[x + dx, y + dy] = (150, 160, 220, 255)
    return im


def _starband():
    im = Image.new('RGBA', (16, 16), (196, 204, 222, 255)); d = ImageDraw.Draw(im)
    d.line((0, 1, 15, 1), fill=(120, 128, 150, 255)); d.line((0, 14, 15, 14), fill=(120, 128, 150, 255))
    for x in (3, 11):
        d.point([(x, 6), (x, 7), (x, 8), (x, 9), (x - 1, 7), (x + 1, 7), (x - 1, 8), (x + 1, 8), (x - 2, 7), (x + 2, 8)], fill=(40, 46, 110, 255))
    return im


INK = (24, 24, 24, 255)


def _drawn_beret():
    """Capshun's beret as he'd draw it: thick ink outline, flat red fill, a white glint, a little stalk - a drawing, not a hat"""
    S = 32; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((2, 10, 29, 25), fill=(214, 46, 52, 255), outline=INK, width=2)
    d.ellipse((5, 20, 27, 27), fill=(170, 30, 40, 255), outline=INK, width=2)       # (its band)
    d.line((15, 10, 16, 5), fill=INK, width=2)
    d.arc((7, 13, 16, 20), 190, 280, fill=(255, 255, 255, 255), width=2)
    return im


def _drawn_kerchief():
    S = 32; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(3, 6), (29, 6), (16, 28)], fill=(52, 120, 220, 255), outline=INK)
    d.line([(3, 6), (29, 6), (16, 28), (3, 6)], fill=INK, width=2)
    for x, y in ((10, 11), (19, 11), (15, 18), (22, 9)):
        d.ellipse((x - 1, y - 1, x + 1, y + 1), fill=(255, 255, 255, 255))
    d.ellipse((12, 4, 20, 10), fill=(52, 120, 220, 255), outline=INK, width=2)          # (its knot)
    return im


def _crayon_line(d, pts, col, rnd, w=2):
    """a crayon stroke: a little wobble, a little gap here and there"""
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(2, int(math.hypot(x1 - x0, y1 - y0)))
        for i in range(n):
            if rnd.random() < 0.08: continue
            t = i / n
            x, y = x0 + (x1 - x0) * t + rnd.uniform(-0.5, 0.5), y0 + (y1 - y0) * t + rnd.uniform(-0.5, 0.5)
            if w == 1: d.point((x, y), fill=col)
            else: d.rectangle((x, y, x + w - 1, y + w - 1), fill=col)


def _paper_crown():
    """Kettle's paper crown, drawn in crayon: yellow paper, a zigzag top, crayon jewels"""
    rnd = random.Random(31)
    S = 32; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    top = [(2, 10), (7, 3), (11, 11), (16, 2), (21, 11), (25, 3), (30, 10)]
    d.polygon(top + [(30, 26), (2, 26)], fill=(255, 220, 70, 255))
    for y in range(12, 26, 3):                                   # (crayon fill: strokes, not a flat colour)
        _crayon_line(d, [(3, y), (29, y + 1)], (240, 196, 40, 255), rnd, 1)
    _crayon_line(d, top + [(30, 26), (2, 26), (2, 10)], (210, 120, 20, 255), rnd)
    for x, col in ((8, (230, 40, 50, 255)), (16, (40, 110, 230, 255)), (24, (40, 180, 70, 255))):
        d.ellipse((x - 3, 16, x + 3, 22), fill=col)
    return im


def _scribble_cape():
    """a hero's cape scribbled in red crayon: wide at the hem, a jagged bottom"""
    rnd = random.Random(12)
    S = 32; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    shape = [(10, 1), (22, 1), (30, 26), (26, 30), (21, 27), (16, 31), (11, 27), (6, 30), (2, 26)]
    d.polygon(shape, fill=(226, 60, 60, 255))
    for i in range(30):                                          # (scribbled in - strokes on the slant)
        y = rnd.uniform(2, 28); x = rnd.uniform(4, 22)
        _crayon_line(d, [(x, y), (x + rnd.uniform(4, 9), y + rnd.uniform(1, 3))], (190, 30, 40, 255), rnd, 1)
    _crayon_line(d, shape + [shape[0]], (120, 16, 24, 255), rnd)
    return Image.composite(im, Image.new('RGBA', (S, S), (0, 0, 0, 0)), _mask(shape, S))


def _mask(poly, S):
    m = Image.new('L', (S, S), 0); ImageDraw.Draw(m).polygon(poly, fill=255); return m


def _aurora():
    """the aurora, pixel art: three ribbons of light rippling across, green into teal into violet, a clear sky between"""
    S = 32; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); px = im.load()
    for x in range(S):
        for k, (base, hue) in enumerate(((7, 0.36), (16, 0.48), (25, 0.78))):
            yc = base + 3 * math.sin(x / S * 2 * math.pi * 1.5 + k * 1.7)
            for y in range(int(yc - 3), int(yc + 3)):
                if 0 <= y < S:
                    f = 1 - abs(y - yc) / 3
                    px[x, y] = _hsv(hue + 0.05 * f, 0.55 + 0.3 * (1 - f), 0.7 + 0.3 * f)
    return im


def _twinkle():
    S = 16; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.line((8, 1, 8, 14), fill=(255, 250, 200, 255)); d.line((1, 8, 14, 8), fill=(255, 250, 200, 255))
    d.rectangle((6, 6, 9, 9), fill=(255, 255, 255, 255)); d.point([(5, 5), (10, 5), (5, 10), (10, 10)], fill=(255, 230, 140, 255))
    return im


def _flower(petal, centre='#f8d030'):
    im = Image.new('RGBA', (16, 16), _hex('#4a9a3a') + (255,)); d = ImageDraw.Draw(im)
    for a in range(5):
        ang = a * 2 * math.pi / 5
        x, y = 8 + 4.5 * math.cos(ang), 8 + 4.5 * math.sin(ang)
        d.ellipse((x - 3.5, y - 3.5, x + 3.5, y + 3.5), fill=_hex(petal) + (255,))
    d.ellipse((5, 5, 10, 10), fill=_hex(centre) + (255,))
    return im


def _petals():
    """layered petals, pale pink, each row's scalloped edge over the next"""
    S = 32; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for row in range(4):
        y = row * 8
        for i in range(-1, 5):
            x = i * 8 + (4 if row % 2 else 0)
            col = (255, 196 - row * 10, 222 - row * 6, 255)
            d.ellipse((x, y - 2, x + 9, y + 9), fill=col, outline=(230, 140, 180, 255))
    return im


def _wave():
    """living water: deep blue rising to light, white foam curling along each crest"""
    S = 32; im = Image.new('RGBA', (S, S)); px = im.load()
    for y in range(S):
        for x in range(S):
            crest = (y + 3 * math.sin(x / 5.0)) % 10
            v = 0.55 + 0.4 * (crest / 10)
            px[x, y] = (236, 248, 255, 255) if crest > 8.6 else _hsv(0.55 - 0.03 * (crest / 10), 0.75 - 0.3 * (crest / 10), v)
    return im


def _shell():
    im = Image.new('RGBA', (16, 16), (250, 210, 180, 255)); d = ImageDraw.Draw(im)
    for x in range(1, 16, 3): d.line((8, 15, x, 1), fill=(230, 150, 120, 255))
    return im


def _pearl(tint=(246, 240, 236)):
    im = Image.new('RGBA', (16, 16), tint + (255,)); d = ImageDraw.Draw(im)
    d.ellipse((2, 2, 9, 9), fill=(255, 255, 255, 255)); d.rectangle((10, 10, 15, 15), fill=tuple(int(v * 0.86) for v in tint) + (255,))
    d.point((4, 4), fill=(255, 230, 245, 255))
    return im


def _marigold(col):
    im = Image.new('RGBA', (16, 16), _hex(col) + (255,)); d = ImageDraw.Draw(im)
    dk = tuple(int(v * 0.75) for v in _hex(col)) + (255,)
    for r in (7, 5, 3):
        for a in range(0, 360, 40):
            x, y = 8 + r * math.cos(math.radians(a + r * 10)), 8 + r * math.sin(math.radians(a + r * 10))
            d.point((x, y), fill=dk)
    return im


def _neon(col):
    im = Image.new('RGBA', (16, 16), _hex(col) + (255,)); d = ImageDraw.Draw(im)
    d.rectangle((0, 6, 15, 9), fill=tuple(min(255, v + 110) for v in _hex(col)) + (255,))
    return im


def _pearlshawl():
    """pearlescent: soft white shot through with pink, lilac and sea-blue, the way a pearl catches light"""
    S = 32; im = Image.new('RGBA', (S, S)); px = im.load()
    for y in range(S):
        for x in range(S):
            h = 0.85 + 0.25 * math.sin((x * 0.25 + y * 0.18)) + 0.1 * math.sin(y * 0.5)
            px[x, y] = _hsv(h, 0.16 + 0.06 * math.sin(x * 0.4), 0.96)
    return im



# ---------------------------------------------------------------------------------------------------- restyled from their own textures
def _lum(p):
    return (0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) / 255


def stained_glass(im):
    """Batty's wing membrane as stained glass: its finger bones become the lead, the membrane between them panes of jewel colour,
    cut again by arcs of lead; its scalloped edge kept"""
    W, H = im.size; px = im.load(); out = im.copy(); po = out.load()
    rootx, rooty = W * 0.47, H * 0.08
    for y in range(H):
        for x in range(W):
            p = px[x, y]
            if p[3] == 0: continue
            if _lum(p) < 0.22 or y < H * 0.08:                    # (a bone, or the arm along the top: lead)
                po[x, y] = (22, 18, 30, 255); continue
            a = math.atan2(x - rootx, y - rooty); r = math.hypot(x - rootx, y - rooty)
            sector = int((a + 1.6) / 0.42); band = int(r / (H * 0.22))
            if abs((r / (H * 0.22)) % 1) < 0.07:
                po[x, y] = (22, 18, 30, 255); continue
            hue = [0.0, 0.58, 0.13, 0.78, 0.33, 0.9, 0.5, 0.07][(sector + band * 3) % 8]
            v = 0.72 + 0.28 * _lum(p)
            po[x, y] = _hsv(hue, 0.72, min(1, v + (0.12 if (x + y) % 9 == 0 else 0)))
    return out


def faberge(im):
    """Eggbert's shell as a Faberge egg: ruby guilloche enamel (its sunburst engraving showing through), a gold lattice, a pearl
    where the lattice crosses, and each of his spots a sapphire set in gold"""
    W, H = im.size; px = im.load(); out = im.copy(); po = out.load()
    g = max(8, W // 4)
    for y in range(H):
        for x in range(W):
            p = px[x, y]
            if p[3] == 0: continue
            L = _lum(p)
            u, v = (x + y) % g, (x - y) % g
            if u in (0, 1) or v in (0, 1):
                po[x, y] = (232, 186, 70, 255) if (x + y) % 3 else (255, 226, 130, 255); continue
            if (x + y) % g in (2,) and (x - y) % g in (2,):
                po[x, y] = (250, 246, 240, 255); continue
            if L > 0.8:                                           # (his shine)
                po[x, y] = (255, 236, 236, 255); continue
            if L < 0.45:                                          # (a spot: a sapphire)
                edge = any(0 <= x + dx < W and 0 <= y + dy < H and _lum(px[x + dx, y + dy]) >= 0.45 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                po[x, y] = (232, 186, 70, 255) if edge else _hsv(0.62, 0.8, 0.55 + 0.35 * ((x * 3 + y) % 5) / 4)
                continue
            ring = math.hypot(x - W / 2, y - H / 2) % 3
            po[x, y] = _hsv(0.98, 0.82, 0.55 + 0.1 * ring)
    return out


def rainbow_current(im):
    """KillerWatt's lightning running through every colour: the hue travels along it, his own light and shade kept"""
    W, H = im.size; px = im.load(); out = im.copy(); po = out.load()
    for y in range(H):
        for x in range(W):
            p = px[x, y]
            if p[3] == 0: continue
            L = _lum(p)
            po[x, y] = _hsv((x + y) / (W + H) * 1.6, 0.75 - 0.4 * max(0, L - 0.7), 0.55 + 0.45 * L)
    return out


DERIVE = {'cf_gb_wing': ('gb_wing', stained_glass), 'cf_kw_bolt': ('kw_gold', rainbow_current)}
DERIVE.update({f'cf_{k}': (k, faberge) for k in ('ge_shell', 'ge_shell_b', 'ge_shell_hi', 'ge_shell_lo')})
# follower -> {part model: {its texture key: the restyled texture}} - their twins wear it
RETEX = {'batty': {'gb_wingr': {'gb_wing': 'cf_gb_wing'}, 'gb_wingl': {'gb_wing': 'cf_gb_wing'}},
         'eggbert': {'ge_body': {k: f'cf_{k}' for k in ('ge_shell', 'ge_shell_b', 'ge_shell_hi', 'ge_shell_lo')}},
         'kw': {'kw_tend': {'kw_gold': 'cf_kw_bolt'}, 'kw_tendl': {'kw_gold': 'cf_kw_bolt'}}}


def _cape_shape(lining):
    """the Count's opera cape: narrow at the shoulders, sweeping wide to a pointed hem - midnight and stars outside, red satin within"""
    S = 32
    shape = [(9, 0), (23, 0), (31, 27), (24, 31), (16, 28), (8, 31), (0, 27)]
    if lining:
        im = Image.new('RGBA', (S, S)); px = im.load()
        for y in range(S):
            for x in range(S):
                px[x, y] = (150 + int(40 * math.sin(x * 0.5 + y * 0.15)), 18, 34, 255)
    else:
        im = _starcape(9).resize((S, S), Image.NEAREST)
    return Image.composite(im, Image.new('RGBA', (S, S), (0, 0, 0, 0)), _mask(shape, S))


def _collar():
    S = 32; shape = [(4, 31), (28, 31), (31, 2), (16, 10), (1, 2)]
    im = _starcape(3).resize((S, S), Image.NEAREST)
    d = ImageDraw.Draw(im)
    for y in range(S): d.point((16, y), fill=(150, 18, 34, 255))
    return Image.composite(im, Image.new('RGBA', (S, S), (0, 0, 0, 0)), _mask(shape, S))


def _petal_wing():
    """a fairy wing of two great petals, pink deepening to rose at the root, veined, a pale edge"""
    S = 32; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); px = im.load()
    for (cx, cy, rx_, ry_, ang) in ((18, 11, 13, 9, -0.5), (14, 23, 9, 7, 0.45)):
        ca, sa = math.cos(ang), math.sin(ang)
        for y in range(S):
            for x in range(S):
                u, v = x + 0.5 - cx, y + 0.5 - cy
                a, b = (u * ca + v * sa) / rx_, (-u * sa + v * ca) / ry_
                r = a * a + b * b
                if r > 1: continue
                vein = abs(b) < 0.06 or abs(b - a * 0.5) < 0.05
                root = math.hypot(x - 2, y - 16) / 30
                px[x, y] = (255, 236, 244, 255) if r > 0.8 else _hsv(0.93, 0.55 - 0.3 * root, 0.85 + 0.15 * root) if not vein else (226, 120, 160, 255)
    return im


def _tier():
    """a tier of pearlescent skirt: its shimmer, a row of pearls along the hem"""
    im = _pearlshawl().resize((16, 16), Image.NEAREST); d = ImageDraw.Draw(im)
    for x in range(1, 16, 3):
        d.rectangle((x, 12, x + 1, 13), fill=(255, 255, 255, 255)); d.point((x + 1, 13), fill=(220, 210, 216, 255))
    return im


def _bolt(col):
    im = Image.new('RGBA', (16, 16), _hex(col) + (255,)); d = ImageDraw.Draw(im)
    d.rectangle((0, 6, 15, 9), fill=(255, 255, 255, 255))
    return im


def textures():
    T = {'cf_fin': _fin(), 'cf_crest': _crest(), 'cf_glass_r': _glass(False), 'cf_glass_l': _glass(True), 'cf_prism': _prism(),
         'cf_chain': _solid('#e0b040', 0.25, 1), 'cf_gold': _gold(), 'cf_ruby': _ruby(), 'cf_starcape': _starcape(), 'cf_starband': _starband(),
         'cf_cap_beret': _drawn_beret(), 'cf_cap_kerchief': _drawn_kerchief(), 'cf_kt_crown': _paper_crown(), 'cf_kt_cape': _scribble_cape(),
         'cf_aurora': _aurora(), 'cf_twinkle': _twinkle(), 'cf_flower_p': _flower('#ff9ac8'), 'cf_flower_w': _flower('#fff6f0'),
         'cf_flower_l': _flower('#c8a0ff', '#fff0a0'), 'cf_petals': _petals(), 'cf_wave': _wave(), 'cf_shell': _shell(), 'cf_pearl': _pearl(),
         'cf_mari_o': _marigold('#f08a10'), 'cf_mari_y': _marigold('#f8c420'), 'cf_pearlshawl': _pearlshawl(), 'cf_pearl_p': _pearl((246, 226, 236))}
    for i, col in enumerate(('#ff3ab0', '#30e8ff', '#fff040', '#60ff60', '#a070ff', '#ff8a30')):
        T[f'cf_neon_{i}'] = _neon(col)
    T['cf_opera'] = _cape_shape(False); T['cf_opera_lining'] = _cape_shape(True); T['cf_collar'] = _collar(); T['cf_tier'] = _tier(); T['cf_petalwing_r'] = _petal_wing(); T['cf_petalwing_l'] = _petal_wing().transpose(Image.FLIP_LEFT_RIGHT)
    return T


# ---------------------------------------------------------------------------------------------------- the pieces (world units, front +z)
def rx(a):
    c, s = math.cos(a), math.sin(a); return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def ry(a):
    c, s = math.cos(a), math.sin(a); return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rz(a):
    c, s = math.cos(a), math.sin(a); return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


D = math.radians


def box(c, h, tex, R=None, glow=0, sprite=False):
    return {'c': np.array(c, float), 'h': np.array(h, float), 'tex': tex, 'R': np.eye(3) if R is None else R, 'glow': glow, 'sprite': sprite}


def sprite(c, hw, hh, tex, R=None, glow=0):
    """a flat drawing in the xy plane (its front toward +z)"""
    return box(c, (hw, hh, 0.002), tex, R, glow, True)


def ring(cx, cy, cz, rx_, rz_, t, hgt, tex, glow=0):
    """a band round something: four boxes, front, back and sides"""
    return [box((cx, cy, cz + rz_), (rx_ + t, hgt, t), tex, glow=glow), box((cx, cy, cz - rz_), (rx_ + t, hgt, t), tex, glow=glow),
            box((cx + rx_, cy, cz), (t, hgt, rz_), tex, glow=glow), box((cx - rx_, cy, cz), (t, hgt, rz_), tex, glow=glow)]


def beads(cx, cy, cz, rx_, rz_, n, s, texs, droop=0.0, glow=0):
    """n little beads round an ellipse (droop: the front hangs lower than the back)"""
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        x, z = cx + rx_ * math.sin(a), cz + rz_ * math.cos(a)
        out.append(box((x, cy - droop * (1 + math.cos(a)) / 2, z), (s, s, s), texs[i % len(texs)], ry(a), glow))
    return out


def design(w, B):
    """-> [(part (whose bounds place it), [pieces], host (whose model carries them) or None)]"""
    lo = {k: v[0] for k, v in B.items()}; hi = {k: v[1] for k, v in B.items()}
    mid = {k: (v[0] + v[1]) / 2 for k, v in B.items()}
    ground = min(v[0][1] for v in B.values())
    if w == 'fishy':
        t = 'fy_body'; c = mid[t]
        tail = []
        for a in (-40, -20, 0, 20, 40):                     # (a betta's tail: five fanned panels from the tank's back, flowing out behind him)
            R = rz(D(a)) @ rx(D(58))
            L = 0.78 - abs(a) / 160
            root = np.array([c[0], lo[t][1] + 0.3, lo[t][2] - 0.01])
            tail.append(sprite(root + R @ np.array([0, -L / 2, 0]), 0.24, L / 2, 'cf_fin', R @ rz(D(180))))
        fins = []
        for p, sx in (('fy_armr', -1), ('fy_arml', 1)):    # (fins sweeping up off his shoulders)
            R = rz(D(180 - sx * 35))
            root = np.array([mid[p][0] - sx * 0.04, hi[p][1] - 0.2, mid[p][2]])
            fins.append((p, [sprite(root + R @ np.array([0, -0.26, 0]), 0.2, 0.26, 'cf_fin', R)]))
        return [(t, tail, None)] + [(p, f, None) for p, f in fins]
    if w == 'batty':
        b = 'gb_body'                                       # (his wings, leaded in glass: RETEX; on his chest a prism on a gold chain)
        chain = [box((mid[b][0] + sx * 0.06, hi[b][1] - 0.08, hi[b][2] + 0.01), (0.008, 0.07, 0.008), 'cf_chain', rz(D(sx * 35))) for sx in (-1, 1)]
        return [(b, chain + [box((mid[b][0], hi[b][1] - 0.17, hi[b][2] + 0.02), (0.045, 0.06, 0.02), 'cf_prism', rz(D(45)), glow=8)], None)]
    if w == 'eggbert':
        t = 'ge_body'; c = mid[t]                           # (his shell, a Faberge egg: RETEX; a jewelled gold finial on top)
        fin = [box((c[0], hi[t][1] + 0.03, c[2]), (0.09, 0.03, 0.09), 'cf_gold'), box((c[0], hi[t][1] + 0.09, c[2]), (0.05, 0.05, 0.05), 'cf_gold', ry(D(45))),
               box((c[0], hi[t][1] + 0.17, c[2]), (0.035, 0.035, 0.035), 'cf_ruby', ry(D(45)) @ rx(D(45)), glow=6)]
        return [(t, fin, 'ge_head')]
    if w == 'count':
        b = 'gc_body'; c = mid[b]
        top = hi[b][1] - 0.06
        L = top - ground - 0.02
        back = lo[b][2] - 0.02
        cape = [sprite((c[0], top - L / 2, back - 0.006), 0.62, L / 2, 'cf_opera'), sprite((c[0], top - L / 2, back), 0.62, L / 2, 'cf_opera_lining'),
                sprite((c[0], top + 0.14, back - 0.04), 0.4, 0.2, 'cf_collar', rx(D(-12)))]
        h = 'gc_hat'
        band = ring(mid[h][0], lo[h][1] + 0.07, mid[h][2], (hi[h][0] - lo[h][0]) * 0.33, (hi[h][2] - lo[h][2]) * 0.33, 0.01, 0.025, 'cf_starband')
        return [(b, cape, None), (h, band, None)]
    if w == 'capshun':
        hd = 'mz_head'; c = mid[hd]; hw = (hi[hd][0] - lo[hd][0]) / 2
        beret = [sprite((c[0] + 0.05, hi[hd][1] + 0.02, 0.012), hw * 0.62, hw * 0.48, 'cf_cap_beret', rz(D(-10)))]
        kerchief = [sprite((mid['mz_body'][0], hi['mz_body'][1] - 0.06, 0.012), 0.12, 0.12, 'cf_cap_kerchief')]
        return [(hd, beret, None), ('mz_body', kerchief, None)]
    if w == 'kettle':
        hd = 'kt_head'; c = mid[hd]; hw = (hi[hd][0] - lo[hd][0]) / 2
        crown = [sprite((c[0], hi[hd][1] - 0.04, 0.012), hw * 0.62, hw * 0.4, 'cf_kt_crown')]
        b = 'kt_body'; top = hi[b][1]
        cape = [sprite((mid[b][0], top - 0.3, -0.012), 0.28, 0.32, 'cf_kt_cape')]
        return [(hd, crown, None), (b, cape, None)]
    if w == 'sky':
        bk = 'yb_back'                                      # (the aurora's ribbons in the sky above and behind them; stars twinkling round the moon)
        aur = [sprite((0.45, 2.3, -0.62), 0.95, 0.32, 'cf_aurora', glow=6)]
        stars = [sprite((x, y, 0.12), s, s, 'cf_twinkle', glow=10) for x, y, s in ((0.72, 2.1, 0.06), (1.5, 1.6, 0.05), (1.38, 2.25, 0.04))]
        return [(bk, aur, 'yb_head'), ('yb_moon', stars, None)]
    if w == 'emma':
        hd = 'em_head'
        cx, cz = 0.0, (lo[hd][2] + hi[hd][2]) / 2 + 0.02
        crown = beads(cx, hi[hd][1] - 0.07, cz, 0.3, 0.27, 11, 0.042, ['cf_flower_p', 'cf_flower_w', 'cf_flower_l'])
        b = 'em_body'
        wings = []                                          # (petal wings on her back, a pair each side, swept back behind her - clear of her
        back = min(lo[hd][2], lo[b][2] + 0.1) - 0.03          #  hair, her arms and her skirt)
        for sx, tex in ((-1, 'cf_petalwing_l'), (1, 'cf_petalwing_r')):
            for k, (sz, rot, y) in enumerate(((0.27, 20, 1.1), (0.18, -12, 1.0))):
                R = ry(D(sx * 38)) @ rz(D(sx * rot))
                root = np.array([sx * 0.05, y, back])
                wings.append(sprite(root + R @ np.array([sx * sz, 0, 0]), sz, sz, tex, R))
        cape = wings
        return [(hd, crown, None), (b, cape, None)]
    if w == 'sky':
        bk = 'yb_back'                                      # (the aurora's ribbons in the sky above and behind them; stars twinkling round the moon)
        aur = [sprite((0.45, 2.3, -0.62), 0.95, 0.32, 'cf_aurora', glow=6)]
        stars = [sprite((x, y, 0.12), s, s, 'cf_twinkle', glow=10) for x, y, s in ((0.72, 2.1, 0.06), (1.5, 1.6, 0.05), (1.38, 2.25, 0.04))]
        return [(bk, aur, 'yb_head'), ('yb_moon', stars, None)]
    if w == 'emma':
        hd = 'em_head'
        cx, cz = 0.0, (lo[hd][2] + hi[hd][2]) / 2 + 0.02
        crown = beads(cx, hi[hd][1] - 0.07, cz, 0.3, 0.27, 11, 0.042, ['cf_flower_p', 'cf_flower_w', 'cf_flower_l'])
        b = 'em_body'
        cape = []
        for yy, r in ((1.045, 0.18), (0.995, 0.21), (0.945, 0.24)):   # (three tiers of petals at her shoulders, under her chin, each wider)
            cape += ring(0.0, yy, 0.05, r, r * 0.75, 0.01, 0.03, 'cf_petals')
        return [(hd, crown, None), (b, cape, None)]
    if w == 'ava':
        b = 'av_body'
        top = hi[b][1] - 0.08
        back = min(lo[k][2] for k in B if hi[k][1] > ground + 0.1 and lo[k][1] < top) - 0.02
        L = top - ground - 0.02
        train = [box((0, top - L / 2, back), (0.3, L / 2, 0.012), 'cf_wave'),
                 box((0, ground + 0.012, back - 0.25), (0.36, 0.012, 0.25), 'cf_wave'),               # (it pools on the ground behind her)
                 box((0, top, (back + mid[b][2]) / 2), (0.3, 0.02, (mid[b][2] - back) / 2), 'cf_wave')]
        neck = beads(0, hi[b][1] - 0.04, mid[b][2] + 0.02, 0.14, 0.12, 12, 0.022, ['cf_pearl', 'cf_shell'], droop=0.05)
        neck.append(box((0, hi[b][1] - 0.15, mid[b][2] + 0.15), (0.045, 0.045, 0.012), 'cf_shell', rz(D(45))))
        return [(b, train + neck, None)]
    if w == 'demo':
        b = 'dm_body'                                       # (a garland of marigolds over his shoulders, hanging in a loop down his chest)
        gar = beads(mid[b][0], hi[b][1] - 0.22, mid[b][2] + 0.02, 0.4, 0.33, 18, 0.05, ['cf_mari_o', 'cf_mari_y'], droop=0.3)
        hd = 'dm_head'
        tuck = [box((lo[hd][0] + 0.02, mid[hd][1] + 0.1, hi[hd][2] - 0.14), (0.065, 0.065, 0.065), 'cf_mari_o', ry(D(30))),
                box((lo[hd][0] + 0.01, mid[hd][1] - 0.02, hi[hd][2] - 0.1), (0.055, 0.055, 0.055), 'cf_mari_y', ry(D(-20)))]
        return [(b, gar, None), (hd, tuck, None)]
    if w == 'kw':                                           # (his lightning runs through every colour: RETEX; and it crackles down his arms)
        out = []
        for p, sx in (('kw_armr', -1), ('kw_arml', 1)):
            c = mid[p]; segs = []
            y = hi[p][1] - 0.12
            x = c[0] + sx * (hi[p][0] - lo[p][0]) * 0.46
            for k in range(7):                              # (a zigzag of current, segment by segment, each a colour)
                ang = 35 if k % 2 else -35
                L = 0.11
                R = rz(D(ang * sx))
                segs.append(box((x, y - L / 2, hi[p][2] - 0.02), (0.012, L / 2 + 0.01, 0.012), f'cf_neon_{k % 6}', R, glow=15))
                y -= L * math.cos(D(35)); x += sx * (0.04 if k % 2 else -0.04)
            out.append((p, segs, None))
        return out
    if w == 'pearlq':
        b = 'pq_body'
        y = hi[b][1] - 0.12
        neck = beads(0, y, mid[b][2] + 0.01, 0.12, 0.11, 14, 0.018, ['cf_pearl', 'cf_pearl_p'], droop=0.04) + \
            beads(0, y - 0.03, mid[b][2] + 0.01, 0.15, 0.13, 16, 0.02, ['cf_pearl_p', 'cf_pearl'], droop=0.09)
        skirt = []                                          # (a pearlescent overskirt in three tiers, pearls along each hem)
        for k, (yy, r) in enumerate(((0.98, 0.21), (0.84, 0.25), (0.7, 0.29))):
            skirt += ring(0, yy, mid[b][2] + 0.01, r, r * 0.8, 0.012, 0.075, 'cf_tier')
        return [(b, neck + skirt, None)]
    raise KeyError(w)

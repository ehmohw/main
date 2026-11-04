"""(3.1 draft, stage 1: art only) A small rig-builder shared by the new followers' art modules (glitch_pet_art, cake_pet_art,
sapling_pet_art, hollowknight_pet_art, mimic_pet_art, spawner_pet_art, assembler_pet_art; doodlemob_forms_art takes Rig).

A Rig is a rigkit rig as rigpet / rigfol / draftkit / phase134 / dolls_bake take one - PREFIX, RIG_SCALE, PIVOT, PARENT, PARTS,
PART_K, HIDDEN(p, pose), model_name(p, pose, suffix), textures(), models(), POSES - built box by box in design units (feet at
y=0, facing -z, its right +x), so each follower module says only what it looks like and how it moves.

  box(part, from, to, tex, ...)   an element (rigkit.el) on a part. Texture tokens in TOKENS ('FACE', 'EYES') become the part's
                                  face / eyes texture, per expression (face_<kind>, eyes_<kind>) - on the face part(s) only
  seg(part, A, B, w, h, tex)      a box along a line (rigkit.seg)
  skin(suffix, {tex: tex2})       a model set with some textures swapped - a palette, a shiny, a stage, an afterimage ('_g')
  opt                             parts hidden unless a pose's '_show' names them (a held prop, a burst of shards)
  ground(pose)                    the pose's '_off' set so its lowest point stands on y=0 (lift: off the floor by that much)
  fit(pose)                       phase134.FIT: (lowest y, height, x0, x1, z0, z1) in blocks at RIG_SCALE

THE QUALITY BAR (v2 - after studying Emma, the Pale Dryad, the Lightbringer, the Keeper, the Mireling, Henry / Nia, the Gem):

  textures   64 px, painted in 2-px cells (half a design unit) with STRUCTURE, never random per-pixel noise:
               soft()     the Dryad's: mostly the base, a few lighter / darker cells in soft 5x5 patches
               lit()      Emma's light from above - a ramp down the first rows (use with anchored boxes: shift=False)
               bark()     ridges: a lit crest, a shaded furrow, wavering, a few lenticels - wood that reads as wood
               leaves()   rows of overlapping leaves (lit tip, dark edge), the Dryad's skirt
               blade()    one leaf (full-uv): a centre vein, lit on one half, a dark rim
               planks()   boards: a dark seam, grain streaks along each board, a lit top edge, nail heads
               metal()    brushed plate: fine streaks, a bright bevel row and a dark one (anchored)
               strands()  hair / fur / flame in clumps: lit in the middle, dark partings, a sheen band (Emma's _hair2)
               glaze()    icing, slime, enamel: smooth, a sheen band, a soft drip shadow
               sponge()   cake crumb: air pits on a jittered grid (each a dark cell with a lit lip below), never speckle
               glow()     full-uv radial ramp for a flame, a soul, an orb
  faces      a face plate (blush, mouth, brows) and a SEPARATE eye overlay ('EYES', 0.02-0.04 proud, light_emission ~6),
             drawn by eye(): a 2-px upper lash with an outer flick, an iris shaded row by row dark-to-light, a pupil, one big
             white shine and a small second one, a rounded bottom row. Every expression is redrawn (happy arcs, blink, hurt > <).
  shapes     silhouettes from slabs: slab() an octagon (3 boxes), stack() / dome() / ball() rows of slabs; leaf() a tapered
             3-seg blade; chain() tapered segs (roots, tails, a serpent); ring() boxes round a circle. Lips, rims and bevels as
             thin boxes a hair proud (0.05-0.15) of the surface; trim strips over seams; accents in small purposeful clusters."""
import math
import random
from PIL import Image, ImageDraw

from rigkit import qs, el, seg as _seg, solve, qrot, D, I

FACESIDES = ('north', 'south', 'east', 'west', 'up', 'down')
TOKENS = ('FACE', 'EYES', 'SNOUT')


def hexc(h, a=255):
    if isinstance(h, tuple): return h if len(h) == 4 else tuple(h) + (a,)
    h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def mix(a, b, t):
    a, b = hexc(a), hexc(b)
    return '#%02x%02x%02x' % tuple(max(0, min(255, int(round(a[i] + (b[i] - a[i]) * t)))) for i in range(3))


def mul(c, k):
    c = hexc(c); return '#%02x%02x%02x' % tuple(max(0, min(255, int(c[i] * k))) for i in range(3))


def limb(sx, fwd=0.0, out=0.0, turn=0.0):
    """a limb's turn (as kettle_art): swung forward, out to its own side, twisted"""
    return qs(('y', turn * sx), ('x', -fwd), ('z', -out * sx))


def T(x=0.0, y=0.0, z=0.0):
    """a trunk's turn: leaned forward (x), turned (y), tipped to its left (z)"""
    return qs(('x', x), ('y', y), ('z', z))


# ---------------------------------------------------------------------------------------------------- textures (v1, kept)
def coat(col, seed, size=32, var=0.06, cell=2, spots=None, alpha=255):
    """(v1 - below the bar: random cells read as noise. Kept for old callers; use soft() and the patterned coats.)"""
    im = Image.new('RGBA', (size, size)); px = im.load(); c = hexc(col); r = random.Random(seed * 7919 + 13)
    for cy in range(0, size, cell):
        for cx in range(0, size, cell):
            k = 1 + r.uniform(-1, 1) * var; q = r.random()
            if q < 0.08: k *= 0.88
            elif q < 0.12: k *= 1.08
            v = tuple(max(0, min(255, int(c[i] * k))) for i in range(3)) + (alpha,)
            for y in range(cy, min(size, cy + cell)):
                for x in range(cx, min(size, cx + cell)): px[x, y] = v
    if spots:
        d = ImageDraw.Draw(im)
        for sc, n in spots:
            for _ in range(n):
                x, y = r.randrange(0, size, cell), r.randrange(0, size, cell)
                d.rectangle((x, y, x + cell - 1, y + cell - 1), fill=hexc(sc, alpha))
    return im


def flat(col, size=16, alpha=255):
    return Image.new('RGBA', (size, size), hexc(col, alpha))


def shade(im, top=1.12, bot=0.82):
    """lit from above: a vertical ramp over the texture (pixel steps)"""
    im = im.copy(); px = im.load(); n = im.height
    for y in range(n):
        k = top + (bot - top) * (y // max(1, n // 8) * max(1, n // 8)) / max(1, n - 1)
        for x in range(im.width):
            r, g, b, a = px[x, y]; px[x, y] = (min(255, int(r * k)), min(255, int(g * k)), min(255, int(b * k)), a)
    return im


def ghost(im, tint, a=120):
    """an afterimage: the texture washed toward a tint, see-through (rendered blended)"""
    im = im.convert('RGBA').copy(); px = im.load(); t = hexc(tint)
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, al = px[x, y]
            if al < 10: continue
            v = (r + g + b) / 765
            px[x, y] = (int(t[0] * (0.5 + 0.5 * v)), int(t[1] * (0.5 + 0.5 * v)), int(t[2] * (0.5 + 0.5 * v)), a)
    return im


def remap(im, pal, stretch=False):
    """recolour by luminance through a list of hex colours, dark to light (a palette swap); stretch: the texture's own darkest
    to lightest spread over the whole list (a dark plate recoloured bright keeps its shading)"""
    im = im.convert('RGBA').copy(); px = im.load(); cols = [hexc(c) for c in pal]; n = len(cols)
    lum = lambda r, g, b: (0.3 * r + 0.59 * g + 0.11 * b) / 255
    vs = [lum(*px[x, y][:3]) for y in range(im.height) for x in range(im.width) if px[x, y][3] >= 10] or [0, 1]
    lo, hi = (min(vs), max(vs)) if stretch else (0.0, 1.0)
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a < 10: continue
            v = (lum(r, g, b) - lo) / max(1e-6, hi - lo) * 0.999
            px[x, y] = cols[min(n - 1, int(v * n))][:3] + (a,)
    return im


def recolor(im, table):
    """swap exact colours (hex -> hex): a palette variant of a hand-painted texture that keeps every highlight where it was"""
    im = im.convert('RGBA').copy(); px = im.load(); t = {hexc(a)[:3]: hexc(b)[:3] for a, b in table.items()}
    for y in range(im.height):
        for x in range(im.width):
            p = px[x, y]
            if p[:3] in t: px[x, y] = t[p[:3]] + (p[3],)
    return im


def hue(im, fn):
    """recolour every pixel through fn((r, g, b)) -> (r, g, b) (keeps alpha)"""
    im = im.convert('RGBA').copy(); px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            p = px[x, y]
            if p[3]: px[x, y] = tuple(max(0, min(255, int(v))) for v in fn(p[:3])) + (p[3],)
    return im


def alpha(im, a):
    im = im.convert('RGBA').copy(); px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            p = px[x, y]
            if p[3]: px[x, y] = p[:3] + (a,)
    return im


def canvas(n=64, fill=None):
    im = Image.new('RGBA', (n, n), hexc(fill) if fill else (0, 0, 0, 0)); return im, ImageDraw.Draw(im)


def up(im, n):
    return im.resize((n, n), Image.NEAREST)


# ---------------------------------------------------------------------------------------------------- textures (v2: the bar)
def cells(fn, seed, cell=2, size=64, alpha=255):
    """a texture painted cell by cell (2-px cells: half a design unit) - fn(cx, cy, rnd) -> colour"""
    im = Image.new('RGBA', (size, size)); d = ImageDraw.Draw(im); rnd = random.Random(seed); n = size // cell
    for cy in range(n):
        for cx in range(n):
            c = fn(cx, cy, rnd)
            if c is None: continue
            d.rectangle((cx * cell, cy * cell, cx * cell + cell - 1, cy * cell + cell - 1), fill=hexc(c, alpha) if isinstance(c, str) else c)
    return im


def _patch(seed, n=5):
    rnd = random.Random(seed * 7 + 1)
    return [[rnd.random() for _ in range(n)] for _ in range(n)]


def soft(base, light, dark, seed, p=0.16, alpha=255):
    """gentle cell shading (the Dryad's): mostly the base, a few cells a shade lighter or darker, in soft patches"""
    pt = _patch(seed)
    def c(x, y, r):
        k = pt[y * 4 // 32][x * 4 // 32]; q = r.random()
        if q < p * (0.4 + k): return light
        if q > 1 - p * (1.4 - k) * 0.6: return dark
        return base
    return cells(c, seed, alpha=alpha)


def lit(im, top=1.10, bot=0.92, rows=12, hl=None):
    """light from above (Emma's): the first `rows` texel rows ramp from `top` to 1, the rest ease to `bot` by the bottom; hl: a
    colour for row 0-1 (a bright lip). Use on boxes that sample from the texture's top (shift=False)"""
    im = im.convert('RGBA').copy(); px = im.load(); n = im.height
    for y in range(n):
        k = top + (1 - top) * min(1.0, y / max(1, rows)) if y < rows else 1 + (bot - 1) * (y - rows) / max(1, n - rows)
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if not a: continue
            px[x, y] = (min(255, int(r * k)), min(255, int(g * k)), min(255, int(b * k)), a)
    if hl:
        d = ImageDraw.Draw(im); d.rectangle((0, 0, im.width - 1, 1), fill=hexc(hl))
    return im


def bark(pal, seed, w=4, knots=3, alpha=255):
    """bark (pal: deep, dark, base, light): vertical ridges every `w` cells - a lit crest, the base, a shaded furrow -
    each wavering a cell left or right as it runs; a few dark lenticel dashes across, and a knot or two (rings)"""
    deep, dark, base, light = pal
    rnd = random.Random(seed)
    n = 32; wav = [[0] * n for _ in range(n // w + 2)]
    for i in range(len(wav)):
        o = 0
        for y in range(n):
            if rnd.random() < 0.16: o = max(-1, min(1, o + rnd.choice((-1, 1))))
            wav[i][y] = o
    dash = {(rnd.randrange(n), rnd.randrange(n)) for _ in range(9)}
    ks = [(rnd.randrange(3, n - 3), rnd.randrange(3, n - 3)) for _ in range(knots)]
    def c(x, y, r):
        for kx, ky in ks:
            dd = max(abs(x - kx), abs(y - ky) * 0.8)
            if dd < 0.8: return deep
            if dd < 1.6: return dark
            if dd < 2.3: return light
        i = x // w; xx = (x - wav[i][y]) % w
        if (x, y) in dash or (x - 1, y) in dash: return dark
        if xx == 0: return dark if (y + i) % 6 else deep
        if xx == 1: return light
        if xx == w - 1: return dark
        return base
    return cells(c, seed, alpha=alpha)


def leaves(pal, seed, alpha=255):
    """rows of overlapping leaves (pal: dark, base, light, tip) - scales 3 cells wide, 4 tall, each row offset: a lit tip in
    the middle, the base, and a shadow under each leaf's two edges (so the shadow scallops instead of striping)"""
    dark, base, light, tip = pal
    def c(x, y, r):
        col = x % 3; k = (y + (x // 3) % 2 * 2) % 4
        if k == 3: return dark if col != 1 else mix(base, dark, 0.4)
        if k == 0: return tip if col == 1 else light
        if k == 1 and col == 1: return light
        return base
    return cells(c, seed, alpha=alpha)


def foliage(pal, seed, step=5, alpha=255):
    """a leafy mass seen from outside (pal: dark, base, light, tip): a soft base, and on a jittered grid single leaves - a lit
    tip cell over a base cell, a shadow cell tucked under - so it reads as many leaves without striping or speckle"""
    dark, base, light, tip = pal
    rnd = random.Random(seed); lv = {}
    for gy in range(0, 32, step):
        for gx in range(0, 32, step):
            x, y = gx + rnd.randrange(step - 1), gy + rnd.randrange(step - 2)
            lv[(x, y)] = rnd.random()
    pt = _patch(seed)
    def c(x, y, r):
        if (x, y) in lv: return tip if lv[(x, y)] < 0.5 else light
        if (x - 1, y) in lv or (x + 1, y) in lv: return light if lv.get((x - 1, y), lv.get((x + 1, y), 1)) < 0.5 else base
        if (x, y - 1) in lv: return base
        if (x, y - 2) in lv or (x - 1, y - 2) in lv: return dark
        k = pt[y * 4 // 32][x * 4 // 32]
        return mix(base, dark, 0.35) if k < 0.25 else base
    return cells(c, seed, alpha=alpha)


def blade(pal, seed=0, vein=None, rim=True, alpha=255):
    """a single leaf for a full-uv face (pal: dark, base, light): a centre vein (column 15-16) and side veins angled up,
    the half toward the light a shade lighter, a darker rim, a pale vein"""
    dark, base, light = pal; vein = vein or mix(light, '#ffffff', 0.3)
    def c(x, y, r):
        if rim and (x in (0, 31) or (rim != 'sides' and y in (0, 31))): return dark
        if x in (15, 16): return vein
        d = abs(x - 15.5)
        if (y + int(d * 0.8)) % 7 == 0 and d < 13: return mix(vein, base, 0.45)
        return light if x < 15 else base
    return cells(c, seed, alpha=alpha)


def planks(pal, seed, board=8, nails=True, alpha=255):
    """boards running across (pal: seam, dark, base, light): each `board` cells tall, a dark seam under it, a lit top row,
    long grain streaks along it (a few cells long, never single dots), a nail head at each end"""
    seam, dark, base, light = pal
    rnd = random.Random(seed)
    streaks = set()
    for _ in range(46):
        y = rnd.randrange(32); x0 = rnd.randrange(32); L = rnd.randint(3, 9)
        if y % board in (0, board - 1): continue
        for x in range(x0, x0 + L): streaks.add((x % 32, y))
    def c(x, y, r):
        b = y % board
        if b == board - 1: return seam
        if b == 0: return light
        if nails and b == board // 2 and x % 16 in (2,): return dark
        if (x, y) in streaks: return dark if (x + y) % 3 else mix(dark, base, 0.5)
        return base
    return cells(c, seed, alpha=alpha)


def metal(pal, seed, rivets=False, alpha=255):
    """brushed plate (pal: dark, base, light, shine): fine horizontal streaks, a bright bevel along the top rows (anchored
    boxes), a darker bottom row, rivets on a grid if asked"""
    dark, base, light, shine = pal
    rnd = random.Random(seed); st = {(rnd.randrange(32), rnd.randrange(32)): rnd.randint(2, 6) for _ in range(30)}
    s2 = set()
    for (x, y), L in st.items():
        for i in range(L): s2.add(((x + i) % 32, y))
    def c(x, y, r):
        if y == 0: return shine
        if y == 1: return light
        if y == 31: return dark
        if rivets and x % 8 == 3 and y % 8 == 3: return shine
        if rivets and x % 8 == 3 and y % 8 == 4: return dark
        if (x, y) in s2: return light if y % 2 else mix(base, dark, 0.5)
        return base
    return cells(c, seed, alpha=alpha)


def strands(pal, seed, sheen=(5, 7), clump=(3, 5), alpha=255):
    """hair / fur / flame in clumps (pal: part, dark, base, light, shine): each clump lit in its middle, dark at its parting,
    strands wandering down it, a sheen band across that waves with the clumps (Emma's _hair2, in cells)"""
    part, dark, base, light, shine = pal
    rnd = random.Random(seed); cl = []; x = 0
    while x < 32:
        w = rnd.randint(*clump); cl.append((x, w, rnd.uniform(0, 6.28))); x += w
    col = {}
    for x0, w, wob in cl:
        for j in range(w):
            col[x0 + j] = (j, w, wob)
    def c(x, y, r):
        j, w, wob = col.get(x, (1, 3, 0))
        sy = sheen[0] + 1.2 * math.sin(wob + x / 3)
        if j == 0: return part
        if sy <= y <= sy + (sheen[1] - sheen[0]) and 0 < j < w - 1: return shine
        t = abs(j - (w - 1) / 2) / max(1, (w - 1) / 2)
        if t > 0.7: return dark
        if t < 0.3 and y % 6 < 4: return light
        return base
    return cells(c, seed, alpha=alpha)


def glaze(pal, seed, sheen=3, alpha=255):
    """a smooth glossy coat (pal: dark, base, light, shine): the base, a soft sheen band near the top (rows sheen..+1, with
    a gap here and there), a hint of darker at the foot - icing, enamel, slime"""
    dark, base, light, shine = pal
    pt = _patch(seed)
    def c(x, y, r):
        k = pt[y * 4 // 32][x * 4 // 32]
        if y in (sheen, sheen + 1) and (x // 5) % 3 != 2: return shine if y == sheen else light
        if y == sheen - 1 and (x // 5) % 3 == 0: return light
        if y >= 28: return dark if (x + y) % 3 else base
        if r.random() < 0.06 * (0.5 + k): return light
        return base
    return cells(c, seed, alpha=alpha)


def sponge(pal, seed, step=4, alpha=255):
    """cake crumb (pal: deep, dark, base, light): air pits on a jittered grid - a dark cell with a deeper core and a lit lip
    under it - over a softly patched base; never single-pixel speckle"""
    deep, dark, base, light = pal
    rnd = random.Random(seed); pits = {}
    for gy in range(0, 32, step):
        for gx in range(0, 32, step):
            if rnd.random() < 0.6:
                x, y = gx + rnd.randrange(step - 1), gy + rnd.randrange(step - 1)
                pits[(x, y)] = rnd.random() < 0.35
    pt = _patch(seed)
    def c(x, y, r):
        if (x, y) in pits: return deep if pits[(x, y)] else dark
        if (x, y - 1) in pits: return light
        k = pt[y * 4 // 32][x * 4 // 32]
        if r.random() < 0.08 * k: return light
        return base
    return cells(c, seed, alpha=alpha)


def glow(stops, size=32, cx=0.5, cy=0.55, alpha=None, ring=False):
    """a full-uv radial ramp (stops: centre to edge) for a flame, a soul, an orb; alpha: per-stop alphas (see-through rim)"""
    im = Image.new('RGBA', (size, size)); px = im.load(); n = len(stops)
    for y in range(size):
        for x in range(size):
            d = math.hypot((x + 0.5) / size - cx, (y + 0.5) / size - cy) / 0.62
            if ring: d = abs(d - 0.5) * 2
            i = min(n - 1, int(d * n))
            px[x, y] = hexc(stops[i], (alpha[i] if alpha else 255))
    return im


def stripes(cols, w, seed=0, vertical=True, alpha=255):
    """bands of colours, each w cells (piping, a candle, a scarf)"""
    return cells(lambda x, y, r: cols[((x if vertical else y) // w) % len(cols)], seed, alpha=alpha)


# ---------------------------------------------------------------------------------------------------- faces
def put(im, x, y, c):
    if 0 <= x < im.width and 0 <= y < im.height: im.putpixel((int(x), int(y)), hexc(c))


def eye(im, cx, y0, w, h, flip=False, kind=None, iris=('#3a1a08', '#6a3410', '#a8621a', '#d89a3a', '#f4cc6a'), lash='#2a1610',
        pupil='#140804', white='#fffaf4', lower=None, sclera=True, shine='#ffffff', glow=None, irk=0.72, lid=None):
    """one big anime eye on a face / eyes sheet (the Lightbringer's eye, generalised). cx: its centre column, y0: its top row,
    w x h in texels. flip: the sheet's right eye (its left), mirrored - the outer corner to the right. sclera=False: a glossy
    all-iris eye (a creature's - the cake, the sapling): the whole eye graded dark-top to light-bottom, a big pupil, the
    shines. kinds: None, 'happy' (^ arches), 'blink' (closed curve), 'hurt' (> <), 'fierce', 'sad', 'surprised', 'sleepy',
    'wide' (no lid at all), 'look' (the iris slid toward the outer corner). glow: an image the iris is copied to (the lit overlay)."""
    o = 1 if flip else -1
    xs = range(cx - w // 2, cx - w // 2 + w)
    dxn = lambda x: (x + 0.5 - cx) / (w / 2)
    inner = lambda x: max(0.0, min(1.0, 0.5 - 0.5 * dxn(x) * (-o)))
    if kind in ('happy', 'blink'):
        for x in xs:
            d = dxn(x)
            if abs(d) > 1: continue
            y = y0 + int(h * 0.62) - round(h * 0.26 * (1 - d * d)) if kind == 'happy' else y0 + int(h * 0.5) + round(h * 0.18 * (1 - d * d))
            put(im, x, y, lash)
            if abs(d) < 0.75: put(im, x, y + 1, lash)
        ox = cx + (w // 2 if flip else -w // 2 - 1)
        if kind == 'blink': put(im, ox, y0 + int(h * 0.5) - 1, lash); put(im, ox + o, y0 + int(h * 0.5) - 2, lash)
        else: put(im, ox, y0 + int(h * 0.62) + 1, lash)
        return
    if kind == 'hurt':
        tip, far = cx + (w // 4 if not flip else -w // 4 - 1), cx + (-w // 2 + 1 if not flip else w // 2 - 2)
        for i in range(9):
            t = i / 8; x = round(far + (tip - far) * t)
            put(im, x, round(y0 + h * 0.2 + h * 0.3 * t), lash); put(im, x, round(y0 + h * 0.8 - h * 0.3 * t), lash)
            if 0.3 < t < 0.85: put(im, x, round(y0 + h * 0.2 + h * 0.3 * t) + 1, lash); put(im, x, round(y0 + h * 0.8 - h * 0.3 * t) - 1, lash)
        return
    L, A, slant = {None: (2, 1.6, 0), 'look': (2, 1.6, 0), 'fierce': (h * 0.32, 0.8, 2), 'sad': (2, 1.4, -2), 'surprised': (0, 0, 0),
                   'wide': (0, 0, 0), 'sleepy': (h * 0.42, 0.5, 0)}.get(kind, (2, 1.6, 0))
    if lid is not None: L = lid
    def lidy(x):
        d = dxn(x)
        return y0 + L - round(A * (1 - d * d)) + round(slant * inner(x) if slant > 0 else -slant * (1 - inner(x)))
    vis = set()
    for y in range(y0, y0 + h):
        t = (y + 0.5 - y0) / h
        half = (w / 2) * math.sqrt(max(0.0, 1 - (2 * t - 1) ** 2 * (0.86 if sclera else 0.62)))
        for x in xs:
            if abs(x + 0.5 - cx) < half and y >= lidy(x): vis.add((x, y))
    if not vis: return
    if sclera:
        for x, y in vis: put(im, x, y, white)
    shift = (o * w * 0.12) if kind == 'look' else 0
    icx = cx + shift
    ir = w * (0.36 if kind != 'surprised' else 0.27) if sclera else w
    icy, ih = (y0 + h * 0.56, h * 0.5 * (1 if kind != 'surprised' else 0.76)) if sclera else (y0 + h / 2, h)
    irs = {(x, y) for (x, y) in vis if (not sclera) or (((x + 0.5 - icx) / ir) ** 2 + ((y + 0.5 - icy) / ih) ** 2 <= 1 and y < y0 + h - 1)}
    if irs:
        top, bot = min(y for _, y in irs), max(y for _, y in irs)
        for x, y in irs:
            t = (y - top) / max(1, bot - top)
            c = iris[min(len(iris) - 1, int(t * len(iris)))]
            edge = any((x + dx, y + dy) not in irs for dx, dy in ((1, 0), (-1, 0), (0, 1)))
            if edge and y > top + 1 and sclera: c = mix(c, '#ffffff', 0.28)
            put(im, x, y, c)
        pr = (w * (0.15 if kind == 'surprised' else 0.2)) if sclera else w * irk * 0.3
        pcy = icy - 0.5 if sclera else y0 + h * 0.52
        for x, y in irs:
            if ((x + 0.5 - icx) / pr) ** 2 + ((y + 0.5 - pcy) / (pr * 1.35)) ** 2 <= 1:
                put(im, x, y, pupil)
        # one big shine (up, toward the viewer's left on both eyes: one light), and a small second one low on the other side
        bs = max(2, round(w * (0.2 if sclera else 0.24)))
        hx = round(icx - w * (0.28 if sclera else 0.26)); hy = top + (1 if sclera else max(1, round(h * 0.14)))
        for dx in range(bs):
            for dy in range(bs + (0 if sclera else 1)):
                if (hx + dx, hy + dy) in irs: put(im, hx + dx, hy + dy, shine)
        sx2, sy2 = round(icx + w * 0.18), bot - max(1, round(h * 0.16))
        for dx, dy in ((0, 0), (1, 0)) if w >= 10 else ((0, 0),):
            if (sx2 + dx, sy2 + dy) in irs: put(im, sx2 + dx, sy2 + dy, shine)
        if glow is not None:
            for x, y in irs: glow.putpixel((x, y), im.getpixel((x, y)))
    tops = {}
    for x, y in vis: tops[x] = min(y, tops.get(x, 99))
    for x, ty in tops.items():
        put(im, x, ty - 1, lash)
        if abs(dxn(x)) < 0.8 and kind not in ('wide',): put(im, x, ty, lash) if sclera else put(im, x, ty - 2, lash) if abs(dxn(x)) < 0.5 else None
    if kind not in ('surprised', 'wide', 'sad'):
        ox = max(tops) if flip else min(tops)
        put(im, ox + o, tops[ox] - 1, lash); put(im, ox + o, tops[ox] - 2, lash); put(im, ox + 2 * o, tops[ox] - 3, lash)
    if lower:
        for x in range(cx - w // 4, cx + w // 4): put(im, x, y0 + h, lower)
    if kind == 'sad':
        for dy, c in ((0, '#bfe6ff'), (1, '#e8f8ff'), (2, '#bfe6ff')): put(im, cx + o * (w // 2 - 1), y0 + h + 1 + dy, c)


def blush(im, cx, cy, w=6, col='#f6a8a0', col2=None, dots=None):
    """a soft blush: a wide row and a narrower one under it, a few darker freckle dots if asked"""
    col2 = col2 or mix(col, '#ffffff', 0.35)
    for x in range(cx - w // 2, cx + w // 2): put(im, x, cy, col)
    for x in range(cx - w // 2 + 1, cx + w // 2 - 1): put(im, x, cy + 1, col2)
    if dots:
        for dx in (-w // 3, 0, w // 3): put(im, cx + dx, cy, dots)


def mouth(im, cx, y, kind='smile', col='#5a2418', tongue='#e8707a', w=4):
    """a small mouth: smile (a soft w / u), open (a little open smile with a tongue), o (surprised), flat, frown, wobble,
    grin (teeth), cat (:3)"""
    cx, y, w = int(cx), int(y), int(w); h = w // 2
    if kind == 'smile':
        put(im, cx - h, y, col); put(im, cx + h - 1, y, col)
        for x in range(cx - h + 1, cx + h - 1): put(im, x, y + 1, col)
    elif kind == 'open':
        for x in range(cx - h, cx + h): put(im, x, y, col)
        for x in range(cx - h + 1, cx + h - 1): put(im, x, y + 1, col); put(im, x, y + 2, tongue if x != cx - h + 1 else col)
        for x in range(cx - h + 2, cx + h - 2): put(im, x, y + 3, col)
        put(im, cx - h + 1, y + 2, col); put(im, cx + h - 2, y + 2, col)
    elif kind == 'o':
        for x in (cx - 1, cx): put(im, x, y, col); put(im, x, y + 2, col)
        put(im, cx - 2, y + 1, col); put(im, cx + 1, y + 1, col); put(im, cx - 1, y + 1, tongue); put(im, cx, y + 1, tongue)
    elif kind == 'flat':
        for x in range(cx - h, cx + h): put(im, x, y + 1, col)
    elif kind == 'frown':
        put(im, cx - h, y + 1, col); put(im, cx + h - 1, y + 1, col)
        for x in range(cx - h + 1, cx + h - 1): put(im, x, y, col)
    elif kind == 'wobble':
        for i, x in enumerate(range(cx - h - 1, cx + h + 1)): put(im, x, y + (i % 2), col)
    elif kind == 'cat':
        put(im, cx - 2, y, col); put(im, cx - 1, y + 1, col); put(im, cx, y, col); put(im, cx + 1, y + 1, col); put(im, cx + 2, y, col)
    elif kind == 'grin':
        for x in range(cx - h - 1, cx + h + 1): put(im, x, y, col); put(im, x, y + 2, col)
        for x in range(cx - h, cx + h): put(im, x, y + 1, '#ffffff')
        put(im, cx - h - 1, y + 1, col); put(im, cx + h, y + 1, col)


# ---------------------------------------------------------------------------------------------------- the rig
def _rotm(rot):
    """an element's rotation (rigkit.el's rot) -> (3x3 rows, origin) in design space"""
    if not rot: return None, None
    def rx(a): c, s = math.cos(a), math.sin(a); return [[1, 0, 0], [0, c, -s], [0, s, c]]
    def ry(a): c, s = math.cos(a), math.sin(a); return [[c, 0, s], [0, 1, 0], [-s, 0, c]]
    def rz(a): c, s = math.cos(a), math.sin(a); return [[c, -s, 0], [s, c, 0], [0, 0, 1]]
    def mm(A, B): return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    if isinstance(rot[0], str):
        M = {'x': rx, 'y': ry, 'z': rz}[rot[0]](math.radians(rot[1]))
    else:
        ax, ay, az = rot[0]; M = mm(rz(math.radians(az)), mm(ry(math.radians(ay)), rx(math.radians(ax))))
    return M, rot[-1]


class Rig:
    def __init__(self, prefix, scale, pivot, parent, faces=(), face_part='head', opt=(), companion=None):
        self.PREFIX = prefix; self.RIG_SCALE = scale; self.COMPANION = companion or scale
        self.PIVOT = dict(pivot); self.PARENT = dict(parent); self.PARTS = tuple(pivot); self.PART_K = {}
        self.FACES = tuple(faces); self.FACE_PART = face_part; self.OPT = set(opt)
        self.FACE_PARTS = (face_part,) if isinstance(face_part, str) else tuple(face_part)
        self._els = {p: [] for p in pivot}; self._pts = {p: [] for p in pivot}
        self._tex = {}; self._skins = {}; self.POSES = {}; self.DRAFT = []
        self._n = 0

    # ---- building
    def tex(self, name, im):
        self._tex[name] = im

    def box(self, part, fr, to, tex, rot=None, uv=None, faces=None, light=0, full=False, shift=None):
        """shift: None (a window per box, spread over the texture), False (anchored at the texture's top-left - lit() rows land
        on the box's top), or (du, dv)"""
        pv = self.PIVOT[part]
        if full: uv = dict({f: [0, 0, 16, 16] for f in FACESIDES}, **(uv or {}))
        self._n += 1
        if shift is None and not (full or uv): sh = ((self._n * 0.37) % 1, (self._n * 0.61) % 1)
        elif shift is False: sh = None
        else: sh = shift
        e = el(fr, to, tex, pv, rot, uv, faces, light, shift=sh)
        self._els[part].append(e)
        M, o = _rotm(rot)
        for x in (fr[0], to[0]):
            for y in (fr[1], to[1]):
                for z in (fr[2], to[2]):
                    v = (x, y, z)
                    if M:
                        d = [v[i] - o[i] for i in range(3)]
                        v = tuple(sum(M[i][k] * d[k] for k in range(3)) + o[i] for i in range(3))
                    self._pts[part].append(v)
        return e

    def seg(self, part, A, B, w, h, tex, up=(0.0, 1.0, 0.0), ext=0.0, light=0, full=False, shift=None):
        self._n += 1
        sh = None if full or shift is False else (shift or ((self._n * 0.37) % 1, (self._n * 0.61) % 1))
        e = _seg(A, B, w, h, tex, self.PIVOT[part], up, ext, light, shift=sh)
        if full:
            for f in e['faces'].values(): f['uv'] = [0, 0, 16, 16]
        self._els[part].append(e)
        for v in (A, B): self._pts[part].append(tuple(v))
        return e

    def skin(self, suffix, swap):
        """a model set named <part><suffix>: these textures swapped for others (names without the prefix)"""
        self._skins[suffix] = dict(swap)

    def count(self):
        return sum(len(v) for v in self._els.values())

    # ---- what rigkit / draftkit / phase134 read
    def HIDDEN(self, p, pose):
        if not self._els[p] or p in pose.get('_hide', ()): return True          # (a bare joint - the root of the slices - has no model)
        return p in self.OPT and p not in pose.get('_show', ())

    def model_name(self, p, pose=None, suffix=''):
        face = f'_x{pose["_face"]}' if pose and p in self.FACE_PARTS and pose.get('_face') else ''
        return f'{self.PREFIX}{p}{face}{suffix}'

    def textures(self):
        return {f'{self.PREFIX}{k}': (v() if callable(v) else v) for k, v in self._tex.items()}

    def models(self):
        out = {}
        for suffix, swap in [('', {})] + list(self._skins.items()):
            for p in self.PARTS:
                variants = [('', None)] + ([(f'_x{f}', f) for f in self.FACES] if p in self.FACE_PARTS else [])
                for vs, face in variants:
                    els = []
                    for e in self._els[p]:
                        fcs = {}
                        for k, fc in e['faces'].items():
                            t = fc['texture'][1:]
                            if t in TOKENS:
                                t = t.lower() if face is None else f'{t.lower()}_{face}'
                                if f'{t}' not in self._tex and face is not None: t = t.rsplit('_', 1)[0]   # (no such expression: the rest face)
                            t = swap.get(t, t)
                            fcs[k] = dict(fc, texture='#' + self.PREFIX + t)
                        els.append(dict(e, faces=fcs))
                    for e in els:
                        for v in e['from'] + e['to']: assert -16 <= v <= 32, (self.PREFIX, p, e['from'], e['to'])
                    used = sorted({fc['texture'][1:] for e in els for fc in e['faces'].values()})
                    if not els: continue
                    out[f'{self.PREFIX}{p}{vs}{suffix}'] = ({t: f'bm:block/{t}' for t in used}, els)
        return out

    # ---- poses
    def world_pts(self, pose):
        xf = solve(self.PIVOT, self.PARENT, pose)
        out = []
        for p in self.PARTS:
            if self.HIDDEN(p, pose): continue
            q, t = xf[p]; pv = D(self.PIVOT[p])
            for v in self._pts[p]:
                r = qrot(q, tuple(D(v)[i] - pv[i] for i in range(3)))
                w = tuple(pv[i] + t[i] + r[i] for i in range(3))
                out.append((-w[0], w[1], -w[2]))           # (back to design axes)
        return out

    def ground(self, pose, lift=0.0, dx=0.0, dz=0.0):
        pose = dict(pose); o = pose.pop('_off', (0.0, 0.0, 0.0))
        low = min(v[1] for v in self.world_pts(pose))
        pose['_off'] = (o[0] + dx, round(lift - low, 3), o[2] + dz)
        return pose

    def fit(self, pose=None):
        pts = self.world_pts(pose or self.POSES['idle_a']); U = self.RIG_SCALE / 16
        lo = [min(p[i] for p in pts) * U for i in range(3)]; hi = [max(p[i] for p in pts) * U for i in range(3)]
        return (round(lo[1], 3), round(hi[1] - lo[1], 3), round(lo[0], 3), round(hi[0], 3), round(lo[2], 3), round(hi[2], 3))


# ---------------------------------------------------------------------------------------------------- shapes (v1, kept)
def rounded(rig, part, c, r, h, tex, n=3, top_tex=None, light=0):
    """a squat round drum: n boxes turned about y, crossed (v1 - slab() / stack() read rounder and cleaner)"""
    x, y, z = c
    for i in range(n):
        a = 90.0 / n * i
        e = rig.box(part, (x - r, y, z - r * 0.42), (x + r, y + h, z + r * 0.42), tex, rot=('y', a, c) if a else None, light=light)
        e2 = rig.box(part, (x - r * 0.42, y, z - r), (x + r * 0.42, y + h, z + r), tex, rot=('y', a, c) if a else None, light=light)
        if top_tex:
            for ee in (e, e2): ee['faces']['up']['texture'] = '#' + top_tex
    return rig


def blob(rig, part, c, r, tex, k=(1.0, 1.0, 1.0), light=0):
    """a rounded lump: three crossed boxes (a ball read blocky)"""
    x, y, z = c; a, b, d = r * k[0], r * k[1], r * k[2]
    rig.box(part, (x - a, y - b * 0.62, z - d * 0.62), (x + a, y + b * 0.62, z + d * 0.62), tex, light=light)
    rig.box(part, (x - a * 0.62, y - b, z - d * 0.62), (x + a * 0.62, y + b, z + d * 0.62), tex, light=light)
    rig.box(part, (x - a * 0.62, y - b * 0.62, z - d), (x + a * 0.62, y + b * 0.62, z + d), tex, light=light)
    return rig


# ---------------------------------------------------------------------------------------------------- shapes (v2)
def slab(rig, part, y0, y1, hw, tex, hd=None, c=(0.0, 0.0), k=0.72, light=0, faces=None, top=None, shift=None, rot=None):
    """one rounded slab: a box with its four corners cut (three boxes, none overlapping) - an octagon from above (the Dryad's
    cap). hd: its half-depth (an oval); top: another texture on its up face (icing on a tier, moss on a stump)"""
    x, z = c; hd = hw if hd is None else hd
    s = shift
    es = [rig.box(part, (x - hw, y0, z - hd * k), (x + hw, y1, z + hd * k), tex, light=light, faces=faces, shift=s, rot=rot),
          rig.box(part, (x - hw * k, y0, z - hd), (x + hw * k, y1, z - hd * k), tex, light=light, faces=faces, shift=s, rot=rot),
          rig.box(part, (x - hw * k, y0, z + hd * k), (x + hw * k, y1, z + hd), tex, light=light, faces=faces, shift=s, rot=rot)]
    if top:
        for e in es:
            if 'up' in e['faces']: e['faces']['up']['texture'] = '#' + top
    return es


def stack(rig, part, rows, tex, c=(0.0, 0.0), k=0.72, light=0, top=None, shift=None, rot=None):
    """slabs stacked: rows of (y0, y1, half-width[, half-depth[, tex]]) - a dome, a trunk, a tier, a burl"""
    out = []
    for r in rows:
        y0, y1, hw = r[:3]; hd = r[3] if len(r) > 3 and r[3] is not None else hw; t = r[4] if len(r) > 4 else tex
        out += slab(rig, part, y0, y1, hw, t, hd, c, k, light, top=top, shift=shift, rot=rot)
    return out


def profile(y0, h, r, n=6, squash=1.0, lo=0.0, hi=1.0, d=None, power=1.0):
    """rows for stack(): n slabs of a ball / dome between lo..hi of its height (0 = bottom, 1 = top), r its radius, d its
    half-depth ratio; power > 1 fattens it (a mushroom / a canopy), < 1 slims it"""
    rows = []
    for i in range(n):
        a, b = lo + (hi - lo) * i / n, lo + (hi - lo) * (i + 1) / n
        m = (a + b) / 2; t = 2 * m - 1
        w = r * (max(0.0, 1 - t * t) ** (0.5 / power)) * squash
        rows.append((y0 + h * a, y0 + h * b, max(0.25, w), max(0.25, w * (d or 1.0))))
    return rows


def ball(rig, part, c, r, tex, n=5, ry=None, d=1.0, light=0, top=None, shift=None, power=1.0):
    """a rounded ball: stacked octagon slabs (reads round from any side - far better than crossed boxes)"""
    ry = ry or r
    return stack(rig, part, profile(c[1] - ry, 2 * ry, r, n, d=d, power=power), tex, (c[0], c[2]), light=light, top=top, shift=shift)


def leaf(rig, part, A, B, w, tex, up=(0.0, 1.0, 0.0), t=0.28, light=0, tipw=0.34, full=False):
    """a tapered leaf from A (its stem end) to B (its tip): three segs - narrow at the stem, widest at 40%, a point at the tip"""
    P = lambda s: tuple(A[i] + (B[i] - A[i]) * s for i in range(3))
    return [rig.seg(part, P(0.0), P(0.3), w * 0.62, t, tex, up, light=light, full=full),
            rig.seg(part, P(0.28), P(0.72), w, t, tex, up, light=light, full=full),
            rig.seg(part, P(0.7), P(1.0), w * tipw, t, tex, up, light=light, full=full)]


def cleaf(rig, part, A, d, L, w, tex, droop=0.25, t=0.3, up=(0.0, 1.0, 0.0), light=0, full=True, n=3, tipw=0.3, base=0.5):
    """a curved leaf: from A along direction d for length L, its tip drooping by droop*L (gravity); widest a third of the way
    out, a point at the tip. A blade() texture on full uv puts the vein down its middle"""
    m = math.sqrt(sum(v * v for v in d)); u = tuple(v / m for v in d)
    pts = [tuple(A[i] + u[i] * L * s - (droop * L * s * s if i == 1 else 0.0) for i in range(3)) for s in [k / n for k in range(n + 1)]]
    ws = [w * base] + [w * (1.0 - 0.55 * max(0.0, (k / n) - 0.35) / 0.65) for k in range(1, n)] + [w * tipw]
    out = []
    for i in range(n):
        out.append(rig.seg(part, pts[i], pts[i + 1], (ws[i] + ws[i + 1]) / 2, t, tex, up, ext=0.08, light=light, full=full))
    return out


def chain(rig, part, pts, ws, tex, hs=None, up=(0.0, 1.0, 0.0), ext=0.12, light=0, texs=None):
    """tapered segs along a path (a root, a tail, a serpent's body): pts, a width per point (and a height per point)"""
    out = []
    for i in range(len(pts) - 1):
        w = (ws[i] + ws[i + 1]) / 2; h = ((hs[i] + hs[i + 1]) / 2) if hs else w
        out.append(rig.seg(part, pts[i], pts[i + 1], w, h, texs[i] if texs else tex, up, ext=ext, light=light))
    return out


def ring(rig, part, c, r, n, w, h, tex, plane='xz', light=0, a0=0.0, arc=360.0, ext=0.12):
    """n boxes round a circle (a collar, a crown, a halo, a cage hoop) - plane 'xz' (flat) or 'xy' (upright, facing front)"""
    pts = []
    for k in range(n + 1):
        a = math.radians(a0 + arc * k / n)
        pts.append((c[0] + r * math.cos(a), c[1], c[2] + r * math.sin(a)) if plane == 'xz' else (c[0] + r * math.cos(a), c[1] + r * math.sin(a), c[2]))
    upv = (0.0, 1.0, 0.0) if plane == 'xz' else (0.0, 0.0, -1.0)
    return [rig.seg(part, pts[k], pts[k + 1], w, h, tex, upv, ext=ext, light=light) for k in range(n)]


def mirror(fn):
    """call fn(sx) for her right (+1) and left (-1)"""
    return [fn(1), fn(-1)]

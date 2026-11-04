"""(3.1 draft, stage 1: art only - not wired) TALUS, THE MOSSBACK TITAN - follower 62, the Kaiju trio's ape (the design:
scratchpad/design_kaiju.md). An ORIGINAL colossal ape: a mountain that got up and walked.

The owner: "Every Godzilla needs a rival. Let's do King Kong and King Ghidorah inspired followers to complete the Kaiju trio...
they should be just as large, with companion size options."

WHO  Talus slept for an age as a mountainside in the deep jungle - granite under a pelt of moss, an amethyst geode for a heart.
     The Atomic Rex's roar shook it awake. It is not a gorilla in a costume: it is GEOLOGY that learned to be an ape.
LOOK (every choice made to read at 8 blocks and to be nobody else's ape)
       - THE STANCE: a knuckle-walker. Its idle is on all fours - huge arms planted, the shoulders a ridge high over the hips,
         the head slung LOW and forward under the brow line of the shoulders. It rears upright only to roar, beat its chest,
         pound or throw - so its silhouette is a MOUNTAIN RANGE, not a man (the Atomic Rex is the upright one of the three).
       - THE PELT: deep moss green, shaggy, in clumps (strands(), lit in the middle, dark at the partings), thickest over the
         shoulders, the hump and the forearms; hanging fringes (cleaf locks) off the arms, the cheeks and the chin.
       - THE STONE: granite skin, warm grey, where an ape is bare - the face, the chest's two great slabs, the belly, the
         palms and knuckles, the feet - set in proud of the fur (a lip of a slab), cracked in structured seams, never speckle.
       - THE GEODE: AMETHYST. Two RIDGES of violet crystals stand along its shoulders (the mountain range: the biggest
         at the shoulders, smaller toward the hips), leaving a mossy hollow between them down the spine - the SADDLE sits
         there, like a pass between peaks. Crystal veins glow in the chest slabs and the forearm bracers; a small cluster on
         the crown and on each forearm (accents in purposeful clusters). Its eyes are geode light deep in stone sockets.
       - THE FACE: a stone mask - a heavy overhanging brow ledge, deep-set violet eyes, a broad flat nose, wide cheek
         FLANGES fringed with moss (it is old), and two stone TUSKS rising from the lower jaw beside the muzzle. A violet
         glow in the throat when it roars.
SCALE  RIG_SCALE 2.6: ~8.1 blocks to the crystal peaks in its knuckle stance (the Atomic Rex: 7.8 to its plates), ~9.5 reared
       up to roar. COMPANION 0.83 (~2.6 blocks): compsize twins the rig at COMPANION / RIG_SCALE, as the Rat King's (the hitbox
       follows). RIDDEN: SEAT_PT on 'saddle'; in 'ride' the seat is (0, 7.07, 1.56) blocks - a horse host at scale 4.90.
RIG    body (root: the hips and pot belly) - chest (the barrel chest, shoulders and hump) - ridge (the crystal ridges: its
       charged model '_ch' lights them for the chest-beat and the Rank III) - head (face part) - jaw - armr / forer / handr,
       arml / forel / handl - thighr / shinr / footr, thighl / shinl / footl - saddle (the moss saddle, rideable). fx (opt):
       'boulder' (a BLOCK-COPY boulder held overhead - in game block_display COPIES of the ground it tore up, never real
       blocks), 'quake' (the ground pound's ring of cracked copies and dust), 'beatfx' (the chest-beat's violet war-drum rings),
       'impact' (a punch's burst), 'aura' (the rare aura: GEODE HEART - crystals orbit it).
SKINS  '_au' AUTUMN MOSS (the cosmetic: rust and gold moss, citrine crystals), '_sn' SNOWCAP (the cosmetic: a white winter
       pelt, ice-blue crystals), '_sh' SHINY "Living Jade" (jade-green stone, pink rose-quartz crystals, a sunrise pelt),
       '_ch' the ridge charged, '_g' an afterimage (the flurry's arm blur)."""
import math
import random
from PIL import Image, ImageDraw
from fol5_kit import (Rig, hexc, mix, mul, limb, T, cells, soft, lit, glow, put, strands, foliage, slab, stack, profile, cleaf, leaf,
                      chain, ring, ghost, recolor, _ell, _rim, _curve, _thick, _vee, stroke, planks, alpha)
import rigkit
from rigkit import qs, qmul

# ---------------------------------------------------------------------------------------------------- the rig
PIVOT = {'body': (0, 17.0, 3.0), 'chest': (0, 26.0, 2.0), 'ridge': (0, 44.0, 6.0), 'head': (0, 41.0, -6.0), 'jaw': (0, 40.6, -9.0),
         'armr': (14.0, 37.0, 0.0), 'forer': (15.2, 24.0, -0.6), 'handr': (15.4, 13.4, -1.4),
         'arml': (-14.0, 37.0, 0.0), 'forel': (-15.2, 24.0, -0.6), 'handl': (-15.4, 13.4, -1.4),
         'thighr': (7.0, 17.0, 3.0), 'shinr': (7.6, 9.0, 2.4), 'footr': (7.8, 2.6, 3.0),
         'thighl': (-7.0, 17.0, 3.0), 'shinl': (-7.6, 9.0, 2.4), 'footl': (-7.8, 2.6, 3.0),
         'saddle': (0, 44.0, 4.0), 'boulder': (0, 60.0, -2.0), 'beatfx': (0, 32.0, -10.0), 'quake': (0, 0.0, -24.0),
         'impact': (0, 30.0, -30.0), 'aura': (0, 24.0, 0.0)}
PARENT = {'body': None, 'chest': 'body', 'ridge': 'chest', 'head': 'chest', 'jaw': 'head',
          'armr': 'chest', 'forer': 'armr', 'handr': 'forer', 'arml': 'chest', 'forel': 'arml', 'handl': 'forel',
          'thighr': 'body', 'shinr': 'thighr', 'footr': 'shinr', 'thighl': 'body', 'shinl': 'thighl', 'footl': 'shinl',
          'saddle': 'chest', 'boulder': 'chest', 'beatfx': 'chest', 'quake': None, 'impact': None, 'aura': None}
FACES = ('fierce', 'roar', 'blink', 'happy', 'hurt', 'sleepy', 'look')
OPT = ('boulder', 'quake', 'beatfx', 'impact', 'aura')
RIG_SCALE = 2.6
COMPANION = 0.83
R = Rig('tl_', RIG_SCALE, PIVOT, PARENT, FACES, face_part='head', opt=OPT, companion=COMPANION)
SKIN_NAMES = {'_au': 'cosmetic: Autumn Moss', '_sn': 'cosmetic: Snowcap', '_sh': 'SHINY: Living Jade', '_ch': 'the ridge charged', '_g': 'afterimage'}
ARMS = ('armr', 'forer', 'handr', 'arml', 'forel', 'handl')

# ---------------------------------------------------------------------------------------------------- palette
FUR = dict(part='#13220d', dark='#203a17', base='#325426', light='#4a7434', shine='#76a246', tip='#9cc05a')
FUR2 = dict(part='#0e180a', dark='#172c12', base='#22401b', light='#335a26', shine='#4f7c36', tip='#6a9a44')
STONE = dict(deep='#2a2726', dark='#46413e', base='#67615c', light='#857e76', shine='#a49b91', fleck='#8a6e62')
AME = dict(deep='#2e0f52', dark='#5a2294', base='#8e44d0', light='#bf86f2', core='#f2dcff')
TUSK = dict(dark='#857c68', base='#b9ae94', light='#dad0b8', shine='#f2ead6')


# ---------------------------------------------------------------------------------------------------- textures (64 px, 2-px cells)
def granite(P, seed, cracks=5, flecks=True):
    """granite skin: broad soft tone patches (a 6 x 6 patch field, never a per-cell coin-flip), a few structured CRACKS (a dark seam
    with a lit lip above it, wandering and branching), feldspar flecks in three tiny 2-cell clusters"""
    rnd = random.Random(seed); C = {}
    for _ in range(cracks):
        x, y = rnd.randrange(32), rnd.randrange(32); dx = rnd.choice((-1, 1))
        for i in range(rnd.randint(5, 11)):
            C[(x % 32, y % 32)] = 'd'
            C.setdefault((x % 32, (y - 1) % 32), 'l')
            if rnd.random() < 0.55: x += dx
            else: y += rnd.choice((-1, 1))
            if rnd.random() < 0.15: dx = -dx
    F = set()
    if flecks:
        for _ in range(3):
            x, y = rnd.randrange(32), rnd.randrange(32); F |= {(x, y), ((x + 1) % 32, y)}
    pr = random.Random(seed * 3 + 1); pt = [[pr.random() for _ in range(7)] for _ in range(7)]
    def c(x, y, r):
        k = C.get((x, y))
        if k == 'd': return P['deep'] if (x + y) % 4 else P['dark']
        if k == 'l': return mix(P['base'], P['light'], 0.6)
        if (x, y) in F: return P['fleck']
        v = pt[y * 6 // 32][x * 6 // 32] * 0.6 + pt[(y * 6 // 32 + 1) % 7][(x * 6 // 32 + 1) % 7] * 0.4
        if v < 0.3: return mix(P['base'], P['dark'], 0.32)
        if v > 0.72: return mix(P['base'], P['light'], 0.35)
        return P['base']
    return cells(c, seed)


def shag(P, seed, w=4, h=5):
    """a shaggy pelt (the bar for fur at kaiju scale): rows of pointed TUFTS, w cells wide and h tall, each row offset half a
    tuft - lit across its root, the base down its middle, its point hanging over the shadowed gap of the row below, a soft
    parting down one edge. Low contrast: it reads as fur at 8 blocks, not as stripes"""
    rnd = random.Random(seed); off = [rnd.randrange(w) for _ in range(40)]
    lt, dk = mix(P['base'], P['light'], 0.55), mix(P['base'], P['dark'], 0.6)
    def c(x, y, r):
        row = y // h; k = y % h; tx = (x + off[row % 40] + (row % 2) * (w // 2)) % w
        if k == h - 1: return dk if tx in (0, w - 1) else mix(P['base'], P['dark'], 0.25)
        if k == 0: return lt if 0 < tx < w - 1 else P['base']
        if tx == 0 and 0 < k < h - 2: return mix(P['base'], P['dark'], 0.4)
        if k == 1 and tx == 1: return P['light']
        return P['base']
    return cells(c, seed)


def crystal(P, seed, charged=False):
    """amethyst faceted crystal: facet columns (lit, base, shaded, base) with a bright edge line between them, a ramp from a dark
    root (row 31) to a bright tip (row 0), a few glints along the edges - light_emission does the rest"""
    pal = (P['deep'], P['dark'], P['base'], P['light'], P['core'])
    def c(x, y, r):
        f = (x // 8) % 4; e = x % 8 == 0
        t = 1 - y / 31
        lv = [1, 2, 0, 1][f] + t * 2.2 + (0.6 if charged else 0)
        if e: lv += 1.4
        if (x * 7 + y * 3) % 23 == 0 and t > 0.3: lv += 1.5
        return pal[max(0, min(4, int(lv)))]
    return cells(c, seed)


def vein(P):
    return cells(lambda x, y, r: P['core'] if (x + y) % 9 < 3 else P['light'], 0)


def mossmat(seed, P=FUR):
    return foliage((P['dark'], P['base'], P['light'], P['tip']), seed, step=4)


def mouth_tex():
    def c(x, y, r):
        if y % 8 == 0: return '#4a1a5a'
        return '#24081e' if (x // 4 + y // 8) % 2 else '#2c0c26'
    return cells(c, 0)


def tusk_tex(P=TUSK):
    def c(x, y, r):
        if x % 10 == 0: return P['dark']
        if y < 4: return P['shine']
        if y % 9 == 4: return P['dark']
        return P['light'] if x % 10 < 4 else P['base']
    return cells(c, 1)


def leather(seed):
    """the saddle's pad: moss-felt and worn leather, stitched"""
    def c(x, y, r):
        if y in (2, 29) and x % 3 == 0: return '#d8c090'
        if y < 2: return '#7a5a3a'
        if y > 29: return '#2e2014'
        return '#5a3e26' if (x // 6 + y // 5) % 5 else '#4a3220'
    return cells(c, seed)


def bamboo(seed):
    def c(x, y, r):
        if y % 12 == 0: return '#5a6a2a'
        if y % 12 == 1: return '#c8d880'
        return '#9aae4a' if x % 8 < 5 else '#7a8e3a'
    return cells(c, seed)


def vine(seed):
    return strands(('#1a2a0c', '#2e4a16', '#3e6420', '#567e2c', '#7aa040'), seed, sheen=(12, 14), clump=(2, 3))


def flower(col):
    def c(x, y, r):
        d = max(abs(x - 15.5), abs(y - 15.5))
        if d < 3: return '#ffe070'
        if (x + y) % 2 == 0 and d < 13: return col
        return mix(col, '#ffffff', 0.25) if d < 13 else None
    return cells(c, 0)


# ---- the eyes: GEODE LIGHT deep in stone sockets (its own eye language - not the Cairn's inlaid gem, not an anime eye)
def geode_eye(im, cx, cy, w, h, flip=False, kind=None, P=AME, sock='#120a12', glow_=None):
    """a deep-set eye: a dark socket in the stone, and in it a small FIERCE iris of violet light, graded from a dim rim to a
    white-hot core, a hard facet glint; the lid line is the brow's own shadow. kinds: None (heavy, watchful), 'fierce' (the
    brow's shadow cuts in toward the nose: a glare), 'roar' (wide, the light flared), 'blink' (a lit seam), 'happy' (crinkled up
    from below: the light a sliver), 'hurt' (> < squeezed), 'sleepy' (lidded low, dim), 'look' (the iris slid to the side)"""
    o = 1 if flip else -1
    if kind == 'hurt':
        S = _vee(cx, cy, w - 1, h - 1, flip); stroke(im, S, P['light'], sock, n8=True); return
    if kind == 'happy':                                                          # (crinkled up from below: two glowing ^ arcs)
        S = _thick(_curve(cx, round(cy) + 2, w, max(2, h // 3)), 2)
        for x, y in _rim(S, True): put(im, x, y, sock)
        for x, y in S: put(im, x, y, P['light'] if abs(x + 0.5 - cx) > w * 0.2 else P['core'])
        return
    if kind == 'blink':
        S = _curve(cx, round(cy) + 1, w, -1); stroke(im, _thick(S, 2), sock)
        for x, y in S:
            if abs(x + 0.5 - cx) < w * 0.3: put(im, x, y, P['base'])
        return
    sw = w / 2 + (0.6 if kind == 'roar' else 0); sh = h / 2 + (0.5 if kind == 'roar' else 0)
    S = _ell(cx, cy, sw, sh)
    inner = lambda x: max(-1.0, min(1.0, (x + 0.5 - cx) / (w / 2) * (-o)))       # (+1 toward the nose)
    lid = {None: 0.38, 'fierce': 0.30, 'roar': 0.05, 'happy': 0.62, 'sleepy': 0.66, 'look': 0.36}.get(kind, 0.38)
    slant = {'fierce': 2.2, 'roar': -0.4, 'happy': -0.6}.get(kind, 0.4)
    top = min(y for _, y in S)
    L = lambda x: top + lid * (2 * sh) + slant * inner(x)
    for x, y in _rim(S): put(im, x, y, mix(sock, STONE['dark'], 0.5))
    for x, y in S: put(im, x, y, sock)
    V = {(x, y) for x, y in S if y + 0.5 >= L(x)}
    if kind == 'happy':
        V = {(x, y) for x, y in V if y + 0.5 <= cy + sh * 0.5}
    shift = 0.0 if kind != 'look' else o * w * 0.22
    ir = (w * (0.34 if kind != 'roar' else 0.42)); ih = h * (0.42 if kind != 'roar' else 0.5)
    icx, icy = cx + shift, cy + h * 0.08
    I = {(x, y) for x, y in V if ((x + 0.5 - icx) / ir) ** 2 + ((y + 0.5 - icy) / ih) ** 2 <= 1}
    ramp = (P['deep'], P['dark'], P['base'], P['light'], P['core']) if kind != 'sleepy' else (P['deep'], P['deep'], P['dark'], P['base'], P['base'])
    for x, y in I:
        d = math.hypot((x + 0.5 - icx) / ir, (y + 0.5 - icy) / ih)
        c = ramp[min(4, int((1 - d) * 5.2))]
        put(im, x, y, c)
        if glow_ is not None: glow_.putpixel((x, y), hexc(c))
    if I and kind != 'sleepy':
        gx = round(icx - ir * 0.45); gy = min(y for _, y in I) + 1
        if (gx, gy) in I: put(im, gx, gy, '#ffffff')
    # the lid line: the brow's shadow over the eye (a hard dark edge)
    for x in range(int(cx - sw) - 1, int(cx + sw) + 2):
        y = math.floor(L(x))
        if (x, y) in S or (x, y + 1) in S: put(im, x, y, '#060306')


def eyes_tex(kind=None, P=AME):
    """the EYES overlay on the face's north face: a 64 x 20 window (uv 16 x 4.9 on a 9.2 x 2.8 unit box), both eyes"""
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    geode_eye(im, 17, 10, 18, 11, False, kind, P)
    geode_eye(im, 47, 10, 18, 11, True, kind, P)
    return im


def ring_tex(col, a=210):
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for r, w, c in ((30, 3, mix(col, '#ffffff', 0.5)), (25, 2, col), (20, 1, mix(col, '#000000', 0.2))):
        d.ellipse((32 - r, 32 - r, 32 + r, 32 + r), outline=hexc(c, a), width=w)
    return im


def burst_tex():
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i in range(8):
        a = math.radians(i * 45 + 22.5); r = 30 if i % 2 else 20
        d.polygon([(32, 32), (32 + r * math.cos(a - 0.22), 32 + r * math.sin(a - 0.22)), (32 + r * 1.1 * math.cos(a), 32 + r * 1.1 * math.sin(a)),
                   (32 + r * math.cos(a + 0.22), 32 + r * math.sin(a + 0.22))], fill=hexc('#f2dcff' if i % 2 else '#bf86f2', 230))
    d.ellipse((22, 22, 42, 42), fill=hexc('#ffffff', 240))
    return im


def dust_tex():
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); px = im.load()
    for y in range(64):
        for x in range(64):
            d = math.hypot(x - 31.5, y - 31.5) / 32
            if d < 1: px[x, y] = hexc(mix('#c8bca8', '#8a8070', d), int(200 * (1 - d) ** 0.6))
    return im


def _tex(F=FUR, F2=FUR2, S=STONE, A=AME, tk=TUSK, sfx=''):
    t = {'fur': shag(F, 11), 'fur2': shag(F2, 12, w=3, h=4),
         'fringe': strands((F['part'], F['dark'], F['base'], F['light'], F['tip']), 13, sheen=(18, 21), clump=(3, 5)),
         'moss': mossmat(14, F),
         'stone': granite(S, 21), 'stone2': granite(S, 22, cracks=7), 'stone_l': lit(granite(S, 23, cracks=2), 1.16, 0.9, 10),
         'stone_d': granite(dict(S, base=S['dark'], light=S['base'], dark=S['deep']), 24, cracks=3, flecks=False),
         'crys': crystal(A, 31), 'crys_c': crystal(A, 32, charged=True), 'vein': vein(A),
         'tusk': tusk_tex(tk), 'mouth': mouth_tex(), 'nail': cells(lambda x, y, r: S['deep'] if y > 24 else '#3a3532', 0),
         'eyes': eyes_tex(None, A)}
    for f in FACES: t[f'eyes_{f}'] = eyes_tex(f, A)
    return t


TEX = _tex()
TEX.update({'leather': leather(41), 'bamboo': bamboo(42), 'vine': vine(43), 'brass': lit(cells(lambda x, y, r: '#b08a3a' if (x + y) % 7 else '#d8b05a', 0), 1.3, 0.8, 6),
            'leaf': foliage(('#1e4412', '#2e6a1c', '#46902a', '#78c040'), 44, step=3), 'berry': glow(['#fff4b0', '#ffd040', '#e09010', '#a05a08']),
            'bloom': flower('#e070b0'), 'rock': granite(STONE, 51, cracks=6), 'rock2': granite(dict(STONE, base='#5c5650'), 52, cracks=4),
            'dirt': soft('#6a4a2e', '#7e5a3a', '#523a24', 53), 'grass': soft('#5a8a3a', '#6e9e48', '#4a7430', 54),
            'ring': ring_tex(AME['light']), 'burst': burst_tex(), 'dust': dust_tex(),
            'aura': glow([AME['core'], AME['light'], AME['base'], AME['dark']], alpha=[230, 200, 150, 0])})
for k, v in TEX.items(): R.tex(k, v)
LIGHT_TEX = {'crys': 12, 'crys_c': 15, 'vein': 13, 'berry': 10, 'mouth': 4}

# ---------------------------------------------------------------------------------------------------- helpers (on this rig)
B = R.box
SEG = R.seg


def L_(tex, light=None):
    return LIGHT_TEX.get(tex, 0) if light is None else light


def oct_(part, y0, y1, hw, hd, tex, c=(0.0, 0.0), k=0.7, top=None, light=0):
    """an octagon slab (slab()), its wide boxes split in two down the middle when wider than 16 units (so the texture keeps
    its 4 texels a unit on a kaiju-sized mass instead of stretching)"""
    x, z = c
    out = []
    def bx(x0, x1, z0, z1):
        if x1 - x0 > 16.0:
            m = (x0 + x1) / 2
            return [B(part, (x0, y0, z0), (m, y1, z1), tex, light=light), B(part, (m, y0, z0), (x1, y1, z1), tex, light=light)]
        return [B(part, (x0, y0, z0), (x1, y1, z1), tex, light=light)]
    out += bx(x - hw, x + hw, z - hd * k, z + hd * k)
    out += bx(x - hw * k, x + hw * k, z - hd, z - hd * k)
    out += bx(x - hw * k, x + hw * k, z + hd * k, z + hd)
    if top:
        for e in out: e['faces']['up']['texture'] = '#' + top
    return out


def mass(part, rows, tex, c=(0.0, 0.0), k=0.7, top=None):
    out = []
    for r in rows:
        out += oct_(part, r[0], r[1], r[2], r[3], r[4] if len(r) > 4 else tex, c, k, top=top)
    return out


def rod(part, pts, ws, tex, front=(0.0, 0.0, -1.0), k=0.78, ext=0.2, light=0):
    """a limb: along pts, two crossed boxes per span (an octagon in section) so it reads round"""
    f2 = (0.7, 0.0, -0.7) if abs(front[0]) < 0.5 else (0.7, 0.0, 0.7)
    out = []
    for i in range(len(pts) - 1):
        w = (ws[i] + ws[i + 1]) / 2
        out.append(SEG(part, pts[i], pts[i + 1], w, w, tex, front, ext=ext, light=light))
        out.append(SEG(part, pts[i], pts[i + 1], w * k * 1.12, w * k * 1.12, tex, f2, ext=ext * 0.4, light=light))
    return out


def crystal_spike(part, base, tip, w, tex='crys', light=None, n=3):
    """an amethyst crystal: a hexagonal prism (two crossed boxes) rising from base, its last third a point - the core lighter"""
    P = lambda s: tuple(base[i] + (tip[i] - base[i]) * s for i in range(3))
    d = [tip[i] - base[i] for i in range(3)]
    up = (0.0, 0.0, -1.0) if abs(d[1]) > 0.6 * math.sqrt(sum(v * v for v in d)) else (0.0, 1.0, 0.0)
    lt = L_(tex, light)
    SEG(part, P(0.0), P(0.66), w, w, tex, up, ext=0.15, light=lt, full=True)
    SEG(part, P(0.0), P(0.62), w * 0.86, w * 0.86, tex, (0.7, 0.0, -0.7) if up[2] else (0.7, 0.7, 0.0), ext=0.1, light=lt, full=True)
    SEG(part, P(0.6), P(0.86), w * 0.62, w * 0.62, tex, up, light=lt, full=True)
    SEG(part, P(0.84), P(1.0), w * 0.28, w * 0.28, tex, up, light=lt, full=True)


def cluster(part, base, dirs, sizes, tex='crys', light=None):
    """a geode cluster: a few crystals from one root, splayed (accents in purposeful clusters)"""
    for d, (L, w) in zip(dirs, sizes):
        m = math.sqrt(sum(v * v for v in d)); u = [v / m for v in d]
        crystal_spike(part, base, tuple(base[i] + u[i] * L for i in range(3)), w, tex, light)


def lock(part, A, d, L, w, tex='fringe', droop=0.35, t=0.9):
    """a hanging lock of moss fur: a curved tapered strand (cleaf), thick enough to read at kaiju scale"""
    return cleaf(R, part, A, d, L, w, tex, droop=droop, t=t, full=False, n=3, tipw=0.35, base=0.8)


def mirror(fn):
    fn(1); fn(-1)


def capture(part, fn):
    """the elements fn() builds on a part, taken back off it (a face part's per-expression geometry - face_els)"""
    n, m = len(R._els[part]), len(R._pts[part])
    fn()
    els = R._els[part][n:]; del R._els[part][n:]; del R._pts[part][m:]
    return els


# ---------------------------------------------------------------------------------------------------- the body: hips and pot belly
mass('body', [(11.5, 14.5, 7.6, 6.4), (14.5, 18.5, 9.0, 7.2), (18.5, 22.5, 9.4, 7.4), (22.5, 26.5, 9.0, 7.0)], 'fur2', c=(0, 3.4))
mass('body', [(11.8, 14.4, 5.6, 4.6), (14.4, 18.6, 7.0, 5.6), (18.6, 22.8, 7.4, 5.8), (22.8, 26.0, 7.0, 5.4)], 'stone', c=(0, 0.6))   # (the belly: bare stone, proud)
for y0, y1 in ((15.0, 15.5), (19.0, 19.5), (23.0, 23.4)):                                    # (seams across it, a lit lip under each)
    B('body', (-5.4, y0, -5.4), (5.4, y1, -5.05), 'stone_d')
for sx in (1, -1):                                                                          # (the flanks' fur falling over the hips)
    lock('body', (sx * 8.6, 24.0, 2.0), (sx * 0.5, -1.0, 0.1), 8.0, 4.2, droop=0.05)
    lock('body', (sx * 7.4, 23.0, 8.6), (sx * 0.3, -1.0, 0.6), 7.0, 3.6, droop=0.05)
B('body', (-3.0, 14.0, 9.8), (3.0, 20.0, 10.8), 'fur2')                                     # (the rump)

# ---------------------------------------------------------------------------------------------------- the chest, shoulders and hump
mass('chest', [(25.0, 29.0, 10.6, 7.6), (29.0, 33.0, 12.6, 8.4), (33.0, 37.0, 14.0, 8.8), (37.0, 40.5, 14.2, 8.6), (40.5, 43.5, 12.0, 7.6)], 'fur', c=(0, 1.6))
mass('chest', [(33.0, 39.0, 10.0, 5.6), (39.0, 44.0, 9.4, 5.4), (44.0, 46.6, 7.0, 4.2)], 'fur', c=(0, 6.0), top='moss')      # (THE HUMP: high behind the shoulders)
for sx in (1, -1):
    stack(R, 'chest', profile(33.0, 9.4, 5.4, n=4), 'fur', c=(sx * 12.6, 0.4))               # (the shoulders' round deltoid masses)
    # THE CHEST'S TWO GREAT SLABS of stone, proud of the fur (a lip of slab), a crack-seam down the sternum between them
    for (x0, x1, y0, y1, z0, a) in ((0.8, 10.4, 30.0, 38.4, -8.9, 8), (1.4, 9.2, 26.6, 30.4, -8.2, 4)):
        lo, hi = sorted((sx * x0, sx * x1))
        B('chest', (lo, y0, z0), (hi, y1, z0 + 2.8), 'stone_l' if y0 > 29 else 'stone', rot=('y', -a * sx, (sx * x0, y0, z0)))
    lo, hi = sorted((sx * 1.2, sx * 10.0))
    B('chest', (lo, 38.2, -8.6), (hi, 39.0, -6.4), 'stone_d', rot=('y', -8 * sx, (sx * 0.8, 38.2, -8.9)))   # (the slab's top lip, shadowed)
    # crystal VEINS glowing in the slab - a branching seam, like lightning frozen in rock
    for (a_, b_) in (((2.6, 31.0), (4.0, 33.6)), ((4.0, 33.6), (3.4, 36.4)), ((4.0, 33.6), (7.2, 34.8)), ((7.2, 34.8), (8.4, 37.4)), ((3.4, 36.4), (5.0, 37.8))):
        A_ = (sx * a_[0], a_[1], -9.05 - 0.13 * a_[0]); B_ = (sx * b_[0], b_[1], -9.05 - 0.13 * b_[0])
        SEG('chest', A_, B_, 0.55, 0.3, 'vein', up=(0.0, 0.0, -1.0), light=13, full=True)
    # fur fringe over the slabs' outer edges and under the arms
    lock('chest', (sx * 10.8, 38.6, -6.0), (sx * 0.25, -1.0, -0.15), 8.6, 3.8, droop=0.05)
    lock('chest', (sx * 12.2, 30.0, -2.0), (sx * 0.2, -1.0, 0.0), 6.8, 3.6, droop=0.05)
B('chest', (-0.7, 27.0, -8.7), (0.7, 38.0, -7.6), 'stone_d')                                  # (the sternum seam)
B('chest', (-5.6, 40.6, -6.6), (5.6, 43.2, -2.6), 'fur')                                      # (the nape, where the head sits low)
# three glow-berries on vines at the left shoulder: a purposeful little cluster (the jungle still grows on it)
for k, (dx, dy, dz) in enumerate(((0.0, 0.0, 0.0), (1.1, -1.6, 0.4), (-0.8, -2.6, -0.2))):
    c = (-13.8 + dx, 40.6 + dy, -3.8 + dz)
    SEG('chest', (c[0], c[1] + 1.4, c[2] + 0.4), c, 0.35, 0.35, 'vine')
    B('chest', (c[0] - 0.6, c[1] - 1.2, c[2] - 0.6), (c[0] + 0.6, c[1], c[2] + 0.6), 'berry', light=10, full=True)
B('chest', (11.6, 42.4, -2.6), (13.2, 42.9, -1.0), 'bloom', faces=('up',), full=True)            # (and one small bloom on the right)

# ---------------------------------------------------------------------------------------------------- THE RIDGES: the geode mountain range
RIDGE = [(-1.4, 13.0, 2.3, 24), (1.8, 11.2, 2.1, 20), (4.8, 9.0, 1.85, 17), (7.6, 7.0, 1.6, 15), (10.2, 5.0, 1.3, 13)]   # (z, length, width, splay)
for sx in (1, -1):
    for i, (z, Ln, w, spl) in enumerate(RIDGE):
        x = sx * (4.6 + i * 0.25); y = 46.0 - i * 1.3
        base = (x, y - 1.4, z)
        tip = (x + sx * Ln * math.sin(math.radians(spl)), y - 1.4 + Ln * math.cos(math.radians(spl)), z + Ln * 0.22)
        crystal_spike('ridge', base, tip, w * 1.6)
    # small ones at the big ones' roots (a geode cluster, not a fence)
    cluster('ridge', (sx * 6.6, 44.2, 0.6), [(sx * 0.8, 1.0, -0.3), (sx * 1.0, 0.6, 0.4)], [(3.6, 1.2), (3.0, 1.0)])
    cluster('ridge', (sx * 7.0, 41.2, 7.6), [(sx * 0.9, 1.0, 0.2), (sx * 0.4, 1.0, 0.8)], [(3.0, 1.0), (2.4, 0.9)])
    B('ridge', (sx * 3.8 - 1.4, 43.4, -2.4), (sx * 3.8 + 1.4, 45.8, 10.6), 'stone2')         # (the stone the ridge grows out of)

# ---------------------------------------------------------------------------------------------------- the head: a stone mask, slung low
HC = (0.0, -8.4)


def zoct(part, z0, z1, hw, hh, tex, c=(0.0, 0.0), k=0.68, light=0):
    """an octagon in the xy section, run along z (a muzzle, a brow, a snout): three boxes"""
    x, y = c
    return [B(part, (x - hw, y - hh * k, z0), (x + hw, y + hh * k, z1), tex, light=light),
            B(part, (x - hw * k, y + hh * k, z0), (x + hw * k, y + hh, z1), tex, light=light),
            B(part, (x - hw * k, y - hh, z0), (x + hw * k, y - hh * k, z1), tex, light=light)]


def head_geom(face=None):
    # the skull: a low dome of fur, sloping back into the nape (an ape's skull: the face juts, the crown is low)
    mass('head', [(40.2, 42.6, 5.2, 4.8), (42.6, 46.4, 6.0, 5.2), (46.4, 49.4, 5.6, 4.8), (49.4, 51.0, 4.2, 3.6)], 'fur', c=HC)
    SEG('head', (0, 50.6, -11.0), (0, 51.8, -4.6), 3.0, 2.4, 'fur', up=(0.0, 1.0, 0.0), ext=0.4)       # (the crest, a moss ridge)
    cluster('head', (0.6, 51.4, -6.0), [(0.3, 1.0, 0.6), (-0.7, 1.0, 0.3), (1.0, 0.7, 0.2)], [(4.2, 1.3), (3.2, 1.0), (2.4, 0.8)])
    # the face: a stone mask set in the fur - a recessed band where the eyes sit, under a heavy rounded brow
    B('head', (-5.2, 40.6, -14.0), (5.2, 48.0, -12.0), 'stone_d')                                      # (the mask's dark recess)
    tilt = {None: 4, 'fierce': 15, 'roar': -6, 'blink': 4, 'happy': -5, 'hurt': 11, 'sleepy': 1, 'look': 4}.get(face, 4)
    drop = {'fierce': 0.45, 'hurt': 0.35, 'roar': -0.5, 'sleepy': 0.3}.get(face, 0.0)
    for sx in (1, -1):                                                                                  # THE BROW LEDGE: two rounded halves
        r = ('z', -tilt * sx, (sx * 0.4, 48.4, -13.5))
        for (y0, y1, z0, z1, x1, tx) in ((47.5, 49.5, -15.4, -11.8, 5.9, 'stone_l'), (49.0, 50.4, -14.9, -11.4, 5.3, 'stone_l'), (50.0, 50.9, -14.3, -10.6, 4.7, 'fur')):
            lo, hi = sorted((sx * 0.0, sx * x1))
            B('head', (lo, y0 - drop, z0), (hi, y1 - drop, z1), tx, rot=r)
    B('head', (-4.6, 44.7, -14.12), (4.6, 47.5, -14.06), 'EYES', faces=('north',), uv={'north': [0, 0, 16, 4.9]}, light=10)
    # the muzzle: rounded, jutting, a broad flat nose on it, the nostrils flared
    zoct('head', -17.2, -13.6, 4.4, 2.2, 'stone_l', c=(0.0, 41.9))
    zoct('head', -17.8, -15.6, 3.0, 1.1, 'stone_l', c=(0.0, 43.4))                                     # (the nose)
    B('head', (-1.2, 44.0, -15.6), (1.2, 47.6, -13.8), 'stone')                                        # (the bridge, up to the brow)
    for sx in (1, -1):
        lo, hi = sorted((sx * 0.6, sx * 2.0)); B('head', (lo, 42.8, -17.85), (hi, 43.7, -17.75), 'nail')     # (nostrils)
        lo, hi = sorted((sx * 3.4, sx * 4.8)); B('head', (lo, 40.6, -16.0), (hi, 43.4, -13.0), 'stone')        # (the lip's corners)
    B('head', (-3.4, 39.9, -16.2), (3.4, 40.3, -9.0), 'mouth', light=4)                                 # (the mouth's roof, its glow)
    for i in range(6):                                                                                  # (the upper teeth)
        z = -15.8 + i * 1.0
        for sx in (1, -1):
            lo, hi = sorted((sx * 3.0, sx * 2.0)); B('head', (lo, 39.4, z), (hi, 40.2, z + 0.7), 'tusk')
    for sx in (1, -1):
        # THE CHEEK FLANGES: wide stone plates flaring out and forward, a moss fringe round their rims (it is old)
        r = ('y', 20 * sx, (sx * 4.8, 44.6, -12.4))
        lo, hi = sorted((sx * 4.8, sx * 8.4)); B('head', (lo, 41.4, -12.8), (hi, 47.6, -10.6), 'stone', rot=r)
        lo, hi = sorted((sx * 4.8, sx * 7.6)); B('head', (lo, 42.2, -13.2), (hi, 46.8, -12.6), 'stone_l', rot=r)
        lo, hi = sorted((sx * 8.2, sx * 8.9)); B('head', (lo, 41.6, -12.4), (hi, 47.8, -10.4), 'fringe', rot=r)
        for k, (y, L) in enumerate(((41.6, 6.4), (44.2, 5.0), (46.8, 3.8))):
            lock('head', (sx * 8.6, y, -11.0), (sx * 0.55, -1.0, -0.1), L, 2.2, droop=0.0, t=0.8)
        lo, hi = sorted((sx * 5.6, sx * 6.8)); B('head', (lo, 45.0, -8.4), (hi, 47.6, -6.2), 'stone_d')     # (ears)
    B('head', (-5.2, 40.6, -4.4), (5.2, 49.2, -1.6), 'fur')                                            # (the back of the head)


head_geom()
for f in FACES:
    R.face_els('head', f, capture('head', lambda f=f: head_geom(f)))

# ---- the jaw: tusks rising beside the muzzle, a moss beard
B('jaw', (-3.8, 37.4, -16.0), (3.8, 40.0, -9.0), 'stone')
B('jaw', (-3.0, 36.6, -15.4), (3.0, 37.6, -10.6), 'stone_d')                                         # (the chin)
B('jaw', (-3.0, 39.9, -15.6), (3.0, 40.2, -9.4), 'mouth', light=4)
for i in range(5):
    z = -15.2 + i * 1.1
    for sx in (1, -1): B('jaw', (min(sx * 2.6, sx * 1.7), 40.0, z), (max(sx * 2.6, sx * 1.7), 40.7, z + 0.7), 'tusk')
for sx in (1, -1):                                                                                   # THE TUSKS
    SEG('jaw', (sx * 4.0, 38.6, -14.8), (sx * 4.9, 42.6, -16.0), 1.7, 1.7, 'tusk', up=(0.0, 0.0, -1.0), ext=0.25)
    SEG('jaw', (sx * 4.9, 42.4, -16.0), (sx * 6.0, 45.2, -15.6), 1.0, 1.0, 'tusk', up=(0.0, 0.0, -1.0))
for k, (x, L) in enumerate(((0.0, 6.0), (-2.0, 5.0), (2.0, 5.2), (-3.4, 3.6), (3.4, 3.8))):        # (the beard: moss)
    lock('jaw', (x, 37.2, -13.6 + abs(x) * 0.6), (x * 0.06, -1.0, -0.12), L, 2.2, droop=0.0, t=0.7)

# ---------------------------------------------------------------------------------------------------- the arms (long; huge forearms)
def arm(sx):
    a, f, h = ('armr', 'forer', 'handr') if sx > 0 else ('arml', 'forel', 'handl')
    SH, EL, WR = PIVOT[a], PIVOT[f], PIVOT[h]
    rod(a, [SH, EL], [8.2, 7.0], 'fur')
    stack(R, a, profile(SH[1] - 3.6, 7.6, 4.6, n=3), 'fur', c=(SH[0] + sx * 0.4, SH[2]))         # (the shoulder cap)
    for k, (dz, L) in enumerate(((2.6, 9.0), (0.4, 8.0), (-2.2, 6.6))):                         # (fringe off the back of the upper arm)
        lock(a, (SH[0] + sx * 3.2, SH[1] - 3.0 - k * 1.4, SH[2] + dz), (sx * 0.16, -1.0, 0.12), L * 0.8, 3.6, droop=0.02, t=0.6)
    # the forearm: huge, fur over its back, a STONE BRACER down its front with a crystal vein, a little cluster at the elbow
    rod(f, [EL, WR], [9.0, 8.4], 'fur')
    stack(R, f, profile(WR[1] + 1.0, 10.0, 5.0, n=3, d=0.95), 'fur', c=(WR[0], WR[2] + 0.4))      # (the forearm's swell)
    for k in range(3):                                                                           # (the bracer: three plates, overlapping like scree)
        y0 = WR[1] + 1.4 + k * 3.2; y1 = y0 + 3.6
        B(f, (WR[0] - 3.7 + k * 0.2, y0, WR[2] - 5.4 + k * 0.15), (WR[0] + 3.7 - k * 0.2, y1, WR[2] - 3.4), 'stone_l', rot=('x', -6.0, (WR[0], y1, WR[2] - 4.4)))
        B(f, (WR[0] - 3.7 + k * 0.2, y1 - 0.5, WR[2] - 5.65 + k * 0.15), (WR[0] + 3.7 - k * 0.2, y1, WR[2] - 5.3 + k * 0.15), 'stone_d', rot=('x', -6.0, (WR[0], y1, WR[2] - 4.4)))
    SEG(f, (WR[0] - sx * 1.0, WR[1] + 3.0, WR[2] - 5.75), (WR[0] + sx * 1.2, EL[1] - 4.4, WR[2] - 5.75), 0.5, 0.3, 'vein', up=(0.0, 0.0, -1.0), light=13, full=True)
    SEG(f, (WR[0] + sx * 1.2, EL[1] - 4.4, WR[2] - 5.75), (WR[0] - sx * 0.6, EL[1] - 3.0, WR[2] - 5.75), 0.5, 0.3, 'vein', up=(0.0, 0.0, -1.0), light=13, full=True)
    cluster(f, (EL[0] + sx * 1.8, EL[1] - 1.6, EL[2] + 3.6), [(sx * 0.6, 0.4, 1.0), (sx * 0.2, 0.9, 0.8), (sx * 0.9, -0.1, 0.6)], [(3.6, 1.2), (2.8, 1.0), (2.2, 0.8)])
    for k, (y, L) in enumerate(((EL[1] - 1.0, 7.0), (EL[1] - 4.0, 6.0))):                       # (fringe off the forearm's outer side)
        lock(f, (EL[0] + sx * 4.2, y, EL[2] + 1.0), (sx * 0.2, -1.0, 0.1), L, 3.2, droop=0.02, t=0.6)
    # the hand: a stone fist - palm, four curled fingers whose knuckle pads take its weight, a thumb on the inside
    x, y, z = WR
    B(h, (x - 4.2, y - 6.2, z - 4.0), (x + 4.2, y + 0.4, z + 3.6), 'stone')                      # (the palm)
    B(h, (x - 4.0, y - 6.0, z + 3.4), (x + 4.0, y - 0.6, z + 4.4), 'fur2')                       # (the back of the hand: fur)
    for i, dx in enumerate((-3.0, -1.0, 1.0, 3.0)):
        fx_ = x + dx * sx * 1.0
        B(h, (fx_ - 0.95, y - 9.6, z - 5.4), (fx_ + 0.95, y - 5.8, z - 0.4), 'stone_l')           # (the finger, curled)
        B(h, (fx_ - 0.85, y - 10.2, z - 4.8), (fx_ + 0.85, y - 9.4, z + 0.6), 'stone_d')          # (its knuckle pad, on the ground)
        B(h, (fx_ - 0.7, y - 8.6, z - 5.9), (fx_ + 0.7, y - 7.2, z - 5.3), 'nail')                # (a nail)
    B(h, (x - sx * 4.8 - 0.9, y - 7.6, z - 3.6), (x - sx * 4.8 + 0.9, y - 3.0, z + 0.4), 'stone_l')    # (the thumb)


mirror(arm)

# ---------------------------------------------------------------------------------------------------- the legs (short, thick) and the feet
def legs(sx):
    t, s, f = ('thighr', 'shinr', 'footr') if sx > 0 else ('thighl', 'shinl', 'footl')
    HP, KN, AN = PIVOT[t], PIVOT[s], PIVOT[f]
    rod(t, [HP, KN], [9.0, 7.6], 'fur2')
    stack(R, t, profile(KN[1], 9.0, 5.2, n=3), 'fur2', c=(HP[0] + sx * 0.4, HP[2] - 0.2))
    lock(t, (HP[0] + sx * 4.6, HP[1] - 1.0, HP[2]), (sx * 0.4, -1.0, 0.1), 7.0, 3.4, droop=0.0)
    rod(s, [KN, AN], [7.2, 6.4], 'fur2')
    B(s, (KN[0] - 2.6, KN[1] - 2.4, KN[2] - 4.0), (KN[0] + 2.6, KN[1] + 0.6, KN[2] - 2.6), 'stone')     # (the knee)
    x, y, z = AN
    B(f, (x - 4.4, 0.0, z - 6.0), (x + 4.4, 2.8, z + 4.2), 'stone')
    B(f, (x - 3.6, 2.6, z - 3.6), (x + 3.6, 4.0, z + 3.2), 'fur2')
    for i, dx in enumerate((-2.6, -0.4, 1.6, 3.4)):
        B(f, (x + sx * dx - 0.95, 0.0, z - 8.0), (x + sx * dx + 0.95, 2.0, z - 5.6), 'stone_l')
        B(f, (x + sx * dx - 0.7, 0.0, z - 8.5), (x + sx * dx + 0.7, 1.1, z - 7.9), 'nail')
    B(f, (x - sx * 4.4 - 1.5, 0.0, z - 6.4), (x - sx * 4.4 + 1.2, 2.2, z - 2.8), 'stone_l')            # (the big toe: an ape's thumb-toe)
    B(f, (x - 3.4, 0.0, z + 4.0), (x + 3.4, 2.0, z + 5.4), 'stone_d')                                 # (the heel)


mirror(legs)

# ---------------------------------------------------------------------------------------------------- THE SADDLE: in the mossy pass between the ridges
LEAN = 46.0                                     # (the knuckle stance's chest lean in the world: the saddle is built level for it)
_tilt = ('x', LEAN, (0.0, 44.0, 4.0))
SEAT_PT = (0.0, 46.2, 4.6)                      # (the seat's surface at the rider's middle, rest design units)
B('saddle', (-4.2, 44.2, -1.2), (4.2, 45.2, 9.4), 'leather', rot=_tilt)                               # (the pad: moss-felt and leather)
B('saddle', (-3.0, 45.0, 0.6), (3.0, 46.2, 8.0), 'leather', rot=_tilt)                                # (the seat)
B('saddle', (-3.2, 45.8, 7.4), (3.2, 48.2, 8.8), 'leather', rot=_tilt)                                # (the cantle)
for sx in (1, -1):
    SEG('saddle', (sx * 2.6, 45.4, -0.6), (sx * 2.2, 49.0, -1.6), 0.8, 0.8, 'bamboo')                 # (two bamboo grips)
    SEG('saddle', (sx * 2.2, 49.0, -1.6), (sx * 1.0, 49.6, -1.8), 0.7, 0.7, 'bamboo')
B('saddle', (-1.2, 49.2, -2.2), (1.2, 50.0, -1.2), 'brass', rot=_tilt)                                # (a brass cap: Black Market tack)
for k, z in enumerate((0.8, 6.8)):                                                                    # (vine girths round the hump, under the ridges)
    for sx in (1, -1):
        SEG('saddle', (sx * 3.6, 44.6, z), (sx * 9.8, 38.0, z - 1.0), 0.9, 0.7, 'vine', up=(0.0, 0.0, 1.0))
        SEG('saddle', (sx * 9.8, 38.0, z - 1.0), (sx * 10.6, 30.0, z - 3.0), 0.9, 0.7, 'vine', up=(0.0, 0.0, 1.0))

# ---------------------------------------------------------------------------------------------------- fx
# THE BOULDER (held overhead): a lump of block COPIES - stone and dirt and a grass cap, cubes knocked out of true (in game:
# block_display copies of the ground under it - the real blocks are never touched)
bx, by, bz = PIVOT['boulder']
rnd = random.Random(7)
for i in range(14):
    a = rnd.uniform(0, 6.28); e = rnd.uniform(-1.2, 1.2); r = rnd.uniform(1.0, 4.0)
    c = (bx + r * math.cos(a) * math.cos(e), by + r * math.sin(e) * 1.1, bz + r * math.sin(a) * math.cos(e))
    s = rnd.uniform(3.4, 5.2)
    tex = 'grass' if c[1] > by + 1.5 else ('dirt' if i % 3 == 0 else ('rock' if i % 2 else 'rock2'))
    B('boulder', (c[0] - s / 2, c[1] - s / 2, c[2] - s / 2), (c[0] + s / 2, c[1] + s / 2, c[2] + s / 2), tex,
      rot=((rnd.uniform(-20, 20), rnd.uniform(-30, 30), rnd.uniform(-20, 20)), c), full=True)
# THE QUAKE: a ring of cracked block copies heaved up round the fists, dust puffs
qx, qy, qz = PIVOT['quake']
for i in range(16):
    a = math.radians(i * 22.5); r = 12.0 + (i % 2) * 2.0
    c = (qx + r * math.cos(a), 0.8, qz + r * math.sin(a))
    B('quake', (c[0] - 1.8, 0.0, c[2] - 1.8), (c[0] + 1.8, 2.6 + (i % 3) * 0.6, c[2] + 1.8), 'rock' if i % 2 else 'grass',
      rot=((18 * math.sin(a), -i * 22.5, 18 * math.cos(a)), c), full=True)
for i in range(8):
    a = math.radians(i * 45 + 10); r = 16.5
    c = (qx + r * math.cos(a), 3.0, qz + r * math.sin(a))
    B('quake', (c[0] - 3.0, c[1] - 3.0, c[2]), (c[0] + 3.0, c[1] + 3.0, c[2] + 0.02), 'dust', faces=('north', 'south'), full=True)
for k in range(3):
    ring(R, 'quake', (qx, 0.3, qz), 6.0 + k * 3.4, 16, 0.7, 0.3, 'vein', light=12)
# THE WAR-DRUM: violet rings booming off its chest
for k, (r, z) in enumerate(((7.0, -11.0), (10.0, -14.0), (13.0, -17.5))):
    ring(R, 'beatfx', (0.0, 32.0, z), r, 16, 0.8, 0.35, 'vein', plane='xy', light=14)
# THE IMPACT: a punch's burst (a star of geode light) and splinters
ix, iy, iz = PIVOT['impact']
B('impact', (ix - 5.0, iy - 5.0, iz), (ix + 5.0, iy + 5.0, iz + 0.02), 'burst', faces=('north', 'south'), full=True, light=15)
for k in range(6):
    a = math.radians(k * 60 + 15)
    SEG('impact', (ix + 2.4 * math.cos(a), iy + 2.4 * math.sin(a), iz), (ix + 7.0 * math.cos(a), iy + 7.0 * math.sin(a), iz + 1.0), 0.6, 0.6, 'crys_c', light=15, full=True)
# THE RARE AURA: GEODE HEART - crystals orbiting it, a glow at its heart
for i in range(9):
    a = math.radians(i * 40); r = 19.0; y = 24.0 + 6.0 * math.sin(a * 3)
    c = (r * math.cos(a), y, r * math.sin(a))
    crystal_spike('aura', (c[0], c[1] - 1.6, c[2]), (c[0], c[1] + 2.6, c[2]), 1.4, 'crys_c', light=15)
    B('aura', (c[0] * 0.8 - 0.5, c[1] + 8.0, c[2] * 0.8), (c[0] * 0.8 + 0.5, c[1] + 9.0, c[2] * 0.8 + 0.02), 'aura', faces=('north', 'south'), full=True, light=15)

# ---------------------------------------------------------------------------------------------------- skins
def _skin(sfx, F, F2, S, A, tk=TUSK):
    t = _tex(F, F2, S, A, tk, sfx)
    sw = {}
    for k, im in t.items():
        R.tex(k + sfx, im); sw[k] = k + sfx
    R.skin(sfx, sw)


_skin('_au', dict(part='#2a1206', dark='#4a2410', base='#7a3e16', light='#a8601e', shine='#d89a3a', tip='#f0c050'),
      dict(part='#1e0e06', dark='#36180a', base='#562a12', light='#7a3e18', shine='#a86024', tip='#c88a30'), STONE,
      dict(deep='#5a2a04', dark='#a05a08', base='#e09a18', light='#ffcc4a', core='#fff4c0'))
_skin('_sn', dict(part='#7a8a96', dark='#a8b6c0', base='#d0dae0', light='#eaf0f4', shine='#ffffff', tip='#ffffff'),
      dict(part='#6a7884', dark='#8a98a4', base='#aebac4', light='#cad4dc', shine='#e8eef2', tip='#f4f8fa'),
      dict(STONE, deep='#2a2c30', dark='#484c52', base='#6c7076', light='#8c9096', shine='#acb0b6', fleck='#7a8896'),
      dict(deep='#0a3a5a', dark='#1a6a9a', base='#4ab0e0', light='#9ae0ff', core='#eafcff'))
_skin('_sh', dict(part='#3a1010', dark='#6a2416', base='#a8481e', light='#e07a2a', shine='#ffb44a', tip='#ffd870'),
      dict(part='#2a0c0c', dark='#4a1a12', base='#74301a', light='#9a4a22', shine='#c8702e', tip='#e09a40'),
      dict(deep='#0e2a1e', dark='#1a4a34', base='#2e7a56', light='#4ea67a', shine='#7cd0a0', fleck='#a8e8c0'),
      dict(deep='#5a1434', dark='#a02a5e', base='#e05a92', light='#ff9ac0', core='#fff0f6'),
      dict(dark='#4a6a5a', base='#8ab8a0', light='#b8dcc8', shine='#e8fff0'))
R.skin('_ch', {'crys': 'crys_c'})
for k in list(R._tex):
    if not any(k.endswith(s) for s in ('_au', '_sn', '_sh')): R.tex(k + '_g', ghost(R._tex[k], AME['light'], 110))
R.skin('_g', {k: k + '_g' for k in list(R._tex) if not k.endswith('_g') and not any(k.endswith(s) for s in ('_au', '_sn', '_sh'))})


# ---------------------------------------------------------------------------------------------------- poses
def _low(pose, parts):
    pts = []
    xf = rigkit.solve(R.PIVOT, R.PARENT, pose)
    for p in parts:
        q, t = xf[p]; pv = rigkit.D(R.PIVOT[p])
        for v in R._pts[p]:
            r = rigkit.qrot(q, tuple(rigkit.D(v)[i] - pv[i] for i in range(3)))
            pts.append(pv[1] + t[1] + r[1])
    return min(pts)


def plant(p, parts=('footr', 'footl'), hands=None):
    """feet flat (each foot's world turn undone), then the root's height set so the lowest of these parts touches y=0; hands:
    the hands' world turn set to it (knuckles down), the arms' reach checked by the caller"""
    p = dict(p)
    for s in 'rl':
        Q = rigkit.solve(R.PIVOT, R.PARENT, p)['shin' + s][0]
        p['foot' + s] = qmul((-Q[0], -Q[1], -Q[2], Q[3]), p.get('_footturn', rigkit.I))
        if hands is not None:
            Qf = rigkit.solve(R.PIVOT, R.PARENT, p)['fore' + s][0]
            p['hand' + s] = qmul((-Qf[0], -Qf[1], -Qf[2], Qf[3]), hands)
    p.pop('_footturn', None)
    return R.ground(p)


def reach(p):
    """(knuckles' lowest - 0, feet's lowest - 0) once grounded: both near 0 means all four plant"""
    return round(_low(p, ('handr', 'handl')), 2), round(_low(p, ('footr', 'footl')), 2)


def K(**kw):
    """the knuckle stance: chest leaned, head up to look ahead, the arms swung forward to stand straight, all four planted"""
    hand = kw.pop('_hand', rigkit.I)
    p = dict(body=T(12), chest=T(24), head=T(-34), jaw=T(4),
             armr=limb(1, 32, 8), forer=limb(1, 4), arml=limb(-1, 32, 8), forel=limb(-1, 4),
             thighr=limb(1, 12, 6), shinr=T(-12), thighl=limb(-1, 12, 6), shinl=T(-12))
    p.update(kw)
    return plant(p, hands=hand)


def U(**kw):
    """upright: reared up on its legs (roar, the drum, the pound's wind-up, the throw)"""
    p = dict(body=T(-4), chest=T(-6), head=T(-2), thighr=limb(1, 10, 6), shinr=T(-14), thighl=limb(-1, 10, 6), shinl=T(-14))
    p.update(kw)
    return plant(p)


s_ = math.sin
POSES = R.POSES
POSES.update({
    'idle_a': K(),
    'idle_b': K(_face='look', head=T(-30, 28, 6), chest=T(22, -4), arml=limb(-1, 30, 8), jaw=T(2)),
})
for k in range(4):                                                  # THE KNUCKLE WALK (24 ticks): a heavy diagonal gait
    ph = math.pi * k / 2; w = s_(ph); c = math.cos(ph)
    POSES[f'walk_{k}'] = K(body=T(12, 4 * w, 3 * w), chest=T(24, -6 * w, -2 * w), head=T(-34, 5 * w, -2 * w),
                           armr=limb(1, 32 + 14 * w, 8), forer=limb(1, 4 + 26 * max(0.0, -c)), arml=limb(-1, 32 - 14 * w, 8), forel=limb(-1, 4 + 26 * max(0.0, c)),
                           thighr=limb(1, 12 - 16 * w, 6), shinr=T(-12 - 26 * max(0.0, c)), thighl=limb(-1, 12 + 16 * w, 6), shinl=T(-12 - 26 * max(0.0, -c)))
for k in range(4):                                                  # THE GALLOP (12 ticks): bounding, the arms reaching together
    ph = math.pi * k / 2; w = s_(ph)
    p = K(body=T(18 + 6 * w), chest=T(22 - 4 * w), head=T(-40 + 4 * w), jaw=T(12),
          armr=limb(1, 40 + 26 * w, 10), forer=limb(1, 10), arml=limb(-1, 36 + 26 * w, 10), forel=limb(-1, 10),
          thighr=limb(1, 20 - 30 * w, 6), shinr=T(-30), thighl=limb(-1, 16 - 30 * w, 6), shinl=T(-30))
    o = p['_off']; p['_off'] = (o[0], o[1] + 2.4 * max(0.0, s_(ph + 1.2)), o[2]); POSES[f'run_{k}'] = p
POSES.update({
    # THE ROAR: reared up, arms flung wide, the jaw dropped, the tusks bared (and the ridge lit)
    'roar': U(_face='roar', body=T(-8), chest=T(-10), head=T(-14), jaw=T(36), armr=limb(1, 30, 60), forer=limb(1, -20), arml=limb(-1, 30, 60), forel=limb(-1, -20),
              handr=limb(1, 0, -20), handl=limb(-1, 0, -20)),
    # THE WAR-DRUM (the chest-beat): upright, the fists hammering its chest slabs in turn
    'beat_0': U(_face='roar', _show=('beatfx',), chest=T(-8, 6), head=T(-16, -6), jaw=T(30), armr=limb(1, 20, 0, 40), forer=limb(1, 100), handr=limb(1, 0, 0, 30),
                arml=limb(-1, 60, 40), forel=limb(-1, 60)),
    'beat_1': U(_face='roar', _show=('beatfx',), chest=T(-8, -6), head=T(-16, 6), jaw=T(30), arml=limb(-1, 20, 0, 40), forel=limb(-1, 100), handl=limb(-1, 0, 0, 30),
                armr=limb(1, 60, 40), forer=limb(1, 60)),
    # THE GROUND POUND: up on its legs, both fists high over its head - then down on the ground before it, crouched
    'pound_0': U(_face='fierce', body=T(-10), chest=T(-14), head=T(-6), jaw=T(14), armr=limb(1, 170, 14), forer=limb(1, 20), arml=limb(-1, 170, 14), forel=limb(-1, 20)),
    'pound_1': K(_face='roar', _show=('quake',), body=T(30), chest=T(36), head=T(-50), jaw=T(30), armr=limb(1, 66, 18), forer=limb(1, -8), arml=limb(-1, 66, 18), forel=limb(-1, -8),
                 thighr=limb(1, 50, 10), shinr=T(-70), thighl=limb(-1, 50, 10), shinl=T(-70)),
    # THE BOULDER: it tears up a lump of ground (copies) and holds it overhead - then hurls it
    'throw_0': U(_face='fierce', _show=('boulder',), body=T(-12), chest=T(-18), head=T(-4), jaw=T(10), armr=limb(1, 160, 22), forer=limb(1, 40), arml=limb(-1, 160, 22), forel=limb(-1, 40),
                 thighr=limb(1, 0, 8), thighl=limb(-1, 24, 8), shinl=T(-26)),
    'throw_1': K(_face='roar', body=T(20), chest=T(26), head=T(-30), jaw=T(26), armr=limb(1, 100, 10), forer=limb(1, 0), arml=limb(-1, 100, 10), forel=limb(-1, 0),
                 thighr=limb(1, 50, 6), shinr=T(-60), thighl=limb(-1, -10, 6), shinl=T(-10)),
    # THE CLIMBING LEAP: coiled low on all fours - then airborne, arms reaching forward
    'leap_0': K(_face='fierce', body=T(26), chest=T(34), head=T(-50), armr=limb(1, 40, 14), forer=limb(1, 28), arml=limb(-1, 40, 14), forel=limb(-1, 28),
                thighr=limb(1, 60, 8), shinr=T(-80), thighl=limb(-1, 60, 8), shinl=T(-80)),
})
_lp = U(_face='roar', body=T(30), chest=T(16), head=T(-36), jaw=T(20), armr=limb(1, 150, 16), forer=limb(1, 10), arml=limb(-1, 150, 16), forel=limb(-1, 10),
        thighr=limb(1, 30, 8), shinr=T(-60), thighl=limb(-1, -20, 8), shinl=T(-30))
_lp['_off'] = (_lp['_off'][0], _lp['_off'][1] + 10.0, _lp['_off'][2] - 6.0)
POSES['leap_1'] = _lp
# THE FIST FLURRY (Rank III, Piercing Blow): planted wide, a lunge, and alternating straight punches - fast snaps (2 ticks each),
# the trailing arm left as an afterimage ('_g'), an impact burst on each hit - then the two-fisted hammer
_FL = dict(body=T(6), thighr=limb(1, 26, 14), shinr=T(-34), thighl=limb(-1, -8, 14), shinl=T(-12))
POSES.update({
    'flurry_0': U(_face='fierce', **_FL, chest=T(12, -26), head=T(-14, 20), jaw=T(16), armr=limb(1, 86, 4, 10), forer=limb(1, 0), handr=limb(1, 0, 0, 0),
                  arml=limb(-1, 40, 26), forel=limb(-1, 110)),
    'flurry_1': U(_face='fierce', _show=('impact',), **_FL, chest=T(12, 26), head=T(-14, -20), jaw=T(24), arml=limb(-1, 86, 4, 10), forel=limb(-1, 0),
                  armr=limb(1, 40, 26), forer=limb(1, 110)),
    'flurry_2': U(_face='roar', **_FL, chest=T(16, -30), head=T(-18, 22), jaw=T(30), armr=limb(1, 96, -6, 10), forer=limb(1, -4),
                  arml=limb(-1, 30, 30), forel=limb(-1, 120)),
    'flurry_3': U(_face='roar', _show=('impact',), **_FL, chest=T(16, 30), head=T(-18, -22), jaw=T(30), arml=limb(-1, 96, -6, 10), forel=limb(-1, -4),
                  armr=limb(1, 30, 30), forer=limb(1, 120)),
    'flurry_fin_0': U(_face='roar', body=T(-12), chest=T(-16), head=T(-8), jaw=T(34), armr=limb(1, 176, -8), forer=limb(1, 30), arml=limb(-1, 176, -8), forel=limb(-1, 30),
                      thighr=limb(1, 20, 10), shinr=T(-24), thighl=limb(-1, 0, 10), shinl=T(-10)),
    'flurry_fin_1': U(_face='roar', _show=('impact',), body=T(22), chest=T(30), head=T(-40), jaw=T(36), armr=limb(1, 110, -10), forer=limb(1, -6), arml=limb(-1, 110, -10), forel=limb(-1, -6),
                      thighr=limb(1, 48, 12), shinr=T(-56), thighl=limb(-1, -12, 12), shinl=T(-18)),
    # SITTING (right-click): down on its haunches, the knuckles resting on its feet, the head up - a mountain at rest
    'sit_a': plant(dict(_face=None, body=T(-24), chest=T(14), head=T(-10), thighr=limb(1, 88, 18), shinr=T(-110), thighl=limb(-1, 88, 18), shinl=T(-110),
                        armr=limb(1, 26, 12), forer=limb(1, 40), arml=limb(-1, 26, 12), forel=limb(-1, 40)), parts=('footr', 'footl', 'body')),
    # (sneak) TAKES ROOT: sat cross-legged like a cairn, eyes shut, hands on its knees, the crystals dim and breathing
    'sit_b': plant(dict(_face='sleepy', body=T(-6), chest=T(18), head=T(20), thighr=limb(1, 84, 50), shinr=T(-140, 50), thighl=limb(-1, 84, 50), shinl=T(-140, -50),
                        armr=limb(1, 40, 8), forer=limb(1, 40), arml=limb(-1, 40, 8), forel=limb(-1, 40)), parts=('body', 'footr', 'footl', 'shinr', 'shinl')),
    'happy': U(_face='happy', head=T(-10, 0, 10), armr=limb(1, 40, 50), forer=limb(1, 70), arml=limb(-1, 40, 50), forel=limb(-1, 70), jaw=T(14)),
    'hurt': K(_face='hurt', body=T(6, 0, 8), chest=T(18, 10, -6), head=T(-20, -20, 12), jaw=T(20), arml=limb(-1, 30, 30)),
    'ride': K(_face='fierce', head=T(-38), jaw=T(6)),
    'aura': K(_show=('aura',), _face='happy'),
    'doll': plant(dict(_face='happy', body=T(-24), chest=T(14), head=T(-12), thighr=limb(1, 88, 18), shinr=T(-110), thighl=limb(-1, 88, 18), shinl=T(-110),
                       armr=limb(1, 40, -4, 20), forer=limb(1, 70), arml=limb(-1, 40, -4, 20), forel=limb(-1, 70)), parts=('footr', 'footl', 'body')),
})
DRAFT = list(POSES)
R.DRAFT = DRAFT
DOLL = {'kh': 1.7, 'kb': 0.74, 'kl': 0.62}            # (close to the default: a mountain of a body needs the head a touch bigger to read chibi)
DOLL_GROUPS = {'head': 'head', 'jaw': 'head', 'ridge': 'body', 'chest': 'body', 'body': 'body', 'saddle': 'body',
               'armr': 'body', 'forer': 'body', 'handr': 'body', 'arml': 'body', 'forel': 'body', 'handl': 'body',
               'thighr': 'legs', 'shinr': 'legs', 'footr': 'legs', 'thighl': 'legs', 'shinl': 'legs', 'footl': 'legs'}

# ---- the moves (ticks; the doc has the whole choreography). A "key" is (tick, pose): the runtime tweens between them.
MOVES = {
    'pound': dict(keys=((0, 'pound_0'), (10, 'pound_1')), hit=12, recover=14, cd=8 * 20, radius=6.0, dmg=10,
                  fx='rears for 10 t, both fists down at 12: a ring of cracked COPIES of the ground heaves up (block_display, 1 s), dust, knockback up'),
    'throw': dict(keys=((0, 'throw_0'), (14, 'throw_1')), hit=16, recover=12, cd=10 * 20, dmg=12, range=24,
                  fx='tears up a boulder of COPIES of the 3x3 under it (block_display, the real blocks untouched), holds 14 t, hurls it along a lob; it bursts into dust and copy-fragments on impact (3-block splash)'),
    'beat': dict(keys=((0, 'beat_0'), (4, 'beat_1'), (8, 'beat_0'), (12, 'beat_1')), hit=4, recover=8, cd=20 * 20, radius=10.0,
                 fx='THE WAR-DRUM: 4 beats (4 t apart), a violet ring off its chest each beat; allies within 10: Strength I + Resistance I 10 s; hostiles: Weakness I 6 s; the ridge charged (_ch) while it drums'),
    'leap': dict(keys=((0, 'leap_0'), (8, 'leap_1')), hit=8, recover=10, cd=6 * 20,
                 fx='a climbing leap: coils 8 t, then launches up to 10 blocks forward / 6 up (an eased motion of its host, never a teleport); lands in a small pound (r 3)'),
    'flurry': dict(keys=((0, 'flurry_0'), (2, 'flurry_1'), (4, 'flurry_2'), (6, 'flurry_3'), (8, 'flurry_0'), (10, 'flurry_1'), (12, 'flurry_2'), (14, 'flurry_3'),
                         (16, 'flurry_fin_0'), (24, 'flurry_fin_1')), hit=(3, 7, 11, 15, 25), recover=14, cd=14 * 20, dmg=(4, 4, 4, 4, 14), pierce=True,
                   fx='RANK III, FIST FLURRY: armour-piercing; 8 punches 2 t apart (an impact burst on every other), each trailing arm left 2 t as an afterimage (_g), the finisher a two-fisted hammer'),
}

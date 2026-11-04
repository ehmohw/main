"""(3.1 draft, stage 1: art only - not wired) THE GOLDEN DOODLE - follower 61 (after the Ferro): a gilded, sparkly, goofy goose.
The Lucky Nights' own creature, and a joke boss that stops being a joke (its second phase, the Gilded Eldritch, is
goldendoodle_boss_art.py; the design: scratchpad/design_goldendoodle.md).

The owner: "a gilded, sparkly follower. Kind of based off a goose. It has two waddly feet, a long neck, and a goofy body. When it
walks, its neck kinda bends backwards, and when it runs, its neck and head funnily flap behind it. It waddles."

LOOK   Knee-to-hip high on a player: ~1.15 blocks to the top of its cowlick (RIG_SCALE 0.8; the boss's phase 1 stands it at 1.0,
       ~1.45 blocks - still smaller than you, which is the joke). A domestic goose's silhouette, pushed goofy:
         - THE BODY: a plump horizontal egg (seven slabs, deep-cut corners), a proud low breast, a flat back running up into a
           short upturned tail, and a domestic goose's PAUNCH - a saggy fold of belly that swings nearly to the ground behind
           its legs (the waddle's whole reason).
         - THE NECK: long, an S (out of the breast, up, and the head carried forward), octagonal (two rods a hair apart in roll)
           with the furrowed feathers a goose's neck has; two parts (neck1, neck2) so it can bend BACK when it walks and stream
           behind it when it runs.
         - THE HEAD: a long egg that runs straight into the beak (a goose's profile), a big orange beak with a pale nail at its
           tip, the black "grin patch" along its edge (a real goose's, and a permanent smirk), nostrils, and the KNOB at its
           base (a Chinese goose's) set with a little EMERALD - its lucky gem. A three-feather cowlick on top.
         - THE FACE: two BEADY eyes, black and glossy, set on the sides of the head but turned forward so they read from the
           front, a gold eye-ring, one big shine; a faint blush behind each. Every expression redrawn (gq_eyes_<kind>), and the
           honk is geometry too: the jaw drops (35 deg), the pink mouth and the goose's notorious serrated TEETH (the tomia, on
           the tongue and the upper bill) show.
         - THE WINGS: folded along its sides - coverts in scalloped rows, a row of secondaries, three long primaries crossing
           over the rump - a lit leading edge a hair proud; separate parts so they can flap, spread and threaten.
         - THE FEET: big floppy orange paddles (a third of its body length): three toes with pale claws, webbing scooped back
           between them; separate parts (the toes slap up as each foot lifts). A jade bird-band on its right leg.
         - GILT: every feather gold leaf - scalloped rows, a lit edge, a running diagonal glint where the light catches it,
           and a few painted star-sparkles in small clusters; a cluster of three real sparkles (light 15) rides on its back
           and one by its head. A four-leaf clover marking on its breast. The belly a softer cream-gold down.
RIG    body (root: body, paunch, breast, tail, the clover, the sparkles) - neck1 - neck2 - head (face part) - jaw - wr / wl
       (wings) - legr / legl (shank, the band) - footr / footl (the paddles); fx: 'honk' (the sound rings), 'egg' (a golden
       egg, laid), 'eggs' (the boss's egg drop: three eggs, one popped into confetti), 'held' (a stolen sword in its beak),
       'coin' (the lucky coin it flips), 'shard' (the Dread Sovereign's shard, lodged in its head: the morph's first beat),
       'aura' (the rare aura: JACKPOT), 'nest' (sitting: a little golden nest).
SKINS  '_rg' ROSE GOLD and '_pt' PLATINUM (cosmetics, each with its Eldritch twin), '_sh' SHINY "FOUR-LEAF" (emerald feathers,
       gold sparkle - "trying something new today"), '_cr1' / '_cr2' (the morph: the shard's cracks spreading), '_gos' (a
       gosling's downy palette, for the Lucky Night goslings).
"""
import math
import random
from PIL import Image, ImageDraw
from fol5_kit import (Rig, hexc, mix, mul, limb, T, cells, soft, lit, glow, put, slab, stack, ball, profile, chain, ring, leaf,
                      cleaf, recolor, _patch, stroke, _curve, _thick, _vee, _ell)
import rigkit

PIVOT = {'body': (0, 9.0, 0.6), 'neck1': (0, 11.0, -5.8), 'neck2': (0, 16.8, -8.2), 'head': (0, 21.6, -8.0), 'jaw': (0, 22.1, -11.2),
         'wr': (5.0, 11.6, -2.4), 'wl': (-5.0, 11.6, -2.4), 'legr': (2.6, 5.4, 0.6), 'legl': (-2.6, 5.4, 0.6),
         'footr': (2.6, 1.0, 0.4), 'footl': (-2.6, 1.0, 0.4),
         'honk': (0, 22.0, -15.6), 'egg': (0, 0, 7.0), 'eggs': (0, 0, 0), 'held': (0, 21.8, -14.2), 'coin': (0, 30.0, -8.0),
         'shard': (0, 25.0, -8.4), 'aura': (0, 0, 0), 'nest': (0, 0, 0)}
PARENT = {'body': None, 'neck1': 'body', 'neck2': 'neck1', 'head': 'neck2', 'jaw': 'head', 'wr': 'body', 'wl': 'body',
          'legr': 'body', 'legl': 'body', 'footr': 'legr', 'footl': 'legl', 'honk': 'head', 'egg': None, 'eggs': None,
          'held': 'jaw', 'coin': None, 'shard': 'head', 'aura': None, 'nest': None}
FACES = ('honk', 'blink', 'happy', 'wide', 'derp', 'fierce', 'sleepy', 'look', 'dizzy', 'smug')
OPT = ('honk', 'egg', 'eggs', 'held', 'coin', 'shard', 'aura', 'nest')
R = Rig('gq_', 0.8, PIVOT, PARENT, FACES, face_part='head', opt=OPT)
BOSS1_SCALE = 0.9                  # (the boss's phase 1: ~1.6 blocks to its cowlick - still smaller than you)
SKIN_NAMES = {'_rg': 'cosmetic: Rose Gold', '_pt': 'cosmetic: Platinum', '_sh': 'SHINY: Four-Leaf'}

# ---------------------------------------------------------------------------------------------------- palette
GOLD = dict(deep='#5e3a06', dark='#94640e', base='#cf981c', light='#f0c444', shine='#fff0a0', white='#fffbe8')
CREAM = dict(dark='#c0923a', base='#e6c470', light='#f6dc98', shine='#fff4cc')
ORANGE = dict(deep='#7a2a06', dark='#b4470c', base='#ee7418', light='#ffa246', hot='#ffd08a')
NAIL, GRIN, MOUTH, TONGUE, TOOTH = '#ffe8b8', '#2a1406', '#a8303a', '#e86a74', '#fff6ea'
EMER = ('#0a3a1a', '#127a34', '#22b050', '#6aec8a', '#d8ffe0')
JADE = ('#0e4a3a', '#1c8a6a', '#4ad0a8', '#b8ffe8')


def sparkle(im, cx, cy, core='#ffffff', arm='#fff4b0', L=2):
    """a painted 4-point star in 2-px cells: a white core, arms L cells out (lighter at the core)"""
    d = ImageDraw.Draw(im)
    def sq(x, y, c):
        if 0 <= x < 32 and 0 <= y < 32: d.rectangle((x * 2, y * 2, x * 2 + 1, y * 2 + 1), fill=hexc(c))
    for k in range(1, L + 1):
        for dx, dy in ((k, 0), (-k, 0), (0, k), (0, -k)): sq(cx + dx, cy + dy, arm if k == 1 else mix(arm, '#000000', 0.0))
    sq(cx, cy, core)


def feathers(P, seed, w=6, rows=4, glint=True, sparks=1):
    """gold-leaf feathers in scalloped rows (P: deep, dark, base, light, shine) - STRUCTURE, not noise (the owner, 3.1: "a bit
    less noisy"): each feather w cells wide and rows tall, every row offset half a feather; inside it a soft gradient, top to
    bottom (tucked under the row above, the base, lit toward its tip), the tip's corners shaded so the edge scallops; a few
    HAND-PLACED glint strokes (short diagonals where the leaf catches the light), never a periodic pattern; one painted sparkle"""
    tuck, lit_ = mix(P['base'], P['dark'], 0.16), mix(P['base'], P['light'], 0.38)
    edge, tip = mix(P['base'], P['dark'], 0.42), mix(P['base'], P['light'], 0.62)
    def c(x, y, r):
        row = y // rows; off = (row % 2) * (w // 2); lx = (x + off) % w; ly = y % rows
        if ly == rows - 1: return edge if lx in (0, w - 1) else tip
        if ly == 0: return tuck
        if ly == rows - 2: return lit_
        return P['base']
    im = cells(c, seed)
    rnd = random.Random(seed); d = ImageDraw.Draw(im)
    if glint:
        for _ in range(3):                                      # (three short glint strokes, placed, not tiled)
            gx, gy = rnd.randrange(2, 28), rnd.randrange(2, 28)
            for k in range(3):
                col = P['shine'] if k == 1 else mix(P['light'], P['shine'], 0.5)
                d.rectangle(((gx + k) * 2, (gy - k) * 2, (gx + k) * 2 + 1, (gy - k) * 2 + 1), fill=hexc(col))
    if sparks:
        sparkle(im, rnd.randrange(6, 26), rnd.randrange(6, 26), P['white'], P['shine'], L=2)
    return im


def furrows(P, seed):
    """a goose neck's furrowed feathers: soft vertical ridges every 3 cells (a lit crest, a shaded furrow) that waver a little,
    and faint scallops every 8 rows - low contrast, structured"""
    rnd = random.Random(seed); wav = [0] * 32; o = 0
    for y in range(32):
        if rnd.random() < 0.1: o = (o + rnd.choice((-1, 1))) % 3
        wav[y] = o
    fur, crest = mix(P['base'], P['dark'], 0.3), mix(P['base'], P['light'], 0.32)
    def c(x, y, r):
        xx = (x + wav[y]) % 3
        if y % 8 == 7 and xx != 0: return mix(P['base'], P['dark'], 0.14)
        if xx == 0: return fur
        if xx == 1: return crest
        return P['base']
    return cells(c, seed)


def primaries(P, seed):
    """long flight feathers side by side: a pale shaft, a lit vane, the base vane, a soft dark edge (low contrast)"""
    def c(x, y, r):
        k = x % 5
        if k == 0: return mix(P['dark'], P['base'], 0.35)
        if k == 1: return mix(P['base'], P['light'], 0.5)
        if k == 2: return P['light'] if y % 16 else P['shine']
        if k == 3: return P['base']
        return mix(P['base'], P['dark'], 0.4)
    return cells(c, seed)


def down(P, seed):
    """soft cream-gold down: smooth, a faint scallop every 8 rows (two cells of shade under each), nothing random"""
    sh = mix(P['base'], P['dark'], 0.2)
    def c(x, y, r):
        if y % 8 == 7 and (x + (y // 8) % 2 * 3) % 6 in (1, 2, 3): return sh
        if y % 8 == 0: return mix(P['base'], P['light'], 0.25)
        return P['base']
    return cells(c, seed)


def orange(P, seed, scutes=False, web=False):
    """beak / leg / foot: a smooth orange glaze lit from above; scutes: a leg's scale rings; web: a paddle's toe ridges"""
    def c(x, y, r):
        if y < 2: return P['light']
        if scutes and y % 4 == 3: return P['dark']
        if web and x % 6 == 0: return P['dark']
        if web and x % 6 == 1: return P['light']
        if y > 27: return P['dark']
        return P['base']
    return cells(c, seed)


def gemtex(ramp, seed=0):
    """a faceted gem: diagonal facets, a bright table, a hot sparkle"""
    def c(x, y, r):
        d = (x + y) % 8
        if (x - y) % 11 == 0: return ramp[3]
        if d < 2: return ramp[1]
        if d < 5: return ramp[2]
        return ramp[3] if d == 5 else ramp[2]
    im = cells(c, seed); sparkle(im, 8, 8, '#ffffff', ramp[4], 1)
    return im


def clover_tex():
    """the four-leaf clover marking (full uv): four heart-leaves round a gold centre, a tiny stem; emerald with a lit edge"""
    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for ang in (45, 135, 225, 315):
        a = math.radians(ang); cx, cy = 16 + 6.2 * math.cos(a), 15 + 6.2 * math.sin(a)
        for k, (rr, col) in enumerate(((5.4, EMER[0]), (4.6, EMER[2]), (2.4, EMER[3]))):
            off = 0 if k < 2 else -1.2
            d.ellipse((cx - rr + off, cy - rr + off, cx + rr + off, cy + rr + off), fill=hexc(col))
    d.line((16, 18, 19, 29), fill=hexc(EMER[1]), width=2)
    d.ellipse((13, 12, 19, 18), fill=hexc(GOLD['light'])); d.ellipse((14, 13, 16, 15), fill=hexc('#ffffff'))
    return im


def spark_tex():
    """a real sparkle (full uv, see-through): a 4-point star, white-hot core, gold arms fading out"""
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for i in range(16):
        for j in range(16):
            dx, dy = abs(i - 7.5), abs(j - 7.5)
            v = max(0.0, 1 - (dx * dy) ** 0.5 / 2.2 - max(dx, dy) / 9.5)
            if v > 0.05:
                c = mix('#ffd040', '#ffffff', min(1, v * 1.4))
                im.putpixel((i, j), hexc(c, int(min(255, 90 + 200 * v))))
    return im


def ring_tex(col='#fff4c0', a=170):
    """the honk's sound ring: a pale band, brighter at its middle, see-through"""
    def c(x, y, r):
        k = abs(y - 15.5) / 16
        return (*hexc(mix(col, '#ffffff', 0.5 - k))[:3], int(a * (1 - k)))
    return cells(c, 0)


def coin_tex():
    """the lucky coin's face: gold, a raised rim, a clover stamped in the middle"""
    def c(x, y, r):
        d = math.hypot(x - 15.5, y - 15.5)
        if d > 15: return GOLD['dark']
        if d > 13: return GOLD['light'] if y < 16 else GOLD['dark']
        return GOLD['base'] if (x + y) % 9 else GOLD['light']
    im = cells(c, 0); d = ImageDraw.Draw(im)
    for ang in (45, 135, 225, 315):
        a = math.radians(ang); cx, cy = 32 + 8 * math.cos(a), 32 + 8 * math.sin(a)
        d.ellipse((cx - 6, cy - 6, cx + 6, cy + 6), fill=hexc(GOLD['deep']))
        d.ellipse((cx - 5, cy - 6, cx + 5, cy + 4), fill=hexc(GOLD['light']))
    return im


def confetti_tex():
    cols = ['#ff5a7a', '#5ad0ff', '#ffe040', '#7aff6a', '#c07aff', '#ffffff']
    return cells(lambda x, y, r: cols[(x // 4 + y // 4 * 3) % len(cols)], 0)


# ---------------------------------------------------------------------------------------------------- the beady eyes
EW, EH = 12, 12              # (one eye's window, px: 3 x 3 units at 4 px a unit; the right eye at u 0, the left at u 12)


def beady(im, x0, y0, kind=None, flip=False, ring='#ffe6a0', bead=('#050302', '#140a04', '#2a160a'), shine='#ffffff', blushc='#f2a08a'):
    """one beady goose eye in a 10 x 10 window: a black glossy bead (darker at the top), a gold eye-ring, one big shine up
    and toward the front (one light), a pin second shine; a blush low behind it. flip: the left eye (its window mirrored: the
    front of the head on the window's left). kinds: None, honk (> squeezed shut), blink, happy (^), wide (a white ring round a
    pin pupil: startled), derp (wide, the pupil rolled up - the LEFT eye only, see eyes()), fierce (a cross brow slanting
    down to the front), sleepy (a heavy lid), look (the bead slid to the front), dizzy (an X), smug (a flat lid, half shut)"""
    fx = (lambda x: x0 + (EW - 1 - x)) if flip else (lambda x: x0 + x)
    P = lambda x, y, c: put(im, fx(x), y0 + y, c)
    # (window coords: x 0 = the back of the head, 9 = the front - before flip)
    for x, y in ((1, 10), (2, 10), (3, 10), (4, 10), (2, 11), (3, 11)): P(x, y, blushc)
    cx, cy = 6.6, 5.4
    line = bead[1]
    if kind == 'honk':
        for x, y in ((4, 2), (5, 3), (6, 4), (7, 5), (8, 6), (7, 6), (6, 7), (5, 8), (4, 9), (8, 5)): P(x, y, line); P(x, y + 1 if (x, y) == (8, 6) else y, line)
        return
    if kind == 'blink':
        for x in range(3, 10): P(x, 5 if x in (3, 9) else 6, line); P(x, 7, line) if 4 < x < 8 else None
        return
    if kind == 'happy':
        for x in range(3, 10): P(x, 4 if 4 < x < 8 else 5, line); P(x, 5 if 4 < x < 8 else 6, line)
        P(3, 7, line); P(9, 7, line)
        return
    if kind == 'dizzy':
        for i in range(7): P(3 + i, 2 + i, line); P(9 - i, 2 + i, line)
        return
    S = _ell(cx + (1.0 if kind == 'look' else 0), cy, 2.7, 3.0)
    if kind in ('wide', 'derp'):
        W = _ell(cx, cy, 3.8, 4.1)
        for x, y in _rim_of(W): P(x, y, ring)
        for x, y in W: P(x, y, '#fffaf0')
        py = cy - (1.6 if kind == 'derp' else 0)
        for x, y in _ell(cx + 0.4, py, 1.4, 1.6): P(x, y, bead[0])
        P(int(cx), int(py) - 1, shine)
        return
    for x, y in _rim_of(S): P(x, y, ring)
    top = min(y for _, y in S); bot = max(y for _, y in S)
    for x, y in S:
        t = (y - top) / max(1, bot - top)
        P(x, y, bead[0] if t < 0.45 else bead[1] if t < 0.8 else bead[2])
    sx = max(x for x, _ in S) - 2
    P(sx, top + 1, shine); P(sx + 1, top + 1, shine); P(sx, top + 2, shine)
    P(min(x for x, _ in S) + 1, bot - 1, '#8a7a6a')
    if kind == 'sleepy' or kind == 'smug':
        cut = top + (3 if kind == 'sleepy' else 2)
        for x, y in S:
            if y < cut: P(x, y, GOLD['base'])
        for x in range(min(x for x, _ in S) - 1, max(x for x, _ in S) + 2): P(x, cut, GOLD['deep'])
    if kind == 'fierce':
        for x, y in ((2, 0), (3, 0), (4, 1), (5, 1), (6, 2), (7, 2), (8, 3), (9, 3), (10, 4)): P(x, y, GOLD['deep']); P(x, y + 1, GOLD['deep'])
        for x, y in S:
            if y < top + 2 and x > 6: P(x, y, GOLD['base'])


def _rim_of(S):
    return {(x + dx, y + dy) for x, y in S for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))} - set(S)


def eyes(kind=None):
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    beady(im, 0, 0, None if kind == 'derp' else kind)                # (its right eye)
    beady(im, EW, 0, kind, flip=True)                                  # (its left)
    return im


# ---------------------------------------------------------------------------------------------------- textures
def _tex(P=GOLD, C=CREAM, O=ORANGE, emer=EMER):
    t = {'gold': feathers(P, 11), 'gold2': feathers(P, 12, w=7), 'gold_d': feathers({**P, 'base': mix(P['base'], P['dark'], 0.3),
                                                                                         'light': P['base']}, 13, sparks=0),
         'neck': furrows(P, 14), 'prim': primaries(P, 15), 'down': down(C, 16), 'lip': lit(feathers(P, 17, glint=False, sparks=0), 1.25, 1.0, 4),
         'beak': orange(O, 18), 'beak_d': orange({**O, 'base': O['dark'], 'light': O['base']}, 19), 'leg': orange(O, 20, scutes=True),
         'foot': orange(O, 21, web=True), 'toe': orange(O, 22), 'claw': cells(lambda x, y, r: NAIL if y < 20 else mix(NAIL, '#b08a5a', 0.5), 0),
         'grin': cells(lambda x, y, r: GRIN, 0), 'mouth': cells(lambda x, y, r: MOUTH if y % 6 else mix(MOUTH, '#000000', 0.3), 0),
         'tongue': cells(lambda x, y, r: TONGUE if x % 3 else mix(TONGUE, '#ffffff', 0.3), 0), 'tooth': cells(lambda x, y, r: TOOTH, 0),
         'nail': cells(lambda x, y, r: NAIL if y > 3 else mix(NAIL, '#ffffff', 0.4), 0), 'nostril': cells(lambda x, y, r: O['deep'], 0),
         'gem': gemtex(emer), 'band': gemtex(JADE + ('#ffffff',)), 'clover': clover_tex(), 'spark': spark_tex(),
         'honkring': ring_tex(), 'egg': lit(feathers({**P, 'dark': P['base'], 'deep': P['base']}, 23, w=8, rows=8, sparks=0), 1.3, 0.85, 10),
         'coin': coin_tex(), 'coin_e': cells(lambda x, y, r: P['dark'] if y % 4 else P['light'], 0), 'confetti': confetti_tex(),
         'straw': cells(lambda x, y, r: (P['light'] if (x + 2 * y) % 7 == 0 else P['base'] if (x - y) % 5 else P['dark']), 24),
         'eyes': eyes(), 'aura': glow(['#ffffff', '#fff0a0', '#ffd040', '#f0a020'], alpha=[230, 190, 120, 0]),
         'steel': cells(lambda x, y, r: '#e8eef4' if x < 10 else '#b8c4d0' if x < 22 else '#8a96a4', 0),
         'hilt': cells(lambda x, y, r: '#5a3a1a' if y % 4 else '#8a5a2a', 0)}
    for f in FACES: t[f'eyes_{f}'] = eyes(f)
    return t


TEX = _tex()
for k, v in TEX.items(): R.tex(k, v)


# ---------------------------------------------------------------------------------------------------- helpers
B = R.box
U3 = (0.0, 0.0, -1.0)


def rod(part, pts, ws, tex, front=(0.0, 0.0, -1.0), k=0.8):
    """a round rod along a path (a neck, a leg): each span two boxes rolled 45 deg apart - an octagon in section"""
    f2 = (front[0] + (0.7 if abs(front[0]) < 0.5 else 0.0), front[1], front[2] * 0.7 + (0.0 if abs(front[0]) < 0.5 else 0.7))
    out = []
    for i in range(len(pts) - 1):
        w = (ws[i] + ws[i + 1]) / 2
        out.append(R.seg(part, pts[i], pts[i + 1], w, w, tex, front, ext=0.15))
        out.append(R.seg(part, pts[i], pts[i + 1], w * k * 1.12, w * k * 1.12, tex, f2, ext=0.05))
    return out


def egg(part, c, r, tex, light=0):
    """an egg: five slabs, fuller below the middle"""
    x, y, z = c
    rows = [(-1.0, -0.7, 0.62), (-0.7, -0.2, 0.96), (-0.2, 0.35, 1.0), (0.35, 0.8, 0.82), (0.8, 1.15, 0.5)]
    return stack(R, part, [(y + a * r, y + b * r, w * r * 0.82) for a, b, w in rows], tex, c=(x, z), k=0.66, light=light)


def sparkle3d(part, c, s, light=15):
    """a real sparkle: two crossed see-through planes with the star on them"""
    x, y, z = c
    B(part, (x - s, y - s, z), (x + s, y + s, z + 0.01), 'spark', faces=('north', 'south'), full=True, light=light)
    B(part, (x, y - s, z - s), (x + 0.01, y + s, z + s), 'spark', faces=('east', 'west'), full=True, light=light)


# ---------------------------------------------------------------------------------------------------- the body
def zslab(part, z0, z1, hw, hh, tex, c=(0.0, 0.0), k=0.7, light=0):
    """one rounded slice across the body (an octagon seen from the front: three boxes, none overlapping) between z0 and z1"""
    x, y = c
    return [B(part, (x - hw, y - hh * k, z0), (x + hw, y + hh * k, z1), tex, light=light),
            B(part, (x - hw * k, y + hh * k, z0), (x + hw * k, y + hh, z1), tex, light=light),
            B(part, (x - hw * k, y - hh, z0), (x + hw * k, y - hh * k, z1), tex, light=light)]


def zegg(part, z0, z1, r, tex, yc, n=9, sq=0.84, blunt=1.35, power=1.2, under=None, xs=1.0):
    """a horizontal egg of n slices from z0 (the blunt front) to z1: radius r at its widest (a third of the way back), its
    height sq of its width, its centre line yc(t) (t 0 front .. 1 back); under: a texture for the lower box of each slice"""
    out = []
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n; t = (t0 + t1) / 2
        u = (t - 0.36) / (0.64 if t > 0.36 else 0.36)                 # (-1 at the front, 0 at the widest, 1 at the tail)
        w = r * max(0.0, 1 - abs(u) ** (blunt if u < 0 else 1.6)) ** (0.5 / power)
        w = max(0.6, w)
        es = zslab(part, z0 + (z1 - z0) * t0, z0 + (z1 - z0) * t1, w * xs, w * sq, tex, c=(0.0, yc(t)), k=0.7)
        if under:
            for f in es[2]['faces'].values(): f['texture'] = '#' + under
        out += es
    return out


# the body: a horizontal egg, the breast blunt and low, the back rising gently into the tail
zegg('body', -8.2, 9.4, 5.9, 'gold', lambda t: 8.4 + 2.6 * t * t, n=10, sq=0.78, under='down')
# the breast: proud and low (cream-gold down), a little fuller than the egg's front
zegg('body', -8.9, -0.6, 4.3, 'down', lambda t: 7.3 + 0.5 * t, n=6, sq=0.84, blunt=0.9, power=1.0)
# the PAUNCH: a domestic goose's saggy belly fold, swinging low behind the legs
zegg('body', -0.6, 7.4, 3.9, 'down', lambda t: 4.9 - 0.3 * t, n=5, sq=0.62)
# the back: a flat run of lit covert feathers a hair proud; the tail: short, pointed, upturned
R.seg('body', (0, 13.25, -3.0), (0, 13.9, 6.6), 6.2, 0.6, 'lip', shift=False)
TAIL = [((0, 11.4, 8.2), (0, 12.9, 11.0), 4.6, 2.6), ((0, 12.5, 10.4), (0, 14.0, 12.6), 3.2, 1.7)]
for a, b, w, h in TAIL: R.seg('body', a, b, w, h, 'gold2', ext=0.2)
for sx in (-1, 0, 1):                                                  # (three tail feathers, the middle one longest)
    leaf(R, 'body', (sx * 1.0, 13.4, 11.6), (sx * 1.8, 15.0 - abs(sx) * 0.5, 13.8 + (0 if sx else 0.8)), 1.6, 'prim', up=(0, 1, 0), t=0.4)
# the clover marking on the breast, and the back's sparkles (a cluster of three; one more by the head, on neck2)
B('body', (-1.6, 5.7, -8.95), (1.6, 8.9, -8.93), 'clover', faces=('north',), full=True, light=5)
for c, s in (((-2.8, 15.6, 4.2), 1.6), ((-4.4, 17.4, 5.6), 1.0), ((-1.7, 18.2, 7.0), 0.7)):
    sparkle3d('body', c, s)

# ---------------------------------------------------------------------------------------------------- the neck
N1 = [(0, 10.4, -5.6), (0, 12.6, -7.7), (0, 15.0, -8.4), (0, 17.0, -8.1)]
N2 = [(0, 16.6, -8.2), (0, 18.6, -7.6), (0, 20.4, -7.5), (0, 21.8, -8.0)]
rod('neck1', N1, [3.8, 2.9, 2.5, 2.35], 'neck')
rod('neck2', N2, [2.35, 2.2, 2.2, 2.3], 'neck')
zslab('neck1', -8.4, -4.6, 2.8, 2.2, 'down', c=(0, 10.2), k=0.66)              # (the neck flares into the breast)
sparkle3d('neck2', (2.9, 21.4, -6.0), 0.9)

# ---------------------------------------------------------------------------------------------------- the head
HC = (0, 23.2, -8.8)
zegg('head', -11.6, -6.0, 2.55, 'gold', lambda t: 23.2 + 0.3 * t, n=5, sq=0.92, blunt=1.0, power=1.1)
slab(R, 'head', 25.3, 25.95, 1.45, 'gold', 2.1, c=(0, -8.7), k=0.66)      # (a domed crown)
for sx in (1, -1):                                                              # (cheeks: fuller low on each side, under the eyes)
    B('head', (sx * 2.15 - 0.45, 21.4, -10.6), (sx * 2.15 + 0.45, 23.0, -7.6), 'gold2')
R.seg('head', (0, 25.3, -9.4), (0, 24.4, -11.4), 2.4, 0.9, 'lip', ext=0.1)    # (the brow running into the knob)
# the cowlick: three gold feathers springing up and curling forward
for sx, L, a in ((0, 2.8, 0.0), (0.8, 2.0, 0.4), (-0.8, 1.9, -0.35)):
    cleaf(R, 'head', (sx * 0.6, 25.4, -8.0), (a, 1.0, -0.55), L, 1.1, 'prim', droop=-0.35, t=0.35, n=3, full=False)
# the beak: an upper bill (two tapering spans), its pale nail, the grin patch along its edge, nostrils, the knob with its emerald
R.seg('head', (0, 22.9, -11.2), (0, 22.6, -13.4), 2.5, 1.45, 'beak', ext=0.1)
R.seg('head', (0, 22.55, -13.3), (0, 22.35, -15.0), 1.8, 1.15, 'beak', ext=0.05)
R.seg('head', (0, 22.3, -14.9), (0, 22.15, -15.3), 1.1, 0.78, 'nail')
for sx in (1, -1):
    R.seg('head', (sx * 1.2, 22.2, -11.4), (sx * 0.85, 22.0, -15.0), 0.22, 0.4, 'grin', up=(0, 1, 0))
    B('head', (sx * 0.58 - 0.2, 23.3, -13.4), (sx * 0.58 + 0.2, 23.45, -12.8), 'nostril')
stack(R, 'head', [(23.3, 23.9, 1.2, 0.9), (23.9, 24.8, 1.4, 1.1), (24.8, 25.3, 0.95, 0.75)], 'beak', c=(0, -11.3), k=0.62)
R.box('head', (-0.6, 23.75, -12.55), (0.6, 24.95, -12.2), 'gem', rot=('z', 45.0, (0, 24.35, -12.37)), light=7)
R.box('head', (-0.35, 24.05, -12.62), (0.35, 24.65, -12.5), 'gem', light=10)
# the upper bill's underside: the mouth's roof and the TOOTHED tomia (seen when it honks)
B('head', (-0.9, 21.8, -14.6), (0.9, 22.05, -11.4), 'mouth')
for i in range(6):
    z = -11.7 - i * 0.5
    for sx in (1, -1): B('head', (sx * 0.8 - 0.12, 21.6, z - 0.14), (sx * 0.8 + 0.12, 21.85, z + 0.14), 'tooth')
# the eyes: each on a little gold eye-socket bump (a goofy pop-eye), turned 22 deg toward the front so the face reads head-on;
# the overlay plate sits on the bump's outer face
for sx in (1, -1):
    xc, yc, zc, a = sx * 2.2, 23.7, -10.0, 22.0 * sx
    B('head', (xc - 0.55, yc - 1.35, zc - 1.3), (xc + 0.55, yc + 1.35, zc + 1.3), 'gold2', rot=('y', a, (xc, yc, zc)))
    B('head', (xc - 0.4, yc + 1.3, zc - 1.0), (xc + 0.4, yc + 1.6, zc + 1.0), 'lip', rot=('y', a, (xc, yc, zc)), shift=False)   # (a brow ledge over it)
    x = xc + 0.56 * sx
    B('head', (min(x, x + 0.02 * sx), yc - 1.3, zc - 1.3), (max(x, x + 0.02 * sx), yc + 1.3, zc + 1.3), 'EYES', faces=('east' if sx > 0 else 'west',),
      uv={'east' if sx > 0 else 'west': [0, 0, 3, 3] if sx > 0 else [3, 0, 6, 3]}, light=8, rot=('y', a, (xc, yc, zc)))

# ---------------------------------------------------------------------------------------------------- the jaw (the lower bill)
R.seg('jaw', (0, 21.8, -11.3), (0, 21.55, -13.9), 2.2, 0.8, 'beak_d', ext=0.1)
R.seg('jaw', (0, 21.55, -13.8), (0, 21.4, -14.9), 1.5, 0.7, 'beak_d')
B('jaw', (-0.7, 22.15, -14.1), (0.7, 22.3, -11.6), 'tongue')
for i in range(5):
    z = -12.0 - i * 0.45
    for sx in (1, -1): B('jaw', (sx * 0.48 - 0.1, 22.3, z - 0.12), (sx * 0.48 + 0.1, 22.48, z + 0.12), 'tooth')

# ---------------------------------------------------------------------------------------------------- the wings (folded)
for p, sx in (('wr', 1), ('wl', -1)):
    X = 5.3 * sx
    TILT = (sx * 0.9, 0.42, 0.0)                                          # (the folded wing leans in at its top: it hugs the body)
    R.seg(p, (X - 0.5 * sx, 12.5, -5.0), (X - 0.1 * sx, 12.2, -1.6), 2.6, 1.1, 'lip', up=TILT, ext=0.3)       # (the shoulder)
    R.seg(p, (X, 11.7, -4.0), (X + 0.3 * sx, 11.6, 5.2), 3.4, 1.2, 'gold', up=TILT, ext=0.3)                 # (the coverts)
    R.seg(p, (X + 0.55 * sx, 9.6, -2.6), (X + 0.85 * sx, 9.9, 6.2), 2.6, 0.9, 'gold2', up=(float(sx), 0.18, 0.0), ext=0.2)  # (secondaries)
    R.seg(p, (X - 0.35 * sx, 13.25, -4.2), (X - 0.05 * sx, 13.05, 4.0), 0.9, 1.0, 'lip', up=TILT, shift=False)  # (the lit leading edge)
    for i, (y, dz) in enumerate(((8.3, 0.0), (8.5, 2.6), (8.8, 5.0))):                                       # (the ragged trailing edge)
        leaf(R, p, (X + 0.95 * sx, y + 0.5, -1.0 + dz), (X + 1.0 * sx, y - 0.3, 2.0 + dz), 1.8, 'gold_d', up=(float(sx), 0.1, 0.0), t=0.45)
    for i, (y, z1) in enumerate(((12.6, 11.2), (11.8, 10.8), (11.0, 10.0))):                                 # (three primaries, over the rump)
        leaf(R, p, (X + 0.2 * sx, y, 2.6), (X - (2.2 + i * 0.6) * sx, y + 1.2 - i * 0.25, z1 + 1.2), 1.9, 'prim', up=TILT, t=0.42, tipw=0.4)

# ---------------------------------------------------------------------------------------------------- the legs and the paddles
for p, f, sx in (('legr', 'footr', 1), ('legl', 'footl', -1)):
    x, y, z = PIVOT[p]
    stack(R, p, [(4.2, 5.8, 1.6, 1.5)], 'down', c=(x, z), k=0.6)                    # (the feathered top, into the belly)
    rod(p, [(x, 4.4, z), (x, 2.4, z - 0.15), (x, 0.9, z - 0.25)], [1.2, 1.05, 1.0], 'leg')
    if sx > 0:                                                                         # (the jade bird-band, its right leg)
        stack(R, p, [(2.6, 3.4, 0.78, 0.78)], 'band', c=(x, z - 0.15), k=0.6, light=3)
    fx, fz = PIVOT[f][0], PIVOT[f][2]
    # the paddle: webbing in three stepped plates, widest at the toes, scooped back between them
    B(f, (fx - 0.9, 0.0, fz - 1.6), (fx + 0.9, 0.55, fz + 1.2), 'foot')
    B(f, (fx - 1.7, 0.0, fz - 3.2), (fx + 1.7, 0.5, fz - 1.5), 'foot')
    B(f, (fx - 2.4, 0.0, fz - 4.0), (fx + 2.4, 0.45, fz - 3.1), 'foot')
    for dx, dz in ((0.0, -5.2), (2.6, -4.5), (-2.6, -4.5)):                           # (three toes, each a ridge with a pale claw)
        R.seg(f, (fx, 0.45, fz - 0.4), (fx + dx, 0.4, fz + dz), 0.75, 0.75, 'toe', ext=0.1)
        tx, tz = fx + dx * 1.08, fz + dz - 0.35
        B(f, (tx - 0.32, 0.1, tz - 0.4), (tx + 0.32, 0.6, tz + 0.2), 'claw')
    B(f, (fx - 0.45, 0.3, fz + 0.8), (fx + 0.45, 0.8, fz + 1.5), 'toe')                # (the little hind toe)

# ---------------------------------------------------------------------------------------------------- fx
# HONK: three sound rings bursting out of the beak (see-through, lit), and two little "honk" sparks
for i, (r, z) in enumerate(((1.6, -16.2), (2.6, -18.0), (3.8, -20.2))):
    ring(R, 'honk', (0, 22.4 + i * 0.4, z), r, 10, 0.45 + i * 0.1, 0.25, 'honkring', plane='xy', light=12, ext=0.1)
sparkle3d('honk', (2.8, 25.6, -17.6), 0.7); sparkle3d('honk', (-3.0, 24.4, -18.8), 0.55)
# EGG: a golden egg it has just laid (behind it, under the paunch), with a glint
egg('egg', (0, 1.75, 8.4), 1.75, 'egg', light=2); sparkle3d('egg', (1.1, 3.4, 7.6), 0.45)
# EGGS: the boss's egg drop - three eggs round it, one popped into a burst of confetti and a coin
for (x, z, r) in ((8.0, -6.0, 1.9), (-9.0, -2.0, 1.7), (3.0, 10.0, 1.8)):
    egg('eggs', (x, r, z), r, 'egg', light=2)
for i in range(14):
    a = i * 2.39; rr = 1.5 + (i % 5) * 0.9
    x, y, z = -6.0 + rr * math.cos(a), 1.2 + (i % 4) * 1.6, 7.0 + rr * math.sin(a)
    B('eggs', (x - 0.35, y, z - 0.35), (x + 0.35, y + 0.08, z + 0.35), 'confetti', rot=('y', (i * 37) % 90, (x, y, z)),
      uv={f: [(i % 4) * 4, (i // 4 % 4) * 4, (i % 4) * 4 + 1, (i // 4 % 4) * 4 + 1] for f in ('up', 'down')}, faces=('up', 'down'))
for k, (dx, dz) in enumerate(((-1.2, 0.4), (0.9, -0.5))):                            # (the shell's two halves)
    stack(R, 'eggs', [(0.0, 0.7, 1.4), (0.7, 1.2, 1.7)], 'egg', c=(-6.0 + dx * 1.6, 7.0 + dz * 1.6), k=0.66)
# HELD: the sword it stole, carried crosswise in its beak (blade, guard, grip, pommel)
hx, hy, hz = PIVOT['held']
R.seg('held', (hx + 1.6, hy, hz), (hx + 11.0, hy + 0.6, hz + 0.3), 1.1, 0.3, 'steel')
R.seg('held', (hx + 10.9, hy + 0.6, hz + 0.3), (hx + 11.9, hy + 0.66, hz + 0.32), 0.6, 0.25, 'steel')
R.seg('held', (hx + 1.4, hy - 1.2, hz), (hx + 1.4, hy + 1.2, hz), 0.5, 0.5, 'hilt', up=(0, 0, -1))
R.seg('held', (hx - 2.2, hy - 0.1, hz), (hx + 1.2, hy, hz), 0.55, 0.55, 'hilt')
B('held', (hx - 3.0, hy - 0.5, hz - 0.45), (hx - 2.1, hy + 0.4, hz + 0.45), 'gem', light=4)
# COIN: the lucky coin it flips (a gold disc: two crossed slabs), spinning over its head
cx, cy, cz = PIVOT['coin']
for i in range(3):
    a = i * 60
    R.box('coin', (cx - 2.4, cy - 2.4, cz - 0.25), (cx + 2.4, cy + 2.4, cz + 0.25), 'coin', rot=('z', a, (cx, cy, cz)),
          uv={'north': [0, 0, 16, 16], 'south': [0, 0, 16, 16]}, faces=('north', 'south', 'east', 'west', 'up', 'down') if i == 0 else ('east', 'west', 'up', 'down'))
sparkle3d('coin', (cx + 2.8, cy + 2.2, cz - 0.4), 0.7)
# NEST: a little golden nest it settles into (sitting)
for i in range(10):
    a = math.radians(i * 36)
    R.seg('nest', (7.6 * math.cos(a), 0.9, 7.6 * math.sin(a) + 1), (7.6 * math.cos(a + 0.7), 1.0, 7.6 * math.sin(a + 0.7) + 1), 2.6, 1.8, 'straw', ext=0.4)
stack(R, 'nest', [(0.0, 0.6, 7.8, 7.8)], 'straw', c=(0, 1.0), k=0.62)
for x, z in ((5.6, -3.2), (-5.2, 4.4)): egg('nest', (x, 1.9, z), 1.3, 'egg', light=2)
# AURA (rare: JACKPOT): eight gold coins on a tilted ring round it, motes, and two big sparkles
for i in range(8):
    a = math.radians(i * 45); x, z = 12.0 * math.cos(a), 12.0 * math.sin(a); y = 12.0 + 3.0 * math.sin(a)
    B('aura', (x - 1.2, y - 1.2, z - 0.2), (x + 1.2, y + 1.2, z + 0.2), 'coin', rot=('y', -i * 45 + 90, (x, y, z)), uv={'north': [0, 0, 16, 16], 'south': [0, 0, 16, 16]}, light=12)
for i in range(6):
    a = math.radians(i * 60 + 20); sparkle3d('aura', (9 * math.cos(a), 4 + (i % 3) * 6, 9 * math.sin(a)), 0.6 + (i % 2) * 0.3)
# SHARD: the Dread Sovereign's crown shard, lodged in the top of its head - void-glass, a red heart-crystal core (its own
# textures are the Sovereign's, borrowed: dread_sovereign_art)
import dread_sovereign_art as DSA
_DST = DSA.textures()
for k in ('ds_glass', 'ds_red', 'ds_heart', 'ds_red_l'): R.tex(k[3:], _DST[k])
sx0, sy0, sz0 = PIVOT['shard']
R.seg('shard', (sx0 + 0.4, sy0 - 0.8, sz0 + 0.8), (sx0 + 1.6, sy0 + 4.6, sz0 + 2.2), 1.5, 1.2, 'glass', ext=0.1)
R.seg('shard', (sx0 + 1.6, sy0 + 4.5, sz0 + 2.2), (sx0 + 1.9, sy0 + 6.4, sz0 + 2.9), 0.7, 0.5, 'glass')
R.seg('shard', (sx0 - 0.8, sy0 - 0.6, sz0 + 0.2), (sx0 - 1.8, sy0 + 2.8, sz0 - 0.6), 0.9, 0.8, 'glass')
R.box('shard', (sx0 - 0.5, sy0 + 0.2, sz0 - 0.1), (sx0 + 0.7, sy0 + 1.4, sz0 + 1.1), 'heart', rot=((35.26, 45.0, 0.0), (sx0 + 0.1, sy0 + 0.8, sz0 + 0.5)), light=15)
for i, (a, L) in enumerate(((200, 2.6), (250, 2.0), (320, 2.4), (20, 1.8), (110, 2.2))):          # (red cracks spreading from it)
    t = math.radians(a)
    R.seg('shard', (sx0 + 0.6 * math.cos(t), sy0 - 0.4, sz0 + 0.6 * math.sin(t)), (sx0 + L * math.cos(t), sy0 - 1.2 - 0.3 * i, sz0 + L * math.sin(t)),
          0.3, 0.2, 'red_l', light=12, up=(0, 1, 0))


# ---------------------------------------------------------------------------------------------------- skins
def _pal(P, C, O, E=EMER):
    t = _tex(P, C, O, E)
    return t


ROSE = (dict(deep='#5a2a26', dark='#94544a', base='#d48a7a', light='#f2b4a2', shine='#ffe4d8', white='#fff6f2'),
        dict(dark='#c08a80', base='#ecc0b4', light='#f8dcd2', shine='#fff4f0'), ORANGE)
PLAT = (dict(deep='#3a4048', dark='#727a86', base='#b4bcc6', light='#dde3ea', shine='#ffffff', white='#ffffff'),
        dict(dark='#a8aeb6', base='#d8dce2', light='#eceef2', shine='#ffffff'), dict(deep='#6a2a06', dark='#a8400c', base='#e86e18', light='#ff9e46', hot='#ffd08a'))
SHINY = (dict(deep='#06301a', dark='#0e5a2e', base='#1e9a48', light='#52d470', shine='#fff0a0', white='#fffbe8'),
         dict(dark='#5aa060', base='#9ad890', light='#c8f0b8', shine='#f4ffe8'),
         dict(deep='#5e3a06', dark='#94640e', base='#e8a820', light='#ffd050', hot='#fff0a0'), ('#3a2206', '#8a5a0a', '#d8a020', '#ffe070', '#ffffff'))
GOS = (dict(deep='#8a7020', dark='#c8a840', base='#f2da70', light='#fff0a8', shine='#fffbe0', white='#ffffff'),
       dict(dark='#d8c070', base='#fbeaa0', light='#fff6cc', shine='#ffffff'), dict(deep='#4a3a2a', dark='#6a5a48', base='#8a7a66', light='#b0a08a', hot='#d0c0a8'))


def _cracked(level):
    """the morph's cracks: the gold feathers split by void-dark seams with red light in them (1: a few, 2: everywhere)"""
    out = {}
    rnd = random.Random(90 + level)
    for name in ('gold', 'gold2', 'gold_d', 'neck', 'prim', 'lip', 'down'):
        im = TEX[name].copy(); d = ImageDraw.Draw(im)
        for _ in range(3 if level == 1 else 8):
            x, y = rnd.randrange(0, 64, 2), rnd.randrange(0, 64, 2)
            for i in range(rnd.randint(5, 12)):
                d.rectangle((x - 2, y, x - 1, y + 1), fill=hexc('#1a0c16')); d.rectangle((x, y, x + 1, y + 1), fill=hexc('#ff5a64' if i % 4 == 0 else '#d0182e'))
                x = (x + rnd.choice((-2, 0, 2))) % 64; y = (y + 2) % 64
        if level == 2:
            px = im.load()
            for yy in range(64):
                for xx in range(64):
                    r, g, b, a = px[xx, yy]
                    if a and (r, g, b) != (255, 90, 100) and (r, g, b) != (208, 24, 46): px[xx, yy] = (int(r * 0.7), int(g * 0.6), int(b * 0.7), a)
        out[name] = im
    return out


for sfx, (P, C, O, *E) in (('_rg', ROSE), ('_pt', PLAT), ('_sh', SHINY), ('_gos', GOS)):
    t = _tex(P, C, O, E[0] if E else EMER)
    swap = {}
    for k in ('gold', 'gold2', 'gold_d', 'neck', 'prim', 'down', 'lip', 'beak', 'beak_d', 'leg', 'foot', 'toe', 'egg', 'gem', 'straw'):
        R.tex(k + sfx, t[k]); swap[k] = k + sfx
    R.skin(sfx, swap)
for lv in (1, 2):
    swap = {}
    for k, im in _cracked(lv).items(): R.tex(f'{k}_cr{lv}', im); swap[k] = f'{k}_cr{lv}'
    R.skin(f'_cr{lv}', swap)


# ---------------------------------------------------------------------------------------------------- poses
def P(lift=0.0, **kw):
    return R.ground(kw, lift)


FOLD = dict(wr=limb(1, 0, 0), wl=limb(-1, 0, 0))
POSES = R.POSES
POSES.update({
    'idle_a': P(neck1=T(-4), neck2=T(2), head=T(2)),
    # preening: the neck curled round, the beak buried in its wing (a goose's favourite thing)
    'idle_b': P(_face='blink', neck1=T(-10, 40, 22), neck2=T(-40, 60, 10), head=T(70, 40, 0), wr=limb(1, 0, 12), body=T(0, 0, -4)),
    # looking about: its head cocked, one eye rolled
    'idle_c': P(_face='derp', neck1=T(2, -10), neck2=T(-6, -14, 6), head=T(4, -20, -22)),
    'alert': P(_face='wide', neck1=T(-14), neck2=T(-4), head=T(14), wr=limb(1, 0, 8), wl=limb(-1, 0, 8)),
    # THE WADDLE (4 frames, 16 ticks): the body rocks onto the planted foot (roll 11 deg) and swings its yaw; the lifted foot's toes
    # curl up as it swings through and SLAP down flat; the NECK BENDS BACK each step (neck1 back 16-22 deg, the head tipped forward
    # to keep the beak level) and bobs; the paunch swings (it is on the body: it goes with the roll)
    'walk_0': P(body=T(2, 6, 11), legr=limb(1, -14, -11), legl=limb(-1, 26, -11), footl=limb(-1, -30), footr=limb(1, 0),
                neck1=T(-30, -4, -8), neck2=T(-14), head=T(44, 0, 4)),
    'walk_1': P(body=T(4, 0, 0), legr=limb(1, 6, 0), legl=limb(-1, 6, 0), neck1=T(-18), neck2=T(-6), head=T(26)),
    'walk_2': P(body=T(2, -6, -11), legl=limb(-1, -14, 11), legr=limb(1, 26, 11), footr=limb(1, -30), footl=limb(-1, 0),
                neck1=T(-30, 4, 8), neck2=T(-14), head=T(44, 0, -4)),
    'walk_3': P(body=T(4, 0, 0), legr=limb(1, 6, 0), legl=limb(-1, 6, 0), neck1=T(-18), neck2=T(-6), head=T(26)),
    # THE RUN (2 frames, 6 ticks): pitched forward, wings flailing, legs a blur - and the neck and head FLAP BEHIND IT like a flag:
    # neck1 thrown back past 60 deg, neck2 whipping the other way, the head dangling, the beak open
    'run_0': P(_face='wide', body=T(16, 0, 6), legr=limb(1, -60, -6), legl=limb(-1, 40, -6), footl=limb(-1, -45),
               neck1=T(-24, 0, -8), neck2=T(-46, 0, 16), head=T(-70, 14, 28), jaw=T(30), wr=limb(1, 0, 34, -20), wl=limb(-1, 0, 70, -20)),
    'run_1': P(_face='derp', body=T(20, 0, -6), legl=limb(-1, -60, 6), legr=limb(1, 40, 6), footr=limb(1, -45),
               neck1=T(-20, 0, 14), neck2=T(-50, 0, -24), head=T(-56, -28, -44), jaw=T(36), wr=limb(1, 0, 70, 10), wl=limb(-1, 0, 30, 10)),
    # HONK: a wind-up (neck coiled back, breast puffed, 6 ticks) - then the neck snaps forward and up, wings flung out, the jaw
    # drops and the rings burst (the hit, 2 ticks), held 6, settle 6
    'honk_up': P(_face='fierce', body=T(-8), neck1=T(-30), neck2=T(-20), head=T(30), wr=limb(1, 0, 30), wl=limb(-1, 0, 30)),
    'honk': P(_face='honk', _show=('honk',), body=T(6), neck1=T(24), neck2=T(-6), head=T(-30), jaw=T(36), wr=limb(1, 0, 95, -25), wl=limb(-1, 0, 95, -25)),
    # THE WADDLE CHARGE: the goose's own threat - head low and forward, neck snaking out level, beak open hissing, wings half up
    'charge': P(_face='fierce', body=T(16), neck1=T(62), neck2=T(-10), head=T(-36), jaw=T(20), wr=limb(1, 0, 40), wl=limb(-1, 0, 40),
                legr=limb(1, -24), legl=limb(-1, 30), footl=limb(-1, -30)),
    # NECK-WHIP SLAP: the neck swung out to its right and back in like a wet towel (wind-up 4, slap 2)
    'slap_up': P(_face='fierce', neck1=T(-10, 50, -30), neck2=T(0, 30, -20), head=T(10, 30)),
    'slap': P(_face='honk', neck1=T(20, -60, 50), neck2=T(10, -40, 30), head=T(-10, -30, 20), jaw=T(16), body=T(0, -14, 0)),
    # THE EGG: a squat, a strain, a pop (the egg is behind it, at its feet), and pride
    'lay': P(_face='blink', _show=('egg',), _o_body=(0, -1.4, 0), body=T(-6), neck1=T(-8), neck2=T(4), head=T(4), legr=limb(1, 0, 12), legl=limb(-1, 0, 12)),
    'proud': P(_face='smug', _show=('egg',), body=T(-10), neck1=T(-16), neck2=T(-4), head=T(-10), wr=limb(1, 0, 14), wl=limb(-1, 0, 14)),
    'eggs': P(_face='happy', _show=('eggs',), body=T(-6), neck1=T(-10), head=T(-8), wr=limb(1, 0, 60), wl=limb(-1, 0, 60)),
    # THE THIEF: your sword in its beak, running off with it (the run's legs, the neck up and smug)
    'steal': P(_face='smug', _show=('held',), body=T(14, 0, 6), legr=limb(1, -34), legl=limb(-1, 40), footl=limb(-1, -40),
               neck1=T(-30), neck2=T(-6), head=T(22), wr=limb(1, 0, 40, -10), wl=limb(-1, 0, 40, -10)),
    # THE LUCKY COIN: it flips a coin with its beak and watches it spin
    'coin': P(_face='wide', _show=('coin',), neck1=T(-20), neck2=T(-14), head=T(-24), jaw=T(12)),
    'happy': P(_face='happy', lift=1.0, wr=limb(1, 0, 80, -10), wl=limb(-1, 0, 80, -10), neck1=T(-10), head=T(-6)),
    'hurt': P(_face='honk', body=T(-12, 0, 10), neck1=T(-30, 0, -20), neck2=T(-10), head=T(-10), jaw=T(20), wr=limb(1, 0, 50), wl=limb(-1, 0, 30)),
    'dazed': P(_face='dizzy', body=T(-4, 0, 8), legr=limb(1, 80, 20), legl=limb(-1, 70, 20), neck1=T(-10, 0, 26), neck2=T(0, 0, 20), head=T(0, 0, 24)),
    # SITTING (right-click): it plops down, its big feet sticking out in front, toes up; idle: a head-bob
    'sit_a': P(_face='happy', body=T(-14), legr=limb(1, 88, 16), legl=limb(-1, 88, 16), footr=limb(1, -24), footl=limb(-1, -24),
               _o_legr=(0.6, 0.4, -4.6), _o_legl=(-0.6, 0.4, -4.6),
               neck1=T(-2), head=T(-4)),
    # SNEAK + RIGHT-CLICK: settled in its golden nest, head tucked under its wing - a sleeping goose
    'sit_b': P(_face='blink', _show=('nest',), _hide=('legr', 'legl', 'footr', 'footl'), _o_body=(0, -3.4, 0), body=T(0),
               neck1=T(-55, 0, 0), neck2=T(-52, 0, 10), head=T(-50, 10, 30)),
    'shard': P(_face='wide', _show=('shard',), body=T(-6), neck1=T(-20, 0, 8), neck2=T(-6), head=T(10, 0, 10), wr=limb(1, 0, 30), wl=limb(-1, 0, 30)),
    'aura': P(_face='smug', _show=('aura',)),
    # (the doll's pose: the neck leant back 61 deg so the head's joint stands on the doll's vertical axis - dolls_bake grows the head
    #  group about that axis (x = z = 0), so a head held forward would float off its neck; the head tipped forward again, face level)
    'doll': P(neck1=T(-36.6), neck2=T(-24.4), head=T(65)),
})
DRAFT = list(POSES)
R.DRAFT = DRAFT
DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62}
DOLL_GROUPS = {'head': 'head', 'jaw': 'head', 'neck2': 'body', 'neck1': 'body', 'body': 'body', 'wr': 'body', 'wl': 'body',
               'legr': 'legs', 'legl': 'legs', 'footr': 'legs', 'footl': 'legs'}
SHINY_NAME = 'Shiny Four-Leaf'

# ATTACKS of the boss's phase 1 (ticks; see the design doc) and the follower's moves - for the wiring stage
ATTACKS = {
    'honk': dict(poses=('honk_up', 'honk'), windup=6, hit=7, hold=6, recover=6, dmg=2, radius=4.5, knock=1.4, cd=6,
                 fx='three sound rings out of the beak; everyone in a 60-deg cone 4.5 blocks long knocked back 1.4 and Slowness I 2 s'),
    'charge': dict(poses=('charge',), windup=10, hit=None, run=30, dmg=4, speed=0.42, cd=9,
                   fx='a hissing waddle-charge straight at you for 1.5 s; it bonks into walls (stunned 20 ticks, a little star burst)'),
    'eggs': dict(poses=('eggs',), windup=8, hit=12, fuse=30, n=3, dmg=3, cd=12,
                 fx='three golden eggs lobbed round you; each wobbles 30 ticks then POPS - confetti and a coin (2 dmg) or, 1 in 4, a Lucky Token'),
    'slap': dict(poses=('slap_up', 'slap'), windup=4, hit=5, hold=2, recover=6, dmg=5, reach=2.6, cd=4, fx='the neck as a wet towel: knockback 0.8 sideways'),
    'steal': dict(poses=('steal',), windup=3, hit=4, run=60, cd=25,
                  fx='it snatches your MAIN-HAND item (never a soulbound one) and runs; hit it 3 times to make it drop it (it honks, outraged)'),
    'coin': dict(poses=('coin',), windup=6, flip=20, cd=18, fx='HEADS: it gets Speed II and Resistance 5 s. TAILS: everyone near gets Luck II 10 s and it sulks (vulnerable, 3 s)'),
}

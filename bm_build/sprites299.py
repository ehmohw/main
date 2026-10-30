"""2.99: THE FOLLOWERS' SUMMONING ITEMS, drawn again - every one the 2.80 repaint never reached.

The 2.80 pass (sprites280..280e) redrew the summons of its day - Cecil's gem to Fishy's bowl. The followers since came with
quick icons of their own: one-pixel lines and flat fills with no outline (Dennis's horn to Mr. Capshun's pencil), or drawn
at 16 and blown up to 32 x 32 so that vanilla.process never finished them (Kettle's plane, the Gentry's tokens, the doodles,
the Herald's feather) - and the Gem of Creativity was a square cut out of its swirl. Each is drawn here again at 16 x 16 in
sprites280's kit and its look: a bold silhouette filling the slot, 4-5 step shading lit from the top left, a dark outline,
then vanilla.process's light and tinted outline - and each still says whose it is.

Their items, models and names are unchanged; sprites280.every_override merges these last (they win), and sprites280.post
writes them over the old textures. (Each old icon's own code stays where it was - rigpet still hands it to R.ICONS - but
these are what the pack ships; the frames, dolls and figurines are models of their own and don't use either.)
Before / after sheets: previews/v299_items/.

Omega's monocle (a 2.80d icon) is here too: its rim had no outline. Left as they were, already in the pack's look: Ashur's
cinder, Ava's locket, the Sovereign's eye (undercrown_art) and Vexis's link (armada_art)."""
import colorsys
import math
from sprites280 import S, GOLD, RED, TEAL, PINK, GLASS, WOOD
from sprites280b import ramp

L = (-0.6, -0.8)                                        # the light: from the top left


def _lit(nx, ny, nz, n):
    v = -(nx * L[0] + ny * L[1]) * 0.75 + nz * 0.55
    return max(0, min(n - 1, int((v + 0.45) / 1.5 * n)))


def tube(s, pts, r, col, samples=80):
    """a rounded rod along a bezier through pts (2-4 control points), its radius r(t) (or a number); col(t) gives the ramp
    (dark -> light) at t, lit as a cylinder from the top left"""
    n = len(pts) - 1

    def at(t):
        x = y = 0.0
        for i, (px, py) in enumerate(pts):
            b = math.comb(n, i) * (1 - t) ** (n - i) * t ** i
            x += b * px; y += b * py
        return x, y
    rf = r if callable(r) else (lambda t: r)
    cf = col if callable(col) else (lambda t: col)
    S_ = [(i / samples,) + at(i / samples) for i in range(samples + 1)]
    for y in range(16):
        for x in range(16):
            best = None
            for t, cx, cy in S_:
                rr = rf(t)
                d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
                if d <= rr and (best is None or d / rr < best[0]):
                    best = (d / rr, t, cx, cy, rr)
            if best:
                _, t, cx, cy, rr = best
                nx, ny = (x + 0.5 - cx) / rr, (y + 0.5 - cy) / rr
                nz = math.sqrt(max(0.0, 1 - nx * nx - ny * ny))
                rp = cf(t)
                if rp is not None: s.px(x, y, rp[_lit(nx, ny, nz, len(rp))])
    return s


def ball(s, cx, cy, r, rp, sq=1.0):
    return s.disc(cx, cy, r, rp, light=L, sq=sq)


def grid(s, rows, pal, x0=0, y0=0):
    return s.g(rows, pal, x0, y0)


def strings(im, pts, only_clear=True):
    """threads and cords, laid on after the finish: one pixel wide with no outline of their own (an outline round a
    one-pixel thread turns it into a black bar). pts: (x, y, colour)"""
    from sprites280 import hx
    px = im.load()
    for x, y, c in pts:
        if not only_clear or px[x, y][3] == 0: px[x, y] = hx(c)
    return im


# palettes not in sprites280 (dark -> light)
SILVER = ['#4a4e58', '#7c828e', '#aab0bc', '#d4d8e0', '#f6f8fc']
IVORY = ['#7a6a4a', '#b0a07a', '#d8ccaa', '#efe6cc', '#fffbee']
LILAC = ramp('#b08ad8')
CRAYON = ramp('#4cb848')
PAPER = ['#8a7e66', '#b8ac90', '#dcd4bc', '#f2ecdc', '#fffcf4']
WHITE = ['#8a8e9a', '#b8bcc6', '#dcdfe6', '#f2f4f8', '#ffffff']
INK = ['#0c0c18', '#1c1c30', '#2e2e4a', '#46466a', '#6a6a96']
SHROOM = ['#1c3a8a', '#2a5ad0', '#3e7cf0', '#6aa8ff', '#b8dcff']
LIME = ['#4a6a10', '#7aa018', '#a8cc2a', '#d0ec5a', '#f0ffb0']
ORANGE = ['#7a2a06', '#c04a0a', '#ec7418', '#ffa040', '#ffd890']
CART = ['#3a3a44', '#5c5c68', '#82828e', '#a4a4b0', '#c8c8d2']
SUNY = ['#a05a08', '#e0900e', '#ffc020', '#ffe060', '#fff8c0']


# ================================================================== the 2.80d pair, Omega's court and the Lantern's crew
def dw_horn():
    """Dennis's Horn: a curled ivory horn off his helmet - ridged, its open mouth rimmed in gold, a gold band, a gold
    mouthpiece at its curled tip"""
    s = S()
    RIDGE = ['#6a5a3c', '#9a8a68', '#c4b690', '#e0d4b0', '#f4ecd2']

    def col(t):
        if 0.46 < t < 0.54 or t > 0.92: return GOLD
        return RIDGE if int(t * 14) % 2 else IVORY
    tube(s, [(4.6, 4.0), (4.0, 13.0), (11.0, 15.0), (14.2, 9.0)], lambda t: 3.3 - 2.5 * t, col, samples=140)
    for y in range(16):                                                               # the mouth: a gold rim, the dark inside
        for x in range(16):
            e = ((x + 0.5 - 4.6) / 3.6) ** 2 + ((y + 0.5 - 3.4) / 1.7) ** 2
            if e <= 1.0: s.px(x, y, GOLD[4] if x < 3 else GOLD[3] if x < 6 else GOLD[2])
            if ((x + 0.5 - 4.6) / 2.4) ** 2 + ((y + 0.5 - 3.4) / 0.8) ** 2 <= 1.0: s.px(x, y, '#3a2810')
    return s.render()


def pi_cloche():
    """Pistachio's Little Cloche: a silver dome and knob on a wide plate - his green ghost-light curling out from under the rim"""
    s = S()
    for y in range(16):
        for x in range(16):
            dx, dy = (x + 0.5 - 8.0) / 6.0, (y + 0.5 - 10.5) / 7.0
            if dy <= 0 and dx * dx + dy * dy <= 1.0:
                nz = math.sqrt(max(0, 1 - dx * dx - dy * dy)); s.px(x, y, SILVER[_lit(dx, dy, nz, 5)])
    s.g(['.ss.', 'sSSs'], {'s': SILVER[3], 'S': SILVER[1]}, 6, 1)                    # the knob
    s.px(6, 1, SILVER[4])
    for x, y in ((4, 6), (5, 5), (4, 7)): s.px(x, y, '#ffffff')                       # its shine
    for x in range(1, 15): s.px(x, 11, SILVER[4] if x < 6 else SILVER[3])             # the plate
    for x in range(0, 16): s.px(x, 12, SILVER[2] if x < 9 else SILVER[1])
    for x in range(2, 14): s.px(x, 13, SILVER[0])
    G = ['#2a8a5a', '#5ad890', '#a8ffc8']                                              # the ghost-light: wisps out of the rim
    for x in range(2, 14): s.px(x, 10, G[1] if 3 < x < 12 else G[0])
    s.px(6, 10, G[2]); s.px(9, 10, G[2])
    return strings(s.render(), [(1, 9, G[1]), (0, 8, G[1]), (0, 7, G[2]), (14, 9, G[1]), (15, 8, G[1]), (15, 7, G[2]), (14, 6, G[2])])


def om_monocle():
    """Omega's Monocle: a thick gold rim, its glass clear (you see the slot through it) with a glint, a gold chain off it"""
    s = S()
    s.ring(6.6, 6.6, 5.6, 5.6, 2.0, GOLD, light=L)
    for y in range(16):
        for x in range(16):
            d = math.hypot(x + 0.5 - 6.6, y + 0.5 - 6.6)
            if d < 3.7: s.px(x, y, (232, 240, 236, 96) if x + y > 10 else (250, 252, 246, 140))
    s.px(4, 5, '#ffffff'); s.px(5, 4, '#ffffff'); s.px(4, 6, (255, 255, 255, 200))
    im = s.render()
    return strings(im, [(11, 12, GOLD[1]), (12, 12, GOLD[3]), (12, 13, GOLD[2]), (13, 14, GOLD[1]), (13, 15, GOLD[3]), (14, 15, GOLD[2])])


def chef_ladle():
    """the Golden Ladle: a deep round gold bowl, a long gold handle with a hooked end, soup in the bowl"""
    s = S()
    tube(s, [(8.2, 8.0), (11.0, 4.0), (13.4, 1.2)], 0.95, GOLD)                       # the handle
    s.px(14, 2, GOLD[2]); s.px(14, 3, GOLD[1])                                       # its hook
    ball(s, 5.6, 11.0, 4.4, GOLD)                                                     # the bowl
    for x in range(16):
        for y in range(16):
            if y <= 8 and (x, y) in s.p and math.hypot(x + 0.5 - 5.6, y + 0.5 - 11.0) <= 4.4: s.px(x, y, None)
    for x in range(2, 10): s.px(x, 8, GOLD[1] if x in (2, 9) else GOLD[3])           # the lip
    for x in range(3, 9): s.px(x, 9, '#c8601a')                                       # the soup
    s.px(4, 9, '#f09a40'); s.px(5, 9, '#ffc070')
    s.px(3, 11, GOLD[4]); s.px(3, 12, GOLD[4])
    return s.render()


def neighbor_baton():
    """the Neighbor's Baton: a slim black baton on the diagonal, a cork grip at its foot, its tip worn pale; a note beside it"""
    s = S()
    BAT = ['#141418', '#2a2a32', '#44444e', '#62626e', '#8a8a98']

    def col(t):
        if t < 0.22: return ['#5a3a1e', '#8a5e34', '#b88850', '#d8ac70', '#f0d098']  # the cork grip
        if t > 0.86: return ['#8a8478', '#bab4a6', '#ddd8cc', '#f2eee4', '#ffffff']  # the worn pale tip
        return BAT
    tube(s, [(2.6, 13.4), (13.4, 2.6)], lambda t: 1.9 if t < 0.2 else 1.05, col)
    s.g(['..NN', '..Nn', '..N.', 'NNN.', 'NNN.'], {'N': '#3a7ae0', 'n': '#8ab8ff'}, 10, 9)   # a quaver
    s.px(10, 12, '#8ab8ff')
    return s.render()


def pq_pearls():
    """Queen Pearl's Pearls: a loop of round pearls, a pink clasp at the top, a teardrop pendant - and one chocolate pearl"""
    s = S()
    PEARL = ['#9a9488', '#c8c2b4', '#e8e4da', '#fbf8f0', '#ffffff']
    pts = []
    for k in range(13):
        a = math.pi * (-0.5 + 2 * k / 13)
        pts.append((8 + 5.6 * math.cos(a), 7.6 + 5.4 * math.sin(a)))
    for k, (x, y) in enumerate(pts):
        if k == 0: continue
        rp = ['#3a2010', '#5a3418', '#7a4a24', '#9a6436', '#b8804a'] if k == 4 else PEARL
        ball(s, x, y, 1.45, rp)
    s.g(['.pp.', 'pPPp', '.pp.'], {'p': PINK[3], 'P': PINK[1]}, 6, 1)                 # the clasp
    s.px(7, 1, PINK[4])
    s.g(['.T.', 'TtT', 'TtT', '.T.'], {'T': TEAL[2], 't': TEAL[4]}, 7, 12)            # the pendant
    return s.render()


def bo_claw():
    """Bloo's Claw: a great curved white claw, its root wrapped in braided bark, a loop of bark cord at its root"""
    s = S()
    CLAW = ['#7e8494', '#b4bac6', '#dadee6', '#f2f4f8', '#ffffff']
    tube(s, [(5.2, 12.0), (5.0, 5.0), (10.0, 1.6), (14.4, 4.0)], lambda t: max(0.6, 3.4 * (1 - t) ** 0.85), CLAW, samples=120)
    BK = ['#3a2410', '#5e3e1e', '#80582e', '#a07444', '#c09060']
    tube(s, [(4.0, 14.0), (5.6, 11.0)], 2.4, lambda t: BK if int(t * 5) % 2 else ['#2a1a0c', '#4a2e16', '#6a4422', '#8a5c32', '#a87444'])
    s.ring(2.6, 12.4, 2.4, 2.6, 0.9, BK)                                              # the cord's loop
    s.px(4, 7, '#ffffff'); s.px(4, 6, '#ffffff'); s.px(5, 5, '#ffffff')
    return s.render()


def st_hook():
    """the Hollow Hook: a long olive-dark hooked claw, ridged, its point wet red"""
    s = S()
    HK = ['#1e2614', '#34401e', '#4e5c2c', '#6c7c3e', '#94a45a']

    def col(t):
        if t > 0.93: return RED
        return HK if int(t * 9) % 3 else ramp('#3a4422')
    tube(s, [(3.0, 14.0), (5.0, 7.0), (6.0, 1.0), (14.0, 1.6), (12.4, 7.2)], lambda t: max(0.6, 2.2 - 1.6 * t), col, samples=140)
    return s.render()


def ln_gourd():
    """the Kindled Gourd: a little carved pumpkin-gourd, a stalk and a curl of vine, its face burning, eight legs' worth of glow"""
    s = S()
    ball(s, 8.0, 9.6, 6.2, ORANGE, sq=0.86)
    for x in (5, 10):                                                                 # its ribs
        for y in range(5, 15):
            if (x, y) in s.p and y not in (5, 14): s.px(x, y, ORANGE[1])
    s.g(['.ss', 'sSs', '.S.'], {'s': '#5a8a2a', 'S': '#2e5a16'}, 7, 1)                # the stalk
    s.px(10, 2, '#5a8a2a'); s.px(11, 1, '#5a8a2a'); s.px(12, 2, '#3a6a1a')           # a curl of vine
    F = {'f': '#ffe85a', 'F': '#fff8c0', 'k': '#4a1404'}                              # the carved face, alight
    s.g(['f..f.', 'Ff.Ff'], F, 5, 8); s.g(['f...f', 'kffff'], F, 5, 11)
    s.g(['f.f.f'], F, 6, 12)
    s.px(9, 9, F['F'])
    return s.render()


def bv_ball():
    """Bender's Ball: a fuzzy green-yellow ball with its white seam, chewed - a bite out of it"""
    s = S()
    ball(s, 8.0, 8.4, 6.3, LIME)
    seam = [(2, 6), (3, 6), (4, 7), (5, 8), (5, 9), (5, 10), (6, 11), (7, 12), (8, 13), (14, 9), (13, 9), (12, 8), (11, 7),
            (11, 6), (10, 5), (9, 4), (8, 3)]
    for x, y in seam: s.px(x, y, '#f4f8e0')
    for x, y in ((12, 3), (13, 4), (12, 4), (13, 3)): s.px(x, y, None)                # a bite out of it
    s.px(11, 4, LIME[1]); s.px(12, 5, LIME[1]); s.px(13, 5, LIME[2])
    s.px(4, 4, LIME[4]); s.px(5, 3, LIME[4])
    return s.render()


def bn_whistle():
    """Bones's Whistle: a big white shark's tooth - a broad tan root, the blade narrowing to its point, serrated edges, a
    hole bored through - hung on a thin cord of kelp"""
    s = S()
    T = ['#8a8270', '#bcb4a0', '#e2dccc', '#f6f2e6', '#ffffff']
    rows = ['rrrrrrrrrrrr',
            'rrrrrrrrrrrR',
            'TTTrrrrrrTTT',
            '.TTTTrrTTTTT',
            '.TTTTTTTTTT.',
            '..TTTTTTTTT.',
            '..TTTTTTTT..',
            '...TTTTTTT..',
            '...TTTTTT...',
            '....TTTTT...',
            '.....TTT....',
            '......T.....']
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch == '.': continue
            x, y = 2 + i, 4 + j
            if ch in 'rR': s.px(x, y, '#c8a070' if j == 0 and i < 6 else '#7a5a36' if ch == 'R' or i > 8 else '#a88050'); continue
            edge_l = i == 0 or row[i - 1] == '.'
            edge_r = i == len(row) - 1 or row[i + 1] == '.'
            s.px(x, y, T[4] if edge_l or (i < 4 and j < 5) else T[1] if edge_r else T[3] if i < 6 else T[2])
    for x, y in ((3, 8), (4, 10), (5, 12), (13, 8), (12, 10), (11, 12)): s.px(x, y, None)   # its serrations
    s.px(7, 5, '#3a2a1a'); s.px(8, 5, '#3a2a1a')                                     # the hole
    K = '#3e6a2a'
    return strings(s.render(), [(5, 3, K), (5, 2, K), (6, 1, K), (7, 0, K), (8, 0, K), (9, 1, K), (10, 2, K), (10, 3, K)])


def capshun_pencil():
    """Mr. Capshun's Pencil: a chunky yellow pencil on the diagonal - sharpened point, a pink eraser well chewed, a tin ferrule"""
    s = S()
    YEL = ['#9a6a08', '#d8a010', '#f8c828', '#ffe060', '#fff4b0']

    def col(t):
        if t < 0.14: return PINK                                                     # the chewed eraser
        if t < 0.24: return SILVER                                                   # the ferrule
        if t < 0.80: return YEL
        if t < 0.93: return ['#8a6a44', '#b8946a', '#d8b88c', '#ecd6b0', '#fff0d6']  # the bare wood
        return ['#101014', '#202028', '#34343e', '#4a4a56', '#6a6a78']               # the graphite
    tube(s, [(2.4, 13.6), (13.8, 2.2)], lambda t: 0.6 if t > 0.95 else 1.1 + (0.0 if t < 0.8 else -2.6 * (t - 0.8)) + 0.8, col)
    for x, y in ((2, 12), (3, 14)): s.px(x, y, PINK[1])                               # tooth marks
    for t in (0.34, 0.5, 0.66):                                                       # its facets
        x = 2.4 + 11.4 * t; y = 13.6 - 11.4 * t
        s.px(round(x) + 1, round(y) + 1, YEL[1])
    return s.render()


# ================================================================== 2.94-2.99
def kettle_plane():
    """Kettle's Paper Plane: a crisp white plane flying up-right, its fold down the middle, KETTLE scrawled on a wing (a red
    wobble), a crayon star"""
    s = S()
    W_ = WHITE
    rows = ['..............A.',
            '............AAB.',
            '..........AAAAB.',
            '........AAAAABB.',
            '......AAAAAABBC.',
            '....AAAAAAABBCC.',
            '..AAAAAAAAABBC..',
            'AAAAAAAAAABBCC..',
            '.....DDDDBBCC...',
            '.......DDBCC....',
            '........DCC.....',
            '........CC......',
            '.......CC.......',
            '......C.........']
    grid(s, rows, {'A': W_[3], 'B': W_[1], 'C': W_[2], 'D': W_[2]}, 1, 1)
    for x in range(5, 11): s.px(x, 7 - (x - 5) // 2, W_[4])                          # the top wing's lit edge
    for x, y in ((4, 7), (6, 6), (7, 7), (9, 5), (10, 6), (8, 6)): s.px(x, y, '#3a5ad8')        # KETTLE, in wobbly blue crayon
    return s.render()


def henry_tag():
    """Henry's Collar Tag: a round silver tag on its ring, hung from a strap of red collar, a paw stamped on its face"""
    s = S()
    tube(s, [(0.4, 3.6), (8.0, 1.0), (15.6, 3.6)], 1.45, ramp('#d02a30'))   # the red collar
    for x, y in ((2, 3), (4, 2), (11, 2), (13, 3)): s.px(x, y, '#4a0a10')             # the collar's holes
    s.ring(8.0, 4.4, 1.6, 1.8, 0.9, SILVER)                                           # the tag's ring
    ball(s, 8.0, 10.2, 5.0, SILVER)                                                   # the tag
    s.g(['.k.k.', 'k...k', '.kkk.', '.kkk.'], {'k': '#646a78'}, 6, 8)                 # a paw print
    s.px(5, 7, '#ffffff'); s.px(4, 8, SILVER[4])
    return s.render()


def nia_bell():
    """Nia's Bell: a round gold cat-bell (its band, its slot) hung from a strap of lilac collar, a soft shine"""
    s = S()
    tube(s, [(0.4, 3.6), (8.0, 1.0), (15.6, 3.6)], 1.45, LILAC)          # the lilac collar
    for x, y in ((2, 3), (4, 2), (11, 2), (13, 3)): s.px(x, y, '#3a2058')             # the collar's holes
    s.ring(8.0, 4.4, 1.6, 1.8, 0.9, GOLD)                                             # its loop
    ball(s, 8.0, 10.4, 5.0, GOLD)                                                     # the bell
    for x in range(4, 13): s.px(x, 10, GOLD[1] if x > 4 else GOLD[2])                 # its band
    s.g(['k', 'k', 'K'], {'k': '#5a3a08', 'K': '#3a2404'}, 8, 11)                     # the slot
    s.px(7, 12, '#5a3a08'); s.px(9, 12, '#5a3a08')
    s.px(5, 7, '#ffffff'); s.px(6, 7, GOLD[4]); s.px(5, 8, GOLD[4])
    return s.render()


def creativity_gem():
    """the Gem of Creativity: an emerald-cut gem standing tall - a pale table at its heart, the rainbow swirling out from it,
    a white doodle (a little heart) floating in it, a sparkle"""
    s = S()
    W, H, C = 5.6, 7.2, 2.4
    cx, cy = 8.0, 8.0
    for y in range(16):
        for x in range(16):
            dx, dy = x + 0.5 - cx, y + 0.5 - cy
            if abs(dx) > W or abs(dy) > H or abs(dx) + abs(dy) > W + H - C: continue
            a = (math.atan2(dy, dx) / (2 * math.pi) + math.hypot(dx, dy) * 0.045) % 1.0
            inner = abs(dx) <= W * 0.5 and abs(dy) <= H * 0.58 and abs(dx) + abs(dy) <= (W + H - C) * 0.55
            l = 0.66 if inner else 0.52
            lit = -(dx / W * L[0] + dy / H * L[1])
            l = max(0.25, min(0.88, l + lit * 0.14))
            r, g, b = colorsys.hls_to_rgb(a, l, 0.95 if not inner else 0.8)
            s.px(x, y, (round(r * 255), round(g * 255), round(b * 255), 255))
    # the facet lines: the table's edge, the corners running out to the girdle
    for y in range(16):
        for x in range(16):
            dx, dy = x + 0.5 - cx, y + 0.5 - cy
            on = abs(abs(dx) - W * 0.5) < 0.5 and abs(dy) <= H * 0.58 or abs(abs(dy) - H * 0.58) < 0.5 and abs(dx) <= W * 0.5
            if on and (x, y) in s.p:
                c = s.p[(x, y)]
                s.px(x, y, tuple(min(255, v + 70) for v in c[:3]) + (255,) if dx + dy < 0 else tuple(v * 3 // 4 for v in c[:3]) + (255,))
    s.g(['w.w', 'www', '.w.'], {'w': '#ffffff'}, 7, 7)                                # a doodle heart
    s.px(4, 2, '#ffffff'); s.px(3, 3, '#ffffff'); s.px(4, 3, '#fff6c0'); s.px(5, 3, '#ffffff'); s.px(4, 4, '#ffffff')
    return s.render()


def _token(motif):
    """the Gutter Gentry's Calling Tokens: a struck brass token, a raised rim, a worn face, its owner stamped on it"""
    s = S()
    BR = ['#4a3410', '#7a5a22', '#a88a42', '#cdb468', '#f0e0a0']
    s.disc(8.0, 8.0, 7.2, BR, light=L)
    s.ring(8.0, 8.0, 7.2, 7.2, 1.6, BR, light=L)
    FACE = ['#5a4416', '#8a6c2e', '#b0944c', '#c8ae66']
    for y in range(16):
        for x in range(16):
            d = math.hypot(x + 0.5 - 8, y + 0.5 - 8)
            if d < 5.6: s.px(x, y, FACE[2] if (x + y) > 13 else FACE[3])
    for y in range(16):
        for x in range(16):
            d = math.hypot(x + 0.5 - 8, y + 0.5 - 8)
            if 5.0 <= d < 5.6 and (x, y) in s.p: s.px(x, y, FACE[1] if x + y < 15 else FACE[3])
    motif(s)
    return s.render()


def gentry_batty():
    """Batty's token: tarnished brass, a little bat stamped on it in dark relief, green tarnish at the rim"""
    def m(s):
        s.g(['K.........K',
             'KK..K.K..KK',
             'KKK.KKK.KKK',
             'KKKKKyKKKKK',
             '.KKKKKKKKK.',
             '..K.KKK.K..',
             '.....K.....'], {'K': '#3a2a4a', 'y': '#ffd040'}, 3, 5)
        s.px(8, 8, '#3a2a4a'); s.px(7, 8, '#ff5a5a'); s.px(9, 8, '#ff5a5a')
        for x, y in ((2, 11), (3, 12), (12, 13), (13, 4), (12, 3)): s.px(x, y, '#5a8a6a')   # tarnish
    return _token(m)


def gentry_eggbert():
    """Eggbert's token: an egg stamped on it, a crack right across the token, yolk dripping from the crack"""
    def m(s):
        s.g(['..EE..', '.EeEE.', 'EeEEEE', 'EEEEEE', 'EEEEEE', '.EEEE.'], {'E': '#f4f0e0', 'e': '#ffffff'}, 5, 3)
        for x, y in ((1, 9), (2, 9), (3, 8), (4, 8), (5, 7), (6, 8), (7, 7), (8, 8), (9, 7), (10, 8), (11, 8), (12, 9), (13, 9), (14, 8)):
            s.px(x, y, '#2a1a08')                                                     # the crack
        s.g(['Y', 'Y', 'y'], {'Y': '#ffb820', 'y': '#ffe070'}, 9, 9)                  # the drip
        s.px(10, 9, '#ffb820'); s.px(9, 12, '#ffb820')
    return _token(m)


def gentry_count():
    """the Count's token: an engraved top hat with a red band, very proper, a tiny monocle-glint"""
    def m(s):
        s.g(['.KKKKK.', '.KkKKK.', '.KkKKK.', '.KKKKK.', '.RRRRR.', 'KKKKKKK'], {'K': '#1a1a22', 'k': '#4a4a5a', 'R': '#c82a2a'}, 4, 4)
        s.px(11, 3, '#ffffff'); s.px(12, 4, '#ffffff')
    return _token(m)


def doodle_drawing():
    """Kettle's Dragon Drawing: a page of crayon on the slant - (3.0a) the Doodle Ender Dragon: a black crayon dragon with grey
    horns and bat wings, glowing purple eyes, a purple ender speck or two, signed with a scrawl"""
    s = S()
    for y in range(1, 15):
        for x in range(1, 15):
            s.px(x, y, PAPER[4] if x == 1 or y == 1 else PAPER[2] if x == 14 or y == 14 else PAPER[3])
    s.px(14, 1, None); s.px(13, 1, PAPER[1]); s.px(14, 2, PAPER[1]); s.px(13, 2, PAPER[2])     # a dog-ear
    K, k, Gy, E, e = '#1c1822', '#3a3544', '#a8a4b4', '#c040ff', '#ffb0ff'
    s.g(['.g.......g..',
         'gW.KKK...Wg.',
         'WWWKKKK.WWW.',
         'WWKKEKEKWWW.',
         'W.KKKKKK..W.',
         '...KkkK.....',
         '..KKkkKK.K..',
         '...K..K.KK..'], {'K': K, 'k': k, 'g': Gy, 'W': '#4a4556', 'E': E}, 2, 3)
    s.px(6, 4, Gy); s.px(9, 4, Gy)                                                     # his horns
    s.px(7, 6, e); s.px(9, 6, e)                                                       # the glow in his eyes
    s.px(4, 2, E); s.px(12, 3, E)                                                      # ender specks
    for x in (9, 10, 11, 12): s.px(x, 12 + (x % 2), '#3a6ae0')                        # KETTLE, scrawled
    return s.render()


def eraser_crumb():
    """the Eraser's Lucky Crumb: a chunk of pink eraser seen at an angle (its rubbed top lit, its sides in shade, a grey
    pencil smudge on it), two small crumbs beside it"""
    s = S()
    P = ['#9a3a5a', '#d0607e', '#f08aa2', '#ffb0c2', '#ffd8e2']
    top = ['....tttttt..', '...tttttttt.', '..tttttttt..', '.tttttttt...']
    for j, row in enumerate(top):
        for i, ch in enumerate(row):
            if ch == 't': s.px(2 + i, 3 + j, P[4] if j == 0 or i == 4 - j else P[3])
    for j in range(5):                                                                # the front face, the side face
        for i in range(8): s.px(3 + i, 7 + j, P[2] if i > 0 else P[3])
        for i in range(3): s.px(11 + i - (i == 2 and j > 3), 7 + j - i, P[1])
    for j in range(5):
        for k in range(3):
            x, y = 11 + k, 6 - k + j
            if y >= 3 + (3 - k) - 1: s.px(x, y, P[1])
    for x, y in ((6, 4), (7, 4), (8, 5), (9, 5)): s.px(x, y, '#b8a0aa')                 # a pencil smudge
    return strings(s.render(), [(13, 13, P[1]), (14, 13, P[1]), (2, 14, P[1])])


def cursor_mouse():
    """the Cursor's Mouse: an old beige computer mouse (two buttons, a wheel), its cable cut short and frayed - and the little
    white arrow pointer following it"""
    s = S()
    BEIGE = ['#7a7468', '#aaa496', '#d0cabc', '#ece6d8', '#fffaf0']
    s.disc(9.6, 10.4, 4.9, BEIGE, light=L, sq=1.12)
    for y in range(5, 10): s.px(10, y, BEIGE[1])                                      # the button split
    for x in range(5, 15):
        if (x, 9) in s.p: s.px(x, 9, BEIGE[1])
    s.px(10, 6, '#3a3a40'); s.px(10, 7, '#3a3a40')                                    # the wheel
    s.px(7, 6, BEIGE[4]); s.px(6, 7, BEIGE[4])
    s.g(['W....', 'WW...', 'WWW..', 'WWWW.', 'WWW..', 'W.W..'], {'W': '#ffffff'}, 1, 1)   # the pointer
    for x, y in ((2, 2), (2, 3), (3, 3)): s.px(x, y, '#e4e4f0')
    im = s.render()
    C = '#3a3a44'
    return strings(im, [(10, 4, C), (10, 3, C), (11, 2, C), (11, 1, '#c86a3a'), (12, 1, '#e0b030'), (12, 0, '#c86a3a')])


def ink_pot():
    """A Little Ink Pot: a squat glass inkwell full of black ink - and the Ink Blot rising out of it, two big white eyes"""
    s = S()
    s.disc(8.0, 11.4, 5.4, GLASS, light=L, sq=0.72)                                   # the glass well
    for y in range(16):
        for x in range(16):
            if (x, y) in s.p and math.hypot(x + 0.5 - 8, (y + 0.5 - 11.4) / 0.72) < 4.3: s.px(x, y, INK[2] if x < 7 else INK[1])
    s.px(4, 10, INK[4]); s.px(4, 11, INK[3])
    for x in range(5, 11): s.px(x, 7, GLASS[1]); s.px(x, 8, GLASS[2])                # its neck
    ball(s, 8.0, 4.6, 3.6, INK, sq=1.05)                                               # the blot
    s.px(4, 6, INK[2]); s.px(11, 6, INK[1]); s.px(10, 1, INK[2])
    s.g(['ww.ww', 'wk.wk', 'wk.wk'], {'w': '#ffffff', 'k': '#101018'}, 6, 3)                     # its eyes
    s.px(3, 9, '#ffffff'); s.px(3, 10, GLASS[3])
    return s.render()


def caption_card():
    """A Blank Caption Card: a white comic speech bubble with a pointed tail, a bold red '!' - shaded like a card, edge-lit"""
    s = S()
    for y in range(16):
        for x in range(16):
            dx, dy = (x + 0.5 - 8.0) / 7.0, (y + 0.5 - 6.5) / 5.6
            if dx * dx + dy * dy <= 1.0:
                s.px(x, y, WHITE[4] if dx + dy < -0.9 else WHITE[2] if dx + dy > 0.75 else WHITE[3])
    s.g(['WWW', 'WW.', 'W..', 'W..'], {'W': WHITE[2]}, 3, 11)                          # the tail
    s.px(3, 11, WHITE[3]); s.px(4, 11, WHITE[3])
    s.g(['RR', 'RR', 'RR', 'Rr', '..', 'RR'], {'R': '#e02a2a', 'r': '#a01a1a'}, 7, 2)  # the '!'
    s.px(7, 2, '#ff6a5a')
    return s.render()


def herald_feather():
    """the Herald's Feather: a long white feather on the diagonal - its quill, its vanes (barbed, a notch), its tip dipped
    in gold light - and a glint of that light"""
    s = S()
    VANE = ['#a6a2b8', '#cfcbe0', '#e8e6f4', '#f8f6ff', '#ffffff']
    GL = ['#b07a10', '#e0a820', '#ffd040', '#ffe880', '#fff8d0']
    # the vane: an elongated leaf along the diagonal (2,14) -> (13,2)
    ax, ay, bx, by = 3.0, 13.5, 13.4, 2.0
    L_ = math.hypot(bx - ax, by - ay); ux, uy = (bx - ax) / L_, (by - ay) / L_
    for y in range(16):
        for x in range(16):
            px_, py_ = x + 0.5 - ax, y + 0.5 - ay
            t = (px_ * ux + py_ * uy) / L_; d = px_ * -uy + py_ * ux                    # along, across (+: lower right)
            if not 0.18 < t < 1.0: continue
            w = 3.0 * math.sin(math.pi * min(1, (t - 0.18) / 0.82) ** 0.8)
            if abs(d) > w: continue
            if 0.46 < t < 0.52 and d > 0.5: continue                                  # a notch in the vane
            rp = GL if t > 0.80 else VANE
            k = 3 if d < -0.4 else 1 if d > 1.2 else 2
            if abs(d) < 0.5: k = 4
            s.px(x, y, rp[k])
    tube(s, [(1.6, 14.6), (5.0, 11.0)], 0.75, ['#8a7a5a', '#b8a882', '#ddd0b0', '#f2ead4', '#fffaf0'])   # the quill
    s.px(14, 1, '#ffffff'); s.px(15, 0, GL[3]); s.px(13, 0, GL[3])
    return s.render()


def dryad_cap():
    """A Glowing Mushroom: a blue cap with orange spots and a pale rim of gills, a cream stem - a soft glow beside it"""
    s = S()
    for y in range(16):
        for x in range(16):
            dx, dy = (x + 0.5 - 8.0) / 6.8, (y + 0.5 - 8.0) / 6.4
            if dy <= 0.12 and dx * dx + dy * dy <= 1.0:
                nx, ny = dx, dy; nz = math.sqrt(max(0, 1 - nx * nx - ny * ny))
                s.px(x, y, SHROOM[_lit(nx, ny, nz, 5)])
    for x in range(2, 15): s.px(x, 8, '#e8e0c8' if 4 < x < 12 else '#c8bc9c')          # the gills
    for x, y, c in ((5, 3, 1), (9, 2, 1), (11, 5, 0), (4, 6, 0), (8, 5, 1), (12, 7, 0)):   # its spots
        s.px(x, y, '#ffa040')
        if c: s.px(x + 1, y, '#ff8a20')
    tube(s, [(8.0, 9.0), (7.6, 14.6)], lambda t: 1.7 + 0.5 * t, ['#9a8a68', '#c8b890', '#e8dcbc', '#f6eed8', '#fffaf0'])   # the stem
    return strings(s.render(), [(1, 12, '#9ad0ff'), (14, 11, '#9ad0ff'), (13, 13, '#c8e8ff'), (2, 14, '#9ad0ff')])   # its glow


def _cart(col, face):
    """the 8-Bit Trio's cartridges: a grey cartridge (the grip ridges, the label recess), the follower's own colour on the
    label with their pixel face, the gold contacts at its foot"""
    def f():
        s = S()
        for y in range(1, 15):
            for x in range(2, 14):
                s.px(x, y, CART[4] if x == 2 or y == 1 else CART[1] if x == 13 or y == 14 else CART[3])
        for x in range(3, 13): s.px(x, 2, CART[2])                                    # the grip ridges
        s.px(13, 1, None); s.px(12, 1, CART[2]); s.px(13, 2, CART[1])
        lab = ramp(col)
        for y in range(4, 11):
            for x in range(4, 12):
                s.px(x, y, lab[4] if y == 4 else lab[3] if x == 4 else lab[1] if x == 11 or y == 10 else lab[2])
        for x in range(3, 13): s.px(x, 3, CART[1]); s.px(x, 11, CART[4])               # the recess
        for y in range(3, 12): s.px(3, y, CART[1]); s.px(12, y, CART[4])
        grid(s, face, {'k': '#1a1a22', 'w': '#ffffff'}, 5, 5)
        for x in range(4, 12, 2): s.px(x, 13, '#e8c050'); s.px(x + 1, 13, CART[2])     # the contacts
        return s.render()
    return f


cart_emma = _cart('#ff6ac8', ['......', '.k..k.', '.w..w.', '......', '.kkkk.'])
cart_leo = _cart('#4ab0ff', ['kkkkkk', 'k.kk.k', '......', '..kk..', '......'])
cart_cecil = _cart('#b070ff', ['......', '.k..k.', '......', 'kkkkkk', '.k..k.'])


def sky_mobile():
    """the Sky Mobile: a wooden crossbar on its hook, a puff of cloud sat on it, three threads - the sun in his shades, the
    grumpy star (lower, in the middle), the moon in her blue nightcap"""
    s = S()
    for x in range(1, 15): s.px(x, 2, WOOD[3] if x < 8 else WOOD[2])                  # the crossbar
    s.px(7, 1, WOOD[2]); s.px(8, 1, WOOD[1])
    CL = ['#8a8e9a', '#b8bcc6', '#dcdfe6', '#f2f4f8', '#ffffff']                        # the cloud on it
    s.g(['.cc.', 'cCcc'], {'c': CL[3], 'C': CL[4]}, 10, 0); s.px(12, 0, CL[4])
    ball(s, 2.9, 8.2, 2.7, SUNY)                                                      # the sun
    for x in range(1, 5): s.px(x, 7, '#1a1a22')                                       # in shades
    s.px(1, 8, '#1a1a22'); s.px(3, 8, '#1a1a22')
    S5 = ['#b07a10', '#e0a820', '#ffd040', '#ffe880', '#fff8d0']                       # the grumpy star
    s.g(['..Y..', '.YhY.', 'YYYYY', '.kYk.', '.YYY.', 'Y...Y'], {'Y': S5[2], 'h': S5[4], 'k': '#5a3a08'}, 6, 9)
    M = ['#9a9468', '#cac498', '#ece6bc', '#fbf7dc', '#ffffff']                         # the moon: a crescent
    ball(s, 13.0, 8.4, 2.7, M)
    for x in range(16):
        for y in range(16):
            if math.hypot(x + 0.5 - 14.6, y + 0.5 - 7.6) < 2.0 and (x, y) in s.p: s.px(x, y, None)
    s.g(['BB', 'Bb'], {'B': '#4a6ad8', 'b': '#ffffff'}, 11, 5)                        # her nightcap
    im = s.render()
    th = '#e8e8f2'
    return strings(im, [(3, 3, th), (3, 4, th), (8, 3, th), (8, 4, th), (8, 5, th), (8, 6, th), (8, 7, th), (12, 3, th)])


OVERRIDES = {f.__name__: f for f in (
    dw_horn, pi_cloche, om_monocle, chef_ladle, neighbor_baton, pq_pearls, bo_claw, st_hook, ln_gourd, bv_ball, bn_whistle, capshun_pencil,
    kettle_plane, henry_tag, nia_bell, creativity_gem, gentry_batty, gentry_eggbert, gentry_count, doodle_drawing,
    eraser_crumb, cursor_mouse, ink_pot, caption_card, herald_feather, dryad_cap, sky_mobile)}
OVERRIDES.update({'cart_emma': cart_emma, 'cart_leo': cart_leo, 'cart_cecil': cart_cecil})

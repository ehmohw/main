"""2.80a: the sprite repaint, part four - everyday things: papers, books and cards, the Lucky map, watches, food,
bottles, boxes and cases, bells and lanterns, records, and the pack's many small charms and trinkets.

    sprites280.post writes these too (OVERRIDES here, merged)."""
import math
import random
from sprites280 import S, GOLD, IRON, BRASS, BONE, RED, GREEN, PURPLE, TEAL, PINK, GLASS, STONE, BLACK, COPPER, WOOD, SACK, GHOST, CLAY
from sprites280b import ramp, emboss, coin, _gem_drop_small

PAPER = ['#8a6e48', '#b8986a', '#dcc496', '#f0e0bc', '#fff6e0']
LEATHER = ['#2e1a0e', '#4a2c18', '#6a4024', '#8a5834', '#aa7448']


# ================================================================== PAPERS, CARDS AND BOOKS
def _sheet(s, x0, y0, w, h, paper=PAPER, fold=True):
    """a sheet of paper: lit at the top-left, a darker bottom-right edge, a turned-down corner"""
    for y in range(h):
        for x in range(w):
            c = paper[3]
            if x == 0 or y == 0: c = paper[4]
            if x == w - 1 or y == h - 1: c = paper[2]
            s.px(x0 + x, y0 + y, c)
    if fold:
        s.px(x0 + w - 1, y0, None); s.px(x0 + w - 2, y0, paper[2]); s.px(x0 + w - 1, y0 + 1, paper[1]); s.px(x0 + w - 2, y0 + 1, paper[1])


def _lines(s, x0, y0, rows, col='#6a5a44'):
    for i, n in enumerate(rows):
        for x in range(n): s.px(x0 + x, y0 + i * 2, col)


def _scroll(s, x0, y0, w, h, paper=PAPER, rod=WOOD):
    """an unrolled scroll: a rolled bar across the top and the bottom"""
    _sheet(s, x0, y0 + 1, w, h - 2, paper, fold=False)
    for yy, top in ((y0, True), (y0 + h - 1, False)):
        for x in range(-1, w + 1):
            s.px(x0 + x, yy, paper[2] if top else paper[1])
        s.px(x0 - 1, yy, rod[2]); s.px(x0 + w, yy, rod[1])
    for x in range(w): s.px(x0 + x, y0 + 1, paper[2])


def _book(s, cover, x0=2, y0=1, w=11, h=14, label=None):
    """a book standing face-on: its cover lit at the top-left, the spine down its left, page edges down the right"""
    for y in range(h):
        for x in range(w):
            c = cover[2]
            if x <= 1: c = cover[1] if x == 0 else cover[3]
            elif y == 0: c = cover[3]
            elif y == h - 1 or x == w - 1: c = cover[1]
            s.px(x0 + x, y0 + y, c)
    for y in range(1, h - 1): s.px(x0 + w, y0 + y, PAPER[3] if y % 2 else PAPER[2])
    s.px(x0 + 2, y0 + 1, cover[4])
    if label:
        lc = label
        for y in range(3, 6):
            for x in range(4, w - 2): s.px(x0 + x, y0 + y, lc[2] if y == 4 else lc[3])


def _card(s, body, x0=1, y0=3, w=14, h=10):
    for y in range(h):
        for x in range(w):
            if (x in (0, w - 1)) and (y in (0, h - 1)): continue
            c = body[2]
            if y == 0 or x == 0: c = body[3]
            if y == h - 1 or x == w - 1: c = body[1]
            s.px(x0 + x, y0 + y, c)
    s.px(x0 + 1, y0 + 1, body[4])


def bankers_card():
    s = S()
    _card(s, GOLD)
    s.g(['CCC', 'ChC', 'CCC'], {'C': '#c8c0a0', 'h': '#fff6e0'}, 3, 5)
    _lines(s, 3, 9, [9], GOLD[0]); _lines(s, 3, 11, [5], GOLD[1])
    s.g(['.RR', 'RR.'], {'R': '#3a2a10'}, 11, 5)
    return s.render()


def fixers_card():
    s = S()
    _card(s, ['#0a0a0e', '#16161c', '#24242c', '#34343e', '#4a4a56'])
    for x in range(2, 14): s.px(x, 3, GOLD[3]); s.px(x, 12, GOLD[1])
    for y in range(4, 12): s.px(1, y, GOLD[2]); s.px(14, y, GOLD[1])
    s.g(['YY', 'Yy'], {'Y': GOLD[3], 'y': GOLD[1]}, 3, 5)
    _lines(s, 6, 5, [6, 5, 4], '#d8d0c0')
    s.g(['RR', 'Rr'], {'R': '#d02a2a', 'r': '#8a1010'}, 11, 9)
    return s.render()


def pearl_card():
    """Pearlman's business card: white, a teal border, his little penguin face and his name in lines"""
    s = S()
    _card(s, ['#a8b4bc', '#d0dae0', '#f0f4f6', '#ffffff', '#ffffff'])
    for x in range(2, 14): s.px(x, 4, TEAL[2])
    s.g(['.KK.', 'KWWK', 'KeWe', '.Ko.'], {'K': '#14181e', 'W': '#ffffff', 'e': '#14181e', 'o': '#ffb020'}, 2, 6)
    _lines(s, 7, 7, [6, 4], '#3a4a58')
    s.px(12, 11, GOLD[3])
    return s.render()


def scratch_card():
    s = S()
    _card(s, ['#2a1a4a', '#3e2a6a', '#5a3e90', '#7a5ab8', '#a080e0'], y0=2, h=12)
    for x in range(2, 14): s.px(x, 3, GOLD[3])
    for y in range(5, 12):
        for x in range(3, 13): s.px(x, y, IRON[3] if (x + y) % 3 else IRON[2])
    s.g(['RRRR', '...R', '..R.', '.R..', '.R..'], {'R': '#e02a2a'}, 4, 6)
    s.g(['WW', 'WW'], {'W': '#ffffff'}, 10, 6); s.g(['ww', 'ww'], {'w': '#d8d8e0'}, 10, 9)
    return s.render()


def merc_contract():
    s = S()
    _sheet(s, 2, 1, 12, 14)
    _lines(s, 4, 4, [7, 8, 6, 8, 4])
    s.disc(11.5, 12.5, 2.2, ['#6a0a0a', '#a01414', '#d02a2a', '#ff6a5a'])
    s.px(13, 15, '#a01414'); s.px(10, 15, '#a01414')
    return s.render()


def blood_bounty():
    s = S()
    _sheet(s, 2, 1, 12, 14)
    s.g(['.RRR.', 'RR.RR', 'R...R', 'RR.RR', '.RRR.'], {'R': '#a01414'}, 5, 3)            # a target
    s.px(7, 5, '#e02a2a')
    _lines(s, 4, 10, [8, 6], '#6a5a44')
    s.g(['rr', 'rR'], {'r': '#d02a2a', 'R': '#6a0a0a'}, 11, 12)
    return s.render()


def tip_bloodmoon():
    s = S()
    _sheet(s, 2, 2, 12, 12, fold=True)
    _lines(s, 4, 5, [5, 7, 4], '#5a4a3a')
    for (x, y) in ((10, 5), (11, 6), (10, 7), (12, 5)): s.px(x, y, '#c41a1a')                # a smudge, in something red
    s.g(['R.R', '.R.', 'R.R'], {'R': '#c41a1a'}, 9, 9)
    return s.render()


def brass_wing_scroll():
    s = S()
    _scroll(s, 3, 1, 10, 14)
    s.g(['B......B', 'BB....BB', 'BbB..BbB', '.BbBBbB.', '..BBBB..'], {'B': BRASS[3], 'b': BRASS[1]}, 4, 5)
    _lines(s, 5, 12, [6], '#6a5a44')
    return s.render()


def market_crest_scroll():
    s = S()
    _scroll(s, 3, 1, 10, 14)
    s.disc(8, 7.5, 3.2, GOLD)
    s.disc(8, 7.5, 2.0, BLACK[:4])
    emboss(s, ['Y.Y', '.Y.'], {'Y': GOLD[3]}, 7, 6)
    _lines(s, 5, 12, [6], '#6a5a44')
    return s.render()


def crimson_ledger():
    s = S()
    _book(s, ['#4a0a0e', '#7a1418', '#b02028', '#e04a4a', '#ff8a8a'], label=GOLD)
    _lines(s, 5, 10, [5], GOLD[2])
    return s.render()


def fixers_ledger():
    """the Fixer's Ledger: a brown leather book, gold corners, a gold lock on its strap"""
    s = S()
    _book(s, LEATHER)
    for (x, y) in ((4, 2), (11, 2), (4, 13), (11, 13)): s.px(x, y, GOLD[3])
    s.g(['SSSSSSSSS'], {'S': LEATHER[0]}, 3, 8)
    s.g(['.YY.', 'Y..Y', 'YYYY', 'YkYY', 'YYYY'], {'Y': GOLD[3], 'k': '#2a1804'}, 6, 6)
    s.px(6, 8, GOLD[4])
    return s.render()


def smugglers_ledger():
    s = S()
    _book(s, ['#1e1a14', '#3a3224', '#564a36', '#76664a', '#968462'])
    _lines(s, 5, 4, [6, 4], GOLD[2])
    s.g(['.W.', 'WkW', '.W.'], {'W': '#d8d0c0', 'k': '#1e1a14'}, 6, 8)                        # a skull mark, small
    return s.render()


def _map_whole():
    """the Lucky treasure map, 42 x 42: parchment, a coast, trees, mountains, the golden pyramid, the path, the X"""
    W = 42
    im = {}
    rnd = random.Random(7)
    for y in range(W):
        for x in range(W):
            n = rnd.random()
            im[(x, y)] = PAPER[3] if n > 0.10 else PAPER[2]
    for y in range(W):                                       # the sea down the right
        for x in range(W):
            if x > 32 + 3 * math.sin(y / 5):
                im[(x, y)] = '#6aa8c8' if (x + y) % 5 else '#8ac8e0'
            elif x > 30 + 3 * math.sin(y / 5): im[(x, y)] = PAPER[1]
    for (cx, cy) in ((6, 8), (10, 6), (8, 12), (13, 10), (5, 15)):                              # a wood
        for dx, dy, c in ((0, 0, '#3a7a2a'), (1, 0, '#2a5a1e'), (0, -1, '#5aa83a'), (0, 1, '#5a3a1a')):
            im[(cx + dx, cy + dy)] = c
    for (cx, cy) in ((22, 6), (26, 8), (18, 9)):                                                 # mountains
        for i in range(4):
            for j in range(-i, i + 1): im[(cx + j, cy - 3 + i)] = '#8a7a6a' if j < 0 else '#6a5a4a'
        im[(cx, cy - 3)] = '#ffffff'
    for i in range(6):                                                                         # the golden pyramid
        for j in range(-i, i + 1): im[(24 + j, 18 + i)] = GOLD[3] if j < 0 else GOLD[1]
    path = [(5, 36), (7, 34), (9, 33), (11, 31), (13, 30), (15, 28), (17, 27), (19, 26), (21, 25), (24, 25), (27, 27), (29, 29), (30, 31)]
    for (x, y) in path: im[(x, y)] = '#a02a1a'
    for k in range(-2, 3): im[(30 + k, 34 + k)] = '#c41a1a'; im[(30 + k, 34 - k)] = '#c41a1a'   # X
    for (x, y), c in (((3, 3), '#5a3a1a'), ((3, 2), '#5a3a1a'), ((3, 1), '#5a3a1a'), ((2, 2), '#5a3a1a'), ((4, 2), '#5a3a1a'), ((3, 4), '#a02a1a')):
        im[(x, y)] = c                                                                          # the compass's needle
    return im


def lucky_fragment(k):
    def f():
        whole = _map_whole()
        tx, ty = (k - 1) % 3, (k - 1) // 3
        s = S()
        rnd = random.Random(k * 31)
        for y in range(14):
            for x in range(14):
                s.px(1 + x, 1 + y, whole[(tx * 14 + x, ty * 14 + y)])
        for i in range(14):                                  # torn edges, a nibble here and there
            for (x, y) in ((1 + i, 1), (1 + i, 14), (1, 1 + i), (14, 1 + i)):
                if rnd.random() < 0.3: s.px(x, y, None)
                elif (x, y) in s.p: s.px(x, y, PAPER[1])
        return s.render()
    return f


# ================================================================== WATCHES, HOURGLASSES, THE PADDLE
def _watch(s, case=GOLD, face=('#c8c0a8', '#e8e2d0', '#fffaf0'), cy=9.0):
    s.g(['.YY.', 'Y..Y', '.YY.'], {'Y': case[2]}, 6, 0)
    s.g(['YY'], {'Y': case[3]}, 7, 3)
    s.disc(7.5, cy, 6.0, case)
    s.disc(7.5, cy, 4.6, list(face), light=(0.6, 0.8))


def pocket_watch():
    s = S()
    _watch(s)
    s.line(7, 9, 7, 6, '#2a2018'); s.line(7, 9, 10, 9, '#2a2018')
    for (x, y) in ((7, 5), (11, 9), (7, 13), (3, 9)): s.px(x, y, '#8a7a5a')
    return s.render()


def stolen_watch():
    s = S()
    _watch(s, case=IRON)
    s.line(7, 9, 9, 6, '#2a2018'); s.line(7, 9, 5, 10, '#2a2018')
    s.g(['C', 'C', 'C', 'C'], {'C': IRON[2]}, 13, 9)                                            # a dangling broken chain
    s.px(14, 12, IRON[1]); s.px(13, 14, IRON[2])
    return s.render()


def the_alibi():
    """the Alibi: a gold watch whose hands run backwards - a blue arrow curling round its face"""
    s = S()
    _watch(s)
    s.line(7, 9, 7, 6, '#2a2018'); s.line(7, 9, 5, 11, '#2a2018')
    for (x, y) in ((4, 6), (5, 5), (6, 5), (9, 5), (10, 6)): s.px(x, y, '#3a8aff')
    s.px(3, 7, '#3a8aff'); s.px(4, 8, '#3a8aff'); s.px(2, 7, '#3a8aff')
    return s.render()


def _hourglass(s, frame, sand, glass=('#9ac8d8', '#c8eaf4', '#eefcff')):
    s.g(['FFFFFFFFF', '.FffffffF.'[:9]], {'F': frame[3], 'f': frame[1]}, 3, 1)
    for y, w in enumerate([3, 3, 2, 1, 0, 0, 1, 2, 3, 3]):
        for x in range(4 - w, 5 + w):
            s.px(3 + x, 3 + y, glass[1] if x < 4 else glass[0])
        s.px(3 + 4 - w - 1, 3 + y, frame[2]); s.px(3 + 4 + w + 1, 3 + y, frame[1])
    for y in range(7, 13):
        for x in range(3, 13):
            if (x, y) in s.p and s.p[(x, y)][:3] in ((0x9a, 0xc8, 0xd8), (0xc8, 0xea, 0xf4)) and y >= 10:
                s.px(x, y, sand[3] if x < 8 else sand[2])
    for y in (4, 5): s.px(7, y, sand[3]); s.px(8, y, sand[2])
    s.px(7, 7, sand[3]); s.px(7, 8, sand[3])
    s.g(['FFFFFFFFF', 'fffffffff'], {'F': frame[3], 'f': frame[1]}, 3, 13)


def thiefs_hourglass():
    s = S()
    _hourglass(s, WOOD, ramp('#e8c070'))
    return s.render()


def crimson_hourglass():
    s = S()
    _hourglass(s, ['#2a0608', '#4a0a0e', '#7a1418', '#a02028', '#c83a3a'], ramp('#d02020'))
    return s.render()


def bidding_paddle():
    s = S()
    _haft(s, WOOD, 7, 15, 8, 11)
    s.disc(8, 6, 5.2, ['#6a4a2a', '#9a6a3a', '#c89a5a', '#e8c08a', '#fff0d0'])
    s.disc(8, 6, 4.0, ['#d0c8b8', '#f0ece0', '#ffffff'])
    s.g(['RRR.', 'R..R', 'RRR.', 'R...', 'R...'], {'R': '#c0392b'}, 6, 4)
    return s.render()


def _haft(s, col, x0, y0, x1, y1):
    n = max(abs(x1 - x0), abs(y1 - y0))
    for i in range(n + 1):
        x = round(x0 + (x1 - x0) * i / n); y = round(y0 + (y1 - y0) * i / n)
        s.px(x, y, col[3]); s.px(x + 1, y, col[1])


# ================================================================== FOOD
def dish_potpie():
    s = S()
    s.g(['...CCCCCCCCC...',
         '..CcCCCCCCcCC..',
         '.CCCCcCCCCCCCC.',
         '.CcCCCCCcCCCcC.',
         'TTTTTTTTTTTTTTT',
         '.ttttttttttttt.',
         '..ddddddddddd..'], {'C': '#e8b060', 'c': '#a86a2a', 'T': IRON[3], 't': IRON[2], 'd': IRON[1]}, 0, 5)
    s.g(['.L.', 'LGL'], {'L': '#fff0c0', 'G': '#3ab84a'}, 6, 5)                                  # a clover cut in the crust
    s.px(4, 6, '#fff0c0')
    return s.render()


def dish_roast():
    s = S()
    s.g(['....RRRRR....',
         '..RRrRRRRRR..',
         '.RrRRRRRRRRRB',
         'RRRRRRRRRRRRB',
         '.RRRRRRRRRRD.',
         '..DDDDDDDDD..'], {'R': '#a85a28', 'r': '#e8a060', 'B': '#fff0e0', 'D': '#6a3010'}, 2, 4)
    s.g(['.PPPPPPPPPPPPP.', 'PpppppppppppppP', '.PPPPPPPPPPPPP.'], {'P': '#e8e8f0', 'p': '#c8c8d4'}, 0, 10)
    s.px(14, 5, '#ffffff'); s.px(15, 6, '#e8e0d0')
    return s.render()


def dish_drumsticks():
    s = S()
    m = ['#6a3010', '#a85a20', '#d8883a', '#f0b060', '#ffd890']
    for (x0, y0) in ((0, 1), (7, 5)):
        s.g(['.MMM....',
             'MhLMM...',
             'MLLMMD..',
             'MLMMMD..',
             '.MMMD...',
             '..DDBB..',
             '.....BB.',
             '....BWBW',
             '.....WW.'], {'M': m[2], 'h': m[4], 'L': m[3], 'D': m[1], 'B': '#e8dcc8', 'W': '#ffffff'}, x0, y0)
    return s.render()


def coffee():
    s = S()
    s.g(['.WWWWWWWW..',
         'WcccccccWW.',
         'WCCCCCCCW.W',
         'WWWWWWWWW.W',
         'WWWWWWWWWWW',
         'WwWWWWWWw..',
         '.wwwwwwww..'], {'W': '#f4f0ea', 'w': '#c8c0b8', 'C': '#4a2a14', 'c': '#7a4a24'}, 2, 6)
    s.g(['SSSSSSSSSSSS'], {'S': '#c8a070'}, 1, 13)
    for (x, y) in ((5, 4), (6, 3), (5, 2), (8, 4), (9, 3), (8, 2)): s.px(x, y, '#d8d4d0')
    return s.render()


def golden_cheese_wheel():
    """a golden cheese wheel face-on, a wedge cut from it, holes in the cheese"""
    s = S()
    rind = ['#7a4a08', '#a86a10', '#d8961a', '#f0b830', '#ffd860']
    s.disc(8, 8, 7.0, rind)
    s.disc(8, 8, 5.6, ['#e8c040', '#ffdc5a', '#ffec90', '#fff6c8'])
    for y in range(16):                                      # the wedge cut away, its sides in shadow
        for x in range(16):
            dx, dy = x + 0.5 - 8, y + 0.5 - 8
            a = math.atan2(dy, dx)
            if -0.55 < a < 0.25 and math.hypot(dx, dy) > 0.6:
                s.px(x, y, None)
            elif -0.75 < a <= -0.55 and math.hypot(dx, dy) < 7: s.px(x, y, '#c89a2a')
            elif 0.25 <= a < 0.45 and math.hypot(dx, dy) < 7: s.px(x, y, '#a87a1a')
    for (x, y) in ((5, 5), (4, 10), (8, 12), (7, 8), (10, 11)): s.px(x, y, '#c8962a')
    s.px(5, 4, '#a8761a'); s.px(4, 3, '#ffffff')
    return s.render()


# ================================================================== BOTTLES, BUCKETS AND JARS
def bucket(liquid):
    def f():
        s = S()
        lq = ramp(liquid)
        s.g(['.HHHHHHHHHH.', 'H..........H', 'H..........H'], {'H': IRON[2]}, 2, 1)
        s.g(['IIIIIIIIIIII',
             'ILLLLLLLLLLI',
             'iLLlLLLLLLLi',
             '.IIIIIIIIII.',
             '.IiIIIIIIiI.',
             '.IIIIIIIIII.',
             '..IIIIIIII..',
             '..iiiiiiii..'], {'I': IRON[3], 'i': IRON[1], 'L': lq[2], 'l': lq[4]}, 2, 4)
        for y in range(7, 12): s.px(3, y, IRON[4])
        s.g(['.Y.', 'YWY', '.Y.'], {'Y': GOLD[3], 'W': '#fff6c0'}, 7, 12)                    # bottomless: a gold spark
        return s.render()
    return f


def smelling_salts():
    s = S()
    s.g(['.KKKK.', '.kkkk.'], {'K': '#3a2a20', 'k': '#2a1a10'}, 5, 1)
    s.g(['GGGGGGGG', 'GwwwwwwG', 'GwWwwwwG', 'GwwwwwwG', 'GwwccwwG', 'GwcccwwG', 'GccccccG', 'GccccccG', 'GGGGGGGG'],
        {'G': GLASS[1], 'w': GLASS[2], 'W': '#ffffff', 'c': '#f4f8ff'}, 4, 4)
    s.px(5, 6, '#ffffff'); s.px(9, 10, '#d8e8f8')
    s.g(['LLLL'], {'L': '#e8dcc0'}, 6, 7)
    return s.render()


def smoke_bomb():
    s = S()
    s.disc(8, 10, 5.0, ['#3a3a44', '#5a5a66', '#8a8a96', '#b8b8c4', '#e0e0e8'])
    s.g(['.II.', 'IIII'], {'I': IRON[1]}, 6, 4)
    s.g(['.f', 'f.', '.f'], {'f': '#8a6a3a'}, 9, 1)
    s.px(11, 0, '#ffb03a'); s.px(12, 1, '#ff6a1a')
    s.px(6, 8, '#ffffff')
    return s.render()


def smuggler_jar_full():
    """the Smuggler's Jar, filled: the clay jar, its stopper out, gold coins at the mouth and a glint"""
    s = S()
    s.g(['....YYYYY....',
         '...YyYYYYY...',
         '....rRRRr....',
         '...KKKKKKK...',
         '..JjJJJJJjJ..',
         '.JjJJJJJJJjJ.',
         '.JJJJJJJJJJj.',
         '.JJJLLLLLJJj.',
         '.JJJLKKKLJJj.',
         '.JJJLKGKLJJj.',
         '.JjJLLLLLJjj.',
         '..jJJJJJJJj..',
         '...jjjjjjj...'], {'Y': GOLD[3], 'y': GOLD[4], 'r': '#c8b090', 'R': '#e8d4b0', 'K': '#2a1a10', 'J': CLAY[3], 'j': CLAY[1],
                            'L': '#e8dcc0', 'G': GOLD[3]}, 1, 2)
    s.px(3, 7, CLAY[4]); s.px(3, 8, CLAY[4]); s.px(10, 0, '#ffffff'); s.px(11, 1, '#fff6c0')
    return s.render()


# ================================================================== BOXES, SACKS, CASES, HOPPERS
def lootbox(body, band, emblem, epal):
    """a raid crate: a banded box with a lid, a plate on its front with what's inside"""
    def f():
        s = S()
        b = ramp(body) if isinstance(body, str) else body
        n = ramp(band) if isinstance(band, str) else band
        for y in range(2, 15):
            for x in range(1, 15):
                c = b[2] if (y - 2) % 4 else b[1]
                if x <= 2 or y == 2: c = b[3]
                if x >= 13 or y == 14: c = b[1]
                s.px(x, y, c)
        for x in range(1, 15): s.px(x, 5, n[2]); s.px(x, 6, n[1])                       # the lid's band
        for y in range(2, 15): s.px(3, y, n[3]); s.px(12, y, n[1])
        s.g(['PPPPPP', 'P....P', 'P....P', 'P....P', 'PPPPPP'], {'P': n[3]}, 5, 8)
        emboss(s, emblem, epal, 6, 9)
        s.px(1, 2, b[4])
        return s.render()
    return f


def display_case(base):
    def f():
        s = S()
        b = ramp(base) if isinstance(base, str) else base
        gl = ['#6a9ab0', '#a8d8ec', '#d0f0fa', '#ffffff']
        for y in range(2, 12):
            for x in range(2, 14):
                if x in (2, 13) or y == 2: s.px(x, y, b[3] if x == 2 or y == 2 else b[1])
                else: s.px(x, y, (200, 236, 248, 255) if (x + y) % 7 else (230, 250, 255, 255))
        s.line(4, 9, 7, 4, gl[3]); s.line(5, 9, 8, 4, gl[2])                                     # the glass's glint
        s.g(['.EE.', 'EeEE', '.EE.', 'RRRR'], {'E': '#3ad87a', 'e': '#c8ffd8', 'R': '#c41a3a'}, 7, 7)
        s.g(['BBBBBBBBBBBBBB', 'bbbbbbbbbbbbbb', '.dddddddddddd.'], {'B': b[3], 'b': b[2], 'd': b[1]}, 1, 11)
        return s.render()
    return f


def hoard_sack():
    s = S()
    sk = ['#4a3418', '#6e5028', '#93703a', '#b89050', '#d8b070']
    s.g(['.....YYY.....', '....YyYYY....', '.....sss.....', '....SSSSS....', '...SsSSSSS...', '..SsSSSSSSSs.', '.SsSSSSSSSSSs',
         '.SSSSSSSSSSSs', '.SSSSSSSSSSss', '..SSSSSSSSss.', '...ssssssss..'], {'S': sk[2], 's': sk[1], 'Y': GOLD[3], 'y': GOLD[4]}, 1, 2)
    s.disc(7.5, 10, 2.0, GOLD)
    s.px(4, 7, sk[4])
    return s.render()


def ender_pouch():
    s = S()
    p = ['#062a24', '#0e463c', '#16645a', '#248a7c', '#3ab0a0']
    s.g(['...ss.ss...', '....SSS....', '..SSSSSSS..', '.SsSSSSSSS.', 'SsSSSSSSSSs', 'SSSSSSSSSSs', 'SSSSSSSSSSs', 'SSSSSSSSSss',
         '.SSSSSSSSs.', '..sssssss..'], {'S': p[2], 's': p[1]}, 2, 3)
    s.disc(7.5, 9.5, 2.3, ['#0a3a30', '#1a8a6a', '#5ae0b0', '#c8fff0'])
    s.px(7, 9, '#000000'); s.px(8, 9, '#000000')
    return s.render()


def vacuum_satchel(on=False):
    def f():
        s = S()
        b = ramp('#c8a050')
        s.g(['...IIIIIIII...', '..I........I..'], {'I': IRON[2]}, 1, 1)
        s.g(['BBBBBBBBBBBB',
             'BhBBBBBBBBBD',
             'BBBBBBBBBBBD',
             'DDDDDDDDDDDD',
             'BBBBBBBBBBBD',
             'BhBBBBBBBBBD',
             'BBBBBBBBBBBD',
             'BBBBBBBBBBBD',
             'BBBBBBBBBBDD',
             '.DDDDDDDDDD.'], {'B': b[2], 'h': b[4], 'D': b[1]}, 2, 4)
        s.disc(8, 10, 2.0, ['#ffe85a', '#fff6b0', '#ffffff'] if on else IRON[:4])
        s.px(8, 10, '#ffffff' if on else IRON[0])
        if on:
            for (x, y) in ((2, 2), (13, 2), (14, 9), (1, 12)): s.px(x, y, '#ffe85a')
        return s.render()
    return f


def caged_spawner():
    s = S()
    for y in range(2, 14):
        for x in range(2, 14):
            if x in (2, 13) or y in (2, 13) or x in (5, 10) or y in (5, 10):
                s.px(x, y, '#3a3e48' if (x in (2,) or y in (2,)) else '#24262e')
    s.disc(8, 8, 2.4, ['#a02a0a', '#e8641a', '#ffb03a', '#fff0a0'])
    for (x, y) in ((2, 2), (13, 2), (2, 13), (13, 13)): s.px(x, y, IRON[3])
    return s.render()


def fy_bowl():
    """Fishy's bowl: a round fishbowl, water, the little orange fish in his top hat, a bubble"""
    s = S()
    s.disc(8, 9, 6.0, ['#6a9ab0', '#a8d8ec', '#d0f0fa', '#ffffff'])
    s.disc(8, 10, 4.8, ['#1e6a9a', '#2a8ac0', '#4ab0e0', '#8ad8f8'])
    for x in range(3, 14): s.px(x, 4, '#a8d8ec')
    s.g(['.OO.O', 'OOwOO', '.OO.O'], {'O': '#ff8a2a', 'w': '#ffffff'}, 6, 10)
    s.px(7, 11, '#1a1a1a')
    s.g(['.KK.', '.KK.', 'KKKK'], {'K': '#1a1a22'}, 6, 7)
    s.px(7, 8, '#c41a3a'); s.px(8, 8, '#c41a3a')
    s.px(11, 7, '#e8fbff'); s.px(12, 5, '#ffffff')
    s.g(['GGGGGGGG'], {'G': '#3a8a3a'}, 4, 14)
    return s.render()


# ================================================================== BELLS, LANTERNS, RECORDS
def bell(metal, clapper=None, extra=None):
    def f():
        s = S()
        m = ramp(metal) if isinstance(metal, str) else metal
        s.g(['.HH.', 'H..H'], {'H': IRON[2]}, 6, 0)
        s.g(['.....LLM.....',
             '....LhLMM....',
             '...LhLLLMD...',
             '...LhLLLMD...',
             '..LhLLLLLMD..',
             '..LLLLLLLMD..',
             '.LhLLLLLLLMD.',
             'LLLLLLLLLLMMD',
             'MMMMMMMMMMMMD',
             '.DDDDDDDDDDD.'], {'L': m[3], 'h': m[4], 'M': m[2], 'D': m[1]}, 1, 2)
        s.g(['CC', 'cc'], {'C': clapper or m[1], 'c': clapper or m[0]}, 7, 12)
        if extra: extra(s)
        return s.render()
    return f


def _fw_extra(s):
    s.g(['.B.', 'BWB', '.B.'], {'B': '#5ac8ff', 'W': '#e8fbff'}, 7, 13)


def _pearl_extra(s):
    for x in range(2, 14): s.px(x, 10, TEAL[3])


def _echo_extra(s):
    for (x, y) in ((0, 6), (0, 8), (15, 6), (15, 8)): s.px(x, y, '#a8f0ff')
    s.px(0, 7, '#5ac8ff'); s.px(15, 7, '#5ac8ff')


# ================================================================== CHARMS, LOCKETS AND TRINKETS
def _pendant_loop(s, col=IRON, x0=7, y0=0):
    s.g(['.CC.', 'C..C', '.CC.'], {'C': col[2]}, x0 - 1, y0)


def lava_charm():
    s = S()
    l = ['#5a1404', '#a8300a', '#e8641a', '#ffa83a', '#fff0a0']
    s.g(['.....L....', '....LLM...', '...LhLMM..', '..LhLLLMD.', '.LhLLLLMMD', '.LhLWLLLMD', 'LLhLLLLMMD', 'LLLLLLLMDD', '.LLLLLMMD.', '..LLLMDD..', '...DDDD...'],
        {'L': l[2], 'h': l[3], 'W': l[4], 'M': l[1], 'D': l[0]}, 3, 3)
    return s.render()


def lava_wader_charm():
    s = S()
    _pendant_loop(s, IRON, 7, 0)
    s.disc(8, 10, 4.6, ['#2a0a04', '#5a1a08', '#8a2a0a', '#b84a1a'])
    s.g(['.LL.', 'LWWL', 'LWWL', '.LL.'], {'L': '#ff8a2a', 'W': '#ffe08a'}, 6, 8)
    for (x, y) in ((4, 3), (11, 4), (5, 5)): s.px(x, y, '#9a9aa6')
    return s.render()


def surface_charm():
    """a pebble that remembers the sky: a green stone, a gold arrow rising out of it"""
    s = S()
    s.g(['..Y..', '.YYY.', 'YYYYY', '..Y..', '..Y..'], {'Y': GOLD[3]}, 6, 0)
    s.disc(8, 10.5, 4.6, ramp('#8fd16a'))
    s.px(6, 9, '#e8ffd0')
    return s.render()


def water_charm():
    s = S()
    w = ramp('#3a8aff')
    s.g(['...L...', '..LhM..', '.LhLMD.', 'LhLLLMD', 'LhLWLMD', 'LLLLLMD', '.LLLMD.', '..DDD..'], {'L': w[3], 'h': w[4], 'W': '#ffffff', 'M': w[2], 'D': w[1]}, 4, 2)
    s.g(['CC', 'cc'], {'C': COPPER[3], 'c': COPPER[1]}, 7, 10)
    s.px(6, 12, COPPER[2]); s.px(9, 12, COPPER[2])
    return s.render()


def specter_charm():
    s = S()
    _pendant_loop(s, IRON, 8, 0)
    s.g(['..GGGG..', '.GgGGGGG.'[:8], 'GgGGGGGG', 'GGKGGKGG', 'GGGGGGGG', 'GGGKKGGG', 'GGGGGGGG', 'GG.GG.GG', 'G...G..G'],
        {'G': GHOST[2], 'g': GHOST[4], 'K': '#1a3a3a'}, 4, 4)
    return s.render()


def showstopper_charm():
    s = S()
    st = ramp('#ffd23f')
    s.g(['....L....', '...LhM...', 'LLLLhMMMD', '.LLhhMMD.', '..LhMMD..', '.LLM.MMD.', '.LD...MD.'], {'L': st[3], 'h': st[4], 'M': st[2], 'D': st[1]}, 3, 4)
    for (x, y, c) in ((1, 2, '#ff3a6a'), (13, 1, '#3a8aff'), (14, 8, '#b45aff'), (1, 12, '#3aff8a'), (12, 13, '#ff8a2a'), (6, 1, '#ffffff')):
        s.px(x, y, c)
    return s.render()


def fizzle_stone():
    s = S()
    s.disc(8, 8, 5.8, ['#3a4a3a', '#566a56', '#7a907a', '#9ab49a', '#c0d8c0'])
    for (x, y) in ((6, 6), (10, 7), (7, 10), (11, 11), (5, 9)): s.px(x, y, '#2a3a2a')
    s.px(5, 4, '#e0f0e0')
    for (x, y) in ((13, 2), (14, 3), (12, 1)): s.px(x, y, '#c8c8c8')
    return s.render()


def gale_locket():
    s = S()
    _pendant_loop(s, IRON, 8, 0)
    s.disc(8, 9, 5.0, IRON)
    s.disc(8, 9, 3.6, ['#7ab0c8', '#a8d4e8', '#d8f0fa'], light=(0.6, 0.8))
    s.g(['WWW.', '...W', 'WW.W', '..W.'], {'W': '#ffffff'}, 6, 7)
    for (x, y) in ((1, 14), (3, 14), (12, 14), (14, 14)): s.px(x, y, '#e8f4ff')
    return s.render()


def lodestone_locket():
    s = S()
    _pendant_loop(s, PURPLE, 8, 0)
    s.disc(8, 9, 5.6, PURPLE)
    s.disc(8, 9, 4.0, ['#0a0810', '#16121e', '#24202e', '#363044'])
    s.px(6, 7, '#b48cff'); s.px(10, 11, '#7a4ab8')
    return s.render()


def wilfrey_locket():
    """Wilfrey's locket: silver on a fine chain, a white enamel heart inside a gold rim"""
    s = S()
    for i, (x, y) in enumerate([(4, 0), (4, 1), (5, 2), (6, 3), (11, 0), (11, 1), (10, 2), (9, 3)]):
        s.px(x, y, IRON[3] if i % 2 else IRON[2])
    s.disc(8, 9.5, 5.6, IRON)
    s.disc(8, 9.5, 4.2, ['#c8ccd2', '#e8ecf0', '#ffffff'])
    s.g(['.GG.GG.', 'GggGggG', 'GgggggG', '.GgggG.', '..GgG..', '...G...'], {'G': GOLD[3], 'g': '#ffffff'}, 5, 7)
    s.px(7, 8, GOLD[2]); s.px(8, 9, '#f4f0ea')
    return s.render()


def wayfarers_lodestar():
    """a star in a brass cage that always points home"""
    s = S()
    s.g(['....BB....', '...B..B...'], {'B': BRASS[2]}, 3, 0)
    for y in range(2, 15):
        w = min(y - 1, 15 - y, 5)
        s.px(8 - w, y, BRASS[3]); s.px(8 + w - 1, y, BRASS[1])
    s.line(8, 2, 8, 14, BRASS[2])
    st = ['#c8a020', '#ffd84a', '#fff0a0', '#ffffff']
    s.g(['..W..', '.WWW.', 'WWsWW', '.WWW.', '..W..'], {'W': st[2], 's': '#ffffff'}, 5, 6)
    s.px(5, 8, st[1]); s.px(9, 8, st[1])
    return s.render()


def horseshoe():
    s = S()
    g = GOLD
    s.g(['..LLLLLLLL..', '.LhLLLLLLMM.', 'LhLM....LLMD', 'LLD......LMD', 'LLD......LMD', 'LLD......LMD', 'LhD......LMD', 'LLD......LMD',
         'LLD......LMD', 'LLD......LMD', 'MMD......MMD', 'DDD......DDD'], {'L': g[3], 'h': g[4], 'M': g[2], 'D': g[1]}, 2, 2)
    for (x, y) in ((2, 6), (2, 10), (13, 6), (13, 10), (5, 3), (10, 3)): s.px(x, y, g[0])
    return s.render()


def kraken_conch():
    """the Kraken's conch: a spiral shell, its spire up and right, ridged, its pink mouth open at the lower left"""
    s = S()
    c = ['#7a4434', '#a86a54', '#d49a80', '#f0c4ac', '#ffe6d6']
    s.g(['..........hL..',
         '.........hLLM.',
         '........LLDLMD',
         '.......LhLLDMD',
         '.....LLLLDLLMD',
         '...LLhLLDLLLMD',
         '..LhLLLDLLLLM.',
         '.LLLLLDLLLLMD.',
         'PPPpLLLLLLMMD.',
         'PppPLLLLLMMD..',
         '.PPPMMMMMDD...',
         '...DDDDD......'], {'L': c[3], 'h': c[4], 'M': c[2], 'D': c[1], 'P': '#ff9ac0', 'p': '#c8507a'}, 1, 2)
    return s.render()


def ocarina():
    s = S()
    o = ['#0e1e4a', '#1a3478', '#2a4ea8', '#4a72d0', '#7a9ef0']
    s.g(['.........LL..', '......LLLhMD.', '...LLLhLLLMD.', '.LLhLLLLLLMD.', 'LhLLLLLLLLMMD', 'LLLLLLLLLLMD.', '.LLLLLLLLMMD.', '..MMMMMMMDD..', '....DDDDD....'],
        {'L': o[3], 'h': o[4], 'M': o[2], 'D': o[1]}, 1, 4)
    for (x, y) in ((5, 8), (7, 7), (9, 8), (6, 10), (9, 10)): s.px(x, y, o[0])
    s.px(11, 5, '#ffe14a')
    return s.render()


def monocle(lens, rim=GOLD, chain=True):
    def f():
        s = S()
        s.disc(7, 7, 5.4, rim)
        s.disc(7, 7, 4.0, ramp(lens), light=(0.6, 0.8))
        s.px(5, 5, '#ffffff'); s.px(6, 4, '#ffffff'); s.px(4, 6, '#e8fbff')
        if chain:
            for i, (x, y) in enumerate([(11, 11), (12, 12), (13, 13), (14, 14), (13, 12), (14, 13)]):
                s.px(x, y, rim[2] if i % 2 else rim[1])
        return s.render()
    return f


def lag_lens():
    s = S()
    s.line(2, 14, 6, 10, WOOD[2], 2)
    s.disc(10, 6, 5.0, ramp('#3a7a3a'))
    s.disc(10, 6, 3.7, ramp('#7cff5a'), light=(0.6, 0.8))
    s.px(8, 4, '#ffffff'); s.px(9, 3, '#e8ffe0')
    return s.render()


def vampire_mirror():
    s = S()
    s.line(2, 14, 6, 10, ['#1a0a04', '#3a1a0a', '#5a2a14', '#7a3a1e'][2], 2)
    s.px(3, 13, GOLD[3]); s.px(5, 11, GOLD[3])
    s.disc(10, 6, 5.2, ['#3a0608', '#6a0e12', '#a01a1e', '#d03a32'])
    s.disc(10, 6, 3.8, ['#4a5a78', '#6a80a8', '#8aa4cc', '#b8ccec'], light=(0.6, 0.8))
    s.line(8, 4, 10, 2, '#ffffff')
    return s.render()


def enchanted_sundial():
    s = S()
    s.g(['.....Y....', '....YY....', '...Yy.....', '..YYYYYY..'], {'Y': GOLD[3], 'y': GOLD[4]}, 3, 2)
    s.g(['QQQQQQQQQQQQ', 'QqqqqqqqqqqQ', '.QQQQQQQQQQ.'], {'Q': '#f0ece0', 'q': '#c8c0b0'}, 2, 6)
    s.g(['....SS....', '....SS....', '...SSSS...', '..SSSSSS..'], {'S': STONE[3]}, 3, 9)
    for (x, y) in ((3, 6), (6, 6), (9, 6), (12, 6)): s.px(x, y, '#8a7a5a')
    s.px(12, 3, '#d8a8ff'); s.px(2, 4, '#d8a8ff')
    return s.render()


def emma_ribbon():
    s = S()
    p = ramp('#ff6ac8')
    s.g(['LL.......LL.', 'LhL.....LhL.'[:12], 'LLLL...LLLL.', 'LLLLMKMLLLLM', 'LLLLMKMLLLLM', 'LLLL.M.LLLL.', 'MM...M...MM.', '....M.M.....', '...M...M....', '..M.....M...'],
        {'L': p[3], 'h': p[4], 'M': p[1], 'K': p[0]}, 2, 3)
    return s.render()


def elytra_repair_kit():
    s = S()
    _sheet(s, 3, 3, 10, 11, ['#4a3a2a', '#6a5a46', '#8a7860', '#a89878', '#c8b898'], fold=False)
    s.g(['....II....', '...I..I...'], {'I': IRON[2]}, 3, 1)
    s.g(['.MM..MM.', 'MmMM.MmM', 'MmM..MmM', '.M....M.'], {'M': '#a8a0c8', 'm': '#d8d0f0'}, 4, 6)
    s.px(8, 11, '#ffd23f')
    return s.render()


def copper_cog():
    s = S()
    c = COPPER
    for k in range(8):
        a = k * math.pi / 4
        x, y = 8 + 6 * math.cos(a), 8 + 6 * math.sin(a)
        s.disc(x, y, 1.4, c[1:])
    s.disc(8, 8, 5.0, c)
    s.disc(8, 8, 2.0, ['#00000000'] if False else c[:2], light=(0.6, 0.8))
    for (x, y) in ((7, 7), (8, 7), (7, 8), (8, 8)): s.px(x, y, None)
    return s.render()


def obsidian_skull():
    s = S()
    o = ['#0a0612', '#1a1028', '#2e1e44', '#46306a', '#6a4a94']
    s.g(['..LLLLLLLL..', '.LhLLLLLLLM.', 'LhLLLLLLLLMD', 'LLEEELLEEEMD', 'LLEWELLEWEMD', 'LLEEELLEEEMD', 'LLLLLLLLLLMD', '.LLLLKKLLLM.', '..LMLMMLMD..',
         '..LDLDDLDD..', '...DDDDDD...'], {'L': o[2], 'h': o[3], 'M': o[1], 'D': o[0], 'E': '#ff6a1a', 'W': '#ffd060', 'K': o[0]}, 2, 2)
    return s.render()


def ring_burrows():
    s = S()
    s.ring(8, 9, 6.0, 5.2, 2.0, ['#4a2c10', '#7a4c1e', '#a87030', '#d09a4a', '#f0c070'])
    s.g(['.GG.', 'GggG', '.GG.'], {'G': GOLD[3], 'g': '#ffffff'}, 6, 2)
    return s.render()


def moon_ward():
    s = S()
    m = ['#8890a8', '#b0b8cc', '#d8deea', '#f4f6fa', '#ffffff']
    s.g(['...LLLL..', '.LLhL....', 'LLhL.....', 'LhL......', 'LhL......', 'LhL......', 'LLL......', 'LLLL.....', '.LLLM....', '..MMMMMD.', '....DDD..'],
        {'L': m[3], 'h': m[4], 'M': m[1], 'D': m[0]}, 3, 2)
    s.g(['.R.', 'RRR', '.R.'], {'R': '#d02a2a'}, 11, 5)
    return s.render()


def phoenix_feather(vane, rib, ash=False):
    def f():
        s = S()
        v = ramp(vane)
        for i in range(10):
            x, y = 3 + i, 12 - i
            s.px(x, y, v[3]); s.px(x + 1, y, v[2]); s.px(x, y - 1, v[4]); s.px(x + 1, y + 1, v[1])
        s.line(2, 14, 12, 4, rib)
        s.px(1, 15, rib)
        if not ash:
            for (x, y) in ((13, 1), (14, 2), (12, 0)): s.px(x, y, '#fff0a0')
        else:
            for (x, y) in ((6, 12), (9, 10), (12, 5)): s.px(x, y, '#ff6a1a')
        return s.render()
    return f


def sanguine_fang():
    s = S()
    s.g(['WWWWWWW', 'WhWWWWD', '.WWWWD.', '.WWWD..', '..WWD..', '..WD...', '..WD...', '...D...'], {'W': '#f4f0e6', 'h': '#ffffff', 'D': '#c8c0b0'}, 4, 1)
    s.g(['R', 'R', 'r', '.', 'r'], {'R': '#c41a1a', 'r': '#8a0a10'}, 7, 9)
    return s.render()


def vault_hound_whistle():
    s = S()
    s.g(['.YYYYYYYY..', 'YhYYYYYYMk.', 'YYYYYYYYMk.', 'MMMMMMMMMk.', '.DDDDDDDD..'], {'Y': GOLD[3], 'h': GOLD[4], 'M': GOLD[2], 'D': GOLD[1], 'k': '#2a1804'}, 1, 7)
    s.g(['..CC', '.C..C'[:4], 'C...', '.C..'], {'C': BRASS[2]}, 11, 2)
    s.px(14, 4, BRASS[2]); s.px(13, 6, BRASS[2])
    s.px(4, 8, '#2a1804')
    return s.render()


def void_totem():
    s = S()
    v = PURPLE
    s.g(['....LLLL....', '...LhLLLM...', '...LKLLKM...', '...LLLLLM...', '..LLLLLLLM..', '.LLhLLLLLLM.', 'LLLLWWWLLLMD', 'LLLLWWWLLLMD', '.LLLLLLLLMD.',
         '..LLLLLLMD..', '...LLLLMD...', '....DDDD....'], {'L': v[2], 'h': v[4], 'M': v[1], 'D': v[0], 'K': '#08020e', 'W': '#e8d0ff'}, 2, 2)
    return s.render()


def tidal_tear():
    s = S()
    c = ['#3a7090', '#5a9ab8', '#8ac8e0', '#c0eaf8', '#ffffff']
    s.g(['L..........L', 'LL........LL', 'LhL......LhL', '.LhL....LhL.', '.LLLL..LLLL.', '..LLLLLLLLL.', '...LLLLLLL..', '....MMMMM...'], {'L': c[2], 'h': c[4], 'M': c[1]}, 2, 3)
    _gem_drop_small(s, '#d040b0', 6, 6)
    return s.render()


def pocket_slots():
    s = S()
    r = ramp('#d02a2a')
    s.g(['GGGGGGGGGGG.', 'GRRRRRRRRRG.', 'GRWWRWWRWWGL', 'GRwWRwWRwWGL', 'GRRRRRRRRRG.', 'GGGGGGGGGGGL', 'GddddddddGG.', 'GGGGGGGGGGG.'],
        {'G': GOLD[3], 'R': r[2], 'W': '#ffffff', 'w': '#e02a2a', 'd': '#3a2a10', 'L': IRON[2]}, 1, 4)
    s.g(['I', 'I', 'O'], {'I': IRON[2], 'O': '#e02a2a'}, 13, 2)
    return s.render()


def smugglers_veil():
    """the Smuggler's Veil: a dark net veil hanging from a brass ring, its hem weighted"""
    s = S()
    v = ['#1a1a24', '#2e2e3c', '#444456', '#5e5e74', '#7a7a92']
    s.g(['..BBBB..', '.B....B.'], {'B': BRASS[2]}, 4, 0)
    for y in range(2, 14):
        w = min(2 + (y - 2) // 2, 6)
        for x in range(8 - w, 8 + w):
            k = 3 if x < 8 - w + 2 else (1 if x >= 8 + w - 2 else 2)
            s.px(x, y, v[k] if (x + y) % 2 else v[k - 1])
    for x in range(2, 14, 2): s.px(x, 14, BRASS[1])
    return s.render()


def rubber_chicken():
    """the rubber chicken: limp and yellow, a red comb, an orange beak, its legs dangling"""
    s = S()
    y = ['#a87a10', '#d8a820', '#f8d040', '#ffe880', '#fff6c8']
    s.g(['.........RR...',
         '........RYYY..',
         '........YkYYOO',
         '........YYYY..',
         '.......YYYM...',
         '......YhYM....',
         '.....YhYYM....',
         '...YYhYYYM....',
         '..YhYYYYMM....',
         '.YYYYYYMM.....',
         'YYYYYMMM......',
         '.MMMMO.O......',
         '.....O..O.....'], {'Y': y[3], 'h': y[4], 'M': y[1], 'R': '#e02a2a', 'O': '#ff8a1a', 'k': '#1a1a1a'}, 1, 1)
    return s.render()


def rubber_duck():
    s = S()
    y = ramp('#ffe04a')
    s.g(['.....YYYY...', '....YhYYYM..', '....YYkYYMOO', '.....YYYMOO.', '.YYYYYYYYM..', 'YhYYYYYYYYM.', 'YYYYYYYYYYM.', 'YYYYYYYYYMM.', '.MMMMMMMMM..'],
        {'Y': y[3], 'h': y[4], 'M': y[1], 'k': '#1a1a1a', 'O': '#ff8a1a'}, 2, 4)
    return s.render()


def songbird():
    """the clockwork Songbird: a brass bird, a winding key in its back, a note in its beak"""
    s = S()
    b = BRASS
    s.g(['....LLL....', '...LhLkL...', '..LLLLLLO..', '.LLLLLLL...', 'LLLLLLLLM..', 'LhLLLLLMM..', '.LLLLLLM...', '..MMMMM....', '...D..D....', '..DD.DD....'],
        {'L': b[3], 'h': b[4], 'M': b[1], 'k': '#1a1a1a', 'O': '#ff8a1a', 'D': IRON[1]}, 3, 4)
    s.g(['.I.', 'III', '.I.'], {'I': IRON[3]}, 1, 7)
    s.g(['.N', 'NN', 'N.'], {'N': '#ffffff'}, 13, 1)
    return s.render()


def pocket_rift():
    s = S()
    s.disc(8, 8, 6.8, ['#0a3a3a', '#146a6a', '#2aa0a0', '#5ad8d0', '#a8fff4'])
    s.disc(8, 8, 4.6, ['#000000', '#06020e', '#0e0620', '#180a32'])
    for (x, y) in ((6, 6), (10, 9), (7, 10), (9, 6)): s.px(x, y, '#ffffff')
    return s.render()


OVERRIDES = {
    'bankers_card': bankers_card, 'fixers_card': fixers_card, 'pearl_card': pearl_card, 'scratch_card': scratch_card,
    'merc_contract': merc_contract, 'blood_bounty': blood_bounty, 'tip_bloodmoon': tip_bloodmoon, 
    'brass_wing_scroll': brass_wing_scroll, 'market_crest_scroll': market_crest_scroll, 
    'crimson_ledger': crimson_ledger, 'fixers_ledger': fixers_ledger, 'smugglers_ledger': smugglers_ledger,
    'pocket_watch': pocket_watch, 'stolen_watch': stolen_watch, 'the_alibi': the_alibi, 'thiefs_hourglass': thiefs_hourglass,
    'crimson_hourglass': crimson_hourglass, 'bidding_paddle': bidding_paddle,
}
OVERRIDES.update({f'lucky_fragment_{k}': lucky_fragment(k) for k in range(1, 10)})

OVERRIDES.update({
    'dish_potpie': dish_potpie, 'dish_roast': dish_roast,
    'dish_drumsticks': dish_drumsticks, 'coffee': coffee, 'golden_cheese_wheel': golden_cheese_wheel,
    'bottomless_lava': bucket('#ff7a1a'), 'bottomless_water': bucket('#3a7aff'),
    'smelling_salts': smelling_salts, 'smoke_bomb': smoke_bomb, 'smuggler_jar_full': smuggler_jar_full,
    'crate_wood': lootbox(WOOD, IRON, ['LLLL', 'llll', 'LLLL'], {'L': WOOD[4], 'l': WOOD[1]}),
    'crate_stone': lootbox(STONE, IRON, ['SS.S', 'S.SS', 'SS.S'], {'S': STONE[4]}),
    'crate_raw': lootbox(['#3a2414', '#5a3820', '#7a5030', '#9a6a40', '#ba8a5a'], COPPER, ['.CC.', 'CcCC', '.CC.'], {'C': COPPER[3], 'c': COPPER[4]}),
    'crate_mineral': lootbox(STONE, GOLD, ['.D..', 'DdD.', '.D.G'], {'D': '#5ae8f0', 'd': '#ffffff', 'G': GOLD[3]}),
    'crate_adventure': lootbox(['#14304a', '#1e4868', '#2a6488', '#3a80a8', '#5aa0c8'], GOLD, ['.R..', 'RRR.', '.R..'], {'R': '#e02a2a'}),
    'display_case_oak': display_case(WOOD), 'display_case_dark_oak': display_case(['#1e1208', '#32200e', '#4a3016', '#62421e', '#7a5428']),
    'display_case_gilded': display_case(GOLD), 'display_case_quartz': display_case(['#a8a29a', '#c8c2ba', '#e0dcd4', '#f4f0ea', '#ffffff']),
    'hoard_sack': hoard_sack, 'ender_pouch': ender_pouch, 'vacuum_satchel': vacuum_satchel(False), 'vacuum_satchel_on': vacuum_satchel(True),
    'caged_spawner': caged_spawner, 'fy_bowl': fy_bowl,
})

OVERRIDES.update({
    'echo_bell': bell(GOLD, extra=_echo_extra), 'fair_weather_bell': bell('#ffe08a', extra=_fw_extra),
    'merchants_bell': bell(['#8a6a2a', '#b89040', '#e0b860', '#f4d488', '#fff0c0']), 'pearl_bell': bell(['#5a6a7a', '#8a9aaa', '#b8c6d4', '#e0e8f0', '#ffffff'], extra=_pearl_extra),
    'lava_charm': lava_charm, 'lava_wader_charm': lava_wader_charm, 'surface_charm': surface_charm, 'water_charm': water_charm,
    'specter_charm': specter_charm, 'showstopper_charm': showstopper_charm, 'fizzle_stone': fizzle_stone, 'gale_locket': gale_locket,
    'lodestone_locket': lodestone_locket, 'wilfrey_locket': wilfrey_locket, 'wayfarers_lodestar': wayfarers_lodestar, 'horseshoe': horseshoe,
    'kraken_conch': kraken_conch, 'ocarina': ocarina, 'cipher_monocle': monocle('#a8e0ff'), 'frog_monocle': monocle('#a8e0ff', chain=True),
    'lag_lens': lag_lens, 'vampire_mirror': vampire_mirror, 
    'enchanted_sundial': enchanted_sundial, 'emma_ribbon': emma_ribbon, 'elytra_repair_kit': elytra_repair_kit, 'copper_cog': copper_cog,
    'obsidian_skull': obsidian_skull, 'ring_burrows': ring_burrows, 'moon_ward': moon_ward,
    'phoenix_plume': phoenix_feather('#ff7a2a', '#a83a0a'), 'phoenix_ash': phoenix_feather('#6a5a5a', '#2a1a1a', ash=True),
    'sanguine_fang': sanguine_fang, 'vault_hound_whistle': vault_hound_whistle, 'void_totem': void_totem, 'tidal_tear': tidal_tear,
    'pocket_slots': pocket_slots, 'smugglers_veil': smugglers_veil, 'rubber_chicken': rubber_chicken, 'rubber_duck': rubber_duck,
    'songbird': songbird, 'pocket_rift': pocket_rift,
})

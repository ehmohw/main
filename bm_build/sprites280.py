"""2.80: the sprite repaint - forty of the pack's weakest item icons drawn again.

The old icons were mostly one-pixel lines and flat blobs with no outline. Each is redrawn at the same 16x16 size, bolder
(sticks two pixels wide, shapes filling the frame), with its own shading and highlights, then finished like every other
icon: a dark outline round the silhouette, then vanilla.process's top-left light and tinted outline. The items, their
names and their models are unchanged - only the textures. A small kit draws them: grids for detail, lines, discs and
rings for the round and diagonal shapes.

    gen_rp appends sprites280.post as its last hook: the icons are written over the old ones, wherever those came from."""
import math
from PIL import Image


def hx(h):
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


class S:
    """a 16x16 sketch"""
    def __init__(self):
        self.p = {}

    def px(self, x, y, c):
        if 0 <= x < 16 and 0 <= y < 16:
            if c is None: self.p.pop((x, y), None)
            else: self.p[(x, y)] = hx(c) if isinstance(c, str) else c

    def g(self, rows, pal, x0=0, y0=0):
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch not in '. ': self.px(x0 + x, y0 + y, None if ch == '_' else pal[ch])
        return self

    def line(self, x0, y0, x1, y1, c, w=1):
        """a line w pixels wide (stamped along x for steep/diagonal lines, along y for shallow ones); c may be
        c(i, n) - a colour per step, for bands"""
        n = max(abs(x1 - x0), abs(y1 - y0))
        steep = abs(y1 - y0) >= abs(x1 - x0)
        for i in range(n + 1):
            x = round(x0 + (x1 - x0) * i / n) if n else x0
            y = round(y0 + (y1 - y0) * i / n) if n else y0
            cc = c(i, n) if callable(c) else c
            for k in range(w):
                self.px(x + k, y, cc) if steep else self.px(x, y + k, cc)
        return self

    def disc(self, cx, cy, r, ramp, light=(-0.6, -0.8), sq=1.0):
        """a ball lit from the top-left: ramp runs dark -> light"""
        for y in range(16):
            for x in range(16):
                dx, dy = (x + 0.5 - cx), (y + 0.5 - cy) / sq
                d = math.hypot(dx, dy)
                if d <= r:
                    nx, ny = dx / r, dy / r
                    nz = math.sqrt(max(0.0, 1 - nx * nx - ny * ny))
                    v = -(nx * light[0] + ny * light[1]) * 0.75 + nz * 0.55
                    i = int((v + 0.45) / 1.5 * len(ramp))
                    self.px(x, y, ramp[max(0, min(len(ramp) - 1, i))])
        return self

    def ring(self, cx, cy, rx, ry, t, ramp, light=(-0.6, -0.8), front=None):
        """an elliptical band t pixels thick; lit by angle. front: a colour ramp for the near (lower) half"""
        for y in range(16):
            for x in range(16):
                dx, dy = (x + 0.5 - cx), (y + 0.5 - cy)
                e_out = (dx / rx) ** 2 + (dy / ry) ** 2
                e_in = (dx / max(0.5, rx - t)) ** 2 + (dy / max(0.5, ry - t)) ** 2
                if e_out <= 1.0 and e_in >= 1.0:
                    a = math.atan2(dy, dx)
                    v = -(math.cos(a) * light[0] + math.sin(a) * light[1])
                    rr = front if (front and dy > 0) else ramp
                    i = int((v + 1) / 2 * len(rr))
                    self.px(x, y, rr[max(0, min(len(rr) - 1, i))])
        return self

    def image(self):
        im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
        for (x, y), c in self.p.items():
            im.putpixel((x, y), c)
        return im

    def render(self, outline=True):
        im = self.image()
        if outline:
            px = im.load()
            add = [(x, y) for y in range(16) for x in range(16) if px[x, y][3] == 0 and
                   any(0 <= x + dx < 16 and 0 <= y + dy < 16 and px[x + dx, y + dy][3] > 0 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
            for x, y in add:
                px[x, y] = (18, 14, 14, 255)
        import vanilla
        return vanilla.process('__sprite280', im)


# ------------------------------------------------------------------ palettes (dark -> light)
WOOD = ['#3d2614', '#5e3b1f', '#80522c', '#a26d3c', '#c48e58']
GOLD = ['#6e4410', '#a06c14', '#d29a22', '#f2c440', '#fff1a6']
IRON = ['#3e434a', '#646b74', '#8f97a1', '#bfc6cf', '#eef2f6']
BRASS = ['#5a3a12', '#8a5e1c', '#b9862e', '#dcb050', '#f6dc8e']
BONE = ['#6e6450', '#a3977a', '#cdc2a4', '#ebe2c8', '#fffaf0']
RED = ['#4e0d0d', '#851a18', '#bb2c24', '#e4523e', '#ff9a80']
GREEN = ['#173d12', '#2b6a1d', '#45962c', '#6ec140', '#a8e878']
PURPLE = ['#2a0e44', '#4b1d75', '#7432a8', '#a35ad6', '#d8a8ff']
TEAL = ['#0e3b3d', '#17646a', '#249a9e', '#48cfc8', '#a6fff2']
PINK = ['#6a1240', '#a3205f', '#d63a86', '#ff6ab0', '#ffb6dc']
GLASS = ['#3c6478', '#6a9ab0', '#a8d8ec', '#e8fbff']
STONE = ['#3a3a3e', '#5a5a60', '#7c7c84', '#a2a2aa', '#c8c8d0']
BLACK = ['#121014', '#24202a', '#3a3440', '#565060', '#7a7486']
CLAY = ['#4e2414', '#7a3a1e', '#a6552c', '#c87444', '#e8a070']
SACK = ['#4a3a20', '#6e5a34', '#937a4a', '#b89e66', '#dcc68e']
GHOST = ['#5e8a96', '#8cbcc6', '#bfe6ea', '#e6fbfb', '#ffffff']
SLIME = ['#0d4a2e', '#178a4e', '#2ccf72', '#7cf7a6', '#d8ffe6']
OLIVE = ['#2a3216', '#465226', '#66763a', '#8a9c52', '#b4c47a']
COPPER = ['#54281a', '#84432d', '#c15a36', '#e3825a', '#fcb08a']


def band(*cols, every=2):
    """a colour per step along a line: bands of `every` pixels"""
    return lambda i, n: cols[(i // every) % len(cols)]


# ------------------------------------------------------------------ the icons
def band_of_regeneration():
    s = S()
    s.ring(8, 10.5, 5.5, 4.2, 2, GOLD[1:], front=GOLD[:4])
    s.g(['.R.R.', 'RPRrR', 'RRRrR', '.Rrr.', '..r..'], {'R': RED[3], 'r': RED[2], 'P': RED[4]}, 6, 1)
    s.px(6, 6, GOLD[2]); s.px(10, 6, GOLD[2]); s.px(8, 6, GOLD[1])
    return s.render()


def skeleton_lockpick():
    s = S()
    s.line(3, 12, 7, 8, BONE[2], 2)                              # the bone handle
    s.g(['BB.', 'BbB', '.BB'], {'B': BONE[3], 'b': BONE[1]}, 1, 12)
    s.g(['.BB', 'BbB', 'BB.'], {'B': BONE[3], 'b': BONE[1]}, 7, 6)
    s.line(9, 7, 13, 3, IRON[3])                                 # the pick
    s.line(10, 7, 13, 4, IRON[1])
    s.g(['II', '.I', '.i'], {'I': IRON[4], 'i': IRON[2]}, 13, 1)
    return s.render()


def rat_familiar():
    s = S()
    pal = {'G': '#9a9aa4', 'g': '#73737e', 'd': '#55555f', 'L': '#c6c6d0', 'P': '#ff9ab8', 'p': '#d66a8e', 'K': '#111018',
           'W': '#ffffff', 'N': '#ff5a8a', 'w': '#e6e6ee'}
    s.g(['................',
         '..ggg......ggg..',
         '.gGPPg....gPPGg.',
         '.gPppG....GppPg.',
         '.gGppGGGGGGppGg.',
         '..gGGLLLLLLGGg..',
         '...GLLLLLLLLG...',
         '..GLKWLLLLKWLG..',
         '..GLKKLLLLKKLG..',
         '..gGLLLLLLLLGg..',
         '.w.gGLLNNLLGg.w.',
         '..w.gGLppLGg.w..',
         '.....gGGGGg.....',
         '......dddd......'], pal)
    return s.render()


def blob_cane():
    s = S()
    s.line(2, 14, 10, 6, lambda i, n: BLACK[3] if i % 3 else BLACK[2], 2)
    s.px(2, 14, IRON[4]); s.px(3, 14, IRON[3]); s.px(2, 13, IRON[3]); s.px(3, 13, IRON[3])
    s.g(['.GGGG.', 'GYYGGg', 'GY..Gg', '....Gg', '...gG.'], {'G': GOLD[3], 'g': GOLD[1], 'Y': GOLD[4]}, 9, 1)
    s.px(10, 6, GOLD[2]); s.px(11, 6, GOLD[2])
    return s.render()


def trial_key_fob():
    s = S()
    s.ring(5, 5, 3.6, 3.6, 1.3, IRON[1:])
    s.g(['.CCCCC.',
         'CcTTTcC',
         'CTtTTTC',
         'CTTttTC',
         'CTTTTTC',
         'CcTTTcC',
         '.CCcCC.'], {'C': COPPER[2], 'c': COPPER[1], 'T': TEAL[3], 't': TEAL[4]}, 7, 7)
    s.px(7, 7, IRON[2]); s.px(8, 8, IRON[3])
    return s.render()


def duelists_ribbon():
    s = S()
    s.line(6, 9, 4, 14, RED[2], 2); s.line(9, 9, 11, 14, RED[1], 2)
    s.px(4, 15, None); s.px(12, 14, None)
    s.disc(8, 6, 5.2, [GOLD[1], GOLD[2], GOLD[3], GOLD[4]])
    for k in range(12):                                          # the pleats
        a = k * math.pi / 6
        s.px(round(8 + 4.6 * math.cos(a) - 0.5), round(6 + 4.6 * math.sin(a) - 0.5), GOLD[1])
    s.disc(8, 6, 2.6, [RED[1], RED[2], RED[3], RED[4]])
    s.px(7, 5, '#fff1d0')
    return s.render()


def pool_noodle():
    s = S()
    s.line(2, 13, 12, 3, lambda i, n: PINK[4] if i % 3 == 0 else PINK[3], 3)
    s.line(3, 13, 13, 3, lambda i, n: PINK[2] if i % 3 == 0 else PINK[2], 1)
    s.g(['.pP', 'pqp', 'Pp.'], {'p': PINK[1], 'P': PINK[2], 'q': PINK[0]}, 12, 1)
    return s.render()


def firefly_jar():
    s = S()
    s.g(['....wwwwww....', '....WWWWWW....', '...cccccccc...'], {'w': WOOD[2], 'W': WOOD[3], 'c': GLASS[1]}, 1, 1)
    for y in range(4, 14):
        s.px(3, y, GLASS[2]); s.px(12, y, GLASS[1])
        for x in range(4, 12): s.px(x, y, '#1a2440' if y > 4 else '#24304e')
    for x in range(3, 13): s.px(x, 14, GLASS[1])
    s.px(4, 5, GLASS[3]); s.px(4, 6, GLASS[3]); s.px(4, 7, GLASS[2])
    for (x, y) in ((6, 6), (9, 8), (7, 11), (10, 12), (5, 9)):
        s.px(x, y, '#f4ff7a')
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x + dx, y + dy) in s.p and s.p[(x + dx, y + dy)][:3] in ((0x1a, 0x24, 0x40), (0x24, 0x30, 0x4e)):
                s.px(x + dx, y + dy, '#5a7a3a')
    return s.render()


def clockwork_key():
    s = S()
    s.g(['..BBBB..BBBB...',
         '.BbbbbBBbbbbB..',
         '.BbHHbBBbHHbB..',
         '.BbHbbBBbbHbB..',
         '.BbbbbBBbbbbB..',
         '..BBBBccBBBB...',
         '......cC.......',
         '......cC.......',
         '......cC.......',
         '......cC.......',
         '......cCBB.....',
         '......cCbB.....',
         '......cCBB.....',
         '......cC.......',
         '......cc.......'], {'B': BRASS[3], 'b': BRASS[1], 'H': BRASS[4], 'c': BRASS[2], 'C': BRASS[3]}, 1, 1)
    return s.render()


def tinkers_thimble():
    s = S()
    s.g(['.....IIIII.....',
         '...IIiIIiII....',
         '..IIIIIIIIIi...',
         '..IiIIiIIiIi...',
         '.IIIIIIIIIIIi..',
         '.IiIIiIIiIIii..',
         '.IIIIIIIIIIIi..',
         '.IiIIiIIiIIii..',
         '.IIIIIIIIIIIi..',
         '.IiIIiIIiIIii..',
         'BBBBBBBBBBBBBb.',
         'bBBbBBBbBBBbbb.',
         '.bbbbbbbbbbbb..'], {'I': IRON[3], 'i': IRON[1], 'B': BRASS[3], 'b': BRASS[1]}, 0, 2)
    s.px(3, 4, IRON[4]); s.px(3, 5, IRON[4]); s.px(4, 3, IRON[4])
    return s.render()


def fallen_star():
    s = S()
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        r = 6.4 if k % 2 == 0 else 2.7
        pts.append((8 + r * math.cos(a), 8.5 + r * math.sin(a)))
    def inside(x, y):
        c = False
        for i in range(10):
            (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % 10]
            if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1): c = not c
        return c
    for y in range(16):
        for x in range(16):
            if inside(x + 0.5, y + 0.5):
                d = (x - 6) * 0.6 + (y - 6) * 0.8
                s.px(x, y, GOLD[4] if d < -2 else GOLD[3] if d < 2 else GOLD[2] if d < 5 else GOLD[1])
    s.px(7, 6, '#ffffff'); s.px(6, 7, '#fff8d0')
    for (x, y) in ((1, 2), (14, 1), (14, 13)):
        s.px(x, y, '#fff6b0')
    return s.render()


def specter_sheet():
    s = S()
    s.g(['......LLLL......',
         '....LLWWWWLL....',
         '...LWWWWWWWWL...',
         '..LWWWWWWWWWWL..',
         '..LWWKKWWKKWWL..',
         '..LWWKKWWKKWWm..',
         '.LWWWWWWWWWWWWL.',
         '.LWWWWWKKWWWWWm.',
         '.LWWWWWWWWWWWWm.',
         '.LWWmWWWWWmWWWm.',
         '.LWWmWWWWWmWWWm.',
         '.LWWmWWWWWmWWmm.',
         '.LWmmWWWmWmmWmm.',
         '.LmmLmWmmmLmmLm.',
         '.Lm..mmL.mm..m..'], {'W': GHOST[3], 'L': GHOST[2], 'm': GHOST[1], 'K': '#1a2a3a'})
    s.px(5, 2, GHOST[4]); s.px(4, 3, GHOST[4]); s.px(4, 4, GHOST[4])
    return s.render()


def dish_kebab():
    s = S()
    s.line(1, 14, 14, 1, WOOD[3])
    chunks = [(3, 11, ['#7a3a18', '#a4542a', '#c8784a']), (6, 8, ['#2b6a1d', '#45962c', '#7cc84a']),
              (9, 5, ['#7a3a18', '#a4542a', '#c8784a']), (12, 2, ['#8a1a1a', '#c8302a', '#ff6a50'])]
    for (cx, cy, rp) in chunks:
        s.g(['.ab.', 'abbc', 'abbc', '.ac.'], {'a': rp[0], 'b': rp[1], 'c': rp[2]}, cx - 2, cy - 1)
    s.g(['.ww', 'wvw', 'ww.'], {'w': '#f2e8f6', 'v': '#a868c0'}, 4, 9)
    s.px(1, 14, WOOD[2]); s.px(14, 1, WOOD[4])
    return s.render()


def smuggler_jar():
    s = S()
    s.g(['.....ccc.....',
         '....cCCCc....',
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
         '...jjjjjjj...'], {'c': WOOD[2], 'C': WOOD[4], 'r': '#c8b090', 'R': '#e8d4b0', 'K': '#2a1a10', 'J': CLAY[3], 'j': CLAY[1],
                            'L': '#e8dcc0', 'G': GOLD[3]}, 1, 2)
    s.px(3, 7, CLAY[4]); s.px(3, 8, CLAY[4])
    return s.render()


def clockwork_fragment():
    s = S()
    for y in range(16):
        for x in range(16):
            dx, dy = x + 0.5 - 8, y + 0.5 - 8
            r, a = math.hypot(dx, dy), math.atan2(dy, dx)
            if 0.25 < a < 1.45 + 0.25 * math.sin(r * 2.3): continue          # the break, jagged
            tooth = math.cos(a * 6) > 0.25
            if 2.0 <= r <= (6.9 if tooth else 5.2):
                v = -(math.cos(a) * -0.6 + math.sin(a) * -0.8)
                s.px(x, y, BRASS[4] if (v > 0.6 and r > 4.4) else BRASS[3] if v > 0.1 else BRASS[2] if v > -0.5 else BRASS[1])
    s.line(5, 6, 7, 3, '#3a2a10')                                       # a crack
    for (x, y) in ((8, 4), (4, 8)): s.px(x, y, BRASS[0])                 # rivets
    return s.render()


def mudlarks_charm():
    s = S()
    s.ring(8, 4, 3.3, 3.6, 1, ['#4a3a24', '#6e5634', '#937446'])
    s.disc(8, 10, 4.6, ['#2a5a4a', '#3e7e66', '#5fa284', '#8ac6a2'])     # verdigris
    s.ring(8, 10, 4.6, 4.6, 1, BRASS[1:4])
    s.g(['w.w.w', '.w.w.'], {'w': '#d6f0e0'}, 6, 9)
    s.g(['w.w.w', '.w.w.'], {'w': '#a8d8c0'}, 6, 11)
    return s.render()


def _branch(accent):
    s = S()
    s.line(2, 14, 12, 4, lambda i, n: WOOD[1] if i % 4 == 2 else WOOD[2], 2)
    s.line(3, 14, 13, 4, WOOD[1], 1)
    s.line(5, 11, 3, 8, WOOD[2]); s.line(9, 7, 11, 9, WOOD[2])          # twigs
    s.g(['.L', 'Ll', 'l.'], {'L': GREEN[3], 'l': GREEN[2]}, 2, 6)
    s.g(['L.', 'lL', '.l'], {'L': GREEN[3], 'l': GREEN[2]}, 11, 9)
    s.px(5, 12, WOOD[0]); s.px(9, 8, WOOD[0])                          # knots
    accent(s)
    return s.render()


def branch_bark():
    def a(s):
        for (x, y) in ((4, 12), (6, 10), (8, 8), (10, 6)):
            s.g(['ss', 's.'], {'s': '#8a8072'}, x, y)
        s.g(['.ss.', 'sSSs', 'sSSs'], {'s': '#6e6658', 'S': '#a49a88'}, 11, 1)
    return _branch(a)


def heartwood_branch():
    def a(s):
        s.line(3, 13, 12, 4, lambda i, n: RED[2] if i % 3 else RED[3], 1)
        for (x, y) in ((5, 10), (8, 7), (11, 4), (7, 11)):
            s.px(x, y, '#e8e0c8')
        s.g(['.R.', 'RrR', '.R.'], {'R': RED[3], 'r': RED[4]}, 12, 1)
    return _branch(a)


def branch_seed():
    def a(s):
        s.g(['.cc.', 'cCCc', 'aaaa', 'aAAa', '.aa.'], {'c': WOOD[0], 'C': WOOD[2], 'a': '#a8823a', 'A': '#d6b062'}, 11, 0)
    return _branch(a)


def branch_bloom():
    def a(s):
        for (x, y) in ((12, 2), (3, 7), (10, 9)):
            s.g(['.P.', 'PyP', '.P.'], {'P': PINK[4], 'y': '#fff28a'}, x - 1, y - 1)
    return _branch(a)


def metal_detector():
    s = S()
    s.line(4, 10, 12, 2, IRON[3], 1); s.line(5, 10, 13, 2, IRON[1], 1)
    s.g(['KK', 'KK', 'Kk'], {'K': BLACK[3], 'k': BLACK[2]}, 12, 1)
    s.g(['bbb', 'bRb', 'bbb'], {'b': '#3a5e8a', 'R': '#ff4a3a'}, 8, 5)
    s.ring(4, 12.5, 3.6, 2.2, 1.4, ['#a06a10', '#d29a22', '#f2c440'])
    return s.render()


def four_leaf_charm():
    s = S()
    leaf = ['.LL.LL.', 'LLlLLlL', 'LlLLLlL', '.LllLL.', '..LLL..']
    pal = {'L': GREEN[3], 'l': GREEN[2]}
    s.g(leaf, pal, 1, 1); s.g(leaf, pal, 8, 1)
    s.g(leaf[::-1], pal, 1, 7); s.g(leaf[::-1], pal, 8, 7)
    s.disc(8, 7, 1.5, GREEN[1:4])
    s.line(8, 9, 10, 14, GREEN[1])
    s.ring(8, 1.2, 1.4, 1.2, 1, GOLD[2:])
    for (x, y) in ((3, 2), (10, 2), (3, 9)): s.px(x, y, GREEN[4])
    return s.render()


def _crook(c1, c2, gem, gem_hi):
    s = S()
    s.line(2, 14, 10, 6, band(c1, c2, every=2), 2)
    s.g(['..gGGg.',
         '.gG..Gg',
         '.G....G',
         '......G',
         '.....gG',
         '.....g.'], {'g': GOLD[1], 'G': GOLD[3]}, 8, 0)
    s.px(10, 6, GOLD[2]); s.px(11, 6, GOLD[2]); s.px(10, 5, GOLD[3])
    s.g(['ee', 'eE'], {'e': gem, 'E': gem_hi}, 8, 1)
    s.px(2, 14, GOLD[1]); s.px(3, 14, GOLD[2])
    return s.render()


def pharaoh_crook(): return _crook(GOLD[3], '#2a5ad0', '#1a8a7a', '#5ff0d0')
def crook_ra():      return _crook(GOLD[3], '#2a5ad0', '#c0201a', '#ff8060')
def crook_sands():   return _crook('#e8d098', '#b8904a', '#c89a3a', '#ffe08a')
def crook_sun():     return _crook(GOLD[4], GOLD[2], '#ff9a1a', '#fff27a')


def rod_of_discord():
    s = S()
    s.line(2, 14, 9, 7, lambda i, n: TEAL[2] if i % 3 else GOLD[2], 2)
    s.g(['...pP.', '..pPPp', '.pPWPp', 'pPPPp.', '.pPp..', '..p...'],
        {'p': PURPLE[2], 'P': PINK[3], 'W': '#ffffff'}, 9, 1)
    s.g(['g.g', '.g.'], {'g': GOLD[3]}, 9, 6)
    return s.render()


def courier_whistle():
    s = S()
    s.ring(4, 4, 3.2, 3.2, 1, ['#3a5ea0', '#5a86d0', '#8ab4f0'])          # the lanyard
    s.g(['.BBBBBBB..',
         'BbBBBBBBBB',
         'BBBBBBBBBB',
         'BBBBbbBBB.',
         '.BbbbbbbB.',
         '..bbbbbb..'], {'B': BRASS[3], 'b': BRASS[1]}, 4, 7)
    s.g(['MMM', 'MmM'], {'M': BRASS[2], 'm': BRASS[0]}, 13, 7)
    s.px(5, 8, BRASS[4]); s.px(6, 8, BRASS[4]); s.px(9, 10, '#1a1208')
    return s.render()


def extendo_grip():
    s = S()
    s.line(4, 11, 10, 5, IRON[2], 2)
    s.line(5, 11, 11, 5, IRON[1], 1)
    s.g(['RRRR', 'RrRR', '.Rrr', '..Rr', '..RR'], {'R': RED[3], 'r': RED[1]}, 1, 10)
    s.px(5, 13, GOLD[3]); s.px(6, 13, GOLD[3])
    s.line(11, 4, 12, 1, IRON[3]); s.line(12, 5, 15, 4, IRON[3])          # the jaws, open
    s.px(13, 0, RED[3]); s.px(12, 0, RED[3]); s.px(15, 3, RED[3]); s.px(15, 4, RED[2])
    return s.render()


def pot_of_gold():
    s = S()
    POT = ['#0c0a0e', '#17141c', '#221e28', '#2e2936', '#443e4e']
    s.disc(8, 10.5, 5.6, POT, sq=0.85)
    for x in range(2, 14): s.px(x, 6, POT[3]); s.px(x, 5, POT[2])
    s.px(1, 5, POT[3]); s.px(1, 6, POT[2]); s.px(14, 5, POT[1]); s.px(14, 6, POT[1])
    s.g(['.....cc.c.....',
         '...cCYCcCCc...',
         '..cCCCCCYCCc..',
         '.cCYCCcCCCCCc.',
         'cCCCCCCCCCCCCc'], {'c': GOLD[1], 'C': GOLD[3], 'Y': GOLD[4]}, 1, 0)
    s.px(3, 15, POT[1]); s.px(12, 15, POT[1]); s.px(4, 15, None); s.px(11, 15, None)
    for y in range(8, 12): s.px(4, y, POT[4])
    return s.render()


def bag_of_rocks():
    s = S()
    s.g(['....r.ss.r.....',
         '...rsSrssSr....',
         '....rrSSrr.....',
         '.....tttt......',
         '.....TtTT......',
         '....aaAAaa.....',
         '...aAAAAAAa....',
         '..aAAAAAAAAa...',
         '.aAAAaAAAAAAa..',
         '.aAAAAAAAaAAa..',
         '.aAAAAAAAAAAa..',
         '.aAaAAAAAAAaa..',
         '..aaAAAAAAaa...',
         '...aaaaaaaa....'], {'r': STONE[1], 's': STONE[2], 'S': STONE[3], 't': '#8a6a3a', 'T': '#c8a060',
                               'a': SACK[1], 'A': SACK[3]}, 0, 1)
    s.g(['.ss', 'sSs', 'ss.'], {'s': STONE[2], 'S': STONE[4]}, 12, 12)
    s.px(4, 8, SACK[4]); s.px(4, 9, SACK[4])
    return s.render()


def rpg_launcher():
    s = S()
    s.line(1, 12, 10, 3, OLIVE[2], 3)
    s.line(2, 13, 11, 4, OLIVE[1], 1)
    s.g(['..rr', '.rRR', 'rRRr', 'RRr.'], {'r': RED[1], 'R': RED[3]}, 11, 0)
    s.g(['KK', 'K.', 'K.'], {'K': BLACK[2]}, 5, 11)
    s.g(['KK', '.K'], {'K': BLACK[2]}, 7, 4)
    s.px(1, 13, BLACK[1]); s.px(2, 14, BLACK[1])
    return s.render()


def flak_rocket():
    s = S()
    for y in range(16):
        for x in range(16):
            u, w = x - y, x + y                                          # along the rocket / across it
            c = None
            if -7 <= u <= 5 and 14 <= w <= 16:
                c = IRON[4] if w == 14 else IRON[3] if w == 15 else IRON[2]
                if u in (-1, 0): c = RED[3] if w < 16 else RED[2]
                if u == 3 and w == 15: c = '#5ab0ff'
            elif 6 <= u <= 7 and 14 <= w <= 16: c = RED[3] if w < 16 else RED[2]
            elif 8 <= u <= 9 and w == 15: c = RED[4]
            elif -7 <= u <= -5 and (w in (12, 13) or w in (17, 18)): c = RED[2] if w < 15 else RED[1]
            elif -10 <= u <= -8 and 14 <= w <= 16: c = '#fff07a' if u == -8 else '#ff9a1a'
            if c: s.px(x, y, c)
    return s.render()


def ectoplasm():
    s = S()
    s.g(['................',
         '.......LL.......',
         '......LWLG......',
         '.....GLLLGG.....',
         '....GLLGGGGg....',
         '...GLLGGGGGGg...',
         '..GLGGGGGGGGGg..',
         '.GGGGGGGGGGGGGg.',
         '.GGGGGGGGGGGGgg.',
         '.gGGGGGGGGGgGgg.',
         '..gGGgGGGGggggd.',
         '..g.ddgGGgd..d..',
         '..d...dggd......',
         '.......dd.......'], {'W': '#ffffff', 'L': SLIME[4], 'G': SLIME[3], 'g': SLIME[2], 'd': SLIME[1]})
    s.px(10, 7, SLIME[4]); s.px(5, 9, SLIME[2])
    return s.render()


def navigators_astrolabe():
    s = S()
    s.ring(8, 2, 1.6, 1.5, 1, BRASS[2:])
    s.disc(8, 9, 6, BRASS[:5])
    s.ring(8, 9, 6, 6, 1, BRASS[1:4])
    s.ring(8, 9, 4.2, 4.2, 1, ['#3a2a10', BRASS[1]])
    for (x, y) in ((8, 4), (3, 9), (12, 9), (8, 13)): s.px(x, y, BRASS[0])
    s.line(4, 13, 12, 5, IRON[3])
    s.disc(8, 9, 1.1, IRON[2:])
    return s.render()


def mailbox_icon():
    s = S()
    s.g(['...BBBBBBB..',
         '..BbBBBBBBB.',
         '.BbBBBBBBBBB',
         '.BbBBBBBBBBB',
         '.BbBBBBBBBBB',
         '.bbbbbbbbbbb'], {'B': '#4a7ac0', 'b': '#2e4e86'}, 1, 3)
    s.g(['Rr', 'RR', 'r.', 'i.', 'i.'], {'R': RED[3], 'r': RED[2], 'i': IRON[2]}, 13, 1)
    s.g(['www', 'wkw'], {'w': '#f6f0e0', 'k': '#c8b890'}, 3, 3)
    s.line(6, 9, 6, 15, WOOD[2], 2)
    return s.render()


def vault_breaker():
    s = S()
    s.line(2, 14, 8, 8, lambda i, n: WOOD[2] if i % 3 else WOOD[1], 2)
    s.px(2, 14, IRON[2]); s.px(3, 14, IRON[2])
    s.g(['....EEE..',
         '...EIIIE.',
         '..EIIIIIE',
         '.EIIiiIIE',
         'SIIiyiIE.',
         'SSiiiIE..',
         '.SSiIE...',
         '..SSE....'], {'E': IRON[4], 'I': IRON[2], 'i': IRON[1], 'y': GOLD[3], 'S': '#2e2a34'}, 7, 0)
    return s.render()


def xenite_dowser():
    s = S()
    s.line(3, 14, 7, 9, WOOD[2], 2)
    s.line(7, 9, 4, 3, WOOD[3]); s.line(8, 9, 13, 4, WOOD[3])
    s.g(['.v.', 'vVv', 'vWv', '.v.'], {'v': '#7a2ad0', 'V': '#b86aff', 'W': '#f0d8ff'}, 6, 5)
    s.px(3, 2, '#8affb0'); s.px(14, 3, '#8affb0')
    return s.render()


def butter_sock():
    s = S()
    s.g(['......YY......',
         '.....YyYY.....',
         '....WWWWW.....',
         '....bbbbb.....',
         '....WWWWW.....',
         '....bbbbb.....',
         '....WWWWW.....',
         '....WWWWWw....',
         '...WWWWWWWw...',
         '..WWWWWWWWWw..',
         '.WWWWWWWWWWWw.',
         '.WWWWWWWWWWww.',
         '..wWWWWWWWww..',
         '...wwwwwwww...'], {'W': '#f4f4f0', 'w': '#c4c8cc', 'b': '#3b6fd6', 'Y': '#ffe066', 'y': '#e0b840'}, 1, 1)
    s.g(['.YY', 'YYy', '.yy'], {'Y': '#ffe066', 'y': '#e0b840'}, 6, 10)
    return s.render()


def storm_ball():
    s = S()
    s.disc(8, 8, 6.4, ['#1a2440', '#26365e', '#3a5288', '#5a78b8', '#8aa8e0'])
    s.line(9, 3, 6, 8, '#fff27a'); s.line(6, 8, 10, 8, '#fff27a'); s.line(10, 8, 7, 13, '#fff27a')
    s.px(5, 4, '#e8f4ff'); s.px(4, 5, '#c8dcff')
    return s.render()


def lifeform_analyzer():
    s = S()
    s.g(['..KKKKKKKKKK..',
         '.KkkkkkkkkkkK.',
         '.KkGGGGGGGGkK.',
         '.KkGgGGgGGGkK.',
         '.KkGGgGgGgGkK.',
         '.KkGGGgGGgGkK.',
         '.KkGGGGGGGGkK.',
         '.KkkkkkkkkkkK.',
         '.KkRkYkBkkkkK.',
         '.KkkkkkkkkkkK.',
         '.KkkkIIIkkkkK.',
         '.KkkkkkkkkkkK.',
         '..KKKKKKKKKK..'], {'K': '#3a3e46', 'k': '#5e646e', 'G': '#1a4a2a', 'g': '#5aff8a', 'R': '#ff4a3a',
                              'Y': '#ffd23a', 'B': '#3a8aff', 'I': IRON[3]}, 1, 2)
    s.line(12, 0, 13, 1, IRON[3]); s.px(12, 0, '#ff4a3a')
    return s.render()


OVERRIDES = {f.__name__: f for f in (
    band_of_regeneration, skeleton_lockpick, rat_familiar, blob_cane, trial_key_fob, duelists_ribbon, pool_noodle, firefly_jar,
    clockwork_key, tinkers_thimble, fallen_star, specter_sheet, dish_kebab, smuggler_jar, clockwork_fragment, mudlarks_charm,
    branch_bark, heartwood_branch, branch_seed, branch_bloom, metal_detector, four_leaf_charm, pharaoh_crook, crook_ra,
    crook_sands, crook_sun, rod_of_discord, courier_whistle, extendo_grip, pot_of_gold, bag_of_rocks, rpg_launcher, flak_rocket,
    ectoplasm, navigators_astrolabe, mailbox_icon, vault_breaker, xenite_dowser, butter_sock, storm_ball, lifeform_analyzer)}


def post(R):
    import os
    for name, f in OVERRIDES.items():
        pth = R.p('assets', 'bm', 'textures', 'item', name + '.png')
        assert os.path.exists(pth), name                 # (a repaint, never a new texture)
        f().save(pth)

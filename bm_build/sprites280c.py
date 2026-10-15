"""2.80a: the sprite repaint, part three - what you wear and what you wield: armour, boots, gauntlets, wings and cloaks,
then the blades, hammers, staffs, guns and tools.

Armour keeps vanilla's silhouettes (a chestplate should read as a chestplate), drawn in the 2.80 style: a dark outline,
full shading, each piece's own trim and gems. Weapons stand on the diagonal like vanilla's, two pixels thick.

    sprites280.post writes these too (OVERRIDES here, merged)."""
from sprites280 import S, GOLD, IRON, BRASS, BONE, RED, GREEN, PURPLE, TEAL, PINK, GLASS, STONE, BLACK, COPPER, WOOD, SACK, GHOST
from sprites280b import ramp, emboss


# ================================================================== ARMOUR
def _armour(rows, r, extra=None):
    s = S()
    pal = {'L': r[3], 'h': r[4], 'M': r[2], 'D': r[1], 'd': r[0]}
    if extra: pal.update(extra)
    s.g(rows, pal, 0, 0)
    return s


CHEST = ['................',
         '..LLL......LLM..',
         '.LhLLL....LLLMD.',
         '.LhLLLLLLLLLLMD.',
         '.LLLLLLLLLLLLMD.',
         '..dLhLLLLLLLMd..',
         '...LhLLRLLLMD...',
         '...LLLLLLLLMD...',
         '...LhLLLLLLMD...',
         '...LLLLLLLLMD...',
         '...LLLLLLLMMD...',
         '...MMMMMMMMMD...',
         '....DDDDDDDD....']
HELM = ['................',
        '................',
        '................',
        '....LLLLLLMM....',
        '...LhLLRLLLMD...',
        '..LhLLLLLLLLMD..',
        '..LLLLLLLLLLMD..',
        '..LLMMMMMMMLMD..',
        '..LLD......LMD..',
        '..LLD......MMD..',
        '..DDd......DDd..']
LEGS = ['................',
        '................',
        '...LLLLLLLLMM...',
        '...LhLLRLLLMD...',
        '...LLLLMMLLMD...',
        '...LhLD..LLMD...',
        '...LLLD..LLMD...',
        '...LhLD..LLMD...',
        '...LLLD..LLMD...',
        '...LhLD..LLMD...',
        '...LLLD..LMMD...',
        '...MMMD..MMMD...',
        '...DDDd..DDDd...']
BOOT = ['..TTT.',
        '..LMD.',
        '..LMD.',
        '..LMD.',
        '.hLMD.',
        '.LLMMD',
        'LhLMMD',
        'LLLMMD',
        'DDDDDD']


def boots(base, trim, sole=None, y0=2):
    """two boots, toes to the left; a trim at the cuffs; something under them (blades, glow, springs, waves, rocket fire)"""
    s = S()
    r = ramp(base) if isinstance(base, str) else base
    t = ramp(trim) if isinstance(trim, str) else trim
    for x0 in (1, 8):
        s.g(BOOT, {'T': t[3], 'L': r[3], 'h': r[4], 'M': r[2], 'D': r[1]}, x0 + 1, y0)
    yb = y0 + len(BOOT)
    if sole:
        kind, col = sole
        c = ramp(col)
        for x0 in (2, 9):
            if kind == 'blade':                              # skate blades with a curled toe
                s.g(['.S...S', 'BBBBBBB', 'b......'], {'S': IRON[2], 'B': c[3], 'b': c[4]}, x0 - 1, yb)
            elif kind == 'glow':                             # glowing soles
                s.g(['GGGGGG', '.g..g.'], {'G': c[3], 'g': c[2]}, x0, yb)
            elif kind == 'spring':                           # coiled springs under the heels
                s.g(['..ccc.', '...cc.', '..ccc.'], {'c': c[3]}, x0, yb)
                s.px(x0 + 3, yb + 1, c[1])
            elif kind == 'wave':                             # a curl of water under each boot
                s.g(['W.W.WW', '.wWw..'], {'W': c[3], 'w': c[2]}, x0, yb)
            elif kind == 'rocket':                           # rocket nozzles and their fire
                s.g(['.NNNN.', '.FffF.', '..Ff..'], {'N': IRON[1], 'F': '#ff6a1a', 'f': '#ffe08a'}, x0, yb)
    return s


def gilded_chestplate(): return _armour(CHEST, GOLD, {'R': '#e02a2a'}).render()
def gilded_helmet():     return _armour(HELM, GOLD, {'R': '#e02a2a'}).render()
def gilded_leggings():   return _armour(LEGS, GOLD, {'R': '#e02a2a'}).render()
def gilded_boots():      return boots(GOLD, ['#8a1010', '#b01e1e', '#e02a2a', '#ff6a5a', '#ffb0a0'], y0=4).render()


def rocket_boots(trim='#e8e8f0', base='#ff8a2a'):
    def f():
        return boots(base, trim, ('rocket', '#ff6a1a'), y0=1).render()
    return f


# ================================================================== GAUNTLETS AND CLAWS
GLOVE = ['.......FF.......',
         '....FF.FF.FF....',
         '....FFdFFdFF.FF.',
         '....FFdFFdFFdFF.',
         '....FFdFFdFFdFF.',
         '.TT.FFFFFFFFFFF.',
         '.TTTFFFFFFFFFFF.',
         '..TTFFFFFFFFFFF.',
         '...TFFFFFFFFFFF.',
         '....FFFFFFFFFF..',
         '....CCCCCCCCCC..',
         '....cccccccccc..',
         '....CCCCCCCCCC..',
         '.....DDDDDDDD...']


def gauntlet(skin, cuff, dots=None, glow=None):
    """a glove seen from the back, fingers up, thumb out to the left; its cuff; studs or a glowing seam on the back"""
    def f():
        s = S()
        r = ramp(skin) if isinstance(skin, str) else skin
        c = ramp(cuff) if isinstance(cuff, str) else cuff
        s.g(GLOVE, {'F': r[2], 'd': r[0], 'T': r[2], 'C': c[3], 'c': c[2], 'D': c[1]}, 0, 1)
        for x in (4, 7, 10, 13):                             # each finger lit on its left, shaded on its right
            for y in range(2, 7):
                if s.p.get((x, y)) == s.p.get((x + 1, y)) and (x, y) in s.p: s.px(x, y, r[3])
        for y in range(6, 11): s.px(4, y, r[3])
        s.px(1, 6, r[3]); s.px(2, 6, r[4]); s.px(7, 1, r[4]); s.px(4, 2, r[4])
        for y in range(7, 11): s.px(14, y, r[1])
        if dots:
            dc = ramp(dots)
            for (x, y) in ((6, 7), (9, 7), (12, 7), (7, 9), (10, 9)): s.px(x, y, dc[3])
            s.px(6, 6, dc[4]); s.px(9, 6, dc[4]); s.px(12, 6, dc[4])
        if glow:
            gc = ramp(glow)
            s.g(['..g..', '.gGg.', 'gGWGg', '.gGg.'], {'g': gc[2], 'G': gc[3], 'W': gc[4]}, 7, 6)
        return s.render()
    return f


def climbing_claws():
    """a leather strap across the palm and three steel claws curving out over the top"""
    s = S()
    l = ramp('#9a6a3a')
    s.g(['.LLLLLLLLLL.', 'LhLLLLLLLLMD', 'LLLLLLLLLLMD', 'MMBBMMMMBBMD', '.DDDDDDDDDD.'], {'L': l[3], 'h': l[4], 'M': l[2], 'D': l[1], 'B': BRASS[3]}, 2, 8)
    for x0 in (3, 7, 11):
        s.g(['.c', 'cC', 'CI', 'CI', 'Ii'], {'c': IRON[4], 'C': IRON[3], 'I': IRON[2], 'i': IRON[1]}, x0, 3)
    return s.render()


def talon(accent):
    """a KillerWatt talon: an armoured bracer and three long claws fanning up and right, charged in their colour"""
    def f():
        s = S()
        a = ramp(accent)
        b = ['#141820', '#262c3a', '#3a4254', '#566078', '#7a849c']
        s.line(2, 13, 7, 8, b[2], 3)                         # the bracer
        s.line(2, 14, 7, 9, b[1], 1)
        s.line(3, 12, 7, 8, b[3], 1)
        s.line(3, 13, 6, 10, a[3])                           # its charged seam
        s.px(4, 12, a[4])
        for (x1, y1) in ((12, 1), (14, 4), (14, 8)):        # three claws, tipped with the charge
            s.line(7, 8, x1, y1, BONE[3])
            s.px(x1, y1, a[3])
        s.line(8, 9, 13, 6, BONE[1]); s.line(8, 7, 11, 2, BONE[2])
        for (x, y) in ((13, 0), (15, 3), (15, 9)): s.px(x, y, a[4])
        return s.render()
    return f


# ================================================================== WINGS AND CLOAKS
ELYTRA = ['...LLLL..LLLL...',
          '..LhLLMDDLLLMM..',
          '.LhLLLMD.LLLLMD.',
          '.LhLLLMD.LLLLMD.',
          '.LLLLMMD.LLLMMD.',
          '.LLLLMD..LLLMMD.',
          '.LLLLMD...LLMMD.',
          '.LLLMMD...LLMMD.',
          '..LLMD.....LMD..',
          '..LLMD.....LMD..',
          '..LMD.......MD..',
          '...D.........D..']


def wings(base, vein=None, rim=None):
    def f():
        s = S()
        r = ramp(base) if isinstance(base, str) else base
        s.g(ELYTRA, {'L': r[3], 'h': r[4], 'M': r[2], 'D': r[1]}, 0, 2)
        if vein:
            v = vein
            for (x, y) in ((3, 5), (4, 7), (3, 9), (11, 5), (12, 7), (12, 9)): s.px(x, y, v)
        if rim:
            for x in list(range(3, 7)) + list(range(9, 13)): s.px(x, 2, rim)
        return s.render()
    return f


def star_cloak():
    s = S()
    c = ['#0a0e2a', '#141c48', '#1e2a6a', '#2e3e90', '#4a5ab8']
    s.g(['.....GGGGGG.....',
         '....GLLLLLMG....',
         '...LhLLLLLLMD...',
         '...LhLLLLLLMD...',
         '..LhLLLLLLLLMD..',
         '..LLLLLLLLLLMD..',
         '.LhLLLLLLLLLLMD.',
         '.LLLLLLLLLLLLMD.',
         'LhLLLLLLLLLLLLMD',
         'LLLLLLLLLLLLLLMD',
         'LLMLLMLLLMLLMMDD',
         '.DD.DD.DDD.DD.D.'], {'L': c[2], 'h': c[3], 'M': c[1], 'D': c[0], 'G': GOLD[3]}, 0, 2)
    for (x, y) in ((5, 6), (10, 5), (7, 9), (12, 9), (3, 11), (9, 12), (6, 12)):
        s.px(x, y, '#ffe85a')
    s.px(10, 4, '#fff6c0'); s.px(5, 5, '#fff6c0')
    return s.render()


def umbrella():
    s = S()
    p = ramp('#ff5a8a')
    s.g(['.....LLLLMM.....',
         '...LLhLLLLMMD...',
         '..LhLLWLLLLWMD..',
         '.LhLLWWLLLWWMMD.',
         'LLLLWWWLLWWWMMMD',
         'DD.DDD.DDD.DDD.D'], {'L': p[3], 'h': p[4], 'M': p[2], 'D': p[1], 'W': '#ffffff'}, 0, 1)
    s.line(8, 7, 8, 13, '#3a2a1a')
    s.g(['.d', 'd.', '.d'], {'d': '#3a2a1a'}, 6, 13)
    s.px(7, 15, '#3a2a1a'); s.px(6, 14, None)
    s.px(8, 0, IRON[3])
    return s.render()


def gilded_grin():
    """the Gilded Grin: a gold mask, wide eyes and a toothy grin"""
    s = S()
    s.disc(8, 8, 6.6, GOLD, sq=1.05)
    s.g(['KKK...KKK', 'KwK...KwK', 'KKK...KKK'], {'K': '#2a1804', 'w': '#fff6c0'}, 3, 4)
    s.g(['K.......K', 'KKKKKKKKK', 'KWKWKWKWK', '.KKKKKKK.'], {'K': '#2a1804', 'W': '#fffaf0'}, 3, 9)
    s.px(4, 2, GOLD[4]); s.px(3, 3, GOLD[4])
    return s.render()


def gilded_leaf():
    s = S()
    s.g(['..........hL',
         '........hLLM',
         '.......hLLMD',
         '......hLLMD.',
         '.....hLLMD..',
         '....hLLMD...',
         '...LLLMD....',
         '..LLMD......',
         '.SMD........',
         'S...........'], {'h': GOLD[4], 'L': GOLD[3], 'M': GOLD[2], 'D': GOLD[1], 'S': GOLD[1]}, 2, 2)
    for (x, y) in ((6, 9), (8, 7), (10, 5), (12, 3)): s.px(x, y, GOLD[1])
    return s.render()


def gilded_staff_topper():
    s = S()
    s.g(['Y.........Y', 'yY.......Yy', '.yY.....Yy.', '..yYY.YYy..', '...yYYYy...', '....RRR....', '...RrRRR...',
         '...RRRRR...', '....RRR....', '....yYy....', '....yYy....', '...YYYYY...'],
        {'Y': GOLD[3], 'y': GOLD[2], 'R': '#c41a1a', 'r': '#ff8a7a'}, 2, 1)
    return s.render()


# ================================================================== BLADES, HAFTS AND STAFFS (on the diagonal, like vanilla's)
def _blade(s, blade, x0, y0, n, tip=True, w=2):
    """a blade from (x0, y0) up and to the right, n steps: a lit upper edge, a dark lower edge"""
    for i in range(n):
        x, y = x0 + i, y0 - i
        s.px(x, y, blade[4] if i % 3 == 1 else blade[3])
        s.px(x + 1, y, blade[2])
        if w > 2: s.px(x + 1, y + 1, blade[1])
        else: s.px(x + 1, y + 1, blade[1]) if i < n - 1 else None
    if tip: s.px(x0 + n, y0 - n, blade[4])


def _haft(s, col, x0, y0, x1, y1, w=2):
    """a handle from (x0, y0) to (x1, y1) (bottom-left to top-right), lit on its upper side"""
    n = max(abs(x1 - x0), abs(y1 - y0))
    for i in range(n + 1):
        x = round(x0 + (x1 - x0) * i / n); y = round(y0 + (y1 - y0) * i / n)
        s.px(x, y, col[3])
        if w > 1: s.px(x + 1, y, col[2]); s.px(x + 1, y + 1, col[1]) if w > 2 else None


def sword(blade, guard, grip, pommel, gem=None, n=8):
    s = S()
    _blade(s, blade, 6, 9, n)
    _haft(s, grip, 2, 13, 4, 11)
    s.g(['G...', '.GG.', '.gG.', '...g'], {'G': guard[3], 'g': guard[1]}, 3, 8)        # the guard, across the blade
    s.px(4, 9, guard[4])
    s.g(['PP', 'Pp'], {'P': pommel[3], 'p': pommel[1]}, 1, 13)
    if gem: s.px(5, 10, gem)
    return s


def enchanted_sword():
    return sword(ramp('#8ad8ff'), GOLD, ramp('#2a3a8a'), GOLD, gem='#ffffff').render()


def gutter_cutlass():
    s = S()
    b = IRON
    for i, (x, y) in enumerate([(6, 9), (7, 8), (8, 7), (9, 6), (10, 5), (11, 4), (12, 3), (13, 3), (14, 2)]):
        s.px(x, y, b[3] if i % 3 else b[4]); s.px(x + 1, y, b[2]); s.px(x + 1, y + 1, b[1]) if i < 8 else None
    s.px(14, 1, b[4]); s.px(15, 2, b[2])
    s.g(['.GGG', 'G..G', 'G.gG', '.gg.'], {'G': GOLD[3], 'g': GOLD[1]}, 2, 8)          # the basket hilt
    _haft(s, WOOD, 2, 13, 4, 11)
    s.px(1, 14, GOLD[2])
    return s.render()


def heisters_shiv():
    s = S()
    _blade(s, IRON, 7, 8, 6)
    s.g(['B.', '.B', 'bb'], {'B': BRASS[3], 'b': BRASS[1]}, 5, 8)
    _haft(s, ['#1a1410', '#2a2018', '#3e3024', '#564432', '#6e5a44'], 3, 12, 5, 10)
    s.g(['W.', '.w'], {'W': '#e8e0d8', 'w': '#a8a098'}, 3, 11)                          # cloth wrap
    s.px(2, 13, BRASS[2])
    return s.render()


def thirsting_blade():
    r = ['#3a0608', '#6a0e12', '#a01a1e', '#e0403a', '#ff8a7a']
    s = sword(r, ['#2a0a0a', '#4a1010', '#6a1a1a', '#8a2a2a', '#aa3a3a'], ['#1a0a08', '#2a140e', '#3e2016', '#563020', '#6e402a'], r, n=8)
    for (x, y) in ((9, 7), (12, 4)): s.px(x, y, '#ffb0a0')
    s.px(3, 14, '#c41a1a'); s.px(2, 15, '#8a0a10')                                       # a drop off the pommel
    return s.render()


def demo_scythe():
    """Democratus's scythe: a long black haft, a pale-green crescent blade sweeping off the top, storm-green bands"""
    s = S()
    _haft(s, BLACK, 2, 14, 11, 3)
    for (x, y) in ((5, 11), (8, 8)): s.px(x, y, '#5ad85a'); s.px(x + 1, y, '#2a8a2a')
    bl = ['#2a5a4a', '#4a8a78', '#7ac0aa', '#b8ecdc', '#f0fff8']
    s.g(['.....hhLLLL.GG',
         '...hLLLLMMMMGg',
         '..LLMMDD....gg',
         '.LMD..........',
         'LMD...........',
         'LD............',
         'D.............'], {'L': bl[3], 'h': bl[4], 'M': bl[2], 'D': bl[1], 'G': '#7aff5a', 'g': '#2a8a2a'}, 1, 1)
    return s.render()


def golden_spear():
    s = S()
    _haft(s, WOOD, 2, 14, 10, 6)
    s.g(['..hL', '.hLM', 'hLMD', 'LMD.'], {'h': '#ffffff', 'L': GLASS[2], 'M': GLASS[1], 'D': GLASS[0]}, 11, 1)
    s.g(['GG', 'Gg'], {'G': GOLD[3], 'g': GOLD[1]}, 10, 5)
    s.px(1, 15, GOLD[2])
    return s.render()


def _maul(head, haft, spikes=True):
    s = S()
    _haft(s, haft, 2, 14, 8, 8)
    s.g(['..LLLL..',
         '.LhLLLMM',
         'LhLLLLMD',
         'LLLLLMMD',
         'LLLLMMMD',
         '.LMMMMD.',
         '..DDDD..'], {'L': head[3], 'h': head[4], 'M': head[2], 'D': head[1]}, 7, 1)
    if spikes:
        for (x, y) in ((9, 0), (15, 3), (15, 6), (6, 3), (6, 6), (12, 8)): s.px(x, y, head[2])
    return s


def quake_maul():
    s = _maul(ramp('#c42a22'), ramp('#4a4e58'))
    s.g(['.Y.', 'YY.', '.YY'], {'Y': '#ffe85a'}, 9, 3)                                   # a crack of the quake in it
    return s.render()


def sepulchre():
    s = _maul(ramp('#6a4a9a'), ramp('#3a2e4a'))
    s.g(['.W.', 'WWW', '.W.', '.W.'], {'W': '#d8c8f0'}, 10, 2)                           # a grave's cross
    return s.render()


def spawner_crowbar():
    s = S()
    c = ramp('#5a5e68')
    _haft(s, c, 3, 13, 12, 4)
    s.g(['.LL', 'L.M', '..D'], {'L': c[3], 'M': c[2], 'D': c[1]}, 12, 1)                 # the hooked end
    s.g(['LL', 'DD'], {'L': c[3], 'D': c[1]}, 1, 14)                                     # the split end
    s.px(1, 13, c[4])
    s.line(5, 11, 7, 9, '#c41a1a')                                                       # a red grip band
    return s.render()


def frying_pan():
    s = S()
    _haft(s, ['#2a1a10', '#4a2e1a', '#6a4426', '#8a5a34', '#a87444'], 2, 14, 6, 10)
    s.disc(10, 6, 4.8, ['#141418', '#24242a', '#36363e', '#4e4e58', '#6e6e7a'])
    s.disc(10.3, 6.3, 3.3, ['#0a0a0e', '#16161c', '#24242a'], light=(0.6, 0.8))
    s.px(8, 3, '#8e8e9a')
    return s.render()


def tinker_wrench():
    s = S()
    c = IRON
    _haft(s, c, 3, 13, 10, 6)
    s.g(['.LL.L', 'LhL.L', 'LL...', '.LMD.', '..D..'], {'L': c[3], 'h': c[4], 'M': c[2], 'D': c[1]}, 10, 1)
    s.g(['LL', 'LD'], {'L': c[3], 'D': c[1]}, 2, 13)
    s.px(5, 11, '#c41a1a'); s.px(6, 10, '#c41a1a')
    return s.render()


def prospector_paxel():
    """the Prospector's Paxel: pick, axe and shovel on one diamond head"""
    s = S()
    _haft(s, WOOD, 3, 14, 9, 8)
    d = ['#0e5a52', '#1a8a7e', '#2ac0b0', '#6aeee0', '#c8fff8']
    s.g(['..LLLLLLL..',
         '.LhLLLLLMMD',
         'LhD....LhMD',
         'LD.....LMD.',
         'L......LD..',
         'D.......D..'], {'L': d[3], 'h': d[4], 'M': d[2], 'D': d[1]}, 4, 1)
    s.g(['SS', 'Ss'], {'S': GLASS[2], 's': GLASS[1]}, 1, 13)
    return s.render()


def grappling_hook():
    s = S()
    r = ['#4a3420', '#6a4c2e', '#8e6a42', '#b08a5a', '#d0aa78']
    for (x, y) in ((2, 14), (3, 13), (3, 12), (2, 11), (2, 10), (3, 9), (4, 8), (5, 9), (6, 10), (7, 10), (8, 9)):
        s.px(x, y, r[3] if (x + y) % 2 else r[2])                                         # a coil of rope
    s.line(8, 9, 11, 6, IRON[2])
    s.g(['L...L', '.L.L.', '..L..', 'LLLLL', '..L..'], {'L': IRON[3]}, 10, 0)
    s.px(10, 0, IRON[4]); s.px(14, 0, IRON[4]); s.px(12, 3, IRON[4])
    return s.render()


def staff(shaft, top):
    """a staff: a two-pixel shaft on the diagonal and its head drawn by `top` at the upper right"""
    def f():
        s = S()
        _haft(s, shaft, 2, 14, 10, 6)
        s.px(1, 15, shaft[1])
        top(s)
        return s.render()
    return f


def top_orb(col, cage=GOLD, r=2.6):
    def t(s):
        s.g(['.C.C.', 'C...C', '.....', 'C...C'], {'C': cage[2]}, 9, 1)
        s.disc(12, 4, r, ramp(col))
        s.px(11, 3, '#ffffff')
    return t


def top_crescent(s):
    s.g(['....YY.', '..YYyY.', '.Yy....', 'Yy.....', 'Yy.....', '.Yy....', '..YYyY.', '....YY.'],
        {'Y': GOLD[3], 'y': GOLD[1]}, 8, 0)
    s.px(13, 4, '#ff7ab8'); s.px(12, 3, '#ffb0d8')


def top_gravewell(s):
    s.disc(12, 4, 3.4, ['#2a0e44', '#4b1d75', '#7432a8', '#a35ad6'])
    s.disc(12.5, 4.5, 1.9, ['#000000', '#08020e', '#120620'])
    s.px(10, 2, '#d6b8ff')


def top_sparks(s):
    s.g(['..W..', '.LLL.', 'LLWLL', '.LLL.', '..L..'], {'W': '#ffffff', 'L': '#a8ecff'}, 10, 1)
    s.px(15, 0, '#5ec3ea'); s.px(9, 0, '#5ec3ea'); s.px(15, 6, '#5ec3ea')


def top_star(col):
    def t(s):
        c = ramp(col)
        s.g(['..L..', '.LhL.', 'LLhLM', '.LMD.', 'L...D'], {'L': c[3], 'h': c[4], 'M': c[2], 'D': c[1]}, 10, 0)
    return t


def top_gem(col, prong=GOLD):
    def t(s):
        c = ramp(col)
        s.g(['P...P', 'PLLMP', '.LhM.', '.LMD.', '..D..'], {'P': prong[3], 'L': c[3], 'h': c[4], 'M': c[2], 'D': c[1]}, 10, 0)
    return t


def levitation_wand():
    s = S()
    _haft(s, ['#14081e', '#2a1440', '#3e2060', '#5a3484', '#7a4aa8'], 3, 13, 11, 5, w=1)
    s.disc(12.5, 3.5, 2.0, ramp('#b080ff'))
    s.px(12, 2, '#ffffff')
    for (x, y) in ((14, 7), (9, 1), (15, 2)): s.px(x, y, '#d8c0ff')
    return s.render()


def treasurers_scepter():
    s = S()
    _haft(s, GOLD, 3, 13, 10, 6)
    s.g(['.YYY.', 'YRRrY', 'YRRRY', '.YYY.'], {'Y': GOLD[4], 'R': '#c41a1a', 'r': '#ff8a7a'}, 10, 1)
    s.g(['.y.y.', '.....'], {'y': GOLD[4]}, 10, 0)
    s.px(2, 14, GOLD[1])
    return s.render()


OVERRIDES = {
    'gilded_chestplate': gilded_chestplate, 'gilded_helmet': gilded_helmet, 'gilded_leggings': gilded_leggings, 'gilded_boots': gilded_boots,
    'rocket_boots': rocket_boots('#e8e8f0', '#ff8a2a'), 'rocket_boots_2': rocket_boots('#7ae8f0', '#3ab0c8'),
    'gravity_boots': lambda: boots('#4a3a6a', '#c8a0ff', ('glow', '#b48cff')).render(),
    'ice_skates': lambda: boots('#7a4a2a', '#f0f0f0', ('blade', '#d8e6f0')).render(),
    'spring_boots': lambda: boots('#2a8a96', '#7ae8f0', ('spring', '#c8ccd2')).render(),
    'triple_boots': lambda: boots('#b8302a', '#ff8a7a', ('glow', '#7dff6a')).render(),
    'water_walking_boots': lambda: boots('#2a5ab8', '#d8f0ff', ('wave', '#9ad8ff')).render(),
    'gauntlet': gauntlet('#8a5a30', '#d8a83a'),
    'gauntlet_hearth': gauntlet(['#1e1210', '#3a2418', '#5a3a26', '#7a5236', '#9a6a46'], '#3a2a24', dots='#ff8a2a'),
    'gauntlet_magma': gauntlet(['#1e1210', '#3a2418', '#5a3a26', '#7a5236', '#9a6a46'], '#ff6a1a', dots='#ffb03a'),
    'gauntlet_obsidian': gauntlet(['#0e0816', '#1e1430', '#2e2248', '#443660', '#5e4e7e'], '#7a4ab8', dots='#ff8a2a'),
    'molten_gauntlet': gauntlet(['#1e1210', '#3a2418', '#5a3a26', '#7a5236', '#9a6a46'], '#2a1a14', glow='#ff7a1a'),
    'climbing_claws': climbing_claws,
    'storm_talon': talon('#ffe85a'), 'talon_chain': talon('#b48cff'), 'talon_static': talon('#7ae8ff'), 'talon_wind': talon('#e8f8ff'),
    'brass_wings': wings(BRASS, vein=BRASS[1]), 'golden_wings': wings(GOLD, vein=GOLD[1]),
    'dragon_wings': wings(['#120618', '#240c30', '#3a1450', '#5a2276', '#7e3aa0'], vein='#a86ad0'),
    'wings_rat_king': wings(['#120a14', '#22142a', '#342040', '#4a3058', '#664a74'], rim=GOLD[3]),
    'star_cloak': star_cloak, 'umbrella': umbrella, 'gilded_grin': gilded_grin, 'gilded_leaf': gilded_leaf,
    'gilded_staff_topper': gilded_staff_topper,
    'enchanted_sword': enchanted_sword, 'gutter_cutlass': gutter_cutlass, 'heisters_shiv': heisters_shiv, 'thirsting_blade': thirsting_blade,
    'demo_scythe': demo_scythe, 'golden_spear': golden_spear, 'quake_maul': quake_maul, 'sepulchre': sepulchre,
    'spawner_crowbar': spawner_crowbar, 'frying_pan': frying_pan, 'tinker_wrench': tinker_wrench, 'prospector_paxel': prospector_paxel,
    'grappling_hook': grappling_hook, 'levitation_wand': levitation_wand, 'treasurers_scepter': treasurers_scepter,
    'crescent_staff': staff(GOLD, top_crescent), 'gravewell_staff': staff(['#100914', '#1e1428', '#3b2a4f', '#5d4880', '#8a72b0'], top_gravewell),
    'staff_of_sparks': staff(COPPER, top_sparks),
    'scepter_phase': staff(BONE, top_gem('#3ad8b0')), 'scepter_rift': staff(BONE, top_gem('#b04aff')), 'scepter_star': staff(BONE, top_star('#ffe85a')),
    'void_scepter': staff(BONE, top_gem('#2ae0c0', prong=PURPLE)),
}

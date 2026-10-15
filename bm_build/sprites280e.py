"""2.80a: the sprite repaint, part five - the strange things: Vorn tech and the skiff's parts, the escort saucers, ray
guns and launchers, the Rat Gang, the summoning items, and the gems, hearts and essences.

    sprites280.post writes these too (OVERRIDES here, merged)."""
import math
from sprites280 import S, GOLD, IRON, BRASS, BONE, RED, GREEN, PURPLE, TEAL, PINK, GLASS, STONE, BLACK, COPPER, WOOD, GHOST, SLIME
from sprites280b import ramp, emboss, _gem_drop_small

VORN = ['#2a2e36', '#444a56', '#646c7a', '#8a94a2', '#b4bcc8']        # the Vorn's gunmetal
XEN = ['#0e5a1e', '#1e8a2e', '#3ac84a', '#7aff6a', '#d8ffc8']         # Vorn green


# ================================================================== VORN TECH AND THE SKIFF'S PARTS
def _screen(s, x0, y0, w, h, body, scr):
    for y in range(h):
        for x in range(w):
            c = body[2]
            if x == 0 or y == 0: c = body[3]
            if x == w - 1 or y == h - 1: c = body[1]
            s.px(x0 + x, y0 + y, c)
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            s.px(x0 + x, y0 + y, scr[1] if (y % 2) else scr[0])


def alarm_jammer():
    s = S()
    s.line(11, 0, 11, 3, IRON[2]); s.px(12, 0, '#ff3a3a')
    _screen(s, 2, 3, 12, 11, ['#1e3a6a', '#2a4e8a', '#3a6aaa', '#5a8ac8'], ['#7ab0ff', '#8ac0ff'])
    s.g(['GG.RR', 'GG.RR'], {'G': '#5aff7a', 'R': '#ff3a3a'}, 5, 5)
    s.g(['KK.KK'], {'K': '#1a2a4a'}, 5, 9)
    s.g(['.KKK.'], {'K': '#1a2a4a'}, 5, 11)
    return s.render()


def signal_jammer():
    s = S()
    s.line(10, 0, 12, 3, BLACK[2]); s.line(12, 0, 12, 2, BLACK[2])
    _screen(s, 2, 4, 12, 9, VORN, ['#5a6474', '#646e80'])
    s.g(['GGG.GGG'], {'G': XEN[3]}, 4, 7); s.px(4, 10, '#ff3a3a'); s.px(5, 10, '#ff3a3a')
    for x in (8, 10, 12): s.px(x, 10, VORN[0])
    return s.render()


def cloaking_device():
    s = S()
    s.disc(8, 7, 6.0, ['#2a6a8a', '#4a9ac0', '#7ad0f0', '#b8f0ff', '#ffffff'])
    s.px(5, 4, '#ffffff'); s.px(6, 3, '#ffffff'); s.px(4, 5, '#e8fbff')
    s.g(['II..II', 'Ii..Ii'], {'I': VORN[3], 'i': VORN[1]}, 5, 12)
    return s.render()


def dimension_shifter():
    s = S()
    for k in range(10):
        a = k * math.pi / 5
        s.disc(8 + 6 * math.cos(a), 8 + 6 * math.sin(a), 1.3, PURPLE[1:])
    s.disc(8, 8, 5.2, PURPLE)
    s.disc(8, 8, 3.2, ['#e8d8ff', '#ffffff'])
    s.disc(8.5, 8.5, 1.6, ['#1a0a30', '#2a0e44'])
    return s.render()


def gravitic_core():
    s = S()
    s.disc(8, 8, 7.0, TEAL)
    s.disc(8, 8, 4.8, ['#0e3a3d', '#17646a', '#249a9e'], light=(0.6, 0.8))
    s.g(['KKKK', 'KCCK', 'KCCK', 'KKKK'], {'K': '#0a2426', 'C': '#a6fff2'}, 6, 6)
    s.px(7, 7, '#ffffff')
    return s.render()


def power_cell():
    s = S()
    s.g(['..TTTT..', '.IIIIII.'], {'T': VORN[3], 'I': VORN[2]}, 4, 1)
    for y in range(3, 14):
        for x in range(4, 12):
            c = XEN[2]
            if x == 4: c = VORN[3]
            elif x == 11: c = VORN[1]
            elif x == 5: c = XEN[4] if y < 12 else XEN[3]
            elif x == 10: c = XEN[1]
            elif (y - 3) % 4 == 3: c = XEN[1]
            s.px(x, y, c)
    s.g(['.IIIIII.'], {'I': VORN[1]}, 4, 14)
    return s.render()


def overcharged_beacon():
    s = S()
    s.g(['.R.', 'RWR', '.R.'], {'R': '#ff3a3a', 'W': '#ffd0c0'}, 7, 0)
    s.line(8, 3, 8, 4, IRON[2])
    s.disc(8, 7.5, 2.8, XEN)
    s.g(['..IIIIII..', '.IiiiiiiI.', 'IIIIIIIIII', 'dddddddddd'], {'I': IRON[3], 'i': IRON[2], 'd': IRON[1]}, 3, 10)
    for (x, y) in ((3, 6), (13, 5), (2, 8), (14, 8)): s.px(x, y, '#ffe85a')
    return s.render()


def tip_alien():
    """the Vorn Signal: a ticking little beacon on a black base, a green light pulsing in its glass"""
    s = S()
    s.g(['..G..', '.GgG.', 'GgWgG'], {'G': XEN[2], 'g': XEN[3], 'W': '#ffffff'}, 6, 0)
    s.g(['.IIII.', 'IggggI', 'IgWWgI', 'IggggI', 'IggggI', '.IIII.'], {'I': VORN[2], 'g': XEN[2], 'W': XEN[4]}, 5, 3)
    s.g(['..BBBBBB..', '.BbbbbbbB.', 'BBBBBBBBBB', 'dddddddddd'], {'B': BLACK[3], 'b': BLACK[2], 'd': BLACK[1]}, 3, 10)
    return s.render()


def skiff_coil():
    s = S()
    for y in range(2, 14):
        for x in range(5, 11):
            ring = (y % 2 == 0)
            s.px(x, y, (XEN[3] if x < 8 else XEN[1]) if ring else (VORN[3] if x < 7 else VORN[1]))
    s.g(['IIIIII'], {'I': VORN[2]}, 5, 1); s.g(['IIIIII'], {'I': VORN[1]}, 5, 14)
    return s.render()


def skiff_core():
    s = S()
    _screen(s, 3, 3, 10, 10, VORN, ['#0e1a14', '#122018'])
    s.g(['G..G', '.GG.', '.GG.', 'G..G'], {'G': XEN[3]}, 6, 6)
    for x in (4, 11): s.px(x, 13, XEN[2]); s.px(x, 14, XEN[1])
    return s.render()


def skiff_dome():
    s = S()
    d = ['#3a8a8a', '#5ab0b0', '#8ad8d8', '#c0f4f4', '#ffffff']
    s.g(['....LLLLLM....', '..LLhLLLLLMM..', '.LhLLLLLLLLMD.', 'LhLLLLLLLLLMMD', 'LLLLLLLLLLLMMD', 'IIIIIIIIIIIIII', 'iiiiiiiiiiiiii'],
        {'L': d[3], 'h': d[4], 'M': d[2], 'D': d[1], 'I': VORN[3], 'i': VORN[1]}, 1, 5)
    return s.render()


def skiff_emitter():
    s = S()
    s.line(2, 13, 10, 5, VORN[3], 2)
    s.line(3, 14, 11, 6, VORN[1])
    s.disc(12, 4, 2.4, XEN)
    s.px(11, 3, '#ffffff')
    for (x, y) in ((15, 1), (14, 7), (9, 1)): s.px(x, y, XEN[3])
    return s.render()


def skiff_hull():
    s = S()
    s.g(['.....LLLLLL.....', '...LLhLLLLLLMM..', '.LLhLLLLLLLLLLMM', 'LhLLGLLLLGLLLLMD', 'MMMMMMMMMMMMMMMD', '.DDDDDDDDDDDDDD.'],
        {'L': VORN[3], 'h': VORN[4], 'M': VORN[2], 'D': VORN[1], 'G': XEN[3]}, 0, 6)
    for x in (3, 7, 11): s.px(x, 12, XEN[2])
    return s.render()


def skiff_key():
    s = S()
    s.g(['..LLLLLLLLM.', '.LhLLLLLLLMD', 'LLLGLLLLGLMD', '.MMMMMMMMMD.'], {'L': VORN[3], 'h': VORN[4], 'M': VORN[2], 'D': VORN[1], 'G': XEN[3]}, 2, 2)
    for y in range(6, 14): s.px(7, y, IRON[3]); s.px(8, y, IRON[1])
    s.g(['II', 'I.', 'II'], {'I': IRON[2]}, 9, 10)
    return s.render()


def skiff_reactor():
    s = S()
    _screen(s, 3, 3, 10, 10, ['#5a1a1a', '#8a2a2a', '#b84040', '#e06060'], ['#3a0a0a', '#4a1010'])
    s.disc(8, 8, 2.8, ['#c41a1a', '#ff6a4a', '#ffc0a0', '#ffffff'])
    for x in (4, 11): s.px(x, 13, VORN[2]); s.px(x, 14, VORN[1])
    return s.render()


ESCORT = {'crimson': '#e83a3a', 'ember': '#ff8a2a', 'gold': '#ffd23f', 'midnight': '#7a5ad8', 'ocean': '#2ac0c8',
          'pearl': '#f0f0f4', 'rose': '#ff7ab8', 'verdant': '#4ad84a'}


def escort(col):
    """an escort saucer: a glass dome, its antenna, a hull with a band of lights in its colour, green tractor legs"""
    def f():
        s = S()
        c = ramp(col)
        s.g(['.Y.', 'YWY', '.Y.'], {'Y': '#ffd23f', 'W': '#fff6c0'}, 7, 0)
        s.px(8, 3, IRON[2])
        s.g(['..GGGG..', '.GgGGGGG', 'GgGGGGGG'], {'G': '#a8e0f0', 'g': '#ffffff'}, 4, 4)
        s.g(['..HHHHHHHHHHHH..', '.HhHHHHHHHHHHHH.', 'CCLCCLCCLCCLCCLC', '.CCCCCCCCCCCCCC.', '..DDDDDDDDDDDD..'],
            {'H': '#d8dee6', 'h': '#ffffff', 'C': c[2], 'L': '#ffffff', 'D': c[0]}, 0, 7)
        s.g(['G..G..G', '.G.G.G.', 'G..G..G'], {'G': XEN[3]}, 4, 12)
        return s.render()
    return f


def vorn_cracking_rig():
    s = S()
    _screen(s, 1, 2, 14, 10, BLACK, ['#1a2a10', '#223214'])
    s.g(['GGGGGGGG', '........', 'G.G.G.G.'], {'G': XEN[3]}, 4, 4)
    s.g(['GGGG'], {'G': XEN[2]}, 4, 8)
    for x in (3, 6, 9, 12): s.px(x, 12, XEN[2]); s.px(x, 13, XEN[1])
    return s.render()


def vorn_drill():
    s = S()
    s.line(2, 13, 7, 8, VORN[3], 3)
    s.line(2, 14, 7, 9, VORN[1])
    for i in range(6):                                       # the bit, spiralled
        x, y = 8 + i, 7 - i
        s.px(x, y, '#ff8a7a' if i % 2 else '#e04a3a'); s.px(x + 1, y, '#a02a1a')
    s.px(14, 1, '#ffd0c0')
    s.g(['GG', 'GG'], {'G': XEN[3]}, 5, 9)
    return s.render()


def drill_bit():
    s = S()
    s.g(['....R....', '...RrR...', '..RrRRR..', '.RRrRRRR.', '..RRrRR..', '...RRR...'], {'R': '#e04a3a', 'r': '#ffb0a0'}, 3, 1)
    s.line(7, 7, 7, 12, VORN[3]); s.line(8, 7, 8, 12, VORN[1])
    s.g(['IIIIII', 'iiiiii'], {'I': VORN[3], 'i': VORN[1]}, 5, 13)
    return s.render()


def ray(tip, body=None):
    """a Vorn ray gun on the diagonal: a grip, a ribbed barrel, an emitter glowing at the tip"""
    def f():
        s = S()
        b = body or IRON
        s.line(2, 13, 4, 11, BLACK[2], 2)                                        # the grip
        s.line(4, 11, 11, 4, b[3], 2)
        s.line(5, 12, 12, 5, b[1])
        for i in (6, 8, 10): s.px(i, 13 - i + 1 - 2, b[4])
        t = ramp(tip)
        s.disc(12.5, 3.5, 2.2, t)
        s.px(12, 3, '#ffffff')
        return s.render()
    return f


def plasma_blaster():
    s = S()
    g = ['#1e2a1e', '#2e3e2e', '#465a46', '#5e765e', '#7e967e']
    s.g(['..........XXX.', '....GGGGGGGXXX', '..GGgGGGGGGGXX', 'GGGGGGGGGGGGG.', 'GGGGGGddddd...', '.GGGGd........', '..GGGd........', '..GGGd........', '..ddd.........'],
        {'G': g[3], 'g': g[4], 'd': g[1], 'X': XEN[3]}, 1, 3)
    s.px(14, 3, XEN[4])
    return s.render()


def fire_charge_launcher():
    s = S()
    s.line(2, 13, 4, 11, WOOD[2], 2)
    s.line(4, 11, 10, 5, BLACK[3], 3)
    s.line(5, 12, 11, 6, BLACK[1])
    s.g(['BB', 'BB'], {'B': BRASS[3]}, 4, 10)
    s.disc(12, 4, 2.6, ['#a02a0a', '#e8641a', '#ffb03a', '#fff0a0'])
    s.px(14, 1, '#ffb03a'); s.px(15, 3, '#ff6a1a')
    return s.render()


def skin_fire_launcher():
    """the launcher's skin: a stencilled card, a flame painted on it, a rolled corner"""
    s = S()
    for y in range(2, 14):
        for x in range(2, 14):
            c = '#f0e0bc'
            if x == 2 or y == 2: c = '#fff6e0'
            if x == 13 or y == 13: c = '#b8986a'
            if x in (3, 12) or y in (3, 12): c = '#8a5a30'
            s.px(x, y, c)
    s.g(['..F...', '.FfF..', '.FffF.', 'FfWfF.', 'FfWWfF', '.FffF.'], {'F': '#e8641a', 'f': '#ffb03a', 'W': '#fff0a0'}, 5, 5)
    s.px(13, 2, None); s.px(12, 2, '#b8986a'); s.px(13, 3, '#8a6e48')
    return s.render()


def pearl_statue():
    """Pearlman's Golden Statue: the penguin in gold, his hat and cane, on a dark plinth"""
    s = S()
    s.g(['....HHH...', '...HHHHH..', '....YYY...', '...YyYYY..', '..YYYYYYY.', '..YyYYYYYc', '..YYYYYYYc', '..YYYYYYY.', '...YYYYY..', '...YY.YY..'],
        {'H': GOLD[1], 'Y': GOLD[3], 'y': GOLD[4], 'c': GOLD[2]}, 3, 1)
    s.px(6, 4, '#2a1804'); s.px(8, 4, '#2a1804'); s.px(7, 5, '#ff9a1a')
    s.g(['BBBBBBBBBB', 'bbbbbbbbbb'], {'B': BLACK[3], 'b': BLACK[1]}, 3, 12)
    return s.render()


# ================================================================== THE RAT GANG
RAT = {'G': '#9a9aa4', 'g': '#73737e', 'L': '#c6c6d0', 'P': '#ff9ab8', 'K': '#111018', 'N': '#ff5a8a', 'd': '#55555f'}


def rat(top, mid, extra=None):
    """a Rat Gang rat, full figure: ears, face, body and tail, then a hat (top) and an outfit (mid)"""
    def f():
        s = S()
        s.g(['.gg......gg.',
             'gPPg....gPPg',
             'gPPgGGGGgPPg',
             '.gGGLLLLGGg.',
             '..GLKLLKLG..',
             '..GLLLLLLG..',
             '...gLNNLg...',
             '...GGGGGG...',
             '..GGLLLLGG..',
             '..GGLLLLGG..',
             '..gGLLLLGg..',
             '...gGGGGg...',
             '...PP..PP...'], RAT, 2, 3)
        s.g(['P', 'P', '.P'], {'P': RAT['P']}, 13, 11)
        mid(s); top(s)
        if extra: extra(s)
        return s.render()
    return f


def _chef_top(s): s.g(['.WWWW.', 'WWWWWW', 'WwwwwW', '.WWWW.'], {'W': '#ffffff', 'w': '#d8d8e0'}, 5, 0)
def _chef_mid(s): s.g(['RRRRRR'], {'R': '#e02a2a'}, 5, 10)
def _lucky_top(s): s.g(['.GGGG.', 'GGgGGG', 'YYYYYY'], {'G': '#3ab84a', 'g': '#7aff6a', 'Y': GOLD[3]}, 5, 1)
def _lucky_mid(s): s.g(['RRRRRR', 'RR..RR', 'RR..RR'], {'R': '#c41a1a'}, 5, 11); s.disc(13, 12, 1.6, GOLD)
def _pirate_top(s): s.g(['..KKKK..', '.KKWKKK.', 'KKKKKKKK'], {'K': '#1a1a22', 'W': '#ffffff'}, 4, 1)
def _pirate_mid(s): s.g(['RRRRRR'], {'R': '#e02a2a'}, 5, 10); s.g(['KKK'], {'K': '#1a1a22'}, 5, 7)
def _prof_top(s): s.g(['.KKKK.', '.KKKK.', 'KKKKKK'], {'K': '#2a2a34'}, 5, 0)
def _prof_mid(s): s.g(['O.O', 'OOO'], {'O': GOLD[2]}, 5, 7); s.g(['O.O'], {'O': GOLD[2]}, 8, 7); s.g(['R.R', '.R.', 'R.R'], {'R': '#e02a2a'}, 6, 10)
def _soldier_top(s): s.g(['.IIII.', 'IiIIII', 'IIIIII'], {'I': IRON[3], 'i': IRON[4]}, 5, 1); s.px(7, 0, '#e02a2a'); s.px(8, 0, '#e02a2a')
def _soldier_mid(s): s.g(['IIII', 'IiII', 'IIII'], {'I': IRON[2], 'i': IRON[3]}, 6, 11); s.disc(3, 12, 2.2, WOOD); s.px(3, 12, GOLD[3])


# ================================================================== SUMMONING ITEMS (the roaming bosses' calls)
def sum_horseman():
    """the Horseman's call: a carved jack-o'-lantern with green fire inside"""
    s = S()
    p = ['#7a3a06', '#b05a0a', '#e08a1a', '#ffb03a', '#ffd88a']
    s.g(['.G', 'GG'], {'G': '#3a8a2a'}, 7, 1)
    s.g(['..LLLLLLLM..', '.LhLLLLLLLMD', 'LhLLLLLLLLMD', 'LLKKLLLLKKMD', 'LLKFLLLLKFMD', 'LLLLLKKLLLMD', 'LLKLKKKKLKMD', 'LLKFKFKFKFMD', '.LLKLKLKLMD.',
         '..MMMMMMMD..'], {'L': p[3], 'h': p[4], 'M': p[2], 'D': p[1], 'K': '#2a1404', 'F': '#7aff5a'}, 2, 3)
    return s.render()


def sum_lantern():
    """the Arachno-Lantern's call: a dormant pumpkin on spider legs, red crescent eyes"""
    s = S()
    p = ['#3a1404', '#6a2a08', '#9a4410', '#c86a1a', '#e8902a']
    s.g(['.G', 'GG'], {'G': '#2a5a1a'}, 7, 1)
    s.disc(8, 7, 5.0, p)
    s.g(['RR...RR', '.R...R.'], {'R': '#ff2a2a'}, 4, 6)
    s.g(['KFKFKFK'], {'K': '#1a0804', 'F': '#ff8a1a'}, 4, 9)
    for (x0, y0, x1, y1) in ((4, 10, 1, 14), (6, 11, 4, 15), (12, 10, 15, 14), (10, 11, 12, 15)):
        s.line(x0, y0, x1, y1, '#1a0804')
    return s.render()


def sum_pharaoh():
    """the Pharaoh's call: a lapis-and-gold scarab"""
    s = S()
    b = ['#0e2a6a', '#1a44a0', '#2a62d0', '#5a8af0', '#a0c0ff']
    s.g(['....YYYY....', '...YyYYYY...', '..LLLLLLLL..', '.LhLLLLLLLM.', '.LhLLDLLLLM.', '.LLLLDLLLLM.', '.LLLLDLLLMM.', '..LLLDLLLM..', '...MMMMMM...'],
        {'Y': GOLD[3], 'y': GOLD[4], 'L': b[2], 'h': b[4], 'D': b[0], 'M': b[1]}, 2, 2)
    for (x0, y0, x1, y1) in ((3, 6, 0, 5), (3, 9, 0, 10), (12, 6, 15, 5), (12, 9, 15, 10), (5, 11, 3, 14), (10, 11, 12, 14)):
        s.line(x0, y0, x1, y1, '#2a1804')
    return s.render()


def sum_roc():
    """the Roc's call: a long storm-blue feather with a gold quill"""
    s = S()
    v = ['#0e2244', '#1a3a6e', '#2a5aa0', '#5a8ad0', '#a8c8ff']
    for i in range(10):
        x, y = 3 + i, 12 - i
        s.px(x, y, v[3]); s.px(x + 1, y, v[2]); s.px(x, y - 1, v[4] if i % 3 else '#ffffff'); s.px(x + 1, y + 1, v[1])
    s.line(2, 14, 12, 4, GOLD[2])
    s.px(1, 15, GOLD[1])
    for (x, y) in ((8, 6), (11, 3)): s.px(x, y, '#ffe85a')
    return s.render()


def sum_treant():
    """the Treant's call: a great acorn, its cap scaled, a leaf on its stem"""
    s = S()
    c = WOOD
    s.g(['......S.', '.....SLL', '..CCCCCC', '.CcCCcCCC', 'CCCcCCCcCC', 'DDDDDDDDDD'], {'S': c[1], 'L': '#5aa83a', 'C': c[2], 'c': c[3], 'D': c[1]}, 3, 1)
    n = ['#6a4a1a', '#9a7030', '#c89a4a', '#e8c070', '#fff0b8']
    s.g(['.NNNNNNNN.', '.NhNNNNNM.', '.NhNNNNNM.', '..NNNNNM..', '..NNNNMM..', '...NNMM...', '....MM....'], {'N': n[3], 'h': n[4], 'M': n[1]}, 3, 7)
    return s.render()


def sum_colossus():
    """the Colossus's call: a magma idol, cracked and glowing"""
    s = S()
    k = ['#140a10', '#24141c', '#3a222e', '#523446', '#6e4a60']
    s.g(['...KKKK...', '..KkKKKK..', '..KEKKEK..', '..KKKKKK..', '.KKKKKKKK.', 'KkKKKKKKKK', 'KKKKKKKKKK', 'KKKKKKKKKK', '.KKKKKKKK.', 'DDDDDDDDDD'],
        {'K': k[2], 'k': k[3], 'E': '#ffb03a', 'D': k[0]}, 3, 2)
    for (x, y) in ((6, 7), (7, 8), (8, 8), (9, 9), (7, 10), (10, 7), (5, 10)): s.px(x, y, '#ff6a1a')
    s.px(8, 9, '#ffd060')
    return s.render()


def sum_voidwalker():
    """the Voidwalker's call: a violet eye in the dark"""
    s = S()
    s.g(['....PPPPPP....', '..PPpppppPPP..', '.PpWWWWWWWWpP.', 'PpWWWVVVVWWWpP', 'PpWWVVKKVVWWpP', 'PpWWWVVVVWWWpP', '.PpWWWWWWWWpP.', '..PPpppppPPP..', '....PPPPPP....'],
        {'P': PURPLE[2], 'p': PURPLE[1], 'W': '#1a0a2a', 'V': PURPLE[3], 'K': '#000000'}, 1, 3)
    s.px(7, 6, '#ffffff')
    return s.render()


# ================================================================== GEMS, HEARTS AND ESSENCES
def crystal_shard(col, diag=False):
    def f():
        s = S()
        c = ramp(col)
        if diag:
            for i in range(9):
                x, y = 3 + i, 12 - i
                s.px(x, y, c[3]); s.px(x + 1, y, c[2]); s.px(x + 1, y + 1, c[1]); s.px(x, y - 1, c[4] if i % 3 == 0 else c[3])
            s.px(12, 2, c[4]); s.px(2, 13, c[1])
        else:
            s.g(['....L....', '...LhM...', '...LhM...', '..LLhMD..', '..LhLMD..', '.LLhLMMD.', '.LhLLMMD.', '.LLLLMMD.', '..LLLMD..', '..LLMMD..', '...LMD...', '....D....'],
                {'L': c[3], 'h': c[4], 'M': c[2], 'D': c[1]}, 3, 2)
        return s.render()
    return f


def blood_crystal():
    s = S()
    c = ['#3a0608', '#6a0e12', '#a01a1e', '#d03a32', '#ff7a6a']
    s.g(['......LLLM', '.....LhLMD', '....LhLMD.', '...LhLMD..', '..LhLMD...', '.LLLMD....', 'LLLMD.....', 'LMMD......', 'MDD.......'],
        {'L': c[2], 'h': c[4], 'M': c[1], 'D': c[0]}, 3, 3)
    for (x, y) in ((9, 4), (7, 6), (5, 8)): s.px(x, y, c[3])
    return s.render()


def ember_scale():
    s = S()
    e = ['#6a1a04', '#b03a0a', '#e8641a', '#ffa83a', '#fff0a0']
    s.g(['...LLM...', '..LhLMM..', '.LhLLLMD.', 'LhLWLLMMD', 'LLLLLLMMD', '.LLLLMMD.', '..LLMMD..', '...LMD...', '....D....'],
        {'L': e[2], 'h': e[3], 'W': e[4], 'M': e[1], 'D': e[0]}, 3, 3)
    for (x, y) in ((6, 7), (8, 9), (9, 6)): s.px(x, y, e[1])
    return s.render()


def bloomheart_gem():
    """the Bloomheart: a pink flower whose heart is a yellow gem"""
    s = S()
    p = ramp('#ff7ac8')
    for k in range(5):
        a = -math.pi / 2 + k * 2 * math.pi / 5
        s.disc(8 + 4.0 * math.cos(a), 8 + 4.0 * math.sin(a), 2.7, p)
    s.disc(8, 8, 2.4, ramp('#ffe14a'))
    s.px(7, 7, '#ffffff')
    return s.render()


def kw_spark():
    """KillerWatt's spark: a green crackling diamond with sparks off it"""
    s = S()
    g = ramp('#5aff5a')
    s.g(['.....L.....', '....LhM....', '...LhWMM...', '..LhWWWMD..', '.LhWWWWWMD.', 'LLWWWWWWMMD', '.LMWWWWWMD.', '..LMWWWMD..', '...LMWMD...', '....LMD....', '.....D.....'],
        {'L': g[3], 'h': g[4], 'W': '#e8ffe0', 'M': g[2], 'D': g[1]}, 2, 2)
    for (x, y) in ((1, 2), (14, 3), (0, 12), (15, 12), (13, 14)): s.px(x, y, g[3])
    return s.render()


HEART = ['.LL...LM.',
         'LhhL.LLMM',
         'LhLLLLLMD',
         'LLLLLLMMD',
         '.LLLLLMD.',
         '..LLLMD..',
         '...LMD...',
         '....D....']


def heart(col, extra=None, big=True):
    def f():
        s = S()
        c = ramp(col) if isinstance(col, str) else col
        rows = HEART
        if big:
            rows = ['.LLL...LLM.',
                    'LhhLL.LLLMM',
                    'LhLLLLLLLMD',
                    'LhLLLLLLLMD',
                    'LLLLLLLLMMD',
                    '.LLLLLLLMD.',
                    '..LLLLLMD..',
                    '...LLLMD...',
                    '....LMD....',
                    '.....D.....']
        s.g(rows, {'L': c[3], 'h': c[4], 'M': c[2], 'D': c[1]}, 2, 3)
        if extra: extra(s)
        return s.render()
    return f


def _forge_x(s):
    for (x, y) in ((6, 7), (7, 8), (9, 7), (8, 9), (10, 6)): s.px(x, y, '#ffe08a')


def _scorch_x(s):
    s.g(['.Y.', 'YWY', '.Y.'], {'Y': '#ffd060', 'W': '#ffffff'}, 6, 6)
    for (x, y) in ((3, 1), (13, 1), (8, 0)): s.px(x, y, '#ff8a1a')


def _wraith_x(s):
    s.g(['.W.', 'WwW', '.W.'], {'W': '#e8ffff', 'w': '#ffffff'}, 6, 6)
    for (x, y) in ((3, 1), (13, 1), (8, 0)): s.px(x, y, '#8af0ff')


def _ravenous_x(s):
    s.g(['KKKKK', 'KWKWK', 'KKKKK', 'KWKWK', '.KKK.'], {'K': '#2a0408', 'W': '#ffffff'}, 5, 6)


def hoard_ember():
    s = S()
    s.g(['....R....', '...RYR...', '..RYWYR..', '.RYWWWYR.', '.RYWWWYR.'], {'R': '#e8641a', 'Y': '#ffb03a', 'W': '#fff0a0'}, 3, 3)
    s.g(['.CCCCCCC.', 'CcCCCCCCC', 'CCCCCCCCC', '.DDDDDDD.'], {'C': '#3a2a2a', 'c': '#5a4444', 'D': '#1a1010'}, 3, 8)
    for (x, y) in ((5, 9), (8, 10), (10, 9)): s.px(x, y, '#ff6a1a')
    return s.render()


def essence(col):
    """a boss's essence: a glowing orb with a spiked halo, a wisp rising from it"""
    def f():
        s = S()
        c = ramp(col)
        for k in range(8):
            a = k * math.pi / 4 + math.pi / 8
            x, y = 8 + 6.2 * math.cos(a), 9 + 6.2 * math.sin(a)
            s.px(int(x), int(y), c[3])
        s.disc(8, 9, 4.6, c)
        s.disc(7, 8, 1.8, [c[4], '#ffffff'])
        s.g(['.W', 'W.', '.W'], {'W': c[4]}, 7, 1)
        return s.render()
    return f


def hollow_summons():
    """the Shard of the Hollow Throne: a jagged slate-grey shard, pale light along its edge"""
    s = S()
    c = ['#1e242e', '#3d4b5c', '#5a6a80', '#8a9ab0', '#c8d4e4']
    s.g(['........LL', '.......LhM', '......LhMD', '.....LhMD.', '....LLMD..', '...LhMD...', '..LhMMD...', '.LLMD.....', 'LMMD......', 'MDD.......'],
        {'L': c[2], 'h': c[4], 'M': c[1], 'D': c[0]}, 3, 3)
    return s.render()


def void_shard():
    return crystal_shard('#a070ff', diag=True)()


def _feather(s, x0, y0, x1, y1, vane, rib):
    """a feather from its quill (x0, y0) to its tip (x1, y1): a vane either side of a dark rib, lit on one side"""
    n = max(abs(x1 - x0), abs(y1 - y0))
    for i in range(n + 1):
        t = i / n
        x = round(x0 + (x1 - x0) * t); y = round(y0 + (y1 - y0) * t)
        w = 0 if i < 2 else (1 if i > n - 2 else 1)
        for dx in range(-w, w + 1):
            if dx: s.px(x + dx, y, vane[3] if dx < 0 else vane[1])
        s.px(x, y, rib if i < n else vane[3])


def fletchers_charm():
    """three goose feathers fanned out, bound with gold wire at their quills"""
    s = S()
    V = ['#8a8478', '#c0bab0', '#e8e4dc', '#ffffff']
    _feather(s, 7, 12, 2, 2, V, '#8a8478')
    _feather(s, 8, 12, 8, 1, V, '#8a8478')
    _feather(s, 9, 12, 14, 2, V, '#8a8478')
    s.g(['YYYY', 'yyyy'], {'Y': GOLD[3], 'y': GOLD[1]}, 6, 11)
    s.px(7, 13, '#6a5a44'); s.px(8, 14, '#6a5a44'); s.px(9, 13, '#6a5a44')
    return s.render()


def grave_charm():
    """the Grave Charm: a little tombstone on a ring, a cross carved in it"""
    s = S()
    s.g(['.YY.', 'Y..Y', '.YY.'], {'Y': GOLD[2]}, 6, 0)
    st = ['#4a525c', '#6a747e', '#8a949e', '#b0b8c2', '#d4dae2']
    s.g(['..LLLLLM..', '.LhLLLLLM.', 'LhLLLLLLMD', 'LhLLKLLLMD', 'LLLKKKLLMD', 'LLLLKLLLMD', 'LLLLKLLLMD', 'LLLLLLLLMD', 'LLLLLLLMMD', 'MMMMMMMMMD'],
        {'L': st[3], 'h': st[4], 'M': st[2], 'D': st[1], 'K': st[0]}, 3, 4)
    return s.render()


def blue_marlin():
    """the Blue Marlin, leaping on the diagonal: a forked tail low left, its sail fin up, a long bill to the upper right"""
    s = S()
    b = ['#0a1e44', '#14346e', '#1e52a0', '#3a7ad0', '#7ab0f0']
    for i in range(8):                                       # the body: a dark-blue back over a silver belly
        x, y = 3 + i, 12 - i
        s.px(x, y - 1, b[2]); s.px(x, y, b[3]); s.px(x + 1, y, b[2]); s.px(x + 1, y + 1, '#d8e4f0'); s.px(x + 2, y + 1, '#b8c8dc')
    for i in range(5):                                       # the sail fin along the back
        s.px(4 + i, 9 - i - 1, b[1]); s.px(4 + i, 9 - i - 2, b[2]) if i < 4 else None
    s.px(10, 5, b[4]); s.px(10, 4, b[3])
    s.px(11, 5, '#ffffff'); s.px(12, 5, b[2])
    s.line(12, 4, 15, 1, '#24344e')                          # the bill
    s.g(['T.', 'TT', '.T', 'TT', 'T.'], {'T': b[1]}, 1, 11)  # the forked tail
    s.px(11, 6, b[1])
    return s.render()


OVERRIDES = {
    'alarm_jammer': alarm_jammer, 'signal_jammer': signal_jammer, 'cloaking_device': cloaking_device, 'dimension_shifter': dimension_shifter,
    'gravitic_core': gravitic_core, 'power_cell': power_cell, 'overcharged_beacon': overcharged_beacon, 'tip_alien': tip_alien,
    'skiff_coil': skiff_coil, 'skiff_core': skiff_core, 'skiff_dome': skiff_dome, 'skiff_emitter': skiff_emitter, 'skiff_hull': skiff_hull,
    'skiff_key': skiff_key, 'skiff_reactor': skiff_reactor, 'vorn_cracking_rig': vorn_cracking_rig, 'vorn_drill': vorn_drill,
    'drill_bit': drill_bit, 'ray_gun': ray('#5aff5a'), 'growth_ray': ray('#ff7a6a'), 'shrink_ray': ray('#ffb0c8'), 'tractor_beam': ray('#d08aff'),
    'plasma_blaster': plasma_blaster, 'fire_charge_launcher': fire_charge_launcher, 'skin_fire_launcher': skin_fire_launcher,
    'pearl_statue': pearl_statue,
    'rat_chef': rat(_chef_top, _chef_mid), 'rat_lucky': rat(_lucky_top, _lucky_mid), 'rat_pirate': rat(_pirate_top, _pirate_mid),
    'rat_prof': rat(_prof_top, _prof_mid), 'rat_soldier': rat(_soldier_top, _soldier_mid),
    'sum_horseman': sum_horseman, 'sum_lantern': sum_lantern, 'sum_pharaoh': sum_pharaoh, 'sum_roc': sum_roc, 'sum_treant': sum_treant,
    'sum_colossus': sum_colossus, 'sum_voidwalker': sum_voidwalker,
    'blood_crystal': blood_crystal, 'ember_scale': ember_scale, 'bloomheart_gem': bloomheart_gem, 'kw_spark': kw_spark, 'void_shard': void_shard,
    'xenite_cyan': crystal_shard('#5ae8f0'), 'xenite_green': crystal_shard('#5aff7a'), 'xenite_red': crystal_shard('#ff4a4a'),
    'xenite_violet': crystal_shard('#b47aff'),
    'heartstone': heart(['#5a0612', '#9a1028', '#d82040', '#ff5a6a', '#ffa8b0']), 'forgeheart': heart(['#4a1004', '#8a2a08', '#d0541a', '#ff8a3a', '#ffc070'], _forge_x),
    'scorching_heart': heart(['#5a0804', '#b0200a', '#f0501a', '#ffa030', '#ffe080'], _scorch_x),
    'wraithfire_heart': heart(['#0a4050', '#14809a', '#2ac8e8', '#8af0ff', '#e8ffff'], _wraith_x),
    'ravenous_heart': heart(['#3a0408', '#6a0a14', '#a01424', '#d0303a', '#ff7a7a'], _ravenous_x), 'hoard_ember': hoard_ember,
    'essence_colossus': essence('#ff6a1a'), 'essence_horseman': essence('#ff8a2a'), 'essence_pharaoh': essence('#ffd23f'),
    'essence_roc': essence('#5a9aff'), 'essence_treant': essence('#6ac83a'), 'essence_voidwalker': essence('#a86aff'),
    'hollow_summons': hollow_summons, 'fletchers_charm': fletchers_charm, 'grave_charm': grave_charm, 'blue_marlin': blue_marlin,
}
OVERRIDES.update({f'skiff_escort_{k}': escort(c) for k, c in ESCORT.items()})

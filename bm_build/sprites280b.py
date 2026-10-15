"""2.80a: the sprite repaint, part two - keys, charms, coins, sigils, emblems, rosettes, laurels and trophies.

Every icon the 2.80 pass hadn't reached is drawn again in its style (sprites280's kit: bold shapes filling the frame, a
dark outline, 4-5 step shading, highlights). This module holds the jewellery and the keys - families that share a body
and differ in colour or in a small motif, so each family is one drawing with its variants as data.

    sprites280.post writes these too (OVERRIDES here, merged)."""
import colorsys
from sprites280 import S, hx, GOLD, IRON, BRASS, BONE, RED, GREEN, PURPLE, TEAL, PINK, GLASS, STONE, BLACK, COPPER, SLIME, GHOST, WOOD


def _hls(h):
    r, g, b, _ = hx(h)
    return colorsys.rgb_to_hls(r / 255, g / 255, b / 255)


def _hex(hh, ll, ss):
    r, g, b = colorsys.hls_to_rgb(hh % 1.0, max(0.0, min(1.0, ll)), max(0.0, min(1.0, ss)))
    return '#%02x%02x%02x' % (round(r * 255), round(g * 255), round(b * 255))


def ramp(base, n=5):
    """dark -> light around a base colour (it sits in the middle): shadows cooler and richer, lights warmer and paler"""
    hh, ll, ss = _hls(base)
    out = []
    for i in range(n):
        t = (i - (n - 1) / 2) / ((n - 1) / 2)              # -1 .. +1
        l2 = ll + t * (0.30 if t > 0 else 0.26) * (1.15 - abs(ll - 0.5))
        h2 = hh + (-0.025 if t < 0 else 0.018) * abs(t)
        s2 = ss * (1.0 + (0.08 if t < 0 else -0.22) * abs(t))
        out.append(_hex(h2, l2, s2))
    return out


# ================================================================== KEYS
# (the dungeon, vault and boss keys and the world's other keys keep their vanilla trial-key look - only the Rat King's is drawn)
def rat_king_key():
    """a gold key with a crowned rat's head for its bow"""
    s = S()
    s.g(['.Y.Y.Y.', '.YYYYY.', 'GyyyyyG'], {'Y': GOLD[3], 'y': GOLD[2], 'G': GOLD[1]}, 1, 0)
    s.disc(4.5, 6.0, 3.6, GOLD[:5])
    s.g(['E..E'], {'E': '#ff3a3a'}, 3, 5); s.px(4, 7, '#ff9ab0'); s.px(5, 7, '#ff9ab0')        # its eyes, its nose
    s.px(1, 4, GOLD[2]); s.px(8, 4, GOLD[1])                                                    # its ears
    s.line(7, 8, 13, 14, GOLD[3], 2)
    s.line(8, 9, 14, 15, GOLD[1])
    s.g(['.YY', 'Y.y', '.y.'], {'Y': GOLD[3], 'y': GOLD[1]}, 10, 13)
    s.g(['Y.', 'YY'], {'Y': GOLD[2]}, 12, 10)
    return s.render()


# ================================================================== CHARMS (the cosmetic pendants)
# a chain from the top corners to a bail, and the charm hanging from it: its own little motif in a bezel.
# The night charms' chains go dark / silver / gold by rarity, like their glints.
CHAIN = {1: ['#2a2a34', '#4a4a58'], 2: IRON[1:3], 3: GOLD[1:3]}


def _chain(s, tier=2, bail=(7, 4)):
    c0, c1 = CHAIN[tier]
    bx, by = bail
    for i, (x, y) in enumerate([(3, 0), (3, 1), (4, 2), (5, 3), (6, 4)]):
        s.px(x, y, c1 if i % 2 else c0)
    for i, (x, y) in enumerate([(12, 0), (12, 1), (11, 2), (10, 3), (9, 4)]):
        s.px(x, y, c0 if i % 2 else c1)
    s.g(['.MM.', 'MLLM', '.MM.'], {'M': c0, 'L': c1}, bx - 1 + 0, by)


def _gem_drop(s, col, top=6):
    r = ramp(col)
    s.g(['...MM...',
         '..MLLM..',
         '.MLhLMM.',
         'MLhLLMMD',
         'MLLLMMMD',
         'MMLMMMDD',
         '.MMMMDD.',
         '..MDDD..',
         '...DD...'], {'M': r[2], 'L': r[3], 'h': r[4], 'D': r[1]}, 4, top)


def charm(motif, tier=2):
    def f():
        s = S()
        _chain(s, tier)
        motif(s)
        return s.render()
    return f


def _bezel(s, metal, inner, cx=7.5, cy=10.5, r=4.4):
    s.disc(cx, cy, r, metal)
    s.disc(cx, cy, r - 1.3, inner)


def m_crimson_drip(s):
    _gem_drop(s, '#c81e1e')
    s.px(6, 15 - 0, None)
    s.px(12, 13, RED[2]); s.px(12, 14, RED[1])           # a drop falling away


def m_bloodbat(s):
    s.g(['W.......W',
         'WW.B.B.WW',
         'WwWBBBWwW',
         'WwwBEBwwW',
         '.wwBBBww.',
         '..w.B.w..'], {'W': '#5a0a14', 'w': '#8a1420', 'B': '#2a0408', 'E': '#ff3a3a'}, 3, 7)
    s.px(7, 9, '#ff3a3a'); s.px(9, 9, '#ff3a3a'); s.px(8, 9, '#2a0408')


def m_blood_halo(s):
    s.ring(8, 7.6, 5.4, 1.9, 1.0, ['#6a0a10', '#a01818', '#e03030', '#ff7060', '#ffc0b0'])
    s.px(7, 6, '#ffd0c0')
    _gem_drop_small(s, '#ff2a2a', 6, 10)
    s.px(7, 9, '#a01818'); s.px(8, 9, '#a01818')


def _gem_drop_small(s, col, x0, y0):
    r = ramp(col)
    s.g(['.ML.', 'MLhM', 'MLMD', '.MD.'], {'M': r[2], 'L': r[3], 'h': r[4], 'D': r[1]}, x0, y0)


def m_clover(s):
    g = GREEN
    s.disc(5.7, 9.3, 2.3, g); s.disc(10.3, 9.3, 2.3, g); s.disc(8, 12.6, 2.3, g)
    s.px(8, 10, g[4]); s.px(8, 11, g[1]); s.px(8, 14, g[0]); s.px(9, 15, g[0])


def m_gold_rush(s):
    for i, y in enumerate((13, 11, 9)):                       # a stack of coins, and one on its edge
        s.g(['.yYYYy.', 'dyyyyyd'], {'Y': GOLD[4], 'y': GOLD[3], 'd': GOLD[1]}, 3, y - 1)
    s.g(['.YY.', 'YyyM', 'YyyM', '.MM.'], {'Y': GOLD[4], 'y': GOLD[3], 'M': GOLD[1]}, 10, 9)
    s.px(4, 8, '#fff6c0'); s.px(12, 8, '#ffffff')


def m_jackpot_crown(s):
    s.g(['Y..Y..Y..',
         'YY.YY.YY.',
         'YYyYYyYYy',
         'yRyyGyyRy',
         'yyyyyyyyy',
         'ddddddddd'], {'Y': GOLD[3], 'y': GOLD[2], 'd': GOLD[1], 'R': '#ff3a3a', 'G': '#3aff6a'}, 3, 7)
    s.px(3, 7, '#fff6c0'); s.px(9, 7, '#fff6c0')


def m_xenite_glow(s):
    g = ramp('#5aff7a')
    s.g(['..L..',
         '.LhM.',
         '.LhM.',
         'LLhMD',
         'LLMMD',
         '.LMD.',
         '..D..'], {'L': g[3], 'h': g[4], 'M': g[2], 'D': g[1]}, 5, 7)
    s.px(4, 9, '#d8ffe0'); s.px(11, 12, '#d8ffe0')


def m_tractor_beam(s):
    b = ramp('#7affd8')
    s.g(['.IIIII.', 'IiIIIiI', '.iiiii.'], {'I': IRON[3], 'i': IRON[1]}, 4, 6)
    s.px(5, 7, '#7affd8'); s.px(7, 7, '#7affd8'); s.px(9, 7, '#7affd8')
    for y in range(9, 15):
        w = (y - 9) // 2
        for x in range(7 - w, 9 + w + 1 - 1):
            s.px(x, y, b[3] if x in (7, 8) else b[2])
    s.px(7, 14, b[4])


def m_saucer_orbit(s):
    s.ring(8, 10.5, 6.2, 2.2, 1, ['#3a6a2a', '#6ac040', '#b0ff5a', '#e0ffb0'])
    s.g(['..GG..', '.GggG.', 'IIIIII', 'iIiIii'], {'G': '#b8f0ff', 'g': '#5ab0d0', 'I': IRON[3], 'i': IRON[1]}, 5, 8)
    s.px(7, 9, '#ffffff')


def m_starlit(s):
    st = ramp('#b8c8ff')
    s.g(['....L....',
         '...LhM...',
         'LLLLhMMMD',
         '.LLhhMMD.',
         '..LhMMD..',
         '.LLM.MMD.',
         '.LD...MD.'], {'L': st[3], 'h': st[4], 'M': st[2], 'D': st[1]}, 3, 7)
    s.px(2, 6, '#ffffff'); s.px(13, 9, '#ffffff'); s.px(12, 14, '#d8e0ff')


def m_glimmer(s):
    _bezel(s, IRON, ramp('#1a5a52'))
    for (x, y, c) in ((6, 9, '#a6fff2'), (9, 11, '#7affd8'), (7, 12, '#48cfc8'), (9, 8, '#ffffff'), (5, 11, '#7affd8')):
        s.px(x, y, c)


def m_bloom(s):
    p = ramp('#9aff5a')
    s.disc(8, 8.7, 1.8, p); s.disc(5.6, 11, 1.8, p); s.disc(10.4, 11, 1.8, p); s.disc(8, 13, 1.8, p)
    s.disc(8, 11, 1.3, ramp('#ffe14a'))


def m_void(s):
    _bezel(s, PURPLE, ['#08020e', '#12061e', '#1e0a30', '#2a0e44'])
    s.px(7, 10, '#d8a8ff'); s.px(8, 11, '#9a5aff'); s.px(6, 12, '#7432a8'); s.px(9, 9, '#7432a8')


def m_ashen(s):
    a = ['#4a4442', '#6e6764', '#958e8a', '#c0bab4', '#e8e2dc']
    s.disc(8, 10.8, 3.8, a)
    s.px(7, 10, '#ff8a3a'); s.px(8, 11, '#c84a10'); s.px(9, 10, '#ffb070')    # a coal still glowing in it
    s.px(3, 7, '#d8d0c8'); s.px(13, 9, '#a8a09a'); s.px(12, 14, '#d8d0c8')


def m_cinder(s):
    _flame(s, ['#5a1404', '#a8300a', '#e8641a', '#ffa83a', '#fff0a0'])


def m_ember(s):
    _flame(s, ['#6a1a04', '#c43a0a', '#ff6a1a', '#ffb050', '#fff6c0'])
    s.px(3, 9, '#ffb050'); s.px(12, 8, '#ff6a1a')


def m_soul(s):
    _flame(s, ['#0a3a44', '#14707e', '#3ac0d0', '#8af0f8', '#e8ffff'])


def _flame(s, f):
    s.g(['...L.....',
         '...LL....',
         '..LhL.M..',
         '..LhLMM..',
         '.LhhLLMD.',
         '.LhWhLMD.',
         'LLhWWhMDD',
         'LLhhhLMMD',
         '.LLLLMMD.'], {'L': f[2], 'h': f[3], 'W': f[4], 'M': f[1], 'D': f[0]}, 3, 6)


def m_frost(s):
    c = ramp('#a8e8ff')
    s.g(['...W...',
         '.W.W.W.',
         '..LWL..',
         'WWWhWWW',
         '..LWL..',
         '.W.W.W.',
         '...W...'], {'W': c[3], 'L': c[2], 'h': '#ffffff'}, 4, 7)


def m_petal(s):
    p = ramp('#ff9ad0')
    s.g(['..LL.LL..',
         '.LhLLLhL.',
         '.LLLYLLM.',
         '..LYyYM..',
         '.LLLYLLM.',
         '.LLM.MMD.',
         '..M...D..'], {'L': p[3], 'h': p[4], 'M': p[2], 'D': p[1], 'Y': '#ffe14a', 'y': '#ff9a1a'}, 3, 7)


def m_gilded(s):
    _gem_drop(s, '#ffd23f')
    s.px(3, 7, '#fff6c0'); s.px(12, 10, '#fff6c0'); s.px(11, 6, '#ffe890')


def m_heart(s):
    h = ramp('#ff3a5a')
    s.g(['.LL..LM.',
         'LhhLLLMM',
         'LhLLLLMD',
         'LLLLLMMD',
         '.LLLMMD.',
         '..LMMD..',
         '...MD...'], {'L': h[3], 'h': h[4], 'M': h[2], 'D': h[1]}, 4, 7)


def m_rainbow(s):
    for i, col in enumerate(['#ff3b3b', '#ff8a1a', '#ffe14a', '#4ade5a', '#3ab4ff', '#7a5aff']):
        s.ring(8, 12.0, 7.4 - i, 7.4 - i, 1.0, [ramp(col)[2], col, ramp(col)[3]])
    for x in range(16):
        for y in range(12, 16): s.px(x, y, None)
    cloud = ['#a8b4c4', '#d0d8e4', '#eef2f8', '#ffffff']
    for cx in (2.6, 13.4):
        s.disc(cx, 11.6, 2.0, cloud); s.disc(cx - 1.2, 12.6, 1.5, cloud); s.disc(cx + 1.2, 12.6, 1.5, cloud)


def charm_rainbow():
    s = S()
    m_rainbow(s)
    return s.render()


def charm_storm():
    """the storm charm: a thundercloud with its bolt"""
    s = S()
    c = ['#2a2e3e', '#4a5068', '#727a94', '#a2a8be', '#d0d4e2']
    s.disc(5, 6.5, 3.2, c); s.disc(10, 5.5, 4.0, c); s.disc(8, 8.2, 3.4, c); s.disc(12.5, 8, 2.4, c)
    s.g(['..YY', '.YY.', 'YYYY', '..Y.', '.Y..', 'Y...'], {'Y': '#ffe85a'}, 6, 9)
    s.px(8, 9, '#fff6b0'); s.px(3, 12, '#5a8aff'); s.px(4, 14, '#5a8aff'); s.px(12, 12, '#5a8aff'); s.px(11, 14, '#5a8aff')
    return s.render()


def charm_eclipse():
    """the Blood Eclipse: a black sun in a ring of blood light"""
    s = S()
    s.disc(8, 8, 7.0, ['#4e0606', '#8a0e10', '#c41a1a', '#ff4a3a', '#ffa080'])
    s.disc(8.6, 8.6, 5.2, ['#000000', '#08020a', '#140810', '#1e0c16'])
    s.px(5, 5, '#ffd0c0'); s.px(4, 6, '#ff8a6a')
    return s.render()


def _wings(feather, lite, dark, core):
    s = S()
    rows = ['L.............L.',
            'LL...........LL.',
            'LWL.........LWL.',
            'LWWL.......LWWL.',
            'LWWWL.....LWWWL.',
            '.LWWWL.c.LWWWL..',
            '.LWWWWLcLWWWWL..',
            '..LWWWWcWWWWL...',
            '..LWWWwcwWWWL...',
            '...LWWw.wWWL....',
            '...LWw...wWL....',
            '....Lw...wL.....',
            '.....w...w......']
    s.g(rows, {'L': dark, 'W': feather, 'w': lite, 'c': core}, 1, 1)
    for (x, y) in ((3, 4), (4, 5), (5, 6), (12, 4), (11, 5), (10, 6)):
        s.px(x, y, lite)
    return s.render()


def charm_wings_angel(): return _wings('#fff6e0', '#ffffff', '#d8b860', '#ffd23f')
def charm_wings_evil():  return _wings('#3a0a14', '#c83a10', '#14040a', '#ff6a1a')


def xp_charm():
    s = S()
    _chain(s, 1)
    g = ramp('#7cff4a')
    s.disc(8, 10.5, 4.2, g)
    s.g(['.W.', 'WWW', '.W.'], {'W': '#f4ffb0'}, 6, 9)
    s.px(10, 12, g[0]); s.px(9, 13, g[1])
    return s.render()


def celi_charm():
    """Celi's Moon Charm: a midnight-blue moonstone in a gold frame with a pale crescent"""
    s = S()
    _chain(s, 3)
    _bezel(s, GOLD, ['#0a1440', '#14246a', '#1e3a9a', '#3a5ac8'], r=4.8)
    s.g(['.WW.', 'W...', 'W...', '.WW.'], {'W': '#e8f0ff'}, 6, 8)
    s.px(6, 9, '#a8c0ff'); s.px(9, 11, '#ffffff')
    return s.render()


def _charms():
    t = {'crimson_drip': 1, 'bloodbat': 2, 'blood_halo': 3, 'clover': 1, 'gold_rush': 2, 'jackpot_crown': 3,
         'xenite_glow': 1, 'tractor_beam': 2, 'saucer_orbit': 3}
    mot = {'crimson_drip': m_crimson_drip, 'bloodbat': m_bloodbat, 'blood_halo': m_blood_halo, 'clover': m_clover,
           'gold_rush': m_gold_rush, 'jackpot_crown': m_jackpot_crown, 'xenite_glow': m_xenite_glow,
           'tractor_beam': m_tractor_beam, 'saucer_orbit': m_saucer_orbit, 'starlit': m_starlit, 'glimmer': m_glimmer,
           'bloom': m_bloom, 'void': m_void, 'ashen': m_ashen, 'cinder': m_cinder, 'ember': m_ember, 'soul': m_soul,
           'frost': m_frost, 'petal': m_petal, 'gilded': m_gilded, 'heart': m_heart}
    out = {f'charm_{k}': charm(m, t.get(k, 2)) for k, m in mot.items()}
    out.update({'charm_rainbow': charm_rainbow, 'charm_storm': charm_storm, 'charm_eclipse': charm_eclipse,
                'charm_wings_angel': charm_wings_angel, 'charm_wings_evil': charm_wings_evil, 'xp_charm': xp_charm,
                'celi_charm': celi_charm})
    return out


# ================================================================== COINS, SEALS AND SIGILS
# a coin: a rim lit like a ball, its face sunk (lit the other way), a symbol struck in relief on it
RIM_LIGHT, SUNK = (-0.6, -0.8), (0.6, 0.8)


def emboss(s, rows, pal, x0, y0, lo=None):
    """a symbol in relief: each stroke casts a one-pixel shadow down and to the right"""
    pts = {}
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch not in '. ': pts[(x0 + x, y0 + y)] = ch
    if lo:
        for (x, y) in pts:
            if (x + 1, y + 1) not in pts: s.px(x + 1, y + 1, lo)
    for (x, y), ch in pts.items():
        s.px(x, y, pal[ch])
    return s


def coin(metal, face, r=6.9, rim=1.5, cx=8.0, cy=8.0):
    s = S()
    s.disc(cx, cy, r, metal)
    s.disc(cx, cy, r - rim, face, light=SUNK)
    return s


SIGIL = {   # Bond Sigils: an enamel face in a gold rim, its sign in white
    'bulwark': ('#4a7aff', ['XXXXXXX', 'XXXOXXX', 'XXXOXXX', 'XOOOOOX', '.XXOXX.', '..XOX..', '...X...']),
    'fortune': ('#e8b020', ['...X...', '.XXXXX.', 'X..X...', '.XXXXX.', '...X..X', '.XXXXX.', '...X...']),
    'fury':    ('#e8402a', ['....XX.', '...XX..', '..XXXX.', '.XXXX..', '...XX..', '..XX...', '.XX....']),
    'sight':   ('#9a6aff', ['.......', '..XXX..', '.X...X.', 'X..O..X', '.X...X.', '..XXX..', '.......']),
    'swift':   ('#2ac0a0', ['X..X...', '.X..X..', '..X..X.', '...X..X', '..X..X.', '.X..X..', 'X..X...']),
    'vigor':   ('#ff7a2a', ['.XX.XX.', 'XXXXXXX', 'XXXXXXX', '.XXXXX.', '..XXX..', '...X...', '.......']),
    'warding': ('#e8c83a', ['...X...', '..X.X..', '.X.O.X.', 'X.OOO.X', '.X.O.X.', '..X.X..', '...X...']),
}


def sigil(k):
    col, sign = SIGIL[k]
    def f():
        face = ramp(col)
        s = coin(GOLD, face)
        emboss(s, sign, {'X': '#ffffff', 'O': face[1]}, 5, 5, lo=face[0])
        return s.render()
    return f


def bond_sigil():
    face = ramp('#ff7ab8')
    s = coin(GOLD, face)
    emboss(s, ['.XX.XX.', 'XhXXXXX', 'XXXXXXX', '.XXXXX.', '..XXX..', '...X...'], {'X': GOLD[3], 'h': GOLD[4]}, 5, 5, lo=face[0])
    return s.render()


def bloodforge_sigil():
    s = coin(GOLD, ['#3a0606', '#5a0a0a', '#7a1010', '#8a1818'])
    _gem_drop_small(s, '#e8202a', 6, 5)
    s.g(['.ML.', 'MLhM', 'MLMD', '.MD.'], {'M': '#c41a1a', 'L': '#ff4a3a', 'h': '#ffb0a0', 'D': '#7a0a0a'}, 6, 7)
    for (x, y) in ((8, 4), (4, 8), (11, 8), (8, 12)): s.px(x, y, GOLD[4])
    return s.render()


RAT_FACE = ['E.....E',
            'EE...EE',
            '.FFFFF.',
            'FeFFFeF',
            '.FFnFF.',
            '..FwF..']


def token():
    """the Black Market token: a gold rat's face struck on black, in a gold rim"""
    s = coin(GOLD, BLACK)
    emboss(s, RAT_FACE, {'E': GOLD[2], 'F': GOLD[3], 'e': '#ff3a3a', 'n': '#ff9ab0', 'w': GOLD[4]}, 5, 5, lo='#000000')
    s.px(6, 7, GOLD[4])
    return s.render()


def medallion():
    """the Medallion: a violet medal with the white rat's face, its ears over the rim"""
    s = S()
    s.disc(8, 9, 6.4, PURPLE)
    s.disc(8, 9, 4.9, ['#3a1a5a', '#4b2475', '#5e3090', '#7440a8'], light=SUNK)
    s.g(['W....W', 'Ww..wW', 'Wp..pW'], {'W': '#f4f0ff', 'w': '#c8c0e0', 'p': '#ff9ad0'}, 5, 1)
    s.g(['.WWWW.', 'WWWWWW', 'WEWWEW', 'WWWWWW', '.WWnW.', '..ww..'], {'W': '#f4f0ff', 'E': '#2a1040', 'n': '#ff8ab0', 'w': '#c8c0e0'}, 5, 6)
    s.px(5, 7, '#ffffff'); s.px(10, 11, '#c8c0e0')
    return s.render()


def gutter_coin():
    face = GOLD[1:]
    s = coin(GOLD, face)
    emboss(s, RAT_FACE, {'E': '#4a2a08', 'F': '#5a3a10', 'e': '#ffd23f', 'n': '#ff8a8a', 'w': '#4a2a08'}, 5, 5, lo=GOLD[0])
    return s.render()


def gutter_medallion():
    s = coin(COPPER, COPPER[:4])
    emboss(s, RAT_FACE, {'E': '#3a1a0a', 'F': '#4a2410', 'e': '#ffcf8a', 'n': '#ff9a9a', 'w': '#3a1a0a'}, 5, 5, lo=COPPER[0])
    s.g(['L.L.L', '.....'], {'L': COPPER[4]}, 6, 13)
    return s.render()


def gold_doubloon():
    s = coin(GOLD, GOLD[1:])
    emboss(s, ['.XXXX.', 'X....X', 'X.XX..', '.X..X.', '..XX.X', 'X....X', '.XXXX.'], {'X': GOLD[4]}, 5, 4, lo=GOLD[0])
    for a in range(0, 16, 2):
        pass
    return s.render()


def lucky_token():
    s = coin(GOLD, ['#d8c080', '#ecd8a0', '#f8ecc0', '#fff8e0'])
    g = GREEN
    emboss(s, ['.GG.GG.', 'GhGGhGG', '.GGGGG.', 'GGGGGGG', 'GhG.GhG', '.G.s.G.', '...s...'], {'G': g[2], 'h': g[4], 's': g[0]}, 4, 4, lo='#a88a50')
    return s.render()


def tul_coin():
    """Tullius's doubloon: old gold rimed with frost, a grinning skull struck on it"""
    s = coin(GOLD, GOLD[1:])
    for (x, y, c) in ((4, 2, '#ffffff'), (5, 1, '#d8f4ff'), (2, 5, '#d8f4ff'), (10, 1, '#a8e0f8'), (13, 5, '#d8f4ff'), (2, 10, '#a8e0f8')):
        s.px(x, y, c)
    emboss(s, ['.XXXXX.', 'XXXXXXX', 'XO.X.OX', 'XXX.XXX', '.XXXXX.', '.X.X.X.'], {'X': '#fff6e0', 'O': '#2a1804'}, 4, 5, lo=GOLD[0])
    s.px(6, 7, '#2a1804'); s.px(10, 7, '#2a1804')
    return s.render()


def gamblers_coin():
    face = ramp('#3ac85a')
    s = coin(GOLD, face)
    emboss(s, ['XXXXX', 'X.X.X', 'XXXXX', 'X.X.X', 'XXXXX'], {'X': '#ffffff'}, 6, 6, lo=face[0])
    s.px(7, 7, '#1a4a20'); s.px(9, 9, '#1a4a20')
    return s.render()


def silver_seal():
    s = coin(IRON, IRON[1:])
    emboss(s, ['XXXXX', 'X...X', 'X.X.X', 'X...X', 'XXXXX'], {'X': IRON[4]}, 6, 6, lo=IRON[0])
    return s.render()


def forged_seal():
    """a wax seal: a red blob with a rough edge, a crest pressed into it"""
    s = S()
    w = ['#4a0808', '#7a1010', '#b01e1e', '#e0402e', '#ff8a70']
    s.disc(8, 8, 6.6, w)
    for (x, y) in ((1, 6), (2, 12), (13, 3), (14, 9), (6, 14), (11, 14)): s.px(x, y, w[2])
    s.disc(8, 8, 4.3, w[:4], light=SUNK)
    emboss(s, ['.X.X.', 'XXXXX', '.XXX.', '..X..'], {'X': w[1]}, 6, 6, lo=w[0])
    s.px(5, 4, '#ffc0b0')
    return s.render()


def apo_oath():
    """the Serpent's Oath: a serpent ring biting its tail round an emerald fang"""
    s = S()
    sc = ['#0a2a14', '#14481e', '#1e6e2c', '#3a9a44', '#7ad070']
    s.ring(8, 8, 6.8, 6.8, 2.0, sc)
    for a, (x, y) in enumerate(((4, 3), (11, 3), (13, 8), (11, 12), (4, 12), (2, 8))):
        s.px(x, y, sc[4] if a % 2 else sc[1])
    s.g(['HH', 'He'], {'H': sc[3], 'e': '#ffd23f'}, 7, 1)
    em = ramp('#3aff8a')
    s.g(['.L.', 'LhM', 'LhM', 'LMD', '.MD', '.D.'], {'L': em[3], 'h': em[4], 'M': em[2], 'D': em[1]}, 6, 5)
    return s.render()


def captains_insignia():
    """the Captain's badge: a gold shield with a red cross, on a violet ribbon"""
    s = S()
    s.g(['VV....VV', '.VV..VV.', '..VVVV..'], {'V': '#7a3ad0'}, 4, 0)
    s.px(5, 0, '#a86aff'); s.px(10, 0, '#a86aff')
    s.g(['.YYYYYYY.',
         'YhyyyyyyM',
         'YyyyRyyyM',
         'YyyRRRyyM',
         'YyyyRyyyM',
         '.YyyyyyM.',
         '..YyyyM..',
         '...YMM...'], {'Y': GOLD[3], 'h': GOLD[4], 'y': GOLD[2], 'M': GOLD[1], 'R': '#e02a2a'}, 3, 4)
    return s.render()


def demo_seal():
    """Democratus's Storm Seal: a green storm crystal on a black iron pin, sparks crackling round it"""
    s = S()
    c = ramp('#5ad85a')
    s.g(['...L...',
         '..LhM..',
         '..LhM..',
         '.LLhMD.',
         '.LhMMD.',
         '..LMD..',
         '...D...'], {'L': c[3], 'h': c[4], 'M': c[2], 'D': c[1]}, 5, 1)
    s.line(8, 8, 8, 14, BLACK[3], 2)
    s.g(['IIIIII'], {'I': BLACK[3]}, 5, 8)
    for (x, y, col) in ((2, 4, '#e8ffb0'), (3, 5, '#a8ff6a'), (13, 3, '#e8ffb0'), (12, 6, '#a8ff6a'), (3, 12, '#a8ff6a'), (12, 12, '#e8ffb0')):
        s.px(x, y, col)
    return s.render()


def leo_crest():
    """Leo's crest: a knight's blue kite shield, a silver rim, a gold lion's mark"""
    s = S()
    b = ramp('#2a6ad0')
    s.g(['IIIIIIIIII',
         'IbbbbbbbbI',
         'IbhbbbbbdI',
         'IbbbYYbbdI',
         'IbbYYYYbdI',
         'IbbbYYbbdI',
         'IbbYbbYbdI',
         '.IbbbbbdI.',
         '.IbbbbbdI.',
         '..IbbbdI..',
         '...IbdI...',
         '....II....'], {'I': IRON[3], 'b': b[2], 'h': b[4], 'd': b[1], 'Y': GOLD[3]}, 3, 2)
    s.px(3, 2, IRON[4]); s.px(12, 2, IRON[1])
    return s.render()


def donado_tag():
    """Donado's tag: an alien ID plate on a clip, its orange read-out"""
    s = S()
    s.g(['....III...', '...I...I..'], {'I': IRON[2]}, 3, 1)
    s.g(['.MMMMMMMMMM.',
         'MLLLLLLLLLLD',
         'MLccccccccLD',
         'MLcgggggg cD',
         'MLccccccccLD',
         'MLLLLLLLLLLD',
         'MLoLoLoLoLLD',
         'MLLLLLLLLLLD',
         '.DDDDDDDDDD.'], {'M': IRON[2], 'L': IRON[3], 'D': IRON[1], 'c': '#1a2a2a', 'g': '#5aff7a', 'o': '#ff8a2a'}, 2, 3)
    return s.render()


def _ring(s, metal, cx=8, cy=10.5, rx=5.5, ry=4.0):
    s.ring(cx, cy, rx, ry, 1.6, metal)


def frog_signet():
    s = S()
    _ring(s, GOLD)
    g = ramp('#4aa84a')
    s.g(['.EE..EE.', 'EwEggEwE', 'gggggggg', 'gddddddg', '.gggggg.'], {'E': g[3], 'w': '#ffffff', 'g': g[2], 'd': '#1a3a14'}, 4, 1)
    s.px(6, 2, '#000000'); s.px(10, 2, '#000000')
    return s.render()


def rat_signet():
    s = S()
    _ring(s, GOLD)
    s.disc(8, 4.5, 3.6, GOLD)
    emboss(s, ['E...E', '.FFF.', 'FeFeF', '.FnF.'], {'E': GOLD[1], 'F': GOLD[1], 'e': '#2a1a04', 'n': '#ff9ab0'}, 6, 2)
    return s.render()


def rat_king_signet():
    s = S()
    _ring(s, GOLD)
    s.g(['Y.Y.Y', 'YYYYY'], {'Y': GOLD[4]}, 6, 0)
    s.disc(8, 5, 3.4, GOLD)
    s.g(['.RRR.', 'RrRrR', '.RRR.'], {'R': '#e02a2a', 'r': '#ff8a7a'}, 6, 3)
    return s.render()


def honeycomb_brooch():
    """an amber cabochon in a gold frame, a honeycomb in the amber, a little bee on the rim"""
    s = S()
    s.disc(8, 8.5, 6.4, GOLD)
    s.disc(8, 8.5, 4.9, ['#6a3204', '#a85a0a', '#e08a14', '#ffb83a', '#ffe08a'])
    for (x, y) in ((6, 6), (10, 6), (4, 9), (8, 9), (12, 9), (6, 12), (10, 12)):
        s.px(x, y - 1, '#6a3204'); s.px(x - 1, y, '#6a3204'); s.px(x + 1, y, '#6a3204'); s.px(x, y + 1, '#8a4204')
    s.px(5, 5, '#fff2c0'); s.px(6, 4, '#ffe08a')
    s.g(['.ww', 'BYB', '.Bw'], {'B': '#1a1004', 'Y': '#ffe14a', 'w': '#e8f6ff'}, 11, 1)
    return s.render()


def _emblem_sign():
    return {
        'brood': ['X.....X', '.X...X.', 'X.XXX.X', '.XXOXX.', 'X.XXX.X', '.X...X.', 'X.....X'],
        'frost': ['...X...', '.X.X.X.', '..XXX..', 'XXXOXXX', '..XXX..', '.X.X.X.', '...X...'],
        'hex':   ['.......', '..XXX..', '.XX.XX.', 'XX.O.XX', '.XX.XX.', '..XXX..', '.......'],
        'hollow': ['.......', 'X..X..X', 'XX.X.XX', 'XXXXXXX', 'XOXOXOX', 'XXXXXXX', '.......'],
        'keep':  ['X.X.X.X', 'XXXXXXX', '.XXXXX.', '.XXOXX.', '.XXOXX.', '.XXXXX.', 'XXXXXXX'],
        'tide':  ['X..X..X', 'X..X..X', 'XX.X.XX', '.XXXXX.', '...X...', '...X...', '...X...'],
    }


def emblem(d):
    def f():
        from p2.config import D
        col = {'hollow': '#5a6a80', 'keep': '#8a4a3a'}.get(d, D[d]['color'])
        inner = ramp(col)
        s = coin(GOLD, inner)
        emboss(s, _emblem_sign()[d], {'X': ramp(inner[4])[3], 'O': inner[0]}, 5, 5, lo=inner[0])
        return s.render()
    return f


def pearl_sigil(n):
    """Pearlman's sigils (I, II, III): a pearl in a teal setting, one more notch per rank"""
    def f():
        s = S()
        s.ring(8, 8, 6.6, 6.6, 2.0, TEAL)
        s.disc(8, 8, 3.6, ['#7a8a96', '#b0bcc6', '#dfe6ec', '#ffffff'] if n == 1 else
               (['#2a8a8a', '#48b8b0', '#8ae8dc', '#e8fffa'] if n == 2 else ['#0e2a3a', '#1a4a62', '#2a6a8a', '#6ab0d0']))
        for (x, y) in [(8, 1), (14, 8), (8, 14)][:n]:
            s.px(x, y, GOLD[3])
        return s.render()
    return f


def pearl_of_return():
    s = S()
    s.disc(8, 8, 6.4, ['#06302c', '#0e5048', '#1a7a6e', '#36b0a0', '#8ae8dc'])
    s.disc(8.6, 8.6, 2.6, ['#020a0a', '#061614', '#0a2420'])
    s.px(5, 4, '#e8fffa'); s.px(4, 5, '#a8f0e4')
    return s.render()


def deep_pearl():
    s = S()
    s.disc(8, 8.5, 6.0, ['#0e4a52', '#1a7480', '#30a8b0', '#6ad8d8', '#c8fff8'])
    s.px(5, 5, '#ffffff'); s.px(6, 5, '#e8fffa'); s.px(5, 6, '#e8fffa')
    return s.render()


# ================================================================== ROSETTES (the Curator's, one per wing)
def rosette(col, grand=False):
    """a prize rosette: a scalloped, pleated frill round a gold button, two ribbon tails below"""
    def f():
        import math
        s = S()
        r = ramp(col)
        rb = ramp('#c8202a') if grand else r
        s.g(['LM...LM', 'LM...LM', 'LMD.LMD', 'L.D.L.D'], {'L': rb[3], 'M': rb[2], 'D': rb[1]}, 4, 11)    # the tails
        wing = ['#ff8ad8', '#a89ad8', '#ffcf40', '#7ae0ff', '#3ab0c8', '#7ad06a']
        cx, cy = 8, 6.8
        for y in range(16):
            for x in range(16):
                dx, dy = x + 0.5 - cx, y + 0.5 - cy
                d = math.hypot(dx, dy); a = math.atan2(dy, dx)
                edge = 6.0 + 0.6 * math.cos(a * 8)
                if d <= edge:
                    seg = int(((a + math.pi) / (2 * math.pi)) * 16)
                    c = ramp(wing[(seg // 2) % 6]) if grand else r
                    k = 3 if seg % 2 else 2
                    if d > edge - 1.0: k -= 1
                    elif d < 3.6: k += 1
                    s.px(x, y, c[k])
        s.disc(cx, cy, 2.7, GOLD)
        s.px(7, 5, GOLD[4]); s.px(6, 6, GOLD[4])
        return s.render()
    return f


def cab_veiled():
    """an exhibit still under its velvet cloth, on a gold plinth, a gold question mark on the cloth"""
    s = S()
    v = ['#2a0812', '#4a1424', '#6a2038', '#8a3050', '#b04a70']
    s.g(['.....LM.....',
         '....LLMM....',
         '...LhLMMD...',
         '..LhLLMMDD..',
         '..LLLLMMDD..',
         '.LhLLLMMMDD.',
         '.LLLLLMMMDD.',
         'LLhLLLMMMDDD',
         'LLLLLLMMMDDD',
         'LMLLMLMMDMDD'], {'L': v[2], 'h': v[3], 'M': v[1], 'D': v[0]}, 2, 2)
    s.g(['.YY.', 'Y..Y', '...Y', '..Y.', '..Y.', '....', '..Y.'], {'Y': '#ffd860'}, 6, 3)
    s.g(['YYYYYYYYYYYYYY', 'dddddddddddddd'], {'Y': GOLD[3], 'd': GOLD[1]}, 1, 12)
    return s.render()


# ================================================================== LAURELS AND TROPHIES
def laurel(col, gem='#e02a2a'):
    """a laurel wreath: a leafy band round a circle, open at the top, tied at the bottom with a gem"""
    def f():
        import math
        s = S()
        r = ramp(col)
        cx, cy = 8.0, 7.6
        for y in range(16):
            for x in range(16):
                dx, dy = x + 0.5 - cx, y + 0.5 - cy
                d = math.hypot(dx, dy)
                a = math.atan2(dx, -dy)                            # 0 at the top, +-pi at the bottom
                if abs(a) < 0.42: continue                         # (the gap at the top)
                ph = (abs(a) - 0.42) / 0.40                        # leaves, from the top down
                fr = ph - math.floor(ph)
                outer = 6.4 - 0.9 * abs(fr - 0.5) * 2
                if 3.2 <= d <= outer:
                    k = 3 if fr < 0.5 else 2
                    if d > outer - 0.8: k -= 1
                    if d < 3.9: k -= 1
                    if a < 0 and fr < 0.3: k += 1                  # (the left branch catches the light)
                    s.px(x, y, r[max(0, min(4, k))])
        for (x, y) in ((4, 2), (11, 2)): s.px(x, y, r[4])
        _gem_drop_small(s, gem, 6, 11)
        return s.render()
    return f


def _cup(s, metal, motif=None, mcol=None):
    s.g(['HHHHHHHHHHHH',
         'hLLLLLLLLMMD',
         'HLhLLLLLLMMD',
         '.LhLLLLLLMD.',
         '.LLLLLLLMMD.',
         '..LLLLLLMD..',
         '...LLLLMD...',
         '.....LM.....',
         '.....LM.....',
         '....LLMM....',
         '..HHHHHHHH..',
         '..DDDDDDDD..'], {'H': metal[4], 'h': metal[3], 'L': metal[3], 'M': metal[2], 'D': metal[1]}, 2, 2)
    s.g(['HH', 'H.', 'HH'], {'H': metal[2]}, 0, 3); s.g(['HH', '.H', 'HH'], {'H': metal[1]}, 14, 3)
    if motif:
        emboss(s, motif, {'X': mcol or metal[0], 'O': '#ffffff'}, 6, 4, lo=None)
    return s


TROPHY = {   # each puzzle room's cup: its own mark on it
    'coffers': ['XXXX', 'X..X', 'XXXX', 'XOOX'],
    'dial':    ['.XX.', 'X.OX', 'X..X', '.XX.'],
    'guards':  ['X..X', 'XXXX', 'XXXX', '.XX.'],
    'lasers':  ['X..X', '.XX.', '.XX.', 'X..X'],
    'levers':  ['..X.', '.X..', 'X...', 'XXXX'],
    'plates':  ['XX.X', 'XX.X', '....', 'X.XX'],
    'tiles':   ['X.X.', '.X.X', 'X.X.', '.X.X'],
}


def trophy_room(k):
    def f():
        s = S()
        _cup(s, GOLD, TROPHY[k], '#8a4a0a')
        return s.render()
    return f


def gutter_trophy():
    s = S()
    _cup(s, ramp('#e8c070'))
    return s.render()


def lucky_trophy():
    s = S()
    _cup(s, GOLD)
    emboss(s, ['.GG.', 'GGGG', 'GGGG', '.Gs.'], {'G': '#3ab84a', 's': '#1a6a20'}, 6, 4)
    return s.render()


def trophy():
    """the Rat Trophy: a gold cup shaped like a rat's head, ears and all, a pink tail curling off the base"""
    s = S()
    _cup(s, GOLD)
    s.g(['PP', 'Pp'], {'P': GOLD[3], 'p': '#ff9ad0'}, 1, 0); s.g(['PP', 'pP'], {'P': GOLD[2], 'p': '#ff9ad0'}, 13, 0)
    s.g(['E..E', '....', '.nn.'], {'E': '#2a1a04', 'n': '#ff8ab0'}, 6, 4)
    s.g(['pp', '.p'], {'p': '#ff8ab0'}, 13, 13)
    return s.render()


OVERRIDES = {}
OVERRIDES['rat_king_key'] = rat_king_key
OVERRIDES.update(_charms())

OVERRIDES.update({f'sigil_{k}': sigil(k) for k in SIGIL})
OVERRIDES.update({'bond_sigil': bond_sigil, 'bloodforge_sigil': bloodforge_sigil, 'token': token, 'medallion': medallion,
                  'gutter_coin': gutter_coin, 'gutter_medallion': gutter_medallion, 'gold_doubloon': gold_doubloon,
                  'lucky_token': lucky_token, 'tul_coin': tul_coin, 'gamblers_coin': gamblers_coin, 'silver_seal': silver_seal,
                  'forged_seal': forged_seal, 'apo_oath': apo_oath, 'captains_insignia': captains_insignia, 'demo_seal': demo_seal,
                  'leo_crest': leo_crest, 'donado_tag': donado_tag, 'frog_signet': frog_signet, 'rat_signet': rat_signet,
                  'rat_king_signet': rat_king_signet, 'honeycomb_brooch': honeycomb_brooch, 'cab_veiled': cab_veiled,
                  'pearl_of_return': pearl_of_return, 'deep_pearl': deep_pearl, 'gutter_trophy': gutter_trophy,
                  'lucky_trophy': lucky_trophy, 'trophy': trophy})
OVERRIDES.update({f'emblem_{d}': emblem(d) for d in ('brood', 'frost', 'hex', 'hollow', 'keep', 'tide')})
OVERRIDES.update({f'pearl_sigil_{n}': pearl_sigil(n) for n in (1, 2, 3)})
OVERRIDES.update({f'cab_rosette_{w}': rosette(c) for w, c in (('hollow', '#a89ad8'), ('gutter', '#ffcf40'), ('skies', '#7ae0ff'),
                                                             ('deep', '#3ab0c8'), ('wilds', '#7ad06a'), ('court', '#ff8ad8'))})
OVERRIDES['cab_rosette_grand'] = rosette('#ffcf40', grand=True)
OVERRIDES.update({f'laurel_t{t}': laurel(c) for t, c in ((1, '#d9824a'), (2, '#c8d0d8'), (3, '#ffcf40'), (4, '#4ad0c0'), (5, '#8a7a96'))})
OVERRIDES['gutter_laurel'] = laurel('#ffcf40', gem='#3ab84a')
OVERRIDES.update({f'trophy_{k}': trophy_room(k) for k in TROPHY})

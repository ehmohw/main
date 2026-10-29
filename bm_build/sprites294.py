"""2.94y: THE 16 x 16 REDRAWS - icons drawn again by hand as vanilla items are: 16 x 16, a one-pixel dark outline, lit from the
top left, a handful of shades. These have the last word (every_override applies them over sprites280..280e): the Dread Token
and the Ravenous Heart (from PixelLab drafts at 32 x 32 - a skull struck on crimson in an iron rim; a heart with a fanged maw
and a drip - drawn again at item size, since a 32 squeezed to 16 turns to mush), the five alien weapons, the Smuggler's
Waytoken and the Wings of the Damned (the icon here; both wings as worn, and the holy icon, written by phase182)."""
from PIL import Image
import math


def hexc(h, a=255): return tuple(int(h[i:i+2],16) for i in (1,3,5)) + (a,)
def dread_token():
    im = Image.new('RGBA', (16,16), (0,0,0,0)); px = im.load()
    cx = cy = 7.5; R = 7.1
    iron = ['#2c282c', '#433d43', '#5f585f', '#857e86', '#b2acb4']
    red = ['#420610', '#640b18', '#8a1426', '#ad1f36', '#cf3a4e']
    for y in range(16):
        for x in range(16):
            dx, dy = x - cx, y - cy; d = math.hypot(dx, dy)
            if d > R: continue
            l = (-dx - dy) / (R * 1.41)
            if d > R - 1: px[x,y] = hexc('#18121a'); continue
            if d > R - 2.2:
                px[x,y] = hexc(iron[max(0, min(4, int(2.2 + l * 2.8)))]); continue
            if d > R - 2.9: px[x,y] = hexc('#21070b'); continue
            px[x,y] = hexc(red[max(0, min(4, int(2.3 + l * 2.4)))])
    sk = ['..www..', '.wwwwwg', 'wwwwwwg', 'wkkwkkg', 'wwwkwwg', '.wwwwg.', '.w.w.g.']
    pal = {'w': '#ece6d8', 'g': '#b4aa9c', 'k': '#1a0a0c'}
    for j, row in enumerate(sk):
        for i, ch in enumerate(row):
            if ch != '.': px[4 + i, 4 + j] = hexc(pal[ch])
    px[5, 5] = hexc('#ffffff')
    return im
def ravenous_heart():
    M = ['................',
         '..XXXX...XXXX...',
         '.XXXXXX.XXXXXX..',
         'XXXXXXXXXXXXXXX.',
         'XXXXXXXXXXXXXXX.',
         'XXXXXXXXXXXXXXX.',
         'XXXXXXXXXXXXXXX.',
         '.XXXXXXXXXXXXX..',
         '.XXXXXXXXXXXXX..',
         '..XXXXXXXXXXX...',
         '...XXXXXXXXX....',
         '....XXXXXXX.....',
         '.....XXXXX......',
         '......XXX.......',
         '.......X........',
         '................']
    m = [[c == 'X' for c in r] for r in M]
    shade = ['#4c0410', '#6e0818', '#911024', '#b51a32', '#d93a50', '#f07888']
    im = Image.new('RGBA', (16,16), (0,0,0,0)); px = im.load()
    inside = lambda x, y: 0 <= x < 16 and 0 <= y < 16 and m[y][x]
    for y in range(16):
        for x in range(16):
            if not m[y][x]: continue
            edge = not all(inside(x + a, y + b) for a, b in ((1,0),(-1,0),(0,1),(0,-1)))
            if edge: px[x,y] = hexc('#24020a'); continue
            l = ((7 - x) + (6 - y)) / 10
            px[x,y] = hexc(shade[max(0, min(5, int(2.4 + l * 2.4)))])
    px[3,3] = px[4,3] = px[3,4] = hexc('#f8a0ac')                 # the gleam
    px[10,3] = hexc('#e2546a')
    for (x, y) in ((11,5),(12,6),(10,8),(3,8),(5,10)):            # veins
        px[x,y] = hexc('#5a0612')
    maw = {(5,6):'k',(6,6):'k',(7,6):'k',(8,6):'k',(9,6):'k',(10,6):'k',
           (4,7):'k',(5,7):'w',(6,7):'k',(7,7):'w',(8,7):'k',(9,7):'w',(10,7):'k',(11,7):'k',
           (4,8):'k',(5,8):'m',(6,8):'m',(7,8):'m',(8,8):'m',(9,8):'m',(10,8):'m',(11,8):'k',
           (5,9):'k',(6,9):'w',(7,9):'k',(8,9):'w',(9,9):'k',(10,9):'k'}
    pal = {'k': '#160105', 'w': '#f2ead8', 'm': '#3a0208'}
    for (x, y), c in maw.items(): px[x, y] = hexc(pal[c])
    px[7,10] = hexc('#c41a32'); px[7,11] = hexc('#e03048')        # a drip from the maw
    return im


OVERRIDES = {'dread_token': dread_token, 'ravenous_heart': ravenous_heart}


# ================================================================== 2.94y: the auto-shaded redraws
# A sprite is a 16 x 16 map of materials. A lower-case letter is a material, shaded as vanilla shades: its silhouette edge is
# the ramp's darkest (the outline), a face lit from above or the left a step lighter, one in shadow (below, right) a step
# darker. An upper-case letter is a fixed colour (eyes, glints, a glow), drawn as it is.
RAMP = {
    'silver': ['#24262c', '#5c626e', '#8c929e', '#c0c6d0', '#eef2f6'], 'gun': ['#101216', '#262a32', '#3c424c', '#58606c', '#808a98'],
    'grip': ['#24160c', '#4a3018', '#6a4626', '#8a6038', '#a87a4a'], 'green': ['#0e3a14', '#1e8a2e', '#3ac84a', '#7aff6a', '#d8ffc8'],
    'pink': ['#4a0a28', '#a02a5a', '#e05a8a', '#ff8ab0', '#ffd0e0'],
    'red': ['#3a0408', '#8a1020', '#c82030', '#ff5a5a', '#ffc0c0'], 'violet': ['#2a0a4a', '#5a1a9a', '#8a3ad8', '#c27dff', '#ecd0ff'],
    'brass': ['#3a2808', '#7a5418', '#b07e28', '#d8a840', '#f8e080'],
    'gold': ['#3a2804', '#9a6e0a', '#d8a418', '#f8d040', '#fff6a8'],
    'rat': ['#2a2a30', '#6a6a74', '#9a9aa4', '#c4c4cc', '#e8e8f0'],
}


def paint(rows, mats, fixed=None):
    fixed = fixed or {}
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); px = im.load()
    at = lambda x, y: rows[y][x] if 0 <= x < 16 and 0 <= y < 16 else '.'
    for y in range(16):
        assert len(rows[y]) == 16, (y, rows[y])
        for x in range(16):
            ch = rows[y][x]
            if ch == '.': continue
            if ch in fixed: px[x, y] = hexc(fixed[ch]); continue
            R = RAMP[mats[ch]]
            if any(at(x + a, y + b) == '.' for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))): px[x, y] = hexc(R[0]); continue
            def run(a, b):                                   # how far this material goes that way
                n = 0
                while at(x + a * (n + 1), y + b * (n + 1)) == ch: n += 1
                return n
            u, l, d, r = run(0, -1), run(-1, 0), run(0, 1), run(1, 0)
            if u == 0 and l == 0: px[x, y] = hexc(R[4]); continue                 # the lit corner
            if d == 0 or (r == 0 and u > 0): px[x, y] = hexc(R[1]); continue      # the shadowed side
            if u == 0 or l == 0: px[x, y] = hexc(R[3]); continue                 # the lit side
            big = u + d >= 4 or l + r >= 5
            px[x, y] = hexc(R[3] if big and u <= 1 and d >= 2 else R[1] if big and d <= 1 else R[2])
    return im




def ray_gun():
    return paint(['................', '................', '................', '............gg..', '...........gggg.',
                  '.sssrsrsrssgWggg', '.sssrsrsrssggggg', '.sssrsrsrssggggg', '.ssssssssssgggg.', '..bbbb.s....gg..',
                  '..bbbbss........', '...bbbb.........', '...bbbb.........', '....bb..........', '................', '................'],
                 dict(s='silver', r='brass', b='grip', g='green'), dict(W='#ffffff'))


def plasma_blaster():
    return paint(['................', '................', '................', '................', '....kkkkkkkkk...',
                  '...kkCCCCCCkkkk.', '..kkkkkkkkkkkkkC', '..kkkkkkkkkkk...', '..kkkk.k........', '..kkkkkk........',
                  '...kkCk.........', '...kkkk.........', '....kkkk........', '....kkk.........', '................', '................'],
                 dict(k='gun'), dict(C='#5af0ff'))


def shrink_ray():
    return paint(['................', '................', '................', '................', '..........p.....',
                  '.sssrssrssppp...', '.sssrssrsspppppW', '.sssrssrsspppppp', '.ssssssssspppp..', '..bbbb.s..ppp...',
                  '..bbbbss..p.....', '...bbbb.........', '...bbbb.........', '....bb..........', '................', '................'],
                 dict(s='silver', r='pink', b='grip', p='pink'), dict(W='#ffe0ec'))


def growth_ray():
    return paint(['................', '................', '................', '..............rr', '.............rrr',
                  '.sssrssrsssrrrQQ', '.sssrssrsssrrrQQ', '.sssrssrsssrrrQQ', '.sssssssssssrrQQ', '..bbbb.s.....rrr',
                  '..bbbbss......rr', '...bbbb.........', '...bbbb.........', '....bb..........', '................', '................'],
                 dict(s='silver', r='red', b='grip'), dict(Q='#ffb0b0'))


def tractor_beam():
    return paint(['.........vvvv...', '........vvvvvv..', '.......vvWWvvvv.', '.......vvWvvvvv.', '.......vvvvvvvv.',
                  '.......vvvvvvvv.', '........vvvvvv..', '.......rrvvvv...', '......rrrr......', '.....sssr.......',
                  '....sss.........', '...rrr..........', '..bbb...........', '.bbb............', '.bb.............', '................'],
                 dict(v='violet', r='brass', s='silver', b='grip'), dict(W='#ffffff'))


# (the owner kept these five - the duck, the RPG, the bag of rocks, the Omni Token and the relics went back to their 2.80 art)
OVERRIDES.update({f.__name__: f for f in (ray_gun, plasma_blaster, shrink_ray, growth_ray, tractor_beam)})


# ---- the Smuggler's Waytoken: a rat in profile, inlaid in silver on brass (it read as a face looking out)
RAMP['coin'] = ['#4a3418', '#a07a30', '#d4aa50', '#ecc868', '#fff0a8']
RAMP['field'] = ['#4a3418', '#8a6424', '#a87c30', '#c0943c', '#d8ac50']


def waytoken():
    rows = [['.'] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            d = math.hypot(x - 7.5, y - 7.5)
            if d <= 7.1: rows[y][x] = 'b' if d > 5.0 else 'f'
    rat = ['......rr..', '.....rPPr.', '...rrrPPr.', '.rrrrrrrr.', 'NrrKrrrrrr', '.rrrrrrrrr', '..rrrrrrrr', '...rr..rr.']
    for j, row in enumerate(rat):
        for i, ch in enumerate(row):
            if ch != '.': rows[3 + j][3 + i] = ch
    rows[10][12] = rows[11][12] = rows[11][11] = rows[12][10] = 'r'               # its tail, curling down
    return paint([''.join(r) for r in rows], dict(b='coin', f='field', r='rat'), dict(N='#f0a0b0', P='#e88aa0', K='#141418'))


# ---- the Wings of the Damned (worn: an elytra's own layout) and their holy twin
def _wing(paint_px):
    """vanilla's elytra shape (vendor/elytra_wings.png), each opaque pixel painted again: paint_px(x, y, u, v, edge) -> rgba
    or None (a hole). u, v: where on the wing face (0..1 across, 0..1 down); edge: 'lead' (its outer, leading edge), 'tip'
    (its trailing feathers' ends) or None."""
    src = Image.open('/home/claude/bm_build/vendor/elytra_wings.png').convert('RGBA')
    sp = src.load(); out = Image.new('RGBA', src.size, (0, 0, 0, 0)); po = out.load()
    on = lambda x, y: 0 <= x < src.width and 0 <= y < src.height and sp[x, y][3] > 0
    for y in range(src.height):
        for x in range(src.width):
            if not on(x, y): continue
            u, v = (x - 34) / 12, (y - 2) / 20
            edge = 'lead' if not on(x - 1, y) else 'tip' if not on(x, y + 1) or not on(x + 1, y) else None
            c = paint_px(x, y, max(0, min(1, u)), max(0, min(1, v)), edge)
            if c: po[x, y] = c
    return out


def _feathers(u, v, x, y, edge, lead, dark, mid, lit, tips, shaft, covert, hole=False):
    """(2.99) a wing face in feathers, on vanilla's elytra shape: the leading edge, two rows of coverts along it, then flight
    feathers slanting back to the trailing edge - each feather three rows deep: its lit top, its vane, its shadowed underside,
    the shaft a lighter line - their ends `tips` (fire, light); hole: tatters torn out of the ends"""
    k = x - 34
    if edge == 'lead': return lead[(y // 2) % len(lead)]
    if k <= 3 and v < 0.85:                                                    # coverts: small scales in staggered rows
        r = (y + (k // 2) * 1) % 3
        return covert[0] if r == 0 else covert[1] if r == 1 else covert[2]
    s = y - (k - 4) // 2                                                       # flight feathers, slanting back
    f, r = s // 3, s % 3
    end = 1.0 - 0.05 * (f % 3)
    if v > 0.8 * end or edge == 'tip':
        if hole and (x * 5 + y * 3) % 7 == 0: return None
        return tips[min(len(tips) - 1, int((v - 0.72) * 14) + (k % 2))] if v > 0.72 else tips[0]
    if k == 5 + (f % 2): return shaft
    return [lit, mid, dark][r]


def damned_wings_tex():
    """(2.99) the Wings of the Damned: tattered black-violet feathers, soul fire along their ends"""
    def p(x, y, u, v, edge):
        if x < 34: return hexc('#2c1e36' if y % 2 else '#1e1424')
        return _feathers(u, v, x, y, edge, [hexc('#8a6ab0'), hexc('#c2a4e8')], hexc('#160e1c'), hexc('#2a1c34'), hexc('#46325a'),
                         [hexc('#3c2a6a'), hexc('#5a3ab0'), hexc('#4ab8e8'), hexc('#8ae8ff'), hexc('#d8f8ff')], hexc('#6a4e8a'),
                         [hexc('#5a4870'), hexc('#3c2a4a'), hexc('#241830')], hole=True)
    return _wing(p)


def holy_wings_tex():
    """(2.99) their holy twin: pearl feathers shaded in lavender, gold along the leading edge and the coverts' tips, a light
    edge - gold running to white - along their ends"""
    def p(x, y, u, v, edge):
        if x < 34: return hexc('#f8d040' if y % 2 else '#c89a20')
        return _feathers(u, v, x, y, edge, [hexc('#f8d040'), hexc('#fff2a0')], hexc('#cfc6d8'), hexc('#ece8f2'), hexc('#ffffff'),
                         [hexc('#e8c050'), hexc('#f8d868'), hexc('#fff0b0'), hexc('#fffbe0'), hexc('#ffffff')], hexc('#f0d890'),
                         [hexc('#fffdf6'), hexc('#e2dcd2'), hexc('#d8b048')])
    return _wing(p)


def hollow_wings():
    """(2.99) the icon: an elytra's own outline (two wings, folded) in black-violet feathers, the leading edges pale, soul fire
    at their ends"""
    return paint(['................', '..LLL......LLL..', '.LmMmL....LmMmL.', '.LmdMmL..LmMdmL.', '.LmmdMmLLmMdmmL.',
                  '.LmMmdMmmMdmMmL.', '.LmmMmdMMdmMmmL.', '.LmdmMmddmMmdmL.', '.LmmdmMmmMmdmmL.', '..LmmdmLLmdmmL..',
                  '..LmMmdLLdmMmL..', '..LmmSdLLdSmmL..', '...LSmSLLSmSL...', '...SS.C..C.SS...', '....C......C....', '................'],
                 dict(m='membrane'), dict(L='#8a6ab0', M='#5a4870', d='#160e1c', S='#4ab8e8', C='#d8f8ff'))


def angel_hollow_wings():
    """(2.99) the holy twin's icon: the same outline in pearl feathers, gold leading edges, a light edge at their ends"""
    return paint(['................', '..ggg......ggg..', '.gwWwg....gwWwg.', '.gwFWwg..gwWFwg.', '.gwwFWwggwWFwwg.',
                  '.gwWwFWwwWFwWwg.', '.gwwWwFWWFwWwwg.', '.gwFwWwFFwWwFwg.', '.gwwFwWwwWwFwwg.', '..gwwFwggwFwwg..',
                  '..gwWwFggFwWwg..', '..gwwTFggFTwwg..', '...gTwTggTwTg...', '...TT.Y..Y.TT...', '....Y......Y....', '................'],
                 dict(g='gold', w='feather'), dict(F='#cfc6d8', W='#ffffff', T='#f8d868', Y='#fffbe0'))


RAMP['bone'] = ['#3a3428', '#8a7e64', '#b8ac90', '#ddd2b6', '#f4ecd8']
RAMP['membrane'] = ['#0e0a12', '#1e1426', '#2e2038', '#40304e', '#5a4870']
RAMP['feather'] = ['#8a8478', '#d8d2c8', '#eeeae2', '#fbf9f4', '#ffffff']
OVERRIDES['waytoken'] = waytoken
OVERRIDES['hollow_wings'] = hollow_wings

"""2.96: THE GEM OF CREATIVITY, the follower - the approved mockup (mockups/creativity_gem.py) as a rigkit rig.

The shard of the Ethereal Gem that gives the Buddies life: an elongated octagon cut as a real stone - an octagonal GIRDLE, a flat
TABLE, eight sloped CROWN facets and a deeper PAVILION narrowing to the culet, each facet a thin plate at its true angle (26.x
elements turn on all three axes) so the light catches each one differently. Every colour of the rainbow swirls out of a pale heart,
little white doodles (notes, flowers, sparkles) drifting inside it: the swirl is an ANIMATED texture (32 frames, interpolated).

Its face is a text emoticon, lit on its table facet (2.96a - it floated over it before): :) c: :o :3 o3o ^-^ ;( and the rest
(EMOTES), each a little pixel-font plate (FONT) standing just proud of the table, glowing white with a dark outline so it reads
over every colour of the swirl. The plain head (cg_head) is :) ; cg_head_x<key> each of the others (phase231 picks them by mood).
It floats - its poses only move, tilt and spin it. Parts: the GEM (body); its FACE on the table (hidden when it's dim); its HALO,
a ring of tiny facet glints orbiting it (3.0a: always turning,
a full turn every HALO_TURN ticks - phase231 spins it; the poses leave it be).

THE ANIMATED TEXTURES: cg_table, cg_crown and cg_pav are vertical strips of 32 64x64 frames. The resource pack writes each with
textures() as usual (assets/bm/textures/block/<name>.png) and beside it the .png.mcmeta in ANIMATED - write_mcmeta(R2) does that,
from the follower phase's rp post (as phase61's hg_portal and phase131's apo_blackfire).

Design units: the gem's heart at PIVOT['body'] (it hovers - its lowest point ~0.6 blocks up), crown toward -z (its front)."""
import colorsys
import math

import numpy as np
from PIL import Image, ImageDraw

from rigkit import qs

PREFIX = 'cg_'
RIG_SCALE = 0.8                                    # (14 units tall -> 0.7 blocks)
PIVOT = {'body': (0, 19.0, 0), 'head': (0, 19.0, 0), 'halo': (0, 19.0, 0),
         'wing_r': (1.7, 22.8, 3.3), 'wing_l': (-1.7, 22.8, 3.3)}      # (3.0a: its forms' wings, at its back - a speck in its own form)
PARENT = {'body': None, 'head': 'body', 'halo': None, 'wing_r': 'body', 'wing_l': 'body'}
WINGS = ('wing_r', 'wing_l')
PARTS = tuple(PIVOT)
PART_K = {}
FACES = ()
SWIM_FRAMES = 8

N = 64                                    # texture px across a 16-unit face
FRAMES = 32
W, H, C = 5.0, 7.0, 2.2                   # the girdle: half width, half height, the corners' cut
TK = 0.5                                  # the table, as a share of the girdle
ZG, ZT, ZC = -0.35, -1.9, 3.3             # the girdle's half thickness, the table's height (front), the culet's depth (back)
O = np.array([8.0, 8.0, 8.0])             # (model units: the heart sits at the part's joint)
ANIMATED = {f'cg_{k}': {'animation': {'frametime': 3, 'interpolate': True}} for k in ('table', 'crown', 'pav')}
ANIMATED.update({f'cg_w_{k}': {'animation': {'frametime': 3, 'interpolate': True}} for k in ('table', 'crown', 'pav')})   # (3.0a: the Wraithfire Form's smoke)
ANIMATED['cg_wf_flame'] = {'animation': {'frametime': 2, 'interpolate': True}}                                         # (...and its flames, flickering)


def write_mcmeta(R2):
    """(the follower phase's rp post) the swirl's animation, beside each strip"""
    for k, meta in ANIMATED.items():
        R2.wj(f'assets/bm/textures/block/{k}.png.mcmeta', meta)


def HIDDEN(p, pose):
    return p in ('head', 'halo') and pose.get('_dim', False)


def model_name(p, pose, suffix=''):
    return f'{PREFIX}{p}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def octagon(s=1.0, dims=None):
    W_, H_, C_ = dims or (W, H, C)
    w, h, c = W_ * s, H_ * s, C_ * s
    return [(-w, -(h - c * 1.2)), (-w, h - c * 1.2), (-(w - c), h), (w - c, h), (w, h - c * 1.2), (w, -(h - c * 1.2)), (w - c, -h), (-(w - c), -h)]


def inside(x, y, s=1.0, pad=0.0, dims=None):
    W_, H_, C_ = dims or (W, H, C)
    w, h, c = W_ * s - pad, H_ * s - pad, C_ * s
    if abs(x) > w or abs(y) > h: return False
    return (abs(x) - (w - c)) / c + (abs(y) - (h - c * 1.2)) / (c * 1.2) <= 1.0


def swirl(f, kind):
    """one frame of the swirl: the hue turning round the heart (f / FRAMES of a turn)"""
    im = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    ph = f / FRAMES
    px_ = im.load()
    for py in range(N):
        for px in range(N):
            x = (px + 0.5) * 16 / N - 8; y = 8 - (py + 0.5) * 16 / N
            dx, dy = x / W, y / H
            r = math.hypot(dx, dy); a = math.atan2(dy, dx)
            h = ((a / (2 * math.pi)) + r * 0.55 - ph) % 1.0
            band = h * 8; fr = band - int(band)
            h = (int(band) + (0 if fr < 0.8 else (fr - 0.8) / 0.2)) / 8
            s = min(1, 0.12 + 0.8 * r * 1.4); v = 1.0 - 0.08 * r
            if kind == 'crown': s *= 0.8; v = min(1, v + 0.06)
            if kind == 'pav': s = min(1, s * 1.15); v *= 0.78
            rr, gg, bb = colorsys.hsv_to_rgb(h, s, v)
            px_[px, py] = (int(rr * 255), int(gg * 255), int(bb * 255), 255)
    if kind == 'table':                   # the doodles, drifting round with the colours
        Wt = (255, 255, 255, 255)
        glyphs = {'note': ['.##', '.#.', '.#.', '##.', '##.'], 'flower': ['.#.', '###', '.#.'], 'spark': ['.#.', '#.#', '.#.'], 'dot': ['#']}
        for g, rad, a0 in (('note', 0.22, 0.0), ('flower', 0.30, 0.25), ('spark', 0.12, 0.5), ('note', 0.32, 0.62),
                           ('spark', 0.26, 0.85), ('dot', 0.05, 0.4), ('flower', 0.15, 0.75)):
            a = 2 * math.pi * (a0 - ph * 0.5)
            cx = int(N / 2 + math.cos(a) * rad * N * W / 8); cy = int(N / 2 - math.sin(a) * rad * N * H / 8)
            for j, row in enumerate(glyphs[g]):
                for k, ch in enumerate(row):
                    if ch == '#' and 0 <= cx + k < N and 0 <= cy + j < N: px_[cx + k, cy + j] = Wt
    return im


def _glint():
    """a facet glint: white at the heart, a pale tint at its edges"""
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 15, 15), fill=(214, 240, 255, 255))
    d.rectangle((3, 3, 12, 12), fill=(240, 250, 255, 255))
    d.rectangle((6, 6, 9, 9), fill=(255, 255, 255, 255))
    return im


def _core():
    """the heart's star: white-hot, gold at its tips"""
    S = 32; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); px = im.load()
    for y in range(S):
        for x in range(S):
            u = abs(x + 0.5 - S / 2) / (S / 2)
            v = abs(y + 0.5 - S / 2) / (S / 2)
            t = max(u, v)
            px[x, y] = (255, 255, int(255 - 80 * t), 255) if t < 0.55 else (255, int(236 - 60 * (t - 0.55)), int(150 - 90 * (t - 0.55)), 255)
    return im


def textures():
    T = {}
    for kind in ('table', 'crown', 'pav'):
        strip = Image.new('RGBA', (N, N * FRAMES))
        for f in range(FRAMES):
            strip.paste(swirl(f, kind), (0, f * N))
        T[f'cg_{kind}'] = strip
    T['cg_glint'] = _glint()
    T['cg_core'] = _core()
    for key, txt in EMOTES:
        T[f'cg_emo_{key}'] = emote_texture(txt)
    T.update(form_textures())
    return T


# ---------------------------------------------------------------------------------------------------- the face: text emoticons
# (key, text) - the head's faces, :) first (the plain head's)
EMOTES = [('smile', ':)'), ('cee', 'c:'), ('cat', ':3'), ('kiss', 'o3o'), ('caret', '^-^'), ('oh', ':o'), ('wink', ';)'), ('grin', ':D'),
          ('owo', 'owo'), ('heart', '<3'), ('cry', ';('), ('dee', 'D:'), ('sad', ':c'), ('tears', 'T_T'), ('angry', '>:('), ('shout', '>:o'),
          ('flat', ':|'), ('meh', '-_-'), ('zzz', 'zZz'), ('uu', 'u_u'), ('cheer', '\\o/'), ('stars', '*o*'),
          ('dots', 'o.o'), ('bigsmall', 'O.o'), ('smallbig', 'o.O'), ('oe', 'o.e')]
# a 5-row pixel font, just the marks the emoticons use ('#' lit)
FONT = {':': ['.', '#', '.', '#', '.'], ';': ['.', '#', '.', '#', '#'], ')': ['#.', '.#', '.#', '.#', '#.'], '(': ['.#', '#.', '#.', '#.', '.#'],
        '|': ['#', '#', '#', '#', '#'], 'o': ['...', '###', '#.#', '###', '...'], 'D': ['##.', '#.#', '#.#', '#.#', '##.'],
        '-': ['...', '...', '###', '...', '...'], '_': ['...', '...', '...', '...', '###'], 'z': ['....', '####', '..#.', '.#..', '####'],
        'Z': ['###', '..#', '.#.', '#..', '###'], 'u': ['...', '#.#', '#.#', '###', '...'], '\\': ['#..', '#..', '.#.', '..#', '..#'],
        '/': ['..#', '..#', '.#.', '#..', '#..'], '*': ['...', '#.#', '.#.', '#.#', '...'], '<': ['..#', '.#.', '#..', '.#.', '..#'],
        '>': ['#..', '.#.', '..#', '.#.', '#..'], '3': ['##.', '..#', '.#.', '..#', '##.'], 'c': ['...', '.##', '#..', '.##', '...'],
        '^': ['.#.', '#.#', '...', '...', '...'], 'w': ['.....', '#...#', '#.#.#', '.#.#.', '.....'], 'T': ['###', '.#.', '.#.', '.#.', '.#.'],
        '.': ['.', '.', '.', '.', '#'], 'O': ['###', '#.#', '#.#', '#.#', '###'], 'e': ['...', '.#.', '###', '#..', '.##']}
EMO_PX = 0.55                             # (units per texture pixel: 16 px -> an 8.8-unit plate - a face across the gem, readable from a few blocks off)


def emote_texture(txt, ink=(255, 255, 255, 255), edge=(34, 14, 52, 255)):
    """32 x 32: the emoticon in white (each font pixel 2 x 2), a thin dark outline round every mark, the rest clear
    (3.0a: ink / edge - the Wraithfire Form's are ghost-white on a soul-blue rim)"""
    cols = []
    for i, ch in enumerate(txt):
        g = FONT[ch]
        if i: cols.append(['.'] * 5)
        cols += [[row[x] for row in g] for x in range(len(g[0]))]
    S = 32
    w = len(cols) * 2; x0 = (S - w) // 2; y0 = (S - 10) // 2
    lit = {(x0 + 2 * x + i, y0 + 2 * y + j) for x, col in enumerate(cols) for y, c in enumerate(col) if c == '#' for i in (0, 1) for j in (0, 1)}
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); px = im.load()
    for (x, y) in lit:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if 0 <= x + dx < S and 0 <= y + dy < S and (x + dx, y + dy) not in lit:
                    px[x + dx, y + dy] = edge
    for (x, y) in lit:
        px[x, y] = ink
    return im


def face_elements(key, zt=ZT, tex='cg_emo_'):
    """the emoticon on its plate, just proud of the table, lit (zt: the table's height - a form's cut; tex: its emoticons' set)"""
    z = 8 + zt - 0.3
    h = 8 * EMO_PX
    return [{'from': [8 - h, 8 - h, z - 0.02], 'to': [8 + h, 8 + h, z + 0.02], 'light_emission': 15,
             'faces': {'north': {'uv': [0, 0, 16, 16], 'texture': f'#{tex}{key}'}}}]


# ---------------------------------------------------------------------------------------------------- models
def _euler(M):
    """M = Rz(c) Ry(b) Rx(a) -> (a, b, c) in degrees"""
    b = math.asin(max(-1, min(1, -M[2, 0])))
    a = math.atan2(M[2, 1], M[2, 2]); c = math.atan2(M[1, 0], M[0, 0])
    return math.degrees(a), math.degrees(b), math.degrees(c)


def plate(P0, P1, P2, P3, tex, t=0.12, out=None, spot=None):
    """a thin plate over the quad P0-P1 (outer edge) / P3-P2 (inner edge), its face toward `out` (heart-relative design units)"""
    P0, P1, P2, P3 = map(np.array, (P0, P1, P2, P3))
    u = P1 - P0; wid = (np.linalg.norm(P1 - P0) + np.linalg.norm(P2 - P3)) / 2 + 0.12; u /= np.linalg.norm(u)
    v = (P2 + P3) / 2 - (P0 + P1) / 2; v -= v.dot(u) * u; hei = np.linalg.norm(v) + 0.06; v /= np.linalg.norm(v)
    n = np.cross(u, v)
    c = (P0 + P1 + P2 + P3) / 4
    if out is not None and n.dot(out) < 0: u = -u; n = -n
    a, b, g = _euler(np.column_stack([u, v, n]))
    cw = c + O
    lo, hi = cw - [wid / 2, hei / 2, t / 2], cw + [wid / 2, hei / 2, t / 2]
    # (a cut stone's facets each catch one tone: one spot of the swirl, where it sits - and it turns with the swirl)
    sc = spot if spot is not None else c
    ux, uy = sc[0] * 1.15 + 8, 8 - sc[1] * 1.15
    s = 0.5
    uv = [round(max(0, ux - s / 2), 3), round(max(0, uy - s / 2), 3), round(min(16, ux + s / 2), 3), round(min(16, uy + s / 2), 3)]
    face = {'uv': uv, 'texture': f'#{tex}'}
    return {'from': [round(x, 4) for x in lo], 'to': [round(x, 4) for x in hi],
            'rotation': {'origin': [round(x, 4) for x in cw], 'x': round(a, 3), 'y': round(b, 3), 'z': round(g, 3)},
            'faces': {d: dict(face) for d in ('north', 'south', 'east', 'west', 'up', 'down')}}


def facet(P0, P1, P2, P3, tex, out, k=3, t=0.12):
    """a trapezoid facet as k strips across its slant, each as wide as its own slice; all one tone"""
    P0, P1, P2, P3 = map(np.array, (P0, P1, P2, P3))
    spot = (P0 + P1 + P2 + P3) / 4
    L = lambda a, b, f: a + (b - a) * f
    return [plate(L(P0, P3, j / k), L(P1, P2, j / k), L(P1, P2, (j + 1) / k), L(P0, P3, (j + 1) / k), tex, t=t, out=out, spot=spot) for j in range(k)]


def gem_elements(cut=None, tex=('cg_crown', 'cg_pav', 'cg_table'), rim=None, glow=0):
    """the stone. cut: (W, H, C, ZT, ZC) - the base gem's when None (3.0a: the forms' sharper, taller cuts: FORM_CUT);
    tex: its crown, pavilion and table textures; rim: (texture, light) for the girdle (else the crown's, unlit); glow: the
    table's light_emission (the forms' inner light)"""
    W_, H_, C_, ZT_, ZC_ = cut or (W, H, C, ZT, ZC)
    dims = (W_, H_, C_)
    tc, tp, tt = tex
    els = []
    g = octagon(dims=dims); tb = octagon(TK, dims); cu = octagon(0.14, dims)
    for i in range(8):
        j = (i + 1) % 8
        mid = np.array([(g[i][0] + g[j][0]) / 2, (g[i][1] + g[j][1]) / 2, 0.0])
        els += facet((*g[i], ZG), (*g[j], ZG), (*tb[j], ZT_), (*tb[i], ZT_), tc, out=mid + [0, 0, -3])       # the crown
        els += facet((*g[i], -ZG), (*g[j], -ZG), (*cu[j], ZC_), (*cu[i], ZC_), tp, out=mid + [0, 0, 3])      # the pavilion
        gp = plate((*g[i], -ZG), (*g[j], -ZG), (*g[j], ZG), (*g[i], ZG), rim[0] if rim else tc, t=0.1, out=mid)   # the girdle
        if rim and rim[1]: gp['light_emission'] = rim[1]
        els.append(gp)
    step = 0.5                                     # the table: flat, face-on, sliced in rows to the octagon
    y = -H_ * TK
    while y < H_ * TK - 1e-6:
        ym = y + step / 2
        xs = [x / 8 for x in range(-80, 81) if inside(x / 8, ym, TK, dims=dims)]
        if xs:
            x1, x2 = min(xs), max(xs)
            lo, hi = [8 + x1, 8 + y, 8 + ZT_ - 0.05], [8 + x2, 8 + y + step, 8 + ZT_ + 0.15]
            uv = [round(8 + x1, 3), round(8 - (y + step), 3), round(8 + x2, 3), round(8 - y, 3)]
            e = {'from': lo, 'to': hi, 'faces': {'south': {'uv': uv, 'texture': f'#{tt}'}, 'north': {'uv': uv, 'texture': f'#{tt}'}}}
            if glow: e['light_emission'] = glow
            els.append(e)
        y += step
    return els


def core_elements():
    """a four-pointed star of light standing just proud of the table, its heart lit (light_emission)"""
    z = 8 + ZT - 0.35
    els = []
    for w, h in ((1.5, 0.22), (0.22, 2.0)):          # (a tall four-pointed star: its long arm along the gem)
        els.append({'from': [8 - w, 8 - h, z - 0.04], 'to': [8 + w, 8 + h, z + 0.04], 'light_emission': 15,
                    'faces': {d: {'uv': [0, 0, 16, 16], 'texture': '#cg_core'} for d in ('north', 'south')}})
    els.append({'from': [8 - 0.45, 8 - 0.45, z - 0.06], 'to': [8 + 0.45, 8 + 0.45, z + 0.06], 'light_emission': 15,
                'rotation': {'origin': [8, 8, z], 'axis': 'z', 'angle': 45},
                'faces': {d: {'uv': [6, 6, 10, 10], 'texture': '#cg_core'} for d in ('north', 'south')}})
    return els


HALO_R, HALO_N = 9.0, 8


def halo_elements(r=HALO_R, n=HALO_N, tex=('cg_glint',), dy=0.0, k=1.0, light=12):
    """a ring of tiny facet glints round the gem's middle, each a little diamond (a cube stood on its point), at two heights
    (3.0a, the forms: wider round their wings, each glint its own texture in turn, k their size, dy the ring's rise)"""
    els = []
    for i in range(n):
        a = 2 * math.pi * i / n
        cx, cz = 8 + r * math.cos(a), 8 + r * math.sin(a)
        cy = 8 + dy + (1.4 if i % 2 else -1.4)
        s = (0.55 if i % 2 else 0.75) * k
        els.append({'from': [round(cx - s, 4), round(cy - s, 4), round(cz - s, 4)], 'to': [round(cx + s, 4), round(cy + s, 4), round(cz + s, 4)], 'light_emission': light,
                    'rotation': {'origin': [round(cx, 4), round(cy, 4), round(cz, 4)], 'x': 45.0, 'y': round(math.degrees(-a), 3), 'z': 35.0},
                    'faces': {d: {'uv': [0, 0, 16, 16], 'texture': f'#{tex[i % len(tex)]}'} for d in ('north', 'south', 'east', 'west', 'up', 'down')}})
    return els


def models():
    M = {}

    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)
    part('cg_body', gem_elements())
    part('cg_head', face_elements('smile'))
    for key, _t in EMOTES[1:]:
        part(f'cg_head_x{key}', face_elements(key))
    part('cg_halo', halo_elements())
    for p_ in WINGS:                                   # (3.0a: the wings - nothing to see in its own form, a speck at the joint)
        part(f'cg_{p_}', [{'from': [7.99, 7.99, 7.99], 'to': [8.01, 8.01, 8.01], 'faces': {'north': {'uv': [0, 0, 1, 1], 'texture': '#cg_glint'}}}])
    for name, els in form_models().items():
        part(name, els)
    return M


# ---------------------------------------------------------------------------------------------------- poses
# (it only floats: the gem tilts and turns, the whole rises and sinks (_off), the halo ring turns on its own (its glints travel
#  round as the poses go by); "dim" poses hide its star and its halo)
def P(**kw):
    return kw


def spin(deg):
    return qs(('y', deg))


def glide(k, lean):
    """a gliding frame: leaning into the way it goes (its top forward), a bob, the halo a step further round"""
    s = math.sin(math.pi * k / 2)
    return P(body=qs(('x', lean), ('z', 4 * s)), halo=spin(22.5 * k), _off=(0, 0.6 * abs(math.cos(math.pi * k / 2)), 0))


POSES = {
    'idle_a': P(body=qs(('y', -12)), halo=spin(0)),
    'idle_b': P(body=qs(('y', 12), ('z', 3)), halo=spin(22.5), _off=(0, 0.9, 0)),
    **{f'walk_{k}': glide(k, 14) for k in range(4)},
    **{f'run_{k}': glide(k, 26) for k in range(4)},
    'jump': P(body=qs(('y', 30), ('x', -8)), halo=spin(45), _off=(0, 4.0, 0)),
    # resting low, its light gone dim
    'sit_a': P(body=qs(('x', -6)), halo=spin(0), _off=(0, -8.0, 0), _dim=True),
    # balanced on its point, turning slowly (the cycle steps it round)
    'sit_b': P(body=qs(('y', 45), ('z', 6)), halo=spin(11.25), _off=(0, -11.6, 0)),
    'sit_c': P(body=qs(('y', 135), ('z', -6)), halo=spin(33.75), _off=(0, -11.6, 0)),
    # a twirl - all the way round, up on its toes
    'happy': P(body=qs(('y', 180), ('z', 8)), halo=spin(67.5), _off=(0, 2.5, 0)),
    # conjuring a Buddy: rising, the crown tipped up - then flaring forward, the halo flung round
    'conjure_up': P(body=qs(('x', -18)), halo=spin(30), _off=(0, 3.0, 0)),
    'conjure': P(body=qs(('x', 12), ('y', 8)), halo=spin(110), _off=(0, 5.0, 0)),
    # knocked: a tilt and a jolt
    'hurt': P(body=qs(('z', 26), ('x', -12)), halo=spin(5), _off=(0.8, -1.0, 0)),
    # tired: sinking, lolling, its light dim
    'tired': P(body=qs(('x', 30), ('z', -12)), halo=spin(0), _off=(0, -6.0, 0), _dim=True),
}
for _i in range(SWIM_FRAMES):                      # (bobbing on the water, rocking, the halo turning)
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(body=qs(('x', 8 + 5 * math.sin(_p)), ('z', 6 * math.cos(_p))), halo=spin(45 * _i), _off=(0, -3.0 + 1.2 * math.sin(_p), 0))

# (3.0a) the halo is no longer posed. phase231 turns it round the gem all the time instead: a step of its right_rotation every
#  few ticks, interpolated, so the glints (the white squares) circle it without stopping. A pose's own turn of the ring swung it
#  back and forth (idle_a 0 deg, idle_b 22.5 deg...). The ring now stays level at rest and rides each pose's rise and sink (_off).
HALO_TURN = 120                                    # (ticks for one full turn of the halo)
for _p in POSES.values():
    _p.pop('halo', None)

DRAFT = ['idle_a', 'idle_b', 'walk_1', 'run_1', 'jump', 'sit_a', 'sit_b', 'sit_c', 'happy', 'conjure_up', 'conjure', 'hurt', 'tired', 'swim_2']


# ==================================================================================================== (3.0a) ITS TWO FORMS
# Handed the ETHEREAL GEM (the nine made whole - the stone it was cut from), or the WRAITHFIRE HEART (that stone's light quenching a
# Scorching Heart), the Gem takes on a form (phase231: '_e' / '_w', every part's twin). Both are the same sharper, taller cut (FORM_CUT:
# a longer octagon, a higher crown, a deeper pavilion, its point where the plain gem's is - DY lifts its heart), a crown of points on
# top and WINGS at its back (wing_r / wing_l: a speck in its own form). Its face is its emoticons still - every one, on the new table.
#   ETHEREAL '_e'   the swirl of every colour (the plain gem's own textures: a look recolours it as it does the plain gem), its table lit
#                   from within, a girdle of pale prismatic light, a crown of five crystal points, and DIAMOND WINGS - five faceted
#                   shards a side, ruby, topaz, emerald, sapphire, amethyst (cg_ew_*: a look's palette, through phase138's SIDE), lit
#                   modestly; its halo twelve glints in those colours.
#   WRAITHFIRE '_w' smoky dark glass with soul-blue veins drifting in it (animated), a girdle and a crown of cyan wraith fire
#                   (animated flicker), FLAME-WISP wings, its halo soul-fire motes; its emoticons ghost-white on a soul-blue rim.
#                   (Its own colours: a form outranks a look, as Apophiss's do.)
# A form's halo circles OVER its crown (HALO_UP, HALO_RF) - round its middle it would cut through its wings - clear of every point and
# wing in every pose (tools/preview/gem_forms.py clip checks it, the ring all the way round).
import rigkit as _RK

FORMS = ('_e', '_w')
FORM_CUT = (5.4, 9.0, 2.9, -2.5, 4.3)            # (W, H, C, ZT, ZC)
DY = FORM_CUT[1] - H                             # (2.0: its heart lifted, so its point hovers where the plain gem's does)
HALO_RF, HALO_UP = 7.0, 20.0                     # (a form's halo: over its crown, clear of every point and wing in every pose)
GEMS5 = (('ruby', (214, 30, 66)), ('topaz', (255, 172, 34)), ('emerald', (34, 206, 108)), ('sapphire', (40, 98, 232)), ('amethyst', (164, 70, 232)))
LOOK_SIDE = tuple(f'cg_ew_{k}' for k, _c in GEMS5) + ('cg_e_spike',)       # (phase231 hands these to phase138: recoloured on the swirl's range)
# THE WING (his right; in its own plane - u out from the joint, v up - swept back SWEEP_Z for each unit out): a crystal ARM, the leading
# edge, out and up to the wrist, and five long BLADES like a bird's feathers - the outer two from the wrist, the inner three from
# along the arm - overlapping into one wing; rainbow from the top: ruby, topaz, emerald, sapphire, amethyst
ARM = ((0.0, 0.0), (4.0, 3.6), (7.5, 6.5))
FEATHERS = (((7.0, 6.2), (15.5, 11.0), 5.2), ((7.2, 5.6), (16.6, 3.8), 5.6), ((5.4, 4.6), (13.2, -2.8), 5.6),
            ((3.2, 2.8), (9.2, -5.8), 5.0), ((1.2, 1.0), (4.8, -6.4), 4.0))
SWEEP_Z = 0.42                                   # (back, for each unit out)
# the crown's points (x, drop below the top, lean (deg, outward), length)
POINTS = ((0.0, 0.0, 0.0, 6.0), (1.7, 0.15, 13.0, 4.4), (-1.7, 0.15, -13.0, 4.4), (3.5, 1.5, 33.0, 3.3), (-3.5, 1.5, -33.0, 3.3))
FULL = {d: [0, 0, 16, 16] for d in ('north', 'south', 'east', 'west', 'up', 'down')}


def _u(v):
    n = math.sqrt(sum(c * c for c in v)); return tuple(c / n for c in v)


def _box(A, B, w, tex, light=0, diamond=True, ext=0.12):
    """a w-by-w box from A to B (part-relative design units: model = 8 + them), turned on its long axis to a diamond's cross-section"""
    d = tuple(B[i] - A[i] for i in range(3))
    x, y, z = _RK.frame(d, (0.0, 1.0, 0.0))
    if diamond:
        up = _u(tuple(x[i] + y[i] for i in range(3)))
        x, y, z = _RK.frame(d, up)
    L = math.sqrt(sum(c * c for c in d)) / 2 + ext
    m = tuple((A[i] + B[i]) / 2 for i in range(3))
    ang = _RK.euler([[x[0], y[0], z[0]], [x[1], y[1], z[1]], [x[2], y[2], z[2]]])
    fr, to = (m[0] - w / 2, m[1] - w / 2, m[2] - L), (m[0] + w / 2, m[1] + w / 2, m[2] + L)
    return _RK.el(fr, to, tex, (0.0, 0.0, 0.0), None if max(abs(v) for v in ang) < 1e-3 else (ang, m), uv=FULL, light=light)


def crystal(A, B, w, tex, light=0, tip_light=None):
    """a tapered crystal from A to its point at B: four boxes narrowing to a sharp tip"""
    P = lambda t: tuple(A[i] + (B[i] - A[i]) * t for i in range(3))
    steps = ((0.0, 0.42, 1.0), (0.38, 0.72, 0.74), (0.68, 0.9, 0.46), (0.86, 1.0, 0.2))
    return [_box(P(a), P(b), w * k, tex, light if b < 1.0 else (tip_light or light)) for a, b, k in steps]


def _slab(A, B, w, t, n, tex, light=0, ext=0.1):
    """a flat slab from A to B, w across (in the wing's plane) and t thick (along n, the plane's normal)"""
    d = tuple(B[i] - A[i] for i in range(3))
    x, y, z = _RK.frame(d, n)
    L = math.sqrt(sum(c * c for c in d)) / 2 + ext
    m = tuple((A[i] + B[i]) / 2 for i in range(3))
    ang = _RK.euler([[x[0], y[0], z[0]], [x[1], y[1], z[1]], [x[2], y[2], z[2]]])
    fr, to = (m[0] - w / 2, m[1] - t / 2, m[2] - L), (m[0] + w / 2, m[1] + t / 2, m[2] + L)
    return _RK.el(fr, to, tex, (0.0, 0.0, 0.0), None if max(abs(v) for v in ang) < 1e-3 else (ang, m), uv=FULL, light=light)


def blade(pts, w, n, tex, light, tip_light=None, t=0.7):
    """a crystal blade (or a flame's feather) along pts: flat in the wing's plane, narrowing to its point, its spine raised"""
    k = len(pts) - 1
    out = []
    for i in range(k):
        f = 1 - 0.7 * i / max(1, k - 1)
        out.append(_slab(pts[i], pts[i + 1], w * f, t, n, tex, light if i < k - 1 else (tip_light or light), ext=0.14))
        if i < k - 1:                                  # (the spine: a ridge down its middle, catching the light)
            out.append(_slab(pts[i], pts[i + 1], w * f * 0.2, t * 1.7, n, tex, (tip_light or light)))
    return out


def _dir(elev, side):
    e = math.radians(elev)
    return _u((side * math.cos(e), math.sin(e), SWEEP_Z))


def _plane(side):
    """the wing's plane: o (out, swept back), up, and its normal"""
    o = _u((side * 1.0, 0.0, SWEEP_Z)); u = (0.0, 1.0, 0.0)
    n = _u((o[1] * u[2] - o[2] * u[1], o[2] * u[0] - o[0] * u[2], o[0] * u[1] - o[1] * u[0]))
    return o, u, n


def wing_elements(form, side=1):
    """a wing (side 1: his right, +x; -1: his left), from its joint: diamond blades ('_e') or feathers of wraith fire ('_w')"""
    o, up, n = _plane(side)
    W3 = lambda uv, lift=0.0: tuple(o[i] * uv[0] + up[i] * uv[1] + n[i] * lift for i in range(3))
    e = form == '_e'
    els = []
    for (a, b, w), (k, _c) in zip(FEATHERS, GEMS5):
        pts = []
        for f in (0.0, 0.35, 0.65, 0.86, 1.0):
            u_ = (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
            if not e: u_ = (u_[0], u_[1] + 2.2 * f * f)                    # (a flame's feather curls up at its tip)
            pts.append(W3(u_, -0.15 - 0.12 * len(els) / 9))               # (just behind the arm, each a little behind the last)
        els += blade(pts, w, n, f'cg_ew_{k}' if e else 'cg_wf_flame', 7 if e else 12, 11 if e else 15, t=0.45)
    arm = [W3(p, 0.2) for p in ARM]
    for i in range(len(arm) - 1):                                          # (the arm: the leading edge, in front of the blades)
        els.append(_box(arm[i], arm[i + 1], 1.9 - 0.4 * i, 'cg_e_spike' if e else 'cg_wf_flame', 9 if e else 14, ext=0.3))
    els.append(_box(W3((-0.4, -0.6), 0.2), W3((0.9, 0.7), 0.2), 2.4, 'cg_e_spike' if e else 'cg_wf_flame', 10 if e else 14))   # (the knot at its root)
    return els


def crown_elements(form):
    """the points on its top: crystal ('_e') or wraith fire ('_w') - body-relative (its heart at DY)"""
    Wf, Hf, Cf = FORM_CUT[:3]
    els = []
    for x, drop, lean, L in POINTS:
        y0 = DY + (Hf if abs(x) <= Wf - Cf else Hf - Cf * 1.2 * (abs(x) - (Wf - Cf)) / Cf) - drop - 0.6
        a = math.radians(lean)
        A0, B0 = (x, y0, 0.0), (x + math.sin(a) * L, y0 + math.cos(a) * L, 0.0)
        if form == '_e':
            els += crystal(A0, B0, 1.5 if x == 0 else 1.2, 'cg_e_spike', light=9, tip_light=12)
        else:
            mid = ((A0[0] + B0[0]) / 2 + 0.35 * (1 if x >= 0 else -1), (A0[1] + B0[1]) / 2, 0.0)
            els += [_box(A0, mid, 2.2 if x == 0 else 1.8, 'cg_wf_flame', 15, ext=0.2), _box(mid, B0, 1.3 if x == 0 else 1.0, 'cg_wf_flame', 15, ext=0.2)]
    return els


def _lift(els):
    return _RK.transform(els, lambda v: [v[0], v[1] + DY, v[2]])


def form_models():
    M = {}
    cut = FORM_CUT
    for f in FORMS:
        e = f == '_e'
        body = gem_elements(cut, tex=('cg_crown', 'cg_pav', 'cg_table') if e else ('cg_w_crown', 'cg_w_pav', 'cg_w_table'),
                            rim=('cg_e_spike', 9) if e else ('cg_wf_flame', 12), glow=6 if e else 8)
        M[f'cg_body{f}'] = _lift(body) + [dict(el) for el in _RK.transform(crown_elements(f), lambda v: v)]
        ft = 'cg_emo_' if e else 'cg_emw_'
        M[f'cg_head{f}'] = _lift(face_elements('smile', cut[3], ft))
        for key, _t in EMOTES[1:]:
            M[f'cg_head_x{key}{f}'] = _lift(face_elements(key, cut[3], ft))
        M[f'cg_halo{f}'] = halo_elements(HALO_RF, 12 if e else 10, tuple(f'cg_ew_{k}' for k, _c in GEMS5) + ('cg_e_spike',) if e else ('cg_w_glint',),
                                         dy=HALO_UP, k=1.0, light=13 if e else 15)
        M[f'cg_wing_r{f}'] = wing_elements(f, 1)
        M[f'cg_wing_l{f}'] = wing_elements(f, -1)
    return M


# ---------------------------------------------------------------------------------------------------- the forms' textures
def _shard(rgb):
    """a gem shard's facet: lit down one side, a white streak of light, a glint or two"""
    im = Image.new('RGBA', (16, 16)); px = im.load()
    for y in range(16):
        for x in range(16):
            d = abs(x - 7.5) / 8
            v = 1.08 - 0.5 * d + (0.14 if x < 8 else -0.06) + 0.06 * math.sin(y * 0.9)
            c = [min(255, int(rgb[i] * v)) for i in range(3)]
            if x in (5, 6): c = [int(c[i] * 0.45 + 255 * 0.55) for i in range(3)]
            if x in (0, 15) or y in (0, 15): c = [int(v_ * 0.62) for v_ in c]
            px[x, y] = (*c, 255)
    for x, y in ((5, 3), (10, 11), (9, 4)):
        px[x, y] = (255, 255, 255, 255)
    return im


def _spike():
    """pale prismatic crystal: white light, every colour faint along its facets"""
    im = Image.new('RGBA', (16, 16)); px = im.load()
    for y in range(16):
        for x in range(16):
            h = ((x + y) / 22.0) % 1.0
            r, g, b = colorsys.hsv_to_rgb(h, 0.26 - 0.12 * (1 - abs(x - 7.5) / 8), 1.0)
            k = 0.9 + 0.1 * (1 - abs(x - 7.5) / 8)
            px[x, y] = (int(r * 255 * k), int(g * 255 * k), int(b * 255 * k), 255)
    for x, y in ((4, 4), (11, 9), (6, 12)):
        px[x, y] = (255, 255, 255, 255)
    return im


SOUL_RGB = np.array([110, 240, 255], float)      # (the pack's wraithfire: Cecil's cec_eye_wraith)


def _smoke(f, kind):
    """one frame of the Wraithfire Form's facets: dark smoky glass, soul-blue veins drifting up through it (loops in FRAMES)"""
    t = 2 * math.pi * f / FRAMES
    ys, xs = np.mgrid[0:N, 0:N].astype(float)
    X = (xs + 0.5) / N * 2 - 1; Y = 1 - (ys + 0.5) / N * 2
    smoke = 0.5 + 0.25 * np.sin(3.1 * X + 2.2 * np.sin(2.0 * Y - t)) + 0.25 * np.sin(2.6 * Y + 1.4 * X - 2 * t)
    vein = np.exp(-(np.sin(3.6 * X + 2.4 * np.sin(1.8 * Y - t) + 2.2 * Y - t) ** 2) / 0.035)
    vein2 = np.exp(-(np.sin(5.1 * Y - 1.7 * X + 1.3 * np.sin(2.6 * X + t) + 2 * t) ** 2) / 0.02)
    dark = np.array([14, 26, 38], float); mid = np.array([36, 72, 92], float)
    c = dark[None, None] + (mid - dark)[None, None] * smoke[..., None]
    k_v = {'table': 0.95, 'crown': 0.9, 'pav': 0.75}[kind]
    v = np.clip(vein * k_v + vein2 * k_v * 0.55, 0, 1)[..., None]
    if kind == 'table':                         # (a ghost flame at its heart, rising)
        r = np.sqrt((X * 1.6) ** 2 + ((Y + 0.25) * 1.0) ** 2)
        flame = np.clip(1.0 - r * (1.35 + 0.25 * np.sin(6 * Y - 2 * t)), 0, 1)[..., None] * 0.7
        v = np.clip(v + flame, 0, 1)
    c = c * (1 - v) + SOUL_RGB[None, None] * v
    c = np.where(v > 0.85, c * 0.4 + 255 * 0.6, c)
    a = np.full((N, N, 1), 255.0)
    return Image.fromarray(np.concatenate([np.clip(c, 0, 255), a], axis=2).astype(np.uint8), 'RGBA')


def _flame(f):
    """a frame of wraith fire: white-cyan at its root, teal toward its tips, tongues flickering up (loops in FRAMES)"""
    t = 2 * math.pi * f / FRAMES
    ys, xs = np.mgrid[0:N, 0:N].astype(float)
    X = (xs + 0.5) / N * 2 - 1; Y01 = 1 - (ys + 0.5) / N
    I = (1.2 - Y01) * (0.8 + 0.2 * np.sin(5 * X + 2 * t)) + 0.22 * np.sin(9 * Y01 - 3 * t + 2.5 * X) * (1 - np.abs(X) * 0.6)
    I = I - 0.3 * np.abs(X) ** 2
    stops = [(0.78, (236, 255, 255)), (0.55, (140, 246, 255)), (0.34, (46, 196, 232)), (-9, (18, 104, 140))]
    out = np.zeros((N, N, 3))
    done = np.zeros((N, N), bool)
    for lv, col in stops:
        m = (I > lv) & ~done
        out[m] = col; done |= m
    a = np.full((N, N, 1), 255.0)
    return Image.fromarray(np.concatenate([out, a], axis=2).astype(np.uint8), 'RGBA')


def _mote():
    im = Image.new('RGBA', (16, 16)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 15, 15), fill=(30, 150, 200, 255)); d.rectangle((3, 3, 12, 12), fill=(110, 240, 255, 255)); d.rectangle((6, 6, 9, 9), fill=(232, 255, 255, 255))
    return im


def form_textures():
    T = {}
    for k, rgb in GEMS5:
        T[f'cg_ew_{k}'] = _shard(rgb)
    T['cg_e_spike'] = _spike()
    for kind in ('table', 'crown', 'pav'):
        strip = Image.new('RGBA', (N, N * FRAMES))
        for f in range(FRAMES):
            strip.paste(_smoke(f, kind), (0, f * N))
        T[f'cg_w_{kind}'] = strip
    strip = Image.new('RGBA', (N, N * FRAMES))
    for f in range(FRAMES):
        strip.paste(_flame(f), (0, f * N))
    T['cg_wf_flame'] = strip
    T['cg_w_glint'] = _mote()
    for key, txt in EMOTES:
        T[f'cg_emw_{key}'] = emote_texture(txt, ink=(226, 255, 255, 255), edge=(14, 116, 148, 255))
    return T


# ---------------------------------------------------------------------------------------------------- the wings' poses
# (lift: up from rest about the gem's front-back line; sweep: back from rest about the vertical. Parented to the gem, they tilt and
#  turn with it. They never droop below rest - a lowered wing would cross the halo's ring - so a tired or seated Gem folds them
#  BACK instead. idle_a / idle_b are a slow beat of them, a second each.)
def wingpose(lift, sweep):
    r = qs(('y', -sweep), ('z', lift))
    return {'wing_r': r, 'wing_l': (r[0], -r[1], -r[2], r[3])}          # (mirrored across his middle)


WING_POSE = {'idle_a': (0, 0), 'idle_b': (12, -6), 'jump': (24, -14), 'sit_a': (0, 44), 'sit_b': (2, 30), 'sit_c': (2, 30), 'happy': (20, -16),
             'conjure_up': (26, 8), 'conjure': (16, -24), 'hurt': (0, 36), 'tired': (0, 46)}
WING_POSE.update({f'walk_{k}': (5 + 5 * math.sin(math.pi * k / 2), 18) for k in range(4)})
WING_POSE.update({f'run_{k}': (4 + 8 * math.sin(math.pi * k / 2), 34) for k in range(4)})
WING_POSE.update({f'swim_{k}': (6 + 6 * math.sin(2 * math.pi * k / SWIM_FRAMES), 24) for k in range(SWIM_FRAMES)})
for _n, _p in POSES.items():
    _p.update(wingpose(*WING_POSE.get(_n, (0, 0))))

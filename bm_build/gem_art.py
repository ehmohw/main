"""2.96: THE GEM OF CREATIVITY, the follower - the approved mockup (mockups/creativity_gem.py) as a rigkit rig.

The shard of the Ethereal Gem that gives the Buddies life: an elongated octagon cut as a real stone - an octagonal GIRDLE, a flat
TABLE, eight sloped CROWN facets and a deeper PAVILION narrowing to the culet, each facet a thin plate at its true angle (26.x
elements turn on all three axes) so the light catches each one differently. Every colour of the rainbow swirls out of a pale heart,
little white doodles (notes, flowers, sparkles) drifting inside it: the swirl is an ANIMATED texture (32 frames, interpolated).

Its face is a text emoticon, lit on its table facet (2.96a - it floated over it before): :) c: :o :3 o3o ^-^ ;( and the rest
(EMOTES), each a little pixel-font plate (FONT) standing just proud of the table, glowing white with a dark outline so it reads
over every colour of the swirl. The plain head (cg_head) is :) ; cg_head_x<key> each of the others (phase231 picks them by mood).
It floats - its poses only move, tilt and spin it. Parts: the GEM (body); its FACE on the table (hidden when it's dim); its HALO,
a ring of tiny facet glints orbiting it (each pose turns the ring - the glints travel round as it glides).

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
PIVOT = {'body': (0, 19.0, 0), 'head': (0, 19.0, 0), 'halo': (0, 19.0, 0)}
PARENT = {'body': None, 'head': 'body', 'halo': None}
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


def write_mcmeta(R2):
    """(the follower phase's rp post) the swirl's animation, beside each strip"""
    for k, meta in ANIMATED.items():
        R2.wj(f'assets/bm/textures/block/{k}.png.mcmeta', meta)


def HIDDEN(p, pose):
    return p in ('head', 'halo') and pose.get('_dim', False)


def model_name(p, pose, suffix=''):
    return f'{PREFIX}{p}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def octagon(s=1.0):
    w, h, c = W * s, H * s, C * s
    return [(-w, -(h - c * 1.2)), (-w, h - c * 1.2), (-(w - c), h), (w - c, h), (w, h - c * 1.2), (w, -(h - c * 1.2)), (w - c, -h), (-(w - c), -h)]


def inside(x, y, s=1.0, pad=0.0):
    w, h, c = W * s - pad, H * s - pad, C * s
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


def emote_texture(txt):
    """32 x 32: the emoticon in white (each font pixel 2 x 2), a thin dark outline round every mark, the rest clear"""
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
                    px[x + dx, y + dy] = (34, 14, 52, 255)
    for (x, y) in lit:
        px[x, y] = (255, 255, 255, 255)
    return im


def face_elements(key):
    """the emoticon on its plate, just proud of the table, lit"""
    z = 8 + ZT - 0.3
    h = 8 * EMO_PX
    return [{'from': [8 - h, 8 - h, z - 0.02], 'to': [8 + h, 8 + h, z + 0.02], 'light_emission': 15,
             'faces': {'north': {'uv': [0, 0, 16, 16], 'texture': f'#cg_emo_{key}'}}}]


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


def gem_elements():
    els = []
    g = octagon(); tb = octagon(TK); cu = octagon(0.14)
    for i in range(8):
        j = (i + 1) % 8
        mid = np.array([(g[i][0] + g[j][0]) / 2, (g[i][1] + g[j][1]) / 2, 0.0])
        els += facet((*g[i], ZG), (*g[j], ZG), (*tb[j], ZT), (*tb[i], ZT), 'cg_crown', out=mid + [0, 0, -3])       # the crown
        els += facet((*g[i], -ZG), (*g[j], -ZG), (*cu[j], ZC), (*cu[i], ZC), 'cg_pav', out=mid + [0, 0, 3])         # the pavilion
        els.append(plate((*g[i], -ZG), (*g[j], -ZG), (*g[j], ZG), (*g[i], ZG), 'cg_crown', t=0.1, out=mid))       # the girdle
    step = 0.5                                     # the table: flat, face-on, sliced in rows to the octagon
    y = -H * TK
    while y < H * TK - 1e-6:
        ym = y + step / 2
        xs = [x / 8 for x in range(-80, 81) if inside(x / 8, ym, TK)]
        if xs:
            x1, x2 = min(xs), max(xs)
            lo, hi = [8 + x1, 8 + y, 8 + ZT - 0.05], [8 + x2, 8 + y + step, 8 + ZT + 0.15]
            uv = [8 + x1, 8 - (y + step), 8 + x2, 8 - y]
            els.append({'from': lo, 'to': hi, 'faces': {'south': {'uv': uv, 'texture': '#cg_table'}, 'north': {'uv': uv, 'texture': '#cg_table'}}})
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


def halo_elements():
    """a ring of tiny facet glints round the gem's middle, each a little diamond (a cube stood on its point), at two heights"""
    els = []
    for i in range(HALO_N):
        a = 2 * math.pi * i / HALO_N
        cx, cz = 8 + HALO_R * math.cos(a), 8 + HALO_R * math.sin(a)
        cy = 8 + (1.4 if i % 2 else -1.4)
        s = 0.55 if i % 2 else 0.75
        els.append({'from': [cx - s, cy - s, cz - s], 'to': [cx + s, cy + s, cz + s], 'light_emission': 12,
                    'rotation': {'origin': [cx, cy, cz], 'x': 45.0, 'y': round(math.degrees(-a), 3), 'z': 35.0},
                    'faces': {d: {'uv': [0, 0, 16, 16], 'texture': '#cg_glint'} for d in ('north', 'south', 'east', 'west', 'up', 'down')}})
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

DRAFT = ['idle_a', 'idle_b', 'walk_1', 'run_1', 'jump', 'sit_a', 'sit_b', 'sit_c', 'happy', 'conjure_up', 'conjure', 'hurt', 'tired', 'swim_2']

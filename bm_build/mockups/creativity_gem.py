"""2.95: THE GEM OF CREATIVITY - the shard of the Ethereal Gem that broke away and gives the Buddies life (the owner's art: an
elongated octagon, every colour of the rainbow swirling out of a pale heart, little white doodles - notes, flowers, sparkles -
drifting inside it).

A real cut, not a slab: an octagonal GIRDLE, a flat TABLE, eight sloped CROWN facets between them, and a deeper PAVILION of
eight facets narrowing behind to the culet - each facet a thin plate set at its true angle (26.x elements turn on all three
axes, Rz Ry Rx), so the game's own light catches each one differently. The swirl is ANIMATED (32 frames, interpolated): the
colours turn slowly round the heart, the table's doodles drifting with them; the crown a little paler, the pavilion deeper.

    python3 mockups/creativity_gem.py OUT_RP     writes assets/bm/{models,textures}/item/creativity_gem* into OUT_RP"""
import colorsys, json, math, os, sys
import numpy as np
from PIL import Image

N = 64                                    # texture px across the 16-unit face
FRAMES = 32
W, H, C = 5.0, 7.0, 2.2                   # the girdle: half width, half height, the corners' cut
TK = 0.5                                  # the table, as a share of the girdle
ZG, ZT, ZC = -0.35, -1.9, 3.3             # the girdle's half thickness, the table's height, the culet's depth (the crown toward -z:
                                          #  a displayed item shows its north side to the one facing it)
O = np.array([8.0, 8.0, 8.0])


def octagon(s=1.0):
    w, h, c = W * s, H * s, C * s
    return [(-w, -(h - c * 1.2)), (-w, h - c * 1.2), (-(w - c), h), (w - c, h), (w, h - c * 1.2), (w, -(h - c * 1.2)), (w - c, -h), (-(w - c), -h)]


def inside(x, y, s=1.0, pad=0.0):
    """is (x, y) (offsets from the centre) inside the octagon at scale s"""
    w, h, c = W * s - pad, H * s - pad, C * s
    if abs(x) > w or abs(y) > h: return False
    return (abs(x) - (w - c)) / c + (abs(y) - (h - c * 1.2)) / (c * 1.2) <= 1.0


def swirl(f, kind):
    """one frame of the swirl: the hue turning round the heart (f / FRAMES of a turn)"""
    im = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    ph = f / FRAMES
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
            im.putpixel((px, py), (int(rr * 255), int(gg * 255), int(bb * 255), 255))
    if kind == 'table':                   # the doodles, drifting round with the colours
        Wt = (255, 255, 255, 255)
        glyphs = {'note': ['.##', '.#.', '.#.', '##.', '##.'], 'flower': ['.#.', '###', '.#.'], 'spark': ['.#.', '#.#', '.#.'], 'dot': ['#']}
        for i, (g, rad, a0) in enumerate((('note', 0.22, 0.0), ('flower', 0.30, 0.25), ('spark', 0.12, 0.5), ('note', 0.32, 0.62),
                                          ('spark', 0.26, 0.85), ('dot', 0.05, 0.4), ('flower', 0.15, 0.75))):
            a = 2 * math.pi * (a0 - ph * 0.5)
            cx = int(N / 2 + math.cos(a) * rad * N * W / 8); cy = int(N / 2 - math.sin(a) * rad * N * H / 8)
            for j, row in enumerate(glyphs[g]):
                for k, ch in enumerate(row):
                    if ch == '#' and 0 <= cx + k < N and 0 <= cy + j < N: im.putpixel((cx + k, cy + j), Wt)
    return im


def textures():
    T = {}
    for kind in ('table', 'crown', 'pav'):
        strip = Image.new('RGBA', (N, N * FRAMES))
        for f in range(FRAMES): strip.paste(swirl(f, kind), (0, f * N))
        T[f'creativity_gem_{kind}'] = strip
    return T


def euler(M):
    """M = Rz(c) Ry(b) Rx(a) -> (a, b, c) in degrees"""
    b = math.asin(max(-1, min(1, -M[2, 0])))
    a = math.atan2(M[2, 1], M[2, 2]); c = math.atan2(M[1, 0], M[0, 0])
    return math.degrees(a), math.degrees(b), math.degrees(c)


def plate(P0, P1, P2, P3, tex, t=0.12, out=None, spot=None):
    """a thin plate over the quad P0-P1 (outer edge) / P3-P2 (inner edge), its face toward `out`"""
    P0, P1, P2, P3 = map(np.array, (P0, P1, P2, P3))
    u = P1 - P0; wid = (np.linalg.norm(P1 - P0) + np.linalg.norm(P2 - P3)) / 2 + 0.12; u /= np.linalg.norm(u)
    v = (P2 + P3) / 2 - (P0 + P1) / 2; v -= v.dot(u) * u; hei = np.linalg.norm(v) + 0.06; v /= np.linalg.norm(v)
    n = np.cross(u, v)
    c = (P0 + P1 + P2 + P3) / 4
    if out is not None and n.dot(out) < 0: u = -u; n = -n
    a, b, g = euler(np.column_stack([u, v, n]))
    cw = c + O
    lo, hi = cw - [wid / 2, hei / 2, t / 2], cw + [wid / 2, hei / 2, t / 2]
    # (its colour: one spot of the swirl where it sits, face-on - a cut stone's facets each catch one tone, and it turns with the swirl)
    sc = spot if spot is not None else c
    ux, uy = sc[0] * 1.15 + 8, 8 - sc[1] * 1.15
    s = 0.5
    uv = [round(max(0, ux - s / 2), 3), round(max(0, uy - s / 2), 3), round(min(16, ux + s / 2), 3), round(min(16, uy + s / 2), 3)]
    face = {'uv': uv, 'texture': f'#{tex}'}
    return {'from': [round(x, 4) for x in lo], 'to': [round(x, 4) for x in hi],
            'rotation': {'origin': [round(x, 4) for x in cw], 'x': round(a, 3), 'y': round(b, 3), 'z': round(g, 3)},
            'faces': {d: dict(face) for d in ('north', 'south', 'east', 'west', 'up', 'down')}}


def facet(P0, P1, P2, P3, tex, out, k=3, t=0.12):
    """a trapezoid facet as k strips across its slant, each as wide as its own slice (a rectangle can't follow a trapezoid);
    all one tone - the facet's own spot of the swirl"""
    P0, P1, P2, P3 = map(np.array, (P0, P1, P2, P3))
    spot = (P0 + P1 + P2 + P3) / 4
    L = lambda a, b, f: a + (b - a) * f
    return [plate(L(P0, P3, j / k), L(P1, P2, j / k), L(P1, P2, (j + 1) / k), L(P0, P3, (j + 1) / k), tex, t=t, out=out, spot=spot) for j in range(k)]


def model():
    els = []
    g = octagon(); tb = octagon(TK); cu = octagon(0.14)
    for i in range(8):
        j = (i + 1) % 8
        mid = np.array([(g[i][0] + g[j][0]) / 2, (g[i][1] + g[j][1]) / 2, 0.0])
        # the crown: girdle edge (front rim) up to the table's edge
        els += facet((*g[i], ZG), (*g[j], ZG), (*tb[j], ZT), (*tb[i], ZT), 'crown', out=mid + [0, 0, -3])
        # the pavilion: girdle edge (back rim) down to the culet
        els += facet((*g[i], -ZG), (*g[j], -ZG), (*cu[j], ZC), (*cu[i], ZC), 'pav', out=mid + [0, 0, 3])
        # the girdle: a band round the widest part
        els.append(plate((*g[i], -ZG), (*g[j], -ZG), (*g[j], ZG), (*g[i], ZG), 'crown', t=0.1, out=mid))
    # the table: flat, face-on, sliced in rows to the octagon
    step = 0.5
    y = -H * TK
    while y < H * TK - 1e-6:
        ym = y + step / 2
        xs = [x / 8 for x in range(-80, 81) if inside(x / 8, ym, TK)]
        if xs:
            x1, x2 = min(xs), max(xs)
            lo, hi = [8 + x1, 8 + y, 8 + ZT - 0.05], [8 + x2, 8 + y + step, 8 + ZT + 0.15]
            uv = [8 + x1, 8 - (y + step), 8 + x2, 8 - y]
            els.append({'from': lo, 'to': hi, 'faces': {'south': {'uv': uv, 'texture': '#table'}, 'north': {'uv': uv, 'texture': '#table'}}})
        y += step
    disp = {'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]},
            'gui': {'rotation': [10, 25, 0], 'translation': [0, 0, 0], 'scale': [0.95, 0.95, 0.95]},
            'ground': {'rotation': [0, 0, 0], 'translation': [0, 2, 0], 'scale': [0.5, 0.5, 0.5]},
            'thirdperson_righthand': {'rotation': [0, 0, 0], 'translation': [0, 2.5, 1.5], 'scale': [0.5, 0.5, 0.5]},
            'firstperson_righthand': {'rotation': [0, -20, 0], 'translation': [1, 3, 0], 'scale': [0.6, 0.6, 0.6]}}
    t = {k: f'bm:item/creativity_gem_{k}' for k in ('table', 'crown', 'pav')}
    return {'textures': dict(t, particle=t['table']), 'elements': els, 'display': disp}


ANIM = {'animation': {'frametime': 3, 'interpolate': True}}


if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(f'{out}/assets/bm/models/item', exist_ok=True); os.makedirs(f'{out}/assets/bm/textures/item', exist_ok=True)
    for k, im in textures().items():
        im.save(f'{out}/assets/bm/textures/item/{k}.png')
        json.dump(ANIM, open(f'{out}/assets/bm/textures/item/{k}.png.mcmeta', 'w'))
    m = model(); json.dump(m, open(f'{out}/assets/bm/models/item/creativity_gem.json', 'w'))
    print(len(m['elements']), 'elements')

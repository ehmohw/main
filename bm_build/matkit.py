"""2.93e: MATERIAL DETAIL for the followers' textures, in the language of Emma's (phase57_art: _fabric, _knit, _pleats, _hair2,
_gloss): every material has life of its own - a weave, folds, clumps of fur, feathers, a gleam - not a flat fill.

enrich(T, KINDS) runs over a module's finished textures: each key in KINDS (key -> kind) keeps its design and colours, and
its brightness is worked over by the kind's detail map (multiplied, so a pattern already drawn stays; alpha is untouched).
A texture under 64 px is scaled up first (each pixel a 4x4 block), so the detail is fine. Faces, eyes, emblems, glass and
flames are never listed - they are drawn already.

The kinds:  fabric  satin  grosgrain  felt  knit  pleats  ribbed  velvet  denim  leather  plumage  down  fur  short_fur  hair
            skin  hide  hide_soft  scales  membrane  horn  rind  wood  straw  metal  gold  stone  ghost  scaly
"""
import math
import random
import numpy as np
from PIL import Image

N = 64


def _lowfreq(rnd, amp, cells=4):
    """a soft blotchy map (bilinear over a coarse random grid), mean 0"""
    g = np.array([[rnd.uniform(-1, 1) for _ in range(cells + 1)] for _ in range(cells + 1)])
    ys, xs = np.mgrid[0:N, 0:N] / (N - 1) * cells
    y0, x0 = np.floor(ys).astype(int).clip(0, cells - 1), np.floor(xs).astype(int).clip(0, cells - 1)
    fy, fx = ys - y0, xs - x0
    v = (g[y0, x0] * (1 - fx) * (1 - fy) + g[y0, x0 + 1] * fx * (1 - fy) + g[y0 + 1, x0] * (1 - fx) * fy + g[y0 + 1, x0 + 1] * fx * fy)
    return v * amp


def _fine(rnd, amp):
    return np.array([[rnd.uniform(-amp, amp) for _ in range(N)] for _ in range(N)])


def _toplight(top=1.06, bottom=0.94, span=36):
    y = np.arange(N)[:, None] * np.ones((1, N))
    return top - (top - bottom) * np.minimum(1.0, y / span)


def _folds(k, rnd, n=2, depth=0.82):
    for _ in range(n):
        x0, w = rnd.randint(5, 58), rnd.uniform(0, 6.28)
        for y in range(N):
            xx = int(round(x0 + 1.5 * math.sin(y / 10 + w)))
            for dx, f in ((-1, 0.5 + depth / 2 - 0.05), (0, depth), (1, 0.5 + depth / 2 - 0.05), (2, 1.1)):
                k[y, (xx + dx) % N] *= f
    return k


def _strands(rnd, clump=(4, 7), strand=0.05, part=0.72, shine=None, tips=0.0, length=None):
    """clumps of hair or fur (Emma's _hair2): lit in the middle, dark at the parting, fine strands, an optional shine"""
    k = np.ones((N, N)); x = 0
    while x < N:
        w = rnd.randint(*clump); wob = rnd.uniform(0, 6.28); off = rnd.randint(0, 15)
        for j in range(w):
            X = x + j
            if X >= N: break
            t = j / max(1, w - 1); base = 1.0 - 0.18 * abs(t - 0.45) * 2; s = rnd.uniform(-strand, strand)
            for y in range(N):
                if rnd.random() < 0.06: s = rnd.uniform(-strand, strand)
                v = base + s
                if j == 0: v *= part
                if shine:
                    sy = shine[0] + 1.4 * math.sin(wob + X / 3)
                    if sy <= y <= sy + (shine[1] - shine[0]) and 0 < j < w - 1: v *= 1.2
                if length and (y + off) % length == 0: v *= 0.86                  # (where one tuft ends and the next begins)
                if length and tips and (y + off) % length == length - 1: v *= 1 + tips
                k[y, X] = v
        x += w
    return k


def _scallops(rnd, h=5, w=6, lit=1.1, dark=0.86, barb=0.03, vary=0.04):
    """overlapping feathers or scales: rows of little arcs, each lit along its top and shadowed under its lower edge, each
    one a shade of its own"""
    k = np.ones((N, N)) + _fine(rnd, barb)
    shade = {}
    for y in range(N):
        r, yy = divmod(y, h)
        for x in range(N):
            col = (x + (w // 2 if r % 2 else 0)) // w
            if (r, col) not in shade: shade[(r, col)] = 1 + rnd.uniform(-vary, vary)
            k[y, x] *= shade[(r, col)]
            xx = (x + (w // 2 if r % 2 else 0)) % w
            c = abs(xx - (w - 1) / 2) / (w / 2)                  # (0 in the middle of a feather, 1 at its sides)
            edge = h - 1 - int(round((1 - c * c) * (h - 2)))      # (the arc of its lower edge)
            if yy == 0: k[y, x] *= lit
            if yy >= edge: k[y, x] *= dark
            elif yy == edge - 1: k[y, x] *= 0.95
    return k


def _round_scales(rnd, R=4.0, rim=0.86, gain=0.16, vary=0.04, barb=0.02):
    """overlapping round scales or feathers, drawn row by row from the top so each row lies over the one above: each one lit
    toward its middle, a dark rim along its lower edge, each a shade of its own"""
    k = np.ones((N, N)) + _fine(rnd, barb)
    sx, sy = 2 * R, R
    rows = int(N / sy) + 3
    yy, xx = np.mgrid[0:N, 0:N]
    for r in range(-1, rows):
        cy = r * sy
        for c in range(-1, int(N / sx) + 2):
            cx = c * sx + (R if r % 2 else 0)
            v = 1 + rnd.uniform(-vary, vary)
            for oy in (0, N, -N):
                for ox in (0, N, -N):
                    d = np.hypot(xx - cx - ox, yy - cy - oy)
                    m = (d <= R) & (yy >= cy + oy - R * 0.2)
                    if not m.any(): continue
                    t = d[m] / R
                    k[m] = v * (1 + gain * (1 - t) - gain * 0.5) * np.where(t > 0.78, rim, 1.0)
    return k


def kmap(kind, seed):
    rnd = random.Random(seed)
    yy, xx = np.mgrid[0:N, 0:N]
    if kind == 'fabric':
        k = (1 + _fine(rnd, 0.02)) * _toplight() * np.where((xx + yy) % 2, 1.025, 0.975)
        return _folds(k, rnd, 2)
    if kind == 'velvet':
        k = (1 + _fine(rnd, 0.03) + _lowfreq(rnd, 0.05)) * _toplight(1.08, 0.9)
        return _folds(k, rnd, 3, 0.78)
    if kind == 'satin':                                           # (a fine diagonal ripple of sheen, a weave, a soft fold or two)
        sheen = 1 + 0.06 * np.cos(2 * math.pi * (xx + yy) / 14.0) + 0.03 * np.cos(2 * math.pi * (xx - 2 * yy) / 23.0)
        k = sheen * np.where((xx + yy) % 2, 1.015, 0.985) * (1 + _fine(rnd, 0.012)) * _toplight(1.05, 0.96, 48)
        return _folds(k, rnd, 1, 0.88)
    if kind == 'grosgrain':                                       # (a ribbon: fine horizontal ribs, a lit top edge)
        k = np.where(yy % 2, 1.05, 0.93) * (1 + _fine(rnd, 0.015))
        k[0] *= 1.12; k[-1] *= 0.85
        return k
    if kind == 'felt':                                            # (a hat: fuzz, a soft blotch, a sheen near the top)
        k = (1 + _fine(rnd, 0.035) + _lowfreq(rnd, 0.04)) * _toplight(1.05, 0.93, 48)
        k[1:4] *= 1.1
        return k
    if kind == 'knit':
        j, i = xx % 4, yy % 3
        k = np.where(i == 2, 0.84, np.where((j == 0) | (j == 3), 0.92, np.where((j == 1) == (i == 0), 1.12, 1.0)))
        return k * (1 + _fine(rnd, 0.02))
    if kind == 'pleats':
        shade = np.array([1.16, 1.07, 1.0, 0.94, 0.84, 0.66])
        k = shade[xx % 6] * (1 + _fine(rnd, 0.02)); k[0] *= 1.14; k[1] *= 1.05
        return k
    if kind == 'ribbed':
        return np.where(xx % 2, 1.0, 0.9) * (1 + _fine(rnd, 0.015))
    if kind == 'denim':                                           # (a twill: diagonal ribs, worn paler in patches)
        return np.where((xx + yy) % 4 < 2, 1.05, 0.93) * (1 + _lowfreq(rnd, 0.07) + _fine(rnd, 0.02))
    if kind == 'leather':                                         # (a grain, a few creases, a gleam)
        k = (1 + _fine(rnd, 0.025) + _lowfreq(rnd, 0.05)) * _toplight(1.08, 0.9, 40)
        for _ in range(4):
            x0, y0, a = rnd.randint(0, 63), rnd.randint(0, 63), rnd.uniform(-0.6, 0.6)
            for t in range(rnd.randint(6, 14)):
                k[int(y0 + t * a) % N, (x0 + t) % N] *= 0.86
        k[1:3, :] *= np.where(xx[1:3] % 16 < 7, 1.2, 1.0)
        return k
    if kind == 'scaly':                                           # (a bird's foot: small tiles)
        k = _scallops(rnd, 3, 4, 1.06, 0.9, 0.02)
        return k * _toplight(1.04, 0.96)
    if kind in ('plumage', 'down'):                               # (a penguin: sleek and smooth - faint short feather strokes laid
        soft = kind == 'down'                                     #  downward, a soft blotch, a gentle sheen; no outlined shapes)
        k = 1 + _lowfreq(rnd, 0.03 if soft else 0.035)
        for _ in range(N * N // (7 if soft else 8)):
            x, y = rnd.uniform(0, N), rnd.randint(0, N - 1)
            L, sl = rnd.randint(3, 5), rnd.uniform(-0.25, 0.25)
            v = rnd.choice((0.965, 0.98, 1.025, 1.04)) if soft else rnd.choice((0.96, 0.975, 1.03, 1.045))
            for t in range(L):
                k[(y + t) % N, int(x + sl * t) % N] *= 1 + (v - 1) * (1 - t / L)
        if not soft:
            k *= 1 + 0.07 * np.exp(-((yy - 14) / 7.0) ** 2)          # (the sheen across his coat)
        return k * _toplight(1.05, 0.96, 56)
    if kind in ('fur', 'short_fur'):                              # (fur: a soft blotch, then thousands of short strokes, lit and dark)
        long = kind == 'fur'
        k = 1 + _lowfreq(rnd, 0.05 if long else 0.035)
        for _ in range(N * N // (6 if long else 5)):
            x, y = rnd.uniform(0, N), rnd.randint(0, N - 1)
            L, sl = rnd.randint(4, 9) if long else rnd.randint(2, 4), rnd.uniform(-0.35, 0.35)
            v = rnd.choice((0.84, 0.9, 0.94, 1.07, 1.12)) if long else rnd.choice((0.9, 0.94, 1.05, 1.09))
            for t in range(L):
                f = 1 + (v - 1) * (1 - t / L)                     # (each stroke fades toward its tip)
                k[(y + t) % N, int(x + sl * t) % N] *= f
        return k * _toplight(1.05, 0.95, 50)
    if kind == 'hair':
        return _strands(rnd, (4, 7), 0.05, 0.72, (7, 11))
    if kind == 'skin':                                            # (barely there: soft warmth and pores)
        return (1 + _lowfreq(rnd, 0.025) + _fine(rnd, 0.012)) * _toplight(1.03, 0.97, 64)
    if kind in ('hide', 'hide_soft'):                             # (a shark's or a beast's hide: grain, mottling, a wet gleam)
        a = 1.0 if kind == 'hide' else 0.5
        k = 1 + _lowfreq(rnd, 0.06 * a) + _fine(rnd, 0.025 * a)
        k *= np.where((xx + 2 * yy) % 5 == 0, 1 - 0.04 * a, 1.0)
        for _ in range(5):
            y0, x0, L = rnd.randint(2, 30), rnd.randint(0, 63), rnd.randint(5, 14)
            for t in range(L): k[y0, (x0 + t) % N] *= 1 + 0.06 * a * (1 - abs(t - L / 2) / (L / 2))
        return k * _toplight(1.05, 0.95, 50)
    if kind == 'scales':
        return _round_scales(rnd, 3.2, 0.84, 0.18, 0.04) * (1 + _lowfreq(rnd, 0.04))
    if kind == 'membrane':                                        # (a fin or wing: rays fanning out, translucent between)
        k = 1 + _lowfreq(rnd, 0.04) + _fine(rnd, 0.015)
        k *= np.where(xx % 7 == 0, 0.86, np.where(xx % 7 == 1, 1.08, 1.0))
        return k
    if kind == 'horn':                                            # (claw, horn, bone: growth rings, a gleam down one side)
        k = np.where(yy % 5 == 0, 0.9, 1.0) * (1 + _fine(rnd, 0.02))
        return k * np.where(xx % 16 < 4, 1.12, 1.0)
    if kind == 'rind':                                            # (a pumpkin: each rib rounded, a speckle, a waxy gleam)
        k = 1 + 0.08 * np.cos((xx % 8 - 3.5) / 8 * math.pi) - 0.04 + _fine(rnd, 0.02)
        for _ in range(40): k[rnd.randint(0, 63), rnd.randint(0, 63)] *= 0.9
        k[:, ::8] *= 0.9
        return k * (1 + _lowfreq(rnd, 0.04)) * np.where((xx % 8 == 2) & (yy % 23 < 9), 1.08, 1.0)
    if kind == 'wood':
        k = np.ones((N, N))
        for x in range(N):
            ph = rnd.uniform(0, 6.28)
            for y in range(N): k[y, x] = 1 + 0.06 * math.sin(x / 2.2 + 1.2 * math.sin(y / 9 + ph))
        return k * (1 + _fine(rnd, 0.02))
    if kind == 'straw':                                           # (a woven boater: crossing strands)
        return np.where(((xx + yy) // 3) % 2, 1.07, 0.92) * np.where(((xx - yy) // 3) % 2, 1.03, 0.97) * (1 + _fine(rnd, 0.025))
    if kind in ('metal', 'gold'):                                 # (brushed, a bright band, darker at the foot; gold sparkles)
        k = (1 + _fine(rnd, 0.012)) * (1 + np.repeat(_fine(rnd, 0.025)[:, :1], N, axis=1) * 0.6 + _fine(rnd, 0.01))
        k *= 1 + 0.22 * np.exp(-((yy - 18) / 5.0) ** 2) - 0.12 * np.clip((yy - 40) / 24, 0, 1)
        if kind == 'gold':
            for _ in range(14):
                k[rnd.randint(0, 63), rnd.randint(0, 63)] *= 1.3
        return k
    if kind == 'stone':
        k = 1 + _lowfreq(rnd, 0.08, 6) + _fine(rnd, 0.04)
        for _ in range(5):
            x, y = rnd.randint(0, 63), rnd.randint(0, 63)
            for _t in range(rnd.randint(6, 16)):
                k[y % N, x % N] *= 0.8; x += rnd.choice((-1, 0, 1)); y += 1
        return k
    if kind == 'ghost':                                           # (soft wisps drifting through)
        return 1 + 0.06 * np.sin(xx / 6.0 + 2 * np.sin(yy / 9.0)) + _lowfreq(rnd, 0.04) + _fine(rnd, 0.015)
    raise KeyError(kind)


def detail(im, kind, seed):
    """one texture, its design kept, worked over by the kind's detail"""
    im = im.convert('RGBA')
    if im.size[0] < N:                                            # (an old 16 px noise fill: its own colour, clean, then detail)
        med = tuple(int(v) for v in np.median(np.asarray(im).reshape(-1, 4), axis=0))
        im = Image.new('RGBA', (N, N * im.size[1] // im.size[0]), med)
    a = np.asarray(im).astype(float)
    h = a.shape[0]
    k = kmap(kind, seed)
    if h != N: k = np.tile(k, (h // N + 1, 1))[:h]
    a[..., :3] = np.clip(a[..., :3] * k[..., None] + (k[..., None] - 1) * 40, 0, 255)      # (+: the darks show it too)
    return Image.fromarray(a.astype(np.uint8), 'RGBA')


def enrich(T, kinds):
    """(a module's textures, key -> kind) each listed key worked over; the rest untouched"""
    for i, (key, kind) in enumerate(sorted(kinds.items())):
        if key in T:
            T[key] = detail(T[key], kind, 9001 + sum(map(ord, key)))
    return T


# ---- which follower textures get which material (faces, eyes, emblems, glass, flames left alone)
_ava = {'av_skin': 'skin', 'av_skin_dk': 'skin', 'av_hair': 'hair', 'av_hair_dk': 'hair', 'av_navy': 'fabric', 'av_navy_dk': 'fabric',
        'av_bodice': 'satin', 'av_skirt': 'fabric', 'av_under': 'fabric', 'av_glove': 'satin', 'av_cuff': 'fabric', 'av_gold': 'gold', 'av_shoe': 'leather'}
KINDS = {
    'phase60': {'pm_black': 'plumage', 'pm_white': 'down', 'pm_orange': 'skin', 'pm_yellow': 'scaly', 'pm_blue': 'satin', 'pm_dblue': 'satin',
                'pm_gold': 'gold', 'pm_case': 'leather', 'pm_hat': 'felt',
                **{f'pm_{s}_{p}': k for s in ('fall', 'xmas', 'easter', 'summer')
                   for p, k in (('body', 'plumage'), ('belly', 'down'), ('band', 'grosgrain'), ('feet', 'scaly'), ('hat', 'straw' if s == 'summer' else 'felt'),
                                ('tie', 'satin'))}},
    'bones_art': {'bn_skin': 'hide', 'bn_skin_dk': 'hide', 'bn_belly': 'hide_soft', 'bn_flank': 'hide', 'bn_side': 'hide'},
    'bender_art': {k: 'short_fur' for k in ('bd_fur', 'bd_back', 'bd_cream', 'bd_fur_lt', 'bd_mask', 'bd_tip', 'bd_paw', 'bd_bridge')} | {'bd_ear_in': 'skin'},
    'lantern_art': {'ln_rind': 'rind', 'ln_rind_top': 'rind', 'ln_rind_dk': 'rind', 'ln_stem': 'wood', 'ln_leaf': 'membrane', 'ln_leg': 'wood'},
    'stalker_art': {'st_skin': 'hide', 'st_shade': 'hide', 'st_ribs': 'hide', 'st_back': 'hide', 'st_claw': 'horn', 'st_nail': 'horn'},
    'ava_art': _ava | {k + '_g': v for k, v in _ava.items()},
    'pearl_art': {'pq_skin': 'skin', 'pq_skin_dk': 'skin', 'pq_hair': 'hair', 'pq_mint': 'fabric', 'pq_dress': 'satin', 'pq_dress_top': 'satin',
                  'pq_gold': 'gold', 'pq_gown': 'velvet', 'pq_gown_top': 'velvet', 'pq_under': 'fabric', 'pq_glove': 'satin', 'pq_cape': 'velvet'},
    'bloo_art': {'bo_fur': 'fur', 'bo_fur_dk': 'fur', 'bo_mane': 'fur', 'bo_chest': 'fur', 'bo_hide': 'hide', 'bo_hide_dk': 'hide', 'bo_claw': 'horn',
                 'bo_wclaw': 'horn', 'bo_wing': 'membrane', 'bo_bone': 'horn', 'bo_horn': 'horn', 'bo_band': 'grosgrain'},
    'ashur_art': {'as_skin': 'skin', 'as_skin_ash': 'skin', 'as_skin_dk': 'skin', 'as_hair': 'hair', 'as_plates': 'metal', 'as_hem': 'fabric',
                  'as_rock': 'stone', 'as_gold': 'gold'},
    'chef_art': {'cf_skin': 'skin', 'cf_skin_dk': 'skin', 'cf_white': 'fabric', 'cf_toque': 'fabric', 'cf_white_dk': 'fabric', 'cf_pleat': 'fabric',
                 'cf_jacket': 'fabric', 'cf_check': 'fabric', 'cf_shoe': 'leather', 'cf_stache': 'hair', 'cf_bow': 'satin', 'cf_steel': 'metal',
                 'cf_steel_dk': 'metal', 'cf_wood': 'wood', 'cf_hair': 'hair'},
    'neighbor_art': {'nb_skin': 'skin', 'nb_skin_dk': 'skin', 'nb_white': 'fabric', 'nb_white_dk': 'fabric', 'nb_shirt': 'fabric', 'nb_collar': 'fabric',
                     'nb_black': 'fabric', 'nb_shoe': 'leather', 'nb_band': 'grosgrain', 'nb_beret': 'felt', 'nb_hair': 'hair', 'nb_baton': 'wood'},
    'dennis_art': {'dw_skin': 'skin', 'dw_skin_dk': 'skin', 'dw_jacket': 'fabric', 'dw_jacket_dk': 'fabric', 'dw_cuff': 'knit', 'dw_shirt': 'fabric',
                   'dw_denim': 'denim', 'dw_denim_lt': 'denim', 'dw_boot': 'leather', 'dw_boot_dk': 'leather', 'dw_beard': 'hair', 'dw_grey': 'fabric',
                   'dw_frame': 'metal', 'dw_helm': 'metal', 'dw_band': 'grosgrain', 'dw_gold': 'gold', 'dw_horn': 'horn', 'dw_horn_dk': 'horn',
                   'dw_steel': 'metal', 'dw_steel_dk': 'metal', 'dw_collar': 'fabric'},
    'pistachio_art': {'ps_ghost': 'ghost', 'ps_ghost_dk': 'ghost', 'ps_coat': 'fabric', 'ps_coat_dk': 'fabric', 'ps_lapel': 'satin', 'ps_tie': 'satin',
                      'ps_hat': 'felt', 'ps_hat_dk': 'felt', 'ps_band': 'grosgrain', 'ps_stache': 'hair', 'ps_gold': 'gold', 'ps_silver': 'metal',
                      'ps_silver_dk': 'metal', 'ps_plate': 'metal'},
    'fishy_art': {'fy_metal': 'metal', 'fy_band': 'metal', 'fy_joint': 'metal', 'fy_fish': 'scales', 'fy_belly': 'scales', 'fy_fin': 'membrane',
                  'fy_gold': 'gold', 'fy_hat': 'felt', 'fy_hatband': 'grosgrain', 'fy_stache': 'hair', 'fy_stone': 'stone', 'fy_sand': 'stone'},
    'omega_art': {'om_body': 'scales', 'om_body_dk': 'scales', 'om_stripe': 'scales', 'om_fin': 'membrane', 'om_claw': 'horn', 'om_gold': 'gold',
                  'om_gold_dk': 'gold'},
}


def wrapped(fn, module):
    """a module's textures() with its followers' materials worked in (every caller - the recolours, gilding, dolls - sees it)"""
    kinds = KINDS[module.rsplit('.', 1)[-1]]
    def textures(*a, **k):
        return enrich(fn(*a, **k), kinds)
    return textures

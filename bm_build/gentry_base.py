"""2.96: THE GUTTER GENTRY AS FOLLOWERS - what Batty, Eggbert and The Count's rigs (batty_art, eggbert_art, count_art) share.

Their look is the boss art's (phase88_art: the same painted textures and blocky geometry, ported under each follower's own prefix),
made into rigkit rigs at follower size, with a face per expression and a CHIBI costume (the form suffix '_c': every part's model
again with a big head, a small body, chunky little limbs and softer faces - on the very same joints, so every pose fits both).
The boss elements are already in rigkit's model space (each part's joint at 8, 8, 8), so a part is the boss's own element list."""
import math
from PIL import Image, ImageDraw

import phase88_art as G88
from phase57_art import hexc
from rigkit import qs, transform

G88.textures()                    # (fills G88.UV - the painted faces' uv windows - before any boss element is made)
TEX = G88.textures()
I = (0.0, 0.0, 0.0, 1.0)


def port(prefix, els):
    """the boss's elements under a follower's prefix: '#gnt_bat_face' -> '#gb_bat_face'"""
    out = []
    for e in els:
        e = dict(e, faces={f: dict(v, texture='#' + prefix + v['texture'][5:]) for f, v in e['faces'].items()})
        out.append(e)
    return out


def ported_textures(prefix, names):
    return {prefix + n[4:]: TEX[n].copy() for n in names}


def scale(els, k=(1.0, 1.0, 1.0), d=(0.0, 0.0, 0.0)):
    """about the joint (model 8, 8, 8): each axis by k, then shifted by d (model units)"""
    return transform(els, lambda v: [8 + (v[i] - 8) * k[i] + d[i] for i in range(3)])


def with_tex(els, old, new):
    """the elements with one texture swapped for another"""
    return [dict(e, faces={f: (dict(v, texture='#' + new) if v['texture'] == '#' + old else v) for f, v in e['faces'].items()}) for e in els]


def builder(M):
    def part(name, els):
        for e in els:
            for c in e['from'] + e['to']:
                assert -16 <= c <= 32, (name, e['from'], e['to'])
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)
    return part


def P(**kw):
    return kw


def limb(sx, fwd=0.0, out=0.0, turn=0.0):
    """a hanging limb: forward by fwd, out to its side by out (rigkit's display frame)"""
    return qs(('y', turn * sx), ('x', -fwd), ('z', -out * sx))


# ---------------------------------------------------------------------------------------------------- faces
# (each painted on the boss's own canvas size, so its uv window is the boss's)
def canvas(w, h, base, seed, var=0.04):
    im = G88._noise(base, seed, var)
    k = 64 / w if w >= h else 64 / h
    return im, ImageDraw.Draw(im), (lambda x, y: (round(x * k), round(y * k)))


def arc(d, P, cx, cy, rx, ry, up, col, w=0.35, n=14):
    """a little arc of squares: up=True is a ^ (a happy closed eye), False a u"""
    for i in range(n + 1):
        t = math.pi * i / n
        x = cx - rx * math.cos(t); y = cy - (ry * math.sin(t) if up else -ry * math.sin(t))
        d.rectangle(P(x - w / 2, y - w / 2) + P(x + w / 2, y + w / 2), fill=hexc(col))


def bat_face(kind=None, chibi=False):
    """Batty's head front (12 x 10): heavy-lidded sleepy yellow eyes (the boss's), or blink / happy / angry / surprised; chibi: big
    round shiny eyes and soft little lids, rosy cheeks"""
    F = G88
    im, d, P = canvas(12, 10, F.FUR, 3, 0.05)
    import random
    rnd = random.Random(4)
    for _ in range(40):
        x, y = rnd.uniform(0, 12), rnd.uniform(0, 10)
        d.rectangle(P(x, y) + P(x + 0.2, y + 0.6), fill=hexc(rnd.choice((F.FUR_LT, F.FUR_DK))))
    for cx, s in ((3.4, 1), (8.6, -1)):
        if chibi: x0, x1, y0, y1 = cx - 2.2, cx + 2.2, 1.6, 5.6
        else: x0, x1, y0, y1 = cx - 1.8, cx + 1.8, 2.3, 4.9
        my = (y0 + y1) / 2
        if kind == 'blink':
            d.rectangle(P(x0, my) + P(x1, my + 0.45), fill=hexc(F.INK))
            arc(d, P, cx, my + 0.2, (x1 - x0) / 2 - 0.2, 0.6, False, F.INK)
        elif kind == 'happy':
            arc(d, P, cx, my + 0.9, (x1 - x0) / 2 - 0.3, 1.6, True, F.INK, 0.45)
        else:
            d.rectangle(P(x0 - 0.2, y0 - 0.2) + P(x1 + 0.2, y1 + 0.2), fill=hexc(F.INK))
            d.rectangle(P(x0, y0) + P(x1, y1), fill=hexc(F.EYE))
            d.rectangle(P(x0, y1 - 0.5) + P(x1, y1), fill=hexc(F.EYE_DK))
            if kind == 'surprised':
                d.rectangle(P(cx - 0.5, my - 0.5) + P(cx + 0.5, my + 0.5), fill=hexc(F.PUPIL))
            elif chibi:                                                                    # (big pupils, two glints)
                d.rectangle(P(cx - 1.2 + 0.3 * s, y0 + 0.6) + P(cx + 1.2 + 0.3 * s, y1 - 0.3), fill=hexc(F.PUPIL))
                d.rectangle(P(cx - 0.9 + 0.3 * s, y0 + 0.8) + P(cx - 0.2 + 0.3 * s, y0 + 1.6), fill=hexc('#ffffff'))
                d.rectangle(P(cx + 0.4 + 0.3 * s, y1 - 1.3) + P(cx + 0.8 + 0.3 * s, y1 - 0.9), fill=hexc('#ffffff'))
            else:
                px = cx + 0.4 * s                                                          # (low and inward: sleepy)
                d.rectangle(P(px - 0.7, y0 + 1.1) + P(px + 0.7, y1 - 0.15), fill=hexc(F.PUPIL))
                d.rectangle(P(px - 0.5 * s - 0.15, y0 + 1.3) + P(px - 0.5 * s + 0.15, y0 + 1.7), fill=hexc('#ffffff'))
            if kind == 'angry':                                                            # (the brows down hard at the middle)
                for i in range(12):
                    t = i / 11; x = x0 - 0.3 + (x1 - x0 + 0.6) * t
                    y = y0 - 0.6 + (1.3 * t if s == 1 else 1.3 * (1 - t))
                    d.rectangle(P(x - 0.25, y - 0.3) + P(x + 0.25, y + 0.3), fill=hexc(F.INK))
            elif not chibi and kind != 'surprised':                                        # (the boss's heavy lid, half shut)
                d.rectangle(P(x0 - 0.3, y0 - 0.3) + P(x1 + 0.3, y0 + 1.0), fill=hexc(F.FUR_DK))
                d.rectangle(P(x0 - 0.3, y0 + 0.9) + P(x1 + 0.3, y0 + 1.2), fill=hexc(F.INK))
            elif chibi and kind != 'surprised':                                            # (a soft little lid)
                d.rectangle(P(x0 - 0.2, y0 - 0.2) + P(x1 + 0.2, y0 + 0.35), fill=hexc(F.FUR_DK))
        if chibi:                                                                          # rosy cheeks
            d.rectangle(P(cx - 1.5 - 0.6 * s, 6.6) + P(cx + 0.2 - 0.6 * s, 7.4), fill=hexc('#7a4a6a'))
    if not chibi:
        for x0, s in ((0.1, 1), (11.0, -1)):                                               # cheek tufts
            for i in range(3):
                x = x0 + s * i * 0.4
                d.rectangle(P(min(x, x + 0.9 * s), 6.4 + i * 0.6) + P(max(x, x + 0.9 * s), 6.8 + i * 0.6), fill=hexc(F.FUR_LT))
    return im


def bat_grin(kind=None, chibi=False):
    """the muzzle's front (8.4 x 4.2): the boss's gritted toothy grin; happy: open, the tongue showing; chibi: a small smile with
    two little fangs"""
    F = G88
    im, d, P = canvas(8.4, 4.2, F.FUR, 5, 0.05)
    d.rectangle(P(3.5, 0.2) + P(4.9, 0.8), fill=hexc(F.NOSE)); d.rectangle(P(3.9, 0.8) + P(4.5, 1.1), fill=hexc(F.NOSE))
    if chibi:
        arc(d, P, 4.2, 1.9, 1.6, 0.9, False, F.INK, 0.35)
        for fx in (3.0, 5.0):
            d.polygon([P(fx - 0.35, 2.4), P(fx + 0.35, 2.4), P(fx, 3.3)], fill=hexc('#ffffff'))
        if kind == 'happy':
            d.rectangle(P(3.6, 2.5) + P(4.8, 3.3), fill=hexc('#d85a7a'))
        return im
    x0, x1, y0, y1 = 0.45, 7.95, 1.35, 3.95
    d.rectangle(P(x0, y0) + P(x1, y1), fill=hexc(F.GUM))
    d.rectangle(P(x0 + 0.2, y0 + 0.2) + P(x1 - 0.2, y1 - 0.2), fill=hexc(F.TEETH))
    ym = (y0 + y1) / 2
    if kind == 'happy':                                                                    # (open: the teeth apart, a pink tongue)
        d.rectangle(P(x0 + 0.2, ym - 0.4) + P(x1 - 0.2, ym + 0.6), fill=hexc(F.GUM))
        d.rectangle(P(2.6, ym + 0.1) + P(5.8, ym + 0.6), fill=hexc('#d85a7a'))
    else:
        d.rectangle(P(x0 + 0.2, ym - 0.12) + P(x1 - 0.2, ym + 0.12), fill=hexc(F.GUM))
    for i in range(1, 7):
        x = x0 + 0.2 + i * (x1 - x0 - 0.4) / 7
        d.rectangle(P(x - 0.08, y0 + 0.2) + P(x + 0.08, y1 - 0.2), fill=hexc(F.TEETH_SH))
    for fx in (x0 + 0.6, x1 - 1.1):
        d.rectangle(P(fx, ym) + P(fx + 0.5, ym + 0.75), fill=hexc('#ffffff'))
    return im


def egg_eye(kind=None, chibi=False):
    """one of Eggbert's eyes (a square glow in the ooze); blink: a slit; happy: a ^; angry: the top cut on a slant (mirror it for
    the other eye); chibi: rounder, two big glints"""
    F = G88
    im = Image.new('RGBA', (64, 64), hexc(F.GOO)); d = ImageDraw.Draw(im)
    if kind == 'blink':
        d.rectangle((6, 28, 57, 36), fill=hexc(F.EGG_EYE)); return im
    if kind == 'happy':
        for i in range(30):
            t = math.pi * i / 29; x = 32 - 24 * math.cos(t); y = 46 - 26 * math.sin(t)
            d.rectangle((x - 4, y - 4, x + 4, y + 4), fill=hexc(F.EGG_EYE))
        return im
    if chibi: d.ellipse((2, 2, 61, 61), fill=hexc('#9aa86a')); d.ellipse((6, 6, 57, 57), fill=hexc(F.EGG_EYE)); d.ellipse((16, 16, 47, 47), fill=hexc(F.EGG_EYE_HL))
    else: d.rectangle((4, 4, 59, 59), fill=hexc('#9aa86a')); d.rectangle((8, 8, 55, 55), fill=hexc(F.EGG_EYE)); d.rectangle((18, 18, 45, 45), fill=hexc(F.EGG_EYE_HL))
    if chibi: d.ellipse((12, 10, 26, 24), fill=hexc('#ffffff')); d.ellipse((40, 40, 48, 48), fill=hexc('#ffffff'))
    else: d.rectangle((12, 12, 22, 20), fill=hexc('#ffffff'))
    if kind == 'angry':
        d.polygon([(0, 0), (64, 0), (64, 30), (0, 6)], fill=hexc(F.GOO))
    if kind == 'surprised':
        d.rectangle((26, 26, 37, 37), fill=hexc(F.GOO))
    return im


def count_face(kind=None, chibi=False):
    """The Count's face (18 x 7): the boss's grump - furrowed brows, empty white spectacle eyes, a knobbly nose line, a frown with
    two little fangs; blink / happy / angry / surprised; chibi: bigger softer eyes (still empty white), a little pout"""
    F = G88
    im, d, P = canvas(18, 7, F.BLOB, 41, 0.025)
    ln = hexc(F.BLOB_LN)
    d.rectangle(P(0, 6.3) + P(18, 7), fill=hexc(F.BLOB_DK))

    def line(pts, w=0.25):
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            for i in range(10):
                x = xa + (xb - xa) * i / 9; y = ya + (yb - ya) * i / 9
                d.rectangle(P(x - w, y - w * 0.8) + P(x + w, y + w * 0.8), fill=ln)
    brow = {None: (0.9, 1.9), 'angry': (0.5, 2.2), 'happy': (1.1, 0.8), 'blink': (1.0, 1.6), 'surprised': (0.7, 0.4)}[kind]
    if chibi: brow = (brow[0] * 0.5 + 0.2, (brow[1] - brow[0]) * 0.4 + brow[0] * 0.5 + 0.2)
    line([(3.2, brow[0]), (7.8, brow[1])]); line([(14.8, brow[0]), (10.2, brow[1])])
    if not chibi and kind in (None, 'angry'):
        for x in (8.6, 9.4):
            d.rectangle(P(x - 0.12, 0.5) + P(x + 0.12, 1.5), fill=ln)
    r = 1.75 if chibi else 1.35
    for cx in (6.4, 11.6):
        cy = 3.4
        if kind == 'blink':
            d.ellipse(P(cx - r - 0.25, cy - r - 0.25) + P(cx + r + 0.25, cy + r + 0.25), fill=hexc(F.SPEC))
            d.ellipse(P(cx - r, cy - r) + P(cx + r, cy + r), fill=hexc(F.BLOB))
            line([(cx - r + 0.3, cy + 0.2), (cx + r - 0.3, cy + 0.2)], 0.2)
        elif kind == 'happy':
            d.ellipse(P(cx - r - 0.25, cy - r - 0.25) + P(cx + r + 0.25, cy + r + 0.25), fill=hexc(F.SPEC))
            d.ellipse(P(cx - r, cy - r) + P(cx + r, cy + r), fill=hexc(F.WHITE))
            arc(d, P, cx, cy + 0.7, r - 0.4, 1.0, True, F.BLOB_LN, 0.3)
        else:
            rr = r * (1.15 if kind == 'surprised' else 1.0)
            d.ellipse(P(cx - rr - 0.25, cy - rr - 0.25) + P(cx + rr + 0.25, cy + rr + 0.25), fill=hexc(F.SPEC))
            d.ellipse(P(cx - rr, cy - rr) + P(cx + rr, cy + rr), fill=hexc(F.WHITE))
            if chibi:
                d.rectangle(P(cx - rr * 0.55, cy - rr * 0.6) + P(cx - rr * 0.15, cy - rr * 0.2), fill=hexc('#ffffff'))
    if not chibi:
        for x, y in ((8.2, 4.95), (9.0, 4.75), (9.8, 4.95)):
            d.rectangle(P(x - 0.3, y) + P(x + 0.3, y + 0.25), fill=ln)
    if kind == 'happy':
        mouth = [(5.6, 5.2), (7.0, 5.9), (9.0, 6.1), (11.0, 5.9), (12.4, 5.2)]
    elif kind == 'surprised':
        d.ellipse(P(8.3, 4.9) + P(9.7, 6.2), fill=ln); mouth = None
    elif chibi:
        mouth = [(7.4, 5.9), (8.2, 5.6), (9.0, 5.75), (9.8, 5.6), (10.6, 5.9)]
    else:
        mouth = [(4.4, 6.3), (5.6, 5.85), (7.4, 5.55), (9.0, 5.45), (10.6, 5.55), (12.4, 5.85), (13.6, 6.3)]
        if kind == 'angry': mouth = [(4.8, 6.3), (6.4, 5.7), (9.0, 5.4), (11.6, 5.7), (13.2, 6.3)]
    if mouth:
        line(mouth, 0.16)
        fl, fr = mouth[1], mouth[-2]
        for fx, fy in ((fl[0], fl[1]), (fr[0], fr[1])):                                    # two little fangs, pointing up
            up = kind != 'happy'
            d.polygon([P(fx - 0.4, fy), P(fx + 0.4, fy), P(fx, fy - 0.8 if up else fy + 0.8)], fill=hexc('#ffffff'), outline=ln)
    if chibi:
        for cx in (4.0, 14.0):
            d.ellipse(P(cx - 0.9, 4.8) + P(cx + 0.9, 5.6), fill=hexc('#f0b4c8'))
    return im


def swim(frames=8, **base):
    """a swim cycle's phase angles (radians)"""
    return [2 * math.pi * i / frames for i in range(frames)]

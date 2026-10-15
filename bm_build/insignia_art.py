"""The followers' chest insignias, as pixel art from the owner's drawings (2.79):

- Emma's: a pink five-petal flower - each petal outlined, a pale streak down its middle - with a faceted yellow gem at its
  heart. On her model the flower is a thin plate on her chest and the gem a small block raised off it.
- Leo's: the sunken kingdom's insignia - a pale-blue drop that opens into two horns at the top (a slit between them), a
  drop-shaped window inside with a small wave at its foot, and a magenta gem in the window. Flat, on his tabard and cape.

Each returns an RGBA image on a transparent ground (supersampled, then thresholded: hard pixel edges)."""
import math
from PIL import Image

SS = 6                                        # (supersampling per pixel)


def _hex(c):
    c = c.lstrip('#'); return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def _mask(w, h, inside):
    """{(x, y): value} for the pixels whose majority of subsamples inside(fx, fy) says not None (the commonest value wins)"""
    out = {}
    for y in range(h):
        for x in range(w):
            votes = {}
            for j in range(SS):
                for i in range(SS):
                    v = inside(x + (i + 0.5) / SS, y + (j + 0.5) / SS)
                    if v is not None: votes[v] = votes.get(v, 0) + 1
            if votes and sum(votes.values()) * 2 >= SS * SS:
                out[(x, y)] = max(votes, key=votes.get)
    return out


# ---------------------------------------------------------------- Emma: the flower brooch
FL_OUT, FL_PET, FL_LIT, FL_HI, FL_GOLD = '#a3267c', '#e46ac2', '#f7a8df', '#ffd6f2', '#f2c832'


def emma_flower(n=16):
    """the five petals on an n x n ground (the gem goes on top, raised - see emma_gem); its heart is painted gold too"""
    c = n / 2; R = n / 2 - 0.3

    def petal(fx, fy):
        dx, dy = fx - c, fy - c
        r = math.hypot(dx, dy)
        if r < 0.1: return (0, 0.0, 0.0)
        best = None
        for k in range(5):
            phi = math.radians(-90 + 72 * k)
            s = dx * math.cos(phi) + dy * math.sin(phi); t = -dx * math.sin(phi) + dy * math.cos(phi)
            if s < 0: continue
            u = s / R
            if u > 1: continue
            half = 0.36 * R * (math.sin(math.pi * min(1, u * 1.05)) ** 0.75) + (0.12 * R if u < 0.3 else 0)
            if abs(t) <= half:
                q = abs(t) / max(half, 1e-6)
                if best is None or q < best[2]: best = (k, u, q)
        return best

    m = _mask(n, n, lambda fx, fy: (lambda p: None if p is None else p[0])(petal(fx, fy)))
    im = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    for (x, y), k in m.items():
        p = petal(x + 0.5, y + 0.5)
        edge = any((x + ax, y + ay) not in m or m[(x + ax, y + ay)] != k for ax, ay in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        col = FL_PET
        if p is not None:
            _k, u, q = p
            if u > 0.32 and q < 0.38: col = FL_LIT
            if 0.45 < u < 0.7 and q < 0.18 and k in (0, 1, 4): col = FL_HI          # (lit from above: the upper petals catch it)
        if edge: col = FL_OUT
        if math.hypot(x + 0.5 - c, y + 0.5 - c) < n * 0.14: col = FL_GOLD
        im.putpixel((x, y), _hex(col))
    return im


GEM = {'O': '#8a6410', 'H': '#fffbd8', 'L': '#ffe866', 'T': '#f7d43c', 'M': '#e2b022', 'D': '#b8840e'}
GEM_ROWS = ['..OOOO..', '.OHLLLO.', 'OHLTTLMO', 'OLTTTTMO', 'OLTHTTMO', 'OLTTTTMO', 'OLTTTMMO', 'OMTTTMDO', '.OMMMDO.', '..OOOO..']


def emma_gem():
    """the gem's face: 8 x 10, an emerald cut - a lit table, darker facets low and right, a glint"""
    im = Image.new('RGBA', (8, 10), (0, 0, 0, 0))
    for y, row in enumerate(GEM_ROWS):
        for x, ch in enumerate(row):
            if ch != '.': im.putpixel((x, y), _hex(GEM[ch]))
    return im


# ---------------------------------------------------------------- Leo: the sunken kingdom's insignia
LB_OUT, LB_FILL, LB_LIT, LB_GEM, LB_GEM_DK, LB_GEM_LT = '#3a7f92', '#a6dbe9', '#c8ecf5', '#a02a80', '#6e1858', '#cc5aa8'


def leo_badge(w=20, h=22):
    """the drop with its horns and window, the gem in the window; w x h on a transparent ground"""
    cx = w / 2; sx, sy = w / 20, h / 22                  # (designed on 20 x 22)

    def body(fx, fy):
        X, Y = (fx - cx) / sx, fy / sy                   # (design units: X from the middle, Y down from the top)
        a = abs(X)
        # the outer edge: two horns rising from the round foot, tips by the middle at the top
        if Y < 0.5 or Y > 21.8: return None
        if Y >= 13.0:
            if a > math.sqrt(max(0.0, 8.6 ** 2 - (Y - 13.2) ** 2)): return None
        else:
            o = 2.5 + (8.6 - 2.5) * (((Y - 0.5) / 12.5) ** 0.55)
            if a > o: return None
        # the window: a slit between the horns, opening into a drop; a little wave at its foot
        if Y < 5.0:
            win = 0.75
        elif Y < 19.0:
            win = max(0.75, 3.3 * (math.sin(math.pi * (Y - 4.2) / 15.2) ** 0.65))
        else:
            win = 0.0
        if Y > 16.6 and math.hypot(X - 1.6, Y - 17.9) < 1.35: win = 0.0          # (the wave)
        if a < win: return None
        return 1

    m = _mask(w, h, body)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    for (x, y) in m:
        edge = any((x + ax, y + ay) not in m for ax, ay in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        X = (x + 0.5 - cx) / sx
        col = LB_OUT if edge else (LB_LIT if X < -2.0 and 6 < (y + 0.5) / sy < 15 else LB_FILL)     # (a pale catch-light on the left horn)
        im.putpixel((x, y), _hex(col))

    # the gem, in the window: a brilliant cut - a flat top, its crown, a point below
    def gem(fx, fy):
        X, Y = (fx - cx) / sx, fy / sy
        top, girdle, point = 9.4, 10.9, 14.9
        if Y < top or Y > point: return None
        half = (1.9 + (2.9 - 1.9) * (Y - top) / (girdle - top)) if Y < girdle else 2.9 * (point - Y) / (point - girdle)
        if abs(X) > half: return None
        if Y < girdle: return 'L' if X < -0.6 else ('D' if X > 1.2 else 'M')
        return 'D' if X > 0.4 else 'M'
    g = _mask(w, h, gem)
    for (x, y), v in g.items():
        im.putpixel((x, y), _hex({'L': LB_GEM_LT, 'M': LB_GEM, 'D': LB_GEM_DK}[v]))
    return im


def sheet(path):
    """a big preview of the three"""
    tiles = [emma_flower(16), emma_gem(), leo_badge(20, 22), leo_badge(16, 16)]
    W = sum(t.width * 14 + 20 for t in tiles); H = max(t.height for t in tiles) * 14 + 20
    out = Image.new('RGBA', (W, H), (60, 110, 170, 255)); x = 10
    for t in tiles:
        out.alpha_composite(t.resize((t.width * 14, t.height * 14), Image.NEAREST), (x, 10)); x += t.width * 14 + 20
    out.save(path)


if __name__ == '__main__':
    import sys
    sheet(sys.argv[1] if len(sys.argv) > 1 else '/tmp/insignias.png')

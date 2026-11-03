"""KillerWatt's Tendrils, worn (2.54): skins for the equipment 'wings' layer (the elytra model).

The elytra texture is 64x32; each wing is a 10x20x2 box at texOffs (22,0). We draw at 4x (256x128) and paint only the
wing's SOUTH face - the one that faces away from your back (the model renders no-cull, so it shows from the front too).
On that face column 0 is the wing's pivot (your shoulder-blade, the outer edge) and the top row is where it hangs from;
the spine runs from about column 5 at the top (20 at 4x) to column 10 at the bottom. The right wing is the same face, mirrored.
"""
import math
from PIL import Image, ImageDraw

S = 4                               # texture scale (64x32 -> 256x128)
FACE = (36 * S, 2 * S)              # the south face's top-left; it is 10x20 (x S)
W, H = 10 * S, 20 * S
OUT, BODY, HOT, CORE = (14, 40, 30, 255), (242, 212, 44, 255), (255, 240, 120, 255), (255, 252, 222, 255)
GREEN, TEAL = (46, 154, 74, 255), (29, 122, 92, 255)

# (points on the 40x80 face, start width) - each a jagged bolt from the spine plate out across your back
LOOKS = {
    # OFFENSE: spread - one sweeps out and down past your hip, one reaches out over your shoulder, one hangs down the spine
    'kw_tendrils': [([(20, 6), (15, 16), (20, 23), (12, 35), (16, 42), (8, 55), (11, 61), (4, 72), (1, 78)], 7),
                    ([(18, 5), (12, 9), (14, 15), (6, 18), (8, 24), (2, 27), (0, 33)], 6),
                    ([(23, 9), (24, 22), (30, 30), (29, 44), (35, 52), (34, 62), (38, 68)], 5)],
    # RANGED: drawn in and coiled, the tips charged blue-white
    'kw_tendrils_r': [([(20, 6), (16, 15), (20, 21), (12, 30), (15, 36), (7, 44), (4, 38), (8, 33)], 7),
                      ([(18, 5), (12, 9), (14, 14), (6, 16), (4, 11), (8, 8)], 6),
                      ([(23, 9), (24, 20), (29, 27), (27, 36), (23, 33)], 5)],
}
LOOKS['kw_tendrils_s'] = LOOKS['kw_tendrils']        # the strike flash: the same spread, white-hot


def _bolt(d, pts, w0, body, core, outline=OUT):
    n = len(pts) - 1
    ws = [max(2, round(w0 - (w0 - 2) * i / n)) for i in range(n)]
    for (a, b), w in zip(zip(pts, pts[1:]), ws):             # outline first, under everything
        d.line([a, b], fill=outline, width=w + 4, joint='curve')
        d.ellipse([a[0] - (w + 4) / 2, a[1] - (w + 4) / 2, a[0] + (w + 4) / 2, a[1] + (w + 4) / 2], fill=outline)
    for (a, b), w in zip(zip(pts, pts[1:]), ws):
        d.line([a, b], fill=body, width=w, joint='curve')
        d.ellipse([a[0] - w / 2, a[1] - w / 2, a[0] + w / 2, a[1] + w / 2], fill=body)
    for (a, b), w in zip(zip(pts, pts[1:]), ws):
        d.line([a, b], fill=core, width=max(1, w // 3))
    # barbs: a white-hot spur off every other kink, pointing back the way the bolt came
    for i in range(1, n, 2):
        (px, py), (qx, qy) = pts[i - 1], pts[i]
        bx, by = qx + (qx - px) * 0.35, qy - 3
        d.line([(qx, qy), (bx, by)], fill=outline, width=4)
        d.line([(qx, qy), (bx, by)], fill=core, width=2)


def skin(name):
    im = Image.new('RGBA', (64 * S, 32 * S), (0, 0, 0, 0))
    face = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(face)
    hot = name == 'kw_tendrils_s'
    for pts, w0 in LOOKS[name]:
        if hot:
            _bolt(d, pts, w0 + 1, HOT, CORE, outline=(60, 50, 10, 255))
        else:
            _bolt(d, pts, w0, BODY, CORE)
    if name == 'kw_tendrils_r':                     # charged tips: blue-white sparks
        for pts, _w in LOOKS[name]:
            x, y = pts[-1]
            for dx, dy in ((0, 0), (-2, -2), (2, -1), (-1, 2), (2, 2)):
                d.rectangle([x + dx - 1, y + dy - 1, x + dx, y + dy], fill=(170, 225, 255, 255))
    if hot:                                         # stray sparks off the strike
        for x, y in ((6, 40), (18, 50), (4, 20), (24, 66), (30, 74), (10, 30)):
            d.line([(x, y), (x + 3, y - 2), (x + 1, y - 4)], fill=CORE, width=1)
    # the spine plate the tendrils grow from (the two wings overlap here, so it reads as one plate)
    d.rounded_rectangle([13, 0, 27, 12], radius=3, fill=OUT)
    d.rounded_rectangle([15, 1, 26, 10], radius=2, fill=GREEN)
    d.rectangle([17, 3, 23, 8], fill=TEAL)
    d.rectangle([19, 4, 21, 7], fill=CORE if not hot else (255, 255, 255, 255))
    im.paste(face, FACE)
    return unshare(im)


# 3.0g: NO Z-FIGHTING. Both wings wear this one face (the right one mirrored) and their faces lie in one plane: from the spine
# out past it they overlap - your back, the plate and the bolts' roots flickered between the two. Each wing now keeps only its own
# side of the spine where the other covers it (the vanilla elytra: wings 10x20x2 inflated by 1, pivots at x=+-5, tilted 15 degrees).
_TILT = 0.2617994


def _world(c, r):
    """face texel (column c from the pivot, row r from the top; may be fractional) -> (x, y) on the left wing's plane"""
    rx, ry = 1 - 1.2 * c, -1 + 1.1 * r                       # (the inflated box: 12 x 22 over 10 x 20 texels)
    co, si = math.cos(-_TILT), math.sin(-_TILT)
    return 5 + co * rx - si * ry, si * rx + co * ry


def _face(x, y):
    """the inverse: a point on the plane -> the left wing's face texel (c, r)"""
    co, si = math.cos(-_TILT), math.sin(-_TILT)
    dx = x - 5
    rx, ry = co * dx + si * y, -si * dx + co * y
    return (1 - rx) / 1.2, (ry + 1) / 1.1


def partner(c, r):
    """the texel of the other wing's face lying on this one, when this one is on the far side of the spine (else None)"""
    x, y = _world(c, r)
    if x >= 0: return None
    mc, mr = _face(-x, y)
    return (mc, mr) if 0 <= mc < 10 and 0 <= mr < 20 else None


def unshare(im):
    """where both wings paint the same spot, the wing on its own side of the spine keeps it (where only one does, it stays)"""
    px = im.load()
    for fy in range(H):
        for fx in range(W):
            if not px[FACE[0] + fx, FACE[1] + fy][3]: continue
            for ox, oy in ((0.5, 0.5), (0.02, 0.02), (0.98, 0.02), (0.02, 0.98), (0.98, 0.98)):      # (the whole texel: its partner can straddle two)
                q = partner((fx + ox) / S, (fy + oy) / S)
                if q and px[FACE[0] + min(W - 1, int(q[0] * S)), FACE[1] + min(H - 1, int(q[1] * S))][3]:
                    px[FACE[0] + fx, FACE[1] + fy] = (0, 0, 0, 0); break
    return im


def harness():
    """the humanoid layer: a green spine plate high on your back and a strap over each shoulder (64x32 armour layout)"""
    im = Image.new('RGBA', (64, 32), (0, 0, 0, 0))
    px = im.putpixel
    # body back face: (32,20) 8x12; front face: (20,20) 8x12; top: (20,16) 8x4
    for x in range(34, 38):
        for y in range(20, 26):
            px((x, y), GREEN if 21 <= y <= 24 and 35 <= x <= 36 else TEAL)
    px((35, 22), CORE); px((36, 23), CORE)
    for y in range(20, 32):                          # shoulder straps, front and back
        for x in (21, 26):
            px((x, y), (40, 44, 48, 255)) if y < 26 else None
        for x in (33, 38):
            px((x, y), (40, 44, 48, 255)) if y < 28 and not (34 <= x <= 37) else None
    for x in (21, 26):
        for y in (16, 17, 18, 19):
            px((x, y), (40, 44, 48, 255))
    return im

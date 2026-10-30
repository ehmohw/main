"""3.0b: THE PIXEL CREEPER's art (phase256) - a tiny creeper drawn by PixelLab (tools/pixellab/creeper_list.py; the export in
ref/pixellab/arcade/px_creeper: its eight turns, and a "hop" from the front and from behind), in the Arcade's own style (made
with Bit the rat trader as its style reference).

PixelLab's hop is a squash in place - the face pulls about as it squats (a frown, then a scowl). So only its bodies are kept:
  stand   the standing sprite (south)
  half    hop frame 2 - knees bent, feet a little apart
  crouch  hop frame 3 - squashed right down, feet splayed
each wearing the standing sprite's own head (the creeper's face never changes), its feet where the standing sprite's are. And
  flash   the standing sprite gone white-hot - a creeper about to... hiss (only hiss)
Every frame has a back: its own outline filled from the north view (pxart._back_of - no face on the back of the head).
The airborne part of a hop isn't drawn: the companion's display rises and falls (its translation, interpolated); the frame
and display-case copy (FRAMED, one animated strip) has the rise baked in, so it hops in place on its own, no commands at all.
The icon (16 x 16): the standing sprite boiled down to the vanilla creeper's own pattern - an 8 x 8 head with the creeper
face, a 4-wide body, four feet - its greens taken from PixelLab's (the commonest colour in each patch of its head and body)."""
import os
from PIL import Image

import pxart

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = 'px_creeper'
SRC = os.path.join(HERE, 'ref', 'pixellab', 'arcade', KEY, 'Idle')
N = 64                                   # (the companion's frames: a 64 canvas, feet on row 59)
HEAD = (4, 32)                           # (the standing sprite's head: rows 4..31 - the face never changes)
FRAMES = ('stand', 'half', 'crouch', 'flash')
PFX = 'pxcr_'
HEIGHT = 0.55                            # (the companion stands this tall, in blocks)
PX_H = 56                                # (the standing sprite's height in pixels: rows 4..59)
_C = {}


def _img(*p):
    return Image.open(os.path.join(SRC, *p)).convert('RGBA')


def _onto(fr, head):
    """an animation frame (an 80 canvas) on the 64 canvas, its feet on the standing sprite's row and centred as it, wearing the
    standing head where the frame's own head is (its head rows found from the top of the frame)"""
    bb = fr.getbbox()
    c = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    dx, dy = -8, 59 - (bb[3] - 1)
    c.alpha_composite(fr, (dx, dy))
    top = bb[1] + dy                                                    # (its head's top row, on the 64 canvas)
    c.paste(Image.new('RGBA', (N, HEAD[1] - HEAD[0]), (0, 0, 0, 0)), (0, top))
    c.alpha_composite(head, (0, top))
    return c


def _flash(im):
    """white-hot: every colour most of the way to white, the black outline and face kept"""
    out = im.copy(); px = out.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a and r + g + b > 90:
                px[x, y] = (r + (255 - r) * 7 // 10, g + (255 - g) * 7 // 10, b + (255 - b) * 7 // 10, a)
    return out


def fronts():
    if 'f' not in _C:
        stand = _img('rotations', 'south.png')
        head = Image.new('RGBA', (N, HEAD[1] - HEAD[0]), (0, 0, 0, 0)); head.alpha_composite(stand.crop((0, HEAD[0], N, HEAD[1])))
        hop = lambda i: _img('animations', 'hop', 'south', f'frame_{i:03d}.png')
        _C['f'] = {'stand': stand, 'half': _onto(hop(2), head), 'crouch': _onto(hop(3), head), 'flash': _flash(stand)}
    return _C['f']


def _parts(im):
    """(head, body, feet) boxes: the head from the top down to where it narrows into the body, the feet from where it widens again"""
    a = im.split()[3].load()
    rows = []
    for y in range(im.height):
        xs = [x for x in range(im.width) if a[x, y] >= 128]
        if xs: rows.append((y, min(xs), max(xs) + 1, len(xs)))
    hw = max(r[3] for r in rows[:6])
    i = next(k for k, r in enumerate(rows) if k > 4 and r[3] <= hw - 4)            # (the body: narrower than the head)
    bw = rows[i][3]
    j = next((k for k, r in enumerate(rows) if k > i + 3 and r[2] - r[1] > bw + 1), len(rows) - 2)   # (the feet: wider than the body)
    box = lambda rs: (min(r[1] for r in rs), rs[0][0], max(r[2] for r in rs), rs[-1][0] + 1)
    return box(rows[:i]), box(rows[i:j]), box(rows[j:])


def _back(front, north):
    """a back for a front frame: the north view's head, body and feet, each fitted (whole pixels, nearest) over the front's own
    head, body and feet - the same outline seen from behind, every pixel of it filled, no face. (pxart._back_of lines the views up
    feet to feet: the north view is shorter than the front - its top showed as a black band)"""
    out = Image.new('RGBA', front.size, (0, 0, 0, 0))
    for fb, nb in zip(_parts(front), _parts(north)):
        part = north.crop(nb).resize((fb[2] - fb[0], fb[3] - fb[1]), Image.NEAREST)
        out.alpha_composite(part, (fb[0], fb[1]))
    fa, op = front.load(), out.load()
    res = Image.new('RGBA', front.size, (0, 0, 0, 0)); rp = res.load()
    for y in range(front.height):
        solid = [x for x in range(front.width) if op[x, y][3] >= 128]
        for x in range(front.width):
            if fa[x, y][3] < 128: continue
            rp[x, y] = op[x, y] if op[x, y][3] >= 128 else (op[min(solid, key=lambda q: abs(q - x)), y] if solid else (24, 24, 24, 255))
    return res


def backs():
    if 'b' not in _C:
        F = fronts()
        north = _img('rotations', 'north.png')
        hop = lambda i: _img('animations', 'hop', 'north', f'frame_{i:03d}.png')
        st = _back(F['stand'], north)
        _C['b'] = {'stand': st, 'half': _back(F['half'], hop(2)), 'crouch': _back(F['crouch'], hop(3)), 'flash': _flash(st)}
    return _C['b']


# ---------------------------------------------------------------------- the framed one: a hop in place, one animated strip
FR_N = 128                                # (its canvas: room above the creeper to hop into)
FR_FEET = 124                             # (its feet's row when standing)
# (the strip's pictures: frame, how high (px); then the cycle: picture, ticks)
FR_PICS = [('stand', 0), ('half', 0), ('crouch', 0), ('stand', 6), ('stand', 12), ('stand', 15), ('flash', 0)]
FR_CYCLE = [(0, 30), (1, 2), (2, 3), (3, 2), (4, 2), (5, 3), (4, 2), (3, 2), (2, 3), (1, 2), (0, 14),
            (1, 2), (2, 3), (3, 2), (4, 2), (5, 3), (4, 2), (3, 2), (2, 3), (1, 2), (0, 40),
            (6, 3), (0, 3), (6, 3), (0, 3), (6, 4), (0, 30)]                # (two hops, a rest, a little hiss)


def strip():
    if 's' not in _C:
        F = fronts()
        S = Image.new('RGBA', (FR_N, FR_N * len(FR_PICS)), (0, 0, 0, 0))
        for i, (k, up) in enumerate(FR_PICS):
            S.alpha_composite(F[k], ((FR_N - N) // 2, i * FR_N + FR_FEET - 59 - up))
        _C['s'] = S
    return _C['s']


def strip_meta():
    return {'animation': {'interpolate': False, 'frames': [{'index': i, 'time': t} for i, t in FR_CYCLE]}}


def framed_model():
    """a flat quad, 32 x 32 units (two blocks at scale 1), the creeper's face on both sides (seen through a frame from either
    way round), its feet just above the model's floor: centred in an item frame, standing on a display case's cushion"""
    t = f'bm:block/{PFX}hop'
    return ({'f': t}, [{'from': [-8, 0, 8], 'to': [24, 32, 8], 'shade': False,
                        'faces': {'north': {'uv': [0, 0, 16, 16], 'texture': '#f'}, 'south': {'uv': [16, 0, 0, 16], 'texture': '#f'}}}])


# (the framed model's extent - for phase134's display case: lowest point, height (the hop's top), left-right, back-front, in blocks
#  at scale 1 in an item display, which shows a model centred on it)
_U = 32.0 / FR_N / 16.0                   # (blocks a pixel)
FIT = (round((32 - FR_FEET * 32.0 / FR_N - 8) / 16, 4), round((PX_H + 15) * _U, 4), round(-13 * _U, 4), round(13 * _U, 4), -0.02, 0.02)


# ---------------------------------------------------------------------- the icon
_FACE = ['........',
         '........',
         '.XX..XX.',
         '.XX..XX.',
         '...XX...',
         '..XXXX..',
         '..XXXX..',
         '..X..X..']


def _patches(im, box, w, h):
    """the commonest green in each of w x h patches of box (black and near-black left out)"""
    x0, y0, x1, y1 = box
    px = im.load()
    out = []
    for j in range(h):
        row = []
        for i in range(w):
            cnt = {}
            for y in range(y0 + (y1 - y0) * j // h, y0 + (y1 - y0) * (j + 1) // h):
                for x in range(x0 + (x1 - x0) * i // w, x0 + (x1 - x0) * (i + 1) // w):
                    c = px[x, y]
                    if c[3] >= 128 and sum(c[:3]) > 120:
                        cnt[c[:3]] = cnt.get(c[:3], 0) + 1
            row.append(max(cnt, key=cnt.get) + (255,) if cnt else None)
        out.append(row)
    return out


def icon():
    if 'i' not in _C:
        st = fronts()['stand']
        head = _patches(st, (20, 5, 44, 31), 8, 8)            # (inside the outline)
        body = _patches(st, (23, 32, 41, 49), 4, 4)
        feet = _patches(st, (21, 50, 43, 59), 4, 2)
        im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); px = im.load()
        K = (24, 24, 24, 255)
        seen = [c for r in head + body for c in r if c]
        G = max(set(seen), key=seen.count)                    # (a patch with no green in it - the face's: the commonest green)
        # (three greens, as a vanilla icon has: PixelLab's own, the darkest, the commonest and the lightest - each patch the nearest)
        lum = lambda c: c[0] * 3 + c[1] * 6 + c[2]
        tones = [min(seen, key=lum), G, max(seen, key=lum)]
        near = lambda c: c and min(tones, key=lambda t: sum((a - b) ** 2 for a, b in zip(t, c)))
        head, body, feet = ([[near(c) for c in r] for r in P] for P in (head, body, feet))
        for y in range(8):
            for x in range(8):
                px[4 + x, 1 + y] = K if _FACE[y][x] == 'X' else (head[y][x] or G)
        for y in range(4):
            for x in range(4):
                px[6 + x, 9 + y] = body[y][x] or G
        for y in range(2):
            for i, x in enumerate((4, 5, 10, 11)):
                px[x, 13 + y] = feet[y][i] or G
        # the outline (black: vanilla.process turns an outer black edge into a deep shade of what it wraps)
        a = im.copy().load()
        for y in range(16):
            for x in range(16):
                if a[x, y][3]: continue
                if any(0 <= x + dx < 16 and 0 <= y + dy < 16 and a[x + dx, y + dy][3] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    px[x, y] = K
        _C['i'] = im
    return _C['i']


# ---------------------------------------------------------------------- the pack's pieces
def textures():
    T = {f'{PFX}{k}': im for k, im in fronts().items()}
    T.update({f'{PFX}b_{k}': im for k, im in backs().items()})
    T[f'{PFX}hop'] = strip()
    return T


def models():
    M = {f'{PFX}{k}': pxart.Sprite.quad(None, f'{PFX}{k}', f'{PFX}b_{k}') for k in FRAMES}
    M[f'{PFX}framed'] = framed_model()
    return M


def item_defs(R2, iid):
    """the companion's frame-picker (bm:pxcr, by its custom_model_data), the strip's .mcmeta, and the item itself: its icon in
    the hand and the inventory, the hopping creeper in an item frame or a display case (display context 'fixed')"""
    mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
    R2.wj('assets/bm/items/pxcr.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                  'cases': [{'when': k, 'model': mdl(f'{PFX}{k}')} for k in FRAMES], 'fallback': mdl(f'{PFX}stand')}})
    R2.wj(f'assets/bm/textures/block/{PFX}hop.png.mcmeta', strip_meta())
    R2.wj(f'assets/bm/items/{iid}.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:display_context',
                                                    'cases': [{'when': 'fixed', 'model': mdl(f'{PFX}framed')}], 'fallback': mdl(iid)}})


if __name__ == '__main__':                 # (a look at every piece, big: python3 px_creeper_art.py out.png)
    import sys
    F, B = fronts(), backs()
    W = 4
    sheet = Image.new("RGBA", ((N + 4) * len(FRAMES) + 66 * len(FR_PICS) + 8, max(2 * N, FR_N) + 70), (200, 200, 210, 255))
    for i, k in enumerate(FRAMES):
        sheet.alpha_composite(F[k], (i * (N + 4), 0)); sheet.alpha_composite(B[k], (i * (N + 4), N + 4))
    x = len(FRAMES) * (N + 4)
    s = strip()
    for i in range(len(FR_PICS)):
        sheet.alpha_composite(s.crop((0, i * FR_N, FR_N, (i + 1) * FR_N)).crop((32, 40, 96, 128)), (x + i * 66, 0))
    sheet.alpha_composite(icon().resize((64, 64), Image.NEAREST), (x, 100))
    sheet.alpha_composite(icon(), (x + 70, 100))
    sheet.resize((sheet.width * W, sheet.height * W), Image.NEAREST).save(sys.argv[1] if len(sys.argv) > 1 else 'px_creeper.png')

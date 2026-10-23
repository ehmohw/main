"""2.94: Dennis's searing throws - a diamond and four ingots (iron, gold, copper, netherite) heated until they glow, from the
game's own item textures: each pixel's brightness read off the forge's ramp (deep cherry red where it was darkest, orange,
then yellow-white where it shone), the metal's own colour kept underneath, and a one-pixel orange glow round the edge. Shown
full-bright on a billboarded display, tumbling through the air."""
import os
from PIL import Image

VANILLA = '/home/claude/mc263/client/assets/minecraft/textures/item'
THROWN = ('diamond', 'iron_ingot', 'gold_ingot', 'copper_ingot', 'netherite_ingot')
# how far each is heated toward the ramp, and how high up the ramp it gets: iron white-hot, gold a yellow glow, copper orange-red;
# netherite stays dark, glowing cherry-red from within; the diamond keeps its blue, its dark edge gone red-hot round it
HEAT = {'diamond': 0.0, 'iron_ingot': 0.75, 'gold_ingot': 0.62, 'copper_ingot': 0.7, 'netherite_ingot': 0.85}
TOP = {'iron_ingot': 1.0, 'gold_ingot': 0.86, 'copper_ingot': 0.66, 'netherite_ingot': 0.42}
RAMP = [(0.0, (70, 6, 2)), (0.25, (170, 22, 4)), (0.5, (255, 92, 10)), (0.75, (255, 186, 40)), (1.0, (255, 250, 214))]


def _ramp(t):
    t = max(0.0, min(1.0, t))
    for (a, ca), (b, cb) in zip(RAMP, RAMP[1:]):
        if t <= b:
            k = (t - a) / (b - a)
            return tuple(round(ca[i] + (cb[i] - ca[i]) * k) for i in range(3))
    return RAMP[-1][1]


def _src(name):
    p = os.path.join(VANILLA, name + '.png')
    if os.path.exists(p):
        return Image.open(p).convert('RGBA')
    import zipfile, io                                                                  # (no extracted assets: the client jar)
    with zipfile.ZipFile('/home/claude/mc263/client.jar') as z:
        return Image.open(io.BytesIO(z.read(f'assets/minecraft/textures/item/{name}.png'))).convert('RGBA')


def hot(name):
    """the item, glowing hot - 16 x 16 like the original, with its glow ring inside the frame"""
    im = _src(name); px = im.load(); W, H = im.size
    vals = [(0.299 * r + 0.587 * g + 0.114 * b) / 255 for y in range(H) for x in range(W) for (r, g, b, a) in [px[x, y]] if a > 0]
    lo, hi = min(vals), max(vals)
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0)); po = out.load()
    k = HEAT[name]
    for y in range(H):
        for x in range(W):
            r, g, b, a = px[x, y]
            if not a:
                continue
            t = ((0.299 * r + 0.587 * g + 0.114 * b) / 255 - lo) / max(1e-6, hi - lo)
            if name == 'diamond':                                                       # (its outline red-hot; the stone itself lit up)
                if t < 0.3:
                    po[x, y] = _ramp(0.35 + t) + (255,)
                else:
                    po[x, y] = tuple(min(255, round(c * 1.12 + 18)) for c in (r, g, b)) + (255,)
                continue
            t = (0.18 + 0.82 * t ** 0.8) * TOP[name]
            h = _ramp(t)
            po[x, y] = tuple(round(h[i] * k + (r, g, b)[i] * (1 - k)) for i in range(3)) + (255,)
    for y in range(H):                                                                   # the glow: a soft orange ring just outside
        for x in range(W):
            if px[x, y][3]:
                continue
            n = sum(1 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + dx < W and 0 <= y + dy < H and px[x + dx, y + dy][3])
            if n:
                po[x, y] = (255, 120, 20, 150 if n == 1 else 200)
    return out


def textures():
    return {f'sear_{n}': hot(n) for n in THROWN}


if __name__ == '__main__':
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else '/tmp/sear.png'
    S = 10
    sheet = Image.new('RGBA', (len(THROWN) * (16 * S + 20), 2 * (16 * S + 20)), (40, 36, 44, 255))
    for i, n in enumerate(THROWN):
        sheet.alpha_composite(_src(n).resize((16 * S, 16 * S), Image.NEAREST), (10 + i * (16 * S + 20), 10))
        sheet.alpha_composite(hot(n).resize((16 * S, 16 * S), Image.NEAREST), (10 + i * (16 * S + 20), 16 * S + 30))
    sheet.save(out)

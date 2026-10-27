"""2.95: the Buddies the Gem of Creativity conjures, cut out of the owner's own art (ref/owner/buddies/<name>.png): each crop's
background flood-filled away from its edges (the sky blue, the floor grey, the bulb's glow; pure white on the white sheets only),
stray scraps of neighbours dropped (only pieces of a good size kept), trimmed, brought down to 256 px.
    python3 tools/buddy_cut.py UPLOADS_DIR"""
import sys
from collections import deque
from PIL import Image

GROUP, SHEET1, SHEET2 = '928fab48-image.png', '4bfa45d3-image.png', 'a4aff836-image.png'
K = 4565 / 2000
sc = lambda b: tuple(int(v * K) for v in b)
BOXES = {'grace': (GROUP, sc((540, 0, 800, 230))), 'robo': (GROUP, sc((270, 210, 730, 430))), 'zapper': (GROUP, sc((30, 690, 290, 970))),
         'dessa': (GROUP, sc((150, 965, 380, 1205))), 'bubbles': (GROUP, sc((1345, 300, 1500, 440))), 'chase': (SHEET1, (480, 20, 810, 545)),
         'spike': (GROUP, sc((1460, 800, 1650, 1000))), 'limer': (SHEET2, (430, 630, 730, 1000)), 'chico': (GROUP, sc((350, 1150, 560, 1560))),
         'cheferoni': (SHEET1, (790, 380, 1180, 1200))}
BG_GROUP = [((126, 200, 220), 48), ((123, 143, 153), 40), ((110, 135, 145), 36), ((196, 226, 182), 40), ((205, 232, 190), 40), ((180, 220, 190), 36)]
BG_WHITE = [((255, 255, 255), 14)]


def cut(im, bg):
    px = im.load(); w, h = im.size; seen = bytearray(w * h); q = deque()
    close = lambda c: c[3] == 0 or any(sum((c[i] - b[i]) ** 2 for i in range(3)) < t * t for b, t in bg)
    for x in range(w): q.extend(((x, 0), (x, h - 1)))
    for y in range(h): q.extend(((0, y), (w - 1, y)))
    while q:
        x, y = q.popleft()
        if x < 0 or y < 0 or x >= w or y >= h or seen[y * w + x]: continue
        seen[y * w + x] = 1
        if close(px[x, y]):
            px[x, y] = (0, 0, 0, 0); q.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    # (scraps of the neighbours: keep only pieces of at least a fiftieth of the biggest)
    lab = [0] * (w * h); sizes = {}; n = 0
    for y0 in range(h):
        for x0 in range(w):
            if px[x0, y0][3] == 0 or lab[y0 * w + x0]: continue
            n += 1; lab[y0 * w + x0] = n; st = [(x0, y0)]; s = 0
            while st:
                x, y = st.pop(); s += 1
                for a, b in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= a < w and 0 <= b < h and not lab[b * w + a] and px[a, b][3]:
                        lab[b * w + a] = n; st.append((a, b))
            sizes[n] = s
    big = max(sizes.values())
    for y in range(h):
        for x in range(w):
            if lab[y * w + x] and sizes[lab[y * w + x]] < big / 50: px[x, y] = (0, 0, 0, 0)
    return im.crop(im.getbbox())


if __name__ == '__main__':
    U = sys.argv[1]
    for name, (src, box) in BOXES.items():
        im = Image.open(f'{U}/{src}').convert('RGBA').crop(box)
        c = cut(im, BG_GROUP if src == GROUP else BG_WHITE)
        c.thumbnail((256, 256), Image.LANCZOS)
        px = c.load()
        for y in range(c.height):
            for x in range(c.width):
                r, g, b, a = px[x, y]; px[x, y] = (r, g, b, 255 if a >= 110 else 0)
        c.save(f'ref/owner/buddies/{name}.png'); print(name, c.size)

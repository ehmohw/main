"""2.95 mockup: THE CREATIVITY GEM - the shard of the Ethereal Gem that broke away and gives the Buddies life (owner's art:
an elongated octagonal cut, every colour of the rainbow swirling out of its heart, little white doodles - notes, flowers,
a sketchbook - drifting inside it). A 3D cut: a raised table in the middle and a bevelled rim of eight facets, its swirl
painted once across the front (64x64) so it runs unbroken from facet to facet. Not wired yet - see the README's design notes.

    python3 mockups/creativity_gem.py OUT_RP     writes assets/bm/{models,textures}/item/creativity_gem* into OUT_RP"""
import colorsys, json, math, os, sys
from PIL import Image

N = 64                                    # texture px across the 16-unit face
W2, H2 = 5.6, 8.0                         # half width / half height of the outline (units)
CUT = 2.6                                 # the corners' cut
CX, CY = 8.0, 8.0


def outline_hw(y):
    """the octagon's half width at height y (0..16)"""
    d = abs(y - CY)
    if d > H2: return 0.0
    return W2 if d <= H2 - CUT else W2 - (d - (H2 - CUT)) * (W2 - (W2 - CUT * 0.95)) / CUT


def texture():
    im = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    for py in range(N):
        for px in range(N):
            x = (px + 0.5) * 16 / N; y = 16 - (py + 0.5) * 16 / N
            hw = outline_hw(y)
            if abs(x - CX) > hw: continue
            dx, dy = (x - CX) / W2, (y - CY) / H2
            r = math.hypot(dx, dy); a = math.atan2(dy, dx)
            h = ((a / (2 * math.pi)) + r * 0.55) % 1.0                     # the swirl: hue turns as it leaves the heart
            band = h * 8; f = band - int(band)                              # eight arms, as cut facets: flat colour, a soft seam
            h = (int(band) + (0 if f < 0.82 else (f - 0.82) / 0.18)) / 8
            s = 0.15 + 0.7 * min(1, r * 1.6); v = 1.0 - 0.1 * r              # a pale, glowing heart; rich colour out at the rim
            rr, gg, bb = colorsys.hsv_to_rgb(h, s, v)
            c = [int(rr * 255), int(gg * 255), int(bb * 255)]
            # facet seams: the eight spokes out to the corners, and the table's edge
            spoke = min(abs(((a + math.pi / 8) % (math.pi / 4)) - math.pi / 8), 9)
            if spoke < 0.035 and r > 0.25: c = [int(v_ * 0.82) for v_ in c]
            edge = hw - abs(x - CX)
            if 1.35 < edge < 1.6 or (0.62 < r < 0.68): c = [min(255, int(v_ * 1.12 + 18)) for v_ in c]
            if edge < 0.28: c = [42, 38, 58]                                # the dark outline
            im.putpixel((px, py), tuple(c) + (255,))
    # little white doodles drifting inside: notes, a flower, a sparkle (the owner's art)
    W = (255, 255, 255, 255)
    note = ['.##', '.#.', '.#.', '##.', '##.']
    flower = ['.#.', '###', '.#.']
    spark = ['.#.', '#.#', '.#.']
    for glyph, (gx, gy) in ((note, (22, 20)), (note, (40, 38)), (flower, (37, 18)), (flower, (20, 42)), (spark, (30, 30)),
                            (spark, (44, 28)), (note, (28, 46)), (spark, (17, 30))):
        for j, row in enumerate(glyph):
            for i, ch in enumerate(row):
                if ch == '#' and im.getpixel((gx + i, gy + j))[3]: im.putpixel((gx + i, gy + j), W)
    for gx, gy in ((19, 14), (45, 47), (33, 12), (25, 36), (42, 22)):   # glints
        if im.getpixel((gx, gy))[3]: im.putpixel((gx, gy), W)
    return im


def model():
    els = []
    uv = lambda x1, y1, x2, y2: [x1, 16 - y2, x2, 16 - y1]
    rim = lambda x1, y1, x2, y2: [x1, 16 - y2, x1 + 0.01, 16 - y2 + 0.01] if False else [x1, 16 - y2, x2, 16 - y1]
    step = 0.5
    y = CY - H2
    while y < CY + H2 - 1e-6:
        y2 = y + step; ym = (y + y2) / 2; hw = outline_hw(ym)
        if hw > 0.2:
            x1, x2 = CX - hw, CX + hw
            # the rim: thin; the table (inside 1.5 of the edge): deep
            els.append({'from': [x1, y, 7.0], 'to': [x2, y2, 9.0],
                        'faces': {'south': {'uv': uv(x1, y, x2, y2), 'texture': '#g'}, 'north': {'uv': uv(x2, y, x1, y2)[::1], 'texture': '#g'},
                                  'east': {'uv': uv(x2 - 1.2, y, x2 - 0.7, y2), 'texture': '#g'}, 'west': {'uv': uv(x1 + 0.7, y, x1 + 1.2, y2), 'texture': '#g'},
                                  'up': {'uv': uv(x1 + 0.7, y2 - 1.2, x2 - 0.7, y2 - 0.7), 'texture': '#g'}, 'down': {'uv': uv(x1 + 0.7, y + 0.7, x2 - 0.7, y + 1.2), 'texture': '#g'}}})
            ti = hw - 1.5
            if ti > 0.4 and abs(ym - CY) < H2 - 1.4:
                t1, t2 = CX - ti, CX + ti
                els.append({'from': [t1, y, 6.0], 'to': [t2, y2, 10.0],
                            'faces': {'south': {'uv': uv(t1, y, t2, y2), 'texture': '#g'}, 'north': {'uv': uv(t2, y, t1, y2), 'texture': '#g'},
                                      'east': {'uv': uv(t2 - 0.5, y, t2, y2), 'texture': '#g'}, 'west': {'uv': uv(t1, y, t1 + 0.5, y2), 'texture': '#g'},
                                      'up': {'uv': uv(t1, y2 - 0.5, t2, y2), 'texture': '#g'}, 'down': {'uv': uv(t1, y, t2, y + 0.5), 'texture': '#g'}}})
        y = y2
    disp = {'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]},
            'gui': {'rotation': [15, 25, 0], 'translation': [0, 0, 0], 'scale': [0.95, 0.95, 0.95]},
            'ground': {'rotation': [0, 0, 0], 'translation': [0, 2, 0], 'scale': [0.5, 0.5, 0.5]},
            'thirdperson_righthand': {'rotation': [0, 0, 0], 'translation': [0, 2.5, 1.5], 'scale': [0.5, 0.5, 0.5]},
            'firstperson_righthand': {'rotation': [0, -20, 0], 'translation': [1, 3, 0], 'scale': [0.6, 0.6, 0.6]}}
    return {'textures': {'g': 'bm:item/creativity_gem', 'particle': 'bm:item/creativity_gem'}, 'elements': els, 'display': disp}


if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(f'{out}/assets/bm/models/item', exist_ok=True); os.makedirs(f'{out}/assets/bm/textures/item', exist_ok=True)
    texture().save(f'{out}/assets/bm/textures/item/creativity_gem.png')
    json.dump(model(), open(f'{out}/assets/bm/models/item/creativity_gem.json', 'w'))
    print(len(model()['elements']), 'elements')

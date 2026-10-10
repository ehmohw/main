"""2.56: the follower Cecil, redrawn - a little shorter than Emma, a bigger hood, a fuller robe.

Four display parts, as before (body, head, eyes, staff arm); each model's joint is at (8, 8, 8). He faces -z; his
right is +x. Sizes (blocks): the robe stands 0.94 tall, the hood's crown at about 1.6 (Emma's head is at 1.75),
the hood 11.5 px wide; the staff reaches the ground. Joints relative to the host: head and eyes (0, 0.94, 0.06),
staff arm (-0.36, 0.84, 0.04), the body drawn from the ground (translation 0.5)."""
from PIL import Image, ImageDraw

HEAD_AT = (0, 0.94, 0.06)
ARM_AT = (-0.34, 0.86, 0.04)
HEAD_K = 0.9
BODY_KX, BODY_KZ = 0.74, 0.8            # (2.56b: slimmer - he was too chunky)
HEAD_KX, HEAD_KZ = 0.86, 0.9
TEX = {'r': 'bm:block/cec_robe', 'd': 'bm:block/cec_robe_dark', 'k': 'bm:block/cec_black', 'g': 'bm:block/cec_gold', 'w': 'bm:block/cec_wood',
       'p': 'bm:block/cec_crystal_poison', 'f': 'bm:block/cec2_face', 'y': 'bm:block/cec_eye', 'b': 'bm:block/cec2_button'}


def face_texture():
    """32 x 32: the smoky black face in the hood and - as in his portrait - a wide, jagged, open grey mouth: the teeth
    are just the zig-zag of its edges (no white). The eyes are their own glowing part."""
    N = 32
    im = Image.new('RGBA', (N, N), (22, 21, 25, 255)); d = ImageDraw.Draw(im)
    for r in range(12):                                         # a smoky lighter haze around the eyes, darker at the rim
        d.ellipse((2 + r * 0.7, 2 + r * 0.45, 30 - r * 0.7, 21 - r * 0.45), fill=(24 + r * 2, 23 + r * 2, 28 + r * 2, 255))
    MOUTH, EDGE = (72, 71, 78, 255), (98, 97, 104, 255)
    top = [(4, 18.5)] + [(x, 20.0 if i % 2 == 0 else 23.0) for i, x in enumerate(range(6, 28, 3))] + [(28, 18.5)]
    bot = [(27, 24.5)] + [(x, 28.4 if i % 2 == 0 else 25.4) for i, x in enumerate(range(25, 4, -3))] + [(5, 24.5)]
    d.polygon(top + bot, fill=MOUTH)
    d.line(top, fill=EDGE, width=1); d.line(bot + [bot[0]][:0], fill=EDGE, width=1)
    d.line([(4, 18.5), (3, 16.6)], fill=EDGE, width=1); d.line([(28, 18.5), (29, 16.6)], fill=EDGE, width=1)   # the corners curl up
    for x in (11, 21):                                          # a crease under each eye
        d.line([(x - 2, 15), (x + 2, 16)], fill=(14, 13, 16, 255), width=1)
    return im


def button_texture():
    """16 x 16: the round bone button at his collar, an X of thread"""
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((1, 1, 14, 14), fill=(212, 196, 120, 255), outline=(120, 104, 50, 255))
    d.line([(5, 5), (10, 10)], fill=(60, 50, 20, 255), width=2); d.line([(10, 5), (5, 10)], fill=(60, 50, 20, 255), width=2)
    return im


def models(cube):
    def c(fr, to, t, rot=None, faces=None):
        e = cube(fr, to, t, **({'faces': faces} if faces else {}))
        if rot: e['rotation'] = {'axis': rot[0], 'angle': rot[1], 'origin': list(rot[2])}
        return e
    # ---- BODY: a full bell of a robe, 15 px tall, hunched forward; the left claw hanging out front
    body = [c((1, 0, 2.5), (15, 1.4, 14.5), 'd'), c((1.6, 1.4, 3), (14.4, 6, 14), 'r'), c((2.4, 6, 3.6), (13.6, 10.5, 13.2), 'r'),
            c((3.2, 10.5, 3.4), (12.8, 14, 11.6), 'r'), c((3.6, 13.6, 3.2), (12.4, 15.2, 10.4), 'r'),
            c((5, 14.6, 2.9), (11, 15.4, 8.6), 'd'),                                                     # collar shadow
            c((3.4, 13.8, 2.6), (6.0, 16.6, 3.6), 'r', ('z', -22.5, (4.7, 13.8, 3.1))),                 # the collar's two points
            c((10.0, 13.8, 2.6), (12.6, 16.6, 3.6), 'r', ('z', 22.5, (11.3, 13.8, 3.1))),
            c((7.85, 1.4, 2.9), (8.15, 6, 3.0), 'd'), c((7.85, 6, 3.5), (8.15, 10.5, 3.6), 'd'), c((7.85, 10.5, 3.3), (8.15, 12.4, 3.4), 'd'),
            c((7.2, 12.4, 3.05), (8.8, 14.0, 3.25), 'b', faces=('north', 'east', 'west', 'up', 'down')),    # the bone button
            # a ragged hem: torn tongues of cloth hanging below the robe all round
            c((1.2, -0.6, 4), (3.2, 1.0, 5.2), 'd', ('x', -22.5, (2.2, 1.0, 4.6))), c((12.8, -0.6, 3.8), (14.6, 1.0, 5.0), 'd', ('x', -22.5, (13.7, 1.0, 4.4))),
            c((4.2, -0.4, 2.2), (6.6, 0.8, 3.0), 'd'), c((9.8, -0.5, 2.2), (12.2, 0.9, 3.0), 'd'),
            c((0.6, 0, 6.5), (1.4, 1.4, 10), 'd'), c((14.6, 0, 5), (15.4, 1.2, 8.5), 'd'),
            c((9.5, -0.4, 14.3), (12.5, 1.2, 15.1), 'd'), c((3, -0.3, 14.3), (5.6, 0.8, 15.0), 'd'), c((6.5, -0.5, 14.4), (8.4, 0.6, 14.9), 'd'),
            # his left sleeve with its flared, ragged cuff, and the long-fingered claw hanging out front
            c((0.7, 7.4, 4.2), (4.0, 13.6, 8.2), 'r', ('x', 22.5, (2.35, 13.4, 6.2))),
            c((0.3, 6.4, 2.6), (4.4, 8.4, 6.0), 'd', ('x', 22.5, (2.35, 8.4, 4.3))),
            c((1.0, 5.0, 2.4), (3.8, 7.0, 5.0), 'k')] + \
           [c((x, 3.3, 2.4), (x + 0.6, 5.2, 3.0), 'k', ('x', -22.5, (x + 0.3, 5.2, 2.7))) for x in (1.1, 2.1, 3.1)]
    # ---- HEAD: a big hood (12 wide, 12 tall), a deep face opening under an overhanging brim, the tip curling back
    face = c((3.4, 8.2, 2.9), (12.6, 17.2, 3.0), 'f', faces=('north',)); face['faces']['north']['uv'] = [0, 0, 16, 16]
    head = [c((2, 7, 3.0), (14, 19, 14), 'r'),
            c((1.6, 7, 1.4), (3.4, 19.2, 3.2), 'r'), c((12.6, 7, 1.4), (14.4, 19.2, 3.2), 'r'), c((1.6, 17.2, 1.4), (14.4, 19.6, 3.2), 'r'),
            c((2.0, 7, 1.8), (14.0, 7.6, 3.1), 'd'),
            c((2.4, 18.4, 0.6), (13.6, 19.6, 2.4), 'r', ('x', -22.5, (8, 19, 2.4))),                    # the brim
            c((0.8, 5.4, 4), (2.4, 9.6, 12.6), 'r'), c((13.6, 5.4, 4), (15.2, 9.6, 12.6), 'r'),          # draped onto the shoulders
            c((2.8, 6.6, 13.8), (13.2, 17.6, 14.8), 'r'), c((3.4, 19, 4.2), (12.6, 19.8, 12.8), 'r'),
            face,
            c((1.3, 9, 4.5), (2.0, 17, 12.6), 'r'), c((14.0, 9, 4.5), (14.7, 17, 12.6), 'r'),              # rounder sides
            # the tip: up from the back of the crown, bending over to his left, curling at the end
            c((5.4, 19, 8.4), (10.2, 21.6, 13.4), 'r'),
            c((4.6, 21.0, 9.2), (8.6, 24.4, 12.6), 'r', ('z', 22.5, (6.6, 21.0, 10.9))),
            c((2.8, 23.2, 9.8), (5.8, 25.8, 12.0), 'r', ('z', 45, (4.3, 23.2, 10.9))),
            c((1.4, 24.0, 10.2), (3.2, 26.0, 11.6), 'd', ('z', -22.5, (2.3, 24.0, 10.9))),
            # the stitched seam from his brow back over the crown
            c((7.8, 19, 1.6), (8.2, 19.8, 11.4), 'k')] + \
           [c((7.2, 19.75, z), (8.8, 19.95, z + 0.35), 'k') for z in (2.4, 4.0, 5.6, 7.2, 8.8, 10.4)]
    eyes = [c((4.0, 13.4, 2.75), (7.4, 14.9, 2.88), 'y', ('z', -22.5, (5.7, 14.15, 2.8))),
            c((8.6, 13.4, 2.75), (12.0, 14.9, 2.88), 'y', ('z', 22.5, (10.3, 14.15, 2.8)))]
    # ---- ARM: his right sleeve and claw on the crescent staff, which stands on the ground
    # (2.58: the arm hangs straight from his shoulder - a full robe sleeve with a ragged cuff - and the claw closes round the
    # staff just under it; the staff stands tall, its crescent above his hood)
    up, sz = 6.0, 3.7                                  # (sz: the staff sits back under the sleeve)
    arm = [c((5.7, 1.2, 5.6), (10.3, 9.2, 10.4), 'r'), c((5.4, 0.0, 5.2), (10.6, 1.6, 10.8), 'd'),                 # sleeve, cuff
           c((6.4, -1.4, 6.0), (9.6, 0.4, 9.6), 'k')] + \
          [c((x, -2.4, 5.7), (x + 0.6, -0.8, 6.3), 'k', ('x', 22.5, (x + 0.3, -0.8, 6.0))) for x in (6.5, 7.6, 8.7)] + \
          [c((7.3, -5.4, 3.45 + sz), (8.7, 17 + up, 4.85 + sz), 'w'), c((6.7, 15 + up, 3.0 + sz), (9.3, 18 + up, 5.3 + sz), 'g'),
           c((4.9, 13.6 + up, 3.5 + sz), (6.7, 19.4 + up, 4.7 + sz), 'g'), c((1.9, 18.4 + up, 3.5 + sz), (5.5, 19.8 + up, 4.7 + sz), 'g', ('z', -22.5, (5.3, 19.1 + up, 4.1 + sz))),
           c((1.9, 13.2 + up, 3.5 + sz), (5.5, 14.6 + up, 4.7 + sz), 'g', ('z', 22.5, (5.3, 13.9 + up, 4.1 + sz))),
           c((9.3, 13.6 + up, 3.5 + sz), (11.1, 19.4 + up, 4.7 + sz), 'g'), c((10.5, 18.4 + up, 3.5 + sz), (14.1, 19.8 + up, 4.7 + sz), 'g', ('z', 22.5, (10.7, 19.1 + up, 4.1 + sz))),
           c((10.5, 13.2 + up, 3.5 + sz), (14.1, 14.6 + up, 4.7 + sz), 'g', ('z', -22.5, (10.7, 13.9 + up, 4.1 + sz))),
           c((6.5, 18 + up, 2.8 + sz), (9.5, 23.6 + up, 5.6 + sz), 'p', ('y', 45, (8, 21 + up, 4.2 + sz))), c((7.2, 23.4 + up, 3.5 + sz), (8.8, 25.4 + up, 4.9 + sz), 'p', ('y', 45, (8, 24.4 + up, 4.2 + sz)))]
    def slim(els, kx, kz, o=(8, 0, 8.5)):
        """narrow and flatten (height unchanged)"""
        out = []
        for e in els:
            e = dict(e)
            f = lambda p: [round(o[0] + (p[0] - o[0]) * kx, 4), p[1], round(o[2] + (p[2] - o[2]) * kz, 4)]
            e['from'], e['to'] = f(e['from']), f(e['to'])
            if 'rotation' in e: e['rotation'] = dict(e['rotation'], origin=f(e['rotation']['origin']))
            out.append(e)
        return out
    body = slim(body, BODY_KX, BODY_KZ)
    head, eyes = slim(head, HEAD_KX, HEAD_KZ, (8, 0, 8)), slim(eyes, HEAD_KX, HEAD_KZ, (8, 0, 8))
    def scaled(els, k, o=(8, 7, 8)):
        """the hood drawn a touch smaller about the neck (k=0.9: 11.5 px across the rim)"""
        out = []
        for e in els:
            e = dict(e)
            e['from'] = [round(o[i] + (v - o[i]) * k, 4) for i, v in enumerate(e['from'])]
            e['to'] = [round(o[i] + (v - o[i]) * k, 4) for i, v in enumerate(e['to'])]
            if 'rotation' in e:
                e['rotation'] = dict(e['rotation'], origin=[round(o[i] + (v - o[i]) * k, 4) for i, v in enumerate(e['rotation']['origin'])])
            out.append(e)
        return out
    head, eyes = scaled(head, HEAD_K), scaled(eyes, HEAD_K)
    # (2.58) the staff's gem and his eyes glow in the dark (and the gem is translucent - its texture)
    for e in arm:
        if any(f['texture'] == '#p' for f in e['faces'].values()): e['light_emission'] = 15
    for e in eyes: e['light_emission'] = 15
    return {'cec2_body': (TEX, body), 'cec2_head': (TEX, head), 'cec2_eyes': (TEX, eyes), 'cec2_arm': (TEX, arm)}

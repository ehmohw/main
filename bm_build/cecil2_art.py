"""2.56: the follower Cecil, redrawn - a little shorter than Emma, a bigger hood, a fuller robe.

Four display parts, as before (body, head, eyes, staff arm); each model's joint is at (8, 8, 8). He faces -z; his
right is +x. Sizes (blocks): the robe stands 0.94 tall, the hood's crown at about 1.6 (Emma's head is at 1.75),
the hood 11.5 px wide; the staff reaches the ground. Joints relative to the host: head and eyes (0, 0.94, 0.06),
staff arm (-0.36, 0.84, 0.04), the body drawn from the ground (translation 0.5)."""
from PIL import Image, ImageDraw

HEAD_AT = (0, 0.94, 0.06)
ARM_AT = (-0.36, 0.84, 0.04)
HEAD_K = 0.9
BODY_KX, BODY_KZ = 0.74, 0.8            # (2.56b: slimmer - he was too chunky)
HEAD_KX, HEAD_KZ = 0.86, 0.9
TEX = {'r': 'bm:block/cec_robe', 'd': 'bm:block/cec_robe_dark', 'k': 'bm:block/cec_black', 'g': 'bm:block/cec_gold', 'w': 'bm:block/cec_wood',
       'p': 'bm:block/cec_crystal', 'f': 'bm:block/cec2_face', 'y': 'bm:block/cec_eye'}


def face_texture():
    """32 x 32: the dark face in the hood, a wide grin of jagged teeth (the eyes are their own glowing part)"""
    N = 32
    im = Image.new('RGBA', (N, N), (29, 28, 33, 255)); d = ImageDraw.Draw(im)
    for r in range(10):
        d.ellipse((4 + r * 0.6, 3 + r * 0.5, 28 - r * 0.6, 22 - r * 0.5), fill=(31 + r, 30 + r, 36 + r, 255))
    d.polygon([(3, 19), (8, 22), (16, 23), (24, 22), (29, 19), (27, 25), (21, 28), (16, 28.5), (11, 28), (5, 25)], fill=(6, 6, 8, 255))
    T = (170, 170, 182, 255)
    for x in range(5, 28, 3):
        yt = 20.5 + 1.5 * (1 - abs(x - 16) / 12)
        d.polygon([(x, yt), (x + 3, yt), (x + 1.5, yt + 2.6)], fill=T)
        yb = 26.8 - 1.2 * (1 - abs(x - 16) / 12)
        d.polygon([(x + 1.5, yb), (x + 4.5, yb), (x + 3, yb - 2.6)], fill=T)
    d.line([(3, 19), (2, 17)], fill=T, width=1); d.line([(29, 19), (30, 17)], fill=T, width=1)
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
            c((7.85, 1.4, 2.9), (8.15, 6, 3.0), 'd'), c((7.85, 6, 3.5), (8.15, 10.5, 3.6), 'd'), c((7.85, 10.5, 3.3), (8.15, 13, 3.4), 'd'),
            c((7.4, 12.6, 3.1), (8.6, 13.8, 3.25), 'g'),                                                 # the clasp
            c((0.6, 0, 6), (1.4, 1.2, 9), 'd'), c((14.6, 0, 4.5), (15.4, 1.0, 7.5), 'd'), c((4, 0, 2.0), (6.5, 0.9, 2.6), 'd'),
            c((10, 0, 2.0), (12, 1.1, 2.6), 'd'), c((9.5, 0, 14.4), (12.5, 1.2, 15), 'd'), c((3, 0, 14.4), (5, 0.8, 14.9), 'd'),
            c((0.7, 7.4, 4.2), (4.0, 13.6, 8.2), 'r', ('x', 22.5, (2.35, 13.4, 6.2))),                 # his left sleeve ...
            c((0.9, 5.0, 2.2), (3.9, 7.6, 5.2), 'k'),                                                    # ... and claw
            c((1.0, 3.4, 2.4), (1.6, 5.2, 3.0), 'k'), c((2.1, 3.0, 2.4), (2.7, 5.2, 3.0), 'k'), c((3.2, 3.4, 2.4), (3.8, 5.2, 3.0), 'k')]
    # ---- HEAD: a big hood (12 wide, 12 tall), a deep face opening under an overhanging brim, the tip curling back
    face = c((3.4, 8.2, 2.9), (12.6, 17.2, 3.0), 'f', faces=('north',)); face['faces']['north']['uv'] = [0, 0, 16, 16]
    head = [c((2, 7, 3.0), (14, 19, 14), 'r'),
            c((1.6, 7, 1.4), (3.4, 19.2, 3.2), 'r'), c((12.6, 7, 1.4), (14.4, 19.2, 3.2), 'r'), c((1.6, 17.2, 1.4), (14.4, 19.6, 3.2), 'r'),
            c((2.0, 7, 1.8), (14.0, 7.6, 3.1), 'd'),
            c((2.4, 18.4, 0.6), (13.6, 19.6, 2.4), 'r', ('x', -22.5, (8, 19, 2.4))),                    # the brim
            c((0.8, 5.4, 4), (2.4, 9.6, 12.6), 'r'), c((13.6, 5.4, 4), (15.2, 9.6, 12.6), 'r'),          # draped onto the shoulders
            c((2.8, 6.6, 13.8), (13.2, 17.6, 14.8), 'r'), c((3.4, 19, 4.2), (12.6, 19.8, 12.8), 'r'),
            face,
            c((6, 19, 8.5), (10, 21.4, 13.5), 'r'), c((6.8, 20.8, 10.5), (9.2, 23.6, 14.4), 'r', ('x', 22.5, (8, 21.4, 12))),
            c((7.2, 22.4, 12.8), (8.8, 24.0, 16.4), 'd', ('x', 45, (8, 22.8, 13.4))),
            c((7.8, 19, 3.6), (8.2, 19.7, 11.4), 'k')]                                                   # the stitched seam
    eyes = [c((4.0, 13.4, 2.75), (7.4, 14.9, 2.88), 'y', ('z', -22.5, (5.7, 14.15, 2.8))),
            c((8.6, 13.4, 2.75), (12.0, 14.9, 2.88), 'y', ('z', 22.5, (10.3, 14.15, 2.8)))]
    # ---- ARM: his right sleeve and claw on the crescent staff, which stands on the ground
    arm = [c((6, 2.4, 6), (10, 9, 10), 'r', ('x', 22.5, (8, 8.6, 8))), c((6.2, 1.4, 3.2), (9.8, 4.0, 6.2), 'k'),
           c((7.3, -5.4, 3.45), (8.7, 17, 4.85), 'w'), c((6.7, 15, 3.0), (9.3, 18, 5.3), 'g'),
           c((4.9, 13.6, 3.5), (6.7, 19.4, 4.7), 'g'), c((1.9, 18.4, 3.5), (5.5, 19.8, 4.7), 'g', ('z', -22.5, (5.3, 19.1, 4.1))),
           c((1.9, 13.2, 3.5), (5.5, 14.6, 4.7), 'g', ('z', 22.5, (5.3, 13.9, 4.1))),
           c((9.3, 13.6, 3.5), (11.1, 19.4, 4.7), 'g'), c((10.5, 18.4, 3.5), (14.1, 19.8, 4.7), 'g', ('z', 22.5, (10.7, 19.1, 4.1))),
           c((10.5, 13.2, 3.5), (14.1, 14.6, 4.7), 'g', ('z', -22.5, (10.7, 13.9, 4.1))),
           c((6.5, 18, 2.8), (9.5, 24, 5.6), 'p', ('y', 45, (8, 21, 4.2))), c((7.2, 24, 3.5), (8.8, 26.4, 4.9), 'p', ('y', 45, (8, 25, 4.2)))]
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
    return {'cec2_body': (TEX, body), 'cec2_head': (TEX, head), 'cec2_eyes': (TEX, eyes), 'cec2_arm': (TEX, arm)}

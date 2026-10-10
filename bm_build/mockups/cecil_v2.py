"""MOCKUP (not in the build): Cecil, shorter and chibi with a big hood. Writes models into $BM_SCRATCH/rp2 (needs cecv2_face.png and the cec_* textures there) and renders old vs new."""
import sys, json, os, math
sys.path.insert(0, '/home/user/main/bm_build')
from gen_rp import cube
from tools.render import Scene
from PIL import Image, ImageDraw
SP = os.environ.get('BM_SCRATCH', '/tmp/bm_mockup')
RP2 = f'{SP}/rp2'; RP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'out_p2', 'BlackMarket_RP')
ct = {'r': 'bm:block/cec_robe', 'd': 'bm:block/cec_robe_dark', 'k': 'bm:block/cec_black', 'g': 'bm:block/cec_gold', 'w': 'bm:block/cec_wood',
      'p': 'bm:block/cec_crystal', 'f': 'bm:block/cecv2_face', 'y': 'bm:block/cec_eye'}
def c(fr, to, t, rot=None, faces=None):
    e = cube(fr, to, t, **({'faces': faces} if faces else {}))
    if rot: e['rotation'] = {'axis': rot[0], 'angle': rot[1], 'origin': list(rot[2])}
    return e
def save(name, els):
    t = dict(ct); t['particle'] = ct['r']
    json.dump({'textures': t, 'elements': els, 'display': {'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]}}},
              open(f'{RP2}/assets/bm/models/item/{name}.json', 'w'))
# ---- BODY: a short bell of a robe (11 tall), hunched, tattered hem; the left claw out front (faces -z; his right is +x)
body = [c((1, 0, 2), (15, 1.4, 14), 'd'), c((1.5, 1.4, 2.5), (14.5, 5.5, 13.5), 'r'), c((2.4, 5.5, 3.2), (13.6, 8.6, 12.6), 'r'),
        c((3.2, 8.6, 3.0), (12.8, 11, 11.6), 'r'),                                   # shoulders, pushed forward (the hunch)
        c((4.5, 10.6, 2.6), (11.5, 11.4, 9.5), 'd'),                                 # collar shadow
        c((7.85, 1.4, 2.4), (8.15, 5.5, 2.5), 'd'), c((7.85, 5.5, 3.1), (8.15, 8.6, 3.2), 'd'), c((7.4, 9.0, 2.9), (8.6, 10.2, 3.0), 'g'),
        # ragged hem flaps
        c((0.6, 0, 5), (1.4, 1.2, 8), 'd'), c((14.6, 0, 4), (15.4, 1.0, 7), 'd'), c((4, 0, 1.6), (6.5, 0.9, 2.1), 'd'), c((10, 0, 1.6), (12, 1.1, 2.1), 'd'),
        c((9.5, 0, 13.9), (12.5, 1.2, 14.6), 'd'), c((3, 0, 13.9), (5, 0.8, 14.4), 'd'),
        # his left sleeve and claw, hanging out front
        c((0.6, 5.5, 3.6), (3.8, 10.6, 7.4), 'r', ('x', 22.5, (2.2, 10.4, 5.5))),
        c((0.8, 3.6, 2.0), (3.6, 5.8, 4.8), 'k'), c((0.9, 2.2, 2.2), (1.5, 3.8, 2.8), 'k'), c((1.9, 1.8, 2.2), (2.5, 3.8, 2.8), 'k'), c((2.9, 2.2, 2.2), (3.5, 3.8, 2.8), 'k')]
# ---- HEAD: a big hood (14 wide, 12 tall), a deep face opening, the curled tip; pivot at (8,8,8) = the neck is y 7
face = c((3.0, 8.2, 2.3), (13.0, 17.2, 2.4), 'f', faces=('north',)); face['faces']['north']['uv'] = [0, 0, 16, 16]
head = [c((1.2, 7, 2.6), (14.8, 19, 14.6), 'r'),
        c((1.0, 7, 1.0), (3.0, 19.2, 2.8), 'r'), c((13.0, 7, 1.0), (15.0, 19.2, 2.8), 'r'), c((1.0, 17.2, 1.0), (15.0, 19.4, 2.8), 'r'),   # the rim
        c((1.6, 7, 1.4), (14.4, 7.6, 2.6), 'd'),                                         # its shadowed lip
        c((2.0, 18.4, 0.4), (14.0, 19.6, 2.2), 'r', ('x', -22.5, (8, 19, 2.2))),           # the brim overhangs the face
        c((0.4, 5.6, 4), (2.2, 10, 13), 'r'), c((13.8, 5.6, 4), (15.6, 10, 13), 'r'),      # it drapes onto the shoulders
        c((2.4, 6.4, 14.4), (13.6, 17.6, 15.4), 'r'), c((3.4, 19, 4), (12.6, 19.8, 13), 'r'),
        face,
        c((5.8, 19, 8), (10.2, 21.4, 14), 'r'), c((6.6, 20.6, 10.5), (9.4, 23.8, 14.6), 'r', ('x', 22.5, (8, 21.2, 12))),
        c((7.0, 22.6, 13), (9.0, 24.4, 17), 'd', ('x', 45, (8, 23, 13.5))),           # the tip curls back
        c((7.8, 19, 3.2), (8.2, 19.7, 11), 'k'),                                           # the stitched seam
        c((3.6, 13.4, 2.15), (7.4, 14.9, 2.3), 'y', ('z', -22.5, (5.5, 14.1, 2.2))),        # big, slanted, glowing eyes
        c((8.6, 13.4, 2.15), (12.4, 14.9, 2.3), 'y', ('z', 22.5, (10.5, 14.1, 2.2)))]
# ---- ARM: his right sleeve and claw on a shorter crescent staff
arm = [c((6, 2.6, 6), (10, 8.6, 10), 'r', ('x', 22.5, (8, 8, 8))), c((6.2, 1.6, 3.2), (9.8, 4.2, 6.2), 'k'),
       c((7.3, -1.6, 3.45), (8.7, 18, 4.85), 'w'), c((6.7, 16, 3.0), (9.3, 19, 5.3), 'g'),
       c((4.9, 14.6, 3.5), (6.7, 20.4, 4.7), 'g'), c((1.9, 19.4, 3.5), (5.5, 20.8, 4.7), 'g', ('z', -22.5, (5.3, 20.1, 4.1))),
       c((1.9, 14.2, 3.5), (5.5, 15.6, 4.7), 'g', ('z', 22.5, (5.3, 14.9, 4.1))),
       c((9.3, 14.6, 3.5), (11.1, 20.4, 4.7), 'g'), c((10.5, 19.4, 3.5), (14.1, 20.8, 4.7), 'g', ('z', 22.5, (10.7, 20.1, 4.1))),
       c((10.5, 14.2, 3.5), (14.1, 15.6, 4.7), 'g', ('z', -22.5, (10.7, 14.9, 4.1))),
       c((6.5, 19, 2.8), (9.5, 25, 5.6), 'p', ('y', 45, (8, 22, 4.2))), c((7.2, 25, 3.5), (8.8, 27.4, 4.9), 'p', ('y', 45, (8, 26, 4.2)))]
save('cecv2_body', body); save('cecv2_head', head); save('cecv2_arm', arm)
q = lambda a: (math.sin(math.radians(a) / 2), 0, 0, math.cos(math.radians(a) / 2))
def scene(new):
    s = Scene(rp=RP2 if new else RP)
    if new:
        s.display('bm:item/cecv2_body', translation=(0, 0.5, 0))
        s.display('bm:item/cecv2_head', pos=(0, 0.75, 0.06))
        s.display('bm:item/cecv2_arm', pos=(-0.38, 0.62, 0.02), left=q(6))
    else:
        s.display('bm:item/cec_body', translation=(0, 0.5, 0))
        s.display('bm:item/cec_head', pos=(0, 1.38, 0.12)); s.display('bm:item/cec_eyes', pos=(0, 1.38, 0.12))
        s.display('bm:item/cec_arm', pos=(-0.31, 1.28, 0.06), left=q(6))
    s.player_box((1.1, 0, 0))
    return s
rows = []
for new in (False, True):
    s = scene(new)
    ims = [s.render(v, size=360, span=3.0, center=(0.4, 1.1, 0)) for v in ('front', 'side', 'iso')]
    row = Image.new('RGB', (360 * 3, 360), 'white')
    for i, im in enumerate(ims): row.paste(im, (i * 360, 0))
    ImageDraw.Draw(row).text((8, 8), 'NEW (proposed)' if new else 'CURRENT', fill=(0, 0, 0))
    rows.append(row)
out = Image.new('RGB', (1080, 720), 'white'); out.paste(rows[0], (0, 0)); out.paste(rows[1], (0, 360))
out.save(f'{SP}/prev/cecil2.png')
s = scene(True)
ims = [s.render(v, size=420, span=1.9, center=(0, 0.85, 0)) for v in ('front', 'iso', 'side')]
z = Image.new('RGB', (1260, 420), 'white')
for i, im in enumerate(ims): z.paste(im, (i * 420, 0))
z.save(f'{SP}/prev/cecil2_zoom.png')

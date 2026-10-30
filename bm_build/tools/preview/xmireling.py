"""The Brood Mireling - the Mireling's alien costume (xmireling_art.py) - preview sheets (stage-1 draft).
    python3 tools/preview/xmireling.py [lineup,poses,faces]
lineup   the Mireling, the Brood Mireling and its shiny beside a player; and FULL-GROWN: the grown Dread Mire and the grown Brood-Mire
poses    every pose of the DRAFT list in the costume, the plain Mireling's beside a few
faces    the six faces (the eye's expressions) in the costume, close
PNGs to $XM_OUT."""
import sys, os, json, types
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM)
from PIL import Image, ImageDraw, ImageFont
FN = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
import draftkit as K
import playerkit as PK
import rigkit
import mireling_art as ML
import xmireling_art as X
import xmire_art as XA
import mire_art as MA

OUT = os.environ.get('XM_OUT', '/tmp/bm_previews/xmire'); os.makedirs(OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['lineup', 'poses', 'faces']
mod = lambda tx, md: types.SimpleNamespace(textures=tx, models=md)
ROOT = K.pack(mod(lambda: dict(X.textures(), **X.textures(shiny=True)), lambda: dict(X.models(), **X.models(shiny=True))), os.path.join(K.OUT, 'rp_xmireling'))
MLROOT = K.pack(ML, os.path.join(K.OUT, 'rp_mireling_cmp'))
XROOT = K.pack(XA, os.path.join(K.OUT, 'rp_xmire'))
MROOT = K.pack(MA, os.path.join(K.OUT, 'rp_mire_cmp'))
GRASS = ('#5a7a3a', '#64843f')
GROWN = 1.5                                               # (phase252.GROWN_SC)


def floor(s, r=3, x0=0.0, x1=None):
    for i in range(int(x0) - r, int(x1 if x1 is not None else x0) + r):
        for j in range(-r, r):
            s.solid((i, -0.25, j), (i + 1, 0.0, j + 1), GRASS[(i + j) % 2])


def scene():
    return K.multi_scene(ROOT, MLROOT, XROOT, MROOT)


def ling(s, pose, at=(0, 0, 0), rig=X.Costume, yaw=0.0):
    rigkit.render(s, rig, ML.POSES[pose] if isinstance(pose, str) else pose, at=at, scale=ML.RIG_SCALE, yaw=yaw)


if 'lineup' in what:
    s = scene()
    ling(s, 'idle_a', (-6.0, 0, 0), ML); ling(s, 'idle_a', (-4.2, 0, 0)); ling(s, 'idle_a', (-2.4, 0, 0), X.ShinyCostume)
    PK.put(s, PK.player('stand'), at=(-0.6, 0, 0.6))
    rigkit.render(s, MA, MA.POSES['idle_a'], at=(3.6, 0, 0), scale=GROWN)
    rigkit.render(s, XA, XA.POSES['idle_a'], at=(10.2, 0, 0), scale=GROWN)
    floor(s, 4, -7, 13)
    N, span = 2400, 21.0; k = N / span
    im = s.render((-12, 8), size=N, span=span, center=(2.6, 2.4, 0))
    im = im.crop((0, int(N / 2 - 4.4 * k), N, int(N / 2 + 3.4 * k)))
    d = ImageDraw.Draw(im)
    for x, t in ((-6.0, 'the Mireling'), (-4.2, 'Brood Mireling'), (-2.4, 'its shiny'), (-0.6, 'a player'), (3.6, 'Grown (Dread)'), (10.2, 'Grown (Brood)')):
        d.text((int(N / 2 + (x - 2.6 - 0.7) * k * 0.98), 54), t, fill=(20, 20, 20), font=FN)
    d.text((10, 8), 'THE BROOD MIRELING (the costume, a wardrobe look) beside the Mireling and its shiny, a player; FULL-GROWN (Honours III, its menu\'s Grown): '
                    'the plain Mireling grows into the Dread Mire, the Brood Mireling into the Brood-Mire (both at 1.5)', fill=(10, 10, 10), font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18))
    p = os.path.join(OUT, 'xmireling_lineup.png'); im.save(p); print(p)

if 'poses' in what:
    tiles = []
    for n in ML.DRAFT:
        s = scene(); ling(s, n, (0.45, 0, 0)); ling(s, n, (-1.15, 0, 0), ML); floor(s, 3)
        tiles.append(K.label(s.render((-30, 14), size=340, span=3.6, center=(-0.3, 0.9, 0)), n, 'plain (left) and Brood (right)'))
    p = os.path.join(OUT, 'xmireling_poses.png'); K.sheet(tiles, p, cols=5, title='The Brood Mireling - every pose, beside the plain Mireling'); print(p)

if 'faces' in what:
    tiles = []
    for shiny in (False, True):
        for f in ML.FACES:
            pz = dict(ML.POSES['idle_a'], _face=f)
            s = scene(); ling(s, pz, rig=X.ShinyCostume if shiny else X.Costume); floor(s, 2)
            c = rigkit.point(ML, pz, 'head', (0.0, ML.CY, ML.HZ - 4.0), scale=ML.RIG_SCALE)
            tiles.append(K.label(s.render('front', size=320, span=1.6, center=(c[0], c[1] + 0.12, c[2])), f, 'shiny' if shiny else 'Brood'))
    p = os.path.join(OUT, 'xmireling_faces.png'); K.sheet(tiles, p, cols=6, title='The Brood Mireling - its faces (every expression of the Mireling\'s eye), and the shiny'); print(p)

"""v299: the Seraph's Raiment redrawn (seraph_art.py, seraph_wings.py) - previews.   python3 tools/preview/seraph.py [what,...]
  worn     the whole set on a player: front, back, three-quarter (standing, the 3D wings at rest), and the bare layers
  helm     the Seraph's Gaze: front, three-quarter, side, behind, above
  wings    the 3D wings on a wearer: at rest (both sway keys), sneaking, gliding (both beat keys, from behind and above),
           falling, riding - with the elytra mesh drawn too, to see that the 3D wings cover it
  before   the old look beside the new (the worn set, the helm)
  icons    the three sprites, big, beside the old ones
PNGs to $SERAPH_OUT (default /home/user/main/previews/v299_seraph). The old look's files are read from $SERAPH_OLD (a copy of
the 2.93 textures and helm model)."""
import sys, os, json, math, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM)
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from tools.render import Scene
import playerkit as PK
import dread_armor as DA
import seraph_art as A
import rigkit

OUT = os.environ.get('SERAPH_OUT', '/home/user/main/previews/v299_seraph'); os.makedirs(OUT, exist_ok=True)
TMP = os.environ.get('BM_PREVIEW_DIR', '/tmp/bm_previews'); os.makedirs(TMP, exist_ok=True)
OLD = os.environ.get('SERAPH_OLD', '')
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['worn', 'helm', 'wings', 'before', 'icons']
SKY = np.array([0.78, 0.86, 0.95]) * 255
GRID = [np.array([0.55, 0.62, 0.55]) * 255, np.array([0.2, 0.5, 0.2]) * 255]


def pack(root, new=True):
    """a scratch resource pack: the textures, the helm, the layers (and the 3D wings' models)"""
    if os.path.exists(root): shutil.rmtree(root)
    def p(*a):
        f = os.path.join(root, 'assets', 'bm', *a); os.makedirs(os.path.dirname(f), exist_ok=True); return f
    E = ('textures', 'entity', 'equipment')
    if new:
        for k, im in A.textures().items(): im.save(p('textures', 'block', k + '.png'))
        json.dump(A.helm_json(DA.helm_json()[1]['display']), open(p('models', 'item', 'seraph_helm.json'), 'w'))
        A.humanoid().save(p(*E, 'humanoid', 'seraph.png')); A.leggings().save(p(*E, 'humanoid_leggings', 'seraph.png'))
        A.wings_layer().save(p(*E, 'wings', 'seraph_wings.png'))
        try:
            import seraph_wings as W
            for k, im in W.textures().items(): im.save(p('textures', 'block', k + '.png'))
            for name, (tex, els) in W.models().items():
                t = dict(tex); t['particle'] = next(iter(tex.values()))
                json.dump({'textures': t, 'elements': els, 'display': {'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]}}},
                          open(p('models', 'item', name + '.json'), 'w'))
        except ImportError:
            pass
    else:
        for f in os.listdir(os.path.join(OLD, 'block')): shutil.copy(os.path.join(OLD, 'block', f), p('textures', 'block', f))
        shutil.copy(os.path.join(OLD, 'seraph_helm.json'), p('models', 'item', 'seraph_helm.json'))
        shutil.copy(os.path.join(OLD, 'seraph.png'), p(*E, 'humanoid', 'seraph.png'))
        shutil.copy(os.path.join(OLD, 'seraph_leg.png'), p(*E, 'humanoid_leggings', 'seraph.png'))
        shutil.copy(os.path.join(OLD, 'seraph_wings.png'), p(*E, 'wings', 'seraph_wings.png'))
    return root


NEW = pack(os.path.join(TMP, 'rp_seraph_new'))
LAYERS = [('bm:entity/equipment/humanoid/seraph', 'outer', ('body', 'armr', 'arml', 'legr', 'legl')),
          ('bm:entity/equipment/humanoid_leggings/seraph', 'inner', ('body', 'legr', 'legl'))]


def dark(im, top=(34, 30, 52), bot=(12, 10, 20)):
    a = np.asarray(im).astype(np.float32); h, w = a.shape[:2]
    m = np.zeros((h, w), bool)
    for c in [SKY] + GRID: m |= np.all(np.abs(a - c.astype(np.uint8).astype(np.float32)) < 1.5, axis=2)
    t = np.linspace(0, 1, h)[:, None, None]
    g = np.array(top, np.float32) * (1 - t) + np.array(bot, np.float32) * t
    return Image.fromarray(np.where(m[..., None], np.broadcast_to(g, a.shape), a).astype(np.uint8))


def label(im, text, sub=None):
    d = ImageDraw.Draw(im)
    try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15); g = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
    except OSError: f = g = None
    d.text((10, 8), text, fill=(250, 236, 200), font=f)
    if sub: d.text((10, 27), sub, fill=(190, 180, 210), font=g)
    return im


def sheet(tiles, out, cols=4, title=None):
    W, H = tiles[0].size; rows = (len(tiles) + cols - 1) // cols; top = 44 if title else 0
    sh = Image.new('RGB', (W * cols, H * rows + top), (14, 12, 22))
    if title:
        d = ImageDraw.Draw(sh)
        try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
        except OSError: f = None
        d.text((12, 10), title, fill=(250, 236, 200), font=f)
    for i, t in enumerate(tiles): sh.paste(t, ((i % cols) * W, top + (i // cols) * H))
    sh.save(out); print(out); return out


def floor(s, r=2.0, step=0.5):
    n = int(r / step)
    for i in range(-n, n):
        for j in range(-n, n):
            s.solid((i * step, -0.06, j * step), ((i + 1) * step, 0.0, (j + 1) * step), '#3a3450' if (i + j) % 2 else '#2c2840')


HEAD_Y = {'stand': 28.0, 'crouch': 24 - 4.2 + 4.0, 'glide': 28.0}
LIFT = {'stand': 0.0, 'crouch': -0.125, 'glide': 0.0}


def wearer(s, kind='stand', root=NEW, yaw=0.0, pitch=0.0, at=(0.0, 0.0, 0.0), helm=True, wings3d=None, elytra=True, layers=True, skin=True):
    """a player wearing the set: the layers, the elytra mesh, the helm on the head, the 3D wings (a seraph_wings pose name)"""
    lift = LIFT[kind]
    PK.put(s, PK.player(kind, LAYERS if layers else (), wings='bm:entity/equipment/wings/seraph_wings' if elytra else None, skin=skin),
           at=(at[0], at[1] + lift, at[2]), yaw=yaw, pitch=pitch)
    if helm:
        hy = HEAD_Y[kind] * PK.S / 16
        E = PK._ry(math.radians(-yaw)) @ PK._rx(math.radians(pitch))
        c = E @ np.array((0, hy, 0)) + np.array(at) + np.array((0, lift, 0))
        s.display('bm:item/seraph_helm', pos=tuple(c), yaw=yaw, pitch=pitch, scale=0.625 * PK.S, ctx='head')
    if wings3d:
        import seraph_wings as W
        W.render(s, wings3d, at=(at[0], at[1], at[2]), yaw=yaw, pitch=0.0 if kind == 'glide' else pitch)   # (gliding: the body's pitch is the pose's; the look is level)


def scene(root=NEW):
    from tools.render import VANILLA
    s = Scene(root)
    roots = [os.path.join(root, 'assets'), os.path.join(BM, 'out_p2', 'BlackMarket_RP', 'assets'), VANILLA]
    def _path(ns_id, kind, ext):
        ns, pth = ns_id.split(':') if ':' in ns_id else ('minecraft', ns_id)
        for r in roots:
            f = os.path.join(r, ns, kind, pth + ext)
            if os.path.exists(f): return f
        raise FileNotFoundError(ns_id)
    s._path = _path
    return s


def tile(view, text, sub=None, size=360, span=2.9, cy=1.05, **kw):
    s = scene(kw.pop('root', NEW)); floor(s)
    wearer(s, **kw)
    return label(dark(s.render(view, size=size, span=span, center=(0, cy, 0))), text, sub)


def flat(im, text, sub=None, k=8, bg=(40, 36, 58)):
    im = im.resize((im.width * k, im.height * k), Image.NEAREST)
    out = Image.new('RGBA', (im.width + 20, im.height + 50), bg + (255,)); out.alpha_composite(im, (10, 44))
    return label(out.convert('RGB'), text, sub)


try:
    import seraph_wings as W
    REST = 'rest_a'
except ImportError:
    W = None; REST = None

if 'worn' in what:
    T = [tile('front', 'front', 'the Raiment, the Gaze, the wings at rest', wings3d=REST),
         tile('back', 'behind', 'the wing-mounts, the folded great wings', wings3d=REST),
         tile((35, 12), 'three-quarter', None, wings3d=REST),
         tile((150, 14), 'from behind, three-quarter', None, wings3d=REST),
         tile('front', 'the plate alone', 'front (no 3D wings, no elytra)', elytra=False, helm=False),
         tile('back', 'the plate alone', 'behind', elytra=False, helm=False),
         tile((90, 4), 'the plate alone', 'its right side', elytra=False, helm=False),
         tile((-55, 25), 'the plate alone', 'from above', elytra=False, helm=False)]
    sheet(T, f'{OUT}/seraph_worn.png', cols=4, title="The Seraph's Raiment - worn")
    L = [flat(A.humanoid(), 'humanoid (bm:seraph)', 'the cuirass, pauldrons, vambraces; the Treads'),
         flat(A.leggings(), 'humanoid_leggings (bm:seraph)', 'belt, tassets, cuisses, knee eyes'),
         flat(A.wings_layer(), 'wings (bm:seraph_wings)', 'the elytra mesh while gliding')]
    W0 = max(t.width for t in L); Hh = max(t.height for t in L)
    sh = Image.new('RGB', (W0 * 3, Hh), (14, 12, 22))
    for i, t in enumerate(L): sh.paste(t, (i * W0, 0))
    sh.save(f'{OUT}/seraph_layers.png'); print(f'{OUT}/seraph_layers.png')

if 'helm' in what:
    T = []
    for view, sub in (((180, 6), 'front'), ((145, 16), 'three-quarter'), ((90, 4), 'side'), ('front', 'behind'), ((200, 55), 'above')):
        s = scene(); s.display('bm:item/seraph_helm', pos=(0, 0, 0), ctx='fixed')
        T.append(label(dark(s.render(view, size=330, span=1.25, center=(0, 0.12, 0))), "Seraph's Gaze", sub))
    s = scene(); floor(s); wearer(s, helm=True, elytra=False)
    T.append(label(dark(s.render((20, 8), size=330, span=0.9, center=(0, 1.62, 0))), 'worn', 'on the head'))
    sheet(T, f'{OUT}/seraph_helm.png', cols=3, title="The Seraph's Gaze - with two they covered their faces")

if 'wings' in what and W:
    T = [tile('back', 'at rest (sway a)', 'great wings folded down the back, lower wings round the legs', wings3d='rest_a'),
         tile('back', 'at rest (sway b)', 'the idle sway, 40 ticks each way', wings3d='rest_b'),
         tile((60, 10), 'at rest, side', None, wings3d='rest_a'),
         tile('front', 'at rest, front', None, wings3d='rest_a'),
         tile('back', 'sneaking', 'leaning, folded close', kind='crouch', wings3d='sneak'),
         tile((70, 8), 'sneaking, side', None, kind='crouch', wings3d='sneak'),
         tile('back', 'riding', 'folded close, the lower wings clear', wings3d='ride'),
         tile((150, 10), 'falling (beat a)', 'spread wide and up', wings3d='fall_a', span=4.2, cy=1.3),
         tile((150, 10), 'falling (beat b)', None, wings3d='fall_b', span=4.2, cy=1.3),
         tile((180, 55), 'gliding (beat a)', 'from behind and above', kind='glide', pitch=90, wings3d='glide_a', span=4.4, cy=0.3),
         tile((180, 55), 'gliding (beat b)', None, kind='glide', pitch=90, wings3d='glide_b', span=4.4, cy=0.3),
         tile((215, 30), 'gliding, three-quarter', 'from the front, above', kind='glide', pitch=90, wings3d='glide_a', span=4.4, cy=0.3)]
    sheet(T, f'{OUT}/seraph_wings3d.png', cols=4, title="The Seraph's Wings - six wings: two cover the face, two the feet, two fly")

if 'before' in what and OLD:
    OLDR = pack(os.path.join(TMP, 'rp_seraph_old'), new=False)
    T = []
    for view, sub in (('front', 'front'), ('back', 'behind'), ((35, 12), 'three-quarter')):
        T.append(tile(view, 'BEFORE (2.93)', sub, root=OLDR))
        T.append(tile(view, 'AFTER (2.99)', sub, wings3d=REST))
    for root, txt in ((OLDR, 'BEFORE'), (NEW, 'AFTER')):
        s = scene(root); s.display('bm:item/seraph_helm', pos=(0, 0, 0), ctx='fixed')
        T.append(label(dark(s.render((150, 12), size=360, span=1.25, center=(0, 0.12, 0))), txt, "the Seraph's Gaze"))
    s = scene(NEW); floor(s); wearer(s, kind='glide', pitch=90, root=NEW, wings3d='glide_a' if W else None)
    T.append(label(dark(s.render((150, 40), size=360, span=4.4, center=(0, 0.3, 0))), 'AFTER', 'gliding'))
    s = scene(OLDR); floor(s); wearer(s, kind='glide', pitch=90, root=OLDR)
    T.insert(len(T) - 1, label(dark(s.render((150, 40), size=360, span=4.4, center=(0, 0.3, 0))), 'BEFORE', 'gliding'))
    sheet(T, f'{OUT}/seraph_before_after.png', cols=2, title="The Seraph's Raiment - before and after")

if 'icons' in what:
    new = A.icons(); T = []
    for k in ('seraph_carapace', 'seraph_greaves', 'seraph_treads'):
        if OLD and os.path.exists(f'{OLD}/{k}.png'): T.append(flat(Image.open(f'{OLD}/{k}.png').convert('RGBA'), 'before', k, k=10))
        T.append(flat(new[k], 'after', k, k=10))
    sheet(T, f'{OUT}/seraph_icons.png', cols=2 if OLD else 3, title="The Seraph's Raiment - sprites")

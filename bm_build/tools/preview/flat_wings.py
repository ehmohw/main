"""v3.0c: worn wings flat by default (flat_wings.py) - each set's new elytra layer on a player, beside its 2.99 mantle (now only under
the 3D wings), and its display piece (the framed 3D model).      python3 tools/preview/flat_wings.py
Everything is read from the built pack (out_p2; run gen_rp --phase2 first). One sheet: $FLAT_OUT/flat_wings_30c.png (default
/home/user/main/previews/v30c_wings)."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM)
import numpy as np
from PIL import Image, ImageDraw
from tools.render import Scene
import playerkit as PK

OUT = os.environ.get('FLAT_OUT', '/home/user/main/previews/v30c_wings'); os.makedirs(OUT, exist_ok=True)
RP = os.path.join(BM, 'out_p2', 'BlackMarket_RP')
W = 'bm:entity/equipment/wings/'
H = 'bm:entity/equipment/humanoid/'
SETS = [  # (name, wings texture, humanoid layer or None, framed model or None)
    ("The Seraph's Wings", 'seraph_wings', 'seraph', 'angel_dread_carapace_3d'),
    ('The Dread Carapace', 'dread_wings', 'dread', 'dread_carapace_3d'),
    ('Wings of the Last Night', 'sov_wings', None, 'sov_wings_3d'),
    ('Wings of the First Light', 'sov_wings_holy', None, 'sov_wings_holy_3d'),
    ('(for comparison) Wings of the Damned', 'damned_wings', None, None)]


def floor(s, r=2.0, step=0.5):
    n = int(r / step)
    for i in range(-n, n):
        for j in range(-n, n):
            s.solid((i * step, -0.06, j * step), ((i + 1) * step, 0.0, (j + 1) * step), '#3a3450' if (i + j) % 2 else '#2c2840')


def dark(im):
    a = np.asarray(im.convert('RGBA')).astype(float); h = a.shape[0]
    bg = np.linspace(np.array((34, 30, 52)), np.array((12, 10, 20)), h)[:, None, :]
    m = a[..., 3:4] / 255.0
    return Image.fromarray((a[..., :3] * m + bg * (1 - m)).astype(np.uint8))


def label(im, text, sub=None):
    d = ImageDraw.Draw(im); d.text((8, 6), text, fill=(240, 236, 255));
    if sub: d.text((8, 20), sub, fill=(170, 164, 200))
    return im


def tile(tex, hum, view, kind='stand', pitch=0.0, text='', sub=None, span=2.9, cy=1.12, size=300):
    s = Scene(RP); floor(s)
    layers = [(H + hum, 'outer', ('body', 'armr', 'arml', 'legr', 'legl'))] if hum else ()
    PK.put(s, PK.player(kind, layers, wings=W + tex), at=(0, -0.125 if kind == 'crouch' else 0.0, 0), pitch=pitch)
    return label(dark(s.render(view, size=size, span=span, center=(0, cy, 0))), text, sub)


def framed(model, text, size=300):
    s = Scene(RP)
    s.display(f'bm:item/{model}', pos=(0, 0, 0), ctx='fixed')
    return label(dark(s.render('front', size=size, span=1.3, center=(0, 0, 0))), text, 'in a frame / display case')


rows = []
for name, tex, hum, model in SETS:
    row = [tile(tex, hum, 'back', text=name, sub='worn, flat (default)'),
           tile(tex, hum, (150, 15), text=name, sub='three-quarter'),
           tile(tex, hum, 'back', kind='crouch', text=name, sub='sneaking'),
           tile(tex, hum, (180, 55), kind='glide', pitch=90, text=name, sub='gliding', span=3.6, cy=0.3),
           tile(tex + ('_mantle' if model else ''), hum, 'back', text=name, sub='2.99 mantle (3D wings on)' if model else '-')]
    row.append(framed(model, name) if model else Image.new('RGB', row[0].size, (20, 18, 30)))
    rows.append(row)
w, h = rows[0][0].size
sheet = Image.new('RGB', (w * len(rows[0]), h * len(rows) + 30), (16, 14, 24))
ImageDraw.Draw(sheet).text((10, 8), 'v3.0c - worn wings flat by default (the elytra layer: never lags); 3D only on the toggle', fill=(255, 255, 255))
for r, row in enumerate(rows):
    for c, im in enumerate(row): sheet.paste(im, (c * w, 30 + r * h))
p = os.path.join(OUT, 'flat_wings_30c.png'); sheet.save(p); print(p)

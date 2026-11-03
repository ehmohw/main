"""3.0g: the ten followers' Ethereal and Wraithfire forms (elemforms.py) - each one's display-case figure, plain / Ethereal / Wraithfire
side by side, and a contact sheet of all ten. The twins are made into a scratch pack from the built one (out_p2 is only read).
    python3 tools/preview/elemforms.py [outdir] [who,who...]"""
import sys, os, json, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [HERE, ROOT, os.path.join(ROOT, 'tools')]
import draftkit as K
import gen_dp  # noqa: F401
import phase134 as P134, phase136  # noqa: F401
import elemforms as EF
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(K.OUT, 'elemforms')
WHO = sys.argv[2].split(',') if len(sys.argv) > 2 else list(EF.FOL)
os.makedirs(OUT, exist_ok=True)
REAL = K.REAL_RP
SCR = os.path.join(OUT, 'rp_scratch')
shutil.rmtree(SCR, ignore_errors=True); os.makedirs(SCR)
FIG = P134.figures()
VAN = '/home/claude/mc263/client/assets'
Tw = EF.Twins(REAL, SCR, VAN if os.path.isdir(VAN) else None)
NAMES = {'bender': 'Bender', 'capshun': 'Mr. Capshun', 'sovereign': 'The Bound Sovereign', 'keeper': 'The Keeper of Bonds', 'lantern': 'The Arachno-Lantern',
         'leo': 'Leo', 'celi': 'Celi', 'demo': 'Democratus', 'eraser': 'The Eraser (joke)', 'don': 'Donado (joke)'}


def leaf(node):
    t = node.get('type')
    if t == 'minecraft:model': return node['model']
    if t == 'minecraft:select': return leaf(node.get('fallback') or node['cases'][0]['model'])
    if t == 'minecraft:condition': return leaf(node['on_false'])
    if t == 'minecraft:range_dispatch': return leaf(node['fallback'])
    if t == 'minecraft:composite': return leaf(node['models'][0])
    raise ValueError(t)


def model_of(item_id):
    n = item_id.split(':')[1]
    f = os.path.join(REAL, 'assets', 'bm', 'items', n + '.json')
    return leaf(json.load(open(f))['model'])[len('bm:item/'):] if os.path.exists(f) else n


def font(sz, bold=True):
    try: return ImageFont.truetype(f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if bold else ""}.ttf', sz)
    except OSError: return None


def tile(w, el, size=300, bg=(255, 255, 255)):
    F = EF.FOL[w]
    name, parts = FIG[F['item']]
    lo, h, x0, x1, z0, z1 = P134.FIT[F['item']]
    s = K.multi_scene(SCR, REAL)
    for model, tr, L, R, sc in parts:
        m = model_of(model)
        mid = f'bm:item/{m}' if el is None else Tw.model(w, m, el)
        s.display(mid, translation=tr, scale=sc, left=L, right=R, yaw=200)
    im = s.render((1.3 * h, h * 0.65, -2.6 * h), size=size, span=h * 1.3, center=(0, lo + h / 2, 0))
    if el is not None:                      # (a soft backdrop of the form's light, so the glow reads on the page)
        back = Image.new('RGB', im.size, (40, 52, 78) if el == EF.ETH else (14, 26, 34))
        im = im.convert('RGBA'); bgk = im.getpixel((2, 2))
        px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                if px[x, y][:3] == bgk[:3]: px[x, y] = (0, 0, 0, 0)
        back.paste(im, (0, 0), im); im = back
    return im.convert('RGB')


def row(w, size=300):
    tiles = [tile(w, None, size), tile(w, EF.ETH, size), tile(w, EF.WR, size)]
    W_, H_ = size * 3, size + 34
    out = Image.new('RGB', (W_, H_), 'white'); d = ImageDraw.Draw(out)
    for i, (t, lab) in enumerate(zip(tiles, ('plain', 'Ethereal', 'Wraithfire'))):
        out.paste(t, (i * size, 34))
        d.text((i * size + 8, 38), lab, fill=(30, 30, 30) if i < 1 else (220, 240, 255), font=font(14))
    d.text((8, 6), NAMES[w], fill=(20, 20, 20), font=font(20))
    return out


rows = []
for w in WHO:
    r = row(w)
    r.save(os.path.join(OUT, f'{w}.png')); rows.append(r); print(os.path.join(OUT, f'{w}.png'))
cols = 2
W_, H_ = rows[0].size
sheet = Image.new('RGB', (W_ * cols, H_ * ((len(rows) + cols - 1) // cols) + 44), 'white')
ImageDraw.Draw(sheet).text((12, 10), '3.0g - Ethereal and Wraithfire forms (elemforms.py)', fill=(20, 20, 20), font=font(24))
for i, r in enumerate(rows): sheet.paste(r, ((i % cols) * W_, 44 + (i // cols) * H_))
sheet.save(os.path.join(OUT, 'contact_sheet.png')); print(os.path.join(OUT, 'contact_sheet.png'))

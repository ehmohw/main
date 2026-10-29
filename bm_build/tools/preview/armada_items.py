"""The Vorn Armada's item art (armada_art.py), previewed.   python3 tools/preview/armada_items.py [icons,models,armor]
icons: every flat icon (vanilla.process'd, as the pack ships them) at 8x on one contact sheet, with each at 1x in a slot below;
models: the 3D models from a 3/4 view, their gui look, the lance and axe beside a vanilla sword's length, the crown on a head;
armor: the Starforged plate (bm:starforged) on a dummy, front and back;
mothership: the Admiral's hull (bm:mothership3d) at the skiff's display (fixed, scale 4.5) beside the Vorn Skiff (ufo3d, from the
shipped dist zip) - front, side, 3/4, below, a cutaway with the seated pilot - and its key's icon.
Sheets go to $AM_OUT (default previews/v299_armada/items); the throwaway pack to draftkit's $BM_PREVIEW_DIR."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from PIL import Image, ImageDraw, ImageFont
import draftkit as K
import armada_art as A
import vanilla

OUT = os.environ.get('AM_OUT', os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), 'previews', 'v299_armada', 'items'))
os.makedirs(OUT, exist_ok=True)
ROOT = os.path.join(K.OUT, 'rp_am')
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['icons', 'models', 'armor', 'mothership']
DIST = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'dist', 'BlackMarket_RP.zip')     # (the shipped skiff, ufo3d, to set beside it)
try:
    FNT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
    FNB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
except OSError:
    FNT = FNB = None


def build_pack():
    os.makedirs(f'{ROOT}/assets/bm/models/item', exist_ok=True); os.makedirs(f'{ROOT}/assets/bm/textures/block', exist_ok=True)
    for k, im in A.textures().items(): im.save(f'{ROOT}/assets/bm/textures/block/{k}.png')
    for name, els in A.models().items():
        json.dump(A.model_json(name, els), open(f'{ROOT}/assets/bm/models/item/{name}.json', 'w'))
    for layer in ('humanoid', 'humanoid_leggings'):
        os.makedirs(f'{ROOT}/assets/bm/textures/entity/{layer}', exist_ok=True)
        A.equip_layer(layer).save(f'{ROOT}/assets/bm/textures/entity/{layer}/starforged.png')


def icons():
    ic = {k: vanilla.process(k, v) for k, v in A.icons().items()}
    names = list(ic); S = 8; T = 16 * S + 20; cols = 6; rows = (len(names) + cols - 1) // cols
    sh = Image.new('RGB', (T * cols, (T + 64) * rows + 40), (198, 198, 198)); d = ImageDraw.Draw(sh)
    d.text((10, 8), 'The Vorn Armada - item icons (8x, and 1x / 2x in a slot)', fill=(20, 20, 20), font=FNB)
    for i, n in enumerate(names):
        x, y = (i % cols) * T, 40 + (i // cols) * (T + 64)
        big = ic[n].resize((16 * S, 16 * S), Image.NEAREST); sh.paste(big, (x + 10, y), big)
        d.rectangle((x + 10, y + T - 10, x + 10 + 19, y + T - 10 + 19), fill=(139, 139, 139)); sh.paste(ic[n], (x + 12, y + T - 8), ic[n])
        two = ic[n].resize((32, 32), Image.NEAREST)
        d.rectangle((x + 36, y + T - 10, x + 36 + 35, y + T - 10 + 35), fill=(139, 139, 139)); sh.paste(two, (x + 38, y + T - 8), two)
        d.text((x + 78, y + T), n, fill=(10, 10, 10), font=FNT)
    p = os.path.join(OUT, 'armada_icons.png'); sh.save(p); print(p)


def tile(scene_fn, view, size=360, span=1.6, center=(0, 0, 0), text=''):
    s = K.multi_scene(ROOT); scene_fn(s)
    im = s.render(view, size=size, span=span, center=center)
    return K.label(im, text)


def models():
    build_pack()
    tiles = []
    for name in A.MODELS3D:
        mid = f'bm:item/{name}'
        tiles.append(tile(lambda s: s.display(mid, ctx='none'), (-35, 22), span=1.7 if 'pylon' not in name else 1.9,
                          center=(0, 0.05 if 'pylon' not in name else 0.25, 0), text=f'{name}  (3/4)'))
        tiles.append(tile(lambda s: s.display(mid, ctx='gui'), 'back', span=1.15, center=(0, 0, 0), text=f'{name}  (gui)'))
    # the crown on a head (head cube 3..13 at the head display's 1.28)
    def head(s):
        s.solid((-0.4, -0.4, -0.4), (0.4, 0.4, 0.4), '#c8956c'); s.solid((-0.41, 0.2, -0.41), (0.41, 0.41, 0.41), '#4a2c14')
        s.solid((-0.25, -0.05, 0.401), (-0.1, 0.05, 0.41), '#ffffff'); s.solid((0.1, -0.05, 0.401), (0.25, 0.05, 0.41), '#ffffff')
        s.display('bm:item/admiral_crown', ctx='head')
    tiles.append(tile(head, (-30, 15), span=2.4, center=(0, 0.35, 0), text='admiral_crown  (worn)'))
    tiles.append(tile(head, (150, 15), span=2.4, center=(0, 0.35, 0), text='admiral_crown  (worn, back)'))
    K.sheet(tiles, os.path.join(OUT, 'armada_models.png'), cols=4, title='The Vorn Armada - 3D items')
    print(os.path.join(OUT, 'armada_models.png'))


def _box(u0, v0, w, h, d, lo, hi, tex):
    U, V = 16 / 64, 16 / 32
    f = lambda a, b, c, e: [a * U, b * V, c * U, e * V]
    return {'from': list(lo), 'to': list(hi), 'faces': {
        'south': {'uv': f(u0 + d, v0 + d, u0 + d + w, v0 + d + h), 'texture': tex},
        'north': {'uv': f(u0 + 2 * d + w, v0 + d, u0 + 2 * d + 2 * w, v0 + d + h), 'texture': tex},
        'west': {'uv': f(u0, v0 + d, u0 + d, v0 + d + h), 'texture': tex},
        'east': {'uv': f(u0 + d + w, v0 + d, u0 + 2 * d + w, v0 + d + h), 'texture': tex},
        'up': {'uv': f(u0 + d, v0, u0 + d + w, v0 + d), 'texture': tex},
        'down': {'uv': f(u0 + d + w, v0, u0 + d + 2 * w, v0 + d), 'texture': tex}}}


def armor():
    build_pack()
    g = lambda lo, hi, k: ([lo[i] - k for i in range(3)], [hi[i] + k for i in range(3)])
    E = []
    a, b = g((4, 24, 4), (12, 32, 12), 1.0); E.append(_box(0, 0, 8, 8, 8, a, b, '#h'))           # (helm)
    a, b = g((4, 12, 6), (12, 24, 10), 1.0); E.append(_box(16, 16, 8, 12, 4, a, b, '#h'))        # (breast)
    for x0 in (0, 12):
        a, b = g((x0, 12, 6), (x0 + 4, 24, 10), 1.0); E.append(_box(40, 16, 4, 12, 4, a, b, '#h'))   # (arms)
    for x0 in (4, 8):
        a, b = g((x0, 0, 6), (x0 + 4, 12, 10), 0.5); E.append(_box(0, 16, 4, 12, 4, a, b, '#l'))     # (leggings)
        a, b = g((x0, 0, 6), (x0 + 4, 12, 10), 1.0); E.append(_box(0, 16, 4, 12, 4, a, b, '#h'))     # (boots)
    a, b = g((4, 12, 6), (12, 24, 10), 0.5); E.append(_box(16, 16, 8, 12, 4, a, b, '#l'))
    m = {'textures': {'h': 'bm:entity/humanoid/starforged', 'l': 'bm:entity/humanoid_leggings/starforged'}, 'elements': E}
    json.dump(m, open(f'{ROOT}/assets/bm/models/item/am_dummy.json', 'w'))
    def sc(s): s.display('bm:item/am_dummy', ctx='none', translation=(0, 0, 0))
    tiles = [tile(sc, (-160, 12), size=420, span=2.6, center=(0, 0.5, 0), text='Starforged (front)'),
             tile(sc, (20, 12), size=420, span=2.6, center=(0, 0.5, 0), text='Starforged (back)')]
    lay = [A.equip_layer(k).resize((64 * 6, 32 * 6), Image.NEAREST) for k in ('humanoid', 'humanoid_leggings')]
    t3 = Image.new('RGB', (420, 420), (198, 198, 198)); t3.paste(lay[0], (18, 10), lay[0]); t3.paste(lay[1], (18, 215), lay[1])
    tiles.append(K.label(t3, 'layers'))
    K.sheet(tiles, os.path.join(OUT, 'armada_starforged.png'), cols=3, title='bm:starforged - the worn plate')
    print(os.path.join(OUT, 'armada_starforged.png'))


def _ms_pack():
    import zipfile
    build_pack()
    tex, els = A.mothership()
    disp = {'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]}}
    t = dict(tex); t['particle'] = 'bm:block/am_plate'
    json.dump({'textures': t, 'elements': els, 'display': disp}, open(f'{ROOT}/assets/bm/models/item/mothership3d.json', 'w'))
    xt = {}                                                                     # (an x-ray copy: the hull's textures see-through)
    for k, v in tex.items():
        if v.startswith('bm:block/'):
            im = Image.open(f'{ROOT}/assets/bm/textures/block/{k}.png').convert('RGBA'); im.putalpha(34)
            im.save(f'{ROOT}/assets/bm/textures/block/xr_{k}.png'); xt[k] = f'bm:block/xr_{k}'
        else: xt[k] = v
    xt['particle'] = 'bm:block/xr_am_plate'
    json.dump({'textures': xt, 'elements': els, 'display': disp}, open(f'{ROOT}/assets/bm/models/item/mothership3d_cut.json', 'w'))
    with zipfile.ZipFile(DIST) as z:
        for n in z.namelist():
            if n == 'assets/bm/models/item/ufo3d.json' or n.startswith('assets/bm/textures/block/skiff_'):
                dst = os.path.join(ROOT, n); os.makedirs(os.path.dirname(dst), exist_ok=True)
                open(dst, 'wb').write(z.read(n))


SC, Y0 = 4.5, 2.4                                                              # (the skiff's scale; lifted clear of the grid)


def _ship(s, mid='bm:item/mothership3d', x=0.0, pilot=True):
    s.display(mid, pos=(x, Y0, 0), scale=SC, ctx='fixed')
    if pilot: K.person(s, (x, Y0 + (A.MS_SEAT[1] / 16 - 0.5) * SC, 0), sit=True)


def mothership():
    _ms_pack()
    tiles = []
    def lineup(s):
        _ship(s); _ship(s, 'bm:item/ufo3d', x=-9.0); K.person(s, (-4.6, 0, 3.0))
    for view, txt in (((-35, 22), 'beside the Vorn Skiff, a player (3/4)'), ((0, 4), 'front'), ((90, 4), 'side'), ((25, -55), 'below')):
        sz = 640
        tiles.append(tile(lineup, view, size=sz, span=17.0, center=(-4.0, 2.4, 0), text=f'The Mothership - {txt}'))
    def hero(s): _ship(s)
    tiles.append(tile(hero, (-38, 26), size=640, span=10.5, center=(0, 2.6, 0), text='The Mothership (3/4, close)'))
    tiles.append(tile(hero, (150, 30), size=640, span=10.5, center=(0, 2.6, 0), text='The Mothership (aft 3/4)'))
    def cut(s): _ship(s, 'bm:item/mothership3d_cut')
    tiles.append(tile(cut, (90, 6), size=640, span=10.5, center=(0, 2.6, 0), text='x-ray: the pilot in the seat (side)'))
    tiles.append(tile(cut, (60, 20), size=640, span=10.5, center=(0, 2.6, 0), text='x-ray (3/4)'))
    K.sheet(tiles, os.path.join(OUT, 'mothership_views.png'), cols=2, title='bm:mothership3d - the Admiral\'s Mothership (skiff display: fixed, x4.5)')
    print(os.path.join(OUT, 'mothership_views.png'))
    # its key, beside the Vorn Skiff's
    ic = vanilla.process('mothership_key', A.mothership_key())
    sk = None
    import zipfile
    with zipfile.ZipFile(DIST) as z:
        import io
        sk = Image.open(io.BytesIO(z.read('assets/bm/textures/item/skiff_key.png'))).convert('RGBA')
    mo = vanilla.process('mothership_module', A.mothership_module())
    sh = Image.new('RGB', (3 * 178 + 10, 230), (198, 198, 198)); d = ImageDraw.Draw(sh)
    for i, (im, n) in enumerate(((sk, 'skiff_key'), (ic, 'mothership_key'), (mo, 'mothership_module'))):
        big = im.resize((128, 128), Image.NEAREST); sh.paste(big, (10 + i * 178, 10), big)
        d.rectangle((10 + i * 178, 150, 29 + i * 178, 169), fill=(139, 139, 139)); sh.paste(im, (12 + i * 178, 152), im)
        two = im.resize((32, 32), Image.NEAREST); d.rectangle((36 + i * 178, 150, 71 + i * 178, 185), fill=(139, 139, 139)); sh.paste(two, (38 + i * 178, 152), two)
        d.text((10 + i * 178, 200), n, fill=(10, 10, 10), font=FNT)
    sh.save(os.path.join(OUT, 'mothership_key.png')); print(os.path.join(OUT, 'mothership_key.png'))


for w in what: globals()[w]()

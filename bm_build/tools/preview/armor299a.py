"""v299a: the armour remodel - the Hero of Time set (hero_armor_art.py) and the Arcade's 8-bit sets (arcade_art.py), before and
after, on a player.      python3 tools/preview/armor299a.py [what,...]
  before   every set as it was (the snapshots in $ARMOR_OLD), front / back / three-quarter
  after    every set as it is now (the art modules), the same
  <set>    (hero, hunter, bomber, plumber, vhunter) its before/after sheet: front, back, three-quarter, the helm close up,
           the four icons before and after -> <set>_before_after.png
  lineup   every redone set side by side -> armor_lineup_after.png
  layers   the flat layers, before and after
The scratch packs hold only the sets' own files (equipment layers, helm models, their block textures); everything else is read
from out_p2's pack and the vanilla client. PNGs to $ARMOR_OUT (default /home/user/main/previews/v299a_armor)."""
import sys, os, json, math, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM)
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from tools.render import Scene, VANILLA
import playerkit as PK

OUT = os.environ.get('ARMOR_OUT', '/home/user/main/previews/v299a_armor'); os.makedirs(OUT, exist_ok=True)
OLD = os.environ.get('ARMOR_OLD', os.path.join(OUT, 'before'))
TMP = os.environ.get('BM_PREVIEW_DIR', '/tmp/bm_previews'); os.makedirs(TMP, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['hero', 'hunter', 'bomber', 'plumber', 'vhunter', 'lineup']
SETS = ['hero', 'hunter', 'bomber', 'plumber', 'vhunter']
ASSET = {'hero': 'hero', 'hunter': 'arc_hunter', 'bomber': 'arc_bomber', 'plumber': 'arc_plumber', 'vhunter': 'arc_vhunter'}
PIECES = {'hero': ['hero_helmet', 'hero_chestplate', 'hero_leggings', 'hero_boots'],
          'hunter': ['hunter_helm', 'hunter_plate', 'hunter_greaves', 'hunter_boots'],
          'bomber': ['bomber_helm', 'bomber_chest', 'bomber_legs', 'bomber_boots'],
          'plumber': ['plumber_cap', 'plumber_shirt', 'plumber_overalls', 'plumber_boots'],
          'vhunter': ['vhunter_band', 'vhunter_cuirass', 'vhunter_legs', 'vhunter_boots']}
TITLE = {'hero': 'The Hero of Time', 'hunter': 'Bounty Hunter', 'bomber': 'Blue Bomber', 'plumber': 'Plumber', 'vhunter': 'Vampire Hunter'}
SKY = np.array([0.78, 0.86, 0.95]) * 255
GRID = [np.array([0.55, 0.62, 0.55]) * 255, np.array([0.2, 0.5, 0.2]) * 255]


# ------------------------------------------------------------------------------------------------ the scratch packs
def _p(root, *a):
    f = os.path.join(root, 'assets', 'bm', *a); os.makedirs(os.path.dirname(f), exist_ok=True); return f


def old_pack(root):
    """the sets as they were: the snapshots' layers (no 3D helms then)"""
    if os.path.exists(root): shutil.rmtree(root)
    for k in SETS:
        a = ASSET[k]
        shutil.copy(os.path.join(OLD, f'{a}.png'), _p(root, 'textures', 'entity', 'equipment', 'humanoid', f'{a}.png'))
        shutil.copy(os.path.join(OLD, f'{a}_leg.png'), _p(root, 'textures', 'entity', 'equipment', 'humanoid_leggings', f'{a}.png'))
    return root


def new_pack(root):
    """the sets as they are now, written by the modules' own rp writers (into a stand-in for gen_rp)"""
    if os.path.exists(root): shutil.rmtree(root)
    class R:
        @staticmethod
        def p(*a):
            f = os.path.join(root, *a); os.makedirs(os.path.dirname(f), exist_ok=True); return f
        @staticmethod
        def wj(rel, obj): json.dump(obj, open(R.p(*rel.split('/')), 'w'))
    import hero_armor_art as HA, arcade_art as AA
    HA.write(R)
    AA.write_sets(R)
    return root


def trimmed_pack(src, root, k='hero', pattern='wayfinder', material='gold'):
    """a copy of a pack with the set's layers wearing a trim, as the game draws it (the pattern in the material's palette, over the layer)"""
    if os.path.exists(root): shutil.rmtree(root)
    shutil.copytree(src, root)
    V = os.path.join(VANILLA, 'minecraft', 'textures')
    key = [Image.open(f'{V}/palettes/trim_base.png').convert('RGBA').getpixel((i, 0))[:3] for i in range(8)]
    pal = [Image.open(f'{V}/palettes/trim/{material}.png').convert('RGBA').getpixel((i, 0)) for i in range(8)]
    for kind in ('humanoid', 'humanoid_leggings'):
        f = _p(root, 'textures', 'entity', 'equipment', kind, f'{ASSET[k]}.png')
        im = Image.open(f).convert('RGBA'); tr = Image.open(f'{V}/trims/entity/{kind}/{pattern}.png').convert('RGBA'); px = tr.load()
        for y in range(tr.height):
            for x in range(tr.width):
                r, g, b, a = px[x, y]
                if a and (r, g, b) in key: px[x, y] = pal[key.index((r, g, b))][:3] + (a,)
        if kind == 'humanoid':                           # (no trim on the head: the cap is its own model, not a layer)
            for y in range(16):
                for x in range(32): px[x, y] = (0, 0, 0, 0)
        im.alpha_composite(tr); im.save(f)
    return root


def helm_model(root, k):
    """the set's 3D helm model id in this pack, if it has one"""
    m = {'hero': 'hero_helmet', 'hunter': 'hunter_helm', 'bomber': 'bomber_helm', 'plumber': 'plumber_cap', 'vhunter': 'vhunter_band'}[k]
    f = os.path.join(root, 'assets', 'bm', 'models', 'item', f'{m}_worn.json')
    return f'bm:item/{m}_worn' if os.path.exists(f) else None


# ------------------------------------------------------------------------------------------------ drawing
def scene(root):
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


def dark(im, top=(34, 30, 52), bot=(12, 10, 20)):
    a = np.asarray(im).astype(np.float32); h, w = a.shape[:2]
    m = np.zeros((h, w), bool)
    for c in [SKY] + GRID: m |= np.all(np.abs(a - c.astype(np.uint8).astype(np.float32)) < 1.5, axis=2)
    t = np.linspace(0, 1, h)[:, None, None]
    g = np.array(top, np.float32) * (1 - t) + np.array(bot, np.float32) * t
    return Image.fromarray(np.where(m[..., None], np.broadcast_to(g, a.shape), a).astype(np.uint8))


def _font(n, bold=True):
    try: return ImageFont.truetype(f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if bold else ""}.ttf', n)
    except OSError: return None


def label(im, text, sub=None):
    d = ImageDraw.Draw(im)
    d.text((10, 8), text, fill=(250, 236, 200), font=_font(15))
    if sub: d.text((10, 27), sub, fill=(190, 180, 210), font=_font(12, False))
    return im


def sheet(tiles, out, cols=4, title=None):
    W, H = max(t.width for t in tiles), max(t.height for t in tiles); rows = (len(tiles) + cols - 1) // cols; top = 44 if title else 0
    sh = Image.new('RGB', (W * cols, H * rows + top), (14, 12, 22))
    if title: ImageDraw.Draw(sh).text((12, 10), title, fill=(250, 236, 200), font=_font(22))
    for i, t in enumerate(tiles): sh.paste(t, ((i % cols) * W, top + (i // cols) * H))
    sh.save(out); print(out); return out


def floor(s, r=2.0, step=0.5):
    n = int(r / step)
    for i in range(-n, n):
        for j in range(-n, n):
            s.solid((i * step, -0.06, j * step), ((i + 1) * step, 0.0, (j + 1) * step), '#3a3450' if (i + j) % 2 else '#2c2840')


def player(layers, skin=True, skin_tex=PK.SKIN):
    """PK.player (standing), but each limb's layer grown a hair more than the body's: the game draws the arms after the body,
    so where their faces lie in one plane (the chestplate's arms over its body) the arm wins - here too, not a z-fight"""
    P, _el = PK.pose('stand')
    out = []
    def part(p, uv, tex, g, tw, th, mirror=False):
        src = p.replace('arml', 'armr').replace('legl', 'legr') if mirror else p
        (w, h, d), o, piv = PK.PARTS[src][1], PK.PARTS[src][2], np.array(PK.PARTS[src][3], float)
        lo = (piv[0] + o[0] - g, piv[1] + o[1] - g, piv[2] + o[2] - g); hi = (piv[0] + o[0] + w + g, piv[1] + o[1] + h + g, piv[2] + o[2] + d + g)
        R, pv = P[p]
        for q, uvs in PK.box_faces(lo, hi, uv, (w, h, d), tw, th, mirror):
            out.append((PK._xf(q, R, pv, np.array(PK.PARTS[p][3], float)), uvs, tex))
    if skin:
        for p in PK.PARTS:
            part(p, PK.SKIN_UV[p], skin_tex, 0.0, 64, 64)
            part(p, PK.HAT_UV[p], skin_tex, 0.5 if p == 'head' else 0.25, 64, 64)
    for tex, which, parts in layers:
        g = 1.0 if which == 'outer' else 0.5
        for p in parts:
            part(p, PK.PARTS[p][0], tex, g + {'armr': 0.02, 'arml': 0.03, 'legr': 0.02, 'legl': 0.03}.get(p, 0.0), 64, 32, mirror=p in ('arml', 'legl'))
    return out


def wearer(s, root, k, at=(0.0, 0.0, 0.0), yaw=0.0, skin=True):
    a = ASSET[k]
    hm = helm_model(root, k)
    outer = ('body', 'armr', 'arml', 'legr', 'legl') if hm else ('head', 'body', 'armr', 'arml', 'legr', 'legl')
    lay = [(f'bm:entity/equipment/humanoid/{a}', 'outer', outer), (f'bm:entity/equipment/humanoid_leggings/{a}', 'inner', ('body', 'legr', 'legl'))]
    PK.put(s, player(lay, skin=skin), at=at, yaw=yaw)
    if hm:
        E = PK._ry(math.radians(-yaw))
        c = E @ np.array((0, 28.0 * PK.S / 16, 0)) + np.array(at)
        s.display(hm, pos=tuple(c), yaw=yaw, scale=0.625 * PK.S, ctx='head')


def tile(root, k, view, text, sub=None, size=330, span=2.6, cy=1.05):
    s = scene(root); floor(s); wearer(s, root, k)
    return label(dark(s.render(view, size=size, span=span, center=(0, cy, 0))), text, sub)


def head_tile(root, k, view, text, sub=None, size=330, span=1.25):
    s = scene(root); floor(s); wearer(s, root, k)
    return label(dark(s.render(view, size=size, span=span, center=(0, 1.58, 0))), text, sub)


def icons_tile(icons, text, sub=None, k=8, size=(330, 330)):
    out = Image.new('RGB', size, (40, 36, 58))
    pos = [(14, 50), (14 + 16 * k + 10, 50), (14, 50 + 16 * k + 10), (14 + 16 * k + 10, 50 + 16 * k + 10)]
    for im, p in zip(icons, pos):
        big = im.convert('RGBA').resize((16 * k, 16 * k), Image.NEAREST)
        bg = Image.new('RGBA', big.size, (58, 52, 80, 255)); bg.alpha_composite(big)
        out.paste(bg.convert('RGB'), p)
    return label(out, text, sub)


def old_icons(k):
    return [Image.open(os.path.join(OLD, f'{i}.png')) for i in PIECES[k]]


def new_icons(k):
    import vanilla
    if k == 'hero':
        import hero_armor_art as HA
        return [vanilla.process(i, HA.icons()[i]) for i in PIECES[k]]
    import arcade_art as AA
    return [vanilla.process(i, AA.icon(i)) for i in PIECES[k]]


def flat(im, text, sub=None, k=6, bg=(40, 36, 58)):
    im = im.convert('RGBA').resize((im.width * k, im.height * k), Image.NEAREST)
    out = Image.new('RGBA', (im.width + 20, im.height + 50), bg + (255,)); out.alpha_composite(im, (10, 44))
    return label(out.convert('RGB'), text, sub)


OLDR = old_pack(os.path.join(TMP, 'rp_armor_old'))
NEWR = new_pack(os.path.join(TMP, 'rp_armor_new')) if any(w != 'before' for w in what) else None
VIEWS = (('front', 'front'), ('back', 'behind'), ((35, 12), 'three-quarter'))

if 'before' in what:
    T = []
    for k in SETS:
        for v, sub in VIEWS: T.append(tile(OLDR, k, v, f'{TITLE[k]} (before)', sub))
        T.append(icons_tile(old_icons(k), 'icons (before)'))
    sheet(T, f'{OUT}/all_before.png', cols=4, title='The five sets, as they were')

if 'after' in what:
    T = []
    for k in SETS:
        for v, sub in VIEWS: T.append(tile(NEWR, k, v, f'{TITLE[k]} (after)', sub))
        T.append(icons_tile(new_icons(k), 'icons (after)'))
    sheet(T, f'{OUT}/all_after.png', cols=4, title='The five sets, now')

for k in SETS:
    if k not in what: continue
    T = []
    for v, sub in VIEWS:
        T.append(tile(OLDR, k, v, 'BEFORE', sub)); T.append(tile(NEWR, k, v, 'AFTER', sub))
    T.append(head_tile(OLDR, k, (30, 10), 'BEFORE', 'the head, close')); T.append(head_tile(NEWR, k, (30, 10), 'AFTER', 'the head, close'))
    if k == 'hero':
        TR = trimmed_pack(NEWR, os.path.join(TMP, 'rp_armor_trim'))
        T.append(tile(TR, k, 'front', 'AFTER + its gold wayfinder trim', 'as the game draws the trim over the layers'))
        T.append(tile(TR, k, (35, 12), 'AFTER + its gold wayfinder trim', 'three-quarter'))
    T.append(icons_tile(old_icons(k), 'BEFORE', 'the icons')); T.append(icons_tile(new_icons(k), 'AFTER', 'the icons'))
    sheet(T, f'{OUT}/{k}_before_after.png', cols=4, title=f'{TITLE[k]} - before and after')

if 'helms' in what:                                     # (working view: each 3D helm from four sides)
    T = []
    for k in [k for k in SETS if helm_model(NEWR, k)]:
        for v, sub in (((20, 8), 'front'), ((90, 5), 'side'), ((145, 12), 'behind, three-quarter'), ((-40, 30), 'above')):
            T.append(head_tile(NEWR, k, v, TITLE[k], sub, size=300, span=1.7))
    sheet(T, f'{OUT}/helms_work.png', cols=4, title='The 3D helms')

if 'lineup' in what:
    done = [k for k in SETS if k not in os.environ.get('ARMOR_SKIP', '').split(',')]
    T = []
    n = len(done); gap = 1.45; span = n * gap + 0.4; size = 1300
    for view, sub in (('front', 'front'), ((30, 12), 'three-quarter'), ('back', 'behind')):
        s = scene(NEWR); floor(s, r=5.0)
        for i, k in enumerate(done): wearer(s, NEWR, k, at=((i - (n - 1) / 2) * gap, 0.0, 0.0))
        im = dark(s.render(view, size=size, span=span, center=(0, 1.05, 0)))
        h = int(size * 2.9 / span); im = im.crop((0, (size - h) // 2, size, (size + h) // 2))
        T.append(label(im, 'The remodelled sets - ' + sub, '   '.join(TITLE[k] for k in (done if view != 'back' else done[::-1]))))
    sheet(T, f'{OUT}/armor_lineup_after.png', cols=1, title='Armour remodel (v299a) - side by side')

if 'layers' in what:
    T = []
    for k in SETS:
        a = ASSET[k]
        for root, txt in ((OLDR, 'before'), (NEWR, 'after')):
            T.append(flat(Image.open(_p(root, 'textures', 'entity', 'equipment', 'humanoid', f'{a}.png')), f'{TITLE[k]} {txt}', 'humanoid'))
            T.append(flat(Image.open(_p(root, 'textures', 'entity', 'equipment', 'humanoid_leggings', f'{a}.png')), f'{TITLE[k]} {txt}', 'humanoid_leggings'))
    sheet(T, f'{OUT}/layers.png', cols=4, title='The layers, flat')

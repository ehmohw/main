"""The Dread Mire (mire_art.py) - preview sheets.   python3 tools/preview/mire.py [lineup,poses,items,turn,night]
lineup   dormant, rise_2 and idle_a beside a player (Steve) for scale; and the same in the dark, its glow (simulated)
poses    every pose, beside a player
items    the two icons (vanilla.process'd, as shipped) at 8x, and 1x / 2x in a slot, beside vanilla items
turn     idle_a and rise_2: front, 3/4, side, back, from above
night    a dark sheet: dormant, rise_2, grab_0 - unlit (moonlight) vs drawn at full brightness (GLOW), light_emission bright
mouth    the maw close: shut, half open, wide - front and 3/4 - the 2.99a first draft (single jaw; $MR_BEFORE, a copy of the old
         mire_art.py) above the jagged petal maw
The scratch pack is written through mire_art.rp (as gen_rp would, its POST included). PNGs to $MR_OUT
(default /home/user/main/previews/v299a_mire). tools/render has no lights: the dark tiles tint each face after the scene is
built (pale_dryad.py's way) - unlit faces dimmed to moonlight, light_emission faces kept bright in proportion to their level."""
import sys, os, json, shutil
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM)
from PIL import Image, ImageDraw, ImageFont
import draftkit as K
import playerkit as PK
import rigkit
import mire_art as A
import vanilla

OUT = os.environ.get('MR_OUT', '/home/user/main/previews/v299a_mire'); os.makedirs(OUT, exist_ok=True)
ROOT = os.path.join(os.environ.get('MR_TMP', K.OUT), 'rp_mire')
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['lineup', 'poses', 'items', 'turn', 'night', 'mouth']
try:
    FNB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16); FNT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
except OSError:
    FNB = FNT = None


def build_pack(root):
    """the Mire as gen_rp writes it: textures (+ .mcmeta), part models, icons (vanilla.process'd), sounds"""
    if os.path.exists(root): shutil.rmtree(root)
    class R:
        POST, ICONS, LANG, TEXTURE_MODS, HATS = [], {}, {}, [], {}
        DISPLAY_3D_EXTRA = ()
        @staticmethod
        def p(*a):
            f = os.path.join(root, *a); os.makedirs(os.path.dirname(f), exist_ok=True); return f
        @staticmethod
        def wj(rel, obj): json.dump(obj, open(R.p(*rel.split('/')), 'w'))
    A.rp(R)
    for mod in R.TEXTURE_MODS:
        for n, im in mod.textures().items(): im.save(R.p('assets', 'bm', 'textures', 'block', n + '.png'))
    for n, im in R.ICONS.items():
        vanilla.process(n, im).save(R.p('assets', 'bm', 'textures', 'item', n + '.png'))
        R.wj(f'assets/bm/models/item/{n}.json', {'parent': 'minecraft:item/generated', 'textures': {'layer0': f'bm:item/{n}'}})
    for n, (tex, els) in R.HATS.items():
        t = dict(tex); t['particle'] = next(iter(tex.values()))
        R.wj(f'assets/bm/models/item/{n}.json', {'textures': t, 'elements': els, 'display': {'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]}}})
    for hook in R.POST: hook(R)
    return R


R = build_pack(ROOT)
FLOOR = ('#3a3a40', '#46464c')                     # (deepslate-ish)


def floor(s, r=5, x0=0.0, z0=0.0, cols=FLOOR):
    for i in range(-r, r):
        for j in range(-r, r):
            s.solid((x0 + i, -0.25, z0 + j), (x0 + i + 1, 0.0, z0 + j + 1), cols[(i + j) % 2])


def steve(s, at=(0, 0, 0), yaw=0.0):
    PK.put(s, PK.player('stand'), at=at, yaw=yaw)


def mire(s, name, at=(0, 0, 0), yaw=0.0):
    rigkit.render(s, A, A.POSES[name], at=at, scale=A.SCALE, yaw=yaw)


def label(im, text, sub=None, col=(30, 30, 30), sub_col=(70, 70, 70)):
    d = ImageDraw.Draw(im); d.text((8, 6), text, fill=col, font=FNB)
    if sub: d.text((8, 26), sub, fill=sub_col, font=FNT)
    return im


def dark_scene(lit=False):
    """a Scene whose display() tints every face: by its element's light_emission (bright), else moonlight - or, lit (the
    brightness override), as painted"""
    s = K.multi_scene(ROOT); base = s.display; s_solid = s.solid

    def display(mid, **kw):
        n0 = len(s.faces); base(mid, **kw)
        lights = [e.get('light_emission', 0) for e in s.model(mid).get('elements', []) for _ in e.get('faces', {})]
        for i, L in enumerate(lights):
            f = s.faces[n0 + i]
            if L:
                k = 0.35 + 0.65 * (L / 15) ** 0.8
                tint = np.array([1.0, 1.0, 1.0]) * (1.0 if L >= 12 else k) if lit else np.array([k, k * 0.96, k * 0.96])
                if lit and L < 12: tint = np.array([1.0, 1.0, 1.0])
                s.faces[n0 + i] = (f[0], f[1], f[2], False if L >= 12 else f[3], tint)
            else:
                s.faces[n0 + i] = (f[0], f[1], f[2], f[3], np.array([0.92, 0.92, 0.95]) if lit else np.array([0.2, 0.21, 0.32]))

    def solid(lo, hi, color='#c08060'):
        c = color.lstrip('#'); rgb = np.array([int(c[i:i + 2], 16) for i in (0, 2, 4)]) * np.array([0.22, 0.23, 0.34])
        s_solid(lo, hi, '#%02x%02x%02x' % tuple(int(v) for v in rgb))
    s.display = display; s.solid = solid
    return s


def darken(im):
    a = np.asarray(im).astype(np.float32)
    sky = (np.abs(a - np.array([199, 219, 242])).sum(axis=2) < 8)
    grid = (np.abs(a - np.array([140, 158, 140])).sum(axis=2) < 10) | (np.abs(a - np.array([51, 127, 51])).sum(axis=2) < 10)
    a[sky] = [10, 10, 18]; a[grid] = [10, 10, 18]
    return Image.fromarray(a.astype(np.uint8))


def put_player_dark(s, at):
    """a player in the dark: its faces dimmed (playerkit draws straight into the face list)"""
    n0 = len(s.faces); steve(s, at)
    for i in range(n0, len(s.faces)):
        f = s.faces[i]
        if f[0] == 'box': continue
        s.faces[i] = tuple(f[:3]) + (f[3] if len(f) > 3 else True, np.array([0.22, 0.23, 0.34]))


# ---------------------------------------------------------------------------------------------------- lineup
if 'lineup' in what:
    xs = {'dormant': -9.0, 'rise_2': 0.0, 'idle_a': 9.5}
    s = K.multi_scene(ROOT)
    for n, x in xs.items(): mire(s, n, at=(x, 0, 0))
    steve(s, (-5.2, 0, 1.0)); steve(s, (4.6, 0, 2.0))
    for i in range(-15, 16):
        for j in range(-5, 5):
            s.solid((i, -0.25, j), (i + 1, 0.0, j + 1), FLOOR[(i + j) % 2])
    N, span = 2400, 27.0; im = s.render((-14, 9), size=N, span=span, center=(0.3, 3.0, 0))
    k = N / span; im = im.crop((0, int(N / 2 - 5.2 * k), N, int(N / 2 + 4.6 * k)))
    d = ImageDraw.Draw(im)
    for n, x in xs.items():
        d.text((int(N / 2 + (x - 0.3 - 1.4) * k * 0.97), 12), n, fill=(20, 20, 20), font=FNB)
    d.text((int(N / 2 + (-5.2 - 0.3 - 0.6) * k * 0.97), 34), 'a player', fill=(60, 60, 60), font=FNT)
    top = Image.new('RGB', (im.width, im.height + 44), 'white'); top.paste(im, (0, 44))
    ImageDraw.Draw(top).text((12, 10), f'The Dread Mire - dormant (the puddle), rise_2 and idle_a, a player (1.8 blocks) for scale. SCALE {A.SCALE}: '
                             '~5 blocks risen, the puddle ~4 across', fill=(10, 10, 10), font=FNB)
    # the dark: the same three, unlit (moonlight) with only light_emission glowing, and drawn at full brightness (GLOW)
    rows = []
    for lit, text in ((False, 'in the dark, no brightness override: only light_emission shows (veins, the mouth, the puddle\'s faint glow)'),
                      (True, 'in the dark, GLOW (brightness 15 on every part, as phase246 sets it): the black hide drawn as painted')):
        s = dark_scene(lit)
        for n, x in xs.items(): mire(s, n, at=(x, 0, 0))
        put_player_dark(s, (-5.2, 0, 1.0)); put_player_dark(s, (4.6, 0, 2.0))
        for i in range(-15, 16):
            for j in range(-5, 5):
                s.solid((i, -0.25, j), (i + 1, 0.0, j + 1), FLOOR[(i + j) % 2])
        imd = darken(s.render((-14, 9), size=N, span=span, center=(0.3, 3.0, 0)))
        imd = imd.crop((0, int(N / 2 - 5.2 * k), N, int(N / 2 + 4.6 * k)))
        ImageDraw.Draw(imd).text((14, 10), text, fill=(230, 220, 225), font=FNB)
        rows.append(imd)
    out = Image.new('RGB', (top.width, top.height + sum(r.height for r in rows)), 'white'); out.paste(top, (0, 0)); y = top.height
    for r in rows: out.paste(r, (0, y)); y += r.height
    p = os.path.join(OUT, 'mire_lineup.png'); out.save(p); print(p)


# ---------------------------------------------------------------------------------------------------- poses
NOTES = {'dormant': 'the puddle alone', 'rise_0': 'the mound swelling', 'rise_1': 'half up, curled', 'rise_2': 'up, mouth open, flaring',
         'idle_a': 'swaying', 'idle_b': 'breathing', 'shriek': 'head back, mouth wide', 'grab_0': 't1 out ~6 blocks, chest height',
         'grab_1': 't1 hauling back in', 'stab_0': 't2 + t3 cocked', 'stab_1': 't2 + t3 tips on the ground ~4 ahead',
         'recoil': 'from the cross', 'sink_0': 'half sunk', 'death_0': 'collapsing', 'death_1': 'a melted heap'}


def tile(name, view=(-32, 14), size=420, span=11.0, center=(0, 2.6, 0.6), text=None, sub=None, player=True, at=(-3.6, 0, 3.2)):
    s = K.multi_scene(ROOT); mire(s, name)
    if player: steve(s, at)
    floor(s, 6, cols=FLOOR)
    lo, hi, zf = A.extent(A.POSES[name])
    return label(s.render(view, size=size, span=span, center=center), text or name,
                 sub or f'{NOTES.get(name, "")}  ({hi * A.SCALE / 16:.1f} tall)')


if 'poses' in what:
    tiles = []
    for n in A.POSE_NAMES:
        if n == 'grab_0': tiles.append(tile(n, view=(72, 12), span=13.0, center=(0, 2.6, 2.4), at=(0.4, 0, 6.3)))
        elif n == 'grab_1': tiles.append(tile(n, view=(72, 12), span=13.0, center=(0, 2.6, 2.4), at=(0.4, 0, 3.0)))
        elif n in ('stab_0', 'stab_1'): tiles.append(tile(n, view=(72, 12), span=13.0, center=(0, 2.8, 1.8), at=(0.6, 0, 4.6)))
        else: tiles.append(tile(n))
    p = os.path.join(OUT, 'mire_poses.png')
    K.sheet(tiles, p, cols=5, title='The Dread Mire - every pose (a player for scale; grab and stab from its side, its front to the left, the player where the blow lands)'); print(p)

# ---------------------------------------------------------------------------------------------------- turnaround
if 'turn' in what:
    tiles = []
    for n in ('idle_a', 'rise_2'):
        for v, l in (('front', 'front'), ((-35, 14), '3/4'), ('side', 'side'), ('back', 'back'), ((-20, 60), 'from above')):
            tiles.append(tile(n, view=v, size=380, text=n, sub=l, player=False))
    tiles.append(tile('dormant', view=(-25, 35), size=380, span=7.0, center=(0, 0.2, 0), text='dormant', sub='the puddle, close', player=False))
    tiles.append(tile('shriek', view=(-10, 8), size=380, span=5.0, center=(0, 5.0, 0.9), text='shriek', sub='the maw, close', player=False))
    tiles.append(tile('rise_2', view=(-35, 12), size=380, span=4.6, center=(0, 4.8, 1.0), text='rise_2', sub='the head, close', player=False))
    tiles.append(tile('idle_a', view=(-40, 5), size=380, span=5.0, center=(1.6, 3.2, -1.2), text='idle_a', sub='a tentacle, close', player=False))
    p = os.path.join(OUT, 'mire_turn.png'); K.sheet(tiles, p, cols=5, title='The Dread Mire - turnarounds and close-ups'); print(p)

# ---------------------------------------------------------------------------------------------------- night
if 'night' in what:
    tiles = []
    for lit in (False, True):
        for n, v, sp, c in (('dormant', (-25, 30), 8.0, (0, 0.3, 0)), ('rise_2', (-32, 12), 11.0, (0, 2.6, -0.6)), ('grab_0', (72, 12), 13.0, (0, 2.6, 2.4))):
            s = dark_scene(lit); mire(s, n); floor(s, 7, cols=FLOOR)
            im = darken(s.render(v, size=420, span=sp, center=c))
            tiles.append(label(im, n, 'GLOW: brightness 15' if lit else 'unlit: light_emission only', col=(230, 220, 225), sub_col=(170, 160, 170)))
    p = os.path.join(OUT, 'mire_night.png'); K.sheet(tiles, p, cols=3, bg='#0a0a12', title=None); print(p)

# ---------------------------------------------------------------------------------------------------- the items
if 'items' in what:
    names = ('shadow_remnant', 'shadow_musk')
    W = 900; strip = Image.new('RGB', (W, 300), (198, 198, 198)); d = ImageDraw.Draw(strip)
    d.text((10, 6), 'The Dread Mire\'s items (vanilla.process\'d, as shipped): 8x, and 1x / 2x in a slot', fill=(20, 20, 20), font=FNB)
    x = 20
    for n in names:
        ic = Image.open(os.path.join(ROOT, 'assets', 'bm', 'textures', 'item', n + '.png')).convert('RGBA')
        big = ic.resize((128, 128), Image.NEAREST); d.rectangle((x - 4, 36, x + 131, 171), fill=(139, 139, 139)); strip.paste(big, (x, 40), big)
        d.rectangle((x + 150, 40, x + 150 + 17, 40 + 17), fill=(139, 139, 139)); strip.paste(ic, (x + 151, 41), ic)
        two = ic.resize((32, 32), Image.NEAREST); d.rectangle((x + 180, 40, x + 180 + 35, 40 + 35), fill=(139, 139, 139)); strip.paste(two, (x + 182, 42), two)
        d.text((x, 180), n, fill=(10, 10, 10), font=FNT)
        x += 260
    van = '/home/claude/mc263/client/assets/minecraft/textures/item/'
    row = [Image.open(os.path.join(ROOT, 'assets', 'bm', 'textures', 'item', n + '.png')).convert('RGBA') for n in names]
    for n in ('ink_sac', 'honey_bottle', 'potion', 'echo_shard', 'slime_ball'):
        f = van + n + '.png'
        if os.path.exists(f): row.append(Image.open(f).convert('RGBA'))
    hx = 20
    for i, ic in enumerate(row):
        big = ic.resize((32, 32), Image.NEAREST)
        d.rectangle((hx + i * 40, 216, hx + i * 40 + 35, 251), fill=(139, 139, 139)); strip.paste(big, (hx + i * 40 + 2, 218), big)
    d.text((hx, 258), 'a hotbar (2x): the remnant, the musk - beside ink sac, honey bottle, potion, echo shard, slimeball', fill=(30, 30, 30), font=FNT)
    p = os.path.join(OUT, 'mire_items.png'); strip.save(p); print(p)

# ---------------------------------------------------------------------------------------------------- the maw, before / after
if 'mouth' in what:
    import importlib.util
    src = os.environ.get('MR_BEFORE', os.path.join(os.environ.get('MR_TMP', K.OUT), 'before', 'mire_before.py'))
    rows = []
    if os.path.exists(src):
        spec = importlib.util.spec_from_file_location('mire_before', src); B = importlib.util.module_from_spec(spec); sys.modules['mire_before'] = B; spec.loader.exec_module(B)
        A_, ROOT_ = A, ROOT
        A = B; ROOT = os.path.join(os.environ.get('MR_TMP', K.OUT), 'rp_mire_before'); build_pack(ROOT)
        A, ROOT_B, ROOT = A_, ROOT, ROOT_
        rows.append(('before (2.99a draft: one jaw)', B, ROOT_B, [(n, dict(B.POSES['rise_2'], jaw=B.JAW(a))) for n, a in (('shut', 0), ('half open', 22), ('wide', 60))]))
    base = {k: v for k, v in A.POSES['rise_2'].items() if k not in A.MAW}
    rows.append(('after (the jagged maw: four petals)', A, ROOT, [(n, dict(base, **A.MAWOPEN(a))) for n, a in (('shut', 0), ('half open', 26), ('wide (shriek)', 78))]))
    tiles = []
    for title, M, root, poses in rows:
        for n, pz in poses:
            c = rigkit.point(M, pz, 'head', (0.0, 37.0, -4.0), scale=M.SCALE)
            pz = dict(pz, _hide=tuple(p for p in M.PARTS if p[0] == 't' and p[1].isdigit()))       # (the tentacles out of the way)
            for v, l in (((-14, 10), 'front'), ((-62, 10), '3/4, from its side')):
                s = K.multi_scene(root); rigkit.render(s, M, pz, scale=M.SCALE)
                im = s.render(v, size=340, span=4.2, center=(c[0], c[1] - 0.2, c[2]))
                tiles.append(label(im, f'{title.split(" (")[0]}: {n}', l))
    p = os.path.join(OUT, 'mire_mouth.png')
    K.sheet(tiles, p, cols=6, title='The Dread Mire - its maw: the first draft (top), the jagged petal maw (below) - shut, half open, wide (tentacles hidden)'); print(p)

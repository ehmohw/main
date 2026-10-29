"""The Rex mounts (rex_art.py) - preview sheets.   python3 tools/preview/rex.py [lineup,poses,items,turn,close]
lineup   both kinds in idle_a beside a player (Steve); each with a player seated in the saddle (a riding Steve, its feet 0.6
         below SEAT, as the game seats a passenger); the same in the dark (light_emission only: the blue glow)
poses    every pose, a sheet per kind (a red marker at the seat, SEATS[pose]; breath_0 / breath_1 with the charged plates)
items    the icons (vanilla.process'd, as shipped) at 8x, 1x and 2x in a vanilla slot, beside vanilla items
turn     each kind's idle_a: front, 3/4, side, back (and from above)
close    close-ups: the heads (shut, roaring), the saddle with its rider, the plates/fins, the tail's joints
The scratch pack is written through rex_art.rp (as gen_rp would). PNGs to $RX_OUT (default /home/user/main/previews/v299a_rex).
tools/render has no lights: the dark tiles tint each face after the scene is built (mire.py's way) - unlit faces dimmed to
night, light_emission faces kept bright."""
import sys, os, json, math, shutil
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM)
from PIL import Image, ImageDraw, ImageFont
import draftkit as K
import playerkit as PK
import rigkit
import rex_art as A
import vanilla

OUT = os.environ.get('RX_OUT', '/home/user/main/previews/v299a_rex'); os.makedirs(OUT, exist_ok=True)
ROOT = os.path.join(os.environ.get('RX_TMP', K.OUT), 'rp_rex')
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['lineup', 'poses', 'items', 'turn', 'close']
try:
    FNB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16); FNT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
except OSError:
    FNB = FNT = None


def build_pack(root):
    """the rexes as gen_rp writes them: textures, part models, icons (vanilla.process'd)"""
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
FLOOR = {'atomic': ('#4a4a44', '#56564e'), 'mecha': ('#3a3e46', '#454a52')}

# a riding player: vanilla's riding pose (HumanoidModel: legs xRot -1.4137 splayed yRot 0.3142, zRot 0.0785; arms xRot -0.6283)
_pose0 = PK.pose


def _pose(kind='stand'):
    if kind != 'ride': return _pose0(kind)
    P, el = _pose0('stand')
    P['legr'] = (PK.e2d(-1.4137167, 0.31415927, 0.07853982), P['legr'][1]); P['legl'] = (PK.e2d(-1.4137167, -0.31415927, -0.07853982), P['legl'][1])
    P['armr'] = (PK.e2d(-0.6283185), P['armr'][1]); P['arml'] = (PK.e2d(-0.6283185), P['arml'][1])
    return P, el


PK.pose = _pose


def floor(s, kind='atomic', r=8, x0=0.0, z0=0.0):
    a, b = FLOOR[kind]
    for i in range(-r, r):
        for j in range(-r, r):
            s.solid((x0 + i, -0.25, z0 + j), (x0 + i + 1, 0.0, z0 + j + 1), a if (i + j) % 2 else b)


def steve(s, at=(0, 0, 0), yaw=0.0, kind='stand'):
    PK.put(s, PK.player(kind), at=at, yaw=yaw)


def _rot(v, yaw):
    c, s_ = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    return (v[0] * c - v[2] * s_, v[1], v[0] * s_ + v[2] * c)


def rider(s, name, at=(0, 0, 0), yaw=0.0):
    """a player riding: its feet 0.6 below the seat (the passenger attachment), facing the rex's front"""
    st = _rot(A.SEATS[name], yaw)
    steve(s, (at[0] + st[0], at[1] + st[1] - 0.6, at[2] + st[2]), yaw=yaw, kind='ride')


def marker(s, name, at=(0, 0, 0), yaw=0.0, r=0.12):
    st = _rot(A.SEATS[name], yaw); c = (at[0] + st[0], at[1] + st[1], at[2] + st[2])
    s.solid((c[0] - r, c[1], c[2] - r), (c[0] + r, c[1] + 2 * r, c[2] + r), '#ff2a2a')


def rex(s, name, kind, at=(0, 0, 0), yaw=0.0):
    rigkit.render(s, A, A.posed(name, kind) if not (name == 'mecha_fist' and kind == 'atomic') else dict(A.POSES['roar'], _kind=kind),
                  at=at, scale=A.SCALE, yaw=yaw)


def label(im, text, sub=None, col=(30, 30, 30), sub_col=(70, 70, 70)):
    d = ImageDraw.Draw(im); d.text((8, 6), text, fill=col, font=FNB)
    if sub: d.text((8, 26), sub, fill=sub_col, font=FNT)
    return im


def dark_scene():
    """a Scene whose display() tints every face: an element with light_emission stays bright, the rest dims to night"""
    s = K.multi_scene(ROOT); base = s.display; s_solid = s.solid

    def display(mid, **kw):
        n0 = len(s.faces); base(mid, **kw)
        lights = [e.get('light_emission', 0) for e in s.model(mid).get('elements', []) for _ in e.get('faces', {})]
        for i, L in enumerate(lights):
            f = s.faces[n0 + i]
            if L: s.faces[n0 + i] = (f[0], f[1], f[2], False, np.array([1.0, 1.0, 1.0]))
            else: s.faces[n0 + i] = (f[0], f[1], f[2], f[3], np.array([0.17, 0.18, 0.28]))

    def solid(lo, hi, color='#c08060'):
        c = color.lstrip('#'); rgb = np.array([int(c[i:i + 2], 16) for i in (0, 2, 4)]) * np.array([0.2, 0.21, 0.32])
        s_solid(lo, hi, '#%02x%02x%02x' % tuple(int(v) for v in rgb))
    s.display = display; s.solid = solid
    return s


def darken(im):
    a = np.asarray(im).astype(np.float32)
    sky = (np.abs(a - np.array([199, 219, 242])).sum(axis=2) < 8)
    grid = (np.abs(a - np.array([140, 158, 140])).sum(axis=2) < 10) | (np.abs(a - np.array([51, 127, 51])).sum(axis=2) < 10)
    a[sky] = [8, 9, 16]; a[grid] = [8, 9, 16]
    return Image.fromarray(a.astype(np.uint8))


def put_player_dark(s, at, yaw=0.0, kind='stand'):
    n0 = len(s.faces); steve(s, at, yaw, kind)
    for i in range(n0, len(s.faces)):
        f = s.faces[i]
        s.faces[i] = tuple(f[:3]) + (f[3] if len(f) > 3 else True, np.array([0.2, 0.21, 0.32]))


def tile(name, kind, view=(-30, 12), size=440, span=15.0, center=(0, 3.8, 0.0), text=None, sub=None, player=None, seat=True, ride=False):
    s = K.multi_scene(ROOT); rex(s, name, kind)
    if player: steve(s, player)
    if ride: rider(s, name)
    elif seat: marker(s, name)
    floor(s, kind)
    lo, hi, zl, zh = A.extent(A.POSES[name], kind)
    return label(s.render(view, size=size, span=span, center=center), text or name,
                 sub or f'{A.NOTES.get(name, "")}  ({hi * A.SCALE / 16:.1f} tall, seat {A.SEATS[name][1]:.2f})')


# ---------------------------------------------------------------------------------------------------- lineup
if 'lineup' in what:
    xs = [('atomic', -13.0, False), ('atomic', -4.0, True), ('mecha', 5.0, False), ('mecha', 14.0, True)]
    N, span = 2600, 36.0; k = N / span; view, cen = (-16, 8), (0.5, 4.2, 0)

    def lay(s, dark=False):
        for kind, x, rd in xs:
            rex(s, 'idle_a', kind, at=(x, 0, 0))
            if rd and dark: put_player_dark(s, (x + A.SEATS['idle_a'][0], A.SEATS['idle_a'][1] - 0.6, A.SEATS['idle_a'][2]), 0.0, 'ride')
            elif rd: rider(s, 'idle_a', at=(x, 0, 0))
        (put_player_dark if dark else steve)(s, (-8.6, 0, 3.0)); (put_player_dark if dark else steve)(s, (0.4, 0, 3.0))
        for i in range(-20, 21):
            for j in range(-7, 7):
                s.solid((i, -0.25, j), (i + 1, 0.0, j + 1), (FLOOR['atomic'] if i < 1 else FLOOR['mecha'])[(i + j) % 2])
    s = K.multi_scene(ROOT); lay(s)
    im = s.render(view, size=N, span=span, center=cen); im = im.crop((0, int(N / 2 - 7.0 * k), N, int(N / 2 + 5.0 * k)))
    d = ImageDraw.Draw(im)
    for kind, x, rd in xs:
        d.text((int(N / 2 + (x - 0.5 - 3.2) * k * 0.97), 12), f'{kind} rex' + (' - ridden' if rd else ''), fill=(20, 20, 20), font=FNB)
        d.text((int(N / 2 + (x - 0.5 - 3.2) * k * 0.97), 32), 'idle_a' + (f', a player in the saddle (SEAT {A.SEAT})' if rd else ''), fill=(60, 60, 60), font=FNT)
    top = Image.new('RGB', (im.width, im.height + 44), 'white'); top.paste(im, (0, 44))
    lo, hi, zl, zh = A.extent(A.POSES['idle_a'])
    ImageDraw.Draw(top).text((12, 10), f'The Rex mounts - Atomic Rex and Mecha Rex (SCALE {A.SCALE}): ~{A.top_of(A.POSES["idle_a"], "head") * A.SCALE / 16:.1f} blocks '
                             f'to the head, {hi * A.SCALE / 16:.1f} to the highest plate, {(zh - zl) * A.SCALE / 16:.1f} nose to tail; players (1.8) for scale',
                             fill=(10, 10, 10), font=FNB)
    s = dark_scene(); lay(s, dark=True)
    imd = darken(s.render(view, size=N, span=span, center=cen)); imd = imd.crop((0, int(N / 2 - 7.0 * k), N, int(N / 2 + 5.0 * k)))
    ImageDraw.Draw(imd).text((14, 10), 'at night: no brightness override - only the light_emission highlights glow (plates / fins, eyes, mouth, reactor, thrusters)',
                             fill=(220, 225, 240), font=FNB)
    out = Image.new('RGB', (top.width, top.height + imd.height), 'white'); out.paste(top, (0, 0)); out.paste(imd, (0, top.height))
    p = os.path.join(OUT, 'rex_lineup.png'); out.save(p); print(p)

# ---------------------------------------------------------------------------------------------------- poses
VIEW = {'breath_1': (-62, 10), 'tailswipe': (-20, 40), 'mecha_fist': (40, 10), 'stomp_0': (-50, 10), 'stomp_1': (-50, 10)}
if 'poses' in what:
    for kind in A.KINDS:
        tiles = []
        for n in A.POSE_NAMES:
            tiles.append(tile(n, kind, view=VIEW.get(n, (-34, 12)), player=(-4.5, 0, 4.0) if n == 'idle_a' else None))
        tiles.append(tile('idle_a', kind, view=(-34, 12), ride=True, text='idle_a, ridden', sub='a riding player at SEAT'))
        tiles.append(tile('sit', kind, view=(-34, 12), ride=True, text='sit, ridden', sub='mounting / dismounting here'))
        p = os.path.join(OUT, f'rex_poses_{kind}.png')
        K.sheet(tiles, p, cols=5, title=f'The {kind.capitalize()} Rex - every pose (the red cube: the seat; breath_0 / breath_1 with the charged plates)'); print(p)

# ---------------------------------------------------------------------------------------------------- turnaround
if 'turn' in what:
    tiles = []
    for kind in A.KINDS:
        for v, l in (('front', 'front'), ((-35, 12), '3/4'), ('side', 'side'), ('back', 'back'), ((-30, 55), 'from above')):
            tiles.append(tile('idle_a', kind, view=v, size=400, span=14.5, text=f'{kind} idle_a', sub=l, seat=False))
    p = os.path.join(OUT, 'rex_turn.png'); K.sheet(tiles, p, cols=5, title='The Rex mounts - turnarounds (idle_a)'); print(p)

# ---------------------------------------------------------------------------------------------------- close-ups
if 'close' in what:
    tiles = []
    for kind in A.KINDS:
        hc = rigkit.point(A, A.POSES['idle_a'], 'head', (0, 44, -6), scale=A.SCALE)
        tiles.append(tile('idle_a', kind, view=(-35, 8), size=400, span=4.5, center=hc, text=f'{kind}: the head', sub='3/4', seat=False))
        tiles.append(tile('idle_a', kind, view=(-5, 4), size=400, span=4.5, center=hc, text=f'{kind}: the head', sub='front', seat=False))
        rc = rigkit.point(A, A.POSES['roar'], 'head', (0, 44, -6), scale=A.SCALE)
        tiles.append(tile('roar', kind, view=(-40, 8), size=400, span=5.0, center=rc, text=f'{kind}: roar', sub='the jaw wide', seat=False))
        st = A.SEATS['idle_a']
        tiles.append(tile('idle_a', kind, view=(-120, 18), size=400, span=6.0, center=(st[0], st[1] - 0.2, st[2]), text=f'{kind}: the saddle', sub='a rider seated', ride=True))
        tiles.append(tile('idle_a', kind, view=(-150, 30), size=400, span=10.0, center=(0, 2.4, -4.5), text=f'{kind}: plates and tail', sub='from behind', seat=False))
    p = os.path.join(OUT, 'rex_close.png'); K.sheet(tiles, p, cols=5, title='The Rex mounts - close-ups'); print(p)

# ---------------------------------------------------------------------------------------------------- the items
if 'items' in what:
    names = A.ITEMS
    W = 1500; strip = Image.new('RGB', (W, 420), (198, 198, 198)); d = ImageDraw.Draw(strip)
    d.text((10, 6), 'The Rex items (vanilla.process\'d, as shipped): 8x, and 1x / 2x in a slot', fill=(20, 20, 20), font=FNB)
    for i, n in enumerate(names):
        x = 20 + (i % 4) * 370; y = 36 + (i // 4) * 180
        ic = Image.open(os.path.join(ROOT, 'assets', 'bm', 'textures', 'item', n + '.png')).convert('RGBA')
        big = ic.resize((128, 128), Image.NEAREST); d.rectangle((x - 4, y, x + 131, y + 135), fill=(139, 139, 139)); strip.paste(big, (x, y + 4), big)
        d.rectangle((x + 150, y + 4, x + 150 + 17, y + 4 + 17), fill=(139, 139, 139)); strip.paste(ic, (x + 151, y + 5), ic)
        two = ic.resize((32, 32), Image.NEAREST); d.rectangle((x + 180, y + 4, x + 180 + 35, y + 4 + 35), fill=(139, 139, 139)); strip.paste(two, (x + 182, y + 6), two)
        d.text((x + 150, y + 50), n, fill=(10, 10, 10), font=FNT)
    van = '/home/claude/mc263/client/assets/minecraft/textures/item/'
    row = [Image.open(os.path.join(ROOT, 'assets', 'bm', 'textures', 'item', n + '.png')).convert('RGBA') for n in names]
    for n in ('bone', 'goat_horn', 'turtle_egg', 'map', 'heart_of_the_sea', 'recovery_compass'):
        f = van + n + '.png'
        if os.path.exists(f): row.append(Image.open(f).convert('RGBA'))
    hx = 20
    for i, ic in enumerate(row):
        big = ic.resize((32, 32), Image.NEAREST)
        d.rectangle((hx + i * 40, 384 - 4, hx + i * 40 + 35, 384 + 31), fill=(139, 139, 139)); strip.paste(big, (hx + i * 40 + 2, 384 - 2), big)
    d.text((hx + len(row) * 40 + 10, 390), 'a hotbar (2x): the Rex items, then vanilla bone, goat horn, turtle egg, map, heart of the sea, recovery compass',
           fill=(30, 30, 30), font=FNT)
    p = os.path.join(OUT, 'rex_items.png'); strip.save(p); print(p)

"""The Statue Knights (knight_art.py) - preview sheets.   python3 tools/preview/knights.py [lineup,poses,items,place,turn,clip]
lineup   both kinds, stone and live, in the statue pose and idle_a, beside a player (Steve) for scale
poses    every pose, a sheet per kind (live), with the stone statue first
items    the placed trophy statues on a block beside a player (front, 3/4, side) and the 16x16 icons at 1x, 2x and 8x in a slot
place    statues flanking a gothic doorway (dread) and a sci-fi door (vorn)
turn     each kind's statue and idle_a, front / 3/4 / side / back
clip     a report: how deep parts cut into each other, pose by pose (the mace against the trunk, the cloak against the legs...)
The scratch pack is written through knight_art.rp (as gen_rp would, its POST included). PNGs to $KN_OUT
(default /home/user/main/previews/v299a_knights)."""
import sys, os, json, math, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM)
from PIL import Image, ImageDraw, ImageFont
import draftkit as K
import playerkit as PK
import rigkit
import knight_art as A
import vanilla

OUT = os.environ.get('KN_OUT', '/home/user/main/previews/v299a_knights'); os.makedirs(OUT, exist_ok=True)
ROOT = os.path.join(K.OUT, 'rp_kn')
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['lineup', 'poses', 'items', 'place', 'turn', 'clip']
try:
    FNB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16); FNT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
except OSError:
    FNB = FNT = None


def build_pack(root):
    """the knights as gen_rp writes them: textures, part models, icons (vanilla.process'd), the statues and item definitions"""
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
FLOOR = {'dread': ('#2a1418', '#3a1c20'), 'vorn': ('#2c3036', '#383d44')}
SKY = None


def floor(s, kind='dread', r=6.0, step=1.0, x0=0.0):
    n = int(r / step); a, b = FLOOR[kind]
    for i in range(-n, n):
        for j in range(-n, n):
            s.solid((x0 + i * step, -0.25, j * step), (x0 + (i + 1) * step, 0.0, (j + 1) * step), a if (i + j) % 2 else b)


def steve(s, at=(0, 0, 0), yaw=0.0):
    PK.put(s, PK.player('stand'), at=at, yaw=yaw)


def knight(s, name, kind, finish, at=(0, 0, 0), yaw=0.0):
    rigkit.render(s, A, A.posed(name, kind, finish), at=at, scale=A.RIG_SCALE, yaw=yaw)


def label(im, text, sub=None, col=(30, 30, 30)):
    d = ImageDraw.Draw(im); d.text((8, 6), text, fill=col, font=FNB)
    if sub: d.text((8, 26), sub, fill=(70, 70, 70), font=FNT)
    return im


def tile(name, kind, finish, view=(-28, 10), size=360, span=4.6, steve_at=None, text=None, sub=None, center=None):
    s = K.multi_scene(ROOT); knight(s, name, kind, finish)
    if steve_at: steve(s, steve_at)
    floor(s, kind, 4.0)
    return label(s.render(view, size=size, span=span, center=center or (0, 1.55, 0)), text or name, sub)


# ---------------------------------------------------------------------------------------------------- lineup
if 'lineup' in what:
    s = K.multi_scene(ROOT)
    xs = {('dread', 'stone', 'statue'): -11.0, ('dread', 'live', 'statue'): -8.0, ('dread', 'stone', 'idle_a'): -5.0, ('dread', 'live', 'idle_a'): -2.0,
          ('vorn', 'stone', 'statue'): 3.0, ('vorn', 'live', 'statue'): 6.0, ('vorn', 'stone', 'idle_a'): 9.0, ('vorn', 'live', 'idle_a'): 12.0}
    for (kind, fin, pz), x in xs.items(): knight(s, pz, kind, fin, at=(x, 0, 0))
    steve(s, (-13.4, 0, 0.4)); steve(s, (0.5, 0, 0.4))
    for i in range(-15, 15):
        for j in range(-3, 3):
            s.solid((i, -0.25, j), (i + 1, 0.0, j + 1), (FLOOR['dread'] if i < 0 else FLOOR['vorn'])[(i + j) % 2])
    N, span = 2400, 28.0; im = s.render((-12, 6), size=N, span=span, center=(0.4, 1.6, 0))
    k = N / span; im = im.crop((0, int(N / 2 - 3.2 * k), N, int(N / 2 + 2.2 * k)))
    d = ImageDraw.Draw(im)
    for (kind, fin, pz), x in xs.items():
        d.text((int(N / 2 + (x - 0.4 - 1.0) * k * 0.98), 12), f'{kind} {fin}', fill=(20, 20, 20), font=FNB)
        d.text((int(N / 2 + (x - 0.4 - 1.0) * k * 0.98), 32), pz, fill=(60, 60, 60), font=FNT)
    im2 = Image.new('RGB', (im.width, im.height + 44), 'white'); im2.paste(im, (0, 44))
    ImageDraw.Draw(im2).text((12, 10), 'The Statue Knights - Undercrown (dread) and Armada (vorn): stone and live, statue and idle_a, a player (1.8) for scale; ~3 blocks tall',
                             fill=(10, 10, 10), font=FNB)
    p = os.path.join(OUT, 'knights_lineup.png'); im2.save(p); print(p)

# ---------------------------------------------------------------------------------------------------- poses
if 'poses' in what:
    for kind in A.KINDS:
        tiles = [tile('statue', kind, 'stone', text='statue (stone)', steve_at=(-2.2, 0, -0.8))]
        tiles += [tile(n, kind, 'live', steve_at=(-2.2, 0, -0.8) if n in ('statue',) else None, view=(-28, 10) if not n.startswith('spin') else (-10, 22),
                       span=5.0 if n.startswith(('spin', 'swing')) else 4.6, center=(0.3 if n.startswith('spin') else 0, 1.6, -0.3 if n == 'swing_1' else 0))
                  for n in A.POSE_NAMES]
        tiles += [tile('death_1', kind, 'stone', text='death_1 (stone)', sub='then it turns to stone in place')]
        p = os.path.join(OUT, f'knights_poses_{kind}.png')
        K.sheet(tiles, p, cols=6, title=f'The Statue Knights - {kind} - every pose (live; the stone statue first, the stone fall last)'); print(p)

# ---------------------------------------------------------------------------------------------------- turnaround
if 'turn' in what:
    tiles = []
    for kind in A.KINDS:
        for n, fin in (('statue', 'stone'), ('idle_a', 'live')):
            for v, l in (('front', 'front'), ((-35, 12), '3/4'), ('side', 'side'), ('back', 'back')):
                tiles.append(tile(n, kind, fin, view=v, size=320, text=f'{kind} {n} {fin}', sub=l))
    p = os.path.join(OUT, 'knights_turn.png'); K.sheet(tiles, p, cols=8, title='The Statue Knights - turnarounds'); print(p)

# ---------------------------------------------------------------------------------------------------- the statue items
if 'items' in what:
    tiles = []
    for kind in A.KINDS:
        for v, l in (('front', 'front'), ((-32, 12), '3/4'), ('side', 'side')):
            s = K.multi_scene(ROOT)
            s.solid((-0.5, -1.0, -0.5), (0.5, 0.0, 0.5), '#5a5a62' if kind == 'dread' else '#8a8e96')          # (the block it was placed on)
            s.display(f'bm:item/{A.STATUES[kind]}', pos=(0, 0.5, 0), yaw=0.0, ctx='fixed')        # (item_display 'fixed' at the air block's centre, yaw 0: facing south, the viewer)
            steve(s, (1.5, 0, 1.2), yaw=0)
            floor(s, kind, 3.0)
            im = s.render(v, size=380, span=4.2, center=(0.4, 1.3, 0))
            tiles.append(label(im, f'{A.STATUES[kind]} - placed', f'{l}; item_display fixed, scale 1'))
    sh = K.sheet(tiles, os.path.join(OUT, '_items_top.png'), cols=6)
    top = Image.open(sh)
    # icons: 8x, and 1x / 2x in a vanilla slot
    W = top.width; strip = Image.new('RGB', (W, 230), (198, 198, 198)); d = ImageDraw.Draw(strip)
    d.text((10, 6), 'The icons (vanilla.process\'d, as shipped): 8x, and 1x / 2x in a slot', fill=(20, 20, 20), font=FNB)
    x = 20
    for kind in A.KINDS:
        ic = Image.open(os.path.join(ROOT, 'assets', 'bm', 'textures', 'item', A.STATUES[kind] + '.png')).convert('RGBA')
        big = ic.resize((128, 128), Image.NEAREST); d.rectangle((x - 4, 36, x + 131, 171), fill=(139, 139, 139)); strip.paste(big, (x, 40), big)
        d.rectangle((x + 150, 40, x + 150 + 17, 40 + 17), fill=(139, 139, 139)); strip.paste(ic, (x + 151, 41), ic)
        two = ic.resize((32, 32), Image.NEAREST); d.rectangle((x + 180, 40, x + 180 + 35, 40 + 35), fill=(139, 139, 139)); strip.paste(two, (x + 182, 42), two)
        d.text((x, 180), A.STATUES[kind], fill=(10, 10, 10), font=FNT)
        x += 300
    # a hotbar row with some vanilla items for comparison
    van = '/home/claude/mc263/client/assets/minecraft/textures/item/'
    row = [Image.open(os.path.join(ROOT, 'assets', 'bm', 'textures', 'item', A.STATUES[k] + '.png')).convert('RGBA') for k in A.KINDS]
    for n in ('iron_sword', 'mace', 'totem_of_undying', 'armor_stand'):
        f = van + n + '.png'
        if os.path.exists(f): row.append(Image.open(f).convert('RGBA'))
    hx = x + 20
    for i, ic in enumerate(row):
        big = ic.resize((32, 32), Image.NEAREST)
        d.rectangle((hx + i * 40, 60, hx + i * 40 + 35, 95), fill=(139, 139, 139)); strip.paste(big, (hx + i * 40 + 2, 62), big)
    d.text((hx, 104), 'beside vanilla (2x): sword, mace, totem, armour stand', fill=(30, 30, 30), font=FNT)
    out = Image.new('RGB', (W, top.height + strip.height), 'white'); out.paste(top, (0, 0)); out.paste(strip, (0, top.height))
    p = os.path.join(OUT, 'knights_statue_items.png'); out.save(p); os.remove(sh); print(p)

# ---------------------------------------------------------------------------------------------------- in place
if 'place' in what:
    def door_gothic(s):
        st, st2, dk = '#3a2a30', '#4a3640', '#120a0e'
        for x in range(-4, 5):
            for y in range(0, 7):
                if -1 <= x <= 1 and y < 4: continue
                if x == 0 and y == 4: continue
                s.solid((x - 0.5, y, 1.5), (x + 0.5, y + 1, 2.5), st if (x + y) % 2 else st2)
        s.solid((-1.5, 0, 2.2), (1.5, 4, 2.5), dk); s.solid((-0.5, 4, 2.2), (0.5, 5, 2.5), dk)
        for x in (-2.5, 2.5):
            s.solid((x - 0.5, 0, 1.0), (x + 0.5, 6.0, 1.5), '#5a4048')
        s.solid((-1.5, 4.6, 1.2), (1.5, 5.0, 1.5), '#a01828')
    def door_scifi(s):
        hl, hd, gl = '#3a3f48', '#2a2e36', '#3ac84a'
        for x in range(-4, 5):
            for y in range(0, 6):
                if -1 <= x <= 1 and y < 4: continue
                s.solid((x - 0.5, y, 1.5), (x + 0.5, y + 1, 2.5), hl if (x + y) % 2 else hd)
        s.solid((-1.5, 0, 2.0), (1.5, 4, 2.5), '#1a1e24'); s.solid((-0.06, 0, 1.94), (0.06, 4, 2.0), gl)
        s.solid((-1.6, 4.0, 1.4), (1.6, 4.2, 1.5), gl); s.solid((-1.6, 0, 1.4), (-1.5, 4.0, 1.5), gl); s.solid((1.5, 0, 1.4), (1.6, 4.0, 1.5), gl)
    tiles = []
    for kind, door in (('dread', door_gothic), ('vorn', door_scifi)):
        for v in ((-22, 10), (0, 4)):
            s = K.multi_scene(ROOT); door(s)
            knight(s, 'statue', kind, 'stone', at=(-2.6, 0, 0.6), yaw=0); knight(s, 'statue', kind, 'stone', at=(2.6, 0, 0.6), yaw=0)
            steve(s, (0.3, 0, -2.6), yaw=180)
            floor(s, kind, 6.0)
            im = s.render(v, size=620, span=9.0, center=(0, 2.6, 0))
            tiles.append(label(im, f'{kind}: statues flanking the door', 'stone, until the puzzle is solved'))
        s = K.multi_scene(ROOT); door(s)
        knight(s, 'statue', kind, 'stone', at=(-2.6, 0, 0.6)); knight(s, 'wake_1', kind, 'live', at=(2.6, 0, 0.0), yaw=-20)
        steve(s, (0.3, 0, -2.6), yaw=180); floor(s, kind, 6.0)
        tiles.append(label(s.render((-22, 10), size=620, span=9.0, center=(0, 2.6, 0)), f'{kind}: one wakes', 'wake_1 (live) beside the statue'))
    p = os.path.join(OUT, 'knights_in_place.png'); K.sheet(tiles, p, cols=3, title='The Statue Knights - in place (mock rooms)'); print(p)

# ---------------------------------------------------------------------------------------------------- clip report
if 'clip' in what:
    SK = {('legr', 'legl'), ('arml', 'chest'), ('armr', 'chest'), ('cape', 'chest')}
    for n in A.POSE_NAMES:
        p = A.POSES[n]; worst = []
        parts = list(A.PARTS)
        for i, a in enumerate(parts):
            for b in parts[i + 1:]:
                if A.PARENT.get(a) == b or A.PARENT.get(b) == a or (a, b) in SK or (b, a) in SK: continue
                if {a, b} in ({'mace', 'forel'}, {'mace', 'forer'}): continue        # (the hands are on the haft)
                d = A.penetration(p, (a,), (b,))
                if d > 0.4: worst.append((round(d, 2), a, b))
        print(f'{n:9s} hands off by {A.ERR[n]}  ' + (', '.join(f'{a}/{b} {d}' for d, a, b in sorted(worst, reverse=True)[:6]) or 'clean'))

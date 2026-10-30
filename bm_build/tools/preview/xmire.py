"""The Brood-Mire (xmire_art.py) - preview sheets (stage-1 draft).   python3 tools/preview/xmire.py [turn,lineup,eyes,arrive,attack,melt,poses]
turn     idle_a and rise_2: front, 3/4, side, back, from above; the puddle close
lineup   the Brood-Mire beside a player and the Dread Mire (mire_art) for size - by day and at night (light_emission only / GLOW)
eyes     the eyes close: the face, a tentacle tip, an eyestalk, the puddle - open, mid-blink (eyes out of step), glancing
arrive   its arrival: dropped balled-up down a green tractor beam, it splats into its puddle and rises
attack   the grab, the stab, the acid spit (wind-up, spit), the writhe (idle_c), the recoil
melt     its death: the Dread Mire's melt (phase246's timings) into a bubbling purple-green goop
poses    every pose
PNGs to $XM_OUT. Scratch packs in $BM_PREVIEW_DIR. tools/render draws the first frame of an animated strip; the eye sheets swap the
eye textures for a chosen frame (xmire_art.eye_textures)."""
import sys, os, json, math, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM)
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import draftkit as K
import playerkit as PK
import rigkit
import xmire_art as A
import mire_art as MA

OUT = os.environ.get('XM_OUT', '/tmp/bm_previews/xmire'); os.makedirs(OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['turn', 'lineup', 'eyes', 'arrive', 'attack', 'melt']
ROOT = K.pack(A, os.path.join(K.OUT, 'rp_xmire'))
MROOT = K.pack(MA, os.path.join(K.OUT, 'rp_mire_cmp'))
FLOOR = ('#2c2a34', '#34323e')                     # (end-stone dusk: a dark floor)
ENDF = ('#d8d49a', '#cfca8e')                      # (end stone)
try:
    FNB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16); FNT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
except OSError:
    FNB = FNT = None


def frame_pack(states):
    """a copy of the pack with each eye texture fixed on a frame: states {eye1: frame, eye2: frame, eye3: frame}"""
    key = '_'.join(f'{k}{v}' for k, v in sorted(states.items()))
    root = os.path.join(K.OUT, f'rp_xmire_{key}')
    if os.path.exists(root): shutil.rmtree(root)
    shutil.copytree(ROOT, root)
    for k, fr in states.items():
        A._eye_frame(*A.EYE_FRAMES[fr]).save(f'{root}/assets/bm/textures/block/bx_{k}.png')
    return root


def floor(s, r=6, cols=ENDF, x0=0.0, z0=0.0):
    for i in range(-r, r):
        for j in range(-r, r):
            s.solid((x0 + i, -0.25, z0 + j), (x0 + i + 1, 0.0, z0 + j + 1), cols[(i + j) % 2])


def steve(s, at=(0, 0, 0), yaw=0.0):
    PK.put(s, PK.player('stand'), at=at, yaw=yaw)


def label(im, text, sub=None, col=(25, 25, 25), sub_col=(70, 70, 70)):
    d = ImageDraw.Draw(im); d.text((8, 6), text, fill=col, font=FNB)
    if sub: d.text((8, 26), sub, fill=sub_col, font=FNT)
    return im


def xm(s, name, at=(0, 0, 0), yaw=0.0, pose=None):
    rigkit.render(s, A, pose or A.POSES[name], at=at, scale=A.SCALE, yaw=yaw)


def tile(name, view=(-32, 14), size=420, span=12.0, center=(0, 2.8, 0.6), text=None, sub=None, player=True, at=(-3.6, 0, 3.2), root=None, pose=None):
    s = K.multi_scene(root or ROOT); xm(s, name, pose=pose)
    if player: steve(s, at)
    floor(s, 7)
    return label(s.render(view, size=size, span=span, center=center), text or name, sub)


def night_scene(lit, *roots):
    """faces tinted after the scene is built: light_emission faces bright, the rest moonlight - or (lit) drawn as painted (GLOW)"""
    s = K.multi_scene(*roots); base = s.display; s_solid = s.solid

    def display(mid, **kw):
        n0 = len(s.faces); base(mid, **kw)
        lights = [e.get('light_emission', 0) for e in s.model(mid).get('elements', []) for _ in e.get('faces', {})]
        for i, L in enumerate(lights):
            if n0 + i >= len(s.faces): break
            f = s.faces[n0 + i]
            if L:
                k = 0.35 + 0.65 * (L / 15) ** 0.8
                tint = np.array([1.0, 1.0, 1.0]) if (lit or L >= 12) else np.array([k, k, k])
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
    a[sky] = [12, 8, 20]
    return Image.fromarray(a.astype(np.uint8))


def dim_player(s, at):
    n0 = len(s.faces); steve(s, at)
    for i in range(n0, len(s.faces)):
        f = s.faces[i]
        if f[0] == 'box': continue
        s.faces[i] = tuple(f[:3]) + (f[3] if len(f) > 3 else True, np.array([0.22, 0.23, 0.34]))


# ---------------------------------------------------------------------------------------------------- turnaround
if 'turn' in what:
    tiles = []
    for n in ('idle_a', 'rise_2'):
        for v, l in (('front', 'front'), ((-35, 14), '3/4'), ('side', 'side'), ('back', 'back'), ((-20, 60), 'from above')):
            tiles.append(tile(n, view=v, size=400, text=f'{n}', sub=l, player=False, span=13.0, center=(0, 3.0, 0.6)))
    tiles.append(tile('dormant', view=(-25, 35), size=400, span=7.5, center=(0, 0.2, 0), text='dormant', sub='the puddle, close: eyes open in it', player=False))
    tiles.append(tile('shriek', view=(-12, 8), size=400, span=5.4, center=(0, 5.3, 0.4), text='shriek', sub='the maw open: the eyes in the throat', player=False))
    tiles.append(tile('idle_a', view=(-30, 10), size=400, span=5.4, center=(0, 5.6, 0.8), text='idle_a', sub='the head, close', player=False))
    tiles.append(tile('idle_a', view=(-55, 8), size=400, span=5.0, center=(2.2, 3.6, -1.6), text='idle_a', sub='a tentacle: suckers, an eye at the tip', player=False))
    tiles.append(tile('idle_c', view=(-35, 14), size=400, span=13.0, center=(0, 3.0, 0.6), text='idle_c', sub='the writhe', player=False))
    p = os.path.join(OUT, 'xmire_turnaround.png'); K.sheet(tiles, p, cols=5, title=f'The {A.NAME} - turnarounds and close-ups'); print(p)

# ---------------------------------------------------------------------------------------------------- lineup: a player, the Dread Mire, the Brood-Mire
if 'lineup' in what:
    N, span = 2400, 28.0; k = N / span
    rows = []
    for mode in ('day', 'dark', 'glow'):
        s = K.multi_scene(ROOT, MROOT) if mode == 'day' else night_scene(mode == 'glow', ROOT, MROOT)
        rigkit.render(s, MA, MA.POSES['idle_a'], at=(-8.5, 0, 0), scale=MA.SCALE)
        xm(s, 'idle_a', at=(1.5, 0, 0)); xm(s, 'dormant', at=(10.5, 0, 0))
        (steve if mode == 'day' else (lambda s_, at: dim_player(s_, at)))(s, (-3.4, 0, 2.0))
        for i in range(-15, 16):
            for j in range(-5, 5):
                s.solid((i, -0.25, j), (i + 1, 0.0, j + 1), ENDF[(i + j) % 2])
        im = s.render((-14, 9), size=N, span=span, center=(0.5, 3.2, 0))
        if mode != 'day': im = darken(im)
        im = im.crop((0, int(N / 2 - 5.6 * k), N, int(N / 2 + 4.4 * k)))
        d = ImageDraw.Draw(im); c = (20, 20, 20) if mode == 'day' else (230, 225, 235)
        d.text((14, 10), {'day': 'by day: the Dread Mire (left, idle_a), a player, the Brood-Mire (idle_a), the Brood-Mire dormant (its puddle)',
                          'dark': 'in the dark, unlit: only light_emission shows - green veins and cysts, yellow eyes, the green-lit maw',
                          'glow': 'in the dark with GLOW (brightness 15 on every part, as phase246 sets it)'}[mode], fill=c, font=FNB)
        rows.append(im)
    out = Image.new('RGB', (N, sum(r.height for r in rows)), 'white'); y = 0
    for r in rows: out.paste(r, (0, y)); y += r.height
    p = os.path.join(OUT, 'xmire_lineup.png'); out.save(p); print(p)

# ---------------------------------------------------------------------------------------------------- the eyes
if 'eyes' in what:
    tiles = []
    sets = [({'eye1': 0, 'eye2': 0, 'eye3': 0}, 'all open'), ({'eye1': 2, 'eye2': 0, 'eye3': 1}, 'mid-blink: eye1 shut, eye3 half (out of step)'),
            ({'eye1': 3, 'eye2': 4, 'eye3': 0}, 'glancing: the pupils aside')]
    for st, l in sets:
        r = frame_pack(st)
        tiles.append(tile('idle_b', view=(-12, 6), size=440, span=4.6, center=(0, 5.0, 0.0), text='the face', sub=l, player=False, root=r))
        tiles.append(tile('idle_a', view=(-24, 12), size=440, span=3.6, center=(-0.2, 7.0, 0.4), text='the eyestalks', sub=l, player=False, root=r))
        tiles.append(tile('dormant', view=(-20, 50), size=440, span=4.6, center=(0, 0.1, 0), text='the puddle', sub=l, player=False, root=r))
    # the eye texture itself, every frame, 12x
    strip = Image.new('RGB', (440, 440), (40, 30, 50)); d = ImageDraw.Draw(strip)
    for i, (st, lk) in enumerate(A.EYE_FRAMES):
        im = A._eye_frame(st, lk).resize((96, 96), Image.NEAREST); strip.paste(im, (16 + (i % 4) * 104, 60 + (i // 4) * 130))
        d.text((16 + (i % 4) * 104, 160 + (i // 4) * 130), f'{st} {lk:+d}' if lk else st, fill=(230, 230, 230), font=FNT)
    d.text((8, 8), 'the eye texture: its frames', fill=(240, 240, 240), font=FNB)
    d.text((8, 30), 'eye1/2/3 play them on their own timings', fill=(200, 200, 200), font=FNT)
    tiles.append(strip)
    s = night_scene(False, frame_pack({'eye1': 0, 'eye2': 1, 'eye3': 0})); xm(s, 'idle_a'); floor(s, 7)
    tiles.append(label(darken(s.render((-24, 8), size=440, span=7.0, center=(0, 4.2, 0.4))), 'at night, unlit', 'the eyes and veins glow on their own', col=(230, 225, 235), sub_col=(180, 170, 190)))
    s = night_scene(False, ROOT); xm(s, 'dormant'); floor(s, 7)
    tiles.append(label(darken(s.render((-25, 35), size=440, span=8.0, center=(0, 0.2, 0))), 'its puddle at night', 'eyes in the dark, watching', col=(230, 225, 235), sub_col=(180, 170, 190)))
    p = os.path.join(OUT, 'xmire_eyes.png'); K.sheet(tiles, p, cols=4, title=f'The {A.NAME} - its eyes (each blinks on its own timing: eye1 / eye2 / eye3)'); print(p)


# ---------------------------------------------------------------------------------------------------- arrival: the tractor beam
def beam(s, top=14.0, r=1.6, rs=None, n=260, base=0.0):
    rs = rs or random.Random(5)
    for _ in range(n):
        a = rs.uniform(0, 2 * math.pi); d = r * math.sqrt(rs.uniform(0, 1)); y = rs.uniform(base, top); sz = rs.uniform(0.06, 0.16)
        x, z = d * math.cos(a), d * math.sin(a)
        s.solid((x - sz, y - sz, z - sz), (x + sz, y + sz, z + sz), rs.choice(('#b6ff3c', '#7dff6a', '#e4ffa0', '#58d830')))
    for k in range(10):                                            # (rings sliding down it)
        y = top * (k + 0.5) / 10; rr = r + 0.15
        for m in range(18):
            a = 2 * math.pi * m / 18; x, z = rr * math.cos(a), rr * math.sin(a)
            s.solid((x - 0.07, y - 0.04, z - 0.07), (x + 0.07, y + 0.04, z + 0.07), '#b6ff3c')


def saucer(s, y=15.0):
    s.solid((-2.6, y, -2.6), (2.6, y + 0.5, 2.6), '#6a7480'); s.solid((-1.6, y + 0.5, -1.6), (1.6, y + 1.3, 1.6), '#8a96a2')
    s.solid((-1.0, y + 1.3, -1.0), (1.0, y + 1.8, 1.0), '#9affd8'); s.solid((-0.9, y - 0.15, -0.9), (0.9, y, 0.9), '#b6ff3c')


if 'arrive' in what:
    tiles = []
    seq = [('beam', 9.0, True, 't0 - a green tractor beam: something balled up comes down it'), ('beam', 4.5, True, 't20 - lowered, writhing in the light'),
           ('beam', 1.2, True, 't36 - it touches down...'), ('rise_0', 0.0, False, 't40 - SPLAT: it bursts into its puddle (the beam cuts out)'),
           ('rise_1', 0.0, False, 't52 - and heaves itself up out of it'), ('rise_2', 0.0, False, 't64 - risen: the eyestalks unfurl'),
           ('shriek', 0.0, False, 't72 - its shriek'), ('idle_a', 0.0, False, 't90 - it hunts (or: the puddle stays, dormant, if nobody is near)')]
    for name, y, bm, lab in seq:
        s = K.multi_scene(ROOT); floor(s, 7)
        pz = dict(A.POSES[name])
        if name == 'rise_0': pz['_hide'] = tuple(p for p in A.PARTS if p not in ('puddle', 'mound'))
        rigkit.render(s, A, pz, at=(0, y, 0), scale=A.SCALE)
        if bm: beam(s, top=15.0, r=2.2, base=0.0); saucer(s, 15.2)
        elif name == 'rise_0':
            rs = random.Random(3)
            for _ in range(40):
                a = rs.uniform(0, 6.28); d = rs.uniform(1.5, 3.8); x, z = d * math.cos(a), d * math.sin(a); yy = rs.uniform(0.2, 1.6); sz = rs.uniform(0.08, 0.2)
                s.solid((x - sz, yy - sz, z - sz), (x + sz, yy + sz, z + sz), rs.choice(('#5a1e7a', '#7dff6a', '#3a1250')))
        steve(s, (-4.2, 0, 4.0))
        tiles.append(label(s.render((-30, 10), size=420, span=17.0, center=(0, 6.8, 0.5)), lab.split(' - ')[0], lab.split(' - ')[1]))
    p = os.path.join(OUT, 'xmire_arrival.png'); K.sheet(tiles, p, cols=4, title=f'The {A.NAME} arrives: lowered down a Vorn tractor beam, it splats into its puddle and rises'); print(p)

# ---------------------------------------------------------------------------------------------------- attacks
if 'attack' in what:
    tiles = []
    def acid(s, a, b, n=9, rs=None):
        rs = rs or random.Random(9)
        for i in range(n):
            t = i / (n - 1); x = a[0] + (b[0] - a[0]) * t; z = a[2] + (b[2] - a[2]) * t; y = a[1] + (b[1] - a[1]) * t + 2.0 * math.sin(math.pi * t)
            sz = 0.28 - 0.12 * t
            s.solid((x - sz, y - sz, z - sz), (x + sz, y + sz, z + sz), '#9cf03a' if i % 2 else '#c8ff70')
            if i % 2: s.solid((x - sz * 0.5 + 0.2, y - sz * 0.5 - 0.3, z - sz * 0.5), (x + sz * 0.5 + 0.2, y + sz * 0.5 - 0.3, z + sz * 0.5), '#6a2a8a')
        for _ in range(16):
            a2 = rs.uniform(0, 6.28); d = rs.uniform(0, 1.3); s.solid((b[0] + d * math.cos(a2) - 0.2, 0.0, b[2] + d * math.sin(a2) - 0.2), (b[0] + d * math.cos(a2) + 0.2, 0.06, b[2] + d * math.sin(a2) + 0.2), '#8ee03a')
    for n, v, sp, c, at, sub in (('grab_0', (72, 12), 14.0, (0, 2.6, 2.4), (0.4, 0, 6.3), 'GRAB: a tentacle shoots out ~6 blocks'),
                                 ('grab_1', (72, 12), 14.0, (0, 2.6, 2.4), (0.4, 0, 3.0), 'and hauls you in'),
                                 ('stab_0', (72, 12), 14.0, (0, 3.0, 1.8), (0.6, 0, 4.6), 'STAB: two tentacles cocked'),
                                 ('stab_1', (72, 12), 14.0, (0, 3.0, 1.8), (0.6, 0, 4.6), 'driven down ~4 ahead'),
                                 ('spit_0', (60, 12), 15.0, (0, 3.2, 3.0), (0.4, 0, 9.5), 'SPIT: it rears, maw wide, every eye on you'),
                                 ('spit_1', (60, 12), 15.0, (0, 3.2, 3.0), (0.4, 0, 9.5), 'a glob of acid lobbed 8-14 blocks'),
                                 ('idle_c', (-35, 14), 13.0, (0, 3.0, 0.6), (-3.6, 0, 3.2), 'the writhe (idle)'),
                                 ('recoil', (-35, 14), 13.0, (0, 3.0, 0.6), (-3.6, 0, 3.2), 'RECOIL: from the Signal Jammer\'s static')):
        s = K.multi_scene(ROOT); xm(s, n); steve(s, at, yaw=180 if at[2] > 5 else 0); floor(s, 8)
        if n == 'spit_1':
            m = rigkit.point(A, A.POSES['spit_1'], 'head', (0.0, A.CY, A.ZB - 8), scale=A.SCALE)
            acid(s, m, (at[0], 0.2, at[2] - 0.2))
        tiles.append(label(s.render(v, size=440, span=sp, center=c), n, sub))
    p = os.path.join(OUT, 'xmire_attacks.png'); K.sheet(tiles, p, cols=4, title=f'The {A.NAME} - its attacks (side on: its front to the left, the player where the blow lands)'); print(p)

# ---------------------------------------------------------------------------------------------------- the melt (phase246's, recoloured)
if 'melt' in what:
    VIEW = (-28, 12)
    TENTS = tuple(p for p in A.PARTS if p[0] == 't' and p[1].isdigit())

    def sprite(s, kind, at, size=1.0):
        s.display(f'bm:item/bx_{kind}', pos=at, yaw=-VIEW[0], pitch=VIEW[1], scale=size)

    tiles = []
    for T, lab in ((10, 't10 - it buckles (death_0)'), (30, 't30 - a heap on its puddle (death_1)'), (50, 't50 - it sags and squashes; the goop wells up'),
                   (70, 't70 - slumped flat, melting into the goop'), (88, 't88 - a bubbling purple-green pile'), (114, 't114 - it shrinks into the ground')):
        s = K.multi_scene(ROOT)
        for i in range(-5, 5):
            for j in range(-5, 5): s.solid((i, -3.0, j), (i + 1, 0.0, j + 1), ENDF[(i + j) % 2])
        pz = A.POSES['death_0' if T < 15 else 'death_1']; U = A.SCALE / 16
        xf = rigkit.solve(A.PIVOT, A.PARENT, pz)
        for p in A.PARTS:
            if A.HIDDEN(p, pz): continue
            kk, dy = (1, 1, 1), 0.0
            if p == 'puddle':
                if T >= 102: u = min(1, (T - 102) / 26); kk = (1 - u,) * 3
            else:
                tent = p in TENTS
                if T >= 86: continue
                elif T >= 74: u = (T - 74) / 12; kk = (1.35 * (1 - u), 0.3 * (1 - u), 1.35 * (1 - u)); dy = -1.0 if not tent else -0.6
                elif T >= 56: u = min(1, (T - 56) / 18); kk = (1.15 + 0.2 * u, 0.7 - 0.4 * u, 1.15 + 0.2 * u); dy = -0.4 - 0.6 * u if not tent else -0.3 - 0.3 * u
                elif T >= 34: u = min(1, (T - 34) / 20); kk = (1 + 0.15 * u, 1 - 0.3 * u, 1 + 0.15 * u); dy = -0.4 * u if not tent else -0.3 * u
            q, t = xf[p]; dp = A.PIVOT[p]
            s.display(f'bm:item/{A.model_id(p)}', pos=(dp[0] * U, dp[1] * U, dp[2] * U), translation=(t[0] * U, t[1] * U + dy, t[2] * U),
                      scale=[A.SCALE * kk[0], A.SCALE * kk[1], A.SCALE * kk[2]], left=tuple(q))
        g = 0 if T < 42 else (min(1, (T - 42) / 30) * 2.2 if T < 102 else 2.2 * max(0, 1 - (T - 102) / 26))
        if g > 0: s.display('bm:item/bx_goop', pos=(0, 0.02 - (0.25 * (T - 102) / 26 if T >= 102 else 0), 0), scale=g)
        rs = random.Random(T)
        if 46 <= T < 104:
            for k in range(6): a = rs.uniform(0, 6.28); r = rs.uniform(0, 1.5); sprite(s, 'bubble', (r * math.cos(a), 0.55 + rs.uniform(0, 0.3), r * math.sin(a)), rs.uniform(0.25, 0.6))
            sprite(s, 'pop', (rs.uniform(-1, 1), 0.7, rs.uniform(-1, 1)), 0.55)
        tiles.append(label(s.render(VIEW, size=440, span=7.5, center=(0, 1.8, 0)), lab.split(' - ')[0], lab.split(' - ')[1]))
    p = os.path.join(OUT, 'xmire_melt.png'); K.sheet(tiles, p, cols=3, title=f'The {A.NAME} melts into a bubbling purple-green goop (phase246 / phase257\'s melt, recoloured)'); print(p)

if 'poses' in what:
    tiles = [tile(n, size=360, span=13.0, center=(0, 3.0, 0.6), sub='') for n in A.POSE_NAMES]
    p = os.path.join(OUT, 'xmire_poses.png'); K.sheet(tiles, p, cols=5, title=f'The {A.NAME} - every pose'); print(p)

"""The Mireling (mireling_art.py) - preview sheets.   python3 tools/preview/mireling.py [lineup,poses,looks,items,doll,clip]
lineup   idle, walk and sit beside a player, and the full-size Dread Mire (mire_art) for comparison; below, the same at night
poses    every pose (DRAFT), with a player for scale; and the six eyes (faces), close
looks    the plain look, the wardrobe's looks (WARDROBE, as phase138 recolours them) and the shiny, idle and close
items    the Mireling's Seed (vanilla.process'd, as shipped) at 8x, 1x and 2x in a slot, beside the Mire's own items
doll     Cecil's doll, baked from the real rig (dolls_bake, A.DOLL) beside the shipped dolls
clip     (text) per pose: pairs of parts cutting into each other beyond their joints, and the lowest point of the risen parts
PNGs to $ML_OUT (default /home/user/main/previews/v300_mireling). tools/render has no lights: the night tiles tint each face
after the scene is built - unlit faces dimmed, light_emission faces kept bright in proportion (keeper.py's way)."""
import sys, os, json, math, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM)
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import draftkit as K
import playerkit as PK
import rigkit
import mireling_art as A
import mire_art as MA
from tools import render as R

OUT = os.environ.get('ML_OUT', '/home/user/main/previews/v300_mireling'); os.makedirs(OUT, exist_ok=True)
SCRATCH = os.environ.get('BM_SCRATCH', '/tmp/bm_previews')
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['lineup', 'poses', 'looks', 'items', 'doll']
ROOT = K.pack(A, f'{SCRATCH}/rp_mireling')
NIGHT_BG, NIGHT_GRID = (14, 14, 26), (30, 30, 44)
FLOOR = ('#5a7a3a', '#64843f')
U = A.RIG_SCALE / 16


def font(sz, bold=True):
    try: return ImageFont.truetype(f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if bold else ""}.ttf', sz)
    except OSError: return None


def mire_pack():
    root = f'{SCRATCH}/rp_mire_for_mireling'
    K.pack(MA, root)
    MA.textures()
    for k, meta in MA.ANIMATED.items():
        json.dump(meta, open(f'{root}/assets/bm/textures/block/{k}.png.mcmeta', 'w'))
    return root


def floor(s, r=3, cols=FLOOR, x0=0.0):
    for i in range(-r, r):
        for j in range(-r, r):
            s.solid((x0 + i, -0.25, j), (x0 + i + 1, 0.0, j + 1), cols[(i + j) % 2])


def steve(s, at=(0, 0, 0), yaw=0.0):
    PK.put(s, PK.player('stand'), at=at, yaw=yaw)


def night_scene(*roots):
    s = K.multi_scene(*(roots or (ROOT,))); base = s.display

    def display(mid, **kw):
        n0 = len(s.faces); base(mid, **kw)
        lights = [e.get('light_emission', 0) for e in s.model(mid).get('elements', []) for _ in e.get('faces', {})]
        for i, L in enumerate(lights):
            f = s.faces[n0 + i]
            k = 0.3 + 0.7 * (L / 15) ** 0.7 if L else None
            tint = np.array([0.17, 0.17, 0.27]) if not L else np.array([k, k, k])
            s.faces[n0 + i] = (f[0], f[1], f[2], False if L else f[3], tint)
    s.display = display

    def solid(lo, hi, color='#c08060'):
        c = tuple(int(int(color[i:i + 2], 16) * 0.2) for i in (1, 3, 5))
        R.Scene.solid(s, lo, hi, '#%02x%02x%02x' % c)
    s.solid = solid
    return s


def steve_dark(s, at):
    n0 = len(s.faces); steve(s, at)
    for i in range(n0, len(s.faces)):
        f = s.faces[i]
        s.faces[i] = tuple(f[:3]) + (f[3] if len(f) > 3 else True, np.array([0.2, 0.2, 0.3]))


def darken(im):
    a = np.asarray(im).astype(np.float32)
    sky = (np.abs(a - np.array([199, 219, 242])).sum(axis=2) < 8)
    grid = (np.abs(a - np.array([140, 158, 140])).sum(axis=2) < 10) | (np.abs(a - np.array([51, 127, 51])).sum(axis=2) < 10)
    a[sky] = NIGHT_BG; a[grid] = NIGHT_GRID
    return Image.fromarray(a.astype(np.uint8))


def dark_label(im, text, sub=None):
    d = ImageDraw.Draw(im); d.text((8, 6), text, fill=(235, 225, 225), font=font(15))
    if sub: d.text((8, 25), sub, fill=(170, 165, 185), font=font(12, False))
    return im


def mireling(s, pose, at=(0, 0, 0), yaw=0.0, scale=None):
    rigkit.render(s, A, A.POSES[pose] if isinstance(pose, str) else pose, at=at, scale=scale or A.RIG_SCALE, yaw=yaw)


NOTES = {'idle_a': 'risen, swaying, the eye peeking', 'idle_b': 'swaying the other way, lid drooping', 'idle_c': 'curious: head tilted, eye wide',
         'walk_0': 'sunk, gliding', 'walk_1': 'the wave through it', 'run_0': 'lower, streaming', 'jump': 'a hop',
         'swim_0': 'floating, paddling', 'sit_a': 'settled: the eye-maw poking up', 'sit_b': 'its idle: the lid drooping',
         'happy': 'tentacles waving, maw open', 'happy_b': '...and the other way', 'hurt': 'flinching, clamped shut',
         'tired': 'fainted: melted flat', 'getup': 'getting up', 'lash_up': 'attack: t1 cocked', 'lash': 'attack: the lash',
         'grab_up': 'grab: raised, maw wide', 'grab': 'grab: shot out', 'grab_pull': 'grab: hauled to the maw'}


def tile(name, view=(32, 12), size=360, span=3.2, center=(0, 0.9, -0.2), player=True, sub=None, at=(1.45, 0, 0.2)):
    s = K.multi_scene(ROOT); mireling(s, name)
    if player: steve(s, at)
    floor(s)
    lo, hi = A.extent(A.POSES[name])
    return K.label(s.render(view, size=size, span=span, center=center), name, sub or f'{NOTES.get(name, "")}  ({max(0, hi) * U:.2f} tall)')


# ---------------------------------------------------------------------------------------------------- lineup
if 'lineup' in what:
    MROOT = mire_pack()
    xs = {'idle_a': 0.0, 'walk_1': 1.6, 'sit_a': 3.0}
    N, span = 2000, 13.0

    def scene(night):
        s = night_scene(ROOT, MROOT) if night else K.multi_scene(ROOT, MROOT)
        for n, x in xs.items(): mireling(s, n, at=(x, 0, 0))
        rigkit.render(s, MA, MA.POSES['idle_a'], at=(-5.6, 0, 1.0), scale=MA.SCALE)
        (steve_dark if night else steve)(s, (-1.5, 0, 0.3)) if night else steve(s, (-1.5, 0, 0.3))
        for i in range(-10, 6):
            for j in range(-4, 4):
                s.solid((i, -0.25, j), (i + 1, 0.0, j + 1), FLOOR[(i + j) % 2])
        return s
    im = scene(False).render((-12, 8), size=N, span=span, center=(-1.6, 2.6, 0))
    d = ImageDraw.Draw(im); k = N / span
    for n, x in xs.items():
        d.text((int(N / 2 + (x + 1.6 - 0.4) * k * 0.98), int(N / 2 + 0.9 * k)), n, fill=(20, 20, 20), font=font(22))
    d.text((int(N / 2 + (-1.5 + 1.6 - 0.5) * k * 0.98), int(N / 2 + 0.9 * k)), 'a player', fill=(40, 40, 40), font=font(20, False))
    d.text((int(N / 2 + (-5.6 + 1.6 - 1.4) * k * 0.98), int(N / 2 + 0.9 * k)), 'the Dread Mire (idle_a)', fill=(40, 40, 40), font=font(20, False))
    d.text((14, 12), f'The Mireling - idle (risen), walk (sunk, gliding) and sit, beside a player and the full-size Dread Mire.  RIG_SCALE {A.RIG_SCALE}: '
                     f'{A.extent(A.POSES["idle_a"])[1] * U:.2f} blocks risen', fill=(10, 10, 10), font=font(22))
    im = im.crop((0, 0, N, int(N / 2 + 1.25 * k)))
    s = night_scene(ROOT, MROOT)
    for n, x in xs.items(): mireling(s, n, at=(x, 0, 0))
    rigkit.render(s, MA, MA.POSES['idle_a'], at=(-5.6, 0, 1.0), scale=MA.SCALE)
    steve_dark(s, (-1.5, 0, 0.3))
    for i in range(-10, 6):
        for j in range(-4, 4):
            s.solid((i, -0.25, j), (i + 1, 0.0, j + 1), FLOOR[(i + j) % 2])
    imd = darken(s.render((-12, 8), size=N, span=span, center=(-1.6, 2.6, 0))).crop((0, 0, N, int(N / 2 + 1.25 * k)))
    dark_label(imd, 'At night: the veins, the eye and the throat glow (light_emission); the puddle glimmers faintly')
    # close at night
    tiles = []
    for n, v in (('idle_a', (-25, 8)), ('idle_c', (-10, 6)), ('sit_a', (-20, 14)), ('walk_0', (-55, 14))):
        s = night_scene(ROOT); mireling(s, n); floor(s)
        tiles.append(dark_label(darken(s.render(v, size=N // 4, span=2.2, center=(0, 0.85 if n.startswith('idle') else 0.35, -0.2))), f'{n}, at night'))
    row = Image.new('RGB', (N, N // 4)); [row.paste(t, (i * (N // 4), 0)) for i, t in enumerate(tiles)]
    out = Image.new('RGB', (N, im.height + imd.height + row.height), 'white')
    out.paste(im, (0, 0)); out.paste(imd, (0, im.height)); out.paste(row, (0, im.height + imd.height))
    p = os.path.join(OUT, 'mireling_lineup.png'); out.save(p); print(p)

# ---------------------------------------------------------------------------------------------------- poses
if 'poses' in what:
    tiles = []
    for n in A.DRAFT:
        if n in ('lash', 'grab', 'grab_pull', 'lash_up'): tiles.append(tile(n, view=(-70, 10), center=(0, 0.9, 0.5), at=(0.0, 0, 1.75)))
        elif n in ('walk_0', 'walk_1', 'run_0'): tiles.append(tile(n, view=(40, 18)))
        else: tiles.append(tile(n))
    # the eyes: every face, close (the maw open so it shows)
    base = dict(A.POSES['idle_a'], **A.MAWOPEN(46))
    for f in (None,) + A.FACES:
        pz = dict(base); pz.pop('_face', None)
        if f: pz['_face'] = f
        c = rigkit.point(A, pz, 'head', (0.0, A.CY, A.ZB - 2.0), scale=A.RIG_SCALE)
        s = K.multi_scene(ROOT); rigkit.render(s, A, pz, scale=A.RIG_SCALE)
        tiles.append(K.label(s.render((-12, 6), size=360, span=0.95, center=c), f'face: {f or "open"}',
                             {v: k for k, v in A.FACE_MAP.items()}.get(f, 'its default eye') if f else 'the default eye'))
    p = os.path.join(OUT, 'mireling_poses.png')
    K.sheet(tiles, p, cols=6, title='The Mireling - every pose (attacks from its side, its front to the right), and its eyes (faces) close'); print(p)

# ---------------------------------------------------------------------------------------------------- looks
if 'looks' in what:
    import gild
    looks = [('plain', None)] + [(n, pal) for k, (n, pal) in A.WARDROBE[1].items() if k <= 3] + [(A.SHINY[0], A.SHINY[1])]
    try:
        gold = [('Gilded Mire (gold)', 'gold')] if 'gold' in gild.TIERS else []
    except Exception:
        gold = []
    tiles, ctiles = [], []
    for name, pal in looks + gold:
        root = f'{SCRATCH}/rp_mireling_look'
        if pal is None: root = ROOT
        else:
            K.pack(A, root)
            ims = A.look_textures(pal) if pal != 'gold' else {n: gild.metal(im, ramp=gild.TIERS['gold']['ramp']) for n, im in A.textures().items() if n in A.RECOL_KEYS}
            for n, im in ims.items(): im.save(f'{root}/assets/bm/textures/block/{n}.png')
        for night in (False, True):
            s = night_scene(root) if night else K.multi_scene(root)
            mireling(s, 'idle_a'); floor(s, 2)
            im = s.render((-28, 10), size=330, span=2.4, center=(0, 0.85, -0.1))
            (tiles if not night else ctiles).append(dark_label(darken(im), name, 'at night') if night else K.label(im, name, 'idle_a'))
        R.Scene._tex_cache = {} if hasattr(R.Scene, '_tex_cache') else None
    p = os.path.join(OUT, 'mireling_looks.png')
    K.sheet(tiles + ctiles, p, cols=len(tiles), title='The Mireling - its looks: plain, the wardrobe (Ember, Void, Frost; then the metals), and the shiny (Bone)'); print(p)

# ---------------------------------------------------------------------------------------------------- items
if 'items' in what:
    import vanilla
    MROOT = mire_pack()
    ic = A.icon()
    others = [('mire_heart', MA.icon('mire_heart')), ('shadow_remnant', MA.icon('shadow_remnant'))]
    W = 900; strip = Image.new('RGB', (W, 300), (198, 198, 198)); d = ImageDraw.Draw(strip)
    d.text((10, 6), "A Mireling's Seed (mire_seed) - vanilla.process'd, as shipped: 8x, 1x and 2x in a slot", fill=(20, 20, 20), font=font(16))
    x = 20
    big = ic.resize((128, 128), Image.NEAREST); d.rectangle((x - 4, 36, x + 131, 171), fill=(139, 139, 139)); strip.paste(big, (x, 40), big)
    d.rectangle((x + 150, 40, x + 167, 57), fill=(139, 139, 139)); strip.paste(ic, (x + 151, 41), ic)
    two = ic.resize((32, 32), Image.NEAREST); d.rectangle((x + 180, 40, x + 215, 75), fill=(139, 139, 139)); strip.paste(two, (x + 182, 42), two)
    d.text((x + 150, 80), '1x      2x', fill=(30, 30, 30), font=font(12, False))
    x = 300
    for n, im in others:
        b = im.resize((128, 128), Image.NEAREST); d.rectangle((x - 4, 36, x + 131, 171), fill=(139, 139, 139)); strip.paste(b, (x, 40), b)
        d.text((x, 176), n + " (the Mire's)", fill=(40, 40, 40), font=font(12, False)); x += 170
    van = '/home/claude/mc263/client/assets/minecraft/textures/item/'
    row = [ic] + [im for _n, im in others]
    for n in ('ink_sac', 'ender_pearl', 'slime_ball', 'echo_shard', 'pumpkin_seeds', 'torchflower_seeds'):
        if os.path.exists(van + n + '.png'): row.append(Image.open(van + n + '.png').convert('RGBA'))
    for i, im in enumerate(row):
        b = im.resize((32, 32), Image.NEAREST)
        d.rectangle((20 + i * 40, 216, 55 + i * 40, 251), fill=(139, 139, 139)); strip.paste(b, (22 + i * 40, 218), b)
    d.text((20, 258), 'a hotbar (2x): the seed, the Mire heart and remnant, then vanilla ink sac, ender pearl, slimeball, echo shard, seeds', fill=(30, 30, 30), font=font(12, False))
    # and on a dark slot
    bg = Image.new('RGB', (150, 150), (40, 40, 50)); b = ic.resize((128, 128), Image.NEAREST); bg.paste(b, (11, 11), b); strip.paste(bg, (W - 170, 30))
    p = os.path.join(OUT, 'mireling_items.png'); strip.save(p); print(p)

# ---------------------------------------------------------------------------------------------------- doll
if 'doll' in what:
    import dolls_bake as DB, phase134 as P134
    parts = P134._rigkit(A, A.POSES['idle_a'], A.RIG_SCALE)
    tex, els = DB.bake(ROOT, parts, ground=A.fit()[0], **A.DOLL)
    json.dump({'textures': tex, 'elements': els}, open(f'{ROOT}/assets/bm/models/item/doll_mireling.json', 'w'))
    dolls = ['doll_emma', 'doll_fishy', 'doll_dryad', 'doll_lightbringer', 'doll_bender', 'doll_henry', 'doll_vexis']
    dolls = [d for d in dolls if os.path.exists(f'{K.REAL}/assets/bm/models/item/{d}.json')]
    tiles = []
    row = dolls[:len(dolls) // 2] + ['doll_mireling'] + dolls[len(dolls) // 2:]
    for view, l in (((160, 10), 'front 3/4'), ((-20, 10), 'back 3/4')):
        s = K.multi_scene(ROOT, K.REAL)
        for i, dn in enumerate(row):
            s.display(f'bm:item/{dn}', pos=(-1.4 + 0.42 * i, 0.5, 0), yaw=180)
        tiles.append(K.label(s.render(view, size=820, span=3.4, center=(-0.1 + 0.42 * (len(row) - 8) / 2, 0.55, 0)), l, '   '.join(d[5:] for d in row)))
    close = []
    for v, l in (((155, 12), 'the Mireling doll, close'), ((110, 12), 'from its side'), ((-25, 12), 'from behind')):
        s = K.multi_scene(ROOT); s.display('bm:item/doll_mireling', pos=(0, 0.5, 0), yaw=180)
        close.append(K.label(s.render(v, size=410, span=1.25, center=(0, 0.62, 0)), l))
    sheet = Image.new('RGB', (820 + 410, max(820 * 2, 410 * 3) + 40), 'white')
    ImageDraw.Draw(sheet).text((12, 8), "The Mireling - Cecil's doll (baked from its real model, the default chibi warp kh 1.55 kb 0.82 kl 0.62; "
                                        "its head: the head and the maw), beside the others", fill=(20, 20, 20), font=font(18))
    for i, t in enumerate(tiles): sheet.paste(t, (0, 40 + 820 * i))
    for i, t in enumerate(close): sheet.paste(t, (820, 40 + 410 * i))
    p = os.path.join(OUT, 'mireling_doll.png'); sheet.save(p); print(p, 'doll elements', len(els))

# ---------------------------------------------------------------------------------------------------- clip
MEET = {frozenset(p) for p in [('body', 'seg1'), ('seg1', 'seg2'), ('seg2', 'head'), ('head', 'maw_u'), ('head', 'maw_r'), ('head', 'jaw'),
                               ('head', 'maw_l'), ('maw_u', 'maw_r'), ('maw_r', 'jaw'), ('jaw', 'maw_l'), ('maw_l', 'maw_u'),
                               ('seg2', 't1a'), ('seg2', 't2a'), ('t1a', 't1b'), ('t1b', 't1c'), ('t2a', 't2b'), ('t2b', 't2c')]}


def _corners(c, ax, h):
    return np.array([[c[i] + sx * ax[0][i] * h[0] + sy * ax[1][i] * h[1] + sz * ax[2][i] * h[2] for i in range(3)]
                     for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)])


def _sat(a, b):
    def axes(c): return [c[4] - c[0], c[2] - c[0], c[1] - c[0]]
    ax = [v for v in axes(a) + axes(b) if np.linalg.norm(v) > 1e-6]
    for u, v in itertools.product(axes(a), axes(b)):
        x = np.cross(u, v)
        if np.linalg.norm(x) > 1e-6: ax.append(x)
    depth = 1e9
    for v in ax:
        v = v / np.linalg.norm(v); pa, pb = a @ v, b @ v
        d = min(pa.max(), pb.max()) - max(pa.min(), pb.min())
        if d <= 0: return 0.0
        depth = min(depth, d)
    return depth


if 'clip' in what:
    for n in A.POSE_NAMES:
        pz = A.POSES[n]; wb = A.world_boxes(pz)
        bx = [(p, _corners(c, ax, h)) for p, bl in wb.items() for c, ax, h, e in bl if e['faces'][next(iter(e['faces']))]['texture'] not in ('#ml_void',)]
        hits = {}
        for (pa, ca), (pb, cb) in itertools.combinations(bx, 2):
            if pa == pb or frozenset((pa, pb)) in MEET: continue
            if not (pa[0] == 't' or pb[0] == 't') or 'body' in (pa, pb): continue        # (the trunk sinking into its mound is meant)
            if (ca.min(0) > cb.max(0)).any() or (cb.min(0) > ca.max(0)).any(): continue
            d = _sat(ca, cb)
            if d > 0.25:
                k = tuple(sorted((pa, pb))); hits[k] = max(hits.get(k, 0), d)
        risen = [p for p in wb if p not in ('body',)]
        low = min(c[:, 1].min() for p, c in bx if p in risen)
        print(f'{n:10s} low {low:+6.2f}  ' + ('  '.join(f'{a}/{b} {d:.1f}' for (a, b), d in sorted(hits.items())) or 'clean'))

"""The Doodle Dragon preview sheets (rigkit) - and a check that no card cuts through another, and he stands on the floor.
python3 tools/preview/doodle_dragon.py [views,poses,faces,lineup,fire,tex,check,player,og,ogcheck,flying,night,looks,doll,fit,zfight,icon,
                                        creeper,crcheck]
(3.0a) He's the Doodle Ender Dragon now; the OG green drawing is his costume ('Crayon Green': a pose with '_og' shows it).
The Doodle Creeper (a second costume: a pose with '_cr' shows it, '_crw' his white flash; A.CR_POSES his own moves): 'creeper'
draws his sheets, 'crcheck' runs the check over every pose (the shared ones and his own) in him.
Sheets go to $BM_PREVIEW_DIR (default previews/v300a_ender_dragon); the scratch packs to $BM_SCRATCH. 'night': tools/render
has no light, so each face is tinted after the scene is built - unlit faces dimmed to night, faces of elements with
light_emission (his eyes) kept bright. 'looks': the wardrobe's recolours made as phase138 makes them. 'doll': baked as
phase141 bakes it (dolls_bake, the default chibi warp), beside the shipped dolls. 'fit': phase134.FIT. 'zfight': zfix's test."""
import sys, os, json, math, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM)
os.environ.setdefault('BM_PREVIEW_DIR', os.path.join(os.path.dirname(BM), 'previews', 'v300a_ender_dragon'))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import draftkit as K, doodle_dragon_art as A, kettle_art as KA, rigkit
from tools import render as R
OUT = os.environ['BM_PREVIEW_DIR']; os.makedirs(OUT, exist_ok=True)
SCRATCH = os.environ.get('BM_SCRATCH', '/tmp/bm_previews'); os.makedirs(SCRATCH, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['views', 'poses', 'faces', 'lineup', 'fire', 'tex', 'check']
root = K.pack(A, SCRATCH + '/rp_dd')
I = A.POSES['idle_a']
OG = lambda pose: dict(pose, _og=True)
CR = lambda pose: dict(pose, _cr=True)
NIGHT_BG, NIGHT_GRID = (16, 18, 34), (34, 38, 52)


def font(sz, bold=True):
    try: return ImageFont.truetype(f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if bold else ""}.ttf', sz)
    except OSError: return None


def night_scene(*roots):
    """a Scene whose display() tints every face by its element's light_emission (dim night when 0)"""
    s = K.multi_scene(*(roots or (root,))); base = s.display

    def display(mid, **kw):
        n0 = len(s.faces); base(mid, **kw)
        lights = [e.get('light_emission', 0) for e in s.model(mid).get('elements', []) for _ in e.get('faces', {})]
        for i, L in enumerate(lights):
            f = s.faces[n0 + i]
            k = 0.22 + 0.78 * (L / 15) ** 0.8 if L else None
            tint = np.array([0.16, 0.17, 0.27]) if not L else np.array([k, k * 0.98, k * 0.92])
            s.faces[n0 + i] = (f[0], f[1], f[2], False if L else f[3], tint)
    s.display = display

    def solid(lo, hi, color='#c08060'):
        c = tuple(int(int(color[i:i + 2], 16) * 0.22) for i in (1, 3, 5))
        R.Scene.solid(s, lo, hi, '#%02x%02x%02x' % c)
    s.solid = solid
    return s


def darken(im, glow=None):
    a = np.asarray(im).astype(np.float32)
    sky = (np.abs(a - np.array([199, 219, 242])).sum(axis=2) < 2)
    grid = (np.abs(a - np.array([140, 158, 140])).sum(axis=2) < 2) | (np.abs(a - np.array([51, 127, 51])).sum(axis=2) < 2)
    a[sky] = NIGHT_BG; a[grid] = NIGHT_GRID
    if glow is not None:                                   # (a soft purple bloom round what glows - as the eye reads it at night)
        from PIL import ImageFilter
        m = Image.fromarray((glow * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))
        g = np.asarray(m).astype(np.float32)[..., None] / 255.0
        a = a + g * np.array([150, 50, 200]) * 0.9
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def dark_label(im, text, sub=None):
    d = ImageDraw.Draw(im); d.text((8, 6), text, fill=(235, 228, 210), font=font(15))
    if sub: d.text((8, 25), sub, fill=(170, 170, 190), font=font(12, False))
    return im


def night_tile(pose, view, span, center, size, label, sub=None, person=None):
    s = night_scene(); rigkit.render(s, A, pose, scale=A.RIG_SCALE)
    if person: K.person(s, person)
    im = s.render(view, size=size, span=span, center=center)
    a = np.asarray(im).astype(np.float32)
    glow = ((a[..., 0] > 150) & (a[..., 2] > 170) & (a[..., 1] < 170)).astype(np.float32)   # (the lit purple: his eyes)
    return dark_label(darken(im, glow), label, sub)


def tile(pose, view=(-30, 12), span=2.4, center=(0, 0.85, 0), size=340, label='', sub=None, person=None):
    s = K.multi_scene(root); rigkit.render(s, A, pose, scale=A.RIG_SCALE * pose.get('_swell', 1.0))
    if person: K.person(s, person)
    return K.label(s.render(view, size=size, span=span, center=center), label, sub)


# ---------------------------------------------------------------------------------------------------- the check
def _cards(pose):
    """every card shown in this pose: (part, world corners p0 p1 p3, uv box, texture alpha)"""
    T, M = A.textures(), A.models()
    xf = rigkit.solve(A.PIVOT, A.PARENT, pose); out = []
    for p in A.PARTS:
        if A.HIDDEN(p, pose): continue
        _tex, els = M[A.model_name(p, pose)]
        q, t = xf[p]; pv = A.PIVOT[p]; Dp = rigkit.D(pv); W = tuple(t[i] + Dp[i] for i in range(3)); k = A.PART_K.get(p, 1.0)
        def world(m):
            d = tuple((m[i] - 8) * k + pv[i] for i in range(3)); r = rigkit.qrot(q, tuple(rigkit.D(d)[i] - Dp[i] for i in range(3)))
            return np.array([W[i] + r[i] for i in range(3)])
        for e in els:
            (x1, y1, z1), (x2, y2, z2) = e['from'], e['to']
            Q = {'north': [(x2, y2, z1), (x1, y2, z1), (x1, y1, z1), (x2, y1, z1)], 'south': [(x1, y2, z2), (x2, y2, z2), (x2, y1, z2), (x1, y1, z2)],
                 'east': [(x2, y2, z2), (x2, y2, z1), (x2, y1, z1), (x2, y1, z2)], 'west': [(x1, y2, z1), (x1, y2, z2), (x1, y1, z2), (x1, y1, z1)],
                 'up': [(x1, y2, z1), (x2, y2, z1), (x2, y2, z2), (x1, y2, z2)], 'down': [(x1, y1, z2), (x2, y1, z2), (x2, y1, z1), (x1, y1, z1)]}
            for fc, f in e['faces'].items():
                if fc in ('south', 'west', 'down'): continue           # (a card's other face: the same shape)
                al = np.asarray(T[f['texture'][1:]])[..., 3] > 0
                c = [world(v) for v in Q[fc]]
                out.append((p, c[0], c[1], c[3], f['uv'], al))
    return out


def _opaque(card, X):
    """is world point X (n x 3, on the card's plane) on a coloured pixel of this card?"""
    _p, p0, p1, p3, uv, al = card
    e1, e2 = p1 - p0, p3 - p0; d = X - p0
    a = d @ e1 / (e1 @ e1); b = d @ e2 / (e2 @ e2)
    u = uv[0] + a * (uv[2] - uv[0]); v = uv[1] + b * (uv[3] - uv[1])
    H, W = al.shape; ok = (a >= 0) & (a <= 1) & (b >= 0) & (b <= 1)
    ui = np.clip((u / 16 * W).astype(int), 0, W - 1); vi = np.clip((v / 16 * H).astype(int), 0, H - 1)
    return ok & al[vi, ui]


def check(name, pose):
    cards = _cards(pose); clips = {}
    for i in range(len(cards)):
        for j in range(i + 1, len(cards)):
            a, b = cards[i], cards[j]
            if a[0] == b[0]: continue
            na = np.cross(a[2] - a[1], a[3] - a[1]); nb = np.cross(b[2] - b[1], b[3] - b[1])
            na, nb = na / np.linalg.norm(na), nb / np.linalg.norm(nb); d = np.cross(na, nb)
            if np.linalg.norm(d) < 1e-4:                               # (parallel: only a worry if they share the plane)
                if abs((b[1] - a[1]) @ na) < 0.06:
                    g = np.stack(np.meshgrid(np.linspace(0, 1, 64), np.linspace(0, 1, 64)), -1).reshape(-1, 2)
                    X = a[1] + g[:, :1] * (a[2] - a[1]) + g[:, 1:] * (a[3] - a[1])
                    n = int((_opaque(a, X) & _opaque(b, X)).sum())
                    if n: clips[(a[0], b[0], 'same plane')] = n
                continue
            d = d / np.linalg.norm(d)
            Mx = np.array([na, nb, d]); rhs = np.array([na @ a[1], nb @ b[1], 0.0]); x0 = np.linalg.solve(Mx, rhs)
            X = x0 + np.arange(-48, 48, 0.04)[:, None] * d
            n = int((_opaque(a, X) & _opaque(b, X)).sum())
            if n: clips[(a[0], b[0])] = clips.get((a[0], b[0]), 0) + n
    low = 1e9
    for c in cards:
        if c[0] in A.FX: continue
        _p, p0, p1, p3, uv, al = c; H, W = al.shape
        vi, ui = np.nonzero(al)
        a = ((ui + 0.5) / W * 16 - uv[0]) / (uv[2] - uv[0]); b = ((vi + 0.5) / H * 16 - uv[1]) / (uv[3] - uv[1])
        Y = p0[1] + a * (p1 - p0)[1] + b * (p3 - p0)[1]
        if len(Y): low = min(low, float(Y.min()))
    return clips, low


def run_check(og=False, cr=False):
    bad = 0; tag = 'OG ' if og else ('CR ' if cr else '')
    poses = dict((n, CR(pz)) for n, pz in A.POSES.items()) if cr else A.POSES
    if cr: poses.update(A.CR_POSES)
    for n, pz in poses.items():
        clips, low = check(n, OG(pz) if og else pz)
        exp = 0.8 if n in ('run_1', 'run_3') else 0.0                  # (a run's airborne frames: a little off the floor)
        flag = '' if (n in A.AIRBORNE or n.startswith('swim_') or abs(low - exp) < 0.35) else '  <- FLOOR'
        if low < exp - 0.35 and not n.startswith('swim_'): flag = '  <- BELOW THE FLOOR'
        if clips or flag: bad += 1
        print(f'{tag}{n:12s} lowest {low:6.2f}{flag}  ' + ('  '.join(f'{k}:{v}' for k, v in clips.items()) if clips else 'clean'))
    print(('OG green: ' if og else ('Doodle Creeper: ' if cr else '')) + 'poses with problems:', bad)


if 'check' in what:
    run_check()
if 'ogcheck' in what:
    run_check(og=True)
if 'crcheck' in what:
    run_check(cr=True)

TITLE = 'The Doodle Ender Dragon'
if 'views' in what:
    K.sheet([tile(I, v, label=l) for v, l in (('front', 'front'), ((-35, 18), '3/4'), ('side', 'side (flat!)'), ('back', 'back'), ((150, 15), 'back 3/4'))],
            OUT + '/ender_turnaround.png', cols=5, title=f'{TITLE} - turnaround')
if 'player' in what:
    tiles = [tile(I, v, span=3.3, center=(0.45, 1.05, 0), size=440, label=l, sub='beside a player (1.8 tall)', person=(1.3, 0, 0.1))
             for v, l in (('front', 'front'), ((-35, 14), 'three-quarter'), ('back', 'back'), ((-78, 6), 'side (a paper puppet: all but flat)'))]
    K.sheet(tiles, OUT + '/ender_beside_player.png', cols=4, title=f'{TITLE} - front, three-quarter, back and side, beside a player')
if 'poses' in what:
    K.sheet([tile(A.POSES[n], label=n, sub=(A.POSES[n].get('_face') or '')) for n in A.DRAFT], OUT + '/ender_poses.png', cols=6,
            title=f'{TITLE} - poses')
if 'faces' in what:
    tiles = []
    for f in (None,) + A.FACES:
        pose = {k: v for k, v in dict(I, _face=f).items() if v is not None}
        s = K.multi_scene(root); rigkit.render(s, A, pose, scale=A.RIG_SCALE)
        tiles.append(K.label(s.render('front', size=260, span=0.95, center=(0, 1.15, 0)), f or 'default'))
    K.sheet(tiles, OUT + '/ender_faces.png', cols=5, title=f'{TITLE} - faces (the eyes and particles glow: a card of their own)')
if 'fire' in what:
    views = (((-30, 12), '3/4', 0.5), ('front', 'front', 0.5), ((-80, 8), 'side', 1.0), ((-40, 50), 'from above', 0.5))
    tiles = [tile(A.POSES[n], v, span=3.4, center=(0, 0.9, cz), label=n, sub=l) for n in ('breathe_up', 'breathe') for v, l, cz in views]
    K.sheet(tiles, OUT + '/ender_fire.png', cols=4, title=f'{TITLE} - crayon fire')
if 'flying' in what:
    tiles = []
    for n, v, l in (('flap_0', (-25, 10), 'flap_0 - wings up'), ('flap_1', (-25, 10), 'flap_1 - wings down, off the ground'), ('happy', 'front', 'happy - wings spread wide'),
                    ('jump', (-30, 20), 'jump'), ('flap_0', (160, 15), 'flap_0 from behind'), ('flap_0', (-20, -25), 'from below')):
        tiles.append(tile(A.POSES[n], v, span=2.9, center=(0, 1.1, 0), size=400, label=l, sub=n))
    K.sheet(tiles, OUT + '/ender_flying.png', cols=3, title=f'{TITLE} - flying: the big bat wings spread')
if 'night' in what:
    tiles = [night_tile(I, (-30, 12), 3.3, (0.45, 1.05, 0), 440, 'at night', 'his eyes and the ender particles aglow', person=(1.3, 0, 0.1)),
             night_tile(A.POSES['flap_0'], (-25, 10), 2.9, (0, 1.1, 0), 440, 'at night, flying', 'flap_0'),
             night_tile(A.POSES['breathe'], (-30, 12), 3.4, (0, 0.9, 0.5), 440, 'at night, crayon fire', 'breathe'),
             night_tile(I, 'front', 0.95, (0, 1.15, 0), 440, 'at night, close', 'the eyes'),
             night_tile(dict(I, _face='fierce'), 'front', 0.95, (0, 1.15, 0), 440, 'at night, fierce', ''),
             night_tile(I, (150, 15), 2.6, (0, 1.0, 0), 440, 'at night, from behind', 'the particles show from behind too')]
    K.sheet(tiles, OUT + '/ender_night.png', cols=3, title=f'{TITLE} - by night: glowing purple eyes (light_emission 15)')
if 'og' in what:
    tiles = []
    for v, l in (('front', 'front'), ((-35, 14), 'three-quarter'), ('back', 'back')):
        for pz, nm in ((I, 'Doodle Ender Dragon (default)'), (OG(I), 'Crayon Green (costume, _og)')):
            tiles.append(tile(pz, v, span=2.6, center=(0, 0.95, 0), size=360, label=nm, sub=l))
    K.sheet(tiles, OUT + '/ender_vs_og_green.png', cols=6, title=f'{TITLE} - the new default and the OG green drawing, his costume "Crayon Green"')
    tiles = []
    for f in (None,) + A.FACES:
        pose = {k: v for k, v in dict(OG(I), _face=f).items() if v is not None}
        s = K.multi_scene(root); rigkit.render(s, A, pose, scale=A.RIG_SCALE)
        tiles.append(K.label(s.render('front', size=220, span=0.95, center=(0, 1.15, 0)), f or 'default', 'Crayon Green'))
    tiles += [tile(OG(A.POSES[n]), label=n, sub='Crayon Green', size=220) for n in ('breathe', 'flap_0', 'sit_a', 'tired')]
    K.sheet(tiles, OUT + '/og_green_costume.png', cols=7, title='Crayon Green (the OG drawing, a costume) - every face, and a few poses on the shared rig')
if 'tex' in what:
    T = A.textures(); ims = []
    for k, im in T.items():
        big = Image.new('RGBA', (256, 256), (255, 255, 255, 255))
        im2 = im.resize((256, 256), Image.NEAREST); big.alpha_composite(im2)
        ims.append(K.label(big.convert('RGB'), k, f'{im.width}x{im.height}'))
    K.sheet(ims, OUT + '/ender_textures.png', cols=8, title=f'{TITLE} - textures (the crayon pictures; _g: the OG green)')
if 'lineup' in what:
    rk = K.pack(KA, SCRATCH + '/rp_kt')
    s = K.multi_scene(root, rk)
    rigkit.render(s, A, I, at=(0.0, 0, 0), scale=A.RIG_SCALE)
    rigkit.render(s, KA, KA.POSES['idle_a'], at=(1.35, 0, 0.2), scale=KA.RIG_SCALE)
    rigkit.render(s, A, OG(I), at=(-1.35, 0, 0.2), scale=A.RIG_SCALE)
    K.person(s, (2.5, 0, 0.3))
    K.sheet([K.label(s.render((-12, 8), size=720, span=4.6, center=(0.55, 1.1, 0)), 'size', 'Crayon Green (costume), the Doodle Ender Dragon, Kettle (who drew him), a player')],
            OUT + '/ender_lineup.png', cols=1, title=f'{TITLE} - next to Kettle')


# ---------------------------------------------------------------------------------------------------- fit, doll, looks, zfight, icon
def fit(pose=I):
    """phase134.FIT: (lowest y, height, x0, x1, z0, z1) in blocks, idle_a at RIG_SCALE"""
    s = K.multi_scene(root)
    rigkit.render(s, A, pose, scale=A.RIG_SCALE)
    pts = np.array([v for f in s.faces for v in f[0]])
    lo, hi = pts.min(0), pts.max(0)
    return (round(lo[1], 3), round(hi[1] - lo[1], 3), round(lo[0], 3), round(hi[0], 3), round(lo[2], 3), round(hi[2], 3))


if 'fit' in what:
    print('FIT =', fit())
    print('FIT (OG green, for reference) =', fit(OG(I)))
if 'doll' in what:
    import dolls_bake as DB, phase134 as P134
    parts = P134._rigkit(A, I, A.RIG_SCALE)                           # (as phase141: the figurine's parts, the default chibi warp)
    lo = fit()[0]
    tex, els = DB.bake(root, parts, ground=lo, kh=1.55, kb=0.82, kl=0.62)
    json.dump({'textures': dict(tex), 'elements': els}, open(f'{root}/assets/bm/models/item/doll_dragon_ender.json', 'w'))
    others = ['doll_eraser', 'doll_cursor', 'doll_inkblot', 'doll_speech', 'doll_kettle', 'doll_capshun']   # (not the shipped doll_dragon: it would wear these new textures)
    others = [d for d in others if os.path.exists(f'{K.REAL}/assets/bm/models/item/{d}.json')]
    tiles = []
    row = others[:3] + ['doll_dragon_ender'] + others[3:]
    for view, l in (((-20, 10), 'front 3/4'), ((160, 10), 'back 3/4')):
        s = K.multi_scene(root, K.REAL)
        xs = [-1.75 + 0.5 * i for i in range(len(row))]
        for x, dname in zip(xs, row):
            s.display(f'bm:item/{dname}', pos=(x, 0.5, 0), yaw=0)
        tiles.append(K.label(s.render(view, size=900, span=4.2, center=(0.0, 0.55, 0)), l,
                             '   '.join(('NEW ender' if d == 'doll_dragon_ender' else d[5:] + (' (old, green)' if d == 'doll_dragon' else '')) for d in row)))
    close = []
    for v, l in (((-25, 12), 'the Doodle Ender Dragon doll, close'), ((150, 12), 'from behind'), ('front', 'front')):
        s = K.multi_scene(root); s.display('bm:item/doll_dragon_ender', pos=(0, 0.5, 0), yaw=0)
        close.append(K.label(s.render(v, size=450, span=1.25, center=(0, 0.62, 0)), l))
    sheet = Image.new('RGB', (900 + 450, max(900 * 2, 450 * 3) + 40), 'white')
    ImageDraw.Draw(sheet).text((12, 8), "The Doodle Ender Dragon - Cecil's doll (baked from his real model; chibi warp kh 1.55 kb 0.82 kl 0.62), beside the doodles' dolls",
                               fill=(20, 20, 20), font=font(16))
    for i, t in enumerate(tiles): sheet.paste(t, (0, 40 + 900 * i))
    for i, t in enumerate(close): sheet.paste(t, (900, 40 + 450 * i))
    sheet.save(OUT + '/ender_doll.png')
    print('doll elements', len(els))
if 'looks' in what:
    import phase99 as P99, phase138 as P138, gild, shiny
    base = A.textures()
    looks = [(0, 'no look (his own)', None)] + [(k, n, pal) for k, (n, pal) in P99.NEW['dragon'][3].items()]
    rows = {False: ([], []), True: ([], [])}
    for og in (False, True):
        for k, name, pal in looks:
            r = root
            if pal is not None:
                r = K.pack(A, f'{SCRATCH}/rp_dd_look')
                if gild.is_gilded('dragon', k): ims = {n: gild.dress('dragon', k, base[n]) for n in A.LOOK_TEX}
                else:
                    main = {n: base[n] for n in A.LOOK_TEX if not n.endswith('_g')}
                    ims = P99._recolour(main, pal)
                    ims.update(P99._recolour({n: base[n] for n in A.LOOK_TEX if n.endswith('_g')}, pal))
                for n, im in ims.items():
                    assert im.size == base[n].size, (n, im.size)
                    im.save(f'{r}/assets/bm/textures/block/{n}.png')
            pz = OG(I) if og else I
            for night in (False, True):
                s = night_scene(r) if night else K.multi_scene(r)
                rigkit.render(s, A, pz, scale=A.RIG_SCALE)
                im = s.render((-30, 10), size=280, span=2.5, center=(0, 0.95, 0))
                rows[og][1 if night else 0].append(dark_label(darken(im), name, 'at night') if night else K.label(im, name, f'look {k}' if k else ('Crayon Green' if og else 'default')))
    K.sheet(rows[False][0] + rows[False][1], OUT + '/ender_looks.png', cols=len(looks),
            title=f"{TITLE} - his wardrobe (phase138's recolours: A.LOOK_TEX; the eyes keep their purple), by day and by night")
    K.sheet(rows[True][0] + rows[True][1], OUT + '/og_green_looks.png', cols=len(looks),
            title="Crayon Green (the OG costume) in every look ('_g' textures recoloured as a set of their own), by day and by night")
if 'zfight' in what:
    import zfix
    n = 0
    for f in sorted(os.listdir(f'{root}/assets/bm/models/item')):
        if not f.startswith(A.PREFIX): continue
        m = json.load(open(f'{root}/assets/bm/models/item/{f}'))
        k = zfix.fix_model(f'{root}/assets', m)
        if k: print('z-fighting:', f, k)
        n += k
    print('zfight: faces zfix would move =', n)
if 'coords' in what:                                                     # (every element inside the model box, every uv in 0..16)
    bad = 0
    for name, (tex, els) in A.models().items():
        for e in els:
            for v in e['from'] + e['to']:
                if not -16 <= v <= 32: bad += 1; print('out of the box:', name, e['from'], e['to'])
            for fc, f in e['faces'].items():
                if any(not 0 <= u <= 16 for u in f['uv']): bad += 1; print('uv:', name, fc, f['uv'])
                assert f['texture'][1:] in A.textures(), (name, f['texture'])
    print('coords/uv problems:', bad, 'over', len(A.models()), 'models')
if 'icon' in what:
    import sprites299 as SP
    im = SP.doodle_drawing()
    sh = Image.new('RGB', (760, 220), 'white'); d = ImageDraw.Draw(sh)
    d.text((10, 8), "Kettle's Dragon Drawing (doodle_drawing) - the summoning item, redrawn: the Doodle Ender Dragon", fill=(20, 20, 20), font=font(14))
    x = 20
    for k in (1, 2, 8):
        big = im.resize((16 * k, 16 * k), Image.NEAREST); sh.paste(big, (x, 40 + (128 - 16 * k) // 2), big); x += 16 * k + 24
    slot = Image.new('RGB', (36, 36), (139, 139, 139)); ImageDraw.Draw(slot).rectangle((0, 0, 35, 35), outline=(55, 55, 55))
    slot.paste(im.resize((32, 32), Image.NEAREST), (2, 2), im.resize((32, 32), Image.NEAREST)); sh.paste(slot, (x, 86))
    bg = Image.new('RGB', (90, 90), (40, 40, 50)); big = im.resize((64, 64), Image.NEAREST); bg.paste(big, (13, 13), big); sh.paste(bg, (x + 60, 60))
    sh.save(OUT + '/ender_icon.png')


# ---------------------------------------------------------------------------------------------------- the Doodle Creeper
def creeper_ref(s, at):
    """a vanilla creeper's size (1.7 tall, 0.6 wide): head 0.5, body 0.75, four feet 0.375 tall"""
    x, y, z = at
    s.solid((x - 0.25, 1.2, z - 0.25), (x + 0.25, 1.7, z + 0.25), '#5cbf4a')
    s.solid((x - 0.25, 0.375, z - 0.125), (x + 0.25, 1.2, z + 0.125), '#4fa83e')
    for dx in (-0.125, 0.125):
        for dz in (-0.25, 0.25):
            s.solid((x + dx - 0.125, 0.0, z + dz - 0.125), (x + dx + 0.125, 0.375, z + dz + 0.125), '#3f8f32')
    for ex in (-0.15, 0.1):                                              # (its face: two eyes, roughly)
        s.solid((x + ex - 0.01, 1.45, z - 0.26), (x + ex + 0.06, 1.52, z - 0.25), '#101010')


if 'creeper' in what:
    CT = 'The Doodle Creeper'
    tiles = []                                                           # 1. beside the Ender default and Crayon Green
    for v, l in (('front', 'front'), ((-35, 14), 'three-quarter'), ('back', 'back')):
        for pz, nm in ((I, 'Doodle Ender Dragon (default)'), (OG(I), 'Crayon Green (_og)'), (CR(I), 'Doodle Creeper (_cr)')):
            tiles.append(tile(pz, v, span=2.6, center=(0, 0.95, 0), size=360, label=nm, sub=l))
    K.sheet(tiles, OUT + '/creeper_vs_ender_og.png', cols=3, title=f'{CT} - beside the Doodle Ender Dragon and Crayon Green (front, 3/4, back)')
    tiles = []                                                           # 2. every face
    for f in (None,) + A.FACES:
        pose = {k: v for k, v in dict(CR(I), _face=f).items() if v is not None}
        s = K.multi_scene(root); rigkit.render(s, A, pose, scale=A.RIG_SCALE)
        tiles.append(K.label(s.render('front', size=300, span=0.72, center=(0, 1.12, 0)), f or 'default', 'creeper face'))
    K.sheet(tiles, OUT + '/creeper_faces.png', cols=5, title=f'{CT} - every face (the head card: drawn in black crayon, in the look\'s colours)')
    tiles = []                                                           # 3. his attacks
    ATT = [('breathe_up', CR(A.POSES['breathe_up']), (-30, 12), 'the hiss (wind-up, _fire kindle)'), ('breathe', CR(A.POSES['breathe']), (-40, 14), 'spark breath (_fire fire)'),
           ('breathe', CR(A.POSES['breathe']), (-80, 8), 'spark breath, side'), ('swipe', CR(A.POSES['swipe']), 'front', 'the pop (Claw: _slash)'),
           ('stomp', CR(A.POSES['stomp']), (-25, 10), 'stomp dust (_boom)'), ('idle_c', CR(A.POSES['idle_c']), (-30, 12), 'hiccup (_fire puff)'),
           ('swell_0', A.CR_POSES['swell_0'], (-30, 12), 'swell: crouch, cheeks puffed'), ('swell_1', A.CR_POSES['swell_1'], (-30, 12), 'swell: puffed up, WHITE FLASH (_crw)'),
           ('kaboom', A.CR_POSES['kaboom'], 'front', 'KABOOM (_fire kaboom)'), ('kaboom', A.CR_POSES['kaboom'], (-35, 12), 'KABOOM, 3/4'),
           ('reform', A.CR_POSES['reform'], (-30, 12), 'scribbled back together')]
    for n, pz, v, l in ATT:
        sp = 4.0 if n in ('breathe', 'kaboom') else 2.8
        cz = 0.6 if n == 'breathe' and v != 'front' else 0
        tiles.append(tile(pz, v, span=sp, center=(0, 1.0, cz), size=380, label=n, sub=l))
    K.sheet(tiles, OUT + '/creeper_attacks.png', cols=4, title=f'{CT} - his attacks: hiss, spark breath, pop, stomp, the swell and its white flash, KABOOM')
    sw = []                                                              # 3b. the swell sequence, side by side, big
    for n, pz in (('idle_a', CR(I)), ('swell_0', A.CR_POSES['swell_0']), ('swell_1', A.CR_POSES['swell_1']), ('kaboom', A.CR_POSES['kaboom']), ('reform', A.CR_POSES['reform'])):
        sw.append(tile(pz, (-20, 10), span=3.6, center=(0, 1.1, 0), size=420, label=n))
    K.sheet(sw, OUT + '/creeper_swell.png', cols=5, title=f'{CT} - the swell: idle, crouch, puff up and flash white, KABOOM, scribble back together')
    tiles = [tile(CR(A.POSES[n]), label=n, sub=(A.POSES[n].get('_face') or ''), size=300) for n in A.CR_DRAFT]   # 4. the shared poses in him
    K.sheet(tiles, OUT + '/creeper_poses.png', cols=7, title=f'{CT} - the shared rig\'s poses, as the creeper')
    rk = K.pack(KA, SCRATCH + '/rp_kt')                                  # 5. the lineup
    s = K.multi_scene(root, rk)
    rigkit.render(s, A, OG(I), at=(-2.6, 0, 0.2), scale=A.RIG_SCALE)
    rigkit.render(s, A, I, at=(-1.3, 0, 0.1), scale=A.RIG_SCALE)
    rigkit.render(s, A, CR(I), at=(0.0, 0, 0), scale=A.RIG_SCALE)
    creeper_ref(s, (1.05, 0, 0.1))
    rigkit.render(s, KA, KA.POSES['idle_a'], at=(2.1, 0, 0.2), scale=KA.RIG_SCALE)
    K.person(s, (3.2, 0, 0.3))
    K.sheet([K.label(s.render((-12, 8), size=900, span=6.0, center=(0.3, 1.1, 0)), 'size',
                     'Crayon Green, the Doodle Ender Dragon, the Doodle Creeper, a vanilla creeper (1.7 tall, solid boxes), Kettle, a player')],
            OUT + '/creeper_lineup.png', cols=1, title=f'{CT} - lineup')
    import phase99 as P99, gild                                          # 6. the wardrobe's looks (+ shiny), as phase138 makes them
    base = A.textures(); tiles = []
    for k, (name, pal) in [(0, ('his own', None))] + list(P99.NEW['dragon'][3].items()):
        r = root
        if pal is not None:
            r = K.pack(A, f'{SCRATCH}/rp_dd_crlook')
            if k == max(P99.NEW['dragon'][3]): ims = {n: A.charged(base[n]) for n in A.LOOK_CR}      # (the shiny: a charged creeper - A.SHINY_SETS)
            elif gild.is_gilded('dragon', k): ims = {n: gild.dress('dragon', k, base[n]) for n in A.LOOK_CR}
            else: ims = P99._recolour({n: base[n] for n in A.LOOK_CR}, pal)
            for n, im in ims.items(): im.save(f'{r}/assets/bm/textures/block/{n}.png')
        s = K.multi_scene(r); rigkit.render(s, A, CR(I), scale=A.RIG_SCALE)
        tiles.append(K.label(s.render((-30, 10), size=260, span=2.3, center=(0, 0.95, 0)), name, f'look {k}' + (' (shiny: charged)' if k == 7 else '') if k else 'Doodle Creeper'))
    K.sheet(tiles, OUT + '/creeper_looks.png', cols=8, title=f"{CT} - in every look (phase138: his '_cp' textures recoloured as a set of their own)")

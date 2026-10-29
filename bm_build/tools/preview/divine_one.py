"""The Divine One preview sheets (rigkit).   python3 tools/preview/divine_one.py [poses,turn,scale,hero,detail,anim,clip]
poses: the cinematic's poses in order (a sheet, and one big tile each); turn: a turnaround (reveal); scale: He beside the
Sovereign's true form at its BOSS_SCALE and a player, so the size reads; hero: the smite beside the Sovereign (the beam, then the
pillar of light) and a look up at Him from His feet;
detail: the head's faces, the halo, the gathering light, the wings from behind; anim: the cinematic as a GIF (the game's
interpolation between the keys); clip: parts cutting into each other, pose by pose.
PNGs go to $DIVINE_OUT (default /home/user/main/previews/v298c_divine); the throwaway resource packs to $BM_PREVIEW_DIR.
The renderer's sky is swapped for the dark of the Undercrown (He is lit from within: what matters is how He reads in the dark)."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import numpy as np
from PIL import Image
import draftkit as K, rigkit
import divine_art as A
OUT = os.environ.get('DIVINE_OUT', '/home/user/main/previews/v298c_divine'); os.makedirs(OUT, exist_ok=True)
os.makedirs(K.OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['poses', 'turn', 'scale', 'hero', 'detail', 'anim', 'clip']
root = K.pack(A, K.OUT + '/rp_dvn')
FLOOR, FLOOR2 = '#2a1418', '#3a1c20'
SKY = np.array([0.78, 0.86, 0.95]) * 255
GRID = [np.array([0.55, 0.62, 0.55]) * 255, np.array([0.2, 0.5, 0.2]) * 255]
SC = A.BOSS_SCALE


def dark(im, top=(26, 18, 34), bot=(8, 5, 10)):
    """the renderer's sky (and its little grid) swapped for a dark gradient"""
    a = np.asarray(im).astype(np.float32); h, w = a.shape[:2]
    m = np.zeros((h, w), bool)
    for c in [SKY] + GRID: m |= np.all(np.abs(a - c.astype(np.uint8).astype(np.float32)) < 1.5, axis=2)
    t = np.linspace(0, 1, h)[:, None, None]
    g = np.array(top, np.float32) * (1 - t) + np.array(bot, np.float32) * t
    a = np.where(m[..., None], np.broadcast_to(g, a.shape), a)
    return Image.fromarray(a.astype(np.uint8))


def label(im, text, sub=None):
    """draftkit's label, in light ink (on the dark)"""
    from PIL import ImageDraw, ImageFont
    d = ImageDraw.Draw(im)
    try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16); g = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
    except OSError: f = g = None
    d.text((10, 8), text, fill=(250, 236, 200), font=f)
    if sub: d.text((10, 28), sub, fill=(190, 176, 150), font=g)
    return im


def floor(s, r=16.0, step=2.0, cx=0.0, cz=0.0):
    n = int(r / step)
    for i in range(-n, n):
        for j in range(-n, n):
            s.solid((cx + i * step, -0.25, cz + j * step), (cx + (i + 1) * step, 0.0, cz + (j + 1) * step), FLOOR if (i + j) % 2 else FLOOR2)


def scene(pose, at=(0, 0, 0), yaw=0.0, fl=True, person=None, r=16.0, *roots):
    s = K.multi_scene(root, *roots)
    rigkit.render(s, A, pose, at=at, scale=A.scale_of(pose), yaw=yaw)
    if person is not None: K.person(s, person)
    if fl: floor(s, r)
    return s


def top(pose, parts):
    """the highest point of these parts in this pose (blocks)"""
    return max(c[1] + sum(abs(ax[i][1]) * h[i] for i in range(3)) for p, bl in A.world_boxes(pose, parts).items() for c, ax, h in bl) * SC / 16


H = top(A.BOSS_POSES['rest'], A.HALOS)                         # (to the halo's top, blocks)
HOOD = top(A.BOSS_POSES['rest'], ('head',))


def tile(pose, view=(-28, 8), size=520, text='', sub=None, span=None, cy=None, fl=True, person=None):
    s = scene(pose, fl=fl, person=person)
    return label(dark(s.render(view, size=size, span=span or H * 1.25, center=(0, cy if cy is not None else H * 0.5, 0))), text, sub)


def sheet(tiles, out, cols=4, title=None):
    from PIL import ImageDraw, ImageFont
    W, Ht = tiles[0].size; rows = (len(tiles) + cols - 1) // cols; top = 44 if title else 0
    sh = Image.new('RGB', (W * cols, Ht * rows + top), (12, 8, 14))
    if title:
        try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
        except OSError: f = None
        ImageDraw.Draw(sh).text((12, 9), title, fill=(255, 236, 190), font=f)
    for i, t in enumerate(tiles): sh.paste(t, ((i % cols) * W, top + (i // cols) * Ht))
    sh.save(out); return out


ORDER = [n for n, _ in A.SEQUENCE]

if 'poses' in what:
    tiles = [tile(A.BOSS_POSES[n], text=f'{i + 1}. {n}', size=460) for i, n in enumerate(ORDER)]
    tiles.append(tile(A.BOSS_POSES['smite'], view=(60, 6), text='smite (side)', sub='the beam down and forward', size=460))
    sheet(tiles, OUT + '/divine_poses.png', cols=4, title='The Divine One - the cinematic\'s poses, in order')
    for i, n in enumerate(ORDER):
        tile(A.BOSS_POSES[n], text=f'{i + 1}. {n}', size=760).save(OUT + f'/divine_pose_{i + 1}_{n}.png')

if 'turn' in what:
    p = A.BOSS_POSES['reveal']
    sheet([tile(p, v, 520, l, fl=v[1] >= 0 if isinstance(v, tuple) else True)
           for v, l in (('front', 'front'), ((-35, 10), '3/4'), ('side', 'side'), ((145, 10), 'back 3/4'), ('back', 'back'), ((-30, -14), 'from below'))],
            OUT + '/divine_turnaround.png', cols=3, title='The Divine One - turnaround (reveal)')

if 'scale' in what or 'hero' in what:
    import dread_sovereign_art as DS
    rds = K.pack(DS, K.OUT + '/rp_ds')

if 'scale' in what:
    # (in the world He faces +z: the Sovereign stands before Him, turned to face Him, a player between)
    s = K.multi_scene(root, rds)
    sov = DS.BOSS_POSES['true']['idle_a']
    rigkit.render(s, A, A.BOSS_POSES['gaze'], at=(0, 0, 0), scale=SC)
    rigkit.render(s, DS, sov, at=(0.0, 0, 16.0), scale=DS.scale_of(sov), yaw=180)
    K.person(s, (1.5, 0, 25.0))
    floor(s, 30.0, 2.0, 0.0, 10.0)
    im = dark(s.render((64, 5), size=1500, span=46.0, center=(0.0, 15.0, 8.0)))
    label(im, 'TO SCALE: the Divine One (gaze), looking down on the Dread Sovereign (true form, hovering) - a player',
          f'He: the hood\'s tip ~{HOOD:.0f} blocks up, the halo to ~{H:.0f} (BOSS_SCALE {SC}); the Sovereign ~14 (BOSS_SCALE {DS.BOSS_SCALE} x 1.12); the player 1.8')
    im.save(OUT + '/divine_scale.png')
    s = K.multi_scene(root, rds)                                # (and the three side by side, front on)
    rigkit.render(s, A, A.BOSS_POSES['rest'], at=(-6.0, 0, 0), scale=SC)
    sa = DS.BOSS_POSES['armored']['idle_a']
    rigkit.render(s, DS, sa, at=(16.0, 0, 0), scale=DS.scale_of(sa), yaw=-20)
    K.person(s, (24.0, 0, -1.0))
    floor(s, 34.0, 2.0, 4.0, 0.0)
    N, span = 1600, 58.0
    im = dark(s.render((0, 2), size=N, span=span, center=(4.0, 15.0, 0)))
    k = N / span; im = im.crop((0, int(N / 2 - 19 * k), N, int(N / 2 + 17.5 * k)))
    label(im, 'TO SCALE, side by side: the Divine One (rest) - the Dread Sovereign, armored (~11 blocks) - a player (1.8)').save(OUT + '/divine_scale_lineup.png')

if 'hero' in what:
    # the smite: from behind a player, past the Sovereign (where His beam lands), up at Him
    sov = DS.BOSS_POSES['true']['death_0']
    sm = A.BOSS_POSES['smite']; fx = A.PIVOT['fx']
    hit = min((rigkit.point(A, sm, 'fx', (fx[0], fx[1] - 1.0 - d, fx[2]), scale=SC) for d in range(0, 61)), key=lambda q: abs(q[1] - 6.5))
    for pillar, name, sub in ((False, 'divine_hero.png', 'the beam out of His hand, down through the Sovereign (true form) - a player beside it'),
                              (True, 'divine_pillar.png', 'and the pillar of light (dvn_pillar, BOSS_SCALE x PILLAR_K) erupting where it strikes')):
        s = K.multi_scene(root, rds)
        rigkit.render(s, A, sm, at=(0, 0, 0), scale=SC)
        rigkit.render(s, DS, sov, at=(hit[0], 0, hit[2]), scale=DS.scale_of(sov), yaw=180)
        if pillar: s.display('bm:item/dvn_pillar', pos=(hit[0], 0.0, hit[2]), scale=SC * A.PILLAR_K)
        K.person(s, (hit[0] - 9.0, 0, hit[2] - 2.0))
        floor(s, 48.0, 2.0, 0.0, 14.0)
        im = dark(s.render((-58, 8), size=1400, span=52, center=(-1.0, 14.5, 11.0)))
        label(im, 'THE SMITING', sub).save(OUT + '/' + name)
    s = K.multi_scene(root)
    rigkit.render(s, A, A.BOSS_POSES['reveal'], scale=SC); K.person(s, (-3.0, 0, 13.0))       # (no floor: seen from below it would hide Him)
    im = dark(s.render((14, -24), size=1300, span=46, center=(0, 16.0, 2.0)))
    label(im, 'LOOKING UP', 'a player\'s-eye view of the reveal, from His feet').save(OUT + '/divine_lookup.png')

if 'detail' in what:
    tiles = []
    for f in (None,) + A.FACES:
        pose = dict(A.BOSS_POSES['reveal'], chest=rigkit.I, head=rigkit.I, _off=(0, 0, 0))
        if f: pose['_face'] = f
        tiles.append(tile(pose, (-14, 4), 460, f'head: {f or "default"}', span=10.0, cy=(A.PIVOT['head'][1] + 4.6) * SC / 16, fl=False))
    pose = dict(A.BOSS_POSES['reveal'], chest=rigkit.I, head=rigkit.I, _off=(0, 0, 0), _fx='gather')
    tiles.append(tile(pose, 'front', 460, 'the halo', 'three rings: gold, white and the sunburst', span=19.0, cy=A.PIVOT['halo_a'][1] * SC / 16, fl=False))
    pose = dict(A.BOSS_POSES['raise'], _off=(0, 0, 0))
    hp = rigkit.point(A, pose, 'fx', (7.6, 15.0, -0.6), scale=SC)
    s = scene(pose, fl=False)
    tiles.append(label(dark(s.render((-30, 10), size=460, span=9.0, center=hp)), 'fx: gather', 'light in the raised hand'))
    sheet(tiles, OUT + '/divine_detail.png', cols=3, title='The Divine One - the face of light, the halo, the hand')
    s = scene(dict(A.BOSS_POSES['reveal'], _off=(0, 0, 0)), fl=False)
    w = label(dark(s.render((150, 6), size=900, span=30, center=(-9.0, 18.0, 4.0))), 'the great wings, from behind', 'feathered light: gold leading edge, coverts, white flights with burning tips')
    w.save(OUT + '/divine_wings.png')

if 'anim' in what:                                         # (the cinematic, as the game moves the displays: each eased from key to key)
    seq = A.SEQUENCE[1:] + A.SEQUENCE[:1]
    frames, step = [], 5
    for i, (name, ticks) in enumerate(seq):
        a, b = A.BOSS_POSES[seq[i - 1][0]], A.BOSS_POSES[name]
        xa, xb = rigkit.solve(A.PIVOT, A.PARENT, a), rigkit.solve(A.PIVOT, A.PARENT, b)
        for k in range(0, max(ticks, 10), step):
            t = k / max(ticks, 10); t = t * t * (3 - 2 * t)
            pz = a if t < 0.5 else b
            s = K.multi_scene(root); rigkit.draw(s, A, rigkit.blend(xa, xb, t), pz, scale=SC); floor(s)
            frames.append(label(dark(s.render((-24, 6), size=420, span=H * 1.25, center=(0, H * 0.5, 0))), name))
    K.gif(frames, OUT + '/divine_cinematic.gif', step=step)

if 'clip' in what:
    sys.argv = sys.argv[:1]
    import numpy as np
    def sat(a, b):
        ca, aa, ha = a; cb, ab, hb = b
        A_, B_ = np.array(aa), np.array(ab); t = np.array(cb) - np.array(ca); best = 1e9
        for L in list(A_) + list(B_) + [np.cross(u, v) for u in A_ for v in B_]:
            n = np.linalg.norm(L)
            if n < 1e-6: continue
            L = L / n
            o = sum(ha[i] * abs(A_[i] @ L) for i in range(3)) + sum(hb[i] * abs(B_[i] @ L) for i in range(3)) - abs(t @ L)
            if o <= 0: return 0.0
            best = min(best, o)
        return best
    LIMBS = {'armr', 'forer', 'handr', 'arml', 'forel', 'handl', 'fx'} | set(A.WINGS) | set(A.HALOS)
    def aabb(bl):
        out = []
        for c, ax, h in bl:
            e = np.array([sum(abs(ax[i][k]) * h[i] for i in range(3)) for k in range(3)])
            out.append((np.array(c) - e, np.array(c) + e))
        return out
    rep = []
    for n, p in A.BOSS_POSES.items():
        wb = A.world_boxes(p); bb = {k: aabb(v) for k, v in wb.items()}; worst = []
        parts = list(wb)
        for i, a in enumerate(parts):
            for b in parts[i + 1:]:
                if A.PARENT.get(a) == b or A.PARENT.get(b) == a: continue
                if a not in LIMBS and b not in LIMBS: continue
                if {a, b} <= set(A.HALOS) or {a, b} <= set(A.WINGS): continue
                if 'fx' in (a, b) and {'handr', 'forer'} & {a, b}: continue
                d = 0.0
                for ea, (la, ha) in zip(wb[a], bb[a]):
                    for eb, (lb, hb) in zip(wb[b], bb[b]):
                        if (la > hb).any() or (lb > ha).any(): continue
                        d = max(d, sat(ea, eb))
                if d > 0.5: worst.append((round(d, 2), a, b))
        rep.append(f'{n:9s} ' + (', '.join(f'{a}x{b} {d}' for d, a, b in sorted(worst, reverse=True)[:8]) or 'clean'))
    open(OUT + '/divine_clip.txt', 'w').write('\n'.join(rep) + '\n')
    print('\n'.join(rep))
print(OUT)

"""The Dread Sovereign preview sheets (rigkit).   python3 tools/preview/dread_sovereign.py [forms,turn,poses,faces,follower,lineup,hero,clip]
forms: the three phases and the follower side by side with a player; turn: a turnaround of each form; poses: the boss poses, a
sheet per form; faces: the helm's slit and the great eye; follower: its poses; lineup: the follower beside a player and Bender;
hero: a low-angle shot of the true form; clip: a report of parts cutting into each other, pose by pose (boxes overlapping by
more than a design unit's fraction, joints with their parents excepted)."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import draftkit as K, rigkit
import dread_sovereign_art as A
OUT = K.OUT; os.makedirs(OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['forms', 'turn', 'poses', 'faces', 'follower', 'lineup', 'hero', 'clip']
root = K.pack(A, OUT + '/rp_ds')
FLOOR, FLOOR2 = '#2a1418', '#3a1c20'


def floor(s, r=12.0, step=1.0):
    """a nether-brick floor (the renderer's own grid only reaches 3 blocks)"""
    n = int(r / step)
    for i in range(-n, n):
        for j in range(-n, n):
            s.solid((i * step, -0.25, j * step), ((i + 1) * step, 0.0, (j + 1) * step), FLOOR if (i + j) % 2 else FLOOR2)


def scene(pose, at=(0, 0, 0), yaw=0.0, person=None, fl=True, r=12.0):
    s = K.multi_scene(root)
    rigkit.render(s, A, pose, at=at, scale=A.scale_of(pose), yaw=yaw)
    if person is not None: K.person(s, person)
    if fl: floor(s, r)
    return s


def boss_tile(pose, view=(-30, 10), size=420, label='', sub=None, span=None, cy=None, person=(-4.2, 0, -2.0)):
    sc = A.scale_of(pose); H = (50 + (A.HOVER if pose['_form'] == 'true' else 0)) * sc / 16
    s = scene(pose, person=person)
    k = 1.85 if pose['_form'] == 'true' else 1.45
    return K.label(s.render(view, size=size, span=span or H * k, center=(0, cy if cy is not None else H * (0.52 if k > 1.5 else 0.47), 0)), label, sub)


if 'forms' in what:
    s = K.multi_scene(root)
    xs = {'armored': -30.0, 'broken': -8.0, 'true': 19.0}
    for f, x in xs.items():
        p = A.BOSS_POSES[f]['idle_a']; rigkit.render(s, A, p, at=(x, 0, 0), scale=A.scale_of(p))
        K.person(s, (x - 4.0, 0, -4.0))
    pf = A.POSES['idle_a']; rigkit.render(s, A, pf, at=(38.0, 0, -1.0), scale=A.scale_of(pf)); K.person(s, (39.6, 0, -1.0))
    for i in range(-44, 46, 2):
        for j in range(-6, 6, 2): s.solid((i, -0.25, j), (i + 2, 0.0, j + 2), FLOOR if (i // 2 + j // 2) % 2 else FLOOR2)
    N, span = 2000, 88.0; im = s.render((0, 4), size=N, span=span, center=(0.0, 9.0, 0))
    k = N / span; im = im.crop((0, int(N / 2 - 16 * k), N, int(N / 2 + 10.5 * k)))
    K.sheet([K.label(im, 'ARMORED (phase 1) - BROKEN (phase 2) - TRUE (phase 3, hovering) - BOUND (the follower)',
                     'a player (1.8 blocks) beside each; armored ~11 blocks to the crown, true ~14 (hovering), bound ~2.3')],
            OUT + '/ds_forms.png', cols=1, title='The Dread Sovereign - its three phases and its bound form, to scale')

if 'turn' in what:
    for f in ('armored', 'broken', 'true'):
        p = A.BOSS_POSES[f]['idle_a']
        K.sheet([boss_tile(p, v, 400, l, person=None) for v, l in (('front', 'front'), ((-35, 12), '3/4'), ('side', 'side'), ('back', 'back'))],
                OUT + f'/ds_turn_{f}.png', cols=4, title=f'The Dread Sovereign - {f} - turnaround')
    p = A.POSES['idle_a']; tiles = []
    for v, l in (('front', 'front'), ((-35, 12), '3/4'), ('side', 'side'), ('back', 'back')):
        s = scene(p, fl=False); tiles.append(K.label(s.render(v, size=400, span=3.2, center=(0, 1.3, 0)), l))
    K.sheet(tiles, OUT + '/ds_turn_bound.png', cols=4, title='The Dread Sovereign - bound (the follower) - turnaround')

if 'poses' in what:
    for f in ('armored', 'broken', 'true'):
        tiles = [boss_tile(A.BOSS_POSES[f][n], label=n, size=360) for n in A.BOSS_DRAFT[f]]
        K.sheet(tiles, OUT + f'/ds_poses_{f}.png', cols=6, title=f'The Dread Sovereign - {f} - boss poses')

if 'faces' in what:
    tiles = []
    for f in ('armored', 'broken', 'bound'):
        for fc in (None,) + A.FACES:
            pose = dict(A.POSES['idle_a'], _form=f, chest=rigkit.I, head=rigkit.I)
            if fc: pose['_face'] = fc
            s = K.multi_scene(root); rigkit.render(s, A, pose, scale=1.0)
            tiles.append(K.label(s.render((-12, 4), size=240, span=1.5, center=(0, 2.55, -0.2)), f, fc or 'default'))
    for fc in (None,) + A.EYE_FACES:
        pose = dict(A.BOSS_POSES['true']['idle_a'], chest=rigkit.I, head=rigkit.I, _off=(0, 0, 0))
        if fc: pose['_face'] = fc
        s = K.multi_scene(root); rigkit.render(s, A, pose, scale=1.0)
        tiles.append(K.label(s.render((-12, 4), size=240, span=1.6, center=(0, 2.6, -0.2)), 'true', fc or 'default (open)'))
    K.sheet(tiles, OUT + '/ds_faces.png', cols=5, title='The Dread Sovereign - faces (the helm\'s slit; the great eye)')

if 'follower' in what:
    tiles = []
    for n in A.DRAFT:
        s = scene(A.POSES[n], fl=False)
        tiles.append(K.label(s.render((-30, 10), size=300, span=3.4, center=(0, 1.3, 0)), n))
    K.sheet(tiles, OUT + '/ds_follower_poses.png', cols=6, title='The Dread Sovereign - bound (follower) poses')

if 'lineup' in what:
    import bender_art as BA
    rb = K.pack(BA, OUT + '/rp_bd')
    s = K.multi_scene(root, rb)
    rigkit.render(s, A, A.POSES['idle_a'], at=(0.0, 0, 0), scale=A.RIG_SCALE)
    rigkit.render(s, BA, BA.POSES['idle_a'], at=(1.9, 0, 0.2), scale=BA.RIG_SCALE, yaw=-20)
    K.person(s, (-1.7, 0, 0.3))
    K.sheet([K.label(s.render(v, size=620, span=4.4, center=(0, 1.3, 0)), 'size', 'a player, the bound Sovereign, Bender') for v in ((-12, 8), (-40, 14))],
            OUT + '/ds_follower_lineup.png', cols=2, title='The Dread Sovereign (bound) - next to a player and Bender')

if 'hero' in what:
    p = dict(A.BOSS_POSES['true']['roar'])
    s = scene(p, person=(-3.0, 0, -7.0), fl=False)
    im = s.render((-24, -9), size=1100, span=21, center=(0, 8.0, 0))       # (no floor: seen from below it would hide the player)
    K.sheet([K.label(im, 'THE TRUE SOVEREIGN', 'low angle: the roar, a player at its feet')], OUT + '/ds_hero.png', cols=1, title='The Dread Sovereign - hero shot')

if 'clip' in what:
    import numpy as np
    def sat(a, b):
        """penetration depth of two oriented boxes (0 if apart)"""
        ca, aa, ha = a; cb, ab, hb = b
        A_, B_ = np.array(aa), np.array(ab); t = np.array(cb) - np.array(ca); best = 1e9
        axes = list(A_) + list(B_) + [np.cross(u, v) for u in A_ for v in B_]
        for L in axes:
            n = np.linalg.norm(L)
            if n < 1e-6: continue
            L = L / n
            ra = sum(ha[i] * abs(A_[i] @ L) for i in range(3)); rb = sum(hb[i] * abs(B_[i] @ L) for i in range(3))
            o = ra + rb - abs(t @ L)
            if o <= 0: return 0.0
            best = min(best, o)
        return best
    def aabb(bl):
        out = []
        for c, ax, h in bl:
            e = [sum(abs(ax[i][k]) * h[i] for i in range(3)) for k in range(3)]
            out.append((np.array(c) - e, np.array(c) + e))
        return out
    LIMBS = {'armr', 'forer', 'arml', 'forel', 'weapon', 'legr', 'shinr', 'legl', 'shinl'} | set(A.WINGS)
    SKIP = {('legr', 'legl'), ('w1r', 'w2r'), ('w2r', 'w3r'), ('w1r', 'w3r'), ('w1l', 'w2l'), ('w2l', 'w3l'), ('w1l', 'w3l')}
    rep = []
    allp = [('boss/' + f, n, p) for f in A.BOSS_POSES for n, p in A.BOSS_POSES[f].items()] + [('follower', n, p) for n, p in A.POSES.items()]
    for grp, n, p in allp:
        wb = A.world_boxes(p); bb = {k: aabb(v) for k, v in wb.items()}; worst = []
        parts = list(wb)
        for i, a in enumerate(parts):
            for b in parts[i + 1:]:
                if A.PARENT.get(a) == b or A.PARENT.get(b) == a or (a, b) in SKIP or (b, a) in SKIP: continue
                if a not in LIMBS and b not in LIMBS: continue
                if {a, b} <= set(A.WINGS): continue                    # (wing against wing: only ever at their roots, behind its back)
                if p.get('_form') == 'true' and {a, b} <= {'body', 'chest', 'legr', 'legl', 'shinr', 'shinl'}: continue   # (smoke into smoke)
                d = 0.0
                for ea, (la, ha_) in zip(wb[a], bb[a]):
                    for eb, (lb, hb_) in zip(wb[b], bb[b]):
                        if (la > hb_).any() or (lb > ha_).any(): continue
                        d = max(d, sat(ea, eb))
                if d > 0.35: worst.append((round(d, 2), a, b))
        if worst: rep.append(f'{grp:13s} {n:12s} ' + ', '.join(f'{a}x{b} {d}' for d, a, b in sorted(worst, reverse=True)[:6]))
    open(OUT + '/ds_clip.txt', 'w').write('\n'.join(rep) + '\n')
    print('\n'.join(rep) or 'no clipping')
print(OUT)

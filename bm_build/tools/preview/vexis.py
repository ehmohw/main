"""Admiral Vexis preview sheets (rigkit).   python3 tools/preview/vexis.py [forms,hero,turn,scale,poses,entrance,faces,follower,lineup,
companions,compare,clip]
forms: the four forms to scale, side by side with a player; hero: each form from the front 3/4, a sheet; turn: a turnaround of
each form; scale: the warframe and the hive-link beside a player and the Dread Sovereign (armored and true); poses: every boss
pose, a sheet per form; entrance: the coming (dormant -> roar); faces: the visor and the eyes; follower: the unlinked follower's
poses; lineup: the follower beside a player and Bender; companions: the three boss forms at companion size beside a player, the
unlinked follower and Bender, and each one's sit_a / happy; compare: a Vorn trooper and the warlord (the shipped vorn3d models,
from out_p2) beside Vexis - heads, figures, the warframe's pilot; clip: a report of parts cutting into each other, pose by pose.
Sheets go to $VX_OUT (default previews/v299_armada/vexis); the throwaway packs to draftkit's $BM_PREVIEW_DIR."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import draftkit as K, rigkit
import vexis_art as A
TMP = K.OUT; os.makedirs(TMP, exist_ok=True)
OUT = os.environ.get('VX_OUT', os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), 'previews', 'v299_armada', 'vexis'))
os.makedirs(OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['forms', 'hero', 'turn', 'scale', 'poses', 'entrance', 'faces', 'follower', 'lineup', 'companions',
                                                          'compare', 'clip']
root = K.pack(A, TMP + '/rp_vx')
FLOOR, FLOOR2 = '#23262e', '#30343e'                     # (the Hive-Throne's deck)


def floor(s, r=12.0, step=1.0, x0=0.0):
    n = int(r / step)
    for i in range(-n, n):
        for j in range(-n, n):
            s.solid((x0 + i * step, -0.25, j * step), (x0 + (i + 1) * step, 0.0, (j + 1) * step), FLOOR if (i + j) % 2 else FLOOR2)


def scene(pose, at=(0, 0, 0), yaw=0.0, person=None, fl=True, r=10.0):
    s = K.multi_scene(root)
    rigkit.render(s, A, pose, at=at, scale=A.scale_of(pose), yaw=yaw)
    if person is not None: K.person(s, person)
    if fl: floor(s, r)
    return s


def tall(pose):
    """its height to frame it by (blocks)"""
    return {'warframe': 54, 'hivelink': 50, 'starfire': 52}.get(pose['_form'], 40) * A.scale_of(pose) / 16


def boss_tile(pose, view=(-30, 10), size=380, label='', sub=None, person=(-3.4, 0, -2.6), span=None, cy=None):
    H = tall(pose); s = scene(pose, person=person)
    return K.label(s.render(view, size=size, span=span or H * 1.45, center=(0, cy if cy is not None else H * 0.47, 0)), label, sub)


FORM_T = {'warframe': 'THE WARFRAME (phase 1)', 'hivelink': 'THE HIVE-LINK (phase 2)', 'starfire': 'STARFIRE (phase 3)', 'unlinked': 'UNLINKED (the follower)'}

if 'forms' in what:
    s = K.multi_scene(root)
    xs = {'warframe': -20.0, 'hivelink': -1.0, 'starfire': 15.0}
    for f, x in xs.items():
        p = A.BOSS_POSES[f]['idle_a']; rigkit.render(s, A, p, at=(x, 0, 0), scale=A.scale_of(p))
        K.person(s, (x - 4.5, 0, -4.0))
    pf = A.POSES['idle_a']; rigkit.render(s, A, pf, at=(28.0, 0, -1.0), scale=A.scale_of(pf)); K.person(s, (29.4, 0, -1.0))
    for i in range(-36, 40, 2):
        for j in range(-6, 6, 2): s.solid((i, -0.25, j), (i + 2, 0.0, j + 2), FLOOR if (i // 2 + j // 2) % 2 else FLOOR2)
    N, span = 2000, 66.0; im = s.render((0, 4), size=N, span=span, center=(3.0, 7.0, 0))
    k = N / span; im = im.crop((0, int(N / 2 - 13 * k), N, int(N / 2 + 8.5 * k)))
    K.sheet([K.label(im, 'WARFRAME (phase 1) - HIVE-LINK (phase 2, hovering) - STARFIRE (phase 3) - UNLINKED (the follower)',
                     'a player (1.8 blocks) beside each; the warframe ~12 blocks to its head (14 to its masts), the hive-link ~8.5 to its skull, starfire ~10, unlinked ~2.3')],
            OUT + '/vx_forms.png', cols=1, title='Admiral Vexis - its three phases and the follower, to scale')

if 'hero' in what:
    tiles = []
    for f in ('warframe', 'hivelink', 'starfire'):
        p = A.BOSS_POSES[f]['idle_a']; tiles.append(boss_tile(p, (-28, 8), 640, FORM_T[f], 'front 3/4, a player for scale', person=(-3.8, 0, -3.4)))
    s = scene(A.POSES['idle_a'], fl=True, r=3, person=(1.25, 0, 0.9))
    tiles.append(K.label(s.render((-28, 8), size=640, span=3.4, center=(0.3, 1.2, 0)), FORM_T['unlinked'], 'front 3/4, a player for scale'))
    K.sheet(tiles, OUT + '/vx_hero.png', cols=4, title='Admiral Vexis - each form, front 3/4')

if 'turn' in what:
    for f in ('warframe', 'hivelink', 'starfire'):
        p = A.BOSS_POSES[f]['idle_a']
        K.sheet([boss_tile(p, v, 420, l, person=None) for v, l in (('front', 'front'), ((-35, 12), '3/4'), ('side', 'side'), ((145, 12), 'back 3/4'), ('back', 'back'))],
                OUT + f'/vx_turn_{f}.png', cols=5, title=f'Admiral Vexis - {f} - turnaround')
    p = A.POSES['idle_a']; tiles = []
    for v, l in (('front', 'front'), ((-35, 12), '3/4'), ('side', 'side'), ((145, 12), 'back 3/4'), ('back', 'back')):
        s = scene(p, fl=False); tiles.append(K.label(s.render(v, size=420, span=2.9, center=(0, 1.2, 0)), l))
    K.sheet(tiles, OUT + '/vx_turn_unlinked.png', cols=5, title='Admiral Vexis - unlinked (the follower) - turnaround')

if 'scale' in what:
    import dread_sovereign_art as DS
    rds = K.pack(DS, TMP + '/rp_ds')
    s = K.multi_scene(root, rds)
    for f, x in (('warframe', -14.0), ('hivelink', 3.0)):
        p = A.BOSS_POSES[f]['idle_a']; rigkit.render(s, A, p, at=(x, 0, 0), scale=A.scale_of(p))
    for f, x in (('armored', 22.0), ('true', 40.0)):
        p = DS.BOSS_POSES[f]['idle_a']; rigkit.render(s, DS, p, at=(x, 0, 0), scale=DS.scale_of(p))
    for x in (-19.5, -0.5, 16.5, 33.5): K.person(s, (x, 0, -3.0))
    for i in range(-26, 52, 2):
        for j in range(-6, 6, 2): s.solid((i, -0.25, j), (i + 2, 0.0, j + 2), FLOOR if (i // 2 + j // 2) % 2 else FLOOR2)
    N, span = 2000, 80.0; im = s.render((0, 4), size=N, span=span, center=(13.0, 8.0, 0))
    k = N / span; im = im.crop((0, int(N / 2 - 16 * k), N, int(N / 2 + 9.5 * k)))
    K.sheet([K.label(im, 'VEXIS: WARFRAME - HIVE-LINK          THE DREAD SOVEREIGN: ARMORED - TRUE',
                     'to scale, a player (1.8 blocks) beside each; the Sovereign is the hardest boss - Vexis stands a little under it in every phase')],
            OUT + '/vx_scale.png', cols=1, title='Admiral Vexis beside the Dread Sovereign')

if 'poses' in what:
    for f in ('warframe', 'hivelink', 'starfire'):
        tiles = [boss_tile(A.BOSS_POSES[f][n], label=n, size=340) for n in A.BOSS_POSES[f]]
        K.sheet(tiles, OUT + f'/vx_poses_{f}.png', cols=6, title=f'Admiral Vexis - {f} - every boss pose')

if 'entrance' in what:
    K.sheet([boss_tile(A.BOSS_POSES['warframe'][n], label=f'{i + 1}. {n}', sub=f'power {A.BOSS_POSES["warframe"][n].get("_power", 3)}', size=360)
             for i, n in enumerate(A.ENTRANCE)] +
            [boss_tile(A.BOSS_POSES['hivelink'][n], label=f'phase 2: {n}', size=360) for n in ('rise', 'roar')] +
            [boss_tile(A.BOSS_POSES['starfire'][n], label=f'the fall: {n}', size=360) for n in ('death_0', 'death_1', 'death_2')],
            OUT + '/vx_entrance.png', cols=6, title='Admiral Vexis - the coming (warframe, lighting up section by section), phase 2\'s rise, the fall')

if 'faces' in what:
    tiles = []
    for fc in (None,) + A.FACES[:4]:
        pose = dict(A.BOSS_POSES['warframe']['idle_a'], chest=rigkit.I, head=rigkit.I)
        if fc: pose['_face'] = fc
        s = K.multi_scene(root); rigkit.render(s, A, pose, scale=1.0)
        tiles.append(K.label(s.render((-14, 4), size=240, span=1.3, center=(0, 2.78, -0.3)), 'warframe', fc or 'default'))
    tiles.append(K.label(K.multi_scene(root).render((-14, 4), size=240, span=1.3), ''))
    for f in ('hivelink', 'starfire', 'unlinked'):
        for fc in (None,) + A.FACES:
            pose = A.fit(dict(A.BOSS_POSES[f]['idle_a'] if f != 'unlinked' else A.POSES['idle_a'], chest=rigkit.I, head=rigkit.I, _off=(0, 0, 0)))
            if fc: pose['_face'] = fc
            s = K.multi_scene(root); rigkit.render(s, A, pose, scale=1.0)
            tiles.append(K.label(s.render((-14, 4), size=240, span=1.2, center=(0, 1.95, -0.2)), f, fc or 'default'))
    K.sheet(tiles, OUT + '/vx_faces.png', cols=6, title='Admiral Vexis - faces (the visor bar; the eyes: the hive, the star, the unlinked)')

if 'follower' in what:
    tiles = []
    for n in A.DRAFT:
        s = scene(A.POSES[n], fl=True, r=2)
        tiles.append(K.label(s.render((-30, 10), size=300, span=3.0, center=(0, 1.15, 0)), n))
    K.sheet(tiles, OUT + '/vx_follower_poses.png', cols=6, title='Admiral Vexis - unlinked (the follower) - poses')

if 'lineup' in what:
    import bender_art as BA
    rb = K.pack(BA, TMP + '/rp_bd')
    s = K.multi_scene(root, rb)
    rigkit.render(s, A, A.POSES['idle_a'], at=(0.0, 0, 0), scale=A.RIG_SCALE)
    rigkit.render(s, BA, BA.POSES['idle_a'], at=(1.9, 0, 0.2), scale=BA.RIG_SCALE, yaw=-20)
    K.person(s, (-1.7, 0, 0.3))
    K.sheet([K.label(s.render(v, size=620, span=4.4, center=(0, 1.3, 0)), 'size', 'a player, Vexis (unlinked), Bender') for v in ((-12, 8), (-40, 14))],
            OUT + '/vx_follower_lineup.png', cols=2, title='Admiral Vexis (unlinked) - next to a player and Bender')

if 'companions' in what:                                    # (every boss form as a follower, at its companion size)
    import bender_art as BA
    rb = K.pack(BA, TMP + '/rp_bd')
    s = K.multi_scene(root, rb)
    xs = {'warframe': -4.2, 'hivelink': -0.6, 'starfire': 2.8}
    for f, x in xs.items():
        rigkit.render(s, A, A.BOSS_POSES[f]['idle_a'], at=(x, 0, 0), scale=A.COMPANION_SCALE[f])
    rigkit.render(s, A, A.POSES['idle_a'], at=(5.4, 0, 0), scale=A.RIG_SCALE)
    rigkit.render(s, BA, BA.POSES['idle_a'], at=(7.4, 0, 0.2), scale=BA.RIG_SCALE, yaw=-20)
    K.person(s, (-6.8, 0, 0.0))
    for i in range(-9, 10):
        for j in range(-3, 3): s.solid((i, -0.25, j), (i + 1, 0.0, j + 1), FLOOR if (i + j) % 2 else FLOOR2)
    top = [K.label(s.render((-10, 6), size=1600, span=16.5, center=(0.6, 2.0, 0)).crop((0, 540, 1600, 1090)),
                   'COMPANIONS: a player - the warframe (~3.5) - the hive-link (~3) - starfire (~3.2) - unlinked (~2.3) - Bender',
                   'each boss form at COMPANION_SCALE, driven by its own BOSS_POSES (idle_a); the antennae and masts stand above those heights')]
    tiles = []
    for f in ('warframe', 'hivelink', 'starfire'):
        for n in ('idle_a', 'sit_a', 'sit_b', 'happy', 'hurt'):
            s2 = K.multi_scene(root); rigkit.render(s2, A, A.BOSS_POSES[f][n], scale=A.COMPANION_SCALE[f]); K.person(s2, (-1.6, 0, -0.6)); floor(s2, 3, 0.5)
            tiles.append(K.label(s2.render((-30, 10), size=320, span=4.6, center=(0, 1.9, 0)), f'{f}: {n}', 'companion size'))
    from PIL import Image
    a = K.sheet(top, TMP + '/_c1.png', cols=1); b = K.sheet(tiles, TMP + '/_c2.png', cols=5)
    A1, B1 = Image.open(a), Image.open(b); W = max(A1.width, B1.width)
    sh = Image.new('RGB', (W, A1.height + B1.height + 40), 'white'); sh.paste(A1, (0, 40)); sh.paste(B1, (0, 40 + A1.height))
    from PIL import ImageDraw, ImageFont
    try: fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
    except OSError: fnt = None
    ImageDraw.Draw(sh).text((12, 8), 'Admiral Vexis - every boss form as a companion follower (sit_a / sit_b / happy / hurt)', fill=(20, 20, 20), font=fnt)
    sh.save(OUT + '/vx_companions.png')

if 'compare' in what:                                       # (is it a Vorn? beside the shipped troopers)
    real = K.REAL_RP
    def trooper(s, at, k=1.0, warlord=False, yaw=0.0):
        s.display(f'bm:item/vorn3d{"_warlord" if warlord else ""}', pos=at, scale=k, yaw=yaw)
    tiles = []
    s = K.multi_scene(root, real)                           # (figures: a trooper, the warlord, Vexis unlinked, the hive-link as a companion)
    trooper(s, (-2.6, 0, 0), 1.5); trooper(s, (-1.0, 0, 0), 1.5, True)
    rigkit.render(s, A, A.POSES['idle_a'], at=(0.9, 0, 0), scale=A.RIG_SCALE)
    rigkit.render(s, A, A.BOSS_POSES['hivelink']['idle_a'], at=(3.4, 0, 0), scale=A.COMPANION_SCALE['hivelink'])
    for v, l in (('front', 'front'), ((-30, 10), '3/4')):
        tiles.append(K.label(s.render(v, size=720, span=7.6, center=(0.4, 1.9, 0)), f'a Vorn trooper, the warlord, Vexis unlinked, Vexis hive-link ({l})',
                             'the troopers: the shipped vorn3d / vorn3d_warlord models (x1.5)'))
    s = K.multi_scene(root, real)                           # (heads, face to face, at one size)
    trooper(s, (-3.7, 0, 0), 2.0)
    for f, x in (('unlinked', -1.2), ('hivelink', 1.4), ('starfire', 4.1)):
        p = A.fit(dict(A.POSES['idle_a'] if f == 'unlinked' else A.BOSS_POSES[f]['idle_a'], chest=rigkit.I, head=rigkit.I, _off=(0, 0, 0)))
        rigkit.render(s, A, p, at=(x, -1.62, 0), scale=2.0)
    tiles.append(K.label(s.render((-10, 4), size=720, span=9.4, center=(0.2, 2.4, 0)), 'heads: a trooper - Vexis unlinked - hive-link - starfire',
                         'the square head, the dark muzzle and green nose, the square green eyes, the dark ears, the two froglight antennae'))
    s = K.multi_scene(root, real)                           # (the warframe's cockpit: a Vorn at the helm)
    rigkit.render(s, A, A.BOSS_POSES['warframe']['idle_a'], scale=A.BOSS_SCALE)
    tiles.append(K.label(s.render((-16, 4), size=720, span=8.0, center=(0.8, 9.6, 0)), 'the warframe: its pilot, and its head',
                         'a Vorn at the helm (black armour, the green stripe, the square head, the two antennae); the Vorn pair of antennae on its head'))
    K.sheet(tiles, OUT + '/vx_vorn_compare.png', cols=2, title='Admiral Vexis beside the Vorn - the family resemblance')

if 'clip' in what:
    import numpy as np
    def sat(a, b):
        ca, aa, ha = a; cb, ab, hb = b
        A_, B_ = np.array(aa), np.array(ab); t = np.array(cb) - np.array(ca); best = 1e9
        for L in list(A_) + list(B_) + [np.cross(u, v) for u in A_ for v in B_]:
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
    LIMBS = {'armr', 'forer', 'arml', 'forel', 'legr', 'shinr', 'footr', 'legl', 'shinl', 'footl', 'podr', 'podl'}
    SKIP = {('legr', 'legl'), ('footr', 'legr'), ('footl', 'legl')}
    rep = []
    allp = [('boss/' + f, n, p) for f in A.BOSS_POSES for n, p in A.BOSS_POSES[f].items()] + [('follower', n, p) for n, p in A.POSES.items()]
    for grp, n, p in allp:
        wb = A.world_boxes(p, [q for q in A.PARTS if q not in A.RINGS + A.FXP]); bb = {k: aabb(v) for k, v in wb.items()}; worst = []
        parts = list(wb)
        for i, a in enumerate(parts):
            for b in parts[i + 1:]:
                if A.PARENT.get(a) == b or A.PARENT.get(b) == a or (a, b) in SKIP or (b, a) in SKIP: continue
                if a not in LIMBS and b not in LIMBS: continue
                d = 0.0
                for ea, (la, ha_) in zip(wb[a], bb[a]):
                    for eb, (lb, hb_) in zip(wb[b], bb[b]):
                        if (la > hb_).any() or (lb > ha_).any(): continue
                        d = max(d, sat(ea, eb))
                if d > 0.35: worst.append((round(d, 2), a, b))
        if worst: rep.append(f'{grp:15s} {n:10s} ' + ', '.join(f'{a}x{b} {d}' for d, a, b in sorted(worst, reverse=True)[:6]))
    open(TMP + '/vx_clip.txt', 'w').write('\n'.join(rep) + '\n')
    print('\n'.join(rep) or 'no clipping')
print(OUT)

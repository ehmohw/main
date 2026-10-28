"""The Ink Blot preview sheets (rigkit).  python3 tools/preview/ink_blot.py [views,shapes,poses,faces,lineup]"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import draftkit as K, ink_blot_art as A, capshun_art as CA, rigkit
OUT = K.OUT; os.makedirs(OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['views', 'shapes', 'poses', 'faces', 'lineup']
root = K.pack(A, OUT + '/rp_ib')


def tile(pose, view=(-30, 12), span=2.0, center=(0, 0.68, 0), size=340, label='', sub=None):
    s = K.multi_scene(root); rigkit.render(s, A, pose, scale=A.RIG_SCALE)
    return K.label(s.render(view, size=size, span=span, center=center), label, sub)


if 'views' in what:
    I = A.POSES['idle_a']
    K.sheet([tile(I, v, label=l) for v, l in (('front', 'front'), ((-35, 18), '3/4'), ('side', 'side (flat!)'), ('back', 'back'))],
            OUT + '/ink_blot_turnaround.png', cols=4, title='The Ink Blot - turnaround')
if 'shapes' in what:
    tiles = []
    for sh in A.SHAPES:
        pose = dict(A.POSES['idle_a'], _shape=sh)
        if sh == 'puddle': pose = A.POSES['sit_a']
        tiles.append(tile(pose, 'front', label=sh))
        tiles.append(tile(pose, (-40, 22), label=sh, sub='3/4'))
    K.sheet(tiles, OUT + '/ink_blot_shapes.png', cols=4, title='The Ink Blot - shapes (_shape)')
if 'poses' in what:
    K.sheet([tile(A.POSES[n], label=n) for n in A.DRAFT], OUT + '/ink_blot_poses.png', cols=5, title='The Ink Blot - poses')
    K.sheet([tile(A.POSES[f'swim_{i}'], label=f'swim_{i}', center=(0, 0.4, 0)) for i in range(A.SWIM_FRAMES)] +
            [tile(A.POSES[f'{w}_{i}'], label=f'{w}_{i}') for w in ('walk', 'run') for i in range(4)],
            OUT + '/ink_blot_cycles.png', cols=4, title='The Ink Blot - swim, walk, run')
if 'faces' in what:
    tiles = []
    for f in (None,) + A.FACES:
        pose = {k: v for k, v in dict(A.POSES['idle_a'], _face=f, body=None).items() if v is not None}
        s = K.multi_scene(root); rigkit.render(s, A, pose, scale=A.RIG_SCALE)
        tiles.append(K.label(s.render('front', size=260, span=0.9, center=(0, 0.52, 0)), f or 'default'))
    K.sheet(tiles, OUT + '/ink_blot_faces.png', cols=9, title='The Ink Blot - faces')
if 'figurine' in what or 'lineup' in what:
    # (the display case's figurine: phase134 solves idle_a at RIG_SCALE - every part must sit within the body's height)
    import phase134
    for mid, tr, L, R, sc in phase134._rigkit(A, A.POSES['idle_a'], A.RIG_SCALE):
        print('figurine', mid, 'translation (blocks)', tuple(round(v, 3) for v in tr))
        assert -0.8 <= tr[0] <= 0.8 and 0.0 <= tr[1] <= 1.5 and -0.8 <= tr[2] <= 0.8, (mid, tr)
if 'lineup' in what:
    rc = K.pack(CA, OUT + '/rp_mz')
    s = K.multi_scene(root, rc, K.REAL_RP)
    rigkit.render(s, A, A.POSES['idle_a'], at=(0.0, 0, 0), scale=A.RIG_SCALE)
    rigkit.render(s, CA, CA.POSES['idle_a'], at=(1.1, 0, 0.2), scale=CA.RIG_SCALE)
    K.person(s, (-1.2, 0, 0.3))
    K.sheet([K.label(s.render((-12, 8), size=620, span=3.4, center=(0, 1.0, 0)), 'size', 'a player, the Ink Blot, Mr. Capshun')],
            OUT + '/ink_blot_lineup.png', cols=1, title='The Ink Blot - next to Mr. Capshun')

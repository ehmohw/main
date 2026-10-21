"""Ashur preview sheets (the draft for approval).  python3 tools/preview/ashur.py [views,poses,faces,lineup]"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import draftkit as K, ashur_art as A, phase57_art as EM, phase66_art as CE
OUT = K.OUT; os.makedirs(OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['views', 'poses', 'faces', 'lineup']
root = K.pack(A, OUT + '/rp_as')
DESC = {'idle': 'idle - a flame in her palm', 'walk_a': 'walk (barefoot)', 'run_a': 'run - both hands burning', 'jump': 'the leap (from the sketch)',
        'cast_back': 'fireball: wind-up', 'cast': 'fireball: thrown', 'blast': 'flamethrower', 'erupt': 'ERUPTION (her great blow)',
        'sit_a': 'sit', 'wave': 'wave', 'hurt': 'hurt', 'tired': 'tired / fainting'}


def tile(pose, view=(-30, 12), span=2.2, center=(0, 0.9, 0), size=340, label='', sub=None):
    s = K.multi_scene(root, K.REAL_RP); K.put_flat(s, A, pose)
    return K.label(s.render(view, size=size, span=span, center=center), label, sub)


if 'views' in what:
    I = A.POSES['idle']
    K.sheet([tile(I, v, label=l) for v, l in (('front', 'front'), ('side', 'side'), ('back', 'back'), ((-35, 18), '3/4'))],
            OUT + '/ashur_turnaround.png', cols=4, title='Ashur - turnaround')
if 'poses' in what:
    K.sheet([tile(A.POSES[n], label=n, sub=DESC.get(n)) for n in A.DRAFT], OUT + '/ashur_poses.png', cols=4, title='Ashur - poses')
if 'faces' in what:
    tiles = []
    for f in (None,) + A.EXPR:
        pose = dict(A.POSES['wave'], _face=f, armr=A.I, forer=A.I)
        s = K.multi_scene(root, K.REAL_RP); K.put_flat(s, A, pose)
        tiles.append(K.label(s.render('front', size=280, span=0.62, center=(0, 1.62, 0)), f or 'default'))
    K.sheet(tiles, OUT + '/ashur_faces.png', cols=6, title='Ashur - faces')
if 'lineup' in what:
    s = K.multi_scene(root, K.REAL_RP)
    K.put_flat(s, A, A.POSES['idle'], at=(0.0, 0, 0))
    K.put_shipped(s, EM, 'em', EM.POSES['idle_a'], at=(1.1, 0, 0.2), parts=('body', 'head', 'armr', 'arml', 'legr', 'legl'))
    K.put_shipped(s, CE, 'ce', CE.POSES['idle'], at=(-1.1, 0, 0.2), parts=('body', 'head', 'armr', 'arml', 'forer', 'forel', 'legr', 'legl'))
    K.person(s, (-2.2, 0, 0.3))
    K.sheet([K.label(s.render((-12, 8), size=620, span=3.6, center=(-0.5, 1.0, 0)), 'size', 'a player, Celi, Ashur, Emma')], OUT + '/ashur_lineup.png', cols=1,
            title='Ashur - next to Celi and Emma')
if 'feet' in what:
    tiles = []
    for v in ('front', (-30, 30), 'side'):
        s = K.multi_scene(root, K.REAL_RP); K.put_flat(s, A, A.POSES['idle'])
        tiles.append(K.label(s.render(v, size=340, span=0.55, center=(0, 0.1, -0.05)), 'feet'))
    K.sheet(tiles, OUT + '/ashur_feet.png', cols=3, title='Ashur - bare feet, red polish, the gold anklet')

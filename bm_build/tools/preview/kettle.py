"""Kettle preview sheets (rigkit).  python3 tools/preview/kettle.py [views,poses,faces,lineup]"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import draftkit as K, kettle_art as A, capshun_art as CA, rigkit
OUT = K.OUT; os.makedirs(OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['views', 'poses', 'faces', 'lineup']
root = K.pack(A, OUT + '/rp_kt')


def tile(pose, view=(-30, 12), span=2.9, center=(0, 1.2, 0), size=340, label='', sub=None):
    s = K.multi_scene(root); rigkit.render(s, A, pose, scale=A.RIG_SCALE)
    return K.label(s.render(view, size=size, span=span, center=center), label, sub)


if 'views' in what:
    I = A.POSES['idle_a']
    K.sheet([tile(I, v, label=l) for v, l in (('front', 'front'), ((-35, 18), '3/4'), ('side', 'side (flat!)'), ('back', 'back'))],
            OUT + '/kettle_turnaround.png', cols=4, title='Kettle - turnaround')
if 'poses' in what:
    K.sheet([tile(A.POSES[n], label=n) for n in A.DRAFT], OUT + '/kettle_poses.png', cols=6, title='Kettle - poses')
if 'faces' in what:
    tiles = []
    for f in (None,) + A.FACES:
        pose = {k: v for k, v in dict(A.POSES['idle_a'], _face=f).items() if v is not None}
        s = K.multi_scene(root); rigkit.render(s, A, pose, scale=A.RIG_SCALE)
        tiles.append(K.label(s.render('front', size=260, span=1.0, center=(0, 1.85, 0)), f or 'default (the art)'))
    K.sheet(tiles, OUT + '/kettle_faces.png', cols=7, title='Kettle - faces')
if 'lineup' in what:
    rc = K.pack(CA, OUT + '/rp_mz')
    s = K.multi_scene(root, rc)
    rigkit.render(s, A, A.POSES['idle_a'], at=(0.0, 0, 0), scale=A.RIG_SCALE)
    rigkit.render(s, CA, CA.POSES['idle_a'], at=(1.2, 0, 0.2), scale=CA.RIG_SCALE)
    K.person(s, (-1.2, 0, 0.3))
    K.sheet([K.label(s.render((-12, 8), size=620, span=3.4, center=(0, 1.1, 0)), 'size', 'a player, Kettle, Mr. Capshun')], OUT + '/kettle_lineup.png', cols=1,
            title='Kettle - next to Mr. Capshun')

"""Mr. Capshun preview sheets.  python3 tools/preview/capshun.py [views,poses,faces,lineup]"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import draftkit as K, capshun_art as A, phase57_art as EM
OUT = K.OUT; os.makedirs(OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['views', 'poses', 'faces', 'lineup']
root = K.pack(A, OUT + '/rp_mz')


def tile(pose, view=(-30, 12), span=2.3, center=(0, 0.95, 0), size=340, label='', sub=None):
    s = K.multi_scene(root, K.REAL_RP); K.put_flat(s, A, pose)
    return K.label(s.render(view, size=size, span=span, center=center), label, sub)


if 'views' in what:
    I = A.POSES['idle_a']
    K.sheet([tile(I, v, label=l) for v, l in (('front', 'front'), ((-35, 18), '3/4'), ('side', 'side (flat!)'), ('back', 'back'))],
            OUT + '/capshun_turnaround.png', cols=4, title='Mr. Capshun - turnaround')
if 'poses' in what:
    K.sheet([tile(A.POSES[n], label=n) for n in A.DRAFT], OUT + '/capshun_poses.png', cols=6, title='Mr. Capshun - poses')
if 'faces' in what:
    tiles = []
    for f in (None,) + A.FACES:
        pose = dict(A.POSES['idle_a'], _face=f, head=None)
        pose = {k: v for k, v in pose.items() if v is not None}
        s = K.multi_scene(root, K.REAL_RP); K.put_flat(s, A, pose)
        tiles.append(K.label(s.render('front', size=260, span=0.75, center=(0, 1.52, 0)), f or 'worried (the sketch)'))
    K.sheet(tiles, OUT + '/capshun_faces.png', cols=6, title='Mr. Capshun - faces')
if 'lineup' in what:
    s = K.multi_scene(root, K.REAL_RP)
    K.put_flat(s, A, A.POSES['idle_a'], at=(0.0, 0, 0))
    K.put_shipped(s, EM, 'em', EM.POSES['idle_a'], at=(1.1, 0, 0.2), parts=('body', 'head', 'armr', 'arml', 'legr', 'legl'))
    K.person(s, (-1.2, 0, 0.3))
    K.sheet([K.label(s.render((-12, 8), size=620, span=3.4, center=(0, 1.0, 0)), 'size', 'a player, Mr. Capshun, Emma')], OUT + '/capshun_lineup.png', cols=1,
            title='Mr. Capshun - next to Emma')

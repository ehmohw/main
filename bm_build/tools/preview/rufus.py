"""Rufus Gnaw's rig preview sheets (rigkit).  python3 tools/preview/rufus.py [views,poses,faces,lineup]
Writes preview/rufus_rig_*.png (BM_PREVIEW_DIR for the scratch packs)."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM)
import draftkit as K, rufus_art as A, bender_art as BD, rigkit
OUT = K.OUT; os.makedirs(OUT, exist_ok=True)
DST = os.path.join(BM, 'preview')
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['views', 'poses', 'faces', 'lineup']
ROOT = K.pack(A, f'{OUT}/rp_rufus')


def tile(pose, view=(-35, 15), span=1.0, center=(0, 0.32, 0), size=320, label='', sub=None):
    s = K.multi_scene(ROOT); rigkit.render(s, A, pose, scale=A.RIG_SCALE)
    return K.label(s.render(view, size=size, span=span, center=center), label, sub)


I = A.POSES['idle_a']
if 'views' in what:
    K.sheet([tile(I, v, label=l) for v, l in (((-35, 15), 'front 3/4'), ('front', 'front'), ('side', 'side'), ('back', 'back'),
                                              ((145, 15), 'back 3/4'))] +
            [tile(dict(I, _tool='crossbow'), (-35, 15), label='crossbow out', sub='(the blade sheathed)')],
            f'{DST}/rufus_rig_views.png', cols=3, title='Rufus Gnaw - turnaround')
if 'poses' in what:
    K.sheet([tile(A.POSES[n], label=n) for n in A.DRAFT], f'{DST}/rufus_rig_poses.png', cols=5, title='Rufus Gnaw - poses')
if 'faces' in what:
    tiles = []
    for f in (None,) + A.FACES:
        pose = {k: v for k, v in dict(I, _face=f).items() if v is not None}
        tiles.append(tile(pose, 'front', span=0.42, center=(0, 0.46, 0), size=240, label=f or 'default'))
    K.sheet(tiles, f'{DST}/rufus_rig_faces.png', cols=4, title='Rufus Gnaw - faces')
if 'lineup' in what:
    BROOT = K.pack(BD, f'{OUT}/rp_bender')
    s = K.multi_scene(ROOT, BROOT)
    rigkit.render(s, A, A.POSES['idle_a'], at=(0.0, 0, 0), scale=A.RIG_SCALE, yaw=-20)
    rigkit.render(s, A, A.POSES['aim'], at=(0.75, 0, 0), scale=A.RIG_SCALE, yaw=-70)
    rigkit.render(s, BD, BD.POSES['idle_a'], at=(1.7, 0, 0.6), scale=BD.RIG_SCALE, yaw=120)
    K.person(s, (-1.0, 0, 0.3))
    K.sheet([K.label(s.render((-12, 8), size=720, span=4.4, center=(0.5, 0.9, 0)), 'size', 'a player, Rufus (and again, aiming), Bender')],
            f'{DST}/rufus_rig_lineup.png', cols=1, title='Rufus Gnaw - to scale')

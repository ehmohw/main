"""The Sky Buddies preview sheets.  python3 tools/preview/sky.py [faces,poses,turn,lineup,anim]
Billboarded: in the game the rig always faces you, so every tile is drawn as the camera sees it (the rig turned to the view)."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import draftkit as K, sky_art as A, rigkit, phase57_art as EM
OUT = K.OUT; os.makedirs(OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['faces', 'poses', 'turn', 'lineup']
root = K.pack(A, OUT + '/rp_yb')
C = (0.35, 1.0, 0)


def tile(pose, view=(0, 0), span=2.6, center=C, size=340, label='', sub=None):
    s = K.multi_scene(root, K.REAL_RP)
    rigkit.render(s, A, pose, scale=A.RIG_SCALE, yaw=-view[0])          # (billboard: turned to whoever looks)
    return K.label(s.render(view, size=size, span=span, center=center), label, sub)


if 'faces' in what:
    tiles = []
    for p in A.FACED:
        for e in (None,) + A.EXPR[p]:
            pose = dict(A.POSES['idle_a'], **{f'_face_{p}': e}) if e else dict(A.POSES['idle_a'])
            tiles.append(tile(pose, label=f'{p}: {e or "as painted"}', size=240))
    K.sheet(tiles, OUT + '/sky_faces.png', cols=7, title='The Sky Buddies - every face (each part: as painted, then its six)')
if 'poses' in what:
    K.sheet([tile(A.POSES[n], label=n) for n in A.DRAFT], OUT + '/sky_poses.png', cols=4, title='The Sky Buddies - poses')
if 'turn' in what:
    K.sheet([tile(A.POSES['idle_a'], v, label=l) for v, l in (((0, 0), 'from the front'), ((70, 10), 'walk round them...'), ((160, 20), '...behind'),
                                                             ((250, -15), 'from below'))],
            OUT + '/sky_billboard.png', cols=4, title='Billboarded - the same from any side')
if 'lineup' in what:
    s = K.multi_scene(root, K.REAL_RP)
    rigkit.render(s, A, A.POSES['idle_a'], at=(0.0, 0, 0), scale=A.RIG_SCALE, yaw=12)
    K.put_shipped(s, EM, 'em', EM.POSES['idle_a'], at=(-1.5, 0, 0.2), parts=('body', 'head', 'armr', 'arml', 'legr', 'legl'))
    K.person(s, (2.3, 0, 0.3))
    K.sheet([K.label(s.render((-12, 6), size=640, span=4.6, center=(0.3, 1.1, 0)), 'size', 'Emma, the Sky Buddies, a player')], OUT + '/sky_lineup.png', cols=1,
            title='The Sky Buddies - next to Emma and a player')
if 'anim' in what:
    import math
    frames = []
    seq = ['idle_0', 'idle_1', 'idle_2', 'idle_3']
    for i in range(24):
        a, b = seq[(i // 6) % 4], seq[(i // 6 + 1) % 4]
        pose = rigkit.mid(A.POSES[a], A.POSES[b], (i % 6) / 6)
        s = K.multi_scene(root, K.REAL_RP)
        xf = rigkit.solve(A.PIVOT, A.PARENT, pose)
        rot = rigkit.qs(('z', -i * 15))
        q, t = xf['rays']
        xf['rays'] = (rigkit.qmul(q, rot), t)
        rigkit.draw(s, A, xf, pose, scale=A.RIG_SCALE)
        frames.append(s.render((0, 0), size=300, span=2.6, center=C))
    frames[0].save(OUT + '/sky_idle.gif', save_all=True, append_images=frames[1:], duration=100, loop=0)

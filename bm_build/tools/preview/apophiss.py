"""Apophiss preview sheets + animations (the draft for approval).
    python3 tools/preview/apophiss.py [poses,turn,faces,follower,gifs] [gif names]"""
import sys, time, os
import os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import draftkit as K, apophiss_art as A, rigkit
import phase57_art as EM, phase96_art as LE
from PIL import Image
OUT = K.OUT; os.makedirs(OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['poses', 'turn', 'faces', 'follower', 'gifs']
t0 = time.time(); root = K.pack(A, K.OUT + '/rp_apo')
SC = A.BOSS_SCALE
k = SC / 2.0                     # (the sheets were framed at scale 2)
PK = A.PET_SCALE / 1.0
DESC = {'idle_a': 'idle - reared up, mace swaying', 'slither_a': 'slither (on the move)', 'battle': 'battle stance', 'claw_up': 'claw rake: wind-up',
        'claw': 'claw rake: strike', 'bite': 'lunging bite', 'mace_up': 'tail mace: raised', 'mace_slam': 'tail mace: slam', 'cast': 'dark magic: gather',
        'cast_point': 'dark magic: hurl', 'roar': 'roar', 'tired': 'tired (low health)', 'crouch': 'crouched to spring (the art)', 'sit': 'follower: sit',
        'ride': 'follower: ridden', 'defeated': 'beaten - offer him a place', 'eth_hover': 'PHASE 2 ethereal: hover', 'eth_beat': 'phase 2: wingbeat',
        'eth_cast': 'phase 2: cast'}

def scene():
    return K.multi_scene(root, K.REAL_RP)

def tile(pose, view='iso', span=8.4 * k, center=(0, 2.5 * k, 0), size=360, player=True, scale=SC, label='', sub=None):
    s = scene(); rigkit.render(s, A, pose, scale=scale)
    if player: K.person(s, (3.8 * k, 0, 1.2 * k))
    return K.label(s.render(view, size=size, span=span, center=center), label, sub)

if 'poses' in what:
    tiles = [tile(A.POSES[n], label=n, sub=DESC.get(n), span=(10.6 if A.POSES[n].get('_eth') else 9.2) * k,
                  center=(0, (3.5 if A.POSES[n].get('_eth') else 2.75) * k, 0)) for n in A.DRAFT]
    K.sheet(tiles, OUT + '/apophiss_poses.png', cols=5, title='Apophiss - boss poses (about nine blocks tall to his crest; the little figure is a player)')
if 'turn' in what:
    I = A.POSES['idle_a']; E = A.POSES['eth_hover']
    tiles = [tile(I, 'front', label='front', player=False), tile(I, 'side', label='side (his right)', player=False), tile(I, 'back', label='back', player=False),
             tile(I, (-35, 20), label='3/4 (his left)', player=False), tile(E, 'front', center=(0, 3.2 * k, 0), span=9.6 * k, label='phase 2 - front', player=False),
             tile(E, (150, 18), center=(0, 3.2 * k, 0), span=9.6 * k, label='phase 2 - from behind', player=False)]
    K.sheet(tiles, OUT + '/apophiss_turnaround.png', cols=3, title='Apophiss - turnaround (phase 1 and phase 2, ethereal)')
if 'faces' in what:
    tiles = []
    for f in (None,) + A.FACES:
        pose = dict(A.POSES['idle_a'], jaw=rigkit.qs(('x', 6)), head=rigkit.I, chest=rigkit.I, body=rigkit.I)
        if f: pose['_face'] = f
        s = scene(); rigkit.render(s, A, pose, scale=SC)
        tiles.append(K.label(s.render('front', size=300, span=3.0 * k, center=(0, 4.62 * k, 0.9 * k)), f or 'scowl (default)'))
    pose = dict(A.POSES['idle_a'], jaw=rigkit.qs(('x', 6)), head=rigkit.I, chest=rigkit.I, body=rigkit.I, _eth=True)
    s = scene(); rigkit.render(s, A, pose, scale=SC); tiles.append(K.label(s.render('front', size=300, span=3.0 * k, center=(0, 4.62 * k, 0.9 * k)), 'phase 2 eyes'))
    K.sheet(tiles, OUT + '/apophiss_faces.png', cols=4, title='Apophiss - faces')
if 'follower' in what:
    tiles = []
    # the lineup: Apophiss as a follower, Emma, Leo, a player
    s = scene(); rigkit.render(s, A, A.POSES['idle_a'], at=(1.6, 0, 0), scale=A.PET_SCALE)
    K.put_shipped(s, EM, 'em', EM.POSES['idle_a'], at=(-0.9, 0, 0.4), parts=('body', 'head', 'armr', 'arml', 'legr', 'legl'))
    K.put_shipped(s, LE, 'le', LE.POSES['idle_a'], at=(-1.9, 0, 0.4), parts=('body', 'head', 'armr', 'arml', 'legr', 'legl', 'trident'))
    K.person(s, (-2.9, 0, 0.4))
    tiles.append(K.label(s.render((15, 8), size=440, span=6.6, center=(-0.5, 2.1, 0)), 'follower size', 'Apophiss, Emma, Leo, a player'))
    # ridden
    s = scene(); pose = A.POSES['ride']; rigkit.render(s, A, pose, scale=A.PET_SCALE)
    seat = rigkit.point(A, pose, 'body', (0, 13.4, 0.6), scale=A.PET_SCALE); K.person(s, seat, sit=True)
    tiles.append(K.label(s.render((112, 14), size=440, span=4.8 * PK, center=(0, 1.4 * PK, 0)), 'ridden', 'saddled: you sit astride his back'))
    s = scene(); rigkit.render(s, A, A.POSES['sit'], scale=A.PET_SCALE); K.person(s, (-2.9, 0, 0.8))
    tiles.append(K.label(s.render('iso', size=440, span=4.6 * PK, center=(-0.3, 1.3 * PK, 0)), 'sit', 'coiled up, smug'))
    K.sheet(tiles, OUT + '/apophiss_follower.png', cols=3, title='Apophiss - as a follower (after you beat him)')
if 'gifs' in what:
    for name in (sys.argv[2].split(',') if len(sys.argv) > 2 else A.ANIMS):
        frames = K.anim_world(A, A.ANIMS[name], step=2)
        ims = []
        for xf, fp in frames:
            s = scene(); rigkit.draw(s, A, xf, fp, scale=SC); K.person(s, (3.8 * k, 0, 1.2 * k))
            c = (0, 3.5 * k, 0) if fp.get('_eth') else (0, 2.75 * k, 0)
            ims.append(s.render('iso', size=320, span=(10.6 if fp.get('_eth') else 9.2) * k, center=c))
        K.gif(ims, f'{OUT}/apophiss_{name}.gif', step=2)
        print(name, len(ims), 'frames', round(time.time() - t0, 1))
print('done', round(time.time() - t0, 1), 's')

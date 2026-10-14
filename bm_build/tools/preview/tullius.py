"""Tullius preview sheets + animations (the draft for approval).
    python3 tools/preview/tullius.py [views,poses,faces,lineup,gifs] [gif names]"""
import sys, time
import os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import draftkit as K, tullius_art as T, rigkit
import phase57_art as EM, phase96_art as LE
OUT = K.OUT; os.makedirs(OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['views', 'poses', 'faces', 'lineup', 'gifs']
t0 = time.time(); root = K.pack(T, K.OUT + '/rp_tu')
SC = T.RIG_SCALE
DESC = {'idle_a': 'idle - chin up, harpoon low', 'walk_a': 'walk', 'guard': 'on guard', 'thrust_back': 'thrust: drawn back', 'thrust': 'thrust: lunge',
        'throw_back': 'harpoon throw: wind-up', 'throw': 'harpoon throw: release', 'ice_cast': 'ice: gather frost', 'slam_up': 'CHARGED: frost harpoon raised',
        'slam': 'charged: driven into the ground', 'tired': 'tired (low health)', 'taunt': 'taunt: tips his hat', 'sit': 'follower: sit',
        'defeated': 'beaten - offer him a place'}

def scene():
    return K.multi_scene(root, K.REAL_RP)

def tile(pose, view='iso', span=3.8, center=(0, 1.3, 0), size=340, label='', sub=None, scale=SC, player=False):
    s = scene(); rigkit.render(s, T, pose, scale=scale)
    if player: K.person(s, (1.4, 0, 0.6))
    return K.label(s.render(view, size=size, span=span, center=center), label, sub)

if 'views' in what:
    I = T.POSES['idle_a']
    tiles = [tile(I, v, label=l) for v, l in (('front', 'front'), ('side', 'side (his right)'), ('back', 'back'), ((-35, 18), '3/4 (his left)'))]
    K.sheet(tiles, OUT + '/tullius_turnaround.png', cols=4, title='Tullius - turnaround (follower size)')
if 'poses' in what:
    tiles = [tile(T.POSES[n], label=n, sub=DESC.get(n)) for n in T.DRAFT]
    K.sheet(tiles, OUT + '/tullius_poses.png', cols=5, title='Tullius - poses (the harpoon frosts over for his charged attack)')
if 'faces' in what:
    tiles = []
    for f in (None,) + T.FACES:
        pose = dict(T.POSES['idle_a'], head=rigkit.I, body=rigkit.I)
        if f: pose['_face'] = f
        s = scene(); rigkit.render(s, T, pose, scale=SC)
        tiles.append(K.label(s.render('front', size=280, span=1.05, center=(0, 1.86, 0)), f or 'cold stare (default)'))
    K.sheet(tiles, OUT + '/tullius_faces.png', cols=4, title='Tullius - faces (a cold light deep in each socket)')
if 'lineup' in what:
    tiles = []
    s = scene()
    rigkit.render(s, T, T.POSES['idle_a'], at=(0.9, 0, 0), scale=SC)
    K.put_shipped(s, LE, 'le', LE.POSES['idle_a'], at=(-0.4, 0, 0.2), parts=('body', 'head', 'armr', 'arml', 'legr', 'legl', 'trident'))
    K.put_shipped(s, EM, 'em', EM.POSES['idle_a'], at=(-1.5, 0, 0.3), parts=('body', 'head', 'armr', 'arml', 'legr', 'legl'))
    K.person(s, (-2.5, 0, 0.3))
    tiles.append(K.label(s.render((10, 6), size=440, span=4.4, center=(-0.6, 1.4, 0)), 'rivals', 'Tullius, Leo, Emma, a player'))
    s = scene(); rigkit.render(s, T, T.POSES['guard'], scale=T.BOSS_SCALE); K.person(s, (2.2, 0, 1.2))
    tiles.append(K.label(s.render('iso', size=440, span=5.4, center=(0, 1.8, 0)), 'as the boss', f'{T.BOSS_SCALE}x - about {round(43.6 * T.BOSS_SCALE / 16, 1)} blocks to the hat'))
    s = scene(); rigkit.render(s, T, T.POSES['sit'], scale=SC); K.person(s, (1.5, 0, -0.4))
    tiles.append(K.label(s.render((30, 16), size=440, span=3.6, center=(0, 1.0, 0)), 'follower: sit', 'harpoon on his shoulder'))
    K.sheet(tiles, OUT + '/tullius_lineup.png', cols=3, title="Tullius - size: Leo's rival, and as the boss")
if 'gifs' in what:
    for name in (sys.argv[2].split(',') if len(sys.argv) > 2 else T.ANIMS):
        frames = K.anim_world(T, T.ANIMS[name], step=2)
        ims = []
        for xf, fp in frames:
            s = scene(); rigkit.draw(s, T, xf, fp, scale=SC)
            ims.append(s.render('iso', size=300, span=3.8, center=(0, 1.3, 0)))
        K.gif(ims, f'{OUT}/tullius_{name}.gif', step=2); print(name, len(ims), round(time.time() - t0, 1))
print('done', round(time.time() - t0, 1), 's')

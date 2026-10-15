"""Fishy preview sheets + animations (the draft for approval).
    python3 tools/preview/fishy.py [views,poses,faces,lineup,gifs] [gif names]"""
import sys, time
import os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import draftkit as K, fishy_art as F, rigkit
import phase57_art as EM
OUT = K.OUT; os.makedirs(OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['views', 'poses', 'faces', 'lineup', 'gifs']
t0 = time.time(); root = K.pack(F, K.OUT + '/rp_fy')
SC = F.RIG_SCALE
DESC = {'idle_a': 'idle - he paddles about his bowl', 'walk_a': 'walk', 'wave_a': 'the wave (from the art)', 'bow': "a gentleman's bow",
        'point': 'points the way (monocle squint)', 'shock': 'shocked - the monocle pops', 'sit': 'sit', 'tired': 'tired / fainting',
        'swim_2': 'laps: at his right', 'swim_6': 'laps: at his left'}


def solve(pose):
    xf = rigkit.solve(F.PIVOT, F.PARENT, pose)
    if '_fish_at' in pose:                               # (the fish swims about the bowl: his display moved, not just turned)
        q, t = xf['fish']; d = rigkit.D(pose['_fish_at']); qb, _ = xf['body']
        d = rigkit.qrot(qb, d)
        xf['fish'] = (q, tuple(t[i] + d[i] for i in range(3)))
    return xf


def scene():
    return K.multi_scene(root, K.REAL_RP)


def tile(pose, view='iso', span=3.2, center=(0, 1.0, 0), size=340, label='', sub=None, player=False):
    s = scene(); rigkit.draw(s, F, solve(pose), pose, scale=SC)
    if player: K.person(s, (1.4, 0, 0.6))
    return K.label(s.render(view, size=size, span=span, center=center), label, sub)


if 'views' in what:
    I = F.POSES['idle_a']
    tiles = [tile(I, v, label=l) for v, l in (('front', 'front'), ('side', 'side (his right)'), ('back', 'back'), ((-35, 18), '3/4 (his left)'))]
    K.sheet(tiles, OUT + '/fishy_turnaround.png', cols=4, title='Fishy - turnaround')
if 'poses' in what:
    tiles = [tile(F.POSES[n], label=n, sub=DESC.get(n)) for n in F.DRAFT]
    K.sheet(tiles, OUT + '/fishy_poses.png', cols=5, title='Fishy - poses')
if 'faces' in what:
    tiles = []
    for f in (None,) + F.FACES:
        pose = dict(F.POSES['idle_a'], fish=rigkit.I)
        if f: pose['_face'] = f
        s = scene(); rigkit.draw(s, F, solve(pose), pose, scale=SC)
        tiles.append(K.label(s.render('front', size=280, span=0.75, center=(0, 1.42, 0)), f or 'default (monocle)'))
    K.sheet(tiles, OUT + '/fishy_faces.png', cols=5, title='Fishy - faces (the monocle pops off when he\'s shocked)')
if 'lineup' in what:
    s = scene()
    rigkit.draw(s, F, solve(F.POSES['wave_a']), F.POSES['wave_a'], at=(0.7, 0, 0), scale=SC)
    K.put_shipped(s, EM, 'em', EM.POSES['idle_a'], at=(-0.6, 0, 0.3), parts=('body', 'head', 'armr', 'arml', 'legr', 'legl'))
    K.person(s, (-1.6, 0, 0.3))
    K.sheet([K.label(s.render((10, 6), size=520, span=3.8, center=(-0.3, 1.0, 0)), 'size', 'Fishy, Emma, a player')], OUT + '/fishy_lineup.png', cols=1,
            title='Fishy - size')
if 'gifs' in what:
    for name in (sys.argv[2].split(',') if len(sys.argv) > 2 else F.ANIMS):
        seq = F.ANIMS[name]; ims = []
        for i, (pn, ticks) in enumerate(seq):
            a, b = F.POSES[seq[i - 1][0]], F.POSES[pn]
            xa, xb = solve(a), solve(b)
            for k in range(0, ticks, 2):
                t = k / ticks; t = t * t * (3 - 2 * t)
                s = scene(); rigkit.draw(s, F, rigkit.blend(xa, xb, t), a if t < 0.5 else b, scale=SC)
                ims.append(s.render('iso', size=300, span=3.2, center=(0, 1.0, 0)))
        K.gif(ims, f'{OUT}/fishy_{name}.gif', step=2); print(name, len(ims), round(time.time() - t0, 1))
print('done', round(time.time() - t0, 1), 's')

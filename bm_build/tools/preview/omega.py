"""King Omega + the soul serpents - preview sheets and animations (the draft for approval; nothing here is in the pack).
    python3 tools/preview/omega.py [omega,serpents,lineup,flame,gifs] [gif names, as omega:idle or serp:cackle]"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [HERE, BM]
import draftkit as K, rigkit
import omega_art as O
import soulserp_art as S
import apophiss_art as A
OUT = K.OUT; os.makedirs(OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['omega', 'serpents', 'lineup', 'gifs']
t0 = time.time()
SC = O.BOSS_SCALE; k = SC / 2.0
ODESC = {'idle_a': 'idle - regal, the flame held up like a lamp', 'glide_a': 'glide (on the move)', 'monocle': 'adjusting the monocle',
         'bow': "a king's gracious bow", 'welcome': 'welcome! (arms wide, grinning)', 'battle': 'battle stance', 'flame_up': 'soul flame: wind-up',
         'flame_throw': 'soul flame: thrown', 'claw': 'claw rake', 'rally': 'the war cry (rallying his soldiers)', 'summon': 'summoning soul serpents',
         'tired': 'tired (low health)', 'sit': 'follower: sit', 'fade': 'fading away', 'shock': 'shocked'}
SDESC = {'idle_a': 'idle - bobbing, cackling', 'float_a': 'float (on the move)', 'cackle': 'the cackle', 'grin': 'the grin (plotting)',
         'sneak': 'sneaking up', 'boo': 'BOO!', 'swipe_up': 'swipe: wind-up', 'swipe': 'swipe', 'lunge': 'lunging bite (tongue first)',
         'flick': 'soul spit (the flame flicked)', 'hurt': 'hurt', 'fade': 'fading into wisps', 'salute': 'saluting the king'}
_root = {}


def scene():
    if not _root:
        _root['o'] = K.pack(O, OUT + '/rp_omega'); _root['s'] = K.pack(S, OUT + '/rp_serp'); _root['a'] = K.pack(A, OUT + '/rp_apo')
    return K.multi_scene(_root['o'], _root['s'], _root['a'], K.REAL_RP)


def otile(pose, view='iso', span=9.6 * k, center=(0, 3.1 * k, 0), size=360, player=True, label='', sub=None):
    s = scene(); rigkit.render(s, O, pose, scale=SC)
    if player: K.person(s, (3.8 * k, 0, 1.2 * k))
    return K.label(s.render(view, size=size, span=span, center=center), label, sub)


def stile(pose, view='iso', span=4.6, center=(0, 1.5, 0.7), size=300, player=True, label='', sub=None):
    s = scene(); rigkit.render(s, S, pose, scale=S.RIG_SCALE)
    if player: K.person(s, (-1.3, 0, 0.3))
    return K.label(s.render(view, size=size, span=span, center=center), label, sub)


if 'omega' in what:
    tiles = [otile(O.POSES[n], label=n, sub=ODESC.get(n)) for n in O.DRAFT]
    K.sheet(tiles, OUT + '/omega_poses.png', cols=5, title='King Omega - poses (about nine blocks tall, as his brother; the little figure is a player)')
    I = O.POSES['idle_a']
    tiles = [otile(I, 'front', label='front', player=False), otile(I, 'side', label='side', player=False),
             otile(I, 'back', label='back', player=False), otile(I, (-35, 20), label='3/4 (his left)', player=False)]
    K.sheet(tiles, OUT + '/omega_turnaround.png', cols=4, title='King Omega - turnaround')
    tiles = []
    for f in (None,) + O.FACES:
        pose = dict(O.POSES['idle_a'], jaw=rigkit.qs(('x', 22 if f in ('warm', 'roar', 'shock') else 6)), head=rigkit.I, chest=rigkit.I, body=rigkit.I)
        pose.pop('_face', None)
        if f: pose['_face'] = f
        s = scene(); rigkit.render(s, O, pose, scale=SC)
        tiles.append(K.label(s.render('front', size=300, span=3.3 * k, center=(0, 5.0 * k, 0.9 * k)), f or 'stern (default)'))
    K.sheet(tiles, OUT + '/omega_faces.png', cols=3, title='King Omega - faces')
    print('omega sheets', round(time.time() - t0, 1))
if 'flame' in what:
    s = scene(); pose = O.POSES['idle_a']; rigkit.render(s, O, pose, scale=SC)
    p = rigkit.point(O, pose, 'flame', (2.75, 8.0, 56.6), scale=SC)
    K.label(s.render('iso', size=420, span=3.2 * k, center=p), 'flame close-up').save(OUT + '/omega_flame.png')
if 'serpents' in what:
    tiles = [stile(dict(S.POSES[n], _crest='abcabcabcabca'[i]), label=n, sub=SDESC.get(n)) for i, n in enumerate(S.DRAFT)]
    K.sheet(tiles, OUT + '/soulserp_poses.png', cols=5, title='Soul serpents - poses (crests mixed; the figure is a player)')
    tiles = []
    for cr in S.CRESTS:
        for f in (None,) + S.FACES:
            pose = dict(S.POSES['idle_a'], _crest=cr, head=rigkit.I, body=rigkit.I, jaw=rigkit.qs(('x', 2 if f in ('grin', 'blink') else 30 if f in ('shriek', 'hurt') else 14)))
            if f: pose['_face'] = f
            tiles.append(stile(pose, 'front', span=1.9, center=(0, 2.2, -0.2), size=240, player=False, label=f'crest {cr}', sub=f or 'scowl (default)'))
    K.sheet(tiles, OUT + '/soulserp_faces.png', cols=4, title='Soul serpents - the three crests and the faces')
    I = S.POSES['idle_a']
    tiles = [stile(I, v, player=False, label=l) for v, l in (('front', 'front'), ('side', 'side'), ('back', 'back'), ((-35, 20), '3/4'))]
    K.sheet(tiles, OUT + '/soulserp_turnaround.png', cols=4, title='Soul serpent - turnaround (crest a)')
    print('serpent sheets', round(time.time() - t0, 1))
if 'lineup' in what:
    s = scene()
    rigkit.render(s, O, O.POSES['idle_a'], at=(0, 0, 0), scale=SC)
    for i, (x, z, cr, pose) in enumerate(((-4.2, -1.5, 'a', 'cackle'), (-6.0, 0.4, 'b', 'salute'), (4.8, -1.8, 'c', 'grin'), (6.4, 0.6, 'a', 'sneak'))):
        rigkit.render(s, S, dict(S.POSES[pose], _crest=cr), at=(x, 0, z), scale=S.RIG_SCALE, yaw=10 * (1 if x < 0 else -1))
    K.person(s, (2.6, 0, -2.6))
    rigkit.render(s, A, A.POSES['idle_a'], at=(13, 0, 2), scale=A.BOSS_SCALE, yaw=-30)
    K.label(s.render((20, 10), size=900, span=26, center=(3.5, 4.0, 0)), 'King Omega, his soul serpents, a player - and his brother Apophiss (right)').save(OUT + '/omega_lineup.png')
    print('lineup', round(time.time() - t0, 1))
if 'gifs' in what:
    names = sys.argv[2].split(',') if len(sys.argv) > 2 else [f'omega:{n}' for n in O.ANIMS] + [f'serp:{n}' for n in S.ANIMS]
    for full in names:
        who, name = full.split(':')
        rig = O if who == 'omega' else S
        frames = K.anim_world(rig, rig.ANIMS[name], step=2)
        ims = []
        for xf, fp in frames:
            s = scene()
            if who == 'omega':
                rigkit.draw(s, O, xf, fp, scale=SC); K.person(s, (3.8 * k, 0, 1.2 * k))
                ims.append(s.render('iso', size=320, span=10.0 * k, center=(0, 3.2 * k, 0)))
            else:
                fp = dict(fp, _crest={'cackle': 'b', 'salute': 'b', 'sneak_boo': 'c', 'flick': 'c'}.get(name, 'a'))
                rigkit.draw(s, S, xf, fp, scale=S.RIG_SCALE); K.person(s, (-1.3, 0, 0.3))
                ims.append(s.render('iso', size=280, span=4.8, center=(0, 1.5, 0.7)))
        K.gif(ims, f'{OUT}/{"omega" if who == "omega" else "soulserp"}_{name}.gif', step=2)
        print(full, len(ims), 'frames', round(time.time() - t0, 1))
print('done', round(time.time() - t0, 1), 's')

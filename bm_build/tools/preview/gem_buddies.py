"""The Gem's Buddies - preview sheets (rigkit).  python3 tools/preview/gem_buddies.py [lineup,poses,faces,vsref] [names...]"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import draftkit as K, gem_buddies_art as GB, kettle_art as KA, rigkit
OUT = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'preview'); os.makedirs(OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['lineup', 'poses']
names = sys.argv[2:] or list(GB.RIGS)
TMP = K.OUT; os.makedirs(TMP, exist_ok=True)
roots = {n: K.pack(GB.RIGS[n], f'{TMP}/rp_gb_{n}') for n in GB.RIGS}


def tile(n, pose, view=(-28, 12), size=300, label='', sub=None, scale=None):
    A = GB.RIGS[n]; s = K.multi_scene(roots[n]); rigkit.render(s, A, A.POSES[pose], scale=scale or A.RIG_SCALE)
    return K.label(s.render(view, size=size, span=1.9, center=(0, 0.62, 0)), label or pose, sub)


if 'poses' in what:
    for n in names:
        mv = GB.MOVES[n]
        seq = ['appear', 'idle_a', 'idle_b', mv[0], mv[1], 'wind', 'strike', 'happy', 'vanish']
        tiles = [tile(n, p, sub=('the ' + mv[2].lower() if p in ('wind', 'strike') else None)) for p in seq]
        tiles += [tile(n, 'idle_a', 'front', label='front'), tile(n, 'idle_a', 'side', label='side (facing left)'), tile(n, 'idle_a', 'back', label='back'),
                  tile(n, 'wind', 'side', label='wind, side'), tile(n, 'strike', 'side', label='strike, side')]
        K.sheet(tiles, f'{OUT}/gem_buddies_{n}.png', cols=6, title=f'{n.capitalize()} - poses ({mv[2]})')
if 'faces' in what:
    for n in names:
        A = GB.RIGS[n]; tiles = []
        for f in (None,) + GB.FACES:
            pose = dict(A.POSES['idle_a']); pose.pop('_face', None)
            if f: pose['_face'] = f
            s = K.multi_scene(roots[n]); rigkit.render(s, A, pose, scale=A.RIG_SCALE)
            tiles.append(K.label(s.render('front', size=240, span=1.3, center=(0, 0.62, 0)), f or 'default'))
        K.sheet(tiles, f'{OUT}/gem_buddies_{n}_faces.png', cols=6, title=f'{n.capitalize()} - faces')
if 'lineup' in what:
    rk = K.pack(KA, TMP + '/rp_kt')
    s = K.multi_scene(rk, *roots.values())
    K.person(s, (-1.4, 0, 0.6))
    rigkit.render(s, KA, KA.POSES['idle_a'], at=(-0.4, 0, 0.6), scale=KA.RIG_SCALE)
    for i, n in enumerate(GB.RIGS):
        A = GB.RIGS[n]; x = 0.7 + i * 0.95; z = 0.0
        rigkit.render(s, A, A.POSES['idle_a'], at=(x, 0, z), scale=A.RIG_SCALE)
    im = s.render((-6, 6), size=1600, span=12.8, center=(4.4, 0.9, 0.0))
    im = im.crop((0, int(im.height * 0.36), im.width, int(im.height * 0.66)))
    K.sheet([K.label(im, 'size',
                     'a player, Kettle, then Grace, Robo, Zapper, Dessa, Bubbles, Chase, Limer, Chico, Spike, Cheferoni')],
            f'{OUT}/gem_buddies_lineup.png', cols=1, title="The Gem's Buddies - to scale")
if 'vsref' in what:
    # each Buddy front on (whole, and the face close up) beside the owner's own drawing of it (ref/owner/buddies - reference only)
    from PIL import Image
    BM = os.path.dirname(os.path.dirname(HERE))
    FOC = {'grace': (0.72, 0.62), 'robo': (0.78, 0.6), 'zapper': (0.62, 0.55), 'dessa': (0.66, 0.6), 'bubbles': (0.34, 0.62),
           'chase': (0.6, 0.5), 'limer': (0.62, 0.58), 'chico': (0.72, 0.55), 'spike': (0.48, 0.55), 'cheferoni': (0.72, 0.62)}
    FULL = {'grace': (0.6, 1.3), 'robo': (0.65, 1.45), 'zapper': (0.55, 1.3), 'dessa': (0.5, 1.2), 'bubbles': (0.38, 1.1),
            'chase': (0.48, 1.0), 'limer': (0.52, 1.1), 'chico': (0.52, 1.15), 'spike': (0.48, 1.0), 'cheferoni': (0.62, 1.35)}
    tiles = []
    for n in names:
        A = GB.RIGS[n]; cy, sp = FOC[n]; fy, fs = FULL[n]
        s = K.multi_scene(roots[n]); rigkit.render(s, A, A.POSES['idle_a'], scale=A.RIG_SCALE)
        full = s.render('front', size=300, span=fs, center=(0, fy, 0))
        s = K.multi_scene(roots[n]); rigkit.render(s, A, A.POSES['idle_a'], scale=A.RIG_SCALE)
        im = s.render('front', size=300, span=sp, center=(0, cy, 0))
        ref = Image.open(f'{BM}/ref/owner/buddies/{n}.png').convert('RGBA'); ref.thumbnail((300, 300))
        bg = Image.new('RGBA', (300, 300), (255, 255, 255, 255)); bg.alpha_composite(ref, ((300 - ref.width) // 2, (300 - ref.height) // 2))
        pair = Image.new('RGB', (912, 300), 'white'); pair.paste(full.convert('RGB'), (0, 0)); pair.paste(im.convert('RGB'), (306, 0)); pair.paste(bg.convert('RGB'), (612, 0))
        tiles.append(K.label(pair, n.capitalize(), 'the model, front | its face | the owner\'s drawing'))
    K.sheet(tiles, f'{OUT}/gem_buddies_faces_vs_ref.png', cols=2, title="The Gem's Buddies - faces against the owner's art")

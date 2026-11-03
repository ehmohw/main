"""The Rat King (ratking_art.py) - preview sheets.   python3 tools/preview/rat_king.py [lineup,poses,turn,anim]
lineup   the new Rat King beside a player (Steve) for scale, idle_a
poses    every pose, one sheet
turn     idle_a and atk_0 from the front, 3/4, side and back
anim     GIFs: idle, walk, attack, the Royal Decree, hurt, death (the poses blended as the game interpolates them)
PNGs / GIFs to $RK_OUT (default /home/user/main/previews/v30g_rat_king)."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM)
from PIL import Image, ImageDraw, ImageFont
import draftkit as K
import playerkit as PK
import rigkit
import ratking_art as A

OUT = os.environ.get('RK_OUT', '/home/user/main/previews/v30g_rat_king'); os.makedirs(OUT, exist_ok=True)
ROOT = K.pack(A, os.path.join(K.OUT, 'rp_rk'))
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['lineup', 'poses', 'turn', 'anim']
try:
    FNB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
except OSError:
    FNB = None


def floor(s, r=4.0):
    n = int(r)
    for i in range(-n, n):
        for j in range(-n, n):
            s.solid((i, -0.25, j), (i + 1, 0.0, j + 1), '#2a2420' if (i + j) % 2 else '#3a322c')


def king(s, pose, at=(0, 0, 0), yaw=0.0):
    rigkit.render(s, A, A.POSES[pose] if isinstance(pose, str) else pose, at=at, scale=A.RIG_SCALE, yaw=yaw)


def tile(pose, view=(-30, 12), size=380, span=4.4, text=None, sub=None, steve=False, center=(0, 1.45, 0)):
    s = K.multi_scene(ROOT); king(s, pose)
    if steve: PK.put(s, PK.player('stand'), at=(-2.0, 0, -0.6))
    floor(s)
    return K.label(s.render(view, size=size, span=span, center=center), text or (pose if isinstance(pose, str) else ''), sub)


if 'lineup' in what:
    tiles = [tile('idle_a', view='front', steve=True, span=5.0, text='The Rat King - idle_a', sub='front, a player (1.8) for scale; ~2.8 blocks to the crown'),
             tile('idle_a', view=(-35, 12), steve=True, span=5.0, text='3/4'),
             tile('idle_a', view=(-120, 14), span=5.0, text='from behind', sub='the cape, the ermine, the gold-ringed tail')]
    p = os.path.join(OUT, 'rat_king_lineup.png'); K.sheet(tiles, p, cols=3, title='The Rat King (3.0g) - the heist\'s rarest champion, as a rig'); print(p)

if 'poses' in what:
    tiles = [tile(n, center=(0, 1.0, 0.4) if n == 'death_1' else (0, 1.45, 0)) for n in A.POSE_NAMES]
    p = os.path.join(OUT, 'rat_king_poses.png'); K.sheet(tiles, p, cols=5, title='The Rat King - every pose'); print(p)

if 'turn' in what:
    tiles = []
    for n in ('idle_a', 'atk_0', 'sp_0'):
        for v, l in (('front', 'front'), ((-35, 12), '3/4'), ('side', 'side'), ('back', 'back')):
            tiles.append(tile(n, view=v, size=320, text=n, sub=l))
    p = os.path.join(OUT, 'rat_king_turn.png'); K.sheet(tiles, p, cols=4, title='The Rat King - turnarounds'); print(p)

if 'anim' in what:
    SEQ = {'idle': [('idle_a', 20), ('idle_b', 20)], 'walk': [('walk_0', 5), ('walk_1', 5), ('walk_2', 5), ('walk_3', 5)] * 2,
           'attack': [('idle_a', 6), ('atk_0', 7), ('atk_1', 3), ('atk_1', 6), ('idle_a', 8)],
           'decree': [('idle_a', 4), ('sp_0', 10), ('sp_0', 12), ('sp_1', 3), ('sp_1', 14), ('idle_a', 10)],
           'hurt': [('idle_a', 4), ('hurt', 2), ('hurt', 6), ('idle_a', 8)],
           'death': [('idle_a', 4), ('death_0', 12), ('death_0', 6), ('death_1', 16), ('death_1', 10)],
           'arrive': [('arrive_0', 6), ('arrive_0', 8), ('arrive_1', 12), ('arrive_1', 8), ('idle_a', 10)]}
    for name, seq in SEQ.items():
        frames = []
        xs = [rigkit.solve(A.PIVOT, A.PARENT, A.POSES[p]) for p, _d in seq]
        for i, (p, d) in enumerate(seq):
            a = xs[i - 1] if i else xs[0]; b = xs[i]
            for t in range(0, d, 2):
                xf = rigkit.blend(a, b, min(1.0, (t + 2) / d))
                s = K.multi_scene(ROOT); rigkit.draw(s, A, xf, A.POSES[p], scale=A.RIG_SCALE); floor(s)
                frames.append(s.render((-30, 12), size=300, span=4.6, center=(0, 1.3, 0)).convert('P', palette=Image.ADAPTIVE))
        out = os.path.join(OUT, f'rat_king_{name}.gif')
        frames[0].save(out, save_all=True, append_images=frames[1:], duration=100, loop=0); print(out)

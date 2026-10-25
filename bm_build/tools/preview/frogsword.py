"""2.94u: the Frog with Mustache and his sword, from the shipped pose functions (front, side, 3/4).
    python3 tools/preview/frogsword.py [out.png] [pose ...]"""
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import draftkit as K
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(K.OUT, 'frogsword.png')
poses = sys.argv[2:] or ['idle0_10', 'hop1_3', 'sit_10']
FN = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'out_p2', 'BlackMarket_DP', 'data', 'bm', 'function', 'p63', 'frog', 'p')
WOLF_Y = 0.85                                       # (the parts ride the wolf: its passenger offset)
def parts(pose):
    P = {}
    for l in open(os.path.join(FN, pose + '.mcfunction')):
        m = re.search(r'tag=bm\.(frr_\w+|fp_weap)\].*left_rotation:\[([^\]]+)\],translation:\[([^\]]+)\]', l)
        if m: P[m.group(1)] = (tuple(float(v.rstrip('f')) for v in m.group(2).split(',')), tuple(float(v.rstrip('f')) for v in m.group(3).split(',')))
    return P
tiles = []
for pose in poses:
    P = parts(pose)
    for view, cam in (('front', 'front'), ('side', (90, 0)), ('3/4', (35, 20))):
        s = K.multi_scene(K.REAL_RP, *([os.environ['STANDIN']] if os.environ.get('STANDIN') else []))
        for n, (rot, tr) in P.items():
            if n == 'fp_weap':
                s.display('minecraft:item/iron_sword', pos=(0, WOLF_Y, 0), scale=0.6, left=rot, translation=tr)
            else:
                s.display(f'bm:item/{n}' if n != 'frr_head' else 'bm:item/frr_head_none', pos=(0, WOLF_Y, 0), scale=0.8, left=rot, translation=tr)
        tiles.append(K.label(s.render(cam, size=300, span=1.4, center=(0, 0.35, 0)), f'{pose}, {view}'))
K.sheet(tiles, out, cols=3, title='The Frog with Mustache - his sword')
print(out)

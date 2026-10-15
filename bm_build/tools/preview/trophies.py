"""2.79a: the dungeon bosses' trophies - each boss in miniature on its plinth (front and three-quarter), beside the trophy it
replaces, from the shipped pack (or the models fresh from p2/trophy_models, before a build).
    python3 tools/preview/trophies.py [out.png] [--fresh]"""
import sys, os, json, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import draftkit as K
args = [a for a in sys.argv[1:] if not a.startswith('--')]
out = args[0] if args else os.path.join(K.OUT, 'trophies.png')
NAMES = {'brood': 'The Broodmother', 'frost': 'The Frost Marksman', 'tide': 'The Drowned Tyrant', 'hex': 'The Archmage',
         'keep': 'Bobbery', 'hollow': 'The Hollow King', 'lucky': 'The Golden Goose'}
roots = [K.REAL_RP]
if '--fresh' in sys.argv:                                   # (the new models, written into a scratch pack in front of the real one)
    import p2.trophy_models as TM
    crown = json.load(open(os.path.join(K.REAL_RP, 'assets', 'bm', 'models', 'item', 'crown.json')))
    tmp = tempfile.mkdtemp()
    md = os.path.join(tmp, 'assets', 'bm', 'models', 'item'); os.makedirs(md)
    for d, (tex, els) in TM.models(({k: v for k, v in crown['textures'].items() if k != 'particle'}, crown['elements'])).items():
        t = dict(tex); t['particle'] = list(tex.values())[0]
        json.dump({'textures': t, 'elements': els}, open(os.path.join(md, f'trophy3d_{d}.json'), 'w'))
    roots = [tmp, K.REAL_RP]
tiles = []
for d, nm in NAMES.items():
    for view, sub in (('front', 'front'), ((35, 22), 'three-quarter')):
        s = K.multi_scene(*roots)
        s.display(f'bm:item/trophy3d_{d}', pos=(0, 0.5, 0), ctx='none')
        tiles.append(K.label(s.render(view, size=330, span=1.15, center=(0, 0.55, 0)), nm, sub))
K.sheet(tiles, out, cols=4, title='Boss trophies')
print(out)

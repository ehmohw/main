"""2.93: the Champions' regalia on their own bones - each follower's head with its head piece, its body with its body piece and
medal (front and three-quarter), from the built pack.   python3 tools/preview/champions.py [out.png] [who ...]
  [--head: the heads and their pieces] [--bare: the bones alone] [--back | --side: the second view] [--medal: medal close-ups]"""
import sys, os, json, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import draftkit as K
import champion_art as CA
args = [a for a in sys.argv[1:] if not a.startswith('--')]
out = args[0] if args and args[0].endswith('.png') else os.path.join(K.OUT, 'champions.png')
only = [a for a in args if not a.endswith('.png')]
tmp = tempfile.mkdtemp()


class R2:
    @staticmethod
    def p(*parts):
        f = os.path.join(tmp, *parts); os.makedirs(os.path.dirname(f), exist_ok=True); return f
    @staticmethod
    def wj(rel, obj):
        json.dump(obj, open(R2.p(*rel.split('/')), 'w'))


CA.build(R2, src=lambda *parts: os.path.join(K.REAL_RP, *parts))
tiles = [(who, bone, piece, view) for who, (_ht, hm, _bt, bm_) in CA.ANCHORS.items() if not only or who in only
         for bone, piece in (((hm, 'head'),) if '--head' in sys.argv else ((bm_, 'body'),)) for view in ('front', (145, 22) if '--back' in sys.argv else (-90, 15) if '--side' in sys.argv else (35, 22))]
# (rendering: the bone's own model and the piece's, both at the origin in 'fixed')
imgs = []
SPAN = {'apo': 3.2, 'omega': 3.2}     # (the serpents' coils stand tall)
def model_id(mid):
    it = json.load(open(os.path.join(K.REAL_RP, 'assets', 'bm', 'items', f'{mid}.json')))['model']
    while it.get('type') in ('minecraft:select', 'minecraft:condition', 'minecraft:composite'):
        it = it.get('fallback') or it.get('on_false') or it['models'][0]
    return it['model']
for who, bone, piece, view in tiles:
    s = K.multi_scene(tmp, K.REAL_RP)
    s.display(model_id(bone), pos=(0, 0, 0))
    if '--bare' not in sys.argv and os.path.exists(R2.p('assets', 'bm', 'models', 'item', f'champ_{who}_{piece}.json')):     # (a follower without that piece shows its own bone)
        s.display(f'bm:item/champ_{who}_{piece}', pos=(0, 0, 0))
    if piece == 'body' and '--bare' not in sys.argv: s.display(f'bm:item/champ_{who}_medal', pos=(0, 0, 0))
    imgs.append(K.label(s.render(view, size=220, span=SPAN.get(who, 1.6) if piece == 'body' else (2.0 if who in SPAN else 1.3), center=(0, (0.1 if who not in SPAN else 0.6) if piece == 'body' else (1.0 if who in SPAN else 0.55), 0)), who, f'{piece} {"front" if view == "front" else "back" if view[0] > 90 else "3/4"}'))
if '--medal' in sys.argv:          # (close-ups: each medal on its chest, front and three-quarter)
    imgs = []
    for who, (_ht, _hm, _bt, bm_) in CA.ANCHORS.items():
        if only and who not in only: continue
        m = json.load(open(R2.p('assets', 'bm', 'models', 'item', f'champ_{who}_medal.json')))
        c = [sum((e['from'][i] + e['to'][i]) / 2 for e in m['elements']) / len(m['elements']) for i in range(3)]
        fx = m.get('display', {}).get('fixed', {})
        sc, tr = fx.get('scale', [1, 1, 1]), fx.get('translation', [0, 0, 0])
        ctr = tuple(((c[i] - 8) * sc[i] + tr[i]) / 16 * (-1 if i != 1 else 1) for i in range(3))   # (a fixed item faces back: x and z turned)
        for view in ('front', (30, 15)):
            s = K.multi_scene(tmp, K.REAL_RP)
            s.display(model_id(bm_), pos=(0, 0, 0)); s.display(f'bm:item/champ_{who}_medal', pos=(0, 0, 0))
            imgs.append(K.label(s.render(view, size=180, span=0.55, center=ctr), who, 'medal'))
K.sheet(imgs, out, cols=8, title="Champions' regalia")
print(out)

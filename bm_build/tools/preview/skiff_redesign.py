"""The player's Vorn Skiff (phase36's skiff_<paint>_<decal> models, vanilla.py's paints), previewed.
    python3 tools/preview/skiff_redesign.py [OLD_MODEL_JSON]
compare: the default paint (Vorn Green, no decal) beside the old model (OLD_MODEL_JSON: an (textures, elements) pair saved from
before the change, optional), each with a seated pilot, 3/4, side, below; paints: all twelve paints; decals: the four decals on
the default. Sheets go to $SK_OUT (default previews/v299_armada/items); the throwaway pack to draftkit's $BM_PREVIEW_DIR."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import draftkit as K
import gen_rp, phase36, vanilla

OUT = os.environ.get('SK_OUT', os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), 'previews', 'v299_armada', 'items'))
os.makedirs(OUT, exist_ok=True)
ROOT = os.path.join(K.OUT, 'rp_skiff')
OLD = sys.argv[1] if len(sys.argv) > 1 else None
SC, Y0, SEAT_Y = 4.5, 2.2, 8.0                     # (phase35's scale; lifted clear of the grid; the pilot's hips, model units)
FIX = {'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]}}


def build():
    os.makedirs(f'{ROOT}/assets/bm/models/item', exist_ok=True); os.makedirs(f'{ROOT}/assets/bm/textures/block', exist_ok=True)
    for k, im in vanilla.textures().items():
        if k.startswith('skiff_'): im.save(f'{ROOT}/assets/bm/textures/block/{k}.png')
    phase36.rp(gen_rp)
    def put(name, tex, els):
        t = dict(tex); t['particle'] = list(tex.values())[0]
        json.dump({'textures': t, 'elements': els, 'display': FIX}, open(f'{ROOT}/assets/bm/models/item/{name}.json', 'w'))
    n = 0
    for name, (tex, els) in gen_rp.HATS.items():
        if name.startswith('skiff_'):
            put(name, tex, els); n = max(n, len(els))
            for e in els:
                for v in e['from'] + e['to']: assert -16 <= v <= 32, (name, e)
                for f in e['faces'].values(): assert all(0 <= u <= 16 for u in f['uv']), (name, f)
    print('skiff models checked; most elements in one:', n, '- base (none):', len(gen_rp.HATS['skiff_green_none'][1]))
    if OLD:
        tex, els = json.load(open(OLD)); put('skiff_old', tex, els)


def ship(s, mid, x=0.0, z=0.0, pilot=True):
    s.display(mid, pos=(x, Y0, z), scale=SC, ctx='fixed')
    if pilot: K.person(s, (x, Y0 + (SEAT_Y / 16 - 0.5) * SC, z), sit=True)


def tile(fn, view, size=520, span=6.0, center=(0, 2.2, 0), text=''):
    s = K.multi_scene(ROOT); fn(s)
    return K.label(s.render(view, size=size, span=span, center=center), text)


build()
tiles = []
pair = (lambda s: (ship(s, 'bm:item/skiff_green_none', 2.6), ship(s, 'bm:item/skiff_old', -2.6))) if OLD else (lambda s: ship(s, 'bm:item/skiff_green_none'))
for view, txt in (((-35, 24), '3/4'), ((90, 5), 'side'), ((20, -50), 'below'), ((0, 8), 'front')):
    tiles.append(tile(pair, view, size=640, span=11.0, center=(0, 2.4, 0), text=f'Vorn Green: new (right) / old (left) - {txt}' if OLD else txt))
K.sheet(tiles, os.path.join(OUT, 'skiff_compare.png'), cols=2, title='The Vorn Skiff - the new default beside the old, a seated pilot')
tiles = [tile(lambda s, c=c: ship(s, f'bm:item/skiff_{c}_none', pilot=False), (-35, 24), size=360, span=5.6, text=f'{c} ({nm})')
         for c, nm, _ in phase36.COLOURS]
K.sheet(tiles, os.path.join(OUT, 'skiff_paints.png'), cols=4, title='The Vorn Skiff - all twelve paints, the new hull')
tiles = [tile(lambda s, d=d: ship(s, f'bm:item/skiff_green_{d}', pilot=False), v, size=420, span=5.6, text=f'{d} ({nm}) {vn}')
         for d, nm in phase36.DECALS for v, vn in (((-35, 24), '3/4'), ((150, 35), 'aft, above'))]
K.sheet(tiles, os.path.join(OUT, 'skiff_decals.png'), cols=4, title='The Vorn Skiff - the four decals on Vorn Green')
for n in ('skiff_compare', 'skiff_paints', 'skiff_decals'): print(os.path.join(OUT, n + '.png'))

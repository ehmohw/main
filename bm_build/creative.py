"""2.96a: THE CREATIVE FORMS' LOOK - a Buddy (and Emma, Queen Ava, Democratus, KillerWatt, Queen Pearl) beside the Gem of Creativity is
painted in its colours: every part of them washed in a rainbow that runs over them, part to part, as they go.

It's a TINT, so it reaches every part whatever pose, face, form or outfit it's showing: the resource pack (rp, a post pass) gives
every face of every model of theirs (by prefix, PREFIX) tintindex 0, and every item definition naming one a tint read from the
display's own custom_model_data colours (white by default - no change: a part without colours looks exactly as it always did).
The datapack (phase233) sets those colours on their parts while the Creative Form pair runs, a few times a second, and takes them
off again when they part."""
import colorsys
import json
import os

# follower -> the prefixes of their models (every part, face and look)
PREFIX = {'fishy': ('fy_',), 'batty': ('gb_',), 'eggbert': ('ge_',), 'count': ('gc_',), 'capshun': ('mz_',), 'sky': ('yb_',),
          'kettle': ('kt_',), 'emma': ('em_', 'ee_', 'emkw_'), 'ava': ('av_',), 'demo': ('dm_',), 'kw': ('kw_',), 'pearlq': ('pq_',)}
FORMS = tuple(PREFIX)
# the rainbow the tint runs through: light, so their own shading and features still show under it
N = 12
COLOURS = [int('%02x%02x%02x' % tuple(int(c * 255) for c in colorsys.hsv_to_rgb(i / N, 0.5, 1.0)), 16) for i in range(N)]
WHITE = 0xFFFFFF
TINT = {'type': 'minecraft:custom_model_data', 'index': 0, 'default': WHITE}


def _tinted(node):
    """every model node of an item definition (through selects, conditions, composites) reads the tint"""
    if isinstance(node, dict):
        if node.get('type') == 'minecraft:model':
            node['tints'] = [TINT]
        for v in node.values():
            _tinted(v)
    elif isinstance(node, list):
        for v in node:
            _tinted(v)


def rp(R):
    def post(R2):
        root = R2.p()
        pre = tuple(p for ps in PREFIX.values() for p in ps)
        md = os.path.join(root, 'assets/bm/models/item')
        n_m = n_i = 0
        for f in os.listdir(md):
            if not f.startswith(pre) or not f.endswith('.json'): continue
            path = os.path.join(md, f)
            m = json.load(open(path))
            for e in m.get('elements', []):
                for face in e.get('faces', {}).values():
                    face['tintindex'] = 0
            json.dump(m, open(path, 'w'), separators=(',', ':'))
            n_m += 1
        idir = os.path.join(root, 'assets/bm/items')
        for f in os.listdir(idir):
            if not f.startswith(pre) or not f.endswith('.json'): continue
            path = os.path.join(idir, f)
            d = json.load(open(path))
            _tinted(d)
            json.dump(d, open(path, 'w'), separators=(',', ':'))
            n_i += 1
        assert n_m and n_i, (n_m, n_i)
        print(f'creative: {n_m} models and {n_i} item definitions take the Creative Forms\' tint')
    R.POST.append(post)

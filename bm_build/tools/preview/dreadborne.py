"""2.93: the Dreadborne and the Seraph's Raiment (2.99: the Seraph's own sheets are tools/preview/seraph.py) - both helms (front, three-quarter, behind), the wings layers, the plate and
the sprites, from the art modules.   python3 tools/preview/dreadborne.py [out.png]"""
import sys, os, json, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from PIL import Image
import draftkit as K
import dread_armor as DA
import dread_set_art as DS
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(K.OUT, 'dreadborne.png')
tmp = tempfile.mkdtemp()


class R2:
    POST, ICONS, LANG, TEXTURE_MODS, HATS = [], {}, {}, [], {}
    @staticmethod
    def p(*parts):
        f = os.path.join(tmp, *parts); os.makedirs(os.path.dirname(f), exist_ok=True); return f
    @staticmethod
    def wj(rel, obj):
        json.dump(obj, open(R2.p(*rel.split('/')), 'w'))


DS.rp(R2)
for f in R2.POST: f(R2)
for m in R2.TEXTURE_MODS:                                 # (2.99: the Seraph's block textures come by TEXTURE_MODS)
    for k, im in m.textures().items(): im.save(R2.p('assets', 'bm', 'textures', 'block', f'{k}.png'))
tex, model = DA.helm_json()
for k, im in tex.items(): im.save(R2.p('assets', 'bm', 'textures', 'block', f'{k}.png'))
R2.wj('assets/bm/models/item/dread_helm.json', model)
imgs = []
for name, label in (('dread_helm', 'Dread Visage'), ('seraph_helm', "Seraph's Gaze")):
    for view, sub in (((180, 8), 'front'), ((145, 18), '3/4'), ('front', 'behind')):     # (a fixed item faces back: 'front' is its back)
        s = K.multi_scene(tmp, K.REAL_RP)
        s.display(f'bm:item/{name}', pos=(0, 0, 0))
        imgs.append(K.label(s.render(view, size=260, span=1.7, center=(0, 0.25, 0)), label, sub))
def flat(path, label, sub, scale=6):
    im = Image.open(path).convert('RGBA'); im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    bg = Image.new('RGBA', (max(260, im.width), max(260, im.height)), (200, 214, 236, 255)); bg.alpha_composite(im, ((bg.width - im.width) // 2, (bg.height - im.height) // 2))
    return K.label(bg.convert('RGB'), label, sub)
E = os.path.join(tmp, 'assets', 'bm', 'textures', 'entity', 'equipment')
imgs += [flat(f'{E}/wings/dread_wings.png', 'Dread Carapace', 'wings', 4), flat(f'{E}/wings/seraph_wings.png', "Seraph's Wings", 'wings (3 tiers, eyes, fire)', 4),
         flat(f'{E}/humanoid/seraph.png', 'Seraph plate', 'body + feathered feet', 4)]
icons = DS.icons()
strip = Image.new('RGBA', (16 * 7 + 6, 18), (200, 214, 236, 255))
for i, (k, im) in enumerate(icons.items()): strip.alpha_composite(im, (i * 16 + i, 1))
imgs.append(flat_im := K.label(strip.resize((strip.width * 3, strip.height * 3), Image.NEAREST).convert('RGB'), 'sprites', ', '.join(icons)))
K.sheet(imgs, out, cols=5, title='The Dreadborne and the Seraph')
print(out)

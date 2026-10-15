"""2.79b: the seven summoning items (the raids' boss summons and the Blood Moon's gourd), from the shipped pack, 8x.
    python3 tools/preview/summons.py [out.png]"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from PIL import Image
import draftkit as K
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(K.OUT, 'summons.png')
TX = os.path.join(K.REAL_RP, 'assets', 'bm', 'textures', 'item')
ITEMS = [('sum_horseman', "Horseman's Lantern", 'the Headless Horseman'), ('sum_pharaoh', "Pharaoh's Scarab", 'the Sand Pharaoh'),
         ('sum_roc', 'Thunderhead Feather', 'the Storm Roc'), ('sum_treant', 'Elder Acorn', 'the Elder Treant'),
         ('sum_colossus', 'Smouldering Idol', 'the Magma Colossus (Nether)'), ('sum_voidwalker', 'Starless Eye', 'the Voidwalker (End)'),
         ('sum_lantern', 'Smouldering Gourd', 'the Arachno-Lantern (Blood Moon heists)')]
tiles = []
for iid, nm, sub in ITEMS:
    t = Image.new('RGB', (300, 300), (198, 216, 236))
    ic = Image.open(os.path.join(TX, iid + '.png')).convert('RGBA').resize((192, 192), Image.NEAREST)
    t.paste(ic, (54, 70), ic)
    tiles.append(K.label(t, nm, 'calls ' + sub))
K.sheet(tiles, out, cols=4, title='Boss summons')
print(out)

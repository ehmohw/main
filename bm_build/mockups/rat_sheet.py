"""Preview sheet of the 2.55 rat poses (renders from the built resource pack): python3 mockups/rat_sheet.py out.png [variants...]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.render import Scene
from PIL import Image, ImageDraw
import phase64
RP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'out_p2', 'BlackMarket_RP')
J = phase64.jobs()
vs = sys.argv[2:] or list(J)
rows = []
for v in vs:
    names = ['walk1', 'walk2', 'walk3', 'groom1', 'scratch1', 'look_l', 'blink'] + list(J[v][1])[:5] if v in J else []
    tiles = []
    for n in names:
        s = Scene(rp=RP)
        s.display(f'bm:item/rat3dq_{v}_{n}', translation=(0, 0.5, 0))
        im = s.render('iso', size=200, span=1.7, center=(0, 0.6, 0))
        ImageDraw.Draw(im).text((4, 4), f'{v} {n}', fill=(0, 0, 0)); tiles.append(im)
    row = Image.new('RGB', (200 * 12, 200), 'white')
    for i, t in enumerate(tiles): row.paste(t, (i * 200, 0))
    rows.append(row)
out = Image.new('RGB', (2400, 200 * len(rows)), 'white')
for i, r in enumerate(rows): out.paste(r, (0, i * 200))
out.save(sys.argv[1])

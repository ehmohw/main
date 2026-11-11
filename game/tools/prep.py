"""Pack the demo's art into the Godot project and write scripts/manifest.gd.

    python3 prep.py <generated art folder> <game folder>

The generated folder holds what the request scripts made:
    gen64/<who>/Idle/...        characters from cast64.py and foes64.py
    env/*.png, env/ts_*.json    props and ground tilesets from env64.py
    font/<name>/package/...     Tiny5 and Press Start 2P (SIL Open Font License), from the npm packages @fontsource/tiny5
                                and @fontsource/press-start-2p
"""
import sys, os, re, glob, shutil, json, base64, io
from PIL import Image

S, G = sys.argv[1], sys.argv[2]
HEROES = ('emma', 'leo', 'bender', 'cecil')
FOES = ('lantern', 'stalker', 'brood')
DIRS = ('south', 'east', 'north', 'west')

# ---------------------------------------------------------------- characters
data = {}
shutil.rmtree(f'{G}/assets/chars', ignore_errors=True)
for who in HEROES + FOES:
    src = f'{S}/gen64/{who}/Idle'
    if not os.path.isdir(src):
        src = f'{S}/gen64/{who}/' + os.listdir(f'{S}/gen64/{who}')[0] if os.path.isdir(f'{S}/gen64/{who}') else ''
    if not os.path.isdir(src):
        print('missing', who); continue
    out = f'{G}/assets/chars/{who}'
    anims = {}
    def put(anim, files):
        os.makedirs(f'{out}/{anim}', exist_ok=True)
        for i, f in enumerate(files): shutil.copy(f, f'{out}/{anim}/{i}.png')
        anims[anim] = len(files)
    for d in DIRS:
        put(f'idle_{d}', [f'{src}/rotations/{d}.png'])       # everyone stands still on their rotation art
    for folder in sorted(glob.glob(f'{src}/animations/*')):
        name = re.sub(r'-[0-9a-f]{8}$', '', os.path.basename(folder))    # directions requested one at a time come back as walk-1a2b3c4d
        for d in DIRS:
            frames = sorted(glob.glob(f'{folder}/{d}/*.png'))
            if frames: put(f'{name}_{d}', frames)
    im = Image.open(f'{src}/rotations/south.png').convert('RGBA'); bb = im.getbbox()
    side = min(24, bb[2] - bb[0] + 2, im.width)
    cx = (bb[0] + bb[2]) // 2
    head = [max(0, min(im.width - side, cx - side // 2)), max(0, bb[1] - 1), side, side]
    data[who] = {'foot': round(bb[3] - im.height / 2 - 1), 'size': im.width, 'head': head, 'anims': anims}
    print(who, im.size, 'bbox', bb, len(anims), 'animations')

# ---------------------------------------------------------------- props (cropped to their content)
shutil.rmtree(f'{G}/assets/props', ignore_errors=True); os.makedirs(f'{G}/assets/props')
for f in sorted(glob.glob(f'{S}/env/*.png')):
    name = os.path.basename(f)[:-4]
    if name.startswith(('forest', 'tilesets', 'ts_')): continue
    im = Image.open(f).convert('RGBA')
    if name == 'web':            # drawn on a dark disc: keep only the silk
        px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                r, g, b, a = px[x, y]
                if max(r, g, b) < 120: px[x, y] = (0, 0, 0, 0)
    bb = im.getbbox()
    if bb: im = im.crop(bb)
    im.save(f'{G}/assets/props/{name}.png')

# ---------------------------------------------------------------- ground tiles
# Each sheet is 4 x 5 tiles of 32px. Rows 0-3: the sixteen corner tiles, at index = NW*1 + NE*2 + SW*4 + SE*8, where a
# set bit means that corner is the sheet's HIGHER terrain (sea < sand < forest < path). Row 4: mirrored copies of the two
# plain tiles (low flipped across, low flipped down, high flipped across, high flipped down) to break up repetition.
SHEETS = {'sea_sand': ('ts_sea', 'upper'), 'sand_forest': ('ts_beach_c', 'upper'),
          'forest_path': ('ts_forest', 'lower')}      # the forest set came back with its two terrains the other way round
shutil.rmtree(f'{G}/assets/tiles', ignore_errors=True); os.makedirs(f'{G}/assets/tiles')
for sheet, (src, high) in SHEETS.items():
    t = json.load(open(f'{S}/env/{src}.json'))
    out = Image.new('RGBA', (4 * 32, 5 * 32))
    plain = {}
    for tl in t['tileset']['tiles']:
        c = tl['corners']
        m = (1 if c['NW'] == high else 0) | (2 if c['NE'] == high else 0) | (4 if c['SW'] == high else 0) | (8 if c['SE'] == high else 0)
        im = Image.open(io.BytesIO(base64.b64decode(tl['image']['base64']))).convert('RGBA')
        out.paste(im, ((m % 4) * 32, (m // 4) * 32))
        if m in (0, 15): plain[m] = im
    for i, (m, flip) in enumerate(((0, Image.FLIP_LEFT_RIGHT), (0, Image.FLIP_TOP_BOTTOM), (15, Image.FLIP_LEFT_RIGHT), (15, Image.FLIP_TOP_BOTTOM))):
        out.paste(plain[m].transpose(flip), (i * 32, 4 * 32))
    out.save(f'{G}/assets/tiles/{sheet}.png')

# ---------------------------------------------------------------- small icons, drawn here
def icon(rows, palette, path):
    im = Image.new('RGBA', (len(rows[0]), len(rows)), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != '.': im.putpixel((x, y), tuple(int(palette[ch][i:i + 2], 16) for i in (1, 3, 5)) + (255,))
    im.save(path)
os.makedirs(f'{G}/assets/ui', exist_ok=True)
icon(['....1....', '...121...', '...121...', '..12321..', '..12321..', '.1233321.', '.1233321.', '.1233321.', '..12321..', '...111...'],
     {'1': '#16356a', '2': '#4aa8ff', '3': '#d8f6ff'}, f'{G}/assets/ui/ember.png')
icon(['.11...11.', '1221.1221', '123212221', '122222221', '.1222221.', '..12221..', '...121...', '....1....'],
     {'1': '#5a1020', '2': '#e8404e', '3': '#ff9aa0'}, f'{G}/assets/ui/heart.png')

# ---------------------------------------------------------------- fonts
shutil.rmtree(f'{G}/assets/fonts', ignore_errors=True); os.makedirs(f'{G}/assets/fonts')
for name in ('tiny5', 'press-start-2p'):
    shutil.copy(f'{S}/font/{name}/package/files/{name}-latin-400-normal.woff2', f'{G}/assets/fonts/{name}.woff2')
    shutil.copy(f'{S}/font/{name}/package/LICENSE', f'{G}/assets/fonts/LICENSE-{name}.txt')

with open(f'{G}/scripts/manifest.gd', 'w') as f:
    f.write('class_name Manifest\n## Generated by tools/prep.py: frame counts, foot offsets and head crops for every sprite set.\n\nconst DATA := ' + json.dumps(data, indent='\t') + '\n')
print('packed')

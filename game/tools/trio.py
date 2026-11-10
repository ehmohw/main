"""Leo and Bender for the demo, matching the Emma test (PixelLab). python3 trio.py <pl dir> <out dir> <owner art dir> <who>"""
import sys, io, zipfile, urllib.request, os
sys.path.insert(0, sys.argv[1]); import pl
from PIL import Image
OUT, ART, WHO = sys.argv[2], sys.argv[3], sys.argv[4]
EMMA = 'eeeafe46-1825-4e5f-9f88-fea154bae941'
STYLE = 'vibrant cartoon pixel art: bold dark outlines, bright saturated colours, soft cel shading with crisp highlights'
DIRS = ['south', 'east', 'north', 'west']
if WHO == 'leo':
    im = Image.open(os.path.join(ART, 'leo.png')).convert('RGBA'); im.thumbnail((1024, 1024))
    body = {'description': "Leo, a young knight of 17: warm brown skin, green eyes, short dark hair, a silver open-faced helmet with a small spike on top; "
            "silver shoulder pauldrons and gorget, grey chainmail sleeves, silver gauntlets; a light-blue tunic with a pale teardrop emblem holding a pink gem, "
            "a brown belt with a silver buckle, grey leggings with silver knee plates and silver sabatons; earnest and determined",
            'image_size': {'width': 128, 'height': 128}, 'method': 'create_from_concept', 'concept_image': pl.b64(im), 'view': 'low top-down',
            'template_id': 'mannequin', 'style_character_id': EMMA, 'style_description': STYLE, 'seed': 1111, 'no_background': True}
    anims = [('idle', 'standing at attention, breathing gently', 4, ['south']), ('walk', 'marching forward steadily', 8, DIRS)]
else:
    body = {'description': "Bender, a friendly tan dog: short tan fur, big upright pointed ears, a black muzzle, a white chest and white paws, a dark collar, a wagging tail",
            'image_size': {'width': 64, 'height': 64}, 'method': 'create_with_style', 'view': 'low top-down', 'template_id': 'dog',
            'style_description': STYLE, 'seed': 1111, 'no_background': True}
    anims = [('idle', 'standing, panting happily, tail wagging', 4, ['south']), ('walk', 'trotting forward', 8, DIRS)]
r = pl.post('/create-character-pro', body); print(WHO, r, flush=True)
print('char', pl.wait(r['background_job_id']).get('status'), flush=True)
cid = r['character_id']
for name, act, n, dirs in anims:
    a = pl.post('/characters/animations', {'character_id': cid, 'mode': 'v3', 'action_description': act, 'animation_name': name,
                                           'frame_count': n, 'directions': dirs, 'seed': 1111})
    for b in a.get('background_job_ids', []):
        print(name, pl.wait(b).get('status'), flush=True)
with urllib.request.urlopen(f'{pl.API}/characters/{cid}/zip', timeout=300) as f:
    zipfile.ZipFile(io.BytesIO(f.read())).extractall(os.path.join(OUT, WHO))
print('done', WHO, cid, flush=True)

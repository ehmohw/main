"""Enemies in the cast's 64px style (PixelLab). python3 foes64.py <pl dir> <out dir> <owner art dir> <who>"""
import sys, io, os, time, zipfile, urllib.request, shutil
sys.path.insert(0, sys.argv[1]); import pl
from PIL import Image
OUT, ART, WHO = sys.argv[2], sys.argv[3], sys.argv[4]
EMMA = 'c66e0ee8-656d-4dda-99c4-f55befef52ff'
STYLE = 'clean 16-bit RPG pixel art sprite, bold dark outline, bright saturated colours, simple readable shapes, light shading'
DIRS = ['south', 'east', 'north', 'west']
FOES = {  # name: (concept, size, template, description, [(animation, action, frames)])
 'lantern': ('lantern.png', 64, 'custom', "an Arachno-Lantern, a spider with a carved jack-o-lantern pumpkin for a body: an orange pumpkin with an evil glowing carved face, a green stem on top, eight long black spindly legs",
             [('walk', 'scuttling forward on its eight legs', 8), ('attack', 'lunging forward to bite, legs spread', 6)]),
 'stalker': ('stalker.png', 64, 'mannequin', "a Stalker, a gaunt hunched pale olive-green creature: a bald skull-like head with small red eyes, a huge jagged fanged mouth, pointed ears, long thin limbs with long hooked claws",
             [('walk', 'creeping forward, hunched, claws hanging low', 8), ('attack', 'lunging and raking forward with long claws', 6)]),
 'brood': ('lantern.png', 128, 'custom', "the Brood Lantern, a huge monstrous spider queen with a giant rotting carved jack-o-lantern pumpkin for a body: a wide jagged glowing grin, burning eyes, a crown of twisted vines and candles on top, "
           "clusters of small glowing egg sacs on its back, eight thick black hairy legs",
           [('walk', 'crawling forward heavily on its eight legs', 8), ('attack', 'rearing up and spitting fire from its mouth', 8)]),
}
def post(path, body):
    for attempt in range(60):
        try: return pl.post(path, body)
        except Exception as e:
            if '429' in str(e) or '502' in str(e) or '503' in str(e): time.sleep(12); continue
            raise
    raise RuntimeError('gave up ' + path)
concept, size, template, desc, anims = FOES[WHO]
im = Image.open(os.path.join(ART, concept)).convert('RGBA'); im.thumbnail((1024, 1024))
body = {'description': desc, 'image_size': {'width': size, 'height': size}, 'method': 'create_from_concept', 'concept_image': pl.b64(im), 'view': 'low top-down',
        'template_id': template, 'style_character_id': EMMA, 'style_description': STYLE, 'seed': 1164, 'no_background': True}
if os.environ.get('CID'): cid = os.environ['CID']
else:
    r = post('/create-character-pro', body); print(WHO, r.get('character_id'), flush=True)
    print('char', pl.wait(r['background_job_id']).get('status'), flush=True); cid = r['character_id']
for name, act, n in anims:
    jobs = []
    for d in DIRS:
        try:
            a = post('/characters/animations', {'character_id': cid, 'mode': 'v3', 'action_description': act, 'animation_name': name, 'frame_count': n, 'directions': [d], 'seed': 1164})
            jobs += a.get('background_job_ids', [])
        except Exception as e: print('anim failed', name, d, str(e)[:200], flush=True)
    for b in jobs: print(name, pl.wait(b).get('status'), flush=True)
dest = os.path.join(OUT, WHO); shutil.rmtree(dest, ignore_errors=True)
with urllib.request.urlopen(f'{pl.API}/characters/{cid}/zip', timeout=300) as f:
    zipfile.ZipFile(io.BytesIO(f.read())).extractall(dest)
print('done', WHO, cid, flush=True)

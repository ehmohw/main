"""The cast at 64px for the demo, with cutscene emotes (PixelLab).
python3 cast64.py <pl dir> <out dir> <owner art dir> <who> [style character id]"""
import sys, io, os, json, zipfile, urllib.request, base64
sys.path.insert(0, sys.argv[1]); import pl
from PIL import Image
OUT, ART, WHO = sys.argv[2], sys.argv[3], sys.argv[4]
STYLE_CHAR = sys.argv[5] if len(sys.argv) > 5 else None
STYLE = 'clean 16-bit RPG pixel art sprite, bold dark outline, bright saturated colours, simple readable shapes, light shading'
DIRS = ['south', 'east', 'north', 'west']
CAST = {
 'emma': ('emma.png', "Emma, a cheerful 16 year old girl: brown hair in a high ponytail tied with a pink bow, a curl by each ear, freckles, big teal eyes; "
          "a long-sleeved blue dress with a light-blue scarf collar and a pink flower brooch, a brown belt with a white oval buckle, a full knee-length blue skirt, white knee socks, navy mary-jane shoes"),
 'leo': ('leo.png', "Leo, a young knight of 17: warm brown skin, green eyes, short dark hair, a silver open-faced helmet with a small spike on top; silver shoulder pauldrons, "
         "grey chainmail sleeves, silver gauntlets; a light-blue tunic with a teardrop emblem holding a pink gem, a brown belt, grey leggings, silver boots"),
 'bender': (None, "Bender, a friendly tan dog: short tan fur, big upright pointed ears, a black muzzle, a white chest and white paws, a dark collar, a wagging tail"),
 'cecil': ('cecil.png', "Cecil, a small hunched hooded mage: a deep purple hooded robe with a ragged hem, a shadowed black face with two glowing yellow eyes and a jagged grin, "
           "black clawed hands, carrying a wooden staff topped with a gold crescent holding a glowing pink crystal"),
}
# cutscene emotes: (name, what happens, frames)
EMOTES = {
 'emma': [('cheer', 'jumping for joy with both arms raised, beaming', 8), ('cry', 'crying, head bowed, wiping tears from her eyes with her hands', 8),
          ('scared', 'gasping and flinching backward in fear, arms pulled in', 6), ('angry', 'furious, fists clenched at her sides, stamping her foot', 8),
          ('think', 'thinking hard, one hand on her chin, looking up, then nodding as she remembers', 8), ('hurt', 'clutching her wounded arm, wincing, sinking to one knee', 8)],
 'leo': [('guard', 'stepping forward and raising his arms wide to shield someone behind him', 6), ('hurt', 'clutching his side in pain, dropping to one knee', 8),
         ('kneel', 'kneeling down gently to tend a wound, hands working carefully', 8), ('salute', 'standing tall and saluting with a fist over his heart', 6)],
 'bender': [('bark', 'barking excitedly, tail wagging', 6), ('whine', 'whimpering, ears down, head lowered sadly', 6)],
 'cecil': [('scoff', 'shaking his head and waving a dismissive hand, annoyed', 8), ('rage', 'slamming the butt of his staff on the ground in anger', 8)],
}
FACES = {'happy': 'a big joyful open-mouthed smile, bright eyes', 'sad': 'crying, tears running down the cheeks, eyebrows raised, mouth trembling',
         'angry': 'furious, eyebrows drawn down hard, teeth gritted', 'scared': 'terrified, wide eyes with tiny pupils, mouth open in a gasp, sweat drop',
         'determined': 'determined, a firm confident frown, steady eyes'}

def find_images(o, out):
    if isinstance(o, dict):
        if o.get('base64') or (o.get('url') and str(o.get('url')).startswith('http')): out.append(o)
        else:
            for v in o.values(): find_images(v, out)
    elif isinstance(o, list):
        for v in o: find_images(v, out)
    return out

concept, desc = CAST[WHO]
if concept:
    im = Image.open(os.path.join(ART, concept)).convert('RGBA'); im.thumbnail((1024, 1024))
    body = {'description': desc, 'image_size': {'width': 64, 'height': 64}, 'method': 'create_from_concept', 'concept_image': pl.b64(im),
            'view': 'low top-down', 'template_id': 'mannequin', 'style_description': STYLE, 'seed': 1164, 'no_background': True}
else:       # Bender has no drawing yet: from words, and smaller, so a dog stands knee-high beside the others
    body = {'description': desc, 'image_size': {'width': 48, 'height': 48}, 'method': 'create_with_style',
            'view': 'low top-down', 'template_id': 'dog', 'style_description': STYLE, 'seed': 1164, 'no_background': True}
    STYLE_CHAR = None
if STYLE_CHAR: body['style_character_id'] = STYLE_CHAR
if os.environ.get('CID'):
    cid = os.environ['CID']
else:
    r = pl.post('/create-character-pro', body); print(WHO, r.get('character_id'), flush=True)
    print('char', pl.wait(r['background_job_id']).get('status'), flush=True)
    cid = r['character_id']
jobs = []
def animate(name, act, n, dirs):
    try:
        a = pl.post('/characters/animations', {'character_id': cid, 'mode': 'v3', 'action_description': act, 'animation_name': name,
                                               'frame_count': n, 'directions': dirs, 'seed': 1164})
        jobs.extend((name, b) for b in a.get('background_job_ids', []))
    except Exception as e:
        print('anim failed', name, str(e)[:200], flush=True)
def drain():
    for name, b in jobs: print(name, pl.wait(b).get('status'), flush=True)
    jobs.clear()
ONLY = os.environ.get('ONLY', '')            # e.g. ONLY=hurt,faces with CID=<character id> to redo parts
if not ONLY or 'walk' in ONLY.split(','):
    animate('walk', 'walking forward', 8, DIRS); drain()
for i, (name, act, n) in enumerate(EMOTES.get(WHO, [])):
    if ONLY and name not in ONLY.split(','): continue
    animate(name, act, n, ['south'])
    if i % 4 == 3: drain()                   # only so many jobs may run at once
drain()
dest = os.path.join(OUT, WHO)
import shutil; shutil.rmtree(os.path.join(dest, 'Idle'), ignore_errors=True)
with urllib.request.urlopen(f'{pl.API}/characters/{cid}/zip', timeout=300) as f:
    zipfile.ZipFile(io.BytesIO(f.read())).extractall(dest)
print('sprites done', WHO, cid, flush=True)
print('done', WHO, cid, flush=True)

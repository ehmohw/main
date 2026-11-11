"""Environment art for the demo (PixelLab): chained ground tilesets and props in the cast's simpler style.
python3 env64.py <pl dir> <out dir> [only-name ...]"""
import sys, os, json, time
sys.path.insert(0, sys.argv[1]); import pl
OUT = sys.argv[2]; ONLY = sys.argv[3:]
os.makedirs(OUT, exist_ok=True)
ST = 'clean 16-bit RPG pixel art, bold dark outline, simple readable shapes, limited palette, game asset on a plain background'
def post(path, body):
    for attempt in range(40):
        try: return pl.post(path, body)
        except Exception as e:
            if '429' in str(e) or '502' in str(e) or '503' in str(e): time.sleep(10); continue
            raise
    raise RuntimeError('gave up ' + path)

# ---- ground: three tilesets that share terrains, so they join without a seam
def tileset(name, lower, upper, **extra):
    f = os.path.join(OUT, name + '.json')
    if os.path.exists(f): return json.load(open(f))
    r = post('/create-tileset', dict({'lower_description': lower, 'upper_description': upper, 'tile_size': {'width': 32, 'height': 32}, 'mode': 'standard',
                                      'shading': 'basic shading', 'detail': 'medium detail', 'raggedness': 0.3, 'seed': 1164}, **extra))
    print(name, pl.wait(r['background_job_id']).get('status'), flush=True)
    t = pl.get('/tilesets/' + r['tileset_id']); json.dump(t, open(f, 'w')); return t
if not ONLY or 'tiles' in ONLY:
    SAND = 'pale sandy beach with a few shells and pebbles'
    forest = tileset('ts_forest', 'dark mossy forest floor, short grass, dead leaves, at dusk', 'worn bare dirt footpath, packed earth, a few pebbles')
    # (this set came back with its two looks swapped: its all-"upper" tile is the dark leafy floor, and prep.py reads it that way)
    floor = [t for t in forest['tileset']['tiles'] if all(v == 'upper' for v in t['corners'].values())][0]['image']
    sea = tileset('ts_sea', 'deep dark blue sea water with gentle waves at dusk', SAND)
    sand = sea['metadata']['terrain_ids']['upper']
    # sand to forest: the sand is the sea set's own tile, and the forest floor is drawn to match a picture of the forest set's.
    # (Passing the forest floor's tile id as well gave a set with stray grey tiles.)
    tileset('ts_beach_c', SAND, 'dark forest floor covered in dead brown leaves, at dusk', lower_base_tile_id=sand, upper_reference_image=floor, seed=1165)

P = {  # name: (what, width, height, outline)
 'tree_a': ('a tall gnarled dead tree with twisted bare branches, dark purple-grey bark', 96, 128, 1), 'tree_b': ('a dark twisted pine tree with drooping blue-green needles', 96, 128, 1),
 'tree_c': ('a large old oak tree with a thick trunk and a dark teal leafy canopy, spooky forest', 96, 128, 1),
 'bush_a': ('a small dark green thorny bush', 32, 32, 1), 'bush_b': ('a small round dark bush with purple berries', 32, 32, 1),
 'stump': ('a mossy tree stump', 32, 32, 1), 'log': ('a fallen mossy log lying on the ground', 64, 32, 1),
 'rock_a': ('a mossy grey boulder', 32, 32, 1), 'rock_b': ('a large cracked grey boulder with glowing purple mushrooms at its base', 48, 48, 1),
 'shrooms': ('a cluster of small glowing purple mushrooms', 32, 32, 1), 'pumpkin': ('a carved jack-o-lantern pumpkin glowing orange from inside', 32, 32, 1),
 'eggsac': ('a spider egg sac cocoon wrapped in white webbing, faintly glowing orange from inside', 48, 48, 1),
 'web': ('a round spider web stretched flat on the ground, white silk threads, seen from directly above', 64, 64, 0),
 'web_post': ('a tall wooden post wrapped in thick white spider webs', 32, 64, 1),
 'wreck_hull': ('the huge splintered bow of a large wooden sailing ship, wrecked and lying tilted on its side, broken ribs and planks, a snapped mast stump and torn sail, '
                'the ship fills the whole image, no ground, no sand, no water', 192, 128, 1),
 'wreck_mast': ('a broken wooden ship mast lying on the ground with a torn white sail and rope', 96, 48, 1),
 'crate': ('a wooden cargo crate', 32, 32, 1), 'barrel': ('a wooden barrel lying on its side', 32, 32, 1), 'driftwood': ('a few pieces of broken ship planks and driftwood', 48, 32, 1),
 'lamp_post': ('an old iron lamp post with a glowing orange lantern', 32, 64, 1), 'bones': ('a small pile of old bones and a skull', 32, 32, 1),
 'gate': ('a tall ornate wrought-iron palace gate between two stone pillars topped with glowing lanterns, front view', 128, 128, 1),
 'chest': ('a wooden treasure chest with gold trim', 32, 32, 1),
 'tuft_a': ('a small tuft of dark green grass', 32, 32, 0), 'tuft_b': ('a few small white wildflowers in grass', 32, 32, 0),
 'leaves': ('a small scatter of orange and brown fallen leaves on the ground, seen from above', 32, 32, 0), 'pebbles': ('a few small grey pebbles on the ground, seen from above', 32, 32, 0),
 'shell': ('a pink seashell and a starfish on the ground, seen from above', 32, 32, 0),
}
for n, (d, w, h, outline) in P.items():
    if ONLY and n not in ONLY and 'props' not in ONLY: continue
    f = os.path.join(OUT, n + '.png')
    if os.path.exists(f): continue
    r = post('/create-image-pixflux', {'description': f'{d}, {ST}', 'image_size': {'width': w, 'height': h}, 'no_background': True, 'view': 'low top-down',
         'outline': 'single color black outline' if outline else 'lineless', 'shading': 'basic shading', 'detail': 'medium detail', 'seed': 1164})
    pl.img(r['image']).save(f); print(n, flush=True)
print('done', flush=True)

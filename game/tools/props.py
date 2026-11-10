import sys, os
sys.path.insert(0, sys.argv[1]); import pl
OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
ST = 'dark fantasy pixel art, bold dark outline, top-down RPG game asset'
P = {'tree1': ('a tall gnarled dead tree with twisted bare black branches and a thick trunk, dark purple-grey bark', 128, 160),
     'tree2': ('a dark twisted pine tree with drooping blue-black needles, spooky forest', 128, 160),
     'rock': ('a mossy grey boulder with a few glowing purple mushrooms at its base', 64, 64),
     'eggsac': ('a spider egg sac cocoon wrapped in white webbing, faintly glowing orange from inside', 64, 64),
     'pumpkin': ('a small carved jack-o-lantern pumpkin glowing orange from inside, on the ground', 48, 48),
     'chest': ('a wooden treasure chest with gold trim, closed, front view from above', 64, 64),
     'ember': ('a small glowing blue-white soul flame wisp, game pickup icon', 32, 32),
     'heart': ('a red heart, game pickup icon', 32, 32),
     'web': ('a large spider web stretched flat on the ground, white silk threads, seen from above', 128, 128)}
import time
for n, (d, w, h) in P.items():
  if os.path.exists(os.path.join(OUT, n + '.png')): continue
  for attempt in range(4):
   try:
    r = pl.post('/create-image-pixflux', {'description': f'{d}, {ST}', 'image_size': {'width': w, 'height': h}, 'no_background': True,
     'view': 'low top-down', 'outline': 'single color black outline', 'shading': 'medium shading', 'detail': 'highly detailed', 'seed': 1111})
    pl.img(r['image']).save(os.path.join(OUT, n + '.png')); print(n, flush=True); break
   except Exception as e:
    print('retry', n, str(e)[:80], flush=True); time.sleep(8)

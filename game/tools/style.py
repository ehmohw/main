import sys, os, time
sys.path.insert(0, sys.argv[1]); import pl
OUT = sys.argv[2]
D = ("Emma, a cheerful young girl standing, facing the viewer: brown hair in a high ponytail with a pink bow, big teal eyes, "
     "a blue long-sleeved dress with a light-blue scarf collar and a pink flower brooch, a brown belt, a full knee-length blue skirt, white knee socks, navy shoes")
OPTS = {'a_32_flat': (32, 'flat shading', 'low detail', 'retro 16-bit JRPG overworld sprite, chunky pixels, very limited palette'),
        'b_48_flat': (48, 'flat shading', 'low detail', 'retro 16-bit JRPG sprite, chunky pixels, limited palette'),
        'c_48_basic': (48, 'basic shading', 'medium detail', 'classic 16-bit RPG sprite, clean readable shapes'),
        'd_64_flat': (64, 'flat shading', 'low detail', 'simple clean pixel art, bold shapes, limited palette, no gradients')}
for n, (sz, sh, det, st) in OPTS.items():
    for attempt in range(4):
        try:
            r = pl.post('/create-image-pixflux', {'description': f'{D}, {st}', 'image_size': {'width': sz, 'height': sz}, 'no_background': True,
                 'view': 'low top-down', 'direction': 'south', 'outline': 'single color black outline', 'shading': sh, 'detail': det, 'seed': 1112})
            pl.img(r['image']).save(os.path.join(OUT, n + '.png')); print(n, flush=True); break
        except Exception as e:
            print('retry', n, str(e)[:80], flush=True); time.sleep(8)

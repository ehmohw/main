"""2.95: KETTLE's playthings, asked of PixelLab (/create-image-pixflux, 64 x 64): his own toys in colour, and the pencil sketches Mr.
Capshun draws for him to play with (black and white, like Capshun's own sketches).   python3 kettle_list.py [name ...]"""
import os, sys
import pl
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'ref', 'pixellab', 'kettle')
COLOUR = 'game item icon'
SKETCH = 'hand-drawn scribbly graphite lines and cross-hatching, no colour, notebook doodle'
ICONS = {
    'plane': f'a single white folded paper airplane with crisp creases, pointing up and to the right, {COLOUR}',
    'ball': f'a single bouncy red playground rubber ball with a white stripe round it and a shine, {COLOUR}',
    'rope': f'a single jump rope: a long thin red rope in a loose loop with two small yellow wooden handles at its ends, {COLOUR}',
    'sk_ball': f'a black and white pencil sketch of a big round bouncy ball with a stripe, {SKETCH}',
    'sk_kite': f'a black and white pencil sketch of a diamond-shaped kite with a long wavy tail with little bows, {SKETCH}',
    'sk_slide': f'a black and white pencil sketch of a small playground slide with a ladder, {SKETCH}',
}
if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for n in sys.argv[1:] or ICONS:
        for seed in (294, 295):
            r = pl.post('/create-image-pixflux', {'description': ICONS[n], 'image_size': {'width': 64, 'height': 64}, 'no_background': True,
                                                  'view': 'side', 'outline': 'single color black outline', 'shading': 'medium shading',
                                                  'detail': 'highly detailed', 'seed': seed})
            pl.img(r['image']).save(os.path.join(OUT, f'{n}_{seed}.png')); print(n, seed)

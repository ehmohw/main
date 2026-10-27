"""2.95: the Gem of Creativity's sparkles, asked of PixelLab's effects artist (/v2/vfx, lite) - saved as ref/pixellab/vfx/<name>.png/.json
like phase210's: its frames, their timing, its anchor.   python3 cg_vfx.py [name ...]"""
import json, os, sys, base64, io
import pl
from PIL import Image
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'ref', 'pixellab', 'vfx')
VFX = {
    'cg_sparkle': ("Rainbow gem sparkles: a scatter of tiny four-pointed star glints twinkles around a centre point - each pops in, flashes "
                   "white, takes one colour of the rainbow (red, orange, yellow, green, cyan, blue, violet, pink) and shrinks away, staggered "
                   "so a few are always lit. Soft and magical, about 1 second, seamless loop.", 'the Gem of Creativity, always'),
    'cg_doodles': ("Creativity drifting up: tiny hand-drawn white doodles - a music note, a little flower, a swirl, a star - float up from the "
                   "centre one after another, each trailing a short rainbow sparkle, wobbling a little, then fading out. Whimsical, "
                   "about 1.2 seconds, no loop.", 'the Gem of Creativity, now and then'),
    'cg_conjure': ("A burst of creation: a spiral of rainbow paint and glitter spins up out of a single point, blooms into a bright "
                   "multicoloured flash shaped like a star, and scatters little doodle stars and sparkles outward that fade. Joyful, "
                   "about 0.8 seconds, no loop.", 'a Buddy conjured by the Gem'),
}
if __name__ == '__main__':
    names = sys.argv[1:] or list(VFX)
    jobs = {n: pl.post('/vfx', {'description': VFX[n][0], 'artist': 'lite', 'name': n}) for n in names}
    for n, j in jobs.items():
        r = pl.wait(j['background_job_id'])
        json.dump(r, open(f'/tmp/claude-0/-home-user-main/99867ee9-8c51-5a94-9ce7-6ff9e7d41656/scratchpad/vfx_{n}.json', 'w'))
        print(n, r.get('status'), str({k: (v if not isinstance(v, (dict, list)) else type(v).__name__) for k, v in r.items()})[:400])

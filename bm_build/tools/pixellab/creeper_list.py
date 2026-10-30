"""3.0b: THE PIXEL CREEPER (phase256, px_creeper_art.py), asked of PixelLab: a character in the Arcade's style (Bit the rat trader,
c06e9b11, as the style reference; the mannequin template - the dog's made it a quadruped seen from above), then a hop, south
and north. Exported as the character's ZIP through the API (its rotation and frame URLs are on a host the proxy won't reach)
into ref/pixellab/arcade/px_creeper.
   python3 creeper_list.py          (the character, its hop, the export)
Kept: seed 301 (character 1045bf39-d8a4-4862-861a-25b8b3b2512f) - the classic face, crisp at 64 px."""
import io, os, sys, zipfile, urllib.request
import pl

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'ref', 'pixellab', 'arcade', 'px_creeper')
STYLE_CHAR = 'c06e9b11-42b0-4091-a3be-5c8f00a39d30'                 # (Bit, the 8-bit trader)
DESC = ('a tiny cute Minecraft creeper: a tall rectangular green body made of mottled green and light-green pixel squares, a square '
        'head on top with the classic creeper face (two black square eyes and a black frowning mouth), four short stubby feet, no arms')
HOP = ('a small happy hop straight up and landing in place, squashing a little on landing, feet together, the head and face stay '
       'the same', 6)


def make(seed=301):
    r = pl.post('/create-character-pro', {'description': DESC, 'image_size': {'width': 64, 'height': 64}, 'method': 'create_with_style',
                                          'view': 'low top-down', 'template_id': 'mannequin', 'style_character_id': STYLE_CHAR,
                                          'style_description': 'retro 8-bit video game pixel art, bold black outline, bright limited palette',
                                          'seed': seed, 'no_background': True})
    pl.wait(r['background_job_id'])
    a = pl.post('/characters/animations', {'character_id': r['character_id'], 'mode': 'v3', 'action_description': HOP[0], 'animation_name': 'hop',
                                           'frame_count': HOP[1], 'directions': ['south', 'north'], 'seed': 294})
    for j in a['background_job_ids']:
        pl.wait(j)
    return r['character_id']


def export(cid):
    with urllib.request.urlopen(f'{pl.API}/characters/{cid}/zip', timeout=300) as f:
        zipfile.ZipFile(io.BytesIO(f.read())).extractall(OUT)


if __name__ == '__main__':
    export(sys.argv[1] if len(sys.argv) > 1 else make())

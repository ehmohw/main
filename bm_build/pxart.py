"""2.94: PIXEL SPRITES - a character drawn by PixelLab (ref/pixellab/twins/<k>, ref/pixellab/chars/<k>: the export of a character,
its south-facing animations - south is toward you, and a billboarded sprite always faces you) made into the game's pieces:

  every frame a texture, put on one canvas (a power of two) so the character's feet stand on the same spot in every animation
    (each animation's first frame is lined up with the standing sprite's feet, the rest of it moves as drawn)
  every frame a model - one flat quad, unshaded - and one item definition that picks the frame by the display's
    custom_model_data string ("walk_3"): so a look's recoloured copy of that definition (phase138's "_c<k>") keeps every frame
  for rigpet (a sprite follower): PARTS body (nothing to see - the shadow) and head (the sprite), POSES "<anim>_<i>", a pose
    setting the frame (pose_extra), RIG_SCALE the quad's size so the character stands as tall as asked.
Pixel art stays pixel art: the frames are never resampled, only placed."""
import glob
import json
import math
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOTS = (os.path.join(HERE, 'ref', 'pixellab', 'twins'), os.path.join(HERE, 'ref', 'pixellab', 'chars'))


def folder(key):
    for r in ROOTS:
        d = os.path.join(r, key)
        if os.path.isdir(d):
            return d
    raise FileNotFoundError(key)


def _frames(d, anim):
    fs = glob.glob(os.path.join(d, '*', 'animations', anim, 'south', '*.png'))
    fs.sort(key=lambda f: int(''.join(c for c in os.path.basename(f) if c.isdigit()) or 0))
    return [Image.open(f).convert('RGBA') for f in fs]


def anims_of(key):
    d = folder(key)
    return sorted(os.path.basename(p) for p in glob.glob(os.path.join(d, '*', 'animations', '*')))


class Sprite:
    """one character: key (its PixelLab folder), prefix (its textures/models: 'pxe_'), height (blocks, standing), ANIMS {our name: (its
    animation's name, frames to keep or None)} - several of ours may share one of its"""
    def __init__(self, key, prefix, height, anims, drop=None):
        self.key, self.prefix, self.height = key, prefix, height
        d = folder(key)
        self.src = {}
        for name, (src, keep) in anims.items():
            fr = _frames(d, src)
            assert fr, (key, src)
            if keep:
                fr = [fr[i] for i in keep if i < len(fr)]
            self.src[name] = fr
        rot = Image.open(glob.glob(os.path.join(d, '*', 'rotations', 'south.png'))[0]).convert('RGBA')
        bb = rot.getbbox()
        self.px_h = bb[3] - bb[1]                                           # (the standing sprite's height in pixels)
        big = max(max(f.width, f.height) for fr in self.src.values() for f in fr)
        n = 16
        while n < big + 24:
            n *= 2
        self.N = n
        self.ppb = self.px_h / height                                        # (pixels to the block)
        self.size = n / self.ppb                                             # (the quad's side, in blocks)
        self.frames = {}
        for name, fr in self.src.items():
            b0 = fr[0].getbbox() or (0, 0, fr[0].width, fr[0].height)
            dx = int(round(n / 2 - (b0[0] + b0[2]) / 2))
            dy = int(n - 6 - b0[3])
            out = []
            for f in fr:
                c = Image.new('RGBA', (n, n), (0, 0, 0, 0))
                c.alpha_composite(f, (dx, dy))
                out.append(c)
            self.frames[name] = out

    # ------------------------------------------------------------------ the pieces
    def textures(self):
        return {f'{self.prefix}{a}_{i}': im for a, fr in self.frames.items() for i, im in enumerate(fr)}

    def frame_names(self):
        return [f'{a}_{i}' for a, fr in self.frames.items() for i in range(len(fr))]

    def quad(self, tex):
        face = {'uv': [0, 0, 16, 16], 'texture': '#f'}
        return ({'f': f'bm:block/{tex}'}, [{'from': [0, 0, 8], 'to': [16, 16, 8], 'shade': False,
                                             'faces': {'north': face, 'south': {'uv': [16, 0, 0, 16], 'texture': '#f'}}}])

    def models(self, head=None):
        """{model: (textures, elements)} - a quad per frame; and (for a rigpet follower) its empty body"""
        M = {f'{self.prefix}{fn}': self.quad(f'{self.prefix}{fn}') for fn in self.frame_names()}
        return M

    def item_def(self, R2, item, first='idle_0'):
        """the one item definition: the frame by the display's custom_model_data"""
        mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{self.prefix}{n}'}
        R2.wj(f'assets/bm/items/{item}.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                         'cases': [{'when': fn, 'model': mdl(fn)} for fn in self.frame_names()], 'fallback': mdl(first)}})

    def frame_cmd(self, sel, name):
        return f'execute as {sel} run data modify entity @s item.components."minecraft:custom_model_data" set value {{strings:["{name}"]}}'


class Rig:
    """a sprite as a rigpet art module: PARTS body (the shadow) and head (the sprite)"""
    def __init__(self, sprite, prefix):
        self.S, self.PREFIX = sprite, prefix
        self.RIG_SCALE = sprite.size
        self.PARTS = ('body', 'head')
        self.PIVOT = {'body': (0.0, 8.0, 0.0), 'head': (0.0, 8.0, 0.0)}
        self.PARENT = {'body': None, 'head': None}
        self.PART_K = {}
        self.SWIM_FRAMES = 0
        self.POSES = {fn: {'_frame': fn} for fn in sprite.frame_names()}
        self.POSES['idle_a'] = {'_frame': 'idle_0'}

    def HIDDEN(self, p, pose):
        return False

    def model_name(self, p, pose, suffix=''):
        return f'{self.PREFIX}{p}{suffix}'

    def textures(self):
        return self.S.textures()

    def models(self):
        M = dict(self.S.models())
        M[f'{self.PREFIX}body'] = ({'f': f'bm:block/{self.S.prefix}idle_0'}, [])                 # (nothing to see: it carries the shadow)
        M[f'{self.PREFIX}head'] = self.S.quad(f'{self.S.prefix}idle_0')
        return M

    def cycle(self, name, every, start=0):
        """[(tick, pose)] through an animation's frames, every few ticks"""
        return [(start + every * i, f'{name}_{i}') for i in range(len(self.S.frames[name]))]

    def length(self, name, every):
        return every * len(self.S.frames[name])

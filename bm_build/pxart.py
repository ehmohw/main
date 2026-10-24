"""2.94: PIXEL SPRITES - a character drawn by PixelLab (ref/pixellab/twins/<k>, ref/pixellab/chars/<k>: the export of a character,
its south-facing animations - south is toward you - and (2.94c) its north-facing ones, the same animations seen from behind)
made into the game's pieces:

  every frame a texture, put on one canvas (a power of two) so the character's feet stand on the same spot in every animation
    (each animation's first frame is lined up with the standing sprite's feet, the rest of it moves as drawn)
  every frame a model - one flat quad, unshaded: the front frame on its front, the back frame on its back (2.94c: it was
    billboarded, always turned to you - from above you saw its face looking up at you; now it's flat as a paper doll, turned
    as the follower is, and edge-on from the side it's a line) - and one item definition that picks the frame by the display's
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
ROOTS = (os.path.join(HERE, 'ref', 'pixellab', 'twins'), os.path.join(HERE, 'ref', 'pixellab', 'chars'), os.path.join(HERE, 'ref', 'pixellab', 'arcade'))


def folder(key):
    for r in ROOTS:
        d = os.path.join(r, key)
        if os.path.isdir(d):
            return d
    raise FileNotFoundError(key)


def _frames(d, anim, side='south'):
    fs = glob.glob(os.path.join(d, '*', 'animations', anim, side, '*.png'))
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
        place = lambda fr: (int(round(n / 2 - ((fr[0].getbbox() or (0, 0, fr[0].width, 0))[0] + (fr[0].getbbox() or (0, 0, fr[0].width, 0))[2]) / 2)),
                            int(n - 6 - (fr[0].getbbox() or (0, 0, 0, fr[0].height))[3]))
        for name, fr in self.src.items():
            dx, dy = place(fr)
            out = []
            for f in fr:
                c = Image.new('RGBA', (n, n), (0, 0, 0, 0))
                c.alpha_composite(f, (dx, dy))
                out.append(c)
            self.frames[name] = out
        # (2.94c) the backs: each animation's north frames, its feet where the front's are, frame for frame (a count that
        # differs is matched by its place in the cycle); an animation drawn only from the front gets the front's outline,
        # filled from the character's own back view - never its face
        rot_n = glob.glob(os.path.join(d, '*', 'rotations', 'north.png'))
        rot_n = Image.open(rot_n[0]).convert('RGBA') if rot_n else None
        self.backs = {}
        for name, (src, keep) in anims.items():
            fr = _frames(d, src, 'north')
            if fr and keep:
                fr = [fr[i] for i in keep if i < len(fr)]
            k = len(self.frames[name])
            if fr:
                dx, dy = place(fr)
                out = []
                for i in range(k):
                    c = Image.new('RGBA', (n, n), (0, 0, 0, 0))
                    c.alpha_composite(fr[min(len(fr) - 1, i * len(fr) // k)], (dx, dy))
                    out.append(c)
            else:
                out = [_back_of(f, rot_n) for f in self.frames[name]]
            self.backs[name] = out

    # ------------------------------------------------------------------ the pieces
    def textures(self):
        T = {f'{self.prefix}{a}_{i}': im for a, fr in self.frames.items() for i, im in enumerate(fr)}
        T.update({f'{self.prefix}b_{a}_{i}': im for a, fr in self.backs.items() for i, im in enumerate(fr)})
        return T

    def frame_names(self):
        return [f'{a}_{i}' for a, fr in self.frames.items() for i in range(len(fr))]

    def quad(self, tex, back=None):
        """a flat two-sided quad: the front frame on its north face (rigkit's front: design -z, the way the follower faces), the
        back frame on its south face - each seen the right way round from its own side"""
        return ({'f': f'bm:block/{tex}', 'b': f'bm:block/{back or tex}'},
                [{'from': [0, 0, 8], 'to': [16, 16, 8], 'shade': False,
                  'faces': {'north': {'uv': [0, 0, 16, 16], 'texture': '#f'},
                            'south': {'uv': [0, 0, 16, 16] if back else [16, 0, 0, 16], 'texture': '#b'}}}])

    def models(self, head=None):
        """{model: (textures, elements)} - a quad per frame; and (for a rigpet follower) its empty body"""
        return {f'{self.prefix}{fn}': self.quad(f'{self.prefix}{fn}', f'{self.prefix}b_{fn}') for fn in self.frame_names()}

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
        y = 8.0 - 96.0 / sprite.N                                             # (the quad's middle, so the feet - 6 pixels up the canvas - touch the ground)
        self.PIVOT = {'body': (0.0, y, 0.0), 'head': (0.0, y, 0.0)}
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
        M[f'{self.PREFIX}head'] = self.S.quad(f'{self.S.prefix}idle_0', f'{self.S.prefix}b_idle_0')
        return M

    def cycle(self, name, every, start=0):
        """[(tick, pose)] through an animation's frames, every few ticks"""
        return [(start + every * i, f'{name}_{i}') for i in range(len(self.S.frames[name]))]

    def length(self, name, every):
        return every * len(self.S.frames[name])


# ---------------------------------------------------------------------- a doll: the standing sprite, chibi, in voxels
def chibi(im, split=0.46, kh=1.3, kb=0.8):
    """the sprite pushed into the dolls' proportions: the head (the top of it) a third bigger, the body smaller - by whole
    pixels (nearest), so it stays pixel art"""
    bb = im.getbbox(); im = im.crop(bb)
    w, h = im.size
    hs = int(round(h * split))
    head = im.crop((0, 0, w, hs)); body = im.crop((0, hs, w, h))
    head = head.resize((max(1, round(w * kh)), max(1, round(hs * kh))), Image.NEAREST)
    body = body.resize((max(1, round(w * kb)), max(1, round((h - hs) * kb))), Image.NEAREST)
    W = max(head.width, body.width)
    out = Image.new('RGBA', (W, head.height + body.height), (0, 0, 0, 0))
    out.alpha_composite(body, ((W - body.width) // 2, head.height))
    out.alpha_composite(head, ((W - head.width) // 2, 0))
    return out


def _back(im, back):
    """the back view lined up behind the front, column for column: mirrored (seen from behind, left is right), its outline
    moved onto the front's, and every front pixel it doesn't cover filled from the nearest back pixel in its row (so the back
    has no holes, and nothing of the face shows through)"""
    b = back.transpose(Image.FLIP_LEFT_RIGHT); bb = b.getbbox(); b = b.crop(bb)
    w, h = im.size
    c = Image.new('RGBA', (w, h), (0, 0, 0, 0)); c.alpha_composite(b, ((w - b.width) // 2, h - b.height))   # (feet to feet, centred)
    fa, cp = im.load(), c.load()
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0)); op = out.load()
    for y in range(h):
        solid = [x for x in range(w) if cp[x, y][3] >= 128]
        for x in range(w):
            if fa[x, y][3] < 128: continue
            if cp[x, y][3] >= 128: op[x, y] = cp[x, y]
            elif solid: op[x, y] = cp[min(solid, key=lambda q: abs(q - x)), y]
            else:                                     # (a row the back doesn't reach: the nearest row it does)
                yy = min((r for r in range(h) if any(cp[q, r][3] >= 128 for q in range(w))), key=lambda r: abs(r - y))
                op[x, y] = cp[min((q for q in range(w) if cp[q, yy][3] >= 128), key=lambda q: abs(q - x)), yy]
    return out


def _back_of(front, rot_n):
    """a back for a frame drawn only from the front: its outline, filled from the back view (the front mirrored, if none)"""
    if rot_n is None:
        return front.transpose(Image.FLIP_LEFT_RIGHT)
    bb = front.getbbox()
    if not bb:
        return front.copy()
    out = Image.new('RGBA', front.size, (0, 0, 0, 0))
    out.alpha_composite(_back(front.crop(bb), rot_n), (bb[0], bb[1]))
    return out.transpose(Image.FLIP_LEFT_RIGHT)


def voxel(im, tex, height=18.0, depth=1.6, back=None):
    """(textures, elements, the square texture) - every row's runs of solid pixels a box, the sprite on its front (north, as
    the dolls face) and on its back (the back view, if given - 2.94b: else the front again, so a hooded face showed on the back
    of the hood), its edge pixels on the sides: a pixel doll you can walk round"""
    bb = im.getbbox(); im = im.crop(bb)
    w, h = im.size
    n = 16
    while n < max(w, h) or (back is not None and n < 2 * w):
        n *= 2
    sq = Image.new('RGBA', (n, n), (0, 0, 0, 0)); sq.alpha_composite(im, (0, 0))
    bx = 0
    if back is not None:                              # (the back beside the front on the texture)
        bx = n // 2; sq.alpha_composite(_back(im, back), (bx, 0))
    s = height / h                                    # (model units a pixel)
    u = 16.0 / n                                      # (uv units a pixel)
    ox = 8 + w * s / 2                                # (column 0 at the east edge: the north face shows it on your left)
    a = im.split()[3].load()
    els = []
    for y in range(h):
        x = 0
        while x < w:
            if a[x, y] < 128:
                x += 1; continue
            x0 = x
            while x < w and a[x, y] >= 128:
                x += 1
            v0, v1 = y * u, (y + 1) * u
            f = [round(ox - x * s, 3), round((h - 1 - y) * s, 3), round(8 - depth / 2, 3)]
            t = [round(ox - x0 * s, 3), round((h - y) * s, 3), round(8 + depth / 2, 3)]
            row = lambda c0, c1: [round(c0 * u, 4), v0, round(c1 * u, 4), v1]
            els.append({'from': f, 'to': t, 'faces': {
                'north': {'uv': row(x0, x), 'texture': '#t'}, 'south': {'uv': row(bx + x, bx + x0), 'texture': '#t'},
                'up': {'uv': row(x0, x), 'texture': '#t'}, 'down': {'uv': row(x0, x), 'texture': '#t'},
                'east': {'uv': row(x0, x0 + 1), 'texture': '#t'}, 'west': {'uv': row(x - 1, x), 'texture': '#t'}}})
    return {'t': f'bm:block/{tex}', 'particle': f'bm:block/{tex}'}, els, sq


def standing(key, side='south'):
    d = folder(key)
    return Image.open(glob.glob(os.path.join(d, '*', 'rotations', f'{side}.png'))[0]).convert('RGBA')


def turned(els):
    """elements turned half round (about the model's middle): a doll made facing one way, facing the other"""
    sw = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east', 'up': 'up', 'down': 'down'}
    out = []
    for e in els:
        f, t = e['from'], e['to']
        out.append({'from': [round(16 - t[0], 3), f[1], round(16 - t[2], 3)], 'to': [round(16 - f[0], 3), t[1], round(16 - f[2], 3)],
                    'faces': {sw[k]: v for k, v in e['faces'].items()}})
    return out

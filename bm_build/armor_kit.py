"""v299a: a small kit for armour drawn the vanilla way - the Hero of Time set (hero_armor_art.py) and the Arcade's 8-bit sets
(arcade_art.py) use it.

LAYERS   an equipment layer is the standard 64 x 32 humanoid armour texture: each part a box laid out as vanilla's ModelPart
         cube does it - its top and bottom faces in a band of `d` rows, then its sides in one strip round it (right, front,
         left, back). Layer.face() paints one face from a grid of characters (a palette per set; '.' left clear), so every
         pixel is placed by hand: flat colour fields, 3-4 shades lit from the top left, square details, no noise.
         The arms and legs are drawn once: the left limb is the right one mirrored (its 'right' face is the outer side).
HELMS    Helm builds a small 3D helmet as an item model worn on the head (a head item with no armour asset is drawn as its own
         model there, as the Dread Visage is): boxes on the head's own pixel grid - one model unit is one pixel of the player,
         the head filling 4..12 on every axis (its head display scales the model 1.6), the front north (-z). Each box face
         gets its own patch of one 64 x 64 texture, one texel a unit, painted by a face painter (a flat shaded material, or
         a grid). Item definition: the 3D helm on the head, the flat icon everywhere else."""
from PIL import Image

PART = {'head': (0, 0, 8, 8, 8), 'body': (16, 16, 8, 12, 4), 'arm': (40, 16, 4, 12, 4), 'leg': (0, 16, 4, 12, 4)}


def hexc(h):
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


def faces(u, v, w, h, d):
    return {'top': (u + d, v, w, d), 'bottom': (u + d + w, v, w, d),
            'right': (u, v + d, d, h), 'front': (u + d, v + d, w, h), 'left': (u + d + w, v + d, d, h), 'back': (u + 2 * d + w, v + d, w, h)}


class Layer:
    """a 64 x 32 armour layer, painted face by face from character grids"""
    def __init__(self, pal):
        self.im = Image.new('RGBA', (64, 32), (0, 0, 0, 0)); self.px = self.im.load()
        self.pal = {k: (hexc(v) if isinstance(v, str) else v) for k, v in pal.items()}

    def face(self, part, side, rows):
        x0, y0, w, h = faces(*PART[part])[side]
        assert len(rows) == h and all(len(r) == w for r in rows), (part, side, [len(r) for r in rows], w, h)
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch != '.':
                    self.px[x0 + x, y0 + y] = self.pal[ch]
        return self

    def faces(self, part, **sides):
        for side, rows in sides.items():
            self.face(part, side, rows)
        return self

    def fill(self, part, side, ch):
        x0, y0, w, h = faces(*PART[part])[side]
        return self.face(part, side, [ch * w] * h)


def ring(rows, w=4):
    """the four sides of a limb from one strip: rows of 16 (right, front, left, back - each `w` wide) -> dict of faces"""
    out = {}
    for i, side in enumerate(('right', 'front', 'left', 'back')):
        out[side] = [r[i * w:(i + 1) * w] for r in rows]
    return out


def body_ring(rows):
    """the body's sides from one strip of 24 (right 4, front 8, left 4, back 8)"""
    return {'right': [r[0:4] for r in rows], 'front': [r[4:12] for r in rows], 'left': [r[12:16] for r in rows], 'back': [r[16:24] for r in rows]}


def head_ring(rows):
    """the head's sides from one strip of 32 (right, front, left, back - 8 each)"""
    return {s: [r[i * 8:(i + 1) * 8] for r in rows] for i, s in enumerate(('right', 'front', 'left', 'back'))}


# ---------------------------------------------------------------------------------------------------------------- 3D helms
def shaded(ramp, top_hi=True, base=2):
    """a face painter: a flat field of ramp[base], lit from the top left - its top row a step lighter (ramp[base+1]), its
    bottom row a step darker; an 'up' face a step lighter all over with a lit rim, a 'down' face a step darker"""
    R = [hexc(c) if isinstance(c, str) else c for c in ramp]
    def paint(face, w, h):
        im = Image.new('RGBA', (w, h), R[base]); px = im.load()
        if face == 'up':
            for y in range(h):
                for x in range(w):
                    px[x, y] = R[min(len(R) - 1, base + 1)]
            for x in range(w): px[x, 0] = R[min(len(R) - 1, base + 2)] if len(R) > base + 2 else R[base + 1]
            for y in range(h): px[0, y] = R[min(len(R) - 1, base + 2)] if len(R) > base + 2 else R[base + 1]
        elif face == 'down':
            for y in range(h):
                for x in range(w): px[x, y] = R[max(0, base - 1)]
        else:
            if top_hi and h > 1:
                for x in range(w): px[x, 0] = R[min(len(R) - 1, base + 1)]
            if h > 2:
                for x in range(w): px[x, h - 1] = R[max(0, base - 1)]
        return im
    return paint


def grid(rows, pal, under=None):
    """a face painter from a character grid (for a face of exactly that size); '.' takes `under` (another painter) or clear"""
    P = {k: (hexc(v) if isinstance(v, str) else v) for k, v in pal.items()}
    def paint(face, w, h):
        assert len(rows) == h and all(len(r) == w for r in rows), (face, w, h, len(rows), [len(r) for r in rows])
        im = under(face, w, h) if under else Image.new('RGBA', (w, h), (0, 0, 0, 0))
        px = im.load()
        for y, r in enumerate(rows):
            for x, ch in enumerate(r):
                if ch != '.': px[x, y] = P[ch]
        return im
    return paint


HELM_DISPLAY = {'head': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1.6, 1.6, 1.6]},   # (one unit a pixel of the head)
                'gui': {'rotation': [25, 200, 0], 'translation': [0, -1, 0], 'scale': [0.75, 0.75, 0.75]},
                'ground': {'rotation': [0, 0, 0], 'translation': [0, -1, 0], 'scale': [0.5, 0.5, 0.5]},
                'fixed': {'rotation': [0, 180, 0], 'translation': [0, -1, 0], 'scale': [0.75, 0.75, 0.75]}}
FACES = ('north', 'south', 'east', 'west', 'up', 'down')


class Helm:
    """a 3D helm: boxes in head pixels (integers; the head 4..12), each face painted into its own patch of one texture"""
    def __init__(self, name):
        self.name = name; self.boxes = []

    def box(self, fr, to, paint, faces=FACES, over=None):
        """paint: a face painter for every face; over: {face: painter} for some faces"""
        self.boxes.append((tuple(fr), tuple(to), paint, tuple(faces), dict(over or {})))
        return self

    @staticmethod
    def _size(fr, to, f):
        dx, dy, dz = (int(round(to[i] - fr[i])) for i in range(3))
        return {'north': (dx, dy), 'south': (dx, dy), 'east': (dz, dy), 'west': (dz, dy), 'up': (dx, dz), 'down': (dx, dz)}[f]

    def build(self, size=64):
        """-> (texture image, model json) - the faces packed on shelves, one texel a unit"""
        tex = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        patches = []
        for i, (fr, to, paint, fs, over) in enumerate(self.boxes):
            for f in fs:
                w, h = self._size(fr, to, f)
                if w > 0 and h > 0: patches.append((h, w, i, f))
        patches.sort(key=lambda p: (-p[0], -p[1]))
        x = y = shelf = 0; at = {}
        for h, w, i, f in patches:
            if x + w > size: x = 0; y += shelf; shelf = 0
            assert y + h <= size, f'{self.name}: the helm texture is full'
            at[(i, f)] = (x, y, w, h); x += w; shelf = max(shelf, h)
        k = 16 / size
        els = []
        for i, (fr, to, paint, fs, over) in enumerate(self.boxes):
            fc = {}
            for f in fs:
                if (i, f) not in at: continue
                x0, y0, w, h = at[(i, f)]
                tex.paste((over.get(f) or paint)(f, w, h), (x0, y0))
                fc[f] = {'uv': [x0 * k, y0 * k, (x0 + w) * k, (y0 + h) * k], 'texture': '#t'}
            els.append({'from': list(fr), 'to': list(to), 'faces': fc})
        model = {'textures': {'t': f'bm:block/{self.name}', 'particle': f'bm:block/{self.name}'}, 'elements': els, 'display': HELM_DISPLAY}
        return tex, model


def write_helm(R2, iid, helm):
    """the helm's texture and model (bm:item/<iid>_worn), and its item definition: the 3D helm on the head, the icon
    (bm:item/<iid>, as gen_rp writes it from the icon) everywhere else"""
    tex, model = helm.build()
    tex.save(R2.p('assets', 'bm', 'textures', 'block', f'{helm.name}.png'))
    R2.wj(f'assets/bm/models/item/{iid}_worn.json', model)
    R2.wj(f'assets/bm/items/{iid}.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:display_context',
                                                    'cases': [{'when': 'head', 'model': {'type': 'minecraft:model', 'model': f'bm:item/{iid}_worn'}}],
                                                    'fallback': {'type': 'minecraft:model', 'model': f'bm:item/{iid}'}}})


def outline(im, col=(18, 14, 14, 255)):
    """an icon's dark outline round its silhouette (vanilla.process then tints it and lights the sprite)"""
    im = im.copy(); px = im.load(); w, h = im.size
    add = [(x, y) for y in range(h) for x in range(w) if px[x, y][3] == 0 and
           any(0 <= x + dx < w and 0 <= y + dy < h and px[x + dx, y + dy][3] > 0 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for x, y in add: px[x, y] = col
    return im


def icon(rows, pal, edge=True):
    """a 16 x 16 icon from a grid ('.' clear), outlined"""
    P = {k: (hexc(v) if isinstance(v, str) else v) for k, v in pal.items()}
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); px = im.load()
    assert len(rows) == 16 and all(len(r) == 16 for r in rows), [len(r) for r in rows]
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != '.': px[x, y] = P[ch]
    return outline(im) if edge else im

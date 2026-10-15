"""Phase 143 (2.78): the followers in finer cloth. Their textures were flat fields of 8-16 colours; now each material carries a
little life of its own, worked in after every follower's art is drawn (a post-pass over the built resource pack):

  CLOTH    a fine twill and soft folds         METAL    a sheen from the light above, and the odd glint
  HAIR     strands, column by column           LEATHER  grain and a few worn specks
  SKIN     the faintest grain

Faces, eyes, glows, emblems, gems, crystals, teeth and the animated textures are left exactly as drawn. Every recoloured look
(the _c / element / outfit copies) gets the same pass, so they still match. Seeded by the texture's name: the same every build.

rp(R) adds the POST; it must run after every follower's textures (gen_rp registers it last)."""
import re
import zlib

PREFIX = ('kw', 'em2', 'em3', 'em', 'cec', 'cec2', 'apo', 'dm', 'tu', 'le', 'ce', 'don', 'pm', 'zb')
SKIP = re.compile(r'face|eye|glow|pupil|lash|lid|brow|mouth|teeth|tongue|fang|emblem|gem|crystal|moon|star|seal|dot|glint|blackfire|cheek|socket|ice|frost|hex|claw')
KIND = [('cloth', re.compile(r'cape|coat|tunic|skirt|shirt|pants|hood|robe|scarf|sash|chest|blue|pink|jeans|top|shorts|hose|cuff|band|bag|bow|dress|black|white')),
        ('metal', re.compile(r'steel|plate|gold|brass|buckle|blade|tri|rim|mail|trim|shaft|mace')),
        ('hair', re.compile(r'hair|beard|fur|mane')),
        ('leather', re.compile(r'belt|boot|glove|shoe|sole|strap|grip|saddle|mitt|sneaker|stock|rope|wood')),
        ('skin', re.compile(r'skin|belly|muzzle|scale|bone|ear|patch|dark|wing|fin|flap'))]


def kind_of(name):
    """(the part's name, its prefix and recolour suffix aside) -> its material, or None to leave it be"""
    if SKIP.search(name): return None
    for k, rx in KIND:
        if rx.search(name): return k
    return None


def detail(img, kind, seed):
    import numpy as np
    a = np.asarray(img.convert('RGBA'), dtype=np.float32)
    h, w = a.shape[:2]
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:h, 0:w]
    if kind == 'cloth':
        f = 1 + 0.03 * np.where(((x + y) // 2) % 2 == 0, 1, -1) + 0.035 * np.sin(2 * np.pi * x / 16 + rng.uniform(0, 6.3)) + rng.normal(0, 0.018, (h, w))
    elif kind == 'metal':
        f = 1.07 - 0.14 * y / max(1, h - 1) + rng.normal(0, 0.015, (h, w))
        f = np.where(rng.random((h, w)) < 0.015, f + 0.22, f)
    elif kind == 'hair':
        f = 1 + rng.normal(0, 0.055, (1, w)) + rng.normal(0, 0.02, (h, w))
    elif kind == 'leather':
        f = 1 + rng.normal(0, 0.04, (h, w))
        f = np.where(rng.random((h, w)) < 0.02, f - 0.15, f)
    else:
        f = 1 + rng.normal(0, 0.018, (h, w))
    f = np.clip(f, 0.78, 1.25)[..., None]
    rgb = np.clip(a[..., :3] * f, 0, 255)
    out = np.concatenate([np.where(a[..., 3:4] > 0, rgb, a[..., :3]), a[..., 3:4]], axis=2)
    from PIL import Image
    return Image.fromarray(out.astype(np.uint8), 'RGBA')


def rp(R):
    def post(R2):
        import os
        from PIL import Image
        d = R2.p('assets', 'bm', 'textures', 'block')
        n = 0
        for fn_ in sorted(os.listdir(d)):
            if not fn_.endswith('.png') or os.path.exists(os.path.join(d, fn_ + '.mcmeta')): continue
            base = fn_[:-4]
            pre = next((p for p in sorted(PREFIX, key=len, reverse=True) if base.startswith(p + '_')), None)
            if not pre: continue
            part = base[len(pre) + 1:]
            k = kind_of(part)
            if not k: continue
            seed = zlib.crc32(re.sub(r'_(c\d+|d\d+|m\d+|r\d+|o\d+|air|earth|eth|fire|grass|ice|poison|rock|water|wf|electric|ethereal|wraith|gold|dk|lt)$', '', base).encode())
            p = os.path.join(d, fn_)
            im = Image.open(p)
            detail(im, k, seed).save(p)
            n += 1
        assert n > 150, n
    R.POST.append(post)

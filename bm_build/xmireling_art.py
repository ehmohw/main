"""3.0e (STAGE 1 DRAFT - art only, not wired): THE BROOD MIRELING - the Mireling's alien costume, a little Brood-Mire (xmire_art).
Purely cosmetic: the same Mireling (mireling_art's rig, every part, pose and face), its skin purple, its veins green, its eye
yellow and slit-pupilled - and more eyes: a pair on its brow, one on each cheek, a little one on its crown, one at its back,
two little eyestalks on its crown, eyes on its rings and its puddle, an eye on each tentacle's hook. Like the Brood-Mire's,
every extra eye blinks on its own timing (eye1 / eye2 / eye3, animated).

HOW IT'S WORN. A wardrobe look like the Mireling's others (phase99 / phase138: a look is a "_c<k>" suffix on whatever model a
part wears, so poses and faces keep working) - but its _c<k> models are not recoloured copies: they are built here, every
Mireling model (each part, each face of the head) with its textures swapped for the alien ones (mlx_*) and its extra eyes added.
LOOK = its key in WARDROBE: 7, the first free one (1-6 the looks, the shiny is phase99's own); its shiny twin 8.
models(suffix) -> {ml_<model>_c<k>: (textures, els)}.
FULL-GROWN in the costume: the Brood-Mire's own rig (xmire_art), as phase252._grown raises mire_art's (same parts, same poses).
SHINY: SHINY_PAL - the costume in a shiny palette of its own (pale pearl skin, magenta veins, gold eyes): models(..., shiny=True)."""
import math
from PIL import Image

import rigkit
from rigkit import el
import mireling_art as ML
import mire_art as MA
import xmire_art as XA

PREFIX = 'mlx_'
LOOK = 7
SUFFIX = f'_c{LOOK}'
SHINY_SUFFIX = f'_c{LOOK + 1}'
NAME, SHINY_NAME = 'Brood Mireling', 'Shiny Pearl Brood'
PIVOT, PARENT, PARTS, POSES, HIDDEN = ML.PIVOT, ML.PARENT, ML.PARTS, ML.POSES, ML.HIDDEN
RIG_SCALE = SCALE = ML.RIG_SCALE
CY, HZ = ML.CY, ML.HZ


# ---------------------------------------------------------------------------------------------------- textures (the Mireling's, made alien)
def _hot():
    return XA._grid(['f' * 16] * 2 + ['ffeeeeeeeeeeeeff'] + ['feeeeeeeeeeeeeef'] * 11 + ['ffeeeeeeeeeeeeff'] + ['f' * 16])


def brood_textures():
    """{mlx_<name>: RGBA} - every ml_ texture's alien twin, and the eyes (their first frame: open; the strips are xmire_art's)"""
    Y = {'i': XA.Y2, 'I': XA.Y3, 'j': XA.Y1, 'r': XA.Y1, 'R': XA.Y2, 's': XA.Y0}
    T = {'mlx_hide': XA._hide(), 'mlx_rib': XA._grid(MA.RIB, dict(XA.PAL, o=XA.G1, O=XA.G2)),
         'mlx_fold': XA._grid(MA.FOLD, dict(XA.PAL, **{'1': XA.V1, '2': XA.V3, '3': XA.V4, '4': XA.V5, '5': XA.V6})),
         'mlx_pool': XA._pool_frame(0, 8), 'mlx_drip': XA._drip(), 'mlx_spine': XA._ramp([XA.V2, XA.V3, XA.V4, XA.G2, XA.G3, XA.G4]),
         'mlx_lid': XA._lid(), 'mlx_glow': XA._vein_frame(1.0), 'mlx_hot': _hot(), 'mlx_barb': XA._ramp([XA.V1, XA.V3, XA.G2, XA.G3, XA.G4, XA.G5]),
         'mlx_fang': XA._ramp([(150, 156, 96), (178, 184, 118), (204, 208, 146), (226, 228, 176), (240, 240, 206)]),
         'mlx_maw': XA._grid(MA.MAWT, dict(XA.PAL, a=XA.G2, b=XA.G3, O=XA.V3)), 'mlx_ember': XA._grid(MA.EMBER, dict(XA.PAL, c=XA.G3, d=XA.G4, e=XA.G5)),
         'mlx_iris': XA._grid(MA.IRIS, Y), 'mlx_irisr': XA._grid(MA.IRISR, Y), 'mlx_void': XA._grid(['0' * 16] * 16, {'0': XA.KP}),
         'mlx_belly': XA._belly(), 'mlx_cyst': XA._cyst()}
    for k in XA.EYE_SEQ: T['mlx_' + k] = XA._eye_frame('open', 0)
    return T


# the shiny: each brood colour -> its shiny twin (by nearest brood colour)
_BROOD = [XA.V0, XA.V1, XA.V2, XA.V3, XA.V4, XA.V5, XA.V6, XA.G0, XA.G1, XA.G2, XA.G3, XA.G4, XA.G5, XA.Y0, XA.Y1, XA.Y2, XA.Y3, XA.Y4]
SHINY_PAL = [(96, 84, 100), (140, 126, 146), (184, 170, 190), (212, 200, 216), (232, 222, 236), (244, 238, 248), (255, 252, 255),
             (80, 12, 60), (140, 20, 104), (196, 40, 150), (236, 80, 190), (255, 140, 222), (255, 206, 240),
             (120, 70, 0), (200, 140, 10), (255, 200, 40), (255, 232, 110), (255, 250, 210)]


def shiny_of(im):
    im = im.convert('RGBA'); px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            k = min(range(len(_BROOD)), key=lambda i: sum((c - d) ** 2 for c, d in zip((r, g, b), _BROOD[i])))
            if sum((c - d) ** 2 for c, d in zip((r, g, b), _BROOD[k])) < 2400: px[x, y] = SHINY_PAL[k] + (a,)
    return im


def textures(shiny=False):
    T = brood_textures()
    if shiny: T = {k.replace('mlx_', 'mls_'): shiny_of(v) for k, v in T.items()}
    return T


# ---------------------------------------------------------------------------------------------------- the extra eyes
_N = [0]


def _eye(piv, c, s, n, pre, var=None, proud=None):
    """an eye set into the surface (xmire_art.EYE's way): a socket rim, a bulging ball, the blinking face"""
    if var is None: _N[0] += 1; var = 'eye' + '123'[_N[0] % 3]
    ax = 'xyz'.index(n[0]); sg = 1 if n[1] == '+' else -1; pr = proud if proud is not None else s * 0.4
    lo, hi = [c[i] - s / 2 for i in range(3)], [c[i] + s / 2 for i in range(3)]
    rlo, rhi = [c[i] - s / 2 - 0.15 for i in range(3)], [c[i] + s / 2 + 0.15 for i in range(3)]
    op = c[ax] + sg * pr
    lo[ax], hi[ax] = sorted((c[ax] - sg * 0.2, op)); rlo[ax], rhi[ax] = sorted((c[ax] - sg * 0.2, c[ax] + sg * min(0.2, pr * 0.5)))
    face = XA.NORMAL[n]; side = tuple(f for f in XA.F6 if f not in (face, XA.NORMAL[n[0] + ('-' if sg > 0 else '+')]))
    plo, phi = list(lo), list(hi); plo[ax], phi[ax] = sorted((op, op + sg * 0.05))
    return [el(rlo, rhi, pre + 'lid', piv, faces=side + (face,)), el(lo, hi, pre + 'lid', piv, faces=side),
            el(plo, phi, pre + var, piv, faces=(face,), uv={face: [0, 0, 16, 16]}, light=15)]


def _seg(piv, a, b, w, mat, pre):
    e = rigkit.seg(a, b, w, w, pre + mat, piv, (0.0, 0.0, -1.0), 0.1)
    return e


def extras(part, pre=PREFIX):
    """the costume's added elements for a part (design units, about the part's joint)"""
    piv = PIVOT[part]; E_ = lambda c, s, n, **kw: _eye(piv, c, s, n, pre, **kw); X = []
    if part == 'head':
        X += E_((-2.2, 31.5, HZ + 0.5 - 4.2 * 0.72 - 0.05), 1.5, 'z-') + E_((2.1, 31.7, HZ + 0.5 - 4.2 * 0.72 - 0.05), 1.1, 'z-')
        X += E_((5.5, 26.6, HZ - 2.2), 1.5, 'z-') + E_((-5.5, 22.4, HZ - 2.2), 1.2, 'z-')
        X += E_((6.6, 24.0, HZ + 0.4), 2.0, 'x+') + E_((-6.6, 26.0, HZ + 1.0), 1.6, 'x-')
        X += E_((1.6, 22.6, HZ + 6.1), 1.4, 'z+') + E_((-2.4, 32.65, HZ + 1.6), 1.1, 'y+')
        for (a, b, s) in (((2.2, 32.4, HZ + 1.8), (3.0, 36.6, HZ + 1.2), 2.0), ((-1.4, 32.4, HZ + 2.6), (-2.4, 35.6, HZ + 2.2), 1.6)):     # (little eyestalks)
            X.append(_seg(piv, a, b, 0.75, 'belly', pre))
            X.append(el((b[0] - s / 2, b[1], b[2] - s / 2), (b[0] + s / 2, b[1] + s, b[2] + s / 2), pre + 'lid', piv))
            X += E_((b[0], b[1] + s / 2, b[2] - s / 2), s * 0.84, 'z-', proud=0.25)
        X.append(el((3.9, 29.0, HZ + 2.4), (5.3, 30.4, HZ + 3.8), pre + 'cyst', piv, uv={f: [0, 0, 16, 16] for f in XA.F6}, light=11))
    elif part == 'seg1':
        X += E_((-1.8, 7.0, -4.7), 1.9, 'z-') + E_((4.7, 6.2, 1.4), 1.3, 'x+') + E_((1.0, 7.4, 4.7), 1.5, 'z+')
        X.append(el((-4.95, 8.6, -1.6), (-4.3, 10.0, -0.2), pre + 'cyst', piv, uv={f: [0, 0, 16, 16] for f in XA.F6}, light=11))
    elif part == 'seg2':
        X += E_((1.6, 14.2, 0.3 - 4.15), 1.5, 'z-') + E_((-4.15, 14.6, 0.6), 1.3, 'x-')
    elif part == 'body':
        X += E_((1.8, 3.2, -5.1), 1.3, 'z-') + E_((-3.4, 4.4, -1.6), 1.0, 'y+') + E_((4.6, 0.45, 4.8), 1.0, 'y+') + E_((-5.8, 0.45, -3.0), 0.8, 'y+')
    elif part in ('t1c', 't2c'):
        x, y, z = piv; X += E_((x, y + 2.7, z - 0.65), 1.15, 'z-', proud=0.3)
    elif part in ('t1a', 't2a'):
        x, y, z = piv; sd = 1 if part == 't1a' else -1
        X += E_((x + sd * 1.1, y + 4.0, z), 0.9, 'x+' if sd > 0 else 'x-')
    return X


# ---------------------------------------------------------------------------------------------------- models
def models(shiny=False, suffix=None):
    """{ml_<model><suffix>: (textures, elements)} - every Mireling model (each part, each face of the head) in the costume"""
    pre = 'mls_' if shiny else 'mlx_'
    suffix = suffix if suffix is not None else (SHINY_SUFFIX if shiny else SUFFIX)
    out = {}; _N[0] = 0
    ext = {p: extras(p, pre) for p in PARTS}
    for mid, (tex, els) in ML.models().items():
        part = mid[len(ML.PREFIX):].split('_x')[0]
        t = {k: v.replace('bm:block/ml_', 'bm:block/' + pre) for k, v in tex.items()}
        add = ext.get(part, [])
        for e in add:
            for fc in e['faces'].values():
                k = fc['texture'][1:]; t[k] = f'bm:block/{k}'
        all_ = els + add
        for e in add:
            for v in e['from'] + e['to']: assert -16 <= v <= 32, (mid, e['from'], e['to'])
        out[mid + suffix] = (t, all_)
    return out


def model_name(p, pose=None, suffix=SUFFIX):
    return ML.model_name(p, pose, suffix)


class Costume:
    """a rigkit rig wearing the costume (previews: rigkit.render(scene, Costume, pose, ...))"""
    PIVOT, PARENT, PARTS, PART_K, PREFIX = ML.PIVOT, ML.PARENT, ML.PARTS, {}, ML.PREFIX
    HIDDEN = staticmethod(ML.HIDDEN)
    SFX = SUFFIX

    @classmethod
    def model_name(cls, p, pose=None, suffix=''):
        return ML.model_name(p, pose, cls.SFX)


class ShinyCostume(Costume):
    SFX = SHINY_SUFFIX

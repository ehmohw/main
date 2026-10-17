"""2.78a: Wilfrey as he is, for his display-case figurine - a wither skeleton (the game's own skin, pulled into the block
atlas, not copied) standing as he comes out of his locket, his sword raised to the guard. One model, 16 units to a block
at half the mob's size (shown at 2x it stands as tall as Wilfrey); it faces north, as the dolls do."""
import json

SKIN = 'minecraft:entity/skeleton/wither_skeleton'
K = 0.5                                                        # (model units per texel)


def _uv(u, v, w, h, d, mirror=False):
    """the skin's box layout (64x32) -> item-model face uvs (0..16 across the sheet)"""
    U = lambda a, b, c, e: [a / 4, b / 2, c / 4, e / 2]
    f = {'north': U(u + d, v + d, u + d + w, v + d + h), 'south': U(u + 2 * d + w, v + d, u + 2 * d + 2 * w, v + d + h),
         'east': U(u, v + d, u + d, v + d + h), 'west': U(u + d + w, v + d, u + 2 * d + w, v + d + h),
         'up': U(u + d, v, u + d + w, v + d), 'down': U(u + d + w, v + d, u + d + 2 * w, v)}
    if mirror:
        f['east'], f['west'] = f['west'], f['east']
        for k in f: a, b, c, e = f[k]; f[k] = [c, b, a, e]
    return f


def _box(x0, y0, z0, x1, y1, z1, uv, rot=None):
    P = lambda x, y, z: [round(8 + x * K, 4), round(y * K, 4), round(8 + z * K, 4)]
    e = {'from': P(x0, y0, z0), 'to': P(x1, y1, z1), 'faces': {k: {'uv': v, 'texture': '#s'} for k, v in uv.items()}}
    if rot:
        ax, ang, (px, py, pz) = rot
        e['rotation'] = {'axis': ax, 'angle': ang, 'origin': P(px, py, pz)}
    return e


def _plain(x0, y0, z0, x1, y1, z1, tex, rot=None):
    e = _box(x0, y0, z0, x1, y1, z1, {k: [0, 0, 16, 16] for k in ('north', 'south', 'east', 'west', 'up', 'down')}, rot)
    for f in e['faces'].values(): f['texture'] = '#' + tex
    return e


def model(chibi=False):
    """chibi: his doll - the skull half again as big, the bones short (legs 8, body and arms 9; the skull 13 across)"""
    ARM = ('x', 45, (5, 22, 0))                               # (his sword arm brought up to the guard, from the shoulder)
    els = [_box(1, 0, -1, 3, 12, 1, _uv(0, 16, 2, 12, 2)), _box(-3, 0, -1, -1, 12, 1, _uv(0, 16, 2, 12, 2, True)),        # legs
           _box(-4, 12, -2, 4, 24, 2, _uv(16, 16, 8, 12, 4)),                                                              # body
           _box(4, 12, -1, 6, 24, 1, _uv(40, 16, 2, 12, 2), ARM),                                                          # sword arm
           _box(-6, 12, -1, -4, 24, 1, _uv(40, 16, 2, 12, 2, True), ('z', -8, (-5, 22, 0))),                              # the other, easy
           _box(-4, 24, -4, 4, 32, 4, _uv(0, 0, 8, 8, 8))]                                                                 # head
    # the sword in his fist (it turns with the arm): grip, guard, a long blade forward and up
    els += [_plain(4.4, 12.2, -1.8, 5.6, 13.4, 1.8, 'g', ARM), _plain(3.6, 12.0, -2.6, 6.4, 13.6, -1.8, 'x', ARM),
            _plain(4.55, 12.25, -14.5, 5.45, 13.35, -2.6, 'b', ARM), _plain(4.75, 12.45, -15.6, 5.25, 13.15, -14.5, 'b', ARM)]
    if chibi:
        els = [_chibi(e) for e in els]
    tex = {'s': SKIN, 'g': 'minecraft:block/dark_oak_planks', 'x': 'minecraft:block/gold_block', 'b': 'minecraft:block/iron_block', 'particle': SKIN}
    return tex, els


def _chibi(e):
    """(model units, half-size) legs 0-6 -> 0-4; body/arms 6-12 -> 4-8.5, scaled 0.75 about the hips; the head 12-16 -> 8.5-15, 1.6x about the neck"""
    e = json.loads(json.dumps(e))
    y0 = e['from'][1]
    if y0 < 5.9:                                              # (a leg: shortened, still axis-aligned)
        e['from'][1] *= 2 / 3; e['to'][1] *= 2 / 3
        return e
    if y0 >= 11.9:                                            # (the head)
        k, c0, c1 = 1.6, (8, 12, 8), (8, 8.5, 8)
    else:
        k, c0, c1 = 0.75, (8, 6, 8), (8, 4, 8)
    f = lambda p: [round(c1[i] + k * (p[i] - c0[i]), 4) for i in range(3)]
    e['from'], e['to'] = f(e['from']), f(e['to'])
    if 'rotation' in e: e['rotation']['origin'] = f(e['rotation']['origin'])
    return e


def rp(R):
    tex, els = model()
    R.HATS['wil_fig'] = ({k: v for k, v in tex.items() if k != 'particle'}, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + ('wil_fig',)

    def post(R2):          # (the skin into the block atlas, beside the vanilla sources - packs add to the list, they don't replace it)
        extra = [SKIN] + [t for t in getattr(R2, 'ATLAS_EXTRA', []) if t != SKIN]       # (2.79a: and the boss trophies' skins and sprites)
        src = lambda t: {'type': 'minecraft:single', 'resource': t[0], 'sprite': t[1]} if isinstance(t, tuple) else {'type': 'minecraft:single', 'resource': t}
        R2.wj('assets/minecraft/atlases/blocks.json', {'sources': [src(t) for t in dict.fromkeys(extra)]})
    R.POST.append(post)

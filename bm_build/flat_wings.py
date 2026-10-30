"""3.0c: THE WINGS, FLAT - worn wings are the elytra 'wings' layer by default (part of the player model: it never lags), and the
3D wings (seraph_wings' runtime) only for a player who switched them on (`bm.w3d`: the Particle Toggler's "3D wings" row, or
/trigger bm.wings3d) - they look great standing still but trail behind a fast-moving player (a display can't ride a player).

So each of the four sets the 3D runtime drives has TWO elytra layers (seraph_wings.sets() swaps the chest item's equippable
asset as the 3D wings come and go):
  bm:<asset>          the whole elytra mesh painted - its full 20 rows on vanilla's shape (sprites294._wing): the default
  bm:<asset>_mantle   the mesh cut back to a mantle over the shoulder blades (the 2.99 layers): under the 3D wings, as before

  set      flat asset (texture)                  mantle asset (texture)
  seraph   seraph_wings (seraph_wings)           seraph_wings_mantle (seraph_wings_mantle)
  dread    dread_carapace (dread_wings)          dread_carapace_mantle (dread_wings_mantle)
  sovn     sov_wings (sov_wings)                 sov_wings_mantle (sov_wings_mantle)
  sovl     sov_wings_holy (sov_wings_holy)       sov_wings_holy_mantle (sov_wings_holy_mantle)

The art: the Seraph's - pearl feathers, a gold leading edge, holy fire only at the ends, eyes open in the flights, a sapphire at
the wrist; the Dread Carapace's - black membrane on bone spars, red veins, two eyes, torn and smouldering at the hem; the Last
Night's - the Sovereign's black void membrane hung in strips from bone, many red eyes glowing, its torn edge burning; the First
Light's - white-gold feathers, gold bands, white fire at their ends, gems of light where the Last Night has eyes."""
from sprites294 import _wing, _feathers

import seraph_art as SA
import dread_art as DK

A = lambda c, a=255: tuple(c[:3]) + (a,)


def _eye(px, x, y, white, pupil, lid=None):
    """a little eye painted over the wing, kept on its opaque pixels: three across (a lid over and under it when given)"""
    for dx, dy, c in ((0, 0, pupil), (-1, 0, white), (1, 0, white)) + (((0, -1, lid), (0, 1, lid)) if lid else ()):
        if px[x + dx, y + dy][3]: px[x + dx, y + dy] = A(c)


def seraph():
    def p(x, y, u, v, edge):
        if x < 34: return A(SA.G1 if y % 2 else SA.G3)
        return _feathers(u, v, x, y, edge, [A(SA.G1), A(SA.G0)], A(SA.P3), A(SA.P2), A(SA.WHITE),
                         [A(SA.P1), A(SA.G1), A(SA.F1), A(SA.F2), A(SA.F0)], A(SA.G2),
                         [A(SA.P1), A(SA.P2), A(SA.G2)])
    im = _wing(p); px = im.load()
    for x, y in ((40, 8), (42, 13), (39, 16)):
        _eye(px, x, y, SA.EYE_W, SA.S2, SA.G1)
    for dx, dy, c in ((0, 0, SA.S1), (1, 0, SA.S2), (0, 1, SA.S2), (1, 1, SA.S3), (0, -1, SA.S0)):   # (the sapphire at the wrist)
        if px[36 + dx, 5 + dy][3]: px[36 + dx, 5 + dy] = A(c)
    return im


def _membrane(x, y, u, v, edge, P, spar_every=3, tear=7):
    """a wing face as membrane between bone spars slanting back from the leading edge; veins; a torn, burning hem"""
    k = x - 34
    if edge == 'lead': return A(P['bone_l'] if y % 3 else P['bone'])
    if k == 1: return A(P['bone_s'])
    s = (y - k // 2)                                                               # (the finger-spars, slanting back)
    if s % (spar_every * 3) == 0 and v < 0.9: return A(P['bone'] if k < 6 else P['bone_s'])
    if v > 0.88 or (edge == 'tip' and v > 0.7):                                    # (the hem: torn, smouldering)
        if (x * 5 + y * 3) % tear == 0: return None
        return A(P['ember'][(x + y) % len(P['ember'])])
    if edge == 'tip': return A(P['mem'][2])                                        # (the trailing edge: a dark rim)
    if k >= 3 and (2 * s + k) % 13 == 0: return A(P['vein'])                       # (veins, running back from the spars)
    band = (k + (y // 5)) % 3
    return A(P['mem'][band])


def dread():
    P = dict(bone_l=DK.BONE_L, bone=DK.BONE, bone_s=DK.BONE_S, vein=DK.RED_D, mem=(DK.VOID, DK.VOID2, DK.BLACK),
             ember=(DK.RED_D, DK.RED, DK.RED_L, DK.RED))
    def p(x, y, u, v, edge):
        if x < 34: return A(DK.VOID2 if y % 2 else DK.BLACK)
        return _membrane(x, y, u, v, edge, P)
    im = _wing(p); px = im.load()
    for x, y in ((41, 7), (40, 14)):
        _eye(px, x, y, DK.RED, DK.HOT)
    return im


def sov_night():
    from sov_wings import SPR
    P = dict(bone_l=SPR['e'], bone=SPR['b'], bone_s=SPR['V'], vein=SPR['l'], mem=(SPR['v'], SPR['k'], SPR['V']),
             ember=(SPR['r'], SPR['R'], SPR['w'], SPR['r']))
    def p(x, y, u, v, edge):
        if x < 34: return A(SPR['b'] if y % 2 else SPR['k'])
        return _membrane(x, y, u, v, edge, P, spar_every=2, tear=5)
    im = _wing(p); px = im.load()
    for x, y in ((40, 6), (42, 10), (39, 13), (42, 17)):                            # (every eye in them open)
        _eye(px, x, y, SPR['r'], SPR['w'])
    return im


def sov_light():
    from sov_wings import SPR
    def p(x, y, u, v, edge):
        if x < 34: return A(SPR['g'] if y % 2 else SPR['h'])
        k = x - 34
        if k in (2, 3) and y % 6 in (0, 1) and v < 0.85: return A(SPR['G'])             # (gold bands across the coverts)
        return _feathers(u, v, x, y, edge, [A(SPR['g']), A(SPR['f'])], A(SPR['s']), A(SPR['P']), A(SPR['W']),
                         [A(SPR['g']), A(SPR['f']), A(SPR['y']), A(SPR['W']), A(SPR['W'])], A(SPR['G']),
                         [A(SPR['p']), A(SPR['P']), A(SPR['G'])])
    im = _wing(p); px = im.load()
    for x, y in ((39, 5), (42, 8), (38, 11), (42, 13), (40, 16), (43, 18)):            # (gems of light where the Last Night has eyes)
        _eye(px, x, y, (200, 240, 255), SPR['W'], SPR['g'])
    return im


# set -> (flat asset, flat texture, its painter); the mantle asset / texture are these + '_mantle'
SETS = {'seraph': ('seraph_wings', 'seraph_wings', seraph), 'dread': ('dread_carapace', 'dread_wings', dread),
        'sovn': ('sov_wings', 'sov_wings', sov_night), 'sovl': ('sov_wings_holy', 'sov_wings_holy', sov_light)}


def mantle_asset(name):
    return f'bm:{SETS[name][0]}_mantle'


def flat_asset(name):
    return f'bm:{SETS[name][0]}'

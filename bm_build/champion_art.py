"""2.93: THE CHAMPIONS' REGALIA - what a fully honoured follower (Vitality, Bulwark and Might V) wears: their own new outfit pieces
and the Champion's gold medal, fitted to their own bones (phase205 wears them).

Every piece is modelled in the space of the bone it rides - the follower's head or body model, measured from the built pack -
so it stays on as that bone turns and swings: a piece copies its bone's place and pose every tick.
  HEAD   fighters get something fierce (a horned war-helm, a spiked or burning crown, a horned hood, bone spikes); the sweet ones
         something grand instead (a little crown, a tiara, a laurel, a pirate's hat) - never anything that scowls.
  BODY   spiked or rounded pauldrons, a cape down the back, a breastplate, a royal ruff, a sash, a spiked collar, a war-blanket
         over a beast's back, a belt.
  MEDAL  the Champion's medal: a gold disc with Queen Ava's sea-star, on a blue-and-gold ribbon, high on the chest.
Colours: gold, and the follower's own colour (light, mid, dark), dark steel, bone, ruby, sapphire, pearl, flame, leaf - one 32 px
sheet per follower (champ_<who>). Model space: the bone's own (its front is north, -z)."""
import json
import math
import random
from PIL import Image

# who: (head bone tag, head bone model, body bone tag, body bone model, extra selector filter)
ANCHORS = {
    'emma': ('bm.ep_head', 'em_head', 'bm.ep_body', 'em_body'),
    'celi': ('bm.cp6_head', 'ce_head', 'bm.cp6_body', 'ce_body'),
    'zib': ('bm.zbr_head', 'zbr_head', 'bm.zbr_torso', 'zbr_torso'),
    'cecil': ('bm.cp_head', 'cec2_head', 'bm.cp_body', 'cec2_body'),
    'kw': ('bm.kxp_head', 'kw_head', 'bm.kxp_body', 'kw_body'),
    'leo': ('bm.lp_head', 'le_head', 'bm.lp_body', 'le_body'),
    'demo': ('bm.dp_head', 'dm_head', 'bm.dp_body', 'dm_body'),
    'apo': ('bm.app_head', 'apo_head', 'bm.app_body', 'apo_body'),
    'tul': ('bm.tup_head', 'tu_head', 'bm.tup_body', 'tu_body'),
    'frog': ('bm.frr_body', 'frr_body', 'bm.frr_body', 'frr_body'),
    'don': ('bm.dnr_head', 'dnr_head_none', 'bm.dnr_torso', 'dnr_torso'),
    'fishy': ('bm.fyp_body', 'fy_body', 'bm.fyp_body', 'fy_body'),
    'dennis': ('bm.dwp_head', 'dw_head', 'bm.dwp_body', 'dw_body'),
    'pistachio': ('bm.pip_head', 'ps_head', 'bm.pip_body', 'ps_body'),
    'omega': ('bm.omp_head', 'om_head', 'bm.omp_body', 'om_body'),
    'ashur': ('bm.asp_head', 'as_head', 'bm.asp_body', 'as_body'),
    'chef': ('bm.kkp_head', 'cf_head', 'bm.kkp_body', 'cf_body'),
    'neighbor': ('bm.nbp_head', 'nb_head', 'bm.nbp_body', 'nb_body'),
    'ava': ('bm.avp_head', 'av_head', 'bm.avp_body', 'av_body'),
    'pearlq': ('bm.pqp_head', 'pq_head', 'bm.pqp_body', 'pq_body'),
    'bloo': ('bm.bop_head', 'bo_head', 'bm.bop_body', 'bo_body'),
    'stalker': ('bm.svp_head', 'st_head', 'bm.svp_body', 'st_body'),
    'lantern': ('bm.lnp_head', 'ln_head', 'bm.lnp_body', 'ln_body'),
    'bender': ('bm.bvp_head', 'bd_head', 'bm.bvp_body', 'bd_body'),
    'bones': ('bm.bjp_head', 'bn_head', 'bm.bjp_body', 'bn_body'),
    'capshun': ('bm.mzp_head', 'mz_head', 'bm.mzp_body', 'mz_body'),
    'kettle': ('bm.ktp_head', 'kt_head', 'bm.ktp_body', 'kt_body'),
    'rufus': ('bm.rup_head', 'rf_head', 'bm.rup_body', 'rf_body'),
    'henry': ('bm.hyp_head', 'hy_head', 'bm.hyp_body', 'hy_body'),
    'nia': ('bm.nip_head', 'ni_head', 'bm.nip_body', 'ni_body'),
    'gem': ('bm.cgp_head', 'cg_head', 'bm.cgp_body', 'cg_body'),
    'batty': ('bm.ytp_head', 'gb_head', 'bm.ytp_body', 'gb_body'),
    'eggbert': ('bm.ebp_head', 'ge_head', 'bm.ebp_body', 'ge_body'),
    'count': ('bm.knp_head', 'gc_head', 'bm.knp_body', 'gc_body'),
    'dragon': ('bm.ddp_head', 'dd_head', 'bm.ddp_body', 'dd_body'),
    'eraser': ('bm.ezp_body', 'er_body', 'bm.ezp_body', 'er_body'),
    'cursor': ('bm.uxp_body', 'cu_body', 'bm.uxp_body', 'cu_body'),
    'inkblot': ('bm.ibp_head', 'ib_head_blot', 'bm.ibp_body', 'ib_body_blot'),
    'speech': ('bm.wbp_body', 'sbb_body_speech', 'bm.wbp_body', 'sbb_body_speech'),
    'lightbringer': ('bm.lhp_head', 'lb_head', 'bm.lhp_body', 'lb_body'),
    'dryad': ('bm.pyp_head', 'pd_head', 'bm.pyp_body', 'pd_body'),
    'sovereign': ('bm.xvp_head', 'ds_head_bound', 'bm.xvp_body', 'ds_body_a'),
    'vexis': ('bm.xbp_head', 'vx_head_unlinked', 'bm.xbp_body', 'vx_body_h'),
    'pxcecil': ('bm.xcp_head', 'xc_hbone', 'bm.xcp_head', 'xc_bbone'),
    'pxleo': ('bm.xlp_head', 'xl_hbone', 'bm.xlp_head', 'xl_bbone'),
    'pxemma': ('bm.xmp_head', 'xm_hbone', 'bm.xmp_head', 'xm_bbone'),
    'sky': ('bm.ybp_head', 'yb_head', 'bm.ybp_body', 'yb_body'),
}
# who: (head piece, [body pieces], fierce?, aura particles)
WHOLE_BODY = {'apo', 'omega', 'fishy', 'bones'}   # (bodies with no chest on top - a serpent's coil, a bowl, a shark: fit the whole bone)
# (2.93: no head pieces - the owner found every crown and hat messy; the regalia is the body's and the medal)
STYLE = {
    'emma': ('tiara', ['cape'], False, ['minecraft:cherry_leaves ~ ~1 ~ 0.5 0.6 0.5 0 2', 'minecraft:dust{color:[1.0,0.55,0.85],scale:1.0} ~ ~1 ~ 0.5 0.6 0.5 0 3']),
    'celi': (None, ['cape'], True, ['minecraft:snowflake ~ ~1 ~ 0.5 0.6 0.5 0.01 3', 'minecraft:dust{color:[0.6,0.85,1.0],scale:1.0} ~ ~1 ~ 0.5 0.6 0.5 0 2']),
    'zib': (None, ['cape'], False, ['minecraft:electric_spark ~ ~1 ~ 0.4 0.5 0.4 0.05 3', 'minecraft:glow ~ ~1 ~ 0.4 0.5 0.4 0 1']),
    'cecil': (None, ['ruff', 'cape'], True, ['minecraft:enchant ~ ~1.2 ~ 0.5 0.6 0.5 0.5 6', 'minecraft:witch ~ ~1 ~ 0.4 0.5 0.4 0 1']),
    'kw': (None, ['bolts'], True, ['minecraft:electric_spark ~ ~1.2 ~ 0.6 0.8 0.6 0.1 6', 'minecraft:dust{color:[1.0,0.9,0.2],scale:1.2} ~ ~1 ~ 0.6 0.7 0.6 0 2']),
    'leo': (None, ['pauldrons', 'cape'], True, ['minecraft:bubble_pop ~ ~1 ~ 0.4 0.6 0.4 0 2', 'minecraft:dust{color:[0.35,0.75,0.95],scale:1.0} ~ ~1 ~ 0.5 0.6 0.5 0 3']),
    'demo': (None, ['cape'], True, ['minecraft:electric_spark ~ ~1.4 ~ 0.6 0.8 0.6 0.05 3', 'minecraft:dust{color:[0.45,0.85,0.4],scale:1.1} ~ ~1 ~ 0.6 0.7 0.6 0 3']),
    'apo': (None, [], True, ['minecraft:soul_fire_flame ~ ~1 ~ 0.8 0.8 0.8 0.01 3', 'minecraft:smoke ~ ~1 ~ 0.8 0.8 0.8 0 2']),
    'tul': (None, ['pauldrons', 'cape'], True, ['minecraft:snowflake ~ ~1 ~ 0.5 0.6 0.5 0.01 2', 'minecraft:bubble_pop ~ ~1 ~ 0.4 0.6 0.4 0 1']),
    'frog': (None, [], False, ['minecraft:happy_villager ~ ~0.6 ~ 0.4 0.3 0.4 0 1', 'minecraft:dust{color:[0.45,0.8,0.35],scale:0.8} ~ ~0.6 ~ 0.4 0.3 0.4 0 2']),
    'don': (None, [], False, ['minecraft:glow ~ ~1 ~ 0.4 0.5 0.4 0 2', 'minecraft:end_rod ~ ~1 ~ 0.4 0.5 0.4 0.01 1']),
    'fishy': (None, [], False, ['minecraft:bubble_pop ~ ~1.2 ~ 0.4 0.5 0.4 0 3', 'minecraft:dust{color:[1.0,0.65,0.25],scale:0.8} ~ ~1 ~ 0.4 0.5 0.4 0 2']),
    'dennis': (None, ['pauldrons', 'belt'], True, ['minecraft:wax_on ~ ~1 ~ 0.4 0.5 0.4 0 2', 'minecraft:dust{color:[1.0,0.8,0.25],scale:1.0} ~ ~0.8 ~ 0.4 0.4 0.4 0 2']),
    'pistachio': (None, [], False, ['minecraft:soul ~ ~1 ~ 0.5 0.6 0.5 0.01 1', 'minecraft:dust{color:[0.5,0.95,0.6],scale:1.0} ~ ~1 ~ 0.5 0.6 0.5 0 3']),
    'omega': (None, ['cape'], True, ['minecraft:soul ~ ~1.2 ~ 0.7 0.8 0.7 0.01 2', 'minecraft:sculk_soul ~ ~1.2 ~ 0.6 0.7 0.6 0.01 1']),
    'ashur': (None, ['cape'], True, ['minecraft:flame ~ ~1 ~ 0.5 0.6 0.5 0.01 4', 'minecraft:lava ~ ~1 ~ 0.3 0.3 0.3 0 1']),
    'chef': (None, ['sash'], False, ['minecraft:happy_villager ~ ~1 ~ 0.4 0.5 0.4 0 1', 'minecraft:dust{color:[1.0,0.85,0.45],scale:0.9} ~ ~1 ~ 0.4 0.5 0.4 0 2']),
    'neighbor': (None, ['cape'], False, ['minecraft:note ~ ~1.5 ~ 0.6 0.4 0.6 1 1', 'minecraft:dust{color:[0.5,0.75,1.0],scale:0.9} ~ ~1 ~ 0.4 0.5 0.4 0 2']),
    'ava': (None, ['cape'], False, ['minecraft:end_rod ~ ~1 ~ 0.4 0.6 0.4 0.01 1', 'minecraft:dust{color:[0.4,0.85,0.92],scale:1.0} ~ ~1 ~ 0.5 0.6 0.5 0 3']),
    'pearlq': (None, ['cape'], False, ['minecraft:glow ~ ~1 ~ 0.4 0.6 0.4 0 1', 'minecraft:dust{color:[0.35,0.88,0.85],scale:1.0} ~ ~1 ~ 0.5 0.6 0.5 0 3']),
    'bloo': (None, ['spines'], True, ['minecraft:crimson_spore ~ ~1 ~ 0.6 0.6 0.6 0 4', 'minecraft:dust{color:[0.35,0.6,0.95],scale:1.0} ~ ~1 ~ 0.5 0.6 0.5 0 2']),
    'stalker': (None, ['spines'], True, ['minecraft:squid_ink ~ ~1 ~ 0.5 0.6 0.5 0 1', 'minecraft:dust{color:[0.45,0.0,0.05],scale:1.2} ~ ~1 ~ 0.6 0.8 0.6 0 3']),
    'lantern': (None, [], True, ['minecraft:flame ~ ~1 ~ 0.8 0.5 0.8 0.01 4', 'minecraft:small_flame ~ ~1 ~ 0.8 0.5 0.8 0.01 3']),
    'bender': ('crown', ['collar'], False, ['minecraft:heart ~ ~1 ~ 0.4 0.3 0.4 0 1', 'minecraft:dust{color:[0.88,0.66,0.38],scale:0.9} ~ ~0.7 ~ 0.4 0.3 0.4 0 2']),
    'bones': ('tricorne', [], False, ['minecraft:bubble ~ ~0.8 ~ 0.6 0.4 0.6 0 3', 'minecraft:nautilus ~ ~1 ~ 0.6 0.4 0.6 0.5 2']),
    'gem': (None, [], False, ['minecraft:end_rod ~ ~0.8 ~ 0.3 0.3 0.3 0.01 1', 'minecraft:dust{color:[0.4,1.0,0.7],scale:0.8} ~ ~0.8 ~ 0.3 0.3 0.3 0 2']),
    'batty': ('crown_flat', [], False, ['minecraft:large_smoke ~ ~0.8 ~ 0.3 0.3 0.3 0.005 1', 'minecraft:dust{color:[0.55,0.55,0.85],scale:0.8} ~ ~0.8 ~ 0.3 0.3 0.3 0 2']),
    'eggbert': ('crown_flat', [], False, ['minecraft:squid_ink ~ ~0.8 ~ 0.3 0.3 0.3 0.005 1', 'minecraft:dust{color:[0.85,0.83,0.75],scale:0.8} ~ ~0.8 ~ 0.3 0.3 0.3 0 2']),
    'dragon': ('crown_flat', [], False, ['minecraft:small_flame ~ ~1.2 ~ 0.3 0.3 0.3 0.01 1', 'minecraft:dust{color:[0.35,0.75,0.28],scale:0.8} ~ ~1 ~ 0.3 0.4 0.3 0 2']),
    'eraser': ('crown_flat', [], False, ['minecraft:cherry_leaves ~ ~0.8 ~ 0.3 0.3 0.3 0 1', 'minecraft:dust{color:[0.94,0.54,0.63],scale:0.8} ~ ~0.6 ~ 0.3 0.3 0.3 0 2']),
    'cursor': ('crown_flat', [], False, ['minecraft:electric_spark ~ ~1 ~ 0.3 0.4 0.3 0.02 1', 'minecraft:dust{color:[0.81,0.91,1.0],scale:0.8} ~ ~1 ~ 0.3 0.4 0.3 0 2']),
    'inkblot': ('crown_flat', [], False, ['minecraft:squid_ink ~ ~0.8 ~ 0.3 0.3 0.3 0.005 1', 'minecraft:dust{color:[0.48,0.48,0.67],scale:0.8} ~ ~0.8 ~ 0.3 0.3 0.3 0 2']),
    'speech': ('crown_flat', [], False, ['minecraft:end_rod ~ ~1 ~ 0.3 0.3 0.3 0.01 1', 'minecraft:dust{color:[1.0,0.82,0.38],scale:0.8} ~ ~1 ~ 0.3 0.4 0.3 0 2']),
    'lightbringer': (None, [], False, ['minecraft:end_rod ~ ~1.8 ~ 0.3 0.2 0.3 0.005 1', 'minecraft:dust{color:[1.0,0.88,0.54],scale:0.8} ~ ~1.4 ~ 0.3 0.5 0.3 0 2']),
    'dryad': ('crown_flat', [], False, ['minecraft:spore_blossom_air ~ ~0.8 ~ 0.3 0.3 0.3 0 1', 'minecraft:dust{color:[0.42,0.66,0.94],scale:0.8} ~ ~0.8 ~ 0.3 0.3 0.3 0 2']),
    'sovereign': (None, [], False, ['minecraft:sculk_soul ~ ~2 ~ 0.3 0.2 0.3 0.01 1', 'minecraft:dust{color:[0.82,0.1,0.18],scale:0.8} ~ ~1.4 ~ 0.3 0.5 0.3 0 2']),
    'vexis': (None, [], False, ['minecraft:reverse_portal ~ ~1.8 ~ 0.3 0.2 0.3 0.01 1', 'minecraft:dust{color:[0.48,1.0,0.42],scale:0.8} ~ ~1.4 ~ 0.3 0.5 0.3 0 2']),
    'count': ('crown_flat', [], False, ['minecraft:item_slime ~ ~0.8 ~ 0.3 0.3 0.3 0.01 1', 'minecraft:dust{color:[0.66,0.78,0.94],scale:0.8} ~ ~0.8 ~ 0.3 0.3 0.3 0 2']),
    'henry': ('crown_flat', [], False, ['minecraft:squid_ink ~ ~0.5 ~ 0.3 0.2 0.3 0.01 1', 'minecraft:dust{color:[0.75,0.75,0.9],scale:0.7} ~ ~0.5 ~ 0.3 0.2 0.3 0 2']),
    'nia': ('crown_flat', [], False, ['minecraft:end_rod ~ ~0.5 ~ 0.3 0.2 0.3 0.005 1', 'minecraft:dust{color:[0.9,0.65,0.3],scale:0.7} ~ ~0.5 ~ 0.3 0.2 0.3 0 2']),
    'rufus': ('crown_flat', [], False, ['minecraft:crit ~ ~0.8 ~ 0.3 0.4 0.3 0.05 1', 'minecraft:dust{color:[1.0,0.8,0.25],scale:0.8} ~ ~0.7 ~ 0.3 0.4 0.3 0 2']),
    'kettle': ('crown_flat', [], False, ['minecraft:happy_villager ~ ~1.2 ~ 0.3 0.6 0.3 0 1', 'minecraft:dust{color:[0.55,0.85,1.0],scale:0.8} ~ ~1.2 ~ 0.3 0.6 0.3 0 2']),
    'capshun': ('crown_flat', [], False, ['minecraft:end_rod ~ ~1 ~ 0.3 0.5 0.3 0.01 1', 'minecraft:dust{color:[1.0,1.0,1.0],scale:0.8} ~ ~1 ~ 0.3 0.5 0.3 0 2']),
    'pxcecil': (None, [], False, ['minecraft:electric_spark ~ ~1 ~ 0.4 0.5 0.4 0.05 1', 'minecraft:dust{color:[1.0,1.0,1.0],scale:0.6} ~ ~1 ~ 0.4 0.5 0.4 0 2']),
    'pxleo': (None, [], False, ['minecraft:electric_spark ~ ~1 ~ 0.4 0.5 0.4 0.05 1', 'minecraft:dust{color:[1.0,1.0,1.0],scale:0.6} ~ ~1 ~ 0.4 0.5 0.4 0 2']),
    'pxemma': (None, [], False, ['minecraft:electric_spark ~ ~1 ~ 0.4 0.5 0.4 0.05 1', 'minecraft:dust{color:[1.0,1.0,1.0],scale:0.6} ~ ~1 ~ 0.4 0.5 0.4 0 2']),
    'sky': (None, [], False, ['minecraft:end_rod ~ ~2 ~ 0.6 0.5 0.6 0.01 1', 'minecraft:dust{color:[1.0,0.85,0.3],scale:0.9} ~ ~2 ~ 0.6 0.5 0.6 0 2']),
}
COL = {'emma': '#ff8ad8', 'celi': '#9ad8ff', 'zib': '#3ad8c8', 'cecil': '#b48cff', 'kw': '#ffe040', 'leo': '#5ab8e0', 'demo': '#7ad06a',
       'apo': '#3ad06a', 'tul': '#7ad8ff', 'frog': '#6ac850', 'don': '#e8d29a', 'fishy': '#ffa040', 'dennis': '#e0a040', 'pistachio': '#7ae890',
       'omega': '#9fb4ff', 'ashur': '#ff7a2a', 'chef': '#ffd07a', 'neighbor': '#7ab8ff', 'ava': '#6ad8e8', 'pearlq': '#5ae0d8', 'bloo': '#5a9ae8',
       'stalker': '#a8ac70', 'lantern': '#ff8a2a', 'bender': '#e0a860', 'bones': '#8ab0c8', 'capshun': '#f0f0f0', 'kettle': '#8ad8ff', 'rufus': '#c0392b', 'henry': '#9a9ab8', 'nia': '#e0a050', 'gem': '#5ae0a0', 'batty': '#8a8ad8', 'eggbert': '#d8d4c0', 'count': '#a8c8f0', 'dragon': '#5ac048', 'eraser': '#f08aa0', 'cursor': '#cfe8ff', 'inkblot': '#7a7aaa', 'speech': '#ffd060', 'lightbringer': '#ffe08a', 'dryad': '#6aa8f0', 'sovereign': '#d0182e', 'vexis': '#7aff6a', 'sky': '#ffd04a', 'pxemma': '#ff6ac8', 'pxleo': '#4ab0ff', 'pxcecil': '#b070ff'}
# the 4 x 4 tiles of a follower's sheet
G, GD, GL, P, PD, PL, ST, STL, BN, BND, RUBY, SAPH, PEARL, FL_O, FL_Y, LEAF = range(16)


def _hex(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _mix(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def sheet(who):
    """32 x 32: 16 tiles of 8 px, each with a little grain and a bevel (light top-left, dark bottom-right)"""
    p = _hex(COL[who])
    cols = [(232, 182, 48), (160, 110, 24), (255, 226, 120), _mix(p, (0, 0, 0), 0.08), _mix(p, (0, 0, 0), 0.45), _mix(p, (255, 255, 255), 0.4),
            (44, 44, 54), (96, 98, 112), (226, 216, 190), (158, 146, 118), (200, 24, 52), (40, 90, 220), (240, 238, 250),
            (255, 120, 24), (255, 214, 72), (70, 160, 60)]
    im = Image.new('RGBA', (32, 32))
    rnd = random.Random(sum(map(ord, who)))
    for t, c in enumerate(cols):
        ox, oy = (t % 4) * 8, (t // 4) * 8
        for y in range(8):
            for x in range(8):
                k = rnd.uniform(-0.06, 0.06)
                if x == 0 or y == 0: k += 0.16
                if x == 7 or y == 7: k -= 0.18
                im.putpixel((ox + x, oy + y), tuple(max(0, min(255, round(v * (1 + k)))) for v in c) + (255,))
    return im


# ---------------------------------------------------------------------------------------------------- geometry
def _clamp(v):
    return round(max(-15.9, min(31.9, v)), 3)


def box(a, b, tile, rot=None):
    a, b = [min(a[i], b[i]) for i in range(3)], [max(a[i], b[i]) for i in range(3)]
    a = [_clamp(v) for v in a]; b = [_clamp(v) for v in b]
    b = [max(b[i], a[i] + 0.05) for i in range(3)]
    u0, v0 = (tile % 4) * 4, (tile // 4) * 4
    uv = [u0 + 0.5, v0 + 0.5, u0 + 3.5, v0 + 3.5]
    e = {'from': a, 'to': b, 'faces': {f: {'uv': uv, 'texture': '#t'} for f in ('north', 'south', 'east', 'west', 'up', 'down')}}
    if rot:
        axis, ang, origin = rot
        e['rotation'] = {'origin': [_clamp(o) for o in origin], 'axis': axis, 'angle': ang}
    return e


class BB:
    def __init__(self, r):
        (self.x0, self.x1), (self.y0, self.y1), (self.z0, self.z1) = r
        self.cx, self.cz = (self.x0 + self.x1) / 2, (self.z0 + self.z1) / 2
        self.w, self.h, self.d = self.x1 - self.x0, self.y1 - self.y0, self.z1 - self.z0


def ring(b, y0, y1, tile, pad=0.35, th=0.6):
    """a band round the bbox at height y0..y1, just outside it"""
    X0, X1, Z0, Z1 = b.x0 - pad, b.x1 + pad, b.z0 - pad, b.z1 + pad
    return [box((X0 - th, y0, Z0 - th), (X1 + th, y1, Z0), tile), box((X0 - th, y0, Z1), (X1 + th, y1, Z1 + th), tile),
            box((X0 - th, y0, Z0), (X0, y1, Z1), tile), box((X1, y0, Z0), (X1 + th, y1, Z1), tile)]


def points(b, y, n, hgt, tile, tip=None, pad=0.35, size=0.9):
    """n spikes round the top of a band (front, back and sides), tipped"""
    out = []
    X0, X1, Z0, Z1 = b.x0 - pad - 0.3, b.x1 + pad + 0.3, b.z0 - pad - 0.3, b.z1 + pad + 0.3
    spots = []
    for i in range(n):
        t = (i + 0.5) / n
        spots += [(X0 + (X1 - X0) * t, Z0), (X0 + (X1 - X0) * t, Z1)]
    for i in range(max(1, n - 2)):
        t = (i + 0.5) / max(1, n - 2)
        spots += [(X0, Z0 + (Z1 - Z0) * t), (X1, Z0 + (Z1 - Z0) * t)]
    for j, (x, z) in enumerate(spots):
        hh = hgt * (1.0 if j % 2 == 0 else 0.7)
        s = size * (1 if hh > 1.4 else 0.8)
        out.append(box((x - s / 2, y, z - s / 2), (x + s / 2, y + hh * 0.75, z + s / 2), tile))
        if tip is not None:
            out.append(box((x - s / 4, y + hh * 0.75, z - s / 4), (x + s / 4, y + hh, z + s / 4), tip))
    return out


def head_piece(kind, b):
    top, H = b.y1, b.h
    out = []
    if kind in ('crown', 'crown_top'):
        y = top - min(1.6, H * 0.18)
        out += ring(b, y, top + 0.6, G, pad=0.2 if kind == 'crown' else -max(0.0, b.w * 0.25), th=0.5) if kind == 'crown' else \
            ring(BB([(b.cx - 2.6, b.cx + 2.6), (b.y0, b.y1), (b.cz - 2.6, b.cz + 2.6)]), top, top + 1.1, G, pad=0, th=0.5)
        bb = b if kind == 'crown' else BB([(b.cx - 2.6, b.cx + 2.6), (b.y0, b.y1), (b.cz - 2.6, b.cz + 2.6)])
        yy = top + 0.6 if kind == 'crown' else top + 1.1
        out += points(bb, yy, 3, 1.5, GL, pad=0.2 if kind == 'crown' else 0, size=0.7)
        out.append(box((bb.cx - 0.5, yy - 1.0, bb.z0 - 1.25), (bb.cx + 0.5, yy, bb.z0 - 0.75), RUBY))
    elif kind == 'crown_flat':                        # (Mr. Capshun is drawn flat: a doodled crown, flat too)
        z0, z1 = b.cz - 0.3, b.cz + 0.3
        out += [box((b.cx - 3, top + 0.2, z0), (b.cx + 3, top + 1.2, z1), G)]
        for dx in (-2.6, 0, 2.6):
            out.append(box((b.cx + dx - 0.5, top + 1.2, z0), (b.cx + dx + 0.5, top + 2.6 + (0.6 if dx == 0 else 0), z1), GL))
        out.append(box((b.cx - 0.45, top + 0.4, z0 - 0.1), (b.cx + 0.45, top + 1.0, z1 + 0.1), RUBY))
    elif kind == 'tiara':
        y = top - min(2.2, H * 0.25)
        out += [box((b.x0 - 0.3, y, b.z0 - 0.5), (b.x1 + 0.3, y + 0.7, b.z0 - 0.1), G),       # the band over the brow
                box((b.x0 - 0.5, y, b.z0 - 0.1), (b.x0 - 0.1, y + 0.7, b.cz), G), box((b.x1 + 0.1, y, b.z0 - 0.1), (b.x1 + 0.5, y + 0.7, b.cz), G)]
        out += [box((b.cx - 0.6, y + 0.7, b.z0 - 0.6), (b.cx + 0.6, y + 2.6, b.z0 - 0.1), GL),
                box((b.cx - 0.45, y + 1.1, b.z0 - 0.8), (b.cx + 0.45, y + 2.0, b.z0 - 0.5), SAPH),
                box((b.cx - 2.2, y + 0.7, b.z0 - 0.5), (b.cx - 1.3, y + 1.7, b.z0 - 0.1), GL), box((b.cx + 1.3, y + 0.7, b.z0 - 0.5), (b.cx + 2.2, y + 1.7, b.z0 - 0.1), GL),
                box((b.cx - 3.6, y + 0.7, b.z0 - 0.5), (b.cx - 3.0, y + 1.2, b.z0 - 0.1), PEARL), box((b.cx + 3.0, y + 0.7, b.z0 - 0.5), (b.cx + 3.6, y + 1.2, b.z0 - 0.1), PEARL)]
    elif kind == 'laurel':
        y = top - min(1.8, H * 0.2)
        out += ring(b, y, y + 0.6, GD, pad=0.2, th=0.4)
        for i in range(7):                             # leaves along each side and over the brow
            t = i / 6
            x = b.x0 + b.w * t
            out.append(box((x - 0.5, y + 0.3, b.z0 - 1.0), (x + 0.5, y + 1.1, b.z0 - 0.3), LEAF if i % 2 else G))
        for i in range(4):
            z = b.z0 + b.d * (i + 0.5) / 4
            out += [box((b.x0 - 1.0, y + 0.3, z - 0.5), (b.x0 - 0.3, y + 1.1, z + 0.5), LEAF), box((b.x1 + 0.3, y + 0.3, z - 0.5), (b.x1 + 1.0, y + 1.1, z + 0.5), LEAF)]
    elif kind == 'spikecrown':
        y = top - min(1.8, H * 0.2)
        out += ring(b, y, top + 0.8, ST, pad=0.25)
        out += ring(b, y + 0.2, y + 0.6, G, pad=0.3, th=0.65)
        out += points(b, top + 0.8, 3, 3.0, ST, tip=RUBY, pad=0.25, size=0.9)
    elif kind == 'icecrown':
        y = top - min(1.8, H * 0.2)
        out += ring(b, y, top + 0.6, PL, pad=0.25)
        out += points(b, top + 0.6, 3, 3.4, PL, tip=PEARL, pad=0.25, size=1.0)
        out.append(box((b.cx - 0.6, y, b.z0 - 1.2), (b.cx + 0.6, y + 1.6, b.z0 - 0.6), SAPH))
    elif kind == 'bonecrown':
        y = top - min(2.0, H * 0.18)
        out += ring(b, y, top + 0.5, BND, pad=0.3)
        out += points(b, top + 0.5, 3, 3.6, BN, tip=BND, pad=0.3, size=1.0)
        out += [box((b.cx - 1.2, y - 0.2, b.z0 - 1.3), (b.cx + 1.2, y + 1.8, b.z0 - 0.7), BN),        # a little skull over the brow
                box((b.cx - 0.8, y + 0.7, b.z0 - 1.4), (b.cx - 0.2, y + 1.3, b.z0 - 1.25), P), box((b.cx + 0.2, y + 0.7, b.z0 - 1.4), (b.cx + 0.8, y + 1.3, b.z0 - 1.25), P)]
    elif kind == 'flamecrown':
        y = top - min(1.6, H * 0.18)
        out += ring(b, y, top + 0.5, GD, pad=0.25)
        out += points(b, top + 0.5, 3, 2.6, FL_O, tip=FL_Y, pad=0.25, size=1.1)
        out += points(b, top + 0.5, 2, 4.2, FL_Y, pad=-0.6, size=0.6)
    elif kind == 'hornhelm':
        y = b.y0 + H * 0.45
        out += [box((b.x0 - 0.5, top, b.z0 - 0.5), (b.x1 + 0.5, top + 0.9, b.z1 + 0.5), ST),          # the crown of the helm
                box((b.x0 - 0.9, y, b.z0 - 0.5), (b.x0 - 0.1, top + 0.4, b.z1 + 0.5), ST), box((b.x1 + 0.1, y, b.z0 - 0.5), (b.x1 + 0.9, top + 0.4, b.z1 + 0.5), ST),
                box((b.x0 - 0.5, y, b.z1 + 0.1), (b.x1 + 0.5, top + 0.4, b.z1 + 0.9), ST),
                box((b.x0 - 0.5, top - H * 0.22, b.z0 - 0.9), (b.x1 + 0.5, top + 0.2, b.z0 - 0.1), STL),           # the brow guard
                box((b.cx - 0.45, top - H * 0.5, b.z0 - 1.0), (b.cx + 0.45, top - H * 0.2, b.z0 - 0.2), STL),     # the nasal
                box((b.x0 - 0.6, top - H * 0.15, b.z0 - 1.0), (b.x1 + 0.6, top - H * 0.08, b.z0 - 0.85), G)]
        hz = b.cz - b.d * 0.1
        for s in (-1, 1):                              # the horns: out, then up, then a bone tip
            x = b.x0 - 0.9 if s < 0 else b.x1 + 0.9
            out += [box((x - (2.6 if s < 0 else 0), top - 1.4, hz - 0.9), (x + (0 if s < 0 else 2.6), top + 0.2, hz + 0.9), BN),
                    box((x - (3.4 if s < 0 else -1.6), top - 0.2, hz - 0.75), (x - (1.8 if s < 0 else -3.4), top + 2.6, hz + 0.75), BN),
                    box((x - (3.2 if s < 0 else -2.0), top + 2.6, hz - 0.5), (x - (2.2 if s < 0 else -3.0), top + 4.2, hz + 0.5), BND)]
    elif kind == 'crested':                            # a knight's helm crest: a gold fin and a plume in his colour
        out += [box((b.cx - 0.4, top, b.z0), (b.cx + 0.4, top + 1.2, b.z1), G),
                box((b.cx - 0.55, top + 1.2, b.z0 + b.d * 0.15), (b.cx + 0.55, top + 3.2, b.z1 + 0.6), P),
                box((b.cx - 0.45, top + 2.4, b.z1 + 0.6), (b.cx + 0.45, top + 3.2, b.z1 + 2.2), PD)]
        out += ring(b, top - min(1.4, H * 0.15), top - min(1.4, H * 0.15) + 0.6, G, pad=0.25, th=0.5)
    elif kind == 'hornhood':                           # two long horns swept back and a ridge of spines
        out += [box((b.cx - 0.5, top, b.z0 + b.d * 0.2), (b.cx + 0.5, top + 1.0, b.z1), ST)]
        for i in range(4):
            z = b.z0 + b.d * (0.25 + 0.2 * i)
            out.append(box((b.cx - 0.35, top + 1.0, z - 0.4), (b.cx + 0.35, top + 1.0 + 1.8 - 0.3 * i, z + 0.4), RUBY if i == 0 else STL))
        for s in (-1, 1):
            x = b.cx + s * b.w * 0.32
            out += [box((x - 0.8, top - 0.4, b.cz - 0.8), (x + 0.8, top + 1.6, b.cz + 0.8), BND),
                    box((x - 0.65, top + 1.2, b.cz + 0.2), (x + 0.65, top + 2.6, b.cz + 3.0), BN),
                    box((x - 0.45, top + 1.8, b.cz + 3.0), (x + 0.45, top + 2.8, b.cz + 5.0), BND)]
    elif kind == 'visor':                              # a pilot's visor and an antenna, gold-trimmed
        y = b.y0 + b.h * 0.55
        out += [box((b.x0 - 0.4, y, b.z0 - 0.8), (b.x1 + 0.4, y + b.h * 0.22, b.z0 - 0.2), SAPH),
                box((b.x0 - 0.5, y - 0.3, b.z0 - 0.9), (b.x1 + 0.5, y, b.z0 - 0.1), G),
                box((b.x0 - 0.8, y - 0.3, b.z0 - 0.1), (b.x0 - 0.2, y + b.h * 0.25, b.cz + 1.0), G), box((b.x1 + 0.2, y - 0.3, b.z0 - 0.1), (b.x1 + 0.8, y + b.h * 0.25, b.cz + 1.0), G),
                box((b.x1 - 1.2, top, b.cz - 0.2), (b.x1 - 0.8, top + 3.0, b.cz + 0.2), ST), box((b.x1 - 1.45, top + 3.0, b.cz - 0.45), (b.x1 - 0.55, top + 3.9, b.cz + 0.45), RUBY)]
    elif kind == 'tricorne':                           # a captain's three-cornered hat, gold-edged
        y = top - min(1.0, b.h * 0.12)
        out += [box((b.x0 - 1.4, y, b.z0 - 1.4), (b.x1 + 1.4, y + 0.6, b.z1 + 1.4), PD),
                box((b.x0 - 1.5, y + 0.6, b.z0 - 1.5), (b.x1 + 1.5, y + 1.0, b.z0 - 0.9), G),
                box((b.x0 - 1.5, y + 0.6, b.z0 - 1.4), (b.x0 - 0.9, y + 1.8, b.z1 + 1.4), PD), box((b.x1 + 0.9, y + 0.6, b.z0 - 1.4), (b.x1 + 1.5, y + 1.8, b.z1 + 1.4), PD),
                box((b.x0 - 0.2, y + 0.6, b.z0 - 0.2), (b.x1 + 0.2, y + 2.6, b.z1 + 0.2), PD),
                box((b.x0 - 0.3, y + 0.7, b.z0 - 0.3), (b.x1 + 0.3, y + 1.1, b.z1 + 0.3), G),
                box((b.cx - 0.5, y + 1.3, b.z0 - 0.5), (b.cx + 0.5, y + 2.3, b.z0 - 0.25), BN)]
    return out


def _cape(b, y0, top):
    """a cape's cloth and trim (hung, then swung back)"""
    out = []
    out += [box((b.x0 - 0.6, y0, b.z1 + 0.25), (b.x1 + 0.6, top, b.z1 + 0.75), PD),
            box((b.x0 - 0.7, y0 - 0.3, b.z1 + 0.3), (b.x1 + 0.7, y0 + 0.5, b.z1 + 0.85), G),
            box((b.x0 - 0.8, top - 0.6, b.z1 - 0.3), (b.x1 + 0.8, top + 0.2, b.z1 + 0.85), G),
            box((b.cx - 1.2, top - 3.5, b.z1 + 0.75), (b.cx + 1.2, top - 1.1, b.z1 + 0.95), G),          # the sea-star device
            box((b.cx - 0.5, top - 3.0, b.z1 + 0.95), (b.cx + 0.5, top - 1.6, b.z1 + 1.05), SAPH)]
    return out


def body_piece(kind, b, fierce):
    out = []
    top, H = b.y1, b.h
    if kind == 'pauldrons':
        for s in (-1, 1):
            x0, x1 = (b.x0 - 1.4, b.x0 + b.w * 0.28) if s < 0 else (b.x1 - b.w * 0.28, b.x1 + 1.4)
            out += [box((x0, top - 1.8, b.z0 - 0.6), (x1, top + 0.6, b.z1 + 0.6), P),
                    box((x0 + 0.3, top + 0.6, b.z0 - 0.3), (x1 - 0.3, top + 1.2, b.z1 + 0.3), PL),
                    box((x0, top - 2.2, b.z0 - 0.7), (x1, top - 1.8, b.z1 + 0.7), G)]
    elif kind == 'spikes':                             # spiked dark pauldrons
        for s in (-1, 1):
            x0, x1 = (b.x0 - 1.6, b.x0 + b.w * 0.3) if s < 0 else (b.x1 - b.w * 0.3, b.x1 + 1.6)
            xm = (x0 + x1) / 2
            out += [box((x0, top - 2.0, b.z0 - 0.7), (x1, top + 0.8, b.z1 + 0.7), ST),
                    box((x0, top - 2.4, b.z0 - 0.8), (x1, top - 2.0, b.z1 + 0.8), RUBY if fierce else G)]
            for dz, hh in ((-0.3, 2.6), (0.35, 1.8)):
                z = b.cz + dz * b.d
                out += [box((xm - 0.5, top + 0.8, z - 0.5), (xm + 0.5, top + 0.8 + hh * 0.7, z + 0.5), STL),
                        box((xm - 0.25, top + 0.8 + hh * 0.7, z - 0.25), (xm + 0.25, top + 0.8 + hh, z + 0.25), BN)]
    elif kind == 'cape':                               # (it hangs back from the shoulders, clear of a skirt or a tail)
        y0 = b.y0 + H * 0.06
        sw = ('x', -22.5, (b.cx, top, b.z1 + 0.5))
        return [dict(e, rotation={'origin': list(sw[2]), 'axis': 'x', 'angle': sw[1]}) for e in _cape(b, y0, top)]
    elif kind == 'bolts':                              # crackling lightning bolts out of his back and shoulders (a beast: no clothes)
        def bolt(x, y, z, sx, l):
            # a zigzag: out from the hide, a kink across, out again to a point
            return [box((x - 0.55, y - 0.55, z - 0.3), (x + 0.55, y + 0.55, z + l * 0.45), FL_Y),
                    box((x - 0.5, y - 0.5, z + l * 0.35), (x + sx * l * 0.4 + 0.5, y + 0.5, z + l * 0.45 + 0.9), FL_Y),
                    box((x + sx * l * 0.4 - 0.45, y - 0.45, z + l * 0.45 + 0.6), (x + sx * l * 0.4 + 0.45, y + 0.45, z + l), FL_O),
                    box((x + sx * l * 0.4 - 0.2, y - 0.2, z + l - 0.1), (x + sx * l * 0.4 + 0.2, y + 0.2, z + l + 0.7), GL)]
        for f, dx, sx, l in ((0.92, -1.6, -1, 4.2), (0.92, 1.6, 1, 4.2), (0.66, -0.9, 1, 3.6), (0.66, 0.9, -1, 3.6), (0.42, 0.0, 1, 3.0)):
            out += bolt(b.cx + dx, b.y0 + b.h * f, b.z1, sx, l)
        for sx in (-1, 1):                             # (and a spark off each shoulder, upward)
            x = b.x0 + 1.0 if sx < 0 else b.x1 - 1.0
            out += [box((x - 0.5, top - 0.3, b.cz - 0.5), (x + 0.5, top + 2.2, b.cz + 0.5), FL_Y),
                    box((x - 0.5, top + 1.6, b.cz - 0.5), (x + sx * 1.6, top + 2.4, b.cz + 0.5), FL_Y),
                    box((x + sx * 1.6 - 0.45, top + 2.0, b.cz - 0.45), (x + sx * 1.6 + 0.45, top + 3.8, b.cz + 0.45), FL_O)]
    elif kind == 'spines':                             # a ridge of bone spines down the back
        for i, f in enumerate((0.96, 0.8, 0.64, 0.48, 0.32)):
            y = b.y0 + H * f
            l = 2.6 - 0.3 * i
            out += [box((b.cx - 0.45, y - 1.6, b.z1 - 0.3), (b.cx + 0.45, y, b.z1 + l), BN, rot=('x', 22.5, (b.cx, y - 0.8, b.z1))),
                    box((b.cx - 0.3, y - 1.2, b.z1 + l - 0.6), (b.cx + 0.3, y - 0.5, b.z1 + l + 0.6), BND, rot=('x', 22.5, (b.cx, y - 0.8, b.z1)))]
    elif kind == 'breastplate':
        y0 = top - H * 0.6
        out += [box((b.x0 - 0.2, y0, b.z0 - 0.7), (b.x1 + 0.2, top - 0.2, b.z0 - 0.15), STL),
                box((b.x0 - 0.3, y0 - 0.3, b.z0 - 0.8), (b.x1 + 0.3, y0 + 0.2, b.z0 - 0.1), G),
                box((b.cx - 0.9, top - H * 0.35, b.z0 - 0.95), (b.cx + 0.9, top - H * 0.15, b.z0 - 0.7), SAPH)]
    elif kind == 'ruff':                               # a royal collar
        out += ring(b, top - 0.8, top + 0.6, PEARL, pad=0.3, th=0.9)
        out += ring(b, top - 1.1, top - 0.7, G, pad=0.4, th=1.0)
    elif kind == 'collar':                             # a gold collar with spikes (or studs, for the sweet ones)
        b2 = BB([(b.x0, b.x1), (b.y0, b.y1), (b.z0, b.z0 + min(b.d, 4.0))]) if b.d > b.h else b
        y0 = top - 1.6
        out += ring(b2, y0, y0 + 1.2, G, pad=0.25, th=0.6)
        out += points(b2, y0 + 1.2, 2, 1.0, GL, pad=0.25, size=0.6)
    elif kind == 'blanket':                            # a war-blanket over a beast's back, gold-hemmed, the sea-star on it
        out += [box((b.x0 - 0.6, top, b.z0 + b.d * 0.15), (b.x1 + 0.6, top + 0.5, b.z1 - b.d * 0.1), P),
                box((b.x0 - 0.8, top - H * 0.45, b.z0 + b.d * 0.15), (b.x0 - 0.3, top + 0.5, b.z1 - b.d * 0.1), P),
                box((b.x1 + 0.3, top - H * 0.45, b.z0 + b.d * 0.15), (b.x1 + 0.8, top + 0.5, b.z1 - b.d * 0.1), P),
                box((b.x0 - 0.9, top - H * 0.5, b.z0 + b.d * 0.13), (b.x0 - 0.2, top - H * 0.4, b.z1 - b.d * 0.08), G),
                box((b.x1 + 0.2, top - H * 0.5, b.z0 + b.d * 0.13), (b.x1 + 0.9, top - H * 0.4, b.z1 - b.d * 0.08), G),
                box((b.cx - 1.4, top + 0.5, b.cz - 1.4), (b.cx + 1.4, top + 0.75, b.cz + 1.4), G),
                box((b.cx - 0.6, top + 0.75, b.cz - 0.6), (b.cx + 0.6, top + 0.95, b.cz + 0.6), SAPH)]
    elif kind == 'sash':                               # a royal sash, shoulder to hip, with a rosette
        out += [box((b.cx - 0.8, b.y0 + H * 0.15, b.z0 - 0.5), (b.cx + 0.8, top + 0.4, b.z0 - 0.1), P, rot=('z', 45 if b.w > 6 else 22.5, (b.cx, b.y0 + H * 0.6, b.z0))),
                box((b.cx - 1.3, b.y0 + H * 0.3, b.z0 - 0.75), (b.cx + 1.3, b.y0 + H * 0.3 + 2.6, b.z0 - 0.45), G)]
    elif kind == 'belt':
        y0 = b.y0 + H * 0.25
        out += ring(b, y0, y0 + 1.1, PD, pad=0.2, th=0.5)
        out.append(box((b.cx - 1.2, y0 - 0.3, b.z0 - 1.0), (b.cx + 1.2, y0 + 1.4, b.z0 - 0.6), G))
    return out


def medal(b, beast=False, at=None, k=None):
    """the Champion's medal: a sapphire-and-ruby ribbon in a V, a rimmed gold medal with a raised sapphire sea-star, sized to
    the chest it hangs on and laid flush on it (a beast wears it on its breast, in the middle). at: (x, y, z) found by
    place_medal - where it lies flat and whole on the chest, clear of everything else"""
    k = k or max(0.7, min(1.1, b.w / 8, b.h / 7))
    if at:
        x, y, z = at
    elif beast:
        x, y, z = b.cx, b.y0 + b.h * beast, b.z0 - 0.02
    else:
        x, y, z = b.cx + b.w * 0.24, b.y1 - min(4.2 * k, b.h * 0.38), b.z0 - 0.02
    # the ribbon: a striped bar (sapphire, pearl, sapphire) on a gold pin, the medal hung from it
    rw, rt, rb = 1.15 * k, y + 3.4 * k, y + 1.2 * k
    out = [box((x - rw, rb, z - 0.3), (x - rw / 3, rt, z), SAPH), box((x - rw / 3, rb, z - 0.3), (x + rw / 3, rt, z), PEARL),
           box((x + rw / 3, rb, z - 0.3), (x + rw, rt, z), SAPH),
           box((x - rw - 0.15, rt - 0.1, z - 0.45), (x + rw + 0.15, rt + 0.45, z), G),                              # (the pin)
           box((x - 0.4 * k, rb - 0.5 * k, z - 0.4), (x + 0.4 * k, rb + 0.3 * k, z - 0.2), GD)]                     # (the loop)
    # the medal: an eight-sided rim, a gold face, the star
    out += [box((x - 1.7 * k, y - 0.75 * k, z - 0.45), (x + 1.7 * k, y + 0.75 * k, z), GD),
            box((x - 0.75 * k, y - 1.7 * k, z - 0.45), (x + 0.75 * k, y + 1.7 * k, z), GD),
            box((x - 1.25 * k, y - 1.25 * k, z - 0.45), (x + 1.25 * k, y + 1.25 * k, z), GD),
            box((x - 1.35 * k, y - 0.55 * k, z - 0.6), (x + 1.35 * k, y + 0.55 * k, z - 0.3), G),
            box((x - 0.55 * k, y - 1.35 * k, z - 0.6), (x + 0.55 * k, y + 1.35 * k, z - 0.3), G),
            box((x - 1.0 * k, y - 1.0 * k, z - 0.6), (x + 1.0 * k, y + 1.0 * k, z - 0.3), G),
            box((x - 0.25 * k, y - 0.95 * k, z - 0.8), (x + 0.25 * k, y + 0.95 * k, z - 0.55), SAPH),
            box((x - 0.95 * k, y - 0.25 * k, z - 0.8), (x + 0.95 * k, y + 0.25 * k, z - 0.55), SAPH),
            box((x - 0.5 * k, y - 0.5 * k, z - 0.85), (x + 0.5 * k, y + 0.5 * k, z - 0.6), SAPH),
            box((x - 0.18 * k, y - 0.18 * k, z - 0.95), (x + 0.18 * k, y + 0.18 * k, z - 0.8), PEARL),
            box((x - 1.0 * k, y + 0.55 * k, z - 0.68), (x - 0.55 * k, y + 0.95 * k, z - 0.55), GL)]                # (a glint)
    return out


# (2.93b) those who already wear a crown or a hat get no second one: an ornament on their own instead - a crystal in their colour
# standing up out of the crown, or pinned to the hat's band (a crystal or a rose bud). who: (ornament, where)
ORNAMENT = {'apo': ('crystal', 'top'), 'omega': ('crystal', 'top'), 'ashur': ('crystal', 'top'), 'ava': ('crystal', 'top'),
            'pearlq': ('crystal', 'top', {'x': 7.05, 'y': 18.0, 'z': 8.0, 'k': 0.6}),         # (her little crown sits to one side)
            'tul': ('crystal', 'pin', {'y': 17.6}),                                          # (his skull is small: the hat is his biggest piece)
            'dennis': ('crystal', 'pin'), 'pistachio': ('rose', 'pin'), 'chef': ('rose', 'pin'), 'neighbor': ('rose', 'pin'),
            'leo': ('crystal', 'brow'), 'demo': ('crystal', 'brow'), 'cecil': ('crystal', 'brow')}


def _front(els, x, y, r=0.35):
    """the frontmost face (least z) of a bone's model over a little patch at (x, y)"""
    hit = [e[2][0] for e in els if e[0][0] < x + r and e[0][1] > x - r and e[1][0] < y + r and e[1][1] > y - r]
    return min(hit) if hit else None


def ornament(kind, x, y, z, k, up=True):
    """a crystal cluster (the follower's colour, a pearl glint) on a gold setting, or a red rose bud on a leaf - its base at
    (x, y), its back at z (or, standing up out of a crown, its middle at z)"""
    if kind == 'crystal':
        zc = z if up else z - 0.75 * k
        out = [box((x - 1.1 * k, y, zc - 0.7 * k), (x + 1.1 * k, y + 0.6 * k, zc + 0.7 * k), G),                       # (the setting)
               box((x - 0.5 * k, y + 0.4 * k, zc - 0.5 * k), (x + 0.5 * k, y + 3.4 * k, zc + 0.5 * k), P, rot=('y', 45, (x, y, zc))),
               box((x - 0.25 * k, y + 3.3 * k, zc - 0.25 * k), (x + 0.25 * k, y + 3.9 * k, zc + 0.25 * k), PEARL, rot=('y', 45, (x, y, zc))),
               box((x - 1.25 * k, y + 0.3 * k, zc - 0.35 * k), (x - 0.55 * k, y + 2.2 * k, zc + 0.35 * k), PL, rot=('z', 22.5, (x - 0.9 * k, y, zc))),
               box((x + 0.55 * k, y + 0.3 * k, zc - 0.35 * k), (x + 1.25 * k, y + 1.8 * k, zc + 0.35 * k), PL, rot=('z', -22.5, (x + 0.9 * k, y, zc))),
               box((x - 0.3 * k, y + 2.5 * k, zc - 0.62 * k), (x - 0.05 * k, y + 3.0 * k, zc - 0.52 * k), PEARL)]              # (a glint)
        return out
    zc = z - 0.8 * k                                                       # the rose bud: leaves, a cupped bud, its petals curled round
    return [box((x - 1.6 * k, y - 0.2 * k, zc - 0.4 * k), (x - 0.2 * k, y + 0.4 * k, zc + 0.6 * k), LEAF, rot=('z', 22.5, (x - 0.2 * k, y, zc))),
            box((x + 0.2 * k, y - 0.2 * k, zc - 0.4 * k), (x + 1.6 * k, y + 0.4 * k, zc + 0.6 * k), LEAF, rot=('z', -22.5, (x + 0.2 * k, y, zc))),
            box((x - 0.7 * k, y + 0.2 * k, zc - 0.7 * k), (x + 0.7 * k, y + 1.6 * k, zc + 0.7 * k), RUBY),
            box((x - 0.85 * k, y + 0.3 * k, zc - 0.85 * k), (x + 0.85 * k, y + 1.1 * k, zc + 0.85 * k), RUBY, rot=('y', 45, (x, y, zc))),
            box((x - 0.4 * k, y + 1.5 * k, zc - 0.4 * k), (x + 0.4 * k, y + 2.1 * k, zc + 0.4 * k), RUBY, rot=('y', 22.5, (x, y, zc))),
            box((x - 0.15 * k, y + 1.9 * k, zc - 0.15 * k), (x + 0.15 * k, y + 2.2 * k, zc + 0.15 * k), PD)]


def _ornament(who, hb):
    if who not in ORNAMENT: return []
    kind, where, at = (ORNAMENT[who] + ({},))[:3]
    els, c = hb['els'], hb['core']
    cx, cz, w = (c[0][0] + c[0][1]) / 2, (c[2][0] + c[2][1]) / 2, c[0][1] - c[0][0]
    k = at.get('k', max(0.7, min(1.1, w / 8)))
    if where == 'top':                                              # (out of the crown's middle, its foot sunk in it)
        return ornament(kind, at.get('x', cx), at.get('y', hb['top'] - 1.2 * k), at.get('z', cz), k)
    if where == 'brow':                                             # (a jewel at the front of a helm or a hood, over the brow)
        y = c[1][1] - 1.6 * k
        return ornament(kind, cx, y, _front(els, cx, y + 1.0) - 0.02, k * 0.8, up=False)
    # (pinned to a hat's band, off to one side: the hat is the biggest piece sitting on the skull)
    hats = [e for e in els if e != c and e[1][0] >= c[1][1] - 3 and e[0][0] <= cx <= e[0][1] and e[2][0] <= cz <= e[2][1]]
    hat = max(hats, key=lambda e: (e[0][1] - e[0][0]) * (e[1][1] - e[1][0]) * (e[2][1] - e[2][0])) if hats else c
    y0, y1 = min(e[1][0] for e in hats or [c]), max(e[1][1] for e in hats or [c])
    x, y = cx + (hat[0][1] - hat[0][0]) * 0.27, at.get('y', y0 + (y1 - y0) * 0.22)      # (low on the hat: its band)
    return ornament(kind, x, y, _front(els, x, y + 1.0 * k) - 0.02, k * 0.85, up=False)


# (2.93c) worn on the face instead: the Arachno-Lantern's pinned to the middle of his pumpkin - its disc over the nose, its
# ribbon up between the eyes. Measured on the head's biggest block (the pumpkin, its face on the front - the model is stored
# shrunk, so design units won't do): how far up the face the disc sits, and its size for each 22 units of face width
MEDAL_FACE = {'lantern': (0.45, 0.95)}
SIDE_MEDAL = {'bones'}                    # (the owner's call: Bones wears his on his side)
BEASTS = {'bender': 0.5, 'bones': 0.45, 'lantern': 0.5, 'fishy': 0.16, 'frog': 0.45}   # (a beast's medal, on its breast: how high)


# per follower: drop (start lower: a low neckline, so the ribbon starts on the dress, not the skin); k (a smaller medal); over
# (it may lie over the regalia - Dennis's beard covers his chest, so his hangs below it, on his belt)
MEDAL_OPT = {'ashur': {'drop': 3.5}, 'pearlq': {'drop': 3.5}, 'dennis': {'k': 0.72, 'over': True}}


def _covers(e, x, y):
    """does a regalia element, seen from the front, cover the point (x, y)? (a sash turned on z, its true slant)"""
    (fx, fy, _fz), (tx, ty, _tz) = e['from'], e['to']
    r = e.get('rotation')
    if r and r.get('axis') == 'z' and r.get('angle'):
        o, a = r['origin'], math.radians(-r['angle'])
        dx, dy = x - o[0], y - o[1]
        x, y = o[0] + dx * math.cos(a) - dy * math.sin(a), o[1] + dx * math.sin(a) + dy * math.cos(a)
    elif r:
        (fx, tx), (fy, ty), _ = _aabb(e)
    return fx - 0.15 < x < tx + 0.15 and fy - 0.15 < y < ty + 0.15


def place_medal(b, bb, hb, body, beast, opt=None, why=None):
    """where the medal lies flat and whole: on the chest's own front (not inside a high collar behind it), every bit of it
    showing - clear of the regalia in front (a sash, a ruff, pauldrons), of the head's hanging parts (a beard, a jaw), off
    any lapel or brooch - stepping down, then aside, until it fits. A beast's hangs in front of its collar. Failing all that:
    where it always went, brought forward of everything there"""
    opt = opt or {}
    els, k = bb['els'], opt.get('k', max(0.7, min(1.1, b.w / 8, b.h / 7)))
    drop, over = opt.get('drop', 0.0), opt.get('over', False)
    c, u = bb['core'], bb['upper']
    # the trunk's front: the chest's, unless the 'chest' found is a high collar standing behind (Tullius's) - then the trunk's
    f0 = b.z0 if beast else (c[2][0] if (u[2][0] + u[2][1]) / 2 > c[2][1] - 1 else min(u[2][0], c[2][0] + 3))
    near = [e for e in els if e[2][0] <= f0 + 1.5 and e[0][0] < b.cx + b.w * 0.25 and e[0][1] > b.cx - b.w * 0.25]
    top = max(e[1][1] for e in near) if near and not beast else b.y1
    # the head's hanging parts, as they fall over the chest (the head sits on the chest's top)
    vol = lambda e: (e[0][1] - e[0][0]) * (e[1][1] - e[1][0]) * (e[2][1] - e[2][0])
    hc = hb['core']
    chin = min(e[1][0] for e in hb['els'] if vol(e) >= vol(hc) * 0.25)      # (the skull's foot: under a hat that is bigger than it)
    hang = [(e[0][0], e[0][1], top - (chin - e[1][0]), top + 9) for e in hb['els']
            if e[1][0] < chin - 0.5 and (e[2][0] + e[2][1]) / 2 < (hc[2][0] + hc[2][1]) / 2] if not beast else []
    front = [e for e in body if _aabb(e)[2][0] < f0 + 1.0]          # (the regalia in front: not a cape behind)
    surf = els + ([_aabb(e) for e in front] if beast or over else [])   # (a beast's medal hangs on its collar)
    keep = [] if beast or over else front
    xs = (0,) if beast else (0.24, -0.24, 0.3, -0.3, 0.12, -0.12)
    y0 = b.y0 + b.h * beast if beast else top - min(4.2 * k, b.h * 0.38) - drop
    grid = lambda r: [(r[0] + (r[1] - r[0]) * i / 4, r[2] + (r[3] - r[2]) * j / 6) for i in range(5) for j in range(7)]
    for dy in range(10) if not beast else (0, 1, -1, 2):
        for fx in xs:
            x, y = b.cx + b.w * fx, y0 - dy
            r = (x - 1.75 * k, x + 1.75 * k, y - 1.75 * k, y + 3.9 * k)
            if r[2] < b.y0 + 0.5 or (not beast and (r[0] < b.x0 - 0.2 or r[1] > b.x1 + 0.2)):
                if why is not None: why.append(('off', round(x, 1), round(y, 1)))
                continue
            pts = grid(r)
            if any(a[0] < r[1] and a[1] > r[0] and a[2] < r[3] and a[3] > r[2] for a in hang) or \
                    any(_covers(e, px, py) for e in keep for px, py in pts):
                if why is not None: why.append(('covered', round(x, 1), round(y, 1)))
                continue
            fr = [_front(surf, px, py, 0.2) for px, py in pts]
            if None in fr or max(fr) - min(fr) > (1.7 if over else 1.0):
                if why is not None: why.append(('bumpy', round(x, 1), round(y, 1), None if None in fr else round(max(fr) - min(fr), 2)))
                continue
            return (x, y, min(fr) - 0.02)
    x, y = (b.cx, y0) if beast else (b.cx + b.w * 0.24, y0)
    fr = [f for f in (_front(els + [_aabb(e) for e in front], px, py, 0.2) for px, py in grid((x - 1.75 * k, x + 1.75 * k, y - 1.75 * k, y + 3.9 * k))) if f is not None]
    return (x, y, min(fr + [b.z0]) - 0.02)


def models(who, hb, bb):
    """(head piece, body piece, medal) element lists for one follower, from its head and body bones' bounds"""
    head_k, body_k, fierce, _aura = STYLE[who]
    c, f0 = hb['core'], hb['full']
    h = BB(f0 if ANCHORS[who][1] == ANCHORS[who][3] else [c[0], (c[1][0], max(c[1][1], hb['top'])), c[2]])   # (on top of hair and hats)
    u, f = (bb['full'] if who in WHOLE_BODY else bb['upper']), bb['full']
    b = BB([u[0], (f[1][0], u[1][1]), u[2]])                        # (the chest's width and depth, the whole body's height)
    hk = 'crown_top' if head_k == 'crown_top' else head_k
    head = (head_piece(hk, h) if hk else []) + _ornament(who, hb)
    body = [e for k in body_k for e in body_piece(k, b, fierce)]
    if who in MEDAL_FACE:
        fy, kk = MEDAL_FACE[who]
        (x0, x1), (y0, y1), (z0, _z1) = hb['core']
        k = kk * (x1 - x0) / 22
        return head, body, medal(b, at=((x0 + x1) / 2, y0 + (y1 - y0) * fy, z0 - 0.02), k=k)
    if who in SIDE_MEDAL:                                           # (worn on the flank: the medal made as for a body turned side-on, turned back)
        v = BB([(b.z0, b.z1), (b.y0, b.y1), (b.x0, b.x1)])
        med = []
        for e in medal(v, BEASTS.get(who, 0)):
            (fx, fy, fz), (tx, ty, tz) = e['from'], e['to']
            dz = 0.22 * (b.z1 - b.z0)                               # (toward his head, clear of the skull on his flank)
            med.append(dict(e, **{'from': [round(b.x0 + b.x1 - tz, 3), fy, round(fx + dz, 3)], 'to': [round(b.x0 + b.x1 - fz, 3), ty, round(tx + dz, 3)]}))
        return head, body, med
    beast = BEASTS.get(who, 0)
    opt = MEDAL_OPT.get(who, {})
    return head, body, medal(b, beast, place_medal(b, bb, hb, body, beast, opt), opt.get('k'))


def _resolve(src, mid):
    it = json.load(open(src('assets', 'bm', 'items', f'{mid}.json')))['model']
    while True:
        t = it.get('type')
        if t == 'minecraft:select': it = it['fallback']
        elif t == 'minecraft:condition': it = it['on_false']
        elif t == 'minecraft:composite': it = it['models'][0]
        else: break
    ns, path = it['model'].split(':')
    j = json.load(open(src('assets', ns, 'models', *path.split('/')) + '.json'))
    els = [_aabb(e) for e in j['elements']]                         # (each element's true bounds, turned as it is turned)
    full = [(min(e[i][0] for e in els), max(e[i][1] for e in els)) for i in range(3)]
    vol = lambda e: (e[0][1] - e[0][0]) * (e[1][1] - e[1][0]) * (e[2][1] - e[2][0])
    core = max(els, key=vol)                                        # (a head: its skull, not its hair and ears)
    top = [e for e in els if e[1][1] >= full[1][1] - 2.5 and e[0][1] - e[0][0] >= 2] or els
    upper = max(top, key=vol)                                       # (a body: the chest at its top, not the skirt)
    cx, cz = (core[0][0] + core[0][1]) / 2, (core[2][0] + core[2][1]) / 2
    mid = [e for e in els if e[0][0] <= cx <= e[0][1] and e[2][0] <= cz <= e[2][1]] or [core]
    return {'full': full, 'core': core, 'upper': upper, 'top': max(e[1][1] for e in mid), 'els': els}, j.get('display', {}).get('fixed')


def _aabb(e):
    """an element's axis-aligned bounds after its rotation (either form: axis + angle, or x/y/z degrees)"""
    pts = [[x, y, z] for x in (e['from'][0], e['to'][0]) for y in (e['from'][1], e['to'][1]) for z in (e['from'][2], e['to'][2])]
    r = e.get('rotation')
    if r:
        o = r.get('origin', [8, 8, 8])
        turns = [(r['axis'], r['angle'])] if 'axis' in r else [(a, r.get(a, 0)) for a in ('x', 'y', 'z')]
        for axis, ang in turns:
            if not ang: continue
            c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            i, k = {'x': (1, 2), 'y': (2, 0), 'z': (0, 1)}[axis]
            for p in pts:
                a, b = p[i] - o[i], p[k] - o[k]
                p[i], p[k] = o[i] + a * c - b * s_, o[k] + a * s_ + b * c
    return [(min(p[i] for p in pts), max(p[i] for p in pts)) for i in range(3)]


def build(R2, src=None):
    """every follower's three pieces and sheet, written into the pack (the bones read from src: the pack itself by default)"""
    src = src or R2.p
    for who, (_ht, hm, _bt, bm_) in ANCHORS.items():
        hb, hdisp = _resolve(src, hm)
        bb, bdisp = _resolve(src, bm_)
        head, body, med = models(who, hb, bb)
        sheet(who).save(R2.p('assets', 'bm', 'textures', 'block', f'champ_{who}.png'))
        for part, els, disp in (('head', head, hdisp), ('body', body, bdisp), ('medal', med, hdisp if who in MEDAL_FACE else bdisp)):
            if not els: continue
            name = f'champ_{who}_{part}'
            m = {'textures': {'t': f'bm:block/champ_{who}', 'particle': f'bm:block/champ_{who}'}, 'elements': els or [box((8, 8, 8), (8.05, 8.05, 8.05), G)]}
            if disp: m['display'] = {'fixed': disp}
            R2.wj(f'assets/bm/models/item/{name}.json', m)
            R2.wj(f'assets/bm/items/{name}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/{name}'}})
    # Wilfrey (a real wither skeleton, no display bones): a crown and a medal of his own, worn from his body's place
    wil_medal = medal(BB([(4.0, 12.0), (0.0, 12.0), (6.0, 10.0)]))
    sheet('wil').save(R2.p('assets', 'bm', 'textures', 'block', 'champ_wil.png'))
    for part, els in (('medal', wil_medal),):
        R2.wj(f'assets/bm/models/item/champ_wil_{part}.json', {'textures': {'t': 'bm:block/champ_wil', 'particle': 'bm:block/champ_wil'}, 'elements': els})
        R2.wj(f'assets/bm/items/champ_wil_{part}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/champ_wil_{part}'}})


COL['wil'] = '#f4f4f4'


def ribbon_icon():
    """the Champion's Ribbon: a gold medal on a sea-blue ribbon"""
    from PIL import ImageDraw
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(3, 0), (7, 0), (9, 7), (6, 8)], fill=(40, 120, 200, 255), outline=(20, 60, 120, 255))
    d.polygon([(13, 0), (9, 0), (7, 7), (10, 8)], fill=(60, 170, 230, 255), outline=(20, 60, 120, 255))
    d.ellipse((3, 6, 13, 15), fill=(232, 182, 48, 255), outline=(150, 100, 20, 255))
    d.ellipse((5, 8, 11, 13), fill=(255, 216, 100, 255))
    d.point([(8, 9), (7, 10), (9, 10), (8, 11), (8, 10)], fill=(40, 90, 220, 255)); d.point((6, 8), fill=(255, 255, 255, 255))
    return im


def rp(R):
    R.POST.append(build)
    R.ICONS['champion_ribbon'] = ribbon_icon()

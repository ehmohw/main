"""2.77b: FOLLOWER FIGURINES - a follower's summoning item in a display case shows a little statue of them instead: posed,
still as stone (no AI - display parts only, like a Smuggler's Jar's creature on its cushion), facing out of the case.
Punch the case to switch between the figurine and the item itself (sneak + punch still picks the case up); sneak +
right-click turns it, as it turns anything; take the item out (empty-handed) or pick the case up and the figurine goes.

Every follower with a summoning item: Cecil (his gem), Emma (her ribbon), Celi (her charm), Zib (the Donadian Medal),
KillerWatt (the Spark), Leo (his crest), Democratus (his seal), Apophiss (the Oath), Tullius (the coin) and Pearlman (his
business card). Each is built from the follower's own rig and an idle pose, then shrunk to fit: about 0.6 blocks tall
in a floor case, 0.5 on a wall (and no deeper than a wall case is).
"""
import math
from nbt import snbt, F, Int

IDENT = (0.0, 0.0, 0.0, 1.0)

# (the cases' own lore says so)
from items import ITEMS as _ITEMS, T as _T
for _v in [k for k in _ITEMS if k.startswith('display_case_')]:
    _L = _ITEMS[_v]['comps'].get('minecraft:lore')
    if _L is not None:
        _L.insert(len(_L) - 1 if len(_L) > 1 else len(_L), _T("A follower's item in it: their figurine (punch: the item).", 'gray'))


def _qy(a):
    return (0.0, math.sin(math.radians(a) / 2), 0.0, math.cos(math.radians(a) / 2))


# ------------------------------------------------------------------------------------------------ each follower, as parts
# (a part: model, translation in the figure's own frame - ^left ^up ^forward, blocks, at the follower's own size -, its
#  left and right rotations, its scale. All parts stand on one spot; the translations do the rest, as with the riders.)
def _jointed(art, models, pose, S, pivot=None, scale_of=None, skip=()):
    """the rigs whose part_xf gives (turn, shift in blocks): Leo, Celi, Democratus, Emma"""
    U = S / 16
    out = []
    for p in art.PARTS:
        if p in skip: continue
        x, y, z = pivot(p) if pivot else art.joint(p)
        rot, tr = art.part_xf(art.POSES[pose], p)[:2]
        out.append((models(p), (-x * U + tr[0], y * U + tr[1], -z * U + tr[2]), tuple(rot), IDENT, scale_of(p) if scale_of else S))
    return out


def _rigkit(art, pose, S):
    """the rigkit rigs (Apophiss, Tullius): the solved hierarchy"""
    import rigkit as RK
    U = S / 16
    xf = RK.solve(art.PIVOT, art.PARENT, pose)
    out = []
    for p in art.PARTS:
        if art.HIDDEN(p, pose): continue
        x, y, z = art.PIVOT[p]
        q, t = xf[p]
        out.append((f'bm:{art.model_name(p, pose)}', (-x * U + t[0] * U, y * U + t[1] * U, -z * U + t[2] * U), tuple(q), IDENT, S * art.PART_K.get(p, 1.0)))
    return out


def figures():
    import phase96_art as LEO, phase66_art as CELI, phase97_art as DEMO, phase57_art as EMMA, phase79_art as KW
    import apophiss_art as APO, tullius_art as TUL, phase72_art as ZIB, cecil2_art as CA
    F_ = {}
    F_['leo_crest'] = ('Leo', _jointed(LEO, lambda p: f'bm:le_{p}', 'idle_a', LEO.RIG_SCALE))
    F_['celi_charm'] = ('Celi', _jointed(CELI, lambda p: f'bm:ce_{p}', 'idle', CELI.RIG_SCALE))
    sk = round(DEMO.RIG_SCALE / DEMO.SCYTHE_K, 4)
    F_['demo_seal'] = ('Democratus', _jointed(DEMO, lambda p: f'bm:dm_{p}', 'idle_a', DEMO.RIG_SCALE, scale_of=lambda p: sk if p == 'scythe' else DEMO.RIG_SCALE))
    F_['emma_ribbon'] = ('Emma', _jointed(EMMA, lambda p: f'bm:em_{p}', 'idle_a', EMMA.RIG_SCALE, pivot=lambda p: EMMA.PIVOT[p],
                                          skip=[p for p in EMMA.PARTS if p.startswith('wing')]))
    # KillerWatt: part_xf gives (turn, shift in design units, lift in blocks at his boss size); the follower's size is 1.05
    S, U = 1.05, 1.05 / 16
    kw = []
    for p in KW.PARTS:
        x, y, z = KW.PIVOT[p]
        rot, (ox, oy, oz), dy = KW.part_xf(KW.POSES['idle_a'], p)
        kw.append((f'bm:kw_{p}', (-x * U + ox * U, y * U + oy * U + dy * S / KW.RIG_SCALE, -z * U + oz * U), tuple(rot), IDENT,
                   S * (KW.TEND_K if p in KW.TEND_PARTS else 1)))
    F_['kw_spark'] = ('KillerWatt', kw)
    F_['apo_oath'] = ('Apophiss', _rigkit(APO, APO.POSES['idle_a'], APO.PET_SCALE))
    F_['tul_coin'] = ('Tullius', _rigkit(TUL, TUL.POSES['idle_a'], TUL.RIG_SCALE))
    # Zib: phase63's rig (every part rides one spot; the solve gives each its turn and joint)
    rig = ZIB.zib_rig()
    sol = rig.solve(ZIB.zib_poses()['idle0'])
    F_['donadian_medal'] = ('Zib', [(f'bm:zbr_{n}', tuple(J), tuple(R), IDENT, rig.S) for n, (R, J) in sol.items()])
    # Cecil: five parts at their joints, standing easy (his staff arm and his free arm turned as he holds them)
    F_['cecil_gem'] = ('Cecil', [('bm:cec2_body', (0.0, 0.5, 0.0), IDENT, IDENT, 1.0), ('bm:cec2_head', (0.0, CA.HEAD_AT[1], CA.HEAD_AT[2]), IDENT, IDENT, 1.0),
                                 ('bm:cec2_eyes', (0.0, CA.HEAD_AT[1], CA.HEAD_AT[2]), IDENT, IDENT, 1.0),
                                 ('bm:cec2_arm', tuple(CA.ARM_AT), IDENT, _qy(CA.ARM_YAW), 1.0), ('bm:cec2_larm', tuple(CA.LARM_AT), IDENT, _qy(CA.LARM_YAW), 1.0)])
    # Pearlman: one model
    F_['pearl_card'] = ('Pearlman', [('bm:pearlman', (0.0, 0.275, 0.0), IDENT, IDENT, 0.55)])
    return F_


# (each figure's extent at its own size, measured with tools/render.py from the built resource pack - see measure() below:
#  in blocks, its own frame (^left ^up ^forward): lowest point, height, then its left-right and back-front spans)
FIT = {
    'leo_crest': (0.000, 2.165, -0.829, 0.497, -0.297, 0.348),   # Leo
    'celi_charm': (0.000, 1.973, -0.660, 0.511, -0.337, 0.328),   # Celi
    'demo_seal': (0.000, 3.363, -0.821, 1.715, -0.510, 0.824),   # Democratus
    'emma_ribbon': (0.000, 1.819, -0.379, 0.387, -0.395, 0.330),   # Emma
    'kw_spark': (0.000, 3.318, -1.176, 1.176, -0.662, 0.476),   # KillerWatt
    'apo_oath': (-0.092, 9.510, -3.444, 3.360, -5.491, 3.605),   # Apophiss (2.77d: his snout, his head tipped down)
    'tul_coin': (0.000, 3.143, -1.079, 1.084, -0.525, 1.087),   # Tullius (from his feet, not the harpoon's tip below them)
    'donadian_medal': (-0.850, 1.287, -0.309, 0.310, -0.287, 0.386),   # Zib
    'cecil_gem': (-0.041, 2.364, -0.938, 0.514, -0.361, 0.550),   # Cecil
    'pearl_card': (0.000, 1.083, -0.213, 0.399, -0.172, 0.258),   # Pearlman
}


def measure(rp):
    """(run by hand after the resource pack is built) prints FIT for every figure"""
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools'))
    from render import Scene
    import numpy as np
    for iid, (name, parts) in figures().items():
        s = Scene(rp)
        for model, tr, L, R, sc in parts:
            s.display(model.replace('bm:', 'bm:item/'), translation=tr, scale=sc, left=L, right=R)
        pts = np.array([v for f in s.faces for v in f[0]])
        lo, hi = pts.min(0), pts.max(0)
        print(f"    '{iid}': ({lo[1]:.3f}, {hi[1] - lo[1]:.3f}, {lo[0]:.3f}, {hi[0]:.3f}, {lo[2]:.3f}, {hi[2]:.3f}),   # {name}")


def generate(G):
    fn, title, PREFIX = G.fn, G.title, G.PREFIX
    from items import T, ITEMS
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    FIG = figures()
    tick = []
    item_d = '@e[type=minecraft:item_display,tag=bm.dcitem,distance=..0.05,limit=1]'
    case = '@e[type=minecraft:item_display,tag=bm.dcase,distance=..0.05,limit=1]'

    # ---- the figures: (at the cushion, turned as the case) its parts, shrunk to fit the case
    def summon_lines(iid, wall):
        lo, h, x0, x1, z0, z1 = FIT[iid]
        # (shrunk to fit - about 0.6 tall on a floor cushion, 0.5 on a wall, never wider or deeper than the glass - and centred in it)
        f = min(0.5 / h, 0.48 / (x1 - x0), 0.3 / (z1 - z0)) if wall else min(0.6 / h, 0.66 / (x1 - x0), 0.66 / (z1 - z0))
        cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
        out = []
        for model, (x, y, z), L, R, sc in FIG[iid][1]:
            n = {'Tags': ['bm.dcfg', 'bm.dcfgnew'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': model}},
                 'item_display': 'fixed', 'brightness': {'block': Int(13), 'sky': Int(13)},
                 'transformation': {'left_rotation': [F(round(v, 5)) for v in L], 'right_rotation': [F(round(v, 5)) for v in R],
                                    'translation': [F(round((x - cx) * f, 4)), F(round((y - lo) * f, 4)), F(round((z - cz) * f, 4))], 'scale': [F(round(sc * f, 4))] * 3}}
            out.append(f'summon minecraft:item_display ~ ~ ~ {snbt(n)}')
        return out + ['execute as @e[type=minecraft:item_display,tag=bm.dcfgnew,distance=..0.1] run tp @s ~ ~ ~ ~ 0',
                      'tag @e[type=minecraft:item_display,tag=bm.dcfgnew,distance=..0.1] remove bm.dcfgnew']
    for iid in FIG:
        fn(f'p134/fig/floor_{iid}', summon_lines(iid, False))
        fn(f'p134/fig/wall_{iid}', summon_lines(iid, True))
    # (as the case's click box, at it) which follower's item is in the case - and its figure, on the cushion
    fn('p134/fig/show', ['kill @e[type=minecraft:item_display,tag=bm.dcfg,distance=..0.8]'] +
       [f'execute if items entity {item_d} contents {holds(iid)} unless entity @s[nbt={{width:0.6f}}] rotated as {case.replace("distance=..0.05", "distance=..0.6")} '
        f'positioned ~ ~0.25 ~ run function bm:p134/fig/floor_{iid}' for iid in FIG] +
       [f'execute if items entity {item_d} contents {holds(iid)} if entity @s[nbt={{width:0.6f}}] rotated as {case.replace("distance=..0.05", "distance=..0.6")} '
        f'positioned ^ ^0.05 ^-0.03 run function bm:p134/fig/wall_{iid}' for iid in FIG] +
       [f'execute if entity @e[type=minecraft:item_display,tag=bm.dcfg,distance=..0.8] run data merge entity {item_d} {{transformation:{{scale:[0f,0f,0f]}}}}',
        'execute if entity @e[type=minecraft:item_display,tag=bm.dcitem,tag=bm.dcspin,distance=..0.05] run tag @e[type=minecraft:item_display,tag=bm.dcfg,distance=..0.8] add bm.dcmspin',
        'particle minecraft:wax_on ~ ~0.6 ~ 0.2 0.25 0.2 0 10', 'playsound minecraft:block.amethyst_block.chime block @a[distance=..16] ~ ~ ~ 0.7 1.4'])
    fn('p134/fig/is_fol', [f'execute if items entity {item_d} contents {holds(iid)} run return 1' for iid in FIG] + ['return 0'])
    # put in: the figure, and how to have the item instead
    put = G.FUNCS['p72/dc/put']
    k = next(i for i, l in enumerate(put) if 'set_count",count:1' in l)
    put.insert(k + 1, 'execute as @e[type=minecraft:interaction,tag=bm.dcme,limit=1] at @s if function bm:p134/fig/is_fol run function bm:p134/fig/shown')
    fn('p134/fig/shown', ['function bm:p134/fig/show',
                          'execute on target run ' + say('A little statue of them, on the cushion. (Punch the case to show the item instead.)', '#e8d29a')])
    # taken out, or the case picked up: the figure goes (with the jar's creature - p73/dcm/clear runs on both)
    G.FUNCS['p73/dcm/clear'].insert(0, 'kill @e[type=minecraft:item_display,tag=bm.dcfg,distance=..0.8]')
    # punched (not sneaking): figure <-> item, when it's a follower's item; anything else, as before
    pn = G.FUNCS['p72/dc/punch']
    j = next(i for i, l in enumerate(pn) if 'unless predicate bm:p20/sneaking run' in l)
    pn[j] = 'execute if score #fgt bm.rng matches 0 ' + pn[j][len('execute '):]
    pn[j:j] = ['scoreboard players set #fgt bm.rng 0', 'execute on attacker unless predicate bm:p20/sneaking run function bm:p134/fig/punch']
    fn('p134/fig/punch', ['execute as @e[type=minecraft:interaction,tag=bm.dcme,limit=1] at @s unless function bm:p134/fig/is_fol run return 0',
                          'scoreboard players set #fgt bm.rng 1',
                          'execute as @e[type=minecraft:interaction,tag=bm.dcme,limit=1] at @s if entity @e[type=minecraft:item_display,tag=bm.dcfg,distance=..0.8] '
                          'run return run function bm:p134/fig/to_item',
                          'execute as @e[type=minecraft:interaction,tag=bm.dcme,limit=1] at @s run function bm:p134/fig/show',
                          say('The figurine. (Punch again for the item.)', '#e8d29a')])
    fn('p134/fig/to_item', ['kill @e[type=minecraft:item_display,tag=bm.dcfg,distance=..0.8]',
                            f'data merge entity {item_d} {{transformation:{{scale:[0.5f,0.5f,0.5f]}}}}',
                            'particle minecraft:wax_off ~ ~0.6 ~ 0.2 0.25 0.2 0 8', 'playsound minecraft:block.amethyst_block.place block @a[distance=..16] ~ ~ ~ 0.7 1.2',
                            'execute on attacker run ' + say('The item itself. (Punch again for the figurine.)', '#e8d29a')])
    # (the case's turn: the figure turns with it)
    G.FUNCS['p72/dc/spin_toggle'] += ['execute as @e[type=minecraft:interaction,tag=bm.dcme,limit=1] at @s run tag @e[type=minecraft:item_display,tag=bm.dcfg,distance=..0.8] add bm.dcmspin']
    G.FUNCS['p72/dc/spin_off'] += ['execute as @e[type=minecraft:interaction,tag=bm.dcme,limit=1] at @s run tag @e[type=minecraft:item_display,tag=bm.dcfg,distance=..0.8] remove bm.dcmspin']
    # (a figure whose case is gone - broken some other way - goes too)
    G.FUNCS['loop/second'][-1:-1] = ['execute as @e[type=minecraft:item_display,tag=bm.dcfg] at @s unless entity @e[type=minecraft:interaction,tag=bm.dchit,distance=..0.9] run kill @s']
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[type=minecraft:item_display,tag=bm.dcfg]')

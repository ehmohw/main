"""2.77: rigkit rigs in the game (Apophiss, Tullius).

As phase79/phase96 do it: one item display per part, teleported every tick to its rest joint (turned with the host),
its transformation interpolated from pose to pose. The difference: a pose here is rigkit's - each joint's own bend, the
tree solved in Python (rigkit.solve) into each display's left_rotation and translation. A part a pose hides goes to
scale 0 in the same merge (the blunderbuss slung away, the wings folded out of sight), and a part with a per-pose
model (the iced harpoon) has it set there too."""
from nbt import snbt, F, Int, B
import rigkit as RK

IDENT = [F(0), F(0), F(0), F(1)]


def qf(q):
    return [F(round(v, 5)) for v in q]


def part_nbt(art, p, tags, S, model=None, extra=None, scale0=False):
    """a part's display: summoned at scale 0 when it should appear in a burst (scale0), else at its own size"""
    k = getattr(art, 'PART_K', {}).get(p, 1.0)
    n = {'Tags': list(tags), 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:{model or art.PREFIX + p}'}},
         'item_display': 'fixed', 'teleport_duration': Int(2), 'interpolation_duration': Int(6), 'start_interpolation': Int(0),
         'transformation': {'left_rotation': IDENT, 'right_rotation': IDENT, 'translation': [F(0)] * 3, 'scale': [F(0 if scale0 else round(S * k, 4))] * 3}}
    n.update(extra or {})
    return snbt(n)


def place(art, U, sel):
    """(rotated with the host, at it) every display to its rest joint: design +x is his right (^-x), design -z his front (^+z)"""
    return [f'execute positioned ^{-x * U:.4f} ^{y * U:.4f} ^{-z * U:.4f} run tp {sel(p)} ~ ~ ~ ~ 0' for p, (x, y, z) in art.PIVOT.items()]


def pose(art, pz, S, dur, sel, swap=(), hide=True, parts=None, keep=False):
    """one pose's lines: each part's solved turn and shift, its scale (0 if the pose hides it), a swapped model if asked.
    2.78: a part the pose hides only shrinks away, where it is, within 2 ticks - it isn't swung to the new pose on the way
    out (the blunderbuss used to sweep up through his face while his arms rose for the slam)"""
    U = S / 16
    xf = RK.solve(art.PIVOT, art.PARENT, pz)
    out = []
    for p in (parts or art.PARTS):
        if hide and hasattr(art, 'HIDDEN') and art.HIDDEN(p, pz):
            out.append(f'execute as {sel(p)} run data merge entity @s {{start_interpolation:0,interpolation_duration:{min(dur, 2)},transformation:{{scale:[0f,0f,0f]}}}}')
            continue
        q, t = xf[p]
        bits = [f'left_rotation:{snbt(qf(q))}', f'translation:[{t[0] * U:.4f}f,{t[1] * U:.4f}f,{t[2] * U:.4f}f]']
        if hide:
            k = getattr(art, 'PART_K', {}).get(p, 1.0)
            sc = round(S * k, 4)
            bits.append(f'scale:[{sc}f,{sc}f,{sc}f]')
        extra = ''
        if p in swap and not keep:
            extra = f',item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"bm:{art.model_name(p, pz)}"}}}}'
        out.append(f'execute as {sel(p)} run data merge entity @s {{start_interpolation:0,interpolation_duration:{dur},transformation:{{{",".join(bits)}}}{extra}}}')
        if p in swap and keep:                             # (2.94 keep: the model alone - the item's other components, a face's custom_model_data, stay)
            out.append(f'execute as {sel(p)} run data modify entity @s item.components."minecraft:item_model" set value "bm:{art.model_name(p, pz)}"')
    return out


TW, TWG = (1, 2, 3), 3                 # (2.94k: in-between keys - three, 3 ticks apart)
DOWN, UP = (4, 6), (0, 1, 2)           # (sitting, lying down to sleep - and up again into standing, walking, running)


def cycles(fn, pfx, cyc, frame_obj, state_obj, pose_fn, tw=None):
    """the state machine's frames: cyc = {state: (period or None, [(tick, pose)])}; writes <pfx>/anim and one function per state.
    (as the host) frame_obj counts ticks in the state; state_obj is the state; pose_fn(name) -> the pose function's name.
    (2.94k) tw = dict(G, A, S, sel, swap): SITTING DOWN, LYING DOWN, GETTING UP in steps. Every part's display interpolates on
    its own - its offset in a straight line, its turn about itself - so in one long swing from standing to sitting (or back)
    a head cut across the arc and came off the shoulders on the way. Three in-between keys, blended joint by joint, 3 ticks
    apart. Where it came from: the state it was in last tick (bm.rfls), taken as it changes (bm.rfps)."""
    top = []
    PZ = (tw.get('P') or getattr(tw['A'], 'POSES', None) or {}) if tw else {}
    if tw and hasattr(tw['A'], 'PARENT') and 'idle_a' in PZ:
        A, G = tw['A'], tw['G']
        if 'bm.rfls' not in G.OBJECTIVES:
            G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.rfls dummy', 'scoreboard objectives add bm.rfps dummy']
            G.OBJECTIVES += ['bm.rfls', 'bm.rfps']
        first = {st: frames[0][1] for st, (_per, frames) in cyc.items() if frames}

        def tween(name, a, b):
            for i in TW:
                fn(f'{pfx}/pose/tw_{name}_{i}', pose(A, blend_pose(PZ[a], PZ[b], i / (len(TW) + 1)), tw['S'], TWG, tw['sel'], swap=tw.get('swap', ()), keep=True))
            fn(f'{pfx}/tw/{name}', [f'execute if score @s {frame_obj} matches {TWG * (i - 1)} run function bm:{pfx}/pose/tw_{name}_{i}' for i in TW] +
               [f'execute if score @s {frame_obj} matches {TWG * len(TW)} run function bm:{pose_fn(b)}'])
        top += [f'execute if score @s {frame_obj} matches 0 run scoreboard players operation @s bm.rfps = @s bm.rfls',
                f'scoreboard players operation @s bm.rfls = @s {state_obj}']
        end = TWG * len(TW)
        for down in DOWN:
            if down not in first:
                continue
            tween(f'in{down}', 'idle_a', first[down])
            top.append(f'execute if score @s {state_obj} matches {down} if score @s {frame_obj} matches ..{end} run return run function bm:{pfx}/tw/in{down}')
            for up in UP:
                if up in first:
                    tween(f'up{down}_{up}', first[down], first[up])
                    top.append(f'execute if score @s {state_obj} matches {up} if score @s bm.rfps matches {down} if score @s {frame_obj} matches ..{end} '
                               f'run return run function bm:{pfx}/tw/up{down}_{up}')
    for st, (period, frames) in cyc.items():
        lines = [f'scoreboard players operation #f bm.rng = @s {frame_obj}']
        if period:
            lines.append(f'scoreboard players operation #f bm.rng %= #{period} bm.rng')
        lines += [f'execute if score #f bm.rng matches {t} run function bm:{pose_fn(p)}' for t, p in frames]
        fn(f'{pfx}/anim/{st}', lines)
        top.append(f'execute if score @s {state_obj} matches {st} run return run function bm:{pfx}/anim/{st}')
    fn(f'{pfx}/anim', top)


def periods(cyc):
    return sorted({period for period, _f in cyc.values() if period})


def blend_pose(a, b, t):
    """a pose between two (each joint slerped, the offset lerped) - an in-between key for a long swing"""
    out = {}
    for k in set(a) | set(b):
        if k.startswith('_') and k != '_off' and not k.startswith('_o_'):
            out[k] = b.get(k, a.get(k))
            continue
        if k == '_off' or k.startswith('_o_'):
            oa, ob = a.get(k, (0.0, 0.0, 0.0)), b.get(k, (0.0, 0.0, 0.0))
            out[k] = tuple(oa[i] * (1 - t) + ob[i] * t for i in range(3))
            continue
        qa, qb = a.get(k, RK.I), b.get(k, RK.I)
        if sum(u * v for u, v in zip(qa, qb)) < 0:
            qb = tuple(-v for v in qb)
        q = tuple(u * (1 - t) + v * t for u, v in zip(qa, qb))
        n = sum(v * v for v in q) ** 0.5
        out[k] = tuple(v / n for v in q)
    return out

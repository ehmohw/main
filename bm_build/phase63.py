"""Phase 2.51: Donado and the Frog with Mustache get jointed rigs.

Until now each was one model swapped between baked poses every couple of ticks (choppy). Now each limb, the head and the
tail are their own display riding the companion's wolf, turning smoothly about its joint (interpolated), driven by a
small state machine: idle (breathing, looking about, blinking, tail wags), walk / run cycles stepped by speed, jumping,
sitting. Helmets sit on the head part; held weapons follow the arm (Donado) or the body (the Frog).
Old companions are re-rigged in place the next time they're near a player."""
import math
from nbt import snbt, Int, F
from phase57_art import qa, qmul, limb, torso

I = (0.0, 0.0, 0.0, 1.0)


def _rot(q, v):
    x, y, z, w = q; cx = y * v[2] - z * v[1] + w * v[0]; cy = z * v[0] - x * v[2] + w * v[1]; cz = x * v[1] - y * v[0] + w * v[2]
    return (v[0] + 2 * (y * cz - z * cy), v[1] + 2 * (z * cx - x * cz), v[2] + 2 * (x * cy - y * cx))


class Rig:
    """parts: {name: (parent or None, pivot in model units, cubes)}. Displays ride a host; model faces -z (display front +z)."""
    def __init__(self, key, scale, base_y, parts):
        self.key, self.S, self.base, self.parts = key, scale, base_y, parts

    def d(self, v):     # a model-space offset -> display frame
        return (-v[0] / 16 * self.S, v[1] / 16 * self.S, -v[2] / 16 * self.S)

    def solve(self, pose):
        """pose: {part: local quat, '_dy': lift} -> {part: (world quat, joint position)}"""
        out = {}
        def get(n):
            if n in out: return out[n]
            par, q, _c = self.parts[n]
            L = pose.get(n, I)
            if par is None:
                o = self.d((q[0] - 8, q[1] - 8, q[2] - 8)); J = (o[0], o[1] + self.base + pose.get('_dy', 0.0), o[2]); R = L
            else:
                Rp, Jp = get(par); pq = self.parts[par][1]
                o = _rot(Rp, self.d((q[0] - pq[0], q[1] - pq[1], q[2] - pq[2]))); J = tuple(Jp[i] + o[i] for i in range(3)); R = qmul(Rp, L)
            out[n] = (R, J); return out[n]
        for n in self.parts: get(n)
        return out

    def shifted(self, n, cubes=None):
        import copy
        q = self.parts[n][1]; els = copy.deepcopy(cubes if cubes is not None else self.parts[n][2])
        for e in els:
            e['from'] = [e['from'][i] - q[i] + 8 for i in range(3)]; e['to'] = [e['to'][i] - q[i] + 8 for i in range(3)]
            if 'rotation' in e: e['rotation']['origin'] = [e['rotation']['origin'][i] - q[i] + 8 for i in range(3)]
        return els

    def merge(self, part, R, J, dur):
        return (f'execute on passengers if entity @s[tag=bm.{self.key}_{part}] run data merge entity @s[type=minecraft:item_display] '
                f'{{start_interpolation:0,interpolation_duration:{dur},transformation:{{left_rotation:[{R[0]:.4f}f,{R[1]:.4f}f,{R[2]:.4f}f,{R[3]:.4f}f],'
                f'translation:[{J[0]:.4f}f,{J[1]:.4f}f,{J[2]:.4f}f]}}}}')

    def summon(self, model_of):
        out = []
        for n in self.parts:
            out.append('summon minecraft:item_display ~ ~ ~ ' + snbt({
                'Tags': ['bm.fp_disp', f'bm.{self.key}', f'bm.{self.key}_{n}', 'bm.rnew'], 'item_display': 'fixed',
                'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': model_of(n)}},
                'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                   'translation': [F(0), F(0), F(0)], 'scale': [F(self.S)] * 3}}))
        return out


# ===================================================================== DONADO
def don_rig():
    import phase25 as P
    D = P.donado_parts()
    return Rig('dnr', P.DS, P.DS / 2 - P.WOLF_TOP, {
        'legl': (None, (6.1, 5, 8.3), D['legL']), 'legr': (None, (9.9, 5, 8.3), D['legR']),
        'torso': (None, (8, 5, 8.3), D['torso']),
        'arml': ('torso', (3.8, 11.6, 8.4), D['armL']), 'armr': ('torso', (12.2, 11.6, 8.4), D['armR']),
        'head': ('torso', (8, 12, 8.0), D['head']), 'eyes': ('head', (8, 12, 8.0), D['eyes']),
        'tail': ('torso', (8, 7, 10.4), D['tail'])})


def don_poses():
    T = {}
    for i in range(8):                                    # idle: a slow breath, a look about, the tail swinging
        p = 2 * math.pi * i / 8
        T[f'idle{i}'] = {'_dy': 0.012 * math.sin(p), 'torso': torso(lean=1.5 * math.sin(p)), 'head': torso(lean=-3 * math.sin(p + 1), tilt=4 * math.sin(p), turn=12 * math.sin(p + 0.6)),
                         'arml': limb(-1, 4 * math.sin(p + 2), 6), 'armr': limb(1, 4 * math.sin(p + 2), 6), 'tail': qa('y', 22 if i % 2 else -22)}
    for name, leg, arm, lean, bob, tail in (('walk', 26, 22, 3, 0.03, 15), ('run', 46, 42, 12, 0.07, 25)):
        for i in range(4):
            s = (1, 0, -1, 0)[i]
            T[f'{name}{i}'] = {'_dy': bob if i % 2 else 0.0, 'torso': torso(lean=lean, tilt=3 * s), 'head': torso(lean=-lean * 0.6, tilt=-3 * s),
                               'legl': limb(-1, leg * s), 'legr': limb(1, -leg * s), 'arml': limb(-1, -arm * s, 8), 'armr': limb(1, arm * s, 8),
                               'tail': qmul(qa('x', -25 if name == 'run' else -8), qa('y', tail * s))}
    T['jump'] = {'_dy': 0.05, 'legl': limb(-1, -28), 'legr': limb(1, -18), 'arml': limb(-1, 55, 25), 'armr': limb(1, 55, 25),
                 'head': torso(lean=-12), 'tail': qa('x', -35)}
    T['sit'] = {'_dy': -0.09, 'torso': torso(lean=-6), 'legl': limb(-1, 82, 6), 'legr': limb(1, 82, 6), 'arml': limb(-1, 28, 4), 'armr': limb(1, 28, 4),
                'head': torso(lean=4, tilt=8), 'tail': qa('y', 30)}
    return T


# ===================================================================== THE FROG WITH MUSTACHE
def frog_rig():
    import gen_rp as R
    from phase20 import FROG_SCALE, WOLF_TOP
    Fc = R.FROG
    pick = lambda ix: [Fc[i] for i in ix]
    return Rig('frr', FROG_SCALE, FROG_SCALE / 2 - WOLF_TOP, {
        'body': (None, (8, 1, 9), pick([0, 1, 20, 21, 30, 31, 32])),
        'head': ('body', (8, 6, 9), pick(range(2, 20))),
        'fl': (None, (4.75, 3, 4.75), pick([22, 24])), 'fr': (None, (11.25, 3, 4.75), pick([23, 25])),
        'bl': (None, (3.5, 2, 10.5), pick([26, 28])), 'br': (None, (12.5, 2, 10.5), pick([27, 29]))})


def frog_poses():
    T = {}
    for i in range(8):
        p = 2 * math.pi * i / 8
        T[f'idle{i}'] = {'_dy': 0.01 * math.sin(p), 'body': torso(lean=-1.5 * math.sin(p)),
                         'head': torso(lean=-2 * math.sin(p + 1), tilt=5 * math.sin(p), turn=14 * math.sin(p + 0.7))}
    # a hop: crouch, push off, sail, land
    T['hop0'] = {'_dy': -0.03, 'body': torso(lean=5), 'head': torso(lean=-4), 'bl': limb(-1, 10), 'br': limb(1, 10), 'fl': limb(-1, -8), 'fr': limb(1, -8)}
    T['hop1'] = {'_dy': 0.12, 'body': torso(lean=-7), 'head': torso(lean=3), 'bl': limb(-1, -35), 'br': limb(1, -35), 'fl': limb(-1, 22), 'fr': limb(1, 22)}
    T['hop2'] = {'_dy': 0.16, 'body': torso(lean=-2), 'head': torso(lean=-1), 'bl': limb(-1, -22), 'br': limb(1, -22), 'fl': limb(-1, 14), 'fr': limb(1, 14)}
    T['hop3'] = {'_dy': 0.0, 'body': torso(lean=4), 'head': torso(lean=-3), 'bl': limb(-1, 5), 'br': limb(1, 5), 'fl': limb(-1, -5), 'fr': limb(1, -5)}
    T['air'] = T['hop2']
    T['sit'] = {'_dy': -0.04, 'body': torso(lean=6), 'head': torso(lean=-3, tilt=6), 'bl': limb(-1, 15), 'br': limb(1, 15)}
    return T


def generate(G):
    fn = G.fn
    from phase20 import HELMS
    tick, second = [], []
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.rgf dummy', 'scoreboard objectives add bm.rgp dummy', 'scoreboard objectives add bm.rgb dummy']
    G.OBJECTIVES += ['bm.rgf', 'bm.rgp', 'bm.rgb']

    def build(rig, poses, host, ns, extra_for):
        names = list(poses)
        for pid, name in enumerate(names, 1):
            S = rig.solve(poses[name])
            for dur in (3, 10):
                fn(f'{ns}/p/{name}_{dur}', [f'execute if score @s bm.rgp matches {pid} run return 0', f'scoreboard players set @s bm.rgp {pid}'] +
                   [rig.merge(n, R, J, dur) for n, (R, J) in S.items()] + extra_for(S, dur))
        # the driver (as the wolf, every tick near players)
        fn(f'{ns}/anim', ['scoreboard players add @s bm.rgf 1',
                          'execute if predicate bm:p21/airborne run return run function ' + f'bm:{ns}/p/{"jump" if "jump" in poses else "air"}_3',
                          f'execute if data entity @s {{Sitting:1b}} run return run function bm:{ns}/p/sit_10',
                          f'execute if predicate bm:p21/running run return run function bm:{ns}/run',
                          f'execute if predicate bm:p21/walking run return run function bm:{ns}/walk',
                          f'function bm:{ns}/idle'])
        tick.append(f'execute as @e[type=minecraft:wolf,tag={host}] at @s if entity @a[distance=..48] run function bm:{ns}/anim')

    # ---------------------------------------------------------------- Donado
    dr, dp = don_rig(), don_poses()
    import phase25 as P25
    WR = P25.WEAP_ROT
    def don_weap(S, dur):
        R, J = S['armr']
        g = rot_off = _rot(R, dr.d((12.2 - 12.2, 5.8 - 11.6, 8.4 - 8.4)))
        Jg = tuple(J[i] + g[i] for i in range(3)); o = _rot(R, (-0.012, 0.17, 0.17)); Rw = qmul(R, tuple(WR))
        T = tuple(Jg[i] + o[i] for i in range(3))
        return [f'execute on passengers if entity @s[tag=bm.dn_weap] run data merge entity @s[type=minecraft:item_display] {{start_interpolation:0,interpolation_duration:{dur},'
                f'transformation:{{left_rotation:[{Rw[0]:.4f}f,{Rw[1]:.4f}f,{Rw[2]:.4f}f,{Rw[3]:.4f}f],translation:[{T[0]:.4f}f,{T[1]:.4f}f,{T[2]:.4f}f]}}}}']
    build(dr, dp, 'bm.donado', 'p63/don', don_weap)
    fn('p63/don/walk', ['scoreboard players operation #f bm.rng = @s bm.rgf', 'scoreboard players operation #f bm.rng %= #12 bm.rng'] +
       [f'execute if score #f bm.rng matches {3 * i} run function bm:p63/don/p/walk{i}_3' for i in range(4)])
    fn('p63/don/run', ['scoreboard players operation #f bm.rng = @s bm.rgf', 'scoreboard players operation #f bm.rng %= #8 bm.rng'] +
       [f'execute if score #f bm.rng matches {2 * i} run function bm:p63/don/p/run{i}_3' for i in range(4)])
    fn('p63/don/idle', ['scoreboard players operation #f bm.rng = @s bm.rgf', 'scoreboard players operation #f bm.rng %= #80 bm.rng'] +
       [f'execute if score #f bm.rng matches {10 * i} run function bm:p63/don/p/idle{i}_10' for i in range(8)] +
       ['execute if score #f bm.rng matches 35 on passengers if entity @s[tag=bm.dnr_eyes] run data modify entity @s item.components."minecraft:item_model" set value "bm:dnr_eyes_blink"',
        'execute if score #f bm.rng matches 38 on passengers if entity @s[tag=bm.dnr_eyes] run data modify entity @s item.components."minecraft:item_model" set value "bm:dnr_eyes"'])
    # the old single-model body is swapped for the rig (here and for any Donado from before)
    G.FUNCS['p25/don/anim'] = ['return 0']
    second.append('execute as @e[type=minecraft:wolf,tag=bm.donado,tag=!bm.rigged] at @s run function bm:p63/don/rig')
    fn('p63/don/rig', ['tag @s add bm.rigged', 'tag @s add bm.rhost', 'execute on passengers if entity @s[tag=bm.dn_body] run kill @s'] +
       dr.summon(lambda n: f'bm:dnr_{n}' if n != 'head' else 'bm:dnr_head_none') +
       ['execute as @e[type=minecraft:item_display,tag=bm.rnew,distance=..2] run ride @s mount @e[type=minecraft:wolf,tag=bm.rhost,limit=1]',
        'tag @e[tag=bm.rnew] remove bm.rnew', 'scoreboard players set @s bm.rgp 0', 'tag @s add bm.fsel', 'function bm:p25/don/refresh', 'tag @s remove bm.fsel',
        'tag @s remove bm.rhost'])
    G.FUNCS['p25/don/refresh'] = (['execute on passengers if entity @s[tag=bm.dnr_head] run data modify entity @s item.components."minecraft:item_model" set value "bm:dnr_head_none"',
                                   'execute if items entity @s armor.head * on passengers if entity @s[tag=bm.dnr_head] run data modify entity @s item.components."minecraft:item_model" set value "bm:dnr_head_iron"'] +
                                  [f'execute if items entity @s armor.head minecraft:{hid} on passengers if entity @s[tag=bm.dnr_head] run data modify entity @s item.components."minecraft:item_model" set value "bm:dnr_head_{m}"'
                                   for hid, m in HELMS])

    # ---------------------------------------------------------------- the Frog
    fr, fp = frog_rig(), frog_poses()
    from phase21 import WEAP_BASE
    def frog_weap(S, dur):
        R, J = S['body']; J0 = fr.solve({})['body'][1]
        v = tuple(WEAP_BASE[i] - J0[i] for i in range(3)); o = _rot(R, v); T = tuple(J[i] + o[i] for i in range(3))
        Rw = qmul(R, (0.0, 0.7071, 0.0, 0.7071))
        return [f'execute on passengers if entity @s[tag=bm.fp_weap] run data merge entity @s[type=minecraft:item_display] {{start_interpolation:0,interpolation_duration:{dur},'
                f'transformation:{{left_rotation:[{Rw[0]:.4f}f,{Rw[1]:.4f}f,{Rw[2]:.4f}f,{Rw[3]:.4f}f],translation:[{T[0]:.4f}f,{T[1]:.4f}f,{T[2]:.4f}f]}}}}']
    build(fr, fp, 'bm.frogpet', 'p63/frog', frog_weap)
    fn('p63/frog/walk', ['scoreboard players operation #f bm.rng = @s bm.rgf', 'scoreboard players operation #f bm.rng %= #16 bm.rng'] +
       [f'execute if score #f bm.rng matches {4 * i} run function bm:p63/frog/p/hop{i}_3' for i in range(4)])
    fn('p63/frog/run', ['scoreboard players operation #f bm.rng = @s bm.rgf', 'scoreboard players operation #f bm.rng %= #12 bm.rng'] +
       [f'execute if score #f bm.rng matches {3 * i} run function bm:p63/frog/p/hop{i}_3' for i in range(4)])
    fn('p63/frog/idle', ['scoreboard players operation #f bm.rng = @s bm.rgf', 'scoreboard players operation #f bm.rng %= #80 bm.rng'] +
       [f'execute if score #f bm.rng matches {10 * i} run function bm:p63/frog/p/idle{i}_10' for i in range(8)] +
       ['execute if score #f bm.rng matches 45 run function bm:p63/frog/blink', 'execute if score #f bm.rng matches 48 run function bm:p63/frog/unblink'])
    fn('p63/frog/blink', ['execute on passengers if entity @s[tag=bm.frr_head] run tag @s add bm.rgblink', 'function bm:p63/frog/headmodel'])
    fn('p63/frog/unblink', ['execute on passengers if entity @s[tag=bm.frr_head] run tag @s remove bm.rgblink', 'function bm:p63/frog/headmodel'])
    helm_of = lambda m: (f'execute on passengers if entity @s[tag=bm.frr_head,tag=!bm.rgblink] run data modify entity @s item.components."minecraft:item_model" set value "bm:frr_head_{m}"',
                         f'execute on passengers if entity @s[tag=bm.frr_head,tag=bm.rgblink] run data modify entity @s item.components."minecraft:item_model" set value "bm:frr_head_{m}_blink"')
    hm = list(helm_of('none'))
    for hid, m in HELMS:
        a, b = helm_of(m); hm += [f'execute if items entity @s armor.head minecraft:{hid} {a[8:]}', f'execute if items entity @s armor.head minecraft:{hid} {b[8:]}']
    fn('p63/frog/headmodel', hm)
    G.FUNCS['p21/frog/anim'] = ['return 0']
    G.FUNCS['p20/frog/refresh'].append('execute if entity @s[tag=bm.frogpet] run function bm:p63/frog/headmodel')
    second.append('execute as @e[type=minecraft:wolf,tag=bm.frogpet,tag=!bm.rigged] at @s run function bm:p63/frog/rig')
    fn('p63/frog/rig', ['tag @s add bm.rigged', 'tag @s add bm.rhost', 'execute on passengers if entity @s[tag=bm.fp_body] run kill @s'] +
       fr.summon(lambda n: f'bm:frr_{n}' if n != 'head' else 'bm:frr_head_none') +
       ['execute as @e[type=minecraft:item_display,tag=bm.rnew,distance=..2] run ride @s mount @e[type=minecraft:wolf,tag=bm.rhost,limit=1]',
        'tag @e[tag=bm.rnew] remove bm.rnew', 'scoreboard players set @s bm.rgp 0', 'function bm:p63/frog/headmodel', 'tag @s remove bm.rhost'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #12 bm.rng 12', 'scoreboard players set #8 bm.rng 8', 'scoreboard players set #16 bm.rng 16', 'scoreboard players set #80 bm.rng 80']
    G.FUNCS['tick'] += tick
    s = G.FUNCS['loop/second']; s[-1:-1] = second


def rp(R):
    def post(R2):
        from gen_rp import HELM_TEX
        import phase25 as P
        def model(name, tex, els):
            t = dict(tex); t['particle'] = list(t.values())[0]
            R2.wj(f'assets/bm/models/item/{name}.json', {'textures': t, 'elements': els, 'display': {'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]}}})
            R2.wj(f'assets/bm/items/{name}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/{name}'}})
        helms = ['none'] + list(HELM_TEX)
        dr = don_rig()
        DT = dict(P.DON_TEX, r='minecraft:block/iron_block', w='minecraft:block/white_wool')
        for n in dr.parts:
            if n != 'head': model(f'dnr_{n}', DT, dr.shifted(n))
        model('dnr_eyes_blink', DT, dr.shifted('eyes', [P._c((5, 16.1, 4.88), (6.6, 16.6, 5.0), 'k'), P._c((9.4, 16.1, 4.88), (11, 16.6, 5.0), 'k')]))
        for m in helms:
            model(f'dnr_head_{m}', dict(DT, h=HELM_TEX.get(m, 'minecraft:block/iron_block')), dr.shifted('head', dr.parts['head'][2] + P.donado_helm(m, 0, 0)))
        fr = frog_rig()
        import gen_rp as G2
        FT = G2.FROG_TEX
        for n in fr.parts:
            if n != 'head': model(f'frr_{n}', FT, fr.shifted(n))
        head = fr.parts['head'][2]
        blink = [c for i, c in enumerate(head) if i not in (5, 6)] + [G2.cube((3.45, 9.05, 4.85), (6.55, 11.45, 4.95), 'e'), G2.cube((9.45, 9.05, 4.85), (12.55, 11.45, 4.95), 'e')]
        for m in helms:
            t = dict(FT, h=HELM_TEX.get(m, 'minecraft:block/iron_block'))
            model(f'frr_head_{m}', t, fr.shifted('head', head + G2.frog_helm(m, 0, 0)))
            model(f'frr_head_{m}_blink', t, fr.shifted('head', blink + G2.frog_helm(m, 0, 0)))
    R.POST.append(post)

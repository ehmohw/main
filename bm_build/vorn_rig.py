"""3.0k: THE VORN WALK - the owner: "please improve the Vorn walking animations. They still look rigid."

What they were: one baked model riding the husk, flipped between two poses (legs +-22.5 degrees, arms the other way) every 4
ticks whatever the husk was doing - no bend, no bob, no ease, no notion of how fast it went: a stiff toy scissoring its legs,
gliding over the ground, turning in snaps. The Armada's crew (phase241's dressed husks) didn't even turn: only Vorn Troopers'
bodies were rotated with their hosts.

What they are now: the same Vorn (phase32/phase45's model - Donado's build in the Vorn's colours, the plasma rifle or the
Warlord's hammer) cut into a rig of eight parts - torso, head, two antennae, two arms, two legs - every part an item display
riding the husk (as the old body did), posed by rigkit and moved by gaitdrive:

  THE GROUND    the cycle advances by the ground the husk really covers (gaitdrive): each stance foot is planted - it slides
                back under the body exactly as fast as the body goes over it - and the frames' interpolations are as long as
                the next frame is away, so the displays glide.
  THE STRIDE    two gaits: a WALK (duty 0.6, both feet down at the change, the hips vaulting over each planted leg) and a RUN
                (duty 0.4, a hop between strides, a deeper lean), picked by real speed with hysteresis. Opposite arm and leg
                swing together, eased (the rifle arm, or the hammer arm, swings less - it's carrying something).
  THE BODY      bobbing with the stride (the hip's true height over the planted leg, and a little hop in the run), leaning
                into the motion (5 / 13 degrees), swaying over the planted foot, the shoulders twisting against the hips.
  THE HEAD      turned back against the shoulders' twist and the lean (it keeps looking where it goes), nodding a beat behind
                the bob.
  THE ANTENNAE  swept back by the speed, springing a beat behind the bob and the sway (their own parts, on the head).
  STILL         it eases into its stance (8 ticks), then breathes; setting off, its first steps take longer (out of the idle,
                not snapped into a stride). Its facing eases a third of the way to the husk's each tick.
  THE WARLORD   the same rig, 2.2 times the size, in red armour with its hammer: its cycles are 2.2 times as long (gaitdrive's
                L), so its feet plant too.

Every Vorn husk gets it: the Troopers (phase32 spawn/trooper - invasions, the Dreadnought's guards, phase70's heist guards,
phase52's waves, the Armada's reinforcements), the Warlord, the Armada's crew (phase241 dress/trooper); one already out in an
older world (wearing the old body) is re-rigged the tick it's seen. A Vorn more than 64 blocks from every player isn't animated.
Parts are bm.vdisp (phase41's orphan sweep kills any left without a host), bm.vrp, bm.vrp_<part>; the host bm.vrg (bm.vrgw: the
Warlord's)."""
import math
from nbt import snbt, F, Int
import rigkit as RK
from rigkit import qs, qa

PARTS = ('torso', 'legl', 'legr', 'head', 'arml', 'armr', 'antl', 'antr')
# design units: feet at y=0, facing -z, his right +x (Donado's model: design = model - (8, 0, 8))
PIVOT = {'torso': (0.0, 5.0, 0.3), 'legl': (-1.9, 5.0, 0.3), 'legr': (1.9, 5.0, 0.3), 'head': (0.0, 12.0, 0.3),
         'arml': (-4.2, 11.6, 0.4), 'armr': (4.2, 11.6, 0.4), 'antl': (-1.6, 19.0, -0.1), 'antr': (1.6, 19.0, -0.1)}
PARENT = {'torso': None, 'legl': None, 'legr': None, 'head': 'torso', 'arml': 'torso', 'armr': 'torso', 'antl': 'head', 'antr': 'head'}
PREFIX = 'vrg_'                           # (the Warlord's parts: vrgw_)
TS, WS = 1.15, 2.2                        # (phase32: the trooper's body scale; the Warlord's size)
LEG = 5.0                                 # (hip to sole)
NF = 8                                    # (frames a cycle)
# the gaits: duty (the share of the cycle a foot is down), stride (how far a foot sweeps under the body, design units), the
# swing's lift, the lean, the sway, the shoulders' twist, the arms' swing (free arm, weapon arm), the antennae's sweep back
WALK = dict(duty=0.6, stride=4.6, lift=1.1, lean=5.0, roll=3.0, twist=6.0, arm=26.0, warm=8.0, sweep=6.0, hop=0.0, nod=3.0)
RUN = dict(duty=0.4, stride=6.0, lift=1.7, lean=13.0, roll=4.0, twist=10.0, arm=44.0, warm=14.0, sweep=16.0, hop=0.55, nod=5.0)
GAITS = {1: ('walk', WALK), 2: ('run', RUN)}


def cycle_len(g):
    """design units of ground a cycle of this gait covers (a foot sweeps its stride while it's down)"""
    p = GAITS[g][1]
    return p['stride'] / p['duty']


def _track(u, duty, stride, lift):
    """a foot's (forward, height) at cycle point u: down and sliding back through the stance, then lifted forward, eased"""
    u %= 1.0
    if u < duty:
        return stride / 2 - stride * u / duty, 0.0
    v = (u - duty) / (1 - duty)
    return -stride / 2 + stride * (0.5 - 0.5 * math.cos(math.pi * v)), lift * math.sin(math.pi * v)


def gait_pose(g, k, n=NF):
    """frame k of gait g"""
    p = GAITS[g][1]
    ph = k / n
    feet = {'legr': _track(ph, p['duty'], p['stride'], p['lift']), 'legl': _track(ph + 0.5, p['duty'], p['stride'], p['lift'])}
    ang = {s: math.degrees(math.asin(max(-0.95, min(0.95, f / LEG)))) for s, (f, _y) in feet.items()}
    down = [s for s in feet if (ph + (0.5 if s == 'legl' else 0.0)) % 1.0 < p['duty']]
    if down:
        h = min(LEG * math.cos(math.radians(ang[s])) for s in down)              # (the hip's true height over the planted leg)
    else:                                                                       # (the run's hop: between two strides, both up)
        w = max(0.0, min(1.0, ((ph % 0.5) - p['duty']) / (0.5 - p['duty'])))
        edge = LEG * math.cos(math.asin(min(0.95, p['stride'] / 2 / LEG)))
        h = edge + p['hop'] * math.sin(math.pi * w)
    off_y = h - LEG
    pose = {'_off': (0.0, off_y, 0.0)}
    for s, (f, y) in feet.items():
        a = ang[s]
        pose[s] = qa('x', -a)
        o = y - h + LEG * math.cos(math.radians(a))                             # (that leg's own shift: its sole on the track)
        pose['_o_' + s] = (0.0, max(-0.6, min(1.8, o)), 0.0)
    _sole(pose, feet)
    if down:                                                                    # (and the hips back over the planted leg, as it stands)
        m = min(pose['_o_' + s][1] for s in down)
        pose['_off'] = (0.0, off_y + m, 0.0)
        for s in feet:
            pose['_o_' + s] = (0.0, pose['_o_' + s][1] - m, 0.0)
        off_y += m
    fr, fl = feet['legr'][0], feet['legl'][0]
    sw = (fr - fl) / p['stride']                                                # (+1: the right leg forward)
    lr, ll = feet['legr'][1], feet['legl'][1]
    roll = p['roll'] * ((ll - lr) / max(0.01, p['lift']))                         # (over the planted foot)
    twist = -p['twist'] * sw                                                    # (the left shoulder forward with the right leg)
    bob = 0.5 * math.cos(4 * math.pi * (ph - 0.08))                              # (a beat behind the hips' rise, for the head and antennae)
    pose['torso'] = qs(('y', twist), ('x', p['lean'] + 1.5 * off_y), ('z', roll))
    pose['head'] = qs(('y', -0.75 * twist), ('x', -0.6 * p['lean'] + p['nod'] * bob), ('z', -0.5 * roll))
    pose['arml'] = qs(('x', -p['arm'] * sw), ('z', 4.0 + 2.0 * abs(sw)))
    pose['armr'] = qs(('x', p['warm'] * sw - 4.0), ('z', -3.0))
    lag = math.sin(4 * math.pi * (ph - 0.16))
    for s, sx in (('antl', 1), ('antr', -1)):
        pose[s] = qs(('x', -(p['sweep'] + 7.0 * lag)), ('z', sx * (5.0 + 2.0 * lag) - 1.5 * roll))
    return pose


def _sole(pose, feet):
    """a leg has no ankle: tipped, it stands on its pad's toe or heel - so each leg's lowest corner (not the middle of its sole)
    is put on its track's height"""
    import gaitkit as GK
    import sys
    me = sys.modules[__name__]
    for s, (_f, y) in feet.items():
        lo = GK.lowest(me, pose, s)
        ox, oy, oz = pose['_o_' + s]
        pose['_o_' + s] = (ox, oy + (y - lo), oz)


IDLE_A = {'antl': qs(('z', 5.0)), 'antr': qs(('z', -5.0)), 'arml': qs(('z', 3.0)), 'armr': qs(('x', -4.0), ('z', -3.0))}
IDLE_B = {'_off': (0.0, 0.14, 0.0), '_o_legl': (0.0, -0.14, 0.0), '_o_legr': (0.0, -0.14, 0.0),
          'torso': qs(('x', -1.5)), 'head': qs(('x', -3.0), ('z', 4.0)), 'antl': qs(('x', -4.0), ('z', 8.0)), 'antr': qs(('x', -2.0), ('z', -3.0)),
          'arml': qs(('z', 5.0)), 'armr': qs(('x', -6.0), ('z', -4.0))}


def poses():
    P = {'idle_a': IDLE_A, 'idle_b': IDLE_B}
    for g, (nm, _p) in GAITS.items():
        for k in range(NF):
            P[f'{nm}_{k}'] = gait_pose(g, k)
    return P



# ---------------------------------------------------------------------------------------------------- the models
def models(warlord=False):
    """{name: (textures, elements)} - each part's cubes from Donado's build, its joint moved to model (8, 8, 8)"""
    import phase25 as R25
    from gen_rp import cube
    c = cube
    P = R25.donado_parts()
    ant_l = [c((6.1, 19, 7.6), (6.7, 23, 8.2), 'm'), c((5.8, 23, 7.3), (7.0, 24.2, 8.5), 'g')]
    ant_r = [c((9.3, 19, 7.6), (9.9, 23, 8.2), 'm'), c((9.0, 23, 7.3), (10.2, 24.2, 8.5), 'g')]
    rifle = [c((11.6, 6.2, 1.5), (12.8, 7.4, 9.0), 'r'), c((11.5, 6.0, 0.4), (12.9, 7.6, 1.6), 'g'), c((11.7, 4.4, 6.5), (12.7, 6.2, 7.5), 'm')]
    hammer = [c((11.8, 2.0, 7.9), (12.6, 12.0, 8.7), 'm'), c((10.2, 11.5, 6.3), (14.2, 14.5, 10.3), 'r'), c((10.0, 12.3, 6.1), (14.4, 13.7, 10.5), 'g')]
    els = {'torso': P['torso'] + P['tail'], 'head': P['head'] + P['eyes'], 'antl': ant_l, 'antr': ant_r,
           'arml': P['armL'], 'armr': P['armR'] + (hammer if warlord else rifle), 'legl': P['legL'], 'legr': P['legR']}
    vt = {'f': 'bm:block/vorn_skin', 'm': 'bm:block/vorn_dark', 'e': 'bm:block/vorn_dark', 'k': 'bm:block/vorn_eye', 't': 'bm:block/vorn_dark',
          's': 'bm:block/vorn_armor', 'p': 'bm:block/vorn_armor', 'g': 'minecraft:block/verdant_froglight_side', 'r': 'minecraft:block/iron_block'}
    if warlord:
        vt = dict(vt, s='bm:block/vorn_armor_red', p='bm:block/vorn_armor_red')
    out = {}
    for p, es in els.items():
        px, py, pz = PIVOT[p]
        moved = RK.transform(es, lambda v, px=px, py=py, pz=pz: [v[0] - px, v[1] - py + 8, v[2] - pz])
        used = {f['texture'][1:] for e in moved for f in e['faces'].values()}
        out[('vrgw_' if warlord else PREFIX) + p] = ({t: vt[t] for t in sorted(used)}, moved)
    return out


def rp(R):
    for wl in (False, True):
        for name, (tex, els) in models(wl).items():
            R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + ('vrg_', 'vrgw_')


# ---------------------------------------------------------------------------------------------------- in the game
def _xf(pose, S, seat):
    """each part's (left_rotation, translation) riding the husk: its joint's place in the posed rig, under the seat"""
    U = S / 16
    out = {}
    for p, (q, t) in RK.solve(PIVOT, PARENT, pose).items():
        d = RK.D(PIVOT[p])
        out[p] = (q, ((d[0] + t[0]) * U, (d[1] + t[1]) * U - seat, (d[2] + t[2]) * U))
    return out


def _merge(q, t, dur):
    rot = '[' + ','.join(f'{v:.5f}f' for v in q) + ']'
    return (f'data merge entity @s {{start_interpolation:0,interpolation_duration:{dur},transformation:{{left_rotation:{rot},'
            f'translation:[{t[0]:.4f}f,{t[1]:.4f}f,{t[2]:.4f}f]}}}}')


def generate(G):
    """(from phase45, where the old flip-book walk was) the rigs, their drive, and the re-rigging of every Vorn husk"""
    import gaitdrive as GD
    from phase32 import HUSK_SEAT
    fn = G.fn
    variants = {'t': (TS, HUSK_SEAT, PREFIX), 'w': (TS * WS, HUSK_SEAT * WS, 'vrgw_')}
    for v, (S, seat, pre) in variants.items():
        pfx = f'vrg/{v}'
        k = S / TS
        # the cycles' ground (milliblocks) and the speeds (smoothed milliblocks a tick) that pick the gaits
        L = {g: int(round(cycle_len(g) * S / 16 * 1000)) for g in GAITS}
        GD.build(G, pfx, [(L[1], int(14 * k), int(6 * k)), (L[2], int(75 * k), int(55 * k))], nf=NF,
                 call=lambda name: f'execute on passengers run function bm:{name}')
        fn(f'{pfx}/turn', ['$execute on passengers run rotate @s $(y) 0'])
        frames = {('0', 'a', 8): POSES['idle_a'], ('0', 'a', 30): POSES['idle_a'], ('0', 'b', 30): POSES['idle_b']}
        for g, (nm, _p) in GAITS.items():
            for kk in range(NF):
                for d in GD.DURS:
                    frames[(str(g), str(kk), d)] = POSES[f'{nm}_{kk}']
        for (g, kk, d), pz in frames.items():
            xf = _xf(pz, S, seat)
            fn(f'{pfx}/f/{g}_{kk}_{d}', [f'execute if entity @s[tag=bm.vrp_{p}] run return run ' + _merge(*xf[p], d) for p in PARTS])
        # the rig: eight displays at the idle, mounted on the husk (tagged bm.vrme while it's made)
        xf0 = _xf(POSES['idle_a'], S, seat)
        parts = []
        for p in PARTS:
            q, t = xf0[p]
            parts.append('summon minecraft:item_display ~ ~ ~ ' + snbt({
                'Tags': ['bm.vdisp', 'bm.vrp', f'bm.vrp_{p}', 'bm.vrnew'],
                'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:{pre}{p}'}},
                'item_display': 'fixed', 'brightness': {'block': Int(13), 'sky': Int(13)}, 'teleport_duration': Int(2),
                'interpolation_duration': Int(0), 'view_range': F(1.5),
                'transformation': {'left_rotation': [F(round(x, 5)) for x in q], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                   'translation': [F(round(x, 4)) for x in t], 'scale': [F(round(S, 4))] * 3}}))
        fn(f'{pfx}/rig', parts + ['execute rotated as @s run rotate @e[type=minecraft:item_display,tag=bm.vrnew,distance=..1] ~ 0',
                                  'execute as @e[type=minecraft:item_display,tag=bm.vrnew,distance=..1] run ride @s mount @e[type=minecraft:husk,tag=bm.vrme,limit=1,sort=nearest]',
                                  'tag @e[type=minecraft:item_display,tag=bm.vrnew,distance=..3] remove bm.vrnew'])
    # making one (as a Vorn husk): its old one-piece body (or 2.24's hoverboard) off, the rig on, its gait from where it stands
    fn('vrg/make', ['execute unless entity @s[tag=bm.vtroop] unless entity @s[tag=bm.vb_warlord] unless entity @s[tag=bm.avorn] run return run tag @s add bm.vrgx',
                    'tag @s add bm.vrg', 'tag @s add bm.v224', 'execute if entity @s[tag=bm.vb_warlord] run tag @s add bm.vrgw',
                    'execute on passengers if entity @s[tag=bm.vbody] run kill @s', 'execute on passengers if entity @s[tag=bm.vboard] run kill @s',
                    'execute on passengers if items entity @s contents *[minecraft:item_model="bm:vorn3d_warlord"] run kill @s',
                    'execute on passengers if items entity @s contents *[minecraft:item_model="bm:hoverboard_red"] run kill @s',
                    'execute on passengers if entity @s[tag=bm.vrp] run kill @s',
                    'tag @s add bm.vrme', 'execute if entity @s[tag=bm.vrgw] run function bm:vrg/w/rig', 'execute unless entity @s[tag=bm.vrgw] run function bm:vrg/t/rig',
                    'tag @s remove bm.vrme'] + GD.init_lines())
    # every tick: any Vorn husk not yet rigged is; each within 64 blocks of a player walks
    fn('vrg/tick', ['execute if entity @s[tag=bm.vrgw] run return run function bm:vrg/w/run', 'function bm:vrg/t/run'])
    for v in variants:
        fn(f'vrg/{v}/run', [f'function bm:vrg/{v}/motion', f'function bm:vrg/{v}/gait'])
    G.FUNCS['tick'] += ['execute as @e[type=minecraft:husk,tag=bm.vorn,tag=!bm.vrg,tag=!bm.vrgx] at @s run function bm:vrg/make',
                        'execute as @e[type=minecraft:husk,tag=bm.vrg] at @s if entity @a[distance=..64] run function bm:vrg/tick']
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.vrp]']


POSES = poses()

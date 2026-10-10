"""2.55: the rats come alive - a real walk cycle, more idle fidgets, and a playful routine for every job.

Every rat is still ONE display entity (the market holds dozens of them: a jointed rig each would cost real lag), but each
variant now has a whole library of baked poses, picked through the item's custom_model_data string and strung together
into sequences by the data pack:
- WALK: a four-frame cycle (paws stepping, arms swinging, the body bobbing, the tail swaying) - the market walkers.
- IDLE (every rat): looks left and right, blinks, grooms its face with both paws, scratches behind an ear, swishes
  its tail, sniffs; the slow breathing (an interpolated scale) carries on underneath.
- JOBS - one playful routine each (with a little sound):
    chef: flips a pancake in his pan        professor: reads, turns a page, pushes up his glasses
    lucky: flips a coin and catches it      pirate: a swig from his bottle, then a hiccup
    soldier: salutes, stamps to attention    ember rat: juggles embers         void rat: motes orbit his head
    auctioneer: bangs the gavel twice       concierge: a deep bow              teller: counts a stack of coins
    the lord: a regal wave                  madame: gazes into her crystal ball
    the gentleman in grey: checks his pocket watch    the mercenary: sharpens his knife
    the familiar (on your shoulder): chases its own tail
Geometry: the poses are built from the base rat by moving whole groups (head, each arm, the feet, the tail, the upper
body); a group may turn about its joint (one axis per element - the block-model limit). Props (pans, coins, bottles...)
ride the group that holds them."""
import copy
import math

# ---------------------------------------------------------------- groups of the base rat (gen_rp.RAT_BASE indices)
FEET_A, FEET_B = {0}, {1}
ARM_A, ARM_B = {6, 8}, {7, 9}                       # A: x 3.5-5 (his left), B: x 11-12.5 (his right - the weapon hand)
HEAD = set(range(10, 21))
EYES = {13, 14}
TAIL = {21, 22}
UPPER_BASE = {4, 5} | ARM_A | ARM_B | HEAD          # (the haunches and feet stay put when the upper body moves)
PIVOT = {'head': (8, 11, 8.25), 'armA': (4.25, 10, 8.25), 'armB': (11.75, 10, 8.25), 'tail': (8, 1.5, 11),
         'upper': (8, 6, 8.75), 'torso': (8, 6, 8.75), 'feetA': (6, 0.5, 7.5), 'feetB': (10, 0.5, 7.5), 'free': (8, 8, 8)}
EXTRA_TEX = {'c': 'minecraft:block/light_blue_stained_glass', 'v': 'minecraft:block/amethyst_block', 'o': 'minecraft:block/stripped_oak_log',
             'f': 'minecraft:block/shroomlight', 'n': 'minecraft:block/green_stained_glass', 't': 'minecraft:block/stone'}


def kit_group(e):
    """which group a kit element rides: hats and glasses with the head, things held at the side with an arm"""
    (x1, y1, z1), (x2, y2, z2) = e['from'], e['to']
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    if cx >= 12.2 and (x2 - x1) <= 1.2: return 'armB'            # a spear, its tip, a cutlass
    if cy < 13.3 and cx >= 11.9: return 'armB'
    if cy < 13.3 and cx <= 4.1: return 'armA'
    if cy >= 13.3: return 'head'
    return 'torso'


def _rotp(p, axis, ang, o):
    a = math.radians(ang); c, s = math.cos(a), math.sin(a)
    x, y, z = p[0] - o[0], p[1] - o[1], p[2] - o[2]
    if axis == 'x': y, z = y * c - z * s, y * s + z * c
    elif axis == 'y': x, z = x * c + z * s, -x * s + z * c
    else: x, y = x * c - y * s, x * s + y * c
    return (x + o[0], y + o[1], z + o[2])


def xf_point(p, T, group):
    """where point p of `group` ends up under transform T (dx, dy, dz[, axis, angle])"""
    if not T: return p
    dx, dy, dz = T[:3]; q = (p[0] + dx, p[1] + dy, p[2] + dz)
    if len(T) > 3:
        o = PIVOT[group]; q = _rotp(q, T[3], T[4], (o[0] + dx, o[1] + dy, o[2] + dz))
    return q


def apply(e, T, group):
    e = copy.deepcopy(e)
    if not T: return e
    dx, dy, dz = T[:3]
    e['from'] = [round(e['from'][0] + dx, 4), round(e['from'][1] + dy, 4), round(e['from'][2] + dz, 4)]
    e['to'] = [round(e['to'][0] + dx, 4), round(e['to'][1] + dy, 4), round(e['to'][2] + dz, 4)]
    if 'rotation' in e:
        o = e['rotation']['origin']; e['rotation']['origin'] = [o[0] + dx, o[1] + dy, o[2] + dz]
    elif len(T) > 3 and T[4]:
        o = PIVOT[group]
        e['rotation'] = {'origin': [round(o[0] + dx, 4), round(o[1] + dy, 4), round(o[2] + dz, 4)], 'axis': T[3], 'angle': round(max(-45, min(45, T[4])), 3)}
    return e


def build(R, v, pose):
    """pose: {group: T, 'upper': T (moves all of the upper body - no other rotation then), 'props': [(group, cube)], 'hide': {...}, 'hide_kit': {...}}"""
    base, kit = R.RAT_BASE, R.RAT_KIT[v]
    out = []
    up = pose.get('upper')
    def T_for(g):
        """-> (transform, the group whose joint it turns about)"""
        t = pose.get(g)
        if up and g in ('head', 'armA', 'armB', 'torso'):
            if t is None: return up, 'upper'
            return (t[0] + up[0], t[1] + up[1], t[2] + up[2]) + tuple(t[3:]), g      # (its own turn wins; the lean becomes a shift)
        return t, g
    def g_of_base(i):
        if i in FEET_A: return 'feetA'
        if i in FEET_B: return 'feetB'
        if i in ARM_A: return 'armA'
        if i in ARM_B: return 'armB'
        if i in HEAD: return 'head'
        if i in TAIL: return 'tail'
        if i in (4, 5): return 'torso'
        return None
    for i, e in enumerate(base):
        if i in pose.get('hide', ()): continue
        g = g_of_base(i)
        out.append(apply(e, *T_for(g)) if g else copy.deepcopy(e))
    for j, e in enumerate(kit):
        if j in pose.get('hide_kit', ()): continue
        g = kit_group(e)
        if v == 'void' and j >= 2: g = 'free'                     # (his floating motes stay where they float)
        out.append(apply(e, *T_for(g)) if g != 'free' else copy.deepcopy(e))
    for g, cube in pose.get('props', ()):
        out.append(apply(cube, *T_for(g)) if g != 'free' else cube)
    return out


# ---------------------------------------------------------------- the pose library
def generic(holds=False):
    """holds: something in his right paw (a spear, a cutlass...) - he grooms with the other"""
    P = {}
    P['look_l'] = {'head': (0, 0, 0, 'y', 35)}
    P['look_r'] = {'head': (0, 0, 0, 'y', -35)}
    P['blink'] = {'hide': EYES, 'props': [('head', ('k', (5.8, 14.3, 5.85), (7, 14.6, 6))), ('head', ('k', (9, 14.3, 5.85), (10.2, 14.6, 6)))]}
    P['groom1'] = {'head': (0, 0, 0, 'x', -12), 'armA': (0, 2.6, -1.4, 'x', 45), 'armB': (0, 2.0, -1.2, 'x', 45)}
    P['groom2'] = {'head': (0, 0, 0, 'x', -8), 'armA': (0, 2.0, -1.2, 'x', 45), 'armB': (0, 2.8, -1.4, 'x', 45)}
    if holds:
        P['groom1'] = {'head': (0, 0, 0, 'x', -12), 'armA': (0.6, 2.6, -1.4, 'x', 45)}
        P['groom2'] = {'head': (0, 0, 0, 'x', -8), 'armA': (0.6, 3.2, -1.6, 'x', 45)}
    P['scratch1'] = {'head': (0, 0, 0, 'z', 12), 'armA': (0.2, 7.0, 0.4)}                     # (his free paw)
    P['scratch2'] = {'head': (0, 0, 0, 'z', 16), 'armA': (0.2, 7.8, 0.2), 'tail': (0, 0, 0, 'y', -20)}
    P['tail_l'] = {'tail': (0, 0, 0, 'y', 40)}
    P['tail_r'] = {'tail': (0, 0, 0, 'y', -40)}
    # the walk: a stride, a passing step (body up), the other stride, a passing step
    P['walk1'] = {'feetA': (0, 0.5, -1.3), 'feetB': (0, 0, 1.1), 'armA': (0, 0, 0, 'x', -22), 'armB': (0, 0, 0, 'x', 22), 'tail': (0, 0, 0, 'y', 16)}
    P['walk2'] = {'upper': (0, 0.45, 0), 'feetA': (0, 0.2, -0.2), 'feetB': (0, 0.7, 0.2), 'tail': (0, 0.2, 0)}
    P['walk3'] = {'feetB': (0, 0.5, -1.3), 'feetA': (0, 0, 1.1), 'armB': (0, 0, 0, 'x', -22), 'armA': (0, 0, 0, 'x', 22), 'tail': (0, 0, 0, 'y', -16)}
    P['walk4'] = {'upper': (0, 0.45, 0), 'feetB': (0, 0.2, -0.2), 'feetA': (0, 0.7, 0.2), 'tail': (0, 0.2, 0)}
    return P


def C(t, fr, to): return (t, fr, to)


PAW_B = (11.75, 6.0, 8.25)           # the right paw's centre (before the arm moves)
PAW_A = (4.25, 6.0, 8.25)


def at(p, d, t='y'):
    """a little cube of half-size d=(hx,hy,hz) centred on p"""
    return C(t, (p[0] - d[0], p[1] - d[1], p[2] - d[2]), (p[0] + d[0], p[1] + d[1], p[2] + d[2]))


def jobs():
    """variant: (sequence of (pose name, quarter-seconds), {pose name: pose}, {frame index: sound})"""
    J = {}
    # CHEF: the pan comes out, the pancake goes up, turns over, comes down, sizzles
    armB = (0, 1.4, -1.0, 'x', 38)
    pan = [('armB', C('k', (11.35, 5.4, 4.0), (12.15, 6.0, 7.6))), ('armB', C('s', (9.3, 5.2, 0.2), (14.2, 5.8, 4.4))),
           ('armB', C('k', (9.6, 5.8, 0.5), (13.9, 6.1, 4.1)))]
    cake0 = xf_point((11.75, 6.4, 2.3), armB, 'armB')
    def cake(dy, flat=True):
        c = (cake0[0], cake0[1] + dy, cake0[2])
        return ('free', at(c, (1.5, 0.25, 1.3) if flat else (1.5, 1.2, 0.3), 'o'))
    P = {'chef_1': {'armB': armB, 'props': pan + [cake(0)]}, 'chef_2': {'armB': armB, 'props': pan + [cake(3)], 'head': (0, 0, 0, 'x', 10)},
         'chef_3': {'armB': armB, 'props': pan + [cake(5.5, False)], 'head': (0, 0, 0, 'x', 18)},
         'chef_4': {'armB': armB, 'props': pan + [cake(2.5)], 'head': (0, 0, 0, 'x', 8)}}
    J['chef'] = ([('chef_1', 3), ('chef_2', 1), ('chef_3', 1), ('chef_4', 1), ('chef_1', 3), ('chef_2', 1), ('chef_3', 1), ('chef_4', 1), ('chef_1', 2)], P,
                 {1: 'minecraft:entity.player.attack.sweep', 3: 'minecraft:block.lava.extinguish', 5: 'minecraft:entity.player.attack.sweep', 7: 'minecraft:block.lava.extinguish'})
    # PROFESSOR: the book comes up and opens, a page turns, then a paw pushes his glasses up
    arms = {'armA': (0.6, 1.6, -1.6, 'x', 38), 'armB': (-0.6, 1.6, -1.6, 'x', 38), 'head': (0, 0, 0, 'x', -14)}
    book = [('free', C('b', (5.4, 9.2, 2.6), (8.0, 9.7, 5.4))), ('free', C('b', (8.0, 9.2, 2.6), (10.6, 9.7, 5.4))),
            ('free', C('w', (5.7, 9.7, 2.8), (10.3, 10.0, 5.2)))]
    page = ('free', {'from': [8.0, 9.9, 2.9], 'to': [10.1, 10.0, 5.1], 'rotation': {'origin': [8.0, 10.0, 4.0], 'axis': 'z', 'angle': 45}, 'tex': 'w'})
    page2 = ('free', {'from': [5.9, 9.9, 2.9], 'to': [8.0, 10.0, 5.1], 'rotation': {'origin': [8.0, 10.0, 4.0], 'axis': 'z', 'angle': -45}, 'tex': 'w'})
    P = {'prof_1': dict(arms, props=book, hide_kit={4}), 'prof_2': dict(arms, props=book + [page], hide_kit={4}),
         'prof_3': dict(arms, props=book + [page2], hide_kit={4}),
         'prof_4': {'armA': (1.4, 6.6, -1.8, 'x', 28), 'head': (0, 0, 0, 'x', 6)}}
    J['prof'] = ([('prof_1', 6), ('prof_2', 1), ('prof_3', 1), ('prof_1', 5), ('prof_4', 3)], P,
                 {1: 'minecraft:item.book.page_turn', 4: 'minecraft:block.wool.hit'})
    # LUCKY: a coin flicked up - spinning (flat, edge-on, flat...) - and caught
    armB = (0, 0.8, -0.8, 'x', 34)
    paw = xf_point((11.75, 6.4, 8.25), armB, 'armB')
    def coin(dy, edge):
        c = (paw[0], paw[1] + dy, paw[2])
        return ('free', at(c, (0.7, 0.15, 0.7) if not edge else (0.7, 0.7, 0.15), 'y'))
    P = {f'lucky_{i}': {'armB': armB, 'props': [coin(dy, e)], 'head': (0, 0, 0, 'x', hx)}
         for i, (dy, e, hx) in enumerate(((0.3, False, 0), (3.0, True, 10), (5.5, False, 18), (6.6, True, 22), (5.0, False, 16), (2.4, True, 8)), 1)}
    J['lucky'] = ([('lucky_1', 2), ('lucky_2', 1), ('lucky_3', 1), ('lucky_4', 1), ('lucky_5', 1), ('lucky_6', 1), ('lucky_1', 3)], P,
                  {1: 'minecraft:block.chain.hit', 6: 'minecraft:block.note_block.bell'})
    # PIRATE: the bottle to his snout, head back - a swig - then a hiccup
    armA = (0.8, 4.4, -2.6, 'x', 45)
    bottle = [('armA', C('n', (3.6, 3.4, 7.4), (4.9, 6.2, 9.1))), ('armA', C('b', (3.9, 2.6, 7.8), (4.6, 3.4, 8.7)))]
    P = {'pirate_1': {'armA': (0.4, 2.2, -1.4, 'x', 30), 'props': bottle}, 'pirate_2': {'armA': armA, 'props': bottle, 'head': (0, 0, 0, 'x', 20)},
         'pirate_3': {'head': (0, 0.4, 0, 'z', 10)}, 'pirate_4': {'head': (0, 0, 0, 'z', -6)}}
    J['pirate'] = ([('pirate_1', 1), ('pirate_2', 5), ('pirate_1', 1), ('pirate_3', 1), ('pirate_4', 2), ('pirate_3', 1)], P,
                   {1: 'minecraft:entity.generic.drink', 3: 'minecraft:entity.villager.ambient'})
    # SOLDIER: a crisp salute, then he stamps to attention
    P = {'soldier_1': {'armA': (1.6, 6.4, -2.4, 'x', 20), 'head': (0, 0, 0, 'x', 6)},
         'soldier_2': {'feetA': (0, 1.6, -0.4), 'armB': (0, 0.6, 0)}, 'soldier_3': {'armB': (0, -0.3, 0)}}
    J['soldier'] = ([('soldier_1', 6), ('soldier_2', 1), ('soldier_3', 1), ('soldier_2', 1), ('soldier_3', 2)], P,
                    {0: 'minecraft:item.armor.equip_iron', 4: 'minecraft:entity.iron_golem.step'})
    # EMBER: three embers juggled in an arc over his paws
    def emb(i, k):
        a = (k + i * 4 / 3) * math.pi / 2
        return ('free', at((8 + 4.0 * math.cos(a), 12.5 + 3.0 * abs(math.sin(a)), 4.4), (0.5, 0.5, 0.5), 'f'))
    P = {f'ember_{k}': {'armA': (0.6, 1.4 + (0.8 if k % 2 else 0), -1.2, 'x', 36), 'armB': (-0.6, 1.4 + (0 if k % 2 else 0.8), -1.2, 'x', 36),
                        'head': (0, 0, 0, 'x', 12), 'props': [emb(i, k) for i in range(3)]} for k in range(4)}
    J['ember'] = ([(f'ember_{k % 4}', 1) for k in range(12)], P, {0: 'minecraft:block.fire.ambient', 6: 'minecraft:block.fire.ambient'})
    # VOID: motes orbit his head, his ears blink away
    def mote(i, k):
        a = (k * 30 + i * 120) * math.pi / 180
        return ('free', at((8 + 5.2 * math.cos(a), 16.5 + 0.8 * math.sin(2 * a), 8.2 + 5.2 * math.sin(a)), (0.45, 0.45, 0.45), 'v'))
    P = {f'void_{k}': {'props': [mote(i, k) for i in range(3)], 'head': (0, 0, 0, 'y', 12 * math.sin(k * math.pi / 3))} for k in range(12)}
    J['void'] = ([(f'void_{k}', 1) for k in range(12)], P, {0: 'minecraft:block.amethyst_block.chime', 6: 'minecraft:block.amethyst_block.chime'})
    # AUCTIONEER: the gavel comes down - twice - SOLD!
    gavel = [('armB', C('b', (11.45, 4.0, 7.95), (12.05, 6.4, 8.55))), ('armB', C('k', (10.6, 3.0, 7.4), (12.9, 4.1, 9.1)))]
    up_, dn = {'armB': (0, 4.0, -1.6, 'x', 45), 'props': gavel, 'head': (0, 0, 0, 'x', 6)}, {'armB': (0, 0.8, -1.2, 'x', 20), 'props': gavel}
    J['auction'] = ([('auction_1', 2), ('auction_2', 1), ('auction_1', 1), ('auction_2', 3)], {'auction_1': up_, 'auction_2': dn},
                    {1: 'minecraft:block.wood.hit', 3: 'minecraft:block.anvil.land'})
    # CONCIERGE: a deep, practised bow, one paw across his chest
    P = {'concierge_1': {'upper': (0, -0.1, -0.4, 'x', -12), 'armB': (-2.4, 3.0, -1.4, 'x', 30)},
         'concierge_2': {'upper': (0, -0.3, -0.8, 'x', -24), 'armB': (-2.4, 2.6, -2.0, 'x', 30)}}
    J['concierge'] = ([('concierge_1', 1), ('concierge_2', 5), ('concierge_1', 1)], P, {1: 'minecraft:entity.villager.yes'})
    # TELLER: counting coins from one paw onto the stack in the other
    armA, armB = (0.8, 1.2, -1.2, 'x', 40), (-0.8, 1.6, -1.2, 'x', 40)
    base_ = xf_point((4.25, 6.4, 8.25), armA, 'armA')
    def stack(n): return [('free', at((base_[0] + 0.4, base_[1] + 0.3 + 0.32 * i, base_[2]), (0.7, 0.15, 0.7), 'y')) for i in range(n)]
    P = {f'teller_{n}': {'armA': armA, 'armB': (armB[0], armB[1] + (0.7 if n % 2 else 0), armB[2], 'x', 40), 'head': (0, 0, 0, 'x', -12), 'props': stack(n)} for n in range(1, 7)}
    J['teller'] = ([(f'teller_{n}', 1) for n in range(1, 7)] + [('teller_6', 3)], P, {i: 'minecraft:block.chain.step' for i in range(0, 6, 2)})
    # LORD: a slow, regal wave, chin up
    P = {'lord_1': {'armB': (0.6, 5.0, 0, 'z', 30), 'head': (0, 0, 0, 'x', 8)}, 'lord_2': {'armB': (0.6, 5.4, 0, 'z', 8), 'head': (0, 0, 0, 'x', 8)}}
    J['lord'] = ([('lord_1', 2), ('lord_2', 2), ('lord_1', 2), ('lord_2', 2), ('lord_1', 2)], P, {0: 'minecraft:entity.villager.celebrate'})
    # MADAME: paws hover over her crystal ball - it glimmers
    ball = [('free', C('c', (6.0, 7.4, 2.4), (10.0, 11.4, 6.4))), ('free', C('k', (6.6, 6.6, 3.0), (9.4, 7.4, 5.8)))]
    P = {f'madame_{k}': {'armA': (0.6 + 0.5 * math.cos(k * math.pi / 2), 3.4 + 0.6 * math.sin(k * math.pi / 2), -1.6, 'x', 40),
                         'armB': (-0.6 - 0.5 * math.cos(k * math.pi / 2), 3.4 - 0.6 * math.sin(k * math.pi / 2), -1.6, 'x', 40),
                         'head': (0, 0, 0, 'x', -10), 'props': ball} for k in range(4)}
    J['madame'] = ([(f'madame_{k % 4}', 1) for k in range(10)], P, {0: 'minecraft:block.amethyst_block.resonate', 5: 'minecraft:block.amethyst_block.chime'})
    # GREY: the pocket watch out of his waistcoat - a glance - snap
    armB = (-1.8, 3.0, -2.0, 'x', 30)
    w = xf_point((11.75, 6.2, 8.25), armB, 'armB')
    watch = [('free', at((w[0] - 0.4, w[1] + 0.6, w[2] - 0.3), (0.9, 0.9, 0.2), 'y')), ('free', at((w[0] - 0.4, w[1] + 0.6, w[2] - 0.55), (0.6, 0.6, 0.05), 'w'))]
    P = {'grey_1': {'armB': armB, 'head': (0, 0, 0, 'x', -16), 'props': watch}, 'grey_2': {'armB': armB, 'head': (0, 0, 0, 'x', -16), 'props': watch[:1]}}
    J['grey'] = ([('grey_1', 5), ('grey_2', 2)], P, {0: 'minecraft:block.note_block.hat', 1: 'minecraft:block.note_block.hat'})
    # MERCENARY: the knife drawn along a whetstone, back and forth
    stone = ('free', C('t', (4.8, 7.6, 3.0), (7.6, 8.4, 5.2)))
    def knife(dz): return [('armB', C('s', (11.5, 4.8, 3.2 + dz), (12.0, 5.4, 7.4 + dz))), ('armB', C('k', (11.4, 5.0, 7.4 + dz), (12.1, 6.2, 8.8 + dz)))]
    P = {'merc_1': {'armA': (1.4, 2.0, -1.4, 'x', 40), 'armB': (-1.4, 2.0, -1.0, 'x', 40), 'head': (0, 0, 0, 'x', -12), 'props': [stone] + knife(0)},
         'merc_2': {'armA': (1.4, 2.0, -1.4, 'x', 40), 'armB': (-1.4, 2.0, -2.2, 'x', 40), 'head': (0, 0, 0, 'x', -12), 'props': [stone] + knife(-1.2)}}
    J['merc'] = ([('merc_1', 1), ('merc_2', 1)] * 4, P, {i: 'minecraft:item.axe.scrape' for i in (0, 4)})
    # FAMILIAR: chases its own tail
    P = {'familiar_1': {'head': (0, 0, 0, 'y', 45), 'tail': (0, 0, 0, 'y', -40)}, 'familiar_2': {'head': (0, 0, 0, 'y', 40), 'tail': (0, 0, 0, 'y', -30), 'feetA': (0, 0.6, 0)},
         'familiar_3': {'head': (0, 0, 0, 'y', 45), 'tail': (0, 0, 0, 'y', -45), 'feetB': (0, 0.6, 0)}}
    J['familiar'] = ([('familiar_1', 1), ('familiar_2', 1), ('familiar_3', 1)] * 3, P, {0: 'minecraft:entity.rabbit.jump'})
    return J


GENERIC_SEQ = {   # name: frames (pose, quarter-seconds)
    'look': [('look_l', 4), (None, 1), ('look_r', 4)], 'blink': [('blink', 1)], 'groom': [('groom1', 1), ('groom2', 1)] * 4,
    'scratch': [('scratch1', 1), ('scratch2', 1)] * 3, 'swish': [('tail_l', 1), ('tail_r', 1)] * 3, 'sniff': [('sniff', 3), (None, 1), ('sniff', 2)],
    'ears': [('ears', 2)]}


def _cube(R, spec):
    """('t', from, to) or a dict with 'tex' -> a model element"""
    if isinstance(spec, dict):
        e = R.cube(tuple(spec['from']), tuple(spec['to']), spec['tex']); e['rotation'] = dict(spec['rotation']); return e
    t, fr, to = spec
    return R.cube(fr, to, t)


def all_poses(R, v):
    """{pose name: elements} for variant v"""
    J = jobs()
    lib = dict(generic(any(kit_group(e) == 'armB' for e in R.RAT_KIT[v])))
    if v in J: lib.update(J[v][1])
    out = {}
    for name, pose in lib.items():
        pose = dict(pose)
        pose['props'] = [(g, _cube(R, s)) for g, s in pose.get('props', ())]
        if 'blink' == name and 'props' in pose: pass
        out[name] = build(R, v, pose)
    return out


def rp(R):
    def post(R2):
        tex_of = lambda v: dict(R2.RAT_TEXV.get(v, R2.RAT_TEX), **EXTRA_TEX)
        for v in R2.RAT_KIT:
            poses = all_poses(R2, v)
            t = tex_of(v); t['particle'] = list(t.values())[0]
            for name, els in poses.items():
                R2.wj(f'assets/bm/models/item/rat3dq_{v}_{name}.json', {'textures': t, 'elements': els, 'display': R2.RAT_DISPLAY})
            mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
            cases = [{'when': pz, 'model': mdl(f'rat3dp_{v}_{pz}')} for pz in R2.RAT_POSES] + \
                    [{'when': name, 'model': mdl(f'rat3dq_{v}_{name}')} for name in poses]
            R2.wj(f'assets/bm/items/rat3d_{v}.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                                 'cases': cases, 'fallback': mdl(f'rat3d_{v}')}})
    R.POST.append(post)


# ================================================================ data pack: the sequences
def generate(G):
    import gen_rp as R
    fn = G.fn
    J = jobs()
    VARS = list(R.RAT_KIT) + [v for v in ('auction', 'concierge', 'teller', 'lord', 'madame', 'grey', 'merc', 'familiar') if v not in R.RAT_KIT]
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.rv dummy', 'scoreboard objectives add bm.rq dummy', 'scoreboard objectives add bm.rf dummy',
                              'scoreboard objectives add bm.wf dummy']
    G.OBJECTIVES += ['bm.rv', 'bm.rq', 'bm.rf', 'bm.wf']
    cmd = 'data modify entity @s item.components."minecraft:custom_model_data" set value {strings:["%s"]}'
    rest = 'data remove entity @s item.components."minecraft:custom_model_data"'
    # which variant each rat display is (once): its model says
    second = [f'execute as @e[type=minecraft:item_display,tag=bm.rat_sprite,tag=!bm.rv] if items entity @s contents *[minecraft:item_model="bm:rat3d_{v}"] run scoreboard players set @s bm.rv {i + 1}'
              for i, v in enumerate(VARS)] + ['tag @e[type=minecraft:item_display,tag=bm.rat_sprite,tag=!bm.rv] add bm.rv']
    second += [f'execute as @e[type=minecraft:item_display,tag=bm.walker,tag=!bm.rv] if items entity @s contents *[minecraft:item_model="bm:rat3d_{v}"] run scoreboard players set @s bm.rv {i + 1}'
               for i, v in enumerate(VARS)] + ['tag @e[type=minecraft:item_display,tag=bm.walker,tag=!bm.rv] add bm.rv']
    second += [f'execute as @e[type=minecraft:item_display,tag=bm.familiar] unless score @s bm.rv matches 1.. run scoreboard players set @s bm.rv {VARS.index("familiar") + 1}']
    G.FUNCS['loop/second'][-1:-1] = second
    # the old three-pose fidget hands over to the new idle for every rat that has a variant
    a = G.FUNCS['p21/rat/anim']
    k = next(i for i, l in enumerate(a) if 'bm.ra matches 1..' in l)
    a.insert(k, 'execute if score @s bm.rv matches 1.. run return run function bm:p64/idle')
    G.FUNCS['loop/fast'].insert(0, 'execute as @e[type=minecraft:item_display,tag=bm.familiar] if score @s bm.rv matches 1.. at @s run function bm:p64/idle')
    fn('p64/idle', ['execute if score @s bm.rq matches 1.. run return run function bm:p64/step',
                    'execute store result score #h bm.rng run random value 1..48'] +
       [f'execute if score @s bm.rv matches {i + 1} run return run function bm:p64/pick/{v}' for i, v in enumerate(VARS)])
    fn('p64/step', [f'execute if score @s bm.rv matches {i + 1} run return run function bm:p64/step/{v}' for i, v in enumerate(VARS)] + ['function bm:p64/end'])
    fn('p64/end', [rest, 'scoreboard players reset @s bm.rq', 'scoreboard players reset @s bm.rf'])
    for i, v in enumerate(VARS):
        seqs = dict(GENERIC_SEQ)
        if v in J: seqs['job'] = J[v][0]
        names = list(seqs)
        # pick: the job routine is the favourite (1-3 of 36), the fidgets share the rest; most ticks nothing starts
        pick = []
        weights = {'job': 3, 'look': 2, 'blink': 2, 'groom': 1, 'scratch': 1, 'swish': 1, 'sniff': 1, 'ears': 1}
        lo = 1
        for q, nm in enumerate(names, 1):
            w = weights.get(nm, 1)
            pick.append(f'execute if score #h bm.rng matches {lo}..{lo + w - 1} run return run function bm:p64/go {{q:{q}}}')
            lo += w
        fn(f'p64/pick/{v}', pick)
        fn(f'p64/step/{v}', [f'execute if score @s bm.rq matches {q} run return run function bm:p64/s/{v}/{nm}' for q, nm in enumerate(names, 1)] + ['function bm:p64/end'])
        for q, nm in enumerate(names, 1):
            frames = []
            for pose, n in seqs[nm]: frames += [pose] * n
            sounds = J[v][2] if (nm == 'job' and v in J) else {}
            lines = ['scoreboard players add @s bm.rf 1']
            # (the sound on a frame index counts sequence entries, not quarter-seconds: map entry -> first quarter)
            starts, t = {}, 0
            for e_i, (pose, n) in enumerate(seqs[nm]): starts[e_i] = t; t += n
            snd = {starts[e_i] + 1: s for e_i, s in sounds.items() if e_i in starts}
            prev = object()
            for f_i, pose in enumerate(frames, 1):
                if f_i in snd: lines.append(f'execute if score @s bm.rf matches {f_i} run playsound {snd[f_i]} neutral @a[distance=..12] ~ ~ ~ 0.35 1.3')
                if pose == prev: continue
                lines.append(f'execute if score @s bm.rf matches {f_i} run return run ' + (cmd % pose if pose else rest))
                prev = pose
            lines.append(f'execute if score @s bm.rf matches {len(frames) + 1}.. run function bm:p64/end')
            fn(f'p64/s/{v}/{nm}', lines)
    fn('p64/go', ['$scoreboard players set @s bm.rq $(q)', 'scoreboard players set @s bm.rf 0', 'function bm:p64/step'])
    # WALKERS: a four-frame walk every two ticks while they're on the move; standing (talking to you) they idle
    G.FUNCS['tick'].append('execute if score #gt2 bm.rng matches 0 as @e[type=minecraft:item_display,tag=bm.walker,tag=bm.wmov] run function bm:p64/walkf')
    G.FUNCS['tick'].insert(0, 'execute store result score #gt2 bm.rng run time query gametime')
    G.FUNCS['tick'].insert(1, 'scoreboard players operation #gt2 bm.rng %= #2 bm.rng')
    fn('p64/walkf', ['scoreboard players add @s bm.wf 1', 'execute if score @s bm.wf matches 4.. run scoreboard players set @s bm.wf 0'] +
       [f'execute if score @s bm.wf matches {k} run return run ' + cmd % f'walk{k + 1}' for k in range(4)])
    w = G.FUNCS['p23/walk']
    w[:] = [l for l in w if 'custom_model_data' not in l and 'bm.wst' not in l and '#w bm.rng' not in l]
    k = next(i for i, l in enumerate(w) if l.startswith('execute if entity @a[distance=..2.5'))
    w.insert(k, 'execute if entity @a[distance=..2.5,gamemode=!spectator] run function bm:p64/stop')
    w.insert(k, 'execute unless entity @a[distance=..2.5,gamemode=!spectator] unless entity @s[tag=bm.wmov] run function bm:p64/move')
    fn('p64/move', ['tag @s add bm.wmov', 'scoreboard players reset @s bm.rq', 'scoreboard players reset @s bm.rf'])
    # (stopped to look at you: he fidgets like the others)
    fn('p64/stop', ['execute if entity @s[tag=bm.wmov] run ' + rest, 'tag @s remove bm.wmov', 'execute if score @s bm.rv matches 1.. run function bm:p64/idle'])

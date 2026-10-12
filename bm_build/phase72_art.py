"""2.61: art for phase72 - glass display cases (floor and wall, four woods/metals), Zib the Donadian trooper's jointed rig
and his ray gun, the Skiff Escort beacons and the case icons.

Cases are plain item models (0..16, drawn at display scale). Zib is phase63's Rig built from Donado's parts in Donadian
colours (teal fur, red eyes, white antennae) in a navy trooper's tunic, with a ray gun on his right paw (its own part, so
it can stay level while the arm swings)."""
import math
import random
from PIL import Image

CASES = {   # variant: (name, colour, plinth, trim, cushion)
    'oak': ('Oak', '#c8a060', 'minecraft:block/oak_planks', 'minecraft:block/stripped_oak_log', 'minecraft:block/red_wool'),
    'dark_oak': ('Dark Oak', '#6a4a2a', 'minecraft:block/dark_oak_planks', 'minecraft:block/stripped_dark_oak_log', 'minecraft:block/green_wool'),
    'gilded': ('Gilded', '#ffcf40', 'minecraft:block/polished_blackstone', 'minecraft:block/gold_block', 'minecraft:block/purple_wool'),
    'quartz': ('Quartz', '#ece6dc', 'minecraft:block/quartz_block_side', 'minecraft:block/quartz_block_top', 'minecraft:block/blue_wool'),
}
ESCORT_COLS = ['crimson', 'gold', 'midnight', 'ocean', 'rose', 'verdant', 'pearl', 'ember']


def hexc(h, a=255):
    h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def _noise(base, seed, var=0.06, size=16):
    rnd = random.Random(seed); b = hexc(base)[:3]; im = Image.new('RGBA', (size, size))
    for y in range(size):
        for x in range(size):
            k = 1 + rnd.uniform(-var, var); im.putpixel((x, y), tuple(int(max(0, min(255, v * k))) for v in b) + (255,))
    return im


def textures():
    T = {}
    # case glass: clear in the middle (so nothing behind it is hidden), a pale rim and two light streaks
    g = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for i in range(16):
        for (x, y) in ((i, 0), (i, 15), (0, i), (15, i)): g.putpixel((x, y), (220, 238, 248, 150))
    for i in range(5): g.putpixel((3 + i, 9 - i), (255, 255, 255, 110)); g.putpixel((4 + i, 9 - i), (255, 255, 255, 60))
    for i in range(3): g.putpixel((9 + i, 13 - i), (255, 255, 255, 90))
    T['case_glass'] = g
    # Zib's tunic: Donadian navy, a teal seam down the front, gold buttons, a dark belt line
    tu = _noise('#26345e', 72)
    for y in range(16):
        tu.putpixel((7, y), hexc('#3ad8c8')); tu.putpixel((8, y), hexc('#2aa898'))
    for y in (3, 7, 11): tu.putpixel((6, y), hexc('#ffd23f')); tu.putpixel((9, y), hexc('#ffd23f'))
    for x in range(16): tu.putpixel((x, 13), hexc('#141a30')); tu.putpixel((x, 14), hexc('#141a30'))
    T['adon_trooper'] = tu
    gm = _noise('#5a6272', 73, 0.05)
    for x in range(16): gm.putpixel((x, 4), hexc('#3a404c')); gm.putpixel((x, 11), hexc('#3a404c'))
    for y in range(16): gm.putpixel((12, y), hexc('#7a8496'))
    T['zb_gun'] = gm
    return T


# ---------------------------------------------------------------------------------------------------- display cases
def case_models(cube):
    M = {}
    for v, (_n, _c, base, trim, cush) in CASES.items():
        tex = {'b': base, 't': trim, 'g': 'bm:block/case_glass', 'c': cush}
        # the floor case: a plinth, a trim band, a little cushion, four glass panes and a lid, posts at the corners
        fl = [cube((1, 0, 1), (15, 2.5, 15), 'b'), cube((0.5, 2.5, 0.5), (15.5, 3.2, 15.5), 't'), cube((5, 3.2, 5), (11, 3.9, 11), 'c'),
              cube((1.5, 3.2, 1.5), (14.5, 14.5, 1.7), 'g'), cube((1.5, 3.2, 14.3), (14.5, 14.5, 14.5), 'g'),
              cube((1.5, 3.2, 1.7), (1.7, 14.5, 14.3), 'g'), cube((14.3, 3.2, 1.7), (14.5, 14.5, 14.3), 'g'),
              cube((1.7, 14.3, 1.7), (14.3, 14.5, 14.3), 'g')]
        for (x, z) in ((1.1, 1.1), (14.1, 1.1), (1.1, 14.1), (14.1, 14.1)):
            fl.append(cube((x, 3.2, z), (x + 0.8, 14.9, z + 0.8), 't'))
        fl += [cube((1.1, 14.5, 1.1), (14.9, 15.2, 1.9), 't'), cube((1.1, 14.5, 14.1), (14.9, 15.2, 14.9), 't'),
               cube((1.1, 14.5, 1.9), (1.9, 15.2, 14.1), 't'), cube((14.1, 14.5, 1.9), (14.9, 15.2, 14.1), 't')]
        M[f'dcase_{v}_floor'] = (tex, fl)
        # the wall case: a back board on the wall (model z 16 = the wall), a ledge, side and top frames, a glass front
        wl = [cube((1, 1, 15), (15, 15, 16), 'b'), cube((0.5, 0.5, 9.4), (15.5, 2.2, 16), 'b'),
              cube((1, 13.8, 9.6), (15, 15, 15), 't'), cube((1, 2.2, 9.6), (2.2, 13.8, 15), 't'), cube((13.8, 2.2, 9.6), (15, 13.8, 15), 't'),
              cube((2.2, 2.2, 9.8), (13.8, 13.8, 10.0), 'g'), cube((4, 2.2, 12.6), (12, 2.9, 15), 'c')]
        M[f'dcase_{v}_wall'] = (tex, wl)
    return M


def case_icon(R, v):
    _n, col, *_r = CASES[v]
    rim = {'oak': '#9a7440', 'dark_oak': '#4a321c', 'gilded': '#ffcf40', 'quartz': '#d8d0c4'}[v]
    base = {'oak': '#b08850', 'dark_oak': '#5a3e22', 'gilded': '#2a2630', 'quartz': '#ece6dc'}[v]
    return R.grid(['................', '..TTTTTTTTTTTT..', '..T..........T..', '..T.w........T..', '..T..w.......T..', '..T....EE....T..',
                   '..T...EeeE...T..', '..T...EeeE...T..', '..T....EE....T..', '..T....cc....T..', '..T..cccccc..T..', '.TTTTTTTTTTTTTT.',
                   '.BBBBBBBBBBBBBB.', '.BBBBBBBBBBBBBB.', '..BBBBBBBBBBBB..', '................'],
                  dict(T=rim, B=base, w='#ffffff', E='#2a9a6a', e='#7affc0', c='#c03040'))


def escort_icon(R, col):
    return R.grid(['................', '.......YY.......', '......YWWY......', '.......YY.......', '.......LL.......', '.....GGGGGG.....',
                   '....GGWGGGGG....', '..HHHHHHHHHHHH..', '.HHhHHhHHhHHhHH.', '..HHHHHHHHHHHH..', '....DDDDDDDD....', '......LLLL......',
                   '.......LL.......', '......L..L......', '.....L....L.....', '................'],
                  dict(Y='#ffe85a', W='#ffffff', L='#7dff6a', G='#bfeaff', H=col, h='#ffffff', D='#3a3a48'))


# ---------------------------------------------------------------------------------------------------- Zib the trooper
ZB_TEX = {'f': 'bm:block/adon_skin', 'm': 'bm:block/adon_muzzle', 'e': 'bm:block/adon_dark', 'k': 'bm:block/adon_mouth',
          't': 'bm:block/adon_tongue', 's': 'bm:block/adon_trooper', 'p': 'bm:block/adon_dark', 'r': 'bm:block/adon_eye',
          'w': 'bm:block/adon_antenna', 'x': 'bm:block/zb_gun', 'n': 'bm:block/adon_disc', 'g': 'minecraft:block/gold_block'}
GRIP = (12.2, 5.8, 8.4)


def zib_parts():
    import phase25 as P
    c = P._c
    D = P.donado_parts()
    torso = [e for e in D['torso'][:4]] + [c((6.9, 9.4, 6.3), (9.1, 10.6, 6.5), 'g'),                     # a gold badge
                                          c((4.5, 6.6, 6.4), (11.5, 7.3, 10.5), 'k')]                    # the belt
    arml = D['armL'] + [c((2.7, 10.4, 7.1), (4.8, 12.2, 9.7), 'g')]                                      # shoulder pads
    armr = D['armR'] + [c((11.2, 10.4, 7.1), (13.3, 12.2, 9.7), 'g')]
    head = D['head'] + [c((6.1, 19, 7.6), (6.7, 23, 8.2), 'w'), c((5.8, 23, 7.3), (7.0, 24.2, 8.5), 'n'),  # antennae, green-tipped
                        c((9.3, 19, 7.6), (9.9, 23, 8.2), 'w'), c((9.0, 23, 7.3), (10.2, 24.2, 8.5), 'n'),
                        c((12.4, 14.0, 7.0), (13.2, 16.2, 9.0), 'x'), c((12.6, 15.8, 6.2), (12.9, 16.1, 7.2), 'x')]   # a headset and mic
    eyes = [c((5, 15.6, 4.88), (6.6, 17.3, 5.0), 'r'), c((9.4, 15.6, 4.88), (11, 17.3, 5.0), 'r'),
            c((5.2, 16.6, 4.86), (5.7, 17.1, 4.9), 'w'), c((9.6, 16.6, 4.86), (10.1, 17.1, 4.9), 'w')]
    blink = [c((5, 16.1, 4.88), (6.6, 16.6, 5.0), 'e'), c((9.4, 16.1, 4.88), (11, 16.6, 5.0), 'e')]
    gun = [c((11.8, 4.4, 8.3), (12.6, 6.0, 9.0), 'x'), c((11.5, 5.8, 6.2), (12.9, 7.0, 9.4), 'x'),
           c((11.35, 5.7, 5.2), (13.05, 7.1, 5.8), 'n'), c((11.35, 5.7, 4.0), (13.05, 7.1, 4.6), 'n'),
           c((11.8, 6.0, 2.6), (12.6, 6.8, 6.2), 'x'), c((11.6, 5.85, 2.0), (12.8, 6.95, 2.6), 'n'),
           c((12.0, 7.0, 7.4), (12.4, 7.5, 8.2), 'x')]
    return {'legl': D['legL'], 'legr': D['legR'], 'torso': torso, 'arml': arml, 'armr': armr, 'head': head, 'eyes': eyes,
            'tail': D['tail'], 'gun': gun}, blink


def zib_rig():
    import phase25 as P
    from phase63 import Rig
    p, _b = zib_parts()
    return Rig('zbr', P.DS, P.DS / 2 - P.WOLF_TOP, {
        'legl': (None, (6.1, 5, 8.3), p['legl']), 'legr': (None, (9.9, 5, 8.3), p['legr']),
        'torso': (None, (8, 5, 8.3), p['torso']),
        'arml': ('torso', (3.8, 11.6, 8.4), p['arml']), 'armr': ('torso', (12.2, 11.6, 8.4), p['armr']),
        'head': ('torso', (8, 12, 8.0), p['head']), 'eyes': ('head', (8, 12, 8.0), p['eyes']),
        'tail': ('torso', (8, 7, 10.4), p['tail']), 'gun': ('armr', GRIP, p['gun'])})


def zib_poses():
    from phase57_art import qa, qmul, limb, torso
    T = {}
    AIM, HELD = 78, 34
    aim = lambda f=AIM, recoil=0: dict(armr=limb(1, f - recoil, 2), gun=qa('x', f - recoil * 0.4), arml=limb(-1, f - 12 - recoil, -26))
    for i in range(8):                                     # idle: breathing, a look round, antennae... the gun held low
        p = 2 * math.pi * i / 8
        T[f'idle{i}'] = {'_dy': 0.012 * math.sin(p), 'torso': torso(lean=1.5 * math.sin(p)),
                         'head': torso(lean=-3 * math.sin(p + 1), tilt=5 * math.sin(p), turn=16 * math.sin(p + 0.6)),
                         'arml': limb(-1, 4 * math.sin(p + 2), 6), 'armr': limb(1, 10 + 3 * math.sin(p + 2), 4), 'gun': qa('x', HELD),
                         'tail': qa('y', 20 * math.sin(p * 2))}
    for name, n, leg, arm, lean, bob in (('walk', 8, 26, 18, 3, 0.03), ('run', 6, 44, 34, 12, 0.07)):
        for i in range(n):
            p = 2 * math.pi * i / n; s = math.sin(p)
            T[f'{name}{i}'] = {'_dy': bob * abs(math.cos(p)), 'torso': torso(lean=lean, tilt=3 * s), 'head': torso(lean=-lean * 0.6, tilt=-3 * s),
                               'legl': limb(-1, leg * s), 'legr': limb(1, -leg * s), 'arml': limb(-1, -arm * s, 8),
                               'armr': limb(1, 12 + arm * 0.4 * s, 4), 'gun': qa('x', HELD + (10 if name == 'run' else 0)),
                               'tail': qmul(qa('x', -25 if name == 'run' else -8), qa('y', 18 * s))}
            # walking with a foe in sight: the legs keep going, the gun stays up
            T[f'{name}aim{i}'] = dict(T[f'{name}{i}'], torso=torso(lean=lean * 0.5, tilt=2 * s), head=torso(lean=-6), **aim())
    for i in range(8):                                     # (2.67) swimming: a brisk paddle, the gun kept in hand, the tail sweeping
        p = 2 * math.pi * i / 8; s = math.sin(p)
        T[f'swim{i}'] = {'_dy': -0.32 + 0.02 * math.sin(2 * p), 'torso': torso(lean=14, tilt=3 * s), 'head': torso(lean=-16, tilt=-3 * s),
                         'legl': limb(-1, -20 + 20 * math.sin(2 * p)), 'legr': limb(1, -20 - 20 * math.sin(2 * p)),
                         'arml': limb(-1, 56 + 30 * s, 14), 'armr': limb(1, 56 - 30 * s, 6), 'gun': qa('x', 16),
                         'tail': qmul(qa('x', -20), qa('y', 26 * s))}
    T['aim'] = {'_dy': 0.0, 'torso': torso(lean=2, turn=-8), 'head': torso(lean=-6, turn=8), 'legl': limb(-1, -8), 'legr': limb(1, 10), 'tail': qa('x', -15), **aim()}
    T['fire'] = dict(T['aim'], torso=torso(lean=-4, turn=-8), head=torso(lean=-10, turn=8), **aim(recoil=16))
    T['charge'] = dict(T['aim'], torso=torso(lean=6, turn=-12), head=torso(lean=-4, turn=12), **aim(f=AIM - 6))
    T['jump'] = {'_dy': 0.05, 'legl': limb(-1, -28), 'legr': limb(1, -18), 'arml': limb(-1, 55, 25), 'armr': limb(1, 40, 18), 'gun': qa('x', 40),
                 'head': torso(lean=-12), 'tail': qa('x', -35)}
    T['sit'] = {'_dy': -0.09, 'torso': torso(lean=-6), 'legl': limb(-1, 82, 6), 'legr': limb(1, 82, 6), 'arml': limb(-1, 28, 4), 'armr': limb(1, 30, 4),
                'gun': qa('x', 60), 'head': torso(lean=4, tilt=8), 'tail': qa('y', 30)}
    return T

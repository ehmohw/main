"""3.0d: the three dramatic deaths, key frames (the built pack's own models and the death sprites, phase257).
    python3 tools/preview/deaths.py [sov,vexis,mire]       (after gen_rp --phase2; PNGs to $DEATHS_OUT)
Each frame poses the rig as the game holds it at that tick (the death's merges: a part charred / white-hot / squashed / sunk /
gone) and stands the sprites where they'd be (seeded scatter round each part). tools/render has no lighting: a white-hot part
is drawn brightened, a charred one darkened (as the brightness override shows them in game)."""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM); sys.path.insert(0, os.path.join(BM, 'tools'))
import numpy as np
from PIL import Image
import draftkit as K
import rigkit as RK
from render import Scene

RP = os.path.join(BM, 'out_p2', 'BlackMarket_RP')
OUT = os.environ.get('DEATHS_OUT', '/tmp/bm_previews/deaths'); os.makedirs(OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['sov', 'vexis', 'mire']
VIEW = (-28, 12)


def rig(s, art, pose, scale, look=None, at=(0, 0, 0)):
    """draw a posed rig; look: {part: dict(hide, dy, k=(sx, sy, sz), tint)}; -> {part: its drawn middle}"""
    look = look or {}
    U = scale / 16
    xf = RK.solve(art.PIVOT, art.PARENT, pose)
    cen = {}
    for p in art.PARTS:
        if hasattr(art, 'HIDDEN') and art.HIDDEN(p, pose): continue
        L = look.get(p, {})
        if L.get('hide'): continue
        q, t = xf[p]
        dp = art.PIVOT[p]
        kk = getattr(art, 'PART_K', {}).get(p, 1.0) * scale
        k3 = L.get('k', (1, 1, 1))
        name = art.model_name(p, pose) if hasattr(art, 'model_name') else art.model_id(p)
        n0 = len(s.faces)
        s.display(f'bm:item/{name}', pos=(at[0] + dp[0] * U, at[1] + dp[1] * U, at[2] + dp[2] * U), translation=(t[0] * U, t[1] * U + L.get('dy', 0), t[2] * U),
                  scale=[kk * k3[0], kk * k3[1], kk * k3[2]], left=tuple(q))
        new = s.faces[n0:]
        pts = [pt for f in new if f[0] != 'box' for pt in f[0]]
        if pts: cen[p] = tuple(np.mean(pts, axis=0))
        if 'tint' in L:
            tm = np.array(L['tint'])
            s.faces[n0:] = [(f[0], f[1], f[2], f[3], tm) if len(f) == 5 else f for f in new]
    return cen


def sprite(s, kind, at, size=1.0):
    """a billboard sprite at a point, turned to the camera of VIEW"""
    yw, pt = VIEW
    s.display(f'bm:item/dfx_{kind}', pos=at, yaw=-yw, pitch=pt, scale=size)


def scatter(rs, c, r, up=0.0):
    a = rs.uniform(0, 2 * math.pi); d = rs.uniform(0.2, 1) * r
    return (c[0] + d * math.cos(a), c[1] + rs.uniform(-0.4, 1) * r * 0.6 + up, c[2] + d * math.sin(a))


def floor(s, r=10, col=('#2a1418', '#3a1c20'), y=0.0):
    for i in range(-r, r):
        for j in range(-r, r):
            s.solid((i, y - 0.25, j), (i + 1, y, j + 1), col[(i + j) % 2])


def shot(s, label, sub, span, cy, size=440):
    im = s.render(VIEW, size=size, span=span, center=(0, cy, 0))
    return K.label(im, label, sub)


WHITE, CHAR, HOT = (1.55, 1.5, 1.35), (0.22, 0.2, 0.2), (1.3, 1.2, 1.0)

if 'sov' in what:
    import dread_sovereign_art as A
    pz = A.BOSS_POSES['true']['death_2']; S = A.BOSS_SCALE * A.FORM_SCALE['true']
    BURN = [(('shinr', 'shinl'), 322, 338, 346), (('legr', 'legl'), 326, 342, 350), (('weapon',), 328, 344, 350), (('forer', 'forel'), 330, 348, 356),
            (('w3r', 'w3l'), 332, 350, 358), (('armr', 'arml'), 334, 354, 362), (('w2r', 'w2l'), 336, 356, 364), (('body',), 338, 360, 368),
            (('w1r', 'w1l'), 340, 362, 370), (('chest',), 344, 366, 376), (('head', 'fx'), 348, 380, 392)]
    tiles = []
    for T, lab in ((320, 't320 - the smiting: His light strikes it'), (336, 't336 - ablaze: white-gold fire climbs from its feet'),
                   (352, 't352 - its legs charred and crumbling, its arms and wings burning'), (370, 't370 - only its chest, wings and helm left, burning'),
                   (386, 't386 - the helm and eye last, charred; the rest ash'), (420, 't420 - nothing left: ash and feathers of light drifting')):
        s = Scene(RP); floor(s, 14)
        look = {}; burning = []
        for parts, on, ch, fa in BURN:
            for p in parts:
                if T >= fa + 14: look[p] = {'hide': 1}
                elif T >= fa: u = (T - fa) / 14; look[p] = {'k': (1 - u,) * 3, 'dy': -1.6 * u, 'tint': CHAR}
                elif T >= ch: look[p] = {'tint': CHAR}; burning.append(p)
                elif T >= on: look[p] = {'tint': WHITE}; burning.append(p)
        cen = rig(s, A, pz, S, look)
        rs = random.Random(T)
        for p in burning:
            if p in cen:
                for k in range(3): sprite(s, 'hflame', scatter(rs, cen[p], 1.2, 0.8), rs.uniform(2.2, 3.4))
                sprite(s, 'ember', scatter(rs, cen[p], 1.5, 1.5), 0.4)
        for parts, on, ch, fa in BURN:
            if fa <= T < fa + 40:
                for p in parts:
                    c = cen.get(p) or (0, 2 + 2 * (fa - 340) / 10, 0)
                    for k in range(3): sprite(s, 'ash', scatter(rs, c, 1.5, (T - fa) * 0.05), 0.5)
        if T >= 394:
            for k in range(26): sprite(s, 'feather', (rs.uniform(-4, 4), rs.uniform(3, 13), rs.uniform(-4, 4)), 0.9)
            for k in range(18): sprite(s, 'ash', (rs.uniform(-4, 4), rs.uniform(1, 9), rs.uniform(-4, 4)), 0.55)
        tiles.append(shot(s, lab, None, 20, 7.5))
    K.sheet(tiles, OUT + '/sovereign_holy_fire.png', cols=3, title='The Dread Sovereign burns up in holy fire (phase238, within the Last Light)')

if 'vexis' in what:
    import vexis_art as A
    VIEW = (152, 14)
    unl = A.POSES.get('tired', A.POSES['sit_a']); S = A.FOLLOWER_SCALE * 1.6
    ORDER = ['footr', 'footl', 'fxh', 'shinr', 'shinl', 'forer', 'forel', 'podr', 'podl', 'legr', 'legl', 'armr', 'arml', 'ring1', 'ring2', 'back', 'body', 'fx', 'chest', 'head']
    SEAMS = [(488, ('chest', 'head')), (496, ('armr', 'arml', 'body')), (504, ('legr', 'legl', 'forer', 'forel')), (512, ('back', 'podr', 'podl', 'shinr', 'shinl'))]
    tiles = []
    for T, lab in ((480, 't480 - "Show me?" - kneeling, only one'), (500, 't500 - light breaks through its seams; it trembles'),
                   (520, 't520 - cracked all over, blazing'), (540, 't540 - coming apart, part by part, into star dust'),
                   (553, 't553 - the nova: a ring of star dust'), (575, 't575 - the dust drifts, twinkling out')):
        s = Scene(RP); floor(s, 6, ('#1a1c2a', '#22263a'))
        look = {}
        if T >= 486:
            for p in A.PARTS: look[p] = {'tint': HOT}
        for i, p in enumerate(ORDER):
            tt = 532 + i
            if T >= tt + 5 or T >= 552: look[p] = {'hide': 1}
            elif T >= tt: look[p] = {'k': (0.4,) * 3, 'tint': HOT}
        cen = rig(s, A, unl, S, look)
        rs = random.Random(T)
        for t0, parts in SEAMS:
            if t0 <= T < 532:
                for p in parts:
                    if p in cen: sprite(s, 'seam', scatter(rs, cen[p], 0.15), 0.7)
        if 532 <= T < 560:
            done = [p for i, p in enumerate(ORDER) if 532 + i <= T]
            allc = rig(Scene(RP), A, unl, S)
            for p in done[-8:]:
                c = allc.get(p, (0, 1, 0)); age = T - (532 + ORDER.index(p))
                for k in range(3):
                    a = rs.uniform(0, 6.28) + age * 0.15; r = 0.2 + age * 0.06
                    sprite(s, 'star', (c[0] + r * math.cos(a), c[1] + age * 0.05, c[2] + r * math.sin(a)), 0.45)
                sprite(s, 'dust', scatter(rs, c, 0.5), 0.35)
        if T >= 552:
            r = 0.4 + (T - 552) * 0.27
            for k in range(18):
                a = 2 * math.pi * k / 18; sprite(s, 'nova', (r * math.cos(a), 1.3 + (T - 552) * 0.01, r * math.sin(a)), 0.6 * max(0.15, 1 - (T - 552) / 22))
        if T >= 556:
            for k in range(24): sprite(s, 'dust', (rs.uniform(-2.5, 2.5), rs.uniform(0.6, 3.4), rs.uniform(-2.5, 2.5)), 0.35)
            for k in range(8): sprite(s, 'star', (rs.uniform(-2, 2), rs.uniform(1.5, 3.8), rs.uniform(-2, 2)), 0.4)
        tiles.append(shot(s, lab, None, 7.5, 1.6))
    K.sheet(tiles, OUT + '/vexis_star_dust.png', cols=3, title='Admiral Vexis bursts into radiant star dust (phase242, the end of the Unlinking)')

if 'mire' in what:
    import mire_art as A
    VIEW = (-28, 12)
    S = A.SCALE if hasattr(A, 'SCALE') else 2.0
    TENTS = tuple(p for p in A.PARTS if p[0] == 't' and p[1].isdigit())
    tiles = []
    for T, lab in ((10, 't10 - it buckles (death_0)'), (30, 't30 - a heap on its puddle (death_1)'), (50, 't50 - it sags and squashes; the goop wells up'),
                   (70, 't70 - slumped flat, melting into the goop'), (88, 't88 - a bubbling pile of goop'), (114, 't114 - it shrinks into the ground')):
        s = Scene(RP); floor(s, 5, ('#2e2a26', '#363029'))
        pz = A.POSES['death_0' if T < 15 else 'death_1']
        look = {}
        for p in A.PARTS:
            if p == 'puddle':
                if T >= 102: u = min(1, (T - 102) / 26); look[p] = {'k': (1 - u,) * 3}
                continue
            tent = p in TENTS
            if T >= 86: look[p] = {'hide': 1}
            elif T >= 74: u = (T - 74) / 12; look[p] = {'k': (1.35 * (1 - u), 0.3 * (1 - u), 1.35 * (1 - u)), 'dy': -1.0 if not tent else -0.6}
            elif T >= 56: u = min(1, (T - 56) / 18); look[p] = {'k': (1.15 + 0.2 * u, 0.7 - 0.4 * u, 1.15 + 0.2 * u), 'dy': -0.4 - 0.6 * u if not tent else -0.3 - 0.3 * u}
            elif T >= 34: u = min(1, (T - 34) / 20); look[p] = {'k': (1 + 0.15 * u, 1 - 0.3 * u, 1 + 0.15 * u), 'dy': -0.4 * u if not tent else -0.3 * u}
        rig(s, A, pz, S, look)
        g = 0 if T < 42 else (min(1, (T - 42) / 30) * 2.2 if T < 102 else 2.2 * max(0, 1 - (T - 102) / 26))
        if g > 0: s.display('bm:item/dfx_goop', pos=(0, 0.02 - (0.25 * (T - 102) / 26 if T >= 102 else 0), 0), scale=g)
        rs = random.Random(T)
        if 46 <= T < 104:
            for k in range(5): a = rs.uniform(0, 6.28); r = rs.uniform(0, 1.5); sprite(s, 'bubble', (r * math.cos(a), 0.55 + rs.uniform(0, 0.3), r * math.sin(a)), rs.uniform(0.2, 0.55))
            sprite(s, 'pop', (rs.uniform(-1, 1), 0.7, rs.uniform(-1, 1)), 0.5)
        tiles.append(shot(s, lab, None, 7.0, 1.6))
    K.sheet(tiles, OUT + '/mire_melt.png', cols=3, title='A Dread Mire melts into a bubbling pile of goop (phase246)')
print('->', OUT)

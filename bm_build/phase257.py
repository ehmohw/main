"""3.0d: DEATH SPRITES - the little drawn "particles" of the three dramatic deaths (the Dread Sovereign burning up in holy fire,
Admiral Vexis bursting into star dust, a Dread Mire melting into goop). Vanilla particles can only be retextured for the whole game,
so these are small billboarded item displays with their own textures (drawn here in PIL), each one moved by the game's own
interpolation and gone when its lifetime score runs out:

  hflame   a tongue of white-gold holy fire (animated flicker; billboarded upright), rising and dwindling
  ember    a hot gold-white spark, rising and turning as it goes
  ash      a grey flake with a dying orange edge, lifted on the heat, tumbling
  feather  a feather of light, drifting down, swaying
  star     a four-pointed twinkle (animated), spiralling out and up in three hops
  dust     a soft mote of star dust, drifting
  nova     a mote flung straight out (summoned in a ring: ring())
  seam     a crack of light (animated pulse), where it was spawned - it widens
  bubble   a black glossy bubble swelling on the goop, then POP (a splash ring and a sound)
  pop      the splash

  spr(kind, size=1.0, jit=0.0) -> the command that spawns one here (size scales it and its travel; jit scatters where it starts)
  ring(kind, size, n)          -> n of them flung out in a ring, round here

Each sprite: tags bm.dfx (+ bm.dfx_<kind>); bm.dfl its age, bm.dfm its life (<= 59 ticks: a hop is a teleport, and a teleport's
smoothing stops at 59), bm.dfd a hop's length, bm.dfh when the next hop is due. It never glows (no Glowing, nothing invisible),
it isn't a rig's part (no sweep moves it), and an age of 300 kills it whatever happened. admin/uninstall clears them.
The goop (dfx_goop) is a model, not a sprite: a dark glossy pile (an animated, bubbling surface) the Mire leaves (phase246)."""
import math
import random
from PIL import Image, ImageDraw
from nbt import snbt, F, Int, B

PFX = 'p257'
#            billboard, brightness, start scale, end scale, lives, hops, hop (forward, up), yaw turn a hop, spin, random yaw
KINDS = {'hflame': ('vertical', 15, 1.0, 0.22, (11, 13, 15, 12), 1, (0.10, 1.25), 0, False, True),
         'ember': ('center', 15, 0.22, 0.0, (24, 30, 36, 20), 2, (0.55, 1.3), 70, True, True),
         'ash': ('center', 8, 0.42, 0.22, (40, 50, 58, 46), 2, (0.8, 1.4), 50, True, True),
         'feather': ('center', 15, 0.62, 0.0, (52, 58, 55, 48), 3, (0.55, -0.55), 110, True, True),
         'star': ('center', 15, 0.5, 0.0, (30, 36, 42, 27), 3, (1.25, 0.8), 55, True, True),
         'dust': ('center', 15, 0.34, 0.0, (36, 44, 52, 30), 2, (0.45, 0.5), 90, True, True),
         'nova': ('center', 15, 0.62, 0.08, (22,), 1, (6.0, 0.3), 0, True, False),
         'seam': ('center', 15, 0.45, 0.85, (44,), 0, (0, 0), 0, False, True),
         'bubble': ('center', 11, 0.04, 0.55, (10, 14, 16, 12), 1, (0.0, 0.14), 0, False, True),
         'pop': ('center', 11, 0.40, 0.95, (5,), 0, (0, 0), 0, False, True)}
VARK = (1.0, 0.85, 1.2, 0.95)                    # (each life's travel, a little more or less)
_USED = {}                                        # (kind, size code) -> (size, jit): the spawners asked for, generated at the end
OBJS = ['bm.dfl', 'bm.dfm', 'bm.dfd', 'bm.dfh']


def _code(size, jit):
    return f'{int(round(size * 100))}_{int(round(jit * 100))}'


SIZES = (0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6)


def _snap(size, jit):
    """(a few sizes and scatters only: each pair is a spawner of its own, and every sprite's step tells them apart)"""
    return min(SIZES, key=lambda v: abs(math.log(v / max(size, 0.01)))), round(jit * 2) / 2


def spr(kind, size=1.0, jit=0.0):
    assert kind in KINDS, kind
    size, jit = _snap(size, jit)
    c = _code(size, jit); _USED[(kind, c)] = (size, jit)
    return f'function bm:{PFX}/s/{kind}_{c}'


def ring(kind, size=1.0, n=16):
    size = _snap(size, 0)[0]
    c = _code(size, 0.0); _USED[(kind, c)] = (size, 0.0); _USED[('ring', f'{kind}_{c}_{n}')] = (kind, n)
    return f'function bm:{PFX}/r/{kind}_{c}_{n}'


def part_centres(art, pose, scale, models=None):
    """{part: (^x, ^y, ^z)} - where each visible part's model is (its box's middle), in the host's own frame (rotated as it,
    yaw only), as RF.place stands the displays and the game draws their transformations"""
    import rigkit as RK
    M = models if models is not None else art.models()
    U = scale / 16
    xf = RK.solve(art.PIVOT, art.PARENT, pose)
    out = {}
    for p in art.PARTS:
        if hasattr(art, 'HIDDEN') and art.HIDDEN(p, pose): continue
        name = art.model_name(p, pose) if hasattr(art, 'model_name') else (art.model_id(p) if hasattr(art, 'model_id') else art.PREFIX + p)
        els = M.get(name, M.get(f'{getattr(art, "PREFIX", "")}{p}', (None, [])))[1]
        if not els: continue
        lo = [min(min(e['from'][i], e['to'][i]) for e in els) for i in range(3)]
        hi = [max(max(e['from'][i], e['to'][i]) for e in els) for i in range(3)]
        c = [((lo[i] + hi[i]) / 2) / 16 - 0.5 for i in range(3)]
        k = getattr(art, 'PART_K', {}).get(p, 1.0); S = scale * k
        v = (-c[0] * S, c[1] * S, -c[2] * S)                         # (the display's own turn: Ry 180)
        q, t = xf[p]
        v = RK.qrot(q, v)
        px, py, pz = art.PIVOT[p]
        out[p] = (-px * U + v[0] + t[0] * U, py * U + v[1] + t[1] * U, -pz * U + v[2] + t[2] * U)
    return out


def at_part(cen, cmd):
    """(as the host, at it) run cmd at a part's middle"""
    x, y, z = cen
    return f'execute rotated as @s rotated ~ 0 positioned ^{x:.3f} ^{y:.3f} ^{z:.3f} run {cmd}'


# ---------------------------------------------------------------------------------------------------- the art
def _soft(n, cx, cy, r, col, a0=255, k=1.6):
    im = Image.new('RGBA', (n, n), (0, 0, 0, 0)); px = im.load()
    for y in range(n):
        for x in range(n):
            d = math.hypot(x + 0.5 - cx, y + 0.5 - cy) / r
            if d < 1: px[x, y] = col + (int(a0 * (1 - d) ** k),)
    return im


def _flame(i, n=8):
    """a tongue of holy fire, frame i: a white core, gold round it, a pale amber lick at its edge; it sways and flickers"""
    W, H = 32, 32
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); px = im.load()
    ph = 2 * math.pi * i / n
    for y in range(H):
        u = 1 - y / (H - 1)                                          # (0 at its foot, 1 at its tip)
        sway = 2.2 * math.sin(ph + u * 3.0) * u
        half = 12.0 * (1 - u) ** 1.15 * min(1.0, (u + 0.1) / 0.32) ** 0.55 + 0.4
        half *= 1 + 0.10 * math.sin(ph * 2 + u * 7)
        for x in range(W):
            d = abs(x + 0.5 - (W / 2 + sway)) / max(half, 0.01)
            if d > 1: continue
            heat = (1 - d) * (1 - u * 0.75)
            if heat > 0.55: c = (255, 255, 246)
            elif heat > 0.35: c = (255, 240, 170)
            elif heat > 0.18: c = (255, 208, 92)
            else: c = (255, 176, 60)
            a = int(255 * min(1, 0.25 + heat * 1.6) * (1 - max(0, u - 0.8) * 3.5))
            if a > 8: px[x, y] = c + (max(0, min(255, a)),)
    # (a lick torn off the top, rising)
    for (dx, dy, r) in ((3 * math.sin(ph), 4 - 2 * math.cos(ph), 2.2), (-4 * math.cos(ph), 7 + math.sin(ph), 1.4)):
        im.alpha_composite(_soft(W, W / 2 + dx, dy + 2, r * 2, (255, 236, 160), 230, 1.0))
    return im


def _ember():
    im = _soft(16, 8, 8, 7.5, (255, 214, 110), 150, 1.4)
    im.alpha_composite(_soft(16, 8, 8, 3.5, (255, 252, 230), 255, 0.8))
    return im


def _ash():
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = [(3, 6), (7, 2), (12, 4), (14, 9), (10, 13), (5, 12), (2, 9)]
    d.polygon(pts, fill=(70, 66, 64, 255), outline=(150, 92, 44, 255))
    for (x, y) in ((6, 6), (9, 8), (7, 10)): im.putpixel((x, y), (108, 102, 98, 255))
    for (x, y) in ((12, 5), (13, 8)): im.putpixel((x, y), (255, 150, 60, 255))
    return im


def _feather():
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); px = im.load()
    for y in range(16):
        for x in range(16):
            # (a feather lying corner to corner: its shaft on x = y, its vane widest a third of the way up)
            s = (x + y) / 2; o = (x - y) / 1.414
            w = 3.4 * math.sin(math.pi * min(1, max(0, (15 - s) / 14))) ** 0.8
            if abs(o) <= w and 1 <= s <= 15:
                k = abs(o) / max(w, 0.1)
                c = (255, 252, 236) if k < 0.3 else ((255, 238, 180) if k < 0.7 else (255, 218, 130))
                px[x, y] = c + (int(255 * (1 - 0.55 * k)),)
    im.alpha_composite(_soft(16, 8, 8, 9, (255, 240, 190), 60, 1.2))
    return im


def _star(i, n=4):
    k = (0.65, 1.0, 0.8, 0.5)[i % 4]
    im = _soft(16, 8, 8, 7.5 * k, (200, 225, 255), 120, 1.5)
    px = im.load()
    L = 7.5 * k
    for t in range(-7, 8):
        a = max(0.0, 1 - abs(t) / max(L, 0.1))
        if a <= 0: continue
        for (x, y) in ((8 + t, 8), (8, 8 + t)):
            if 0 <= x < 16 and 0 <= y < 16:
                r, g, b, al = px[x, y]
                c = (255, 255, 255) if abs(t) < 2 else (220, 236, 255)
                px[x, y] = c + (max(al, int(255 * a ** 0.7)),)
    for (x, y) in ((7, 7), (9, 7), (7, 9), (9, 9)): px[x, y] = (255, 250, 220, int(200 * k))
    return im


def _dust():
    im = _soft(16, 8, 8, 7.0, (255, 226, 160), 110, 1.3)
    im.alpha_composite(_soft(16, 8, 8, 3.2, (235, 245, 255), 255, 0.9))
    return im


def _nova():
    im = _soft(16, 8, 8, 7.5, (190, 220, 255), 160, 1.2)
    im.alpha_composite(_soft(16, 8, 8, 3.6, (255, 255, 255), 255, 0.7))
    return im


def _seam(i, n=4):
    """a crack of light: a jagged white-hot line, its glow pulsing"""
    k = (0.7, 1.0, 0.85, 0.6)[i % 4]
    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = [(2, 18), (8, 14), (11, 19), (16, 11), (20, 17), (25, 9), (30, 13)]
    d.line(pts, fill=(255, 220, 120, int(150 * k)), width=6)
    d.line(pts, fill=(255, 245, 200, int(230 * k)), width=3)
    d.line(pts, fill=(255, 255, 255, 255), width=1)
    d.line([(16, 11), (15, 5), (18, 2)], fill=(255, 250, 220, int(220 * k)), width=1)
    d.line([(11, 19), (12, 26), (9, 30)], fill=(255, 250, 220, int(220 * k)), width=1)
    return im


def _bubble():
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); px = im.load()
    for y in range(16):
        for x in range(16):
            dd = math.hypot(x + 0.5 - 8, y + 0.5 - 8) / 7.2
            if dd > 1: continue
            c = (26, 8, 12) if dd < 0.78 else (90, 16, 28)
            if dd < 0.6: c = (14, 4, 8)
            px[x, y] = c + (235 if dd < 0.85 else 255,)
    for (x, y, a) in ((5, 4, 255), (6, 4, 230), (4, 5, 230), (5, 5, 200), (10, 11, 120)):
        px[x, y] = (230, 190, 200, a)
    return im


def _pop():
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((1, 1, 14, 14), outline=(60, 10, 18, 255), width=2)
    for a in range(0, 360, 45):
        x, y = 8 + 7 * math.cos(math.radians(a)), 8 + 7 * math.sin(math.radians(a))
        d.point((round(x), round(y)), fill=(130, 30, 44, 255))
    return im


def _goop(i, n=8):
    """the Mire's goop, frame i of n: wet black, red-black swirls, a glossy shine sliding; bubbles swell and burst in turn"""
    rs = random.Random(246)
    im = Image.new('RGBA', (16, 16), (12, 4, 7, 255)); px = im.load()
    for y in range(16):
        for x in range(16):
            v = math.sin(x * 0.9 + i * 0.6) + math.cos(y * 0.7 - i * 0.4) + math.sin((x + y) * 0.5)
            if v > 1.4: px[x, y] = (54, 6, 16, 255)
            elif v > 0.7: px[x, y] = (30, 4, 10, 255)
    sx = (i * 2) % 16
    for k in range(5): px[(sx + k) % 16, (3 + k // 2) % 16] = (120, 70, 84, 255)
    spots = [(rs.randrange(2, 14), rs.randrange(2, 14), rs.randrange(n)) for _ in range(5)]
    for (bx, by, ph) in spots:
        age = (i - ph) % n
        if age < 3:                                                   # (swelling)
            r = 1 + age
            for yy in range(by - r, by + r + 1):
                for xx in range(bx - r, bx + r + 1):
                    if 0 <= xx < 16 and 0 <= yy < 16 and (xx - bx) ** 2 + (yy - by) ** 2 <= r * r:
                        px[xx, yy] = (70, 14, 26, 255)
            if 0 <= bx - 1 < 16 and 0 <= by - 1 < 16: px[bx - 1, by - 1] = (210, 170, 180, 255)
        elif age == 3:                                                # (burst: a ring)
            for (dx, dy) in ((-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (1, -1), (-1, 1)):
                if 0 <= bx + dx < 16 and 0 <= by + dy < 16: px[bx + dx, by + dy] = (110, 24, 40, 255)
    return im


def _strip(frames):
    w, h = frames[0].size
    im = Image.new('RGBA', (w, h * len(frames)), (0, 0, 0, 0))
    for i, f in enumerate(frames): im.paste(f, (0, h * i))
    return im


ANIM = {'dfx_hflame': {'animation': {'frametime': 2, 'interpolate': True}}, 'dfx_star': {'animation': {'frametime': 3, 'interpolate': True}},
        'dfx_seam': {'animation': {'frametime': 3, 'interpolate': True}}, 'dfx_goop': {'animation': {'frametime': 4, 'interpolate': True}}}


def textures():
    return {'dfx_hflame': _strip([_flame(i) for i in range(8)]), 'dfx_ember': _ember(), 'dfx_ash': _ash(), 'dfx_feather': _feather(),
            'dfx_star': _strip([_star(i) for i in range(4)]), 'dfx_dust': _dust(), 'dfx_nova': _nova(),
            'dfx_seam': _strip([_seam(i) for i in range(4)]), 'dfx_bubble': _bubble(), 'dfx_pop': _pop(),
            'dfx_goop': _strip([_goop(i) for i in range(8)])}


def _quad(tex, light):
    f = {'uv': [0, 0, 16, 16], 'texture': '#f'}
    return ({'f': f'bm:block/{tex}'}, [{'from': [0, 0, 8], 'to': [16, 16, 8], 'shade': False, 'light_emission': light,
                                        'faces': {'north': f, 'south': {'uv': [16, 0, 0, 16], 'texture': '#f'}}}])


def _goop_model():
    """a pile of goop: terraced blobs, the model's centre on its foot (8, 8, 8 sits on the ground); 28 x 7 units"""
    def cube(a, b, uvk=1.0):
        fc = {d: {'uv': [0, 0, 16 * uvk, 16 * uvk] if d in ('up', 'down') else [0, 0, 16, 4], 'texture': '#g'} for d in ('north', 'south', 'east', 'west', 'up', 'down')}
        return {'from': list(a), 'to': list(b), 'faces': fc}
    els = [cube((-6, 8, -5), (22, 9.4, 21)), cube((-3, 9.4, -2), (19, 11.2, 18)), cube((1, 11.2, 2), (15, 13.2, 14)),
           cube((4, 13.2, 5), (11, 14.6, 11)), cube((-8, 8, 4), (-6, 8.8, 12)), cube((22, 8, 2), (24, 8.7, 9)),
           cube((5, 8, -7), (12, 8.8, -5)), cube((8, 8, 21), (15, 8.6, 23))]
    return ({'g': 'bm:block/dfx_goop'}, els)


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    light = {'ash': 0, 'bubble': 0, 'pop': 0}
    for k in KINDS:
        R.HATS[f'dfx_{k}'] = _quad(f'dfx_{k}', light.get(k, 15))
    R.HATS['dfx_goop'] = _goop_model()
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + ('dfx_',)

    def post(R2):
        for k, meta in ANIM.items():
            R2.wj(f'assets/bm/textures/block/{k}.png.mcmeta', meta)
    R.POST.append(post)


# ---------------------------------------------------------------------------------------------------- the machinery
def _q(axis, deg):
    s = math.sin(math.radians(deg) / 2)
    return [F(axis[0] * s), F(axis[1] * s), F(axis[2] * s), F(math.cos(math.radians(deg) / 2))]


def _make(G, kind, c, size, jit, rs):
    """one spawner: its summon, its start (a life picked of four, a random turn, a scatter), its moves; -> its step's route"""
    fn = G.fn
    bill, bri, s0, s1, lives, hops, (fw, up), turn, spin, ryaw = KINDS[kind]
    nbt = {'Tags': ['bm.dfx', f'bm.dfx_{kind}', f'bm.dfs_{kind}_{c}', 'bm.dfxn'],
           'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:dfx_{kind}'}},
           'item_display': 'fixed', 'billboard': bill, 'brightness': {'block': Int(bri), 'sky': Int(bri)}, 'view_range': F(1.2),
           'teleport_duration': Int(0), 'interpolation_duration': Int(0),
           'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                              'translation': [F(0), F(0), F(0)], 'scale': [F(round(s0 * size, 3))] * 3}}
    fn(f'{PFX}/s/{kind}_{c}', [f'summon minecraft:item_display ~ ~ ~ {snbt(nbt)}',
                               f'execute as @e[type=minecraft:item_display,tag=bm.dfxn,distance=..0.2] at @s run function bm:{PFX}/i/{kind}_{c}'])
    init = ['tag @s remove bm.dfxn', 'scoreboard players set @s bm.dfl 0', 'execute store result score #v bm.rng run random value 0..%d' % (len(lives) - 1)]
    if ryaw: init.append('execute store result entity @s Rotation[0] float 1 run random value 0..359')
    else: init.append('execute store result entity @s Rotation[0] float 1 run scoreboard players get #ryaw bm.rng')
    step = []
    for v, L in enumerate(lives):
        d = max(1, (L - 2) // hops) if hops else 0
        init.append(f'execute if score #v bm.rng matches {v} run function bm:{PFX}/v/{kind}_{c}_{v}')
        fn(f'{PFX}/v/{kind}_{c}_{v}', [f'scoreboard players set @s bm.dfm {L}', 'scoreboard players set @s bm.dfh 2', f'tag @s add bm.dfv{v}'])
        ang = rs.choice((-1, 1)) * rs.uniform(150, 175)
        rot = f',right_rotation:{snbt(_q((0, 0, 1), ang))}' if spin else ''
        sc = round(s1 * size, 3)
        fn(f'{PFX}/g/{kind}_{c}_{v}', [f'data merge entity @s[type=minecraft:item_display] {{start_interpolation:0,interpolation_duration:{L - 2},transformation:{{scale:[{sc}f,{sc}f,{sc}f]{rot}}}}}'])
        step.append(f'execute if score @s bm.dfl matches 2 if entity @s[tag=bm.dfv{v}] run function bm:{PFX}/g/{kind}_{c}_{v}')
        if hops:
            k = VARK[v % len(VARK)] * size
            fn(f'{PFX}/h/{kind}_{c}_{v}', [f'data merge entity @s[type=minecraft:item_display] {{teleport_duration:{min(d, 59)}}}',
                                           f'execute at @s rotated as @s run tp @s ^ ^{up * k / hops:.3f} ^{fw * k / hops:.3f} ~{turn} ~',
                                           f'scoreboard players add @s bm.dfh {d}', f'execute if score @s bm.dfh matches {2 + hops * d}.. run scoreboard players set @s bm.dfh 9999'])
            step.append(f'execute if score @s bm.dfl = @s bm.dfh if entity @s[tag=bm.dfv{v}] run function bm:{PFX}/h/{kind}_{c}_{v}')
    if jit > 0:
        init.append('execute store result score #j bm.rng run random value 0..7')
        for j in range(8):
            a = 2 * math.pi * j / 8 + 0.4; r = jit * (0.45 + 0.55 * ((j * 5) % 8) / 7)
            init.append(f'execute if score #j bm.rng matches {j} run tp @s ~{r * math.cos(a):.2f} ~{jit * 0.5 * math.sin(a * 3):.2f} ~{r * math.sin(a):.2f}')
    fn(f'{PFX}/i/{kind}_{c}', init)
    fn(f'{PFX}/st/{kind}_{c}', step)
    return f'execute if entity @s[tag=bm.dfs_{kind}_{c}] run return run function bm:{PFX}/st/{kind}_{c}'


def generate(G):
    """(late: after every phase that asked for a spawner) the spawners, the step, the cleanup"""
    fn = G.fn
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in OBJS] + ['scoreboard players set #ryaw bm.rng 0']
    G.OBJECTIVES += OBJS
    rs = random.Random(257)
    pop_cmd = spr('pop', 0.6)
    show = [f'execute positioned ^{(i % 5) * 2 - 4} ^1.2 ^{5 + (i // 5) * 3} run {spr(k, 1.0, 0.3)}' for i, k in enumerate(k for k in KINDS if k != 'pop')]
    step = ['scoreboard players add @s bm.dfl 1', 'execute if score @s bm.dfl matches 300.. run return run kill @s',
            'execute if score @s bm.dfl >= @s bm.dfm run return run function bm:p257/end',
            'execute unless score @s bm.dfl matches 2 unless score @s bm.dfl = @s bm.dfh run return 0']
    for (kind, c), val in sorted(_USED.items()):
        if kind == 'ring': continue
        step.append(_make(G, kind, c, val[0], val[1], rs))
    fn(f'{PFX}/step', step)
    # (the rings: n flung straight out, evenly round - each one's line its turn, #ryaw, as it's summoned)
    for (kind, key), val in sorted(_USED.items()):
        if kind != 'ring': continue
        k2, n = val
        c = key[len(k2) + 1:].rsplit('_', 1)[0]
        body = []
        for i in range(n):
            body += [f'scoreboard players set #ryaw bm.rng {round(360 * i / n)}', f'function bm:{PFX}/s/{k2}_{c}']
        fn(f'{PFX}/r/{key}', body)
    fn(f'{PFX}/end', ['execute if entity @s[tag=bm.dfx_bubble] at @s run ' + pop_cmd,
                      'execute if entity @s[tag=bm.dfx_bubble] at @s run playsound minecraft:block.bubble_column.bubble_pop hostile @a[distance=..24] ~ ~ ~ 0.8 0.7',
                      'kill @s'])
    G.FUNCS['tick'].append(f'execute as @e[type=minecraft:item_display,tag=bm.dfx] at @s run function bm:{PFX}/step')
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[type=minecraft:item_display,tag=bm.dfx]')
    fn('admin/dfx', show * 3)
    G.FUNCS['admin/help'].append(G.tellraw('@s', [{'text': '/function bm:admin/dfx', 'color': 'yellow'}, {'text': '  the death sprites (3.0d), a few of each, in front of you', 'color': 'gray'}]))

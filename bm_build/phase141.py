"""Phase 141 (2.78): A DOLL OF EVERY FOLLOWER. Emma had a doll; now they all do - Cecil, Celi, Leo, Democratus, KillerWatt,
Apophiss, Tullius, Zib and Pearlman, each a little statue of them in their idle pose (their figurine, one model you can hold).
Cecil sells them beside Emma's (3 Trophies each). Right-click a block: set it down. Right-click it: it twirls, in its own
colours and sounds. It shimmers now and then while it stands. Sneak + punch: pick it up.

Importing registers the items; generate(G) runs after phase46 (it copies the Emma doll's placer); rp(R) adds a POST that builds
each doll's model from the figurine's parts (phase134), merged into one."""
import math
from items import item, T, TOTEM
from useitem import hold, HOLD
from nbt import snbt, B, F, Int

# (doll, figurine, name, colour, what it is, click particle, click sound, idle shimmer)
DOLLS = [('doll_cecil', 'cecil_gem', 'Cecil', '#9a6ad8', 'A felt doll of Cecil, staff and all.', 'minecraft:witch', 'minecraft:block.amethyst_block.chime', 'minecraft:enchant'),
         ('doll_celi', 'celi_charm', 'Celi', '#a8e4ff', 'A doll of Celi, spear on her shoulder.', 'minecraft:snowflake', 'minecraft:block.powder_snow.step', 'minecraft:snowflake'),
         ('doll_leo', 'leo_crest', 'Leo', '#4a8ad8', 'A doll of Sir Leo, ready for anything.', 'minecraft:nautilus', 'minecraft:block.bell.use', 'minecraft:bubble_pop'),
         ('doll_demo', 'demo_seal', 'Democratus', '#c0c8e0', 'A doll of Democratus, scythe and storm-cloak.', 'minecraft:electric_spark', 'minecraft:item.trident.thunder', 'minecraft:electric_spark'),
         ('doll_kw', 'kw_spark', 'KillerWatt', '#ffe04a', 'A doll of KillerWatt, tendrils crackling.', 'minecraft:electric_spark', 'minecraft:block.beacon.power_select', 'minecraft:wax_off'),
         ('doll_apo', 'apo_oath', 'Apophiss', '#3a7a3a', 'A doll of the Serpent King. It looks back.', 'minecraft:soul_fire_flame', 'minecraft:entity.wither.ambient', 'minecraft:soul'),
         ('doll_tul', 'tul_coin', 'Tullius', '#7ab0c0', 'A doll of Captain Tullius, dripping wet.', 'minecraft:splash', 'minecraft:entity.player.splash', 'minecraft:dripping_water'),
         ('doll_zib', 'donadian_medal', 'Zib', '#7aff9a', 'A doll of Zib the Donadian. Batteries not included.', 'minecraft:glow', 'minecraft:block.beacon.activate', 'minecraft:glow'),
         ('doll_pearl', 'pearl_card', 'Pearlman', '#e8e8f0', 'A doll of Pearlman, salespenguin of the year.', 'minecraft:happy_villager', 'minecraft:block.note_block.pling', 'minecraft:end_rod')]
PRICE = ('trophy', 3)
SIZE = 0.62                  # (as tall as Emma's, set down)

for _d, _f, _n, _c, _what, *_ in DOLLS:
    item(_d, TOTEM, f'{_n} Doll', _c, [_what, ('Right-click a block: set it down.', 'blue'), ('Right-click it: it twirls.', 'blue'),
                                       ('Sneak + punch: pick it up.', 'gray')],
         model=f'bm:{_d}', stack=16, cat='fun', comps=hold('none'))
    HOLD[_d] = f'bm:p141/{_d}/use'


def extend_offers(O, offer):
    O['wizard'] += [offer(PRICE, (d, 1)) for d, *_ in DOLLS]


def generate(G):
    fn, give, title = G.fn, G.give, G.title
    ident = [F(0), F(0), F(0), F(1)]
    fast, second = [], []
    for d, fig, name, col, what, ptc, snd, idle in DOLLS:
        P = f'p141/{d}/'
        fn(P + 'use', [l.replace('p46/emma/', P).replace('"emma_doll"', f'"{d}"') for l in G.FUNCS['p46/emma/use']])
        fn(P + 'ray', [l.replace('p46/emma/', P) for l in G.FUNCS['p46/emma/ray']])
        fn(P + 'hit', [l.replace('p46/emma/', P) for l in G.FUNCS['p46/emma/hit']])
        disp = snbt({'Tags': ['bm.dolld', f'bm.{d}d', 'bm.p45new'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:{d}'}},
                     'item_display': 'fixed', 'teleport_duration': Int(6),
                     'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0), F(0)], 'scale': [F(SIZE)] * 3}})   # (its feet at the model's middle: at the block's top)
        hit = snbt({'Tags': ['bm.dollhit', f'bm.{d}hit', 'bm.p45hit', 'bm.p45new'], 'width': F(0.55), 'height': F(SIZE + 0.05), 'response': B(1)})
        fn(P + 'spawn', [f'summon minecraft:item_display ~ ~ ~ {disp}', f'summon minecraft:interaction ~ ~ ~ {hit}', 'tp @e[tag=bm.p45new,distance=..0.5] ~ ~ ~ ~ 0',
                         'tag @e[tag=bm.p45new,distance=..0.5] remove bm.p45new', 'playsound minecraft:block.wool.place block @a[distance=..12] ~ ~ ~ 1 1.2',
                         f'particle {ptc} ~ ~0.4 ~ 0.25 0.25 0.25 0.02 8'])
        fast.append(f'execute as @e[type=minecraft:interaction,tag=bm.{d}hit] if data entity @s interaction at @s run function bm:{P}click')
        fn(P + 'click', [f'execute as @e[type=minecraft:item_display,tag=bm.{d}d,distance=..0.4] at @s run tp @s ~ ~ ~ ~120 0',
                         f'playsound {snd} block @a[distance=..12] ~ ~ ~ 0.6 1.4', f'particle {ptc} ~ ~{SIZE:.2f} ~ 0.3 0.3 0.3 0.02 8', 'data remove entity @s interaction'])
        fast.append(f'execute as @e[type=minecraft:interaction,tag=bm.{d}hit] if data entity @s attack at @s run function bm:{P}punch')
        fn(P + 'punch', ['tag @s add bm.p45me', f'execute on attacker if predicate bm:p20/sneaking run function bm:{P}pick', 'tag @s remove bm.p45me', 'data remove entity @s attack'])
        fn(P + 'pick', [give(d), f'execute as @e[type=minecraft:interaction,tag=bm.p45me] at @s run function bm:{P}gone', 'playsound minecraft:entity.item.pickup player @s ~ ~ ~ 1 1'])
        fn(P + 'gone', [f'kill @e[type=minecraft:item_display,tag=bm.{d}d,distance=..0.6]', 'particle minecraft:poof ~ ~0.3 ~ 0.2 0.2 0.2 0.02 6', 'kill @s'])
        # (it shimmers now and then while it stands)
        second.append(f'execute as @e[type=minecraft:item_display,tag=bm.{d}d] at @s if predicate bm:p141/now_and_then run particle {idle} ~ ~{SIZE * 0.7:.2f} ~ 0.2 0.25 0.2 0 2')
    G.wjson('bm/predicate/p141/now_and_then.json', {'condition': 'minecraft:random_chance', 'chance': 0.25})
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    G.FUNCS['loop/second'][-1:-1] = second
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.dolld]', 'kill @e[type=minecraft:interaction,tag=bm.dollhit]']


# ================================================================================================= the dolls' models
def _rx(a): return [[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]]


def rp(R):
    def post(R2):
        import json, os
        import numpy as np
        import rigkit as RK
        import phase134 as P134
        from heldfx import eul
        def quat(q):
            x, y, z, w = q
            return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                             [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                             [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
        def model_ref(mid):                               # an item id -> the model its definition shows (its plain case)
            ns, n = mid.split(':')
            p = R2.p('assets', ns, 'items', f'{n}.json')
            if not os.path.exists(p): return f'{ns}:item/{n}'
            m = json.load(open(p))['model']
            while m.get('type') != 'minecraft:model':
                m = m.get('fallback') or m.get('on_false') or (m.get('cases') or m.get('entries'))[0]['model']
            return m['model']
        def load(ref):                                    # a model with its parents' textures and elements folded in
            ns, n = ref.split(':')
            d = json.load(open(R2.p('assets', ns, 'models', f'{n}.json')))
            if 'parent' in d and d['parent'].startswith('bm:'):
                base = load(d['parent'])
                base['textures'] = dict(base.get('textures', {}), **d.get('textures', {}))
                if 'elements' in d: base['elements'] = d['elements']
                if 'display' in d: base['display'] = dict(base.get('display', {}), **d['display'])
                return base
            return d
        Ry = np.diag([-1.0, 1.0, -1.0])
        FIG = P134.figures()
        for d, fig, *_ in DOLLS:
            lo, h, x0, x1, z0, z1 = P134.FIT[fig]
            f = 1.0 / h                                     # (the doll a block tall in its own model; the display shrinks it)
            cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
            tex, els = {}, []
            for i, (mid, (x, y, z), L, Rr, sc) in enumerate(FIG[fig][1]):
                m = load(model_ref(mid))
                fx = m.get('display', {}).get('fixed', {})
                Rd = eul(fx.get('rotation', [0, 0, 0])); td = np.array(fx.get('translation', [0, 0, 0])) / 16; sd = float(np.mean(fx.get('scale', [1, 1, 1])))
                t = np.array([(x - cx) * f, (y - lo) * f, (z - cz) * f])
                Q = quat(L) @ quat(Rr)
                A = Q @ Ry @ Rd * (sc * f * sd)             # (world = A (p/16 - 0.5) + b, the figure's feet at 0)
                b = t + Q @ Ry @ td * (sc * f)
                # (into the doll's own frame, which the game turns half round and centres: c = 16 (Ry w + 0.5))
                M = Ry @ A / 16 * 16                        # c = M p + k, per model unit
                k = 16 * (Ry @ (b - A @ np.full(3, 0.5)) + 0.5)
                g = float(np.cbrt(abs(np.linalg.det(M))))
                Rm = M / g
                for kk, v in m.get('textures', {}).items():
                    tex[f'p{i}_{kk}'] = v if not v.startswith('#') else f'#p{i}_{v[1:]}'
                for e in m.get('elements', []):
                    r = e.get('rotation')
                    if r:
                        o = np.array(r['origin'], float)
                        if 'axis' in r:
                            ang = {a: (math.radians(r['angle']) if a == r['axis'] else 0.0) for a in 'xyz'}
                        else:
                            ang = {a: math.radians(r.get(a, 0.0)) for a in 'xyz'}
                        cz_, sz_ = math.cos(ang['z']), math.sin(ang['z']); cy_, sy_ = math.cos(ang['y']), math.sin(ang['y']); cx_, sx_ = math.cos(ang['x']), math.sin(ang['x'])
                        Re = np.array([[cz_, -sz_, 0], [sz_, cz_, 0], [0, 0, 1]]) @ np.array([[cy_, 0, sy_], [0, 1, 0], [-sy_, 0, cy_]]) @ np.array([[1, 0, 0], [0, cx_, -sx_], [0, sx_, cx_]])
                    else:
                        o, Re = np.array([8.0, 8.0, 8.0]), np.eye(3)
                    Rn = Rm @ Re
                    dsh = g * (Rm @ o) + k - g * o
                    fr, to = g * np.array(e['from'], float) + dsh, g * np.array(e['to'], float) + dsh
                    on = g * o + dsh
                    ax, ay, az = RK.euler(Rn.tolist())
                    ne = {'from': [round(float(v), 4) for v in np.minimum(fr, to)], 'to': [round(float(v), 4) for v in np.maximum(fr, to)],
                          'faces': {fk: dict(fv, texture=f'#p{i}_{fv["texture"][1:]}') for fk, fv in e['faces'].items()}}
                    if abs(ax) + abs(ay) + abs(az) > 1e-4:
                        ne['rotation'] = {'origin': [round(float(v), 4) for v in on], 'x': ax, 'y': ay, 'z': az}
                    for kk in ('shade', 'light_emission'):
                        if kk in e: ne[kk] = e[kk]
                    els.append(ne)
            tex['particle'] = next(v for kk, v in tex.items() if not v.startswith('#'))
            # (the doll stands from the model's middle up: each view lowered by half its height, at that view's scale)
            disp = {'gui': {'rotation': [20, 200, 0], 'translation': [0, -5.6, 0], 'scale': [0.7, 0.7, 0.7]},
                    'ground': {'rotation': [0, 0, 0], 'translation': [0, -0.5, 0], 'scale': [0.35, 0.35, 0.35]},
                    'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]},
                    'head': {'rotation': [0, 180, 0], 'translation': [0, 1.5, 0], 'scale': [0.6, 0.6, 0.6]},
                    'thirdperson_righthand': {'rotation': [0, 180, 0], 'translation': [0, -1, 1.5], 'scale': [0.3, 0.3, 0.3]},
                    'thirdperson_lefthand': {'rotation': [0, 180, 0], 'translation': [0, -1, 1.5], 'scale': [0.3, 0.3, 0.3]},
                    'firstperson_righthand': {'rotation': [0, 200, 0], 'translation': [0, -1, 0], 'scale': [0.35, 0.35, 0.35]},
                    'firstperson_lefthand': {'rotation': [0, 160, 0], 'translation': [0, -1, 0], 'scale': [0.35, 0.35, 0.35]}}
            R2.wj(f'assets/bm/models/item/{d}.json', {'textures': tex, 'elements': els, 'display': disp})
            R2.wj(f'assets/bm/items/{d}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/{d}'}})
    R.POST.append(post)

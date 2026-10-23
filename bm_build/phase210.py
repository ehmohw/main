"""2.94: EFFECT SPRITES - the big blows drawn, not only sparkled: PixelLab's effects artist painted each one as a short
animation (ref/pixellab/vfx/<name>.png and .json - its frames, their timing, its anchor), and it plays in the world on a
billboarded display (always facing you), full-bright, as a flipbook: one model per frame, the display stepped to the next
each tick, so a burst always starts at its first frame (an animated texture runs on the game's own clock, and would start
anywhere). Apophiss's black fire (phase131) is the same idea, as a looping texture.

  fx(name, scale=1.0, dy=0.0) -> the command that plays it here (as anyone, at the spot)
  USES: the synergy attacks (phase208, by role), the big blows (Dennis's Mother Lode, Mr. Capshun's Rainbow Stroke, Apophiss's
  Black Flame Coil, Ashur's Inferno - phase205's champions), the Sky Buddies' attacks (phase211), Dennis's searing throws
  (phase212) and the pixel followers' retro attacks (phase213)."""
import json
import os
from PIL import Image
from nbt import snbt, F, Int, B

HERE = os.path.dirname(os.path.abspath(__file__))
VFX = os.path.join(HERE, 'ref', 'pixellab', 'vfx')
PX = 32.0                                 # (sprite pixels to a block at scale 1)


def _load(name):
    meta = json.load(open(os.path.join(VFX, name + '.json')))
    fr = meta['frames']; fr = list(fr.values()) if isinstance(fr, dict) else fr
    return Image.open(os.path.join(VFX, name + '.png')).convert('RGBA'), fr


def names():
    return sorted(f[:-5] for f in os.listdir(VFX) if f.endswith('.json'))


_INFO = {}


def info(name):
    """(frames, size: the square canvas each frame sits in, pivot in it)"""
    if name not in _INFO:
        _sheet, fr = _load(name)
        w, h = fr[0]['frame']['w'], fr[0]['frame']['h']
        pv = fr[0].get('pivot') or {'x': 0.5, 'y': 0.5}
        px, py = min(max(pv['x'], 0.0), 1.0) * w, min(max(pv['y'], 0.0), 1.0) * h
        half = max(px, w - px, py, h - py)                                    # (the frame put in a square round its anchor)
        n = 16
        while n < 2 * half:
            n *= 2
        _INFO[name] = (len(fr), n, (px, py), (w, h))
    return _INFO[name]


def textures():
    T = {}
    for nm in names():
        sheet, fr = _load(nm)
        n_fr, n, (px, py), (w, h) = info(nm)
        for i, f in enumerate(fr):
            r = f['frame']
            im = sheet.crop((r['x'], r['y'], r['x'] + r['w'], r['y'] + r['h']))
            c = Image.new('RGBA', (n, n), (0, 0, 0, 0))
            c.alpha_composite(im, (int(round(n / 2 - px)), int(round(n / 2 - py))))
            T[f'fx_{nm}_{i}'] = c
    return T


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    for nm in names():
        n_fr, n, _pv, _wh = info(nm)
        h = 8.0                                                               # (a frame is one block wide as built; fx() scales it)
        for i in range(n_fr):
            face = {'uv': [0, 0, 16, 16], 'texture': '#f'}
            R.HATS[f'fx_{nm}_{i}'] = ({'f': f'bm:block/fx_{nm}_{i}'}, [{'from': [8 - h, 8 - h, 8], 'to': [8 + h, 8 + h, 8], 'shade': False, 'light_emission': 15,
                                                                         'faces': {'north': face, 'south': {'uv': [16, 0, 0, 16], 'texture': '#f'}}}])


def fx(name, scale=1.0, dy=0.0):
    """play an effect here (it faces whoever looks): the display summoned at its first frame"""
    n_fr, n, _pv, _wh = info(name)
    s = round(scale * n / PX, 4)                                               # (PX sprite pixels to the block at scale 1)
    nbt = {'Tags': ['bm.fxs', f'bm.fxs_{name}'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:fx_{name}_0'}},
           'item_display': 'fixed', 'billboard': 'center', 'brightness': {'block': Int(15), 'sky': Int(15)}, 'view_range': F(2.0),
           'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)], 'translation': [F(0), F(0), F(0)],
                              'scale': [F(s)] * 3}}
    return f'summon minecraft:item_display ~ ~{dy} ~ {snbt(nbt)}'


def generate(G):
    fn = G.fn
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.fxf dummy']
    G.OBJECTIVES.append('bm.fxf')
    step = ['scoreboard players add @s bm.fxf 1']
    for nm in names():
        n_fr = info(nm)[0]
        step.append(f'execute if entity @s[tag=bm.fxs_{nm}] run return run function bm:p210/f/{nm}')
        fn(f'p210/f/{nm}', [f'execute if score @s bm.fxf matches {n_fr}.. run return run kill @s'] +
           [f'execute if score @s bm.fxf matches {i} run return run data modify entity @s item.components."minecraft:item_model" set value "bm:fx_{nm}_{i}"'
            for i in range(1, n_fr)])
    step.append('kill @s')
    fn('p210/step', step)
    G.FUNCS['tick'].append('execute as @e[type=minecraft:item_display,tag=bm.fxs] run function bm:p210/step')
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[type=minecraft:item_display,tag=bm.fxs]')
    # (admin) every effect in a row in front of you, one after another
    fn('admin/fx', [f'execute positioned ^{(i % 6) * 2.2 - 5.5:.1f} ^1 ^{4 + (i // 6) * 3} run {fx(nm, 0.8)}' for i, nm in enumerate(names())])
    G.FUNCS['admin/help'].append(G.tellraw('@s', [{'text': '/function bm:admin/fx', 'color': 'yellow'}, {'text': '  every effect sprite, played in front of you', 'color': 'gray'}]))


def hooks(G):
    """(late: after phase163, phase198, phase205 and phase208) the big blows get their sprites"""
    import phase208 as P208
    F = G.FUNCS
    for role in P208.ROLES:
        F[f'p208/{role}_duo'].insert(0, fx(f'syn_{role}', 1.6, 0.8))
        F[f'p208/{role}_trio'].insert(0, fx(f'syn_{role}', 2.4, 1.0))
    big = {'p163/dw/ult_hit': ('dennis_lode', 2.6, 0.0), 'p198/rainbow': ('capshun_rainbow', 2.6, 1.2),
           'p205/ab/apo': ('apo_coil', 2.4, 0.0), 'p205/ab/ashur': ('ashur_inferno', 2.4, 0.4)}
    for f_, (nm, sc, dy) in big.items():
        assert f_ in F, f_
        F[f_].insert(0, fx(nm, sc, dy) if not f_.startswith('p198') else f'execute positioned ^ ^ ^2.5 run {fx(nm, sc, dy)}')

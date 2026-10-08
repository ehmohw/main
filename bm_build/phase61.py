"""Phase 2.48: the Hollow Gate - a real portal to the Hollow Throne.

- THE HOLLOW GATE (placeable; the reward for conquering Wilfrey's Keep, and sold by The Fence): a worn deepslate archway,
  4 blocks tall, with five empty sockets - one cut for each Conquest Emblem, in conquest order up and over the arch.
  Use it on the ground to set it up (it squares itself to face you; it needs a clear 4x5 space).
- SOCKETS: right-click a socket holding its Emblem to set it in (it glows in its dungeon's colour). Sneak + punch a
  socket to take its Emblem back. With all five set, the arch fills with the swirling dark of the Hollow and hums.
- PASSING THROUGH: walk into the open gate. Only those whose record shows all five conquests may pass - anyone else is
  thrown back. You return through the rift in the Hollow Throne, arriving just in front of the gate.
- Sneak + punch an empty socket of a gate with no Emblems in it to pack the gate back up.
- The Shard of the Hollow Throne is retired: using an old one turns it into a Hollow Gate. The Warpstone still comes only
  from defeating the Hollow King (inside, through the gate)."""
import sys
from items import item, T, TOTEM
from useitem import hold, HOLD
from nbt import snbt, B, F, Int

HG = '#c8c4d8'
S = 1.5                                         # display scale of the gate model
ORDER5 = ['brood', 'frost', 'tide', 'hex', 'keep']
# socket model positions (x, y, front z) -> blocks in the gate's own frame: ^x left, ^y up, ^z out of the front
SOCK_M = {'brood': (-8, 4, 4), 'frost': (-8, 16, 4), 'tide': (8, 28.5, 3), 'hex': (24, 16, 4), 'keep': (24, 4, 4)}
def _loc(xm, ym, zm): return (round(-(xm - 8) / 16 * S, 3), round((ym + 14) / 16 * S, 3), round(-(zm - 8) / 16 * S + 0.06, 3))
SOCK = {d: _loc(*m) for d, m in SOCK_M.items()}
TY = round((8 + 14) / 16 * S, 4)                 # lifts model y = -14 to the ground

if '--phase2' in sys.argv:
    item('hollow_gate', TOTEM, 'Hollow Gate', HG,
         ['An archway of old deepslate, cold to the touch.', 'Five empty sockets run up and over it.',
          ('Use on the ground: set it up (it needs a 4x5 space).', 'blue'),
          ('Set a Conquest Emblem in each socket and it opens', 'blue'), ('onto the Hollow Throne.', 'blue'),
          ('Only those who have conquered all five may pass.', 'gray'),
          ('Sneak + punch a socket: take its Emblem back.', 'dark_gray'), ('Sneak + punch an empty gate: pack it up.', 'dark_gray')],
         model='bm:hollow_gate', stack=1, cat='p2map', glint=False, comps=hold('none'))
    HOLD['hollow_gate'] = 'bm:p61/use'


def extend_offers(O, offer):
    O['fence'].append(offer(('token', 10), ('hollow_gate', 1)))


def generate(G):
    if not G.PHASE2: return
    from p2.config import D
    from p2.data import HOLLOW_VER
    fn, title, tellraw, give = G.fn, G.title, G.tellraw, G.give
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    tick, second, fast = [], [], []
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.hgcd dummy', 'scoreboard objectives add bm.hgt dummy']
    G.OBJECTIVES += ['bm.hgcd', 'bm.hgt']
    tick.append('scoreboard players remove @a[scores={bm.hgcd=1..}] bm.hgcd 1')
    holds = '*[minecraft:custom_data~{bm:"%s"}]'
    def disp(model, tags, sc=S, ty=TY, bright=None):
        d = {'Tags': tags, 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': model}},
             'item_display': 'fixed', 'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                                         'translation': [F(0), F(ty), F(0)], 'scale': [F(sc)] * 3}}
        if bright: d['brightness'] = {'block': Int(bright), 'sky': Int(15)}
        return d

    # ================================================================== setting it up
    fn('p61/use', ['execute if dimension bm:hollow_throne run return run ' + say('The gate will not stand here - you are already beyond the world.'),
                   'scoreboard players set #placed bm.rng 0', 'scoreboard players set #ray bm.rng 25', 'tag @s add bm.placer',
                   'execute anchored eyes positioned ^ ^ ^ run function bm:p61/ray', 'tag @s remove bm.placer',
                   'execute if score #placed bm.rng matches 0 run return 0',
                   'execute unless entity @s[gamemode=creative] if items entity @s weapon.mainhand ' + holds % 'hollow_gate' +
                   ' run return run item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
                   'execute unless entity @s[gamemode=creative] run item modify entity @s weapon.offhand {function:"minecraft:set_count",count:-1,add:true}'])
    fn('p61/ray', ['execute unless block ~ ~ ~ #minecraft:replaceable run return run function bm:p61/hit',
                   'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p61/ray'])
    fn('p61/hit', ['execute align xyz positioned ~0.5 ~1 ~0.5 if entity @e[type=minecraft:marker,tag=bm.hgate,distance=..10] run return run ' +
                   title('@a[tag=bm.placer]', 'actionbar', T('Too close to another Hollow Gate.', 'gray')),
                   'execute align xyz positioned ~0.5 ~1 ~0.5 run function bm:p61/try'])
    # (at the base's centre) square up to face the placer, check the space, then build
    fn('p61/try', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.hgate","bm.hgnew"]}'] +
       [f'execute if entity @a[tag=bm.placer,y_rotation={lo}..{hi}] run tp @e[type=minecraft:marker,tag=bm.hgnew,distance=..0.5] ~ ~ ~ {yaw} 0'
        for lo, hi, yaw in ((-45, 44.99, 180), (45, 134.99, -90), (135, 180, 0), (-180, -135.01, 0), (-135, -45.01, 90))] +
       ['execute as @e[type=minecraft:marker,tag=bm.hgnew,distance=..0.5] at @s run function bm:p61/space'])
    pts = [(x, y) for x in (-1.5, -0.75, 0, 0.75, 1.5) for y in (0.3, 1.3, 2.3, 3.3, 4.1)]
    fn('p61/space', [f'execute unless block ^{x} ^{y} ^ #minecraft:replaceable run return run function bm:p61/nospace' for x, y in pts] +
       ['function bm:p61/build'])
    fn('p61/nospace', ['kill @s', title('@a[tag=bm.placer]', 'actionbar', T('The gate needs a clear space 4 wide and 5 high.', 'gray'))])
    sbox = lambda d: {'Tags': ['bm.hgs', f'bm.hgs_{d}', 'bm.hgnew'], 'width': F(0.55), 'height': F(0.55), 'response': B(1)}
    fn('p61/build', ['tag @s remove bm.hgnew', 'scoreboard players set #placed bm.rng 1',
                     f'summon minecraft:item_display ~ ~ ~ {snbt(disp("bm:hollow_gate", ["bm.hgd", "bm.hgnew"]))}'] +
       [f'execute positioned ^{x} ^{y - 0.27} ^{z} run summon minecraft:interaction ~ ~ ~ {snbt(sbox(d))}' for d, (x, y, z) in SOCK.items()] +
       ['execute as @e[tag=bm.hgnew,distance=..5] at @s rotated as @e[type=minecraft:marker,tag=bm.hgate,sort=nearest,limit=1] run tp @s ~ ~ ~ ~ 0',
        'tag @e[tag=bm.hgnew,distance=..5] remove bm.hgnew',
        'playsound minecraft:block.deepslate.place block @a[distance=..24] ~ ~ ~ 1 0.6', 'playsound minecraft:block.respawn_anchor.charge block @a[distance=..24] ~ ~ ~ 0.6 0.5',
        'particle minecraft:ash ~ ~2 ~ 1 1.5 0.3 0 60', tellraw('@a[tag=bm.placer]', [T('The Hollow Gate stands. Five sockets wait for their Emblems.', HG, italic=True)])])

    # ================================================================== the sockets
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.hgs] if data entity @s interaction at @s run function bm:p61/sock/click',
             'execute as @e[type=minecraft:interaction,tag=bm.hgs] if data entity @s attack at @s run function bm:p61/sock/punch']
    fn('p61/sock/click', ['tag @a remove bm.hgu', 'execute on target run tag @s add bm.hgu', 'data remove entity @s interaction'] +
       [f'execute if entity @s[tag=bm.hgs_{d}] run function bm:p61/sock/put_{d}' for d in ORDER5] + ['tag @a remove bm.hgu'])
    fn('p61/sock/punch', ['tag @a remove bm.hgu', 'execute on attacker run tag @s add bm.hgu', 'data remove entity @s attack',
                          'execute unless entity @a[tag=bm.hgu,predicate=bm:p20/sneaking] run return run ' +
                          title('@a[tag=bm.hgu]', 'actionbar', T('Sneak + punch: take an Emblem back (or pack up an empty gate).', 'gray')),
                          'execute if entity @s[tag=bm.hgfull] run return run function bm:p61/sock/takeback',
                          'execute as @e[type=minecraft:marker,tag=bm.hgate,distance=..4.6,sort=nearest,limit=1] at @s run function bm:p61/pack'])
    G.FUNCS['p61/sock/punch'].append('tag @a remove bm.hgu')
    for i, d in enumerate(ORDER5):
        col = D[d]['color']
        r, g, b = (int(col[k:k + 2], 16) / 255 for k in (1, 3, 5))
        fn(f'p61/sock/put_{d}', [
            'execute if entity @s[tag=bm.hgfull] run return run ' + title('@a[tag=bm.hgu]', 'actionbar', T('That socket already holds its Emblem.', 'gray')),
            f'execute unless items entity @a[tag=bm.hgu,limit=1] weapon.mainhand {holds % ("emblem_" + d)} run return run ' +
            title('@a[tag=bm.hgu]', 'actionbar', [T('This socket is cut for the Conquest Emblem of ', 'gray'), T(D[d]['boss'], col, bold=True), T('.', 'gray')]),
            'item modify entity @a[tag=bm.hgu,limit=1] weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
            'tag @s add bm.hgfull',
            f'summon minecraft:item_display ~ ~0.27 ~ {snbt(dict(disp(f"bm:emblem_{d}", ["bm.hge", f"bm.hge_{d}", "bm.hgnew"], 0.42, 0, 15)))}',
            'execute as @e[type=minecraft:item_display,tag=bm.hgnew,distance=..1] at @s rotated as @e[type=minecraft:marker,tag=bm.hgate,distance=..4.6,sort=nearest,limit=1] run tp @s ~ ~ ~ ~ 0',
            'tag @e[tag=bm.hgnew,distance=..1] remove bm.hgnew',
            f'particle minecraft:dust{{color:[{r:.2f},{g:.2f},{b:.2f}],scale:1.4}} ~ ~0.27 ~ 0.15 0.15 0.15 0 20',
            f'playsound minecraft:block.end_portal_frame.fill block @a[distance=..24] ~ ~ ~ 1 {0.7 + i * 0.12:.2f}',
            'execute as @e[type=minecraft:marker,tag=bm.hgate,distance=..4.6,sort=nearest,limit=1] at @s run function bm:p61/check'])
        fn(f'p61/sock/give_{d}', [f'loot give @a[tag=bm.hgu,limit=1] loot bm:items/emblem_{d}'])
    fn('p61/sock/takeback', [f'execute if entity @s[tag=bm.hgs_{d}] run function bm:p61/sock/give_{d}' for d in ORDER5] +
       ['tag @s remove bm.hgfull', 'kill @e[type=minecraft:item_display,tag=bm.hge,distance=..0.6]',
        'playsound minecraft:block.deepslate.break block @a[distance=..16] ~ ~ ~ 1 1.2', 'particle minecraft:ash ~ ~0.3 ~ 0.1 0.1 0.1 0 10',
        'execute as @e[type=minecraft:marker,tag=bm.hgate,distance=..4.6,sort=nearest,limit=1] at @s run function bm:p61/check'])
    fn('p61/pack', ['execute if entity @e[type=minecraft:interaction,tag=bm.hgs,tag=bm.hgfull,distance=..4.6] run return run ' +
                    title('@a[tag=bm.hgu]', 'actionbar', T('Take the Emblems out first.', 'gray')),
                    'loot give @a[tag=bm.hgu,limit=1] loot bm:items/hollow_gate',
                    'kill @e[type=minecraft:interaction,tag=bm.hgs,distance=..4.6]', 'kill @e[type=minecraft:item_display,tag=bm.hgd,distance=..0.2]',
                    'kill @e[type=minecraft:item_display,tag=bm.hgp,distance=..0.2]',
                    'playsound minecraft:block.deepslate.break block @a[distance=..24] ~ ~ ~ 1 0.6', 'particle minecraft:ash ~ ~2 ~ 1 1.5 0.3 0 40', 'kill @s'])

    # ================================================================== opening and closing (as the gate's marker)
    portal = disp('bm:hollow_portal', ['bm.hgp', 'bm.hgnew'], bright=15)
    fn('p61/check', ['execute store result score #hgn bm.rng if entity @e[type=minecraft:interaction,tag=bm.hgs,tag=bm.hgfull,distance=..4.6]',
                     'execute if score #hgn bm.rng matches 5 unless entity @s[tag=bm.hgon] run return run function bm:p61/open',
                     'execute unless score #hgn bm.rng matches 5 if entity @s[tag=bm.hgon] run function bm:p61/close'])
    fn('p61/open', ['tag @s add bm.hgon', f'summon minecraft:item_display ~ ~ ~ {snbt(portal)}',
                    'execute rotated as @s run tp @e[tag=bm.hgnew,distance=..0.5] ~ ~ ~ ~ 0', 'tag @e[tag=bm.hgnew,distance=..0.5] remove bm.hgnew',
                    'playsound minecraft:block.end_portal.spawn block @a[distance=..48] ~ ~ ~ 0.8 0.7',
                    'playsound minecraft:block.respawn_anchor.set_spawn block @a[distance=..32] ~ ~ ~ 1 0.5',
                    'particle minecraft:reverse_portal ^ ^2 ^ 0.7 1.3 0.7 0.2 120', 'particle minecraft:flash{color:[0.85,0.8,1.0,1.0]} ^ ^2 ^ 0 0 0 0 1',
                    'title @a[distance=..20] times 10 50 20', title('@a[distance=..20]', 'subtitle', T('Five seals, set in the order they were broken.', 'gray', italic=True)),
                    title('@a[distance=..20]', 'title', T('THE HOLLOW GATE OPENS', HG, bold=True))])
    fn('p61/close', ['tag @s remove bm.hgon', 'kill @e[type=minecraft:item_display,tag=bm.hgp,distance=..0.2]',
                     'playsound minecraft:block.beacon.deactivate block @a[distance=..32] ~ ~ ~ 1 0.5', 'particle minecraft:ash ^ ^2 ^ 0.7 1.3 0.3 0 40'])
    # while open: the dark of the Hollow drifts out of it, and it hums
    second.append('execute as @e[type=minecraft:marker,tag=bm.hgate,tag=bm.hgon] at @s if entity @a[distance=..32] run function bm:p61/hum')
    fn('p61/hum', ['particle minecraft:reverse_portal ^ ^1.9 ^ 0.6 1.1 0.15 0.02 12', 'particle minecraft:ash ^ ^1.9 ^0.4 0.6 1.1 0.3 0 6',
                   'particle minecraft:soul ^ ^0.4 ^0.3 0.5 0.1 0.2 0.01 1',
                   'scoreboard players add @s bm.hgt 1', 'execute if score @s bm.hgt matches 4.. run function bm:p61/hum_sound'])
    fn('p61/hum_sound', ['scoreboard players set @s bm.hgt 0', 'playsound minecraft:block.portal.ambient ambient @a[distance=..20] ~ ~2 ~ 0.35 0.6'])

    # ================================================================== passing through
    fast.append('execute as @e[type=minecraft:marker,tag=bm.hgate,tag=bm.hgon] at @s if entity @a[distance=..3] run function bm:p61/door')
    fn('p61/door', ['tag @s add bm.hgme'] +
       [f'execute positioned ^{x} ^0.4 ^ as @a[distance=..0.72,gamemode=!spectator] at @s run function bm:p61/pass' for x in (-0.6, 0, 0.6)] +
       ['tag @s remove bm.hgme'])
    fn('p61/pass', ['execute if score @s bm.hgcd matches 1.. run return 0', 'scoreboard players set @s bm.hgcd 30',
                    'execute unless score @s bm.conq matches 5.. run return run function bm:p61/bounce',
                    f'execute unless score #hver bm.p2 matches {HOLLOW_VER} run return run function bm:p61/bounce_wait',
                    # (step out in front first, so the way home lands you just outside the gate, not back in it)
                    'execute at @e[type=minecraft:marker,tag=bm.hgme,limit=1] run tp @s ^ ^ ^1.6', 'function bm:p2/hollow/enter'])
    fn('p61/bounce', ['execute at @e[type=minecraft:marker,tag=bm.hgme,limit=1] run tp @s ^ ^ ^1.5', 'effect give @s minecraft:slowness 2 2 true', 'particle minecraft:ash ~ ~1 ~ 0.3 0.6 0.3 0 20',
                      'playsound minecraft:entity.warden.sonic_boom player @s ~ ~ ~ 0.4 1.6',
                      say('The gate throws you back. Only those who have conquered all five may pass.', HG)])
    fn('p61/bounce_wait', ['execute at @e[type=minecraft:marker,tag=bm.hgme,limit=1] run tp @s ^ ^ ^1.5', say('The Throne beyond is still forming... try again in a moment.')])

    fn('admin/hollow_gate', [give('hollow_gate')])
    G.FUNCS['tick'] += tick
    s = G.FUNCS['loop/second']; s[-1:-1] = second
    f = G.FUNCS['loop/fast']; f[-1:-1] = fast


# ===================================================================== resource pack: the gate and its portal surface
GATE_DISP = {'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]},
             'gui': {'rotation': [20, 200, 0], 'translation': [0, 0.5, 0], 'scale': [0.34, 0.34, 0.34]},
             'ground': {'rotation': [0, 0, 0], 'translation': [0, 2, 0], 'scale': [0.2, 0.2, 0.2]},
             'thirdperson_righthand': {'rotation': [0, 180, 0], 'translation': [0, 2, 1], 'scale': [0.18, 0.18, 0.18]},
             'firstperson_righthand': {'rotation': [0, 200, 0], 'translation': [0, 2, 0], 'scale': [0.2, 0.2, 0.2]},
             'thirdperson_lefthand': {'rotation': [0, 180, 0], 'translation': [0, 2, 1], 'scale': [0.18, 0.18, 0.18]},
             'firstperson_lefthand': {'rotation': [0, 200, 0], 'translation': [0, 2, 0], 'scale': [0.2, 0.2, 0.2]}}


def textures():
    import math, random
    from PIL import Image
    rnd = random.Random(61)
    # the dark of the Hollow: a slow violet-grey swirl, 16 frames
    N = 16
    im = Image.new('RGBA', (16, 16 * N))
    for f in range(N):
        ph = f / N * 2 * math.pi
        for y in range(16):
            for x in range(16):
                dx, dy = x - 7.5, y - 7.5
                r = math.hypot(dx, dy); a = math.atan2(dy, dx)
                v = 0.5 + 0.5 * math.sin(a * 2 + r * 0.9 - ph * 2) * math.cos(r * 0.35 + ph)
                v = max(0, min(1, v * 0.85 + rnd.uniform(-0.06, 0.06)))
                c = (int(18 + 70 * v), int(14 + 50 * v), int(34 + 110 * v))
                if v > 0.86: c = (200, 196, 226)
                im.putpixel((x, y + 16 * f), c + (255,))
    return {'hg_portal': im}


def rp(R):
    import sys as _s
    R.TEXTURE_MODS.append(_s.modules[__name__])
    cube = R.cube
    def post(R2):
        def model(name, tex, els, disp):
            t = {k: (v if ':' in v else f'bm:block/{v}') for k, v in tex.items()}; t['particle'] = list(t.values())[0]
            R2.wj(f'assets/bm/models/item/{name}.json', {'textures': t, 'elements': els, 'display': disp})
            R2.wj(f'assets/bm/items/{name}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/{name}'}})
        R2.wj('assets/bm/textures/block/hg_portal.png.mcmeta', {'animation': {'frametime': 3, 'interpolate': True}})
        c = cube
        tex = {'s': 'minecraft:block/polished_deepslate', 't': 'minecraft:block/deepslate_tiles', 'k': 'minecraft:block/chiseled_deepslate',
               'b': 'minecraft:block/polished_blackstone', 'w': 'minecraft:block/calcite', 'o': 'minecraft:block/crying_obsidian',
               'r': 'minecraft:block/cracked_deepslate_tiles'}
        g = [c((-14, -14, 3), (30, -12, 13), 'b')]                                      # the plinth
        for x0, x1 in ((-12, -4), (20, 28)):                                            # the pillars, in courses
            for i, y in enumerate(range(-12, 22, 8)):
                g.append(c((x0, y, 4), (x1, min(y + 8, 22), 12), 't' if i % 2 else 'r' if (i == 1 and x0 > 0) else 's'))
            g.append(c((x0 - 1, 22, 3.5), (x1 + 1, 24, 12.5), 'w'))                     # capitals
            g.append(c((x0 - 1, -12, 3.5), (x1 + 1, -10.5, 12.5), 'w'))                 # bases
        g += [c((-13, 24, 4.5), (29, 30, 11.5), 's'), c((-13, 30, 4), (29, 31, 12), 'w'),  # lintel and its cornice
              c((-4, 19, 5), (0, 24, 11), 't'), c((16, 19, 5), (20, 24, 11), 't'),      # stepped inner corners
              c((-4, 16, 5.5), (-2, 19, 10.5), 't'), c((18, 16, 5.5), (20, 19, 10.5), 't'),
              c((3, 24, 3), (13, 32, 13), 'k')]                                         # the keystone
        for d, (xm, ym, zm) in SOCK_M.items():                                          # five sockets: a pale rim and a dark hollow
            g += [c((xm - 2.6, ym - 2.6, zm - 0.3), (xm + 2.6, ym + 2.6, zm + 0.2), 'w'), c((xm - 1.9, ym - 1.9, zm - 0.45), (xm + 1.9, ym + 1.9, zm), 'o')]
        model('hollow_gate', tex, g, GATE_DISP)
        # the portal surface: a thin pane filling the opening
        pane = c((-4, -12, 7.6), (20, 24, 8.4), 'p')
        for f in pane['faces'].values(): f['uv'] = [0, 0, 16, 16]
        model('hollow_portal', {'p': 'hg_portal'}, [pane], {'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]}})
    R.POST.append(post)

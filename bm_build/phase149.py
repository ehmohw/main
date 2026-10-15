"""Phase 149 (2.80): THE ROAMING BOSSES, STAGED - the six bosses whose relics have four forms (the Headless Horseman, the
Sand Pharaoh, the Storm Roc, the Elder Treant, the Magma Colossus, the Voidwalker) brought up to Apophiss's standard with
the staging kit (cine.py). Each:

- ARRIVES (5 s, frozen until it is done): the Horseman gallops in out of the dark along a trail of fire and pulls up in a
  ring of it; the Pharaoh rises out of a tightening sand vortex as the ground trembles, in a flare of sunlight; the Roc
  dives out of a gathering storm in a spiral and lands on a lightning strike; the Treant tears itself up out of the
  ground in three lurches, the roots cracking toward it first; the Colossus erupts out of a fissure of lava and slams
  down; the Voidwalker steps out of a rift that opens in the air - and the rift snaps shut behind it. Then its title
  card, and its song.
- RAGES as a moment (it freezes, roars, the ground answers) before its rage takes hold.
- WINDS UP its instant blows: the Colossus squats before the slam (a ring of fire marks the reach); the Pharaoh's sun-ray
  charges with an aiming line; his sandblast pulls the sand in first; his eruption cracks the ground in its reach; the
  Horseman's fire ring smoulders outward before it bursts; the Treant's roots and brambles crack and bud where they'll
  come; the Voidwalker's grasp drags the dark in toward it.
- DIES as a sequence (5 s): the Horseman's flaming head tumbles to the ground while he and his steed burn away; the
  Pharaoh sinks into the sand, light bleeding out of him; the Roc spirals down out of the sky and crashes in a lightning
  strike; the Treant withers and crumbles and a sapling takes root where it stood; the Colossus swells, cracks and
  explodes; the Voidwalker glitches, is dragged back into a rift, and a star falls where it stood. Then it is killed
  as by the player who brought it down: its loot, its title, its bounties and its advancements as before.

Importing does nothing; generate(G) runs after the bosses' phases and phase142 (it takes over their entrances)."""
import math
import cine as C
from cine import at as _at

A, D, R = 'bm.cat', 'bm.cdt', 'bm.crt'
a = lambda t, *c: _at(A, t, *c)
d = lambda t, *c: _at(D, t, *c)
r_ = lambda t, *c: _at(R, t, *c)
snd, stack, dark = C.snd, C.stack, C.dark
F96 = 'force @a[distance=..96]'

# kind: (entity, tag, summon fn, new-tag, sensed tag, song, name, colour, epithet, rage line, enrage fn, its own loops)
BOSS = {
    'hhm': ('wither_skeleton', 'bm.hhm', 'p42/boss/summon', 'bm.hh_new', 'bm.hhsensed', 'music_disc.13',
            'THE HEADLESS HORSEMAN', '#ff7a1a', 'he rides for your head', 'The Horseman rages!', 'p42/boss/enrage',
            ['p42/boss/second', 'p42/boss/fast']),
    'sph': ('husk', 'bm.sph', 'p53/sph/summon', 'bm.sph_new', 'bm.sphsensed', 'music_disc.relic',
            'THE SAND PHARAOH', '#e8c060', 'the tomb stirs', 'The sandstorm thickens!', 'p53/sph/enrage',
            ['p53/sph/second', 'p53/sph/fast']),
    'roc': ('phantom', 'bm.roc', 'p53/roc/summon', 'bm.roc_new', 'bm.rocsensed', 'music_disc.precipice',
            'THE STORM ROC', '#9ad8ff', 'the sky screams', 'The storm breaks!', 'p53/roc/enrage',
            ['p53/roc/second', 'p53/roc/fast']),
    'trt': ('creaking', 'bm.trt', 'p54/trt/summon', 'bm.trt_new', 'bm.trtsensed', 'music_disc.mellohi',
            'THE ELDER TREANT', '#7ac040', 'the forest remembers', 'The forest rises!', 'p54/trt/enrage',
            ['p54/trt/second', 'p54/trt/fast']),
    'mcol': ('magma_cube', 'bm.mcol', 'p54/mcol/summon', 'bm.mcol_new', 'bm.mcolsensed', 'music_disc.pigstep',
             'THE MAGMA COLOSSUS', '#ff5a1a', 'the earth bleeds fire', 'It boils over!', 'p54/mcol/enrage',
             ['p54/mcol/second', 'p54/mcol/fast']),
    'vwk': ('enderman', 'bm.vwk', 'p54/vwk/summon', 'bm.vwk_new', 'bm.vwksensed', 'music_disc.5',
            'THE VOIDWALKER', '#c070ff', 'between the stars, it waits', 'The stars go out!', 'p54/vwk/enrage',
            ['p54/vwk/second', 'p54/vwk/fast']),
}
# (markers a sequence leaves while it runs - cleared if their boss is gone)
MARKERS = {'hhm': ['bm.cdst_hhm'], 'sph': ['bm.cpos_sph', 'bm.cspot_sph'], 'roc': ['bm.cdst_roc', 'bm.cgnd_roc'], 'trt': ['bm.cspot_trt'],
           'mcol': ['bm.cspot_mcol'], 'vwk': ['bm.cdst_vwk', 'bm.cpos_vwk']}


def spot(k):
    """(start) the spot it will stand on, remembered - a mob grown while still in the ground is nudged about as it grows"""
    return [f'kill @e[type=minecraft:marker,tag=bm.cspot_{k}]', f'summon minecraft:marker ~ ~ ~ {{Tags:["bm.cspot_{k}"]}}']


def land(k, t):
    """(tick t) set exactly on its spot, facing as it was; the spot forgotten"""
    m = f'@e[type=minecraft:marker,tag=bm.cspot_{k},sort=nearest,limit=1]'
    return a(t, f'execute positioned as {m} run tp @s ~ ~ ~', f'kill {m}')


def q(axis, deg):
    """a quaternion [x,y,z,w] for a turn about an axis"""
    h = math.radians(deg) / 2
    s = math.sin(h)
    n = math.sqrt(sum(c * c for c in axis))
    return [axis[0] / n * s, axis[1] / n * s, axis[2] / n * s, math.cos(h)]


def qs(v):
    return '[' + ','.join(f'{c:.4f}f' for c in v) + ']'


def reveal(k, t):
    """its title card for all near, and its song for those who hadn't sensed it yet (the old 'presence' line is not shown)"""
    ent, tag, _s, _n, sensed, song, name, col, epithet, *_ = BOSS[k]
    return a(t, *C.title_card('@a[distance=..64]', name, col, epithet),
             f'execute as @a[distance=..64,tag=!{sensed},gamemode=!spectator] at @s run function bm:cine/{k}/heard')


def rage_card(k):
    col, line = BOSS[k][7], BOSS[k][9]
    return C.title_card('@a[distance=..48]', '', col, line, col, (4, 26, 10))


def generate(G):
    fn = G.fn
    C.install(G)

    # ================================================================== shared: a summon loses its instant fanfare; the
    # arrival begins instead. (phase142's entrance stays for Captain Tullius alone.)
    for k, (ent, tag, summon, new, sensed, song, name, col, epi, rage_line, enrage, loops) in BOSS.items():
        keep = []
        for l in G.FUNCS[summon]:
            if l.startswith(('particle ', 'playsound ', 'function bm:p142/', 'function bm:p53/bolt')):
                continue
            if l.startswith('execute as @a[') and l.endswith('/sense'):
                continue
            keep.append(l)
        rm = [i for i, l in enumerate(keep) if l.startswith('tag @e[') and l.endswith(f'remove {new}')]
        assert len(rm) == 1, (k, rm)
        keep.insert(rm[0], f'execute as @e[type=minecraft:{ent},tag={new}] at @s run function bm:cine/{k}/start')
        G.FUNCS[summon] = keep
        fn(f'cine/{k}/heard', [f'tag @s add {sensed}', 'stopsound @s music', 'stopsound @s record',
                               f'playsound minecraft:{song} record @s ~ ~ ~ 1 1 1'])
        C.gate(G, loops)
        # (its rage freezes it - the rest of that second's turn waits too)
        sec = G.FUNCS[loops[0]]
        ie = [i for i, l in enumerate(sec) if l.endswith(f'run function bm:{enrage}')]
        assert len(ie) == 1, (k, ie)
        sec.insert(ie[0] + 1, 'execute if entity @s[tag=bm.cfrz] run return 0')
        G.FUNCS[enrage].insert(0, 'function bm:cine/rage/start')
    for b in ('horseman', 'pharaoh', 'roc', 'treant', 'colossus', 'voidwalker'):
        G.FUNCS.pop(f'p142/{b}/start', None)
        G.FUNCS.pop(f'p142/{b}/tick', None)
        G.FUNCS['tick'] = [l for l in G.FUNCS['tick'] if f'bm:p142/{b}/tick' not in l]

    # every function of theirs that reads their health, without the buffer
    fams = ('p42/boss/', 'p53/sph/', 'p53/roc/', 'p54/trt/', 'p54/mcol/', 'p54/vwk/')
    nb, ns = C.debuffer(G, [n for n in G.FUNCS if n.startswith(fams)])
    assert nb == 6 and ns >= 7, (nb, ns)
    sec = G.FUNCS['loop/second']
    # (a boss already out when the pack updated is armed when seen; a sequence's markers go with their boss)
    sec += [f'execute as @e[type=minecraft:{v[0]},tag={v[1]},tag=!bm.carm,tag=!bm.cfrz] run function bm:cine/arm' for v in BOSS.values()]
    for k, tags in MARKERS.items():
        ent, tag = BOSS[k][:2]
        sec += [f'execute unless entity @e[type=minecraft:{ent},tag={tag}] run kill @e[type=minecraft:marker,tag={m}]' for m in tags]
    G.FUNCS['admin/uninstall'][0:0] = [f'kill @e[type=minecraft:marker,tag={m}]' for ms in MARKERS.values() for m in ms] + \
                                      ['kill @e[type=minecraft:item_display,tag=bm.chead]']

    horseman(G)
    pharaoh(G)
    roc(G)
    treant(G)
    colossus(G)
    voidwalker(G)
    windups(G)
    C.finish(G)


# ====================================================================== THE HEADLESS HORSEMAN
def horseman(G):
    """the rider is the boss; his Hellsteed is the vehicle and moves for both (a teleport would unseat him)"""
    fn = G.fn
    M = '@e[type=minecraft:marker,tag=bm.cdst_hhm,limit=1]'
    fn('cine/hhm/start', ['function bm:cine/arr/start', 'kill @e[type=minecraft:marker,tag=bm.cdst_hhm]',
                          'execute on vehicle at @s run summon minecraft:marker ~ ~ ~ {Tags:["bm.cdst_hhm","bm.cdnew"]}',
                          # (the spot faces away from whoever is nearest: he comes out of the dark from beyond it)
                          'execute as @e[type=minecraft:marker,tag=bm.cdnew] at @s facing entity @p[distance=..64,gamemode=!spectator] feet run tp @s ~ ~ ~ ~180 0',
                          'tag @e[type=minecraft:marker,tag=bm.cdnew] remove bm.cdnew',
                          # (a gallop under the open sky only - in a cave or a hall he rises out of the smoke where he is)
                          'execute on vehicle run tag @s add bm.cgal',
                          'execute on vehicle at @s positioned over motion_blocking_no_leaves unless entity @e[type=minecraft:marker,tag=bm.cdst_hhm,distance=..2.5] run tag @s remove bm.cgal',
                          f'execute on vehicle if entity @s[tag=bm.cgal] positioned as {M} rotated as {M} positioned ^ ^ ^22 positioned over motion_blocking_no_leaves run tp @s ~ ~ ~ ~180 0'])
    T0, T1 = 2, 50
    v = 1 / 0.85                                       # (a steady gallop, reined in over the last stretch)

    def far(k):
        f = v * k if k <= 0.7 else v * 0.7 + v * (k - 0.7) - v * (k - 0.7) ** 2 / 0.6
        return 22 * (1 - f)
    arr = [*a(1, dark(6, 64), snd('ambient.cave', 1.4, 0.5, 96), snd('entity.lightning_bolt.thunder', 0.5, 0.5, 96, 'weather')),
           *a(12, snd('entity.skeleton_horse.ambient', 1.0, 0.5, 96))]
    for t in range(T0, T1 + 1):
        dist = far((t - T0) / (T1 - T0))
        arr += a(t, f'execute on vehicle if entity @s[tag=bm.cgal] positioned as {M} rotated as {M} positioned ^ ^ ^{dist:.2f} '
                    'positioned over motion_blocking_no_leaves run tp @s ~ ~ ~ ~180 0')
    arr += a('2..56', f'execute on vehicle at @s run particle minecraft:flame ~ ~0.1 ~ 0.35 0.02 0.35 0.01 6 {F96}',
             f'execute on vehicle at @s run particle minecraft:soul_fire_flame ~ ~0.1 ~ 0.3 0.02 0.3 0.01 2 {F96}',
             f'execute on vehicle at @s run particle minecraft:large_smoke ~ ~0.6 ~ 0.3 0.3 0.3 0.01 2 {F96}')
    for j, t in enumerate(range(5, 50, 4)):            # hoofbeats, louder as he comes
        arr += a(t, f'execute on vehicle at @s run playsound minecraft:entity.horse.gallop hostile @a[distance=..96] ~ ~ ~ {0.5 + j * 0.12:.2f} 0.6')
    fire = lambda rr, n: [f'execute on vehicle at @s run {l}' for l in C.ring('minecraft:flame', rr, n, 0.1)]
    arr += [*a(52, *stack(('entity.horse.angry', 2, 0.5), ('entity.skeleton_horse.ambient', 2, 0.4), ('entity.blaze.shoot', 1.5, 0.5))),
            *a(52, *fire(2.6, 28)),
            *C.shake(A, 52, 8, 1.2),
            *a(58, *stack(('entity.witch.celebrate', 1.6, 0.5), ('entity.wither.ambient', 0.8, 0.6))),
            *a(58, f'execute anchored eyes positioned ^0.35 ^-0.6 ^0.3 run particle minecraft:flame ~ ~ ~ 0.15 0.15 0.15 0.06 30 {F96}'),
            *reveal('hhm', 60), *a(62, snd('block.fire.ambient', 2, 0.6))]
    for t in range(62, 82):                            # the fire ring runs out from him
        arr += a(t, *fire(2 + 7 * C.ease_out((t - 62) / 19), 30)[t % 2::2])
    arr += a(99, 'execute on vehicle run tag @s remove bm.cgal')

    # his death: the head tumbles from his hand; he and the steed burn away
    fall = q((0.36, 0.0, 0.93), 160)
    head = '@e[type=minecraft:item_display,tag=bm.chead,distance=..8]'
    die = [*d(1, 'bossbar set bm:hhm visible false', 'stopsound @a[tag=bm.hhsensed] record',
              *stack(('entity.wither.hurt', 2, 0.5), ('entity.skeleton_horse.death', 2, 0.5), ('entity.witch.hurt', 1.5, 0.4)),
              f'particle minecraft:flash{{color:[1.0,0.55,0.15,1.0]}} ~ ~1.5 ~ 0 0 0 0 1 {F96}'),
           *C.shake(D, 1, 8, 1.0),
           *d('2..80', f'particle minecraft:large_smoke ~ ~1.2 ~ 0.4 0.7 0.4 0.02 3 {F96}',
              f'particle minecraft:soul_fire_flame ~ ~1.0 ~ 0.35 0.6 0.35 0.02 2 {F96}'),
           *C.jitter(D, 6, 40, 0.06, vehicle=True),
           *d(30, snd('entity.horse.death', 1.5, 0.4)),
           # (the head: out of his hand and tumbling down)
           *d(40, 'item replace entity @s weapon.offhand with minecraft:air',
              'execute anchored eyes positioned ^0.35 ^-0.55 ^0.3 run summon minecraft:item_display ~ ~ ~ {Tags:["bm.chead","bm.chnew"],'
              'item:{id:"minecraft:jack_o_lantern",count:1},item_display:"fixed",brightness:{block:15,sky:15},'
              'transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.55f,0.55f,0.55f]}}',
              snd('entity.blaze.hurt', 1.5, 0.4)),
           *d(41, 'execute as @e[type=minecraft:item_display,tag=bm.chnew] run data merge entity @s {start_interpolation:0,interpolation_duration:18,'
              f'transformation:{{left_rotation:{qs(fall)},right_rotation:[0f,0f,0f,1f],translation:[0.9f,-1.75f,0.6f],scale:[0.55f,0.55f,0.55f]}}}}',
              'tag @e[type=minecraft:item_display,tag=bm.chnew] remove bm.chnew'),
           *d(59, snd('block.wood.fall', 1.6, 0.5), snd('block.fire.extinguish', 1.0, 0.6)),
           *d('60..88', f'execute as {head} at @s run particle minecraft:flame ~0.9 ~-1.5 ~0.6 0.1 0.1 0.1 0.01 1'),
           *C.scale_tween(D, 45, 82, 1.25, 0.15),
           *C.tween(D, 45, 82, lambda kk: f'execute on vehicle run attribute @s minecraft:scale base set {1.3 + (0.15 - 1.3) * C.ease(kk):.3f}'),
           *d(84, *stack(('entity.wither.death', 0.6, 0.6), ('block.fire.extinguish', 1.5, 0.5))),
           *d(84, f'particle minecraft:soul ~ ~0.8 ~ 0.6 0.6 0.6 0.03 40 {F96}'),
           *d(88, f'execute as {head} run data merge entity @s {{start_interpolation:0,interpolation_duration:8,'
              f'transformation:{{left_rotation:{qs(fall)},right_rotation:[0f,0f,0f,1f],translation:[0.9f,-1.75f,0.6f],scale:[0f,0f,0f]}}}}',
              f'execute as {head} at @s run particle minecraft:large_smoke ~0.9 ~-1.5 ~0.6 0.2 0.2 0.2 0.02 20'),
           *d(97, f'kill {head}', 'execute on vehicle run tag @s add bm.cgone', 'ride @s dismount',
              'execute as @e[type=minecraft:skeleton_horse,tag=bm.cgone] at @s run tp @s ~ -400 ~',
              'kill @e[type=minecraft:skeleton_horse,tag=bm.cgone]')]
    rage = [*r_(1, *stack(('entity.witch.celebrate', 2, 0.4), ('entity.blaze.shoot', 2, 0.4), ('entity.wither.shoot', 1.5, 0.5))),
            *r_(1, *rage_card('hhm')), *C.shake(R, 1, 10, 1.4),
            *r_('1..30', f'execute anchored eyes positioned ^0.35 ^-0.6 ^0.3 run particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.08 6 {F96}'),
            *r_(4, *fire(3.0, 30)), *r_(8, *[f'execute on vehicle at @s run {l}' for l in C.ring('minecraft:soul_fire_flame', 5.0, 40, 0.1)])]
    C.stage(G, 'hhm', 'wither_skeleton', 'bm.hhm', arr, die, rage)


# ====================================================================== THE SAND PHARAOH
def pharaoh(G):
    fn = G.fn
    DEEP = 4.5
    up = [(35, 85, DEEP, C.ease_out)]
    gr = lambda t: DEEP - C.offset(up, t - 1)          # the ground, from where he is at tick t
    fn('cine/sph/start', ['function bm:cine/arr/start', *spot('sph'), 'attribute @s minecraft:scale base set 1.0', f'tp @s ~ ~-{DEEP} ~'])
    arr = [*a(1, snd('entity.breeze.idle_air', 1.5, 0.5, 96), snd('ambient.cave', 1.0, 0.6, 96))]
    for t in range(1, 92):                             # the sand vortex: three arms, closing in and climbing
        rr = 4.2 - 2.6 * C.ease(t / 91)
        for arm in range(3):
            th = t * 0.32 + arm * 2 * math.pi / 3
            x, z = rr * math.cos(th), rr * math.sin(th)
            y = gr(t) + (t % 18) / 18 * 3.2
            arr += a(t, f'particle minecraft:falling_dust{{block_state:"minecraft:sand"}} ~{x:.2f} ~{y:.2f} ~{z:.2f} 0.15 0.15 0.15 0 2 {F96}')
            if t % 2 == 0:
                arr += a(t, f'particle minecraft:dust{{color:[0.86,0.75,0.5],scale:2.0}} ~{x:.2f} ~{max(gr(t), y - 0.6):.2f} ~{z:.2f} 0.2 0.2 0.2 0 1 {F96}')
    for t in range(10, 86, 10):
        arr += a(t, snd('block.sand.break', 1.6, 0.5), snd('entity.warden.dig', 0.5, 0.8))
    for t in range(35, 86):
        arr += a(t, f'particle minecraft:block{{block_state:"minecraft:sand"}} ~ ~{gr(t) + 0.1:.2f} ~ 1.0 0.1 1.0 0.1 6 {F96}')
    arr += [*C.shake(A, 30, 50, 0.5), *C.rise(A, *up[0]), *C.scale_tween(A, 35, 85, 1.0, 2.6),
            *a(86, f'particle minecraft:flash{{color:[1.0,0.85,0.45,1.0]}} ~ ~2 ~ 0 0 0 0 1 {F96}',
               f'particle minecraft:end_rod ~ ~2.5 ~ 0.4 1.2 0.4 0.25 80 {F96}',
               f'particle minecraft:dust_plume ~ ~1 ~ 2 0.6 2 0.08 80 {F96}',
               *stack(('block.beacon.activate', 2, 0.7), ('entity.husk.converted_to_zombie', 2, 0.5), ('entity.ravager.roar', 1.5, 0.6), ('item.trident.thunder', 0.6, 1.4))),
            *C.shake(A, 86, 10, 1.4), *reveal('sph', 88), *land('sph', 86)]
    # his death: shuddering, he sinks back into the sand, the light bleeding out of him
    down = [(20, 84, -4.0, C.ease)]
    sc = lambda t: 2.6 + (1.8 - 2.6) * C.ease((t - 20) / 64) if t >= 20 else 2.6
    P = '@e[type=minecraft:marker,tag=bm.cpos_sph,sort=nearest,limit=1]'
    die = [*d(1, 'bossbar set bm:sph visible false', 'stopsound @a[tag=bm.sphsensed] record',
              'summon minecraft:marker ~ ~ ~ {Tags:["bm.cpos_sph"]}',
              *stack(('entity.husk.death', 2, 0.5), ('entity.ravager.hurt', 1.5, 0.5), ('entity.wither.hurt', 1.0, 0.7)),
              f'particle minecraft:flash{{color:[1.0,0.85,0.45,1.0]}} ~ ~2 ~ 0 0 0 0 1 {F96}'),
           *C.shake(D, 1, 8, 1.0), *C.jitter(D, 5, 60, 0.12)]
    for t in range(2, 85):
        top = 1.95 * sc(t)
        g = -C.offset(down, t - 1)
        die += d(t, f'particle minecraft:falling_dust{{block_state:"minecraft:sand"}} ~ ~{top:.2f} ~ 0.6 0.3 0.6 0 5 {F96}',
                 f'particle minecraft:end_rod ~ ~{top * 0.55:.2f} ~ 0.5 0.8 0.5 0.06 1 {F96}')
        if t >= 20 and t % 2 == 0:
            die += d(t, f'particle minecraft:block{{block_state:"minecraft:sand"}} ~ ~{g + 0.1:.2f} ~ 1.0 0.1 1.0 0.1 6 {F96}')
    die += [*d(40, snd('block.sand.break', 2, 0.5), snd('item.brush.brushing.sand', 1.5, 0.5)),
            *d(60, snd('block.sand.break', 2, 0.45), snd('item.brush.brushing.sand', 1.5, 0.45)),
            *C.rise(D, *down[0]), *C.scale_tween(D, 20, 84, 2.6, 1.8),
            *d(86, f'execute at {P} run particle minecraft:flash{{color:[1.0,0.85,0.45,1.0]}} ~ ~0.5 ~ 0 0 0 0 1 {F96}',
               f'execute at {P} run particle minecraft:end_rod ~ ~0.5 ~ 0.3 0.3 0.3 0.4 90 {F96}',
               *stack(('block.beacon.deactivate', 2, 0.6), ('entity.husk.converted_to_zombie', 1, 0.4), ('block.sand.fall', 2, 0.5)))]
    for t in range(86, 97):
        rr = 1 + 5 * C.ease_out((t - 86) / 10)
        die += d(t, f'execute at {P} run particle minecraft:dust_plume ~ ~0.3 ~ {rr / 2:.2f} 0.1 {rr / 2:.2f} 0.05 12 {F96}')
    die += d(97, f'tp @s {P}', f'kill {P}')
    rage = [*r_(1, *stack(('entity.ravager.roar', 2, 0.5), ('block.beacon.power_select', 1.5, 0.6), ('entity.breeze.wind_burst', 1.5, 0.5))),
            *r_(1, *rage_card('sph')), *C.shake(R, 1, 10, 1.2),
            *r_('2..28', f'particle minecraft:dust_plume ~ ~1 ~ 2.5 0.6 2.5 0.06 10 {F96}',
                f'particle minecraft:falling_dust{{block_state:"minecraft:sand"}} ~ ~4 ~ 3 1 3 0 10 {F96}')]
    C.stage(G, 'sph', 'husk', 'bm.sph', arr, die, rage)


# ====================================================================== THE STORM ROC
def roc(G):
    fn = G.fn
    M = '@e[type=minecraft:marker,tag=bm.cdst_roc,limit=1]'
    GND = '@e[type=minecraft:marker,tag=bm.cgnd_roc,sort=nearest,limit=1]'
    F128 = 'force @a[distance=..128]'
    fn('cine/roc/start', ['function bm:cine/arr/start', 'kill @e[type=minecraft:marker,tag=bm.cdst_roc]',
                          'summon minecraft:marker ~ ~ ~ {Tags:["bm.cdst_roc"]}', 'tp @s ~14 ~36 ~'])
    pts = []
    for t in range(20, 71):                            # the dive: a spiral narrowing to the strike, faster as it falls
        k = (t - 20) / 50
        th = 1.6 * math.pi * k
        rr = 14 * (1 - C.ease(k))
        h = 36 * (1 - k ** 1.6)
        pts.append((t, rr * math.cos(th), h, rr * math.sin(th)))
    arr = [*a(1, snd('entity.lightning_bolt.thunder', 0.6, 0.5, 128, 'weather')),
           *a(8, snd('entity.lightning_bolt.thunder', 0.8, 0.6, 128, 'weather')),
           *a(16, snd('entity.lightning_bolt.thunder', 1.0, 0.7, 128, 'weather')),
           *a(20, snd('entity.phantom.swoop', 3, 0.5, 128), snd('item.elytra.flying', 1.2, 0.6, 96))]
    for t in range(1, 70, 2):                          # the storm gathers over the spot
        th = t * 0.18
        arr += a(t, *[f'execute at {M} run particle minecraft:cloud ~{9 * math.cos(th + j * math.pi / 2):.2f} ~26 ~{9 * math.sin(th + j * math.pi / 2):.2f} '
                      f'1.5 0.4 1.5 0.02 4 {F128}' for j in range(4)],
                 f'execute at {M} run particle minecraft:electric_spark ~ ~24 ~ 6 1 6 0.2 6 {F128}')
    for i, (t, x, h, z) in enumerate(pts):
        face = ''
        if i + 1 < len(pts):
            nx, nh, nz = pts[i + 1][1:]
            face = f' facing ~{nx:.2f} ~{nh:.2f} ~{nz:.2f}'
        arr += a(t, f'execute positioned as {M} run tp @s ~{x:.2f} ~{h:.2f} ~{z:.2f}{face}',
                 f'particle minecraft:cloud ~ ~1 ~ 0.8 0.3 0.8 0.02 3 {F128}',
                 f'particle minecraft:electric_spark ~ ~1 ~ 1 0.5 1 0.2 3 {F128}')
    arr += [*a(71, f'execute at {M} run function bm:p53/bolt',
               *stack(('entity.ender_dragon.growl', 2, 0.7), ('entity.phantom.ambient', 3, 0.4), ('item.trident.thunder', 1.0, 0.8))),
            *C.shake(A, 71, 12, 1.6), *reveal('roc', 72),
            *[l for t in range(72, 84) for l in a(t, *C.ring('minecraft:cloud', 1.5 + (t - 72) * 0.6, 20, 0.5, 0.05))],
            *a(99, 'kill @e[type=minecraft:marker,tag=bm.cdst_roc]')]
    # its death: struck, it spirals down out of the sky and crashes
    fn('cine/roc/drop', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.cgnd_roc","bm.cgnew"]}',
                         'execute as @e[type=minecraft:marker,tag=bm.cgnew] at @s positioned over motion_blocking_no_leaves run tp @s ~ ~ ~',
                         'tag @e[type=minecraft:marker,tag=bm.cgnew] remove bm.cgnew',
                         'execute store result score #ry bm.rng run data get entity @s Pos[1] 100',
                         f'execute store result score #gy bm.rng run data get entity {GND} Pos[1] 100',
                         'scoreboard players operation #ry bm.rng -= #gy bm.rng', 'scoreboard players set #c60 bm.rng 60',
                         'scoreboard players operation #ry bm.rng /= #c60 bm.rng',
                         'execute if score #ry bm.rng matches ..-1 run scoreboard players set #ry bm.rng 0',
                         'execute store result storage bm:cine roc.s float 0.01 run scoreboard players get #ry bm.rng'])
    fn('cine/roc/fall', ['execute at @s rotated ~ 0 run tp @s ^ ^ ^0.42 ~9 22', '$execute at @s run tp @s ~ ~-$(s) ~'])
    die = [*d(1, 'bossbar set bm:roc visible false', 'stopsound @a[tag=bm.rocsensed] record', 'function bm:p53/bolt', 'function bm:cine/roc/drop',
              *stack(('entity.phantom.death', 3, 0.4), ('entity.ender_dragon.hurt', 2, 0.7), ('entity.lightning_bolt.thunder', 2, 0.8))),
           *C.shake(D, 1, 8, 1.0),
           *d('4..64', 'function bm:cine/roc/fall with storage bm:cine roc',
              f'particle minecraft:electric_spark ~ ~1 ~ 1 0.6 1 0.3 4 {F128}',
              f'particle minecraft:item{{item:"minecraft:feather"}} ~ ~1 ~ 1.2 0.6 1.2 0.05 3 {F128}'),
           *[l for t in range(6, 64, 7) for l in d(t, snd('entity.phantom.flap', 2, 0.5, 96))],
           *d(10, snd('item.elytra.flying', 1.5, 0.5, 96)),
           *d(65, f'tp @s {GND}', f'execute at {GND} run function bm:p53/bolt',
              f'execute at {GND} run particle minecraft:explosion_emitter ~ ~1 ~ 0 0 0 0 1 {F128}',
              f'execute at {GND} run particle minecraft:item{{item:"minecraft:feather"}} ~ ~1.5 ~ 1.5 1 1.5 0.15 70 {F128}',
              *stack(('entity.generic.explode', 2, 0.6), ('block.anvil.land', 1, 0.5), ('entity.phantom.hurt', 2, 0.4))),
           *C.shake(D, 65, 14, 2.0),
           *C.jitter(D, 70, 92, 0.05, 11, 4),
           *d('66..95', f'particle minecraft:electric_spark ~ ~1 ~ 1.4 0.4 1.4 0.1 2 {F96}'),
           *d(97, 'kill @e[type=minecraft:marker,tag=bm.cgnd_roc]')]
    rage = [*r_(1, 'function bm:p53/bolt', *stack(('item.trident.thunder', 2, 0.6), ('entity.phantom.ambient', 3, 0.3), ('entity.lightning_bolt.thunder', 1.5, 0.7))),
            *r_(1, *rage_card('roc')), *C.shake(R, 1, 10, 1.2), *r_(12, 'function bm:p53/bolt'), *r_(22, 'function bm:p53/bolt'),
            *r_('2..30', f'particle minecraft:electric_spark ~ ~1 ~ 3 1.2 3 0.4 10 {F128}')]
    C.stage(G, 'roc', 'phantom', 'bm.roc', arr, die, rage)


# ====================================================================== THE ELDER TREANT
def treant(G):
    fn = G.fn
    DEEP = 6.5
    lurch = [(35, 49, 2.6, C.ease), (54, 66, 2.2, C.ease), (71, 84, 1.7, C.ease)]
    gr = lambda t: DEEP - C.offset(lurch, t - 1)
    fn('cine/trt/start', ['function bm:cine/arr/start', *spot('trt'), 'attribute @s minecraft:scale base set 1.4', f'tp @s ~ ~-{DEEP} ~'])
    arr = [*a(1, snd('entity.creaking.ambient', 1.5, 0.4, 96), snd('block.azalea_leaves.break', 2, 0.5, 96))]
    for t in range(1, 91, 2):
        arr += a(t, f'particle minecraft:block{{block_state:"minecraft:oak_leaves"}} ~ ~{gr(t) + 6:.2f} ~ 10 3 10 0 5 {F96}')
    for t in range(5, 36):                             # cracks run in toward the spot
        rr = 11 * (1 - (t - 5) / 30) + 0.8
        arr += a(t, *[f'particle minecraft:block{{block_state:"minecraft:rooted_dirt"}} ~{rr * math.cos(j * math.pi / 2 + 0.4):.2f} ~{gr(t) + 0.1:.2f} '
                      f'~{rr * math.sin(j * math.pi / 2 + 0.4):.2f} 0.2 0.05 0.2 0 4 {F96}' for j in range(4)])
        if t % 6 == 5:
            arr += a(t, snd('block.rooted_dirt.break', 1.5, 0.5))
    for i, (t0, t1, dy, cv) in enumerate(lurch):       # three lurches up out of the ground
        arr += C.rise(A, t0, t1, dy, cv)
        arr += a(t0, *stack(('block.rooted_dirt.break', 2, 0.5), ('block.wood.break', 1.6, 0.4 + 0.05 * i), ('entity.creaking.twitch', 1.2, 0.5)),
                 f'particle minecraft:block{{block_state:"minecraft:rooted_dirt"}} ~ ~{gr(t0) + 0.1:.2f} ~ 2 0.2 2 0.2 60 {F96}',
                 f'particle minecraft:block{{block_state:"minecraft:dirt"}} ~ ~{gr(t0) + 0.1:.2f} ~ 2 0.2 2 0.2 40 {F96}')
        arr += C.shake(A, t0, 6, 0.8 + 0.2 * i, seed=20 + i)
    arr += [*C.scale_tween(A, 35, 84, 1.4, 2.6),
            *a(86, *stack(('entity.creaking.activate', 2, 0.4), ('entity.warden.emerge', 1.2, 0.6), ('entity.ravager.roar', 1.2, 0.4)),
               f'particle minecraft:block{{block_state:"minecraft:oak_leaves"}} ~ ~4 ~ 2 2.5 2 0.1 160 {F96}'),
            *C.shake(A, 86, 10, 1.2), *reveal('trt', 88), *land('trt', 85)]
    die = [*d(1, 'bossbar set bm:trt visible false', 'stopsound @a[tag=bm.trtsensed] record',
              *stack(('entity.creaking.death', 2, 0.4), ('block.wood.break', 2, 0.4), ('entity.ravager.hurt', 1.0, 0.5))),
           *C.shake(D, 1, 8, 1.0),
           *d('2..84', f'particle minecraft:block{{block_state:"minecraft:oak_leaves"}} ~ ~5 ~ 1 0.6 1 0 4 {F96}',
              f'particle minecraft:block{{block_state:"minecraft:oak_log"}} ~ ~3 ~ 0.6 1.5 0.6 0 2 {F96}'),
           *[l for t in range(10, 70, 10) for l in d(t, snd('entity.creaking.twitch', 1.4, 0.5))],
           *C.scale_tween(D, 10, 70, 2.6, 1.5), *C.jitter(D, 10, 70, 0.06, 13),
           *d(72, snd('block.wood.break', 2, 0.4)), *d(76, snd('block.wood.break', 2, 0.35)), *d(80, snd('block.wood.break', 2, 0.3)),
           *d(72, f'particle minecraft:block{{block_state:"minecraft:oak_log"}} ~ ~1.5 ~ 1 1 1 0.2 80 {F96}'),
           *d(80, f'particle minecraft:block{{block_state:"minecraft:oak_leaves"}} ~ ~1.5 ~ 1.5 1 1.5 0.2 120 {F96}'),
           *C.shake(D, 72, 10, 1.4),
           # (where it fell, a sapling takes root - the forest remembers)
           *d(88, 'execute if block ~ ~-1 ~ #minecraft:supports_vegetation if block ~ ~ ~ #minecraft:air run setblock ~ ~ ~ minecraft:oak_sapling',
              snd('block.grass.place', 1.2, 0.8), f'particle minecraft:happy_villager ~ ~0.5 ~ 0.5 0.4 0.5 0 20 {F96}',
              f'particle minecraft:falling_spore_blossom ~ ~3 ~ 2 1 2 0 20 {F96}')]
    rage = [*r_(1, *stack(('entity.creaking.activate', 2, 0.3), ('entity.warden.roar', 0.8, 0.6), ('block.roots.break', 2, 0.4))),
            *r_(1, *rage_card('trt')), *C.shake(R, 1, 10, 1.2),
            *r_(4, *C.ring('minecraft:block{block_state:"minecraft:rooted_dirt"}', 4, 28, 0.1, 0.2, 0, 3)),
            *r_('2..28', f'particle minecraft:block{{block_state:"minecraft:oak_leaves"}} ~ ~4 ~ 2.5 2 2.5 0 6 {F96}')]
    C.stage(G, 'trt', 'creaking', 'bm.trt', arr, die, rage, die_len=95)


# ====================================================================== THE MAGMA COLOSSUS
def colossus(G):
    fn = G.fn
    DEEP = 7.0
    moves = [(45, 68, DEEP + 2.5, C.ease_out), (69, 78, -2.5, lambda kk: kk * kk)]
    gr = lambda t: DEEP - C.offset(moves, t - 1)
    fn('cine/mcol/start', ['function bm:cine/arr/start', *spot('mcol'), f'tp @s ~ ~-{DEEP} ~'])
    arr = [*a(1, snd('block.lava.ambient', 2, 0.5, 96), snd('ambient.basalt_deltas.mood', 1.5, 0.6, 96)),
           *a('1..44', f'particle minecraft:dripping_lava ~ ~{DEEP + 0.3} ~ 2.5 0.1 2.5 0 3 {F96}',
              f'particle minecraft:ash ~ ~{DEEP + 2} ~ 4 2 4 0 6 {F96}'),
           *[l for t in range(4, 44, 8) for l in a(t, snd('block.lava.pop', 1.6, 0.5))],
           *C.shake(A, 10, 34, 0.4),
           *a(42, *stack(('entity.generic.explode', 1.2, 0.4), ('block.basalt.break', 2, 0.5))),
           *a(42, f'particle minecraft:lava ~ ~{DEEP + 0.2} ~ 1.5 0.2 1.5 0 40 {F96}')]
    for t in range(44, 69):                            # the eruption: a fountain of fire from the fissure
        g = gr(t)
        arr += a(t, f'particle minecraft:lava ~ ~{g + 0.2:.2f} ~ 1 0.2 1 0 4 {F96}',
                 f'particle minecraft:flame ~ ~{g + 1.5:.2f} ~ 0.6 1.5 0.6 0.06 8 {F96}')
    arr += [*C.rise(A, *moves[0]), *C.rise(A, *moves[1]),
            *a(46, *stack(('entity.magma_cube.jump', 2, 0.3), ('entity.ravager.roar', 1.5, 0.4))),
            *a(79, f'particle minecraft:explosion_emitter ~ ~1 ~ 0 0 0 0 1 {F96}',
               f'particle minecraft:lava ~ ~1 ~ 3 0.5 3 0 60 {F96}',
               *stack(('entity.generic.explode', 2, 0.5), ('entity.magma_cube.squish', 2, 0.3), ('entity.ravager.roar', 1.5, 0.4), ('block.anvil.land', 1, 0.4))),
            *C.shake(A, 79, 14, 2.0), *reveal('mcol', 81), *land('mcol', 79)]
    for t in range(79, 92):
        arr += a(t, *C.ring('minecraft:flame', 2 + 7 * C.ease_out((t - 79) / 12), 32, 0.2)[t % 2::2])
    die = [*d(1, 'bossbar set bm:mcol visible false', 'stopsound @a[tag=bm.mcolsensed] record',
              *stack(('entity.magma_cube.hurt', 2, 0.3), ('entity.blaze.death', 1.5, 0.5), ('block.lava.extinguish', 2, 0.5))),
           *C.shake(D, 1, 8, 1.0),
           *d('2..75', f'particle minecraft:large_smoke ~ ~2.5 ~ 1.2 1 1.2 0.03 4 {F96}',
              f'particle minecraft:lava ~ ~2 ~ 1.8 1.2 1.8 0 1 {F96}',
              f'particle minecraft:flame ~ ~2 ~ 1.8 1.4 1.8 0.03 3 {F96}'),
           *[l for t in range(6, 74, 8) for l in d(t, snd('block.lava.extinguish', 1.4, 0.5 + t / 200))],
           *C.scale_tween(D, 20, 75, 1.0, 1.35, lambda kk: kk * kk), *C.jitter(D, 40, 75, 0.06, 17), *C.shake(D, 40, 34, 0.5, seed=5),
           *d(76, f'particle minecraft:explosion_emitter ~ ~1.5 ~ 1 0.5 1 0 2 {F96}',
              f'particle minecraft:lava ~ ~2 ~ 2.5 1.5 2.5 0 120 {F96}',
              f'particle minecraft:flame ~ ~2 ~ 1.5 1.5 1.5 0.3 120 {F96}',
              *stack(('entity.generic.explode', 3, 0.5), ('entity.dragon_fireball.explode', 2, 0.6), ('entity.magma_cube.death', 2, 0.3))),
           *C.shake(D, 76, 16, 2.4), *d(77, 'attribute @s minecraft:scale base set 1.0')]
    rage = [*r_(1, *stack(('entity.generic.explode', 1.6, 0.4), ('entity.magma_cube.squish', 2, 0.25), ('block.lava.pop', 2, 0.4))),
            *r_(1, *rage_card('mcol')), *C.shake(R, 1, 12, 1.6),
            *r_('2..28', *C.column('minecraft:lava', 5, 5, 0.6, 1), f'particle minecraft:flame ~ ~3 ~ 2 1.5 2 0.05 10 {F96}')]
    C.stage(G, 'mcol', 'magma_cube', 'bm.mcol', arr, die, rage, die_len=78)
    # (it still bursts into Magma Spawn - they come out of it as it was at the end: awake, visible, loud)
    G.FUNCS['p54/mcol/spawnling'] += ['effect clear @s minecraft:invisibility', 'data merge entity @s {NoAI:0b,Invulnerable:0b,Silent:0b}',
                                      'attribute @s minecraft:max_health modifier remove bm:cine_buf', 'tag @s remove bm.csil']


# ====================================================================== THE VOIDWALKER
def voidwalker(G):
    fn = G.fn
    M = '@e[type=minecraft:marker,tag=bm.cdst_vwk,limit=1]'
    P = '@e[type=minecraft:marker,tag=bm.cpos_vwk,sort=nearest,limit=1]'
    fn('cine/vwk/start', ['function bm:cine/arr/start', 'attribute @s minecraft:scale base set 0.05',
                          'kill @e[type=minecraft:marker,tag=bm.cdst_vwk]', 'summon minecraft:marker ~ ~ ~ {Tags:["bm.cdst_vwk"]}',
                          'execute facing entity @p[distance=..64,gamemode=!spectator] feet run tp @s ~ ~ ~ ~ 0',
                          'execute at @s rotated ~ 0 run tp @s ^ ^ ^-1.5'])

    def rift(w, part='minecraft:portal', n=18, at_dst=True):
        pre = f'execute positioned as {M} rotated as @s rotated ~ 0 run ' if at_dst else 'execute rotated ~ 0 run '
        out = []
        for kk in range(n):
            th = 2 * math.pi * kk / n
            x, y = w * math.cos(th), 2.1 + 2.0 * math.sin(th)
            out.append(f'{pre}particle {part} ^{x:.2f} ^{y:.2f} ^ 0.02 0.02 0.02 0 1 {F96}')
        return out
    arr = [*a(1, dark(6, 64), snd('ambient.cave', 1.5, 0.5, 96)), *a(20, snd('block.end_portal.spawn', 0.8, 0.5, 96))]
    for t in range(2, 36, 2):
        arr += a(t, *[f'execute at {M} run {l}' for l in C.converge('minecraft:reverse_portal', 12 - t / 4, 16, 2, 0.5)])
    for t in range(30, 88):
        w = 1.6 * C.ease_out(min(1.0, (t - 30) / 15))
        arr += a(t, *rift(w)[t % 2::2])
        if t % 3 == 0:
            arr += a(t, *rift(w * 0.8, 'minecraft:dragon_breath', 10))
    arr += [*a(32, snd('block.portal.trigger', 0.8, 0.6, 64), snd('entity.enderman.stare', 1.2, 0.5, 64)),
            *C.scale_tween(A, 45, 85, 0.05, 2.5), *C.tween(A, 45, 85, lambda kk: 'execute at @s rotated ~ 0 run tp @s ^ ^ ^0.037'),
            *a(60, snd('entity.enderman.stare', 1.5, 0.6, 64)),
            *a(86, *[f'execute at {M} run {l}' for l in C.converge('minecraft:reverse_portal', 3, 30, 2, 0.6)],
               f'particle minecraft:flash{{color:[0.65,0.3,0.95,1.0]}} ~ ~2 ~ 0 0 0 0 1 {F96}',
               *stack(('entity.enderman.scream', 2, 0.5), ('entity.warden.roar', 1, 0.7), ('entity.ender_dragon.growl', 1, 0.9))),
            *C.shake(A, 86, 10, 1.2), *reveal('vwk', 88), *a(99, 'kill @e[type=minecraft:marker,tag=bm.cdst_vwk]')]
    die = [*d(1, 'bossbar set bm:vwk visible false', 'stopsound @a[tag=bm.vwksensed] record', 'summon minecraft:marker ~ ~ ~ {Tags:["bm.cpos_vwk"]}',
              *stack(('entity.enderman.death', 2, 0.5), ('entity.warden.hurt', 1, 0.6), ('block.respawn_anchor.deplete', 1.5, 0.6))),
           *C.shake(D, 1, 8, 1.0), *C.jitter(D, 2, 44, 0.35, 19),
           *d('2..44', f'particle minecraft:portal ~ ~2 ~ 0.6 1.2 0.6 0.4 8 {F96}'),
           *[l for t in range(4, 44, 6) for l in d(t, snd('entity.enderman.teleport', 1.2, 0.5 + t / 100))],
           *[l for t in range(4, 44, 8) for l in d(t, 'attribute @s minecraft:scale base set 2.2') + d(t + 4, 'attribute @s minecraft:scale base set 2.5')],
           *C.scale_tween(D, 45, 78, 2.5, 0.05, lambda kk: kk * kk),
           *C.tween(D, 45, 78, lambda kk: 'execute at @s run tp @s ~ ~ ~ ~18 ~')]
    for t in range(40, 80):
        die += d(t, *rift(1.4, 'minecraft:portal', 16, at_dst=False)[t % 2::2])
    die += [*d(79, *C.converge('minecraft:reverse_portal', 4, 32, 2, 0.7),
               f'particle minecraft:flash{{color:[0.65,0.3,0.95,1.0]}} ~ ~2 ~ 0 0 0 0 1 {F96}',
               *stack(('entity.generic.explode', 1.5, 1.4), ('block.end_portal.spawn', 1.0, 1.2))),
            *C.shake(D, 79, 10, 1.5)]
    for t in range(82, 95):                            # a star falls where it stood
        h = 15 * (1 - (t - 82) / 12)
        die += d(t, f'execute at {P} run particle minecraft:end_rod ~ ~{h:.1f} ~ 0.05 0.3 0.05 0 6 {F96}')
    die += [*d(95, f'execute at {P} run particle minecraft:end_rod ~ ~0.3 ~ 0.4 0.2 0.4 0.08 30 {F96}',
               snd('entity.firework_rocket.twinkle', 1.5, 0.8)),
            *d(97, 'attribute @s minecraft:scale base set 2.5', f'tp @s {P}', f'kill {P}')]
    rage = [*r_(1, dark(3, 48), *stack(('entity.enderman.scream', 2, 0.4), ('entity.warden.sonic_charge', 1, 0.6), ('block.end_portal.spawn', 0.6, 0.8))),
            *r_(1, *rage_card('vwk')), *C.shake(R, 1, 10, 1.2), *r_(2, *C.converge('minecraft:reverse_portal', 8, 30, 2, 0.6)),
            *r_('2..30', f'particle minecraft:portal ~ ~2.5 ~ 1 1.5 1 0.6 12 {F96}')]
    C.stage(G, 'vwk', 'enderman', 'bm.vwk', arr, die, rage)


# ====================================================================== WIND-UPS: the instant blows, telegraphed
def windups(G):
    fn = G.fn
    each = lambda ticks, mk: [f'execute if score @s bm.cwu matches {t} run {l}' for t in range(ticks) for l in mk(t)]
    pulse = lambda part, rr, n: C.ring(part, rr, n, 0.15, 0.05)
    wu = {}
    # the Horseman's fire ring: embers spread out from under the steed (or him, if he's lost it) to the ring's reach
    for rr in (3, 5, 7):
        fn(f'cine/wu/hhr{rr}', C.ring('minecraft:small_flame', rr, 12 + 3 * rr, 0.15) + C.ring('minecraft:flame', rr - 0.5, 6 + rr, 0.1)[::2])
    vis = ['scoreboard players set #wm bm.rng 0', 'execute on vehicle run scoreboard players set #wm bm.rng 1']
    for lo, hi, rr in ((11, 15, 3), (6, 10, 5), (0, 5, 7)):
        vis += [f'execute if score @s bm.cwu matches {lo}..{hi} if score #wm bm.rng matches 1 on vehicle at @s run function bm:cine/wu/hhr{rr}',
                f'execute if score @s bm.cwu matches {lo}..{hi} if score #wm bm.rng matches 0 run function bm:cine/wu/hhr{rr}']
    vis += ['execute if score @s bm.cwu matches 8 run ' + snd('entity.blaze.ambient', 1.5, 0.5),
            f'execute anchored eyes positioned ^0.35 ^-0.6 ^0.3 run particle minecraft:flame ~ ~ ~ 0.1 0.1 0.1 0.03 3 {F96}']
    wu['p42/boss/ring'] = C.windup(G, 'hhm', 'p42/boss/ring', 16, vis, [snd('block.fire.ambient', 2, 0.5), snd('entity.ghast.warn', 0.8, 0.5)])
    # the Pharaoh: the sand pulled in (sandblind, reach 14); the ground cracking (eruption, 10); the sun gathering (sun-ray)
    wu['p53/sph/sandblind'] = C.windup(G, 'sph', 'p53/sph/sandblind', 16,
        each(16, lambda t: C.ring('minecraft:dust{color:[0.86,0.75,0.5],scale:1.8}', 3 + 11 * t / 15, 24, 1.0)),
        [snd('entity.breeze.charge', 1.5, 0.5), snd('item.brush.brushing.sand', 1.2, 0.6)])
    wu['p53/sph/eruption'] = C.windup(G, 'sph', 'p53/sph/eruption', 18,
        each(18, lambda t: pulse('minecraft:dust{color:[0.95,0.75,0.35],scale:1.6}', 10, 40) if t % 2 == 0 else []) +
        [f'particle minecraft:block{{block_state:"minecraft:sand"}} ~ ~0.1 ~ 5 0 5 0 6 {F96}'],
        [snd('block.sand.break', 2, 0.5), snd('entity.warden.dig', 0.8, 0.7)])
    fn('cine/wu/aim', [f'particle minecraft:dust{{color:[1.0,0.82,0.3],scale:0.7}} ^ ^ ^{1.5 * i:.1f} 0 0 0 0 1 force @a[distance=..64]' for i in range(1, 13)])
    wu['p53/sph/sunray'] = C.windup(G, 'sph', 'p53/sph/sunray', 16,
        [f'execute anchored eyes positioned ^ ^ ^0.4 run particle minecraft:end_rod ~ ~ ~ 0.5 0.5 0.5 0 2 {F96}',
         f'execute anchored eyes positioned ^ ^ ^0.4 run particle minecraft:dust{{color:[1.0,0.85,0.4],scale:1.2}} ~ ~ ~ 0.3 0.3 0.3 0 3 {F96}',
         'execute anchored eyes positioned ^ ^ ^0.6 facing entity @p[distance=..20,gamemode=!creative,gamemode=!spectator] eyes run function bm:cine/wu/aim'],
        [snd('block.beacon.ambient', 2, 1.4), snd('block.beacon.power_select', 1, 1.8)])
    # the Treant: the ground cracks where the roots will come (12) and buds where the brambles will (9)
    wu['p54/trt/roots'] = C.windup(G, 'trt', 'p54/trt/roots', 16,
        each(16, lambda t: pulse('minecraft:dust{color:[0.35,0.6,0.2],scale:1.5}', 12, 44) if t % 2 == 0 else []) +
        [f'particle minecraft:block{{block_state:"minecraft:rooted_dirt"}} ~ ~0.1 ~ 6 0 6 0 6 {F96}'],
        [snd('block.rooted_dirt.break', 2, 0.5), snd('entity.creaking.twitch', 1, 0.6)])
    wu['p54/trt/brambles'] = C.windup(G, 'trt', 'p54/trt/brambles', 16,
        each(16, lambda t: pulse('minecraft:dust{color:[0.6,0.12,0.15],scale:1.4}', 9, 36) if t % 2 == 0 else []) +
        each(16, lambda t: C.ring('minecraft:block{block_state:"minecraft:sweet_berry_bush"}', 6, 20, 0.2) if t in (12, 6) else []),
        [snd('block.sweet_berry_bush.place', 2, 0.6)])
    # the Colossus squats (and a ring of fire marks the slam's reach, 9) - put back if it's cut short
    wu['p54/mcol/slam'] = C.windup(G, 'mcol', 'p54/mcol/slam', 18,
        each(18, lambda t: pulse('minecraft:dust{color:[1.0,0.35,0.1],scale:1.8}', 9, 44) if t % 2 == 0 else []) +
        each(18, lambda t: C.ring('minecraft:flame', 4.5, 20, 0.15) if t % 3 == 0 else []) +
        ['execute if score @s bm.cwu matches 12 run attribute @s minecraft:scale base set 0.8',
         'execute if score @s bm.cwu matches 6 run attribute @s minecraft:scale base set 0.74'],
        ['attribute @s minecraft:scale base set 0.88', snd('entity.magma_cube.squish', 2, 0.4), snd('block.lava.ambient', 2, 0.6)],
        ['attribute @s minecraft:scale base set 1.0'])
    G.FUNCS['p54/mcol/slam'].insert(0, 'attribute @s minecraft:scale base set 1.0')
    # the Voidwalker's grasp: the dark dragged in toward it from the grasp's reach (16)
    wu['p54/vwk/grasp'] = C.windup(G, 'vwk', 'p54/vwk/grasp', 16,
        each(16, lambda t: C.ring('minecraft:reverse_portal', 3 + 13 * t / 15, 24, 1.2)),
        [snd('entity.warden.sonic_charge', 1, 0.5)])
    for atk, target in wu.items():
        fam = atk.rsplit('/', 1)[0] + '/'
        n = C.hook_calls(G, [nm for nm in G.FUNCS if nm.startswith(fam) and nm.endswith('second')], atk, target)
        assert n >= 1, (atk, n)

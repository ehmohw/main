"""3.0e: THE MIRES' SHARED RUNTIME - the rig, the rise, the fight (grab, stab, and for those that have it the spit), the recoil
from whatever repels them, the sink, the melt into goop, and the bound guard planted from a heart: everything phase246 (the
Dread Mire) and phase258 (the Brood-Mire, the Vorn's) do alike, each with its own art module, tags, numbers, sounds and colours.

A Mire is an invisible husk host (NoAI, rooted) carrying item displays - one per part of its art's rig (mire_art / xmire_art, the
same rig: the Brood-Mire's has three eyestalks more). Its state is bm.ms (0 dormant, 1 rising, 2 risen, 3 grabbing, 4 stabbing,
5 recoiling, 6 sinking, 7 melting, 8 spitting), bm.mt the ticks in it, bm.ma the ticks since its last blow, bm.mq its patience,
bm.mid the number its parts share (one counter, #mid bm.mid, for every Mire of every kind). The objectives, the constants #4 /
#20 / #40 and the predicates are the caller's (phase246 makes them; phase258 uses them).

Cfg (a class, attributes; Dread's values in phase246.CFG):
  P            the functions' prefix ('p246')                    A        the art module
  NAME, COL    its name and colour                                HP, FLOOR  its health, and the floor under it (it dies at FLOOR)
  HOST         the host's tag ('bm.mire')                         R        every part's tag ('bm.mr'; a part's own: R + '_' + part)
  NEWP, NEWH   new parts' / new host's tags                       GRAB     the grabbed's tag    GOOPT, GNEW  the goop's tags
  MELT, TAME   melting / bound tags                               FELL     the score that ends them ('#dfell bm.cfg')
  CROSS        the predicate-function that repels it ('bm:p181/in_cross')     FLEE_FROM  the selector it slips away from
  LIGHT_EXEMPT the tag that keeps it from melting in bright light; None: light never melts it
  WAKE_FOES    who wakes it / it creeps towards (selector arguments)          FOES  who it fights
  DUST, DRIP_DUST, STAB_DUST  dust colours ('r,g,b')   INK  its spray particle   DRIP_BLOCK  falling_dust's block
  SMOKE        its smoke particle   RECOIL_FX  the recoil's flash   GOOP  the goop's model   BUBBLE, POP  the sprites (phase257)
  LOOT         the loot table its death drops   SPIT  (dict or None) the spit   LIVE  the states its health is watched in
  snd(name, v, p, who)  its voice"""
from items import T
from nbt import snbt, B, F, Int, D as Dd
import rigfol as RF


def runtime(G, C):
    fn, title = G.fn, G.title
    tick, second = G.FUNCS['tick'], G.FUNCS['loop/second']
    P, A, SCALE = C.P, C.A, C.SCALE
    ME = '@e[type=minecraft:husk,tag=bm.mme,limit=1]'
    FOES, WFOES = C.FOES, C.WAKE_FOES
    snd = C.snd
    sel = lambda p: f'@e[type=minecraft:item_display,tag=bm.msel,tag={C.R}_{p}]'
    at = lambda t, cmd: f'execute if score @s bm.mt matches {t} {cmd[8:]}' if cmd.startswith('execute ') else f'execute if score @s bm.mt matches {t} run {cmd}'
    GLOW = tuple(getattr(A, 'GLOW', ()))

    # ================================================================== the rig
    for name, pz in A.POSES.items():
        fn(f'{P}/pose/{name}', RF.pose(A, pz, SCALE, C.DUR.get(name, 8), sel))
    fn(f'{P}/place', RF.place(A, SCALE / 16, sel))
    fn(f'{P}/stash', RF.pose(A, A.POSES['dormant'], SCALE, 1, sel, hide=False) +
       [f'execute as {sel(p)} run data merge entity @s {{transformation:{{scale:[0f,0f,0f]}}}}' for p in A.PARTS if p != 'puddle'])
    rig = []
    for p in A.PARTS:
        extra = dict(view_range=F(4.0))
        if p in GLOW: extra['brightness'] = {'block': Int(15), 'sky': Int(15)}
        rig.append(f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, [C.R, f"{C.R}_{p}", C.NEWP], SCALE, model=A.model_id(p), extra=extra, scale0=p != "puddle")}')
    fn(f'{P}/rig', rig)
    fn(f'{P}/mine', ['scoreboard players operation #me bm.mid = @s bm.mid',
                     f'execute as @e[type=minecraft:item_display,tag={C.R}] if score @s bm.mid = #me bm.mid run tag @s add bm.msel'])

    # ================================================================== the host, and a Mire made at a place
    host = {'Tags': [C.HOST, 'bm.seen', C.NEWH], 'NoAI': B(1), 'Silent': B(1), 'PersistenceRequired': B(0), 'Invulnerable': B(1),
            'CustomName': T(C.NAME, C.COL), 'DeathLootTable': 'minecraft:empty', 'CanPickUpLoot': B(0),
            'attributes': [{'id': 'minecraft:max_health', 'base': Dd(C.HP + C.FLOOR)}, {'id': 'minecraft:scale', 'base': Dd(C.DORMANT_SC)},
                           {'id': 'minecraft:knockback_resistance', 'base': Dd(1.0)}, {'id': 'minecraft:armor', 'base': Dd(C.ARMOR)}],
            'Health': F(C.HP + C.FLOOR),
            'active_effects': [{'id': 'minecraft:invisibility', 'duration': Int(-1), 'amplifier': B(0), 'show_particles': B(0)},
                               {'id': 'minecraft:fire_resistance', 'duration': Int(-1), 'amplifier': B(0), 'show_particles': B(0)}]}
    C.host = host
    fn(f'{P}/spawn', [f'summon minecraft:husk ~ ~ ~ {snbt(host)}',
                      'scoreboard players add #mid bm.mid 1',
                      f'execute as @e[type=minecraft:husk,tag={C.NEWH},distance=..1] at @s run function bm:{P}/spawn1'])
    fn(f'{P}/spawn1', ['scoreboard players operation @s bm.mid = #mid bm.mid', 'scoreboard players set @s bm.ms 0', 'scoreboard players set @s bm.mt 0',
                       'execute store result entity @s Rotation[0] float 1 run random value 0..359',
                       f'execute at @s rotated as @s rotated ~ 0 run function bm:{P}/rig',
                       f'scoreboard players operation @e[type=minecraft:item_display,tag={C.NEWP},distance=..1] bm.mid = @s bm.mid',
                       f'tag @e[type=minecraft:item_display,tag={C.NEWP},distance=..1] remove {C.NEWP}',
                       f'function bm:{P}/mine', f'execute at @s rotated as @s rotated ~ 0 run function bm:{P}/place', f'function bm:{P}/stash', f'function bm:{P}/pose/dormant',
                       'tag @e[type=minecraft:item_display,tag=bm.msel] remove bm.msel', f'tag @s remove {C.NEWH}'])


def watch(G, C):
    """each second (the puddle's patience, what repels it, the light, its master's fall) and each tick (awake)"""
    fn = G.fn
    tick, second = G.FUNCS['tick'], G.FUNCS['loop/second']
    P = C.P
    FOES, WFOES = C.FOES, C.WAKE_FOES
    snd = C.snd
    second.append(f'execute as @e[type=minecraft:husk,tag={C.HOST}] at @s run function bm:{P}/sec')
    fn(f'{P}/sec', [f'execute if entity @s[tag={C.TAME}] run return run function bm:{P}/t/sec',
                    f'execute if score {C.FELL} matches 1 unless score @s bm.ms matches 7 run return run function bm:{P}/melt'] + list(getattr(C, 'SEC_EXTRA', [])) +
       [f'execute if score @s bm.ms matches 0 run function bm:{P}/sec0',
        f'execute if score @s bm.ms matches 2 run function bm:{P}/sec2'])
    sec0 = ([f'execute if predicate bm:p246/bright unless entity @s[tag={C.LIGHT_EXEMPT}] run return run function bm:{P}/melt'] if C.LIGHT_EXEMPT else []) + \
           [f'execute if function {C.CROSS} run return run function bm:{P}/flee',
            f'execute if entity @a[distance=..{C.WAKE},{WFOES}] run return run function bm:{P}/rise0',
            f'execute facing entity @p[distance=..{C.CREEP},{WFOES}] feet rotated ~ 0 positioned ^ ^ ^0.35 unless block ~ ~-1 ~ #minecraft:replaceable '
            'if block ~ ~ ~ #minecraft:replaceable run tp @s ~ ~ ~',
            'execute store result score #r bm.rng run random value 0..3', 'execute if score #r bm.rng matches 0 run ' + snd('bubble', 0.7),
            f'particle minecraft:dust{{color:[{C.DUST}],scale:1.3}} ~ ~0.1 ~ 1.4 0.02 1.4 0 10',
            f'particle {C.SMOKE} ~ ~0.1 ~ 1.2 0.02 1.2 0 4']
    fn(f'{P}/sec0', sec0)
    fn(f'{P}/sec2', [f'execute if function {C.CROSS} run return run function bm:{P}/recoil0',
                     f'execute if entity @a[distance=..{C.LEAVE},{FOES}] run scoreboard players set @s bm.mq 0',
                     f'execute unless entity @a[distance=..{C.LEAVE},{FOES}] run scoreboard players add @s bm.mq 1',
                     f'execute if score @s bm.mq matches 10.. run function bm:{P}/sink0',
                     'execute store result score #r bm.rng run random value 0..4', 'execute if score #r bm.rng matches 0 run ' + snd('idle', 1.2)])
    fn(f'{P}/flee', [f'execute facing entity {C.FLEE_FROM} feet rotated ~ 0 positioned ^ ^ ^-0.8 '
                     'unless block ~ ~-1 ~ #minecraft:replaceable if block ~ ~ ~ #minecraft:replaceable run tp @s ~ ~ ~',
                     f'particle {C.SMOKE} ~ ~0.2 ~ 1 0.1 1 0.01 12'])
    fn(f'{P}/melt', [f'particle {C.SMOKE} ~ ~0.3 ~ 1.4 0.2 1.4 0.02 40', f'particle {C.INK} ~ ~0.3 ~ 1.2 0.2 1.2 0.05 20', snd('death', 0.6, 1.4),
                     'scoreboard players operation #me bm.mid = @s bm.mid', f'execute as @e[type=minecraft:item_display,tag={C.R}] if score @s bm.mid = #me bm.mid run kill @s'] +
       list(getattr(C, 'MELT_EXTRA', [])) + ['tp @s ~ -400 ~', 'kill @s'])

    # ================================================================== each tick, each one awake
    tick.append(f'execute as @e[type=minecraft:husk,tag={C.HOST},scores={{bm.ms=1..}}] at @s run function bm:{P}/tick')
    live = []
    for rng in C.LIVE:
        live += [f'execute if score @s bm.ms matches {rng} store result score #h bm.rng run data get entity @s Health',
                 f'execute if score @s bm.ms matches {rng} if score #h bm.rng matches ..{C.FLOOR} run function bm:{P}/die0']
    spit = C.SPIT is not None
    fn(f'{P}/tick', ['scoreboard players add @s bm.mt 1', 'tag @s add bm.mme', f'function bm:{P}/mine'] + live +
       [f'execute if score @s bm.ms matches 1 run function bm:{P}/s/rise',
        f'execute if score @s bm.ms matches 2 unless entity @s[tag={C.TAME}] run function bm:{P}/s/fight',
        f'execute if score @s bm.ms matches 3 unless entity @s[tag={C.TAME}] run function bm:{P}/s/grab',
        f'execute if score @s bm.ms matches 4 unless entity @s[tag={C.TAME}] run function bm:{P}/s/stab',
        f'execute if score @s bm.ms matches 2 if entity @s[tag={C.TAME}] run function bm:{P}/t/fight',
        f'execute if score @s bm.ms matches 3 if entity @s[tag={C.TAME}] run function bm:{P}/t/grab',
        f'execute if score @s bm.ms matches 4 if entity @s[tag={C.TAME}] run function bm:{P}/t/stab',
        f'execute if score @s bm.ms matches 5 run function bm:{P}/s/recoil',
        f'execute if score @s bm.ms matches 6 run function bm:{P}/s/sink',
        f'execute if score @s bm.ms matches 7 run function bm:{P}/s/die'] +
       ([f'execute if score @s bm.ms matches 8 run function bm:{P}/s/spit'] if spit else []) +
       [f'execute if score @s bm.ms matches 2..5 run function bm:{P}/drip'] +
       ([f'execute if score @s bm.ms matches 8 run function bm:{P}/drip'] if spit else []) +
       list(getattr(C, 'TICK_EXTRA', [])) +
       [f'execute rotated as @s rotated ~ 0 run function bm:{P}/place',
        'tag @e[type=minecraft:item_display,tag=bm.msel] remove bm.msel', 'tag @s remove bm.mme'])
    fn(f'{P}/drip', ['scoreboard players operation #f bm.rng = @s bm.mt', 'scoreboard players operation #f bm.rng %= #4 bm.rng',
                     f'execute if score #f bm.rng matches 0 run particle minecraft:falling_dust{{block_state:"{C.DRIP_BLOCK}"}} ~ ~3.2 ~ 0.7 1.2 0.7 0 3',
                     f'execute if score #f bm.rng matches 2 run particle {C.INK} ~ ~2.6 ~ 0.6 1 0.6 0.02 1',
                     f'execute if score #f bm.rng matches 0 run particle minecraft:dust{{color:[{C.DRIP_DUST}],scale:1.1}} ~ ~0.2 ~ 1.3 0.05 1.3 0 3'])


def fight(G, C):
    """rising, the risen fight (grab, stab, the spit), the recoil, the sink"""
    fn, title = G.fn, G.title
    P = C.P
    FOES = C.FOES
    snd = C.snd
    ME = '@e[type=minecraft:husk,tag=bm.mme,limit=1]'
    at = lambda t, cmd: f'execute if score @s bm.mt matches {t} {cmd[8:]}' if cmd.startswith('execute ') else f'execute if score @s bm.mt matches {t} run {cmd}'
    face = f'execute facing entity @p[distance=..16,{FOES}] feet run tp @s ~ ~ ~ ~ 0'
    C.face = face
    # ---- rising
    fn(f'{P}/rise0', ['scoreboard players set @s bm.ms 1', 'scoreboard players set @s bm.mt 0', 'scoreboard players set @s bm.mq 0', face])
    fn(f'{P}/s/rise', [at(1, f'function bm:{P}/pose/rise_0'), at(1, snd('rise', 1.4)), at(1, f'particle {C.INK} ~ ~0.4 ~ 1.2 0.2 1.2 0.08 30'),
                       at(12, f'function bm:{P}/pose/rise_1'),
                       at(24, f'function bm:{P}/pose/shriek'), at(24, snd('shriek', 1.0, 0.7)), at(32, f'function bm:{P}/pose/rise_2'),
                       at(24, f'attribute @s minecraft:scale base set {C.RISEN_SC}'), at(24, f'execute unless entity @s[tag={C.TAME}] run data merge entity @s {{Invulnerable:0b}}'),
                       at(40, 'scoreboard players set @s bm.ms 2'), at(40, 'scoreboard players set @s bm.ma 30'), at(40, 'scoreboard players set @s bm.mt 0')] +
       list(getattr(C, 'RISE_EXTRA', [])))
    # ---- risen: swaying, facing its prey; every EVERY ticks a grab or a stab (or, at range, a spit)
    spit = C.SPIT
    fn(f'{P}/s/fight', ['scoreboard players add @s bm.ma 1',
                        'scoreboard players operation #f bm.rng = @s bm.mt', 'scoreboard players operation #f bm.rng %= #20 bm.rng',
                        'scoreboard players operation #g bm.rng = @s bm.mt', 'scoreboard players operation #g bm.rng %= #40 bm.rng',
                        f'execute if score #g bm.rng matches 0 run function bm:{P}/pose/idle_a', f'execute if score #g bm.rng matches 20 run function bm:{P}/pose/idle_b',
                        f'execute if score #f bm.rng matches 0 if entity @p[distance=..16,{FOES}] run {face}',
                        f'execute if score @s bm.ma matches {C.EVERY}.. if entity @a[distance=..4.5,{FOES}] run return run function bm:{P}/stab0',
                        f'execute if score @s bm.ma matches {C.EVERY}.. if entity @a[distance=3.5..8,{FOES}] run return run function bm:{P}/grab0'] +
       ([f'execute if score @s bm.ma matches {C.EVERY}.. if entity @a[distance=8..{spit["reach"]},{FOES}] run return run function bm:{P}/spit0'] if spit else []) +
       list(getattr(C, 'FIGHT_EXTRA', [])))
    fn(f'{P}/grab0', ['scoreboard players set @s bm.ms 3', 'scoreboard players set @s bm.mt 0', face, f'function bm:{P}/pose/grab_0', snd('lash', 1.4)])
    fn(f'{P}/s/grab', [at(4, f'execute positioned ^ ^1.4 ^4 as @p[distance=..3.5,{FOES}] run tag @s add {C.GRAB}'),
                       at(4, f'execute positioned ^ ^1.4 ^4 run particle {C.INK} ~ ~ ~ 0.6 0.4 0.6 0.1 20'),
                       at(5, f'execute as @a[tag={C.GRAB}] run {title("@s", "actionbar", T("A tentacle has you!", C.COL, bold=True))}'),
                       at(5, f'effect give @a[tag={C.GRAB}] minecraft:slowness 2 4 true'),
                       at(10, f'function bm:{P}/pose/grab_1'),
                       f'execute if score @s bm.mt matches 6..30 as @a[tag={C.GRAB},distance=2.6..] at @s facing entity {ME} feet positioned ^ ^ ^0.3 run tp @s ~ ~ ~',
                       f'execute if score @s bm.mt matches 6..30 as @a[tag={C.GRAB}] at @s run particle minecraft:falling_dust{{block_state:"{C.DRIP_BLOCK}"}} ~ ~1 ~ 0.3 0.5 0.3 0 2',
                       at(30, f'execute as @a[tag={C.GRAB}] run damage @s {C.GRAB_DMG} minecraft:mob_attack by {ME}'),
                       at(30, snd('lash', 1.0, 0.6)), at(31, f'tag @a remove {C.GRAB}'),
                       at(40, 'scoreboard players set @s bm.ms 2'), at(40, 'scoreboard players set @s bm.ma 0'), at(40, 'scoreboard players set @s bm.mt 0')])
    fn(f'{P}/stab0', ['scoreboard players set @s bm.ms 4', 'scoreboard players set @s bm.mt 0', face, f'function bm:{P}/pose/stab_0', snd('idle', 1.4, 0.6)])
    fn(f'{P}/s/stab', [at(14, f'function bm:{P}/pose/stab_1'), at(15, snd('lash', 1.6, 0.8)),
                       at(17, f'execute positioned ^ ^ ^3.5 as @a[distance=..2.4,{FOES}] run damage @s {C.STAB_DMG} minecraft:mob_attack by {ME}'),
                       at(17, f'execute positioned ^ ^ ^3.5 run particle {C.INK} ~ ~0.3 ~ 0.8 0.2 0.8 0.1 30'),
                       at(17, f'execute positioned ^ ^ ^3.5 run particle minecraft:dust{{color:[{C.STAB_DUST}],scale:1.6}} ~ ~0.3 ~ 1 0.1 1 0 20'),
                       at(32, 'scoreboard players set @s bm.ms 2'), at(32, 'scoreboard players set @s bm.ma 0'), at(32, 'scoreboard players set @s bm.mt 0')])
    # ---- what repels it: a shriek, a recoil, down it goes
    fn(f'{P}/recoil0', ['scoreboard players set @s bm.ms 5', 'scoreboard players set @s bm.mt 0', f'function bm:{P}/pose/recoil', snd('shriek', 1.6),
                        f'tag @a remove {C.GRAB}', f'particle {C.RECOIL_FX} ~ ~3 ~ 1 1.5 1 0.05 20'])
    fn(f'{P}/s/recoil', [at(20, f'function bm:{P}/sink0')])
    fn(f'{P}/sink0', ['scoreboard players set @s bm.ms 6', 'scoreboard players set @s bm.mt 0', f'function bm:{P}/pose/sink_0', snd('rise', 1.0, 1.3)])
    fn(f'{P}/s/sink', [at(12, f'function bm:{P}/pose/dormant'), at(12, f'attribute @s minecraft:scale base set {C.DORMANT_SC}'),
                       at(12, 'data merge entity @s {Invulnerable:1b}'),
                       at(24, 'scoreboard players set @s bm.ms 0'), at(24, 'scoreboard players set @s bm.mq 0'), at(24, 'scoreboard players set @s bm.mt 0')])


def death(G, C):
    """(3.0d) IT MELTS - the risen mass sags and squashes, its tentacles droop and sink; it slumps into a bubbling pile of goop that
    bubbles a few seconds, then shrinks into the ground and is gone; its drops are left where it was. Invulnerable all the while
    (ms 7: no blow); every part and the goop share its bm.mid, so its melt (the sweeps, what repels it, its master's fall) takes
    them all at once, whenever it comes"""
    fn = G.fn
    P, A, SCALE = C.P, C.A, C.SCALE
    snd = C.snd
    sel = lambda p: f'@e[type=minecraft:item_display,tag=bm.msel,tag={C.R}_{p}]'
    at = lambda t, cmd: f'execute if score @s bm.mt matches {t} {cmd[8:]}' if cmd.startswith('execute ') else f'execute if score @s bm.mt matches {t} run {cmd}'
    fn(f'{P}/die0', ['scoreboard players set @s bm.ms 7', 'scoreboard players set @s bm.mt 0', 'data merge entity @s {Invulnerable:1b}', f'tag @s add {C.MELT}',
                     f'tag @a remove {C.GRAB}', f'function bm:{P}/pose/death_0', snd('death', 1.6), snd('shriek', 1.0, 0.5)] + list(getattr(C, 'DIE0_EXTRA', [])))
    import phase257 as DFX
    import rigkit as RK
    U = SCALE / 16
    XF = RK.solve(A.PIVOT, A.PARENT, A.POSES['death_1'])

    def squash(p, dy, kx, ky, dur):
        q, t = XF[p]; sc = SCALE * getattr(A, 'PART_K', {}).get(p, 1.0)
        return (f'execute as {sel(p)} run data merge entity @s[type=minecraft:item_display] {{start_interpolation:0,interpolation_duration:{dur},transformation:{{translation:'
                f'[{t[0] * U:.3f}f,{t[1] * U + dy:.3f}f,{t[2] * U:.3f}f],scale:[{sc * kx:.3f}f,{sc * ky:.3f}f,{sc * kx:.3f}f]}}}}')
    TENTS = tuple(p for p in A.PARTS if p[0] == 't' and p[1].isdigit())
    BODY = tuple(p for p in A.PARTS if p != 'puddle' and p not in TENTS)
    goop = {'Tags': [C.R, C.GOOPT, C.GNEW], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': C.GOOP}},
            'item_display': 'fixed', 'brightness': {'block': Int(11), 'sky': Int(11)}, 'view_range': F(3.0), 'teleport_duration': Int(1),
            'transformation': {'left_rotation': RF.IDENT, 'right_rotation': RF.IDENT, 'translation': [F(0), F(0.02), F(0)], 'scale': [F(0)] * 3}}
    gsel = f'@e[type=minecraft:item_display,tag={C.GOOPT},tag=bm.msel]'
    fn(f'{P}/goop', ['summon minecraft:item_display ~ ~ ~ ' + snbt(goop), f'scoreboard players operation @e[type=minecraft:item_display,tag={C.GNEW},distance=..1] bm.mid = @s bm.mid',
                     f'execute as @e[type=minecraft:item_display,tag={C.GNEW},distance=..1] store result entity @s Rotation[0] float 1 run random value 0..359',
                     f'tag @e[type=minecraft:item_display,tag={C.GNEW},distance=..1] remove {C.GNEW}'])
    die = [at(15, f'function bm:{P}/pose/death_1'), at(15, f'particle {C.INK} ~ ~1 ~ 1.4 0.6 1.4 0.1 60'),
           *[at(34, squash(p, -0.4, 1.15, 0.7, 20)) for p in BODY], *[at(34, squash(p, -0.3, 1.05, 0.6, 20)) for p in TENTS],
           at(34, snd('death', 0.9, 0.7)), at(34, 'playsound minecraft:block.honey_block.slide hostile @a[distance=..24] ~ ~ ~ 1.5 0.5'),
           at(40, f'function bm:{P}/goop'),
           at(42, f'execute as {gsel} run data merge entity @s[type=minecraft:item_display] {{start_interpolation:0,interpolation_duration:30,transformation:{{scale:[2.2f,2.2f,2.2f]}}}}'),
           *[at(56, squash(p, -1.0, 1.35, 0.3, 18)) for p in BODY], *[at(56, squash(p, -0.6, 1.1, 0.25, 18)) for p in TENTS],
           at(56, 'playsound minecraft:block.mud.break hostile @a[distance=..24] ~ ~ ~ 1.5 0.5'), at(56, 'playsound minecraft:block.honey_block.slide hostile @a[distance=..24] ~ ~ ~ 1.5 0.4'),
           *[at(74, f'execute as {sel(p)} run data merge entity @s[type=minecraft:item_display] {{start_interpolation:0,interpolation_duration:12,transformation:{{scale:[0f,0f,0f]}}}}') for p in BODY + TENTS],
           at('20..74', f'particle minecraft:falling_dust{{block_state:"{C.DRIP_BLOCK}"}} ~ ~1.6 ~ 0.9 0.8 0.9 0 2'),
           *[at(t, 'execute positioned ~ ~0.55 ~ run ' + DFX.spr(C.BUBBLE, 1.0, 1.5)) for t in range(46, 104, 3)],
           *[at(t, 'execute positioned ~ ~0.7 ~ run ' + DFX.spr(C.BUBBLE, 1.4, 0.7)) for t in range(50, 100, 7)],
           *[at(t, 'playsound minecraft:block.bubble_column.upwards_ambient hostile @a[distance=..24] ~ ~ ~ 0.8 0.6') for t in range(48, 104, 12)],
           at('44..104', f'particle minecraft:dust{{color:[{C.DUST}],scale:1.1}} ~ ~0.5 ~ 1.2 0.1 1.2 0 1'),
           at(102, f'execute as {gsel} run data merge entity @s[type=minecraft:item_display] {{start_interpolation:0,interpolation_duration:26,transformation:{{translation:[0f,-0.25f,0f],scale:[0f,0f,0f]}}}}'),
           at(102, f'execute as {sel("puddle")} run data merge entity @s[type=minecraft:item_display] {{start_interpolation:0,interpolation_duration:26,transformation:{{scale:[0f,0f,0f]}}}}'),
           at(102, snd('death', 0.6, 1.3)), at(102, f'particle {C.SMOKE} ~ ~0.3 ~ 1.4 0.1 1.4 0.01 30'),
           at(C.DIE_END - 2, f'particle {C.SMOKE} ~ ~0.3 ~ 0.8 0.1 0.8 0.02 20'),
           at(C.DIE_END - 2, f'loot spawn ~ ~0.5 ~ loot {C.LOOT}'), at(C.DIE_END - 2, 'summon minecraft:experience_orb ~ ~0.5 ~ {Value:30}'),
           at(C.DIE_END, 'execute as @e[type=minecraft:item_display,tag=bm.msel] run kill @s'), at(C.DIE_END, 'tp @s ~ -400 ~'), at(C.DIE_END, 'kill @s')]
    fn(f'{P}/s/die', die)


def bound(G, C, K):
    """THE BOUND ONE: a heart (K.ITEM) sneak + used on the top of a block plants a Mire of your own - stationary; it rises for any
    monster within WAKE and fights it as a wild one fights you - never you, never anyone; it can't be hurt; creepers won't come
    within 10 of it (shoved back, fuses out). Sneak + punch its puddle to take it back up.
    K: ITEM, TK (the interaction's tag), TAME_NAME, MON (the monsters it fights: selector arguments), DAY_SINK (by day in the
    Overworld it stays a puddle), refuse (lines refusing a place, first), msgs (use, place, planted, vault)"""
    fn, title, give = G.fn, G.title, G.give
    P = C.P
    snd = C.snd
    ME = '@e[type=minecraft:husk,tag=bm.mme,limit=1]'
    at = lambda t, cmd: f'execute if score @s bm.mt matches {t} {cmd[8:]}' if cmd.startswith('execute ') else f'execute if score @s bm.mt matches {t} run {cmd}'
    MON = K.MON
    mon = lambda r: f'@e[{MON},distance=..{r}]'
    fn(f'{P}/heart/use', ['execute unless predicate bm:p20/sneaking run return run ' + title('@s', 'actionbar', T(K.msg_use, 'gray')),
                          'execute if dimension bm:gutter run return run ' + title('@s', 'actionbar', T('Not in the vault.', 'gray'))] + list(K.refuse) +
       ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
        'scoreboard players set #placed bm.rng 0', 'scoreboard players set #ray bm.rng 25', 'tag @s add bm.placer',
        f'execute anchored eyes positioned ^ ^ ^ run function bm:{P}/heart/ray', 'tag @s remove bm.placer',
        'execute if score #placed bm.rng matches 0 run return run ' + title('@s', 'actionbar', T('Look at the top of a block within 5 blocks.', 'gray')),
        f'execute unless entity @s[gamemode=creative] if items entity @s weapon.mainhand *[minecraft:custom_data~{{bm:"{K.ITEM}"}}] run return run item modify entity @s weapon.mainhand bm:p241/take_one',
        f'execute unless entity @s[gamemode=creative] if items entity @s weapon.offhand *[minecraft:custom_data~{{bm:"{K.ITEM}"}}] run item modify entity @s weapon.offhand bm:p241/take_one'])
    fn(f'{P}/heart/ray', [f'execute unless block ~ ~ ~ #minecraft:replaceable run return run function bm:{P}/heart/hit',
                          'scoreboard players remove #ray bm.rng 1', f'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:{P}/heart/ray'])
    fn(f'{P}/heart/hit', ['execute align xyz positioned ~0.5 ~1 ~0.5 unless block ~ ~ ~ #minecraft:replaceable run return 0',
                          'execute align xyz positioned ~0.5 ~1 ~0.5 if entity @e[type=minecraft:interaction,tag=bm.gvdeco,distance=..2] run return 0',
                          f'execute align xyz positioned ~0.5 ~1 ~0.5 run function bm:{P}/heart/plant', 'scoreboard players set #placed bm.rng 1'])
    fn(f'{P}/heart/plant', [f'function bm:{P}/spawn',
                            f'execute as @e[type=minecraft:husk,tag={C.HOST},distance=..1,limit=1,sort=nearest] run function bm:{P}/heart/bind',
                            'summon minecraft:interaction ~ ~ ~ ' + snbt({'Tags': [K.TK, 'bm.gvdeco', K.TK + 'new'], 'width': F(2.4), 'height': F(0.4), 'response': B(1)}),
                            f'scoreboard players operation @e[type=minecraft:interaction,tag={K.TK}new,distance=..1] bm.pid = @a[tag=bm.placer,limit=1] bm.pid',
                            f'tag @e[type=minecraft:interaction,tag={K.TK}new] remove {K.TK}new',
                            snd('rise', 0.8, 1.4), f'particle {C.INK} ~ ~0.3 ~ 1.2 0.2 1.2 0.05 30',
                            title('@a[tag=bm.placer]', 'actionbar', [T(K.msg_planted, C.COL, bold=True), T('It will rise for any monster that comes near. (Sneak + punch it: take it back.)', 'gray')])])
    fn(f'{P}/heart/bind', [f'tag @s add {C.TAME}', 'data merge entity @s {PersistenceRequired:1b,Invulnerable:1b}',
                           'scoreboard players operation @s bm.pid = @a[tag=bm.placer,limit=1] bm.pid',
                           'data modify entity @s CustomName set value ' + snbt(T(K.TAME_NAME, C.COL))])
    fn(f'{P}/heart/take', [give(K.ITEM),
                           f'execute as @e[type=minecraft:husk,tag={C.TAME},distance=..1.5,limit=1,sort=nearest] at @s run function bm:{P}/heart/gone',
                           'kill @e[type=minecraft:interaction,tag=bm.gvdme,limit=1]'])
    fn(f'{P}/heart/gone', ['scoreboard players operation #me bm.mid = @s bm.mid', f'execute as @e[type=minecraft:item_display,tag={C.R}] if score @s bm.mid = #me bm.mid run kill @s',
                           f'particle {C.INK} ~ ~0.3 ~ 1 0.2 1 0.05 20', snd('death', 0.5, 1.6), 'tp @s ~ -400 ~', 'kill @s'])
    G.FUNCS['p71/deco/pick'][0:0] = [f'execute if entity @e[type=minecraft:interaction,tag=bm.gvdme,tag={K.TK}] at @e[type=minecraft:interaction,tag=bm.gvdme,limit=1] '
                                     f'run function bm:{P}/heart/take']
    tface = f'execute facing entity @e[{MON},distance=..16,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0'
    day = (['execute if score @s bm.ms matches 2 if dimension minecraft:overworld if predicate bm:p246/day run return run function bm:p246/sink0'.replace('p246', P),
            'execute if score @s bm.ms matches 0 if dimension minecraft:overworld if predicate bm:p246/day run return 0'] if K.DAY_SINK else [])
    fn(f'{P}/t/sec', [f'execute as @e[type=minecraft:creeper,distance=..10] at @s run function bm:{P}/t/shoo'] + day +
       [f'execute if score @s bm.ms matches 0 if entity {mon(C.WAKE)} run return run function bm:{P}/t/rise0',
        f'execute if score @s bm.ms matches 2 if entity {mon(16)} run scoreboard players set @s bm.mq 0',
        f'execute if score @s bm.ms matches 2 unless entity {mon(16)} run scoreboard players add @s bm.mq 1',
        f'execute if score @s bm.ms matches 2 if score @s bm.mq matches 6.. run function bm:{P}/sink0',
        f'execute if score @s bm.ms matches 0 run particle minecraft:dust{{color:[{C.DUST}],scale:1.3}} ~ ~0.1 ~ 1.4 0.02 1.4 0 6'])
    fn(f'{P}/t/shoo', ['data merge entity @s[type=minecraft:creeper] {Fuse:30s}', f'execute facing entity @e[type=minecraft:husk,tag={C.TAME},sort=nearest,limit=1] feet rotated ~ 0 '
                       'positioned ^ ^ ^-1.5 if block ~ ~ ~ #minecraft:replaceable if block ~ ~1 ~ #minecraft:replaceable run tp @s ~ ~ ~',
                       f'particle {C.SMOKE} ~ ~1 ~ 0.3 0.4 0.3 0.02 6'])
    fn(f'{P}/t/rise0', ['scoreboard players set @s bm.ms 1', 'scoreboard players set @s bm.mt 0', 'scoreboard players set @s bm.mq 0', tface])
    fn(f'{P}/t/fight', ['scoreboard players add @s bm.ma 1',
                        'scoreboard players operation #g bm.rng = @s bm.mt', 'scoreboard players operation #g bm.rng %= #40 bm.rng',
                        f'execute if score #g bm.rng matches 0 run function bm:{P}/pose/idle_a', f'execute if score #g bm.rng matches 20 run function bm:{P}/pose/idle_b',
                        f'execute if score #g bm.rng matches 0 run {tface}', f'execute if score #g bm.rng matches 20 run {tface}',
                        f'execute if score @s bm.ma matches 30.. if entity {mon(4.5)} run return run function bm:{P}/t/stab0',
                        f'execute if score @s bm.ma matches 30.. if entity @e[{MON},distance=3.5..8] run return run function bm:{P}/t/grab0'] + list(getattr(K, 'FIGHT_EXTRA', [])))
    fn(f'{P}/t/grab0', ['scoreboard players set @s bm.ms 3', 'scoreboard players set @s bm.mt 0', tface, f'function bm:{P}/pose/grab_0', snd('lash', 1.2)])
    fn(f'{P}/t/grab', [at(4, f'execute positioned ^ ^1.4 ^4 as @e[{MON},distance=..3.5,sort=nearest,limit=2] run tag @s add {C.GRAB}'),
                       at(10, f'function bm:{P}/pose/grab_1'),
                       f'execute if score @s bm.mt matches 6..30 as @e[tag={C.GRAB},type=!minecraft:player,distance=2.6..] at @s facing entity {ME} feet positioned ^ ^ ^0.3 run tp @s ~ ~ ~',
                       at(30, f'execute as @e[tag={C.GRAB},type=!minecraft:player] run damage @s {C.GRAB_DMG + 4} minecraft:mob_attack by {ME}'),
                       at(30, snd('lash', 0.8, 0.6)), at(31, f'tag @e[tag={C.GRAB},type=!minecraft:player] remove {C.GRAB}'),
                       at(40, 'scoreboard players set @s bm.ms 2'), at(40, 'scoreboard players set @s bm.ma 0'), at(40, 'scoreboard players set @s bm.mt 0')])
    fn(f'{P}/t/stab0', ['scoreboard players set @s bm.ms 4', 'scoreboard players set @s bm.mt 0', tface, f'function bm:{P}/pose/stab_0'])
    fn(f'{P}/t/stab', [at(14, f'function bm:{P}/pose/stab_1'), at(15, snd('lash', 1.2, 0.8)),
                       at(17, f'execute positioned ^ ^ ^3.5 as @e[{MON},distance=..2.4] run damage @s {C.STAB_DMG + 4} minecraft:mob_attack by {ME}'),
                       at(17, f'execute positioned ^ ^ ^3.5 run particle {C.INK} ~ ~0.3 ~ 0.8 0.2 0.8 0.1 30'),
                       at(32, 'scoreboard players set @s bm.ms 2'), at(32, 'scoreboard players set @s bm.ma 0'), at(32, 'scoreboard players set @s bm.mt 0')])

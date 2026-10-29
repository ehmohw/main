"""2.99a: THE STATUE KNIGHTS - dark knights of stone that guard the final dungeons' puzzle rooms (knight_art draws them).

WHERE      the Undercrown: two DREAD SENTINELS flanking the Throne Gate (trial 16, its last puzzle before the Sovereign's
           throne). The Vorn Armada: two VORN SENTINELS posed at either end of the
           Command Lock (17). The builders place a marker for each (DBuild.knight: bm.kstat, bm.kn<n>, bm.knk_<kind>, its
           yaw); within 48 blocks of a player it raises the statue - the knight's own rig in stone, in its sentinel pose.
THE WAKING solve the room's puzzle and its statues come to life (p2/logic: a trial in its dungeon's CFG['guard'] calls
           p245/wake/<d><n> on its solve INSTEAD of opening its gate): the stone cracks, the eyes light, it hefts its mace -
           and the room's door stays shut until every knight in it has fallen (then pz<n>_open runs, as a plain solve would).
THE FIGHT  an invisible husk carries the rig (bm.khost, bm.kg_<d><n>); its health over FLOOR is the knight's. It stalks you
           (walking with its mace on its shoulder), and every ~2.5 s it attacks, by turns:
  SLAM     the mace raised overhead (a long wind-up - step back), then driven into the floor 2 blocks ahead: a heavy blow
           there, a lighter shockwave round it.
  SPIN     the mace held out at arm's length and swung round and round as it drifts after you - every 0.4 s it strikes
           anyone within reach. Then it REELS, dizzy: its guard is down (no Resistance) - strike now.
THE FALL   down on one knee, slumped over its haft, and it turns back to stone where it knelt. Everyone near is granted ITS
           STATUE (knight_statue_<kind>): sneak + use on a block to set it up in your base; sneak + punch it to take it back.
           The fallen stone stays until the trial resets (its pz<n>_reset - the dungeon's idle reset, a rebuild): then the
           knight stands on its plinth again, a statue, waiting."""
from items import T, item, TOTEM
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D as Dd
import rigfol as RF
import knight_art as A

PFX = 'p245'
FLOOR = 100                          # (the host's health over this is the knight's)
HOSTSC = 1.5                         # (a husk 1.95 tall: ~2.9 blocks, the rig's height)
SCALE = getattr(A, 'SCALE', 1.0)
RESIST = 0                           # (Resistance I while its guard is up)
KN = {'dread': dict(name='Dread Sentinel', col='#c8323c', hp=240, slam=14, wave=6, spin=7, dust='0.85,0.08,0.12',
                    stone='minecraft:polished_blackstone', item="Dread Sentinel's Statue",
                    lore='A knight of the Undercrown, turned back to stone.'),
      'vorn': dict(name='Vorn Sentinel', col='#7aff6a', hp=200, slam=12, wave=5, spin=6, dust='0.4,1.0,0.35',
                   stone='minecraft:smooth_stone', item="Vorn Sentinel's Statue",
                   lore='A sentinel of the Armada, its hive-light gone out.')}
DUR = {'statue': 0, 'wake_0': 10, 'wake_1': 10, 'idle_a': 10, 'idle_b': 10, 'walk_0': 5, 'walk_1': 5, 'walk_2': 5, 'walk_3': 5,
       'swing_0': 8, 'swing_1': 3, 'spin_0': 5, 'spin_1': 5, 'stagger': 6, 'death_0': 10, 'death_1': 15}
WIND, HIT, BACK = 16, 19, 40         # the slam: wind-up .. the blow .. back to the fight (ticks)
SPIN0, SPIN1, REEL = 10, 70, 40      # the spin: from .. to (ticks); then reeling this long
EVERY = 50                           # (ticks between attacks)
ME = '@e[type=minecraft:husk,tag=bm.kme,limit=1]'
sel = lambda p: f'@e[type=minecraft:item_display,tag=bm.ksel,tag=bm.kr_{p}]'
FOES = 'gamemode=!spectator,gamemode=!creative'


def groups():
    """every guarded trial: (d, n, kind)"""
    import p2.undercfg as U
    import p2.armadacfg as AC
    return [(cfg_d, n, k) for cfg_d, cfg in ((U.d, U.CFG), (AC.d, AC.CFG)) for n, k in sorted(cfg.get('guard', {}).items())]


for _k, _c in KN.items():
    item(f'knight_statue_{_k}', TOTEM, _c['item'], _c['col'],
         [_c['lore'], ('Sneak + use on a block: set it up.', 'blue'), ('Sneak + punch it: take it back.', 'gray')],
         model=f'bm:knight_statue_{_k}', stack=1, cat='relic', comps=hold('none'), bold=True)
    HOLD[f'knight_statue_{_k}'] = f'bm:{PFX}/statue/use_{_k}'


def generate(G):
    fn, title, give = G.fn, G.title, G.give
    tick, second = G.FUNCS['tick'], G.FUNCS['loop/second']
    objs = ['bm.kid', 'bm.kst', 'bm.ks', 'bm.kt', 'bm.ka', 'bm.kc']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + \
        ['scoreboard players set #5 bm.rng 5', 'scoreboard players set #8 bm.rng 8', 'scoreboard players set #10 bm.rng 10',
         'scoreboard players set #20 bm.rng 20', 'scoreboard players set #40 bm.rng 40']
    G.OBJECTIVES += objs
    GR = groups()
    snd = lambda s, v, p: f'playsound minecraft:{s} hostile @a[distance=..24] ~ ~ ~ {v} {p}'
    at = lambda t, cmd: f'execute if score @s bm.kt matches {t} run {cmd}'

    # ================================================================== the rig: poses, finishes, its place each tick
    for name, pz in A.POSES.items():
        fn(f'{PFX}/pose/{name}', RF.pose(A, pz, SCALE, DUR.get(name, 6), sel))
    fn(f'{PFX}/place', RF.place(A, SCALE / 16, sel))
    for k in KN:
        for fin in ('stone', 'live'):
            fn(f'{PFX}/finish/{k}_{fin}', [f'data modify entity @e[type=minecraft:item_display,tag=bm.ksel,tag=bm.kr_{p},limit=1] item.components."minecraft:item_model" '
                                           f'set value "{A.model_name(p, k, fin)}"' for p in A.PARTS])
        fn(f'{PFX}/rig/{k}', [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, ["bm.kr", f"bm.kr_{p}", "bm.knew"], SCALE, model=A.model_name(p, k, "stone")[3:], extra=dict(view_range=F(3.0)))}'
                              for p in A.PARTS])
    # (each part's kid: the knight's, so many can share a room - its own are tagged bm.ksel for the moment they move)
    fn(f'{PFX}/mine', ['scoreboard players operation #me bm.kid = @s bm.kid',
                       'execute as @e[type=minecraft:item_display,tag=bm.kr] if score @s bm.kid = #me bm.kid run tag @s add bm.ksel'])

    # ================================================================== the statue: raised by its marker near a player
    fn(f'{PFX}/raise', ['scoreboard players add #kid bm.kid 1', 'scoreboard players operation @s bm.kid = #kid bm.kid', 'scoreboard players set @s bm.kst 1'] +
       [f'execute if entity @s[tag=bm.knk_{k}] rotated as @s rotated ~ 0 run function bm:{PFX}/rig/{k}' for k in KN] +
       ['scoreboard players operation @e[type=minecraft:item_display,tag=bm.knew,distance=..1] bm.kid = @s bm.kid',
        'tag @e[type=minecraft:item_display,tag=bm.knew,distance=..1] add bm.ksel', 'tag @e[tag=bm.knew] remove bm.knew',
        f'execute rotated as @s rotated ~ 0 run function bm:{PFX}/place', f'function bm:{PFX}/pose/statue',
        'tag @e[tag=bm.ksel] remove bm.ksel'])
    second.append(f'execute as @e[type=minecraft:marker,tag=bm.kstat] unless score @s bm.kst matches 1.. at @s if entity @a[distance=..48] run function bm:{PFX}/raise')

    # ================================================================== the waking: its room solved
    for (d, n, k) in GR:
        c = KN[k]
        host = {'Tags': ['bm.khost', f'bm.kh_{k}', f'bm.kg_{d}{n}', 'bm.seen', 'bm.knewh'], 'NoAI': B(1), 'Silent': B(1), 'PersistenceRequired': B(1),
                'CustomName': T(c['name'], c['col']), 'DeathLootTable': 'minecraft:empty', 'CanPickUpLoot': B(0),
                'attributes': [{'id': 'minecraft:max_health', 'base': Dd(c['hp'] + FLOOR)}, {'id': 'minecraft:scale', 'base': Dd(HOSTSC)},
                               {'id': 'minecraft:armor', 'base': Dd(10)}, {'id': 'minecraft:knockback_resistance', 'base': Dd(1.0)},
                               {'id': 'minecraft:attack_damage', 'base': Dd(0)}, {'id': 'minecraft:movement_speed', 'base': Dd(0.2)},
                               {'id': 'minecraft:follow_range', 'base': Dd(40)}],
                'Health': F(c['hp'] + FLOOR),
                'active_effects': [{'id': 'minecraft:invisibility', 'duration': Int(-1), 'amplifier': B(0), 'show_particles': B(0)},
                                   {'id': 'minecraft:fire_resistance', 'duration': Int(-1), 'amplifier': B(0), 'show_particles': B(0)}]}
        fn(f'{PFX}/wake/{d}{n}', ['title @a[distance=..40] times 10 50 20', title('@a[distance=..40]', 'title', T(' ', 'white')),
                                  title('@a[distance=..40]', 'subtitle', T(f'The statues stir... the {c["name"]}s wake!', c['col'], bold=True)),
                                  f'execute as @e[type=minecraft:marker,tag=bm.kstat,tag=bm.kn{n},tag=bm.d_{d},distance=..60] at @s run function bm:{PFX}/wake1/{d}{n}'])
        fn(f'{PFX}/wake1/{d}{n}', ['execute if score @s bm.kst matches 2.. run return 0',
                                   f'execute unless score @s bm.kst matches 1 run function bm:{PFX}/raise',
                                   'scoreboard players set @s bm.kst 2',
                                   f'execute rotated as @s rotated ~ 0 run summon minecraft:husk ~ ~ ~ {snbt(host)}',
                                   'scoreboard players operation @e[type=minecraft:husk,tag=bm.knewh,distance=..1] bm.kid = @s bm.kid',
                                   'scoreboard players set @e[type=minecraft:husk,tag=bm.knewh,distance=..1] bm.ks 0',
                                   'scoreboard players set @e[type=minecraft:husk,tag=bm.knewh,distance=..1] bm.kt 0',
                                   'tag @e[type=minecraft:husk,tag=bm.knewh,distance=..1] remove bm.knewh'])
        # (the trial reset: its knights back on their plinths, stone - the marker raises them again)
        fn(f'{PFX}/rest/{d}{n}', [f'execute as @e[type=minecraft:marker,tag=bm.kstat,tag=bm.kn{n},tag=bm.d_{d},distance=..60] run function bm:{PFX}/rest1'])
        # (the last of them fallen: the door opens, as the solve would have)
        fn(f'{PFX}/done/{d}{n}', [f'execute if entity @e[type=minecraft:marker,tag=bm.kstat,tag=bm.kn{n},tag=bm.d_{d},scores={{bm.kst=2..3}}] run return 0',
                                  f'execute as @e[type=minecraft:marker,tag=bm.pz,tag=bm.pz{n},tag=bm.d_{d}] at @s run function bm:p2/{d}/pz{n}_open'])
        # (the room's bar: what's left of its knights)
        G.FUNCS['load'][-1:-1] = [f'bossbar add bm:kn_{d}{n} {snbt(T(c["name"] + "s", c["col"], bold=True))}', f'bossbar set bm:kn_{d}{n} color {"red" if k == "dread" else "green"}',
                                  f'bossbar set bm:kn_{d}{n} style notched_10']
        fn(f'{PFX}/bar/{d}{n}', ['scoreboard players set #s bm.rng 0', 'scoreboard players set #c bm.rng 0',
                                 f'execute as @e[type=minecraft:husk,tag=bm.kg_{d}{n},scores={{bm.ks=1..4}}] run function bm:{PFX}/hpadd',
                                 f'execute if score #c bm.rng matches 0 run return run bossbar set bm:kn_{d}{n} players',
                                 f'execute store result bossbar bm:kn_{d}{n} value run scoreboard players get #s bm.rng',
                                 f'bossbar set bm:kn_{d}{n} max {c["hp"] * 2}', f'bossbar set bm:kn_{d}{n} players @a[distance=..48]'])
        second.append(f'execute as @e[type=minecraft:marker,tag=bm.pz,tag=bm.pz{n},tag=bm.d_{d}] at @s run function bm:{PFX}/bar/{d}{n}')
    fn(f'{PFX}/hpadd', ['execute store result score #h bm.rng run data get entity @s Health', f'scoreboard players remove #h bm.rng {FLOOR}',
                        'scoreboard players operation #s bm.rng += #h bm.rng', 'scoreboard players add #c bm.rng 1'])
    fn(f'{PFX}/rest1', ['scoreboard players operation #me bm.kid = @s bm.kid',
                        'execute as @e[type=minecraft:item_display,tag=bm.kr] if score @s bm.kid = #me bm.kid run kill @s',
                        'execute as @e[type=minecraft:husk,tag=bm.khost] if score @s bm.kid = #me bm.kid run function bm:p245/gone',
                        'scoreboard players set @s bm.kst 0'])
    fn(f'{PFX}/gone', ['tp @s ~ -400 ~', 'kill @s'])

    # ================================================================== each tick, each knight awake
    tick.append(f'execute as @e[type=minecraft:husk,tag=bm.khost] at @s run function bm:{PFX}/tick')
    fn(f'{PFX}/tick', ['scoreboard players add @s bm.kt 1', 'tag @s add bm.kme', f'function bm:{PFX}/mine',
                       f'execute if score @s bm.ks matches 1..4 store result score #h bm.rng run data get entity @s Health',
                       f'execute if score @s bm.ks matches 1..4 if score #h bm.rng matches ..{FLOOR} run function bm:{PFX}/fall0',
                       f'execute if score @s bm.ks matches 0 run function bm:{PFX}/s/wake',
                       f'execute if score @s bm.ks matches 1 run function bm:{PFX}/s/fight',
                       f'execute if score @s bm.ks matches 2 run function bm:{PFX}/s/slam',
                       f'execute if score @s bm.ks matches 3 run function bm:{PFX}/s/spin',
                       f'execute if score @s bm.ks matches 4 run function bm:{PFX}/s/reel',
                       f'execute if score @s bm.ks matches 5 run function bm:{PFX}/s/fall',
                       f'execute unless score @s bm.ks matches 5 rotated as @s rotated ~ 0 run function bm:{PFX}/place',
                       'tag @e[type=minecraft:item_display,tag=bm.ksel] remove bm.ksel', 'tag @s remove bm.kme'])
    crumble = lambda k: f'particle minecraft:block{{block_state:"{KN[k]["stone"]}"}} ~ ~1.5 ~ 0.6 1.2 0.6 0 60'
    lit = lambda k: f'particle minecraft:dust{{color:[{KN[k]["dust"]}],scale:1.6}} ~ ~2.4 ~ 0.4 0.4 0.4 0 30'
    # ---- the waking (stone cracks, eyes light, the mace hefted)
    fn(f'{PFX}/s/wake', [at(1, f'function bm:{PFX}/pose/wake_0'), at(1, snd('block.deepslate.break', 1.4, 0.5)), at(1, snd('entity.warden.emerge', 0.8, 1.4))] +
       [at(12, f'execute if entity @s[tag=bm.kh_{k}] run function bm:{PFX}/finish/{k}_live') for k in KN] +
       [at(12, f'execute if entity @s[tag=bm.kh_{k}] run {crumble(k)}') for k in KN] + [at(12, f'execute if entity @s[tag=bm.kh_{k}] run {lit(k)}') for k in KN] +
       [at(12, snd('entity.iron_golem.repair', 1.2, 0.5)),
        at(22, f'function bm:{PFX}/pose/wake_1'), at(22, snd('item.mace.smash_air', 1.2, 0.6)),
        at(40, 'data merge entity @s {NoAI:0b}'), at(40, f'effect give @s minecraft:resistance infinite {RESIST} true'),
        at(40, 'scoreboard players set @s bm.ka 0'), at(40, 'scoreboard players set @s bm.kc 0'), at(40, 'scoreboard players set @s bm.kt 0'),
        at(40, 'scoreboard players set @s bm.ks 1')])
    # ---- the fight: stalk (walking) or square up (idle), and every EVERY ticks an attack - slam and spin by turns
    near = f'@a[distance=..3,{FOES}]'
    fn(f'{PFX}/s/fight', ['scoreboard players add @s bm.ka 1',
                          'scoreboard players operation #f bm.rng = @s bm.kt', 'scoreboard players operation #f bm.rng %= #20 bm.rng',
                          f'execute if entity {near} if score #f bm.rng matches 0 run function bm:{PFX}/pose/idle_a',
                          f'execute if entity {near} if score #f bm.rng matches 10 run function bm:{PFX}/pose/idle_b',
                          f'execute unless entity {near} if score #f bm.rng matches 0 run function bm:{PFX}/pose/walk_0',
                          f'execute unless entity {near} if score #f bm.rng matches 5 run function bm:{PFX}/pose/walk_1',
                          f'execute unless entity {near} if score #f bm.rng matches 10 run function bm:{PFX}/pose/walk_2',
                          f'execute unless entity {near} if score #f bm.rng matches 15 run function bm:{PFX}/pose/walk_3',
                          f'execute unless entity {near} if score #f bm.rng matches 0 run {snd("entity.iron_golem.step", 0.9, 0.5)}',
                          f'execute unless entity {near} if score #f bm.rng matches 10 run {snd("entity.iron_golem.step", 0.9, 0.5)}',
                          f'execute if score @s bm.ka matches {EVERY}.. if score @s bm.kc matches 0 if entity @a[distance=..4.5,{FOES}] run return run function bm:{PFX}/slam0',
                          f'execute if score @s bm.ka matches {EVERY}.. if score @s bm.kc matches 1 if entity @a[distance=..6,{FOES}] run return run function bm:{PFX}/spin0'])
    face = f'execute facing entity @p[distance=..16,{FOES}] feet run tp @s ~ ~ ~ ~ 0'
    fn(f'{PFX}/slam0', ['scoreboard players set @s bm.ks 2', 'scoreboard players set @s bm.kt 0', 'scoreboard players set @s bm.kc 1',
                        'data merge entity @s {NoAI:1b}', face, f'function bm:{PFX}/pose/swing_0',
                        snd('entity.ravager.attack', 1.2, 0.5), snd('block.chain.break', 1, 0.5)])
    fn(f'{PFX}/s/slam', [at(WIND, f'function bm:{PFX}/pose/swing_1')] +
       [at(HIT, f'execute if entity @s[tag=bm.kh_{k}] run function bm:{PFX}/slam_{k}') for k in KN] +
       [at(BACK - 8, f'function bm:{PFX}/pose/idle_a'),
        at(BACK, 'data merge entity @s {NoAI:0b}'), at(BACK, 'scoreboard players set @s bm.ka 0'), at(BACK, 'scoreboard players set @s bm.ks 1')])
    for k, c in KN.items():
        fn(f'{PFX}/slam_{k}', [f'execute positioned ^ ^ ^2 as @a[distance=..2.6,{FOES}] run damage @s {c["slam"]} minecraft:mob_attack by {ME}',
                               f'execute positioned ^ ^ ^2 as @a[distance=2.6..5,{FOES}] run damage @s {c["wave"]} minecraft:mob_attack by {ME}',
                               f'execute positioned ^ ^ ^2 run particle minecraft:explosion ~ ~0.2 ~ 0.6 0.1 0.6 0 3',
                               f'execute positioned ^ ^ ^2 run particle minecraft:block{{block_state:"{c["stone"]}"}} ~ ~0.2 ~ 1.4 0.1 1.4 0.2 80',
                               f'execute positioned ^ ^ ^2 run particle minecraft:dust{{color:[{c["dust"]}],scale:2.0}} ~ ~0.3 ~ 1.8 0.1 1.8 0 40',
                               snd('item.mace.smash_ground_heavy', 1.6, 0.6), snd('entity.generic.explode', 0.8, 0.7)])
    # ---- the spin: the mace out at arm's length, round and round, drifting after you; then it reels
    fn(f'{PFX}/spin0', ['scoreboard players set @s bm.ks 3', 'scoreboard players set @s bm.kt 0', 'scoreboard players set @s bm.kc 0',
                        'data merge entity @s {NoAI:1b}', face, f'function bm:{PFX}/pose/spin_0',
                        snd('entity.player.attack.sweep', 1.4, 0.4), snd('entity.ravager.roar', 0.8, 0.8)])
    fn(f'{PFX}/s/spin', ['scoreboard players operation #f bm.rng = @s bm.kt', 'scoreboard players operation #f bm.rng %= #10 bm.rng',
                         f'execute if score @s bm.kt matches {SPIN0}..{SPIN1} run tp @s ~ ~ ~ ~36 ~',
                         f'execute if score @s bm.kt matches {SPIN0}..{SPIN1} facing entity @p[distance=..16,{FOES}] feet rotated ~ 0 positioned ^ ^ ^0.12 '
                         'if block ~ ~ ~ #minecraft:replaceable if block ~ ~1 ~ #minecraft:replaceable if block ~ ~2 ~ #minecraft:replaceable run tp @s ~ ~ ~',
                         f'execute if score @s bm.kt matches {SPIN0}..{SPIN1} if score #f bm.rng matches 0 run function bm:{PFX}/pose/spin_1',
                         f'execute if score @s bm.kt matches {SPIN0}..{SPIN1} if score #f bm.rng matches 5 run function bm:{PFX}/pose/spin_0',
                         'scoreboard players operation #g bm.rng = @s bm.kt', 'scoreboard players operation #g bm.rng %= #8 bm.rng'] +
       [f'execute if score @s bm.kt matches {SPIN0}..{SPIN1} if score #g bm.rng matches 0 if entity @s[tag=bm.kh_{k}] run function bm:{PFX}/whirl_{k}' for k in KN] +
       [at(SPIN1 + 1, 'scoreboard players set @s bm.ks 4'), at(SPIN1 + 1, 'scoreboard players set @s bm.kt 0'),
        at(SPIN1 + 1, f'function bm:{PFX}/pose/stagger'), at(SPIN1 + 1, 'effect clear @s minecraft:resistance'),
        at(SPIN1 + 1, snd('entity.iron_golem.damage', 1.2, 0.5)),
        at(SPIN1 + 1, title(f'@a[distance=..16]', 'actionbar', T('It reels, dizzy - its guard is down. Strike now!', 'gold', bold=True)))])
    for k, c in KN.items():
        fn(f'{PFX}/whirl_{k}', [f'execute as @a[distance=..3.8,{FOES}] run damage @s {c["spin"]} minecraft:mob_attack by {ME}',
                                'particle minecraft:sweep_attack ~ ~1.2 ~ 1.6 0.2 1.6 0 6',
                                f'particle minecraft:dust{{color:[{c["dust"]}],scale:1.4}} ~ ~1.2 ~ 2 0.2 2 0 16',
                                snd('entity.player.attack.sweep', 1.0, 0.6)])
    fn(f'{PFX}/s/reel', ['execute if score @s bm.kt matches 1.. run particle minecraft:crit ~ ~3.1 ~ 0.3 0.1 0.3 0.1 2',
                         at(REEL, f'effect give @s minecraft:resistance infinite {RESIST} true'), at(REEL, f'function bm:{PFX}/pose/idle_a'),
                         at(REEL, 'data merge entity @s {NoAI:0b}'), at(REEL, 'scoreboard players set @s bm.ka 0'), at(REEL, 'scoreboard players set @s bm.ks 1')])
    # ---- the fall: to one knee, slumped over the haft, stone again where it knelt; its statue for everyone near
    fn(f'{PFX}/fall0', ['scoreboard players set @s bm.ks 5', 'scoreboard players set @s bm.kt 0', 'data merge entity @s {NoAI:1b,Invulnerable:1b}',
                        'effect clear @s minecraft:resistance', f'function bm:{PFX}/pose/death_0', snd('entity.iron_golem.death', 1.4, 0.5)])
    fn(f'{PFX}/s/fall', [at(25, f'function bm:{PFX}/pose/death_1'), at(25, snd('block.chain.fall', 1, 0.5))] +
       [at(45, f'execute if entity @s[tag=bm.kh_{k}] run function bm:{PFX}/finish/{k}_stone') for k in KN] +
       [at(45, f'execute if entity @s[tag=bm.kh_{k}] run {crumble(k)}') for k in KN] +
       [at(45, snd('block.deepslate.place', 1.4, 0.5)), at(45, snd('block.stone.break', 1.2, 0.6))] +
       [at(60, f'execute if entity @s[tag=bm.kh_{k}] as @a[distance=..32,gamemode=!spectator] run function bm:{PFX}/gift_{k}') for k in KN] +
       [at(60, f'function bm:{PFX}/fell')])
    for k, c in KN.items():
        fn(f'{PFX}/gift_{k}', [give(f'knight_statue_{k}'), 'playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 0.7',
                               title('@s', 'actionbar', [T('The ' + c['name'] + ' falls - ', c['col'], bold=True), T('its statue is yours.', 'gray')])])
    fn(f'{PFX}/fell', ['execute as @e[type=minecraft:marker,tag=bm.kstat] if score @s bm.kid = #me bm.kid run scoreboard players set @s bm.kst 4'] +
       [f'execute if entity @s[tag=bm.kg_{d}{n}] run function bm:{PFX}/done/{d}{n}' for (d, n, k) in GR] +
       [f'function bm:{PFX}/gone'])

    # ================================================================== the statue at home: set up on a block, taken back with sneak + punch
    ident = [F(0), F(0), F(0), F(1)]
    T_ = getattr(A, 'STATUE_DISPLAY', {'translation': [0.0, 0.0, 0.0], 'scale': 1.0})
    for k, c in KN.items():
        iid = f'knight_statue_{k}'
        fn(f'{PFX}/statue/use_{k}', ['execute unless predicate bm:p20/sneaking run return run ' + title('@s', 'actionbar', T('Sneak + use on the top of a block: set the statue up.', 'gray')),
                                     'execute if dimension bm:gutter run return run ' + title('@s', 'actionbar', T('Not in the vault - set it up out in the world.', 'gray')),
                                     'scoreboard players set #placed bm.rng 0', 'scoreboard players set #ray bm.rng 25', 'tag @s add bm.placer',
                                     f'execute anchored eyes positioned ^ ^ ^ run function bm:{PFX}/statue/ray_{k}', 'tag @s remove bm.placer',
                                     'execute if score #placed bm.rng matches 0 run return run ' + title('@s', 'actionbar', T('Look at the top of a block within 5 blocks (with room above it).', 'gray')),
                                     f'execute unless entity @s[gamemode=creative] if items entity @s weapon.mainhand *[minecraft:custom_data~{{bm:"{iid}"}}] run return run item replace entity @s weapon.mainhand with minecraft:air',
                                     f'execute unless entity @s[gamemode=creative] if items entity @s weapon.offhand *[minecraft:custom_data~{{bm:"{iid}"}}] run item replace entity @s weapon.offhand with minecraft:air'])
        fn(f'{PFX}/statue/ray_{k}', [f'execute unless block ~ ~ ~ #minecraft:replaceable run return run function bm:{PFX}/statue/hit_{k}',
                                     'scoreboard players remove #ray bm.rng 1', f'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:{PFX}/statue/ray_{k}'])
        fn(f'{PFX}/statue/hit_{k}', ['execute align xyz positioned ~0.5 ~1 ~0.5 unless block ~ ~ ~ #minecraft:replaceable run return 0',
                                     'execute align xyz positioned ~0.5 ~1 ~0.5 unless block ~ ~1 ~ #minecraft:replaceable run return 0',
                                     'execute align xyz positioned ~0.5 ~1 ~0.5 unless block ~ ~2 ~ #minecraft:replaceable run return 0',
                                     'execute align xyz positioned ~0.5 ~1 ~0.5 if entity @e[type=minecraft:interaction,tag=bm.gvdeco,distance=..0.8] run return 0',
                                     f'execute align xyz positioned ~0.5 ~1 ~0.5 run function bm:{PFX}/statue/place_{k}', 'scoreboard players set #placed bm.rng 1'])
        disp = {'Tags': ['bm.knsd', f'bm.knsd_{k}', 'bm.knnew'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:knight_statue_{k}'}},
                'item_display': 'fixed', 'view_range': F(2.0),
                'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(v) for v in T_['translation']], 'scale': [F(T_['scale'])] * 3}}
        fn(f'{PFX}/statue/place_{k}', ['summon minecraft:item_display ~ ~ ~ ' + snbt(disp),
                                       'summon minecraft:interaction ~ ~ ~ ' + snbt({'Tags': ['bm.knst', f'bm.knst_{k}', 'bm.gvdeco', 'bm.knnew'], 'width': F(1.0), 'height': F(2.8), 'response': B(1)}),
                                       'execute as @e[type=minecraft:item_display,tag=bm.knnew,distance=..0.5] at @s facing entity @a[tag=bm.placer,limit=1] feet run tp @s ~ ~ ~ ~ 0',
                                       'tag @e[tag=bm.knnew,distance=..0.5] remove bm.knnew',
                                       f'particle minecraft:block{{block_state:"{c["stone"]}"}} ~ ~1 ~ 0.5 1 0.5 0 40',
                                       'playsound minecraft:block.deepslate.place block @a[distance=..16] ~ ~ ~ 1 0.6',
                                       title('@a[tag=bm.placer]', 'actionbar', [T(c['item'], c['col'], bold=True), T(' stands guard. (Sneak + punch it: take it back.)', 'gray')])])
        fn(f'{PFX}/statue/take_{k}', [give(iid), f'kill @e[type=minecraft:item_display,tag=bm.knsd_{k},distance=..0.6,limit=1,sort=nearest]',
                                      f'particle minecraft:block{{block_state:"{c["stone"]}"}} ~ ~1 ~ 0.5 1 0.5 0 30', 'playsound minecraft:block.deepslate.break block @a[distance=..16] ~ ~ ~ 1 0.6'])
        G.FUNCS['p71/deco/pick'][0:0] = [f'execute if entity @e[type=minecraft:interaction,tag=bm.gvdme,tag=bm.knst_{k}] at @e[type=minecraft:interaction,tag=bm.gvdme,limit=1] '
                                         f'run function bm:{PFX}/statue/take_{k}']
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.knsd]', 'kill @e[type=minecraft:interaction,tag=bm.knst]',
                                       'kill @e[type=minecraft:item_display,tag=bm.kr]', 'execute as @e[type=minecraft:husk,tag=bm.khost] run function bm:p245/gone']
    fn('admin/knights/statues', [give(f'knight_statue_{k}') for k in KN])
    fn('admin/knights/wake', [f'execute as @e[type=minecraft:marker,tag=bm.pz,tag=bm.pz{n},tag=bm.d_{d}] at @s if entity @a[distance=..60] run function bm:{PFX}/wake/{d}{n}'
                              for (d, n, k) in GR])
    fn('admin/knights/rest', [f'execute as @e[type=minecraft:marker,tag=bm.pz,tag=bm.pz{n},tag=bm.d_{d}] at @s run function bm:{PFX}/rest/{d}{n}' for (d, n, k) in GR])


def rp(R):
    A.rp(R)

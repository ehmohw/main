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
           knight stands on its plinth again, a statue, waiting.
AT HOME    (3.0, the owner) its statue set up in your base, right-clicked (not sneaking) by its OWNER - the placer (the plinth's
           bm.pid; a statue set up before 3.0 has none: the first to right-click it becomes its owner) - opens its dialog:
  STAND GUARD  it wakes (the dungeon's waking) as a guard: it keeps its post (NoAI; it steps after its foe, never more than
           6 blocks from its plinth, and walks back when there's none), goes for the monsters within 10 blocks of its plinth
           (#bm:hostile, never the pack's own: npcs, other knights, Mires, bosses) with its slam and spin - which strike only
           them: never players, pets, followers, villagers, never a block. Only monsters can hurt it (any other blow is undone
           at once) and it mends 1 a second. Brought low it kneels, stone, for a minute (invulnerable), then wakes again.
           Right-clicked again: "Rest" - it walks back onto its plinth and is stone (waking or kneeling: at once).
  DUEL ME  it wakes as the dungeon's mini-boss (its health, slam and spin, Resistance, the reel) against its owner alone (no other
           player is struck), its bar (bm:kduel1..4, one per duel) for everyone within 48. It keeps within 20 of its plinth.
           You fall, go 32 blocks from it, log out or go creative: it walks home, stone, the statue intact. You strike it down:
           it falls (the fall, the stone), its plinth empties and its STATUE DROPS (plus 10 xp, nothing more). One duel per
           statue, one per player at a time.
  CAP      four knights awake (guarding or duelling) within 64 blocks of a statue at most.
  KEPT     the state is on the entities (the host's bm.ks/bm.kt, the plinth's bm.kgm 1 guard / 2 duel, bm.pid, the shared bm.kid),
           all persistent - a logout or an unloaded chunk just pauses it. Each second the knight counts its rig (13 parts; one
           lost, or doubled by a late-loading chunk: built afresh), and a knight and its plinth that lose each other for 5 s
           end it: the plinth turns to stone again (the knight killed, the world gone peaceful...), the knight goes.
           Sneak + punch while it's awake: it goes, and the statue is yours (no copy).
           (p245/h/*; its buttons 5591-5593, menu 5590)"""
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
T_SC = getattr(A, 'STATUE_DISPLAY', {'scale': 1.0})['scale']        # (the placed statue's own scale - put back when it's stone again)
sel = lambda p: f'@e[type=minecraft:item_display,tag=bm.ksel,tag=bm.kr_{p}]'
FOES = 'gamemode=!spectator,gamemode=!creative'


def groups():
    """every guarded trial: (d, n, kind)"""
    import p2.undercfg as U
    import p2.armadacfg as AC
    return [(cfg_d, n, k) for cfg_d, cfg in ((U.d, U.CFG), (AC.d, AC.CFG)) for n, k in sorted(cfg.get('guard', {}).items())]


for _k, _c in KN.items():
    item(f'knight_statue_{_k}', TOTEM, _c['item'], _c['col'],
         [_c['lore'], ('Sneak + use on a block: set it up.', 'blue'), ('Right-click it, set up: wake it - to', 'blue'),
          ('stand guard, or to duel you.', 'blue'), ('Sneak + punch it: take it back.', 'gray')],
         model=f'bm:knight_statue_{_k}', stack=1, cat='relic', comps=hold('none'), bold=True)
    HOLD[f'knight_statue_{_k}'] = f'bm:{PFX}/statue/use_{_k}'


def generate(G):
    fn, title, give = G.fn, G.title, G.give
    tick, second = G.FUNCS['tick'], G.FUNCS['loop/second']
    objs = ['bm.kid', 'bm.kst', 'bm.ks', 'bm.kt', 'bm.ka', 'bm.kc', 'bm.kgm', 'bm.ksq', 'bm.kgh', 'bm.kmiss', 'bm.kbs']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + \
        ['scoreboard players set #5 bm.rng 5', 'scoreboard players set #8 bm.rng 8', 'scoreboard players set #10 bm.rng 10',
         'scoreboard players set #20 bm.rng 20', 'scoreboard players set #40 bm.rng 40']
    G.OBJECTIVES += objs
    GR = groups()
    snd = lambda s, v, p: f'playsound minecraft:{s} hostile @a[distance=..24] ~ ~ ~ {v} {p}'
    at = lambda t, cmd: f'execute if score @s bm.kt matches {t} {cmd[8:]}' if cmd.startswith('execute ') else f'execute if score @s bm.kt matches {t} run {cmd}'

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
        fn(f'{PFX}/rest/{d}{n}', [f'execute as @e[type=minecraft:marker,tag=bm.kstat,tag=bm.kn{n},tag=bm.d_{d},distance=..60] at @s run function bm:{PFX}/rest1'])
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
                        'execute as @e[type=minecraft:husk,tag=bm.khost] if score @s bm.kid = #me bm.kid at @s run function bm:p245/gone',
                        'scoreboard players set @s bm.kst 0'])
    fn(f'{PFX}/gone', ['tp @s ~ -400 ~', 'kill @s'])

    # ================================================================== each tick, each knight awake
    tick.append(f'execute as @e[type=minecraft:husk,tag=bm.khost] at @s run function bm:{PFX}/tick')
    fn(f'{PFX}/tick', ['scoreboard players add @s bm.kt 1', 'tag @s add bm.kme', f'function bm:{PFX}/mine',
                       f'execute if entity @s[tag=bm.khome] run return run function bm:{PFX}/h/tick',      # (3.0: a statue woken at home - its own)
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
        at(40, 'scoreboard players set @s bm.ka 0'), at(40, 'scoreboard players set @s bm.kc 0'), at(40, 'scoreboard players set @s bm.ks 1'),
        at(40, 'scoreboard players set @s bm.kt 0')])        # (the timer's reset last: every line after it would read 0)
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
       [at(SPIN1 + 1, f'function bm:{PFX}/pose/stagger'), at(SPIN1 + 1, 'effect clear @s minecraft:resistance'),
        at(SPIN1 + 1, snd('entity.iron_golem.damage', 1.2, 0.5)),
        at(SPIN1 + 1, title(f'@a[distance=..16]', 'actionbar', T('It reels, dizzy - its guard is down. Strike now!', 'gold', bold=True))),
        at(SPIN1 + 1, 'scoreboard players set @s bm.ks 4'), at(SPIN1 + 1, 'scoreboard players set @s bm.kt 0')])
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
       [at(60, f'execute if entity @s[tag=bm.kh_{k}] as @a[distance=..32,gamemode=!spectator] at @s run function bm:{PFX}/gift_{k}') for k in KN] +
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
                                     'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
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
                                       'scoreboard players operation @e[type=minecraft:interaction,tag=bm.knnew,distance=..0.5] bm.pid = @a[tag=bm.placer,limit=1] bm.pid',
                                       'scoreboard players set @e[type=minecraft:interaction,tag=bm.knnew,distance=..0.5] bm.kgm 0',
                                       'tag @e[tag=bm.knnew,distance=..0.5] remove bm.knnew',
                                       f'particle minecraft:block{{block_state:"{c["stone"]}"}} ~ ~1 ~ 0.5 1 0.5 0 40',
                                       'playsound minecraft:block.deepslate.place block @a[distance=..16] ~ ~ ~ 1 0.6',
                                       title('@a[tag=bm.placer]', 'actionbar', [T(c['item'], c['col'], bold=True), T(' stands here. (Right-click it: wake it. Sneak + punch it: take it back.)', 'gray')])])
        fn(f'{PFX}/statue/take_{k}', ['execute as @e[type=minecraft:interaction,tag=bm.gvdme,limit=1] if score @s bm.kgm matches 1.. at @s run function bm:p245/h/unwake',
                                      give(iid), f'kill @e[type=minecraft:item_display,tag=bm.knsd_{k},distance=..0.6,limit=1,sort=nearest]',
                                      f'particle minecraft:block{{block_state:"{c["stone"]}"}} ~ ~1 ~ 0.5 1 0.5 0 30', 'playsound minecraft:block.deepslate.break block @a[distance=..16] ~ ~ ~ 1 0.6'])
        G.FUNCS['p71/deco/pick'][0:0] = [f'execute if entity @e[type=minecraft:interaction,tag=bm.gvdme,tag=bm.knst_{k}] at @e[type=minecraft:interaction,tag=bm.gvdme,limit=1] '
                                         f'run function bm:{PFX}/statue/take_{k}']
    home(G, snd, at, crumble, lit)

    G.FUNCS['admin/uninstall'][0:0] = [f'bossbar remove bm:kduel{i}' for i in range(1, DUELS + 1)]
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.knsd]', 'kill @e[type=minecraft:interaction,tag=bm.knst]',
                                       'kill @e[type=minecraft:item_display,tag=bm.kr]', 'execute as @e[type=minecraft:husk,tag=bm.khost] at @s run function bm:p245/gone']
    fn('admin/knights/statues', [give(f'knight_statue_{k}') for k in KN])
    fn('admin/knights/wake', [f'execute as @e[type=minecraft:marker,tag=bm.pz,tag=bm.pz{n},tag=bm.d_{d}] at @s if entity @a[distance=..60] run function bm:{PFX}/wake/{d}{n}'
                              for (d, n, k) in GR])
    fn('admin/knights/rest', [f'execute as @e[type=minecraft:marker,tag=bm.pz,tag=bm.pz{n},tag=bm.d_{d}] at @s run function bm:{PFX}/rest/{d}{n}' for (d, n, k) in GR])



# ====================================================================== 3.0: THE STATUE AT HOME, WOKEN (the owner's "Stand guard" / "Duel me")
MENU = 5590                          # (bm.menu while a home statue's dialog is up)
B_GUARD, B_DUEL, B_REST = 5591, 5592, 5593
CAP, CAPR = 4, 64                    # (at most four knights awake at home within 64 blocks of each other's plinths)
LEASH, SIGHT = 6, 10                 # (a guard keeps within 6 blocks of its plinth; it goes for monsters within 10 of it)
DLEASH, REACH = 20, 32               # (a dueller keeps within 20 of its plinth; the duel is over if its challenger is 32 away)
COOL = 1200                          # (a guard brought low: stone this long - a minute - then it wakes again)
HOMEWARD = 200                       # (walking home longer than this: it steps straight onto its plinth)
DUELS = 4                            # (the duels' bars: bm:kduel1..4 - so many duels at once, world-wide)
MON = 'type=#bm:hostile,tag=!bm.npc,tag=!bm.khost,tag=!bm.mire,tag=!bm.boss,tag=!bm.stalker,tag=!bm.wil_body,tag=!bm.gvprop'
POST = '@e[type=minecraft:interaction,tag=bm.kpost,limit=1]'
TG = '@e[tag=bm.ktgt,limit=1]'
SQ = '@e[type=minecraft:interaction,tag=bm.kpick,limit=1]'      # (the statue a click / a button is about)
WALK = 'if block ~ ~ ~ #minecraft:replaceable if block ~ ~1 ~ #minecraft:replaceable'


def home(G, snd, at, crumble, lit):
    """3.0 (the owner): a statue set up at home, right-clicked by its owner, wakes - to STAND GUARD (it keeps its post, fights the
    monsters that come near, never you, your pets or your base; brought low it kneels, stone, for a minute, then wakes again) or to
    DUEL its owner (the dungeon's fight, in your base: beaten, it drops its statue again; it wins, it walks home and is stone)."""
    import phase28 as P28
    fn, title, give = G.fn, G.title, G.give
    tick, second, fast = G.FUNCS['tick'], G.FUNCS['loop/second'], G.FUNCS['loop/fast']
    say = lambda who, comp: title(who, 'actionbar', comp)
    H = f'{PFX}/h'
    G.FUNCS['load'][-1:-1] = [l for i in range(1, DUELS + 1) for l in (f'bossbar add bm:kduel{i} {snbt(T("Statue Knight", "gray"))}',
                                                                       f'bossbar set bm:kduel{i} style notched_10')]

    # ------------------------------------------------------------------ right-clicked: its dialog (the owner's; an older statue: the first to click)
    fast.append(f'execute as @e[type=minecraft:interaction,tag=bm.knst] if data entity @s interaction at @s run function bm:{H}/click')
    fn(f'{H}/click', ['execute on target run tag @s add bm.kclk', 'data remove entity @s interaction', 'tag @s add bm.kpick',
                      f'execute as @a[tag=bm.kclk,limit=1] at @s unless predicate bm:p20/sneaking run function bm:{H}/open',
                      'tag @s remove bm.kpick', 'tag @a[tag=bm.kclk] remove bm.kclk'])
    fn(f'{H}/open', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                     f'execute unless score {SQ} bm.pid matches 1.. run function bm:{H}/claim',
                     f'execute unless score @s bm.pid = {SQ} bm.pid run return run ' + say('@s', T('This knight answers only to the one who set it up.', 'gray')),
                     f'execute as {SQ} unless score @s bm.kid matches 1.. run function bm:{H}/newid',
                     f'execute if score {SQ} bm.kgm matches 2 run return run ' + say('@s', [T('A duel is under way. ', 'red', bold=True), T('Win it - or fall.', 'gray')]),
                     f'scoreboard players operation @s bm.ksq = {SQ} bm.kid', f'scoreboard players set @s bm.menu {MENU}'] +
       [f'execute if score {SQ} bm.kgm matches 1 if entity @e[type=minecraft:interaction,tag=bm.kpick,tag=bm.knst_{k}] run return run function bm:{H}/dlg/awake_{k}' for k in KN] +
       [f'execute if entity @e[type=minecraft:interaction,tag=bm.kpick,tag=bm.knst_{k}] run return run function bm:{H}/dlg/stone_{k}' for k in KN])
    fn(f'{H}/claim', [f'scoreboard players operation {SQ} bm.pid = @s bm.pid',
                      'tellraw @s ' + snbt([T('The statue knows you now: ', 'gray'), T('it answers to you alone.', 'white')])])
    fn(f'{H}/newid', ['scoreboard players add #kid bm.kid 1', 'scoreboard players operation @s bm.kid = #kid bm.kid'])
    for k, c in KN.items():
        nm = c['name']
        stone = P28.multi([T(nm.upper(), c['col'], bold=True), T('  ·  your statue', 'gray')],
                          [P28.body([T('Wake it, and it will...', 'gray')], 300)],
                          [P28.btn(T('Stand guard', 'green', bold=True), B_GUARD,
                                   tooltip=T(f'It keeps watch here, and fights any monster that comes within {SIGHT} blocks - never you, '
                                             'your pets or your base. Monsters that bring it low only stone it for a minute.', 'gray')),
                           P28.btn(T('Duel me', 'red', bold=True), B_DUEL,
                                   tooltip=T(f'It wakes as it fought in the dungeon - and fights you. Strike it down: its statue drops '
                                             f'again. Fall, or run ({REACH} blocks): it walks home, stone again.', 'gray'))], columns=2)
        awake = P28.multi([T(nm.upper(), c['col'], bold=True), T('  ·  on guard', 'gray')],
                          [P28.body([T('It keeps watch over this place.', 'gray')], 300)],
                          [P28.btn(T('Rest', 'gold', bold=True), B_REST, tooltip=T('It walks back to its plinth and turns to stone.', 'gray'))],
                          columns=1, exit_label='Keep watch')
        fn(f'{H}/dlg/stone_{k}', [f'dialog show @s {snbt(stone)}'])
        fn(f'{H}/dlg/awake_{k}', [f'dialog show @s {snbt(awake)}'])
    # ------------------------------------------------------------------ its buttons (exact codes; the router checks bm.menu)
    for code in (B_GUARD, B_DUEL, B_REST):
        G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {code} run return run function bm:{H}/act')
    fn(f'{H}/act', [f'execute unless score @s bm.menu matches {MENU} run return run function bm:p28/stale',
                    'scoreboard players operation #ksq bm.kid = @s bm.ksq',
                    'execute as @e[type=minecraft:interaction,tag=bm.knst,distance=..12] if score @s bm.kid = #ksq bm.kid run tag @s add bm.kpick',
                    'tag @s add bm.kclk', f'function bm:{H}/act2', 'tag @s remove bm.kclk',
                    'tag @e[type=minecraft:interaction,tag=bm.kpick] remove bm.kpick'])
    fn(f'{H}/act2', [f'execute unless entity {SQ} run return run ' + say('@s', T('Stand by your statue to do that.', 'gray')),
                     f'execute unless score @s bm.pid = {SQ} bm.pid run return run ' + say('@s', T('This knight answers only to the one who set it up.', 'gray')),
                     f'execute if score #act bm.pay matches {B_REST} as {SQ} at @s run return run function bm:{H}/rest',
                     f'execute if score {SQ} bm.kgm matches 1.. run return run ' + say('@s', T('It is awake already.', 'gray')),
                     f'execute store result score #n bm.rng at {SQ} if entity @e[type=minecraft:husk,tag=bm.khome,distance=..{CAPR}]',
                     f'execute if score #n bm.rng matches {CAP}.. run return run ' + say('@s', T(f'{CAP} knights are awake within {CAPR} blocks already - let one rest first.', 'gray')),
                     f'execute if score #act bm.pay matches {B_GUARD} as {SQ} at @s run return run function bm:{H}/guard',
                     f'execute if score #act bm.pay matches {B_DUEL} run return run function bm:{H}/duel'])
    fn(f'{H}/guard', ['scoreboard players set @s bm.kgm 1'] +
       [f'execute if entity @s[tag=bm.knst_{k}] run function bm:{H}/raise_{k}_g' for k in KN] +
       ['tag @e[type=minecraft:husk,tag=bm.knewh] remove bm.knewh',
        say('@a[tag=bm.kclk]', [T('It takes up its watch. ', 'green', bold=True), T('(Right-click its plinth: let it rest.)', 'gray')])])
    fn(f'{H}/duel', ['execute if entity @s[gamemode=creative] run return run ' + say('@s', T('Not in creative - it fights only those it can hurt.', 'gray')),
                     'scoreboard players operation #kp bm.pid = @s bm.pid', 'scoreboard players set #f bm.rng 0',
                     'execute as @e[type=minecraft:husk,tag=bm.kduel] if score @s bm.pid = #kp bm.pid run scoreboard players set #f bm.rng 1',
                     'execute if score #f bm.rng matches 1 run return run ' + say('@s', T('You are in a duel already.', 'gray')),
                     'scoreboard players set #slot bm.rng 0'] +
       [f'execute if score #slot bm.rng matches 0 unless entity @e[type=minecraft:husk,tag=bm.kduel,scores={{bm.kbs={i}}}] run scoreboard players set #slot bm.rng {i}' for i in range(1, DUELS + 1)] +
       ['execute if score #slot bm.rng matches 0 run return run ' + say('@s', T('Too many knights are duelling already - try again soon.', 'gray')),
        f'execute as {SQ} at @s run function bm:{H}/duel1'])
    fn(f'{H}/duel1', ['scoreboard players set @s bm.kgm 2'] +
       [f'execute if entity @s[tag=bm.knst_{k}] run function bm:{H}/raise_{k}_d' for k in KN] +
       ['scoreboard players operation @e[type=minecraft:husk,tag=bm.knewh,distance=..1] bm.kbs = #slot bm.rng'] +
       [f'execute if score #slot bm.rng matches {i} run function bm:{H}/d/barset{i}' for i in range(1, DUELS + 1)] +
       ['tag @e[type=minecraft:husk,tag=bm.knewh] remove bm.knewh',
        'title @a[tag=bm.kclk] times 10 50 20', title('@a[tag=bm.kclk]', 'title', T(' ', 'white')),
        title('@a[tag=bm.kclk]', 'subtitle', T('The statue stirs... it lifts its mace to you!', 'red', bold=True)),
        say('@a[tag=bm.kclk]', T(f'Strike it down to win its statue back. Fall, or run {REACH} blocks: it walks home.', 'gray'))])
    for i in range(1, DUELS + 1):
        fn(f'{H}/d/barset{i}', [l for k, c in KN.items() for l in
                                (f'execute if entity @s[tag=bm.knst_{k}] run bossbar set bm:kduel{i} name {snbt(T(c["name"], c["col"], bold=True))}',
                                 f'execute if entity @s[tag=bm.knst_{k}] run bossbar set bm:kduel{i} color {"red" if k == "dread" else "green"}',
                                 f'execute if entity @s[tag=bm.knst_{k}] run bossbar set bm:kduel{i} max {c["hp"]}')] +
           [f'bossbar set bm:kduel{i} players @a[tag=bm.kclk]'])
        fn(f'{H}/d/bar{i}', ['execute unless score @s bm.ks matches 0..5 run return 0',
                             'execute store result score #h bm.rng run data get entity @s Health', f'scoreboard players remove #h bm.rng {FLOOR}',
                             f'execute store result bossbar bm:kduel{i} value run scoreboard players get #h bm.rng',
                             f'bossbar set bm:kduel{i} players @a[distance=..48]'])
        second.append(f'execute unless entity @e[type=minecraft:husk,tag=bm.kduel,scores={{bm.kbs={i},bm.ks=0..5}}] run bossbar set bm:kduel{i} players')

    # ------------------------------------------------------------------ waking at home: the statue hidden, the rig stood in its place, a host for it
    for k, c in KN.items():
        for m, mt in (('g', ['bm.kguard', 'bm.npc']), ('d', ['bm.kduel'])):
            host = {'Tags': ['bm.khost', f'bm.kh_{k}', 'bm.khome'] + mt + ['bm.seen', 'bm.knewh'], 'NoAI': B(1), 'Silent': B(1), 'PersistenceRequired': B(1),
                    'CustomName': T(c['name'], c['col']), 'DeathLootTable': 'minecraft:empty', 'CanPickUpLoot': B(0),
                    'attributes': [{'id': 'minecraft:max_health', 'base': Dd(c['hp'] + FLOOR)}, {'id': 'minecraft:scale', 'base': Dd(HOSTSC)},
                                   {'id': 'minecraft:armor', 'base': Dd(10)}, {'id': 'minecraft:knockback_resistance', 'base': Dd(1.0)},
                                   {'id': 'minecraft:attack_damage', 'base': Dd(0)}],
                    'Health': F(c['hp'] + FLOOR),
                    'active_effects': [{'id': 'minecraft:invisibility', 'duration': Int(-1), 'amplifier': B(0), 'show_particles': B(0)},
                                       {'id': 'minecraft:fire_resistance', 'duration': Int(-1), 'amplifier': B(0), 'show_particles': B(0)}]}
            D = f'@e[type=minecraft:item_display,tag=bm.knsd_{k},distance=..0.6,sort=nearest,limit=1]'
            NH = '@e[type=minecraft:husk,tag=bm.knewh,distance=..1]'
            fn(f'{H}/raise_{k}_{m}', ['scoreboard players set @s bm.kmiss 0', 'data merge entity @s {height:0.5f}',
                                      f'execute as {D} run data merge entity @s {{transformation:{{scale:[0f,0f,0f]}}}}',
                                      f'execute rotated as {D} rotated ~ 0 run function bm:{PFX}/rig/{k}',
                                      'scoreboard players operation @e[type=minecraft:item_display,tag=bm.knew,distance=..1] bm.kid = @s bm.kid',
                                      'tag @e[type=minecraft:item_display,tag=bm.knew,distance=..1] add bm.ksel', 'tag @e[tag=bm.knew] remove bm.knew',
                                      f'execute rotated as {D} rotated ~ 0 run function bm:{PFX}/place', f'function bm:{PFX}/pose/statue',
                                      'tag @e[tag=bm.ksel] remove bm.ksel',
                                      f'summon minecraft:husk ~ ~ ~ {snbt(host)}',
                                      f'execute as {NH} rotated as {D} run tp @s ~ ~ ~ ~ 0',
                                      f'scoreboard players operation {NH} bm.kid = @s bm.kid',
                                      f'scoreboard players operation {NH} bm.pid = @a[tag=bm.kclk,limit=1] bm.pid',
                                      f'scoreboard players set {NH} bm.ks 0', f'scoreboard players set {NH} bm.kt 0', f'scoreboard players set {NH} bm.kbs 0',
                                      f'scoreboard players set {NH} bm.kmiss 0', f'scoreboard players set {NH} bm.kgh {(c["hp"] + FLOOR) * 10}'])
    # (the knight gone - taken back up, stood down, lost: its rig with it; as the statue's interaction)
    fn(f'{H}/unwake', ['scoreboard players operation #me bm.kid = @s bm.kid',
                       'execute as @e[type=minecraft:item_display,tag=bm.kr] if score @s bm.kid = #me bm.kid run kill @s',
                       'execute as @e[type=minecraft:husk,tag=bm.khome] if score @s bm.kid = #me bm.kid at @s run function bm:p245/h/gone',
                       'scoreboard players set @s bm.kgm 0'])
    fn(f'{H}/gone', ['scoreboard players set @s bm.ks 99', f'function bm:{PFX}/gone'])
    # (stone again on its plinth: as the statue's interaction)
    fn(f'{H}/restore', ['scoreboard players operation #me bm.kid = @s bm.kid',
                        'execute as @e[type=minecraft:item_display,tag=bm.kr] if score @s bm.kid = #me bm.kid run kill @s',
                        'execute as @e[type=minecraft:item_display,tag=bm.knsd,distance=..0.6,sort=nearest,limit=1] run data merge entity @s '
                        f'{{transformation:{{scale:[{T_SC}f,{T_SC}f,{T_SC}f]}}}}',
                        'data merge entity @s {height:2.8f}', 'scoreboard players set @s bm.kgm 0', 'scoreboard players set @s bm.kmiss 0'] +
       [f'execute if entity @s[tag=bm.knst_{k}] run {crumble(k)}' for k in KN] +
       [snd('block.deepslate.place', 1.4, 0.5), snd('block.stone.break', 1.2, 0.6)])
    fn(f'{H}/stone', ['scoreboard players operation #me bm.kid = @s bm.kid',
                      f'execute as @e[type=minecraft:interaction,tag=bm.knst] if score @s bm.kid = #me bm.kid at @s run function bm:{H}/restore',
                      f'function bm:{H}/gone'])
    fn(f'{H}/dismiss', ['scoreboard players operation #me bm.kid = @s bm.kid',
                        'execute as @e[type=minecraft:item_display,tag=bm.kr] if score @s bm.kid = #me bm.kid run kill @s', f'function bm:{H}/gone'])
    # ("Rest": as the statue's interaction - awake and fighting, it walks home first; waking, kneeling, stone: at once)
    fn(f'{H}/rest', ['execute unless score @s bm.kgm matches 1 run return run ' + say('@a[tag=bm.kclk]', T('It is not on guard.', 'gray')),
                     'scoreboard players operation #me bm.kid = @s bm.kid', 'scoreboard players set #f bm.rng 0',
                     f'execute as @e[type=minecraft:husk,tag=bm.khome,distance=..48] if score @s bm.kid = #me bm.kid at @s run function bm:{H}/rest1',
                     f'execute if score #f bm.rng matches 0 run function bm:{H}/restore',
                     say('@a[tag=bm.kclk]', T('It lays down its watch.', 'gray'))])
    fn(f'{H}/rest1', ['scoreboard players set #f bm.rng 1',
                      f'execute if score @s bm.ks matches 1..4 run return run function bm:{H}/homeward',
                      f'execute unless score @s bm.ks matches 7..8 run function bm:{H}/stone'])
    fn(f'{H}/homeward', ['data merge entity @s {Invulnerable:1b}', 'effect clear @s minecraft:resistance', 'scoreboard players set @s bm.ks 7',
                         'scoreboard players set @s bm.kt 0'])

    # ------------------------------------------------------------------ each tick (from p245/tick, its kid's parts tagged bm.ksel, @s bm.kme)
    fn(f'{H}/tick', ['execute as @e[type=minecraft:interaction,tag=bm.knst,distance=..48] if score @s bm.kid = #me bm.kid run tag @s add bm.kpost',
                     f'execute if entity @s[tag=bm.kduel] run function bm:{H}/d/pre',
                     f'execute if entity @s[tag=bm.kguard] run function bm:{H}/g/pre',
                     'execute if score @s bm.ks matches 1..4 store result score #h bm.rng run data get entity @s Health',
                     f'execute if score @s bm.ks matches 1..4 if score #h bm.rng matches ..{FLOOR} run function bm:{PFX}/fall0',
                     f'execute if score @s bm.ks matches 1..4 if entity @s[tag=bm.kduel] unless entity {TG} run function bm:{H}/d/won',
                     f'execute if score @s bm.ks matches 0..4 run function bm:{H}/grav', f'execute if score @s bm.ks matches 7 run function bm:{H}/grav',
                     f'execute if score @s bm.ks matches 0 run function bm:{H}/wake'] +
       [f'execute if score @s bm.ks matches {s} if entity @s[tag=bm.k{"guard" if m == "g" else "duel"}] run function bm:{H}/{m}/{f}'
        for m in ('g', 'd') for s, f in ((1, 'fight'), (2, 'slam'), (3, 'spin'), (4, 'reel'))] +
       [f'execute if score @s bm.ks matches 5 run function bm:{H}/fall', f'execute if score @s bm.ks matches 6 run function bm:{H}/g/cool',
        f'execute if score @s bm.ks matches 7 run function bm:{H}/back', f'execute if score @s bm.ks matches 8 run function bm:{H}/settle',
        f'execute if score @s bm.ks matches 0..4 rotated as @s rotated ~ 0 run function bm:{PFX}/place',
        f'execute if score @s bm.ks matches 6..8 rotated as @s rotated ~ 0 run function bm:{PFX}/place',
        'tag @e[type=minecraft:interaction,tag=bm.kpost] remove bm.kpost', 'tag @e[tag=bm.ktgt] remove bm.ktgt', 'tag @a[tag=bm.kfoe] remove bm.kfoe',
        'tag @e[type=minecraft:item_display,tag=bm.ksel] remove bm.ksel', 'tag @s remove bm.kme'])
    # (it has no AI: it falls by itself, and steps - up or down one block at most, never off a ledge)
    fn(f'{H}/grav', [f'execute if block ~ ~-0.1 ~ #minecraft:replaceable positioned ~ ~-0.5 ~ run function bm:{H}/drop'])
    fn(f'{H}/drop', ['execute unless block ~ ~ ~ #minecraft:replaceable align y positioned ~ ~1 ~ run return run tp @s ~ ~ ~', 'tp @s ~ ~ ~'])
    for nm, sp, lim in (('g', 0.12, LEASH), ('d', 0.16, DLEASH), ('h', 0.14, None)):
        cond = f' if entity @e[type=minecraft:interaction,tag=bm.kpost,distance=..{lim}]' if lim else ''
        fn(f'{H}/step_{nm}', [f'execute positioned ^ ^ ^{sp}{yo} {WALK} unless block ~ ~-1 ~ #minecraft:replaceable{cond} run return run tp @s ~ ~ ~ ~ ~'
                              for yo in ('', ' positioned ~ ~1 ~', ' positioned ~ ~-1 ~')])
    walkp = lambda pre: [f'{pre} if score #f bm.rng matches {t} run function bm:{PFX}/pose/walk_{i}' for i, t in enumerate((0, 5, 10, 15))] + \
                        [f'{pre} if score #f bm.rng matches {t} run {snd("entity.iron_golem.step", 0.9, 0.5)}' for t in (0, 10)]
    idlep = lambda pre: [f'{pre} if score #f bm.rng matches 0 run function bm:{PFX}/pose/idle_a', f'{pre} if score #f bm.rng matches 10 run function bm:{PFX}/pose/idle_b']
    tick20 = ['scoreboard players operation #f bm.rng = @s bm.kt', 'scoreboard players operation #f bm.rng %= #20 bm.rng']
    # ---- the waking (as the dungeon's, with no AI to give it)
    fn(f'{H}/wake', [at(1, 'data merge entity @s {Invulnerable:0b}'), at(1, f'function bm:{PFX}/pose/wake_0'),
                     at(1, snd('block.deepslate.break', 1.4, 0.5)), at(1, snd('entity.warden.emerge', 0.8, 1.4))] +
       [at(12, f'execute if entity @s[tag=bm.kh_{k}] run function bm:{PFX}/finish/{k}_live') for k in KN] +
       [at(12, f'execute if entity @s[tag=bm.kh_{k}] run {crumble(k)}') for k in KN] + [at(12, f'execute if entity @s[tag=bm.kh_{k}] run {lit(k)}') for k in KN] +
       [at(12, snd('entity.iron_golem.repair', 1.2, 0.5)), at(22, f'function bm:{PFX}/pose/wake_1'), at(22, snd('item.mace.smash_air', 1.2, 0.6)),
        at(40, f'effect give @s minecraft:resistance infinite {RESIST} true'), at(40, 'execute store result score @s bm.kgh run data get entity @s Health 10'),
        at(40, 'scoreboard players set @s bm.ka 0'), at(40, 'scoreboard players set @s bm.kc 0'), at(40, 'scoreboard players set @s bm.ks 1'),
        at(40, 'scoreboard players set @s bm.kt 0')])

    # ---- the GUARD: monsters within SIGHT of its plinth (nearest the plinth) its foe; players' (and golems', and the world's) blows undone
    fn(f'{H}/g/pre', [f'execute if score @s bm.ks matches 0..4 run function bm:{H}/g/ward',
                      f'execute at {POST} as @e[{MON},distance=..{SIGHT},sort=nearest,limit=1] run tag @s add bm.ktgt'])
    fn(f'{H}/g/ward', ['execute store result score #h bm.rng run data get entity @s Health 10',
                       f'execute if score #h bm.rng < @s bm.kgh unless function bm:{H}/g/bymob store result entity @s Health float 0.1 run scoreboard players get @s bm.kgh',
                       'execute store result score @s bm.kgh run data get entity @s Health 10'])
    fn(f'{H}/g/bymob', ['execute on attacker if entity @s[type=#bm:hostile] run return 1', 'return 0'])
    fn(f'{H}/g/regen', ['execute store result score #h bm.rng run data get entity @s Health 10',
                        f'execute if score #h bm.rng matches {(max(c["hp"] for c in KN.values()) + FLOOR) * 10}.. run return 0',
                        'scoreboard players add #h bm.rng 10', f'execute store result entity @s Health float 0.1 run scoreboard players get #h bm.rng',
                        'execute store result score @s bm.kgh run data get entity @s Health 10'])
    fn(f'{H}/g/idle', [f'execute unless entity @e[type=minecraft:interaction,tag=bm.kpost,distance=..0.8] if entity {POST} facing entity {POST} feet rotated ~ 0 run function bm:{H}/step_h'] +
       walkp('execute unless entity @e[type=minecraft:interaction,tag=bm.kpost,distance=..0.8] if entity ' + POST) +
       idlep('execute if entity @e[type=minecraft:interaction,tag=bm.kpost,distance=..0.8]') +
       ['execute if entity @e[type=minecraft:interaction,tag=bm.kpost,distance=..0.8] if score #f bm.rng matches 0 '
        'rotated as @e[type=minecraft:item_display,tag=bm.knsd,distance=..1.5,sort=nearest,limit=1] run tp @s ~ ~ ~ ~ 0'])
    fn(f'{H}/g/down', ['scoreboard players set @s bm.ks 6', 'scoreboard players set @s bm.kt 0',
                       'execute store result entity @s Health float 1 run attribute @s minecraft:max_health get',
                       'execute store result score @s bm.kgh run data get entity @s Health 10',
                       say('@a[distance=..24]', [T('Brought low, it kneels - stone again. ', 'gray'), T('In a minute it will rise once more.', 'white')])])
    fn(f'{H}/g/cool', [f'execute if score @s bm.kt matches {COOL}.. run return run function bm:{H}/g/rearm',
                       'scoreboard players operation #f bm.rng = @s bm.kt', 'scoreboard players operation #f bm.rng %= #40 bm.rng'] +
       [f'execute if score #f bm.rng matches 0 if entity @s[tag=bm.kh_{k}] run particle minecraft:dust{{color:[{KN[k]["dust"]}],scale:1.0}} ~ ~2.0 ~ 0.3 0.3 0.3 0 4' for k in KN])
    fn(f'{H}/g/rearm', ['scoreboard players set @s bm.ks 0', 'scoreboard players set @s bm.kt 0'])
    # ---- the DUEL: its challenger (bm.pid) its only foe - alive, playing, within REACH
    fn(f'{H}/d/pre', ['scoreboard players operation #kp bm.pid = @s bm.pid', 'execute as @a if score @s bm.pid = #kp bm.pid run tag @s add bm.kfoe',
                      'scoreboard players set #fh bm.rng 0',
                      f'execute as @a[tag=bm.kfoe,distance=..{REACH},{FOES},limit=1] store result score #fh bm.rng run data get entity @s Health 10',
                      f'execute if score #fh bm.rng matches 1.. run tag @a[tag=bm.kfoe,distance=..{REACH},{FOES}] add bm.ktgt'])
    fn(f'{H}/d/won', [say('@a[tag=bm.kfoe]', [T('It has bested you. ', 'red', bold=True), T('It walks back to its plinth - stone again.', 'gray')]),
                      f'function bm:{H}/homeward'])
    fn(f'{H}/d/beaten', [title('@a[distance=..32]', 'actionbar', [T('It falls - ', 'gold', bold=True), T('and its statue is yours again.', 'gray')]),
                         'xp add @a[tag=bm.kfoe] 10 points'] +
       [f'execute if entity @s[tag=bm.kh_{k}] run loot spawn ~ ~1 ~ loot bm:items/knight_statue_{k}' for k in KN] +
       ['particle minecraft:totem_of_undying ~ ~1.5 ~ 0.6 0.8 0.6 0.3 40', 'playsound minecraft:block.amethyst_block.resonate player @a[distance=..24] ~ ~ ~ 1 0.7',
        f'execute as @e[type=minecraft:interaction,tag=bm.knst] if score @s bm.kid = #me bm.kid at @s run function bm:{H}/empty',
        f'function bm:{H}/dismiss'])
    fn(f'{H}/empty', ['kill @e[type=minecraft:item_display,tag=bm.knsd,distance=..0.6,sort=nearest,limit=1]',
                      'particle minecraft:poof ~ ~0.4 ~ 0.3 0.2 0.3 0.02 8', 'kill @s'])

    # ---- the fight, two ways: the guard's (monsters; its leash) and the duel's (the challenger alone)
    for m, lim, foes in (('g', LEASH, lambda r: f'@e[{MON},{r}]'), ('d', DLEASH, lambda r: f'@a[tag=bm.ktgt,{r}]')):
        P = f'{H}/{m}'
        leash = f' if entity @e[type=minecraft:interaction,tag=bm.kpost,distance=..{lim}]'
        near = '@e[tag=bm.ktgt,distance=..3]'
        face = f'execute facing entity {TG} feet run tp @s ~ ~ ~ ~ 0'
        fn(f'{P}/fight', ['scoreboard players add @s bm.ka 1'] + tick20 +
           [f'execute unless entity {TG} run return run ' + (f'function bm:{H}/g/idle' if m == 'g' else 'scoreboard players set @s bm.ka 0'), face,
            f'execute unless entity {near} facing entity {TG} feet rotated ~ 0 run function bm:{H}/step_{m}'] +
           idlep(f'execute if entity {near}') + walkp(f'execute unless entity {near}') +
           [f'execute if score @s bm.ka matches {EVERY}.. if score @s bm.kc matches 0 if entity @e[tag=bm.ktgt,distance=..4.5] run return run function bm:{P}/slam0',
            f'execute if score @s bm.ka matches {EVERY}.. if score @s bm.kc matches 1 if entity @e[tag=bm.ktgt,distance=..6] run return run function bm:{P}/spin0'])
        fn(f'{P}/slam0', ['scoreboard players set @s bm.ks 2', 'scoreboard players set @s bm.kt 0', 'scoreboard players set @s bm.kc 1', face,
                          f'function bm:{PFX}/pose/swing_0', snd('entity.ravager.attack', 1.2, 0.5), snd('block.chain.break', 1, 0.5)])
        fn(f'{P}/slam', [at(WIND, f'function bm:{PFX}/pose/swing_1')] +
           [at(HIT, f'execute if entity @s[tag=bm.kh_{k}] run function bm:{P}/slam_{k}') for k in KN] +
           [at(BACK - 8, f'function bm:{PFX}/pose/idle_a'), at(BACK, 'scoreboard players set @s bm.ka 0'), at(BACK, 'scoreboard players set @s bm.ks 1')])
        fn(f'{P}/spin0', ['scoreboard players set @s bm.ks 3', 'scoreboard players set @s bm.kt 0', 'scoreboard players set @s bm.kc 0', face,
                          f'function bm:{PFX}/pose/spin_0', snd('entity.player.attack.sweep', 1.4, 0.4), snd('entity.ravager.roar', 0.8, 0.8)])
        fn(f'{P}/spin', ['scoreboard players operation #f bm.rng = @s bm.kt', 'scoreboard players operation #f bm.rng %= #10 bm.rng',
                         f'execute if score @s bm.kt matches {SPIN0}..{SPIN1} run tp @s ~ ~ ~ ~36 ~',
                         f'execute if score @s bm.kt matches {SPIN0}..{SPIN1} if entity {TG} facing entity {TG} feet rotated ~ 0 positioned ^ ^ ^0.12 '
                         f'{WALK}{leash} run tp @s ~ ~ ~',
                         f'execute if score @s bm.kt matches {SPIN0}..{SPIN1} if score #f bm.rng matches 0 run function bm:{PFX}/pose/spin_1',
                         f'execute if score @s bm.kt matches {SPIN0}..{SPIN1} if score #f bm.rng matches 5 run function bm:{PFX}/pose/spin_0',
                         'scoreboard players operation #g bm.rng = @s bm.kt', 'scoreboard players operation #g bm.rng %= #8 bm.rng'] +
           [f'execute if score @s bm.kt matches {SPIN0}..{SPIN1} if score #g bm.rng matches 0 if entity @s[tag=bm.kh_{k}] run function bm:{P}/whirl_{k}' for k in KN] +
           [at(SPIN1 + 1, f'function bm:{PFX}/pose/stagger'), at(SPIN1 + 1, 'effect clear @s minecraft:resistance'),
            at(SPIN1 + 1, snd('entity.iron_golem.damage', 1.2, 0.5))] +
           ([at(SPIN1 + 1, title('@a[tag=bm.kfoe]', 'actionbar', T('It reels, dizzy - its guard is down. Strike now!', 'gold', bold=True)))] if m == 'd' else []) +
           [at(SPIN1 + 1, 'scoreboard players set @s bm.ks 4'), at(SPIN1 + 1, 'scoreboard players set @s bm.kt 0')])
        fn(f'{P}/reel', ['execute if score @s bm.kt matches 1.. run particle minecraft:crit ~ ~3.1 ~ 0.3 0.1 0.3 0.1 2',
                         at(REEL, f'effect give @s minecraft:resistance infinite {RESIST} true'), at(REEL, f'function bm:{PFX}/pose/idle_a'),
                         at(REEL, 'scoreboard players set @s bm.ka 0'), at(REEL, 'scoreboard players set @s bm.ks 1')])
        for k, c in KN.items():
            fn(f'{P}/slam_{k}', [f'execute positioned ^ ^ ^2 as {foes("distance=..2.6")} run damage @s {c["slam"]} minecraft:mob_attack by {ME}',
                                 f'execute positioned ^ ^ ^2 as {foes("distance=2.6..5")} run damage @s {c["wave"]} minecraft:mob_attack by {ME}',
                                 'execute positioned ^ ^ ^2 run particle minecraft:explosion ~ ~0.2 ~ 0.6 0.1 0.6 0 3',
                                 f'execute positioned ^ ^ ^2 run particle minecraft:block{{block_state:"{c["stone"]}"}} ~ ~0.2 ~ 1.4 0.1 1.4 0.2 80',
                                 f'execute positioned ^ ^ ^2 run particle minecraft:dust{{color:[{c["dust"]}],scale:2.0}} ~ ~0.3 ~ 1.8 0.1 1.8 0 40',
                                 snd('item.mace.smash_ground_heavy', 1.6, 0.6), snd('entity.generic.explode', 0.8, 0.7)])
            fn(f'{P}/whirl_{k}', [f'execute as {foes("distance=..3.8")} run damage @s {c["spin"]} minecraft:mob_attack by {ME}',
                                  'particle minecraft:sweep_attack ~ ~1.2 ~ 1.6 0.2 1.6 0 6',
                                  f'particle minecraft:dust{{color:[{c["dust"]}],scale:1.4}} ~ ~1.2 ~ 2 0.2 2 0 16',
                                  snd('entity.player.attack.sweep', 1.0, 0.6)])

    # ---- the fall (as the dungeon's: to one knee, slumped, stone) - then a guard waits; a dueller is beaten
    fn(f'{H}/fall', [at(25, f'function bm:{PFX}/pose/death_1'), at(25, snd('block.chain.fall', 1, 0.5))] +
       [at(45, f'execute if entity @s[tag=bm.kh_{k}] run function bm:{PFX}/finish/{k}_stone') for k in KN] +
       [at(45, f'execute if entity @s[tag=bm.kh_{k}] run {crumble(k)}') for k in KN] +
       [at(45, snd('block.deepslate.place', 1.4, 0.5)), at(45, snd('block.stone.break', 1.2, 0.6)),
        at(60, f'execute if entity @s[tag=bm.kguard] run function bm:{H}/g/down'),
        at(60, f'execute if entity @s[tag=bm.kduel] run function bm:{H}/d/beaten')])
    # ---- home: walk back to the plinth, face as it was set up, stone
    fn(f'{H}/back', tick20 + [f'execute unless entity {POST} run return run function bm:{H}/dismiss',
                              f'execute if entity @e[type=minecraft:interaction,tag=bm.kpost,distance=..0.7] run return run function bm:{H}/arrive',
                              f'execute if score @s bm.kt matches {HOMEWARD}.. run return run function bm:{H}/arrive',
                              f'execute facing entity {POST} feet rotated ~ 0 run function bm:{H}/step_h'] + walkp('execute'))
    fn(f'{H}/arrive', [f'execute at {POST} run tp @s ~ ~ ~',
                       f'execute at {POST} rotated as @e[type=minecraft:item_display,tag=bm.knsd,distance=..0.8,sort=nearest,limit=1] run tp @s ~ ~ ~ ~ 0',
                       'scoreboard players set @s bm.ks 8', 'scoreboard players set @s bm.kt 0'])
    fn(f'{H}/settle', [at(1, f'function bm:{PFX}/pose/statue'), at(1, snd('block.chain.place', 1, 0.5))] +
       [at(14, f'execute if entity @s[tag=bm.kh_{k}] run function bm:{PFX}/finish/{k}_stone') for k in KN] +
       [at(14, f'execute if entity @s[tag=bm.kh_{k}] run {crumble(k)}') for k in KN] + [at(28, f'function bm:{H}/stone')])

    # ------------------------------------------------------------------ each second: still whole, still posted, (a guard) mending, (a duel) its bar
    second.append(f'execute as @e[type=minecraft:husk,tag=bm.khome] at @s run function bm:{H}/sec')
    fn(f'{H}/sec', ['scoreboard players operation #me bm.kid = @s bm.kid', 'scoreboard players set #pf bm.rng 0',
                    'execute as @e[type=minecraft:interaction,tag=bm.knst,distance=..48,scores={bm.kgm=1..}] if score @s bm.kid = #me bm.kid run scoreboard players set #pf bm.rng 1',
                    'execute if score #pf bm.rng matches 0 run scoreboard players add @s bm.kmiss 1', 'execute if score #pf bm.rng matches 1 run scoreboard players set @s bm.kmiss 0',
                    f'execute if score @s bm.kmiss matches 5.. run return run function bm:{H}/dismiss',
                    f'function bm:{PFX}/mine', 'execute store result score #np bm.rng if entity @e[type=minecraft:item_display,tag=bm.ksel]',
                    f'execute unless score #np bm.rng matches {len(A.PARTS)} run function bm:{H}/rerig',
                    'tag @e[type=minecraft:item_display,tag=bm.ksel] remove bm.ksel',
                    f'execute if entity @s[tag=bm.kguard] if score @s bm.ks matches 0..4 run function bm:{H}/g/regen'] +
       [f'execute if score @s bm.kbs matches {i} run function bm:{H}/d/bar{i}' for i in range(1, DUELS + 1)])
    # (a part lost - or doubled, its chunk loaded late: the rig built afresh, in the finish and pose of the moment)
    fn(f'{H}/rerig', ['kill @e[type=minecraft:item_display,tag=bm.ksel]'] +
       [f'execute if entity @s[tag=bm.kh_{k}] rotated as @s rotated ~ 0 run function bm:{PFX}/rig/{k}' for k in KN] +
       ['scoreboard players operation @e[type=minecraft:item_display,tag=bm.knew,distance=..1] bm.kid = @s bm.kid',
        'tag @e[type=minecraft:item_display,tag=bm.knew,distance=..1] add bm.ksel', 'tag @e[tag=bm.knew] remove bm.knew'] +
       [f'execute if entity @s[tag=bm.kh_{k}] if score @s bm.ks matches 1..5 run function bm:{PFX}/finish/{k}_live' for k in KN] +
       [f'execute rotated as @s rotated ~ 0 run function bm:{PFX}/place',
        f'execute if score @s bm.ks matches 5..6 run function bm:{PFX}/pose/death_1',
        f'execute if score @s bm.ks matches 0 run function bm:{PFX}/pose/statue',
        f'execute if score @s bm.ks matches 8 run function bm:{PFX}/pose/statue',
        f'execute if score @s bm.ks matches 1..4 run function bm:{PFX}/pose/idle_a',
        f'execute if score @s bm.ks matches 7 run function bm:{PFX}/pose/idle_a'])
    # (the statue's side: awake, but its knight nowhere near for 5 s - killed, lost, the world's peace: stone again on its plinth)
    second.append(f'execute as @e[type=minecraft:interaction,tag=bm.knst,scores={{bm.kgm=1..}}] at @s run function bm:{H}/psec')
    fn(f'{H}/psec', ['scoreboard players operation #me bm.kid = @s bm.kid', 'scoreboard players set #f bm.rng 0',
                     'execute as @e[type=minecraft:husk,tag=bm.khome,distance=..48] if score @s bm.kid = #me bm.kid run scoreboard players set #f bm.rng 1',
                     'execute if score #f bm.rng matches 1 run return run scoreboard players set @s bm.kmiss 0',
                     'scoreboard players add @s bm.kmiss 1', f'execute if score @s bm.kmiss matches 5.. run function bm:{H}/restore'])
    fn('admin/knights/home', [f'execute as @e[type=minecraft:husk,tag=bm.khome] at @s run function bm:{H}/stone'])

def rp(R):
    A.rp(R)

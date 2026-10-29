"""2.99a: THE DREAD MIRE - a lesser manifestation of the Dread, loose in the world in hard mode (mire_art draws it).

WHERE      any of the three dimensions, rarely, in the dark: now and then a hostile mob rising naturally (mobs/init) in hard mode
           comes up as a Mire instead - where the light is low (4 or less), outside a Golden Cross's ground, never near another
           Mire, never in the vault or the Hollow Throne. None rise once the Dread Sovereign has fallen (#dfell) - until the
           Dread Ember kindles the nights again; those still about melt away.
DORMANT    a puddle of shimmering reddish-black shadow, 4 blocks across, faintly moving: it creeps towards anyone within 24
           blocks, bubbles and whispers. It can't be hurt like this. Daylight or a bright light on it and it seeps away.
RISEN      anyone (not in creative or spectator) within 10 blocks and it rises: a worm-like black mass ~5 blocks tall, a blind
           ring-mouth glowing red inside, four tentacles, dripping black goo. It is rooted where it rose. Every ~2.5 s:
  GRAB     at 3.5..8 blocks: a tentacle darts out and drags you in (Slowness, pulled towards it) and squeezes (6).
  STAB     within 4.5 blocks: two tentacles cocked back and driven down 4 blocks ahead (10 there).
  THE CROSS  a Golden Cross within 15 blocks (phase181's) and it shrieks, recoils and sinks - and the puddle slips away from
           the cross; it will not rise in the cross's ground. Nobody near for 10 s: it sinks back down to wait.
ITS DEATH  it collapses into the puddle and dissolves, leaving 1-3 SHADOW REMNANTS.
SHADOW MUSK   4 Shadow Remnants in hand, used: kneaded into a vial of Shadow Musk. Drink it: for 5 minutes the Stalkers of a
           Dread Night lose your scent - none rises for you, those hunting you lose you, standing still calls nothing."""
from items import T, item, TOTEM, consumable
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D as Dd
import rigfol as RF
import mire_art as A

PFX = 'p246'
NAME, COL = 'Dread Mire', '#b0182a'
HP, FLOOR = 150, 100
SCALE = getattr(A, 'SCALE', 1.0)
ROLL = 300                          # (1 in this many natural hostile spawns in hard mode comes up a Mire)
APART = 96                          # (never within this of another)
WAKE, LEAVE, CREEP = 10, 20, 24     # (rises for anyone within WAKE; sinks with nobody within LEAVE for 10 s; creeps towards within CREEP)
GRAB_DMG, STAB_DMG = 6, 10
EVERY = 50
MUSK = 300                          # (seconds the musk masks you)
RISEN_SC, DORMANT_SC = 2.4, 1.0     # (the host husk's scale: a 4.7-block hitbox risen; small, invulnerable, dormant)
DUR = {'dormant': 10, 'rise_0': 10, 'rise_1': 12, 'rise_2': 12, 'idle_a': 20, 'idle_b': 20, 'shriek': 6, 'grab_0': 3, 'grab_1': 8,
       'stab_0': 10, 'stab_1': 3, 'recoil': 5, 'sink_0': 10, 'death_0': 12, 'death_1': 20}
GLOW = tuple(getattr(A, 'GLOW', ()))
SND = getattr(A, 'SOUNDS', {})      # name -> sound id (the art's own, else vanilla below)
VAN = {'bubble': ('block.bubble_column.whirlpool_ambient', 0.35), 'rise': ('entity.warden.emerge', 0.6), 'idle': ('entity.warden.ambient', 0.5),
       'lash': ('entity.warden.attack_impact', 1.3), 'shriek': ('block.sculk_shrieker.shriek', 0.6), 'death': ('entity.warden.death', 0.7)}
ME = '@e[type=minecraft:husk,tag=bm.mme,limit=1]'
FOES = 'gamemode=!spectator,gamemode=!creative'
sel = lambda p: f'@e[type=minecraft:item_display,tag=bm.msel,tag=bm.mr_{p}]'

item('shadow_remnant', TOTEM, 'Shadow Remnant', COL,
     ['What is left of a Dread Mire. It moves when', 'you are not looking.', ('4 in hand, used: knead them into Shadow Musk.', 'blue')],
     model='bm:shadow_remnant', stack=64, cat='magic', comps=hold('none'))
HOLD['shadow_remnant'] = f'bm:{PFX}/knead'
item('shadow_musk', TOTEM, 'Shadow Musk', COL,
     ['Black, cold, and it smells of nothing at all.', ('Drink: for 5 minutes the Stalkers', 'blue'), ('of a Dread Night lose your scent.', 'blue')],
     model='bm:shadow_musk', stack=16, cat='magic',
     comps={'minecraft:consumable': consumable(1.6, 'drink', 'minecraft:entity.generic.drink', False)})


def snd(name, v=1.0, p=None, who='@a[distance=..32]'):
    sid, pv = (SND[name], 1.0) if name in SND else ('minecraft:' + VAN[name][0], VAN[name][1])
    return f'playsound {sid} hostile {who} ~ ~ ~ {v} {p if p is not None else pv}'


def generate(G):
    fn, title, give = G.fn, G.title, G.give
    tick, second = G.FUNCS['tick'], G.FUNCS['loop/second']
    objs = ['bm.mid', 'bm.ms', 'bm.mt', 'bm.ma', 'bm.mc', 'bm.mq', 'bm.musk']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + ['scoreboard players set #4 bm.rng 4', 'scoreboard players set #20 bm.rng 20']
    G.OBJECTIVES += objs
    at = lambda t, cmd: f'execute if score @s bm.mt matches {t} {cmd[8:]}' if cmd.startswith('execute ') else f'execute if score @s bm.mt matches {t} run {cmd}'
    G.wjson('bm/predicate/p246/dark.json', {'condition': 'minecraft:location_check', 'predicate': {'light': {'light': {'max': 4}}}})
    G.wjson('bm/predicate/p246/bright.json', {'condition': 'minecraft:location_check', 'predicate': {'light': {'light': {'min': 12}}}})

    # ================================================================== the rig
    for name, pz in A.POSES.items():
        fn(f'{PFX}/pose/{name}', RF.pose(A, pz, SCALE, DUR.get(name, 8), sel))
    fn(f'{PFX}/place', RF.place(A, SCALE / 16, sel))
    rig = []
    for p in A.PARTS:
        extra = dict(view_range=F(4.0))
        if p in GLOW: extra['brightness'] = {'block': Int(15), 'sky': Int(15)}
        rig.append(f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, ["bm.mr", f"bm.mr_{p}", "bm.mnew"], SCALE, model=A.model_id(p), extra=extra)}')
    fn(f'{PFX}/rig', rig)
    fn(f'{PFX}/mine', ['scoreboard players operation #me bm.mid = @s bm.mid',
                       'execute as @e[type=minecraft:item_display,tag=bm.mr] if score @s bm.mid = #me bm.mid run tag @s add bm.msel'])

    # ================================================================== rising out of the world: a natural spawn, now and then
    host = {'Tags': ['bm.mire', 'bm.seen', 'bm.mnewh'], 'NoAI': B(1), 'Silent': B(1), 'PersistenceRequired': B(0), 'Invulnerable': B(1),
            'CustomName': T(NAME, COL), 'DeathLootTable': 'minecraft:empty', 'CanPickUpLoot': B(0),
            'attributes': [{'id': 'minecraft:max_health', 'base': Dd(HP + FLOOR)}, {'id': 'minecraft:scale', 'base': Dd(DORMANT_SC)},
                           {'id': 'minecraft:knockback_resistance', 'base': Dd(1.0)}, {'id': 'minecraft:armor', 'base': Dd(6)}],
            'Health': F(HP + FLOOR),
            'active_effects': [{'id': 'minecraft:invisibility', 'duration': Int(-1), 'amplifier': B(0), 'show_particles': B(0)},
                               {'id': 'minecraft:fire_resistance', 'duration': Int(-1), 'amplifier': B(0), 'show_particles': B(0)}]}
    fn(f'{PFX}/roll', ['execute store result score #r bm.rng run random value 1..' + str(ROLL), 'execute unless score #r bm.rng matches 1 run return 0',
                       'execute unless predicate bm:p246/dark run return 0',
                       f'execute if entity @e[type=minecraft:husk,tag=bm.mire,distance=..{APART}] run return 0',
                       'execute if function bm:p181/in_cross run return 0',
                       'execute unless block ~ ~-1 ~ #minecraft:replaceable if block ~ ~ ~ #minecraft:replaceable run function bm:p246/spawn',
                       'execute unless entity @e[type=minecraft:husk,tag=bm.mire,distance=..1] run return 0', 'tp @s ~ -400 ~', 'kill @s', 'return 1'])
    fn(f'{PFX}/spawn', [f'summon minecraft:husk ~ ~ ~ {snbt(host)}',
                        'scoreboard players add #mid bm.mid 1',
                        'execute as @e[type=minecraft:husk,tag=bm.mnewh,distance=..1] run function bm:p246/spawn1'])
    fn(f'{PFX}/spawn1', ['scoreboard players operation @s bm.mid = #mid bm.mid', 'scoreboard players set @s bm.ms 0', 'scoreboard players set @s bm.mt 0',
                         'execute store result entity @s Rotation[0] float 1 run random value 0..359',
                         f'execute at @s rotated as @s rotated ~ 0 run function bm:{PFX}/rig',
                         'scoreboard players operation @e[type=minecraft:item_display,tag=bm.mnew,distance=..1] bm.mid = @s bm.mid',
                         'tag @e[type=minecraft:item_display,tag=bm.mnew,distance=..1] remove bm.mnew',
                         f'function bm:{PFX}/mine', f'execute at @s rotated as @s rotated ~ 0 run function bm:{PFX}/place', f'function bm:{PFX}/pose/dormant',
                         'tag @e[type=minecraft:item_display,tag=bm.msel] remove bm.msel', 'tag @s remove bm.mnewh'])
    skip = {'ghast', 'phantom', 'drowned', 'shulker', 'blaze', 'breeze', 'pillager', 'vindicator', 'piglin_brute'}
    for t in list(G.ARMORED) + list(G.UNARMORED):
        if t in skip or f'mobs/init/{t}' not in G.FUNCS: continue
        G.FUNCS[f'mobs/init/{t}'].insert(0, 'execute if score #hard bm.cfg matches 1 unless score #dfell bm.cfg matches 1 unless dimension bm:gutter '
                                            f'unless dimension bm:hollow_throne if function bm:{PFX}/roll run return 0')

    # ================================================================== each second: the puddle's patience, the cross, the light, the fallen Dread
    second.append(f'execute as @e[type=minecraft:husk,tag=bm.mire] at @s run function bm:{PFX}/sec')
    fn(f'{PFX}/sec', ['execute if score #dfell bm.cfg matches 1 unless score @s bm.ms matches 7 run return run function bm:p246/melt',
                      f'execute if score @s bm.ms matches 0 run function bm:{PFX}/sec0',
                      f'execute if score @s bm.ms matches 2 run function bm:{PFX}/sec2'])
    fn(f'{PFX}/sec0', ['execute if predicate bm:p246/bright run return run function bm:p246/melt',
                       'execute if function bm:p181/in_cross run return run function bm:p246/flee',
                       f'execute if entity @a[distance=..{WAKE},{FOES}] run return run function bm:{PFX}/rise0',
                       f'execute facing entity @p[distance=..{CREEP},{FOES}] feet rotated ~ 0 positioned ^ ^ ^0.35 unless block ~ ~-1 ~ #minecraft:replaceable '
                       'if block ~ ~ ~ #minecraft:replaceable run tp @s ~ ~ ~',
                       'execute store result score #r bm.rng run random value 0..3', 'execute if score #r bm.rng matches 0 run ' + snd('bubble', 0.7),
                       'particle minecraft:dust{color:[0.45,0.02,0.06],scale:1.3} ~ ~0.1 ~ 1.4 0.02 1.4 0 10',
                       'particle minecraft:smoke ~ ~0.1 ~ 1.2 0.02 1.2 0 4'])
    fn(f'{PFX}/sec2', ['execute if function bm:p181/in_cross run return run function bm:p246/recoil0',
                       f'execute if entity @a[distance=..{LEAVE},{FOES}] run scoreboard players set @s bm.mq 0',
                       f'execute unless entity @a[distance=..{LEAVE},{FOES}] run scoreboard players add @s bm.mq 1',
                       'execute if score @s bm.mq matches 10.. run function bm:p246/sink0',
                       'execute store result score #r bm.rng run random value 0..4', 'execute if score #r bm.rng matches 0 run ' + snd('idle', 1.2)])
    fn(f'{PFX}/flee', ['execute facing entity @e[type=minecraft:marker,tag=bm.gcm,sort=nearest,limit=1] feet rotated ~ 0 positioned ^ ^ ^-0.8 '
                       'unless block ~ ~-1 ~ #minecraft:replaceable if block ~ ~ ~ #minecraft:replaceable run tp @s ~ ~ ~',
                       'particle minecraft:smoke ~ ~0.2 ~ 1 0.1 1 0.01 12'])
    fn(f'{PFX}/melt', ['particle minecraft:smoke ~ ~0.3 ~ 1.4 0.2 1.4 0.02 40', 'particle minecraft:squid_ink ~ ~0.3 ~ 1.2 0.2 1.2 0.05 20', snd('death', 0.6, 1.4),
                       'scoreboard players operation #me bm.mid = @s bm.mid', 'execute as @e[type=minecraft:item_display,tag=bm.mr] if score @s bm.mid = #me bm.mid run kill @s',
                       'tp @s ~ -400 ~', 'kill @s'])

    # ================================================================== each tick, each Mire awake
    tick.append(f'execute as @e[type=minecraft:husk,tag=bm.mire,scores={{bm.ms=1..}}] at @s run function bm:{PFX}/tick')
    fn(f'{PFX}/tick', ['scoreboard players add @s bm.mt 1', 'tag @s add bm.mme', f'function bm:{PFX}/mine',
                       'execute if score @s bm.ms matches 2..5 store result score #h bm.rng run data get entity @s Health',
                       f'execute if score @s bm.ms matches 2..5 if score #h bm.rng matches ..{FLOOR} run function bm:{PFX}/die0',
                       f'execute if score @s bm.ms matches 1 run function bm:{PFX}/s/rise',
                       f'execute if score @s bm.ms matches 2 run function bm:{PFX}/s/fight',
                       f'execute if score @s bm.ms matches 3 run function bm:{PFX}/s/grab',
                       f'execute if score @s bm.ms matches 4 run function bm:{PFX}/s/stab',
                       f'execute if score @s bm.ms matches 5 run function bm:{PFX}/s/recoil',
                       f'execute if score @s bm.ms matches 6 run function bm:{PFX}/s/sink',
                       f'execute if score @s bm.ms matches 7 run function bm:{PFX}/s/die',
                       f'execute if score @s bm.ms matches 2..5 run function bm:{PFX}/drip',
                       f'execute rotated as @s rotated ~ 0 run function bm:{PFX}/place',
                       'tag @e[type=minecraft:item_display,tag=bm.msel] remove bm.msel', 'tag @s remove bm.mme'])
    fn(f'{PFX}/drip', ['scoreboard players operation #f bm.rng = @s bm.mt', 'scoreboard players operation #f bm.rng %= #4 bm.rng',
                       'execute if score #f bm.rng matches 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ~ ~3.2 ~ 0.7 1.2 0.7 0 3',
                       'execute if score #f bm.rng matches 2 run particle minecraft:squid_ink ~ ~2.6 ~ 0.6 1 0.6 0.02 1',
                       'execute if score #f bm.rng matches 0 run particle minecraft:dust{color:[0.5,0.02,0.06],scale:1.1} ~ ~0.2 ~ 1.3 0.05 1.3 0 3'])
    face = f'execute facing entity @p[distance=..16,{FOES}] feet run tp @s ~ ~ ~ ~ 0'
    # ---- rising
    fn(f'{PFX}/rise0', ['scoreboard players set @s bm.ms 1', 'scoreboard players set @s bm.mt 0', 'scoreboard players set @s bm.mq 0', face])
    fn(f'{PFX}/s/rise', [at(1, f'function bm:{PFX}/pose/rise_0'), at(1, snd('rise', 1.4)), at(1, 'particle minecraft:squid_ink ~ ~0.4 ~ 1.2 0.2 1.2 0.08 30'),
                         at(12, f'function bm:{PFX}/pose/rise_1'),
                         at(24, f'function bm:{PFX}/pose/rise_2'), at(24, snd('shriek', 1.0, 0.7)),
                         at(24, f'attribute @s minecraft:scale base set {RISEN_SC}'), at(24, 'data merge entity @s {Invulnerable:0b}'),
                         at(40, 'scoreboard players set @s bm.ms 2'), at(40, 'scoreboard players set @s bm.mt 0'), at(40, 'scoreboard players set @s bm.ma 30')])
    # ---- risen: swaying, facing its prey; every EVERY ticks a grab or a stab
    fn(f'{PFX}/s/fight', ['scoreboard players add @s bm.ma 1',
                          'scoreboard players operation #f bm.rng = @s bm.mt', 'scoreboard players operation #f bm.rng %= #20 bm.rng',
                          'scoreboard players operation #g bm.rng = @s bm.mt', 'scoreboard players operation #g bm.rng %= #40 bm.rng',
                          f'execute if score #g bm.rng matches 0 run function bm:{PFX}/pose/idle_a', f'execute if score #g bm.rng matches 20 run function bm:{PFX}/pose/idle_b',
                          f'execute if score #f bm.rng matches 0 if entity @p[distance=..16,{FOES}] run {face}',
                          f'execute if score @s bm.ma matches {EVERY}.. if entity @a[distance=..4.5,{FOES}] run return run function bm:{PFX}/stab0',
                          f'execute if score @s bm.ma matches {EVERY}.. if entity @a[distance=3.5..8,{FOES}] run return run function bm:{PFX}/grab0'])
    fn(f'{PFX}/grab0', ['scoreboard players set @s bm.ms 3', 'scoreboard players set @s bm.mt 0', face, f'function bm:{PFX}/pose/grab_0', snd('lash', 1.4)])
    fn(f'{PFX}/s/grab', [at(4, f'execute positioned ^ ^1.4 ^4 as @p[distance=..3.5,{FOES}] run tag @s add bm.mgrab'),
                         at(4, f'execute positioned ^ ^1.4 ^4 run particle minecraft:squid_ink ~ ~ ~ 0.6 0.4 0.6 0.1 20'),
                         at(5, f'execute as @a[tag=bm.mgrab] run {title("@s", "actionbar", T("A tentacle has you!", COL, bold=True))}'),
                         at(5, 'effect give @a[tag=bm.mgrab] minecraft:slowness 2 4 true'),
                         at(10, f'function bm:{PFX}/pose/grab_1'),
                         f'execute if score @s bm.mt matches 6..30 as @a[tag=bm.mgrab,distance=2.6..] at @s facing entity {ME} feet positioned ^ ^ ^0.3 run tp @s ~ ~ ~',
                         f'execute if score @s bm.mt matches 6..30 as @a[tag=bm.mgrab] at @s run particle minecraft:falling_dust{{block_state:"minecraft:black_concrete"}} ~ ~1 ~ 0.3 0.5 0.3 0 2',
                         at(30, f'execute as @a[tag=bm.mgrab] run damage @s {GRAB_DMG} minecraft:mob_attack by {ME}'),
                         at(30, snd('lash', 1.0, 0.6)), at(31, 'tag @a remove bm.mgrab'),
                         at(40, 'scoreboard players set @s bm.ms 2'), at(40, 'scoreboard players set @s bm.ma 0'), at(40, 'scoreboard players set @s bm.mt 0')])
    fn(f'{PFX}/stab0', ['scoreboard players set @s bm.ms 4', 'scoreboard players set @s bm.mt 0', face, f'function bm:{PFX}/pose/stab_0', snd('idle', 1.4, 0.6)])
    fn(f'{PFX}/s/stab', [at(14, f'function bm:{PFX}/pose/stab_1'), at(15, snd('lash', 1.6, 0.8)),
                         at(17, f'execute positioned ^ ^ ^3.5 as @a[distance=..2.4,{FOES}] run damage @s {STAB_DMG} minecraft:mob_attack by {ME}'),
                         at(17, 'execute positioned ^ ^ ^3.5 run particle minecraft:squid_ink ~ ~0.3 ~ 0.8 0.2 0.8 0.1 30'),
                         at(17, 'execute positioned ^ ^ ^3.5 run particle minecraft:dust{color:[0.6,0.02,0.08],scale:1.6} ~ ~0.3 ~ 1 0.1 1 0 20'),
                         at(32, 'scoreboard players set @s bm.ms 2'), at(32, 'scoreboard players set @s bm.ma 0'), at(32, 'scoreboard players set @s bm.mt 0')])
    # ---- the cross: a shriek, a recoil, down it goes
    fn(f'{PFX}/recoil0', ['scoreboard players set @s bm.ms 5', 'scoreboard players set @s bm.mt 0', f'function bm:{PFX}/pose/recoil', snd('shriek', 1.6),
                          'tag @a remove bm.mgrab', 'particle minecraft:end_rod ~ ~3 ~ 1 1.5 1 0.05 20'])
    fn(f'{PFX}/s/recoil', [at(20, f'function bm:{PFX}/sink0')])
    fn(f'{PFX}/sink0', ['scoreboard players set @s bm.ms 6', 'scoreboard players set @s bm.mt 0', f'function bm:{PFX}/pose/sink_0', snd('rise', 1.0, 1.3)])
    fn(f'{PFX}/s/sink', [at(12, f'function bm:{PFX}/pose/dormant'), at(12, f'attribute @s minecraft:scale base set {DORMANT_SC}'),
                         at(12, 'data merge entity @s {Invulnerable:1b}'),
                         at(24, 'scoreboard players set @s bm.ms 0'), at(24, 'scoreboard players set @s bm.mt 0'), at(24, 'scoreboard players set @s bm.mq 0')])
    # ---- its death: collapsing, melted, gone - its remnants left behind
    fn(f'{PFX}/die0', ['scoreboard players set @s bm.ms 7', 'scoreboard players set @s bm.mt 0', 'data merge entity @s {Invulnerable:1b}',
                       'tag @a remove bm.mgrab', f'function bm:{PFX}/pose/death_0', snd('death', 1.6), snd('shriek', 1.0, 0.5)])
    fn(f'{PFX}/s/die', [at(15, f'function bm:{PFX}/pose/death_1'), at(15, 'particle minecraft:squid_ink ~ ~1 ~ 1.4 0.6 1.4 0.1 60'),
                        at(50, 'particle minecraft:smoke ~ ~0.5 ~ 1.5 0.3 1.5 0.02 60'),
                        at(50, 'loot spawn ~ ~0.5 ~ loot bm:p246/remnants'), at(50, 'summon minecraft:experience_orb ~ ~0.5 ~ {Value:30}'),
                        at(50, 'execute as @e[type=minecraft:item_display,tag=bm.msel] run kill @s'), at(50, 'tp @s ~ -400 ~'), at(50, 'kill @s')])
    G.wjson('bm/loot_table/p246/remnants.json', {'pools': [{'rolls': 1, 'entries': [G.loot_entry('shadow_remnant', G.uni(1, 3))]}]})

    # ================================================================== the remnants kneaded; the musk drunk; the Stalkers lose your scent
    fn(f'{PFX}/knead', ['execute store result score #n bm.rng run clear @s *[minecraft:custom_data~{bm:"shadow_remnant"}] 0',
                        'execute if score #n bm.rng matches ..3 run return run ' + title('@s', 'actionbar', T('Four Shadow Remnants knead into a vial of Shadow Musk.', 'gray')),
                        'clear @s *[minecraft:custom_data~{bm:"shadow_remnant"}] 4', give('shadow_musk'),
                        'playsound minecraft:block.honey_block.slide player @s ~ ~ ~ 1 0.6', 'playsound minecraft:item.bottle.fill player @s ~ ~ ~ 1 0.7',
                        title('@s', 'actionbar', T('You knead the remnants into a vial of Shadow Musk.', COL))])
    G.consume_adv('shadow_musk', f'bm:{PFX}/musk')
    fn(f'{PFX}/musk', ['advancement revoke @s only bm:consume/shadow_musk', f'scoreboard players set @s bm.musk {MUSK}',
                       'particle minecraft:squid_ink ~ ~1 ~ 0.3 0.6 0.3 0.02 12', 'playsound minecraft:entity.warden.sniff player @s ~ ~ ~ 1 0.6',
                       title('@s', 'actionbar', [T('Your scent is gone. ', COL, bold=True), T('The Stalkers will not find you for 5 minutes.', 'gray')])])
    second.append(f'execute as @a[scores={{bm.musk=1..}}] run function bm:{PFX}/musk_sec')
    fn(f'{PFX}/musk_sec', ['scoreboard players remove @s bm.musk 1',
                           'execute if score @s bm.musk matches 30 run ' + title('@s', 'actionbar', T('The Shadow Musk is wearing off...', 'gray', italic=True)),
                           'execute if score @s bm.musk matches 0 run ' + title('@s', 'actionbar', T('Your scent returns.', COL))])
    # (phase181: no Stalker rises or steps out for the masked; one hunting them loses them)
    G.FUNCS['p181/hunted'].insert(0, 'execute if score @s bm.musk matches 1.. run return run scoreboard players set @s bm.dnst 0')
    s2 = G.FUNCS['p181/stk/second']
    k = next(i for i, l in enumerate(s2) if 'unless entity @a[tag=bm.stko] run return run function bm:p181/stk/gone' in l)
    s2.insert(k + 1, 'execute if entity @a[tag=bm.stko,scores={bm.musk=1..}] run return run function bm:p181/stk/lost')

    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.mr]', 'execute as @e[type=minecraft:husk,tag=bm.mire] at @s run tp @s ~ -400 ~']
    fn('admin/mire/spawn', [f'execute positioned ^ ^ ^6 run function bm:{PFX}/spawn'])
    fn('admin/mire/kit', [give('shadow_remnant', 4), give('shadow_musk')])


def rp(R):
    A.rp(R)

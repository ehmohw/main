"""2.65: KILLERWATT - the storm-alien, as a boss (and, once beaten, a follower). Rig, textures and poses: phase79_art.

THE STORM EFFIGY (Cecil sells it): use it outdoors in a THUNDERSTORM - the sky gathers for five seconds and KillerWatt
  crashes down in front of you. (It does nothing in clear weather or under a roof.) Four and a half blocks of glassy
  green brute with four golden scythe-tendrils on his back; he grows tougher with every player who stands against him.
  THUNDER SLAM: arms up - the bent-elbow arms from the art - then down: a shockwave round him.
  TENDRIL SWEEP: the scythes swing round in a wide circle.
  CALL LIGHTNING: arms to the sky; sparks gather under up to three of you - move, or the bolt lands on you.
  At half health he ROARS: everyone near is thrown up and back, three STATIC WISPS come for you, and from then on he
  attacks faster and his slams bring bolts down round him.
  Smooth animation throughout: he breathes and sways standing, strides when he walks, winds up and follows through,
  and when he falls he crumples, sparking, and fades.
  He leaves if nobody's within 96 blocks for a minute.
THE REWARD (everyone within 64 when he falls): his TENDRILS (no longer in Cecil's shop) and KILLERWATT'S SPARK - certain
  the first time, a chance after - and Medallions, a Trophy or two and Tokens.
KILLERWATT'S SPARK: use it - he comes as a follower, a smaller version of himself (about three blocks): he walks with you,
  slams what comes close and calls lightning onto monsters further off. Use again: he comes to you; sneak + use: he goes
  home. A follower like the others (counts toward three; not in the vault or the Hollow Throne; goes home if you go far
  or put the Spark away); if he falls, 5 minutes."""
from items import item, T, TOTEM
from useitem import hold, HOLD
from nbt import snbt, B, F, D, Int
import phase67 as P67
import phase73 as P73
import phase79_art as ART

YEL = '#f6dc30'
GRN = '#74d462'
SCALE = {'boss': ART.RIG_SCALE, 'pet': 1.05}       # (1.55: about 4.7 blocks with the tendrils; the follower about 3)
DUR = {'idle_a': 30, 'idle_b': 30, 'walk_a': 10, 'walk_b': 10, 'slam_up': 10, 'slam_dn': 3, 'sweep_a': 7, 'sweep_b': 4,
       'roar': 6, 'call': 8, 'fall': 20}
PET_DUR = dict(DUR, walk_a=6, walk_b=6, slam_up=8)
STRIDE = {'boss': 20, 'pet': 12}
BOSS_HP, PET_HP, PET_CD = 500, 80, 300
P67.BOSSES += [('bm.kxboss', 'bm:kwb')]

item('kw_effigy', TOTEM, 'Storm Effigy', YEL, ['A little iron figure that hums when the sky growls.', ('Use outdoors in a thunderstorm:', 'blue'),
                                              ('KillerWatt comes down.', 'blue'), ('It does nothing in clear weather.', 'gray')],
     model='minecraft:lightning_rod', glint=True, stack=4, cat='magic', comps=hold('none'), tier=2)
HOLD['kw_effigy'] = 'bm:p79/effigy'
item('kw_spark', TOTEM, "KillerWatt's Spark", GRN, ['A crackling green mote that answers to you now.', ('Use: KillerWatt comes as a follower', 'blue'),
                                                   ('(use again: to you; sneak + use: home).', 'blue'), ('He slams what comes close and calls', 'blue'),
                                                   ('lightning onto monsters further off.', 'blue'), ('If he falls: 5 minutes.', 'gray')],
     model='bm:kw_spark', glint=True, stack=1, cat='magic', comps=hold('none'), tier=3)
HOLD['kw_spark'] = 'bm:p79/spark'


def extend_offers(O, offer):
    # his Tendrils come from him now, not from Cecil; Cecil sells the Effigy that calls him instead
    O['wizard'] = [o for o in O['wizard'] if (o['sell'].get('components') or {}).get('minecraft:custom_data', {}).get('bm') != 'killerwatt_tendrils']
    O['wizard'] += [offer(('trophy', 4), ('kw_effigy', 1))]


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    tick, fast, second = [], [], []
    ident = [F(0), F(0), F(0), F(1)]
    qf = lambda q: [F(round(v, 4)) for v in q]
    eff = lambda e: {'id': f'minecraft:{e}', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}
    attr = lambda **kw: [{'id': f'minecraft:{k}', 'base': D(v)} for k, v in kw.items()]
    objs = ['bm.kxid', 'bm.kxf', 'bm.kxs', 'bm.kxatk', 'bm.kxt', 'bm.kxc', 'bm.kxr', 'bm.kxlone', 'bm.kxk', 'bm.kxcd', 'bm.fgk']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + \
        ['bossbar add bm:kwb {text:"KillerWatt",color:"green"}', 'bossbar set bm:kwb color green', 'bossbar set bm:kwb style notched_10'] + \
        [f'scoreboard players set #{n} bm.rng {n}' for n in (2, 12, 20, 60)]
    G.OBJECTIVES += objs
    wjson('bm/predicate/p79/thunder.json', {'condition': 'minecraft:weather_check', 'thundering': True})
    wjson('bm/predicate/p79/sky.json', {'condition': 'minecraft:location_check', 'predicate': {'can_see_sky': True}})
    wjson('bm/tags/entity_type/kw_hosts.json', {'values': ['minecraft:husk', 'minecraft:wolf']})
    sel = lambda p=None: '@e[type=minecraft:item_display,tag=bm.kxsel' + (f',tag=bm.kxp_{p}]' if p else ']')

    # ================================================================== THE RIG: one display per part, stood at its joint every tick
    for kind, S in SCALE.items():
        U = S / 16
        boss = kind == 'boss'
        def part_nbt(p):
            n = {'Tags': ['bm.kxp', f'bm.kxp_{p}', f'bm.kxp_{kind}', 'bm.kxnew'],
                 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:kw_{p}'}},
                 'item_display': 'fixed', 'teleport_duration': Int(2), 'interpolation_duration': Int(8), 'start_interpolation': Int(0),
                 'view_range': F(2.0 if boss else 1.0), 'shadow_radius': F((1.4 if boss else 0.9) if p == 'body' else 0.0), 'shadow_strength': F(0.6),
                 'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0)] * 3,
                                    'scale': [F(S * (ART.TEND_K if p == 'tend' else 1))] * 3}}
            if boss:
                n['brightness'] = {'sky': Int(12), 'block': Int(12)}         # (a storm at night: he glows a little, so you can see him coming)
            return snbt(n)
        # (as the host, at it; #kid its link) a fresh set of parts
        fn(f'p79/{kind}/rig', [f'summon minecraft:item_display ~ ~ ~ {part_nbt(p)}' for p in ART.PARTS] +
           ['scoreboard players operation @e[type=minecraft:item_display,tag=bm.kxnew,distance=..1] bm.kxid = #kid bm.rng',
            'execute if score @s bm.pid matches 1.. run scoreboard players operation @e[type=minecraft:item_display,tag=bm.kxnew,distance=..1] bm.pid = @s bm.pid',
            'tag @e[type=minecraft:item_display,tag=bm.kxnew,distance=..1] add bm.kxsel', 'tag @e[type=minecraft:item_display,tag=bm.kxnew] remove bm.kxnew',
            'scoreboard players set @s bm.kxs -1'])
        # (rotated with the host) design +x is his right = ^-x; design -z his front = ^+z
        fn(f'p79/{kind}/place', [f'execute positioned ^{-x * U:.4f} ^{y * U:.4f} ^{-z * U:.4f} run tp {sel(p)} ~ ~ ~ ~ 0' for p, (x, y, z) in ART.PIVOT.items()])
        # poses: the same quaternions at either size; the lift scales with him
        for name, pose in ART.POSES.items():
            d = (DUR if boss else PET_DUR)[name]
            def xf(p):
                rot, (_x, dy, _z) = ART.part_xf(pose, p)
                return f'left_rotation:{snbt(qf(rot))},translation:[0f,{dy * S / ART.RIG_SCALE:.4f}f,0f]'
            fn(f'p79/{kind}/pose/{name}', [f'execute as {sel(p)} run data merge entity @s {{start_interpolation:0,interpolation_duration:{d},transformation:{{{xf(p)}}}}}'
                                           for p in ART.PARTS])
        # the heartbeat (as the host, at it): find his parts (or make them), stand them up, attack or move
        fn(f'p79/{kind}/tick', ['scoreboard players add @s bm.kxf 1', 'scoreboard players operation #kid bm.rng = @s bm.kxid',
                                'execute as @e[type=minecraft:item_display,tag=bm.kxp,tag=!bm.kxdying] if score @s bm.kxid = #kid bm.rng run tag @s add bm.kxsel',
                                f'execute unless entity {sel("body")} run function bm:p79/{kind}/rig',
                                f'execute rotated as @s rotated ~ 0 run function bm:p79/{kind}/place',
                                f'execute if score @s bm.kxatk matches 1.. run function bm:p79/{kind}/attack',
                                f'execute unless score @s bm.kxatk matches 1.. run function bm:p79/{kind}/move',
                                f'execute unless score @s bm.kxatk matches 1.. run function bm:p79/{kind}/mind',
                                f'tag {sel()} remove bm.kxsel'])
        # walking: a stride cycle (footfalls that shake); standing: a slow breath
        T2 = STRIDE[kind]
        steps = [] if not boss else \
            [f'execute if score #st bm.rng matches 1 if score #f bm.rng matches {T2 // 4} run playsound minecraft:entity.iron_golem.step hostile @a[distance=..28] ~ ~ ~ 1 0.6',
             f'execute if score #st bm.rng matches 1 if score #f bm.rng matches {3 * T2 // 4} run playsound minecraft:entity.iron_golem.step hostile @a[distance=..28] ~ ~ ~ 1 0.55',
             f'execute if score #st bm.rng matches 1 if score #f bm.rng matches {T2 // 4} run particle minecraft:electric_spark ~ ~0.1 ~ 0.6 0 0.6 0.05 4']
        fn(f'p79/{kind}/move', ['scoreboard players set #st bm.rng 0', 'execute if predicate bm:p21/walking run scoreboard players set #st bm.rng 1',
                                'execute unless score @s bm.kxs = #st bm.rng run scoreboard players set @s bm.kxf 0', 'scoreboard players operation @s bm.kxs = #st bm.rng',
                                'scoreboard players operation #f bm.rng = @s bm.kxf',
                                f'execute if score #st bm.rng matches 1 run scoreboard players operation #f bm.rng %= #{T2} bm.rng',
                                'execute if score #st bm.rng matches 0 run scoreboard players operation #f bm.rng %= #60 bm.rng',
                                f'execute if score #st bm.rng matches 1 if score #f bm.rng matches 0 run function bm:p79/{kind}/pose/walk_a',
                                f'execute if score #st bm.rng matches 1 if score #f bm.rng matches {T2 // 2} run function bm:p79/{kind}/pose/walk_b',
                                f'execute if score #st bm.rng matches 0 if score #f bm.rng matches 0 run function bm:p79/{kind}/pose/idle_a',
                                f'execute if score #st bm.rng matches 0 if score #f bm.rng matches 30 run function bm:p79/{kind}/pose/idle_b'] + steps)
        fn(f'p79/{kind}/done', ['scoreboard players set @s bm.kxatk 0', 'scoreboard players set @s bm.kxs -1', 'scoreboard players set @s bm.kxf 0'])
        fn(f'p79/{kind}/go', ['$scoreboard players set @s bm.kxatk $(a)', 'scoreboard players set @s bm.kxt 0'])
    fn('p79/flex', [f'data modify entity @e[type=minecraft:item_display,tag=bm.kxsel,tag=bm.kxp_{p},limit=1] item.components."minecraft:item_model" set value "bm:kw_{p}_flex"'
                    for p in ('armr', 'arml')])
    fn('p79/unflex', [f'data modify entity @e[type=minecraft:item_display,tag=bm.kxsel,tag=bm.kxp_{p},limit=1] item.components."minecraft:item_model" set value "bm:kw_{p}"'
                      for p in ('armr', 'arml')])
    # a host gone (he fell): his parts crumple - the fall pose - spark, and fade; a follower's owner waits five minutes
    fast.append('execute as @e[type=minecraft:item_display,tag=bm.kxp_body,tag=!bm.kxdying] at @s if entity @a[distance=..96] run function bm:p79/orphan')
    fn('p79/orphan', ['scoreboard players operation #kid bm.rng = @s bm.kxid', 'scoreboard players set #has bm.rng 0',
                      'execute as @e[type=#bm:kw_hosts,tag=bm.kxhost,distance=..24] if score @s bm.kxid = #kid bm.rng run scoreboard players set #has bm.rng 1',
                      'execute if score #has bm.rng matches 1 run return 0',
                      'execute as @e[type=minecraft:item_display,tag=bm.kxp,distance=..12] if score @s bm.kxid = #kid bm.rng run tag @s add bm.kxsel',
                      'function bm:p79/unflex',
                      'execute if entity @s[tag=bm.kxp_boss] run function bm:p79/boss/pose/fall', 'execute if entity @s[tag=bm.kxp_pet] run function bm:p79/pet/pose/fall',
                      f'scoreboard players set {sel()} bm.kxt 40', f'tag {sel()} add bm.kxdying',
                      'execute if entity @s[tag=bm.kxp_boss] run function bm:p79/boss/fallen', 'execute if entity @s[tag=bm.kxp_pet] run function bm:p79/pet/fallen',
                      f'tag {sel()} remove bm.kxsel'])
    tick.append('execute as @e[type=minecraft:item_display,tag=bm.kxdying] at @s run function bm:p79/fade')
    fn('p79/fade', ['scoreboard players remove @s bm.kxt 1',
                    'execute if score @s bm.kxt matches 30 run particle minecraft:electric_spark ~ ~0.5 ~ 0.4 0.4 0.4 0.15 10',
                    'execute if score @s bm.kxt matches 12 run particle minecraft:electric_spark ~ ~0.5 ~ 0.5 0.5 0.5 0.2 20',
                    'execute if score @s bm.kxt matches 12 run data merge entity @s {start_interpolation:0,interpolation_duration:12,transformation:{scale:[0f,0f,0f]}}',
                    'execute if score @s bm.kxt matches ..0 run kill @s'])
    # (as a host) go quietly: his parts first, so nothing reads as a fall
    fn('p79/unrig', ['scoreboard players operation #kid bm.rng = @s bm.kxid',
                     'execute as @e[type=minecraft:item_display,tag=bm.kxp,distance=..16] if score @s bm.kxid = #kid bm.rng run kill @s'])

    # ---- the bolt: a marker sparks on the ground, then lightning (tag kwhurtp: it hurts players; kwhurtm: monsters)
    tick.append('execute as @e[type=minecraft:marker,tag=bm.kxstrike] at @s run function bm:p79/strike')
    fn('p79/strike', ['scoreboard players remove @s bm.kxt 1', 'particle minecraft:electric_spark ~ ~0.2 ~ 0.6 0 0.6 0.05 5',
                      'particle minecraft:dust{color:[0.5,1.0,0.3],scale:1.2} ~ ~0.1 ~ 0.7 0 0.7 0 3',
                      'execute if score @s bm.kxt matches 10 run playsound minecraft:block.beacon.power_select hostile @a[distance=..24] ~ ~ ~ 0.7 2',
                      'execute if score @s bm.kxt matches ..0 run function bm:p79/bolt'])
    fn('p79/bolt', [f'particle minecraft:end_rod ~ ~{y} ~ 0.05 0.4 0.05 0 4' for y in range(0, 16, 2)] +
       ['particle minecraft:flash{color:[0.75,1.0,0.6,1.0]} ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:electric_spark ~ ~0.5 ~ 1 0.5 1 0.4 60',
        'playsound minecraft:entity.lightning_bolt.thunder weather @a[distance=..48] ~ ~ ~ 0.8 1.2', 'playsound minecraft:entity.lightning_bolt.impact weather @a[distance=..32] ~ ~ ~ 1 1',
        'execute if entity @s[tag=bm.kxhurtp] as @a[distance=..2,gamemode=!creative,gamemode=!spectator] run damage @s 9 minecraft:lightning_bolt',
        'execute if entity @s[tag=bm.kxhurtm] as @e[type=#bm:hostile,tag=!bm.npc,distance=..2.2] run damage @s 9 minecraft:lightning_bolt', 'kill @s'])
    for who, t in (('p', 25), ('m', 16)):
        fn(f'p79/mark_{who}', [f'summon minecraft:marker ~ ~ ~ {{Tags:["bm.kxstrike","bm.kxhurt{who}","bm.kxsn"]}}',
                               f'scoreboard players set @e[type=minecraft:marker,tag=bm.kxsn,distance=..1] bm.kxt {t}', 'tag @e[type=minecraft:marker,tag=bm.kxsn] remove bm.kxsn'])

    # ================================================================== THE STORM EFFIGY: outdoors, in a thunderstorm
    fn('p79/effigy', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 3',
                      'execute unless dimension minecraft:overworld run return run ' + say('The effigy is cold here. (It wants an Overworld thunderstorm.)', YEL),
                      'execute unless predicate bm:p79/thunder run return run ' + say('The effigy only answers a thunderstorm.', YEL),
                      'execute unless predicate bm:p79/sky run return run ' + say('It needs the open sky above you.', YEL),
                      'execute if entity @e[type=minecraft:husk,tag=bm.kxboss,distance=..160] run return run ' + say('KillerWatt is already here!', 'red'),
                      'execute if entity @e[type=minecraft:marker,tag=bm.kxcall,distance=..160] run return run ' + say('The storm is already gathering...', YEL),
                      'execute unless entity @s[gamemode=creative] run clear @s *[minecraft:custom_data~{bm:"kw_effigy"}] 1',
                      'execute rotated ~ 0 positioned ^ ^ ^9 run summon minecraft:marker ~ ~ ~ {Tags:["bm.kxcall","bm.kxsn"]}',
                      'scoreboard players set #gd bm.rng 64',
                      'execute as @e[type=minecraft:marker,tag=bm.kxsn,limit=1] at @s run function bm:p79/rise',
                      'scoreboard players set #gd bm.rng 64',
                      'execute as @e[type=minecraft:marker,tag=bm.kxsn,limit=1] at @s run function bm:p79/sink',
                      'scoreboard players set @e[type=minecraft:marker,tag=bm.kxsn,limit=1] bm.kxt 100', 'tag @e[type=minecraft:marker,tag=bm.kxsn] remove bm.kxsn',
                      'playsound minecraft:block.beacon.activate player @a[distance=..16] ~ ~ ~ 1 0.6',
                      tellraw('@a[distance=..96]', PREFIX + [T('The storm gathers... ', YEL, bold=True), T('something is coming down.', 'gray')])])
    # (the landing spot: out of any hill, then down onto the ground)
    fn('p79/rise', ['execute if block ~ ~ ~ #minecraft:replaceable run return 0', 'scoreboard players remove #gd bm.rng 1',
                    'execute if score #gd bm.rng matches ..0 run return 0', 'tp @s ~ ~1 ~', 'execute at @s run function bm:p79/rise'])
    fn('p79/sink', ['execute unless block ~ ~-1 ~ #minecraft:replaceable run return 0', 'scoreboard players remove #gd bm.rng 1',
                    'execute if score #gd bm.rng matches ..0 run return 0', 'tp @s ~ ~-1 ~', 'execute at @s run function bm:p79/sink'])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.kxcall] at @s run function bm:p79/calling')
    fn('p79/calling', ['scoreboard players remove @s bm.kxt 1', 'particle minecraft:electric_spark ~ ~0.5 ~ 1.5 0.2 1.5 0.1 6',
                       'execute if score @s bm.kxt matches 80 run playsound minecraft:entity.lightning_bolt.thunder weather @a[distance=..96] ~ ~ ~ 1 0.6',
                       'execute if score @s bm.kxt matches 40 run playsound minecraft:entity.lightning_bolt.thunder weather @a[distance=..96] ~ ~ ~ 1 0.8',
                       'execute if score @s bm.kxt matches 1..60 run particle minecraft:end_rod ~ ~8 ~ 0.6 5 0.6 0.02 4',
                       'execute if score @s bm.kxt matches 1..30 run particle minecraft:dust{color:[0.5,1.0,0.3],scale:2.0} ~ ~0.2 ~ 1.4 0 1.4 0 10',
                       'execute if score @s bm.kxt matches ..0 run function bm:p79/boss/arrive'])

    # ================================================================== THE BOSS
    bnbt = {'Tags': ['bm.kxboss', 'bm.kxhost', 'bm.kxnew', 'bm.seen'], 'PersistenceRequired': B(1), 'Silent': B(1), 'CustomName': T('KillerWatt', GRN, bold=True),
            'IsBaby': B(0), 'CanBreakDoors': B(0), 'DeathLootTable': 'minecraft:empty', 'Health': F(BOSS_HP),
            'attributes': attr(scale=2.3, max_health=BOSS_HP, attack_damage=10, armor=10, armor_toughness=4, movement_speed=0.26, follow_range=48,
                               knockback_resistance=0.8, spawn_reinforcements=0.0, step_height=1.5),
            'active_effects': [eff('invisibility'), eff('fire_resistance')],
            'drop_chances': {s: F(0.0) for s in ('mainhand', 'offhand', 'head', 'chest', 'legs', 'feet')}}
    fn('p79/boss/arrive', [f'summon minecraft:husk ~ ~ ~ {snbt(bnbt)}', 'execute as @e[type=minecraft:husk,tag=bm.kxnew,limit=1] at @s run function bm:p79/boss/init',
                           'particle minecraft:flash{color:[0.75,1.0,0.6,1.0]} ~ ~2 ~ 0 0 0 0 1'] +
       [f'particle minecraft:end_rod ~ ~{y} ~ 0.1 0.5 0.1 0 6' for y in range(0, 27, 3)] +
       ['particle minecraft:explosion_emitter ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:electric_spark ~ ~0.5 ~ 3 0.3 3 0.4 150',
        'playsound minecraft:entity.lightning_bolt.impact weather @a[distance=..96] ~ ~ ~ 2 0.6', 'playsound minecraft:entity.ravager.roar hostile @a[distance=..64] ~ ~ ~ 1.5 0.5',
        'title @a[distance=..64] times 10 50 15', title('@a[distance=..64]', 'title', T('KILLERWATT', GRN, bold=True)),
        title('@a[distance=..64]', 'subtitle', T('the storm walks', YEL)), 'kill @s'])
    fn('p79/boss/init', ['scoreboard players add #kwn bm.kxid 1', 'scoreboard players operation @s bm.kxid = #kwn bm.kxid',
                         'scoreboard players set @s bm.kxr 0', 'scoreboard players set @s bm.kxatk 0', 'scoreboard players set @s bm.kxc 30',
                         'scoreboard players set @s bm.kxlone 0', 'tag @s remove bm.kxnew', 'scoreboard players operation #kid bm.rng = @s bm.kxid',
                         'function bm:p79/boss/rig', f'tag {sel()} remove bm.kxsel'])
    tick.append('execute as @e[type=minecraft:husk,tag=bm.kxboss] at @s run function bm:p79/boss/tick')
    # the mind (each tick he isn't mid-attack): every second, maybe start one; 3 seconds between (under 2 once enraged)
    fn('p79/boss/mind', ['scoreboard players remove @s bm.kxc 1', 'execute if score @s bm.kxc matches 1.. run return 0', 'scoreboard players set @s bm.kxc 20',
                         'execute store result score #hp bm.rng run data get entity @s Health', 'execute store result score #mx bm.rng run attribute @s minecraft:max_health get',
                         'scoreboard players operation #mx bm.rng /= #2 bm.rng',
                         'execute if score @s bm.kxr matches 0 if score #hp bm.rng <= #mx bm.rng run return run function bm:p79/boss/start {a:4}',
                         'execute store result score #r bm.rng run random value 1..100',
                         'execute if entity @a[distance=..5.5,gamemode=!creative,gamemode=!spectator] if score #r bm.rng matches 1..50 run return run function bm:p79/boss/start {a:1}',
                         'execute if entity @a[distance=..7,gamemode=!creative,gamemode=!spectator] if score #r bm.rng matches 51..85 run return run function bm:p79/boss/start {a:2}',
                         'execute if entity @a[distance=..28,gamemode=!creative,gamemode=!spectator] if score #r bm.rng matches 60..100 run return run function bm:p79/boss/start {a:3}'])
    fn('p79/boss/start', ['$function bm:p79/boss/go {a:$(a)}', 'execute if score @s bm.kxatk matches 4 run scoreboard players set @s bm.kxr 1',
                          'scoreboard players set @s bm.kxc 60', 'execute if score @s bm.kxr matches 1 run scoreboard players set @s bm.kxc 36',
                          'effect give @s minecraft:slowness 2 6 true'])
    fn('p79/boss/attack', ['scoreboard players add @s bm.kxt 1', 'tag @s add bm.kxme',
                           'execute if score @s bm.kxatk matches 1 run function bm:p79/boss/a_slam', 'execute if score @s bm.kxatk matches 2 run function bm:p79/boss/a_sweep',
                           'execute if score @s bm.kxatk matches 3 run function bm:p79/boss/a_call', 'execute if score @s bm.kxatk matches 4 run function bm:p79/boss/a_roar',
                           'tag @s remove bm.kxme'])
    me = '@e[type=minecraft:husk,tag=bm.kxme,limit=1]'
    foes = lambda r: f'@a[distance=..{r},gamemode=!creative,gamemode=!spectator]'
    at = lambda t, cmd: f'execute if score @s bm.kxt matches {t} run {cmd}'
    # THUNDER SLAM: up (the bent arms, sparks crawling over them), down, the quake
    fn('p79/boss/a_slam', [at(1, 'function bm:p79/boss/pose/slam_up'), at(1, 'function bm:p79/flex'),
                           at(1, 'playsound minecraft:entity.warden.attack_impact hostile @a[distance=..32] ~ ~ ~ 1 1.6'),
                           at('2..12', 'particle minecraft:electric_spark ~ ~4.8 ~ 1.4 0.4 1.4 0.05 4'),
                           at(13, 'function bm:p79/boss/pose/slam_dn'), at(13, 'function bm:p79/unflex'), at(16, 'function bm:p79/boss/quake'),
                           at('28..', 'function bm:p79/boss/done')])
    fn('p79/boss/quake', ['particle minecraft:explosion ~ ~0.3 ~ 2.5 0.1 2.5 0 10', 'particle minecraft:electric_spark ~ ~0.3 ~ 4 0.1 4 0.3 120',
                          'particle minecraft:block{block_state:"minecraft:dirt"} ~ ~0.2 ~ 3 0.1 3 0 60',
                          'playsound minecraft:entity.generic.explode hostile @a[distance=..40] ~ ~ ~ 1.2 0.6', 'playsound minecraft:entity.lightning_bolt.impact hostile @a[distance=..40] ~ ~ ~ 1 1.4',
                          f'execute as {foes(5.5)} run damage @s 11 minecraft:mob_attack by {me}', f'effect give {foes(5.5)} minecraft:slowness 2 1'] +
       [f'execute if score @s bm.kxr matches 1 positioned ^{x} ^ ^{z} run function bm:p79/mark_p' for x, z in ((5, 0), (-5, 0), (0, 5), (0, -5))])
    # TENDRIL SWEEP: the scythes wind back, then round
    fn('p79/boss/a_sweep', [at(1, 'function bm:p79/boss/pose/sweep_a'), at(1, 'playsound minecraft:item.trident.riptide_1 hostile @a[distance=..32] ~ ~ ~ 1 0.6'),
                            at(9, 'function bm:p79/boss/pose/sweep_b'), at(10, 'function bm:p79/boss/swipe'), at('22..', 'function bm:p79/boss/done')])
    fn('p79/boss/swipe', [f'particle minecraft:sweep_attack ^{x} ^2.5 ^{z} 0 0 0 0 1' for x, z in ((-4, 0), (-3, 3), (0, 4), (3, 3), (4, 0), (3, -3), (0, -4), (-3, -3))] +
       ['particle minecraft:electric_spark ~ ~2 ~ 4 0.6 4 0.2 60', 'playsound minecraft:entity.player.attack.sweep hostile @a[distance=..32] ~ ~ ~ 1.4 0.5',
        f'execute as {foes(7)} run damage @s 9 minecraft:mob_attack by {me}'])
    # CALL LIGHTNING: arms to the sky; a bolt marked under up to three of you (enraged: four more round him)
    fn('p79/boss/a_call', [at(1, 'function bm:p79/boss/pose/call'), at(1, 'playsound minecraft:entity.lightning_bolt.thunder weather @a[distance=..64] ~ ~ ~ 1 0.7'),
                           at('2..30', 'particle minecraft:end_rod ~ ~5.8 ~ 0.6 0.6 0.6 0.05 3'),
                           at(9, 'execute as @a[distance=..28,gamemode=!creative,gamemode=!spectator,sort=random,limit=3] at @s run function bm:p79/mark_p')] +
       [at(9, f'execute if score @s bm.kxr matches 1 positioned ^{x} ^ ^{z} run function bm:p79/mark_p') for x, z in ((7, 3), (-7, 3), (3, -7), (-3, -7))] +
       [at('40..', 'function bm:p79/boss/done')])
    # THE ROAR (once, at half health): thrown up and back, Static Wisps
    wisp = {'Tags': ['bm.kxwisp', 'bm.seen'], 'PersistenceRequired': B(1), 'CustomName': T('Static Wisp', '#c0ff80'), 'Glowing': B(1),
            'DeathLootTable': 'minecraft:empty', 'Health': F(16), 'attributes': attr(max_health=16, attack_damage=4)}
    fn('p79/boss/a_roar', [at(1, 'function bm:p79/boss/pose/roar'), at(1, 'function bm:p79/flex'),
                           at(1, 'playsound minecraft:entity.ravager.roar hostile @a[distance=..64] ~ ~ ~ 2 0.5'),
                           at(1, 'playsound minecraft:entity.lightning_bolt.thunder weather @a[distance=..64] ~ ~ ~ 1 0.5'),
                           at('2..24', 'particle minecraft:electric_spark ~ ~4 ~ 1.5 1.5 1.5 0.3 8'),
                           at(8, 'function bm:p79/boss/shock'), at(26, 'function bm:p79/unflex'), at('32..', 'function bm:p79/boss/done')])
    fn('p79/boss/shock', ['particle minecraft:electric_spark ~ ~2 ~ 3 1 3 0.6 160', 'particle minecraft:flash{color:[0.75,1.0,0.6,1.0]} ~ ~2 ~ 0 0 0 0 1',
                          f'execute as {foes(7)} run damage @s 5 minecraft:mob_attack by {me}', f'effect give {foes(7)} minecraft:levitation 1 3 true'] +
       [f'execute positioned ^{x} ^3 ^{z} run summon minecraft:vex ~ ~ ~ {snbt(wisp)}' for x, z in ((3, 2), (-3, 2), (0, -3))] +
       ['scoreboard players set @e[type=minecraft:vex,tag=bm.kxwisp,distance=..8] bm.kxt 40',
        tellraw('@a[distance=..64]', PREFIX + [T('KillerWatt roars - the air itself turns on you!', GRN, bold=True)])])
    # each hit on him: a crackle and a grunt (he's Silent - these are his own)
    wjson('bm/advancement/p79/hit.json', {'criteria': {'h': {'trigger': 'minecraft:player_hurt_entity', 'conditions': {'entity': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["bm.kxboss"]}'}}]}}}, 'rewards': {'function': 'bm:p79/hit'}})
    fn('p79/hit', ['advancement revoke @s only bm:p79/hit',
                   'execute at @s as @e[type=minecraft:husk,tag=bm.kxboss,distance=..48,limit=1,sort=nearest] at @s run function bm:p79/boss/ouch'])
    fn('p79/boss/ouch', ['particle minecraft:electric_spark ~ ~2.5 ~ 0.8 1.2 0.8 0.2 14', 'playsound minecraft:entity.iron_golem.hurt hostile @a[distance=..32] ~ ~ ~ 0.9 0.55',
                         'playsound minecraft:block.amethyst_block.hit hostile @a[distance=..32] ~ ~ ~ 1 0.6'])
    # every second: the bar, the wisps' time, and whether anyone's still here
    second += ['bossbar set bm:kwb players', 'execute as @e[type=minecraft:husk,tag=bm.kxboss] at @s run function bm:p79/boss/sec',
               'execute as @e[type=minecraft:vex,tag=bm.kxwisp] at @s run function bm:p79/wisp']
    fn('p79/boss/sec', ['execute store result bossbar bm:kwb value run data get entity @s Health', 'execute store result bossbar bm:kwb max run attribute @s minecraft:max_health get',
                        'bossbar set bm:kwb players @a[distance=..64]', 'data modify entity @s InWaterTime set value -1',
                        'particle minecraft:electric_spark ~ ~3 ~ 1 1.5 1 0.05 6',
                        'execute if entity @a[distance=..96] run scoreboard players set @s bm.kxlone 0', 'execute unless entity @a[distance=..96] run scoreboard players add @s bm.kxlone 1',
                        'execute if score @s bm.kxlone matches 60.. run function bm:p79/boss/leave'])
    fn('p79/wisp', ['scoreboard players remove @s bm.kxt 1', 'particle minecraft:electric_spark ~ ~0.4 ~ 0.2 0.2 0.2 0.05 2',
                    'execute if score @s bm.kxt matches ..0 run return run function bm:p79/wisp_go',
                    'execute unless entity @e[type=minecraft:husk,tag=bm.kxboss,distance=..64] run function bm:p79/wisp_go'])
    fn('p79/wisp_go', ['particle minecraft:electric_spark ~ ~0.4 ~ 0.3 0.3 0.3 0.2 12', 'tp @s ~ -400 ~', 'kill @s'])
    fn('p79/boss/leave', ['particle minecraft:flash{color:[0.75,1.0,0.6,1.0]} ~ ~2 ~ 0 0 0 0 1', 'playsound minecraft:entity.lightning_bolt.thunder weather @a[distance=..96] ~ ~ ~ 1 1',
                          'function bm:p79/unrig', 'tp @s ~ -400 ~', 'kill @s'])
    fn('p79/boss/fallen', ['kill @e[type=minecraft:marker,tag=bm.kxstrike,distance=..64]',
                           'playsound minecraft:entity.lightning_bolt.thunder weather @a[distance=..96] ~ ~ ~ 1.5 0.5', 'playsound minecraft:entity.warden.death hostile @a[distance=..48] ~ ~ ~ 1 1.4',
                           'particle minecraft:electric_spark ~ ~1 ~ 2 2 2 0.4 200', 'particle minecraft:flash{color:[0.75,1.0,0.6,1.0]} ~ ~1 ~ 0 0 0 0 1'])
    # the reward: everyone within 64 of the killing blow
    wjson('bm/advancement/p79/kill.json', {'criteria': {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["bm.kxboss"]}'}}]}}}, 'rewards': {'function': 'bm:p79/killed'}})
    fn('p79/killed', ['advancement revoke @s only bm:p79/kill', 'execute at @s as @a[distance=..64] at @s run function bm:p79/reward',
                      tellraw('@a', PREFIX + [{'selector': '@s', 'color': 'white'}, T(' brought down ', 'gray'), T('KILLERWATT', GRN, bold=True), T('!', 'gray')])])
    fn('p79/reward', ['scoreboard players add @s bm.kxk 1', 'execute if score @s bm.kxk matches 1 run function bm:p79/first',
                      'execute store result score #r bm.rng run random value 1..100',
                      'execute if score @s bm.kxk matches 2.. if score #r bm.rng matches 1..20 run ' + give('killerwatt_tendrils'),
                      'execute if score @s bm.kxk matches 2.. if score #r bm.rng matches 21..30 run ' + give('kw_spark'),
                      'loot give @s loot bm:p79/hoard', 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1'])
    fn('p79/first', [give('killerwatt_tendrils'), give('kw_spark'),
                     tellraw('@s', PREFIX + [T("KillerWatt's Tendrils", YEL, bold=True), T(' and ', 'gray'), T('his Spark', GRN, bold=True),
                                             T(" are yours - use the Spark and he'll fight beside you.", 'gray')])])
    wjson('bm/loot_table/p79/hoard.json', {'pools': [{'rolls': 1, 'entries': [G.loot_entry('medallion', G.uni(3, 6))]},
                                                     {'rolls': 1, 'entries': [G.loot_entry('trophy', G.uni(1, 2))]},
                                                     {'rolls': 1, 'entries': [G.loot_entry('token', G.uni(4, 9))]}]})

    # ================================================================== THE FOLLOWER
    pnbt = {'Tags': ['bm.kxpet', 'bm.kxhost', 'bm.kxnew', 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1), 'CustomName': T('KillerWatt', GRN, bold=True),
            'CustomNameVisible': B(0), 'Health': F(PET_HP),
            'attributes': attr(scale=1.7, max_health=PET_HP, armor=8, attack_damage=4, movement_speed=0.33, follow_range=32, step_height=1.25),
            'active_effects': [eff('invisibility')]}
    mine = 'execute as @e[type=minecraft:wolf,tag=bm.kxpet] if score @s bm.pid = #me bm.pid'
    fn('p79/spark', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                     'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                     f'{mine} run tag @s add bm.kxsel2',
                     'execute if entity @e[type=minecraft:wolf,tag=bm.kxsel2] if predicate bm:p20/sneaking run function bm:p79/pet/home',
                     'execute if entity @e[type=minecraft:wolf,tag=bm.kxsel2] unless predicate bm:p20/sneaking run function bm:p79/pet/recall',
                     'execute unless entity @e[type=minecraft:wolf,tag=bm.kxsel2] unless predicate bm:p20/sneaking run function bm:p79/pet/try',
                     'execute unless entity @e[type=minecraft:wolf,tag=bm.kxsel2] if predicate bm:p20/sneaking run ' + say("KillerWatt isn't with you. (Use the Spark to call him.)"),
                     'tag @e[type=minecraft:wolf,tag=bm.kxsel2] remove bm.kxsel2'])
    fn('p79/pet/recall', ['tp @e[type=minecraft:wolf,tag=bm.kxsel2,limit=1] @s', 'data modify entity @e[type=minecraft:wolf,tag=bm.kxsel2,limit=1] Sitting set value 0b',
                          'particle minecraft:electric_spark ~ ~1.5 ~ 0.6 1 0.6 0.3 40', 'playsound minecraft:entity.lightning_bolt.impact neutral @a[distance=..16] ~ ~ ~ 0.4 1.8',
                          say('KillerWatt crackles over to you.', GRN)])
    fn('p79/pet/home', ['execute as @e[type=minecraft:wolf,tag=bm.kxsel2] at @s run function bm:p79/pet/vanish', say('KillerWatt goes home.', GRN)])
    fn('p79/pet/try', ['execute if score @s bm.kxcd matches 1.. store result score #m bm.rng run scoreboard players get @s bm.kxcd',
                       'execute if score @s bm.kxcd matches 1.. run scoreboard players add #m bm.rng 59', 'execute if score @s bm.kxcd matches 1.. run scoreboard players operation #m bm.rng /= #60 bm.rng',
                       'execute if score @s bm.kxcd matches 1.. run return run ' + title('@s', 'actionbar', [T('KillerWatt is still recharging: about ', 'gray'),
                                                                                                          {'score': {'name': '#m', 'objective': 'bm.rng'}, 'color': 'white'}, T(' min.', 'gray')]),
                       'execute unless function bm:p74/fol_ok run return run ' + say("The Spark won't answer here."),
                       'execute if function bm:p58/full run return 0', 'function bm:p79/pet/summon'])
    fn('p79/pet/summon', [f'execute rotated ~ 0 positioned ^ ^ ^2 run summon minecraft:wolf ~ ~ ~ {snbt(pnbt)}',
                          'data modify entity @e[type=minecraft:wolf,tag=bm.kxnew,limit=1,sort=nearest] Owner set from entity @s UUID',
                          # (a wolf loaded without an owner resets to 8 health; taming it by NBT doesn't put it back - as for Zib)
                          f'attribute @e[type=minecraft:wolf,tag=bm.kxnew,limit=1,sort=nearest] minecraft:max_health base set {PET_HP}',
                          f'data modify entity @e[type=minecraft:wolf,tag=bm.kxnew,limit=1,sort=nearest] Health set value {PET_HP}f',
                          'scoreboard players operation @e[type=minecraft:wolf,tag=bm.kxnew,limit=1,sort=nearest] bm.pid = @s bm.pid',
                          'execute as @e[type=minecraft:wolf,tag=bm.kxnew,limit=1,sort=nearest] at @s run function bm:p79/pet/init',
                          'execute rotated ~ 0 positioned ^ ^ ^2 run particle minecraft:electric_spark ~ ~1.5 ~ 0.6 1 0.6 0.3 60',
                          'execute rotated ~ 0 positioned ^ ^ ^2 run particle minecraft:flash{color:[0.75,1.0,0.6,1.0]} ~ ~1 ~ 0 0 0 0 1',
                          'playsound minecraft:entity.lightning_bolt.impact neutral @a[distance=..24] ~ ~ ~ 0.6 1.6', say('KillerWatt answers the Spark.', GRN)])
    fn('p79/pet/init', ['scoreboard players add #kwn bm.kxid 1', 'scoreboard players operation @s bm.kxid = #kwn bm.kxid', 'scoreboard players set @s bm.kxatk 0',
                        'scoreboard players set @s bm.kxc 40', 'tag @s remove bm.kxnew', 'scoreboard players operation #kid bm.rng = @s bm.kxid',
                        'function bm:p79/pet/rig', f'tag {sel()} remove bm.kxsel'])
    fn('p79/pet/vanish', ['particle minecraft:electric_spark ~ ~1.5 ~ 0.6 1 0.6 0.3 30', 'function bm:p79/unrig', 'data remove entity @s Owner', 'tp @s ~ -400 ~', 'kill @s'])
    tick.append('execute as @e[type=minecraft:wolf,tag=bm.kxpet] at @s run function bm:p79/pet/tick')
    hostile = 'type=#bm:hostile,tag=!bm.npc'
    fn('p79/pet/mind', ['scoreboard players remove @s bm.kxc 1', 'execute if score @s bm.kxc matches 1.. run return 0', 'scoreboard players set @s bm.kxc 10',
                        'execute if data entity @s {Sitting:1b} run return 0',
                        f'execute if entity @e[{hostile},distance=..4.5] run return run function bm:p79/pet/start {{a:1}}',
                        f'execute if entity @e[{hostile},distance=..16] run return run function bm:p79/pet/start {{a:3}}'])
    fn('p79/pet/start', ['$function bm:p79/pet/go {a:$(a)}', 'scoreboard players set @s bm.kxc 90'])
    fn('p79/pet/attack', ['scoreboard players add @s bm.kxt 1', 'tag @s add bm.kxme',
                          'execute if score @s bm.kxatk matches 1 run function bm:p79/pet/a_slam', 'execute if score @s bm.kxatk matches 3 run function bm:p79/pet/a_call',
                          'tag @s remove bm.kxme'])
    pme = '@e[type=minecraft:wolf,tag=bm.kxme,limit=1]'
    fn('p79/pet/a_slam', [at(1, 'function bm:p79/pet/pose/slam_up'), at(1, 'function bm:p79/flex'), at(9, 'function bm:p79/pet/pose/slam_dn'),
                          at(9, 'function bm:p79/unflex'), at(11, 'function bm:p79/pet/quake'), at('20..', 'function bm:p79/pet/done')])
    fn('p79/pet/quake', ['particle minecraft:explosion ~ ~0.3 ~ 1.5 0.1 1.5 0 5', 'particle minecraft:electric_spark ~ ~0.3 ~ 2.5 0.1 2.5 0.3 70',
                         'playsound minecraft:entity.generic.explode neutral @a[distance=..24] ~ ~ ~ 0.7 0.9',
                         f'execute as @e[{hostile},distance=..4.5] run damage @s 8 minecraft:mob_attack by {pme}'])
    fn('p79/pet/a_call', [at(1, 'function bm:p79/pet/pose/call'), at('2..14', 'particle minecraft:end_rod ~ ~3.6 ~ 0.4 0.4 0.4 0.04 2'),
                          at(6, f'execute as @e[{hostile},distance=..16,sort=nearest,limit=1] at @s run function bm:p79/mark_m'),
                          at(6, 'playsound minecraft:entity.lightning_bolt.thunder neutral @a[distance=..32] ~ ~ ~ 0.4 1.4'),
                          at('20..', 'function bm:p79/pet/done')])
    # he falls: the owner waits five minutes
    fn('p79/pet/fallen', ['scoreboard players operation #me bm.pid = @s bm.pid', 'particle minecraft:electric_spark ~ ~1 ~ 0.8 0.8 0.8 0.3 60',
                          'playsound minecraft:entity.lightning_bolt.impact neutral @a[distance=..24] ~ ~ ~ 0.6 0.6',
                          f'execute as @a if score @s bm.pid = #me bm.pid run scoreboard players set @s bm.kxcd {PET_CD}',
                          'execute as @a if score @s bm.pid = #me bm.pid run ' + tellraw('@s', PREFIX + [T('KillerWatt falls! ', GRN, bold=True),
                                                                                                          T(f'The Spark needs {PET_CD // 60} minutes to recharge.', 'gray')])])
    second += ['scoreboard players remove @a[scores={bm.kxcd=1..}] bm.kxcd 1',
               'execute as @e[type=minecraft:wolf,tag=bm.kxpet] at @s unless entity @e[type=#bm:hostile,tag=!bm.npc,distance=..16] run effect give @s minecraft:regeneration 3 0 true']
    # a follower like the others: the limit of three, gone with you when you die, home when you go far or put the Spark away
    cnt = G.FUNCS['p58/count']
    cnt.insert(len(cnt) - 1, 'execute as @e[type=minecraft:wolf,tag=bm.kxpet] on owner if entity @s[tag=bm.fcme] run scoreboard players add #fc bm.rng 1')
    G.FUNCS['p62/died'].insert(-1, 'execute as @e[type=minecraft:wolf,tag=bm.kxpet] if score @s bm.pid = #me bm.pid at @s run function bm:p79/pet/died')
    fn('p79/pet/died', ['scoreboard players add #gone bm.rng 1', 'function bm:p79/pet/vanish'])
    P73.follow_rules(G, ('kw', 'wolf', 'bm.kxpet', 'kw_spark', 'p79/pet/vanish', 'KillerWatt', 'bm.fgk', 'p79/pet/summon'), second)

    # ================================================================== admin
    fn('admin/killerwatt', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.kxcall","bm.kxsn"]}',
                            'scoreboard players set @e[type=minecraft:marker,tag=bm.kxsn,limit=1] bm.kxt 1', 'tag @e[type=minecraft:marker,tag=bm.kxsn] remove bm.kxsn'])
    fn('admin/killerwatt_items', [give('kw_effigy'), give('kw_spark'), give('killerwatt_tendrils')])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.kxp]', 'kill @e[type=minecraft:marker,tag=bm.kxstrike]',
                                       'kill @e[type=minecraft:marker,tag=bm.kxcall]', 'execute as @e[type=minecraft:husk,tag=bm.kxboss] run tp @s ~ -400 ~',
                                       'execute as @e[type=minecraft:wolf,tag=bm.kxpet] run tp @s ~ -400 ~', 'execute as @e[type=minecraft:vex,tag=bm.kxwisp] run tp @s ~ -400 ~']

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    f[-1:-1] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


def rp(R):
    R.TEXTURE_MODS.append(ART)
    for name, (tex, els) in ART.models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + ('kw_',)
    R.ICONS['kw_spark'] = R.grid(['................', '.......g........', '......gLg.......', '.....gLYLg......', '....gLYWYLg..g..', '...gLYWWWYLg.L..',
                                  '..gLYWWWWWYLg...', '.gLYWWWWWWWYLg..', '..gLYWWWWWYLg...', '...gLYWWWYLg....', '.L..gLYWYLg.....', '.....gLYLg......',
                                  '......gLg....g..', '.......g...g.L..', '...g............', '................'],
                                 dict(g='#258a46', L='#74d462', Y='#c8ff80', W='#f4ffe8'))

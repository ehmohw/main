"""2.65: KILLERWATT - the storm-alien, as a boss (and, once beaten, a follower). Rig, textures and poses: phase79_art.

THE STORM EFFIGY (2.79b: Democratus gives it to whoever beats him in a duel - KillerWatt is his successor; Cecil no longer
  sells it): use it outdoors in a THUNDERSTORM - the sky gathers for five seconds and KillerWatt
  crashes down in front of you. (It does nothing in clear weather or under a roof.) Four and a half blocks of glassy
  green brute with four golden scythe-tendrils on his back; he grows tougher with every player who stands against him.
  THUNDER SLAM: arms up - the bent-elbow arms from the art - then down: a shockwave round him.
  TENDRIL SWEEP: the scythes swing round in a wide circle.
  (2.67) TENDRIL LUNGE: he turns on you, coils all four scythes back and drives them at you.
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
  or put the Spark away); if he falls, 5 minutes.
2.66 - THE FOLLOWER GROWS UP:
  RIDE HIM: use the Spark beside him and you're up on his back. He goes where you look; walk to stride, jump to hop, and a
  wall ahead is no wall - he climbs it on his tendrils. The Spark, riding: THUNDER LEAP (up, over, and a slam where he
  lands). Sneak to get off. He still fights while you ride.
  HIS FIGHTING: THE TENDRIL STAB (the scythes drive down and pin a foe, then a right and a left), THE LEAP (a crouch, up
  and down on a foe a little way off), CHAIN LIGHTNING (arcs from his hands to three foes), and the old slam and call.
  He climbs walls to follow you.
  HIS ELEMENT: right-click him with one of Pearlman's gems - his hide takes its colours and every blow its touch (fire
  burns, water slows, poison poisons, earth roots, rock weakens, air throws up, grass heals him, ice freezes). Electric is
  his own. Sneak + right-click him empty-handed: the gem back. THE ETHEREAL GEM: his ETHEREAL FORM - metallic black,
  iridescent tendrils, glowing seams and jagged spikes; half again as strong, and he floats - ridden, he FLIES (look up
  to rise, down to sink)."""
import math
from items import item, T, TOTEM
from useitem import hold, HOLD
from nbt import snbt, B, F, D, Int
import phase67 as P67
import phase73 as P73
import phase79_art as ART
from phase60 import GEMS as _GEMS
GEMS_COL = {k: v[1] for k, v in _GEMS.items()}

YEL = '#f6dc30'
GRN = '#74d462'
SCALE = {'boss': ART.RIG_SCALE, 'pet': 1.05}       # (1.55: about 4.7 blocks with the tendrils; the follower about 3)
DUR = {'idle_a': 30, 'idle_b': 30, 'walk_a': 10, 'walk_b': 10, 'slam_up': 10, 'slam_dn': 3, 'sweep_a': 7, 'sweep_b': 4,
       'roar': 6, 'call': 8, 'fall': 20, 'stab': 4, 'punch_r': 3, 'punch_l': 3, 'crouch': 5, 'hover': 20, 'climb': 6,
       'lunge_a': 8, 'lunge_b': 3, 'charge': 14, 'release': 3, 'flinch': 3, 'swim_a': 6, 'swim_b': 6, 'swim_c': 6, 'swim_d': 6,
       'sit_a': 24, 'sit_b': 30, 'sit_look': 18}
PET_DUR = dict(DUR, walk_a=6, walk_b=6, slam_up=8)
STRIDE = {'boss': 20, 'pet': 12}
BOSS_HP, PET_HP, PET_CD = 500, 80, 300
P67.BOSSES += [('bm.kxboss', 'bm:kwb')]

item('kw_effigy', TOTEM, 'Storm Effigy', YEL, ['A little iron figure that hums when the sky growls.', ('Use outdoors in a thunderstorm:', 'blue'),
                                              ('KillerWatt comes down.', 'blue'), ('It does nothing in clear weather.', 'gray')],
     model='minecraft:lightning_rod', glint=True, stack=4, cat='magic', comps=hold('none'), tier=2)
HOLD['kw_effigy'] = 'bm:p79/effigy'
item('kw_spark', TOTEM, "KillerWatt's Spark", GRN, ['A crackling green mote that answers to you now.', ('Use: KillerWatt comes as a follower', 'blue'),
                                                   ('(use again: to you; beside him: ride him;', 'blue'), ('sneak + use: home). Riding: Thunder Leap.', 'blue'),
                                                   ('Give him a gem: his element. The Ethereal', 'blue'), ('Gem: his Ethereal Form - and he flies.', 'blue'),
                                                   ('If he falls: 5 minutes.', 'gray')],
     model='bm:kw_spark', glint=True, stack=1, cat='magic', comps=hold('none'), tier=3)
HOLD['kw_spark'] = 'bm:p79/spark'


def extend_offers(O, offer):
    # his Tendrils come from him now, not from Cecil (and his Effigy from Democratus' duel - 2.79b - not from Cecil either)
    O['wizard'] = [o for o in O['wizard'] if (o['sell'].get('components') or {}).get('minecraft:custom_data', {}).get('bm') != 'killerwatt_tendrils']


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    tick, fast, second = [], [], []
    ident = [F(0), F(0), F(0), F(1)]
    qf = lambda q: [F(round(v, 4)) for v in q]
    eff = lambda e: {'id': f'minecraft:{e}', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}
    attr = lambda **kw: [{'id': f'minecraft:{k}', 'base': D(v)} for k, v in kw.items()]
    objs = ['bm.kxid', 'bm.kxf', 'bm.kxs', 'bm.kxatk', 'bm.kxt', 'bm.kxc', 'bm.kxr', 'bm.kxlone', 'bm.kxk', 'bm.kxcd', 'bm.fgk', 'bm.kxel', 'bm.kxlt', 'bm.kxch']
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
                                    'scale': [F(S * (ART.TEND_K if p in ART.TEND_PARTS else 1))] * 3}}
            if boss:
                n['brightness'] = {'sky': Int(12), 'block': Int(12)}         # (a storm at night: he glows a little, so you can see him coming)
            return snbt(n)
        # (as the host, at it; #kid its link) a fresh set of parts
        fn(f'p79/{kind}/rig', [f'summon minecraft:item_display ~ ~ ~ {part_nbt(p)}' for p in ART.PARTS] +
           ['scoreboard players operation @e[type=minecraft:item_display,tag=bm.kxnew,distance=..1] bm.kxid = #kid bm.rng',
            'execute if score @s bm.pid matches 1.. run scoreboard players operation @e[type=minecraft:item_display,tag=bm.kxnew,distance=..1] bm.pid = @s bm.pid',
            'tag @e[type=minecraft:item_display,tag=bm.kxnew,distance=..1] add bm.kxsel', 'tag @e[type=minecraft:item_display,tag=bm.kxnew] remove bm.kxnew',
            'scoreboard players set @s bm.kxs -1'])
        fn(f'p79/{kind}/rerig', [f'kill {sel()}', f'function bm:p79/{kind}/rig'])
        # (rotated with the host) design +x is his right = ^-x; design -z his front = ^+z
        fn(f'p79/{kind}/place', [f'execute positioned ^{-x * U:.4f} ^{y * U:.4f} ^{-z * U:.4f} run tp {sel(p)} ~ ~ ~ ~ 0' for p, (x, y, z) in ART.PIVOT.items()])
        # poses: the same quaternions at either size; the lift scales with him
        for name, pose in ART.POSES.items():
            d = (DUR if boss else PET_DUR)[name]
            def xf(p):
                rot, (ox, oy, oz), dy = ART.part_xf(pose, p)                    # (2.67: children ride the torso's lean)
                return (f'left_rotation:{snbt(qf(rot))},translation:[{ox * U:.4f}f,{oy * U + dy * S / ART.RIG_SCALE:.4f}f,{oz * U:.4f}f]')
            fn(f'p79/{kind}/pose/{name}', [f'execute as {sel(p)} run data merge entity @s {{start_interpolation:0,interpolation_duration:{d},transformation:{{{xf(p)}}}}}'
                                           for p in ART.PARTS])
        # the heartbeat (as the host, at it): find his parts (or make them), stand them up, attack or move
        fn(f'p79/{kind}/tick', ['scoreboard players add @s bm.kxf 1', 'scoreboard players operation #kid bm.rng = @s bm.kxid',
                                'execute as @e[type=minecraft:item_display,tag=bm.kxp,tag=!bm.kxdying] if score @s bm.kxid = #kid bm.rng run tag @s add bm.kxsel',
                                f'execute unless entity {sel("body")} run function bm:p79/{kind}/rig',
                                f'execute unless entity {sel("tendl")} run function bm:p79/{kind}/rerig',
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
    # (2.67) he goes out in an EXPLOSION OF ELECTRICITY: crumpling, he crackles and charges - then bursts apart in a blinding flash
    fn('p79/fade', ['scoreboard players remove @s bm.kxt 1',
                    'execute if score @s bm.kxt matches 26..34 run particle minecraft:electric_spark ~ ~0.5 ~ 0.4 0.4 0.4 0.2 6',
                    'execute if score @s bm.kxt matches 30 if entity @s[tag=bm.kxp_body] run playsound minecraft:block.beacon.power_select hostile @a[distance=..48] ~ ~ ~ 1.5 0.6',
                    'execute if score @s bm.kxt matches 22..26 if entity @s[tag=bm.kxp_body] run particle minecraft:end_rod ~ ~1 ~ 1 1.5 1 0.2 12',
                    'execute if score @s bm.kxt matches 21 if entity @s[tag=bm.kxp_body] run function bm:p79/boom',
                    'execute if score @s bm.kxt matches 21 run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{scale:[0f,0f,0f]}}',
                    'execute if score @s bm.kxt matches 21 run particle minecraft:electric_spark ~ ~0.5 ~ 0.3 0.3 0.3 0.6 14',
                    'execute if score @s bm.kxt matches ..16 run kill @s'])
    fn('p79/boom', ['particle minecraft:flash{color:[0.8,1.0,0.6,1.0]} ~ ~1.5 ~ 0 0 0 0 1', 'particle minecraft:explosion_emitter ~ ~1.5 ~ 0 0 0 0 1',
                    'particle minecraft:electric_spark ~ ~1.5 ~ 0.4 0.4 0.4 1.4 400', 'particle minecraft:end_rod ~ ~1.5 ~ 0.2 0.2 0.2 0.6 120',
                    'particle minecraft:dust{color:[0.55,1.0,0.35],scale:2.5} ~ ~1.5 ~ 2.5 2 2.5 0 120'] +
       [f'particle minecraft:end_rod ~{dx} ~{y} ~{dz} 0.05 0.3 0.05 0 3' for dx, dz in ((0, 0), (2.5, 1), (-2, -2), (1, -2.5), (-2.5, 1.5)) for y in range(0, 14, 2)] +
       ['playsound minecraft:entity.lightning_bolt.thunder hostile @a[distance=..96] ~ ~ ~ 2 0.8', 'playsound minecraft:entity.lightning_bolt.impact hostile @a[distance=..48] ~ ~ ~ 2 0.7',
        'playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 1.5 0.6',
        'execute as @a[distance=..10,gamemode=!spectator] at @s run particle minecraft:electric_spark ~ ~1 ~ 0.3 0.6 0.3 0.1 10'])
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
            'attributes': attr(scale=2.4, max_health=BOSS_HP, attack_damage=10, armor=10, armor_toughness=4, movement_speed=0.26, follow_range=48,
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
    # (2.67) his hitbox fits him: the husk itself (scale 2.4: 4.7 high, 1.4 wide) for arrows, and a body-wide box for blows
    #        (phase82's relay passes a hit on it to him, as yours)
    G.FUNCS['p79/boss/tick'][-1:-1] = ['execute as @e[type=minecraft:interaction,tag=bm.bhit_kw,distance=..16] if score @s bm.hbid = #kid bm.rng run tag @s add bm.hbsel',
                                       'execute unless entity @e[type=minecraft:interaction,tag=bm.hbsel,tag=bm.bhit_kw] run function bm:p79/boss/hitbox',
                                       'tp @e[type=minecraft:interaction,tag=bm.hbsel,tag=bm.bhit_kw] ~ ~ ~', 'tag @e[type=minecraft:interaction,tag=bm.hbsel] remove bm.hbsel']
    fn('p79/boss/hitbox', ['summon minecraft:interaction ~ ~ ~ {Tags:["bm.bhit","bm.bhit_kw","bm.hbnew"],width:2.6f,height:4.4f}',
                           'scoreboard players operation @e[type=minecraft:interaction,tag=bm.hbnew] bm.hbid = #kid bm.rng',
                           'tag @e[type=minecraft:interaction,tag=bm.hbnew] add bm.hbsel', 'tag @e[type=minecraft:interaction,tag=bm.hbnew] remove bm.hbnew'])
    # the mind (each tick he isn't mid-attack): every second, maybe start one; 3 seconds between (under 2 once enraged)
    fn('p79/boss/mind', ['scoreboard players remove @s bm.kxc 1', 'execute if score @s bm.kxc matches 1.. run return 0', 'scoreboard players set @s bm.kxc 20',
                         'execute store result score #hp bm.rng run data get entity @s Health', 'execute store result score #mx bm.rng run attribute @s minecraft:max_health get',
                         'scoreboard players operation #mx bm.rng /= #2 bm.rng',
                         'execute if score @s bm.kxr matches 0 if score #hp bm.rng <= #mx bm.rng run return run function bm:p79/boss/start {a:4}',
                         'execute store result score #r bm.rng run random value 1..100',
                         'execute if entity @a[distance=..5.5,gamemode=!creative,gamemode=!spectator] if score #r bm.rng matches 1..35 run return run function bm:p79/boss/start {a:1}',
                         'execute if entity @a[distance=..7,gamemode=!creative,gamemode=!spectator] if score #r bm.rng matches 36..60 run return run function bm:p79/boss/start {a:2}',
                         'execute if entity @a[distance=..9,gamemode=!creative,gamemode=!spectator] if score #r bm.rng matches 61..88 run return run function bm:p79/boss/start {a:5}',
                         'execute if entity @a[distance=..28,gamemode=!creative,gamemode=!spectator] if score #r bm.rng matches 60..100 run return run function bm:p79/boss/start {a:3}'])
    fn('p79/boss/start', ['$function bm:p79/boss/go {a:$(a)}', 'execute if score @s bm.kxatk matches 4 run scoreboard players set @s bm.kxr 1',
                          'scoreboard players set @s bm.kxc 60', 'execute if score @s bm.kxr matches 1 run scoreboard players set @s bm.kxc 36',
                          'effect give @s minecraft:slowness 2 6 true'])
    fn('p79/boss/attack', ['scoreboard players add @s bm.kxt 1', 'tag @s add bm.kxme',
                           'execute if score @s bm.kxatk matches 1 run function bm:p79/boss/a_slam', 'execute if score @s bm.kxatk matches 2 run function bm:p79/boss/a_sweep',
                           'execute if score @s bm.kxatk matches 3 run function bm:p79/boss/a_call', 'execute if score @s bm.kxatk matches 4 run function bm:p79/boss/a_roar',
                           'execute if score @s bm.kxatk matches 5 run function bm:p79/boss/a_lunge',
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
    # (2.67) THE TENDRIL LUNGE: he turns on you, coils all four scythes back - and drives them at you
    fn('p79/boss/a_lunge', [at(1, 'execute facing entity @a[distance=..10,gamemode=!creative,gamemode=!spectator,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0'),
                            at(1, 'function bm:p79/boss/pose/lunge_a'), at(1, 'playsound minecraft:entity.warden.sonic_charge hostile @a[distance=..32] ~ ~ ~ 0.8 1.6'),
                            at('2..9', 'particle minecraft:electric_spark ^ ^3.6 ^-1.2 1.2 0.6 0.3 0.05 4'),
                            at(10, 'function bm:p79/boss/pose/lunge_b'), at(12, 'function bm:p79/boss/lunged'), at('26..', 'function bm:p79/boss/done')])
    fn('p79/boss/lunged', ['execute rotated as @s rotated ~ 0 positioned ^ ^2 ^4.2 run particle minecraft:sweep_attack ~ ~ ~ 1.6 0.6 1.6 0 6',
                           'execute rotated as @s rotated ~ 0 positioned ^ ^2 ^4.2 run particle minecraft:electric_spark ~ ~ ~ 1.8 1 1.8 0.3 60',
                           'playsound minecraft:item.trident.hit hostile @a[distance=..32] ~ ~ ~ 1.4 0.6',
                           f'execute rotated as @s rotated ~ 0 positioned ^ ^ ^4.2 as @a[distance=..3.6,gamemode=!creative,gamemode=!spectator] at @s run function bm:p79/boss/skewered'])
    fn('p79/boss/skewered', [f'damage @s 11 minecraft:mob_attack by {me}', 'effect give @s minecraft:slowness 2 3', 'particle minecraft:crit ~ ~1 ~ 0.3 0.6 0.3 0.4 20'])
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
                           'particle minecraft:electric_spark ~ ~1 ~ 2 2 2 0.4 200', 'particle minecraft:flash{color:[0.75,1.0,0.6,1.0]} ~ ~1 ~ 0 0 0 0 1',
                           'function bm:p79/payout'])
    # (2.82) whatever brought him down - a follower, his own lightning, fire, a fall - the reward still comes: the killing-blow
    #  advancement pays the moment he dies; if nobody's paid by the time his body crumples, everyone within 64 is, here
    fn('p79/payout', ['execute store result score #now bm.rng run time query gametime', 'scoreboard players operation #now bm.rng -= #kxpaid bm.rng',
                      'execute if score #now bm.rng matches 0..100 run return 0',
                      'execute store result score #now bm.rng run time query gametime', 'scoreboard players operation #now bm.rng -= #kxalive bm.rng',
                      'execute unless score #now bm.rng matches 0..40 run return 0',          # (a rig left over from long ago pays nobody)
                      'execute store result score #kxpaid bm.rng run time query gametime',
                      'execute unless entity @a[distance=..64,gamemode=!spectator] run return 0',
                      'execute if entity @s[scores={bm.kxel=10}] run return run function bm:p79/payout_eth',
                      'execute as @a[distance=..64,gamemode=!spectator] at @s run function bm:p79/reward',
                      tellraw('@a[distance=..96]', PREFIX + [T('KILLERWATT', GRN, bold=True), T(' has fallen!', 'gray')])])
    fn('p79/payout_eth', ['scoreboard players set #eth bm.kxek 1', 'execute as @a[distance=..64,gamemode=!spectator] at @s run function bm:p79/reward',
                          'execute as @a[distance=..64,gamemode=!spectator] at @s run function bm:p83/eth_reward', 'scoreboard players set #eth bm.kxek 0',
                          tellraw('@a[distance=..96]', PREFIX + [T('ETHEREAL KILLERWATT', GRN, bold=True), T(' has fallen!', 'gray')])])
    # the reward: everyone within 64 of the killing blow
    wjson('bm/advancement/p79/kill.json', {'criteria': {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["bm.kxboss"]}'}},
        {'condition': 'minecraft:inverted', 'term': {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["bm.kxeth"]}'}}}]}}},
        'rewards': {'function': 'bm:p79/killed'}})                      # (his ethereal form: phase83 runs this itself, with #eth set - no plain Tendrils)
    fn('p79/killed', ['advancement revoke @s only bm:p79/kill', 'execute store result score #kxpaid bm.rng run time query gametime', 'execute at @s as @a[distance=..64] at @s run function bm:p79/reward',
                      tellraw('@a', PREFIX + [{'selector': '@s', 'color': 'white'}, T(' brought down ', 'gray'), T('KILLERWATT', GRN, bold=True), T('!', 'gray')])])
    fn('p79/reward', ['scoreboard players add @s bm.kxk 1', 'execute if score @s bm.kxk matches 1 run function bm:p79/first',
                      'execute store result score #r bm.rng run random value 1..100',
                      'execute if score @s bm.kxk matches 2.. if score #r bm.rng matches 1..20 unless score #eth bm.kxek matches 1 run ' + give('killerwatt_tendrils'),
                      'execute if score @s bm.kxk matches 2.. if score #r bm.rng matches 21..30 run ' + give('kw_spark'),
                      'loot give @s loot bm:p79/hoard', 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1'])
    fn('p79/first', ['execute if score #eth bm.kxek matches 1 run return run function bm:p79/first_eth', give('killerwatt_tendrils'), give('kw_spark'),
                     tellraw('@s', PREFIX + [T("KillerWatt's Tendrils", YEL, bold=True), T(' and ', 'gray'), T('his Spark', GRN, bold=True),
                                             T(" are yours - use the Spark and he'll fight beside you.", 'gray')])])
    # (a first win over his ethereal form: the Spark - the Tendrils it gives are the ethereal ones, phase83)
    fn('p79/first_eth', [give('kw_spark'), tellraw('@s', PREFIX + [T('His Spark', GRN, bold=True), T(" is yours - use it and he'll fight beside you.", 'gray')])])
    wjson('bm/loot_table/p79/hoard.json', {'pools': [{'rolls': 1, 'entries': [G.loot_entry('medallion', G.uni(3, 6))]},
                                                     {'rolls': 1, 'entries': [G.loot_entry('trophy', G.uni(1, 2))]},
                                                     {'rolls': 1, 'entries': [G.loot_entry('token', G.uni(4, 9))]}]})

    # ================================================================== THE FOLLOWER
    ETH = len(ART.EL_KEYS) + 1                   # 10: the Ethereal form (1..9: the gems, in Cecil's order; 0 or 5: his own electric)
    SUF = {0: ''} | {i + 1: ('' if k == 'electric' else f'_{k}') for i, k in enumerate(ART.EL_KEYS)} | {ETH: '_eth'}
    pnbt = {'Tags': ['bm.kxpet', 'bm.kxhost', 'bm.kxnew', 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1), 'CustomName': T('KillerWatt', GRN, bold=True),
            'CustomNameVisible': B(0), 'Health': F(PET_HP),
            'attributes': attr(scale=1.7, max_health=PET_HP, armor=8, attack_damage=4, movement_speed=0.33, follow_range=32, step_height=1.25,
                               fall_damage_multiplier=0.0),
            'active_effects': [eff('invisibility')]}
    mine = 'execute as @e[type=minecraft:wolf,tag=bm.kxpet] if score @s bm.pid = #me bm.pid'
    # 2.81: a KillerWatt with no id (one summoned bare, not through his arrival) never finds his own parts and rigs anew every
    # tick, thousands of displays a minute - give him one first
    G.FUNCS['p79/boss/tick'][0:0] = ['execute store result score #kxalive bm.rng run time query gametime',
                                     'execute unless score @s bm.kxid = @s bm.kxid run scoreboard players add #kwn bm.kxid 1',
                                     'execute unless score @s bm.kxid = @s bm.kxid run scoreboard players operation @s bm.kxid = #kwn bm.kxid']
    G.FUNCS['p79/boss/tick'].insert(0, 'scoreboard players set #kel bm.rng 0')      # (first: phase83 swaps this line for its form checks)
    # his parts wear his element (#kel: 0 his own, 1..9 a gem, 10 ethereal); the flexed arms too
    fn('p79/flex', [f'execute if score #kel bm.rng matches {i} run data modify entity @e[type=minecraft:item_display,tag=bm.kxsel,tag=bm.kxp_{p},limit=1] '
                    f'item.components."minecraft:item_model" set value "bm:kw_{p}_flex{s}"' for i, s in SUF.items() for p in ('armr', 'arml')])
    fn('p79/unflex', [f'execute if score #kel bm.rng matches {i} run data modify entity @e[type=minecraft:item_display,tag=bm.kxsel,tag=bm.kxp_{p},limit=1] '
                      f'item.components."minecraft:item_model" set value "bm:kw_{p}{s}"' for i, s in SUF.items() for p in ('armr', 'arml')])
    G.FUNCS['p79/orphan'].insert(0, 'scoreboard players operation #kel bm.rng = @s bm.kxel')
    fn('p79/pet/dress_rig', ['scoreboard players operation #kel bm.rng = @s bm.kxel', f'scoreboard players operation {sel()} bm.kxel = #kel bm.rng'] +
       [f'execute if score #kel bm.rng matches {i} run data modify entity @e[type=minecraft:item_display,tag=bm.kxsel,tag=bm.kxp_{p},limit=1] '
        f'item.components."minecraft:item_model" set value "bm:kw_{p}{s}"' for i, s in SUF.items() for p in ART.PARTS])
    G.FUNCS['p79/pet/rig'].append('function bm:p79/pet/dress_rig')
    fn('p79/pet/redress', ['scoreboard players operation #kid bm.rng = @s bm.kxid',
                           'execute as @e[type=minecraft:item_display,tag=bm.kxp_pet,distance=..12] if score @s bm.kxid = #kid bm.rng run tag @s add bm.kxsel',
                           'function bm:p79/pet/dress_rig', f'tag {sel()} remove bm.kxsel'])

    # ---- the Spark: call him, call him over, climb on (close by), send him home (sneaking); riding, it's his THUNDER LEAP
    fn('p79/spark', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                     'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                     f'{mine} run tag @s add bm.kxsel2',
                     'execute on vehicle if entity @s[tag=bm.kxsel2] at @s run return run function bm:p79/pet/rleap',
                     'execute if entity @e[type=minecraft:wolf,tag=bm.kxsel2] if predicate bm:p20/sneaking run function bm:p79/pet/home',
                     'execute if entity @e[type=minecraft:wolf,tag=bm.kxsel2,distance=..3.5] unless predicate bm:p20/sneaking run function bm:p79/pet/mount',
                     'execute if entity @e[type=minecraft:wolf,tag=bm.kxsel2] unless entity @e[type=minecraft:wolf,tag=bm.kxsel2,distance=..3.5] unless predicate bm:p20/sneaking run function bm:p79/pet/recall',
                     'execute unless entity @e[type=minecraft:wolf,tag=bm.kxsel2] unless predicate bm:p20/sneaking run function bm:p79/pet/try',
                     'execute unless entity @e[type=minecraft:wolf,tag=bm.kxsel2] if predicate bm:p20/sneaking run ' + say("KillerWatt isn't with you. (Use the Spark to call him.)"),
                     'tag @e[type=minecraft:wolf,tag=bm.kxsel2] remove bm.kxsel2'])
    fn('p79/pet/recall', ['tp @e[type=minecraft:wolf,tag=bm.kxsel2,limit=1] @s', 'data modify entity @e[type=minecraft:wolf,tag=bm.kxsel2,limit=1] Sitting set value 0b',
                          'particle minecraft:electric_spark ~ ~1.5 ~ 0.6 1 0.6 0.3 40', 'playsound minecraft:entity.lightning_bolt.impact neutral @a[distance=..16] ~ ~ ~ 0.4 1.8',
                          say('KillerWatt crackles over to you. (Use the Spark beside him to climb on.)', GRN)])
    fn('p79/pet/mount', ['ride @s mount @e[type=minecraft:wolf,tag=bm.kxsel2,limit=1]', 'playsound minecraft:entity.lightning_bolt.impact neutral @a[distance=..16] ~ ~ ~ 0.3 2',
                         'particle minecraft:electric_spark ~ ~1 ~ 0.6 0.6 0.6 0.2 30',
                         title('@s', 'actionbar', [T('On his back. ', GRN, bold=True), T('Walk to stride; jump to hop; walls - he climbs them. The Spark: THUNDER LEAP. ', 'gray'),
                                                   T('Sneak to get off.', 'dark_gray')])])
    fn('p79/pet/home', ['execute as @e[type=minecraft:wolf,tag=bm.kxsel2] at @s run function bm:p79/pet/vanish', say('KillerWatt goes home.', GRN)])
    fn('p79/pet/try', ['execute if score @s bm.kxcd matches 1.. store result score #m bm.rng run scoreboard players get @s bm.kxcd',
                       'execute if score @s bm.kxcd matches 1.. run scoreboard players add #m bm.rng 59', 'execute if score @s bm.kxcd matches 1.. run scoreboard players operation #m bm.rng /= #60 bm.rng',
                       'execute if score @s bm.kxcd matches 1.. run return run ' + title('@s', 'actionbar', [T('KillerWatt is still recharging: about ', 'gray'),
                                                                                                          {'score': {'name': '#m', 'objective': 'bm.rng'}, 'color': 'white'}, T(' min.', 'gray')]),
                       'execute unless function bm:p74/fol_ok run return run ' + say("The Spark won't answer here."),
                       'execute if function bm:p58/full run return 0', 'function bm:p79/pet/summon'])
    fn('p79/pet/summon', ['execute unless score @s bm.kxel matches 0.. run scoreboard players set @s bm.kxel 0',
                          f'execute rotated ~ 0 positioned ^ ^ ^2 run summon minecraft:wolf ~ ~ ~ {snbt(pnbt)}',
                          'data modify entity @e[type=minecraft:wolf,tag=bm.kxnew,limit=1,sort=nearest] Owner set from entity @s UUID',
                          # (a wolf loaded without an owner resets to 8 health; taming it by NBT doesn't put it back - as for Zib)
                          f'attribute @e[type=minecraft:wolf,tag=bm.kxnew,limit=1,sort=nearest] minecraft:max_health base set {PET_HP}',
                          f'data modify entity @e[type=minecraft:wolf,tag=bm.kxnew,limit=1,sort=nearest] Health set value {PET_HP}f',
                          'scoreboard players operation @e[type=minecraft:wolf,tag=bm.kxnew,limit=1,sort=nearest] bm.pid = @s bm.pid',
                          'scoreboard players operation @e[type=minecraft:wolf,tag=bm.kxnew,limit=1,sort=nearest] bm.kxel = @s bm.kxel',
                          'execute as @e[type=minecraft:wolf,tag=bm.kxnew,limit=1,sort=nearest] at @s run function bm:p79/pet/init',
                          'execute rotated ~ 0 positioned ^ ^ ^2 run particle minecraft:electric_spark ~ ~1.5 ~ 0.6 1 0.6 0.3 60',
                          'execute rotated ~ 0 positioned ^ ^ ^2 run particle minecraft:flash{color:[0.75,1.0,0.6,1.0]} ~ ~1 ~ 0 0 0 0 1',
                          'playsound minecraft:entity.lightning_bolt.impact neutral @a[distance=..24] ~ ~ ~ 0.6 1.6', say('KillerWatt answers the Spark.', GRN)])
    fn('p79/pet/init', ['scoreboard players add #kwn bm.kxid 1', 'scoreboard players operation @s bm.kxid = #kwn bm.kxid', 'scoreboard players set @s bm.kxatk 0',
                        'scoreboard players set @s bm.kxc 40', 'scoreboard players set @s bm.kxch 0', 'tag @s remove bm.kxnew', 'scoreboard players operation #kid bm.rng = @s bm.kxid',
                        'function bm:p79/pet/rig', f'tag {sel()} remove bm.kxsel'])
    fn('p79/pet/vanish', ['particle minecraft:electric_spark ~ ~1.5 ~ 0.6 1 0.6 0.3 30', 'execute on passengers run ride @s dismount', 'function bm:p79/unrig',
                          'data remove entity @s Owner', 'tp @s ~ -400 ~', 'kill @s'])
    tick.append('execute as @e[type=minecraft:wolf,tag=bm.kxpet] at @s run function bm:p79/pet/tick')
    # the heartbeat, his way: ridden (his rider steers), hovering (ethereal), climbing to you
    pt = G.FUNCS['p79/pet/tick']
    pt[0:0] = ['scoreboard players operation #kel bm.rng = @s bm.kxel',
               # (store success of `on passengers` stores nothing when there are none - set it first)
               'scoreboard players set #rid bm.rng 0', 'execute on passengers if entity @s[type=minecraft:player] run scoreboard players set #rid bm.rng 1',
               'execute if score #rid bm.rng matches 1 run function bm:p79/pet/ride',
               'execute if score #rid bm.rng matches 0 if entity @s[tag=bm.kxrd] run function bm:p79/pet/unride']
    k_ = next(i for i, l in enumerate(pt) if 'function bm:p79/pet/place' in l)
    pt[k_:k_ + 1] = ['execute if score #rid bm.rng matches 1 rotated as @s rotated ~ 0 positioned ^ ^ ^0.55 run function bm:p79/pet/place',
                     f'execute if score #rid bm.rng matches 0 if score #kel bm.rng matches {ETH} rotated as @s rotated ~ 0 positioned ~ ~0.35 ~ run function bm:p79/pet/place',
                     f'execute if score #rid bm.rng matches 0 unless score #kel bm.rng matches {ETH} rotated as @s rotated ~ 0 run function bm:p79/pet/place']
    k_ = next(i for i, l in enumerate(pt) if 'function bm:p79/pet/move' in l)
    pt[k_] = 'execute unless score @s bm.kxatk matches 1.. unless entity @s[tag=bm.kxclimb] run function bm:p79/pet/move'
    pt.insert(k_, 'execute if score #rid bm.rng matches 0 unless score @s bm.kxatk matches 1.. unless data entity @s {Sitting:1b} run function bm:p79/pet/climb_chk')
    hostile = 'type=#bm:hostile,tag=!bm.npc'
    pme = '@e[type=minecraft:wolf,tag=bm.kxme,limit=1]'

    # ---- riding: his rider's facing is his; walk to stride (6-7 blocks a second), jump to hop, a wall ahead - he climbs it.
    #      Ethereal: he flies - look up to rise, down to sink. (The direction: a marker swung round the coat check's corner, as for the Volley Quiver.)
    fn('p79/pet/ride', ['tag @s add bm.kxdrv', 'tag @s add bm.kxrd', 'data modify entity @s Sitting set value 1b',
                        'attribute @s minecraft:scale modifier add bm:kx_ride 0.5 add_value',
                        'scoreboard players set #fw bm.rng 0', 'scoreboard players set #jp bm.rng 0',
                        'execute on passengers if predicate bm:p39/forward run scoreboard players set #fw bm.rng 1',
                        'execute on passengers if predicate bm:p26/jump_key run scoreboard players set #jp bm.rng 1',
                        'execute on passengers run function bm:p79/pet/rider',
                        'execute on passengers store result score #pitch bm.rng run data get entity @s Rotation[1]',
                        'execute on passengers store result score #yaw bm.rng run data get entity @s Rotation[0] 100',
                        'execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #yaw bm.rng',
                        f'execute if score #kel bm.rng matches {ETH} run data modify entity @s NoGravity set value 1b',
                        'execute if score #fw bm.rng matches 1 run function bm:p79/pet/drive',
                        'execute if score #fw bm.rng matches 0 run data modify entity @s Motion[0] set value 0.0d',
                        'execute if score #fw bm.rng matches 0 run data modify entity @s Motion[2] set value 0.0d',
                        f'execute if score #kel bm.rng matches {ETH} run function bm:p79/pet/fly',
                        f'execute unless score #kel bm.rng matches {ETH} if score #jp bm.rng matches 1 if predicate bm:p39/on_ground run data modify entity @s Motion[1] set value 0.62d',
                        'execute if entity @s[tag=bm.kxleap] run function bm:p79/pet/leap_tick',
                        'tag @s remove bm.kxdrv'])
    fn('p79/pet/drive', ['scoreboard players set #sp bm.rng 340', f'execute if score #kel bm.rng matches {ETH} run scoreboard players set #sp bm.rng 440',
                         'execute store result storage bm:tmp kxd.s double 0.001 run scoreboard players get #sp bm.rng',
                         'function bm:p79/pet/dir with storage bm:tmp kxd',
                         'execute store result entity @s Motion[0] double 0.001 run scoreboard players get #mx bm.rng',
                         'execute store result entity @s Motion[2] double 0.001 run scoreboard players get #mz bm.rng',
                         # a wall ahead: up he goes, tendrils first
                         f'execute unless score #kel bm.rng matches {ETH} rotated as @s rotated ~ 0 positioned ^ ^ ^1.1 unless block ~ ~0.6 ~ #bm:grap_pass run function bm:p79/pet/climb_up',
                         f'execute unless score #kel bm.rng matches {ETH} rotated as @s rotated ~ 0 positioned ^ ^ ^1.1 unless block ~ ~1.6 ~ #bm:grap_pass run function bm:p79/pet/climb_up'])
    # (as the host) #mx, #mz = a step of $(s) blocks along his facing, in thousandths
    fn('p79/pet/dir', ['$execute in bm:gutter positioned -200.0 64.0 -200.0 rotated as @s rotated ~ 0 run summon minecraft:marker ^ ^ ^$(s) {Tags:["bm.kxmv"]}',
                       'execute in bm:gutter store result score #mx bm.rng run data get entity @e[type=minecraft:marker,tag=bm.kxmv,limit=1] Pos[0] 1000',
                       'execute in bm:gutter store result score #mz bm.rng run data get entity @e[type=minecraft:marker,tag=bm.kxmv,limit=1] Pos[2] 1000',
                       'execute in bm:gutter run kill @e[type=minecraft:marker,tag=bm.kxmv]',
                       'scoreboard players operation #mx bm.rng += #200000 bm.rng', 'scoreboard players operation #mz bm.rng += #200000 bm.rng'])
    fn('p79/pet/climb_up', ['data modify entity @s Motion[1] set value 0.32d', 'tag @s add bm.kxclimbing'])
    fn('p79/pet/fly', ['execute if score #pitch bm.rng matches ..-25 run data modify entity @s Motion[1] set value 0.24d',
                       'execute if score #pitch bm.rng matches 40.. run data modify entity @s Motion[1] set value -0.24d',
                       'execute if score #pitch bm.rng matches -24..39 run data modify entity @s Motion[1] set value 0.0d',
                       'particle minecraft:end_rod ~ ~0.3 ~ 0.4 0.1 0.4 0.01 1'])
    fn('p79/pet/rider', ['tag @s add bm.kxrider', 'attribute @s minecraft:fall_damage_multiplier modifier add bm:kx_ride -1 add_multiplied_total'])
    fn('p79/pet/unride', ['tag @s remove bm.kxrd', 'data modify entity @s Sitting set value 0b', 'attribute @s minecraft:scale modifier remove bm:kx_ride',
                          'data modify entity @s NoGravity set value 0b', 'tag @s remove bm.kxleap', 'tag @s remove bm.kxclimb', 'scoreboard players set @s bm.kxs -1'])
    second += ['execute as @a[tag=bm.kxrider] unless function bm:p79/pet/on_kw run function bm:p79/pet/rider_off']
    fn('p79/pet/on_kw', ['execute on vehicle if entity @s[type=minecraft:wolf,tag=bm.kxpet] run return 1', 'return 0'])
    fn('p79/pet/rider_off', ['tag @s remove bm.kxrider', 'attribute @s minecraft:fall_damage_multiplier modifier remove bm:kx_ride'])
    # THUNDER LEAP (the Spark, riding): up and forward - and where he lands, a slam
    fn('p79/pet/rleap', ['tag @s remove bm.kxsel2', 'execute unless predicate bm:p39/on_ground run return 0', 'execute if entity @s[tag=bm.kxleap] run return 0',
                         'tag @s add bm.kxleap', 'scoreboard players set @s bm.kxlt 0', 'scoreboard players set #kel bm.rng 0',
                         'scoreboard players operation #kel bm.rng = @s bm.kxel', 'scoreboard players operation #kid bm.rng = @s bm.kxid',
                         'execute as @e[type=minecraft:item_display,tag=bm.kxp_pet,distance=..12] if score @s bm.kxid = #kid bm.rng run tag @s add bm.kxsel',
                         'function bm:p79/pet/pose/slam_up', 'function bm:p79/flex', f'tag {sel()} remove bm.kxsel',
                         'data modify storage bm:tmp kxd.s set value 0.55d', 'function bm:p79/pet/dir with storage bm:tmp kxd',
                         'execute store result entity @s Motion[0] double 0.001 run scoreboard players get #mx bm.rng',
                         'execute store result entity @s Motion[2] double 0.001 run scoreboard players get #mz bm.rng',
                         'data modify entity @s Motion[1] set value 0.95d', 'data modify entity @s NoGravity set value 0b',
                         'particle minecraft:electric_spark ~ ~0.3 ~ 0.8 0.1 0.8 0.3 40', 'playsound minecraft:entity.breeze.jump neutral @a[distance=..24] ~ ~ ~ 1 0.7'])
    fn('p79/pet/leap_tick', ['scoreboard players add @s bm.kxlt 1', 'execute if score @s bm.kxlt matches ..5 run return 0',
                             'execute if score @s bm.kxlt matches ..60 unless predicate bm:p39/on_ground run return 0',
                             'tag @s remove bm.kxleap', 'tag @s add bm.kxme', 'function bm:p79/pet/pose/slam_dn', 'function bm:p79/unflex', 'function bm:p79/pet/quake',
                             'execute as @e[type=#bm:hostile,tag=!bm.npc,distance=..6,sort=nearest,limit=2] at @s run function bm:p79/mark_m', 'tag @s remove bm.kxme',
                             'scoreboard players set @s bm.kxs -1'])
    # ---- climbing to you: you're up a wall and he isn't - he goes up it on his tendrils
    fn('p79/pet/climb_chk', ['scoreboard players set #cl bm.rng 0', 'execute on owner if entity @s[distance=..14] run tag @s add bm.kxown',
                             'execute unless entity @a[tag=bm.kxown] run return run function bm:p79/pet/climb_end',
                             'execute store result score #oy bm.rng run data get entity @a[tag=bm.kxown,limit=1] Pos[1] 10',
                             'execute store result score #wy bm.rng run data get entity @s Pos[1] 10', 'scoreboard players operation #oy bm.rng -= #wy bm.rng',
                             # (a climb starts when you're well above him - over 2.2 blocks, past what he steps up - and goes on while you're above at all)
                             'scoreboard players set #up bm.rng 0', 'execute if score #oy bm.rng matches 22.. run scoreboard players set #up bm.rng 1',
                             'execute if entity @s[tag=bm.kxclimb] if score #oy bm.rng matches 1.. run scoreboard players set #up bm.rng 1',
                             'execute if score #up bm.rng matches 1 facing entity @a[tag=bm.kxown,limit=1] feet rotated ~ 0 positioned ^ ^ ^1.2 unless block ~ ~0.6 ~ #bm:grap_pass run scoreboard players set #cl bm.rng 1',
                             'execute if score #up bm.rng matches 1 facing entity @a[tag=bm.kxown,limit=1] feet rotated ~ 0 positioned ^ ^ ^1.2 unless block ~ ~1.6 ~ #bm:grap_pass run scoreboard players set #cl bm.rng 1',
                             'execute if score #cl bm.rng matches 1 unless entity @s[tag=bm.kxclimb] run function bm:p79/pet/climb_start',
                             'tag @a[tag=bm.kxown] remove bm.kxown',
                             'execute if score #cl bm.rng matches 1 run return run function bm:p79/pet/climb_go',
                             # (over the top: a push over the lip until he's on his feet)
                             'execute if entity @s[tag=bm.kxclimb] unless predicate bm:p39/on_ground run return run function bm:p79/pet/climb_crest',
                             'function bm:p79/pet/climb_end'])
    fn('p79/pet/climb_go', ['data modify entity @s Motion[1] set value 0.3d', 'data modify storage bm:tmp kxd.s set value 0.08d', 'function bm:p79/pet/dir with storage bm:tmp kxd',
                            'execute store result entity @s Motion[0] double 0.001 run scoreboard players get #mx bm.rng',
                            'execute store result entity @s Motion[2] double 0.001 run scoreboard players get #mz bm.rng',
                            'particle minecraft:electric_spark ~ ~1 ~ 0.4 0.4 0.4 0.05 1'])
    fn('p79/pet/climb_crest', ['data modify storage bm:tmp kxd.s set value 0.25d', 'function bm:p79/pet/dir with storage bm:tmp kxd',
                               'execute store result entity @s Motion[0] double 0.001 run scoreboard players get #mx bm.rng',
                               'execute store result entity @s Motion[2] double 0.001 run scoreboard players get #mz bm.rng'])
    fn('p79/pet/climb_start', ['tag @s add bm.kxclimb', 'execute facing entity @a[tag=bm.kxown,limit=1] feet run tp @s ~ ~ ~ ~ 0',
                               'scoreboard players operation #kid bm.rng = @s bm.kxid',
                               'execute as @e[type=minecraft:item_display,tag=bm.kxp_pet,distance=..12] if score @s bm.kxid = #kid bm.rng run tag @s add bm.kxsel',
                               'function bm:p79/pet/pose/climb', f'tag {sel()} remove bm.kxsel', 'playsound minecraft:block.chain.step neutral @a[distance=..16] ~ ~ ~ 1 0.6'])
    fn('p79/pet/climb_end', ['execute unless entity @s[tag=bm.kxclimb] run return 0', 'tag @s remove bm.kxclimb', 'scoreboard players set @s bm.kxs -1'])
    # the ethereal one floats, and never falls
    second += [f'execute as @e[type=minecraft:wolf,tag=bm.kxpet,scores={{bm.kxel={ETH}}}] at @s run function bm:p79/pet/eth_sec']
    fn('p79/pet/eth_sec', ['effect give @s minecraft:slow_falling 3 0 true', 'particle minecraft:end_rod ~ ~1.4 ~ 0.6 0.9 0.6 0.02 4',
                           'particle minecraft:dust{color:[0.7,0.5,1.0],scale:1.2} ~ ~0.2 ~ 0.5 0.05 0.5 0 6'])

    # ---- the mind: close - the tendril stab or the slam; a little way off - the leap or chain lightning; far - call lightning
    fn('p79/pet/mind', ['scoreboard players remove @s bm.kxc 1', 'execute if score @s bm.kxc matches 1.. run return 0', 'scoreboard players set @s bm.kxc 10',
                        'execute if data entity @s {Sitting:1b} unless score #rid bm.rng matches 1 run return 0',
                        'execute store result score #r bm.rng run random value 1..100',
                        f'execute if entity @e[{hostile},distance=..3.5] if score #r bm.rng matches 1..55 run return run function bm:p79/pet/start {{a:4}}',
                        f'execute if entity @e[{hostile},distance=..4.5] run return run function bm:p79/pet/start {{a:1}}',
                        f'execute if score #rid bm.rng matches 0 if entity @e[{hostile},distance=5..10] if score #r bm.rng matches 1..50 run return run function bm:p79/pet/start {{a:5}}',
                        f'execute if entity @e[{hostile},distance=..10] run return run function bm:p79/pet/start {{a:6}}',
                        f'execute if entity @e[{hostile},distance=..16] run return run function bm:p79/pet/start {{a:3}}'])
    fn('p79/pet/start', ['$function bm:p79/pet/go {a:$(a)}', 'scoreboard players set @s bm.kxc 60', f'execute if score #kel bm.rng matches {ETH} run scoreboard players set @s bm.kxc 40'])
    fn('p79/pet/attack', ['scoreboard players add @s bm.kxt 1', 'tag @s add bm.kxme'] +
       [f'execute if score @s bm.kxatk matches {a} run function bm:p79/pet/a_{n}' for a, n in ((1, 'slam'), (3, 'call'), (4, 'stab'), (5, 'leap'), (6, 'chain'))] +
       ['tag @s remove bm.kxme'])
    # every blow: x1.5 ethereal, and the element's touch
    for d in (4, 5, 6, 8):
        fn(f'p79/pet/hit{d}', [f'execute if score #kel bm.rng matches {ETH} run damage @s {d * 1.5:g} minecraft:mob_attack by {pme}',
                               f'execute unless score #kel bm.rng matches {ETH} run damage @s {d} minecraft:mob_attack by {pme}', 'function bm:p79/pet/touch'])
    el = {k: i + 1 for i, k in enumerate(ART.EL_KEYS)}
    fn('p79/pet/touch', [f'execute if score #kel bm.rng matches {el["fire"]} run data modify entity @s Fire set value 80s',
                         f'execute if score #kel bm.rng matches {el["water"]} run effect give @s minecraft:slowness 3 1',
                         f'execute if score #kel bm.rng matches {el["water"]} run particle minecraft:splash ~ ~1 ~ 0.4 0.5 0.4 0.1 20',
                         f'execute if score #kel bm.rng matches {el["poison"]} run effect give @s minecraft:poison 4 1',
                         f'execute if score #kel bm.rng matches {el["earth"]} run effect give @s minecraft:slowness 3 3',
                         f'execute if score #kel bm.rng matches {el["rock"]} run effect give @s minecraft:weakness 5 1',
                         f'execute if score #kel bm.rng matches {el["air"]} run effect give @s minecraft:levitation 1 4',
                         f'execute if score #kel bm.rng matches {el["grass"]} run effect give {pme} minecraft:regeneration 3 1',
                         f'execute if score #kel bm.rng matches {el["ice"]} run data modify entity @s TicksFrozen set value 200',
                         f'execute if score #kel bm.rng matches {el["ice"]} run effect give @s minecraft:slowness 3 2',
                         f'execute if score #kel bm.rng matches {ETH} run effect give @s minecraft:wither 3 1',
                         f'execute if score #kel bm.rng matches {ETH} run particle minecraft:end_rod ~ ~1 ~ 0.3 0.5 0.3 0.1 12',
                         f'execute if score #kel bm.rng matches {el["electric"]} run effect give @s minecraft:glowing 3 0',
                         'execute if score #kel bm.rng matches 0 run effect give @s minecraft:glowing 3 0',
                         'particle minecraft:electric_spark ~ ~1 ~ 0.3 0.4 0.3 0.2 10'])
    fn('p79/pet/a_slam', [at(1, 'function bm:p79/pet/pose/slam_up'), at(1, 'function bm:p79/flex'), at(9, 'function bm:p79/pet/pose/slam_dn'),
                          at(9, 'function bm:p79/unflex'), at(11, 'function bm:p79/pet/quake'), at('20..', 'function bm:p79/pet/done')])
    fn('p79/pet/quake', ['particle minecraft:explosion ~ ~0.3 ~ 1.5 0.1 1.5 0 5', 'particle minecraft:electric_spark ~ ~0.3 ~ 2.5 0.1 2.5 0.3 70',
                         'playsound minecraft:entity.generic.explode neutral @a[distance=..24] ~ ~ ~ 0.7 0.9',
                         f'execute as @e[{hostile},distance=..4.5] at @s run function bm:p79/pet/hit8'])
    fn('p79/pet/a_call', [at(1, 'function bm:p79/pet/pose/call'), at('2..14', 'particle minecraft:end_rod ~ ~3.6 ~ 0.4 0.4 0.4 0.04 2'),
                          at(6, f'execute as @e[{hostile},distance=..16,sort=nearest,limit=1] at @s run function bm:p79/mark_m'),
                          at(6, f'execute if score #kel bm.rng matches {ETH} as @e[{hostile},distance=..16,sort=furthest,limit=1] at @s run function bm:p79/mark_m'),
                          at(6, 'playsound minecraft:entity.lightning_bolt.thunder neutral @a[distance=..32] ~ ~ ~ 0.4 1.4'),
                          at('20..', 'function bm:p79/pet/done')])
    # THE TENDRIL STAB: the scythes drive down and pin it - then a right, and a left
    fn('p79/pet/a_stab', [at(1, 'function bm:p79/pet/pose/stab'), at(1, 'playsound minecraft:item.trident.throw neutral @a[distance=..16] ~ ~ ~ 1 0.6'),
                          at(1, f'execute if score #rid bm.rng matches 0 facing entity @e[{hostile},distance=..5,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0'),
                          at(4, f'execute as @e[{hostile},distance=..5,sort=nearest,limit=1] at @s run function bm:p79/pet/pin'),
                          at(9, 'function bm:p79/pet/pose/punch_r'), at(11, 'execute as @e[tag=bm.kxpin,distance=..6] at @s run function bm:p79/pet/punch'),
                          at(15, 'function bm:p79/pet/pose/punch_l'), at(17, 'execute as @e[tag=bm.kxpin,distance=..6] at @s run function bm:p79/pet/punch'),
                          at('24..', 'tag @e[tag=bm.kxpin,distance=..8] remove bm.kxpin'), at('24..', 'function bm:p79/pet/done')])
    fn('p79/pet/pin', ['tag @s add bm.kxpin', 'function bm:p79/pet/hit5', 'effect give @s minecraft:slowness 2 9 true', 'effect give @s minecraft:jump_boost 2 200 true',
                       'particle minecraft:crit ~ ~0.6 ~ 0.3 0.2 0.3 0.3 16', 'particle minecraft:electric_spark ~ ~0.2 ~ 0.6 0.05 0.6 0.1 20',
                       'playsound minecraft:item.trident.hit neutral @a[distance=..16] ~ ~ ~ 1 0.7'])
    fn('p79/pet/punch', ['function bm:p79/pet/hit4', 'particle minecraft:crit ~ ~1 ~ 0.3 0.4 0.3 0.4 10',
                         'playsound minecraft:entity.player.attack.strong neutral @a[distance=..16] ~ ~ ~ 1 0.7'])
    # THE LEAP: a crouch, up and over to it, and down on it
    fn('p79/pet/a_leap', [at(1, 'function bm:p79/pet/pose/crouch'),
                          at(1, f'execute if score #rid bm.rng matches 0 facing entity @e[{hostile},distance=..12,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0'),
                          at(6, 'function bm:p79/pet/pose/slam_up'), at(6, 'function bm:p79/flex'), at(6, 'function bm:p79/pet/launch'),
                          at('10..59', 'execute if predicate bm:p39/on_ground run scoreboard players set @s bm.kxt 60'),
                          at(60, 'function bm:p79/pet/pose/slam_dn'), at(60, 'function bm:p79/unflex'), at(60, 'function bm:p79/pet/quake'),
                          at(60, f'execute as @e[{hostile},distance=..5,sort=nearest,limit=1] at @s run function bm:p79/mark_m'),
                          at('70..', 'function bm:p79/pet/done')])
    fn('p79/pet/launch', ['scoreboard players set #dd bm.rng 500', 'execute store result storage bm:tmp kxd.s double 0.001 run scoreboard players get #dd bm.rng',
                          'function bm:p79/pet/dir with storage bm:tmp kxd',
                          'execute store result entity @s Motion[0] double 0.001 run scoreboard players get #mx bm.rng',
                          'execute store result entity @s Motion[2] double 0.001 run scoreboard players get #mz bm.rng', 'data modify entity @s Motion[1] set value 0.8d',
                          'particle minecraft:electric_spark ~ ~0.3 ~ 0.8 0.1 0.8 0.3 40', 'playsound minecraft:entity.breeze.jump neutral @a[distance=..24] ~ ~ ~ 1 0.8'])
    # CHAIN LIGHTNING: from his hands to three foes in a crackling line
    fn('p79/pet/a_chain', [at(1, 'function bm:p79/pet/pose/punch_r'), at(1, 'playsound minecraft:block.beacon.power_select neutral @a[distance=..16] ~ ~ ~ 0.8 2'),
                           at('1..6', 'particle minecraft:electric_spark ~ ~1.6 ~ 0.4 0.3 0.4 0.2 6'),
                           at(7, f'execute as @e[{hostile},distance=..10,sort=nearest,limit=3] at @s run function bm:p79/pet/arc'),
                           at(7, 'playsound minecraft:entity.lightning_bolt.impact neutral @a[distance=..24] ~ ~ ~ 0.6 1.8'),
                           at('18..', 'function bm:p79/pet/done')])
    fn('p79/pet/arc', ['function bm:p79/pet/hit6', 'scoreboard players set #st bm.rng 0',
                       f'execute positioned ~ ~1 ~ facing entity {pme} eyes run function bm:p79/pet/arc_ray'])
    fn('p79/pet/arc_ray', ['particle minecraft:electric_spark ~ ~ ~ 0.05 0.05 0.05 0 2', 'particle minecraft:end_rod ~ ~ ~ 0 0 0 0 1',
                           'scoreboard players add #st bm.rng 1', 'execute if score #st bm.rng matches 30.. run return 0',
                           'execute if entity @e[type=minecraft:wolf,tag=bm.kxme,limit=1,distance=..1.6] run return 0', 'execute positioned ^ ^ ^0.4 run function bm:p79/pet/arc_ray'])
    # he falls: the owner waits five minutes
    fn('p79/pet/fallen', ['scoreboard players operation #me bm.pid = @s bm.pid', 'particle minecraft:electric_spark ~ ~1 ~ 0.8 0.8 0.8 0.3 60',
                          'playsound minecraft:entity.lightning_bolt.impact neutral @a[distance=..24] ~ ~ ~ 0.6 0.6',
                          f'execute as @a if score @s bm.pid = #me bm.pid run scoreboard players set @s bm.kxcd {PET_CD}',
                          'execute as @a if score @s bm.pid = #me bm.pid run ' + tellraw('@s', PREFIX + [T('KillerWatt falls! ', GRN, bold=True),
                                                                                                          T(f'The Spark needs {PET_CD // 60} minutes to recharge.', 'gray')])])
    second += ['scoreboard players remove @a[scores={bm.kxcd=1..}] bm.kxcd 1',
               'execute as @e[type=minecraft:wolf,tag=bm.kxpet] at @s unless entity @e[type=#bm:hostile,tag=!bm.npc,distance=..16] run effect give @s minecraft:regeneration 3 0 true']

    # ---- (2.67) THE CHARGED ATTACKS: every blow he lands (and every second of a fight) charges him; at 14 he unleashes his
    #      form's - and riding, the Spark lets it go when you choose. One per form, and none of them gentle.
    CHMAX = 14
    ULT = {0: ('storm', 'STORMBREAKER', '#f6e030', (1.0, 0.9, 0.2)), el['electric']: ('storm', 'STORMBREAKER', '#f6e030', (1.0, 0.9, 0.2)),
           el['fire']: ('nova', 'SUPERNOVA', '#ff7a2a', (1.0, 0.45, 0.12)), el['water']: ('maelstrom', 'MAELSTROM', '#3a9cff', (0.2, 0.55, 1.0)),
           el['poison']: ('plague', 'PLAGUE BLOOM', '#a64ce8', (0.65, 0.3, 0.9)), el['earth']: ('tectonic', 'TECTONIC SLAM', '#9a7a4a', (0.6, 0.45, 0.25)),
           el['rock']: ('avalanche', 'AVALANCHE', '#b09070', (0.65, 0.55, 0.45)), el['air']: ('tempest', 'TEMPEST', '#d8f2ff', (0.88, 0.96, 1.0)),
           el['grass']: ('overgrowth', 'OVERGROWTH', '#52d24a', (0.35, 0.85, 0.3)), el['ice']: ('zero', 'ABSOLUTE ZERO', '#a8ecff', (0.65, 0.92, 1.0)),
           ETH: ('void', 'VOID REQUIEM', '#c8a0ff', (0.75, 0.55, 1.0))}
    foe = lambda r, lo=None: f'@e[type=#bm:hostile,tag=!bm.npc,distance={lo or ""}..{r}]'
    for d in (4, 5, 6, 8):
        G.FUNCS[f'p79/pet/hit{d}'].append(f'scoreboard players add {pme} bm.kxch 1')
    for d in (4, 5, 6, 8, 10, 12, 14, 15, 16, 18, 20, 22):
        fn(f'p79/pet/uhit{d}', [f'execute if score #kel bm.rng matches {ETH} run damage @s {d * 1.5:g} minecraft:mob_attack by {pme}',
                                f'execute unless score #kel bm.rng matches {ETH} run damage @s {d} minecraft:mob_attack by {pme}', 'function bm:p79/pet/touch'])
    second += [f'execute as @e[type=minecraft:wolf,tag=bm.kxpet] at @s if entity {foe(16)} unless score @s bm.kxch matches {CHMAX}.. run scoreboard players add @s bm.kxch 1',
               f'execute as @e[type=minecraft:wolf,tag=bm.kxpet,scores={{bm.kxch={CHMAX}..}}] at @s run function bm:p79/pet/charged_sec']
    fn('p79/pet/charged_sec', ['scoreboard players operation #kel bm.rng = @s bm.kxel'] +
       [f'execute if score #kel bm.rng matches {i} run particle minecraft:dust{{color:[{c[0]},{c[1]},{c[2]}],scale:1.6}} ~ ~1.6 ~ 0.6 0.9 0.6 0 10' for i, (_k, _n, _h, c) in ULT.items()] +
       ['particle minecraft:electric_spark ~ ~1.6 ~ 0.6 0.9 0.6 0.2 6',
        'execute unless entity @s[tag=bm.kxcharged] on owner run ' + title('@s', 'actionbar', [T('⚡ KillerWatt is CHARGED', '#f6e030', bold=True),
                                                                                             T(' - he lets it go on the next foe (riding: the Spark).', 'gray')]),
        'execute unless entity @s[tag=bm.kxcharged] run playsound minecraft:block.beacon.power_select neutral @a[distance=..16] ~ ~ ~ 0.8 1.6',
        'tag @s add bm.kxcharged'])
    pm = G.FUNCS['p79/pet/mind']
    k_ = next(i for i, l in enumerate(pm) if 'random value 1..100' in l)
    pm.insert(k_, f'execute if score @s bm.kxch matches {CHMAX}.. if entity {foe(12)} run return run function bm:p79/pet/start {{a:7}}')
    G.FUNCS['p79/pet/attack'].insert(-1, 'execute if score @s bm.kxatk matches 7 run function bm:p79/pet/a_ult')
    rl = G.FUNCS['p79/pet/rleap']
    rl.insert(1, f'execute if score @s bm.kxch matches {CHMAX}.. unless score @s bm.kxatk matches 1.. run return run function bm:p79/pet/go {{a:7}}')
    fn('p79/pet/a_ult', [at(1, 'tag @s add bm.kxult'), at(1, 'function bm:p79/pet/pose/charge'), at(1, 'function bm:p79/flex'),
                         at(1, 'effect give @s minecraft:resistance 3 3 true'), at(1, 'playsound minecraft:block.beacon.activate neutral @a[distance=..32] ~ ~ ~ 1.2 0.7'),
                         at(1, 'playsound minecraft:entity.warden.sonic_charge neutral @a[distance=..32] ~ ~ ~ 1 1.2'),
                         at('2..18', 'function bm:p79/pet/ult_gather'), at(19, 'function bm:p79/pet/pose/release'), at(19, 'function bm:p79/unflex'),
                         at(20, 'function bm:p79/pet/ult_name')] +
       [at(20, f'execute if score #kel bm.rng matches {i} run function bm:p79/pet/ult/{k}') for i, (k, _n, _h, _c) in ULT.items()] +
       [at('21..55', f'execute if score #kel bm.rng matches {i} run function bm:p79/pet/ultb/{k}') for i, (k, _n, _h, _c) in ULT.items() if k in
        ('nova', 'maelstrom', 'plague', 'tectonic', 'tempest', 'overgrowth', 'zero', 'void')] +
       [at('56..', 'scoreboard players set @s bm.kxch 0'), at('56..', 'tag @s remove bm.kxcharged'), at('56..', 'tag @s remove bm.kxult'),
        at('56..', 'function bm:p79/pet/done')])
    fn('p79/pet/ult_gather', [f'execute if score #kel bm.rng matches {i} run particle minecraft:dust{{color:[{c[0]},{c[1]},{c[2]}],scale:2.0}} ~ ~2.2 ~ 2.5 1.5 2.5 0 14'
                              for i, (_k, _n, _h, c) in ULT.items()] +
                             ['particle minecraft:electric_spark ~ ~3 ~ 0.3 0.3 0.3 0.4 10', 'particle minecraft:end_rod ~ ~3.2 ~ 0.2 0.2 0.2 0.02 2'])
    fn('p79/pet/ult_name', [f'execute if score #kel bm.rng matches {i} run ' + title('@a[distance=..32]', 'actionbar', [T('KillerWatt: ', 'gray'), T(n, h, bold=True)])
                            for i, (_k, n, h, _c) in ULT.items()] +
                           ['particle minecraft:flash{color:[1.0,1.0,1.0,1.0]} ~ ~2 ~ 0 0 0 0 1', 'playsound minecraft:entity.lightning_bolt.thunder neutral @a[distance=..48] ~ ~ ~ 1 0.8'])
    atk = lambda d, r, lo=None: f'execute as {foe(r, lo)} at @s run function bm:p79/pet/uhit{d}'
    ring = lambda part, r, n=24: [f'particle {part} ^{r * math.cos(2 * math.pi * k / n):.2f} ^0.4 ^{r * math.sin(2 * math.pi * k / n):.2f} 0.1 0.1 0.1 0.02 3' for k in range(n)]
    beat = lambda t, cmd: f'execute if score @s bm.kxt matches {t} run {cmd}'
    # STORMBREAKER (his own): a blast of lightning round him, then a bolt on every foe and a ring of them
    fn('p79/pet/ult/storm', [atk(14, 10), f'effect give {foe(10)} minecraft:slowness 3 3', 'particle minecraft:electric_spark ~ ~1 ~ 5 1 5 0.6 300'] +
       [f'execute positioned ^{5 * math.cos(2 * math.pi * k / 8):.2f} ^ ^{5 * math.sin(2 * math.pi * k / 8):.2f} run function bm:p79/mark_m' for k in range(8)] +
       [f'execute as {foe(12)} at @s run function bm:p79/mark_m'])
    # SUPERNOVA (fire): a fireball bursting out of him, then a second wave of flame
    fn('p79/pet/ult/nova', [atk(18, 9), f'execute as {foe(9)} run data modify entity @s Fire set value 200s', 'particle minecraft:explosion_emitter ~ ~1 ~ 0 0 0 0 1',
                            'particle minecraft:flame ~ ~1 ~ 4 1.5 4 0.3 400', 'particle minecraft:lava ~ ~1 ~ 3 1 3 0 60',
                            'playsound minecraft:entity.generic.explode neutral @a[distance=..40] ~ ~ ~ 1.5 0.6'])
    fn('p79/pet/ultb/nova', [beat(28, atk(6, 10)), beat(28, 'particle minecraft:soul_fire_flame ~ ~0.5 ~ 5 0.4 5 0.1 300')] +
       [beat(28, c) for c in ring('minecraft:flame', 8)])
    # MAELSTROM (water): a whirlpool drags them in, round and round - then it crashes down
    fn('p79/pet/ult/maelstrom', [f'effect give {foe(11)} minecraft:slowness 5 4', 'particle minecraft:splash ~ ~1 ~ 6 1 6 0.3 300',
                                 'playsound minecraft:entity.generic.splash neutral @a[distance=..32] ~ ~ ~ 1.5 0.5'])
    fn('p79/pet/ultb/maelstrom', [beat(t, f'execute as {foe(11)} at @s facing entity {pme} feet run tp @s ^0.8 ^ ^1.4') for t in (24, 27, 30, 33)] +
       [beat(t, atk(4, 11)) for t in (24, 30)] + [beat(t, 'particle minecraft:bubble_column_up ~ ~0.5 ~ 4 0.2 4 0.1 120') for t in (24, 27, 30, 33)] +
       [beat(36, atk(16, 6)), beat(36, f'effect give {foe(6)} minecraft:nausea 6 0'), beat(36, 'particle minecraft:splash ~ ~2 ~ 3 2 3 0.6 600'),
        beat(36, 'playsound minecraft:entity.player.splash.high_speed neutral @a[distance=..32] ~ ~ ~ 1.5 0.6')])
    # PLAGUE BLOOM (poison): a burst of venom, then the cloud keeps on eating at them
    fn('p79/pet/ult/plague', [atk(12, 10), f'effect give {foe(10)} minecraft:poison 8 2', f'effect give {foe(10)} minecraft:wither 5 1',
                              'particle minecraft:witch ~ ~1 ~ 5 1 5 0.2 300', 'particle minecraft:dust{color:[0.4,0.85,0.2],scale:2.5} ~ ~1 ~ 5 1 5 0 200',
                              'playsound minecraft:entity.witch.throw neutral @a[distance=..32] ~ ~ ~ 1.5 0.5'])
    fn('p79/pet/ultb/plague', [beat(t, atk(5, 10)) for t in (30, 40, 50)] + [beat(t, f'effect give {foe(10)} minecraft:poison 6 2') for t in (30, 40, 50)] +
       [beat(t, 'particle minecraft:dust{color:[0.65,0.3,0.9],scale:2.5} ~ ~1 ~ 5 0.8 5 0 160') for t in range(22, 56, 3)])
    # TECTONIC SLAM (earth): three shockwaves roll out of the ground, each throwing them into the air
    fn('p79/pet/ult/tectonic', ['particle minecraft:explosion ~ ~0.3 ~ 1 0.1 1 0 6', 'playsound minecraft:entity.warden.attack_impact neutral @a[distance=..40] ~ ~ ~ 1.6 0.5'])
    for i_, (t, lo, hi) in enumerate(((20, None, 4), (24, 4, 7), (28, 7, 10))):
        fn(f'p79/pet/ultw{i_}', [atk(10, hi, lo), f'effect give {foe(hi, lo)} minecraft:levitation 1 6', f'effect give {foe(hi, lo)} minecraft:slowness 5 3'] +
           ring('minecraft:block{block_state:"minecraft:dirt"}', hi - 1, 20) + ['playsound minecraft:entity.generic.explode neutral @a[distance=..32] ~ ~ ~ 1 0.6'])
    G.FUNCS['p79/pet/ult/tectonic'].append('function bm:p79/pet/ultw0')
    fn('p79/pet/ultb/tectonic', [beat(24, 'function bm:p79/pet/ultw1'), beat(28, 'function bm:p79/pet/ultw2')])
    # AVALANCHE (rock): boulders drop out of the sky onto every foe
    fn('p79/pet/ult/avalanche', [f'execute as {foe(11)} at @s run summon minecraft:block_display ~ ~9 ~ ' +
                                 snbt({'Tags': ['bm.kxboulder', 'bm.kxbn'], 'block_state': 'minecraft:cobblestone', 'teleport_duration': Int(1),
                                       'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(-1), F(0), F(-1)], 'scale': [F(2)] * 3}}),
                                 'scoreboard players set @e[type=minecraft:block_display,tag=bm.kxbn] bm.kxt 10', 'tag @e[type=minecraft:block_display,tag=bm.kxbn] remove bm.kxbn',
                                 'particle minecraft:block{block_state:"minecraft:stone"} ~ ~6 ~ 5 2 5 0 200', 'playsound minecraft:block.stone.break neutral @a[distance=..32] ~ ~ ~ 1.5 0.5'])
    tick.append('execute as @e[type=minecraft:block_display,tag=bm.kxboulder] at @s run function bm:p79/pet/boulder')
    fn('p79/pet/boulder', ['tp @s ~ ~-0.9 ~', 'particle minecraft:falling_dust{block_state:"minecraft:stone"} ~ ~1 ~ 0.6 0.4 0.6 0 4',
                           'scoreboard players remove @s bm.kxt 1', 'execute if score @s bm.kxt matches ..0 run function bm:p79/pet/boulder_hit'])
    fn('p79/pet/boulder_hit', ['particle minecraft:explosion ~ ~0.5 ~ 0.5 0.3 0.5 0 3', 'particle minecraft:block{block_state:"minecraft:cobblestone"} ~ ~0.5 ~ 1.2 0.4 1.2 0 80',
                               'playsound minecraft:entity.generic.explode neutral @a[distance=..32] ~ ~ ~ 1 0.5',
                               'execute as @e[type=#bm:hostile,tag=!bm.npc,distance=..2.6] run damage @s 20 minecraft:falling_block',
                               'effect give @e[type=#bm:hostile,tag=!bm.npc,distance=..2.6] minecraft:weakness 6 1', 'kill @s'])
    # TEMPEST (air): a cyclone hurls them high into the sky - and the fall does the rest
    fn('p79/pet/ult/tempest', [atk(12, 11), f'effect give {foe(11)} minecraft:levitation 2 14', 'particle minecraft:cloud ~ ~1 ~ 5 2 5 0.3 300',
                               'particle minecraft:gust_emitter_large ~ ~1 ~ 0 0 0 0 1', 'playsound minecraft:entity.breeze.wind_burst neutral @a[distance=..40] ~ ~ ~ 1.6 0.5'])
    fn('p79/pet/ultb/tempest', [beat(t, f'particle minecraft:cloud ~ ~{2 + (t - 22) // 2} ~ 2 0.5 2 0.2 40') for t in range(22, 40, 2)] +
       [beat(32, atk(6, 14)), beat(32, 'particle minecraft:gust_emitter_small ~ ~4 ~ 3 2 3 0 6')])
    # OVERGROWTH (grass): thorned vines burst up and hold them fast, while everything on his side is healed
    fn('p79/pet/ult/overgrowth', [atk(14, 10), f'effect give {foe(10)} minecraft:slowness 4 9', f'effect give {foe(10)} minecraft:jump_boost 4 200',
                                  'effect give @a[distance=..10] minecraft:instant_health 1 1', 'effect give @a[distance=..10] minecraft:regeneration 8 1',
                                  'effect give @s minecraft:instant_health 1 2', 'particle minecraft:happy_villager ~ ~1 ~ 5 1 5 0 200',
                                  'particle minecraft:composter ~ ~0.5 ~ 5 0.5 5 0 200', 'playsound minecraft:block.big_dripleaf.tilt_down neutral @a[distance=..32] ~ ~ ~ 1.5 0.5'])
    fn('p79/pet/ultb/overgrowth', [beat(32, atk(8, 10)), beat(32, 'particle minecraft:crit ~ ~0.5 ~ 5 0.5 5 0.2 160'),
                                   beat(32, 'playsound minecraft:block.sweet_berry_bush.break neutral @a[distance=..32] ~ ~ ~ 1.5 0.6')])
    # ABSOLUTE ZERO (ice): everything around him freezes solid - and then shatters
    fn('p79/pet/ult/zero', [atk(15, 11), f'execute as {foe(11)} run data modify entity @s TicksFrozen set value 400', f'effect give {foe(11)} minecraft:slowness 3 9',
                            'particle minecraft:snowflake ~ ~1 ~ 6 1.5 6 0.05 400', 'particle minecraft:block{block_state:"minecraft:ice"} ~ ~1 ~ 5 1 5 0 120',
                            'playsound minecraft:block.glass.break neutral @a[distance=..32] ~ ~ ~ 1.2 0.5'])
    fn('p79/pet/ultb/zero', [beat(40, atk(12, 11)), beat(40, 'particle minecraft:block{block_state:"minecraft:packed_ice"} ~ ~1 ~ 5 1 5 0 300'),
                             beat(40, 'playsound minecraft:block.glass.break neutral @a[distance=..32] ~ ~ ~ 1.6 0.8')])
    # VOID REQUIEM (ethereal): the void pours out of him at everything for fourteen blocks, drags it all in - and detonates
    fn('p79/pet/ult/void', [atk(22, 14), f'effect give {foe(14)} minecraft:wither 6 2', f'effect give {foe(14)} minecraft:glowing 6 0',
                            'particle minecraft:reverse_portal ~ ~1.5 ~ 7 2 7 0.2 500', 'particle minecraft:end_rod ~ ~2 ~ 6 2 6 0.1 200',
                            'particle minecraft:sonic_boom ~ ~1.5 ~ 0 0 0 0 1', 'playsound minecraft:entity.warden.sonic_boom neutral @a[distance=..48] ~ ~ ~ 1.4 0.7'])
    fn('p79/pet/ultb/void', [beat(t, f'execute as {foe(14)} at @s facing entity {pme} feet run tp @s ^ ^ ^1.6') for t in (26, 29, 32)] +
       [beat(t, 'particle minecraft:portal ~ ~1.5 ~ 4 2 4 1.5 200') for t in (26, 29, 32)] +
       [beat(36, atk(16, 6)), beat(36, 'particle minecraft:explosion_emitter ~ ~1 ~ 0 0 0 0 1'), beat(36, 'particle minecraft:flash{color:[0.8,0.6,1.0,1.0]} ~ ~1.5 ~ 0 0 0 0 1'),
        beat(36, 'playsound minecraft:entity.generic.explode neutral @a[distance=..48] ~ ~ ~ 1.5 0.4')])

    # ---- his element: hand him a gem (right-click him with it); the Ethereal Gem - his ETHEREAL FORM; sneak + right-click him empty-handed: take it back
    wjson('bm/advancement/p79/pet_interact.json', {'criteria': {'i': {'trigger': 'minecraft:player_interacted_with_entity', 'conditions': {
        'entity': [{'condition': 'minecraft:entity_properties', 'entity': 'this',
                    'predicate': {'minecraft:entity_type': 'minecraft:wolf', 'minecraft:nbt': '{Tags:["bm.kxpet"]}'}}]}}}, 'rewards': {'function': 'bm:p79/el/interact'}})
    fn('p79/el/interact', ['advancement revoke @s only bm:p79/pet_interact',
                           'execute if predicate bm:p20/sneaking unless items entity @s weapon.mainhand * run return run function bm:p79/el/take',
                           'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"ethereal_gem"}] run return run function bm:p79/el/set {i:%d}' % ETH] +
       [f'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{{bm:"gem_{k}"}}] run return run function bm:p79/el/set {{i:{i + 1}}}' for i, k in enumerate(ART.EL_KEYS)])
    unsit = ['execute as @e[type=minecraft:wolf,tag=bm.kxsel2] store success score #s bm.rng if data entity @s {Sitting:1b}',
             'execute if score #s bm.rng matches 1 run data modify entity @e[type=minecraft:wolf,tag=bm.kxsel2,limit=1] Sitting set value 0b',
             'execute if score #s bm.rng matches 0 run data modify entity @e[type=minecraft:wolf,tag=bm.kxsel2,limit=1] Sitting set value 1b']
    gem_loot = lambda i: f'loot give @s loot bm:items/{"ethereal_gem" if i == ETH else "gem_" + ART.EL_KEYS[i - 1]}'
    fn('p79/el/give_back', [f'execute if score @s bm.kxel matches {i} run {gem_loot(i)}' for i in range(1, ETH + 1) if i != el['electric']])
    look = {'fire': 'molten - and every blow burns', 'water': 'deep blue - and every blow drags them slow', 'poison': 'violet - and every blow poisons',
            'earth': 'earthen - and every blow roots them', 'rock': 'stone-grey - and every blow saps their strength', 'air': 'sky-pale - and every blow throws them up',
            'grass': 'leaf-green - and every blow heals him', 'ice': 'frost-blue - and every blow freezes'}
    fn('p79/el/set', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                      'execute unless score @s bm.kxel matches 0.. run scoreboard players set @s bm.kxel 0',
                      f'{mine} if entity @s[distance=..8] run tag @s add bm.kxsel2',
                      'execute unless entity @e[type=minecraft:wolf,tag=bm.kxsel2] run return run ' + say('KillerWatt only takes gems from the one who called him.', GRN)] + unsit +
       ['$scoreboard players set #el bm.rng $(i)',
        f'execute if score #el bm.rng matches {el["electric"]} run tag @e[tag=bm.kxsel2] remove bm.kxsel2',
        f'execute if score #el bm.rng matches {el["electric"]} run return run ' + say('KillerWatt crackles: he IS electricity. (Keep the gem.)', GRN),
        'execute if score @s bm.kxel = #el bm.rng run tag @e[tag=bm.kxsel2] remove bm.kxsel2',
        'execute if score @s bm.kxel = #el bm.rng run return run ' + say('He has that one in him already.', GRN),
        'function bm:p79/el/give_back', 'scoreboard players operation @s bm.kxel = #el bm.rng',
        'execute unless entity @s[gamemode=creative] run item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
        'execute as @e[type=minecraft:wolf,tag=bm.kxsel2] at @s run function bm:p79/el/apply'] +
       [f'execute if score #el bm.rng matches {i + 1} run ' + title('@s', 'actionbar', [T('KillerWatt drinks the gem - ', GRN), T(k.upper(), GEMS_COL[k], bold=True),
                                                                                         T(f': {look[k]}.', 'gray')]) for i, k in enumerate(ART.EL_KEYS) if k in look] +
       [f'execute if score #el bm.rng matches {ETH} run ' + title('@s', 'actionbar', [T('KillerWatt drinks the Ethereal Gem - ', GRN), T('ETHEREAL FORM', 'white', bold=True),
                                                                                    T(': black steel, half again as strong, and he flies.', 'gray')]),
        'tag @e[tag=bm.kxsel2] remove bm.kxsel2'])
    fn('p79/el/apply', ['scoreboard players operation @s bm.kxel = #el bm.rng', 'function bm:p79/pet/redress',
                        'particle minecraft:flash{color:[1.0,1.0,1.0,1.0]} ~ ~1.5 ~ 0 0 0 0 1', 'particle minecraft:electric_spark ~ ~1.5 ~ 0.6 1 0.6 0.4 60',
                        'playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..16] ~ ~ ~ 1 0.6',
                        'playsound minecraft:entity.lightning_bolt.impact neutral @a[distance=..16] ~ ~ ~ 0.5 1.4',
                        f'execute if score #el bm.rng matches {ETH} run particle minecraft:end_rod ~ ~1.5 ~ 0.4 1 0.4 0.15 60',
                        f'execute if score #el bm.rng matches {ETH} run playsound minecraft:block.beacon.power_select neutral @a[distance=..16] ~ ~ ~ 1 0.8',
                        f'execute unless score #el bm.rng matches {ETH} run effect clear @s minecraft:slow_falling',
                        f'execute unless score #el bm.rng matches {ETH} run data modify entity @s NoGravity set value 0b'])
    fn('p79/el/take', ['execute unless score @s bm.pid matches 1.. run return 0', 'scoreboard players operation #me bm.pid = @s bm.pid',
                       f'{mine} if entity @s[distance=..8] run tag @s add bm.kxsel2', 'execute unless entity @e[type=minecraft:wolf,tag=bm.kxsel2] run return 0'] + unsit +
       ['execute unless score @s bm.kxel matches 1.. run tag @e[tag=bm.kxsel2] remove bm.kxsel2',
        'execute unless score @s bm.kxel matches 1.. run return run ' + say('No gem in him - the lightning is his own.', 'gray'),
        'function bm:p79/el/give_back', 'scoreboard players set @s bm.kxel 0', 'scoreboard players set #el bm.rng 0',
        'execute as @e[type=minecraft:wolf,tag=bm.kxsel2] at @s run function bm:p79/el/apply',
        say('KillerWatt sparks the gem back out into your hand - green and gold again.', GRN), 'tag @e[tag=bm.kxsel2] remove bm.kxsel2'])
    # his element shows: a wisp of it, now and then
    elp = {'fire': 'flame', 'water': 'dripping_water', 'poison': 'witch', 'earth': 'composter', 'rock': 'ash', 'air': 'cloud', 'grass': 'happy_villager', 'ice': 'snowflake'}
    second += [f'execute as @e[type=minecraft:wolf,tag=bm.kxpet,scores={{bm.kxel={el[k]}}}] at @s run particle minecraft:{p} ~ ~1.6 ~ 0.5 0.8 0.5 0.01 3' for k, p in elp.items()]

    # a follower like the others: the limit of three, gone with you when you die, home when you go far or put the Spark away
    cnt = G.FUNCS['p58/count']
    cnt.insert(len(cnt) - 1, 'execute as @e[type=minecraft:wolf,tag=bm.kxpet] on owner if entity @s[tag=bm.fcme] run scoreboard players add #fc bm.rng 1')
    G.FUNCS['p62/died'].insert(-1, 'execute as @e[type=minecraft:wolf,tag=bm.kxpet] if score @s bm.pid = #me bm.pid at @s run function bm:p79/pet/died')
    fn('p79/pet/died', ['scoreboard players add #gone bm.rng 1', 'function bm:p79/pet/vanish'])
    P73.follow_rules(G, ('kw', 'wolf', 'bm.kxpet', 'kw_spark', 'p79/pet/vanish', 'KillerWatt', 'bm.fgk', 'p79/pet/summon'), second)

    # ================================================================== (2.67) ANIMATION: poses that hold, reactions, in the air
    # A reaction pose holds bm.kxho ticks, then the walk / breath cycle picks up again from its first frame (eased - no snap).
    # Reactions wait in bm.kxou: 1 a blow (the flinch), 2 he's just arrived (a roar), 3 a monster in reach (a tendril swipe).
    # The rider's Thunder Leap keeps its pose to the landing - the walk cycle used to step over it in mid-air.
    ao = ['bm.kxho', 'bm.kxou', 'bm.kxfc', 'bm.kxair']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in ao]
    G.OBJECTIVES += ao
    for kind in ('boss', 'pet'):
        tk = G.FUNCS[f'p79/{kind}/tick']
        k_ = next(i for i, l in enumerate(tk) if f'function bm:p79/{kind}/move' in l)
        tk[k_] = tk[k_].replace(' run function bm:', (' unless entity @s[tag=bm.kxleap]' if kind == 'pet' else '') +
                                ' unless score @s bm.kxho matches 1.. run function bm:')
        tk[k_:k_] = ['execute if score @s bm.kxfc matches 1.. run scoreboard players remove @s bm.kxfc 1',
                     'execute if score @s bm.kxho matches 1.. run function bm:p79/hold'] + \
                    (['execute unless score @s bm.kxfc matches 1.. if data entity @s {HurtTime:10s} run scoreboard players set @s bm.kxou 1',
                      'execute if score #rid bm.rng matches 0 unless score @s bm.kxatk matches 1.. unless score @s bm.kxho matches 1.. unless entity @s[tag=bm.kxleap] '
                      'unless entity @s[tag=bm.kxclimb] run function bm:p79/pet/brawl_chk'] if kind == 'pet' else []) + \
                    [f'execute if score @s bm.kxou matches 1.. unless score @s bm.kxatk matches 1.. ' +
                     ('unless entity @s[tag=bm.kxclimb] unless entity @s[tag=bm.kxleap] ' if kind == 'pet' else '') + f'run function bm:p79/{kind}/react']
        G.FUNCS[f'p79/{kind}/go'] += ['scoreboard players set @s bm.kxho 0', 'tag @s remove bm.kxsw']
        fn(f'p79/{kind}/flinch', [f'function bm:p79/{kind}/pose/flinch', 'scoreboard players set @s bm.kxho 8', 'scoreboard players set @s bm.kxfc 40',
                                  'tag @s remove bm.kxsw'])
    fn('p79/hold', ['scoreboard players remove @s bm.kxho 1',
                    'execute if score @s bm.kxho matches 7 if entity @s[tag=bm.kxsw] run function bm:p79/pet/pose/sweep_b',
                    'execute if score @s bm.kxho matches 6 if entity @s[tag=bm.kxsw] rotated as @s rotated ~ 0 run particle minecraft:sweep_attack ^ ^0.8 ^1.3 0 0 0 0 1',
                    'execute if score @s bm.kxho matches 0 run tag @s remove bm.kxsw', 'execute if score @s bm.kxho matches 0 run function bm:p79/unflex',
                    'execute if score @s bm.kxho matches 0 run scoreboard players set @s bm.kxs -1'])
    fn('p79/boss/react', ['execute if score @s bm.kxou matches 1 run function bm:p79/boss/flinch', 'scoreboard players set @s bm.kxou 0'])
    G.FUNCS['p79/boss/ouch'].append('execute unless score @s bm.kxatk matches 1.. unless score @s bm.kxfc matches 1.. run scoreboard players set @s bm.kxou 1')
    fn('p79/pet/react', ['execute if score @s bm.kxou matches 1 run function bm:p79/pet/flinch', 'execute if score @s bm.kxou matches 2 run function bm:p79/pet/greet',
                         'execute if score @s bm.kxou matches 3 run function bm:p79/pet/swipe', 'scoreboard players set @s bm.kxou 0'])
    G.FUNCS['p79/pet/rig'].append('scoreboard players set @s bm.kxou 2')
    fn('p79/pet/greet', ['function bm:p79/pet/pose/roar', 'function bm:p79/flex', 'scoreboard players set @s bm.kxho 18',
                         'particle minecraft:electric_spark ~ ~1.6 ~ 0.5 0.6 0.5 0.2 16', 'playsound minecraft:block.beacon.power_select neutral @a[distance=..16] ~ ~ ~ 0.5 1.8'])
    # (a monster in bite reach, no attack under way: the tendrils swipe at it in time with his bite - for show, the bite does the harm)
    fn('p79/pet/brawl_chk', ['scoreboard players operation #sw bm.rng = @s bm.kxf', 'scoreboard players operation #sw bm.rng %= #20 bm.rng',
                             'execute unless score #sw bm.rng matches 10 run return 0', 'execute if data entity @s {Sitting:1b} run return 0',
                             f'execute if entity @e[{hostile},distance=..2.4] run scoreboard players set @s bm.kxou 3'])
    fn('p79/pet/swipe', ['function bm:p79/pet/pose/sweep_a', 'scoreboard players set @s bm.kxho 14', 'tag @s add bm.kxsw',
                         'playsound minecraft:entity.player.attack.sweep neutral @a[distance=..16] ~ ~ ~ 0.5 1.5'])
    # in the air (a drop, a jump, flying with his rider) for over 6 ticks: arms out, tendrils trailing - the hover
    mv = G.FUNCS['p79/pet/move']
    k_ = next(i for i, l in enumerate(mv) if 'bm:p21/walking' in l) + 1
    mv[k_:k_] = ['execute if predicate bm:p39/on_ground run scoreboard players set @s bm.kxair 0',
                 'execute unless predicate bm:p39/on_ground run scoreboard players add @s bm.kxair 1',
                 'execute if score @s bm.kxair matches 7.. run scoreboard players set #st bm.rng 2']
    mv.append('execute if score #st bm.rng matches 2 if score #f bm.rng matches 0 run function bm:p79/pet/pose/hover')
    # (2.67) in the water: the breaststroke (it beats the hover - off the ground in water is swimming, not flying)
    k_ = next(i for i, l in enumerate(mv) if 'bm.kxair matches 7..' in l) + 1
    mv.insert(k_, 'execute if predicate bm:swim unless predicate bm:p39/on_ground run scoreboard players set #st bm.rng 3')
    mv += ['execute if score #st bm.rng matches 3 run scoreboard players operation #f bm.rng %= #24 bm.rng'] + \
          [f'execute if score #st bm.rng matches 3 if score #f bm.rng matches {6 * i} run function bm:p79/pet/pose/swim_{c}' for i, c in enumerate('abcd')]
    # the boss up close: a quick one-two with the fists (a share of the slams he'd throw at arm's length)
    bme = '@e[type=minecraft:husk,tag=bm.kxme,limit=1]'
    bat = lambda t, cmd: f'execute if score @s bm.kxt matches {t} run {cmd}'
    bm_ = G.FUNCS['p79/boss/mind']
    k_ = next(i for i, l in enumerate(bm_) if 'boss/start {a:1}' in l)
    bm_.insert(k_, 'execute if entity @a[distance=..4,gamemode=!creative,gamemode=!spectator] if score #r bm.rng matches 1..14 run return run function bm:p79/boss/start {a:6}')
    ba = G.FUNCS['p79/boss/attack']
    ba.insert(len(ba) - 1, 'execute if score @s bm.kxatk matches 6 run function bm:p79/boss/a_jab')
    fn('p79/boss/a_jab', [bat(1, 'execute facing entity @a[distance=..6,gamemode=!creative,gamemode=!spectator,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0'),
                          bat(1, 'function bm:p79/boss/pose/punch_r'), bat(1, 'playsound minecraft:entity.iron_golem.attack hostile @a[distance=..24] ~ ~ ~ 1 0.6'),
                          bat(4, 'function bm:p79/boss/jab_hit'),
                          bat(9, 'function bm:p79/boss/pose/punch_l'), bat(9, 'playsound minecraft:entity.iron_golem.attack hostile @a[distance=..24] ~ ~ ~ 1 0.7'),
                          bat(12, 'function bm:p79/boss/jab_hit'), bat('22..', 'function bm:p79/boss/done')])
    fn('p79/boss/jab_hit', ['execute rotated as @s rotated ~ 0 positioned ^ ^2.2 ^2.6 run particle minecraft:electric_spark ~ ~ ~ 0.6 0.6 0.6 0.2 20',
                            f'execute rotated as @s rotated ~ 0 positioned ^ ^ ^2.6 as @a[distance=..2.4,gamemode=!creative,gamemode=!spectator] run damage @s 6 minecraft:mob_attack by {bme}'])

    # ================================================================== (2.67) HIS FACE: the maw moves
    # bm.kxfe the face wanted (0 his grin, then ART.MAW_EXPR in order), bm.kxft how long a reaction holds, bm.kxfl the face shown;
    # the follower snarls with a monster within 10 (the boss with someone to fight within 20), clenches when hurt, roars as he
    # strikes or arrives - and now and then, calm, the follower smirks. The head's item picks the maw from custom_model_data.
    fo = ['bm.kxfe', 'bm.kxft', 'bm.kxfl', 'bm.kxfg']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in fo]
    G.OBJECTIVES += fo
    MAW = {e: i + 1 for i, e in enumerate(ART.MAW_EXPR)}
    face = lambda e, t: [f'scoreboard players set @s bm.kxfe {MAW[e]}', f'scoreboard players set @s bm.kxft {t}']
    for kind in ('boss', 'pet'):
        tk = G.FUNCS[f'p79/{kind}/tick']
        tk.insert(len(tk) - 1, f'function bm:p79/{kind}/face')
        fn(f'p79/{kind}/face', ['execute if score @s bm.kxft matches 1.. run scoreboard players remove @s bm.kxft 1',
                                f'execute unless score @s bm.kxft matches 1.. run function bm:p79/{kind}/face_base',
                                'execute unless score @s bm.kxfe = @s bm.kxfl run function bm:p79/face_set'])
        G.FUNCS[f'p79/{kind}/flinch'] += face('hurt', 12)
        G.FUNCS[f'p79/{kind}/go'] += face('roar', 14)
        G.FUNCS[f'p79/{kind}/rig'].append('scoreboard players set @s bm.kxfl -1')
    fn('p79/pet/face_base', ['scoreboard players set @s bm.kxfe 0',
                             f'execute if score #fxk bm.fxt matches 0 store success score @s bm.kxfg if entity @e[{hostile},distance=..10]',
                             f'execute if score @s bm.kxfg matches 1 run scoreboard players set @s bm.kxfe {MAW["snarl"]}',
                             'execute if score @s bm.kxfg matches 1 run return 0',
                             'execute store result score #r bm.rng run random value 1..400',
                             'execute if score #r bm.rng matches 1 run function bm:p79/pet/smirk'])
    fn('p79/pet/smirk', face('smug', 50))
    fn('p79/boss/face_base', ['scoreboard players set @s bm.kxfe 0',
                              'execute if score #fxk bm.fxt matches 0 store success score @s bm.kxfg if entity @a[distance=..20,gamemode=!creative,gamemode=!spectator]',
                              f'execute if score @s bm.kxfg matches 1 run scoreboard players set @s bm.kxfe {MAW["snarl"]}'])
    G.FUNCS['p79/pet/greet'] += face('roar', 18)
    G.FUNCS['p79/pet/swipe'] += face('snarl', 14)
    fn('p79/face_set', ['scoreboard players operation @s bm.kxfl = @s bm.kxfe',
                        f'execute if score @s bm.kxfe matches 0 run data remove entity {sel("head")[:-1]},limit=1] item.components."minecraft:custom_model_data"'] +
       [f'execute if score @s bm.kxfe matches {i} run data modify entity {sel("head")[:-1]},limit=1] item.components."minecraft:custom_model_data" set value {{strings:["{e}"]}}'
        for e, i in MAW.items()])

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
    # (2.67) his maw: each head (his own, every element's, the ethereal one) gains a model per expression, picked by custom_model_data
    heads = {}
    for name in ['kw_head'] + [f'kw_head_{v}' for v in ART.VARIANTS]:
        tex, els = R.HATS[name]
        v = name[len('kw_head'):]
        key = 'kw_face' + v
        assert key in tex, (name, key)
        heads[name] = []
        for e in ART.MAW_EXPR:
            R.HATS[f'{name}_x{e}'] = (dict(tex, **{key: f'bm:block/kw_face_x{e}{v}'}), els)
            heads[name].append((e, f'{name}_x{e}'))
    def post(R2):
        mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
        for name, cases in heads.items():
            R2.wj(f'assets/bm/items/{name}.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                             'cases': [{'when': e, 'model': mdl(m)} for e, m in cases], 'fallback': mdl(name)}})
    R.POST.append(post)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + ('kw_',)
    R.ICONS['kw_spark'] = R.grid(['................', '.......g........', '......gLg.......', '.....gLYLg......', '....gLYWYLg..g..', '...gLYWWWYLg.L..',
                                  '..gLYWWWWWYLg...', '.gLYWWWWWWWYLg..', '..gLYWWWWWYLg...', '...gLYWWWYLg....', '.L..gLYWYLg.....', '.....gLYLg......',
                                  '......gLg....g..', '.......g...g.L..', '...g............', '................'],
                                 dict(g='#258a46', L='#74d462', Y='#c8ff80', W='#f4ffe8'))

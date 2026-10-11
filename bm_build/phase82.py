"""2.67: THE SCORCHING ARACHNO-LANTERN - a rare Blood Moon boss (rig, textures and poses: phase82_art).

ON A BLOOD MOON, very rarely, a monster's spawn under the open sky becomes the ARACHNO-LANTERN instead: a carved pumpkin the
  size of a house, lit from inside and burning at both cheeks, carried fourteen blocks up on eight long black legs. It walks
  over the trees after you (four legs planted, four swinging) and grows tougher with every player who stands against it.
  STOMP: the front pair rears up high - and comes down: a burning shockwave that throws you.
  TONGUE LASH: its lolling purple tongue shoots out and drags you in.
  EMBER RAIN: it throws its head back, its fires roar up, and burning embers fall where you stand - move.
  At half health it SHRIEKS: ember spiderlings pour out from under it, and from then on THE GLARE - a beam of fire from its
  carved eyes that follows you.
  It flees the dawn (when the Blood Moon ends) and leaves if nobody's within 96 blocks for a minute.
THE REWARD (everyone within 64 when it falls): the SCORCHING HEART - certain the first time, a chance after - and Blood
  Crystals, Medallions, a Trophy and Tokens.
ITS HITBOX FITS IT: the giant under it takes your arrows; the pumpkin and each of its eight legs take your blows.
THE SCORCHING HEART: carried (anywhere in your pack), fire can't touch you. Sneak + use on a block: set it down as THE
  HEARTHFIRE - a burning heart on a lantern-light. No monster spawns within 48 blocks of it; monsters that wander within 12
  are seared, and Blood Moon horrors within 24 burn. Sneak + punch it to take it back. (A base's best friend.)"""
from items import item, T, TOTEM
from useitem import hold, HOLD
from nbt import snbt, B, F, D, Int
import phase67 as P67
import phase82_art as ART

ORANGE = '#ff8a2a'
EMBER = '#ff5a1a'
HP = 1000
P67.BOSSES += [('bm.salboss', 'bm:salb')]

item('scorching_heart', TOTEM, 'Scorching Heart', EMBER,
     ['The Arachno-Lantern\'s heart. It never stops burning.', ('Carried: fire can\'t touch you.', 'blue'),
      ('Sneak + use on a block: the HEARTHFIRE -', 'blue'), ('no monster spawns within 48 blocks;', 'blue'),
      ('those that come close are seared, and', 'blue'), ('Blood Moon horrors burn.', 'blue'), ('Sneak + punch it: take it back.', 'gray')],
     model='bm:scorching_heart', glint=True, stack=1, cat='blood', comps=hold('none'), bold=True)
HOLD['scorching_heart'] = 'bm:p82/heart/use'


def extend_offers(O, offer):
    pass


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    tick, fast, second = [], [], []
    ident = [F(0), F(0), F(0), F(1)]
    qf = lambda q: [F(round(v, 4)) for v in q]
    eff = lambda e: {'id': f'minecraft:{e}', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}
    objs = ['bm.salid', 'bm.salf', 'bm.sals', 'bm.salatk', 'bm.salt', 'bm.salc', 'bm.salr', 'bm.salk', 'bm.sallone', 'bm.saln', 'bm.hbid', 'bm.hbt']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + \
        ['scoreboard players set #5 bm.rng 5', 'bossbar add bm:salb {text:"The Scorching Arachno-Lantern",color:"gold"}', 'bossbar set bm:salb color red', 'bossbar set bm:salb style notched_10']
    G.OBJECTIVES += objs
    sel = lambda p=None: '@e[type=minecraft:item_display,tag=bm.salsel' + (f',tag=bm.salp_{p}]' if p else ']')
    me = '@e[type=minecraft:giant,tag=bm.salme,limit=1]'
    near = 'gamemode=!creative,gamemode=!spectator'
    at = lambda t, cmd: f'execute if score @s bm.salt matches {t} run {cmd}'

    # ================================================================== THE RIG
    def part_nbt(p):
        t, q, s = ART.POSES['stand'][p]
        glow = p in ('flame_r', 'flame_l')
        n = {'Tags': ['bm.salp', f'bm.salp_{p}', 'bm.salnewp'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:{ART.MODEL[p]}'}},
             'item_display': 'fixed', 'teleport_duration': Int(3), 'interpolation_duration': Int(10), 'start_interpolation': Int(0), 'view_range': F(4.0),
             'shadow_radius': F(5.0 if p == 'body' else 0.0), 'shadow_strength': F(0.5),
             'transformation': {'left_rotation': qf(q), 'right_rotation': ident, 'translation': [F(round(v, 4)) for v in t], 'scale': [F(round(s, 4))] * 3}}
        if glow: n['brightness'] = {'sky': Int(15), 'block': Int(15)}
        elif p in ('body', 'tongue', 'stem'): n['brightness'] = {'sky': Int(15), 'block': Int(7)}      # (a dim inner light: the face's red glow reads at night)
        return snbt(n)
    fn('p82/rig', [f'summon minecraft:item_display ~ ~ ~ {part_nbt(p)}' for p in ART.PARTS] +
       ['scoreboard players operation @e[type=minecraft:item_display,tag=bm.salnewp,distance=..1] bm.salid = #sid bm.rng',
        'tag @e[type=minecraft:item_display,tag=bm.salnewp,distance=..1] add bm.salsel', 'tag @e[type=minecraft:item_display,tag=bm.salnewp] remove bm.salnewp',
        'scoreboard players set @s bm.sals -1'])
    for name, xf in ART.POSES.items():
        d = ART.DUR[name]
        fn(f'p82/pose/{name}', [f'execute as {sel(p)} run data merge entity @s {{start_interpolation:0,interpolation_duration:{d},transformation:{{'
                                f'left_rotation:{snbt(qf(q))},translation:{snbt([F(round(v, 4)) for v in t])},scale:{snbt([F(round(s, 4))] * 3)}}}}}'
                                for p, (t, q, s) in xf.items()])

    # ================================================================== THE SPAWN: one Blood Moon spawn in a few thousand, under the open sky
    host = {'Tags': ['bm.salboss', 'bm.salhost', 'bm.salnew', 'bm.seen', 'bm.blood', 'bm.tiered'], 'Silent': B(1), 'PersistenceRequired': B(1), 'NoGravity': B(1),
            'CustomName': T('The Scorching Arachno-Lantern', ORANGE, bold=True), 'Health': F(HP), 'DeathLootTable': 'minecraft:empty',
            'attributes': [{'id': 'minecraft:max_health', 'base': D(HP)}, {'id': 'minecraft:armor', 'base': D(10)}, {'id': 'minecraft:armor_toughness', 'base': D(6)},
                           {'id': 'minecraft:knockback_resistance', 'base': D(1)}, {'id': 'minecraft:attack_damage', 'base': D(14)},
                           {'id': 'minecraft:scale', 'base': D(1.25)}],
            'active_effects': [eff('invisibility'), eff('fire_resistance')],
            'drop_chances': {s: F(0.0) for s in ('mainhand', 'offhand', 'head', 'chest', 'legs', 'feet')}}
    fn('p82/summon', [f'summon minecraft:giant ~ ~ ~ {snbt(host)}', 'execute as @e[type=minecraft:giant,tag=bm.salnew,limit=1] at @s run function bm:p82/init',
                      'particle minecraft:flame ~ ~6 ~ 4 4 4 0.1 300', 'particle minecraft:large_smoke ~ ~2 ~ 5 2 5 0.05 120'])
    fn('p82/init', ['scoreboard players add #saln bm.saln 1', 'scoreboard players operation @s bm.salid = #saln bm.saln', 'scoreboard players operation #sid bm.rng = @s bm.salid',
                    'scoreboard players set @s bm.salatk 0', 'scoreboard players set @s bm.salc 60', 'scoreboard players set @s bm.salr 0',
                    'scoreboard players set @s bm.sallone 0', 'tag @s remove bm.salnew', 'function bm:p82/rig', f'tag {sel()} remove bm.salsel'])
    fn('p82/spawn', ['function bm:p82/summon', 'tp @s ~ -400 ~'])
    roll = ('execute if score #sr bm.rng matches 1 if dimension minecraft:overworld unless entity @e[type=minecraft:giant,tag=bm.salboss] '
            'if predicate bm:sees_sky unless block ~ ~-1 ~ #minecraft:air unless block ~ ~ ~ minecraft:water run return run function bm:p82/spawn')
    for t in ('zombie', 'husk', 'skeleton', 'stray', 'spider', 'creeper', 'witch', 'enderman'):
        G.FUNCS[f'mobs/blood_roll/{t}'][0:0] = ['execute store result score #sr bm.rng run random value 1..2500', roll]

    # ================================================================== THE HEARTBEAT
    tick.append('execute as @e[type=minecraft:giant,tag=bm.salboss] at @s run function bm:p82/tick')
    fn('p82/tick', ['execute unless score #active bm.bm matches 1 unless score #forced bm.bm matches 1 run return run function bm:p82/leave',
                    'scoreboard players operation #sid bm.rng = @s bm.salid',
                    'execute as @e[type=minecraft:item_display,tag=bm.salp,tag=!bm.saldying] if score @s bm.salid = #sid bm.rng run tag @s add bm.salsel',
                    f'execute unless entity {sel("body")} run function bm:p82/rig',
                    f'execute rotated as @s rotated ~ 0 run tp {sel()} ~ ~ ~ ~ 0',
                    f'execute if entity @s[tag=!bm.salintro] if entity @a[distance=..48,{near}] run function bm:p82/intro',
                    'tag @a remove bm.saltgt', f'tag @a[distance=..64,{near},sort=nearest,limit=1] add bm.saltgt',
                    'execute if score @s bm.salatk matches 1.. run function bm:p82/attack',
                    'execute unless score @s bm.salatk matches 1.. run function bm:p82/move',
                    'execute unless score @s bm.salatk matches 1.. run function bm:p82/mind',
                    'function bm:p82/ground', 'function bm:p82/hitboxes', f'tag {sel()} remove bm.salsel',
                    # (2.67) its fire licks out of the corners of its mouth
                    'execute rotated as @s rotated ~ 0 positioned ^3.3 ^8.2 ^3.1 run particle minecraft:flame ~ ~ ~ 0.12 0.12 0.08 0.025 2',
                    'execute rotated as @s rotated ~ 0 positioned ^-3.3 ^8.2 ^3.1 run particle minecraft:flame ~ ~ ~ 0.12 0.12 0.08 0.025 2'])
    fn('p82/intro', ['tag @s add bm.salintro', 'title @a[distance=..64] times 10 60 20',
                     title('@a[distance=..64]', 'title', T('THE SCORCHING ARACHNO-LANTERN', ORANGE, bold=True)),
                     title('@a[distance=..64]', 'subtitle', T('it walks over the trees', 'red', italic=True)),
                     'playsound minecraft:entity.ravager.roar hostile @a[distance=..96] ~ ~8 ~ 3 0.4',
                     'playsound minecraft:entity.blaze.ambient hostile @a[distance=..96] ~ ~8 ~ 3 0.5'])
    second += ['execute as @e[type=minecraft:giant,tag=bm.salboss] at @s run function bm:p82/sec']
    fn('p82/sec', ['bossbar set bm:salb visible true', 'bossbar set bm:salb players @a[distance=..72]',
                   'execute store result bossbar bm:salb value run data get entity @s Health',
                   'execute store result score #h bm.rng run data get entity @s Health', 'execute store result score #mx bm.rng run attribute @s minecraft:max_health get',
                   'scoreboard players operation #mx bm.rng /= #2 bm.rng',
                   'execute if score @s bm.salr matches 0 if score #h bm.rng <= #mx bm.rng run function bm:p82/shriek',
                   'execute rotated as @s rotated ~ 0 positioned ^3.4 ^8.4 ^3.0 run particle minecraft:lava ~ ~ ~ 0.2 0.1 0.2 0 1',
                   'execute rotated as @s rotated ~ 0 positioned ^-3.4 ^8.4 ^3.0 run particle minecraft:lava ~ ~ ~ 0.2 0.1 0.2 0 1',
                   'execute rotated as @s rotated ~ 0 positioned ^ ^7.2 ^3.1 run particle minecraft:small_flame ~ ~ ~ 1.6 0.2 0.1 0.01 6',
                   f'execute as @a[distance=..5,{near}] run data modify entity @s Fire set value 60s',
                   'execute if entity @a[distance=..96] run scoreboard players set @s bm.sallone 0', 'scoreboard players add @s bm.sallone 1',
                   'execute if score @s bm.sallone matches 60.. run function bm:p82/leave'])
    # walking: it turns on the nearest of you and strides (a 2-second gait cycle, 3 blocks a second); close in, it stands
    fn('p82/move', ['scoreboard players set #st bm.rng 0', 'execute if entity @a[tag=bm.saltgt,distance=7..] run scoreboard players set #st bm.rng 1',
                    'execute unless score @s bm.sals = #st bm.rng run scoreboard players set @s bm.salf 0', 'scoreboard players operation @s bm.sals = #st bm.rng',
                    'execute if score #st bm.rng matches 1 facing entity @a[tag=bm.saltgt,limit=1] feet run tp @s ~ ~ ~ ~ 0',
                    'execute if score #st bm.rng matches 1 rotated as @s rotated ~ 0 run tp @s ^ ^ ^0.16',
                    'scoreboard players add @s bm.salf 1', 'scoreboard players operation #f bm.rng = @s bm.salf',
                    'execute if score #st bm.rng matches 1 run scoreboard players operation #f bm.rng %= #40 bm.rng',
                    'execute if score #st bm.rng matches 0 run scoreboard players operation #f bm.rng %= #60 bm.rng'] +
       [f'execute if score #st bm.rng matches 1 if score #f bm.rng matches {10 * k} run function bm:p82/pose/walk{k}' for k in range(4)] +
       ['execute if score #st bm.rng matches 1 if score #f bm.rng matches 0 run playsound minecraft:entity.iron_golem.step hostile @a[distance=..48] ~ ~ ~ 2 0.4',
        'execute if score #st bm.rng matches 1 if score #f bm.rng matches 20 run playsound minecraft:entity.iron_golem.step hostile @a[distance=..48] ~ ~ ~ 2 0.45',
        'execute if score #st bm.rng matches 0 if score #f bm.rng matches 0 run function bm:p82/pose/stand',
        'execute if score #st bm.rng matches 0 if score #f bm.rng matches 30 run function bm:p82/pose/breathe'])
    # (it keeps its feet on the ground, rising or settling no more than a quarter block a tick - over a tree, it steps up)
    fn('p82/ground', ['execute positioned over motion_blocking_no_leaves run summon minecraft:marker ~ ~ ~ {Tags:["bm.salgr"]}',
                      'execute store result score #gy bm.rng run data get entity @e[type=minecraft:marker,tag=bm.salgr,limit=1] Pos[1] 100',
                      'kill @e[type=minecraft:marker,tag=bm.salgr]', 'execute store result score #hy bm.rng run data get entity @s Pos[1] 100',
                      'scoreboard players operation #gy bm.rng -= #hy bm.rng', 'execute if score #gy bm.rng matches 26.. run scoreboard players set #gy bm.rng 25',
                      'execute if score #gy bm.rng matches ..-26 run scoreboard players set #gy bm.rng -25', 'scoreboard players operation #hy bm.rng += #gy bm.rng',
                      'execute store result entity @s Pos[1] double 0.01 run scoreboard players get #hy bm.rng'])
    # (its hitbox fits it: the giant itself, scale 1.25 - 15 blocks high, 4.5 wide - takes arrows; boxes over the pumpkin and
    #  each of the eight lower legs take blows, passed to it by the relay below)
    LEGBOX = [(8.63, 8.34), (11.52, 2.03), (10.59, -4.49), (6.43, -9.53), (-8.63, 8.34), (-11.52, 2.03), (-10.59, -4.49), (-6.43, -9.53)]
    fn('p82/hitboxes', ['execute as @e[type=minecraft:interaction,tag=bm.bhit_sal,distance=..32] if score @s bm.hbid = #sid bm.rng run tag @s add bm.hbsel',
                        'execute unless entity @e[type=minecraft:interaction,tag=bm.hbsel,tag=bm.bhit_sal] run function bm:p82/hitbox_make',
                        'tp @e[type=minecraft:interaction,tag=bm.hbsel,tag=bm.salhb_body] ~ ~4.9 ~'] +
       [f'execute rotated as @s rotated ~ 0 positioned ^{x} ^ ^{z} run tp @e[type=minecraft:interaction,tag=bm.hbsel,tag=bm.salhb_{k}] ~ ~ ~' for k, (x, z) in enumerate(LEGBOX)] +
       ['tag @e[type=minecraft:interaction,tag=bm.hbsel] remove bm.hbsel'])
    fn('p82/hitbox_make', ['summon minecraft:interaction ~ ~4.9 ~ {Tags:["bm.bhit","bm.bhit_sal","bm.salhb_body","bm.hbnew"],width:6.6f,height:6.6f}'] +
       [f'summon minecraft:interaction ~ ~ ~ {{Tags:["bm.bhit","bm.bhit_sal","bm.salhb_{k}","bm.hbnew"],width:2.2f,height:7.0f}}' for k in range(len(LEGBOX))] +
       ['scoreboard players operation @e[type=minecraft:interaction,tag=bm.hbnew] bm.hbid = #sid bm.rng',
        'tag @e[type=minecraft:interaction,tag=bm.hbnew] add bm.hbsel', 'tag @e[type=minecraft:interaction,tag=bm.hbnew] remove bm.hbnew'])
    # THE RELAY (both big bosses): a blow on one of their hitboxes is a blow on them - your weapon's damage (its Sharpness too),
    # once a half-second at most, and the kill is yours
    tick.append('execute as @e[type=minecraft:interaction,tag=bm.bhit] if data entity @s attack at @s run function bm:p82/hb/hit')
    fn('p82/hb/hit', ['scoreboard players operation #hbid bm.rng = @s bm.hbid', 'scoreboard players set #hbk bm.rng 0',
                      'execute if entity @s[tag=bm.bhit_kw] run scoreboard players set #hbk bm.rng 1', 'execute if entity @s[tag=bm.bhit_sal] run scoreboard players set #hbk bm.rng 2',
                      'execute on attacker if entity @s[type=minecraft:player] run function bm:p82/hb/relay', 'data remove entity @s attack'])
    fn('p82/hb/relay', ['execute store result score #gt bm.rng run time query gametime', 'scoreboard players operation #d bm.rng = #gt bm.rng',
                        'scoreboard players operation #d bm.rng -= @s bm.hbt', 'execute if score #d bm.rng matches 0..9 run return 0',
                        'scoreboard players operation @s bm.hbt = #gt bm.rng',
                        'execute store result score #ad bm.rng run attribute @s minecraft:attack_damage get 10',
                        'execute store result score #sh bm.rng run data get entity @s SelectedItem.components."minecraft:enchantments"."minecraft:sharpness"',
                        'execute if score #sh bm.rng matches 1.. run scoreboard players operation #sh bm.rng *= #5 bm.rng',
                        'execute if score #sh bm.rng matches 1.. run scoreboard players add #sh bm.rng 5',
                        'execute if score #sh bm.rng matches 1.. run scoreboard players operation #ad bm.rng += #sh bm.rng',
                        'execute store result storage bm:tmp hb.d double 0.1 run scoreboard players get #ad bm.rng', 'tag @s add bm.hbatk',
                        'execute if score #hbk bm.rng matches 1 as @e[type=minecraft:husk,tag=bm.kxboss] if score @s bm.kxid = #hbid bm.rng at @s run function bm:p82/hb/dmg with storage bm:tmp hb',
                        'execute if score #hbk bm.rng matches 2 as @e[type=minecraft:giant,tag=bm.salboss] if score @s bm.salid = #hbid bm.rng at @s run function bm:p82/hb/dmg with storage bm:tmp hb',
                        'tag @s remove bm.hbatk'])
    fn('p82/hb/dmg', ['$damage @s $(d) minecraft:player_attack by @a[tag=bm.hbatk,limit=1]',
                      'execute at @a[tag=bm.hbatk,limit=1] anchored eyes positioned ^ ^ ^2 run particle minecraft:crit ~ ~ ~ 0.3 0.3 0.3 0.3 10',
                      'execute at @a[tag=bm.hbatk,limit=1] run playsound minecraft:entity.player.attack.strong player @a[distance=..16] ~ ~ ~ 1 1'])
    # (a hitbox whose boss is gone goes too)
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.bhit] at @s run function bm:p82/hb/orphan')
    fn('p82/hb/orphan', ['scoreboard players operation #hbid bm.rng = @s bm.hbid',
                         'execute if entity @s[tag=bm.bhit_kw] as @e[type=minecraft:husk,tag=bm.kxboss,distance=..32] if score @s bm.kxid = #hbid bm.rng run return 0',
                         'execute if entity @s[tag=bm.bhit_sal] as @e[type=minecraft:giant,tag=bm.salboss,distance=..40] if score @s bm.salid = #hbid bm.rng run return 0',
                         'kill @s'])

    # the mind: close - STOMP; a little way off - the TONGUE; anywhere - EMBER RAIN; enraged - THE GLARE too
    fn('p82/mind', ['scoreboard players remove @s bm.salc 1', 'execute if score @s bm.salc matches 1.. run return 0', 'scoreboard players set @s bm.salc 20',
                    'execute unless entity @a[tag=bm.saltgt] run return 0', 'execute store result score #r bm.rng run random value 1..100',
                    'execute if entity @a[tag=bm.saltgt,distance=..10] if score #r bm.rng matches 1..55 run return run function bm:p82/start {a:1}',
                    'execute if entity @a[tag=bm.saltgt,distance=..15] if score #r bm.rng matches 56..80 run return run function bm:p82/start {a:2}',
                    'execute if score @s bm.salr matches 1 if entity @a[tag=bm.saltgt,distance=..30] if score #r bm.rng matches 81..100 run return run function bm:p82/start {a:4}',
                    'execute if entity @a[tag=bm.saltgt,distance=..40] run return run function bm:p82/start {a:3}'])
    fn('p82/start', ['$scoreboard players set @s bm.salatk $(a)', 'scoreboard players set @s bm.salt 0', 'scoreboard players set @s bm.salc 70',
                     'execute if score @s bm.salr matches 1 run scoreboard players set @s bm.salc 45'])
    fn('p82/done', ['scoreboard players set @s bm.salatk 0', 'scoreboard players set @s bm.sals -1', 'scoreboard players set @s bm.salf 0'])
    fn('p82/attack', ['scoreboard players add @s bm.salt 1', 'tag @s add bm.salme'] +
       [f'execute if score @s bm.salatk matches {a} run function bm:p82/a_{n}' for a, n in ((1, 'stomp'), (2, 'lash'), (3, 'embers'), (4, 'glare'))] +
       ['tag @s remove bm.salme'])
    # STOMP
    fn('p82/a_stomp', [at(1, 'execute facing entity @a[tag=bm.saltgt,limit=1] feet run tp @s ~ ~ ~ ~ 0'), at(1, 'function bm:p82/pose/rear'),
                       at(1, 'playsound minecraft:entity.ravager.roar hostile @a[distance=..64] ~ ~8 ~ 2 0.6'),
                       at('2..13', 'particle minecraft:flame ^ ^14 ^6 1.5 1 1.5 0.05 6'), at(14, 'function bm:p82/pose/stomp'), at(16, 'function bm:p82/quake'),
                       at(26, 'function bm:p82/pose/stand'), at('34..', 'function bm:p82/done')])
    fn('p82/quake', ['execute rotated as @s rotated ~ 0 positioned ^ ^ ^6 run particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 1',
                     'execute rotated as @s rotated ~ 0 positioned ^ ^ ^6 run particle minecraft:flame ~ ~0.5 ~ 5 0.4 5 0.2 300',
                     'execute rotated as @s rotated ~ 0 positioned ^ ^ ^6 run particle minecraft:lava ~ ~0.5 ~ 4 0.3 4 0 60',
                     'playsound minecraft:entity.generic.explode hostile @a[distance=..64] ~ ~ ~ 2 0.5',
                     f'execute rotated as @s rotated ~ 0 positioned ^ ^ ^6 as @a[distance=..8,{near}] at @s run function bm:p82/stomped'])
    fn('p82/stomped', [f'damage @s 14 minecraft:mob_attack by {me}', 'data modify entity @s Fire set value 100s', 'effect give @s minecraft:levitation 1 4',
                       'particle minecraft:flame ~ ~1 ~ 0.4 0.6 0.4 0.05 20'])
    # TONGUE LASH
    fn('p82/a_lash', [at(1, 'execute facing entity @a[tag=bm.saltgt,limit=1] feet run tp @s ~ ~ ~ ~ 0'), at(1, 'function bm:p82/pose/lash_a'),
                      at(1, 'playsound minecraft:entity.frog.tongue hostile @a[distance=..48] ~ ~8 ~ 2 0.4'),
                      at(9, 'function bm:p82/pose/lash_b'), at(11, 'function bm:p82/lashed'), at(20, 'function bm:p82/pose/stand'), at('26..', 'function bm:p82/done')])
    fn('p82/lashed', ['execute rotated as @s rotated ~ 0 positioned ^ ^4 ^8 run particle minecraft:dust{color:[0.55,0.15,0.8],scale:2.5} ~ ~ ~ 1.5 1.5 3 0 60',
                      f'execute as @a[tag=bm.saltgt,distance=..16,{near}] at @s run function bm:p82/grabbed'])
    fn('p82/grabbed', [f'damage @s 8 minecraft:mob_attack by {me}', 'effect give @s minecraft:slowness 3 2', f'execute facing entity {me} feet run tp @s ^ ^0.5 ^6',
                       'playsound minecraft:entity.slime.squish hostile @a[distance=..24] ~ ~ ~ 1.5 0.5'])
    # EMBER RAIN
    fn('p82/a_embers', [at(1, 'function bm:p82/pose/flare'), at(1, 'playsound minecraft:entity.blaze.shoot hostile @a[distance=..64] ~ ~8 ~ 2 0.5'),
                        at('2..18', 'particle minecraft:flame ~ ~11 ~ 2.5 1.5 2.5 0.15 20'), at('2..18', 'particle minecraft:lava ~ ~11 ~ 2 1 2 0 3'),
                        at(10, f'execute as @a[distance=..40,{near},sort=random,limit=4] at @s run function bm:p82/mark'),
                        at(10, f'execute if score @s bm.salr matches 1 as @a[distance=..40,{near},sort=random,limit=4] at @s positioned ~3 ~ ~2 run function bm:p82/mark'),
                        at(22, 'function bm:p82/pose/stand'), at('30..', 'function bm:p82/done')])
    fn('p82/mark', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.salem","bm.salemn"]}', 'scoreboard players set @e[type=minecraft:marker,tag=bm.salemn] bm.salt 24',
                    'tag @e[type=minecraft:marker,tag=bm.salemn] remove bm.salemn'])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.salem] at @s run function bm:p82/ember')
    fn('p82/ember', ['scoreboard players remove @s bm.salt 1', 'particle minecraft:flame ~ ~0.1 ~ 0.8 0 0.8 0.01 4',
                     'particle minecraft:dust{color:[1.0,0.35,0.05],scale:1.4} ~ ~0.1 ~ 1 0 1 0 3',
                     'execute if score @s bm.salt matches 1..10 run particle minecraft:lava ~ ~8 ~ 0.3 1.5 0.3 0 3',
                     'execute if score @s bm.salt matches 12 run playsound minecraft:entity.blaze.shoot hostile @a[distance=..24] ~ ~ ~ 1 1.4',
                     'execute if score @s bm.salt matches ..0 run function bm:p82/ember_hit'])
    fn('p82/ember_hit', ['particle minecraft:explosion ~ ~0.5 ~ 0.4 0.2 0.4 0 2', 'particle minecraft:flame ~ ~0.5 ~ 1.2 0.4 1.2 0.15 60',
                         'playsound minecraft:entity.generic.explode hostile @a[distance=..32] ~ ~ ~ 1 1.2',
                         f'execute as @a[distance=..2.6,{near}] run damage @s 10 minecraft:in_fire',
                         f'execute as @a[distance=..2.6,{near}] run data modify entity @s Fire set value 100s', 'kill @s'])
    # THE GLARE (enraged): a beam of fire from its carved eyes that follows you
    fn('p82/a_glare', [at(1, 'function bm:p82/pose/flare'), at(1, 'playsound minecraft:block.beacon.activate hostile @a[distance=..64] ~ ~8 ~ 2 0.5'),
                       at('2..11', 'execute rotated as @s rotated ~ 0 positioned ^ ^9.2 ^3.6 run particle minecraft:flame ~ ~ ~ 0.6 0.4 0.2 0.02 8'),
                       at('12..32', 'execute facing entity @a[tag=bm.saltgt,limit=1] feet run tp @s ~ ~ ~ ~ 0'),
                       at('12..32', 'function bm:p82/beam'), at(34, 'function bm:p82/pose/stand'), at('40..', 'function bm:p82/done')])
    fn('p82/beam', ['scoreboard players set #st bm.rng 0',
                    'execute rotated as @s rotated ~ 0 positioned ^ ^9.2 ^3.6 facing entity @a[tag=bm.saltgt,limit=1] eyes run function bm:p82/beam_ray',
                    'execute if score @s bm.salt matches 12 run playsound minecraft:entity.blaze.shoot hostile @a[distance=..64] ~ ~ ~ 2 0.4'])
    fn('p82/beam_ray', ['particle minecraft:flame ~ ~ ~ 0.08 0.08 0.08 0.01 2', 'particle minecraft:dust{color:[1.0,0.7,0.2],scale:1.6} ~ ~ ~ 0 0 0 0 1',
                        f'execute as @a[distance=..1.3,{near}] run function bm:p82/beam_hit', 'scoreboard players add #st bm.rng 1',
                        'execute if score #st bm.rng matches 40.. run return 0', 'execute unless block ~ ~ ~ #minecraft:replaceable run return 0',
                        'execute positioned ^ ^ ^0.8 run function bm:p82/beam_ray'])
    fn('p82/beam_hit', [f'damage @s 6 minecraft:in_fire by {me}', 'data modify entity @s Fire set value 80s'])
    # at half health: the shriek, and ember spiderlings
    fn('p82/shriek', ['scoreboard players set @s bm.salr 1', 'playsound minecraft:entity.ghast.scream hostile @a[distance=..96] ~ ~8 ~ 3 0.5',
                      'playsound minecraft:entity.spider.ambient hostile @a[distance=..64] ~ ~ ~ 3 0.4',
                      title('@a[distance=..64]', 'actionbar', T('The Arachno-Lantern SHRIEKS - its brood spills out!', ORANGE, bold=True)),
                      'particle minecraft:flame ~ ~8 ~ 4 3 4 0.2 300'] +
       [f'execute positioned ^{x} ^ ^{z} positioned over motion_blocking_no_leaves run function bm:p82/brood' for x, z in ((6, 6), (-6, 6), (6, -6), (-6, -6), (0, 9))])
    fn('p82/brood', ['summon minecraft:cave_spider ~ ~ ~ ' + snbt({'Tags': ['bm.seen', 'bm.salling', 'bm.blood'], 'CustomName': T('Ember Spiderling', EMBER),
                                                                   'Health': F(24), 'DeathLootTable': 'minecraft:empty',
                                                                   'attributes': [{'id': 'minecraft:max_health', 'base': D(24)}, {'id': 'minecraft:attack_damage', 'base': D(5)},
                                                                                  {'id': 'minecraft:movement_speed', 'base': D(0.36)}, {'id': 'minecraft:scale', 'base': D(1.3)}],
                                                                   'active_effects': [eff('fire_resistance')]}),
                     'particle minecraft:flame ~ ~0.5 ~ 0.6 0.4 0.6 0.05 20'])
    second.append('execute as @e[type=minecraft:cave_spider,tag=bm.salling] at @s run particle minecraft:flame ~ ~0.4 ~ 0.3 0.2 0.3 0.01 2')
    # dawn, or nobody near: it sinks into smoke
    fn('p82/leave', ['scoreboard players operation #sid bm.rng = @s bm.salid',
                     'execute as @e[type=minecraft:item_display,tag=bm.salp] if score @s bm.salid = #sid bm.rng run kill @s',
                     'particle minecraft:large_smoke ~ ~6 ~ 5 4 5 0.05 300', 'particle minecraft:flame ~ ~8 ~ 3 3 3 0.05 120',
                     title('@a[distance=..64]', 'actionbar', T('The Arachno-Lantern gutters out and fades with the night...', 'gold', italic=True)),
                     'bossbar set bm:salb visible false', 'tp @s ~ -400 ~', 'kill @s'])
    # its fall: the legs buckle, the pumpkin crashes down, and the fires gutter out
    fast.append('execute as @e[type=minecraft:item_display,tag=bm.salp_body,tag=!bm.saldying] at @s if entity @a[distance=..96] run function bm:p82/orphan')
    fn('p82/orphan', ['scoreboard players operation #sid bm.rng = @s bm.salid', 'scoreboard players set #has bm.rng 0',
                      'execute as @e[type=minecraft:giant,tag=bm.salhost,distance=..24] if score @s bm.salid = #sid bm.rng run scoreboard players set #has bm.rng 1',
                      'execute if score #has bm.rng matches 1 run return 0',
                      'execute as @e[type=minecraft:item_display,tag=bm.salp,distance=..24] if score @s bm.salid = #sid bm.rng run tag @s add bm.salsel',
                      'function bm:p82/pose/fall', f'scoreboard players set {sel()} bm.salt 90', f'tag {sel()} add bm.saldying', f'tag {sel()} remove bm.salsel',
                      'playsound minecraft:entity.generic.explode hostile @a[distance=..64] ~ ~ ~ 2 0.4', 'bossbar set bm:salb visible false'])
    tick.append('execute as @e[type=minecraft:item_display,tag=bm.saldying] at @s run function bm:p82/fade')
    fn('p82/fade', ['scoreboard players remove @s bm.salt 1',
                    'execute if score @s bm.salt matches 60 if entity @s[tag=bm.salp_body] run particle minecraft:large_smoke ~ ~2 ~ 3 2 3 0.05 200',
                    'execute if score @s bm.salt matches 20 run data merge entity @s {start_interpolation:0,interpolation_duration:20,transformation:{scale:[0f,0f,0f]}}',
                    'execute if score @s bm.salt matches 20 if entity @s[tag=bm.salp_body] run particle minecraft:flame ~ ~3 ~ 3 2 3 0.05 200',
                    'execute if score @s bm.salt matches ..0 run kill @s'])

    # ================================================================== THE REWARD
    wjson('bm/advancement/p82/killed.json', {'criteria': {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["bm.salboss"]}'}}]}}}, 'rewards': {'function': 'bm:p82/killed'}})
    fn('p82/killed', ['advancement revoke @s only bm:p82/killed', 'execute as @a[distance=..64] at @s run function bm:p82/reward',
                      'execute as @a[distance=..64] run ' + title('@s', 'title', T('THE LANTERN GOES OUT', ORANGE, bold=True)),
                      'execute as @a[distance=..64] run ' + title('@s', 'subtitle', T('its heart still burns', 'gray', italic=True))])
    fn('p82/reward', ['scoreboard players add @s bm.salk 1', 'execute if score @s bm.salk matches 1 run function bm:p82/first',
                      'execute store result score #r bm.rng run random value 1..100',
                      'execute if score @s bm.salk matches 2.. if score #r bm.rng matches 1..35 run ' + give('scorching_heart'),
                      'loot give @s loot bm:p82/hoard', 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 0.9'])
    fn('p82/first', [give('scorching_heart'), tellraw('@s', PREFIX + [T('The Scorching Heart', EMBER, bold=True),
                                                                     T(' is yours - carried, fire can\'t touch you; set down, it keeps the monsters away.', 'gray')])])
    wjson('bm/loot_table/p82/hoard.json', {'pools': [{'rolls': 1, 'entries': [G.loot_entry('blood_crystal', G.uni(6, 12))]},
                                                     {'rolls': 1, 'entries': [G.loot_entry('medallion', G.uni(3, 6))]},
                                                     {'rolls': 1, 'entries': [G.loot_entry('trophy', G.uni(1, 2))]},
                                                     {'rolls': 1, 'entries': [G.loot_entry('token', G.uni(4, 9))]}]})

    # ================================================================== THE SCORCHING HEART: fire can't touch you; set down, the Hearthfire
    holds = '*[minecraft:custom_data~{bm:"scorching_heart"}]'
    second += [f'execute as @a if items entity @s container.* {holds} run effect give @s minecraft:fire_resistance 3 0 true',
               f'execute as @a if items entity @s weapon.offhand {holds} run effect give @s minecraft:fire_resistance 3 0 true']
    fn('p82/heart/use', ['execute unless predicate bm:p20/sneaking run return run ' + say('Sneak + use on a block: set down the Hearthfire. (Carried, fire can\'t touch you.)', EMBER),
                         'scoreboard players set #placed bm.rng 0', 'scoreboard players set #ray bm.rng 25', 'tag @s add bm.placer',
                         'execute anchored eyes positioned ^ ^ ^ run function bm:p82/heart/ray', 'tag @s remove bm.placer',
                         'execute if score #placed bm.rng matches 0 run return run ' + say('Look at the top of a block within 5 blocks.'),
                         'execute unless entity @s[gamemode=creative] run item replace entity @s weapon.mainhand with minecraft:air'])
    fn('p82/heart/ray', ['execute unless block ~ ~ ~ #minecraft:replaceable run return run function bm:p82/heart/hit',
                         'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p82/heart/ray'])
    fn('p82/heart/hit', ['execute align xyz positioned ~0.5 ~1 ~0.5 unless block ~ ~ ~ #minecraft:replaceable run return 0',
                         'execute align xyz positioned ~0.5 ~1 ~0.5 if entity @e[type=minecraft:interaction,tag=bm.hearth,distance=..0.6] run return 0',
                         'execute align xyz positioned ~0.5 ~1 ~0.5 run function bm:p82/heart/place', 'scoreboard players set #placed bm.rng 1'])
    fn('p82/heart/place', ['summon minecraft:item_display ~ ~ ~ ' + snbt({'Tags': ['bm.hearthd', 'bm.hnew'], 'item': {'id': 'minecraft:paper', 'count': Int(1),
                                                                                                                     'components': {'minecraft:item_model': 'bm:scorching_heart'}},
                                                                     'item_display': 'fixed', 'billboard': 'vertical', 'brightness': {'sky': Int(15), 'block': Int(15)},
                                                                     'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.5), F(0)],
                                                                                        'scale': [F(0.8)] * 3}}),
                           'summon minecraft:interaction ~ ~ ~ ' + snbt({'Tags': ['bm.hearth', 'bm.gvdeco', 'bm.hnew'], 'width': F(0.7), 'height': F(0.9), 'response': B(1)}),
                           'tag @e[tag=bm.hnew,distance=..0.5] remove bm.hnew', 'execute if block ~ ~ ~ minecraft:air run setblock ~ ~ ~ minecraft:light[level=15]',
                           'particle minecraft:flame ~ ~0.5 ~ 0.3 0.3 0.3 0.05 30', 'playsound minecraft:item.firecharge.use block @a[distance=..16] ~ ~ ~ 1 0.8',
                           title('@a[tag=bm.placer]', 'actionbar', T('The Hearthfire burns: no monster spawns within 48 blocks.', EMBER))])
    # (each second: new monsters within 48 that would despawn anyway are snuffed out; those near are seared; Blood Moon horrors burn)
    second.append('execute as @e[type=minecraft:interaction,tag=bm.hearth] at @s run function bm:p82/hearth/sec')
    keep = 'tag=!bm.boss,tag=!bm.npc,tag=!bm.monstrosity,tag=!bm.salboss,tag=!bm.kxboss,tag=!bm.gvg,tag=!bm.gvboss,tag=!bm.tiered'
    fn('p82/hearth/sec', [f'execute as @e[type=#bm:hostile,tag=!bm.hfseen,distance=..48] at @s run function bm:p82/hearth/check',
                          'execute as @e[type=#bm:hostile,tag=bm.hfseen,distance=..12] run data modify entity @s Fire set value 60s',
                          'execute as @e[type=#bm:hostile,tag=bm.blood,distance=..24] run function bm:p82/hearth/burn',
                          'particle minecraft:flame ~ ~0.7 ~ 0.15 0.2 0.15 0.01 3', 'particle minecraft:small_flame ~ ~1.1 ~ 0.1 0.1 0.1 0.01 2'])
    fn('p82/hearth/check', ['tag @s add bm.hfseen', f'execute if entity @s[{keep}] if data entity @s {{PersistenceRequired:0b}} unless data entity @s CustomName run function bm:p82/hearth/snuff'])
    fn('p82/hearth/snuff', ['particle minecraft:smoke ~ ~0.6 ~ 0.2 0.4 0.2 0.01 6', 'tp @s ~ -400 ~', 'kill @s'])
    fn('p82/hearth/burn', ['data modify entity @s Fire set value 60s', 'damage @s 3 minecraft:in_fire'])
    G.FUNCS['p71/deco/pick'][0:0] = ['execute if entity @e[type=minecraft:interaction,tag=bm.gvdme,tag=bm.hearth] at @e[type=minecraft:interaction,tag=bm.gvdme,limit=1] '
                                     'run function bm:p82/hearth/take']
    fn('p82/hearth/take', [give('scorching_heart'), 'kill @e[type=minecraft:item_display,tag=bm.hearthd,distance=..0.6]',
                           'execute if block ~ ~ ~ minecraft:light run setblock ~ ~ ~ minecraft:air', 'playsound minecraft:block.fire.extinguish block @a[distance=..16] ~ ~ ~ 0.8 1.2'])

    # ================================================================== admin
    fn('admin/arachno_lantern', ['execute rotated ~ 0 positioned ^ ^ ^14 positioned over motion_blocking_no_leaves run function bm:p82/summon'])
    fn('admin/scorching_heart', [give('scorching_heart')])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.salp]', 'kill @e[type=minecraft:marker,tag=bm.salem]',
                                       'execute as @e[type=minecraft:giant,tag=bm.salboss] run tp @s ~ -400 ~', 'kill @e[type=minecraft:item_display,tag=bm.hearthd]',
                                       'kill @e[type=minecraft:interaction,tag=bm.hearth]']

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    f[-1:-1] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


def rp(R):
    R.TEXTURE_MODS.append(ART)
    for name, (tex, els) in ART.models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + ('sal_',)
    R.ICONS['scorching_heart'] = R.grid(['................', '..rr.......rr...', '.rOOr.....rOOr..', 'rOYYOr...rOYYOr.', 'rOYWYOr.rOYWYOr.', 'rOYYYOOrOOYYYOr.',
                                         'rOOYYYOOOYYYOOr.', '.rOOYYYYYYYOOr..', '..rOOYYYYYOOr...', '...rOOYYYOOr....', '....rOOYOOr.....', '.....rOOOr......',
                                         '......rOr.......', '.......r........', '................', '................'],
                                        dict(r='#7a1a08', O='#ff5a1a', Y='#ffc838', W='#fff4b8'))

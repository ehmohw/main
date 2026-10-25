"""2.94u: SIGNATURE MOVES - choreographed like Bender's Rage (atk.sig: a timeline of poses, dashes and blows; the follower's own
animation held while it plays). Every pose is one the follower already has (their own art - nothing new to clip); the move is
in the timing, the travel, and the finish.

EMMA (Ethereal Form)
  CRESCENT DIVE   (a foe 3-14 off) her wings flare and the axe goes back - she swoops down on it in an arc, cleaves it (8, 13
                  with a gem; 4 to anything beside it) with a crescent of light, and glides back to your side.
  PETAL WALTZ     (two or more foes within 10; every 15 s) she twirls from foe to foe - up to four, a spinning slash each (7,
                  10 with a gem), petals trailing - then rises and brings the axe down: a shockwave ring (10 to all within 4).
LEO
  SHIELD CHARGE   (a foe 3.5-10 off; every 8 s) shield up, he charges in and bashes it (5, slowed) - then the trident goes up
                  over his head and comes down (11; 3 to those beside it).
CELI
  LUNGE AND VAULT (a foe 3.5-10 off; every 7 s) the spear drawn back, she lunges across the gap and runs it through (12, frozen
                  a moment) - then vaults off it, up and back over, and lands ready.
DEMOCRATUS
  REAPING WHIRL   (two or more foes within 7; every 12 s) the scythe drawn back, he spins - three turns - dragging everything near
                  in toward the blade (5 a turn), and ends with a great sweep (12).
APOPHISS
  COIL AND STRIKE (a foe 4-12 off; every 10 s) he coils, hissing - then strikes across the gap (16) and lashes round with his
                  claws on the way out (8 to all within 4.5).
ASHUR
  FIRE WHEEL      (a foe 3-12 off; every 10 s) she crouches, then cartwheels through them in a wheel of fire - burning what
                  she passes (6, set alight) - and erupts where she lands (9 to all within 3).
CECIL
  STAFF TWIRL     (a foe within 14; every 9 s) the staff raised and spun - a ring of arcane light gathering - then a blast down
                  the line at his foe (14, and 6 to those round it)."""
import atk
from items import T

FOE = 'type=#bm:hostile,tag=!bm.npc,tag=!bm.wil_body'


def ring(fn, name, particle, r, n=16, y=0.2):
    """a ring of particles round where it's run"""
    fn(name, [f'execute rotated {360 * i / n:.1f} 0 positioned ^ ^{y} ^{r} run particle {particle}' for i in range(n)])


def generate(G):
    import phase125 as P125
    fn = G.fn
    col = lambda w: P125.WHO[w][2]

    # ================================================================== EMMA
    by = 'by @e[type=minecraft:cat,tag=bm.emme,limit=1]'
    gem = 'entity @e[type=minecraft:cat,tag=bm.emme,tag=bm.emgem]'
    fn('p57/sg/cleave', ['tag @s add bm.emme', f'execute as @e[{FOE},distance=..3.5,sort=nearest,limit=1] at @s run function bm:p57/strike_at', 'tag @s remove bm.emme',
                         'playsound minecraft:entity.player.attack.sweep neutral @a[distance=..20] ~ ~ ~ 1 1.3',
                         'playsound minecraft:block.amethyst_block.chime neutral @a[distance=..20] ~ ~ ~ 1 0.7'])
    atk.sig(G, 'p57', kid=1, tick_fn='p57/tick', state_fn='p57/state', anim_fn='p57/anim', s_obj='bm.ems', place_fn='p57/place_fly', col=col('emma'),
            trigger=f'execute if score @s bm.eme matches 1.. if entity @e[{FOE},distance=3..14]', cd=14, end=19, timeline={
                1: ['function bm:p57/pose/strike_up', 'particle minecraft:end_rod ~ ~1.6 ~ 0.4 0.3 0.4 0.02 8', 'playsound minecraft:entity.phantom.flap neutral @a[distance=..20] ~ ~ ~ 0.8 1.4'],
                4: [f'DASH 2 @e[{FOE},distance=..14,sort=nearest,limit=1]'],
                5: ['function bm:p57/pose/strike_dn', 'function bm:p57/sg/cleave'],
                11: ['function bm:p57/pose/hover_0'],
                14: ['execute on owner run tag @s add bm.ktn', 'DASH 3 @e[tag=bm.ktn,limit=1]'],
                15: ['function bm:p57/pose/hover_0']})
    fn('p57/sg/two', [f'execute store result score #n bm.rng if entity @e[{FOE},distance=..10]', 'return run execute if score #n bm.rng matches 2..'])
    fn('p57/sg/slash', ['tag @s add bm.emme', f'execute as @e[{FOE},distance=..3.5,sort=nearest,limit=1] at @s run function bm:p57/sg/slashed', 'tag @s remove bm.emme',
                        'particle minecraft:cherry_leaves ~ ~1 ~ 0.8 0.4 0.8 0 16', 'playsound minecraft:entity.player.attack.sweep neutral @a[distance=..20] ~ ~ ~ 0.9 1.5'])
    fn('p57/sg/slashed', ['tag @s add bm.emwz', f'execute unless {gem} run damage @s 7 minecraft:magic {by}', f'execute if {gem} run damage @s 10 minecraft:magic {by}',
                          'particle minecraft:sweep_attack ~ ~1 ~ 0.3 0.2 0.3 0 2'])
    ring(fn, 'p57/sg/wave', 'minecraft:dust{color:[1.0,0.7,0.9],scale:1.6} ~ ~ ~ 0 0 0 0 1', 4.0, 24)
    fn('p57/sg/slam', ['data merge entity @s {NoGravity:0b}', 'tag @s add bm.emme', f'execute as @e[{FOE},distance=..4] run damage @s 10 minecraft:magic {by}', 'tag @s remove bm.emme',
                       'function bm:p57/sg/wave', 'particle minecraft:cherry_leaves ~ ~0.5 ~ 2 0.3 2 0 40', 'particle minecraft:end_rod ~ ~0.5 ~ 1.5 0.2 1.5 0.05 20',
                       'playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..24] ~ ~ ~ 1 0.6', 'playsound minecraft:entity.generic.explode neutral @a[distance=..24] ~ ~ ~ 0.4 1.6'])
    nxt = f'@e[{FOE},distance=..10,tag=!bm.emwz,sort=nearest,limit=1]'
    tl = {1: ['function bm:p57/pose/cast', 'tag @e[tag=bm.emwz] remove bm.emwz', 'particle minecraft:cherry_leaves ~ ~1 ~ 0.6 0.6 0.6 0 20',
              'playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..20] ~ ~ ~ 1 1.2', 'execute on owner if entity @s[tag=!bm.hush] run ' +
              G.title('@s', 'actionbar', [T('Emma: ', '#ff8ad8', bold=True), T('Petal Waltz!', '#ffd0ec')])]}
    for j, a in enumerate((4, 5, 6, 7)):
        t0 = 4 + 5 * j
        tl[t0] = [f'DASH {a} {nxt}']
        tl[t0 + 1] = ['function bm:p57/pose/strike_dn', 'function bm:p57/sg/slash']
        tl[t0 + 3] = ['function bm:p57/pose/strike_up']
    tl[25] = ['data merge entity @s {NoGravity:1b}', 'function bm:p57/pose/strike_up', 'particle minecraft:end_rod ~ ~1 ~ 0.3 0.6 0.3 0.04 12']
    for t in range(25, 29): tl.setdefault(t, []).append('execute if block ~ ~2.6 ~ #bm:grap_pass run tp @s ~ ~0.35 ~')
    tl[31] = ['function bm:p57/pose/strike_dn', 'function bm:p57/sg/slam']
    tl[38] = ['function bm:p57/pose/wave_a']
    tl[44] = ['function bm:p57/pose/hover_0']
    atk.sig(G, 'p57', kid=2, tick_fn='p57/tick', state_fn='p57/state', anim_fn='p57/anim', s_obj='bm.ems', place_fn='p57/place_fly', col=col('emma'),
            trigger='execute if score @s bm.eme matches 1.. if function bm:p57/sg/two', cd=300, end=46, timeline=tl)
    # (her old once-a-second strike: only a foe already close)
    E = G.FUNCS['p57/ethereal']
    E[:] = [l.replace(f'if entity @e[{FOE},distance=..14] run function bm:p57/strike', f'unless score @s bm.ksg matches 1.. if entity @e[{FOE},distance=..3] run function bm:p57/strike')
            for l in E]
    G.FUNCS['p57/descend'] += ['scoreboard players set @s bm.ksg 0', 'scoreboard players set @s bm.ksw 0', 'scoreboard players set @s bm.kd 0', 'data merge entity @s {NoGravity:0b}']

    # ================================================================== LEO
    lby = 'by @e[type=minecraft:wolf,tag=bm.leme,limit=1]'
    fn('p96/sg/bash', ['tag @s add bm.leme', f'execute as @e[{FOE},distance=..2.6,sort=nearest,limit=1] at @s run function bm:p96/sg/bashed', 'tag @s remove bm.leme',
                       'playsound minecraft:item.shield.block neutral @a[distance=..16] ~ ~ ~ 1 0.8', 'playsound minecraft:entity.iron_golem.attack neutral @a[distance=..16] ~ ~ ~ 0.6 1.3'])
    fn('p96/sg/bashed', [f'damage @s 5 minecraft:mob_attack {lby}', 'effect give @s minecraft:slowness 2 2', 'particle minecraft:cloud ~ ~1 ~ 0.2 0.3 0.2 0.05 6'])
    fn('p96/sg/smite', ['tag @s add bm.leme', f'execute as @e[{FOE},distance=..3.6,sort=nearest,limit=1] at @s run function bm:p96/sg/smitten', 'tag @s remove bm.leme',
                        'playsound minecraft:item.trident.hit neutral @a[distance=..16] ~ ~ ~ 1 0.7', 'playsound minecraft:entity.player.attack.crit neutral @a[distance=..16] ~ ~ ~ 1 0.8'])
    fn('p96/sg/smitten', [f'damage @s 11 minecraft:mob_attack {lby}', f'execute as @e[{FOE},distance=0.1..2.2] run damage @s 3 minecraft:mob_attack {lby}',
                          'particle minecraft:splash ~ ~1 ~ 0.4 0.4 0.4 0.2 20', 'particle minecraft:sweep_attack ~ ~1 ~ 0.3 0.1 0.3 0 1'])
    atk.sig(G, 'p96', kid=1, tick_fn='p96/tick', state_fn='p96/state', anim_fn='p96/anim', s_obj='bm.les', place_fn='p96/place', col=col('leo'),
            trigger=f'execute unless data entity @s {{Sitting:1b}} unless score @s bm.lek matches 1.. if entity @e[{FOE},distance=3.5..10]', cd=160, end=26,
            dash_kw=dict(reach=1.9, speed=1.0, lift=1), timeline={
                1: ['function bm:p96/pose/guard', 'playsound minecraft:item.armor.equip_iron neutral @a[distance=..16] ~ ~ ~ 1 0.9'],
                5: [f'DASH 1 @e[{FOE},distance=..10,sort=nearest,limit=1]'],
                6: ['function bm:p96/sg/bash'],
                10: ['function bm:p96/pose/throw_back'],
                17: ['function bm:p96/pose/thrust', 'function bm:p96/sg/smite'],
                23: ['function bm:p96/pose/idle_a']})

    # ================================================================== CELI: lunge and vault
    cby = 'by @e[type=minecraft:wolf,tag=bm.ceme,limit=1]'
    fn('p66/sg/pierce', ['tag @s add bm.ceme', f'execute as @e[{FOE},distance=..2.8,sort=nearest,limit=1] at @s run function bm:p66/sg/pierced', 'tag @s remove bm.ceme',
                         'playsound minecraft:item.trident.hit neutral @a[distance=..16] ~ ~ ~ 1 1.2', 'playsound minecraft:block.glass.break neutral @a[distance=..16] ~ ~ ~ 0.4 1.6'])
    fn('p66/sg/pierced', [f'damage @s 12 minecraft:mob_attack {cby}', 'effect give @s minecraft:slowness 2 4', 'particle minecraft:snowflake ~ ~1 ~ 0.3 0.5 0.3 0.05 20',
                          'particle minecraft:item_snowball ~ ~1 ~ 0.3 0.4 0.3 0.1 10'])
    back = f'facing entity @e[{FOE},distance=..12,sort=nearest,limit=1] feet rotated ~ 0'
    vault = {t: [f'execute {back} positioned ^ ^0.32 ^-0.42 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~ ~'] for t in range(9, 13)}
    vault.update({t: [f'execute {back} positioned ^ ^-0.3 ^-0.38 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~ ~'] for t in range(13, 17)})
    tl = {1: ['function bm:p66/pose/stab_back', 'playsound minecraft:item.trident.riptide_1 neutral @a[distance=..16] ~ ~ ~ 0.5 1.4'],
          4: [f'DASH 1 @e[{FOE},distance=..10,sort=nearest,limit=1]'],
          5: ['function bm:p66/pose/stab', 'function bm:p66/sg/pierce'],
          8: ['function bm:p66/pose/jump', 'data merge entity @s {NoGravity:1b}', 'particle minecraft:snowflake ~ ~0.3 ~ 0.3 0.1 0.3 0.05 12']}
    for t, c in vault.items(): tl.setdefault(t, []).extend(c)
    tl[17] = ['data merge entity @s {NoGravity:0b}', 'function bm:p66/pose/stab_back', 'particle minecraft:poof ~ ~0.1 ~ 0.3 0.05 0.3 0.02 8',
              'playsound minecraft:entity.player.big_fall neutral @a[distance=..16] ~ ~ ~ 0.4 1.6']
    tl[22] = ['function bm:p66/pose/idle']
    atk.sig(G, 'p66', kid=1, tick_fn='p66/tick', state_fn='p66/state', anim_fn='p66/anim', s_obj='bm.ces', place_fn='p66/place', col=col('celi'),
            trigger=f'execute unless data entity @s {{Sitting:1b}} if entity @e[{FOE},distance=3.5..10]', cd=140, end=24,
            dash_kw=dict(reach=1.7, speed=1.2, lift=0), timeline=tl)

    # ================================================================== DEMOCRATUS: the reaping whirl
    dby = 'by @e[type=minecraft:wolf,tag=bm.dmme,limit=1]'
    fn('p97/sg/two', [f'execute store result score #n bm.rng if entity @e[{FOE},distance=..7]', 'return run execute if score #n bm.rng matches 2..'])
    fn('p97/sg/spinplace', ['execute store result storage bm:tmp dmy.y int 36 run scoreboard players get @s bm.ksg', 'function bm:p97/place_y with storage bm:tmp dmy'])
    fn('p97/sg/reap', ['tag @s add bm.dmme', f'execute as @e[{FOE},distance=..6] at @s run function bm:p97/sg/reaped', 'tag @s remove bm.dmme',
                       'particle minecraft:sweep_attack ~ ~1 ~ 1.6 0.2 1.6 0 6', 'playsound minecraft:entity.player.attack.sweep neutral @a[distance=..20] ~ ~ ~ 1 0.6'])
    fn('p97/sg/reaped', [f'damage @s 5 minecraft:mob_attack {dby}', f'execute facing entity @e[type=minecraft:wolf,tag=bm.dmme,limit=1] feet positioned ^ ^ ^0.9 '
                         'if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass unless entity @e[type=minecraft:wolf,tag=bm.dmme,distance=..1.6] run tp @s ~ ~ ~',
                         'particle minecraft:soul ~ ~1 ~ 0.2 0.3 0.2 0.02 2'])
    fn('p97/sg/sweep', ['tag @s add bm.dmme', f'execute as @e[{FOE},distance=..4.5] run damage @s 12 minecraft:mob_attack {dby}', 'tag @s remove bm.dmme',
                        'particle minecraft:sweep_attack ~ ~1 ~ 2 0.2 2 0 10', 'particle minecraft:soul_fire_flame ~ ~0.5 ~ 2 0.2 2 0.03 30',
                        'playsound minecraft:entity.wither.shoot neutral @a[distance=..24] ~ ~ ~ 0.5 1.6', 'playsound minecraft:entity.player.attack.sweep neutral @a[distance=..24] ~ ~ ~ 1 0.5'])
    ring(fn, 'p97/sg/ring', 'minecraft:soul ~ ~ ~ 0 0.1 0 0.01 1', 3.0, 12, 0.6)
    tl = {1: ['function bm:p97/pose/swing_back', 'playsound minecraft:entity.wither.ambient neutral @a[distance=..20] ~ ~ ~ 0.4 1.6'],
          8: ['function bm:p97/pose/spin', 'effect give @s minecraft:slowness 2 4 true']}
    for t in (12, 22, 32): tl.setdefault(t, []).extend(['function bm:p97/sg/reap', 'function bm:p97/sg/ring'])
    tl[41] = ['function bm:p97/pose/swing']
    tl[43] = ['function bm:p97/sg/sweep']
    tl[52] = ['function bm:p97/pose/idle_a']
    atk.sig(G, 'p97', kid=1, tick_fn='p97/tick', state_fn='p97/state', anim_fn='p97/frame', s_obj='bm.dms', place_fn='p97/place', col=col('demo'),
            trigger='execute unless data entity @s {Sitting:1b} if function bm:p97/sg/two', cd=240, end=54, face='none',
            each=['execute if score @s bm.ksg matches 9..40 run function bm:p97/sg/spinplace',
                  f'execute unless score @s bm.ksg matches 9..40 if entity @e[{FOE},distance=..20] facing entity @e[{FOE},distance=..20,sort=nearest,limit=1] feet rotated ~ 0 run function bm:p97/place'],
            timeline=tl)

    # ================================================================== APOPHISS: coil and strike
    aby = 'by @e[type=minecraft:wolf,tag=bm.apme2,limit=1]'
    fn('p131/sg/strike', ['tag @s add bm.apme2', f'execute as @e[{FOE},distance=..3.6,sort=nearest,limit=1] at @s run function bm:p131/sg/struck', 'tag @s remove bm.apme2',
                          'playsound minecraft:entity.evoker_fangs.attack neutral @a[distance=..20] ~ ~ ~ 1 0.6'])
    fn('p131/sg/struck', [f'damage @s 16 minecraft:mob_attack {aby}', 'effect give @s minecraft:poison 4 1', 'particle minecraft:item_slime ~ ~1 ~ 0.3 0.4 0.3 0.1 12'])
    fn('p131/sg/lash', ['tag @s add bm.apme2', f'execute as @e[{FOE},distance=..4.5] run damage @s 8 minecraft:mob_attack {aby}', 'tag @s remove bm.apme2',
                        'particle minecraft:sweep_attack ~ ~1.2 ~ 1.8 0.3 1.8 0 6', 'playsound minecraft:entity.player.attack.sweep neutral @a[distance=..20] ~ ~ ~ 1 0.5'])
    atk.sig(G, 'p131', kid=1, tick_fn='p131/tick', state_fn='p131/state', anim_fn='p131/anim', s_obj='bm.aps', place_fn='p131/place', col=col('apo'),
            trigger=f'execute unless data entity @s {{Sitting:1b}} if entity @e[{FOE},distance=4..12]', cd=200, end=31,
            dash_kw=dict(reach=2.6, speed=1.1, lift=0), timeline={
                1: ['function bm:p131/pose/crouch', 'playsound minecraft:entity.ravager.ambient neutral @a[distance=..20] ~ ~ ~ 0.6 1.6'],
                5: ['function bm:p131/pose/battle', 'playsound minecraft:entity.cat.hiss neutral @a[distance=..20] ~ ~ ~ 1 0.5', 'particle minecraft:item_slime ~ ~0.5 ~ 0.6 0.2 0.6 0 6'],
                10: [f'DASH 1 @e[{FOE},distance=..12,sort=nearest,limit=1]'],
                11: ['function bm:p131/pose/bite', 'function bm:p131/sg/strike'],
                17: ['function bm:p131/pose/claw_up'],
                22: ['function bm:p131/pose/claw', 'function bm:p131/sg/lash'],
                28: ['function bm:p131/pose/idle_a']})

    # ================================================================== ASHUR: the fire wheel
    sby = 'by @e[type=minecraft:wolf,tag=bm.aspme,limit=1]'
    fn('p185/sg/singe', ['tag @s add bm.asfw', f'damage @s 6 minecraft:mob_attack {sby}', 'data merge entity @s {Fire:80s}', 'particle minecraft:lava ~ ~1 ~ 0.2 0.2 0.2 0 3'])
    fn('p185/sg/burn', ['tag @s add bm.aspme', f'execute as @e[{FOE},distance=..1.8,tag=!bm.asfw] at @s run function bm:p185/sg/singe', 'tag @s remove bm.aspme'])
    fn('p185/sg/wheelplace', ['execute store result storage bm:tmp asy.y int 45 run scoreboard players get @s bm.kd', 'function bm:p185/sg/wheel_y with storage bm:tmp asy'])
    fn('p185/sg/wheel_y', ['$execute rotated ~$(y) 0 run function bm:p185/place'])
    ring(fn, 'p185/sg/flames', 'minecraft:flame ~ ~ ~ 0 0 0 0.01 1', 1.0, 10, 0.9)
    fn('p185/sg/erupt', ['tag @s add bm.aspme', f'execute as @e[{FOE},distance=..3] run damage @s 9 minecraft:mob_attack {sby}', f'execute as @e[{FOE},distance=..3] run data merge entity @s {{Fire:100s}}',
                         'tag @s remove bm.aspme', 'tag @e[tag=bm.asfw] remove bm.asfw',
                         'particle minecraft:flame ~ ~0.5 ~ 1.4 0.4 1.4 0.06 50', 'particle minecraft:lava ~ ~0.5 ~ 1 0.2 1 0 12',
                         'playsound minecraft:entity.blaze.shoot neutral @a[distance=..24] ~ ~ ~ 1 0.8', 'playsound minecraft:item.firecharge.use neutral @a[distance=..24] ~ ~ ~ 1 0.6'])
    atk.sig(G, 'p185', kid=1, tick_fn='p185/tick', state_fn='p185/state', anim_fn='p185/anim', s_obj='bm.azs', place_fn='p185/place', col=col('ashur'),
            trigger=f'execute unless data entity @s {{Sitting:1b}} if entity @e[{FOE},distance=3..12]', cd=200, end=29, face='none',
            dash_kw=dict(reach=1.2, speed=0.9, lift=2, trail=['function bm:p185/sg/flames', 'function bm:p185/sg/burn']),
            each=['execute if score @s bm.ksg matches 1000 run function bm:p185/sg/wheelplace',
                  f'execute unless score @s bm.ksg matches 1000 if entity @e[{FOE},distance=..20] facing entity @e[{FOE},distance=..20,sort=nearest,limit=1] feet rotated ~ 0 run function bm:p185/place'],
            timeline={
                1: ['function bm:p185/pose/crouch', 'particle minecraft:flame ~ ~0.3 ~ 0.4 0.1 0.4 0.02 12', 'playsound minecraft:block.fire.ambient neutral @a[distance=..16] ~ ~ ~ 1 1.4'],
                5: ['function bm:p185/pose/jump', 'tag @e[tag=bm.asfw] remove bm.asfw', f'DASH 1 @e[{FOE},distance=..12,sort=nearest,limit=1]'],
                6: ['function bm:p185/pose/crouch', 'particle minecraft:poof ~ ~0.1 ~ 0.4 0.05 0.4 0.03 8'],
                16: ['function bm:p185/pose/erupt', 'function bm:p185/sg/erupt'],
                26: ['function bm:p185/pose/idle']})

    # ================================================================== CECIL: the staff twirl
    pby = 'by @e[type=minecraft:wolf,tag=bm.cpme,limit=1]'
    for i in range(4):
        ring(fn, f'p46/pet/sg/orbit{i}', 'minecraft:enchant ~ ~ ~ 0 0 0 0.3 1', 1.2 - 0.2 * i, 10, 0.6 + 0.4 * i)
    fn('p46/pet/sg/beam', [f'particle minecraft:dust{{color:[0.7,0.5,1.0],scale:1.4}} ^ ^1.4 ^{0.5 * i:.1f} 0.05 0.05 0.05 0 2' for i in range(1, 29)])
    fn('p46/pet/sg/blast', ['tag @s add bm.cpme', f'execute as @e[{FOE},distance=..14,sort=nearest,limit=1] at @s run function bm:p46/pet/sg/blasted', 'tag @s remove bm.cpme',
                            f'execute facing entity @e[{FOE},distance=..14,sort=nearest,limit=1] eyes run function bm:p46/pet/sg/beam',
                            'playsound minecraft:entity.evoker.cast_spell neutral @a[distance=..24] ~ ~ ~ 1 0.8', 'playsound minecraft:entity.illusioner.cast_spell neutral @a[distance=..24] ~ ~ ~ 0.7 1.2'])
    fn('p46/pet/sg/blasted', [f'damage @s 14 minecraft:magic {pby}', f'execute as @e[{FOE},distance=0.1..2.5] run damage @s 6 minecraft:magic {pby}',
                              'particle minecraft:witch ~ ~1 ~ 0.8 0.6 0.8 0.1 30', 'particle minecraft:end_rod ~ ~1 ~ 0.3 0.4 0.3 0.1 12'])
    tl = {1: ['function bm:p46/pet/arm_cast', 'playsound minecraft:block.enchantment_table.use neutral @a[distance=..20] ~ ~ ~ 1 1.2']}
    for k in range(12): tl.setdefault(2 + k, []).append(f'function bm:p46/pet/sg/orbit{k % 4}')
    tl[15] = ['function bm:p46/pet/sg/blast']
    tl[19] = ['function bm:p46/pet/arm_down']
    atk.sig(G, 'p46/pet', kid=1, tick_fn='p46/pet/tick', state_fn='p46/pet/anim', anim_fn='p46/pet/anim', s_obj='bm.ksg', place_fn='p46/pet/place', col=col('cecil'),
            trigger=f'execute unless data entity @s {{Sitting:1b}} if entity @e[{FOE},distance=..14]', cd=180, end=21, face='none', st=99999, timeline=tl)

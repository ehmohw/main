"""2.84a: HARD MODE - once anyone has felled the Hollow King (bm.conqb 6+: a world that already has, wakes at once).

THE WAKING    the first second someone who has ever beaten the King is online, the world turns: a thunderclap, a moment of
              dark, and word of what has changed. It stays on (an operator can switch it off in admin/settings).
BLOOD MOONS   every 15 days (the settings page can still change it).
THE NIGHT'S   in the Overworld, the Nether and the End, a monster that isn't anything else already rolls again: 1.2% a
MONSTERS      DREAD, 6% a Champion, 18% an Elite. Of the rest, three in four come out with Strength and Resistance - one
              in five of those at II. (Blood Moons, invasions and lucky nights keep their own rolls.)
DREAD MOBS    far past a Champion: half again their health and more, netherite under a black-red trim, Strength II and
              Resistance, a cold that dims the light around them. Twice in a fight they gather themselves -
                THE PULSE   the ground about them boils red for a second and a half, then bursts (7, through armour);
                THE MARK    a column of souls falls on where you stand for a second and a quarter (9, through armour).
              Step out of either and it misses. They drop what a Champion drops, and 1 in 12 a Blood Moon Crystal - but
              never a Dread Token. Every Dread killed is counted (bm.dkill, and the world's #dk) - what they serve notices.
"""
import math
from items import T
from nbt import snbt, B, F

DREAD = '#b0102a'
DREAD_D = '#5a0812'
TYPES_SKIP = ('ghast', 'phantom', 'shulker')       # (no Dread version: they float, shoot or hide - nothing to dodge)
ROLL = (12, 72, 252)                                # per thousand: dread .. champion .. elite (in hard mode)


def ring(r, n, y=0.15):
    return [(round(r * math.cos(2 * math.pi * i / n), 2), y, round(r * math.sin(2 * math.pi * i / n), 2)) for i in range(n)]


def generate(G):
    fn, wjson, title, tellraw = G.fn, G.wjson, G.title, G.tellraw
    P = [T('[', 'dark_gray'), T('Black Market', 'dark_purple', bold=True), T('] ', 'dark_gray')]
    second, fast = G.FUNCS['loop/second'], G.FUNCS['loop/fast']
    G.FUNCS['load'][-1:-1] = ['execute unless score #hard bm.cfg matches 0.. run scoreboard players set #hard bm.cfg 0',
                              'execute unless score #hardoff bm.cfg matches 0.. run scoreboard players set #hardoff bm.cfg 0',
                              'execute unless score #dk bm.cfg matches 0.. run scoreboard players set #dk bm.cfg 0',
                              'scoreboard objectives add bm.dkill dummy', 'scoreboard objectives add bm.drcd dummy', 'scoreboard objectives add bm.drt dummy']
    G.OBJECTIVES += ['bm.dkill', 'bm.drcd', 'bm.drt']

    # ================================================================== the waking
    second.append('execute unless score #hard bm.cfg matches 1 unless score #hardoff bm.cfg matches 1 if entity @a[scores={bm.conqb=6..}] run function bm:p176/wake')
    fn('p176/wake', ['scoreboard players set #hard bm.cfg 1',
                     'execute if score #bmper bm.cfg matches 16.. run scoreboard players set #bmper bm.cfg 15',
                     'execute as @a at @s run playsound minecraft:entity.lightning_bolt.thunder ambient @s ~ ~ ~ 1 0.5',
                     'execute as @a at @s run playsound minecraft:ambient.cave ambient @s ~ ~ ~ 1 0.5',
                     'effect give @a minecraft:darkness 4 0 true',
                     'title @a times 10 70 30', title('@a', 'title', T('HARD MODE', DREAD, bold=True)),
                     title('@a', 'subtitle', T('Something older than the Hollow King has noticed you.', '#c8a0a0', italic=True)),
                     'schedule function bm:p176/wake_say 4s'])
    fn('p176/wake_say', [tellraw('@a', P + [T('The Hollow King is felled - and what made him turns its eye on this world.', DREAD, bold=True)]),
                         tellraw('@a', [T('  • ', DREAD_D), T('Blood Moons rise every 15 days.', 'gray')]),
                         tellraw('@a', [T('  • ', DREAD_D), T('Elites and Champions walk far more often; most monsters come out with Strength and Resistance.', 'gray')]),
                         tellraw('@a', [T('  • ', DREAD_D), T('DREAD monsters hunt the dark. ', DREAD, bold=True),
                                        T('When one gathers itself - a red ring at its feet, or souls falling on you - move.', 'gray')]),
                         tellraw('@a', [T('  • ', DREAD_D), T('A new trader has taken an empty stall in the Black Market.', 'gray')]),
                         tellraw('@a', [T('  • ', DREAD_D), T('Dungeon bosses fight harder for anyone who has beaten the King - and keep new things for them.', 'gray')])])
    # an operator's switch (admin/settings): off stays off until switched on again
    fn('admin/set/hard_0', ['scoreboard players set #hard bm.cfg 0', 'scoreboard players set #hardoff bm.cfg 1', 'function bm:admin/settings'])
    fn('admin/set/hard_1', ['scoreboard players set #hardoff bm.cfg 0', 'scoreboard players set #hard bm.cfg 1', 'function bm:admin/settings'])
    st = G.FUNCS['admin/settings']
    st.append(tellraw('@s', [T('  Hard Mode: ', 'white'), {'score': {'name': '#hard', 'objective': 'bm.cfg'}, 'color': 'aqua'}, T('  ', 'gray'),
                             T('[On]', 'green', click_event={'action': 'run_command', 'command': '/function bm:admin/set/hard_1'}), T(' ', 'gray'),
                             T('[Off]', 'red', click_event={'action': 'run_command', 'command': '/function bm:admin/set/hard_0'}),
                             T('  wakes by itself once the Hollow King falls', 'gray')]))

    # ================================================================== every monster rolls again in hard mode
    ARM, UNARM = G.ARMORED, G.UNARMORED
    d1, d2, d3 = ROLL
    n = 0
    for t in list(ARM) + list(UNARM):
        L = G.FUNCS[f'mobs/init/{t}']
        k = next(i for i, l in enumerate(L) if l.startswith('execute store result score #r bm.rng run random value 1..1000'))
        L.insert(k, f'execute if score #hard bm.cfg matches 1 unless dimension bm:gutter unless dimension bm:hollow_throne if function bm:p176/roll/{t} run return 0')
        n += 1
        dread = t not in TYPES_SKIP
        fn(f'p176/roll/{t}', ['execute store result score #hr bm.rng run random value 1..1000'] +
           ([f'execute if score #hr bm.rng matches 1..{d1} run function bm:p176/mk/{t}', f'execute if score #hr bm.rng matches 1..{d1} run return 1'] if dread else []) +
           [f'execute if score #hr bm.rng matches {d1 + 1}..{d2} run function bm:mobs/champion/{t}', f'execute if score #hr bm.rng matches {d1 + 1}..{d2} run return 1',
            f'execute if score #hr bm.rng matches {d2 + 1}..{d3} run function bm:mobs/elite/{t}', f'execute if score #hr bm.rng matches {d2 + 1}..{d3} run return 1',
            'function bm:p176/buff', 'return 0'])
        if dread:
            hp = ARM[t][0] if t in ARM else UNARM[t]
            mhp = hp * 5 if t in ARM else hp * 4
            name = {'text': 'Dread ', 'color': DREAD, 'bold': True, 'extra': [{'translate': f'entity.minecraft.{t}'}]}
            lines = [f'data merge entity @s {snbt(dict(G.NO_DROPS, DeathLootTable=f"bm:entities/dread/{t}", CustomName=name))}',
                     'tag @s add bm.dread', 'tag @s add bm.tiered']
            if t in ARM:
                for slot, piece in [('head', 'helmet'), ('chest', 'chestplate'), ('legs', 'leggings'), ('feet', 'boots')]:
                    lines.append(f'item replace entity @s armor.{slot} with minecraft:netherite_{piece}[enchantments={{"minecraft:protection":5,"minecraft:unbreaking":5}},'
                                 f'trim={{material:"minecraft:redstone",pattern:"minecraft:silence"}}]')
                lines.append(f'item replace entity @s weapon.mainhand with {G.WEAPON["champion"][ARM[t][1]]}')
            for e, a in [('strength', 1), ('resistance', 0), ('fire_resistance', 0)] + ([] if t in ARM else [('speed', 0), ('regeneration', 0)]):
                lines.append(f'effect give @s minecraft:{e} infinite {a} true')
            if t == 'creeper':
                lines.append('data merge entity @s {ExplosionRadius:5b,Fuse:20s}')
            lines += [f'attribute @s minecraft:max_health base set {mhp}', f'data modify entity @s Health set value {mhp}.0f',
                      'attribute @s minecraft:scale base set 1.25', 'attribute @s minecraft:knockback_resistance base set 0.8',
                      'attribute @s minecraft:follow_range base set 48', 'execute store result score @s bm.drcd run random value 40..120']
            fn(f'p176/mk/{t}', lines)
            wjson(f'bm/loot_table/entities/dread/{t}.json', {'type': 'minecraft:entity', 'pools': [
                {'rolls': 1, 'entries': [{'type': 'minecraft:loot_table', 'value': f'bm:entities/champion/{t}'}]},
                {'rolls': 1, 'entries': [G.loot_entry('blood_crystal')], 'conditions': [G.KILLED, G.chance(1 / 12)]}]})
    assert n >= 20, n
    # the rest: three in four with Strength and Resistance, one in five of those at II
    fn('p176/buff', ['execute store result score #hb bm.rng run random value 1..100', 'execute if score #hb bm.rng matches 76.. run return 0',
                     'execute if score #hb bm.rng matches 1..15 run return run function bm:p176/buff2',
                     'effect give @s minecraft:strength infinite 0 true', 'effect give @s minecraft:resistance infinite 0 true'])
    fn('p176/buff2', ['effect give @s minecraft:strength infinite 1 true', 'effect give @s minecraft:resistance infinite 1 true'])
    # (an operator's way to meet one: admin/dread_<mob> summons one in front of you)
    for t in ('zombie', 'skeleton', 'spider', 'vindicator', 'husk'):
        fn(f'admin/dread_{t}', [f'execute at @s rotated ~ 0 positioned ^ ^ ^4 run summon minecraft:{t} ~ ~ ~ {{Tags:["bm.seen","bm.dnew"]}}',
                                f'execute as @e[type=minecraft:{t},tag=bm.dnew] run function bm:p176/mk/{t}', 'tag @e[tag=bm.dnew] remove bm.dnew'])

    # ================================================================== a Dread's presence
    second += ['execute as @e[tag=bm.dread] at @s run function bm:p176/dread/aura']
    fn('p176/dread/aura', ['particle minecraft:soul ~ ~1 ~ 0.35 0.6 0.35 0.01 2',
                           f'particle minecraft:dust{{color:[0.35,0.0,0.06],scale:1.4}} ~ ~0.8 ~ 0.4 0.6 0.4 0 4',
                           'effect give @a[distance=..7,gamemode=!creative,gamemode=!spectator] minecraft:darkness 3 0 true',
                           'execute store result score #ha bm.rng run random value 1..6',
                           'execute if score #ha bm.rng matches 1 run playsound minecraft:entity.warden.heartbeat hostile @a[distance=..20] ~ ~ ~ 1.2 0.6'])

    # ================================================================== the Pulse and the Mark (both dodgeable, both through armour)
    fast += ['execute as @e[tag=bm.dread] at @s if entity @a[distance=..14,gamemode=!creative,gamemode=!spectator] run function bm:p176/dread/think',
             'execute as @e[type=minecraft:marker,tag=bm.drm] at @s run function bm:p176/dread/tickm']
    fn('p176/dread/think', ['scoreboard players remove @s bm.drcd 5', 'execute if score @s bm.drcd matches 1.. run return 0',
                            'execute store result score @s bm.drcd run random value 110..190',
                            'execute store result score #dra bm.rng run random value 1..2',
                            'execute if score #dra bm.rng matches 1 if entity @a[distance=..5,gamemode=!creative,gamemode=!spectator] run return run function bm:p176/dread/pulse',
                            'execute as @p[distance=..14,gamemode=!creative,gamemode=!spectator] at @s run function bm:p176/dread/mark'])
    fn('p176/dread/pulse', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.drm","bm.drpulse","bm.drnew"]}',
                            'scoreboard players set @e[type=minecraft:marker,tag=bm.drnew] bm.drt 30', 'tag @e[type=minecraft:marker,tag=bm.drnew] remove bm.drnew',
                            'playsound minecraft:entity.warden.roar hostile @a[distance=..24] ~ ~ ~ 0.8 1.4',
                            'effect give @s minecraft:slowness 2 3 true'])
    fn('p176/dread/mark', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.drm","bm.drmark","bm.drnew"]}',
                           'scoreboard players set @e[type=minecraft:marker,tag=bm.drnew] bm.drt 25', 'tag @e[type=minecraft:marker,tag=bm.drnew] remove bm.drnew',
                           'playsound minecraft:entity.warden.sonic_charge hostile @s ~ ~ ~ 1 0.8',
                           title('@s', 'actionbar', T('Something has marked where you stand -', DREAD, bold=True))])
    pr = lambda r, n_, part: [f'particle {part} ~{x} ~{y} ~{z} 0 0 0 0 1' for x, y, z in ring(r, n_)]
    fn('p176/dread/tickm', ['scoreboard players remove @s bm.drt 5',
                            'execute if entity @s[tag=bm.drpulse] run function bm:p176/dread/tick_pulse',
                            'execute if entity @s[tag=bm.drmark] run function bm:p176/dread/tick_mark',
                            'execute if score @s bm.drt matches ..-20 run kill @s'])
    fn('p176/dread/tick_pulse', pr(3.5, 18, 'minecraft:dust{color:[0.75,0.02,0.08],scale:1.6}') +
       ['particle minecraft:sculk_charge_pop ~ ~0.2 ~ 1.6 0.05 1.6 0.02 12', 'playsound minecraft:block.sculk_catalyst.bloom hostile @a[distance=..16] ~ ~ ~ 0.8 0.6',
        'execute if score @s bm.drt matches ..0 run function bm:p176/dread/pulse_go'])
    fn('p176/dread/pulse_go', ['particle minecraft:soul_fire_flame ~ ~0.3 ~ 1.8 0.2 1.8 0.12 60', 'particle minecraft:large_smoke ~ ~0.5 ~ 1.5 0.3 1.5 0.05 30',
                               'particle minecraft:sculk_soul ~ ~0.5 ~ 1.5 0.4 1.5 0.04 20',
                               'playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..24] ~ ~ ~ 0.9 0.7',
                               'execute as @a[distance=..3.6,gamemode=!creative,gamemode=!spectator] at @s run function bm:p176/dread/hit_pulse', 'kill @s'])
    fn('p176/dread/hit_pulse', ['damage @s 7 bm:dread', 'effect give @s minecraft:wither 3 0', 'particle minecraft:damage_indicator ~ ~1 ~ 0.3 0.4 0.3 0.2 6'])
    fn('p176/dread/tick_mark', pr(1.7, 12, 'minecraft:dust{color:[0.6,0.0,0.1],scale:1.3}') +
       ['particle minecraft:soul ~ ~3 ~ 0.6 1.2 0.6 0 6', 'particle minecraft:sculk_soul ~ ~4 ~ 0.3 0.3 0.3 0.01 2',
        'execute if score @s bm.drt matches ..0 run function bm:p176/dread/mark_go'])
    fn('p176/dread/mark_go', ['particle minecraft:soul_fire_flame ~ ~0.5 ~ 0.8 1.2 0.8 0.05 40', 'particle minecraft:explosion ~ ~0.5 ~ 0.3 0.2 0.3 0 2',
                              'playsound minecraft:entity.warden.attack_impact hostile @a[distance=..20] ~ ~ ~ 1.2 0.6',
                              'execute as @a[distance=..1.8,gamemode=!creative,gamemode=!spectator] at @s run function bm:p176/dread/hit_mark', 'kill @s'])
    fn('p176/dread/hit_mark', ['damage @s 9 bm:dread', 'effect give @s minecraft:darkness 4 0 true', 'particle minecraft:damage_indicator ~ ~1 ~ 0.3 0.4 0.3 0.2 6'])
    # (no Dread nearby any more - its last ring fades without a sound)
    second.append('execute as @e[type=minecraft:marker,tag=bm.drm] at @s unless entity @e[tag=bm.dread,distance=..40] run kill @s')
    import json, os
    wjson('bm/damage_type/dread.json', {'exhaustion': 0.0, 'message_id': 'bm.dread', 'scaling': 'never', 'effects': 'hurt'})
    for tg in ('bypasses_armor', 'bypasses_enchantments', 'bypasses_shield'):
        f_ = G.path('data', 'minecraft', 'tags', 'damage_type', f'{tg}.json')
        vals = json.load(open(f_))['values'] if os.path.exists(f_) else []
        wjson(f'minecraft/tags/damage_type/{tg}.json', {'replace': False, 'values': [v for v in vals if v != 'bm:dread'] + ['bm:dread']})

    # ================================================================== every Dread killed is counted
    wjson('bm/advancement/p176/dread_kill.json', {'criteria': {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {
        'entity': [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["bm.dread"]}'}}]}}},
        'rewards': {'function': 'bm:p176/dread/killed'}})
    fn('p176/dread/killed', ['advancement revoke @s only bm:p176/dread_kill', 'scoreboard players add @s bm.dkill 1', 'scoreboard players add #dk bm.cfg 1',
                             'playsound minecraft:entity.warden.death hostile @a[distance=..24] ~ ~ ~ 0.6 1.4',
                             title('@s', 'actionbar', [T('A Dread falls. ', DREAD, bold=True), T('Something, somewhere, counts it.', '#806060', italic=True)])])


def rp(R):
    R.LANG.update({'death.attack.bm.dread': '%1$s was torn apart by the Dread',
                   'death.attack.bm.dread.player': '%1$s was torn apart by the Dread while fighting %2$s'})


# (Omega's tithe and the like treat a Dread as no regular monster)
import phase172 as _P172
_P172.NOT_REGULAR = tuple(_P172.NOT_REGULAR) + ('bm.dread',)

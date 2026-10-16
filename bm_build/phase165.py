"""2.80g: HEIST REVIEW - no room the crew can't finish.

STRAGGLERS   a room that fights you is done when no guard (bm.gvg) or wave mob (bm.gvwv) is left in it - so one the crew can't
             reach kept the door shut for good: a vex resting inside a wall, a shulker that teleported onto the ceiling or the
             rafters, a phantom, blaze or breeze hanging up out of reach, a guard wedged behind a prop. Now any of them with no
             raider within 7 blocks for 40 seconds, while the crew is in that room (within 28 blocks), is flushed out to the
             middle of its room's floor and glows a few seconds, so it can be found and finished. (A crew that has walked on
             is no reason: the timer only runs with someone near. Bosses keep their own arenas.)
THE KIT, NEVER LOST  a loaned weapon dropped (Q) came back to you within a quarter second - long enough to burn in lava or fire.
             Now every new item in the vault is looked at the tick it appears, so a dropped kit item is back in your hands at
             once; and the kit is fireproof (like netherite), so not even a slip into lava takes it. (Paperweights and food
             can still be put down, as before.)
THE GUARDIAN, SCALED FOR EVERY CREW  the vault's guardian grows 50% stronger for each raider past the first - but no mob holds
             more than 1024 health, so from Tier IV on any crew of two or more met the same capped guardian (a crew of six, a
             third of the fight it was owed), its bar opened part-empty and its shell came at the wrong times. Now what's over
             1024 is a reserve that keeps its health topped up; the bar and the shell read health and reserve against the whole.
"""
from items import T


def generate(G):
    fn, title = G.fn, G.title
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.gvidle dummy']
    G.OBJECTIVES.append('bm.gvidle')
    near = 'tag=bm.gvp,gamemode=!spectator'
    second = G.FUNCS['loop/second']
    for tg in ('bm.gvg', 'bm.gvwv'):
        second.insert(-1, f'execute in bm:gutter as @e[tag={tg},tag=!bm.gvboss] at @s run function bm:p165/idle')
    # ---- the kit, never lost: every new item looked at once, the tick it appears (the quarter-second sweep stays as a backstop)
    fast = G.FUNCS['loop/fast']
    sweep = next(l for l in fast if 'function bm:p98/kit/bounce' in l)
    G.FUNCS['tick'].append('execute in bm:gutter as @e[type=minecraft:item,tag=!bm.kseen,distance=0..] run function bm:p165/seen')
    fn('p165/seen', ['tag @s add bm.kseen', sweep.replace('execute in bm:gutter as @e[type=minecraft:item,distance=0..] ', 'execute ')])
    # ---- the guardian, scaled for every crew: past the 1024 a mob can hold, the rest is a reserve (topped up every 5 ticks)
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.gvres dummy', 'scoreboard objectives add bm.gvmx dummy']
    G.OBJECTIVES += ['bm.gvres', 'bm.gvmx']
    HPLINE = 'execute store result storage bm:gv h double 1 run scoreboard players get #h bm.rng'
    HSET = 'execute store result entity @s Health float 1 run scoreboard players get #h bm.rng'
    su = G.FUNCS['p70/boss/setup']
    k = su.index(HPLINE)
    su[k:k] = ['scoreboard players set @s bm.gvres 0', 'scoreboard players operation @s bm.gvmx = #h bm.rng',
               'execute if score #h bm.rng matches 1025.. run function bm:p165/cap']
    k = su.index(HSET)
    su.insert(k + 1, 'scoreboard players operation #h bm.rng = @s bm.gvmx')          # (the bar's max: the whole)
    fn('p165/cap', ['scoreboard players operation @s bm.gvres = #h bm.rng', 'scoreboard players remove @s bm.gvres 1024', 'scoreboard players set #h bm.rng 1024'])
    se = G.FUNCS['p70/boss/sec']
    HP = 'execute store result score #hp bm.rng run data get entity @s Health'
    MX = 'execute store result score #mx bm.rng run attribute @s minecraft:max_health get'
    assert HP in se and MX in se, 'p70/boss/sec reads its health'
    se.remove(HP)
    se[2:2] = [HP, 'execute if score @s bm.gvres matches 1.. run scoreboard players operation #hp bm.rng += @s bm.gvres']
    nbar = 0
    for i, l in enumerate(se):
        if 'store result bossbar' in l and l.endswith('value run data get entity @s Health'):
            se[i] = l.replace('value run data get entity @s Health', 'value run scoreboard players get #hp bm.rng'); nbar += 1
    assert nbar == 8, nbar
    se[se.index(MX)] = MX + '\nexecute if score @s bm.gvmx matches 1.. run scoreboard players operation #mx bm.rng = @s bm.gvmx'
    G.FUNCS['p70/boss/sec'] = [x for l in se for x in l.split('\n')]
    fast.append('execute as @e[tag=bm.gvboss,scores={bm.gvres=1..}] run function bm:p165/refill')
    fn('p165/refill', ['execute store result score #a bm.rng run data get entity @s Health',
                       'execute if score #a bm.rng matches ..0 run return 0',
                       'scoreboard players set #m bm.rng 1024', 'scoreboard players operation #m bm.rng -= #a bm.rng',
                       'scoreboard players operation #m bm.rng < @s bm.gvres', 'execute if score #m bm.rng matches ..0 run return 0',
                       'scoreboard players operation @s bm.gvres -= #m bm.rng', 'scoreboard players operation #a bm.rng += #m bm.rng',
                       'execute store result entity @s Health float 1 run scoreboard players get #a bm.rng'])
    # (a crew that changes mid-heist rescales the living (phase104): the guardian's whole and what's left of it, reserve and all)
    rs = G.FUNCS['p104/rescale']
    head = rs[:rs.index('execute store result score #m bm.rng run attribute @s minecraft:max_health base get 100')]
    assert len(head) == 10 and head[-1] == 'scoreboard players add #fn bm.rng 100', head
    dmg = [l for l in rs if '#hadm' in l]
    rs.insert(0, 'execute if entity @s[tag=bm.gvboss] if score @s bm.gvmx matches 1.. run return run function bm:p165/rescale')
    fn('p165/rescale', head + [
        'scoreboard players operation @s bm.gvmx *= #fn bm.rng', 'scoreboard players operation @s bm.gvmx /= #fo bm.rng',
        'execute if score @s bm.gvmx matches ..0 run scoreboard players set @s bm.gvmx 1',
        'execute store result score #a bm.rng run data get entity @s Health', 'scoreboard players operation #a bm.rng += @s bm.gvres',
        'scoreboard players operation #a bm.rng *= #fn bm.rng', 'scoreboard players operation #a bm.rng /= #fo bm.rng',
        'execute if score #a bm.rng matches ..0 run scoreboard players set #a bm.rng 1',
        'scoreboard players operation #h bm.rng = @s bm.gvmx', 'execute if score #h bm.rng matches 1025.. run scoreboard players set #h bm.rng 1024',
        'execute store result storage bm:gv h double 1 run scoreboard players get #h bm.rng', 'function bm:p70/hp with storage bm:gv',
        'scoreboard players operation @s bm.gvres = #a bm.rng', 'execute if score #a bm.rng matches 1025.. run scoreboard players set #a bm.rng 1024',
        'scoreboard players operation @s bm.gvres -= #a bm.rng',
        'execute store result entity @s Health float 1 run scoreboard players get #a bm.rng'] + dmg +
       [f'execute if score @s bm.gvi matches {i + 1} store result bossbar bm:gvb{i} max run scoreboard players get @s bm.gvmx' for i in range(8)] +
       ['scoreboard players operation @s bm.gvcw = #crew bm.rng'])
    fn('p165/idle', [f'execute if entity @a[{near},distance=..7] run return run scoreboard players set @s bm.gvidle 0',
                     f'execute unless entity @a[{near},distance=..28] run return run scoreboard players set @s bm.gvidle 0',
                     'scoreboard players add @s bm.gvidle 1',
                     'execute if score @s bm.gvidle matches 40.. run function bm:p165/flush'])
    # (to the floor's middle: the nearest room marker - the room it's in - where the guards' leash also sends them)
    fn('p165/flush', ['scoreboard players set @s bm.gvidle 0', 'tag @s add bm.gvflush',
                      'particle minecraft:poof ~ ~1 ~ 0.3 0.5 0.3 0.02 10',
                      'execute as @e[type=minecraft:marker,tag=bm.gvr,distance=..40,sort=nearest,limit=1] at @s run tp @e[tag=bm.gvflush,limit=1] ~ ~ ~',
                      'tag @s remove bm.gvflush',
                      'execute at @s run particle minecraft:poof ~ ~1 ~ 0.3 0.5 0.3 0.02 10',
                      'effect give @s minecraft:glowing 6 0 true',
                      'execute at @s run playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..24] ~ ~ ~ 0.6 1.6',
                      'execute at @s as @a[tag=bm.gvp,distance=..28] run ' + title('@s', 'actionbar', T('A straggler is flushed out into the open.', '#ffcf40'))])

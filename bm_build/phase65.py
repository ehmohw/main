"""2.56: every follower faints instead of dying - five minutes, then they're back.

- Cecil, Emma (and Celi): their summoning item rests 5 minutes after they faint (was 10).
- The Frog with Mustache and Donado used to be lost for good (re-hire for a Medallion / wait for the cell to fill).
  Now they faint: they limp home, and after 5 minutes they'll rejoin you there for free - right-click the Frog's
  hut sign or Donado's cell. (The cell itself refills 5 minutes after he leaves, for anyone else.)"""
from items import T


def generate(G):
    fn, title, tellraw, PREFIX = G.fn, G.title, G.tellraw, G.PREFIX
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.fgcd dummy', 'scoreboard objectives add bm.dncd dummy']
    G.OBJECTIVES += ['bm.fgcd', 'bm.dncd']
    second = []
    # every hired companion carries its owner's id (and so do the parts riding it), so a faint can be traced to them
    for tag in ('bm.frogpet', 'bm.donado'):
        second.append(f'execute as @e[type=minecraft:wolf,tag={tag}] run function bm:p65/own')
    fn('p65/own', ['execute on owner unless score @s bm.pid matches 1.. run function bm:p21/pid',
                   'execute store result score @s bm.pid on owner run scoreboard players get @s bm.pid',
                   'scoreboard players operation #wp bm.rng = @s bm.pid', 'execute on passengers run scoreboard players operation @s bm.pid = #wp bm.rng'])
    second += ['scoreboard players remove @a[scores={bm.fgcd=1..}] bm.fgcd 1', 'scoreboard players remove @a[scores={bm.dncd=1..}] bm.dncd 1']
    s = G.FUNCS['loop/second']
    k = next(i for i, l in enumerate(s) if 'tag=bm.fp_disp] unless function bm:p20/frog/has_vehicle run kill @s' in l)
    # a head part left without its wolf: he fainted (the parts are tidied away right after)
    s[k:k] = second + [
        'execute as @e[type=minecraft:item_display,tag=bm.frr_head] unless function bm:p20/frog/has_vehicle if score @s bm.pid matches 1.. at @s run function bm:p65/faint_fg',
        'execute as @e[type=minecraft:item_display,tag=bm.dnr_head] unless function bm:p20/frog/has_vehicle if score @s bm.pid matches 1.. at @s run function bm:p65/faint_dn']
    for k in ('fg', 'dn'):
        fn(f'p65/faint_{k}', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players reset @s bm.pid',
                              'particle minecraft:poof ~ ~0.5 ~ 0.3 0.4 0.3 0.02 16', 'playsound minecraft:entity.player.hurt_sweet_berry_bush neutral @a[distance=..16] ~ ~ ~ 0.6 1.2',
                              f'execute as @a if score @s bm.pid = #me bm.pid run function bm:p65/fainted_{k}'])
    fn('p65/fainted_fg', ['scoreboard players set @s bm.fgcd 300', 'tag @s add bm.fgowed',
                          tellraw('@s', PREFIX + [T('The Frog with Mustache faints! ', 'green', bold=True),
                                                  T('He limps home to his hut. In 5 minutes he\'ll rejoin you there - no charge.', 'gray')])])
    fn('p65/fainted_dn', ['scoreboard players set @s bm.dncd 300', 'tag @s add bm.dnowed',
                          tellraw('@s', PREFIX + [T('Donado faints! ', '#e8d29a', bold=True),
                                                  T('He scrambles back to the mothership cell to lick his wounds. In 5 minutes he\'ll come with you again.', 'gray')])])
    mins = lambda o: [f'execute store result score #m bm.rng run scoreboard players get @s {o}', 'scoreboard players add #m bm.rng 59',
                      'scoreboard players operation #m bm.rng /= #60 bm.rng']
    # the Frog's hut: resting? owed a free return?
    h = G.FUNCS['p20/frog/hire']
    k = next(i for i, l in enumerate(h) if 'p20/frog/recall' in l) + 1
    h[k:k] = ['execute if score @s bm.fgcd matches 1.. run return run function bm:p65/frog_rest',
              'execute if entity @s[tag=bm.fgowed] run return run function bm:p65/frog_back']
    fn('p65/frog_rest', mins('bm.fgcd') + [title('@s', 'actionbar', [T('The Frog with Mustache is still recovering: about ', 'gray'),
                                                                     {'score': {'name': '#m', 'objective': 'bm.rng'}, 'color': 'white'}, T(' min.', 'gray')])])
    fn('p65/frog_back', ['tag @s remove bm.fgowed', 'function bm:p20/frog/summon',
                         title('@s', 'actionbar', T('"Ribbit. Back on my feet - shall we?" The Frog with Mustache rejoins you.', 'green'))])
    # Donado's cell: the same, and he comes back to you even if the cell's empty
    d = G.FUNCS['p25/don/hire']
    k = next(i for i, l in enumerate(d) if 'p25/don/recall' in l) + 1
    d[k:k] = ['execute if score @s bm.dncd matches 1.. run return run function bm:p65/don_rest',
              'execute if entity @s[tag=bm.dnowed] run return run function bm:p65/don_back']
    fn('p65/don_rest', mins('bm.dncd') + [title('@s', 'actionbar', [T('Donado is still licking his wounds: about ', 'gray'),
                                                                    {'score': {'name': '#m', 'objective': 'bm.rng'}, 'color': 'white'}, T(' min.', 'gray')])])
    fn('p65/don_back', ['tag @s remove bm.dnowed',
                        'execute at @e[type=minecraft:item_display,tag=bm.don_pen,sort=nearest,limit=1] run function bm:p25/don/summon',
                        title('@s', 'actionbar', T('*happy bark* Donado bounds back to your side!', '#e8d29a'))])
    p = G.FUNCS['p25/don/pen_empty']
    p[:] = [l.replace('scoreboard players set @s bm.dng 600', 'scoreboard players set @s bm.dng 300') for l in p]

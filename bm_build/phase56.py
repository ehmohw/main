"""Phase 2.36: fixes.

- Trading screens no longer close by themselves: the market patch re-teleported Vinny, the Fence and Old Barnaby in place
  every 10 seconds (their new spot was inside the radius that looks for their old one), and in 26.3 any teleport ends a
  trade. Now only a trader still on its old spot moves (phase35).
- Old Barnaby steps out from behind the counter post (phase35 MOVES).
- Nameplates follow their trader: a plate that has drifted from its trader (Zorp walks; three traders were moved) is set
  again over it.
- Cecil (the companion) is summoned where there's room - never inside a slope or a step in front of you.
- /function bm:admin/blood_moon starts a Blood Moon tonight (jumping to nightfall if it's day); calling bloodmoon/start
  by hand now sticks instead of ending on the next tick."""


def generate(G):
    fn, tellraw, PREFIX = G.fn, G.tellraw, G.PREFIX
    from items import T
    second = []

    # nameplates: re-seat any that drifted from their trader
    # (a plate already sitting on another trader is never taken - two traders side by side can't trade plates back and forth)
    second += ['tag @e[type=minecraft:text_display,tag=bm.pok] remove bm.pok',
               'execute as @e[type=#bm:p56_traders,tag=bm.plated] at @s run tag @e[type=minecraft:text_display,tag=bm.plate,distance=..0.7] add bm.pok',
               'execute as @e[type=#bm:p56_traders,tag=bm.plated] at @s unless entity @e[type=minecraft:text_display,tag=bm.plate,distance=..0.7] run function bm:p56/replate']
    G.wjson('bm/tags/entity_type/p56_traders.json', {'values': ['minecraft:villager', 'minecraft:wandering_trader']})
    fn('p56/replate', ['kill @e[type=minecraft:text_display,tag=bm.plate,tag=!bm.pok,distance=..4,sort=nearest,limit=1]', 'function bm:p26/plate/add',
                       'tag @e[type=minecraft:text_display,tag=bm.plate,distance=..0.7] add bm.pok'])

    # Cecil: summoned 1.2 blocks ahead if there's room, else a block up (a step), else at your feet
    sm = G.FUNCS['p46/pet/summon']
    G.FUNCS['p56/cecil_here'] = [l.replace('^ ^ ^1.2', '~ ~ ~') for l in sm]
    sm[:] = ['execute positioned ^ ^ ^1.2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:p56/cecil_here',
             'execute positioned ^ ^1 ^1.2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:p56/cecil_here',
             'function bm:p56/cecil_here']

    # the Blood Moon by hand
    G.FUNCS['bloodmoon/start'][0:0] = ['scoreboard players set #forced bm.bm 1', 'execute unless score #tod bm.bm matches 13000..22999 run time set night']
    fn('admin/blood_moon', ['scoreboard players set #forced bm.bm 1',
                            'execute unless score #tod bm.bm matches 13000..22999 run time set night',
                            tellraw('@s', PREFIX + [T('A Blood Moon rises tonight. ', 'dark_red', bold=True),
                                                    T('(It ends at dawn, like any other.)', 'gray')])])

    s = G.FUNCS['loop/second']
    s[-1:-1] = second

"""3.0: THE LOOM SANCTUARY - where the Keeper of Bonds waits (keeper_sanctuary.py, keeper_art.py). A small island high in the
Overworld sky that isn't there at all until someone has earned the way to it.

THE COMPASS OF BONDS  once you have met every other follower (bm:met/<kind>: every one of phase125.WHO but the Keeper itself), the
           compass is yours - once, with a word - and the sanctuary is woven into the sky (placed the first time anyone earns it).
           Its needle points at the island; it hangs at y {Y} - high above the clouds.
THE WAY UP  stand right under the island holding the compass, for three seconds: a thread of light draws you up to its landing
           circle. THE WAY DOWN: step off the edge - anyone falling from it drifts down (Slow Falling) to the ground.
Nothing on it can be broken (Adventure mode while you're on it, as in the dungeons)."""
from items import item, T
from nbt import IntArray
import keeper_sanctuary as KS

COL = '#ffd6f0'
X0, Y0, Z0 = -2600, 262, 2600                 # (the template's corner; its grass at Y0 + TOP)
SX, SY, SZ = KS.SIZE
KVER = 1
BOX = f'x={X0},y={Y0},z={Z0},dx={SX - 1},dy={SY - 1},dz={SZ - 1}'
W = lambda p: (X0 + p[0], Y0 + p[1], Z0 + p[2])
AX, AY, AZ = W(KS.ARRIVAL)
DX, DY, DZ = W(KS.DAIS)
UNDER = f'x={AX - 3},y=-64,z={AZ - 3},dx=6,dy={Y0 + 64 - 2},dz=6'     # (the column under the landing circle)
FALL = f'x={X0 - 24},y={Y0 - 240},z={Z0 - 24},dx={SX + 48},dy={240 + KS.TOP},dz={SZ + 48}'
__doc__ = __doc__.replace('{Y}', str(Y0 + KS.TOP))

item('bond_compass', 'minecraft:compass', 'The Compass of Bonds', COL,
     ['A compass strung with fifty threads, one for every', 'friend you have walked beside. Its needle points up.',
      ('It leads to the Loom Sanctuary, high in the sky.', 'light_purple'), ('Stand beneath the island holding it: the thread draws you up.', 'blue')],
     glint=True, stack=1, cat='map',
     comps={'minecraft:lodestone_tracker': {'target': {'dimension': 'minecraft:overworld', 'pos': IntArray([int(DX), int(DY), int(DZ)])}, 'tracked': False}})


def generate(G):
    import phase125 as P125
    import phase220 as P220
    fn, title, tellraw, give = G.fn, G.title, G.tellraw, G.give
    second = G.FUNCS['loop/second']
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.kbq dummy']
    G.OBJECTIVES.append('bm.kbq')
    KS.build(markers=True).export(G.path('data', 'bm', 'structure', 'p253_loom.nbt'))
    holds = 'items entity @s weapon.* *[minecraft:custom_data~{bm:"bond_compass"}]'
    # ---- the compass: every other follower met
    kinds = [w for w in P125.WHO if w != 'keeper']
    fn('p253/all_met', [f'execute unless entity @s[advancements={{bm:met/{P220.MET_KEY.get(w, w)}=true}}] run return 0' for w in kinds] + ['return 1'])
    second.append('execute as @a[tag=!bm.kbcomp] if function bm:p253/all_met at @s run function bm:p253/grant')
    fn('p253/grant', ['tag @s add bm.kbcomp', give('bond_compass'), 'scoreboard players set #kbwant bm.p2 1',
                      'playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 0.8', 'playsound minecraft:entity.allay.ambient_with_item player @s ~ ~ ~ 1 1.2',
                      'particle minecraft:end_rod ~ ~1 ~ 0.6 0.8 0.6 0.05 40', 'title @s times 20 80 30',
                      title('@s', 'title', T('Every bond, woven', COL, bold=True)),
                      title('@s', 'subtitle', T(f'{len(kinds)} friends - and one more, waiting in the sky', '#e8d8ff', italic=True)),
                      tellraw('@s', [T('The Compass of Bonds ', COL, bold=True), T('is in your pack. Its needle points somewhere high above the clouds.', 'gray')])])
    G.FUNCS['load'][-1:-1] = ['execute if entity @a[tag=bm.kbcomp] run scoreboard players set #kbwant bm.p2 1']
    # ---- weaving the island into the sky (the first time it's wanted, or after a version bump)
    fl = f'{X0 - 4} {Z0 - 4} {X0 + SX + 4} {Z0 + SZ + 4}'
    fn('p253/build/try', [f'execute in minecraft:overworld run forceload add {fl}',
                          f'execute in minecraft:overworld store success score #kbload bm.p2 if loaded {X0} {Y0} {Z0} if loaded {X0 + SX - 1} {Y0} {Z0 + SZ - 1}',
                          'execute unless score #kbload bm.p2 matches 1 run return 0',
                          f'execute in minecraft:overworld run kill @e[type=minecraft:marker,tag=bm.kbm,{BOX}]',
                          f'execute in minecraft:overworld run place template bm:p253_loom {X0} {Y0} {Z0}',
                          f'execute in minecraft:overworld as @e[type=minecraft:marker,{BOX}] if entity @s[tag=bm.kb_spawn] run tag @s add bm.kbm',
                          f'execute in minecraft:overworld as @e[type=minecraft:marker,{BOX}] if entity @s[tag=bm.kb_dais] run tag @s add bm.kbm',
                          f'execute in minecraft:overworld as @e[type=minecraft:marker,{BOX}] if entity @s[tag=bm.kb_arrive] run tag @s add bm.kbm',
                          f'scoreboard players set #kbver bm.p2 {KVER}', f'execute in minecraft:overworld run forceload remove {fl}'])
    second.append(f'execute if score #kbwant bm.p2 matches 1 unless score #kbver bm.p2 matches {KVER} run function bm:p253/build/try')
    # ---- the way up: beneath it, holding the compass, three seconds
    second += [f'execute in minecraft:overworld as @a[{UNDER}] if {holds} at @s run function bm:p253/rise',
               f'execute in minecraft:overworld as @a[{UNDER},scores={{bm.kbq=1..}}] unless {holds} run scoreboard players set @s bm.kbq 0']
    fn('p253/rise', ['execute unless score #kbver bm.p2 matches 1.. run return run ' + title('@s', 'actionbar', T('The needle trembles... the threads are still being woven. (a moment)', 'gray', italic=True)),
                     'scoreboard players add @s bm.kbq 1', 'particle minecraft:end_rod ~ ~ ~ 0.3 2 0.3 0.05 20',
                     'playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1.4',
                     'execute if score @s bm.kbq matches ..2 run return run ' + title('@s', 'actionbar', T('A thread of light lowers from the sky...', COL, italic=True)),
                     'scoreboard players set @s bm.kbq 0', f'tp @s {AX} {AY} {AZ} 180 0', 'effect give @s minecraft:slow_falling 6 0 true',
                     f'execute positioned {AX} {AY} {AZ} run particle minecraft:end_rod ~ ~1 ~ 0.6 1 0.6 0.1 60',
                     f'execute positioned {AX} {AY} {AZ} run playsound minecraft:block.beacon.power_select player @a[distance=..24] ~ ~ ~ 1 1.6',
                     title('@s', 'actionbar', T('The Loom Sanctuary.', COL, bold=True))])
    # ---- the way down, and nothing broken on it
    second += [f'execute in minecraft:overworld as @a[{FALL},gamemode=!creative,gamemode=!spectator] at @s if block ~ ~-1 ~ minecraft:air if block ~ ~-2 ~ minecraft:air '
               'run effect give @s minecraft:slow_falling 4 0 true',
               f'execute in minecraft:overworld as @a[{BOX},gamemode=survival] run function bm:p253/adv/in',
               'execute as @a[tag=bm.kbadv,gamemode=adventure] at @s unless function bm:p253/on_it run function bm:p253/adv/out']
    fn('p253/on_it', [f'execute in minecraft:overworld if entity @s[{BOX}] run return 1', 'return 0'])
    fn('p253/adv/in', ['tag @s add bm.kbadv', 'gamemode adventure @s'])
    fn('p253/adv/out', ['tag @s remove bm.kbadv', 'gamemode survival @s'])
    fn('admin/keeper/compass', ['tag @s remove bm.kbcomp', 'function bm:p253/grant'])
    fn('admin/keeper/go', ['scoreboard players set #kbwant bm.p2 1', 'execute unless score #kbver bm.p2 matches 1.. run function bm:p253/build/try',
                           f'execute in minecraft:overworld run tp @s {AX} {AY} {AZ} 180 0'])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:marker,tag=bm.kbm]']

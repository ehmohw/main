"""2.72: ROOM CURSES, FORKS IN THE ROAD, CORRIDOR TRAPS.

ROOM CURSES   now and then a room is CURSED (a purple banner over the door says how): 9% of rooms at Tier I up to 21% at
              Tier V. Beat a cursed room and the pot takes a few extra coins. A curse only lands where it's fair:
                FOG       darkness creeps in (any room)
                FROST     the cold slows you (not the rooms you cross by jumping)
                LEADEN    no jumping at all (only puzzle rooms with nothing to jump)
                FRAGILE   your armour counts for half (fights)
                PHANTOMS  the guards are invisible - watch for the mould at their feet (fights)
                FRENZY    the guards are quicker and hit harder (fights)
                UNSTEADY  every few seconds the floor lurches and you float up for a moment (fights on solid ground)
FORKS         about one heist in three, a room is a FORK: a wall across it with two doors. The crew votes by standing on a
              pad: the SKULL door makes the next room Prime (if it's a fight) and cursed - and the pot pays well for it -
              the PLAIN door leaves it as it is. Everyone in the room must stand on the same pad for two seconds.
CORRIDOR TRAPS  some passages between rooms are trapped (20% at Tier I up to 40% at Tier V): FLAME JETS that roar up
              on a beat (watch for the smoke), SPIKES that spring from the floor (listen for the rumble), and ARROW SLITS
              that fire across the passage a moment after you step in (hear the click).
              (never in the passage out of the den, where the Fixer's care would heal it away)
"""
from items import T
from nbt import snbt, B, F, Int
from structures import Build
import phase70_rooms as RM
import phase75 as P75
import phase76_rooms as R6
from phase75_rooms import BASE, wall_glow
import phase110 as P110
import phase113 as P113

GOLD = '#ffcf40'
CURSE = '#c060ff'
rel, relf, IDENT = RM.rel, P110.relf, P110.IDENT
CURSES = {1: ('FOG', 'Darkness creeps in.'), 2: ('FROST', 'The cold slows you.'), 3: ('LEADEN', 'Nobody can jump in here.'),
          4: ('FRAGILE', 'Your armour counts for half.'), 5: ('PHANTOMS', 'The guards are invisible - watch for the mould at their feet.'),
          6: ('FRENZY', 'The guards are quicker and hit harder.'), 7: ('UNSTEADY', 'The floor lurches now and then - you float up.')}
FIGHT = ['guards', 'ambush', 'pit']
JUMPY = ['tiles', 'rafters', 'lasers', 'climb', 'spire', 'grapple']
CALM = ['levers', 'plates', 'dial', 'coffers', 'lamps', 'lightsout', 'tumbler', 'bench', 'library', 'pipes', 'apoth']
HOP = ['mason', 'dig']
ALLOWED = {1: [1, 2, 4, 5, 6, 7], 2: [1, 2, 3], 3: [1], 4: [1, 4, 5, 6], 5: [1, 2]}   # group: curses (1 fight, 2 calm, 3 jumpy, 4 the Sky Isles, 5 calm with a hop)
GROUP = {**{k: 1 for k in FIGHT}, **{k: 2 for k in CALM}, **{k: 3 for k in JUMPY}, 'isles': 4, **{k: 5 for k in HOP}}


def fork():
    b = R6.shell()
    for z in range(1, 24):
        for y in range(4, 15): b.set(13, y, z, BASE['wall'])
    for z0 in (4, 18):
        for z in range(z0, z0 + 3):
            for y in range(4, 7): b.set(13, y, z, 'minecraft:iron_bars')
    for z in range(4, 7):
        for x in (9, 10, 11): b.set(x, 3, z, 'minecraft:crying_obsidian')
    for z in range(18, 21):
        for x in (9, 10, 11): b.set(x, 3, z, 'minecraft:polished_diorite')
    R6.ctrl(b, 'fork'); return wall_glow(b)


P75.EXTRA_ROOMS['fork'] = fork
R6.NAMES['fork'] = 'The Fork'


def generate(G):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    label, sign, vbutton, press, themed, crew_say, oops, choose = P110.helpers(G)
    inst = lambda f: f'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run function {f}'
    crew = '@a[tag=bm.gvp,distance=..30]'
    P = [T('[', 'dark_gray'), T('Heist', GOLD, bold=True), T('] ', 'dark_gray')]
    def big(t_, sub, col, who=crew):
        return [f'title {who} times 5 50 15', title(who, 'title', T(t_, col, bold=True)), title(who, 'subtitle', T(sub, 'gray'))]
    objs = ['bm.gvcrs', 'bm.crl', 'bm.crf']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    inroom = 'positioned ~-12.5 ~-4 ~-12.5 as @a[tag=bm.gvp,dx=24,dy=24,dz=24]'
    foes = 'positioned ~-12.5 ~-4 ~-12.5 as @e[tag=bm.gvg,dx=24,dy=24,dz=24]'

    # ================================================================== ROOM CURSES
    G.FUNCS['p70/r/init'][0:0] = [f'execute if entity @s[tag=bm.gvr_{k}] run scoreboard players set #cg bm.rng {g}' for k, g in GROUP.items()] + \
                                 ['function bm:p116/curse/roll', 'scoreboard players set #cg bm.rng 0']
    G.FUNCS['load'].append('scoreboard players set #cg bm.rng 0')
    fn('p116/curse/roll', ['scoreboard players set @s bm.gvcrs 0', 'execute if score #cg bm.rng matches 0 run return 0', 'execute if score #fcr bm.gvv matches -1 run return 0',
                           'execute if score #fcr bm.gvv matches 1..7 run return run function bm:p116/curse/forced',
                           'execute store result score #r bm.rng run random value 1..100', 'scoreboard players operation #c bm.rng = @s bm.gvt',
                           'scoreboard players operation #c bm.rng *= #3 bm.rng', 'scoreboard players add #c bm.rng 6',
                           'execute if score #fcr bm.gvv matches 99 run scoreboard players set #r bm.rng 0',
                           'execute if score #r bm.rng <= #c bm.rng run function bm:p116/curse/pick'])
    G.FUNCS['load'].append('scoreboard players set #3 bm.rng 3')
    pick = []
    for g, L in ALLOWED.items():
        pick += [f'execute if score #cg bm.rng matches {g} store result score #i bm.rng run random value 0..{len(L) - 1}']
        pick += [f'execute if score #cg bm.rng matches {g} if score #i bm.rng matches {i} run return run function bm:p116/curse/set{c}' for i, c in enumerate(L)]
    fn('p116/curse/pick', pick)
    fn('p116/curse/forced', [f'execute if score #fcr bm.gvv matches {c} if score #cg bm.rng matches {g} run return run function bm:p116/curse/set{c}'
                             for g, L in ALLOWED.items() for c in L])
    for c, (nm, what) in CURSES.items():
        fn(f'p116/curse/set{c}', [f'scoreboard players set @s bm.gvcrs {c}',
                                  label(relf(1.2, 10.2, 12.5), [T(f'☠ CURSED: {nm} ☠\n', CURSE, bold=True), T(what, 'gray')], 0.7)])
    for nm_, v, txt in (('always', 99, 'every room that can be is cursed'), ('never', -1, 'no room is cursed'), ('chance', 0, 'rooms are cursed by chance')):
        fn(f'admin/curse_{nm_}', [f'scoreboard players set #fcr bm.gvv {v}', tellraw('@s', P + [T(f'From the next heist, {txt}.', 'gray')])])
    for c, (nm, what) in CURSES.items():
        fn(f'admin/curse_{nm.lower()}', [f'scoreboard players set #fcr bm.gvv {c}', tellraw('@s', P + [T(f'From the next heist, every room that can take it is cursed with {nm}.', 'gray')])])
    # the curse at work (in the room's tick)
    G.FUNCS['p70/r/tick'].insert(1, 'execute if score @s bm.gvcrs matches 1.. run function bm:p116/curse/tick')
    fn('p116/curse/tick', ['execute if score @s bm.gvs matches 3 run return 0',
                           'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #20 bm.rng'] +
       [f'execute if score @s bm.gvcrs matches {c} run function bm:p116/curse/t{c}' for c in CURSES])
    fn('p116/curse/t1', [f'execute if score #q bm.rng matches 0 {inroom} run effect give @s minecraft:darkness 3 0 true'])
    fn('p116/curse/t2', [f'execute if score #q bm.rng matches 0 {inroom} run effect give @s minecraft:slowness 2 0 true',
                         f'execute if score #q bm.rng matches 0 {inroom} at @s run particle minecraft:snowflake ~ ~1.5 ~ 0.6 0.6 0.6 0 4'])
    fn('p116/curse/t3', [f'execute {inroom} run function bm:p116/curse/leaden'])
    fn('p116/curse/leaden', ['execute unless score @s bm.crl matches 1.. run attribute @s minecraft:jump_strength modifier add bm:curse_leaden -1 add_multiplied_total',
                             'scoreboard players set @s bm.crl 3'])
    fn('p116/curse/t4', [f'execute {inroom} run function bm:p116/curse/fragile'])
    fn('p116/curse/fragile', ['execute unless score @s bm.crf matches 1.. run attribute @s minecraft:armor modifier add bm:curse_fragile -0.5 add_multiplied_total',
                              'scoreboard players set @s bm.crf 3'])
    fn('p116/curse/t5', [f'execute if score #q bm.rng matches 0 {foes} run effect give @s minecraft:invisibility 3 0 true',
                         f'execute if score #q bm.rng matches 0 {foes} at @s run particle minecraft:mycelium ~ ~0.1 ~ 0.3 0 0.3 0 6'])
    fn('p116/curse/t6', [f'execute {foes.replace("tag=bm.gvg", "tag=bm.gvg,tag=!bm.gvfrz")} run function bm:p116/curse/frenzy'])
    fn('p116/curse/frenzy', ['tag @s add bm.gvfrz', 'attribute @s minecraft:movement_speed modifier add bm:curse_frenzy 0.25 add_multiplied_base',
                             'attribute @s minecraft:attack_damage modifier add bm:curse_frenzy_hit 0.3 add_multiplied_base'])
    fn('p116/curse/t7', ['scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #100 bm.rng',
                         f'execute if score #q bm.rng matches 80 {inroom} at @s run playsound minecraft:block.sculk_shrieker.shriek player @s ~ ~ ~ 0.3 1.6',
                         f'execute if score #q bm.rng matches 99 {inroom} run effect give @s minecraft:levitation 1 1 true'])
    G.FUNCS['tick'] += ['scoreboard players remove @a[scores={bm.crl=1..}] bm.crl 1',
                        'execute as @a[scores={bm.crl=0}] run function bm:p116/curse/unleaden',
                        'scoreboard players remove @a[scores={bm.crf=1..}] bm.crf 1',
                        'execute as @a[scores={bm.crf=0}] run function bm:p116/curse/unfragile']
    fn('p116/curse/unleaden', ['attribute @s minecraft:jump_strength modifier remove bm:curse_leaden', 'scoreboard players reset @s bm.crl'])
    fn('p116/curse/unfragile', ['attribute @s minecraft:armor modifier remove bm:curse_fragile', 'scoreboard players reset @s bm.crf'])
    k = next(i for i, l in enumerate(G.FUNCS['p76/first_visit']) if l == 'tag @s add bm.gvseen')
    G.FUNCS['p76/first_visit'].insert(k + 1, 'execute if score @s bm.gvcrs matches 1.. run function bm:p116/curse/warn')
    warn = []
    for c, (nm, what) in CURSES.items():
        warn += [f'execute if score @s bm.gvcrs matches {c} run {l}' for l in big(f'CURSED: {nm}', what, CURSE)]
    fn('p116/curse/warn', warn + [f'execute as {crew} at @s run playsound minecraft:entity.elder_guardian.curse player @s ~ ~ ~ 0.4 1.4'])
    G.FUNCS['p70/solved'] += ['execute if score @s bm.gvcrs matches 1.. run function bm:p116/curse/won']
    fn('p116/curse/won', ['scoreboard players operation #c bm.rng = #gt bm.rng', 'scoreboard players add #c bm.rng 4', inst('bm:p75/pot_add'),
                          f'execute as @a[tag=bm.gvp,distance=..300] if score @s bm.gvi = #gi bm.rng run ' + title('@s', 'actionbar', [T('The curse lifts', CURSE, bold=True), T(' - a little extra in the pot.', 'gray')])])
    G.FUNCS['p70/unraid'] += ['function bm:p116/curse/unleaden', 'function bm:p116/curse/unfragile']

    # ================================================================== FORKS IN THE ROAD
    G.FUNCS['p75/lay/rooms'].insert(1, 'function bm:p116/fork/roll')
    fn('p116/fork/roll', ['scoreboard players set #fk bm.rng 0', 'scoreboard players set #fkn bm.rng 0', 'execute if score #ffk bm.gvv matches 2 run return 0',
                          'execute if score #frk bm.gvv matches 1.. unless score #ffk bm.gvv matches 1 run return 0',
                          'execute if score #gk bm.rng matches ..2 run return 0',
                          'execute store result score #r bm.rng run random value 1..3', 'execute if score #ffk bm.gvv matches 1 run scoreboard players set #r bm.rng 1',
                          'execute unless score #r bm.rng matches 1 run return 0', 'scoreboard players set #fk bm.rng 1',
                          'scoreboard players operation #m bm.rng = #gk bm.rng', 'scoreboard players remove #m bm.rng 1',
                          'execute store result score #fkq bm.rng run random value 2..3', 'execute if score #fkq bm.rng > #m bm.rng run scoreboard players operation #fkq bm.rng = #m bm.rng',
                          'execute if score #thr bm.rng matches 1.. if score #fkq bm.rng = #thq bm.rng run scoreboard players add #fkq bm.rng 1',
                          'execute if score #fkq bm.rng > #m bm.rng run return run scoreboard players set #fk bm.rng 0',
                          'scoreboard players operation #fkn bm.rng = #fkq bm.rng', 'scoreboard players add #fkn bm.rng 1',
                          'execute if score #thr bm.rng matches 1.. if score #fkn bm.rng = #thq bm.rng run return run scoreboard players set #fk bm.rng 0'])
    G.FUNCS['p75/lay/can_event'].insert(0, 'execute if score #fkn bm.rng matches 1.. if score #q bm.rng = #fkn bm.rng run return 0')
    k = next(i for i, l in enumerate(G.FUNCS['p75/lay/room']) if 'function bm:p113/throne/lay' in l)
    G.FUNCS['p75/lay/room'].insert(k + 1, 'execute if score #fk bm.rng matches 1 if score #q bm.rng = #fkq bm.rng run return run function bm:p116/fork/lay')
    fn('p116/fork/lay', ['function bm:p75/pc/fork', 'execute as @e[type=minecraft:marker,tag=bm.gvnew] run function bm:p75/claim', 'scoreboard players set #fk bm.rng 0'])
    for nm_, v in (('always', 1), ('never', 2), ('chance', 0)):
        fn(f'admin/fork_{nm_}', [f'scoreboard players set #ffk bm.gvv {v}', tellraw('@s', P + [T(f'Forks in the road: {nm_} (from the next heist).', 'gray')])])
    G.FUNCS['p70/r/init'] += ['execute if entity @s[tag=bm.gvr_fork] run return run function bm:p116/fork/init']
    G.FUNCS['p70/r/tick'] += ['execute if entity @s[tag=bm.gvr_fork] run return run function bm:p116/fork/tick']
    k = next(i for i, l in enumerate(G.FUNCS['p76/first_visit']) if 'bm.gvr_rest' in l)
    G.FUNCS['p76/first_visit'].insert(k + 1, 'execute if entity @s[tag=bm.gvr_fork] run return 0')
    fn('p116/fork/init', ['scoreboard players set @s bm.gvs 0', 'scoreboard players set @s bm.gvx 0', 'scoreboard players set @s bm.gvz 0',
                          label(relf(12.6, 8.2, 5.5), [T('☠ THE HARD WAY ☠\n', '#ff4a4a', bold=True), T('The next room is Prime and cursed -\nand the pot pays well for it.', 'gray')], 0.6, 'fixed', yaw=90),
                          label(relf(12.6, 8.2, 19.5), [T('THE SAFE WAY\n', '#d0d0d0', bold=True), T('The next room as it is.', 'gray')], 0.6, 'fixed', yaw=90),
                          sign(rel(4, 7.4, 12), 'THE FORK', 'Choose a door: the whole crew stands on one pad (dark for the skull, pale for the plain) for two seconds.', 0.6)])
    pad = lambda z0: f'positioned {relf(9, 3.9, z0)} as @a[tag=bm.gvp,dx=2,dy=2,dz=2]'
    fn('p116/fork/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'execute if score @s bm.gvs matches 0 run scoreboard players set @s bm.gvs 1',
                          'execute store result score #n bm.rng positioned ~-12.5 ~-4 ~-12.5 if entity @a[tag=bm.gvp,dx=24,dy=12,dz=24]',
                          'scoreboard players set #sk bm.rng 0', 'scoreboard players set #pl bm.rng 0',
                          f'execute {pad(4)} run scoreboard players add #sk bm.rng 1', f'execute {pad(18)} run scoreboard players add #pl bm.rng 1',
                          'execute if score #n bm.rng matches 1.. if score #sk bm.rng = #n bm.rng run scoreboard players add @s bm.gvx 1',
                          'execute unless score #sk bm.rng = #n bm.rng run scoreboard players set @s bm.gvx 0',
                          'execute if score #n bm.rng matches 1.. if score #pl bm.rng = #n bm.rng run scoreboard players add @s bm.gvz 1',
                          'execute unless score #pl bm.rng = #n bm.rng run scoreboard players set @s bm.gvz 0',
                          'execute if score @s bm.gvx matches 1 run ' + crew_say([T('The skull door... ', '#ff4a4a', bold=True), T('hold still, all of you.', 'gray')], r=18),
                          'execute if score @s bm.gvz matches 1 run ' + crew_say([T('The plain door... ', '#d0d0d0', bold=True), T('hold still, all of you.', 'gray')], r=18),
                          'execute if score @s bm.gvx matches 40.. run return run function bm:p116/fork/hard',
                          'execute if score @s bm.gvz matches 40.. run return run function bm:p116/fork/safe'])
    fn('p116/fork/hard', [f'fill {rel(13, 4, 4)} {rel(13, 6, 6)} minecraft:air replace minecraft:iron_bars', 'scoreboard players operation #nq bm.rng = @s bm.gvq',
                          'scoreboard players add #nq bm.rng 1',
                          'execute as @e[type=minecraft:marker,tag=bm.gvr] if score @s bm.gvi = #gi bm.rng if score @s bm.gvq = #nq bm.rng at @s run function bm:p116/fork/harden',
                          f'execute as {crew} at @s run playsound minecraft:entity.wither.spawn player @s ~ ~ ~ 0.4 1.6'] +
       big('THE HARD WAY', 'The next room is waiting for you...', '#ff4a4a') + ['function bm:p70/solved'])
    fn('p116/fork/safe', [f'fill {rel(13, 4, 18)} {rel(13, 6, 20)} minecraft:air replace minecraft:iron_bars', f'execute as {crew} at @s run playsound minecraft:block.iron_door.open player @s ~ ~ ~ 1 1'] +
       big('THE SAFE WAY', 'Steady does it.', '#d0d0d0') + ['function bm:p70/solved'])
    # (the next room, made harder: Prime if it's a fight, cursed if it can be, and worth more)
    fn('p116/fork/harden', ['tag @s add bm.gvskull'] +
       [f'execute if entity @s[tag=bm.gvr_{k}] unless entity @s[tag=bm.gvprime] run function bm:p116/fork/prime' for k in P113.PRIME_KINDS] +
       [f'execute if entity @s[tag=bm.gvr_{k}] run scoreboard players set #cg bm.rng {g}' for k, g in GROUP.items()] +
       ['execute unless score @s bm.gvcrs matches 1.. unless score #cg bm.rng matches 0 run function bm:p116/curse/pick', 'scoreboard players set #cg bm.rng 0'])
    fn('p116/fork/prime', ['tag @s add bm.gvprime',
                           label(relf(1.2, 8.6, 12.5), [T('⚔ PRIME ⚔\n', P113.PRIME, bold=True), T('Tougher guards - richer pickings', 'gray')], 0.75)])
    G.FUNCS['p70/solved'] += ['execute if entity @s[tag=bm.gvskull] run function bm:p116/fork/paid']
    fn('p116/fork/paid', ['scoreboard players operation #c bm.rng = #gt bm.rng', 'scoreboard players operation #c bm.rng *= #4 bm.rng', 'scoreboard players add #c bm.rng 10',
                          inst('bm:p75/pot_add'),
                          f'execute as @a[tag=bm.gvp,distance=..300] if score @s bm.gvi = #gi bm.rng run ' + title('@s', 'actionbar', [T('The hard way pays! ', '#ff4a4a', bold=True), T('A fat cut into the pot.', 'gray')])])

    # ================================================================== CORRIDOR TRAPS (in the straight and bending passages, just past a room's exit) (the layout cursor stands at a block centre, so +27 +12 is the passage centre)
    for cn in ('st', 'lf', 'rt'):
        L = G.FUNCS[f'p75/cn/{cn}']
        k = next(i for i, l in enumerate(L) if l.startswith('tp @s'))
        L.insert(k, 'execute if function bm:p116/trap/roll positioned ~27 ~4 ~12 run function bm:p116/trap/place')
    fn('p116/trap/roll', ['execute if score #q bm.rng matches 0 run return fail', 'execute if score #ftr bm.gvv matches 2 run return fail', 'execute if score #ftr bm.gvv matches 1 run return 1',
                          'execute store result score #r bm.rng run random value 1..100', 'scoreboard players operation #c bm.rng = #gt bm.rng',
                          'scoreboard players operation #c bm.rng *= #5 bm.rng', 'scoreboard players add #c bm.rng 15',
                          'execute if score #r bm.rng <= #c bm.rng run return 1', 'return fail'])
    G.FUNCS['load'].append('scoreboard players set #5 bm.rng 5')
    for nm_, v in (('always', 1), ('never', 2), ('chance', 0)):
        fn(f'admin/traps_{nm_}', [f'scoreboard players set #ftr bm.gvv {v}', tellraw('@s', P + [T(f'Corridor traps: {nm_} (from the next heist).', 'gray')])])
    def bd(blk, pos, sc, tags, tr=(0, 0, 0)):
        return f'summon minecraft:block_display {pos} ' + snbt({'Tags': ['bm.gvprop'] + tags, 'block_state': blk, 'interpolation_duration': Int(3),
                                                               'transformation': {'left_rotation': IDENT, 'right_rotation': IDENT, 'translation': [F(v) for v in tr], 'scale': [F(v) for v in sc]}})
    fn('p116/trap/place', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.gvprop","bm.gvtrap","bm.gvtrn"]}',
                           'scoreboard players operation @e[type=minecraft:marker,tag=bm.gvtrn,distance=..1] bm.gvi = #gi bm.rng',
                           'scoreboard players operation @e[type=minecraft:marker,tag=bm.gvtrn,distance=..1] bm.gvt = #gt bm.rng',
                           'execute store result score @e[type=minecraft:marker,tag=bm.gvtrn,distance=..1] bm.gvy1 run random value 1..3',
                           'execute as @e[type=minecraft:marker,tag=bm.gvtrn,distance=..1] at @s run function bm:p116/trap/dress',
                           'tag @e[type=minecraft:marker,tag=bm.gvtrn] remove bm.gvtrn'])
    fn('p116/trap/dress', ['scoreboard players set @s bm.gvtm 0', 'scoreboard players set @s bm.gvx 0',
                           'execute if score @s bm.gvy1 matches 1 run function bm:p116/trap/d1', 'execute if score @s bm.gvy1 matches 2 run function bm:p116/trap/d2',
                           'execute if score @s bm.gvy1 matches 3 run function bm:p116/trap/d3'])
    fn('p116/trap/d1', [bd('minecraft:polished_blackstone', f'~-0.15 ~-0.02 ~{dz - 0.15}', (0.3, 0.06, 0.3), []) for dz in (-1, 0, 1)])
    fn('p116/trap/d2', [bd('minecraft:pointed_dripstone', f'~{dx - 0.35} ~-0.02 ~{dz - 0.35}', (0.7, 0.7, 0.7), ['bm.gvspk'], (0, -0.72, 0))
                        for dx in (-1, 0, 1) for dz in (-1, 0, 1)])
    fn('p116/trap/d3', [bd('minecraft:iron_bars', f'~-0.4 ~1.0 ~{dz}', (0.8, 0.4, 0.08), []) for dz in (-1.5, 1.42)])
    G.FUNCS['tick'].append('execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvtrap] at @s if entity @a[tag=bm.gvp,distance=..10] run function bm:p116/trap/tick')
    zone = 'positioned ~-1 ~ ~-1.5 as @a[tag=bm.gvp,dx=1,dy=1.5,dz=2]'
    fn('p116/trap/tick', ['scoreboard players add @s bm.gvtm 1',
                          'execute if score @s bm.gvy1 matches 1 run function bm:p116/trap/flame', 'execute if score @s bm.gvy1 matches 2 run function bm:p116/trap/spike',
                          'execute if score @s bm.gvy1 matches 3 run function bm:p116/trap/arrow'])
    dmg = lambda n, kind: [f'execute if score @s bm.gvt matches ..2 {zone} run damage @s {n} minecraft:{kind}', f'execute if score @s bm.gvt matches 3.. {zone} run damage @s {n + 2} minecraft:{kind}']
    fn('p116/trap/flame', ['execute if score @s bm.gvtm matches 60.. run scoreboard players set @s bm.gvtm 0',
                           'execute if score @s bm.gvtm matches 35..44 run particle minecraft:smoke ~ ~0.2 ~ 0.1 0.1 1 0.01 3',
                           'execute if score @s bm.gvtm matches 45 run playsound minecraft:item.firecharge.use block @a[distance=..12] ~ ~ ~ 1 0.7',
                           'execute if score @s bm.gvtm matches 45..59 run particle minecraft:flame ~ ~0.8 ~ 0.15 0.6 1.1 0.02 18',
                           'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #5 bm.rng'] +
       [f'execute if score @s bm.gvtm matches 45..59 if score #q bm.rng matches 0 {l[8:]}' for l in dmg(2, 'in_fire')])
    fn('p116/trap/spike', ['execute if score @s bm.gvtm matches 50.. run scoreboard players set @s bm.gvtm 0',
                           'execute if score @s bm.gvtm matches 30 run playsound minecraft:block.pointed_dripstone.land block @a[distance=..12] ~ ~ ~ 1 0.6',
                           'execute if score @s bm.gvtm matches 30..34 run particle minecraft:block{block_state:"minecraft:dripstone_block"} ~ ~0.1 ~ 1 0 1 0 4',
                           'execute if score @s bm.gvtm matches 35 as @e[type=minecraft:block_display,tag=bm.gvspk,distance=..2.5] run data merge entity @s {start_interpolation:0,transformation:{translation:[0f,0f,0f]}}',
                           'execute if score @s bm.gvtm matches 49 as @e[type=minecraft:block_display,tag=bm.gvspk,distance=..2.5] run data merge entity @s {start_interpolation:0,transformation:{translation:[0f,-0.72f,0f]}}',
                           'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #5 bm.rng'] +
       [f'execute if score @s bm.gvtm matches 36..48 if score #q bm.rng matches 0 {l[8:]}' for l in dmg(2, 'cactus')])
    fn('p116/trap/arrow', ['execute if score @s bm.gvx matches 1.. run scoreboard players remove @s bm.gvx 1',
                           'execute if score @s bm.gvx matches 0 positioned ~-1 ~ ~-1.5 if entity @a[tag=bm.gvp,dx=1,dy=1.5,dz=2] positioned ~1 ~ ~1.5 run function bm:p116/trap/arm',
                           'execute if score @s bm.gvx matches 52 run function bm:p116/trap/fire'])
    fn('p116/trap/arm', ['scoreboard players set @s bm.gvx 60', 'playsound minecraft:block.tripwire.click_on block @a[distance=..12] ~ ~ ~ 1 1.2'])
    fn('p116/trap/fire', ['playsound minecraft:entity.arrow.shoot block @a[distance=..12] ~ ~ ~ 1 0.9'] +
       [f'summon minecraft:arrow ~{dx} ~1.2 ~-1.4 {{Motion:[0.0d,0.0d,1.6d],pickup:0b,damage:2.0d,Tags:["bm.gvtar"]}}' for dx in (-0.6, 0.6)] +
       [f'summon minecraft:arrow ~{dx} ~1.2 ~1.4 {{Motion:[0.0d,0.0d,-1.6d],pickup:0b,damage:2.0d,Tags:["bm.gvtar"]}}' for dx in (0.0,)])
    G.FUNCS['tick'].append('kill @e[type=minecraft:arrow,tag=bm.gvtar,nbt={inGround:1b}]')

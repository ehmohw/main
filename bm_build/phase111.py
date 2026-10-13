"""2.69: THREE WAYS THROUGH EVERY PUZZLE (II).

THE DIAL LOCK          A  the blueprint's arrows (as before)
                       B  THE NUMBERED DIALS: each dial points at a number (0 at the top, round clockwise); three or four
                          sums ("Left + middle = 9", "Right is odd") fix the one setting
                       C  THE GEARED DIALS: the blueprint's arrows again - but the dials are geared together: turning
                          the right one turns all three, the middle turns itself and the left, the left turns itself and
                          the right. Work out the turns
THE THREE COFFERS      A  the riddle of places (as before)
                       B  THE LYING COFFERS: each coffer says where the honest one is - and exactly one of them is telling
                          the truth
                       C  THE SHELL GAME: the gold goes into one of four plain chests; they shuffle (faster and longer on
                          the higher tiers) - open the one it's in. A wrong pick lets a Mimic out and they shuffle again
THE SIGNAL LAMPS       A  repeat the sequence (as before)
                       B  BACKWARDS: press it last flash first
                       C  THE CIPHER: the wall says what each colour really means (RED means BLUE...) - press what the
                          flashes mean, not what they show
THE LAMP FLOOR         A  each button flips its lamp and the four beside it (as before)
                       B  each button flips its lamp and the four at its corners
                       C  each button flips its lamp and every lamp in its row and column
THE TUMBLER LOCK       A  catch the running light on the gold gate (as before)
                       B  THE WANDERING GATE: the gate is the lamp marked green - and the mark moves after every hit
                       C  THE BLIND TUMBLER: the light runs once where you can see it, then only ticks in the dark (a
                          deeper knock at each end) - count your way to the gate
THE BELL TOWER         A  the spiral of broad steps (as before)
                       B  THE SOUTH STAIR: single posts up the south and east walls - one-block landings, longer jumps
                       C  THE FALLING STAIR: the steps run up the south side and give way a moment after you land
                          (back a few seconds later) - keep moving
THE CRUMBLING RAFTERS  A  beams that fall once stood on (as before)
                       B  THE BLINKING BEAMS: beams that wink out and back in a travelling wave (they flicker first)
                       C  THE GHOST BEAMS: a winding path of beams nobody can see - they shimmer only when you're right
                          beside them
"""
import itertools
import math
from items import T
from nbt import snbt, B, F, Int
import phase70_rooms as RM
import phase75_rooms as R5
import phase76_rooms as R6
import phase110 as P110
import p110data as PD

GOLD = '#ffcf40'
rel, relf, IDENT = RM.rel, P110.relf, P110.IDENT
CC = {'red': '#ff5050', 'blue': '#5a8aff', 'lime': '#7dff6a', 'yellow': '#ffe050'}


def generate(G):
    fn, title = G.fn, G.title
    label, sign, vbutton, press, themed, crew_say, oops, choose = P110.helpers(G)
    dispatch = lambda k, b, c: P110.dispatch(G, k, b, c)
    objs = ['bm.gvya', 'bm.gvyb']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    copy = lambda f: list(G.FUNCS[f])

    # ================================================================== THE DIAL LOCK
    DX = [10, 12, 14]                            # (dial 0 is on the right as you face them)
    dinit, dtick = copy('p70/r/dial/init'), copy('p70/r/dial/tick')
    frames = [l for l in dinit if 'summon minecraft:item_frame' in l]
    try_btn = vbutton(16, 5, 22, 'north', 'TRY THE DIALS')
    # ---- B: the numbered dials
    DP = PD.dial_puzzles()
    ring = []
    for x in DX:
        for k in range(8):
            th = math.radians(45 * k)
            ring.append(label(relf(x + 0.5 - 0.66 * math.sin(th), 6.43 + 0.66 * math.cos(th), 22.88), T(str(k), GOLD, bold=True), 0.34, 'fixed', yaw=180, bg=False))
    fn('p111/dial/b/init', ['function bm:p70/ctx'] + frames + ring + choose('#i', len(DP), 'p111/dial/b/p') + try_btn)
    for j, (v, clues) in enumerate(DP):
        r = [(v[2] + 7) % 8, (v[1] + 7) % 8, (v[0] + 7) % 8]          # (dial 0 right, 1 middle, 2 left; a value sits one turn past the frame's 0)
        fn(f'p111/dial/b/p{j}', [f'scoreboard players set @s bm.gvc {r[0] + 8 * r[1] + 64 * r[2]}',
                                 label(relf(12.5, 7.9, 22.88), [T('THE NUMBERED DIALS\n', GOLD, bold=True),
                                                                T('Each dial points at a number - 0 at the top, counting round clockwise.\n', 'gray'),
                                                                T('\n'.join(clues), 'white')], 0.55, 'fixed', yaw=180, width=300, tags=('bm.gvboard',))])
    # ---- C: the geared dials (right: all three; middle: middle + left; left: left + right)
    fn('p111/dial/c/init', dinit + ['scoreboard players set @s bm.gvy1 0', 'scoreboard players set @s bm.gvy2 0', 'scoreboard players set @s bm.gvy3 0',
                                    label(relf(12.5, 3.75, 22.88), [T('GEARED: ', GOLD, bold=True), T('turning a dial turns others too.', 'gray')], 0.5, 'fixed', yaw=180)])
    get = lambda i: f'execute store result score #c{i} bm.rng run data get entity @e[type=minecraft:item_frame,tag=bm.gvdial{i},distance=..14,limit=1] ItemRotation'
    put = lambda i: f'execute store result entity @e[type=minecraft:item_frame,tag=bm.gvdial{i},distance=..14,limit=1] ItemRotation byte 1 run scoreboard players get #n{i} bm.rng'
    prev = ['bm.gvy1', 'bm.gvy2', 'bm.gvy3']
    fn('p111/dial/c/gears', [get(i) for i in range(3)] +
       sum(([f'scoreboard players operation #d{i} bm.rng = #c{i} bm.rng', f'scoreboard players operation #d{i} bm.rng -= @s {prev[i]}',
             f'scoreboard players add #d{i} bm.rng 8', f'scoreboard players operation #d{i} bm.rng %= #8 bm.rng'] for i in range(3)), []) +
       ['execute if score #d0 bm.rng matches 0 if score #d1 bm.rng matches 0 if score #d2 bm.rng matches 0 run return 0',
        'scoreboard players operation #n0 bm.rng = #c0 bm.rng', 'scoreboard players operation #n0 bm.rng += #d2 bm.rng',
        'scoreboard players operation #n1 bm.rng = #c1 bm.rng', 'scoreboard players operation #n1 bm.rng += #d0 bm.rng',
        'scoreboard players operation #n2 bm.rng = #c2 bm.rng', 'scoreboard players operation #n2 bm.rng += #d0 bm.rng', 'scoreboard players operation #n2 bm.rng += #d1 bm.rng'] +
       sum(([f'scoreboard players operation #n{i} bm.rng %= #8 bm.rng', put(i), f'scoreboard players operation @s {prev[i]} = #n{i} bm.rng'] for i in range(3)), []) +
       ['playsound minecraft:block.chain.place block @a[distance=..16] ~ ~2 ~10 0.8 0.8'])
    fn('p111/dial/c/tick', ['execute if score @s bm.gvs matches 0..2 run function bm:p111/dial/c/gears'] + dtick)
    dispatch('dial', ('p111/dial/b/init', None), ('p111/dial/c/init', 'p111/dial/c/tick'))

    # ================================================================== THE THREE COFFERS
    CZ = [6, 10, 14, 18]
    KI = ['minecraft:chest', 'minecraft:copper_chest', 'minecraft:ender_chest', 'minecraft:barrel']
    inter = lambda tag: [f'summon minecraft:interaction {rel(19, 5, z)} {{Tags:["bm.gvprop","{tag}","{tag}{i}"],width:1.0f,height:1.0f,response:1b}}' for i, z in enumerate(CZ)]
    chest = lambda i, z, item, tags, td=0: f'summon minecraft:item_display {rel(19, 5, z)} ' + snbt({'Tags': ['bm.gvprop'] + tags, 'item': {'id': item, 'count': Int(1)}, 'item_display': 'fixed', 'teleport_duration': Int(td),
                                                                                         'Rotation': [F(90), F(0)], 'transformation': {'left_rotation': IDENT, 'right_rotation': IDENT,
                                                                                                                                      'translation': [F(0), F(0.5), F(0)], 'scale': [F(0.9)] * 3}})
    # ---- B: the lying coffers (exactly one tells the truth)
    LP = PD.liar_puzzles()
    fn('p111/coffers/b/init', ['function bm:p70/ctx'] + inter('bm.gvcof') + choose('#i', len(LP), 'p111/coffers/b/p') +
       [sign(rel(5, 7, 22), 'THE LYING COFFERS', 'Each coffer says where the honest one is. Exactly one of them is telling the truth. '
             'The honest coffer opens the way; the rest bite.', 0.6)])
    for j, pz in enumerate(LP):
        L = [f'scoreboard players set @s bm.gvc {pz["h"]}']
        for i, z in enumerate(CZ):
            L.append(chest(i, z, KI[pz['perm'][i]], [f'bm.gvcofd{i}']))
            L.append(label(relf(18.3, 6.35, z + 0.5), [T(PD.CKINDS[pz['perm'][i]].upper() + ':\n', GOLD, bold=True), T(f'"{pz["say"][i]}"', 'white')], 0.42, 'fixed', yaw=90, width=110))
        fn(f'p111/coffers/b/p{j}', L)
    # ---- C: the shell game
    tiers = range(1, 6)
    LEG = {1: 10, 2: 9, 3: 8, 4: 7, 5: 6}
    SWAPS = {1: 5, 2: 6, 3: 7, 4: 8, 5: 10}
    fn('p111/coffers/c/init', ['function bm:p70/ctx'] + inter('bm.gvshi') +
       [f'execute if score #gt bm.rng matches {t} run ' + chest(i, z, 'minecraft:chest', [f'bm.gvsd{i}', 'bm.gvsd'], LEG[t]) for t in tiers for i, z in enumerate(CZ)] +
       [f'execute if score #gt bm.rng matches {t} run scoreboard players set @s bm.gvy1 {LEG[t]}' for t in tiers] +
       [sign(rel(5, 7, 22), 'THE SHELL GAME', 'The gold goes into one chest, and they shuffle. Keep your eye on it - then open that one. The rest bite.', 0.6)])
    mimic = [l for l in G.FUNCS['p70/r/coffers/mimic0'] if not l.startswith('kill ')]
    fn('p111/coffers/c/tick', ['execute if score @s bm.gvs matches 3 run return 0',
                               'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..9] run function bm:p111/coffers/c/round',
                               'execute unless score @s bm.gvs matches 2 as @e[type=minecraft:interaction,tag=bm.gvshi,distance=..14] if data entity @s interaction run data remove entity @s interaction',
                               'execute if score @s bm.gvs matches 1 run function bm:p111/coffers/c/show',
                               'execute if score @s bm.gvs matches 2 as @e[type=minecraft:interaction,tag=bm.gvshi,distance=..14] if data entity @s interaction at @s run function bm:p111/coffers/c/pick'])
    fn('p111/coffers/c/round', ['scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvx 0', 'scoreboard players set @s bm.gvy3 0',
                                'execute store result score @s bm.gvc run random value 0..3'] +
       [f'execute if score @s bm.gvt matches {t} run scoreboard players set @s bm.gvy2 {SWAPS[t]}' for t in tiers] +
       [f'execute if score @s bm.gvc matches {i} run summon minecraft:item_display {relf(19.5, 6.6, z + 0.5)} {{Tags:["bm.gvprop","bm.gvgold"],billboard:"vertical",item:{{id:"minecraft:gold_block",count:1}},'
        f'transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.5f,0.5f,0.5f]}}}}' for i, z in enumerate(CZ)] +
       ['playsound minecraft:block.chest.open block @a[distance=..24] ~7 ~ ~ 1 1.2', crew_say('Watch the gold...', GOLD, 24)])
    fn('p111/coffers/c/show', ['scoreboard players add @s bm.gvx 1',
                               'execute if score @s bm.gvx matches 34 run kill @e[type=minecraft:item_display,tag=bm.gvgold,distance=..14]',
                               'execute if score @s bm.gvx matches 34 run playsound minecraft:block.chest.close block @a[distance=..24] ~7 ~ ~ 1 1',
                               'execute if score @s bm.gvx matches ..44 run return 0',
                               'execute if score @s bm.gvy3 matches 0 if score @s bm.gvy2 matches ..0 run return run function bm:p111/coffers/c/ready',
                               'execute if score @s bm.gvy3 matches 0 run function bm:p111/coffers/c/swap',
                               'scoreboard players add @s bm.gvy3 1',
                               'execute if score @s bm.gvy3 = @s bm.gvy1 run function bm:p111/coffers/c/leg2',
                               'scoreboard players operation #l2 bm.rng = @s bm.gvy1', 'scoreboard players operation #l2 bm.rng *= #2 bm.rng',
                               'execute if score @s bm.gvy3 >= #l2 bm.rng run function bm:p111/coffers/c/done'])
    pairs = [(a, b) for a in range(4) for b in range(4) if a != b]
    fn('p111/coffers/c/swap', ['execute store result score @s bm.gvya run random value 0..3', 'execute store result score #k bm.rng run random value 1..3',
                               'scoreboard players operation @s bm.gvyb = @s bm.gvya', 'scoreboard players operation @s bm.gvyb += #k bm.rng',
                               'scoreboard players operation @s bm.gvyb %= #4 bm.rng'] +
       [f'execute if score @s bm.gvya matches {a} if score @s bm.gvyb matches {b} run return run function bm:p111/coffers/c/l1_{a}{b}' for a, b in pairs])
    fn('p111/coffers/c/leg2', [f'execute if score @s bm.gvya matches {a} if score @s bm.gvyb matches {b} run return run function bm:p111/coffers/c/l2_{a}{b}' for a, b in pairs])
    fn('p111/coffers/c/done', ['scoreboard players set @s bm.gvy3 0', 'scoreboard players remove @s bm.gvy2 1'] +
       [f'execute if score @s bm.gvya matches {a} if score @s bm.gvyb matches {b} run return run function bm:p111/coffers/c/end_{a}{b}' for a, b in pairs])
    for a, b in pairs:
        za, zb = CZ[a] + 0.5, CZ[b] + 0.5; mid = (za + zb) / 2
        fn(f'p111/coffers/c/l1_{a}{b}', [f'tag @e[type=minecraft:item_display,tag=bm.gvsd{a},distance=..14] add bm.gvsa', f'tag @e[type=minecraft:item_display,tag=bm.gvsd{b},distance=..14] add bm.gvsb',
                                         f'tp @e[type=minecraft:item_display,tag=bm.gvsa,distance=..14] {relf(17.3, 5, mid)}', f'tp @e[type=minecraft:item_display,tag=bm.gvsb,distance=..14] {relf(21.7, 5, mid)}',
                                         'playsound minecraft:block.wood.hit block @a[distance=..20] ~7 ~ ~ 0.6 1.3'])
        fn(f'p111/coffers/c/l2_{a}{b}', [f'tp @e[type=minecraft:item_display,tag=bm.gvsa,distance=..14] {relf(19.5, 5, zb)}', f'tp @e[type=minecraft:item_display,tag=bm.gvsb,distance=..14] {relf(19.5, 5, za)}'])
        fn(f'p111/coffers/c/end_{a}{b}', [f'tag @e[type=minecraft:item_display,tag=bm.gvsa,distance=..14] remove bm.gvsd{a}', f'tag @e[type=minecraft:item_display,tag=bm.gvsb,distance=..14] remove bm.gvsd{b}',
                                          f'tag @e[type=minecraft:item_display,tag=bm.gvsa,distance=..14] add bm.gvsd{b}', f'tag @e[type=minecraft:item_display,tag=bm.gvsb,distance=..14] add bm.gvsd{a}',
                                          'tag @e[type=minecraft:item_display,distance=..14] remove bm.gvsa', 'tag @e[type=minecraft:item_display,distance=..14] remove bm.gvsb',
                                          f'execute if score @s bm.gvc matches {a} run return run scoreboard players set @s bm.gvc {b}',
                                          f'execute if score @s bm.gvc matches {b} run scoreboard players set @s bm.gvc {a}'])
    fn('p111/coffers/c/ready', ['scoreboard players set @s bm.gvs 2', crew_say('Which one has the gold? Open it.', GOLD, 24)])
    fn('p111/coffers/c/pick', ['data remove entity @s interaction'] + [f'execute if entity @s[tag=bm.gvshi{i}] run scoreboard players set #pick bm.rng {i}' for i in range(4)] +
       ['execute as @e[type=minecraft:marker,tag=bm.gvr_coffers,distance=..14,sort=nearest,limit=1] at @s run function bm:p111/coffers/c/judge'])
    fn('p111/coffers/c/judge', ['execute if score #pick bm.rng = @s bm.gvc run return run function bm:p70/r/coffers/right'] + oops(12) +
       [f'execute if score #pick bm.rng matches {i} positioned {rel(19, 5, z)} run function bm:p111/coffers/c/bite' for i, z in enumerate(CZ)] +
       ['function bm:p111/coffers/c/round'])
    fn('p111/coffers/c/bite', mimic[:-1] + ['execute as @a[tag=bm.gvp,distance=..20] run ' + title('@s', 'actionbar', T('A Mimic! And they shuffle again...', 'red'))])
    dispatch('coffers', ('p111/coffers/b/init', None), ('p111/coffers/c/init', 'p111/coffers/c/tick'))

    # ================================================================== THE SIGNAL LAMPS
    linit, ltick, linp = copy('p76/r/lamps/init'), copy('p76/r/lamps/tick'), copy('p76/r/lamps/input')
    LX = R6.LAMPS_X
    nosign = [l for l in linit if 'THE SIGNAL LAMPS' not in l]
    DER = [p for p in itertools.permutations(range(4)) if all(p[i] != i for i in range(4))]
    fn('p111/lamps/b/init', nosign + [sign(rel(12, 10.4, 1.5), 'BACKWARDS', 'Watch the lamps flash - then press their buttons in the opposite order: last flash first.')])
    fn('p111/lamps/c/init', nosign + choose('#i', len(DER), 'p111/lamps/c/k'))
    for d, p in enumerate(DER):
        body = []
        for a in range(4):
            body += [T(PD.COLS[a].upper(), CC[PD.COLS[a]], bold=True), T(' means ', 'gray'), T(PD.COLS[p[a]].upper(), CC[PD.COLS[p[a]]], bold=True), T('\n' if a < 3 else '', 'gray')]
        fn(f'p111/lamps/c/k{d}', [f'scoreboard players set @s bm.gvy1 {d}',
                                  label(rel(12, 10.4, 1.5), [T('THE CIPHER\n', GOLD, bold=True), T('Watch the lamps, then press what each flash MEANS:\n', 'gray')] + body, 0.6, 'vertical')])
    for v in 'bc':
        fn(f'p111/lamps/{v}/tick', [l.replace('bm:p76/r/lamps/input', f'bm:p111/lamps/{v}/input') for l in ltick])
        fn(f'p111/lamps/{v}/input', [l.replace('bm:p76/r/lamps/press', f'bm:p111/lamps/{v}/press') for l in linp])
    snd = lambda j: f'playsound minecraft:block.note_block.bell block @a[distance=..24] {rel(LX[j], 7, 1)} 1 {[0.7, 0.9, 1.1, 1.35][j]}'
    for j in range(4):
        digit = ['scoreboard players operation #q bm.rng = @s bm.gvc'] + [f'execute if score #k bm.rng matches {i} run scoreboard players operation #q bm.rng /= #pw{i} bm.rng' for i in range(8)] + \
                ['scoreboard players operation #q bm.rng %= #4 bm.rng']
        fn(f'p111/lamps/b/press{j}', ['scoreboard players operation #k bm.rng = @s bm.gvx', 'scoreboard players operation #k bm.rng -= @s bm.gvw', 'scoreboard players remove #k bm.rng 1'] +
           digit + [snd(j), f'execute unless score #q bm.rng matches {j} run return run function bm:p76/r/lamps/wrong',
                    'scoreboard players add @s bm.gvw 1', 'execute if score @s bm.gvw >= @s bm.gvx run function bm:p70/solved'])
        fn(f'p111/lamps/c/press{j}', ['scoreboard players operation #k bm.rng = @s bm.gvw'] + digit +
           [f'execute if score @s bm.gvy1 matches {d} if score #q bm.rng matches {a} run scoreboard players set #q2 bm.rng {p[a]}' for d, p in enumerate(DER) for a in range(4)] +
           [snd(j), f'execute unless score #q2 bm.rng matches {j} run return run function bm:p76/r/lamps/wrong',
            'scoreboard players add @s bm.gvw 1', 'execute if score @s bm.gvw >= @s bm.gvx run function bm:p70/solved'])
    G.FUNCS['p76/r/lamps/your_turn'][0:0] = [
        'execute if score @s bm.gvvar matches 1 run ' + crew_say('Your turn - press them backwards, last flash first.', GOLD, 20),
        'execute if score @s bm.gvvar matches 2 run ' + crew_say('Your turn - press what each flash means (see the wall).', GOLD, 20),
        'execute if score @s bm.gvvar matches 1..2 run scoreboard players set @s bm.gvw 0',
        'execute if score @s bm.gvvar matches 1..2 run return run scoreboard players set @s bm.gvs 2']
    dispatch('lamps', ('p111/lamps/b/init', 'p111/lamps/b/tick'), ('p111/lamps/c/init', 'p111/lamps/c/tick'))

    # ================================================================== THE LAMP FLOOR
    oinit, otick = copy('p76/r/lightsout/init'), copy('p76/r/lightsout/tick')
    PAT = {'b': lambda i, j: {(i, j)} | {(i + a, j + c) for a in (-1, 1) for c in (-1, 1) if 0 <= i + a < 3 and 0 <= j + c < 3},
           'c': lambda i, j: {(a, j) for a in range(3)} | {(i, c) for c in range(3)}}
    TXT = {'b': 'Each button flips its lamp - and the lamps at its corners. Light them all.', 'c': 'Each button flips its lamp - and every lamp in its row and column. Light them all.'}
    for v in 'bc':
        for b_ in range(9):
            i, j = b_ % 3, b_ // 3
            fn(f'p111/lightsout/{v}/p{b_}', [f'function bm:p76/r/lightsout/t{a + 3 * c}' for a, c in sorted(PAT[v](i, j))])
            fn(f'p111/lightsout/{v}/push{b_}', [f'function bm:p111/lightsout/{v}/p{b_}', 'function bm:p76/r/lightsout/draw',
                                                 'playsound minecraft:block.stone_button.click_on block @a[distance=..20] ~ ~ ~ 1 1.4',
                                                 'execute if score @s bm.gvc matches 511 run function bm:p70/solved'])
        fn(f'p111/lightsout/{v}/scramble', ['execute if score #k bm.rng matches ..0 run return 0', 'execute store result score #b bm.rng run random value 0..8'] +
           [f'execute if score #b bm.rng matches {b_} run function bm:p111/lightsout/{v}/p{b_}' for b_ in range(9)] +
           ['scoreboard players remove #k bm.rng 1', f'function bm:p111/lightsout/{v}/scramble'])
        L = []
        for l in oinit:
            if 'THE LAMP FLOOR' in l: L.append(sign(rel(6, 7.5, 12), 'THE LAMP FLOOR', TXT[v])); continue
            L.append(l.replace('bm:p76/r/lightsout/scramble', f'bm:p111/lightsout/{v}/scramble').replace('bm:p76/r/lightsout/p4', f'bm:p111/lightsout/{v}/p4'))
        fn(f'p111/lightsout/{v}/init', L)
        fn(f'p111/lightsout/{v}/tick', [l.replace('bm:p76/r/lightsout/push', f'bm:p111/lightsout/{v}/push') for l in otick])
    dispatch('lightsout', ('p111/lightsout/b/init', 'p111/lightsout/b/tick'), ('p111/lightsout/c/init', 'p111/lightsout/c/tick'))

    # ================================================================== THE TUMBLER LOCK
    tinit, ttick, tstep = copy('p76/r/tumbler/init'), copy('p76/r/tumbler/tick'), copy('p76/r/tumbler/step')
    TX = R6.TUMB_X; gx = TX[4]
    tnos = [l for l in tinit if 'THE TUMBLER LOCK' not in l]
    # ---- B: the wandering gate
    fn('p111/tumbler/b/init', tnos + themed(f'fill {rel(gx - 1, 5, 0)} {rel(gx + 1, 9, 0)} {{b}}', 'wall') +
       [f'fill {rel(gx - 1, 7, 0)} {rel(gx + 1, 7, 0)} minecraft:redstone_lamp[lit=false]'] +
       themed(f'fill {rel(gx - 1, 6, 0)} {rel(gx + 1, 6, 0)} {{b}}', 'trim') + themed(f'fill {rel(gx - 1, 8, 0)} {rel(gx + 1, 8, 0)} {{b}}', 'trim') +
       ['execute store result score @s bm.gvy1 run random value 1..7', 'function bm:p111/tumbler/b/mark',
        sign(rel(12, 10.6, 1.5), 'THE WANDERING GATE', 'Press as the light crosses the lamp marked green - three times running. The mark moves after every hit.')])
    fn('p111/tumbler/b/mark', [f'execute if score @s bm.gvy1 matches {g} run fill {rel(TX[g], 6, 0)} {rel(TX[g], 8, 0)} minecraft:emerald_block' for g in range(1, 8)] +
       [f'execute if score @s bm.gvy1 matches {g} run setblock {rel(TX[g], 7, 0)} minecraft:redstone_lamp[lit=false]' for g in range(1, 8)])
    fn('p111/tumbler/b/unmark', [f'execute if score @s bm.gvy1 matches {g} run function bm:p111/tumbler/b/un{g}' for g in range(1, 8)])
    for g in range(1, 8):
        fn(f'p111/tumbler/b/un{g}', themed(f'setblock {rel(TX[g], 6, 0)} {{b}}', 'trim') + themed(f'setblock {rel(TX[g], 8, 0)} {{b}}', 'trim'))
    fn('p111/tumbler/b/tick', [l.replace('bm:p76/r/tumbler/try', 'bm:p111/tumbler/b/try') for l in ttick])
    fn('p111/tumbler/b/try', ['scoreboard players operation #L bm.rng = @s bm.gvc', 'execute if score @s bm.gvc matches 9.. run scoreboard players set #L bm.rng 16',
                              'execute if score @s bm.gvc matches 9.. run scoreboard players operation #L bm.rng -= @s bm.gvc',
                              'execute unless score #L bm.rng = @s bm.gvy1 run return run function bm:p76/r/tumbler/miss',
                              'scoreboard players add @s bm.gvw 1', 'playsound minecraft:block.iron_trapdoor.open block @a[distance=..20] ~ ~ ~ 1 1.5',
                              crew_say([T('Click! ', GOLD, bold=True), {'score': {'name': '@e[type=marker,tag=bm.gvr_tumbler,limit=1,sort=nearest]', 'objective': 'bm.gvw'}, 'color': 'white'},
                                        T(' of 3 - the gate moves!', 'gray')], r=20),
                              'execute if score @s bm.gvw matches 3.. run return run function bm:p70/solved',
                              'function bm:p111/tumbler/b/unmark', 'execute store result score #g bm.rng run random value 1..6',
                              'execute if score #g bm.rng >= @s bm.gvy1 run scoreboard players add #g bm.rng 1', 'scoreboard players operation @s bm.gvy1 = #g bm.rng',
                              'function bm:p111/tumbler/b/mark'])
    # ---- C: the blind tumbler
    fn('p111/tumbler/c/init', tnos + ['scoreboard players set @s bm.gvy2 17',
                                      sign(rel(12, 10.6, 1.5), 'THE BLIND TUMBLER', 'The light runs once where you can see it - then only ticks in the dark (a deeper knock at each end). '
                                           'Press as it crosses the gold gate, three times running.')])
    fn('p111/tumbler/c/tick', ['execute if score @s bm.gvs matches 3 run return 0',
                               'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..12] run scoreboard players set @s bm.gvs 1',
                               'execute if score @s bm.gvs matches 0 run return 0',
                               'scoreboard players set #sp bm.rng 8', 'execute if score @s bm.gvw matches 1 run scoreboard players set #sp bm.rng 7',
                               'execute if score @s bm.gvw matches 2.. run scoreboard players set #sp bm.rng 6', 'execute if score @s bm.gvt matches 4.. run scoreboard players remove #sp bm.rng 1',
                               'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #sp bm.rng',
                               'execute if score #q bm.rng matches 0 run function bm:p111/tumbler/c/step'] + press('tumb', (12, 5, 2), 'bm:p111/tumbler/c/try'))
    lights = [l for l in tstep if l.startswith('execute if score @s bm.gvc matches') and 'redstone_lamp[lit=true]' in l]
    fn('p111/tumbler/c/step', [l for l in tstep if 'redstone_lamp[lit=true]' not in l] + ['execute if score @s bm.gvy2 matches 1.. run function bm:p111/tumbler/c/lit',
                                                                                        'execute if score @s bm.gvy2 matches 1.. run scoreboard players remove @s bm.gvy2 1',
                                                                                        'execute if score @s bm.gvc matches 0 run playsound minecraft:block.note_block.basedrum block @a[distance=..20] ~ ~3 ~-11 1 0.7',
                                                                                        'execute if score @s bm.gvc matches 8 run playsound minecraft:block.note_block.basedrum block @a[distance=..20] ~ ~3 ~-11 1 0.7',
                                                                                        'execute unless score @s bm.gvc matches 0 unless score @s bm.gvc matches 8 run playsound minecraft:block.note_block.hat block @a[distance=..20] ~ ~3 ~-11 0.8 1.6'])
    fn('p111/tumbler/c/lit', lights)
    fn('p111/tumbler/c/try', ['execute unless score @s bm.gvc matches 4 unless score @s bm.gvc matches 12 run return run function bm:p111/tumbler/c/miss',
                              'scoreboard players add @s bm.gvw 1', 'scoreboard players set @s bm.gvy2 17', 'playsound minecraft:block.iron_trapdoor.open block @a[distance=..20] ~ ~ ~ 1 1.5',
                              crew_say([T('Click! ', GOLD, bold=True), {'score': {'name': '@e[type=marker,tag=bm.gvr_tumbler,limit=1,sort=nearest]', 'objective': 'bm.gvw'}, 'color': 'white'},
                                        T(' of 3 - watch it once more...', 'gray')], r=20),
                              'execute if score @s bm.gvw matches 3.. run function bm:p70/solved'])
    fn('p111/tumbler/c/miss', ['function bm:p76/r/tumbler/miss', 'scoreboard players set @s bm.gvy2 17'])
    dispatch('tumbler', ('p111/tumbler/b/init', 'p111/tumbler/b/tick'), ('p111/tumbler/c/init', 'p111/tumbler/c/tick'))

    # ================================================================== THE BELL TOWER
    APATH = [(3, 7), (3, 4), (6, 3), (9, 3), (12, 3), (15, 3), (18, 3), (21, 4), (21, 7)]
    ctick = copy('p76/r/climb/tick'); cinit = copy('p76/r/climb/init')
    clear_a = sum(([f'fill {rel(x, 4 + k, z)} {rel(x + 1, 4 + k, z + 1)} minecraft:air', f'setblock {rel(x, 3 + k, z)} minecraft:air'] for k, (x, z) in enumerate(APATH)), [])
    # ---- B: the south stair (single posts)
    POSTS = [(3, 20, 4), (5, 21, 5), (7, 20, 6), (9, 21, 7), (12, 21, 7), (14, 20, 8), (16, 21, 9), (18, 20, 10), (21, 21, 10), (21, 19, 11), (21, 17, 12)]
    fn('p111/climb/b/init', ['function bm:p70/ctx'] + clear_a +
       sum((themed(f'setblock {rel(x, t, z)} {{b}}', 'trim') + themed(f'setblock {rel(x, t - 1, z)} {{b}}', 'chain') for x, z, t in POSTS), []) +
       [l.replace('The way on is at the top. Mind the drop.', 'Single posts this time - up the south wall and round. Mind the drop.') for l in cinit if 'function bm:p70/ctx' not in l])
    # ---- C: the falling stair (A's steps, mirrored to the south side; each gives way a moment after you land)
    CPATH = [(x, 23 - z) for x, z in APATH]
    fn('p111/climb/c/init', ['function bm:p70/ctx', 'scoreboard players operation @s bm.gvy3 = #gsf bm.rng'] + clear_a +
       sum((themed(f'fill {rel(x, 4 + k, z)} {rel(x + 1, 4 + k, z + 1)} {{b}}', 'trim' if k % 2 else 'floor') +
            [f'summon minecraft:marker {relf(x + 1, 5 + k, z + 1)} {{Tags:["bm.gvprop","bm.gvcs"' + (',"bm.gvodd"' if k % 2 else '') + ']}'] for k, (x, z) in enumerate(CPATH)), []) +
       ['execute as @e[type=minecraft:marker,tag=bm.gvcs,distance=..30] run scoreboard players set @s bm.gvx 0'] +
       [l.replace('The way on is at the top. Mind the drop.', 'These steps give way a moment after you land - keep moving.') for l in cinit if 'function bm:p70/ctx' not in l])
    fn('p111/climb/c/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'scoreboard players operation #gt bm.rng = @s bm.gvt', 'scoreboard players operation #gsf bm.rng = @s bm.gvy3',
                             'execute as @e[type=minecraft:marker,tag=bm.gvcs,distance=..30] at @s run function bm:p111/climb/c/step'] + ctick)
    fn('p111/climb/c/step', ['execute if score @s bm.gvx matches 0 if entity @a[tag=bm.gvp,distance=..1.5] run function bm:p111/climb/c/creak',
                             'execute if score @s bm.gvx matches 2.. run scoreboard players remove @s bm.gvx 1',
                             'execute if score @s bm.gvx matches 1 run function bm:p111/climb/c/fall',
                             'execute if score @s bm.gvx matches ..-2 run scoreboard players add @s bm.gvx 1',
                             'execute if score @s bm.gvx matches -1 run function bm:p111/climb/c/back'])
    fn('p111/climb/c/creak', ['scoreboard players set @s bm.gvx 24', 'execute if score #gt bm.rng matches 4.. run scoreboard players set @s bm.gvx 16',
                              'playsound minecraft:block.stone.hit block @a[distance=..16] ~ ~ ~ 0.8 0.6', 'particle minecraft:block{block_state:"minecraft:gravel"} ~ ~-0.1 ~ 0.6 0.1 0.6 0 10'])
    fn('p111/climb/c/fall', ['fill ~-1 ~-1 ~-1 ~ ~-1 ~ minecraft:air', 'scoreboard players set @s bm.gvx -70', 'playsound minecraft:block.stone.break block @a[distance=..16] ~ ~ ~ 1 0.6'])
    fn('p111/climb/c/back', ['scoreboard players set @s bm.gvx 0', 'execute if entity @s[tag=bm.gvodd] run return run function bm:p111/climb/c/back_t'] +
       themed('fill ~-1 ~-1 ~-1 ~ ~-1 ~ {b}', 'floor'))
    fn('p111/climb/c/back_t', themed('fill ~-1 ~-1 ~-1 ~ ~-1 ~ {b}', 'trim'))
    dispatch('climb', ('p111/climb/b/init', None), ('p111/climb/c/init', 'p111/climb/c/tick'))

    # ================================================================== THE CRUMBLING RAFTERS
    rtick, rinit = copy('p76/r/rafters/tick'), copy('p76/r/rafters/init')
    rsign = lambda t_, body: [sign(rel(1.5, 7.5, 12), t_, body)]
    clear_r = [f'setblock {rel(x, 3, z)} minecraft:air' for x, z in R6.RAFT]
    # ---- B: blinking beams (a travelling wave; solid 42 ticks of 60, 36 on Tiers IV-V; they flicker first)
    RB = [(4, 12), (6, 12), (8, 13), (10, 13), (12, 12), (14, 11), (16, 11), (18, 12), (20, 12)]
    fn('p111/rafters/b/init', ['function bm:p70/ctx', 'scoreboard players operation @s bm.gvy3 = #gsf bm.rng'] + clear_r +
       [f'summon minecraft:marker {rel(x, 4, z)} {{Tags:["bm.gvprop","bm.gvrb","bm.gvrb{i}"]}}' for i, (x, z) in enumerate(RB)] +
       [f'scoreboard players set @e[type=minecraft:marker,tag=bm.gvrb{i},distance=..16,limit=1] bm.gvy1 {6 * i}' for i in range(len(RB))] +
       rsign('THE BLINKING BEAMS', 'The beams wink out and back in a wave - they flicker first. Time your crossing.'))
    fn('p111/rafters/b/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'scoreboard players operation #gt bm.rng = @s bm.gvt', 'scoreboard players operation #gsf bm.rng = @s bm.gvy3',
                               'scoreboard players operation #t bm.rng = @s bm.gvtm', 'scoreboard players set #cut bm.rng 42', 'execute if score #gt bm.rng matches 4.. run scoreboard players set #cut bm.rng 36',
                               'execute as @e[type=minecraft:marker,tag=bm.gvrb,distance=..16] at @s run function bm:p111/rafters/b/beam'] + rtick)
    fn('p111/rafters/b/beam', ['scoreboard players operation #p bm.rng = #t bm.rng', 'scoreboard players operation #p bm.rng += @s bm.gvy1', 'scoreboard players operation #p bm.rng %= #60 bm.rng',
                               'execute if score #p bm.rng >= #cut bm.rng unless block ~ ~-1 ~ minecraft:air run function bm:p111/rafters/b/gone',
                               'execute if score #p bm.rng < #cut bm.rng if block ~ ~-1 ~ minecraft:air run function bm:p111/rafters/b/come',
                               'scoreboard players operation #w bm.rng = #cut bm.rng', 'scoreboard players remove #w bm.rng 12',
                               'execute if score #p bm.rng >= #w bm.rng if score #p bm.rng < #cut bm.rng run particle minecraft:smoke ~ ~0.05 ~ 0.3 0 0.3 0 2'])
    fn('p111/rafters/b/gone', ['setblock ~ ~-1 ~ minecraft:air', 'playsound minecraft:block.wood.fall block @a[distance=..16] ~ ~ ~ 0.5 1.2'])
    fn('p111/rafters/b/come', themed('setblock ~ ~-1 ~ {b}', 'trim'))
    # ---- C: the ghost beams (barriers, shimmering only within reach)
    GP = PD.ghost_paths()
    fn('p111/rafters/c/init', ['function bm:p70/ctx'] + clear_r + choose('#i', len(GP), 'p111/rafters/c/p') +
       rsign('THE GHOST BEAMS', 'There is a way across. You just can\'t see it - not until you\'re right beside it.'))
    for j, path in enumerate(GP):
        fn(f'p111/rafters/c/p{j}', sum(([f'setblock {rel(x, 3, z)} minecraft:barrier', f'summon minecraft:marker {rel(x, 4, z)} {{Tags:["bm.gvprop","bm.gvrg"]}}'] for x, z in path), []))
    fn('p111/rafters/c/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #4 bm.rng',
                               'execute if score #q bm.rng matches 0 as @e[type=minecraft:marker,tag=bm.gvrg,distance=..16] at @s if entity @a[tag=bm.gvp,distance=..3.2] '
                               'run particle minecraft:dust{color:[0.75,0.9,1.0],scale:0.9} ~ ~0.05 ~ 0.3 0 0.3 0 3'] + rtick)
    dispatch('rafters', ('p111/rafters/b/init', 'p111/rafters/b/tick'), ('p111/rafters/c/init', 'p111/rafters/c/tick'))

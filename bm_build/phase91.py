"""2.67: GAME NIGHT IN THE VAULT - seven rooms after the games everyone knows (and two that race the clock).

THE SHOOTING GALLERY (timed)  targets pop up on the walls - hit enough of them in 30 seconds (6 + the tier, +2 for each
                              crewmate). Out of time: it costs a try, and you go again. (No bow? The gallery lends one.)
THE BUTTON DASH (timed)       six buttons on six perches: press them all before the clock runs out. Miss it: a try, again.
PIPE PLAZA                    bonk the ? blocks for coins, stomp the Grumbas, grab enough coins and touch the flagpole.
THE BLOCK TEMPLE              push the stone blocks onto the gold switches (hit a block to push it away from you). The
                              layouts get properly hard from Tier IV. Stuck? The button by the door resets it.
THE GIRDER CLIMB              a big rat at the top rolls barrels down the girders - climb the ladders, jump the barrels
                              (a coin for each one cleared), reach the gold plate at the top.
THE MEAD HALL                 raiders, berserkers and shieldmaidens - then the Jarl himself.
THE TALL GRASS (Tiers I-IV)   critters hide in the grass: throw Rat Balls (snowballs) at them to catch them. Something
                              wild might jump out at you. The Rat Center by the door hands out more balls.
"""
import math
import random
from items import T, ITEMS
from nbt import snbt, B, F, Int
from nbt import D as Dd
from structures import Build
import phase70_rooms as RM
import phase75 as P75
import phase76_rooms as R6
from phase75_rooms import BASE, wall_glow

GOLD = '#ffcf40'
GAME = '#7ad0ff'
FY = RM.FY
W, H = RM.W, RM.H
NAMES = {'gallery': 'The Shooting Gallery', 'dash': 'The Button Dash', 'plaza': 'Pipe Plaza', 'temple': 'The Block Temple', 'girder': 'The Girder Climb',
         'mead': 'The Mead Hall', 'grass': 'The Tall Grass'}


# ===================================================================== the rooms
GAL_SLOTS = [(x, y, 1) for x in (4, 7, 10, 14, 17, 20) for y in (5, 8)] + [(1, 6, 4), (1, 6, 7), (23, 6, 4), (23, 6, 7), (8, 5, 8), (12, 6, 6), (16, 5, 8)]


def gallery():
    b = R6.shell()
    for x in range(2, 23):                                   # the firing line (a rail you shoot over)
        if x in (11, 12, 13): continue
        b.set(x, 4, 15, 'minecraft:spruce_fence')
    for (x, y, z) in GAL_SLOTS:                              # a dark backing plate behind every slot
        if z == 1: b.set(x, y, 0, 'minecraft:black_concrete')
        elif x == 1: b.set(0, y, z, 'minecraft:black_concrete')
        elif x == 23: b.set(24, y, z, 'minecraft:black_concrete')
        else:
            for yy in range(4, y): b.set(x, yy, z, 'minecraft:spruce_fence')
    for x in range(2, 23):
        for z in range(16, 23): b.set(x, FY, z, 'minecraft:spruce_planks')
    for x in (3, 21): b.set(x, 13, 18, 'minecraft:lantern[hanging=true]')
    R6.ctrl(b, 'gallery'); return wall_glow(b)


DASH = [(4, 5, 4), (20, 6, 4), (4, 7, 20), (20, 8, 20), (12, 9, 5), (12, 6, 19)]      # (x, perch top y, z): a button on top of each


def dash():
    b = R6.shell()
    for (x, top, z) in DASH:
        for y in range(4, top + 1): b.set(x, y, z, 'minecraft:polished_deepslate')
        b.set(x, top + 1, z, 'minecraft:stone_button[face=floor,facing=north,powered=false]')
        # a stair of steps toward the room's middle, one block a step
        sx = 1 if x < 12 else (-1 if x > 12 else 0); sz = 1 if z < 12 else -1
        cx, cz = x, z
        for y in range(top - 1, 3, -1):
            cx, cz = (cx + sx, cz) if sx else (cx, cz + sz)
            if (cx, cz) == (x, z): continue
            if 10 <= cz <= 14 and (cx < 3 or cx > 21): break
            b.set(cx, y, cz, 'minecraft:polished_blackstone_bricks')
    R6.ctrl(b, 'dash'); return wall_glow(b)


QBLOCKS = [(6, 6, 9), (9, 6, 9), (12, 7, 9), (15, 6, 9), (18, 6, 9)]
PIPES = [(4, 3, 17), (9, 4, 19), (15, 2, 17), (20, 3, 19)]                   # (x, height, z): 2x2
FLAG = (22, 18)


def plaza():
    b = R6.shell()
    for x in range(1, W - 1):
        for z in range(1, RM.D - 1): b.set(x, FY, z, 'minecraft:grass_block[snowy=false]')
    for y in range(4, 15):                                   # sky walls with clouds
        for x in range(1, W - 1):
            for z in (0, RM.D - 1): b.set(x, y, z, 'minecraft:light_blue_concrete' if not (y in (11, 12) and x % 7 in (1, 2, 3)) else 'minecraft:white_wool')
        for z in range(1, RM.D - 1):
            for x in (0, W - 1):
                if not (10 <= z <= 14 and y <= 7): b.set(x, y, z, 'minecraft:light_blue_concrete')
    for (x, y, z) in QBLOCKS:
        b.set(x, y, z, 'minecraft:gold_block')
        for dx in (-1, 1):
            if (x + dx, y, z) not in [(q[0], q[1], q[2]) for q in QBLOCKS]: b.set(x + dx, y, z, 'minecraft:bricks')
    for (x, hgt, z) in PIPES:
        for dx in (0, 1):
            for dz in (0, 1):
                for y in range(4, 4 + hgt): b.set(x + dx, y, z + dz, 'minecraft:lime_concrete')
                b.set(x + dx, 4 + hgt, z + dz, 'minecraft:lime_terracotta')
    fx, fz = FLAG                                            # the flagpole on its block, a green flag at the top
    b.set(fx, 4, fz, 'minecraft:mossy_stone_bricks')
    for y in range(5, 13): b.set(fx, y, fz, 'minecraft:end_rod[facing=up]')
    for (dx, y) in ((-1, 12), (-2, 12), (-1, 11)): b.set(fx + dx, y, fz, 'minecraft:lime_wool')
    R6.ctrl(b, 'plaza'); return b


# ---- the Block Temple's layouts (each checked solvable when the pack is built)
TEMPLE = {
    'easy': ["#########",
             "#.......#",
             "#..B.S..#",
             "#.......#",
             "#.S.B...#",
             "#.......#",
             "####@####"],
    'medium': ["#########",
               "#S..#..S#",
               "#..B#B..#",
               "#.......#",
               "##.#B#.##",
               "#...S...#",
               "####@####"],
    'hard': ["###########",
             "#..S.#....#",
             "#..#.B.##B#",
             "#..###.##S#",
             "#....#....#",
             "#....SB...#",
             "#.........#",
             "#####@#####"],
    'hardest': ["###########",
                "#.....#.#.#",
                "#.......B.#",
                "#SB....##.#",
                "#.#.#.....#",
                "#B..#.....#",
                "#...#.S#.S#",
                "#####@#####"]}
TEMPLE_TIER = {1: 'easy', 2: 'easy', 3: 'medium', 4: 'hard', 5: 'hardest'}
TG = (7, 1)                                                  # the grid's north-west corner (x, z): 11 wide, 8 deep at most


def temple_cells(name):
    rows = TEMPLE[name]
    off = (11 - len(rows[0])) // 2
    out = []
    for z, r in enumerate(rows):
        for x, c in enumerate(r):
            out.append((TG[0] + off + x, TG[1] + z, c))
    return out


def solvable(rows):
    from collections import deque
    walls, blocks, sw, start, floor = set(), set(), set(), None, set()
    for z, r in enumerate(rows):
        for x, c in enumerate(r):
            if c == '#': walls.add((x, z)); continue
            if c in 'BX': blocks.add((x, z))
            if c in 'SX': sw.add((x, z))
            if c == '@': start = (x, z)
            else: floor.add((x, z))
    def reach(p, bl):
        seen = {p}; q = deque([p])
        while q:
            x, z = q.popleft()
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, z + dz)
                if n in seen or n in walls or n in bl or (n not in floor and n != start): continue
                seen.add(n); q.append(n)
        return seen
    s0 = frozenset(blocks); seen = {(min(reach(start, s0)), s0)}; q = deque([(start, s0, 0)])
    while q:
        p, bl, d = q.popleft()
        if sw <= bl: return d
        R = reach(p, bl)
        for bx, bz in bl:
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if (bx - dx, bz - dz) not in R: continue
                tgt = (bx + dx, bz + dz)
                if tgt in walls or tgt in bl or tgt not in floor: continue
                nb = frozenset(bl - {(bx, bz)} | {tgt})
                k = (min(reach((bx, bz), nb)), nb)
                if k in seen: continue
                seen.add(k); q.append(((bx, bz), nb, d + 1))
    return None


for _n, _rows in TEMPLE.items():
    assert solvable(_rows), f'the Block Temple layout {_n} cannot be solved'


def temple():
    b = R6.shell()
    for x in range(1, W - 1):
        for z in range(1, RM.D - 1): b.set(x, FY, z, 'minecraft:stone_bricks' if (x + z) % 5 else 'minecraft:mossy_stone_bricks')
    for x in range(TG[0] - 1, TG[0] + 12):                   # a raised dais for the grid (drawn per tier when the room wakes)
        for z in range(TG[1], TG[1] + 9): b.set(x, FY, z, 'minecraft:polished_andesite')
    for (x, z) in ((2, 2), (22, 2), (2, 22), (22, 22)):      # braziers
        b.set(x, 4, z, 'minecraft:stone_brick_wall'); b.set(x, 5, z, 'minecraft:campfire[lit=true,signal_fire=false,waterlogged=false,facing=north]')
    b.set(5, 4, 10, 'minecraft:chiseled_stone_bricks'); b.set(5, 5, 10, 'minecraft:stone_button[face=floor,facing=north,powered=false]')
    for y in range(4, 14):
        for z in (6, 18):
            if y % 3 == 0: b.set(1, y, z, 'minecraft:vine[east=true,north=false,south=false,up=false,west=false]')
    R6.ctrl(b, 'temple'); return wall_glow(b)


GIRDER = {6: (2, 22), 9: (1, 21), 12: (2, 21)}               # block layer y: x from..to (z 2-3)
LADDERS = [(18, 4, 7), (6, 7, 10), (16, 10, 13)]             # (x, y from, y to) at z 1, on the north wall


def girder():
    b = R6.shell()
    for y, (x0, x1) in GIRDER.items():
        for x in range(x0, x1 + 1):
            for z in (2, 3): b.set(x, y, z, 'minecraft:red_concrete')
            b.set(x, y + 1, 4, 'minecraft:iron_bars') if x % 4 == 0 else None
    for (x, y0, y1) in LADDERS:
        for y in range(y0, y1 + 1): b.set(x, y, 1, 'minecraft:ladder[facing=south,waterlogged=false]')
    for y in range(4, 8): b.set(23, y, 22, 'minecraft:ladder[facing=north,waterlogged=false]')
    b.set(3, 13, 2, 'minecraft:light_weighted_pressure_plate[power=0]')     # the goal, top west
    for x in range(2, 23, 5): b.set(x, 14, 12, 'minecraft:lantern[hanging=true]')
    R6.ctrl(b, 'girder'); return b


def mead():
    b = R6.shell()
    for x in range(1, W - 1):
        for z in range(1, RM.D - 1): b.set(x, FY, z, 'minecraft:spruce_planks')
    for y in range(4, 15):                                   # a longhouse: spruce walls, dark beams
        for x in range(1, W - 1):
            for z in (0, RM.D - 1): b.set(x, y, z, 'minecraft:stripped_dark_oak_log[axis=x]' if y in (4, 9, 14) else 'minecraft:spruce_planks')
        for z in range(1, RM.D - 1):
            for x in (0, W - 1):
                if not (10 <= z <= 14 and y <= 7): b.set(x, y, z, 'minecraft:stripped_dark_oak_log[axis=z]' if y in (4, 9, 14) else 'minecraft:spruce_planks')
    for x in range(4, 21):                                   # two long tables
        for z in (6, 18):
            b.set(x, 4, z, 'minecraft:spruce_slab[type=top]')
    for x in range(10, 15):                                  # the fire pit
        for z in range(10, 15):
            if x in (10, 14) or z in (10, 14): b.set(x, 4, z, 'minecraft:cobblestone_slab[type=bottom]')
    b.set(12, 4, 12, 'minecraft:campfire[lit=true,signal_fire=false,waterlogged=false,facing=north]')
    for x in (4, 8, 16, 20):                                 # shields on the walls
        b.set(x, 7, 1, 'minecraft:red_wall_banner[facing=south]'); b.set(x, 7, 23, 'minecraft:white_wall_banner[facing=north]')
    for x in range(3, 22, 6):
        for z in range(1, RM.D - 1): b.set(x, 13, z, 'minecraft:stripped_spruce_log[axis=z]')
    R6.ctrl(b, 'mead'); return b


def grass():
    b = R6.shell()
    rnd = random.Random(17)
    for x in range(1, W - 1):
        for z in range(1, RM.D - 1):
            b.set(x, FY, z, 'minecraft:grass_block[snowy=false]')
            if 10 <= z <= 14 and (x < 6 or x > 18): continue
            if (x, z) in ((3, 9), (4, 9), (3, 8)): continue
            if rnd.random() < 0.75:
                b.set(x, 4, z, 'minecraft:tall_grass[half=lower]'); b.set(x, 5, z, 'minecraft:tall_grass[half=upper]')
    for (tx, tz) in ((6, 4), (19, 19), (18, 5)):
        for y in range(4, 8): b.set(tx, y, tz, 'minecraft:oak_log[axis=y]')
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                for y in (7, 8):
                    if abs(dx) + abs(dz) <= 3 and (dx, dz) != (0, 0): b.set(tx + dx, y, tz + dz, 'minecraft:oak_leaves[distance=1,persistent=true,waterlogged=false]')
    b.set(3, 4, 9, 'minecraft:red_concrete'); b.set(4, 4, 9, 'minecraft:white_concrete'); b.set(3, 4, 8, 'minecraft:quartz_block')   # the Rat Center
    R6.ctrl(b, 'grass'); return b


BUILDERS = {'gallery': gallery, 'dash': dash, 'plaza': plaza, 'temple': temple, 'girder': girder, 'mead': mead, 'grass': grass}
POOLS = {'gallery': (1, 2, 3, 4, 5), 'dash': (1, 2, 3, 4, 5), 'plaza': (1, 2, 3), 'temple': (1, 2, 3, 4, 5), 'girder': (2, 3, 4, 5), 'mead': (2, 3, 4, 5),
         'grass': (1, 2, 3, 4)}
for _k, _f in BUILDERS.items():
    P75.EXTRA_ROOMS[_k] = _f
    R6.NAMES[_k] = NAMES[_k]
    for _t in POOLS[_k]: P75.EVENT_POOL[_t].append(_k)


def extend_offers(O, offer):
    pass


def generate(G):
    fn, wjson, tellraw, title = G.fn, G.wjson, G.tellraw, G.title
    rel = RM.rel
    ident = [F(0), F(0), F(0), F(1)]
    P = [T('[', 'dark_gray'), T('Heist', GOLD, bold=True), T('] ', 'dark_gray')]
    inst = lambda f: f'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run function {f}'
    crew = '@a[tag=bm.gvp,distance=..16]'
    mk = P75._mob
    def label(x, y, z, text, scale=0.6, tags=('bm.gvprop',), yaw=None):
        return f'summon minecraft:text_display {rel(x, y, z)} ' + snbt({'Tags': list(tags), 'billboard': 'vertical' if yaw is None else 'fixed', 'brightness': {'block': 15, 'sky': 15},
                                                                       **({'Rotation': [F(yaw), F(0)]} if yaw is not None else {}),
                                                                       'background': Int(0x90000000 - 2 ** 32), 'text': text, 'line_width': Int(220),
                                                                       'transformation': {'left_rotation': ident, 'right_rotation': ident,
                                                                                          'translation': [F(0)] * 3, 'scale': [F(scale)] * 3}})
    def sign(x, y, z, t_, body, col=GAME):
        return label(x, y, z, [T(t_ + '\n', col, bold=True), T(body, 'gray')])
    def big(t_, sub, col=GAME, who=crew):
        return [f'title {who} times 5 40 10', title(who, 'title', T(t_, col, bold=True)), title(who, 'subtitle', T(sub, 'gray'))]
    def pot(n):
        return [f'scoreboard players set #c bm.rng {n}', inst('bm:p75/pot_add')]
    def hud(txt, col, cur, goal, left_ticks_score=True):
        return [f'scoreboard players operation #h1 bm.rng = @s {cur}', f'scoreboard players operation #h2 bm.rng = @s {goal}',
                'scoreboard players operation #h3 bm.rng = @s bm.gvz', 'scoreboard players operation #h3 bm.rng -= @s bm.gvtm',
                'scoreboard players operation #h3 bm.rng /= #20 bm.rng',
                f'title {crew} actionbar ' + snbt([T(txt + ' ', col), {'score': {'name': '#h1', 'objective': 'bm.rng'}, 'color': 'white', 'bold': True},
                                                   T(' / ', 'gray'), {'score': {'name': '#h2', 'objective': 'bm.rng'}, 'color': 'white'},
                                                   T('    ', 'gray'), {'score': {'name': '#h3', 'objective': 'bm.rng'}, 'color': 'yellow'}, T(' s', 'yellow')])]
    objs = ['bm.gvz', 'bm.gvpz', 'bm.gvbc']
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.gvz dummy', 'scoreboard objectives add bm.gvpz minecraft.picked_up:minecraft.raw_gold',
                              'scoreboard objectives add bm.gvbc dummy']
    G.OBJECTIVES += objs
    fail_try = ['function bm:p70/ctx', 'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng at @s run function bm:p90/lose_try']

    ks = list(BUILDERS)
    G.FUNCS['p70/r/init'] += [f'execute if entity @s[tag=bm.gvr_{k}] run return run function bm:p91/{k}/init' for k in ks]
    G.FUNCS['p70/r/tick'] += [f'execute if entity @s[tag=bm.gvr_{k}] run return run function bm:p91/{k}/tick' for k in ks]
    k0 = next(i for i, l in enumerate(G.FUNCS['p70/r/init']) if 'tag @s add bm.gvnopick' in l)
    G.FUNCS['p70/r/init'][k0:k0] = [f'execute if entity @s[tag=bm.gvr_{k}] run tag @s add bm.gvnopick' for k in ks]
    G.FUNCS['p70/solved'] += [f'execute if entity @s[tag=bm.gvr_{k}] as @a[tag=bm.gvp,distance=..300] if score @s bm.gvi = #gi bm.rng run ' +
                              title('@s', 'actionbar', [T(NAMES[k], GOLD, bold=True), T(' - done. The way on is open.', 'gray')]) for k in ks]
    loan = lambda iid, n, extra='': f'{iid}[minecraft:custom_data={{bm_kit:1b}},minecraft:lore=[{snbt(T("Loaned by the Fixer - stays in the vault.", "dark_gray"))}]{extra}] {n}'

    # ================================================================== THE SHOOTING GALLERY (timed)
    N = len(GAL_SLOTS)
    fn('p91/gallery/init', ['function bm:p70/ctx', sign(12.5, 7.5, 21, 'THE SHOOTING GALLERY', 'Hit the targets as they pop up - enough of them in 30 seconds. Shoot from behind the rail.')])
    fn('p91/gallery/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'scoreboard players set @a[tag=bm.gvp,distance=..15] bm.gvmz 7',
                            'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..9] run function bm:p91/gallery/ready',
                            'execute if score @s bm.gvs matches 2 if score @s bm.gvx matches 2 if score @s bm.gvtm matches 60.. run function bm:p91/gallery/go',
                            'execute if score @s bm.gvs matches 2 if score @s bm.gvx matches 1 if score @s bm.gvtm matches 100.. run function bm:p91/gallery/ready',
                            'execute unless score @s bm.gvs matches 1 run return 0',
                            'scoreboard players set #hit bm.rng 0'] +
       [f'execute if block {rel(x, y, z)} minecraft:target unless block {rel(x, y, z)} minecraft:target[power=0] run function bm:p91/gallery/hit{i}' for i, (x, y, z) in enumerate(GAL_SLOTS)] +
       ['execute if score #hit bm.rng matches 1.. run scoreboard players operation @s bm.gvw += #hit bm.rng',
        'execute if score @s bm.gvw >= @s bm.gvc run return run function bm:p91/gallery/won',
        'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #10 bm.rng',
        'execute if score #q bm.rng matches 0 run function bm:p91/gallery/hud',
        'execute if score @s bm.gvtm >= @s bm.gvz run function bm:p91/gallery/timeout'])
    fn('p91/gallery/hud', hud('Targets', GAME, 'bm.gvw', 'bm.gvc'))
    for i, (x, y, z) in enumerate(GAL_SLOTS):
        fn(f'p91/gallery/hit{i}', [f'setblock {rel(x, y, z)} minecraft:air', 'scoreboard players add #hit bm.rng 1', f'particle minecraft:crit {rel(x, y, z)} 0.3 0.3 0.3 0.2 10',
                                   f'playsound minecraft:block.note_block.bit block @a[distance=..24] {rel(x, y, z)} 1 1.6', 'function bm:p91/gallery/pop'])
    fn('p91/gallery/pop', [f'execute store result score #r bm.rng run random value 0..{N - 1}', 'scoreboard players set #k bm.rng 0', 'function bm:p91/gallery/put'])
    fn('p91/gallery/put', ['execute if score #k bm.rng matches %d.. run return 0' % N] +
       [f'execute if score #r bm.rng matches {i} if block {rel(x, y, z)} minecraft:air run return run setblock {rel(x, y, z)} minecraft:target' for i, (x, y, z) in enumerate(GAL_SLOTS)] +
       ['scoreboard players add #r bm.rng 1', f'execute if score #r bm.rng matches {N}.. run scoreboard players set #r bm.rng 0', 'scoreboard players add #k bm.rng 1',
        'function bm:p91/gallery/put'])
    clear_targets = [f'setblock {rel(x, y, z)} minecraft:air replace' for (x, y, z) in GAL_SLOTS]
    fn('p91/gallery/ready', ['function bm:p70/ctx', 'scoreboard players set @s bm.gvs 2', 'scoreboard players set @s bm.gvx 2', 'scoreboard players set @s bm.gvtm 0'] + clear_targets +
       ['execute as @a[tag=bm.gvp,distance=..16] unless items entity @s container.* minecraft:bow unless items entity @s weapon.offhand minecraft:bow run give @s ' +
        loan('minecraft:bow', 1, ',minecraft:custom_name=' + snbt(T('Gallery Bow', GAME))),
        'execute as @a[tag=bm.gvp,distance=..16] run give @s ' + loan('minecraft:arrow', 24)] +
       big('THE SHOOTING GALLERY', 'Get behind the rail... 3... 2... 1...'))
    fn('p91/gallery/go', ['scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvtm 0', 'scoreboard players set @s bm.gvw 0', 'scoreboard players set @s bm.gvz 600',
                          'execute store result score @s bm.gvc if entity @a[tag=bm.gvp,distance=..20]', 'scoreboard players remove @s bm.gvc 1',
                          'scoreboard players operation @s bm.gvc *= #2 bm.rng', 'scoreboard players operation @s bm.gvc += #gt bm.rng', 'scoreboard players add @s bm.gvc 6',
                          'function bm:p91/gallery/pop', 'function bm:p91/gallery/pop', 'playsound minecraft:block.note_block.pling block @a[distance=..24] ~ ~ ~ 1 1.8',
                          title(crew, 'actionbar', T('GO!', GAME, bold=True))])
    fn('p91/gallery/won', clear_targets + pot(6) + big('SHARPSHOOTERS!', 'Every target down. The way on is open.') + ['function bm:p70/solved'])
    fn('p91/gallery/timeout', clear_targets + ['scoreboard players set @s bm.gvs 2', 'scoreboard players set @s bm.gvx 1', 'scoreboard players set @s bm.gvtm 0'] +
       big('TIME!', 'That cost a try - again in five seconds.', '#ff6a6a') + ['playsound minecraft:block.note_block.bass block @a[distance=..24] ~ ~ ~ 1 0.5'] + fail_try)

    # ================================================================== THE BUTTON DASH (timed)
    btn = lambda x, top, z: rel(x, top + 1, z)
    reset_dash = [f'setblock {btn(x, t, z)} minecraft:stone_button[face=floor,facing=north,powered=false]' for (x, t, z) in DASH] + \
                 [f'setblock {rel(x, t, z)} minecraft:polished_deepslate' for (x, t, z) in DASH]
    fn('p91/dash/init', ['function bm:p70/ctx', sign(2.5, 7.5, 12, 'THE BUTTON DASH', 'Press the button on top of every perch before time runs out.')])
    fn('p91/dash/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'scoreboard players set @a[tag=bm.gvp,distance=..15] bm.gvmz 7',
                         'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..9] run function bm:p91/dash/ready',
                         'execute if score @s bm.gvs matches 2 if score @s bm.gvx matches 2 if score @s bm.gvtm matches 60.. run function bm:p91/dash/go',
                         'execute if score @s bm.gvs matches 2 if score @s bm.gvx matches 1 if score @s bm.gvtm matches 100.. run function bm:p91/dash/ready',
                         'execute unless score @s bm.gvs matches 1 run return 0'] +
       [f'execute if block {btn(x, t, z)} minecraft:stone_button[powered=true] run function bm:p91/dash/press{i}' for i, (x, t, z) in enumerate(DASH)] +
       ['execute if score @s bm.gvw matches %d.. run return run function bm:p91/dash/won' % len(DASH),
        'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #10 bm.rng',
        'execute if score #q bm.rng matches 0 run function bm:p91/dash/hud', 'execute if score @s bm.gvtm >= @s bm.gvz run function bm:p91/dash/timeout'])
    fn('p91/dash/hud', ['scoreboard players set @s bm.gvc %d' % len(DASH)] + hud('Buttons', GAME, 'bm.gvw', 'bm.gvc'))
    for i, (x, t, z) in enumerate(DASH):
        fn(f'p91/dash/press{i}', [f'setblock {btn(x, t, z)} minecraft:air', f'setblock {rel(x, t, z)} minecraft:redstone_lamp[lit=true]', 'scoreboard players add @s bm.gvw 1',
                                  f'playsound minecraft:block.note_block.chime block @a[distance=..24] {btn(x, t, z)} 1 {1.0 + 0.1 * i:.1f}',
                                  f'particle minecraft:happy_villager {btn(x, t, z)} 0.3 0.3 0.3 0 8'])
    fn('p91/dash/ready', ['scoreboard players set @s bm.gvs 2', 'scoreboard players set @s bm.gvx 2', 'scoreboard players set @s bm.gvtm 0', 'scoreboard players set @s bm.gvw 0'] + reset_dash +
       big('THE BUTTON DASH', 'Every perch, every button... 3... 2... 1...'))
    fn('p91/dash/go', ['function bm:p70/ctx', 'scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvtm 0',
                       'scoreboard players set @s bm.gvz 700', 'scoreboard players operation #q bm.rng = #gt bm.rng', 'scoreboard players operation #q bm.rng *= #30 bm.rng',
                       'scoreboard players operation @s bm.gvz -= #q bm.rng',
                       'playsound minecraft:block.note_block.pling block @a[distance=..24] ~ ~ ~ 1 1.8', title(crew, 'actionbar', T('GO!', GAME, bold=True))])
    fn('p91/dash/won', pot(5) + big('DASHED IT!', 'Six for six. The way on is open.') + ['function bm:p70/solved'])
    fn('p91/dash/timeout', ['scoreboard players set @s bm.gvs 2', 'scoreboard players set @s bm.gvx 1', 'scoreboard players set @s bm.gvtm 0'] + big('TIME!', 'That cost a try - again in five seconds.', '#ff6a6a') +
       ['playsound minecraft:block.note_block.bass block @a[distance=..24] ~ ~ ~ 1 0.5'] + fail_try)
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #30 bm.rng 30', 'scoreboard players set #10 bm.rng 10']

    # ================================================================== PIPE PLAZA
    coin_model = ITEMS['gutter_coin']['comps'].get('minecraft:item_model', 'minecraft:gold_nugget')
    coin = lambda mot=None: snbt(dict({'Item': {'id': 'minecraft:raw_gold', 'count': Int(1), 'components': {'minecraft:custom_data': {'bm_pz': B(1)}, 'minecraft:item_model': coin_model}},
                                       'Age': Int(-32768), 'PickupDelay': Int(0), 'Tags': ['bm.gvprop', 'bm.gvpzc']}, **({'Motion': [Dd(m) for m in mot]} if mot else {'NoGravity': B(1)})))
    LOOSE = [(4, 4 + 3 + 1, 17), (9, 4 + 4 + 1, 19), (15, 4 + 2 + 1, 17), (20, 4 + 3 + 1, 19), (12, 9, 9), (3, 5, 4), (21, 5, 4)]
    grumba = mk('husk', 'Grumba', '#a0703a', {'head': 'minecraft:brown_mushroom_block'},
                {'Tags': ['bm.gvg', 'bm.gvnew2', 'bm.tiered', 'bm.seen', 'bm.gvgrum'], 'IsBaby': B(1)}, {'movement_speed': 0.18, 'attack_damage': 2.0})
    GRUM_SPOTS = [(8, 13), (14, 15), (18, 8), (6, 6), (16, 21), (11, 4)]
    fn('p91/plaza/init', ['function bm:p70/ctx'] +
       [f'summon minecraft:interaction {rel(x, y, z)} ' + snbt({'Tags': ['bm.gvprop', 'bm.gvq'], 'width': F(1.02), 'height': F(1.02), 'response': B(1)}) for (x, y, z) in QBLOCKS] +
       [label(x, y + 0.15, z + 0.52, T('?', '#fff4c0', bold=True), 1.4, ('bm.gvprop', 'bm.gvql'), 0) for (x, y, z) in QBLOCKS] +
       [label(x, y + 0.15, z - 0.52, T('?', '#fff4c0', bold=True), 1.4, ('bm.gvprop', 'bm.gvql'), 180) for (x, y, z) in QBLOCKS] +
       [f'summon minecraft:item {rel(x, y + 0.3, z)} {coin()}' for (x, y, z) in LOOSE] +
       [f'summon minecraft:interaction {rel(FLAG[0], 4, FLAG[1])} ' + snbt({'Tags': ['bm.gvprop', 'bm.gvflag'], 'width': F(1.4), 'height': F(9.0), 'response': B(1)}),
        'scoreboard players set #n bm.rng 3', 'scoreboard players operation #n bm.rng += #gt bm.rng'] +
       [f'execute if score #n bm.rng matches {i + 1}.. positioned {rel(x, 4, z)} run function bm:p91/plaza/grumba' for i, (x, z) in enumerate(GRUM_SPOTS)] +
       [sign(2.5, 7.5, 12, 'PIPE PLAZA', 'Bonk the ? blocks, stomp the Grumbas, grab the coins - then touch the flagpole.', '#ffd040')])
    fn('p91/plaza/grumba', [f'summon minecraft:husk ~ ~ ~ {snbt(grumba[1])}', 'function bm:p70/guard_set'])
    fn('p91/plaza/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'scoreboard players set @a[tag=bm.gvp,distance=..15] bm.gvmz 7',
                          'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..12] run function bm:p91/plaza/start',
                          'execute as @e[type=minecraft:interaction,tag=bm.gvq,distance=..16] if data entity @s attack at @s run function bm:p91/plaza/bonk',
                          'execute as @e[type=minecraft:interaction,tag=bm.gvq,distance=..16] if data entity @s interaction at @s run function bm:p91/plaza/bonk',
                          'execute as @a[tag=bm.gvp,distance=..16,scores={bm.gvpz=1..}] at @s run function bm:p91/plaza/coin',
                          # (a stomp: in the air, feet about level with a Grumba's head, right above it)
                          'tag @a[tag=bm.gvstomp,distance=..18,nbt={OnGround:1b}] remove bm.gvstomp',
                          'execute as @a[tag=bm.gvp,tag=!bm.gvstomp,distance=..18,nbt={OnGround:0b}] at @s positioned ~ ~-1 ~ if entity @e[type=minecraft:husk,tag=bm.gvgrum,distance=..0.75] run function bm:p91/plaza/stomp',
                          'execute if entity @e[type=minecraft:interaction,tag=bm.gvflag,distance=..16,nbt={attack:{}}] run return run function bm:p91/plaza/flag',
                          'execute if entity @e[type=minecraft:interaction,tag=bm.gvflag,distance=..16,nbt={interaction:{}}] run return run function bm:p91/plaza/flag',
                          f'execute positioned {rel(FLAG[0] - 1.5, 4, FLAG[1] - 1.5)} if entity @a[tag=bm.gvp,dx=2,dy=3,dz=2] positioned as @s run function bm:p91/plaza/flag'])   # (back at the room's centre: the door it opens is measured from there)
    fn('p91/plaza/start', ['scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvw 0', 'scoreboard players set @a[tag=bm.gvp,distance=..20] bm.gvpz 0',
                           'execute store result score @s bm.gvc if entity @a[tag=bm.gvp,distance=..20]', 'scoreboard players remove @s bm.gvc 1',
                           'scoreboard players operation @s bm.gvc *= #2 bm.rng', 'scoreboard players add @s bm.gvc 8'] +
       big('PIPE PLAZA', 'Coins, ? blocks, Grumbas - and a flagpole at the end.', '#ffd040'))
    fn('p91/plaza/bonk', ['data remove entity @s attack', 'data remove entity @s interaction', 'execute if entity @s[tag=bm.gvqused] run return 0', 'tag @s add bm.gvqused',
                          'setblock ~ ~ ~ minecraft:brown_terracotta', 'kill @e[type=minecraft:text_display,tag=bm.gvql,distance=..1.2]',
                          f'summon minecraft:item ~ ~1.1 ~ {coin((0.08, 0.35, 0.0))}', f'summon minecraft:item ~ ~1.1 ~ {coin((-0.08, 0.4, 0.05))}',
                          'playsound minecraft:block.note_block.bell block @a[distance=..20] ~ ~ ~ 1 1.8', 'particle minecraft:wax_on ~ ~0.6 ~ 0.3 0.3 0.3 0 12'])
    fn('p91/plaza/coin', ['scoreboard players operation #c bm.rng = @s bm.gvpz', 'scoreboard players set @s bm.gvpz 0', 'clear @s minecraft:raw_gold[minecraft:custom_data~{bm_pz:1b}]',
                          'scoreboard players operation #w bm.rng = #c bm.rng',
                          'execute as @e[type=minecraft:marker,tag=bm.gvr_plaza,distance=..30,limit=1,sort=nearest] run scoreboard players operation @s bm.gvw += #w bm.rng',
                          inst('bm:p75/pot_add'), 'playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.7 1.8',
                          'scoreboard players operation #h1 bm.rng = @e[type=minecraft:marker,tag=bm.gvr_plaza,distance=..30,limit=1,sort=nearest] bm.gvw',
                          'scoreboard players operation #h2 bm.rng = @e[type=minecraft:marker,tag=bm.gvr_plaza,distance=..30,limit=1,sort=nearest] bm.gvc',
                          f'title {crew} actionbar ' + snbt([T('Coins ', '#ffd040'), {'score': {'name': '#h1', 'objective': 'bm.rng'}, 'color': 'white', 'bold': True}, T(' / ', 'gray'),
                                                             {'score': {'name': '#h2', 'objective': 'bm.rng'}, 'color': 'white'}])])
    fn('p91/plaza/stomp', ['tag @s add bm.gvstomp', 'execute as @e[type=minecraft:husk,tag=bm.gvgrum,distance=..0.75,limit=1,sort=nearest] at @s run function bm:p91/plaza/squash'])
    fn('p91/plaza/squash', ['particle minecraft:block{block_state:"minecraft:brown_mushroom_block"} ~ ~0.5 ~ 0.3 0.2 0.3 0 20',
                            'playsound minecraft:entity.slime.squish neutral @a[distance=..16] ~ ~ ~ 1 1.4', f'summon minecraft:item ~ ~0.6 ~ {coin((0.0, 0.3, 0.0))}',
                            'tag @s add bm.gvgone', 'tp @s ~ -200 ~', 'kill @s'])
    fn('p91/plaza/flag', ['execute as @e[type=minecraft:interaction,tag=bm.gvflag,distance=..30] run data remove entity @s attack',
                          'execute as @e[type=minecraft:interaction,tag=bm.gvflag,distance=..30] run data remove entity @s interaction',
                          'execute if score @s bm.gvw < @s bm.gvc run return run function bm:p91/plaza/notyet',
                          'scoreboard players set @s bm.gvs 2'] + pot(6) +
       big('COURSE CLEAR!', 'The flag comes down - the way on is open.', '#ffd040') +
       [f'particle minecraft:firework {rel(FLAG[0], 10, FLAG[1])} 1 2 1 0.1 40', 'playsound minecraft:entity.firework_rocket.blast block @a[distance=..24] ~ ~ ~ 1 1',
        'kill @e[type=minecraft:husk,tag=bm.gvgrum,distance=..20]', 'kill @e[type=minecraft:item,tag=bm.gvpzc,distance=..20]', 'function bm:p70/solved'])
    fn('p91/plaza/notyet', ['scoreboard players operation #h1 bm.rng = @s bm.gvw', 'scoreboard players operation #h2 bm.rng = @s bm.gvc',
                            f'title {crew} actionbar ' + snbt([T('Not yet - coins ', '#ffd040'), {'score': {'name': '#h1', 'objective': 'bm.rng'}, 'color': 'white', 'bold': True},
                                                               T(' / ', 'gray'), {'score': {'name': '#h2', 'objective': 'bm.rng'}, 'color': 'white'}])])

    # ================================================================== THE BLOCK TEMPLE (push-block puzzles)
    wjson('bm/tags/block/temple_floor.json', {'values': ['minecraft:smooth_stone', 'minecraft:gold_block']})
    stone = {'Tags': ['bm.gvprop', 'bm.gvtb'], 'block_state': 'minecraft:mossy_cobblestone', 'teleport_duration': Int(3),
             'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(-0.5), F(0), F(-0.5)], 'scale': [F(1.0)] * 3}}
    for name in TEMPLE:
        cells = temple_cells(name)
        lay = [f'fill {rel(TG[0] - 1, 3, TG[1])} {rel(TG[0] + 11, 3, TG[1] + 8)} minecraft:polished_andesite',
               f'fill {rel(TG[0] - 1, 4, TG[1])} {rel(TG[0] + 11, 6, TG[1] + 8)} minecraft:air']
        for (x, z, c) in cells:
            if c == '#': lay += [f'setblock {rel(x, 3, z)} minecraft:mossy_stone_bricks', f'fill {rel(x, 4, z)} {rel(x, 5, z)} minecraft:mossy_stone_bricks',
                                 f'setblock {rel(x, 6, z)} minecraft:barrier']
            elif c == '@': lay.append(f'setblock {rel(x, 3, z)} minecraft:polished_andesite')
            elif c in 'SX': lay.append(f'setblock {rel(x, 3, z)} minecraft:gold_block')
            else: lay.append(f'setblock {rel(x, 3, z)} minecraft:smooth_stone')
            if c in 'BX':
                lay += [f'fill {rel(x, 4, z)} {rel(x, 5, z)} minecraft:barrier', f'summon minecraft:block_display {rel(x, 4, z)} {snbt(stone)}',
                        f'summon minecraft:interaction {rel(x, 4, z)} ' + snbt({'Tags': ['bm.gvprop', 'bm.gvtbi'], 'width': F(1.02), 'height': F(1.02), 'response': B(1)})]
        fn(f'p91/temple/lay_{name}', ['kill @e[type=minecraft:block_display,tag=bm.gvtb,distance=..20]', 'kill @e[type=minecraft:interaction,tag=bm.gvtbi,distance=..20]'] + lay)
        sw = [(x, z) for (x, z, c) in cells if c in 'SX']
        fn(f'p91/temple/check_{name}', ['scoreboard players set #n bm.rng 0'] + [f'execute if block {rel(x, 4, z)} minecraft:barrier run scoreboard players add #n bm.rng 1' for (x, z) in sw] +
           [f'execute if score #n bm.rng matches {len(sw)} run function bm:p91/temple/done'])
    fn('p91/temple/init', ['function bm:p70/ctx', 'scoreboard players operation @s bm.gvt = #gt bm.rng', 'function bm:p91/temple/lay',
                           sign(2.5, 7.5, 12, 'THE BLOCK TEMPLE', 'Push every stone block onto a gold switch. Hit a block to push it away from you. The button resets it.', '#7adf8a')])
    fn('p91/temple/lay', [f'execute if score @s bm.gvt matches {t} run function bm:p91/temple/lay_{n}' for t, n in TEMPLE_TIER.items()])
    fn('p91/temple/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'scoreboard players set @a[tag=bm.gvp,distance=..15] bm.gvmz 9',
                           'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..12] run function bm:p91/temple/start',
                           'execute as @e[type=minecraft:interaction,tag=bm.gvtbi,distance=..20] if data entity @s attack at @s run function bm:p91/temple/push',
                           'execute as @e[type=minecraft:interaction,tag=bm.gvtbi,distance=..20] if data entity @s interaction at @s run function bm:p91/temple/push',
                           f'execute if block {rel(5, 5, 10)} minecraft:stone_button[powered=true] run function bm:p91/temple/reset',
                           'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #10 bm.rng',
                           'execute if score #q bm.rng matches 0 run function bm:p91/temple/check'])
    fn('p91/temple/start', ['scoreboard players set @s bm.gvs 1'] + big('THE BLOCK TEMPLE', 'Every block on a switch. Think before you push.', '#7adf8a'))
    fn('p91/temple/check', [f'execute if score @s bm.gvt matches {t} run function bm:p91/temple/check_{n}' for t, n in TEMPLE_TIER.items()])
    fn('p91/temple/reset', [f'setblock {rel(5, 5, 10)} minecraft:stone_button[face=floor,facing=north,powered=false]', 'function bm:p91/temple/lay',
                            'playsound minecraft:block.stone.place block @a[distance=..20] ~ ~ ~ 1 0.6', title(crew, 'actionbar', T('The blocks grind back where they began.', '#7adf8a'))])
    # (as the block's interaction, at it) which way: away from whoever hit it, along the longer axis
    fn('p91/temple/push', ['scoreboard players set #pu bm.rng 0', 'execute if data entity @s attack on attacker run function bm:p91/temple/who',
                           'execute if score #pu bm.rng matches 0 if data entity @s interaction on target run function bm:p91/temple/who',
                           'data remove entity @s attack', 'data remove entity @s interaction',
                           'execute if score #pu bm.rng matches 0 run return 0',
                           'execute store result score #bx bm.rng run data get entity @s Pos[0] 100', 'execute store result score #bz bm.rng run data get entity @s Pos[2] 100',
                           'scoreboard players operation #bx bm.rng -= #px bm.rng', 'scoreboard players operation #bz bm.rng -= #pz bm.rng',
                           'scoreboard players operation #ax bm.rng = #bx bm.rng', 'execute if score #ax bm.rng matches ..-1 run scoreboard players operation #ax bm.rng *= #-1 bm.rng',
                           'scoreboard players operation #az bm.rng = #bz bm.rng', 'execute if score #az bm.rng matches ..-1 run scoreboard players operation #az bm.rng *= #-1 bm.rng',
                           'data modify storage bm:gv tpush set value {dx:0,dz:-1,nx:0,nz:1}',
                           'execute if score #bz bm.rng matches 1.. run data modify storage bm:gv tpush set value {dx:0,dz:1,nx:0,nz:-1}',
                           'execute if score #ax bm.rng >= #az bm.rng if score #bx bm.rng matches ..0 run data modify storage bm:gv tpush set value {dx:-1,dz:0,nx:1,nz:0}',
                           'execute if score #ax bm.rng >= #az bm.rng if score #bx bm.rng matches 1.. run data modify storage bm:gv tpush set value {dx:1,dz:0,nx:-1,nz:0}',
                           'tag @s add bm.gvtbme', 'function bm:p91/temple/aim with storage bm:gv tpush', 'tag @s remove bm.gvtbme'])
    fn('p91/temple/aim', ['$execute positioned ~$(dx) ~ ~$(dz) run function bm:p91/temple/try with storage bm:gv tpush'])
    fn('p91/temple/who', ['scoreboard players set #pu bm.rng 1', 'execute store result score #px bm.rng run data get entity @s Pos[0] 100',
                          'execute store result score #pz bm.rng run data get entity @s Pos[2] 100'])
    # (positioned at the target cell) free floor, nothing in it: slide there
    fn('p91/temple/try', ['execute unless block ~ ~-1 ~ #bm:temple_floor run return run playsound minecraft:block.stone.hit block @a[distance=..16] ~ ~ ~ 1 0.5',
                          'execute unless block ~ ~ ~ minecraft:air run return run playsound minecraft:block.stone.hit block @a[distance=..16] ~ ~ ~ 1 0.5',
                          'execute unless block ~ ~1 ~ minecraft:air run return run playsound minecraft:block.stone.hit block @a[distance=..16] ~ ~ ~ 1 0.5',
                          'execute positioned ~-0.5 ~ ~-0.5 if entity @e[type=!minecraft:block_display,type=!minecraft:interaction,type=!minecraft:marker,type=!minecraft:text_display,type=!minecraft:item_display,type=!minecraft:item,dx=0,dy=1,dz=0] run return run playsound minecraft:block.stone.hit block @a[distance=..16] ~ ~ ~ 1 0.5',
                          '$execute positioned ~$(nx) ~ ~$(nz) as @e[type=minecraft:block_display,tag=bm.gvtb,distance=..0.3,limit=1] run tp @s ~$(dx) ~ ~$(dz)',
                          'fill ~ ~ ~ ~ ~1 ~ minecraft:barrier', '$execute positioned ~$(nx) ~ ~$(nz) run fill ~ ~ ~ ~ ~1 ~ minecraft:air',
                          'tp @e[type=minecraft:interaction,tag=bm.gvtbme,limit=1] ~ ~ ~',
                          'playsound minecraft:block.stone.place block @a[distance=..16] ~ ~ ~ 1 0.8', 'particle minecraft:block{block_state:"minecraft:mossy_cobblestone"} ~ ~0.1 ~ 0.3 0.05 0.3 0 6'])
    fn('p91/temple/done', ['scoreboard players set @s bm.gvs 2', 'execute as @e[type=minecraft:block_display,tag=bm.gvtb,distance=..20] run data merge entity @s {Glowing:1b}'] + pot(6) +
       big('THE TEMPLE OPENS', 'Every switch pressed. The way on is open.', '#7adf8a') + ['playsound minecraft:block.end_portal_frame.fill block @a[distance=..20] ~ ~ ~ 1 0.8',
                                                                                         'function bm:p70/solved'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #-1 bm.rng -1']

    # ================================================================== THE GIRDER CLIMB
    rat = {'Tags': ['bm.gvprop', 'bm.gvgrat'], 'Rotation': [F(90), F(0)], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:rat3d_pirate'}},
           'item_display': 'fixed', 'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.9), F(0)], 'scale': [F(1.8)] * 3}}
    barrel = {'Tags': ['bm.gvprop', 'bm.gvbar'], 'block_state': {'id': 'minecraft:barrel', 'properties': {'facing': 'south', 'open': 'false'}}, 'teleport_duration': Int(1),
              'interpolation_duration': Int(2), 'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(-0.4)] * 3, 'scale': [F(0.8)] * 3}}
    fn('p91/girder/init', ['function bm:p70/ctx', 'scoreboard players operation @s bm.gvt = #gt bm.rng', f'summon minecraft:item_display {rel(21, 13, 2.5)} {snbt(rat)}',
                           sign(2.5, 7.5, 12, 'THE GIRDER CLIMB', 'Climb to the gold plate at the top. Jump the barrels!', '#ff6a4a')])
    fn('p91/girder/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'scoreboard players set @a[tag=bm.gvp,distance=..18] bm.gvmz 7',
                           'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..12] run function bm:p91/girder/start',
                           'execute unless score @s bm.gvs matches 1 run return 0',
                           'execute store result score #mx bm.rng run data get entity @s Pos[0] 100', 'execute store result score #my bm.rng run data get entity @s Pos[1] 100',
                           'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= @s bm.gvz',
                           'execute if score #q bm.rng matches 0 run function bm:p91/girder/throw',
                           'execute as @e[type=minecraft:block_display,tag=bm.gvbar,distance=..24] at @s run function bm:p91/girder/roll',
                           f'execute positioned {rel(2, 13, 2)} if entity @a[tag=bm.gvp,dx=2,dy=1,dz=1] positioned as @s run function bm:p91/girder/done'])   # (back at the centre, or the door it opens is ten blocks off)
    fn('p91/girder/start', ['scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvtm 0', 'scoreboard players set @s bm.gvz 60',
                            'scoreboard players operation #q bm.rng = @s bm.gvt', 'scoreboard players operation #q bm.rng *= #5 bm.rng', 'scoreboard players operation @s bm.gvz -= #q bm.rng',
                            'scoreboard players set @s bm.gvc 14', 'scoreboard players operation @s bm.gvc += @s bm.gvt', 'scoreboard players operation @s bm.gvc += @s bm.gvt'] +
       big('THE GIRDER CLIMB', 'Up the ladders - mind the barrels!', '#ff6a4a'))
    fn('p91/girder/throw', [f'summon minecraft:block_display {rel(19, 13.4, 2.5)} {snbt(barrel)}',
                            'execute as @e[type=minecraft:block_display,tag=bm.gvbar,distance=..24] unless score @s bm.gvx matches 0.. run scoreboard players operation @s bm.gvc = @e[type=minecraft:marker,tag=bm.gvr_girder,limit=1,sort=nearest] bm.gvc',
                            'execute as @e[type=minecraft:block_display,tag=bm.gvbar,distance=..24] unless score @s bm.gvx matches 0.. run scoreboard players set @s bm.gvx 0',
                            'playsound minecraft:entity.ravager.roar hostile @a[distance=..24] ~ ~ ~ 0.4 1.8'])
    # (as a barrel, at it) where it is (in the room's own hundredths), then which way it goes: west on the top girder, drop, east,
    # drop, west, drop, east along the floor and gone. #mx/#my: the room marker (12.5, 4) in hundredths
    seg_speed = lambda d: f'execute store result entity @s Pos[0] double 0.01 run scoreboard players operation #bx bm.rng {"-=" if d < 0 else "+="} @s bm.gvc'
    fn('p91/girder/roll', ['execute store result score #bx bm.rng run data get entity @s Pos[0] 100', 'execute store result score #by bm.rng run data get entity @s Pos[1] 100',
                           'scoreboard players operation #lx bm.rng = #bx bm.rng', 'scoreboard players operation #lx bm.rng -= #mx bm.rng', 'scoreboard players add #lx bm.rng 1250',
                           'scoreboard players operation #ly bm.rng = #by bm.rng', 'scoreboard players operation #ly bm.rng -= #my bm.rng', 'scoreboard players add #ly bm.rng 400',
                           'execute if score @s bm.gvx matches 0 if score #lx bm.rng matches ..150 run scoreboard players set @s bm.gvx 1',
                           'execute if score @s bm.gvx matches 2 if score #lx bm.rng matches 2250.. run scoreboard players set @s bm.gvx 3',
                           'execute if score @s bm.gvx matches 4 if score #lx bm.rng matches ..150 run scoreboard players set @s bm.gvx 5',
                           'execute if score @s bm.gvx matches 6 if score #lx bm.rng matches 2200.. run return run kill @s',
                           'execute if score @s bm.gvx matches 1 if score #ly bm.rng matches ..1040 run function bm:p91/girder/land {y:1040,s:2}',
                           'execute if score @s bm.gvx matches 3 if score #ly bm.rng matches ..740 run function bm:p91/girder/land {y:740,s:4}',
                           'execute if score @s bm.gvx matches 5 if score #ly bm.rng matches ..440 run function bm:p91/girder/land {y:440,s:6}',
                           'execute if score @s bm.gvx matches 0 run ' + seg_speed(-1), 'execute if score @s bm.gvx matches 4 run ' + seg_speed(-1),
                           'execute if score @s bm.gvx matches 2 run ' + seg_speed(1), 'execute if score @s bm.gvx matches 6 run ' + seg_speed(1),
                           'execute if score @s bm.gvx matches 1 run tp @s ~ ~-0.4 ~', 'execute if score @s bm.gvx matches 3 run tp @s ~ ~-0.4 ~', 'execute if score @s bm.gvx matches 5 run tp @s ~ ~-0.4 ~',
                           # it rolls (a quarter turn every other tick)
                           'scoreboard players add @s bm.gvw 1', 'scoreboard players operation #q bm.rng = @s bm.gvw', 'scoreboard players operation #q bm.rng %= #8 bm.rng',
                           # (rolling the other way round going east; each turn keeps the barrel centred on its spot)
                           'execute if score #q bm.rng matches 0 run data merge entity @s {start_interpolation:0,transformation:{left_rotation:[0f,0f,0f,1f],translation:[-0.4f,-0.4f,-0.4f]}}',
                           'execute if score #q bm.rng matches 2 run data merge entity @s {start_interpolation:0,transformation:{left_rotation:[0f,0f,0.7071f,0.7071f],translation:[0.4f,-0.4f,-0.4f]}}',
                           'execute if score #q bm.rng matches 4 run data merge entity @s {start_interpolation:0,transformation:{left_rotation:[0f,0f,1f,0f],translation:[0.4f,0.4f,-0.4f]}}',
                           'execute if score #q bm.rng matches 6 run data merge entity @s {start_interpolation:0,transformation:{left_rotation:[0f,0f,0.7071f,-0.7071f],translation:[-0.4f,0.4f,-0.4f]}}',
                           'execute positioned ~ ~-0.4 ~ as @a[tag=bm.gvp,distance=..0.8] at @s run return run function bm:p91/girder/hit',
                           'execute if entity @s[tag=!bm.gvjmpd] positioned ~-0.5 ~0.45 ~-0.5 as @a[tag=bm.gvp,dx=0,dy=0,dz=0,nbt={OnGround:0b}] at @s run function bm:p91/girder/cleared'])
    fn('p91/girder/land', ['$scoreboard players set @s bm.gvx $(s)', '$scoreboard players set #t bm.rng $(y)', 'scoreboard players remove #t bm.rng 400',
                           'scoreboard players operation #t bm.rng += #my bm.rng', 'execute store result entity @s Pos[1] double 0.01 run scoreboard players get #t bm.rng',
                           'playsound minecraft:block.wood.fall block @a[distance=..20] ~ ~ ~ 1 0.6'])
    fn('p91/girder/hit', ['damage @s 4 minecraft:generic', 'playsound minecraft:entity.zombie.break_wooden_door hostile @a[distance=..16] ~ ~ ~ 0.8 1.2',
                          'particle minecraft:block{block_state:"minecraft:barrel"} ~ ~0.5 ~ 0.3 0.3 0.3 0 16', title('@s', 'actionbar', T('BONK! Jump the barrels!', '#ff6a4a', bold=True)),
                          'kill @e[type=minecraft:block_display,tag=bm.gvbar,distance=..1.5,limit=1,sort=nearest]'])
    fn('p91/girder/cleared', ['tag @e[type=minecraft:block_display,tag=bm.gvbar,distance=..2.5,limit=1,sort=nearest] add bm.gvjmpd', 'scoreboard players set #c bm.rng 1',
                              inst('bm:p75/pot_add'), title('@s', 'actionbar', T('Jumped it! +1 coin', GOLD, bold=True)),
                              'playsound minecraft:entity.experience_orb.pickup player @a[distance=..6] ~ ~ ~ 0.6 1.6'])
    fn('p91/girder/done', ['scoreboard players set @s bm.gvs 2', 'kill @e[type=minecraft:block_display,tag=bm.gvbar,distance=..30]',
                           'execute as @e[type=minecraft:item_display,tag=bm.gvgrat,distance=..30] at @s run particle minecraft:poof ~ ~1 ~ 0.4 0.6 0.4 0.02 20',
                           'kill @e[type=minecraft:item_display,tag=bm.gvgrat,distance=..30]'] + pot(6) +
       big('TOP OF THE GIRDERS!', 'The rat bolts. The way on is open (a ladder down by the exit).', '#ff6a4a') + ['function bm:p70/solved'])

    # ================================================================== THE MEAD HALL (waves, then the Jarl)
    VK = lambda extra=(): {'Tags': ['bm.gvg', 'bm.gvnew2', 'bm.tiered', 'bm.seen', 'bm.gvwv'] + list(extra)}
    raider = mk('vindicator', 'Viking Raider', '#c8a060', {'head': 'minecraft:iron_helmet', 'mainhand': 'minecraft:iron_axe'}, VK())
    berserk = mk('vindicator', 'Berserker', '#ff5a3a', {'mainhand': 'minecraft:stone_axe'}, VK(), {'movement_speed': 0.42, 'attack_damage': 7.0})
    maiden = mk('zombie', 'Shieldmaiden', '#c0d0e0', {'head': 'minecraft:chainmail_helmet', 'chest': 'minecraft:iron_chestplate', 'mainhand': 'minecraft:iron_sword',
                                                       'offhand': 'minecraft:shield'}, dict(VK(), IsBaby=B(0), CanBreakDoors=B(0)), {'armor': 8.0, 'spawn_reinforcements': 0.0})
    thrower = mk('pillager', 'Axe Thrower', '#c8a060', {'head': 'minecraft:leather_helmet', 'mainhand': 'minecraft:crossbow'}, VK())
    jarl = mk('vindicator', 'Jarl Ironbeard', '#ffd040', {'head': {'id': 'minecraft:golden_helmet', 'count': Int(1), 'components': {'minecraft:enchantment_glint_override': True}},
                                                          'chest': 'minecraft:iron_chestplate', 'mainhand': {'id': 'minecraft:diamond_axe', 'count': Int(1),
                                                                                                           'components': {'minecraft:enchantment_glint_override': True}}},
              dict(VK(('bm.gvcap',)), CustomNameVisible=B(1)), {'scale': 1.4, 'attack_damage': 9.0})
    carl = mk('zombie', 'Housecarl', '#a0a0b0', {'head': 'minecraft:iron_helmet', 'chest': 'minecraft:iron_chestplate', 'legs': 'minecraft:iron_leggings', 'mainhand': 'minecraft:iron_axe'},
              dict(VK(), IsBaby=B(0), CanBreakDoors=B(0)), {'spawn_reinforcements': 0.0})
    def spawn(m, x, z):
        return [f'execute positioned {rel(x, 4, z)} run summon minecraft:{m[0]} ~ ~ ~ {snbt(m[1])}', f'execute positioned {rel(x, 4, z)} run function bm:p70/guard_set']
    SP = [(5, 9), (19, 9), (5, 15), (19, 15), (12, 4), (12, 20), (8, 12), (16, 12)]
    w1 = sum((spawn(raider, x, z) for (x, z) in SP[:4]), []) + ['execute if score #gt bm.rng matches 3.. run ' + l for l in spawn(raider, *SP[4])]
    w2 = sum((spawn(berserk, x, z) for (x, z) in SP[:2]), []) + sum((spawn(maiden, x, z) for (x, z) in SP[2:4]), []) + \
        ['execute if score #gt bm.rng matches 3.. run ' + l for l in spawn(thrower, *SP[5])]
    w3 = spawn(jarl, 12, 18) + ['execute if score #gt bm.rng matches 4.. run ' + l for l in spawn(carl, *SP[6]) + spawn(carl, *SP[7])]
    fn('p91/mead/init', ['function bm:p70/ctx', sign(2.5, 7.5, 12, 'THE MEAD HALL', 'The raiders are back from the sea. Beat them, then their Jarl.', '#ffd040')])
    fn('p91/mead/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'scoreboard players set @a[tag=bm.gvp,distance=..15] bm.gvmz 5',
                         'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..9] run function bm:p91/mead/wave',
                         'execute unless score @s bm.gvs matches 1 run return 0',
                         'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #20 bm.rng', 'execute unless score #q bm.rng matches 0 run return 0',
                         'execute store result score #n bm.rng if entity @e[tag=bm.gvwv,distance=..18]',
                         'execute if score #n bm.rng matches 0 if score @s bm.gvw matches 3.. run return run function bm:p91/mead/done',
                         'execute if score #n bm.rng matches 0 run function bm:p91/mead/wave'])
    fn('p91/mead/wave', ['function bm:p70/ctx', 'scoreboard players set @s bm.gvs 1', 'scoreboard players add @s bm.gvw 1',
                         'execute if score @s bm.gvw matches 1 run function bm:p91/mead/w1', 'execute if score @s bm.gvw matches 2 run function bm:p91/mead/w2',
                         'execute if score @s bm.gvw matches 3 run function bm:p91/mead/w3', 'playsound minecraft:event.raid.horn hostile @a[distance=..30] ~ ~ ~ 0.8 1',
                         'execute if score @s bm.gvw matches 1 run ' + title(crew, 'actionbar', T('The horn sounds - raiders!', '#ffd040')),
                         'execute if score @s bm.gvw matches 2 run ' + title(crew, 'actionbar', T('Berserkers and shieldmaidens!', '#ff5a3a'))] +
       ['execute if score @s bm.gvw matches 3 run ' + l for l in big('JARL IRONBEARD', 'He wants his mead hall back.', '#ffd040')])
    fn('p91/mead/w1', w1); fn('p91/mead/w2', w2); fn('p91/mead/w3', w3)
    fn('p91/mead/done', ['scoreboard players set @s bm.gvs 2'] + pot(8) + big('SKÅL!', 'The Jarl is down. The way on is open.', '#ffd040') +
       [f'effect give {crew} minecraft:regeneration 8 1', 'function bm:p70/solved'])

    # ================================================================== THE TALL GRASS (catching critters)
    CRIT = [('rabbit', 'Hopper', '#d8c8a8', {}), ('fox', 'Embertail', '#ff8a3a', {}), ('frog', 'Croaker', '#7ad050', {}), ('armadillo', 'Rollbud', '#c89a7a', {}),
            ('rabbit', 'Snowpuff', '#ffffff', {'RabbitType': Int(2)}), ('ocelot', 'Spotsy', '#e0c060', {})]
    def crit(i, x, z):
        ty, nm, col, extra = CRIT[i % len(CRIT)]
        d = dict({'Tags': ['bm.gvprop', 'bm.gvcrit'], 'PersistenceRequired': B(1), 'Invulnerable': B(1), 'CustomName': T(nm, col, bold=True), 'CustomNameVisible': B(1)}, **extra)
        return f'summon minecraft:{ty} {rel(x, 4, z)} {snbt(d)}'
    CRIT_SPOTS = [(8, 5), (16, 6), (6, 18), (17, 17), (12, 8), (20, 12), (10, 20), (14, 16)]
    wild = {1: mk('zombie', 'Wild Zombie', '#7a9a5a', {}, {'IsBaby': B(0)}, {'spawn_reinforcements': 0.0}), 2: mk('spider', 'Wild Spider', '#8a6a6a', {}),
            3: mk('skeleton', 'Wild Skeleton', '#d0d0d0', {'mainhand': 'minecraft:bow'}), 4: mk('witch', 'Wild Witch', '#b080ff', {})}
    fn('p91/grass/init', ['function bm:p70/ctx'] + [crit(i, x, z) for i, (x, z) in enumerate(CRIT_SPOTS[:6])] +
       [f'summon minecraft:interaction {rel(3, 5, 9)} ' + snbt({'Tags': ['bm.gvprop', 'bm.gvctr'], 'width': F(1.2), 'height': F(1.2), 'response': B(1)}),
        label(3.5, 6.8, 9, [T('RAT CENTER\n', '#ff5a5a', bold=True), T('Right-click: 3 Rat Balls', 'gray')], 0.5),
        sign(2.5, 7.5, 12, 'THE TALL GRASS', 'Throw Rat Balls (snowballs) at the critters to catch them. Mind what else is in the grass.', '#7ad050')])
    ball = loan('minecraft:snowball', 6, ',minecraft:custom_name=' + snbt(T('Rat Ball', '#ff5a5a')))
    fn('p91/grass/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'scoreboard players set @a[tag=bm.gvp,distance=..15] bm.gvmz 9',
                          'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..10] run function bm:p91/grass/start',
                          'execute unless score @s bm.gvs matches 1 run return 0',
                          'execute as @e[type=minecraft:snowball,distance=..20] at @s if entity @e[tag=bm.gvcrit,distance=..1.6] run function bm:p91/grass/catch',
                          'execute as @e[type=minecraft:interaction,tag=bm.gvctr,distance=..16] if data entity @s interaction at @s run function bm:p91/grass/center',
                          'execute if score @s bm.gvw >= @s bm.gvc run return run function bm:p91/grass/done',
                          'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #20 bm.rng', 'execute unless score #q bm.rng matches 0 run return 0',
                          'execute as @e[tag=bm.gvcrit,distance=..40] unless entity @s[distance=..13] run tp @s ~ ~ ~',
                          'execute store result score #n bm.rng if entity @e[tag=bm.gvcrit,distance=..16]', 'scoreboard players operation #need bm.rng = @s bm.gvc',
                          'scoreboard players operation #need bm.rng -= @s bm.gvw', 'execute if score #n bm.rng < #need bm.rng run function bm:p91/grass/more',
                          'execute as @a[tag=bm.gvp,distance=..14] at @s if block ~ ~ ~ minecraft:tall_grass if predicate bm:p91/wild run function bm:p91/grass/wild'])
    wjson('bm/predicate/p91/wild.json', {'condition': 'minecraft:random_chance', 'chance': 0.05})
    fn('p91/grass/start', ['function bm:p70/ctx', 'scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvw 0',
                           'execute store result score @s bm.gvc if entity @a[tag=bm.gvp,distance=..20]', 'scoreboard players add @s bm.gvc 3',
                           'execute as @a[tag=bm.gvp,distance=..16] run give @s ' + ball] +
       big('THE TALL GRASS', 'Catch the critters - throw your Rat Balls!', '#7ad050'))
    fn('p91/grass/catch', ['execute as @e[tag=bm.gvcrit,distance=..1.6,limit=1,sort=nearest] at @s run function bm:p91/grass/caught', 'kill @s'])
    fn('p91/grass/caught', ['particle minecraft:dust{color:[1.0,0.3,0.3],scale:1.2} ~ ~0.5 ~ 0.3 0.3 0.3 0 20', 'particle minecraft:end_rod ~ ~0.5 ~ 0.2 0.2 0.2 0.05 10',
                            'playsound minecraft:entity.chicken.egg neutral @a[distance=..20] ~ ~ ~ 1 1.6', 'playsound minecraft:block.note_block.chime neutral @a[distance=..20] ~ ~ ~ 1 1.8',
                            tellraw('@a[tag=bm.gvp,distance=..20]', [T('Gotcha! ', '#ff5a5a', bold=True), {'selector': '@s'}, T(' was caught!', 'gray')]),
                            'execute as @e[type=minecraft:marker,tag=bm.gvr_grass,distance=..30,limit=1,sort=nearest] run scoreboard players add @s bm.gvw 1',
                            'scoreboard players set #c bm.rng 1', inst('bm:p75/pot_add'), 'tp @s ~ -200 ~', 'kill @s'])
    fn('p91/grass/more', ['execute store result score #r bm.rng run random value 0..7'] +
       [f'execute if score #r bm.rng matches {i} run ' + crit(i + 2, x, z) for i, (x, z) in enumerate(CRIT_SPOTS)])
    fn('p91/grass/center', ['execute on target at @s run function bm:p91/grass/center2', 'data remove entity @s interaction'])
    fn('p91/grass/center2', ['execute store result score #now bm.rng run time query gametime', 'execute if score @s bm.gvbc > #now bm.rng run return run ' +
                             title('@s', 'actionbar', T('The Rat Center is restocking - try again in a little while.', 'gray')),
                             'scoreboard players operation @s bm.gvbc = #now bm.rng', 'scoreboard players add @s bm.gvbc 300',
                             'give @s ' + loan('minecraft:snowball', 3, ',minecraft:custom_name=' + snbt(T('Rat Ball', '#ff5a5a'))),
                             'playsound minecraft:entity.item.pickup player @s ~ ~ ~ 1 1.2'])
    fn('p91/grass/wild', ['execute store result score #n bm.rng if entity @e[tag=bm.gvg,distance=..20]', 'execute if score #n bm.rng matches 3.. run return 0',
                          'function bm:p70/ctx', 'scoreboard players set #wt bm.rng 1', 'execute if score #gt bm.rng matches 2 run scoreboard players set #wt bm.rng 2',
                          'execute if score #gt bm.rng matches 3 run scoreboard players set #wt bm.rng 3', 'execute if score #gt bm.rng matches 4.. run scoreboard players set #wt bm.rng 4'] +
       [f'execute if score #wt bm.rng matches {t} positioned ^ ^ ^2 run summon minecraft:{m[0]} ~ ~ ~ {snbt(m[1])}' for t, m in wild.items()] +
       ['execute positioned ^ ^ ^2 run function bm:p70/guard_set',
        'execute as @e[tag=bm.gvg,distance=..4,limit=1,sort=nearest] run ' + title('@a[tag=bm.gvp,distance=..12]', 'actionbar', [T('A wild ', '#7ad050'), {'selector': '@s'},
                                                                                                                                T(' appeared!', '#7ad050')]),
        'playsound minecraft:block.grass.break hostile @a[distance=..12] ~ ~ ~ 1 0.6'])
    fn('p91/grass/done', ['scoreboard players set @s bm.gvs 2', 'execute as @e[tag=bm.gvcrit,distance=..20] at @s run particle minecraft:poof ~ ~0.5 ~ 0.2 0.2 0.2 0.02 6',
                          'tp @e[tag=bm.gvcrit,distance=..20] ~ -200 ~', 'kill @e[tag=bm.gvcrit]'] + pot(6) +
       big('GOTTA CATCH \'EM!', 'Enough critters caught - the way on is open.', '#7ad050') + ['function bm:p70/solved'])

    # admin: lay one of these rooms next
    EVENTS = [k for k in P75.EXTRA_ROOMS if k not in P75.KINDS]
    for k in ks:
        fn(f'admin/room_{k}', [f'scoreboard players set #frm bm.gvv {EVENTS.index(k) + 1}', tellraw('@s', P + [T(f'The next event room drawn is {NAMES[k]}.', 'gray')])])

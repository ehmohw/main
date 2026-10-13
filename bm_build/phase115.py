"""2.72: FIVE NEW ROOMS, three ways each - the Library, the Pipes, the Apothecary, the Grapple, and the Minecart Run.

THE LIBRARY (puzzle)     a wall of 36 books. Pull a book: right-click it. A wrong pull rings the alarm and every book slides back.
    A  THE CATALOGUE  the card on the desk names two to four books (more at higher tiers): find them by their titles and pull them
    B  THE ACROSTIC   the desk has a riddle; each book has a letter - pull the books that spell the answer, first letter first
    C  THE SUM        twelve books carry numbers: pull three, one from each of three shelves, that add up to the desk's number
THE PIPES (puzzle)       a 5x5 grid of pipe pieces; water comes in at the west and must leave at the east (pieces carrying water
                         turn blue as you go). Right-click a piece to work it.
    A  TURN           each click turns a piece a quarter round
    B  SWAP           the pieces don't turn: click one, then another, and they swap places
    C  GAUGES         turn them - and the water must pass through both gold gauges on its way
THE APOTHECARY (puzzle, Tiers II-V)  three brewing stands, water bottles, blaze powder and a shelf of ingredients (some you won't
                         need). Brew what the Fixer wants and hand it in at his hatch. A wrong potion rings the alarm.
    A  THE ORDER      he names the potion
    B  THE RIDDLE     he describes what it does - work out which potion that is
    C  THE TINCTURE   he names it with its modifiers: longer, stronger, a splash, or turned (the fermented eye)
THE GRAPPLE (puzzle, Tiers II-V)  the Fixer lends a grappling hook that bites only the lamps (target blocks), and reaches nine
                         blocks. Hook a lamp and you hang beneath it; let go (sneak) and you drop. Fall into the hay: back to the
                         start. (The hook works only in its own room.)
    A  THE CHASM      islands over a pit and a lamp over each - and only so many hooks (two or three): find a way across with
                      what you're given (some gaps you can jump)
    B  THE SWINGING LAMPS  the lamps swing to and fro over the pit: hook each one as it swings over its island
    C  THE BELLS      four bells across the gap: ring them with the hook, in the order the mural shows, and the bridge comes out
THE MINECART RUN (event) carts on rails over a pit; get in at the station and you're off. Fall: back to the station.
    A  THE RAIL SHOOTER   hit enough of the targets beside the track on one ride (5 + the tier; a bow is lent)
    B  THE SWITCH YARD    three sets of points, set by the levers at the station: only one way reaches the gold station
    C  THE DRAWBRIDGES    three gaps in the track: a button beside the rails closes each one for two seconds
"""
import math
import random
from items import T
from nbt import snbt, B, F, Int
from structures import Build
import phase70_rooms as RM
import phase75 as P75
import phase75_rooms as R5
import phase76_rooms as R6
from phase75_rooms import BASE, wall_glow
import phase110 as P110
import p115data as PD

GOLD = '#ffcf40'
BOOK = '#c8a070'
rel, relf, IDENT = RM.rel, P110.relf, P110.IDENT
FY = RM.FY
W, D = 25, 25
NAMES = {'library': 'The Library', 'pipes': 'The Pipes', 'apoth': 'The Apothecary', 'grapple': 'The Grapple', 'minecart': 'The Minecart Run'}


def _pit(b, x0, x1):
    """an open pit with hay at the bottom between x0 and x1 (the whole width of the room)"""
    for x in range(x0, x1 + 1):
        for z in range(1, 24):
            b.set(x, 0, z, 'minecraft:hay_block')
            for y in range(1, 6): b.set(x, y, z, 'minecraft:air')


def library():
    b = R6.shell()
    for x in range(3, 22):
        for y in range(4, 10): b.set(x, y, 1, 'minecraft:bookshelf')
    for x in range(10, 15): b.set(x, 4, 6, 'minecraft:dark_oak_planks')
    b.set(12, 5, 6, 'minecraft:lectern[facing=south]')
    for (x, z) in ((3, 3), (21, 3)):
        b.set(x, 4, z, 'minecraft:air'); b.set(x + 1, 4, z, 'minecraft:air'); b.set(x, 5, z, 'minecraft:air')
    R6.ctrl(b, 'library'); return wall_glow(b)


def pipes():
    b = R6.shell()
    for x in range(6, 19):
        for z in range(6, 19): b.set(x, FY, z, BASE['floor'])
    for x in range(7, 18):
        for z in range(7, 18): b.set(x, FY, z, 'minecraft:smooth_stone')
    R6.ctrl(b, 'pipes'); return wall_glow(b)


def apoth():
    b = R6.shell()
    for x in range(5, 20): b.set(x, 4, 20, 'minecraft:dark_oak_planks')
    for x in (8, 12, 16): b.set(x, 5, 20, 'minecraft:brewing_stand')
    for x in (5, 19): b.set(x, 5, 20, 'minecraft:water_cauldron[level=3]')
    for x in range(4, 21):
        b.set(x, 6, 23, 'minecraft:spruce_slab[type=top]'); b.set(x, 8, 23, 'minecraft:spruce_slab[type=top]')
    b.set(12, 4, 2, 'minecraft:barrel[facing=south]')
    for x in (11, 13): b.set(x, 4, 2, BASE['metal']); b.set(x, 5, 2, BASE['metal'])
    b.set(12, 6, 2, BASE['metal'])
    for x in (10, 14): b.set(x, 5, 20, 'minecraft:barrel[facing=up]')          # (2.75: the supply barrels - phase126 keeps them stocked)
    R6.ctrl(b, 'apoth'); return wall_glow(b)


def grapple():
    b = R6.shell()
    _pit(b, 4, 22)
    for (x, z) in ((3, 3), (3, 21)):
        for y in (4, 5): b.set(x, y, z, 'minecraft:air')
        b.set(x + 1, 4, z, 'minecraft:air')
    R6.ctrl(b, 'grapple'); return wall_glow(b)


def minecart():
    b = R6.shell()
    _pit(b, 4, 20)
    for (x, z) in ((3, 3), (3, 21), (21, 3), (21, 21)):
        for y in (4, 5): b.set(x, y, z, 'minecraft:air')
        b.set(x + 1, 4, z, 'minecraft:air')
    b.set(2, 4, 12, BASE['pillar'])
    R6.ctrl(b, 'minecart'); return wall_glow(b)


PUZ = {'library': library, 'pipes': pipes, 'apoth': apoth, 'grapple': grapple}
EVS = {'minecart': minecart}
P75.KINDS += list(PUZ)
for _k, _f in list(PUZ.items()) + list(EVS.items()):
    P75.EXTRA_ROOMS[_k] = _f
    R6.NAMES[_k] = NAMES[_k]
for _t in range(1, 6):
    P75.TIER_POOL[_t] += ['library', 'pipes'] + (['apoth', 'grapple'] if _t >= 2 else [])
    P75.EVENT_POOL[_t] += ['minecart']
P110.TRAV += ['grapple', 'minecart']

BREW_A, RIDDLE_B, BREW_B, BREW_C, INGR, DECOY = PD.BREW_A, PD.RIDDLE_B, PD.BREW_B, PD.BREW_C, PD.INGR, PD.DECOY


def generate(G):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    label, sign, vbutton, press, themed, crew_say, oops, choose = P110.helpers(G)
    inst = lambda f: f'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run function {f}'
    crew = '@a[tag=bm.gvp,distance=..30]'
    pot = lambda n: [f'scoreboard players set #c bm.rng {n}', inst('bm:p75/pot_add')]
    objs = ['bm.lq0', 'bm.lq1', 'bm.lq2', 'bm.lq3', 'bm.lq4', 'bm.pr', 'bm.pc', 'bm.gvhk', 'bm.gvhr', 'bm.gvhu', 'bm.gvhb', 'bm.gvhq']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    def room_item(i, extra=''):
        return f'minecraft:{i}[minecraft:custom_data={{bm_room:1b}}{extra}]'
    def disp(blk, pos, sc, tags, tr=(0, 0, 0), extra=None):
        d = {'Tags': ['bm.gvprop'] + tags, 'block_state': blk, 'brightness': {'block': 15, 'sky': 15},
             'transformation': {'left_rotation': IDENT, 'right_rotation': IDENT, 'translation': [F(v) for v in tr], 'scale': [F(v) for v in sc]}}
        if extra: d.update(extra)
        return f'summon minecraft:block_display {pos} ' + snbt(d)
    def big(t_, sub, col='#7ad0ff', who=crew):
        return [f'title {who} times 5 40 10', title(who, 'title', T(t_, col, bold=True)), title(who, 'subtitle', T(sub, 'gray'))]
    def var_init(k, a, b, c):
        return ['function bm:p70/ctx', 'function bm:p110/var', f'execute if score @s bm.gvvar matches 1 run return run function bm:{b}',
                f'execute if score @s bm.gvvar matches 2 run return run function bm:{c}', f'function bm:{a}']

    # ================================================================== dispatch, names, tags
    ks = list(PUZ) + list(EVS)
    G.FUNCS['p70/r/init'] += [f'execute if entity @s[tag=bm.gvr_{k}] run return run function bm:p115/{k}/init' for k in ks]
    G.FUNCS['p70/r/tick'] += [f'execute if entity @s[tag=bm.gvr_{k}] run return run function bm:p115/{k}/tick' for k in ks]
    k0 = next(i for i, l in enumerate(G.FUNCS['p70/r/init']) if 'tag @s add bm.gvnopick' in l)
    G.FUNCS['p70/r/init'][k0:k0] = [f'execute if entity @s[tag=bm.gvr_{k}] run tag @s add bm.gvnopick' for k in EVS] + \
                                   [f'execute if entity @s[tag=bm.gvr_{k}] run tag @s add bm.gvpuz' for k in PUZ]
    G.FUNCS['p70/solved'] += [f'execute if entity @s[tag=bm.gvr_{k}] as @a[tag=bm.gvp,distance=..300] if score @s bm.gvi = #gi bm.rng run ' +
                              title('@s', 'actionbar', [T(NAMES[k], GOLD, bold=True), T(' - beaten. The way on is open.', 'gray')]) for k in ks] + \
                             [f'execute if entity @s[tag=bm.gvr_{k}] if score @s bm.gvf matches 0 run function bm:p76/flawless' for k in PUZ]
    EVALL = [k for k in P75.EXTRA_ROOMS if k not in P75.KINDS]
    fn('admin/room_minecart', [f'scoreboard players set #frm bm.gvv {EVALL.index("minecart") + 1}', tellraw('@s', [T('The next event room drawn is The Minecart Run.', 'gray')])])

    # ================================================================== THE LIBRARY
    BCOL = ['red', 'blue', 'green', 'brown', 'purple', 'cyan', 'orange', 'black']
    rngc = random.Random(7210)
    COLS = [rngc.choice(BCOL) for _ in range(36)]
    def books(vals, words):
        L = []
        for i, (x, y) in enumerate(PD.LSLOTS):
            L.append(disp(f'minecraft:{COLS[i]}_wool', relf(x + 0.36, y + 0.08, 1.88), (0.28, 0.78, 0.36), ['bm.gvbkd'],
                          extra={'interpolation_duration': Int(4)}))
            L.append(f'summon minecraft:interaction {relf(x + 0.5, y, 2.2)} {{Tags:["bm.gvprop","bm.gvbk","bm.gvbkn"],width:0.62f,height:0.95f,response:1b}}')
            L.append(f'scoreboard players set @e[type=minecraft:interaction,tag=bm.gvbkn,limit=1] bm.gvy1 {i}')
            L.append(f'scoreboard players set @e[type=minecraft:interaction,tag=bm.gvbkn,limit=1] bm.gvy2 {vals[i]}')
            L.append(f'scoreboard players set @e[type=minecraft:interaction,tag=bm.gvbkn,limit=1] bm.gvy3 {i // 9}')
            L.append('tag @e[type=minecraft:interaction,tag=bm.gvbkn] remove bm.gvbkn')
            if words[i]:
                L.append(label(relf(x + 0.5, y + 0.86, 2.25), T(words[i], '#f0e0c0', bold=True), 0.26, 'center', width=120, bg=False))
        return L
    fn('p115/library/init', var_init('library', 'p115/library/a', 'p115/library/b', 'p115/library/c'))
    for v in 'abc':
        n = 8
        fn(f'p115/library/{v}', ['scoreboard players set @s bm.gvw 0', 'scoreboard players set @s bm.gvy3 0'] + choose('#i', n, f'p115/library/{v}') +
           ['scoreboard players operation @s bm.gvc = #i bm.rng'])
    for j, (words, tg) in enumerate(PD.LIB_A):
        vals = [0] * 36
        for rank, s in enumerate(tg): vals[s] = rank + 1
        fn(f'p115/library/a{j}', books(vals, words) +
           ['scoreboard players set @s bm.gvx 2', 'execute if score #gt bm.rng matches 3.. run scoreboard players set @s bm.gvx 3',
            'execute if score #gt bm.rng matches 5 run scoreboard players set @s bm.gvx 4'] +
           [f'execute if score @s bm.gvx matches {n_} run ' + sign(rel(12, 7.4, 6), 'THE CATALOGUE', 'The Fixer wants these books pulled (right-click them) - and no others:\n' +
                                                            ', '.join(words[s] for s in tg[:n_]), 0.6) for n_ in (2, 3, 4)])
    for j, (riddle, ans, letters) in enumerate(PD.LIB_B):
        vals = [ord(ch) - 64 for ch in letters]
        fn(f'p115/library/b{j}', books(vals, letters) + [f'scoreboard players set @s bm.gvx {len(ans)}'] +
           [f'scoreboard players set @s bm.lq{k} {ord(ch) - 64}' for k, ch in enumerate(ans[:5])] +
           [sign(rel(12, 7.4, 6), 'THE ACROSTIC', f'"{riddle}" Pull the books that spell the answer - first letter first.', 0.6)])
    for j, (nums, tgt, _t3) in enumerate(PD.LIB_C):
        vals = [nums.get(s, 0) for s in range(36)]
        fn(f'p115/library/c{j}', books(vals, [str(nums[s]) if s in nums else '' for s in range(36)]) + [f'scoreboard players set @s bm.gvz {tgt}', 'scoreboard players set @s bm.gvx 3'] +
           [sign(rel(12, 7.4, 6), 'THE SUM', f'Pull three numbered books - one from each of three different shelves - that add up to {tgt}.', 0.6)])
    fn('p115/library/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'execute if score @s bm.gvs matches 0 run scoreboard players set @s bm.gvs 1',
                             'execute if score @s bm.gvtm matches 3000 run scoreboard players set @s bm.gvf 1',
                             'execute as @e[type=minecraft:interaction,tag=bm.gvbk,distance=..20] if data entity @s interaction at @s run function bm:p115/library/click'])
    fn('p115/library/click', ['data remove entity @s interaction', 'execute if entity @s[tag=bm.gvbkp] run return 0', 'tag @s add bm.gvbkp',
                              'execute as @e[type=minecraft:block_display,tag=bm.gvbkd,distance=..0.9,sort=nearest,limit=1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0f,0f,0.42f]}}',
                              'playsound minecraft:item.book.page_turn block @a[distance=..16] ~ ~ ~ 1 1', 'scoreboard players operation #val bm.rng = @s bm.gvy2',
                              'execute as @e[type=minecraft:marker,tag=bm.gvr_library,distance=..20,sort=nearest,limit=1] at @s run function bm:p115/library/judge'])
    fn('p115/library/judge', ['execute if score @s bm.gvvar matches 1 run return run function bm:p115/library/jb',
                              'execute if score @s bm.gvvar matches 2 run return run function bm:p115/library/jc',
                              'execute unless score #val bm.rng matches 1.. run return run function bm:p115/library/wrong',
                              'execute if score #val bm.rng > @s bm.gvx run return run function bm:p115/library/wrong',
                              'scoreboard players add @s bm.gvw 1', 'execute if score @s bm.gvw >= @s bm.gvx run function bm:p115/library/won'])
    fn('p115/library/jb', [f'execute if score @s bm.gvw matches {k} unless score #val bm.rng = @s bm.lq{k} run return run function bm:p115/library/wrong' for k in range(5)] +
       ['scoreboard players add @s bm.gvw 1', 'execute if score @s bm.gvw >= @s bm.gvx run function bm:p115/library/won'])
    fn('p115/library/jc', ['execute unless score #val bm.rng matches 1.. run return run function bm:p115/library/wrong', 'scoreboard players operation @s bm.gvy3 += #val bm.rng',
                           'scoreboard players add @s bm.gvw 1', 'execute if score @s bm.gvw matches ..2 run return 0'] +
       [f'execute store result score #r{r} bm.rng if entity @e[type=minecraft:interaction,tag=bm.gvbkp,distance=..20,scores={{bm.gvy3={r}}}]' for r in range(4)] +
       [f'execute if score #r{r} bm.rng matches 2.. run return run function bm:p115/library/wrong' for r in range(4)] +
       ['execute unless score @s bm.gvy3 = @s bm.gvz run return run function bm:p115/library/wrong', 'function bm:p115/library/won'])
    fn('p115/library/wrong', ['scoreboard players set @s bm.gvw 0', 'scoreboard players set @s bm.gvy3 0', 'scoreboard players set @s bm.gvf 1',
                              'tag @e[type=minecraft:interaction,tag=bm.gvbkp,distance=..20] remove bm.gvbkp',
                              'execute as @e[type=minecraft:block_display,tag=bm.gvbkd,distance=..20] run data merge entity @s {start_interpolation:0,transformation:{translation:[0f,0f,0f]}}',
                              'playsound minecraft:block.chiseled_bookshelf.insert block @a[distance=..20] ~ ~ ~ 1 0.6',
                              crew_say([T('Wrong book! ', 'red', bold=True), T('They all slide back - and the alarm rings.', 'gray')], r=24)] + oops(2))
    fn('p115/library/won', big('THE SHELF SWINGS OPEN', 'The right books - the way on is open.', BOOK) + pot(4) + ['function bm:p70/solved'])

    # ================================================================== THE PIPES
    CX = lambda c: 8 + 2 * c
    CZ = lambda r: 8 + 2 * r
    fn('p115/pipes/init', var_init('pipes', 'p115/pipes/a', 'p115/pipes/b', 'p115/pipes/c'))
    def pipe_set(rs, rd, grid, gauges=()):
        L = [f'scoreboard players set @s bm.gvx {rs}', f'scoreboard players set @s bm.gvz {rd}',
             disp('minecraft:light_blue_concrete', relf(5.6, 4.02, CZ(rs) + 0.4), (1.8, 0.2, 0.2), ['bm.gvpsrc']),
             disp('minecraft:waxed_copper_block', relf(18.6, 4.02, CZ(rd) + 0.4), (1.8, 0.2, 0.2), ['bm.gvpsrc']),
             label(relf(5.2, 4.8, CZ(rs) + 0.5), T('IN', '#7ad0ff', bold=True), 0.5), label(relf(19.8, 4.8, CZ(rd) + 0.5), T('OUT', '#7ad0ff', bold=True), 0.5)]
        for (r, c), (t, k) in grid.items():
            L += [f'summon minecraft:marker {relf(CX(c) + 0.5, 4, CZ(r) + 0.5)} {{Tags:["bm.gvprop","bm.gvpcell","bm.gvpn"]}}',
                  f'summon minecraft:interaction {relf(CX(c) + 0.5, 4, CZ(r) + 0.5)} {{Tags:["bm.gvprop","bm.gvpint"],width:1.3f,height:0.5f,response:1b}}',
                  f'scoreboard players set @e[type=minecraft:marker,tag=bm.gvpn,limit=1] bm.pr {r}', f'scoreboard players set @e[type=minecraft:marker,tag=bm.gvpn,limit=1] bm.pc {c}',
                  f'scoreboard players set @e[type=minecraft:marker,tag=bm.gvpn,limit=1] bm.gvy1 {t}', f'scoreboard players set @e[type=minecraft:marker,tag=bm.gvpn,limit=1] bm.gvy2 {k}']
            if (r, c) in gauges:
                L += ['tag @e[type=minecraft:marker,tag=bm.gvpn,limit=1] add bm.gvpg', disp('minecraft:gold_block', relf(CX(c) + 0.1, 3.99, CZ(r) + 0.1), (0.8, 0.03, 0.8), [])]
            L.append('tag @e[type=minecraft:marker,tag=bm.gvpn] remove bm.gvpn')
        return L + ['function bm:p115/pipes/flow']
    for v, P in (('a', PD.PIPE_A), ('b', PD.PIPE_B), ('c', PD.PIPE_C)):
        fn(f'p115/pipes/{v}', choose('#i', len(P), f'p115/pipes/{v}') + ['scoreboard players operation @s bm.gvc = #i bm.rng'] +
           [sign(rel(12, 8.2, 3), {'a': 'THE PIPES', 'b': 'THE PIPES - SWAP', 'c': 'THE PIPES - GAUGES'}[v],
                 {'a': 'Run the water from IN to OUT. Right-click a piece to turn it.',
                  'b': 'Run the water from IN to OUT. The pieces won\'t turn: click one, then another, and they swap.',
                  'c': 'Run the water from IN to OUT - through both gold gauges. Right-click a piece to turn it.'}[v], 0.6)])
        for j, p in enumerate(P):
            fn(f'p115/pipes/{v}{j}', pipe_set(p[0], p[1], p[2], p[4] if v == 'c' else ()))
    # the openings of a piece: type 0 straight (N+S at turn 0), 1 corner (N+E at turn 0); each turn a quarter clockwise
    om = ['tag @s remove bm.po_n', 'tag @s remove bm.po_e', 'tag @s remove bm.po_s', 'tag @s remove bm.po_w']
    for t in (0, 1):
        for k in range(4):
            m = PD.mask(t, k)
            for bit, nm in ((PD.N_, 'n'), (PD.E_, 'e'), (PD.S_, 's'), (PD.W_, 'w')):
                if m & bit: om.append(f'execute if score @s bm.gvy1 matches {t} if score @s bm.gvy2 matches {k} run tag @s add bm.po_{nm}')
    fn('p115/pipes/mask', om)
    cells = '@e[type=minecraft:marker,tag=bm.gvpcell,distance=..12]'
    fn('p115/pipes/flow', [f'execute as {cells} run function bm:p115/pipes/mask', f'tag {cells} remove bm.gvwet',
                           'scoreboard players operation #rs bm.rng = @s bm.gvx', 'scoreboard players operation #rd bm.rng = @s bm.gvz',
                           f'execute as {cells} if score @s bm.pc matches 0 if score @s bm.pr = #rs bm.rng if entity @s[tag=bm.po_w] at @s run function bm:p115/pipes/visit',
                           f'execute as {cells} at @s run function bm:p115/pipes/draw',
                           'scoreboard players set #ok bm.rng 0',
                           f'execute as {cells} if score @s bm.pc matches 4 if score @s bm.pr = #rd bm.rng if entity @s[tag=bm.gvwet,tag=bm.po_e] run scoreboard players set #ok bm.rng 1',
                           'execute if entity @e[type=minecraft:marker,tag=bm.gvpg,tag=!bm.gvwet,distance=..12] run scoreboard players set #ok bm.rng 0',
                           'execute if score #ok bm.rng matches 1 if score @s bm.gvs matches ..2 run function bm:p115/pipes/won'])
    nb = '@e[type=minecraft:marker,tag=bm.gvpcell,tag=!bm.gvwet,distance=..0.5,limit=1]'
    fn('p115/pipes/visit', ['tag @s add bm.gvwet',
                            f'execute if entity @s[tag=bm.po_n] positioned ~ ~ ~-2 as {nb.replace("tag=!bm.gvwet", "tag=!bm.gvwet,tag=bm.po_s")} at @s run function bm:p115/pipes/visit',
                            f'execute if entity @s[tag=bm.po_s] positioned ~ ~ ~2 as {nb.replace("tag=!bm.gvwet", "tag=!bm.gvwet,tag=bm.po_n")} at @s run function bm:p115/pipes/visit',
                            f'execute if entity @s[tag=bm.po_e] positioned ~2 ~ ~ as {nb.replace("tag=!bm.gvwet", "tag=!bm.gvwet,tag=bm.po_w")} at @s run function bm:p115/pipes/visit',
                            f'execute if entity @s[tag=bm.po_w] positioned ~-2 ~ ~ as {nb.replace("tag=!bm.gvwet", "tag=!bm.gvwet,tag=bm.po_e")} at @s run function bm:p115/pipes/visit'])
    ARM = {'n': ((-0.1, 0.03, -1.0), (0.2, 0.2, 0.85)), 's': ((-0.1, 0.03, 0.15), (0.2, 0.2, 0.85)),
           'e': ((0.15, 0.03, -0.1), (0.85, 0.2, 0.2)), 'w': ((-1.0, 0.03, -0.1), (0.85, 0.2, 0.2))}
    draw = ['scoreboard players operation #r bm.rng = @s bm.pr', 'scoreboard players operation #c bm.rng = @s bm.pc',
            'execute as @e[type=minecraft:block_display,tag=bm.gvpd,distance=..2] if score @s bm.pr = #r bm.rng if score @s bm.pc = #c bm.rng run kill @s']
    for wet, blk in ((0, 'minecraft:waxed_cut_copper'), (1, 'minecraft:light_blue_concrete')):
        c_ = 'execute ' + ('if' if wet else 'unless') + ' entity @s[tag=bm.gvwet] run '
        draw.append(c_ + disp(blk, '~-0.15 ~0.01 ~-0.15', (0.3, 0.26, 0.3), ['bm.gvpd', 'bm.gvpdn']))
        for d, (o, sc) in ARM.items():
            draw.append(f'execute if entity @s[tag=bm.po_{d}] ' + c_[8:] + disp(blk, f'~{o[0]} ~{o[1]} ~{o[2]}', sc, ['bm.gvpd', 'bm.gvpdn']))
    draw += ['scoreboard players operation @e[type=minecraft:block_display,tag=bm.gvpdn,distance=..2] bm.pr = #r bm.rng',
             'scoreboard players operation @e[type=minecraft:block_display,tag=bm.gvpdn,distance=..2] bm.pc = #c bm.rng',
             'tag @e[type=minecraft:block_display,tag=bm.gvpdn,distance=..2] remove bm.gvpdn']
    fn('p115/pipes/draw', draw)
    fn('p115/pipes/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'execute if score @s bm.gvs matches 0 run scoreboard players set @s bm.gvs 1',
                           'execute if score @s bm.gvtm matches 3000 run scoreboard players set @s bm.gvf 1',
                           'execute as @e[type=minecraft:interaction,tag=bm.gvpint,distance=..12] if data entity @s interaction at @s run function bm:p115/pipes/click'])
    fn('p115/pipes/click', ['data remove entity @s interaction', 'playsound minecraft:block.copper_trapdoor.close block @a[distance=..16] ~ ~ ~ 1 1.2',
                            'tag @e[type=minecraft:marker,tag=bm.gvpcell,distance=..0.3,limit=1] add bm.gvpme',
                            'execute as @e[type=minecraft:marker,tag=bm.gvr_pipes,distance=..14,sort=nearest,limit=1] at @s run function bm:p115/pipes/work',
                            'tag @e[type=minecraft:marker,tag=bm.gvpme] remove bm.gvpme'])
    me = '@e[type=minecraft:marker,tag=bm.gvpme,limit=1]'
    sel = '@e[type=minecraft:marker,tag=bm.gvpsel,distance=..12,limit=1]'
    fn('p115/pipes/work', [f'execute unless score @s bm.gvvar matches 1 as {me} run function bm:p115/pipes/turn',
                           f'execute if score @s bm.gvvar matches 1 run function bm:p115/pipes/swap', 'function bm:p115/pipes/flow'])
    fn('p115/pipes/turn', ['scoreboard players add @s bm.gvy2 1', 'execute if score @s bm.gvy2 matches 4.. run scoreboard players set @s bm.gvy2 0'])
    fn('p115/pipes/pick', [crew_say([T('Picked. ', GOLD, bold=True), T('Now click the piece to swap it with.', 'gray')], r=16), f'tag {me} add bm.gvpsel'])
    fn('p115/pipes/swap', [f'execute unless entity {sel} run return run function bm:p115/pipes/pick', 'execute if entity @e[type=minecraft:marker,tag=bm.gvpsel,tag=bm.gvpme] run return run tag @e[tag=bm.gvpsel] remove bm.gvpsel',
                           f'scoreboard players operation #t bm.rng = {me} bm.gvy1', f'scoreboard players operation #k bm.rng = {me} bm.gvy2',
                           f'scoreboard players operation {me} bm.gvy1 = {sel} bm.gvy1', f'scoreboard players operation {me} bm.gvy2 = {sel} bm.gvy2',
                           f'scoreboard players operation {sel} bm.gvy1 = #t bm.rng', f'scoreboard players operation {sel} bm.gvy2 = #k bm.rng',
                           'tag @e[type=minecraft:marker,tag=bm.gvpsel] remove bm.gvpsel'])
    fn('p115/pipes/won', ['scoreboard players set @s bm.gvs 2'] + big('THE WATER RUNS', 'Through and out - the way on is open.', '#7ad0ff') + pot(4) +
       ['playsound minecraft:block.water.ambient block @a[distance=..20] ~ ~ ~ 1 1', 'function bm:p70/solved'])

    # ================================================================== THE APOTHECARY
    def hatch():
        return [f'summon minecraft:interaction {relf(12.5, 4, 2.5)} {{Tags:["bm.gvprop","bm.gvhatch"],width:1.2f,height:1.6f,response:1b}}',
                label(rel(12, 6.6, 2), T("THE FIXER'S HATCH", GOLD, bold=True), 0.5)]
    WATER = room_item('potion', ',minecraft:potion_contents={potion:"minecraft:water"}')
    def bottle(it, pid): return f'minecraft:{it}[minecraft:potion_contents={{potion:"minecraft:{pid}"}}]'
    APA = [(t, j, nm, it, pid) for t, L in BREW_A.items() for j, (nm, it, pid) in enumerate(L)]
    APB = [(t, j, pid) for t, L in BREW_B.items() for j, pid in enumerate(L)]
    APC = [(t, j, nm, it, pid) for t, L in BREW_C.items() for j, (nm, it, pid) in enumerate(L)]
    fn('p115/apoth/init', var_init('apoth', 'p115/apoth/a', 'p115/apoth/b', 'p115/apoth/c'))
    for v, rows, size in (('a', APA, 3), ('b', APB, 3), ('c', APC, 2)):
        fn(f'p115/apoth/{v}', hatch() + ['scoreboard players set @s bm.gvc 0'] +
           [f'execute if score #gt bm.rng matches {t} store result score @s bm.gvc run random value {10 * t}..{10 * t + size - 1}' for t in range(2, 6)] +
           ['execute if score #gt bm.rng matches 1 store result score @s bm.gvc run random value 20..21'] +
           [f'execute if score @s bm.gvc matches {10 * r[0] + r[1]} run function bm:p115/apoth/s{v}{r[0]}{r[1]}' for r in rows])
    def give_ing(pids, extra_decoys, rng):
        need = []
        for p in pids:
            for i in INGR[p]: need.append(i)
        dec = [d for d in DECOY if d not in need]
        rng.shuffle(dec)
        items = {'nether_wart': len(pids) + 1, 'blaze_powder': 2}
        for i in need + dec[:extra_decoys]: items[i] = items.get(i, 0) + 1
        return [f'give @s {WATER} 3'] + [f'give @s {room_item(i)} {n}' for i, n in sorted(items.items())]
    rngi = random.Random(7211)
    for t, j, nm, it, pid in APA:
        fn(f'p115/apoth/sa{t}{j}', [sign(rel(12, 8.2, 1), 'THE APOTHECARY', f'The Fixer wants {nm}. Brew it at the stands and hand it in at his hatch.', 0.6)])
        fn(f'p115/apoth/ga{t}{j}', give_ing([pid], 2, rngi))
    for t, j, pid in APB:
        fn(f'p115/apoth/sb{t}{j}', [sign(rel(12, 8.2, 1), "THE APOTHECARY'S RIDDLE", f'"{RIDDLE_B[pid]}" Brew it and hand it in. A wrong potion rings the alarm.', 0.6)])
        fn(f'p115/apoth/gb{t}{j}', give_ing(BREW_B[t], 0, rngi))
    for t, j, nm, it, pid in APC:
        fn(f'p115/apoth/sc{t}{j}', [sign(rel(12, 8.2, 1), "THE APOTHECARY'S TINCTURE", f'The Fixer wants {nm}. Mind the order: the base, the effect, then what changes it.', 0.6)])
        extra = ['gunpowder'] if it == 'splash_potion' else []
        fn(f'p115/apoth/gc{t}{j}', give_ing([pid], 1, rngi) + [f'give @s {room_item(e)} 2' for e in extra] + [f'give @s {room_item("redstone")} 1', f'give @s {room_item("glowstone_dust")} 1'])
    ALLV = [('a', t, j, it, pid) for t, j, nm, it, pid in APA] + [('b', t, j, 'potion', pid) for t, j, pid in APB] + [('c', t, j, it, pid) for t, j, nm, it, pid in APC]
    fn('p115/apoth/tick', ['execute if score @s bm.gvs matches 3 run return 0',
                           'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..10] run function bm:p115/apoth/start',
                           'execute if score @s bm.gvtm matches 6000 run scoreboard players set @s bm.gvf 1',
                           'execute as @e[type=minecraft:interaction,tag=bm.gvhatch,distance=..14] if data entity @s interaction at @s run function bm:p115/apoth/hatch'])
    fn('p115/apoth/start', ['scoreboard players set @s bm.gvs 1', 'scoreboard players operation #rc bm.rng = @s bm.gvc'] +
       [f'execute if score @s bm.gvvar matches {"abc".index(v)} if score #rc bm.rng matches {10 * t + j} as {crew} run function bm:p115/apoth/g{v}{t}{j}' for v, t, j, it, pid in ALLV] +
       [crew_say('The Fixer\'s shelf: water, blaze powder for the stands, and a few ingredients.', GOLD, 30)])
    fn('p115/apoth/hatch', ['execute on target run function bm:p115/apoth/hand', 'data remove entity @s interaction'])
    fn('p115/apoth/hand', ['execute as @e[type=minecraft:marker,tag=bm.gvr_apoth,distance=..16,sort=nearest,limit=1] run function bm:p115/apoth/rc'] +
       [f'execute if score #rv bm.rng matches {"abc".index(v)} if score #rc bm.rng matches {10 * t + j} if items entity @s weapon.mainhand {bottle(it, pid)} run return run function bm:p115/apoth/done'
        for v, t, j, it, pid in ALLV] +
       ['execute if items entity @s weapon.mainhand #bm:p115/potions run return run function bm:p115/apoth/wrong',
        title('@s', 'actionbar', T('"Bring me the potion - in your hand."', 'red'))])
    G.wjson('bm/tags/item/p115/potions.json', {'values': ['minecraft:potion', 'minecraft:splash_potion', 'minecraft:lingering_potion']})
    fn('p115/apoth/rc', ['scoreboard players operation #rc bm.rng = @s bm.gvc', 'scoreboard players operation #rv bm.rng = @s bm.gvvar'])
    fn('p115/apoth/wrong', ['item replace entity @s weapon.mainhand with minecraft:air', 'playsound minecraft:entity.witch.drink player @a[distance=..16] ~ ~ ~ 1 0.6',
                            title('@s', 'actionbar', T('"Pfah! That\'s not what I asked for." He pours it out - loudly.', 'red')),
                            'execute as @e[type=minecraft:marker,tag=bm.gvr_apoth,distance=..16,sort=nearest,limit=1] at @s run function bm:p115/apoth/oops'])
    fn('p115/apoth/oops', oops(2) + ['scoreboard players set @s bm.gvf 1'])
    fn('p115/apoth/done', ['item replace entity @s weapon.mainhand with minecraft:air', 'playsound minecraft:entity.witch.celebrate player @a[distance=..16] ~ ~ ~ 1 1.2',
                           'execute as @e[type=minecraft:marker,tag=bm.gvr_apoth,distance=..16,sort=nearest,limit=1] at @s run function bm:p115/apoth/won'])
    fn('p115/apoth/won', [f'clear {crew} #bm:p115/potions[!minecraft:custom_data]', 'kill @e[type=minecraft:item,distance=..16]'] +
       big('JUST THE THING', 'The Fixer corks it - the way on is open.', '#c070ff') + pot(4) + ['function bm:p70/solved'])

    # ================================================================== THE GRAPPLE (the hook: phase21's, lent by the room)
    HOOK = ('minecraft:carrot_on_a_stick[minecraft:custom_data={bm:"grappling_hook",bm_room:1b,bm_rhook:1b},minecraft:item_model="bm:grappling_hook",minecraft:max_stack_size=1,'
            'minecraft:item_name=' + snbt(T("The Fixer's Hook", GOLD)) + ',minecraft:lore=[' + snbt(T('Bites only the lamps. Works only in its own room.', 'gray')) + ']]')
    rhook = '*[minecraft:custom_data~{bm_rhook:1b}]'
    use = G.FUNCS['p21/grap/use']
    k = next(i for i, l in enumerate(use) if 'tag=bm.adv' in l)
    use[k] = use[k].replace('execute if entity @s[tag=bm.adv] run', 'execute if entity @s[tag=bm.adv] unless score @s bm.gvhk matches 1.. run')
    use.insert(k, f'execute if items entity @s weapon.* {rhook} unless score @s bm.gvhk matches 1.. run return run ' + title('@s', 'actionbar', T("The Fixer's hook only works in its own room.", 'gray')))
    use.insert(k + 1, 'execute if score @s bm.gvhk matches 1.. if score @s bm.gvhu matches ..0 run return run ' + title('@s', 'actionbar', T('No hooks left - the rope is spent.', 'red')))
    k = next(i for i, l in enumerate(use) if l == 'scoreboard players set #gr bm.rng 64, scoreboard players set #ghit bm.rng 0' or l.startswith('scoreboard players set #gr bm.rng 64'))
    use.insert(k + 1, 'execute if score @s bm.gvhk matches 1.. run scoreboard players operation #gr bm.rng = @s bm.gvhr')
    k = next(i for i, l in enumerate(use) if 'if score #ghit bm.rng matches 0 run return' in l)
    use[k:k] = ['execute if score #ghit bm.rng matches 2 run return 0',
                'execute if score #ghit bm.rng matches 3 run return run ' + title('@s', 'actionbar', T("The hook won't bite on that - only the lamps.", 'gray'))]
    use.append('execute if score @s bm.gvhk matches 1.. run function bm:p115/hook/used')
    ray = G.FUNCS['p21/grap/ray']
    ray.insert(0, 'execute if score @s bm.gvhk matches 1.. unless block ~ ~ ~ #bm:grap_pass unless block ~ ~ ~ minecraft:target run return run scoreboard players set #ghit bm.rng 3')
    hit = G.FUNCS['p21/grap/hit']
    hit[0:0] = ['execute if score @s bm.gvhb matches 1 run return run function bm:p115/hook/bell',
                'execute if score @s bm.gvhk matches 1.. align xyz positioned ~0.5 ~-0.5 ~0.5 run return run function bm:p115/hook/snap']
    pull = G.FUNCS['p21/grap/pull']
    k = next(i for i, l in enumerate(pull) if 'tag=bm.adv' in l)
    pull[k] = pull[k].replace('execute if entity @s[tag=bm.adv] run', 'execute if entity @s[tag=bm.adv] unless score @s bm.gvhk matches 1.. run')
    # (a hook in a grapple room hangs you right under the lamp's middle, whatever face the rope struck)
    fn('p115/hook/snap', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.ganchor","bm.gnew"]}', 'summon minecraft:marker ~ ~-2.1 ~ {Tags:["bm.gtgt","bm.gnew"]}',
                          'scoreboard players operation @e[type=minecraft:marker,tag=bm.gnew] bm.pid = @s bm.pid', 'tag @e[type=minecraft:marker,tag=bm.gnew] remove bm.gnew',
                          'scoreboard players set #ghit bm.rng 1', 'particle minecraft:crit ~ ~0.5 ~ 0.2 0.2 0.2 0.2 8'])
    fn('p115/hook/used', ['execute if score #ghit bm.rng matches 1 run scoreboard players remove @s bm.gvhu 1',
                          'execute if score #ghit bm.rng matches 1 if score @s bm.gvhu matches 0..9 run ' + title('@s', 'actionbar', [T('Hooks left: ', GOLD), {'score': {'name': '@s', 'objective': 'bm.gvhu'}, 'color': 'white', 'bold': True}])])
    fn('p115/hook/bell', ['scoreboard players set #ghit bm.rng 2',
                          'execute align xyz positioned ~0.5 ~0.5 ~0.5 as @e[type=minecraft:marker,tag=bm.gvbell,distance=..0.6,limit=1] at @s run function bm:p115/grapple/ring',
                          'execute unless entity @e[type=minecraft:marker,tag=bm.gvbell,distance=..2] run scoreboard players set #ghit bm.rng 3'])
    G.FUNCS['tick'].append('scoreboard players remove @a[scores={bm.gvhk=1..}] bm.gvhk 1')
    def lamp(x, y, z, top=14):
        return ['setblock ' + rel(x, y, z) + ' minecraft:target'] + [f'fill {rel(x, y + 1, z)} {rel(x, top, z)} minecraft:iron_chain']
    def island(cx, cz):
        return [f'fill {rel(cx - 1, 0, cz - 1)} {rel(cx, 3, cz)} minecraft:air'] + themed(f'fill {rel(cx - 1, 0, cz - 1)} {rel(cx, 2, cz)} {{b}}', 'pillar') + \
               themed(f'fill {rel(cx - 1, 3, cz - 1)} {rel(cx, 3, cz)} {{b}}', 'trim')
    fn('p115/grapple/init', var_init('grapple', 'p115/grapple/a', 'p115/grapple/b', 'p115/grapple/c'))
    ledge = themed(f'fill {rel(23, 0, 10)} {rel(23, 3, 14)} {{b}}', 'floor')
    for j, (isl, h) in enumerate(PD.CHASMS):
        L = list(ledge)
        for (cx, cz) in isl: L += island(cx, cz) + lamp(cx - 1, PD.LAMP_Y, cz - 1)
        L += lamp(23, PD.LAMP_Y, 12)
        fn(f'p115/grapple/a{j}', L + [f'scoreboard players set @s bm.gvx {h}'])
    fn('p115/grapple/a', choose('#i', len(PD.CHASMS), 'p115/grapple/a') + ['scoreboard players operation @s bm.gvc = #i bm.rng', 'scoreboard players set @s bm.gvy3 18'] +
       [sign(rel(2, 7.8, 9), 'THE CHASM', 'The Fixer\'s hook bites only the lamps: hook one and hang under it, sneak to let go. You get only so many hooks - some gaps you can jump. Hay: back to the start.', 0.55)])
    bl = list(ledge)
    for i, cx in enumerate(PD.LANES):
        bl += island(cx, 12) + [f'summon minecraft:marker {relf(cx - 0.5, PD.LAMP_Y, 11.5)} {{Tags:["bm.gvprop","bm.gvswing"]}}']
        for dz in PD.SWING: bl += [f'fill {rel(cx - 1, PD.LAMP_Y + 1, 11 + dz)} {rel(cx - 1, 14, 11 + dz)} minecraft:iron_chain']
    bl += lamp(23, PD.LAMP_Y, 12)
    fn('p115/grapple/b', bl + ['scoreboard players set @s bm.gvx 99', 'scoreboard players set @s bm.gvy3 18'] +
       [sign(rel(2, 7.8, 9), 'THE SWINGING LAMPS', 'The lamps swing over the pit: hook each one as it swings over its island, then let go (sneak). Hay: back to the start.', 0.55)])
    swing = []
    for ph, dz in enumerate(PD.SWING):
        swing.append(f'execute if score #ph bm.rng matches {ph * 16} as @e[type=minecraft:marker,tag=bm.gvswing,distance=..20] at @s run function bm:p115/grapple/sw{ph}')
        fn(f'p115/grapple/sw{ph}', [f'setblock ~ ~ ~{d} ' + ('minecraft:target' if d == dz else 'minecraft:air') for d in PD.SWING])
    # C: the bells - near floor x 1..8, the gap x 9..15, the far side x 16..23
    cl = [f'fill {rel(1, 0, 1)} {rel(8, 3, 23)} minecraft:blackstone'] + themed(f'fill {rel(1, 3, 1)} {rel(8, 3, 23)} {{b}}', 'floor') + \
         [f'fill {rel(16, 0, 1)} {rel(23, 3, 23)} minecraft:blackstone'] + themed(f'fill {rel(16, 3, 1)} {rel(23, 3, 23)} {{b}}', 'floor')
    for i, (x, y, z) in enumerate(PD.BELLS):
        cl += themed(f'fill {rel(x, 4, z)} {rel(x, y - 2, z)} {{b}}', 'pillar') + [f'setblock {rel(x, y - 1, z)} minecraft:{PD.BELL_COLS[i]}_wool',
                                                                                    f'setblock {rel(x, y, z)} minecraft:target', f'setblock {rel(x, y + 1, z)} minecraft:bell[attachment=floor,facing=west]',
                                                                                    f'summon minecraft:marker {relf(x + 0.5, y + 0.5, z + 0.5)} {{Tags:["bm.gvprop","bm.gvbell","bm.gvbn"]}}',
                                                                                    f'scoreboard players set @e[type=minecraft:marker,tag=bm.gvbn,limit=1] bm.gvy1 {i}',
                                                                                    'tag @e[type=minecraft:marker,tag=bm.gvbn] remove bm.gvbn']
    ORDERS = [[2, 0, 3, 1], [1, 3, 0, 2], [3, 1, 2, 0], [0, 2, 1, 3]]
    fn('p115/grapple/c', cl + ['scoreboard players set @s bm.gvx 99', 'scoreboard players set @s bm.gvy3 24', 'scoreboard players set @s bm.gvw 0'] + choose('#i', len(ORDERS), 'p115/grapple/o') +
       ['scoreboard players operation @s bm.gvc = #i bm.rng'])
    CN = {'red': '#ff5050', 'blue': '#5a8aff', 'yellow': '#ffe050', 'lime': '#7dff6a'}
    for o, order in enumerate(ORDERS):
        fn(f'p115/grapple/o{o}', [sign(rel(2, 7.8, 9), 'THE BELLS', 'Ring the bells across the gap with the hook (it won\'t pull you - it rings), in this order:', 0.55),
                                  label(rel(2, 6.8, 9), [T('●  ', CN[PD.BELL_COLS[b]], bold=True) for b in order], 0.9)] +
           [f'scoreboard players set @s bm.lq{k} {b}' for k, b in enumerate(order)])
    fn('p115/grapple/ring', ['playsound minecraft:block.bell.use block @a[distance=..30] ~ ~ ~ 1.4 1', 'scoreboard players operation #bell bm.rng = @s bm.gvy1',
                             'execute as @e[type=minecraft:marker,tag=bm.gvr_grapple,distance=..20,sort=nearest,limit=1] at @s run function bm:p115/grapple/rung'])
    fn('p115/grapple/rung', ['execute if score @s bm.gvs matches 3 run return 0'] +
       [f'execute if score @s bm.gvw matches {k} unless score #bell bm.rng = @s bm.lq{k} run return run function bm:p115/grapple/wrong' for k in range(4)] +
       ['scoreboard players add @s bm.gvw 1', 'execute if score @s bm.gvw matches 4.. run function bm:p115/grapple/bridge'])
    fn('p115/grapple/wrong', ['scoreboard players set @s bm.gvw 0', 'scoreboard players set @s bm.gvf 1',
                              crew_say([T('A wrong note! ', 'red', bold=True), T('Start again - and the alarm rings.', 'gray')], r=30)] + oops(2))
    fn('p115/grapple/bridge', themed(f'fill {rel(9, 3, 12)} {rel(15, 3, 12)} {{b}}', 'trim') + big('THE BRIDGE COMES OUT', 'Walk across - the way on is open.', GOLD) + pot(4) +
       ['function bm:p70/solved'])
    box = f'positioned {relf(0.6, 3.5, 0.6)} as @a[tag=bm.gvp,dx=22.8,dy=12,dz=22.8]'
    fn('p115/grapple/tick', ['execute if score @s bm.gvs matches 0 run scoreboard players set @s bm.gvs 1',
                             'scoreboard players set #hb bm.rng 0', 'execute if score @s bm.gvvar matches 2 run scoreboard players set #hb bm.rng 1',
                             f'execute unless score @s bm.gvs matches 3 {box} at @s run function bm:p115/grapple/me',
                             'execute if score @s bm.gvs matches 3 run return 0',
                             'execute if score @s bm.gvtm matches 3000 run scoreboard players set @s bm.gvf 1',
                             'scoreboard players operation #ph bm.rng = @s bm.gvtm', 'scoreboard players operation #ph bm.rng %= #48 bm.rng'] + swing +
                            [f'execute positioned {relf(3.6, -2, 0.6)} as @a[tag=bm.gvp,dx=19,dy=4,dz=22.8] at @s run function bm:p115/grapple/fell',
                             f'execute unless score @s bm.gvvar matches 2 positioned {relf(23, 3.9, 9.6)} if entity @a[tag=bm.gvp,dx=0.8,dy=2,dz=4.8] positioned as @s run function bm:p115/grapple/across'])
    G.FUNCS['load'].append('scoreboard players set #48 bm.rng 48')
    fn('p115/grapple/me', ['scoreboard players set @s bm.gvhk 3',
                           'scoreboard players operation #key bm.rng = @s bm.gvrun',
                           'scoreboard players operation #key bm.rng *= #100 bm.rng',
                           'scoreboard players operation #key bm.rng += @e[type=minecraft:marker,tag=bm.gvr_grapple,limit=1,sort=nearest] bm.gvq',
                           'execute unless score @s bm.gvhq = #key bm.rng run scoreboard players reset @s bm.gvhu',
                           'scoreboard players operation @s bm.gvhq = #key bm.rng',
                           'scoreboard players operation @s bm.gvhr = @e[type=minecraft:marker,tag=bm.gvr_grapple,limit=1,sort=nearest] bm.gvy3',
                           'scoreboard players operation @s bm.gvhb = #hb bm.rng',
                           'execute unless score @s bm.gvhu matches -100.. run scoreboard players operation @s bm.gvhu = @e[type=minecraft:marker,tag=bm.gvr_grapple,limit=1,sort=nearest] bm.gvx',
                           f'execute unless items entity @s container.* {rhook} unless items entity @s weapon.offhand {rhook} run function bm:p115/grapple/lend'])
    fn('p115/grapple/lend', [f'give @s {HOOK}', 'scoreboard players operation @s bm.gvhu = @e[type=minecraft:marker,tag=bm.gvr_grapple,limit=1,sort=nearest] bm.gvx',
                             title('@s', 'actionbar', [T("The Fixer's hook. ", GOLD, bold=True), T('Right-click a lamp to swing to it; sneak to let go.', 'gray')])])
    fn('p115/grapple/fell', ['execute if entity @s[tag=bm.grappling] run function bm:p21/grap/release',
                             'execute at @e[type=minecraft:marker,tag=bm.gvr_grapple,distance=..30,sort=nearest,limit=1] run tp @s ' + rel(2, 4, 12) + ' -90 0',
                             'scoreboard players operation @s bm.gvhu = @e[type=minecraft:marker,tag=bm.gvr_grapple,limit=1,sort=nearest] bm.gvx',
                             title('@s', 'actionbar', T('Down into the hay! Back to the start - and your hooks back.', 'red'))])
    fn('p115/grapple/across', big('ACROSS!', 'The far ledge - the way on is open.', GOLD) + pot(4) + ['function bm:p70/solved'])
    G.FUNCS['p70/unraid'].append('scoreboard players reset @s bm.gvhu')

    # ================================================================== THE MINECART RUN
    def track(path, powered_every=5):
        sup, rl = [], []
        for i, ((x, z), shp) in enumerate(PD.rails(path)):
            pw = shp in ('north_south', 'east_west') and i % powered_every == 2
            sup.append(f'setblock {rel(x, 3, z)} ' + ('minecraft:redstone_block' if pw else 'minecraft:spruce_planks'))
            rl.append(f'setblock {rel(x, 4, z)} ' + (f'minecraft:powered_rail[shape={shp},powered=true]' if pw else f'minecraft:rail[shape={shp}]'))
        return sup + rl + rl            # (twice: a rail set over a rail keeps exactly the shape it's given)
    def post(x, y, z):
        return [f'fill {rel(x, 0, z)} {rel(x, y - 1, z)} minecraft:spruce_fence']
    fn('p115/minecart/init', var_init('minecart', 'p115/minecart/a', 'p115/minecart/b', 'p115/minecart/c'))
    ma = track(PD.RUN_A) + sum((post(x, y, z) + [f'setblock {rel(x, y, z)} minecraft:target'] for x, y, z in PD.TARGETS_A), [])
    fn('p115/minecart/a', ma + ['scoreboard players set @s bm.gvw 0', 'scoreboard players operation @s bm.gvx = #gt bm.rng', 'scoreboard players add @s bm.gvx 5',
                                'execute if score @s bm.gvx matches 9.. run scoreboard players set @s bm.gvx 8',
                                sign(rel(2, 7.6, 9), 'THE RAIL SHOOTER', 'Get in the cart and you\'re off. Hit enough of the targets beside the track on one ride (a bow is lent at the station).', 0.55),
                                'function bm:p115/minecart/cart'])
    mb = track(PD.RUN_B_MAIN) + track(PD.RUN_B_SOUTH) + track(PD.SPUR_J1) + track(PD.SPUR_J3)
    for n, ((x, z), s0, s1) in PD.JUNCTIONS.items():
        mb.append(f'setblock {rel(x, 4, z)} minecraft:rail[shape={s0}]')
        mb += themed(f'setblock {rel(n, 4, 14)} {{b}}', 'pillar') + [f'setblock {rel(n, 5, 14)} minecraft:lever[face=floor,facing=north,powered=false]']
        mb.append(label(relf(n + 0.5, 5.9, 14.5), T(f'POINTS {n}', GOLD, bold=True), 0.4))
    for x, z in PD.B_ENDS:
        mb += [f'summon minecraft:marker {relf(x + 0.5, 4, z + 0.5)} {{Tags:["bm.gvprop","bm.gvbuf"]}}', label(relf(x + 0.5, 5.4, z + 0.5), T('DEAD END', 'red', bold=True), 0.5)]
    fn('p115/minecart/b', mb + [
                                sign(rel(2, 7.6, 9), 'THE SWITCH YARD', 'Set the points with the levers by the station, then ride: only one way reaches the gold station. A dead end rings the alarm.', 0.55),
                                'function bm:p115/minecart/cart'])
    mc = track(PD.RUN_C)
    for g in PD.GAPS_C:
        mc += [f'setblock {rel(x, 4, z)} minecraft:air' for x, z in g] + [f'setblock {rel(x, 3, z)} minecraft:air' for x, z in g]
    for (x, y, z) in PD.BUTTONS_C:
        mc += post(x, y, z) + [f'setblock {rel(x, y, z)} minecraft:pale_oak_button[face=floor,facing=east,powered=false]']
    fn('p115/minecart/c', mc + ['scoreboard players set @s bm.gvw 0',
                                sign(rel(2, 7.6, 9), 'THE DRAWBRIDGES', 'Three gaps in the track. Press the button by the rails and the gap ahead closes for two seconds - press it as you pass, or have a friend do it.', 0.55),
                                'function bm:p115/minecart/cart'])
    fn('p115/minecart/cart', ['kill @e[type=minecraft:minecart,tag=bm.gvcart,distance=..20]',
                              f'summon minecraft:minecart {relf(3.5, 4.1, 12.5)} {{Tags:["bm.gvprop","bm.gvcart"],Rotation:[-90f,0f]}}'])
    riding = '@a[tag=bm.gvp,distance=..24,predicate=bm:p21/riding]'
    mtick = ['execute if score @s bm.gvs matches 3 run return 0', 'execute if score @s bm.gvs matches 0 run scoreboard players set @s bm.gvs 1',
             f'execute if score @s bm.gvvar matches 0 positioned {relf(0.6, 3.9, 9.6)} as @a[tag=bm.gvp,dx=3,dy=2,dz=4.8] unless items entity @s container.* minecraft:bow run function bm:p115/minecart/bow',
             # (off: someone in the cart at the station)
             f'execute if score @s bm.gvs matches 1 positioned {relf(3.5, 4, 12.5)} if entity @e[type=minecraft:minecart,tag=bm.gvcart,distance=..1.2] as @e[type=minecraft:minecart,tag=bm.gvcart,distance=..1.2,limit=1] on passengers if entity @s[type=minecraft:player] at @s run function bm:p115/minecart/go_as',
             f'execute positioned {relf(4, 0.5, 0.6)} as @a[tag=bm.gvp,dx=17,dy=2,dz=22.8] at @s run function bm:p115/minecart/fell',
             f'execute if score @s bm.gvs matches 2 positioned {relf(21, 3.6, 9.6)} as @a[tag=bm.gvp,dx=3,dy=3,dz=4.8,predicate=bm:p21/riding] at @s run function bm:p115/minecart/home',
             'execute if score @s bm.gvs matches 2 run scoreboard players add @s bm.gvy3 1',
             'execute if score @s bm.gvs matches 2 if score @s bm.gvy3 matches 1200.. run function bm:p115/minecart/timeout',
             'execute if score @s bm.gvvar matches 0 if score @s bm.gvs matches 2 run function bm:p115/minecart/shoot',
             'execute if score @s bm.gvvar matches 1 run function bm:p115/minecart/points',
             'execute if score @s bm.gvvar matches 1 if score @s bm.gvs matches 2 as @e[type=minecraft:marker,tag=bm.gvbuf,distance=..20] at @s if entity @a[tag=bm.gvp,distance=..1.6] run function bm:p115/minecart/deadend',
             'execute if score @s bm.gvvar matches 2 run function bm:p115/minecart/bridges']
    fn('p115/minecart/tick', mtick)
    fn('p115/minecart/bow', [f'give @s {room_item("bow", ",minecraft:unbreakable={}")}', f'give @s {room_item("arrow")} 24'])
    fn('p115/minecart/go_as', ['execute as @e[type=minecraft:marker,tag=bm.gvr_minecart,distance=..20,sort=nearest,limit=1] at @s run function bm:p115/minecart/go'])
    fn('p115/minecart/go', ['scoreboard players set @s bm.gvs 2', 'scoreboard players set @s bm.gvy3 0', 'scoreboard players set @s bm.gvw 0',
                            'execute as @e[type=minecraft:minecart,tag=bm.gvcart,distance=..20] run data merge entity @s {Motion:[0.6d,0.0d,0.0d]}',
                            'playsound minecraft:entity.minecart.riding neutral @a[distance=..20] ~ ~ ~ 0.6 1.2',
                            crew_say([T('Off you go! ', GOLD, bold=True)], r=24)])
    fn('p115/minecart/fell', ['execute on vehicle run kill @s', 'ride @s dismount',
                              'execute at @e[type=minecraft:marker,tag=bm.gvr_minecart,distance=..30,sort=nearest,limit=1] run tp @s ' + rel(2, 5, 12) + ' -90 0',
                              title('@s', 'actionbar', T('Off the rails and into the hay! Back to the station.', 'red')),
                              'execute as @e[type=minecraft:marker,tag=bm.gvr_minecart,distance=..30,sort=nearest,limit=1] at @s run function bm:p115/minecart/reset'])
    fn('p115/minecart/reset', ['scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvy3 0', 'scoreboard players set @s bm.gvw 0',
                               'execute if score @s bm.gvvar matches 0 run function bm:p115/minecart/targets', 'function bm:p115/minecart/cart'])
    fn('p115/minecart/targets', [f'setblock {rel(x, y, z)} minecraft:target' for x, y, z in PD.TARGETS_A])
    fn('p115/minecart/timeout', [crew_say([T('The cart stalls. ', 'red', bold=True), T('Back to the station.', 'gray')], r=30),
                                 f'execute as {riding} run ride @s dismount', f'execute as @a[tag=bm.gvp,distance=..24] run tp @s ' + rel(2, 5, 12) + ' -90 0', 'function bm:p115/minecart/reset'])
    fn('p115/minecart/shoot', [f'execute if block {rel(x, y, z)} minecraft:target unless block {rel(x, y, z)} minecraft:target[power=0] run function bm:p115/minecart/hit{i}'
                               for i, (x, y, z) in enumerate(PD.TARGETS_A)])
    for i, (x, y, z) in enumerate(PD.TARGETS_A):
        fn(f'p115/minecart/hit{i}', [f'setblock {rel(x, y, z)} minecraft:redstone_lamp[lit=true]', 'scoreboard players add @s bm.gvw 1',
                                     f'particle minecraft:crit {rel(x, y, z)} 0.3 0.3 0.3 0.2 10', 'playsound minecraft:entity.arrow.hit_player block @a[distance=..30] ~ ~ ~ 1 1.4',
                                     crew_say([T('Hit! ', GOLD, bold=True), {'score': {'name': '@e[type=minecraft:marker,tag=bm.gvr_minecart,limit=1,sort=nearest]', 'objective': 'bm.gvw'}, 'color': 'white'},
                                               T(' of ', 'gray'), {'score': {'name': '@e[type=minecraft:marker,tag=bm.gvr_minecart,limit=1,sort=nearest]', 'objective': 'bm.gvx'}, 'color': 'white'}], r=30)])
    fn('p115/minecart/home', ['execute as @e[type=minecraft:marker,tag=bm.gvr_minecart,distance=..30,sort=nearest,limit=1] at @s run function bm:p115/minecart/arrive'])
    fn('p115/minecart/arrive', ['execute if score @s bm.gvs matches 3 run return 0',
                                'execute if score @s bm.gvvar matches 0 if score @s bm.gvw < @s bm.gvx run return run function bm:p115/minecart/short',
                                f'execute as {riding} run ride @s dismount', 'kill @e[type=minecraft:minecart,tag=bm.gvcart,distance=..30]', 'scoreboard players set @s bm.gvs 3'] +
       big('END OF THE LINE', 'Into the gold station - the way on is open.', GOLD) + pot(5) + ['function bm:p70/solved'])
    fn('p115/minecart/short', [crew_say([T('Not enough hits! ', 'red', bold=True), T('Back to the station - the alarm rings.', 'gray')], r=30),
                               f'execute as {riding} run ride @s dismount', f'execute as @a[tag=bm.gvp,distance=..30] run tp @s ' + rel(2, 5, 12) + ' -90 0',
                               'scoreboard players set @s bm.gvf 1'] + oops(2) + ['function bm:p115/minecart/reset'])
    fn('p115/minecart/deadend', ['execute as @e[type=minecraft:marker,tag=bm.gvr_minecart,distance=..30,sort=nearest,limit=1] at @s run function bm:p115/minecart/dead'])
    fn('p115/minecart/dead', [crew_say([T('Dead end! ', 'red', bold=True), T('Back to the station - the alarm rings.', 'gray')], r=30),
                              f'execute as {riding} run ride @s dismount', f'execute as @a[tag=bm.gvp,distance=..30] run tp @s ' + rel(2, 5, 12) + ' -90 0',
                              'scoreboard players set @s bm.gvf 1'] + oops(2) + ['function bm:p115/minecart/reset'])
    pts = []
    for n, ((x, z), s0, s1) in PD.JUNCTIONS.items():
        pts += [f'execute if block {rel(n, 5, 14)} minecraft:lever[powered=true] unless block {rel(x, 4, z)} minecraft:rail[shape={s1}] run setblock {rel(x, 4, z)} minecraft:rail[shape={s1}]',
                f'execute if block {rel(n, 5, 14)} minecraft:lever[powered=false] unless block {rel(x, 4, z)} minecraft:rail[shape={s0}] run setblock {rel(x, 4, z)} minecraft:rail[shape={s0}]']
    fn('p115/minecart/points', pts)
    br = []
    for i, ((x, y, z), g) in enumerate(zip(PD.BUTTONS_C, PD.GAPS_C)):
        br += press(f'db{i}', (x, y, z), f'bm:p115/minecart/close{i}')
        fn(f'p115/minecart/close{i}', [f'scoreboard players set @s bm.lq{i} 40', 'playsound minecraft:block.piston.extend block @a[distance=..30] ~ ~ ~ 1 1'] +
           [f'setblock {rel(gx, 3, gz)} minecraft:spruce_planks' for gx, gz in g] +
           [f'setblock {rel(gx, 4, gz)} minecraft:rail[shape={dict(PD.rails(PD.RUN_C))[(gx, gz)]}]' for gx, gz in g])
        fn(f'p115/minecart/open{i}', ['playsound minecraft:block.piston.contract block @a[distance=..30] ~ ~ ~ 1 1'] +
           [f'setblock {rel(gx, 4, gz)} minecraft:air' for gx, gz in g] + [f'setblock {rel(gx, 3, gz)} minecraft:air' for gx, gz in g])
        br += [f'execute if score @s bm.lq{i} matches 1.. run scoreboard players remove @s bm.lq{i} 1', f'execute if score @s bm.lq{i} matches 1 run function bm:p115/minecart/open{i}']
    fn('p115/minecart/bridges', br)

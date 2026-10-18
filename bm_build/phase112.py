"""2.69: NEW ROOMS - a fight over the void, a harder climb, three puzzles you work with your hands, three new games.

THE SKY ISLES (fight, Tiers II-V)   islands joined by one-block bridges over a drop. Two waves of guards; from Tier III
                                    the drop is the void (fall in and you're knocked out - it costs a try) and breezes
                                    join the second wave to blow you off. On Tier II there's hay at the bottom (back to
                                    the start). Knock a guard off the edge and it's gone.
THE SPIRE (puzzle, Tiers III-V)     single blocks spiral up round a tall pillar - long jumps, one up at a time - to the
                                    pillar's top and the bridge out. A gold CHECKPOINT block halfway: fall into the hay
                                    after touching it and you're back there, not at the bottom.
THE TINKER'S BENCH (Tiers I-V)      the Fixer wants something made (a compass, a lantern, a crossbow, a hopper, an
                                    observer...): you're handed the parts - and a few you don't need. Craft it at the
                                    benches (higher tiers need a part made first) and hand it in at his hatch. Leftovers
                                    go back to him.
THE MASON'S PLAN (Tiers I-IV)       lay coloured blocks on the lodestone grid to match the plan on the plinth by the door.
                                    The blocks only go down on lodestone. From Tier III the plan is drawn turned round -
                                    line up its gold corner with the grid's. RESET by the door clears the grid.
THE DIG (Tiers I-V)                 a wall of deepslate fills the room, threaded with veins of mud bricks. The Fixer's
                                    pick bites only the mud: tunnel through - most veins end in rock. Find the one that
                                    goes all the way.
EVENTS (the event draw, every tier)
  BLOCK PARTY            the floor is a patchwork of colours; a colour is called - get on it before the rest drop away.
                         Eight rounds, quicker each time (ten, and more colours, higher up). Each round someone survives:
                         a coin. Survive most of them for the prize.
  RED LIGHT, GREEN LIGHT the watcher at the far end turns its back - run. When it turns round, freeze: anyone it sees
                         moving goes back to the line. Everyone over the gold line before time's up.
  MEMORY MATCH           sixteen face-down cards: turn two at a time and find the eight pairs before your misses run out.
"""
import math
import random
import itertools
from items import T
from nbt import snbt, B, F, Int
from structures import Build
import phase70_rooms as RM
import phase75 as P75
import phase75_rooms as R5
import phase76_rooms as R6
from phase75_rooms import BASE, wall_glow
import phase110 as P110

GOLD = '#ffcf40'
GAME = '#7ad0ff'
rel, relf, IDENT = RM.rel, P110.relf, P110.IDENT
FY = RM.FY
W, D = 25, 25

# ===================================================================== THE SKY ISLES
ISLANDS = [((1, 10), (3, 14)), ((21, 10), (23, 14)), ((10, 10), (14, 14)), ((5, 4), (7, 6)), ((17, 4), (19, 6)), ((5, 18), (7, 20)), ((17, 18), (19, 20))]
BRIDGES = [(x, 12) for x in range(4, 10)] + [(x, 12) for x in range(15, 21)] + [(6, 10), (6, 8), (18, 10), (18, 8), (6, 14), (6, 16), (18, 14), (18, 16)]
ISLE_SPAWN = [(11, 11), (13, 13), (11, 13), (13, 11), (6, 5), (18, 5), (6, 19), (18, 19)]


def isles():
    b = R6.shell()
    for x in range(1, 24):
        for z in range(1, 24):
            for y in range(0, FY + 1): b.set(x, y, z, 'minecraft:air')
            for y in (4, 5): b.set(x, y, z, 'minecraft:air')          # (the shell's loot piles would float)
    for (x0, z0), (x1, z1) in ISLANDS:
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                b.set(x, FY, z, BASE['floor'] if (x + z) % 2 else BASE['trim']); b.set(x, FY - 1, z, BASE['wall'])
    for x, z in BRIDGES:
        b.set(x, FY, z, BASE['slab'] + '[type=top]' if (x, z) not in ((6, 10), (6, 8), (18, 10), (18, 8), (6, 14), (6, 16), (18, 14), (18, 16)) else BASE['pillar'])
    for (x, z) in ((5, 4), (19, 4), (5, 20), (19, 20)):
        b.set(x, 4, z, 'minecraft:iron_chain'); b.set(x, 5, z, 'minecraft:lantern')
    R6.ctrl(b, 'isles'); return wall_glow(b)


# ===================================================================== THE SPIRE
SPIRE_H, SPIRE_EXIT = 26, 14
PILLAR = (10, 14)                                 # x/z 10..14, up to y 13 (stand at 14)


def _ring():
    return [(8, z) for z in range(16, 7, -1)] + [(x, 8) for x in range(9, 17)] + [(16, z) for z in range(9, 17)] + [(x, 16) for x in range(15, 8, -1)]


def spire_route():
    """(x, z, top) blocks from the floor to the pillar top: on the ring two cells from the pillar; each jump at most one up
    (and then at most 3 across), or level (4 across at most); no block hangs low over another's jumper"""
    ring = _ring()
    route = [(4, 12, 4), (6, 14, 5)]
    i, top = 0, 5
    pat = [(3, 1), (3, 0), (2, 1), (3, 1), (3, 0), (2, 1), (4, 0), (2, 1)]
    k = 0
    route.append((*ring[0], top))
    while top < 12:
        st, dy = pat[k % len(pat)]; k += 1
        i += st; top += dy
        route.append((*ring[i % len(ring)], top))
    return route


SROUTE = spire_route()
SCHECK = len(SROUTE) // 2                          # the checkpoint block


def _spire_ok(route):
    for a, b in zip(route, route[1:] + [(12 - 2 if route[-1][0] <= 8 else (14 + 2 if route[-1][0] >= 16 else route[-1][0]), route[-1][1], 13)]):
        d = math.hypot(a[0] - b[0], a[1] - b[1]); dy = b[2] - a[2]
        assert dy <= 1 and (d <= 3.01 if dy == 1 else d <= 4.01), (a, b, d, dy)
    for a in route:
        for b in route:
            if abs(a[0] - b[0]) <= 1 and abs(a[1] - b[1]) <= 1 and b[2] > a[2]:
                assert b[2] - a[2] >= 5, (a, b)


_spire_ok(SROUTE)


def spire():
    H = SPIRE_H
    b = Build(W, H, D)
    b.fill(0, 0, 0, W - 1, FY - 1, D - 1, 'minecraft:blackstone')
    b.room(0, FY, 0, W - 1, H - 1, D - 1, BASE['wall'], floor='minecraft:hay_block', ceil=BASE['ceil'])
    for y in range(4, 8):
        for z in (11, 12, 13): b.set(0, y, z, 'minecraft:air')
    for y in range(SPIRE_EXIT, SPIRE_EXIT + 4):
        for z in (11, 12, 13): b.set(W - 1, y, z, 'minecraft:iron_bars')
    for y in range(SPIRE_EXIT, SPIRE_EXIT + 5):
        b.set(W - 1, y, 10, BASE['metal']); b.set(W - 1, y, 14, BASE['metal'])
    for z in range(10, 15): b.set(W - 1, SPIRE_EXIT + 4, z, BASE['metal'])
    for y in (4, 5, 6, 7, 8):
        b.set(0, y, 10, BASE['metal']); b.set(0, y, 14, BASE['metal'])
    for z in range(10, 15): b.set(0, 8, z, BASE['metal'])
    for x in range(1, 4):                                    # (the start: firm ground by the door)
        for z in range(10, 15): b.set(x, FY, z, BASE['floor'])
    for y in range(4, SPIRE_EXIT):                           # the pillar
        for x in range(PILLAR[0], PILLAR[1] + 1):
            for z in range(PILLAR[0], PILLAR[1] + 1):
                edge = x in PILLAR or z in PILLAR
                b.set(x, y, z, (BASE['pillar'] if (x + y + z) % 5 else BASE['glow']) if edge else BASE['wall'])
    for x in range(PILLAR[0], PILLAR[1] + 1):
        for z in range(PILLAR[0], PILLAR[1] + 1): b.set(x, SPIRE_EXIT - 1, z, BASE['floor'])
    for x in range(15, 21): b.set(x, SPIRE_EXIT - 1, 12, BASE['slab'] + '[type=top]')        # the bridge out
    for x in range(21, 24):
        for z in range(10, 15): b.set(x, SPIRE_EXIT - 1, z, BASE['floor'])
    b.set(22, SPIRE_EXIT, 12, 'minecraft:light_weighted_pressure_plate')
    for k, (x, z, t) in enumerate(SROUTE):
        b.set(x, t, z, BASE['metal'] if k == SCHECK else (BASE['trim'] if k % 2 else BASE['floor']))
    for x in range(4, W - 3, 6):
        for z in (4, 20): b.set(x, H - 2, z, 'minecraft:iron_chain'); b.set(x, H - 3, z, 'minecraft:lantern[hanging=true]')
    for x in (6, 18):
        for z in (0, D - 1): b.set(x, 6, z, BASE['glow']); b.set(x, 15, z, BASE['glow'])
    b.marker(*RM.CTRL, ['bm.gvr', 'bm.gvr_spire', 'bm.gvnew'])
    return b


# ===================================================================== THE TINKER'S BENCH
BENCHES = [(7, 20), (12, 20), (17, 20)]
HATCH = (12, 4, 2)


def bench():
    b = R6.shell()
    for x, z in BENCHES:
        b.set(x, 4, z, 'minecraft:crafting_table'); b.set(x - 1, 4, z, 'minecraft:barrel[facing=up]'); b.set(x + 1, 4, z, BASE['pillar'])
    b.set(*HATCH, 'minecraft:barrel[facing=south]')
    for x in (11, 13): b.set(x, 4, 2, BASE['metal']); b.set(x, 5, 2, BASE['metal'])
    b.set(12, 6, 2, BASE['metal'])
    R6.label_wall(b, 8, 16, 8, 0)
    R6.ctrl(b, 'bench'); return wall_glow(b)


# ===================================================================== THE MASON'S PLAN
GRID0 = (11, 11)          # the 3x3 lodestone grid (floor, y 3): x 11..13, z 11..13; its gold corner at (10, 10)
PLAN0 = (4, 15)           # the plan on its plinth: x 4..6, z 15..17 (blocks at y 5 on a plinth at y 4)


def mason():
    b = R6.shell()
    for x in range(GRID0[0] - 1, GRID0[0] + 4):
        for z in range(GRID0[1] - 1, GRID0[1] + 4): b.set(x, FY, z, BASE['trim'])
    for x in range(GRID0[0], GRID0[0] + 3):
        for z in range(GRID0[1], GRID0[1] + 3): b.set(x, FY, z, 'minecraft:lodestone')
    b.set(GRID0[0] - 1, FY, GRID0[1] - 1, 'minecraft:gold_block')
    for x in range(PLAN0[0] - 1, PLAN0[0] + 4):
        for z in range(PLAN0[1] - 1, PLAN0[1] + 4): b.set(x, 4, z, BASE['pillar'])
    b.set(2, 5, 9, 'minecraft:pale_oak_button[face=wall,facing=east]')
    b.set(1, 5, 9, BASE['pillar'])
    R6.ctrl(b, 'mason'); return wall_glow(b)


# ===================================================================== THE DIG
DIG_X = (9, 15)           # the wall: x 9..15, z 1..23, y 4..14


def dig():
    b = R6.shell()
    for x in range(DIG_X[0], DIG_X[1] + 1):
        for z in range(1, 24):
            for y in range(4, 15): b.set(x, y, z, 'minecraft:deepslate_bricks')
    for z in range(1, 24):
        for x in (DIG_X[0], DIG_X[1]):
            b.set(x, 9, z, 'minecraft:chiseled_deepslate')
    R6.ctrl(b, 'dig'); return wall_glow(b)


def dig_mazes(n=6, seed=6921):
    """veins of mud through the wall (cells x 9..15, z 2..22): one runs from the west face to the east face; the rest stop"""
    rng = random.Random(seed)
    out = []
    while len(out) < n:
        X0, X1, Z0, Z1 = DIG_X[0], DIG_X[1], 2, 22
        z = rng.randrange(5, 20); path = [(X0, z)]; x = X0
        while x < X1:
            dx, dz = rng.choice([(1, 0), (1, 0), (0, 1), (0, -1), (0, 1), (0, -1)])
            nx, nz = x + dx, z + dz
            if not (Z0 <= nz <= Z1) or (nx, nz) in path: continue
            if sum((nx + a, nz + c) in path for a, c in ((1, 0), (-1, 0), (0, 1), (0, -1))) != 1: continue
            x, z = nx, nz; path.append((x, z))
        cells = set(path)
        def add_branch(start, length):
            bx, bz = start; br = []
            for _ in range(length):
                opts = [(bx + a, bz + c) for a, c in ((1, 0), (-1, 0), (0, 1), (0, -1))]
                rng.shuffle(opts)
                for nx, nz in opts:
                    if not (X0 <= nx <= X1 - 1 and Z0 <= nz <= Z1) or (nx, nz) in cells: continue
                    if sum((nx + a, nz + c) in cells for a, c in ((1, 0), (-1, 0), (0, 1), (0, -1))) != 1: continue
                    cells.add((nx, nz)); br.append((nx, nz)); bx, bz = nx, nz; break
                else: break
            return br
        for _ in range(rng.randint(5, 8)):
            add_branch(rng.choice(path[1:-2]), rng.randint(2, 6))
        for _ in range(3):                                   # false starts from the west face
            zz = rng.randrange(Z0, Z1 + 1)
            if (X0, zz) in cells or any((X0, zz + d) in cells for d in (-1, 1)): continue
            cells.add((X0, zz)); add_branch((X0, zz), rng.randint(2, 5))
        # (only the true vein reaches the east face)
        if sum(1 for c in cells if c[0] == X1) != 1: continue
        out.append(sorted(cells))
    return out


# ===================================================================== EVENTS: BLOCK PARTY, RED LIGHT GREEN LIGHT, MEMORY MATCH
BP_TILES = [(4 + 3 * c, 4 + 3 * r) for c in range(6) for r in range(6)]       # tile centres (3x3 each, x/z 3..20)
BP_COLS = ['red', 'blue', 'lime', 'yellow', 'purple', 'orange']


def party():
    b = R6.shell()
    for x in range(1, 24):
        for z in range(1, 24):
            b.set(x, FY, z, 'minecraft:air'); b.set(x, 2, z, 'minecraft:air'); b.set(x, 1, z, 'minecraft:air'); b.set(x, 0, z, 'minecraft:hay_block')
            for y in (4, 5): b.set(x, y, z, 'minecraft:air')
    for x in range(3, 21):
        for z in range(3, 21): b.set(x, FY, z, 'minecraft:white_concrete')
    for x in (1, 2):
        for z in range(11, 14): b.set(x, FY, z, BASE['floor'])
    for x in range(4, W - 3, 6):
        for z in (6, 18): b.set(x, 14, z, 'minecraft:iron_chain'); b.set(x, 13, z, 'minecraft:lantern[hanging=true]')
    R6.ctrl(b, 'party'); return b


def redlight():
    b = R6.shell()
    for z in range(1, 24):
        b.set(3, FY, z, 'minecraft:white_concrete'); b.set(21, FY, z, 'minecraft:gold_block')
    for x in range(22, 24):
        for z in range(9, 16): b.set(x, 4, z, 'minecraft:air')
    b.set(23, 4, 12, BASE['pillar']); b.set(23, 5, 12, BASE['pillar'])
    R6.ctrl(b, 'redlight'); return b


MM_CARDS = [(x, z) for z in (6, 10, 14, 18) for x in (6, 10, 14, 18)]
MM_ITEMS = ['minecraft:diamond', 'minecraft:emerald', 'minecraft:gold_ingot', 'minecraft:apple', 'minecraft:bone', 'minecraft:feather', 'minecraft:redstone', 'minecraft:lapis_lazuli']


def memory():
    b = R6.shell()
    for x, z in MM_CARDS:
        b.set(x, 4, z, BASE['pillar'])
    R6.ctrl(b, 'memory'); return wall_glow(b)


def mm_shuffles(n=12, seed=6922):
    rng = random.Random(seed); out = []
    for _ in range(n):
        d = [i // 2 for i in range(16)]; rng.shuffle(d); out.append(d)
    return out


NAMES = {'isles': 'The Sky Isles', 'spire': 'The Spire', 'bench': "The Tinker's Bench", 'mason': "The Mason's Plan", 'dig': 'The Dig',
         'party': 'Block Party', 'redlight': 'Red Light, Green Light', 'memory': 'Memory Match'}
MAIN = {'isles': isles, 'spire': spire, 'bench': bench, 'mason': mason, 'dig': dig}
EVS = {'party': party, 'redlight': redlight, 'memory': memory}
P75.KINDS += list(MAIN)
for _k, _f in list(MAIN.items()) + list(EVS.items()):
    P75.EXTRA_ROOMS[_k] = _f
    R6.NAMES[_k] = NAMES[_k]
P75.SIZE['spire'] = (25, SPIRE_H, 25)
P75.ROOM_DY['spire'] = SPIRE_EXIT - 4
P75.ROOM_MAXY['spire'] = P75.Y0 + 5
for _t, _ks in {1: ['bench', 'mason', 'dig'], 2: ['isles', 'bench', 'mason', 'dig'], 3: ['isles', 'spire', 'bench', 'mason', 'dig'],
                4: ['isles', 'spire', 'bench', 'mason', 'dig'], 5: ['isles', 'spire', 'bench', 'dig']}.items():
    P75.TIER_POOL[_t] += _ks
for _t in range(1, 6):
    P75.EVENT_POOL[_t] += ['party', 'redlight', 'memory']
PUZ = ['spire', 'bench', 'mason', 'dig']
FIGHTS = ['guards', 'ambush', 'pit', 'isles']
P110.TRAV.append('spire')


# ===================================================================== recipes (the Tinker's Bench)
RECIPES = {   # tier: [(target item, what to call it, the parts, the extras, a hint)]
    1: [('compass', 'a Compass', [('iron_ingot', 4), ('redstone', 1)], [('gold_ingot', 2), ('string', 2)], 'Iron round a spark of redstone.'),
        ('clock', 'a Clock', [('gold_ingot', 4), ('redstone', 1)], [('iron_ingot', 2), ('string', 2)], 'Gold round a spark of redstone.')],
    2: [('lantern', 'a Lantern', [('iron_ingot', 1), ('coal', 1), ('stick', 1)], [('copper_ingot', 2), ('string', 1)], 'A torch in a cage of nuggets. Make the torch - and the nuggets - first.'),
        ('bow', 'a Bow', [('oak_planks', 2), ('string', 3)], [('feather', 2), ('flint', 1)], 'Sticks first - three of them - then string them.')],
    3: [('crossbow', 'a Crossbow', [('iron_ingot', 2), ('oak_planks', 1), ('stick', 4), ('string', 2)], [('feather', 1), ('copper_ingot', 2)], 'It needs a tripwire hook. Make that first.'),
        ('spyglass', 'a Spyglass', [('copper_ingot', 2), ('amethyst_shard', 1)], [('glass', 2), ('iron_ingot', 1)], 'Copper tube, amethyst lens.')],
    4: [('hopper', 'a Hopper', [('iron_ingot', 5), ('oak_log', 2)], [('cobblestone', 4), ('redstone', 1)], 'Iron round a chest. Planks for the chest first.'),
        ('piston', 'a Piston', [('oak_log', 1), ('cobblestone', 4), ('iron_ingot', 1), ('redstone', 1)], [('copper_ingot', 2), ('string', 1)], 'Planks on top, stone round iron, redstone below.')],
    5: [('observer', 'an Observer', [('cobblestone', 6), ('redstone', 2), ('quartz', 1)], [('iron_ingot', 2), ('gold_ingot', 1)], 'Stone, a redstone line, a quartz eye.'),
        ('dispenser', 'a Dispenser', [('cobblestone', 7), ('redstone', 1), ('string', 3), ('oak_planks', 2)], [('feather', 1), ('flint', 1)], 'It holds a bow. Make the sticks, then the bow, then the rest.')]}
LEFTOVER = sorted({i for t in RECIPES.values() for r in t for i, _n in r[2] + r[3]} | {r[0] for t in RECIPES.values() for r in t} |
                  {'iron_nugget', 'torch', 'tripwire_hook', 'chest', 'oak_planks', 'stick', 'bow'})


def generate(G):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    label, sign, vbutton, press, themed, crew_say, oops, choose = P110.helpers(G)
    inst = lambda f: f'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run function {f}'
    pot = lambda n: [f'scoreboard players set #c bm.rng {n}', inst('bm:p75/pot_add')]
    crew = '@a[tag=bm.gvp,distance=..30]'
    def big(t_, sub, col=GAME, who=crew):
        return [f'title {who} times 5 40 10', title(who, 'title', T(t_, col, bold=True)), title(who, 'subtitle', T(sub, 'gray'))]
    objs = ['bm.gvcpk']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs

    # ================================================================== dispatch, names, tags
    ks = list(MAIN) + list(EVS)
    G.FUNCS['p70/r/init'] += [f'execute if entity @s[tag=bm.gvr_{k}] run return run function bm:p112/{k}/init' for k in ks]
    G.FUNCS['p70/r/tick'] += [f'execute if entity @s[tag=bm.gvr_{k}] run return run function bm:p112/{k}/tick' for k in ks]
    k0 = next(i for i, l in enumerate(G.FUNCS['p70/r/init']) if 'tag @s add bm.gvnopick' in l)
    G.FUNCS['p70/r/init'][k0:k0] = [f'execute if entity @s[tag=bm.gvr_{k}] run tag @s add bm.gvnopick' for k in EVS] + \
                                   [f'execute if entity @s[tag=bm.gvr_{k}] run tag @s add bm.gvpuz' for k in PUZ]
    G.FUNCS['p70/solved'] += [f'execute if entity @s[tag=bm.gvr_{k}] as @a[tag=bm.gvp,distance=..300] if score @s bm.gvi = #gi bm.rng run ' +
                              title('@s', 'actionbar', [T(NAMES[k], GOLD, bold=True), T(' - beaten. The way on is open.', 'gray')]) for k in ks] + \
                             [f'execute if entity @s[tag=bm.gvr_{k}] if score @s bm.gvf matches 0 run function bm:p76/flawless' for k in PUZ] + \
                             ['execute if entity @s[tag=bm.gvr_spire] run function bm:p112/spire/open']
    # (the turns: the Sky Isles is a fight)
    # (2.82b: the fights may come round again - a tier has only a few kinds of fight, and once each was used the 'none twice'
    #  rule sent every later fight turn back to the whole list, nearly all puzzles. Now a fight never repeats the one just before
    #  it, but may come again later; Tier I fights the Ambush too, so it has two to take turns)
    for t in range(1, 6):
        tp_ = P75.TIER_POOL[t]
        fights = ['guards'] + [k for k in FIGHTS[1:] if k in tp_ or (t == 1 and k == 'ambush')]
        puzzles = [k for k in tp_ if k not in FIGHTS]
        for nm_, pool in (('fight', fights), ('puzzle', puzzles)):
            ids = [P75.KINDS.index(k) for k in pool]
            again = (['execute if score #r bm.rng = #lastf bm.rng run return run function bm:p104/lay/fight%d' % t] if nm_ == 'fight' and len(ids) > 1 else
                     ['function bm:p75/lay/bit', f'execute if score #q2 bm.rng matches 1 run return run function bm:p104/lay/{nm_}{t}'] if nm_ == 'puzzle' else [])
            G.FUNCS[f'p104/lay/{nm_}{t}'] = ['scoreboard players add #try bm.rng 1', f'execute if score #try bm.rng matches 25.. run return run function bm:p75/lay/pick{t}',
                                             f'execute store result score #i bm.rng run random value 0..{len(ids) - 1}'] + \
                [f'execute if score #i bm.rng matches {i} run scoreboard players set #r bm.rng {j}' for i, j in enumerate(ids)] + \
                [f'execute if score #r bm.rng matches {P75.KINDS.index(k)} if score #cy bm.rng matches {my + 1}.. run return run function bm:p104/lay/{nm_}{t}'
                 for k, my in P75.ROOM_MAXY.items() if k in pool] + again + \
                (['scoreboard players operation #lastf bm.rng = #r bm.rng'] if nm_ == 'fight' else []) + \
                ['function bm:p75/lay/bit', 'execute if score #q2 bm.rng matches 0 run scoreboard players operation #pool bm.rng += #bit bm.rng']   # (a fight met again: its bit is set already)
    G.FUNCS['p75/lay/rooms'].insert(0, 'scoreboard players set #lastf bm.rng -1')
    # (2.82b: an event room only ever stands in on a puzzle's turn - up to three a heist used to eat the fight turns too, which
    #  left one or two fights a heist. Every fight turn is a fight now)
    lr = G.FUNCS['p75/lay/room']
    ev = [i for i, l in enumerate(lr) if 'if function bm:p75/lay/can_event run return run function bm:p75/lay/event' in l]
    assert len(ev) == 1, 'the event roll moved'
    lr[ev[0]] = lr[ev[0]].replace('execute if score #ev', 'execute if score #par bm.rng matches 1 if score #ev')
    lr[ev[0]:ev[0]] = ['scoreboard players operation #par bm.rng = #q bm.rng', 'scoreboard players operation #par bm.rng %= #2 bm.rng']

    EVALL = [k for k in P75.EXTRA_ROOMS if k not in P75.KINDS]
    for k in EVS:
        fn(f'admin/room_{k}', [f'scoreboard players set #frm bm.gvv {EVALL.index(k) + 1}', tellraw('@s', [T('The next event room drawn is ' + NAMES[k] + '.', 'gray')])])

    # ================================================================== THE SKY ISLES
    fn('p112/isles/init', ['function bm:p70/ctx', 'scoreboard players operation @s bm.gvy3 = #gt bm.rng',
                           f'execute if score #gt bm.rng matches ..2 run fill {rel(1, 0, 1)} {rel(23, 0, 23)} minecraft:hay_block',
                           sign(rel(2, 7, 12), 'THE SKY ISLES', 'Islands over a long drop. Fight on - and keep your footing. Knock a guard off and it\'s gone.')])
    void_box = f'positioned {relf(0.6, -7, 0.6)} as @a[tag=bm.gvp,dx=22.8,dy=7.5,dz=22.8]'
    fn('p112/isles/tick', ['execute if score @s bm.gvs matches 3 run return 0',
                           f'execute {void_box} at @s run function bm:p112/isles/fell',
                           f'execute positioned {relf(0.6, -7, 0.6)} as @e[tag=bm.gvg,dx=22.8,dy=7.5,dz=22.8] at @s run function bm:p112/isles/gone',
                           'execute if score @s bm.gvs matches 1..2 if score @s bm.gvtm matches 1800 run scoreboard players set @s bm.gvf 1',
                           'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..9] run function bm:p112/isles/wave1',
                           'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #20 bm.rng',
                           'execute unless score #q bm.rng matches 0 run return 0',
                           'execute store result score #n bm.rng if entity @e[tag=bm.gvg,distance=..20]',
                           'execute if score @s bm.gvs matches 1 if score #n bm.rng matches 0 run function bm:p112/isles/wave2',
                           'execute if score @s bm.gvs matches 2 if score #n bm.rng matches 0 run function bm:p70/solved'])
    def wave(extra):
        return ['scoreboard players set @s bm.gvtm 0', 'function bm:p70/ctx', 'execute store result score #n bm.rng if entity @a[tag=bm.gvp,distance=..300]',
                'scoreboard players operation #n bm.rng += #gt bm.rng', f'scoreboard players add #n bm.rng {extra}'] + \
               [f'execute if score #n bm.rng matches {i + 1}.. positioned {rel(ISLE_SPAWN[i % 8][0], 4, ISLE_SPAWN[i % 8][1])} run function bm:p70/guard' for i in range(10)]
    fn('p112/isles/wave1', ['scoreboard players set @s bm.gvs 1'] + wave(0) + [crew_say('Guards on the islands!', 'red', 30)])
    breeze = snbt({'Tags': ['bm.gvg', 'bm.gvnew2', 'bm.seen'], 'PersistenceRequired': B(1), 'CustomName': T('Vault Gale', '#c0e0ff'), 'DeathLootTable': 'bm:gv/guard'})
    fn('p112/isles/wave2', ['scoreboard players set @s bm.gvs 2'] + wave(1) +
       [f'execute positioned {rel(12, 4, 12)} run function bm:p70/captain'] +
       [f'execute if score #gt bm.rng matches {3 + i}.. positioned {rel(*((6, 4, 5), (18, 4, 19), (18, 4, 5))[i])} run function bm:p112/isles/breeze' for i in range(3)] +
       [crew_say('More - and something on the wind!' , 'red', 30)])
    fn('p112/isles/breeze', [f'summon minecraft:breeze ~ ~ ~ {breeze}', 'function bm:p70/guard_set'])
    fn('p112/isles/gone', ['particle minecraft:poof ~ ~ ~ 0.4 0.4 0.4 0.02 10', 'kill @s'])
    fn('p112/isles/fell', ['execute if entity @e[type=minecraft:marker,tag=bm.gvr_isles,distance=..30,sort=nearest,limit=1,scores={bm.gvy3=..2}] run return run function bm:p112/isles/hay',
                           'function bm:p112/void_ko'])
    fn('p112/isles/hay', ['execute at @e[type=minecraft:marker,tag=bm.gvr_isles,distance=..30,sort=nearest,limit=1] run tp @s ' + rel(2, 4, 12) + ' -90 0',
                          title('@s', 'actionbar', T('Down into the hay! Back to the start.', 'red'))])
    # (the void: knocked out, as if you'd fallen in battle - it costs a try; your things stay with you)
    fn('p112/void_ko', ['tag @s add bm.gvdead', 'function bm:p75/ko', 'function bm:p104/ko_mark', 'effect give @s minecraft:resistance 4 4 true',
                        'effect give @s minecraft:instant_health 1 3 true', 'function bm:p70/revive',
                        title('@s', 'actionbar', T('Into the void - the gang hauls you back to the den.', 'red'))])

    # ================================================================== THE SPIRE
    sx, sz, st = SROUTE[SCHECK]
    fn('p112/spire/init', ['function bm:p70/ctx',
                           label(relf(sx + 0.5, st + 1.6, sz + 0.5), T('CHECKPOINT', GOLD, bold=True), 0.5),
                           sign(rel(2, 7.5, 12), 'THE SPIRE', 'Up round the pillar to the top - one block at a time. Touch the gold CHECKPOINT and a fall brings you back to it.')])
    fn('p112/spire/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'execute if score @s bm.gvs matches 0 run scoreboard players set @s bm.gvs 1',
                           'execute if score @s bm.gvtm matches 3000 run scoreboard players set @s bm.gvf 1',
                           'scoreboard players operation #me bm.rng = @s bm.gvq',
                           f'execute positioned {relf(sx + 0.5, st + 1, sz + 0.5)} as @a[tag=bm.gvp,distance=..0.9] unless score @s bm.gvcpk = #me bm.rng at @s run function bm:p112/spire/cp',
                           f'execute positioned {relf(3.6, 3.5, 0.6)} as @a[tag=bm.gvp,dx=20,dy=0.1,dz=22.8] at @s run function bm:p112/spire/fell',
                           f'execute unless block {rel(22, SPIRE_EXIT, 12)} minecraft:light_weighted_pressure_plate[power=0] run function bm:p70/solved'])
    fn('p112/spire/cp', ['scoreboard players operation @s bm.gvcpk = #me bm.rng', 'playsound minecraft:block.note_block.chime player @s ~ ~ ~ 1 1.5',
                         title('@s', 'actionbar', [T('Checkpoint! ', GOLD, bold=True), T('A fall brings you back here now.', 'gray')])])
    fn('p112/spire/fell', ['execute if score @s bm.gvcpk = #me bm.rng at @e[type=minecraft:marker,tag=bm.gvr_spire,distance=..30,sort=nearest,limit=1] run return run tp @s ' +
                           relf(sx + 0.5, st + 1, sz + 0.5),
                           'execute at @e[type=minecraft:marker,tag=bm.gvr_spire,distance=..30,sort=nearest,limit=1] run tp @s ' + rel(2, 4, 12) + ' -90 0',
                           title('@s', 'actionbar', T('Down into the hay! Back to the start.', 'red'))])
    fn('p112/spire/open', [f'fill {rel(24, SPIRE_EXIT, 11)} {rel(24, SPIRE_EXIT + 3, 13)} minecraft:air replace minecraft:iron_bars',
                           'execute as @e[type=minecraft:marker,tag=bm.gvcp] if score @s bm.gvi = #gi bm.rng run tp @s ' + rel(25, SPIRE_EXIT, 12) + ' -90 0'])

    # ================================================================== THE TINKER'S BENCH
    def item(i, n, room=True):
        return f'minecraft:{i}[minecraft:custom_data={{bm_room:1b}}]' if room else f'minecraft:{i}'
    fn('p112/bench/init', ['function bm:p70/ctx', 'scoreboard players set @s bm.gvc 0',
                           f'summon minecraft:interaction {relf(12.5, 4, 2.5)} {{Tags:["bm.gvprop","bm.gvhatch"],width:1.2f,height:1.6f,response:1b}}',
                           label(rel(12, 6.6, 2), T("THE FIXER'S HATCH", GOLD, bold=True), 0.5)] +
       [f'execute if score #gt bm.rng matches {t} run ' + c for t in range(1, 6) for c in [f'execute store result score @s bm.gvc run random value {10 * t}..{10 * t + len(RECIPES[t]) - 1}']] +
       [f'execute if score @s bm.gvc matches {10 * t + j} run function bm:p112/bench/r{t}{j}' for t in range(1, 6) for j in range(len(RECIPES[t]))])
    for t, rs in RECIPES.items():
        for j, (tgt, nm, parts, extra, hint) in enumerate(rs):
            fn(f'p112/bench/r{t}{j}', [sign(rel(12, 8.2, 1), "THE TINKER'S BENCH", f'The Fixer wants {nm}. Make it at the benches and hand it in at his hatch. '
                                            f'Not everything you\'re given is needed. ({hint})', 0.6)])
            fn(f'p112/bench/give{t}{j}', [f'give @s {item(i, n)} {n}' for i, n in parts + extra] +
               [title('@s', 'actionbar', [T('The Fixer hands you the parts. ', GOLD, bold=True), T(f'Make {nm}.', 'gray')])])
    fn('p112/bench/tick', ['execute if score @s bm.gvs matches 3 run return 0',
                           'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..10] run function bm:p112/bench/start',
                           'execute if score @s bm.gvtm matches 3600 run scoreboard players set @s bm.gvf 1',
                           'execute as @e[type=minecraft:interaction,tag=bm.gvhatch,distance=..14] if data entity @s interaction at @s run function bm:p112/bench/hatch'])
    fn('p112/bench/start', ['scoreboard players set @s bm.gvs 1', 'scoreboard players operation #rc bm.rng = @s bm.gvc'] +
       [f'execute if score #rc bm.rng matches {10 * t + j} as @a[tag=bm.gvp,distance=..30] run function bm:p112/bench/give{t}{j}' for t in range(1, 6) for j in range(len(RECIPES[t]))])
    fn('p112/bench/hatch', ['tag @s add bm.gvme2', 'execute on target run function bm:p112/bench/hand', 'tag @s remove bm.gvme2', 'data remove entity @s interaction'])
    fn('p112/bench/hand', ['execute as @e[type=minecraft:marker,tag=bm.gvr_bench,distance=..16,sort=nearest,limit=1] run scoreboard players operation #rc bm.rng = @s bm.gvc'] +
       [f'execute if score #rc bm.rng matches {10 * t + j} if items entity @s weapon.mainhand minecraft:{rs[j][0]} run return run function bm:p112/bench/done'
        for t, rs in RECIPES.items() for j in range(len(rs))] +
       [title('@s', 'actionbar', T('"That\'s not what I asked for." (Hold it in your hand.)', 'red'))])
    fn('p112/bench/done', ['item replace entity @s weapon.mainhand with minecraft:air', 'playsound minecraft:block.barrel.close player @a[distance=..16] ~ ~ ~ 1 1',
                           'execute as @e[type=minecraft:marker,tag=bm.gvr_bench,distance=..16,sort=nearest,limit=1] at @s run function bm:p112/bench/won'])
    fn('p112/bench/won', [f'clear {crew} minecraft:{i}[!minecraft:custom_data]' for i in LEFTOVER] + ['kill @e[type=minecraft:item,distance=..16]', 'function bm:p70/solved'])

    # ================================================================== THE MASON'S PLAN
    rng = random.Random(6923)
    MCOL = ['red', 'blue', 'yellow', 'lime']
    MPZ = []
    for j in range(12):
        ncol = 3 if j < 6 else 4
        while True:
            pat = [[rng.randrange(ncol) for _ in range(3)] for _ in range(3)]
            if len({c for row in pat for c in row}) == ncol and pat != [list(r) for r in zip(*pat)]: break
        MPZ.append((pat, 0 if j < 6 else rng.randint(1, 3)))
    def rot(v, k):
        a, b = v
        for _ in range(k): a, b = -b, a
        return a, b
    def stone(c): return f'minecraft:{MCOL[c]}_concrete[minecraft:custom_data={{bm_room:1b}},minecraft:can_place_on={{blocks:"minecraft:lodestone"}}]'
    fn('p112/mason/init', ['function bm:p70/ctx', 'execute store result score @s bm.gvc run random value 0..5', 'execute if score #gt bm.rng matches 3.. run scoreboard players add @s bm.gvc 6'] +
       [f'execute if score @s bm.gvc matches {j} run function bm:p112/mason/p{j}' for j in range(12)] +
       vbutton(2, 5, 9, 'east', 'RESET', col='#ff7a7a') +
       [sign(rel(5, 7.4, 13), "THE MASON'S PLAN", 'Lay the blocks on the lodestone grid to match the plan on the plinth. The gold corners show which way round it goes.', 0.55)])
    for j, (pat, k) in enumerate(MPZ):
        L = []
        for i in range(3):
            for jj in range(3):
                a, b = rot((i - 1, jj - 1), k)
                L.append(f'setblock {rel(PLAN0[0] + 1 + a, 5, PLAN0[1] + 1 + b)} minecraft:{MCOL[pat[i][jj]]}_concrete')
        a, b = rot((-2, -2), k)
        L.append(f'setblock {rel(PLAN0[0] + 1 + a, 4, PLAN0[1] + 1 + b)} minecraft:gold_block')
        fn(f'p112/mason/p{j}', L)
        fn(f'p112/mason/chk{j}', [f'execute unless block {rel(GRID0[0] + i, 4, GRID0[1] + jj)} minecraft:{MCOL[pat[i][jj]]}_concrete run return 0' for i in range(3) for jj in range(3)] +
           ['return 1'])
        need = {}
        for row in pat:
            for c in row: need[c] = need.get(c, 0) + 1
        fn(f'p112/mason/give{j}', [f'give @s {stone(c)} {n + 1}' for c, n in sorted(need.items())])
    fn('p112/mason/tick', ['execute if score @s bm.gvs matches 3 run return 0',
                           'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..12] run function bm:p112/mason/start',
                           'execute if score @s bm.gvtm matches 3000 run scoreboard players set @s bm.gvf 1'] + press('mreset', (2, 5, 9), 'bm:p112/mason/reset') +
       ['scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #10 bm.rng', 'execute unless score #q bm.rng matches 0 run return 0'] +
       [f'execute if score @s bm.gvc matches {j} if function bm:p112/mason/chk{j} run return run function bm:p70/solved' for j in range(12)])
    fn('p112/mason/start', ['scoreboard players set @s bm.gvs 1', 'function bm:p112/mason/hand'])
    fn('p112/mason/hand', [f'clear {crew} *[minecraft:custom_data~{{bm_room:1b}}]'] +
       [f'execute if score @s bm.gvc matches {j} as {crew} run function bm:p112/mason/give{j}' for j in range(12)] +
       [crew_say('The mason\'s blocks: they only go down on the lodestone.', GOLD, 30)])
    fn('p112/mason/reset', [f'fill {rel(GRID0[0], 4, GRID0[1])} {rel(GRID0[0] + 2, 4, GRID0[1] + 2)} minecraft:air', 'function bm:p112/mason/hand'] + oops(2) +
       ['scoreboard players set @s bm.gvf 1', 'playsound minecraft:block.stone.break block @a[distance=..20] ~ ~ ~ 1 0.8'])

    # ================================================================== THE DIG
    MZ = dig_mazes()
    PICK = ('minecraft:stone_pickaxe[minecraft:custom_data={bm_room:1b,bm_digpick:1b},minecraft:can_break={blocks:"minecraft:mud_bricks"},minecraft:unbreakable={},'
            'minecraft:item_name=' + snbt(T("The Fixer's Pick", GOLD)) + ',minecraft:lore=[' + snbt(T('It bites only the mud bricks.', 'gray')) + ']]')
    fn('p112/dig/init', ['function bm:p70/ctx'] + choose('#i', len(MZ), 'p112/dig/m') +
       [sign(rel(4, 7, 12), 'THE DIG', 'Tunnel through the wall with the Fixer\'s pick - it bites only the mud bricks. Most veins end in rock; one goes all the way.', 0.6)])
    for j, cells in enumerate(MZ):
        fn(f'p112/dig/m{j}', [f'fill {rel(x, 4, z)} {rel(x, 5, z)} minecraft:mud_bricks' for x, z in cells])
    fn('p112/dig/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'execute if score @s bm.gvs matches 0 run scoreboard players set @s bm.gvs 1',
                         'execute if score @s bm.gvtm matches 3000 run scoreboard players set @s bm.gvf 1',
                         f'execute positioned {relf(0.6, 3.5, 0.6)} as @a[tag=bm.gvp,dx=7.8,dy=3,dz=22.8] unless items entity @s container.* *[minecraft:custom_data~{{bm_digpick:1b}}] run function bm:p112/dig/pick',
                         'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #10 bm.rng',
                         'execute if score #q bm.rng matches 0 positioned ~-12.5 ~-4 ~-12.5 run kill @e[type=minecraft:item,dx=24,dy=15,dz=24]',
                         f'execute positioned {relf(17, 3.5, 0.6)} if entity @a[tag=bm.gvp,dx=5.8,dy=3,dz=22.8] positioned as @s run function bm:p70/solved'])
    fn('p112/dig/pick', [f'give @s {PICK}', title('@s', 'actionbar', [T("The Fixer's pick. ", GOLD, bold=True), T('It only bites the mud bricks.', 'gray')])])

    # ================================================================== BLOCK PARTY
    NR = {1: 8, 2: 8, 3: 9, 4: 10, 5: 10}
    NK = {1: 4, 2: 4, 3: 5, 4: 5, 5: 6}
    CD = {1: 80, 2: 72, 3: 64, 4: 56, 5: 50}
    fn('p112/party/init', ['function bm:p70/ctx'] + [f'summon minecraft:marker {rel(x, 4, z)} {{Tags:["bm.gvprop","bm.gvbt"]}}' for x, z in BP_TILES] +
       [f'execute if score #gt bm.rng matches {t} run scoreboard players set @s bm.gvy1 {NR[t]}' for t in range(1, 6)] +
       [f'execute if score #gt bm.rng matches {t} run scoreboard players set @s bm.gvy2 {NK[t]}' for t in range(1, 6)] +
       [f'execute if score #gt bm.rng matches {t} run scoreboard players set @s bm.gvy3 {CD[t]}' for t in range(1, 6)] +
       ['scoreboard players set @s bm.gvc 0', 'scoreboard players set @s bm.gvw 0',
        sign(rel(1.5, 7.5, 12), 'BLOCK PARTY', 'A colour is called - get on it before the rest of the floor drops away! Each round someone survives earns a coin.', 0.6)])
    fn('p112/party/tick', ['execute if score @s bm.gvs matches 3 run return 0',
                           'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..10] run function bm:p112/party/round',
                           'execute if score @s bm.gvs matches 0 run return 0',
                           'scoreboard players remove @s bm.gvx 1',
                           f'execute positioned {relf(0.6, -2, 0.6)} as @a[tag=bm.gvp,dx=22.8,dy=3.4,dz=22.8,tag=!bm.gvout] at @s run function bm:p112/party/fall',
                           'execute if score @s bm.gvs matches 1 run function bm:p112/party/count',
                           'execute if score @s bm.gvs matches 1 if score @s bm.gvx matches ..0 run function bm:p112/party/drop',
                           'execute if score @s bm.gvs matches 2 if score @s bm.gvx matches ..0 run function bm:p112/party/after'])
    tiles = 'execute as @e[type=minecraft:marker,tag=bm.gvbt,distance=..16] at @s run function bm:p112/party/tile'
    fn('p112/party/tile', ['execute store result score @s bm.gvy1 run random value 0..5', 'execute if score @s bm.gvy1 >= #nk bm.rng run scoreboard players operation @s bm.gvy1 %= #nk bm.rng'] +
       [f'execute if score @s bm.gvy1 matches {i} run fill ~-1 ~-1 ~-1 ~1 ~-1 ~1 minecraft:{c}_concrete' for i, c in enumerate(BP_COLS)])
    fn('p112/party/round', ['scoreboard players add @s bm.gvc 1', 'execute if score @s bm.gvc > @s bm.gvy1 run return run function bm:p112/party/end',
                            'scoreboard players set @s bm.gvs 1', 'scoreboard players operation #nk bm.rng = @s bm.gvy2', tiles,
                            'execute as @e[type=minecraft:marker,tag=bm.gvbt,distance=..16,sort=random,limit=1] run scoreboard players operation #ch bm.rng = @s bm.gvy1',
                            'scoreboard players operation @s bm.gvk = #ch bm.rng',
                            'scoreboard players operation @s bm.gvx = @s bm.gvy3', 'scoreboard players operation #s bm.rng = @s bm.gvc', 'scoreboard players operation #s bm.rng *= #4 bm.rng',
                            'scoreboard players operation @s bm.gvx -= #s bm.rng', 'execute if score @s bm.gvx matches ..24 run scoreboard players set @s bm.gvx 24',
                            'tag @a[tag=bm.gvp,distance=..30] remove bm.gvout',
                            f'execute positioned {relf(0.6, 3.5, 0.6)} as @a[tag=bm.gvp,dx=0.9,dy=3,dz=22.8] run tp @s {rel(12, 4, 12)}'] +
       [f'execute if score #ch bm.rng matches {i} run function bm:p112/party/call{i}' for i in range(6)])
    PCOL = {'red': '#ff5050', 'blue': '#5a8aff', 'lime': '#7dff6a', 'yellow': '#ffe050', 'purple': '#b060ff', 'orange': '#ff9a30'}
    for i, c in enumerate(BP_COLS):
        fn(f'p112/party/call{i}', [f'title {crew} times 0 30 5', title(crew, 'title', T(c.upper() + '!', PCOL[c], bold=True)),
                                   f'playsound minecraft:block.note_block.bit block {crew} ~ ~ ~ 1 {0.8 + 0.1 * i:.1f}'])
    fn('p112/party/count', ['scoreboard players operation #q bm.rng = @s bm.gvx', 'scoreboard players operation #q bm.rng %= #10 bm.rng',
                            'execute if score #q bm.rng matches 0 run playsound minecraft:block.note_block.hat block @a[distance=..24] ~ ~ ~ 0.8 1.4'])
    fn('p112/party/drop', ['scoreboard players set @s bm.gvs 2', 'scoreboard players set @s bm.gvx 40', 'scoreboard players operation #ch bm.rng = @s bm.gvk',
                           'execute as @e[type=minecraft:marker,tag=bm.gvbt,distance=..16] unless score @s bm.gvy1 = #ch bm.rng at @s run fill ~-1 ~-1 ~-1 ~1 ~-1 ~1 minecraft:air',
                           f'execute positioned {relf(0.6, 3.5, 0.6)} as @a[tag=bm.gvp,dx=2,dy=3,dz=22.8,tag=!bm.gvout] at @s run function bm:p112/party/fall',
                           'playsound minecraft:block.stone.break block @a[distance=..24] ~ ~ ~ 1 0.6'])
    fn('p112/party/fall', ['tag @s add bm.gvout', 'execute as @e[type=minecraft:marker,tag=bm.gvr_party,distance=..30,sort=nearest,limit=1] run function bm:p112/party/miss'])
    fn('p112/party/miss', oops(3) + ['scoreboard players set @s bm.gvf 1'])
    fn('p112/party/after', ['execute if entity @a[tag=bm.gvp,distance=..20,tag=!bm.gvout] run function bm:p112/party/kept', 'function bm:p112/party/round'])
    fn('p112/party/kept', ['scoreboard players add @s bm.gvw 1'] + pot(1) + [crew_say('Round survived - a coin for the pot.', GOLD, 30)])
    fn('p112/party/end', ['scoreboard players set @s bm.gvs 3', f'fill {rel(1, 3, 1)} {rel(23, 3, 23)} minecraft:white_concrete',
                          'tag @a[tag=bm.gvp,distance=..30] remove bm.gvout',
                          f'execute positioned {relf(0.6, -2, 0.6)} as @a[tag=bm.gvp,dx=22.8,dy=3.4,dz=22.8] run tp @s {rel(12, 4, 12)}',
                          'scoreboard players operation #h bm.rng = @s bm.gvy1', 'scoreboard players operation #h bm.rng *= #3 bm.rng', 'scoreboard players operation #h bm.rng /= #4 bm.rng',
                          'execute if score @s bm.gvw >= #h bm.rng run function bm:p112/party/won', 'function bm:p70/solved'])
    fn('p112/party/won', big('PARTY ANIMALS!', 'The floor stays put - and the Fixer\'s impressed') + pot(6))

    # ================================================================== RED LIGHT, GREEN LIGHT
    WATCH = snbt({'Tags': ['bm.gvprop', 'bm.gvwatch'], 'item': {'id': 'minecraft:carved_pumpkin', 'count': Int(1)}, 'item_display': 'fixed', 'Rotation': [F(270), F(0)],
                  'interpolation_duration': Int(6), 'brightness': {'block': 15, 'sky': 15},
                  'transformation': {'left_rotation': IDENT, 'right_rotation': IDENT, 'translation': [F(0)] * 3, 'scale': [F(3)] * 3}})
    face = lambda yaw: f'execute as @e[type=minecraft:item_display,tag=bm.gvwatch,distance=..16] run data merge entity @s {{start_interpolation:0,transformation:{{left_rotation:[0f,{math.sin(math.radians(yaw) / 2):.4f}f,0f,{math.cos(math.radians(yaw) / 2):.4f}f]}}}}'
    fn('p112/redlight/init', ['function bm:p70/ctx', f'summon minecraft:item_display {relf(23.5, 8, 12.5)} {WATCH}', 'scoreboard players set @s bm.gvc 0',
                              sign(rel(2, 7, 12), 'RED LIGHT, GREEN LIGHT', 'Run while the watcher looks away. When it turns round - FREEZE. Anyone it sees moving goes back to the line. Everyone over the gold line!', 0.6)])
    fn('p112/redlight/tick', ['execute if score @s bm.gvs matches 3 run return 0',
                              'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..12] run function bm:p112/redlight/start',
                              'execute if score @s bm.gvs matches 0 run return 0',
                              'scoreboard players remove @s bm.gvx 1', 'scoreboard players add @s bm.gvc 1',
                              'execute if score @s bm.gvs matches 1 if score @s bm.gvx matches ..0 run function bm:p112/redlight/next',
                              'execute if score @s bm.gvs matches 2 if score @s bm.gvx matches ..0 run function bm:p112/redlight/green',
                              'execute if score @s bm.gvs matches 2 if score @s bm.gvw matches ..-1 as @a[tag=bm.gvp,distance=..24] at @s run function bm:p112/redlight/watch',
                              'execute if score @s bm.gvs matches 2 if score @s bm.gvw matches 1.. run scoreboard players remove @s bm.gvw 1',
                              'execute if score @s bm.gvs matches 2 if score @s bm.gvw matches 0 as @a[tag=bm.gvp,distance=..24] run function bm:p112/redlight/mark',
                              'execute if score @s bm.gvs matches 2 if score @s bm.gvw matches 0 run scoreboard players set @s bm.gvw -1',
                              f'execute positioned {relf(21, 3.5, 0.6)} if entity @a[tag=bm.gvp,dx=2.4,dy=3,dz=22.8] positioned as @s run function bm:p112/redlight/check',
                              'execute if score @s bm.gvc matches 2400.. run function bm:p112/redlight/timeup'])
    fn('p112/redlight/start', ['scoreboard players set @s bm.gvc 0', 'function bm:p112/redlight/green', crew_say('GREEN LIGHT - run!', '#7dff6a', 30)])
    fn('p112/redlight/next', ['execute if score @s bm.gvy3 matches 1 run return run function bm:p112/redlight/red', 'function bm:p112/redlight/turn'])
    fn('p112/redlight/green', ['scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvy3 0', 'execute store result score @s bm.gvx run random value 24..70',
                               'execute if score #gt bm.rng matches 4.. run scoreboard players remove @s bm.gvx 10', face(0),
                               title(crew, 'actionbar', T('GREEN LIGHT', '#7dff6a', bold=True))])
    fn('p112/redlight/turn', ['scoreboard players set @s bm.gvy3 1', 'scoreboard players set @s bm.gvx 8', 'playsound minecraft:block.note_block.didgeridoo block @a[distance=..30] ~ ~ ~ 1 1.2',
                              title(crew, 'actionbar', T('...', '#ffe050', bold=True))])
    fn('p112/redlight/red', ['scoreboard players set @s bm.gvs 2', 'scoreboard players set @s bm.gvy3 0', 'execute store result score @s bm.gvx run random value 30..60', 'scoreboard players set @s bm.gvw 4', face(180),
                             'playsound minecraft:entity.warden.sonic_charge block @a[distance=..30] ~ ~ ~ 0.6 1.6', title(crew, 'actionbar', T('RED LIGHT - FREEZE!', 'red', bold=True))])
    fn('p112/redlight/mark', ['execute store result score @s bm.gvy1 run data get entity @s Pos[0] 100', 'execute store result score @s bm.gvy2 run data get entity @s Pos[2] 100'])
    fn('p112/redlight/watch', ['execute store result score #x bm.rng run data get entity @s Pos[0] 100', 'execute store result score #z bm.rng run data get entity @s Pos[2] 100',
                               'scoreboard players operation #x bm.rng -= @s bm.gvy1', 'scoreboard players operation #z bm.rng -= @s bm.gvy2',
                               'execute unless score #x bm.rng matches -6..6 run return run function bm:p112/redlight/caught',
                               'execute unless score #z bm.rng matches -6..6 run function bm:p112/redlight/caught'])
    fn('p112/redlight/caught', ['execute at @e[type=minecraft:marker,tag=bm.gvr_redlight,distance=..30,sort=nearest,limit=1] run tp @s ' + rel(2, 4, 12) + ' -90 0',
                                'function bm:p112/redlight/mark', 'playsound minecraft:entity.villager.no player @a[distance=..30] ~ ~ ~ 1 0.6',
                                title('@s', 'actionbar', T('It saw you move! Back to the line.', 'red')),
                                'execute as @e[type=minecraft:marker,tag=bm.gvr_redlight,distance=..30,sort=nearest,limit=1] run function bm:p112/redlight/miss'])
    fn('p112/redlight/miss', oops(3) + ['scoreboard players set @s bm.gvf 1'])
    fn('p112/redlight/check', [f'execute positioned {relf(0.6, 3.5, 0.6)} if entity @a[tag=bm.gvp,dx=19.6,dy=3,dz=22.8] run return 0', 'function bm:p112/redlight/won'])
    fn('p112/redlight/won', ['scoreboard players set @s bm.gvs 3'] + big('ALL ACROSS!', 'The watcher sulks - the Fixer pays up') + pot(6) + ['function bm:p70/solved'])
    fn('p112/redlight/timeup', ['scoreboard players set @s bm.gvs 3'] + big('TOO SLOW', 'The watcher calls the guards...', 'red') + oops(5) + ['function bm:p70/solved'])

    # ================================================================== MEMORY MATCH
    SH = mm_shuffles()
    MISS = {1: 12, 2: 10, 3: 9, 4: 8, 5: 7}
    card = lambda tags: snbt({'Tags': ['bm.gvprop'] + tags, 'item': {'id': 'minecraft:paper', 'count': Int(1)}, 'item_display': 'fixed', 'brightness': {'block': 15, 'sky': 15},
                              'transformation': {'left_rotation': [F(-0.7071), F(0), F(0), F(0.7071)], 'right_rotation': IDENT, 'translation': [F(0), F(0.03), F(0)], 'scale': [F(0.8)] * 3}})
    fn('p112/memory/init', ['function bm:p70/ctx'] +
       sum(([f'summon minecraft:item_display {relf(x + 0.5, 5, z + 0.5)} {card(["bm.gvmmd", f"bm.gvmmd{i}"])}',
             f'summon minecraft:interaction {relf(x + 0.5, 4, z + 0.5)} {{Tags:["bm.gvprop","bm.gvmm","bm.gvmm{i}"],width:1.1f,height:1.3f,response:1b}}'] for i, (x, z) in enumerate(MM_CARDS)), []) +
       choose('#i', len(SH), 'p112/memory/s') +
       ['execute as @e[type=minecraft:interaction,tag=bm.gvmm,distance=..16] run scoreboard players set @s bm.gvy2 0', 'scoreboard players set @s bm.gvc -1', 'scoreboard players set @s bm.gvw 0',
        'scoreboard players set @s bm.gvx 0'] + [f'execute if score #gt bm.rng matches {t} run scoreboard players set @s bm.gvy3 {MISS[t]}' for t in range(1, 6)] +
       [sign(rel(2, 7, 12), 'MEMORY MATCH', 'Turn two cards at a time (right-click). Find all eight pairs before your misses run out.', 0.6)])
    for j, d in enumerate(SH):
        fn(f'p112/memory/s{j}', [f'scoreboard players set @e[type=minecraft:interaction,tag=bm.gvmm{i},distance=..16,limit=1] bm.gvy1 {d[i]}' for i in range(16)])
    fn('p112/memory/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'execute if score @s bm.gvs matches 0 run scoreboard players set @s bm.gvs 1',
                            'execute if score @s bm.gvx matches 1.. run scoreboard players remove @s bm.gvx 1',
                            'execute if score @s bm.gvx matches 1 run function bm:p112/memory/judge',
                            'execute if score @s bm.gvx matches 1.. as @e[type=minecraft:interaction,tag=bm.gvmm,distance=..16] if data entity @s interaction run data remove entity @s interaction',
                            'execute as @e[type=minecraft:interaction,tag=bm.gvmm,distance=..16] if data entity @s interaction at @s run function bm:p112/memory/click'])
    fn('p112/memory/click', ['data remove entity @s interaction', 'execute unless score @s bm.gvy2 matches 0 run return 0', 'scoreboard players set @s bm.gvy2 1',
                             'scoreboard players operation #sym bm.rng = @s bm.gvy1'] +
       [f'execute if score #sym bm.rng matches {s} as @e[type=minecraft:item_display,tag=bm.gvmmd,distance=..1.2,limit=1,sort=nearest] run data modify entity @s item.id set value "{it}"' for s, it in enumerate(MM_ITEMS)] +
       ['playsound minecraft:item.book.page_turn block @a[distance=..16] ~ ~ ~ 1 1.2',
        'execute as @e[type=minecraft:marker,tag=bm.gvr_memory,distance=..16,sort=nearest,limit=1] run function bm:p112/memory/flip'])
    fn('p112/memory/flip', ['execute if score @s bm.gvc matches -1 run return run scoreboard players operation @s bm.gvc = #sym bm.rng',
                            'scoreboard players operation @s bm.gvk = #sym bm.rng', 'scoreboard players set @s bm.gvx 16'])
    fn('p112/memory/judge', ['execute if score @s bm.gvc = @s bm.gvk run function bm:p112/memory/pair', 'execute unless score @s bm.gvc = @s bm.gvk run function bm:p112/memory/nope',
                             'scoreboard players set @s bm.gvc -1'])
    fn('p112/memory/pair', ['execute as @e[type=minecraft:interaction,tag=bm.gvmm,distance=..16,scores={bm.gvy2=1}] run scoreboard players set @s bm.gvy2 2',
                            'scoreboard players add @s bm.gvw 1', 'playsound minecraft:entity.experience_orb.pickup block @a[distance=..16] ~ ~ ~ 1 1.3',
                            'execute if score @s bm.gvw matches 8.. run function bm:p112/memory/won'])
    fn('p112/memory/nope', ['execute as @e[type=minecraft:interaction,tag=bm.gvmm,distance=..16,scores={bm.gvy2=1}] at @s run function bm:p112/memory/hide',
                            'scoreboard players remove @s bm.gvy3 1', 'scoreboard players set @s bm.gvf 1', 'playsound minecraft:block.note_block.bass block @a[distance=..16] ~ ~ ~ 1 0.7',
                            crew_say([T('No match. Misses left: ', 'red'), {'score': {'name': '@e[type=minecraft:marker,tag=bm.gvr_memory,limit=1,sort=nearest]', 'objective': 'bm.gvy3'}, 'color': 'white'}], r=20),
                            'execute if score @s bm.gvy3 matches ..0 run function bm:p112/memory/lost'])
    fn('p112/memory/hide', ['scoreboard players set @s bm.gvy2 0', 'execute as @e[type=minecraft:item_display,tag=bm.gvmmd,distance=..1.2,limit=1,sort=nearest] run data modify entity @s item.id set value "minecraft:paper"'])
    fn('p112/memory/won', ['scoreboard players set @s bm.gvs 3'] + big('A PERFECT MEMORY', 'Eight pairs - the Fixer is impressed') + pot(6) + ['function bm:p70/solved'])
    # (2.82g: out of misses the door stays shut - a try lost, the cards reshuffled, the misses back - as any puzzle's failure)
    fn('p112/memory/lost', big('OUT OF MISSES', 'A try lost - the cards shuffle themselves...', 'red') + oops(4) +
       ['function bm:p70/ctx', 'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng at @s run function bm:p90/lose_try',
        'execute as @e[type=minecraft:interaction,tag=bm.gvmm,distance=..16] at @s run function bm:p112/memory/hide'] +
       choose('#i', len(SH), 'p112/memory/s') +
       ['scoreboard players set @s bm.gvc -1', 'scoreboard players set @s bm.gvw 0', 'scoreboard players set @s bm.gvx 0'] +
       [f'execute if score #gt bm.rng matches {t} run scoreboard players set @s bm.gvy3 {MISS[t]}' for t in range(1, 6)])

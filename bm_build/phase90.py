"""2.67: THE VAULT GROWS - dearer tiers, double heists, alien heists, and five new kinds of room.

THE FEE BY TIER: Tier I 2 Tokens, II 3, III 4, IV 5, V 6 (each crew member, into the Lucky Pool). The better tiers pay
  better (more shares, the bigger prize caps), so they cost more to walk into.
DOUBLE HEIST (1 in 10): twice the rooms - and two more shares each, and better odds at the Fixer's prize.
ALIEN HEIST (1 in 8): the Vorn got there first - every room rebuilt in their white-and-cyan steel, Vorn troopers on
  guard, the invasion's own loot in the haul.
NEW ROOMS (the event draw - one or two a heist, three from Tier III, more in a double heist):
  THE SANCTUARY (rare)     a quiet spring: everyone is healed on arrival, and each of you may take one boon from its
                           shrines - Might (Strength), Swiftness (Speed) or the Bulwark (Resistance), five minutes.
  THE STALKER'S WARD       pitch dark. Something moves when you don't look at it. Find and pull the three levers.
  THE BLAZE FORGE          the Nether's heat: three waves - magma cubes, blazes, then the Forge Keeper.
  THE VOID GARDEN (III+)   end-stone islands over a drop; shulkers float you off your feet. Wake the three Eye shrines.
  THE HOLLOW RELIQUARY (rare, III+)  a shard of the Hollow Throne: watch the seals flare, then strike them in that order.
                           Done: a Hollow relic for each of you, in The Haul.
"""
import random
from items import T, ITEMS
from nbt import snbt, B, F, Int
from nbt import D as Dd
from structures import Build
import phase70_rooms as RM
import phase75 as P75
import phase75_rooms as R5
import phase76_rooms as R6
from phase75_rooms import BASE, wall_glow

GOLD = '#ffcf40'
FEE_T = {1: 2, 2: 3, 3: 4, 4: 5, 5: 6}
DOUBLE_IN, SCIFI_IN = 10, 8                     # (one heist in ...)
FY = RM.FY
W, H, D = RM.W, RM.H, RM.D
NAMES = {'sanctum': 'The Sanctuary', 'hunted': "The Stalker's Ward", 'forge': 'The Blaze Forge', 'voidg': 'The Void Garden', 'hollow': 'The Hollow Reliquary'}
RESTS = ('rest', 'sanctum')                    # (2.67: the rest rooms - at most one a heist)
RARE = {'sanctum': 35, 'hollow': 25}           # (a rare room, drawn: kept only this often (%), else the draw goes again)

# ---- the Vorn's look (an alien heist: every template once more in this)
R5.THEMES[6] = dict(wall='minecraft:white_concrete', trim='minecraft:cyan_concrete', pillar='minecraft:purpur_pillar', floor='minecraft:gray_concrete',
                    ceil='minecraft:light_gray_concrete', lantern='minecraft:sea_lantern', chain='minecraft:iron_chain', metal='minecraft:iron_block',
                    raw='minecraft:amethyst_block', carpet='minecraft:cyan_carpet', stairs='minecraft:smooth_quartz_stairs', slab='minecraft:smooth_quartz_slab',
                    glow='minecraft:verdant_froglight')


# ===================================================================== the rooms
SHRINES = [(6, 3, 'might', 'minecraft:iron_sword', 'Might', 'strength', '#ff6a5a'), (12, 2, 'swift', 'minecraft:feather', 'Swiftness', 'speed', '#7ae0ff'),
           (18, 3, 'bulwark', 'minecraft:shield', 'the Bulwark', 'resistance', '#ffd36a')]


def sanctum():
    b = R6.shell()
    for x in range(1, W - 1):
        for z in range(1, D - 1):
            b.set(x, FY, z, 'minecraft:calcite' if (x + z) % 3 else 'minecraft:smooth_quartz')
    for x in range(9, 16):                                   # the healing spring
        for z in range(9, 16):
            edge = x in (9, 15) or z in (9, 15)
            b.set(x, FY, z, 'minecraft:quartz_bricks' if edge else 'minecraft:water')
            if edge: b.set(x, 4, z, 'minecraft:quartz_slab[type=bottom]')
            else: b.set(x, 2, z, 'minecraft:sea_lantern')
    b.set(12, FY, 12, 'minecraft:quartz_pillar[axis=y]'); b.set(12, 4, 12, 'minecraft:quartz_pillar[axis=y]'); b.set(12, 5, 12, 'minecraft:amethyst_cluster[facing=up]')
    for (x, z, *_r) in SHRINES:                              # three shrines along the north wall
        b.set(x, 4, z, 'minecraft:chiseled_quartz_block'); b.set(x, 5, z, 'minecraft:quartz_slab[type=bottom]')
        for dx in (-1, 1): b.set(x + dx, 4, z, 'minecraft:flowering_azalea')
    rnd = random.Random(5)
    for x in range(2, 23):
        for z in range(2, 23):
            if 8 <= x <= 16 and 8 <= z <= 16: continue
            if 10 <= z <= 14: continue
            r = rnd.random()
            if r < 0.08: b.set(x, 4, z, 'minecraft:moss_carpet')
            elif r < 0.12: b.set(x, 4, z, 'minecraft:pink_petals[facing=north,flower_amount=4]')
    for x in range(3, 22, 6):
        for z in (4, 20): b.set(x, 13, z, 'minecraft:end_rod[facing=down]')
    R6.ctrl(b, 'sanctum'); return wall_glow(b)


HUNT_PILLARS = [(5, 5), (5, 19), (12, 5), (12, 19), (19, 5), (19, 19), (8, 12), (16, 12)]
HUNT_LEVERS = [(5, 5, 4, 'north'), (19, 5, 20, 'south'), (16, 5, 11, 'north')]          # (x, y, z, facing) - on a pillar's face
HUNT_START = [(21, 4, 21), (21, 4, 3), (3, 4, 21)]


def hunted():
    b = R6.shell()
    rnd = random.Random(23)
    for x in range(1, W - 1):
        for z in range(1, D - 1):
            r = rnd.random()
            b.set(x, FY, z, 'minecraft:pale_moss_block' if r < 0.35 else ('minecraft:cobbled_deepslate' if r < 0.7 else 'minecraft:deepslate_tiles'))
    for (x, z) in HUNT_PILLARS:                              # pillars to hide behind
        for dx in (0, 1):
            for dz in (0, 1):
                for y in range(4, 10): b.set(x + dx - (1 if x > 12 else 0), y, z + dz - (1 if z > 12 else 0), 'minecraft:deepslate_bricks')
    for (x0, z0, x1, z1) in ((3, 8, 9, 8), (15, 16, 21, 16), (9, 15, 9, 21), (15, 3, 15, 9)):    # broken hedge walls
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                if rnd.random() < 0.8:
                    for y in (4, 5, 6): b.set(x, y, z, 'minecraft:pale_oak_leaves[distance=7,persistent=true,waterlogged=false]')
    for (x, y, z, face) in HUNT_LEVERS:
        b.set(x, y, z, f'minecraft:lever[face=wall,facing={face},powered=false]')
    for _ in range(26):
        x, z = rnd.randint(2, 22), rnd.randint(2, 22)
        if 10 <= z <= 14 and (x < 3 or x > 21): continue
        if b.b.get((x, 4, z)) is None: b.set(x, rnd.choice((4, 9, 10)), z, 'minecraft:cobweb')
    for x in range(1, W - 1):                                # no light but a few dead lanterns
        for z in (0, D - 1):
            b.set(x, 9, z, 'minecraft:deepslate_tiles')
    for (x, z) in ((4, 12), (20, 12)): b.set(x, 13, z, 'minecraft:soul_lantern[hanging=true]')
    R6.ctrl(b, 'hunted')
    for pos, st in list(b.b.items()):                        # (the base glow and lanterns go dark)
        if st in (BASE['glow'], BASE['lantern'] + '[hanging=true]', BASE['lantern']): b.b[pos] = 'minecraft:deepslate_tiles' if st == BASE['glow'] else 'minecraft:air'
    return b


def forge():
    b = R6.shell()
    for x in range(1, W - 1):
        for z in range(1, D - 1):
            b.set(x, FY, z, 'minecraft:magma_block' if (x * 3 + z * 7) % 13 == 0 and not 10 <= z <= 14 else ('minecraft:netherrack' if (x + z) % 4 else 'minecraft:blackstone'))
    for y in range(4, 15):                                   # nether-brick walls with lava behind iron grilles
        for x in range(1, W - 1):
            for z in (0, D - 1): b.set(x, y, z, 'minecraft:nether_bricks' if y != 9 else 'minecraft:red_nether_bricks')
        for z in range(1, D - 1):
            for x in (0, W - 1):
                if not (x == W - 1 and 11 <= z <= 13 and y <= 7) and not (x == 0 and 11 <= z <= 13 and y <= 7):
                    b.set(x, y, z, 'minecraft:nether_bricks' if y != 9 else 'minecraft:red_nether_bricks')
    for x in (5, 10, 15, 20):
        for z in (0, D - 1):
            b.set(x, 5, z, 'minecraft:iron_bars'); b.set(x, 6, z, 'minecraft:iron_bars')
    for (x, z) in ((5, 5), (19, 5), (5, 19), (19, 19)):     # basalt columns with soul braziers
        for y in range(4, 8): b.set(x, y, z, 'minecraft:polished_basalt[axis=y]')
        b.set(x, 8, z, 'minecraft:soul_campfire[lit=true,signal_fire=false,waterlogged=false,facing=north]')
    for x in range(10, 15):                                  # the great forge
        for z in range(18, 21): b.set(x, 4, z, 'minecraft:polished_blackstone_bricks')
    b.set(12, 5, 19, 'minecraft:anvil[facing=east]'); b.set(10, 5, 19, 'minecraft:blast_furnace[facing=north,lit=true]'); b.set(14, 5, 19, 'minecraft:blast_furnace[facing=north,lit=true]')
    for x in range(3, 22, 6):
        for z in range(3, 22, 6): b.set(x, 14, z, 'minecraft:shroomlight')
    R6.ctrl(b, 'forge'); return b


VOID_ISLES = [(3, 12, 2), (7, 9, 2), (7, 15, 1), (11, 6, 2), (11, 18, 2), (12, 12, 2), (16, 8, 1), (16, 16, 2), (20, 12, 2)]   # (x, z, radius)
VOID_EYES = [(11, 6), (11, 18), (20, 12)]


def voidg():
    b = R6.shell()
    for x in range(2, W - 2):                                # the drop: everything between the door ledges
        for z in range(1, D - 1):
            for y in (FY, 2): b.set(x, y, z, 'minecraft:air')
            b.set(x, 1, z, 'minecraft:water'); b.set(x, 0, z, 'minecraft:black_concrete')
    for z in range(1, D - 1):
        for x in (1, W - 2): b.set(x, FY, z, 'minecraft:end_stone_bricks')
    for z in range(1, D - 1, 3): b.set(2, 2, z, 'minecraft:ladder[facing=east,waterlogged=false]'); b.set(2, 1, z, 'minecraft:ladder[facing=east,waterlogged=false]')
    for z in range(1, D - 1, 3): b.set(1, 2, z, 'minecraft:end_stone_bricks'); b.set(1, 1, z, 'minecraft:end_stone_bricks')
    for (cx, cz, r) in VOID_ISLES:
        for x in range(cx - r, cx + r + 1):
            for z in range(cz - r, cz + r + 1):
                if (x - cx) ** 2 + (z - cz) ** 2 <= r * r + 1 and 2 <= x <= W - 3 and 1 <= z <= D - 2:
                    b.set(x, FY, z, 'minecraft:end_stone'); b.set(x, 2, z, 'minecraft:end_stone')
    for (cx, cz) in VOID_EYES:
        b.set(cx, 4, cz, 'minecraft:end_portal_frame[eye=false,facing=north]')
    for (cx, cz) in ((7, 9), (16, 16), (7, 15)):
        b.set(cx, 4, cz, 'minecraft:chorus_plant[down=true,up=true,north=false,south=false,east=false,west=false]'); b.set(cx, 5, cz, 'minecraft:chorus_flower[age=5]')
    for y in range(4, 15):                                   # end-stone and purpur walls
        for x in range(1, W - 1):
            for z in (0, D - 1): b.set(x, y, z, 'minecraft:end_stone_bricks' if y % 5 else 'minecraft:purpur_block')
    for (x, z) in ((6, 1), (18, 1), (6, 23), (18, 23)): b.set(x, 12, z, 'minecraft:end_rod[facing=down]')
    R6.ctrl(b, 'voidg'); return b


SEALS = [(5, 'minecraft:white_wool', '#ffffff'), (10, 'minecraft:packed_ice', '#a0d8ff'), (15, 'minecraft:prismarine_bricks', '#5ad8b0'), (20, 'minecraft:amethyst_block', '#c080ff')]


def hollow():
    b = R6.shell()
    rnd = random.Random(31)
    for x in range(1, W - 1):
        for z in range(1, D - 1):
            r = rnd.random()
            b.set(x, FY, z, 'minecraft:soul_soil' if r < 0.25 else ('minecraft:polished_deepslate' if r < 0.6 else 'minecraft:deepslate_tiles'))
    for y in range(4, 15):                                   # the black citadel's stone, a red band
        for x in range(1, W - 1):
            for z in (0, D - 1):
                b.set(x, y, z, 'minecraft:red_nether_bricks' if y == 9 else ('minecraft:cracked_deepslate_bricks' if rnd.random() < 0.15 else 'minecraft:deepslate_bricks'))
    for (x, blk, _c) in SEALS:                               # four seals on the north wall, a button under each
        for dx in (-1, 0, 1):
            for dy in (0, 1, 2): b.set(x + dx, 6 + dy, 0, blk)
        b.set(x, 7, 0, 'minecraft:crying_obsidian')
        b.set(x, 5, 1, 'minecraft:polished_blackstone_button[face=wall,facing=south,powered=false]')
    for (x, z) in ((4, 18), (20, 18)):                       # soul fire pits
        b.set(x, 4, z, 'minecraft:soul_campfire[lit=true,signal_fire=false,waterlogged=false,facing=north]')
    for y in range(4, 10): b.set(12, y, 18, 'minecraft:stripped_dark_oak_log[axis=y]')     # a dead tree
    for (dx, dy, dz) in ((1, 8, 0), (-1, 7, 0), (0, 9, 1), (2, 9, 0), (-2, 8, 0)):
        b.set(12 + dx, dy, 18 + dz, 'minecraft:stripped_dark_oak_log[axis=x]')
    for x in range(3, 22, 9):
        b.set(x, 14, 12, 'minecraft:iron_chain[axis=y]'); b.set(x, 13, 12, 'minecraft:soul_lantern[hanging=true]')
    R6.ctrl(b, 'hollow'); return b


BUILDERS = {'sanctum': sanctum, 'hunted': hunted, 'forge': forge, 'voidg': voidg, 'hollow': hollow}
POOLS = {'sanctum': (1, 2, 3, 4, 5), 'hunted': (1, 2, 3, 4, 5), 'forge': (2, 3, 4, 5), 'voidg': (3, 4, 5), 'hollow': (3, 4, 5)}
for _k, _f in BUILDERS.items():
    P75.EXTRA_ROOMS[_k] = _f
    R6.NAMES[_k] = NAMES[_k]
    for _t in POOLS[_k]: P75.EVENT_POOL[_t].append(_k)


def extend_offers(O, offer):
    pass


def generate(G):
    fn, wjson, tellraw, title = G.fn, G.wjson, G.tellraw, G.title
    import phase70 as P70
    rel = RM.rel
    ident = [F(0), F(0), F(0), F(1)]
    P = [T('[', 'dark_gray'), T('Heist', GOLD, bold=True), T('] ', 'dark_gray')]
    inst = lambda f: f'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run function {f}'
    crew = '@a[tag=bm.gvp,distance=..16]'
    SL = P70.SLOTS
    def label(x, y, z, text, scale=0.6, tags=('bm.gvprop',)):
        return f'summon minecraft:text_display {rel(x, y, z)} ' + snbt({'Tags': list(tags), 'billboard': 'vertical', 'brightness': {'block': 15, 'sky': 15},
                                                                       'background': Int(0x90000000 - 2 ** 32), 'text': text, 'line_width': Int(220),
                                                                       'transformation': {'left_rotation': ident, 'right_rotation': ident,
                                                                                          'translation': [F(0)] * 3, 'scale': [F(scale)] * 3}})
    def sign(x, y, z, t_, body, col=GOLD):
        return label(x, y, z, [T(t_ + '\n', col, bold=True), T(body, 'gray')])
    def big(t_, sub, col=GOLD, who=crew):
        return [f'title {who} times 5 40 10', title(who, 'title', T(t_, col, bold=True)), title(who, 'subtitle', T(sub, 'gray'))]
    def pot(n):
        return [f'scoreboard players set #c bm.rng {n}', inst('bm:p75/pot_add')]
    objs = ['bm.gvdb', 'bm.gvsf', 'bm.gvbn', 'bm.gvv']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs

    # ================================================================== THE FEE BY TIER
    fee = G.FUNCS['p75/fee']
    tok = '*[minecraft:custom_data~{bm:"token"}]'
    fn('p75/fee', ['scoreboard players set #fee bm.rng 3'] + [f'execute if score #feet bm.rng matches {t} run scoreboard players set #fee bm.rng {n}' for t, n in FEE_T.items()] +
       [f'execute store result score #tk bm.rng run clear @s {tok} 0', 'execute if score #tk bm.rng < #fee bm.rng run return run function bm:p75/fee_no',
        'execute store result storage bm:gv fee.n int 1 run scoreboard players get #fee bm.rng', 'function bm:p90/fee_take with storage bm:gv fee',
        'scoreboard players operation #lpool bm.gvlp += #fee bm.rng',
        tellraw('@s', P + [T('You pay the Fixer\'s fee (', 'gray'), {'score': {'name': '#fee', 'objective': 'bm.rng'}, 'color': 'white'}, T(' Tokens). ', 'gray'),
                           T('Lucky pool: ', '#7dff6a'), {'score': {'name': '#lpool', 'objective': 'bm.gvlp'}, 'color': '#7dff6a', 'bold': True}]), 'return 1'])
    fn('p90/fee_take', [f'execute store result score #tk bm.rng run clear @s {tok} 0', f'$execute if score #tk bm.rng matches $(n).. run clear @s {tok} $(n)'])
    fn('p75/fee_no', [tellraw('@s', P + [T('The Fixer\'s fee for this tier is ', 'red'), {'score': {'name': '#fee', 'objective': 'bm.rng'}, 'color': 'white', 'bold': True},
                                         T(' Black Market Tokens', 'red'), T(' - you don\'t have them, so you stay behind.', 'gray')]),
                      'playsound minecraft:entity.villager.no player @s ~ ~ ~ 1 1', 'return 0'])
    # (who pays what: the one claiming, the tier they picked; a recruit or a latecomer, the slot's tier)
    pl = G.FUNCS['p75/pick_lives']
    k = pl.index('execute unless function bm:p75/fee run return 0')
    pl.insert(k, 'scoreboard players operation #feet bm.rng = #t bm.rng')
    for s in range(SL):
        G.FUNCS[f'p70/s{s}/recruit'].insert(0, f'scoreboard players operation #feet bm.rng = #t{s} bm.gvt')
    jf = G.FUNCS['p75/join_fee']
    jf.insert(len(jf) - 1, 'function bm:p90/join_tier')
    fn('p90/join_tier', [f'execute if score #j bm.rng matches {s + 1} run scoreboard players operation #feet bm.rng = #t{s} bm.gvt' for s in range(SL)])
    # the menu's line about the fee
    G.FUNCS['p75/lives_show'] = [l.replace("The Fixer's fee: 3 Tokens each", "The Fixer's fee: 2 Tokens (Tier I) to 6 (Tier V) each") for l in G.FUNCS['p75/lives_show']]
    import phase28 as P28

    # ================================================================== EVENT ROOMS: bits of their own (the room kinds keep #pool)
    EVENTS = [k for k in P75.EXTRA_ROOMS if k not in P75.KINDS]
    assert len(EVENTS) <= 31, EVENTS
    for f_ in list(G.FUNCS):
        L = G.FUNCS[f_]
        if any(l == 'scoreboard players set #pool bm.rng 0' or l.endswith(' run scoreboard players set #pool bm.rng 0') for l in L):
            L[:] = sum(([l, l.replace('#pool', '#epool')] if l.endswith('scoreboard players set #pool bm.rng 0') else [l] for l in L), [])
    fn('p90/lay/ebit', ['scoreboard players set #bit bm.rng 1', 'scoreboard players operation #k bm.rng = #r bm.rng', 'function bm:p75/lay/bit2',
                        'scoreboard players operation #q2 bm.rng = #epool bm.rng', 'scoreboard players operation #q2 bm.rng /= #bit bm.rng',
                        'scoreboard players operation #q2 bm.rng %= #2 bm.rng'])
    import phase85 as P85
    for t in range(1, 6):
        evs = P75.EVENT_POOL[t]
        L = [f'execute store result score #i bm.rng run random value 0..{len(evs) - 1}'] + \
            [f'execute if score #i bm.rng matches {i} run scoreboard players set #r bm.rng {EVENTS.index(k)}' for i, k in enumerate(evs)] + \
            ([f'execute if score #q bm.rng matches ..1 if score #r bm.rng matches {EVENTS.index("rest")} run return run function bm:p75/lay/event{t}']
             if 'rest' in evs else []) + \
            [f'execute if score #r bm.rng matches {EVENTS.index(k)} if function bm:p90/lay/rested run return run function bm:p75/lay/event{t}' for k in RESTS if k in evs] + \
            [f'execute if score #r bm.rng matches {EVENTS.index(k)} if score #gpl bm.rng matches ..1 run return run function bm:p85/lay/solo' for k in P85.COMPETITIVE if k in evs] + \
            [f'execute if score #r bm.rng matches {EVENTS.index(k)} if predicate bm:p90/rare_{k} run return run function bm:p75/lay/event{t}' for k in RARE if k in evs] + \
            ['function bm:p90/lay/ebit', f'execute if score #q2 bm.rng matches 1 run return run function bm:p75/lay/event{t}', 'scoreboard players operation #epool bm.rng += #bit bm.rng'] + \
            [f'execute if score #i bm.rng matches {i} run function bm:p75/pc/{k}' for i, k in enumerate(evs)]
        G.FUNCS[f'p75/lay/event{t}'] = L         # (2.67: the Rats' Rest is never the first room - nothing to rest from yet)
    # (2.67) one rest room a heist at most - the Rats' Rest or the Sanctuary, never both, never two; the Endless Vault rests at
    #  its own cash-out Rests (every fifth room) and draws neither
    fn('p90/lay/rested', ['execute if score #endl bm.rng matches 1 run return 1'] +
       sum(([f'scoreboard players operation #q2 bm.rng = #epool bm.rng', f'scoreboard players set #bit bm.rng {2 ** EVENTS.index(k)}',
             'scoreboard players operation #q2 bm.rng /= #bit bm.rng', 'scoreboard players operation #q2 bm.rng %= #2 bm.rng',
             'execute if score #q2 bm.rng matches 1 run return 1'] for k in RESTS), []) + ['return 0'])
    G.FUNCS['p75/lay/rooms'].insert(0, 'scoreboard players set #endl bm.rng 0')
    for f_ in [f for f in G.FUNCS if f.startswith('p77/endless/') and (f.endswith('/extend') or '/lay' in f)]:
        G.FUNCS[f_].insert(0, 'scoreboard players set #endl bm.rng 1'); G.FUNCS[f_].append('scoreboard players set #endl bm.rng 0')
    for k, pct in RARE.items():
        wjson(f'bm/predicate/p90/rare_{k}.json', {'condition': 'minecraft:random_chance', 'chance': round(1 - pct / 100, 3)})
    # (more of them now: 30% a room, at most 2 - 3 from Tier III - and two more in a double heist)
    lr = G.FUNCS['p75/lay/room']
    G.FUNCS['p75/lay/room'] = [l.replace('matches 1..22 if function bm:p75/lay/can_event', 'matches 1..30 if function bm:p75/lay/can_event') for l in lr]
    lr = G.FUNCS['p75/lay/room']
    lr.insert(next(i for i, l in enumerate(lr) if 'random value 1..100' in l), 'execute if score #frm bm.gvv matches 1.. run return run function bm:p75/lay/event')
    fn('p75/lay/can_event', ['scoreboard players set #emax bm.rng 2', 'execute if score #gt bm.rng matches 3.. run scoreboard players set #emax bm.rng 3',
                             'execute if score #gdb bm.rng matches 1 run scoreboard players add #emax bm.rng 2',
                             'execute if score #nev bm.rng < #emax bm.rng run return 1', 'return 0'])

    # ================================================================== DOUBLE HEISTS, ALIEN HEISTS: rolled when the heist is claimed
    for s in range(SL):
        z0 = P75.zoff(s)
        cl = G.FUNCS[f'p70/s{s}/claim']
        k = next(i for i, l in enumerate(cl) if 'forceload add' in l)
        cl[k:k] = [f'scoreboard players set #db{s} bm.gvv 0', f'scoreboard players set #sf{s} bm.gvv 0',
                   'execute store result score #r bm.rng run random value 1..1000',
                   f'execute if score #r bm.rng matches ..{1000 // DOUBLE_IN} run scoreboard players set #db{s} bm.gvv 1',
                   'execute store result score #r bm.rng run random value 1..1000',
                   f'execute if score #r bm.rng matches ..{1000 // SCIFI_IN} run scoreboard players set #sf{s} bm.gvv 1',
                   f'execute if score #md{s} bm.gvmd matches 2 run scoreboard players set #db{s} bm.gvv 0',         # (not in the Endless Vault)
                   f'execute if score #fdb bm.gvv matches 1 run scoreboard players set #db{s} bm.gvv 1',            # (the admin's forcing: 1 always, -1 never)
                   f'execute if score #fsf bm.gvv matches 1 run scoreboard players set #sf{s} bm.gvv 1',
                   f'execute if score #fdb bm.gvv matches -1 run scoreboard players set #db{s} bm.gvv 0', f'execute if score #fsf bm.gvv matches -1 run scoreboard players set #sf{s} bm.gvv 0']
        cl.insert(k + len(cl[k:k]) + 10, f'execute if score #db{s} bm.gvv matches 1 in bm:gutter run forceload add {P75.FL_X[1] + 1} {z0 - 32} {P75.FL_X[1] + 360} {z0 + 48}')
        b = G.FUNCS[f'p70/s{s}/build']
        kk = b.index('scoreboard players operation #gk bm.rng = #gt bm.rng')
        b[kk:kk] = [f'scoreboard players operation #gdb bm.rng = #db{s} bm.gvv', f'scoreboard players operation #gsf bm.rng = #sf{s} bm.gvv',
                    'execute if score #gsf bm.rng matches 1 if score #gn bm.rng matches 0 run scoreboard players set #gn bm.rng 3',
                    'execute if score #gsf bm.rng matches 1 unless score #gn bm.rng matches 3 run scoreboard players set #gsf bm.rng 0']
        kk = b.index('scoreboard players add #gk bm.rng 2')
        b.insert(kk + 1, 'execute if score #gdb bm.rng matches 1 run scoreboard players operation #gk bm.rng *= #2 bm.rng')
        for f_ in (f'p70/s{s}/enter', f'p70/s{s}/join'):
            G.FUNCS[f_].append(f'function bm:p90/announce{s}')
        fn(f'p90/announce{s}', [f'execute if score #db{s} bm.gvv matches 1 run function bm:p90/say_double', f'execute if score #sf{s} bm.gvv matches 1 run function bm:p90/say_alien'])
    fn('p90/say_double', ['title @s times 10 60 20', title('@s', 'title', T('DOUBLE HEIST', GOLD, bold=True)), title('@s', 'subtitle', T('twice the rooms - twice the take', 'gray')),
                          tellraw('@s', P + [T('DOUBLE HEIST! ', GOLD, bold=True), T('Twice as many rooms tonight. Win it and everyone gets two extra shares, ', 'gray'),
                                             T('and better odds at the Fixer\'s prize.', 'gray')])])
    fn('p90/say_alien', ['title @s times 10 60 20', title('@s', 'title', T('ALIEN HEIST', '#7dffd0', bold=True)), title('@s', 'subtitle', T('the Vorn got here first', 'gray')),
                         tellraw('@s', P + [T('ALIEN HEIST! ', '#7dffd0', bold=True), T('The Vorn have taken the vault - their steel on every wall, their troopers on guard. ', 'gray'),
                                            T('Their loot is yours if you win.', 'gray')]),
                         'playsound minecraft:block.beacon.activate ambient @s ~ ~ ~ 1 0.6'])
    ii = G.FUNCS['p70/inst_init']
    ii[-1:-1] = ['scoreboard players operation @s bm.gvdb = #gdb bm.rng', 'scoreboard players operation @s bm.gvsf = #gsf bm.rng']
    G.FUNCS['p70/ctx1'] += ['scoreboard players operation #gdb bm.rng = @s bm.gvdb', 'scoreboard players operation #gsf bm.rng = @s bm.gvsf']
    # the double heist's extra: two shares each, and better odds at the prize (never above its caps)
    pay = G.FUNCS['p70/payout_inst']
    k = next(i for i, l in enumerate(pay) if l == 'scoreboard players operation #plu bm.rng = @s bm.gvlu')
    pay[k:k] = ['execute if score @s bm.gvdb matches 1 run scoreboard players add #sh bm.rng 2', 'execute if score @s bm.gvdb matches 1 run scoreboard players add #pb bm.rng 10']
    # the alien look: every template once more in the Vorn's steel, placed when #gsf says so
    rooms = {'lobby': R5.lobby2, 'dial': R5.dial2}
    for k_ in ('levers', 'plates', 'lasers', 'tiles', 'guards', 'coffers', 'cache'):
        rooms[k_] = R5.glowing(RM.BUILDERS[k_])
    rooms['vault'] = lambda: wall_glow(RM.vault(), RM.VAULT_LEN)
    rooms.update(P75.EXTRA_ROOMS)
    keys = set()
    for k_, f in rooms.items():
        R5.retheme(f(), 6, R5.VAULT_DOOR if k_ == 'vault' else ()).export(G.path('data', 'bm', 'structure', f'gv_{k_}_t6.nbt')); keys.add(k_)
    for k_, (f, *_r) in R5.CONN.items():
        R5.retheme(f(), 6).export(G.path('data', 'bm', 'structure', f'gv_cn_{k_}_t6.nbt')); keys.add(f'cn_{k_}')
    for k_ in keys:
        L = G.FUNCS[f'p75/pc/{k_}']
        L[:] = [l.replace('execute if score #gt bm.rng matches', 'execute if score #gsf bm.rng matches 0 if score #gt bm.rng matches') if ' run place template ' in l else l for l in L]
        L.insert(0, f'execute if score #gsf bm.rng matches 1 run place template bm:gv_{k_}_t6 ~ ~ ~')
    ex = G.FUNCS.get('p77/endless/s0/extend')
    for s in range(SL):
        e = G.FUNCS.get(f'p77/endless/s{s}/extend')
        if e: e.insert(0, f'scoreboard players operation #gsf bm.rng = #sf{s} bm.gvv')
    fn('admin/heist_double', ['scoreboard players set #fdb bm.gvv 1', tellraw('@s', P + [T('Every heist claimed from now on is a Double Heist (admin/heist_variants_off to stop).', 'gray')])])
    fn('admin/heist_alien', ['scoreboard players set #fsf bm.gvv 1', tellraw('@s', P + [T('Every heist claimed from now on is an Alien Heist (admin/heist_variants_off to stop).', 'gray')])])
    fn('admin/heist_variants_never', ['scoreboard players set #fdb bm.gvv -1', 'scoreboard players set #fsf bm.gvv -1', tellraw('@s', P + [T('No Double or Alien Heists until admin/heist_variants_off.', 'gray')])])
    fn('admin/heist_variants_off', ['scoreboard players set #fdb bm.gvv 0', 'scoreboard players set #fsf bm.gvv 0', tellraw('@s', P + [T('Heist variants back to chance.', 'gray')])])

    # ================================================================== THE ALARM: a choice now (off unless you turn it on, on the tries page)
    # off: nothing rings - no patrols, no lockdown (Greedy Vault and Silent Alarm aren't rolled either);
    # on: one more share for the trouble, and the old one for keeping it under 50
    objs = ['bm.gval']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    MENU = P28.MENU['heist']
    LUCKY = '#7dff6a'
    lbtn = lambda c, n, col, txt: P28.btn([T(f'{n} TRIES  ', col, bold=True), T(txt, 'white')], 7610 + c, width=300,
                                          tooltip=T(f'Your crew can be knocked out {n} times (one more per crewmate past the first).', 'gray'))
    abtn = P28.btn([T('ALARM: ', '#ff5a5a', bold=True), T('$(al)', 'white', bold=True), T('  (click to switch)', 'gray')], 7619, width=300,
                   tooltip=T('Off: no alarm, no patrols, no lockdown. On: mistakes ring it - at 50 guards patrol, at 100 the vault locks down - '
                             'and you get one more share (two if you keep it under 50).', 'gray'))
    dlg = P28.multi([T('How many tries?', GOLD, bold=True)],
                    [P28.body([T('Every knock-out costs the crew a try. Run out and the heist fails: back to the den, everything gathered lost '
                                 '- then the leader picks: home, or a new raid.', 'gray')]),
                     P28.body([T('Fewer tries, bigger haul - the higher the tier, the bigger. ', GOLD), T('No knock-outs at all: a share more (two from Tier III).', 'gray')]),
                     P28.body([T('The alarm is up to you: ', '#ff7a7a'), T('$(al_txt)', 'gray')]),
                     P28.body([T("The Fixer's fee: 2 Tokens (Tier I) to 6 (Tier V) - everyone pays their own; win and it comes back, maybe with a few more (1 at Tier I, up to 5 at Tier V). "
                                 'Every fee goes into the Lucky Pool (now ', 'dark_gray'), T('$(p)', LUCKY, bold=True),
                               T('). From Tier III, one heist in 150 is a Lucky Raid - harder, and the crew splits the pool.', 'dark_gray')])],
                    [abtn, lbtn(1, 3, '#ff5a5a', '+1 to +4 shares (by tier) - for the bold'), lbtn(2, 5, GOLD, '+0 to +2 shares (by tier)'),
                     lbtn(3, 7, LUCKY, 'no bonus - for a first try')],
                    columns=1, exit_label='Back')
    G.FUNCS['p75/lives_menu'] = ['execute store result storage bm:gv m.p int 1 run scoreboard players get #lpool bm.gvlp',
                                 'data modify storage bm:gv m.al set value "OFF"', 'data modify storage bm:gv m.al_txt set value "off - a quiet job, no patrols, no lockdown."',
                                 'execute if score @s bm.gval matches 1 run data modify storage bm:gv m.al set value "ON"',
                                 'execute if score @s bm.gval matches 1 run data modify storage bm:gv m.al_txt set value "ON - mistakes ring it (patrols at 50, lockdown at 100); one more share, two if you keep it under 50."',
                                 f'scoreboard players set @s bm.menu {MENU}', 'function bm:p75/lives_show with storage bm:gv m']
    G.FUNCS['p75/lives_show'] = [f'$dialog show @s {snbt(dlg)}']
    holds_plans = '*[minecraft:custom_data~{bm:"fixers_ledger"}]'      # (2.75: the Ledger plans heists now - the Heist Plans folded into it)
    G.FUNCS['p28/act'].append('execute if score #act bm.pay matches 7619 run return run function bm:p90/alarm_toggle')
    fn('p90/alarm_toggle', [f'execute unless score @s bm.menu matches {MENU} run return run function bm:p28/stale',
                            f'execute unless items entity @s container.* {holds_plans} unless items entity @s weapon.offhand {holds_plans} run return run function bm:p28/stale',
                            'execute if score @s bm.gval matches 1 run return run function bm:p90/alarm_off', 'scoreboard players set @s bm.gval 1',
                            'playsound minecraft:block.bell.use player @s ~ ~ ~ 0.8 0.8', 'function bm:p75/lives_menu'])
    fn('p90/alarm_off', ['scoreboard players set @s bm.gval 0', 'playsound minecraft:ui.button.click player @s ~ ~ ~ 0.8 1', 'function bm:p75/lives_menu'])
    pl = G.FUNCS['p75/pick_lives']
    pl.insert(pl.index('scoreboard players operation #feet bm.rng = #t bm.rng'), 'scoreboard players set #al bm.rng 0')
    pl.insert(pl.index('scoreboard players operation #feet bm.rng = #t bm.rng'), 'execute if score @s bm.gval matches 1 run scoreboard players set #al bm.rng 1')
    for s in range(SL):
        G.FUNCS[f'p70/s{s}/claim'].insert(0, f'scoreboard players operation #al{s} bm.gvv = #al bm.rng')
        b = G.FUNCS[f'p70/s{s}/build']
        b.insert(0, f'scoreboard players operation #gal bm.rng = #al{s} bm.gvv')
    ii = G.FUNCS['p70/inst_init']
    ii[-1:-1] = ['scoreboard players operation @s bm.gval = #gal bm.rng', 'execute unless score @s bm.gval matches 1 run scoreboard players set @s bm.gva 0']
    G.FUNCS['p70/ctx1'].append('scoreboard players operation #gal bm.rng = @s bm.gval')
    G.FUNCS['p70/alarm'].insert(0, 'execute unless score @s bm.gval matches 1 run return 0')
    rm = G.FUNCS['p70/roll_mod']
    rm.insert(1, 'execute unless score #gal bm.rng matches 1 if score #r bm.rng matches 5..6 run return run function bm:p70/roll_mod')
    G.FUNCS['p70/bar'] += [f'execute unless score @s bm.gval matches 1 if score @s bm.gvi matches {s + 1} run bossbar set bm:gva{s} name ' +
                           snbt([T('Tries ', '#ff7a7a'), {'score': {'name': '@s', 'objective': 'bm.gvlv'}, 'color': 'white', 'bold': True},
                                 T('   Pot ', GOLD), {'score': {'name': '@s', 'objective': 'bm.gvpot'}, 'color': 'white', 'bold': True}, T(' coins', GOLD)]) for s in range(SL)]
    pay = G.FUNCS['p70/payout_inst']
    k = pay.index('execute if score #ga bm.rng matches ..49 run scoreboard players add #sh bm.rng 1')
    pay[k:k + 1] = ['execute if score @s bm.gval matches 1 if score #ga bm.rng matches ..49 run scoreboard players add #sh bm.rng 1',
                    'execute if score @s bm.gval matches 1 run scoreboard players add #sh bm.rng 1']

    # ================================================================== the rooms' dispatch
    ks = list(BUILDERS)
    G.FUNCS['p70/r/init'] += [f'execute if entity @s[tag=bm.gvr_{k}] run return run function bm:p90/{k}/init' for k in ks]
    G.FUNCS['p70/r/tick'] += [f'execute if entity @s[tag=bm.gvr_{k}] run return run function bm:p90/{k}/tick' for k in ks]
    k0 = next(i for i, l in enumerate(G.FUNCS['p70/r/init']) if 'tag @s add bm.gvnopick' in l)
    G.FUNCS['p70/r/init'][k0:k0] = [f'execute if entity @s[tag=bm.gvr_{k}] run tag @s add bm.gvnopick' for k in ks]
    G.FUNCS['p70/solved'] += [f'execute if entity @s[tag=bm.gvr_{k}] as @a[tag=bm.gvp,distance=..300] if score @s bm.gvi = #gi bm.rng run ' +
                              title('@s', 'actionbar', [T(NAMES[k], GOLD, bold=True), T(' - done. The way on is open.', 'gray')]) for k in ks]
    # (losing a try without a knock-out: a timed room run out - phase91 too)
    fn('p90/lose_try', ['scoreboard players remove @s bm.gvlv 1', 'function bm:p70/bar', 'function bm:p70/tag_mine',
                        'execute if score @s bm.gvlv matches 1.. run ' + tellraw('@a[tag=bm.gvme]', P + [T('Out of time - that cost a try! ', 'red', bold=True),
                                                                                                         {'score': {'name': '@s', 'objective': 'bm.gvlv'}, 'color': 'white', 'bold': True},
                                                                                                         T(' tries left.', 'gray')]),
                        'execute if score @s bm.gvlv matches ..0 run function bm:p75/fail', 'tag @a[tag=bm.gvme] remove bm.gvme'])

    # ================================================================== THE SANCTUARY
    def shrine(x, z, key, item, name, eff, col):
        disp = {'Tags': ['bm.gvprop', 'bm.gvshd'], 'Glowing': B(1), 'item': {'id': item, 'count': Int(1)}, 'item_display': 'ground', 'billboard': 'vertical',
                'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0)] * 3, 'scale': [F(0.9)] * 3}}
        return [f'summon minecraft:item_display {rel(x + 0.5, 6.0, z + 0.5)} {snbt(disp)}',
                f'summon minecraft:interaction {rel(x + 0.5, 5, z + 0.5)} ' + snbt({'Tags': ['bm.gvprop', 'bm.gvsh', f'bm.gvsh_{key}'], 'width': F(1.2), 'height': F(1.8), 'response': B(1)}),
                label(x + 0.5, 7.2, z + 0.5, [T(name + '\n', col, bold=True), T({'strength': 'Strength', 'speed': 'Speed', 'resistance': 'Resistance'}[eff] + ', 5 min', 'gray')], 0.5)]
    fn('p90/sanctum/init', ['function bm:p70/ctx'] + sum((shrine(*s_) for s_ in SHRINES), []) +
       [sign(2.5, 7.5, 12, 'THE SANCTUARY', 'Rest. The spring heals. Each of you may take one boon from the shrines.', '#9af0ff')])
    fn('p90/sanctum/tick', ['scoreboard players set @a[tag=bm.gvp,distance=..12] bm.gvmz 8',
                            'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..10] run function bm:p90/sanctum/arrive',
                            'execute as @e[type=minecraft:interaction,tag=bm.gvsh,distance=..12] if data entity @s interaction at @s run function bm:p90/sanctum/take',
                            'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #20 bm.rng',
                            'execute if score #q bm.rng matches 0 run effect give @a[tag=bm.gvp,distance=..11] minecraft:regeneration 3 1 true',
                            f'execute if score #q bm.rng matches 0 run particle minecraft:glow {rel(12, 5, 12)} 2 0.5 2 0 6'])
    fn('p90/sanctum/arrive', ['scoreboard players set @s bm.gvs 1', 'function bm:p70/solved',
                              'execute as @a[tag=bm.gvp,distance=..300] if score @s bm.gvi = #gi bm.rng at @s run function bm:p90/sanctum/heal'] +
       big('THE SANCTUARY', 'The spring heals you. Take a boon from the shrines.', '#9af0ff', '@a[tag=bm.gvp,distance=..14]'))
    fn('p90/sanctum/heal', ['effect give @s minecraft:instant_health 1 4 true', 'effect give @s minecraft:saturation 3 2 true',
                            'effect clear @s minecraft:poison', 'effect clear @s minecraft:wither', 'effect clear @s minecraft:slowness', 'effect clear @s minecraft:weakness',
                            'effect clear @s minecraft:darkness', 'effect clear @s minecraft:blindness',
                            'particle minecraft:heart ~ ~2 ~ 0.3 0.2 0.3 0 5', 'playsound minecraft:block.beacon.power_select player @s ~ ~ ~ 0.8 1.6'])
    fn('p90/sanctum/take', ['tag @s add bm.gvshme', 'execute on target run function bm:p90/sanctum/take2', 'tag @s remove bm.gvshme', 'data remove entity @s interaction'])
    fn('p90/sanctum/take2', ['execute if score @s bm.gvbn = @s bm.gvrun run return run ' + title('@s', 'actionbar', T('You\'ve taken your boon this heist.', 'gray'))] +
       [f'execute if entity @e[type=minecraft:interaction,tag=bm.gvshme,tag=bm.gvsh_{key},limit=1] run function bm:p90/sanctum/boon_{key}' for (_x, _z, key, *_r) in SHRINES])
    for (_x, _z, key, item, name, eff, col) in SHRINES:
        fn(f'p90/sanctum/boon_{key}', ['scoreboard players operation @s bm.gvbn = @s bm.gvrun', f'effect give @s minecraft:{eff} 300 0',
                                       'playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 1.2', 'particle minecraft:end_rod ~ ~1 ~ 0.3 0.6 0.3 0.05 20',
                                       tellraw('@s', P + [T('The shrine grants you ', 'gray'), T(name, col, bold=True), T(f' ({eff.title()}, five minutes).', 'gray')])])

    # ================================================================== THE STALKER'S WARD
    stalker = {'Tags': ['bm.gvprop', 'bm.gvstalk'], 'PersistenceRequired': B(1), 'Invulnerable': B(1), 'CustomName': T('Something', '#8a8a8a'),
               'attributes': [{'id': 'minecraft:attack_damage', 'base': Dd(4.0)}, {'id': 'minecraft:follow_range', 'base': Dd(32.0)}]}
    fn('p90/hunted/init', ['function bm:p70/ctx', 'scoreboard players operation @s bm.gvt = #gt bm.rng',
                           sign(2.5, 7.5, 12, "THE STALKER'S WARD", "Pull the three levers. Don't stop looking behind you.", '#9a9aa8')])
    fn('p90/hunted/tick', ['execute if score @s bm.gvs matches 3 run return 0',
                           'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..10] run function bm:p90/hunted/start',
                           'execute unless score @s bm.gvs matches 1 run return 0',
                           'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #20 bm.rng',
                           'execute if score #q bm.rng matches 0 run effect give @a[tag=bm.gvp,distance=..15] minecraft:darkness 3 0 true',
                           'execute if score #q bm.rng matches 0 as @e[type=minecraft:creaking,tag=bm.gvstalk,distance=..20] at @s as @a[tag=bm.gvp,distance=..7] at @s run playsound minecraft:entity.warden.heartbeat hostile @s ~ ~ ~ 1 0.8',
                           # (it never leaves the ward)
                           'execute if score #q bm.rng matches 0 as @e[type=minecraft:creaking,tag=bm.gvstalk,distance=..40] unless entity @s[distance=..15] run tp @s ~8 ~ ~8',
                           'scoreboard players set #lv bm.rng 0'] +
       [f'execute if block {rel(x, y, z)} minecraft:lever[powered=true] run scoreboard players add #lv bm.rng 1' for (x, y, z, _f) in HUNT_LEVERS] +
       ['execute unless score #lv bm.rng = @s bm.gvw run function bm:p90/hunted/pulled', 'execute if score #lv bm.rng matches 3 run function bm:p90/hunted/done'])
    fn('p90/hunted/start', ['scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvtm 0', 'scoreboard players set @s bm.gvw 0',
                            'scoreboard players set #n bm.rng 1', 'execute if score #gt bm.rng matches 2.. run scoreboard players set #n bm.rng 2',
                            'execute if score #gt bm.rng matches 4.. run scoreboard players set #n bm.rng 3'] +
       [f'execute if score #n bm.rng matches {i + 1}.. run summon minecraft:creaking {rel(x + 0.5, y, z + 0.5)} {snbt(stalker)}' for i, (x, y, z) in enumerate(HUNT_START)] +
       ['execute as @e[type=minecraft:creaking,tag=bm.gvstalk,distance=..20] run scoreboard players operation @s bm.gvi = #gi bm.rng',
        'execute as @e[type=minecraft:creaking,tag=bm.gvstalk,distance=..20] store result entity @s attributes[{id:"minecraft:attack_damage"}].base double 1 run scoreboard players operation #q bm.rng = #gt bm.rng',
        'execute as @e[type=minecraft:creaking,tag=bm.gvstalk,distance=..20] run attribute @s minecraft:attack_damage base set 5'] +
       big('THE STALKER\'S WARD', 'Something is in here with you.', '#9a9aa8', '@a[tag=bm.gvp,distance=..15]') +
       ['playsound minecraft:entity.creaking.activate hostile @a[distance=..20] ~ ~ ~ 1 0.7', 'playsound minecraft:ambient.cave hostile @a[distance=..20] ~ ~ ~ 1 0.6'])
    fn('p90/hunted/pulled', ['scoreboard players operation @s bm.gvw = #lv bm.rng', 'execute if score #lv bm.rng matches 1..2 run ' +
                             title('@a[tag=bm.gvp,distance=..15]', 'actionbar', [T('A lever clanks. ', '#9a9aa8'), {'score': {'name': '#lv', 'objective': 'bm.rng'}, 'color': 'white'},
                                                                                 T(' of 3.', 'gray')]),
                             'playsound minecraft:block.iron_trapdoor.close block @a[distance=..20] ~ ~ ~ 1 0.5'])
    fn('p90/hunted/done', ['execute as @e[type=minecraft:creaking,tag=bm.gvstalk,distance=..30] at @s run particle minecraft:block{block_state:"minecraft:pale_oak_log"} ~ ~1.5 ~ 0.4 1 0.4 0 40',
                           'kill @e[type=minecraft:creaking,tag=bm.gvstalk,distance=..30]', 'effect clear @a[tag=bm.gvp,distance=..16] minecraft:darkness',
                           'playsound minecraft:entity.creaking.death hostile @a[distance=..20] ~ ~ ~ 1 0.8'] + pot(6) +
       big('THE WARD FALLS SILENT', 'Whatever it was crumbles to splinters.', '#9a9aa8', '@a[tag=bm.gvp,distance=..16]') + ['function bm:p70/solved'])

    # ================================================================== THE BLAZE FORGE
    mk = P75._mob
    WV = {'Tags': ['bm.gvg', 'bm.gvnew2', 'bm.tiered', 'bm.seen', 'bm.gvwv']}
    cube = lambda sz, nm: mk('magma_cube', nm, '#ff8a3a', {}, dict(WV, Size=Int(sz)))
    waves = {1: [cube(1, 'Forge Ember')] * 3, 2: [cube(2, 'Forge Ember')] * 2 + [mk('blaze', 'Forge Blaze', '#ffb040', {}, WV)],
             3: [cube(3, 'The Forge Keeper')]}
    keeper = mk('blaze', 'The Forge Keeper', '#ff5a20', {}, dict(WV, CustomNameVisible=B(1), Tags=WV['Tags'] + ['bm.gvcap']), {'scale': 1.7, 'max_health': 60.0, 'attack_damage': 8.0})
    def spawn(ty, nbt, x, z):
        return [f'execute positioned {rel(x, 5, z)} run summon minecraft:{ty} ~ ~ ~ {snbt(nbt)}', f'execute positioned {rel(x, 5, z)} run function bm:p70/guard_set']
    SPOTS = [(6, 6), (18, 6), (6, 18), (18, 18), (12, 8), (12, 16)]
    w1 = sum((spawn(*cube(2, 'Forge Ember'), x, z) for (x, z) in SPOTS[:4]), [])
    w2 = sum((spawn(*cube(2, 'Forge Ember'), x, z) for (x, z) in SPOTS[:2]), []) + \
        ['execute if score #gt bm.rng matches ..2 run ' + l for l in sum((spawn(*cube(3, 'Forge Ember'), x, z) for (x, z) in SPOTS[2:4]), [])] + \
        ['execute if score #gt bm.rng matches 3.. run ' + l for l in sum((spawn(*mk('blaze', 'Forge Blaze', '#ffb040', {}, WV), x, z) for (x, z) in SPOTS[2:5]), [])]
    w3 = ['execute if score #gt bm.rng matches ..2 run ' + l for l in spawn(*cube(4, 'The Forge Keeper'), 12, 12)] + \
        ['execute if score #gt bm.rng matches 3.. run ' + l for l in spawn(*keeper, 12, 12)] + \
        ['execute if score #gt bm.rng matches 5 run ' + l for l in sum((spawn(*mk('wither_skeleton', 'Forge Reaver', '#5a5a6a', {'mainhand': 'minecraft:stone_sword'}, WV), x, z)
                                                                         for (x, z) in SPOTS[4:6]), [])]
    fn('p90/forge/init', ['function bm:p70/ctx', sign(2.5, 7.5, 12, 'THE BLAZE FORGE', 'Three waves of the Nether\'s worst. Then the Forge Keeper.', '#ff8a3a')])
    fn('p90/forge/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'scoreboard players set @a[tag=bm.gvp,distance=..15] bm.gvmz 5',
                          'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..9] run function bm:p90/forge/wave',
                          'execute unless score @s bm.gvs matches 1 run return 0',
                          'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #20 bm.rng',
                          'execute unless score #q bm.rng matches 0 run return 0',
                          'execute store result score #n bm.rng if entity @e[tag=bm.gvwv,distance=..18]',
                          'execute if score #n bm.rng matches 0 if score @s bm.gvw matches 3.. run return run function bm:p90/forge/done',
                          'execute if score #n bm.rng matches 0 run function bm:p90/forge/wave'])
    fn('p90/forge/wave', ['function bm:p70/ctx', 'scoreboard players set @s bm.gvs 1', 'scoreboard players add @s bm.gvw 1',
                          'execute if score @s bm.gvw matches 1 run function bm:p90/forge/w1', 'execute if score @s bm.gvw matches 2 run function bm:p90/forge/w2',
                          'execute if score @s bm.gvw matches 3 run function bm:p90/forge/w3',
                          f'playsound minecraft:block.blastfurnace.fire_crackle hostile @a[distance=..20] ~ ~ ~ 1 0.6', f'particle minecraft:lava {rel(12, 5, 19)} 1 0.5 1 0 30',
                          'execute if score @s bm.gvw matches 1..2 run ' + title('@a[tag=bm.gvp,distance=..16]', 'actionbar', [T('The forge roars - wave ', '#ff8a3a'),
                                                                                                                                  {'score': {'name': '@s', 'objective': 'bm.gvw'}, 'color': 'white', 'bold': True},
                                                                                                                                  T(' of 3', 'gray')])] +
       ['execute if score @s bm.gvw matches 3 run ' + l for l in big('THE FORGE KEEPER', 'It steps out of the fire.', '#ff5a20', '@a[tag=bm.gvp,distance=..16]')])
    fn('p90/forge/w1', w1); fn('p90/forge/w2', w2); fn('p90/forge/w3', w3)
    fn('p90/forge/done', ['scoreboard players set @s bm.gvs 2'] + pot(8) + big('THE FORGE GOES COLD', 'The way on is open.', '#ff8a3a', '@a[tag=bm.gvp,distance=..16]') +
       [f'effect give @a[tag=bm.gvp,distance=..16] minecraft:fire_resistance 120 0', 'function bm:p70/solved'])

    # ================================================================== THE VOID GARDEN
    shulker = mk('shulker', 'Void Warden', '#c080ff', {}, {'Tags': ['bm.gvg', 'bm.gvnew2', 'bm.tiered', 'bm.seen', 'bm.gvvoid']})
    eye_box = lambda i, x, z: f'summon minecraft:interaction {rel(x + 0.5, 4, z + 0.5)} ' + snbt({'Tags': ['bm.gvprop', 'bm.gveye', f'bm.gveye{i}'], 'width': F(1.2),
                                                                                                    'height': F(1.2), 'response': B(1)})
    SH_SPOTS = [(7, 9), (16, 16), (12, 12)]
    fn('p90/voidg/init', ['function bm:p70/ctx'] + [eye_box(i, x, z) for i, (x, z) in enumerate(VOID_EYES)] +
       [label(x + 0.5, 5.6, z + 0.5, T('◉', '#c080ff', bold=True), 0.9, ('bm.gvprop', f'bm.gveyel{i}')) for i, (x, z) in enumerate(VOID_EYES)] +
       ['scoreboard players set #n bm.rng 1', 'execute if score #gt bm.rng matches 4.. run scoreboard players set #n bm.rng 2', 'execute if score #gt bm.rng matches 5 run scoreboard players set #n bm.rng 3'] +
       [f'execute if score #n bm.rng matches {i + 1}.. positioned {rel(x, 4, z)} run summon minecraft:shulker ~ ~ ~ {snbt(shulker[1])}' for i, (x, z) in enumerate(SH_SPOTS)] +
       [f'execute positioned {rel(x, 4, z)} run function bm:p70/guard_set' for (x, z) in SH_SPOTS] +
       [sign(1.5, 7.5, 12, 'THE VOID GARDEN', 'Wake the three Eye shrines. Mind the drop - and the shulkers.', '#c080ff')])
    fn('p90/voidg/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'scoreboard players set @a[tag=bm.gvp,distance=..15] bm.gvmz 9',
                          'execute as @e[type=minecraft:interaction,tag=bm.gveye,distance=..16] if data entity @s interaction at @s run function bm:p90/voidg/wake',
                          'execute store result score #n bm.rng if entity @e[type=minecraft:interaction,tag=bm.gveye,tag=bm.gvwoke,distance=..16]',
                          'execute if score #n bm.rng matches 3 run function bm:p90/voidg/done'])
    fn('p90/voidg/wake', ['data remove entity @s interaction', 'execute if entity @s[tag=bm.gvwoke] run return 0', 'tag @s add bm.gvwoke',
                          'setblock ~ ~ ~ minecraft:end_portal_frame[eye=true,facing=north]', 'particle minecraft:portal ~ ~1 ~ 0.4 0.6 0.4 0.3 60',
                          'playsound minecraft:block.end_portal_frame.fill block @a[distance=..20] ~ ~ ~ 1 1',
                          title('@a[tag=bm.gvp,distance=..16]', 'actionbar', T('An Eye shrine wakes...', '#c080ff'))])
    fn('p90/voidg/done', ['scoreboard players set @s bm.gvs 2', 'execute as @e[tag=bm.gvvoid,distance=..20] at @s run particle minecraft:reverse_portal ~ ~0.5 ~ 0.3 0.3 0.3 0.05 20',
                          'tag @e[tag=bm.gvvoid,distance=..20] add bm.gvgone', 'tp @e[tag=bm.gvgone] ~ -200 ~', 'kill @e[tag=bm.gvgone]', 'playsound minecraft:block.end_portal.spawn block @a[distance=..20] ~ ~ ~ 0.6 1.4'] +
       pot(8) + big('THE GARDEN OPENS', 'Three eyes watch you go.', '#c080ff', '@a[tag=bm.gvp,distance=..16]') + ['function bm:p70/solved'])

    # ================================================================== THE HOLLOW RELIQUARY (a memory: watch the seals, strike them in order)
    wisp = mk('vex', 'Hollow Wisp', '#e5e4e2', {}, {'Tags': ['bm.gvg', 'bm.gvnew2', 'bm.tiered', 'bm.seen', 'bm.gvwisp']})
    fn('p90/hollow/init', ['function bm:p70/ctx', 'scoreboard players operation @s bm.gvt = #gt bm.rng',
                           sign(2.5, 7.5, 12, 'THE HOLLOW RELIQUARY', 'Watch the seals flare. Strike them in the same order.', '#e5e4e2')])
    seal_flash = lambda i: [f'particle minecraft:end_rod {rel(SEALS[i][0], 7, 0.6)} 0.6 0.6 0.1 0.02 30',
                            f'particle minecraft:soul_fire_flame {rel(SEALS[i][0], 7, 0.8)} 0.6 0.6 0.1 0.01 12',
                            f'playsound minecraft:block.note_block.chime block @a[distance=..20] {rel(SEALS[i][0], 7, 1)} 1 {[0.7, 0.9, 1.2, 1.5][i]}']
    for i in range(4): fn(f'p90/hollow/flash{i}', seal_flash(i))
    fn('p90/hollow/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'scoreboard players set @a[tag=bm.gvp,distance=..15] bm.gvmz 6',
                           'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..9] run function bm:p90/hollow/new',
                           # (1: showing - a seal every 16 ticks; 2: your turn)
                           'execute if score @s bm.gvs matches 1 run function bm:p90/hollow/show',
                           'execute if score @s bm.gvs matches 2 run function bm:p90/hollow/turn'])
    # the sequence: storage bm:gv hol.i{gi} = [..]; length 5 (6 from Tier IV)
    fn('p90/hollow/new', ['function bm:p70/ctx', 'scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvtm 0', 'scoreboard players set @s bm.gvw 0',
                          'scoreboard players set @s bm.gvc 5', 'execute if score #gt bm.rng matches 4.. run scoreboard players set @s bm.gvc 6',
                          'execute store result storage bm:gv hol.gi int 1 run scoreboard players get #gi bm.rng', 'function bm:p90/hollow/clear with storage bm:gv hol',
                          'scoreboard players set #k bm.rng 0', 'function bm:p90/hollow/roll',
                          'execute if score #gt bm.rng matches 3.. unless entity @e[tag=bm.gvwisp,distance=..20] positioned ~ ~2 ~ run function bm:p90/hollow/wisps',
                          title('@a[tag=bm.gvp,distance=..16]', 'actionbar', T('Watch the seals...', '#e5e4e2'))])
    fn('p90/hollow/clear', ['$data modify storage bm:gv hol.s$(gi) set value []'])
    fn('p90/hollow/roll', ['execute if score #k bm.rng >= @s bm.gvc run return 0', 'execute store result storage bm:gv hol.v int 1 run random value 0..3',
                           'function bm:p90/hollow/push with storage bm:gv hol', 'scoreboard players add #k bm.rng 1', 'function bm:p90/hollow/roll'])
    fn('p90/hollow/push', ['$data modify storage bm:gv hol.s$(gi) append value $(v)'])
    fn('p90/hollow/wisps', [f'summon minecraft:vex ~ ~ ~ {snbt(wisp[1])}', 'function bm:p70/guard_set', f'summon minecraft:vex ~2 ~ ~ {snbt(wisp[1])}', 'function bm:p70/guard_set'])
    fn('p90/hollow/show', ['scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #16 bm.rng',
                           'execute unless score #q bm.rng matches 0 run return 0',
                           'execute if score @s bm.gvw >= @s bm.gvc run return run function bm:p90/hollow/your_turn',
                           'execute store result storage bm:gv hol.k int 1 run scoreboard players get @s bm.gvw',
                           'execute store result storage bm:gv hol.gi int 1 run scoreboard players get #gi bm.rng',
                           'function bm:p90/hollow/at with storage bm:gv hol'] +
       [f'execute if score #v bm.rng matches {i} run function bm:p90/hollow/flash{i}' for i in range(4)] + ['scoreboard players add @s bm.gvw 1'])
    fn('p90/hollow/at', ['$execute store result score #v bm.rng run data get storage bm:gv hol.s$(gi)[$(k)]'])
    fn('p90/hollow/your_turn', ['scoreboard players set @s bm.gvs 2', 'scoreboard players set @s bm.gvw 0'] +
       [f'setblock {rel(x, 5, 1)} minecraft:polished_blackstone_button[face=wall,facing=south,powered=false]' for (x, _b, _c) in SEALS] +
       [title('@a[tag=bm.gvp,distance=..16]', 'actionbar', T('Your turn: strike the seals in that order.', '#e5e4e2', bold=True))])
    turn = ['scoreboard players set #p bm.rng -1']
    for i, (x, _b, _c) in enumerate(SEALS):
        turn += [f'execute if block {rel(x, 5, 1)} minecraft:polished_blackstone_button[powered=true] run scoreboard players set #p bm.rng {i}',
                 f'execute if block {rel(x, 5, 1)} minecraft:polished_blackstone_button[powered=true] run setblock {rel(x, 5, 1)} minecraft:polished_blackstone_button[face=wall,facing=south,powered=false]']
    turn += ['execute if score #p bm.rng matches -1 run return 0',
             'execute store result storage bm:gv hol.k int 1 run scoreboard players get @s bm.gvw', 'execute store result storage bm:gv hol.gi int 1 run scoreboard players get #gi bm.rng',
             'function bm:p90/hollow/at with storage bm:gv hol',
             'execute unless score #p bm.rng = #v bm.rng run return run function bm:p90/hollow/wrong'] + \
        [f'execute if score #p bm.rng matches {i} run function bm:p90/hollow/flash{i}' for i in range(4)] + \
        ['scoreboard players add @s bm.gvw 1', 'execute if score @s bm.gvw >= @s bm.gvc run function bm:p90/hollow/done']
    fn('p90/hollow/turn', turn)
    fn('p90/hollow/wrong', [title('@a[tag=bm.gvp,distance=..16]', 'actionbar', T('Wrong seal! The Hollow stirs... watch again.', 'red', bold=True)),
                            'playsound minecraft:entity.wither.ambient hostile @a[distance=..20] ~ ~ ~ 0.6 1.4', 'scoreboard players set #add bm.rng 2', 'function bm:p70/oops',
                            'scoreboard players set @s bm.gvs 0'])
    fn('p90/hollow/done', ['scoreboard players set @s bm.gvs 2', 'kill @e[tag=bm.gvwisp,distance=..24]'] + pot(10) +
       big('THE SEALS ARE STILLED', 'A Hollow relic for each of you - in The Haul.', '#e5e4e2', '@a[tag=bm.gvp,distance=..16]') +
       ['execute as @a[tag=bm.gvp,distance=..300] if score @s bm.gvi = #gi bm.rng run function bm:p81/defer {t:"bm:p2/hollow/hidden"}',
        'playsound minecraft:ui.toast.challenge_complete player @a[distance=..20] ~ ~ ~ 0.8 0.8', 'function bm:p70/solved'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #16 bm.rng 16']
    # ================================================================== NO FARMING THE VAULT: its creatures drop nothing of their own
    # (a raid's rewards come through the pot and The Haul; whatever spawns in the vault - a guard, a split magma cube, a Vorn
    #  trooper, a shulker - drops no shells, rods, skulls or gear. Bosses and rare mobs pay out through their death handlers)
    HOSTILE = ['zombie', 'husk', 'drowned', 'zombie_villager', 'skeleton', 'stray', 'bogged', 'wither_skeleton', 'spider', 'cave_spider', 'creeper', 'witch',
               'vindicator', 'pillager', 'evoker', 'vex', 'ravager', 'illusioner', 'piglin', 'piglin_brute', 'zombified_piglin', 'hoglin', 'zoglin', 'blaze',
               'ghast', 'magma_cube', 'slime', 'endermite', 'enderman', 'shulker', 'silverfish', 'phantom', 'guardian', 'elder_guardian', 'warden', 'breeze',
               'creaking', 'giant', 'wither']
    wjson('bm/tags/entity_type/gv_hostile.json', {'values': [f'minecraft:{h}' for h in HOSTILE]})
    G.FUNCS['loop/fast'][-1:-1] = ['execute in bm:gutter as @e[type=#bm:gv_hostile,tag=!bm.gvlt,distance=0..] run function bm:p90/nodrops']
    # (2.82: no phantom in the vault at all - one wandering in, or spawned for a sleepless raider, sticks to the ceilings)
    G.FUNCS['loop/second'][-1:-1] = ['execute in bm:gutter as @e[type=minecraft:phantom,distance=0..] at @s run function bm:p90/nophantom']
    fn('p90/nophantom', ['tp @s ~ -400 ~', 'kill @s'])
    fn('p90/nodrops', ['tag @s add bm.gvlt',
                       'data merge entity @s {DeathLootTable:"bm:gv/guard",drop_chances:{mainhand:0f,offhand:0f,head:0f,chest:0f,legs:0f,feet:0f,body:0f}}'])

    # admin: lay one of the new rooms next (for testing)
    for k in ks:
        fn(f'admin/room_{k}', [f'scoreboard players set #frm bm.gvv {EVENTS.index(k) + 1}', tellraw('@s', P + [T(f'The next event room drawn is {NAMES[k]}.', 'gray')])])
    for t in range(1, 6):
        L = G.FUNCS[f'p75/lay/event{t}']
        L.insert(0, 'execute if score #frm bm.gvv matches 1.. run return run function bm:p90/lay/forced')
    fn('p90/lay/forced', ['scoreboard players operation #r bm.rng = #frm bm.gvv', 'scoreboard players remove #r bm.rng 1', 'scoreboard players set #frm bm.gvv 0',
                          'function bm:p90/lay/ebit', 'execute if score #q2 bm.rng matches 0 run scoreboard players operation #epool bm.rng += #bit bm.rng'] +
       [f'execute if score #r bm.rng matches {EVENTS.index(k)} run return run function bm:p90/lay/place_{k}' for k in EVENTS])
    for k in EVENTS:
        fn(f'p90/lay/place_{k}', [f'function bm:p75/pc/{k}'])

"""2.67: THE VAULT, KINDER - plain supplies in every haul, larders in the rooms, food for the Endless Vault, paperweights
for the scales, and THE LOCKER HALL.

THE HAUL'S SUPPLIES: every won heist packs plain, useful goods as well - logs, planks, cobblestone, stone, deepslate,
  bricks, glass, sand, torches, iron, copper, coal, string, leather, redstone... (three stacks at Tier I, seven at V).
LARDERS: about one room in three keeps a larder barrel by its door - bread, cooked meat, baked potatoes, pie, now and
  then a golden carrot or (higher up) a golden apple. Every Rats' Rest has a well-stocked one.
THE ENDLESS VAULT: its kits carry far more food (32 more steak, 16 golden carrots).
PAPERWEIGHTS: three in every kit. Drop one (Q) on a golden scale and it stays tipped - pick it back up after.
THE LOCKER HALL: an annexe off the den (the copper plate by the leave plate, before the heist begins) or through the
  Fixer's Ledger anywhere outside a heist. Eighteen bays of double chests, two high, round three walls: right-click a
  bay's plaque to claim it (three each). One Locker Key opens all your bays - hold it when you open one. Sneak +
  right-click your plaque to give a bay up (empty it first). From the den, only heist tools go back in with you.
  (You can't break anything in the hall - it puts you in adventure mode while you're there.)
"""
from items import item, T, TOTEM, ITEMS
from nbt import snbt, B, F, Int
import phase70_rooms as RM
import phase72 as P72

GOLD = '#ffcf40'
LOCK = '#c89a5a'
item('paperweight', TOTEM, "Fixer's Paperweight", '#b8c0c8', ['A lump of lead with a brass handle.', ('Drop it (Q) on a pressure plate', 'blue'),
                                                             ('to hold it down. Pick it up after.', 'blue')], model='minecraft:heavy_core', stack=16, cat='misc')
item('locker_key', TOTEM, 'Locker Key', LOCK, ['Brass, and stamped with your name.', ('Opens your bays in the Locker Hall -', 'blue'),
                                               ('hold it when you open one.', 'blue')], model='minecraft:trial_key', stack=1, cat='misc')
P72.KEEP += ['paperweight', 'locker_key']

# ---------------------------------------------------------------- the haul's plain supplies
SUPPLY = [('oak_log', 14, 8, 16), ('spruce_log', 10, 8, 16), ('birch_log', 8, 8, 16), ('dark_oak_log', 6, 8, 16), ('oak_planks', 6, 32, 64),
          ('cobblestone', 14, 32, 64), ('stone', 10, 16, 48), ('cobbled_deepslate', 10, 32, 64), ('deepslate', 6, 16, 32),
          ('stone_bricks', 7, 16, 32), ('deepslate_bricks', 5, 16, 32), ('smooth_stone', 5, 16, 32), ('bricks', 5, 16, 32),
          ('glass', 7, 16, 32), ('sand', 5, 16, 32), ('gravel', 3, 16, 32), ('white_wool', 3, 8, 16), ('torch', 7, 16, 32), ('ladder', 3, 8, 16),
          ('iron_ingot', 7, 4, 12), ('copper_ingot', 5, 8, 16), ('coal', 9, 8, 24), ('string', 5, 4, 12), ('leather', 4, 4, 8),
          ('redstone', 5, 8, 16), ('flint', 3, 4, 8), ('paper', 3, 8, 16), ('slime_ball', 2, 2, 6), ('quartz', 3, 8, 16),
          ('lapis_lazuli', 3, 4, 12), ('clay_ball', 3, 8, 16)]
SUPPLY_ROLLS = {1: 3, 2: 4, 3: 5, 4: 6, 5: 7}
LARDER = [('bread', 14, 3, 6), ('cooked_beef', 10, 2, 5), ('cooked_porkchop', 8, 2, 5), ('cooked_mutton', 6, 2, 5), ('cooked_chicken', 6, 2, 5),
          ('baked_potato', 10, 3, 6), ('apple', 6, 2, 4), ('pumpkin_pie', 4, 1, 2), ('cookie', 4, 4, 8), ('golden_carrot', 4, 2, 4), ('honey_bottle', 2, 1, 2)]

# ---------------------------------------------------------------- the Locker Hall: one chunk of bm:gutter, kept loaded
HX, HZ, HY = -256, -256, 63                                  # the chunk's corner; the floor's block layer
IN_LO, IN_HI = -255, -242                                    # the inside (x and z)
ARRIVE = (-248.5, 64, -244.5)
EXIT_PLATE = (-249, 64, -242)
MAXBAYS = 3
HALL_VER = 1


def bays():
    """[(n, [(x, y, z, state)...4 chest cells], plaque centre (x, y, z))] - north, west and east walls, six bays each"""
    out = []
    for i, x in enumerate(range(-254, -243, 2)):             # north wall, facing south
        cells = [(x, y, IN_LO, 'facing=south,type=right') for y in (64, 65)] + [(x + 1, y, IN_LO, 'facing=south,type=left') for y in (64, 65)]
        out.append((len(out) + 1, cells, (x + 1.0, 66.1, IN_LO + 0.55)))
    for z in range(-254, -243, 2):                           # west wall, facing east
        cells = [(IN_LO, y, z, 'facing=east,type=left') for y in (64, 65)] + [(IN_LO, y, z + 1, 'facing=east,type=right') for y in (64, 65)]
        out.append((len(out) + 1, cells, (IN_LO + 0.55, 66.1, z + 1.0)))
    for z in range(-254, -243, 2):                           # east wall, facing west
        cells = [(IN_HI, y, z, 'facing=west,type=right') for y in (64, 65)] + [(IN_HI, y, z + 1, 'facing=west,type=left') for y in (64, 65)]
        out.append((len(out) + 1, cells, (IN_HI + 0.45, 66.1, z + 1.0)))
    return out


def extend_offers(O, offer):
    pass


def generate(G):
    fn, wjson, tellraw, title = G.fn, G.wjson, G.tellraw, G.title
    import phase70 as P70
    import phase80 as P80
    rel = RM.rel
    P = [T('[', 'dark_gray'), T('Vault', GOLD, bold=True), T('] ', 'dark_gray')]
    say = lambda txt, col='gray': tellraw('@s', P + [T(txt, col)])
    ident = [F(0), F(0), F(0), F(1)]
    fast, second = [], []
    objs = ['bm.lkn', 'bm.lko']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + [f'execute in bm:gutter run forceload add {HX} {HZ}']
    G.OBJECTIVES += objs
    HA, HB = '-200 64 -197', '-198 64 -197'
    def ins(table, cond=''):
        return [f'execute {cond}in bm:gutter unless data block {HA} Items[26] run loot insert {HA} loot {table}',
                f'execute {cond}in bm:gutter if data block {HA} Items[26] run loot insert {HB} loot {table}']
    def entry(i, w, lo, hi):
        return {'type': 'minecraft:item', 'name': 'minecraft:' + i, 'weight': w, 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(lo, hi)}]}

    # ================================================================== THE HAUL'S SUPPLIES
    for t, n in SUPPLY_ROLLS.items():
        wjson(f'bm/loot_table/p84/supplies_t{t}.json', {'pools': [{'rolls': n, 'entries': [entry(*e) for e in SUPPLY]}]})
    haul = G.FUNCS['p70/haul']
    k = haul.index('function bm:p75/prize')
    haul[k:k] = sum((ins(f'bm:p84/supplies_t{t}', f'if score #gt bm.rng matches {t} ') for t in SUPPLY_ROLLS), [])

    # ================================================================== LARDERS
    for t in range(1, 6):
        extra = [{'type': 'minecraft:item', 'name': 'minecraft:golden_apple', 'weight': t - 2}] if t >= 3 else []
        wjson(f'bm/loot_table/p84/larder_t{t}.json', {'type': 'minecraft:chest', 'pools': [{'rolls': G.uni(2, 3), 'entries': [entry(*e) for e in LARDER] + extra}]})
        wjson(f'bm/loot_table/p84/larder_rest_t{t}.json', {'type': 'minecraft:chest', 'pools': [{'rolls': G.uni(5, 7), 'entries': [entry(*e) for e in LARDER] + extra}]})
    k = G.FUNCS['p70/r/init'].index('function bm:p76/secret/maybe') + 1
    G.FUNCS['p70/r/init'][k:k] = ['function bm:p84/larder/maybe']
    skip = ['lobby', 'vault', 'cache', 'arena']
    fn('p84/larder/maybe', [f'execute if entity @s[tag=bm.gvr_{k_}] run return 0' for k_ in skip] +
       ['function bm:p70/ctx', 'scoreboard players set #lr bm.rng 0', 'execute if entity @s[tag=bm.gvr_rest] run scoreboard players set #lr bm.rng 1',
        'execute store result score #r bm.rng run random value 1..100', 'execute if score #lr bm.rng matches 0 if score #r bm.rng matches 34.. run return 0',
        f'execute if block {rel(1, 4, 8)} minecraft:air run return run function bm:p84/larder/put_a',
        f'execute if block {rel(1, 4, 16)} minecraft:air run return run function bm:p84/larder/put_b'])
    for nm, (x, z) in (('a', (1, 8)), ('b', (1, 16))):
        fn(f'p84/larder/put_{nm}', [f'execute if score #lr bm.rng matches 0 if score #gt bm.rng matches {t} run setblock {rel(x, 4, z)} minecraft:barrel[facing=east]{{LootTable:"bm:p84/larder_t{t}"}}'
                                     for t in range(1, 6)] +
           [f'execute if score #lr bm.rng matches 1 if score #gt bm.rng matches {t} run setblock {rel(x, 4, z)} minecraft:barrel[facing=east]{{LootTable:"bm:p84/larder_rest_t{t}"}}'
            for t in range(1, 6)] +
           [f'execute unless block {rel(x, 5, z)} minecraft:air run return 0', f'setblock {rel(x, 5, z)} minecraft:candle[candles=3,lit=true]',
            f'summon minecraft:text_display {rel(x, 5.7, z)} ' + snbt({'Tags': ['bm.gvprop'], 'billboard': 'vertical', 'background': Int(0x70000000),
                                                                     'text': T('LARDER', '#e8b070', bold=True),
                                                                     'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0)] * 3,
                                                                                        'scale': [F(0.45)] * 3}})])

    # ================================================================== KITS: paperweights for everyone, the Endless Vault's extra food
    ka = P72.kit_arg
    G.FUNCS['p80/kit/extras'] += [f'give @s {ka("paperweight")} 3', 'scoreboard players operation #gi bm.rng = @s bm.gvi', 'function bm:p77/mode',
                                  f'execute if score #md bm.rng matches 2 run give @s {ka("minecraft:cooked_beef")} 32',
                                  f'execute if score #md bm.rng matches 2 run give @s {ka("minecraft:golden_carrot")} 16']

    # ================================================================== THE LOCKER HALL
    B_ = bays()
    x0, z0, x1, z1 = HX, HZ, HX + 15, HZ + 15
    def plaque(n, free=True):
        return snbt({'text': '', 'extra': [T(f'LOCKER {n}\n', LOCK, bold=True)] +
                     ([T('free - right-click to claim', 'gray')] if free else [T('?', 'white'), T('\nsneak + right-click: give it up', 'dark_gray')])})
    build = [f'kill @e[type=minecraft:interaction,tag=bm.lkb,x={x0},y=60,z={z0},dx=16,dy=14,dz=16]',
             f'kill @e[type=minecraft:text_display,tag=bm.lkt,x={x0},y=60,z={z0},dx=16,dy=14,dz=16]',
             f'fill {x0} {HY - 1} {z0} {x1} {HY + 8} {z1} minecraft:deepslate_tiles',
             f'fill {IN_LO} {HY + 1} {IN_LO} {IN_HI} {HY + 7} {IN_HI} minecraft:air',
             f'fill {IN_LO} {HY} {IN_LO} {IN_HI} {HY} {IN_HI} minecraft:polished_deepslate',
             f'fill {IN_LO + 2} {HY} {-249} {IN_HI - 2} {HY} {-248} minecraft:gilded_blackstone',
             f'fill {-249} {HY} {IN_LO + 2} {-248} {HY} {IN_HI} minecraft:gilded_blackstone',
             f'fill {IN_LO} {HY + 4} {IN_LO} {IN_HI} {HY + 4} {IN_LO} minecraft:polished_blackstone_bricks',
             f'fill {IN_LO} {HY + 4} {IN_LO} {IN_LO} {HY + 4} {IN_HI} minecraft:polished_blackstone_bricks',
             f'fill {IN_HI} {HY + 4} {IN_LO} {IN_HI} {HY + 4} {IN_HI} minecraft:polished_blackstone_bricks']
    for (lx, lz) in ((-252, -252), (-245, -252), (-252, -245), (-245, -245), (-249, -249)):
        build += [f'setblock {lx} {HY + 8} {lz} minecraft:ochre_froglight', f'setblock {lx} {HY + 7} {lz} minecraft:iron_chain', f'setblock {lx} {HY + 6} {lz} minecraft:lantern[hanging=true]']
    for n, cells, (px, py, pz) in B_:
        build += [f'setblock {cx} {cy} {cz} minecraft:chest[{st}]' for cx, cy, cz, st in cells]
        build += [f'summon minecraft:interaction {px} {py} {pz} ' + snbt({'Tags': ['bm.lkb', f'bm.lkb{n}'], 'width': F(1.7), 'height': F(0.9), 'response': B(1)}),
                  f'summon minecraft:text_display {px} {py + 0.35} {pz} ' + snbt({'Tags': ['bm.lkt', f'bm.lkt{n}'], 'billboard': 'vertical', 'background': Int(0x90000000 - 2 ** 32),
                                                                             'line_width': Int(120), 'text': '',
                                                                             'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0)] * 3,
                                                                                                'scale': [F(0.42)] * 3}}),
                  f'scoreboard players set @e[type=minecraft:interaction,tag=bm.lkb{n}] bm.lkn {n}',
                  f'execute unless score @e[type=minecraft:interaction,tag=bm.lkb{n},limit=1] bm.lko matches 0.. run scoreboard players set @e[type=minecraft:interaction,tag=bm.lkb{n}] bm.lko 0',
                  f'scoreboard players set @e[type=minecraft:text_display,tag=bm.lkt{n}] bm.lkn {n}',
                  f'data modify entity @e[type=minecraft:text_display,tag=bm.lkt{n},limit=1] text set value {plaque(n)}']
    ex, ey, ez = EXIT_PLATE
    build += [f'setblock {ex} {ey - 1} {ez} minecraft:waxed_copper_block', f'setblock {ex} {ey} {ez} minecraft:heavy_weighted_pressure_plate',
              f'summon minecraft:text_display {ex + 0.5} {ey + 1.6} {ez + 0.5} ' + snbt({'Tags': ['bm.lkt'], 'billboard': 'vertical', 'background': Int(0x90000000 - 2 ** 32),
                                                                                    'text': [T('THE WAY BACK\n', GOLD, bold=True), T('step on the plate', 'gray')],
                                                                                    'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0)] * 3,
                                                                                                       'scale': [F(0.55)] * 3}}),
              f'summon minecraft:text_display -248.5 68.3 {IN_LO + 0.6} ' + snbt({'Tags': ['bm.lkt'], 'billboard': 'fixed', 'background': Int(0x90000000 - 2 ** 32), 'line_width': Int(260),
                                                                           'text': [T('THE LOCKER HALL\n', LOCK, bold=True),
                                                                                    T(f'Claim up to {MAXBAYS} bays. Your Locker Key opens them - hold it to open one.', 'gray')],
                                                                           'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0)] * 3,
                                                                                              'scale': [F(0.6)] * 3}}),
              f'data modify storage bm:lk built set value {HALL_VER}']
    fn('p84/hall/build', build)
    second.append(f'execute in bm:gutter if loaded {x0} {HY} {z0} unless data storage bm:lk {{built:{HALL_VER}}} run function bm:p84/hall/build')
    # (inside the hall: no breaking anything - survival players go adventure while they're in it)
    second += [f'execute in bm:gutter positioned {x0} 60 {z0} as @a[dx=15,dy=12,dz=15,gamemode=survival] run function bm:p84/lk/adv',
               'execute as @a[tag=bm.lkadv] unless function bm:p84/lk/inside run function bm:p84/lk/unadv']
    fn('p84/lk/adv', ['gamemode adventure @s', 'tag @s add bm.lkadv'])
    fn('p84/lk/unadv', ['tag @s remove bm.lkadv', 'execute if entity @s[gamemode=adventure] unless entity @s[tag=bm.gvp] run gamemode survival @s'])
    fn('p84/lk/inside', ['execute unless dimension bm:gutter run return 0', f'execute positioned {x0} 60 {z0} if entity @s[dx=15,dy=12,dz=15] run return 1', 'return 0'])

    # ---- getting there: the den's copper plate (before the heist begins), or the Ledger (outside a heist)
    G.FUNCS['p70/r/lobby/init'] += [f'setblock {rel(2, 3, 7)} minecraft:waxed_copper_block', f'setblock {rel(2, 4, 7)} minecraft:heavy_weighted_pressure_plate',
                                    f'summon minecraft:text_display {rel(2, 5.6, 7)} ' + snbt({'Tags': ['bm.gvprop'], 'billboard': 'vertical', 'background': Int(0x70000000),
                                                                                             'text': [T('THE LOCKERS\n', LOCK, bold=True), T('(before the heist begins)', 'gray')],
                                                                                             'transformation': {'left_rotation': ident, 'right_rotation': ident,
                                                                                                                'translation': [F(0)] * 3, 'scale': [F(0.5)] * 3}})]
    G.FUNCS['p70/r/lobby/tick'] += [f'execute positioned {rel(2, 4, 7)} as @a[tag=bm.gvp,distance=..0.7] at @s run function bm:p84/lk/from_den']
    fn('p84/lk/from_den', ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'scoreboard players set #st bm.rng 0',
                           'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng store result score #st bm.rng run scoreboard players get @s bm.gvst',
                           'execute if score #st bm.rng matches 2.. run return run ' + title('@s', 'actionbar', T('The Lockers are shut once the heist is on.', 'red')),
                           'function bm:p84/lk/enter'])
    fn('p84/lk/from_ledger', ['execute if entity @s[tag=bm.gvp] run return run ' + say('In a heist? The Lockers are through the copper plate in the den (before it begins).'),
                              'function bm:p84/lk/enter'])
    fn('p84/lk/enter', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                        'execute store result storage bm:lk tmp.pid int 1 run scoreboard players get @s bm.pid',
                        'data modify storage bm:lk tmp.x set from entity @s Pos[0]', 'data modify storage bm:lk tmp.y set from entity @s Pos[1]',
                        'data modify storage bm:lk tmp.z set from entity @s Pos[2]', 'data modify storage bm:lk tmp.r set from entity @s Rotation[0]',
                        'data modify storage bm:lk tmp.d set from entity @s Dimension', 'function bm:p84/lk/save with storage bm:lk tmp',
                        'execute if entity @s[gamemode=survival] run function bm:p84/lk/adv',
                        f'execute in bm:gutter run tp @s {ARRIVE[0]} {ARRIVE[1]} {ARRIVE[2]} 180 0',
                        'title @s times 5 40 10', title('@s', 'title', T('THE LOCKER HALL', LOCK, bold=True)),
                        title('@s', 'subtitle', T('Claim a bay - your Locker Key opens it', 'gray')),
                        'playsound minecraft:block.iron_door.open player @s ~ ~ ~ 1 0.8'])
    fn('p84/lk/save', ['$data modify storage bm:lk r.p$(pid) set value {x:$(x),y:$(y),z:$(z),r:$(r),d:"$(d)"}'])
    fast.append(f'execute in bm:gutter positioned {ex + 0.5} {ey} {ez + 0.5} as @a[distance=..0.7] at @s run function bm:p84/lk/leave')
    keep_not = '*[' + ','.join(f'!minecraft:custom_data~{{bm:"{t}"}}' for t in P72.KEEP) + ',!minecraft:custom_data~{bm_kit:1b}]'
    fn('p84/lk/leave', ['execute if entity @s[tag=bm.gvp] run return run function bm:p84/lk/to_den', 'function bm:p84/lk/back'])
    fn('p84/lk/to_den', [f'execute if items entity @s {sl} {keep_not} run return run function bm:p84/lk/not_that' for sl in ('container.*', 'armor.*', 'weapon.offhand')] +
       ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'tag @s add bm.lkgo', 'scoreboard players set #ok bm.rng 0',
        'execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby] if score @s bm.gvi = #gi bm.rng at @s run function bm:p84/lk/den_tp',
        'tag @s remove bm.lkgo', 'execute if score #ok bm.rng matches 0 run function bm:p84/lk/back'])
    fn('p84/lk/den_tp', ['scoreboard players set #ok bm.rng 1', 'tp @a[tag=bm.lkgo,limit=1] ~-9 ~ ~-4 270 0'])
    fn('p84/lk/not_that', [f'tp @s {ARRIVE[0]} {ARRIVE[1]} {ARRIVE[2]} 180 0',
                           say('Only heist tools go back into the vault with you - leave the rest in your locker.', 'red'),
                           'playsound minecraft:entity.villager.no player @s ~ ~ ~ 1 1'])
    fn('p84/lk/back', ['execute store result storage bm:lk tmp.pid int 1 run scoreboard players get @s bm.pid', 'function bm:p84/lk/back1 with storage bm:lk tmp'])
    fn('p84/lk/back1', ['$execute unless data storage bm:lk r.p$(pid) run return run function bm:p84/lk/nowhere', '$function bm:p84/lk/back2 with storage bm:lk r.p$(pid)',
                        'function bm:p84/lk/unadv', 'playsound minecraft:block.iron_door.close player @s ~ ~ ~ 1 0.8'])
    fn('p84/lk/back2', ['$execute in $(d) run tp @s $(x) $(y) $(z) $(r) 0'])
    fn('p84/lk/nowhere', ['execute in minecraft:overworld run tp @s 0 200 0', 'effect give @s minecraft:slow_falling 30 0', 'function bm:p84/lk/unadv'])

    # ---- the bays: claim, open, give up
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.lkb] if data entity @s interaction at @s run function bm:p84/lk/click')
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.lkb] if data entity @s attack run data remove entity @s attack')
    fn('p84/lk/click', ['scoreboard players operation #b bm.rng = @s bm.lkn', 'scoreboard players operation #o bm.rng = @s bm.lko', 'tag @s add bm.lkme',
                        'execute on target run function bm:p84/lk/claim', 'tag @s remove bm.lkme', 'data remove entity @s interaction'])
    fn('p84/lk/claim', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                        'execute store result storage bm:lk tmp.pid int 1 run scoreboard players get @s bm.pid',
                        'execute if score #o bm.rng = @s bm.pid if predicate bm:p20/sneaking run return run function bm:p84/lk/release',
                        'execute if score #o bm.rng = @s bm.pid run return run function bm:p84/lk/mine',
                        'execute if score #o bm.rng matches 1.. run return run ' + say('Somebody already keeps their things in this one.', 'red'),
                        'scoreboard players set #n bm.rng 0', 'scoreboard players operation #me bm.rng = @s bm.pid',
                        'execute as @e[type=minecraft:interaction,tag=bm.lkb] if score @s bm.lko = #me bm.rng run scoreboard players add #n bm.rng 1',
                        f'execute if score #n bm.rng matches {MAXBAYS}.. run return run ' + say(f'You keep {MAXBAYS} lockers already - give one up first (sneak + right-click its plaque).', 'red'),
                        'scoreboard players operation @e[type=minecraft:interaction,tag=bm.lkme] bm.lko = @s bm.pid'] +
       [f'execute if score #b bm.rng matches {n} in bm:gutter run function bm:p84/lk/lock{n} with storage bm:lk tmp' for n, *_r in B_] +
       ['function bm:p84/lk/name', 'function bm:p84/lk/key',
        'playsound minecraft:block.chest.locked player @s ~ ~ ~ 1 1.2', tellraw('@s', P + [T('Locker ', LOCK), {'score': {'name': '#b', 'objective': 'bm.rng'}, 'color': 'white', 'bold': True},
                                                                                       T(' is yours. Hold your Locker Key to open it.', LOCK)])])
    fn('p84/lk/mine', ['function bm:p84/lk/key', tellraw('@s', P + [T('Locker ', LOCK), {'score': {'name': '#b', 'objective': 'bm.rng'}, 'color': 'white', 'bold': True},
                                                                   T(' is yours. (Sneak + right-click the plaque to give it up.)', 'gray')])])
    give_key = G.give('locker_key').replace('minecraft:custom_data={bm:"locker_key"', 'minecraft:custom_data={bm:"locker_key",bm_lk:$(pid)')
    assert '$(pid)' in give_key
    fn('p84/lk/key', ['execute if items entity @s container.* *[minecraft:custom_data~{bm:"locker_key"}] run return 0',
                      'execute if items entity @s weapon.offhand *[minecraft:custom_data~{bm:"locker_key"}] run return 0',
                      'function bm:p84/lk/key2 with storage bm:lk tmp', say('The Fixer presses a Locker Key into your hand.', LOCK)])
    fn('p84/lk/key2', ['$' + give_key])
    fn('p84/lk/release', [f'execute if score #b bm.rng matches {n} in bm:gutter if function bm:p84/lk/full{n} run return run ' + say('Empty it first.', 'red') for n, *_r in B_] +
       [f'execute if score #b bm.rng matches {n} in bm:gutter run function bm:p84/lk/unlock{n}' for n, *_r in B_] +
       ['scoreboard players set @e[type=minecraft:interaction,tag=bm.lkme] bm.lko 0'] +
       [f'execute if score #b bm.rng matches {n} run data modify entity @e[type=minecraft:text_display,tag=bm.lkt{n},limit=1] text set value {plaque(n)}' for n, *_r in B_] +
       ['playsound minecraft:block.chest.close player @s ~ ~ ~ 1 0.8', say('You give the locker back to the Fixer.')])
    for n, cells, _p in B_:
        fn(f'p84/lk/lock{n}', [f'$data merge block {cx} {cy} {cz} {{lock:{{predicates:{{"minecraft:custom_data":{{bm_lk:$(pid)}}}}}}}}' for cx, cy, cz, st in cells])
        fn(f'p84/lk/unlock{n}', [f'data remove block {cx} {cy} {cz} lock' for cx, cy, cz, st in cells])
        fn(f'p84/lk/full{n}', [f'execute if data block {cx} {cy} {cz} Items[0] run return 1' for cx, cy, cz, st in cells] + ['return 0'])
    # (the plaque gets the owner's name: resolved through a scratch item_display, then copied in)
    fn('p84/lk/name', ['execute in bm:gutter run summon minecraft:item_display -248.5 64 -248.5 {Tags:["bm.lktmp"],item:{id:"minecraft:paper",count:1}}',
                       'item modify entity @e[type=minecraft:item_display,tag=bm.lktmp,limit=1] contents {function:"minecraft:set_name",target:"custom_name",entity:"this",name:{selector:"@s"}}'] +
       [f'execute if score #b bm.rng matches {n} run function bm:p84/lk/name{n}' for n, *_r in B_] +
       ['kill @e[type=minecraft:item_display,tag=bm.lktmp]'])
    for n, *_r in B_:
        fn(f'p84/lk/name{n}', [f'data modify entity @e[type=minecraft:text_display,tag=bm.lkt{n},limit=1] text set value {plaque(n, False)}',
                               f'data modify entity @e[type=minecraft:text_display,tag=bm.lkt{n},limit=1] text.extra[1] set from entity @e[type=minecraft:item_display,tag=bm.lktmp,limit=1] item.components."minecraft:custom_name"'])
    fn('admin/lockers_reset', ['data remove storage bm:lk built', 'scoreboard players set @e[type=minecraft:interaction,tag=bm.lkb] bm.lko 0',
                               tellraw('@s', P + [T('The Locker Hall rebuilds within a second; every bay is free again (contents kept, locks lifted).', 'gray')])] +
       [f'execute in bm:gutter run function bm:p84/lk/unlock{n}' for n, *_r in B_])

    f = G.FUNCS['loop/fast']
    f[-1:-1] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


def rp(R):
    pass

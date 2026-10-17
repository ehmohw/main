"""2.71: THREE WAYS THROUGH THE NEW PUZZLES (the Spire, the Tinker's Bench, the Mason's Plan, the Dig).

THE SPIRE            A  the spiral of single blocks (as before)
                     B  THE LADDER SPIRE: three posts with ladders up their sides; jump-grab each ladder, climb, and leap
                        across to the next post. A checkpoint on the second post
                     C  THE SWITCH SPIRE: red and blue blocks - only one colour is solid at a time. Each gold switch post
                        has a button: press it and the colours swap. Swap at the wrong moment and someone falls
THE TINKER'S BENCH   A  make what the Fixer names (as before)
                     B  THE RIDDLE: he won't say what he wants - just a riddle. You're given the parts for three things;
                        make the one the riddle means. Hand in the wrong one and the alarm rings
                     C  THE HERALD'S BANNER: copy the banner on the wall at the looms - the colours, the shapes and the
                        order they go on in. A wrong banner rings the alarm (and you get a fresh one)
THE MASON'S PLAN     A  copy the plan (as before)
                     B  (THE MOSAIC, a sudoku-like colour square - retired in 2.82b: the Plan is A or C)
                     C  THE PICTURE: a 5x5 grid and a clue for every row and column (the runs of blocks, in order); lay
                        the black blocks to draw the one picture that fits
THE DIG              A  find the one vein of mud that goes through (as before)
                     B  THE MINEFIELD: packed mud, and TNT hidden in it. Every cell you dig shows how many of the eight
                        round it hide TNT; dig a way across without setting one off (each one rings the alarm)
                     C  THE SCULPTOR: carve the block of calcite until it matches the little model on the plinth - the
                        gold corners line up. RESET puts the block back
"""
from items import T
from nbt import snbt, B, F, Int
import phase70_rooms as RM
import phase110 as P110
import phase112 as P112
import p114data as PD

GOLD = '#ffcf40'
rel, relf, IDENT = RM.rel, P110.relf, P110.IDENT
NUMCOL = {0: 'gray', 1: '#5a8aff', 2: '#4ad04a', 3: '#ff5050', 4: '#3a4ad0', 5: '#b04040', 6: '#30b0b0', 7: '#dddddd', 8: '#888888'}
MCOL = ['red', 'blue', 'yellow', 'lime']


def generate(G):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    label, sign, vbutton, press, themed, crew_say, oops, choose = P110.helpers(G)
    crew = '@a[tag=bm.gvp,distance=..30]'
    def dispatch(k, b, c):
        G.FUNCS[f'p112/{k}/init'][0:0] = ['function bm:p110/var', f'execute if score @s bm.gvvar matches 1 run return run function bm:p114/{k}b/init',
                                          f'execute if score @s bm.gvvar matches 2 run return run function bm:p114/{k}c/init']
        G.FUNCS[f'p112/{k}/tick'][0:0] = [f'execute if score @s bm.gvvar matches 1 run return run function bm:p114/{k}b/tick',
                                          f'execute if score @s bm.gvvar matches 2 run return run function bm:p114/{k}c/tick']
    def room_item(i, extra=''):
        return f'minecraft:{i}[minecraft:custom_data={{bm_room:1b}}{extra}]'
    def mini(blk, pos, s=0.3):
        return f'summon minecraft:block_display {pos} ' + snbt({'Tags': ['bm.gvprop'], 'block_state': blk,
                                                              'transformation': {'left_rotation': IDENT, 'right_rotation': IDENT, 'translation': [F(0)] * 3, 'scale': [F(s)] * 3}})

    # ================================================================== THE SPIRE
    clear_a = [f'setblock {rel(x, t, z)} minecraft:air' for x, z, t in P112.SROUTE]
    def spire_tick(v, cp):
        return ['execute if score @s bm.gvs matches 3 run return 0', 'execute if score @s bm.gvs matches 0 run scoreboard players set @s bm.gvs 1',
                'execute if score @s bm.gvtm matches 3000 run scoreboard players set @s bm.gvf 1', 'scoreboard players operation #me bm.rng = @s bm.gvq',
                f'execute positioned {relf(cp[0] + 0.5, cp[2], cp[1] + 0.5)} as @a[tag=bm.gvp,distance=..0.9] unless score @s bm.gvcpk = #me bm.rng at @s run function bm:p112/spire/cp',
                f'execute positioned {relf(3.6, 3.5, 0.6)} as @a[tag=bm.gvp,dx=20,dy=0.1,dz=22.8] at @s run function bm:p114/spire{v}/fell',
                f'execute unless block {rel(22, P112.SPIRE_EXIT, 12)} minecraft:light_weighted_pressure_plate[power=0] run function bm:p70/solved']
    def spire_fell(v, cp):
        fn(f'p114/spire{v}/fell', ['execute if score @s bm.gvcpk = #me bm.rng at @e[type=minecraft:marker,tag=bm.gvr_spire,distance=..30,sort=nearest,limit=1] run return run tp @s ' +
                                   relf(cp[0] + 0.5, cp[2], cp[1] + 0.5),
                                   'execute at @e[type=minecraft:marker,tag=bm.gvr_spire,distance=..30,sort=nearest,limit=1] run tp @s ' + rel(2, 4, 12) + ' -90 0',
                                   title('@s', 'actionbar', T('Down into the hay! Back to the start.', 'red'))])
    # ---- B: the ladder spire
    binit = ['function bm:p70/ctx'] + clear_a
    for (x, z, f, y0, y1, (px, pz, ptop)) in PD.LADDERS:
        binit += themed(f'fill {rel(px, 4, pz)} {rel(px, ptop - 2, pz)} {{b}}', 'pillar') + themed(f'setblock {rel(px, ptop - 1, pz)} {{b}}', 'trim')
        binit.append(f'fill {rel(x, y0, z)} {rel(x, y1, z)} minecraft:ladder[facing={f}]')
    for k, (x, z, top) in enumerate(n for seg in PD.LJUMPS for n in seg):
        binit += themed(f'setblock {rel(x, top - 1, z)} {{b}}', 'trim' if k % 2 else 'floor')
    bx, bz, bt = PD.BCHECK
    binit += [label(relf(bx + 0.5, bt + 0.9, bz + 0.5), T('CHECKPOINT', GOLD, bold=True), 0.5),
              sign(rel(2, 7.5, 12), 'THE LADDER SPIRE', 'Jump for the ladders, climb, and leap across to the next post. The second post is a CHECKPOINT. The hay sends you back.')]
    fn('p114/spireb/init', binit)
    fn('p114/spireb/tick', spire_tick('b', PD.BCHECK))
    spire_fell('b', PD.BCHECK)
    # ---- C: the switch spire
    posts = [n for n in PD.SROUTE_C if n[3] == 'p']
    cols = {'r': [n for n in PD.SROUTE_C if n[3] == 'r'], 'b': [n for n in PD.SROUTE_C if n[3] == 'b']}
    ghost = lambda c, x, z, top: f'summon minecraft:block_display {relf(x + 0.01, top - 1 + 0.01, z + 0.01)} ' + snbt(
        {'Tags': ['bm.gvprop'], 'block_state': f'minecraft:{"red" if c == "r" else "blue"}_stained_glass', 'brightness': {'block': 12, 'sky': 12},
         'transformation': {'left_rotation': IDENT, 'right_rotation': IDENT, 'translation': [F(0)] * 3, 'scale': [F(0.98)] * 3}})
    cinit = ['function bm:p70/ctx'] + clear_a + ['scoreboard players set @s bm.gvy1 0']
    for (x, z, top, _c) in posts:
        cinit += themed(f'setblock {rel(x, top - 1, z)} {{b}}', 'metal') + [f'setblock {rel(x, top, z)} minecraft:pale_oak_button[face=floor,facing=east,powered=false]']
    for c, ns in cols.items():
        cinit += [ghost(c, x, z, top) for x, z, top, _c in ns]
    cinit += ['function bm:p114/spirec/red']
    cx, cz, ct, _c = PD.CCHECK
    cinit += [label(relf(cx + 0.5, ct + 1.2, cz + 0.5), T('CHECKPOINT', GOLD, bold=True), 0.5),
              sign(rel(2, 7.5, 12), 'THE SWITCH SPIRE', 'Only one colour is solid at a time. Press the button on a gold switch post and red and blue swap. Mind your friends! The middle post is a CHECKPOINT.')]
    fn('p114/spirec/init', cinit)
    fn('p114/spirec/red', [f'setblock {rel(x, top - 1, z)} minecraft:red_concrete' for x, z, top, _c in cols['r']] +
       [f'setblock {rel(x, top - 1, z)} minecraft:air' for x, z, top, _c in cols['b']] + ['scoreboard players set @s bm.gvy1 0'])
    fn('p114/spirec/blue', [f'setblock {rel(x, top - 1, z)} minecraft:blue_concrete' for x, z, top, _c in cols['b']] +
       [f'setblock {rel(x, top - 1, z)} minecraft:air' for x, z, top, _c in cols['r']] + ['scoreboard players set @s bm.gvy1 1'])
    fn('p114/spirec/swap', ['execute if score @s bm.gvy1 matches 1 run return run function bm:p114/spirec/to_red', 'function bm:p114/spirec/to_blue'])
    for c, nm in (('red', 'RED'), ('blue', 'BLUE')):
        fn(f'p114/spirec/to_{c}', [f'function bm:p114/spirec/{c}', 'playsound minecraft:block.note_block.pling block @a[distance=..30] ~ ~5 ~ 1 ' + ('1.6' if c == 'red' else '1.1'),
                                   crew_say([T('Switch! ', GOLD, bold=True), T(nm, '#ff5050' if c == 'red' else '#5a8aff', bold=True), T(' blocks are solid now.', 'gray')], r=30)])
    CC = (cx, cz, ct)
    ctick = spire_tick('c', CC)
    for i, (x, z, top, _c) in enumerate(posts):
        ctick[4:4] = press(f'sw{i}', (x, top, z), 'bm:p114/spirec/swap')
    fn('p114/spirec/tick', ctick)
    spire_fell('c', CC)
    dispatch('spire', None, None)

    # ================================================================== THE TINKER'S BENCH
    # ---- B: the riddle
    RID = {1: [('compass', 'I always point the same way home, however lost you are.', [('iron_ingot', 4), ('redstone', 1)]),
               ('clock', 'Down in the dark, I still know whether the sun is up.', [('gold_ingot', 4), ('redstone', 1)]),
               ('shears', 'Two blades, no handle: I take the wool and leave the sheep.', [('iron_ingot', 2)])],
           2: [('bucket', "I carry the sea - or a cow's breakfast.", [('iron_ingot', 3)]),
               ('fishing_rod', 'A stick, a thread and patience, and the river pays you.', [('stick', 3), ('string', 2)]),
               ('bow', 'I bend, I sing, and feathers fly.', [('stick', 3), ('string', 3)])],
           3: [('spyglass', 'I bring the far hills near.', [('copper_ingot', 2), ('amethyst_shard', 1)]),
               ('flint_and_steel', 'Strike me and the world catches fire.', [('iron_ingot', 1), ('flint', 1)]),
               ('lead', 'I keep the llama close and the horse from wandering.', [('string', 4), ('slime_ball', 1)])],
           4: [('shield', "I take the blow so you don't have to.", [('oak_planks', 6), ('iron_ingot', 1)]),
               ('item_frame', 'I hang on the wall and hold one thing up to be admired.', [('stick', 8), ('leather', 1)]),
               ('brush', 'I sweep the sand from old secrets.', [('feather', 1), ('copper_ingot', 1), ('stick', 1)])],
           5: [('piston', "I push, but never pull - unless I've been made sticky.", [('oak_planks', 3), ('cobblestone', 4), ('iron_ingot', 1), ('redstone', 1)]),
               ('observer', 'I stare at one thing and shout the moment it changes.', [('cobblestone', 6), ('redstone', 2), ('quartz', 1)]),
               ('dropper', 'I spit out whatever you give me, but I have no bow.', [('cobblestone', 7), ('redstone', 1)])]}
    RLEFT = sorted({i for t in RID.values() for c in t for i, _n in c[2]} | {c[0] for t in RID.values() for c in t})
    fn('p114/benchb/init', ['function bm:p70/ctx', 'scoreboard players set @s bm.gvc 0',
                            f'summon minecraft:interaction {relf(12.5, 4, 2.5)} {{Tags:["bm.gvprop","bm.gvhatch"],width:1.2f,height:1.6f,response:1b}}',
                            label(rel(12, 6.6, 2), T("THE FIXER'S HATCH", GOLD, bold=True), 0.5)] +
       [f'execute if score #gt bm.rng matches {t} store result score @s bm.gvc run random value {10 * t}..{10 * t + 2}' for t in RID] +
       [f'execute if score @s bm.gvc matches {10 * t + j} run ' + sign(rel(12, 8.2, 1), "THE FIXER'S RIDDLE", f'He won\'t say what he wants - only this: "{c[1]}" You have the parts for three things. Make the right one and hand it in. A wrong one rings the alarm.', 0.6)
        for t, cs in RID.items() for j, c in enumerate(cs)])
    for t, cs in RID.items():
        need = {}
        for c in cs:
            for i, n in c[2]: need[i] = need.get(i, 0) + n
        fn(f'p114/benchb/give{t}', [f'give @s {room_item(i)} {n}' for i, n in sorted(need.items())] +
           [title('@s', 'actionbar', [T('The Fixer hands you a pile of parts. ', GOLD, bold=True), T('Read his riddle.', 'gray')])])
    fn('p114/benchb/tick', ['execute if score @s bm.gvs matches 3 run return 0',
                            'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..10] run function bm:p114/benchb/start',
                            'execute if score @s bm.gvtm matches 3600 run scoreboard players set @s bm.gvf 1',
                            'execute as @e[type=minecraft:interaction,tag=bm.gvhatch,distance=..14] if data entity @s interaction at @s run function bm:p114/benchb/hatch'])
    fn('p114/benchb/start', ['scoreboard players set @s bm.gvs 1'] + [f'execute if score #gt bm.rng matches {t} as {crew} run function bm:p114/benchb/give{t}' for t in RID])
    fn('p114/benchb/hatch', ['execute on target run function bm:p114/benchb/hand', 'data remove entity @s interaction'])
    fn('p114/benchb/hand', ['execute as @e[type=minecraft:marker,tag=bm.gvr_bench,distance=..16,sort=nearest,limit=1] run scoreboard players operation #rc bm.rng = @s bm.gvc'] +
       [f'execute if score #rc bm.rng matches {10 * t + j} if items entity @s weapon.mainhand minecraft:{c[0]} run return run function bm:p114/benchb/done'
        for t, cs in RID.items() for j, c in enumerate(cs)] +
       [f'execute if score #rc bm.rng matches {10 * t}..{10 * t + 2} if items entity @s weapon.mainhand minecraft:{c[0]} run return run function bm:p114/benchb/wrong'
        for t, cs in RID.items() for c in cs] +
       [title('@s', 'actionbar', T('"That\'s not anything I\'d want." (Hold it in your hand.)', 'red'))])
    fn('p114/benchb/wrong', ['item replace entity @s weapon.mainhand with minecraft:air', 'playsound minecraft:entity.villager.no player @a[distance=..16] ~ ~ ~ 1 0.8',
                             title('@s', 'actionbar', T('"No! That\'s not what I meant." He keeps it - and someone heard him.', 'red')),
                             'execute as @e[type=minecraft:marker,tag=bm.gvr_bench,distance=..16,sort=nearest,limit=1] at @s run function bm:p114/benchb/oops'])
    fn('p114/benchb/oops', oops(2) + ['scoreboard players set @s bm.gvf 1'])
    fn('p114/benchb/done', ['item replace entity @s weapon.mainhand with minecraft:air', 'playsound minecraft:block.barrel.close player @a[distance=..16] ~ ~ ~ 1 1',
                            'execute as @e[type=minecraft:marker,tag=bm.gvr_bench,distance=..16,sort=nearest,limit=1] at @s run function bm:p114/benchb/won'])
    fn('p114/benchb/won', [f'clear {crew} minecraft:{i}[!minecraft:custom_data]' for i in RLEFT] + ['kill @e[type=minecraft:item,distance=..16]', 'function bm:p70/solved'])
    # ---- C: the herald's banner
    def pats(d): return '[' + ','.join(f'{{pattern:"minecraft:{p}",color:"{c}"}}' for p, c in d) + ']'
    fn('p114/benchc/init', ['function bm:p70/ctx', 'scoreboard players set @s bm.gvc 0'] +
       [f'setblock {rel(x, 4, z)} minecraft:loom[facing=north]' for x, z in P112.BENCHES] +
       [f'summon minecraft:interaction {relf(12.5, 4, 2.5)} {{Tags:["bm.gvprop","bm.gvhatch"],width:1.2f,height:1.6f,response:1b}}',
        label(rel(12, 6.6, 2), T("THE FIXER'S HATCH", GOLD, bold=True), 0.5),
        sign(rel(6, 8.2, 1), "THE HERALD'S BANNER", 'Make a banner just like the one on the wall, at the looms: the same colours, the same shapes - laid on in the same order. Hand it in at the hatch.', 0.55)] +
       [f'execute if score #gt bm.rng matches {t} store result score @s bm.gvc run random value {10 * t}..{10 * t + 3}' for t in PD.BANNERS] +
       [f'execute if score @s bm.gvc matches {10 * t + j} run setblock {rel(12, 7, 1)} minecraft:white_wall_banner[facing=south]{{patterns:{pats(d)}}}'
        for t, ds in PD.BANNERS.items() for j, d in enumerate(ds)])
    for t, ds in PD.BANNERS.items():
        for j, d in enumerate(ds):
            dye = sorted({c for _p, c in d})
            decoy = next(c for c in PD.BCOLS if c not in dye)
            fn(f'p114/benchc/give{t}{j}', [f'give @s {room_item("white_banner")} 1'] + [f'give @s {room_item(c + "_dye")} 2' for c in dye] +
               [f'give @s {room_item(decoy + "_dye")} 1', title('@s', 'actionbar', [T('A white banner and some dyes. ', GOLD, bold=True), T('Copy the one on the wall.', 'gray')])])
    BC = [(t, j, d) for t, ds in PD.BANNERS.items() for j, d in enumerate(ds)]
    fn('p114/benchc/tick', ['execute if score @s bm.gvs matches 3 run return 0',
                            'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..10] run function bm:p114/benchc/start',
                            'execute if score @s bm.gvtm matches 3600 run scoreboard players set @s bm.gvf 1',
                            'execute as @e[type=minecraft:interaction,tag=bm.gvhatch,distance=..14] if data entity @s interaction at @s run function bm:p114/benchc/hatch'])
    fn('p114/benchc/start', ['scoreboard players set @s bm.gvs 1', 'scoreboard players operation #rc bm.rng = @s bm.gvc'] +
       [f'execute if score #rc bm.rng matches {10 * t + j} as {crew} run function bm:p114/benchc/give{t}{j}' for t, j, d in BC])
    fn('p114/benchc/hatch', ['execute on target run function bm:p114/benchc/hand', 'data remove entity @s interaction'])
    fn('p114/benchc/hand', ['execute as @e[type=minecraft:marker,tag=bm.gvr_bench,distance=..16,sort=nearest,limit=1] run scoreboard players operation #rc bm.rng = @s bm.gvc'] +
       [f'execute if score #rc bm.rng matches {10 * t + j} if items entity @s weapon.mainhand minecraft:white_banner[minecraft:banner_patterns={pats(d)}] run return run function bm:p114/benchb/done'
        for t, j, d in BC] +
       ['execute if items entity @s weapon.mainhand minecraft:white_banner run return run function bm:p114/benchc/wrong',
        title('@s', 'actionbar', T('"The banner - hold it in your hand."', 'red'))])
    fn('p114/benchc/wrong', ['item replace entity @s weapon.mainhand with minecraft:air', 'playsound minecraft:entity.villager.no player @a[distance=..16] ~ ~ ~ 1 0.8',
                             title('@s', 'actionbar', T('"That\'s not it - look again." A fresh banner, and someone heard him.', 'red')),
                             f'clear @s *[minecraft:custom_data~{{bm_room:1b}}]'] +
       [f'execute if score #rc bm.rng matches {10 * t + j} run function bm:p114/benchc/give{t}{j}' for t, j, d in BC] +
       ['execute as @e[type=minecraft:marker,tag=bm.gvr_bench,distance=..16,sort=nearest,limit=1] at @s run function bm:p114/benchb/oops'])
    dispatch('bench', None, None)

    # ================================================================== THE MASON'S PLAN
    LODE = ',minecraft:can_place_on={blocks:"minecraft:lodestone"}'
    def stone(c, n): return 'give @s ' + room_item(c + '_concrete', LODE) + f' {n}'
    def mfloor(n):
        return themed(f'fill {rel(9, 3, 9)} {rel(15, 3, 15)} {{b}}', 'trim') + [f'fill {rel(9, 4, 9)} {rel(15, 4, 15)} minecraft:air',
                                                                                 f'fill {rel(10, 3, 10)} {rel(9 + n, 3, 9 + n)} minecraft:lodestone']
    def mtick(v, checks):
        return ['execute if score @s bm.gvs matches 3 run return 0',
                f'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..12] run function bm:p114/mason{v}/start',
                'execute if score @s bm.gvtm matches 3000 run scoreboard players set @s bm.gvf 1'] + press('mreset', (2, 5, 9), f'bm:p114/mason{v}/reset') + \
               ['scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #10 bm.rng', 'execute unless score #q bm.rng matches 0 run return 0'] + checks
    # ---- B: (2.82b) the Mosaic - a sudoku-like colour square - is retired: a Mason's Plan is the copy (A) or the Picture (C)
    # ---- C: the picture (a 5x5 nonogram)
    fn('p114/masonc/init', ['function bm:p70/ctx'] + mfloor(5) + choose('#i', len(PD.PICTURES), 'p114/masonc/p') + ['scoreboard players operation @s bm.gvc = #i bm.rng'] +
       vbutton(2, 5, 9, 'east', 'RESET', col='#ff7a7a') +
       [sign(rel(5, 7.4, 13), 'THE PICTURE', 'Lay black blocks on the grid. The numbers by each row (read west to east) and each column (read north to south) are its runs of blocks, in order. One picture fits.', 0.55)])
    for j, (g, rc, cc) in enumerate(PD.PICTURES):
        fn(f'p114/masonc/p{j}', [label(relf(9.5, 4.55, 10.5 + r), T(' '.join(map(str, rc[r])), 'white', bold=True), 0.5) for r in range(5)] +
           [label(relf(10.5 + c, 4.75, 9.5), T('\n'.join(map(str, cc[c])), 'white', bold=True), 0.5) for c in range(5)])
        fn(f'p114/masonc/chk{j}', [f'execute unless block {rel(10 + c, 4, 10 + r)} minecraft:{"black_concrete" if g[r][c] else "air"} run return 0'
                                   for r in range(5) for c in range(5)] + ['return 1'])
        fn(f'p114/masonc/give{j}', [stone('black', sum(map(sum, g)) + 2)])
    fn('p114/masonc/tick', mtick('c', [f'execute if score @s bm.gvc matches {j} if function bm:p114/masonc/chk{j} run return run function bm:p70/solved' for j in range(len(PD.PICTURES))]))
    fn('p114/masonc/start', ['scoreboard players set @s bm.gvs 1', 'function bm:p114/masonc/hand'])
    fn('p114/masonc/hand', [f'clear {crew} *[minecraft:custom_data~{{bm_room:1b}}]'] +
       [f'execute if score @s bm.gvc matches {j} as {crew} run function bm:p114/masonc/give{j}' for j in range(len(PD.PICTURES))] +
       [crew_say('The mason\'s blocks: they only go down on the lodestone.', GOLD, 30)])
    fn('p114/masonc/reset', [f'fill {rel(10, 4, 10)} {rel(14, 4, 14)} minecraft:air replace minecraft:black_concrete', 'function bm:p114/masonc/hand'] + oops(2) +
       ['scoreboard players set @s bm.gvf 1', 'playsound minecraft:block.stone.break block @a[distance=..20] ~ ~ ~ 1 0.8'])
    dispatch('mason', None, None)
    for f in ('p112/mason/init', 'p112/mason/tick'):
        G.FUNCS[f] = [l for l in G.FUNCS[f] if 'p114/masonb/' not in l]
    mi = G.FUNCS['p112/mason/init']
    k = mi.index('function bm:p110/var') + 1
    mi[k:k] = ['execute if score @s bm.gvvar matches 1 store result score @s bm.gvvar run random value 0..1',     # (B gone: A or C, evenly)
               'execute if score @s bm.gvvar matches 1 run scoreboard players set @s bm.gvvar 2']

    # ================================================================== THE DIG
    def pick(blk, nm, lore):
        return (f'minecraft:stone_pickaxe[minecraft:custom_data={{bm_room:1b,bm_digpick:1b}},minecraft:can_break={{blocks:"minecraft:{blk}"}},minecraft:unbreakable={{}},'
                'minecraft:item_name=' + snbt(T(nm, GOLD)) + ',minecraft:lore=[' + snbt(T(lore, 'gray')) + ']]')
    def dtick(v, dx, rest):
        return ['execute if score @s bm.gvs matches 3 run return 0', 'execute if score @s bm.gvs matches 0 run scoreboard players set @s bm.gvs 1',
                'execute if score @s bm.gvtm matches 3000 run scoreboard players set @s bm.gvf 1',
                f'execute positioned {relf(0.6, 3.5, 0.6)} as @a[tag=bm.gvp,dx={dx},dy=3,dz=22.8] unless items entity @s container.* *[minecraft:custom_data~{{bm_digpick:1b}}] run function bm:p114/dig{v}/pick',
                'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #10 bm.rng',
                'execute if score #q bm.rng matches 0 positioned ~-12.5 ~-4 ~-12.5 run kill @e[type=minecraft:item,dx=24,dy=15,dz=24]'] + rest
    # ---- B: the minefield
    fn('p114/digb/pick', ['give @s ' + pick('packed_mud', "The Fixer's Pick", 'It bites only the packed mud.'),
                          title('@s', 'actionbar', [T("The Fixer's pick. ", GOLD, bold=True), T('Dig the packed mud - and count the TNT.', 'gray')])])
    fx0, fx1, fz0, fz1 = PD.FX[0], PD.FX[-1], PD.FZ[0], PD.FZ[-1]
    num = lambda n: f'summon minecraft:text_display ~ ~0.35 ~ ' + snbt({'Tags': ['bm.gvprop'], 'billboard': 'center', 'brightness': {'block': 15, 'sky': 15},
                                                                       'text': T(str(n), NUMCOL[n], bold=True), 'background': Int(0),
                                                                       'transformation': {'left_rotation': IDENT, 'right_rotation': IDENT, 'translation': [F(0)] * 3, 'scale': [F(1.2)] * 3}})
    fn('p114/digb/init', ['function bm:p70/ctx', f'fill {rel(fx0, 4, fz0)} {rel(fx1, 5, fz1)} minecraft:packed_mud', f'fill {rel(fx0, 6, fz0)} {rel(fx1, 6, fz1)} minecraft:deepslate_tiles',
                          f'fill {rel(fx0, 4, fz0)} {rel(fx0, 5, fz1)} minecraft:air', f'fill {rel(fx0, 6, fz0)} {rel(fx0, 6, fz1)} minecraft:polished_deepslate'] +
       choose('#i', len(PD.MINEFIELDS), 'p114/digb/b') + ['scoreboard players operation @s bm.gvc = #i bm.rng'] +
       [sign(rel(4, 7, 12), 'THE MINEFIELD', 'TNT is hidden in the packed mud. Every cell you dig shows how many of the eight round it hide TNT. Dig a way across - set one off and the alarm rings.', 0.6)])
    USED = sorted({nums[c] for mines, nums in PD.MINEFIELDS for c in nums if c not in set(mines)})
    for n in USED:
        fn(f'p114/digb/s{n}', ['fill ~ ~ ~ ~ ~1 ~ minecraft:air', 'setblock ~ ~2 ~ minecraft:polished_deepslate', num(n), 'playsound minecraft:block.mud.break block @a[distance=..16] ~ ~ ~ 0.8 1.2'])
    fn('p114/digb/mine', ['setblock ~ ~ ~ minecraft:tnt', 'setblock ~ ~1 ~ minecraft:tnt', 'setblock ~ ~2 ~ minecraft:polished_deepslate',
                          'particle minecraft:explosion ~ ~1 ~ 0.5 0.5 0.5 0 3', 'playsound minecraft:entity.generic.explode block @a[distance=..30] ~ ~ ~ 1 1.2',
                          crew_say([T('BOOM! ', 'red', bold=True), T('A charge goes off in the mud - and the alarm rings.', 'gray')], r=30)] + oops(2) + ['scoreboard players set @s bm.gvf 1'])
    for j, (mines, nums) in enumerate(PD.MINEFIELDS):
        M = set(mines)
        fn(f'p114/digb/b{j}', [f'execute positioned {relf(fx0 + 0.5, 4, z + 0.5)} run {num(nums[(fx0, z)])}' for z in PD.FZ])
        L = []
        for x in PD.FX:
            if x == fx0: continue
            for z in PD.FZ:
                tgt = 'mine' if (x, z) in M else f's{nums[(x, z)]}'
                for y in (4, 5):
                    L.append(f'execute if block {rel(x, 6, z)} minecraft:deepslate_tiles unless block {rel(x, y, z)} minecraft:packed_mud positioned {relf(x + 0.5, 4, z + 0.5)} run function bm:p114/digb/{tgt}')
        fn(f'p114/digb/c{j}', L)
    fn('p114/digb/tick', dtick('b', 7.8, []) +
       [f'execute if score @s bm.gvc matches {j} run function bm:p114/digb/c{j}' for j in range(len(PD.MINEFIELDS))] +
       [f'execute positioned {relf(17, 3.5, 0.6)} if entity @a[tag=bm.gvp,dx=5.8,dy=3,dz=22.8] positioned as @s run function bm:p70/solved'])
    # ---- C: the sculptor
    fn('p114/digc/pick', ['give @s ' + pick('calcite', "The Sculptor's Chisel", 'It bites only the calcite.'),
                          title('@s', 'actionbar', [T("The Sculptor's chisel. ", GOLD, bold=True), T('Carve the block to match the model.', 'gray')])])
    MO = (3.4, 5.05, 3.4)                  # the model's corner
    fn('p114/digc/init', ['function bm:p70/ctx', f'fill {rel(9, 4, 1)} {rel(15, 14, 23)} minecraft:air', f'fill {rel(11, 4, 11)} {rel(13, 6, 13)} minecraft:calcite'] +
       [f'setblock {rel(10, 3, 10)} minecraft:gold_block'] + themed(f'fill {rel(3, 4, 3)} {rel(5, 4, 5)} {{b}}', 'pillar') +
       [mini('minecraft:gold_block', relf(MO[0] - 0.34, MO[1], MO[2] - 0.34)),
        ] + themed(f'setblock {rel(1, 5, 9)} {{b}}', 'pillar') + vbutton(2, 5, 9, 'east', 'RESET', col='#ff7a7a') +
       choose('#i', len(PD.MODELS), 'p114/digc/m') + ['scoreboard players operation @s bm.gvc = #i bm.rng'] +
       [sign(rel(4, 7.6, 7), 'THE SCULPTOR', 'Carve the calcite until it matches the little model - the gold corners line up. RESET puts the block back (and rings the alarm).', 0.6)])
    cube = [(x, y, z) for x in range(3) for y in range(3) for z in range(3)]
    for j, keep in enumerate(PD.MODELS):
        K = set(keep)
        fn(f'p114/digc/m{j}', [mini('minecraft:calcite', relf(MO[0] + 0.34 * x, MO[1] + 0.34 * y, MO[2] + 0.34 * z)) for x, y, z in keep])
        fn(f'p114/digc/k{j}', [f'execute unless block {rel(11 + x, 4 + y, 11 + z)} minecraft:{"calcite" if (x, y, z) in K else "air"} run return 0' for x, y, z in cube] + ['return 1'])
    fn('p114/digc/tick', dtick('c', 22.8, press('dreset', (2, 5, 9), 'bm:p114/digc/reset')) +
       [f'execute if score @s bm.gvc matches {j} if function bm:p114/digc/k{j} run return run function bm:p70/solved' for j in range(len(PD.MODELS))])
    fn('p114/digc/reset', [f'fill {rel(11, 4, 11)} {rel(13, 6, 13)} minecraft:calcite'] + oops(2) +
       ['scoreboard players set @s bm.gvf 1', 'playsound minecraft:block.stone.place block @a[distance=..20] ~ ~ ~ 1 0.8'])
    dispatch('dig', None, None)

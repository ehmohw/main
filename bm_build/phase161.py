"""2.80d: THE TROPHY STAND - every trophy you've earned, on show.

Madame Velour sells it (3 Trophies). Use it on the top of a block: a three-step stand of dark oak, red velvet and gold trim,
three blocks wide, turned to face you. Right-click it and it OPENS: the record of whoever clicked comes out onto it as models -
  the top step:    the seven dungeon bosses' trophies (the Broodmother ... the Golden Goose) you've earned;
  the middle step: the twelve heist rooms, each in the best metal you've won it in (copper ... netherite);
  the front step:  the five tier laurels and the Gutter Laurel.
A plaque above counts them (bosses n/7, rooms n/12, laurels n/6). Right-click again and it folds away; it folds by itself
when nobody's near. Sneak + punch it to pick it up. A boss trophy counts once you've carried it (or the victor's key), or
conquered its dungeon; a room trophy as the raid records it; a laurel by its advancement (the Gutter Laurel once carried).
"""
from items import item, T, TOTEM
from useitem import hold, HOLD
from nbt import snbt, B, F, Int
import phase81 as P81
from p2.config import D, ORDER

WOOD = '#c89a5a'
item('trophy_stand', TOTEM, 'Trophy Stand', WOOD,
     ['Three velvet steps for everything you\'ve won.', ('Use it on a block to set it down.', 'blue'),
      ('Right-click it: your trophies come out to be seen.', 'blue'), ('Bosses, heist rooms and laurels.', 'gray'),
      ('Sneak + punch it to pick it up.', 'gray')],
     model='bm:trophy_stand_icon', stack=1, cat='fun', comps=hold('none'))
HOLD['trophy_stand'] = 'bm:p161/place'

BOSSES = list(D)                                      # 7: brood .. hollow, lucky
ROOMS = P81.TK                                        # 12 rooms, metals 1..6
LAURELS = [f'laurel_t{t}' for t in range(1, 6)] + ['gutter_laurel']
IDN = [F(0), F(0), F(0), F(1)]
FLIP = [F(0), F(1), F(0), F(0)]                         # (2.83) half a turn: a display shows a model's back toward its facing
# (tier, x spacing, scale, height of the step's top, depth: + toward the viewer)
STEP = {'boss': (0.42, 0.40, 0.95, -0.40), 'room': (0.245, 0.24, 0.60, 0.0), 'laurel': (0.45, 0.34, 0.30, 0.40)}


def disp(model, scale, tags, flip=True):
    return snbt({'Tags': ['bm.tsd', 'bm.tsnew'] + tags, 'item_display': 'fixed', 'teleport_duration': Int(2),
                 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': model}},
                 'transformation': {'left_rotation': FLIP if flip else IDN, 'right_rotation': IDN, 'translation': [F(0), F(scale / 2), F(0)],
                                    'scale': [F(scale)] * 3}})


def generate(G):
    fn, title, give, tellraw, PREFIX = G.fn, G.title, G.give, G.tellraw, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    second, fast = [], []
    objs = ['bm.tsb dummy', 'bm.tsid dummy', 'bm.tso dummy']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o}' for o in objs]
    G.OBJECTIVES += [o.split()[0] for o in objs]
    has = '*[minecraft:custom_data~{bm:"%s"}]'

    # ---------------- the record: boss trophies (bits 0-6) and the Gutter Laurel (bit 7), kept once carried
    for i, d in enumerate(BOSSES):
        second.append(f'execute as @a[gamemode=!spectator] unless score @s bm.tsb matches -2147483648.. run scoreboard players set @s bm.tsb 0')
        break
    for i, d in enumerate(BOSSES):
        fn(f'p161/rec/b{i}', [f'scoreboard players operation #q bm.rng = @s bm.tsb', f'scoreboard players operation #q bm.rng /= #p{i} bm.rng',
                              'scoreboard players operation #q bm.rng %= #2 bm.rng',
                              f'execute if score #q bm.rng matches 0 run scoreboard players add @s bm.tsb {2 ** i}'])
        second += [f'execute as @a[gamemode=!spectator] if items entity @s container.* {has % f"trophy_{d}"} run function bm:p161/rec/b{i}']
    fn('p161/rec/b7', ['scoreboard players operation #q bm.rng = @s bm.tsb', 'scoreboard players operation #q bm.rng /= #p7 bm.rng',
                       'scoreboard players operation #q bm.rng %= #2 bm.rng', 'execute if score #q bm.rng matches 0 run scoreboard players add @s bm.tsb 128'])
    second.append(f'execute as @a[gamemode=!spectator] if items entity @s container.* {has % "gutter_laurel"} run function bm:p161/rec/b7')
    G.FUNCS['load'][-1:-1] = [f'scoreboard players set #p{i} bm.rng {2 ** i}' for i in range(12)]
    # (as the opener) also counted: a victor's key on you, or the dungeon conquered (the conquest record)
    backfill = []
    for i, d in enumerate(BOSSES):
        backfill.append(f'execute if items entity @s container.* {has % f"bkey_{d}"} run function bm:p161/rec/b{i}')
        if d in ORDER:
            backfill.append(f'execute if score @s bm.conq matches {max(ORDER.index(d), 1)}.. run function bm:p161/rec/b{i}')
    fn('p161/backfill', ['execute unless score @s bm.tsb matches -2147483648.. run scoreboard players set @s bm.tsb 0'] + backfill)

    # ---------------- setting it down (use on the top of a block, within 5 blocks)
    fn('p161/place', ['scoreboard players set #placed bm.rng 0', 'scoreboard players set #ray bm.rng 25', 'tag @s add bm.placer',
                      'execute anchored eyes positioned ^ ^ ^ run function bm:p161/ray', 'tag @s remove bm.placer',
                      'execute if score #placed bm.rng matches 0 run ' + say('Look at the top of a block within 5 blocks to set it down.')])
    fn('p161/ray', ['execute unless block ~ ~ ~ #minecraft:replaceable run return run function bm:p161/hit',
                    'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p161/ray'])
    fn('p161/hit', ['execute align xyz positioned ~0.5 ~1 ~0.5 unless block ~ ~ ~ #minecraft:replaceable run return 0',
                    'execute align xyz positioned ~0.5 ~1 ~0.5 if entity @e[type=minecraft:interaction,tag=bm.tstand,distance=..2.5] run return run '
                    + say('Too close to another Trophy Stand.'),
                    'execute align xyz positioned ~0.5 ~1 ~0.5 rotated as @a[tag=bm.placer,limit=1] rotated ~180 0 run function bm:p161/spawn'])
    stand = {'Tags': ['bm.tsd', 'bm.tsbase', 'bm.tsnew'], 'item_display': 'fixed',
             'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:trophy_stand'}},
             'transformation': {'left_rotation': FLIP, 'right_rotation': IDN, 'translation': [F(0), F(0.6), F(0)], 'scale': [F(3.0), F(1.2), F(1.2)]}}
    box = {'Tags': ['bm.tstand', 'bm.tsnew'], 'width': F(1.6), 'height': F(1.3), 'response': B(1)}
    fn('p161/spawn', ['scoreboard players add #tsid bm.rng 1',
                      f'summon minecraft:item_display ~ ~ ~ {snbt(stand)}', f'summon minecraft:interaction ~ ~ ~ {snbt(box)}',
                      'scoreboard players operation @e[tag=bm.tsnew,distance=..0.5] bm.tsid = #tsid bm.rng',
                      'scoreboard players set @e[type=minecraft:interaction,tag=bm.tsnew,distance=..0.5] bm.tso 0',
                      'tp @e[tag=bm.tsnew,distance=..0.5] ~ ~ ~ ~ 0', 'tag @e[tag=bm.tsnew,distance=..0.5] remove bm.tsnew',
                      'item modify entity @a[tag=bm.placer,limit=1] weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
                      'scoreboard players set #placed bm.rng 1',
                      'playsound minecraft:block.wood.place block @a[distance=..16] ~ ~ ~ 1 0.8', 'playsound minecraft:block.chain.place block @a[distance=..16] ~ ~ ~ 0.6 1.2',
                      'particle minecraft:wax_on ~ ~0.6 ~ 1.2 0.3 0.4 0 16'])

    # ---------------- right-click: open (the clicker's record) / fold away; sneak + punch: pick it up
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.tstand] if data entity @s interaction at @s run function bm:p161/click',
             'execute as @e[type=minecraft:interaction,tag=bm.tstand] if data entity @s attack at @s run function bm:p161/punch']
    fn('p161/click', ['tag @s add bm.tsme', 'execute on target run tag @s add bm.tsviewer', 'data remove entity @s interaction',
                      'execute store result score #was bm.rng run scoreboard players get @s bm.tso',
                      'execute if score #was bm.rng matches 1 run function bm:p161/close',
                      'execute unless score #was bm.rng matches 1 as @a[tag=bm.tsviewer,limit=1] at @s run function bm:p161/open',
                      'tag @a remove bm.tsviewer', 'tag @s remove bm.tsme'])
    fn('p161/punch', ['tag @s add bm.tsme', 'execute on attacker run tag @s add bm.tsviewer', 'data remove entity @s attack',
                      'execute as @a[tag=bm.tsviewer,limit=1] unless predicate bm:p20/sneaking run ' + say('Sneak + punch the stand to pick it up.'),
                      'execute if entity @a[tag=bm.tsviewer,limit=1,predicate=bm:p20/sneaking] run function bm:p161/pickup',
                      'tag @a remove bm.tsviewer', 'tag @s remove bm.tsme'])
    fn('p161/pickup', ['function bm:p161/close', 'scoreboard players operation #id bm.rng = @s bm.tsid',
                       'execute as @e[type=minecraft:item_display,tag=bm.tsbase,distance=..1] if score @s bm.tsid = #id bm.rng run kill @s',
                       'loot give @a[tag=bm.tsviewer,limit=1] loot bm:items/trophy_stand', 'particle minecraft:poof ~ ~0.6 ~ 1 0.3 0.4 0.02 12',
                       'playsound minecraft:block.wood.break block @a[distance=..16] ~ ~ ~ 1 0.9', 'kill @s'])
    # (as the stand's interaction, at it)
    fn('p161/close', ['scoreboard players operation #id bm.rng = @s bm.tsid',
                      'execute as @e[type=minecraft:item_display,tag=bm.tsshow,distance=..3] if score @s bm.tsid = #id bm.rng run kill @s',
                      'execute as @e[type=minecraft:text_display,tag=bm.tsshow,distance=..3] if score @s bm.tsid = #id bm.rng run kill @s',
                      'execute if score @s bm.tso matches 1 run playsound minecraft:block.chest.close block @a[distance=..12] ~ ~ ~ 0.7 1.2',
                      'scoreboard players set @s bm.tso 0'])
    second.append('execute as @e[type=minecraft:interaction,tag=bm.tstand,scores={bm.tso=1}] at @s unless entity @a[distance=..12,gamemode=!spectator] run function bm:p161/close')

    # (as the opener; the stand is @e[tag=bm.tsme]) count while laying out each model at its step
    op = ['function bm:p161/backfill', 'execute as @e[type=minecraft:interaction,tag=bm.tsme] run scoreboard players set @s bm.tso 1',
          'scoreboard players set #nb bm.rng 0', 'scoreboard players set #nr bm.rng 0', 'scoreboard players set #nl bm.rng 0']
    sp, sc, hy, dz = STEP['boss']
    for i, d in enumerate(BOSSES):
        x = (i - (len(BOSSES) - 1) / 2) * sp
        fn(f'p161/sh/b{i}', ['scoreboard players add #nb bm.rng 1',
                             f'execute at @e[type=minecraft:interaction,tag=bm.tsme] rotated as @e[type=minecraft:interaction,tag=bm.tsme] positioned ^{x:.3f} ^{hy} ^{dz} '
                             f'run summon minecraft:item_display ~ ~ ~ {disp(f"bm:trophy3d_{d}", sc, ["bm.tsshow"], flip=False)}'])   # (2.94: the boss figures face you - the half-turn is for the cups)
        op += [f'scoreboard players operation #q bm.rng = @s bm.tsb', f'scoreboard players operation #q bm.rng /= #p{i} bm.rng',
               'scoreboard players operation #q bm.rng %= #2 bm.rng', f'execute if score #q bm.rng matches 1 run function bm:p161/sh/b{i}']
    sp, sc, hy, dz = STEP['room']
    for j, k in enumerate(ROOMS):
        x = (j - (len(ROOMS) - 1) / 2) * sp
        cases = []
        for m in range(P81.NMET, 0, -1):          # the best metal it's been won in
            cases += [f'scoreboard players operation #q bm.rng = @s bm.tr{m}', f'scoreboard players operation #q bm.rng /= #p{j} bm.rng',
                      'scoreboard players operation #q bm.rng %= #2 bm.rng', f'execute if score #q bm.rng matches 1 run return run function bm:p161/sh/r{j}_{m}']
            fn(f'p161/sh/r{j}_{m}', ['scoreboard players add #nr bm.rng 1',
                                     f'execute at @e[type=minecraft:interaction,tag=bm.tsme] rotated as @e[type=minecraft:interaction,tag=bm.tsme] positioned ^{x:.3f} ^{hy} ^{dz} '
                                     f'run summon minecraft:item_display ~ ~ ~ {disp(f"bm:trophy3d_{k}_{m}", sc, ["bm.tsshow"])}'])
        fn(f'p161/sh/r{j}', cases)
        op.append(f'function bm:p161/sh/r{j}')
    sp, sc, hy, dz = STEP['laurel']
    for t, lid in enumerate(LAURELS):
        x = (t - (len(LAURELS) - 1) / 2) * sp
        fn(f'p161/sh/l{t}', ['scoreboard players add #nl bm.rng 1',
                             f'execute at @e[type=minecraft:interaction,tag=bm.tsme] rotated as @e[type=minecraft:interaction,tag=bm.tsme] positioned ^{x:.3f} ^{hy} ^{dz} '
                             f'run summon minecraft:item_display ~ ~ ~ {disp(f"bm:{lid}", sc, ["bm.tsshow"], flip=False)}'])
        if t < 5:
            op.append(f'execute if entity @s[advancements={{bm:story/raid_t{t + 1}=true}}] run function bm:p161/sh/l{t}')
        else:
            op += ['scoreboard players operation #q bm.rng = @s bm.tsb', 'scoreboard players operation #q bm.rng /= #p7 bm.rng',
                   'scoreboard players operation #q bm.rng %= #2 bm.rng', f'execute if score #q bm.rng matches 1 run function bm:p161/sh/l{t}']
    op += ['execute store result storage bm:p161 c.b int 1 run scoreboard players get #nb bm.rng',
           'execute store result storage bm:p161 c.r int 1 run scoreboard players get #nr bm.rng',
           'execute store result storage bm:p161 c.l int 1 run scoreboard players get #nl bm.rng',
           'execute at @e[type=minecraft:interaction,tag=bm.tsme] rotated as @e[type=minecraft:interaction,tag=bm.tsme] positioned ^ ^1.55 ^-0.45 run function bm:p161/plaque with storage bm:p161 c',
           # every new piece: the stand's id, turned to face the way it does, and a little flourish
           'execute as @e[type=minecraft:interaction,tag=bm.tsme] run scoreboard players operation #id bm.rng = @s bm.tsid',
           'execute at @e[type=minecraft:interaction,tag=bm.tsme] run scoreboard players operation @e[tag=bm.tsnew,distance=..3] bm.tsid = #id bm.rng',
           'execute at @e[type=minecraft:interaction,tag=bm.tsme] as @e[tag=bm.tsnew,distance=..3] at @s rotated as @e[type=minecraft:interaction,tag=bm.tsme] run tp @s ~ ~ ~ ~ 0',
           'execute at @e[type=minecraft:interaction,tag=bm.tsme] run tag @e[tag=bm.tsnew,distance=..3] remove bm.tsnew',
           'execute at @e[type=minecraft:interaction,tag=bm.tsme] run particle minecraft:wax_on ~ ~0.9 ~ 1.2 0.4 0.4 0 24',
           'execute at @e[type=minecraft:interaction,tag=bm.tsme] run playsound minecraft:block.chest.open block @a[distance=..12] ~ ~ ~ 0.7 1.1',
           'execute at @e[type=minecraft:interaction,tag=bm.tsme] run playsound minecraft:ui.toast.in block @a[distance=..12] ~ ~ ~ 1 1.2',
           say('Your trophies, on show. (Right-click again to fold them away.)', WOOD)]
    fn('p161/open', op)
    plaque = {'Tags': ['bm.tsd', 'bm.tsshow', 'bm.tsnew'], 'billboard': 'center', 'background': Int(0x90201008 - 2 ** 32), 'alignment': 'center',
              'line_width': Int(260), 'transformation': {'left_rotation': IDN, 'right_rotation': IDN, 'translation': [F(0), F(0), F(0)], 'scale': [F(0.6)] * 3}}
    plaque['text'] = {'text': '', 'extra': [T('\u2726 TROPHIES \u2726', 'gold', bold=True), T('\n'), T('Bosses $(b)/7', '#ff9a6a'),
                                            T('   Heist rooms $(r)/12', '#7ad8ff'), T('   Laurels $(l)/6', '#9aff7a')]}
    fn('p161/plaque', ['$summon minecraft:text_display ~ ~ ~ ' + snbt(plaque)])

    fn('admin/trophy_stand', [give('trophy_stand')])
    G.FUNCS['loop/second'][-1:-1] = second
    G.FUNCS['loop/fast'] += fast


def extend_offers(O, offer):
    O['outfitter'].append(offer(('trophy', 3), ('trophy_stand', 1)))


# ===================================================================== resource pack: the stand, and its icon
def rp(R):
    cube = R.cube
    tex = {'w': 'minecraft:block/dark_oak_planks', 'v': 'minecraft:block/red_wool', 'g': 'minecraft:block/gold_block',
           's': 'minecraft:block/stripped_dark_oak_log'}
    # front = north (z 0), three steps rising to the back; the item display stretches it to 3 x 1.2 x 1.2 blocks
    els = [cube((0, 0, 0), (16, 1.5, 16), 's')]
    for z0, z1, h in ((0, 15.2, 4.0), (5.33, 15.2, 8.0), (10.67, 15.2, 12.67)):      # (2.83: up to the back panel, not through it)
        els += [cube((0.2, 1.5, z0), (15.8, h - 0.5, z1), 'w'), cube((0.2, h - 0.5, z0), (15.8, h, z1), 'v'),
                cube((0.1, h - 0.9, z0 - 0.15), (15.9, h - 0.5, z0 + 0.25), 'g')]
    els += [cube((0, 1.5, 15.2), (16, 13.2, 16), 's'), cube((-0.1, 13.2, 14.9), (16.1, 13.6, 16.1), 'g')]
    R.HATS['trophy_stand'] = (tex, els)
    R.ICONS['trophy_stand_icon'] = R.grid(['................', '................', '.......Y........', '......YYY.......', '.......Y........',
                                           '..........rrrrr.', '...Y......rRRRr.', '..YYY.wwwwwwwww.', '...Y..wvvvvvvvw.', 'wwwwwwwyyyyyyyw.',
                                           'wvvvvvvvvvvvvvw.', 'wyyyyyyyyyyyyyw.', 'wdddddddddddddw.', 'wdddddddddddddw.', 'wwwwwwwwwwwwwww.',
                                           '................'],
                                          dict(Y='#ffd040', r='#6a4a20', R='#c08a3a', w='#3a2414', v='#b0202a', y='#e8b830', d='#5a3a20'))

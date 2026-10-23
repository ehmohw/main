"""2.93d: PEARLMAN'S SEASONS - his earth gem takes on the season of the land around him.

  FORMS       base (his own penguin colours: plains, meadows, anywhere neutral), Fall (the dappled and dark forests, the pale
              garden, the birch woods - the form he was drawn in), Christmas (snow and ice), Easter (flower forests, cherry
              groves, sunflower plains), Summer (deserts, beaches, savannas, badlands, jungles, warm seas). The models are
              phase60's (pearlman, pearlman_<form>).
  THE NPC     wears the season of the biome he lands in.
  FOLLOWER    each form is unlocked by walking him through one of its biomes. His card's Seasons page picks:
              Dynamic (the default - he changes as he walks), Off (his base colours, always - and his wardrobe colour, which
              the seasonal outfits replace), or any unlocked form, for good.
"""
from items import T
from nbt import snbt
import phase28 as P28

PEARL = '#7ad0e8'
MENU = 971
BASE = 3480                                  # (3480-3489: the Seasons page - 3480 Dynamic, 3481 Off, 3482-3485 a form each)
FORMS = [   # key, name, colour, biomes, where to find it (as told), the burst when he changes into it
    ('fall', 'Fall', '#d8803a', ['dappled_forest', 'dark_forest', 'pale_garden', 'birch_forest', 'old_growth_birch_forest'],
     'a dappled, dark or birch forest', 'minecraft:dust{color:[0.85,0.45,0.15],scale:1.2}'),
    ('xmas', 'Christmas', '#e0404a', ['snowy_plains', 'ice_spikes', 'snowy_taiga', 'snowy_slopes', 'frozen_peaks', 'jagged_peaks', 'grove',
                                      'snowy_beach', 'frozen_river', 'frozen_ocean', 'deep_frozen_ocean'],
     'somewhere snowy', 'minecraft:snowflake'),
    ('easter', 'Easter', '#f29cc0', ['flower_forest', 'cherry_grove', 'sunflower_plains'],
     'a flower forest, cherry grove or sunflower plain', 'minecraft:cherry_leaves'),
    ('summer', 'Summer', '#ffc040', ['desert', 'beach', 'savanna', 'savanna_plateau', 'windswept_savanna', 'badlands', 'eroded_badlands',
                                     'wooded_badlands', 'jungle', 'sparse_jungle', 'bamboo_jungle', 'warm_ocean', 'lukewarm_ocean', 'deep_lukewarm_ocean'],
     'a desert, beach, savanna, badlands or jungle', 'minecraft:dust{color:[1.0,0.85,0.3],scale:1.2}'),
]
FORM_KEYS = [f[0] for f in FORMS]


def generate(G):
    fn, wjson, tellraw = G.fn, G.wjson, G.tellraw
    objs = ['bm.pmsea', 'bm.pmf']               # (a player's choice: 0 dynamic, 1 off, 2.. a form; his cat's form now)
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    for k, _n, _c, biomes, *_r in FORMS:
        wjson(f'bm/tags/worldgen/biome/pm_{k}.json', {'values': [f'minecraft:{b}' for b in biomes]})
    pmsay = lambda txt, who='@s': tellraw(who, [T('Pearlman: ', PEARL, bold=True), T(txt, 'white')])

    # ---- #pf: the form the land here asks for (0 base, 1.. a form)
    fn('p209/here', ['scoreboard players set #pf bm.rng 0'] +
       [f'execute if biome ~ ~ ~ #bm:pm_{k} run return run scoreboard players set #pf bm.rng {i}' for i, k in enumerate(FORM_KEYS, 1)])
    # ---- the NPC: the season he lands in (as his new display, at him)
    spawn = G.FUNCS['p60/pm/spawn']
    at = next(i for i, l in enumerate(spawn) if l == 'tag @e[tag=bm.pnew,distance=..1] remove bm.pnew')
    spawn.insert(at, 'execute as @e[type=minecraft:item_display,tag=bm.pnew,distance=..1] at @s run function bm:p209/npc')
    fn('p209/npc', ['function bm:p209/here'] +
       [f'execute if score #pf bm.rng matches {i} run data modify entity @s item.components."minecraft:item_model" set value "bm:pearlman_{k}"'
        for i, k in enumerate(FORM_KEYS, 1)])

    # ---- the follower (as his cat, at it): the form his owner's choice gives
    fn('p209/form', ['scoreboard players set #pmm bm.rng 0', 'execute on owner run scoreboard players operation #pmm bm.rng = @s bm.pmsea',
                     'execute if score #pmm bm.rng matches 1 run return run scoreboard players set #pf bm.rng 0',
                     'execute if score #pmm bm.rng matches 2.. run return run function bm:p209/fixed',
                     'function bm:p209/here'])
    # (the fixed choices are stored one higher than the form: 2 is Fall's 1)
    fn('p209/fixed', ['scoreboard players operation #pf bm.rng = #pmm bm.rng', 'scoreboard players remove #pf bm.rng 1'])
    # his model dressed for it: the base form takes his wardrobe colour (phase138's "_c<k>"); a season's outfit is its own
    fn('p209/look', ['function bm:p209/form', 'scoreboard players operation @s bm.pmf = #pf bm.rng', 'function bm:p138/k/pearl',
                     'scoreboard players operation #me bm.pid = @s bm.pid',
                     'execute as @e[type=minecraft:item_display,tag=bm.pmd] if score @s bm.pid = #me bm.pid run function bm:p209/set'])
    fn('p209/set', ['execute if score #pf bm.rng matches 0 run data modify entity @s item.components."minecraft:item_model" set value "bm:pearlman"',
                    'execute if score #pf bm.rng matches 0 run return run function bm:p138/sfx'] +
       [f'execute if score #pf bm.rng matches {i} run data modify entity @s item.components."minecraft:item_model" set value "bm:pearlman_{k}"'
        for i, k in enumerate(FORM_KEYS, 1)])
    # (a change of season: his look, and a little burst of it)
    fn('p209/change', ['function bm:p209/look', 'particle minecraft:end_rod ~ ~0.7 ~ 0.3 0.4 0.3 0.02 6',
                       'execute if score #pf bm.rng matches 0 run particle minecraft:snowflake ~ ~0.7 ~ 0.4 0.5 0.4 0.02 14'] +
       [f'execute if score #pf bm.rng matches {i} run particle {p} ~ ~0.7 ~ 0.4 0.5 0.4 0.02 18' for i, (*_x, p) in enumerate(FORMS, 1)] +
       ['playsound minecraft:block.amethyst_block.chime neutral @a[distance=..12] ~ ~ ~ 0.8 1.3'])
    # every second: a season unlocked where he walks with you; his look follows the choice (and, dynamic, the land)
    G.FUNCS['p128/pm/sec'].append('function bm:p209/sec')
    fn('p209/sec', [f'execute if biome ~ ~ ~ #bm:pm_{k} on owner if entity @s[tag=!bm.pmu_{k},distance=..16] run function bm:p209/u/{k}' for k in FORM_KEYS] +
       ['function bm:p209/form', 'execute unless score #pf bm.rng = @s bm.pmf run function bm:p209/change'])
    for k, nm, col, _b, _where, _p in FORMS:
        fn(f'p209/u/{k}', [f'tag @s add bm.pmu_{k}', 'playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 1.2',
                           tellraw('@s', [T('Pearlman\'s earth gem hums: ', PEARL), T(f'his {nm} look', col, bold=True), T(' is yours to keep. ', PEARL),
                                          T('(His card - sneak + use - then Seasons.)', 'gray')])])
    # ...and on the spot whenever his model is put on him (summoned, re-made, or his wardrobe changed)
    G.FUNCS['p128/pm/summon_here'].append('execute as @e[type=minecraft:cat,tag=bm.pmpet] if score @s bm.pid = #me bm.pid at @s run function bm:p209/look')
    G.FUNCS['p128/pm/tick'].append('execute if score #ok bm.rng matches 0 run function bm:p209/look')
    G.FUNCS['p138/pearl/now2'].append('function bm:p209/look')

    # ---- the Seasons page (from his card, 8303): one card per set of forms unlocked, so the locked ones say so
    def page(mask):
        btn = [P28.btn(T('Dynamic', '#9ae8a0', bold=True), BASE, width=150, tooltip=T('He changes with the land he walks.', 'gray')),
               P28.btn(T('Off - his own colours', 'white'), BASE + 1, width=150, tooltip=T('Always his base penguin colours (and his wardrobe colour).', 'gray'))]
        for i, (k, nm, col, _b, where, _p) in enumerate(FORMS):
            if mask >> i & 1:
                btn.append(P28.btn(T(nm, col, bold=True), BASE + 2 + i, width=150, tooltip=T(f'{nm}, always.', 'gray')))
            else:
                btn.append(P28.btn(T(f'{nm} (locked)', 'dark_gray'), BASE + 2 + i, width=150, tooltip=T(f'Walk him through {where}.', 'gray')))
        dlg = P28.multi([T("Pearlman's Seasons", PEARL, bold=True)],
                        [P28.body([T('His earth gem takes on the season of the land: ', 'white'),
                                   T('Fall', '#d8803a', bold=True), T(' in dappled and dark forests, ', 'gray'), T('Christmas', '#e0404a', bold=True),
                                   T(' in the snow, ', 'gray'), T('Easter', '#f29cc0', bold=True), T(' among the flowers, ', 'gray'), T('Summer', '#ffc040', bold=True),
                                   T(' in the heat. Walk him through one to keep its look.', 'gray')], 300)],
                        btn, columns=2, exit_label='Back')
        return f'dialog show @s {snbt(dlg)}'
    fn('p209/menu', [f'scoreboard players set @s bm.menu {MENU}', 'scoreboard players set #mask bm.rng 0'] +
       [f'execute if entity @s[tag=bm.pmu_{k}] run scoreboard players add #mask bm.rng {1 << i}' for i, k in enumerate(FORM_KEYS)] +
       [f'execute if score #mask bm.rng matches {m} run return run {page(m)}' for m in range(1 << len(FORMS))])
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {BASE}..{BASE + 1 + len(FORMS)} run return run function bm:p209/act')
    fn('p209/act', [f'execute unless score @s bm.menu matches {MENU} run return run function bm:p28/stale',
                    f'execute if score #act bm.pay matches {BASE} run function bm:p209/pick/dynamic',
                    f'execute if score #act bm.pay matches {BASE + 1} run function bm:p209/pick/off'] +
                   [f'execute if score #act bm.pay matches {BASE + 2 + i} run function bm:p209/pick/{k}' for i, k in enumerate(FORM_KEYS)] +
                   # (his look now, if he's out)
                   ['scoreboard players operation #me bm.pid = @s bm.pid',
                    'execute as @e[type=minecraft:cat,tag=bm.pmpet] if score @s bm.pid = #me bm.pid at @s run function bm:p209/change'])
    fn('p209/pick/dynamic', ['scoreboard players set @s bm.pmsea 0', pmsay('"Dynamic it is! Pearlman dresses for the weather. A salesman must."')])
    fn('p209/pick/off', ['scoreboard players set @s bm.pmsea 1', pmsay('"Back to basics. The classic black and white never goes out of style."')])
    LINES = {'fall': '"Autumn! Pumpkins, bats, and the crunch of leaves underfoot. My season."',
             'xmas': '"Ho ho - ahem. Season\'s greetings, and season\'s discounts!"',
             'easter': '"Spring has sprung! Mind the eggs - they\'re for display only."',
             'summer': '"Sunglasses on. Pearlman is officially on holiday. Mostly."'}
    for i, (k, nm, *_r) in enumerate(FORMS):
        fn(f'p209/pick/{k}', [f'execute unless entity @s[tag=bm.pmu_{k}] run return run function bm:p209/locked/{k}',
                              f'scoreboard players set @s bm.pmsea {i + 2}', pmsay(LINES[k])])
        fn(f'p209/locked/{k}', [pmsay(f'"My {nm} look? We\'d have to go somewhere for that first - {FORMS[i][4]}."'), 'function bm:p209/menu'])
    # (admin: every season unlocked)
    fn('admin/pearlman_seasons', [f'tag @s add bm.pmu_{k}' for k in FORM_KEYS] + [tellraw('@s', [T('Every one of Pearlman\'s seasons unlocked.', PEARL)])])

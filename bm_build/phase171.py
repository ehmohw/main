"""2.82b: THE TOWN DIRECTORY - finding your way round the rat town.

The 2.81 town is big: a dozen traders and as many places, over two levels and both banks of a river. TOWN DIRECTORY boards
stand where people arrive and gather - on the Lookout by the vault door, in Fountain Plaza, on the Wharf, in Furnace Row and in
Night Alley. Right-click one: WHO'S WHERE, every trader and place by district. Pick one and a trail of light leads you from
wherever you are to it (its name on your action bar, and how near you are) until you get there - or for two minutes. Pick
another, or the same again, any time. (The Captain keeps his own counsel: he isn't listed.)

The boards are spawned at run time from the market's bm.mkt marker (mgeo), so they turn with the town and come to markets
already in worlds; each guide's target is a walkable spot by its trader or place, checked against the built town."""
from items import T
from nbt import snbt, B, F, Int
import mgeo
import market3 as M3

W, BF = M3.W, M3.BF
MENU = 2400                                     # bm.menu while the directory is open; its buttons are 2401..2400+len(PLACES)
GOLD, TRAIL = '#ffcf40', '#7ad0ff'
GUIDE_S = 120                                   # seconds a guide lasts
ARRIVE = 4.5                                    # blocks from the spot: you're there

# (label, where, template spot by it) - grouped by district; the spot is snapped to the nearest walkable cell
PLACES = [
    ('Old Barnaby', 'pawn shop, Pawn Alley', (29.5, W, 20.5)),
    ('Prof. Whiskerton', 'the Stacks, over Barnaby\'s', (30.5, BF + 1, 19.5)),
    ('Madame Velour', 'outfitters, Pawn Alley', (30.5, W, 29.5)),
    ('The Fence', 'his terrace, Pawn Alley', (46.5, W, 18.5)),
    ('Dark Auction gate', 'top of Pawn Alley', (39.5, W, 16.5)),
    ('Gilded Gutter gate', 'off the Fence\'s terrace (Gold Key)', (48.5, BF + 1, 16.5)),
    ('Scrap Bin', 'by Barnaby\'s shop front', (33.5, W, 24.5)),
    ('Bounty Board', 'Fountain Plaza', (34.5, W, 38.5)),
    ("Mike's pond", 'Fountain Plaza', (38.5, W, 40.5)),
    ("Vinny 'Two-Blades'", 'gunsmith, Furnace Row', (56.5, W, 24.5)),
    ('Steelwhisker', 'armory, Furnace Row', (67.5, W, 30.5)),
    ("Fishy's Cabinet", 'Curio Court, off Furnace Row', (55.5, W, 13.5)),
    ('Chef Fromage', 'the Gnawed Flagon', (68.5, W, 45.5)),
    ('Cecil', 'his tent, Night Alley', (52.5, W, 70.5)),
    ('The Bloodbroker', 'the Blood Alcove, Night Alley', (63.5, W, 74.5)),
    ('Lucky Whiskers', 'the riverboat casino, the Wharf', (12.5, W, 72.5)),
    ('The dock house', 'Salty Sal, the Wharf', (9.5, W, 26.5)),
    ('Dennis', 'Assay Office, under the Lookout', (34.5, W, 78.5)),
    ('Pistachio', 'Pantry, under the Lookout', (42.5, W, 78.5)),
    ("Newcomers' Book", 'the lectern on the Lookout', (34.5, BF + 1, 78.5)),
    ('The way out', 'the vault door, the Lookout', (38.5, BF + 1, 80.5)),
]
BOARDS = [((31.5, BF + 1, 79.5), 'the Lookout'), ((31.5, W, 46.5), 'Fountain Plaza'), ((8.5, W, 37.5), 'the Wharf'),
          ((60.5, W, 36.5), 'Furnace Row'), ((60.5, W, 63.5), 'Night Alley')]


def _snap(p):
    """The walkable cell nearest a place's spot (its floor in the public town, or the Gutter for the Gutter's gate)."""
    cells = mgeo.reach('public')
    x0, y0, z0 = int(p[0] // 1), int(round(p[1])), int(p[2] // 1)
    best = min(cells, key=lambda c: (c[0] - x0) ** 2 + 4 * (c[1] - y0) ** 2 + (c[2] - z0) ** 2)
    d2 = (best[0] - x0) ** 2 + (best[1] - y0) ** 2 + (best[2] - z0) ** 2
    assert d2 <= 25, f'town directory: nothing walkable near {p} (nearest {best})'
    return (best[0] + 0.5, best[1], best[2] + 0.5)


def generate(G):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    import phase28 as P28
    fast, second = G.FUNCS['loop/fast'], G.FUNCS['loop/second']
    P = [T('[', 'dark_gray'), T('Town Directory', GOLD, bold=True), T('] ', 'dark_gray')]
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.dirt dummy', 'scoreboard objectives add bm.dirs dummy']
    G.OBJECTIVES += ['bm.dirt', 'bm.dirs']
    spots = [_snap(p) for _l, _w, p in PLACES]
    mk = '@e[type=minecraft:marker,tag=bm.mkt,distance=..140,sort=nearest,limit=1]'

    # ---- the boards (installed once per town, like Dennis's rooms; a rebuilt town has a fresh marker and gets them again)
    build = ['kill @e[tag=bm.dirprop,distance=..120]']
    for (bx, by, bz), where in BOARDS:
        mgeo.need_air((int(bx), int(by), int(bz)), f'the town directory board ({where})')
        mgeo.need_air((int(bx), int(by) + 1, int(bz)), f'the town directory board ({where})')
        txt = snbt({'Tags': ['bm.dirprop'], 'billboard': 'vertical', 'see_through': B(1), 'view_range': F(0.6), 'background': Int(0x90000000 - (1 << 32)),
                    'text': [T('TOWN DIRECTORY\n', GOLD, bold=True), T("who's where - ", 'gray'), T('right-click', 'white')],
                    'transformation': {'left_rotation': [F(0)] * 3 + [F(1)], 'right_rotation': [F(0)] * 3 + [F(1)], 'translation': [F(0)] * 3, 'scale': [F(0.55)] * 3}})
        icon = snbt({'Tags': ['bm.dirprop'], 'billboard': 'vertical', 'item': {'id': 'minecraft:filled_map', 'count': Int(1)}, 'item_display': 'fixed',
                     'brightness': {'block': Int(15), 'sky': Int(15)},
                     'transformation': {'left_rotation': [F(0)] * 3 + [F(1)], 'right_rotation': [F(0)] * 3 + [F(1)], 'translation': [F(0)] * 3, 'scale': [F(0.8)] * 3}})
        hit = snbt({'Tags': ['bm.dirprop', 'bm.dirb'], 'width': F(0.9), 'height': F(1.9), 'response': B(1)})
        at = f'execute positioned {mgeo.rel((bx, by, bz))} run '
        build += [at + f'summon minecraft:interaction ~ ~ ~ {hit}', at + f'summon minecraft:item_display ~ ~1.1 ~ {icon}',
                  at + f'summon minecraft:text_display ~ ~1.8 ~ {txt}']
    fn('p171/install', ['tag @s add bm.dir282'] + build)
    corners = [(1, W - 1, 1), (74, W - 1, 1), (1, W - 1, 84), (74, W - 1, 84)]
    loaded = ' '.join(f'if loaded {mgeo.rel(c)}' for c in corners)
    second.append(f'execute as @e[type=minecraft:marker,tag=bm.mkt,tag=!bm.dir282] at @s rotated as @s {loaded} run function bm:p171/install')
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[tag=bm.dirprop]', 'kill @e[type=minecraft:marker,tag=bm.dirm]']

    # ---- right-clicked: WHO'S WHERE
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.dirb] if data entity @s interaction at @s run function bm:p171/click',
             'execute as @e[type=minecraft:interaction,tag=bm.dirb] if data entity @s attack run data remove entity @s attack']
    fn('p171/click', ['execute on target run function bm:p171/open', 'data remove entity @s interaction'])
    btns = [P28.btn([T(lbl, 'white')], MENU + 1 + i, tooltip=T(where, 'gray'), width=150) for i, (lbl, where, _p) in enumerate(PLACES)]
    dlg = P28.multi([T("WHO'S WHERE", GOLD, bold=True), T('  ·  the rat town', 'gray')],
                    [P28.body([T('Pick a trader or a place: a trail of light leads you there.', 'gray')], 300)],
                    btns, columns=2)
    fn('p171/open', [f'scoreboard players set @s bm.menu {MENU}', 'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 1.1',
                     f'dialog show @s {P28.inline(dlg)}'])
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {MENU + 1}..{MENU + len(PLACES)} run return run function bm:p171/act')
    fn('p171/act', [f'execute unless score @s bm.menu matches {MENU} run return run function bm:p28/stale',
                    'scoreboard players operation @s bm.dirt = #act bm.pay', f'scoreboard players remove @s bm.dirt {MENU}',
                    'function bm:p171/go'])

    # ---- the guide: a marker at the spot (one per player, by bm.pid), a trail toward it, the name on the action bar
    fn('p171/go', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                   'execute as @e[type=minecraft:marker,tag=bm.dirm] if score @s bm.pid = #me bm.pid run kill @s',
                   f'execute unless entity {mk} run return run scoreboard players set @s bm.dirt 0',
                   f'scoreboard players set @s bm.dirs {GUIDE_S}'] +
       [f'execute if score @s bm.dirt matches {i + 1} at {mk} rotated as {mk} positioned {mgeo.rel(sp)} run summon minecraft:marker ~ ~ ~ {{Tags:["bm.dirm","bm.dirnew"]}}'
        for i, sp in enumerate(spots)] +
       ['scoreboard players operation @e[type=minecraft:marker,tag=bm.dirnew] bm.pid = #me bm.pid', 'tag @e[type=minecraft:marker,tag=bm.dirnew] remove bm.dirnew',
        'playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1.4', 'function bm:p171/bar'])
    fast.append('execute as @a[scores={bm.dirt=1..}] at @s run function bm:p171/tick')
    fn('p171/tick', ['scoreboard players operation #me bm.pid = @s bm.pid',
                     'execute as @e[type=minecraft:marker,tag=bm.dirm] if score @s bm.pid = #me bm.pid run tag @s add bm.dirsel',
                     'execute unless entity @e[type=minecraft:marker,tag=bm.dirsel,distance=..160] run return run function bm:p171/stop',
                     f'execute if entity @e[type=minecraft:marker,tag=bm.dirsel,distance=..{ARRIVE}] run return run function bm:p171/arrive'] +
       [f'execute facing entity @e[type=minecraft:marker,tag=bm.dirsel,limit=1] feet run particle minecraft:dust{{color:[0.48,0.82,1.0],scale:1.1}} ^ ^0.35 ^{d} 0.02 0.02 0.02 0 1'
        for d in (1.2, 1.9, 2.6, 3.3, 4.0)] +
       ['execute at @e[type=minecraft:marker,tag=bm.dirsel] run particle minecraft:end_rod ~ ~1.6 ~ 0.1 0.4 0.1 0.01 2',
        'function bm:p171/bar', 'tag @e[type=minecraft:marker,tag=bm.dirsel] remove bm.dirsel'])
    near = lambda r: f'entity @e[type=minecraft:marker,tag=bm.dirsel,distance=..{r}]'
    fn('p171/bar', [f'execute if score @s bm.dirt matches {i + 1} run return run function bm:p171/bar/{i + 1}' for i in range(len(PLACES))])
    for i, (lbl, where, _p) in enumerate(PLACES):
        msg = lambda how, col: title('@s', 'actionbar', [T('→ ', TRAIL, bold=True), T(lbl, 'white', bold=True), T(f'  ({where})  ', 'gray'), T(how, col)])
        fn(f'p171/bar/{i + 1}', [f'execute if {near(12)} run return run ' + msg('just ahead', '#7aff7a'),
                                 f'execute if {near(30)} run return run ' + msg('close by', '#ffe07a'),
                                 msg('follow the light', TRAIL)])
    fn('p171/arrive', ['playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.8 1.2',
                       title('@s', 'actionbar', [T('You\'re there. ', '#7aff7a', bold=True), T('(Any directory board: somewhere else.)', 'gray')]),
                       'function bm:p171/stop'])
    fn('p171/stop', ['scoreboard players set @s bm.dirt 0', 'scoreboard players set @s bm.dirs 0', 'scoreboard players operation #me bm.pid = @s bm.pid',
                     'execute as @e[type=minecraft:marker,tag=bm.dirm] if score @s bm.pid = #me bm.pid run kill @s'])
    second += ['scoreboard players remove @a[scores={bm.dirs=1..}] bm.dirs 1',
               'execute as @a[scores={bm.dirt=1..,bm.dirs=..0}] run function bm:p171/timeout']
    fn('p171/timeout', [title('@s', 'actionbar', T('The trail fades. (A directory board will light another.)', 'gray')), 'function bm:p171/stop'])
    # (a guide marker left behind by a player who logged off mid-way, or a trail that outlived its player)
    second.append('execute as @e[type=minecraft:marker,tag=bm.dirm] run function bm:p171/orphan')
    fn('p171/orphan', ['scoreboard players operation #o bm.pid = @s bm.pid', 'scoreboard players set #f bm.rng 0',
                       'execute as @a[scores={bm.dirt=1..}] if score @s bm.pid = #o bm.pid run scoreboard players set #f bm.rng 1',
                       'execute if score #f bm.rng matches 0 run kill @s'])
    G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/directory', 'yellow'), T('  put the Town Directory boards up again in every loaded market', 'gray')]))
    fn('admin/directory', ['tag @e[type=minecraft:marker,tag=bm.mkt] remove bm.dir282', tellraw('@s', P + [T('The boards go up again in every loaded market.', 'gray')])])

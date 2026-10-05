"""Phase 1.8: item re-sync (old copies of Black Market items are updated to the current definition, so trade-ins
always match), the market's living details (Mike the Spikefish, drips and fireflies), new skin art and rat-themed
Medallion/Trophy icons. Importing does nothing; generate(G) runs after phase17.generate."""
from nbt import snbt, B, F, Int
from items import T, ITEMS, ITEM_VERSION, TOTEM

SLOTS = [(f'container.{i}', f'Inventory[{{Slot:{i}b}}]') for i in range(36)] + \
        [('armor.head', 'equipment.head'), ('armor.chest', 'equipment.chest'), ('armor.legs', 'equipment.legs'),
         ('armor.feet', 'equipment.feet'), ('weapon.offhand', 'equipment.offhand')]


def generate(G):
    fn, wjson, title, tellraw, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.PREFIX
    second, fast = [], []

    # ---------------- re-sync: any Black Market item without this version's stamp gets the current definition
    from items import DYNAMIC
    for iid in ITEMS:
        comps = dict(G.exact_comps(iid))
        if ITEMS[iid]['base'] == TOTEM: comps['!minecraft:death_protection'] = {}
        if iid in DYNAMIC:      # 1.18: keep what the item carries (a bottled creature, charges, uses); just restamp the version
            for k in ('minecraft:custom_data', 'minecraft:item_model', 'minecraft:lore', 'minecraft:enchantment_glint_override'): comps.pop(k, None)
            wjson(f'bm/item_modifier/refresh/{iid}.json', [{'function': 'minecraft:set_components', 'components': comps},
                                                           {'function': 'minecraft:set_custom_data', 'tag': f'{{bmv:{ITEM_VERSION}}}'}])
            continue
        wjson(f'bm/item_modifier/refresh/{iid}.json', {'function': 'minecraft:set_components', 'components': comps})
    old = f'*[minecraft:custom_data,!minecraft:custom_data~{{bmv:{ITEM_VERSION}}}]'
    fn('p18/refresh/scan', [f'execute if items entity @s {slot} {old} run function bm:p18/refresh/slot {{path:"{path}",slot:"{slot}"}}'
                            for slot, path in SLOTS])
    fn('p18/refresh/slot', ['data remove storage bm:tmp rf',
                            '$data modify storage bm:tmp rf.iid set from entity @s $(path).components."minecraft:custom_data".bm',
                            '$data modify storage bm:tmp rf.slot set value "$(slot)"',
                            'execute if data storage bm:tmp rf.iid run function bm:p18/refresh/apply with storage bm:tmp rf'])
    fn('p18/refresh/apply', ['$item modify entity @s $(slot) bm:refresh/$(iid)'])
    second += [f'execute as @a if items entity @s container.* {old} run function bm:p18/refresh/scan',
               f'execute as @a unless items entity @s container.* {old} if items entity @s armor.* {old} run function bm:p18/refresh/scan',
               f'execute as @a unless items entity @s container.* {old} if items entity @s weapon.offhand {old} run function bm:p18/refresh/scan']

    # ---------------- Mike the Spikefish (persistent, invulnerable; his name shows when you look at him)
    mike = {'Tags': ['bm.npc', 'bm.mike'], 'CustomName': T('Mike the Spikefish', 'yellow', bold=True), 'CustomNameVisible': B(0),
            'PersistenceRequired': B(1), 'Invulnerable': B(1), 'FromBucket': B(1), 'PuffState': Int(0)}
    fn('npc/mike', [f'summon minecraft:pufferfish ~ ~ ~ {snbt(mike)}'])
    G.FUNCS['npc/spawn'][0:0] = ['execute if entity @s[tag=bm.npc.mike] run function bm:npc/mike']
    # if Mike ever wanders off (or somebody fishes him out with a bucket), he comes home
    second.append('execute as @e[type=minecraft:pufferfish,tag=bm.mike] at @s unless block ~ ~ ~ minecraft:water run tp @s @e[type=minecraft:marker,tag=bm.mfx2,distance=..64,sort=nearest,limit=1]')
    fn('p18/market_fx', ['particle minecraft:dripping_water ~ ~1.5 ~ 9 0 9 0 3',
                         'particle minecraft:firefly ~ ~-7 ~ 9 3 9 0 2',
                         'particle minecraft:white_ash ~ ~-6 ~ 12 5 12 0 6'])
    fn('p18/fountain_fx', ['particle minecraft:splash ~ ~ ~ 1 0.2 1 0.05 8', 'particle minecraft:falling_water ~ ~-1 ~ 1.1 0.5 1.1 0 3'])
    fast.append('execute as @e[type=minecraft:marker,tag=bm.mfx] at @s if entity @a[distance=..30] run function bm:p18/market_fx')
    fast.append('execute as @e[type=minecraft:marker,tag=bm.mfx2] at @s if entity @a[distance=..24] run function bm:p18/fountain_fx')

    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


# ===================================================================== ICONS
def icons(grid):
    I = {}
    I['medallion'] = grid([          # a silver medal on a purple ribbon, a rat's face struck into it
        '...RR......RR...', '...RRr....rRR...', '....RRr..rRR....', '.....RRrrRR.....', '.....SSSSSS.....',
        '...SSVVVVVVSS...', '..SVPPVVVVPPVS..', '..SVPWWWWWWPVS..', '.SVVWWKWWKWWVVS.', '.SVVWWWWWWWWVVS.',
        '.SVVVWWPPWWVVVS.', '..SVVVWWWWVVVS..', '..SVVVVWWVVVVS..', '...SSVVVVVVSS...', '.....SSSSSS.....', '................'],
        dict(R='#7b2fbe', r='#4e1a80', S='#c9c9dc', V='#6a2fa8', W='#e8e8f0', P='#e88aa0', K='#0d0d0d'))
    I['trophy'] = grid([             # a golden cup with rat ears, a rat face on the bowl and a tail off the plinth
        '..PP........PP..', '.PYYP......PYYP.', '.YYYYYYYYYYYYYY.', 'Y.YWYYYYYYYYYO.Y', 'Y.YWYKYYYYKYYO.Y',
        '.YYWYYYPPYYYYOY.', '...YYYYYYYYYO...', '....YYYYYYYO....', '.....OYYYYO.....', '......YYYY......',
        '.......YY.......', '.......YO.......', '.....OOOOOO.....', '....DDDDDDDD....', '....DDDDDDDDPP..', '..............P.'],
        dict(Y='#f2c230', W='#fff6c0', O='#a77d10', D='#4a2f1a', P='#e88aa0', K='#3a2a00'))
    I['bag_of_rocks'] = grid([
        '................', '.....gGgG.......', '....GgGGgG......', '.....KSSK.......', '....BBSSBB......', '...BBBBBBBB.....',
        '..BBbBBBBbBB....', '..BBBBBBBBBB....', '.BBBBbBBBBBBB...', '.BBBBBBBBBbBB...', '.BBbBBBBBBBBB...', '.BBBBBBBbBBBB...',
        '..BBBBBBBBBB....', '...BBBBBBBB.....', '................', '................'],
        dict(g='#9a9a9a', G='#6e6e6e', K='#3b2a1a', S='#d8c8a0', B='#a07a48', b='#80603a'))
    I['rpg_launcher'] = grid([
        '............RRR.', '...........RRRRR', '..........GRRRR.', '.........GGGRR..', '........GGGGG...', '.......GGgGG....',
        '......GGgGG.....', '.....GGKGG......', '....GGGKK.......', '...GGGG.K.......', '..GGgG..........', '.DDGG...........',
        'DDDD............', '.DD.............', '................', '................'],
        dict(R='#c0392b', G='#556b2f', g='#6b8e3a', K='#2b2b2b', D='#3a3a3a'))
    I['butter_sock'] = grid([
        '....WWWW........', '....BBBB........', '....WWWW........', '....WWWW........', '....BBBB........', '....WWWW........',
        '....WWWW........', '....WWWWy.......', '....WWWyYy......', '...WWWyYYYy.....', '..WWWyYYYYYy....', '..WWWyYYYYYy....',
        '..WWWWyYYYy.....', '...WWWWWWW......', '................', '................'],
        dict(W='#f2f2f2', B='#3b6fd6', Y='#ffe066', y='#e0b840'))
    I['pool_noodle'] = grid([
        '.............PP.', '............PPPP', '...........PpPP.', '..........PPPP..', '.........PPpP...', '........PPPP....',
        '.......PpPP.....', '......PPPP......', '.....PPpP.......', '....PPPP........', '...PpPP.........', '..PPPP..........',
        '.PPpP...........', 'PPPP............', '.PP.............', '................'],
        dict(P='#ff3fa4', p='#c4207a'))
    I['rubber_duck'] = grid([
        '................', '................', '.......YYYY.....', '......YYYYYY....', '......YYKYYYOO..', '......YYYYYYOO..',
        '.......YYYYY....', '..Y....YYYY.....', '..YYYYYYYYYYYY..', '..YYYYYYYYYYYYY.', '..YYYYYYYYYYYYY.', '...YYYYYYYYYYY..',
        '....yyyyyyyyy...', '................', '................', '................'],
        dict(Y='#ffd93b', y='#e0b020', K='#1a1a1a', O='#ff8c1a'))
    return I


HANDHELD = {'rpg_launcher', 'pool_noodle', 'butter_sock', 'bag_of_rocks', 'rubber_duck'}

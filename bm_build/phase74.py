"""2.63: a friendlier Black Market - half prices, an easier way in and out, underground ruins, Emma's Mining form.

PRICES: every Black Market good costs half what it did (Tokens, Medallions, Trophies, Blood Crystals, Lucky Tokens; tier
  upgrades too). The Fence buys a Diamond for 2 Tokens. Heist Plans: 3 Tokens. Pearlman's gems: 1 Medallion each. The
  currency exchanges keep their rates, and nothing can be bought and sold back for a profit.
EARNING: Tokens are a rare catch when fishing, Medallions a very rare one; every heist won pays at least a Token a head
  (more, and now and then a Medallion, the higher the tier).
THE WAY IN: the shaft's ladders reach the top at last (the last three were missing); a pool at the bottom so you can just
  jump; and a LIFT button by the vault door (inside, on the right) that puts you back on the surface beside the shaft.
  Markets already in a world get all of it the next time someone comes by.
THE NEWCOMERS' BOOK: a short who-sells-what, not an inventory.
FOLLOWERS: welcome in the market and the Overworld's dungeons (not in the vault, nor the Hollow Throne).
EMMA: a fifth buff, MINING - Haste II (III with harmony or in her Ethereal Form), in amber and ochre.
UNDERGROUND RUINS (Overworld, Nether and End): small crumbling rooms, shrines and halls with a loot chest - ores, tools,
  Tokens, now and then a Heartstone or a Black Market accessory. Heartstones turn up three times as often in chests.
ALSO: the Minish Cap moved to Madame Velour (with her Mini and Mega Mushrooms); the Wings of the Golden Rat are built on a
  real elytra; the Grimoire Key has its own colours; the Portable Trash Can's icon fits its slot."""
import random
from items import T, ITEMS
from nbt import snbt, B, F, D, Int
import rot
import phase17
import phase60

phase60.GEM_PRICE = ('medallion', 1)
import phase62, economy
economy.DIRECT['shift_core'] = (('trophy', 6), ('blood_crystal', 12))    # (2.65: 70% of 8 + 16, like everything else)
for _k in phase17.HEART_CHANCE: phase17.HEART_CHANCE[_k] *= 3

GOLD = '#ffcf40'
H = '#6a2a8a'
DIRECTORY = [   # who, where, what (in a phrase)
    ('The Fence', 'Pawn Alley', 'money changing (Diamonds, Tokens, Medallions, Trophies), maps, keys, Heist Plans, mail'),
    ('Old Barnaby', 'Pawn Alley', 'buys your Black Market goods back; odd gadgets, the Scrap Bin'),
    ('Madame Velour', 'the Plaza', 'boots, wings, hats, power-ups and gadgets'),
    ('Cecil the Wizard', 'the purple tent', 'magic staffs, bows and charms - and Cecil himself'),
    ('Prof. Whiskerton', 'the Stacks', 'books, maps, weapon skins and tinkering machines'),
    ("Vinny 'Two-Blades'", 'the Forge Pit', 'weapons and tools, and the Shifting arms'),
    ('Sgt. Steelwhisker', 'the Forge Pit', 'armour sets and their upgrades'),
    ('Chef Fromage', 'the Gnawed Flagon', 'feasts that buff you'),
    ('The Bloodbroker', 'the Blood Alcove', 'Blood Moon goods, for Blood Crystals'),
    ('Salty Sal', 'the Docks', 'sea and fishing gear, weather vials'),
    ('Lucky Whiskers', 'the Lucky Den', 'scratch cards and lucky charms'),
    ('Capt. Cheddarbeard', 'behind a very small door', 'pirate treasures'),
    ('Zorp', 'aboard a Donadian mothership', 'alien tech, for Xenite'),
]
SHAFT = None          # (filled in generate)
RUIN_PAL = {
    'stone': dict(wall=['stone_bricks', 'stone_bricks', 'mossy_stone_bricks', 'cracked_stone_bricks', 'cobblestone', 'mossy_cobblestone'],
                  floor=['stone_bricks', 'cobblestone', 'mossy_stone_bricks', 'gravel'], trim='chiseled_stone_bricks', pillar='stone_bricks',
                  stair='stone_brick_stairs', slab='stone_brick_slab', light='lantern[hanging=false,waterlogged=false]'),
    'deep': dict(wall=['deepslate_bricks', 'cracked_deepslate_bricks', 'deepslate_tiles', 'cobbled_deepslate', 'polished_deepslate'],
                 floor=['deepslate_tiles', 'cobbled_deepslate', 'deepslate_bricks'], trim='chiseled_deepslate', pillar='polished_deepslate',
                 stair='deepslate_brick_stairs', slab='deepslate_brick_slab', light='soul_lantern[hanging=false,waterlogged=false]'),
    'nether': dict(wall=['polished_blackstone_bricks', 'cracked_polished_blackstone_bricks', 'blackstone', 'nether_bricks', 'gilded_blackstone'],
                   floor=['polished_blackstone', 'blackstone', 'nether_bricks'], trim='chiseled_polished_blackstone', pillar='polished_basalt[axis=y]',
                   stair='polished_blackstone_brick_stairs', slab='polished_blackstone_brick_slab', light='soul_lantern[hanging=false,waterlogged=false]'),
    'end': dict(wall=['end_stone_bricks', 'end_stone_bricks', 'purpur_block', 'end_stone'], floor=['end_stone_bricks', 'purpur_block'],
                trim='purpur_pillar[axis=y]', pillar='purpur_pillar[axis=y]', stair='purpur_stairs', slab='purpur_slab',
                light='end_rod[facing=up]'),
}
RUINS = {'overworld': ['stone', 'deep'], 'nether': ['nether'], 'end': ['end']}


def extend_offers(O, offer):
    O['outfitter'].append(offer(('token', 6), ('minish_cap', 1)))       # 2.63: with the other size-changers (was at the Lucky Den)


def guide_pages(O, zorp):
    """2.63: the newcomers' book - a short who-sells-what"""
    pages = [[T('NEWCOMERS,\nSTART HERE\n\n', H, bold=True), T('Welcome to the Black Market.\n\nWe trade in ', 'black'), T('Tokens', H), T(', ', 'black'),
              T('Medallions', H), T(' and ', 'black'), T('Trophies', H), T(' (9 Tokens = 1 Medallion, 6 Medallions = 1 Trophy).', 'black')],
             [T('EARNING\n\n', H, bold=True), T('- monsters (more on special nights)\n- bosses and dungeons\n- heists in the Gilded Gutter\n'
                                                  '- fishing (if you\'re lucky)\n- bounties on the board by this book\n- Diamonds: the Fence pays 2 Tokens each', 'black')]]
    for i in range(0, len(DIRECTORY), 3):
        pg = [T('WHO SELLS WHAT\n\n' if i == 0 else '', H, bold=True)]
        for who, where, what in DIRECTORY[i:i + 3]:
            pg += [T(who, 'black', bold=True), T(f' ({where})\n', 'dark_gray'), T(f'{what}\n\n', 'black')]
        pages.append(pg)
    pages.append([T('BEHIND THE NORTH WALL\n\n', H, bold=True), T('The Dark Auction and the Gilded Gutter open as your ', 'black'), T('Standing', H),
                  T(' grows - spend, and the market notices.\n\nLeaving? The ', 'black'), T('LIFT', H, bold=True),
                  T(' button by the vault door takes you up.\n\n- The Management', 'black')])
    return pages


import phase50
phase50.guide_pages = guide_pages


def build_ruin(kind, pal, seed):
    import structures as S
    r = random.Random(seed); P = RUIN_PAL[pal]
    w = lambda: r.choice(P['wall'])
    if kind == 'room': sx, sy, sz = 9, 6, 9
    elif kind == 'shrine': sx, sy, sz = 7, 6, 7
    else: sx, sy, sz = 13, 5, 7
    Bd = S.Build(sx, sy, sz)
    for x in range(sx):
        for z in range(sz):
            Bd.set(x, 0, z, r.choice(P['floor']))
            edge = x in (0, sx - 1) or z in (0, sz - 1)
            for y in range(1, sy - 1):
                if edge:
                    if r.random() < 0.7: Bd.set(x, y, z, w())          # (the rest crumbled away: the rock shows through)
                else:
                    Bd.set(x, y, z, 'air')
            if r.random() < 0.55: Bd.set(x, sy - 1, z, w())             # a broken ceiling
    # pillars, rubble, cobwebs, a light, a skull
    for (x, z) in ((1, 1), (sx - 2, 1), (1, sz - 2), (sx - 2, sz - 2)):
        h = r.randint(1, sy - 2)
        for y in range(1, h + 1): Bd.set(x, y, z, P['pillar'])
        if h < sy - 2 and r.random() < 0.5: Bd.set(x, h + 1, z, P['slab'] + '[type=bottom,waterlogged=false]')
    for _ in range(sx * sz // 10):
        x, z = r.randint(2, sx - 3), r.randint(2, sz - 3)
        if r.random() < 0.5: Bd.set(x, 1, z, r.choice([w(), P['slab'] + '[type=bottom,waterlogged=false]', P['stair'] + '[facing=north,half=bottom,shape=straight,waterlogged=false]']))
        else: Bd.set(x, sy - 2, z, 'cobweb')
    cx, cz = sx // 2, sz - 2
    if kind == 'shrine':
        Bd.set(cx, 1, cz, P['trim']); Bd.set(cx - 1, 1, cz, P['stair'] + '[facing=east,half=bottom,shape=straight,waterlogged=false]')
        Bd.set(cx + 1, 1, cz, P['stair'] + '[facing=west,half=bottom,shape=straight,waterlogged=false]')
        Bd.set(cx, 2, cz, 'chest[facing=north,type=single,waterlogged=false]', {'id': 'minecraft:chest', 'LootTable': 'bm:ruins/' + ('nether' if pal == 'nether' else 'end' if pal == 'end' else 'overworld')})
        Bd.set(cx - 1, 2, cz, 'candle[candles=3,lit=false,waterlogged=false]'); Bd.set(cx + 1, 2, cz, 'skeleton_skull[powered=false,rotation=8]')
    else:
        Bd.set(cx, 1, cz, 'chest[facing=north,type=single,waterlogged=false]', {'id': 'minecraft:chest', 'LootTable': 'bm:ruins/' + ('nether' if pal == 'nether' else 'end' if pal == 'end' else 'overworld')})
        Bd.set(cx + 1, 1, cz, P['light'])
        if kind == 'hall':
            Bd.set(2, 1, cz, 'barrel[facing=up,open=false]', {'id': 'minecraft:barrel', 'LootTable': 'bm:ruins/' + ('nether' if pal == 'nether' else 'end' if pal == 'end' else 'overworld')})
            for x in range(3, sx - 3, 3):                                # arches along the hall
                Bd.set(x, sy - 2, 1, P['stair'] + '[facing=south,half=top,shape=straight,waterlogged=false]')
                Bd.set(x, sy - 2, sz - 2, P['stair'] + '[facing=north,half=top,shape=straight,waterlogged=false]')
    return Bd


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    tick, fast, second = [], [], []
    import mgeo, market2
    rel = mgeo.rel
    BF, SZ = market2.BF, market2.SZ
    SHAFT_POS = (38.5, BF + 1, SZ + 1.5)
    back = {0: 'north', 1: 'east', 2: 'south', 3: 'west'}

    # ================================================================== THE WAY IN AND OUT
    # new shafts: a pool at the bottom, ladders to the very top
    pit = ['execute rotated as @s run fill ^-2 ^-1 ^-2 ^2 ^-1 ^2 minecraft:cobbled_deepslate', 'execute rotated as @s run fill ^-1 ^-2 ^-1 ^1 ^-2 ^1 minecraft:cobbled_deepslate',
           'execute rotated as @s run fill ^-1 ^-1 ^-1 ^1 ^-1 ^1 minecraft:water']
    G.FUNCS['p41/shaft/start'] += pit
    for n in range(4):
        lv = G.FUNCS[f'p41/shaft/lv_{n}']
        lv[:] = [l.replace('run function bm:p41/shaft/top', f'run function bm:p74/shaft/top_{n}') for l in lv]
        fn(f'p74/shaft/top_{n}', ['function bm:p41/shaft/top', 'fill ^-1 ^ ^2 ^1 ^ ^2 minecraft:cobbled_deepslate replace #minecraft:replaceable'] +
           [f'setblock ^{dx} ^ ^1 minecraft:ladder[facing={back[n]},waterlogged=false]' for dx in (-1, 0, 1)])
        # (shafts already dug: climb to where the ladders stop, and finish them)
        fn(f'p74/shaft/climb_{n}', [f'execute if block ^ ^ ^1 minecraft:ladder positioned ~ ~1 ~ run return run function bm:p74/shaft/climb_{n}',
                                    'execute unless block ^ ^ ^ #minecraft:air run return 0',
                                    'fill ^-1 ^ ^2 ^1 ^ ^2 minecraft:cobbled_deepslate replace #minecraft:replaceable'] +
           [f'setblock ^{dx} ^ ^1 minecraft:ladder[facing={back[n]},waterlogged=false]' for dx in (-1, 0, 1)])
    second.append('execute as @e[type=minecraft:marker,tag=bm.mshaft,tag=bm.msdone,tag=!bm.ms74] at @s if entity @a[distance=..96] if loaded ~3 ~ ~3 if loaded ~-3 ~ ~-3 '
                  'run function bm:p74/shaft/fix')
    fn('p74/shaft/fix', ['tag @s add bm.ms74'] + pit + [f'execute if entity @s[y_rotation={r}] rotated as @s run function bm:p74/shaft/climb_{n}' for r, n in rot.TURNS])
    # the lift: a button by the vault door (inside, right-hand wall), a sign above it
    LB, LS = (43, BF + 1, 86), (43, BF + 2, 86)
    sign = {'front_text': {'has_glowing_text': B(1), 'color': 'yellow', 'messages': [{'text': 'LIFT'}, {'text': 'press the button'}, {'text': 'to go up to'}, {'text': 'the surface'}]},
            'back_text': {'has_glowing_text': B(0), 'color': 'black', 'messages': [{'text': ''}] * 4}, 'is_waxed': B(1)}
    for n in range(4):
        fn(f'p74/lift_build_{n}', [f'execute positioned {rel((LB[0] + 0.5, LB[1] + 0.5, LB[2] + 0.5))} run setblock ~ ~ ~ '
                                   f'{rot.rotate("minecraft:polished_blackstone_button[face=wall,facing=west,powered=false]", n)}',
                                   f'execute positioned {rel((LS[0] + 0.5, LS[1] + 0.5, LS[2] + 0.5))} run setblock ~ ~ ~ '
                                   f'{rot.rotate("minecraft:dark_oak_wall_sign[facing=west,waterlogged=false]", n)}{snbt(sign)}'])
    corners = ' '.join(f'if loaded {rel(c)}' for c in ((LB[0] + 0.5, LB[1], LB[2] + 0.5), SHAFT_POS))
    second.append(f'execute as @e[type=minecraft:marker,tag=bm.mkt,tag=!bm.p74l] at @s rotated as @s if entity @a[distance=..64] {corners} run function bm:p74/lift_build')
    fn('p74/lift_build', ['tag @s add bm.p74l'] + [f'execute if entity @s[y_rotation={r}] run function bm:p74/lift_build_{n}' for r, n in rot.TURNS])
    LBR = rel((LB[0] + 0.5, LB[1] + 0.5, LB[2] + 0.5))
    fast.append(f'execute as @e[type=minecraft:marker,tag=bm.mkt,tag=bm.p74l] at @s rotated as @s if entity @a[distance=..72] '
                f'if block {LBR} #minecraft:buttons[powered=true] run function bm:p74/lift')
    # (as the market marker, at it, turned with it)
    fn('p74/lift', [f'execute positioned {LBR} run tag @a[distance=..3,gamemode=!spectator] add bm.lifter', 'execute unless entity @a[tag=bm.lifter] run return 0',
                    f'execute positioned {rel(SHAFT_POS)} as @e[type=minecraft:marker,tag=bm.mshaft,tag=bm.msdone,distance=..3,limit=1] at @s rotated as @s positioned ^ ^ ^-3 '
                    'positioned over motion_blocking_no_leaves run function bm:p74/lift_up',
                    'execute as @a[tag=bm.lifter] run ' + say('The lift isn\'t rigged yet - give it a moment.'), 'tag @a remove bm.lifter'])
    fn('p74/lift_up', ['execute as @a[tag=bm.lifter] at @s run particle minecraft:cloud ~ ~0.5 ~ 0.3 0.3 0.3 0.02 10',
                       'tp @a[tag=bm.lifter] ~ ~ ~', 'effect give @a[tag=bm.lifter] minecraft:slow_falling 2 0 true',
                       'execute as @a[tag=bm.lifter] at @s run playsound minecraft:block.chain.place player @s ~ ~ ~ 1 0.8',
                       'execute as @a[tag=bm.lifter] at @s run ' + title('@s', 'actionbar', T('Up you go.', GOLD)), 'tag @a remove bm.lifter'])
    # (the newcomers' book: markets already in a world get the short one once)
    second.append('execute as @e[type=minecraft:marker,tag=bm.mkt,tag=bm.p50,tag=!bm.p74b] at @s rotated as @s if entity @a[distance=..64] run function bm:p74/book')
    fn('p74/book', ['tag @s add bm.p74b', 'function bm:p50/book'])

    # ================================================================== FOLLOWERS: welcome everywhere but the vault and the Hollow Throne
    fn('p74/fol_ok', ['execute if dimension bm:gutter run return 0', 'execute if dimension bm:hollow_throne run return 0', 'return 1'])
    for f in ('p46/pet/try_summon', 'p57/try_summon', 'p66/try_summon', 'p72/zb/try_summon', 'p72/esk/use', 'p68/spawn'):
        L = G.FUNCS[f]
        assert any('function bm:p37/allowed' in l for l in L), f
        L[:] = [l.replace('function bm:p37/allowed', 'function bm:p74/fol_ok') for l in L]

    # ================================================================== EARNING: fishing, heists
    G.FUNCS['p39/fish'] += ['execute if score #r bm.rng matches 70..99 run function bm:p74/fish_token',
                            'execute if score #r bm.rng matches 100..104 run function bm:p74/fish_medal']
    fn('p74/fish_token', [give('token'), say('...and a Black Market Token came up on the line!', GOLD), 'playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 1 1.4'])
    fn('p74/fish_medal', [give('medallion'), say('...a MEDALLION, tangled in the line!', GOLD), 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.6 1.6'])
    # (2.67) the heist's cash is coins now - Tokens and Medallions come only from the Fixer's capped prize (phase75 p75/prize)
    for t in range(1, 6):
        wjson(f'bm/loot_table/gv/cash_t{t}.json', {'pools': [
            {'rolls': 1, 'entries': [G.loot_entry('gutter_coin', G.uni(1 + t, 2 + 2 * t))]}]})
    G.FUNCS['p70/haul'] += [f'execute if score #gt bm.rng matches {t} run loot give @s loot bm:gv/cash_t{t}' for t in range(1, 6)]     # (packed into The Haul below)

    # ================================================================== DISPLAY CASES: floor cases placed before 2.64 sank a block into the floor - lift them out
    second.append('execute as @e[type=minecraft:interaction,tag=bm.dchit,tag=!bm.dc64] at @s run function bm:p74/dc_lift')
    fn('p74/dc_lift', ['tag @s add bm.dc64', 'execute unless data entity @s {width:0.85f} run return 0',
                       'execute if block ~ ~ ~ #minecraft:replaceable run return 0',
                       'execute unless block ~ ~1 ~ #minecraft:replaceable run return 0',
                       'execute as @e[tag=bm.dcmob,distance=..0.8] run ride @s dismount',
                       'execute as @e[type=#bm:auto30,distance=..0.1] at @s run tp @s ~ ~1 ~',
                       'execute as @e[type=minecraft:block_display,tag=bm.dcseat,distance=..0.8] at @s run tp @s ~ ~1 ~',
                       'execute as @e[tag=bm.dcmob,distance=..0.8] at @s run tp @s ~ ~1 ~',
                       'execute positioned ~ ~1 ~ as @e[tag=bm.dcmob,distance=..1.2] run ride @s mount @e[type=minecraft:block_display,tag=bm.dcseat,distance=..1.2,sort=nearest,limit=1]'])

    # ================================================================== THE VAULT: buttons you can't miss - pale oak on the dark stone, a glowing label over
    #      each, and each room sets its own again as it readies, so a button is always there and always seen
    import phase70_rooms as RM
    def vbutton(x, y, z, facing, label):
        back = {'west': (1, 0), 'east': (-1, 0), 'north': (0, 1), 'south': (0, -1)}[facing]
        lbl = snbt({'Tags': ['bm.gvprop'], 'billboard': 'center', 'brightness': {'block': 15, 'sky': 15}, 'background': Int(0x90000000 - 2 ** 32),
                    'text': T(label, GOLD, bold=True), 'transformation': {'left_rotation': [F(0)] * 3 + [F(1)], 'right_rotation': [F(0)] * 3 + [F(1)],
                                                                          'translation': [F(0)] * 3, 'scale': [F(0.55)] * 3}})
        return [f'setblock {RM.rel(x, y, z)} minecraft:pale_oak_button[face=wall,facing={facing},powered=false]',
                f'summon minecraft:text_display {RM.rel(x, y + 0.7, z)} {lbl}']
    G.FUNCS['p70/r/lobby/init'] += vbutton(23, 5, 15, 'west', 'BEGIN') + vbutton(23, 5, 9, 'west', 'BEGIN')
    G.FUNCS['p70/r/levers/init'] += vbutton(12, 7, 23, 'north', 'TRY THE LEVERS')
    G.FUNCS['p70/r/tiles/init'] += vbutton(1, 5, 9, 'east', 'PEEK')

    # ================================================================== THE VAULT: re-planning a party's unfinished heist brings the party too (not just the leader)
    pl = G.FUNCS['p70/plans']
    k = pl.index('execute if score #j bm.rng matches 0.. run return run function bm:p70/join')
    pl[k] = 'execute if score #j bm.rng matches 0.. run return run function bm:p74/join_party'
    fn('p74/join_party', ['function bm:p70/join',
                          'execute as @a[distance=..24,gamemode=!spectator,tag=!bm.gvp,tag=!bm.gvwait] unless dimension bm:gutter if score @s bm.pty = #asker bm.pty at @s run function bm:p70/join'])
    # the heist's mobs keep their own counsel: Mimics drop nothing in the vault (no reward for a wrong pick)
    for i in range(4):                       # (all four coffers - the fourth's Mimic used to drop its overworld loot)
        f = G.FUNCS[f'p70/r/coffers/mimic{i}']
        k = next(j for j, l in enumerate(f) if 'tag @e[type=minecraft:rabbit,tag=bm.mnew' in l)
        f.insert(k + 1, 'execute as @e[type=minecraft:rabbit,tag=bm.mnew,distance=..3] run data merge entity @s {DeathLootTable:"minecraft:empty"}')
        f.insert(k + 2, 'tag @e[type=minecraft:rabbit,tag=bm.mnew,distance=..3] add bm.gvmimic')

    # ================================================================== THE VAULT: adventure mode inside (no breaking the vault's walls); survival again on the way out
    second.append('execute as @a[tag=bm.gvp,gamemode=survival] at @s if dimension bm:gutter run function bm:p74/vault_adv')
    fn('p74/vault_adv', ['tag @s add bm.gvadv', 'gamemode adventure @s'])
    for s_ in range(70):
        if f'p70/s{s_}/enter' not in G.FUNCS: break
        G.FUNCS[f'p70/s{s_}/enter'].append('execute if entity @s[gamemode=survival] run function bm:p74/vault_adv')
        G.FUNCS[f'p70/s{s_}/join'].append('execute if entity @s[gamemode=survival] run function bm:p74/vault_adv')
    G.FUNCS['p70/unraid'][0:0] = ['execute if entity @s[tag=bm.gvadv,gamemode=adventure] run gamemode survival @s', 'tag @s remove bm.gvadv']
    # (and anyone found in adventure with the tag outside the vault - a crash, a logout across a cleanup - gets survival back)
    second.append('execute as @a[tag=bm.gvadv,tag=!bm.gvp,tag=!bm.gvdead] at @s unless dimension bm:gutter run function bm:p74/vault_unadv')
    fn('p74/vault_unadv', ['execute if entity @s[gamemode=adventure] run gamemode survival @s', 'tag @s remove bm.gvadv'])

    # ================================================================== THE VAULT: THE HAUL - prizes come packed in one crate, not poured into your pockets
    #  every prize of a payout lands in a staging barrel (two, if it overflows); then it's handed over as a single barrel item,
    #  "The Haul": set it down anywhere and open it. (The Bond Sigil still comes loose - it's yours to keep on you.)
    HA, HB = '-200 64 -197', '-198 64 -197'          # (the coat check's chunk, kept loaded)
    def ins(table):
        return (f'execute in bm:gutter unless data block {HA} Items[26] run loot insert {HA} loot {table}', f'execute in bm:gutter if data block {HA} Items[26] run loot insert {HB} loot {table}')
    def redirect(fname):
        out = []
        for l in G.FUNCS[fname]:
            m = l.find('loot give @s loot ')
            if m < 0: out.append(l); continue
            pre, table = l[:m], l[m + len('loot give @s loot '):]
            a_, b_ = ins(table)
            if pre:                                                   # 'execute <conditions> run ' + 'execute <...>' -> one execute
                assert pre.startswith('execute ') and pre.endswith(' run '), l
                out += [pre[:-len('run ')] + a_[len('execute '):], pre[:-len('run ')] + b_[len('execute '):]]
            else:
                out += [a_, b_]
        G.FUNCS[fname][:] = out
    for f_ in ('p70/haul', 'p70/haul_roll', 'p70/first_clear', 'p70/core'):
        redirect(f_)
    G.FUNCS['p70/haul'][0:0] = [f'execute in bm:gutter run setblock {HA} minecraft:barrel', f'execute in bm:gutter run setblock {HB} minecraft:barrel',
                                f'execute in bm:gutter run data modify block {HA} Items set value []', f'execute in bm:gutter run data modify block {HB} Items set value []']
    G.FUNCS['p70/haul'].append('function bm:p74/haul_pack')
    crate = {'id': 'minecraft:barrel', 'count': Int(1), 'components': {
        'minecraft:custom_name': T('The Haul', GOLD, bold=True), 'minecraft:custom_data': {'bm_haul': B(1)}, 'minecraft:enchantment_glint_override': True,
        'minecraft:lore': [T('Everything you took from the vault.', 'gray'), T('Set it down and open it.', 'blue'),
                           T('Walk away and it folds up - into your pack if', 'gray'), T('anything is left in it.', 'gray')]}}
    fn('p74/haul_pack', ['scoreboard players set #hn bm.rng 0',
                         f'execute in bm:gutter if data block {HA} Items[0] run function bm:p74/haul_crate {{src:"{HA}"}}',
                         f'execute in bm:gutter if data block {HB} Items[0] run function bm:p74/haul_crate {{src:"{HB}"}}',
                         'execute if score #hn bm.rng matches 1.. run ' + tellraw('@s', PREFIX + [T('The Fixer hands you ', 'gray'), T('The Haul', GOLD, bold=True),
                                                                                                  T(' - set it down and open it.', 'gray')])])
    # (Items -> the barrel item's container: each {Slot, id, count, components} becomes {slot, item:{id, count, components}})
    fn('p74/haul_crate', ['scoreboard players add #hn bm.rng 1', '$data modify storage bm:tmp haul.in set from block $(src) Items', 'data modify storage bm:tmp haul.out set value []',
                          'function bm:p74/haul_conv', '$data modify block $(src) Items set value []',
                          f'execute at @s run summon minecraft:item ~ ~0.3 ~ {snbt({"Item": crate, "PickupDelay": Int(0), "Tags": ["bm.hauln"]})}',
                          'execute at @s run data modify entity @e[type=minecraft:item,tag=bm.hauln,distance=..2,limit=1] Item.components."minecraft:container" set from storage bm:tmp haul.out',
                          'execute at @s run data modify entity @e[type=minecraft:item,tag=bm.hauln,distance=..2,limit=1] Owner set from entity @s UUID',
                          'execute at @s run tag @e[type=minecraft:item,tag=bm.hauln,distance=..2] remove bm.hauln'])
    fn('p74/haul_conv', ['execute unless data storage bm:tmp haul.in[0] run return 0',
                         'data modify storage bm:tmp haul.e set value {}', 'execute store result storage bm:tmp haul.e.slot int 1 run data get storage bm:tmp haul.in[0].Slot',
                         'data modify storage bm:tmp haul.e.item set from storage bm:tmp haul.in[0]', 'data remove storage bm:tmp haul.e.item.Slot',
                         'data modify storage bm:tmp haul.out append from storage bm:tmp haul.e', 'data remove storage bm:tmp haul.in[0]', 'function bm:p74/haul_conv'])

    # (2.67) a Haul set down is a portable crate, like the trash can: walk away and it goes - emptied, it simply vanishes; with
    #  things still in it, it folds back into your pack as The Haul. Broken by hand, what's inside spills out, but the barrel
    #  itself never lands in your pockets. (Found by sight: the placing advancement looks along your view for it.)
    G.OBJECTIVES += ['bm.haulc']
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.haulc dummy']
    wjson('bm/advancement/p74/haul_placed.json', {'criteria': {'p': {'trigger': 'minecraft:placed_block', 'conditions': {'location': [
        {'condition': 'minecraft:match_tool', 'predicate': {'items': 'minecraft:barrel', 'predicates': {'minecraft:custom_data': '{bm_haul:1b}'}}}]}}},
        'rewards': {'function': 'bm:p74/haul/placed'}})
    fn('p74/haul/placed', ['advancement revoke @s only bm:p74/haul_placed', 'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                           'scoreboard players operation #hp bm.rng = @s bm.pid', 'scoreboard players set #hk bm.rng 0',
                           'execute anchored eyes positioned ^ ^ ^ run function bm:p74/haul/ray'])
    fn('p74/haul/ray', ['scoreboard players add #hk bm.rng 1', 'execute if score #hk bm.rng matches 30.. run return 0',
                        'execute if block ~ ~ ~ minecraft:barrel if data block ~ ~ ~ components."minecraft:custom_data".bm_haul align xyz positioned ~0.5 ~0.5 ~0.5 '
                        'unless entity @e[type=minecraft:marker,tag=bm.haulm,distance=..0.5] run return run function bm:p74/haul/mark',
                        'execute positioned ^ ^ ^0.25 run function bm:p74/haul/ray'])
    fn('p74/haul/mark', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.haulm","bm.hnewm"]}',
                         'scoreboard players operation @e[type=minecraft:marker,tag=bm.hnewm,distance=..0.5] bm.pid = #hp bm.rng',
                         'scoreboard players set @e[type=minecraft:marker,tag=bm.hnewm,distance=..0.5] bm.haulc 0',
                         'tag @e[type=minecraft:marker,tag=bm.hnewm] remove bm.hnewm', 'playsound minecraft:block.barrel.open block @a[distance=..16] ~ ~ ~ 0.6 1.2'])
    # (every tick: broken by hand - the barrel's own drop is caught before it can be picked up)
    tick.append('execute as @e[type=minecraft:marker,tag=bm.haulm] at @s unless block ~ ~ ~ minecraft:barrel run function bm:p74/haul/broke')
    fn('p74/haul/broke', ['kill @e[type=minecraft:item,distance=..1.5,nbt={Item:{id:"minecraft:barrel",components:{"minecraft:custom_name":{text:"The Haul"}}}}]',
                          'particle minecraft:poof ~ ~ ~ 0.3 0.3 0.3 0.02 8', 'kill @s'])
    # (every second: you've walked away - more than 7 blocks - and are still about: it goes)
    second.append('execute as @e[type=minecraft:marker,tag=bm.haulm] at @s run function bm:p74/haul/check')
    fn('p74/haul/check', ['scoreboard players operation #hp bm.rng = @s bm.pid', 'scoreboard players set #near bm.rng 0', 'scoreboard players set #on bm.rng 0',
                          'execute as @a if score @s bm.pid = #hp bm.rng run scoreboard players set #on bm.rng 1',
                          'execute as @a[distance=..7] if score @s bm.pid = #hp bm.rng run scoreboard players set #near bm.rng 1',
                          'execute if score #on bm.rng matches 0 run return 0', 'execute if score #near bm.rng matches 1 run return run scoreboard players set @s bm.haulc 0',
                          'scoreboard players add @s bm.haulc 1', 'execute if score @s bm.haulc matches 2.. run function bm:p74/haul/fold'])
    fn('p74/haul/fold', ['data modify storage bm:tmp haul.in set from block ~ ~ ~ Items', 'data modify storage bm:tmp haul.out set value []', 'function bm:p74/haul_conv',
                         'data modify block ~ ~ ~ Items set value []', 'setblock ~ ~ ~ minecraft:air',
                         'particle minecraft:poof ~ ~ ~ 0.3 0.3 0.3 0.02 10', 'playsound minecraft:block.barrel.close block @a[distance=..16] ~ ~ ~ 0.8 0.8',
                         'execute if data storage bm:tmp haul.out[0] as @a if score @s bm.pid = #hp bm.rng at @s run function bm:p74/haul/back', 'kill @s'])
    fn('p74/haul/back', [f'summon minecraft:item ~ ~0.3 ~ {snbt({"Item": crate, "PickupDelay": Int(0), "Tags": ["bm.hauln"]})}',
                         'data modify entity @e[type=minecraft:item,tag=bm.hauln,distance=..2,limit=1] Item.components."minecraft:container" set from storage bm:tmp haul.out',
                         'data modify entity @e[type=minecraft:item,tag=bm.hauln,distance=..2,limit=1] Owner set from entity @s UUID',
                         'tag @e[type=minecraft:item,tag=bm.hauln,distance=..2] remove bm.hauln',
                         title('@s', 'actionbar', [T('The Haul', GOLD, bold=True), T(' folds up and goes back in your pack - what\'s left is still in it.', 'gray')])])
    # (and an emptied Haul never sits in your inventory)
    second.append('clear @a minecraft:barrel[minecraft:custom_data~{bm_haul:1b},minecraft:container=[]]')
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[type=minecraft:marker,tag=bm.haulm]')

    # ================================================================== THE VAULT: the den heals (regeneration and a full belly before you go in)
    second.append('execute as @e[type=minecraft:marker,tag=bm.gvr_lobby] at @s positioned ~-12 ~-1 ~-12 if entity @a[tag=bm.gvp,dx=24,dy=8,dz=24] run function bm:p74/den_rest')
    fn('p74/den_rest', ['effect give @a[tag=bm.gvp,dx=24,dy=8,dz=24] minecraft:regeneration 3 1 true',
                        'effect give @a[tag=bm.gvp,dx=24,dy=8,dz=24] minecraft:saturation 2 0 true'])

    # ================================================================== UNDERGROUND RUINS
    loot_common = [('minecraft:iron_ingot', 20, (1, 4)), ('minecraft:gold_ingot', 14, (1, 3)), ('minecraft:redstone', 12, (2, 6)),
                   ('minecraft:lapis_lazuli', 10, (2, 6)), ('minecraft:emerald', 6, (1, 2)), ('minecraft:diamond', 3, (1, 1)),
                   ('minecraft:bread', 10, (2, 4)), ('minecraft:torch', 8, (4, 8)), ('minecraft:golden_apple', 3, (1, 1)), ('minecraft:name_tag', 2, (1, 1))]
    extra = {'overworld': [('minecraft:arrow', 8, (4, 10)), ('minecraft:copper_ingot', 10, (3, 8)), ('minecraft:amethyst_shard', 6, (2, 5))],
             'nether': [('minecraft:quartz', 12, (3, 8)), ('minecraft:gold_nugget', 12, (6, 16)), ('minecraft:blaze_rod', 5, (1, 2)),
                        ('minecraft:magma_cream', 5, (1, 3)), ('minecraft:ancient_debris', 2, (1, 1))],
             'end': [('minecraft:ender_pearl', 10, (1, 3)), ('minecraft:chorus_fruit', 8, (2, 5)), ('minecraft:shulker_shell', 3, (1, 1)),
                     ('minecraft:experience_bottle', 8, (2, 5))]}
    def ent(i, wt, c):
        return {'type': 'minecraft:item', 'name': i, 'weight': wt, 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(*c)}]}
    from phase39 import ACC_ALL
    for dim in RUINS:
        wjson(f'bm/loot_table/ruins/{dim}.json', {'type': 'minecraft:chest', 'pools': [
            {'rolls': G.uni(3, 5), 'entries': [ent(i, wt, c) for i, wt, c in loot_common + extra[dim]] +
             [{'type': 'minecraft:item', 'name': 'minecraft:book', 'weight': 5, 'functions': [{'function': 'minecraft:enchant_randomly'}]}]},
            {'rolls': 1, 'entries': [G.loot_entry('token', G.uni(1, 3))], 'conditions': [G.chance(0.4)]},
            {'rolls': 1, 'entries': [G.loot_entry('medallion', None)], 'conditions': [G.chance(0.03)]},
            {'rolls': 1, 'entries': [G.loot_entry('heartstone', None)], 'conditions': [G.chance(0.2)]},
            {'rolls': 1, 'entries': [G.loot_entry(a) for a in ACC_ALL], 'conditions': [G.chance(0.05)]}]})
    names = {}
    k = 0
    for dim, pals in RUINS.items():
        names[dim] = []
        for pal in pals:
            for kind in ('room', 'shrine', 'hall'):
                k += 1
                nm = f'ruin_{pal}_{kind}'
                build_ruin(kind, pal, 7400 + k).export(G.path('data', 'bm', 'structure', f'{nm}.nbt'))
                names[dim].append(nm)
    place = {'overworld': ('#bm:has_structure/ruins_overworld', 'underground_structures', {'type': 'minecraft:uniform', 'min_inclusive': {'absolute': -48}, 'max_inclusive': {'absolute': 36}},
                           None, 22, 7, 74010101),
             'nether': ('#bm:has_structure/ruins_nether', 'underground_structures', {'type': 'minecraft:uniform', 'min_inclusive': {'absolute': 16}, 'max_inclusive': {'absolute': 100}},
                        None, 24, 8, 74020202),
             'end': ('#bm:has_structure/ruins_end', 'surface_structures', {'absolute': -4}, 'WORLD_SURFACE_WG', 20, 6, 74030303)}
    wjson('bm/tags/worldgen/biome/has_structure/ruins_overworld.json', {'values': ['#minecraft:is_overworld']})
    wjson('bm/tags/worldgen/biome/has_structure/ruins_nether.json', {'values': ['#minecraft:is_nether']})
    wjson('bm/tags/worldgen/biome/has_structure/ruins_end.json', {'values': ['minecraft:end_highlands', 'minecraft:end_midlands', 'minecraft:end_barrens']})
    for dim, (biomes, step, height, proj, spacing, sep, salt) in place.items():
        sid = f'ruins_{dim}'
        s = {'type': 'minecraft:jigsaw', 'biomes': biomes, 'step': step, 'spawn_overrides': {}, 'terrain_adaptation': 'none',
             'start_pool': f'bm:{sid}/start', 'size': 1, 'start_height': height, 'max_distance_from_center': 80, 'use_expansion_hack': False,
             'liquid_settings': 'ignore_waterlogging'}
        if proj: s['project_start_to_heightmap'] = proj
        wjson(f'bm/worldgen/structure/{sid}.json', s)
        wjson(f'bm/worldgen/template_pool/{sid}/start.json', {'fallback': 'minecraft:empty', 'elements': [
            {'weight': 1, 'element': {'element_type': 'minecraft:single_pool_element', 'location': f'bm:{nm}', 'projection': 'rigid', 'processors': 'minecraft:empty'}}
            for nm in names[dim]]})
        wjson(f'bm/worldgen/structure_set/{sid}.json', {'structures': [{'structure': f'bm:{sid}', 'weight': 1}],
                                                         'placement': {'type': 'minecraft:random_spread', 'spacing': spacing, 'separation': sep, 'salt': salt}})
    wjson('bm/tags/worldgen/structure/ruins.json', {'values': [f'bm:ruins_{d}' for d in RUINS]})
    fn('admin/ruin', ['place template bm:ruin_stone_room ~-4 ~-1 ~-4', tellraw('@s', PREFIX + [T('A ruin, here (try /locate structure #bm:ruins to find a real one).', 'gray')])])

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


def rp(R):
    def post(R2):
        import json, os
        p = R2.p('assets', 'bm', 'models', 'item', 'trash3d.json')
        m = json.load(open(p))
        d = m.setdefault('display', {})
        d['gui'] = {'rotation': [30, 225, 0], 'translation': [0, -0.4, 0], 'scale': [0.5, 0.5, 0.5]}     # (was 0.7: ran 3 px past the slot)
        for k in ('thirdperson_righthand', 'thirdperson_lefthand'): d[k] = {'rotation': [75, 45, 0], 'translation': [0, 0, 0], 'scale': [0.25, 0.25, 0.25]}
        for k in ('firstperson_righthand', 'firstperson_lefthand'): d[k] = {'rotation': [0, 45, 0], 'translation': [0, 0, 0], 'scale': [0.3, 0.3, 0.3]}
        d['ground'] = {'rotation': [0, 0, 0], 'translation': [0, 2, 0], 'scale': [0.3, 0.3, 0.3]}
        json.dump(m, open(p, 'w'), indent=1)
    R.POST.append(post)

"""Phase 2.31: the special nights, in the market and in the sky.

- AMBIENCE: each special night has its own feel inside every Black Market - red haze and a slow heartbeat on a Blood Moon,
  drifting gold and chimes on a Lucky Night, green static and a far-off hum on an Invasion Night. On an Invasion Night the
  Donadian motherships go to red alert and the Vorn Dreadnought's alarms never stop.
- LUCKY NIGHT HAPPY HOUR: from dusk to dawn every Black Market trader drops the market's 1.5x markup, and Zorp knocks a
  third off his Xenite prices. Lucky Whiskers and Zorp add a few Lucky-Night-only trades.
- THE LUCKY DEN'S SLOT MACHINES WORK: pull a lever. Two Lucky Slots (1 Token a pull) and the PROGRESSIVE JACKPOT
  (5 Tokens a pull): every pull feeds one jackpot shared by every market; three 7s on the Jackpot machine win all of it.
- THE LEPRECHAUN RAT: on a Lucky Night a little rat in a green bowler sometimes turns up near you, and bolts. Catch it for
  its Pot of Gold.
- DEFEND THE MOTHERSHIP: on an Invasion Night, board a Donadian mothership and the Vorn beam onto its deck in three waves.
  Beat all three and Zorp rewards everyone aboard with Xenite and a Donadian Medal.
- SABOTAGE THE REACTOR: on an Invasion Night the Dreadnought's reactor runs hot behind four power conduits. Smash all four
  while guards beam in and the ship shuts down - and its vault opens.
- INVASION GOODS at the Fence: the Signal Jammer (no Vorn drop near you until dawn), Flak Rockets (fired at the nearest
  Scout Saucer) and a salvage counter that buys Xenite and Power Cells for Tokens."""
from items import item, T, TOTEM, ITEMS, consumable
from useitem import hold, HOLD
from nbt import snbt, B, F, D, Int

GOLD, GREEN, RED = '#ffd23f', '#7dff6a', '#ff4a4a'
SYM = [('♣', 'green'), ('♦', 'aqua'), ('♥', 'red'), ('★', 'yellow'), ('♛', 'gold'), ('7', 'dark_red')]
W_REG = [30, 25, 20, 13, 8, 4]                        # ~87% back over time
W_JP = [30, 25, 15, 7, 5, 18]                         # three 7s: about 1 pull in 170
PAY_REG = [4, 6, 10, 25, 60, 150]                     # three of a kind; any pair: the Token back
POT_SEED, POT_ADD = 50, 2
SLOTS = {56: 'reg', 59: 'jp', 62: 'reg'}             # the Den's three machines (template z; lever at x 5, y W+1)

item('four_leaf_charm', TOTEM, 'Four-Leaf Charm', 'green', ['A pressed four-leaf clover in glass.', ('Keep it anywhere in your inventory:', 'blue'),
                                                            ('Luck, always.', 'blue'), ('Sold only on Lucky Nights.', 'gray')],
     model='bm:four_leaf_charm', stack=1, cat='charm', glint=True)
item('pot_of_gold', TOTEM, 'Pot of Gold', GOLD, ['Dropped by a Leprechaun Rat.', ('Use: tip it out.', 'blue')],
     model='bm:pot_of_gold', stack=16, cat='lucky', comps={'minecraft:consumable': consumable(0.8, 'none', 'minecraft:block.chain.break', False)})
item('donadian_medal', TOTEM, 'Donadian Medal', '#3ad8c8', ['For defending a Donadian mothership', 'from the Vorn.', ('A keepsake. Zorp insists you wear it.', 'gray')],
     model='bm:donadian_medal', stack=1, cat='cosmetic', glint=True)
item('signal_jammer', TOTEM, 'Signal Jammer', '#7a8a9c', ['Switch it on during an Invasion Night.', ('Until dawn, no Vorn trooper, saucer or', 'blue'),
                                                         ('beast drops in within 48 blocks of you.', 'blue'), ('Sold only on Invasion Nights.', 'gray')],
     model='bm:signal_jammer', stack=8, cat='alien', comps={'minecraft:consumable': consumable(1.0, 'none', 'minecraft:block.beacon.power_select', False)})
item('flak_rocket', TOTEM, 'Flak Rocket', '#ff8a3a', ['Right-click: fire at the nearest Vorn', 'Scout Saucer within 48 blocks (14 damage).', ('Sold only on Invasion Nights.', 'gray')],
     model='bm:flak_rocket', stack=16, cat='alien', comps=hold('none'))
HOLD['flak_rocket'] = 'bm:p52/flak/use'
item('warlord_banner', 'minecraft:red_banner', "Warlord's Banner", RED, ['Torn from a Vorn Dreadnought\'s vault.'],
     stack=1, cat='cosmetic', comps={'minecraft:banner_patterns': [{'pattern': 'minecraft:skull', 'color': 'black'}, {'pattern': 'minecraft:border', 'color': 'lime'},
                                                                    {'pattern': 'minecraft:triangles_bottom', 'color': 'black'}]})


def lucky_specials(offer):
    return {'lucky': [offer(('lucky_token', 8), ('four_leaf_charm', 1)), offer(('lucky_token', 10), ('heartstone', 1)),
                      offer(('lucky_token', 3), ('jackpot_card_5', 1))]}


def invasion_specials(offer):
    return {'fence': [offer(('token', 6), ('signal_jammer', 1)), offer(('token', 4), ('flak_rocket', 4)),
                      offer(('xenite_green', 3), ('token', 1)), offer(('xenite_violet', 3), ('token', 1)), offer(('xenite_cyan', 3), ('token', 1)),
                      offer(('power_cell', 1), ('medallion', 2))]}


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    import zlib, mgeo, market2, phase24
    rel, W = mgeo.rel, market2.W
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    tick, fast, second = [], [], []
    objs = ['bm.slot dummy', 'bm.sst dummy', 'bm.sr1 dummy', 'bm.sr2 dummy', 'bm.sr3 dummy', 'bm.slv dummy', 'bm.lept dummy', 'bm.ev dummy', 'bm.evt dummy',
            'bm.evd dummy', 'bm.chp dummy']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o}' for o in objs] + [f'execute unless score #pot bm.slot matches 1.. run scoreboard players set #pot bm.slot {POT_SEED}']
    G.OBJECTIVES += [o.split()[0] for o in objs]
    TOK = '*[minecraft:custom_data~{bm:"token"}]'
    LIGHTS = 'execute as @a[gamemode=!spectator] at @s if entity @e[type=minecraft:marker,tag=bm.mkt,distance=..80]'

    # ================================================================ 1) ambience
    second += [f'execute if score #active bm.bm matches 1 {LIGHTS[8:]} run function bm:p52/amb/blood',
               f'execute if score #lnight bm.bm matches 1 {LIGHTS[8:]} run function bm:p52/amb/lucky',
               f'execute if score #inv bm.bm matches 1 {LIGHTS[8:]} run function bm:p52/amb/inv',
               'execute if score #inv bm.bm matches 1 as @e[type=minecraft:item_display,tag=bm.xholo] at @s if entity @a[distance=..40] run function bm:p52/amb/ship']
    fn('p52/amb/blood', ['particle minecraft:dust{color:[0.55,0.02,0.04],scale:1.6} ~ ~2 ~ 8 3 8 0 14 normal @s',
                         'execute store result score #r bm.rng run random value 1..4',
                         'execute if score #r bm.rng matches 1 run playsound minecraft:entity.warden.heartbeat ambient @s ~ ~ ~ 0.5 0.7'])
    fn('p52/amb/lucky', ['particle minecraft:wax_on ~ ~2 ~ 7 2.5 7 0 10 normal @s', 'particle minecraft:happy_villager ~ ~1.5 ~ 6 2 6 0 3 normal @s',
                         'execute store result score #r bm.rng run random value 1..5',
                         'execute if score #r bm.rng matches 1 run playsound minecraft:block.note_block.chime ambient @s ~ ~ ~ 0.4 1.6',
                         'execute if score #r bm.rng matches 2 run playsound minecraft:block.note_block.bell ambient @s ~ ~ ~ 0.3 1.2'])
    fn('p52/amb/inv', ['particle minecraft:dust{color:[0.45,1.0,0.35],scale:1.2} ~ ~2 ~ 8 3 8 0 10 normal @s', 'particle minecraft:electric_spark ~ ~2 ~ 6 2 6 0.05 3 normal @s',
                       'execute store result score #r bm.rng run random value 1..5',
                       'execute if score #r bm.rng matches 1 run playsound minecraft:block.beacon.ambient ambient @s ~ ~ ~ 0.5 0.6'])
    # the ships: red alert on a friendly mothership, alarms aboard the Dreadnought (its hologram sits next to the core)
    fn('p52/amb/ship', ['execute if entity @e[type=minecraft:marker,tag=bm.dread_core,distance=..6] run return run function bm:p52/amb/dread',
                        'particle minecraft:dust{color:[1.0,0.1,0.1],scale:2.0} ~ ~-1 ~ 9 2 9 0 24 force @a[distance=..40]',
                        'execute store result score #r bm.rng run random value 1..3',
                        'execute if score #r bm.rng matches 1 run playsound minecraft:block.note_block.bass ambient @a[distance=..40] ~ ~ ~ 1 0.5',
                        'execute if score #r bm.rng matches 1 run title @a[distance=..30] actionbar ' + snbt(T('RED ALERT - Vorn vessels inbound', RED, bold=True))])
    fn('p52/amb/dread', ['particle minecraft:crimson_spore ~ ~-1 ~ 9 2 9 0 30 force @a[distance=..40]', 'particle minecraft:dust{color:[1.0,0.0,0.0],scale:2.4} ~ ~ ~ 1 1 1 0 12 force @a[distance=..40]',
                         'execute store result score #r bm.rng run random value 1..3',
                         'execute if score #r bm.rng matches 1 run playsound minecraft:block.bell.resonate hostile @a[distance=..40] ~ ~ ~ 1.4 0.6'])

    # ================================================================ 2) Happy Hour + night-only trades (trader offers swap with the night)
    normal = G.all_offers()
    saved = dict(G.PRICE_SCALE); G.PRICE_SCALE.clear()          # (G is the running build module: its own price scale)
    try:
        happy = G.all_offers()
    finally:
        G.PRICE_SCALE.update(saved)
    for k, extra in lucky_specials(G.offer).items(): happy[k] = happy[k] + extra
    inv = {k: list(v) for k, v in normal.items()}
    for k, extra in invasion_specials(G.offer).items(): inv[k] = inv[k] + extra
    ln = G.FUNCS['loop/second']
    for k in G.NPCS:
        old = next((i for i, l in enumerate(ln) if l.startswith(f'execute as @e[tag=bm.npc_{k}] unless score @s bm.ofv matches ')), None)
        if old is None: continue
        ver = ln[old].split('matches ')[1].split()[0]
        lines = []
        for night, offers, cond in (('lucky', happy, 'if score #lnight bm.bm matches 1'), ('inv', inv, 'if score #inv bm.bm matches 1')):
            if snbt(offers[k]) == snbt(normal[k]): continue
            blob = snbt(offers[k]); v = zlib.crc32((night + blob).encode()) % 1000000000
            fn(f'p52/npc/{k}_{night}', [f'data modify entity @s Offers.Recipes set value {blob}', f'scoreboard players set @s bm.ofv {v}'])
            lines.append(f'execute {cond} as @e[tag=bm.npc_{k}] unless score @s bm.ofv matches {v} run function bm:p52/npc/{k}_{night}')
        guard = ''.join(f' unless score #{"lnight" if n == "lucky" else "inv"} bm.bm matches 1' for n, o in (('lucky', happy), ('inv', inv)) if snbt(o[k]) != snbt(normal[k]))
        ln[old] = f'execute{guard} as @e[tag=bm.npc_{k}] unless score @s bm.ofv matches {ver} run function bm:p17/npc/{k}'
        ln[old + 1:old + 1] = lines
    # Zorp: a third off on a Lucky Night, and two Lucky-Night trades
    zl = [(b, bb, s) for b, bb, s in phase24.OFFERS]
    cut = lambda c: (c[0], max(1, -(-c[1] * 2 // 3))) if c else None
    zh = [G.offer(cut(b), s, cut(bb)) if bb else G.offer(cut(b), s) for b, bb, s in zl]
    zh += [G.offer(('xenite_cyan', 6), ('xenite_red', 1)), G.offer(('xenite_green', 20), ('power_cell', 1), ('xenite_violet', 20))]
    blob = snbt(zh); zv = zlib.crc32(('lucky' + blob).encode()) % 1000000000
    fn('p52/npc/alien_lucky', [f'data modify entity @s Offers.Recipes set value {blob}', f'scoreboard players set @s bm.ofv {zv}'])
    za = next(i for i, l in enumerate(ln) if l.startswith('execute as @e[tag=bm.npc_alien] unless score @s bm.ofv matches '))
    ln[za] = ln[za].replace('execute as @e[tag=bm.npc_alien]', 'execute unless score #lnight bm.bm matches 1 as @e[tag=bm.npc_alien]')
    ln.insert(za + 1, f'execute if score #lnight bm.bm matches 1 as @e[tag=bm.npc_alien] unless score @s bm.ofv matches {zv} run function bm:p52/npc/alien_lucky')
    G.FUNCS['p22/lucky/start'].append(tellraw('@a', PREFIX + [T('HAPPY HOUR! ', GOLD, bold=True), T('Until dawn every Black Market trader sells at base price, Zorp takes a third off, and Lucky Whiskers has something special.', 'yellow')]))
    G.FUNCS['p32/inv/start'].append(tellraw('@a', PREFIX + [T('The Fence has invasion stock tonight: ', GREEN), T('Signal Jammers, Flak Rockets, and he buys Vorn salvage.', 'gray')]))
    second.append('execute as @a if items entity @s container.* *[minecraft:custom_data~{bm:"four_leaf_charm"}] run effect give @s minecraft:luck 3 0 true')

    # ================================================================ 3) the Lucky Den's slot machines + the progressive jackpot
    S = 'storage bm:slot'
    G.FUNCS['load'][-1:-1] = [f'data modify {S} sym set value {snbt([T(s, c, bold=True) for s, c in SYM])}']
    for z, kind in SLOTS.items():
        mgeo.need_air((4, W + 2, z), 'a slot machine\'s reels')
    reels = lambda kind: snbt({'Tags': ['bm.slotd', f'bm.slotd_{kind}'], 'billboard': 'center', 'text': [T('♣  ♦  ♥', 'white', bold=True)], 'background': Int(0xC0000000 - (1 << 32)),
                                'line_width': Int(120), 'brightness': {'block': Int(15), 'sky': Int(15)},
                                'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)], 'translation': [F(0), F(0), F(0)], 'scale': [F(0.9)] * 3}})
    potd = snbt({'Tags': ['bm.potd'], 'billboard': 'center', 'text': [T('PROGRESSIVE JACKPOT', GOLD, bold=True)], 'background': Int(0xA0000000 - (1 << 32)), 'line_width': Int(200),
                 'brightness': {'block': Int(15), 'sky': Int(15)},
                 'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)], 'translation': [F(0), F(0), F(0)], 'scale': [F(0.7)] * 3}})
    patch = ['tag @s add bm.p52']
    for z, kind in SLOTS.items():
        patch += [f'execute positioned {rel((5.5, W + 1.5, z + 0.5))} unless entity @e[type=minecraft:marker,tag=bm.slot,distance=..0.5] run summon minecraft:marker ~ ~ ~ {{Tags:["bm.slot","bm.slot_{kind}"]}}',
                  f'execute positioned {rel((4.5, W + 2.55, z + 0.5))} unless entity @e[type=minecraft:text_display,tag=bm.slotd,distance=..0.5] run summon minecraft:text_display ~ ~ ~ {reels(kind)}']
    patch.append(f'execute positioned {rel((4.5, W + 3.35, 59.5))} unless entity @e[type=minecraft:text_display,tag=bm.potd,distance=..0.5] run summon minecraft:text_display ~ ~ ~ {potd}')
    fn('p52/market', patch)
    p41 = next(l for l in G.FUNCS['loop/second'] if 'function bm:p41/patch' in l)
    second.append(p41.replace('tag=!bm.p41]', 'tag=!bm.p52]').replace('function bm:p41/patch', 'function bm:p52/market'))
    # a pull: the lever changed state (either way - levers stay where they're flipped)
    tick.append('execute as @e[type=minecraft:marker,tag=bm.slot] at @s if entity @a[distance=..8] run function bm:p52/slot/tick')
    fn('p52/slot/tick', ['execute store result score #lv bm.rng if block ~ ~ ~ minecraft:lever[powered=true]',
                         'execute unless score @s bm.slv = #lv bm.rng unless score @s bm.sst matches 1.. if score @s bm.slv matches 0.. run function bm:p52/slot/pull',
                         'scoreboard players operation @s bm.slv = #lv bm.rng',
                         'execute if score @s bm.sst matches 1.. run function bm:p52/slot/spin'])
    fn('p52/slot/pull', ['scoreboard players set #have bm.rng 0', 'scoreboard players set #cost bm.rng 1', 'execute if entity @s[tag=bm.slot_jp] run scoreboard players set #cost bm.rng 5',
                         f'execute as @p[distance=..5,gamemode=!spectator] store result score #have bm.rng run clear @s {TOK} 0',
                         'execute if score #have bm.rng < #cost bm.rng run return run execute as @p[distance=..5] run ' + title('@s', 'actionbar', T('The machine wants Black Market Tokens.', 'gray')),
                         'execute as @p[distance=..5,gamemode=!spectator] run function bm:p52/slot/pay_in',
                         'scoreboard players operation @s bm.pid = #sp bm.pid', 'scoreboard players set @s bm.sst 30',
                         'execute if entity @s[tag=bm.slot_reg] run function bm:p52/slot/roll_reg', 'execute if entity @s[tag=bm.slot_jp] run function bm:p52/slot/roll_jp',
                         f'execute if entity @s[tag=bm.slot_jp] run scoreboard players add #pot bm.slot {POT_ADD}',
                         f'execute if entity @s[tag=bm.slot_jp] if score #lnight bm.bm matches 1 run scoreboard players add #pot bm.slot {POT_ADD}',
                         'playsound minecraft:block.lever.click block @a[distance=..12] ~ ~ ~ 1 0.6', 'playsound minecraft:block.note_block.pling block @a[distance=..12] ~ ~ ~ 0.6 0.8'])
    fn('p52/slot/pay_in', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #sp bm.pid = @s bm.pid',
                           f'execute store result score #have bm.rng run clear @s {TOK} 0',
                           'execute if score #cost bm.rng matches 1 if score #have bm.rng matches 1.. run clear @s ' + TOK + ' 1',
                           'execute if score #cost bm.rng matches 5 if score #have bm.rng matches 5.. run clear @s ' + TOK + ' 5',
                           'advancement grant @s only bm:story/slots'])
    for kind, wts in (('reg', W_REG), ('jp', W_JP)):
        lines = []
        for r in (1, 2, 3):
            lines.append('execute store result score #x bm.rng run random value 1..100')
            acc = 0
            for i, w in enumerate(wts):
                lines.append(f'execute if score #x bm.rng matches {acc + 1}..{acc + w} run scoreboard players set @s bm.sr{r} {i}')
                acc += w
        fn(f'p52/slot/roll_{kind}', lines)
    # the reels: each stops in turn (at 20, 12 and 4 ticks left), then the machine pays
    fn('p52/slot/spin', ['scoreboard players remove @s bm.sst 1',
                         'execute store result score #s1 bm.rng run random value 0..5', 'execute store result score #s2 bm.rng run random value 0..5',
                         'execute store result score #s3 bm.rng run random value 0..5',
                         'execute if score @s bm.sst matches ..20 run scoreboard players operation #s1 bm.rng = @s bm.sr1',
                         'execute if score @s bm.sst matches ..12 run scoreboard players operation #s2 bm.rng = @s bm.sr2',
                         'execute if score @s bm.sst matches ..4 run scoreboard players operation #s3 bm.rng = @s bm.sr3',
                         'execute if score @s bm.sst matches 20 run playsound minecraft:block.note_block.hat block @a[distance=..12] ~ ~ ~ 1 1.2',
                         'execute if score @s bm.sst matches 12 run playsound minecraft:block.note_block.hat block @a[distance=..12] ~ ~ ~ 1 1.2',
                         'execute if score @s bm.sst matches 4 run playsound minecraft:block.note_block.hat block @a[distance=..12] ~ ~ ~ 1 1.2',
                         f'execute store result {S} q.a int 1 run scoreboard players get #s1 bm.rng', f'execute store result {S} q.b int 1 run scoreboard players get #s2 bm.rng',
                         f'execute store result {S} q.c int 1 run scoreboard players get #s3 bm.rng', f'function bm:p52/slot/show with {S} q',
                         'execute if score @s bm.sst matches 0 run function bm:p52/slot/result'])
    fn('p52/slot/show', [f'data modify {S} line set value ["","","  ","","  ",""]', f'$data modify {S} line[1] set from {S} sym[$(a)]',
                         f'$data modify {S} line[3] set from {S} sym[$(b)]', f'$data modify {S} line[5] set from {S} sym[$(c)]',
                         f'execute positioned ^ ^ ^ as @e[type=minecraft:text_display,tag=bm.slotd,distance=..2,limit=1,sort=nearest] run data modify entity @s text set from {S} line'])
    # results
    fn('p52/slot/result', ['scoreboard players set #win bm.rng 0', 'scoreboard players set #trip bm.rng 0', 'scoreboard players set #pair bm.rng 0',
                           'execute if score @s bm.sr1 = @s bm.sr2 if score @s bm.sr2 = @s bm.sr3 run scoreboard players set #trip bm.rng 1',
                           'execute if score #trip bm.rng matches 0 if score @s bm.sr1 = @s bm.sr2 run scoreboard players set #pair bm.rng 1',
                           'execute if score #trip bm.rng matches 0 if score @s bm.sr2 = @s bm.sr3 run scoreboard players set #pair bm.rng 1',
                           'execute if score #trip bm.rng matches 0 if score @s bm.sr1 = @s bm.sr3 run scoreboard players set #pair bm.rng 1',
                           'execute if entity @s[tag=bm.slot_reg] run function bm:p52/slot/res_reg', 'execute if entity @s[tag=bm.slot_jp] run function bm:p52/slot/res_jp',
                           'execute if score #win bm.rng matches 1.. run function bm:p52/slot/payout',
                           'execute if score #win bm.rng matches 0 run playsound minecraft:block.note_block.didgeridoo block @a[distance=..12] ~ ~ ~ 0.6 0.6'])
    fn('p52/slot/res_reg', [f'execute if score #trip bm.rng matches 1 if score @s bm.sr1 matches {i} run scoreboard players set #win bm.rng {p}' for i, p in enumerate(PAY_REG)] +
       ['execute if score #pair bm.rng matches 1 run scoreboard players set #win bm.rng 1'])
    fn('p52/slot/res_jp', ['execute if score #trip bm.rng matches 1 if score @s bm.sr1 matches 5 run return run function bm:p52/slot/jackpot',
                           'execute if score #trip bm.rng matches 1 if score @s bm.sr1 matches 4 run scoreboard players set #win bm.rng 30',
                           'execute if score #trip bm.rng matches 1 if score @s bm.sr1 matches 3 run scoreboard players set #win bm.rng 15',
                           'scoreboard players set #sev bm.rng 0', 'execute if score @s bm.sr1 matches 5 run scoreboard players add #sev bm.rng 1',
                           'execute if score @s bm.sr2 matches 5 run scoreboard players add #sev bm.rng 1', 'execute if score @s bm.sr3 matches 5 run scoreboard players add #sev bm.rng 1',
                           'execute if score #sev bm.rng matches 2 run scoreboard players set #win bm.rng 5'])
    fn('p52/slot/jackpot', ['scoreboard players operation #win bm.rng = #pot bm.slot', f'scoreboard players set #pot bm.slot {POT_SEED}',
                            'scoreboard players operation #sp bm.pid = @s bm.pid', 'execute as @a if score @s bm.pid = #sp bm.pid run tag @s add bm.jpw',
                            'advancement grant @a[tag=bm.jpw] only bm:story/jackpot',
                            tellraw('@a', PREFIX + [T('JACKPOT! ', GOLD, bold=True), {'selector': '@a[tag=bm.jpw]', 'color': 'yellow'},
                                                    T(' hit three 7s in the Lucky Den and won ', 'yellow'), {'score': {'name': '#win', 'objective': 'bm.rng'}, 'color': GOLD, 'bold': True},
                                                    T(' Tokens!', 'yellow')]),
                            'tag @a remove bm.jpw', 'particle minecraft:firework ~ ~1.5 ~ 1 1 1 0.15 80', 'particle minecraft:wax_on ~ ~2 ~ 2 2 2 0 60',
                            'playsound minecraft:ui.toast.challenge_complete block @a[distance=..24] ~ ~ ~ 1 1'])
    fn('p52/slot/payout', ['scoreboard players operation #sp bm.pid = @s bm.pid', f'execute store result {S} w.n int 1 run scoreboard players get #win bm.rng',
                           f'execute as @a if score @s bm.pid = #sp bm.pid run function bm:p52/slot/give with {S} w',
                           'playsound minecraft:entity.player.levelup block @a[distance=..12] ~ ~ ~ 0.6 1.4', 'particle minecraft:wax_on ~ ~1 ~ 0.6 0.6 0.6 0 20'])
    fn('p52/slot/give', [f'$give @s {G.item_arg("token")} $(n)', '$title @s actionbar ' + snbt([T('You win ', GOLD), T('$(n)', GOLD, bold=True), T(' Tokens!', GOLD)])])
    # the jackpot's sign
    second.append(f'execute store result {S} p.n int 1 run scoreboard players get #pot bm.slot')
    second.append(f'execute as @e[type=minecraft:text_display,tag=bm.potd] at @s if entity @a[distance=..24] run function bm:p52/slot/sign with {S} p')
    fn('p52/slot/sign', ['$data modify entity @s text set value ' + snbt([T('PROGRESSIVE JACKPOT\n', GOLD, bold=True), T('$(n) Tokens', 'yellow', bold=True),
                                                                          T('\n5 Tokens a pull - three 7s win it all', 'gray')])])

    # ================================================================ 4) the Leprechaun Rat
    lep = {'Tags': ['bm.lep', 'bm.lepnew', 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1), 'Health': F(8),
           'DeathLootTable': 'bm:entities/leprechaun', 'CustomName': T('Leprechaun Rat', 'green', bold=True),
           'attributes': [{'id': 'minecraft:max_health', 'base': D(8)}, {'id': 'minecraft:movement_speed', 'base': D(0.42)}, {'id': 'minecraft:scale', 'base': D(0.7)}],
           'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}]}
    lepd = snbt({'Tags': ['bm.lepd', 'bm.lepnew'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:rat3d_lucky'}},
                 'item_display': 'fixed', 'teleport_duration': Int(2), 'brightness': {'block': Int(13), 'sky': Int(13)},
                 'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)], 'translation': [F(0), F(0.4), F(0)], 'scale': [F(0.8)] * 3}})
    wjson('bm/loot_table/entities/leprechaun.json', {'type': 'minecraft:entity', 'pools': [{'rolls': 1, 'entries': [G.loot_entry('pot_of_gold')]}]})
    wjson('bm/loot_table/p52/pot_of_gold.json', {'type': 'minecraft:command', 'pools': [{'rolls': 1, 'entries': [G.loot_entry('token', G.uni(8, 16))]},
                                                                                       {'rolls': 1, 'entries': [G.loot_entry('lucky_token', G.uni(3, 6))]}]})
    G.consume_adv('pot_of_gold', 'bm:p52/pot')
    fn('p52/pot', ['advancement revoke @s only bm:consume/pot_of_gold', 'loot give @s loot bm:p52/pot_of_gold', 'particle minecraft:wax_on ~ ~1 ~ 0.4 0.5 0.4 0 30',
                   'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.8', say('The pot spills over with gold!', GOLD)])
    second += ['execute if score #lnight bm.bm matches 1 as @a[gamemode=survival] at @s if dimension minecraft:overworld if predicate bm:sees_sky run function bm:p52/lep/try',
               'scoreboard players remove @e[type=minecraft:ocelot,tag=bm.lep] bm.lept 1',
               'execute as @e[type=minecraft:ocelot,tag=bm.lep,scores={bm.lept=..0}] at @s run function bm:p52/lep/vanish',
               'execute unless score #lnight bm.bm matches 1 as @e[type=minecraft:ocelot,tag=bm.lep] at @s run function bm:p52/lep/vanish']
    fn('p52/lep/try', ['execute store result score #r bm.rng run random value 1..90', 'execute unless score #r bm.rng matches 1 run return 0',
                       'execute if entity @e[type=minecraft:ocelot,tag=bm.lep,distance=..96] run return 0',
                       'summon minecraft:marker ~ ~ ~ {Tags:["bm.lsp"]}',
                       'execute as @e[type=minecraft:marker,tag=bm.lsp,distance=..1,limit=1] store result entity @s Rotation[0] float 1 run random value 0..359',
                       'execute as @e[type=minecraft:marker,tag=bm.lsp,distance=..1,limit=1] rotated as @s positioned ^ ^ ^12 positioned over motion_blocking_no_leaves run function bm:p52/lep/spawn',
                       'kill @e[type=minecraft:marker,tag=bm.lsp]'])
    fn('p52/lep/spawn', ['execute unless block ~ ~ ~ #minecraft:replaceable run return 0', f'summon minecraft:ocelot ~ ~ ~ {snbt(lep)}', f'summon minecraft:item_display ~ ~ ~ {lepd}',
                         'scoreboard players set @e[type=minecraft:ocelot,tag=bm.lepnew,distance=..1] bm.lept 150', 'tag @e[tag=bm.lepnew,distance=..1] remove bm.lepnew',
                         'particle minecraft:happy_villager ~ ~0.5 ~ 0.4 0.4 0.4 0 12', 'playsound minecraft:entity.allay.ambient_with_item neutral @a[distance=..24] ~ ~ ~ 1 1.6',
                         tellraw('@a[distance=..24]', [T('A Leprechaun Rat! ', 'green', bold=True), T('Catch it before it vanishes...', 'gray', italic=True)])])
    tick.append('execute as @e[type=minecraft:item_display,tag=bm.lepd] at @s run function bm:p52/lep/follow')
    fn('p52/lep/follow', ['execute unless entity @e[type=minecraft:ocelot,tag=bm.lep,distance=..3] run return run kill @s',
                          'execute as @e[type=minecraft:ocelot,tag=bm.lep,distance=..3,limit=1,sort=nearest] at @s run tp @e[type=minecraft:item_display,tag=bm.lepd,distance=..3,limit=1,sort=nearest] ~ ~ ~ ~180 0'])
    fn('p52/lep/vanish', ['particle minecraft:happy_villager ~ ~0.5 ~ 0.4 0.4 0.4 0 16', 'particle minecraft:wax_on ~ ~0.5 ~ 0.3 0.3 0.3 0 10',
                          'kill @e[type=minecraft:item_display,tag=bm.lepd,distance=..3]', 'tp @s ~ -400 ~', 'kill @s'])
    fast.append('execute if score #lnight bm.bm matches 1 as @e[type=minecraft:ocelot,tag=bm.lep] at @s run particle minecraft:wax_on ~ ~0.4 ~ 0.2 0.2 0.2 0 2')

    # ================================================================ 5) Defend the Mothership (anchored on the green hologram over the deck)
    second.append('execute if score #inv bm.bm matches 1 as @e[type=minecraft:item_display,tag=bm.xholo] at @s unless entity @e[type=minecraft:marker,tag=bm.dread_core,distance=..6] run function bm:p52/def/tick')
    second.append('execute unless score #inv bm.bm matches 1 as @e[type=minecraft:item_display,tag=bm.xholo,scores={bm.ev=1..}] at @s run function bm:p52/def/cancel')
    deck = 'positioned ~ ~-2.5 ~'
    fn('p52/def/tick', ['execute unless score @s bm.ev matches 1.. if score @s bm.evd = #day bm.bm run return 0',
                        f'execute unless score @s bm.ev matches 1.. if entity @a[gamemode=!spectator,gamemode=!creative,distance=..24] run function bm:p52/def/start',
                        'execute unless score @s bm.ev matches 1.. run return 0',
                        f'execute unless entity @a[gamemode=!spectator,distance=..48] run scoreboard players add @s bm.evt 1',
                        f'execute if entity @a[gamemode=!spectator,distance=..48] run scoreboard players set @s bm.evt 0',
                        'execute if score @s bm.evt matches 30.. run return run function bm:p52/def/cancel',
                        f'execute {deck} store result score #n bm.rng if entity @e[tag=bm.dwave,distance=..40]',
                        'execute if score #n bm.rng matches 0 run function bm:p52/def/next'])
    fn('p52/def/start', ['scoreboard players set @s bm.ev 1', 'scoreboard players set @s bm.evt 0',
                         'title @a[distance=..48] times 10 50 20', 'title @a[distance=..48] subtitle ' + snbt(T('The Vorn are boarding! Defend the mothership.', RED)),
                         'title @a[distance=..48] title ' + snbt(T('RED ALERT', RED, bold=True)),
                         'playsound minecraft:event.raid.horn hostile @a[distance=..48] ~ ~ ~ 1 1.2', 'function bm:p52/def/wave'])
    fn('p52/def/next', ['execute if score @s bm.ev matches 4.. run return run function bm:p52/def/win', 'function bm:p52/def/wave'])
    fn('p52/def/wave', ['scoreboard players set #k bm.rng 3', 'execute if score @s bm.ev matches 2 run scoreboard players set #k bm.rng 5',
                        'execute if score @s bm.ev matches 3 run scoreboard players set #k bm.rng 7',
                        title('@a[distance=..48]', 'actionbar', [T('Wave ', RED), {'score': {'name': '@s', 'objective': 'bm.ev'}, 'color': 'white', 'bold': True}, T(' of 3', RED)]),
                        f'execute {deck} run function bm:p52/def/drop', 'scoreboard players add @s bm.ev 1'])
    fn('p52/def/drop', ['execute if score #k bm.rng matches ..0 run return 0', 'scoreboard players remove #k bm.rng 1',
                        'summon minecraft:marker ~ ~ ~ {Tags:["bm.dsp"]}',
                        'execute as @e[type=minecraft:marker,tag=bm.dsp,distance=..1,limit=1] store result entity @s Rotation[0] float 1 run random value 0..359',
                        'execute as @e[type=minecraft:marker,tag=bm.dsp,distance=..1,limit=1] rotated as @s positioned ^ ^ ^5 run function bm:p32/spawn/trooper',
                        'kill @e[type=minecraft:marker,tag=bm.dsp]', 'tag @e[tag=bm.vtroop,tag=!bm.dwave,distance=..8] add bm.dwave', 'function bm:p52/def/drop'])
    fn('p52/def/win', ['scoreboard players set @s bm.ev 0', 'scoreboard players operation @s bm.evd = #day bm.bm',
                       'execute as @a[gamemode=!spectator,distance=..40] run function bm:p52/def/reward',
                       'title @a[distance=..48] title ' + snbt(T('MOTHERSHIP SAVED', GREEN, bold=True)), 'playsound minecraft:ui.toast.challenge_complete hostile @a[distance=..48] ~ ~ ~ 1 1',
                       'particle minecraft:end_rod ~ ~ ~ 3 2 3 0.1 60'])
    fn('p52/def/reward', [give('xenite_green', 6), give('xenite_violet', 6), give('xenite_cyan', 6),
                          'execute unless items entity @s container.* *[minecraft:custom_data~{bm:"donadian_medal"}] run ' + give('donadian_medal'),
                          'advancement grant @s only bm:story/defend', tellraw('@s', PREFIX + [T('Zorp: "You fought for us. Take these - and wear the medal!"', '#3ad8c8')])])
    fn('p52/def/cancel', ['scoreboard players set @s bm.ev 0', f'execute {deck} as @e[tag=bm.dwave,distance=..48] at @s run function bm:p32/beamup'])

    # ================================================================ 6) Sabotage the Reactor (the Dreadnought's core)
    cond = snbt({'Tags': ['bm.rcond', 'bm.rnew'], 'item': {'id': 'minecraft:beacon', 'count': Int(1)}, 'item_display': 'fixed', 'brightness': {'block': Int(15), 'sky': Int(15)},
                 'glow_color_override': Int(0xff3030), 'Glowing': B(1),
                 'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)], 'translation': [F(0), F(0.6), F(0)], 'scale': [F(1.1)] * 3}})
    chit = snbt({'Tags': ['bm.rhit', 'bm.rnew'], 'width': F(1.3), 'height': F(1.6), 'response': B(1)})
    second.append('execute if score #inv bm.bm matches 1 as @e[type=minecraft:marker,tag=bm.dread_core] at @s run function bm:p52/rx/tick')
    second.append('execute unless score #inv bm.bm matches 1 as @e[type=minecraft:marker,tag=bm.dread_core,scores={bm.ev=1..}] at @s run function bm:p52/rx/cancel')
    fn('p52/rx/tick', ['execute unless score @s bm.ev matches 1.. if score @s bm.evd = #day bm.bm run return 0',
                       'execute unless score @s bm.ev matches 1.. if entity @a[gamemode=!spectator,gamemode=!creative,distance=..30] run function bm:p52/rx/start',
                       'execute unless score @s bm.ev matches 1.. run return 0',
                       'execute unless entity @a[gamemode=!spectator,distance=..48] run scoreboard players add @s bm.evt 1',
                       'execute if entity @a[gamemode=!spectator,distance=..48] run scoreboard players set @s bm.evt 0',
                       'execute if score @s bm.evt matches 60.. run return run function bm:p52/rx/cancel',
                       'execute unless entity @e[type=minecraft:interaction,tag=bm.rhit,distance=..12] run return run function bm:p52/rx/win',
                       'scoreboard players add @s bm.chp 1',
                       'execute if score @s bm.chp matches 20.. run function bm:p52/rx/reinforce',
                       'particle minecraft:dust{color:[1.0,0.1,0.1],scale:2.0} ~ ~1 ~ 0.6 1.2 0.6 0 16 force @a[distance=..40]'])
    fn('p52/rx/start', ['scoreboard players set @s bm.ev 1', 'scoreboard players set @s bm.evt 0', 'scoreboard players set @s bm.chp 0'] +
       [f'execute positioned {o} run function bm:p52/rx/conduit' for o in ('~5 ~ ~', '~-5 ~ ~', '~ ~ ~5', '~ ~ ~-5')] +
       ['title @a[distance=..48] times 10 50 20', 'title @a[distance=..48] subtitle ' + snbt(T('Smash the four power conduits round the core!', RED)),
        'title @a[distance=..48] title ' + snbt(T('REACTOR OVERLOAD', RED, bold=True)), 'playsound minecraft:block.beacon.activate hostile @a[distance=..48] ~ ~ ~ 1 0.5'])
    fn('p52/rx/conduit', [f'summon minecraft:item_display ~ ~ ~ {cond}', f'summon minecraft:interaction ~ ~ ~ {chit}',
                          'scoreboard players set @e[type=minecraft:interaction,tag=bm.rnew,distance=..0.5] bm.chp 8', 'tag @e[tag=bm.rnew,distance=..0.5] remove bm.rnew'])
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.rhit] if data entity @s attack at @s run function bm:p52/rx/hit')
    fn('p52/rx/hit', ['scoreboard players remove @s bm.chp 1', 'particle minecraft:electric_spark ~ ~1 ~ 0.4 0.5 0.4 0.3 20', 'playsound minecraft:block.anvil.land hostile @a[distance=..24] ~ ~ ~ 0.5 1.6',
                      title('@a[distance=..8]', 'actionbar', [T('Conduit: ', RED), {'score': {'name': '@s', 'objective': 'bm.chp'}, 'color': 'white'}, T(' hits left', RED)]),
                      'execute if score @s bm.chp matches ..0 run return run function bm:p52/rx/break', 'data remove entity @s attack'])
    fn('p52/rx/break', ['particle minecraft:explosion ~ ~1 ~ 0.4 0.4 0.4 0 3', 'playsound minecraft:entity.generic.explode hostile @a[distance=..32] ~ ~ ~ 1 1.2',
                        'kill @e[type=minecraft:item_display,tag=bm.rcond,distance=..0.5]', 'kill @s'])
    fn('p52/rx/reinforce', ['scoreboard players set @s bm.chp 0', 'execute positioned ~3 ~ ~3 run function bm:p32/spawn/trooper',
                            'execute positioned ~-3 ~ ~-3 run function bm:p32/spawn/trooper',
                            title('@a[distance=..40]', 'actionbar', T('Vorn reinforcements beaming in!', RED, bold=True))])
    fn('p52/rx/win', ['scoreboard players set @s bm.ev 0', 'scoreboard players operation @s bm.evd = #day bm.bm',
                      'execute positioned ~ ~ ~3 run setblock ~ ~ ~ minecraft:barrel[facing=up]',
                      'execute positioned ~ ~ ~3 run data merge block ~ ~ ~ {LootTable:"bm:p52/vault",CustomName:' + snbt(T('Dreadnought Vault', RED)) + '}',
                      'execute as @a[gamemode=!spectator,distance=..40] run advancement grant @s only bm:story/reactor',
                      'title @a[distance=..48] title ' + snbt(T('REACTOR OFFLINE', GREEN, bold=True)), 'title @a[distance=..48] subtitle ' + snbt(T('The vault is open.', 'gray')),
                      'playsound minecraft:block.beacon.deactivate hostile @a[distance=..48] ~ ~ ~ 1 0.5', 'particle minecraft:end_rod ~ ~1 ~ 2 2 2 0.1 50',
                      'scoreboard players set @s bm.xlf 600'])
    fn('p52/rx/cancel', ['scoreboard players set @s bm.ev 0', 'kill @e[type=minecraft:item_display,tag=bm.rcond,distance=..12]', 'kill @e[type=minecraft:interaction,tag=bm.rhit,distance=..12]'])
    wjson('bm/loot_table/p52/vault.json', {'type': 'minecraft:chest', 'pools': [
        {'rolls': 1, 'entries': [G.loot_entry('xenite_red', G.uni(6, 10))]}, {'rolls': 1, 'entries': [G.loot_entry('warlord_banner')]},
        {'rolls': 1, 'entries': [G.loot_entry('power_cell')], 'conditions': [{'condition': 'minecraft:random_chance', 'chance': 0.25}]},
        {'rolls': 1, 'entries': [G.loot_entry('xenite_green', G.uni(8, 16))]}]})

    # ================================================================ 7) invasion goods
    G.consume_adv('signal_jammer', 'bm:p52/jam')
    fn('p52/jam', ['advancement revoke @s only bm:consume/signal_jammer',
                   'execute unless score #inv bm.bm matches 1 run return run function bm:p52/jam_refund',
                   'tag @s add bm.jam', 'advancement grant @s only bm:story/jammer', 'particle minecraft:electric_spark ~ ~1.5 ~ 0.4 0.4 0.4 0.2 30',
                   say('Jammer on. No Vorn will drop in near you until dawn.', '#7a8a9c')])
    fn('p52/jam_refund', [give('signal_jammer'), say('There is nothing to jam tonight. (Refunded)')])
    G.FUNCS['p32/inv/surge'].insert(0, 'execute if entity @a[tag=bm.jam,distance=..48] run return 0')
    G.FUNCS['p32/inv/end'].append('tag @a remove bm.jam')
    second.append('execute unless score #inv bm.bm matches 1 run tag @a[tag=bm.jam] remove bm.jam')
    second.append('execute as @a[tag=bm.jam] at @s run particle minecraft:electric_spark ~ ~2.2 ~ 0.2 0.1 0.2 0.02 1')
    fn('p52/flak/use', ['execute unless entity @e[tag=bm.vsauc,distance=..48] run return run ' + say('No Vorn saucer in range.'),
                        'execute unless entity @s[gamemode=creative] run item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
                        'tag @s add bm.flaker', 'tag @e[tag=bm.vsauc,distance=..48,sort=nearest,limit=1] add bm.ftgt',
                        'scoreboard players set #fs bm.rng 40', 'execute anchored eyes positioned ^ ^ ^1 facing entity @e[tag=bm.ftgt,limit=1] eyes run function bm:p52/flak/step',
                        'execute as @e[tag=bm.ftgt,limit=1] at @s run function bm:p52/flak/boom', 'tag @e[tag=bm.ftgt] remove bm.ftgt', 'tag @s remove bm.flaker',
                        'playsound minecraft:entity.firework_rocket.launch player @a[distance=..24] ~ ~ ~ 1 1'])
    fn('p52/flak/step', ['particle minecraft:firework ~ ~ ~ 0 0 0 0 1 force @a[distance=..64]', 'execute if entity @e[tag=bm.ftgt,distance=..1.5] run return 0',
                         'scoreboard players remove #fs bm.rng 1', 'execute if score #fs bm.rng matches 1.. positioned ^ ^ ^1.2 run function bm:p52/flak/step'])
    fn('p52/flak/boom', ['damage @s 14 minecraft:fireworks by @a[tag=bm.flaker,limit=1]', 'particle minecraft:firework ~ ~ ~ 0.6 0.6 0.6 0.2 40',
                         'playsound minecraft:entity.firework_rocket.large_blast hostile @a[distance=..48] ~ ~ ~ 1.5 1'])

    # ================================================================ 8) achievements
    def adv(key, parent, ico, ttl, desc, crit, frame='task'):
        icon = {'id': ITEMS[ico]['base'], 'components': {'minecraft:item_model': ITEMS[ico]['comps'].get('minecraft:item_model', ITEMS[ico]['base'])}} if ico in ITEMS else {'id': ico}
        wjson(f'bm/advancement/story/{key}.json', {'parent': f'bm:story/{parent}', 'criteria': crit,
                                                   'display': {'icon': icon, 'title': T(ttl, 'gold' if frame == 'challenge' else 'yellow'), 'description': T(desc, 'gray'),
                                                               'frame': frame, 'show_toast': True, 'announce_to_chat': True, 'hidden': False}})
    granted = {'done': {'trigger': 'minecraft:impossible'}}
    adv('happy_hour', 'lucky_night', 'minecraft:emerald', 'Happy Hour', 'Trade at the Black Market on a Lucky Night', granted)
    adv('slots', 'lucky_night', 'minecraft:lever', 'One-Armed Bandit', 'Pull a slot machine lever in the Lucky Den', granted)
    adv('jackpot', 'slots', 'token', 'Jackpot!', 'Win the progressive jackpot', granted, 'challenge')
    adv('leprechaun', 'lucky_night', 'pot_of_gold', "Top o' the Mornin'", 'Catch a Leprechaun Rat',
        {'slain': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [{'condition': 'minecraft:entity_properties', 'entity': 'this',
                                                                                           'predicate': {'minecraft:nbt': '{Tags:["bm.lep"]}'}}]}}}, 'goal')
    adv('defend', 'invasion', 'donadian_medal', 'Hold the Line', 'Defend a Donadian mothership from all three Vorn waves', granted, 'goal')
    adv('reactor', 'invasion', 'warlord_banner', 'Meltdown', "Sabotage a Vorn Dreadnought's reactor", granted, 'challenge')
    adv('jammer', 'invasion', 'signal_jammer', 'Radio Silence', 'Switch on a Signal Jammer', granted)
    wjson('bm/advancement/p52/happy_trade.json', {'criteria': {'t': {'trigger': 'minecraft:villager_trade'}}, 'rewards': {'function': 'bm:p52/happy_trade'}})
    fn('p52/happy_trade', ['advancement revoke @s only bm:p52/happy_trade', 'execute if score #lnight bm.bm matches 1 run advancement grant @s only bm:story/happy_hour'])

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


# ===================================================================== resource pack
def icons():
    import vanilla as v
    from PIL import Image
    def grid(rows, pal):
        im = Image.new('RGBA', (16, 16))
        for y, r in enumerate(rows):
            for x, c in enumerate(r):
                if c != '.': im.putpixel((x, y), v._hex(pal[c]))
        return im
    clover = lambda: grid(['................', '.....GG..GG.....', '....GLLGGLLG....', '....GLGGGGLG....', '.....GGGGGG.....', '..GG.GGGGGG.GG..',
                           '.GLLGGGggGGGLLG.', '.GLGGGgggGGGGLG.', '.GLGGGgggGGGGLG.', '.GLLGGGggGGGLLG.', '..GG.GGGGGG.GG..', '.....GGGGGG.....',
                           '....GLGGGGLG....', '....GLLGGLLG....', '.....GG.dGG.....', '........d.......'],
                          {'G': '#3a9a3a', 'L': '#7ad86a', 'g': '#1e6a2a', 'd': '#3a5a2a'})
    pot = lambda: grid(['................', '....YYyYYyY.....', '...YyYYyYYyY....', '..YYYyYYYyYYY...', '..KKKKKKKKKKKK..', '.KkkkkkkkkkkkkK.',
                        '.KkkkkkkkkkkkkK.', '..KkkkkkkkkkkK..', '..KkkkkkkkkkkK..', '..KkkkkkkkkkkK..', '...KkkkkkkkkK...', '....KKKKKKKK....',
                        '................', '................', '................', '................'],
                       {'Y': '#ffd23f', 'y': '#fff3a0', 'K': '#1a1a1e', 'k': '#3a3a44'})
    medal = lambda: grid(['................', '......r..r......', '......rr.r......', '.......rr.......', '......TTTT......', '.....TttttT.....',
                          '....TttGGttT....', '....TtGGGGtT....', '....TtGGGGtT....', '....TttGGttT....', '.....TttttT.....', '......TTTT......',
                          '................', '................', '................', '................'],
                         {'r': '#c83030', 'T': '#1e8a80', 't': '#3ad8c8', 'G': '#7dff6a'})
    jammer = lambda: grid(['...........k....', '...........k....', '..........kk....', '..........k.....', '...KKKKKKKKKK...', '...KggggggggK...',
                           '...KgLLggLLgK...', '...KggggggggK...', '...KgRggggggK...', '...KggggggggK...', '...KKKKKKKKKK...', '................',
                           '................', '................', '................', '................'],
                          {'k': '#3a3a44', 'K': '#2a2c30', 'g': '#7a8a9c', 'L': '#7dff6a', 'R': '#ff4a4a'})
    flak = lambda: v.recolor_where(v._load(v.V + 'firework_rocket.png'), lambda c: v._hsv(c)[1] > 0.3, [v._hex(h) for h in ('#7a2a10', '#d85a20', '#ff9a4a')])
    return {'four_leaf_charm': clover, 'pot_of_gold': pot, 'donadian_medal': medal, 'signal_jammer': jammer, 'flak_rocket': flak}


def rp(R):
    import vanilla
    from PIL import Image
    for k, f in icons().items():
        R.ICONS[k] = Image.new('RGBA', (16, 16))
        vanilla.OVERRIDES[k] = f

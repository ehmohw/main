"""Phase 1.18 (part 3): THE DARK AUCTION.

Every 7th in-game night (day % 7 == 6) and every Blood Moon night, the Auction Hall's doors open at 17000 and the
Auctioneer calls the first of five lots at midnight (18000). Each lot sells when a 10-second countdown runs out with no
new bid; every bid restarts it. Silver Key or better walks in through the gate ledger; anyone else can buy a one-night
pass there for 2 Medallions while the doors are open. Operators: /function bm:admin/auction_now (and auction_stop).

Bidding: right-click the Bidding Paddle handed out at the door (or the ledger on the podium): +1 / +2 / +5 / +10
Medallions over the current bid (the first bid opens at the lot's price). Medallions are paid the moment you bid -
from your inventory, then your Rat Bank balance, then Trophies broken into 6 (change handed back) - and held in
ESCROW, a score against your name. Outbid: refunded at once, or the next time you're online. Win: escrow spent, lot
delivered (on your next login if you left). A crash, restart or /reload mid-sale refunds everyone and returns the lot.

Rival bidders (Lord Squeakington, Madame Nibbles, the Gentleman in Grey) hold a hidden reserve of 0.8-1.3x a lot's
value (value = twice its opening bid) and may raise by 1-2 in the last 3 seconds while the price is under it. A rival
win refunds everyone and returns the lot to the pool. The headline lot (*) is always called last; one-per-world lots
leave the pool for good; one-per-player lots refuse a second bid from a past winner; relic cosmetics show up in about
one sale in three. Importing registers the paddle; generate(G) runs after phase29.generate."""
from nbt import snbt, B, F, Int
from items import item, T, TOTEM, ITEMS
import mgeo
import market2

W, BF = market2.W, market2.BF
item('bidding_paddle', 'minecraft:carrot_on_a_stick', 'Bidding Paddle', '#c0392b',
     ['Raise it and the Auctioneer sees you.', ('Right-click: open the bidding menu.', 'blue'), ('Only works inside the Auction Hall.', 'gray'),
      ('(It stays at the door when you leave.)', 'dark_gray')], model='bm:bidding_paddle', stack=1, cat='misc',
     comps={'minecraft:unbreakable': {}, 'minecraft:tooltip_display': {'hidden_components': ['minecraft:unbreakable']}})

# (id, name, colour, kind, opening bid, limit, give: [(what, count)], phase2 only)
LOTS = [
    ('wings_rat_king', 'Wings of the Rat King', '#ffb300', 'head', 40, 'world', [('wings_rat_king', 1)], False),
    ('merc_contract', 'Mercenary Contract', '#c0392b', 'head', 35, 'player', [('merc_contract', 1)], False),
    # 2.13: on the Phase 2 build the Golden Donado left the Auction - it is found in the Gilded Roost ('base': base pack only)
    ('golden_donado', 'Golden Donado', '#ffd700', 'head', 30, 'world', [('golden_donado', 1)], 'base'),
    ('ring_burrows', 'Ring of Three Burrows', '#d4a35a', 'head', 30, 'player', [('ring_burrows', 1)], False),
    ('pocket_rift', 'Pocket Rift', '#4fd6c4', 'head', 25, None, [('pocket_rift', 1)], False),
    ('rat_king_signet', "Rat King's Signet", '#ffb300', 'head', 25, 'world', [('rat_king_signet', 1)], False),
    ('auroral_crown', 'Auroral Crown', '#7fffd4', 'relic', 20, None, [('auroral_crown', 1)], False),
    ('brass_wing_scroll', 'Brass Wing Scroll', '#c8963c', 'relic', 18, None, [('brass_wing_scroll', 1)], False),
    ('rat_familiar', 'Rat Familiar', '#b0b0b8', 'relic', 18, None, [('rat_familiar', 1)], False),
    ('bloomwalker_boots', 'Bloomwalker Boots', '#7ccf5a', 'relic', 15, None, [('bloomwalker_boots', 1)], False),
    ('showstopper_charm', 'Showstopper Charm', '#ffd700', 'relic', 15, None, [('showstopper_charm', 1)], False),
    ('market_crest_scroll', 'Market Crest Scroll', '#ffcf3f', 'relic', 12, None, [('market_crest_scroll', 1)], False),
    ('smuggler_jar', "Smuggler's Jar", '#9fd1b0', 'reg', 15, None, [('smuggler_jar', 1)], False),
    ('spawner_crowbar', 'Spawner Crowbar', '#8a8a96', 'reg', 12, None, [('spawner_crowbar', 1)], False),
    ('lodestone_locket', 'Lodestone Locket', '#b0a0d0', 'reg', 10, None, [('lodestone_locket', 1)], False),
    ('donado_trophy', 'Donado Trophy', '#e8d29a', 'reg', 10, None, [('donado_trophy', 1)], False),
    ('heartstones', 'Heartstone Trio', 'red', 'reg', 18, None, [('heartstone', 3)], False),
    ('egapples', '2 Enchanted Golden Apples', 'gold', 'reg', 12, None, [('minecraft:enchanted_golden_apple', 2)], False),
    ('totems', '2 Totems of Undying', 'gold', 'reg', 10, None, [('minecraft:totem_of_undying', 2)], False),
    ('templates', '2 Netherite Upgrade Templates', 'dark_gray', 'reg', 10, None, [('minecraft:netherite_upgrade_smithing_template', 2)], False),
    ('jackpot_cards', '3 Jackpot Scratch Cards', 'gold', 'reg', 9, None, [('jackpot_card_5', 3)], False),
    ('skulls', '3 Wither Skeleton Skulls', 'dark_gray', 'reg', 8, None, [('minecraft:wither_skeleton_skull', 3)], False),
    ('explorer_map', "Sealed Explorer's Map", 'aqua', 'reg', 8, None, [('sealed_explorer_map', 1)], False),
    ('portrait', 'Rat Gang Portrait', '#c8a050', 'reg', 6, None, [('rat_gang_portrait', 1)], False),
    ('bell', 'Fair Weather Bell', '#ffe08a', 'reg', 8, None, [('fair_weather_bell', 1)], False),
    ('bank_card', "Banker's Card", '#e8d27a', 'reg', 8, None, [('bankers_card', 1)], False),
    ('boss_key', 'Next Boss Key', '#a96bff', 'reg', 20, None, [('next_boss_key', 1)], True),
]
RIVALS = [('Lord Squeakington', 'lord', (32.5, W + 1.25, 8.5)), ('Madame Nibbles', 'madame', (42.5, W + 1.25, 8.5)),     # 2.13: on cushions
          ('The Gentleman in Grey', 'grey', (33.5, W + 2.25, 10.5))]
HALL_C = (37.5, W + 1, 7.0)
HALL_R = 8.0
CALL = ['“Next, from a very private collection...”', '“Fresh off the boat, no questions asked...”', '“A rare one, friends. Bid like you mean it.”',
        '“Feast your whiskers on this...”', '“Our pride and joy. The last lot of the night!”']


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    import phase28 as P28
    tick, fast, second, load = [], [], [], []
    ident = [F(0), F(0), F(0), F(1)]
    lots = [l for l in LOTS if (G.PHASE2 and l[7] != 'base') or (not G.PHASE2 and l[7] is not True)]
    N = len(lots)
    G.P30_LOTS = lots

    objs = ['bm.auc dummy', 'bm.escrow dummy', 'bm.apass dummy']
    load += [f'scoreboard objectives add {o}' for o in objs] + [
        'bossbar add bm:auction "Dark Auction"', 'bossbar set bm:auction color red', 'bossbar set bm:auction max 200', 'bossbar set bm:auction style notched_10',
        # a crash, restart or /reload mid-sale: everyone is refunded (the settle loop), the lot goes back into the pool
        'execute if score #state bm.auc matches 2.. run function bm:p30/abort',
        'execute unless score #pgen bm.auc matches 0.. run scoreboard players set #pgen bm.auc 0',
        'scoreboard players set #usebank bm.pay 0', 'scoreboard players set #2 bm.auc 2', 'scoreboard players set #7 bm.auc 7',
        'scoreboard players set #30 bm.auc 30', 'scoreboard players set #20 bm.auc 20', 'scoreboard players set #10 bm.auc 10']
    G.FUNCS['admin/uninstall'][-1:-1] = ['bossbar remove bm:auction', 'scoreboard objectives remove bm.auc', 'scoreboard objectives remove bm.escrow']

    # ------------------------------------------------------------------ the hall: auctioneer, pedestal, price board, rivals, podium ledger
    place = G.P28_PLACE
    fin = 'execute rotated ~ 0 run tp @e[tag=bm.n18,distance=..1.5] ~ ~ ~ ~ ~'
    untag = 'tag @e[tag=bm.n18,distance=..1.5] remove bm.n18'
    fn('p30/spawn/hall', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.e18","bm.ahall"]}'])
    place(HALL_C, 0, 'p30/spawn/hall', 'auction hall centre', air_only=True)
    rat = G.rat_sprite('bm:rat_auction', ['bm.e18', 'bm.n18', 'bm.rat_sprite', 'bm.auctioneer'])
    bub = {'Tags': ['bm.e18', 'bm.n18', 'bm.abubble'], 'billboard': 'center', 'view_range': F(0.5), 'default_background': B(0), 'background': Int(0x90000000 - (1 << 32)),
           'line_width': Int(170), 'text': T('"Welcome, welcome. Tonight\'s sale begins at midnight."', 'white', italic=True),
           'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(1.45), F(0)], 'scale': [F(0.5)] * 3}}
    fn('p30/spawn/auctioneer', [rat, f'summon minecraft:text_display ~ ~ ~ {snbt(bub)}', fin, untag])
    place((35.5, W + 1, 3.5), 0, 'p30/spawn/auctioneer', 'the Auctioneer', air_only=True)
    ped = {'Tags': ['bm.e18', 'bm.n18', 'bm.apedestal'], 'item_display': 'ground', 'billboard': 'fixed', 'teleport_duration': Int(3),
           'brightness': {'block': Int(15), 'sky': Int(15)}, 'glow_color_override': Int(0xFFD700),
           'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.25), F(0)], 'scale': [F(0.8)] * 3}}
    fn('p30/spawn/pedestal', [f'summon minecraft:item_display ~ ~ ~ {snbt(ped)}', fin, untag])
    place((37.5, W + 2.05, 3.5), 0, 'p30/spawn/pedestal', 'the lot pedestal', air_only=True)
    board = {'Tags': ['bm.e18', 'bm.n18', 'bm.aboard'], 'billboard': 'fixed', 'line_width': Int(220), 'default_background': B(0),
             'background': Int(0xC0100008 - (1 << 32)), 'brightness': {'block': Int(15), 'sky': Int(15)},
             'text': [T('THE DARK AUCTION\n', 'gold', bold=True), T('Next sale: ', 'gray'), T('see the sign at the gate', 'white')],
             'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0), F(0)], 'scale': [F(0.7)] * 3}}
    fn('p30/spawn/board', [f'summon minecraft:text_display ~ ~ ~ {snbt(board)}', fin, untag])
    place((37.5, W + 3.05, 2.3), 0, 'p30/spawn/board', 'the price board', air_only=True)
    for i, (nm, v, pos) in enumerate(RIVALS, 1):
        r = G.rat_sprite(f'bm:rat_{v}', ['bm.e18', 'bm.n18', 'bm.rat_sprite', 'bm.arival', f'bm.arival{i}'], 0.75)
        plate = {'Tags': ['bm.e18', 'bm.n18', 'bm.arplate'], 'billboard': 'center', 'view_range': F(0.2), 'default_background': B(0), 'background': Int(0x60000000),
                 'text': T(nm, 'gray', italic=True), 'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(1.0), F(0)], 'scale': [F(0.4)] * 3}}
        fn(f'p30/spawn/rival{i}', [r, f'summon minecraft:text_display ~ ~ ~ {snbt(plate)}', fin, untag])
        c = mgeo.cell(pos)                     # 2.13: they sit on a cushion seat (an open cell over a solid step)
        if (c[0], c[1], c[2]) not in [(x, y, z) for (x, y, z) in market2.AUCTION_SEATS] or not mgeo.passable(c) or not mgeo.standable((c[0], c[1] - 1, c[2])):
            raise SystemExit(f'phase30: rival seat {pos} is not a cushion seat ({mgeo.st(c)})')
        place(pos, 180, f'p30/spawn/rival{i}', f'rival {nm}')
    # the podium ledger (bids without a paddle)
    G.FUNCS['p28/ledger/open'].append('execute if score #lg bm.pay matches 31 run return run function bm:p30/menu')
    book = {'Tags': ['bm.e18', 'bm.n18', 'bm.lg_book'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:statue_ledger'}},
            'item_display': 'fixed', 'billboard': 'fixed', 'brightness': {'block': Int(12), 'sky': Int(10)},
            'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.25), F(0)], 'scale': [F(0.5)] * 3}}
    box = {'Tags': ['bm.e18', 'bm.n18', 'bm.ledger'], 'response': B(1), 'width': F(0.7), 'height': F(0.4)}
    fn('p28/spawn/lg_31', [f'summon minecraft:item_display ~ ~ ~ {snbt(book)}', f'summon minecraft:interaction ~ ~ ~ {snbt(box)}',
                           'scoreboard players set @e[type=minecraft:interaction,tag=bm.n18,distance=..1.5] bm.lgid 31', fin, untag])
    place((39.5, W + 1, 3.5), 0, 'p28/spawn/lg_31', 'the podium ledger', air_only=True)

    # ------------------------------------------------------------------ who is in the hall (each second) + paddles
    second += ['tag @a remove bm.inhall',
               f'execute as @e[type=minecraft:marker,tag=bm.ahall] at @s run tag @a[distance=..{HALL_R}] add bm.inhall',
               'bossbar set bm:auction players @a[tag=bm.inhall]',
               'execute if score #state bm.auc matches 1..3 as @a[tag=bm.inhall,tag=!bm.gotpad,gamemode=!spectator] unless items entity @s container.* *[minecraft:custom_data~{bm:"bidding_paddle"}] unless items entity @s weapon.offhand *[minecraft:custom_data~{bm:"bidding_paddle"}] run function bm:p30/paddle',
               'execute as @e[type=minecraft:item] if items entity @s contents *[minecraft:custom_data~{bm:"bidding_paddle"}] run kill @s',
               'tag @a[tag=bm.gotpad,tag=!bm.inhall] remove bm.gotpad',
               'execute as @a[tag=!bm.inhall] run clear @s *[minecraft:custom_data~{bm:"bidding_paddle"}]',
               'execute unless score #state bm.auc matches 1..3 run clear @a *[minecraft:custom_data~{bm:"bidding_paddle"}]']
    fn('p30/paddle', ['tag @s add bm.gotpad', give('bidding_paddle'), title('@s', 'actionbar', T('A Bidding Paddle is pressed into your paw. Right-click it to bid.', 'gold'))])
    fn('p30/enter', ['execute if score #state bm.auc matches 1..3 unless items entity @s container.* *[minecraft:custom_data~{bm:"bidding_paddle"}] run function bm:p30/paddle',
                     'execute if score #state bm.auc matches 1 run ' + tellraw('@s', PREFIX + [T('Take a seat. The first lot is called at midnight.', 'gray')])])
    fn('p30/leave', ['clear @s *[minecraft:custom_data~{bm:"bidding_paddle"}]'])
    G.FUNCS['p21/grap/use'][1:1] = ['execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"bidding_paddle"}] run return run function bm:p30/menu']

    # ------------------------------------------------------------------ schedule: the sign, the warning, doors, start
    sch = ['scoreboard players operation #wk bm.auc = #day bm.bm', 'scoreboard players operation #wk bm.auc %= #7 bm.auc',
           'scoreboard players set #tonight bm.auc 0',
           'execute if score #wk bm.auc matches 6 run scoreboard players set #tonight bm.auc 1',
           'execute if score #bday bm.bm matches 1 run scoreboard players set #tonight bm.auc 1',
           # a sale night slept through (the clock jumped past it) is held the next night instead
           'execute unless score #lastday bm.auc = #day bm.bm run function bm:p30/day_change',
           'execute if score #owed bm.auc matches 1 run scoreboard players set #tonight bm.auc 1',
           'execute if score #state bm.auc matches 0 if score #tonight bm.auc matches 1 if score #tod bm.bm matches 17000..17999 unless score #saled bm.auc = #day bm.bm run function bm:p30/doors',
           'execute if score #state bm.auc matches 1 if score #tod bm.bm matches 18000.. run function bm:p30/start',
           'execute if score #state bm.auc matches 1 if score #tod bm.bm matches ..16999 run function bm:p30/start',
           # warning: the day before an auction night, once
           'execute if score #tod bm.bm matches 1000..1999 unless score #warnd bm.auc = #day bm.bm run function bm:p30/warn',
           # the gate sign: days until the next sale
           'function bm:p30/sign_calc',
           'execute as @e[type=minecraft:marker,tag=bm.mkt,tag=bm.i18] at @s rotated as @s unless score @s bm.auc = #signv bm.auc run function bm:p30/sign']
    fn('p30/schedule', sch)
    second.append('function bm:p30/schedule')
    fn('p30/day_change', ['execute unless score #lastday bm.auc matches 0.. run return run scoreboard players operation #lastday bm.auc = #day bm.bm',
                          'scoreboard players operation #a bm.auc = #lastday bm.auc', 'scoreboard players operation #a bm.auc %= #7 bm.auc',
                          'scoreboard players operation #b bm.auc = #lastday bm.auc', 'scoreboard players operation #b bm.auc %= #30 bm.auc',
                          'execute if score #a bm.auc matches 6 unless score #saled bm.auc = #lastday bm.auc run scoreboard players set #owed bm.auc 1',
                          'execute if score #b bm.auc matches 29 unless score #saled bm.auc = #lastday bm.auc run scoreboard players set #owed bm.auc 1',
                          'scoreboard players operation #lastday bm.auc = #day bm.bm'])
    fn('p30/warn', ['scoreboard players operation #warnd bm.auc = #day bm.bm',
                    'scoreboard players operation #n bm.auc = #day bm.bm', 'scoreboard players add #n bm.auc 1',
                    'scoreboard players operation #m bm.auc = #n bm.auc', 'scoreboard players operation #m bm.auc %= #7 bm.auc',
                    'scoreboard players operation #n bm.auc %= #30 bm.auc',
                    'execute if score #m bm.auc matches 6 run return run function bm:p30/warn_say',
                    'execute if score #n bm.auc matches 29 run function bm:p30/warn_say'])
    fn('p30/warn_say', [tellraw('@a[scores={bm.tier=2..}]', PREFIX + [T('The Dark Auction opens ', 'gray'), T('tomorrow at midnight', 'gold', bold=True),
                                                                        T('. Doors at dusk. Bring Medallions.', 'gray')])])
    # days until the next sale (weekly: day%7==6; Blood Moon: day%30==29). Tonight counts until the sale is done.
    fn('p30/sign_calc', [
        'scoreboard players operation #a bm.auc = #day bm.bm', 'scoreboard players operation #a bm.auc %= #7 bm.auc',
        'scoreboard players set #dw bm.auc 6', 'scoreboard players operation #dw bm.auc -= #a bm.auc',
        'scoreboard players operation #b bm.auc = #day bm.bm', 'scoreboard players operation #b bm.auc %= #30 bm.auc',
        'scoreboard players set #db bm.auc 29', 'scoreboard players operation #db bm.auc -= #b bm.auc',
        'scoreboard players operation #dn bm.auc = #dw bm.auc', 'scoreboard players operation #dn bm.auc < #db bm.auc',
        # tonight's sale already over: count from the next one
        'execute if score #dn bm.auc matches 0 if score #saled bm.auc = #day bm.bm if score #state bm.auc matches 0 run function bm:p30/sign_next',
        'scoreboard players operation #signv bm.auc = #dn bm.auc',
        'execute if score #state bm.auc matches 1..3 run scoreboard players set #signv bm.auc -1'])
    fn('p30/sign_next', ['execute if score #dw bm.auc matches 0 run scoreboard players set #dw bm.auc 7',
                         'execute if score #db bm.auc matches 0 run scoreboard players set #db bm.auc 30',
                         'scoreboard players operation #dn bm.auc = #dw bm.auc', 'scoreboard players operation #dn bm.auc < #db bm.auc'])
    sign_rel = mgeo.rel((37.5, W + 4.5, 15.5))
    if 'sign' not in mgeo.st((37, W + 4, 15)): raise SystemExit('phase30: the auction sign moved')
    fn('p30/sign', ['scoreboard players operation @s bm.auc = #signv bm.auc',
                    f'execute positioned {sign_rel} if score #signv bm.auc matches -1 run data modify block ~ ~ ~ front_text.messages[3] set value "NOW - come in!"',
                    f'execute positioned {sign_rel} if score #signv bm.auc matches 0 run data modify block ~ ~ ~ front_text.messages[3] set value "tonight!"',
                    f'execute positioned {sign_rel} if score #signv bm.auc matches 1 run data modify block ~ ~ ~ front_text.messages[3] set value "tomorrow."',
                    'execute store result storage bm:tmp sg.n int 1 run scoreboard players get #signv bm.auc',
                    f'execute positioned {sign_rel} if score #signv bm.auc matches 2.. run function bm:p30/sign_m with storage bm:tmp sg'])
    fn('p30/sign_m', ['$data modify block ~ ~ ~ front_text.messages[3] set value "in $(n) days."'])

    # ------------------------------------------------------------------ doors open / start / lots
    fn('p30/doors', ['scoreboard players set #state bm.auc 1', 'scoreboard players set #aopen bm.auc 1', 'scoreboard players operation #saled bm.auc = #day bm.bm',
                     'scoreboard players set #owed bm.auc 0',
                     tellraw('@a[scores={bm.tier=2..}]', PREFIX + [T("The Dark Auction's doors are open. ", 'gold', bold=True), T('First lot at midnight.', 'gray')]),
                     tellraw('@a[tag=bm.adv,scores={bm.tier=..1}]', PREFIX + [T('The Dark Auction is open tonight. No key? A one-night pass is sold at the gate.', 'gray')]),
                     'function bm:p30/bub {t:"“Doors are open! Find a seat. We begin at midnight.”"}'])
    G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/auction_now', 'yellow'), T('  starts a Dark Auction right away (and auction_stop)', 'gray')]))
    fn('admin/auction_now', ['execute if score #state bm.auc matches 2..3 run return run ' + tellraw('@s', PREFIX + [T('A sale is already running.', 'gray')]),
                             'scoreboard players operation #saled bm.auc = #day bm.bm', 'scoreboard players set #aopen bm.auc 1',
                             'function bm:p30/start', tellraw('@s', PREFIX + [T('Dark Auction started.', 'gray')])])
    fn('admin/auction_stop', ['function bm:p30/abort', tellraw('@s', PREFIX + [T('Dark Auction stopped; every bid refunded.', 'gray')])])
    fn('p30/abort', ['scoreboard players set #state bm.auc 0', 'scoreboard players set #aopen bm.auc 0', 'scoreboard players set #hb bm.auc 0',
                     'scoreboard players set #usebank bm.pay 0', 'bossbar set bm:auction visible false',
                     'data remove storage bm:auction sale', 'function bm:p30/ped_clear', 'scoreboard players add #pgen bm.auc 1',
                     tellraw('@a[scores={bm.escrow=1..}]', PREFIX + [T('The Dark Auction was interrupted. Your Medallions come straight back.', 'gray')])])
    # draw: one headline (last), a relic cosmetic about one sale in three, regular lots for the rest; no repeats
    heads = [i for i, l in enumerate(lots) if l[3] == 'head']
    relics = [i for i, l in enumerate(lots) if l[3] == 'relic']
    regs = [i for i, l in enumerate(lots) if l[3] == 'reg']
    st = ['scoreboard players set #state bm.auc 2', 'scoreboard players set #aopen bm.auc 1', 'scoreboard players set #lotn bm.auc 0',
          'data modify storage bm:auction sale set value []'] + [f'scoreboard players set #pk{i} bm.auc 0' for i in range(N)]
    st += ['scoreboard players set #want bm.auc 3', 'function bm:p30/draw_reg']
    st += ['execute store result score #r bm.auc run random value 1..3', 'execute if score #r bm.auc matches 1 run function bm:p30/draw_relic',
           'execute unless score #r bm.auc matches 1 run function bm:p30/draw_one_reg',
           'function bm:p30/draw_head', 'function bm:p30/next']
    fn('p30/start', st)

    def picker(name, pool):
        lines = ['scoreboard players set #got bm.auc 0', 'scoreboard players set #try bm.auc 0', f'function bm:p30/{name}_try']
        fn(f'p30/{name}', lines)
        tr = ['scoreboard players add #try bm.auc 1', f'execute store result score #r bm.auc run random value 0..{len(pool) - 1}']
        tr += [f'execute if score #r bm.auc matches {k} run function bm:p30/pick {{i:{i}}}' for k, i in enumerate(pool)]
        tr += [f'execute if score #got bm.auc matches 0 if score #try bm.auc matches ..60 run function bm:p30/{name}_try']
        fn(f'p30/{name}_try', tr)
    picker('draw_one_reg', regs)
    picker('draw_relic', relics)
    picker('draw_head', heads)
    fn('p30/draw_reg', ['function bm:p30/draw_one_reg', 'scoreboard players remove #want bm.auc 1',
                        'execute if score #want bm.auc matches 1.. run function bm:p30/draw_reg'])
    G.FUNCS['p30/draw_relic'].append('execute if score #got bm.auc matches 0 run function bm:p30/draw_one_reg')
    G.FUNCS['p30/draw_head'].append('execute if score #got bm.auc matches 0 run function bm:p30/draw_one_reg')
    fn('p30/pick', ['$execute if score #pk$(i) bm.auc matches 1 run return 0', '$execute if score #sold$(i) bm.auc matches 1 run return 0',
                    '$scoreboard players set #pk$(i) bm.auc 1', '$data modify storage bm:auction sale append value $(i)', 'scoreboard players set #got bm.auc 1'])
    load += [f'execute unless score #sold{i} bm.auc matches 0.. run scoreboard players set #sold{i} bm.auc 0' for i in range(N)]

    # call the next lot (or close)
    fn('p30/next', ['scoreboard players set #hb bm.auc 0', 'scoreboard players set #price bm.auc 0',
                    'execute unless data storage bm:auction sale[0] run return run function bm:p30/close',
                    'execute store result score #lot bm.auc run data get storage bm:auction sale[0]', 'data remove storage bm:auction sale[0]',
                    'scoreboard players add #lotn bm.auc 1', 'scoreboard players set #state bm.auc 2', 'scoreboard players set #cd bm.auc 200',
                    'data modify storage bm:auction cur.who set value "no bids yet"'] +
       [f'execute if score #lot bm.auc matches {i} run function bm:p30/lot/show_{i}' for i in range(N)] +
       ['execute store result score #rr bm.auc run random value 80..130', 'scoreboard players operation #reserve bm.auc = #open bm.auc',
        'scoreboard players operation #reserve bm.auc *= #2 bm.auc', 'scoreboard players operation #reserve bm.auc *= #rr bm.auc',
        'scoreboard players operation #reserve bm.auc /= #100 bm.pay',
        'bossbar set bm:auction visible true', 'bossbar set bm:auction value 200',
        'function bm:p30/board',
        'execute as @e[type=minecraft:item_display,tag=bm.auctioneer] at @s run playsound minecraft:block.anvil.place neutral @a[distance=..24] ~ ~ ~ 0.4 1.8',
        'title @a[tag=bm.inhall] times 5 50 10'])
    for i, (lid, nm, col, kind, opn, lim, gv, p2) in enumerate(lots):
        disp_item = G.stack(gv[0][0], gv[0][1]) if gv[0][0] in ITEMS else {'id': gv[0][0] if ':' in gv[0][0] else 'minecraft:' + gv[0][0], 'count': Int(gv[0][1])}
        if gv[0][0] == 'next_boss_key': disp_item = {'id': 'minecraft:trial_key', 'count': Int(1)}
        call = CALL[4] if kind == 'head' else CALL[i % 4]
        tag = {'head': '★ ', 'relic': '✿ ', 'reg': ''}[kind]
        fn(f'p30/lot/show_{i}', [f'data modify storage bm:auction cur merge value {snbt({"name": tag + nm, "col": col, "open": opn})}',
                                 f'scoreboard players set #open bm.auc {opn}',
                                 f'execute as @e[type=minecraft:item_display,tag=bm.apedestal] run data modify entity @s item set value {snbt(disp_item)}',
                                 'execute as @e[type=minecraft:item_display,tag=bm.apedestal] run data modify entity @s Glowing set value 1b',
                                 title('@a[tag=bm.inhall]', 'subtitle', [T(f'opening at {opn} Medallions', 'gray')]),
                                 title('@a[tag=bm.inhall]', 'title', T(tag + nm, col, bold=True)),
                                 tellraw('@a[tag=bm.inhall]', PREFIX + [T('Lot ', 'gray'), {'score': {'name': '#lotn', 'objective': 'bm.auc'}, 'color': 'white'},
                                                                        T(': ', 'gray'), T(tag + nm, col, bold=True), T(f' - opening at {opn} Medallions.', 'gray')]),
                                 'function bm:p30/bub {t:"%s"}' % call])
        give_l = []
        for what, n in gv:
            if what == 'next_boss_key': give_l.append('function bm:p30/bosskey')
            elif what in ITEMS: give_l.append(give(what, n))
            else: give_l.append(f'give @s {what if ":" in what else "minecraft:" + what} {n}')
        if lim == 'world': give_l.append(f'scoreboard players set #sold{i} bm.auc 1')
        if lim == 'player': give_l.append(f'tag @s add bm.won_{lid}')
        fn(f'p30/lot/give_{i}', give_l)
    if G.PHASE2:
        from p2.config import ORDER, D
        bk = []
        for idx, d in enumerate(ORDER):
            key = D[d]['key'] or 'hollow_summons'
            bk.append(f'execute if score @s bm.conq matches {idx} run return run ' + give(key))
        bk.append(give('hollow_summons'))
        fn('p30/bosskey', ['execute unless score @s bm.conq matches 0.. run scoreboard players set @s bm.conq 0'] + bk)
    fn('p30/ped_clear', ['execute as @e[type=minecraft:item_display,tag=bm.apedestal] run data remove entity @s item'])
    fn('p30/close', ['scoreboard players set #state bm.auc 0', 'scoreboard players set #aopen bm.auc 0', 'scoreboard players set #hb bm.auc 0',
                     'scoreboard players set #usebank bm.pay 0', 'bossbar set bm:auction visible false', 'function bm:p30/ped_clear',
                     'scoreboard players add #pgen bm.auc 1', 'tag @a remove bm.gotpad',
                     'function bm:p30/bub {t:"“That\'s the last lot, friends. Mind the step on your way out.”"}',
                     tellraw('@a[tag=bm.inhall]', PREFIX + [T('The Dark Auction is closed for tonight.', 'gray')]),
                     'execute as @e[type=minecraft:text_display,tag=bm.aboard] run data modify entity @s text set value ' +
                     snbt([T('THE DARK AUCTION\n', 'gold', bold=True), T('Closed for tonight.', 'gray')])])

    # ------------------------------------------------------------------ the countdown (only ticks during a lot)
    tick.append('execute if score #state bm.auc matches 2..3 run function bm:p30/tick')
    fn('p30/tick', ['execute if score #state bm.auc matches 3 run return run function bm:p30/pause',
                    'scoreboard players remove #cd bm.auc 1',
                    'execute store result bossbar bm:auction value run scoreboard players get #cd bm.auc',
                    'scoreboard players operation #s bm.auc = #cd bm.auc', 'scoreboard players operation #s bm.auc %= #20 bm.auc',
                    'execute if score #s bm.auc matches 0 run function bm:p30/each_second',
                    'execute as @e[type=minecraft:item_display,tag=bm.apedestal] at @s run tp @s ~ ~ ~ ~4 0',
                    'execute if score #cd bm.auc matches ..0 run function bm:p30/sold'])
    fn('p30/each_second', ['function bm:p30/board',
                           'execute if score #cd bm.auc matches 60 run function bm:p30/going {t:"Going once..."}',
                           'execute if score #cd bm.auc matches 40 run function bm:p30/going {t:"Going twice..."}',
                           'execute if score #cd bm.auc matches 20 run function bm:p30/going {t:"Last call!"}',
                           'execute if score #cd bm.auc matches 20..60 if score #price bm.auc < #reserve bm.auc run function bm:p30/rival_maybe'])
    fn('p30/going', ['$title @a[tag=bm.inhall] actionbar {text:"$(t)",color:"gold",bold:true}',
                     'execute as @e[type=minecraft:item_display,tag=bm.auctioneer] at @s run playsound minecraft:block.wooden_button.click_on neutral @a[distance=..24] ~ ~ ~ 1 0.6',
                     '$function bm:p30/bub {t:"“$(t)”"}'])
    fn('p30/pause', ['scoreboard players remove #cd bm.auc 1', 'execute if score #cd bm.auc matches ..0 run function bm:p30/next'])

    # ------------------------------------------------------------------ rivals
    fn('p30/rival_maybe', ['execute store result score #r bm.auc run random value 1..100', 'execute if score #r bm.auc matches 51.. run return 0',
                           'execute if score #hb bm.auc matches ..-1 if score #r bm.auc matches 26.. run return 0',
                           'execute store result score #who bm.auc run random value 1..3',
                           'execute if score #who bm.auc = #rival bm.auc run scoreboard players add #who bm.auc 1',
                           'execute if score #who bm.auc matches 4 run scoreboard players set #who bm.auc 1',
                           'execute store result score #inc bm.auc run random value 1..2',
                           'scoreboard players operation #new bm.auc = #price bm.auc', 'scoreboard players operation #new bm.auc += #inc bm.auc',
                           'execute if score #hb bm.auc matches 0 run scoreboard players operation #new bm.auc = #open bm.auc',
                           'scoreboard players operation #prev bm.auc = #hb bm.auc',
                           'scoreboard players operation #price bm.auc = #new bm.auc', 'scoreboard players operation #rival bm.auc = #who bm.auc',
                           'scoreboard players set #hb bm.auc 0', 'scoreboard players operation #hb bm.auc -= #who bm.auc',
                           'execute if score #prev bm.auc matches 1.. as @e[type=minecraft:player] if score @s bm.pid = #prev bm.auc at @s run function bm:p30/outbid',
                           'scoreboard players set #cd bm.auc 200'] +
       [f'execute if score #who bm.auc matches {i} run function bm:p30/rival_say {{n:"{nm}",i:{i}}}' for i, (nm, v, pos) in enumerate(RIVALS, 1)] +
       ['function bm:p30/board'])
    fn('p30/rival_say', ['$data modify storage bm:auction cur.who set value "$(n)"',
                         '$execute as @e[type=minecraft:item_display,tag=bm.arival$(i)] at @s run particle minecraft:wax_on ~ ~1 ~ 0.3 0.4 0.3 0 12',
                         '$execute as @e[type=minecraft:item_display,tag=bm.arival$(i)] at @s run playsound minecraft:entity.silverfish.ambient neutral @a[distance=..24] ~ ~ ~ 1 1.6',
                         '$tellraw @a[tag=bm.inhall] [{text:"$(n)",color:"gray",italic:true},{text:" raises a paddle: ",color:"dark_gray"},{score:{name:"#price",objective:"bm.auc"},color:"light_purple"},{text:" Medallions.",color:"dark_gray"}]'])

    # ------------------------------------------------------------------ bidding (menu + /trigger buttons)
    dlg = P28.multi([T('The Dark Auction', 'gold', bold=True)],
                    [P28.body([T('Lot: ', 'gray'), T('$(name)', 'gold', bold=True)]),
                     P28.body([T('Current bid: ', 'gray'), T('$(price)', 'light_purple'), T(' Medallions  (', 'gray'), T('$(who)', 'white'), T(')', 'gray')]),
                     P28.body([T('Your bid in escrow: ', 'gray'), T('$(esc)', 'light_purple'), T('   Opening price: ', 'gray'), T('$(open)', 'white')]),
                     P28.body([T('Paid from your Medallions, then your Rat Bank, then Trophies (6 each, change returned). Outbid? Refunded at once.', 'dark_gray')], 300)],
                    [P28.btn([T('Bid +1', 'white')], 3101), P28.btn([T('Bid +2', 'white')], 3102), P28.btn([T('Bid +5', 'white')], 3105),
                     P28.btn([T('Bid +10', 'white')], 3110), P28.btn([T('Open the bidding', 'gold')], 3100, tooltip=T('Only while nobody has bid yet: bids the opening price.', 'gray'))],
                    columns=2, exit_label='Pass')
    fn('p30/menu', ['execute unless score #state bm.auc matches 2 run return run ' + title('@s', 'actionbar', T('No lot on the block right now.', 'gray')),
                    'execute unless entity @s[tag=bm.inhall] run return run ' + title('@s', 'actionbar', T('Bids are taken in the Auction Hall only.', 'gray')),
                    f'scoreboard players set @s bm.menu {P28.MENU["auction"]}',
                    'execute store result storage bm:auction cur.price int 1 run scoreboard players get #price bm.auc',
                    'execute store result storage bm:auction cur.esc int 1 run scoreboard players get @s bm.escrow',
                    'execute unless score @s bm.escrow matches 1.. run data modify storage bm:auction cur.esc set value 0',
                    'function bm:p30/menu_m with storage bm:auction cur'])
    fn('p30/menu_m', [f'$dialog show @s {P28.inline(dlg)}'])
    G.FUNCS['p28/act'].append('execute if score #act bm.pay matches 3100..3199 run return run function bm:p30/act')
    fn('p30/act', [f'execute unless score @s bm.menu matches {P28.MENU["auction"]} run return run function bm:p28/stale',
                   'execute unless score #state bm.auc matches 2 run return run ' + title('@s', 'actionbar', T('Too late - the gavel has fallen.', 'gray')),
                   'execute unless entity @s[tag=bm.inhall] run return run ' + title('@s', 'actionbar', T('Bids are taken in the Auction Hall only.', 'gray')),
                   'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                   'execute if score @s bm.escrow matches 1.. unless score @s bm.pid = #hb bm.auc run function bm:p30/settle'] +
       [f'execute if score #lot bm.auc matches {i} if entity @s[tag=bm.won_{l[0]}] run return run ' + title('@s', 'actionbar', T('One per customer - you already won one of these.', 'gray'))
        for i, l in enumerate(lots) if l[5] == 'player'] +
       ['scoreboard players operation #new bm.auc = #price bm.auc',
        'execute if score #act bm.pay matches 3100 unless score #hb bm.auc matches 0 run return run ' + title('@s', 'actionbar', T('Bidding is already open - raise instead.', 'gray')),
        'execute if score #act bm.pay matches 3100 run scoreboard players operation #new bm.auc = #open bm.auc',
        'execute if score #act bm.pay matches 3101..3110 if score #hb bm.auc matches 0 run scoreboard players operation #new bm.auc = #open bm.auc',
        'execute if score #act bm.pay matches 3101..3110 if score #hb bm.auc matches 0 run scoreboard players remove #new bm.auc 1',
        'execute if score #act bm.pay matches 3101 run scoreboard players add #new bm.auc 1',
        'execute if score #act bm.pay matches 3102 run scoreboard players add #new bm.auc 2',
        'execute if score #act bm.pay matches 3105 run scoreboard players add #new bm.auc 5',
        'execute if score #act bm.pay matches 3110 run scoreboard players add #new bm.auc 10',
        'execute unless score #act bm.pay matches 3100..3102 unless score #act bm.pay matches 3105 unless score #act bm.pay matches 3110 run return 0',
        'execute if score #new bm.auc < #open bm.auc run scoreboard players operation #new bm.auc = #open bm.auc',
        'execute unless score #hb bm.auc matches 0 unless score #new bm.auc > #price bm.auc run return 0',
        # what to pay now: the whole bid, or (raising your own) the difference
        'scoreboard players operation #need bm.pay = #new bm.auc',
        'execute unless score @s bm.escrow matches 0.. run scoreboard players set @s bm.escrow 0',
        'execute if score @s bm.pid = #hb bm.auc run scoreboard players operation #need bm.pay -= @s bm.escrow',
        'scoreboard players set #usebank bm.pay 1',
        'execute store result score #ok bm.pay run function bm:p28/pay/med_s',
        'scoreboard players set #usebank bm.pay 0',
        'execute if score #ok bm.pay matches 0 run return run function bm:p30/broke',
        'execute unless score @s bm.pid = #hb bm.auc run scoreboard players set @s bm.escrow 0',
        'scoreboard players operation @s bm.escrow = #new bm.auc',
        'scoreboard players operation #prev bm.auc = #hb bm.auc', 'scoreboard players operation #hb bm.auc = @s bm.pid',
        'scoreboard players operation #price bm.auc = #new bm.auc', 'scoreboard players set #cd bm.auc 200', 'scoreboard players set #rival bm.auc 0',
        'execute if score #prev bm.auc matches 1.. unless score #prev bm.auc = #hb bm.auc as @e[type=minecraft:player] if score @s bm.pid = #prev bm.auc at @s run function bm:p30/outbid',
        'function bm:p28/name/of', 'data modify storage bm:auction cur.who set from storage bm:tmp nm.name',
        'function bm:p30/board',
        tellraw('@a[tag=bm.inhall]', PREFIX + [{'selector': '@s', 'color': 'yellow'}, T(' bids ', 'gray'), {'score': {'name': '#price', 'objective': 'bm.auc'}, 'color': 'light_purple'},
                                               T(' Medallions!', 'gray')]),
        'playsound minecraft:entity.experience_orb.pickup player @a[tag=bm.inhall] ~ ~ ~ 0.5 1.6',
        'function bm:p30/menu'])
    fn('p30/broke', [title('@s', 'actionbar', T("You can't cover that bid. Nothing was taken.", 'red')), 'playsound minecraft:entity.villager.no player @s ~ ~ ~ 0.8 1'])
    # outbid / refunds: escrow back as Medallions (online now, or the next time they're seen)
    fn('p30/outbid', ['function bm:p30/refund', title('@s', 'actionbar', T("You've been outbid - your Medallions are back.", 'gold')),
                      'playsound minecraft:block.note_block.bass player @s ~ ~ ~ 1 0.8'])
    fn('p30/refund', ['execute unless score @s bm.escrow matches 1.. run return 0',
                      'execute store result storage bm:tmp rf2.n int 1 run scoreboard players get @s bm.escrow',
                      'scoreboard players set @s bm.escrow 0', 'function bm:p28/pay/give_med_n with storage bm:tmp rf2'])
    second.append('execute as @e[type=minecraft:player,scores={bm.escrow=1..}] unless score @s bm.pid = #hb bm.auc at @s run function bm:p30/settle')
    fn('p30/settle', ['execute store result storage bm:tmp st.pid int 1 run scoreboard players get @s bm.pid',
                      'execute store success score #pw bm.auc run function bm:p30/pending with storage bm:tmp st',
                      'execute if score #pw bm.auc matches 1 run return 0',
                      'function bm:p30/refund', tellraw('@s', PREFIX + [T('Your Dark Auction bid was returned to you.', 'gray')])])
    # a win while the winner was away: their escrow is spent and the lot handed over on their next visit
    fn('p30/pending', ['$execute unless data storage bm:auction pend.p$(pid) run return fail',
                       '$data modify storage bm:tmp pw set from storage bm:auction pend.p$(pid)',
                       '$data remove storage bm:auction pend.p$(pid)',
                       'scoreboard players set @s bm.escrow 0', 'function bm:p30/pend_give with storage bm:tmp pw', 'return 1'])
    fn('p30/pend_give', ['$function bm:p30/lot/give_$(lot)',
                         tellraw('@s', PREFIX + [T('While you were away, you won a lot at the Dark Auction. Here it is.', 'gold')])])
    # sold
    fn('p30/sold', ['scoreboard players set #state bm.auc 3', 'scoreboard players set #cd bm.auc 60',
                    'execute as @e[type=minecraft:item_display,tag=bm.auctioneer] at @s run playsound minecraft:block.anvil.land neutral @a[distance=..24] ~ ~ ~ 0.5 1.6',
                    'execute if score #hb bm.auc matches 0 run function bm:p30/unsold',
                    'execute if score #hb bm.auc matches ..-1 run function bm:p30/rival_won',
                    'execute if score #hb bm.auc matches 1.. run function bm:p30/player_won',
                    'execute as @e[type=minecraft:item_display,tag=bm.apedestal] run data modify entity @s Glowing set value 0b'])
    fn('p30/unsold', ['function bm:p30/bub {t:"“No takers? Back to the vault it goes.”"}',
                      tellraw('@a[tag=bm.inhall]', PREFIX + [T('No bids. The lot goes back to the vault.', 'gray')])])
    fn('p30/rival_won', ['function bm:p30/bub {t:"“SOLD! To the distinguished rodent in the stands.”"}',
                         tellraw('@a[tag=bm.inhall]', PREFIX + [T('SOLD to ', 'gray'), {'nbt': 'cur.who', 'storage': 'bm:auction', 'color': 'white', 'italic': True},
                                                                T(' for ', 'gray'), {'score': {'name': '#price', 'objective': 'bm.auc'}, 'color': 'light_purple'},
                                                                T(' Medallions. (It may turn up again.)', 'gray')])])
    fn('p30/player_won', ['scoreboard players set #here bm.auc 0',
                          'execute as @e[type=minecraft:player] if score @s bm.pid = #hb bm.auc at @s run function bm:p30/win_here',
                          'execute if score #here bm.auc matches 0 run function bm:p30/win_away',
                          'title @a[tag=bm.inhall] times 5 50 15', title('@a[tag=bm.inhall]', 'title', T('SOLD!', 'gold', bold=True)),
                          title('@a[tag=bm.inhall]', 'subtitle', [T('to ', 'gray'), {'nbt': 'cur.who', 'storage': 'bm:auction', 'color': 'yellow'},
                                                                  T(' for ', 'gray'), {'score': {'name': '#price', 'objective': 'bm.auc'}, 'color': 'light_purple'}]),
                          'function bm:p30/bub {t:"“SOLD! A pleasure doing business.”"}'])
    fn('p30/win_here', ['scoreboard players set #here bm.auc 1', 'scoreboard players set @s bm.escrow 0', 'function bm:p30/deliver',
                        'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1', 'particle minecraft:totem_of_undying ~ ~1 ~ 0.5 0.8 0.5 0.3 40'])
    fn('p30/win_away', ['execute store result storage bm:tmp wa.pid int 1 run scoreboard players get #hb bm.auc',
                        'execute store result storage bm:tmp wa.lot int 1 run scoreboard players get #lot bm.auc',
                        'function bm:p30/win_away_m with storage bm:tmp wa'] +
       [f'execute if score #lot bm.auc matches {i} run scoreboard players set #sold{i} bm.auc 1' for i, l in enumerate(lots) if l[5] == 'world'])
    fn('p30/win_away_m', ['$data modify storage bm:auction pend.p$(pid) set value {lot:$(lot)}'])
    fn('p30/deliver', [f'execute if score #lot bm.auc matches {i} run function bm:p30/lot/give_{i}' for i in range(N)])

    # ------------------------------------------------------------------ the board + the auctioneer's bubble
    fn('p30/board', ['execute store result storage bm:auction cur.price int 1 run scoreboard players get #price bm.auc',
                     'scoreboard players operation #secs bm.auc = #cd bm.auc', 'scoreboard players add #secs bm.auc 19', 'scoreboard players operation #secs bm.auc /= #20 bm.auc',
                     'execute store result storage bm:auction cur.secs int 1 run scoreboard players get #secs bm.auc',
                     'execute as @e[type=minecraft:text_display,tag=bm.aboard] run function bm:p30/board_m with storage bm:auction cur'])
    fn('p30/board_m', ['$data modify entity @s text set value [{text:"$(name)\\n",color:"$(col)",bold:true},{text:"Bid: ",color:"gray"},'
                       '{text:"$(price) Medallions\\n",color:"light_purple"},{text:"$(who)\\n",color:"white"},{text:"$(secs)s",color:"yellow"}]'])
    fn('p30/bub', ['$execute as @e[type=minecraft:text_display,tag=bm.abubble] run data modify entity @s text set value {text:"$(t)",color:"white",italic:true}'])

    G.FUNCS['load'][-1:-1] = load
    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second

"""Phase 1.18 (part 1): STANDING, the upgrading key, the members' gates and the back rooms - plus the plumbing the
Dark Auction (phase30) and the Gilded Gutter (phase31) share: menus (26.2 dialogs), `/trigger` buttons, payments that
match currency by its Black Market id only, a player-name resolver and the per-market runtime install.

STANDING is one market-wide reputation score per player. A purchase from a market trader earns its price in Token
value (Token 1, Lucky Token 5, Blood Moon Crystal 3, Medallion 9, Trophy 54), read from the game's villager_trade
advancement - no trader's offers are touched. Currency swaps and Old Barnaby's buy-backs earn nothing. Deeds: +20 a
finished Blood Bounty, +10 a Jackpot monster, +50 each first boss victory (Phase 2). Tiers: Stranger 0, Regular 150,
Associate 500, Partner 1,500, Family 4,000. `/trigger bm.standing` (no operator rights needed) opens your status.

THE KEY follows your tier: at Associate, Partner and Family any older Black Market key you carry turns into the Silver
Key, the Gold Key, then the Rat King's Key, in the same slot. The original key's item data is never edited; the three
new keys share the marker custom_data bm_key:1b, and the vault door accepts the old key OR that marker.

GATES: the Auction Hall and the Gilded Gutter keep their iron bars; a ledger at each gate waves a good-enough key
through (a short teleport), and the Captain's den gets a front-door ledger for the Rat King's Key.
BACK ROOMS: a ledger on each trader's counter opens a menu of extra stock filtered by your tier.

Every menu button runs `/trigger bm.act set <code>`; every handler re-checks the menu that was opened, distance and
tier, so typing a trigger by hand can't buy anything the menu wouldn't sell. Importing registers the items;
generate(G) runs after phase27.generate."""
from nbt import snbt, B, F, Int
from items import item, consumable, T, TOTEM, ITEMS, ITEM_VERSION
import mgeo
import market2

W, BF = market2.W, market2.BF
VALUE = {'token': 1, 'lucky_token': 5, 'blood_crystal': 3, 'medallion': 9, 'trophy': 54}
SWAP_SELLS = {'token', 'medallion', 'trophy', 'lucky_token', 'blood_crystal', 'diamond', 'emerald', 'netherite_ingot'}
NO_POINTS = {'pawn'}                         # Old Barnaby buys back: nothing he hands over is a purchase
TIERS = [  # (tier, title, points, colour, key item, what it unlocks)
    (0, 'Stranger', 0, 'gray', 'market_key', 'everything the market has today'),
    (1, 'Regular', 150, 'green', 'market_key', 'traders greet you by name; each back room opens'),
    (2, 'Associate', 500, 'aqua', 'silver_key', 'the Silver Key, the Dark Auction, more back-room stock'),
    (3, 'Partner', 1500, 'gold', 'gold_key', 'the Gold Key, the Gilded Gutter, its Concierge and the Rat Bank'),
    (4, 'Family', 4000, 'light_purple', 'rat_king_key', "the Rat King's Key, the Captain's front door, your portrait, signature stock"),
]
DEEDS = {'bounty': 20, 'jackpot': 10, 'boss': 50}
MENU = {'standing': 1, 'back': 100, 'gate': 200, 'auction': 300, 'bank': 400, 'concierge': 500, 'burrow': 600, 'merc': 700,
        'teller': 400}
CUR_NAME = {'token': ('Token', 'Tokens', 'gold'), 'medallion': ('Medallion', 'Medallions', 'light_purple'),
            'trophy': ('Trophy', 'Trophies', '#ffb300'), 'lucky_token': ('Lucky Token', 'Lucky Tokens', 'green'),
            'blood_crystal': ('Blood Moon Crystal', 'Blood Moon Crystals', 'dark_red')}


def cur_text(cur, n):
    one, many, _ = CUR_NAME[cur]
    return f'{n} {one if n == 1 else many}'


# ===================================================================== ITEMS: the three new keys
KEY_LORE = {
    'silver_key': ('Silver Key', '#c9d1dc', 'Associate', ['the vault door', 'the Dark Auction']),
    'gold_key': ('Gold Key', '#ffcf3f', 'Partner', ['the vault door', 'the Dark Auction', 'the Gilded Gutter']),
    'rat_king_key': ("Rat King's Key", '#ffb300', 'Family', ['the vault door', 'the Dark Auction', 'the Gilded Gutter', "the Captain's den"]),
}
for kid, (nm, col, title_, rooms) in KEY_LORE.items():
    item(kid, TOTEM, nm, col,
         [f'Carried by a {title_} of the Black Market.', ('Opens: ' + ', '.join(rooms[:2]) + (',' if len(rooms) > 2 else ''), 'blue')] +
         ([(', '.join(rooms[2:]) + '.', 'blue')] if len(rooms) > 2 else []) +
         ['Keep it in your inventory.', ('It changes as your Standing grows.', 'dark_gray')],
         model=f'bm:{kid}', glint=True, cat='key', custom_extra={'bm_key': B(1)}, bold=(kid == 'rat_king_key'))
KEY_ORDER = ['market_key', 'silver_key', 'gold_key', 'rat_king_key']

# ===================================================================== BACK ROOMS (tier 1 Regular, 2 Associate, 4 Family)
# entry: (tier, what, count, (currency, price), label). `what` is a Black Market item id, a vanilla item id, or a
# special: 'mending_book', 'treasure_map'.
TRADER_ORDER = ['fence', 'pawn', 'outfitter', 'arms', 'armory', 'chef', 'professor', 'lucky', 'captain', 'blood']
BACKROOM = {
    'fence': [(1, 'sealed_explorer_map', 1, ('token', 3), "Sealed Explorer's Map"), (2, 'bankers_card', 1, ('medallion', 3), "Banker's Card"),
              (4, 'smuggler_jar', 1, ('medallion', 6), "Smuggler's Jar")],
    'pawn': [(1, 'fair_weather_bell', 1, ('token', 6), 'Fair Weather Bell'), (2, 'minecraft:totem_of_undying', 2, ('medallion', 4), '2 Totems of Undying'),
             (4, 'spawner_crowbar', 1, ('medallion', 8), 'Spawner Crowbar')],
    'outfitter': [(1, 'rat_gang_portrait', 1, ('token', 4), 'Rat Gang Portrait'), (2, 'donado_trophy', 1, ('medallion', 4), 'Donado Trophy'),
                  (4, 'brass_wing_scroll', 1, ('trophy', 2), 'Brass Wing Scroll')],
    'arms': [(1, 'minecraft:spectral_arrow', 16, ('token', 3), '16 Spectral Arrows'),
             (2, 'minecraft:netherite_upgrade_smithing_template', 1, ('medallion', 3), 'Netherite Upgrade Template'),
             (4, 'showstopper_charm', 1, ('trophy', 2), 'Showstopper Charm')],
    'armory': [(1, 'lodestone_locket', 1, ('token', 8), 'Lodestone Locket'), (2, 'minecraft:wither_skeleton_skull', 3, ('medallion', 4), '3 Wither Skeleton Skulls'),
               (4, 'market_crest_scroll', 1, ('trophy', 2), 'Market Crest Scroll')],
    'chef': [(1, 'minecraft:cake', 1, ('token', 2), 'A Whole Cake'), (2, 'minecraft:enchanted_golden_apple', 1, ('medallion', 6), 'Enchanted Golden Apple'),
             (4, 'minecraft:enchanted_golden_apple', 3, ('trophy', 2), '3 Enchanted Golden Apples')],
    'professor': [(1, 'minecraft:experience_bottle', 16, ('token', 3), "16 Bottles o' Enchanting"), (2, 'mending_book', 1, ('medallion', 4), 'Book of Mending'),
                  (4, 'auroral_crown', 1, ('trophy', 2), 'Auroral Crown')],
    'lucky': [(1, 'jackpot_card_5', 1, ('lucky_token', 4), 'Jackpot Scratch Card'), (2, 'heartstone', 1, ('lucky_token', 15), 'Heartstone'),
              (4, 'bloomwalker_boots', 1, ('trophy', 2), 'Bloomwalker Boots')],
    'captain': [(1, 'treasure_map', 1, ('token', 3), 'Buried Treasure Map'), (2, 'minecraft:heart_of_the_sea', 1, ('medallion', 3), 'Heart of the Sea'),
                (4, 'rat_familiar', 1, ('trophy', 2), 'Rat Familiar')],
    'blood': [(1, 'minecraft:ominous_bottle', 1, ('blood_crystal', 6), 'Ominous Bottle'), (2, 'minecraft:nether_star', 1, ('blood_crystal', 24), 'Nether Star'),
              (4, 'heartstone', 3, ('trophy', 1), '3 Heartstones')],
}
TRADER_NAME = {'fence': 'The Fence', 'pawn': 'Old Barnaby', 'outfitter': 'Madame Velour', 'arms': "Vinny 'Two-Blades'",
               'armory': 'Sgt. Steelwhisker', 'chef': 'Chef Fromage', 'professor': 'Prof. Whiskerton', 'lucky': 'Lucky Whiskers',
               'captain': 'Capt. Cheddarbeard', 'blood': 'The Bloodbroker'}
FLOOR_LEDGER = {'chef': ((66.5, W, 43.5), 90), 'professor': ((31.5, BF + 1, 18.5), -90), 'lucky': ((9.5, W, 68.5), 180),
                'captain': ((2.5, W, 18.5), 0)}

# ===================================================================== GATES (ledger id: (pos, yaw, region, kind))
GATES = {
    21: ((39.5, W, 15.5), 0, 'public', 'hall_in'), 22: ((39.5, W, 12.5), 180, 'hall', 'hall_out'),
    23: ((48.5, BF + 1, 15.5), 0, 'public', 'vip_in'), 24: ((47.5, BF + 1, 13.5), 180, 'gutter', 'vip_out'),
    25: ((5.5, W, 23.5), 0, 'public', 'den_in'), 26: ((5.5, W, 18.5), 180, 'den', 'den_out'),
}
GATE_DEST = {'hall_in': ((37.5, W, 12.5), 180, 'hall'), 'hall_out': ((37.5, W, 17.5), 0, 'public'),
             'vip_in': ((46.5, BF + 1, 12.5), 180, 'gutter'), 'vip_out': ((46.5, BF + 1, 16.5), 0, 'public'),
             'den_in': ((4.5, W, 16.5), 0, 'den'), 'den_out': ((3.5, W, 23.5), 0, 'public')}
GATE_LABEL = {'hall_in': ('The Dark Auction', 'Members: Silver Key or better'), 'hall_out': ('Exit', 'back to Pawn Alley'),
              'vip_in': ('The Gilded Gutter', 'Partners only: Gold Key or better'), 'vip_out': ('Exit', 'back to the terrace'),
              'den_in': ('Rat Gang HQ', "Family only: the Rat King's Key"), 'den_out': ('Front door', 'out to the docks')}
# Family portraits round Fountain Plaza (feet positions of the plinths), facing the fountain
PORTRAITS = [((31.5, W, 41.5), -45), ((45.5, W, 41.5), 45), ((31.5, W, 51.5), -135), ((45.5, W, 51.5), 135)]

SPAWNS = []        # (pos, what) for the install bounds check - later phases add theirs


# ===================================================================== dialog helpers (shared with phase30/31)
def text_lines(parts):
    return parts


def btn(label, code=None, tooltip=None, width=None):
    b = {'label': label}
    if tooltip: b['tooltip'] = tooltip
    if width: b['width'] = Int(width)
    if code is not None: b['action'] = {'type': 'minecraft:run_command', 'command': f'/trigger bm.act set {code}'}
    return b


def body(contents, width=260):
    return {'type': 'minecraft:plain_message', 'contents': contents, 'width': Int(width)}


def multi(title, bodies, buttons, columns=2, exit_label='Close', button_width=150):
    d = {'type': 'minecraft:multi_action', 'title': title, 'body': bodies, 'actions': buttons, 'columns': Int(columns),
         'exit_action': {'label': exit_label}, 'pause': False, 'after_action': 'close'}
    return d


def notice(title, bodies, label='Close'):
    return {'type': 'minecraft:notice', 'title': title, 'body': bodies, 'action': {'label': label}, 'pause': False,
            'after_action': 'close'}


RAW = '@@RAW:'


def inline(d):
    """A dialog for `$dialog show @s <snbt>` inside a macro function: "@@RAW:name@@" strings become $(name) unquoted."""
    import re
    s = snbt(d)
    return re.sub(r'"@@RAW:(\w+)@@"', r'$(\1)', s)


# ===================================================================== payments
def pay_lines(cur, n, fail):
    """Commands that take `n` of `cur` from @s (Medallions: inventory, then the bank when #usebank is 1, then Trophies
    broken with change) and run `fail` (a command) if the player can't cover it."""
    if cur == 'medallion':
        return [f'execute store result score #ok bm.pay run function bm:p28/pay/med {{n:{n}}}',
                f'execute if score #ok bm.pay matches 0 run return run {fail}']
    return [f'execute store result score #ok bm.pay run function bm:p28/pay/any {{cur:"{cur}",n:{n}}}',
            f'execute if score #ok bm.pay matches 0 run return run {fail}']


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    tick, fast, second, load = [], [], [], []
    ident = [F(0), F(0), F(0), F(1)]
    G.P28_SPAWNS = SPAWNS

    objs = ['bm.stand dummy', 'bm.tier dummy', 'bm.standing trigger', 'bm.act trigger', 'bm.menu dummy', 'bm.lgid dummy',
            'bm.greet dummy', 'bm.pay dummy', 'bm.bk_med dummy']
    load += [f'scoreboard objectives add {o}' for o in objs]
    load += ['scoreboard players set #6 bm.pay 6', 'scoreboard players set #20 bm.pay 20', 'scoreboard players set #100 bm.pay 100']
    G.P28_OBJ = [o.split()[0] for o in objs]

    # ------------------------------------------------------------------ menu buttons: /trigger
    tick += ['scoreboard players enable @a bm.standing', 'scoreboard players enable @a bm.act',
             'execute as @a[scores={bm.standing=1..}] at @s run function bm:p28/standing/open',
             'execute as @a[scores={bm.act=1..}] at @s run function bm:p28/act',
             'scoreboard players set @a[scores={bm.act=..-1}] bm.act 0', 'scoreboard players set @a[scores={bm.standing=..-1}] bm.standing 0']
    fn('p28/act', ['scoreboard players operation #act bm.pay = @s bm.act', 'scoreboard players set @s bm.act 0',
                   'execute if score #act bm.pay matches 1 run return run function bm:p28/standing/show',
                   'execute if score #act bm.pay matches 1000..1999 run return run function bm:p28/back/act',
                   'execute if score #act bm.pay matches 2000..2099 run return run function bm:p28/gate/act'])
    fn('p28/stale', [title('@s', 'actionbar', T('That menu has closed - open it again.', 'gray'))])

    # ------------------------------------------------------------------ payments (custom_data id only: immune to NBT drift)
    fn('p28/pay/any', ['$execute store result score #have bm.pay run clear @s *[minecraft:custom_data~{bm:"$(cur)"}] 0',
                       '$execute unless score #have bm.pay matches $(n).. run return 0',
                       '$clear @s *[minecraft:custom_data~{bm:"$(cur)"}] $(n)',
                       'return 1'])
    fn('p28/pay/med', ['$scoreboard players set #need bm.pay $(n)', 'return run function bm:p28/pay/med_s'])
    fn('p28/pay/med_s', [
        'execute store result score #have bm.pay run clear @s *[minecraft:custom_data~{bm:"medallion"}] 0',
        'scoreboard players set #bank bm.pay 0',
        'execute if score #usebank bm.pay matches 1 if score @s bm.bk_med matches 1.. run scoreboard players operation #bank bm.pay = @s bm.bk_med',
        'execute store result score #tro bm.pay run clear @s *[minecraft:custom_data~{bm:"trophy"}] 0',
        'scoreboard players operation #tot bm.pay = #tro bm.pay', 'scoreboard players operation #tot bm.pay *= #6 bm.pay',
        'scoreboard players operation #tot bm.pay += #have bm.pay', 'scoreboard players operation #tot bm.pay += #bank bm.pay',
        'execute if score #tot bm.pay < #need bm.pay run return 0',
        # 1) Medallions in the inventory
        'scoreboard players operation #take bm.pay = #need bm.pay', 'scoreboard players operation #take bm.pay < #have bm.pay',
        'execute store result storage bm:tmp pay.n int 1 run scoreboard players get #take bm.pay',
        'execute if score #take bm.pay matches 1.. run function bm:p28/pay/clear_med with storage bm:tmp pay',
        'scoreboard players operation #need bm.pay -= #take bm.pay',
        # 2) the Rat Bank (auction bids only)
        'scoreboard players operation #take bm.pay = #need bm.pay', 'scoreboard players operation #take bm.pay < #bank bm.pay',
        'scoreboard players operation @s bm.bk_med -= #take bm.pay', 'scoreboard players operation #need bm.pay -= #take bm.pay',
        'execute if score #take bm.pay matches 1.. run ' + tellraw('@s', PREFIX + [T('The Rat Bank covered ', 'gray'), {'score': {'name': '#take', 'objective': 'bm.pay'}, 'color': 'light_purple'}, T(' Medallions of that.', 'gray')]),
        # 3) Trophies, broken into 6 Medallions each, change handed back
        'execute if score #need bm.pay matches 1.. run function bm:p28/pay/break',
        'return 1'])
    fn('p28/pay/break', [
        'scoreboard players operation #t bm.pay = #need bm.pay', 'scoreboard players add #t bm.pay 5', 'scoreboard players operation #t bm.pay /= #6 bm.pay',
        'execute store result storage bm:tmp pay.t int 1 run scoreboard players get #t bm.pay',
        'function bm:p28/pay/clear_tro with storage bm:tmp pay',
        'scoreboard players operation #chg bm.pay = #t bm.pay', 'scoreboard players operation #chg bm.pay *= #6 bm.pay',
        'scoreboard players operation #chg bm.pay -= #need bm.pay',
        'execute store result storage bm:tmp pay.c int 1 run scoreboard players get #chg bm.pay',
        'execute if score #chg bm.pay matches 1.. run function bm:p28/pay/give_med with storage bm:tmp pay',
        tellraw('@s', PREFIX + [T('The rats broke ', 'gray'), {'score': {'name': '#t', 'objective': 'bm.pay'}, 'color': '#ffb300'},
                                T(' Trophy into Medallions (6 each); ', 'gray'), {'score': {'name': '#chg', 'objective': 'bm.pay'}, 'color': 'light_purple'},
                                T(' came back as change.', 'gray')])])
    fn('p28/pay/clear_med', ['$clear @s *[minecraft:custom_data~{bm:"medallion"}] $(n)'])
    fn('p28/pay/clear_tro', ['$clear @s *[minecraft:custom_data~{bm:"trophy"}] $(t)'])
    fn('p28/pay/give_med', [f'$give @s {G.item_arg("medallion")} $(c)'])
    fn('p28/pay/give_med_n', [f'$give @s {G.item_arg("medallion")} $(n)'])

    # ------------------------------------------------------------------ player names as plain strings (portraits, the price board)
    # a player head filled from the player carries their profile; its name is a plain string we can copy anywhere
    wjson('bm/loot_table/p28/head.json', {'pools': [{'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:player_head',
                                                                              'functions': [{'function': 'minecraft:fill_player_head', 'entity': 'this'}]}]}]})
    namer = {'Tags': ['bm.namer'], 'item': {'id': 'minecraft:stone', 'count': Int(1)}, 'transformation': {
        'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0), F(0)], 'scale': [F(0), F(0), F(0)]}}
    fn('p28/name/of', ['data remove storage bm:tmp nm', f'summon minecraft:item_display ~ ~ ~ {snbt(namer)}',
                       'loot replace entity @e[type=minecraft:item_display,tag=bm.namer,distance=..1,limit=1] contents loot bm:p28/head',
                       'data modify storage bm:tmp nm.name set from entity @e[type=minecraft:item_display,tag=bm.namer,distance=..1,limit=1] item.components."minecraft:profile".name',
                       'data modify storage bm:tmp nm.profile set from entity @e[type=minecraft:item_display,tag=bm.namer,distance=..1,limit=1] item.components."minecraft:profile"',
                       'kill @e[type=minecraft:item_display,tag=bm.namer,distance=..1]'])

    # ================================================================== STANDING: points from trades
    O = G.all_offers()

    def iid_of(st_):
        c = st_.get('components', {}).get('minecraft:custom_data')
        return c['bm'] if c and 'bm' in c else st_['id'].split(':', 1)[1]
    groups = {}
    for tr, offs in O.items():
        for o in offs:
            s = iid_of(o['sell']); n = int(o['sell']['count'])
            pts = 0 if (s in SWAP_SELLS or tr in NO_POINTS) else sum(VALUE.get(iid_of(o[k]), 0) * int(o[k]['count']) for k in ('buy', 'buyB') if k in o)
            groups.setdefault((tr, s, n), set()).add(pts)
    wjson('bm/advancement/p28/trade/root.json', {'criteria': {'never': {'trigger': 'minecraft:impossible'}}})
    point_values = set()
    G.P28_TRADE_ADV = 0
    for (tr, s, n), pts in sorted(groups.items()):
        p = min(pts)                     # (the build proves no offer group is ambiguous; min is the safe reading)
        if len(pts) > 1: print(f'phase28: {tr}/{s}x{n} sells at several prices {sorted(pts)} - earning {p}')
        if p <= 0: continue
        point_values.add(p)
        base = ITEMS[s]['base'] if s in ITEMS else 'minecraft:' + s
        itp = {'items': base, 'count': Int(n)}
        if s in ITEMS: itp['predicates'] = {'minecraft:custom_data': snbt(ITEMS[s]['custom'])}
        wjson(f'bm/advancement/p28/trade/{tr}/{s}_{n}.json', {'parent': 'bm:p28/trade/root', 'criteria': {'t': {
            'trigger': 'minecraft:villager_trade', 'conditions': {
                'villager': [{'condition': 'minecraft:entity_properties', 'entity': 'this',
                              'predicate': {'minecraft:entity_tags': {'all_of': [f'bm.npc_{tr}']}}}],
                'item': itp}}}, 'rewards': {'function': f'bm:p28/pts/{p}'}})
        G.P28_TRADE_ADV += 1
    for p in sorted(point_values):
        fn(f'p28/pts/{p}', ['advancement revoke @s from bm:p28/trade/root', f'scoreboard players set #pts bm.pay {p}', 'function bm:p28/st/add'])
    # deeds
    G.FUNCS['p17/bounty_done'] += [f'scoreboard players set #pts bm.pay {DEEDS["bounty"]}', 'execute at @s run function bm:p28/st/add']
    wjson('bm/advancement/p28/jackpot_kill.json', {'criteria': {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {
        'entity': [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:entity_tags': {'all_of': ['bm.jackpot']}}}]}}},
        'rewards': {'function': 'bm:p28/deed/jackpot'}})
    fn('p28/deed/jackpot', ['advancement revoke @s only bm:p28/jackpot_kill', f'scoreboard players set #pts bm.pay {DEEDS["jackpot"]}', 'function bm:p28/st/add'])
    for k in list(G.FUNCS):
        if k.startswith('p2/') and k.endswith('/credit_first'):
            G.FUNCS[k] += [f'scoreboard players set #pts bm.pay {DEEDS["boss"]}', 'execute at @s run function bm:p28/st/add']

    # adding points: the Rat King's Signet (anywhere in the inventory) adds a quarter
    fn('p28/st/add', ['execute unless score @s bm.stand matches 0.. run scoreboard players set @s bm.stand 0',
                      'execute if items entity @s container.* *[minecraft:custom_data~{bm:"rat_king_signet"}] run function bm:p28/st/signet',
                      'execute unless items entity @s container.* *[minecraft:custom_data~{bm:"rat_king_signet"}] if items entity @s weapon.offhand *[minecraft:custom_data~{bm:"rat_king_signet"}] run function bm:p28/st/signet',
                      'scoreboard players operation @s bm.stand += #pts bm.pay',
                      title('@s', 'actionbar', [T('+', 'gold'), {'score': {'name': '#pts', 'objective': 'bm.pay'}, 'color': 'gold'}, T(' Standing  ', 'gold'),
                                                T('(', 'dark_gray'), {'score': {'name': '@s', 'objective': 'bm.stand'}, 'color': 'gray'}, T(')', 'dark_gray')]),
                      'function bm:p28/st/tier'])
    fn('p28/st/signet', ['scoreboard players operation #q bm.pay = #pts bm.pay', 'scoreboard players add #q bm.pay 2',
                         'scoreboard players operation #q bm.pay /= #4 bm.pay', 'scoreboard players operation #pts bm.pay += #q bm.pay'])
    load.append('scoreboard players set #4 bm.pay 4')
    tier_lines = ['execute unless score @s bm.stand matches 0.. run scoreboard players set @s bm.stand 0',
                  'execute unless score @s bm.tier matches 0.. run scoreboard players set @s bm.tier 0',
                  'scoreboard players set #nt bm.pay 0']
    tier_lines += [f'execute if score @s bm.stand matches {pts}.. run scoreboard players set #nt bm.pay {t}' for t, _, pts, _, _, _ in TIERS[1:]]
    tier_lines += ['execute if score #nt bm.pay > @s bm.tier run function bm:p28/st/up']
    fn('p28/st/tier', tier_lines)
    up = ['scoreboard players operation @s bm.tier = #nt bm.pay', 'title @s times 10 70 20']
    for t, nm, pts, col, key, unlock in TIERS[1:]:
        up += [f'execute if score @s bm.tier matches {t} run ' + title('@s', 'subtitle', T('Unlocked: ' + unlock, 'gray')),
               f'execute if score @s bm.tier matches {t} run ' + title('@s', 'title', T(nm, col, bold=True)),
               f'execute if score @s bm.tier matches {t} run ' + tellraw('@s', PREFIX + [T('Your Standing rises: you are now ', 'gray'), T(nm, col, bold=True),
                                                                                          T(f'. Unlocked: {unlock}.', 'gray')])]
    up += ['playsound minecraft:block.bell.use player @s ~ ~ ~ 1 1', 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.6 1.2',
           'execute as @e[type=minecraft:item_display,tag=bm.rat_sprite,distance=..48] at @s run particle minecraft:happy_villager ~ ~1 ~ 0.3 0.4 0.3 0 6',
           'execute if entity @e[type=minecraft:item_display,tag=bm.rat_sprite,distance=..48] run playsound minecraft:entity.villager.celebrate neutral @s ~ ~ ~ 0.8 1.7',
           'execute if score @s bm.tier matches 4 run function bm:p28/portrait/join']
    fn('p28/st/up', up)
    second.append('execute as @a at @s run function bm:p28/st/tier')

    # ------------------------------------------------------------------ the status menu (/trigger bm.standing)
    fn('p28/standing/open', ['scoreboard players set @s bm.standing 0', 'function bm:p28/standing/show'])
    show = ['execute unless score @s bm.stand matches 0.. run scoreboard players set @s bm.stand 0', 'function bm:p28/st/tier',
            'scoreboard players set @s bm.menu 1', 'data remove storage bm:ui st',
            'execute store result storage bm:ui st.pts int 1 run scoreboard players get @s bm.stand']
    for i, (t, nm, pts, col, key, unlock) in enumerate(TIERS):
        nxt = TIERS[i + 1] if i + 1 < len(TIERS) else None
        d = {'title': nm, 'col': col, 'next': (f'Next: {nxt[1]} at {nxt[2]:,} points' if nxt else 'The top of the ladder. The rats salute you.'),
             'lo': pts, 'hi': nxt[2] if nxt else pts}
        show.append(f'execute if score @s bm.tier matches {t} run data modify storage bm:ui st merge value {snbt(d)}')
        if nxt:
            show += [f'execute if score @s bm.tier matches {t} run scoreboard players set #lo bm.pay {pts}',
                     f'execute if score @s bm.tier matches {t} run scoreboard players set #hi bm.pay {nxt[2]}']
    show += ['scoreboard players set #pct bm.pay 20',
             'execute if score @s bm.tier matches ..3 run function bm:p28/standing/pct',
             'scoreboard players operation #togo bm.pay = #hi bm.pay', 'scoreboard players operation #togo bm.pay -= @s bm.stand',
             'execute if score @s bm.tier matches 4 run scoreboard players set #togo bm.pay 0',
             'execute store result storage bm:ui st.togo int 1 run scoreboard players get #togo bm.pay']
    for k in range(21):
        show.append(f'execute if score #pct bm.pay matches {k} run data modify storage bm:ui st.bar set value "{"■" * k}{"□" * (20 - k)}"')
    show.append('function bm:p28/standing/dlg with storage bm:ui st')
    fn('p28/standing/show', show)
    fn('p28/standing/pct', ['scoreboard players operation #pct bm.pay = @s bm.stand', 'scoreboard players operation #pct bm.pay -= #lo bm.pay',
                            'scoreboard players operation #pct bm.pay *= #20 bm.pay',
                            'scoreboard players operation #rng bm.pay = #hi bm.pay', 'scoreboard players operation #rng bm.pay -= #lo bm.pay',
                            'scoreboard players operation #pct bm.pay /= #rng bm.pay',
                            'execute if score #pct bm.pay matches 20.. run scoreboard players set #pct bm.pay 19',
                            'execute if score #pct bm.pay matches ..-1 run scoreboard players set #pct bm.pay 0'])
    ladder = []
    for t, nm, pts, col, key, unlock in TIERS:
        ladder += [T(f'\n{nm}', col, bold=True), T(f'  {pts:,}  ', 'white'), T(unlock, 'gray')]
    dlg = notice(T('Your Standing', 'gold', bold=True), [
        body([T('', 'white'), {'text': '$(title)', 'color': '$(col)', 'bold': True}], 260),
        body([T('Points: ', 'gray'), T('$(pts)', 'white')], 260),
        body([T('$(bar)', 'green')], 260),
        body([T('$(next)', 'gray'), T('  (', 'dark_gray'), T('$(togo)', 'yellow'), T(' to go)', 'dark_gray')], 260),
        body([T('Earn Standing by buying from market traders (Token value of the price), Blood Bounties, Jackpot monsters and first boss victories.', 'dark_gray')] + ladder, 300)])
    fn('p28/standing/dlg', [f'$dialog show @s {inline(dlg)}'])

    # ------------------------------------------------------------------ traders greet Regulars by name
    wjson('bm/tags/entity_type/p28_traders.json', {'values': ['minecraft:villager', 'minecraft:wandering_trader']})
    second += ['scoreboard players remove @e[type=#bm:p28_traders,tag=bm.npc,scores={bm.greet=1..}] bm.greet 1',
               'execute as @e[type=#bm:p28_traders,tag=bm.npc] at @s unless score @s bm.greet matches 1.. '
               'if entity @a[distance=..4,scores={bm.tier=1..},gamemode=!spectator] run function bm:p28/greet']
    greet = ['scoreboard players set @s bm.greet 90', 'tag @s add bm.greeter']
    lines = {1: 'Good to see you again, ', 2: 'Ah, my favourite Associate, ', 3: 'Partner! Welcome back, ', 4: 'Family is always welcome here, '}
    for t, msg in lines.items():
        greet.append(f'execute as @a[distance=..4,scores={{bm.tier={t}}},gamemode=!spectator,sort=nearest,limit=1] run ' +
                     title('@s', 'actionbar', [{'selector': '@e[tag=bm.greeter,limit=1]', 'color': 'yellow'}, T(': ', 'gray'),
                                               T(msg, 'white'), {'selector': '@s', 'color': 'gold'}, T('!', 'white')]))
    greet += ['tag @s remove bm.greeter']
    fn('p28/greet', greet)

    # ================================================================== KEYS: the door accepts the shared marker; keys follow the tier
    f = G.FUNCS['loop/fast']
    anchor = 'execute as @a[tag=!bm.haskey] if items entity @s weapon.offhand *[minecraft:custom_data~{bm:"market_key"}] run tag @s add bm.haskey'
    k = f.index(anchor) + 1
    f[k:k] = ['execute as @a[tag=!bm.haskey] if items entity @s container.* *[minecraft:custom_data~{bm_key:1b}] run tag @s add bm.haskey',
              'execute as @a[tag=!bm.haskey] if items entity @s weapon.offhand *[minecraft:custom_data~{bm_key:1b}] run tag @s add bm.haskey']
    slots = [f'container.{i}' for i in range(36)] + ['weapon.offhand']
    for t, nm, pts, col, key, unlock in TIERS[2:]:
        lower = KEY_ORDER[:KEY_ORDER.index(key)]
        sw = []
        for sl in slots:
            for lk in lower:
                sw.append(f'execute if items entity @s {sl} *[minecraft:custom_data~{{bm:"{lk}"}}] run item replace entity @s {sl} with {G.item_arg(key)}')
        sw += ['playsound minecraft:block.bell.use player @s ~ ~ ~ 1 1.3', 'playsound minecraft:block.chain.place player @s ~ ~ ~ 1 0.8',
               title('@s', 'actionbar', T(f'Your key turns in your pocket... it is now the {ITEMS[key]["name"]}.', col))]
        fn(f'p28/key/to_{t}', sw)
        for lk in lower:
            second.append(f'execute as @a[scores={{bm.tier={t}}}] if items entity @s container.* *[minecraft:custom_data~{{bm:"{lk}"}}] at @s run function bm:p28/key/to_{t}')
            second.append(f'execute as @a[scores={{bm.tier={t}}}] if items entity @s weapon.offhand *[minecraft:custom_data~{{bm:"{lk}"}}] at @s run function bm:p28/key/to_{t}')

    # ================================================================== LEDGERS (gates, back rooms) + the per-market install
    fin = 'execute rotated ~ 0 run tp @e[tag=bm.n18,distance=..1.5] ~ ~ ~ ~ ~'
    untag = 'tag @e[tag=bm.n18,distance=..1.5] remove bm.n18'

    def label_disp(lines_, y):
        return {'Tags': ['bm.e18', 'bm.n18', 'bm.lg_label'], 'billboard': 'center', 'view_range': F(0.18), 'default_background': B(0),
                'background': Int(0x60000000), 'text': lines_, 'line_width': Int(160),
                'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(y), F(0)], 'scale': [F(0.45)] * 3}}

    def ledger_spawn(lid, kind, label):
        """At the ledger's spot (feet / counter top), rotated to face where it should face."""
        box = {'Tags': ['bm.e18', 'bm.n18', 'bm.ledger'], 'response': B(1)}
        cmds = []
        if kind == 'counter':
            box.update(width=F(0.7), height=F(0.4))
            book = {'Tags': ['bm.e18', 'bm.n18', 'bm.lg_book'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:statue_ledger'}},
                    'item_display': 'fixed', 'billboard': 'fixed', 'brightness': {'block': Int(12), 'sky': Int(10)},
                    'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.25), F(0)], 'scale': [F(0.5)] * 3}}
            cmds.append(f'summon minecraft:item_display ~ ~ ~ {snbt(book)}')
            ly = 0.75
        else:
            box.update(width=F(0.9), height=F(1.1))
            lect = {'Tags': ['bm.e18', 'bm.n18', 'bm.lg_book'], 'block_state': {'id': 'minecraft:lectern', 'properties': {'facing': 'south', 'has_book': 'true', 'powered': 'false'}},
                    'brightness': {'block': Int(12), 'sky': Int(10)},
                    'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(-0.5), F(0), F(-0.5)], 'scale': [F(1)] * 3}}
            cmds.append(f'summon minecraft:block_display ~ ~ ~ {snbt(lect)}')
            ly = 1.55
        cmds += [f'summon minecraft:interaction ~ ~ ~ {snbt(box)}',
                 f'scoreboard players set @e[type=minecraft:interaction,tag=bm.n18,distance=..1.5] bm.lgid {lid}',
                 f'summon minecraft:text_display ~ ~ ~ {snbt(label_disp(label, ly))}', fin, untag]
        fn(f'p28/spawn/lg_{lid}', cmds)

    install = ['tag @s add bm.i18', 'kill @e[tag=bm.e18,distance=..96]']

    def place(pos, yaw, func, what, region=None, air_only=False):
        if region: mgeo.need_floor(pos, region, what)
        elif air_only: mgeo.need_air(pos, what)
        SPAWNS.append((pos, what))
        install.append(f'execute positioned {mgeo.rel(pos)} rotated ~{yaw} 0 run function bm:{func}')
    G.P28_PLACE = place
    G.P28_INSTALL = install

    # back-room ledgers: on the trader's counter (or a lectern on the floor beside the traders who stand in front of theirs)
    LEDGER_POS = {}
    for ti, tr in enumerate(TRADER_ORDER, 1):
        if tr in FLOOR_LEDGER:
            pos, yaw = FLOOR_LEDGER[tr]; kind = 'lectern'
            place(pos, yaw, f'p28/spawn/lg_{ti}', f'{tr} back-room ledger', region='den' if tr == 'captain' else 'public')
        else:
            spot = mgeo.counter_spot(tr)
            if not spot: raise SystemExit(f'phase28: no counter spot for {tr}')
            pos, yaw = spot; kind = 'counter'
            mgeo.need_air(pos, f'{tr} back-room ledger')
            place(pos, yaw, f'p28/spawn/lg_{ti}', f'{tr} back-room ledger', air_only=True)
        LEDGER_POS[tr] = (pos, kind)
        ledger_spawn(ti, kind, [T('Back Room', 'yellow', bold=True), T('\nright-click the ledger', 'gray')])
    G.P28_LEDGERS = LEDGER_POS
    for lid, (pos, yaw, region, kind) in GATES.items():
        place(pos, yaw, f'p28/spawn/lg_{lid}', f'gate ledger {kind}', region=region)
        a, b = GATE_LABEL[kind]
        ledger_spawn(lid, 'lectern', [T(a, 'gold', bold=True), T('\n' + b, 'gray')])
    for kind, (pos, yaw, region) in GATE_DEST.items():
        mgeo.need_floor(pos, region, f'gate destination {kind}')

    # clicks: read the clicking player BEFORE clearing the interaction (check_logic lints this order)
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.ledger] if data entity @s interaction at @s run function bm:p28/ledger/click',
             'execute as @e[type=minecraft:interaction,tag=bm.ledger] if data entity @s attack run data remove entity @s attack']
    fn('p28/ledger/click', ['scoreboard players operation #lg bm.pay = @s bm.lgid', 'tag @s add bm.lgsel',
                            'execute on target at @s run function bm:p28/ledger/open', 'tag @s remove bm.lgsel',
                            'data remove entity @s interaction'])
    opn = ['execute if entity @s[gamemode=spectator] run return 0', 'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 1']
    opn += [f'execute if score #lg bm.pay matches {ti} run return run function bm:p28/back/open_{ti}' for ti in range(1, len(TRADER_ORDER) + 1)]
    opn += [f'execute if score #lg bm.pay matches {lid} run return run function bm:p28/gate/{GATES[lid][3]}' for lid in GATES]
    fn('p28/ledger/open', opn)       # later phases add their ledger ids (31 podium, 41 concierge, 42 teller) to this dispatch

    # ------------------------------------------------------------------ back rooms
    def give_cmds(what, n):
        if what in ITEMS: return [give(what, n)]
        if what == 'mending_book':
            return [f'give @s minecraft:enchanted_book[minecraft:stored_enchantments={{"minecraft:mending":1}}] {n}']
        if what == 'treasure_map':
            return [f'loot spawn ~ ~0.5 ~ loot bm:p28/treasure_map']
        return [f'give @s {what} {n}']
    wjson('bm/loot_table/p28/treasure_map.json', {'pools': [{'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:buried_treasure_map', 'functions': [     # 26.3 explorer-map item
        {'function': 'minecraft:exploration_map', 'destination': 'minecraft:on_treasure_maps', 'decoration': 'minecraft:red_x', 'zoom': 1,
         'search_radius': 50, 'skip_existing_chunks': False},
        {'function': 'minecraft:set_name', 'target': 'item_name', 'name': T("Cheddarbeard's Treasure Map", 'gold')}]}]}]})
    tier_name = {t: nm for t, nm, *_ in TIERS}
    act = []
    for ti, tr in enumerate(TRADER_ORDER, 1):
        stock = BACKROOM[tr]
        for t in range(5):
            buttons = []
            for i, (req, what, n, (cur, price), label) in enumerate(stock):
                code = 1000 + ti * 20 + i
                if t >= req:
                    buttons.append(btn([T(label, 'white'), T(f'  {cur_text(cur, price)}', CUR_NAME[cur][2])], code,
                                       tooltip=T(f'{tier_name[req]} stock. Paid straight from your inventory.', 'gray'), width=240))
                else:
                    buttons.append(btn([T('🔒 ', 'dark_gray'), T(label, 'dark_gray'), T(f'  ({tier_name[req]})', 'gray')],
                                       tooltip=T(f'Reach {tier_name[req]} Standing to buy this.', 'gray'), width=240))
            intro = ('The back room is closed to strangers. Come back as a Regular.' if t == 0 else
                     'Keep your voice down. This stock is not on the board.')
            wjson(f'bm/dialog/p28/back_{tr}_{t}.json', multi(
                [T(TRADER_NAME[tr], 'gold', bold=True), T(' - Back Room', 'gray')],
                [body([T(intro, 'gray', italic=True)]), body([T('You are: ', 'dark_gray'), T(tier_name[t], TIERS[t][3], bold=True)])],
                buttons, columns=1))
        fn(f'p28/back/open_{ti}', [f'scoreboard players set @s bm.menu {MENU["back"] + ti}'] +
           [f'execute if score @s bm.tier matches {t} run return run dialog show @s bm:p28/back_{tr}_{t}' for t in range(1, 5)] +
           [f'dialog show @s bm:p28/back_{tr}_0'])
        # handlers
        hb = [f'execute unless score @s bm.menu matches {MENU["back"] + ti} run return run function bm:p28/stale',
              f'execute unless entity @e[type=minecraft:interaction,tag=bm.ledger,distance=..8,scores={{bm.lgid={ti}}}] run return run function bm:p28/stale']
        hb += [f'execute if score #act bm.pay matches {1000 + ti * 20 + i} run return run function bm:p28/back/buy_{ti}_{i}' for i in range(len(stock))]
        fn(f'p28/back/act_{ti}', hb)
        act.append(f'execute if score #act bm.pay matches {1000 + ti * 20}..{1000 + ti * 20 + 19} run return run function bm:p28/back/act_{ti}')
        for i, (req, what, n, (cur, price), label) in enumerate(stock):
            broke = 'function bm:p28/back/broke {m:"%s"}' % f'That one costs {cur_text(cur, price)}.'
            fn(f'p28/back/buy_{ti}_{i}', [f'execute unless score @s bm.tier matches {req}.. run return run function bm:p28/back/locked'] +
               pay_lines(cur, price, broke) + give_cmds(what, n) +
               ['playsound minecraft:entity.villager.yes neutral @s ~ ~ ~ 0.8 1.2', 'playsound minecraft:block.chest.close player @s ~ ~ ~ 0.5 1.2',
                title('@s', 'actionbar', [T(f'{TRADER_NAME[tr]}: ', 'gold'), T(f'{label} - pleasure doing business.', 'white')])])
    fn('p28/back/act', act)
    fn('p28/back/locked', [title('@s', 'actionbar', T('Your Standing is too low for that shelf.', 'red')), 'playsound minecraft:entity.villager.no neutral @s ~ ~ ~ 0.8 1'])
    fn('p28/back/broke', ['$title @s actionbar {text:"$(m)",color:"red"}', 'playsound minecraft:entity.villager.no neutral @s ~ ~ ~ 0.8 1'])

    # ------------------------------------------------------------------ gates
    def tp_to(kind):
        pos, yaw, _ = GATE_DEST[kind]
        return f'execute at @e[type=minecraft:marker,tag=bm.mkt,distance=..120,sort=nearest,limit=1] rotated as @e[type=minecraft:marker,tag=bm.mkt,distance=..120,sort=nearest,limit=1] positioned {mgeo.rel(pos)} rotated ~{yaw} 0 run tp @s ~ ~ ~ ~ ~'
    key_ok = {'hall_in': ['silver_key', 'gold_key', 'rat_king_key'], 'vip_in': ['gold_key', 'rat_king_key'], 'den_in': ['rat_king_key']}
    for kind, keys in key_ok.items():
        fn(f'p28/gate/has_{kind}', ['execute if entity @s[gamemode=creative] run return 1'] +
           [f'execute if items entity @s container.* *[minecraft:custom_data~{{bm:"{k}"}}] run return 1' for k in keys] +
           [f'execute if items entity @s weapon.offhand *[minecraft:custom_data~{{bm:"{k}"}}] run return 1' for k in keys] + ['return 0'])
    shove = ['playsound minecraft:entity.silverfish.hurt hostile @s ~ ~ ~ 1 1.4',
             'execute at @s rotated as @e[type=minecraft:interaction,tag=bm.lgsel,limit=1] run tp @s ^ ^ ^0.6']
    fn('p28/gate/hall_in', ['execute if function bm:p28/gate/has_hall_in run return run function bm:p28/gate/enter_hall',
                            'execute if score #aopen bm.auc matches 1 run return run function bm:p28/gate/pass_menu',
                            title('@s', 'actionbar', T('Members only. A Silver Key or better - or come back on an auction night with a pass.', 'gray'))] + shove)
    fn('p28/gate/enter_hall', [tp_to('hall_in'), 'playsound minecraft:block.iron_door.open block @s ~ ~ ~ 0.8 0.8',
                               title('@s', 'actionbar', T('The bouncer rat waves you through.', 'gold')), 'function bm:p30/enter'])
    fn('p28/gate/hall_out', [tp_to('hall_out'), 'playsound minecraft:block.iron_door.close block @s ~ ~ ~ 0.8 0.8', 'function bm:p30/leave'])
    fn('p28/gate/vip_in', ['execute unless function bm:p28/gate/has_vip_in run return run function bm:p28/gate/vip_no',
                           tp_to('vip_in'), 'playsound minecraft:block.iron_door.open block @s ~ ~ ~ 0.8 0.9',
                           title('@s', 'actionbar', T('Welcome to the Gilded Gutter. Mind the carpet.', 'gold'))])
    fn('p28/gate/vip_no', [title('@s', 'actionbar', T('Members only. Partners carry a Gold Key.', 'gray'))] + shove)
    fn('p28/gate/vip_out', [tp_to('vip_out'), 'playsound minecraft:block.iron_door.close block @s ~ ~ ~ 0.8 0.9'])
    fn('p28/gate/den_in', ['execute unless function bm:p28/gate/has_den_in run return run function bm:p28/gate/den_no',
                           tp_to('den_in'), 'playsound minecraft:block.wooden_door.open block @s ~ ~ ~ 1 0.9',
                           title('@s', 'actionbar', T('"Family! Come in, come in." The crew makes room.', 'yellow'))])
    fn('p28/gate/den_no', [title('@s', 'actionbar', T('Crew and Family only. (There is always the mouse hole...)', 'gray'))] + shove)
    fn('p28/gate/den_out', [tp_to('den_out'), 'playsound minecraft:block.wooden_door.close block @s ~ ~ ~ 1 0.9'])
    # the one-night pass (auction nights only, below Associate): 2 Medallions, straight from the inventory
    wjson('bm/dialog/p28/pass.json', multi([T('The Dark Auction', 'gold', bold=True)],
                                          [body([T('"No key, no seat... unless you buy a one-night pass. Two Medallions, valid until the last lot."', 'gray', italic=True)])],
                                          [btn([T('Buy a one-night pass  ', 'white'), T('2 Medallions', 'light_purple')], 2001, width=240)], columns=1, exit_label='Not tonight'))
    fn('p28/gate/pass_menu', [f'scoreboard players set @s bm.menu {MENU["gate"] + 1}',
                              'execute if score @s bm.apass = #pgen bm.auc run return run function bm:p28/gate/enter_hall',
                              'dialog show @s bm:p28/pass'])
    fn('p28/gate/act', [f'execute unless score @s bm.menu matches {MENU["gate"] + 1} run return run function bm:p28/stale',
                        'execute unless entity @e[type=minecraft:interaction,tag=bm.ledger,distance=..8,scores={bm.lgid=21}] run return run function bm:p28/stale',
                        'execute unless score #aopen bm.auc matches 1 run return run ' + title('@s', 'actionbar', T('The sale is over for tonight.', 'gray')),
                        'execute if score #act bm.pay matches 2001 run function bm:p28/gate/buy_pass'])
    fn('p28/gate/buy_pass', pay_lines('medallion', 2, 'function bm:p28/back/broke {m:"Two Medallions, friend. Rules are rules."}') +
       ['scoreboard players operation @s bm.apass = #pgen bm.auc', tellraw('@s', PREFIX + [T('A one-night pass to the Dark Auction is yours. It lapses when the last lot is sold.', 'gold')]),
        'function bm:p28/gate/enter_hall'])

    # ================================================================== FAMILY PORTRAITS round Fountain Plaza
    # the roster lives in storage (up to four, first come); every market draws it from there
    fn('p28/portrait/join', ['execute if entity @s[tag=bm.fam] run return 0', 'tag @s add bm.fam',
                             'execute if data storage bm:family list[3] run return 0',
                             'function bm:p28/name/of',
                             'data modify storage bm:family list append from storage bm:tmp nm',
                             'scoreboard players add #famv bm.pay 1',
                             tellraw('@a', PREFIX + [{'selector': '@s', 'color': 'gold'}, T(' is now ', 'gray'), T('Family', 'light_purple', bold=True),
                                                     T('. Their portrait goes up in Fountain Plaza.', 'gray')])])
    # empty slots draw nothing: the plinth starts at scale 0, the head display holds no item, the label is blank
    for i, (pos, yaw) in enumerate(PORTRAITS):
        plinth = {'Tags': ['bm.e18', 'bm.n18', 'bm.plinth', f'bm.pp{i}'], 'block_state': 'minecraft:chiseled_polished_blackstone',
                  'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(-0.35), F(0), F(-0.35)], 'scale': [F(0)] * 3}}
        cap = {'Tags': ['bm.e18', 'bm.n18', 'bm.plinth', f'bm.pc{i}'], 'block_state': 'minecraft:gold_block',
               'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(-0.4), F(1.1), F(-0.4)], 'scale': [F(0)] * 3}}
        head = {'Tags': ['bm.e18', 'bm.n18', 'bm.phead', f'bm.ph{i}'], 'item_display': 'head',
                'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(1.62), F(0)], 'scale': [F(0.9)] * 3}}
        name = {'Tags': ['bm.e18', 'bm.n18', 'bm.pname', f'bm.pn{i}'], 'billboard': 'center', 'view_range': F(0.25), 'text': '',
                'default_background': B(0), 'background': Int(0x60000000),
                'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(2.3), F(0)], 'scale': [F(0.5)] * 3}}
        fn(f'p28/spawn/portrait_{i}', [f'summon minecraft:block_display ~ ~ ~ {snbt(plinth)}', f'summon minecraft:block_display ~ ~ ~ {snbt(cap)}',
                                       f'summon minecraft:item_display ~ ~ ~ {snbt(head)}', f'summon minecraft:text_display ~ ~ ~ {snbt(name)}', fin, untag])
        place(pos, yaw, f'p28/spawn/portrait_{i}', f'Family portrait {i}', region='public')
    # draw: an empty slot is invisible (scale 0); a filled one shows the head and the name
    draw = ['scoreboard players operation @s bm.pay = #famv bm.pay']
    for i in range(4):
        draw += [f'execute if data storage bm:family list[{i}] run function bm:p28/portrait/fill {{i:{i}}}']
    fn('p28/portrait/draw', draw)
    fn('p28/portrait/fill', ['$data modify storage bm:tmp pf set from storage bm:family list[$(i)]',
                             '$data merge entity @e[type=minecraft:block_display,tag=bm.pp$(i),distance=..80,limit=1] {transformation:{scale:[0.7f,1.1f,0.7f]}}',
                             '$data merge entity @e[type=minecraft:block_display,tag=bm.pc$(i),distance=..80,limit=1] {transformation:{scale:[0.8f,0.12f,0.8f]}}',
                             '$execute as @e[type=minecraft:item_display,tag=bm.ph$(i),distance=..80] run function bm:p28/portrait/head',
                             '$execute as @e[type=minecraft:text_display,tag=bm.pn$(i),distance=..80] run function bm:p28/portrait/label'])
    fn('p28/portrait/head', ['data modify entity @s item set value {id:"minecraft:player_head",count:1}',
                             'data modify entity @s item.components."minecraft:profile" set from storage bm:tmp pf.profile'])
    fn('p28/portrait/label', ['data modify entity @s text set value [{text:"",color:"gold",bold:true},{text:"Family",color:"light_purple",bold:true}]',
                              'data modify entity @s text[0].text set from storage bm:tmp pf.name'])
    second.append('execute as @e[type=minecraft:marker,tag=bm.mkt,tag=bm.i18] at @s unless score @s bm.pay = #famv bm.pay run function bm:p28/portrait/draw')
    load.append('execute unless score #famv bm.pay matches 0.. run scoreboard players set #famv bm.pay 0')

    # ================================================================== install (later phases append their spawns)
    second.append('function bm:p28/install_check')
    G.FUNCS['load'][-1:-1] = load
    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


def finalize(G):
    """Runs after every 1.18 phase added its spawns: write the install function and its trigger."""
    G.fn('p28/install', G.P28_INSTALL + ['scoreboard players set @s bm.pay -1'])
    corners = [(0.5, market2.W, 0.5), (market2.SX - 0.5, market2.W, 0.5), (0.5, market2.W, market2.SZ - 0.5), (market2.SX - 0.5, market2.W, market2.SZ - 0.5)]
    loaded = ' '.join(f'if loaded {mgeo.rel(c)}' for c in corners)
    G.fn('p28/install_check', [f'execute as @e[type=minecraft:marker,tag=bm.mkt,tag=!bm.i18] at @s rotated as @s {loaded} run function bm:p28/install'])
    G.FUNCS['admin/uninstall'][-1:-1] = ['kill @e[tag=bm.e18]'] + [f'scoreboard objectives remove {o}' for o in G.P28_OBJ]


# ===================================================================== RESOURCE PACK
def rp(R):
    from PIL import Image
    base = R.ICONS['market_key']

    def tint(im, lo, hi, accent=None):
        out = Image.new('RGBA', im.size)
        for y in range(im.size[1]):
            for x in range(im.size[0]):
                r, g, b, a = im.getpixel((x, y))
                if a == 0: continue
                if accent and (r, g, b) == (0xa9, 0x6b, 0xff):
                    out.putpixel((x, y), R.hexc(accent)); continue
                l = (0.3 * r + 0.59 * g + 0.11 * b) / 255
                out.putpixel((x, y), tuple(int(lo[i] + (hi[i] - lo[i]) * l) for i in range(3)) + (a,))
        return out
    R.ICONS['silver_key'] = tint(base, (40, 44, 52), (235, 240, 248), '#7fd4ff')
    R.ICONS['gold_key'] = tint(base, (60, 34, 4), (255, 226, 110), '#ff3b3b')
    rk = tint(base, (10, 8, 6), (255, 196, 40), '#ffffff')
    for (x, y) in [(2, 0), (4, 0), (6, 0), (3, 1), (5, 1)]:          # a tiny crown on the bow
        rk.putpixel((x, y), R.hexc('#ffd700'))
    R.ICONS['rat_king_key'] = rk
    # the ledger: an open book lying on a counter (3D, face = model north)
    R.HATS['statue_ledger'] = ({'c': 'minecraft:block/red_wool', 'p': 'minecraft:block/white_wool', 'l': 'minecraft:block/black_wool',
                                'g': 'minecraft:block/gold_block'}, [
        R.cube((2, 0, 3), (14, 0.6, 13), 'c'), R.cube((2.4, 0.6, 3.4), (7.8, 1.4, 12.6), 'p'), R.cube((8.2, 0.6, 3.4), (13.6, 1.4, 12.6), 'p'),
        R.cube((7.8, 0.6, 3), (8.2, 1.2, 13), 'l'), R.cube((3.2, 1.4, 5), (7, 1.45, 5.4), 'l'), R.cube((3.2, 1.4, 6.5), (6.4, 1.45, 6.9), 'l'),
        R.cube((9, 1.4, 5), (12.8, 1.45, 5.4), 'l'), R.cube((9, 1.4, 6.5), (12.2, 1.45, 6.9), 'l'), R.cube((12.6, 1.2, 10.5), (13.4, 1.6, 12.8), 'g')])

"""Phase 2.30: a day count that /time set can't scramble, and the Scrap Bin.

- DAYS: every schedule (Blood Moons, Lucky and Invasion Nights, the Dark Auction's week, paydays) used to count days from
  the world's total time, so `/time set 1000` sent the count back to day 0. The pack now counts sunrises itself: the count
  only ever goes up (a sunrise, a night slept through, or `time set` to an earlier hour all count as a new day).
  Worlds carry on from the day they were on.
- THE SCRAP BIN: a barrel that scraps what's put in it, once a second, for half what it cost - anything bought from a
  Black Market trader, a back room or Zorp. Something bought for 1 Token gives the Token back. Bundles go back as
  bundles (16 Spectral Arrows for the 3 Tokens they cost: 1 Token). Old Barnaby's buy-backs (gear found in the world,
  the Lucky 7) are in it too. Money itself is never scrapped. Every market has one at the end of Old Barnaby's counter;
  Barnaby sells them (3 Tokens) to place anywhere.
- Old Barnaby keeps his goofy goods, breaking Medallions and Trophies into change, and Tokens for Diamonds."""
from items import T, ITEMS, PRICES, CATEGORY
from nbt import snbt, B, F, Int

BIN_AT = (26, None, 20)            # the market's own bin: the west end of Barnaby's counter (template coords; y = W)
TOKEN_VALUE = {'token': 1, 'medallion': 9, 'trophy': 54}


def extend_offers(O, offer):
    from gen_dp import CURRENCY
    def iid(st):
        cd = st.get('components', {}).get('minecraft:custom_data')
        return cd['bm'] if isinstance(cd, dict) and 'bm' in cd else st['id'].split(':')[-1]
    # Barnaby's buy-backs move into the Scrap Bin: keep only trades that take money (change, diamonds, his goods)
    O['pawn'] = [o for o in O['pawn'] if iid(o['buy']) in CURRENCY | {'lucky_token'}]
    O['pawn'].append(offer(('token', 3), ('scrap_bin', 1)))


def refund_table(O, zorp, backroom):
    """id -> (k, [(currency, n), ...]): scrapping k of the item pays those back."""
    import economy
    from items import UPGRADES
    def iid(st):
        cd = st.get('components', {}).get('minecraft:custom_data')
        if isinstance(cd, dict) and 'bm' in cd: return cd['bm']
        return st['id'] if ':' in st['id'] else 'minecraft:' + st['id']
    def stackable(i):
        return i not in ITEMS or ITEMS[i]['comps'].get('minecraft:max_stack_size', 64 if ITEMS[i]['base'] != 'minecraft:totem_of_undying' else 1) > 1
    sales = []                        # (item, k, [(cost id, n)])
    for offers in O.values():
        for o in offers:
            costs = [(iid(o[b]), int(o[b]['count'])) for b in ('buy', 'buyB') if b in o]
            sales.append((iid(o['sell']), int(o['sell']['count']), costs))
    for buy, buyB, (s, k) in zorp:
        sales.append((s, k, [buy] + ([buyB] if buyB else [])))
    for (s, k, cost) in backroom:
        sales.append((s, k, [cost]))
    # money: anything a trader takes in stacks (Tokens, Crystals, Xenite, meats, Ectoplasm...) is never scrapped
    money = {c for _, _, costs in sales for c, _ in costs if c in ITEMS and stackable(c)}
    money |= {'token', 'medallion', 'trophy', 'lucky_token', 'lucky_trophy', 'blood_crystal'}
    vanilla_money = {'minecraft:diamond', 'minecraft:emerald', 'minecraft:netherite_ingot'}
    def half(c, n):
        if n >= 2: return [(c, n // 2)]
        return {'token': [('token', 1)], 'medallion': [('token', 4)], 'trophy': [('medallion', 3)]}.get(c, [(c, 1)])
    def value(costs):
        return sum(n * TOKEN_VALUE.get(c, 1000 if c in ITEMS else 1) for c, n in costs)
    best = {}
    for s, k, costs in sales:
        if s in money or s in vanilla_money or k < 1: continue
        if s not in best or value(costs) / k < value(best[s][1]) / best[s][0]: best[s] = (k, costs)
    upgraded = {to for _, _, _, to in UPGRADES}
    table = {}
    for s, (k, costs) in best.items():
        trade_in = [c for c, _ in costs if c in ITEMS and c not in money]
        if trade_in or s in upgraded:                         # an upgrade: half of the whole chain, as the pawn shop always paid
            if s in PRICES: table[s] = (1, [economy.pawn(s, PRICES[s])]); continue
            costs = [(c, n) for c, n in costs if c not in trade_in]
            if not costs: continue
        pay = []
        for c, n in costs: pay += half(c, n)
        table[s] = (k, pay)
    # Barnaby's old buy-backs for gear that's only found (never sold), and the Lucky 7
    for i, price in PRICES.items():
        if i not in table and CATEGORY.get(i) in ('gear', 'builder', 'cosmetic') and i != 'lucky_seven':
            table[i] = (1, [economy.pawn(i, price)])
    table['lucky_seven'] = (1, [('trophy', 3)])
    return table


def generate(G):
    fn, title, tellraw, PREFIX = G.fn, G.title, G.tellraw, G.PREFIX
    import mgeo, market2, phase24, phase32, phase28
    rel = mgeo.rel
    W = market2.W
    second = []

    # ================================================================ DAYS: count sunrises (the time of day going backwards)
    tk = G.FUNCS['bloodmoon/tick']
    k = tk.index('scoreboard players operation #tod bm.bm %= #24000 bm.bm')
    tk[k + 1:k + 1] = [
        'execute unless score #bmday bm.bm matches 0.. run scoreboard players operation #bmday bm.bm = #day bm.bm',     # (a world carries on from its day)
        'execute unless score #ptod bm.bm matches 0.. run scoreboard players operation #ptod bm.bm = #tod bm.bm',
        'execute if score #tod bm.bm < #ptod bm.bm run scoreboard players add #bmday bm.bm 1',
        'scoreboard players operation #ptod bm.bm = #tod bm.bm',
        'scoreboard players operation #day bm.bm = #bmday bm.bm']
    assert any('#cyc bm.bm = #day bm.bm' in l for l in tk[k + 6:]), 'the cycle must be read after the day count'

    # ================================================================ the refund table (storage bm:scrap table / money)
    O = G.P2_OFFERS() if hasattr(G, 'P2_OFFERS') else G.all_offers()
    zorp = [(b, bb, s) for b, bb, s in phase24.OFFERS if s[0] not in phase32._ALTAR_MADE]
    backroom = []
    for lst in phase28.BACKROOM.values():
        for _, what, n, cost, _ in lst:
            if what == 'treasure_map': continue
            backroom.append(('minecraft:enchanted_book' if what == 'mending_book' else what, n, cost))
    table = refund_table(O, zorp, backroom)
    G.SCRAP_TABLE = table
    cur = sorted({c for _, pay in table.values() for c, _ in pay})
    money_nbt = {c: dict(G.stack(c, 1)) for c in cur}
    for c, st in money_nbt.items(): st.pop('count', None)
    tab = {s: {'k': Int(k), 'r': [{'c': c, 'n': Int(n)} for c, n in pay]} for s, (k, pay) in table.items()}
    G.FUNCS['load'][-1:-1] = [f'data modify storage bm:scrap table set value {snbt(tab)}', f'data modify storage bm:scrap money set value {snbt(money_nbt)}']

    # ================================================================ the bin: every second, scrap what's inside
    S = 'storage bm:scrap'
    second.append('execute as @e[type=minecraft:marker,tag=bm.rs_scrap_bin] at @s if block ~ ~ ~ minecraft:barrel if data block ~ ~ ~ Items[0] run function bm:p51/bin')
    fn('p51/bin', [f'data modify {S} src set from block ~ ~ ~ Items', f'data modify {S} keep set value []', f'data modify {S} pay set value []',
                   'scoreboard players set #did bm.rng 0', 'function bm:p51/scan',
                   'execute if score #did bm.rng matches 0 run return 0',
                   f'data modify block ~ ~ ~ Items set from {S} keep', 'function bm:p51/payall',
                   'playsound minecraft:block.smithing_table.use block @a[distance=..12] ~ ~ ~ 0.7 1.3',
                   'particle minecraft:wax_off ~ ~0.7 ~ 0.3 0.2 0.3 0 8'])
    fn('p51/scan', [f'execute unless data {S} src[0] run return 0', f'data modify {S} it set from {S} src[0]', f'data remove {S} src[0]',
                    f'data remove {S} k', f'data remove {S} hit',
                    f'execute if data {S} it.components."minecraft:custom_data".bm run data modify {S} k.id set from {S} it.components."minecraft:custom_data".bm',
                    f'execute unless data {S} k.id if data {S} it.components."minecraft:custom_data".bm_from run data modify {S} k.id set from {S} it.id',
                    f'execute if data {S} k.id run function bm:p51/look with {S} k',
                    f'execute unless data {S} hit run data modify {S} keep append from {S} it',
                    f'execute if data {S} hit run function bm:p51/take', 'function bm:p51/scan'])
    fn('p51/look', [f'$execute if data {S} table."$(id)" run data modify {S} hit set from {S} table."$(id)"'])
    fn('p51/take', [f'execute store result score #n bm.rng run data get {S} it.count', f'execute store result score #k bm.rng run data get {S} hit.k',
                    'scoreboard players operation #times bm.rng = #n bm.rng', 'scoreboard players operation #times bm.rng /= #k bm.rng',
                    f'execute if score #times bm.rng matches 0 run return run data modify {S} keep append from {S} it',
                    'scoreboard players set #did bm.rng 1',
                    'scoreboard players operation #left bm.rng = #times bm.rng', 'scoreboard players operation #left bm.rng *= #k bm.rng',
                    'scoreboard players operation #n bm.rng -= #left bm.rng',
                    f'execute if score #n bm.rng matches 1.. store result {S} it.count int 1 run scoreboard players get #n bm.rng',
                    f'execute if score #n bm.rng matches 1.. run data modify {S} keep append from {S} it',
                    f'data modify {S} rs set from {S} hit.r', 'function bm:p51/rpay'])
    fn('p51/rpay', [f'execute unless data {S} rs[0] run return 0', f'execute store result score #pn bm.rng run data get {S} rs[0].n',
                    'scoreboard players operation #pn bm.rng *= #times bm.rng', f'data modify {S} pe set value {{}}', f'data modify {S} pe.c set from {S} rs[0].c',
                    f'execute store result {S} pe.n int 1 run scoreboard players get #pn bm.rng', f'data modify {S} pay append from {S} pe',
                    f'data remove {S} rs[0]', 'function bm:p51/rpay'])
    # pay out: full stacks into empty slots of the bin; anything that doesn't fit pops out on top
    fn('p51/payall', [f'execute unless data {S} pay[0] run return 0', f'execute store result score #pn bm.rng run data get {S} pay[0].n',
                      f'function bm:p51/money with {S} pay[0]', 'function bm:p51/stacks', f'data remove {S} pay[0]', 'function bm:p51/payall'])
    fn('p51/money', [f'$data modify {S} el set from {S} money."$(c)"'])
    fn('p51/stacks', ['execute if score #pn bm.rng matches ..0 run return 0', 'scoreboard players operation #m bm.rng = #pn bm.rng',
                      'execute if score #m bm.rng matches 65.. run scoreboard players set #m bm.rng 64', 'scoreboard players operation #pn bm.rng -= #m bm.rng',
                      f'execute store result {S} el.count int 1 run scoreboard players get #m bm.rng', 'scoreboard players set #pl bm.rng 0'] +
       [f'execute if score #pl bm.rng matches 0 unless items block ~ ~ ~ container.{i} * run function bm:p51/put {{s:{i}}}' for i in range(27)] +
       ['execute if score #pl bm.rng matches 0 run function bm:p51/spill', 'function bm:p51/stacks'])
    fn('p51/put', [f'$data modify {S} el.Slot set value $(s)b', f'data modify block ~ ~ ~ Items append from {S} el', f'data remove {S} el.Slot',
                   'scoreboard players set #pl bm.rng 1'])
    fn('p51/spill', ['summon minecraft:item ~ ~0.8 ~ {Item:{id:"minecraft:stone",count:1},Tags:["bm.spill"]}',
                     f'data modify entity @e[type=minecraft:item,tag=bm.spill,limit=1,sort=nearest] Item set from {S} el',
                     'tag @e[type=minecraft:item,tag=bm.spill] remove bm.spill'])

    # ================================================================ every market gets a bin at the end of Barnaby's counter
    x, _, z = BIN_AT
    mgeo.need_air((x, W, z), 'the Scrap Bin by Old Barnaby')
    label = snbt({'Tags': ['bm.scraplabel'], 'billboard': 'center', 'text': [T('Scrap Bin\n', '#c89060', bold=True), T('half back on Black Market goods', 'gray')],
                  'background': Int(0x60000000), 'line_width': Int(160),
                  'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)], 'translation': [F(0), F(0), F(0)], 'scale': [F(0.55)] * 3}})
    p41 = next(l for l in G.FUNCS['loop/second'] if 'function bm:p41/patch' in l)
    second.append(p41.replace('tag=!bm.p41]', 'tag=!bm.p51]').replace('function bm:p41/patch', 'function bm:p51/market'))
    fn('p51/market', ['tag @s add bm.p51', f'execute positioned {rel((x + 0.5, W + 0.5, z + 0.5))} run function bm:p51/market_bin'])
    fn('p51/market_bin', ['execute unless block ~ ~ ~ #minecraft:replaceable unless block ~ ~ ~ minecraft:barrel run return 0',
                          'setblock ~ ~ ~ minecraft:barrel[facing=up]', 'data merge block ~ ~ ~ {CustomName:' + snbt(T('Scrap Bin', '#c89060')) + '}',
                          'kill @e[type=minecraft:marker,tag=bm.rs,distance=..0.3]',
                          'summon minecraft:marker ~ ~ ~ {Tags:["bm.rs","bm.rs_scrap_bin","bm.mktbin"]}',
                          'kill @e[type=minecraft:text_display,tag=bm.scraplabel,distance=..2]', f'summon minecraft:text_display ~ ~0.95 ~ {label}'])

    s = G.FUNCS['loop/second']
    s[-1:-1] = second

"""Phase 1.18 (part 4): THE GILDED GUTTER - the Partners' lounge behind the terrace (Gold Key or better at its gate).

- THE CONCIERGE sells three goods that change every in-game week (regular Dark Auction lots, at their opening bid
  in Medallions) and repairs the item in your main hand for 1 Medallion (a full repair; unbreakable things politely
  refused). Paid by menu - no villager trade, so no trader's offers change.
- THE RAT BANK (the Teller): Tokens, Lucky Tokens, Medallions and Trophies kept as separate balances against your
  name - safe from death, lava and thieves. Deposit everything of one kind, or take 1, 10 or all of it back as real
  items. The Dark Auction draws on your Medallion balance when your pockets run short. A Banker's Card opens the
  account anywhere. Interest is off by default (/function bm:admin/bank_interest_on: 1 Token per 50 held, paid when
  each Dark Auction closes).
The lounge gets two counters (plain blocks, so they sit right in any rotation) - nothing outside the sealed room
changes. Importing does nothing; generate(G) runs after phase30.generate."""
from nbt import snbt, B, F, Int
from items import T, ITEMS
import mgeo
import market3 as market2

W, BF = market2.W, market2.BF
SAVE_PER, SAVE_DAYS = 25, 7                          # (2.82b) savings: 1 a day per 25 kept; days away paid up to a week
SAVE_PCT = 100 // SAVE_PER
SAVE_CAP = {'token': 8, 'lucky_token': 8, 'medallion': 3, 'trophy': 1}
SAVE_CAP_ELSE = 4                                    # (any other currency the bank comes to keep)
BANK = [('token', 'bm.bk_tok', 'Tokens', 'gold'), ('lucky_token', 'bm.bk_luck', 'Lucky Tokens', 'green'),
        ('medallion', 'bm.bk_med', 'Medallions', 'light_purple'), ('trophy', 'bm.bk_tro', 'Trophies', '#ffb300')]
COUNTERS = {'concierge': ([(50, BF + 1, 5), (51, BF + 1, 5), (52, BF + 1, 5)], 'minecraft:dark_oak_planks'),
            'teller': ([(58, BF + 1, 5), (59, BF + 1, 5), (60, BF + 1, 5)], 'minecraft:polished_blackstone_bricks')}
NPC = {'concierge': (41, (51.5, BF + 1, 4.5), 0, 'concierge', 'The Concierge', 'right-click: exclusive stock & repairs'),
       'teller': (42, (59.5, BF + 1, 4.5), 0, 'teller', 'The Teller', 'right-click: your Rat Bank account')}


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    import phase28 as P28
    tick, fast, second, load = [], [], [], []
    ident = [F(0), F(0), F(0), F(1)]
    objs = ['bm.bk_tok dummy', 'bm.bk_luck dummy', 'bm.bk_tro dummy']
    load += [f'scoreboard objectives add {o}' for o in objs]
    G.FUNCS['admin/uninstall'][-1:-1] = [f'scoreboard objectives remove {o.split()[0]}' for o in objs]

    # ------------------------------------------------------------------ the room: two counters + two rats
    place = G.P28_PLACE
    wjson('bm/tags/block/p31_soft.json', {'values': ['#minecraft:air', 'minecraft:light', 'minecraft:red_carpet', 'minecraft:black_carpet']})
    patch = []
    for who, (cells, block) in COUNTERS.items():
        for (x, y, z) in cells:
            if not mgeo.passable((x, y, z)): raise SystemExit(f'phase31: counter cell {(x, y, z)} is {mgeo.st((x, y, z))}')
            patch.append(f'execute positioned {mgeo.rel((x + 0.5, y + 0.5, z + 0.5))} if block ~ ~ ~ #bm:p31_soft run setblock ~ ~ ~ {block}')
    fn('p31/counters', patch)
    G.P28_INSTALL.append('function bm:p31/counters')
    fin = 'execute rotated ~ 0 run tp @e[tag=bm.n18,distance=..1.5] ~ ~ ~ ~ ~'
    untag = 'tag @e[tag=bm.n18,distance=..1.5] remove bm.n18'
    for who, (lid, pos, yaw, v, nm, hint) in NPC.items():
        rat = G.rat_sprite(f'bm:rat_{v}', ['bm.e18', 'bm.n18', 'bm.rat_sprite', f'bm.g_{who}'])
        box = {'Tags': ['bm.e18', 'bm.n18', 'bm.ledger'], 'response': B(1), 'width': F(0.9), 'height': F(1.4)}
        plate = {'Tags': ['bm.e18', 'bm.n18'], 'billboard': 'center', 'view_range': F(0.2), 'default_background': B(0), 'background': Int(0x60000000),
                 'text': [T(nm, 'gold', bold=True), T('\n' + hint, 'gray')],
                 'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(1.45), F(0)], 'scale': [F(0.45)] * 3}}
        fn(f'p31/spawn/{who}', [rat, f'summon minecraft:interaction ~ ~ ~ {snbt(box)}',
                                f'scoreboard players set @e[type=minecraft:interaction,tag=bm.n18,distance=..1.5] bm.lgid {lid}',
                                f'summon minecraft:text_display ~ ~ ~ {snbt(plate)}', fin, untag])
        place(pos, yaw, f'p31/spawn/{who}', nm, region='gutter')
    op = G.FUNCS['p28/ledger/open']
    op += ['execute if score #lg bm.pay matches 41 run return run function bm:p31/conc/open', 'execute if score #lg bm.pay matches 42 run return run function bm:p31/bank/open']

    # ------------------------------------------------------------------ the Rat Bank
    near_or_card = ['execute if entity @e[type=minecraft:interaction,tag=bm.ledger,distance=..8,scores={bm.lgid=42}] run return 1',
                    'execute if items entity @s container.* *[minecraft:custom_data~{bm:"bankers_card"}] run return 1',
                    'execute if items entity @s weapon.offhand *[minecraft:custom_data~{bm:"bankers_card"}] run return 1', 'return 0']
    fn('p31/bank/can', near_or_card)
    fn('p31/bank/card', ['execute if score @s bm.rcd2 matches 1.. run return 0', 'scoreboard players set @s bm.rcd2 10', 'function bm:p31/bank/open'])
    op_lines = [f'scoreboard players set @s bm.menu {P28.MENU["bank"]}', 'data remove storage bm:ui bk']
    for cur, obj, nm, col in BANK:
        op_lines += [f'execute unless score @s {obj} matches 0.. run scoreboard players set @s {obj} 0',
                     f'execute store result storage bm:ui bk.{cur} int 1 run scoreboard players get @s {obj}']
    op_lines += ['data modify storage bm:ui bk.sv set value "Savings: none yet - the Teller in the Gilded Gutter opens one."',
                 f'execute if score @s bm.bksv matches 1 run data modify storage bm:ui bk.sv set value "Savings: open - {SAVE_PCT}% a day on every currency here."']
    op_lines += ['data modify storage bm:ui bk.ac set value "off"', 'execute if score @s bm.bkac matches 1 run data modify storage bm:ui bk.ac set value "ON"']
    op_lines.append('function bm:p31/bank/dlg with storage bm:ui bk')
    fn('p31/bank/open', op_lines)
    # 2.80: a page per currency. The account page lists every currency with its balance (one button each); a currency's
    # page shows its icon, what's in the account and what's on you, and the four actions - and an action brings you back
    # to that page. (The four action codes per currency are the 2.76 ones, unchanged.)
    bank_code = lambda i, k: 4010 + 4 * i + k
    page_code = lambda i: 4060 + i
    DEP_ALL, BACK, SAVE = 4071, 4072, 4073
    assert bank_code(len(BANK) - 1, 3) < page_code(0) and page_code(len(BANK) - 1) < DEP_ALL, 'the Rat Bank has outgrown its codes'
    btns = [P28.btn([T(nm, col), T('   $(' + cur + ')', 'white')], page_code(i), tooltip=T(f'Deposit or take out your {nm}', 'gray'), width=150)
            for i, (cur, obj, nm, col) in enumerate(BANK)]
    btns.append(P28.btn(T('Deposit everything', 'gold'), DEP_ALL, tooltip=T('Every currency the bank keeps, from your pockets into your account', 'gray'), width=150))
    btns.append(P28.btn(T('Savings account', '#7aff7a'), SAVE, tooltip=T('Daily interest on what you keep here - the Teller opens one', 'gray'), width=150))
    # (2.83) THE EXCHANGE: change Tokens, Medallions and Trophies in your account up or down - at the Fence's rates both ways
    EXCH = 4074                                       # the page; 4075-4078 its four swaps
    import economy as _EC
    TPM, MPT = _EC.TOKENS_PER_MEDALLION, _EC.MEDALLIONS_PER_TROPHY
    btns.append(P28.btn(T('Exchange', '#7ad8ff'), EXCH, tooltip=T('Change Tokens, Medallions and Trophies in your account - no fee, either way', 'gray'), width=150))
    # (2.83) AUTO-DEPOSIT, on the card: once a second, every currency the bank keeps goes from your pockets into your account
    # (Tokens above 8 - a heist's fee stays on you); it rests 30 seconds after you take anything out; never in the gutter
    AUTO, KEEP_TOK = 4079, 8
    btns.append(P28.btn([T('Auto-deposit: ', '#c8ffb0'), T('$(ac)', 'white')], AUTO,
                        tooltip=T(f'While you carry the card, what the bank keeps goes straight into your account (you keep {KEEP_TOK} Tokens for fees)', 'gray'), width=150))
    dlg = P28.multi([T('The Rat Bank', 'gold', bold=True), T(' - your account', 'gray')],
                    [P28.body([T('Pick a currency to deposit or take out.', 'gray')], 300),
                     P28.body([T('$(sv)', '#7aff7a')], 300),
                     P28.body([T('Kept against your name: safe from death, lava and thieves. The Dark Auction can draw on your Medallions.', 'dark_gray')], 300)],
                    btns, columns=2)
    fn('p31/bank/dlg', [f'$dialog show @s {P28.inline(dlg)}'])
    G.FUNCS['p28/act'].append('execute if score #act bm.pay matches 4000..4099 run return run function bm:p31/bank/act')
    act = [f'execute unless score @s bm.menu matches {P28.MENU["bank"]} run return run function bm:p28/stale',
           'execute unless function bm:p31/bank/can run return run function bm:p28/stale',
           f'execute if score #act bm.pay matches {DEP_ALL} run return run function bm:p31/bank/dep_every',
           f'execute if score #act bm.pay matches {BACK} run return run function bm:p31/bank/open',
           f'execute if score #act bm.pay matches {SAVE} run return run function bm:p31/sav/btn',
           f'execute if score #act bm.pay matches {EXCH} run return run function bm:p31/bank/xpage'] + \
          [f'execute if score #act bm.pay matches {EXCH + 1 + k} run return run function bm:p31/bank/x{k}' for k in range(4)] + \
          [f'execute if score #act bm.pay matches {AUTO} run return run function bm:p31/bank/ac_toggle']
    fn('p31/bank/ac_toggle', ['execute unless function bm:p31/bank/card_on run return run ' + title('@s', 'actionbar', T('Auto-deposit works from the Banker\'s Card - carry one.', 'gray')),
                              'execute if score @s bm.bkac matches 1 run scoreboard players set @s bm.bkac 2',
                              'execute unless score @s bm.bkac matches 2 run scoreboard players set @s bm.bkac 1',
                              'execute if score @s bm.bkac matches 2 run scoreboard players set @s bm.bkac 0',
                              'playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.3', 'function bm:p31/bank/open'])
    fn('p31/bank/card_on', ['execute if items entity @s container.* *[minecraft:custom_data~{bm:"bankers_card"}] run return 1',
                            'execute if items entity @s weapon.offhand *[minecraft:custom_data~{bm:"bankers_card"}] run return 1', 'return 0'])
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.bkac dummy', 'scoreboard objectives add bm.bkag dummy']
    G.OBJECTIVES += ['bm.bkac', 'bm.bkag']
    G.FUNCS['loop/second'] += ['scoreboard players remove @a[scores={bm.bkag=1..}] bm.bkag 1',
                               'execute as @a[scores={bm.bkac=1},gamemode=!spectator] unless score @s bm.bkag matches 1.. at @s unless dimension bm:gutter if function bm:p31/bank/card_on run function bm:p31/bank/auto']
    auto = ['scoreboard players set #atot bm.pay 0']
    for cur, obj, nm, col in BANK:
        has = f'*[minecraft:custom_data~{{bm:"{cur}"}}]'
        if cur == 'token':
            auto += [f'execute store result score #n bm.pay run clear @s {has} 0', f'execute if score #n bm.pay matches {KEEP_TOK + 1}.. run function bm:p31/bank/auto_tok']
            continue
        auto += [f'execute store result score #n bm.pay run clear @s {has}', f'scoreboard players operation @s {obj} += #n bm.pay', 'scoreboard players operation #atot bm.pay += #n bm.pay']
    auto += ['execute if score #atot bm.pay matches 1.. run playsound minecraft:block.chain.place player @s ~ ~ ~ 0.3 1.8']
    fn('p31/bank/auto', auto)
    fn('p31/bank/auto_tok', [f'scoreboard players remove #n bm.pay {KEEP_TOK}', 'execute store result storage bm:ui at.n int 1 run scoreboard players get #n bm.pay',
                             'scoreboard players operation @s bm.bk_tok += #n bm.pay', 'scoreboard players operation #atot bm.pay += #n bm.pay',
                             'function bm:p31/bank/auto_tok_m with storage bm:ui at'])
    fn('p31/bank/auto_tok_m', ['$clear @s *[minecraft:custom_data~{bm:"token"}] $(n)'])
    # the swaps, on the account (bm.bk_tok / bm.bk_med / bm.bk_tro), then back to the page
    XS = [('bm.bk_tok', TPM, 'bm.bk_med', 1, f'{TPM} Tokens', '1 Medallion'), ('bm.bk_med', 1, 'bm.bk_tok', TPM, '1 Medallion', f'{TPM} Tokens'),
          ('bm.bk_med', MPT, 'bm.bk_tro', 1, f'{MPT} Medallions', '1 Trophy'), ('bm.bk_tro', 1, 'bm.bk_med', MPT, '1 Trophy', f'{MPT} Medallions')]
    for k, (src, n, dst, m, a, b_) in enumerate(XS):
        fn(f'p31/bank/x{k}', [f'execute unless score @s {src} matches {n}.. run return run function bm:p31/bank/xshort {{a:"{a}"}}',
                              f'scoreboard players remove @s {src} {n}', f'scoreboard players add @s {dst} {m}',
                              'playsound minecraft:block.chain.place player @s ~ ~ ~ 0.6 1.6',
                              title('@s', 'actionbar', [T(a, 'gray'), T(' \u2192 ', 'white'), T(b_, 'gold')]), 'function bm:p31/bank/xpage'])
    fn('p31/bank/xshort', ['$' + title('@s', 'actionbar', T('Your account needs $(a) for that.', 'gray')), 'function bm:p31/bank/xpage'])
    xpg = P28.multi([T('The Exchange', '#7ad8ff', bold=True), T('  \u00b7  The Rat Bank', 'gray')],
                    [P28.body([T('In your account: ', 'gray'), T('$(t) Tokens', 'gold'), T('  \u00b7  ', 'dark_gray'), T('$(m) Medallions', 'light_purple'),
                               T('  \u00b7  ', 'dark_gray'), T('$(r) Trophies', '#ffb300')], 300),
                     P28.body([T(f'{TPM} Tokens make a Medallion, {MPT} Medallions a Trophy - and they break back down the same. No fee.', 'dark_gray')], 300)],
                    [P28.btn([T(f'{TPM} Tokens', 'gold'), T(' \u2192 ', 'white'), T('1 Medallion', 'light_purple')], EXCH + 1, width=150),
                     P28.btn([T('1 Medallion', 'light_purple'), T(' \u2192 ', 'white'), T(f'{TPM} Tokens', 'gold')], EXCH + 2, width=150),
                     P28.btn([T(f'{MPT} Medallions', 'light_purple'), T(' \u2192 ', 'white'), T('1 Trophy', '#ffb300')], EXCH + 3, width=150),
                     P28.btn([T('1 Trophy', '#ffb300'), T(' \u2192 ', 'white'), T(f'{MPT} Medallions', 'light_purple')], EXCH + 4, width=150),
                     P28.btn(T('\u00ab Your account', 'gray'), BACK, width=150)], columns=2)
    fn('p31/bank/xpage', [f'scoreboard players set @s bm.menu {P28.MENU["bank"]}'] +
       [f'execute unless score @s {o} matches 0.. run scoreboard players set @s {o} 0' for o in ('bm.bk_tok', 'bm.bk_med', 'bm.bk_tro')] +
       ['data remove storage bm:ui bkx', 'execute store result storage bm:ui bkx.t int 1 run scoreboard players get @s bm.bk_tok',
        'execute store result storage bm:ui bkx.m int 1 run scoreboard players get @s bm.bk_med',
        'execute store result storage bm:ui bkx.r int 1 run scoreboard players get @s bm.bk_tro', 'function bm:p31/bank/xdlg with storage bm:ui bkx'])
    fn('p31/bank/xdlg', [f'$dialog show @s {P28.inline(xpg)}'])
    for i, (cur, obj, nm, col) in enumerate(BANK):
        has = f'*[minecraft:custom_data~{{bm:"{cur}"}}]'
        act += [f'execute if score #act bm.pay matches {page_code(i)} run return run function bm:p31/bank/page_{cur}',
                f'execute if score #act bm.pay matches {bank_code(i, 0)} run return run function bm:p31/bank/dep_{cur}',
                f'execute if score #act bm.pay matches {bank_code(i, 1)} run return run function bm:p31/bank/take_{cur} {{n:1}}',
                f'execute if score #act bm.pay matches {bank_code(i, 2)} run return run function bm:p31/bank/take_{cur} {{n:10}}',
                f'execute if score #act bm.pay matches {bank_code(i, 3)} run return run function bm:p31/bank/take_all_{cur}']
        # ---- its page
        mdl = ITEMS[cur]['comps'].get('minecraft:item_model')
        icon = {'id': ITEMS[cur]['base'], 'count': Int(1), 'components': {'minecraft:item_name': T(nm, col)}}
        if mdl: icon['components']['minecraft:item_model'] = mdl
        pg = P28.multi([T(nm, col, bold=True), T('  ·  The Rat Bank', 'gray')],
                       [{'type': 'minecraft:item', 'item': icon, 'show_decorations': B(0), 'show_tooltip': B(1), 'width': Int(22), 'height': Int(22),
                         'description': {'contents': [T('In your account: ', 'gray'), T('$(n)', col, bold=True), T(chr(10) + 'On you: ', 'gray'), T('$(h)', 'white')],
                                         'width': Int(220)}}],
                       [P28.btn([T('Deposit all ', 'white'), T(nm, col), T('  ($(h))', 'gray')], bank_code(i, 0), tooltip=T(f'Every {nm[:-1] if nm.endswith("s") else nm} you carry, into your account', 'gray'), width=150),
                        P28.btn(T('Take 1', 'gray'), bank_code(i, 1), width=150), P28.btn(T('Take 10', 'gray'), bank_code(i, 2), width=150),
                        P28.btn([T('Take all', 'gray'), T('  ($(n))', 'dark_gray')], bank_code(i, 3), width=150),
                        P28.btn(T('« Your account', 'gray'), BACK, width=150)], columns=2)
        fn(f'p31/bank/page_{cur}', [f'scoreboard players set @s bm.menu {P28.MENU["bank"]}', f'execute unless score @s {obj} matches 0.. run scoreboard players set @s {obj} 0',
                                    'data remove storage bm:ui bkp', f'execute store result storage bm:ui bkp.n int 1 run scoreboard players get @s {obj}',
                                    f'execute store result storage bm:ui bkp.h int 1 run clear @s {has} 0',
                                    f'function bm:p31/bank/pdlg_{cur} with storage bm:ui bkp'])
        fn(f'p31/bank/pdlg_{cur}', [f'$dialog show @s {P28.inline(pg)}'])
        # ---- deposits (quietly, for 'everything'; with a word and back to the page, for one)
        fn(f'p31/bank/depq_{cur}', [f'execute store result score #n bm.pay run clear @s {has} 0', 'execute if score #n bm.pay matches 0 run return 0',
                                    f'clear @s {has}', f'scoreboard players operation @s {obj} += #n bm.pay', 'scoreboard players operation #tot bm.pay += #n bm.pay', 'return 1'])
        fn(f'p31/bank/dep_{cur}', ['scoreboard players set #tot bm.pay 0', f'function bm:p31/bank/depq_{cur}',
                                   'execute if score #tot bm.pay matches 0 run ' + title('@s', 'actionbar', T(f'You have no {nm} on you.', 'gray')),
                                   'execute if score #tot bm.pay matches 1.. run playsound minecraft:block.chain.place player @s ~ ~ ~ 0.8 1.4',
                                   'execute if score #tot bm.pay matches 1.. run ' + title('@s', 'actionbar', [T('Deposited ', 'gray'), {'score': {'name': '#tot', 'objective': 'bm.pay'}, 'color': col}, T(f' {nm}.', 'gray')]),
                                   f'function bm:p31/bank/page_{cur}'])
        fn(f'p31/bank/take_{cur}', ['scoreboard players set @s bm.bkag 30', '$scoreboard players set #n bm.pay $(n)', f'scoreboard players operation #n bm.pay < @s {obj}',
                                    'execute if score #n bm.pay matches ..0 run ' + title('@s', 'actionbar', T(f'No {nm} in your account.', 'gray')),
                                    f'execute if score #n bm.pay matches ..0 run return run function bm:p31/bank/page_{cur}',
                                    f'scoreboard players operation @s {obj} -= #n bm.pay',
                                    'execute store result storage bm:tmp bk.n int 1 run scoreboard players get #n bm.pay',
                                    f'function bm:p31/bank/give_{cur} with storage bm:tmp bk',
                                    'playsound minecraft:block.chain.break player @s ~ ~ ~ 0.8 1.4', f'function bm:p31/bank/page_{cur}'])
        fn(f'p31/bank/take_all_{cur}', ['scoreboard players set @s bm.bkag 30', f'scoreboard players operation #n bm.pay = @s {obj}',
                                        'execute if score #n bm.pay matches ..0 run ' + title('@s', 'actionbar', T(f'No {nm} in your account.', 'gray')),
                                        f'execute if score #n bm.pay matches ..0 run return run function bm:p31/bank/page_{cur}',
                                        f'scoreboard players set @s {obj} 0', f'function bm:p31/bank/loop_{cur}',
                                        'playsound minecraft:block.chain.break player @s ~ ~ ~ 0.8 1.2', f'function bm:p31/bank/page_{cur}'])
        # hand back in stacks of 64 (16 for Trophies)
        stack_n = ITEMS[cur]['comps'].get('minecraft:max_stack_size', 64)
        fn(f'p31/bank/loop_{cur}', [f'scoreboard players set #k bm.pay {stack_n}', 'scoreboard players operation #k bm.pay < #n bm.pay',
                                    'execute store result storage bm:tmp bk.n int 1 run scoreboard players get #k bm.pay',
                                    f'function bm:p31/bank/give_{cur} with storage bm:tmp bk', 'scoreboard players operation #n bm.pay -= #k bm.pay',
                                    f'execute if score #n bm.pay matches 1.. run function bm:p31/bank/loop_{cur}'])
        fn(f'p31/bank/give_{cur}', [f'$give @s {G.item_arg(cur)} $(n)'])
    fn('p31/bank/dep_every', ['scoreboard players set #tot bm.pay 0'] + [f'function bm:p31/bank/depq_{cur}' for cur, *_r in BANK] +
       ['execute if score #tot bm.pay matches 0 run ' + title('@s', 'actionbar', T('You carry nothing the bank keeps.', 'gray')),
        'execute if score #tot bm.pay matches 1.. run playsound minecraft:block.chain.place player @s ~ ~ ~ 0.8 1.2',
        'execute if score #tot bm.pay matches 1.. run ' + title('@s', 'actionbar', [T('Deposited ', 'gray'), {'score': {'name': '#tot', 'objective': 'bm.pay'}, 'color': 'gold'}, T(' in all.', 'gray')]),
        'function bm:p31/bank/open'])
    fn('p31/bank/act', act)
    # optional interest (off by default): 1 Token per 50 held, paid when each Dark Auction closes
    load.append('execute unless score #interest bm.pay matches 0.. run scoreboard players set #interest bm.pay 0')
    load.append('scoreboard players set #50 bm.pay 50')
    G.FUNCS['p30/close'].append('execute if score #interest bm.pay matches 1 run function bm:p31/bank/interest')
    fn('p31/bank/interest', ['execute as @a[scores={bm.bk_tok=50..}] run function bm:p31/bank/interest1'])
    fn('p31/bank/interest1', ['scoreboard players operation #i bm.pay = @s bm.bk_tok', 'scoreboard players operation #i bm.pay /= #50 bm.pay',
                              'scoreboard players operation @s bm.bk_tok += #i bm.pay',
                              tellraw('@s', PREFIX + [T('The Rat Bank paid you ', 'gray'), {'score': {'name': '#i', 'objective': 'bm.pay'}, 'color': 'gold'}, T(' Tokens of interest.', 'gray')])])
    fn('admin/bank_interest_on', ['scoreboard players set #interest bm.pay 1', tellraw('@s', PREFIX + [T('Rat Bank interest ON (1 Token per 50, each Dark Auction).', 'gray')])])
    # ------------------------------------------------------------------ (2.82b) SAVINGS: opened at the Teller, paid every day
    # (the Banker's Card took the Teller's old job - anywhere - so reaching him now opens what only he can: a savings account.
    #  Every in-game day, 1 in 25 of each currency kept here, capped a day; days you're away are paid when you're back, up to a week)
    load += ['scoreboard objectives add bm.bksv dummy', 'scoreboard objectives add bm.bkday dummy', 'scoreboard objectives add bm.bkint dummy']
    G.OBJECTIVES += ['bm.bksv', 'bm.bkday', 'bm.bkint']
    at_teller = 'entity @e[type=minecraft:interaction,tag=bm.ledger,distance=..8,scores={bm.lgid=42}]'
    fn('p31/sav/btn', ['execute if score @s bm.bksv matches 1 run return run function bm:p31/sav/page',
                       f'execute if {at_teller} run return run function bm:p31/sav/open',
                       title('@s', 'actionbar', [T('Savings accounts are opened in person: ', 'gray'), T('the Teller, in the Gilded Gutter', 'gold')]),
                       'function bm:p31/bank/open'])
    fn('p31/sav/open', ['scoreboard players set @s bm.bksv 1', 'scoreboard players operation @s bm.bkday = #day bm.bm', 'scoreboard players set @s bm.bkint 0',
                        'playsound minecraft:block.chiseled_bookshelf.insert player @s ~ ~ ~ 1 1.2', 'playsound minecraft:entity.villager.yes player @s ~ ~ ~ 0.6 1.4',
                        tellraw('@s', PREFIX + [T('The Teller: ', 'gold', bold=True),
                                                T(f'"A savings account, then. Every day the bank adds {SAVE_PCT}% of everything you keep with us. '
                                                  'Even on days you\'re away, up to a week. Pleasure doing business."', 'gray')]),
                        'function bm:p31/sav/page'])
    rate_lines = [P28.body([T(nm, col, bold=True), T(f': 1 a day for every {SAVE_PER} kept (up to {SAVE_CAP.get(cur, SAVE_CAP_ELSE)} a day)', 'gray')], 300) for cur, obj, nm, col in BANK]
    sp = P28.multi([T('Savings', '#7aff7a', bold=True), T('  ·  The Rat Bank', 'gray')],
                   [P28.body([T(f'Open. Every in-game day the bank adds {SAVE_PCT}% of each currency in your account:', 'gray')], 300)] + rate_lines +
                   [P28.body([T('Days you\'re away are paid when you\'re back, up to a week. Paid in so far: ', 'gray'), T('$(int)', 'white'), T(' (all currencies).', 'gray')], 300)],
                   [P28.btn(T('« Back to your account', 'gray'), BACK, width=200)], columns=1)
    fn('p31/sav/page', [f'scoreboard players set @s bm.menu {P28.MENU["bank"]}', 'execute store result storage bm:ui sv.int int 1 run scoreboard players get @s bm.bkint',
                        'function bm:p31/sav/pdlg with storage bm:ui sv'])
    fn('p31/sav/pdlg', [f'$dialog show @s {P28.inline(sp)}'])
    second.append('execute as @a[scores={bm.bksv=1}] at @s unless score @s bm.bkday = #day bm.bm run function bm:p31/sav/due')
    fn('p31/sav/due', ['scoreboard players operation #sd bm.pay = #day bm.bm', 'scoreboard players operation #sd bm.pay -= @s bm.bkday',
                       'scoreboard players operation @s bm.bkday = #day bm.bm',
                       'execute if score #sd bm.pay matches ..0 run return 0',          # (the day counter went back: nothing owed)
                       f'execute if score #sd bm.pay matches {SAVE_DAYS + 1}.. run scoreboard players set #sd bm.pay {SAVE_DAYS}'] +
       [f'scoreboard players set #g_{cur} bm.pay 0' for cur, *_r in BANK] +
       ['function bm:p31/sav/day'] +
       ['scoreboard players set #gt bm.pay 0'] + [f'scoreboard players operation #gt bm.pay += #g_{cur} bm.pay' for cur, *_r in BANK] +
       ['execute if score #gt bm.pay matches 1.. run function bm:p31/sav/paid'])
    day = ['scoreboard players remove #sd bm.pay 1']
    for cur, obj, nm, col in BANK:
        day += [f'execute unless score @s {obj} matches 0.. run scoreboard players set @s {obj} 0',
                f'scoreboard players operation #i bm.pay = @s {obj}', f'scoreboard players operation #i bm.pay /= #{SAVE_PER} bm.pay',
                f'execute if score #i bm.pay matches {SAVE_CAP.get(cur, SAVE_CAP_ELSE) + 1}.. run scoreboard players set #i bm.pay {SAVE_CAP.get(cur, SAVE_CAP_ELSE)}',
                f'scoreboard players operation @s {obj} += #i bm.pay', f'scoreboard players operation #g_{cur} bm.pay += #i bm.pay',
                'scoreboard players operation @s bm.bkint += #i bm.pay']
    day += ['execute if score #sd bm.pay matches 1.. run function bm:p31/sav/day']
    fn('p31/sav/day', day)
    G.FUNCS['load'][-1:-1] = [f'scoreboard players set #{SAVE_PER} bm.pay {SAVE_PER}']
    fn('p31/sav/paid', ['playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 0.6 1.4',
                        tellraw('@s', PREFIX + [T('Your savings earned interest - added to your Rat Bank account:', 'gray')])] +
       [f'execute if score #g_{cur} bm.pay matches 1.. run ' + tellraw('@s', [T('   +', col), {'score': {'name': f'#g_{cur}', 'objective': 'bm.pay'}, 'color': col}, T(f' {nm}', col)])
        for cur, obj, nm, col in BANK])
    fn('admin/bank_interest_off', ['scoreboard players set #interest bm.pay 0', tellraw('@s', PREFIX + [T('Rat Bank interest off.', 'gray')])])

    # ------------------------------------------------------------------ the Concierge: weekly stock + repairs
    lots = G.P30_LOTS
    pool = [i for i, l in enumerate(lots) if l[3] == 'reg' and l[0] != 'boss_key']
    second.append('scoreboard players operation #wkn bm.pay = #day bm.bm')
    second.append('scoreboard players operation #wkn bm.pay /= #7 bm.auc')
    second.append('execute unless score #cweek bm.pay = #wkn bm.pay run function bm:p31/conc/restock')
    rs = ['scoreboard players operation #cweek bm.pay = #wkn bm.pay']
    for s_ in (1, 2, 3):
        rs += [f'execute store result score #cs{s_} bm.pay run random value 0..{len(pool) - 1}']
    rs += ['execute if score #cs2 bm.pay = #cs1 bm.pay run function bm:p31/conc/bump2', 'execute if score #cs3 bm.pay = #cs1 bm.pay run function bm:p31/conc/bump3',
           'execute if score #cs3 bm.pay = #cs2 bm.pay run function bm:p31/conc/bump3', 'execute if score #cs3 bm.pay = #cs1 bm.pay run function bm:p31/conc/bump3']
    fn('p31/conc/restock', rs)
    for s_ in (2, 3):
        fn(f'p31/conc/bump{s_}', [f'scoreboard players add #cs{s_} bm.pay 1', f'execute if score #cs{s_} bm.pay matches {len(pool)}.. run scoreboard players set #cs{s_} bm.pay 0'])
    op2 = [f'scoreboard players set @s bm.menu {P28.MENU["concierge"]}', 'data remove storage bm:ui cc']
    for s_ in (1, 2, 3):
        for k, i in enumerate(pool):
            l = lots[i]
            op2.append(f'execute if score #cs{s_} bm.pay matches {k} run data modify storage bm:ui cc merge value {snbt({f"n{s_}": l[1], f"p{s_}": l[4]})}')
    op2.append('function bm:p31/conc/dlg with storage bm:ui cc')
    fn('p31/conc/open', op2)
    dlg = P28.multi([T('The Concierge', 'gold', bold=True)],
                    [P28.body([T('"This week\'s little luxuries, for our Partners. And if anything of yours is looking tired..."', 'gray', italic=True)], 300)],
                    [P28.btn([T('$(n1)', 'white'), T('  $(p1) Medallions', 'light_purple')], 5001, width=260),
                     P28.btn([T('$(n2)', 'white'), T('  $(p2) Medallions', 'light_purple')], 5002, width=260),
                     P28.btn([T('$(n3)', 'white'), T('  $(p3) Medallions', 'light_purple')], 5003, width=260),
                     P28.btn([T('Repair the item in my main hand  ', 'white'), T('1 Medallion', 'light_purple')], 5010, width=260,
                             tooltip=T('A full repair. Unbreakable things need no help.', 'gray'))], columns=1)
    fn('p31/conc/dlg', [f'$dialog show @s {P28.inline(dlg)}'])
    G.FUNCS['p28/act'].append('execute if score #act bm.pay matches 5000..5099 run return run function bm:p31/conc/act')
    ca = [f'execute unless score @s bm.menu matches {P28.MENU["concierge"]} run return run function bm:p28/stale',
          'execute unless entity @e[type=minecraft:interaction,tag=bm.ledger,distance=..8,scores={bm.lgid=41}] run return run function bm:p28/stale',
          'execute if score #act bm.pay matches 5010 run return run function bm:p31/conc/repair']
    for s_ in (1, 2, 3):
        ca.append(f'execute if score #act bm.pay matches {5000 + s_} run return run function bm:p31/conc/buy{s_}')
        b = []
        for k, i in enumerate(pool):
            b.append(f'execute if score #cs{s_} bm.pay matches {k} run return run function bm:p31/conc/sell_{i}')
        fn(f'p31/conc/buy{s_}', b)
    for i in pool:
        l = lots[i]
        fn(f'p31/conc/sell_{i}', P28.pay_lines('medallion', l[4], 'function bm:p28/back/broke {m:"%s"}' % f'That is {l[4]} Medallions, dear.') +
           [f'function bm:p30/lot/give_{i}', 'playsound minecraft:entity.villager.yes neutral @s ~ ~ ~ 0.8 1.3',
            title('@s', 'actionbar', T(f'The Concierge wraps your {l[1]} in tissue paper.', 'gold'))])
    fn('p31/conc/act', ca)
    fn('p31/conc/repair', ['execute unless items entity @s weapon.mainhand *[minecraft:max_damage] run return run ' + title('@s', 'actionbar', T('Hold something that can wear out.', 'gray')),
                           'execute if items entity @s weapon.mainhand *[minecraft:unbreakable] run return run ' + title('@s', 'actionbar', T('That will outlive us all. No repair needed.', 'gray')),
                           'execute if items entity @s weapon.mainhand *[minecraft:damage=0] run return run ' + title('@s', 'actionbar', T('Already pristine, darling.', 'gray'))] +
       P28.pay_lines('medallion', 1, 'function bm:p28/back/broke {m:"Repairs are a Medallion."}') +
       ['item modify entity @s weapon.mainhand bm:p31/repair', 'playsound minecraft:block.anvil.use player @s ~ ~ ~ 0.8 1.2',
        title('@s', 'actionbar', T('Good as new. Better, even.', 'gold'))])
    wjson('bm/item_modifier/p31/repair.json', {'function': 'minecraft:set_damage', 'damage': 1.0})

    G.FUNCS['load'][-1:-1] = load
    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second

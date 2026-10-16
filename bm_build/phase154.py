"""2.80a: THE GUTTER BANK, A PAGE PER CURRENCY - one coin or spoil at a time, in and out.

Until now the Gutter Bank was all or nothing: "Deposit everything" took every coin and spoil you carried, and taking a
spoil out handed back every one you had of it (all your Copper Cogs, say). Now it works like the Rat Bank:

THE ACCOUNT    one button per currency with its balance - loose Gutter Coins, Gutter Medallions, Gutter Trophies, and the
               six spoils (Copper Cogs, Silver Seals, Gilded Leaves, Deep Pearls, Hoard Embers, Captain's Insignia) - then
               Deposit everything, the ⇄ exchange (coins, Medallions and Trophies into each other), Buy Tokens, the Office.
A CURRENCY     its icon, how many are in your account and how many you carry; Deposit 1 / 10 / all and Take 1 / 10 / all.
               Each brings you back to the same page. (Taking coins takes loose coins; a Medallion or Trophy is never melted
               down for them - change one on the ⇄ page first.)

How the codes work: a currency's page sets bm.menu to that page's own code, so the six action buttons (shared by every
page) know which currency they act on, and a button from an old page can't act on a different currency."""
from items import T, ITEMS
from nbt import snbt, B, Int
import phase28 as P28
import phase80 as P80

MC = P80.MENU_CODE
GOLD, GUT_M, TRO = P80.GOLD, P80.GUT_M, '#ffd870'
PAGE0 = MC + 170                                  # 7970..7978: a currency's page (also its bm.menu while it's open)
ACT0 = MC + 180                                   # 7980..7985: deposit 1 / 10 / all, take 1 / 10 / all
EXCH = MC + 70                                    # (phase120/123: the ⇄ Medallions & Trophies page)
# (key, plural, item, colour, its worth in coins - 0: a spoil, kept on its own score)
CUR = [('c', 'Gutter Coins', 'gutter_coin', GOLD, 1), ('m', 'Gutter Medallions', 'gutter_medallion', GUT_M, 16),
       ('t', 'Gutter Trophies', 'gutter_trophy', TRO, 128)] + \
      [(f's{i}', m[2], m[0], m[3], 0) for i, m in enumerate(P80.MATS, 1)]
ACTS = [('dep', 1), ('dep', 10), ('dep', 0), ('take', 1), ('take', 10), ('take', 0)]       # (0: all)


def generate(G):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    has = lambda iid: f'*[minecraft:custom_data~{{bm:"{iid}"}}]'
    bar = lambda parts: title('@s', 'actionbar', parts)
    assert PAGE0 + len(CUR) <= ACT0 and ACT0 + len(ACTS) <= MC + 199, 'the Gutter Bank has outgrown its codes'

    # ------------------------------------------------------------------ the account page
    # (p80/bank fills bm:ui bk2: c = loose coins, gm / gt = Medallions / Trophies, m1.. = the spoils, all = the worth)
    val = {'c': 'c', 'm': 'gm', 't': 'gt', **{f's{i}': f'm{i}' for i in range(1, P80.NM + 1)}}
    btns = [P28.btn([T(nm, col), T(f'   $({val[k]})', 'white')], PAGE0 + j, width=150, tooltip=T(f'Deposit or take out your {nm}', 'gray'))
            for j, (k, nm, iid, col, w) in enumerate(CUR)]
    btns += [P28.btn([T('⬇ ', P80.LUCKY), T('Deposit everything', 'white', bold=True)], MC + 40, width=150,
                     tooltip=T('Every coin, Medallion, Trophy and spoil you carry, into your account.', 'gray')),
             P28.btn([T('⇄ ', TRO), T('Change coins', 'white')], EXCH, width=150,
                     tooltip=T('Coins, Medallions and Trophies into each other, either way. Nothing lost.', 'gray')),
             P28.btn([T('✦ ', GOLD), T('Buy Tokens', 'white')], MC + 48, width=150, tooltip=T(f'{P80.TOKEN_COINS} coins a Black Market Token.', 'gray')),
             P28.btn(T('« The Office', 'gray'), MC, width=150)]
    acct = P28.multi([T('THE GUTTER BANK', GOLD, bold=True), T('  ·  your coins and spoils', 'gray')],
                     [P28.body([T('Pick one to put in or take out - one, ten, or all of it. ', 'gray'),
                                T('All told: ', 'gray'), T('$(all)', GOLD, bold=True), T(' coins', 'gray'), T(' (a Medallion is 16, a Trophy 128).', 'dark_gray')], 300),
                      P28.body([T('The Armory and the shops pay from here first, then from your pockets.', 'dark_gray')], 300)],
                     btns, columns=2)
    G.FUNCS['p80/bank_dlg'] = [f'$dialog show @s {P28.inline(acct)}']

    # ------------------------------------------------------------------ a currency's page
    for j, (k, nm, iid, col, w) in enumerate(CUR):
        it = ITEMS[iid]
        icon = {'id': it['base'], 'count': Int(1), 'components': {'minecraft:item_name': T(nm, col)}}
        if it['comps'].get('minecraft:item_model'):
            icon['components']['minecraft:item_model'] = it['comps']['minecraft:item_model']
        note = {'c': 'Taking coins takes loose ones - a Medallion or Trophy is never broken for them (change one on the ⇄ page).',
                'm': 'A Medallion is worth 16 coins - it stays a Medallion in your account until you change it.',
                't': 'A Trophy is worth 128 coins - it stays a Trophy in your account until you change it.'}.get(k, 'A spoil off the vault\'s guards: the Armory takes them for its ranks.')
        pg = P28.multi([T(nm.upper(), col, bold=True), T('  ·  The Gutter Bank', 'gray')],
                       [{'type': 'minecraft:item', 'item': icon, 'show_decorations': B(0), 'show_tooltip': B(1), 'width': Int(22), 'height': Int(22),
                         'description': {'contents': [T('In your account: ', 'gray'), T('$(n)', col, bold=True), T('\nOn you: ', 'gray'), T('$(h)', 'white')],
                                         'width': Int(220)}},
                        P28.body([T(note, 'dark_gray')], 300)],
                       [P28.btn([T('⬇ ', P80.LUCKY), T('Deposit 1', 'white')], ACT0, width=100),
                        P28.btn([T('⬇ ', P80.LUCKY), T('Deposit 10', 'white')], ACT0 + 1, width=100),
                        P28.btn([T('⬇ ', P80.LUCKY), T('Deposit all', 'white'), T('  ($(h))', 'gray')], ACT0 + 2, width=100),
                        P28.btn([T('⬆ ', col), T('Take 1', 'white')], ACT0 + 3, width=100),
                        P28.btn([T('⬆ ', col), T('Take 10', 'white')], ACT0 + 4, width=100),
                        P28.btn([T('⬆ ', col), T('Take all', 'white'), T('  ($(n))', 'gray')], ACT0 + 5, width=100)] +
                       ([P28.btn([T('⇄ ', TRO), T('Change coins', 'white')], EXCH, width=150)] if k in ('c', 'm', 't') else []) +
                       [P28.btn(T('« Your account', 'gray'), MC + 2, width=150)],
                       columns=3)
        fn(f'p154/dlg_{k}', [f'$dialog show @s {P28.inline(pg)}'])
        avail = {'c': ['function bm:p120/bk_loose', 'scoreboard players operation #bka bm.rng = #bkl bm.rng'],
                 'm': ['scoreboard players operation #bka bm.rng = @s bm.gbm'], 't': ['scoreboard players operation #bka bm.rng = @s bm.gbt']}.get(
                     k, [f'scoreboard players operation #bka bm.rng = @s bm.gb{k[1:]}'])
        fn(f'p154/avail_{k}', ['function bm:p80/init_me'] + avail)
        fn(f'p154/page_{k}', [f'scoreboard players set @s bm.menu {PAGE0 + j}', f'function bm:p154/avail_{k}', 'data remove storage bm:ui bkp',
                              'execute store result storage bm:ui bkp.n int 1 run scoreboard players get #bka bm.rng',
                              f'execute store result storage bm:ui bkp.h int 1 run clear @s {has(iid)} 0', f'function bm:p154/dlg_{k} with storage bm:ui bkp'])
        # deposit #bkn (0: all) of it: what you carry, into the account
        add = {'c': ['scoreboard players operation @s bm.gbc += #bkm bm.rng'],
               'm': ['scoreboard players operation @s bm.gbm += #bkm bm.rng', 'scoreboard players operation #bkw bm.rng = #bkm bm.rng',
                     'scoreboard players set #bkk bm.rng 16', 'scoreboard players operation #bkw bm.rng *= #bkk bm.rng', 'scoreboard players operation @s bm.gbc += #bkw bm.rng'],
               't': ['scoreboard players operation @s bm.gbt += #bkm bm.rng', 'scoreboard players operation #bkw bm.rng = #bkm bm.rng',
                     'scoreboard players set #bkk bm.rng 128', 'scoreboard players operation #bkw bm.rng *= #bkk bm.rng', 'scoreboard players operation @s bm.gbc += #bkw bm.rng']}.get(
                         k, [f'scoreboard players operation @s bm.gb{k[1:]} += #bkm bm.rng'])
        fn(f'p154/dep_{k}', ['function bm:p80/init_me', f'execute store result score #bkm bm.rng run clear @s {has(iid)} 0',
                             'execute if score #bkn bm.rng matches 1.. run scoreboard players operation #bkm bm.rng < #bkn bm.rng',
                             f'execute if score #bkm bm.rng matches ..0 run return run function bm:p154/none_{k}',
                             'execute store result storage bm:tmp bkd.m int 1 run scoreboard players get #bkm bm.rng', f'function bm:p154/clr_{k} with storage bm:tmp bkd'] + add +
           ['playsound minecraft:block.chain.place player @s ~ ~ ~ 0.8 1.4',
            bar([T('Deposited ', 'gray'), {'score': {'name': '#bkm', 'objective': 'bm.rng'}, 'color': col, 'bold': True}, T(f' {nm}.', 'gray')]),
            f'function bm:p154/page_{k}'])
        fn(f'p154/clr_{k}', [f'$clear @s {has(iid)} $(m)'])
        fn(f'p154/none_{k}', [bar(T(f'You have no {nm} on you.', 'gray')), f'function bm:p154/page_{k}'])
        # take #bkn (0: all) of it out of the account
        sub = {'c': ['scoreboard players operation @s bm.gbc -= #bkm bm.rng'],
               'm': ['scoreboard players operation @s bm.gbm -= #bkm bm.rng', 'scoreboard players operation #bkw bm.rng = #bkm bm.rng',
                     'scoreboard players set #bkk bm.rng 16', 'scoreboard players operation #bkw bm.rng *= #bkk bm.rng', 'scoreboard players operation @s bm.gbc -= #bkw bm.rng'],
               't': ['scoreboard players operation @s bm.gbt -= #bkm bm.rng', 'scoreboard players operation #bkw bm.rng = #bkm bm.rng',
                     'scoreboard players set #bkk bm.rng 128', 'scoreboard players operation #bkw bm.rng *= #bkk bm.rng', 'scoreboard players operation @s bm.gbc -= #bkw bm.rng']}.get(
                         k, [f'scoreboard players operation @s bm.gb{k[1:]} -= #bkm bm.rng'])
        fn(f'p154/take_{k}', [f'function bm:p154/avail_{k}', 'scoreboard players operation #bkm bm.rng = #bka bm.rng',
                              'execute if score #bkn bm.rng matches 1.. run scoreboard players operation #bkm bm.rng < #bkn bm.rng',
                              f'execute if score #bkm bm.rng matches ..0 run return run function bm:p154/empty_{k}'] + sub +
           ['scoreboard players operation #c bm.rng = #bkm bm.rng', f'function bm:p80/hand {{iid:"{iid}"}}', 'playsound minecraft:block.chain.break player @s ~ ~ ~ 0.8 1.4',
            bar([T('Took out ', 'gray'), {'score': {'name': '#bkm', 'objective': 'bm.rng'}, 'color': col, 'bold': True}, T(f' {nm}.', 'gray')]),
            f'function bm:p154/page_{k}'])
        fn(f'p154/empty_{k}', [bar(T(f'No {nm} in your account' + (' (loose - Medallions and Trophies stay whole).' if k == 'c' else '.'), 'gray')),
                               f'function bm:p154/page_{k}'])
    # ------------------------------------------------------------------ the routing
    # (a page's code opens it; the six actions act on the page that's open - bm.menu says which)
    r = [f'execute if score #act bm.pay matches {PAGE0 + j} run return run function bm:p154/page_{k}' for j, (k, *_x) in enumerate(CUR)]
    for a, (verb, n) in enumerate(ACTS):
        r.append(f'execute if score #act bm.pay matches {ACT0 + a} run return run function bm:p154/{verb} {{n:{n}}}')
    fn('p154/act', r)
    for verb in ('dep', 'take'):
        fn(f'p154/{verb}', ['$scoreboard players set #bkn bm.rng $(n)'] +
           [f'execute if score @s bm.menu matches {PAGE0 + j} run return run function bm:p154/{verb}_{k}' for j, (k, *_x) in enumerate(CUR)] +
           ['function bm:p28/stale'])
    G.FUNCS['p80/act'].insert(2, f'execute if score #act bm.pay matches {PAGE0}..{ACT0 + len(ACTS) - 1} run return run function bm:p154/act')

    # ------------------------------------------------------------------ the old all-or-nothing pages go
    # (Take out coins: 16 / 64 / all; Take out spoils: every one of a kind; the ⇄ page's Take 1 / all Medallions and Trophies)
    for f_ in ['p80/bank_coins', 'p80/bank_cdlg', 'p80/bank_spoils', 'p80/bank_sdlg', 'p80/bank_take16', 'p80/bank_take64', 'p80/bank_takeall',
               'p80/bank_mat', 'p80/bank_mat2', 'p80/bank_takegm', 'p80/bank_takegt'] + [f'p80/bank_mat_{i}' for i in range(1, P80.NM + 1)] + \
              [f'p120/bk_{x}' for x in ('m1', 'ma', 't1', 'ta')]:
        G.FUNCS.pop(f_, None)
    gone = {MC + 41, MC + 42, MC + 43, MC + 46, MC + 47, MC + 57, MC + 58} | {MC + 50 + i for i in range(1, P80.NM + 1)}
    G.FUNCS['p80/act'] = [l for l in G.FUNCS['p80/act'] if not any(f'matches {c} run' in l for c in gone)]
    G.FUNCS['p120/bk_act'] = [l for l in G.FUNCS['p120/bk_act'] if not any(f'matches {EXCH + i} run' in l for i in range(1, 5))]
    ex = G.FUNCS['p120/bk_dlg'][0]
    for i, lab in ((1, 'Take 1 Medallion'), (2, 'Take all Medallions'), (3, 'Take 1 Trophy'), (4, 'Take all Trophies')):
        col = GUT_M if i <= 2 else TRO
        s_ = snbt(P28.btn([T(lab, col)], EXCH + i, width=150)) + ','
        assert s_ in ex, lab
        ex = ex.replace(s_, '')
    G.FUNCS['p120/bk_dlg'] = [ex.replace('Take them out to spend, or change them here', 'Change them here')]

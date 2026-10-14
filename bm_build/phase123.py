"""2.75: CHANGE IT BACK - the bank's exchange, chatter from any follower's menu, and a heist's modifiers said out loud.

THE GUTTER BANK  one page for Medallions & Trophies (the bank's ⇄ button): take them out, or change them - 16 coins to a
                 Medallion and a Medallion back to 16 coins, 128 coins to a Trophy and back, 8 Medallions to a Trophy and
                 back. Any time, both ways, nothing lost; a Medallion or Trophy in your pockets changes too (bought one by
                 mistake? Change it back). The coin-to-Medallion buttons have left "Take out coins" - that page is coins only.
FOLLOWER CHATTER the on/off switch is in every follower's own menu now too (sneak + use their item), not just the Ledger: one
                 switch for all of them, everywhere - their quips, and the banter when two or three are together.
MODIFIERS        BEGIN reads out the heist's modifiers in the chat (Glass Cannon, Lights Out, Speed Run...) - or that there
                 are none. (They were only on the sheet in the den.)
"""
from items import T
from nbt import snbt
import phase28 as P28
import phase70 as P70
import phase80 as P80
import phase99 as P99

GOLD = '#ffcf40'
CHAT = 7735
MC = P80.MENU_CODE
PAGE = MC + 70                                    # (phase120's Medallions & Trophies page; 71-74 its take-outs)
EX = {'c2m': MC + 75, 'c2t': MC + 76, 'm2c': MC + 77, 't2c': MC + 78, 'm2t': MC + 79, 't2m': MC + 83}


def generate(G):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    P = [T('[', 'dark_gray'), T('Gutter Bank', GOLD, bold=True), T('] ', 'dark_gray')]
    say = lambda txt, col='gray': tellraw('@s', P + [T(txt, col)])
    hold = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    GUT_M, TRO, GOLD_ = P80.GUT_M, '#ffd870', P80.GOLD

    # ================================================================== THE GUTTER BANK: the exchange, both ways
    btitle = [T('THE GUTTER BANK', GOLD_, bold=True), T('  ·  Medallions & Trophies', 'gray')]
    acct = [T('YOUR ACCOUNT\n', 'white', bold=True), T('◆ ', GOLD_), T('Gutter Coins (loose)   ', 'white'), T('$(c)', GOLD_, bold=True),
            T('\n◆ ', GUT_M), T('Gutter Medallions   ', 'white'), T('$(gm)', GUT_M, bold=True), T('   (on you: $(gmi))', 'dark_gray'),
            T('\n◆ ', TRO), T('Gutter Trophies   ', 'white'), T('$(gt)', TRO, bold=True), T('   (on you: $(gti))', 'dark_gray')]
    b = lambda lab, code, col='white', tip=None: P28.btn(lab, code, width=150, tooltip=T(tip, 'gray') if tip else None)
    dlg = P28.multi(btitle,
                    [P28.body(acct, 280),
                     P28.body([T('Take them out to spend, or change them here - either way, any time, nothing lost. ', 'gray'),
                               T('A Medallion is 16 coins; a Trophy is 128, or 8 Medallions. Changing back uses the account first, then your pockets.', 'dark_gray')], 300)],
                    [b([T('Take 1 Medallion', GUT_M)], PAGE + 1), b([T('Take all Medallions', GUT_M)], PAGE + 2),
                     b([T('Take 1 Trophy', TRO)], PAGE + 3), b([T('Take all Trophies', TRO)], PAGE + 4),
                     b([T('16 coins ', GOLD_), T('→ ', 'gray'), T('Medallion', GUT_M)], EX['c2m'], tip='From your loose coins; the Medallion stays in your account.'),
                     b([T('Medallion ', GUT_M), T('→ ', 'gray'), T('16 coins', GOLD_)], EX['m2c'], tip='Changes one back - from your account, or one you carry.'),
                     b([T('128 coins ', GOLD_), T('→ ', 'gray'), T('Trophy', TRO)], EX['c2t'], tip='From your loose coins; the Trophy stays in your account.'),
                     b([T('Trophy ', TRO), T('→ ', 'gray'), T('128 coins', GOLD_)], EX['t2c'], tip='Changes one back - from your account, or one you carry.'),
                     b([T('8 Medallions ', GUT_M), T('→ ', 'gray'), T('Trophy', TRO)], EX['m2t'], tip='Eight of your account\'s Medallions into one Trophy.'),
                     b([T('Trophy ', TRO), T('→ ', 'gray'), T('8 Medallions', GUT_M)], EX['t2m'], tip='One Trophy into eight Medallions - from your account, or one you carry.'),
                     P28.btn(T('« Back', 'gray'), MC + 2, width=150)],
                    columns=2)
    G.FUNCS['p120/bk_dlg'] = [f'$dialog show @s {P28.inline(dlg)}']
    # (only its own codes: 80 and 81 are the Lounge and Skip this puzzle - 2.76 fix, a 75..83 range swallowed them)
    G.FUNCS['p80/act'][2:2] = [f'execute if score #act bm.pay matches {code} run return run function bm:p123/ex_act' for code in sorted(EX.values())]
    fn('p123/ex_act', [f'execute if score #act bm.pay matches {code} run return run function bm:p123/ex_{k}' for k, code in EX.items()])
    ding = 'playsound minecraft:block.chain.place player @s ~ ~ ~ 0.8 1.3'
    back = 'function bm:p120/bk_page'
    fn('p123/ex_c2m', ['function bm:p120/bk_loose', 'execute unless score #bkl bm.rng matches 16.. run return run ' + say('That takes 16 loose coins in your account.', 'red'),
                       'scoreboard players add @s bm.gbm 1', ding, back])
    fn('p123/ex_c2t', ['function bm:p120/bk_loose', 'execute unless score #bkl bm.rng matches 128.. run return run ' + say('That takes 128 loose coins in your account.', 'red'),
                       'scoreboard players add @s bm.gbt 1', ding, back])
    fn('p123/ex_m2c', ['function bm:p80/init_me', 'execute if score @s bm.gbm matches 1.. run return run function bm:p123/ex_m2c_bank',
                       f'execute unless items entity @s container.* {hold("gutter_medallion")} unless items entity @s weapon.offhand {hold("gutter_medallion")} run return run ' +
                       say('No Medallion in your account or your pockets.', 'red'),
                       f'clear @s {hold("gutter_medallion")} 1', 'scoreboard players add @s bm.gbc 16', ding, back])
    fn('p123/ex_m2c_bank', ['scoreboard players remove @s bm.gbm 1', ding, back])                      # (its 16 coins are loose in the account now)
    fn('p123/ex_t2c', ['function bm:p80/init_me', 'execute if score @s bm.gbt matches 1.. run return run function bm:p123/ex_t2c_bank',
                       f'execute unless items entity @s container.* {hold("gutter_trophy")} unless items entity @s weapon.offhand {hold("gutter_trophy")} run return run ' +
                       say('No Trophy in your account or your pockets.', 'red'),
                       f'clear @s {hold("gutter_trophy")} 1', 'scoreboard players add @s bm.gbc 128', ding, back])
    fn('p123/ex_t2c_bank', ['scoreboard players remove @s bm.gbt 1', ding, back])
    fn('p123/ex_m2t', ['function bm:p80/init_me', 'execute unless score @s bm.gbm matches 8.. run return run ' + say('That takes 8 Medallions in your account.', 'red'),
                       'scoreboard players remove @s bm.gbm 8', 'scoreboard players add @s bm.gbt 1', ding, back])
    fn('p123/ex_t2m', ['function bm:p80/init_me', 'execute if score @s bm.gbt matches 1.. run return run function bm:p123/ex_t2m_bank',
                       f'execute unless items entity @s container.* {hold("gutter_trophy")} unless items entity @s weapon.offhand {hold("gutter_trophy")} run return run ' +
                       say('No Trophy in your account or your pockets.', 'red'),
                       f'clear @s {hold("gutter_trophy")} 1', 'scoreboard players add @s bm.gbc 128', 'scoreboard players add @s bm.gbm 8', ding, back])
    fn('p123/ex_t2m_bank', ['scoreboard players remove @s bm.gbt 1', 'scoreboard players add @s bm.gbm 8', ding, back])
    # ("Take out coins" is coins only now: its Medallion and Trophy buttons go - the exchange page has them, both ways)
    cd = G.FUNCS['p80/bank_cdlg']
    for btn in (P28.btn([T('A Gutter Medallion ', GUT_M), T('(16)', 'gray')], MC + 57, width=150), P28.btn([T('A Gutter Trophy ', TRO), T('(128)', 'gray')], MC + 58, width=150)):
        s_ = snbt(btn) + ','
        assert s_ in cd[0], 'take-out-coins button'
        cd[0] = cd[0].replace(s_, '')
    old_t = snbt(T('A Gutter Medallion is 16 coins in one piece (a Gutter Trophy, 128).', 'dark_gray'))
    assert old_t in cd[0]
    cd[0] = cd[0].replace(old_t, snbt(T('Medallions and Trophies: the ⇄ Medallions & Trophies page - take them out, or change coins into them and back.', 'dark_gray')))
    # (the account page's button says what it does)
    bd = G.FUNCS['p80/bank_dlg']
    ob = snbt(P28.btn([T('⬆ ', TRO), T('Medallions & Trophies', 'white')], PAGE, tooltip=T('Take out the Gutter Medallions and Trophies you keep here.'), width=150))
    nb = snbt(P28.btn([T('⇄ ', TRO), T('Medallions & Trophies', 'white')], PAGE,
                      tooltip=T('Take them out - or change coins, Medallions and Trophies into each other, either way. Nothing lost.'), width=150))
    assert ob in bd[0], 'the bank page button'
    bd[0] = bd[0].replace(ob, nb)

    # ================================================================== FOLLOWER CHATTER: from any follower's menu
    G.FUNCS['p28/act'].insert(0, f'execute if score #act bm.pay matches {CHAT} run return run function bm:p123/chat')
    fn('p123/chat', ['execute if entity @s[tag=bm.hush] run tag @s add bm.hush0', 'tag @s add bm.hush', 'execute if entity @s[tag=bm.hush0] run tag @s remove bm.hush',
                     'tag @s remove bm.hush0',
                     'execute if entity @s[tag=bm.hush] run ' + tellraw('@s', [T('Follower chatter off. ', '#d0d0d0', bold=True), T('Your followers keep their quips and banter to themselves.', 'gray')]),
                     'execute unless entity @s[tag=bm.hush] run ' + tellraw('@s', [T('Follower chatter on. ', '#d0d0d0', bold=True), T('Let them talk.', 'gray')]),
                     'playsound minecraft:ui.button.click player @s ~ ~ ~ 0.7 1.1'] +
       [f'execute if score @s bm.menu matches {P99.BASE[w]} run return run function bm:p99/menu/{w}' for w in P99.BASE])
    cbtn = snbt(P28.btn([T('Chatter: ', 'gray'), T('$(chat)', 'white', bold=True), T('  (all followers)', 'dark_gray')], CHAT, width=150,
                        tooltip=T('Hush what your followers say unprompted - quips, and banter when two or three are together. One switch for all of them.', 'gray')))
    for w, base in P99.BASE.items():
        d = G.FUNCS[f'p99/dlg/{w}']
        anchor = f'command:"/trigger bm.act set {base}"}}}}'
        assert anchor in d[0], w
        d[0] = d[0].replace(anchor, anchor + ',' + cbtn, 1)
        m = G.FUNCS[f'p99/menu/{w}']
        m.insert(len(m) - 2, 'data modify storage bm:ui wd.chat set value "on"')
        m.insert(len(m) - 2, 'execute if entity @s[tag=bm.hush] run data modify storage bm:ui wd.chat set value "off"')

    # ================================================================== MODIFIERS: said out loud at BEGIN
    lines = ['scoreboard players operation #gm bm.rng = @s bm.gvmod', 'function bm:p70/tag_mine',
             'execute if score #gm bm.rng matches 0 run ' + tellraw('@a[tag=bm.gvme]', [T('[', 'dark_gray'), T('Heist', GOLD, bold=True), T('] ', 'dark_gray'),
                                                                                         T('No modifiers tonight - a quiet job.', 'gray')]),
             'execute unless score #gm bm.rng matches 0 run ' + tellraw('@a[tag=bm.gvme]', [T('[', 'dark_gray'), T('Heist', GOLD, bold=True), T('] ', 'dark_gray'),
                                                                                             T('Tonight\'s modifiers (one share more each):', 'gray')])]
    for bit, nm, desc, col in P70.MODS:
        desc = desc.replace('darkness everywhere', 'darkness out on the heist (never in the den)')
        lines.append(f'execute if function bm:p70/mod{bit} run ' + tellraw('@a[tag=bm.gvme]', [T('  • ', 'dark_gray'), T(nm, col, bold=True), T(f' - {desc}', 'gray')]))
    lines.append('tag @a[tag=bm.gvme] remove bm.gvme')
    fn('p123/mods', lines)
    for name, L in G.FUNCS.items():                         # (Lights Out darkens the heist, not the den - 2.74)
        for i, l in enumerate(L):
            if 'darkness everywhere' in l: L[i] = l.replace('darkness everywhere', 'darkness out on the heist (never in the den)')
    bg = G.FUNCS['p70/begin']
    bg.append('execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run function bm:p123/mods')

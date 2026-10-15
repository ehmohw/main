"""2.74: OUTFITS AND EMMA'S BUFF FROM THE LEDGER - in the vault or anywhere else.

THE RAID CREW page (the Fixer's Ledger -> Raid Crew) has a new button, OUTFITS & EMMA'S BUFF: every follower's wardrobe
  (Emma, Celi, Zib, Cecil, KillerWatt, Leo, Democratus) - the same wardrobe as sneak + using their item, so it works in
  the vault, where their items wait at the coat check - and EMMA'S BUFF: Speed, Offense, Defense, Healing or Mining.
EMMA REMEMBERS: whichever buff you last picked for her (from the Ledger or her ribbon's menu) she comes back with, every
  time she's called - on a heist too. (Before, she always arrived on Healing.)
FOLLOWER CHATTER (same page): on or off. Off hushes what they say unprompted - quips after a kill, banter between two or
  three of them, battle cries, weather talk; what they say when you call, send home or change them still shows.
"""
from items import T
import phase28 as P28
import phase57 as P57
import phase80 as P80
import phase99 as P99
import re

CREW = '#9ad0ff'
PAGE = 7950                                   # the page; its wardrobes 7951-7957, Emma's buffs 7961-7965
WHO = [('emma', 'Emma'), ('celi', 'Celi'), ('zib', 'Zib'), ('cecil', 'Cecil'), ('kw', 'KillerWatt'), ('leo', 'Leo'), ('demo', 'Democratus'),
       ('apo', 'Apophiss'), ('tul', 'Tullius'), ('frog', 'The Frog'), ('don', 'Donado'), ('pearl', 'Pearlman'), ('wil', 'Wilfrey'), ('fishy', 'Fishy')]
COL = {'emma': '#ff7ad0', 'celi': '#9ad8ff', 'zib': '#3ad8c8', 'cecil': '#b48cff', 'kw': '#ffe040', 'leo': '#5ab8e0', 'demo': '#7ad06a',
       'apo': '#3ad06a', 'tul': '#7ad8ff', 'frog': '#6ac850', 'don': '#e8d29a', 'pearl': '#5ac8ff', 'wil': '#f4f4f4', 'fishy': '#ffa040'}
WD2 = 8280                                    # 2.78: the wardrobes past the seventh (8280-8286; 7958-7960 is too little room)
wcode = lambda i: PAGE + 1 + i if i < 7 else WD2 + i - 7


def generate(G):
    fn, tellraw = G.fn, G.tellraw
    MC = P80.MENU_CODE
    P = [T('[', 'dark_gray'), T('Ledger', P80.OFFICE, bold=True), T('] ', 'dark_gray')]
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.emode dummy']
    G.OBJECTIVES += ['bm.emode']
    sel_pet = 'execute as @e[type=minecraft:cat,tag=bm.emmapet] if score @s bm.pid = #me bm.pid'

    # ================================================================== Emma remembers her buff
    sm = G.FUNCS['p57/set_mode']
    sm[0:0] = ['scoreboard players operation @s bm.emode = #act bm.pay', 'scoreboard players remove @s bm.emode 7300']
    sh = G.FUNCS['p57/summon_here']
    k = sh.index('scoreboard players set @e[type=minecraft:cat,tag=bm.emnew,limit=1,sort=nearest] bm.emm 4')
    sh.insert(k + 1, 'execute if score @s bm.emode matches 1..5 run scoreboard players operation @e[type=minecraft:cat,tag=bm.emnew,limit=1,sort=nearest] bm.emm = @s bm.emode')
    k = sh.index('scoreboard players set #emo bm.rng 4')
    sh.insert(k + 1, 'execute if score @s bm.emode matches 1..5 run scoreboard players operation #emo bm.rng = @s bm.emode')

    # ================================================================== the page: wardrobes and Emma's buff
    from nbt import snbt
    crew = G.FUNCS['p98/crew']
    k = next(i for i, l in enumerate(crew) if l.startswith('data modify storage bm:ui crew.acts append value') and '« The Office' in l)
    crew.insert(k, 'data modify storage bm:ui crew.acts append value ' + snbt(P28.btn([T('Outfits & Emma\'s buff', '#ff8ad8', bold=True)], PAGE, width=180,
                                                                                   tooltip=T('Every follower\'s wardrobe, and what Emma focuses on - in the vault too.', 'gray'))))
    page = ['tag @s remove bm.wdled', f'scoreboard players set @s bm.menu {PAGE}', 'data remove storage bm:ui crx',
            'data modify storage bm:ui crx.mode set value "Healing"'] + \
        [f'execute if score @s bm.emode matches {m} run data modify storage bm:ui crx.mode set value "{nm}"' for m, (nm, _c) in P57.MODES.items()] + \
        ['data modify storage bm:ui crx.chat set value "on"', 'execute if entity @s[tag=bm.hush] run data modify storage bm:ui crx.chat set value "off"',
         'function bm:p119/page_dlg with storage bm:ui crx']
    fn('p119/page', page)
    TIPS = {1: 'Speed + Jump Boost', 2: 'Strength', 3: 'Resistance', 4: 'Regeneration + quick heals', 5: 'Haste: dig and chop faster'}
    dlg = P28.multi([T('OUTFITS & EMMA\'S BUFF', '#ff8ad8', bold=True), T('  ·  your followers, from the Ledger', 'gray')],
                    [P28.body([T('Each follower\'s wardrobe - the outfits you\'ve unlocked, to wear any time (Goldtooth sells the rest). ', 'gray'),
                               T('Works in the vault too, while their items wait at the coat check.', 'dark_gray')], 360),
                     P28.body([T('Emma focuses on: ', 'gray'), T('$(mode)', 'white', bold=True),
                               T('  - she remembers it every time she comes, on a heist too.', 'gray')], 360),
                     P28.body([T('Follower chatter: ', 'gray'), T('$(chat)', 'white', bold=True),
                               T('  - quips, banter and battle cries. (What they say when you call or change them always shows.)', 'dark_gray')], 360)],
                    [P28.btn([T(f'{nm}\'s wardrobe', COL[w], bold=True)], wcode(i), width=180) for i, (w, nm) in enumerate(WHO)] +
                    [P28.btn([T('Emma: ', '#ff8ad8'), T(nm, c, bold=True)], PAGE + 10 + m, width=180, tooltip=T(TIPS[m], 'gray')) for m, (nm, c) in P57.MODES.items()] +
                    [P28.btn([T('Chatter on / off', '#d0d0d0', bold=True)], PAGE + 18, width=180, tooltip=T('Hush what your followers say unprompted - or let them talk.', 'gray')),
                     P28.btn([T('« Raid Crew', 'gray')], MC + 7, width=180)], columns=2, exit_label='Close')
    fn('p119/page_dlg', [f'$dialog show @s {P28.inline(dlg)}'])
    G.FUNCS['p80/act'].insert(2, f'execute if score #act bm.pay matches {PAGE}..{PAGE + 19} run return run function bm:p119/act')
    fn('p119/act', [f'execute if score #act bm.pay matches {PAGE} run return run function bm:p119/page'] +
       [f'execute if score #act bm.pay matches {wcode(i)} run return run function bm:p119/wd/{w}' for i, (w, _n) in enumerate(WHO)] +
       [f'execute if score #act bm.pay matches {PAGE + 10 + m} run return run function bm:p119/buff{m}' for m in P57.MODES] +
       [f'execute if score #act bm.pay matches {PAGE + 18} run return run function bm:p119/hush'])
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {WD2}..{wcode(len(WHO) - 1)} if score @s bm.menu matches {PAGE} run return run function bm:p119/act')
    fn('p119/hush', ['execute if entity @s[tag=bm.hush] run return run function bm:p119/unhush', 'tag @s add bm.hush',
                     tellraw('@s', P + [T('Follower chatter off. ', '#d0d0d0', bold=True), T('They\'ll keep their quips to themselves.', 'gray')]), 'function bm:p119/page'])
    fn('p119/unhush', ['tag @s remove bm.hush', tellraw('@s', P + [T('Follower chatter on. ', '#d0d0d0', bold=True), T('Let them talk.', 'gray')]), 'function bm:p119/page'])
    # (what they say unprompted: every line of these goes to whoever hasn't hushed them)
    HUSH = re.compile(r'^(p100/say_|p57/harmony|p66/quip$|p96/quip$|p97/quip$|p96/banter_|p97/banter_|p96/guard$|p97/wx_say$|p97/reap_go$|p79/pet/ult_name$|'
                      r'p96/duo_\w+_first$|p97/duo_\w+_first$)')
    def hush(l):
        def sub(m):
            sel, br = m.group(2), m.group(3)
            return f'{m.group(1)} {sel}[{br[1:-1] + "," if br else ""}tag=!bm.hush]'
        return re.sub(r'\b(title|tellraw) (@[sapre])(\[[^\]]*\])?', sub, l)
    nh = 0
    for name in [n for n in G.FUNCS if HUSH.match(n)]:
        G.FUNCS[name] = [hush(l) for l in G.FUNCS[name]]; nh += 1
    assert nh >= 20, nh
    for m, (nm, c) in P57.MODES.items():
        fn(f'p119/buff{m}', [f'scoreboard players set @s bm.emode {m}', 'scoreboard players operation #me bm.pid = @s bm.pid', f'{sel_pet} run tag @s add bm.emsel2',
                             'execute unless entity @e[type=minecraft:cat,tag=bm.emsel2] run ' + tellraw('@s', P + [T('Emma will focus on ', 'gray'), T(nm, c, bold=True),
                                                                                                                     T(' when she next comes.', 'gray')]),
                             f'execute if entity @e[type=minecraft:cat,tag=bm.emsel2] run scoreboard players set #act bm.pay {7300 + m}',
                             'execute if entity @e[type=minecraft:cat,tag=bm.emsel2] run function bm:p57/set_mode',
                             'tag @e[tag=bm.emsel2] remove bm.emsel2', 'function bm:p119/page'])

    # ================================================================== a wardrobe opened from the Ledger: its first button goes back to the page
    for w, nm in WHO:
        b = P99.BASE[w]
        fn(f'p119/wd/{w}', ['tag @s add bm.wdled', f'function bm:p99/menu/{w}'])
        d = G.FUNCS[f'p99/dlg/{w}'][0]
        home = next(t for t in ('Send her home', 'Send him home') if t in d)
        fn(f'p119/dlg/{w}', [d.replace(home, '« Outfits & buffs')])
        menu = G.FUNCS[f'p99/menu/{w}']
        assert menu[-1] == f'function bm:p99/dlg/{w} with storage bm:ui wd', menu[-1]
        menu.insert(len(menu) - 1, f'execute if entity @s[tag=bm.wdled] run return run function bm:p119/dlg/{w} with storage bm:ui wd')
        G.FUNCS[f'p99/act/{w}'].insert(2, f'execute if score #act bm.pay matches {b} if entity @s[tag=bm.wdled] run return run function bm:p119/page')
        fn(f'p119/plain/{w}', ['tag @s remove bm.wdled', f'function bm:p99/menu/{w}'])
    # (every other way into a wardrobe - sneak + use, Emma's buff menu - is the ordinary one, with 'Send home')
    for name, L in G.FUNCS.items():
        if name.startswith('p99/') or name.startswith('p119/'):
            continue
        for i, l in enumerate(L):
            if 'function bm:p99/menu/' in l:
                L[i] = l.replace('function bm:p99/menu/', 'function bm:p119/plain/')

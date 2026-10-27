"""2.74: SKIP A PUZZLE, A BIGGER SOLO CREW, AND TIDYING UP.

SKIP A PUZZLE   stuck? Every puzzle room (the calm ones, the jumping ones, the Mason's Plan and the Dig) offers a way past:
                SKIP THIS PUZZLE in the chat as you walk in, or in the Fixer's Ledger on a heist. It asks first, then opens
                the way on as if you'd solved it - at the cost of one try for the crew. No coins for the pot, no flawless
                trophy, and never on your last try.
A SOLO CREW     raiding alone, three followers come along (was two) - so a trio's bonus works in the vault too. In a party:
                one each, as before.
ENDLESS & PIT   no ALARM switch on the tries page for the Endless Vault or the Pit - there's no alarm in either; it stays off.
THE BOSS BAR    a raid boss's bar shows only to the crew within 30 blocks of it - from the vault's doorway, not from the den.
                (The guardian waits in the vault from the start; its bar used to show the whole way there.)
A MISTAKE'S GUARD whatever a failed puzzle brought down on you - a guard, or a trap's silverfish, vexes or slimes - goes when
                the room is solved: any still in it vanish in a puff, dropping nothing.
LOOSE CARPETS   carpets and moss carpets knocked loose when a room is laid out (they pop off as items) are swept up -
                every room near the crew, every second.
BLOCK PARTY     its "back to the middle" teleports aimed at the room's corner, not its centre: players landed in the wall,
                or under the floor once it ended, and were pushed out into the void. They land in the middle now; and
                whoever drops through steps back to the starting edge for the next round.
THE MINECART RUN the shooting gallery (Version A) is gone: the cart's speed and the arrows' drift made six targets near
                impossible. The junction run and the bridges stay.
"""
from items import T
from nbt import snbt
import phase28 as P28
import phase70 as P70
import phase116 as P116

GOLD = '#ffcf40'
PUZZLES = sorted(set(P116.CALM) | set(P116.JUMPY) | set(P116.HOP) | {'memory'})       # (2.82g: Memory Match is a puzzle too)
# (2.95a: every room that isn't a fight can be skipped too - the games, the parkour, the events. Never a fight (its foes are the
#  way on), nor the den, the cache, the vault, the Pit, the Fork's wall, a room that's open as you walk in (the Rest, the
#  Sanctuary) or the Throne's coffer. TIDY: what a room's own finish clears away that the solve doesn't.)
GAMES = ['brawl', 'dash', 'gallery', 'girder', 'grass', 'grove', 'hollow', 'hunted', 'minecart', 'party', 'plaza', 'rave', 'redlight',
         'says', 'scramble', 'storm', 'temple', 'ufo', 'voidg', 'whack']
SKIPPABLE = sorted(set(PUZZLES) | set(GAMES))
ASK, YES, LEDGER = 7733, 7734, 7881
SL = P70.SLOTS


def generate(G):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    second = G.FUNCS['loop/second']
    P = [T('[', 'dark_gray'), T('Heist', GOLD, bold=True), T('] ', 'dark_gray')]
    say = lambda txt, col='gray': tellraw('@s', P + [T(txt, col)])

    # ================================================================== SKIP A PUZZLE
    fn('p122/is_puzzle', [f'execute if entity @s[tag=bm.gvr_{k}] run return 1' for k in SKIPPABLE] + ['return 0'])
    keep = lambda f, *drop: [l for l in G.FUNCS[f] if not any(d in l for d in ('title ', 'p70/solved') + drop)]
    TIDY = {
        'brawl': keep('p85/brawl/finish'),                                                     # (the ring's floor and bridges back, the charges taken)
        'party': G.FUNCS['p112/party/end'][1:3] + [                                            # (the floor back; whoever fell, up again)
            'execute positioned ~-11.9 ~-6 ~-11.9 as @a[tag=bm.gvp,dx=22.8,dy=3.4,dz=22.8] at @e[type=minecraft:marker,tag=bm.gvr_party,distance=..40,sort=nearest,limit=1] run tp @s ~ ~ ~'],
        'gallery': [l for l in G.FUNCS['p91/gallery/won'] if l.startswith('setblock ')],       # (the targets down)
        'hunted': ['kill @e[type=minecraft:creaking,tag=bm.gvstalk,distance=..30]', 'effect clear @a[tag=bm.gvp,distance=..16] minecraft:darkness'],
        'minecart': ['execute as @a[tag=bm.gvp,distance=..40,predicate=bm:p21/riding] run ride @s dismount', 'kill @e[type=minecraft:minecart,tag=bm.gvcart,distance=..40]'],
        'scramble': ['kill @e[type=minecraft:item,tag=bm.gvscoin,distance=..24]', 'clear @a[tag=bm.gvp,distance=..30] *[minecraft:custom_data~{bm_scr:1b}]'],
        'whack': ['execute as @e[type=minecraft:interaction,tag=bm.gvwhup,distance=..14] at @s run function bm:p85/whack/down'],
        'girder': ['kill @e[type=minecraft:block_display,tag=bm.gvbar,distance=..30]', 'kill @e[type=minecraft:item_display,tag=bm.gvgrat,distance=..30]'],
        'grass': ['tp @e[type=#bm:auto54,tag=bm.gvcrit,distance=..20] ~ -200 ~', 'kill @e[type=#bm:auto54,tag=bm.gvcrit]'],
        'plaza': ['kill @e[type=minecraft:husk,tag=bm.gvgrum,distance=..20]', 'kill @e[type=minecraft:item,tag=bm.gvpzc,distance=..20]',
                  'execute as @e[type=minecraft:interaction,tag=bm.gvflag,distance=..30] run data remove entity @s attack'],
        'storm': ['kill @e[type=minecraft:marker,tag=bm.gvstrike,distance=..20]', 'tp @e[type=minecraft:breeze,tag=bm.gvg,distance=..20] ~ -300 ~'],
        'ufo': ['kill @e[type=minecraft:interaction,tag=bm.gvcoreh,distance=..16]', 'tp @e[tag=bm.gvg,distance=..20] ~ -300 ~', 'kill @e[tag=bm.gvg,distance=..20]'],
        'grove': ['kill @e[type=minecraft:vex,tag=bm.gvg,distance=..20]', 'kill @e[type=minecraft:block_display,tag=bm.gvwisp,distance=..24]'],
        'hollow': ['kill @e[type=#bm:auto53,tag=bm.gvwisp,distance=..24]'],
        'voidg': ['tp @e[type=minecraft:shulker,tag=bm.gvvoid,distance=..20] ~ -200 ~', 'kill @e[type=minecraft:shulker,tag=bm.gvvoid]'],
    }
    assert not set(TIDY) - set(GAMES) and all(TIDY.values()), TIDY
    for k, ls in TIDY.items():
        fn(f'p122/tidy/{k}', ls)
    fn('p122/tidy', [f'execute if entity @s[tag=bm.gvr_{k}] run function bm:p122/tidy/{k}' for k in sorted(TIDY)])
    # (as a raider: tag the unsolved puzzle room of their heist they stand in - bm.skroom; #sk = 1 if there is one)
    fn('p122/find', ['tag @e[type=minecraft:marker,tag=bm.skroom] remove bm.skroom', 'scoreboard players set #sk bm.rng 0',
                     'scoreboard players operation #gi bm.rng = @s bm.gvi', 'tag @s add bm.skme',
                     'execute as @e[type=minecraft:marker,tag=bm.gvr,scores={bm.gvs=0..2}] if score @s bm.gvi = #gi bm.rng if function bm:p122/is_puzzle at @s '
                     'positioned ~-12.5 ~-12 ~-12.5 if entity @a[tag=bm.skme,dx=24,dy=48,dz=24] run tag @s add bm.skroom',
                     'tag @s remove bm.skme', 'execute if entity @e[type=minecraft:marker,tag=bm.skroom] run scoreboard players set #sk bm.rng 1'])
    # (#lv = the crew's tries left)
    fn('p122/tries', ['scoreboard players set #lv bm.rng 0',
                      'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng store result score #lv bm.rng run scoreboard players get @s bm.gvlv'])
    ask = P28.multi([T('Skip this room?', GOLD, bold=True)],
                    [P28.body([T('The way on opens as if you\'d solved it - and it costs the crew ', 'gray'), T('one try', 'red', bold=True),
                               T('. No coins for the pot, no flawless trophy.', 'gray')]),
                     P28.body([T('Tries left now: ', 'gray'), T('$(lv)', 'white', bold=True)])],
                    [P28.btn([T('Skip it  ', 'red', bold=True), T('(costs a try)', 'gray')], YES, width=200),
                     P28.btn([T('Keep at it', 'white')], None, width=200)], columns=1, exit_label='Back')
    ask['actions'][1]['action'] = {'type': 'minecraft:run_command', 'command': f'/trigger bm.act set {P28.NOOP}'}   # (closes it, nothing else - 1 opened the standing screen)
    fn('p122/ask_dlg', [f'$dialog show @s {P28.inline(ask)}'])
    fn('p122/ask', ['execute unless entity @s[tag=bm.gvp] run return 0', 'function bm:p122/find',
                    'execute if score #sk bm.rng matches 0 run return run ' + say('Stand in the room you want to skip (one that isn\'t solved yet).'),
                    'function bm:p122/tries',
                    'execute if score #lv bm.rng matches ..1 run return run ' + say('Not on your last try - a skip would end the heist.', 'red'),
                    'execute store result storage bm:ui sk.lv int 1 run scoreboard players get #lv bm.rng', 'function bm:p122/ask_dlg with storage bm:ui sk'])
    fn('p122/yes', ['execute unless entity @s[tag=bm.gvp] run return 0', 'function bm:p122/find',
                    'execute if score #sk bm.rng matches 0 run return run ' + say('No unsolved room here to skip - fights can\'t be skipped.'),
                    'function bm:p122/tries', 'execute if score #lv bm.rng matches ..1 run return run ' + say('Not on your last try - a skip would end the heist.', 'red'),
                    'tag @s add bm.skwho',
                    'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run function bm:p122/pay',
                    'execute as @e[type=minecraft:marker,tag=bm.skroom,limit=1] at @s run function bm:p122/open',
                    'tag @s remove bm.skwho', 'tag @e[type=minecraft:marker,tag=bm.skroom] remove bm.skroom'])
    fn('p122/pay', ['scoreboard players remove @s bm.gvlv 1', 'function bm:p70/bar', 'function bm:p70/tag_mine',
                    tellraw('@a[tag=bm.gvme]', P + [{'selector': '@a[tag=bm.skwho]', 'color': 'white'}, T(' skipped the room - ', 'gray'), T('that cost a try. ', 'red', bold=True),
                                                    {'score': {'name': '@s', 'objective': 'bm.gvlv'}, 'color': 'white', 'bold': True}, T(' tries left.', 'gray')]),
                    'tag @a[tag=bm.gvme] remove bm.gvme'])
    fn('p122/open', ['scoreboard players set @s bm.gvf 1', 'function bm:p70/ctx', 'scoreboard players operation #gi bm.rng = @s bm.gvi', 'function bm:p122/tidy', 'function bm:p70/solved',
                     'playsound minecraft:block.chain.break block @a[distance=..30] ~ ~ ~ 1 0.6'])
    G.FUNCS['p28/act'].insert(0, f'execute if score #act bm.pay matches {ASK} run return run function bm:p122/ask')
    G.FUNCS['p28/act'].insert(0, f'execute if score #act bm.pay matches {YES} run return run function bm:p122/yes')
    # (offered as you walk in: a click in the chat)
    G.FUNCS['p76/first_visit'].insert(1, 'execute if function bm:p122/is_puzzle run function bm:p122/offer')
    click = T('[Skip this room - costs a try]', '#ff9a7a', click_event={'action': 'run_command', 'command': f'/trigger bm.act set {ASK}'},
              hover_event={'action': 'show_text', 'value': T('Asks first. Opens the way on; the crew loses a try.', 'gray')})
    fn('p122/offer', ['scoreboard players operation #gi bm.rng = @s bm.gvi',
                      'execute as @a[tag=bm.gvp,distance=..40] if score @s bm.gvi = #gi bm.rng run ' + tellraw('@s', P + [T('Stuck? ', 'gray'), click])])
    # (and in the Ledger, on a heist)
    hub = G.FUNCS['p104/office_dlg']
    anchor = 'command:"/trigger bm.act set 7808"}}'
    assert anchor in hub[0]
    hub[0] = hub[0].replace(anchor, anchor + ',' + snbt(P28.btn([T('⏭ ', '#ff9a7a'), T('Skip this room', 'white', bold=True)], LEDGER,
                                                                  tooltip=T('In a puzzle or game room you can\'t crack? Skip it (not a fight) - the crew loses a try. Asks first.', 'gray'), width=150)))
    G.FUNCS['p80/act'].insert(2, f'execute if score #act bm.pay matches {LEDGER} run return run function bm:p122/ask')

    # (any guard still standing in a room when it's solved - a wrong move's, most likely - goes in a puff)
    G.FUNCS['p70/solved'].append('execute positioned ~-12.5 ~-4 ~-12.5 as @e[tag=bm.gvg,tag=!bm.gvboss,dx=24,dy=24,dz=24] at @s run function bm:p118/poof')
    G.FUNCS['p70/solved'].append('execute positioned ~-12.5 ~-4 ~-12.5 as @e[type=#bm:p118_spawnlings,tag=!bm.gnt,tag=!bm.gntl,tag=!bm.npc,dx=24,dy=24,dz=24] at @s run function bm:p118/poof')

    # (loose carpets: a room laid out over blocks its own setup then clears knocks its carpets off - swept up near the crew)
    second[-1:-1] = ['execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr,distance=0..] at @s if entity @a[tag=bm.gvp,distance=..24] run function bm:p122/sweep']
    fn('p122/sweep', [f'execute positioned ~-12.5 ~-6 ~-12.5 as @e[type=minecraft:item,dx=24,dy=26,dz=24] if items entity @s contents {pred} run kill @s'
                      for pred in ('#minecraft:wool_carpets', 'minecraft:moss_carpet', 'minecraft:pale_moss_carpet')])

    # ================================================================== A SOLO CREW: three
    k = G.FUNCS['p98/count'].index('execute if score #np bm.rng matches ..1 run scoreboard players set #lim bm.rng 2')
    G.FUNCS['p98/count'][k] = 'execute if score #np bm.rng matches ..1 run scoreboard players set #lim bm.rng 3'
    n = 0
    for name, L in G.FUNCS.items():
        for i, l in enumerate(L):
            if 'two when you raid alone' in l or 'Raid alone and two come along' in l:
                L[i] = l.replace('two when you raid alone', 'three when you raid alone').replace('Raid alone and two come along', 'Raid alone and three come along'); n += 1
    assert n >= 2, n

    # ================================================================== ENDLESS & PIT: no alarm switch
    ls = G.FUNCS['p75/lives_show'][0]
    abtn = snbt(P28.btn([T('ALARM: ', '#ff5a5a', bold=True), T('$(al)', 'white', bold=True), T('  (click to switch)', 'gray')], 7619, width=300,
                        tooltip=T('Off: no alarm, no patrols, no lockdown. On: mistakes ring it - at 50 guards patrol, at 100 the vault locks down - '
                                  'and you get one more share (two if you keep it under 50).', 'gray')))
    assert abtn + ',' in ls, 'the alarm button'
    na = ls.replace(abtn + ',', '').replace('The alarm is up to you: ', 'The alarm: ')
    fn('p122/lives_show_na', [na])
    lm = G.FUNCS['p75/lives_menu']
    k = lm.index('function bm:p75/lives_show with storage bm:gv m')
    lm[k:k + 1] = ['execute if score @s bm.gvpt matches 6..7 run data modify storage bm:gv m.al_txt set value "none in the Endless Vault or the Pit - it\'s a fight from the first room."',
                   'execute if score @s bm.gvpt matches 6..7 run return run function bm:p122/lives_show_na with storage bm:gv m',
                   'function bm:p75/lives_show with storage bm:gv m']
    pl = G.FUNCS['p75/pick_lives']
    k = pl.index('execute if score @s bm.gval matches 1 run scoreboard players set #al bm.rng 1')
    pl[k] = 'execute if score @s bm.gval matches 1 unless score @s bm.gvpt matches 6..7 run scoreboard players set #al bm.rng 1'

    # ================================================================== THE BOSS BAR: only near the boss
    for s in range(SL):
        second[-1:-1] = [f'execute unless entity @e[tag=bm.gvboss{s}] run bossbar set bm:gvb{s} players',
                         f'execute in bm:gutter as @e[tag=bm.gvboss{s},limit=1] at @s run bossbar set bm:gvb{s} players @a[tag=bm.gvp,scores={{bm.gvi={s + 1}}},distance=..30]']
    for f_ in ['p70/unraid'] + [k_ for k_ in G.FUNCS if k_.startswith('p70/boss/')]:
        G.FUNCS[f_] = [l for l in G.FUNCS[f_] if not (l.startswith('bossbar set bm:gvb') and ' players @a[tag=bm.gvp' in l and 'distance' not in l)]

    # ================================================================== BLOCK PARTY: the teleports land in the room
    mid = 'at @e[type=minecraft:marker,tag=bm.gvr_party,distance=..40,sort=nearest,limit=1] run tp @s ~ ~ ~'
    n = 0
    for f_ in ('p112/party/round', 'p112/party/end'):
        L = G.FUNCS[f_]
        for i, l in enumerate(L):
            if l.startswith('execute positioned ') and l.endswith(' run tp @s ~ ~ ~'):
                L[i] = l[:-len(' run tp @s ~ ~ ~')] + ' ' + mid; n += 1
    assert n == 2, n
    G.FUNCS['p112/party/fall'].append('execute at @e[type=minecraft:marker,tag=bm.gvr_party,distance=..40,sort=nearest,limit=1] run tp @s ~-11.5 ~ ~ 90 0')

    # ================================================================== THE MINECART RUN: no more shooting gallery
    mi = G.FUNCS['p115/minecart/init']
    k = mi.index('function bm:p110/var')
    mi.insert(k + 1, 'execute if score @s bm.gvvar matches 0 store result score @s bm.gvvar run random value 1..2')

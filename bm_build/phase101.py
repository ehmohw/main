"""2.67b: AFTER THE HEIST - win or lose, the leader decides what's next; Lucky Raids harder; raid followers back sooner.

WHEN IT'S OVER (the haul paid out, or the last try spent - the crew back in the den): the LEADER (whoever planned the heist;
  if they've gone, whoever's left first) gets a choice:
  - BACK TO THE OVERWORLD: the whole crew goes home, as they would through the plates.
  - START A NEW RAID: the Heist Plans open for the leader (tier, then tries, then their fee). Everyone else is asked to OPT IN
    or OUT. Out: home as usual. In: when the leader confirms, they're recruited and pay their OWN fee (no Tokens - left behind,
    home). Anyone who hasn't answered by then heads home. The new raid keeps everyone's way home and own spawn from before.
  Shut the window by mistake? The same choices sit in chat as buttons.
  (A failed heist no longer rebuilds itself for free: a new raid is a new plan, and a new fee.)
LUCKY RAIDS are harder by default: every guard and the guardian has half again the health (the guards hit harder too), and the
  heist rolls one modifier more.
RAID FOLLOWERS who faint in the vault are back in 45 seconds, not 5 minutes (only in the vault - a heist can be over quickly).
"""
from items import T
from nbt import snbt
import phase28 as P28
import phase70 as P70
import phase75 as P75

GOLD = '#ffcf40'
LUCKY = '#7dff6a'
SL = P70.SLOTS
C_HOME, C_NEXT, C_IN, C_OUT = 7720, 7721, 7722, 7723
RAID_CD = 45


def generate(G):
    fn, tellraw, title, PREFIX = G.fn, G.tellraw, G.title, G.PREFIX
    P = PREFIX
    second = []
    objs = ['bm.gvnx', 'bm.gvpq']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs

    # (every won heist pays at least its fee back - checked here, at build time)
    import phase90 as P90
    assert all(P75.PRIZE_TOK[t][0] >= P90.FEE_T[t] for t in P90.FEE_T), 'the Fixer\'s sure prize must cover the fee'

    crew = lambda s: f'@a[tag=bm.gvp,scores={{bm.gvi={s + 1}}}]'
    chat = lambda txt, col, code, tip: T(txt, col, bold=True, click_event={'action': 'run_command', 'command': f'/trigger bm.act set {code}'},
                                         hover_event={'action': 'show_text', 'value': T(tip, 'gray')})

    # ================================================================== the leader's choice
    lead_dlg = P28.multi([T('The heist is over', GOLD, bold=True)],
                         [P28.body([T('You planned this one, so it\'s your call: ', 'gray'), T('home', 'white', bold=True), T(', or ', 'gray'),
                                    T('another job', GOLD, bold=True), T('?', 'gray')]),
                          P28.body([T('A new raid opens the Heist Plans: pick the tier and tries, and pay your fee. Your crew is asked to opt in - '
                                      'each pays their own fee, and anyone who opts out goes home.', 'dark_gray')])],
                         [P28.btn([T('Back to the Overworld', 'white', bold=True)], C_HOME, width=200, tooltip=T('The whole crew heads home.', 'gray')),
                          P28.btn([T('Start a new raid', GOLD, bold=True)], C_NEXT, width=200, tooltip=T('Pick the next job - your crew opts in or out.', 'gray'))],
                         columns=1, exit_label='Decide later')
    lead_chat = tellraw('@s', P + [T('Home, or another job? ', 'gray'), chat('[Back to the Overworld]', 'white', C_HOME, 'The whole crew heads home.'), T('  '),
                                   chat('[Start a new raid]', GOLD, C_NEXT, 'Pick the next job - your crew opts in or out.')])
    for s in range(SL):
        fn(f'p101/s{s}/ask', ['tag @a[tag=bm.gvask] remove bm.gvask',
                              f'execute as {crew(s)} if score @s bm.pid = #ld{s} bm.gvld run tag @s add bm.gvask',
                              f'execute unless entity @a[tag=bm.gvask] run tag {crew(s)[:-1]},limit=1] add bm.gvask',
                              f'scoreboard players set @a[tag=bm.gvask] bm.gvnx {s + 1}',
                              'execute as @a[tag=bm.gvask] at @s run function bm:p101/ask_lead',
                              f'execute as {crew(s)[:-1]},tag=!bm.gvask] run function bm:p101/wait_note'])
    fn('p101/ask_lead', [f'dialog show @s {snbt(lead_dlg)}', lead_chat, 'playsound minecraft:block.note_block.chime player @s ~ ~ ~ 0.8 1.2'])
    fn('p101/wait_note', [tellraw('@s', P + [T('Waiting on ', 'gray'), {'selector': '@a[tag=bm.gvask]', 'color': 'white'},
                                             T(': home, or another job? (Or take the plate home any time.)', 'gray')])])

    # the codes (the chat buttons too - so no menu check: each one checks it's yours to press)
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {C_HOME}..{C_OUT} run return run function bm:p101/act')
    fn('p101/act', [f'execute if score #act bm.pay matches {C_HOME} run return run function bm:p101/go_home',
                    f'execute if score #act bm.pay matches {C_NEXT} run return run function bm:p101/go_next',
                    f'execute if score #act bm.pay matches {C_IN} run return run function bm:p101/opt_in',
                    f'execute if score #act bm.pay matches {C_OUT} run return run function bm:p101/opt_out'])
    # home: the whole crew, as through the plates
    fn('p101/go_home', ['execute unless entity @s[tag=bm.gvask] unless entity @s[tag=bm.gvnext] run return 0',
                        'tag @s remove bm.gvask', 'tag @s remove bm.gvnext'] +
       [f'execute if score @s bm.gvnx matches {s + 1} as {crew(s)} at @s run function bm:p101/send_home' for s in range(SL)] +
       ['scoreboard players reset @s bm.gvnx'])
    fn('p101/send_home', ['tag @s remove bm.gvoffer', 'tag @s remove bm.gvin', 'tag @s remove bm.gvask', 'tag @s remove bm.gvnext',
                          'function bm:p70/home', 'playsound minecraft:block.iron_door.open player @s ~ ~ ~ 1 0.8',
                          tellraw('@s', P + [T('The crew heads home. ', GOLD), T('Good work.', 'gray')])])
    # another job: the plans open for the leader; the rest are asked
    mem_dlg = P28.multi([T('Another job?', GOLD, bold=True)],
                        [P28.body([T('Your leader is planning the next heist. ', 'gray'), T('In?', GOLD, bold=True)]),
                         P28.body([T('You pay your own fee when the plan is set: 2 Tokens (Tier I) to 6 (Tier V). Out: you head home.', 'dark_gray')])],
                        [P28.btn([T('Count me in', GOLD, bold=True)], C_IN, width=200, tooltip=T('Come along - and pay your own fee.', 'gray')),
                         P28.btn([T('Head home', 'white', bold=True)], C_OUT, width=200, tooltip=T('Back to the Overworld, as usual.', 'gray'))],
                        columns=1, exit_label='Decide later')
    mem_chat = tellraw('@s', P + [T('Another job? ', 'gray'), chat('[Count me in]', GOLD, C_IN, 'Come along - and pay your own fee.'), T('  '),
                                  chat('[Head home]', 'white', C_OUT, 'Back to the Overworld, as usual.')])
    fn('p101/go_next', ['execute unless entity @s[tag=bm.gvask] unless entity @s[tag=bm.gvnext] run return 0',
                        'execute if entity @s[tag=bm.gvnext] run return run function bm:p70/menu',            # (pressed again: the plans reopen)
                        'tag @s remove bm.gvask', 'tag @s add bm.gvnext'] +
       [f'execute if score @s bm.gvnx matches {s + 1} as {crew(s)[:-1]},tag=!bm.gvnext] at @s run function bm:p101/offer' for s in range(SL)] +
       [tellraw('@s', P + [T('The Fixer unrolls a fresh set of plans. ', GOLD), T('Pick the job - your crew is deciding whether they\'re in.', 'gray')]),
        'function bm:p70/menu'])
    fn('p101/offer', ['tag @s add bm.gvoffer', 'tag @s remove bm.gvin', f'dialog show @s {snbt(mem_dlg)}', mem_chat,
                      'playsound minecraft:block.note_block.chime player @s ~ ~ ~ 0.8 1.2'])
    fn('p101/opt_in', ['execute unless entity @s[tag=bm.gvoffer] run return 0', 'tag @s remove bm.gvoffer', 'tag @s add bm.gvin',
                       tellraw('@s', P + [T('You\'re in. ', GOLD), T('You\'ll pay your fee when the plan is set.', 'gray')]),
                       'scoreboard players operation #me bm.pty = @s bm.pty', 'tag @s add bm.gvjust',
                       'execute as @a[tag=bm.gvnext] if score @s bm.pty = #me bm.pty run ' + tellraw('@s', P + [{'selector': '@a[tag=bm.gvjust]', 'color': 'white'},
                                                                                                          T(' is in.', GOLD)]),
                       'tag @s remove bm.gvjust'])
    fn('p101/opt_out', ['execute unless entity @s[tag=bm.gvoffer] run return 0', 'scoreboard players operation #me bm.pty = @s bm.pty', 'tag @s add bm.gvjust',
                        'execute as @a[tag=bm.gvnext] if score @s bm.pty = #me bm.pty run ' + tellraw('@s', P + [{'selector': '@a[tag=bm.gvjust]', 'color': 'white'}, T(' heads home.', 'gray')]),
                        'tag @s remove bm.gvjust', 'function bm:p101/send_home'])

    # ================================================================== a new raid from inside the vault: the plans work there for the leader
    nxt = 'execute unless entity @s[tag=bm.gvnext] '
    def unlock(f):
        L = G.FUNCS[f]
        for i, l in enumerate(L):
            if l == 'execute if dimension bm:gutter run return 0' or ('holds_plans' not in l and 'heist_plans' in l and 'run return run function bm:p28/stale' in l) or \
               l.startswith('execute unless dimension minecraft:overworld unless dimension minecraft:the_nether'):
                L[i] = nxt + l[len('execute '):]
    for f in ('p70/pick_tier', 'p75/pick_lives'):
        unlock(f)
    # ...and the claim takes along only those who opted in (by tag, anywhere in the vault - not whoever's standing near)
    for s in range(SL):
        cl = G.FUNCS[f'p70/s{s}/claim']
        k = next(i for i, l in enumerate(cl) if f'function bm:p70/s{s}/recruit' in l)
        cl[k] = nxt + cl[k][len('execute '):]
        cl.insert(k + 1, f'execute if entity @s[tag=bm.gvnext] as @a[tag=bm.gvin,tag=!bm.gvwait] at @s if score @s bm.pty = #asker bm.pty run function bm:p70/s{s}/recruit')
    # once the plan is set (the claim made): whoever couldn't pay, or never answered, goes home; the leader's done deciding
    G.FUNCS['p75/pick_lives'].append('execute if entity @s[tag=bm.gvnext] run function bm:p101/claimed')
    fn('p101/claimed', ['tag @s remove bm.gvnext', 'tag @s remove bm.gvask', 'scoreboard players reset @s bm.gvnx', 'scoreboard players operation #me bm.pty = @s bm.pty',
                        'execute as @a[tag=bm.gvin,tag=!bm.gvwait] if score @s bm.pty = #me bm.pty at @s run function bm:p101/left_behind',
                        'execute as @a[tag=bm.gvoffer] if score @s bm.pty = #me bm.pty at @s run function bm:p101/no_answer',
                        'execute as @a[tag=bm.gvin] if score @s bm.pty = #me bm.pty run tag @s remove bm.gvin'])
    fn('p101/left_behind', [tellraw('@s', P + [T('No fee, no job - ', 'red'), T('you head home.', 'gray')]), 'function bm:p101/send_home'])
    fn('p101/no_answer', [tellraw('@s', P + [T('The crew moved on without an answer from you - ', 'gray'), T('you head home.', 'white')]), 'function bm:p101/send_home'])
    # straight from one heist into the next: keep the way home, the coat check and your own spawn from the first
    G.FUNCS['p70/save_ret'].insert(0, 'execute if dimension bm:gutter run return 0')
    G.FUNCS['p75/sp_save'].insert(0, 'execute if dimension bm:gutter run return 0')
    G.FUNCS['p72/bag/check'].insert(0, 'execute if dimension bm:gutter run return 0')
    # (waiting to be taken into the next one - between the plan and the build - you still belong)
    G.FUNCS['p70/belong'].insert(0, 'execute if entity @s[tag=bm.gvwait] run return 0')
    fn('p101/bars', ['tag @s remove bm.gvdead'] +
       [f'bossbar set bm:gva{s} players @a[tag=bm.gvp,scores={{bm.gvi={s + 1}}}]' for s in range(SL)] +
       [f'bossbar set bm:gvb{s} players @a[tag=bm.gvp,scores={{bm.gvi={s + 1}}}]' for s in range(SL)])
    for s in range(SL):
        G.FUNCS[f'p70/s{s}/enter'].append('function bm:p101/bars')

    # ================================================================== the fee from inside the vault: the Fixer takes it from what he's minding for you
    # (the coat check holds your Tokens while you're in a heist - a new raid's fee comes out of your bag, stack by stack)
    tokq = 'bf.one[{components:{"minecraft:custom_data":{bm:"token"}}}]'      # (the element under test, alone in a list)
    one = ['data modify storage bm:gv bf.one set value []', 'data modify storage bm:gv bf.one append from storage bm:gv bf.tk[0]']
    fee = G.FUNCS['p75/fee']
    k = next(i for i, l in enumerate(fee) if l.startswith('execute store result score #tk bm.rng run clear @s'))
    fee.insert(k + 1, 'execute if dimension bm:gutter if score #tk bm.rng < #fee bm.rng run return run function bm:p101/fee_bag')
    fn('p101/fee_bag', ['function bm:p101/bag_count', 'execute if score #bagtk bm.rng < #fee bm.rng run return run function bm:p75/fee_no',
                        'scoreboard players operation #need bm.rng = #fee bm.rng', 'execute store result storage bm:gv bf.pid int 1 run scoreboard players get @s bm.pid',
                        'function bm:p101/bag_take with storage bm:gv bf', 'scoreboard players operation #lpool bm.gvlp += #fee bm.rng',
                        tellraw('@s', P + [T('You pay the Fixer\'s fee (', 'gray'), {'score': {'name': '#fee', 'objective': 'bm.rng'}, 'color': 'white'},
                                           T(' Tokens) out of what he\'s minding for you. ', 'gray'), T('Lucky pool: ', LUCKY),
                                           {'score': {'name': '#lpool', 'objective': 'bm.gvlp'}, 'color': LUCKY, 'bold': True}]), 'return 1'])
    # (as a player) #bagtk = the Tokens in their coat-check bag
    fn('p101/bag_count', ['execute store result storage bm:gv bf.pid int 1 run scoreboard players get @s bm.pid', 'scoreboard players set #bagtk bm.rng 0',
                          'function bm:p101/bag_count2 with storage bm:gv bf'])
    fn('p101/bag_count2', ['data remove storage bm:gv bf.tk', '$data modify storage bm:gv bf.tk set from storage bm:gv bag.p$(pid).inv', 'function bm:p101/bag_count3'])
    fn('p101/bag_count3', ['execute unless data storage bm:gv bf.tk[0] run return 0'] + one + [
                           f'execute if data storage bm:gv {tokq} store result score #c bm.rng run data get storage bm:gv bf.tk[0].count',
                           f'execute if data storage bm:gv {tokq} unless data storage bm:gv bf.tk[0].count run scoreboard players set #c bm.rng 1',
                           f'execute if data storage bm:gv {tokq} run scoreboard players operation #bagtk bm.rng += #c bm.rng',
                           'data remove storage bm:gv bf.tk[0]', 'function bm:p101/bag_count3'])
    # (#need Tokens out of the bag: whole stacks first, the last one cut down)
    fn('p101/bag_take', ['data remove storage bm:gv bf.tk', '$data modify storage bm:gv bf.tk set from storage bm:gv bag.p$(pid).inv',
                         'data modify storage bm:gv bf.out set value []', 'function bm:p101/bag_take2', '$data modify storage bm:gv bag.p$(pid).inv set from storage bm:gv bf.out'])
    fn('p101/bag_take2', ['execute unless data storage bm:gv bf.tk[0] run return 0', 'data remove storage bm:gv bf.drop'] + one + [
                          f'execute if data storage bm:gv {tokq} if score #need bm.rng matches 1.. run function bm:p101/bag_take3',
                          'execute unless data storage bm:gv bf.drop run data modify storage bm:gv bf.out append from storage bm:gv bf.tk[0]',
                          'data remove storage bm:gv bf.tk[0]', 'function bm:p101/bag_take2'])
    fn('p101/bag_take3', ['execute store result score #c bm.rng run data get storage bm:gv bf.tk[0].count', 'execute unless data storage bm:gv bf.tk[0].count run scoreboard players set #c bm.rng 1',
                          'scoreboard players operation #left bm.rng = #c bm.rng', 'scoreboard players operation #left bm.rng -= #need bm.rng',
                          'execute if score #left bm.rng matches ..0 run data modify storage bm:gv bf.drop set value 1b',
                          'execute if score #left bm.rng matches ..0 run scoreboard players operation #need bm.rng -= #c bm.rng',
                          'execute if score #left bm.rng matches 1.. store result storage bm:gv bf.tk[0].count int 1 run scoreboard players get #left bm.rng',
                          'execute if score #left bm.rng matches 1.. run scoreboard players set #need bm.rng 0'])

    # ================================================================== the fee back with any haul (the 2-5 more, Medallions and Trophies stay the Black Market haul's)
    HA, HB = '-200 64 -197', '-198 64 -197'                 # (phase75's haul barrels)
    G.FUNCS['p75/prize'].insert(0, 'execute unless score #th bm.rng matches 2 run return run function bm:p101/fee_back')
    fn('p101/fee_back', ['scoreboard players set #ptk bm.rng 0', 'scoreboard players set #pbx bm.rng 0'] +
       [f'execute if score #gt bm.rng matches {t} run scoreboard players set #ptk bm.rng {sure}' for t, (sure, pct) in P75.PRIZE_TOK.items()] +
       [f'execute if score #ptk bm.rng matches 1.. in bm:gutter unless data block {HA} Items[26] run loot insert {HA} loot bm:p75/prize_tokens',
        f'execute if score #ptk bm.rng matches 1.. in bm:gutter if data block {HA} Items[26] run loot insert {HB} loot bm:p75/prize_tokens',
        'execute if score #ptk bm.rng matches 1.. run ' + tellraw('@s', P + [T('The Fixer\'s prize: ', GOLD), T('your fee back, ', 'gray'),
                                                                            {'score': {'name': '#ptk', 'objective': 'bm.rng'}, 'color': 'white', 'bold': True}, T(' Token(s).', 'gray')])])

    # ================================================================== when to ask: a few seconds after the haul; a failed heist once the crew's back in the den
    pay = G.FUNCS['p70/payout_inst']
    pay += [f'execute if score @s bm.gvi matches {s + 1} run scoreboard players set #pq{s} bm.gvpq 5' for s in range(SL)] + ['tag @a[tag=bm.lkld] remove bm.lkld']
    for s in range(SL):
        second.append(f'execute if score #pq{s} bm.gvpq matches 1.. run function bm:p101/s{s}/pq')
        fn(f'p101/s{s}/pq', [f'scoreboard players remove #pq{s} bm.gvpq 1', f'execute if score #pq{s} bm.gvpq matches 0 run function bm:p101/s{s}/ask'])
        # (the failed heist: back to the den - no free rebuild any more; the leader decides)
        z0 = P75.zoff(s)
        G.FUNCS[f'p75/s{s}/reset'] = [l for l in G.FUNCS[f'p75/s{s}/reset'] if 'p77/endless/unload' in l] + [f'scoreboard players set #gi bm.rng {s + 1}',
                                      f'execute as {crew(s)} in bm:gutter run tp @s {P75.DEN[0]} {P75.DEN[1]} {z0 + P75.DEN[2]} -90 0',
                                      f'execute as {crew(s)} run function bm:p101/after_fail', f'function bm:p101/s{s}/ask']
    G.FUNCS.pop('p75/after_fail', None)                 # (the free rebuild's message - gone with it)
    fn('p101/after_fail', ['function bm:p70/glass_check', 'effect clear @s', 'effect give @s minecraft:instant_health 1 4 true',
                           tellraw('@s', P + [T('Back in the den. ', GOLD), T('Everything gathered is lost - the leader decides what\'s next.', 'gray')])])

    # ================================================================== LUCKY RAIDS: harder
    gs = G.FUNCS['p70/guard_set1']
    k = next(i for i, l in enumerate(gs) if l.startswith('execute store result storage bm:gv h double 1 run scoreboard players get #h bm.rng'))
    gs[k:k] = [f'execute if score #gi bm.rng matches {s + 1} if score #lu{s} bm.gvlu matches 1 run function bm:p101/lk_guard' for s in range(SL)]
    fn('p101/lk_guard', ['scoreboard players operation #h bm.rng *= #3 bm.rng', 'scoreboard players operation #h bm.rng /= #2 bm.rng',
                         'effect give @s minecraft:strength infinite 0 true', 'tag @s add bm.lkhard'])
    for s in range(SL):
        second.append(f'execute if score #lu{s} bm.gvlu matches 1 in bm:gutter as @e[tag=bm.gvboss{s},tag=!bm.lkhard] run function bm:p101/lk_boss')
    fn('p101/lk_boss', ['tag @s add bm.lkhard', 'attribute @s minecraft:max_health modifier add bm:lucky_hard 0.5 add_multiplied_base',
                        'data modify entity @s Health set value 4096f'])
    G.FUNCS['p70/roll_mods'] += [f'execute if score #gs bm.rng matches {s} if score #lu{s} bm.gvlu matches 1 run function bm:p101/lk_mod' for s in range(SL)]
    fn('p101/lk_mod', ['scoreboard players set #nm bm.rng 1', 'function bm:p70/roll_mod'])
    G.FUNCS['p75/lucky_announce'].insert(-1, tellraw('@a[tag=bm.gvme]', P + [T('LUCKY RAID! ', LUCKY, bold=True),
                                                                            T('Harder than it looks: the guards and the guardian are tougher, and there\'s one modifier more. ', 'gray'),
                                                                            T('Win it and the pool is split between you (the odd Tokens to the leader).', LUCKY)]))

    # ================================================================== RAID FOLLOWERS: back in 45 seconds
    import phase98 as P98
    cds = [v[6] for v in P98.CALLED] + [v[4] for v in P98.HIRED]
    second.append('execute in bm:gutter as @a[tag=bm.gvp,distance=0..] run function bm:p101/cd')
    fn('p101/cd', [f'execute if score @s {cd} matches {P98_CD_FRESH}.. run function bm:p101/cd_{i}' for i, cd in enumerate(cds)])
    for i, cd in enumerate(cds):
        fn(f'p101/cd_{i}', [f'scoreboard players set @s {cd} {RAID_CD}',
                            tellraw('@s', P + [T('In the vault your follower is back on their feet in ', 'gray'), T(f'{RAID_CD} seconds', GOLD, bold=True), T('.', 'gray')])])

    s_ = G.FUNCS['loop/second']
    s_[-1:-1] = second


P98_CD_FRESH = 290          # (a faint just now: 300 down to here - an older one, from outside the vault, keeps its time)

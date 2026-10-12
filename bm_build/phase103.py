"""2.67d: THE VAULT, SMOOTHED OUT - exits that ask first, a crew that needn't wait, a den laid out by job, three shopkeepers,
a clearer Raid Crew, one end-of-heist card, followers that come home with you, a ready check, and the Fixer's Door.

EXITS ASK FIRST WHILE A HEIST IS ON: step into the way out mid-run and the Fixer asks - leave now (your share stays behind,
  the crew carries on) or stay. Before the heist begins, after a win or after a fail, it's instant as ever.
NOBODY WAITS ON THE LEADER: when a heist ends the crew gets their own card - HEAD HOME NOW, or I'M IN IF WE GO AGAIN (you're
  taken along without being asked again, and pay your own fee then). A leader who hasn't chosen in 75 seconds passes the
  choice on to the crew (a solo raider takes as long as they like). Closed the card? Use the Fixer's Ledger: while it's
  your call it opens your choice again (its Office button carries on to the Office).
"""
from items import T
from nbt import snbt
import phase28 as P28
import phase70 as P70
import phase70_rooms as RM

GOLD = '#ffcf40'
LUCKY = '#7dff6a'
SL = P70.SLOTS
C_LEAVE, C_STAY, C_MHOME, C_PREIN, C_OFFICE = 7724, 7725, 7726, 7727, 7728
DECIDE_S = 75                                  # seconds a leader has before the choice passes on (with a crew waiting)
DEN_EXIT = (2, 4, 4)                           # the den's way out (local)
VAULT_EXIT = (34, 4, 12)                       # the treasury's way out, once the vault is open (local)


def generate(G):
    fn, tellraw, title, PREFIX = G.fn, G.tellraw, G.title, G.PREFIX
    P = PREFIX
    rel = RM.rel
    tick, fast, second = [], [], []
    objs = ['bm.gvdt']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    crew = lambda s: f'@a[tag=bm.gvp,scores={{bm.gvi={s + 1}}}]'
    chat = lambda txt, col, code, tip: T(txt, col, bold=True, click_event={'action': 'run_command', 'command': f'/trigger bm.act set {code}'},
                                         hover_event={'action': 'show_text', 'value': T(tip, 'gray')})
    say = lambda txt, col='gray': tellraw('@s', P + [T(txt, col)])
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {C_LEAVE}..{C_OFFICE} run return run function bm:p103/act')
    fn('p103/act', [f'execute if score #act bm.pay matches {C_LEAVE} run return run function bm:p103/leave_yes',
                    f'execute if score #act bm.pay matches {C_STAY} run return run function bm:p103/leave_no',
                    f'execute if score #act bm.pay matches {C_MHOME} run return run function bm:p103/mem_home',
                    f'execute if score #act bm.pay matches {C_PREIN} run return run function bm:p103/pre_in',
                    f'execute if score #act bm.pay matches {C_OFFICE} run return run function bm:p80/office'])

    # ================================================================== 1a. THE WAY OUT ASKS FIRST WHILE THE HEIST IS ON
    # (each way out is a marker, bm.exitm: the den's from the start, the treasury's once the vault opens. Standing in one shows
    #  the question once - step out and back in to see it again.)
    lt = G.FUNCS['p70/r/lobby/tick']
    old = f'execute positioned {rel(*DEN_EXIT)} as @a[tag=bm.gvp,distance=..0.8] at @s run function bm:p70/leave'
    assert old in lt, 'the den\'s leave plate line moved'
    lt.remove(old)
    vt = G.FUNCS['p70/r/vault/tick']
    old = f'execute if score @s bm.gvs matches 2.. positioned {rel(*VAULT_EXIT)} as @a[tag=bm.gvp,distance=..0.9] at @s run function bm:p70/leave'
    assert old in vt, 'the treasury\'s way-out line moved'
    vt.remove(old)
    G.FUNCS['p70/r/lobby/init'].append(f'summon minecraft:marker {rel(*DEN_EXIT)} {{Tags:["bm.gvprop","bm.exitm"]}}')
    G.FUNCS['p70/r/vault/open'].append(f'summon minecraft:marker {rel(*VAULT_EXIT)} {{Tags:["bm.gvprop","bm.exitm"]}}')
    tick += ['execute as @e[type=minecraft:marker,tag=bm.exitm] at @s as @a[tag=bm.gvp,tag=!bm.exon,distance=..0.9] at @s run function bm:p103/exit',
             'execute as @a[tag=bm.exon] at @s unless entity @e[type=minecraft:marker,tag=bm.exitm,distance=..1.8] run function bm:p103/exit_off']
    fn('p103/exit_off', ['tag @s remove bm.exon', 'tag @s remove bm.exask'])
    fn('p103/exit', ['tag @s add bm.exon', 'scoreboard players operation #gi bm.rng = @s bm.gvi', 'scoreboard players set #st bm.rng 0',
                     'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng store result score #st bm.rng run scoreboard players get @s bm.gvst',
                     'execute unless score #st bm.rng matches 2..3 run return run function bm:p70/leave',
                     'tag @s add bm.exask', 'function bm:p103/exit_ask', 'playsound minecraft:block.iron_door.close player @s ~ ~ ~ 0.8 0.8'])
    ask = P28.multi([T('Leave the heist?', GOLD, bold=True)],
                    [P28.body([T('The heist is still on. ', 'white'), T('Leave now and your share stays behind', '#ff9a7a'),
                               T(' - the crew carries on without you, and you go home as you came.', 'gray')])],
                    [P28.btn([T('Leave now', '#ff9a7a', bold=True)], C_LEAVE, width=200, tooltip=T('Home, out of the heist.', 'gray')),
                     P28.btn([T('Stay', LUCKY, bold=True)], C_STAY, width=200, tooltip=T('Back to the job.', 'gray'))],
                    columns=1, exit_label='Stay')
    fn('p103/exit_ask', [f'dialog show @s {snbt(ask)}'])
    fn('p103/leave_yes', ['execute unless entity @s[tag=bm.exask] run return 0', 'tag @s remove bm.exask',
                          'execute unless entity @s[tag=bm.gvp] run return 0', 'execute at @s run function bm:p70/leave'])
    fn('p103/leave_no', ['execute unless entity @s[tag=bm.exask] run return 0', 'tag @s remove bm.exask', say('You stay with the job.', LUCKY)])

    # ================================================================== 1b. NOBODY WAITS ON THE LEADER
    mem = P28.multi([T('The heist is over', GOLD, bold=True)],
                    [P28.body([T('Your leader is choosing: ', 'gray'), T('home', 'white', bold=True), T(', or ', 'gray'), T('another job', GOLD, bold=True), T('.', 'gray')]),
                     P28.body([T('You needn\'t wait. Head home now - or say you\'re in, and if they go again you come along (and pay your own fee then).',
                                 'dark_gray')])],
                    [P28.btn([T('Head home now', 'white', bold=True)], C_MHOME, width=200, tooltip=T('Back to the Overworld, as usual.', 'gray')),
                     P28.btn([T('I\'m in if we go again', GOLD, bold=True)], C_PREIN, width=200, tooltip=T('Come along if there\'s another job.', 'gray')),
                     P28.btn([T('The Fixer\'s Office', 'gray')], C_OFFICE, width=200)],
                    columns=1, exit_label='Decide later')
    mem_chat = tellraw('@s', P + [T('Waiting on ', 'gray'), {'selector': '@a[tag=bm.gvask]', 'color': 'white'}, T(': ', 'gray'),
                                  chat('[Head home now]', 'white', C_MHOME, 'Back to the Overworld, as usual.'), T('  '),
                                  chat('[I\'m in if we go again]', GOLD, C_PREIN, 'Come along if there\'s another job.')])
    G.FUNCS['p101/wait_note'][:] = ['tag @s add bm.gvwaitd', 'function bm:p103/mem_show', mem_chat, 'playsound minecraft:block.note_block.chime player @s ~ ~ ~ 0.6 1.0']
    fn('p103/mem_show', [f'dialog show @s {snbt(mem)}'])
    # (the member's buttons: home now - any time while it's being decided; in - only while waiting)
    notify = lambda txt, col: ['scoreboard players operation #mi bm.rng = @s bm.gvi', 'tag @s add bm.gvjust',
                               'execute as @a[tag=bm.gvp] if score @s bm.gvi = #mi bm.rng unless entity @s[tag=bm.gvjust] run ' +
                               tellraw('@s', P + [{'selector': '@a[tag=bm.gvjust]', 'color': 'white'}, T(txt, col)]),
                               'tag @s remove bm.gvjust']
    fn('p103/mem_home', ['execute unless entity @s[tag=bm.gvwaitd] unless entity @s[tag=bm.gvoffer] unless entity @s[tag=bm.gvin] run return 0'] +
       notify(' heads home.', 'gray') + ['execute at @s run function bm:p101/send_home'])
    fn('p103/pre_in', ['execute unless entity @s[tag=bm.gvwaitd] run return 0', 'tag @s add bm.gvpre'] + notify(' is in if you go again.', GOLD) +
       [say('You\'re in - if the leader goes again, you come along (and pay your own fee then).', GOLD)])
    # (a new raid: whoever said they're in is taken along without being asked again)
    G.FUNCS['p101/offer'][0:0] = ['tag @s remove bm.gvwaitd', 'execute if entity @s[tag=bm.gvpre] run return run function bm:p103/auto_in']
    fn('p103/auto_in', ['tag @s remove bm.gvpre', 'tag @s add bm.gvoffer', 'function bm:p101/opt_in'])
    # (every way the deciding ends clears the member tags)
    clear = ['tag @s remove bm.gvwaitd', 'tag @s remove bm.gvpre']
    G.FUNCS['p101/send_home'][0:0] = clear
    G.FUNCS['p70/unraid'] += clear + ['tag @s remove bm.exon', 'tag @s remove bm.exask']
    G.FUNCS['p101/claimed'].append('execute as @a[tag=bm.gvp] if score @s bm.pty = #me bm.pty run function bm:p103/mem_clear')
    fn('p103/mem_clear', clear)
    G.FUNCS['p101/ask_lead'][0:0] = clear                             # (the choice passed to someone who'd said they're in)

    # ================================================================== 1c. A LEADER WHO DOESN'T CHOOSE PASSES THE CHOICE ON
    for s in range(SL):
        a = G.FUNCS[f'p101/s{s}/ask']
        assert a[0] == 'tag @a[tag=bm.gvask] remove bm.gvask'
        a[0] = f'tag {crew(s)} remove bm.gvask'                       # (2.67d: only this heist's - two heists could end together)
        a.append(f'scoreboard players set #dt{s} bm.gvdt {DECIDE_S}')
        second.append(f'execute if score #dt{s} bm.gvdt matches 1.. run function bm:p103/s{s}/dt')
        asker = f'@a[tag=bm.gvask,scores={{bm.gvnx={s + 1}}}]'
        fn(f'p103/s{s}/dt', [f'execute unless entity {asker} run return run scoreboard players set #dt{s} bm.gvdt 0',
                             f'execute store result score #n bm.rng if entity {crew(s)}',
                             f'execute if score #n bm.rng matches ..1 run return run scoreboard players set #dt{s} bm.gvdt 0',
                             f'scoreboard players remove #dt{s} bm.gvdt 1',
                             f'execute if score #dt{s} bm.gvdt matches 15 run ' + tellraw(asker, P + [T('15 seconds to choose', GOLD, bold=True),
                                                                                                   T(' - then the choice passes to your crew.', 'gray')]),
                             f'execute if score #dt{s} bm.gvdt matches 0 run function bm:p103/s{s}/pass'])
        fn(f'p103/s{s}/pass', [f'tag {asker} add bm.gvskip',
                               f'execute as {crew(s)[:-1]},tag=!bm.gvskip,limit=1] run scoreboard players operation #ld{s} bm.gvld = @s bm.pid',
                               tellraw('@a[tag=bm.gvskip]', P + [T('Time\'s up - ', 'gray'), T('the choice passes to your crew.', GOLD)]),
                               'scoreboard players reset @a[tag=bm.gvskip] bm.gvnx', 'tag @a[tag=bm.gvskip] remove bm.gvask', 'tag @a[tag=bm.gvskip] remove bm.gvskip',
                               f'function bm:p101/s{s}/ask'])

    # ================================================================== 1d. CLOSED THE CARD? THE LEDGER OPENS YOUR CHOICE AGAIN
    L = G.FUNCS['p80/ledger']
    k = L.index('function bm:p80/office')
    L[k:k] = ['execute if entity @s[tag=bm.gvask] run return run function bm:p101/ask_lead',
              'execute if entity @s[tag=bm.gvnext] run return run function bm:p70/menu',
              'execute if entity @s[tag=bm.gvoffer] run return run function bm:p103/offer_show',
              'execute if entity @s[tag=bm.gvwaitd] run return run function bm:p103/mem_show']
    off = G.FUNCS['p101/offer']
    dlg = next(l for l in off if l.startswith('dialog show @s '))
    fn('p103/offer_show', [dlg])

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    f[-1:-1] = fast
    s_ = G.FUNCS['loop/second']
    s_[-1:-1] = second

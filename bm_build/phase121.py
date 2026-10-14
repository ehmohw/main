"""2.74: THE FIXER'S LOUNGE - the den, without a heist.

THE LOUNGE      a den of its own in a quiet corner of the vault, never part of a heist: Goldtooth, the Recruiter and the
                Tailor at their counter, the Gutter Bank, the Armory, the Raid Crew board, the Crate Desk, the Scrap Box and
                the copper door to the Locker Hall - shop, bank, rank up and sort your lockers without planning a raid or
                paying a fee. No loaner racks, no BEGIN; the Fixer's Door takes you back where you came from.
GETTING THERE   the Fixer's Ledger: THE FIXER'S LOUNGE in the Office (from safe ground, hold still for 3 seconds - as for
                the Locker Hall). And when a heist ends, the leader's choice and the crew's offer both add GO TO THE
                LOUNGE: the heist ends as if you'd headed home, and you step into the lounge instead - its door then
                takes you home.
                (You can't break anything in there - it puts you in adventure mode while you're in it.)
"""
import re
from items import T
from nbt import snbt, B, F, Int
import phase28 as P28
import phase70_rooms as RM
import phase80 as P80
import phase84 as P84

GOLD, LOUNGE = '#ffcf40', '#e8c070'
OX, OY, OZ = -320, 64, -256                       # the template's corner (bm:gutter); the room's marker is +12.5 +4 +12.5
MX, MY, MZ = OX + 12.5, OY + 4, OZ + 12.5
BOX = (OX - 1, OY - 4, OZ - 1, 26, 20, 26)        # (x, y, z, dx, dy, dz) - inside the lounge
VER = 2                                           # (2: the template's own room marker removed - it joined heists)
TRIP = 7880                                       # the Office's button (the Ledger)
C_LEAD, C_MEM, C_OUT = 7730, 7731, 7732           # the end-of-heist choices (the leader; a member waiting; a member asked to go again)


def generate(G):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    tick, fast, second = G.FUNCS['tick'], G.FUNCS['loop/fast'], G.FUNCS['loop/second']
    P = [T('[', 'dark_gray'), T('Lounge', LOUNGE, bold=True), T('] ', 'dark_gray')]
    say = lambda txt, col='gray': tellraw('@s', P + [T(txt, col)])
    bx, by, bz, dx, dy, dz = BOX
    G.FUNCS['load'][-1:-1] = [f'execute in bm:gutter run forceload add {OX - 1} {OZ - 1} {OX + 25} {OZ + 25}']

    # ================================================================== the room: the den's template, and the den's counter
    skip = ('scoreboard players operation #gi bm.rng = @s bm.gvi', 'bm.gvsheet', 'bm.gvboard', 'bm.gvnew3', 'p70/claim_disp', 'function bm:p70/sheet',
            'function bm:p70/board', 'bm.gvkit', 'LOANERS', 'pale_oak_button', 'text:"BEGIN"', 'BACK TO THE CREW', 'bm.gvpoold', 'p75/pool_show',
            'minecraft:emerald_block', 'polished_blackstone_pressure_plate') + tuple(f'{{text:"{r}\\n"' for r in ('TANK', 'OFFENSE', 'RANGED', 'SUPPORT'))
    props = []
    for l in G.FUNCS['p70/r/lobby/init']:
        if any(s in l for s in skip):
            continue
        l = l.replace('"bm.gvprop"', '"bm.lgprop"').replace('"bm.exitm"', '"bm.lgexit"')
        l = l.replace('home (it asks first, mid-heist)', 'back where you came from')
        props.append(l)
    assert sum('summon minecraft:villager' in l for l in props) == 3, 'Goldtooth, the Recruiter and the Tailor'
    assert any('bm.lgexit' in l for l in props) and any('bm.tailhit' in l for l in props) and any('bm.ofcrew' in l for l in props)
    WALL = RM.WALL
    rel = lambda x, y, z: f'~{x - 12:g} ~{y - 4:g} ~{z - 12:g}'.replace('~0 ', '~ ').replace('~0', '~')
    props += [f'fill {rel(25, 4, 9)} {rel(25, 9, 15)} {WALL}',                      # (the way on into a heist: walled up)
              'summon minecraft:text_display ~-6.5 ~2 ~-11 ' + snbt({'Tags': ['bm.lgprop'], 'billboard': 'fixed', 'line_width': Int(220), 'background': Int(0x70000000),
                                                                     'text': [T("THE FIXER'S LOUNGE\n", LOUNGE, bold=True),
                                                                              T('The den, without a heist. Shop, bank, rank up your kits and sort your lockers - '
                                                                                'no plans, no fee. The Fixer\'s Door takes you back.', 'gray')],
                                                                     'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                                                                        'translation': [F(0)] * 3, 'scale': [F(0.8)] * 3}})]
    fn('p121/props', props)
    fn('p121/build', [f'kill @e[tag=bm.lgprop,x={bx},y={by},z={bz},dx={dx},dy={dy},dz={dz}]',
                      f'kill @e[type=minecraft:marker,tag=bm.lgm,x={bx},y={by},z={bz},dx={dx},dy={dy},dz={dz}]',
                      f'kill @e[type=minecraft:villager,tag=bm.npc,x={bx},y={by},z={bz},dx={dx},dy={dy},dz={dz}]',
                      f'kill @e[type=minecraft:text_display,tag=bm.plate,x={bx},y={by},z={bz},dx={dx},dy={dy},dz={dz}]',
                      f'place template bm:gv_lobby_t3 {OX} {OY} {OZ}',
                      f'kill @e[type=minecraft:marker,x={bx},y={by},z={bz},dx={dx},dy={dy},dz={dz}]',            # (the den template carries the den's room marker - not here: it would join a heist)
                      f'summon minecraft:marker {MX} {MY} {MZ} {{Tags:["bm.lgm"]}}',
                      'scoreboard players set #gt bm.rng 3',
                      f'execute as @e[type=minecraft:marker,tag=bm.lgm,limit=1] at @s run function bm:p121/props',
                      f'kill @e[type=minecraft:item,x={bx},y={by},z={bz},dx={dx},dy={dy},dz={dz}]',
                      f'data modify storage bm:lg built set value {VER}'])
    second[-1:-1] = [f'execute in bm:gutter if loaded {OX} {OY} {OZ} unless data storage bm:lg {{built:{VER}}} run function bm:p121/build']
    second[-1:-1] = [f'execute in bm:gutter run kill @e[type=minecraft:marker,tag=bm.gvr,x={bx},y={by},z={bz},dx={dx},dy={dy},dz={dz}]']
    fn('admin/lounge_rebuild', ['data remove storage bm:lg built', 'execute in bm:gutter run function bm:p121/build'])

    # ================================================================== in the lounge: not a heist, nobody sent home, nothing broken
    # (where the player is - not where the command runs: so 'at @s', whoever calls it)
    fn('p121/inside', ['execute at @s unless dimension bm:gutter run return 0', f'execute at @s positioned {bx} {by} {bz} if entity @s[dx={dx},dy={dy},dz={dz}] run return 1', 'return 0'])
    li_ = G.FUNCS['p84/lk/inside']                         # (the Locker Hall's own check had the same slip: its adventure mode never stuck)
    li_[:] = [l.replace('execute unless dimension bm:gutter', 'execute at @s unless dimension bm:gutter').replace('execute positioned', 'execute at @s positioned') for l in li_]
    assert all('at @s' in l for l in li_ if l.startswith('execute')), li_
    G.FUNCS['p70/belong'][0:0] = ['execute if function bm:p121/inside run return 0']
    G.FUNCS['p80/can'][0:0] = ['execute if function bm:p121/inside run return 1']      # (the Office's counter works without a Ledger in hand)
    second += [f'execute in bm:gutter positioned {bx} {by} {bz} as @a[dx={dx},dy={dy},dz={dz},gamemode=survival] run function bm:p121/adv',
               'execute as @a[tag=bm.lgadv] unless function bm:p121/inside run function bm:p121/unadv']
    fn('p121/adv', ['gamemode adventure @s', 'tag @s add bm.lgadv'])
    fn('p121/unadv', ['tag @s remove bm.lgadv', 'execute if function bm:p84/lk/inside run return run tag @s add bm.lkadv',
                      'execute if entity @s[gamemode=adventure] unless entity @s[tag=bm.gvp] run gamemode survival @s'])
    G.FUNCS['p84/lk/unadv'][0:0] = ['execute if function bm:p121/inside run return run function bm:p121/hall_to_lounge']
    fn('p121/hall_to_lounge', ['tag @s remove bm.lkadv', 'tag @s add bm.lgadv'])

    # ================================================================== in and out
    fn('p121/enter', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                      'execute store result storage bm:lg tmp.pid int 1 run scoreboard players get @s bm.pid',
                      'data modify storage bm:lg tmp.x set from entity @s Pos[0]', 'data modify storage bm:lg tmp.y set from entity @s Pos[1]',
                      'data modify storage bm:lg tmp.z set from entity @s Pos[2]', 'data modify storage bm:lg tmp.r set from entity @s Rotation[0]',
                      'data modify storage bm:lg tmp.d set from entity @s Dimension', 'function bm:p121/save with storage bm:lg tmp',
                      f'execute in bm:gutter unless data storage bm:lg {{built:{VER}}} run function bm:p121/build',
                      'execute if entity @s[gamemode=survival] run function bm:p121/adv',
                      f'execute in bm:gutter run tp @s {MX - 8:g} {MY} {MZ:g} -90 0',
                      'title @s times 5 40 10', title('@s', 'title', T("THE FIXER'S LOUNGE", LOUNGE, bold=True)),
                      title('@s', 'subtitle', T('the den, without a heist - no fee', 'gray')),
                      'playsound minecraft:block.iron_door.open player @s ~ ~ ~ 1 0.9'])
    fn('p121/save', ['$data modify storage bm:lg r.p$(pid) set value {x:$(x),y:$(y),z:$(z),r:$(r),d:"$(d)"}'])
    fast.append('execute in bm:gutter as @e[type=minecraft:marker,tag=bm.lgexit,distance=0..] at @s as @a[distance=..0.9,tag=!bm.gvp] at @s run function bm:p121/leave')
    fn('p121/leave', ['execute store result storage bm:lg tmp.pid int 1 run scoreboard players get @s bm.pid', 'function bm:p121/back with storage bm:lg tmp'])
    fn('p121/back', ['$execute unless data storage bm:lg r.p$(pid) run return run function bm:p84/lk/nowhere', '$function bm:p84/lk/back2 with storage bm:lg r.p$(pid)',
                     'function bm:p121/unadv', 'playsound minecraft:block.iron_door.close player @s ~ ~ ~ 1 0.9'])

    # ---- the Ledger: a button in the Office, the Locker Hall's 3-second hold from safe ground
    btn_hall = 'command:"/trigger bm.act set 7805"}}'
    lounge_btn = snbt(P28.btn([T('⌂ ', LOUNGE), T("The Fixer's Lounge", 'white', bold=True)], TRIP,
                              tooltip=T('The den without a heist: shops, the bank, the armory, your lockers - no fee. From safe ground: hold still for 3 seconds.'), width=150))
    n = 0
    for name, L in G.FUNCS.items():
        for i, l in enumerate(L):
            if l.startswith('$dialog show') and btn_hall in l and 'THE FIXER' in l and name != 'p104/office_dlg':      # (not the Office on a heist)
                L[i] = l.replace(btn_hall, btn_hall + ',' + lounge_btn); n += 1
    assert n >= 1, 'the Office dialog'
    G.FUNCS['p80/act'].insert(2, f'execute if score #act bm.pay matches {TRIP} run return run function bm:p121/from_ledger')
    fn('p121/from_ledger', ['execute if entity @s[tag=bm.gvp] run return run ' + say('You\'re on a heist - the den has all of this. (The lounge is for the days between.)'),
                            'execute if function bm:p121/inside run return run ' + say('You\'re in the lounge already.'),
                            'execute at @s run function bm:p121/lh/try'])
    # (a copy of the Locker Hall's trip - its checks, its hold - that ends in the lounge)
    names = [k for k in G.FUNCS if k.startswith('p103/lh/')]
    for k in names:
        L2 = []
        for l in G.FUNCS[k]:
            l = l.replace('function bm:p103/lh/', 'function bm:p121/lh/').replace('bm.lkch', 'bm.lgch').replace('function bm:p84/lk/enter', 'function bm:p121/enter')
            l = l.replace('the Locker Hall stays shut', 'the lounge stays shut').replace('Opening the Locker Hall', "Off to the Fixer's Lounge")
            l = l.replace("You're in the gutter already - the Locker Hall's door is the copper one in the den.", "You're in the gutter already - head home first.")
            L2.append(l)
        fn('p121/lh/' + k[len('p103/lh/'):], L2)
    assert 'p121/lh/go' in G.FUNCS and 'p121/enter' in ' '.join(G.FUNCS['p121/lh/go'])
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.lgch dummy']
    G.OBJECTIVES += ['bm.lgch']
    tick.append('execute as @a[tag=bm.lgch] at @s run function bm:p121/lh/step')

    # ================================================================== a heist ends: GO TO THE LOUNGE
    def add_after(fname, anchor_code, code, label, tip, col=LOUNGE):
        b = snbt(P28.btn([T(label, col, bold=True)], code, width=200, tooltip=T(tip, 'gray')))
        anchor = f'command:"/trigger bm.act set {anchor_code}"}}}}'
        L = G.FUNCS[fname]
        k = next(i for i, l in enumerate(L) if 'dialog show' in l and anchor in l)
        L[k] = L[k].replace(anchor, anchor + ',' + b)
    tip_in = 'The heist ends and you step into the Fixer\'s Lounge - shop, bank, lockers - no fee. Its door takes you home.'
    add_after('p101/ask_dlg', 7720, C_LEAD, 'Go to the Lounge', 'The heist ends and the crew steps into the Fixer\'s Lounge - shop, bank, lockers - no fee. Its door takes you home.')
    add_after('p103/mem_dlg', 7726, C_MEM, 'Go to the Lounge', tip_in)
    add_after('p103/offer_show', 7723, C_OUT, 'Go to the Lounge', tip_in)
    add_after('p101/offer', 7723, C_OUT, 'Go to the Lounge', tip_in)      # (2.76 fix: the card itself, not only its copy the Ledger reopens)
    G.FUNCS['p28/act'].insert(0, f'execute if score #act bm.pay matches {C_LEAD}..{C_OUT} run return run function bm:p121/act')
    fn('p121/act', [f'execute if score #act bm.pay matches {C_LEAD} run return run function bm:p121/lead',
                    f'execute if score #act bm.pay matches {C_MEM} run return run function bm:p121/mem',
                    f'execute if score #act bm.pay matches {C_OUT} run return run function bm:p121/out'])
    for new, old in (('p121/lead', 'p101/go_home'), ('p121/mem', 'p103/mem_home'), ('p121/out', 'p101/opt_out')):
        fn(new, [l.replace('function bm:p101/send_home', 'function bm:p121/send') for l in G.FUNCS[old]])
        assert any('p121/send' in l for l in G.FUNCS[new]), new
    # (2.78: to the Lounge your overworld gear stays at the coat check - the Lounge's door hands it back as it takes you home.
    #  It used to come back the moment the heist ended, in the Lounge, as if you'd gone home)
    fn('p121/send', ['tag @s add bm.lgbag', 'function bm:p101/send_home', 'function bm:p121/enter',
                     tellraw('@s', P + [T('Your own gear waits at the coat check - ', 'gray'), T('the Lounge\'s door hands it back', 'white'), T(' as it takes you home.', 'gray')])])
    ur = G.FUNCS['p70/unraid']
    k = ur.index('execute at @s run function bm:p72/bag/restore')
    ur[k] = 'execute unless entity @s[tag=bm.lgbag] at @s run function bm:p72/bag/restore'
    G.FUNCS['p121/back'] += ['execute if entity @s[tag=bm.lgbag] at @s run function bm:p72/bag/restore', 'tag @s remove bm.lgbag']
    G.FUNCS['p72/bag/check'].insert(0, 'tag @s remove bm.lgbag')      # (a heist from the Lounge: its own way home gives the gear back)

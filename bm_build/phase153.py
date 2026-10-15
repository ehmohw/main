"""Phase 153 (2.80): the last of the click-in-chat menus become dialogs.

- SERVER SETTINGS (ops: /function bm:admin/settings): a dialog - each setting shows its state on its own button, and a
  click flips it; the Blood Moon's period is a row of choices. (It was lines of [On] [Off] links in chat.)
- THE PARTY'S MEMBERS (the party menu's "Members"): a dialog listing everyone with their health, the leader starred; the
  leader gets a Kick button for each of the others. (Names are resolved first - a dialog won't resolve a selector.)

Left in chat on purpose: requests from another player (party invites, teleport requests) and the puzzle's "Stuck? Skip"
hint arrive unasked, and a dialog would snatch the screen mid-fight; the post-heist prompts already open a dialog and keep
a chat line only as a fallback; admin/help is a reference that fills the chat box (suggest, not run).

Importing does nothing; generate(G) runs late (after phase132 adds its setting)."""
from items import T
from nbt import Int, snbt
import phase28 as P28

GOLD = '#ffcf40'
SETTINGS = [('breaker', 'Block Breaker', 'Breaks blocks when powered.'),
            ('bombs', 'Skiff TNT bombs', "The skiff's bomb bay."),
            ('pvp', 'Magic hurts players', "Cecil's staffs, bows, the Tidal Tear..."),
            ('tulleo', 'Tullius needs Leo', "The ghost ship's captain only rises with Leo in the boarding crew.")]
PERIODS = (10, 20, 30, 45, 60)
MAX_PARTY = 6


def cmd_btn(label, command, tooltip=None, width=150):
    b = {'label': label, 'action': {'type': 'minecraft:run_command', 'command': command}, 'width': Int(width)}
    if tooltip: b['tooltip'] = tooltip
    return b


def generate(G):
    fn = G.fn

    # ================================================================== SERVER SETTINGS
    lines = ['data remove storage bm:ui cfg', 'execute store result storage bm:ui cfg.per int 1 run scoreboard players get #bmper bm.cfg']
    for key, nm, desc in SETTINGS:
        lines += [f'data modify storage bm:ui cfg.{key} set value "Off"', f'execute if score #{key} bm.cfg matches 1 run data modify storage bm:ui cfg.{key} set value "On"']
    lines += ['execute if score #bmoff bm.cfg matches 1 run return run function bm:admin/settings_dlg_off with storage bm:ui cfg',
              'function bm:admin/settings_dlg with storage bm:ui cfg']
    btns = ([cmd_btn([T('Blood Moon: ', 'gray'), T(f'{d} days', 'yellow')], f'/function bm:admin/set/bmper_{d}', T(f'A Blood Moon every {d} days', 'gray'), 100)
             for d in PERIODS] +
            [cmd_btn([T('Blood Moon: ', 'gray'), T('never', 'red')], '/function bm:admin/set/bmoff_1', T('No Blood Moon on its own', 'gray'), 100)] +
            [cmd_btn([T(f'{nm}: ', 'white'), T(f'$({key})', 'aqua', bold=True)], f'/function bm:admin/set/{key}_flip', T(desc, 'gray'), 150)
             for key, nm, desc in SETTINGS])
    for suffix, bm in (('', [T('every ', 'aqua'), T('$(per)', 'aqua', bold=True), T(' days', 'aqua')]), ('_off', [T('never on its own', 'red')])):
        dlg = P28.multi([T('SERVER SETTINGS', GOLD, bold=True), T('  ·  for operators', 'gray')],
                        [P28.body([T('Blood Moon: ', 'white')] + bm + [T('   (one can still be summoned)', 'dark_gray')], 320),
                         P28.body([T('Click a setting to switch it.', 'gray')], 320)], btns, columns=3)
        fn(f'admin/settings_dlg{suffix}', [f'$dialog show @s {P28.inline(dlg)}'])
    fn('admin/settings', lines)
    for key, nm, desc in SETTINGS:
        assert f'admin/set/{key}_1' in G.FUNCS, key
        fn(f'admin/set/{key}_flip', [f'execute if score #{key} bm.cfg matches 1 run return run function bm:admin/set/{key}_0', f'function bm:admin/set/{key}_1'])

    # ================================================================== THE PARTY'S MEMBERS
    # (the viewer first, so a leader's own row is slot 0 and the Kick buttons are slots 1+)
    fn('p67/members', ['execute unless score @s bm.pty matches 1.. run return run title @s actionbar ' + snbt(T("You aren't in a party. Invite someone from the menu.", 'gray')),
                       'scoreboard players operation #p bm.pty = @s bm.pty', 'data remove storage bm:ui pm', 'scoreboard players set #ps bm.rng 0',
                       'execute at @s run function bm:p67/mrow', 'tag @s add bm.pview',
                       'execute as @a[tag=!bm.pview] if score @s bm.pty = #p bm.pty at @s run function bm:p67/mrow',
                       'tag @s remove bm.pview'] +
       [f'execute if entity @s[tag=bm.pleader] if score #ps bm.rng matches {n} run return run function bm:p67/mdlg_l{n} with storage bm:ui pm' for n in range(1, MAX_PARTY + 1)] +
       [f'execute if score #ps bm.rng matches {n} run return run function bm:p67/mdlg_{n} with storage bm:ui pm' for n in range(1, MAX_PARTY + 1)])
    fn('p67/mrow', ['function bm:p28/name/of', 'execute store result score #k bm.rng run scoreboard players get @s bm.pid', 'scoreboard players add #k bm.rng 10000'] +
       sum(([f'execute if score #ps bm.rng matches {i} run data modify storage bm:ui pm.n{i} set from storage bm:tmp nm.name',
             f'execute if score #ps bm.rng matches {i} unless data storage bm:ui pm.n{i} run data modify storage bm:ui pm.n{i} set value "?"',
             f'execute if score #ps bm.rng matches {i} store result storage bm:ui pm.h{i} int 1 run scoreboard players get @s bm.hp',
             f'execute if score #ps bm.rng matches {i} store result storage bm:ui pm.k{i} int 1 run scoreboard players get #k bm.rng',
             f'execute if score #ps bm.rng matches {i} run data modify storage bm:ui pm.l{i} set value "   "',
             f'execute if score #ps bm.rng matches {i} if entity @s[tag=bm.pleader] run data modify storage bm:ui pm.l{i} set value "★ "']
            for i in range(MAX_PARTY)), []) +
       ['scoreboard players add #ps bm.rng 1'])
    for n in range(1, MAX_PARTY + 1):
        rows = sum(([T(f'$(l{i})', GOLD), T(f'$(n{i})', 'white', bold=(i == 0)), T('   ❤ ', 'red'), T(f'$(h{i})', 'white'), T('\n')] for i in range(n)), [])[:-1]
        back = cmd_btn(T('« Party', 'gray'), '/trigger bm.party set 1', width=150)
        title = [T('YOUR PARTY', '#ffd25a', bold=True), T(f'  ·  {n} of {MAX_PARTY}', 'gray')]
        body = [P28.body(rows, 260), P28.body([T('★ leads. Party members can\'t hurt each other and see each other\'s health.', 'dark_gray')], 260)]
        fn(f'p67/mdlg_{n}', [f'$dialog show @s {P28.inline(P28.multi(title, body, [back], columns=1))}'])
        kicks = [cmd_btn([T('Kick ', 'red'), T(f'$(n{i})', 'white')], f'/trigger bm.party set $(k{i})', T('Out of the party', 'gray'), 150) for i in range(1, n)]
        fn(f'p67/mdlg_l{n}', [f'$dialog show @s {P28.inline(P28.multi(title, body, kicks + [back], columns=2))}'])
    G.FUNCS['p67/kick'].append('function bm:p67/members')          # (the list again, one fewer)
    G.FUNCS.pop('p67/member', None)
    G.FUNCS.pop('p67/member_kick', None)

"""2.58: playing together - parties, and bosses that grow with the crowd.

PARTIES (up to 6). Open the party menu with your Quick Actions key (the game's own "quick actions" dialog list),
or type /trigger bm.party:
- Invite players near me (10 blocks): they get an [Accept] / [Decline] message (it lapses after a minute).
- Party members can't hurt each other, wear the party's colour on their names, chat privately with /teammsg, and see
  everyone's health in a party list on the side of the screen. Members: the list in chat (health, distance) and, for
  the leader, [Kick] buttons. Leave any time; the leadership passes on, and a party of one dissolves.
(Party colour = the party's team. Someone on a special team - the Crimson set's necromancer team, Wilfrey's pack - keeps
it; they are still in the party, just without the team perks while they wear it.)

BOSS SCALING. Every boss checks every 5 seconds how many players are within 40 blocks (creative and spectators don't
count): each player past the first adds 50% to its health and 10% to its melee damage (up to 6 players: x3.5 health,
+50% damage). Its health keeps the same fraction as it grows or shrinks, and its boss bar follows. Bosses: the seven
dungeon bosses (Hollow King and the Lucky Den's included), the Blood Moon Monstrosity, the Headless Horseman, the
Vorn Warlord / Abductor / Overseer, the Sand Pharaoh, the Storm Roc, the Elder Treant, the Magma Colossus and the
Voidwalker."""
from items import T
from nbt import snbt

GOLD = '#ffd25a'
MAX_PARTY = 6
COLORS = ['aqua', 'green', 'gold', 'light_purple', 'yellow', 'red', 'blue', 'dark_aqua', 'dark_green', 'dark_purple', 'dark_red', 'dark_blue', 'white', 'gray',
          'dark_gray']
BOSSES = [  # entity tag, its boss bar
    *[(f'bm.boss_{d}', f'bm:boss_{d}') for d in ('brood', 'frost', 'tide', 'hex', 'keep', 'hollow', 'lucky')],
    ('bm.monstrosity', 'bm:monst'), ('bm.hhm', 'bm:hhm'), ('bm.vb_warlord', 'bm:warlord'), ('bm.vb_abductor', 'bm:abductor'),
    ('bm.vb_overseer', 'bm:overseer'), ('bm.sph', 'bm:sph'), ('bm.roc', 'bm:roc'), ('bm.trt', 'bm:trt'), ('bm.mcol', 'bm:mcol'), ('bm.vwk', 'bm:vwk')]


def generate(G):
    fn, wjson, title, tellraw, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    P = [T('[Party] ', GOLD, bold=True)]
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.party trigger', 'scoreboard objectives add bm.pty dummy', 'scoreboard objectives add bm.pinv dummy',
                              'scoreboard objectives add bm.pinvt dummy', 'scoreboard objectives add bm.hp health', 'scoreboard objectives add bm.bsn dummy',
                              'scoreboard objectives add bm.pcol dummy', 'scoreboard players set #15 bm.rng 15', 'scoreboard players set #1000 bm.rng 1000']
    G.OBJECTIVES += ['bm.party', 'bm.pty', 'bm.pinv', 'bm.pinvt', 'bm.hp', 'bm.bsn', 'bm.pcol']
    tick, second = [], []

    # ================================================================== BOSS SCALING
    second += ['scoreboard players add #bsc bm.bm 1', 'execute if score #bsc bm.bm matches 5.. run function bm:p67/scale_all']
    fn('p67/scale_all', ['scoreboard players set #bsc bm.bm 0'] +
       [f'execute as @e[tag={t},tag=!bm.dead] at @s run function bm:p67/scale' for t, _b in BOSSES])
    # (as the boss) how many fighters now? if that changed: re-scale, keeping its health fraction
    fn('p67/scale', ['execute store result score #n bm.rng if entity @a[distance=..40,gamemode=!spectator,gamemode=!creative]',
                     'execute if score #n bm.rng matches ..0 run return 0', 'execute if score #n bm.rng matches 7.. run scoreboard players set #n bm.rng 6',
                     'execute unless score @s bm.bsn matches 1.. run scoreboard players set @s bm.bsn 1',
                     'execute if score #n bm.rng = @s bm.bsn run return 0',
                     'execute store result score #h bm.rng run data get entity @s Health',
                     'execute store result score #mx bm.rng run attribute @s minecraft:max_health get',
                     'execute if score #mx bm.rng matches ..0 run return 0',
                     'scoreboard players operation #fr bm.rng = #h bm.rng', 'scoreboard players operation #fr bm.rng *= #1000 bm.rng',
                     'scoreboard players operation #fr bm.rng /= #mx bm.rng',
                     'execute if score #n bm.rng > @s bm.bsn run tag @s add bm.bsup', 'scoreboard players operation @s bm.bsn = #n bm.rng',
                     'attribute @s minecraft:max_health modifier remove bm:party_scale', 'attribute @s minecraft:attack_damage modifier remove bm:party_dmg'] +
       [f'execute if score #n bm.rng matches {n} run attribute @s minecraft:max_health modifier add bm:party_scale {0.5 * (n - 1):.1f} add_multiplied_base' for n in range(2, 7)] +
       [f'execute if score #n bm.rng matches {n} run attribute @s minecraft:attack_damage modifier add bm:party_dmg {0.1 * (n - 1):.1f} add_multiplied_base' for n in range(2, 7)] +
       ['execute store result score #mx bm.rng run attribute @s minecraft:max_health get',
        'scoreboard players operation #h bm.rng = #mx bm.rng', 'scoreboard players operation #h bm.rng *= #fr bm.rng', 'scoreboard players operation #h bm.rng /= #1000 bm.rng',
        'execute if score #h bm.rng matches ..0 run scoreboard players set #h bm.rng 1',
        'execute store result entity @s Health float 1 run scoreboard players get #h bm.rng'] +
       [f'execute if entity @s[tag={t}] store result bossbar {b} max run scoreboard players get #mx bm.rng' for t, b in BOSSES] +
       ['execute if entity @s[tag=bm.bsup] run function bm:p67/scale_up', 'tag @s remove bm.bsup'])
    fn('p67/scale_up', ['execute as @a[distance=..40] run ' + title('@s', 'actionbar', [{'selector': '@e[tag=bm.bsup,limit=1]'}, T(' grows stronger: ', 'red'),
                                                                                      {'score': {'name': '#n', 'objective': 'bm.rng'}, 'color': 'white'}, T(' of you face it.', 'red')]),
                        'playsound minecraft:entity.wither.ambient hostile @a[distance=..40] ~ ~ ~ 0.5 1.4'])

    # ================================================================== PARTIES
    tick += ['scoreboard players enable @a bm.party', 'execute as @a[scores={bm.party=1..}] at @s run function bm:p67/act',
             'scoreboard players set @a[scores={bm.party=..-1}] bm.party 0']
    dlg = {'type': 'minecraft:multi_action', 'title': T('Party', GOLD, bold=True),
           'body': [{'type': 'minecraft:plain_message', 'width': 260, 'contents': T('Up to 6. Party members can\'t hurt each other, share a colour, see each other\'s health on the side of the screen, and chat with /teammsg. Bosses grow tougher with every player near them.', 'gray')}],
           'actions': [{'label': T('Invite players near me', 'green'), 'tooltip': T('Everyone within 10 blocks who isn\'t in a party', 'gray'),
                        'action': {'type': 'minecraft:run_command', 'command': '/trigger bm.party set 2'}},
                       {'label': T('Members', 'aqua'), 'action': {'type': 'minecraft:run_command', 'command': '/trigger bm.party set 6'}},
                       {'label': T('Accept invite', 'yellow'), 'action': {'type': 'minecraft:run_command', 'command': '/trigger bm.party set 4'}},
                       {'label': T('Leave party', 'red'), 'action': {'type': 'minecraft:run_command', 'command': '/trigger bm.party set 3'}}],
           'columns': 2, 'exit_action': {'label': T('Close')}, 'pause': False, 'after_action': 'close'}
    wjson('bm/dialog/party.json', dlg)
    wjson('minecraft/tags/dialog/quick_actions.json', {'replace': False, 'values': ['bm:party']})
    fn('p67/act', ['scoreboard players operation #pa bm.rng = @s bm.party', 'scoreboard players set @s bm.party 0',
                   'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                   'execute if score #pa bm.rng matches 1 run return run dialog show @s bm:party',
                   'execute if score #pa bm.rng matches 2 run return run function bm:p67/invite',
                   'execute if score #pa bm.rng matches 3 run return run function bm:p67/leave',
                   'execute if score #pa bm.rng matches 4 run return run function bm:p67/accept',
                   'execute if score #pa bm.rng matches 5 run return run function bm:p67/decline',
                   'execute if score #pa bm.rng matches 6 run return run function bm:p67/members',
                   'execute if score #pa bm.rng matches 10000.. run return run function bm:p67/kick'])
    # ---- forming: inviting with no party makes one (you lead); the party's id is your player id
    fn('p67/invite', ['execute unless score @s bm.pty matches 1.. run function bm:p67/form',
                      'scoreboard players operation #p bm.pty = @s bm.pty', 'function bm:p67/count',
                      f'execute if score #pc bm.rng matches {MAX_PARTY}.. run return run ' + say(f'Your party is full ({MAX_PARTY}).', 'red'),
                      'scoreboard players set #inv bm.rng 0', 'tag @s add bm.pinviter',
                      'execute as @a[distance=0.1..10,gamemode=!spectator] unless score @s bm.pty matches 1.. at @s run function bm:p67/invite1',
                      'tag @s remove bm.pinviter',
                      'execute if score #inv bm.rng matches 0 run return run ' + say('Nobody near you to invite (they must be within 10 blocks and not in a party).'),
                      tellraw('@s', P + [T('Invited ', 'gray'), {'score': {'name': '#inv', 'objective': 'bm.rng'}, 'color': 'white'}, T(' player(s).', 'gray')])])
    fn('p67/invite1', ['scoreboard players add #inv bm.rng 1', 'scoreboard players operation @s bm.pinv = #p bm.pty', 'scoreboard players set @s bm.pinvt 60',
                       tellraw('@s', P + [{'selector': '@a[tag=bm.pinviter,limit=1]', 'color': 'white'}, T(' invites you to their party. ', 'gray'),
                                          {'text': '[Accept]', 'color': 'green', 'bold': True, 'click_event': {'action': 'run_command', 'command': '/trigger bm.party set 4'},
                                           'hover_event': {'action': 'show_text', 'value': T('Join the party', 'gray')}},
                                          T(' '), {'text': '[Decline]', 'color': 'red', 'click_event': {'action': 'run_command', 'command': '/trigger bm.party set 5'}}]),
                       'playsound minecraft:block.note_block.chime player @s ~ ~ ~ 1 1.4'])
    second += ['scoreboard players remove @a[scores={bm.pinvt=1..}] bm.pinvt 1', 'scoreboard players reset @a[scores={bm.pinvt=0}] bm.pinv',
               'scoreboard players reset @a[scores={bm.pinvt=0}] bm.pinvt']
    fn('p67/form', ['scoreboard players operation @s bm.pty = @s bm.pid', 'tag @s add bm.pleader',
                    'scoreboard players operation #c bm.rng = @s bm.pid', 'scoreboard players operation #c bm.rng %= #15 bm.rng',
                    'scoreboard players operation @s bm.pcol = #c bm.rng',
                    'execute store result storage bm:tmp pty.id int 1 run scoreboard players get @s bm.pty', 'function bm:p67/make with storage bm:tmp pty',
                    tellraw('@s', P + [T('You formed a party. Invite more from the menu (Quick Actions, or /trigger bm.party).', 'gray')])])
    # the party's team (colour, no friendly fire, see invisible friends) and its health list
    fn('p67/make', ['$team add bm.p$(id)', '$team modify bm.p$(id) friendlyFire false', '$team modify bm.p$(id) seeFriendlyInvisibles true',
                    '$scoreboard objectives add bm.ph$(id) dummy {text:"Party",color:"gold",bold:true}',
                    'function bm:p67/join_team'])
    fn('p67/join_team', ['execute store result storage bm:tmp pty.id int 1 run scoreboard players get @s bm.pty',
                         'execute store result score #c bm.rng run scoreboard players get @s bm.pty', 'scoreboard players operation #c bm.rng %= #15 bm.rng'] +
       [f'execute if score #c bm.rng matches {i} run data modify storage bm:tmp pty.col set value "{c}"' for i, c in enumerate(COLORS)] +
       ['function bm:p67/join_team1 with storage bm:tmp pty'])
    fn('p67/join_team1', ['$team modify bm.p$(id) color $(col)', '$execute if entity @s[team=] run team join bm.p$(id) @s',
                          '$execute if entity @s[team=bm.p$(id)] run scoreboard objectives setdisplay sidebar.team.$(col) bm.ph$(id)'])
    fn('p67/accept', ['execute unless score @s bm.pinv matches 1.. run return run ' + say('You have no party invite (or it lapsed).'),
                      'execute if score @s bm.pty matches 1.. run function bm:p67/leave',
                      'scoreboard players operation #p bm.pty = @s bm.pinv', 'function bm:p67/count',
                      'execute if score #pc bm.rng matches 0 run scoreboard players reset @s bm.pinv',
                      'execute if score #pc bm.rng matches 0 run return run ' + say('That party has broken up.'),
                      f'execute if score #pc bm.rng matches {MAX_PARTY}.. run return run ' + say('That party is full.', 'red'),
                      'scoreboard players operation @s bm.pty = @s bm.pinv', 'scoreboard players reset @s bm.pinv', 'scoreboard players reset @s bm.pinvt',
                      'function bm:p67/join_team', 'tag @s add bm.pnew',
                      'execute as @a if score @s bm.pty = #p bm.pty run ' + tellraw('@s', P + [{'selector': '@a[tag=bm.pnew,limit=1]', 'color': 'white'}, T(' joined the party.', 'gray')]),
                      'execute as @a if score @s bm.pty = #p bm.pty at @s run playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.5 1.6', 'tag @s remove bm.pnew'])
    fn('p67/decline', ['execute unless score @s bm.pinv matches 1.. run return 0', 'scoreboard players reset @s bm.pinv', 'scoreboard players reset @s bm.pinvt',
                       say('Invite declined.')])
    fn('p67/count', ['scoreboard players set #pc bm.rng 0', 'execute as @a if score @s bm.pty = #p bm.pty run scoreboard players add #pc bm.rng 1'])
    # ---- leaving: the team goes; a new leader if needed; a party of one dissolves
    fn('p67/leave', ['execute unless score @s bm.pty matches 1.. run return run ' + say("You aren't in a party."),
                     'scoreboard players operation #p bm.pty = @s bm.pty', 'tag @s add bm.pgone',
                     'execute store result storage bm:tmp pty.id int 1 run scoreboard players get @s bm.pty', 'function bm:p67/leave_team with storage bm:tmp pty',
                     'scoreboard players reset @s bm.pty', 'execute if entity @s[tag=bm.pleader] run tag @s add bm.pwasl', 'tag @s remove bm.pleader',
                     'execute as @a if score @s bm.pty = #p bm.pty run ' + tellraw('@s', P + [{'selector': '@a[tag=bm.pgone,limit=1]', 'color': 'white'}, T(' left the party.', 'gray')]),
                     say('You left the party.'),
                     'function bm:p67/count',
                     'execute if entity @s[tag=bm.pwasl] if score #pc bm.rng matches 1.. as @a if score @s bm.pty = #p bm.pty run tag @s add bm.pcand',
                     'execute if entity @s[tag=bm.pwasl] if score #pc bm.rng matches 1.. run function bm:p67/new_leader',
                     'execute if score #pc bm.rng matches 1 as @a if score @s bm.pty = #p bm.pty run function bm:p67/dissolve',
                     'tag @s remove bm.pgone', 'tag @s remove bm.pwasl'])
    fn('p67/leave_team', ['$execute if entity @s[team=bm.p$(id)] run team leave @s', '$scoreboard players reset @s bm.ph$(id)'])
    fn('p67/new_leader', ['tag @a[tag=bm.pcand,limit=1,sort=random] add bm.pleader', 'tag @a remove bm.pcand',
                          'execute as @a[tag=bm.pleader] if score @s bm.pty = #p bm.pty run ' + tellraw('@a[tag=bm.pleader,limit=1]', P + [T('You lead the party now.', 'gray')])])
    fn('p67/dissolve', ['execute store result storage bm:tmp pty.id int 1 run scoreboard players get @s bm.pty', 'function bm:p67/leave_team with storage bm:tmp pty',
                        'function bm:p67/drop with storage bm:tmp pty', 'scoreboard players reset @s bm.pty', 'tag @s remove bm.pleader',
                        tellraw('@s', P + [T('Your party has dissolved.', 'gray')])])
    fn('p67/drop', ['$team remove bm.p$(id)', '$scoreboard objectives remove bm.ph$(id)'])
    # ---- the member list (and [Kick] for the leader)
    fn('p67/members', ['execute unless score @s bm.pty matches 1.. run return run ' + say("You aren't in a party. Invite someone from the menu."),
                       'scoreboard players operation #p bm.pty = @s bm.pty', 'tag @s add bm.pview', tellraw('@s', P + [T('Members:', 'gray')]),
                       'execute as @a if score @s bm.pty = #p bm.pty at @s run function bm:p67/member', 'tag @s remove bm.pview'])
    fn('p67/member', ['execute store result score #k bm.rng run scoreboard players get @s bm.pid', 'scoreboard players add #k bm.rng 10000',
                      'execute store result storage bm:tmp pm.k int 1 run scoreboard players get #k bm.rng',
                      'execute if entity @s[tag=bm.pleader] run return run ' + tellraw('@a[tag=bm.pview]', [T('  ★ ', GOLD), {'selector': '@s', 'color': 'white'},
                                                                                                         T('  ❤ ', 'red'), {'score': {'name': '@s', 'objective': 'bm.hp'}, 'color': 'white'}]),
                      'execute unless entity @a[tag=bm.pview,tag=bm.pleader] run return run ' + tellraw('@a[tag=bm.pview]', [T('  '), {'selector': '@s', 'color': 'white'},
                                                                                                                      T('  ❤ ', 'red'), {'score': {'name': '@s', 'objective': 'bm.hp'}, 'color': 'white'}]),
                      'function bm:p67/member_kick with storage bm:tmp pm'])
    # (kick codes: 10000 + the member's player id)
    fn('p67/member_kick', ['$tellraw @a[tag=bm.pview] [{text:"  "},{selector:"@s",color:"white"},{text:"  ❤ ",color:"red"},{score:{name:"@s",objective:"bm.hp"},color:"white"},'
                           '{text:"  [Kick]",color:"red",click_event:{action:"run_command",command:"/trigger bm.party set $(k)"}}]'])
    fn('p67/kick', ['execute unless entity @s[tag=bm.pleader] run return run ' + say('Only the party leader can kick.'),
                    'scoreboard players operation #kid bm.rng = #pa bm.rng', 'scoreboard players remove #kid bm.rng 10000',
                    'scoreboard players operation #p bm.pty = @s bm.pty',
                    'execute as @a if score @s bm.pid = #kid bm.rng if score @s bm.pty = #p bm.pty unless entity @s[tag=bm.pleader] run function bm:p67/kicked'])
    fn('p67/kicked', [tellraw('@s', P + [T('You were removed from the party.', 'gray')]), 'function bm:p67/leave'])
    # ---- every second: the health list, the team (re-joined after a special team lets go), stragglers whose party is gone
    second.append('execute as @a[scores={bm.pty=1..}] run function bm:p67/sync')
    fn('p67/sync', ['execute store result storage bm:tmp pty.id int 1 run scoreboard players get @s bm.pty', 'function bm:p67/sync1 with storage bm:tmp pty'])
    fn('p67/sync1', ['$scoreboard players operation @s bm.ph$(id) = @s bm.hp', '$execute if entity @s[team=] run team join bm.p$(id) @s'])

    G.FUNCS['tick'] += tick
    s = G.FUNCS['loop/second']
    s[-1:-1] = second

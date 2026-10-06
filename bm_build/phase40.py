"""Phase 1.26 / 2.19: the Bounty Board.

Every Black Market has a BOUNTY BOARD on the balcony beside the Newcomers' lectern. On special nights it posts a bounty;
right-click the board to sign it (one per player per night). Bounties expire at dawn.
- BLOOD MOON: slay 8 Blood Moon horrors -> 10 Blood Crystals and a Medallion.
- LUCKY NIGHT: defeat 6 Lucky monsters -> 3 Lucky Tokens and a Jackpot Scratch Card.
- INVASION NIGHT: down 8 Vorn invaders or bioengineered monsters -> 6 Tokens, 4 Green Xenite, and a 10% chance of a
  Vorn Skiff part."""
from items import T
from nbt import snbt, B, F, Int

BOARD = (36.5, 18, 81.5)          # market template: the balcony, against the wall beside the lectern (34, 18, 80)
# state: (kind, colour, title, task, target, kill tags, reward text)
BOUNTIES = {1: ('blood', '#ff3b3b', 'BLOOD MOON BOUNTY', 'Slay 8 Blood Moon horrors', 8, ['bm.blood'], '10 Blood Crystals + a Medallion'),
            2: ('lucky', '#ffd23f', 'LUCKY NIGHT BOUNTY', 'Defeat 6 Lucky monsters', 6, ['bm.lucky'], '3 Lucky Tokens + a Jackpot Card'),
            3: ('invasion', '#7dff6a', 'INVASION BOUNTY', 'Down 8 Vorn invaders', 8, ['bm.vorn', 'bm.bio'], '6 Tokens + 4 Green Xenite (+ a rare skiff part?)')}
ident = [F(0), F(0), F(0), F(1)]


def generate(G):
    fn, wjson, title, give, tellraw, PREFIX = G.fn, G.wjson, G.title, G.give, G.tellraw, G.PREFIX
    import mgeo
    from phase35 import PARTS
    objs = ['bm.bnt dummy', 'bm.bntk dummy', 'bm.bntn dummy', 'bm.bst dummy']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o}' for o in objs]
    G.OBJECTIVES += [o.split()[0] for o in objs]
    say = lambda parts: title('@s', 'actionbar', parts)
    second = []

    # ------------------------------------------------------------------ tonight's bounty (blood moon > invasion > lucky night)
    second += ['scoreboard players operation #bprev bm.rng = #bstate bm.rng', 'scoreboard players set #bstate bm.rng 0',
               'execute if score #lnight bm.bm matches 1 run scoreboard players set #bstate bm.rng 2',
               'execute if score #inv bm.bm matches 1 run scoreboard players set #bstate bm.rng 3',
               'execute if score #active bm.bm matches 1 run scoreboard players set #bstate bm.rng 1',
               'execute if score #bstate bm.rng matches 1.. unless score #bprev bm.rng matches 1.. run function bm:p40/night_start',
               'execute if score #bstate bm.rng matches 0 if score #bprev bm.rng matches 1.. run function bm:p40/dawn']
    fn('p40/night_start', ['scoreboard players add #bnight bm.rng 1',
                           'execute as @a run ' + tellraw('@s', PREFIX + [T('A new bounty is posted on the Black Market\'s Bounty Board.', 'gold')])])
    fn('p40/dawn', ['execute as @a[scores={bm.bnt=1..}] run ' + tellraw('@s', PREFIX + [T('Your bounty expired at dawn.', 'gray')]),
                    'scoreboard players set @a bm.bnt 0'])

    # ------------------------------------------------------------------ the board (placed in every market by the p35 patch)
    mgeo.need_floor(BOARD, 'public', 'the bounty board')
    board_text = {'Tags': ['bm.bboard', 'bm.npc'], 'billboard': 'vertical', 'see_through': B(0), 'shadow': B(1), 'background': Int(0xB0201810 - 0x100000000),
                  'brightness': {'block': Int(15), 'sky': Int(15)}, 'line_width': Int(220), 'alignment': 'center',
                  'text': T('BOUNTY BOARD', '#ffd23f', bold=True),
                  'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0), F(0)], 'scale': [F(0.7)] * 3}}
    board_hit = {'Tags': ['bm.bbhit', 'bm.npc'], 'width': F(1.0), 'height': F(2.4), 'response': B(1)}
    tpos, hpos = mgeo.rel((BOARD[0], BOARD[1] + 0.75, BOARD[2] + 0.22)), mgeo.rel(BOARD)     # 2.23: pinned to the board (phase44 builds it)
    G.FUNCS['p35/patch'] += [
        f'execute positioned {tpos} unless entity @e[type=minecraft:text_display,tag=bm.bboard,distance=..1.5] run summon minecraft:text_display ~ ~ ~ {snbt(board_text)}',
        f'execute positioned {hpos} unless entity @e[type=minecraft:interaction,tag=bm.bbhit,distance=..1.5] run summon minecraft:interaction ~ ~ ~ {snbt(board_hit)}']
    texts = {0: [T('BOUNTY BOARD\n', '#ffd23f', bold=True), T('No bounties tonight.\n', 'gray'),
                 T('Come back on a Blood Moon,\na Lucky Night or an Invasion Night.', 'dark_gray')]}
    for st, (k, col, head, task, n, _, reward) in BOUNTIES.items():
        texts[st] = [T(head + '\n', col, bold=True), T(task + ' before dawn.\n', 'white'), T('Reward: ' + reward + '\n', 'gold'),
                     T('Right-click to sign.', 'gray', italic=True)]
    second.append('execute as @e[type=minecraft:text_display,tag=bm.bboard] unless score @s bm.bst = #bstate bm.rng run function bm:p40/board_text')
    fn('p40/board_text', ['scoreboard players operation @s bm.bst = #bstate bm.rng'] +
       [f'execute if score #bstate bm.rng matches {st} run data modify entity @s text set value {snbt({"text": "", "extra": parts})}' for st, parts in texts.items()])
    G.FUNCS['tick'].append('execute as @e[type=minecraft:interaction,tag=bm.bbhit] if data entity @s interaction at @s run function bm:p40/board_click')
    fn('p40/board_click', ['execute on target run function bm:p40/sign', 'data remove entity @s interaction'])
    fn('p40/sign', ['execute if score #bstate bm.rng matches 0 run return run ' + say(T('No bounties tonight - come back on a special night.', 'gray')),
                    'execute if score @s bm.bnt matches 1.. run return run ' + say(T('You already carry tonight\'s bounty.', 'gray')),
                    'execute if score @s bm.bntn = #bnight bm.rng run return run ' + say(T('You\'ve already taken tonight\'s bounty.', 'gray')),
                    'execute if entity @s[tag=bm.bty] run return run ' + say(T('You already carry a Blood Bounty - one bounty a night.', 'gray')),
                    'scoreboard players operation @s bm.bnt = #bstate bm.rng', 'scoreboard players set @s bm.bntk 0',
                    'scoreboard players operation @s bm.bntn = #bnight bm.rng',
                    'playsound minecraft:item.book.put player @s ~ ~ ~ 1 0.7'] +
       [f'execute if score @s bm.bnt matches {st} run ' + say([T('Bounty signed: ', col), T(task + ' before dawn.', 'white')])
        for st, (k, col, head, task, n, _, _) in BOUNTIES.items()])

    # ------------------------------------------------------------------ kills and rewards
    for st, (k, col, head, task, n, tags, reward) in BOUNTIES.items():
        for i, tg in enumerate(tags):
            wjson(f'bm/advancement/p40/kill_{k}_{i}.json', {
                'criteria': {'slain': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [
                    {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["%s"]}' % tg}}]}}},
                'rewards': {'function': f'bm:p40/kill_{k}_{i}'}})
            fn(f'p40/kill_{k}_{i}', [f'advancement revoke @s only bm:p40/kill_{k}_{i}', f'execute if score @s bm.bnt matches {st} run function bm:p40/count_{k}'])
        fn(f'p40/count_{k}', ['scoreboard players add @s bm.bntk 1', f'execute if score @s bm.bntk matches {n}.. run return run function bm:p40/done_{k}',
                              say([T('Bounty: ', col), {'score': {'name': '@s', 'objective': 'bm.bntk'}, 'color': 'white'}, T(f' / {n}', 'gray')])])
    rewards = {'blood': [give('blood_crystal', 10), give('medallion')],
               'lucky': [give('lucky_token', 3), give('jackpot_card_5')],
               'invasion': [give('token', 6), give('xenite_green', 4), 'execute store result score #r bm.rng run random value 1..10',
                            'execute if score #r bm.rng matches 1 run function bm:p40/part']}
    for st, (k, col, head, task, n, _, reward) in BOUNTIES.items():
        fn(f'p40/done_{k}', ['scoreboard players set @s bm.bnt 0'] + rewards[k] +
           ['title @s times 10 50 20', title('@s', 'subtitle', T('Reward: ' + reward.replace(' (+ a rare skiff part?)', ''), 'gold')),
            title('@s', 'title', T('BOUNTY COMPLETE', col, bold=True)), 'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1 0.8',
            tellraw('@a', PREFIX + [{'selector': '@s', 'color': 'yellow'}, T(' completed the ', 'gray'), T(head.title(), col), T('!', 'gray')])])
    fn('p40/part', ['execute store result score #p bm.rng run random value 1..%d' % len(PARTS)] +
       [f'execute if score #p bm.rng matches {i + 1} run ' + give(p) for i, (p, _, _) in enumerate(PARTS)] +
       [tellraw('@s', PREFIX + [T('...and a Vorn Skiff part was pinned to the bounty!', '#7dff6a')])])
    G.FUNCS['admin/help'] += [tellraw('@s', [T('/function bm:admin/bounty_test', 'yellow'), T('  signs you up for tonight\'s bounty from anywhere', 'gray')])]
    fn('admin/bounty_test', ['function bm:p40/sign'])

    s = G.FUNCS['loop/second']
    s[-1:-1] = second

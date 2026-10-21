"""2.85c: THE RAT RACE (the owner's "Goal Day") - a day's job for the whole server, raced against the sunset.

THE STARTER'S PISTOL (Goldtooth, in the heist den and the Lounge: 2 Gutter Medallions)   fire it in the Overworld, between
               dawn and mid-afternoon (0-8999), and the Rat Race is on: one job for everyone, drawn from the list below,
               to be done before sunset (12000). One race a day; not while one is running.
THE JOB        scales with the players online - the most seen during the race (the target only ever grows):
                 mine iron ore, gold ore, copper ore, diamond ore, nether quartz; chop acacia logs; dig sand; quarry obsidian;
                 slay blazes, endermen, wither skeletons, guardians; catch fish; breed animals; trade with villagers.
               Mined blocks count only once: every one of them set back down is taken off again (placing ore you carried
               in, then mining it, nets nothing) - so it has to be the world's own. Everyone's work counts, wherever they
               are; a gold bar at the top of the screen shows the job and the count.
NO PENALTY     if the sun sets first, the race is simply lost.
THE PRIZE      if it's done, everyone online wins: 3-6 Tokens each, and a draw - Medallions, a Trophy, a LUCKY MAP
               FRAGMENT (one you don't carry yet), a LUCKY HORSESHOE (new: hang it up and tonight is a Lucky Night), a
               Crimson Effigy (a Blood Moon tonight), Pearlman's Bell, a Vorn Fleet Beacon (once the fleet has noticed the
               world) or three Lucky Scratch Cards.
"""
from items import item, T, TOTEM, consumable
import phase70 as P70

GOLD, CHEESE, DIM = '#ffd24a', '#ffe58a', '#b89a4a'
LUCKY = '#5ad86a'
holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
PRICE = ('gutter_medallion', 2)
LAST_START = 8999                      # (the latest hour the pistol can start one: a sunset at 12000)
SUNSET = 12000

# (kind, the job as shown, criteria that count, criteria taken off again, base target, more for each extra player)
def mined(*b):
    return [f'minecraft.mined:minecraft.{x}' for x in b]


def placed(*b):
    return [f'minecraft.used:minecraft.{x}' for x in b]


def killed(x):
    return [f'minecraft.killed:minecraft.{x}']


JOBS = [
    ('iron', 'Mine %s iron ore', mined('iron_ore', 'deepslate_iron_ore'), placed('iron_ore', 'deepslate_iron_ore'), 30, 15),
    ('gold', 'Mine %s gold ore', mined('gold_ore', 'deepslate_gold_ore', 'nether_gold_ore'),
     placed('gold_ore', 'deepslate_gold_ore', 'nether_gold_ore'), 24, 12),
    ('copper', 'Mine %s copper ore', mined('copper_ore', 'deepslate_copper_ore'), placed('copper_ore', 'deepslate_copper_ore'), 48, 24),
    ('diamond', 'Mine %s diamond ore', mined('diamond_ore', 'deepslate_diamond_ore'), placed('diamond_ore', 'deepslate_diamond_ore'), 8, 4),
    ('quartz', 'Mine %s nether quartz ore', mined('nether_quartz_ore'), placed('nether_quartz_ore'), 64, 32),
    ('acacia', 'Chop %s acacia logs', mined('acacia_log'), placed('acacia_log'), 192, 64),
    ('sand', 'Dig %s sand', mined('sand'), placed('sand'), 320, 128),
    ('obsidian', 'Quarry %s obsidian', mined('obsidian'), placed('obsidian'), 32, 16),
    ('blaze', 'Slay %s blazes', killed('blaze'), [], 10, 5),
    ('enderman', 'Slay %s endermen', killed('enderman'), [], 12, 6),
    ('wskel', 'Slay %s wither skeletons', killed('wither_skeleton'), [], 8, 4),
    ('guardian', 'Slay %s guardians', killed('guardian'), [], 10, 5),
    ('fish', 'Catch %s fish', ['minecraft.custom:minecraft.fish_caught'], [], 24, 10),
    ('breed', 'Breed %s pairs of animals', ['minecraft.custom:minecraft.animals_bred'], [], 20, 10),
    ('trade', 'Trade %s times with villagers', ['minecraft.custom:minecraft.traded_with_villager'], [], 20, 10),
]
CRIT = sorted({c for j in JOBS for c in j[2] + j[3]})
OBJ = {c: f'bm.rr{i}' for i, c in enumerate(CRIT)}

# ================================================================== THE ITEMS
item('rat_race_pistol', TOTEM, "Starter's Pistol", GOLD,
     ['Loaded with blanks and a promise.', ('Fire it (use) in the Overworld before', 'blue'), ('mid-afternoon: the Rat Race is on -', 'blue'),
      ('one job for everyone, done by sunset.', 'blue'), ('Win, and everyone online gets a prize.', 'gray'), ('One race a day. From Goldtooth.', 'dark_gray')],
     model='bm:rat_race_pistol', stack=16, cat='magic',
     comps={'minecraft:consumable': consumable(0.8, 'bow', 'minecraft:entity.firework_rocket.blast', False)})
item('lucky_horseshoe', TOTEM, 'Lucky Horseshoe', LUCKY,
     ['Still warm from the hoof. Points up, of course.', ('Hang it up (use, 1.5 s): tonight is', 'blue'), ('a Lucky Night.', 'blue'),
      ('Not on a Blood Moon day, a Dread Night,', 'gray'), ('or when tonight is already lucky.', 'gray')],
     model='bm:lucky_horseshoe', stack=16, cat='magic',
     comps={'minecraft:consumable': consumable(1.5, 'bow', 'minecraft:block.anvil.land', False)})

# (Goldtooth sells the pistol - wrapped before the den's shops are split from his stock)
_goldtooth0 = P70.goldtooth


def _goldtooth():
    from gen_dp import offer
    d = _goldtooth0()
    d['Offers']['Recipes'].append(offer(PRICE, ('rat_race_pistol', 1)))
    return d


P70.goldtooth = _goldtooth


def generate(G):
    fn, wjson, title, tellraw, give = G.fn, G.wjson, G.title, G.tellraw, G.give
    P = [T('[', 'dark_gray'), T('Black Market', 'dark_purple', bold=True), T('] ', 'dark_gray')]
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    sc = lambda n: {'score': {'name': n, 'objective': 'bm.bm'}, 'color': 'white', 'bold': True}
    objs = sorted(OBJ.values())
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {OBJ[c]} {c}' for c in CRIT] + [
        'execute unless score #rrday bm.bm matches -1.. run scoreboard players set #rrday bm.bm -1',
        'bossbar add bm:ratrace {text:"The Rat Race",color:"gold",bold:true}',
        'bossbar set bm:ratrace color yellow', 'bossbar set bm:ratrace style notched_10']
    G.OBJECTIVES += objs

    # ================================================================== THE PISTOL: the race is on
    G.consume_adv('rat_race_pistol', 'bm:p183/fire')
    no = lambda why: f'return run function bm:p183/no/{why}'
    fn('p183/fire', ['advancement revoke @s only bm:consume/rat_race_pistol',
                     'execute unless dimension minecraft:overworld run ' + no('world'),
                     'execute if score #rron bm.bm matches 1 run ' + no('running'),
                     'execute if score #rrday bm.bm = #day bm.bm run ' + no('today'),
                     f'execute if score #tod bm.bm matches {LAST_START + 1}.. run ' + no('late'),
                     'function bm:p183/start'])
    for why, msg in (('world', 'Fire it out in the Overworld - that\'s where the race is run.'),
                     ('running', 'The Rat Race is already on - get to work!'),
                     ('today', 'One Rat Race a day. Keep it for tomorrow.'),
                     ('late', 'Too late in the day - the race runs to sunset. Fire it before mid-afternoon.')):
        fn(f'p183/no/{why}', [give('rat_race_pistol'), say(msg, GOLD), 'playsound minecraft:block.dispenser.fail player @s ~ ~ ~ 0.8 1.2'])

    # the draw: never the same job twice running
    fn('p183/start', [
        'scoreboard players set #rron bm.bm 1', 'scoreboard players operation #rrday bm.bm = #day bm.bm',
        'scoreboard players set #rrc bm.bm 0', 'scoreboard players set #rrpk bm.bm 0', 'scoreboard players set #rrhalf bm.bm 0',
        f'execute store result score #rrk bm.bm run random value 1..{len(JOBS)}',
        'execute if score #rrk bm.bm = #rrlast bm.bm run scoreboard players add #rrk bm.bm 1',
        f'execute if score #rrk bm.bm matches {len(JOBS) + 1}.. run scoreboard players set #rrk bm.bm 1',
        'scoreboard players operation #rrlast bm.bm = #rrk bm.bm'] +
       [f'scoreboard players reset * {o}' for o in objs] +
       [f'execute if score #rrk bm.bm matches {k} run function bm:p183/job/{j[0]}' for k, j in enumerate(JOBS, 1)] +
       ['function bm:p183/scale', 'function bm:p183/bar', 'bossbar set bm:ratrace visible true',
        tellraw('@a', P + [{'selector': '@s', 'color': GOLD}, T(' fired a Starter\'s Pistol. ', 'gray'), T('The Rat Race is on!', GOLD, bold=True)]),
        'function bm:p183/announce',
        'execute as @a at @s run playsound minecraft:entity.firework_rocket.blast player @s ~ ~ ~ 1 0.8',
        'execute as @a at @s run playsound minecraft:block.note_block.bell player @s ~ ~ ~ 1 1.5',
        'execute as @a run title @s title {text:"The Rat Race",color:"gold",bold:true}',
        'particle minecraft:firework ~ ~2 ~ 0.3 0.3 0.3 0.15 40'])
    for k, (kind, label, add, sub, base, per) in enumerate(JOBS, 1):
        fn(f'p183/job/{kind}', [f'scoreboard players set #rrbase bm.bm {base}', f'scoreboard players set #rrper bm.bm {per}'])
        a, b = label.split('%s')
        # (the count: each player's work since the last second, set-back blocks off again)
        fn(f'p183/c/{kind}', [f'scoreboard players operation #rrc bm.bm += @s {OBJ[c]}' for c in add] +
                             [f'scoreboard players operation #rrc bm.bm -= @s {OBJ[c]}' for c in sub] +
                             [f'scoreboard players reset @s {OBJ[c]}' for c in add + sub])
        fn(f'p183/bar/{kind}', [f'bossbar set bm:ratrace name {G.snbt([T("The Rat Race: ", GOLD, bold=True), T(a, CHEESE), sc("#rrt"), T(b, CHEESE), T("  ·  ", "dark_gray"), sc("#rrv"), T(" / ", "gray"), sc("#rrt"), T("  ·  by sunset", DIM)])}'])
        fn(f'p183/say/{kind}', [tellraw('@a', [T('  The job: ', 'gray'), T(a, CHEESE, bold=True), sc('#rrt'), T(b, CHEESE, bold=True),
                                               T(' before sunset', 'gray'), T(' - everyone\'s work counts.', 'dark_gray')] +
                                        ([T(' (Set back down, a block comes off again.)', 'dark_gray')] if sub else []))])
    fn('p183/announce', [f'execute if score #rrk bm.bm matches {k} run function bm:p183/say/{j[0]}' for k, j in enumerate(JOBS, 1)])

    # ================================================================== EVERY SECOND
    G.FUNCS['bloodmoon/tick'].append('execute if score #rron bm.bm matches 1 run function bm:p183/during')
    fn('p183/during', [
        'execute unless score #rrday bm.bm = #day bm.bm run return run function bm:p183/lose',
        f'execute if score #tod bm.bm matches {SUNSET}.. run return run function bm:p183/lose',
        'execute store result score #n bm.rng if entity @a',
        'execute if score #n bm.rng > #rrpk bm.bm run function bm:p183/scale'] +
       [f'execute if score #rrk bm.bm matches {k} as @a run function bm:p183/c/{j[0]}' for k, j in enumerate(JOBS, 1)] +
       ['execute if score #rrc bm.bm >= #rrt bm.bm run return run function bm:p183/win',
        'scoreboard players operation #h bm.rng = #rrc bm.bm', 'scoreboard players operation #h bm.rng *= #2 bm.rng',
        'execute if score #rrhalf bm.bm matches 0 if score #h bm.rng >= #rrt bm.bm run function bm:p183/half',
        'function bm:p183/bar'])
    # (the target: base, and more for each extra player - the most seen online during the race)
    fn('p183/scale', ['execute store result score #rrpk bm.bm if entity @a', 'execute if score #rrpk bm.bm matches ..0 run scoreboard players set #rrpk bm.bm 1',
                      'scoreboard players operation #rrt bm.bm = #rrpk bm.bm', 'scoreboard players remove #rrt bm.bm 1',
                      'scoreboard players operation #rrt bm.bm *= #rrper bm.bm', 'scoreboard players operation #rrt bm.bm += #rrbase bm.bm'])
    fn('p183/bar', ['scoreboard players operation #rrv bm.bm = #rrc bm.bm', 'execute if score #rrv bm.bm matches ..-1 run scoreboard players set #rrv bm.bm 0',
                    'execute store result bossbar bm:ratrace max run scoreboard players get #rrt bm.bm',
                    'execute store result bossbar bm:ratrace value run scoreboard players get #rrv bm.bm',
                    'bossbar set bm:ratrace players @a'] +
       [f'execute if score #rrk bm.bm matches {k} run function bm:p183/bar/{j[0]}' for k, j in enumerate(JOBS, 1)])
    fn('p183/half', ['scoreboard players set #rrhalf bm.bm 1',
                     tellraw('@a', P + [T('The Rat Race: ', GOLD, bold=True), T('halfway there - ', CHEESE), sc('#rrv'), T(' of ', 'gray'), sc('#rrt'), T('.', 'gray')]),
                     'execute as @a at @s run playsound minecraft:block.note_block.chime player @s ~ ~ ~ 0.8 1.4'])

    # ================================================================== THE END: won, or the sun sets first (no penalty)
    fn('p183/lose', ['scoreboard players set #rron bm.bm 0', 'bossbar set bm:ratrace visible false',
                     tellraw('@a', P + [T('The sun\'s down. ', DIM), T('The Rat Race is lost', GOLD), T(' - ', 'gray'), sc('#rrv'), T(' of ', 'gray'), sc('#rrt'),
                                        T('. No harm done; try again tomorrow.', 'gray')]),
                     'execute as @a at @s run playsound minecraft:block.note_block.didgeridoo player @s ~ ~ ~ 0.8 0.6'])
    fn('p183/win', ['scoreboard players set #rron bm.bm 0', 'scoreboard players operation #rrv bm.bm = #rrt bm.bm', 'bossbar set bm:ratrace visible false',
                    tellraw('@a', P + [T('The Rat Race is WON! ', GOLD, bold=True), sc('#rrt'), T(' done before sunset - a prize for everyone.', CHEESE)]),
                    'execute as @a run title @s title {text:"Race won!",color:"gold",bold:true}',
                    'execute as @a run title @s subtitle {text:"a prize for everyone",color:"#ffe58a"}',
                    'execute as @a at @s run playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1',
                    'execute as @a at @s run particle minecraft:firework ~ ~2 ~ 0.6 0.6 0.6 0.2 50',
                    'execute as @a at @s run particle minecraft:wax_on ~ ~1.5 ~ 1 1 1 0 30',
                    'execute as @a at @s run function bm:p183/prize'])

    # ================================================================== THE PRIZE (each player: Tokens, and one draw)
    wjson('bm/loot_table/p183/tokens.json', {'type': 'minecraft:command', 'pools': [{'rolls': 1, 'entries': [G.loot_entry('token', G.uni(3, 6))]}]})
    wjson('bm/loot_table/p183/medallions.json', {'type': 'minecraft:command', 'pools': [{'rolls': 1, 'entries': [G.loot_entry('medallion', G.uni(1, 2))]}]})
    won = lambda what, col: tellraw('@s', [T('  Your prize: ', 'gray'), T('Tokens', GOLD), T(' and ', 'gray'), T(what, col, bold=True), T('!', 'gray')])
    DRAW = [   # (out of 100)
        (30, 'medallions', ['loot give @s loot bm:p183/medallions'], won('Medallions', '#c0c8d8')),
        (12, 'trophy', [give('trophy')], won('a Trophy', GOLD)),
        (18, 'fragment', ['loot give @s loot bm:p173/win_frag'], won('a Lucky Map Fragment', '#e8c547')),
        (10, 'horseshoe', [give('lucky_horseshoe')], won('a Lucky Horseshoe', LUCKY)),
        (8, 'effigy', [give('crimson_effigy')], won('a Crimson Effigy', '#d02020')),
        (8, 'bell', [give('pearl_bell')], won("Pearlman's Bell", '#9ad0ff')),
        (6, 'beacon', ['execute unless score #vornmet bm.bm matches 1 run return run function bm:p183/d/cards', give('vorn_beacon')], won('a Vorn Fleet Beacon', '#7dff6a')),
        (8, 'cards', [give('scratch_card', 3)], won('three Lucky Scratch Cards', 'yellow')),
    ]
    assert sum(w for w, *_ in DRAW) == 100
    lines, lo = ['loot give @s loot bm:p183/tokens', 'execute store result score #r bm.rng run random value 1..100'], 1
    for w, k, cmds, msg in DRAW:
        lines.append(f'execute if score #r bm.rng matches {lo}..{lo + w - 1} run return run function bm:p183/d/{k}')
        fn(f'p183/d/{k}', cmds + [msg]); lo += w
    fn('p183/prize', lines)

    # ================================================================== THE LUCKY HORSESHOE: tonight is a Lucky Night
    G.consume_adv('lucky_horseshoe', 'bm:p183/shoe')
    fn('p183/shoe', ['advancement revoke @s only bm:consume/lucky_horseshoe',
                     'execute unless dimension minecraft:overworld run return run function bm:p183/shoe_no',
                     'execute if score #bday bm.bm matches 1 run return run function bm:p183/shoe_no',
                     'execute if score #dnday bm.bm = #day bm.bm run return run function bm:p183/shoe_no',
                     'execute if score #lnight bm.bm matches 1 run return run function bm:p183/shoe_no',
                     'execute if score #lucky bm.bm matches 1 if score #lday bm.bm = #day bm.bm run return run function bm:p183/shoe_no',
                     'scoreboard players set #lucky bm.bm 1', 'scoreboard players operation #lday bm.bm = #day bm.bm',
                     'execute if score #tod bm.bm matches 23000.. run scoreboard players set #lforce bm.bm 1',
                     'playsound minecraft:block.amethyst_block.chime player @a[distance=..32] ~ ~ ~ 1 1.2',
                     'particle minecraft:happy_villager ~ ~1.5 ~ 0.5 0.5 0.5 0 20',
                     tellraw('@a', P + [{'selector': '@s', 'color': LUCKY}, T(' hung up a Lucky Horseshoe. ', 'gray'), T('Tonight is a Lucky Night!', LUCKY, bold=True)])])
    fn('p183/shoe_no', [give('lucky_horseshoe'), say('It won\'t hang - not tonight (a Blood Moon, a Dread Night, or luck already on its way).', LUCKY),
                        'playsound minecraft:block.anvil.land player @s ~ ~ ~ 0.4 1.6'])

    # ================================================================== the admin's own (for tests)
    fn('admin/rat_race', [give('rat_race_pistol', 2), give('lucky_horseshoe')])
    fn('admin/rat_race_end', ['execute if score #rron bm.bm matches 1 run function bm:p183/lose'])
    if 'admin/help' in G.FUNCS:
        G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/rat_race', 'yellow'), T('  two Starter\'s Pistols and a Lucky Horseshoe; ', 'gray'),
                                                    T('/function bm:admin/rat_race_end', 'yellow'), T('  call off a race', 'gray')]))
    G.FUNCS['admin/uninstall'][0:0] = ['bossbar remove bm:ratrace'] + [f'scoreboard objectives remove {o}' for o in objs]
    return len(JOBS), len(DRAW)


def rp(R):
    g = R.grid
    R.ICONS['rat_race_pistol'] = g(['................', '................', '................', '..kkkkkkkkkkk...', '.kGgggggggggGk..', '.kGkkkkkkkkkkWk.',
                                    '.kGgggggggk.kk..', '..kkkkGggk......', '.....kGgk.k.....', '.....kGgkkk.....', '....kRrrk.......', '....kRrrk.......',
                                    '...kRrrk........', '...kRrrk........', '...kkkk.........', '................'],
                                   dict(k='#1a1410', G='#ffd24a', g='#a87a20', W='#fff4c0', R='#6a2a10', r='#a8501c'))
    R.ICONS['lucky_horseshoe'] = g(['................', '................', '...kkk....kkk...', '..kSsk....kSsk..', '..kSsk....kSsk..', '..kSok....koSk..',
                                    '..kSsk....kSsk..', '..kSok....koSk..', '..kSsk....kSsk..', '..kSssk..kssSk..', '...kSsskkssSk...', '....kSssssSk.....',
                                    '.....kkkkkk.....', '.......gg.......', '......gLLg......', '.......gg.......'],
                                   dict(k='#202428', S='#e8eef2', s='#9aa6b0', o='#3a3f44', g='#2a7a34', L='#5ad86a'))

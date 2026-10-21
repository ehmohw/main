"""2.84b: HARD MODE'S DARK AUCTIONS, DUNGEON REPLAYS AND THE COMMUNITY POTS.

THE DARK AUCTION, HARD MODE   every sale in a hard-mode world swaps a regular lot for two of its own:
  INFUSIONS (power upgrades)  hold the infusion, the item to infuse in your OFF hand, and hold right-click: one infusion an item.
                weapons   Lifesteal (a kill heals 2 hearts), Frenzy (a kill: Speed II + Strength I for 6 s), Reaper (8 more XP a kill)
                tools     Quickhand (Haste II while held), Deepsight (Night Vision while held, below y 50)
                armour    Vitality (Regeneration I), Emberward (Fire Resistance), Swiftstride (Speed I), Tidebound (Water Breathing;
                          Dolphin's Grace in water) - while worn
  ARTIFACTS     six pieces of the world's history, to set down and show off (sneak + use on a block; punch to pick up) - or to
                scrap at the Scrap Bin for Medallions.
HARD REPLAYS  a dungeon boss woken in a hard-mode world by someone who has beaten the Hollow King fights at 175% health, with
              Strength and Resistance - its minions too. Its fall gives each victor who has beaten the King its RELIC the first
              time (1 in 5 after), and 2 Blood Moon Crystals. Relics work anywhere in your pack:
                Broodmother's Heartsilk  poison never takes; Jump Boost I        Frost Marksman's Rimeheart  slowness never takes; Speed II on ice and snow
                Tyrant's Pearl           Water Breathing, Dolphin's Grace, Conduit Power in water
                Archmage's Focus         weakness and mining fatigue never take; Luck I
                Bobbery's Fuse           Fire Resistance; Haste I                Hollow Crownshard  wither never takes; Strength I
                Golden Egg of Plenty     Luck II; Hero of the Village (the Golden Goose)
THE COMMUNITY POTS   on the Rat Bank's account page: everyone's Tokens go into one pot; a full pot unlocks a buff for the whole
              world, for good - and anyone can switch it on or off. (Never in the gutter.)
                Lamplighters' Fund  250  Night Vision at night (Overworld)      Harvest Guild    300  Luck I
                Miners' Union       400  Haste I                                Couriers' Guild  400  Speed I
                Hearth Fund         500  Second Wind: under 3 hearts, Regeneration II for 5 s (a minute's rest)
                Bounty Office       600  Hunter's Purse: every monster you kill, 1 in 30 a Token
"""
from items import item, T, TOTEM, ITEMS, consumable
from nbt import snbt, B, F, Int
import economy as ECON
import phase30 as P30
import phase31 as P31
import phase177 as P177

DREAD = '#b0102a'

# ================================================================== INFUSIONS
INF = {  # key: (class, name, colour, what it does)
    'lifesteal': ('weapon', 'Lifesteal', '#e02040', 'Every kill heals two hearts.'),
    'frenzy': ('weapon', 'Frenzy', '#ff8a30', 'A kill: Speed II and Strength I for 6 s.'),
    'reaper': ('weapon', 'Reaper', '#7ad0a0', 'Every kill: 8 more experience.'),
    'quickhand': ('tool', 'Quickhand', '#ffd040', 'Haste II while held.'),
    'deepsight': ('tool', 'Deepsight', '#70a0ff', 'Night Vision while held, below y 50.'),
    'vitality': ('armor', 'Vitality', '#ff6080', 'Regeneration I while worn.'),
    'emberward': ('armor', 'Emberward', '#ff7020', 'Fire Resistance while worn.'),
    'swiftstride': ('armor', 'Swiftstride', '#80e0ff', 'Speed I while worn.'),
    'tidebound': ('armor', 'Tidebound', '#30c0b0', "Water Breathing - and Dolphin's Grace in water - while worn."),
}
CLASS_WORD = {'weapon': 'a weapon', 'tool': 'a tool', 'armor': 'an armour piece'}
for k, (cls, nm, col, what) in INF.items():
    item(f'inf_{k}', TOTEM, f'Infusion of {nm}', col,
         [f'For {CLASS_WORD[cls]}: {what}', ('Hold the item to infuse in your OFF hand,', 'blue'), ('then hold right-click with this. One', 'blue'),
          ('infusion an item - it stays for good.', 'blue'), ('Sold only at hard mode\'s Dark Auctions.', 'dark_gray')],
         model=f'bm:inf_{k}', stack=4, glint=True, comps={'minecraft:consumable': consumable(1.2, 'drink', 'minecraft:item.bottle.fill_dragonbreath', False)}, cat='misc')

# ================================================================== ARTIFACTS
ART = {  # key: (name, colour, lore, scrap Medallions, ambient particle)
    'crownshard': ('Shard of the Hollow Crown', '#9a8ab0', 'Still cold where he wore it.', 5, 'minecraft:sculk_soul ~ ~0.8 ~ 0.15 0.15 0.15 0.01 1'),
    'starchart': ('Vorn Star-Chart', '#5ad8ff', 'Every star on it is a place they have taken.', 5, 'minecraft:end_rod ~ ~0.9 ~ 0.2 0.1 0.2 0.01 1'),
    'bell': ('Drowned Bell', '#2fa39b', 'It rang for the Sunken Throne. It still rings, underwater.', 4, 'minecraft:bubble_pop ~ ~0.8 ~ 0.2 0.2 0.2 0 1'),
    'dreadheart': ('Petrified Dread Heart', DREAD, 'Turned to stone - and still, now and then, it beats.', 6, 'minecraft:dust{color:[0.69,0.06,0.16],scale:0.8} ~ ~0.7 ~ 0.15 0.1 0.15 0 1'),
    'ledger': ("The Rat King's Ledger of Debts", '#ffb300', 'Every name in the Black Market - and what they owe.', 5, 'minecraft:wax_on ~ ~0.8 ~ 0.2 0.1 0.2 0 1'),
    'firstkey': ('The First Black Market Key', '#a96bff', 'The very first. It opened a door that is not there any more.', 6, 'minecraft:enchant ~ ~0.9 ~ 0.2 0.2 0.2 0.3 2'),
}
for k, (nm, col, lore, scrap, _p) in ART.items():
    item(f'art_{k}', TOTEM, nm, col,
         [lore, ('An artifact: sneak + use on a block to set', 'blue'), ('it down (punch it to pick it up) - or scrap', 'blue'),
          (f'it at the Scrap Bin for {scrap} Medallions.', 'blue'), ('Sold only at hard mode\'s Dark Auctions.', 'dark_gray')],
         model=f'bm:art_{k}', stack=1, comps=P177.hold('none'), cat='misc')

# the auction's hard-mode lots (kind 'hard': never drawn but by the hard draw)
HARD_LOTS = [(f'inf_{k}', f'Infusion of {nm}', col, 'hard', ECON.cut(b), None, [(f'inf_{k}', 1)], True)
             for (k, (cls, nm, col, what)), b in zip(INF.items(), (24, 20, 16, 18, 16, 22, 18, 18, 16))] + \
            [(f'art_{k}', nm, col, 'hard', ECON.cut(2 * scrap + 4), None, [(f'art_{k}', 1)], True) for k, (nm, col, lore, scrap, _p) in ART.items()]
P30.LOTS += HARD_LOTS

# ================================================================== DUNGEON RELICS (hard replays)
RELIC = {  # dungeon: (iid, name, colour, lines of what it does, effect commands run each second as the carrier, at them)
    'brood': ('relic_brood', "Broodmother's Heartsilk", '#7d8f3a', ['Poison never takes hold of you.', 'Jump Boost I.'],
              ['effect clear @s minecraft:poison', 'effect give @s minecraft:jump_boost 3 0 true']),
    'frost': ('relic_frost', "Frost Marksman's Rimeheart", '#a8d8ff', ['Slowness never takes hold of you.', 'Speed II on ice and snow.'],
              ['effect clear @s minecraft:slowness', 'execute if block ~ ~-0.5 ~ #minecraft:ice run effect give @s minecraft:speed 2 1 true',
               'execute if block ~ ~-0.5 ~ minecraft:snow_block run effect give @s minecraft:speed 2 1 true',
               'execute if block ~ ~ ~ minecraft:snow run effect give @s minecraft:speed 2 1 true']),
    'tide': ('relic_tide', "Tyrant's Pearl", '#2fa39b', ["In water: Water Breathing, Dolphin's Grace", 'and Conduit Power.'],
             ['execute if block ~ ~1 ~ minecraft:water run effect give @s minecraft:water_breathing 12 0 true',
              'execute if block ~ ~1 ~ minecraft:water run effect give @s minecraft:dolphins_grace 2 0 true',
              'execute if block ~ ~1 ~ minecraft:water run effect give @s minecraft:conduit_power 12 0 true']),
    'hex': ('relic_hex', "Archmage's Focus", '#9b59d0', ['Weakness and Mining Fatigue never take hold.', 'Luck I.'],
            ['effect clear @s minecraft:weakness', 'effect clear @s minecraft:mining_fatigue', 'effect give @s minecraft:luck 3 0 true']),
    'keep': ('relic_keep', "Bobbery's Fuse", '#e0602a', ['Fire Resistance.', 'Haste I.'],
             ['effect give @s minecraft:fire_resistance 3 0 true', 'effect give @s minecraft:haste 3 0 true']),
    'hollow': ('relic_hollow', 'Hollow Crownshard', '#c8c4d8', ['The Wither never takes hold of you.', 'Strength I.'],
               ['effect clear @s minecraft:wither', 'effect give @s minecraft:strength 3 0 true']),
    'lucky': ('relic_lucky', 'Golden Egg of Plenty', '#ffd700', ['Luck II.', 'Hero of the Village.'],
              ['effect give @s minecraft:luck 3 1 true', 'effect give @s minecraft:hero_of_the_village 3 0 true']),
}
from p2.config import D as P2D
for d, (iid, nm, col, lines, cmds) in RELIC.items():
    item(iid, TOTEM, nm, col, [f'From {P2D[d]["boss"]}, beaten again in a hard-mode world.'] + [(l, 'blue') for l in lines] +
         [('Works anywhere in your pack.', 'dark_aqua'), ('A relic of a hard replay - for those who beat the Hollow King.', 'dark_gray')],
         model=f'bm:{iid}', stack=1, glint=True, cat='misc')
HP_MULT = 0.75                                       # +75% health in a hard replay

# ================================================================== COMMUNITY POTS
POTS = [  # (key, pot, goal Tokens, buff, what it does)
    ('night', "Lamplighters' Fund", 250, 'Night Lights', 'Night Vision for everyone at night, in the Overworld'),
    ('luck', 'Harvest Guild', 300, 'Bountiful', 'Luck I for everyone'),
    ('haste', "Miners' Union", 400, 'Quick Picks', 'Haste I for everyone'),
    ('speed', "Couriers' Guild", 400, 'Fleet Feet', 'Speed I for everyone'),
    ('wind', 'Hearth Fund', 500, 'Second Wind', 'under 3 hearts, Regeneration II for 5 s (then a minute\'s rest)'),
    ('purse', 'Bounty Office', 600, "Hunter's Purse", 'every monster killed: 1 in 30 a Token'),
]
PMENU = 3300                                        # (his block: 3300-3349)
POT_BTN = 4085                                      # on the Rat Bank's account page
P31.ACCT_EXTRA.append(([T('Community Pots', '#ffd27a')], POT_BTN, T('Everyone\'s Tokens in one pot: a full pot is a buff for the whole world', 'gray'), 'p178/pots/open'))


def generate(G):
    fn, wjson, title, tellraw, give = G.fn, G.wjson, G.title, G.tellraw, G.give
    import phase28 as P28
    import phase177 as P177g
    PRE = [T('[', 'dark_gray'), T('Black Market', 'dark_purple', bold=True), T('] ', 'dark_gray')]
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    second, fast = G.FUNCS['loop/second'], G.FUNCS['loop/fast']
    load = G.FUNCS['load']
    objs = ['bm.potg', 'bm.potsw']
    load[-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs

    # ---------------------------------------------------------------- infusions
    cls_lines = ['scoreboard players set #oc bm.rng 0'] + \
        [f'execute if items entity @s weapon.offhand {it} run scoreboard players set #oc bm.rng 1' for it in P177g.WEAPON_ITEMS] + \
        [f'execute if items entity @s weapon.offhand {it} run scoreboard players set #oc bm.rng 2' for it in P177g.TOOL_ITEMS] + \
        [f'execute if items entity @s weapon.offhand {it} run scoreboard players set #oc bm.rng {3 + i}' for i, (it, sl) in enumerate(P177g.ARMOR_SLOTS)]
    fn('p178/oclass', cls_lines)
    want = {'weapon': '1', 'tool': '2', 'armor': '3..6'}
    for k, (cls, nm, col, what) in INF.items():
        iid = f'inf_{k}'
        G.consume_adv(iid, f'bm:p178/inf/{k}')
        lore = T(f'☠ Infused: {nm} - {what}', col)
        fn(f'p178/inf/{k}', [f'advancement revoke @s only bm:consume/{iid}', 'function bm:p178/oclass',
                             f'execute unless score #oc bm.rng matches {want[cls]} run return run function bm:p178/inf/{k}_no',
                             'execute if data entity @s equipment.offhand.components."minecraft:custom_data".bm_inf run return run function bm:p178/inf/' + k + '_twice',
                             f'item modify entity @s weapon.offhand {{function:"minecraft:set_custom_data",tag:{{bm_inf:"{k}"}}}}',
                             f'item modify entity @s weapon.offhand {{function:"minecraft:set_lore",mode:"append",lore:[{snbt(lore)}]}}',
                             'playsound minecraft:block.brewing_stand.brew player @s ~ ~ ~ 1 0.7', 'playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.6 1.2',
                             'particle minecraft:witch ~ ~1 ~ 0.4 0.5 0.4 0.1 30',
                             tellraw('@s', PRE + [T('Infused: ', 'gray'), T(nm, col, bold=True), T(f' - {what}', 'gray')])])
        fn(f'p178/inf/{k}_no', [give(iid), say(f'Hold {CLASS_WORD[cls]} in your off hand to infuse it. (Returned.)', '#c8a0a0')])
        fn(f'p178/inf/{k}_twice', [give(iid), say('That item already carries an infusion. (Returned.)', '#c8a0a0')])
    inf = lambda k: f'*[minecraft:custom_data~{{bm_inf:"{k}"}}]'
    # weapons: on a kill
    for k, reward in (('lifesteal', ['effect give @s minecraft:instant_health 1 0 true', 'particle minecraft:heart ~ ~1.8 ~ 0.3 0.2 0.3 0 3']),
                      ('frenzy', ['effect give @s minecraft:speed 6 1 true', 'effect give @s minecraft:strength 6 0 true', 'particle minecraft:angry_villager ~ ~1.8 ~ 0.3 0.2 0.3 0 2']),
                      ('reaper', ['xp add @s 8 points', 'particle minecraft:soul ~ ~1.2 ~ 0.3 0.3 0.3 0.02 6'])):
        wjson(f'bm/advancement/p178/kill_{k}.json', {'criteria': {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {
            'player': [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {
                'equipment': {'mainhand': {'predicates': {'minecraft:custom_data': f'{{bm_inf:"{k}"}}'}}}}}]}}}, 'rewards': {'function': f'bm:p178/kill/{k}'}})
        fn(f'p178/kill/{k}', [f'advancement revoke @s only bm:p178/kill_{k}'] + reward)
    # tools: while held; armour: while worn
    second += [f'execute as @a if items entity @s weapon.mainhand {inf("quickhand")} run effect give @s minecraft:haste 2 1 true',
               f'execute as @a at @s if entity @s[y=-64,dy=113] if items entity @s weapon.mainhand {inf("deepsight")} run effect give @s minecraft:night_vision 12 0 true']
    wjson('bm/predicate/p178/has_regen.json', {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:effects': {'minecraft:regeneration': {}}}})
    for sl in ('armor.head', 'armor.chest', 'armor.legs', 'armor.feet'):
        second += [f'execute as @a if items entity @s {sl} {inf("vitality")} unless predicate bm:p178/has_regen run effect give @s minecraft:regeneration 8 0 true',
                   f'execute as @a if items entity @s {sl} {inf("emberward")} run effect give @s minecraft:fire_resistance 3 0 true',
                   f'execute as @a if items entity @s {sl} {inf("swiftstride")} run effect give @s minecraft:speed 2 0 true',
                   f'execute as @a if items entity @s {sl} {inf("tidebound")} run effect give @s minecraft:water_breathing 12 0 true',
                   f'execute as @a at @s if block ~ ~1 ~ minecraft:water if items entity @s {sl} {inf("tidebound")} run effect give @s minecraft:dolphins_grace 2 0 true']

    # ---------------------------------------------------------------- artifacts: set down, picked up, scrapped
    for i, (k, (nm, col, lore, scrap, part)) in enumerate(ART.items()):
        P177g.placeable(G, 'p178', f'art_{k}', f'bm.art{i}', scale=0.8, sound='minecraft:block.amethyst_block')
        second.append(f'execute as @e[type=minecraft:marker,tag=bm.art{i}m] at @s if entity @a[distance=..16] run particle {part}')
        load.insert(-1, f'data modify storage bm:scrap table.art_{k} set value ' + snbt({'k': Int(1), 'r': [{'c': 'medallion', 'n': Int(scrap)}]}))
        G.SCRAP_TABLE[f'art_{k}'] = (1, [('medallion', scrap)])

    # ---------------------------------------------------------------- the auction's hard draw: two of its own lots in place of a regular one
    lots = G.P30_LOTS
    idx = {l[0]: i for i, l in enumerate(lots)}
    pools = {'infusion': [idx[f'inf_{k}'] for k in INF], 'artifact': [idx[f'art_{k}'] for k in ART]}
    st = G.FUNCS['p30/start']
    st.insert(st.index('function bm:p30/next'), 'execute if score #hard bm.cfg matches 1 run function bm:p178/auc/draw')
    fn('p178/auc/draw', ['data remove storage bm:auction sale[0]', 'function bm:p178/auc/infusion', 'function bm:p178/auc/artifact'])
    for name, pool in pools.items():
        fn(f'p178/auc/{name}', ['scoreboard players set #got bm.auc 0', 'scoreboard players set #try bm.auc 0', f'function bm:p178/auc/{name}_try'])
        fn(f'p178/auc/{name}_try', ['scoreboard players add #try bm.auc 1', f'execute store result score #r bm.auc run random value 0..{len(pool) - 1}'] +
           [f'execute if score #r bm.auc matches {j} run function bm:p178/auc/pick {{i:{i}}}' for j, i in enumerate(pool)] +
           [f'execute if score #got bm.auc matches 0 if score #try bm.auc matches ..30 run function bm:p178/auc/{name}_try'])
    fn('p178/auc/pick', ['$execute if score #pk$(i) bm.auc matches 1 run return 0', '$scoreboard players set #pk$(i) bm.auc 1',
                         '$data modify storage bm:auction sale insert 0 value $(i)', 'scoreboard players set #got bm.auc 1'])

    # ---------------------------------------------------------------- hard replays of the dungeons
    for d, (iid, nm, col, lines, cmds) in RELIC.items():
        cfg = P2D[d]
        ar = cfg['arena_r']
        R = ar + 28
        boss = f'@e[tag=bm.boss_{d},distance=..{R}]'
        G.FUNCS[f'p2/{d}/fight_begin'].append(f'execute if score #hard bm.cfg matches 1 if entity @a[tag=bm.ina_{d},scores={{bm.conqb=6..}},distance=..{ar + 40}] run function bm:p178/hr/begin_{d}')
        fn(f'p178/hr/begin_{d}', ['tag @s add bm.hardrun', f'execute as {boss} at @s run function bm:p178/hr/buff',
                                  f'title @a[tag=bm.ina_{d},distance=..{ar + 40}] times 5 50 15',
                                  title(f'@a[tag=bm.ina_{d},distance=..{ar + 40}]', 'subtitle', T(f'{cfg["boss"]} remembers you - and has grown.', '#c8a0a0', italic=True)),
                                  title(f'@a[tag=bm.ina_{d},distance=..{ar + 40}]', 'title', T('HARD REPLAY', DREAD, bold=True)),
                                  f'playsound minecraft:entity.wither.spawn hostile @a[distance=..{ar + 40}] ~ ~ ~ 0.6 0.6'])
        fl = G.FUNCS[f'p2/{d}/fight']
        fl[0:0] = [f'execute if entity @s[tag=bm.hardrun] as {boss.replace("]", ",tag=!bm.hrb]")} at @s run function bm:p178/hr/buff',
                   f'execute if entity @s[tag=bm.hardrun] as @e[tag=bm.minion_{d},tag=!bm.hrb,distance=..{ar + 40}] run function bm:p178/hr/mbuff']
        fl.insert(0, f'execute if entity @s[tag=bm.hardrun] store result bossbar bm:boss_{d} max run attribute @e[tag=bm.boss_{d},distance=..{R},limit=1] minecraft:max_health get')
        # (the victors of a hard replay are marked before the credit runs as each of them)
        vl = G.FUNCS[f'p2/{d}/victory']
        k = next(i for i, l in enumerate(vl) if l.endswith(f'run function bm:p2/{d}/credit'))
        vl.insert(k, f'execute if entity @s[tag=bm.hardrun] run tag @a[tag=bm.f_{d}] add bm.hrv')
        G.FUNCS[f'p2/{d}/credit'] += [f'execute if entity @s[tag=bm.hrv] at @s run function bm:p178/hr/win_{d}', 'tag @s remove bm.hrv']
        vl.append('tag @s remove bm.hardrun')
        G.FUNCS[f'p2/{d}/abandon'].append('tag @s remove bm.hardrun')
        fn(f'p178/hr/win_{d}', ['execute unless score @s bm.conqb matches 6.. run return 0', give('blood_crystal', 2),
                                f'execute unless entity @s[tag=bm.hrw_{d}] run return run function bm:p178/hr/first_{d}',
                                'execute store result score #r bm.rng run random value 1..5',
                                f'execute if score #r bm.rng matches 1 run {give(iid)}',
                                'execute if score #r bm.rng matches 1 run ' + tellraw('@s', PRE + [T('The hard replay leaves you another ', 'gray'), T(nm, col, bold=True), T('.', 'gray')]),
                                'execute unless score #r bm.rng matches 1 run ' + tellraw('@s', PRE + [T(f'Hard replay won. ({nm}: 1 in 5 after the first.)', 'gray')])])
        fn(f'p178/hr/first_{d}', [f'tag @s add bm.hrw_{d}', give(iid), 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 0.8',
                                  tellraw('@a', PRE + [{'selector': '@s', 'color': 'gold'}, T(' beat ', 'gray'), T(cfg['boss'], cfg['color'], bold=True),
                                                       T(' in a hard replay, and took ', 'gray'), T(nm, col, bold=True), T('.', 'gray')])])
        # the relic, carried
        second += [f'execute as @a at @s if items entity @s container.* {holds(iid)} run function bm:p178/rl/{d}',
                   f'execute as @a at @s unless items entity @s container.* {holds(iid)} if items entity @s weapon.offhand {holds(iid)} run function bm:p178/rl/{d}']
        fn(f'p178/rl/{d}', cmds)
    fn('p178/hr/buff', [f'attribute @s minecraft:max_health modifier add bm:hardrun {HP_MULT} add_multiplied_base',
                        'execute store result entity @s Health float 1 run attribute @s minecraft:max_health get',
                        'effect give @s minecraft:strength infinite 0 true', 'effect give @s minecraft:resistance infinite 0 true', 'tag @s add bm.hrb',
                        'particle minecraft:soul_fire_flame ~ ~1 ~ 0.6 1 0.6 0.05 40'])
    fn('p178/hr/mbuff', [f'attribute @s minecraft:max_health modifier add bm:hardrun {HP_MULT / 1.5:.2f} add_multiplied_base',
                         'execute store result entity @s Health float 1 run attribute @s minecraft:max_health get',
                         'effect give @s minecraft:strength infinite 0 true', 'tag @s add bm.hrb'])

    # ---------------------------------------------------------------- the community pots
    for i, (k, pot, goal, buff, what) in enumerate(POTS):
        load[-1:-1] = [f'execute unless score #pot{i} bm.cfg matches 0.. run scoreboard players set #pot{i} bm.cfg 0',
                       f'execute unless score #potu{i} bm.cfg matches 0.. run scoreboard players set #potu{i} bm.cfg 0',
                       f'execute unless score #poton{i} bm.cfg matches 0.. run scoreboard players set #poton{i} bm.cfg 0']
    B_ = lambda lbl, code, w=200, tip=None: P28.btn(lbl, code, tooltip=tip, width=w)
    main = P28.multi([T('Community Pots', '#ffd27a', bold=True), T('  ·  The Rat Bank', 'gray')],
                     [P28.body([T('Everyone\'s Tokens go into one pot. A full pot unlocks a buff for the whole world, for good - '
                                  'and anyone can switch it on or off. (Never in the gutter.)', 'gray')], 320),
                      P28.body([T('You have given ', 'dark_gray'), T('$(mine)', 'gold'), T(' Tokens in all.', 'dark_gray')], 320)],
                     [B_([T(pot, '#ffd27a'), T(f'  $(p{i})/{goal}', 'white'), T(f'$(s{i})', '#7aff7a', bold=True)], PMENU + 1 + i, tip=T(f'{buff}: {what}', 'gray'))
                      for i, (k, pot, goal, buff, what) in enumerate(POTS)] + [B_(T('« Your account', 'gray'), PMENU + 9)], columns=2)
    fill = []
    for i in range(len(POTS)):
        fill += [f'execute store result storage bm:ui pots.p{i} int 1 run scoreboard players get #pot{i} bm.cfg', f'data modify storage bm:ui pots.s{i} set value ""',
                 f'execute if score #potu{i} bm.cfg matches 1 if score #poton{i} bm.cfg matches 1 run data modify storage bm:ui pots.s{i} set value "  ON"',
                 f'execute if score #potu{i} bm.cfg matches 1 unless score #poton{i} bm.cfg matches 1 run data modify storage bm:ui pots.s{i} set value "  off"']
    fn('p178/pots/fill', ['execute unless score @s bm.potg matches 0.. run scoreboard players set @s bm.potg 0',
                          'execute store result storage bm:ui pots.mine int 1 run scoreboard players get @s bm.potg'] + fill)
    fn('p178/pots/open', [f'scoreboard players set @s bm.menu {PMENU}', 'function bm:p178/pots/fill', 'function bm:p178/pots/dlg with storage bm:ui pots'])
    fn('p178/pots/dlg', [f'$dialog show @s {P28.inline(main)}'])
    act = [f'execute unless score @s bm.menu matches {PMENU} run return run function bm:p28/stale',
           f'execute if score #act bm.pay matches {PMENU + 9} run return run function bm:p31/bank/open']
    for i, (k, pot, goal, buff, what) in enumerate(POTS):
        page = P28.multi([T(pot, '#ffd27a', bold=True), T('  ·  Community Pots', 'gray')],
                         [P28.body([T(f'{buff}: ', '#7aff7a', bold=True), T(what[0].upper() + what[1:] + '.', 'gray')], 320),
                          P28.body([T('In the pot: ', 'gray'), T(f'$(p{i})', 'white', bold=True), T(f' of {goal} Tokens', 'gray'), T(f'$(s{i})', '#7aff7a', bold=True)], 320),
                          P28.body([T('From your pockets first, then your account.', 'dark_gray')], 320)],
                         [B_([T('Give 10 Tokens', 'gold')], PMENU + 10 + i), B_([T('Give 50 Tokens', 'gold')], PMENU + 20 + i),
                          B_([T('Switch it on / off', '#7aff7a')], PMENU + 30 + i, tip=T('Once the pot is full: for everyone', 'gray')),
                          B_(T('« The pots', 'gray'), PMENU + 40)], columns=2)
        fn(f'p178/pots/page{i}', [f'scoreboard players set @s bm.menu {PMENU}', 'function bm:p178/pots/fill', f'function bm:p178/pots/pdlg{i} with storage bm:ui pots'])
        fn(f'p178/pots/pdlg{i}', [f'$dialog show @s {P28.inline(page)}'])
        for n, code in ((10, PMENU + 10 + i), (50, PMENU + 20 + i)):
            fn(f'p178/pots/give{i}_{n}', [f'execute if score #potu{i} bm.cfg matches 1 run return run function bm:p178/pots/full{i}',
                                          f'scoreboard players set #need bm.pay {goal}', f'scoreboard players operation #need bm.pay -= #pot{i} bm.cfg',
                                          f'execute if score #need bm.pay matches {n + 1}.. run scoreboard players set #need bm.pay {n}',
                                          'scoreboard players operation #gv bm.rng = #need bm.pay',
                                          'execute unless function bm:p178/paytok run return run function bm:p178/pots/poor',
                                          f'scoreboard players operation #pot{i} bm.cfg += #gv bm.rng', 'scoreboard players operation @s bm.potg += #gv bm.rng',
                                          'playsound minecraft:block.chain.place player @s ~ ~ ~ 0.8 1.4',
                                          title('@s', 'actionbar', [T('Given: ', 'gray'), {'score': {'name': '#gv', 'objective': 'bm.rng'}, 'color': 'gold'}, T(f' Tokens to the {pot}.', 'gray')]),
                                          f'execute if score #pot{i} bm.cfg matches {goal}.. run function bm:p178/pots/unlock{i}', f'function bm:p178/pots/page{i}'])
            act.append(f'execute if score #act bm.pay matches {code} run return run function bm:p178/pots/give{i}_{n}')
        fn(f'p178/pots/full{i}', [say(f'The {pot} is full - its buff is the world\'s.', '#7aff7a'), f'function bm:p178/pots/page{i}'])
        fn(f'p178/pots/unlock{i}', [f'scoreboard players set #potu{i} bm.cfg 1', f'scoreboard players set #poton{i} bm.cfg 1',
                                    tellraw('@a', PRE + [T(f'The {pot} is full! ', '#ffd27a', bold=True), T(f'{buff} for everyone: {what}. ', 'gray'),
                                                         T('(Switch it on or off in Community Pots, on the Rat Bank\'s account page.)', 'dark_gray')]),
                                    'execute as @a at @s run playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.6 1.2'])
        fn(f'p178/pots/toggle{i}', [f'execute unless score #potu{i} bm.cfg matches 1 run return run function bm:p178/pots/notyet{i}',
                                    f'execute if score #poton{i} bm.cfg matches 1 run scoreboard players set #poton{i} bm.cfg 2',
                                    f'execute unless score #poton{i} bm.cfg matches 2 run scoreboard players set #poton{i} bm.cfg 1',
                                    f'execute if score #poton{i} bm.cfg matches 2 run scoreboard players set #poton{i} bm.cfg 0',
                                    f'execute if score #poton{i} bm.cfg matches 1 run ' + tellraw('@a', PRE + [{'selector': '@s', 'color': 'white'}, T(f' switched {buff} on.', 'gray')]),
                                    f'execute if score #poton{i} bm.cfg matches 0 run ' + tellraw('@a', PRE + [{'selector': '@s', 'color': 'white'}, T(f' switched {buff} off.', 'gray')]),
                                    'playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.3', f'function bm:p178/pots/page{i}'])
        fn(f'p178/pots/notyet{i}', [say(f'The {pot} isn\'t full yet.', '#c8a0a0'), f'function bm:p178/pots/page{i}'])
        act += [f'execute if score #act bm.pay matches {PMENU + 1 + i} run return run function bm:p178/pots/page{i}',
                f'execute if score #act bm.pay matches {PMENU + 30 + i} run return run function bm:p178/pots/toggle{i}']
    act.append(f'execute if score #act bm.pay matches {PMENU + 40} run return run function bm:p178/pots/open')
    fn('p178/pots/act', act)
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {PMENU}..{PMENU + 49} run return run function bm:p178/pots/act')
    fn('p178/pots/poor', [say('Not enough Tokens (in your pockets and the Rat Bank together).', 'red'), 'playsound minecraft:entity.villager.no player @s ~ ~ ~ 0.8 0.8'])
    # paying in Tokens: pockets first, then the bank (#need bm.pay set by the caller)
    fn('p178/paytok', [f'execute store result score #inv bm.pay run clear @s {holds("token")} 0',
                       'execute unless score @s bm.bk_tok matches 0.. run scoreboard players set @s bm.bk_tok 0',
                       'scoreboard players operation #all bm.pay = #inv bm.pay', 'scoreboard players operation #all bm.pay += @s bm.bk_tok',
                       'execute if score #all bm.pay < #need bm.pay run return 0',
                       'scoreboard players operation #ti bm.pay = #need bm.pay', 'scoreboard players operation #ti bm.pay < #inv bm.pay',
                       'execute store result storage bm:ui p178.k int 1 run scoreboard players get #ti bm.pay', 'function bm:p178/paytok_inv with storage bm:ui p178',
                       'scoreboard players operation #need bm.pay -= #ti bm.pay', 'scoreboard players operation @s bm.bk_tok -= #need bm.pay', 'return 1'])
    fn('p178/paytok_inv', [f'execute store result score #chk bm.pay run clear @s {holds("token")} 0', f'$clear @s {holds("token")} $(k)'])
    # the buffs (never in the gutter)
    on = lambda i: f'execute if score #poton{i} bm.cfg matches 1 as @a[gamemode=!spectator] at @s unless dimension bm:gutter run '
    second += [on(0) + 'execute if dimension minecraft:overworld if score #tod bm.bm matches 12500..23500 run effect give @s minecraft:night_vision 15 0 true',
               on(1) + 'effect give @s minecraft:luck 3 0 true', on(2) + 'effect give @s minecraft:haste 3 0 true', on(3) + 'effect give @s minecraft:speed 3 0 true',
               on(4) + 'execute unless score @s bm.potsw matches 1.. run function bm:p178/pots/wind',
               'scoreboard players remove @a[scores={bm.potsw=1..}] bm.potsw 1']
    fn('p178/pots/wind', ['execute store result score #hh bm.rng run data get entity @s Health', 'execute if score #hh bm.rng matches 6.. run return 0',
                          'effect give @s minecraft:regeneration 5 1 true', 'scoreboard players set @s bm.potsw 60',
                          'particle minecraft:totem_of_undying ~ ~1 ~ 0.4 0.6 0.4 0.2 16', say('Second Wind!', '#ffd27a')])
    wjson('bm/advancement/p178/purse.json', {'criteria': {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {
        'entity': [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:entity_type': '#bm:hostile'}}]}}}, 'rewards': {'function': 'bm:p178/pots/purse'}})
    fn('p178/pots/purse', ['advancement revoke @s only bm:p178/purse', 'execute unless score #poton5 bm.cfg matches 1 run return 0',
                           'execute if dimension bm:gutter run return 0', 'execute store result score #r bm.rng run random value 1..30',
                           'execute if score #r bm.rng matches 1 run ' + give('token'),
                           'execute if score #r bm.rng matches 1 run ' + say("Hunter's Purse: a Token!", '#ffd27a')])

    # ---------------------------------------------------------------- admin
    fn('admin/hard_lots', [give(f'inf_{k}') for k in INF] + [give(f'art_{k}') for k in ART] + [give(RELIC[d][0]) for d in RELIC])
    fn('admin/pots_fill', [f'scoreboard players set #pot{i} bm.cfg {goal}' for i, (k, pot, goal, buff, what) in enumerate(POTS)] +
       [f'function bm:p178/pots/unlock{i}' for i in range(len(POTS))])
    fn('admin/pots_reset', [f'scoreboard players set #{v}{i} bm.cfg 0' for i in range(len(POTS)) for v in ('pot', 'potu', 'poton')] +
       [tellraw('@s', PRE + [T('Community pots emptied and locked.', 'gray')])])
    G.FUNCS['admin/help'] += [tellraw('@s', [T('/function bm:admin/hard_lots', 'yellow'), T('  every infusion, artifact and dungeon relic', 'gray')]),
                              tellraw('@s', [T('/function bm:admin/pots_fill', 'yellow'), T(' / ', 'gray'), T('pots_reset', 'yellow'), T('  fill (and unlock) or empty the community pots', 'gray')])]


# ================================================================== sprites
VIAL = ['................', '......kkkk......', '......kccK......', '.......kk.......', '......kwwk......', '.....kwLLwk.....', '....kwLLLLwk....',
        '....kLLLLLLk....', '...kLLLLlLLLk...', '...kLLLllLLLk...', '...kLLLLLLLLk...', '...kDLLLLLLDk...', '....kDDDDDDk....', '.....kkkkkk.....',
        '................', '................']
AMULET = ['................', '......kkkk......', '.....k....k.....', '....k......k....', '....k......k....', '.....k....k.....', '......kGGk......',
          '.....kGRRGk.....', '....kGRWRRGk....', '....kGRRRRGk....', '....kGRRRRGk....', '.....kGRRGk.....', '......kGGk......', '.......kk.......',
          '................', '................']


def _dark(h, f=0.55):
    h = h.lstrip('#')
    return '#' + ''.join('%02x' % int(int(h[i:i + 2], 16) * f) for i in (0, 2, 4))


def rp(R):
    g = R.grid
    for k, (cls, nm, col, what) in INF.items():
        R.ICONS[f'inf_{k}'] = g(VIAL, dict(k='#1a1418', c='#8a5a2a', K='#5a3a1a', w='#e8f0ff', L=col, l='#ffffff', D=_dark(col)))
    gold = {'brood': '#8a6a2a', 'frost': '#c8d8e8', 'tide': '#c8a040', 'hex': '#c8a040', 'keep': '#7a6a5a', 'hollow': '#8a8aa0', 'lucky': '#ffd700'}
    for d, (iid, nm, col, lines, cmds) in RELIC.items():
        R.ICONS[iid] = g(AMULET, dict(k='#1a1418', G=gold[d], R=col, W='#ffffff'))
    A = {}
    A['crownshard'] = (['................', '................', '..k..k..........', '..kk.kk.........', '..kPkPPk........', '..kPPPPPk.......', '...kPpPPPk......',
                        '....kPPpPPk.....', '.....kPPPPPk....', '......kPPpPk....', '.......kPPk.....', '........kk......', '................', '................',
                        '................', '................'], dict(k='#2a2438', P='#9a8ab0', p='#d8d0f0'))
    A['starchart'] = (['................', '..pppppppppppp..', '..pBBBBBBBBBBp..', '..pBwBBBBBwBBp..', '..pBBBBcBBBBBp..', '..pBBBcBcBBBBp..', '..pBwBBcBBBwBp..',
                       '..pBBBBBBcBBBp..', '..pBBBBBBBcBBp..', '..pBBwBBBBBwBp..', '..pBBBBBBBBBBp..', '..pppppppppppp..', '................', '................',
                       '................', '................'], dict(p='#5a4a3a', B='#102a40', w='#ffffff', c='#5ad8ff'))
    A['bell'] = (['................', '.......kk.......', '......kGGk......', '.....kGGGGk.....', '.....kGgGGk.....', '....kGGgGGGk....', '....kGGGGGGk....',
                  '...kGGGGGGGGk...', '...kGGGGGGGGk...', '..kGGGGGGGGGGk..', '..kkkkkkkkkkkk..', '.......kk.......', '.......GG.......', '................',
                  '................', '................'], dict(k='#1a2a28', G='#2fa39b', g='#9ff0e0'))
    A['dreadheart'] = (['................', '................', '....kk...kk.....', '...kRRk.kRRk....', '..kRRRRkRrRRk...', '..kRRRRRRRRRk...', '..kRRsRRRRRRk...',
                        '...kRRRRsRRk....', '....kRRRRRk.....', '.....kRRRk......', '......kRk.......', '.......k........', '................', '................',
                        '................', '................'], dict(k='#1a0205', R='#5a3a3a', r='#b0102a', s='#8a7a7a'))
    A['ledger'] = (['................', '..kkkkkkkkkkk...', '..kYYYYYYYYYkw..', '..kYrrrrrrrYkw..', '..kYYYYYYYYYkw..', '..kYrrrrrYYYkw..', '..kYYYYYYYYYkw..',
                    '..kYrrrrrrYYkw..', '..kYYYYYGGYYkw..', '..kYYYYGooGYkw..', '..kYYYYYGGYYkw..', '..kkkkkkkkkkkw..', '...wwwwwwwwwww..', '................',
                    '................', '................'], dict(k='#4a2a10', Y='#e8c870', r='#5a3a1a', G='#ffb300', o='#fff0a0', w='#f0e8d0'))
    A['firstkey'] = (['................', '................', '...kkkk.........', '..kPPPPk........', '..kP..Pk........', '..kP..Pk........', '..kPPPPkkkkkkk..',
                      '...kkkkPPPPPPPk.', '.......kkPkPkk..', '........kPkPk...', '.........k.k....', '................', '................', '................',
                      '................', '................'], dict(k='#2a1a3a', P='#a96bff'))
    for k, (rows, pal) in A.items():
        R.ICONS[f'art_{k}'] = g(rows, pal)

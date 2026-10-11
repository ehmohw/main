"""2.65: THE VAULT'S NEW ROOMS, SECRETS AND RARITIES (templates: phase76_rooms; the heist itself: phase70/phase75).

NEW ROOMS (drawn by tier - each tier has its own set, see phase75.TIER_POOL)
  THE SIGNAL LAMPS     watch four coloured lamps flash a sequence, then press their buttons in the same order.
  THE LAMP FLOOR       nine lamps in the floor; each desk button flips its lamp and the ones beside it. Light them all.
  THE TUMBLER LOCK     a light runs along the wall: press the button as it passes the gold gate, three times running.
  THE BELL TOWER       a climb round a bell column to a landing ten blocks up - the way on is up there.
  THE CRUMBLING RAFTERS beams over a pit that give way a moment after you step on them.
  THE ARCANE STUDY     quiet... until the door slams and the casters appear. Two waves.
  THE CHAMPION'S PIT   a champion steps out: the Gold Ooze, the Bone Duelist, the Vault Ravager, the Illusionist, the
                       Twin Gales - and, very rarely, THE RAT KING.
RANDOM EVENTS (now and then a room is one of these instead)
  THE RAT RAVE         a dance-off: the DJ calls a colour, be standing on it when the beat drops. Six rounds.
  THE RATS' REST       a tavern: rest, a peddler, and if you're knocked out after this you wake HERE.
  THE STORM VAULT      lightning (watch for the sparks) and breezes - pull the three levers on the copper pillars.
  THE VORN LANDING     a Vorn saucer: smash its three power cores while the troopers pour out.
  THE ENCHANTED GROVE  catch four wisps; the grove's sprites don't like it.
SECRETS: a room may hide a LOOSE BRICK (a cracked wall block - right-click it): coins for the pot, maybe a rare find,
  maybe a PHANTOM THIEF who runs off with the pot until you catch him. The Cipher Monocle shows loose bricks close by,
  the Lantern of Lost Things from across the room, and a Treasure Map Scrap marks every one in the heist.
RARE FOES: the COIN RAT (now and then, in any room - fast, and worth a fortune), SHINY guards (1 in 150 - rare loot).
HIDDEN THINGS (only from rare foes, secrets and champions): the PHANTOM REGALIA (four pieces; all four: invisible
  while you sneak, and you fall softly), the GUTTER MASTER KEY (beats a puzzle room, every ten minutes), the LANTERN OF
  LOST THINGS, the LUCKY RAT'S FOOT (luck; +1 share of every haul).
GOLDTOOTH (and the rest's peddler) sells: Healing Draughts, a SECOND WIND (+1 try, once a heist each), a TREASURE MAP
  SCRAP, the GOLDEN COMPASS (shows the way to the next locked door) and the FIXER'S LUCKY PURSE (+2 shares, once)."""
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, D, Int
import phase70 as P70
import phase70_rooms as RM
import phase72 as P72
import phase75 as P75
import phase76_rooms as R6

GOLD = '#ffcf40'
LUCKY = '#7dff6a'
PH = '#8a5adf'
NEW_ROOMS = ['lamps', 'lightsout', 'tumbler', 'climb', 'rafters', 'ambush', 'pit']
EVENTS = ['rave', 'rest', 'storm', 'ufo', 'grove']
PUZZLES = ['levers', 'plates', 'lasers', 'tiles', 'dial', 'coffers', 'lamps', 'lightsout', 'tumbler', 'climb', 'rafters']
NOPICK = ['ambush', 'pit'] + EVENTS
SECRET_KINDS = ['levers', 'plates', 'tiles', 'dial', 'guards', 'coffers', 'lamps', 'lightsout', 'tumbler', 'rafters', 'pit']

# ---------------------------------------------------------------- the layout learns the new rooms (before phase75 generates)
P75.KINDS += NEW_ROOMS
P75.SIZE['climb'] = (25, R6.CLIMB_H, 25)
P75.ROOM_DY['climb'] = R6.CLIMB_EXIT - 4
P75.ROOM_MAXY['climb'] = P75.Y0 + 5
for _k in NEW_ROOMS + EVENTS:
    P75.EXTRA_ROOMS[_k] = R6.BUILDERS[_k]
P75.TIER_POOL.update({
    1: ['levers', 'plates', 'tiles', 'coffers', 'lamps', 'rafters', 'guards'],
    2: ['levers', 'dial', 'coffers', 'lamps', 'lightsout', 'tumbler', 'ambush', 'rafters'],
    3: ['lasers', 'tiles', 'coffers', 'dial', 'plates', 'lightsout', 'climb', 'ambush', 'pit'],
    4: ['lasers', 'dial', 'coffers', 'lightsout', 'tumbler', 'climb', 'ambush', 'pit', 'rafters'],
    5: ['lasers', 'dial', 'coffers', 'tumbler', 'lightsout', 'climb', 'ambush', 'pit', 'rafters', 'lamps']})
P75.EVENT_POOL.update({1: ['rest', 'rave', 'grove'], 2: ['rest', 'rave', 'storm', 'grove'], 3: ['rest', 'rave', 'ufo', 'grove', 'storm'],
                       4: ['rest', 'storm', 'ufo', 'grove', 'rave'], 5: ['rest', 'storm', 'ufo', 'rave', 'grove']})

# ---------------------------------------------------------------- items: heist tools (Goldtooth) and hidden finds
item('healing_draught', 'minecraft:potion', 'Healing Draught', '#ff5a7a', ['A gutter apothecary\'s finest.', ('Drink: instant healing II.', 'blue')],
     comps={'minecraft:potion_contents': {'potion': 'minecraft:strong_healing', 'custom_color': 0xff5a7a}}, cat='potion')
item('second_wind', TOTEM, 'Second Wind', '#ff7a7a', ['A pinch of something that gets you up again.', ('Use in a heist: your crew gets one', 'blue'),
                                                    ('more try. (Once a heist each.)', 'blue')], model='minecraft:totem_of_undying', glint=True, stack=8, cat='magic', comps=hold('none'))
HOLD['second_wind'] = 'bm:p76/item/second_wind'
item('treasure_map_scrap', TOTEM, 'Treasure Map Scrap', '#d9a066', ['A torn corner of a vault plan, scribbled on.', ('Use in a heist: every loose brick', 'blue'),
                                                                     ('in it glows for a minute.', 'blue')], model='minecraft:map', stack=16, cat='misc', comps=hold('none'))
HOLD['treasure_map_scrap'] = 'bm:p76/item/map'
item('golden_compass', TOTEM, 'Golden Compass', GOLD, ['It never points north.', ('Use in a heist: a trail of gold leads', 'blue'), ('to the next locked door.', 'blue')],
     model='minecraft:compass', glint=True, stack=1, cat='misc', comps=hold('none'))
HOLD['golden_compass'] = 'bm:p76/item/compass'
item('lucky_purse', TOTEM, "Fixer's Lucky Purse", LUCKY, ['Empty. For now.', ('Carry it when a heist is won:', 'blue'), ('+2 shares for you (it\'s used up).', 'blue')],
     model='minecraft:bundle', stack=4, cat='misc')
PHANTOM = [('phantom_hood', 'leather_helmet', 'Phantom Hood', 'head', 3), ('phantom_mantle', 'leather_chestplate', 'Phantom Mantle', 'chest', 8),
           ('phantom_greaves', 'leather_leggings', 'Phantom Greaves', 'legs', 6), ('phantom_treads', 'leather_boots', 'Phantom Treads', 'feet', 3)]
for _iid, _base, _nm, _slot, _arm in PHANTOM:
    _mods = [{'type': 'minecraft:armor', 'id': f'bm:{_iid}', 'amount': float(_arm), 'operation': 'add_value', 'slot': _slot},
             {'type': 'minecraft:armor_toughness', 'id': f'bm:{_iid}_t', 'amount': 2.0, 'operation': 'add_value', 'slot': _slot},
             {'type': 'minecraft:movement_speed', 'id': f'bm:{_iid}_s', 'amount': 0.05, 'operation': 'add_multiplied_base', 'slot': _slot}]
    if _slot == 'feet':
        _mods.append({'type': 'minecraft:safe_fall_distance', 'id': f'bm:{_iid}_f', 'amount': 6.0, 'operation': 'add_value', 'slot': _slot})
    item(_iid, f'minecraft:{_base}', _nm, PH, ['Woven from a vault ghost\'s shadow.', ('PHANTOM REGALIA (one of four)', PH), ('Quick on your feet.', 'blue'),
                                             ('All four: invisible while you sneak,', 'blue'), ('and you fall softly.', 'blue'), ('Hidden: only rare foes carry it.', 'dark_gray')],
         glint=True, cat='armor', comps={'minecraft:dyed_color': 0x3a1a5a, 'minecraft:unbreakable': {}, 'minecraft:attribute_modifiers': _mods,
                                        'minecraft:tooltip_display': {'hidden_components': ['minecraft:dyed_color']}})
item('master_key', TOTEM, 'Gutter Master Key', GOLD, ['The Fixer would pay a fortune for this.', ('Use in a heist puzzle room: beat it', 'blue'),
                                                      ('(no flawless bonus). Every ten minutes.', 'blue'), ('Hidden: only rare foes carry it.', 'dark_gray')],
     model='minecraft:ominous_trial_key', glint=True, stack=1, cat='misc', comps=hold('none'))
HOLD['master_key'] = 'bm:p76/item/master_key'
item('lost_lantern', TOTEM, 'Lantern of Lost Things', '#7ad0ff', ['It flickers toward what\'s hidden.', ('Held in the vault: loose bricks', 'blue'),
                                                                   ('shimmer from across the room.', 'blue'), ('Hidden: only rare foes carry it.', 'dark_gray')],
     model='minecraft:soul_lantern', glint=True, stack=1, cat='magic')
item('rats_foot', TOTEM, "Lucky Rat's Foot", LUCKY, ['Lucky for you. Less so for the rat.', ('Carried: Luck.', 'blue'), ('+1 share of every heist haul.', 'blue'),
                                                    ('Hidden: only rare foes carry it.', 'dark_gray')], model='minecraft:rabbit_foot', glint=True, stack=1, cat='magic')
P72.KEEP += ['second_wind', 'treasure_map_scrap', 'golden_compass', 'lucky_purse', 'healing_draught', 'master_key', 'lost_lantern', 'rats_foot']
P70.GOLDTOOTH_STOCK += [(8, 'healing_draught', 2), (40, 'second_wind', 1), (24, 'treasure_map_scrap', 1), (30, 'golden_compass', 1), (36, 'lucky_purse', 1)]
PEDDLER = [(6, 'healing_draught', 2), (32, 'second_wind', 1), (18, 'treasure_map_scrap', 1), (4, 'minecraft:cooked_beef', 8), (12, 'minecraft:golden_carrot', 4)]

LAMPS_X, LAMP_COL = R6.LAMPS_X, R6.LAMP_COL
CASTERS = {   # the Arcane Study's casters by tier
    1: [('witch', 'Hex Witch', '#b080ff')],
    2: [('witch', 'Hex Witch', '#b080ff'), ('illusioner', 'Illusionist', '#5a8aff')],
    3: [('illusioner', 'Illusionist', '#5a8aff'), ('witch', 'Hex Witch', '#b080ff'), ('evoker', 'Gutter Evoker', '#c060ff')],
    4: [('evoker', 'Gutter Evoker', '#c060ff'), ('illusioner', 'Illusionist', '#5a8aff'), ('witch', 'Hex Witch', '#b080ff')],
    5: [('evoker', 'Gutter Evoker', '#c060ff'), ('evoker', 'Gutter Evoker', '#c060ff'), ('illusioner', 'Illusionist', '#5a8aff')]}
CHAMPS = [   # weight, key, type, name, colour, extra nbt, attributes
    (6, 'ooze', 'magma_cube', 'The Gold Ooze', GOLD, {'Size': Int(3)}, {}),
    (6, 'duelist', 'wither_skeleton', 'The Bone Duelist', '#d0d0d0', {'equipment': {'mainhand': {'id': 'minecraft:netherite_sword', 'count': Int(1)},
                                                                                   'head': {'id': 'minecraft:golden_helmet', 'count': Int(1)}}},
     {'scale': 1.3, 'movement_speed': 0.32}),
    (5, 'ravager', 'ravager', 'The Vault Ravager', '#c06040', {}, {}),
    (5, 'illusionist', 'illusioner', 'The Illusionist', '#5a8aff', {}, {}),
    (4, 'gales', 'breeze', 'The Twin Gales', '#c0e0ff', {}, {}),
    (1, 'ratking', 'zombie', 'THE RAT KING', '#ffd040', {'IsBaby': B(0), 'Silent': B(1),
                                                        'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0)}]},
     {'spawn_reinforcements': 0.0, 'scale': 1.25, 'movement_speed': 0.3})]


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    P = [T('[Heist] ', GOLD, bold=True)]
    rel = RM.rel
    tick, fast, second = [], [], []
    ident = [F(0), F(0), F(0), F(1)]
    objs = ['bm.gvsw', 'bm.gvmk', 'bm.gvl', 'bm.gvh', 'bm.gvstl']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + \
        [f'scoreboard players set #pw{i} bm.rng {4 ** i}' for i in range(8)] + [f'scoreboard players set #pb{i} bm.rng {2 ** i}' for i in range(9)] + \
        ['scoreboard players set #4 bm.rng 4', 'scoreboard players set #16 bm.rng 16']
    G.OBJECTIVES += objs
    def label(x, y, z, text, scale=0.55, bill='center', extra_tags=()):
        return f'summon minecraft:text_display {rel(x, y, z)} ' + snbt({'Tags': ['bm.gvprop'] + list(extra_tags), 'billboard': bill, 'brightness': {'block': 15, 'sky': 15},
                                                                       'background': Int(0x90000000 - 2 ** 32), 'text': text, 'alignment': 'center', 'line_width': Int(220),
                                                                       'transformation': {'left_rotation': ident, 'right_rotation': ident,
                                                                                          'translation': [F(0)] * 3, 'scale': [F(scale)] * 3}})
    def sign(x, y, z, title_, body, rot=None):
        return label(x, y, z, [T(title_ + '\n', GOLD, bold=True), T(body, 'gray')], 0.6, 'vertical')
    def vbutton(x, y, z, facing, text, face='wall', col=GOLD):
        return [f'setblock {rel(x, y, z)} minecraft:pale_oak_button[face={face},facing={facing},powered=false]',
                label(x, y + (0.7 if face == 'wall' else 0.55), z, T(text, col, bold=True), 0.45)]
    btn = lambda x, y, z: f'minecraft:pale_oak_button[powered=true]'
    inst = lambda f: f'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run function {f}'
    crew = '@a[tag=bm.gvp,distance=..30]'
    def press(name, pos, then):
        """lines: a pale oak button at pos (local) pressed -> run `then` once (latched until it pops back out)"""
        return [f'execute if block {rel(*pos)} minecraft:pale_oak_button[powered=true] unless entity @s[tag=bm.gvl_{name}] run function {then}',
                f'execute if block {rel(*pos)} minecraft:pale_oak_button[powered=true] run tag @s add bm.gvl_{name}',
                f'execute unless block {rel(*pos)} minecraft:pale_oak_button[powered=true] run tag @s remove bm.gvl_{name}']
    room_ctx = 'scoreboard players operation #gt bm.rng = @s bm.gvt'
    # (every room remembers its tier, for the rooms that need it every tick)
    G.FUNCS['p70/claim_room'] += ['scoreboard players operation @s bm.gvt = #gt bm.rng']

    # ================================================================== dispatch, names, the solve, the lockpick
    G.FUNCS['p70/r/init'] += [f'execute if entity @s[tag=bm.gvr_{k}] run return run function bm:p76/r/{k}/init' for k in NEW_ROOMS + EVENTS]
    G.FUNCS['p70/r/tick'] += [f'execute if entity @s[tag=bm.gvr_{k}] run return run function bm:p76/r/{k}/tick' for k in NEW_ROOMS + EVENTS]
    G.FUNCS['p70/solved'] += [f'execute if entity @s[tag=bm.gvr_{k}] as @a[tag=bm.gvp,distance=..300] if score @s bm.gvi = #gi bm.rng run ' +
                              title('@s', 'actionbar', [T(R6.NAMES[k], GOLD, bold=True), T(' - beaten. The way on is open.', 'gray')]) for k in NEW_ROOMS + EVENTS] + \
                             ['execute if entity @s[tag=bm.gvr_climb] run function bm:p76/r/climb/open'] + \
                             [f'execute if entity @s[tag=bm.gvr_{k}] if score @s bm.gvf matches 0 run function bm:p76/flawless' for k in NEW_ROOMS if k not in ('ambush', 'pit')]
    fn('p76/flawless', ['scoreboard players set #c bm.rng 5', inst('bm:p75/pot_add'),
                        'execute as @a[tag=bm.gvp,distance=..300] if score @s bm.gvi = #gi bm.rng run ' + say('Flawless! 5 coins into the pot.', GOLD)])
    for f_ in ('p71/pick', 'p71/rig'):
        if f_ in G.FUNCS:
            G.FUNCS[f_] = [l.replace("tag=!bm.gvr_guards,", "tag=!bm.gvr_guards,tag=!bm.gvnopick,") for l in G.FUNCS[f_]]
    nopick = [f'execute if entity @s[tag=bm.gvr_{k}] run tag @s add bm.gvnopick' for k in NOPICK] + [f'execute if entity @s[tag=bm.gvr_{k}] run tag @s add bm.gvpuz' for k in PUZZLES]
    G.FUNCS['p70/r/init'][0:0] = nopick + ['function bm:p76/secret/maybe']

    # ================================================================== THE SIGNAL LAMPS
    def lamp(i, on):
        return f'setblock {rel(LAMPS_X[i], 7, 0)} minecraft:redstone_lamp[lit={"true" if on else "false"}] strict'
    fn('p76/r/lamps/init', ['function bm:p70/ctx', 'scoreboard players operation @s bm.gvt = #gt bm.rng',
                            'scoreboard players operation @s bm.gvx = #gt bm.rng', 'scoreboard players add @s bm.gvx 1', 'scoreboard players operation @s bm.gvx /= #2 bm.rng',
                            'scoreboard players add @s bm.gvx 3', 'scoreboard players set @s bm.gvc 0'] +
       sum(([f'execute store result score #d bm.rng run random value 0..3', f'scoreboard players operation #d bm.rng *= #pw{i} bm.rng',
             'scoreboard players operation @s bm.gvc += #d bm.rng'] for i in range(8)), []) +
       sum((vbutton(x, 5, 1, 'south', LAMP_COL[i].upper(), col={'red': '#ff5050', 'blue': '#5a8aff', 'lime': '#7dff6a', 'yellow': '#ffe050'}[LAMP_COL[i]])
            for i, x in enumerate(LAMPS_X)), []) +
       [sign(12, 10.4, 1.5, 'THE SIGNAL LAMPS', 'Watch the lamps flash - then press their buttons in the same order.')])
    lt = ['execute if score @s bm.gvs matches 3 run return 0',
          'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..9] run function bm:p76/r/lamps/start',
          'execute if score @s bm.gvs matches 1 run function bm:p76/r/lamps/show', 'execute if score @s bm.gvs matches 2 run function bm:p76/r/lamps/input']
    fn('p76/r/lamps/tick', lt)
    fn('p76/r/lamps/start', ['scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvtm 0', 'scoreboard players set @s bm.gvw 0'] + [lamp(i, False) for i in range(4)])
    show = []
    for i in range(8):
        show += [f'execute if score @s bm.gvtm matches {24 + 16 * i} if score @s bm.gvx matches {i + 1}.. run function bm:p76/r/lamps/flash{i}',
                 f'execute if score @s bm.gvtm matches {34 + 16 * i} run function bm:p76/r/lamps/dark']
    show += ['scoreboard players operation #end bm.rng = @s bm.gvx', 'scoreboard players operation #end bm.rng *= #16 bm.rng', 'scoreboard players add #end bm.rng 26',
             'execute if score @s bm.gvtm >= #end bm.rng run function bm:p76/r/lamps/your_turn']
    fn('p76/r/lamps/show', show)
    for i in range(8):
        fn(f'p76/r/lamps/flash{i}', ['scoreboard players operation #q bm.rng = @s bm.gvc', f'scoreboard players operation #q bm.rng /= #pw{i} bm.rng',
                                     'scoreboard players operation #q bm.rng %= #4 bm.rng'] +
           [f'execute if score #q bm.rng matches {j} run function bm:p76/r/lamps/lit{j}' for j in range(4)])
    for j in range(4):
        fn(f'p76/r/lamps/lit{j}', [lamp(j, True), f'playsound minecraft:block.note_block.bell block @a[distance=..24] {rel(LAMPS_X[j], 7, 1)} 1 {[0.7, 0.9, 1.1, 1.35][j]}',
                                    f'particle minecraft:end_rod {rel(LAMPS_X[j], 7, 1.2)} 0.2 0.2 0.1 0.01 6'])
    fn('p76/r/lamps/dark', [lamp(i, False) for i in range(4)])
    fn('p76/r/lamps/your_turn', ['scoreboard players set @s bm.gvs 2', 'scoreboard players set @s bm.gvw 0',
                                 'execute as @a[tag=bm.gvp,distance=..20] run ' + title('@s', 'actionbar', T('Your turn - press the buttons in order.', GOLD))])
    inp = []
    for j, x in enumerate(LAMPS_X):
        inp += press(f'lamp{j}', (x, 5, 1), f'bm:p76/r/lamps/press{j}')
        inp += [f'execute if block {rel(x, 5, 1)} minecraft:pale_oak_button[powered=true] run {lamp(j, True)}',
                f'execute unless block {rel(x, 5, 1)} minecraft:pale_oak_button[powered=true] run {lamp(j, False)}']
    fn('p76/r/lamps/input', inp)
    for j in range(4):
        fn(f'p76/r/lamps/press{j}', ['scoreboard players operation #q bm.rng = @s bm.gvc'] +
           [f'execute if score @s bm.gvw matches {i} run scoreboard players operation #q bm.rng /= #pw{i} bm.rng' for i in range(8)] +
           ['scoreboard players operation #q bm.rng %= #4 bm.rng',
            f'playsound minecraft:block.note_block.bell block @a[distance=..24] {rel(LAMPS_X[j], 7, 1)} 1 {[0.7, 0.9, 1.1, 1.35][j]}',
            f'execute unless score #q bm.rng matches {j} run return run function bm:p76/r/lamps/wrong',
            'scoreboard players add @s bm.gvw 1', 'execute if score @s bm.gvw >= @s bm.gvx run function bm:p70/solved'])
    fn('p76/r/lamps/wrong', ['scoreboard players set #add bm.rng 8', 'function bm:p70/oops', 'scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvtm 0',
                             'playsound minecraft:block.note_block.didgeridoo block @a[distance=..24] ~ ~ ~ 1 0.6',
                             f'particle minecraft:dust{{color:[1.0,0.1,0.1],scale:1.5}} {rel(12, 7, 1)} 5 1 0.2 0 40',
                             'execute as @a[tag=bm.gvp,distance=..20] run ' + title('@s', 'actionbar', T('Wrong lamp! Watch again...', 'red'))])

    # ================================================================== THE LAMP FLOOR (lights out)
    def cells(i, j):
        return [(i, j)] + [(a, b) for a, b in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)) if 0 <= a < 3 and 0 <= b < 3]
    fn('p76/r/lightsout/init', ['function bm:p70/ctx', 'scoreboard players operation @s bm.gvt = #gt bm.rng', 'scoreboard players set @s bm.gvc 511',
                                'scoreboard players operation #k bm.rng = #gt bm.rng', 'scoreboard players add #k bm.rng 2', 'function bm:p76/r/lightsout/scramble',
                                'execute if score @s bm.gvc matches 511 run function bm:p76/r/lightsout/p4',
                                'scoreboard players operation @s bm.gvx = @s bm.gvc', 'function bm:p76/r/lightsout/draw'] +
       [f'setblock {rel(*R6.LO_BTN(i, j))} minecraft:pale_oak_button[face=floor,facing=east,powered=false]' for i in range(3) for j in range(3)] +
       vbutton(5, 5, 9, 'east', 'RESET', 'floor', '#ff7a7a') +
       [sign(6, 7.5, 12, 'THE LAMP FLOOR', 'Each button flips its lamp - and the lamps beside it. Light them all.')])
    fn('p76/r/lightsout/scramble', ['execute if score #k bm.rng matches ..0 run return 0', 'execute store result score #b bm.rng run random value 0..8'] +
       [f'execute if score #b bm.rng matches {b} run function bm:p76/r/lightsout/p{b}' for b in range(9)] +
       ['scoreboard players remove #k bm.rng 1', 'function bm:p76/r/lightsout/scramble'])
    for b in range(9):
        fn(f'p76/r/lightsout/t{b}', ['scoreboard players operation #q bm.rng = @s bm.gvc', f'scoreboard players operation #q bm.rng /= #pb{b} bm.rng',
                                     'scoreboard players operation #q bm.rng %= #2 bm.rng',
                                     f'execute if score #q bm.rng matches 1 run return run scoreboard players remove @s bm.gvc {2 ** b}', f'scoreboard players add @s bm.gvc {2 ** b}'])
        i, j = b % 3, b // 3
        fn(f'p76/r/lightsout/p{b}', [f'function bm:p76/r/lightsout/t{a + 3 * c}' for a, c in cells(i, j)])
    draw = []
    for b in range(9):
        i, j = b % 3, b // 3
        x0, z0 = R6.LO_CELL(i, j)
        draw += ['scoreboard players operation #q bm.rng = @s bm.gvc', f'scoreboard players operation #q bm.rng /= #pb{b} bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng',
                 f'execute if score #q bm.rng matches 1 run fill {rel(x0, 3, z0)} {rel(x0 + 2, 3, z0 + 2)} minecraft:redstone_lamp[lit=true] strict',
                 f'execute if score #q bm.rng matches 0 run fill {rel(x0, 3, z0)} {rel(x0 + 2, 3, z0 + 2)} minecraft:redstone_lamp[lit=false] strict']
    fn('p76/r/lightsout/draw', draw)
    lo = ['execute if score @s bm.gvs matches 3 run return 0', 'execute if score @s bm.gvs matches 0 run scoreboard players set @s bm.gvs 1',
          'execute if score @s bm.gvtm matches 2400 run scoreboard players set @s bm.gvf 1']
    for b in range(9):
        lo += press(f'lo{b}', R6.LO_BTN(b % 3, b // 3), f'bm:p76/r/lightsout/push{b}')
    lo += press('lor', (5, 5, 9), 'bm:p76/r/lightsout/reset')
    fn('p76/r/lightsout/tick', lo)
    for b in range(9):
        fn(f'p76/r/lightsout/push{b}', [f'function bm:p76/r/lightsout/p{b}', 'function bm:p76/r/lightsout/draw',
                                        'playsound minecraft:block.stone_button.click_on block @a[distance=..20] ~ ~ ~ 1 1.4',
                                        'execute if score @s bm.gvc matches 511 run function bm:p70/solved'])
    fn('p76/r/lightsout/reset', ['scoreboard players operation @s bm.gvc = @s bm.gvx', 'function bm:p76/r/lightsout/draw', 'scoreboard players set @s bm.gvf 1',
                                 'scoreboard players set #add bm.rng 4', 'function bm:p70/oops',
                                 'execute as @a[tag=bm.gvp,distance=..20] run ' + title('@s', 'actionbar', T('The floor clicks back to how it was. (A bell rings.)', 'gray'))])

    # ================================================================== THE TUMBLER LOCK
    TX = R6.TUMB_X
    fn('p76/r/tumbler/init', ['function bm:p70/ctx', 'scoreboard players operation @s bm.gvt = #gt bm.rng', 'scoreboard players set @s bm.gvc 0', 'scoreboard players set @s bm.gvw 0'] +
       vbutton(12, 5, 2, 'south', 'PULL THE PIN', 'floor') +
       [sign(12, 10.6, 1.5, 'THE TUMBLER LOCK', 'Press as the light crosses the gold gate - three times running.')])
    tt = ['execute if score @s bm.gvs matches 3 run return 0', 'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..12] run scoreboard players set @s bm.gvs 1',
          'execute if score @s bm.gvs matches 0 run return 0',
          # the step period: 6 / 4 / 3 ticks by successes (5 / 3 / 2 on tiers IV-V)
          'scoreboard players set #sp bm.rng 6', 'execute if score @s bm.gvw matches 1 run scoreboard players set #sp bm.rng 4',
          'execute if score @s bm.gvw matches 2.. run scoreboard players set #sp bm.rng 3', 'execute if score @s bm.gvt matches 4.. run scoreboard players remove #sp bm.rng 1',
          'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #sp bm.rng',
          'execute if score #q bm.rng matches 0 run function bm:p76/r/tumbler/step'] + press('tumb', (12, 5, 2), 'bm:p76/r/tumbler/try')
    fn('p76/r/tumbler/tick', tt)
    fn('p76/r/tumbler/step', ['scoreboard players add @s bm.gvc 1', 'execute if score @s bm.gvc matches 16.. run scoreboard players set @s bm.gvc 0',
                              f'fill {rel(TX[0], 7, 0)} {rel(TX[-1], 7, 0)} minecraft:redstone_lamp[lit=false] strict'] +
       [f'execute if score @s bm.gvc matches {p} run setblock {rel(TX[p if p < 9 else 16 - p], 7, 0)} minecraft:redstone_lamp[lit=true] strict' for p in range(16)])
    fn('p76/r/tumbler/try', ['execute unless score @s bm.gvc matches 4 unless score @s bm.gvc matches 12 run return run function bm:p76/r/tumbler/miss',
                             'scoreboard players add @s bm.gvw 1', 'playsound minecraft:block.iron_trapdoor.open block @a[distance=..20] ~ ~ ~ 1 1.5',
                             f'particle minecraft:wax_on {rel(TX[4], 7, 1)} 0.3 0.3 0.1 0 20',
                             'execute as @a[tag=bm.gvp,distance=..20] run ' + title('@s', 'actionbar', [T('Click! ', GOLD, bold=True), {'score': {'name': '@e[type=marker,tag=bm.gvr_tumbler,limit=1,sort=nearest]', 'objective': 'bm.gvw'}, 'color': 'white'},
                                                                                                       T(' of 3', 'gray')]),
                             'execute if score @s bm.gvw matches 3.. run function bm:p70/solved'])
    fn('p76/r/tumbler/miss', ['scoreboard players set @s bm.gvw 0', 'scoreboard players set #add bm.rng 5', 'function bm:p70/oops', 'scoreboard players set @s bm.gvf 1',
                              'playsound minecraft:block.note_block.basedrum block @a[distance=..20] ~ ~ ~ 1 0.5',
                              'execute as @a[tag=bm.gvp,distance=..20] run ' + title('@s', 'actionbar', T('Missed - the tumblers fall back. (Start again.)', 'red'))])

    # ================================================================== THE BELL TOWER
    up = R6.CLIMB_EXIT
    fn('p76/r/climb/init', ['function bm:p70/ctx', sign(2.5, 7.5, 12, 'THE BELL TOWER', 'The way on is at the top. Mind the drop.')])
    fn('p76/r/climb/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'execute if score @s bm.gvs matches 0 run scoreboard players set @s bm.gvs 1',
                            'execute if score @s bm.gvtm matches 2400 run scoreboard players set @s bm.gvf 1',
                            f'execute unless block {rel(21, up, 12)} minecraft:light_weighted_pressure_plate[power=0] run function bm:p70/solved',
                            f'execute if score @s bm.gvtm matches 100 run playsound minecraft:block.bell.use block @a[distance=..30] {rel(12, 22, 12)} 1 0.6'])
    fn('p76/r/climb/open', [f'fill {rel(24, up, 11)} {rel(24, up + 3, 13)} minecraft:air replace minecraft:iron_bars',
                            f'playsound minecraft:block.bell.resonate block @a[distance=..40] {rel(12, 22, 12)} 1 1',
                            'execute as @e[type=minecraft:marker,tag=bm.gvcp] if score @s bm.gvi = #gi bm.rng run tp @s ' + rel(25, up, 12) + ' -90 0'])

    # ================================================================== THE CRUMBLING RAFTERS
    fn('p76/r/rafters/init', ['function bm:p70/ctx', 'scoreboard players operation @s bm.gvt = #gt bm.rng'] +
       [f'summon minecraft:marker {rel(x, 4, z)} {{Tags:["bm.gvraf","bm.gvprop"]}}' for (x, z) in R6.RAFT] +
       ['execute as @e[type=minecraft:marker,tag=bm.gvraf,distance=..16] run scoreboard players set @s bm.gvx 0',
        sign(1.5, 7.5, 12, 'THE CRUMBLING RAFTERS', 'Old beams. Don\'t stand still.')])
    fn('p76/r/rafters/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'execute if score @s bm.gvs matches 0 run scoreboard players set @s bm.gvs 1', room_ctx,
                              'execute as @e[type=minecraft:marker,tag=bm.gvraf,distance=..16] at @s run function bm:p76/r/rafters/beam',
                              f'execute positioned {rel(3, 0, 1)} positioned ~-0.5 ~-0.5 ~-0.5 as @a[tag=bm.gvp,dx=18,dy=2.4,dz=22] at @s run function bm:p76/r/rafters/fell',
                              f'execute positioned {rel(22, 4, 12)} if entity @a[tag=bm.gvp,distance=..1.2] positioned as @s run function bm:p70/solved'])
    fn('p76/r/rafters/beam', ['execute if score @s bm.gvx matches 0 positioned ~ ~0.05 ~ if entity @a[tag=bm.gvp,distance=..0.85] run function bm:p76/r/rafters/creak',
                              'execute if score @s bm.gvx matches 2.. run scoreboard players remove @s bm.gvx 1',
                              'execute if score @s bm.gvx matches 1 run function bm:p76/r/rafters/drop',
                              'execute if score @s bm.gvx matches ..-2 run scoreboard players add @s bm.gvx 1',
                              'execute if score @s bm.gvx matches -1 run function bm:p76/r/rafters/back'])
    fn('p76/r/rafters/creak', ['scoreboard players set @s bm.gvx 14', 'execute if score #gt bm.rng matches 4.. run scoreboard players set @s bm.gvx 9',
                               'playsound minecraft:block.wood.break block @a[distance=..16] ~ ~ ~ 0.6 0.6', 'particle minecraft:block{block_state:"minecraft:dark_oak_planks"} ~ ~-0.2 ~ 0.3 0.1 0.3 0 8'])
    fn('p76/r/rafters/drop', ['setblock ~ ~-1 ~ minecraft:air', 'scoreboard players set @s bm.gvx -70', 'playsound minecraft:block.wood.fall block @a[distance=..16] ~ ~ ~ 1 0.5',
                              'particle minecraft:block{block_state:"minecraft:dark_oak_planks"} ~ ~-0.5 ~ 0.3 0.2 0.3 0 15'])
    fn('p76/r/rafters/back', ['scoreboard players set @s bm.gvx 0'] +
       [f'execute if score #gt bm.rng matches {t} run setblock ~ ~-1 ~ {__import__("phase75_rooms").THEMES[t]["trim"]}' for t in range(1, 6)])
    fn('p76/r/rafters/fell', ['scoreboard players set #add bm.rng 4', 'execute as @e[type=minecraft:marker,tag=bm.gvr_rafters,distance=..24,sort=nearest,limit=1] at @s run function bm:p70/oops',
                              'execute at @e[type=minecraft:marker,tag=bm.gvr_rafters,distance=..24,sort=nearest,limit=1] run tp @s ' + rel(1, 4, 12) + ' -90 0',
                              'playsound minecraft:block.grass.fall player @a[distance=..16] ~ ~ ~ 1 0.8', say('Down into the hay! Back to the start.', 'red')])

    # ================================================================== THE ARCANE STUDY (an ambush)
    AMB = [(5, 4, 5), (19, 4, 5), (5, 4, 19), (19, 4, 19), (12, 4, 4), (12, 4, 20)]
    fn('p76/r/ambush/init', ['function bm:p70/ctx', sign(2.5, 7.5, 12, 'THE ARCANE STUDY', 'Hush. Something reads in here.')])
    fn('p76/r/ambush/tick', ['execute if score @s bm.gvs matches 3 run return 0',
                             f'execute if score @s bm.gvs matches 0 positioned {rel(11, 4, 1)} if entity @a[tag=bm.gvp,dx=12,dy=4,dz=22] at @s run function bm:p76/r/ambush/spring',
                             'execute if score @s bm.gvs matches 1..2 run function bm:p76/r/ambush/fight'])
    fn('p76/r/ambush/spring', ['scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvtm 0', 'scoreboard players set @s bm.gvh 0',
                               f'fill {rel(0, 4, 11)} {rel(0, 7, 13)} minecraft:iron_bars', f'playsound minecraft:block.iron_door.close block @a[distance=..30] {rel(0, 5, 12)} 1 0.5',
                               'title @a[tag=bm.gvp,distance=..20] times 5 40 10',
                               title('@a[tag=bm.gvp,distance=..20]', 'title', T('AMBUSH!', '#c060ff', bold=True)), title('@a[tag=bm.gvp,distance=..20]', 'subtitle', T('The casters were waiting', 'gray')),
                               'function bm:p76/r/ambush/wave'])
    fn('p76/r/ambush/wave', ['function bm:p70/ctx', 'execute store result score #n bm.rng if entity @a[tag=bm.gvp,distance=..20]', 'scoreboard players operation #n bm.rng += #gt bm.rng',
                             'execute if score #n bm.rng matches 7.. run scoreboard players set #n bm.rng 6'] +
       [f'execute if score #n bm.rng matches {i + 1}.. positioned {rel(*AMB[i])} run function bm:p76/caster' for i in range(6)] +
       ['playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..30] ~ ~ ~ 1 0.8'])
    fn('p76/caster', ['particle minecraft:witch ~ ~1 ~ 0.4 0.8 0.4 0 30', 'execute store result score #rr bm.rng run random value 0..2'] +
       [f'execute if score #gt bm.rng matches {t} if score #rr bm.rng matches {j} run summon minecraft:{ty} ~ ~ ~ {snbt(P75._mob(ty, nm, col, {})[1])}'
        for t, lst in CASTERS.items() for j, (ty, nm, col) in enumerate((lst * 3)[:3])] +
       ['function bm:p70/guard_set'])
    fn('p76/r/ambush/fight', ['scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #20 bm.rng', 'execute unless score #q bm.rng matches 0 run return 0',
                              # (the whole crew knocked out: the trap resets so nobody's shut out)
                              'execute unless entity @a[tag=bm.gvp,distance=..14] run scoreboard players add @s bm.gvh 1',
                              'execute if entity @a[tag=bm.gvp,distance=..14] run scoreboard players set @s bm.gvh 0',
                              'execute if score @s bm.gvh matches 10.. run return run function bm:p76/r/ambush/rearm',
                              'execute store result score #n bm.rng if entity @e[tag=bm.gvg,distance=..16]', 'execute if score #n bm.rng matches 1.. run return 0',
                              'execute if score @s bm.gvs matches 1 run return run function bm:p76/r/ambush/wave2',
                              f'fill {rel(0, 4, 11)} {rel(0, 7, 13)} minecraft:air replace minecraft:iron_bars', 'function bm:p70/solved'])
    fn('p76/r/ambush/wave2', ['scoreboard players set @s bm.gvs 2', 'function bm:p76/r/ambush/wave',
                              'execute as @a[tag=bm.gvp,distance=..20] run ' + title('@s', 'actionbar', T('More of them!', '#c060ff'))])
    fn('p76/r/ambush/rearm', ['scoreboard players set @s bm.gvs 0', 'scoreboard players set @s bm.gvh 0', 'kill @e[tag=bm.gvg,distance=..16]',
                              f'fill {rel(0, 4, 11)} {rel(0, 7, 13)} minecraft:air replace minecraft:iron_bars'])

    # ================================================================== THE CHAMPION'S PIT
    fn('p76/r/pit/init', ['function bm:p70/ctx', sign(2.5, 7.5, 12, "THE CHAMPION'S PIT", 'Step into the sand if you dare.')])
    fn('p76/r/pit/tick', ['execute if score @s bm.gvs matches 3 run return 0',
                          'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..7] run function bm:p76/r/pit/call',
                          'execute if score @s bm.gvs matches 1 run function bm:p76/r/pit/fight'])
    tot = sum(c[0] for c in CHAMPS)
    call = ['scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvtm 0', 'function bm:p70/ctx',
            f'execute store result score #rr bm.rng run random value 1..{tot}']
    acc = 0
    for w, key, ty, nm, col, extra, attrs in CHAMPS:
        call.append(f'execute if score #rr bm.rng matches {acc + 1}..{acc + w} positioned {rel(12, 4, 12)} run return run function bm:p76/champ/{key}')
        acc += w
    fn('p76/r/pit/call', call)
    for w, key, ty, nm, col, extra, attrs in CHAMPS:
        nbt = {'Tags': ['bm.gvg', 'bm.gvchamp', 'bm.gvnew2', 'bm.tiered', 'bm.seen'], 'PersistenceRequired': B(1), 'CustomName': T(nm, col, bold=True), 'CustomNameVisible': B(1),
               'DeathLootTable': 'minecraft:empty', 'drop_chances': {k: F(0) for k in ('head', 'chest', 'legs', 'feet', 'mainhand', 'offhand')}}
        nbt.update(extra)
        if attrs: nbt['attributes'] = [{'id': f'minecraft:{a}', 'base': D(v)} for a, v in attrs.items()]
        n = 2 if key == 'gales' else 1
        lines = [f'summon minecraft:{ty} ~{i * 2} ~ ~ {snbt(nbt)}' for i in range(n)]
        if key == 'ratking':
            disp = {'Tags': ['bm.gvrkd', 'bm.gvprop'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:rat3d_lord'}},
                    'item_display': 'fixed', 'teleport_duration': Int(2),
                    'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(-0.9), F(0)], 'scale': [F(1.7)] * 3}}
            lines += [f'summon minecraft:item_display ~ ~ ~ {snbt(disp)}',
                      'ride @e[type=minecraft:item_display,tag=bm.gvrkd,distance=..1,limit=1,sort=nearest] mount @e[type=minecraft:zombie,tag=bm.gvnew2,limit=1,sort=nearest]',
                      'tag @e[type=minecraft:zombie,tag=bm.gvnew2,limit=1,sort=nearest] add bm.gvratking',
                      tellraw('@a[tag=bm.gvp,distance=..40]', P + [T('THE RAT KING ', '#ffd040', bold=True), T('scuttles out of the dark. Nobody has ever seen him and lived to sell the tale.', 'gray')])]
        lines += ['execute as @e[tag=bm.gvnew2,distance=..4] at @s run function bm:p76/champ_hp', 'tag @e[tag=bm.gvnew2,distance=..4] remove bm.gvnew2',
                  'particle minecraft:explosion ~ ~1 ~ 1 0.5 1 0 4', 'playsound minecraft:entity.ravager.roar hostile @a[distance=..30] ~ ~ ~ 1 0.9',
                  'title @a[tag=bm.gvp,distance=..24] times 5 40 10', title('@a[tag=bm.gvp,distance=..24]', 'title', T(nm, col, bold=True)),
                  title('@a[tag=bm.gvp,distance=..24]', 'subtitle', T('enters the pit', 'gray'))]
        fn(f'p76/champ/{key}', lines)
    fn('p76/champ_hp', ['scoreboard players operation @s bm.gvi = #gi bm.rng', 'execute store result score #n bm.rng if entity @a[tag=bm.gvp,distance=..30]',
                        'scoreboard players operation #h bm.rng = #gt bm.rng', 'scoreboard players set #q bm.rng 30', 'scoreboard players operation #h bm.rng *= #q bm.rng',
                        'scoreboard players add #h bm.rng 40', 'scoreboard players remove #n bm.rng 1', 'scoreboard players set #q bm.rng 20', 'scoreboard players operation #n bm.rng *= #q bm.rng',
                        'scoreboard players operation #h bm.rng += #n bm.rng', 'execute if entity @s[type=minecraft:breeze] run scoreboard players operation #h bm.rng /= #2 bm.rng',
                        'execute if entity @s[tag=bm.gvratking] run scoreboard players operation #h bm.rng *= #2 bm.rng',
                        'execute store result storage bm:gv h double 1 run scoreboard players get #h bm.rng', 'function bm:p70/hp with storage bm:gv',
                        'execute store result entity @s Health float 1 run scoreboard players get #h bm.rng',
                        'scoreboard players operation #d bm.rng = #gt bm.rng', 'scoreboard players add #d bm.rng 5',
                        'execute store result storage bm:gv d double 1 run scoreboard players get #d bm.rng', 'execute unless entity @s[type=minecraft:breeze] unless entity @s[type=minecraft:magma_cube] run function bm:p70/dmg with storage bm:gv'])
    fn('p76/r/pit/fight', ['scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #20 bm.rng', 'execute unless score #q bm.rng matches 0 run return 0',
                           'execute if entity @e[tag=bm.gvchamp,distance=..24] run return 0', 'function bm:p76/r/pit/won', 'function bm:p70/solved'])
    fn('p76/r/pit/won', ['execute store result score #c bm.rng run random value 10..20', inst('bm:p75/pot_add'),
                         'execute as @a[tag=bm.gvp,distance=..30] if score @s bm.gvi = #gi bm.rng at @s run function bm:p76/roll_champion',
                         'playsound minecraft:ui.toast.challenge_complete block @a[distance=..30] ~ ~ ~ 1 1.2'])
    fn('p76/roll_champion', ['execute store result score #r bm.rng run random value 1..100', 'execute if score #r bm.rng matches 1..25 run function bm:p76/find {t:"bm:p76/champion"}'])
    second.append('execute as @e[type=minecraft:item_display,tag=bm.gvrkd] at @s unless entity @e[type=minecraft:zombie,tag=bm.gvratking,distance=..4] run kill @s')
    # (a find: into this player's pot, told)
    fn('p76/find', ['$data modify storage bm:gv pf.t set value "$(t)"', 'function bm:p75/pot_item',
                    tellraw('@s', P + [T('Something rare goes into your haul... ', '#e0c0ff', bold=True), T('(you\'ll see what when you win)', 'gray')]),
                    'playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 1.2'])

    # ================================================================== THE RAT RAVE
    RV = R6.RAVE
    RCOL = {'red': '#ff4040', 'blue': '#4a6aff', 'lime': '#7dff6a', 'yellow': '#ffe040', 'magenta': '#ff50e0'}
    rats = [('pirate', 12, 5, 3, 180), ('soldier', 3, 4, 3, 220), ('chef', 21, 4, 3, 140), ('grey', 3, 4, 21, 320), ('lucky', 21, 4, 21, 40), ('prof', 12, 4, 22, 0)]
    def rat_disp(v, x, y, z, yaw, tag='bm.gvrat'):
        d = {'Tags': ['bm.gvprop', tag], 'Rotation': [F(yaw), F(0)], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:rat3d_{v}'}},
             'item_display': 'fixed', 'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.5), F(0)], 'scale': [F(0.9)] * 3}}
        return f'summon minecraft:item_display {rel(x, y, z)} {snbt(d)}'
    fn('p76/r/rave/init', ['function bm:p70/ctx'] + [rat_disp(*r) for r in rats] +
       ['summon minecraft:block_display ' + rel(11.5, 11.5, 11.5) + ' ' + snbt({'Tags': ['bm.gvprop', 'bm.gvball'], 'block_state': 'minecraft:sea_lantern', 'brightness': {'block': 15, 'sky': 15},
                                                                           'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(-0.5), F(-0.5), F(-0.5)], 'scale': [F(1.4)] * 3}}),
        sign(2.5, 7.5, 12, 'THE RAT RAVE', 'The DJ calls a colour. Be standing on it when the beat drops!')])
    fn('p76/r/rave/tick', ['execute if score @s bm.gvs matches 3 run return 0',
                           'scoreboard players set @a[tag=bm.gvp,distance=..15] bm.gvmz 7',
                           'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..10] run function bm:p76/r/rave/start',
                           'execute if score @s bm.gvs matches 1 run function bm:p76/r/rave/round',
                           'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #8 bm.rng',
                           'execute if score #q bm.rng matches 0 run function bm:p76/r/rave/lights'])
    fn('p76/r/rave/start', ['scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvw 0', 'scoreboard players set @s bm.gvtm 0', 'scoreboard players set @s bm.gvh 0',
                            'title @a[tag=bm.gvp,distance=..16] times 5 40 10', title('@a[tag=bm.gvp,distance=..16]', 'title', T('DANCE-OFF!', '#ff50e0', bold=True)),
                            title('@a[tag=bm.gvp,distance=..16]', 'subtitle', T('Stand on the colour the DJ calls', 'gray')), 'function bm:p76/r/rave/call'])
    # (round w: 80 ticks, 8 fewer each round; the call at 0, ticks at the end, the drop at the last tick)
    fn('p76/r/rave/round', ['scoreboard players set #len bm.rng 80', 'scoreboard players operation #q bm.rng = @s bm.gvw', 'scoreboard players operation #q bm.rng *= #8 bm.rng',
                            'scoreboard players operation #len bm.rng -= #q bm.rng',
                            'scoreboard players operation #left bm.rng = #len bm.rng', 'scoreboard players operation #left bm.rng -= @s bm.gvtm',
                            'execute if score #left bm.rng matches 20 run playsound minecraft:block.note_block.hat block @a[distance=..20] ~ ~ ~ 1 1',
                            'execute if score #left bm.rng matches 10 run playsound minecraft:block.note_block.hat block @a[distance=..20] ~ ~ ~ 1 1.4',
                            'execute if score #left bm.rng matches ..0 run function bm:p76/r/rave/drop'])
    call = ['execute store result score @s bm.gvc run random value 0..4', 'function bm:p76/r/rave/shuffle', 'scoreboard players set @s bm.gvtm 0']
    for j, c in enumerate(RV):
        call += [f'execute if score @s bm.gvc matches {j} run title @a[tag=bm.gvp,distance=..16] actionbar ' + snbt([T('The DJ calls: ', 'white'), T(c.upper() + '!', RCOL[c], bold=True)]),
                 f'execute if score @s bm.gvc matches {j} run particle minecraft:dust{{color:[{int(RCOL[c][1:3], 16) / 255:.2f},{int(RCOL[c][3:5], 16) / 255:.2f},{int(RCOL[c][5:7], 16) / 255:.2f}],scale:2}} {rel(12, 6, 3)} 2 1 0.5 0 40']
    call += ['playsound minecraft:block.note_block.pling block @a[distance=..20] ~ ~ ~ 1 1.2']
    fn('p76/r/rave/call', call)
    cells_ = [(x, z) for x in range(2, 23, 3) for z in range(2, 23, 3)]
    fn('p76/r/rave/shuffle', sum(([f'execute store result score #c bm.rng run random value 0..4'] +
                                  [f'execute if score #c bm.rng matches {j} run fill {rel(x, 3, z)} {rel(x + 2, 3, z + 2)} minecraft:{c}_stained_glass' for j, c in enumerate(RV)]
                                  for (x, z) in cells_), []))
    drop = ['tag @a remove bm.gvdance']
    for j, c in enumerate(RV):
        drop += [f'execute if score @s bm.gvc matches {j} as @a[tag=bm.gvp,distance=..15] at @s if block ~ ~-0.6 ~ minecraft:{c}_stained_glass run tag @s add bm.gvdance',
                 f'execute if score @s bm.gvc matches {j} as @a[tag=bm.gvp,distance=..15] at @s if block ~ ~-1.2 ~ minecraft:{c}_stained_glass run tag @s add bm.gvdance']
    drop += ['execute as @a[tag=bm.gvp,distance=..15,tag=bm.gvdance] run ' + title('@s', 'actionbar', T('Nice moves! +2 coins', LUCKY, bold=True)),
             'execute as @a[tag=bm.gvp,distance=..15,tag=!bm.gvdance] run ' + title('@s', 'actionbar', T('Missed the beat!', 'red')),
             'execute store result score #c bm.rng if entity @a[tag=bm.gvp,distance=..15,tag=bm.gvdance]', 'scoreboard players operation #c bm.rng *= #2 bm.rng',
             inst('bm:p75/pot_add'),
             'execute if entity @a[tag=bm.gvp,distance=..15,tag=!bm.gvdance] run scoreboard players set #add bm.rng 3',
             'execute if entity @a[tag=bm.gvp,distance=..15,tag=!bm.gvdance] run function bm:p70/oops',
             'execute as @a[tag=bm.gvp,distance=..15,tag=!bm.gvdance] run scoreboard players set @e[type=minecraft:marker,tag=bm.gvr_rave,distance=..20,limit=1] bm.gvf 1',
             'tag @a remove bm.gvdance', 'playsound minecraft:entity.firework_rocket.blast block @a[distance=..20] ~ ~ ~ 1 1',
             f'particle minecraft:firework {rel(12, 8, 12)} 4 2 4 0.1 60',
             'scoreboard players add @s bm.gvw 1', 'execute if score @s bm.gvw matches 6.. run return run function bm:p76/r/rave/done', 'function bm:p76/r/rave/call']
    fn('p76/r/rave/drop', drop)
    fn('p76/r/rave/done', ['effect give @a[tag=bm.gvp,distance=..16] minecraft:speed 120 0', 'effect give @a[tag=bm.gvp,distance=..16] minecraft:jump_boost 120 0',
                           'title @a[tag=bm.gvp,distance=..16] times 5 50 10', title('@a[tag=bm.gvp,distance=..16]', 'title', T('WHAT A PARTY', '#ff50e0', bold=True)),
                           title('@a[tag=bm.gvp,distance=..16]', 'subtitle', T('The rats let you through - with a spring in your step', 'gray')), 'function bm:p70/solved'])
    lights = ['execute store result score #c bm.rng run random value 0..4'] + \
             [f'execute if score #c bm.rng matches {j} run particle minecraft:dust{{color:[{int(RCOL[c][1:3], 16) / 255:.2f},{int(RCOL[c][3:5], 16) / 255:.2f},{int(RCOL[c][5:7], 16) / 255:.2f}],scale:1.5}} {rel(12, 11, 12)} 8 1 8 0 30'
              for j, c in enumerate(RV)] + \
             ['scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #16 bm.rng',
              'execute if score #q bm.rng matches 0 as @e[type=minecraft:item_display,tag=bm.gvrat,distance=..16] run data merge entity @s {start_interpolation:0,interpolation_duration:6,transformation:{translation:[0f,0.9f,0f]}}',
              'execute if score #q bm.rng matches 8 as @e[type=minecraft:item_display,tag=bm.gvrat,distance=..16] run data merge entity @s {start_interpolation:0,interpolation_duration:6,transformation:{translation:[0f,0.5f,0f]}}',
              'execute as @e[type=minecraft:block_display,tag=bm.gvball,distance=..16] at @s run tp @s ~ ~ ~ ~22.5 ~']
    fn('p76/r/rave/lights', lights)

    # ================================================================== THE RATS' REST
    from gen_dp import offer
    peddler = {'Tags': ['bm.gvprop', 'bm.npc'], 'NoAI': B(1), 'Invulnerable': B(1), 'Silent': B(1), 'PersistenceRequired': B(1), 'Rotation': [F(180), F(0)],
               'CustomName': T('Whiskers the Peddler', '#d9a066', bold=True), 'CustomNameVisible': B(1),
               'VillagerData': {'type': 'minecraft:swamp', 'profession': 'minecraft:butcher', 'level': Int(5)},
               'Offers': {'Recipes': [offer(('gutter_coin', p), (iid, n)) for p, iid, n in PEDDLER]}}
    fn('p76/r/rest/init', ['function bm:p70/ctx', f'summon minecraft:villager {rel(20.5, 4, 5)} {snbt(peddler)}',
                           rat_disp('chef', 12, 4, 3, 180, 'bm.gvrrat'), rat_disp('grey', 5, 5, 8, 90, 'bm.gvrrat'), rat_disp('pirate', 19, 5, 16, 270, 'bm.gvrrat'),
                           rat_disp('prof', 3, 6, 3, 135, 'bm.gvrrat'),
                           sign(2.5, 7.5, 12, "THE RATS' REST", 'Sit by the fire. Knocked out after this? You\'ll wake here.')])
    fn('p76/r/rest/tick', ['scoreboard players set @a[tag=bm.gvp,distance=..12] bm.gvmz 8',
                           'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..10] run function bm:p76/r/rest/arrive',
                           'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #20 bm.rng',
                           'execute if score #q bm.rng matches 0 run effect give @a[tag=bm.gvp,distance=..11] minecraft:regeneration 3 1 true',
                           'execute if score #q bm.rng matches 0 run effect give @a[tag=bm.gvp,distance=..11] minecraft:saturation 2 0 true',
                           f'execute if score #q bm.rng matches 0 run particle minecraft:campfire_cosy_smoke {rel(12, 6, 1)} 1 0.5 0.2 0.01 2'])
    fn('p76/r/rest/arrive', ['scoreboard players set @s bm.gvs 1', 'function bm:p70/solved',
                             'execute as @a[tag=bm.gvp,distance=..300] if score @s bm.gvi = #gi bm.rng run spawnpoint @s ~ ~ ~ -90 0',
                             'execute as @a[tag=bm.gvp,distance=..300] if score @s bm.gvi = #gi bm.rng run ' +
                             tellraw('@s', P + [T('The Rats\' Rest. ', '#d9a066', bold=True), T('If you\'re knocked out from here on, you wake by its fire.', 'gray')])])
    G.FUNCS['p75/after_fail'] += ['scoreboard players operation #gi bm.rng = @s bm.gvi'] + \
        [f'execute if score @s bm.gvi matches {s + 1} in bm:gutter run spawnpoint @s {int(P75.DEN[0])} {P75.DEN[1]} {P75.zoff(s) + int(P75.DEN[2])} -90 0' for s in range(P70.SLOTS)]

    # ================================================================== THE STORM VAULT
    fn('p76/r/storm/init', ['function bm:p70/ctx', 'scoreboard players operation @s bm.gvt = #gt bm.rng',
                            sign(2.5, 7.5, 12, 'THE STORM VAULT', 'Pull the lever on every copper pillar. Watch for the sparks.')] +
       [label(x, 8.5, z, T('⚡', '#ffe040', bold=True), 1.0) for (x, z) in R6.STORM_PILLARS])
    fn('p76/r/storm/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'scoreboard players set @a[tag=bm.gvp,distance=..15] bm.gvmz 9',
                            'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..11] run function bm:p76/r/storm/start',
                            'execute if score @s bm.gvs matches 0 run return 0', room_ctx,
                            'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #4 bm.rng',
                            f'execute if score #q bm.rng matches 0 run particle minecraft:falling_water {rel(12, 13, 12)} 10 0 10 0 25',
                            'scoreboard players set #per bm.rng 46', 'scoreboard players operation #q bm.rng = #gt bm.rng', 'scoreboard players operation #q bm.rng *= #4 bm.rng',
                            'scoreboard players operation #per bm.rng -= #q bm.rng',
                            'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #per bm.rng',
                            'execute if score #q bm.rng matches 0 as @a[tag=bm.gvp,distance=..15,sort=random,limit=1] at @s run function bm:p76/r/storm/aim',
                            'execute as @e[type=minecraft:marker,tag=bm.gvstrike,distance=..20] at @s run function bm:p76/r/storm/strike',
                            'scoreboard players set #n bm.rng 0'] +
       [f'execute if block {rel(x, y, z)} minecraft:lever[powered=true] run scoreboard players add #n bm.rng 1' for (x, y, z, f) in R6.STORM_LEVERS] +
       ['execute if score #n bm.rng matches 3.. run function bm:p76/r/storm/calm'])
    fn('p76/r/storm/start', ['scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvtm 1', 'function bm:p70/ctx',
                             'title @a[tag=bm.gvp,distance=..16] times 5 40 10', title('@a[tag=bm.gvp,distance=..16]', 'title', T('A STORM BREAKS', '#ffe040', bold=True)),
                             title('@a[tag=bm.gvp,distance=..16]', 'subtitle', T('Pull the three levers - mind the sparks', 'gray')),
                             'playsound minecraft:entity.lightning_bolt.thunder weather @a[distance=..30] ~ ~ ~ 1 0.8',
                             'scoreboard players operation #n bm.rng = #gt bm.rng', 'scoreboard players operation #n bm.rng /= #2 bm.rng', 'scoreboard players add #n bm.rng 1'] +
       [f'execute if score #n bm.rng matches {i + 1}.. positioned {rel(*p)} run function bm:p76/breeze' for i, p in enumerate([(4, 4, 20), (20, 4, 20), (12, 4, 4)])])
    fn('p76/breeze', [f'summon minecraft:breeze ~ ~ ~ {snbt(P75._mob("breeze", "Storm Breeze", "#c0e0ff", {})[1])}', 'function bm:p70/guard_set'])
    fn('p76/r/storm/aim', ['execute store result score #dx bm.rng run random value -2..2', 'execute store result score #dz bm.rng run random value -2..2',
                           'summon minecraft:marker ~ ~ ~ {Tags:["bm.gvstrike","bm.gvstn"]}',
                           'execute as @e[type=minecraft:marker,tag=bm.gvstn,limit=1] store result entity @s Pos[0] double 1 run data get entity @s Pos[0]',
                           'scoreboard players set @e[type=minecraft:marker,tag=bm.gvstn] bm.gvx 30', 'tag @e[type=minecraft:marker,tag=bm.gvstn] remove bm.gvstn'])
    fn('p76/r/storm/strike', ['scoreboard players remove @s bm.gvx 1', 'particle minecraft:electric_spark ~ ~0.2 ~ 0.6 0 0.6 0.05 6',
                              'execute if score @s bm.gvx matches 15 run playsound minecraft:block.beacon.power_select block @a[distance=..16] ~ ~ ~ 0.6 2',
                              'execute if score @s bm.gvx matches ..0 run function bm:p76/r/storm/bolt'])
    fn('p76/r/storm/bolt', [f'particle minecraft:end_rod ~ ~{y} ~ 0.05 0.3 0.05 0 4' for y in range(0, 11, 2)] +
       ['particle minecraft:flash{color:[1.0,1.0,0.8,1.0]} ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:electric_spark ~ ~0.5 ~ 1 0.5 1 0.4 60',
        'playsound minecraft:entity.lightning_bolt.thunder weather @a[distance=..30] ~ ~ ~ 1 1.2', 'playsound minecraft:entity.lightning_bolt.impact weather @a[distance=..30] ~ ~ ~ 1 1',
        'execute as @a[tag=bm.gvp,distance=..1.8] run damage @s 6 minecraft:lightning_bolt', 'kill @s'])
    fn('p76/r/storm/calm', ['kill @e[type=minecraft:marker,tag=bm.gvstrike,distance=..20]', 'execute as @e[type=minecraft:breeze,tag=bm.gvg,distance=..20] at @s run particle minecraft:poof ~ ~1 ~ 0.3 0.5 0.3 0.05 10',
                            'tp @e[type=minecraft:breeze,tag=bm.gvg,distance=..20] ~ -300 ~', 'kill @e[type=minecraft:breeze,tag=bm.gvg,distance=..20]',
                            'execute store result score #c bm.rng run random value 6..12', inst('bm:p75/pot_add'), 'function bm:p70/solved'])

    # ================================================================== THE VORN LANDING
    core = lambda i, x, z: [f'summon minecraft:item_display {rel(x, 4.6, z)} ' + snbt({'Tags': ['bm.gvprop', 'bm.gvcore', f'bm.gvcore{i}'], 'item': {'id': 'minecraft:beacon', 'count': Int(1)},
                                                                                       'brightness': {'block': 15, 'sky': 15}, 'Glowing': B(1),
                                                                                       'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0)] * 3, 'scale': [F(0.9)] * 3}}),
                            f'summon minecraft:interaction {rel(x, 4, z)} {{Tags:["bm.gvprop","bm.gvcoreh","bm.gvcoreh{i}"],width:1.1f,height:1.4f,response:1b}}']
    fn('p76/r/ufo/init', ['function bm:p70/ctx'] + sum((core(i, x, z) for i, (x, z) in enumerate(R6.UFO_CORES)), []) +
       ['execute as @e[type=minecraft:interaction,tag=bm.gvcoreh,distance=..16] run scoreboard players set @s bm.gvx 6',
        sign(2.5, 7.5, 12, 'THE VORN LANDING', 'Smash the saucer\'s three power cores.')])
    fn('p76/r/ufo/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'scoreboard players set @a[tag=bm.gvp,distance=..15] bm.gvmz 9',
                          'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..11] run function bm:p76/r/ufo/start',
                          'execute if score @s bm.gvs matches 0 run return 0',
                          f'particle minecraft:dust{{color:[0.5,1.0,0.3],scale:1.2}} {rel(12, 6, 12)} 0.6 1.2 0.6 0 3',
                          'execute as @e[type=minecraft:interaction,tag=bm.gvcoreh,distance=..16] if data entity @s attack at @s run function bm:p76/r/ufo/hit',
                          'execute as @e[type=minecraft:interaction,tag=bm.gvcoreh,distance=..16] if data entity @s interaction run data remove entity @s interaction',
                          'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #300 bm.rng',
                          'execute if score #q bm.rng matches 0 run function bm:p76/r/ufo/drop',
                          'execute unless entity @e[type=minecraft:interaction,tag=bm.gvcoreh,distance=..16] run function bm:p76/r/ufo/done'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #300 bm.rng 300']
    fn('p76/r/ufo/start', ['scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvtm 1', 'title @a[tag=bm.gvp,distance=..16] times 5 40 10',
                           title('@a[tag=bm.gvp,distance=..16]', 'title', T('THE VORN HAVE LANDED', '#b6ff3c', bold=True)),
                           title('@a[tag=bm.gvp,distance=..16]', 'subtitle', T('Smash the three power cores', 'gray')),
                           'playsound minecraft:block.beacon.activate hostile @a[distance=..30] ~ ~ ~ 1 0.6', 'function bm:p76/r/ufo/drop'])
    fn('p76/r/ufo/drop', ['function bm:p70/ctx', 'execute store result score #ng bm.rng if entity @e[tag=bm.gvg,distance=..20]', 'execute if score #ng bm.rng matches 6.. run return 0',
                          'execute positioned ' + rel(12, 4, 12) + ' run function bm:p70/guard_vorn', 'execute positioned ' + rel(10, 4, 12) + ' run function bm:p70/guard_vorn',
                          'execute if score #gt bm.rng matches 3.. positioned ' + rel(14, 4, 12) + ' run function bm:p70/guard_vorn',
                          f'particle minecraft:end_rod {rel(12, 6, 12)} 0.5 1.5 0.5 0.05 40', 'playsound minecraft:block.beacon.power_select hostile @a[distance=..30] ~ ~ ~ 1 1.4'])
    fn('p76/r/ufo/hit', ['data remove entity @s attack', 'scoreboard players remove @s bm.gvx 1', 'particle minecraft:electric_spark ~ ~0.8 ~ 0.3 0.3 0.3 0.3 25',
                         'playsound minecraft:block.glass.hit block @a[distance=..16] ~ ~ ~ 1 0.6', 'execute if score @s bm.gvx matches ..0 run function bm:p76/r/ufo/boom'])
    fn('p76/r/ufo/boom', ['particle minecraft:explosion ~ ~1 ~ 0.4 0.4 0.4 0 6', 'playsound minecraft:entity.generic.explode block @a[distance=..30] ~ ~ ~ 1 1.2',
                          'kill @e[type=minecraft:item_display,tag=bm.gvcore,distance=..1.5]', 'kill @s'])
    fn('p76/r/ufo/done', ['execute as @e[tag=bm.gvg,distance=..20] at @s run particle minecraft:end_rod ~ ~1 ~ 0.2 1 0.2 0.05 20',
                          'tp @e[tag=bm.gvg,distance=..20] ~ -300 ~', 'kill @e[tag=bm.gvg,distance=..20]',
                          'execute store result score #c bm.rng run random value 12..20', inst('bm:p75/pot_add'),
                          'execute as @a[tag=bm.gvp,distance=..30] if score @s bm.gvi = #gi bm.rng at @s run function bm:p76/find {t:"bm:items/xenite_green"}',
                          'title @a[tag=bm.gvp,distance=..20] times 5 40 10', title('@a[tag=bm.gvp,distance=..20]', 'title', T('SAUCER DOWN', '#b6ff3c', bold=True)),
                          'function bm:p70/solved'])

    # ================================================================== THE ENCHANTED GROVE
    wisp = lambda x, y, z: f'summon minecraft:block_display {rel(x, 5, z)} ' + snbt({'Tags': ['bm.gvprop', 'bm.gvwisp'], 'block_state': 'minecraft:pearlescent_froglight',
                                                                                    'brightness': {'block': 15, 'sky': 15}, 'Glowing': B(1), 'glow_color_override': Int(0xb0f0ff),
                                                                                    'transformation': {'left_rotation': ident, 'right_rotation': ident,
                                                                                                       'translation': [F(-0.18), F(0.2), F(-0.18)], 'scale': [F(0.36)] * 3}})
    fn('p76/r/grove/init', ['function bm:p70/ctx', 'scoreboard players set @s bm.gvc 0', 'scoreboard players set @s bm.gvw 0',
                            sign(2.5, 7.5, 12, 'THE ENCHANTED GROVE', 'Catch the four wisps. The sprites will mind.')] +
       [wisp(*p) for p in R6.GROVE_WISPS] + ['kill @e[type=minecraft:block_display,tag=bm.gvwisp,distance=..20,sort=random,limit=2]'])
    fn('p76/r/grove/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'scoreboard players set @a[tag=bm.gvp,distance=..15] bm.gvmz 8',
                            'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..12] run scoreboard players set @s bm.gvs 1',
                            'execute if score @s bm.gvs matches 0 run return 0',
                            'execute as @e[type=minecraft:block_display,tag=bm.gvwisp,distance=..20] at @s positioned ~ ~-0.8 ~ if entity @a[tag=bm.gvp,distance=..1.4] run function bm:p76/r/grove/catch',
                            'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #10 bm.rng',
                            'execute if score #q bm.rng matches 0 as @e[type=minecraft:block_display,tag=bm.gvwisp,distance=..20] at @s run particle minecraft:end_rod ~ ~0.4 ~ 0.15 0.15 0.15 0.01 2',
                            'execute if score #q bm.rng matches 0 run particle minecraft:glow ' + rel(12, 7, 12) + ' 10 3 10 0 6',
                            'execute if score @s bm.gvc matches 4.. run function bm:p76/r/grove/done'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #10 bm.rng 10']
    fn('p76/r/grove/catch', ['kill @s', 'particle minecraft:end_rod ~ ~0.5 ~ 0.3 0.3 0.3 0.1 25', 'playsound minecraft:block.amethyst_block.chime block @a[distance=..20] ~ ~ ~ 1 1.6',
                             'execute as @e[type=minecraft:marker,tag=bm.gvr_grove,distance=..24,sort=nearest,limit=1] at @s run function bm:p76/r/grove/caught'])
    fn('p76/r/grove/caught', ['scoreboard players add @s bm.gvc 1', 'scoreboard players set #c bm.rng 3', inst('bm:p75/pot_add'),
                              'execute as @a[tag=bm.gvp,distance=..24] run ' + title('@s', 'actionbar', [T('A wisp! ', '#b0f0ff', bold=True),
                                                                                                         {'score': {'name': '@e[type=minecraft:marker,tag=bm.gvr_grove,limit=1,sort=nearest]', 'objective': 'bm.gvc'}, 'color': 'white'},
                                                                                                         T(' of 4', 'gray')]),
                              'execute if score @s bm.gvc matches 1 at @s run function bm:p76/r/grove/sprites'])
    fn('p76/r/grove/sprites', ['function bm:p70/ctx', 'scoreboard players operation #n bm.rng = #gt bm.rng', 'scoreboard players add #n bm.rng 1'] +
       [f'execute if score #n bm.rng matches {i + 1}.. positioned {rel(x, 7, z)} run function bm:p76/sprite' for i, (x, z) in enumerate([(5, 5), (19, 5), (5, 19), (19, 19), (12, 6), (12, 18)])] +
       ['playsound minecraft:entity.vex.charge hostile @a[distance=..24] ~ ~ ~ 1 1.4'])
    fn('p76/sprite', [f'summon minecraft:vex ~ ~ ~ {snbt(P75._mob("vex", "Grove Sprite", "#b0f0ff", {}, {})[1])}', 'function bm:p70/guard_set'])
    fn('p76/r/grove/done', ['effect give @a[tag=bm.gvp,distance=..16] minecraft:regeneration 60 0', 'effect give @a[tag=bm.gvp,distance=..16] minecraft:luck 300 0',
                            'execute as @e[type=minecraft:vex,tag=bm.gvg,distance=..20] at @s run particle minecraft:end_rod ~ ~ ~ 0.2 0.2 0.2 0.05 10',
                            'kill @e[type=minecraft:vex,tag=bm.gvg,distance=..20]', 'scoreboard players set #c bm.rng 8', inst('bm:p75/pot_add'),
                            'title @a[tag=bm.gvp,distance=..16] times 5 40 10', title('@a[tag=bm.gvp,distance=..16]', 'title', T('THE GROVE BLESSES YOU', '#b0f0ff', bold=True)),
                            'function bm:p70/solved'])

    # ================================================================== SECRETS: loose bricks, the Phantom Thief
    CRACK = {1: 'minecraft:chiseled_tuff', 2: 'minecraft:cracked_stone_bricks', 3: 'minecraft:cracked_polished_blackstone_bricks',
             4: 'minecraft:cracked_deepslate_tiles', 5: 'minecraft:cracked_deepslate_bricks'}
    SPOTS = [(0, 5, 5), (0, 6, 19), (24, 5, 5), (24, 6, 19)]
    fn('p76/secret/maybe', ['scoreboard players set #ok bm.rng 0'] +
       [f'execute if entity @s[tag=bm.gvr_{k}] run scoreboard players set #ok bm.rng 1' for k in SECRET_KINDS] +
       ['execute if score #ok bm.rng matches 0 run return 0', 'execute store result score #r bm.rng run random value 1..100', 'execute if score #r bm.rng matches 36.. run return 0',
        'execute store result score #r bm.rng run random value 0..3'] +
       [f'execute if score #r bm.rng matches {i} positioned {rel(*p)} run function bm:p76/secret/set' for i, p in enumerate(SPOTS)])
    fn('p76/secret/set', [f'execute if score #gt bm.rng matches {t} run setblock ~ ~ ~ {b}' for t, b in CRACK.items()] +
       ['summon minecraft:interaction ~ ~ ~ {Tags:["bm.gvprop","bm.gvsec","bm.gvsecn"],width:1.04f,height:1.04f,response:1b}',
        'scoreboard players operation @e[type=minecraft:interaction,tag=bm.gvsecn] bm.gvi = #gi bm.rng', 'tag @e[type=minecraft:interaction,tag=bm.gvsecn] remove bm.gvsecn'])
    G.FUNCS['p76/secret/set'] = [l.replace('setblock ~ ~ ~', 'execute align xyz run setblock ~ ~ ~') if 'setblock' in l else l for l in G.FUNCS['p76/secret/set']]
    G.FUNCS['p76/secret/set'] = [l.replace('summon minecraft:interaction ~ ~ ~', 'execute align xyz positioned ~0.5 ~-0.02 ~0.5 run summon minecraft:interaction ~ ~ ~') for l in G.FUNCS['p76/secret/set']]
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.gvsec] if data entity @s interaction at @s run function bm:p76/secret/open')
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.gvsec] if data entity @s attack run data remove entity @s attack')
    fn('p76/secret/open', ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'execute align xyz run setblock ~ ~ ~ minecraft:chiseled_bookshelf[facing=north]',
                           'particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~0.5 ~ 0.4 0.4 0.4 0 25', 'particle minecraft:wax_on ~ ~0.5 ~ 0.5 0.5 0.5 0 15',
                           'playsound minecraft:block.chiseled_bookshelf.pickup.enchanted block @a[distance=..16] ~ ~ ~ 1 0.8',
                           'playsound minecraft:entity.experience_orb.pickup block @a[distance=..16] ~ ~ ~ 1 0.7',
                           'execute store result score #c bm.rng run random value 6..12', inst('bm:p75/pot_add'),
                           'execute as @a[tag=bm.gvp,distance=..24] if score @s bm.gvi = #gi bm.rng at @s run function bm:p76/secret/share',
                           'execute store result score #r bm.rng run random value 1..100', 'execute if score #r bm.rng matches ..20 positioned ^ ^ ^1 run function bm:p76/thief/spawn',
                           'kill @s'])
    fn('p76/secret/share', [say('A loose brick - a hidden stash behind it! Coins into the pot.', GOLD),
                            'execute store result score #r bm.rng run random value 1..100', 'execute if score #r bm.rng matches ..15 run function bm:p76/find {t:"bm:p76/secret"}'])
    # the hints: the Cipher Monocle (close by), the Lantern of Lost Things (across the room), a Treasure Map Scrap (everything, for a minute)
    monocle = '*[minecraft:custom_data~{bm:"cipher_monocle"}]'
    lantern = '*[minecraft:custom_data~{bm:"lost_lantern"}]'
    second += [f'execute as @a[tag=bm.gvp] if items entity @s armor.head {monocle} at @s as @e[type=minecraft:interaction,tag=bm.gvsec,distance=..8] at @s run particle minecraft:wax_on ~ ~0.5 ~ 0.4 0.4 0.4 0 6',
               f'execute as @a[tag=bm.gvp] if items entity @s weapon.* {lantern} at @s as @e[type=minecraft:interaction,tag=bm.gvsec,distance=..22] at @s run particle minecraft:soul_fire_flame ~ ~0.5 ~ 0.3 0.4 0.3 0.01 6']
    # the Phantom Thief: grabs from the pot and runs - catch him and you get it back, twice over
    thief = {'Tags': ['bm.gvthief', 'bm.gvnew2', 'bm.tiered', 'bm.seen'], 'PersistenceRequired': B(1), 'CustomName': T('Phantom Thief', PH, bold=True), 'CustomNameVisible': B(1),
             'Silent': B(1), 'DeathLootTable': 'minecraft:empty', 'Health': F(14),
             'attributes': [{'id': 'minecraft:max_health', 'base': D(14)}, {'id': 'minecraft:movement_speed', 'base': D(0.5)}],
             'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0)}]}
    thief_d = {'Tags': ['bm.gvthiefd', 'bm.gvprop'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:rat3d_void'}},
               'item_display': 'fixed', 'teleport_duration': Int(2),
               'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(-0.1), F(0)], 'scale': [F(0.8)] * 3}}
    fn('p76/thief/spawn', [f'summon minecraft:rabbit ~ ~ ~ {snbt(thief)}', f'summon minecraft:item_display ~ ~ ~ {snbt(thief_d)}',
                           'ride @e[type=minecraft:item_display,tag=bm.gvthiefd,distance=..1,limit=1,sort=nearest] mount @e[type=minecraft:rabbit,tag=bm.gvnew2,limit=1,sort=nearest]',
                           'scoreboard players operation @e[type=minecraft:rabbit,tag=bm.gvnew2,limit=1,sort=nearest] bm.gvi = #gi bm.rng',
                           'scoreboard players set @e[type=minecraft:rabbit,tag=bm.gvnew2,limit=1,sort=nearest] bm.gvx 0',
                           'scoreboard players set @e[type=minecraft:rabbit,tag=bm.gvnew2,limit=1,sort=nearest] bm.gvh 40',
                           'tag @e[type=minecraft:rabbit,tag=bm.gvnew2] remove bm.gvnew2', 'particle minecraft:portal ~ ~1 ~ 0.4 0.6 0.4 0.5 40',
                           tellraw('@a[tag=bm.gvp,distance=..30]', P + [T('A PHANTOM THIEF ', PH, bold=True), T('was hiding in the wall - he\'s off with the pot! Catch him!', 'gray')])])
    second.append('execute as @e[type=minecraft:rabbit,tag=bm.gvthief] at @s run function bm:p76/thief/sec')
    fn('p76/thief/sec', ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'scoreboard players remove @s bm.gvh 1', 'particle minecraft:reverse_portal ~ ~0.5 ~ 0.2 0.3 0.2 0.02 8',
                         'scoreboard players set #c bm.rng 2', inst('bm:p76/thief/grab'), 'scoreboard players operation @s bm.gvx += #got bm.rng',
                         'execute if score @s bm.gvh matches ..0 run function bm:p76/thief/gone'])
    fn('p76/thief/grab', ['scoreboard players set #got bm.rng 0', 'execute if score @s bm.gvpot matches 2.. run scoreboard players set #got bm.rng 2',
                          'scoreboard players operation @s bm.gvpot -= #got bm.rng', 'scoreboard players operation @s bm.gvstl += #got bm.rng', 'function bm:p70/bar'])
    fn('p76/thief/gone', ['particle minecraft:portal ~ ~1 ~ 0.4 0.6 0.4 0.5 40', 'playsound minecraft:entity.enderman.teleport hostile @a[distance=..24] ~ ~ ~ 1 0.6',
                          tellraw('@a[tag=bm.gvp,distance=..40]', P + [T('The Phantom Thief vanishes into the walls with ', PH), {'score': {'name': '@s', 'objective': 'bm.gvx'}, 'color': 'white', 'bold': True},
                                                                       T(' coins.', PH)]),
                          'execute on passengers run kill @s', 'tp @s ~ -300 ~', 'kill @s'])
    second.append('execute as @e[type=minecraft:item_display,tag=bm.gvthiefd] at @s unless entity @e[type=minecraft:rabbit,tag=bm.gvthief,distance=..3] run kill @s')

    # ================================================================== RARE FOES: the Coin Rat, shiny guards (and the thief and champions above)
    gob = {'Tags': ['bm.gvgob', 'bm.gvnew2', 'bm.seen'], 'PersistenceRequired': B(1), 'CustomName': T('✦ Coin Rat ✦', GOLD, bold=True), 'CustomNameVisible': B(1), 'Silent': B(1),
           'DeathLootTable': 'minecraft:empty', 'Health': F(12), 'Glowing': B(1),
           'attributes': [{'id': 'minecraft:max_health', 'base': D(12)}, {'id': 'minecraft:movement_speed', 'base': D(0.45)}],
           'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0)}]}
    gob_d = dict(thief_d, Tags=['bm.gvgobd', 'bm.gvprop'], item={'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:rat3d_lucky'}})
    G.FUNCS['p70/r/tick'][2:2] = ['execute if score @s bm.gvs matches 0 unless entity @s[tag=bm.gvseen] if entity @a[tag=bm.gvp,distance=..12] run function bm:p76/first_visit']
    fn('p76/first_visit', ['tag @s add bm.gvseen', 'execute if entity @s[tag=bm.gvr_lobby] run return 0', 'execute if entity @s[tag=bm.gvr_vault] run return 0',
                           'execute if entity @s[tag=bm.gvr_cache] run return 0', 'execute if entity @s[tag=bm.gvr_rest] run return 0',
                           'execute store result score #r bm.rng run random value 1..100', 'scoreboard players set #gch bm.rng 6',
                           'execute if score @s bm.gvt matches 5 run scoreboard players set #gch bm.rng 9',
                           'execute if score #r bm.rng <= #gch bm.rng positioned ' + rel(4, 4, 20) + ' run function bm:p76/gob/spawn'])
    fn('p76/gob/spawn', [f'summon minecraft:rabbit ~ ~ ~ {snbt(gob)}', f'summon minecraft:item_display ~ ~ ~ {snbt(gob_d)}',
                         'ride @e[type=minecraft:item_display,tag=bm.gvgobd,distance=..1,limit=1,sort=nearest] mount @e[type=minecraft:rabbit,tag=bm.gvnew2,limit=1,sort=nearest]',
                         'scoreboard players operation @e[type=minecraft:rabbit,tag=bm.gvnew2,limit=1,sort=nearest] bm.gvi = #gi bm.rng',
                         'scoreboard players set @e[type=minecraft:rabbit,tag=bm.gvnew2,limit=1,sort=nearest] bm.gvh 30',
                         'tag @e[type=minecraft:rabbit,tag=bm.gvnew2] remove bm.gvnew2', 'playsound minecraft:entity.experience_orb.pickup neutral @a[distance=..30] ~ ~ ~ 1 2',
                         tellraw('@a[tag=bm.gvp,distance=..30]', P + [T('A COIN RAT! ', GOLD, bold=True), T('Catch it before it gets away - it\'s worth a fortune.', 'gray')])])
    second.append('execute as @e[type=minecraft:rabbit,tag=bm.gvgob] at @s run function bm:p76/gob/sec')
    fn('p76/gob/sec', ['scoreboard players remove @s bm.gvh 1', 'particle minecraft:wax_on ~ ~0.6 ~ 0.3 0.3 0.3 0 6',
                       'execute if score @s bm.gvh matches ..0 run function bm:p76/gob/gone'])
    fn('p76/gob/gone', ['particle minecraft:poof ~ ~0.5 ~ 0.3 0.3 0.3 0.05 20', tellraw('@a[tag=bm.gvp,distance=..40]', P + [T('The Coin Rat got away.', 'gray')]),
                        'execute on passengers run kill @s', 'tp @s ~ -300 ~', 'kill @s'])
    second.append('execute as @e[type=minecraft:item_display,tag=bm.gvgobd] at @s unless entity @e[type=minecraft:rabbit,tag=bm.gvgob,distance=..3] run kill @s')
    killed = lambda tag: {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["%s"]}' % tag}}]}}}
    for key, tag in (('gob', 'bm.gvgob'), ('thief', 'bm.gvthief'), ('shiny', 'bm.gvshiny'), ('ratking', 'bm.gvratking')):
        wjson(f'bm/advancement/p76/kill_{key}.json', {'criteria': killed(tag), 'rewards': {'function': f'bm:p76/kill_{key}'}})
    fn('p76/kill_gob', ['advancement revoke @s only bm:p76/kill_gob', 'execute unless entity @s[tag=bm.gvp] run return 0', 'scoreboard players operation #gi bm.rng = @s bm.gvi',
                        'function bm:p70/ctx', 'execute store result score #c bm.rng run random value 15..30', 'scoreboard players operation #q bm.rng = #gt bm.rng',
                        'scoreboard players set #k bm.rng 8', 'scoreboard players operation #q bm.rng *= #k bm.rng', 'scoreboard players operation #c bm.rng += #q bm.rng', inst('bm:p75/pot_add'),
                        tellraw('@a[tag=bm.gvp,distance=..60]', P + [{'selector': '@s', 'color': 'white'}, T(' caught the Coin Rat! ', GOLD, bold=True),
                                                                     {'score': {'name': '#c', 'objective': 'bm.rng'}, 'color': GOLD}, T(' coins into the pot.', 'gray')]),
                        'execute store result score #r bm.rng run random value 1..100', 'execute if score #r bm.rng matches ..10 run function bm:p76/find {t:"bm:items/rats_foot"}',
                        'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1.6',
                        # (its model goes with it at once, not at the next second's sweep)
                        'execute at @s as @e[type=minecraft:item_display,tag=bm.gvgobd,distance=..48] at @s unless entity @e[type=minecraft:rabbit,tag=bm.gvgob,distance=..3] run function bm:p76/gob/poof'])
    fn('p76/gob/poof', ['particle minecraft:poof ~ ~0.5 ~ 0.3 0.3 0.3 0.05 16', 'particle minecraft:wax_on ~ ~0.5 ~ 0.4 0.4 0.4 0 12', 'kill @s'])
    fn('p76/kill_thief', ['advancement revoke @s only bm:p76/kill_thief', 'execute unless entity @s[tag=bm.gvp] run return 0', 'scoreboard players operation #gi bm.rng = @s bm.gvi',
                          inst('bm:p76/thief/repay'),
                          tellraw('@a[tag=bm.gvp,distance=..60]', P + [{'selector': '@s', 'color': 'white'}, T(' caught the Phantom Thief - the pot gets it all back, twice over.', PH)]),
                          'execute store result score #r bm.rng run random value 1..100', 'execute if score #r bm.rng matches ..30 run function bm:p76/find {t:"bm:p76/phantom"}'])
    fn('p76/thief/repay', ['scoreboard players operation #c bm.rng = @s bm.gvstl', 'scoreboard players operation #c bm.rng *= #2 bm.rng', 'scoreboard players add #c bm.rng 6',
                           'scoreboard players set @s bm.gvstl 0', 'function bm:p75/pot_add'])
    fn('p76/kill_shiny', ['advancement revoke @s only bm:p76/kill_shiny', 'execute unless entity @s[tag=bm.gvp] run return 0', 'scoreboard players operation #gi bm.rng = @s bm.gvi',
                          'scoreboard players set #c bm.rng 10', inst('bm:p75/pot_add'), 'function bm:p76/find {t:"bm:p76/shiny"}',
                          tellraw('@a[tag=bm.gvp,distance=..60]', P + [{'selector': '@s', 'color': 'white'}, T(' felled a ', 'gray'), T('SHINY', GOLD, bold=True), T(' guard!', 'gray')])])
    fn('p76/kill_ratking', ['advancement revoke @s only bm:p76/kill_ratking', 'execute unless entity @s[tag=bm.gvp] run return 0',
                            'execute as @a[tag=bm.gvp,distance=..40] at @s run function bm:p76/find {t:"bm:p76/ratking"}',
                            tellraw('@a', P + [{'selector': '@s', 'color': 'white'}, T(' and their crew brought down ', 'gray'), T('THE RAT KING', '#ffd040', bold=True), T('!', 'gray')])])
    # shiny: 1 in 150 of any guard (set as it's made)
    G.FUNCS['p70/guard_set1'] += ['execute store result score #r bm.rng run random value 1..150', 'execute if score #r bm.rng matches 1 run function bm:p76/shiny']
    fn('p76/shiny', ['tag @s add bm.gvshiny', 'data merge entity @s {Glowing:1b,CustomNameVisible:1b}',
                     'data modify entity @s CustomName set value [{"text":"✦ Shiny ","color":"#ffcf40","bold":true},{"text":"Guard","color":"#ffcf40"},{"text":" ✦","color":"#ffcf40","bold":true}]',
                     'execute store result score #h bm.rng run attribute @s minecraft:max_health base get', 'scoreboard players operation #h bm.rng *= #2 bm.rng',
                     'execute store result storage bm:gv h double 1 run scoreboard players get #h bm.rng', 'function bm:p70/hp with storage bm:gv',
                     'execute store result entity @s Health float 1 run scoreboard players get #h bm.rng'])
    second.append('execute as @e[tag=bm.gvshiny] at @s run particle minecraft:wax_on ~ ~1.2 ~ 0.3 0.6 0.3 0 4')

    # ================================================================== LOOT: the rare tables (rolled when the haul is paid)
    # (2.67: no Tokens or Medallions in any of them - those come only from the Fixer's capped prize, phase75 p75/prize)
    from gen_dp import loot_entry, uni
    def table(*entries):
        return {'pools': [{'rolls': 1, 'entries': [dict(loot_entry(i, c), weight=w) if i in ITEMS else
                                                   {'type': 'minecraft:item', 'name': i, 'weight': w, 'functions': [{'function': 'minecraft:set_count', 'count': c}] if c else []}
                                                   for i, w, c in entries]}]}
    regalia = [(iid, 1, None) for iid, *_r in PHANTOM]
    wjson('bm/loot_table/p76/phantom.json', table(*regalia))
    wjson('bm/loot_table/p76/secret.json', table(('second_wind', 6, None), ('treasure_map_scrap', 6, None), ('healing_draught', 10, uni(1, 2)),
                                                ('gutter_coin', 14, uni(4, 10)), ('lucky_purse', 3, None), ('lost_lantern', 1, None), ('master_key', 1, None), ('rats_foot', 1, None),
                                                *[(iid, 1, None) for iid, *_r in PHANTOM]))
    wjson('bm/loot_table/p76/shiny.json', table(*[(iid, 4, None) for iid, *_r in PHANTOM], ('master_key', 3, None), ('lost_lantern', 3, None), ('rats_foot', 3, None),
                                               ('gutter_coin', 3, uni(8, 16)), ('second_wind', 3, None)))
    wjson('bm/loot_table/p76/champion.json', table(('gutter_coin', 8, uni(8, 16)), ('second_wind', 4, None), ('lucky_purse', 3, None),
                                                  ('master_key', 1, None), ('lost_lantern', 1, None), ('rats_foot', 1, None), *[(iid, 1, None) for iid, *_r in PHANTOM]))
    wjson('bm/loot_table/p76/ratking.json', {'pools': [{'rolls': 1, 'entries': [loot_entry('rats_foot')]},
                                                       {'rolls': 1, 'entries': [dict(loot_entry(iid), weight=1) for iid, *_r in PHANTOM] + [dict(loot_entry('master_key'), weight=1)]},
                                                       {'rolls': 1, 'entries': [loot_entry('gutter_coin', uni(12, 24))]}]})

    # ================================================================== THE ITEMS
    # Second Wind: +1 try for your crew, once a heist each
    fn('p76/item/second_wind', ['execute unless entity @s[tag=bm.gvp] run return run ' + say('Save it for a heist.'),
                                'scoreboard players operation #q bm.rng = @s bm.gvrun', 'execute if score @s bm.gvsw = #q bm.rng run return run ' + say('You\'ve had your second wind this heist.', 'red'),
                                'scoreboard players operation #gi bm.rng = @s bm.gvi', 'scoreboard players set #ok bm.rng 0', inst('bm:p76/item/sw_inst'),
                                'execute if score #ok bm.rng matches 0 run return run ' + say('Not now - the heist isn\'t on.', 'red'),
                                'scoreboard players operation @s bm.gvsw = @s bm.gvrun', 'execute unless entity @s[gamemode=creative] run clear @s *[minecraft:custom_data~{bm:"second_wind"}] 1',
                                'playsound minecraft:item.totem.use player @a[distance=..16] ~ ~ ~ 0.6 1.4', 'particle minecraft:totem_of_undying ~ ~1 ~ 0.4 0.6 0.4 0.3 30',
                                'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run function bm:p70/tag_mine',
                                tellraw('@a[tag=bm.gvme]', P + [{'selector': '@s', 'color': 'white'}, T(' takes a Second Wind: ', 'gray'), T('one more try for the crew.', '#ff7a7a', bold=True)]),
                                'tag @a[tag=bm.gvme] remove bm.gvme'])
    fn('p76/item/sw_inst', ['execute unless score @s bm.gvst matches 1..3 run return 0', 'scoreboard players add @s bm.gvlv 1', 'scoreboard players set #ok bm.rng 1', 'function bm:p70/bar'])
    # Treasure Map Scrap: every loose brick in the heist glows for a minute
    fn('p76/item/map', ['execute unless entity @s[tag=bm.gvp] run return run ' + say('Save it for a heist.'), 'scoreboard players operation #gi bm.rng = @s bm.gvi',
                        'execute store result score #n bm.rng as @e[type=minecraft:interaction,tag=bm.gvsec] if score @s bm.gvi = #gi bm.rng at @s run function bm:p76/item/map_mark',
                        'execute unless entity @s[gamemode=creative] run clear @s *[minecraft:custom_data~{bm:"treasure_map_scrap"}] 1',
                        'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 1',
                        'execute if score #n bm.rng matches 0 run return run ' + say('The scrap shows nothing hidden in this heist. (The Fixer\'s maps are never wrong.)', '#d9a066'),
                        title('@s', 'actionbar', [T('The map shows ', '#d9a066'), {'score': {'name': '#n', 'objective': 'bm.rng'}, 'color': 'white', 'bold': True},
                                                  T(' hidden stash(es) - they glow for a minute.', '#d9a066')])])
    fn('p76/item/map_mark', ['execute align xyz run summon minecraft:block_display ~ ~ ~ ' + snbt({'Tags': ['bm.gvmapd', 'bm.gvprop'], 'block_state': 'minecraft:gold_block',
                                                                                              'Glowing': B(1), 'glow_color_override': Int(0xffcf40),
                                                                                              'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0.05)] * 3,
                                                                                                                 'scale': [F(0.9)] * 3}}),
                             'execute align xyz run scoreboard players set @e[type=minecraft:block_display,tag=bm.gvmapd,dx=0,dy=0,dz=0] bm.gvx 60', 'return 1'])
    second.append('execute as @e[type=minecraft:block_display,tag=bm.gvmapd] at @s run function bm:p76/item/map_fade')
    fn('p76/item/map_fade', ['scoreboard players remove @s bm.gvx 1', 'execute if score @s bm.gvx matches ..0 run kill @s',
                             'execute at @s unless entity @e[type=minecraft:interaction,tag=bm.gvsec,distance=..1.2] run kill @s'])
    # Golden Compass: a trail to the nearest locked door
    fn('p76/item/compass', ['execute unless entity @s[tag=bm.gvp] run return run ' + say('It spins idly. (It only works in a heist.)', GOLD),
                            'scoreboard players operation #gi bm.rng = @s bm.gvi',
                            'tag @s add bm.gvcmp',
                            'execute as @e[type=minecraft:marker,tag=bm.gvr,tag=!bm.gvr_lobby,tag=!bm.gvr_cache,scores={bm.gvs=0..2},sort=nearest] if score @s bm.gvi = #gi bm.rng run tag @s add bm.gvcmpt',
                            'execute unless entity @e[type=minecraft:marker,tag=bm.gvcmpt] run return run function bm:p76/item/compass_none',
                            'execute facing entity @e[type=minecraft:marker,tag=bm.gvcmpt,limit=1,sort=nearest] feet run function bm:p76/item/compass_trail',
                            'tag @e[type=minecraft:marker,tag=bm.gvcmpt] remove bm.gvcmpt', 'tag @s remove bm.gvcmp', 'playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1.8'])
    fn('p76/item/compass_none', ['tag @s remove bm.gvcmp', say('Every door is open. The vault waits ahead.', GOLD)])
    fn('p76/item/compass_trail', [f'particle minecraft:dust{{color:[1.0,0.8,0.25],scale:1.2}} ^ ^0.9 ^{d} 0 0 0 0 1' for d in range(1, 21)])
    # Master Key: beats the puzzle room you stand in (every ten minutes)
    fn('p76/item/master_key', ['execute unless entity @s[tag=bm.gvp] run return run ' + say('It turns in no lock up here.'),
                               'execute if score @s bm.gvmk matches 1.. run return run ' + say('The key is still cooling (ten minutes between locks).', 'red'),
                               'scoreboard players set #ok bm.rng 0',
                               'execute as @e[type=minecraft:marker,tag=bm.gvr,tag=bm.gvpuz,distance=..16,sort=nearest,limit=1] unless score @s bm.gvs matches 3 run scoreboard players set #ok bm.rng 1',
                               'execute if score #ok bm.rng matches 0 run return run ' + say('No puzzle lock here.'),
                               'scoreboard players set @s bm.gvmk 600', 'execute as @e[type=minecraft:marker,tag=bm.gvr,tag=bm.gvpuz,distance=..16,sort=nearest,limit=1] at @s run function bm:p71/crack1',
                               'playsound minecraft:block.vault.open_shutter player @a[distance=..16] ~ ~ ~ 1 1', say('The Master Key turns. Everything opens.', GOLD)])
    second.append('scoreboard players remove @a[scores={bm.gvmk=1..}] bm.gvmk 1')
    # the Lucky Rat's Foot (luck; +1 share) and the Lucky Purse (+2 shares, used up) - counted in each player's own haul
    foot = '*[minecraft:custom_data~{bm:"rats_foot"}]'
    purse = '*[minecraft:custom_data~{bm:"lucky_purse"}]'
    second.append(f'execute as @a if items entity @s container.* {foot} run effect give @s minecraft:luck 3 0 true')
    haul = G.FUNCS['p70/haul']
    k = next(i for i, l in enumerate(haul) if l == 'scoreboard players operation #i bm.rng = #sh bm.rng')
    haul[k + 1:k + 1] = [f'execute if items entity @s container.* {foot} run scoreboard players add #i bm.rng 1',
                         f'execute if items entity @s container.* {purse} run scoreboard players add #i bm.rng 2',
                         f'execute if items entity @s container.* {purse} run ' + tellraw('@s', P + [T('Your Lucky Purse fills up: ', LUCKY), T('+2 shares.', LUCKY, bold=True)]),
                         f'clear @s {purse} 1']
    # the Phantom Regalia's set bonus: invisible while sneaking, soft landings
    full = ' '.join(f'if items entity @s armor.{s} *[minecraft:custom_data~{{bm:"{iid}"}}]' for iid, b, nm, s, a in PHANTOM)
    fast.append(f'execute as @a[scores={{bm.sneak=1..}}] {full} run effect give @s minecraft:invisibility 1 0 true')
    second.append(f'execute as @a {full} at @s run function bm:p76/phantom_set')
    fn('p76/phantom_set', ['execute if predicate bm:p21/airborne run effect give @s minecraft:slow_falling 2 0 true', 'particle minecraft:reverse_portal ~ ~1 ~ 0.25 0.5 0.25 0.01 2'])

    # ================================================================== den livelihood: a few rats about the place
    G.FUNCS['p70/r/lobby/init'] += [rat_disp('grey', 7, 5, 19, 180, 'bm.gvdrat'), rat_disp('chef', 2, 4, 17, 90, 'bm.gvdrat'), rat_disp('soldier', 22, 4, 3, 270, 'bm.gvdrat')]

    # ================================================================== admin
    fn('admin/heist_items', [give(i) for i in ('second_wind', 'treasure_map_scrap', 'golden_compass', 'lucky_purse', 'healing_draught', 'master_key', 'lost_lantern', 'rats_foot')] +
       [give(iid) for iid, *_r in PHANTOM])

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s_ = G.FUNCS['loop/second']
    s_[-1:-1] = second


def extend_offers(O, offer):
    pass


def rp(R):
    pass

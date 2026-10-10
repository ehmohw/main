"""2.59: a framed follower moves in.

Put Cecil's Summoning Gem, Emma's Ribbon or Celi's Moon Charm in an item frame (or glow item frame): the follower
steps out of it and makes themselves at home, wandering around the frame (they drift back if they stray too far).
- Right-click the frame: they sit down / get up. (The item doesn't turn - the click is read and undone.)
- Sneak + right-click the frame: send them back into it, or call them out again - so the item can hang there as
  plain decoration.
- Take the item out (or break the frame): they go with it.
- They faint like any follower: 5 minutes later they're back by the frame.
- They won't come out where they won't be summoned (in the market, in a dungeon).
A framed follower is nobody's: its "owner" is an invisible marker armor stand at the frame (the tamed wolf or cat
wanders near it and walks back to it, the vanilla way), carrying an id of its own - so it never follows, buffs or
heals a player, and the player who hung the item can still have their own follower out. Cecil keeps the element of
the player who hung his gem."""
from items import T
from nbt import snbt, B

KINDS = {  # kind: (number, item, host, pet tag, the summon (as the summoner), the dismiss (as anyone, on #me and the select tag), select tag, name, colour)
    'cecil': (1, 'cecil_gem', 'wolf', 'bm.cecilpet', 'p46/pet/summon', 'p46/pet/dismiss', 'bm.cpsel', 'Cecil', '#b48cff'),
    'emma': (2, 'emma_ribbon', 'cat', 'bm.emmapet', 'p57/summon', 'p57/dismiss', 'bm.emsel2', 'Emma', '#ff8ad8'),
    'celi': (3, 'celi_charm', 'wolf', 'bm.celipet', 'p66/summon', 'p66/dismiss', 'bm.cesel2', 'Celi', '#bfe8ff'),
}
CD = 300                                    # seconds before a fainted framed follower comes back
FACE = {0: ('~ ~-1.8 ~', 0), 1: ('~ ~0.1 ~', 0), 2: ('~ ~ ~-0.3', 180), 3: ('~ ~ ~0.3', 0), 4: ('~-0.3 ~ ~', 90), 5: ('~0.3 ~ ~', -90)}


def generate(G):
    fn, title, tellraw, PREFIX = G.fn, G.title, G.tellraw, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    objs = ['bm.ffk', 'bm.ffon', 'bm.ffsit', 'bm.ffcd', 'bm.ffr', 'bm.ffm']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    FR = '@e[type=#bm:p49_frames,tag=bm.ffsel,limit=1]'
    ANC = '@e[type=minecraft:armor_stand,tag=bm.ffas,limit=1]'
    holds = lambda k: f'*[minecraft:custom_data~{{bm:"{KINDS[k][1]}"}}]'
    second, fast = [], []

    # ---- every second: a summoning item newly in a frame?
    second.append('execute as @e[type=#bm:p49_frames,tag=!bm.ff] run function bm:p68/scan')
    fn('p68/scan', [f'execute if items entity @s contents {holds(k)} at @s run return run function bm:p68/new_{k}' for k in KINDS])
    anchor = snbt({'Tags': ['bm.ffa', 'bm.ffnew'], 'Marker': B(1), 'Invisible': B(1), 'NoGravity': B(1), 'Invulnerable': B(1), 'Silent': B(1)})
    for k, (n, _it, _h, _t, _s, _d, _sel, name, col) in KINDS.items():
        fn(f'p68/new_{k}', ['tag @s add bm.ff', 'function bm:p21/pid', 'scoreboard players operation #ff bm.pid = @s bm.pid'] +
           [f'execute if entity @s[nbt={{Facing:{f}b}}] positioned {pos} run summon minecraft:armor_stand ~ ~ ~ {anchor}' for f, (pos, _y) in FACE.items()] +
           [f'execute if entity @s[nbt={{Facing:{f}b}}] run rotate @e[type=minecraft:armor_stand,tag=bm.ffnew,distance=..3,limit=1] {y} 0' for f, (_p, y) in FACE.items()] +
           ['execute as @e[type=minecraft:armor_stand,tag=bm.ffnew,distance=..3] run function bm:p68/init',
            f'scoreboard players set @e[type=minecraft:armor_stand,tag=bm.ffnew,distance=..3] bm.ffk {n}',
            'execute store result score @e[type=minecraft:armor_stand,tag=bm.ffnew,distance=..3] bm.ffr run data get entity @s ItemRotation',
            # (Cecil: the element of whoever hung him up)
            'execute as @p[distance=..8] run scoreboard players operation #el bm.rng = @s bm.cpel',
            'execute unless entity @p[distance=..8] run scoreboard players set #el bm.rng 0',
            'scoreboard players operation @e[type=minecraft:armor_stand,tag=bm.ffnew,distance=..3] bm.cpel = #el bm.rng',
            'execute as @e[type=minecraft:armor_stand,tag=bm.ffnew,distance=..3] at @s run function bm:p68/spawn',
            'tag @e[type=minecraft:armor_stand,tag=bm.ffnew,distance=..3] remove bm.ffnew'])
    fn('p68/init', ['scoreboard players operation @s bm.pid = #ff bm.pid', 'scoreboard players set @s bm.ffon 1', 'scoreboard players set @s bm.ffsit 0',
                    'scoreboard players set @s bm.ffcd 0', 'scoreboard players set @s bm.ffm 0'])
    # (as the anchor, at it) out they come - unless this is somewhere they won't go
    fn('p68/spawn', ['scoreboard players operation #ff bm.pid = @s bm.pid', 'scoreboard players set @s bm.ffm 0', 'scoreboard players set @s bm.ffsit 0',
                     'execute unless function bm:p37/allowed run return run function bm:p68/refuse'] +
       [f'execute if score @s bm.ffk matches {n} run function bm:p68/spawn_{k}' for k, (n, *_r) in KINDS.items()])
    fn('p68/refuse', ['scoreboard players set @s bm.ffon 0',
                      'execute as @a[distance=..10] run ' + say('(Followers won\'t come out of a frame here - it\'s just decoration in this place.)')])
    for k, (n, _it, host, tag, summon, _d, _sel, name, col) in KINDS.items():
        fn(f'p68/spawn_{k}', [f'function bm:{summon}',
                              f'execute as @e[type=minecraft:{host},tag={tag},distance=..4] if score @s bm.pid = #ff bm.pid run tag @s add bm.ffpet',
                              'execute as @a[distance=..10] run ' + title('@s', 'actionbar', [T(f'{name} climbs out of the frame and makes ' + ('herself' if k != 'cecil' else 'himself') + ' at home. ', col),
                                                                                             T('(Right-click the frame: sit / stand. Sneak + right-click: in / out.)', 'gray')])])

    # ---- every second, each anchor: is the frame still there, holding the item? is the follower out? (fainted: back in 5 minutes)
    second.append('execute as @e[type=minecraft:armor_stand,tag=bm.ffa] at @s run function bm:p68/anchor')
    fn('p68/anchor', ['scoreboard players operation #ff bm.pid = @s bm.pid',
                      'execute as @e[type=#bm:p49_frames,tag=bm.ff,distance=..2.5] if score @s bm.pid = #ff bm.pid run tag @s add bm.ffsel',
                      f'execute unless entity {FR} run return run function bm:p68/gone'] +
       [f'execute if score @s bm.ffk matches {n} unless items entity {FR} contents {holds(k)} run return run function bm:p68/gone' for k, (n, *_r) in KINDS.items()] +
       ['tag @e[tag=bm.ffsel] remove bm.ffsel',
        'execute unless score @s bm.ffon matches 1 run return 0',
        'execute if score @s bm.ffcd matches 2.. run return run scoreboard players remove @s bm.ffcd 1',
        'execute if score @s bm.ffcd matches 1 run return run function bm:p68/back',
        'function bm:p68/find',
        'execute unless entity @e[tag=bm.ffp] run scoreboard players add @s bm.ffm 1',
        'execute if entity @e[tag=bm.ffp] run scoreboard players set @s bm.ffm 0',
        # two of them (a chunk that loaded late): the extra one goes
        'execute as @e[tag=bm.ffp,sort=furthest] run function bm:p68/dup',
        'execute if score @s bm.ffsit matches 1 as @e[tag=bm.ffp,tag=!bm.ffdup] run data modify entity @s Sitting set value 1b',
        'execute if score @s bm.ffm matches 3.. run function bm:p68/fainted',
        'tag @e[tag=bm.ffp] remove bm.ffp', 'tag @e[tag=bm.ffdup] remove bm.ffdup'])
    fn('p68/back', ['scoreboard players set @s bm.ffcd 0', 'function bm:p68/spawn'])
    # (#ff = the id) tag the follower(s) of this frame: bm.ffp
    fn('p68/find', [f'execute as @e[type=minecraft:{host},tag={tag},distance=..48] if score @s bm.pid = #ff bm.pid run tag @s add bm.ffp' for host, tag in
                    sorted({(v[2], v[3]) for v in KINDS.values()})])
    fn('p68/dup', ['execute store result score #c bm.rng if entity @e[tag=bm.ffp,tag=!bm.ffdup]', 'execute if score #c bm.rng matches ..1 run return 0',
                   'tag @s add bm.ffdup', 'execute at @s run function bm:p68/drop'])
    # (as a follower, at it) send it off, its own way
    fn('p68/drop', ['scoreboard players operation #me bm.pid = @s bm.pid'] +
       [f'execute if entity @s[tag={tag}] run return run function bm:p68/drop_{k}' for k, (_n, _i, _h, tag, *_r) in KINDS.items()])
    for k, (_n, _i, _h, _t, _s, dismiss, sel, *_r) in KINDS.items():
        fn(f'p68/drop_{k}', [f'tag @s add {sel}', f'function bm:{dismiss}', f'tag @e[tag={sel}] remove {sel}'])
    fn('p68/fainted', [f'scoreboard players set @s bm.ffcd {CD}', 'scoreboard players set @s bm.ffm 0', 'scoreboard players set @s bm.ffsit 0'] +
       [f'execute if score @s bm.ffk matches {n} run ' + tellraw('@a[distance=..32]', PREFIX + [T(f'{name} faints! ', col, bold=True),
                                                                                              T(f'Back by the frame in {CD // 60} minutes.', 'gray')])
        for k, (n, _i, _h, _t, _s, _d, _sel, name, col) in KINDS.items()])
    # the frame's gone, or the item's out of it: the follower goes, and so does the anchor
    fn('p68/gone', ['tag @e[tag=bm.ffsel] remove bm.ff', 'tag @e[tag=bm.ffsel] remove bm.ffsel', 'function bm:p68/find',
                    'execute as @e[tag=bm.ffp] at @s run function bm:p68/drop', 'tag @e[tag=bm.ffp] remove bm.ffp', 'kill @s'])
    # ---- every 5 ticks: a framed follower's frame was clicked (its item turned)? Undo the turn; sit/stand, or (sneaking) in/out
    fast.append('execute as @e[type=#bm:p49_frames,tag=bm.ff] at @s run function bm:p68/rot')
    fn('p68/rot', ['scoreboard players operation #ff bm.pid = @s bm.pid',
                   'execute as @e[type=minecraft:armor_stand,tag=bm.ffa,distance=..2.5] if score @s bm.pid = #ff bm.pid run tag @s add bm.ffas',
                   f'execute unless entity {ANC} run return 0',
                   'execute store result score #r bm.rng run data get entity @s ItemRotation',
                   f'execute if score #r bm.rng = {ANC} bm.ffr run return run tag @e[tag=bm.ffas] remove bm.ffas',
                   f'execute store result entity @s ItemRotation byte 1 run scoreboard players get {ANC} bm.ffr',
                   'execute as @p[distance=..7,gamemode=!spectator] if predicate bm:p20/sneaking run tag @s add bm.ffsn',
                   'execute if entity @p[distance=..7,tag=bm.ffsn] as @p[distance=..7,tag=bm.ffsn] at @s run function bm:p68/toggle_on',
                   'execute unless entity @p[distance=..7,tag=bm.ffsn] as @p[distance=..7,gamemode=!spectator] at @s run function bm:p68/toggle_sit',
                   'tag @a[tag=bm.ffsn] remove bm.ffsn', 'tag @e[tag=bm.ffas] remove bm.ffas'])
    # (as the player who clicked; the anchor tagged bm.ffas, #ff its id)
    names = lambda lines_for: [f'execute if score {ANC} bm.ffk matches {n} run ' + lines_for(k, name, col) for k, (n, _i, _h, _t, _s, _d, _sel, name, col) in KINDS.items()]
    pron = lambda k: 'him' if k == 'cecil' else 'her'
    fn('p68/toggle_on', [f'execute if score {ANC} bm.ffon matches 1 run return run function bm:p68/send_in', 'function bm:p68/call_out'])
    fn('p68/send_in', [f'scoreboard players set {ANC} bm.ffon 0', f'scoreboard players set {ANC} bm.ffsit 0',
                       f'execute as {ANC} at @s run function bm:p68/find', 'execute as @e[tag=bm.ffp] at @s run function bm:p68/drop', 'tag @e[tag=bm.ffp] remove bm.ffp',
                       'playsound minecraft:entity.item_frame.rotate_item block @a[distance=..12] ~ ~ ~ 1 0.6'] +
       names(lambda k, name, col: title('@s', 'actionbar', [T(f'{name} steps back into the frame. ', col), T(f'(Sneak + right-click to call {pron(k)} out again.)', 'gray')])))
    fn('p68/call_out', [f'scoreboard players set {ANC} bm.ffon 1', f'execute if score {ANC} bm.ffcd matches 1.. run return run function bm:p68/resting',
                        f'execute as {ANC} at @s run function bm:p68/spawn'])
    fn('p68/resting', [f'execute store result score #m bm.rng run scoreboard players get {ANC} bm.ffcd', 'scoreboard players add #m bm.rng 59',
                       'scoreboard players operation #m bm.rng /= #60 bm.rng'] +
       names(lambda k, name, col: title('@s', 'actionbar', [T(f'{name} is still recovering - out in about ', 'gray'), {'score': {'name': '#m', 'objective': 'bm.rng'}, 'color': 'white'},
                                                            T(' min.', 'gray')])))
    fn('p68/toggle_sit', [f'execute unless score {ANC} bm.ffon matches 1 run return run function bm:p68/sit_off',
                          f'execute as {ANC} at @s run function bm:p68/find',
                          f'execute unless entity @e[tag=bm.ffp] run return run function bm:p68/sit_none',
                          f'execute if score {ANC} bm.ffsit matches 1 run return run function bm:p68/stand', 'function bm:p68/sit'])
    fn('p68/sit', [f'scoreboard players set {ANC} bm.ffsit 1', 'execute as @e[tag=bm.ffp] run data modify entity @s Sitting set value 1b', 'tag @e[tag=bm.ffp] remove bm.ffp'] +
       names(lambda k, name, col: title('@s', 'actionbar', T(f'{name} sits down by the frame.', col))))
    fn('p68/stand', [f'scoreboard players set {ANC} bm.ffsit 0', 'execute as @e[tag=bm.ffp] run data modify entity @s Sitting set value 0b', 'tag @e[tag=bm.ffp] remove bm.ffp'] +
       names(lambda k, name, col: title('@s', 'actionbar', T(f'{name} gets up and wanders about.', col))))
    fn('p68/sit_off', names(lambda k, name, col: title('@s', 'actionbar', T(f'(The frame is just decoration now. Sneak + right-click to call {name} out.)', 'gray'))))
    fn('p68/sit_none', ['tag @e[tag=bm.ffp] remove bm.ffp'] + names(lambda k, name, col: title('@s', 'actionbar', T(f'({name} isn\'t here right now.)', 'gray'))))

    s = G.FUNCS['loop/second']
    s[-1:-1] = second
    f = G.FUNCS['loop/fast']
    f[-1:-1] = fast

"""2.62: bottled creatures in display cases, Cecil's click box (sit, gems, fire cooking), the Fixer's Calling Card,
wider crypt tunnels (old crypts too), glowing signs, followers that go home cleanly, and fixes.

BOTTLED CREATURES ON SHOW: put a full Smuggler's Jar in a display case and the creature inside appears on the cushion,
  shrunk to fit (floor or wall case), still as a statue (no AI, can't be hurt, can't be pushed). Sneak + right-click: it
  turns. Take the jar back out (empty-handed) or pick the case up and the creature goes back in the jar, unharmed.
CECIL: his whole body can be clicked now (it used to be only the invisible dog under him). Right-click: sit / follow.
  With a gem: as before (it takes the gem; sneak + empty hand takes it back). With FIRE magic (or Ethereal), right-click
  him holding raw food: he breathes on it - the whole stack comes out cooked.
THE FIXER'S CALLING CARD (first clear of a Tier II heist; Goldtooth sells more): use it and pick a player - ask to go to
  them, or ask them to come to you. They get [Accept] / [Deny] in chat (60 seconds). Any distance, any dimension (not
  from or into the vault). No cooldown, never runs out.
THE CRYPT: tunnels 3 wide (were 2) - room to slip past the Warden. Existing crypts are rebuilt the first time someone
  comes near (while nobody is down there and the Warden sleeps).
SIGNS: every sign in the graveyard, crypt and market glows now (and old ones are lit when you come by).
FOLLOWERS (Cecil, Emma, Celi, Zib, Skiff Escorts) go home - quietly, no cooldown - when you get too far away (another
  dimension, a long teleport, logging off), and when their item leaves your inventory (into a chest, a barrel, dropped)
  for 3 seconds. Use the item again to call them. A copy left behind in some far-off chunk can never come back as a
  double: each call gets a fresh ticket and old ones dismiss themselves.
FIXES: one Dockmaster per market (extras removed); Pearlman's model goes when he does; the Fence no longer buys emeralds;
  Celi's spear no longer clips her hair; Emma wears her own blue by default (Healing); crash-site Xenite Altars can be
  picked up (sneak + punch)."""
import json
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, D, Int
import rot
import phase70 as P70
from phase46 import EL_KEYS

GOLD = '#ffcf40'
MENU = 1310
STAY = 60                       # seconds a teleport request stays open

item('fixers_card', TOTEM, "Fixer's Calling Card", GOLD,
     ['Gold-edged, smells of cigar smoke.', ('Use: pick a player - ask to go to them,', 'blue'), ('or ask them to come to you.', 'blue'),
      ('They accept or decline in chat.', 'gray'), ('Any distance, any dimension. Never runs out.', 'gray'), ('(No signal inside the vault.)', 'dark_gray')],
     model='bm:fixers_card', stack=1, cat='magic', glint=True, comps=hold('none'), tier=2)
HOLD['fixers_card'] = 'bm:p73/tp/use'
P70.GOLDTOOTH_STOCK.append((40, 'fixers_card', 1))

# creature sizes (width, height) for fitting a jar's creature into a case
DIMS = {'allay': (.35, .6), 'armadillo': (.7, .65), 'axolotl': (.75, .42), 'bat': (.5, .9), 'bee': (.7, .6), 'blaze': (.6, 1.8), 'bogged': (.6, 2.0),
        'breeze': (.6, 1.77), 'camel': (1.7, 2.4), 'camel_husk': (1.7, 2.4), 'cat': (.6, .7), 'cave_spider': (.7, .5), 'chicken': (.4, .7), 'cod': (.5, .3),
        'copper_golem': (.5, 1.0), 'cow': (.9, 1.4), 'creaking': (.9, 2.7), 'creeper': (.6, 1.7), 'dolphin': (.9, .6), 'donkey': (1.4, 1.5),
        'drowned': (.6, 1.95), 'enderman': (.6, 2.9), 'endermite': (.4, .3), 'evoker': (.6, 1.95), 'fox': (.6, .7), 'frog': (.5, .5), 'ghast': (4, 4),
        'glow_squid': (.8, .8), 'goat': (.9, 1.3), 'guardian': (.85, .85), 'happy_ghast': (4, 4), 'hoglin': (1.4, 1.4), 'horse': (1.4, 1.6),
        'husk': (.6, 1.95), 'iron_golem': (1.4, 2.7), 'llama': (.9, 1.87), 'magma_cube': (2, 2), 'mooshroom': (.9, 1.4), 'mule': (1.4, 1.6),
        'nautilus': (.9, .95), 'ocelot': (.6, .7), 'panda': (1.3, 1.25), 'parched': (.6, 2.0), 'parrot': (.5, .9), 'phantom': (.9, .5), 'pig': (.9, .9),
        'piglin': (.6, 1.95), 'piglin_brute': (.6, 1.95), 'pillager': (.6, 1.95), 'polar_bear': (1.4, 1.4), 'pufferfish': (.7, .7), 'rabbit': (.4, .5),
        'ravager': (1.95, 2.2), 'salmon': (.7, .4), 'sheep': (.9, 1.3), 'shulker': (1, 1), 'silverfish': (.4, .3), 'skeleton': (.6, 2.0),
        'skeleton_horse': (1.4, 1.6), 'slime': (2, 2), 'sniffer': (1.9, 1.75), 'snow_golem': (.7, 1.9), 'spider': (1.4, .9), 'squid': (.8, .8),
        'stray': (.6, 2.0), 'strider': (.9, 1.7), 'sulfur_cube': (1, 1), 'tadpole': (.4, .3), 'trader_llama': (.9, 1.87), 'tropical_fish': (.5, .4),
        'turtle': (1.2, .4), 'vex': (.4, .8), 'villager': (.6, 1.95), 'vindicator': (.6, 1.95), 'wandering_trader': (.6, 1.95), 'witch': (.6, 1.95),
        'wither_skeleton': (.7, 2.4), 'wolf': (.6, .85), 'zoglin': (1.4, 1.4), 'zombie': (.6, 1.95), 'zombie_horse': (1.4, 1.6),
        'zombie_nautilus': (.9, .95), 'zombie_villager': (.6, 1.95), 'zombified_piglin': (.6, 1.95)}
RAW = {'beef': 'cooked_beef', 'porkchop': 'cooked_porkchop', 'chicken': 'cooked_chicken', 'mutton': 'cooked_mutton', 'rabbit': 'cooked_rabbit',
       'cod': 'cooked_cod', 'salmon': 'cooked_salmon', 'potato': 'baked_potato', 'kelp': 'dried_kelp'}
FOLLOW = [   # kind, host type, host tag, item, "goes away" function, name, ticket objective
    ('cecil', 'wolf', 'bm.cecilpet', 'cecil_gem', 'p62/cecil_go', 'Cecil', 'bm.fgc', 'p46/pet/summon'),
    ('emma', 'cat', 'bm.emmapet', 'emma_ribbon', 'p62/emma_go', 'Emma', 'bm.fge', 'p57/summon_here'),
    ('celi', 'wolf', 'bm.celipet', 'celi_charm', 'p66/go', 'Celi', 'bm.fgl', 'p66/summon_here'),
    ('zib', 'wolf', 'bm.zibpet', 'donadian_medal', 'p72/zb/beamup', 'Zib', 'bm.fgz', 'p72/zb/summon')]
CRYPT_CTRL = (15.5, 2, 49.5)


def follow_rules(G, entry, second):
    """(2.65: shared) a follower goes home when its owner's gone, too far, or its item's put away; one ticket per call"""
    fn, tellraw, PREFIX = G.fn, G.tellraw, G.PREFIX
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    kind, host, tag, iid, go, name, obj, summon = entry
    G.FUNCS[summon] += [f'scoreboard players add @s {obj} 1', 'scoreboard players operation #fgp bm.rng = @s bm.pid', f'scoreboard players operation #fgv bm.rng = @s {obj}',
                        f'execute as @e[type=minecraft:{host},tag={tag},distance=..6] if score @s bm.pid = #fgp bm.rng run scoreboard players operation @s {obj} = #fgv bm.rng',
                        f'execute as @e[type=minecraft:{host},tag={tag},distance=..6] if score @s bm.pid = #fgp bm.rng run scoreboard players set @s bm.fmis 0']
    own = '@a[tag=bm.fown,limit=1]'
    second.append(f'execute as @e[type=minecraft:{host},tag={tag},tag=!bm.ffpet] at @s run function bm:p73/fol/{kind}')
    fn(f'p73/fol/{kind}', ['scoreboard players operation #me bm.pid = @s bm.pid', 'tag @a remove bm.fown',
                           'execute as @a if score @s bm.pid = #me bm.pid run tag @s add bm.fown',
                           f'execute unless entity @a[tag=bm.fown] run return run function bm:{go}',
                           f'execute unless score {own} {obj} matches 0.. run scoreboard players set {own} {obj} 0',
                           f'execute unless score @s {obj} matches 0.. run scoreboard players operation @s {obj} = {own} {obj}',
                           f'execute unless score @s {obj} = {own} {obj} run return run function bm:{go}',
                           f'execute unless entity @a[tag=bm.fown,distance=..96] run return run function bm:p73/fol/{kind}_far',
                           f'execute if items entity {own} container.* {holds(iid)} run return run scoreboard players set @s bm.fmis 0',
                           f'execute if items entity {own} weapon.offhand {holds(iid)} run return run scoreboard players set @s bm.fmis 0',
                           f'execute if items entity {own} player.cursor {holds(iid)} run return run scoreboard players set @s bm.fmis 0',
                           'scoreboard players add @s bm.fmis 1', f'execute if score @s bm.fmis matches 3.. run function bm:p73/fol/{kind}_stash',
                           'tag @a remove bm.fown'])
    the = '' if "'s " in ITEMS[iid]['name'] else 'the '          # (2.78: "Tullius's Frozen Doubloon", "the Signet of the Frog Knight")
    fn(f'p73/fol/{kind}_far', [f'function bm:{go}', tellraw('@a[tag=bm.fown]', PREFIX + [T(f'{name} couldn\'t keep up and went home. ', 'gray'),
                                                                                          T(f'(Use {the}{ITEMS[iid]["name"]} to call {"her" if kind in ("emma", "celi") else "him"} again.)', 'dark_gray')]),
                               'tag @a remove bm.fown'])
    fn(f'p73/fol/{kind}_stash', [f'function bm:{go}', tellraw('@a[tag=bm.fown]', PREFIX + [T(f'You put {the}{ITEMS[iid]["name"]} away - {name} heads home.', 'gray')]),
                                 'tag @a remove bm.fown'])


def extend_offers(O, offer):
    pass


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    tick, fast, second = [], [], []
    objs = ['bm.tpq', 'bm.tpk', 'bm.tpt', 'bm.fmis'] + [f[6] for f in FOLLOW]
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs

    # ================================================================== BOTTLED CREATURES IN DISPLAY CASES
    sel = '@e[type=minecraft:item_display,tag=bm.dcsel,limit=1]'
    put = G.FUNCS['p72/dc/put']
    k = next(i for i, l in enumerate(put) if 'set_count",count:1' in l)
    put.insert(k + 1, f'execute if data entity {sel} item.components."minecraft:custom_data".jar as @e[type=minecraft:interaction,tag=bm.dcme,limit=1] at @s run function bm:p73/dcm/show')
    G.FUNCS['p72/dc/take'].insert(0, 'execute as @e[type=minecraft:interaction,tag=bm.dcme,limit=1] at @s run function bm:p73/dcm/clear')
    G.FUNCS['p72/dc/drop'].insert(0, 'function bm:p73/dcm/clear')
    G.FUNCS['p72/dc/spin_toggle'] += ['execute as @e[type=minecraft:interaction,tag=bm.dcme,limit=1] at @s run tag @e[tag=bm.dcmob,distance=..0.8] add bm.dcmspin']
    G.FUNCS['p72/dc/spin_off'] += ['execute as @e[type=minecraft:interaction,tag=bm.dcme,limit=1] at @s run tag @e[tag=bm.dcmob,distance=..0.8] remove bm.dcmspin']
    size = []
    for t, (w, h) in DIMS.items():
        fs = max(0.0625, min(1.0, 0.58 / h, 0.62 / w)); ws = max(0.0625, min(1.0, 0.55 / h, 0.3 / w))
        size.append(f'execute if data storage bm:dcm {{j:{{eid:"minecraft:{t}"}}}} run data modify storage bm:dcm s set value {{f:{fs:.3f}d,w:{ws:.3f}d}}')
    fn('p73/dcm/size', size)
    case = '@e[type=minecraft:item_display,tag=bm.dcase,distance=..0.05,limit=1]'
    fn('p73/dcm/show', [f'data modify storage bm:dcm j set from entity {sel} item.components."minecraft:custom_data".jar',
                        'data modify storage bm:dcm data set from storage bm:dcm j.data', 'data modify storage bm:dcm eid set from storage bm:dcm j.eid'] +
       [f'data remove storage bm:dcm data.{k}' for k in ('UUID', 'Pos', 'Rotation', 'Motion', 'Passengers', 'leash', 'Leash', 'Brain', 'HurtTime', 'DeathTime')] +
       [f'data modify storage bm:dcm data.{k} set value 1b' for k in ('NoAI', 'Invulnerable', 'Silent', 'PersistenceRequired', 'NoGravity')] +
       ['data modify storage bm:dcm data.Tags append value "bm.dcmob"', 'data modify storage bm:dcm data.Tags append value "bm.dcmnew"',
        'data remove storage bm:dcm data.attributes[{id:"minecraft:scale"}]',
        'data modify storage bm:dcm s set value {f:0.3d,w:0.25d}', 'function bm:p73/dcm/size',
        'data modify storage bm:dcm data.attributes append value {id:"minecraft:scale",base:0.3d}',
        'execute if entity @s[nbt={width:0.6f}] run data modify storage bm:dcm data.attributes[-1].base set from storage bm:dcm s.w',
        'execute unless entity @s[nbt={width:0.6f}] run data modify storage bm:dcm data.attributes[-1].base set from storage bm:dcm s.f',
        # on a seat (a ridden mob can't be pushed out of its case), on the cushion, facing out
        'execute unless entity @s[nbt={width:0.6f}] positioned ~ ~0.25 ~ run function bm:p73/dcm/place',
        f'execute if entity @s[nbt={{width:0.6f}}] rotated as {case} positioned ^ ^0.05 ^-0.03 run function bm:p73/dcm/place',
        f'execute if entity @e[tag=bm.dcmob,distance=..0.8] run data merge entity {sel} {{transformation:{{scale:[0f,0f,0f]}}}}'])
    fn('p73/dcm/place', ['summon minecraft:block_display ~ ~ ~ {Tags:["bm.dcseat","bm.dcsnew"]}', 'function bm:p73/dcm/summon with storage bm:dcm',
                         'ride @e[tag=bm.dcmnew,limit=1,sort=nearest] mount @e[type=minecraft:block_display,tag=bm.dcsnew,limit=1,sort=nearest]',
                         f'execute rotated as {case.replace("distance=..0.05", "distance=..0.6")} run rotate @e[tag=bm.dcmnew,limit=1,sort=nearest] ~ 0',
                         'execute unless entity @e[tag=bm.dcmnew,distance=..1] run kill @e[type=minecraft:block_display,tag=bm.dcsnew,distance=..0.1]',
                         'execute if entity @e[tag=bm.dcmnew,distance=..1] run particle minecraft:poof ~ ~0.2 ~ 0.15 0.15 0.15 0.01 8',
                         'execute if entity @e[tag=bm.dcmnew,distance=..1] run playsound minecraft:item.bottle.empty block @a[distance=..16] ~ ~ ~ 0.8 1.2',
                         'tag @e[tag=bm.dcmnew] remove bm.dcmnew', 'tag @e[tag=bm.dcsnew] remove bm.dcsnew'])
    fn('p73/dcm/summon', ['$execute store success score #dok bm.rng run summon $(eid) ~ ~ ~ $(data)'])
    fn('p73/dcm/clear', ['execute as @e[tag=bm.dcmob,distance=..0.8] at @s run function bm:p73/dcm/vanish', 'kill @e[type=minecraft:block_display,tag=bm.dcseat,distance=..0.8]',
                         'execute as @e[type=minecraft:item_display,tag=bm.dcitem,distance=..0.05] run data merge entity @s {transformation:{scale:[0.5f,0.5f,0.5f]}}'])
    fn('p73/dcm/vanish', ['particle minecraft:poof ~ ~0.2 ~ 0.15 0.15 0.15 0.01 8', 'ride @s dismount', 'tp @s ~ -2000 ~', 'kill @s'])
    tick.append('execute as @e[tag=bm.dcmspin] at @s run rotate @s ~3 ~')

    # ================================================================== CECIL: a click box the size of him
    P46_FIRE = EL_KEYS.index('fire') + 1
    from phase69 import ETH_I
    wjson('bm/tags/item/p73_raw.json', {'values': [f'minecraft:{r}' for r in RAW]})
    fn('p73/cec/has_hit', ['execute on passengers if entity @s[type=minecraft:interaction,tag=bm.cphit] run return 1', 'return 0'])
    second.append('execute as @e[type=minecraft:wolf,tag=bm.cecilpet,tag=!bm.ffpet] unless function bm:p73/cec/has_hit at @s run function bm:p73/cec/add_hit')
    fn('p73/cec/add_hit', ['summon minecraft:interaction ~ ~ ~ {Tags:["bm.cphit","bm.cphnew"],width:0.8f,height:0.95f,response:1b}',
                           'ride @e[type=minecraft:interaction,tag=bm.cphnew,limit=1,sort=nearest] mount @s', 'tag @e[tag=bm.cphnew] remove bm.cphnew'])
    second.append('execute as @e[type=minecraft:interaction,tag=bm.cphit] unless function bm:p20/frog/has_vehicle run kill @s')
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.cphit] if data entity @s interaction run function bm:p73/cec/click',
             'execute as @e[type=minecraft:interaction,tag=bm.cphit] if data entity @s attack run data remove entity @s attack']
    cw = '@e[type=minecraft:wolf,tag=bm.cpclk,limit=1]'
    gems = [f'gem_{k}' for k in EL_KEYS] + ['ethereal_gem']
    fn('p73/cec/click', ['execute on vehicle run tag @s add bm.cpclk', 'execute on target at @s run function bm:p73/cec/who', 'tag @e[tag=bm.cpclk] remove bm.cpclk',
                         'data remove entity @s interaction'])
    # (one right-click can reach both the dog and the box - handle it once)
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.cpck dummy']
    G.OBJECTIVES.append('bm.cpck')
    tick.append('scoreboard players remove @a[scores={bm.cpck=1..}] bm.cpck 1')
    fn('p73/cec/who', ['execute if score @s bm.cpck matches 1.. run return 0', 'scoreboard players set @s bm.cpck 10',
                       'scoreboard players operation #me bm.pid = @s bm.pid',
                       f'execute unless score {cw} bm.pid = #me bm.pid run return run ' + say('Cecil ignores you. ("Not my summoner.")', '#b48cff'),
                       f'execute store success score #s0 bm.rng if data entity {cw} {{Sitting:1b}}',
                       'execute if predicate bm:p20/sneaking unless items entity @s weapon.mainhand * run return run function bm:p73/cec/take'] +
       [f'execute if items entity @s weapon.mainhand {holds(g)} run return run function bm:p73/cec/gem' for g in gems] +
       [f'execute if items entity @s weapon.mainhand #bm:p73_raw if score {cw} bm.cpel matches {P46_FIRE} run return run function bm:p73/cec/cook',
        f'execute if items entity @s weapon.mainhand #bm:p73_raw if score {cw} bm.cpel matches {ETH_I} run return run function bm:p73/cec/cook',
        f'execute if score #s0 bm.rng matches 1 run data modify entity {cw} Sitting set value 0b',
        f'execute if score #s0 bm.rng matches 0 run data modify entity {cw} Sitting set value 1b',
        'execute if score #s0 bm.rng matches 1 run ' + say('Cecil hops up. "Off we go, then."', '#b48cff'),
        'execute if score #s0 bm.rng matches 0 run ' + say('Cecil sits down and leans on his staff. "I\'ll be right here."', '#b48cff')])
    fn('p73/cec/gem', ['scoreboard players set #cphit bm.rng 1', 'function bm:p46/el/interact', 'scoreboard players set #cphit bm.rng 0'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #cphit bm.rng 0']
    # (taking his gem back undoes a sit-toggle that only a click on the dog under him makes - put his pose back as it was)
    fn('p73/cec/take', ['scoreboard players set #cphit bm.rng 1', 'function bm:p69/take', 'scoreboard players set #cphit bm.rng 0', f'execute if score #s0 bm.rng matches 1 run data modify entity {cw} Sitting set value 1b',
                        f'execute if score #s0 bm.rng matches 0 run data modify entity {cw} Sitting set value 0b'])
    fn('p73/cec/cook', [f'execute if items entity @s weapon.mainhand minecraft:{r} run item modify entity @s weapon.mainhand {{function:"minecraft:set_item",item:"minecraft:{c}"}}'
                        for r, c in RAW.items()] +
       [f'execute at {cw} run particle minecraft:flame ~ ~1.1 ~ 0.25 0.2 0.25 0.03 20', f'execute at {cw} run particle minecraft:small_flame ~ ~1 ~ 0.3 0.3 0.3 0.01 12',
        'playsound minecraft:entity.blaze.shoot player @a[distance=..16] ~ ~ ~ 0.6 1.4', 'playsound minecraft:block.fire.ambient player @s ~ ~ ~ 1 1',
        say('Cecil breathes on it - fwoosh! "Done to a turn. Hehehe."', '#ff8a3a')])
    # (a click on the dog under him: the same cooking - that click also sat him down or stood him up, so undo that)
    it = G.FUNCS['p46/el/interact']
    it[1:1] = ['execute unless score #cphit bm.rng matches 1 if score @s bm.cpck matches 1.. run return 0',
               'execute unless score #cphit bm.rng matches 1 run scoreboard players set @s bm.cpck 10',f'execute if items entity @s weapon.mainhand #bm:p73_raw if score @s bm.cpel matches {P46_FIRE} run return run function bm:p73/cec/cook_dog',
               f'execute if items entity @s weapon.mainhand #bm:p73_raw if score @s bm.cpel matches {ETH_I} run return run function bm:p73/cec/cook_dog']
    sel_pet = 'execute as @e[type=minecraft:wolf,tag=bm.cecilpet,tag=!bm.ffpet,distance=..8] if score @s bm.pid = #me bm.pid'
    fn('p73/cec/cook_dog', ['scoreboard players operation #me bm.pid = @s bm.pid', f'{sel_pet} run tag @s add bm.cpclk',
                            f'execute unless entity {cw} run return 0',
                            f'execute store success score #s0 bm.rng if data entity {cw} {{Sitting:1b}}',
                            f'execute if score #s0 bm.rng matches 1 run data modify entity {cw} Sitting set value 0b',
                            f'execute if score #s0 bm.rng matches 0 run data modify entity {cw} Sitting set value 1b',
                            'function bm:p73/cec/cook', 'tag @e[tag=bm.cpclk] remove bm.cpclk'])

    # ================================================================== THE FIXER'S CALLING CARD
    # the menu: one row per other player online (their name read off a scrap display): go to them / bring them
    fn('p73/tp/use', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                      'execute if dimension bm:gutter run return run ' + say('No signal down here in the vault.', 'red'),
                      'tag @s add bm.tpme', 'data modify storage bm:tp acts set value []',
                      'execute as @a[tag=!bm.tpme] at @s run function bm:p73/tp/btn', 'tag @s remove bm.tpme',
                      'execute unless data storage bm:tp acts[0] run return run ' + say('Nobody else is about to call on.'),
                      f'scoreboard players set @s bm.menu {MENU}', 'function bm:p73/tp/show with storage bm:tp',
                      'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 1.2'])
    dlg = ('{type:"minecraft:multi_action",title:' + snbt(T("Fixer's Calling Card", GOLD, bold=True)) +
           ',body:[{type:"minecraft:plain_message",width:260,contents:' + snbt(T('Who are you calling on? They get to say yes or no.', 'gray')) + '}]'
           ',actions:$(acts),columns:2,exit_action:{label:"Close"},pause:false,after_action:"close"}')
    fn('p73/tp/show', [f'$dialog show @s {dlg}'])
    fn('p73/tp/btn', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                      'summon minecraft:item_display ~ ~-64 ~ {Tags:["bm.tpn"],item:{id:"minecraft:paper",count:1}}',
                      'item modify entity @e[type=minecraft:item_display,tag=bm.tpn,limit=1] contents {function:"minecraft:set_name",target:"custom_name",entity:"this",name:{selector:"@s"}}',
                      'data modify storage bm:tp nm set from entity @e[type=minecraft:item_display,tag=bm.tpn,limit=1] item.components."minecraft:custom_name"',
                      'kill @e[type=minecraft:item_display,tag=bm.tpn]',
                      'scoreboard players operation #c bm.rng = @s bm.pid', 'scoreboard players add #c bm.rng 8000000',
                      'execute store result storage bm:tp go int 1 run scoreboard players get #c bm.rng', 'scoreboard players add #c bm.rng 1000000',
                      'execute store result storage bm:tp bring int 1 run scoreboard players get #c bm.rng', 'function bm:p73/tp/btn2 with storage bm:tp'])
    fn('p73/tp/btn2', ['$data modify storage bm:tp acts append value {label:[{text:"Go to ",color:"#ffcf40"},$(nm)],width:150,'
                       'tooltip:{text:"Ask to teleport to them",color:"gray"},action:{type:"minecraft:run_command",command:"/trigger bm.act set $(go)"}}',
                       '$data modify storage bm:tp acts append value {label:[{text:"Bring ",color:"#7ad0ea"},$(nm)],width:150,'
                       'tooltip:{text:"Ask them to teleport to you",color:"gray"},action:{type:"minecraft:run_command",command:"/trigger bm.act set $(bring)"}}'])
    G.FUNCS['p28/act'] += ['execute if score #act bm.pay matches 8000001..8999999 run return run function bm:p73/tp/ask_go',
                           'execute if score #act bm.pay matches 9000001..9999999 run return run function bm:p73/tp/ask_bring',
                           'execute if score #act bm.pay matches 7711 run return run function bm:p73/tp/accept',
                           'execute if score #act bm.pay matches 7712 run return run function bm:p73/tp/deny']
    for kind, off, k in (('go', 8000000, 1), ('bring', 9000000, 2)):
        fn(f'p73/tp/ask_{kind}', [f'execute unless score @s bm.menu matches {MENU} run return run function bm:p28/stale',
                                  f'execute unless items entity @s container.* {holds("fixers_card")} unless items entity @s weapon.offhand {holds("fixers_card")} run return run function bm:p28/stale',
                                  'scoreboard players set @s bm.menu 0',
                                  f'scoreboard players operation #t bm.rng = #act bm.pay', f'scoreboard players remove #t bm.rng {off}',
                                  'execute if score #t bm.rng = @s bm.pid run return 0',
                                  'tag @a remove bm.tptg', 'execute as @a if score @s bm.pid = #t bm.rng run tag @s add bm.tptg',
                                  'execute unless entity @a[tag=bm.tptg] run return run ' + say('They\'ve gone offline.'),
                                  'scoreboard players operation @a[tag=bm.tptg] bm.tpq = @s bm.pid', f'scoreboard players set @a[tag=bm.tptg] bm.tpk {k}',
                                  f'scoreboard players set @a[tag=bm.tptg] bm.tpt {STAY}',
                                  tellraw('@a[tag=bm.tptg]', PREFIX + [{'selector': '@s', 'color': 'white'},
                                                                       T(' wants to teleport to you. ' if k == 1 else ' asks you to teleport to them. ', GOLD),
                                                                       T('[Accept]', 'green', bold=True, click_event={'action': 'run_command', 'command': '/trigger bm.act set 7711'},
                                                                         hover_event={'action': 'show_text', 'value': T('Yes, come on over' if k == 1 else 'Take me there', 'gray')}),
                                                                       T(' ', 'gray'),
                                                                       T('[Deny]', 'red', bold=True, click_event={'action': 'run_command', 'command': '/trigger bm.act set 7712'}),
                                                                       T(f' ({STAY} s)', 'dark_gray')]),
                                  'execute as @a[tag=bm.tptg] at @s run playsound minecraft:block.note_block.bell player @s ~ ~ ~ 1 1.4',
                                  tellraw('@s', PREFIX + [T('Request sent to ', 'gray'), {'selector': '@a[tag=bm.tptg]', 'color': 'white'}, T('.', 'gray')]),
                                  'tag @a remove bm.tptg'])
    fn('p73/tp/accept', ['execute unless score @s bm.tpt matches 1.. run return run ' + say('No teleport request waiting for you.'),
                         'tag @s add bm.tpme2', 'tag @a remove bm.tprq', 'scoreboard players set @s bm.tpt 0',
                         'execute as @a if score @s bm.pid = @a[tag=bm.tpme2,limit=1] bm.tpq run tag @s add bm.tprq',
                         'execute unless entity @a[tag=bm.tprq] run return run ' + say('They\'ve gone offline.'),
                         'execute if dimension bm:gutter run return run ' + say('No signal down here in the vault.', 'red'),
                         'execute as @a[tag=bm.tprq] at @s if dimension bm:gutter run tag @s add bm.tpv',
                         'execute if entity @a[tag=bm.tpv] run return run ' + say('They\'re in the vault - no signal there.', 'red'),
                         'execute at @s run particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.6 0.3 0.05 40',
                         'execute as @a[tag=bm.tprq] at @s run particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.6 0.3 0.05 40',
                         'execute if score @s bm.tpk matches 1 run tp @a[tag=bm.tprq,limit=1] @s',
                         'execute if score @s bm.tpk matches 2 run tp @s @a[tag=bm.tprq,limit=1]',
                         'execute at @s run playsound minecraft:entity.enderman.teleport player @a[distance=..16] ~ ~ ~ 1 1.2',
                         'execute at @s run particle minecraft:portal ~ ~1 ~ 0.4 0.8 0.4 0.4 40',
                         tellraw('@a[tag=bm.tprq]', PREFIX + [{'selector': '@s', 'color': 'white'}, T(' accepted.', 'green')]),
                         'tag @a remove bm.tprq', 'tag @s remove bm.tpme2'])
    fn('p73/tp/deny', ['execute unless score @s bm.tpt matches 1.. run return run ' + say('No teleport request waiting for you.'),
                       'scoreboard players set @s bm.tpt 0', 'tag @s add bm.tpme2',
                       'execute as @a if score @s bm.pid = @a[tag=bm.tpme2,limit=1] bm.tpq run ' + tellraw('@s', PREFIX + [{'selector': '@a[tag=bm.tpme2]', 'color': 'white'}, T(' declined.', 'red')]),
                       'tag @s remove bm.tpme2', say('Declined.')])
    second.append('scoreboard players remove @a[scores={bm.tpt=1..}] bm.tpt 1')
    tick += ['tag @a[tag=bm.tpme2] remove bm.tpme2', 'tag @a[tag=bm.tpv] remove bm.tpv']
    fc = G.FUNCS['p70/first_clear']
    fc.insert(1, 'execute if score #gt bm.rng matches 2 run loot give @s loot bm:items/fixers_card')
    fn('admin/fixers_card', [give('fixers_card')])

    # ================================================================== THE CRYPT: wider tunnels (old crypts rebuilt once) and lit signs
    import structures as S
    NB = S.build_graveyard()
    old = json.load(open('crypt_v1.json'))
    WALL = {'minecraft:deepslate_bricks', 'minecraft:deepslate_tiles', 'minecraft:polished_deepslate', 'minecraft:cobbled_deepslate', 'minecraft:sculk'}
    cls = lambda st: 'wall' if st in WALL else 'slab' if (st and 'slab[type=bottom' in st and 'deepslate' in st) else st
    diff = []
    for x in range(2, 29):
        for z in range(32, 65):
            for y in range(0, 19):
                o = old.get(f'{x},{y},{z}', 'minecraft:air'); n = NB.b.get((x, y, z), 'minecraft:air')
                if cls(o) != cls(n): diff.append((x, y, z, n))
    attached = ('skull', 'sculk_vein', 'lantern', 'cobweb', 'candle', 'ladder')
    diff.sort(key=lambda d: (any(a in d[3] for a in attached), d[1]))
    cr = lambda x, y, z: '^{:g} ^{:g} ^{:g}'.format(x + 0.5 - CRYPT_CTRL[0], y + 0.5 - CRYPT_CTRL[1], z + 0.5 - CRYPT_CTRL[2])
    for n in range(4):
        fn(f'p73/crypt_{n}', [f'execute positioned {cr(x, y, z)} run setblock ~ ~ ~ {rot.rotate(st, n)} strict' for x, y, z, st in diff])
    signs_gy = [(x, y, z) for (x, y, z), nb in NB.nbt.items() if isinstance(nb, dict) and 'front_text' in nb]
    fn('p73/crypt_signs', [f'execute positioned {cr(x, y, z)} run data merge block ~ ~ ~ {{front_text:{{has_glowing_text:1b}}}}' for x, y, z in signs_gy])
    corners = ' '.join(f'if loaded {cr(x, 1, z)}' for x, z in ((3, 38), (27, 38), (3, 62), (27, 62), (26, 64)))
    second.append('execute as @e[type=minecraft:marker,tag=bm.crypt_ctrl,tag=!bm.cr62] at @s rotated as @s if entity @a[distance=..96] '
                  f'unless entity @a[distance=..26] {corners} run function bm:p73/crypt_fix')
    fn('p73/crypt_fix', ['execute unless score @s bm.state matches 0 run return 0', 'tag @s add bm.cr62', 'function bm:p73/crypt_signs'] +
       [f'execute if entity @s[y_rotation={r}] run function bm:p73/crypt_{n}' for r, n in rot.TURNS])
    G.P73_CRYPT_DIFF = len(diff)
    # the market's last two unlit signs
    import mgeo
    MB = mgeo.MB()
    dark = [c for c, nb in MB.nbt.items() if isinstance(nb, dict) and 'front_text' in nb]      # (every sign: the template's are all lit now)
    fn('p73/mkt_signs', ['tag @s add bm.p73s'] + [f'execute positioned {mgeo.rel((c[0] + 0.5, c[1] + 0.5, c[2] + 0.5))} run data merge block ~ ~ ~ {{front_text:{{has_glowing_text:1b}}}}' for c in dark])
    second.append('execute as @e[type=minecraft:marker,tag=bm.mkt,tag=!bm.p73s] at @s rotated as @s if entity @a[distance=..64] run function bm:p73/mkt_signs')

    # ================================================================== FIXES
    # one Dockmaster per market: keep the one nearest his counter, remove the rest (and their rat)
    from phase34 import DOCK_POS
    second.append('execute as @e[type=minecraft:marker,tag=bm.mkt] at @s rotated as @s if entity @a[distance=..64] run function bm:p73/dock')
    fn('p73/dock', [f'execute positioned {mgeo.rel(DOCK_POS)} run tag @e[type=minecraft:villager,tag=bm.npc_dock,distance=..80,sort=nearest,limit=1] add bm.dkkeep',
                    'execute as @e[type=minecraft:villager,tag=bm.npc_dock,tag=!bm.dkkeep,distance=..80] at @s run function bm:p73/dock_kill',
                    'execute as @e[type=minecraft:villager,tag=bm.dkkeep] at @s run function bm:p73/dock_sprite', 'tag @e[tag=bm.dkkeep] remove bm.dkkeep'])
    fn('p73/dock_kill', ['execute unless entity @e[type=minecraft:villager,tag=bm.dkkeep,distance=..1.5] run kill @e[type=minecraft:item_display,tag=bm.rat_sprite,distance=..1,sort=nearest,limit=1]',
                         'tp @s ~ -500 ~', 'kill @s'])
    fn('p73/dock_sprite', ['tag @e[type=minecraft:item_display,tag=bm.rat_sprite,distance=..1.5,sort=nearest,limit=1] add bm.dkks',
                           'kill @e[type=minecraft:item_display,tag=bm.rat_sprite,tag=!bm.dkks,distance=..1.5]', 'tag @e[tag=bm.dkks] remove bm.dkks'])
    # Pearlman's model goes with him (however he goes)
    second.append('execute as @e[type=minecraft:item_display,tag=bm.pearld] at @s unless entity @e[type=minecraft:villager,tag=bm.pearl,distance=..1] run function bm:p73/pearl_gone')
    fn('p73/pearl_gone', ['particle minecraft:snowflake ~ ~1 ~ 0.4 0.6 0.4 0.02 20', 'particle minecraft:poof ~ ~0.6 ~ 0.3 0.4 0.3 0.02 8', 'kill @s'])

    # ================================================================== FOLLOWERS GO HOME (too far, logged off, item put away; stale copies)
    for entry in FOLLOW:
        follow_rules(G, entry, second)
    # Skiff Escorts (they fly with you anywhere already): put the beacon away and it flies home too
    from phase72_art import ESCORT_COLS
    second.append('execute as @e[type=minecraft:bat,tag=bm.eskhost] at @s run function bm:p73/fol/esk')
    fn('p73/fol/esk', ['scoreboard players operation #me bm.pid = @s bm.pid', 'tag @a remove bm.fown', 'execute as @a if score @s bm.pid = #me bm.pid run tag @s add bm.fown',
                       'execute unless entity @a[tag=bm.fown] run return 0'] +
       sum(([f'execute if score @s bm.eskc matches {i} if items entity @a[tag=bm.fown,limit=1] container.* {holds("skiff_escort_" + c)} run return run scoreboard players set @s bm.fmis 0',
             f'execute if score @s bm.eskc matches {i} if items entity @a[tag=bm.fown,limit=1] weapon.offhand {holds("skiff_escort_" + c)} run return run scoreboard players set @s bm.fmis 0',
             f'execute if score @s bm.eskc matches {i} if items entity @a[tag=bm.fown,limit=1] player.cursor {holds("skiff_escort_" + c)} run return run scoreboard players set @s bm.fmis 0']
            for i, c in enumerate(ESCORT_COLS)), []) +
       ['scoreboard players add @s bm.fmis 1', 'execute if score @s bm.fmis matches 3.. as @a[tag=bm.fown,limit=1] at @s run function bm:p73/fol/esk_stash', 'tag @a remove bm.fown'])
    fn('p73/fol/esk_stash', ['function bm:p72/esk/vanish', tellraw('@s', PREFIX + [T('You put the beacon away - your Skiff Escort flies home.', 'gray')])])

    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:interaction,tag=bm.cphit]', 'kill @e[type=minecraft:block_display,tag=bm.dcseat]',
                                       'execute as @e[tag=bm.dcmob] run tp @s ~ -2000 ~', 'kill @e[tag=bm.dcmob]']
    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


def rp(R):
    R.ICONS['fixers_card'] = R.grid(['................', '................', '..YYYYYYYYYYYY..', '.YkkkkkkkkkkkkY.', '.YkYYkkkkkkkkkY.', '.YkYYkkwwwwwkkY.',
                                     '.YkkkkkkkkkkkkY.', '.YkkkwwwwwwwkkY.', '.YkkkkkkkkkkkkY.', '.YkkkwwwwkkkkkY.', '.YkkkkkkkkkrrkY.', '.YkkkkkkkkkrrkY.',
                                     '..YYYYYYYYYYYY..', '................', '................', '................'],
                                    dict(Y='#ffcf40', k='#1e1a22', w='#d8d0c0', r='#c0303a'))

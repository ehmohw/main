"""2.79b: CALLING THE BOSSES - rare raid finds that force a roaming boss out, the Arachno-Lantern's gourd on a Blood Moon
heist, a little netherite and diamond in the vault's rare stores, and KillerWatt's Effigy from his predecessor's hand.

SUMMONS (a won heist, Tier III and up, every raider: 1% at Tier III, 3% at IV, 5% at V) - one of six, each forcing out one
              of the roaming bosses whose relic has four forms: the HORSEMAN'S LANTERN (the Headless Horseman), the PHARAOH'S
              SCARAB (the Sand Pharaoh), the THUNDERHEAD FEATHER (the Storm Roc), the ELDER ACORN (the Elder Treant) - those
              four in the Overworld - the SMOULDERING IDOL (the Magma Colossus, in the Nether) and the STARLESS EYE (the
              Voidwalker, in the End). Use one (under the open sky, in the Overworld): the boss comes now, whatever the hour, the weather or the
              biome, and stays to fight (the dawn, the clear sky or the night that would send it off don't, while it was
              called - it still leaves if nobody stays near). Not while that boss is already out; not in a heist; nothing is
              used up if it can't come (no sky, nowhere to stand).
THE SMOULDERING GOURD (a won BLOOD MOON heist, Tier III and up, every raider: 5%) - set it down under the open sky in the
              Overworld: the Scorching Arachno-Lantern grows from it - dormant until you come near, then awake - on any
              night, Blood Moon or not.
THE CRIMSON WAR HORN (2.82c: the Bloodbroker, 13 Blood Crystals; a won BLOOD MOON heist, any tier, every raider: 5%) - blown
              under the open sky on a Blood Moon, the Monstrosity and its Herald come out ten blocks ahead.
THE CRIMSON EFFIGY and THE VORN FLEET BEACON (2.82c: a won heist, any tier, every raider: 5% each - the beacon only once the fleet
              has noticed the world) - the beacon calls an Invasion Night tonight; Zorp sells it once invasions are unlocked.
THE VAULT'S RARE STORES (the Tier III-V vault treasure roll, as before: 8%/9%/10% a win) now hold a few diamonds, a little
              netherite scrap and, rarely, a netherite upgrade template beside the tier's own gear - sparingly (about 1 win in
              60 for diamonds at Tier III, a template about 1 in 370).
THE STORM EFFIGY is no longer Cecil's: Democratus gives it to whoever beats him in a duel - every duel won - because
              KillerWatt is his successor.
"""
from items import item, T, TOTEM, ITEMS, DYNAMIC
from useitem import hold, HOLD
import phase72 as _P72

ROMAN = ['', 'I', 'II', 'III', 'IV', 'V']
HA, HB = '-200 64 -197', '-198 64 -197'                 # (the haul's two barrels - as phase105)
BOSS_CHANCE = {3: 3, 4: 6, 5: 10}                      # % a won heist, every raider (2.94o: was 1 / 3 / 5)
LANTERN_CHANCE = 5                                     # % a won Blood Moon heist, Tier III and up, every raider
# key: (item, name, colour, the boss's own placing (as a player, at them), its body, its tag, its dimension, who, lore)
SUMMON = {
    'hhm': ('sum_horseman', "Horseman's Lantern", '#ff8a2a', 'p42/spawn/try', 'wither_skeleton', 'bm.hhm', 'overworld', 'the Headless Horseman',
            'A pumpkin lantern that laughs when lit.'),
    'sph': ('sum_pharaoh', "Pharaoh's Scarab", '#e8b923', 'p53/sph/try', 'husk', 'bm.sph', 'overworld', 'the Sand Pharaoh',
            'A gold scarab, warm as desert sand.'),
    'roc': ('sum_roc', 'Thunderhead Feather', '#7ab8ff', 'p53/roc/try', 'phantom', 'bm.roc', 'overworld', 'the Storm Roc',
            'A feather that crackles in your fingers.'),
    'trt': ('sum_treant', 'Elder Acorn', '#6fae3a', 'p54/trt/try', 'creaking', 'bm.trt', 'overworld', 'the Elder Treant',
            'An acorn as old as the forest.'),
    'mcol': ('sum_colossus', 'Smouldering Idol', '#ff6a1a', 'p54/mcol/try', 'magma_cube', 'bm.mcol', 'the_nether', 'the Magma Colossus',
             'An obsidian idol with lava in its cracks.'),
    'vwk': ('sum_voidwalker', 'Starless Eye', '#c27dff', 'p54/vwk/try', 'enderman', 'bm.vwk', 'the_end', 'the Voidwalker',
            'An eye with no stars in it.'),
}
WHERE = {'overworld': 'the Overworld', 'the_nether': 'the Nether', 'the_end': 'the End'}
# (each boss's leave-by-the-hour (or -weather) line, waived while it was called)
LEAVE = {'p42/boss/second': 'execute unless score #tod', 'p53/sph/second': 'execute unless score #tod', 'p54/trt/second': 'execute unless score #tod',
         'p53/roc/second': 'execute if score @s bm.rfx matches 10..', 'p82/tick': 'execute unless score #active bm.bm matches 1'}
# the vault's rare stores, Tier III and up: (item, weight, count) beside the tier's gear (weight 10 each)
RARE_EXTRA = {3: [('diamond', 6, (1, 2)), ('netherite_scrap', 3, 1), ('netherite_upgrade_smithing_template', 1, 1)],
              4: [('diamond', 6, (1, 3)), ('netherite_scrap', 3, (1, 2)), ('netherite_upgrade_smithing_template', 1, 1)],
              5: [('diamond', 6, (2, 3)), ('netherite_scrap', 4, (1, 2)), ('netherite_upgrade_smithing_template', 2, 1)]}

for _k, (_iid, _nm, _col, _try, _ty, _tag, _dim, _who, _l0) in SUMMON.items():
    item(_iid, TOTEM, _nm, _col, [_l0, (f'Use under the open sky in {WHERE[_dim]}:' if _dim == 'overworld' else f'Use it in {WHERE[_dim]}:', 'blue'), (f'{_who[0].upper() + _who[1:]} comes - now,', 'blue'),
                                  ('whatever the hour or the weather.', 'blue'), ('◆ Rare raid find (Tier III and up)', '#5ab0ff')],
         model=f'bm:{_iid}', glint=True, stack=4, cat='relic', comps=hold('none'))
    HOLD[_iid] = f'bm:p148/use/{_k}'
item('sum_lantern', TOTEM, 'Smouldering Gourd', '#ff5a1a', ['A charred little gourd. Something inside it breathes.', ('Use under the open sky in the Overworld:', 'blue'),
                                                         ('the Scorching Arachno-Lantern grows', 'blue'), ('from it - Blood Moon or not.', 'blue'),
                                                         ('◆ Blood Moon heist find (Tier III and up)', '#d02020')],
     model='bm:sum_lantern', glint=True, stack=4, cat='relic', comps=hold('none'))
HOLD['sum_lantern'] = 'bm:p148/use/lantern'
# (2.82c) THE CRIMSON WAR HORN - the Bloodbroker's (13 Blood Crystals, a fixed price) and a won Blood Moon heist's (5%, every
#  raider, any tier): blown under the open sky on a Blood Moon, it calls the Monstrosity and its Herald out - now
HORN_PRICE, HORN_CHANCE = 13, 5
item('sum_monstrosity', TOTEM, 'Crimson War Horn', '#c01818', ['A ravager\'s tusk, bound in red iron. It sounds like the Blood Moon.',
                                                             ('Use under the open sky on a Blood Moon:', 'blue'), ('the Monstrosity and its Herald', 'blue'),
                                                             ('come for you - now.', 'blue'), ('◆ The Bloodbroker - or a Blood Moon heist', '#d02020')],
     model='bm:sum_monstrosity', glint=True, stack=4, cat='blood', comps=hold('none'))
HOLD['sum_monstrosity'] = 'bm:p148/use/monstrosity'
# (2.82c) THE VORN FLEET BEACON - the Crimson Effigy's twin for the Vorn: an Invasion Night tonight. Only once the fleet has
#  noticed this world (#vornmet: a Vorn killed aboard a Dreadnought) - Zorp only shows it then, and it won't work before.
#  Zorp sells it (once unlocked); a won heist of any tier gives one 5% of the time (unlocked worlds only), and the Crimson
#  Effigy 5% too.
EVENT_CHANCE = 5
item('vorn_beacon', TOTEM, 'Vorn Fleet Beacon', '#7dff6a', ['A stolen Vorn homing beacon. Switch it on and they come.',
                                                          ('Use it: an Invasion Night TONIGHT.', 'blue'), ('Every player will know you did it.', 'red'),
                                                          ('Only once the fleet has noticed this world.', 'gray')],
     model='bm:vorn_beacon', glint=True, stack=4, cat='alien', comps=hold('none'))
HOLD['vorn_beacon'] = 'bm:p148/use/beacon'
import phase24 as _R24
_R24.INV_EXTRA.append((('xenite_green', 24), ('xenite_red', 4), ('vorn_beacon', 1)))
# ---- (2.82g) the Fixer's Lamp: Goldtooth sells it; lit in the den before BEGIN, the heist's Lights Out is lifted
LAMP_PRICE = 24
item('fixers_lamp', TOTEM, "Fixer's Lamp", '#ffd27a', ['A brass lamp that never goes out.', ('Use it in the den, before BEGIN:', 'blue'),
                                                     ('the heist\'s Lights Out is lifted.', 'blue'), ('Sold by Goldtooth.', 'dark_gray')],
     model='minecraft:lantern', glint=True, stack=4, cat='misc', comps=hold('none'))
HOLD['fixers_lamp'] = 'bm:p148/use/lamp'
# (2.82i) THE PRIME COOLER - Chef Fromage's: a cold box for Prime cuts and nothing else (27 slots, the satchel's crate trick)
COOLER_PRICE = 8
PRIME_CUTS = ('prime_beef', 'prime_pork', 'prime_mutton', 'prime_chicken', 'prime_rabbit')
item('prime_cooler', TOTEM, 'Prime Cooler', '#8ad8ff',
     ['Right-click: it unfolds into a barrel (27 slots).', ('Sneak or walk away to pack it up.', 'gray'), ('Keeps Prime cuts cold: Prime Beef, Porkchop,', 'blue'), ('Mutton, Chicken and Rabbit.', 'blue'),
      'Nothing else goes in - not even plain meat.', ('Carried, it gathers Prime cuts', 'blue'), ('lying within 6 blocks.', 'blue'),
      'From Chef Fromage\'s kitchen.'],
     model='bm:prime_cooler', stack=1, cat='meat', comps=dict(hold('none'), **{'minecraft:container': []}))
DYNAMIC.add('prime_cooler')
HOLD['prime_cooler'] = 'bm:p148/use/cooler'
import phase70 as _P70
_goldtooth0 = _P70.goldtooth


def _goldtooth():
    from gen_dp import offer
    d = _goldtooth0()
    d['Offers']['Recipes'].append(offer(('gutter_coin', LAMP_PRICE), ('fixers_lamp', 1)))
    return d


_P70.goldtooth = _goldtooth
import economy as _ECON
_ECON.DIRECT['sum_monstrosity'] = (('blood_crystal', HORN_PRICE), None)      # (the price as set: no scale, no cut)
_ECON.DIRECT['prime_cooler'] = (('token', COOLER_PRICE), None)


def extend_offers(O, offer):
    O['blood'].append(offer(('blood_crystal', HORN_PRICE), ('sum_monstrosity', 1)))
    O['chef'].append(offer(('token', COOLER_PRICE), ('prime_cooler', 1)))


# (2.82n) the Crew Flare: a loaner in every kit - stuck somewhere, it takes you to a crewmate
item('crew_flare', TOTEM, 'Crew Flare', '#ff8a5a', ['A Fixer\'s flare, for when you\'re cut off.', ('Use: you\'re taken to a crewmate.', 'blue'),
                                                    ('Sneak + use (or alone): to the hall', 'blue'), ('before the room ahead.', 'blue'),
                                                    ('Only while a heist is under way; every 20 s.', 'gray'), ('Loaned with every kit.', 'gray')],
     model='minecraft:recovery_compass', stack=1, cat='magic',
     comps=dict(hold('none'), **{'minecraft:use_cooldown': {'seconds': 20.0, 'cooldown_group': 'bm:crew_flare'}}))
HOLD['crew_flare'] = 'bm:p148/flare'


def generate(G):
    fn, wjson, tellraw, PREFIX = G.fn, G.wjson, G.tellraw, G.PREFIX
    P = PREFIX
    say = lambda txt, col='gray': G.title('@s', 'actionbar', T(txt, col))
    holds = lambda iid: f'*[minecraft:custom_data~{{bm:"{iid}"}}]'
    near = 'gamemode=!creative,gamemode=!spectator'

    # ================================================================== THE SUMMONS (as the player who uses one, where they stand)
    for k, (iid, nm, col, try_, ty, tag, dim, who, _l0) in SUMMON.items():
        Who = who[0].upper() + who[1:]
        assert try_ in G.FUNCS, try_
        boss = f'@e[type=minecraft:{ty},tag={tag}'
        fn(f'p148/use/{k}', [
            'execute if dimension bm:gutter run return run ' + say(f'{Who} won\'t come into a heist - use it out in the world.'),
            f'execute unless dimension minecraft:{dim} run return run ' + say(f'{Who} only answers in {WHERE[dim]}.', col),
            f'execute if entity {boss}] run return run ' + say(f'{Who} is already abroad.', col),
            *([f'execute positioned ~ ~1.6 ~ unless predicate bm:sees_sky run return run ' + say('It needs the open sky over you.')]
              if dim == 'overworld' else []),                        # (the Nether and the End: the boss finds its own ground round you)
            f'tag {boss}] add bm.c148old',
            f'function bm:{try_}',
            f'execute unless entity {boss},tag=!bm.c148old] run return run ' + say('Nothing came - find open ground around you, and try again.'),
            f'tag {boss},tag=!bm.c148old] add bm.called',
            f'tag {boss}] remove bm.c148old',
            f'execute unless entity @s[gamemode=creative] run clear @s {holds(iid)} 1',
            tellraw(f'@a[distance=..96]', P + [{'selector': '@s', 'color': 'white'}, T(' called out ', 'gray'), T(Who, col, bold=True), T('!', 'gray')]),
            'playsound minecraft:event.raid.horn hostile @a[distance=..96] ~ ~ ~ 1.5 0.8'])
    # (called: the hour, the weather or the moon doesn't send it home - only being left alone does)
    for f_, head in LEAVE.items():
        L = G.FUNCS[f_]
        k_ = [i for i, l in enumerate(L) if l.startswith(head) and ('retreat' in l or 'leave' in l)]
        assert len(k_) == 1, (f_, k_)
        L[k_[0]] = L[k_[0]].replace('execute ', 'execute unless entity @s[tag=bm.called] ', 1)

    # ---- the gourd: the Arachno-Lantern grows from it (dormant till you come near - its own waking)
    lan = '@e[type=minecraft:giant,tag=bm.salboss'
    fn('p148/use/lantern', [
        'execute if dimension bm:gutter run return run ' + say('It won\'t grow in a heist - use it out in the world.'),
        'execute unless dimension minecraft:overworld run return run ' + say('It only grows in the Overworld.', '#ff5a1a'),
        f'execute if entity {lan}] run return run ' + say('The Arachno-Lantern is already abroad.', '#ff5a1a'),
        'execute positioned ~ ~1.6 ~ unless predicate bm:sees_sky run return run ' + say('It needs the open sky over you.'),
        'execute rotated ~ 0 positioned ^ ^ ^14 positioned over motion_blocking_no_leaves run function bm:p82/summon',
        f'execute unless entity {lan}] run return run ' + say('Nothing grew - find open ground ahead of you, and try again.'),
        f'tag {lan}] add bm.called',
        f'execute unless entity @s[gamemode=creative] run clear @s {holds("sum_lantern")} 1',
        tellraw('@a[distance=..96]', P + [{'selector': '@s', 'color': 'white'}, T(' planted a ', 'gray'), T('Smouldering Gourd', '#ff5a1a', bold=True),
                                          T('... something enormous is growing.', 'gray')])])
    # (its dormant self also leaves on its own clock if nobody's near - that stays)

    # ---- the war horn: the Monstrosity and its Herald, ten blocks ahead - on a Blood Moon only (it retreats at dawn, as ever)
    mon = '@e[type=minecraft:ravager,tag=bm.monstrosity'
    room = ' '.join(f'if block {p} #minecraft:air' for p in ('~ ~1 ~', '~ ~3 ~', '~2 ~3 ~', '~-2 ~3 ~', '~ ~3 ~2', '~ ~3 ~-2'))
    fn('p148/use/monstrosity', [
        'execute if dimension bm:gutter run return run ' + say('Nothing answers a horn in a heist - blow it out in the world.'),
        'execute unless dimension minecraft:overworld run return run ' + say('Only the Overworld\'s Blood Moon hears it.', '#c01818'),
        'execute unless score #active bm.bm matches 1 run return run ' + say('The horn is silent - wait for a Blood Moon.', '#c01818'),
        f'execute if entity {mon}] run return run ' + say('The Monstrosity is already abroad.', '#c01818'),
        'execute positioned ~ ~1.6 ~ unless predicate bm:sees_sky run return run ' + say('It needs the open sky over you.'),
        f'execute rotated ~ 0 positioned ^ ^ ^10 positioned over motion_blocking_no_leaves {room} run function bm:monst/summon',
        f'execute unless entity {mon}] run return run ' + say('Nothing came - find open ground ahead of you, and try again.'),
        f'execute unless entity @s[gamemode=creative] run clear @s {holds("sum_monstrosity")} 1',
        'playsound minecraft:event.raid.horn hostile @a[distance=..128] ~ ~ ~ 3 0.6', 'playsound minecraft:entity.ravager.roar hostile @a[distance=..96] ~ ~ ~ 2 0.7',
        tellraw('@a[distance=..128]', P + [{'selector': '@s', 'color': 'white'}, T(' blew the ', 'gray'), T('Crimson War Horn', '#c01818', bold=True),
                                           T(' - the Monstrosity answers!', 'gray')])])

    # ---- the fleet beacon: an Invasion Night tonight (as the admin's invasion_now), once the fleet has noticed this world
    VG = '#7dff6a'
    inst = 'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run '
    LP = '#ffd27a'
    fn('p148/use/lamp', [
        'execute unless dimension bm:gutter run return run ' + say('Light it in the Fixer\'s den, before BEGIN - it lifts a heist\'s Lights Out.', LP),
        'execute unless entity @s[tag=bm.gvp] run return run ' + say('Light it in the Fixer\'s den, before BEGIN - it lifts a heist\'s Lights Out.', LP),
        'scoreboard players operation #gi bm.rng = @s bm.gvi', 'scoreboard players set #ls bm.rng -1', 'scoreboard players set #lo bm.rng 0',
        inst + 'scoreboard players operation #ls bm.rng = @s bm.gvst',
        inst + 'scoreboard players operation #lo bm.rng = @s bm.gvmod', 'scoreboard players operation #lo bm.rng %= #2 bm.rng',
        'execute if score #ls bm.rng matches 2.. run return run ' + say('Too late - the job\'s already on. Light it before BEGIN next time.', LP),
        'execute unless score #ls bm.rng matches 1 run return run ' + say('Light it in the Fixer\'s den, before BEGIN - it lifts a heist\'s Lights Out.', LP),
        'execute unless score #lo bm.rng matches 1 run return run ' + say('No Lights Out on this job - keep your lamp for one that has it.', LP),
        inst + 'scoreboard players remove @s bm.gvmod 1', inst + 'function bm:p70/bar',
        f'execute unless entity @s[gamemode=creative] run clear @s {holds("fixers_lamp")} 1',
        'tag @s add bm.lamplit',
        'execute as @a[tag=bm.gvp] if score @s bm.gvi = #gi bm.rng run ' + tellraw('@s', P + [{'selector': '@a[tag=bm.lamplit]', 'color': LP}, T(' lit a Fixer\'s Lamp. ', 'gray'), T('No Lights Out on this job.', LP, bold=True)]),
        'tag @s remove bm.lamplit',
        'execute as @a[tag=bm.gvp] if score @s bm.gvi = #gi bm.rng at @s run playsound minecraft:block.beacon.activate player @s ~ ~ ~ 0.7 1.6'])
    fn('p148/use/beacon', [
        'execute if dimension bm:gutter run return run ' + say('No signal down here - switch it on out in the world.'),
        'execute unless score #vornmet bm.bm matches 1 run return run ' + say('Dead air. The fleet hasn\'t noticed this world - kill a Vorn aboard a Dreadnought first.', VG),
        'execute if score #inv bm.bm matches 1 run return run ' + say('The Vorn are already here.', VG),
        'execute if score #bday bm.bm matches 1 run return run ' + say('Not on a Blood Moon day - the Vorn won\'t come near it.', VG),
        'execute if score #ivn bm.bm matches 1 if score #iday bm.bm = #day bm.bm run return run ' + say('The Vorn are already coming tonight.', VG),
        'scoreboard players set #ivn bm.bm 1', 'scoreboard players operation #iday bm.bm = #day bm.bm',
        'execute if score #tod bm.bm matches 23000.. run scoreboard players set #iforce bm.bm 1',
        f'execute unless entity @s[gamemode=creative] run clear @s {holds("vorn_beacon")} 1',
        tellraw('@a', P + [{'selector': '@s', 'color': VG}, T(' switched on a Vorn Fleet Beacon. ', 'gray'), T('The Vorn are coming tonight!', VG, bold=True)]),
        'execute as @a at @s run playsound minecraft:block.beacon.power_select ambient @s ~ ~ ~ 0.8 0.5'])

    # ---- Zorp: the beacon on his stock once the fleet has noticed the world (not on a Lucky Night - his discount list then)
    sec = G.FUNCS['loop/second']
    za = [i for i, l in enumerate(sec) if 'as @e[tag=bm.npc_alien] unless score @s bm.ofv matches ' in l and 'function bm:p17/npc/alien' in l]
    assert len(za) == 1, za
    sec[za[0]] = sec[za[0]].replace('execute ', 'execute unless score #vornmet bm.bm matches 1 ', 1)
    sec.insert(za[0] + 1, f'execute if score #vornmet bm.bm matches 1 unless score #lnight bm.bm matches 1 as @e[tag=bm.npc_alien] '
                          f'unless score @s bm.ofv matches {_R24.INV_VER} run function bm:p148/zorp_unlocked')

    # ---- (2.82m) another job: the whole kit comes out of the Armory again - the secondary (wind charges, potions, arrows),
    #      the ranged kit's arrows, the support's potions, the golden apples, food and paperweights, each at its rank's count.
    #      (2.68 / 2.82f topped up only the paperweights, food and apples; a spent secondary stayed spent.) The wind charges the
    #      Fixer held at a room's door belong to the old job - they're not handed back on top.
    G.FUNCS['p104/resupply'] = ['execute in bm:gutter as @e[type=minecraft:item] if items entity @s contents *[minecraft:custom_data~{bm_kit:1b}] run kill @s',
                                'clear @s *[minecraft:custom_data~{bm_kit:1b}]', 'function bm:p72/kit/strip', 'scoreboard players set @s bm.gvhw 0'] + \
                               [f'execute if score @s bm.gvrole matches {r} run function bm:p72/kit/give_{r}' for r in range(1, 5)]

    # ---- (2.82m) the Arcane Study's ambush bars its door behind whoever walked in first; a crewmate who was still behind
    #      (or comes back from a knock-out) was shut out until both waves fell. Now anyone of the crew at the bars while
    #      they're down is pulled through to the fight. (Local x -3..0 at the door, z 10..14; into x 2.5, z 12.5.)
    # (2.82n) every room: anyone of the crew at a barred entrance (the ambush's, or a solved room's) is let through
    G.FUNCS['loop/fast'].append('execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr] at @s if block ~-12 ~ ~ minecraft:iron_bars positioned ~-15.5 ~ ~-2.5 '
                                'if entity @a[tag=bm.gvp,dx=2.5,dy=4,dz=4] positioned ~15.5 ~ ~2.5 run function bm:p148/amb_pull')
    fn('p148/amb_pull', ['execute positioned ~-15.5 ~ ~-2.5 run tag @a[tag=bm.gvp,dx=2.5,dy=4,dz=4] add bm.ambp', 'tp @a[tag=bm.ambp] ~-10 ~ ~ -90 0',
                         'execute as @a[tag=bm.ambp] at @s run playsound minecraft:block.iron_door.open player @s ~ ~ ~ 1 0.8',
                         G.title('@a[tag=bm.ambp]', 'actionbar', T('The bars let you through - your crew is ahead!', '#c060ff')), 'tag @a remove bm.ambp'])


    # ---- (2.82n) no backtracking: a solved room's entrance is barred as its exit opens (only open air is barred)
    G.FUNCS['p70/solved'].insert(2, 'fill ~-12 ~ ~-1 ~-12 ~3 ~1 minecraft:iron_bars replace minecraft:air')
    # ---- (2.82n) a won heist: the vault's entrance is barred, and anyone of the crew outside the vault (not in the den, the
    #      Lounge or the Locker Hall) is put back in the treasury - no wandering the old rooms behind the choice dialog
    G.FUNCS['p70/payout_inst'] += ['scoreboard players operation #vi bm.rng = @s bm.gvi',
                                   'execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_vault] if score @s bm.gvi = #vi bm.rng at @s run fill ~-12 ~ ~-1 ~-12 ~3 ~1 minecraft:iron_bars replace minecraft:air']
    G.FUNCS['loop/second'].append('execute as @e[type=minecraft:marker,tag=bm.gvinst,scores={bm.gvst=4}] at @s run function bm:p148/vlock')
    fn('p148/vlock', ['scoreboard players operation #vi bm.rng = @s bm.gvi',
                      'execute as @a[tag=bm.gvp] if score @s bm.gvi = #vi bm.rng at @s if dimension bm:gutter unless function bm:p121/inside unless function bm:p84/lk/inside run tag @s add bm.vout',
                      'execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_vault] if score @s bm.gvi = #vi bm.rng at @s positioned ~-12.5 ~-2 ~-12.5 run tag @a[tag=bm.vout,dx=37,dy=20,dz=25] remove bm.vout',
                      'execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby] if score @s bm.gvi = #vi bm.rng at @s positioned ~-12.5 ~-2 ~-12.5 run tag @a[tag=bm.vout,dx=25,dy=20,dz=25] remove bm.vout',
                      'execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_vault] if score @s bm.gvi = #vi bm.rng at @s run tp @a[tag=bm.vout] ~18 ~ ~ -90 0',
                      'execute as @a[tag=bm.vout] run ' + say('The job\'s done - the Fixer keeps you in the vault. Your Ledger has the choice.', '#ffcf40'),
                      'tag @a remove bm.vout'])
    # ---- (2.82n) the Crew Flare: with every kit (a loaner - it goes with the kit), to a crewmate on the same heist
    G.FUNCS['p80/kit/extras'].append(f'give @s {_P72.kit_arg("crew_flare")} 1')
    fn('p148/flare', ['execute unless entity @s[tag=bm.gvp] run return run ' + say('The flare only burns on a heist.', 'gray'),
                      'scoreboard players operation #fi bm.rng = @s bm.gvi', 'scoreboard players set #st bm.rng 0',
                      'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #fi bm.rng store result score #st bm.rng run scoreboard players get @s bm.gvst',
                      'execute unless score #st bm.rng matches 2..3 run return run ' + say('The flare only burns while a heist is under way.', 'gray'),
                      'tag @s add bm.flme',
                      'execute as @a[tag=bm.gvp,tag=!bm.flme] if score @s bm.gvi = #fi bm.rng at @s if dimension bm:gutter unless function bm:p121/inside unless function bm:p84/lk/inside run tag @s add bm.flto',
                      'execute if predicate bm:p20/sneaking run tag @a remove bm.flto',
                      'particle minecraft:flame ~ ~1 ~ 0.3 0.6 0.3 0.05 30',
                      'execute if entity @a[tag=bm.flto] run tp @s @a[tag=bm.flto,sort=random,limit=1]',
                      'execute if entity @a[tag=bm.flto] run ' + say('The flare takes you to your crew.', '#ff8a5a'),
                      'execute unless entity @a[tag=bm.flto] in bm:gutter as @e[type=minecraft:marker,tag=bm.gvcp] if score @s bm.gvi = #fi bm.rng run tp @a[tag=bm.flme] @s',
                      'execute unless entity @a[tag=bm.flto] run ' + say('The flare takes you to the hall before the room ahead.', '#ff8a5a'),
                      'execute at @s run playsound minecraft:entity.firework_rocket.launch player @a[distance=..16] ~ ~ ~ 1 1.2',
                      'execute at @s run particle minecraft:flame ~ ~1 ~ 0.3 0.6 0.3 0.05 30',
                      'tag @a remove bm.flto', 'tag @s remove bm.flme'])
    # ---- (2.82n) the Locker Hall's adventure mode, four times a second (and again once they're through the door)
    G.FUNCS['loop/fast'].append('execute in bm:gutter positioned -256 60 -256 as @a[dx=15,dy=12,dz=15,gamemode=survival] run function bm:p84/lk/adv')
    G.FUNCS['p84/lk/enter'].append('execute if entity @s[gamemode=survival] run function bm:p84/lk/adv')


    # ---- (2.82o) the Grapple room: a hook lent only when you truly have none (the cursor and the crafting grid count), at most
    #      every 3 s, and a dropped hook is gone (no pile of them); the swinging lamps (B) can be hooked anywhere on their
    #      swing - the chains included - and the hook hangs you under the lamp over its island
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.gvhl dummy']
    G.OBJECTIVES.append('bm.gvhl')
    rh = '*[minecraft:custom_data~{bm_rhook:1b}]'
    me = G.FUNCS['p115/grapple/me']
    k = next(i for i, l in enumerate(me) if 'function bm:p115/grapple/lend' in l)
    me[k] = me[k].replace('run function bm:p115/grapple/lend', f'unless items entity @s player.cursor {rh} unless items entity @s player.crafting.* {rh} unless score @s bm.gvhl matches 1.. run function bm:p115/grapple/lend')
    G.FUNCS['p115/grapple/lend'].append('scoreboard players set @s bm.gvhl 60')
    G.FUNCS['tick'].append('scoreboard players remove @a[scores={bm.gvhl=1..}] bm.gvhl 1')
    G.FUNCS['loop/second'].append(f'execute in bm:gutter as @e[type=minecraft:item] if items entity @s contents {rh} run kill @s')
    ray = G.FUNCS['p21/grap/ray']
    assert 'unless block ~ ~ ~ minecraft:target run return run scoreboard players set #ghit bm.rng 3' in ray[0], ray[0]
    ray[0] = ray[0].replace('unless block ~ ~ ~ minecraft:target run', 'unless block ~ ~ ~ minecraft:target unless block ~ ~ ~ minecraft:iron_chain run')
    ray.insert(1, 'execute if score @s bm.gvhk matches 1.. if block ~ ~ ~ minecraft:iron_chain unless entity @e[type=minecraft:marker,tag=bm.gvswing,distance=..5] run return run scoreboard players set #ghit bm.rng 3')
    hit = G.FUNCS['p21/grap/hit']
    hit.insert(1, 'execute if score @s bm.gvhk matches 1.. if entity @e[type=minecraft:marker,tag=bm.gvswing,distance=..5] at @e[type=minecraft:marker,tag=bm.gvswing,distance=..5,sort=nearest,limit=1] positioned ~ ~-0.5 ~ run return run function bm:p115/hook/snap')


    # ---- (2.82o) heists and the den's trips (Lounge, Locker Hall) start from inside dungeons, the Hollow and the Black Market too
    bad = ('if dimension bm:hollow_throne', 'if predicate bm:p103/boss_dungeon', 'if entity @s[tag=bm.adv]')
    hit = 0
    for f_, L in G.FUNCS.items():
        if f_ in ('p104/unsafe',) or (f_.startswith(('p103/lh/', 'p121/')) and f_.endswith('try')):
            n0 = len(L); L[:] = [l for l in L if not any(b in l for b in bad)]; hit += n0 - len(L)
    assert hit >= 6, hit
    for f_ in [f for f in G.FUNCS if f.endswith('/no_dun')]:
        if not any(f'bm:{f_}' in l for L in G.FUNCS.values() for l in L): del G.FUNCS[f_]


    # ---- (2.82p) a room's lent items (the hook, batons, puzzle tools...) never leave the heist: taken on every way out, and
    #      swept off anyone outside one (as the kit is)
    G.FUNCS['p70/unraid'][0:0] = ['clear @s *[minecraft:custom_data~{bm_room:1b}]']
    G.FUNCS['loop/second'].append('clear @a[tag=!bm.gvp,tag=!bm.gvdead] *[minecraft:custom_data~{bm_room:1b}]')


    # ---- (2.82q) THE FEE MULTIPLIER: winning a Tier III / IV / V heist has a 5 / 10 / 15% chance of paying the raider's fee back
    #      doubled, tripled or quadrupled (2x 45%, 3x 40%, 4x 15%); Tier I and II: 5%, mostly doubled (2x 85%, 3x 10%, 4x 5%) - the extra on top of the fee the win already returns
    import phase90 as _P90
    title = G.title
    G.FUNCS['p70/haul'].append('function bm:p148/feex')
    fn('p148/feex', ['scoreboard players set #fmul bm.rng 1', 'execute unless score #gt bm.rng matches 1..5 run return 0', 'execute store result score #r bm.rng run random value 1..100',
                     'execute if score #gt bm.rng matches ..2 if score #r bm.rng matches 6.. run return 0',
                     'execute if score #gt bm.rng matches 3 if score #r bm.rng matches 6.. run return 0',
                     'execute if score #gt bm.rng matches 4 if score #r bm.rng matches 11.. run return 0',
                     'execute if score #gt bm.rng matches 5 if score #r bm.rng matches 16.. run return 0',
                     'execute store result score #r bm.rng run random value 1..100',
                     'scoreboard players set #fm bm.rng 2', 'execute if score #r bm.rng matches 46..85 run scoreboard players set #fm bm.rng 3',
                     'execute if score #r bm.rng matches 86.. run scoreboard players set #fm bm.rng 4',
                     'execute if score #gt bm.rng matches ..2 run scoreboard players set #fm bm.rng 2',
                     'execute if score #gt bm.rng matches ..2 if score #r bm.rng matches 86..95 run scoreboard players set #fm bm.rng 3',
                     'execute if score #gt bm.rng matches ..2 if score #r bm.rng matches 96.. run scoreboard players set #fm bm.rng 4'] +
       [f'execute if score #gt bm.rng matches {t} run scoreboard players set #c bm.rng {_P90.FEE_T[t]}' for t in (1, 2, 3, 4, 5)] +
       ['scoreboard players operation #fx bm.rng = #fm bm.rng', 'scoreboard players remove #fx bm.rng 1', 'scoreboard players operation #c bm.rng *= #fx bm.rng',
        'scoreboard players operation #fxc bm.rng = #c bm.rng', 'scoreboard players operation #fmul bm.rng = #fm bm.rng', 'function bm:p80/hand {iid:"token"}',
        'function bm:p148/feex_coins',
        'title @s times 5 50 15', title('@s', 'title', [{'score': {'name': '#fm', 'objective': 'bm.rng'}, 'color': '#7dff6a', 'bold': True}, T('x YOUR FEE!', '#7dff6a', bold=True)]),
        title('@s', 'subtitle', [T('The Fixer pays out big: +', 'gray'), {'score': {'name': '#fxc', 'objective': 'bm.rng'}, 'color': 'white', 'bold': True}, T(' Tokens - and your haul too', 'gray')]),
        'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1.2', 'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1 0.8'])


    # (2.82r) the multiplier pays on the win's gutter coins too: as many again (2x), twice as many (3x), three times (4x)
    def _haul_count(iid):
        q = f'*[minecraft:custom_data~{{bm:"{iid}"}}]'
        return [x for b in ('-200 64 -197', '-198 64 -197') for n in range(27) for x in (
            f'execute in bm:gutter if items block {b} container.{n} {q} store result score #s bm.rng run data get block {b} Items[{{Slot:{n}b}}].count',
            f'execute in bm:gutter if items block {b} container.{n} {q} run scoreboard players operation #co bm.rng += #s bm.rng')]
    # (2.82r/s) the multiplier pays on what's in the win's Haul too - gutter coins, BM Medallions and Trophies: as many again (2x),
    #  twice as many (3x), three times (4x)
    fn('p148/feex_coins', ['function bm:p148/feex_n/gutter_coin', 'function bm:p148/feex_n/medallion', 'function bm:p148/feex_n/trophy'])
    for iid in ('gutter_coin', 'medallion', 'trophy'):
        fn(f'p148/feex_n/{iid}', ['scoreboard players set #co bm.rng 0'] + _haul_count(iid) +
           ['scoreboard players operation #co bm.rng *= #fx bm.rng', f'execute if score #co bm.rng matches 1.. run function bm:p148/give1/{iid}'])
        fn(f'p148/give1/{iid}', [f'loot give @s loot bm:items/{iid}', 'scoreboard players remove #co bm.rng 1',
                                 f'execute if score #co bm.rng matches 1.. run function bm:p148/give1/{iid}'])
    # (2.82r) every won heist: a chance at a Gutter Medallion and a rarer one at a Gutter Trophy, both rising with the tier
    MED, TRO = {1: 10, 2: 15, 3: 20, 4: 25, 5: 30}, {1: 1, 2: 2, 3: 4, 4: 6, 5: 8}
    G.FUNCS['p70/haul'].append('function bm:p148/gutx')
    fn('p148/gutx', ['execute store result score #r bm.rng run random value 1..100'] +
       [f'execute if score #gt bm.rng matches {t} if score #r bm.rng matches ..{p} run function bm:p148/gutx_m' for t, p in MED.items()] +
       ['execute store result score #r bm.rng run random value 1..100'] +
       [f'execute if score #gt bm.rng matches {t} if score #r bm.rng matches ..{p} run function bm:p148/gutx_t' for t, p in TRO.items()])
    fn('p148/gutx_m', ['loot give @s loot bm:items/gutter_medallion', 'execute if score #fmul bm.rng matches 2.. run loot give @s loot bm:items/gutter_medallion', 'execute if score #fmul bm.rng matches 3.. run loot give @s loot bm:items/gutter_medallion', 'execute if score #fmul bm.rng matches 4.. run loot give @s loot bm:items/gutter_medallion', 'playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 1 0.8',
                       tellraw('@s', [T('[Heist] ', '#ffcf40', bold=True), T('The Fixer slips you a ', 'gray'), T('Gutter Medallion', '#e0a040', bold=True), T(' for a job well done', 'gray'), T(' (x', 'gray'), {'score': {'name': '#fmul', 'objective': 'bm.rng'}, 'color': 'white'}, T(').', 'gray')])])
    fn('p148/gutx_t', ['loot give @s loot bm:items/gutter_trophy', 'execute if score #fmul bm.rng matches 2.. run loot give @s loot bm:items/gutter_trophy', 'execute if score #fmul bm.rng matches 3.. run loot give @s loot bm:items/gutter_trophy', 'execute if score #fmul bm.rng matches 4.. run loot give @s loot bm:items/gutter_trophy', 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1',
                       tellraw('@s', [T('[Heist] ', '#ffcf40', bold=True), T('A ', 'gray'), T('Gutter Trophy', '#ffd870', bold=True), T(' from the vault - the Fixer lets you keep it', 'gray'), T(' (x', 'gray'), {'score': {'name': '#fmul', 'objective': 'bm.rng'}, 'color': 'white'}, T(').', 'gray')])])

    # ---- (2.82g) a failed heist: the crew is walked back to the den within a second, and stays there (the den and the Locker
    #      Hall) until the choice is made - backing out of the dialog no longer lets anyone walk on into the dead heist
    fl = G.FUNCS['p75/fail']
    nfl = 0
    for i, l in enumerate(fl):
        if l.endswith(' bm.gvfail 4'): fl[i] = l[:-1] + '1'; nfl += 1
    assert nfl == _P70.SLOTS, nfl
    lo = G.FUNCS['p120/lights_out']
    safe = [l for l in lo if l.endswith('add bm.gvsafe')]
    assert len(safe) == 2, safe
    fence = [f'execute if score @s bm.gvi matches {s + 1} unless score #fl{s} bm.gvfail matches 0 run return 0' for s in range(_P70.SLOTS)]
    fence += ['function bm:p70/tag_mine'] + safe
    for s_ in range(_P70.SLOTS):
        tp = [l for l in G.FUNCS[f'p75/s{s_}/reset'] if ' in bm:gutter run tp @s ' in l]
        assert len(tp) == 1, (s_, tp)
        spot = tp[0].split(' run tp @s ')[1].split()[:3]
        fence.append(f'execute if score @s bm.gvi matches {s_ + 1} in bm:gutter positioned {" ".join(spot)} run tag @a[tag=bm.gvme,distance=..18] add bm.gvsafe')
        fence.append(f'execute if score @s bm.gvi matches {s_ + 1} as @a[tag=bm.gvme,tag=!bm.gvsafe] run function bm:p148/failback{s_}')
        fn(f'p148/failback{s_}', ['execute in bm:gutter run tp @s ' + tp[0].split(' run tp @s ')[1],
                                  say('The job\'s off - the Fixer walks you back. Your Ledger has the choice: a new raid, or home.', 'red')])
    fence += ['tag @a[tag=bm.gvsafe] remove bm.gvsafe', 'tag @a[tag=bm.gvme] remove bm.gvme']
    fn('p148/failfence', fence)
    G.FUNCS['p70/inst_sec'].append('execute if score @s bm.gvst matches 5 run function bm:p148/failfence')

    # ---- (2.82h) the heist's Nether: a monster standing on (or beside) a magma floor - Hot Floor's rooms, the Blaze Forge - is
    #      fireproofed for good, so the floor doesn't burn the crew's foes down for them; and every heist piglin is grown (a baby
    #      piglin isn't hostile)
    G.FUNCS['loop/second'] += ['execute in bm:gutter as @e[tag=bm.gvg,tag=!bm.gvfr] at @s if function bm:p148/hot run function bm:p148/fireproof',
                               'execute in bm:gutter as @e[tag=bm.gvboss,tag=!bm.gvfr] at @s if function bm:p148/hot run function bm:p148/fireproof',
                               'execute in bm:gutter as @e[type=minecraft:piglin,tag=bm.gvg,tag=!bm.gvad] run function bm:p148/grown']
    fn('p148/hot', [f'execute if block ~{dx} ~-1 ~{dz} minecraft:magma_block run return 1' for dx in (0, -1, 1) for dz in (0, -1, 1)] + ['return 0'])
    fn('p148/fireproof', ['effect give @s minecraft:fire_resistance infinite 0 true', 'tag @s add bm.gvfr'])
    fn('p148/grown', ['data modify entity @s IsBaby set value 0b', 'tag @s add bm.gvad'])

    # ---- (2.82k) the traders' hands stay empty: a wandering-trader NPC host that ever got a moment of AI (Zorp, aboard a mothership)
    #      can be left holding its milk bucket or potion - and a held item shows even on an invisible host, in front of the model
    G.FUNCS['loop/second'] += ['execute as @e[type=minecraft:wandering_trader,tag=bm.npc] if items entity @s weapon.mainhand * run item replace entity @s weapon.mainhand with minecraft:air',
                               'execute as @e[type=minecraft:wandering_trader,tag=bm.npc] if items entity @s weapon.offhand * run item replace entity @s weapon.offhand with minecraft:air']

    # ---- (2.82k) adventure mode aboard the motherships and the Vorn Dreadnoughts (as in the market and the crypts). The hull is
    #      ~25 blocks round its beam marker (bm.tbeam / bm.tbeam_red, on the lower deck), from 5 below it to 14 above. Its own
    #      tag (bm.advs), so the zone/exit sweep for the market and crypts doesn't undo it. The conduits, crystals, chests and
    #      crew all work in adventure mode.
    for t in ('bm.tbeam', 'bm.tbeam_red'):
        G.FUNCS['loop/second'].append(f'execute as @e[type=minecraft:marker,tag={t}] at @s positioned ~-25 ~-5 ~-25 as @a[dx=50,dy=19,dz=50,gamemode=survival,tag=!bm.advs] run function bm:p148/ship/enter')
    G.FUNCS['loop/second'].append('execute as @a[tag=bm.advs] at @s unless function bm:p148/ship/aboard run function bm:p148/ship/leave')
    fn('p148/ship/enter', ['gamemode adventure @s', 'tag @s add bm.advs', say('Aboard the ship: blocks cannot be broken or placed here.', 'dark_aqua')])
    fn('p148/ship/aboard', [f'execute positioned ~-25 ~-14 ~-25 if entity @e[type=minecraft:marker,tag={t},dx=50,dy=19,dz=50] run return 1' for t in ('bm.tbeam', 'bm.tbeam_red')] + ['return 0'])
    fn('p148/ship/leave', ['tag @s remove bm.advs', 'execute if entity @s[gamemode=adventure,tag=!bm.adv] run gamemode survival @s'])

    # ---- (2.82l) a pop-up container broken by hand drops no block: the Prime Cooler's / shulker box's barrel (bm.bxm), the Vacuum
    #      Satchel's barrel (bm.vacm) and the Ender Pouch's ender chest (bm.pouch) were free barrels / ender chests (or eight
    #      obsidian) for the breaking. Checked every tick, before the drop's pick-up delay runs out; whatever was inside stays on
    #      the ground for its owner, and the marker's own check then packs the item up (empty) or folds the pouch away.
    G.FUNCS['tick'] += ['execute as @e[type=minecraft:marker,tag=bm.bxm] at @s unless block ~ ~ ~ minecraft:barrel run function bm:p148/broke/box',
                        'execute as @e[type=minecraft:marker,tag=bm.vacm] at @s unless block ~ ~ ~ minecraft:barrel run function bm:p148/broke/vac',
                        'execute as @e[type=minecraft:marker,tag=bm.pouch] at @s unless block ~ ~ ~ minecraft:ender_chest run function bm:p148/broke/pouch']
    nobarrel = 'execute as @e[type=minecraft:item,distance=..2] if items entity @s contents minecraft:barrel run kill @s'
    fn('p148/broke/box', [nobarrel, 'function bm:p33/box/close'])                       # (its owner gets the item back, empty)
    fn('p148/broke/vac', [nobarrel, 'kill @s'])                                          # (the satchel's storage went into the barrel)
    fn('p148/broke/pouch', ['execute as @e[type=minecraft:item,distance=..2] if items entity @s contents minecraft:ender_chest run kill @s',
                            'execute as @e[type=minecraft:item,distance=..2] if items entity @s contents minecraft:obsidian run kill @s',
                            'kill @s'])

    # ---- (2.82i) THE PRIME COOLER: right-click sets it down as a barrel (phase33's boxes, as the satchel: the item is held in
    #      storage while it's open, its contents moved into the barrel, and back when it's packed up). Only Prime cuts stay in:
    #      anything else put in is handed straight back out at the owner's feet - while it's open, and once more as it closes.
    cool_hand = ['scoreboard players set #hand bm.rng 0',
                 f'execute if items entity @s weapon.mainhand {holds("prime_cooler")} run scoreboard players set #hand bm.rng 1',
                 f'execute if score #hand bm.rng matches 0 if items entity @s weapon.offhand {holds("prime_cooler")} run scoreboard players set #hand bm.rng 2',
                 'execute if score #hand bm.rng matches 0 run return 0']
    fn('p148/use/cooler', cool_hand + ['execute if score #hand bm.rng matches 1 run return run function bm:p33/box/open {path:"SelectedItem",slot:"weapon.mainhand",name:"Prime Cooler",kind:"cool"}',
                                       'function bm:p33/box/open {path:"equipment.offhand",slot:"weapon.offhand",name:"Prime Cooler",kind:"cool"}'])
    keep = ''.join(f' unless items block ~ ~ ~ container.%d {holds(c)}' for c in PRIME_CUTS)
    fn('p148/cool/bad', [f'execute if items block ~ ~ ~ container.{n} *{keep % ((n,) * len(PRIME_CUTS))} run return 1' for n in range(27)] + ['return 0'])
    fn('p148/cool/purge', [f'execute if items block ~ ~ ~ container.{n} *{keep % ((n,) * len(PRIME_CUTS))} run function bm:p148/cool/spit {{n:{n}}}' for n in range(27)])
    fn('p148/cool/spit', ['$data modify storage bm:tmp cool set from block ~ ~ ~ Items[{Slot:$(n)b}]', 'data remove storage bm:tmp cool.Slot',
                          '$item replace block ~ ~ ~ container.$(n) with minecraft:air',
                          'execute at @a[tag=bm.cown,limit=1] run summon minecraft:item ~ ~0.3 ~ {Tags:["bm.cspit"],Item:{id:"minecraft:stone",count:1},PickupDelay:0s}',
                          'data modify entity @e[type=minecraft:item,tag=bm.cspit,limit=1] Item set from storage bm:tmp cool',
                          'tag @e[type=minecraft:item,tag=bm.cspit] remove bm.cspit'])
    G.FUNCS['loop/fast'] += ['execute as @e[type=minecraft:marker,tag=bm.bx_cool] at @s if block ~ ~ ~ minecraft:barrel if function bm:p148/cool/bad run function bm:p148/cool/live']
    fn('p148/cool/live', ['tag @a remove bm.cown', 'scoreboard players operation #own bm.pid = @s bm.pid',
                          'execute as @a if score @s bm.pid = #own bm.pid run tag @s add bm.cown',
                          'execute unless entity @a[tag=bm.cown] run return 0', 'function bm:p148/cool/purge',
                          'execute as @a[tag=bm.cown] at @s run playsound minecraft:block.chest.close player @s ~ ~ ~ 0.5 1.6',
                          G.title('@a[tag=bm.cown]', 'actionbar', T('Only Prime cuts go in the cooler.', '#8ad8ff')), 'tag @a remove bm.cown'])
    # (2.82j) it gathers Prime cuts lying within 6 blocks into itself while it's anywhere in its owner's inventory (the Vacuum
    # Satchel's pick-up, p33/vac/take: matching stacks merge, then the first free slot; what doesn't fit stays on the ground)
    cool = holds('prime_cooler')
    G.FUNCS['loop/fast'] += [f'execute as @a[gamemode=!spectator] if items entity @s container.* {cool} at @s if entity @e[type=minecraft:item,distance=..6,nbt={{PickupDelay:0s}}] run function bm:p148/cool/pull']
    fn('p148/cool/pull', ['scoreboard players set #vs bm.rng -1'] +
       [f'execute if score #vs bm.rng matches -1 if items entity @s container.{n} {cool} run scoreboard players set #vs bm.rng {n}' for n in range(36)] +
       ['execute if score #vs bm.rng matches -1 run return 0',
        'execute store result storage bm:tmp cpk.n int 1 run scoreboard players get #vs bm.rng',
        'function bm:p148/cool/read with storage bm:tmp cpk', 'scoreboard players set #vtak bm.rng 0',
        'execute as @e[type=minecraft:item,distance=..6,nbt={PickupDelay:0s},limit=16,sort=nearest] if function bm:p148/cool/prime at @s run function bm:p33/vac/take',
        'execute if score #vtak bm.rng matches 1.. run function bm:p148/cool/write with storage bm:tmp cpk'])
    fn('p148/cool/prime', [f'execute if items entity @s contents {holds(c)} run return 1' for c in PRIME_CUTS] + ['return 0'])
    fn('p148/cool/read', ['data remove storage bm:tmp vac.c', '$data modify storage bm:tmp vac.c set from entity @s Inventory[{Slot:$(n)b}].components."minecraft:container"',
                          'execute unless data storage bm:tmp vac.c run data modify storage bm:tmp vac.c set value []',
                          'data modify storage bm:tmp cpk.c set from storage bm:tmp vac.c'])
    fn('p148/cool/write', ['data modify storage bm:tmp cpk.c set from storage bm:tmp vac.c',
                           'function bm:p148/cool/write_m with storage bm:tmp cpk', 'playsound minecraft:entity.item.pickup player @s ~ ~ ~ 0.4 0.6'])
    fn('p148/cool/write_m', ['$item modify entity @s container.$(n) {type:"minecraft:set_components",components:{"minecraft:container":$(c)}}'])
    bc = G.FUNCS['p33/box/close']
    k = next(i for i, l in enumerate(bc) if l.startswith('execute if block ~ ~ ~ minecraft:barrel run data modify storage bm:tmp bx.src'))
    bc.insert(k, 'execute if entity @s[tag=bm.bx_cool] if block ~ ~ ~ minecraft:barrel run function bm:p148/cool/purge')

    # ================================================================== THE FINDS (in a won heist's haul)
    ins = lambda table: [f'execute in bm:gutter unless data block {HA} Items[26] run loot insert {HA} loot {table}',
                         f'execute in bm:gutter if data block {HA} Items[26] run loot insert {HB} loot {table}']
    for k, (iid, *_r) in SUMMON.items():
        wjson(f'bm/loot_table/p148/{k}.json', {'type': 'minecraft:chest', 'pools': [{'rolls': 1, 'entries': [G.loot_entry(iid)]}]})
    wjson('bm/loot_table/p148/lantern.json', {'type': 'minecraft:chest', 'pools': [{'rolls': 1, 'entries': [G.loot_entry('sum_lantern')]}]})
    G.FUNCS['p105/finds'] += ['execute store result score #r bm.rng run random value 1..100'] + \
        [f'execute if score #gt bm.rng matches {t} if score #r bm.rng matches ..{c} run function bm:p148/find/boss' for t, c in BOSS_CHANCE.items()] + \
        ['execute store result score #r bm.rng run random value 1..100',
         f'execute if score #gn bm.rng matches 1 if score #gt bm.rng matches 3.. if score #r bm.rng matches ..{LANTERN_CHANCE} run function bm:p148/find/lantern',
         'execute store result score #r bm.rng run random value 1..100',
         f'execute if score #gn bm.rng matches 1 if score #r bm.rng matches ..{HORN_CHANCE} run function bm:p148/find/horn',
         # (2.82c: any tier, every raider - the Crimson Effigy, and the Vorn Fleet Beacon once invasions are unlocked)
         'execute store result score #r bm.rng run random value 1..100',
         f'execute if score #r bm.rng matches ..{EVENT_CHANCE} run function bm:p148/find/effigy',
         'execute store result score #r bm.rng run random value 1..100',
         f'execute if score #vornmet bm.bm matches 1 if score #r bm.rng matches ..{EVENT_CHANCE} run function bm:p148/find/beacon']
    keys = list(SUMMON)
    # (its own roll, #sb: the caller's #r stays as it was)
    fn('p148/find/boss', [f'execute store result score #sb bm.rng run random value 1..{len(keys)}'] +
       [f'execute if score #sb bm.rng matches {i} run function bm:p148/find/{k}' for i, k in enumerate(keys, 1)])
    for k, (iid, nm, col, _t, _ty, _tag, _d, who, _l0) in SUMMON.items():
        fn(f'p148/find/{k}', ins(f'bm:p148/{k}') + [
            tellraw('@a', P + [{'selector': '@s', 'color': 'white'}, T(' found a ', 'gray'), T(nm, col, bold=True), T(f' in a won heist - it calls {who}!', 'gray')]),
            'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 0.9'])
    wjson('bm/loot_table/p148/horn.json', {'type': 'minecraft:chest', 'pools': [{'rolls': 1, 'entries': [G.loot_entry('sum_monstrosity')]}]})
    fn('p148/find/horn', ins('bm:p148/horn') + [
        tellraw('@a', P + [{'selector': '@s', 'color': 'white'}, T(' found a ', 'gray'), T('Crimson War Horn', '#c01818', bold=True),
                           T(' in a Blood Moon haul - it calls the Monstrosity!', 'gray')]),
        'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 0.6'])
    for k, iid, nm, col, what in (('effigy', 'crimson_effigy', 'Crimson Effigy', '#c01818', 'it calls a Blood Moon!'),
                                  ('beacon', 'vorn_beacon', 'Vorn Fleet Beacon', '#7dff6a', 'it calls the Vorn!')):
        fn(f'p148/find/{k}', ins(f'bm:items/{iid}') + [
            tellraw('@a', P + [{'selector': '@s', 'color': 'white'}, T(' found a ', 'gray'), T(nm, col, bold=True), T(f' in a won heist - {what}', 'gray')]),
            'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 0.8'])
    fn('p148/find/lantern', ins('bm:p148/lantern') + [
        tellraw('@a', P + [{'selector': '@s', 'color': 'white'}, T(' found a ', 'gray'), T('Smouldering Gourd', '#ff5a1a', bold=True),
                           T(' in a Blood Moon haul - the Arachno-Lantern sleeps in it!', 'gray')]),
        'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 0.7'])

    # ---- the vault's rare stores (Tier III and up): a little diamond and netherite beside the tier's own gear
    import phase105 as P105
    def ent(i, w, c):
        if i in ITEMS:
            return dict(G.loot_entry(i), weight=w)
        e = {'type': 'minecraft:item', 'name': f'minecraft:{i}', 'weight': w}
        if c != 1:
            e['functions'] = [{'function': 'minecraft:set_count', 'count': G.uni(*c) if isinstance(c, tuple) else c}]
        return e
    for t, extra in RARE_EXTRA.items():
        wjson(f'bm/loot_table/p105/rare_t{t}.json', {'pools': [{'rolls': 1, 'entries': [ent(i, 10, 1) for i in P105.RARE_POOL[t]] +
                                                                                  [ent(i, w, c) for i, w, c in extra]}]})
        fg = G.FUNCS[f'p105/find_gear{t}']
        fg[:] = [l.replace(f'A piece of Tier {ROMAN[t]}\'s own gear.', 'From the vault\'s own rare stores.') for l in fg]

    # ================================================================== KILLERWATT'S EFFIGY: from Democratus, every duel won (his successor)
    import phase97 as P97
    dchat = lambda txt: tellraw('@s', [T('Democratus: ', P97.STORM, bold=True), T(f'"{txt}"', P97.STORM_LT)])
    pz = G.FUNCS['p97/duel/prize']
    k_ = next(i for i, l in enumerate(pz) if l.startswith('execute if score @s bm.dmsc matches 1.. run return run'))
    pz[k_:k_] = ['loot spawn ~ ~0.4 ~ loot bm:items/kw_effigy',
                 dchat('And this. A storm needs an heir - KillerWatt will carry it when I am gone. Raise the Effigy in thunder, and he comes.'),
                 tellraw('@s', P + [T('A Storm Effigy! ', '#ffe040', bold=True), T('Use it outdoors in a thunderstorm: KillerWatt comes down.', 'gray')])]

    fn('admin/summons', [G.give(v[0]) for v in SUMMON.values()] + [G.give('sum_lantern')])


def rp(R):
    g = R.grid
    def art(rows, pal):
        rows = [(r + '.' * 16)[:16] for r in rows] + ['.' * 16] * (16 - len(rows))
        return g(rows, pal)
    R.ICONS['sum_horseman'] = art(['................', '.....hhhhhh.....', '....h......h....', '....h..ss..h....', '.....kkkkkk.....',
                                   '...kkoooooOkk...', '..kooOooooOOok..', '..koyykooyykok..', '..kooyooooyook..', '..koooooooooOk..',
                                   '..kokyyyyyykok..', '..kookyykyykok..', '...kooooooook...', '....kkkkkkkk....'],
                                  dict(k='#3a1a04', o='#e07a10', O='#ffb04a', y='#ffe060', s='#4a6a20', h='#8a8a8a'))
    R.ICONS['sum_pharaoh'] = art(['................', '.......kk.......', '......kGGk......', '.....kgGGgk.....', '..k..kggggk..k..',
                                  '...kkbBBBBbkk...', '....kbBbbBbk....', '..kkbbBbbBbbkk..', '....kbbbbbbk....', '..kkkbbbbbbkkk..',
                                  '....kbbbbbbk....', '.....kbbbbk.....', '......kkkk......'],
                                 dict(k='#3a2604', g='#c8961c', G='#ffe07a', b='#1a4aa8', B='#5a9aff'))
    R.ICONS['sum_roc'] = art(['................', '............kk..', '...........kwlk.', '..........kwllk.', '.........kwlbk..',
                              '........kwlybk..', '.......kwyybk...', '......kwlybk....', '.....kwlbbk.....', '....kwlbbk......',
                              '...kwlbk........', '...kwbk.........', '..kkk...........', '.kk.............', 'k...............'],
                             dict(k='#1a2a3a', w='#f4f8ff', l='#a8c8f0', b='#5a7aa8', y='#ffe040'))
    R.ICONS['sum_treant'] = art(['................', '.......k........', '......kl........', '.....kllk.......', '....kkkkkkk.....',
                                 '...kcCcCcCck....', '..kcCcCcCcCck...', '..kccccccccck...', '...knNNNNnnk....', '...knNNNnnnk....',
                                 '...knNNnnnnk....', '....knnnnnk.....', '.....knnnk......', '......kkk.......'],
                                dict(k='#2a1a08', l='#5aa83a', c='#6a4a22', C='#8a6a3a', n='#b8863a', N='#e0b060'))
    R.ICONS['sum_colossus'] = art(['................', '......kkkk......', '.....koooolk....', '.....kolyook....', '.....koooook....',
                                   '......kllkk.....', '....kkoooookk...', '...koloyooolok..', '...kooolooook...', '....kooloook....',
                                   '....koooyook....', '....kooolook....', '...kkoooooookk..', '...kllllllllk...', '...kkkkkkkkkk...'],
                                  dict(k='#0a0410', o='#2a1a3a', l='#ff6a1a', y='#ffd040'))
    R.ICONS['sum_voidwalker'] = art(['................', '................', '.....kkkkkk.....', '...kkppppppkk...', '..kpPPppppPPpk..',
                                     '.kpPppkkkkppPpk.', '.kpPpkvvvvkpPpk.', 'kpPpkvvwvvvkpPpk', 'kpPpkvvvvvvkpPpk', '.kpPpkvvvvkpPpk.',
                                     '.kpPppkkkkppPpk.', '..kpPPppppPPpk..', '...kkppppppkk...', '.....kkkkkk.....'],
                                    dict(k='#10041a', p='#7a3ac0', P='#c27dff', v='#06020a', w='#ffffff'))
    R.ICONS['sum_monstrosity'] = art(['................', '.y..............', '.yk.............', '..kbk...........', '...kbbk.........', '....kbbrk.......',
                                      '.....kbbrbk.....', '......kbbrbbk...', '.......kbbrbbk..', '........kbbrbbk.', '.........kbbbbk.', '..........kkkk..'],
                                     dict(k='#3a0606', b='#d8c8a0', r='#a01010', y='#ffd040'))      # (2.82c: sprites280e repaints it)
    R.ICONS['vorn_beacon'] = art(['................', '.......gg.......', '......gGGg......', '.......kk.......', '.....kkkkkk.....', '....kvvvvvvk....',
                                  '....kvGggGvk....', '....kvgGGgvk....', '....kvGggGvk....', '....kvvvvvvk....', '....kkkkkkkk....', '...kvvvvvvvvk...',
                                  '...kkkkkkkkkk...'], dict(k='#1a1e24', v='#5a6474', g='#3ac84a', G='#b4ff9a'))
    R.ICONS['prime_cooler'] = art(['................', '................', '.....kkkkkk.....', '.....k....k.....', '..kkkkkkkkkkkk..',
                                   '..kwwwwwwwwwwk..', '..kWWWWWWWWWWk..', '..kkkkkkkkkkkk..', '..kbBBBBBBBBbk..', '..kbBfBBBBBBbk..',
                                   '..kbBBrrrrBBbk..', '..kbBrRRRrwwbk..', '..kbBBrrrrBBbk..', '..kbbbbbbbbbbk..', '..kkkkkkkkkkkk..'],
                                  dict(k='#14303e', w='#f4fbff', W='#c8e4f0', b='#2a7aa8', B='#5ab4e0', f='#e0f8ff', r='#c83a3a', R='#ff8a7a'))
    R.ICONS['sum_lantern'] = art(['................', '.......ss.......', '......ss........', '....kkkkkkkk....', '...kddddddddk...',
                                  '..kddoddddoddk..', '..kdyodddoydk...', '..kddddddddddk..', '..kdoyyyyyyodk..', '..kddoyoyyoddk..',
                                  '...kddddddddk...', '..k.kkkkkkkk.k..', '.k..k..k..k..k..', 'k...k..k..k...k.'],
                                 dict(k='#1a0604', d='#3a1a0a', o='#ff6a1a', y='#ffd040', s='#2a3a10'))

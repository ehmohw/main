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
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD

ROMAN = ['', 'I', 'II', 'III', 'IV', 'V']
HA, HB = '-200 64 -197', '-198 64 -197'                 # (the haul's two barrels - as phase105)
BOSS_CHANCE = {3: 1, 4: 3, 5: 5}                       # % a won heist, every raider
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


def extend_offers(O, offer):
    O['blood'].append(offer(('blood_crystal', HORN_PRICE), ('sum_monstrosity', 1)))


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

    # ---- (2.82f) another job: the kit's golden apples topped back up with the paperweights and food (eaten on the last heist,
    #      they never came back) - each kit rank's own count, from its own give list
    gap = 'minecraft:golden_apple[minecraft:custom_data={bm_kit:1b}'
    for r in range(1, 5):
        lines = {k: [l for l in G.FUNCS[f'p80/kit/give_{r}_{k}'] if l.startswith(f'give @s {gap}')] for k in range(1, 7)}
        assert all(len(v) == 1 for v in lines.values()), (r, {k: len(v) for k, v in lines.items()})
        fn(f'p148/gap/r{r}', [f'execute if score @s bm.kr{r} matches {k} run return run {lines[k][0]}' for k in range(2, 7)] + [lines[1][0]])
    G.FUNCS['p104/resupply'] += ['clear @s minecraft:golden_apple[minecraft:custom_data~{bm_kit:1b}]'] + \
                                [f'execute if score @s bm.gvrole matches {r} run function bm:p148/gap/r{r}' for r in range(1, 5)]

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
    R.ICONS['sum_lantern'] = art(['................', '.......ss.......', '......ss........', '....kkkkkkkk....', '...kddddddddk...',
                                  '..kddoddddoddk..', '..kdyodddoydk...', '..kddddddddddk..', '..kdoyyyyyyodk..', '..kddoyoyyoddk..',
                                  '...kddddddddk...', '..k.kkkkkkkk.k..', '.k..k..k..k..k..', 'k...k..k..k...k.'],
                                 dict(k='#1a0604', d='#3a1a0a', o='#ff6a1a', y='#ffd040', s='#2a3a10'))

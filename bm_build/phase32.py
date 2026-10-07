"""Phase 1.20 / 2.13: the Visitors, part 3 - the Vorn.

LORE: there are two fleets in the sky. The DONADIANS (Zorp's people) are collectors and traders; their motherships are
friendly. The VORN are a hive that bioengineers whatever it finds. On an INVASION NIGHT the Vorn come down.

- CRASH SITES are carved into the real ground the first time a player comes near (the worldgen piece is only a marker),
  so the crater follows hills and never floats, and there is no square patch of flattened terrain. Zorp no longer
  waits at crash sites (existing ones pack up); a wrecked supply chest holds a Mothership Chart.
- MOTHERSHIPS are about three times rarer, and their stores hold loot barrels (shards and supplies, never Zorp's goods).
  Zorp is their quartermaster. He no longer sells what the Xenite Altar makes (ray gun, tractor beam, cloaking device,
  dowser, gravity boots); he sells new tech instead (the Overcharged Beacon, the Dimension Shifter, jump boots...).
- THE DONADIANS look like Donado now (his build, in teal), without the green disc. The disc became the Vorn hoverboard.
- INVASION NIGHTS: about 1 night in 30 that is neither a Blood Moon nor a Lucky Night (or /function bm:admin/invasion_now).
  Vorn Troopers ride hoverboards and fire plasma, Scout Saucers (UFOs) swoop and shoot, and bioengineered monsters glow an
  eerie green: oversized slimes, phantoms that dive out of the open sky whether or not anyone has slept, and a third of
  ordinary night spawns. Everything drops Xenite shards of every colour. At midnight a Vorn boss lands: the WARLORD or the
  ABDUCTOR. They drop Power Cells; Zorp trades Power Cells for the OVERCHARGED BEACON, which summons the SUPERCHARGED
  OVERSEER (invasion nights only) - and only the Overseer carries the GRAVITIC CORE: hover-flight in survival.
- THE VORN DREADNOUGHT: an incredibly rare hostile mothership with red crystals, Vorn guards, the QUAKE MAUL (right-click:
  a ground-shaking shockwave) and the Vorn Saucer Crown (cosmetic).
- RED XENITE: socket it into gear at the altar to grow (another red shard flips it to shrink) while the item is held or
  worn. Infuse a crossbow (Growth Ray) or a bow (Shrink Ray) with 8 red shards: permanent on mobs (never the Ender
  Dragon), 30 seconds on players."""
import math
import random
from nbt import snbt, B, F, Int, D
from items import item, consumable, attr, T, TOTEM, ITEM_VERSION, ITEMS, book, hat
from useitem import hold, HOLD
import phase24 as R24
import phase25 as R25

RED = '#ff4a4a'
GREEN = '#7dff6a'
ident = [F(0), F(0), F(0), F(1)]
INV_CHANCE = 3          # % of eligible nights
HUSK_SEAT, PHANTOM_SEAT = 2.075, (0.3375, 0.0506)     # measured on the 26.3 server: where a passenger rides


def seat_phantom(size): return round(PHANTOM_SEAT[0] + PHANTOM_SEAT[1] * size, 4)


# ===================================================================== items
R24.COLORS['red'] = (RED, 'Red Xenite', 'mass')
item('xenite_red', TOTEM, 'Red Xenite Shard', RED,
     ['Vorn crystal - it hums with mass.', ('Grown only aboard a Vorn Dreadnought;', 'gray'), ('the invaders carry a few.', 'gray'),
      ('Altar: socket it to change your size,', 'dark_gray'), ('or infuse a bow / crossbow (8 shards).', 'dark_gray')],
     model='bm:xenite_red', stack=64, cat='alien', glint=False)
item('growth_ray', 'minecraft:carrot_on_a_stick', 'Growth Ray', RED,
     ['Right-click: a beam that makes things bigger.', ('Permanent on creatures (never the Ender Dragon);', 'blue'),
      ('30 seconds on players.', 'blue'), ('4 shots per Red Xenite shard (from your bag).', 'gray')], model='bm:growth_ray', stack=1, cat='alien')
item('shrink_ray', 'minecraft:carrot_on_a_stick', 'Shrink Ray', '#ff8a8a',
     ['Right-click: a beam that makes things smaller.', ('Permanent on creatures (never the Ender Dragon);', 'blue'),
      ('30 seconds on players.', 'blue'), ('4 shots per Red Xenite shard (from your bag).', 'gray')], model='bm:shrink_ray', stack=1, cat='alien')
item('plasma_blaster', 'minecraft:carrot_on_a_stick', 'Vorn Plasma Blaster', GREEN,
     ['Taken from a Vorn Trooper.', ('Right-click: a plasma bolt, 9 damage,', 'blue'), ('fires twice as fast as a Ray Gun.', 'blue'),
      ('6 shots per Cyan Xenite shard (from your bag).', 'gray')], model='bm:plasma_blaster', stack=1, cat='alien')
item('power_cell', TOTEM, 'Vorn Power Cell', '#b6ff3c',
     ['The heart of a Vorn war machine.', ('Carried by Vorn bosses.', 'gray'), ('Zorp wants these. Badly.', 'dark_gray')],
     model='bm:power_cell', stack=16, cat='alien', glint=True)
item('overcharged_beacon', TOTEM, 'Overcharged Beacon', '#b6ff3c',
     ['A Vorn distress beacon, wired wrong on purpose.', ('Right-click under an open sky on an', 'blue'), ('INVASION NIGHT to summon the', 'blue'),
      ('Supercharged Overseer.', 'blue'), ('Used up when it answers.', 'gray')],
     model='bm:overcharged_beacon', stack=1, cat='alien', glint=True, bold=True, comps=hold('spyglass'))
HOLD['overcharged_beacon'] = 'bm:p32/beacon/use'
item('gravitic_core', TOTEM, 'Gravitic Core', '#e0fcff',
     ['The Overseer\'s anti-gravity heart.', ('Keep it anywhere in your inventory:', 'blue'),
      ('in mid-air, press jump again to hover-fly.', 'blue'), ('Hold jump to rise, sneak to sink;', 'blue'),
      ('touching the ground ends the flight.', 'blue'), ('No fall damage while you carry it.', 'gray')],
     model='bm:gravitic_core', stack=1, cat='alien', glint=True, bold=True)
item('xeno_visor', TOTEM, 'Xeno Visor', '#9bff8a',
     ['Vorn targeting optics.', ('Wear it: Night Vision, and every', 'blue'), ('monster within 24 blocks glows.', 'blue')],
     model='bm:xeno_visor', stack=1, cat='alien',
     comps={'minecraft:equippable': {'slot': 'head', 'swappable': True, 'equip_sound': 'minecraft:item.armor.equip_iron'},
            'minecraft:attribute_modifiers': [attr('armor', 3, 'head', ident='minecraft:armor.helmet')]})
item('quake_maul', 'minecraft:mace', 'Vorn Quake Maul', RED,
     ['The Dreadnought\'s war hammer.', ('Right-click: a shockwave - 10 damage to every', 'blue'),
      ('creature within 7 blocks, and they are thrown up.', 'blue'), ('4 second recharge.', 'gray')],
     model='bm:quake_maul', stack=1, cat='alien', bold=True,
     comps=hold('spear', {'minecraft:enchantments': {'minecraft:density': Int(5), 'minecraft:breach': Int(3), 'minecraft:unbreaking': Int(5)},
                          'minecraft:unbreakable': {}}))
HOLD['quake_maul'] = 'bm:p32/quake/use'
hat('vorn_crown', 'Vorn Saucer Crown', RED, 'bm:vorn_crown', 'minecraft:dust{color:[1.0,0.2,0.15],scale:0.9} ~ ~2.5 ~ 0.25 0.05 0.25 0 2', None,
    ['Taken from the bridge of a Dreadnought.', ('A tiny saucer circles your head.', 'gray')])
item('sealed_map_dread', TOTEM, 'Sealed Vorn Star-Chart', RED,
     ['Hold right-click to break the seal.', 'Marks the nearest Vorn Dreadnought.', ('If you are brave. Or foolish.', 'gray')],
     model='minecraft:map', glint=True, stack=16,
     comps={'minecraft:consumable': consumable(0.8, 'none', 'minecraft:item.book.page_turn', False)}, cat='map')
book('book_two_fleets', 'The Two Fleets', 'Prof. Whiskerton', [
    "THE TWO FLEETS\nby Prof. Whiskerton\n\nThere are two kinds of visitor in our sky, and confusing them may be the last mistake you make.",
    "The DONADIANS are collectors. Zorp is one. They look a great deal like a certain Earth-dog (they admire him) and they want only shinies, "
    "stories and, occasionally, a cow. Their motherships are friendly. Mostly.",
    "The VORN are something else: a hive that rebuilds whatever it touches. On certain nights they come down. Their saucers swoop, their "
    "troopers ride glowing boards, and every beast they have touched glows a sick green.",
    "Kill them and they shed crystal: green, violet, cyan... and rarely red, which only grows aboard their Dreadnoughts. "
    "Zorp pays well for their Power Cells. I would not ask what he does with them.",
    "One last note. A Vorn ship that glows RED is not a trading post. Do not board one unless you are ready to fight your way off it."])

# Zorp: no altar-craftable goods any more (the altar makes them); new tech instead. Rebuilt at import, before phase24
# builds his offer list (and its checksum), so only he re-syncs.
_ALTAR_MADE = {'ray_gun', 'tractor_beam', 'cloaking_device', 'xenite_dowser', 'gravity_boots', 'sealed_map_mothership'}
R24.OFFERS[:] = [o for o in R24.OFFERS if o[2][0] not in _ALTAR_MADE]
_k = next(i for i, o in enumerate(R24.OFFERS) if o[2][0] == 'xenite_violet')
R24.OFFERS[_k:_k] = [(('power_cell', 4), ('xenite_red', 16), ('overcharged_beacon', 1)),
                     (('xenite_green', 16), ('xenite_cyan', 8), ('sealed_map_dread', 1)),
                     (('xenite_red', 2), None, ('token', 3))]
R25.CREW_SAYS[:] = ["Earth-dog look-alike, reporting.", "Do not touch the reactor.", "Welcome aboard, collector.", "Glorp.",
                    "Your species smells of cheese.", "We are not the Vorn. Please stop asking.", "The red ships? We do not speak of them.",
                    "Zorp is in the mess hall. He wants Power Cells."]

TROOPER_SAYS = ['FOR THE HIVE', 'SPECIMEN LOCATED', 'COMPLY', 'YOU WILL BE IMPROVED']
DREAD_COLORS = {'red'}


# ===================================================================== generation
def generate(G):
    fn, wjson, title, tellraw, give, loot_entry, uni, KILLED, chance = (G.fn, G.wjson, G.title, G.tellraw, G.give, G.loot_entry, G.uni,
                                                                         G.KILLED, G.chance)
    PREFIX = G.PREFIX
    tick, fast, second, load = [], [], [], []
    objs = ['bm.xat', 'bm.xat2', 'bm.xlf', 'bm.qcd', 'bm.rred', 'bm.rsc', 'bm.rayt', 'bm.rays', 'bm.gcj', 'bm.gcair', 'bm.gcfly',
            'bm.pbcd', 'bm.pbammo', 'bm.becd']
    load += [f'scoreboard objectives add {o} dummy' for o in objs]
    load += ['team add bm.bio', 'team modify bm.bio color green', 'team modify bm.bio friendlyFire false',
             'team add bm.vornred', 'team modify bm.vornred color red',
             'bossbar add bm:invasion {"text":"Invasion Night","color":"green","bold":true}', 'bossbar set bm:invasion color green',
             'bossbar set bm:invasion max 10000', 'bossbar set bm:invasion style notched_10', 'bossbar set bm:invasion visible false']
    for b, nm in (('warlord', 'The Vorn Warlord'), ('abductor', 'The Abductor'), ('overseer', 'The Supercharged Overseer')):
        load += [f'bossbar add bm:{b} {snbt(T(nm, RED if b != "abductor" else GREEN, bold=True))}', f'bossbar set bm:{b} color {"green" if b == "abductor" else "red"}',
                 f'bossbar set bm:{b} style notched_10', f'bossbar set bm:{b} visible false']
    G.OBJECTIVES += objs
    wjson('bm/damage_type/plasma.json', {'exhaustion': 0.1, 'message_id': 'bm.plasma', 'scaling': 'when_caused_by_living_non_player'})
    wjson('bm/damage_type/quake.json', {'exhaustion': 0.1, 'message_id': 'bm.quake', 'scaling': 'never'})
    wjson('bm/predicate/p32/c30.json', {'condition': 'minecraft:random_chance', 'chance': 0.3})
    wjson('bm/predicate/p32/c50.json', {'condition': 'minecraft:random_chance', 'chance': 0.5})
    wjson('bm/predicate/p32/c15.json', {'condition': 'minecraft:random_chance', 'chance': 0.15})
    wjson('bm/tags/entity_type/p32_nobeam.json', {'values': ['#bm:ray_ignore', 'minecraft:ender_dragon']})
    shard = lambda c: f'*[minecraft:custom_data~{{bm:"xenite_{c}"}}]'
    mob_ok = 'type=!#bm:ray_ignore,tag=!bm.npc,tag=!bm.frogpet,tag=!bm.wilfrey,tag=!bm.donado,tag=!bm.wil_body,tag=!bm.merc,tag=!bm.cecilpet'

    # ------------------------------------------------------------------ loot tables (shards from Vorn and bio mobs)
    def shard_pool(n_lo, n_hi, p=1.0, colors=('green', 'violet', 'cyan')):
        p_ = {'rolls': 1, 'entries': [loot_entry(f'xenite_{c}', uni(n_lo, n_hi)) for c in colors], 'conditions': [KILLED]}
        if p < 1: p_['conditions'] = [KILLED, chance(p)]
        return p_
    def single(iid, n=1, p=1.0):
        c = [KILLED] + ([chance(p)] if p < 1 else [])
        return {'rolls': 1, 'entries': [loot_entry(iid, n if isinstance(n, dict) else None)], 'conditions': c}
    wjson('bm/loot_table/p32/trooper.json', {'type': 'minecraft:entity', 'pools': [shard_pool(1, 2), shard_pool(1, 1, 0.35), single('token', p=0.15),
                                                                                    single('plasma_blaster', p=0.04), single('xenite_red', p=0.03)]})
    wjson('bm/loot_table/p32/saucer.json', {'type': 'minecraft:entity', 'pools': [shard_pool(2, 4), shard_pool(1, 2), single('xenite_red', p=0.12),
                                                                                   single('power_cell', p=0.03), single('token', uni(1, 2), 0.3)]})
    wjson('bm/loot_table/p32/bigslime.json', {'type': 'minecraft:entity', 'pools': [
        {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:slime_ball', 'functions': [{'function': 'minecraft:set_count', 'count': uni(2, 5)}]}]},
        shard_pool(2, 3, colors=('green',)), shard_pool(1, 2, 0.5)]})
    wjson('bm/loot_table/p32/bphantom.json', {'type': 'minecraft:entity', 'pools': [
        {'rolls': 1, 'entries': [{'type': 'minecraft:loot_table', 'value': 'minecraft:entities/phantom'}]}, shard_pool(1, 3, colors=('violet',)), shard_pool(1, 2, 0.4)]})
    boss_pools = lambda cells, red: [single('power_cell', uni(*cells)), shard_pool(8, 14, colors=('green',)), shard_pool(8, 14, colors=('violet',)),
                                    shard_pool(8, 14, colors=('cyan',)), single('xenite_red', uni(*red)), single('medallion', uni(2, 4)), single('token', uni(6, 12))]
    wjson('bm/loot_table/p32/warlord.json', {'type': 'minecraft:entity', 'pools': boss_pools((1, 2), (2, 4)) + [single('xeno_visor', p=0.3), single('plasma_blaster', p=0.35)]})
    wjson('bm/loot_table/p32/abductor.json', {'type': 'minecraft:entity', 'pools': boss_pools((1, 2), (3, 5)) + [single('xeno_visor', p=0.35), single('plasma_blaster', p=0.25)]})
    wjson('bm/loot_table/p32/overseer.json', {'type': 'minecraft:entity', 'pools': [single('gravitic_core'), single('trophy', uni(1, 2)),
                                                                                     single('power_cell', uni(1, 3)), single('xenite_red', uni(6, 10))] + boss_pools((0, 0), (0, 0))[1:4]})
    # bioengineered versions of ordinary monsters: their vanilla drops + a shard
    bio_types = list(G.ARMORED) + list(G.UNARMORED)
    for t in bio_types:
        wjson(f'bm/loot_table/p32/bio/{t}.json', {'type': 'minecraft:entity', 'pools': [
            {'rolls': 1, 'entries': [{'type': 'minecraft:loot_table', 'value': f'minecraft:entities/{t}'}]}, shard_pool(1, 2, 0.75)]})
    # mothership stores: shards and supplies (never Zorp's goods), and the Dreadnought armoury
    item_e = lambda name, lo=1, hi=1, w=1: {'type': 'minecraft:item', 'name': f'minecraft:{name}', 'weight': w,
                                            'functions': [{'function': 'minecraft:set_count', 'count': uni(lo, hi)}]}
    wjson('bm/loot_table/p32/mothership_stores.json', {'type': 'minecraft:chest', 'pools': [
        {'rolls': uni(2, 3), 'entries': [dict(loot_entry(f'xenite_{c}', uni(2, 6)), weight=3) for c in ('green', 'violet', 'cyan')]},
        {'rolls': uni(2, 4), 'entries': [item_e('iron_ingot', 3, 8, 4), item_e('gold_ingot', 2, 6, 3), item_e('diamond', 1, 3, 2), item_e('ender_pearl', 2, 6, 3),
                                         item_e('glow_ink_sac', 2, 5, 3), item_e('experience_bottle', 4, 10, 3), item_e('golden_carrot', 4, 10, 3),
                                         item_e('amethyst_shard', 4, 12, 3), item_e('echo_shard', 1, 2, 1), item_e('beef', 2, 5, 2)]},
        {'rolls': 1, 'entries': [loot_entry('book_two_fleets')], 'conditions': [chance(0.25)]},
        {'rolls': 1, 'entries': [loot_entry('xenite_red')], 'conditions': [chance(0.08)]}]})
    wjson('bm/loot_table/p32/crash_wreck.json', {'type': 'minecraft:chest', 'pools': [
        {'rolls': 1, 'entries': [loot_entry('sealed_map_mothership')]},
        {'rolls': uni(1, 2), 'entries': [dict(loot_entry(f'xenite_{c}', uni(1, 3)), weight=1) for c in ('green', 'violet', 'cyan')]},
        {'rolls': uni(1, 3), 'entries': [item_e('iron_ingot', 2, 5, 3), item_e('copper_ingot', 3, 9, 3), item_e('redstone', 4, 12, 2), item_e('glow_ink_sac', 1, 3, 2)]}]})
    wjson('bm/loot_table/p32/dread_armory.json', {'type': 'minecraft:chest', 'pools': [
        {'rolls': 1, 'entries': [loot_entry('quake_maul')]}, {'rolls': 1, 'entries': [loot_entry('vorn_crown')]},
        {'rolls': 1, 'entries': [loot_entry('xenite_red', uni(6, 12))]}, {'rolls': 1, 'entries': [loot_entry('power_cell', uni(1, 2))]},
        {'rolls': 1, 'entries': [loot_entry('trophy')]}]})
    wjson('bm/loot_table/p32/dread_stores.json', {'type': 'minecraft:chest', 'pools': [
        {'rolls': uni(2, 3), 'entries': [dict(loot_entry(f'xenite_{c}', uni(3, 7)), weight=3) for c in ('green', 'violet', 'cyan')] + [dict(loot_entry('xenite_red', uni(1, 3)), weight=2)]},
        {'rolls': uni(1, 3), 'entries': [item_e('diamond', 1, 4, 2), item_e('netherite_scrap', 1, 2, 1), item_e('experience_bottle', 6, 14, 3), item_e('ender_pearl', 3, 8, 2)]}]})
    wjson('bm/loot_table/maps/dread.json', {'type': 'minecraft:command', 'pools': [{'rolls': 1, 'entries': [{
        'type': 'minecraft:item', 'name': 'minecraft:filled_map', 'functions': [
            {'function': 'minecraft:exploration_map', 'destination': 'bm:red_mothership', 'decoration': 'minecraft:red_x', 'zoom': 2,
             'search_radius': 200, 'skip_existing_chunks': False},
            {'function': 'minecraft:set_name', 'target': 'item_name', 'name': T('Vorn Star-Chart', RED)}]}]}]})
    G.consume_adv('sealed_map_dread', 'bm:maps/open_dread')
    fn('maps/open_dread', ['advancement revoke @s only bm:consume/sealed_map_dread', 'loot give @s loot bm:maps/dread',
                           title('@s', 'actionbar', T('The seal cracks... the chart marks a Vorn Dreadnought.', RED))])

    # ------------------------------------------------------------------ CRASH SITES (built into the real terrain at runtime)
    second.append('execute as @e[type=minecraft:marker,tag=bm.crash_seed,tag=!bm.built] at @s if entity @a[distance=..112] '
                  'if loaded ~-18 ~ ~-18 if loaded ~18 ~ ~18 if loaded ~-18 ~ ~18 if loaded ~18 ~ ~-18 run function bm:p32/crash/build')
    floors = {0: 'coarse_dirt', 1: 'blackstone', 2: 'gravel', 3: 'tuff', 4: 'magma_block'}
    cols = []
    for dx in range(-17, 18):
        for dz in range(-17, 18):
            r = math.hypot(dx, dz)
            if r > 17.2: continue
            if r < 11.5:
                d = max(0, int(round(3.2 * (1 - (r / 11.5) ** 2))))
                kind = f'c{d}'
            elif r <= 13.5:
                kind = 'rim'
            else:
                kind = 'scorch'
            cols.append(f'execute positioned ~{dx} ~ ~{dz} positioned over motion_blocking_no_leaves run function bm:p32/crash/{kind}')
    clear = []
    for (x0, x1) in ((-18, -1), (0, 18)):
        for (z0, z1) in ((-18, -1), (0, 18)):
            clear += [f'fill ~{x0} ~-4 ~{z0} ~{x1} ~24 ~{z1} minecraft:air replace #minecraft:logs',
                      f'fill ~{x0} ~-4 ~{z0} ~{x1} ~24 ~{z1} minecraft:air replace #minecraft:leaves',
                      f'fill ~{x0} ~-2 ~{z0} ~{x1} ~6 ~{z1} minecraft:air replace minecraft:vine',
                      f'fill ~{x0} ~-2 ~{z0} ~{x1} ~6 ~{z1} minecraft:air replace minecraft:snow']
    # trees are cleared first (round the worldgen surface the seed sits on), then the seed steps onto the real ground
    fn('p32/crash/build', ['tag @s add bm.built', 'execute align xz positioned ~0.5 ~ ~0.5 run tp @s ~ ~ ~', 'execute at @s run function bm:p32/crash/clear', 'execute positioned over motion_blocking_no_leaves run tp @s ~ ~ ~',
                           'execute at @s run function bm:p32/crash/carve'])
    fn('p32/crash/clear', clear)
    fn('p32/crash/carve', cols + [
        # the saucer, sunk into the crater floor (hull centre one block above the floor, the low edge ploughed in)
        'execute positioned over motion_blocking_no_leaves positioned ~-8 ~-4 ~-8 run place template bm:crash_saucer ~ ~ ~',
        # Xenite deposits on the crater floor, the altar and a wrecked supply chest just outside the hull
        *[f'execute positioned ~{dx} ~ ~{dz} positioned over motion_blocking_no_leaves run function bm:p32/crash/dep_{c}'
          for (dx, dz, c) in [(-9, -3, 'green'), (-6, 7, 'violet'), (6, 7, 'cyan'), (8, -6, 'green'), (1, 10, 'violet'), (-10, 1, 'cyan'), (3, -10, 'cyan')]],
        'execute positioned ~9 ~ ~-3 positioned over motion_blocking_no_leaves run function bm:npc/xaltar',
        'execute positioned ~-9 ~ ~5 positioned over motion_blocking_no_leaves run setblock ~ ~ ~ minecraft:barrel[facing=up,open=false]{LootTable:"bm:p32/crash_wreck"}',
        'execute positioned ~-9 ~ ~6 positioned over motion_blocking_no_leaves run setblock ~ ~ ~ minecraft:iron_trapdoor[facing=north,half=bottom,open=true]',
        'execute positioned ~-7 ~ ~4 positioned over motion_blocking_no_leaves run setblock ~ ~ ~ minecraft:soul_campfire[lit=true,signal_fire=true]',
        'execute positioned ~-7 ~ ~4 positioned over motion_blocking_no_leaves run setblock ~ ~-1 ~ minecraft:hay_block',
        'particle minecraft:explosion_emitter ~ ~2 ~ 1 1 1 0 3', 'particle minecraft:large_smoke ~ ~2 ~ 6 2 6 0.02 200'])
    for d in range(4):
        body = ['execute if block ~ ~ ~ #minecraft:replaceable run setblock ~ ~ ~ minecraft:air']
        if d: body.append(f'fill ~ ~-{d} ~ ~ ~-1 ~ minecraft:air')
        y = -(d + 1)
        body += [f'setblock ~ ~{y} ~ minecraft:coarse_dirt',
                 f'execute if predicate bm:p32/c30 run setblock ~ ~{y} ~ minecraft:blackstone',
                 f'execute if predicate bm:p32/c15 run setblock ~ ~{y} ~ minecraft:gravel',
                 f'execute if predicate bm:p32/c15 run setblock ~ ~{y} ~ minecraft:tuff']
        if d >= 2: body.append(f'execute if predicate bm:p32/c15 run setblock ~ ~{y} ~ minecraft:magma_block')
        fn(f'p32/crash/c{d}', body)
    fn('p32/crash/rim', ['execute if block ~ ~ ~ #minecraft:replaceable run setblock ~ ~ ~ minecraft:air',
                         'execute if predicate bm:p32/c50 run setblock ~ ~ ~ minecraft:coarse_dirt',
                         'execute if predicate bm:p32/c15 run setblock ~ ~ ~ minecraft:gravel',
                         'execute if block ~ ~-1 ~ minecraft:grass_block run setblock ~ ~-1 ~ minecraft:coarse_dirt'])
    fn('p32/crash/scorch', ['execute unless predicate bm:p32/c50 run return 0',
                            'execute if block ~ ~ ~ #minecraft:replaceable run setblock ~ ~ ~ minecraft:air',
                            'execute if block ~ ~-1 ~ #minecraft:dirt run setblock ~ ~-1 ~ minecraft:coarse_dirt',
                            'execute if predicate bm:p32/c30 if block ~ ~-1 ~ minecraft:coarse_dirt run setblock ~ ~-1 ~ minecraft:podzol'])
    for c in ('green', 'violet', 'cyan', 'red'):
        d = {'Tags': ['bm.xdep', f'bm.xc_{c}'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:xdep_{c}'}},
             'item_display': 'fixed', 'brightness': {'block': Int(13), 'sky': Int(13)}, 'view_range': F(1.5),
             'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0), F(0)], 'scale': [F(1), F(1), F(1)]}}
        fn(f'p32/crash/dep_{c}', ['setblock ~ ~ ~ minecraft:amethyst_block', f'summon minecraft:item_display ~ ~0.5 ~ {snbt(d)}'])
    fast.append('execute as @e[type=minecraft:marker,tag=bm.crash_seed,tag=bm.built] at @s if entity @a[distance=..48] run particle minecraft:campfire_signal_smoke ~-7 ~1 ~4 0.2 0.5 0.2 0.01 1 force')
    # Zorp has gone home: crash-site Zorps already in worlds pack up (motherships float at y~200; crash sites never do)
    fn('p32/zorp_leave', ['particle minecraft:end_rod ~ ~1 ~ 0.3 0.6 0.3 0.05 30', 'playsound minecraft:block.beacon.deactivate neutral @a[distance=..16] ~ ~ ~ 1 1.4',
                          'execute positioned ~ ~ ~ run kill @e[type=minecraft:item_display,tag=bm.alien_sprite,distance=..1.5]',
                          'kill @e[type=minecraft:text_display,tag=bm.bubble,distance=..3]', 'tp @s ~ -400 ~'])
    second.append('execute as @e[type=minecraft:wandering_trader,tag=bm.npc_alien] at @s if entity @e[type=minecraft:marker,tag=bm.crash_seed,distance=..40] run function bm:p32/zorp_leave')   # 2.23: by the crash marker (a low mothership sent its Zorp away too)
    # the mothership beam: the Dreadnought's is red
    beam = G.FUNCS['p25/beam']
    G.FUNCS['p25/beam'] = [l.replace('dust{color:[0.49,1.0,0.42],scale:2.0}', 'dust{color:[1.0,0.25,0.2],scale:2.0}') for l in beam]
    fn('p32/beam_red', G.FUNCS['p25/beam'])
    G.FUNCS['p25/beam'] = beam
    fast.append('execute as @e[type=minecraft:marker,tag=bm.tbeam_red] at @s if entity @a[distance=..240] run function bm:p32/beam_red')

    # ------------------------------------------------------------------ INVASION NIGHTS
    OW = '@a[tag=bm.ow]'
    bt = G.FUNCS['bloodmoon/tick']
    bt.append('function bm:p32/inv/tick')
    fn('p32/inv/tick', [
        'execute if score #tod bm.bm matches 12000.. unless score #iday bm.bm = #day bm.bm run function bm:p32/inv/roll',
        'scoreboard players set #iwant bm.bm 0',
        'execute if score #ivn bm.bm matches 1 if score #iday bm.bm = #day bm.bm if score #bday bm.bm matches 0 if score #tod bm.bm matches 13000..22999 run scoreboard players set #iwant bm.bm 1',
        'execute if score #iwant bm.bm matches 1 unless score #inv bm.bm matches 1 run function bm:p32/inv/start',
        'execute if score #iwant bm.bm matches 0 if score #inv bm.bm matches 1 run function bm:p32/inv/end',
        'execute if score #inv bm.bm matches 1 run function bm:p32/inv/during'])
    fn('p32/inv/roll', ['scoreboard players operation #iday bm.bm = #day bm.bm', 'scoreboard players set #ivn bm.bm 0',
                        'execute if score #bday bm.bm matches 1 run return 0',
                        'execute if score #iforce bm.bm matches 1 run scoreboard players set #ivn bm.bm 1', 'scoreboard players set #iforce bm.bm 0',
                        'execute if score #lucky bm.bm matches 1 if score #lday bm.bm = #day bm.bm run return run scoreboard players set #ivn bm.bm 0',
                        'execute store result score #r bm.rng run random value 1..100',
                        f'execute if score #r bm.rng matches 1..{INV_CHANCE} run scoreboard players set #ivn bm.bm 1',
                        'execute if score #ivn bm.bm matches 1 run function bm:p32/inv/warn'])
    fn('p32/inv/warn', [tellraw(OW, PREFIX + [T('Static on every compass. Lights moving where no stars should be... ', GREEN), T('the Vorn are coming tonight.', GREEN, bold=True)]),
                        f'execute as {OW} at @s run playsound minecraft:block.beacon.power_select ambient @s ~ ~ ~ 1 0.5'])
    fn('p32/inv/start', ['scoreboard players set #inv bm.bm 1', 'scoreboard players set #iboss bm.bm 0',
                         f'title {OW} times 20 80 30', title(OW, 'subtitle', T('Saucers in the sky. Glowing beasts in the dark.', GREEN, italic=True)),
                         title(OW, 'title', T('INVASION NIGHT', GREEN, bold=True)),
                         f'execute as {OW} at @s run playsound minecraft:block.end_portal.spawn ambient @s ~ ~ ~ 0.6 1.6',
                         f'execute as {OW} at @s run playsound minecraft:block.beacon.activate ambient @s ~ ~ ~ 1 0.5',
                         f'bossbar set bm:invasion players {OW}', 'bossbar set bm:invasion visible true',
                         tellraw(OW, PREFIX + [T('The Vorn have landed. Their troopers, saucers and bioengineered beasts drop Xenite of every colour until dawn. ', GREEN),
                                               T('A Vorn boss will land at midnight.', GREEN, bold=True)])])
    fn('p32/inv/during', [
        'scoreboard players operation #prog bm.bm = #tod bm.bm', 'scoreboard players remove #prog bm.bm 13000',
        'execute store result bossbar bm:invasion value run scoreboard players get #prog bm.bm', f'bossbar set bm:invasion players {OW}',
        f'execute as @a[tag=bm.ow,gamemode=!spectator] at @s if predicate bm:sees_sky run particle minecraft:dust{{color:[0.5,1.0,0.35],scale:1.6}} ~ ~16 ~ 24 4 24 0 6 normal @s',
        'execute as @a[tag=bm.ow,gamemode=survival] at @s if predicate bm:sees_sky run function bm:p32/inv/surge',
        'execute as @a[tag=bm.ow,gamemode=adventure,tag=!bm.adv] at @s if predicate bm:sees_sky run function bm:p32/inv/surge',
        'execute if score #iboss bm.bm matches 0 if score #tod bm.bm matches 18000.. run function bm:p32/inv/boss_land'])
    fn('p32/inv/surge', [
        'execute store result score #r bm.rng run random value 1..10', 'execute unless score #r bm.rng matches 1 run return 0',     # 2.20: was 1 in 4 a second, up to 9
        'execute store result score #n bm.rng if entity @e[tag=bm.vorn,distance=..64]', 'execute if score #n bm.rng matches 5.. run return 0',
        'summon minecraft:marker ~ ~ ~ {Tags:["bm.vsp"]}',
        'execute as @e[type=minecraft:marker,tag=bm.vsp,distance=..1,limit=1] store result entity @s Rotation[0] float 1 run random value 0..359',
        'execute store result score #k bm.rng run random value 1..100',
        'execute if score #k bm.rng matches 1..38 as @e[type=minecraft:marker,tag=bm.vsp,distance=..1,limit=1] rotated as @s positioned ^ ^ ^22 positioned over motion_blocking_no_leaves run function bm:p32/spawn/trooper',
        'execute if score #k bm.rng matches 39..55 as @e[type=minecraft:marker,tag=bm.vsp,distance=..1,limit=1] rotated as @s positioned ^ ^ ^24 positioned over motion_blocking_no_leaves run function bm:p32/spawn/bigslime',
        'execute if score #k bm.rng matches 56..78 as @e[type=minecraft:marker,tag=bm.vsp,distance=..1,limit=1] rotated as @s positioned ^ ^ ^20 positioned over motion_blocking_no_leaves positioned ~ ~16 ~ run function bm:p32/spawn/saucer',
        'execute if score #k bm.rng matches 79..100 as @e[type=minecraft:marker,tag=bm.vsp,distance=..1,limit=1] rotated as @s positioned ^ ^ ^14 positioned over motion_blocking_no_leaves positioned ~ ~22 ~ run function bm:p32/spawn/bphantom',
        'kill @e[type=minecraft:marker,tag=bm.vsp]'])
    fn('p32/inv/end', ['scoreboard players set #inv bm.bm 0', 'bossbar set bm:invasion visible false',
                       'execute as @e[tag=bm.vtroop] at @s run function bm:p32/beamup', 'execute as @e[tag=bm.vsauc] at @s run function bm:p32/beamup',
                       'execute as @e[tag=bm.vboss] at @s run function bm:p32/beamup',
                       'bossbar set bm:warlord visible false', 'bossbar set bm:abductor visible false', 'bossbar set bm:overseer visible false',
                       tellraw(OW, PREFIX + [T('Dawn. The Vorn ships lift away... for now.', GREEN)])])
    fn('p32/beamup', ['particle minecraft:end_rod ~ ~1 ~ 0.3 1.5 0.3 0.1 30', 'particle minecraft:dust{color:[0.5,1.0,0.35],scale:2.0} ~ ~4 ~ 0.3 4 0.3 0 40',
                      'playsound minecraft:block.beacon.deactivate hostile @a[distance=..24] ~ ~ ~ 1 1.6',
                      'execute on passengers run kill @s', 'tp @s ~ -400 ~'])
    fn('admin/invasion_now', ['execute if score #bday bm.bm matches 1 run return run ' + tellraw('@s', PREFIX + [T('Not on a Blood Moon day.', 'red')]),
                              'scoreboard players set #ivn bm.bm 1', 'scoreboard players operation #iday bm.bm = #day bm.bm',
                              'execute if score #tod bm.bm matches 23000.. run scoreboard players set #iforce bm.bm 1',
                              tellraw('@s', PREFIX + [T('Invasion Night set: tonight (or now, if it is already night).', GREEN)])])
    fn('admin/invasion_stop', ['scoreboard players set #ivn bm.bm 0', 'function bm:p32/inv/end'])
    fn('admin/spawn_warlord', ['function bm:p32/boss/warlord'])
    fn('admin/spawn_abductor', ['execute positioned ~ ~16 ~ run function bm:p32/boss/abductor'])
    fn('admin/spawn_overseer', ['execute positioned ~ ~20 ~ run function bm:p32/boss/overseer'])

    # bioengineered natural spawns (a third of Overworld monsters on an Invasion Night)
    for t in bio_types:
        init = G.FUNCS[f'mobs/init/{t}']
        k = next(i for i, l in enumerate(init) if 'mobs/blood_roll/' in l)
        init.insert(k + 1, f'execute if score #inv bm.bm matches 1 if dimension minecraft:overworld run return run function bm:p32/bio/roll_{t}')
        fn(f'p32/bio/roll_{t}', ['execute store result score #r bm.rng run random value 1..100',
                                 f'execute if score #r bm.rng matches 1..35 run return run function bm:p32/bio/make_{t}'])
        fn(f'p32/bio/make_{t}', [f'data merge entity @s {snbt({"DeathLootTable": f"bm:p32/bio/{t}", "CustomName": G.mob_name("Bioengineered ", "green", t)})}',
                                 'function bm:p32/bio/apply'])
    fn('p32/bio/apply', ['tag @s add bm.bio', 'tag @s add bm.tiered', 'team join bm.bio @s',      # 2.22: the green outline is back (with the 2.20 particles)
                         'attribute @s minecraft:max_health modifier add bm:bio 0.5 add_multiplied_base',
                         'attribute @s minecraft:movement_speed modifier add bm:bio 0.12 add_multiplied_base',
                         'attribute @s minecraft:scale modifier add bm:bio 0.15 add_multiplied_base',
                         'execute store result entity @s Health float 1 run attribute @s minecraft:max_health get'])
    fast.append('execute as @e[tag=bm.bio] at @s if entity @a[distance=..32] run particle minecraft:dust{color:[0.45,1.0,0.3],scale:0.9} ~ ~0.8 ~ 0.3 0.5 0.3 0 2')

    # ------------------------------------------------------------------ Vorn mobs
    def disp(model, scale, ty, tags=('bm.vdisp',), extra=None, rot=None):
        d = {'id': 'minecraft:item_display', 'Tags': list(tags), 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': model}},
             'item_display': 'fixed', 'brightness': {'block': Int(13), 'sky': Int(13)}, 'teleport_duration': Int(2),
             'transformation': {'left_rotation': rot or ident, 'right_rotation': ident, 'translation': [F(0), F(ty), F(0)], 'scale': [F(scale)] * 3}}
        if extra: d.update(extra)
        return d
    invis = {'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}
    fireres = {'id': 'minecraft:fire_resistance', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}
    nodrop = {k: F(0.0) for k in ['head', 'chest', 'legs', 'feet', 'mainhand', 'offhand', 'body']}
    def attrs(**kw): return [{'id': f'minecraft:{k}', 'base': D(v)} for k, v in kw.items()]
    TS = 1.15            # trooper body scale (the model is ~1.6 blocks tall at scale 1)
    trooper = {'Tags': ['bm.seen', 'bm.vorn', 'bm.vtroop'], 'Silent': B(1), 'CanPickUpLoot': B(0), 'CustomName': T('Vorn Trooper', GREEN),
               'DeathLootTable': 'bm:p32/trooper', 'Health': F(30), 'attributes': attrs(max_health=30, movement_speed=0.27, follow_range=40, attack_damage=4),
               'active_effects': [invis, fireres], 'drop_chances': nodrop,
               'Passengers': [disp('bm:vorn3d', TS, round(-HUSK_SEAT + TS / 2, 3), ('bm.vdisp', 'bm.vbody'))]}      # 2.24: on foot (the hoverboard is gone)
    fn('p32/spawn/trooper', ['execute unless block ~ ~ ~ #minecraft:replaceable run return 0', f'summon minecraft:husk ~ ~ ~ {snbt(trooper)}',
                             'particle minecraft:end_rod ~ ~1 ~ 0.3 1 0.3 0.05 20', 'playsound minecraft:block.beacon.power_select hostile @a[distance=..32] ~ ~ ~ 0.8 1.6'])
    SS = 3
    saucer = {'Tags': ['bm.seen', 'bm.vorn', 'bm.vsauc'], 'size': Int(SS), 'Silent': B(1), 'CustomName': T('Vorn Scout Saucer', GREEN),
              'DeathLootTable': 'bm:p32/saucer', 'Health': F(40), 'attributes': attrs(max_health=40, attack_damage=4, follow_range=64),
              'active_effects': [invis, fireres],
              'Passengers': [disp('bm:ufo3d', 2.8, round(-seat_phantom(SS) + 0.2, 3), ('bm.vdisp', 'bm.vufo'))]}
    fn('p32/spawn/saucer', ['execute unless block ~ ~ ~ #minecraft:air run return 0', f'summon minecraft:phantom ~ ~ ~ {snbt(saucer)}',
                            'playsound minecraft:block.beacon.ambient hostile @a[distance=..48] ~ ~ ~ 1 1.8'])
    bigslime = {'Tags': ['bm.seen', 'bm.vorn', 'bm.bio', 'bm.vslime'], 'Size': Int(6), 'CustomName': T('Bioengineered Slime', 'green'),
                'DeathLootTable': 'bm:p32/bigslime',                 'Health': F(60), 'attributes': attrs(max_health=60)}
    fn('p32/spawn/bigslime', ['execute unless block ~ ~ ~ #minecraft:replaceable run return 0', 'execute store result score #s bm.rng run random value 5..7'] +
       [f'execute if score #s bm.rng matches {n} run summon minecraft:slime ~ ~ ~ {snbt(dict(bigslime, Size=Int(n)))}' for n in (5, 6, 7)] +
       ['team join bm.bio @e[type=minecraft:slime,tag=bm.vslime,distance=..2]'])
    bph = {'Tags': ['bm.seen', 'bm.vorn', 'bm.bio', 'bm.vphan'], 'size': Int(5), 'CustomName': T('Bioengineered Phantom', 'green'),
           'DeathLootTable': 'bm:p32/bphantom', 'Health': F(40), 'attributes': attrs(max_health=40, attack_damage=7),
           'active_effects': [fireres]}
    fn('p32/spawn/bphantom', ['execute unless block ~ ~ ~ #minecraft:air run return 0', f'summon minecraft:phantom ~ ~ ~ {snbt(bph)}',
                              'team join bm.bio @e[type=minecraft:phantom,tag=bm.vphan,distance=..2]'])
    # every tick: displays face their mount's way; every second: aim and fire
    tick += ['execute as @e[tag=bm.vtroop] at @s on passengers run rotate @s ~ 0',
             'execute as @e[tag=bm.vsauc] at @s on passengers run rotate @s ~ 0',
             'execute as @e[tag=bm.vboss] at @s on passengers run rotate @s ~ 0']
    second += ['scoreboard players add @e[tag=bm.vtroop] bm.xat 1', 'scoreboard players add @e[tag=bm.vsauc] bm.xat 1',
               'execute as @e[tag=bm.vtroop,scores={bm.xat=3..}] at @s run function bm:p32/troop/fire',
               'execute as @e[tag=bm.vsauc,scores={bm.xat=3..}] at @s run function bm:p32/sauc/fire',
               'execute as @e[tag=bm.vsauc] at @s run particle minecraft:dust{color:[0.5,1.0,0.35],scale:1.2} ~ ~-0.3 ~ 0.6 0.1 0.6 0 6 force @a[distance=..64]',
               'execute as @e[tag=bm.vorn] at @s unless entity @a[distance=..128] run tp @s ~ -400 ~']
    tgt = '@p[distance=..{r},gamemode=!spectator,gamemode=!creative]'
    def fire(name, r, dmg, steps, snd):
        fn(name, ['scoreboard players set @s bm.xat 0', f'execute unless entity {tgt.format(r=r)} run return 0',
                  f'scoreboard players set #bd bm.rng {dmg}', 'tag @s add bm.vshoot', f'scoreboard players set #rr bm.rng {steps}',
                  f'execute anchored eyes facing entity {tgt.format(r=r)} eyes positioned ^ ^ ^1.2 run function bm:p32/beam/step',
                  'tag @s remove bm.vshoot', f'playsound {snd} hostile @a[distance=..{r + 8}] ~ ~ ~ 0.8 1.7'])
    fire('p32/troop/fire', 24, 4, 50, 'minecraft:block.beacon.power_select')
    fire('p32/sauc/fire', 32, 5, 70, 'minecraft:entity.guardian.attack')
    fn('p32/beam/step', ['particle minecraft:dust{color:[0.5,1.0,0.35],scale:0.9} ~ ~ ~ 0 0 0 0 1 force @a[distance=..64]',
                         'execute unless block ~ ~ ~ #bm:grap_pass run return run particle minecraft:electric_spark ~ ~ ~ 0.1 0.1 0.1 0.2 6',
                         'execute positioned ~-0.5 ~-0.5 ~-0.5 if entity @a[dx=0,dy=0,dz=0,gamemode=!spectator,gamemode=!creative] positioned ~0.5 ~0.5 ~0.5 run return run function bm:p32/beam/hit',
                         'scoreboard players remove #rr bm.rng 1', 'execute if score #rr bm.rng matches 1.. positioned ^ ^ ^0.5 run function bm:p32/beam/step'])
    fn('p32/beam/hit', [f'execute if score #bd bm.rng matches {n} positioned ~-0.5 ~-0.5 ~-0.5 run damage @a[dx=0,dy=0,dz=0,gamemode=!spectator,gamemode=!creative,limit=1] {n} bm:plasma by @e[tag=bm.vshoot,limit=1]'
                        for n in (4, 5, 6, 8)] + ['particle minecraft:dust{color:[0.5,1.0,0.35],scale:1.8} ~ ~ ~ 0.2 0.2 0.2 0 14 force @a[distance=..48]'])
    second.append('execute as @e[tag=bm.vtroop] at @s if entity @a[distance=..6] run function bm:p32/troop/say')
    fn('p32/troop/say', ['execute store result score #c bm.rng run random value 1..12', 'execute unless score #c bm.rng matches 1 run return 0',
                         f'execute store result score #l bm.rng run random value 1..{len(TROOPER_SAYS)}'] +
       [f'execute if score #l bm.rng matches {i} run summon minecraft:text_display ~ ~2.6 ~ {snbt({"Tags": ["bm.bubble", "bm.bnew"], "text": T(s, GREEN, bold=True), "billboard": "center", "background": Int(1879048192), "brightness": {"block": Int(15), "sky": Int(15)}, "transformation": {"left_rotation": ident, "right_rotation": ident, "translation": [F(0), F(0), F(0)], "scale": [F(0), F(0), F(0)]}})}'
        for i, s in enumerate(TROOPER_SAYS, 1)])

    # ------------------------------------------------------------------ Vorn bosses
    fn('p32/inv/boss_land', ['scoreboard players set #iboss bm.bm 1',
                             'execute as @a[tag=bm.ow,gamemode=survival] at @s if predicate bm:sees_sky run tag @s add bm.bcand',
                             'execute as @a[tag=bm.bcand,sort=random,limit=1] at @s run function bm:p32/inv/boss_pick', 'tag @a remove bm.bcand'])
    fn('p32/inv/boss_pick', ['execute store result score #r bm.rng run random value 1..2',
                             tellraw(OW, PREFIX + [T('Midnight. Something huge is coming down near ', GREEN), {'selector': '@s', 'color': 'yellow'}, T('...', GREEN)]),
                             'execute if score #r bm.rng matches 1 positioned ^ ^ ^18 positioned over motion_blocking_no_leaves run function bm:p32/boss/warlord',
                             'execute if score #r bm.rng matches 2 positioned ^ ^ ^10 positioned over motion_blocking_no_leaves positioned ~ ~18 ~ run function bm:p32/boss/abductor'])
    WS = 2.2
    warlord = {'Tags': ['bm.seen', 'bm.vorn', 'bm.vboss', 'bm.vb_warlord'], 'Silent': B(1), 'CanPickUpLoot': B(0), 'PersistenceRequired': B(1),
               'CustomName': T('The Vorn Warlord', RED, bold=True), 'CustomNameVisible': B(1), 'DeathLootTable': 'bm:p32/warlord', 'Health': F(400),
               'attributes': attrs(max_health=400, movement_speed=0.3, follow_range=64, attack_damage=10, armor=12, knockback_resistance=1.0, scale=WS),
               'active_effects': [invis, fireres], 'drop_chances': nodrop,
               'Passengers': [disp('bm:vorn3d_warlord', TS * WS, round(-HUSK_SEAT * WS + TS * WS / 2, 3), ('bm.vdisp',))]}
    fn('p32/boss/warlord', [f'summon minecraft:husk ~ ~ ~ {snbt(warlord)}', 'particle minecraft:explosion_emitter ~ ~1 ~ 0 0 0 0 1',
                            'playsound minecraft:entity.wither.spawn hostile @a[distance=..64] ~ ~ ~ 0.8 1.4',
                            'team join bm.vornred @e[tag=bm.vb_warlord,distance=..3]',
                            'title @a[distance=..64] times 10 50 15', title('@a[distance=..64]', 'subtitle', T('Breaker of Worlds', 'gray', italic=True)),
                            title('@a[distance=..64]', 'title', T('THE VORN WARLORD', RED, bold=True))])
    AS = 14
    abductor = {'Tags': ['bm.seen', 'bm.vorn', 'bm.vboss', 'bm.vb_abductor'], 'size': Int(AS), 'Silent': B(1), 'PersistenceRequired': B(1),
                'CustomName': T('The Abductor', GREEN, bold=True), 'CustomNameVisible': B(1), 'DeathLootTable': 'bm:p32/abductor', 'Health': F(320),
                'attributes': attrs(max_health=320, attack_damage=8, follow_range=96, armor=8), 'active_effects': [invis, fireres],
                'Passengers': [disp('bm:ufo3d', 9.0, round(-seat_phantom(AS) + 0.5, 3), ('bm.vdisp',))]}
    fn('p32/boss/abductor', [f'summon minecraft:phantom ~ ~ ~ {snbt(abductor)}', 'playsound minecraft:block.end_portal.spawn hostile @a[distance=..96] ~ ~ ~ 1 1.4',
                             'title @a[distance=..64] times 10 50 15', title('@a[distance=..64]', 'subtitle', T('It wants specimens.', 'gray', italic=True)),
                             title('@a[distance=..64]', 'title', T('THE ABDUCTOR', GREEN, bold=True))])
    OS = 22
    overseer = {'Tags': ['bm.seen', 'bm.vorn', 'bm.vboss', 'bm.vb_overseer'], 'size': Int(OS), 'Silent': B(1), 'PersistenceRequired': B(1),
                'CustomName': T('The Supercharged Overseer', RED, bold=True), 'CustomNameVisible': B(1), 'DeathLootTable': 'bm:p32/overseer', 'Health': F(1200),
                'attributes': attrs(max_health=1200, attack_damage=12, follow_range=128, armor=14, armor_toughness=6), 'active_effects': [invis, fireres],
                'Passengers': [disp('bm:ufo3d_red', 13.0, round(-seat_phantom(OS) + 0.8, 3), ('bm.vdisp',))]}
    fn('p32/boss/overseer', [f'summon minecraft:phantom ~ ~ ~ {snbt(overseer)}', 'playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..128] ~ ~ ~ 1 0.6',
                             'team join bm.vornred @e[tag=bm.vb_overseer,distance=..4]',
                             'title @a[distance=..96] times 10 60 20', title('@a[distance=..96]', 'subtitle', T('The hive answers its beacon.', 'gray', italic=True)),
                             title('@a[distance=..96]', 'title', T('THE SUPERCHARGED OVERSEER', RED, bold=True))])
    for b, hp in (('warlord', 400), ('abductor', 320), ('overseer', 1200)):
        second += [f'execute store result bossbar bm:{b} value run data get entity @e[tag=bm.vb_{b},limit=1] Health',
                   f'bossbar set bm:{b} max {hp}', f'execute if entity @e[tag=bm.vb_{b}] run bossbar set bm:{b} visible true',
                   f'execute unless entity @e[tag=bm.vb_{b}] run bossbar set bm:{b} visible false',
                   f'execute as @e[tag=bm.vb_{b},limit=1] at @s run bossbar set bm:{b} players @a[distance=..96]',
                   f'execute as @e[tag=bm.vb_{b}] at @s run function bm:p32/boss/{b}_tick']
    FT = '@a[distance=..{r},gamemode=!spectator,gamemode=!creative]'
    fn('p32/boss/warlord_tick', ['scoreboard players add @s bm.xat 1', 'scoreboard players add @s bm.xat2 1', 'scoreboard players add @s bm.xlf 1',
                                 'execute if score @s bm.xat matches 6.. run function bm:p32/boss/quake',
                                 'execute if score @s bm.xat2 matches 9.. run function bm:p32/boss/volley',
                                 'execute if score @s bm.xlf matches 15.. run function bm:p32/boss/call_bio'])
    fn('p32/boss/quake', ['scoreboard players set @s bm.xat 0', 'particle minecraft:explosion ~ ~0.5 ~ 3 0.2 3 0 12',
                          'particle minecraft:block{block_state:"minecraft:dirt"} ~ ~0.3 ~ 4 0.2 4 0.2 200',
                          'playsound minecraft:item.mace.smash_ground_heavy hostile @a[distance=..32] ~ ~ ~ 2 0.6',
                          f'execute as {FT.format(r=7)} run damage @s 8 bm:quake by @e[tag=bm.vboss,limit=1,sort=nearest]',
                          f'effect give {FT.format(r=7)} minecraft:levitation 1 2 true', f'effect give {FT.format(r=7)} minecraft:slowness 3 1'])
    fn('p32/boss/volley', ['scoreboard players set @s bm.xat2 0', 'scoreboard players set #bd bm.rng 6', 'tag @s add bm.vshoot',
                           f'execute as {FT.format(r=40)} at @s run tag @s add bm.vtgt',
                           'execute as @a[tag=bm.vtgt,sort=random,limit=3] at @s run function bm:p32/boss/volley_one',
                           'tag @a remove bm.vtgt', 'tag @s remove bm.vshoot', 'playsound minecraft:entity.guardian.attack hostile @a[distance=..48] ~ ~ ~ 1.5 1.2'])
    fn('p32/boss/volley_one', ['scoreboard players set #rr bm.rng 80',
                               'execute positioned as @e[tag=bm.vshoot,limit=1] positioned ~ ~2 ~ facing entity @s eyes positioned ^ ^ ^2 run function bm:p32/beam/step'])
    fn('p32/boss/call_bio', ['scoreboard players set @s bm.xlf 0',
                             'execute store result score #n bm.rng if entity @e[tag=bm.vminion,distance=..48]', 'execute if score #n bm.rng matches 6.. run return 0',
                             'playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..40] ~ ~ ~ 1.5 0.6',
                             *[f'execute positioned ~{dx} ~ ~{dz} positioned over motion_blocking_no_leaves run function bm:p32/boss/bio_minion' for dx, dz in ((4, 0), (-4, 1), (0, -4))]])
    fn('p32/boss/bio_minion', ['execute unless block ~ ~ ~ #minecraft:replaceable run return 0',
                               'summon minecraft:zombie ~ ~ ~ {Tags:["bm.seen","bm.vorn","bm.vminion","bm.newbio"],DeathLootTable:"bm:p32/bio/zombie",CustomName:{text:"Bioengineered Zombie",color:"green"}}',
                               'execute as @e[tag=bm.newbio,distance=..2] run function bm:p32/bio/apply', 'tag @e[tag=bm.newbio] remove bm.newbio',
                               'particle minecraft:end_rod ~ ~1 ~ 0.3 1 0.3 0.05 20'])
    fn('p32/boss/abductor_tick', ['scoreboard players add @s bm.xat 1', 'scoreboard players add @s bm.xat2 1', 'scoreboard players add @s bm.xlf 1',
                                  'particle minecraft:dust{color:[0.5,1.0,0.35],scale:3.0} ~ ~-1 ~ 3 0.3 3 0 20 force @a[distance=..96]',
                                  'execute if score @s bm.xat matches 4.. run function bm:p32/boss/volley_a',
                                  'execute if score @s bm.xat2 matches 10.. run function bm:p32/boss/tractor',
                                  'execute if score @s bm.xlf matches 14.. run function bm:p32/boss/deploy'])
    fn('p32/boss/volley_a', ['scoreboard players set @s bm.xat 0', 'scoreboard players set #bd bm.rng 6', 'tag @s add bm.vshoot',
                             f'execute as {FT.format(r=48)} at @s run tag @s add bm.vtgt',
                             'execute as @a[tag=bm.vtgt,sort=random,limit=2] at @s run function bm:p32/boss/volley_one',
                             'tag @a remove bm.vtgt', 'tag @s remove bm.vshoot', 'playsound minecraft:entity.guardian.attack hostile @a[distance=..64] ~ ~ ~ 1.5 1.0'])
    fn('p32/boss/tractor', ['scoreboard players set @s bm.xat2 0',
                            f'execute as {FT.format(r=40)} at @s run tag @s add bm.vtgt',
                            'execute as @a[tag=bm.vtgt,sort=random,limit=1] at @s run function bm:p32/boss/tractor_on', 'tag @a remove bm.vtgt'])
    fn('p32/boss/tractor_on', ['effect give @s minecraft:levitation 3 2', 'particle minecraft:end_rod ~ ~2 ~ 0.4 2 0.4 0.05 40',
                               'playsound minecraft:block.beacon.activate hostile @s ~ ~ ~ 1 1.6',
                               title('@s', 'actionbar', T('You are being ABDUCTED! Shoot it down!', GREEN, bold=True))])
    fn('p32/boss/deploy', ['scoreboard players set @s bm.xlf 0', 'execute store result score #n bm.rng if entity @e[tag=bm.vtroop,distance=..64]',
                           'execute if score #n bm.rng matches 6.. run return 0',
                           f'execute as {FT.format(r=48)} at @s run tag @s add bm.vtgt',
                           'execute as @a[tag=bm.vtgt,sort=random,limit=1] at @s run function bm:p32/boss/deploy_at', 'tag @a remove bm.vtgt'])
    fn('p32/boss/deploy_at', ['execute positioned ~5 ~ ~3 positioned over motion_blocking_no_leaves run function bm:p32/spawn/trooper',
                              'execute positioned ~-4 ~ ~-4 positioned over motion_blocking_no_leaves run function bm:p32/spawn/trooper'])
    fn('p32/boss/overseer_tick', ['scoreboard players add @s bm.xat 1', 'scoreboard players add @s bm.xat2 1', 'scoreboard players add @s bm.xlf 1',
                                  'particle minecraft:dust{color:[1.0,0.25,0.2],scale:3.0} ~ ~-1 ~ 4 0.4 4 0 30 force @a[distance=..128]',
                                  'execute store result score #mh bm.rng run data get entity @s Health',
                                  'execute if score #mh bm.rng matches ..600 unless entity @s[tag=bm.rage] run function bm:p32/boss/o_phase2',
                                  'execute if score #mh bm.rng matches ..240 unless entity @s[tag=bm.rage2] run function bm:p32/boss/o_phase3',
                                  'execute if score @s bm.xat matches 3.. run function bm:p32/boss/volley_o',
                                  'execute if score @s bm.xat2 matches 9.. run function bm:p32/boss/tractor',
                                  'execute if score @s bm.xlf matches 12.. run function bm:p32/boss/deploy',
                                  'execute if entity @s[tag=bm.rage] if score @s bm.xlf matches 6 run function bm:p32/boss/o_slimes'])
    fn('p32/boss/volley_o', ['scoreboard players set @s bm.xat 0', 'scoreboard players set #bd bm.rng 8', 'tag @s add bm.vshoot',
                             f'execute as {FT.format(r=64)} at @s run tag @s add bm.vtgt',
                             'execute as @a[tag=bm.vtgt,sort=random,limit=3] at @s run function bm:p32/boss/volley_one',
                             'tag @a remove bm.vtgt', 'tag @s remove bm.vshoot', 'playsound minecraft:entity.guardian.attack hostile @a[distance=..96] ~ ~ ~ 2 0.8'])
    fn('p32/boss/o_phase2', ['tag @s add bm.rage', 'effect give @s minecraft:resistance 10 2 true',
                             title('@a[distance=..96]', 'actionbar', T('The Overseer raises its shields and calls the hive!', RED, bold=True)),
                             'playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..96] ~ ~ ~ 1 1',
                             *[f'execute positioned ~{dx} ~-4 ~{dz} run function bm:p32/spawn/bphantom' for dx, dz in ((6, 0), (-6, 0), (0, 6), (0, -6))]])
    fn('p32/boss/o_phase3', ['tag @s add bm.rage2', 'effect give @s minecraft:strength infinite 1 true',
                             title('@a[distance=..96]', 'actionbar', T('OVERLOAD! The Overseer burns white-hot!', RED, bold=True)),
                             'playsound minecraft:entity.wither.spawn hostile @a[distance=..96] ~ ~ ~ 1 1.2'])
    fn('p32/boss/o_slimes', [f'execute as {FT.format(r=48)} at @s run tag @s add bm.vtgt',
                             'execute as @a[tag=bm.vtgt,sort=random,limit=1] at @s positioned ~3 ~ ~3 positioned over motion_blocking_no_leaves run function bm:p32/spawn/bigslime',
                             'tag @a remove bm.vtgt'])
    # the beacon that calls the Overseer
    fn('p32/beacon/use', ['execute unless score #inv bm.bm matches 1 run return run ' + title('@s', 'actionbar', T('Only on an Invasion Night. The beacon stays dark.', 'gray')),
                          'execute unless dimension minecraft:overworld run return run ' + title('@s', 'actionbar', T('The beacon needs the Overworld sky.', 'gray')),
                          'execute unless predicate bm:sees_sky run return run ' + title('@s', 'actionbar', T('Step out under the open sky.', 'gray')),
                          'execute if entity @e[tag=bm.vb_overseer] run return run ' + title('@s', 'actionbar', T('The Overseer is already here!', RED)),
                          'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"overcharged_beacon"}] run item modify entity @s weapon.mainhand bm:p24/take_1',
                          'execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"overcharged_beacon"}] run item modify entity @s weapon.offhand bm:p24/take_1',
                          'summon minecraft:marker ~ ~ ~ {Tags:["bm.becon"]}', 'scoreboard players set @e[type=minecraft:marker,tag=bm.becon,distance=..1] bm.xlf 0',
                          tellraw('@a[distance=..96]', PREFIX + [{'selector': '@s', 'color': 'yellow'}, T(' lit an Overcharged Beacon. The hive is answering...', RED)]),
                          'playsound minecraft:block.beacon.activate player @a[distance=..48] ~ ~ ~ 2 0.5'])
    second += ['scoreboard players add @e[type=minecraft:marker,tag=bm.becon] bm.xlf 1',
               'execute as @e[type=minecraft:marker,tag=bm.becon] at @s run particle minecraft:dust{color:[1.0,0.25,0.2],scale:2.0} ~ ~ ~ 0.3 12 0.3 0 80 force @a[distance=..128]',
               'execute as @e[type=minecraft:marker,tag=bm.becon,scores={bm.xlf=6..}] at @s positioned ~ ~22 ~ run function bm:p32/boss/overseer',
               'kill @e[type=minecraft:marker,tag=bm.becon,scores={bm.xlf=6..}]']

    # ------------------------------------------------------------------ RED XENITE: sockets (size) and the growth / shrink rays
    use = G.FUNCS['p24/altar/use']
    k = next(i for i, l in enumerate(use) if 'already has a socket' in l)
    use.insert(k, 'execute if items entity @s weapon.offhand ' + shard('red') + ' run return run function bm:p32/altar/red')
    use[:] = [l for l in use if 'bm:p24/altar/sock_red' not in l]       # (phase24's per-colour loop saw red in COLORS)
    lore_red = T('◆ Red Xenite socket: shifts your size while held or worn (socket another red shard to flip it)', RED)
    wjson('bm/item_modifier/p32/sock_red_new.json', [{'function': 'minecraft:set_custom_data', 'tag': f'{{bm_sock:1b,bm_sockc:"red",bm_red:"grow",bmv:{ITEM_VERSION}}}'},
                                                     {'function': 'minecraft:set_lore', 'mode': 'append', 'lore': [lore_red]}])
    wjson('bm/item_modifier/p32/sock_red_grow.json', {'function': 'minecraft:set_custom_data', 'tag': '{bm_red:"grow"}'})
    wjson('bm/item_modifier/p32/sock_red_shrink.json', {'function': 'minecraft:set_custom_data', 'tag': '{bm_red:"shrink"}'})
    fn('p32/altar/red', ['execute unless items entity @s weapon.mainhand *[minecraft:max_damage] run return run function bm:p24/altar/help',
                         'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bm_red:"grow"}] run return run function bm:p32/altar/red_flip_s',
                         'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bm_red:"shrink"}] run return run function bm:p32/altar/red_flip_g',
                         'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bm_sock:1b}] run return run ' + title('@s', 'actionbar', T('That item already has a socket.', 'gray')),
                         'item modify entity @s weapon.mainhand bm:p32/sock_red_new', 'item modify entity @s weapon.offhand bm:p24/take_1',
                         'playsound minecraft:block.amethyst_block.resonate player @a[distance=..12] ~ ~ ~ 1 0.6',
                         'particle minecraft:dust{color:[1.0,0.25,0.2],scale:1.4} ~ ~1.2 ~ 0.3 0.3 0.3 0 20',
                         title('@s', 'actionbar', T('Socketed! Red Xenite: GROWTH while held or worn.', RED))])
    for a, b_, word in (('s', 'shrink', 'SHRINK'), ('g', 'grow', 'GROWTH')):
        fn(f'p32/altar/red_flip_{a}', [f'item modify entity @s weapon.mainhand bm:p32/sock_red_{b_}', 'item modify entity @s weapon.offhand bm:p24/take_1',
                                       'playsound minecraft:block.amethyst_block.resonate player @a[distance=..12] ~ ~ ~ 1 1.4',
                                       title('@s', 'actionbar', T(f'The red crystal flips: {word}.', RED))])
    # every second: a player's red sockets (held or worn) set their size
    slots = ['weapon.mainhand', 'weapon.offhand', 'armor.head', 'armor.chest', 'armor.legs', 'armor.feet']
    rs = ['scoreboard players set #rg bm.rng 0']
    for s_ in slots:
        rs += [f'execute if items entity @s {s_} *[minecraft:custom_data~{{bm_red:"grow"}}] run scoreboard players add #rg bm.rng 1',
               f'execute if items entity @s {s_} *[minecraft:custom_data~{{bm_red:"shrink"}}] run scoreboard players remove #rg bm.rng 1']
    rs += ['execute if score #rg bm.rng matches 2.. run scoreboard players set #rg bm.rng 2', 'execute if score #rg bm.rng matches ..-2 run scoreboard players set #rg bm.rng -2',
           'execute if score @s bm.rsc = #rg bm.rng run return 0', 'scoreboard players operation @s bm.rsc = #rg bm.rng',
           'attribute @s minecraft:scale modifier remove bm:red_socket']
    for v, amt in ((2, 1.0), (1, 0.5), (-1, -0.35), (-2, -0.6)):
        rs.append(f'execute if score #rg bm.rng matches {v} run attribute @s minecraft:scale modifier add bm:red_socket {amt} add_multiplied_base')
    fn('p32/red_size', rs)
    second.append('execute as @a run function bm:p32/red_size')
    # infusions: crossbow + 8 red = Growth Ray, bow + 8 red = Shrink Ray (the altar's sneak-click)
    inf = G.FUNCS['p24/altar/infuse']
    for test, res in (('minecraft:crossbow', 'growth_ray'), ('minecraft:bow', 'shrink_ray')):
        inf.insert(0, f'execute if items entity @s weapon.mainhand {test} if items entity @s weapon.offhand {shard("red")} run return run function bm:p32/altar/inf_{res}')
        fn(f'p32/altar/inf_{res}', ['execute store result score #n bm.rng run data get entity @s equipment.offhand.count',
                                    'execute if score #n bm.rng matches ..7 run return run ' + title('@s', 'actionbar', T('You need 8 Red Xenite shards in your off hand.', 'gray')),
                                    'item modify entity @s weapon.offhand bm:p24/take_8', 'item modify entity @s weapon.mainhand bm:p24/take_1', give(res),
                                    'playsound minecraft:block.beacon.activate player @a[distance=..12] ~ ~ ~ 1 0.8',
                                    'particle minecraft:dust{color:[1.0,0.25,0.2],scale:1.4} ~ ~1.2 ~ 0.3 0.4 0.3 0 30',
                                    title('@s', 'actionbar', T(f'The altar hums - you made a {ITEMS[res]["name"]}!', RED))])
    G.FUNCS['p24/altar/help'].append(tellraw('@s', [T('Red Xenite: ', RED, bold=True), T('socket it to grow (another red shard flips it to shrink); sneak-infuse a crossbow (Growth Ray) or bow (Shrink Ray) with 8.', 'gray')]))
    gu = G.FUNCS['p21/grap/use']
    gu[1:1] = ['execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"growth_ray"}] run return run function bm:p32/ray/fire {d:1}',
               'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"shrink_ray"}] run return run function bm:p32/ray/fire {d:-1}',
               'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"plasma_blaster"}] run return run function bm:p32/blaster/fire']
    fn('p32/ray/fire', ['execute if score @s bm.rcd matches 1.. run return 0',
                        'execute unless score @s bm.rred matches 1.. store result score #s bm.rng run clear @s ' + shard('red') + ' 0',
                        'execute unless score @s bm.rred matches 1.. if score #s bm.rng matches 0 run return run ' + title('@s', 'actionbar', T('Out of power - carry Red Xenite shards.', 'red')),
                        'execute unless score @s bm.rred matches 1.. run clear @s ' + shard('red') + ' 1',
                        'execute unless score @s bm.rred matches 1.. run scoreboard players set @s bm.rred 4',
                        'scoreboard players remove @s bm.rred 1', 'scoreboard players set @s bm.rcd 15',
                        '$scoreboard players set #rdir bm.rng $(d)', 'tag @s add bm.shooter', 'scoreboard players set #rr bm.rng 100',
                        'playsound minecraft:block.beacon.power_select player @a[distance=..20] ~ ~ ~ 0.8 0.6',
                        'execute anchored eyes positioned ^ ^ ^0.6 run function bm:p32/ray/step', 'tag @s remove bm.shooter'])
    fn('p32/ray/step', ['particle minecraft:dust{color:[1.0,0.3,0.25],scale:0.7} ~ ~ ~ 0 0 0 0 1 force @a[distance=..48]',
                        'execute unless block ~ ~ ~ #bm:grap_pass run return 0',
                        f'execute positioned ~-0.5 ~-0.5 ~-0.5 if entity @e[dx=0,dy=0,dz=0,type=!#bm:p32_nobeam,tag=!bm.shooter,tag=!bm.npc,tag=!bm.vdisp] positioned ~0.5 ~0.5 ~0.5 run return run function bm:p32/ray/hit',
                        'scoreboard players remove #rr bm.rng 1', 'execute if score #rr bm.rng matches 1.. positioned ^ ^ ^0.4 run function bm:p32/ray/step'])
    fn('p32/ray/hit', ['execute positioned ~-0.5 ~-0.5 ~-0.5 as @e[dx=0,dy=0,dz=0,type=!#bm:p32_nobeam,tag=!bm.shooter,tag=!bm.npc,tag=!bm.vdisp,limit=1,sort=nearest] at @s run function bm:p32/ray/apply',
                       'particle minecraft:dust{color:[1.0,0.3,0.25],scale:1.6} ~ ~ ~ 0.25 0.25 0.25 0 20 force @a[distance=..48]'])
    fn('p32/ray/apply', ['execute if entity @s[type=minecraft:player] run return run function bm:p32/ray/player',
                         'execute store result score #s bm.rng run attribute @s minecraft:scale base get 100',
                         'execute if score #rdir bm.rng matches 1 run scoreboard players operation #s bm.rng *= #5 bm.rng',
                         'execute if score #rdir bm.rng matches 1 run scoreboard players operation #s bm.rng /= #4 bm.rng',
                         'execute if score #rdir bm.rng matches -1 run scoreboard players operation #s bm.rng *= #4 bm.rng',
                         'execute if score #rdir bm.rng matches -1 run scoreboard players operation #s bm.rng /= #5 bm.rng',
                         'execute if score #s bm.rng matches ..15 run scoreboard players set #s bm.rng 15', 'execute if score #s bm.rng matches 600.. run scoreboard players set #s bm.rng 600',
                         'execute store result storage bm:tmp ray.s double 0.01 run scoreboard players get #s bm.rng',
                         'function bm:p32/ray/set with storage bm:tmp ray',
                         'playsound minecraft:entity.puffer_fish.blow_up neutral @a[distance=..16] ~ ~ ~ 1 1'])
    fn('p32/ray/set', ['$attribute @s minecraft:scale base set $(s)'])
    fn('p32/ray/player', ['scoreboard players operation @s bm.rays += #rdir bm.rng', 'execute if score @s bm.rays matches 3.. run scoreboard players set @s bm.rays 2',
                          'execute if score @s bm.rays matches ..-3 run scoreboard players set @s bm.rays -2', 'scoreboard players set @s bm.rayt 30',
                          'function bm:p32/ray/pmod', title('@s', 'actionbar', T('A ray hits you! Your size shifts for 30 seconds.', RED))])
    pm = ['attribute @s minecraft:scale modifier remove bm:size_ray']
    for v, amt in ((2, 0.6), (1, 0.3), (-1, -0.25), (-2, -0.45)):
        pm.append(f'execute if score @s bm.rays matches {v} run attribute @s minecraft:scale modifier add bm:size_ray {amt} add_multiplied_base')
    fn('p32/ray/pmod', pm)
    second += ['scoreboard players remove @a[scores={bm.rayt=1..}] bm.rayt 1',
               'execute as @a[scores={bm.rayt=0,bm.rays=-9..9}] unless score @s bm.rays matches 0 run function bm:p32/ray/pclear']
    fn('p32/ray/pclear', ['scoreboard players set @s bm.rays 0', 'attribute @s minecraft:scale modifier remove bm:size_ray'])
    load += ['scoreboard players set #4 bm.rng 4', 'scoreboard players set #5 bm.rng 5']
    # the plasma blaster (cyan ammo, fast)
    cyan = shard('cyan')
    fn('p32/blaster/fire', ['execute if score @s bm.pbcd matches 1.. run return 0',
                            'execute unless score @s bm.pbammo matches 1.. store result score #s bm.rng run clear @s ' + cyan + ' 0',
                            'execute unless score @s bm.pbammo matches 1.. if score #s bm.rng matches 0 run return run ' + title('@s', 'actionbar', T('Out of power - carry Cyan Xenite shards.', 'red')),
                            f'execute unless score @s bm.pbammo matches 1.. run clear @s {cyan} 1',
                            'execute unless score @s bm.pbammo matches 1.. run scoreboard players set @s bm.pbammo 6',
                            'scoreboard players remove @s bm.pbammo 1', 'scoreboard players set @s bm.pbcd 6', 'tag @s add bm.shooter', 'scoreboard players set #rr bm.rng 100',
                            'playsound minecraft:entity.guardian.attack player @a[distance=..20] ~ ~ ~ 0.8 2',
                            'execute anchored eyes positioned ^ ^ ^0.6 run function bm:p32/blaster/step', 'tag @s remove bm.shooter'])
    fn('p32/blaster/step', ['particle minecraft:dust{color:[0.45,1.0,0.3],scale:0.9} ~ ~ ~ 0 0 0 0 1 force @a[distance=..48]',
                            'execute unless block ~ ~ ~ #bm:grap_pass run return run particle minecraft:electric_spark ~ ~ ~ 0.1 0.1 0.1 0.2 8',
                            f'execute positioned ~-0.5 ~-0.5 ~-0.5 if entity @e[dx=0,dy=0,dz=0,{mob_ok},tag=!bm.shooter,tag=!bm.vdisp] positioned ~0.5 ~0.5 ~0.5 run return run function bm:p32/blaster/hit',
                            'scoreboard players remove #rr bm.rng 1', 'execute if score #rr bm.rng matches 1.. positioned ^ ^ ^0.4 run function bm:p32/blaster/step'])
    fn('p32/blaster/hit', [f'execute positioned ~-0.5 ~-0.5 ~-0.5 as @e[dx=0,dy=0,dz=0,{mob_ok},tag=!bm.shooter,tag=!bm.vdisp,limit=1,sort=nearest] run damage @s 9 minecraft:indirect_magic by @a[tag=bm.shooter,limit=1]',
                           'particle minecraft:dust{color:[0.45,1.0,0.3],scale:1.8} ~ ~ ~ 0.25 0.25 0.25 0 20 force @a[distance=..48]'])
    tick.append('scoreboard players remove @a[scores={bm.pbcd=1..}] bm.pbcd 1')

    # ------------------------------------------------------------------ QUAKE MAUL
    fn('p32/quake/use', ['execute if score @s bm.qcd matches 1.. run return run ' + title('@s', 'actionbar', [T('The maul is still ringing: ', 'gray'), {'score': {'name': '@s', 'objective': 'bm.qcd'}, 'color': 'white'}, T(' s', 'gray')]),
                         'scoreboard players set @s bm.qcd 4', 'tag @s add bm.quaker',
                         'particle minecraft:explosion ~ ~0.3 ~ 3 0.1 3 0 10', 'particle minecraft:block{block_state:"minecraft:dirt"} ~ ~0.2 ~ 3.5 0.1 3.5 0.3 220',
                         'particle minecraft:dust{color:[1.0,0.25,0.2],scale:2.0} ~ ~0.4 ~ 3.5 0.2 3.5 0 60',
                         'playsound minecraft:item.mace.smash_ground_heavy player @a[distance=..32] ~ ~ ~ 2 0.6',
                         f'execute as @e[distance=0.5..7,{mob_ok},tag=!bm.quaker] run function bm:p32/quake/hit',
                         'tag @s remove bm.quaker'])
    fn('p32/quake/hit', ['damage @s 10 bm:quake by @a[tag=bm.quaker,limit=1]', 'effect give @s minecraft:levitation 1 3 true', 'effect give @s minecraft:slowness 3 2'])
    second.append('scoreboard players remove @a[scores={bm.qcd=1..}] bm.qcd 1')

    # ------------------------------------------------------------------ GRAVITIC CORE: hover-flight while carried
    gc = '*[minecraft:custom_data~{bm:"gravitic_core"}]'
    tick += ['tag @a remove bm.hasgc',
             f'execute as @a[gamemode=!spectator,gamemode=!creative] if items entity @s container.* {gc} run tag @s add bm.hasgc',
             f'execute as @a[gamemode=!spectator,gamemode=!creative,tag=!bm.hasgc] if items entity @s weapon.offhand {gc} run tag @s add bm.hasgc',
             'execute as @a[tag=bm.hasgc] at @s run function bm:p32/gcore/tick',
             'execute as @a[tag=!bm.hasgc,scores={bm.gcfly=1}] run function bm:p32/gcore/land']
    fn('p32/gcore/tick', ['scoreboard players set #j bm.rng 0', 'execute if predicate bm:p26/jump_key run scoreboard players set #j bm.rng 1',
                          'execute unless predicate bm:p21/airborne run scoreboard players set @s bm.gcair 0',
                          'execute unless predicate bm:p21/airborne if score @s bm.gcfly matches 1 run function bm:p32/gcore/land',
                          'execute if predicate bm:p21/airborne run scoreboard players add @s bm.gcair 1',
                          'execute unless score @s bm.gcfly matches 1 if predicate bm:p21/airborne if score @s bm.gcair matches 3.. if score #j bm.rng matches 1 unless score @s bm.gcj matches 1 unless predicate bm:p26/no_rocket run function bm:p32/gcore/takeoff',
                          'execute if score @s bm.gcfly matches 1 run function bm:p32/gcore/fly',
                          'scoreboard players operation @s bm.gcj = #j bm.rng'])
    fn('p32/gcore/takeoff', ['scoreboard players set @s bm.gcfly 1', 'attribute @s minecraft:gravity modifier add bm:gcore -1 add_multiplied_total',
                             'attribute @s minecraft:safe_fall_distance modifier add bm:gcore 512 add_value',
                             'playsound minecraft:block.beacon.power_select player @a[distance=..16] ~ ~ ~ 0.6 2',
                             title('@s', 'actionbar', T('Hover-flight: hold jump to rise, sneak to sink.', '#e0fcff'))])
    fn('p32/gcore/fly', ['execute if score #j bm.rng matches 1 run effect give @s minecraft:levitation 1 5 true',
                         'execute if score #j bm.rng matches 0 run effect clear @s minecraft:levitation',
                         'execute if predicate bm:p20/sneaking run attribute @s minecraft:gravity modifier remove bm:gcore',
                         'execute unless predicate bm:p20/sneaking run attribute @s minecraft:gravity modifier add bm:gcore -1 add_multiplied_total',
                         'execute if predicate bm:p20/sneaking run effect give @s minecraft:slow_falling 1 0 true',
                         'particle minecraft:end_rod ~ ~-0.2 ~ 0.2 0 0.2 0.01 1'])
    fn('p32/gcore/land', ['scoreboard players set @s bm.gcfly 0', 'attribute @s minecraft:gravity modifier remove bm:gcore',
                          'effect clear @s minecraft:levitation', 'execute unless entity @s[tag=bm.hasgc] run attribute @s minecraft:safe_fall_distance modifier remove bm:gcore'])
    second.append('execute as @a[tag=bm.hasgc,scores={bm.gcfly=0}] run attribute @s minecraft:safe_fall_distance modifier add bm:gcore 512 add_value')
    second.append('execute as @a[tag=!bm.hasgc] run attribute @s minecraft:safe_fall_distance modifier remove bm:gcore')

    # ------------------------------------------------------------------ XENO VISOR
    second += ['execute as @a if items entity @s armor.head *[minecraft:custom_data~{bm:"xeno_visor"}] at @s run function bm:p32/visor']
    fn('p32/visor', ['effect give @s minecraft:night_vision 15 0 true', 'effect give @e[type=#bm:hostile,distance=..24] minecraft:glowing 2 0 true'])

    # ------------------------------------------------------------------ THE VORN DREADNOUGHT (runtime: guards on approach)
    second += ['execute as @e[type=minecraft:marker,tag=bm.dread_core] at @s if entity @a[distance=..40,gamemode=!spectator,gamemode=!creative] unless score @s bm.xlf matches 1.. run function bm:p32/dread/alarm',
               'scoreboard players remove @e[type=minecraft:marker,tag=bm.dread_core,scores={bm.xlf=1..}] bm.xlf 1']
    fn('p32/dread/alarm', ['scoreboard players set @s bm.xlf 1800',
                           'execute as @e[type=minecraft:marker,tag=bm.vguard,distance=..40] at @s run function bm:p32/spawn/trooper',
                           'execute at @e[type=minecraft:marker,tag=bm.vguard_boss,distance=..40,limit=1] run function bm:p32/spawn/trooper',
                           'execute at @e[type=minecraft:marker,tag=bm.vguard_boss,distance=..40,limit=1] run function bm:p32/spawn/trooper',
                           title('@a[distance=..40]', 'actionbar', T('INTRUDER. INTRUDER. THE HIVE WILL IMPROVE YOU.', RED, bold=True)),
                           'playsound minecraft:block.bell.resonate hostile @a[distance=..48] ~ ~ ~ 2 0.5'])

    G.FUNCS['npc/abductee'].append('execute if entity @s[tag=bm.ab_villager] run function bm:p32/abduct_villager')
    fn('p32/abduct_villager', [f'summon minecraft:villager ~ ~ ~ {snbt({"Tags": ["bm.abductee", "bm.seen"], "PersistenceRequired": B(1), "CustomName": T("Abducted Villager", "gray"), "VillagerData": {"type": "minecraft:plains", "profession": "minecraft:none", "level": Int(1)}})}'])
    holo = {'Tags': ['bm.xholo', 'bm.new'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:xenite_red'}},
            'item_display': 'fixed', 'billboard': 'fixed', 'brightness': {'block': Int(15), 'sky': Int(15)}, 'teleport_duration': Int(5),
            'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0), F(0)], 'scale': [F(2.2), F(2.2), F(2.2)]}}
    fn('npc/xholo_red', [f'summon minecraft:item_display ~ ~ ~ {snbt(holo)}', 'tag @e[tag=bm.new,distance=..1] remove bm.new'])
    G.FUNCS['npc/spawn'][0:0] = ['execute if entity @s[tag=bm.npc.xholo_red] run function bm:npc/xholo_red']

    G.FUNCS['load'][-1:-1] = load
    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


def post_admin(G):
    T_, tr = G.T, G.tellraw
    G.FUNCS['admin/uninstall'][0:0] = ['bossbar remove bm:invasion', 'bossbar remove bm:warlord', 'bossbar remove bm:abductor', 'bossbar remove bm:overseer',
                                       'team remove bm.bio', 'team remove bm.vornred']
    G.FUNCS['admin/help'] += [tr('@s', [T_('/function bm:admin/invasion_now', 'yellow'), T_('  tonight is an Invasion Night (', 'gray'), T_('invasion_stop', 'yellow'), T_(' ends it)', 'gray')]),
                              tr('@s', [T_('/function bm:admin/spawn_<warlord|abductor|overseer>', 'yellow'), T_('  a Vorn boss at your feet', 'gray')]),
                              tr('@s', [T_('/function bm:admin/place_dreadnought', 'yellow'), T_('  a Vorn Dreadnought 40 blocks up (/locate structure bm:red_mothership)', 'gray')])]
    G.fn('admin/place_crash_site', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.crash_seed"]}',
                                    'execute as @e[type=minecraft:marker,tag=bm.crash_seed,distance=..1,limit=1] at @s run function bm:p32/crash/build',
                                    G.tellraw('@s', G.PREFIX + [T('Crash site carved around you.', 'gray')])])
    G.fn('admin/place_dreadnought', [f'execute positioned ~ ~40 ~ run place template bm:red_mothership ~-{R25.MC} ~-2 ~-{R25.MC}',
                                     G.tellraw('@s', G.PREFIX + [T('A Vorn Dreadnought hangs overhead. Its red beam is right where you stand.', 'gray')])])


# ===================================================================== structures
def build_crash_seed():
    """The worldgen piece: a lone marker. Everything else is carved into the real ground at runtime (p32/crash/build)."""
    from structures import Build
    Bd = Build(1, 1, 1)
    Bd.marker(0.5, 0.0, 0.5, ['bm.crash_seed'], 0)
    return Bd


def build_crash_saucer():
    """The tilted saucer alone (17 x 12 x 17), placed 6 below the crater's surface centre. Its low side ploughs into the
    floor; dirt fills under the hull so it never sits on air."""
    from structures import Build
    SX, SY, SZ = 17, 12, 17
    Bd = Build(SX, SY, SZ)
    S = Bd.set
    cx = cz = 8
    tilt = math.tan(math.radians(16))
    for x in range(SX):
        for z in range(SZ):
            d = math.hypot(x - cx, z - cz)
            if d > 7.4: continue
            y = 4 + round((x - cx) * tilt)
            for yy in range(0, y): S(x, yy, z, 'coarse_dirt' if (x + yy + z) % 3 else 'gravel')
            S(x, y, z, 'light_gray_concrete' if d < 5.5 else 'iron_block')
            if d >= 6.4:
                S(x, y + 1, z, 'sea_lantern' if (x + z) % 3 == 0 else 'iron_block')
            elif d < 3.6:
                for h in range(1, 4 - (1 if d > 2.5 else 0)):
                    S(x, y + h, z, 'light_blue_stained_glass' if h < 3 or d < 1.5 else 'air')
                S(x, y + (3 if d <= 2.5 else 2), z, 'light_blue_stained_glass')
            else:
                S(x, y + 1, z, 'smooth_stone_slab[type=bottom,waterlogged=false]' if (x * 7 + z) % 5 else 'end_rod[facing=up]')
            for yy in range(y + 2, SY):
                if (x, yy, z) not in Bd.b: S(x, yy, z, 'air')
    y0 = 4
    S(cx, y0 + 1, cz, 'quartz_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]')
    S(cx - 1, y0 + 1, cz, 'cyan_stained_glass'); S(cx - 1, y0 + 2, cz, 'air')
    hx, hz = cx + 6, cz - 3
    hy = 4 + round((hx - cx) * tilt)
    for h in range(1, 4): S(hx, hy + h, hz, 'lightning_rod[facing=up,powered=false,waterlogged=false]')
    S(hx + 1, hy + 4, hz, 'lightning_rod[facing=east,powered=false,waterlogged=false]')
    return Bd


def build_dreadnought():
    """A Vorn Dreadnought: the mothership hull in red, hostile guards instead of crew, red Xenite in the reactor, an armoury
    on the bridge instead of a quartermaster, and no Donado (the cell holds a different prisoner)."""
    Bd = R25.build_mothership(red=True)
    return Bd


# ===================================================================== resource pack
def rp(R):
    """Icons + 3D models (Donadian redesign, Vorn trooper/warlord, saucers, hoverboards, cosmetics)."""
    grid = R.grid
    I = {}
    I['xenite_red'] = grid([
        '................', '.......D........', '......DLD.......', '......DLMD......', '.....DLMMD......', '.....DLMMMD.....',
        '....DLMMMMD.....', '....DLMMMMMD....', '....DLMMMMMD....', '.....DLMMMD.....', '.....DLMMMD.....', '......DLMD......',
        '......DMD.......', '.......D........', '................', '................'], dict(D='#6e1414', M='#ff4a4a', L='#ffd8d8'))
    gun = ['................', '...........RR...', '..........RLLR..', '.........SSRRS..', '........SSSSS...', '.......SSDSS....',
           '......SSDSS.....', '.....SKSSS......', '....SKKSS.......', '...KKK.S........', '..KKK...........', '..KK............',
           '................', '................', '................', '................']
    I['growth_ray'] = grid(gun, dict(R='#ff4a4a', L='#ffd8d8', S='#b8bec8', D='#6a707c', K='#3a3f4a'))
    I['shrink_ray'] = grid(gun, dict(R='#ff9a9a', L='#ffffff', S='#8a8f98', D='#4a4f5c', K='#2a2f3a'))
    I['plasma_blaster'] = grid([
        '................', '................', '..........GGGG..', '.........GLLLLG.', '....KKKKKSSSSSS.', '...KSSSSSSDDDDS.',
        '...KSSDDSSSSSSS.', '....KKSSKKKK....', '.....KSK........', '.....KSK........', '....KKK.........', '....KK..........',
        '................', '................', '................', '................'], dict(G='#7dff6a', L='#e0ffd8', S='#5a6a58', D='#2f3a2e', K='#1a1f1a'))
    I['power_cell'] = grid([
        '................', '......KKKK......', '.....KSSSSK.....', '.....KGGGGK.....', '.....KGLLGK.....', '.....KGLLGK.....',
        '.....KGGGGK.....', '.....KGGGGK.....', '.....KGLLGK.....', '.....KGGGGK.....', '.....KGGGGK.....', '.....KSSSSK.....',
        '......KKKK......', '................', '................', '................'], dict(K='#1f2a10', S='#8a9a7a', G='#b6ff3c', L='#f4ffd8'))
    I['overcharged_beacon'] = grid([
        '.......RR.......', '......RLLR......', '.......RR.......', '.......SS.......', '......SGGS......', '.....SGLLGS.....',
        '.....SGLLGS.....', '.....SGGGGS.....', '....SSSSSSSS....', '....SKKKKKKS....', '...SSSSSSSSSS...', '...KKKKKKKKKK...',
        '................', '................', '................', '................'], dict(R='#ff4a4a', L='#ffffff', S='#b8bec8', G='#b6ff3c', K='#3a3f4a'))
    I['gravitic_core'] = grid([
        '................', '.....CCCCCC.....', '....CLLLLLLC....', '...CLWWWWWWLC...', '..CLWCCCCCCWLC..', '..CLWCKKKKCWLC..',
        '..CLWCKLLKCWLC..', '..CLWCKLLKCWLC..', '..CLWCKKKKCWLC..', '..CLWCCCCCCWLC..', '...CLWWWWWWLC...', '....CLLLLLLC....',
        '.....CCCCCC.....', '................', '................', '................'], dict(C='#4fb8c8', L='#9fe8f0', W='#e0fcff', K='#204a58'))
    I['quake_maul'] = grid([
        '................', '..RRRRRR........', '.RDDDDDDR.......', '.RDLLLLDR.......', '.RDDDDDDR.......', '..RRRRRRK.......',
        '.......KSK......', '........KSK.....', '.........KSK....', '..........KSK...', '...........KSK..', '............KK..',
        '................', '................', '................', '................'], dict(R='#ff4a4a', D='#6e1414', L='#ffb0b0', K='#2a1a1a', S='#8a6a5a'))
    for k, v in I.items(): R.ICONS[k] = v
    R.HANDHELD_EXTRA = getattr(R, 'HANDHELD_EXTRA', set()) | {'growth_ray', 'shrink_ray', 'plasma_blaster', 'quake_maul'}
    # --- 3D models
    cube = R.cube
    def c(fr, to, t, rot=None):
        e = cube(fr, to, t)
        if rot: e['rotation'] = rot
        return e
    def ufo(red=False):
        paint = 'crimson' if red else 'green'                     # 2.25: the skiff's riveted plates (vanilla.py)
        tex = {'h': f'bm:block/skiff_{paint}_hull', 'p': f'bm:block/skiff_{paint}_deck', 'g': 'minecraft:block/light_blue_stained_glass' if not red else 'minecraft:block/red_stained_glass',
               'l': 'minecraft:block/verdant_froglight_side' if not red else 'minecraft:block/shroomlight', 'd': 'bm:block/skiff_belly'}
        els = [c((3, 4, 3), (13, 6, 13), 'd'),                                                  # belly
               c((0.5, 6, 3), (15.5, 7.5, 13), 'h'), c((3, 6.03, 0.5), (13, 7.47, 15.5), 'h'),        # the disc (two crossed slabs + a turned one)
               c((1.5, 6.06, 1.5), (14.5, 7.44, 14.5), 'p', {'origin': [8, 6.75, 8], 'axis': 'y', 'angle': 45}),
               c((3.5, 7.5, 3.5), (12.5, 9, 12.5), 'p'),                                          # upper hull
               c((5.5, 9, 5.5), (10.5, 12, 10.5), 'g'),                                           # dome
               c((7, 3, 7), (9, 4, 9), 'l')]                                                       # engine glow
        for (x, z) in ((0.2, 7.5), (15.2, 7.5), (7.5, 0.2), (7.5, 15.2)):
            els.append(c((x, 6.4, z), (x + 0.6, 7.1, z + 0.6), 'l'))
        return tex, els
    R.HATS['ufo3d'] = ufo()
    R.HATS['ufo3d_red'] = ufo(True)
    def board(red=False):
        tex = {'d': 'minecraft:block/verdant_froglight_side' if not red else 'minecraft:block/shroomlight', 'k': 'minecraft:block/gray_concrete'}
        return tex, [c((2.5, 0, 2.5), (13.5, 0.7, 13.5), 'd'), c((5, 0.7, 5), (11, 1.0, 11), 'k'),
                     c((3.5, -0.4, 3.5), (12.5, 0, 12.5), 'k')]
    R.HATS['hoverboard'] = board()
    R.HATS['hoverboard_red'] = board(True)
    # the Vorn: Donado's build with Vorn colours (grey-violet skin, green eyes, black armour), a plasma rifle in hand
    P = R25.donado_parts()
    vt = {'f': 'bm:block/vorn_skin', 'm': 'bm:block/vorn_dark', 'e': 'bm:block/vorn_dark', 'k': 'bm:block/vorn_eye', 't': 'bm:block/vorn_dark',
          's': 'bm:block/vorn_armor', 'p': 'bm:block/vorn_armor', 'g': 'minecraft:block/verdant_froglight_side', 'r': 'minecraft:block/iron_block'}
    body = [e for n in ('legL', 'legR', 'torso', 'armL', 'armR', 'head', 'eyes', 'tail') for e in P[n]]
    ant = [c((6.1, 19, 7.6), (6.7, 23, 8.2), 'm'), c((5.8, 23, 7.3), (7.0, 24.2, 8.5), 'g'),
           c((9.3, 19, 7.6), (9.9, 23, 8.2), 'm'), c((9.0, 23, 7.3), (10.2, 24.2, 8.5), 'g')]
    rifle = [c((11.6, 6.2, 1.5), (12.8, 7.4, 9.0), 'r'), c((11.5, 6.0, 0.4), (12.9, 7.6, 1.6), 'g'), c((11.7, 4.4, 6.5), (12.7, 6.2, 7.5), 'm')]
    R.HATS['vorn3d'] = (vt, body + ant + rifle)
    hammer = [c((11.8, 2.0, 7.9), (12.6, 12.0, 8.7), 'm'), c((10.2, 11.5, 6.3), (14.2, 14.5, 10.3), 'r'), c((10.0, 12.3, 6.1), (14.4, 13.7, 10.5), 'g')]
    R.HATS['vorn3d_warlord'] = (dict(vt, s='bm:block/vorn_armor_red', p='bm:block/vorn_armor_red'), body + ant + hammer)
    # cosmetic: a tiny saucer circling the head (head-slot model, sits above the head)
    th, tel = ufo(True)
    small = []
    for e in tel:
        e2 = dict(e); e2['from'] = [e['from'][0] * 0.55 + 3.6, e['from'][1] * 0.55 + 14.5, e['from'][2] * 0.55 + 3.6]
        e2['to'] = [e['to'][0] * 0.55 + 3.6, e['to'][1] * 0.55 + 14.5, e['to'][2] * 0.55 + 3.6]
        if 'rotation' in e: e2['rotation'] = dict(e['rotation'], origin=[8, e['rotation']['origin'][1] * 0.55 + 14.5, 8])
        small.append(e2)
    R.HATS['vorn_crown'] = (th, small)
    R.HATS['xeno_visor'] = ({'b': 'minecraft:block/black_concrete', 'g': 'minecraft:block/verdant_froglight_side', 'i': 'minecraft:block/iron_block'}, [
        c((3.5, 4.5, 3.4), (12.5, 7.5, 4.4), 'b'), c((4.5, 5.2, 3.2), (7.5, 6.8, 3.5), 'g'), c((8.5, 5.2, 3.2), (11.5, 6.8, 3.5), 'g'),
        c((3.2, 5, 4.4), (4.0, 7, 12.6), 'i'), c((12.0, 5, 4.4), (12.8, 7, 12.6), 'i'), c((3.2, 5, 11.8), (12.8, 7, 12.6), 'i')])
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + ('ufo3d', 'hoverboard', 'vorn3d')


def textures():
    from PIL import Image
    rnd = random.Random(99)
    out = {}
    def tex(base, var=10):
        im = Image.new('RGBA', (16, 16))
        for x in range(16):
            for y in range(16):
                n = rnd.randrange(-var, var + 1)
                im.putpixel((x, y), tuple(max(0, min(255, c_ + n)) for c_ in base) + (255,))
        return im
    out['vorn_skin'] = tex((122, 110, 140), 10)
    out['vorn_dark'] = tex((40, 34, 52), 5)
    eye = tex((60, 255, 80), 18)
    for (x, y) in ((4, 4), (5, 4), (4, 5)): eye.putpixel((x, y), (230, 255, 230, 255))
    out['vorn_eye'] = eye
    arm = tex((34, 36, 40), 6)
    for x in range(16):
        arm.putpixel((x, 7), (90, 255, 110, 255))
    out['vorn_armor'] = arm
    armr = tex((40, 22, 24), 6)
    for x in range(16):
        armr.putpixel((x, 7), (255, 70, 60, 255))
    out['vorn_armor_red'] = armr
    out['adon_muzzle'] = tex((120, 222, 206), 6)
    out['adon_tongue'] = tex((226, 120, 140), 6)
    return out

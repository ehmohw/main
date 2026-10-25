"""2.72: SMELLING SALTS, THE THIEF'S HOURGLASS, THE ALARM JAMMER, MASTERWORKS, THE CODEX, AND EACH TIER'S OWN FINDS.

SMELLING SALTS (Goldtooth, 24 coins)  hold them in either hand: when a blow would knock you out, a whiff brings you round
              instead - no try lost. One use. Goldtooth's own blend: they won't keep outside the vault.
              (how: the salts carry the game's own death-protection - the thing a Totem of Undying does - so the knock-out never
              happens and nothing that counts tries has to change. The one fall the game can't catch, into the Sky Isles' void,
              checks for the salts before it counts you out.)
THE THIEF'S HOURGLASS (Goldtooth, 16 coins)  turn it in a timed room while the clock runs - the Shooting Gallery, the Button
              Dash, the Minecart Run - for 20 seconds more. Once a room.
THE ALARM JAMMER (Goldtooth, 20 coins)  for 30 seconds nothing raises the alarm (the bar turns blue). One at a time.
MASTERWORKS   win a Tier IV or V heist with a kit and that kit's own weapon becomes a Masterwork - from then on it comes out of
              the Armory with a gold name and something extra: the Tank's KOKIRI SWORD (two more Sharpness, Knockback; +4 armour
              and toughness while you hold it), the Offense CAPTAIN'S CUTLASS (two more Sharpness, Fire Aspect; quicker on your
              feet and with your blade), the Ranged FAIRY BOW (two more Power, Flame, Punch; quicker on your feet), the Support
              STAFF OF SPARKS (crewmates within 8 blocks of you take a fifth less harm while you hold it; +4 health).
THE CODEX     a new page in the Ledger's Office: every room you've walked into, every curse you've lifted, every rare find and
              every Masterwork - written down. Fill a section for a one-time reward.
EACH TIER'S OWN FINDS  a won heist's rare, legendary and mythical finds now come half the time from the tier's own three:
              rare (a handy charm for your off hand), legendary (a look of your own) and mythical (something special).
"""
import copy
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int
import phase28 as P28
import phase70 as P70
import phase70_rooms as RM
import phase72 as P72
import phase75 as P75
import phase76_rooms as R6
import phase80 as P80
import phase105 as P105
import phase116 as P116

GOLD = '#ffcf40'
CODEX = '#d8b4ff'
ROMAN = ['', 'I', 'II', 'III', 'IV', 'V']
HOURGLASS_T = 400                              # ticks the Hourglass gives back
JAM_T = 600                                    # ticks the Jammer holds the alarm
C_CODEX, C_SEC = P80.MENU_CODE + 8, 7861       # the Office's Codex button; its sections 7861..7865
holds = lambda iid: f'*[minecraft:custom_data~{{bm:"{iid}"}}]'

# ---------------------------------------------------------------- heist supplies
item('smelling_salts', TOTEM, 'Smelling Salts', '#e8f0ff', ['A corked vial of something eye-watering.', ('Hold them in either hand: when you', 'blue'),
                                                           ('would be knocked out, a whiff brings', 'blue'), ('you round instead - no try lost.', 'blue'),
                                                           ('One use. Goldtooth\'s own blend:', 'gray'), ('they won\'t keep outside the vault.', 'gray')],
     model='bm:smelling_salts', stack=4, cat='misc', custom_extra={'bm_vault': B(1)},
     comps={'minecraft:death_protection': {'death_effects': [{'type': 'minecraft:clear_all_effects'},
                                                              {'type': 'minecraft:apply_effects', 'effects': [
                                                                  {'id': 'minecraft:regeneration', 'amplifier': 1, 'duration': 100},
                                                                  {'id': 'minecraft:resistance', 'amplifier': 2, 'duration': 60},
                                                                  {'id': 'minecraft:nausea', 'amplifier': 0, 'duration': 80}]}]}})
ITEMS['smelling_salts']['comps'].pop('!minecraft:death_protection')
item('thiefs_hourglass', TOTEM, "Thief's Hourglass", '#e0c080', ['Sand that runs slow when you need it to.', ('Use it in a timed room while the clock', 'blue'),
                                                                ('runs: 20 seconds more. Once a room.', 'blue')],
     model='bm:thiefs_hourglass', stack=8, cat='misc', comps=hold('none'))
HOLD['thiefs_hourglass'] = 'bm:p117/hg/use'
item('alarm_jammer', TOTEM, 'Alarm Jammer', '#7ab0ff', ['A box of clockwork that hums at the alarm bells.', ('Use it in a heist: for 30 seconds', 'blue'),
                                                       ('nothing raises the alarm.', 'blue')],
     model='bm:alarm_jammer', stack=8, cat='misc', comps=hold('none'))
HOLD['alarm_jammer'] = 'bm:p117/jam/use'
item('salamander_salve', TOTEM, 'Salamander Salve', '#ff8a3a', ['A tin of ember-red grease that never cools.', ('Use it in a heist: fire and lava', 'blue'),
                                                                ('can\'t hurt you until the heist ends.', 'blue'), ('One heist a tin.', 'gray')],
     model='bm:salamander_salve', stack=8, cat='misc', comps=hold('none'))
HOLD['salamander_salve'] = 'bm:p117/salve/use'
P70.GOLDTOOTH_STOCK += [(24, 'smelling_salts', 1), (16, 'thiefs_hourglass', 1), (20, 'alarm_jammer', 1), (24, 'salamander_salve', 1)]
P72.KEEP += ['thiefs_hourglass', 'alarm_jammer', 'salamander_salve']

# ---------------------------------------------------------------- each tier's own finds: (id, name, colour, lore, kind)
#  kind: ('attr', [modifiers]) an off-hand charm; ('aura', key) a look, in the off hand; ('bell'|'thimble'|'fizzle'|'astro'|'lodestar'|'fletch'|'plume')
RARE, LEGEND, MYTH = P105.RARE_TAG, P105.LEGEND_TAG, P105.MYTH_TAG
def _m(attr, amt, op='add_value'):
    return {'type': f'minecraft:{attr}', 'id': f'bm:tf_{attr}', 'amount': amt, 'operation': op, 'slot': 'offhand'}
TIER_FINDS = {
    1: [('mudlarks_charm', "Mudlark's Charm", '#a08050', ['A pebble with a hole, worn smooth by the sewers.', ('In your off hand: mud, soul sand, honey', 'blue'),
                                                                                                         ('and snow can\'t slow you down.', 'blue')], ('attr', [_m('movement_efficiency', 1.0)])),
        ('songbird', 'Wind-Up Songbird', '#e0b060', ['A tin bird with a key in its back.', ('In your off hand: it whistles, and', 'blue'), ('music notes dance about your head.', 'blue')], ('aura', 'notes')),
        ('merchants_bell', "Merchant's Bell", '#e8c870', ['The bell from a market-master\'s stall.', ('Ring it near villagers: every one', 'blue'),
                                                         ('within 10 blocks restocks its wares.', 'blue'), ('Once a day.', 'gray')], ('bell',))],
    2: [('smugglers_veil', "Smuggler's Veil", '#5a5a7a', ['Grey gauze that the eye slides off.', ('In your off hand: you vanish from', 'blue'), ('other players\' locator bars.', 'blue')],
         ('attr', [_m('waypoint_transmit_range', -1.0, 'add_multiplied_total')])),
        ('firefly_jar', 'Firefly Jar', '#d8f080', ['A jar of lights, holes punched in the lid.', ('In your off hand: fireflies drift', 'blue'), ('and blink about you.', 'blue')], ('aura', 'firefly')),
        ('tinkers_thimble', "Tinker's Thimble", '#c8c8d0', ['A silver thimble that hums when it touches iron.', ('Carry it: whatever you wear and hold', 'blue'),
                                                         ('slowly mends itself.', 'blue')], ('thimble',))],
    3: [('duelists_ribbon', "Duelist's Ribbon", '#d04060', ['Tied round the hilt for luck.', ('In your off hand: your sword\'s sweep', 'blue'),
                                                           ('strikes as hard as the blow itself.', 'blue')], ('attr', [_m('sweeping_damage_ratio', 1.0)])),
        ('honeycomb_brooch', 'Honeycomb Brooch', '#ffb030', ['Wax and gold, still sticky.', ('In your off hand: honey drips', 'blue'), ('from your shoulders.', 'blue')], ('aura', 'honey')),
        ('fizzle_stone', 'Fizzle Stone', '#7ad070', ['A damp grey pebble that smells of wet powder.', ('Carry it: creepers within 12 blocks', 'blue'),
                                                    ('of you fizzle out harmlessly.', 'blue')], ('fizzle',))],
    4: [('navigators_astrolabe', "Navigator's Astrolabe", '#c09040', ['Brass rings that always know where they are.', ('In your off hand: where you stand, which', 'blue'),
                                                                     ('way you face and the time of day,', 'blue'), ('above your hotbar.', 'blue')], ('astro',)),
        ('trial_key_fob', 'Trial Key Fob', '#80c0d0', ['A key ring from a sealed trial vault.', ('In your off hand: streams of light', 'blue'), ('spiral in towards you.', 'blue')], ('aura', 'trial')),
        ('wayfarers_lodestar', "Wayfarer's Lodestar", '#ffe890', ['A star in a brass cage that always points home.', ('Sneak and use: it remembers this spot.', 'blue'),
                                                                  ('Use: back to it (in the same world;', 'blue'), ('once every 5 minutes).', 'blue')], ('lodestar',))],
    5: [('fletchers_charm', "Fletcher's Charm", '#a0b070', ['Three goose feathers bound with gold wire.', ('In your off hand: your arrows fly', 'blue'),
                                                           ('half again as fast - and hit harder.', 'blue')], ('fletch',)),
        ('gale_locket', 'Gale Locket', '#c0e0f0', ['A locket with a breeze shut inside.', ('In your off hand: little gusts', 'blue'), ('whirl about your feet.', 'blue')], ('aura', 'gale')),
        ('phoenix_plume', 'Phoenix Plume', '#ff6a30', ['It smoulders, and never burns away.', ('Hold it in either hand: it saves you', 'blue'),
                                                      ('from death - then smoulders for', 'blue'), ('10 minutes before it can again.', 'blue')], ('plume',))]}
PLUME_CD = 600
for _t, _row in TIER_FINDS.items():
    for _j, (_iid, _nm, _col, _lore, _kind) in enumerate(_row):
        _tag = (RARE, LEGEND, MYTH)[_j]
        _c = {}
        if _kind[0] == 'attr': _c['minecraft:attribute_modifiers'] = _kind[1]
        if _kind[0] in ('lodestar', 'bell'): _c = hold('none')
        if _kind[0] == 'plume':
            _c['minecraft:death_protection'] = {'death_effects': [{'type': 'minecraft:clear_all_effects'}, {'type': 'minecraft:apply_effects', 'effects': [
                {'id': 'minecraft:regeneration', 'amplifier': 1, 'duration': 200}, {'id': 'minecraft:fire_resistance', 'amplifier': 0, 'duration': 400},
                {'id': 'minecraft:absorption', 'amplifier': 1, 'duration': 200}]}]}
        item(_iid, TOTEM, _nm, _col, _lore + [(f'{_tag[0]} - Tier {ROMAN[_t]}', _tag[1])], model=f'bm:{_iid}', stack=1, cat='relic', comps=_c, glint=_j == 2 or None)
        if _kind[0] == 'plume': ITEMS[_iid]['comps'].pop('!minecraft:death_protection')
HOLD['wayfarers_lodestar'] = 'bm:p117/star/use'
HOLD['merchants_bell'] = 'bm:p117/bell/use'
item('phoenix_ash', TOTEM, 'Smouldering Plume', '#a05030', ['A Phoenix Plume, burnt down to the quill.', ('It blazes back to life 10 minutes', 'blue'),
                                                           ('after it saved you - carry it.', 'blue'), (f'{MYTH[0]} - Tier V', MYTH[1])],
     model='bm:phoenix_ash', stack=1, cat='relic')

# ---------------------------------------------------------------- masterworks: the kits' own weapons, made better
MW = {1: ('kokiri_sword', 'Kokiri Sword', 'Tank', {'minecraft:sharpness': 2, 'minecraft:knockback': 1},
          [('armor', 4.0, 'add_value'), ('armor_toughness', 2.0, 'add_value')], '+4 armour and toughness while you hold it'),
      2: ('pirate_cutlass', "Captain's Cutlass", 'Offense', {'minecraft:sharpness': 2, 'minecraft:fire_aspect': 1},
          [('movement_speed', 0.15, 'add_multiplied_base'), ('attack_speed', 0.15, 'add_multiplied_base')], 'quicker on your feet and with your blade'),
      3: ('fairy_bow', 'Fairy Bow', 'Ranged', {'minecraft:power': 2, 'minecraft:flame': 1, 'minecraft:punch': 1},
          [('movement_speed', 0.12, 'add_multiplied_base')], 'quicker on your feet while you hold it'),
      4: ('staff_of_sparks', 'Staff of Sparks', 'Support', {},
          [('max_health', 4.0, 'add_value')], 'your crew near you take a fifth less harm; +4 health')}


def generate(G):
    fn, title, tellraw, wjson = G.fn, G.title, G.tellraw, G.wjson
    P = [T('[', 'dark_gray'), T('Heist', GOLD, bold=True), T('] ', 'dark_gray')]
    say = lambda txt, col='gray': tellraw('@s', P + [T(txt, col)])
    clear1 = lambda i: f'execute unless entity @s[gamemode=creative] run clear @s {holds(i)} 1'
    HA, HB = '-200 64 -197', '-198 64 -197'
    def ins(table):
        return [f'execute in bm:gutter unless data block {HA} Items[26] run loot insert {HA} loot {table}',
                f'execute in bm:gutter if data block {HA} Items[26] run loot insert {HB} loot {table}']
    objs = ['bm.gvjam', 'bm.mbd', 'bm.wlx', 'bm.wly', 'bm.wlz', 'bm.wld', 'bm.wlc', 'bm.phx'] + [f'bm.mw{r}' for r in MW] + [f'bm.cxr{s}' for s in range(1, 6)]
    tick, fast, second = [], [], []

    # ================================================================== SMELLING SALTS
    # (the knock-out never happens - the game's own death protection; so a try is never lost. Spent: a word for the crew)
    wjson('bm/advancement/p117/salts.json', {'criteria': {'used': {'trigger': 'minecraft:used_totem', 'conditions': {
        'item': {'items': TOTEM, 'predicates': {'minecraft:custom_data': '{bm:"smelling_salts"}'}}}}}, 'rewards': {'function': 'bm:p117/salts/used'}})
    fn('p117/salts/used', ['advancement revoke @s only bm:p117/salts',
                           'execute at @s run particle minecraft:cloud ~ ~1.6 ~ 0.3 0.2 0.3 0.02 20', 'execute at @s run playsound minecraft:entity.player.breath player @a[distance=..16] ~ ~ ~ 1 1.4',
                           title('@s', 'actionbar', [T('A whiff of salts - ', '#e8f0ff', bold=True), T('you come round! No try lost.', 'gray')]),
                           'execute if entity @s[tag=bm.gvp] run ' + tellraw('@a[tag=bm.gvp,distance=..40]', P + [{'selector': '@s', 'color': 'white'},
                                                                                                                   T(' went down - and the smelling salts brought them round.', 'gray')])])
    # (the void can't be caught by death protection: it checks for the salts itself)
    vk = G.FUNCS['p112/void_ko']
    vk.insert(0, 'execute if function bm:p117/salts/void run return 0')
    fn('p117/salts/void', ['execute unless items entity @s weapon.mainhand ' + holds('smelling_salts') + ' unless items entity @s weapon.offhand ' + holds('smelling_salts') + ' run return fail',
                           'execute if items entity @s weapon.mainhand ' + holds('smelling_salts') + ' run item modify entity @s weapon.mainhand bm:p117/less1',
                           'execute unless items entity @s weapon.mainhand ' + holds('smelling_salts') + ' if items entity @s weapon.offhand ' + holds('smelling_salts') + ' run item modify entity @s weapon.offhand bm:p117/less1',
                           'execute at @e[type=minecraft:marker,tag=bm.gvr,distance=..40,sort=nearest,limit=1] run tp @s ' + RM.rel(2, 4, 12) + ' -90 0',
                           'effect give @s minecraft:resistance 3 4 true', 'effect give @s minecraft:nausea 4 0 true',
                           'execute at @s run particle minecraft:cloud ~ ~1.6 ~ 0.3 0.2 0.3 0.02 20',
                           title('@s', 'actionbar', [T('A whiff of salts - ', '#e8f0ff', bold=True), T('you come round at the door! No try lost.', 'gray')]), 'return 1'])
    wjson('bm/item_modifier/p117/less1.json', {'function': 'minecraft:set_count', 'count': -1, 'add': True})

    # ================================================================== THE THIEF'S HOURGLASS
    fn('p117/hg/use', ['execute unless entity @s[tag=bm.gvp] run return run ' + say('Save it for a heist - for a room against the clock.'),
                       'scoreboard players set #hg bm.rng 0',
                       'execute as @e[type=minecraft:marker,tag=bm.gvr,distance=..26,sort=nearest,limit=1] run function bm:p117/hg/room',
                       'execute if score #hg bm.rng matches 0 run return run ' + say('No clock is running here - the sand stays put.'),
                       'execute if score #hg bm.rng matches 2 run return run ' + say('This room\'s clock has been turned once already.'),
                       clear1('thiefs_hourglass'), 'execute at @s run particle minecraft:falling_dust{block_state:"minecraft:sand"} ~ ~1.8 ~ 0.4 0.2 0.4 0 20',
                       'execute at @s run playsound minecraft:block.sand.fall player @a[distance=..24] ~ ~ ~ 1 0.6',
                       tellraw('@a[tag=bm.gvp,distance=..30]', P + [{'selector': '@s', 'color': 'white'}, T(' turns the hourglass: ', 'gray'), T('20 seconds more!', '#e0c080', bold=True)])])
    fn('p117/hg/room', ['execute unless entity @s[tag=bm.gvr_gallery] unless entity @s[tag=bm.gvr_dash] unless entity @s[tag=bm.gvr_minecart] run return 0',
                        'execute if entity @s[tag=bm.gvr_minecart] unless score @s bm.gvs matches 2 run return 0',
                        'execute unless entity @s[tag=bm.gvr_minecart] unless score @s bm.gvs matches 1 run return 0',
                        'execute if entity @s[tag=bm.gvhg] run return run scoreboard players set #hg bm.rng 2',
                        'tag @s add bm.gvhg', 'scoreboard players set #hg bm.rng 1',
                        f'execute if entity @s[tag=bm.gvr_minecart] run scoreboard players remove @s bm.gvy3 {HOURGLASS_T}',
                        f'execute unless entity @s[tag=bm.gvr_minecart] run scoreboard players add @s bm.gvz {HOURGLASS_T}'])

    # ================================================================== THE SALAMANDER SALVE (2.82t): fire immunity for one heist
    fn('p117/salve/use', ['execute unless entity @s[tag=bm.gvp] run return run ' + say('Save it for a heist.'),
                          'execute if entity @s[tag=bm.gvfire] run return run ' + say('The salve is still on you - it lasts the whole heist.'),
                          clear1('salamander_salve'), 'tag @s add bm.gvfire', 'effect give @s minecraft:fire_resistance infinite 0 true',
                          'execute at @s run particle minecraft:flame ~ ~1 ~ 0.4 0.6 0.4 0.02 30',
                          'execute at @s run playsound minecraft:item.firecharge.use player @a[distance=..16] ~ ~ ~ 0.8 1.4',
                          say('Salamander Salve: fire and lava can\'t touch you until this heist ends.', '#ff8a3a')])
    fn('p117/salve/off', ['execute unless entity @s[tag=bm.gvfire] run return 0', 'tag @s remove bm.gvfire', 'effect clear @s minecraft:fire_resistance'])
    second += ['effect give @a[tag=bm.gvfire] minecraft:fire_resistance infinite 0 true']     # (back on after a knock-out, which clears effects)
    for end in ('p70/haul', 'p101/after_fail', 'p70/unraid'):     # won, lost, or left: the heist is over
        G.FUNCS[end].append('function bm:p117/salve/off')

    # ================================================================== THE ALARM JAMMER
    G.FUNCS['p70/alarm'].insert(0, 'execute if score @s bm.gvjam matches 1.. run return run function bm:p117/jam/hush')
    fn('p117/jam/hush', ['function bm:p70/tag_mine', 'execute as @a[tag=bm.gvme] at @s run playsound minecraft:block.note_block.didgeridoo player @s ~ ~ ~ 0.5 1.6',
                         title('@a[tag=bm.gvme]', 'actionbar', [T('The jammer swallows the alarm.', '#7ab0ff')]), 'tag @a[tag=bm.gvme] remove bm.gvme'])
    fn('p117/jam/use', ['execute unless entity @s[tag=bm.gvp] run return run ' + say('Save it for a heist.'),
                        'scoreboard players operation #gi bm.rng = @s bm.gvi', 'scoreboard players set #hg bm.rng 0',
                        'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run function bm:p117/jam/inst',
                        'execute if score #hg bm.rng matches 2 run return run ' + say('A jammer is already humming.'),
                        'execute if score #hg bm.rng matches 0 run return 0', clear1('alarm_jammer'),
                        'execute at @s run playsound minecraft:block.beacon.activate player @a[distance=..24] ~ ~ ~ 1 1.6',
                        tellraw('@a[tag=bm.gvp,distance=..300]', P + [{'selector': '@s', 'color': 'white'}, T(' switches on a jammer: ', 'gray'), T('30 seconds of quiet.', '#7ab0ff', bold=True)])])
    fn('p117/jam/inst', ['execute if score @s bm.gvjam matches 1.. run return run scoreboard players set #hg bm.rng 2', 'scoreboard players set #hg bm.rng 1',
                         f'scoreboard players set @s bm.gvjam {JAM_T}'] +
       [f'execute if score @s bm.gvi matches {s + 1} run bossbar set bm:gva{s} color blue' for s in range(P70.SLOTS)] +
       [f'execute if score @s bm.gvi matches {s + 1} run bossbar set bm:gva{s} name {snbt(T("Alarm - jammed", "#7ab0ff"))}' for s in range(P70.SLOTS)])
    tick += ['execute as @e[type=minecraft:marker,tag=bm.gvinst,scores={bm.gvjam=1}] run function bm:p117/jam/off',
             'scoreboard players remove @e[type=minecraft:marker,tag=bm.gvinst,scores={bm.gvjam=1..}] bm.gvjam 1']
    fn('p117/jam/off', [f'execute if score @s bm.gvi matches {s + 1} run bossbar set bm:gva{s} color red' for s in range(P70.SLOTS)] +
       [f'execute if score @s bm.gvi matches {s + 1} run bossbar set bm:gva{s} name {snbt(T("Alarm", "red"))}' for s in range(P70.SLOTS)] +
       ['function bm:p70/tag_mine', title('@a[tag=bm.gvme]', 'actionbar', [T('The jammer splutters out.', '#7ab0ff')]), 'tag @a[tag=bm.gvme] remove bm.gvme'])
    G.FUNCS['p70/inst_init'].append('scoreboard players set @s bm.gvjam 0')

    # ================================================================== MASTERWORKS
    for r, (iid, nm, role, ench, attrs, what) in MW.items():
        mods = [{'function': 'minecraft:set_name', 'target': 'item_name', 'name': [T('✦ ', GOLD), T(f'{nm} · Masterwork', GOLD, bold=True), T(' ✦', GOLD)]},
                {'function': 'minecraft:set_lore', 'mode': 'append', 'lore': [T('✦ MASTERWORK ✦', GOLD, bold=True), T(f'Won at Tier IV+ with the {role} kit:', 'gray'), T(what + '.', 'blue')]},
                {'function': 'minecraft:set_custom_data', 'tag': '{bm_mw:1b}'},
                {'function': 'minecraft:set_components', 'components': {'minecraft:enchantment_glint_override': True}}]
        if ench: mods.append({'function': 'minecraft:set_enchantments', 'enchantments': ench, 'add': True})
        mods.append({'function': 'minecraft:set_attributes', 'replace': False,
                     'modifiers': [{'attribute': f'minecraft:{a}', 'id': f'bm:mw{r}_{a}', 'amount': v, 'operation': op, 'slot': 'mainhand'} for a, v, op in attrs]})
        wjson(f'bm/item_modifier/p117/mw{r}.json', mods)
        slots = [f'hotbar.{i}' for i in range(9)] + [f'inventory.{i}' for i in range(27)] + ['weapon.offhand']
        fn(f'p117/mw/forge{r}', [f'execute if items entity @s {sl} *[minecraft:custom_data~{{bm:"{iid}",bm_kit:1b}}] unless items entity @s {sl} *[minecraft:custom_data~{{bm_mw:1b}}] '
                                 f'run return run item modify entity @s {sl} bm:p117/mw{r}' for sl in slots])
        for n in range(1, 7):
            L = G.FUNCS[f'p80/kit/give_{r}_{n}']
            k = L.index('function bm:p80/kit/extras')
            L.insert(k, f'execute if score @s bm.mw{r} matches 1 run function bm:p117/mw/forge{r}')
        fn(f'p117/mw/new{r}', [f'scoreboard players set @s bm.mw{r} 1',
                               tellraw('@a', P + [{'selector': '@s', 'color': 'white'}, T(' has earned a Masterwork: ', 'gray'), T(f'the {nm}', GOLD, bold=True),
                                                  T(f' ({role} kit) - it comes out of the Armory gilded from now on.', 'gray')]),
                               'playsound minecraft:block.anvil.use player @s ~ ~ ~ 1 0.8', 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1.2',
                               f'function bm:p117/cx/m{r}'])
    fn('p117/mw/earn', [f'execute if score @s bm.gvrole matches {r} unless score @s bm.mw{r} matches 1 run function bm:p117/mw/new{r}' for r in MW])
    G.FUNCS['p70/haul'].append('execute if score #gt bm.rng matches 4.. run function bm:p117/mw/earn')
    second.append('execute as @a[tag=bm.gvp] if items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"staff_of_sparks",bm_mw:1b}] at @s run '
                  'effect give @a[tag=bm.gvp,distance=..8] minecraft:resistance 2 0 true')
    fn('admin/masterworks_all', [f'scoreboard players set @s bm.mw{r} 1' for r in MW] + [say('All four Masterworks are yours (from your next kit).')])
    fn('admin/masterworks_reset', [f'scoreboard players reset @s bm.mw{r}' for r in MW] + [say('Masterworks forgotten.')])

    # ================================================================== EACH TIER'S OWN FINDS
    for j, kind in enumerate(('rare', 'legend', 'myth')):
        f_ = G.FUNCS[f'p105/find_{kind}']
        glob = {'rare': 'forgeheart', 'legend': 'the_alibi', 'myth': 'counterfeiters_press'}[kind]
        f_[0:0] = ['execute store result score #fz bm.rng run random value 0..1', f'execute if score #fz bm.rng matches 1 run return run function bm:p117/find/{kind}',
                   f'function bm:p117/cx/f_{glob}']
        fn(f'p117/find/{kind}', [f'execute if score #gt bm.rng matches {t} run return run function bm:p117/find/{kind}{t}' for t in TIER_FINDS])
        tag = (RARE, LEGEND, MYTH)[j]
        for t, row in TIER_FINDS.items():
            iid, nm, col, _l, _k = row[j]
            who = '@s' if j == 0 else '@a'
            line = P + ([T('Rare find! ', tag[1], bold=True), T('A ', 'gray')] if j == 0 else
                        [{'selector': '@s', 'color': 'white'}, T(f' found a {"legendary" if j == 1 else "mythical"} ', 'gray')]) + \
                [T(nm, col, bold=True), T(f' - Tier {ROMAN[t]}\'s own - in ' + ('your haul.' if j == 0 else 'a won heist!'), 'gray')]
            fn(f'p117/find/{kind}{t}', ins(f'bm:items/{iid}') + [tellraw(who, line), f'function bm:p117/cx/f_{iid}',
                                                                 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 ' + ('1.0' if j == 0 else '1.3')])
    # the charms' off-hand modifiers need nothing more; the rest:
    aura = {'notes': ['particle minecraft:note ~ ~2.15 ~ 0.45 0.15 0.45 1 1'],
            'firefly': ['particle minecraft:firefly ~ ~1.1 ~ 0.9 0.6 0.9 0 1'],
            'honey': ['particle minecraft:dripping_honey ~ ~1.45 ~ 0.3 0.05 0.3 0 1'],
            'trial': ['particle minecraft:vault_connection ~ ~1 ~ 0.7 0.6 0.7 0.15 2'],
            'gale': ['particle minecraft:small_gust ~ ~0.15 ~ 0.6 0 0.6 0 1']}
    for t, row in TIER_FINDS.items():
        for iid, nm, col, _l, kind in row:
            if kind[0] == 'aura':
                fast.append(f'execute as @a[gamemode=!spectator] if items entity @s weapon.offhand {holds(iid)} at @s rotated ~ 0 run function bm:p117/aura/{kind[1]}')
                fn(f'p117/aura/{kind[1]}', aura[kind[1]])
    # (the Merchant's Bell: the villagers near you restock - natural villagers only, never the market's own traders; once a game day)
    fn('p117/bell/use', ['scoreboard players operation #day bm.rng = #day bm.bm',
                         'execute if score @s bm.mbd = #day bm.rng run return run ' + say('The bell needs a day\'s rest before it rings again.'),
                         'scoreboard players set #nv bm.rng 0', 'execute as @e[type=minecraft:villager,distance=..10] unless data entity @s Tags run scoreboard players add #nv bm.rng 1',
                         'execute if score #nv bm.rng matches 0 run return run ' + say('No villager near enough to hear it.'),
                         'scoreboard players operation @s bm.mbd = #day bm.rng',
                         'execute as @e[type=minecraft:villager,distance=..10] unless data entity @s Tags run data modify entity @s Offers.Recipes[].uses set value 0',
                         'execute as @e[type=minecraft:villager,distance=..10] unless data entity @s Tags at @s run particle minecraft:happy_villager ~ ~2.2 ~ 0.3 0.2 0.3 0 5',
                         'playsound minecraft:block.bell.use player @a[distance=..16] ~ ~ ~ 1 1.4',
                         tellraw('@s', P + [T('Ding! ', '#e8c870', bold=True), {'score': {'name': '#nv', 'objective': 'bm.rng'}, 'color': 'white'}, T(' villager(s) restock their wares.', 'gray')])])
    # (the Tinker's Thimble: every 10 seconds, 3% back on whatever's worn or held and worn down)
    second += ['scoreboard players add #thm bm.rng 1', 'execute if score #thm bm.rng matches 10.. run function bm:p117/thimble/all']
    fn('p117/thimble/all', ['scoreboard players set #thm bm.rng 0', f'execute as @a if items entity @s container.* {holds("tinkers_thimble")} run function bm:p117/thimble/me',
                            f'execute as @a unless items entity @s container.* {holds("tinkers_thimble")} if items entity @s weapon.offhand {holds("tinkers_thimble")} run function bm:p117/thimble/me'])
    fn('p117/thimble/me', [f'execute if items entity @s {sl} *[minecraft:damage~{{damage:{{min:1}}}}] run item modify entity @s {sl} bm:p117/mend'
                           for sl in ('weapon.mainhand', 'weapon.offhand', 'armor.head', 'armor.chest', 'armor.legs', 'armor.feet')])
    wjson('bm/item_modifier/p117/mend.json', {'function': 'minecraft:set_damage', 'damage': 0.03, 'add': True})
    # (the Fizzle Stone: the creepers near you lose their bang)
    fast.append(f'execute as @a[gamemode=!spectator] if items entity @s container.* {holds("fizzle_stone")} at @s run function bm:p117/fizzle/near')
    fast.append(f'execute as @a[gamemode=!spectator] unless items entity @s container.* {holds("fizzle_stone")} if items entity @s weapon.offhand {holds("fizzle_stone")} at @s run function bm:p117/fizzle/near')
    fn('p117/fizzle/near', ['execute as @e[type=minecraft:creeper,distance=..12,tag=!bm.fizz] at @s run function bm:p117/fizzle/one'])
    fn('p117/fizzle/one', ['tag @s add bm.fizz', 'data merge entity @s {ExplosionRadius:0b}', 'particle minecraft:smoke ~ ~1.2 ~ 0.2 0.3 0.2 0.01 6'])
    # (the Navigator's Astrolabe: where you are, which way you face, the time - above the hotbar)
    fast.append(f'execute as @a[gamemode=!spectator] if items entity @s weapon.offhand {holds("navigators_astrolabe")} run function bm:p117/astro/show')
    DIRS = [('South', -22, 22), ('South-West', 23, 67), ('West', 68, 112), ('North-West', 113, 157), ('North', 158, 180), ('North', -180, -158),
            ('North-East', -157, -113), ('East', -112, -68), ('South-East', -67, -23)]
    sc = lambda n: {'score': {'name': n, 'objective': 'bm.rng'}, 'color': 'white'}
    fn('p117/astro/show', ['execute store result score #ax bm.rng run data get entity @s Pos[0]', 'execute store result score #ay bm.rng run data get entity @s Pos[1]',
                           'execute store result score #az bm.rng run data get entity @s Pos[2]', 'execute store result score #ar bm.rng run data get entity @s Rotation[0]',
                           'scoreboard players operation #td bm.rng = #tod bm.bm', 'scoreboard players operation #hh bm.rng = #td bm.rng',
                           'scoreboard players operation #hh bm.rng /= #k1000 bm.rng', 'scoreboard players add #hh bm.rng 6', 'scoreboard players operation #hh bm.rng %= #24 bm.rng',
                           'scoreboard players operation #mm bm.rng = #td bm.rng', 'scoreboard players operation #mm bm.rng %= #k1000 bm.rng',
                           'scoreboard players operation #mm bm.rng *= #60 bm.rng', 'scoreboard players operation #mm bm.rng /= #k1000 bm.rng',
                           'scoreboard players operation #mt bm.rng = #mm bm.rng', 'scoreboard players operation #mt bm.rng /= #10 bm.rng',
                           'scoreboard players operation #mo bm.rng = #mm bm.rng', 'scoreboard players operation #mo bm.rng %= #10 bm.rng'] +
       [f'execute if score #ar bm.rng matches {lo}..{hi} run ' + title('@s', 'actionbar', [T('⌖ ', '#c09040'), sc('#ax'), T('  ', 'gray'), sc('#ay'), T('  ', 'gray'), sc('#az'),
                                                                                          T('   ⇧ ', '#c09040'), T(nm_, 'white'), T('   ☀ ', '#c09040'), sc('#hh'), T(':', 'white'), sc('#mt'), sc('#mo')])
        for nm_, lo, hi in DIRS])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #k1000 bm.rng 1000', 'scoreboard players set #24 bm.rng 24', 'scoreboard players set #60 bm.rng 60', 'scoreboard players set #10 bm.rng 10']
    # (the Fletcher's Charm: each new arrow from someone holding it flies half again as fast)
    tick.append('execute as @e[type=#minecraft:arrows,tag=!bm.flc] run function bm:p117/fletch/arrow')
    fn('p117/fletch/arrow', ['tag @s add bm.flc', 'execute unless function bm:p117/fletch/owner run return 0'] +
       [f'execute store result entity @s Motion[{i}] double 0.00015 run data get entity @s Motion[{i}] 10000' for i in range(3)])
    fn('p117/fletch/owner', [f'execute on origin if items entity @s weapon.offhand {holds("fletchers_charm")} run return 1', 'return fail'])
    # (the Wayfarer's Lodestar: sneak - mark; use - back to the mark; same world; 5-minute rest)
    dims = [('minecraft:overworld', 1), ('minecraft:the_nether', 2), ('minecraft:the_end', 3)]
    fn('p117/star/use', ['scoreboard players set #wd bm.rng 0'] + [f'execute if dimension {d} run scoreboard players set #wd bm.rng {v}' for d, v in dims] +
       ['execute if score #wd bm.rng matches 0 run return run ' + say('The Lodestar can\'t see the stars down here.'),
        'execute if predicate bm:p20/sneaking run return run function bm:p117/star/mark',
        'execute unless score @s bm.wld matches 1.. run return run ' + say('Sneak and use it first, to mark a spot.'),
        'execute unless score @s bm.wld = #wd bm.rng run return run ' + say('Your mark is in another world.'),
        'execute if score @s bm.wlc matches 1.. run return run function bm:p117/star/rest',
        f'scoreboard players set @s bm.wlc {300}',
        'execute store result storage bm:gv wl.x double 0.1 run scoreboard players get @s bm.wlx', 'execute store result storage bm:gv wl.y double 0.1 run scoreboard players get @s bm.wly',
        'execute store result storage bm:gv wl.z double 0.1 run scoreboard players get @s bm.wlz',
        'execute at @s run particle minecraft:end_rod ~ ~1 ~ 0.3 0.6 0.3 0.05 30', 'function bm:p117/star/go with storage bm:gv wl',
        'execute at @s run particle minecraft:end_rod ~ ~1 ~ 0.3 0.6 0.3 0.05 30', 'execute at @s run playsound minecraft:block.amethyst_block.resonate player @a[distance=..16] ~ ~ ~ 1 1.4'])
    fn('p117/star/go', ['$tp @s $(x) $(y) $(z)'])
    fn('p117/star/mark', ['scoreboard players operation @s bm.wld = #wd bm.rng', 'execute store result score @s bm.wlx run data get entity @s Pos[0] 10',
                          'execute store result score @s bm.wly run data get entity @s Pos[1] 10', 'execute store result score @s bm.wlz run data get entity @s Pos[2] 10',
                          'execute at @s run particle minecraft:wax_on ~ ~0.2 ~ 0.4 0 0.4 0 12', say('The Lodestar will remember this spot.', '#ffe890')])
    fn('p117/star/rest', ['scoreboard players operation #s bm.rng = @s bm.wlc',
                          tellraw('@s', P + [T('The Lodestar is still finding its bearings: ', 'gray'), {'score': {'name': '#s', 'objective': 'bm.rng'}, 'color': 'white'}, T(' s.', 'gray')])])
    second.append('scoreboard players remove @a[scores={bm.wlc=1..}] bm.wlc 1')
    # (the Phoenix Plume: it saves you, burns to a quill, and blazes back 10 minutes on)
    wjson('bm/advancement/p117/plume.json', {'criteria': {'used': {'trigger': 'minecraft:used_totem', 'conditions': {
        'item': {'items': TOTEM, 'predicates': {'minecraft:custom_data': '{bm:"phoenix_plume"}'}}}}}, 'rewards': {'function': 'bm:p117/plume/used'}})
    fn('p117/plume/used', ['advancement revoke @s only bm:p117/plume', G.give('phoenix_ash'), f'scoreboard players set @s bm.phx {PLUME_CD}',
                           'execute at @s run particle minecraft:flame ~ ~1 ~ 0.4 0.8 0.4 0.08 60', 'execute at @s run playsound minecraft:entity.blaze.shoot player @a[distance=..16] ~ ~ ~ 1 0.7',
                           title('@s', 'actionbar', [T('The Phoenix Plume ', '#ff6a30', bold=True), T('burns down to the quill - and you live.', 'gray')])])
    second += ['scoreboard players remove @a[scores={bm.phx=1..}] bm.phx 1',
               f'execute as @a unless score @s bm.phx matches 1.. if items entity @s container.* {holds("phoenix_ash")} at @s run function bm:p117/plume/back']
    fn('p117/plume/back', ['clear @s ' + holds('phoenix_ash') + ' 1', G.give('phoenix_plume'), 'scoreboard players reset @s bm.phx',
                           'execute at @s run playsound minecraft:item.firecharge.use player @s ~ ~ ~ 1 1.2', say('Your Phoenix Plume blazes back to life.', '#ff6a30')])
    allf = [r[0] for row in TIER_FINDS.values() for r in row]
    fn('admin/tier_finds', [G.give(i) for i in allf] + [G.give(i) for i in ('smelling_salts', 'thiefs_hourglass', 'alarm_jammer')])

    # ================================================================== THE CODEX
    names = {**RM.NAMES, **R6.NAMES}
    rooms = list(P75.KINDS)
    pool = []
    for t in range(1, 6):
        for k in P75.EVENT_POOL[t]:
            if k not in pool: pool.append(k)
    events = pool + [k for k in ('throne', 'fork', 'minecart', 'cache') if k not in pool]
    finds = ['forgeheart', 'the_alibi', 'counterfeiters_press'] + allf
    SECS = {1: ('Rooms of the Vault', [(f'r_{k}', names.get(k, k.title())) for k in rooms], ('token', 4, '4 Black Market Tokens')),
            2: ('Events and Secrets', [(f'r_{k}', names.get(k, k.title())) for k in events], ('token', 4, '4 Black Market Tokens')),
            3: ('Curses Lifted', [(f'c{c}', nm.title()) for c, (nm, _w) in P116.CURSES.items()], ('medallion', 1, 'a Black Market Medallion')),
            4: ('Rare Finds', [(f'f_{i}', ITEMS[i]['name']) for i in finds], ('trophy', 1, 'a Black Market Trophy')),
            5: ('Masterworks', [(f'm{r}', f'{MW[r][1]} ({MW[r][2]})') for r in MW], ('medallion', 1, 'a Black Market Medallion'))}
    SECTION_OF = {}
    for s, (snm, ents, rw) in SECS.items():
        for key, enm in ents:
            SECTION_OF[key] = (s, enm)
            objs.append(f'bm.cx_{key}')
    # (a new entry: written down, counted, and a full section paid once)
    for key, (s, enm) in SECTION_OF.items():
        snm, ents, rw = SECS[s]
        fn(f'p117/cx/{key}', [f'execute if score @s bm.cx_{key} matches 1 run return 0', f'scoreboard players set @s bm.cx_{key} 1', f'function bm:p117/cx/count{s}',
                              tellraw('@s', [T('📖 ', CODEX), T('New in your Codex: ', 'gray'), T(enm, 'white', bold=True), T(f'  ({snm} ', 'dark_gray'),
                                             {'score': {'name': '#cxn', 'objective': 'bm.rng'}, 'color': 'dark_gray'}, T(f'/{len(ents)})', 'dark_gray')]),
                              f'execute if score #cxn bm.rng matches {len(ents)} unless score @s bm.cxr{s} matches 1 run function bm:p117/cx/reward{s}'])
    for s, (snm, ents, (rid, rn, rtxt)) in SECS.items():
        fn(f'p117/cx/count{s}', ['scoreboard players set #cxn bm.rng 0'] + [f'execute if score @s bm.cx_{key} matches 1 run scoreboard players add #cxn bm.rng 1' for key, _n in ents])
        fn(f'p117/cx/reward{s}', [f'scoreboard players set @s bm.cxr{s} 1', G.give(rid, rn), 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 0.9',
                                  tellraw('@a', [T('📖 ', CODEX), {'selector': '@s', 'color': 'white'}, T(' has filled the Codex\'s ', 'gray'), T(snm, CODEX, bold=True),
                                                 T(f' - {rtxt}.', 'gray')])])
    # rooms: written down the first time any of the crew comes within 12 blocks (the den, the vault and the Pit aren't rooms of the Codex)
    G.FUNCS['p70/r/tick'].insert(1, 'execute unless entity @s[tag=bm.gvcx] if entity @a[tag=bm.gvp,distance=..12] run function bm:p117/cx/room')
    fn('p117/cx/room', ['tag @s add bm.gvcx'] +
       [f'execute if entity @s[tag=bm.gvr_{k}] as @a[tag=bm.gvp,distance=..16] at @s run function bm:p117/cx/r_{k}' for k in rooms + events])
    # curses: when a cursed room is beaten, the crew writes that curse down
    G.FUNCS['p116/curse/won'] += [f'execute if score @s bm.gvcrs matches {c} as @a[tag=bm.gvp,distance=..300] if score @s bm.gvi = #gi bm.rng at @s run function bm:p117/cx/c{c}' for c in P116.CURSES]
    # the pages
    G.FUNCS['p80/act'].insert(2, f'execute if score #act bm.pay matches {C_CODEX} run return run function bm:p117/cx/menu')
    G.FUNCS['p80/act'].insert(2, f'execute if score #act bm.pay matches {C_SEC + 5} run return run function bm:p218/odds')        # (2.94o)
    for s in SECS:
        G.FUNCS['p80/act'].insert(2, f'execute if score #act bm.pay matches {C_SEC + s - 1} run return run function bm:p117/cx/page{s}')
    menu = [f'scoreboard players set @s bm.menu {C_CODEX}', 'data remove storage bm:ui cx']
    for s, (snm, ents, (rid, rn, rtxt)) in SECS.items():
        menu += [f'function bm:p117/cx/count{s}', f'execute store result storage bm:ui cx.n{s} int 1 run scoreboard players get #cxn bm.rng',
                 f'data modify storage bm:ui cx.w{s} set value "full: {rtxt}"', f'execute if score @s bm.cxr{s} matches 1 run data modify storage bm:ui cx.w{s} set value "✔ paid: {rtxt}"']
    menu.append('function bm:p117/cx/menu_dlg with storage bm:ui cx')
    fn('p117/cx/menu', menu)
    body = [T('"Every room you\'ve walked into, every curse you\'ve lifted, every rare find and every Masterwork - written down. '
              'Fill a section, and the Fixer pays once."\n', '#d8c8a8', italic=True)]
    for s, (snm, ents, rw) in SECS.items():
        body += [T('\n📖 ', CODEX), T(snm + '   ', 'white'), T(f'$(n{s})', CODEX, bold=True), T(f' of {len(ents)}', 'gray'), T(f'\n     $(w{s})', 'dark_gray')]
    dlg = P28.multi([T('THE CODEX', CODEX, bold=True), T('  ·  what you\'ve seen in the vault', 'gray')], [P28.body(body, 300)],
                    [P28.btn([T('📖 ', CODEX), T(snm, 'white', bold=True)], C_SEC + s - 1, width=150) for s, (snm, _e, _r) in SECS.items()] +
                    [P28.btn([T('🎲 ', '#ffcf40'), T('Raid Odds', 'white', bold=True)], C_SEC + 5, width=150,           # (2.94o: phase218)
                             tooltip=T('What a won heist can bring, tier by tier - and your mythic luck.', 'gray'))] +
                    [P28.btn([T('◀ ', P80.OFFICE), T('The Office', 'white')], P80.MENU_CODE, width=150)], columns=2)
    fn('p117/cx/menu_dlg', [f'$dialog show @s {P28.inline(dlg)}'])
    for s, (snm, ents, rw) in SECS.items():
        pg = [f'scoreboard players set @s bm.menu {C_CODEX}', 'data remove storage bm:ui cxp', f'function bm:p117/cx/count{s}',
              'execute store result storage bm:ui cxp.n int 1 run scoreboard players get #cxn bm.rng']
        lines = []
        for i, (key, enm) in enumerate(ents):
            pg += [f'data modify storage bm:ui cxp.e{i} set value "???"', f'data modify storage bm:ui cxp.c{i} set value "dark_gray"',
                   f'execute if score @s bm.cx_{key} matches 1 run data modify storage bm:ui cxp.e{i} set value {snbt(enm)}',
                   f'execute if score @s bm.cx_{key} matches 1 run data modify storage bm:ui cxp.c{i} set value "white"']
            lines += [T('\n◆ ' if i else '◆ ', CODEX), {'text': f'$(e{i})', 'color': f'$(c{i})'}]
        pg.append(f'function bm:p117/cx/page{s}_dlg with storage bm:ui cxp')
        fn(f'p117/cx/page{s}', pg)
        d = P28.multi([T(f'📖 {snm}', CODEX, bold=True), T(f'  ·  $(n) of {len(ents)}', 'gray')], [P28.body(lines, 300)],
                      [P28.btn([T('◀ ', CODEX), T('The Codex', 'white')], C_CODEX, width=150)], columns=1)
        fn(f'p117/cx/page{s}_dlg', [f'$dialog show @s {P28.inline(d)}'])
    # the Office's new button (and its copy on a heist, with 'Leave the heist' still last)
    import phase104 as P104
    cbtn = P28.btn([T('📖 ', CODEX), T('The Codex', 'white', bold=True)], C_CODEX, tooltip=T('Every room, curse, rare find and Masterwork you\'ve seen - and what a full page pays.'), width=150)
    P80.HUB['actions'].append(cbtn)
    hub1 = copy.deepcopy(P80.HUB); hub1['actions'].insert(0, copy.deepcopy(P80.PLAN_BTN))     # (off a heist, planning heads the Office - 2.76 fix: it went missing here)
    G.FUNCS['p80/office_dlg'] = [f'$dialog show @s {P28.inline(hub1)}']
    hub2 = copy.deepcopy(P80.HUB)
    hub2['actions'].append(P28.btn([T('⏏ ', '#ff9a7a'), T('Leave the heist', '#ff9a7a', bold=True)], P104.C_LEAVE_ASK, width=150,
                                   tooltip=T('Home now, from right here: your own gear comes back; the fee and any share stay behind. (It asks first.)', 'gray')))
    G.FUNCS['p104/office_dlg'] = [f'$dialog show @s {P28.inline(hub2)}']
    fn('admin/codex_reset', [f'scoreboard players reset @s bm.cx_{key}' for key in SECTION_OF] + [f'scoreboard players reset @s bm.cxr{s}' for s in SECS] + [say('Your Codex is blank again.')])
    fn('admin/codex_fill', [f'function bm:p117/cx/{key}' for key in SECTION_OF])

    # ================================================================== wiring
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']; f[-1:-1] = fast
    s_ = G.FUNCS['loop/second']; s_[-1:-1] = second


def rp(R):
    g = R.grid
    ic = R.ICONS
    ic['smelling_salts'] = g(['................', '......kkkk......', '......cccc......', '.......kk.......', '......k..k......', '.....kwwwwk.....', '....kwbbbbwk....', '....kwbsbbwk....',
                              '....kwbbbbwk....', '....kwbbsbwk....', '....kwbbbbwk....', '....kwwwwwwk....', '.....kkkkkk.....', '................', '................', '................'],
                             dict(k='#3a4050', c='#a07040', w='#e8f0ff', b='#c0e0f0', s='#ffffff'))
    ic['thiefs_hourglass'] = g(['................', '....kkkkkkkk....', '.....bbbbbb.....', '.....bssssb.....', '......bssb......', '.......sb.......', '.......bb.......', '.......bs.......',
                                '......b..b......', '.....b.ss.b.....', '.....bssssb.....', '.....bbbbbb.....', '....kkkkkkkk....', '................', '................', '................'],
                               dict(k='#6a4a20', b='#c8e0f0', s='#e0c080'))
    ic['salamander_salve'] = g(['................', '................', '.......ff.......', '......fyyf......', '......fyf.......', '....kkkkkkkk....', '...kwwwwwwwwk...', '...krrrrrrrrk...',
                                '...krroorrrrk...', '...krrrrroork...', '...krrrrrrrrk...', '....kkkkkkkk....', '................', '................', '................', '................'],
                               dict(k='#5a3020', w='#c0c0c8', r='#d84020', o='#ff9a3a', f='#ff6a1a', y='#ffe060'))
    ic['alarm_jammer'] = g(['................', '..........a.....', '.........a......', '..kkkkkkka.k....', '..kbbbbbbbbk....', '..kbggbbrrbk....', '..kbggbbrrbk....', '..kbbbbbbbbk....',
                            '..kbwwwwwwbk....', '..kbwkwkwwbk....', '..kbwwwwwwbk....', '..kkkkkkkkkk....', '................', '................', '................', '................'],
                           dict(k='#2a3040', b='#7ab0ff', g='#7dff6a', r='#ff5a5a', w='#d0e0ff', a='#c0c0c0'))
    ic['mudlarks_charm'] = g(['................', '.......kk.......', '......k..k......', '.......kk.......', '.......ll.......', '.....bbbbbb.....', '....bbbbbbbb....', '...bbbb..bbbb...',
                              '...bbb....bbb...', '...bbbb..bbbb...', '....bbbbbbbb....', '.....bbbbbb.....', '................', '................', '................', '................'],
                             dict(k='#8a6a40', l='#5a4020', b='#a08050'))
    ic['tinkers_thimble'] = g(['................', '................', '......ssss......', '.....sddddS.....', '....sdsdsdsS....', '....sddddddS....', '....sdsdsdsS....', '....sddddddS....',
                               '....sdsdsdsS....', '....sddddddS....', '....ssssssss....', '................', '................', '................', '................', '................'],
                              dict(s='#e0e0e8', d='#a0a0b0', S='#707080'))
    ic['wayfarers_lodestar'] = g(['................', '.......bb.......', '......b..b......', '.....bbbbbb.....', '....b..yy..b....', '....b.yYYy.b....', '....byYwwYyb....', '....b.yYYy.b....',
                                  '....b..yy..b....', '.....bbbbbb.....', '......bbbb......', '.......bb.......', '................', '................', '................', '................'],
                                 dict(b='#b08a40', y='#ffe890', Y='#fff4c0', w='#ffffff'))
    ic['songbird'] = g(['................', '.........kk.....', '........kyyk....', '.......kyyyyk.o.', '..k...kyywyyko..', '.kok.kyyyyyyk...', '..kkkyyyyyyk....', '....kyyyyyk.....',
                        '....kyyyyk......', '.....kkkk.......', '......k.k.......', '.....kk.kk......', '................', '..n.........n...', '.nn........nn...', '.n.........n....'],
                       dict(k='#5a4020', y='#e0b060', w='#ffffff', o='#ff9030', n='#ffe090'))
    ic['merchants_bell'] = g(['................', '.......kk.......', '......k..k......', '.......kk.......', '......yyyy......', '.....yYYYYy.....', '....yYYYYYYy....', '....yYYYYYYy....',
                              '....yYYwYYYy....', '...yYYYwYYYYy...', '...yYYYYYYYYy...', '..yyyyyyyyyyyy..', '.......kk.......', '.......kk.......', '................', '................'],
                             dict(k='#5a4020', y='#b08020', Y='#e8c870', w='#fff4c0'))
    ic['smugglers_veil'] = g(['................', '.....gggggg.....', '....gGGGGGGg....', '...gGGgGGgGGg...', '...gGGGGGGGGg...', '...gGgGGGGgGg...', '...gGGGGGGGGg...', '...gGGgGGgGGg...',
                              '...gGGGGGGGGg...', '...gGgGGGGgGg...', '....gGGGGGGg....', '.....g.gg.g.....', '................', '................', '................', '................'],
                             dict(g='#4a4a6a', G='#8a8aa8'))
    ic['firefly_jar'] = g(['................', '.....kkkkkk.....', '.....wwwwww.....', '....w......w....', '...w..y.....w...', '...w.....y..w...', '...w.y......w...', '...w....y...w...',
                           '...w..y...y.w...', '...w........w...', '....w..y...w....', '.....wwwwww.....', '................', '................', '................', '................'],
                          dict(k='#7a5a30', w='#c0e0e8', y='#e8ff70'))
    ic['duelists_ribbon'] = g(['................', '.......rr.......', '......rRRr......', '.....rR..Rr.....', '.....rR..Rr.....', '......rRRr......', '.....rr..rr.....', '....rR....Rr....',
                               '...rR......Rr...', '..rR........Rr..', '..r..........r..', '................', '................', '................', '................', '................'],
                              dict(r='#a02040', R='#e05070'))
    ic['honeycomb_brooch'] = g(['................', '......kkkk......', '.....kyyyyk.....', '....kyYkkYyk....', '....kyk..kyk....', '....kyYkkYyk....', '....kykyykyk....', '....kyYkkYyk....',
                                '.....kyyyyk.....', '......kkkk......', '.......h........', '.......h........', '........h.......', '................', '................', '................'],
                               dict(k='#8a5010', y='#ffb030', Y='#ffd870', h='#ffc040'))
    ic['fizzle_stone'] = g(['................', '................', '.....kkkkk......', '....kgggggk.....', '...kgGggGggk....', '...kgggggggk....', '...kgGgggGgk....', '...kgggGgggk....',
                            '....kgggggk.....', '.....kkkkk......', '.......s........', '......s.s.......', '.......s........', '................', '................', '................'],
                           dict(k='#3a4a3a', g='#6a8a6a', G='#7ad070', s='#c0c0c0'))
    ic['navigators_astrolabe'] = g(['................', '.......kk.......', '.....yyyyyy.....', '....y..k...y....', '...y...k....y...', '...y...k....y...', '..y....k.....y..', '..ykkkkwkkkkky..',
                                    '..y....k.....y..', '...y...k....y...', '...y...k....y...', '....y..k...y....', '.....yyyyyy.....', '................', '................', '................'],
                                   dict(k='#6a4a20', y='#c09040', w='#fff4c0'))
    ic['trial_key_fob'] = g(['................', '....cccc........', '...c....c.......', '...c....c.......', '....cccc........', '.......kk.......', '........kk......', '.........kkk....',
                             '..........kkk...', '.........k.k....', '.........kk.....', '................', '...b.....b......', '..b.......b.....', '................', '................'],
                            dict(c='#80c0d0', k='#506070', b='#a0e0ff'))
    ic['fletchers_charm'] = g(['................', '..w.............', '..ww............', '..wwg...........', '...wwg..........', '....wwg.........', '.....wwyy.......', '......yyy.......',
                               '.......yyk......', '........kk......', '.........kk.....', '..........kk....', '...........kk...', '............k...', '................', '................'],
                              dict(w='#f0f0e0', g='#a0b070', y='#e0c050', k='#6a5030'))
    ic['gale_locket'] = g(['................', '.......kk.......', '......k..k......', '.......kk.......', '.....ssssss.....', '....sbbbbbbs....', '....sbwwbbbs....', '....sbbwwwbs....',
                           '....sbbbbwbs....', '....sbbbbbbs....', '.....ssssss.....', '................', '..w..ww..w......', '...ww..ww.......', '................', '................'],
                          dict(k='#7a8a9a', s='#a0b0c0', b='#c0e0f0', w='#ffffff'))
    ic['phoenix_plume'] = g(['................', '..........ooo...', '.........oyyo...', '........oyyro...', '.......oyyro....', '......oyyro.....', '.....oyyro......', '....oyyro.......',
                             '...oyyro........', '...oyro.........', '..oor...........', '..kk............', '.k..............', '................', '................', '................'],
                            dict(o='#ff6a30', y='#ffd060', r='#c02010', k='#5a3a20'))
    ic['phoenix_ash'] = g(['................', '..........aaa...', '.........adda...', '........adddr...', '.......addda....', '......addda.....', '.....addda......', '....addra.......',
                           '...addda........', '...adra.........', '..aar...........', '..kk............', '.k..............', '................', '................', '................'],
                          dict(a='#5a4a40', d='#8a7a70', r='#c05020', k='#3a2a20'))

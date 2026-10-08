"""Phase 2.32: two more roaming bosses, their relics, and WANTED posters on the Bounty Board.

THE SAND PHARAOH - a roaming boss of the desert day
- After the first 10 days, rarely, when someone stands under open sky in a desert by day, a sandstorm rises and the
  Pharaoh walks out of it (about 20 blocks off). Everyone within 30 blocks feels it: "The wind turns to sand..."
- A towering husk king, three times a man's height, in a golden crown (320 health). He pours out scarab swarms, throws sand in your eyes, raises
  Tomb Guards (husks in gold) and burns you with a beam of the sun. At half health the storm thickens: Strength, speed,
  and the sand bursts up beneath you. The storm follows him: blowing sand, the wind, the hiss of the dunes - and his song.
- He sinks back into the dunes at dusk (or when nobody is near). Slay him for Tokens, Medallions, a Trophy and gold -
  and (always, 2.34) THE PHARAOH'S CROOK.

THE STORM ROC - a roaming boss of the thunderstorm
- In any thunderstorm (after day 10), now and then, a colossal phantom comes down out of the clouds
  near someone under open sky. "Thunder rolls... something vast circles above."
- 260 health. It circles and dives, calls lightning down on you (watch for the sparks), and beats gusts of wind that throw
  you off your feet. At half health it shrieks and Stormlings join the hunt. It leaves when the storm does.
  Slay it for Tokens, Medallions, a Trophy, feathers - and (always, 2.34) THE THUNDERBIRD TALON.

THE RELICS - like the Horseman's Head, each takes four forms. Off hand + look straight up + right-click:
  Blaze Rod = OFFENSE, Armadillo Scute = DEFENSE, Breeze Rod = RANGED, Heartstone = SUPPORT (the catalyst is used up).
- The Pharaoh's Crook (stronger by day, under the sun):
  Crook of Scarabs (OFFENSE): heavy blows; right-click sends a scarab swarm that eats through everything in its path.
  Crook of the Sands (DEFENSE): blows slow; right-click raises a Sandstone Shell (8 s) - Resistance II, and whoever hits
    you gets sand in the eyes.
  Crook of the Sun (RANGED): right-click: a Sunbeam Lance - pierces everything in 40 blocks and sets it alight.
  Crook of Ra (SUPPORT): right-click: the Blessing of Ra - Strength and Haste II for you and every ally within 8 blocks.
- The Thunderbird Talon (stronger in a thunderstorm):
  Thunderbird Talon (OFFENSE): its blows often call down a thunderbolt; right-click: a Thunderclap strikes every monster
    within 5 blocks.
  Static Talon (DEFENSE): right-click: a Static Field (8 s) - Resistance, and anything near you or that hits you is shocked.
  Stormcaller Talon (RANGED): right-click: Chain Lightning - 32 blocks, leaping to 4 targets.
  Tailwind Talon (SUPPORT): right-click: a Tailwind - Speed II, Jump Boost II and Slow Falling for you and your allies.

WANTED - the Bounty Board now lists the three roaming bosses as standing bounties: whoever slays one collects
8 Tokens + 2 Medallions on top of its loot. Slaying all three: the Monster Slayer achievement; holding a relic of each:
Relic Hunter."""
from items import item, attr, T, TOTEM
from useitem import hold, HOLD
from nbt import snbt, B, F, D, Int, IntArray
from phase42 import ring, FIRE_RES, NO_DROP, at

GRACE_DAYS = 10
PH_HP, ROC_HP = 320, 260
PH_ODDS, ROC_ODDS = 300, 30           # 1 in N, every 20 s (a desert day / a thunderstorm)
GOLD, SAND, STORM, VOLT = '#e8b923', '#d8b878', '#7ab8ff', '#ffe14a'
RELIC = '*[minecraft:custom_data~{bm_relic:1b}]'
MOB = ('type=!#bm:p44_nonmob,type=!minecraft:player,tag=!bm.npc,tag=!bm.wilfrey,tag=!bm.wil_body,tag=!bm.frogpet,tag=!bm.merc,'
       'tag=!bm.cecilpet,tag=!bm.emmapet,tag=!bm.r53hit')
NEAR = 'gamemode=!creative,gamemode=!spectator'
CATALYSTS = [(1, 'minecraft:blaze_rod'), (2, 'minecraft:armadillo_scute'), (3, 'minecraft:breeze_rod'), (4, '*[minecraft:custom_data~{bm:"heartstone"}]')]
CLASS = {1: ('OFFENSE', 'red'), 2: ('DEFENSE', 'aqua'), 3: ('RANGED', 'green'), 4: ('SUPPORT', 'light_purple')}
_cat = [('Off hand + look up + right-click to turn it:', 'dark_gray'), ('Blaze Rod - Offense, Armadillo Scute - Defense,', 'dark_gray'),
        ('Breeze Rod - Ranged, Heartstone - Support.', 'dark_gray')]
_melee = lambda dmg, spd=-2.8: [attr('attack_damage', dmg, 'mainhand', ident='minecraft:base_attack_damage'),
                                attr('attack_speed', spd, 'mainhand', ident='minecraft:base_attack_speed')]

# family -> form -> (item id, name, colour, melee, lore, cooldown ticks)
FAMILIES = {
    'crook': {1: ('pharaoh_crook', 'Crook of Scarabs', GOLD, 9, [('Heavy blows.', 'gray'), ('Right-click: a scarab swarm that eats through', 'blue'),
                                                                   ('everything in its path (14 blocks).', 'blue')], 60),
              2: ('crook_sands', 'Crook of the Sands', SAND, 6, [('Its blows slow their victims.', 'gray'), ('Right-click: a Sandstone Shell (8 s) -', 'blue'),
                                                                   ('Resistance II, and whoever hits you gets', 'blue'), ('sand in the eyes. 20 s to recover.', 'blue')], 400),
              3: ('crook_sun', 'Crook of the Sun', '#ffdf6a', 4, [('A light club.', 'gray'), ('Right-click: a Sunbeam Lance that pierces', 'blue'),
                                                                   ('everything in 40 blocks and sets it alight.', 'blue')], 30),
              4: ('crook_ra', 'Crook of Ra', '#ff9a3c', 3, [('A poor club.', 'gray'), ('Right-click: the Blessing of Ra - Strength and', 'blue'),
                                                             ('Haste II (20 s) for you and every ally within', 'blue'), ('8 blocks. 30 s to recover.', 'blue')], 600)},
    'talon': {1: ('storm_talon', 'Thunderbird Talon', VOLT, 8, [('Its blows often call down a thunderbolt.', 'gray'),
                                                                 ('Right-click: a Thunderclap strikes every monster', 'blue'), ('within 5 blocks. 10 s to recover.', 'blue')], 200),
              2: ('talon_static', 'Static Talon', STORM, 6, [('Its blows weaken their victims.', 'gray'), ('Right-click: a Static Field (8 s) - Resistance,', 'blue'),
                                                              ('and anything near you or that hits you is', 'blue'), ('shocked. 20 s to recover.', 'blue')], 400),
              3: ('talon_chain', 'Stormcaller Talon', '#b48cff', 4, [('A light weapon.', 'gray'), ('Right-click: Chain Lightning - 32 blocks,', 'blue'),
                                                                     ('leaping on to 4 targets.', 'blue')], 50),
              4: ('talon_wind', 'Tailwind Talon', '#9affd8', 3, [('A poor weapon.', 'gray'), ('Right-click: a Tailwind - Speed II, Jump Boost II', 'blue'),
                                                                 ('and Slow Falling for you and every ally', 'blue'), ('within 8 blocks. 25 s to recover.', 'blue')], 500)}}
FLAVOUR = {'crook': ("The Sand Pharaoh's crook of gold and lapis.", ('Stronger by day, under the sun.', 'gold')),
           'talon': ("A talon of the Storm Roc, crackling still.", ('Stronger in a thunderstorm.', 'gold'))}
EDGE = {('crook', 2): 'sands_edge', ('talon', 1): 'thunder_edge', ('talon', 2): 'static_edge'}
def define_relics(families, flavour, edge, extra_attrs=None):
    """The relic items (2.33: shared with phase54): four forms a family, right-click runs bm:p53/<family>/use."""
    for fam, forms in families.items():
        for v, (iid, name, col, dmg, lore, cd) in forms.items():
            c = {'minecraft:attribute_modifiers': _melee(dmg) + list((extra_attrs or {}).get((fam, v), []))}
            if (fam, v) in edge: c['minecraft:enchantments'] = {f'bm:{edge[(fam, v)]}': Int(1)}
            item(iid, TOTEM, name, col, [flavour[fam][0], CLASS[v]] + lore + [flavour[fam][1]] + _cat,
                 model=f'bm:{iid}', stack=1, cat='relic', glint=False, bold=True, custom_extra={'bm_relic': B(1), 'rf': fam},
                 comps=dict(hold('none'), **c))
            HOLD[iid] = f'bm:p53/{fam}/use'


define_relics(FAMILIES, FLAVOUR, EDGE)
CAT_FX = {1: ['particle minecraft:flame ~ ~1.2 ~ 0.4 0.6 0.4 0.05 30', 'playsound minecraft:item.firecharge.use player @a[distance=..16] ~ ~ ~ 1 0.8'],
          2: ['particle minecraft:block{block_state:"minecraft:sandstone"} ~ ~1.2 ~ 0.4 0.6 0.4 0 30', 'playsound minecraft:entity.armadillo.scute_drop player @a[distance=..16] ~ ~ ~ 1 0.8'],
          3: ['particle minecraft:small_gust ~ ~1.2 ~ 0.4 0.6 0.4 0 12', 'playsound minecraft:entity.breeze.shoot player @a[distance=..16] ~ ~ ~ 1 1'],
          4: ['particle minecraft:heart ~ ~1.4 ~ 0.5 0.5 0.5 0 10', 'playsound minecraft:entity.warden.heartbeat player @a[distance=..16] ~ ~ ~ 1.5 1']}


def relic_funcs(G, families):
    """Each family's form check, right-click dispatch (catalyst turn / cooldown / mood / act_N) and turns.
    The family's bm:p53/mood_<family> and bm:p53/<family>/act_<form> functions are written by its phase."""
    fn, title = G.fn, G.title
    holds = '*[minecraft:custom_data~{bm:"%s"}]'
    for fam, forms in families.items():
        fn(f'p53/{fam}/form', ['scoreboard players set #rv bm.rng 0'] +
           [f'execute if items entity @s weapon.mainhand {holds % iid} run return run scoreboard players set #rv bm.rng {v}' for v, (iid, *_r) in forms.items()])
        fn(f'p53/{fam}/use', [f'execute unless items entity @s weapon.mainhand {RELIC} run return 0',
                              f'function bm:p53/{fam}/form',
                              f'execute if entity @s[x_rotation=-90..-55] if function bm:p53/cat/has run return run function bm:p53/{fam}/turn',
                              'execute if score @s bm.rcd matches 1.. run return run function bm:p53/wait',
                              f'function bm:p53/mood_{fam}', 'tag @s add bm.r53me'] +
           [f'execute if score #rv bm.rng matches {v} run function bm:p53/{fam}/act_{v}' for v in forms] +
           ['tag @s remove bm.r53me', 'tag @e[tag=bm.r53hit] remove bm.r53hit'] +
           [f'execute if score #rv bm.rng matches {v} run scoreboard players set @s bm.rcd {cd}' for v, (*_r, cd) in forms.items()])
        fn(f'p53/{fam}/turn', [f'execute if items entity @s weapon.offhand {c} run return run function bm:p53/{fam}/to_{v}' for v, c in CATALYSTS])
        for v, (iid, name, col, *_r) in forms.items():
            fn(f'p53/{fam}/to_{v}', [f'execute if score #rv bm.rng matches {v} run return run ' + title('@s', 'actionbar', T('It is already in that form.', 'gray')),
                                     f'item replace entity @s weapon.mainhand with {G.item_arg(iid)}',
                                     'item modify entity @s weapon.offhand {function:"minecraft:set_count",count:-1,add:true}', 'scoreboard players set @s bm.rcd 0'] +
               CAT_FX[v] + [title('@s', 'actionbar', [T(name, col, bold=True), T(' - ' + CLASS[v][0], CLASS[v][1])])])

# ---------------------------------------------------------------------- the bosses' bodies
PHARAOH = {'Tags': ['bm.seen', 'bm.tiered', 'bm.sph', 'bm.sph_new'], 'PersistenceRequired': B(1), 'Silent': B(1),
           'equipment': {'head': {'id': 'minecraft:golden_helmet', 'count': Int(1), 'components': {
                             'minecraft:trim': {'material': 'minecraft:lapis', 'pattern': 'minecraft:dune'}}},
                         'mainhand': {'id': 'minecraft:golden_hoe', 'count': Int(1)}},
           'CustomName': T('The Sand Pharaoh', GOLD, bold=True), 'Health': F(PH_HP), 'DeathLootTable': 'bm:p53/pharaoh',
           'attributes': [at('max_health', PH_HP), at('attack_damage', 7), at('armor', 6), at('follow_range', 64), at('movement_speed', 0.26),
                          at('scale', 2.6), at('knockback_resistance', 1.0), at('step_height', 2.0), at('safe_fall_distance', 40)],
           'active_effects': [FIRE_RES], 'drop_chances': NO_DROP}
GUARD = {'Tags': ['bm.seen', 'bm.tiered', 'bm.sphmin'], 'CustomName': T('Tomb Guard', SAND), 'Health': F(30), 'PersistenceRequired': B(1),
         'attributes': [at('max_health', 30), at('follow_range', 48)], 'drop_chances': NO_DROP,
         'equipment': {'head': {'id': 'minecraft:golden_helmet', 'count': Int(1)}, 'chest': {'id': 'minecraft:golden_chestplate', 'count': Int(1)},
                       'mainhand': {'id': 'minecraft:golden_sword', 'count': Int(1)}}}
SCARAB = {'Tags': ['bm.seen', 'bm.tiered', 'bm.sphmin', 'bm.scarab'], 'CustomName': T('Scarab', '#3a6a5a'), 'Lifetime': Int(1800),
          'Health': F(6), 'attributes': [at('max_health', 6), at('movement_speed', 0.32), at('scale', 0.8)]}
ROC = {'Tags': ['bm.seen', 'bm.tiered', 'bm.roc', 'bm.roc_new'], 'PersistenceRequired': B(1), 'Silent': B(1), 'size': Int(0), 'anchor_pos': IntArray([0, 0, 0]),
       'CustomName': T('The Storm Roc', STORM, bold=True), 'Health': F(ROC_HP), 'DeathLootTable': 'bm:p53/roc',
       'attributes': [at('max_health', ROC_HP), at('attack_damage', 9), at('armor', 6), at('follow_range', 64), at('scale', 4.5),
                      at('knockback_resistance', 0.8)],
       'active_effects': [FIRE_RES], 'drop_chances': NO_DROP}
STORMLING = {'Tags': ['bm.seen', 'bm.tiered', 'bm.rocmin'], 'CustomName': T('Stormling', STORM), 'size': Int(1), 'Health': F(20),
             'PersistenceRequired': B(1), 'attributes': [at('max_health', 20)], 'active_effects': [FIRE_RES]}


def generate(G):
    fn, wjson, title, give, tellraw, PREFIX = G.fn, G.wjson, G.title, G.give, G.tellraw, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    tick, fast, second = [], [], []
    objs = ['bm.rcd dummy', 'bm.rst dummy', 'bm.r53t dummy', 'bm.r53x dummy', 'bm.rfx dummy', 'bm.r53w dummy']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o}' for o in objs] + [
        f'bossbar add bm:sph {snbt(T("The Sand Pharaoh", GOLD, bold=True))}', 'bossbar set bm:sph color yellow',
        'bossbar set bm:sph style notched_10', f'bossbar set bm:sph max {PH_HP}', 'bossbar set bm:sph visible false',
        f'bossbar add bm:roc {snbt(T("The Storm Roc", STORM, bold=True))}', 'bossbar set bm:roc color blue',
        'bossbar set bm:roc style notched_10', f'bossbar set bm:roc max {ROC_HP}', 'bossbar set bm:roc visible false']
    G.OBJECTIVES += [o.split()[0] for o in objs]
    G.FUNCS['admin/uninstall'].insert(0, 'bossbar remove bm:sph')
    G.FUNCS['admin/uninstall'].insert(0, 'bossbar remove bm:roc')

    # ------------------------------------------------------------------ registry bits
    for name, msg in [('scarab', 'bm.scarab'), ('sunbeam', 'bm.sunbeam'), ('sandstorm', 'bm.sandstorm')]:
        wjson(f'bm/damage_type/{name}.json', {'exhaustion': 0.1, 'message_id': msg, 'scaling': 'when_caused_by_living_non_player'})
    wjson('bm/predicate/p53/desert.json', {'condition': 'minecraft:location_check', 'predicate': {'biomes': ['minecraft:desert']}})
    wjson('bm/predicate/p53/thunder.json', {'condition': 'minecraft:weather_check', 'thundering': True})
    ench = lambda desc, col, effs: {'anvil_cost': 8, 'description': T(desc, col), 'max_level': 1, 'weight': 1,
                                    'min_cost': {'base': 1, 'per_level_above_first': 0}, 'max_cost': {'base': 1, 'per_level_above_first': 0},
                                    'slots': ['mainhand'], 'supported_items': '#minecraft:enchantable/weapon',
                                    'effects': {'minecraft:post_attack': [dict({'affected': 'victim', 'enchanted': 'attacker'}, **e) for e in effs]}}
    mob_eff = lambda e, s, a: {'type': 'minecraft:apply_mob_effect', 'to_apply': f'minecraft:{e}', 'min_duration': float(s), 'max_duration': float(s),
                               'min_amplifier': float(a), 'max_amplifier': float(a)}
    wjson('bm/enchantment/sands_edge.json', ench('Sandbound', SAND, [{'effect': mob_eff('slowness', 3, 1)}]))
    wjson('bm/enchantment/static_edge.json', ench('Static', STORM, [{'effect': mob_eff('weakness', 3, 0)}]))
    wjson('bm/enchantment/thunder_edge.json', ench('Thunderbird', VOLT, [
        {'effect': {'type': 'minecraft:run_function', 'function': 'bm:p53/talon/mark'},
         'requirements': {'condition': 'minecraft:random_chance', 'chance': 0.3}}]))
    wjson('bm/tags/item/p53_catalyst.json', {'values': ['minecraft:blaze_rod', 'minecraft:armadillo_scute', 'minecraft:breeze_rod']})

    # ================================================================== the relics
    holds = '*[minecraft:custom_data~{bm:"%s"}]'
    fn('p53/cat/has', ['execute if items entity @s weapon.offhand #bm:p53_catalyst run return 1',
                       'execute if items entity @s weapon.offhand ' + holds % 'heartstone' + ' run return 1', 'return 0'])
    fn('p53/wait', ['scoreboard players operation #fs bm.rng = @s bm.rcd', 'scoreboard players add #fs bm.rng 19', 'scoreboard players operation #fs bm.rng /= #20 bm.rng',
                    title('@s', 'actionbar', [T('The relic is gathering its strength... ', 'gray'), {'score': {'name': '#fs', 'objective': 'bm.rng'}, 'color': 'white'},
                                              T(' s', 'gray')])])
    # this hit's damage: base (tenths) x the relic's mood (x1.5 for the crook under the sun, the talon in a thunderstorm)
    fn('p53/dmg', ['$scoreboard players set #dm bm.rng $(b)', 'scoreboard players operation #dm bm.rng *= #rmul bm.rng',
                   'scoreboard players operation #dm bm.rng /= #10 bm.rng',
                   'execute store result storage bm:tmp p53.d double 0.1 run scoreboard players get #dm bm.rng'])
    fn('p53/mood_crook', ['scoreboard players set #rmul bm.rng 10',
                          'execute if dimension minecraft:overworld if score #tod bm.bm matches 0..12000 positioned ~ ~1.6 ~ if predicate bm:sees_sky run scoreboard players set #rmul bm.rng 15'])
    fn('p53/mood_talon', ['scoreboard players set #rmul bm.rng 10',
                          'execute if dimension minecraft:overworld if predicate bm:p53/thunder run scoreboard players set #rmul bm.rng 15'])
    relic_funcs(G, FAMILIES)
    fast.append('scoreboard players remove @a[scores={bm.rcd=1..}] bm.rcd 5')
    # (hits from a relic: as the target; bm.r53me = the wielder)
    hit = lambda dtype, extra=(): [f'tag @s add bm.r53hit', f'$damage @s $(d) {dtype} by @a[tag=bm.r53me,limit=1]'] + list(extra)
    pvp = f'@a[tag=!bm.r53me,tag=!bm.r53hit,tag=!bm.nopvp,{NEAR}'

    # ---- Crook of Scarabs: a swarm down the line of sight, eating through all in its path
    fn('p53/crook/act_1', ['function bm:p53/dmg {b:70}', 'scoreboard players set #k bm.rng 0',
                           'playsound minecraft:entity.silverfish.ambient player @a[distance=..24] ~ ~ ~ 1.5 0.6',
                           'playsound minecraft:item.brush.brushing.sand player @a[distance=..24] ~ ~ ~ 1.5 0.7',
                           'execute anchored eyes positioned ^ ^-0.4 ^1 run function bm:p53/crook/swarm'])
    fn('p53/crook/swarm', ['scoreboard players add #k bm.rng 1', 'particle minecraft:dust{color:[0.12,0.18,0.14],scale:0.7} ~ ~ ~ 0.5 0.5 0.5 0 10',
                           'particle minecraft:dust{color:[0.25,0.55,0.45],scale:0.5} ~ ~ ~ 0.5 0.5 0.5 0 4',
                           'particle minecraft:falling_dust{block_state:"minecraft:sand"} ~ ~ ~ 0.4 0.4 0.4 0 2',
                           f'execute as @e[{MOB},distance=..1.8] at @s run function bm:p53/hit/scarab with storage bm:tmp p53',
                           f'execute as {pvp},distance=..1.8] at @s run function bm:p53/hit/scarab with storage bm:tmp p53',
                           'execute unless block ~ ~ ~ #bm:grap_pass run return 0', 'execute if score #k bm.rng matches 14.. run return 0',
                           'execute positioned ^ ^ ^1 run function bm:p53/crook/swarm'])
    fn('p53/hit/scarab', hit('bm:scarab', ['effect give @s minecraft:hunger 5 1', 'effect give @s minecraft:slowness 2 0',
                                           'particle minecraft:dust{color:[0.12,0.18,0.14],scale:0.6} ~ ~1 ~ 0.3 0.5 0.3 0 12']))
    # ---- Crook of the Sands: a Sandstone Shell
    fn('p53/crook/act_2', ['effect give @s minecraft:resistance 8 1 true', 'effect give @s minecraft:absorption 8 0 true',
                           'tag @s add bm.r53shell', 'scoreboard players set @s bm.rst 8',
                           'particle minecraft:block{block_state:"minecraft:sandstone"} ~ ~1 ~ 0.6 0.8 0.6 0 60',
                           'playsound minecraft:block.stone.place player @a[distance=..16] ~ ~ ~ 1.2 0.6',
                           'playsound minecraft:item.brush.brushing.sand player @a[distance=..16] ~ ~ ~ 1 0.6', say('A shell of sandstone closes around you.', SAND)])
    # ---- Crook of the Sun: a Sunbeam Lance
    fn('p53/crook/act_3', ['function bm:p53/dmg {b:80}', 'scoreboard players set #k bm.rng 0',
                           'playsound minecraft:block.beacon.power_select player @a[distance=..32] ~ ~ ~ 1 1.6',
                           'playsound minecraft:entity.blaze.shoot player @a[distance=..32] ~ ~ ~ 0.8 1.4',
                           'execute anchored eyes positioned ^ ^-0.2 ^0.8 run particle minecraft:flash{color:[1.0,0.9,0.5,1.0]} ~ ~ ~ 0 0 0 0 1',
                           'execute anchored eyes positioned ^ ^-0.2 ^1 run function bm:p53/crook/beam'])
    fn('p53/crook/beam', ['scoreboard players add #k bm.rng 1', 'particle minecraft:end_rod ~ ~ ~ 0.03 0.03 0.03 0 1',
                          'particle minecraft:dust{color:[1.0,0.85,0.3],scale:1.2} ~ ~ ~ 0.05 0.05 0.05 0 2',
                          f'execute positioned ~ ~-0.9 ~ as @e[{MOB},distance=..1.3] at @s run function bm:p53/hit/sun with storage bm:tmp p53',
                          f'execute positioned ~ ~-0.9 ~ as {pvp},distance=..1.3] at @s run function bm:p53/hit/sun with storage bm:tmp p53',
                          'execute unless block ~ ~ ~ #bm:grap_pass run return run particle minecraft:lava ~ ~ ~ 0.1 0.1 0.1 0 3',
                          'execute if score #k bm.rng matches 40.. run return 0', 'execute positioned ^ ^ ^1 run function bm:p53/crook/beam'])
    fn('p53/hit/sun', hit('bm:sunbeam', ['execute if entity @s[type=!minecraft:player] run data merge entity @s {Fire:80s}',
                                         'execute if entity @s[type=minecraft:player] unless predicate bm:p42/burning if block ~ ~ ~ #minecraft:air run function bm:p42/fx/flicker',
                                         'particle minecraft:flame ~ ~1 ~ 0.3 0.5 0.3 0.02 8']))
    # ---- Crook of Ra: the Blessing
    fn('p53/crook/act_4', [*ring(8, 40, 0.2, 'minecraft:dust{color:[1.0,0.75,0.2],scale:1.5}'), 'particle minecraft:totem_of_undying ~ ~1 ~ 2 1 2 0.3 50',
                           'playsound minecraft:block.beacon.activate player @a[distance=..32] ~ ~ ~ 1.2 1.4', 'playsound minecraft:item.totem.use player @a[distance=..32] ~ ~ ~ 0.4 1.6',
                           'execute as @a[distance=..8,gamemode=!spectator] at @s run function bm:p53/crook/bless',
                           'execute as @e[type=#bm:p42_ally,distance=..8] at @s run function bm:p53/crook/bless',
                           say('The Blessing of Ra shines on you and yours.', '#ff9a3c')])
    fn('p53/crook/bless', ['effect give @s minecraft:strength 20 0', 'effect give @s minecraft:haste 20 1', 'effect give @s minecraft:instant_health 1 0',
                           'particle minecraft:wax_on ~ ~1.5 ~ 0.3 0.5 0.3 0 8'])

    # ---- the thunderbolt (no fire, no block damage): a column of sparks, a flash, the crack - at this spot
    fn('p53/bolt', [f'particle minecraft:electric_spark ~ ~{y} ~ 0.08 0.4 0.08 0 5 force @a[distance=..96]' for y in (0.5, 2, 3.5, 5, 6.5, 8, 9.5, 11, 12.5)] +
       ['particle minecraft:end_rod ~ ~6 ~ 0.05 6 0.05 0 25 force @a[distance=..96]', 'particle minecraft:flash{color:[0.8,0.85,1.0,1.0]} ~ ~1 ~ 0 0 0 0 1 force @a[distance=..96]',
        'particle minecraft:electric_spark ~ ~0.2 ~ 0.8 0.1 0.8 0.3 30', 'playsound minecraft:entity.lightning_bolt.thunder weather @a[distance=..96] ~ ~ ~ 1.5 1.3',
        'playsound minecraft:entity.lightning_bolt.impact weather @a[distance=..32] ~ ~ ~ 1 1'])
    # ---- Thunderbird Talon: blows call thunderbolts (just after the hit, past its invulnerable moment); the Thunderclap
    fn('p53/talon/mark', ['tag @s add bm.r53bolt', 'schedule function bm:p53/talon/bolts 11t replace'])
    fn('p53/talon/bolts', ['execute as @e[tag=bm.r53bolt] at @s run function bm:p53/talon/smite'])
    fn('p53/talon/smite', ['tag @s remove bm.r53bolt', 'function bm:p53/bolt',
                           'execute if entity @a[distance=0.1..10,gamemode=!spectator] run return run damage @s 6 minecraft:lightning_bolt by @p[distance=0.1..10,gamemode=!spectator]',
                           'damage @s 6 minecraft:lightning_bolt'])
    fn('p53/talon/act_1', ['function bm:p53/dmg {b:80}', 'particle minecraft:electric_spark ~ ~1 ~ 2.5 0.5 2.5 0.4 80',
                           'playsound minecraft:item.trident.thunder player @a[distance=..48] ~ ~ ~ 1.2 1.2',
                           'execute as @e[type=#bm:p42_foe,distance=..5] at @s run function bm:p53/hit/clap with storage bm:tmp p53'])
    fn('p53/hit/clap', hit('minecraft:lightning_bolt', ['function bm:p53/bolt']))
    # ---- Static Talon: a Static Field
    fn('p53/talon/act_2', ['effect give @s minecraft:resistance 8 0 true', 'tag @s add bm.r53static', 'scoreboard players set @s bm.rst 8',
                           'particle minecraft:electric_spark ~ ~1 ~ 0.8 1 0.8 0.3 60', 'playsound minecraft:block.beacon.activate player @a[distance=..16] ~ ~ ~ 1 1.8',
                           'playsound minecraft:entity.creeper.primed player @a[distance=..16] ~ ~ ~ 0.6 0.6', say('The air around you crackles with static.', STORM)])
    # ---- Stormcaller Talon: Chain Lightning
    fn('p53/talon/act_3', ['function bm:p53/dmg {b:70}', 'scoreboard players set #k bm.rng 0', 'scoreboard players set #ch bm.rng 0',
                           'playsound minecraft:item.trident.thunder player @a[distance=..48] ~ ~ ~ 0.8 1.6',
                           'execute anchored eyes positioned ^ ^-0.2 ^1 run function bm:p53/chain/ray'])
    fn('p53/chain/ray', ['scoreboard players add #k bm.rng 1', 'particle minecraft:electric_spark ~ ~ ~ 0.05 0.05 0.05 0 2',
                         'execute if score #k bm.rng matches 2.. run particle minecraft:end_rod ~ ~ ~ 0 0 0 0 1',
                         f'execute positioned ~ ~-0.9 ~ as @e[{MOB},distance=..1.4,sort=nearest,limit=1] at @s run return run function bm:p53/chain/zap with storage bm:tmp p53',
                         f'execute positioned ~ ~-0.9 ~ as {pvp},distance=..1.4,sort=nearest,limit=1] at @s run return run function bm:p53/chain/zap with storage bm:tmp p53',
                         'execute unless block ~ ~ ~ #bm:grap_pass run return 0', 'execute if score #k bm.rng matches 32.. run return 0',
                         'execute positioned ^ ^ ^1 run function bm:p53/chain/ray'])
    fn('p53/chain/zap', hit('minecraft:lightning_bolt', [
        'particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.2 25', 'particle minecraft:flash{color:[0.8,0.7,1.0,1.0]} ~ ~1 ~ 0 0 0 0 1',
        'playsound minecraft:entity.lightning_bolt.impact player @a[distance=..32] ~ ~ ~ 0.8 1.4', 'scoreboard players add #ch bm.rng 1',
        'execute if score #ch bm.rng matches 4.. run return 0',
        f'execute positioned ~ ~1 ~ facing entity @e[type=#bm:p42_foe,{MOB.split(",", 2)[2]},distance=..7,sort=nearest,limit=1] eyes run function bm:p53/chain/arc',
        f'execute as @e[type=#bm:p42_foe,{MOB.split(",", 2)[2]},distance=..7,sort=nearest,limit=1] at @s run function bm:p53/chain/zap with storage bm:tmp p53']))
    fn('p53/chain/arc', [f'particle minecraft:electric_spark ^ ^ ^{d} 0.05 0.05 0.05 0 2' for d in (0.7, 1.4, 2.1, 2.8, 3.5, 4.2, 4.9, 5.6)] +
       ['particle minecraft:end_rod ^ ^ ^2 0.1 0.1 0.6 0 3'])
    # ---- Tailwind Talon: a Tailwind
    fn('p53/talon/act_4', ['particle minecraft:gust_emitter_small ~ ~1 ~ 0 0 0 0 1', *ring(6, 30, 0.6, 'minecraft:small_gust'),
                           'playsound minecraft:entity.breeze.wind_burst player @a[distance=..32] ~ ~ ~ 1.2 0.8',
                           'execute as @a[distance=..8,gamemode=!spectator] at @s run function bm:p53/talon/wind',
                           'execute as @e[type=#bm:p42_ally,distance=..8] at @s run function bm:p53/talon/wind',
                           say('A tailwind rises behind you and yours.', '#9affd8')])
    fn('p53/talon/wind', ['effect give @s minecraft:speed 20 1', 'effect give @s minecraft:jump_boost 20 1', 'effect give @s minecraft:slow_falling 8 0',
                          'particle minecraft:cloud ~ ~0.3 ~ 0.3 0.1 0.3 0.02 6'])
    # ---- the guards (shell, static field): every second while they last; and whoever hurts you pays
    second.append('execute as @a[scores={bm.rst=1..}] at @s run function bm:p53/guard')
    fn('p53/guard', ['scoreboard players remove @s bm.rst 1',
                     'execute if entity @s[tag=bm.r53shell] run function bm:p53/shell_fx',
                     'execute if entity @s[tag=bm.r53static] run function bm:p53/static_fx',
                     'execute if score @s bm.rst matches ..0 run tag @s remove bm.r53shell', 'execute if score @s bm.rst matches ..0 run tag @s remove bm.r53static'])
    fn('p53/shell_fx', [*ring(1.2, 12, 0.6, 'minecraft:falling_dust{block_state:"minecraft:sandstone"}'), 'particle minecraft:dust_plume ~ ~1 ~ 0.6 0.8 0.6 0.01 4'])
    fn('p53/static_fx', ['particle minecraft:electric_spark ~ ~1 ~ 1.5 0.8 1.5 0.2 30', 'playsound minecraft:block.copper_bulb.turn_on player @a[distance=..12] ~ ~ ~ 0.6 1.6',
                         'tag @s add bm.r53me', 'execute as @e[type=#bm:p42_foe,distance=..3] at @s run function bm:p53/shock', 'tag @s remove bm.r53me'])
    fn('p53/shock_back', ['damage @s 5 minecraft:lightning_bolt by @a[tag=bm.r53me,limit=1]', 'particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.3 20'])
    fn('p53/shock', ['damage @s 3 minecraft:lightning_bolt by @a[tag=bm.r53me,limit=1]', 'particle minecraft:electric_spark ~ ~1 ~ 0.3 0.5 0.3 0.2 12'])
    wjson('bm/advancement/p53/guard_hit.json', {'criteria': {'h': {'trigger': 'minecraft:entity_hurt_player', 'conditions': {'player': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["bm.r53g"]}'}}]}}},
        'rewards': {'function': 'bm:p53/guard_hit'}})
    fn('p53/guard_hit', ['advancement revoke @s only bm:p53/guard_hit', 'tag @s add bm.r53me',
                         'execute if entity @s[tag=bm.r53shell] as @e[type=#bm:p42_foe,distance=..4] at @s run function bm:p53/sand_eyes',
                         'execute if entity @s[tag=bm.r53static] as @e[type=#bm:p42_foe,distance=..4] at @s run function bm:p53/shock_back',
                         'execute if entity @s[tag=bm.r53static] run playsound minecraft:entity.lightning_bolt.impact player @a[distance=..16] ~ ~ ~ 0.6 1.6',
                         'tag @s remove bm.r53me'])
    fn('p53/sand_eyes', ['damage @s 2 bm:sandstorm by @a[tag=bm.r53me,limit=1]', 'effect give @s minecraft:blindness 3 0', 'effect give @s minecraft:slowness 3 1',
                         'particle minecraft:falling_dust{block_state:"minecraft:sand"} ~ ~1.5 ~ 0.3 0.3 0.3 0 15'])
    # a guarded player carries bm.r53g while the guard lasts
    tick.append('tag @a[scores={bm.rst=1..}] add bm.r53g')
    tick.append('tag @a[scores={bm.rst=..0},tag=bm.r53g] remove bm.r53g')
    fn('admin/relics', [give(forms[v][0]) for forms in FAMILIES.values() for v in forms] +
       ['give @s minecraft:blaze_rod 4', 'give @s minecraft:armadillo_scute 4', 'give @s minecraft:breeze_rod 4', give('heartstone', 4)])

    # ================================================================== THE SAND PHARAOH
    fn('p53/sph/summon', [f'summon minecraft:husk ~ ~ ~ {snbt(PHARAOH)}',
                          'execute as @e[type=minecraft:husk,tag=bm.sph_new] run function bm:p53/sph/init', 'tag @e[tag=bm.sph_new] remove bm.sph_new',
                          'execute store result score #sphseen bm.bm run time query gametime',
                          'particle minecraft:falling_dust{block_state:"minecraft:sand"} ~ ~2 ~ 1.5 2 1.5 0 120',
                          'particle minecraft:dust_plume ~ ~1 ~ 1.5 1 1.5 0.05 60', 'particle minecraft:block{block_state:"minecraft:sand"} ~ ~0.2 ~ 1.5 0.1 1.5 0.2 120',
                          'playsound minecraft:block.trial_spawner.ominous_activate hostile @a[distance=..48] ~ ~ ~ 1.5 0.6',
                          'execute as @a[distance=..30,gamemode=!spectator] at @s run function bm:p53/sph/sense'])
    fn('p53/sph/init', ['scoreboard players set @s bm.r53t 0', 'scoreboard players set @s bm.r53x 0', 'bossbar set bm:sph color yellow'])
    fn('p53/sph/sense', ['tag @s add bm.sphsensed', 'title @s times 10 70 30', title('@s', 'subtitle', T('The wind turns to sand... something ancient wakes.', GOLD, italic=True)),
                         title('@s', 'title', T('', GOLD)), 'playsound minecraft:ambient.cave ambient @s ~ ~ ~ 1 0.6',
                         'playsound minecraft:entity.husk.converted_to_zombie hostile @s ~ ~ ~ 0.6 0.5',
                         # his song: "Relic", over any other music
                         'stopsound @s music', 'stopsound @s record', 'playsound minecraft:music_disc.relic record @s ~ ~ ~ 1 1 1'])
    fn('p53/sph/second', ['execute store result score #sphseen bm.bm run time query gametime',
                          'execute unless score #tod bm.bm matches 0..12499 run return run function bm:p53/sph/retreat',
                          f'execute if entity @a[distance=..128,{NEAR}] run scoreboard players set @s bm.r53x 0',
                          f'execute unless entity @a[distance=..128,{NEAR}] run scoreboard players add @s bm.r53x 1',
                          'execute if score @s bm.r53x matches 90.. run return run function bm:p53/sph/retreat',
                          'execute as @a[distance=..30,tag=!bm.sphsensed,gamemode=!spectator] at @s run function bm:p53/sph/sense',
                          'stopsound @a[tag=bm.sphsensed] music',
                          'bossbar set bm:sph players @a[distance=..64]', 'bossbar set bm:sph visible true',
                          'execute store result bossbar bm:sph value run data get entity @s Health',
                          'execute store result score #hh bm.rng run data get entity @s Health',
                          f'execute if score #hh bm.rng matches ..{PH_HP // 2} unless entity @s[tag=bm.sph_rage] run function bm:p53/sph/enrage',
                          'function bm:p53/sph/ambience',
                          f'execute unless entity @a[distance=..24,{NEAR}] run return 0',
                          'scoreboard players add @s bm.r53t 1',
                          'execute if score @s bm.r53t matches 3 run function bm:p53/sph/scarabs',
                          'execute if score @s bm.r53t matches 6 run function bm:p53/sph/sandblind',
                          'execute if score @s bm.r53t matches 9 run function bm:p53/sph/guards',
                          'execute if score @s bm.r53t matches 12 run function bm:p53/sph/sunray',
                          'execute if score @s bm.r53t matches 14 if entity @s[tag=bm.sph_rage] run function bm:p53/sph/eruption',
                          'execute if score @s bm.r53t matches 15 run function bm:p53/sph/sunray',
                          'execute if score @s bm.r53t matches 16.. run scoreboard players set @s bm.r53t 0'])
    # the sandstorm: blowing sand and dust around everyone near him
    fn('p53/sph/fast', ['particle minecraft:falling_dust{block_state:"minecraft:sand"} ~ ~2.6 ~ 0.4 0.4 0.4 0 2',
                        'particle minecraft:dust_plume ~ ~0.3 ~ 0.6 0.1 0.6 0.02 2',
                        'execute anchored eyes positioned ^ ^ ^0.35 run particle minecraft:dust{color:[0.3,0.9,1.0],scale:0.6} ~ ~ ~ 0.12 0.02 0.02 0 2',
                        'execute as @a[distance=..48] at @s run function bm:p53/sph/storm'])
    fn('p53/sph/storm', ['particle minecraft:falling_dust{block_state:"minecraft:sand"} ~ ~3 ~ 9 3 9 0 30 normal @s',
                         'particle minecraft:dust{color:[0.86,0.75,0.5],scale:2.5} ~ ~1.5 ~ 9 2 9 0 18 normal @s',
                         'particle minecraft:dust_plume ~ ~0.5 ~ 7 0.5 7 0.02 6 normal @s',
                         'execute if entity @e[type=minecraft:husk,tag=bm.sph_rage,distance=..48] run particle minecraft:dust{color:[0.8,0.66,0.4],scale:3.5} ~ ~1.5 ~ 5 2 5 0 25 normal @s'])
    fn('p53/sph/ambience', ['execute store result score #r bm.rng run random value 1..12',
                            'execute if score #r bm.rng matches 1 run playsound minecraft:entity.husk.ambient hostile @a[distance=..48] ~ ~ ~ 1.5 0.5',
                            'execute if score #r bm.rng matches 2 as @a[distance=..48] at @s run playsound minecraft:entity.breeze.idle_air ambient @s ~ ~ ~ 1 0.5',
                            'execute if score #r bm.rng matches 3 as @a[distance=..48] at @s run playsound minecraft:item.brush.brushing.sand ambient @s ~ ~ ~ 1.2 0.5',
                            'execute if score #r bm.rng matches 4 run playsound minecraft:entity.camel.ambient hostile @a[distance=..48] ~ ~ ~ 0.8 0.5',
                            'execute if score #r bm.rng matches 5 as @a[distance=..48] at @s run playsound minecraft:weather.rain.above ambient @s ~ ~ ~ 0.5 0.5',
                            'execute if score #r bm.rng matches 6 run playsound minecraft:entity.elder_guardian.curse hostile @a[distance=..40] ~ ~ ~ 0.3 0.6',
                            'execute if score #r bm.rng matches 7 as @a[distance=..40] at @s run playsound minecraft:ambient.cave ambient @s ~ ~ ~ 0.6 0.6',
                            'execute if score #r bm.rng matches 8 run playsound minecraft:entity.silverfish.ambient hostile @a[distance=..24] ~ ~ ~ 1 0.5'])
    # scarabs pour from his wraps (at most 8 near him)
    fn('p53/sph/scarabs', ['execute store result score #mc bm.rng if entity @e[type=minecraft:endermite,tag=bm.scarab,distance=..40]',
                           'execute if score #mc bm.rng matches 8.. run return 0',
                           'playsound minecraft:entity.silverfish.ambient hostile @a[distance=..32] ~ ~ ~ 2 0.5',
                           'particle minecraft:dust{color:[0.12,0.18,0.14],scale:1.0} ~ ~1 ~ 1 1 1 0 40'] +
       [f'execute rotated ~ 0 positioned ^{x} ^ ^1 if block ~ ~ ~ #bm:grap_pass run summon minecraft:endermite ~ ~ ~ {snbt(SCARAB)}' for x in (-1, 0, 1)])
    # sand in everyone's eyes
    fn('p53/sph/sandblind', ['playsound minecraft:entity.breeze.wind_burst hostile @a[distance=..32] ~ ~ ~ 1.5 0.5',
                             'playsound minecraft:item.brush.brushing.sand hostile @a[distance=..32] ~ ~ ~ 2 0.5',
                             'tag @s add bm.sphme', f'execute as @a[distance=..14,{NEAR}] at @s run function bm:p53/sph/blind', 'tag @s remove bm.sphme'])
    fn('p53/sph/blind', ['effect give @s minecraft:blindness 3 0', 'effect give @s minecraft:slowness 3 0',
                         'damage @s 3 bm:sandstorm by @e[type=minecraft:husk,tag=bm.sphme,limit=1]',
                         'particle minecraft:falling_dust{block_state:"minecraft:sand"} ~ ~1.6 ~ 0.5 0.5 0.5 0 30'])
    # Tomb Guards (at most 4 near him)
    fn('p53/sph/guards', ['execute store result score #mc bm.rng if entity @e[type=minecraft:husk,tag=bm.sphmin,distance=..40]',
                          'execute if score #mc bm.rng matches 4.. run return 0',
                          'playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..32] ~ ~ ~ 1.5 0.5',
                          'execute rotated ~ 0 positioned ^2.5 ^ ^-1 run function bm:p53/sph/guard', 'execute rotated ~ 0 positioned ^-2.5 ^ ^-1 run function bm:p53/sph/guard'])
    fn('p53/sph/guard', ['execute unless block ~ ~ ~ #bm:grap_pass run return 0', 'execute unless block ~ ~1 ~ #bm:grap_pass run return 0',
                         f'summon minecraft:husk ~ ~ ~ {snbt(GUARD)}', 'particle minecraft:block{block_state:"minecraft:sand"} ~ ~0.3 ~ 0.5 0.3 0.5 0.1 40'])
    # a beam of the sun from his eyes at the nearest player
    fn('p53/sph/sunray', [f'execute unless entity @a[distance=..20,{NEAR}] run return 0', 'tag @s add bm.sphme', 'scoreboard players set #k bm.rng 0',
                          'playsound minecraft:block.beacon.power_select hostile @a[distance=..32] ~ ~ ~ 1.5 0.6',
                          f'execute anchored eyes positioned ^ ^ ^0.5 facing entity @p[distance=..20,{NEAR}] eyes run function bm:p53/sph/ray',
                          'tag @s remove bm.sphme', 'tag @a[tag=bm.sphhit] remove bm.sphhit'])
    fn('p53/sph/ray', ['scoreboard players add #k bm.rng 1', 'execute unless block ~ ~ ~ #bm:grap_pass run return 0',
                       'particle minecraft:dust{color:[1.0,0.85,0.3],scale:1.3} ~ ~ ~ 0.05 0.05 0.05 0 2', 'particle minecraft:end_rod ~ ~ ~ 0 0 0 0 1',
                       f'execute positioned ~ ~-1 ~ as @a[distance=..1.5,tag=!bm.sphhit,{NEAR}] at @s run function bm:p53/sph/burn',
                       'execute if score #k bm.rng matches 40.. run return 0', 'execute positioned ^ ^ ^0.6 run function bm:p53/sph/ray'])
    fn('p53/sph/burn', ['tag @s add bm.sphhit', 'damage @s 6 bm:sunbeam by @e[type=minecraft:husk,tag=bm.sphme,limit=1]',
                        'execute unless predicate bm:p42/burning if block ~ ~ ~ #minecraft:air run function bm:p42/fx/flicker'])
    # enraged: the sand bursts up under everyone near
    fn('p53/sph/eruption', ['playsound minecraft:entity.ravager.roar hostile @a[distance=..32] ~ ~ ~ 1 0.6', 'tag @s add bm.sphme',
                            f'execute as @a[distance=..10,{NEAR}] at @s run function bm:p53/sph/erupt', 'tag @s remove bm.sphme'])
    fn('p53/sph/erupt', ['damage @s 5 bm:sandstorm by @e[type=minecraft:husk,tag=bm.sphme,limit=1]', 'effect give @s minecraft:levitation 1 6 true',
                         'particle minecraft:block{block_state:"minecraft:sand"} ~ ~0.3 ~ 0.6 0.3 0.6 0.3 60', 'particle minecraft:dust_plume ~ ~0.5 ~ 0.4 0.8 0.4 0.05 20'])
    fn('p53/sph/enrage', ['tag @s add bm.sph_rage', 'effect give @s minecraft:strength infinite 0 true',
                          'attribute @s minecraft:movement_speed modifier add bm:sph_rage 0.25 add_multiplied_base', 'bossbar set bm:sph color red',
                          title('@a[distance=..48]', 'actionbar', T('The sandstorm thickens around the Pharaoh!', GOLD, bold=True)),
                          'playsound minecraft:entity.ravager.roar hostile @a[distance=..48] ~ ~ ~ 1.5 0.5',
                          'particle minecraft:dust_plume ~ ~1.5 ~ 1.5 1.5 1.5 0.1 80', 'function bm:p53/sph/guards'])
    fn('p53/sph/retreat', [title('@a[distance=..64]', 'actionbar', T('The Sand Pharaoh sinks back beneath the dunes...', GOLD, italic=True)),
                           'playsound minecraft:block.sand.break hostile @a[distance=..64] ~ ~ ~ 2 0.4',
                           'particle minecraft:block{block_state:"minecraft:sand"} ~ ~0.5 ~ 1 0.5 1 0.2 120',
                           'function bm:p53/sph/cleanup', 'tp @s ~ -400 ~', 'kill @s'])
    fn('p53/sph/cleanup', ['stopsound @a[tag=bm.sphsensed] record minecraft:music_disc.relic',
                           'execute as @e[tag=bm.sphmin,distance=..96] at @s run function bm:p42/boss/crumble',
                           'tag @a remove bm.sphsensed', 'bossbar set bm:sph visible false'])
    wjson('bm/loot_table/p53/pharaoh.json', {'type': 'minecraft:entity', 'pools': [
        {'rolls': 1, 'entries': [G.loot_entry('pharaoh_crook')], 'conditions': [G.KILLED]},
        {'rolls': 1, 'entries': [G.loot_entry('token', G.uni(10, 16))], 'conditions': [G.KILLED]},
        {'rolls': 1, 'entries': [G.loot_entry('medallion', G.uni(2, 4))], 'conditions': [G.KILLED]},
        {'rolls': 1, 'entries': [G.loot_entry('trophy')], 'conditions': [G.KILLED, G.chance(0.4)]},
        {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:gold_ingot', 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(4, 9)}]}]},
        {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:lapis_lazuli', 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(6, 14)}]}]},
        {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:armadillo_scute', 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(1, 3)}]}],
         'conditions': [G.KILLED]}]})

    # ================================================================== THE STORM ROC
    fn('p53/roc/summon', [f'summon minecraft:phantom ~ ~ ~ {snbt(ROC)}'] +
       ['execute as @e[type=minecraft:phantom,tag=bm.roc_new] run function bm:p53/roc/init', 'tag @e[tag=bm.roc_new] remove bm.roc_new',
        'execute store result score #rocseen bm.bm run time query gametime',
        'function bm:p53/bolt', 'particle minecraft:cloud ~ ~1 ~ 2 1 2 0.05 60', 'particle minecraft:electric_spark ~ ~1 ~ 2 1 2 0.3 60',
        'playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..64] ~ ~ ~ 1 1.6',
        'execute as @a[distance=..40,gamemode=!spectator] at @s run function bm:p53/roc/sense'])
    # (it circles its anchor until it has a target: here, over where it came down)
    fn('p53/roc/init', ['scoreboard players set @s bm.r53t 0', 'scoreboard players set @s bm.r53x 0', 'scoreboard players set @s bm.rfx 0', 'bossbar set bm:roc color blue',
                        ] +
       [f'execute store result entity @s anchor_pos[{i}] int 1 run data get entity @s Pos[{i}]' for i in range(3)])
    fn('p53/roc/sense', ['tag @s add bm.rocsensed', 'title @s times 10 70 30', title('@s', 'subtitle', T('Thunder rolls... something vast circles above.', STORM, italic=True)),
                         title('@s', 'title', T('', STORM)), 'playsound minecraft:entity.lightning_bolt.thunder weather @s ~ ~ ~ 1 0.5',
                         'playsound minecraft:entity.phantom.ambient hostile @s ~ ~ ~ 1 0.4',
                         # its song: "Precipice", over any other music
                         'stopsound @s music', 'stopsound @s record', 'playsound minecraft:music_disc.precipice record @s ~ ~ ~ 1 1 1'])
    fn('p53/roc/fast', ['particle minecraft:electric_spark ~ ~1 ~ 2.5 0.6 2.5 0.1 4', 'particle minecraft:cloud ~ ~0.8 ~ 2 0.3 2 0.01 2',
                        'execute if entity @s[tag=bm.roc_rage] run particle minecraft:electric_spark ~ ~1 ~ 3 1 3 0.3 6'])
    fn('p53/roc/second', ['execute store result score #rocseen bm.bm run time query gametime',
                          # (the storm has to be over for 10 s: a thunderstorm takes a moment to build and to clear)
                          'execute if predicate bm:p53/thunder run scoreboard players set @s bm.rfx 0',
                          'execute unless predicate bm:p53/thunder run scoreboard players add @s bm.rfx 1',
                          'execute if score @s bm.rfx matches 10.. run return run function bm:p53/roc/retreat',
                          f'execute if entity @a[distance=..128,{NEAR}] run scoreboard players set @s bm.r53x 0',
                          f'execute unless entity @a[distance=..128,{NEAR}] run scoreboard players add @s bm.r53x 1',
                          'execute if score @s bm.r53x matches 90.. run return run function bm:p53/roc/retreat',
                          'execute as @a[distance=..40,tag=!bm.rocsensed,gamemode=!spectator] at @s run function bm:p53/roc/sense',
                          'stopsound @a[tag=bm.rocsensed] music',
                          'bossbar set bm:roc players @a[distance=..80]', 'bossbar set bm:roc visible true',
                          'execute store result bossbar bm:roc value run data get entity @s Health',
                          'execute store result score #hh bm.rng run data get entity @s Health',
                          f'execute if score #hh bm.rng matches ..{ROC_HP // 2} unless entity @s[tag=bm.roc_rage] run function bm:p53/roc/enrage',
                          'function bm:p53/roc/ambience',
                          f'execute unless entity @a[distance=..40,{NEAR}] run return 0',
                          'scoreboard players add @s bm.r53t 1',
                          'execute if score @s bm.r53t matches 4 run function bm:p53/roc/call',
                          'execute if score @s bm.r53t matches 8 run function bm:p53/roc/gust',
                          'execute if score @s bm.r53t matches 12 run function bm:p53/roc/call',
                          'execute if score @s bm.r53t matches 14 if entity @s[tag=bm.roc_rage] run function bm:p53/roc/call',
                          'execute if score @s bm.r53t matches 15 if entity @s[tag=bm.roc_rage] run function bm:p53/roc/stormlings',
                          'execute if score @s bm.r53t matches 16.. run scoreboard players set @s bm.r53t 0'])
    fn('p53/roc/ambience', ['execute store result score #r bm.rng run random value 1..10',
                            'execute if score #r bm.rng matches 1 as @a[distance=..64] at @s run playsound minecraft:entity.lightning_bolt.thunder weather @s ~ ~ ~ 0.5 0.6',
                            'execute if score #r bm.rng matches 2 run playsound minecraft:entity.phantom.ambient hostile @a[distance=..64] ~ ~ ~ 2 0.4',
                            'execute if score #r bm.rng matches 3 as @a[distance=..64] at @s run playsound minecraft:entity.breeze.idle_air ambient @s ~ ~ ~ 1 0.6',
                            'execute if score #r bm.rng matches 4 run playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..64] ~ ~ ~ 0.6 1.8',
                            'execute if score #r bm.rng matches 5 as @a[distance=..64] at @s run playsound minecraft:item.elytra.flying ambient @s ~ ~ ~ 0.4 0.6',
                            'execute if score #r bm.rng matches 6 as @a[distance=..40] at @s run playsound minecraft:ambient.cave ambient @s ~ ~ ~ 0.5 1.2'])
    # lightning: sparks gather over a player's head for a second, then the bolt falls
    fn('p53/roc/call', ['playsound minecraft:item.trident.thunder hostile @a[distance=..48] ~ ~ ~ 0.6 0.5',
                        f'execute as @a[distance=..40,{NEAR},sort=random,limit=1] at @s run summon minecraft:marker ~ ~ ~ {{Tags:["bm.rocbolt"]}}',
                        f'execute if entity @s[tag=bm.roc_rage] as @a[distance=..40,{NEAR},sort=random,limit=1] at @s positioned ~2 ~ ~ run summon minecraft:marker ~ ~ ~ {{Tags:["bm.rocbolt"]}}',
                        'scoreboard players set @e[type=minecraft:marker,tag=bm.rocbolt,distance=..64] bm.rfx 20'])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.rocbolt] at @s run function bm:p53/roc/bolt_tick')
    fn('p53/roc/bolt_tick', ['scoreboard players remove @s bm.rfx 1', *ring(1.5, 8, 0.1, 'minecraft:electric_spark'),
                             'particle minecraft:electric_spark ~ ~3 ~ 0.4 0.4 0.4 0.1 3',
                             'execute if score @s bm.rfx matches 0 run function bm:p53/roc/strike', 'execute if score @s bm.rfx matches ..0 run kill @s'])
    fn('p53/roc/strike', ['function bm:p53/bolt', f'execute as @a[distance=..2.5,{NEAR}] run damage @s 7 minecraft:lightning_bolt by @e[type=minecraft:phantom,tag=bm.roc,limit=1]'])
    # a gust of wind under everyone near (it throws them)
    fn('p53/roc/gust', ['playsound minecraft:entity.breeze.wind_burst hostile @a[distance=..48] ~ ~ ~ 2 0.5',
                        f'execute as @a[distance=..16,{NEAR}] at @s run summon minecraft:breeze_wind_charge ~ ~0.3 ~ {{Motion:[0.0d,-1.0d,0.0d]}}'])
    fn('p53/roc/stormlings', ['execute store result score #mc bm.rng if entity @e[type=minecraft:phantom,tag=bm.rocmin,distance=..64]',
                              'execute if score #mc bm.rng matches 4.. run return 0', 'playsound minecraft:entity.phantom.swoop hostile @a[distance=..48] ~ ~ ~ 1.5 0.6',
                              f'execute rotated ~ 0 run summon minecraft:phantom ^2 ^ ^-2 {snbt(STORMLING)}', f'execute rotated ~ 0 run summon minecraft:phantom ^-2 ^ ^-2 {snbt(STORMLING)}'])
    fn('p53/roc/enrage', ['tag @s add bm.roc_rage', 'effect give @s minecraft:strength infinite 0 true', 'bossbar set bm:roc color red',
                          title('@a[distance=..64]', 'actionbar', T('The Storm Roc shrieks - the storm answers!', STORM, bold=True)),
                          'playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..64] ~ ~ ~ 2 1.2',
                          'function bm:p53/bolt', 'function bm:p53/roc/stormlings'])
    fn('p53/roc/retreat', [title('@a[distance=..80]', 'actionbar', T('The Storm Roc rises back into the clouds...', STORM, italic=True)),
                           'playsound minecraft:entity.phantom.flap hostile @a[distance=..64] ~ ~ ~ 2 0.4', 'particle minecraft:cloud ~ ~1 ~ 2 1 2 0.05 60',
                           'function bm:p53/roc/cleanup', 'tp @s ~ -400 ~', 'kill @s'])
    fn('p53/roc/cleanup', ['stopsound @a[tag=bm.rocsensed] record minecraft:music_disc.precipice',
                           'execute as @e[type=minecraft:phantom,tag=bm.rocmin,distance=..128] at @s run function bm:p42/boss/crumble',
                           'kill @e[type=minecraft:marker,tag=bm.rocbolt]', 'tag @a remove bm.rocsensed', 'bossbar set bm:roc visible false'])
    wjson('bm/loot_table/p53/roc.json', {'type': 'minecraft:entity', 'pools': [
        {'rolls': 1, 'entries': [G.loot_entry('storm_talon')], 'conditions': [G.KILLED]},
        {'rolls': 1, 'entries': [G.loot_entry('token', G.uni(10, 16))], 'conditions': [G.KILLED]},
        {'rolls': 1, 'entries': [G.loot_entry('medallion', G.uni(2, 4))], 'conditions': [G.KILLED]},
        {'rolls': 1, 'entries': [G.loot_entry('trophy')], 'conditions': [G.KILLED, G.chance(0.4)]},
        {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:feather', 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(6, 14)}]}]},
        {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:phantom_membrane', 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(2, 5)}]}]},
        {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:breeze_rod', 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(1, 3)}]}],
         'conditions': [G.KILLED]}]})

    # ================================================================== falls, WANTED, achievements
    for key, tag, name, col, sub, hdr in [('sph', 'bm.sph', 'The Sand Pharaoh', GOLD, '...the sands will remember.', 'THE PHARAOH FALLS'),
                                          ('roc', 'bm.roc', 'The Storm Roc', STORM, '...and the storm breaks.', 'THE ROC FALLS'),
                                          ('hhm', 'bm.hhm', None, None, None, None)]:
        wjson(f'bm/advancement/p53/slain_{key}.json', {'criteria': {'slain': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [
            {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["%s"]}' % tag}}]}}},
            'rewards': {'function': f'bm:p53/slain_{key}'}})
        lines = [f'advancement revoke @s only bm:p53/slain_{key}', 'function bm:p53/wanted']
        if name:
            lines += [tellraw('@a[distance=..160]', PREFIX + [T(name + ' has fallen to ', col), {'selector': '@s', 'color': 'gold'}, T('!', col)]),
                      f'function bm:p53/{key}/cleanup', 'title @a[distance=..64] times 10 70 20',
                      title('@a[distance=..64]', 'subtitle', T(sub, 'gray', italic=True)), title('@a[distance=..64]', 'title', T(hdr, col, bold=True)),
                      'execute as @a[distance=..64] at @s run playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1',
                      'summon minecraft:experience_orb ~ ~1 ~ {Value:60s}', 'summon minecraft:experience_orb ~ ~1 ~ {Value:60s}',
                      'summon minecraft:experience_orb ~ ~1 ~ {Value:60s}']
        fn(f'p53/slain_{key}', lines)
    fn('p53/wanted', [give('token', 8), give('medallion', 2), 'title @s times 10 50 20',
                      title('@s', 'actionbar', [T('WANTED bounty collected: ', '#ff5a3c', bold=True), T('8 Tokens + 2 Medallions', 'gold')]),
                      'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1 0.8'])
    adv = lambda key, parent, ico, ttl, desc, crit, frame: wjson(f'bm/advancement/story/{key}.json', {
        'parent': f'bm:story/{parent}', 'criteria': crit,
        'display': {'icon': ({'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': f'bm:{ico}'}} if ':' not in ico else {'id': ico}),
                    'title': T(ttl, 'gold' if frame == 'challenge' else 'yellow'), 'description': T(desc, 'gray'),
                    'frame': frame, 'show_toast': True, 'announce_to_chat': True, 'hidden': False}})
    kill = lambda tag: {'slain': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["%s"]}' % tag}}]}}}
    adv('pharaoh', 'root', 'minecraft:sandstone', 'Curse of the Pharaoh', 'Slay the Sand Pharaoh', kill('bm.sph'), 'challenge')
    adv('storm_roc', 'root', 'minecraft:feather', 'Eye of the Storm', 'Slay the Storm Roc', kill('bm.roc'), 'challenge')
    adv('relic_hunter', 'pharaoh', 'pharaoh_crook', 'Relic Hunter', "Hold the Horseman's Head, the Pharaoh's Crook and the Thunderbird Talon",
        {'head': {'trigger': 'minecraft:inventory_changed', 'conditions': {'items': [{'items': 'minecraft:totem_of_undying',
                                                                                     'predicates': {'minecraft:custom_data': '{bm_head:1b}'}}]}},
         'crook': {'trigger': 'minecraft:inventory_changed', 'conditions': {'items': [{'items': 'minecraft:totem_of_undying',
                                                                                      'predicates': {'minecraft:custom_data': '{rf:"crook"}'}}]}},
         'talon': {'trigger': 'minecraft:inventory_changed', 'conditions': {'items': [{'items': 'minecraft:totem_of_undying',
                                                                                      'predicates': {'minecraft:custom_data': '{rf:"talon"}'}}]}}}, 'challenge')
    adv('monster_slayer', 'storm_roc', 'minecraft:netherite_sword', 'Monster Slayer', 'Slay the Headless Horseman, the Sand Pharaoh and the Storm Roc',
        {'hhm': kill('bm.hhm')['slain'], 'sph': kill('bm.sph')['slain'], 'roc': kill('bm.roc')['slain']}, 'challenge')

    # ================================================================== when they come
    fn('p53/sph/check', ['scoreboard players set #sphchk bm.bm 0',
                         'execute unless score #tod bm.bm matches 0..10999 run return 0',
                         f'execute if score #day bm.bm matches ..{GRACE_DAYS - 1} run return 0',
                         'execute if entity @e[type=minecraft:husk,tag=bm.sph] run return 0',
                         'execute store result score #now bm.rng run time query gametime',
                         'scoreboard players operation #gap bm.rng = #now bm.rng', 'scoreboard players operation #gap bm.rng -= #sphseen bm.bm',
                         'execute if score #sphseen bm.bm matches 1.. if score #gap bm.rng matches 0..2399 run return 0',
                         f'execute store result score #r bm.rng run random value 1..{PH_ODDS}', 'execute unless score #r bm.rng matches 1 run return 0',
                         f'execute in minecraft:overworld as @a[distance=0..,{NEAR},predicate=bm:p53/desert,sort=random,limit=1] at @s run function bm:p53/sph/try'])
    fn('p53/sph/try', ['execute positioned ~ ~1.6 ~ unless predicate bm:sees_sky run return 0',
                       'execute store result storage bm:tmp p53s.a int 1 run random value 0..359', 'function bm:p53/sph/at with storage bm:tmp p53s'])
    fn('p53/sph/at', ['$execute rotated $(a) 0 positioned ^ ^ ^20 positioned over motion_blocking_no_leaves run function bm:p53/sph/place'])
    fn('p53/sph/place', ['execute if block ~ ~-1 ~ minecraft:water run return 0', 'execute if block ~ ~-1 ~ minecraft:lava run return 0'] +
       [f'execute unless block ~ ~{y} ~ #bm:grap_pass run return 0' for y in range(4)] +
       ['execute if block ~ ~ ~ minecraft:water run return 0', 'execute unless function bm:p37/allowed run return 0', 'function bm:p53/sph/summon'])
    fn('p53/roc/check', ['scoreboard players set #rocchk bm.bm 0',
                         f'execute if score #day bm.bm matches ..{GRACE_DAYS - 1} run return 0',
                         'execute unless predicate bm:p53/thunder run return 0',
                         'execute if entity @e[type=minecraft:phantom,tag=bm.roc] run return 0',
                         'execute store result score #now bm.rng run time query gametime',
                         'scoreboard players operation #gap bm.rng = #now bm.rng', 'scoreboard players operation #gap bm.rng -= #rocseen bm.bm',
                         'execute if score #rocseen bm.bm matches 1.. if score #gap bm.rng matches 0..2399 run return 0',
                         f'execute store result score #r bm.rng run random value 1..{ROC_ODDS}', 'execute unless score #r bm.rng matches 1 run return 0',
                         f'execute in minecraft:overworld as @a[distance=0..,{NEAR},sort=random,limit=1] at @s run function bm:p53/roc/try'])
    fn('p53/roc/try', ['execute positioned ~ ~1.6 ~ unless predicate bm:sees_sky run return 0',
                       'execute store result storage bm:tmp p53s.a int 1 run random value 0..359', 'function bm:p53/roc/at with storage bm:tmp p53s'])
    fn('p53/roc/at', ['$execute rotated $(a) 0 positioned ^ ^ ^28 positioned over motion_blocking positioned ~ ~16 ~ run function bm:p53/roc/place'])
    fn('p53/roc/place', ['execute unless block ~ ~ ~ #bm:grap_pass run return 0', 'execute unless function bm:p37/allowed run return 0', 'function bm:p53/roc/summon'])

    # ---------------- the clock
    second += ['execute as @e[type=minecraft:husk,tag=bm.sph] at @s run function bm:p53/sph/second',
               'execute unless entity @e[type=minecraft:husk,tag=bm.sph] run bossbar set bm:sph visible false',
               'execute as @e[type=minecraft:phantom,tag=bm.roc] at @s run function bm:p53/roc/second',
               'execute unless entity @e[type=minecraft:phantom,tag=bm.roc] run bossbar set bm:roc visible false',
               'scoreboard players add #sphchk bm.bm 1', 'execute if score #sphchk bm.bm matches 20.. run function bm:p53/sph/check',
               'scoreboard players add #rocchk bm.bm 1', 'execute if score #rocchk bm.bm matches 20.. run function bm:p53/roc/check',
               # orphaned minions (their master gone a while) crumble
               'execute unless entity @e[type=minecraft:husk,tag=bm.sph] as @e[type=minecraft:husk,tag=bm.sphmin] at @s run function bm:p42/boss/crumble',
               'execute unless entity @e[type=minecraft:phantom,tag=bm.roc] as @e[type=minecraft:phantom,tag=bm.rocmin] at @s run function bm:p42/boss/crumble',
               # the Bounty Board picks up its WANTED posters once
               'execute as @e[type=minecraft:text_display,tag=bm.bboard,tag=!bm.b53] run function bm:p53/board',
               'kill @e[type=minecraft:item_display,tag=bm.rig53]']
    fn('p53/board', ['tag @s add bm.b53', 'scoreboard players set @s bm.bst -1'])
    fast += ['execute as @e[type=minecraft:husk,tag=bm.sph] at @s run function bm:p53/sph/fast',
             'execute as @e[type=minecraft:phantom,tag=bm.roc] at @s run function bm:p53/roc/fast']

    # ---------------- admin
    fn('admin/pharaoh', ['execute rotated ~ 0 positioned ^ ^ ^10 positioned over motion_blocking_no_leaves run function bm:p53/sph/summon',
                         tellraw('@s', PREFIX + [T('The Sand Pharaoh rises 10 blocks ahead. He sinks away at dusk.', 'gray')])])
    fn('admin/storm_roc', ['execute rotated ~ 0 positioned ^ ^ ^12 positioned over motion_blocking positioned ~ ~8 ~ run function bm:p53/roc/summon',
                           tellraw('@s', PREFIX + [T('The Storm Roc comes down 12 blocks ahead. It leaves when the thunder stops', 'gray'),
                                                   T(' (/weather thunder keeps it).', 'dark_gray')])])

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


# ===================================================================== resource pack: the Pharaoh, the Roc, the relics
def _hex(c):
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


def rp(R):
    import sys
    from PIL import Image, ImageDraw
    # the relics' icons, drawn like tools (handle bottom-left)
    def crook(gem):
        im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
        G_, B_, D_ = _hex('#e8b923'), _hex('#1f3fa8'), _hex('#7a5a10')
        staff = [(2 + i, 14 - i) for i in range(10)]
        for i, (x, y) in enumerate(staff):
            im.putpixel((x, y), (G_ if (i // 2) % 2 == 0 else B_) + (255,))
            if x + 1 < 16: im.putpixel((x + 1, y), D_ + (255,))
        for x, y in [(12, 4), (12, 3), (12, 2), (11, 1), (10, 1), (9, 1), (8, 2), (8, 3), (13, 3), (13, 2), (12, 1), (11, 0), (10, 0)]:
            im.putpixel((x, y), G_ + (255,))
        for x, y in [(10, 6), (11, 6), (10, 5)]:
            im.putpixel((x, y), _hex(gem) + (255,))
        return im
    def talon(gem):
        im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rectangle((1, 12, 4, 15), fill=_hex('#4a4038') + (255,))
        d.line((3, 12, 8, 7), fill=_hex('#3d4a63') + (255,), width=3)
        for (x0, y0, x1, y1) in [(8, 7, 13, 2), (9, 8, 15, 6), (7, 6, 9, 1)]:
            d.line((x0, y0, x1, y1), fill=_hex('#efe6cf') + (255,), width=1)
        for (x, y) in [(13, 2), (15, 6), (9, 1)]:
            im.putpixel((x, y), _hex('#ffffff') + (255,))
        for (x, y) in [(6, 9), (7, 8), (5, 10)]:
            im.putpixel((x, y), _hex(gem) + (255,))
        return im
    for fam, forms in FAMILIES.items():
        for v, (iid, name, col, *_r) in forms.items():
            R.ICONS[iid] = crook(col) if fam == 'crook' else talon(col)
            R.HANDHELD_EXTRA.add(iid)
    R.LANG.update({'death.attack.bm.scarab': '%1$s was devoured by scarabs', 'death.attack.bm.scarab.player': '%1$s was devoured by %2$s\'s scarabs',
                   'death.attack.bm.sunbeam': '%1$s was burned by the sun', 'death.attack.bm.sunbeam.player': '%1$s was burned by %2$s\'s sunbeam',
                   'death.attack.bm.sandstorm': '%1$s was scoured by the sand', 'death.attack.bm.sandstorm.player': '%1$s was scoured by %2$s\'s sandstorm'})

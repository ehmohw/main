"""Phase 2.33: three more roaming bosses (vanilla bodies, scaled up) and their relics.

THE ELDER TREANT - the forest night
- After day 10, rarely, at night in a forest, a towering Creaking (seven blocks tall, 340 health) walks out of the trees about
  20 blocks from someone under the sky: "The trees lean closer... something old is walking."
- Like every creaking it freezes while you look at it - but its magic doesn't: roots that pin you in place, thrown logs,
  Twigs (little creakings) and, at half health, bursts of brambles while it draws life back from the forest.
- It leaves at dawn. Drops the HEARTWOOD BRANCH 1 time in 10.

THE MAGMA COLOSSUS - the Nether
- After day 10, now and then in the Nether Wastes or Basalt Deltas, a gigantic Magma Cube (over four blocks wide, 420 health)
  heaves up near you: "The ground shakes... something molten rises."
- Ground slams, thrown magma boulders and lava geysers under your feet; it sheds Magma Spawn as it's hurt, and when it
  dies it bursts apart into smaller cubes. Drops the MOLTEN GAUNTLET 1 time in 10.

THE VOIDWALKER - the End
- Out on the End's outer islands (700+ blocks from the centre), rarely, an Enderman over seven blocks tall (450 health)
  steps out of nowhere: "The stars go out... something is watching you."
- It blinks behind you and strikes, fires homing shulker bullets, smothers you in darkness and calls Voidlings
  (endermites). It never carries blocks. Drops the VOID SCEPTER 1 time in 6, and plenty of shulker shells.

THE RELICS - four forms each, turned with the same catalysts (off hand + look straight up + right-click):
  Blaze Rod = OFFENSE, Armadillo Scute = DEFENSE, Breeze Rod = RANGED, Heartstone = SUPPORT.
- Heartwood Branch (stronger in a forest): Thornlash (a thorn whip that heals you), Barkskin (Resistance II +
  Regeneration; attackers are pricked and rooted), Seedcaster (three rooting seeds), Bloomheart (Regeneration II
  for you and your allies, and the crops around you ripen).
- Molten Gauntlet (stronger in the Nether): Volcanic (punches that knock foes flying; an Eruption Punch that blasts
  everything in front of you up and alight), Obsidian (Fire Resistance + Resistance II; attackers burn), Magmashot (a
  magma shot - sets the target alight but never the ground), Hearthfire (Fire Resistance, Regeneration and Absorption
  for you and your allies).
- Void Scepter (stronger in the End): Voidrend (blink to the monster you're looking at and strike it), Phaseguard
  (Resistance II; whoever hits you floats away), Starseeker (three homing shulker bullets), Riftcall (every player within
  32 blocks blinks to your side; Resistance, Regeneration and Slow Falling for all of you).
Each boss pays the Bounty Board's WANTED bounty (8 Tokens + 2 Medallions). Achievements for each, Legendary Hunter for
slaying all six roaming bosses, and Grand Relic Hunter for holding a relic of each."""
from items import attr, T
from nbt import snbt, B, F, D, Int
from phase42 import ring, FIRE_RES, NO_DROP, at
import phase53
from phase53 import MOB, NEAR, define_relics, relic_funcs

GRACE_DAYS = 10
TRT_HP, COL_HP, VWK_HP = 340, 420, 450
TRT_ODDS, COL_ODDS, VWK_ODDS = 250, 150, 40        # 1 in N, every 20 s (a forest night / the Nether's wastes and deltas / the outer End)
OAK, LAVA, VOID = '#6fae3a', '#ff6a1a', '#c27dff'
RESIST = {'id': 'minecraft:resistance', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0)}

FAMILIES = {
    'branch': {1: ('heartwood_branch', 'Thornlash Branch', OAK, 8, [('Right-click: a thorn whip (8 blocks) that', 'blue'),
                                                                     ('slows its victim and heals you.', 'blue')], 40),
               2: ('branch_bark', 'Barkskin Branch', '#8a6a3a', 6, [('Its blows root their victims.', 'gray'), ('Right-click: Barkskin (8 s) - Resistance II and', 'blue'),
                                                                    ('Regeneration; whoever hits you is pricked and', 'blue'), ('rooted. 20 s to recover.', 'blue')], 400),
               3: ('branch_seed', 'Seedcaster Branch', '#b8d84a', 4, [('A light club.', 'gray'), ('Right-click: three seeds that hurt and root', 'blue'),
                                                                      ('whatever they hit (24 blocks).', 'blue')], 30),
               4: ('branch_bloom', 'Bloomheart Branch', '#ff9ad8', 3, [('A poor club.', 'gray'), ('Right-click: Regeneration II for you and every', 'blue'),
                                                                       ('ally within 8 blocks - and the crops around you', 'blue'), ('ripen. 30 s to recover.', 'blue')], 600)},
    'gauntlet': {1: ('molten_gauntlet', 'Volcanic Gauntlet', LAVA, 9, [('Its punches knock foes flying.', 'gray'), ('Right-click: an Eruption Punch blasts everything', 'blue'),
                                                                        ('in front of you up and alight. 4 s to recover.', 'blue')], 80),
                 2: ('gauntlet_obsidian', 'Obsidian Gauntlet', '#5a3a8a', 6, [('Its blows set victims alight.', 'gray'), ('Right-click: Obsidian Guard (8 s) - Fire', 'blue'),
                                                                              ('Resistance and Resistance II; whoever hits you', 'blue'), ('burns. 20 s to recover.', 'blue')], 400),
                 3: ('gauntlet_magma', 'Magmashot Gauntlet', '#ffb43a', 4, [('A light weapon.', 'gray'), ('Right-click: a magma shot (30 blocks) that sets', 'blue'),
                                                                            ('its target alight - never the ground.', 'blue')], 30),
                 4: ('gauntlet_hearth', 'Hearthfire Gauntlet', '#ff8a5a', 3, [('A poor weapon.', 'gray'), ('Right-click: Fire Resistance, Regeneration and', 'blue'),
                                                                              ('Absorption for you and every ally within 8', 'blue'), ('blocks. 30 s to recover.', 'blue')], 600)},
    'scepter': {1: ('void_scepter', 'Voidrend Scepter', VOID, 9, [('Right-click: blink to the monster you are looking', 'blue'),
                                                                  ('at (16 blocks) and strike it. 4 s to recover.', 'blue')], 80),
                2: ('scepter_phase', 'Phaseguard Scepter', '#7ad8ff', 6, [('Right-click: Phaseguard (8 s) - Resistance II;', 'blue'),
                                                                          ('whoever hits you floats away. 20 s to recover.', 'blue')], 400),
                3: ('scepter_star', 'Starseeker Scepter', '#f4f0b0', 4, [('A light weapon.', 'gray'), ('Right-click: three homing shulker bullets at the', 'blue'),
                                                                         ('nearest monsters (24 blocks).', 'blue')], 60),
                4: ('scepter_rift', 'Riftcall Scepter', '#e07dff', 3, [('A poor weapon.', 'gray'), ('Right-click: every player within 32 blocks', 'blue'),
                                                                       ('blinks to your side; Resistance, Regeneration', 'blue'),
                                                                       ('and Slow Falling for all of you. 30 s to recover.', 'blue')], 600)}}
FLAVOUR = {'branch': ("A living branch from the Elder Treant's heart.", ('Stronger in a forest.', 'gold')),
           'gauntlet': ("The Magma Colossus's molten core, made a fist.", ('Stronger in the Nether.', 'gold')),
           'scepter': ("The Voidwalker's eye, set on a rod of the End.", ('Stronger in the End.', 'gold'))}
EDGE = {('branch', 2): 'bark_edge', ('gauntlet', 2): 'obsidian_edge'}
define_relics(FAMILIES, FLAVOUR, EDGE, {('gauntlet', 1): [attr('attack_knockback', 1.5, 'mainhand')]})

# ---------------------------------------------------------------------- the bosses: vanilla bodies, made huge
TREANT = {'Tags': ['bm.seen', 'bm.tiered', 'bm.trt', 'bm.trt_new'], 'PersistenceRequired': B(1),
          'CustomName': T('The Elder Treant', OAK, bold=True), 'Health': F(TRT_HP), 'DeathLootTable': 'bm:p54/treant',
          'attributes': [at('max_health', TRT_HP), at('attack_damage', 10), at('armor', 8), at('follow_range', 48), at('movement_speed', 0.3),
                         at('scale', 2.6), at('knockback_resistance', 1.0), at('step_height', 2.0), at('safe_fall_distance', 40)],
          'active_effects': [RESIST], 'drop_chances': NO_DROP}
TWIG = {'Tags': ['bm.seen', 'bm.tiered', 'bm.trtmin'], 'CustomName': T('Twig', '#8a6a3a'), 'Health': F(14), 'PersistenceRequired': B(1),
        'attributes': [at('max_health', 14), at('attack_damage', 3), at('scale', 0.6), at('follow_range', 32)]}
COLOSSUS = {'Tags': ['bm.seen', 'bm.tiered', 'bm.mcol', 'bm.mcol_new'], 'PersistenceRequired': B(1), 'Size': Int(7),
            'CustomName': T('The Magma Colossus', LAVA, bold=True), 'DeathLootTable': 'bm:p54/colossus', 'active_effects': [RESIST]}
SPAWNLING = {'Tags': ['bm.seen', 'bm.tiered', 'bm.mcolmin'], 'Size': Int(1), 'CustomName': T('Magma Spawn', '#ff9a3a')}
VOIDWALKER = {'Tags': ['bm.seen', 'bm.tiered', 'bm.vwk', 'bm.vwk_new'], 'PersistenceRequired': B(1),
              'CustomName': T('The Voidwalker', VOID, bold=True), 'Health': F(VWK_HP), 'DeathLootTable': 'bm:p54/voidwalker',
              'attributes': [at('max_health', VWK_HP), at('attack_damage', 11), at('armor', 8), at('follow_range', 64), at('movement_speed', 0.32),
                             at('scale', 2.5), at('knockback_resistance', 1.0), at('step_height', 2.0), at('safe_fall_distance', 60)],
              'active_effects': [RESIST], 'drop_chances': NO_DROP}
VOIDLING = {'Tags': ['bm.seen', 'bm.tiered', 'bm.vwkmin'], 'CustomName': T('Voidling', VOID), 'Lifetime': Int(1800), 'Health': F(8),
            'attributes': [at('max_health', 8), at('movement_speed', 0.3)]}
BOSSES = [  # key, entity, tag, name, colour, hp, bossbar colour, music, sense line
    ('trt', 'creaking', 'bm.trt', 'The Elder Treant', OAK, TRT_HP, 'green', 'music_disc.mellohi', 'The trees lean closer... something old is walking.'),
    ('mcol', 'magma_cube', 'bm.mcol', 'The Magma Colossus', LAVA, COL_HP, 'red', 'music_disc.pigstep', 'The ground shakes... something molten rises.'),
    ('vwk', 'enderman', 'bm.vwk', 'The Voidwalker', VOID, VWK_HP, 'purple', 'music_disc.5', 'The stars go out... something is watching you.')]


def generate(G):
    fn, wjson, title, give, tellraw, PREFIX = G.fn, G.wjson, G.title, G.give, G.tellraw, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    tick, fast, second = [], [], []
    G.FUNCS['load'][-1:-1] = [x for key, ent, tag, name, col, hp, bc, *_ in BOSSES for x in (
        f'bossbar add bm:{key} {snbt(T(name, col, bold=True))}', f'bossbar set bm:{key} color {bc}', f'bossbar set bm:{key} style notched_10',
        f'bossbar set bm:{key} max {hp}', f'bossbar set bm:{key} visible false')]
    for key, *_ in BOSSES:
        G.FUNCS['admin/uninstall'].insert(0, f'bossbar remove bm:{key}')
    for name, msg in [('bramble', 'bm.bramble'), ('magma', 'bm.magma'), ('void', 'bm.void')]:
        wjson(f'bm/damage_type/{name}.json', {'exhaustion': 0.1, 'message_id': msg, 'scaling': 'when_caused_by_living_non_player'})
    wjson('bm/predicate/p54/forest.json', {'condition': 'minecraft:location_check', 'predicate': {'biomes': '#minecraft:is_forest'}})
    wjson('bm/predicate/p54/nether_waste.json', {'condition': 'minecraft:location_check',
                                                 'predicate': {'biomes': ['minecraft:nether_wastes', 'minecraft:basalt_deltas']}})
    ench = lambda desc, col, effs: {'anvil_cost': 8, 'description': T(desc, col), 'max_level': 1, 'weight': 1,
                                    'min_cost': {'base': 1, 'per_level_above_first': 0}, 'max_cost': {'base': 1, 'per_level_above_first': 0},
                                    'slots': ['mainhand'], 'supported_items': '#minecraft:enchantable/weapon',
                                    'effects': {'minecraft:post_attack': [dict({'affected': 'victim', 'enchanted': 'attacker'}, **e) for e in effs]}}
    mob_eff = lambda e, s, a: {'type': 'minecraft:apply_mob_effect', 'to_apply': f'minecraft:{e}', 'min_duration': float(s), 'max_duration': float(s),
                               'min_amplifier': float(a), 'max_amplifier': float(a)}
    wjson('bm/enchantment/bark_edge.json', ench('Rooting', '#8a6a3a', [{'effect': mob_eff('slowness', 2, 3)}]))
    wjson('bm/enchantment/obsidian_edge.json', ench('Molten', LAVA, [{'effect': {'type': 'minecraft:ignite', 'duration': 4}}]))

    # ================================================================== the relics
    relic_funcs(G, FAMILIES)
    fn('p53/mood_branch', ['scoreboard players set #rmul bm.rng 10', 'execute if predicate bm:p54/forest run scoreboard players set #rmul bm.rng 15'])
    fn('p53/mood_gauntlet', ['scoreboard players set #rmul bm.rng 10', 'execute if dimension minecraft:the_nether run scoreboard players set #rmul bm.rng 15'])
    fn('p53/mood_scepter', ['scoreboard players set #rmul bm.rng 10', 'execute if dimension minecraft:the_end run scoreboard players set #rmul bm.rng 15'])
    hit = lambda dtype, extra=(): ['tag @s add bm.r53hit', f'$damage @s $(d) {dtype} by @a[tag=bm.r53me,limit=1]'] + list(extra)
    pvp = f'@a[tag=!bm.r53me,tag=!bm.r53hit,tag=!bm.nopvp,{NEAR}'
    body = 'positioned ~ ~-0.9 ~'           # (selectors measure to the feet: test a ray's point a block lower)
    alight = ['execute if entity @s[type=!minecraft:player] run data merge entity @s {Fire:100s}',
              'execute if entity @s[type=minecraft:player] unless predicate bm:p42/burning if block ~ ~ ~ #minecraft:air run function bm:p42/fx/flicker']
    allies = lambda f: [f'execute as @a[distance=..8,gamemode=!spectator] at @s run function {f}', f'execute as @e[type=#bm:p42_ally,distance=..8] at @s run function {f}']
    # a ray from the eyes that stops at the first thing it meets: p54/ray/<name> (steps of 1 block), on a hit runs p54/hit/<name>
    def ray(name, steps, part, lead='positioned ^ ^-0.2 ^1'):
        fn(f'p54/ray/{name}', ['scoreboard players add #k bm.rng 1', *part,
                               f'execute {body} as @e[{MOB},distance=..1.3,sort=nearest,limit=1] at @s run return run function bm:p54/hit/{name} with storage bm:tmp p53',
                               f'execute {body} as {pvp},distance=..1.3,sort=nearest,limit=1] at @s run return run function bm:p54/hit/{name} with storage bm:tmp p53',
                               'execute unless block ~ ~ ~ #bm:grap_pass run return 0', f'execute if score #k bm.rng matches {steps}.. run return 0',
                               f'execute positioned ^ ^ ^1 run function bm:p54/ray/{name}'])
        return f'execute anchored eyes {lead} run function bm:p54/ray/{name}'

    # ---- Heartwood Branch
    fn('p53/branch/act_1', ['function bm:p53/dmg {b:90}', 'scoreboard players set #k bm.rng 0', 'playsound minecraft:entity.player.attack.sweep player @a[distance=..24] ~ ~ ~ 1 0.6',
                            'playsound minecraft:block.sweet_berry_bush.pick_berries player @a[distance=..24] ~ ~ ~ 1 0.6',
                            ray('thorn', 8, ['particle minecraft:dust{color:[0.3,0.55,0.15],scale:1.0} ~ ~ ~ 0.05 0.05 0.05 0 3',
                                             'particle minecraft:block{block_state:"minecraft:oak_leaves"} ~ ~ ~ 0.1 0.1 0.1 0 2'])])
    fn('p54/hit/thorn', hit('bm:bramble', ['effect give @s minecraft:slowness 2 1', 'particle minecraft:block{block_state:"minecraft:oak_leaves"} ~ ~1 ~ 0.3 0.5 0.3 0 15',
                                           'effect give @a[tag=bm.r53me,limit=1] minecraft:regeneration 3 2 true',
                                           'execute at @a[tag=bm.r53me,limit=1] run particle minecraft:heart ~ ~2 ~ 0.3 0.2 0.3 0 2']))
    fn('p53/branch/act_2', ['effect give @s minecraft:resistance 8 1 true', 'effect give @s minecraft:regeneration 8 0 true', 'tag @s add bm.r54bark',
                            'scoreboard players set @s bm.rst 8', 'particle minecraft:block{block_state:"minecraft:oak_log"} ~ ~1 ~ 0.6 0.8 0.6 0 60',
                            'playsound minecraft:block.wood.place player @a[distance=..16] ~ ~ ~ 1.2 0.6', say('Bark closes over your skin.', '#8a6a3a')])
    fn('p53/branch/act_3', ['function bm:p53/dmg {b:50}', 'playsound minecraft:block.big_dripleaf.tilt_down player @a[distance=..24] ~ ~ ~ 1 1.4'] +
       [f'scoreboard players set #k bm.rng 0\n' + ray('seed', 24, ['particle minecraft:dust{color:[0.75,0.85,0.3],scale:0.8} ~ ~ ~ 0.02 0.02 0.02 0 2'],
                                                     f'rotated ~{a} ~ positioned ^ ^-0.2 ^1') for a in (-6, 0, 6)])
    fn('p54/hit/seed', hit('bm:bramble', ['effect give @s minecraft:slowness 3 3', 'particle minecraft:block{block_state:"minecraft:rooted_dirt"} ~ ~0.3 ~ 0.3 0.1 0.3 0 15']))
    fn('p53/branch/act_4', [*ring(8, 40, 0.2, 'minecraft:happy_villager'), 'particle minecraft:cherry_leaves ~ ~2 ~ 3 1 3 0 60',
                            'playsound minecraft:block.chorus_flower.grow player @a[distance=..24] ~ ~ ~ 1.2 1.2', 'playsound minecraft:block.moss.place player @a[distance=..24] ~ ~ ~ 1 0.8',
                            *allies('bm:p54/bloom'),
                            # the crops round you ripen
                            *[f'fill ~-5 ~-2 ~-5 ~5 ~2 ~5 minecraft:{c}[age={a}] replace minecraft:{c}' for c, a in
                              [('wheat', 7), ('carrots', 7), ('potatoes', 7), ('beetroots', 3), ('nether_wart', 3), ('sweet_berry_bush', 3)]],
                            say('Everything around you blooms.', '#ff9ad8')])
    fn('p54/bloom', ['effect give @s minecraft:regeneration 10 1', 'effect give @s minecraft:instant_health 1 0', 'particle minecraft:heart ~ ~2 ~ 0.3 0.2 0.3 0 3'])
    # ---- Molten Gauntlet
    fn('p53/gauntlet/act_1', ['function bm:p53/dmg {b:100}', 'playsound minecraft:entity.generic.explode player @a[distance=..32] ~ ~ ~ 1 1.2',
                              'playsound minecraft:item.firecharge.use player @a[distance=..32] ~ ~ ~ 1 0.6'] +
       [f'execute rotated ~ 0 positioned ^ ^0.6 ^{d} run function bm:p54/erupt' for d in (1, 2, 3, 4, 5)])
    fn('p54/erupt', ['particle minecraft:lava ~ ~ ~ 0.4 0.3 0.4 0 4', 'particle minecraft:flame ~ ~ ~ 0.5 0.4 0.5 0.05 12',
                     f'execute as @e[{MOB},distance=..1.8] at @s run function bm:p54/hit/erupt with storage bm:tmp p53',
                     f'execute as {pvp},distance=..1.8] at @s run function bm:p54/hit/erupt with storage bm:tmp p53'])
    fn('p54/hit/erupt', hit('bm:magma', [*alight, 'effect give @s minecraft:levitation 1 3', 'particle minecraft:lava ~ ~0.5 ~ 0.3 0.3 0.3 0 8']))
    fn('p53/gauntlet/act_2', ['effect give @s minecraft:fire_resistance 30 0 true', 'effect give @s minecraft:resistance 8 1 true', 'tag @s add bm.r54obs',
                              'scoreboard players set @s bm.rst 8', 'particle minecraft:block{block_state:"minecraft:obsidian"} ~ ~1 ~ 0.6 0.8 0.6 0 60',
                              'playsound minecraft:block.respawn_anchor.charge player @a[distance=..16] ~ ~ ~ 1 0.8', say('Obsidian armours your skin.', '#5a3a8a')])
    fn('p53/gauntlet/act_3', ['function bm:p53/dmg {b:90}', 'scoreboard players set #k bm.rng 0', 'playsound minecraft:entity.blaze.shoot player @a[distance=..32] ~ ~ ~ 1 0.8',
                              ray('magma', 30, ['particle minecraft:flame ~ ~ ~ 0.05 0.05 0.05 0.01 2', 'execute if score #k bm.rng matches 3.. run particle minecraft:dripping_lava ~ ~ ~ 0.05 0.05 0.05 0 1'])])
    fn('p54/hit/magma', hit('bm:magma', [*alight, 'particle minecraft:lava ~ ~1 ~ 0.3 0.4 0.3 0 10',
                                         'playsound minecraft:block.lava.extinguish player @a[distance=..16] ~ ~ ~ 0.6 1.2']))
    fn('p53/gauntlet/act_4', [*ring(8, 40, 0.2, 'minecraft:flame'), 'particle minecraft:campfire_cosy_smoke ~ ~1 ~ 1 0.5 1 0.01 10',
                              'playsound minecraft:block.campfire.crackle player @a[distance=..24] ~ ~ ~ 2 0.8', *allies('bm:p54/hearth'),
                              say('Hearthfire warms you and yours.', '#ff8a5a')])
    fn('p54/hearth', ['effect give @s minecraft:fire_resistance 60 0', 'effect give @s minecraft:regeneration 10 0', 'effect give @s minecraft:absorption 30 0',
                      'particle minecraft:flame ~ ~1 ~ 0.3 0.5 0.3 0.02 6'])
    # ---- Void Scepter
    fn('p53/scepter/act_1', ['function bm:p53/dmg {b:120}', 'scoreboard players set #k bm.rng 0', 'scoreboard players set #vr bm.rng 0',
                             ray('rend', 16, ['particle minecraft:reverse_portal ~ ~ ~ 0.05 0.05 0.05 0 2']),
                             'execute if score #vr bm.rng matches 0 run ' + say('Nothing there to rend.', VOID)])
    fn('p54/hit/rend', ['scoreboard players set #vr bm.rng 1', 'particle minecraft:portal ~ ~1 ~ 0.5 1 0.5 0.5 40',
                        # (1.5 blocks short of it, on your side, if there's room)
                        'execute facing entity @a[tag=bm.r53me,limit=1] feet positioned ^ ^ ^1.5 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass '
                        'run tp @a[tag=bm.r53me,limit=1] ~ ~ ~ facing entity @s eyes',
                        'playsound minecraft:entity.enderman.teleport player @a[distance=..24] ~ ~ ~ 1 0.8'] + hit('bm:void', ['particle minecraft:portal ~ ~1 ~ 0.4 0.8 0.4 0.3 30']))
    fn('p53/scepter/act_2', ['effect give @s minecraft:resistance 8 1 true', 'tag @s add bm.r54phase', 'scoreboard players set @s bm.rst 8',
                             'particle minecraft:end_rod ~ ~1 ~ 0.6 0.8 0.6 0.05 40', 'playsound minecraft:entity.shulker.close player @a[distance=..16] ~ ~ ~ 1 0.8',
                             say('You phase half out of the world.', '#7ad8ff')])
    fn('p53/scepter/act_3', ['scoreboard players set #sb bm.rng 0', 'playsound minecraft:entity.shulker.shoot player @a[distance=..24] ~ ~ ~ 1 1',
                             'execute as @e[type=#bm:p42_foe,distance=..24,sort=nearest,limit=3] at @s run function bm:p54/star',
                             'execute if score #sb bm.rng matches 0 run ' + say('No monster near enough to seek.', '#f4f0b0')])
    fn('p54/star', ['scoreboard players add #sb bm.rng 1',
                    'execute at @a[tag=bm.r53me,limit=1] anchored eyes positioned ^ ^ ^1 run summon minecraft:shulker_bullet ~ ~ ~ {Tags:["bm.r54b"],Steps:1}',
                    'data modify entity @e[type=minecraft:shulker_bullet,tag=bm.r54b,limit=1] Target set from entity @s UUID',
                    'data modify entity @e[type=minecraft:shulker_bullet,tag=bm.r54b,limit=1] Owner set from entity @a[tag=bm.r53me,limit=1] UUID',
                    'tag @e[type=minecraft:shulker_bullet,tag=bm.r54b] remove bm.r54b'])
    fn('p53/scepter/act_4', ['playsound minecraft:block.end_gateway.spawn player @a[distance=..32] ~ ~ ~ 0.6 1.4',
                             'execute as @a[distance=0.1..32,gamemode=!spectator] at @s run particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.8 0.3 0.1 30',
                             'tp @a[distance=0.1..32,gamemode=!spectator] @s', 'particle minecraft:portal ~ ~1 ~ 1.5 1 1.5 0.5 80',
                             'execute as @a[distance=..8,gamemode=!spectator] run function bm:p54/rift', say('Your allies step out of the rift beside you.', '#e07dff')])
    fn('p54/rift', ['effect give @s minecraft:resistance 10 0', 'effect give @s minecraft:regeneration 10 0', 'effect give @s minecraft:slow_falling 10 0'])
    # ---- the new guards (bark, obsidian, phase) join phase53's: their look every second, and what hitting you costs
    g, gh = G.FUNCS['p53/guard'], G.FUNCS['p53/guard_hit']
    g[1:1] = ['execute if entity @s[tag=bm.r54bark] run particle minecraft:block{block_state:"minecraft:oak_log"} ~ ~1 ~ 0.5 0.8 0.5 0 8',
              'execute if entity @s[tag=bm.r54obs] run particle minecraft:flame ~ ~1 ~ 0.5 0.8 0.5 0.02 8',
              'execute if entity @s[tag=bm.r54phase] run particle minecraft:end_rod ~ ~1 ~ 0.5 0.8 0.5 0.02 6']
    g += [f'execute if score @s bm.rst matches ..0 run tag @s remove {t}' for t in ('bm.r54bark', 'bm.r54obs', 'bm.r54phase')]
    gh[-1:-1] = ['execute if entity @s[tag=bm.r54bark] as @e[type=#bm:p42_foe,distance=..4] at @s run function bm:p54/prick',
                 'execute if entity @s[tag=bm.r54obs] as @e[type=#bm:p42_foe,distance=..4] at @s run function bm:p54/burn',
                 'execute if entity @s[tag=bm.r54phase] as @e[type=#bm:p42_foe,distance=..4] at @s run function bm:p54/float']
    fn('p54/prick', ['damage @s 3 bm:bramble by @a[tag=bm.r53me,limit=1]', 'effect give @s minecraft:slowness 3 3',
                     'particle minecraft:block{block_state:"minecraft:sweet_berry_bush"} ~ ~1 ~ 0.3 0.5 0.3 0 10'])
    fn('p54/burn', ['damage @s 3 bm:magma by @a[tag=bm.r53me,limit=1]', 'data merge entity @s {Fire:100s}', 'particle minecraft:flame ~ ~1 ~ 0.3 0.5 0.3 0.03 10'])
    fn('p54/float', ['damage @s 3 bm:void by @a[tag=bm.r53me,limit=1]', 'effect give @s minecraft:levitation 3 1', 'particle minecraft:end_rod ~ ~1 ~ 0.3 0.5 0.3 0.05 10'])
    G.FUNCS['admin/relics'][-4:-4] = [give(forms[v][0]) for forms in FAMILIES.values() for v in forms]

    # ================================================================== the bosses: shared pieces
    for key, ent, tag, name, col, hp, bc, music, line in BOSSES:
        fn(f'p54/{key}/sense', [f'tag @s add {tag}sensed', 'title @s times 10 70 30', title('@s', 'subtitle', T(line, col, italic=True)), title('@s', 'title', T('', col)),
                                'playsound minecraft:ambient.cave ambient @s ~ ~ ~ 1 0.7',
                                'stopsound @s music', 'stopsound @s record', f'playsound minecraft:{music} record @s ~ ~ ~ 1 1 1'])
        fn(f'p54/{key}/cleanup', [f'stopsound @a[tag={tag}sensed] record minecraft:{music}', f'execute as @e[tag={tag}min,distance=..128] at @s run function bm:p42/boss/crumble',
                                  f'tag @a remove {tag}sensed', f'bossbar set bm:{key} visible false'])
        # the once-a-second heart of each: bossbar, sense, enrage at half, ambience, then its attack clock (only with someone within 24)
        fn(f'p54/{key}/second', [f'execute store result score #{key}seen bm.bm run time query gametime',
                                 f'execute if entity @a[distance=..128,{NEAR}] run scoreboard players set @s bm.r53x 0',
                                 f'execute unless entity @a[distance=..128,{NEAR}] run scoreboard players add @s bm.r53x 1',
                                 f'execute if score @s bm.r53x matches 90.. run return run function bm:p54/{key}/retreat',
                                 f'execute as @a[distance=..32,tag=!{tag}sensed,gamemode=!spectator] at @s run function bm:p54/{key}/sense',
                                 f'stopsound @a[tag={tag}sensed] music', f'bossbar set bm:{key} players @a[distance=..64]', f'bossbar set bm:{key} visible true',
                                 f'execute store result bossbar bm:{key} value run data get entity @s Health',
                                 'execute store result score #hh bm.rng run data get entity @s Health',
                                 f'execute if score #hh bm.rng matches ..{hp // 2} unless entity @s[tag={tag}_rage] run function bm:p54/{key}/enrage',
                                 f'function bm:p54/{key}/ambience', f'execute unless entity @a[distance=..24,{NEAR}] run return 0',
                                 'scoreboard players add @s bm.r53t 1'] +
           [f'execute if score @s bm.r53t matches {t} {"if entity @s[tag=" + tag + "_rage] " if rage else ""}rotated ~ 0 run function bm:p54/{key}/{a}'
            for t, a, rage in {'trt': [(3, 'roots', 0), (6, 'log', 0), (9, 'twigs', 0), (12, 'log', 0), (14, 'brambles', 1), (15, 'roots', 0)],
                               'mcol': [(3, 'slam', 0), (6, 'boulder', 0), (9, 'geyser', 0), (12, 'boulder', 0), (14, 'geyser', 1), (15, 'slam', 0)],
                               'vwk': [(3, 'blink', 0), (6, 'stars', 0), (9, 'grasp', 0), (12, 'voidlings', 0), (14, 'blink', 1), (15, 'stars', 0)]}[key]] +
           ['execute if score @s bm.r53t matches 16.. run scoreboard players set @s bm.r53t 0'])
        wjson(f'bm/advancement/p54/slain_{key}.json', {'criteria': {'slain': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [
            {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["%s"]}' % tag}}]}}},
            'rewards': {'function': f'bm:p54/slain_{key}'}})
        fn(f'p54/slain_{key}', [f'advancement revoke @s only bm:p54/slain_{key}', 'function bm:p53/wanted',
                                tellraw('@a[distance=..160]', PREFIX + [T(name + ' has fallen to ', col), {'selector': '@s', 'color': 'gold'}, T('!', col)]),
                                f'function bm:p54/{key}/cleanup', 'title @a[distance=..64] times 10 70 20',
                                title('@a[distance=..64]', 'title', T(name.upper().replace('THE ', '') + ' FALLS', col, bold=True)),
                                'execute as @a[distance=..64] at @s run playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1'] +
           ['summon minecraft:experience_orb ~ ~1 ~ {Value:60s}'] * 4)
        second += [f'execute as @e[type=minecraft:{ent},tag={tag}] at @s run function bm:p54/{key}/second',
                   f'execute unless entity @e[type=minecraft:{ent},tag={tag}] run bossbar set bm:{key} visible false',
                   f'scoreboard players add #{key}chk bm.bm 1', f'execute if score #{key}chk bm.bm matches 20.. run function bm:p54/{key}/check']
    # a lobbed boulder (a snowball carrying a block display - it marks where it lands): p54/lob {b:<block>,k:<kind>} as the boss, facing its target
    fn('p54/lob', ['execute anchored eyes positioned ^ ^ ^ run summon minecraft:marker ^ ^ ^1 {Tags:["bm.hhvec"]}',
                   'execute anchored eyes positioned ^ ^ ^ run summon minecraft:marker ~ ~ ~ {Tags:["bm.hhvec0"]}'] +
       [f'execute store result score #a{a} bm.rng run data get entity @e[type=minecraft:marker,tag=bm.hhvec,limit=1] Pos[{i}] 1000' for i, a in enumerate('xyz')] +
       [f'execute store result score #s{a} bm.rng run data get entity @e[type=minecraft:marker,tag=bm.hhvec0,limit=1] Pos[{i}] 1000' for i, a in enumerate('xyz')] +
       [f'scoreboard players operation #a{a} bm.rng -= #s{a} bm.rng' for a in 'xyz'] +
       ['kill @e[type=minecraft:marker,tag=bm.hhvec]', 'kill @e[type=minecraft:marker,tag=bm.hhvec0]', 'scoreboard players add #ay bm.rng 200',
        '$execute anchored eyes positioned ^ ^ ^2.5 run summon minecraft:snowball ~ ~ ~ {Tags:["bm.r54lob","bm.r54new"],Item:{id:"$(blk)",count:1},'
        'Passengers:[{id:"minecraft:block_display",block_state:"$(blk)",Tags:["bm.r54rock","bm.r54_$(k)","bm.r54new"],'
        'transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[-0.6f,-0.6f,-0.6f],scale:[1.2f,1.2f,1.2f]}}]}',
        'execute as @e[type=minecraft:snowball,tag=bm.r54new] run function bm:p54/lob_aim',
        'data modify entity @e[type=minecraft:snowball,tag=bm.r54new,limit=1] Owner set from entity @s UUID',
        'scoreboard players set @e[type=minecraft:block_display,tag=bm.r54new] bm.hzt 100', 'tag @e[tag=bm.r54new] remove bm.r54new'])
    fn('p54/lob_aim', [f'execute store result entity @s Motion[{i}] double 0.0013 run scoreboard players get #a{a} bm.rng' for i, a in enumerate('xyz')])
    tick.append('execute as @e[type=minecraft:block_display,tag=bm.r54rock] at @s run function bm:p54/rock')
    fn('p54/rock', ['execute if entity @s[tag=bm.r54_log] run particle minecraft:block{block_state:"minecraft:oak_leaves"} ~ ~ ~ 0.2 0.2 0.2 0 1',
                    'execute if entity @s[tag=bm.r54_magma] run particle minecraft:flame ~ ~ ~ 0.3 0.3 0.3 0.01 2',
                    'scoreboard players remove @s bm.hzt 1', 'execute if score @s bm.hzt matches ..0 run return run function bm:p54/rock_land',
                    'execute unless function bm:p42/plague/riding run function bm:p54/rock_land'])
    fn('p54/rock_land', [f'execute if entity @s[tag=bm.r54_log] as @a[distance=..2.8,{NEAR}] run damage @s 7 bm:bramble by @e[type=minecraft:creaking,tag=bm.trt,limit=1,sort=nearest]',
                         f'execute if entity @s[tag=bm.r54_magma] as @a[distance=..2.8,{NEAR}] at @s run function bm:p54/mcol/scorch',
                         'execute if entity @s[tag=bm.r54_log] run particle minecraft:block{block_state:"minecraft:oak_log"} ~ ~ ~ 1 0.5 1 0 60',
                         'execute if entity @s[tag=bm.r54_log] run playsound minecraft:block.wood.break hostile @a[distance=..32] ~ ~ ~ 2 0.5',
                         'execute if entity @s[tag=bm.r54_magma] run particle minecraft:lava ~ ~ ~ 1 0.5 1 0 30',
                         'execute if entity @s[tag=bm.r54_magma] run particle minecraft:block{block_state:"minecraft:magma_block"} ~ ~ ~ 1 0.5 1 0 40',
                         'execute if entity @s[tag=bm.r54_magma] run playsound minecraft:block.lava.extinguish hostile @a[distance=..32] ~ ~ ~ 1.5 0.6',
                         'execute on vehicle run kill @s', 'kill @s'])
    # telegraphed bursts under a player's feet (the Colossus's geysers): a marker with a 1.5 s fuse
    tick.append('execute as @e[type=minecraft:marker,tag=bm.r54gey] at @s run function bm:p54/mcol/gey_tick')

    # ================================================================== THE ELDER TREANT (a giant creaking)
    fn('p54/trt/summon', [f'summon minecraft:creaking ~ ~ ~ {snbt(TREANT)}', 'execute as @e[type=minecraft:creaking,tag=bm.trt_new] run function bm:p54/init',
                          'tag @e[tag=bm.trt_new] remove bm.trt_new', 'execute store result score #trtseen bm.bm run time query gametime',
                          'particle minecraft:block{block_state:"minecraft:oak_leaves"} ~ ~3 ~ 2 3 2 0 150', 'particle minecraft:block{block_state:"minecraft:rooted_dirt"} ~ ~0.2 ~ 2 0.1 2 0.1 80',
                          'playsound minecraft:entity.creaking.activate hostile @a[distance=..48] ~ ~ ~ 2 0.4', 'playsound minecraft:block.wood.break hostile @a[distance=..48] ~ ~ ~ 2 0.4',
                          'execute as @a[distance=..32,gamemode=!spectator] at @s run function bm:p54/trt/sense'])
    fn('p54/init', ['scoreboard players set @s bm.r53t 0', 'scoreboard players set @s bm.r53x 0'])
    fn('p54/trt/fast', ['particle minecraft:block{block_state:"minecraft:oak_leaves"} ~ ~5 ~ 1 1.2 1 0 3', 'particle minecraft:falling_spore_blossom ~ ~6 ~ 1.5 0.5 1.5 0 1',
                        'execute as @a[distance=..40] at @s run particle minecraft:spore_blossom_air ~ ~2 ~ 8 3 8 0 12 normal @s',
                        'execute if entity @s[tag=bm.trt_rage] run particle minecraft:happy_villager ~ ~3 ~ 1.2 2 1.2 0 4'])
    fn('p54/trt/ambience', ['execute store result score #r bm.rng run random value 1..10',
                            'execute if score #r bm.rng matches 1 run playsound minecraft:entity.creaking.ambient hostile @a[distance=..48] ~ ~ ~ 2 0.5',
                            'execute if score #r bm.rng matches 2 as @a[distance=..48] at @s run playsound minecraft:block.azalea_leaves.step ambient @s ~ ~ ~ 1.5 0.6',
                            'execute if score #r bm.rng matches 3 run playsound minecraft:block.wood.break hostile @a[distance=..48] ~ ~ ~ 1 0.4',
                            'execute if score #r bm.rng matches 4 as @a[distance=..40] at @s run playsound minecraft:ambient.cave ambient @s ~ ~ ~ 0.6 0.6',
                            'execute if score #r bm.rng matches 5 run playsound minecraft:entity.creaking.freeze hostile @a[distance=..40] ~ ~ ~ 1.5 0.5',
                            'execute if score #r bm.rng matches 6 as @a[distance=..20] at @s run playsound minecraft:entity.warden.heartbeat ambient @s ~ ~ ~ 0.6 0.6'])
    # roots: everyone near is pinned in place for a moment
    fn('p54/trt/roots', ['playsound minecraft:block.roots.break hostile @a[distance=..32] ~ ~ ~ 2 0.5', 'tag @s add bm.trtme',
                         f'execute as @a[distance=..12,{NEAR}] at @s run function bm:p54/trt/root', 'tag @s remove bm.trtme'])
    fn('p54/trt/root', ['effect give @s minecraft:slowness 3 6', 'effect give @s minecraft:mining_fatigue 3 1',
                        'damage @s 2 bm:bramble by @e[type=minecraft:creaking,tag=bm.trtme,limit=1]',
                        'particle minecraft:block{block_state:"minecraft:rooted_dirt"} ~ ~0.2 ~ 0.4 0.1 0.4 0.1 30',
                        'particle minecraft:block{block_state:"minecraft:mangrove_roots"} ~ ~0.6 ~ 0.3 0.4 0.3 0 20'])
    fn('p54/trt/log', [f'execute unless entity @a[distance=..28,{NEAR}] run return 0', 'playsound minecraft:entity.creaking.attack hostile @a[distance=..32] ~ ~ ~ 2 0.5',
                       f'execute facing entity @p[distance=..28,{NEAR}] eyes run function bm:p54/lob {{blk:"minecraft:oak_log",k:"log"}}'])
    fn('p54/trt/twigs', ['execute store result score #mc bm.rng if entity @e[type=minecraft:creaking,tag=bm.trtmin,distance=..40]',
                         'execute if score #mc bm.rng matches 4.. run return 0', 'playsound minecraft:entity.creaking.activate hostile @a[distance=..32] ~ ~ ~ 1.5 1.4',
                         'execute positioned ^2.5 ^ ^-1 run function bm:p54/trt/twig', 'execute positioned ^-2.5 ^ ^-1 run function bm:p54/trt/twig'])
    fn('p54/trt/twig', ['execute unless block ~ ~ ~ #bm:grap_pass run return 0', 'execute unless block ~ ~1 ~ #bm:grap_pass run return 0',
                        f'summon minecraft:creaking ~ ~ ~ {snbt(TWIG)}', 'particle minecraft:block{block_state:"minecraft:oak_log"} ~ ~0.5 ~ 0.3 0.5 0.3 0 20'])
    fn('p54/trt/brambles', ['playsound minecraft:block.sweet_berry_bush.pick_berries hostile @a[distance=..32] ~ ~ ~ 2 0.5', 'tag @s add bm.trtme',
                            *ring(6, 30, 0.4, 'minecraft:block{block_state:"minecraft:sweet_berry_bush"}'),
                            f'execute as @a[distance=..9,{NEAR}] at @s run function bm:p54/trt/bramble', 'tag @s remove bm.trtme'])
    fn('p54/trt/bramble', ['damage @s 5 bm:bramble by @e[type=minecraft:creaking,tag=bm.trtme,limit=1]', 'effect give @s minecraft:poison 3 0',
                           'particle minecraft:block{block_state:"minecraft:sweet_berry_bush"} ~ ~0.5 ~ 0.4 0.4 0.4 0 20'])
    fn('p54/trt/enrage', ['tag @s add bm.trt_rage', 'effect give @s minecraft:regeneration 12 1 true',
                          'attribute @s minecraft:movement_speed modifier add bm:trt_rage 0.25 add_multiplied_base', 'bossbar set bm:trt color yellow',
                          title('@a[distance=..48]', 'actionbar', T('The forest groans - the Elder Treant draws life from its roots!', OAK, bold=True)),
                          'playsound minecraft:entity.creaking.activate hostile @a[distance=..48] ~ ~ ~ 2 0.3', 'function bm:p54/trt/twigs'])
    fn('p54/trt/retreat', [title('@a[distance=..64]', 'actionbar', T('The Elder Treant walks back into the trees...', OAK, italic=True)),
                           'particle minecraft:block{block_state:"minecraft:oak_leaves"} ~ ~3 ~ 2 3 2 0 150', 'playsound minecraft:block.wood.break hostile @a[distance=..64] ~ ~ ~ 2 0.4',
                           'function bm:p54/trt/cleanup', 'tp @s ~ -400 ~', 'kill @s'])
    G.FUNCS['p54/trt/second'].insert(1, 'execute unless score #tod bm.bm matches 13000..23199 run return run function bm:p54/trt/retreat')
    fn('p54/trt/check', ['scoreboard players set #trtchk bm.bm 0', 'execute unless score #tod bm.bm matches 13000..21999 run return 0',
                         f'execute if score #day bm.bm matches ..{GRACE_DAYS - 1} run return 0', 'execute if entity @e[type=minecraft:creaking,tag=bm.trt] run return 0',
                         'function bm:p54/gap {k:"trt"}', 'execute if score #gap bm.rng matches 0..2399 run return 0',
                         f'execute store result score #r bm.rng run random value 1..{TRT_ODDS}', 'execute unless score #r bm.rng matches 1 run return 0',
                         f'execute in minecraft:overworld as @a[distance=0..,{NEAR},predicate=bm:p54/forest,sort=random,limit=1] at @s run function bm:p54/trt/try'])
    fn('p54/trt/try', ['execute positioned ~ ~1.6 ~ unless predicate bm:sees_sky run return 0',
                       'execute store result storage bm:tmp p54s.a int 1 run random value 0..359', 'function bm:p54/trt/at with storage bm:tmp p54s'])
    fn('p54/trt/at', ['$execute rotated $(a) 0 positioned ^ ^ ^20 positioned over motion_blocking_no_leaves run function bm:p54/trt/place'])
    fn('p54/trt/place', ['execute if block ~ ~-1 ~ minecraft:water run return 0', 'execute if block ~ ~ ~ minecraft:water run return 0'] +
       [f'execute unless block ~ ~{y} ~ #bm:grap_pass run return 0' for y in range(3)] +
       ['execute unless function bm:p37/allowed run return 0', 'function bm:p54/trt/summon'])
    fn('p54/gap', ['execute store result score #now bm.rng run time query gametime', 'scoreboard players operation #gap bm.rng = #now bm.rng',
                   '$scoreboard players operation #gap bm.rng -= #$(k)seen bm.bm', '$execute unless score #$(k)seen bm.bm matches 1.. run scoreboard players set #gap bm.rng 99999'])

    # ================================================================== THE MAGMA COLOSSUS (a gigantic magma cube)
    fn('p54/mcol/summon', [f'summon minecraft:magma_cube ~ ~ ~ {snbt(COLOSSUS)}', 'execute as @e[type=minecraft:magma_cube,tag=bm.mcol_new] run function bm:p54/mcol/init',
                           'tag @e[tag=bm.mcol_new] remove bm.mcol_new', 'execute store result score #mcolseen bm.bm run time query gametime',
                           'particle minecraft:lava ~ ~1 ~ 2.5 1 2.5 0 80', 'particle minecraft:large_smoke ~ ~2 ~ 2.5 2 2.5 0.05 80',
                           'playsound minecraft:entity.magma_cube.squish hostile @a[distance=..48] ~ ~ ~ 2 0.3', 'playsound minecraft:block.lava.pop hostile @a[distance=..48] ~ ~ ~ 2 0.5',
                           'execute as @a[distance=..32,gamemode=!spectator] at @s run function bm:p54/mcol/sense'])
    # (a slime's size sets its own health and strength as it loads: set ours after)
    fn('p54/mcol/init', ['function bm:p54/init', f'attribute @s minecraft:max_health base set {COL_HP}', f'data modify entity @s Health set value {COL_HP}f',
                         'attribute @s minecraft:attack_damage base set 10', 'attribute @s minecraft:armor base set 10',
                         'attribute @s minecraft:knockback_resistance base set 1', 'attribute @s minecraft:follow_range base set 64'])
    fn('p54/mcol/fast', ['particle minecraft:lava ~ ~2 ~ 1.5 1 1.5 0 2', 'particle minecraft:flame ~ ~1 ~ 2 1 2 0.02 4',
                         'execute as @a[distance=..40] at @s run particle minecraft:ash ~ ~2 ~ 8 3 8 0 20 normal @s',
                         'execute if entity @s[tag=bm.mcol_rage] run particle minecraft:large_smoke ~ ~3 ~ 1.5 1 1.5 0.02 4'])
    fn('p54/mcol/ambience', ['execute store result score #r bm.rng run random value 1..10',
                             'execute if score #r bm.rng matches 1 run playsound minecraft:block.lava.pop hostile @a[distance=..48] ~ ~ ~ 2 0.5',
                             'execute if score #r bm.rng matches 2 run playsound minecraft:entity.magma_cube.squish hostile @a[distance=..48] ~ ~ ~ 2 0.4',
                             'execute if score #r bm.rng matches 3 as @a[distance=..48] at @s run playsound minecraft:ambient.basalt_deltas.mood ambient @s ~ ~ ~ 1 0.7',
                             'execute if score #r bm.rng matches 4 run playsound minecraft:entity.blaze.ambient hostile @a[distance=..40] ~ ~ ~ 1 0.4',
                             'execute if score #r bm.rng matches 5 as @a[distance=..40] at @s run playsound minecraft:ambient.nether_wastes.mood ambient @s ~ ~ ~ 1 0.6'])
    fn('p54/mcol/slam', ['playsound minecraft:item.mace.smash_ground hostile @a[distance=..40] ~ ~ ~ 2 0.5', 'playsound minecraft:entity.generic.explode hostile @a[distance=..40] ~ ~ ~ 1.2 0.6',
                         *ring(4, 24, 0.2, 'minecraft:flame'), *ring(7, 36, 0.2, 'minecraft:lava'), 'tag @s add bm.mcolme',
                         f'execute as @a[distance=..9,{NEAR}] at @s run function bm:p54/mcol/slammed', 'tag @s remove bm.mcolme'])
    fn('p54/mcol/slammed', ['damage @s 7 bm:magma by @e[type=minecraft:magma_cube,tag=bm.mcolme,limit=1]', 'effect give @s minecraft:levitation 1 4 true',
                            'execute unless predicate bm:p42/burning if block ~ ~ ~ #minecraft:air run function bm:p42/fx/flicker'])
    fn('p54/mcol/scorch', ['damage @s 6 bm:magma by @e[type=minecraft:magma_cube,tag=bm.mcol,limit=1,sort=nearest]',
                           'execute unless predicate bm:p42/burning if block ~ ~ ~ #minecraft:air run function bm:p42/fx/flicker'])
    fn('p54/mcol/boulder', [f'execute unless entity @a[distance=..28,{NEAR}] run return 0', 'playsound minecraft:entity.magma_cube.jump hostile @a[distance=..32] ~ ~ ~ 2 0.5',
                            f'execute facing entity @p[distance=..28,{NEAR}] eyes run function bm:p54/lob {{blk:"minecraft:magma_block",k:"magma"}}'])
    fn('p54/mcol/geyser', ['playsound minecraft:block.lava.pop hostile @a[distance=..40] ~ ~ ~ 2 0.4',
                           f'execute as @a[distance=..28,{NEAR},sort=random,limit=2] at @s run summon minecraft:marker ~ ~ ~ {{Tags:["bm.r54gey","bm.r54gn"]}}',
                           'scoreboard players set @e[type=minecraft:marker,tag=bm.r54gn] bm.rfx 30', 'tag @e[tag=bm.r54gn] remove bm.r54gn'])
    fn('p54/mcol/gey_tick', ['scoreboard players remove @s bm.rfx 1', *ring(1.4, 8, 0.1, 'minecraft:dripping_lava'), 'particle minecraft:smoke ~ ~0.2 ~ 0.6 0.1 0.6 0.01 2',
                             'execute if score @s bm.rfx matches 0 run function bm:p54/mcol/erupt', 'execute if score @s bm.rfx matches ..0 run kill @s'])
    fn('p54/mcol/erupt', ['particle minecraft:lava ~ ~0.5 ~ 0.6 1.5 0.6 0 40', 'particle minecraft:flame ~ ~1.5 ~ 0.4 2 0.4 0.1 60',
                          'playsound minecraft:entity.generic.explode hostile @a[distance=..32] ~ ~ ~ 1 1.2',
                          f'execute as @a[distance=..2.5,{NEAR}] at @s run function bm:p54/mcol/blasted'])
    fn('p54/mcol/blasted', ['damage @s 6 bm:magma by @e[type=minecraft:magma_cube,tag=bm.mcol,limit=1,sort=nearest]', 'effect give @s minecraft:levitation 1 6 true',
                            'execute unless predicate bm:p42/burning if block ~ ~ ~ #minecraft:air run function bm:p42/fx/flicker'])
    fn('p54/mcol/enrage', ['tag @s add bm.mcol_rage', 'effect give @s minecraft:strength infinite 0 true', 'bossbar set bm:mcol color yellow',
                           title('@a[distance=..48]', 'actionbar', T('The Magma Colossus boils over!', LAVA, bold=True)),
                           'playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 1.5 0.4', 'function bm:p54/mcol/shed'])
    # it sheds Magma Spawn when hurt (at 2/3 and 1/3 health) ...
    fn('p54/mcol/shed', ['playsound minecraft:entity.magma_cube.squish hostile @a[distance=..40] ~ ~ ~ 2 1.2',
                         *[f'summon minecraft:magma_cube ^{x} ^1 ^ {snbt(SPAWNLING)}' for x in (-3, 3)], 'particle minecraft:lava ~ ~2 ~ 2 1 2 0 30'])
    G.FUNCS['p54/mcol/second'][1:1] = [f'execute store result score #hh bm.rng run data get entity @s Health',
                                       f'execute if score #hh bm.rng matches ..{COL_HP * 2 // 3} unless entity @s[tag=bm.mcol_s1] run function bm:p54/mcol/shed1',
                                       f'execute if score #hh bm.rng matches ..{COL_HP // 3} unless entity @s[tag=bm.mcol_s2] run function bm:p54/mcol/shed2']
    fn('p54/mcol/shed1', ['tag @s add bm.mcol_s1', 'execute rotated ~ 0 run function bm:p54/mcol/shed'])
    fn('p54/mcol/shed2', ['tag @s add bm.mcol_s2', 'execute rotated ~ 0 run function bm:p54/mcol/shed'])
    # ... and when it dies it bursts into smaller cubes. They inherit its name and tags but not its scores: found that way,
    # they become Magma Spawn
    tick.append('execute as @e[type=minecraft:magma_cube,tag=bm.mcol] unless score @s bm.r53x matches -2147483648.. run function bm:p54/mcol/spawnling')
    fn('p54/mcol/spawnling', [*[f'tag @s remove bm.mcol{t}' for t in ('', '_s1', '_s2', '_rage', '_new')], 'tag @s add bm.mcolmin',
                              'effect clear @s minecraft:strength', f'data modify entity @s CustomName set value {snbt(T("Magma Spawn", "#ff9a3a"))}'])
    fn('p54/mcol/retreat', [title('@a[distance=..64]', 'actionbar', T('The Magma Colossus sinks back into the lava...', LAVA, italic=True)),
                            'particle minecraft:lava ~ ~1 ~ 2.5 1 2.5 0 80', 'playsound minecraft:block.lava.pop hostile @a[distance=..64] ~ ~ ~ 2 0.4',
                            'function bm:p54/mcol/cleanup', 'tp @s ~ -400 ~', 'kill @s'])
    fn('p54/mcol/check', ['scoreboard players set #mcolchk bm.bm 0', f'execute if score #day bm.bm matches ..{GRACE_DAYS - 1} run return 0',
                          'execute if entity @e[type=minecraft:magma_cube,tag=bm.mcol] run return 0',
                          'function bm:p54/gap {k:"mcol"}', 'execute if score #gap bm.rng matches 0..2399 run return 0',
                          f'execute store result score #r bm.rng run random value 1..{COL_ODDS}', 'execute unless score #r bm.rng matches 1 run return 0',
                          f'execute in minecraft:the_nether as @a[distance=0..,{NEAR},predicate=bm:p54/nether_waste,sort=random,limit=1] at @s run function bm:p54/mcol/try'])
    fn('p54/mcol/try', ['scoreboard players set #fk bm.rng 1', 'execute store result storage bm:tmp p54s.a int 1 run random value 0..359',
                        'function bm:p54/find/at with storage bm:tmp p54s'])
    # (in the Nether there's no open sky to drop from: search a column for floor with headroom)
    fn('p54/find/at', ['$execute rotated $(a) 0 positioned ^ ^6 ^18 align y run function bm:p54/find/start'])
    fn('p54/find/start', ['scoreboard players set #fy bm.rng 0', 'function bm:p54/find/step'])
    fn('p54/find/step', ['scoreboard players add #fy bm.rng 1', 'execute if score #fy bm.rng matches 16.. run return 0',
                         'execute unless block ~ ~-1 ~ #bm:grap_pass unless block ~ ~-1 ~ minecraft:lava unless block ~ ~-1 ~ minecraft:bedrock '
                         'if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air if block ~ ~2 ~ minecraft:air if block ~ ~3 ~ minecraft:air run return run function bm:p54/find/found',
                         'execute positioned ~ ~-1 ~ run function bm:p54/find/step'])
    fn('p54/find/found', ['execute unless function bm:p37/allowed run return 0',
                          'execute if score #fk bm.rng matches 1 run return run function bm:p54/mcol/summon',
                          'execute if score #fk bm.rng matches 2 run return run function bm:p54/vwk/summon'])

    # ================================================================== THE VOIDWALKER (a giant enderman)
    fn('p54/vwk/summon', [f'summon minecraft:enderman ~ ~ ~ {snbt(VOIDWALKER)}', 'execute as @e[type=minecraft:enderman,tag=bm.vwk_new] run function bm:p54/init',
                          'tag @e[tag=bm.vwk_new] remove bm.vwk_new', 'execute store result score #vwkseen bm.bm run time query gametime',
                          'particle minecraft:portal ~ ~3 ~ 1.5 3 1.5 1 300', 'particle minecraft:reverse_portal ~ ~3 ~ 1.5 3 1.5 0.1 100',
                          'playsound minecraft:entity.enderman.stare hostile @a[distance=..48] ~ ~ ~ 2 0.5', 'playsound minecraft:block.end_portal.spawn hostile @a[distance=..48] ~ ~ ~ 0.6 0.6',
                          'execute as @a[distance=..32,gamemode=!spectator] at @s run function bm:p54/vwk/sense'])
    # it is always angry at the nearest player, and never carries blocks off
    G.FUNCS['p54/vwk/second'][1:1] = [f'execute if entity @a[distance=..64,{NEAR}] run data modify entity @s angry_at set from entity @p[distance=..64,{NEAR}] UUID',
                                      'execute store result score #ae bm.rng run time query gametime', 'scoreboard players add #ae bm.rng 400',
                                      'execute store result entity @s anger_end_time long 1 run scoreboard players get #ae bm.rng',
                                      'data remove entity @s carriedBlockState']
    fn('p54/vwk/fast', ['particle minecraft:portal ~ ~3 ~ 1 2.5 1 0.5 10', 'particle minecraft:reverse_portal ~ ~5 ~ 0.6 1 0.6 0.02 3',
                        'execute as @a[distance=..40] at @s run particle minecraft:end_rod ~ ~3 ~ 9 4 9 0.01 6 normal @s',
                        'execute if entity @s[tag=bm.vwk_rage] run particle minecraft:dragon_breath ~ ~3 ~ 1 2 1 0.01 6'])
    fn('p54/vwk/ambience', ['execute store result score #r bm.rng run random value 1..10',
                            'execute if score #r bm.rng matches 1 run playsound minecraft:entity.enderman.ambient hostile @a[distance=..48] ~ ~ ~ 2 0.4',
                            'execute if score #r bm.rng matches 2 as @a[distance=..48] at @s run playsound minecraft:block.portal.ambient ambient @s ~ ~ ~ 0.4 0.6',
                            'execute if score #r bm.rng matches 3 run playsound minecraft:entity.enderman.stare hostile @a[distance=..40] ~ ~ ~ 1 0.5',
                            'execute if score #r bm.rng matches 4 as @a[distance=..40] at @s run playsound minecraft:ambient.cave ambient @s ~ ~ ~ 0.6 0.5',
                            'execute if score #r bm.rng matches 5 as @a[distance=..20] at @s run playsound minecraft:entity.warden.heartbeat ambient @s ~ ~ ~ 0.6 0.5'])
    # it blinks behind someone and strikes
    fn('p54/vwk/blink', [f'execute unless entity @a[distance=..28,{NEAR}] run return 0', 'tag @s add bm.vwkme',
                         f'execute as @p[distance=..28,{NEAR}] at @s rotated ~ 0 positioned ^ ^ ^-2.5 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass '
                         'if block ~ ~2 ~ #bm:grap_pass unless block ~ ~-1 ~ #bm:grap_pass run function bm:p54/vwk/behind',
                         'tag @s remove bm.vwkme'])
    fn('p54/vwk/behind', ['particle minecraft:portal ~ ~2 ~ 0.6 1.5 0.6 0.5 60',
                          'tp @e[type=minecraft:enderman,tag=bm.vwkme,limit=1] ~ ~ ~ facing entity @p[distance=..4] feet',
                          'playsound minecraft:entity.enderman.teleport hostile @a[distance=..32] ~ ~ ~ 2 0.5',
                          f'execute as @p[distance=..4,{NEAR}] run damage @s 8 bm:void by @e[type=minecraft:enderman,tag=bm.vwkme,limit=1]'])
    fn('p54/vwk/stars', ['playsound minecraft:entity.shulker.shoot hostile @a[distance=..40] ~ ~ ~ 2 0.6',
                         f'execute as @a[distance=..28,{NEAR},sort=random,limit=3] at @s run function bm:p54/vwk/star'])
    fn('p54/vwk/star', ['execute at @e[type=minecraft:enderman,tag=bm.vwk,limit=1,sort=nearest] anchored eyes positioned ^ ^ ^1.5 run summon minecraft:shulker_bullet ~ ~ ~ {Tags:["bm.r54b"],Steps:1}',
                        'data modify entity @e[type=minecraft:shulker_bullet,tag=bm.r54b,limit=1] Target set from entity @s UUID',
                        'data modify entity @e[type=minecraft:shulker_bullet,tag=bm.r54b,limit=1] Owner set from entity @e[type=minecraft:enderman,tag=bm.vwk,limit=1,sort=nearest] UUID',
                        'tag @e[type=minecraft:shulker_bullet,tag=bm.r54b] remove bm.r54b'])
    fn('p54/vwk/grasp', ['playsound minecraft:entity.warden.sonic_charge hostile @a[distance=..40] ~ ~ ~ 1 0.5', 'tag @s add bm.vwkme',
                         f'execute as @a[distance=..16,{NEAR}] at @s run function bm:p54/vwk/grasped', 'tag @s remove bm.vwkme'])
    fn('p54/vwk/grasped', ['effect give @s minecraft:darkness 5 0', 'effect give @s minecraft:slowness 4 1', 'damage @s 4 bm:void by @e[type=minecraft:enderman,tag=bm.vwkme,limit=1]',
                           'particle minecraft:reverse_portal ~ ~1 ~ 0.4 0.8 0.4 0.1 30'])
    fn('p54/vwk/voidlings', ['execute store result score #mc bm.rng if entity @e[type=minecraft:endermite,tag=bm.vwkmin,distance=..40]',
                             'execute if score #mc bm.rng matches 6.. run return 0', 'playsound minecraft:entity.endermite.ambient hostile @a[distance=..32] ~ ~ ~ 2 0.5'] +
       [f'execute positioned ^{x} ^ ^1.5 if block ~ ~ ~ #bm:grap_pass run summon minecraft:endermite ~ ~ ~ {snbt(VOIDLING)}' for x in (-1.5, 0, 1.5)])
    fn('p54/vwk/enrage', ['tag @s add bm.vwk_rage', 'effect give @s minecraft:strength infinite 0 true',
                          'attribute @s minecraft:movement_speed modifier add bm:vwk_rage 0.3 add_multiplied_base', 'bossbar set bm:vwk color red',
                          title('@a[distance=..48]', 'actionbar', T('The Voidwalker tears at the stars!', VOID, bold=True)),
                          'playsound minecraft:entity.enderman.scream hostile @a[distance=..48] ~ ~ ~ 2 0.4', 'function bm:p54/vwk/voidlings'])
    fn('p54/vwk/retreat', [title('@a[distance=..64]', 'actionbar', T('The Voidwalker steps out of the world...', VOID, italic=True)),
                           'particle minecraft:portal ~ ~3 ~ 1.5 3 1.5 1 300', 'playsound minecraft:entity.enderman.teleport hostile @a[distance=..64] ~ ~ ~ 2 0.4',
                           'function bm:p54/vwk/cleanup', 'tp @s ~ -400 ~', 'kill @s'])
    fn('p54/vwk/check', ['scoreboard players set #vwkchk bm.bm 0', 'execute if entity @e[type=minecraft:enderman,tag=bm.vwk] run return 0',
                         'function bm:p54/gap {k:"vwk"}', 'execute if score #gap bm.rng matches 0..2399 run return 0',
                         f'execute store result score #r bm.rng run random value 1..{VWK_ODDS}', 'execute unless score #r bm.rng matches 1 run return 0',
                         f'execute in minecraft:the_end as @a[distance=0..,{NEAR},sort=random,limit=1] at @s unless entity @s[x=0,y=64,z=0,distance=..700] run function bm:p54/vwk/try'])
    fn('p54/vwk/try', ['scoreboard players set #fk bm.rng 2', 'execute store result storage bm:tmp p54s.a int 1 run random value 0..359',
                       'function bm:p54/find/at with storage bm:tmp p54s'])

    # ================================================================== loot, achievements, admin
    tables = {'treant': ('heartwood_branch', 0.10, [('oak_log', 8, 16), ('oak_sapling', 2, 5), ('apple', 2, 5), ('moss_block', 4, 8)], (10, 16), (2, 4), 0.4),
              'colossus': ('molten_gauntlet', 0.10, [('magma_cream', 4, 8), ('blaze_rod', 1, 3), ('netherite_scrap', 1, 1)], (10, 16), (2, 4), 0.4),
              'voidwalker': ('void_scepter', 1 / 6, [('shulker_shell', 2, 4), ('ender_pearl', 4, 8), ('dragon_breath', 2, 4)], (16, 24), (4, 6), 0.6)}
    for t, (relic, ch, extras, tok, med, tro) in tables.items():
        wjson(f'bm/loot_table/p54/{t}.json', {'type': 'minecraft:entity', 'pools': [
            {'rolls': 1, 'entries': [G.loot_entry(relic)], 'conditions': [G.KILLED, G.chance(ch)]},
            {'rolls': 1, 'entries': [G.loot_entry('token', G.uni(*tok))], 'conditions': [G.KILLED]},
            {'rolls': 1, 'entries': [G.loot_entry('medallion', G.uni(*med))], 'conditions': [G.KILLED]},
            {'rolls': 1, 'entries': [G.loot_entry('trophy')], 'conditions': [G.KILLED, G.chance(tro)]}] +
            [{'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': f'minecraft:{i}', 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(a, b)}]}],
              'conditions': [G.KILLED]} for i, a, b in extras]})
    adv = lambda key, parent, ico, ttl, desc, crit: wjson(f'bm/advancement/story/{key}.json', {
        'parent': f'bm:story/{parent}', 'criteria': crit,
        'display': {'icon': ({'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': f'bm:{ico}'}} if ':' not in ico else {'id': ico}),
                    'title': T(ttl, 'gold'), 'description': T(desc, 'gray'), 'frame': 'challenge', 'show_toast': True, 'announce_to_chat': True, 'hidden': False}})
    kill = lambda tag: {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["%s"]}' % tag}}]}}
    holding = lambda cd: {'trigger': 'minecraft:inventory_changed', 'conditions': {'items': [{'items': 'minecraft:totem_of_undying',
                                                                                              'predicates': {'minecraft:custom_data': cd}}]}}
    adv('treant', 'root', 'minecraft:oak_sapling', 'Heart of the Forest', 'Slay the Elder Treant', {'slain': kill('bm.trt')})
    adv('colossus', 'root', 'minecraft:magma_block', 'Cooled Off', 'Slay the Magma Colossus', {'slain': kill('bm.mcol')})
    adv('voidwalker', 'root', 'minecraft:ender_eye', 'Stare Down', 'Slay the Voidwalker', {'slain': kill('bm.vwk')})
    adv('legendary_hunter', 'monster_slayer', 'minecraft:netherite_sword', 'Legendary Hunter', 'Slay all six roaming bosses',
        {k: kill(f'bm.{k}') for k in ('hhm', 'sph', 'roc', 'trt', 'mcol', 'vwk')})
    adv('grand_relic_hunter', 'relic_hunter', 'void_scepter', 'Grand Relic Hunter', 'Hold a relic of every roaming boss',
        dict({'head': holding('{bm_head:1b}')}, **{f: holding('{rf:"%s"}' % f) for f in ('crook', 'talon', 'branch', 'gauntlet', 'scepter')}))
    fn('admin/treant', ['execute rotated ~ 0 positioned ^ ^ ^12 positioned over motion_blocking_no_leaves run function bm:p54/trt/summon',
                        tellraw('@s', PREFIX + [T('The Elder Treant walks out 12 blocks ahead. It leaves at dawn.', 'gray')])])
    fn('admin/colossus', ['execute rotated ~ 0 positioned ^ ^ ^12 run function bm:p54/mcol/summon',
                          tellraw('@s', PREFIX + [T('The Magma Colossus rises 12 blocks ahead.', 'gray')])])
    fn('admin/voidwalker', ['execute rotated ~ 0 positioned ^ ^ ^12 run function bm:p54/vwk/summon',
                            tellraw('@s', PREFIX + [T('The Voidwalker steps out 12 blocks ahead.', 'gray')])])
    fast += ['execute as @e[type=minecraft:creaking,tag=bm.trt] at @s run function bm:p54/trt/fast',
             'execute as @e[type=minecraft:magma_cube,tag=bm.mcol] at @s run function bm:p54/mcol/fast',
             'execute as @e[type=minecraft:enderman,tag=bm.vwk] at @s run function bm:p54/vwk/fast']
    second += ['execute unless entity @e[type=minecraft:creaking,tag=bm.trt] as @e[type=minecraft:creaking,tag=bm.trtmin] at @s run function bm:p42/boss/crumble']

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


# ===================================================================== resource pack: the relics' icons
def _hex(c):
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


def rp(R):
    from PIL import Image, ImageDraw
    def branch(gem):
        im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.line((2, 14, 12, 4), fill=_hex('#6a4a2a') + (255,), width=2)
        d.line((7, 9, 4, 5), fill=_hex('#6a4a2a') + (255,), width=1); d.line((10, 6, 13, 9), fill=_hex('#6a4a2a') + (255,), width=1)
        for (x, y) in [(12, 3), (13, 4), (11, 2), (3, 4), (4, 4), (13, 9), (14, 8), (13, 2)]:
            im.putpixel((x, y), _hex('#4a9a2a') + (255,))
        for (x, y) in [(12, 4), (4, 5), (13, 8)]:
            im.putpixel((x, y), _hex(gem) + (255,))
        return im
    def gauntlet(gem):
        im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rectangle((4, 9, 11, 14), fill=_hex('#3a2a2a') + (255,))
        d.rectangle((4, 3, 12, 9), fill=_hex('#5a3a2a') + (255,))
        for x in (5, 7, 9, 11):
            d.line((x, 2, x, 4), fill=_hex('#4a2a1a') + (255,))
        for (x, y) in [(6, 5), (7, 6), (9, 5), (10, 7), (8, 8), (6, 7)]:
            im.putpixel((x, y), _hex('#ff8a1a') + (255,))
        d.rectangle((7, 10, 8, 11), fill=_hex(gem) + (255,))
        return im
    def scepter(gem):
        im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.line((2, 14, 10, 6), fill=_hex('#e8e0b0') + (255,), width=1); d.line((3, 14, 10, 7), fill=_hex('#9a9070') + (255,), width=1)
        d.ellipse((9, 1, 14, 6), fill=_hex('#1a6a5a') + (255,)); d.ellipse((10, 2, 13, 5), fill=_hex('#3ad8a8') + (255,))
        im.putpixel((11, 3), (10, 10, 10, 255)); im.putpixel((12, 3), (10, 10, 10, 255))
        for (x, y) in [(8, 4), (14, 7), (12, 0)]:
            im.putpixel((x, y), _hex(gem) + (255,))
        return im
    draw = {'branch': branch, 'gauntlet': gauntlet, 'scepter': scepter}
    for fam, forms in FAMILIES.items():
        for v, (iid, name, col, *_r) in forms.items():
            R.ICONS[iid] = draw[fam](col)
            R.HANDHELD_EXTRA.add(iid)
    R.LANG.update({'death.attack.bm.bramble': '%1$s was torn apart by brambles', 'death.attack.bm.bramble.player': '%1$s was torn apart by %2$s\'s brambles',
                   'death.attack.bm.magma': '%1$s was melted by magma', 'death.attack.bm.magma.player': '%1$s was melted by %2$s\'s magma',
                   'death.attack.bm.void': '%1$s was swallowed by the void', 'death.attack.bm.void.player': '%1$s was swallowed by %2$s\'s void'})

"""2.99a: THE REX MOUNTS - two hidden RIDEABLE MOUNTS (not followers), summoned with an item, ridden, kept on the Partner
Wheel's new MOUNTS PAGE (with the Vorn Skiff and the Mothership). rex_art.py draws them; this is their runtime.

THE ATOMIC REX (atomic_whistle; any player, any mode)
  1. THE FOSSIL     mining deepslate or any deepslate ore below y=0: 1 in 400 a block gives a REX FOSSIL (the mined-stat scores,
                    as phase183 counts them) - while you haven't hatched one and carry no fossil or egg.
  2. THE LIGHTNING  the fossil dropped on (or right beside) a lightning rod in a thunderstorm: each second it rests there, 1 in 20
                    the sky strikes it (a summoned bolt) and it is a REX EGG (fire- and lightning-proof: damage_resistant, the
                    tag bm:p249_proof), with a burst of blue and a word to the nearest player.
  3. THE HATCHING   the egg dropped into LAVA in the Nether: it floats; after 60 s there it bursts - its thrower (Thrower; else the
                    nearest player) gets the whistle: a blue pillar, the roar, THE ATOMIC REX HATCHES, an advancement.
THE MECHA REX (mecha_remote; the Vorn Armada - hard mode)
  1. THREE BLUEPRINTS  aboard the Armada, once a player each, with a relic pedestal's Hive Sigil: I from SECRET 1 (the Star-Forge's
                    forgotten hold), II from SECRET 2 (Dreadnought B's sealed bulkhead), III from any of the four follower rooms.
  2. THE CORE       the Mecha Core: opening the Hive Vault (behind the helm), or Vexis's spoils the first time it falls.
  3. THE HANGAR     behind the Flagship's SECRET 3 (a button on the antechamber's south-west pillar; the door in its south wall):
                    the dormant Mecha Rex, sat, dim - a rig with no host. All four in your pack and right-click it: they're taken,
                    it boots (lights, the roar), and its remote is yours; then it powers down for the next player.
THE MOUNT  an invisible, tamed, saddled horse (an empty saddle asset) scaled so its rider sits on the rig's saddle; the rig is
           placed on it every tick, turned with it. Right-click it to mount; WASD drives, jump jumps, sprint runs; sneak gets off.
           Owner only (anyone else is thrown off), never glowing, 200 health; at 30 it RETREATS (sent home, 2 minutes' rest).
  THE HOST MATHS  a horse's passenger attachment is 1.44375 x its scale (EntityTypes: HORSE ... passengerAttachments(1.44375f));
           a player rides with its feet 0.6 under that point (its hips 0.15 over it), so the saddle's seat is the point itself:
           1.44375 x HOSTSC = rex_art.SEAT y (7.023)  ->  HOSTSC = 4.8645 (the box: 1.3965 x 4.8645 = 6.79 wide, 1.6 x 4.8645 = 7.78
           tall - the rex's own height). The seat is SEAT z = 0.352 ahead of the rig's origin: the rig stands 0.352 behind the host.
  POSES    sit when nobody rides (it stops dead: speed 0); idle_a/b while still; walk_0..3 moving; run_0..3 sprinting forward (the
           rider's player-input predicate; speed 0.33 / 0.45). Footsteps (iron golem + warden, low) and dust at the feet.
  ITS ITEM (use)       call it: out -> beside you; else it's summoned beside you, sat. Sneak + use: home. One rex a player (the
                       other kind goes home). Not in the gutter, a heist or the vault, a market or crypt, or a Phase 2 dungeon.
  RIDING (use the item - or the wheel, if your rex is on it):
    level / up         ATOMIC BREATH (atomic) / LASER BREATH (mecha): breath_0 1 s, the plates lighting tail to neck, then breath_1
                       2 s - a beam from the mouth along your look; 8 to every hostile in it, every 10 ticks (vanilla's hurt
                       cooldown would swallow faster hits), the atomic's sets them alight with blue fire. 8 s.
    down past 50       STOMP (atomic): rear and slam - a 5-block shockwave, 12 and a knock. ROCKET FIST (mecha): the right forearm
                       flies 12 blocks along your look and back, 14 to what it hits. 5 s.
    up past 60         ROAR (both): hostiles within 12 slowed and weakened 5 s. 12 s.
  It never hurts players, tamed pets or followers (#bm:hostile only, the allies pass), nor is hurt by its owner.
THE MOUNTS PAGE (the Partner Wheel's "Mounts" button; codes 5640-5659, menu 5640): the rex (whistle or remote - one slot), the
  Vorn Skiff (skiff_key or mothership_key - one slot): off hand + use the wheel puts one on; the page calls it / sends it home, or
  takes it back off. Carrying the wheel counts as carrying it: the rex stays out, and riding, the wheel fires as the item would
  (the skiff's laser and bomb, the Mothership's cannon, the rex's breath). "Partners" goes back to the wheel."""
import math
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import rigfol as RF
import rigkit
import rex_art as A

PFX = 'p249'
SCALE = A.SCALE
SEAT_Y, SEAT_Z = A.SEAT[1], A.SEAT[2]
HORSE_ATTACH = 1.44375                       # (EntityTypes HORSE: passengerAttachments(1.44375f), scaled with the horse)
HOSTSC = round(SEAT_Y / HORSE_ATTACH, 4)     # 4.8645
HP, RETREAT, REST = 200, 30, 120             # host health; at or under RETREAT it retreats; then REST seconds before it comes again
WALK, RUN = 0.33, 0.45
CD = {'breath': 8, 'down': 5, 'roar': 12}    # seconds
KN = {'atomic': dict(n=1, name='Atomic Rex', col='#5ac8ff', item='atomic_whistle', tag='bm.rxa'),
      'mecha': dict(n=2, name='Mecha Rex', col='#8ab4ff', item='mecha_remote', tag='bm.rxm')}
DUR = {'sit': 10, 'idle_a': 20, 'idle_b': 20, 'roar': 6, 'breath_0': 10, 'breath_1': 4, 'stomp_0': 8, 'stomp_1': 3, 'tailswipe': 6,
       'mecha_fist': 3, **{f'walk_{i}': 5 for i in range(4)}, **{f'run_{i}': 4 for i in range(4)}}
MENU = 5640                                  # the Mounts page (its block: 5640-5659)
C_RX, C_RXOUT, C_SK, C_SKOUT, C_BACK, C_OPEN = MENU + 1, MENU + 2, MENU + 3, MENU + 4, MENU + 5, MENU + 6
holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
HOSTILE = 'type=#bm:hostile,tag=!bm.frogpet,tag=!bm.npc,tag=!bm.rxh'     # (bm.frogpet: the allies pass widens it to every follower)
sel = lambda p: f'@e[type=minecraft:item_display,tag=bm.rxsel,tag=bm.rxp_{p}]'
BLUE = '#5ac8ff'
SKIFF_C, MS_C = '#7dff6a', '#7aff6a'

# ================================================================== ITEMS
PROOF = {'minecraft:damage_resistant': {'types': '#bm:p249_proof'}}
item('atomic_whistle', TOTEM, 'Atomic Whistle', BLUE,
     ['A fossil claw, hollowed into a whistle. Its blue veins glow.', ('Use: call your Atomic Rex (again: to your side).', 'blue'),
      ('Sneak + use: send it home.', 'blue'), ('Riding, use it: look level - ATOMIC BREATH;', 'gray'), ('down - STOMP; straight up - ROAR.', 'gray'),
      ('It answers to you alone.', 'dark_gray')], model='bm:atomic_whistle', stack=1, cat='relic', glint=True, bold=True, comps=hold('none'))
item('mecha_remote', TOTEM, 'Mecha Rex Remote', '#8ab4ff',
     ['A chunky grey remote. One green button, one blue screen.', ('Use: call your Mecha Rex (again: to your side).', 'blue'),
      ('Sneak + use: send it home.', 'blue'), ('Riding, use it: look level - LASER BREATH;', 'gray'), ('down - ROCKET FIST; straight up - ROAR.', 'gray'),
      ('Built in the Armada\'s hidden hangar.', 'dark_gray')], model='bm:mecha_remote', stack=1, cat='alien', glint=True, bold=True, comps=hold('none'))
HOLD['atomic_whistle'] = f'bm:{PFX}/use_atomic'
HOLD['mecha_remote'] = f'bm:{PFX}/use_mecha'
item('rex_fossil', TOTEM, 'Rex Fossil', '#a8a196',
     ['A great fossil claw, cold and heavy, from deep under the world.', 'It hums when a storm is near.',
      ('Leave it on a lightning rod in a thunderstorm.', 'blue')], model='bm:rex_fossil', stack=1, cat='relic', comps=PROOF)
item('rex_egg', TOTEM, 'Rex Egg', '#7cc8ff',
     ['A stone-grey egg, scorched by lightning. Blue light pulses inside.', 'It is warm - and it wants to be warmer.',
      ('Drop it into lava, in the Nether, and wait.', 'blue')], model='bm:rex_egg', stack=1, cat='relic', glint=True, comps=PROOF)
for _i, (_part, _hint) in enumerate((('the head', 'Hidden in a forgotten hold of the Star-Forge.'), ('the body', 'Sealed behind a bulkhead on Dreadnought B.'),
                                     ('the legs', 'Kept in a room only an old friend can open.')), 1):
    item(f'mecha_blueprint_{_i}', TOTEM, f'Mecha Rex Blueprint {"I" * _i}', '#4c90e4',
         [f'A Vorn schematic: {_part} of a great machine.', ('Three blueprints and a Mecha Core:', 'blue'),
          ('the Flagship hides a hangar behind its antechamber.', 'blue'), (_hint, 'dark_gray')], model=f'bm:mecha_blueprint_{_i}', stack=1, cat='alien')
item('mecha_core', TOTEM, 'Mecha Core', '#5ab0ff',
     ['A Vorn reactor core, still humming - a machine\'s heart.', ('With the three Mecha Rex blueprints, wake what', 'blue'),
      ('sleeps in the Flagship\'s hidden hangar.', 'blue'), ('From the Hive Vault, or the Admiral\'s spoils.', 'dark_gray')],
     model='bm:mecha_core', stack=1, cat='alien', glint=True)
QUEST = ['rex_fossil', 'rex_egg', 'mecha_blueprint_1', 'mecha_blueprint_2', 'mecha_blueprint_3', 'mecha_core']
DIG = ['deepslate'] + [f'deepslate_{o}_ore' for o in ('coal', 'iron', 'copper', 'gold', 'redstone', 'emerald', 'lapis', 'diamond')]
RODS = ['lightning_rod'] + [f'{w}{a}_lightning_rod' for w in ('', 'waxed_') for a in ('exposed', 'weathered', 'oxidized')] + ['waxed_lightning_rod']


def host_nbt(k):
    c = KN[k]
    saddle = {'id': 'minecraft:saddle', 'count': Int(1), 'components': {
        'minecraft:equippable': {'slot': 'saddle', 'asset_id': 'bm:skiff_none', 'equip_sound': 'minecraft:entity.horse.saddle', 'allowed_entities': 'minecraft:horse'},
        'minecraft:custom_data': {'rxsaddle': B(1)}}}
    at = lambda a, v: {'id': f'minecraft:{a}', 'base': D(v)}
    return {'Tags': ['bm.rxh', c['tag'], 'bm.rxnew', 'bm.seen'], 'Tame': B(1), 'PersistenceRequired': B(1), 'Silent': B(1), 'Age': Int(0),
            'CustomName': T(f'The {c["name"]}', c['col'], bold=True), 'CustomNameVisible': B(0), 'DeathLootTable': 'minecraft:empty',
            'equipment': {'saddle': saddle}, 'drop_chances': {'saddle': F(0)}, 'Health': F(HP),
            'attributes': [at('max_health', HP), at('scale', HOSTSC), at('movement_speed', 0.0), at('jump_strength', 0.8), at('step_height', 1.5),
                           at('fall_damage_multiplier', 0.0), at('safe_fall_distance', 24), at('knockback_resistance', 1.0), at('armor', 10)],
            'active_effects': [{'id': 'minecraft:invisibility', 'duration': Int(-1), 'amplifier': B(0), 'show_particles': B(0), 'show_icon': B(0)},
                               {'id': 'minecraft:fire_resistance', 'duration': Int(-1), 'amplifier': B(0), 'show_particles': B(0), 'show_icon': B(0)}]}


def generate(G):
    fn, title, tellraw, give = G.fn, G.title, G.tellraw, G.give
    tick, second = G.FUNCS['tick'], G.FUNCS['loop/second']
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    PRE = [T('[', 'dark_gray'), T('Black Market', 'dark_purple', bold=True), T('] ', 'dark_gray')]
    snd = lambda s, v, p, r=32: f'playsound minecraft:{s} neutral @a[distance=..{r}] ~ ~ ~ {v} {p}'
    stat = {b: f'bm.rxd{i}' for i, b in enumerate(DIG)}
    objs = ['bm.rxid', 'bm.rxo', 'bm.rxpid', 'bm.rxs', 'bm.rxt', 'bm.rxw', 'bm.rxv', 'bm.rxhp', 'bm.rxrc', 'bm.rxcb', 'bm.rxcs', 'bm.rxcr',
            'bm.rxl', 'bm.rxb', 'bm.pwrx', 'bm.pwsk']
    G.FUNCS['load'][-1:-1] = ([f'scoreboard objectives add {o} dummy' for o in objs] +
                              [f'scoreboard objectives add {o} minecraft.mined:minecraft.{b}' for b, o in stat.items()] +
                              [f'scoreboard players set #{n} bm.rxv {n}' for n in (2, 10, 16, 20, 60)])
    G.OBJECTIVES += objs + list(stat.values())
    G.wjson('bm/tags/damage_type/p249_proof.json', {'values': [{'id': f'minecraft:{t}', 'required': False} for t in
                                                                ('in_fire', 'on_fire', 'lava', 'hot_floor', 'lightning_bolt', 'campfire')]})
    G.wjson('bm/tags/block/p249_rods.json', {'values': [{'id': f'minecraft:{r}', 'required': False} for r in RODS]})
    inp = lambda **k: {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:type_specific/player': {'input': k}}}
    G.wjson('bm/predicate/p249/moving.json', {'condition': 'minecraft:any_of', 'terms': [inp(forward=True), inp(backward=True), inp(left=True), inp(right=True)]})
    G.wjson('bm/predicate/p249/sprint.json', inp(forward=True, sprint=True))
    G.wjson('bm/predicate/p249/thunder.json', {'condition': 'minecraft:weather_check', 'thundering': True})
    for k, c in KN.items():
        G.wjson(f'bm/advancement/story/rex_{k}.json', {
            'parent': 'bm:story/root' if k == 'atomic' else 'bm:story/vexis', 'criteria': {'got': {'trigger': 'minecraft:impossible'}},
            'display': {'icon': {'id': 'minecraft:paper', 'components': {'minecraft:item_model': f'bm:{c["item"]}'}},
                        'title': T('King of the Monsters' if k == 'atomic' else 'Steel Kaiju', c['col']),
                        'description': T('Hatch an Atomic Rex from a storm-struck fossil, in Nether lava' if k == 'atomic' else
                                         'Wake the Mecha Rex in the Vorn Armada\'s hidden hangar', 'gray'), 'frame': 'challenge', 'hidden': True}})

    # ================================================================== THE RIG: its poses (each kind), its place
    for k in KN:
        used = ['sit', 'idle_a', 'idle_b', 'roar', 'breath_0', 'breath_1'] + [f'{g}_{i}' for g in ('walk', 'run') for i in range(4)] + \
               (['stomp_0', 'stomp_1'] if k == 'atomic' else ['mecha_fist'])
        for name in used:
            fn(f'{PFX}/pose/{k}/{name}', RF.pose(A, A.posed(name, k, charged=False), SCALE, DUR.get(name, 6), sel))
        for p in A.PLATED:
            fn(f'{PFX}/charge/{k}/{p}', [f'execute as {sel(p)} run data modify entity @s item.components."minecraft:item_model" set value "{A.model_name(p, k, "charged")}"'])
        fn(f'{PFX}/uncharge/{k}', [f'execute as {sel(p)} run data modify entity @s item.components."minecraft:item_model" set value "{A.model_name(p, k)}"' for p in A.PLATED])
        fn(f'{PFX}/rig/{k}', [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, ["bm.rxp", f"bm.rxp_{p}", "bm.rxpn"], SCALE, model=A.model_id(p, k), extra=dict(view_range=F(4.0)))}'
                              for p in A.PARTS])
    fn(f'{PFX}/place', RF.place(A, SCALE / 16, sel))

    # ================================================================== WHERE IT MAY COME (as the player)
    fn(f'{PFX}/allowed', ['execute if dimension bm:gutter run return 0', 'execute if dimension bm:hollow_throne run return 0',
                          'execute if entity @s[tag=bm.adv] run return 0', 'execute if entity @s[tag=bm.gvp] run return 0',
                          'execute if entity @e[type=minecraft:marker,tag=bm.zone_d,distance=..48] run return 0',
                          'execute if entity @e[type=minecraft:marker,tag=bm.crypt_ctrl,distance=..30] run return 0',
                          'execute if entity @e[type=minecraft:marker,tag=bm.mkt,distance=..80] run return 0', 'return 1'])
    fn(f'{PFX}/spot_ok', ['execute unless block ~ ~ ~ #bm:grap_pass run return 0', 'execute unless block ~ ~3 ~ #bm:grap_pass run return 0',
                          'execute unless block ~ ~6 ~ #bm:grap_pass run return 0', 'return 1'])
    for k, c in KN.items():
        fn(f'{PFX}/carries_{k}', [f'execute if items entity @s container.* {holds(c["item"])} run return 1',
                                  f'execute if items entity @s weapon.offhand {holds(c["item"])} run return 1',
                                  f'execute if items entity @s player.cursor {holds(c["item"])} run return 1',
                                  f'execute if entity @s[tag=bm.pwc] if score @s bm.pwrx matches {c["n"]} run return 1', 'return 0'])
    # (riding my own rex: its host's id is the one I last called)
    fn(f'{PFX}/riding_mine', ['scoreboard players operation #rxo bm.rxv = @s bm.rxo',
                              'execute on vehicle if entity @s[type=minecraft:horse,tag=bm.rxh] if score @s bm.rxid = #rxo bm.rxv run return 1', 'return 0'])
    fn(f'{PFX}/has_rider', ['execute on passengers if entity @s[type=minecraft:player] run return 1', 'return 0'])

    # ================================================================== THE ITEM: call it, send it home, or (riding) its powers
    for k, c in KN.items():
        fn(f'{PFX}/use_{k}', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                              f'execute if function bm:{PFX}/riding_mine run return run function bm:{PFX}/ride_use',
                              'execute if predicate bm:p20/sneaking run return run function bm:p249/home_cmd',
                              'execute if entity @s[predicate=bm:p29/has_vehicle] run return run ' + say('Get down first - the rex comes to you on the ground.'),
                              f'scoreboard players set #k bm.rxv {c["n"]}', f'function bm:{PFX}/call'])
    fn(f'{PFX}/home_cmd', ['scoreboard players operation #me bm.rxid = @s bm.rxo', 'scoreboard players set #out bm.rxv 0',
                           f'execute as @e[type=minecraft:horse,tag=bm.rxh] if score @s bm.rxid = #me bm.rxid run function bm:{PFX}/out_kind',
                           'execute if score #out bm.rxv matches 0 run return run ' + say('Your rex isn\'t out.'),
                           f'execute as @e[type=minecraft:horse,tag=bm.rxh] if score @s bm.rxid = #me bm.rxid at @s run function bm:{PFX}/gone',
                           'execute if score #out bm.rxv matches 1 run ' + title('@s', 'actionbar', [T('Your Atomic Rex', BLUE, bold=True), T(' stomps off home.', 'gray')]),
                           'execute if score #out bm.rxv matches 2 run ' + title('@s', 'actionbar', [T('Your Mecha Rex', '#8ab4ff', bold=True), T(' powers down and folds away home.', 'gray')])])
    fn(f'{PFX}/out_kind', [f'execute if entity @s[tag={c["tag"]}] run scoreboard players set #out bm.rxv {c["n"]}' for c in KN.values()] + ['tag @s add bm.rxfetch'])
    # (#k: the kind wanted. Out and the same kind: it comes to your side; the other kind out: that one goes home first)
    fn(f'{PFX}/call', ['execute unless function bm:p249/allowed run return run ' + say('The rex won\'t come here - not in a dungeon, a market, the vault or a heist.'),
                       'execute if score @s bm.rxrc matches 1.. run return run ' + title('@s', 'actionbar', [T('Your rex is still licking its wounds: ', 'gray'),
                                                                                                         {'score': {'name': '@s', 'objective': 'bm.rxrc'}, 'color': 'white'}, T(' s', 'gray')]),
                       'tag @e[type=minecraft:horse,tag=bm.rxfetch] remove bm.rxfetch',
                       'scoreboard players operation #me bm.rxid = @s bm.rxo', 'scoreboard players set #out bm.rxv 0',
                       f'execute as @e[type=minecraft:horse,tag=bm.rxh] if score @s bm.rxid = #me bm.rxid run function bm:{PFX}/out_kind',
                       'scoreboard players set #mode bm.rxv 0', 'execute if score #out bm.rxv = #k bm.rxv run scoreboard players set #mode bm.rxv 1',
                       f'execute if score #mode bm.rxv matches 0 as @e[type=minecraft:horse,tag=bm.rxfetch] at @s run function bm:{PFX}/gone',
                       'tag @s add bm.rxcaller',
                       f'execute rotated ~ 0 positioned ^-4 ^ ^2 if function bm:{PFX}/spot_ok run return run function bm:{PFX}/arrive',
                       f'execute rotated ~ 0 positioned ^4 ^ ^2 if function bm:{PFX}/spot_ok run return run function bm:{PFX}/arrive',
                       f'execute if function bm:{PFX}/spot_ok run return run function bm:{PFX}/arrive',
                       'tag @s remove bm.rxcaller', 'tag @e[type=minecraft:horse,tag=bm.rxfetch] remove bm.rxfetch',
                       say('No room for a rex here - find open ground, with the sky (or a high roof) over you.')])
    fn(f'{PFX}/arrive', ['tag @s remove bm.rxcaller', f'execute if score #mode bm.rxv matches 1 run return run function bm:{PFX}/fetch',
                         'tag @s add bm.rxcaller', 'scoreboard players add #rxn bm.rxid 1',
                         f'execute if score #k bm.rxv matches 1 rotated ~ 0 run summon minecraft:horse ~ ~ ~ {snbt(host_nbt("atomic"))}',
                         f'execute if score #k bm.rxv matches 2 rotated ~ 0 run summon minecraft:horse ~ ~ ~ {snbt(host_nbt("mecha"))}',
                         'scoreboard players operation @s bm.rxo = #rxn bm.rxid',
                         f'execute as @e[type=minecraft:horse,tag=bm.rxnew,distance=..2,limit=1] at @s run function bm:{PFX}/born',
                         'tag @s remove bm.rxcaller'])
    fn(f'{PFX}/fetch', ['execute rotated ~ 0 run tp @e[type=minecraft:horse,tag=bm.rxfetch,limit=1] ~ ~ ~ ~ 0',
                        'tag @e[type=minecraft:horse,tag=bm.rxfetch] remove bm.rxfetch',
                        'particle minecraft:poof ~ ~1 ~ 1.2 0.6 1.2 0.05 30', snd('entity.iron_golem.step', 1.4, 0.5),
                        title('@s', 'actionbar', T('Your rex comes thundering to your side.', BLUE))])
    born = ['execute rotated as @a[tag=bm.rxcaller,limit=1] run tp @s ~ ~ ~ ~ 0', 'scoreboard players operation @s bm.rxid = #rxn bm.rxid', 'scoreboard players operation @s bm.rxpid = @a[tag=bm.rxcaller,limit=1] bm.pid',
            'data modify entity @s Owner set from entity @a[tag=bm.rxcaller,limit=1] UUID',
            'scoreboard players set @s bm.rxs 0', 'scoreboard players set @s bm.rxw 99', 'scoreboard players set @s bm.rxt 0', f'scoreboard players set @s bm.rxhp {HP * 10}']
    born += [f'execute if entity @s[tag={c["tag"]}] rotated as @s rotated ~ 0 positioned ^ ^ ^-{SEAT_Z} run function bm:{PFX}/rig/{k}' for k, c in KN.items()]
    born += ['scoreboard players operation @e[type=minecraft:item_display,tag=bm.rxpn] bm.rxid = #rxn bm.rxid',
             'tag @e[type=minecraft:item_display,tag=bm.rxpn] remove bm.rxpn', 'tag @s remove bm.rxnew',
             f'execute if entity @s[tag=bm.rxa] run function bm:{PFX}/fx/arrive_atomic', f'execute if entity @s[tag=bm.rxm] run function bm:{PFX}/fx/arrive_mecha']
    fn(f'{PFX}/born', born)
    fn(f'{PFX}/fx/arrive_atomic', ['particle minecraft:explosion ~ ~0.5 ~ 1.5 0.2 1.5 0 6', 'particle minecraft:dust{color:[0.3,0.75,1.0],scale:2.0} ~ ~4 ~ 1.5 2.5 1.5 0 60',
                                   'particle minecraft:block{block_state:"minecraft:coarse_dirt"} ~ ~0.2 ~ 2 0.1 2 0.2 80',
                                   snd('entity.ravager.roar', 2, 0.5, 48), snd('entity.ender_dragon.growl', 1, 0.7, 48),
                                   title('@a[tag=bm.rxcaller]', 'actionbar', [T('The Atomic Rex', BLUE, bold=True), T(' answers! Right-click it to climb on.', 'gray')])])
    fn(f'{PFX}/fx/arrive_mecha', ['particle minecraft:electric_spark ~ ~3 ~ 1.5 2.5 1.5 0.3 120', 'particle minecraft:end_rod ~ ~3 ~ 1.5 2 1.5 0.05 40',
                                  'particle minecraft:poof ~ ~0.5 ~ 2 0.2 2 0.05 40',
                                  snd('block.beacon.activate', 2, 0.5, 48), snd('entity.iron_golem.repair', 2, 0.5, 48), snd('block.piston.extend', 2, 0.5, 48),
                                  title('@a[tag=bm.rxcaller]', 'actionbar', [T('The Mecha Rex', '#8ab4ff', bold=True), T(' boots up and stands by. Right-click it to climb into the cockpit.', 'gray')])])
    # (gone home: its rider set down, its rig and fist away, the host out of the world)
    fn(f'{PFX}/gone', ['execute on passengers run ride @s dismount', 'scoreboard players operation #gid bm.rxv = @s bm.rxid',
                       'execute as @e[type=minecraft:item_display,tag=bm.rxp] if score @s bm.rxid = #gid bm.rxv run kill @s',
                       'execute as @e[type=minecraft:item_display,tag=bm.rxfist] if score @s bm.rxid = #gid bm.rxv run kill @s',
                       'particle minecraft:poof ~ ~2 ~ 1.5 2 1.5 0.05 40', 'particle minecraft:dust{color:[0.3,0.75,1.0],scale:1.6} ~ ~3 ~ 1.5 2.5 1.5 0 40',
                       'item replace entity @s saddle with minecraft:air', 'tp @s ~ -400 ~', 'kill @s'])

    # ================================================================== EACH TICK, EACH REX
    tick.append(f'execute as @e[type=minecraft:horse,tag=bm.rxh] at @s run function bm:{PFX}/tick')
    fn(f'{PFX}/tick', ['tag @s add bm.rxme', 'scoreboard players operation #me bm.rxid = @s bm.rxid', 'scoreboard players operation #own bm.rxpid = @s bm.rxpid',
                       'execute as @e[type=minecraft:item_display,tag=bm.rxp] if score @s bm.rxid = #me bm.rxid run tag @s add bm.rxsel',
                       # (its health: a blow from its owner undone; at RETREAT, home it goes)
                       'execute store result score #h bm.rxv run data get entity @s Health 10',
                       f'execute if score #h bm.rxv < @s bm.rxhp on attacker if entity @s[type=minecraft:player] if score @s bm.pid = #own bm.rxpid run function bm:{PFX}/undo',
                       'scoreboard players operation @s bm.rxhp = #h bm.rxv',
                       f'execute if score #h bm.rxv matches ..{RETREAT * 10} run return run function bm:{PFX}/retreat',
                       # (its rider: the owner drives; anyone else is thrown off)
                       'scoreboard players set #g bm.rxv -1', f'execute on passengers if entity @s[type=minecraft:player] run function bm:{PFX}/rider'] +
       [f'execute if entity @s[tag={c["tag"]}] run function bm:{PFX}/k/{k}' for k, c in KN.items()] +
       [f'execute rotated as @s rotated ~ 0 positioned ^ ^ ^-{SEAT_Z} run function bm:{PFX}/place',
        'tag @e[type=minecraft:item_display,tag=bm.rxsel] remove bm.rxsel', 'tag @a[tag=bm.rxrider] remove bm.rxrider', 'tag @s remove bm.rxme'])
    fn(f'{PFX}/undo', ['execute store result entity @e[type=minecraft:horse,tag=bm.rxme,limit=1] Health float 0.1 run scoreboard players get @e[type=minecraft:horse,tag=bm.rxme,limit=1] bm.rxhp',
                       'scoreboard players operation #h bm.rxv = @e[type=minecraft:horse,tag=bm.rxme,limit=1] bm.rxhp'])
    fn(f'{PFX}/rider', [f'execute unless score @s bm.pid = #own bm.rxpid run return run function bm:{PFX}/throw', 'tag @s add bm.rxrider',
                        'scoreboard players set #g bm.rxv 0', 'execute if predicate bm:p249/moving run scoreboard players set #g bm.rxv 1',
                        'execute if predicate bm:p249/sprint run scoreboard players set #g bm.rxv 2'])
    fn(f'{PFX}/throw', ['ride @s dismount', 'effect give @s minecraft:slow_falling 3 0 true',
                        title('@s', 'actionbar', T('It shakes you off - this rex answers to its owner alone.', 'red'))])
    fn(f'{PFX}/retreat', ['tag @s remove bm.rxme', 'execute as @a if score @s bm.pid = #own bm.rxpid run function bm:p249/retreat_owner',
                          snd('entity.ravager.hurt', 2, 0.5, 48), f'function bm:{PFX}/gone'])
    fn(f'{PFX}/retreat_owner', [f'scoreboard players set @s bm.rxrc {REST}',
                                title('@s', 'actionbar', [T('Your rex is badly hurt - it retreats. ', 'red', bold=True), T(f'({REST // 60} minutes to recover.)', 'gray')])])
    # (gait: -1 nobody aboard (it sits, stock-still), 0 still, 1 walking, 2 running; a change starts its cycle and sets its pace)
    fn(f'{PFX}/gait', ['scoreboard players operation @s bm.rxw = #g bm.rxv', 'scoreboard players set @s bm.rxt 0',
                       'execute if score #g bm.rxv matches -1 run attribute @s minecraft:movement_speed base set 0.0',
                       f'execute if score #g bm.rxv matches 0..1 run attribute @s minecraft:movement_speed base set {WALK}',
                       f'execute if score #g bm.rxv matches 2 run attribute @s minecraft:movement_speed base set {RUN}'])
    at = lambda t, cmd: f'execute if score @s bm.rxt matches {t} {cmd[8:]}' if cmd.startswith('execute ') else f'execute if score @s bm.rxt matches {t} run {cmd}'
    atf = lambda f_, cmd: f'execute if score #f bm.rxv matches {f_} {cmd[8:]}' if cmd.startswith('execute ') else f'execute if score #f bm.rxv matches {f_} run {cmd}'
    steps = ['playsound minecraft:entity.iron_golem.step neutral @a[distance=..32] ~ ~ ~ 1.6 0.5',
             'playsound minecraft:entity.warden.step neutral @a[distance=..32] ~ ~ ~ 1.4 0.6']
    feet = lambda sx: [f'execute rotated as @s rotated ~ 0 positioned ^{sx * 1.4:.2f} ^ ^0.3 run particle minecraft:block{{block_state:"minecraft:coarse_dirt"}} ~ ~0.1 ~ 0.5 0.05 0.5 0 14',
                       f'execute rotated as @s rotated ~ 0 positioned ^{sx * 1.4:.2f} ^ ^0.3 run particle minecraft:poof ~ ~0.1 ~ 0.4 0.02 0.4 0.01 3']
    P = lambda k, name: f'function bm:{PFX}/pose/{k}/{name}'
    for k, c in KN.items():
        fn(f'{PFX}/k/{k}', [f'execute if score @s bm.rxs matches 0 run return run function bm:{PFX}/s/{k}/move',
                            f'execute if score @s bm.rxs matches 2 run return run function bm:{PFX}/s/{k}/breath',
                            f'execute if score @s bm.rxs matches 3 run return run function bm:{PFX}/s/{k}/down',
                            f'execute if score @s bm.rxs matches 4 run return run function bm:{PFX}/s/{k}/roar'])
        # ---- moving (or parked): sit / idle / walk / run
        fn(f'{PFX}/s/{k}/move', [f'execute unless score #g bm.rxv = @s bm.rxw run function bm:{PFX}/gait', 'scoreboard players add @s bm.rxt 1',
                                 f'execute if score @s bm.rxw matches -1 if score @s bm.rxt matches 1 run {P(k, "sit")}',
                                 f'execute if score @s bm.rxw matches 0 run function bm:{PFX}/s/{k}/idle',
                                 f'execute if score @s bm.rxw matches 1 run function bm:{PFX}/s/{k}/walk',
                                 f'execute if score @s bm.rxw matches 2 run function bm:{PFX}/s/{k}/run'])
        fn(f'{PFX}/s/{k}/idle', ['scoreboard players operation #f bm.rxv = @s bm.rxt', 'scoreboard players operation #f bm.rxv %= #60 bm.rxv',
                                 atf(1, P(k, 'idle_a')), atf(31, P(k, 'idle_b'))])
        fn(f'{PFX}/s/{k}/walk', ['scoreboard players operation #f bm.rxv = @s bm.rxt', 'scoreboard players operation #f bm.rxv %= #20 bm.rxv'] +
           [atf(1 + 5 * i, P(k, f'walk_{i}')) for i in range(4)] + [atf(3, l) for l in steps + feet(1)] + [atf(13, l) for l in steps + feet(-1)])
        fn(f'{PFX}/s/{k}/run', ['scoreboard players operation #f bm.rxv = @s bm.rxt', 'scoreboard players operation #f bm.rxv %= #16 bm.rxv'] +
           [atf(1 + 4 * i, P(k, f'run_{i}')) for i in range(4)] + [atf(3, l) for l in steps + feet(1)] + [atf(11, l) for l in steps + feet(-1)])
        # ---- the breath: breath_0 and the plates lighting up tail to neck (1 s), then breath_1 and the beam (2 s)
        (mo, md) = A.breath()
        mouth = f'^{mo[0]:.3f} ^{mo[1]:.3f} ^{mo[2] - SEAT_Z:.3f}'
        fire = [f'execute if function bm:{PFX}/has_rider rotated as @s rotated ~ 0 positioned {mouth} on passengers if entity @s[type=minecraft:player] rotated as @s run function bm:{PFX}/beam/{k}/go',
                f'execute unless function bm:{PFX}/has_rider rotated as @s rotated ~ 0 positioned {mouth} run function bm:{PFX}/beam/{k}/go']
        cs = ('block.respawn_anchor.charge', 1.6, 0.6) if k == 'atomic' else ('block.beacon.power_select', 1.6, 1.4)
        fire_snd = [snd('entity.ender_dragon.growl', 2, 0.5, 48), snd('entity.blaze.shoot', 1.5, 0.5, 48)] if k == 'atomic' else \
                   [snd('entity.guardian.attack', 2, 1.4, 48), snd('entity.warden.sonic_boom', 0.8, 1.6, 48)]
        fn(f'{PFX}/s/{k}/breath', ['scoreboard players add @s bm.rxt 1', at(1, P(k, 'breath_0')), at(1, snd(*cs))] +
           [at(1 + 3 * i, f'function bm:{PFX}/charge/{k}/{p}') for i, p in enumerate(A.CHARGE_ORDER)] +
           [at(1 + 3 * i, snd('block.amethyst_block.chime', 1.2, round(0.6 + 0.12 * i, 2))) for i in range(len(A.CHARGE_ORDER))] +
           [at(21, P(k, 'breath_1'))] + [at(21, l) for l in fire_snd] +
           ['scoreboard players operation #f bm.rxv = @s bm.rxt', 'scoreboard players operation #f bm.rxv %= #10 bm.rxv',
            'scoreboard players set #dmg bm.rxv 0', 'execute if score #f bm.rxv matches 1 run scoreboard players set #dmg bm.rxv 1',
            'scoreboard players operation #f bm.rxv = @s bm.rxt', 'scoreboard players operation #f bm.rxv %= #2 bm.rxv'] +
           [f'execute if score @s bm.rxt matches 21..60 if score #f bm.rxv matches 1 {l[8:]}' for l in fire] +      # (the beam every other tick; it hurts at t%10 = 1)
           [at(61, f'function bm:{PFX}/uncharge/{k}'), at(61, P(k, 'idle_a')), at(61, 'scoreboard players set @s bm.rxw 99'),
            at(61, 'scoreboard players set @s bm.rxs 0'), at(61, 'scoreboard players set @s bm.rxt 0')])     # (the timer's reset last)
        dust = 'dust{color:[0.2,0.6,1.0],scale:2.2}' if k == 'atomic' else 'dust{color:[0.65,0.95,1.0],scale:1.0}'
        ex = ['particle minecraft:soul_fire_flame ~ ~ ~ 0.18 0.18 0.18 0.01 1 force @a[distance=..64]'] if k == 'atomic' else \
             ['particle minecraft:electric_spark ~ ~ ~ 0.05 0.05 0.05 0.05 1 force @a[distance=..64]', 'particle minecraft:end_rod ~ ~ ~ 0 0 0 0 1 force @a[distance=..64]']
        fn(f'{PFX}/beam/{k}/go', ['scoreboard players set #rr bm.rxv 40', f'function bm:{PFX}/beam/{k}/step', 'tag @e[tag=bm.rxhit] remove bm.rxhit'])
        fn(f'{PFX}/beam/{k}/step', [f'particle minecraft:{dust} ~ ~ ~ 0.06 0.06 0.06 0 2 force @a[distance=..64]',
                                    'particle minecraft:end_rod ~ ~ ~ 0.04 0.04 0.04 0.005 1 force @a[distance=..64]'] + ex +
           [f'execute if score #dmg bm.rxv matches 1 as @e[{HOSTILE},tag=!bm.rxhit,distance=..1.7] at @s run function bm:{PFX}/beam/{k}/hit',
            'execute unless block ~ ~ ~ #bm:grap_pass run return run particle minecraft:explosion ~ ~ ~ 0.2 0.2 0.2 0 1',
            'scoreboard players remove #rr bm.rxv 1', f'execute if score #rr bm.rxv matches 1.. positioned ^ ^ ^0.6 run function bm:{PFX}/beam/{k}/step'])
        hit = ['tag @s add bm.rxhit', 'execute if entity @a[tag=bm.rxrider] run damage @s 8 minecraft:player_attack by @a[tag=bm.rxrider,limit=1]',
               'execute unless entity @a[tag=bm.rxrider] run damage @s 8 minecraft:generic']
        hit += ['scoreboard players set @s bm.rxb 4', 'tag @s add bm.rxburn', 'particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.5 0.3 0.02 14'] if k == 'atomic' else \
               ['particle minecraft:electric_spark ~ ~1 ~ 0.3 0.5 0.3 0.2 14']
        fn(f'{PFX}/beam/{k}/hit', hit)
        # ---- looking down: the stomp (atomic) / the rocket fist (mecha)
        if k == 'atomic':
            sp = rigkit.point(A, A.POSES['stomp_1'], *A.STOMP, scale=SCALE)
            ring = []
            for r, n in ((2.0, 12), (3.5, 18), (5.0, 24)):
                for j in range(n):
                    a = 2 * math.pi * j / n
                    ring.append(f'particle minecraft:block{{block_state:"minecraft:stone"}} ~{r * math.cos(a):.2f} ~0.2 ~{r * math.sin(a):.2f} 0.2 0.1 0.2 0.1 4')
            fn(f'{PFX}/stomp/wave', ring + ['particle minecraft:explosion ~ ~0.4 ~ 1.2 0.2 1.2 0 4',
                                            f'execute as @e[{HOSTILE},distance=..5] at @s run function bm:{PFX}/stomp/hit',
                                            snd('item.mace.smash_ground_heavy', 2, 0.5, 48), snd('entity.generic.explode', 1.2, 0.6, 48), snd('entity.warden.step', 2, 0.5, 48)])
            fn(f'{PFX}/stomp/hit', ['execute if entity @a[tag=bm.rxrider] run damage @s 12 minecraft:player_attack by @a[tag=bm.rxrider,limit=1]',
                                    'execute unless entity @a[tag=bm.rxrider] run damage @s 12 minecraft:generic',
                                    'effect give @s minecraft:levitation 1 1 true', 'effect give @s minecraft:slowness 3 2 true'])
            fn(f'{PFX}/s/{k}/down', ['scoreboard players add @s bm.rxt 1', at(1, P(k, 'stomp_0')), at(1, snd('entity.ravager.roar', 1.2, 0.7, 32)),
                                     at(14, P(k, 'stomp_1')), at(16, f'execute rotated as @s rotated ~ 0 positioned ^{sp[0]:.2f} ^ ^{sp[2] - SEAT_Z:.2f} run function bm:{PFX}/stomp/wave'),
                                     at(34, P(k, 'idle_a')), at(34, 'scoreboard players set @s bm.rxw 99'), at(34, 'scoreboard players set @s bm.rxs 0'),
                                     at(34, 'scoreboard players set @s bm.rxt 0')])
        else:
            fp = rigkit.point(A, A.POSES['mecha_fist'], 'forer', A.PIVOT['forer'], scale=SCALE)      # (the forearm's elbow: it leaves from where it was)
            fpos = f'^{fp[0]:.3f} ^{fp[1]:.3f} ^{fp[2] - SEAT_Z:.3f}'
            fist = {'Tags': ['bm.rxfist', 'bm.rxfnew'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': A.model_name('forer', 'mecha')}},
                    'item_display': 'fixed', 'teleport_duration': Int(1), 'view_range': F(4.0),
                    'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)], 'translation': [F(0)] * 3, 'scale': [F(SCALE)] * 3}}
            launch = [f'execute if function bm:{PFX}/has_rider rotated as @s rotated ~ 0 positioned {fpos} on passengers if entity @s[type=minecraft:player] rotated as @s run function bm:{PFX}/fist/launch',
                      f'execute unless function bm:{PFX}/has_rider rotated as @s rotated ~ 0 positioned {fpos} run function bm:{PFX}/fist/launch']
            fn(f'{PFX}/fist/launch', [f'summon minecraft:item_display ~ ~ ~ {snbt(fist)}', 'execute as @e[type=minecraft:item_display,tag=bm.rxfnew] run tp @s ~ ~ ~ ~ ~',
                                      'scoreboard players operation @e[type=minecraft:item_display,tag=bm.rxfnew] bm.rxid = #me bm.rxid',
                                      'scoreboard players operation @e[type=minecraft:item_display,tag=bm.rxfnew] bm.rxpid = #own bm.rxpid',
                                      'scoreboard players set @e[type=minecraft:item_display,tag=bm.rxfnew] bm.rxt 0', 'tag @e[type=minecraft:item_display,tag=bm.rxfnew] remove bm.rxfnew',
                                      snd('entity.firework_rocket.launch', 2, 0.5, 48), snd('block.piston.extend', 1.6, 0.6, 48),
                                      'particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.05 16', 'particle minecraft:electric_spark ~ ~ ~ 0.3 0.3 0.3 0.2 20'])
            fn(f'{PFX}/s/{k}/down', ['scoreboard players add @s bm.rxt 1', at(1, P(k, 'mecha_fist')), at(1, snd('block.piston.contract', 1.6, 0.5, 32))] +
               [at(4, f'execute as {sel("forer")} run data merge entity @s {{start_interpolation:0,interpolation_duration:1,transformation:{{scale:[0f,0f,0f]}}}}')] +
               [at(4, l) for l in launch] +
               [at(30, P(k, 'idle_a')), at(30, snd('block.piston.contract', 1.4, 0.7, 32)), at(30, 'scoreboard players set @s bm.rxw 99'),
                at(30, 'scoreboard players set @s bm.rxs 0'), at(30, 'scoreboard players set @s bm.rxt 0')])
            # (the fist: 12 out along the rider's look - back early off a wall - and 12 home; 14 to anything it meets, once)
            tick.append(f'execute as @e[type=minecraft:item_display,tag=bm.rxfist] at @s run function bm:{PFX}/fist/fly')
            fn(f'{PFX}/fist/fly', ['scoreboard players add @s bm.rxt 1', 'scoreboard players operation #fo bm.rxpid = @s bm.rxpid',
                                   'execute as @a if score @s bm.pid = #fo bm.rxpid run tag @s add bm.rxfo',
                                   'execute if score @s bm.rxt matches 1..12 unless block ^ ^ ^1 #bm:grap_pass run function bm:p249/fist/bounce',
                                   'execute if score @s bm.rxt matches 1..12 run tp @s ^ ^ ^1',
                                   'execute if score @s bm.rxt matches 13..24 run tp @s ^ ^ ^-1',
                                   'particle minecraft:soul_fire_flame ^ ^ ^-0.8 0.1 0.1 0.1 0.02 3', 'particle minecraft:electric_spark ~ ~ ~ 0.3 0.3 0.3 0.1 3',
                                   f'execute as @e[{HOSTILE},tag=!bm.rxfh,distance=..1.8] at @s run function bm:{PFX}/fist/hit',
                                   'tag @a[tag=bm.rxfo] remove bm.rxfo',
                                   'execute if score @s bm.rxt matches 25.. run function bm:p249/fist/done'])
            fn(f'{PFX}/fist/bounce', ['scoreboard players operation #b bm.rxv = @s bm.rxt', 'scoreboard players set @s bm.rxt 25', 'scoreboard players operation @s bm.rxt -= #b bm.rxv',
                                      'particle minecraft:explosion ^ ^ ^1 0.1 0.1 0.1 0 1', 'playsound minecraft:block.anvil.land neutral @a[distance=..24] ~ ~ ~ 1 0.6'])
            fn(f'{PFX}/fist/hit', ['tag @s add bm.rxfh', 'execute if entity @a[tag=bm.rxfo] run damage @s 14 minecraft:player_attack by @a[tag=bm.rxfo,limit=1]',
                                   'execute unless entity @a[tag=bm.rxfo] run damage @s 14 minecraft:generic', 'particle minecraft:explosion ~ ~1 ~ 0.2 0.2 0.2 0 1',
                                   'playsound minecraft:entity.iron_golem.attack neutral @a[distance=..24] ~ ~ ~ 1.4 0.6'])
            fn(f'{PFX}/fist/done', ['tag @e[tag=bm.rxfh] remove bm.rxfh', 'playsound minecraft:block.piston.contract neutral @a[distance=..24] ~ ~ ~ 1 1.2', 'kill @s'])
        # ---- the roar (both): hostiles within 12 slowed and weakened
        rsnd = [snd('entity.ravager.roar', 2, 0.5, 64), snd('entity.ender_dragon.growl', 1.6, 0.6, 64)] if k == 'atomic' else \
               [snd('entity.ravager.roar', 1.6, 0.6, 64), snd('entity.warden.roar', 1.6, 0.6, 64), snd('block.respawn_anchor.deplete', 1.4, 0.5, 64)]
        mr = rigkit.point(A, A.POSES['roar'], *A.MOUTH, scale=SCALE)
        fn(f'{PFX}/s/{k}/roar', ['scoreboard players add @s bm.rxt 1', at(1, P(k, 'roar'))] + [at(4, l) for l in rsnd] +
           [at(8, f'execute rotated as @s rotated ~ 0 positioned ^{mr[0]:.2f} ^{mr[1]:.2f} ^{mr[2] - SEAT_Z:.2f} run particle minecraft:sonic_boom ~ ~ ~ 0 0 0 0 1 force @a[distance=..64]'),
            at(8, 'particle minecraft:poof ~ ~1 ~ 6 0.4 6 0.05 120'), at(8, f'execute as @e[{HOSTILE},distance=..12] at @s run function bm:{PFX}/roar_hit'),
            at(40, P(k, 'idle_a')), at(40, 'scoreboard players set @s bm.rxw 99'), at(40, 'scoreboard players set @s bm.rxs 0'), at(40, 'scoreboard players set @s bm.rxt 0')])
    fn(f'{PFX}/roar_hit', ['effect give @s minecraft:slowness 5 2', 'effect give @s minecraft:weakness 5 1', 'particle minecraft:smoke ~ ~1.2 ~ 0.3 0.4 0.3 0.02 8'])
    # (blue fire: the atomic breath's burn, a few seconds)
    second.append(f'execute as @e[tag=bm.rxburn] at @s run function bm:{PFX}/burn')
    fn(f'{PFX}/burn', ['scoreboard players remove @s bm.rxb 1', 'damage @s 2 minecraft:on_fire', 'particle minecraft:soul_fire_flame ~ ~0.8 ~ 0.3 0.5 0.3 0.03 16',
                       'execute if score @s bm.rxb matches ..0 run tag @s remove bm.rxburn'])

    # ================================================================== RIDING: the item's (or the wheel's) use picks a power by your look
    fn(f'{PFX}/ride_use', ['scoreboard players operation #me bm.rxid = @s bm.rxo',
                           f'execute if entity @s[x_rotation=-90..-60] run return run function bm:{PFX}/try/roar',
                           f'execute if entity @s[x_rotation=50..90] run return run function bm:{PFX}/try/down', f'function bm:{PFX}/try/breath'])
    busy = ['scoreboard players set #busy bm.rxv 0', 'execute on vehicle unless score @s bm.rxs matches 0 run scoreboard players set #busy bm.rxv 1',
            'execute if score #busy bm.rxv matches 1 run return run ' + say('It\'s busy - wait for it.')]
    cdl = lambda o, word: 'execute if score @s %s matches 1.. run return run ' % o + title('@s', 'actionbar', [T(word + ' recharging: ', 'gray'), {'score': {'name': '@s', 'objective': o}, 'color': 'white'}, T(' s', 'gray')])
    go = lambda st: ['execute on vehicle run scoreboard players set @s bm.rxt 0', f'execute on vehicle run scoreboard players set @s bm.rxs {st}']
    fn(f'{PFX}/try/breath', [cdl('bm.rxcb', 'The breath')] + busy + [f'scoreboard players set @s bm.rxcb {CD["breath"]}'] + go(2))
    fn(f'{PFX}/try/down', [cdl('bm.rxcs', 'That')] + busy + [f'scoreboard players set @s bm.rxcs {CD["down"]}'] + go(3))
    fn(f'{PFX}/try/roar', [cdl('bm.rxcr', 'The roar')] + busy + [f'scoreboard players set @s bm.rxcr {CD["roar"]}'] + go(4))
    second.append('scoreboard players remove @a[scores={bm.rxcb=1..}] bm.rxcb 1')
    second.append('scoreboard players remove @a[scores={bm.rxcs=1..}] bm.rxcs 1')
    second.append('scoreboard players remove @a[scores={bm.rxcr=1..}] bm.rxcr 1')
    second.append('scoreboard players remove @a[scores={bm.rxrc=1..}] bm.rxrc 1')
    # (riding: what's ready, every second, on the actionbar)
    rdy = lambda o, word: [T(word + ' ', 'gray'), {'score': {'name': '@s', 'objective': o}, 'color': 'white'}, T('s  ', 'dark_gray')]
    for k, c in KN.items():
        down = 'Stomp' if k == 'atomic' else 'Fist'
        fn(f'{PFX}/hud_{k}', [title('@s', 'actionbar', [T(c['name'].upper() + '  ', c['col'], bold=True)] + rdy('bm.rxcb', 'Breath') + rdy('bm.rxcs', down) + rdy('bm.rxcr', 'Roar') +
                                    [T('(look level / down / up)', 'dark_gray')])])
    fn(f'{PFX}/hud', ['scoreboard players set #hk bm.rxv 0'] + [f'execute on vehicle if entity @s[tag={c["tag"]}] run scoreboard players set #hk bm.rxv {c["n"]}' for c in KN.values()] +
       [f'execute if score #hk bm.rxv matches {c["n"]} run function bm:{PFX}/hud_{k}' for k, c in KN.items()])
    second.append(f'execute as @a[predicate=bm:p29/has_vehicle] if function bm:{PFX}/riding_mine run function bm:{PFX}/hud')

    # ================================================================== EACH SECOND: its owner near and carrying it, the place allowed; strays cleaned up
    second.append(f'execute as @e[type=minecraft:horse,tag=bm.rxh] at @s run function bm:{PFX}/watch')
    fn(f'{PFX}/watch', ['scoreboard players operation #me bm.rxid = @s bm.rxid', 'scoreboard players operation #own bm.rxpid = @s bm.rxpid',
                        'tag @a remove bm.rxown', 'execute as @a[distance=..160] if score @s bm.pid = #own bm.rxpid if score @s bm.rxo = #me bm.rxid run tag @s add bm.rxown',
                        f'execute unless entity @a[tag=bm.rxown] run return run function bm:{PFX}/gone'] +
       [f'execute if entity @s[tag={c["tag"]}] as @a[tag=bm.rxown] unless function bm:{PFX}/carries_{k} run return run function bm:{PFX}/left_{k}' for k, c in KN.items()] +
       [f'execute as @a[tag=bm.rxown] unless function bm:{PFX}/allowed run return run function bm:{PFX}/refused',
        # (the horse's own inventory: its saddle back if taken, any armour put on it given back)
        f'execute unless items entity @s saddle *[minecraft:custom_data~{{rxsaddle:1b}}] run function bm:{PFX}/resaddle',
        f'execute if items entity @s armor.body * run function bm:{PFX}/unarmor', 'tag @a remove bm.rxown'])
    for k, c in KN.items():
        fn(f'{PFX}/left_{k}', [title('@s', 'actionbar', [T(f'Without its {ITEMS[c["item"]]["name"]}, your {c["name"]}', c['col']), T(' wanders off home.', 'gray')]),
                               'execute as @e[type=minecraft:horse,tag=bm.rxh] if score @s bm.rxid = #me bm.rxid at @s run function bm:p249/gone', 'tag @s remove bm.rxown'])
    fn(f'{PFX}/refused', [say('Your rex won\'t follow you here - it heads home.'),
                          'execute as @e[type=minecraft:horse,tag=bm.rxh] if score @s bm.rxid = #me bm.rxid at @s run function bm:p249/gone', 'tag @s remove bm.rxown'])
    saddle = host_nbt('atomic')['equipment']['saddle']
    fn(f'{PFX}/resaddle', [f'item replace entity @s saddle with minecraft:saddle[{",".join(f"{kk}={snbt(vv)}" for kk, vv in saddle["components"].items())}]'])
    fn(f'{PFX}/unarmor', ['summon minecraft:item ~ ~1 ~ {Tags:["bm.rxarm"],PickupDelay:0s,Item:{id:"minecraft:stone",count:1}}',
                          'data modify entity @e[type=minecraft:item,tag=bm.rxarm,limit=1] Item set from entity @s equipment.body',
                          'tag @e[type=minecraft:item,tag=bm.rxarm] remove bm.rxarm', 'item replace entity @s armor.body with minecraft:air'])
    second.append('clear @a *[minecraft:custom_data~{rxsaddle:1b}]')
    # (a part whose host is gone - killed outright, unloaded and left - goes too)
    second += ['tag @e[type=minecraft:item_display,tag=bm.rxp] add bm.rxorph', f'execute as @e[type=minecraft:horse,tag=bm.rxh] run function bm:{PFX}/keep',
               'kill @e[type=minecraft:item_display,tag=bm.rxorph]']
    fn(f'{PFX}/keep', ['scoreboard players operation #kid bm.rxv = @s bm.rxid',
                       'execute as @e[type=minecraft:item_display,tag=bm.rxorph] if score @s bm.rxid = #kid bm.rxv run tag @s remove bm.rxorph'])

    # ================================================================== ATOMIC 1: THE FOSSIL (deepslate under y 0)
    for b, o in stat.items():
        tick.append(f'execute as @a[scores={{{o}=1..}}] at @s run function bm:{PFX}/fos/dig')
    fn(f'{PFX}/fos/dig', [f'scoreboard players set @s {o} 0' for o in stat.values()] +
       ['execute unless entity @s[y=-80,dy=79.9] run return 0', 'execute if entity @s[tag=bm.rxhatch] run return 0',
        f'execute if items entity @s container.* {holds("rex_fossil")} run return 0', f'execute if items entity @s container.* {holds("rex_egg")} run return 0',
        f'execute if items entity @s weapon.offhand {holds("rex_fossil")} run return 0', f'execute if items entity @s weapon.offhand {holds("rex_egg")} run return 0',
        'execute store result score #r bm.rxv run random value 1..400', 'execute if score #r bm.rxv matches 1 run function bm:p249/fos/found'])
    fn(f'{PFX}/fos/found', [give('rex_fossil'), 'playsound minecraft:block.bone_block.break player @s ~ ~ ~ 1 0.5', 'playsound minecraft:block.trial_spawner.about_to_spawn_item player @s ~ ~ ~ 0.8 0.6',
                            'particle minecraft:block{block_state:"minecraft:bone_block"} ~ ~1 ~ 0.5 0.5 0.5 0.1 30',
                            tellraw('@s', [T('Your pick rings on something that isn\'t rock... ', 'gray', italic=True), T('a REX FOSSIL', '#cfc8ba', bold=True),
                                           T(' - a great claw, cold and heavy. It hums when the sky darkens.', 'gray', italic=True)])])
    # ================================================================== ATOMIC 2: THE LIGHTNING (the fossil on a rod, in a storm)
    second.append(f'execute as @e[type=minecraft:item] if items entity @s contents {holds("rex_fossil")} at @s run function bm:{PFX}/fos/rod')
    near_rod = [f'execute positioned ~{dx} ~{dy} ~{dz} if block ~ ~ ~ #bm:p249_rods run return 1' for dy in (-0.4, -1, 0) for dx in (0, -1, 1) for dz in (0, -1, 1)]
    fn(f'{PFX}/fos/near_rod', near_rod + ['return 0'])
    fn(f'{PFX}/fos/rod', [f'execute unless function bm:{PFX}/fos/near_rod run return 0', 'data modify entity @s Age set value -32768s',
                          'particle minecraft:electric_spark ~ ~0.3 ~ 0.2 0.2 0.2 0.05 3',
                          'execute unless predicate bm:p249/thunder run return 0', 'execute store result score #r bm.rxv run random value 1..20',
                          'execute if score #r bm.rxv matches 1 run function bm:p249/fos/strike'])
    fn(f'{PFX}/fos/strike', ['summon minecraft:lightning_bolt ~ ~ ~', 'loot spawn ~ ~0.3 ~ loot bm:items/rex_egg',
                             'execute as @e[type=minecraft:item,distance=..1.5] if items entity @s contents *[minecraft:custom_data~{bm:"rex_egg"}] run function bm:p249/fos/keep_egg',
                             'particle minecraft:dust{color:[0.3,0.75,1.0],scale:2.0} ~ ~1 ~ 0.8 1.2 0.8 0 80', 'particle minecraft:end_rod ~ ~1 ~ 0.6 1 0.6 0.1 40',
                             'particle minecraft:electric_spark ~ ~0.5 ~ 0.6 0.6 0.6 0.4 60',
                             tellraw('@p[distance=..64]', [T('The lightning finds the fossil - ', '#7cc8ff'), T('and the bone cracks open around something warm. ', 'gray', italic=True),
                                                           T('A REX EGG.', BLUE, bold=True), T(' (It wants heat. Real heat.)', 'dark_gray')]),
                             'kill @s'])
    fn(f'{PFX}/fos/keep_egg', ['data modify entity @s Age set value -32768s', 'data modify entity @s Invulnerable set value 1b'])
    # ================================================================== ATOMIC 3: THE HATCHING (the egg in Nether lava, 60 s)
    second.append(f'execute as @e[type=minecraft:item] if items entity @s contents {holds("rex_egg")} at @s run function bm:{PFX}/egg/lava')
    fn(f'{PFX}/egg/lava', ['execute unless dimension minecraft:the_nether run return run scoreboard players set @s bm.rxl 0',
                           'execute unless block ~ ~ ~ minecraft:lava unless block ~ ~-0.3 ~ minecraft:lava run return run scoreboard players set @s bm.rxl 0',
                           'data modify entity @s Age set value -32768s', 'scoreboard players add @s bm.rxl 1',
                           'particle minecraft:soul_fire_flame ~ ~0.4 ~ 0.2 0.2 0.2 0.02 4', 'particle minecraft:dust{color:[0.3,0.75,1.0],scale:1.2} ~ ~0.5 ~ 0.3 0.3 0.3 0 4',
                           'execute if score @s bm.rxl matches 20 run playsound minecraft:block.sniffer_egg.crack neutral @a[distance=..24] ~ ~ ~ 1 0.5',
                           'execute if score @s bm.rxl matches 40 run playsound minecraft:block.sniffer_egg.crack neutral @a[distance=..24] ~ ~ ~ 1.2 0.6',
                           'execute if score @s bm.rxl matches 40 run ' + tellraw('@a[distance=..24]', [T('The egg rocks in the lava. Something inside is ', 'gray', italic=True), T('knocking.', BLUE, italic=True)]),
                           'execute if score @s bm.rxl matches 55 run playsound minecraft:block.sniffer_egg.crack neutral @a[distance=..24] ~ ~ ~ 1.4 0.7',
                           'execute if score @s bm.rxl matches 60.. run function bm:p249/egg/hatch'])
    fn(f'{PFX}/egg/hatch', ['tag @a remove bm.rxthr', 'data remove storage bm:tmp rx.th', 'data modify storage bm:tmp rx.th set from entity @s Thrower',
                            f'execute as @a[distance=..48] run function bm:{PFX}/egg/thrower',
                            'execute unless entity @a[tag=bm.rxthr] run tag @p[distance=..32,gamemode=!spectator] add bm.rxthr',
                            'execute unless entity @a[tag=bm.rxthr] run return 0',
                            'particle minecraft:end_rod ~ ~6 ~ 0.3 6 0.3 0.02 300 force @a[distance=..96]',
                            'particle minecraft:dust{color:[0.3,0.75,1.0],scale:3.0} ~ ~8 ~ 0.4 8 0.4 0 300 force @a[distance=..96]',
                            'particle minecraft:soul_fire_flame ~ ~1 ~ 1 1 1 0.2 80', 'particle minecraft:explosion_emitter ~ ~1 ~ 0 0 0 0 1',
                            'playsound minecraft:block.sniffer_egg.hatch neutral @a[distance=..48] ~ ~ ~ 2 0.5', 'playsound minecraft:entity.ravager.roar neutral @a[distance=..96] ~ ~ ~ 3 0.5',
                            'playsound minecraft:entity.ender_dragon.growl neutral @a[distance=..96] ~ ~ ~ 2 0.6',
                            f'execute as @a[tag=bm.rxthr,limit=1] run function bm:{PFX}/egg/gift', 'tag @a remove bm.rxthr', 'kill @s'])
    fn(f'{PFX}/egg/thrower', ['data modify storage bm:tmp rx.u set from storage bm:tmp rx.th',
                              'execute store success score #df bm.rxv run data modify storage bm:tmp rx.u set from entity @s UUID',
                              'execute if score #df bm.rxv matches 0 if data storage bm:tmp rx.th run tag @s add bm.rxthr'])
    fn(f'{PFX}/egg/gift', [give('atomic_whistle'), 'tag @s add bm.rxhatch', 'advancement grant @s only bm:story/rex_atomic',
                           'title @s times 10 70 20', title('@s', 'title', T('THE ATOMIC REX HATCHES', BLUE, bold=True)),
                           title('@s', 'subtitle', T('...and it already thinks you are its mother.', '#c8ecff', italic=True)),
                           tellraw('@s', PRE + [T('The Atomic Whistle', BLUE, bold=True), T(' is yours. Use it on open ground to call your rex; right-click it to ride.', 'gray')])])

    # ================================================================== MECHA 1-2: THE BLUEPRINTS (relic pedestals) AND THE CORE
    for kk, n in (('secret1', 1), ('secret2', 2)):
        G.FUNCS[f'p241/relic/take_{kk}'].append(f'execute unless entity @s[tag=bm.rxbp{n}] run function bm:{PFX}/bp/{n}')
    import p2.armadacfg as AC
    for kk in AC.HIDDEN:
        G.FUNCS[f'p241/relic/take_{kk}'].append(f'execute unless entity @s[tag=bm.rxbp3] run function bm:{PFX}/bp/3')
    where = {1: 'tucked under the relic\'s plinth', 2: 'folded in the pedestal\'s base', 3: 'pinned beneath the relic'}
    for n in (1, 2, 3):
        fn(f'{PFX}/bp/{n}', [f'tag @s add bm.rxbp{n}', give(f'mecha_blueprint_{n}'), 'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.6',
                             tellraw('@s', [T('  ' + where[n][0].upper() + where[n][1:] + ': ', 'gray'), T(f'Mecha Rex Blueprint {"I" * n}', '#4c90e4', bold=True),
                                            T(' - a Vorn schematic of something very big, and very much asleep.', 'gray', italic=True)])])
    G.FUNCS['p242/first'].append(f'execute unless entity @s[tag=bm.rxcore] run function bm:{PFX}/core')
    vo = G.FUNCS['p241/vault/open']
    vo.insert(1, f'execute unless entity @s[tag=bm.rxcore] run function bm:{PFX}/core')
    fn(f'{PFX}/core', ['tag @s add bm.rxcore', give('mecha_core'), 'playsound minecraft:block.beacon.power_select player @s ~ ~ ~ 1 0.6',
                       tellraw('@s', [T('  Among the spoils: ', 'gray'), T('a Mecha Core', '#5ab0ff', bold=True), T(' - a reactor heart, still humming, wired for something with legs.', 'gray', italic=True)])])

    # ================================================================== MECHA 3: THE HANGAR (a marker the builder places: B.hangar)
    dim = {'block': Int(3), 'sky': Int(3)}
    second.append(f'execute as @e[type=minecraft:marker,tag=bm.rxhang,tag=!bm.rxon] at @s if entity @a[distance=..48] run function bm:{PFX}/hang/raise')
    fn(f'{PFX}/hang/raise', ['tag @s add bm.rxon', 'scoreboard players set @s bm.rxs 0',
                             'kill @e[type=minecraft:item_display,tag=bm.rxdm,distance=..16]', 'kill @e[type=minecraft:interaction,tag=bm.rxhi,distance=..16]'] +
       [f'execute rotated as @s rotated ~ 0 run summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, ["bm.rxdm", f"bm.rxp_{p}", "bm.rxsel"], SCALE, model=A.model_id(p, "mecha"), extra=dict(view_range=F(4.0), brightness=dim))}'
        for p in A.PARTS] +
       ['execute rotated as @s rotated ~ 0 run function bm:p249/place', P('mecha', 'sit'),
        'tag @e[type=minecraft:item_display,tag=bm.rxsel] remove bm.rxsel',
        'execute rotated as @s rotated ~ 0 positioned ^ ^ ^2.5 run summon minecraft:interaction ~ ~ ~ {Tags:["bm.rxhi"],width:4.0f,height:5.5f,response:1b}'])
    second.append(f'execute as @e[type=minecraft:marker,tag=bm.rxhang,tag=bm.rxon,scores={{bm.rxs=0}}] at @s if entity @a[distance=..14] run function bm:{PFX}/hang/hum')
    fn(f'{PFX}/hang/hum', ['execute store result score #r bm.rxv run random value 1..4',
                           'execute if score #r bm.rxv matches 1 run particle minecraft:electric_spark ~ ~5 ~ 0.6 0.6 0.6 0.1 4',
                           'execute if score #r bm.rxv matches 1 run playsound minecraft:block.beacon.ambient block @a[distance=..14] ~ ~ ~ 0.5 0.5'])
    tick.append(f'execute as @e[type=minecraft:interaction,tag=bm.rxhi] if data entity @s interaction at @s run function bm:{PFX}/hang/click')
    fn(f'{PFX}/hang/click', [f'execute on target run function bm:{PFX}/hang/try', 'data remove entity @s interaction'])
    need = [('mecha_blueprint_1', 'Blueprint I'), ('mecha_blueprint_2', 'Blueprint II'), ('mecha_blueprint_3', 'Blueprint III'), ('mecha_core', 'a Mecha Core')]
    fn(f'{PFX}/hang/try', ['execute if entity @e[type=minecraft:marker,tag=bm.rxhang,distance=..12,scores={bm.rxs=1}] run return run ' + say('It is already waking...'),
                           'scoreboard players set #n bm.rxv 0'] +
       [f'execute if items entity @s container.* {holds(i)} run scoreboard players add #n bm.rxv 1' for i, _ in need] +
       ['execute unless score #n bm.rxv matches 4 run return run ' + tellraw('@s', [T('A machine the size of a house, cold and grey. ', 'gray', italic=True), T('To wake it you need: ', 'gray')] +
                                                                              sum([[T(nm, '#4c90e4'), T(', ' if j < 3 else '.', 'gray')] for j, (_, nm) in enumerate(need)], [])),
        'tag @s add bm.rxwaker'] +
       [f'clear @s {holds(i)} 1' for i, _ in need] +
       [give('mecha_remote'), 'tag @s add bm.rxmecha', 'advancement grant @s only bm:story/rex_mecha',
        'title @s times 10 70 20', title('@s', 'title', T('THE MECHA REX', '#8ab4ff', bold=True)), title('@s', 'subtitle', T('online. awaiting its pilot.', '#c8e0ff', italic=True)),
        tellraw('@s', PRE + [T('The Mecha Rex Remote', '#8ab4ff', bold=True), T(' is yours. Out on open ground, use it to call your Mecha Rex; right-click it to ride.', 'gray')]),
        'execute as @e[type=minecraft:marker,tag=bm.rxhang,distance=..12,sort=nearest,limit=1] run function bm:p249/hang/wake', 'tag @s remove bm.rxwaker'])
    fn(f'{PFX}/hang/wake', ['scoreboard players set @s bm.rxs 1', 'scoreboard players set @s bm.rxt 0'])
    tick.append(f'execute as @e[type=minecraft:marker,tag=bm.rxhang,scores={{bm.rxs=1}}] at @s run function bm:{PFX}/hang/boot')
    lit = lambda on: 'execute as @e[type=minecraft:item_display,tag=bm.rxsel] run ' + ('data remove entity @s brightness' if on else 'data merge entity @s[type=minecraft:item_display] {brightness:{block:3,sky:3}}')
    fn(f'{PFX}/hang/boot', ['scoreboard players add @s bm.rxt 1', 'tag @e[type=minecraft:item_display,tag=bm.rxdm,distance=..16] add bm.rxsel',
                            at(1, lit(True)), at(1, P('mecha', 'idle_a')), at(1, snd('block.beacon.activate', 2, 0.6, 32)), at(1, snd('entity.iron_golem.repair', 1.6, 0.5, 32)),
                            at(1, 'particle minecraft:electric_spark ~ ~4 ~ 1.5 2.5 1.5 0.3 120'), at(12, snd('block.piston.extend', 1.6, 0.5, 32)),
                            at(24, P('mecha', 'roar')), at(26, snd('entity.ravager.roar', 2, 0.6, 48)), at(26, snd('entity.warden.roar', 1.6, 0.7, 48)),
                            at(26, 'particle minecraft:end_rod ~ ~6 ~ 2 2 2 0.1 80'), at(90, P('mecha', 'sit')), at(90, snd('block.beacon.deactivate', 1.6, 0.6, 32)),
                            at(110, lit(False)), at(110, 'scoreboard players set @s bm.rxs 0'), at(110, 'scoreboard players set @s bm.rxt 0'),
                            'tag @e[type=minecraft:item_display,tag=bm.rxsel] remove bm.rxsel'])
    # (the Armada (re)placed: its hangar's rig and interaction go with the rest - the marker comes back with the template)
    bt = G.FUNCS['p241/build/try']
    j = bt.index('scoreboard players set #abuilt bm.p2 0')
    from phase241 import END, BOX
    bt[j:j] = [f'execute in {END} run kill @e[type=minecraft:item_display,tag=bm.rxdm,{BOX}]', f'execute in {END} run kill @e[type=minecraft:interaction,tag=bm.rxhi,{BOX}]']

    # ================================================================== THE MOUNTS PAGE (off the Partner Wheel)
    import sys
    import phase28 as P28
    P179 = sys.modules.get('phase179')                 # (the build has it; the wheel's menu code, its purple)
    WM = getattr(P179, 'WMENU', 3350)
    icon = lambda iid, col: {'type': 'object', 'object': 'atlas', 'atlas': 'minecraft:items', 'sprite': 'bm:item/' + ITEMS[iid]['comps']['minecraft:item_model'].split(':', 1)[1],
                             'fallback': {'text': '◆', 'color': col}}
    MK = {1: ('atomic_whistle', 'Atomic Rex', BLUE), 2: ('mecha_remote', 'Mecha Rex', '#8ab4ff')}
    SK = {1: ('skiff_key', 'Vorn Skiff', SKIFF_C), 2: ('mothership_key', 'Mothership', MS_C)}
    # (off hand + the wheel: on it goes)
    use = G.FUNCS['p179/w/use']
    adds = [f'execute if function bm:{PFX}/riding_mine if score @s bm.pwrx matches 1.. run return run function bm:{PFX}/ride_use',
            f'execute if function bm:p35/skiff/riding if score @s bm.pwsk matches 1 run return run function bm:p35/skiff/use',
            f'execute if function bm:p35/skiff/riding if score @s bm.pwsk matches 2 run return run function bm:p242/ms/use']
    adds += [f'execute if items entity @s weapon.offhand {holds(MK[n][0])} run return run function bm:{PFX}/w/add_rx{n}' for n in MK]
    adds += [f'execute if items entity @s weapon.offhand {holds(SK[n][0])} run return run function bm:{PFX}/w/add_sk{n}' for n in SK]
    use[1:1] = adds
    for slot, D_, obj, key, what in (('rx', MK, 'bm.pwrx', 'rx', 'A rex'), ('sk', SK, 'bm.pwsk', 'msk', 'A skiff')):
        for n, (iid, nm, col) in D_.items():
            fn(f'{PFX}/w/add_{slot}{n}', [f'execute if score @s {obj} matches 1.. run return run ' + say(f'{what} is on your wheel already - take it back off its Mounts page first.'),
                                          'function bm:p179/w/pid', f'function bm:{PFX}/w/addm_{slot} with storage bm:tmp pw',
                                          'item replace entity @s weapon.offhand with minecraft:air', f'scoreboard players set @s {obj} {n}',
                                          'playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.6 1.6', 'particle minecraft:enchant ~ ~1.2 ~ 0.3 0.4 0.3 0.6 20',
                                          tellraw('@s', PRE + [T(ITEMS[iid]['name'], col, bold=True), T(' goes on your Partner Wheel\'s Mounts page. ', 'gray'),
                                                               T('(Use the wheel, then Mounts, to call it.)', 'dark_gray')])])
        fn(f'{PFX}/w/addm_{slot}', [f'$data modify storage bm:pw p$(pid).{key} set from entity @s equipment.offhand'])
        fn(f'{PFX}/w/outm_{slot}', [f'$execute unless data storage bm:pw p$(pid).{key} run return 0',
                                    'summon minecraft:item ~ ~0.4 ~ {Tags:["bm.pwout"],PickupDelay:0s,Item:{id:"minecraft:paper",count:1}}',
                                    f'$data modify entity @e[type=minecraft:item,tag=bm.pwout,limit=1] Item set from storage bm:pw p$(pid).{key}',
                                    'data modify entity @e[type=minecraft:item,tag=bm.pwout,limit=1] Owner set from entity @s UUID',
                                    'tag @e[type=minecraft:item,tag=bm.pwout] remove bm.pwout', f'$data remove storage bm:pw p$(pid).{key}', 'return 1'])
    # (the rex's row: out -> send home; else call)
    rx_on = ['scoreboard players operation #me bm.rxid = @s bm.rxo', 'scoreboard players set #on bm.rxv 0',
             'execute as @e[type=minecraft:horse,tag=bm.rxh] if score @s bm.rxid = #me bm.rxid run scoreboard players set #on bm.rxv 1']
    sk_on = ['scoreboard players operation #kp bm.pid = @s bm.pid', 'scoreboard players set #on bm.rxv 0',
             'execute as @e[type=minecraft:happy_ghast,tag=bm.skiff] if score @s bm.pid = #kp bm.pid run scoreboard players set #on bm.rxv 1']
    rows = {}
    for slot, D_, obj, on, cc, co in (('rx', MK, 'bm.pwrx', rx_on, C_RX, C_RXOUT), ('sk', SK, 'bm.pwsk', sk_on, C_SK, C_SKOUT)):
        L = list(on)
        for n, (iid, nm, col) in D_.items():
            b_call = P28.btn([icon(iid, col), T(' Call your ', 'white'), T(nm, col, bold=True)], cc, tooltip=T(f'Your {nm} comes to your side', 'gray'), width=200)
            b_home = P28.btn([icon(iid, col), T(f' Send your {nm} home', '#c8c8c8')], cc, tooltip=T(f'Your {nm} goes home', 'gray'), width=200)
            b_out = P28.btn(T('Take it back off the wheel', 'gray'), co, tooltip=T(f'{ITEMS[iid]["name"]} comes off the wheel', 'gray'), width=200)
            L += [f'execute if score @s {obj} matches {n} if score #on bm.rxv matches 0 run data modify storage bm:tmp rxm.acts append value {snbt(b_call)}',
                  f'execute if score @s {obj} matches {n} if score #on bm.rxv matches 1 run data modify storage bm:tmp rxm.acts append value {snbt(b_home)}',
                  f'execute if score @s {obj} matches {n} run data modify storage bm:tmp rxm.acts append value {snbt(b_out)}']
        rows[slot] = L
        fn(f'{PFX}/m/row_{slot}', L)
    b_back = P28.btn([T('« ', 'gray'), T('Partners', getattr(P179, 'PURPLE', '#c08bff'), bold=True)], C_BACK, tooltip=T('Back to the Partner Wheel', 'gray'), width=200)
    head = [T('Partner Wheel', '#c08bff', bold=True), T('  »  ', 'dark_gray'), T('Mounts', '#7ad8ff', bold=True)]
    full = P28.multi(head, [P28.body([T('Your mounts on the wheel: call one or send it home - or take its item back off. Carrying the wheel counts as carrying them.', 'gray')], 300)],
                     '@@ACTS@@', columns=1, button_width=200)
    empty = P28.multi(head, [P28.body([T('No mounts on your wheel yet.', 'white')], 300),
                             P28.body([T('Hold a mount\'s item in your off hand - the ', 'gray'), T('Atomic Whistle', BLUE), T(', the ', 'gray'), T('Mecha Rex Remote', '#8ab4ff'),
                                       T(', a ', 'gray'), T('Vorn Skiff Key', SKIFF_C), T(' or the ', 'gray'), T('Mothership Key', MS_C),
                                       T(' - and use the wheel: it goes on this page. (One rex and one skiff.)', 'gray')], 300)], [b_back], columns=1, button_width=200)
    fn(f'{PFX}/m/show', ['$dialog show @s ' + snbt(full).replace('"@@ACTS@@"', '$(acts)')])
    fn(f'{PFX}/m/open', ['dialog clear @s', f'scoreboard players set @s bm.menu {MENU}', 'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                         'execute unless score @s bm.pwrx matches 1.. unless score @s bm.pwsk matches 1.. run return run dialog show @s ' + snbt(empty),
                         'data modify storage bm:tmp rxm.acts set value []',
                         f'execute if score @s bm.pwrx matches 1.. run function bm:{PFX}/m/row_rx', f'execute if score @s bm.pwsk matches 1.. run function bm:{PFX}/m/row_sk',
                         f'data modify storage bm:tmp rxm.acts append value {snbt(b_back)}',
                         f'function bm:{PFX}/m/show with storage bm:tmp rxm', 'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 0.8 1.2'])
    fn(f'{PFX}/m/any', ['execute if score @s bm.pwrx matches 1.. run return 1', 'execute if score @s bm.pwsk matches 1.. run return 1', 'return 0'])
    # (the wheel's own "Mounts" button: with its partners - or alone, if mounts are all it holds)
    b_mounts = P28.btn([T('◈ ', '#7ad8ff'), T('Mounts', '#7ad8ff', bold=True), T(' »', 'gray')], C_OPEN, tooltip=T('Your rex and your skiff - the mounts on your wheel', 'gray'))
    fn(f'{PFX}/m/wbtn', [f'data modify storage bm:tmp pw.acts append value {snbt(b_mounts)}', 'tag @s add bm.rxmb'])
    op = G.FUNCS['p179/w/open']
    kk = next(j for j, l in enumerate(op) if 'unless data storage bm:tmp pw.acts[0]' in l)
    op[kk:kk] = [f'execute unless data storage bm:tmp pw.acts[0] if function bm:{PFX}/m/any run function bm:{PFX}/m/wbtn']
    ks = next(j for j, l in enumerate(op) if l.startswith('function bm:p179/w/show'))
    op[ks:ks + 1] = [f'execute unless entity @s[tag=bm.rxmb] run function bm:{PFX}/m/wbtn', op[ks], 'tag @s remove bm.rxmb']
    # (the page's buttons: its own block - and the wheel's "Mounts", which the wheel's menu shows)
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {MENU}..{MENU + 19} run return run function bm:{PFX}/act')
    fn(f'{PFX}/act', [f'execute if score #act bm.pay matches {C_OPEN} unless score @s bm.menu matches {WM} run return run function bm:p28/stale',
                      f'execute if score #act bm.pay matches {C_OPEN} run return run function bm:{PFX}/m/open',
                      f'execute unless score @s bm.menu matches {MENU} run return run function bm:p28/stale',
                      f'execute if score #act bm.pay matches {C_RX} run return run function bm:{PFX}/w/rx_call',
                      f'execute if score #act bm.pay matches {C_RXOUT} run return run function bm:{PFX}/w/rx_out',
                      f'execute if score #act bm.pay matches {C_SK} run return run function bm:{PFX}/w/sk_call',
                      f'execute if score #act bm.pay matches {C_SKOUT} run return run function bm:{PFX}/w/sk_out',
                      f'execute if score #act bm.pay matches {C_BACK} run return run function bm:p179/w/open'])
    fn(f'{PFX}/w/rx_call', ['execute unless score @s bm.pwrx matches 1.. run return run function bm:p28/stale'] + rx_on +
       [f'execute if score #on bm.rxv matches 1 run return run function bm:{PFX}/home_cmd',
        'execute if entity @s[predicate=bm:p29/has_vehicle] run return run ' + say('Get down first - the rex comes to you on the ground.'),
        'scoreboard players operation #k bm.rxv = @s bm.pwrx', f'function bm:{PFX}/call'])
    fn(f'{PFX}/w/rx_out', ['execute unless score @s bm.pwrx matches 1.. run return run function bm:p28/stale'] + rx_on +
       [f'execute if score #on bm.rxv matches 1 run function bm:{PFX}/home_cmd', 'function bm:p179/w/pid',
        'scoreboard players set #got bm.rxv 0', f'execute store result score #got bm.rxv run function bm:{PFX}/w/outm_rx with storage bm:tmp pw'] +
       [f'execute if score #got bm.rxv matches 0 if score @s bm.pwrx matches {n} run {give(MK[n][0])}' for n in MK] +
       ['scoreboard players reset @s bm.pwrx', 'playsound minecraft:item.armor.equip_chain player @s ~ ~ ~ 0.6 1.4',
        tellraw('@s', PRE + [T('Your rex\'s call', BLUE, bold=True), T(' comes off your Partner Wheel.', 'gray')])])
    fn(f'{PFX}/w/sk_home', ['execute as @e[type=minecraft:happy_ghast,tag=bm.skiff] if score @s bm.pid = #kp bm.pid run function bm:p249/w/sk_gone',
                            'execute as @e[type=minecraft:item_display,tag=bm.skdisp] if score @s bm.pid = #kp bm.pid run kill @s',
                            title('@s', 'actionbar', T('Your skiff lifts away home.', SKIFF_C))])
    fn(f'{PFX}/w/sk_gone', ['execute on passengers run effect give @s minecraft:slow_falling 10 0 true', 'execute on passengers run ride @s dismount',
                            'execute at @s run function bm:p35/skiff/gone'])
    fn(f'{PFX}/w/sk_call', ['execute unless score @s bm.pwsk matches 1.. run return run function bm:p28/stale'] + sk_on +
       [f'execute if score #on bm.rxv matches 1 run return run function bm:{PFX}/w/sk_home',
        'execute if score @s bm.pwsk matches 1 run return run function bm:p35/skiff/use', 'function bm:p242/ms/use'])
    fn(f'{PFX}/w/sk_out', ['execute unless score @s bm.pwsk matches 1.. run return run function bm:p28/stale'] + sk_on +
       [f'execute if score #on bm.rxv matches 1 run function bm:{PFX}/w/sk_home', 'function bm:p179/w/pid',
        'scoreboard players set #got bm.rxv 0', f'execute store result score #got bm.rxv run function bm:{PFX}/w/outm_sk with storage bm:tmp pw'] +
       [f'execute if score #got bm.rxv matches 0 if score @s bm.pwsk matches {n} run {give(SK[n][0])}' for n in SK] +
       ['scoreboard players reset @s bm.pwsk', 'playsound minecraft:item.armor.equip_chain player @s ~ ~ ~ 0.6 1.4',
        tellraw('@s', PRE + [T('Your skiff\'s key', SKIFF_C, bold=True), T(' comes off your Partner Wheel.', 'gray')])])
    # (the Admiral's module upgrades a skiff kept on the wheel, too: the wheel then holds the Mothership - its key, fresh, when taken back)
    fn(f'{PFX}/w/forget_sk', ['$data remove storage bm:pw p$(pid).msk'])
    ug = G.FUNCS['p242/ms/upgrade']
    ug.insert(0, f'execute if score @s bm.pwsk matches 1 unless items entity @s container.* {holds("skiff_key")} unless items entity @s weapon.offhand {holds("skiff_key")} '
                 f'run return run function bm:{PFX}/w/sk_upgrade')
    fn(f'{PFX}/w/sk_upgrade', [f'clear @s {holds("mothership_module")} 1', 'scoreboard players set @s bm.pwsk 2', 'function bm:p179/w/pid',
                               f'function bm:{PFX}/w/forget_sk with storage bm:tmp pw',
                               'particle minecraft:electric_spark ~ ~1 ~ 0.5 0.8 0.5 0.3 60', 'playsound minecraft:block.beacon.power_select player @a[distance=..16] ~ ~ ~ 1 0.6',
                               'title @s times 6 50 14', title('@s', 'title', T('THE MOTHERSHIP', MS_C, bold=True)),
                               title('@s', 'subtitle', T('your skiff on the wheel, rebuilt round the Admiral\'s command module', '#c8f0c0', italic=True))])

    # ================================================================== ADMIN, UNINSTALL
    fn('admin/rex/kit', [give(i) for i in ('atomic_whistle', 'mecha_remote', *QUEST)])
    fn('admin/rex/atomic', [give('atomic_whistle')])
    fn('admin/rex/mecha', [give('mecha_remote')])
    fn('admin/rex/home', ['execute as @e[type=minecraft:horse,tag=bm.rxh] at @s run function bm:p249/gone'])
    if 'admin/help' in G.FUNCS:
        G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/rex/', 'yellow'), T('kit | atomic | mecha | home', 'yellow'),
                                                    T('  the rex mounts: every item, a summon item, every rex sent home', 'gray')]))
    G.FUNCS['admin/uninstall'][0:0] = ['execute as @e[type=minecraft:horse,tag=bm.rxh] at @s run function bm:p249/gone',
                                       'kill @e[type=minecraft:item_display,tag=bm.rxp]', 'kill @e[type=minecraft:item_display,tag=bm.rxfist]',
                                       'kill @e[type=minecraft:item_display,tag=bm.rxdm]', 'kill @e[type=minecraft:interaction,tag=bm.rxhi]',
                                       'tag @e[type=minecraft:marker,tag=bm.rxhang] remove bm.rxon']
    return len(A.PARTS)



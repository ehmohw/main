"""Phase 2.23: fixes and odds and ends.

- GLOW RANGE: Blood Moon horrors, bioengineered beasts and Jackpot monsters only glow within 30 blocks of a player
  (they used to shine through the whole world).
- VACUUM SATCHEL: sneak + right-click unfolds it into a barrel in front of you (like the Ender Pouch and the Hoard
  Sack); walk away and it folds back up, contents kept. Right-click still switches the auto pick-up ON and OFF.
- MAILBOXES: the model landed at the placer's feet, away from its hitbox - fixed, and old mailboxes are repaired.
- SOUL VIALS: zombies, skeletons and spiders very rarely (about 1 in 700 kills) leave a soul vial. Use it on a
  monster spawner (an empty caged one included) to make it spawn that monster.
- BOUNTY BOARD: a real notice board on the balcony wall beside the Newcomers' lectern, with the bounty pinned on it."""
from items import item, T, TOTEM, DYNAMIC
from useitem import hold, HOLD
from nbt import snbt, B, F, Int

NONMOB = ['player', 'armor_stand', 'mannequin', 'marker', 'interaction', 'item_display', 'block_display', 'text_display', 'item', 'experience_orb',
          'falling_block', 'tnt', 'arrow', 'spectral_arrow', 'trident', 'fireball', 'small_fireball', 'dragon_fireball', 'wither_skull',
          'shulker_bullet', 'llama_spit', 'wind_charge', 'breeze_wind_charge', 'splash_potion', 'lingering_potion', 'egg', 'snowball',
          'ender_pearl', 'eye_of_ender', 'experience_bottle', 'firework_rocket', 'fishing_bobber', 'item_frame', 'glow_item_frame', 'painting',
          'leash_knot', 'lightning_bolt', 'end_crystal', 'evoker_fangs', 'area_effect_cloud', 'ominous_item_spawner', 'minecart', 'chest_minecart',
          'furnace_minecart', 'hopper_minecart', 'tnt_minecart', 'spawner_minecart', 'command_block_minecart'] + \
         [f'{w}_{k}' for w in ('oak', 'spruce', 'birch', 'jungle', 'acacia', 'dark_oak', 'mangrove', 'cherry', 'pale_oak') for k in ('boat', 'chest_boat')] + \
         ['bamboo_raft', 'bamboo_chest_raft']
GLOW_TAGS = ['bm.blood', 'bm.bio', 'bm.jackpot']
VIALS = {'zombie': ('Zombie', '#5a8a3a', 'rotten'), 'skeleton': ('Skeleton', '#d8d8c8', 'bone'), 'spider': ('Spider', '#8a2a2a', 'eye')}
VIAL_CHANCE = 0.0015

for _m, (_n, _c, _) in VIALS.items():
    item(f'soul_vial_{_m}', TOTEM, f'{_n} Soul Vial', _c,
         [f'A {_n.lower()}\'s soul, corked in glass.', ('Right-click a monster spawner: it will', 'blue'), (f'spawn {_n.lower()}s from now on.', 'blue'),
          ('Works on a Caged Spawner you\'ve set down.', 'gray'), ('Very, very rare.', 'dark_purple')],
         model=f'bm:soul_vial_{_m}', stack=16, cat='relic', glint=True, comps=hold('none'))
    HOLD[f'soul_vial_{_m}'] = f'bm:p44/vial/{_m}'


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    holds = '*[minecraft:custom_data~{bm:"%s"}]'
    fast, second, tick = [], [], []
    wjson('bm/tags/entity_type/p44_nonmob.json', {'values': [{'id': f'minecraft:{e}', 'required': False} for e in NONMOB]})

    # ------------------------------------------------------------------ glow only within 30 blocks
    second += [f'execute as @e[tag={t},tag=!bm.g30,type=!minecraft:player] run function bm:p44/g30' for t in GLOW_TAGS]
    fn('p44/g30', ['tag @s add bm.g30', 'data merge entity @s {Glowing:0b}', 'effect clear @s minecraft:glowing'])
    second.append('execute as @a[gamemode=!spectator] at @s run effect give @e[tag=bm.g30,distance=..30] minecraft:glowing 2 0 true')

    # ------------------------------------------------------------------ the Vacuum Satchel unfolds into a barrel
    # its contents live in storage bm:vac v<player id> (in the satchel's own container format, so the pick-up code is unchanged)
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.vact dummy']
    G.OBJECTIVES.append('bm.vact')
    hand = ['scoreboard players set #hand bm.rng 0',
            f'execute if items entity @s weapon.mainhand {holds % "vacuum_satchel"} run scoreboard players set #hand bm.rng 1',
            f'execute if score #hand bm.rng matches 0 if items entity @s weapon.offhand {holds % "vacuum_satchel"} run scoreboard players set #hand bm.rng 2',
            'execute if score #hand bm.rng matches 0 run return 0']
    fn('p33/vac/use', hand + [
        'execute if predicate bm:p20/sneaking if score #hand bm.rng matches 1 run return run function bm:p44/vac/open {path:"SelectedItem",slot:"weapon.mainhand"}',
        'execute if predicate bm:p20/sneaking if score #hand bm.rng matches 2 run return run function bm:p44/vac/open {path:"equipment.offhand",slot:"weapon.offhand"}',
        'execute if score #hand bm.rng matches 1 if items entity @s weapon.mainhand *[minecraft:custom_data~{bm_vac:1b}] run return run function bm:p33/vac/off {slot:"weapon.mainhand"}',
        'execute if score #hand bm.rng matches 2 if items entity @s weapon.offhand *[minecraft:custom_data~{bm_vac:1b}] run return run function bm:p33/vac/off {slot:"weapon.offhand"}',
        'execute if score #hand bm.rng matches 1 run return run function bm:p33/vac/on {slot:"weapon.mainhand"}',
        'function bm:p33/vac/on {slot:"weapon.offhand"}'])
    fn('p44/vac/open', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #kp bm.pid = @s bm.pid',
                        'data modify storage bm:tmp vs set value {}', 'execute store result storage bm:tmp vs.pid int 1 run scoreboard players get @s bm.pid',
                        '$data modify storage bm:tmp vs.path set value "$(path)"', '$data modify storage bm:tmp vs.slot set value "$(slot)"',
                        'function bm:p44/vac/migrate with storage bm:tmp vs',
                        'scoreboard players set #had bm.rng 0',
                        'execute as @e[type=minecraft:marker,tag=bm.vacm] if score @s bm.pid = #kp bm.pid at @s run function bm:p44/vac/close_mine',
                        'execute if score #had bm.rng matches 1 run return 0',
                        'execute unless function bm:p37/allowed run return run ' + say('The satchel won\'t unfold here.'),
                        'scoreboard players set #ok bm.rng 0',
                        'execute rotated ~ 0 positioned ^ ^ ^1.6 align xyz positioned ~0.5 ~ ~0.5 run function bm:p44/vac/try with storage bm:tmp vs',
                        'execute if score #ok bm.rng matches 0 rotated ~ 0 positioned ^ ^ ^2.6 align xyz positioned ~0.5 ~ ~0.5 run function bm:p44/vac/try with storage bm:tmp vs',
                        'execute if score #ok bm.rng matches 0 run ' + say('No room on the ground in front of you.')])
    # a satchel from before 2.23 still carries its items: they move into storage (or, if storage already holds a satchel's worth, spill out)
    fn('p44/vac/migrate', ['$execute unless data entity @s $(path).components."minecraft:container"[0] run return 0',
                           '$execute if data storage bm:vac v$(pid)[0] run function bm:p44/vac/spill with storage bm:tmp vs',
                           '$execute unless data storage bm:vac v$(pid)[0] run data modify storage bm:vac v$(pid) set from entity @s $(path).components."minecraft:container"',
                           '$item modify entity @s $(slot) {function:"minecraft:set_components",components:{"minecraft:container":[]}}'])
    fn('p44/vac/spill', ['$data modify storage bm:tmp vs.src set from entity @s $(path).components."minecraft:container"', 'function bm:p44/vac/spill1'])
    fn('p44/vac/spill1', ['execute unless data storage bm:tmp vs.src[0] run return 0',
                          'summon minecraft:item ~ ~0.5 ~ {Tags:["bm.vspill"],Item:{id:"minecraft:stone",count:1},PickupDelay:10s}',
                          'data modify entity @e[type=minecraft:item,tag=bm.vspill,limit=1] Item set from storage bm:tmp vs.src[0].item',
                          'tag @e[type=minecraft:item,tag=bm.vspill] remove bm.vspill', 'data remove storage bm:tmp vs.src[0]', 'function bm:p44/vac/spill1'])
    fn('p44/vac/close_mine', ['scoreboard players set #had bm.rng 1', 'function bm:p44/vac/close'])
    fn('p44/vac/try', ['execute unless block ~ ~ ~ #bm:p41_open run return 0', 'execute if block ~ ~-1 ~ #minecraft:replaceable run return 0',
                       'setblock ~ ~ ~ minecraft:barrel[facing=up]{CustomName:{text:"Vacuum Satchel",color:"#c8a050"}}',
                       '$data modify storage bm:tmp vs.src set from storage bm:vac v$(pid)', '$data remove storage bm:vac v$(pid)',
                       'execute unless data storage bm:tmp vs.src run data modify storage bm:tmp vs.src set value []',
                       'data modify storage bm:tmp vs.out set value []', 'function bm:p44/vac/c2i', 'data modify block ~ ~ ~ Items set from storage bm:tmp vs.out',
                       'summon minecraft:marker ~ ~ ~ {Tags:["bm.vacm","bm.vnew"]}',
                       'scoreboard players operation @e[type=minecraft:marker,tag=bm.vnew,distance=..0.5] bm.pid = #kp bm.pid',
                       'scoreboard players set @e[type=minecraft:marker,tag=bm.vnew,distance=..0.5] bm.vact 180',
                       'tag @e[type=minecraft:marker,tag=bm.vnew] remove bm.vnew', 'scoreboard players set #ok bm.rng 1',
                       'particle minecraft:wax_on ~ ~0.6 ~ 0.3 0.3 0.3 0.02 12', 'playsound minecraft:block.barrel.open block @a[distance=..16] ~ ~ ~ 1 1.1'])
    # container entries {slot, item:{...}} <-> barrel Items {Slot, id, count, components}
    fn('p44/vac/c2i', ['execute unless data storage bm:tmp vs.src[0] run return 0',
                       'data modify storage bm:tmp vs.e set from storage bm:tmp vs.src[0].item',
                       'execute store result storage bm:tmp vs.e.Slot byte 1 run data get storage bm:tmp vs.src[0].slot',
                       'data modify storage bm:tmp vs.out append from storage bm:tmp vs.e', 'data remove storage bm:tmp vs.src[0]', 'function bm:p44/vac/c2i'])
    fn('p44/vac/i2c', ['execute unless data storage bm:tmp vs.src[0] run return 0',
                       'data modify storage bm:tmp vs.e set value {slot:0}',
                       'execute store result storage bm:tmp vs.e.slot int 1 run data get storage bm:tmp vs.src[0].Slot',
                       'data modify storage bm:tmp vs.e.item set from storage bm:tmp vs.src[0]', 'data remove storage bm:tmp vs.e.item.Slot',
                       'data modify storage bm:tmp vs.out append from storage bm:tmp vs.e', 'data remove storage bm:tmp vs.src[0]', 'function bm:p44/vac/i2c'])
    second.append('execute as @e[type=minecraft:marker,tag=bm.vacm] at @s run function bm:p44/vac/check')
    fn('p44/vac/check', ['scoreboard players remove @s bm.vact 1', 'scoreboard players operation #kp bm.pid = @s bm.pid', 'scoreboard players set #near bm.rng 0',
                         'execute as @a[distance=..6] if score @s bm.pid = #kp bm.pid run scoreboard players set #near bm.rng 1',
                         'execute unless block ~ ~ ~ minecraft:barrel run return run kill @s',
                         'execute if score #near bm.rng matches 0 run return run function bm:p44/vac/close',
                         'execute if score @s bm.vact matches ..0 run function bm:p44/vac/close'])
    fn('p44/vac/close', ['data modify storage bm:tmp vs set value {}', 'execute store result storage bm:tmp vs.pid int 1 run scoreboard players get @s bm.pid',
                         'function bm:p44/vac/close_m with storage bm:tmp vs'])
    fn('p44/vac/close_m', ['execute unless block ~ ~ ~ minecraft:barrel run return run kill @s',
                           'data modify storage bm:tmp vs.src set from block ~ ~ ~ Items', 'data modify storage bm:tmp vs.out set value []', 'function bm:p44/vac/i2c',
                           '$data modify storage bm:vac v$(pid) set from storage bm:tmp vs.out', 'data remove block ~ ~ ~ Items', 'setblock ~ ~ ~ minecraft:air',
                           'particle minecraft:wax_off ~ ~0.6 ~ 0.3 0.3 0.3 0.02 12', 'playsound minecraft:block.barrel.close block @a[distance=..16] ~ ~ ~ 1 1.1', 'kill @s'])
    # the auto pick-up now fills storage (and waits while the barrel is out)
    fn('p33/vac/pull', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #kp bm.pid = @s bm.pid',
                        'scoreboard players set #vopen bm.rng 0',
                        'execute as @e[type=minecraft:marker,tag=bm.vacm] if score @s bm.pid = #kp bm.pid run scoreboard players set #vopen bm.rng 1',
                        'execute if score #vopen bm.rng matches 1 run return 0',
                        'execute store result storage bm:tmp vac.pid int 1 run scoreboard players get @s bm.pid',
                        'function bm:p33/vac/read with storage bm:tmp vac', 'scoreboard players set #vtak bm.rng 0', 'tag @s add bm.vacuser',
                        'execute as @e[type=minecraft:item,distance=..6,nbt={PickupDelay:0s},limit=4,sort=nearest] unless items entity @s contents *[minecraft:custom_data~{bm:"vacuum_satchel"}] at @s run function bm:p33/vac/take',
                        'tag @s remove bm.vacuser',
                        'execute if score #vtak bm.rng matches 1.. run function bm:p33/vac/write with storage bm:tmp vac'])
    fn('p33/vac/read', ['data remove storage bm:tmp vac.c', '$data modify storage bm:tmp vac.c set from storage bm:vac v$(pid)',
                        'execute unless data storage bm:tmp vac.c run data modify storage bm:tmp vac.c set value []'])
    fn('p33/vac/write', ['$data modify storage bm:vac v$(pid) set from storage bm:tmp vac.c', 'playsound minecraft:entity.item.pickup player @s ~ ~ ~ 0.4 0.6'])

    # ------------------------------------------------------------------ mailboxes placed before 2.23: put the model back on its hitbox
    ident = [F(0), F(0), F(0), F(1)]
    mdisp = {'Tags': ['bm.mbdisp'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:mailbox3d'}},
             'item_display': 'fixed', 'brightness': {'block': Int(13), 'sky': Int(13)},
             'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.5), F(0)], 'scale': [F(1.0)] * 3}}
    second += ['kill @e[type=minecraft:item_display,tag=bm.mbdisp,tag=bm.mbnew]',
               f'execute as @e[type=minecraft:interaction,tag=bm.mbox] at @s unless entity @e[type=minecraft:item_display,tag=bm.mbdisp,distance=..0.8] run summon minecraft:item_display ~ ~ ~ {snbt(mdisp)}']

    # ------------------------------------------------------------------ soul vials
    for m, (nm, col, _) in VIALS.items():
        wjson(f'bm/advancement/p44/vial_{m}.json', {'criteria': {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [
            {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:entity_type': f'minecraft:{m}'}},
            {'condition': 'minecraft:random_chance', 'chance': VIAL_CHANCE}]}}}, 'rewards': {'function': f'bm:p44/vial/got_{m}'}})
        fn(f'p44/vial/got_{m}', [f'advancement revoke @s only bm:p44/vial_{m}', give(f'soul_vial_{m}'),
                                 'playsound minecraft:particle.soul_escape player @s ~ ~ ~ 1 0.8', 'particle minecraft:soul ~ ~1 ~ 0.3 0.5 0.3 0.02 12',
                                 tellraw('@s', PREFIX + [T('A soul lingers... and you catch it: ', 'gray'), T(f'{nm} Soul Vial', col, bold=True), T('!', 'gray')])])
        fn(f'p44/vial/{m}', ['scoreboard players set #ray bm.rng 25', 'scoreboard players set #got bm.rng 0',
                             f'execute anchored eyes positioned ^ ^ ^ run function bm:p44/vial/ray_{m}',
                             'execute if score #got bm.rng matches 0 run return run ' + say('Look at a monster spawner (within 5 blocks).'),
                             f'execute unless entity @s[gamemode=creative] run clear @s {holds % f"soul_vial_{m}"} 1',
                             title('@s', 'actionbar', [T('The spawner drinks the soul: ', 'gray'), T(f'{nm.lower()}s', col), T(' from now on.', 'gray')])])
        fn(f'p44/vial/ray_{m}', [f'execute if block ~ ~ ~ minecraft:spawner run return run function bm:p44/vial/set_{m}',
                                 'execute unless block ~ ~ ~ #bm:grap_pass run return 0', 'scoreboard players remove #ray bm.rng 1',
                                 f'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p44/vial/ray_{m}'])
        fn(f'p44/vial/set_{m}', [f'data merge block ~ ~ ~ {{SpawnData:{{entity:{{id:"minecraft:{m}"}}}},SpawnPotentials:[],Delay:40s}}', 'scoreboard players set #got bm.rng 1',
                                 'execute align xyz positioned ~0.5 ~0.5 ~0.5 run particle minecraft:soul ~ ~ ~ 0.4 0.4 0.4 0.03 20',
                                 'playsound minecraft:block.sculk_catalyst.bloom block @a[distance=..16] ~ ~ ~ 1 0.7'])

    # ------------------------------------------------------------------ the bounty board: a real board on the wall
    import mgeo
    from phase40 import BOARD
    bx, by, bz = BOARD
    panel = lambda tags, block, scale: {'Tags': tags, 'block_state': f'minecraft:{block}', 'brightness': {'block': Int(13), 'sky': Int(13)},
                                        'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0), F(0)], 'scale': [F(v) for v in scale]}}
    # template frame: the wall is at z = 82 (the board's back), the balcony in front of it (smaller z); yaw 0 = template axes
    parts = [((bx - 0.75, by + 0.45, bz + 0.33), 'dark_oak_planks', (1.5, 1.45, 0.12)),          # the board
             ((bx - 0.85, by + 0.35, bz + 0.31), 'stripped_dark_oak_log', (1.7, 0.1, 0.16)),     # frame, bottom
             ((bx - 0.85, by + 1.9, bz + 0.31), 'stripped_dark_oak_log', (1.7, 0.1, 0.16)),      # frame, top
             ((bx - 0.62, by + 1.55, bz + 0.31), 'red_wool', (0.08, 0.08, 0.02)),                 # pins
             ((bx + 0.54, by + 1.55, bz + 0.31), 'red_wool', (0.08, 0.08, 0.02))]
    patch = G.FUNCS['p35/patch']
    for i, (p, block, scale) in enumerate(parts):
        tag = f'bm.bbp{i}'
        patch += [f'execute positioned {mgeo.rel(p)} unless entity @e[type=minecraft:block_display,tag={tag},distance=..0.6] run summon minecraft:block_display ~ ~ ~ {snbt(panel(["bm.bbpanel", tag, "bm.npc", "bm.bbnew"], block, scale))}']
    patch += ['execute as @e[type=minecraft:block_display,tag=bm.bbnew] positioned as @s run tp @s ~ ~ ~ ~ 0', 'tag @e[tag=bm.bbnew] remove bm.bbnew',
              # the old floating notice (2.19-2.22) sat higher up; the new one is pinned to the board
              f'execute positioned {mgeo.rel((bx, by + 1.7, bz + 0.2))} run kill @e[type=minecraft:text_display,tag=bm.bboard,distance=..0.3]']

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


def rp(R):
    grid = R.grid
    for m, (_n, col, mark) in VIALS.items():
        R.ICONS[f'soul_vial_{m}'] = grid(['................', '......KKKK......', '......KbbK......', '.......KK.......', '......KggK......', '.....KgSSgK.....',
                                          '....KgSSSSgK....', '....KSSmSSSK....', '....KSmmmSSK....', '....KSSmSSSK....', '....KgSSSSgK....', '.....KggggK.....',
                                          '......KKKK......', '................', '................', '................'],
                                         dict(K='#2a2a3a', b='#8a6a40', g='#c8e8ff', S='#5ad8e8', m=col))

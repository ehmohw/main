"""Phase 1.6: the hidden Blood Moon Monstrosity (ravager boss + Crimson Herald rider), the Ravenous Heart,
and mounted mobs (champion cavalry, spider jockeys, blood horsemen).
Importing registers the new item; generate(G) writes the logic after phase15.generate."""
from items import item, T
from nbt import snbt, B, F, D, Int

item('ravenous_heart', 'minecraft:heart_of_the_sea', 'Ravenous Heart', 'dark_red',
     ['Torn from the Blood Moon Monstrosity.', 'It is still hungry. So are you... sometimes.',
      ('While anywhere in your inventory:', 'gray'), ('every kill refills your hunger.', 'blue')],
     model='bm:ravenous_heart', glint=True, stack=1, bold=True, cat='blood')

HP = 500                       # Monstrosity health
GROUND = ['zombie', 'husk', 'skeleton', 'stray', 'bogged', 'spider', 'creeper', 'pillager', 'vindicator',
          'zombie_villager', 'witch', 'enderman']          # mobs whose spawn spot can host the boss
NO_DROP = {k: F(0.0) for k in ['head', 'chest', 'legs', 'feet', 'mainhand', 'offhand', 'body', 'saddle']}
FIRE_RES = [{'id': 'minecraft:fire_resistance', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0)}]


def generate(G):
    fn, wjson, title, tellraw, loot_entry, uni, KILLED = G.fn, G.wjson, G.title, G.tellraw, G.loot_entry, G.uni, G.KILLED

    # ================================================================ MONSTROSITY
    boss = {'Tags': ['bm.seen', 'bm.monstrosity', 'bm.tiered', 'bm.blood', 'bm.m_new'],
            'CustomName': T('Blood Moon Monstrosity', 'dark_red', bold=True), 'Glowing': B(1), 'PersistenceRequired': B(1),
            'DeathLootTable': 'bm:entities/monstrosity', 'Health': F(HP),
            'attributes': [{'id': 'minecraft:max_health', 'base': D(HP)}, {'id': 'minecraft:attack_damage', 'base': D(18)},
                           {'id': 'minecraft:armor', 'base': D(12)}, {'id': 'minecraft:armor_toughness', 'base': D(6)},
                           {'id': 'minecraft:knockback_resistance', 'base': D(1)}, {'id': 'minecraft:follow_range', 'base': D(64)},
                           {'id': 'minecraft:attack_knockback', 'base': D(2.5)}, {'id': 'minecraft:movement_speed', 'base': D(0.33)},
                           {'id': 'minecraft:scale', 'base': D(1.45)}, {'id': 'minecraft:step_height', 'base': D(1.5)}],
            'active_effects': FIRE_RES,
            # a bone carries the bite enchantment; it adds no attack-damage modifiers and ravagers don't render held items
            'equipment': {'mainhand': {'id': 'minecraft:bone', 'count': Int(1),
                                       'components': {'minecraft:enchantments': {'bm:monstrous_maw': Int(1)}}}},
            'drop_chances': NO_DROP}
    herald = {'Tags': ['bm.seen', 'bm.herald', 'bm.tiered', 'bm.blood', 'bm.h_new'],
              'CustomName': T('The Crimson Herald', 'dark_red', bold=True), 'Glowing': B(1), 'PersistenceRequired': B(1),
              'DeathLootTable': 'bm:entities/herald', 'Health': F(60),
              'attributes': [{'id': 'minecraft:max_health', 'base': D(60)}, {'id': 'minecraft:follow_range', 'base': D(64)}],
              'active_effects': FIRE_RES,
              'equipment': {'mainhand': {'id': 'minecraft:crossbow', 'count': Int(1), 'components': {
                  'minecraft:enchantments': {'minecraft:quick_charge': Int(2), 'bm:blood_curse': Int(1)}}},
                  'head': {'id': 'minecraft:netherite_helmet', 'count': Int(1), 'components': {
                      'minecraft:trim': {'material': 'minecraft:redstone', 'pattern': 'minecraft:rib'}}}},
              'drop_chances': NO_DROP}
    fn('monst/summon', [
        f'summon minecraft:ravager ~ ~ ~ {snbt(boss)}',
        f'summon minecraft:pillager ~ ~ ~ {snbt(herald)}',
        'ride @e[type=minecraft:pillager,tag=bm.h_new,limit=1] mount @e[type=minecraft:ravager,tag=bm.m_new,limit=1]',
        'team join bm.blood @e[tag=bm.m_new]', 'team join bm.blood @e[tag=bm.h_new]',
        'tag @e[tag=bm.m_new] remove bm.m_new', 'tag @e[tag=bm.h_new] remove bm.h_new',
        'particle minecraft:dust{color:[0.6,0.0,0.0],scale:3.0} ~ ~1.5 ~ 1.5 1.5 1.5 0 60'])
    # replaces the hostile mob whose spawn rolled it
    fn('monst/spawn', ['function bm:monst/summon', 'tp @s ~ -400 ~'])
    roll = ('execute if score #m bm.rng matches 1 unless entity @e[type=minecraft:ravager,tag=bm.monstrosity] '
            'if predicate bm:sees_sky unless block ~ ~-1 ~ #minecraft:air unless block ~ ~ ~ minecraft:water '
            + ' '.join(f'if block {p} #minecraft:air' for p in ['~ ~3 ~', '~2 ~3 ~', '~-2 ~3 ~', '~ ~3 ~2', '~ ~3 ~-2'])
            + ' run return run function bm:monst/spawn')
    for t in GROUND:
        G.FUNCS[f'mobs/blood_roll/{t}'][0:0] = ['execute store result score #m bm.rng run random value 1..1000', roll]

    near = 'gamemode=!creative,gamemode=!spectator'
    fn('monst/tick', [
        'execute unless score #active bm.bm matches 1 run return run function bm:monst/retreat',
        f'execute if entity @s[tag=!bm.m_intro] if entity @a[distance=..40,gamemode=!spectator] run function bm:monst/intro',
        'execute unless entity @s[tag=bm.m_intro] run return 0',
        'bossbar set bm:monst visible true', 'bossbar set bm:monst players @a[distance=..64]',
        'execute store result bossbar bm:monst value run data get entity @s Health',
        'execute store result score #mh bm.rng run data get entity @s Health',
        f'execute if score #mh bm.rng matches ..{HP // 2} unless entity @s[tag=bm.m_rage] run return run function bm:monst/enrage',
        'scoreboard players add @s bm.mt 1',
        'execute if score @s bm.mt matches 12.. run function bm:monst/roar'])
    # first sight: local only (players within 48 blocks)
    fn('monst/intro', [
        'tag @s add bm.m_intro', 'scoreboard players set @s bm.mt 0', 'scoreboard players set @s bm.mr 0',
        'title @a[distance=..48] times 10 60 20',
        title('@a[distance=..48]', 'subtitle', T('It has your scent.', 'red', italic=True)),
        title('@a[distance=..48]', 'title', T('Blood Moon Monstrosity', 'dark_red', bold=True)),
        'playsound minecraft:entity.ravager.roar hostile @a[distance=..48] ~ ~ ~ 3 0.5'])
    fn('monst/roar', [
        'scoreboard players set @s bm.mt 0',
        f'execute unless entity @a[distance=..24,{near}] run return 0',
        'playsound minecraft:entity.ravager.roar hostile @a[distance=..40] ~ ~ ~ 2.5 0.6',
        'particle minecraft:dust{color:[0.6,0.0,0.0],scale:3.0} ~ ~1.5 ~ 3 1 3 0 80',
        f'effect give @a[distance=..8,{near}] minecraft:slowness 3 1',
        f'execute as @a[distance=..6,{near}] run damage @s 4 minecraft:mob_attack by @e[type=minecraft:ravager,tag=bm.monstrosity,sort=nearest,limit=1]',
        'scoreboard players add @s bm.mr 1',
        'execute if score @s bm.mr matches 2.. run function bm:monst/minions'])
    fn('monst/minions', [
        'scoreboard players set @s bm.mr 0',
        'execute store result score #mc bm.rng if entity @e[tag=bm.m_minion,distance=..32]',
        'execute if score #mc bm.rng matches 3.. run return 0',
        'summon minecraft:zombie ~2 ~ ~ {Tags:["bm.seen","bm.m_minion","bm.new_mm"]}',
        'summon minecraft:zombie ~-2 ~ ~ {Tags:["bm.seen","bm.m_minion","bm.new_mm"]}',
        'execute as @e[tag=bm.new_mm] at @s run function bm:mobs/blood/zombie',
        # no crystals from the boss's spawn - otherwise it's a crystal farm
        'execute as @e[tag=bm.new_mm] run data merge entity @s {DeathLootTable:"minecraft:entities/zombie"}',
        'tag @e[tag=bm.new_mm] remove bm.new_mm',
        'particle minecraft:soul ~ ~0.5 ~ 2 0.3 2 0.02 30'])
    fn('monst/enrage', [
        'tag @s add bm.m_rage', 'scoreboard players set @s bm.mt 0',
        'effect give @s minecraft:strength infinite 1 true',
        'attribute @s minecraft:movement_speed modifier add bm:rage 0.2 add_multiplied_base',
        title('@a[distance=..40]', 'actionbar', T('The Monstrosity is ENRAGED!', 'dark_red', bold=True)),
        'playsound minecraft:entity.ravager.stunned hostile @a[distance=..40] ~ ~ ~ 2 0.5',
        'particle minecraft:angry_villager ~ ~3 ~ 1.5 0.8 1.5 0 20'])
    fn('monst/retreat', [
        title('@a[distance=..48]', 'actionbar', T('The Monstrosity flees from the dawn...', 'gold', italic=True)),
        'playsound minecraft:entity.ravager.ambient hostile @a[distance=..48] ~ ~ ~ 2 0.5',
        'particle minecraft:large_smoke ~ ~1.5 ~ 1.5 1.5 1.5 0.02 60',
        'tp @e[type=minecraft:pillager,tag=bm.herald,distance=..8] ~ -400 ~', 'tp @s ~ -400 ~'])
    # kill credit -> local announcement; the victory jingle waits a second so it doesn't land on the death roar
    wjson('bm/advancement/monst/slain.json', {
        'criteria': {'slain': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [
            {'condition': 'minecraft:entity_properties', 'entity': 'this',
             'predicate': {'minecraft:nbt': '{Tags:["bm.monstrosity"]}'}}]}}},
        'rewards': {'function': 'bm:monst/slain'}})
    fn('monst/slain', [
        'advancement revoke @s only bm:monst/slain',
        'scoreboard players set @a[distance=..48] bm.mvic 20'])
    fn('monst/victory', [
        'scoreboard players reset @s bm.mvic',
        'title @s times 10 70 20',
        title('@s', 'subtitle', T('Its heart is yours. Keep it close.', 'gray', italic=True)),
        title('@s', 'title', T('MONSTROSITY SLAIN', 'gold', bold=True)),
        'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1'])
    wjson('bm/enchantment/monstrous_maw.json', {
        'anvil_cost': 8, 'description': T('Monstrous Maw', 'dark_red'), 'max_level': 1, 'weight': 1,
        'min_cost': {'base': 1, 'per_level_above_first': 0}, 'max_cost': {'base': 1, 'per_level_above_first': 0},
        'slots': ['mainhand'], 'supported_items': '#minecraft:enchantable/weapon',
        'effects': {'minecraft:post_attack': [{
            'affected': 'victim', 'enchanted': 'attacker',
            'effect': {'type': 'minecraft:all_of', 'effects': [
                {'type': 'minecraft:damage_entity', 'damage_type': 'bm:blood_drain', 'min_damage': 5.0, 'max_damage': 5.0},
                {'type': 'minecraft:apply_mob_effect', 'to_apply': 'minecraft:wither', 'min_duration': 5.0, 'max_duration': 5.0,
                 'min_amplifier': 1.0, 'max_amplifier': 1.0},
                {'type': 'minecraft:apply_mob_effect', 'to_apply': 'minecraft:hunger', 'min_duration': 8.0, 'max_duration': 8.0,
                 'min_amplifier': 2.0, 'max_amplifier': 2.0}]},
            'requirements': {'condition': 'minecraft:entity_properties', 'entity': 'this',
                             'predicate': {'minecraft:entity_type': 'minecraft:player'}}}]}})
    wjson('bm/loot_table/entities/monstrosity.json', {'type': 'minecraft:entity', 'pools': [
        {'rolls': 1, 'entries': [{'type': 'minecraft:loot_table', 'value': 'minecraft:entities/ravager'}]},
        {'rolls': 1, 'entries': [loot_entry('ravenous_heart')]},
        {'rolls': 1, 'entries': [loot_entry('blood_crystal', uni(10, 16))]},
        {'rolls': 1, 'entries': [loot_entry('trophy')], 'conditions': [KILLED]},
        {'rolls': 1, 'entries': [loot_entry('medallion', uni(2, 4))], 'conditions': [KILLED]},
        # 1.7: the legendary Blood Eclipse charm (10% per kill)
        {'rolls': 1, 'entries': [loot_entry('charm_eclipse')], 'conditions': [KILLED, G.chance(0.1)]}]})
    wjson('bm/loot_table/entities/herald.json', {'type': 'minecraft:entity', 'pools': [
        {'rolls': 1, 'entries': [{'type': 'minecraft:loot_table', 'value': 'minecraft:entities/pillager'}]},
        {'rolls': 1, 'entries': [loot_entry('blood_crystal', uni(2, 3))]}]})

    # ---------------- Ravenous Heart: any kill refills hunger while it's carried
    fn('monst/has_heart', [
        'execute if items entity @s container.* *[minecraft:custom_data~{bm:"ravenous_heart"}] run return 1',
        'execute if items entity @s weapon.offhand *[minecraft:custom_data~{bm:"ravenous_heart"}] run return 1',
        'return fail'])
    fn('monst/feed', [
        'execute store result score @s bm.food run data get entity @s foodLevel',
        'execute if score @s bm.food matches 20.. run return 0',
        'effect give @s minecraft:saturation 1 0 true',
        'playsound minecraft:entity.generic.eat player @s ~ ~ ~ 0.6 0.8',
        'particle minecraft:dust{color:[0.6,0.0,0.05],scale:1.0} ~ ~1 ~ 0.3 0.4 0.3 0 8'])

    # ================================================================ MOUNTED MOBS
    def mount_fn(name, vehicle, pct, checks, nbt, blood=False):
        tags = ['bm.seen', 'bm.mount', 'bm.newmount'] + (['bm.blood'] if blood else [])
        body = {'Tags': tags, **nbt}
        if blood:
            body['Glowing'] = B(1)
        lines = ['execute if entity @s[tag=bm.m_minion] run return 0',
                 'execute store result score #r bm.rng run random value 1..100',
                 f'execute if score #r bm.rng matches {pct + 1}.. run return 0']
        lines += [f'execute {c} run return 0' for c in checks]
        lines += [f'summon minecraft:{vehicle} ~ ~ ~ {snbt(body)}',
                  f'ride @s mount @e[type=minecraft:{vehicle},tag=bm.newmount,sort=nearest,limit=1]']
        if blood:
            lines.append('team join bm.blood @e[tag=bm.newmount]')
        lines.append('tag @e[tag=bm.newmount] remove bm.newmount')
        fn(f'mounts/{name}', lines)

    sky = ['unless predicate bm:sees_sky', 'unless block ~ ~2 ~ #minecraft:air', 'unless block ~ ~3 ~ #minecraft:air']
    tall = sky + ['unless block ~ ~4 ~ #minecraft:air']
    wet = ['unless block ~ ~ ~ minecraft:water', 'unless block ~ ~1 ~ minecraft:water']
    saddle = {'saddle': {'id': 'minecraft:saddle', 'count': Int(1)}}
    # tamed + saddled: kill the rider and the mount is yours
    steed = lambda hp: {'Tame': B(1), 'equipment': saddle, 'Health': F(hp),
                        'attributes': [{'id': 'minecraft:max_health', 'base': D(hp)}]}
    mount_fn('zombie_horse', 'zombie_horse', 35, sky, steed(40))
    mount_fn('skeleton_horse', 'skeleton_horse', 35, sky, steed(40))
    mount_fn('camel_husk', 'camel_husk', 35, tall, steed(50))
    mount_fn('zombie_nautilus', 'zombie_nautilus', 35, wet,
             {'equipment': saddle, 'Health': F(40), 'attributes': [{'id': 'minecraft:max_health', 'base': D(40)}]})
    blood_steed = dict(steed(60), CustomName=T('Blood Moon Steed', 'dark_red'),
                       attributes=[{'id': 'minecraft:max_health', 'base': D(60)},
                                   {'id': 'minecraft:movement_speed', 'base': D(0.28)}])
    mount_fn('blood_skeleton_horse', 'skeleton_horse', 40, sky, blood_steed, blood=True)
    mount_fn('blood_zombie_horse', 'zombie_horse', 30, sky, blood_steed, blood=True)
    fn('mounts/spider_jockey', [
        'execute store result score #r bm.rng run random value 1..100',
        'execute if score #r bm.rng matches 41.. run return 0',
        'execute unless block ~ ~1 ~ #minecraft:air run return 0', 'execute unless block ~ ~2 ~ #minecraft:air run return 0',
        'summon minecraft:skeleton ~ ~ ~ {Tags:["bm.seen","bm.newmount"]}',
        'execute as @e[type=minecraft:skeleton,tag=bm.newmount,sort=nearest,limit=1] run function bm:mobs/elite/skeleton',
        'ride @e[type=minecraft:skeleton,tag=bm.newmount,sort=nearest,limit=1] mount @s',
        'tag @e[tag=bm.newmount] remove bm.newmount'])
    for t, m in [('zombie', 'zombie_horse'), ('zombie_villager', 'zombie_horse'), ('skeleton', 'skeleton_horse'),
                 ('stray', 'skeleton_horse'), ('husk', 'camel_husk'), ('drowned', 'zombie_nautilus'), ('spider', 'spider_jockey')]:
        G.FUNCS[f'mobs/champion/{t}'].append(f'function bm:mounts/{m}')
    for t, m in [('skeleton', 'blood_skeleton_horse'), ('stray', 'blood_skeleton_horse'), ('zombie', 'blood_zombie_horse')]:
        G.FUNCS[f'mobs/blood/{t}'].append(f'function bm:mounts/{m}')
    # once a player has ridden a mount it's theirs: it stops glowing and is never cleaned up
    fn('mounts/claim_blood', ['data merge entity @s {Glowing:0b}', 'tag @s remove bm.blood', 'team leave @s'])

    # ================================================================ wiring
    G.FUNCS['load'][-1:-1] = [
        'scoreboard objectives add bm.kill minecraft.custom:minecraft.mob_kills', 'scoreboard objectives add bm.food dummy',
        'scoreboard objectives add bm.mt dummy', 'scoreboard objectives add bm.mr dummy', 'scoreboard objectives add bm.mvic dummy',
        'bossbar add bm:monst {text:"Blood Moon Monstrosity",color:"dark_red",bold:true}',
        'bossbar set bm:monst color red', 'bossbar set bm:monst style notched_10', f'bossbar set bm:monst max {HP}',
        'bossbar set bm:monst visible false']
    G.OBJECTIVES += ['bm.kill', 'bm.food', 'bm.mt', 'bm.mr', 'bm.mvic']
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = ['execute as @a[scores={bm.kill=1..}] at @s if function bm:monst/has_heart run function bm:monst/feed',
              'scoreboard players reset @a bm.kill']
    s = G.FUNCS['loop/second']
    s[-1:-1] = [
        'execute as @e[type=minecraft:ravager,tag=bm.monstrosity] at @s run function bm:monst/tick',
        'execute unless entity @e[type=minecraft:ravager,tag=bm.monstrosity] run bossbar set bm:monst visible false',
        'execute as @a on vehicle if entity @s[tag=bm.mount] run tag @s add bm.claimed',
        'execute as @e[tag=bm.claimed,tag=bm.blood] run function bm:mounts/claim_blood',
        'execute as @e[tag=bm.mount,tag=!bm.claimed] at @s unless entity @a[distance=..100] run tp @s ~ -400 ~']
    t = G.FUNCS['tick']
    t += ['execute as @a[scores={bm.mvic=1}] at @s run function bm:monst/victory',
          'scoreboard players remove @a[scores={bm.mvic=2..}] bm.mvic 1']


def post_admin(G):
    fn, tellraw = G.fn, G.tellraw
    fn('admin/spawn_monstrosity', ['function bm:monst/summon',
                                   tellraw('@s', G.PREFIX + [T('Monstrosity summoned. It only stays while a Blood Moon is up', 'gray'),
                                                             T(' (/scoreboard players set #forced bm.bm 1).', 'yellow')])])
    G.FUNCS['admin/help'].insert(-1, tellraw('@s', [T('/function bm:admin/spawn_monstrosity', 'yellow'),
                                                    T('  spawns the hidden Blood Moon boss at your feet', 'gray')]))
    G.FUNCS['admin/uninstall'].insert(0, 'execute as @a run attribute @s minecraft:movement_speed modifier remove bm:tide_land')
    G.FUNCS['admin/uninstall'].insert(0, 'bossbar remove bm:monst')

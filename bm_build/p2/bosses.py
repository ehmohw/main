"""Boss framework (altar -> intro -> fight -> victory/abandon -> credit) and the seven bosses.

Audience rule: everything a fight does is LOCAL (players in/near that arena). The only global message is the
chat line when someone defeats the Hollow King, like a vanilla advancement.
"""
from items import T
from nbt import snbt, B, F, D as Dd, Int
from p2.config import D, ORDER

FIRE_RES = [{'id': 'minecraft:fire_resistance', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0)}]
NODROP = {k: F(0.0) for k in ['head', 'chest', 'legs', 'feet', 'mainhand', 'offhand', 'body', 'saddle']}


def attrs(**kw):
    return [{'id': f'minecraft:{k}', 'base': Dd(v)} for k, v in kw.items()]


def eq(iid, comps=None):
    e = {'id': iid, 'count': Int(1)}
    if comps: e['components'] = comps
    return e


def boss_nbt(d, name, hp, at, extra=None, effects=None, equipment=None):
    n = {'Tags': ['bm.seen', 'bm.boss', f'bm.boss_{d}', 'bm.newboss'], 'CustomName': T(name, D[d]['color'], bold=True),
         'CustomNameVisible': B(1), 'PersistenceRequired': B(1), 'DeathLootTable': f'bm:p2/{d}/boss', 'Health': F(hp),
         'attributes': attrs(max_health=hp, **at), 'drop_chances': NODROP}
    if effects: n['active_effects'] = effects
    if equipment: n['equipment'] = equipment
    if extra: n.update(extra)
    return snbt(n)


def minion(d, kind, name=None, hp=None, equipment=None, extra=None):
    n = {'Tags': ['bm.seen', 'bm.dgmob', f'bm.minion_{d}']}
    if name: n['CustomName'] = T(name, D[d]['color'])
    if hp: n['Health'] = F(hp); n['attributes'] = attrs(max_health=hp)
    if equipment: n['equipment'] = equipment; n['drop_chances'] = NODROP
    if extra: n.update(extra)
    return f'summon minecraft:{kind} ~ ~ ~ {snbt(n)}'


def at_spawn(d, cmd):
    return f'execute at @e[type=minecraft:marker,tag=bm.mspawn,tag=bm.d_{d},distance=..64,sort=random,limit=1] run {cmd}'


def cap(d, n):
    return [f'execute store result score #mc bm.rng if entity @e[tag=bm.minion_{d},distance=..48]',
            f'execute if score #mc bm.rng matches {n}.. run return 0']


AR = {d: D[d]['arena_r'] for d in D}
# fighters = players standing inside the arena volume (tagged each second by p2/<d>/ina from the arena probes)
FIGHT = lambda d, extra='': f'@a[tag=bm.ina_{d},distance=..{AR[d] + 40},gamemode=!spectator,gamemode=!creative{extra}]'
AUD = lambda d: f'@a[distance=..{AR[d] + 10}]'


def generate(G, builds):
    fn, wjson, title, tellraw, give, loot_entry, uni, KILLED, chance = (G.fn, G.wjson, G.title, G.tellraw, G.give, G.loot_entry,
                                                                        G.uni, G.KILLED, G.chance)
    PREFIX = G.PREFIX
    tick, fast, second, load = [], [], [], []
    ench = {}

    def every(sec, fname, timer='bm.at'):
        return [f'execute if score @s {timer} matches {sec}.. run function {fname}']

    # ================================================================== shared boss helpers
    # warning circle now, eruption 1-2 seconds later (always at least a full second to step away)
    fn('p2/boss/pillar_mark', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.p2","bm.pillar","bm.newpillar"]}',
                               'scoreboard players set @e[type=minecraft:marker,tag=bm.newpillar,distance=..1] bm.life 2',
                               'tag @e[type=minecraft:marker,tag=bm.newpillar,distance=..1] remove bm.newpillar',
                               'particle minecraft:dust{color:[1.0,0.2,0.1],scale:1.6} ~ ~0.1 ~ 0.7 0 0.7 0 25',
                               'playsound minecraft:block.fire.ambient hostile @a[distance=..12] ~ ~ ~ 1 0.6'])
    fn('p2/boss/web_tick', ['scoreboard players remove @s bm.life 1',
                            'execute if score @s bm.life matches ..0 if block ~ ~ ~ minecraft:cobweb run setblock ~ ~ ~ minecraft:air',
                            'execute if score @s bm.life matches ..0 run kill @s'])
    second += ['execute as @e[type=minecraft:marker,tag=bm.tmpweb] at @s run function bm:p2/boss/web_tick',
               'execute as @e[type=minecraft:arrow,tag=bm.hail] if data entity @s {inGround:1b} run kill @s']

    # ================================================================== THE BROODMOTHER (spider)
    ench['venom_bite'] = [('minecraft:apply_mob_effect', 'minecraft:poison', 5, 1)]
    fn('p2/brood/boss_spawn', [
        f'summon minecraft:spider ~ ~9 ~ {boss_nbt("brood", "The Broodmother", 360, dict(attack_damage=9, armor=8, follow_range=48, knockback_resistance=0.9, scale=3.0, movement_speed=0.32, step_height=1.5), effects=[{"id": "minecraft:slow_falling", "amplifier": B(0), "duration": Int(100), "show_particles": B(0)}], equipment={"mainhand": eq("minecraft:bone", {"minecraft:enchantments": {"bm:venom_bite": Int(1)}})})}'])
    fn('p2/brood/boss_tick', [
        'scoreboard players add @s bm.at 1', 'scoreboard players add @s bm.at2 1',
        *every(8, 'bm:p2/brood/web_spit'), *every(15, 'bm:p2/brood/burst', 'bm.at2'),
        'execute store result score #mh bm.rng run data get entity @s Health',
        'execute if score #mh bm.rng matches ..180 unless entity @s[tag=bm.rage] run function bm:p2/brood/enrage'])
    fn('p2/brood/web_spit', ['scoreboard players set @s bm.at 0',
                             'playsound minecraft:entity.llama.spit hostile @a[distance=..30] ~ ~1 ~ 1.5 0.5',
                             f'execute as {FIGHT("brood", ",sort=random,limit=2")} at @s run function bm:p2/brood/web_on'])
    fn('p2/brood/web_on', ['execute if block ~ ~ ~ minecraft:air run setblock ~ ~ ~ minecraft:cobweb',
                           'execute if block ~ ~ ~ minecraft:cobweb run summon minecraft:marker ~ ~ ~ {Tags:["bm.p2","bm.tmpweb","bm.newweb"]}',
                           'scoreboard players set @e[type=minecraft:marker,tag=bm.newweb,distance=..1] bm.life 3',
                           'tag @e[type=minecraft:marker,tag=bm.newweb,distance=..1] remove bm.newweb',
                           'particle minecraft:white_ash ~ ~1 ~ 0.6 0.6 0.6 0 40', title('@s', 'actionbar', T('You are caught in her silk!', 'gray'))])
    fn('p2/brood/burst', ['scoreboard players set @s bm.at2 0', *cap('brood', 8),
                          'particle minecraft:item{item:"minecraft:white_wool"} ~ ~1 ~ 1 0.5 1 0.1 30',
                          'playsound minecraft:entity.turtle.egg_break hostile @a[distance=..30] ~ ~ ~ 1 0.6',
                          minion('brood', 'cave_spider'), minion('brood', 'cave_spider'), minion('brood', 'cave_spider')])
    fn('p2/brood/enrage', ['tag @s add bm.rage', 'effect give @s minecraft:strength infinite 0 true',
                           'attribute @s minecraft:movement_speed modifier add bm:rage 0.25 add_multiplied_base',
                           title(AUD('brood'), 'actionbar', T('The Broodmother shrieks and sheds her skin!', 'red', bold=True)),
                           'playsound minecraft:entity.spider.death hostile @a[distance=..30] ~ ~ ~ 2 0.4',
                           at_spawn('brood', minion('brood', 'spider', 'Brood Guard', 30)), at_spawn('brood', minion('brood', 'spider', 'Brood Guard', 30))])
    INTRO = {}
    INTRO['brood'] = (70, {
        1: ['playsound minecraft:entity.spider.ambient hostile {A} ~ ~8 ~ 2 0.4', 'particle minecraft:white_ash ~ ~6 ~ 8 3 8 0 120'],
        20: [G.title('{A}', 'actionbar', T('The webs above you tremble...', 'gray', italic=True)), 'playsound minecraft:block.cobweb.step hostile {A} ~ ~8 ~ 2 0.5'],
        40: ['playsound minecraft:entity.spider.hurt hostile {A} ~ ~8 ~ 3 0.4', 'particle minecraft:white_ash ~ ~8 ~ 6 2 6 0 200'],
        62: ['title {A} times 5 50 15', G.title('{A}', 'subtitle', T('Mother of the Nest', 'gray', italic=True)),
             G.title('{A}', 'title', T('THE BROODMOTHER', D['brood']['color'], bold=True))],
        70: ['function bm:p2/brood/boss_spawn']})

    # ================================================================== THE FROST MARKSMAN (stray)
    ench['frostbite_mob'] = [('minecraft:apply_mob_effect', 'minecraft:slowness', 3, 1), ('damage', 'minecraft:freeze', 2)]
    bow = eq('minecraft:bow', {'minecraft:enchantments': {'minecraft:power': Int(5), 'minecraft:punch': Int(2), 'bm:frostbite_mob': Int(1)}})
    fn('p2/frost/boss_spawn', [
        f'execute at @e[type=minecraft:marker,tag=bm.perch,tag=bm.d_frost,distance=..40,sort=random,limit=1] run summon minecraft:stray ~ ~ ~ {boss_nbt("frost", "The Frost Marksman", 320, dict(armor=12, follow_range=64, knockback_resistance=0.7, scale=1.8, movement_speed=0.27), equipment={"mainhand": bow, "head": eq("minecraft:diamond_helmet", {"minecraft:trim": {"material": "minecraft:diamond", "pattern": "minecraft:snout"}}), "chest": eq("minecraft:chainmail_chestplate")})}'])
    fn('p2/frost/boss_tick', [
        'scoreboard players add @s bm.at 1', 'scoreboard players add @s bm.at2 1', 'scoreboard players add @s bm.life 1',
        f'execute if score @s bm.life matches 5.. if entity @a[distance=..4,gamemode=!spectator,gamemode=!creative] run function bm:p2/frost/blink',
        *every(10, 'bm:p2/frost/hail'), *every(16, 'bm:p2/frost/blizzard', 'bm.at2'),
        'execute store result score #mh bm.rng run data get entity @s Health',
        'execute if score #mh bm.rng matches ..160 unless entity @s[tag=bm.rage] run function bm:p2/frost/enrage'])
    fn('p2/frost/blink', ['scoreboard players set @s bm.life 0', 'particle minecraft:snowflake ~ ~1 ~ 0.6 1 0.6 0.05 40',
                          'playsound minecraft:entity.enderman.teleport hostile @a[distance=..20] ~ ~ ~ 1 1.4',
                          'tp @s @e[type=minecraft:marker,tag=bm.perch,tag=bm.d_frost,distance=..48,sort=random,limit=1]',
                          'particle minecraft:snowflake ~ ~1 ~ 0.6 1 0.6 0.05 40'])
    fn('p2/frost/hail', ['scoreboard players set @s bm.at 0',
                         f'execute as {FIGHT("frost")} at @s run function bm:p2/frost/hail_on'])
    fn('p2/frost/hail_on', ['playsound minecraft:entity.arrow.shoot hostile @s ~ ~8 ~ 1.5 0.6',
                            'particle minecraft:snowflake ~ ~6 ~ 1.5 0.5 1.5 0 30', title('@s', 'actionbar', T('Hail of arrows - move!', 'aqua')),
                            *[f'summon minecraft:arrow ~{dx} ~11 ~{dz} {{Motion:[0.0,-1.4,0.0],damage:3.0d,pickup:0b,Tags:["bm.hail"]}}'
                              for dx, dz in ((0.6, 0.4), (-0.7, 0.3), (0.2, -0.8), (1.2, 1.1))]])
    fn('p2/frost/blizzard', ['scoreboard players set @s bm.at2 0',
                             f'effect give {FIGHT("frost")} minecraft:slowness 4 1',
                             f'execute as {FIGHT("frost")} at @s run particle minecraft:snowflake ~ ~2 ~ 3 2 3 0.05 120 normal @s',
                             'playsound minecraft:item.elytra.flying hostile @a[distance=..30] ~ ~ ~ 0.8 0.5',
                             title(AUD('frost'), 'actionbar', T('A blizzard howls through the spire!', 'aqua')),
                             *cap('frost', 6), at_spawn('frost', minion('frost', 'stray')), at_spawn('frost', minion('frost', 'stray'))])
    fn('p2/frost/enrage', ['tag @s add bm.rage', 'effect give @s minecraft:speed infinite 0 true',
                           title(AUD('frost'), 'actionbar', T('The Marksman calls his steed!', 'aqua', bold=True)),
                           'summon minecraft:skeleton_horse ~ ~ ~ {Tags:["bm.seen","bm.minion_frost"],Tame:1b,equipment:{saddle:{id:"minecraft:saddle",count:1}},CustomName:{text:"Rime Steed",color:"aqua"},Health:60f,attributes:[{id:"minecraft:max_health",base:60d}]}',
                           'ride @s mount @e[type=minecraft:skeleton_horse,tag=bm.minion_frost,distance=..3,sort=nearest,limit=1]',
                           'playsound minecraft:entity.skeleton_horse.ambient hostile @a[distance=..30] ~ ~ ~ 2 0.6'])
    INTRO['frost'] = (70, {
        1: ['playsound minecraft:item.elytra.flying hostile {A} ~ ~ ~ 1 0.5', 'particle minecraft:snowflake ~ ~6 ~ 10 4 10 0.02 300'],
        24: ['playsound minecraft:entity.arrow.hit hostile {A} ~ ~2 ~ 2 0.7', G.title('{A}', 'actionbar', T('An arrow thunks into the wall beside you.', 'gray', italic=True))],
        44: ['playsound minecraft:entity.stray.ambient hostile {A} ~ ~4 ~ 3 0.5'],
        62: ['title {A} times 5 50 15', G.title('{A}', 'subtitle', T('Two hundred winters on the string.', 'gray', italic=True)),
             G.title('{A}', 'title', T('THE FROST MARKSMAN', D['frost']['color'], bold=True))],
        70: ['function bm:p2/frost/boss_spawn']})

    # ================================================================== THE DROWNED TYRANT (drowned)
    ench['tidal_crush'] = [('minecraft:apply_mob_effect', 'minecraft:slowness', 3, 1), ('minecraft:apply_mob_effect', 'minecraft:nausea', 4, 0)]
    tri = eq('minecraft:trident', {'minecraft:enchantments': {'minecraft:impaling': Int(5), 'bm:tidal_crush': Int(1)}})
    fn('p2/tide/boss_spawn', [
        f'summon minecraft:drowned ~ ~ ~ {boss_nbt("tide", "The Drowned Tyrant", 420, dict(attack_damage=10, armor=10, follow_range=56, knockback_resistance=0.9, scale=2.4, movement_speed=0.28), equipment={"mainhand": tri, "head": eq("minecraft:golden_helmet", {"minecraft:trim": {"material": "minecraft:emerald", "pattern": "minecraft:tide"}})})}'])
    fn('p2/tide/boss_tick', [
        'scoreboard players add @s bm.at 1', 'scoreboard players add @s bm.at2 1', 'scoreboard players add @s bm.life 1',
        *every(9, 'bm:p2/tide/slam'), *every(14, 'bm:p2/tide/call', 'bm.at2'),
        'execute if score @s bm.life matches 12.. run function bm:p2/tide/riptide',
        'execute store result score #mh bm.rng run data get entity @s Health',
        'execute if score #mh bm.rng matches ..210 unless entity @s[tag=bm.rage] run function bm:p2/tide/enrage'])
    fn('p2/tide/slam', ['scoreboard players set @s bm.at 0', 'particle minecraft:splash ~ ~0.5 ~ 4 0.3 4 0.4 200',
                        'playsound minecraft:entity.generic.splash hostile @a[distance=..24] ~ ~ ~ 2 0.5',
                        f'execute as @a[distance=..6,gamemode=!spectator,gamemode=!creative] run damage @s 4 minecraft:mob_attack by @e[tag=bm.boss_tide,limit=1,sort=nearest]',
                        'effect give @a[distance=..6,gamemode=!spectator,gamemode=!creative] minecraft:slowness 3 1'])
    fn('p2/tide/riptide', ['scoreboard players set @s bm.life 0',
                           f'execute as {FIGHT("tide", ",sort=random,limit=1")} at @s run function bm:p2/tide/riptide_on'])
    fn('p2/tide/riptide_on', ['particle minecraft:bubble_pop ~ ~1 ~ 1 1 1 0.1 40', 'playsound minecraft:item.trident.riptide_3 hostile @a[distance=..24] ~ ~ ~ 1.5 0.8',
                              'execute rotated ~ 0 run tp @e[tag=bm.boss_tide,limit=1,sort=nearest] ^ ^ ^-2.5',
                              'damage @s 3 minecraft:mob_attack by @e[tag=bm.boss_tide,limit=1,sort=nearest]',
                              title('@s', 'actionbar', T('The Tyrant surges behind you!', 'aqua'))])
    fn('p2/tide/call', ['scoreboard players set @s bm.at2 0', *cap('tide', 6),
                        'playsound minecraft:entity.drowned.ambient_water hostile @a[distance=..30] ~ ~ ~ 2 0.6',
                        at_spawn('tide', minion('tide', 'drowned', equipment={'mainhand': eq('minecraft:trident')})),
                        at_spawn('tide', minion('tide', 'drowned', equipment={'mainhand': eq('minecraft:trident')}))])
    fn('p2/tide/enrage', ['tag @s add bm.rage', 'effect give @s minecraft:resistance infinite 0 true', 'effect give @s minecraft:regeneration 10 1 true',
                          'effect give @s minecraft:dolphins_grace infinite 0 true',
                          title(AUD('tide'), 'actionbar', T('The Tyrant raises the Crown of the Deep!', 'aqua', bold=True)),
                          'playsound minecraft:entity.elder_guardian.curse hostile @a[distance=..30] ~ ~ ~ 1 0.7'])
    INTRO['tide'] = (70, {
        1: ['playsound minecraft:ambient.underwater.loop.additions.ultra_rare hostile {A} ~ ~ ~ 2 0.6', 'particle minecraft:bubble_pop ~ ~1 ~ 8 1 8 0.05 200'],
        24: ['playsound minecraft:block.conduit.ambient.short hostile {A} ~ ~ ~ 2 0.5', G.title('{A}', 'actionbar', T('The water churns...', 'gray', italic=True))],
        44: ['playsound minecraft:entity.drowned.ambient_water hostile {A} ~ ~ ~ 3 0.4', 'particle minecraft:splash ~ ~1 ~ 3 0.5 3 0.4 300'],
        62: ['title {A} times 5 50 15', G.title('{A}', 'subtitle', T('Lord of the Sunken Throne', 'gray', italic=True)),
             G.title('{A}', 'title', T('THE DROWNED TYRANT', D['tide']['color'], bold=True))],
        70: ['function bm:p2/tide/boss_spawn']})

    # ================================================================== THE ARCHMAGE (evoker)
    fn('p2/hex/boss_spawn', [
        f'summon minecraft:evoker ~ ~ ~ {boss_nbt("hex", "The Archmage", 300, dict(armor=10, follow_range=48, knockback_resistance=0.8, scale=1.6, movement_speed=0.5))}'])
    fn('p2/hex/boss_tick', [
        'scoreboard players add @s bm.at 1', 'scoreboard players add @s bm.at2 1', 'scoreboard players add @s bm.life 1',
        *every(7, 'bm:p2/hex/blink', 'bm.life'), *every(11, 'bm:p2/hex/lances'), *every(15, 'bm:p2/hex/coven', 'bm.at2'),
        'execute store result score #mh bm.rng run data get entity @s Health',
        'execute if score #mh bm.rng matches ..150 unless entity @s[tag=bm.rage] run function bm:p2/hex/enrage'])
    fn('p2/hex/blink', ['scoreboard players set @s bm.life 0', 'particle minecraft:reverse_portal ~ ~1 ~ 0.5 1 0.5 0.1 60',
                        'playsound minecraft:entity.illusioner.mirror_move hostile @a[distance=..24] ~ ~ ~ 1.5 1',
                        'tp @s @e[type=minecraft:marker,tag=bm.perch,tag=bm.d_hex,distance=..48,sort=random,limit=1]',
                        'particle minecraft:reverse_portal ~ ~1 ~ 0.5 1 0.5 0.1 60'])
    fn('p2/hex/lances', ['scoreboard players set @s bm.at 0', 'playsound minecraft:entity.evoker.prepare_attack hostile @a[distance=..30] ~ ~ ~ 2 0.8',
                         f'execute as {FIGHT("hex", ",sort=random,limit=2")} at @s run function bm:p2/hex/lance'])
    fn('p2/hex/beam', [f'particle minecraft:witch ^ ^ ^{i} 0.05 0.05 0.05 0 2' for i in range(1, 25)])
    fn('p2/hex/lance', ['execute positioned as @e[tag=bm.boss_hex,limit=1,sort=nearest] anchored eyes facing entity @s eyes run function bm:p2/hex/beam',
                        'damage @s 3 minecraft:magic by @e[tag=bm.boss_hex,limit=1,sort=nearest]',
                        'effect give @s minecraft:levitation 1 1', 'playsound minecraft:entity.illusioner.cast_spell hostile @s ~ ~ ~ 1 1.2'])
    fn('p2/hex/coven', ['scoreboard players set @s bm.at2 0', *cap('hex', 6),
                        'playsound minecraft:entity.witch.celebrate hostile @a[distance=..30] ~ ~ ~ 2 0.7',
                        at_spawn('hex', minion('hex', 'witch')), at_spawn('hex', minion('hex', 'witch')),
                        at_spawn('hex', minion('hex', 'vindicator', equipment={'mainhand': eq('minecraft:iron_axe')}))])
    fn('p2/hex/enrage', ['tag @s add bm.rage',
                         title(AUD('hex'), 'actionbar', T('Mirror Veil! Which Archmage is real?', 'light_purple', bold=True)),
                         'playsound minecraft:entity.illusioner.prepare_mirror hostile @a[distance=..30] ~ ~ ~ 2 1',
                         *[at_spawn('hex', minion('hex', 'evoker', 'The Archmage', 20, extra={'Glowing': B(1)})) for _ in range(2)],
                         'function bm:p2/hex/blink'])
    INTRO['hex'] = (70, {
        1: ['playsound minecraft:block.bell.resonate hostile {A} ~ ~ ~ 2 0.6', 'particle minecraft:enchant ~ ~3 ~ 6 3 6 1 300'],
        24: ['playsound minecraft:entity.evoker.ambient hostile {A} ~ ~ ~ 3 0.5', G.title('{A}', 'actionbar', T('Candles gutter. Someone is chanting.', 'gray', italic=True))],
        44: ['playsound minecraft:entity.illusioner.prepare_blindness hostile {A} ~ ~ ~ 2 0.6', 'particle minecraft:witch ~ ~2 ~ 4 2 4 0 200'],
        62: ['title {A} times 5 50 15', G.title('{A}', 'subtitle', T('Keeper of the Hollow Pact', 'gray', italic=True)),
             G.title('{A}', 'title', T('THE ARCHMAGE', D['hex']['color'], bold=True))],
        70: ['function bm:p2/hex/boss_spawn']})

    # ================================================================== BOBBERY (wither skeleton) - semi-final
    def netherite(p, trim=('minecraft:gold', 'minecraft:rib')):
        return eq(f'minecraft:netherite_{p}', {'minecraft:trim': {'material': trim[0], 'pattern': trim[1]}})
    axe = eq('minecraft:netherite_axe', {'minecraft:enchantments': {'minecraft:sharpness': Int(6), 'minecraft:fire_aspect': Int(2)},
                                         'minecraft:item_name': T("Bobbery's Axe", D['keep']['color'], bold=True)})
    fn('p2/keep/boss_spawn', [
        f'summon minecraft:wither_skeleton ~ ~ ~ {boss_nbt("keep", "Bobbery", 500, dict(attack_damage=12, follow_range=64, knockback_resistance=1.0, scale=1.7, movement_speed=0.3), effects=FIRE_RES, equipment={"mainhand": axe, "head": netherite("helmet"), "chest": netherite("chestplate"), "legs": netherite("leggings"), "feet": netherite("boots")})}',
        'execute as @e[type=minecraft:wither_skeleton,tag=bm.boss_keep,distance=..4,sort=nearest,limit=1] at @s run function bm:p2/keep/steed'])
    # 2.2: Bobbery rides a great spider ("Mutton", stolen from the Broodmother's nest)
    fn('p2/keep/steed', [minion('keep', 'spider', 'Mutton, Bobbery\'s Steed', 140, extra={
                             'Tags': ['bm.seen', 'bm.dgmob', 'bm.minion_keep', 'bm.keep_steed'], 'PersistenceRequired': B(1),
                             'attributes': attrs(max_health=140, scale=1.4, movement_speed=0.34, follow_range=64, attack_damage=6)}),
                         'ride @s mount @e[type=minecraft:spider,tag=bm.keep_steed,distance=..3,sort=nearest,limit=1]',
                         'particle minecraft:large_smoke ~ ~1 ~ 0.6 0.6 0.6 0.02 20'])
    fn('p2/keep/boss_tick', [
        'scoreboard players add @s bm.at 1', 'scoreboard players add @s bm.at2 1', 'scoreboard players add @s bm.life 1',
        *every(8, 'bm:p2/keep/cleave'), *every(12, 'bm:p2/keep/crew', 'bm.at2'), *every(18, 'bm:p2/keep/pillars', 'bm.life'),
        'execute store result score #mh bm.rng run data get entity @s Health',
        'execute if score #mh bm.rng matches ..250 unless entity @s[tag=bm.rage] run function bm:p2/keep/wilfrey',
        'execute if score #mh bm.rng matches ..125 unless entity @s[tag=bm.rage2] run function bm:p2/keep/enough'])
    fn('p2/keep/cleave', ['scoreboard players set @s bm.at 0', 'playsound minecraft:entity.wither.shoot hostile @a[distance=..24] ~ ~ ~ 1.5 0.5',
                          'particle minecraft:soul_fire_flame ~ ~0.3 ~ 3 0.1 3 0.02 120',
                          f'execute as @a[distance=..4.5,gamemode=!spectator,gamemode=!creative] run damage @s 5 minecraft:mob_attack by @e[tag=bm.boss_keep,limit=1,sort=nearest]',
                          'effect give @a[distance=..4.5,gamemode=!spectator,gamemode=!creative] minecraft:wither 3 1'])
    fn('p2/keep/crew', ['scoreboard players set @s bm.at2 0', *cap('keep', 6),
                        'playsound minecraft:entity.wither_skeleton.ambient hostile @a[distance=..30] ~ ~ ~ 2 0.5',
                        at_spawn('keep', minion('keep', 'wither_skeleton', "Bobbery's Bonecrew", equipment={'mainhand': eq('minecraft:stone_sword')})),
                        at_spawn('keep', minion('keep', 'wither_skeleton', "Bobbery's Bonecrew", equipment={'mainhand': eq('minecraft:stone_sword')})),
                        at_spawn('keep', minion('keep', 'blaze'))])
    fn('p2/keep/pillars', ['scoreboard players set @s bm.life 0',
                           title(AUD('keep'), 'actionbar', T('The floor glows red beneath you - MOVE!', 'red')),
                           f'execute as {FIGHT("keep", ",sort=random,limit=3")} at @s run function bm:p2/boss/pillar_mark'])
    fn('p2/boss/pillar_fire', ['particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 1.5 0.3 0.02 60', 'particle minecraft:flame ~ ~0.5 ~ 0.6 0.2 0.6 0.02 30',
                               'playsound minecraft:item.firecharge.use hostile @a[distance=..16] ~ ~ ~ 1 0.6',
                               'execute as @a[distance=..1.6,gamemode=!spectator,gamemode=!creative] run damage @s 6 minecraft:in_fire',
                               'kill @s'])
    fn('p2/boss/pillar_tick', ['scoreboard players remove @s bm.life 1', 'particle minecraft:dust{color:[1.0,0.2,0.1],scale:1.6} ~ ~0.1 ~ 0.7 0 0.7 0 25',
                               'execute if score @s bm.life matches ..0 run function bm:p2/boss/pillar_fire'])
    second.append('execute as @e[type=minecraft:marker,tag=bm.pillar] at @s run function bm:p2/boss/pillar_tick')
    fn('p2/keep/wilfrey', ['tag @s add bm.rage', 'effect give @s minecraft:strength infinite 0 true',
                           'title {A} times 10 60 20'.format(A=AUD('keep')),
                           G.title(AUD('keep'), 'subtitle', T('"Cousin... enough." A gentle light fills the hall.', 'white', italic=True)),
                           G.title(AUD('keep'), 'title', T('', 'white')),
                           f'effect give {FIGHT("keep")} minecraft:resistance 10 0', f'effect give {FIGHT("keep")} minecraft:regeneration 6 1',
                           'particle minecraft:end_rod ~ ~2 ~ 6 2 6 0.02 120',
                           'playsound minecraft:block.beacon.activate player @a[distance=..30] ~ ~ ~ 1 1.2'])
    fn('p2/keep/enough', ['tag @s add bm.rage2', 'effect give @s minecraft:strength infinite 1 true', 'effect give @s minecraft:speed infinite 0 true',
                          title(AUD('keep'), 'actionbar', T('BOBBERY: "ENOUGH! This keep is MINE!"', 'dark_red', bold=True)),
                          'playsound minecraft:entity.wither.spawn hostile @a[distance=..30] ~ ~ ~ 0.6 1.2',
                          at_spawn('keep', minion('keep', 'blaze')), at_spawn('keep', minion('keep', 'blaze'))])
    INTRO['keep'] = (80, {
        1: ['playsound minecraft:ambient.soul_sand_valley.mood hostile {A} ~ ~ ~ 2 0.6', 'particle minecraft:soul ~ ~1 ~ 8 1 8 0.02 80'],
        20: ['playsound minecraft:entity.wither_skeleton.step hostile {A} ~ ~ ~ 2 0.5', G.title('{A}', 'actionbar', T('Heavy footsteps echo from the throne...', 'gray', italic=True))],
        40: ['playsound minecraft:entity.wither_skeleton.ambient hostile {A} ~ ~ ~ 3 0.4', 'particle minecraft:soul_fire_flame ~ ~0.2 ~ 8 0.1 8 0.01 150'],
        58: [G.title('{A}', 'actionbar', T('"So. My cousin\'s little helpers."', 'dark_red', italic=True))],
        70: ['title {A} times 5 50 15', G.title('{A}', 'subtitle', T("Usurper of Wilfrey's Keep", 'gray', italic=True)),
             G.title('{A}', 'title', T('BOBBERY', '#c0392b', bold=True))],
        80: ['function bm:p2/keep/boss_spawn']})

    # ================================================================== THE HOLLOW KING (final; two phases)
    crown = eq('minecraft:netherite_helmet', {'minecraft:item_model': 'bm:crown', 'minecraft:trim': {'material': 'minecraft:quartz', 'pattern': 'minecraft:silence'}})
    ench['hollow_touch'] = [('minecraft:apply_mob_effect', 'minecraft:wither', 4, 1), ('minecraft:apply_mob_effect', 'minecraft:darkness', 3, 0)]
    sword = eq('minecraft:netherite_sword', {'minecraft:enchantments': {'minecraft:sharpness': Int(5), 'bm:hollow_touch': Int(1)}})
    fn('p2/hollow/boss_spawn', [
        'scoreboard players set @s bm.at2 0',
        f'summon minecraft:wither_skeleton ~ ~ ~ {boss_nbt("hollow", "The Hollow King", 700, dict(attack_damage=14, armor=16, armor_toughness=8, follow_range=64, knockback_resistance=1.0, scale=2.4, movement_speed=0.3), effects=FIRE_RES, equipment={"mainhand": sword, "head": crown, "chest": netherite("chestplate", ("minecraft:quartz", "minecraft:silence")), "legs": netherite("leggings", ("minecraft:quartz", "minecraft:silence")), "feet": netherite("boots", ("minecraft:quartz", "minecraft:silence"))}, extra={"DeathLootTable": "bm:entities/empty"})}'])
    fn('p2/hollow/boss_tick', [
        'execute if entity @s[type=minecraft:wither] run return run function bm:p2/hollow/wither_tick',
        'scoreboard players add @s bm.at 1', 'scoreboard players add @s bm.at2 1', 'scoreboard players add @s bm.life 1',
        *every(6, 'bm:p2/hollow/decree'), *every(10, 'bm:p2/hollow/spears', 'bm.life'), *every(10, 'bm:p2/hollow/court', 'bm.at2')])
    fn('p2/hollow/decree', ['scoreboard players set @s bm.at 0', f'effect give {FIGHT("hollow")} minecraft:darkness 3 0',
                            f'effect give {FIGHT("hollow")} minecraft:slowness 2 0',
                            'playsound minecraft:entity.warden.sonic_charge hostile @a[distance=..40] ~ ~ ~ 1.5 0.5',
                            title(AUD('hollow'), 'actionbar', T('"KNEEL."', 'dark_gray', bold=True))])
    fn('p2/hollow/fangs', [f'summon minecraft:evoker_fangs ^ ^ ^{2 + i * 1.5:.1f} {{Warmup:{i * 3}}}' for i in range(8)])
    fn('p2/hollow/spears', ['scoreboard players set @s bm.life 0', 'playsound minecraft:entity.evoker.prepare_attack hostile @a[distance=..40] ~ ~ ~ 2 0.5',
                            f'execute as {FIGHT("hollow", ",sort=random,limit=2")} at @s run function bm:p2/hollow/spear_line'])
    fn('p2/hollow/spear_line', ['execute positioned as @e[tag=bm.boss_hollow,limit=1,sort=nearest] rotated ~ 0 facing entity @s feet rotated ~ 0 run function bm:p2/hollow/fangs'])
    knight = minion('hollow', 'wither_skeleton', 'Hollow Knight', 30, equipment={'mainhand': eq('minecraft:netherite_sword'), 'head': eq('minecraft:netherite_helmet')})
    archer = minion('hollow', 'stray', 'Hollow Archer', equipment={'mainhand': eq('minecraft:bow')})
    brute = minion('hollow', 'piglin_brute', 'Hollow Brute', 50, equipment={'mainhand': eq('minecraft:netherite_axe')}, extra={'IsImmuneToZombification': B(1)})
    hog = minion('hollow', 'hoglin', 'Hollow Tusker', 40, extra={'IsImmuneToZombification': B(1)})
    # 2.2: the court answers every 10 s in phase 1 and every 8 s in phase 2, loudly, from smoking rifts
    fn('p2/hollow/rift', ['particle minecraft:large_smoke ~ ~1 ~ 0.4 0.8 0.4 0.03 25', 'particle minecraft:soul_fire_flame ~ ~0.2 ~ 0.5 0.1 0.5 0.02 15',
                          'playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..40] ~ ~ ~ 1 0.6'])
    fn('p2/hollow/court', ['scoreboard players set @s bm.at2 0', *cap('hollow', 12),
                           'playsound minecraft:entity.wither_skeleton.ambient hostile @a[distance=..40] ~ ~ ~ 2 0.4',
                           title(AUD('hollow'), 'actionbar', T('"RISE, MY COURT."', '#e5e4e2', bold=True)),
                           *[at_spawn('hollow', 'function bm:p2/hollow/rift') for _ in range(2)],
                           # 2.49: the court is all undead - a brute would turn on the King (a wither skeleton) itself
                           *[at_spawn('hollow', knight) for _ in range(3)], at_spawn('hollow', archer), at_spawn('hollow', archer)])
    # phase 2: when the king falls, he rises as a Wither (mob griefing is off in the Hollow Throne, so he can't break out)
    if 'hollow' in builds:
        fn('p2/hollow/on_boss_gone', ['execute if score @s bm.at2 matches 0 run return run function bm:p2/hollow/ascend', 'function bm:p2/hollow/victory'])
    fn('p2/hollow/ascend', ['scoreboard players set @s bm.at2 1',
                            'title {A} times 5 70 20'.format(A=AUD('hollow')),
                            G.title(AUD('hollow'), 'subtitle', T('Get back from the throne!', 'red')),
                            G.title(AUD('hollow'), 'title', T('THE HOLLOW KING ASCENDS', '#e5e4e2', bold=True)),
                            'playsound minecraft:entity.wither.spawn hostile @a[distance=..60] ~ ~ ~ 1 0.6',
                            'particle minecraft:sculk_soul ~ ~4 ~ 3 3 3 0.05 300',
                            'bossbar set bm:boss_hollow visible false',
                            f'summon minecraft:wither ~ ~6 ~ {snbt({"Tags": ["bm.seen", "bm.boss", "bm.boss_hollow"], "CustomName": T("The Hollow King, Unbound", "#e5e4e2", bold=True), "PersistenceRequired": B(1), "DeathLootTable": "bm:p2/hollow/boss", "attributes": attrs(max_health=900, armor=8), "Health": F(900)})}'])
    fn('p2/hollow/wither_tick', ['scoreboard players add @s bm.at 1', *every(8, 'bm:p2/hollow/w_court'), 'scoreboard players add @s bm.life 1',
                                 *every(8, 'bm:p2/hollow/w_storm', 'bm.life')])
    fn('p2/hollow/w_court', ['scoreboard players set @s bm.at 0', *cap('hollow', 12),
                             title(AUD('hollow'), 'actionbar', T('The dead of the Throne answer their King!', 'red')),
                             *[at_spawn('hollow', 'function bm:p2/hollow/rift') for _ in range(2)],
                             # 2.49: undead only - the Wither hunts anything living, brutes and tuskers included
                             *[at_spawn('hollow', knight) for _ in range(3)], at_spawn('hollow', archer), at_spawn('hollow', archer)])
    fn('p2/hollow/w_storm', ['scoreboard players set @s bm.life 0', 'particle minecraft:soul ~ ~ ~ 8 3 8 0.05 200',
                             'playsound minecraft:particle.soul_escape hostile @a[distance=..40] ~ ~ ~ 2 0.5',
                             'effect give @a[distance=..10,gamemode=!spectator,gamemode=!creative] minecraft:wither 4 1'])
    INTRO['hollow'] = (100, {
        1: ['playsound minecraft:entity.warden.heartbeat hostile {A} ~ ~ ~ 1 0.6', 'particle minecraft:sculk_soul ~ ~2 ~ 10 3 10 0.01 100'],
        20: ['playsound minecraft:entity.warden.heartbeat hostile {A} ~ ~ ~ 1 0.7'],
        36: ['playsound minecraft:entity.warden.heartbeat hostile {A} ~ ~ ~ 1 0.8', G.title('{A}', 'actionbar', T('The throne is not empty.', 'gray', italic=True))],
        50: ['playsound minecraft:block.sculk_shrieker.shriek hostile {A} ~ ~ ~ 2 0.5', 'particle minecraft:ash ~ ~4 ~ 12 5 12 0 500'],
        78: ['title {A} times 5 60 20', G.title('{A}', 'subtitle', T('Eldest of the wither-born', 'gray', italic=True)),
             G.title('{A}', 'title', T('THE HOLLOW KING', '#e5e4e2', bold=True))],
        100: ['function bm:p2/hollow/boss_spawn']})

    # ================================================================== THE GOLDEN GOOSE (lucky) - chicken jockey
    fn('p2/lucky/boss_spawn', [
        f'summon minecraft:chicken ~ ~1 ~ {boss_nbt("lucky", "The Golden Goose", 260, dict(armor=6, follow_range=48, knockback_resistance=0.6, scale=3.5, movement_speed=0.35), extra={"variant": "minecraft:warm"}, effects=[{"id": "minecraft:glowing", "amplifier": B(0), "duration": Int(-1), "show_particles": B(0)}])}',
        minion('lucky', 'zombie', 'Lucky Jack', 40, equipment={'mainhand': eq('minecraft:golden_sword', {'minecraft:enchantments': {'minecraft:sharpness': Int(4)}}),
                                                               'head': eq('minecraft:golden_helmet'), 'chest': eq('minecraft:golden_chestplate')},
               extra={'IsBaby': B(1), 'Tags': ['bm.seen', 'bm.dgmob', 'bm.minion_lucky', 'bm.jack']}),
        'ride @e[type=minecraft:zombie,tag=bm.jack,distance=..4,sort=nearest,limit=1] mount @e[type=minecraft:chicken,tag=bm.boss_lucky,distance=..4,sort=nearest,limit=1]'])
    fn('p2/lucky/boss_tick', [
        'scoreboard players add @s bm.at 1', 'scoreboard players add @s bm.at2 1', 'scoreboard players add @s bm.life 1',
        *every(6, 'bm:p2/lucky/eggs'), *every(12, 'bm:p2/lucky/jackpot', 'bm.at2'), *every(9, 'bm:p2/lucky/dash', 'bm.life'),
        'particle minecraft:wax_on ~ ~2 ~ 1 1 1 0 4',
        'execute store result score #mh bm.rng run data get entity @s Health',
        'execute if score #mh bm.rng matches ..130 unless entity @s[tag=bm.rage] run function bm:p2/lucky/double'])
    fn('p2/lucky/eggs', ['scoreboard players set @s bm.at 0', 'playsound minecraft:entity.chicken.egg hostile @a[distance=..24] ~ ~ ~ 2 0.6',
                         title(AUD('lucky'), 'actionbar', T('Golden eggs incoming!', 'gold')),
                         f'execute as {FIGHT("lucky", ",sort=random,limit=3")} at @s run function bm:p2/lucky/egg_on'])
    fn('p2/lucky/egg_on', ['summon minecraft:snowball ~ ~9 ~ {Motion:[0.0,-0.8,0.0],Item:{id:"minecraft:egg",count:1}}', 'function bm:p2/boss/pillar_mark'])
    fn('p2/lucky/jackpot', ['scoreboard players set @s bm.at2 0', *cap('lucky', 7),
                            'playsound minecraft:block.amethyst_block.chime hostile @a[distance=..24] ~ ~ ~ 2 1.2',
                            title(AUD('lucky'), 'actionbar', T('Jackpot! Lucky mobs pour out!', 'yellow')),
                            *[at_spawn('lucky', 'summon minecraft:zombie ~ ~ ~ {Tags:["bm.newlucky","bm.minion_lucky"]}') for _ in range(3)],
                            'execute as @e[type=minecraft:zombie,tag=bm.newlucky] at @s run function bm:mobs/lucky/zombie',
                            'tag @e[type=minecraft:zombie,tag=bm.newlucky] add bm.seen', 'tag @e[tag=bm.newlucky] remove bm.newlucky'])
    fn('p2/lucky/dash', ['scoreboard players set @s bm.life 0', 'effect give @s minecraft:speed 3 3 true',
                         'particle minecraft:item{item:"minecraft:feather"} ~ ~1 ~ 1 1 1 0.1 30', 'playsound minecraft:entity.chicken.hurt hostile @a[distance=..24] ~ ~ ~ 2 0.6'])
    fn('p2/lucky/double', ['tag @s add bm.rage', 'effect give @s minecraft:resistance 8 1 true',
                           title(AUD('lucky'), 'actionbar', T('Double or nothing!', 'gold', bold=True)),
                           'effect give @e[type=minecraft:zombie,tag=bm.jack,distance=..8] minecraft:strength infinite 1 true',
                           'playsound minecraft:block.bell.use hostile @a[distance=..24] ~ ~ ~ 2 1.4'])
    INTRO['lucky'] = (60, {
        1: ['playsound minecraft:block.amethyst_block.chime hostile {A} ~ ~ ~ 2 0.6', 'particle minecraft:wax_on ~ ~3 ~ 6 3 6 0 200'],
        20: ['playsound minecraft:entity.chicken.ambient hostile {A} ~ ~ ~ 3 0.5', G.title('{A}', 'actionbar', T('Something enormous clucks.', 'gray', italic=True))],
        40: ['playsound minecraft:block.bell.use hostile {A} ~ ~ ~ 2 0.8'],
        48: ['title {A} times 5 50 15', G.title('{A}', 'subtitle', T('...and Lucky Jack, who never lost a bet', 'gray', italic=True)),
             G.title('{A}', 'title', T('THE GOLDEN GOOSE', '#ffd700', bold=True))],
        60: ['function bm:p2/lucky/boss_spawn']})

    # ================================================================== custom boss/item enchantments
    def enchant(eid, effects, slots, supported, victim_type='minecraft:player', aff='victim'):
        eff = []
        for e in effects:
            if e[0] == 'damage':
                eff.append({'type': 'minecraft:damage_entity', 'damage_type': e[1], 'min_damage': float(e[2]), 'max_damage': float(e[2])})
            else:
                eff.append({'type': 'minecraft:apply_mob_effect', 'to_apply': e[1], 'min_duration': float(e[2]), 'max_duration': float(e[2]),
                            'min_amplifier': float(e[3]), 'max_amplifier': float(e[3])})
        body = {'type': 'minecraft:all_of', 'effects': eff} if len(eff) > 1 else eff[0]
        req = {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:entity_type': victim_type}}
        wjson(f'bm/enchantment/{eid}.json', {
            'anvil_cost': 8, 'description': T(eid.replace('_', ' ').title(), 'dark_red'), 'max_level': 1, 'weight': 1,
            'min_cost': {'base': 1, 'per_level_above_first': 0}, 'max_cost': {'base': 1, 'per_level_above_first': 0},
            'slots': slots, 'supported_items': supported,
            'effects': {'minecraft:post_attack': [{'affected': aff, 'enchanted': 'attacker', 'effect': body, 'requirements': req}]}})
    for eid, effs in ench.items():
        enchant(eid, effs, ['mainhand'], '#minecraft:enchantable/weapon')
    # player-side enchantments on boss drops (they affect hostile mobs, not players)
    enchant('venom', [('minecraft:apply_mob_effect', 'minecraft:poison', 4, 1)], ['mainhand'], '#minecraft:enchantable/weapon', '#bm:hostile')
    enchant('frostbite', [('minecraft:apply_mob_effect', 'minecraft:slowness', 3, 1), ('damage', 'minecraft:freeze', 2)], ['mainhand'], '#minecraft:enchantable/bow', '#bm:hostile')
    enchant('arcane', [('minecraft:apply_mob_effect', 'minecraft:levitation', 2, 0)], ['mainhand'], '#minecraft:enchantable/mace', '#bm:hostile')

    # ================================================================== framework: altar -> arena state machine
    for d, Bd in builds.items():
        cfg = D[d]
        idx, ar = cfg['idx'], AR[d]
        r2 = cfg['radius'] * 2
        NP = len(Bd.meta['puzzles'])
        A = AUD(d)
        prev = ORDER[idx - 2] if idx >= 2 else None
        ar_sel = f'@e[type=minecraft:marker,tag=bm.arena,tag=bm.d_{d},distance=..64,sort=nearest,limit=1]'
        load += [f'bossbar add bm:boss_{d} {snbt(T(cfg["boss"], cfg["color"], bold=True))}', f'bossbar set bm:boss_{d} color red',
                 f'bossbar set bm:boss_{d} style notched_10', f'bossbar set bm:boss_{d} visible false']
        # ---- altar
        tl = ['execute if score @s bm.acd matches 1.. run return 0', 'scoreboard players set @s bm.acd 2',
              f'execute store result score #bs bm.rng run scoreboard players get {ar_sel} bm.bs',
              f'execute if score #bs bm.rng matches 1.. run return run ' + title('@s', 'actionbar', T(f'{cfg["boss"]} is already awake!', 'red')),
              f'execute store result score #dpz bm.rng run scoreboard players get @e[type=minecraft:marker,tag=bm.dg,tag=bm.d_{d},distance=..{r2},sort=nearest,limit=1] bm.pz',
              f'execute unless score #dpz bm.rng matches {NP}.. run return run function bm:p2/{d}/altar_dormant']
        fn(f'p2/{d}/altar_dormant', [title('@s', 'actionbar', T('The altar is cold. Every trial in this place must be solved first.', 'gray', italic=True)),
                                     'playsound minecraft:block.respawn_anchor.deplete block @s ~ ~ ~ 0.6 0.6'])
        if idx >= 1:
            tl.append(f'execute unless score @s bm.conq matches {idx - 1}.. run return run function bm:p2/{d}/altar_record')
            fn(f'p2/{d}/altar_record', [title('@s', 'actionbar', T(f'Your conquest record is incomplete. Defeat {D[prev]["boss"]} first.' if prev else 'Your record is incomplete.', 'red')),
                                        'playsound minecraft:block.note_block.bass block @s ~ ~ ~ 1 0.5'])
        if cfg['key']:
            key = cfg['key']
            tl.append(f'execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{{bm:"{key}"}}] run return run function bm:p2/{d}/altar_nokey')
            fn(f'p2/{d}/altar_nokey', [title('@s', 'actionbar', T(f'Kneel with the {G.ITEMS[key]["name"]} in your hand.', 'gold')),
                                       'playsound minecraft:block.note_block.bass block @s ~ ~ ~ 1 0.7'])
            tl.append('item modify entity @s weapon.mainhand bm:p2/consume_one')
        tl.append(f'execute as {ar_sel} at @s run function bm:p2/{d}/start')
        fn(f'p2/{d}/altar', tl)
        fast.append(f'execute as @e[type=minecraft:marker,tag=bm.altar,tag=bm.d_{d}] at @s as @a[distance=..2.5,scores={{bm.sneak=1..}},gamemode=!spectator] at @s run function bm:p2/{d}/altar')
        from p2.kit import SHRINE
        part = SHRINE[d][5] if d in SHRINE else 'minecraft:soul_fire_flame'
        fast.append(f'execute as @e[type=minecraft:marker,tag=bm.altar,tag=bm.d_{d}] at @s if entity @a[distance=..20] run particle {part} ~ ~0.4 ~ 1.3 0.5 1.3 0 3')
        # ---- start / intro
        H = Bd.meta.get('arena_h', 12)
        fn(f'p2/{d}/ina', [f'tag @a[distance=..{ar + 60}] remove bm.ina_{d}'] + [
            f'execute as @e[type=minecraft:marker,tag=bm.aprobe,tag=bm.aps{sq},tag=bm.d_{d},distance=..{ar + 40}] at @s positioned ~-{sq / 2} ~-1.5 ~-{sq / 2} '
            f'run tag @a[dx={sq - 1},dy={H + 1},dz={sq - 1},gamemode=!spectator] add bm.ina_{d}' for sq in Bd.meta.get('probe_sizes', [])])
        fn(f'p2/{d}/start', ['scoreboard players set @s bm.bs 1', 'scoreboard players set @s bm.bt 0', 'scoreboard players set @s bm.ba 0',
                             f'execute as @e[type=minecraft:marker,tag=bm.adoor,tag=bm.d_{d},distance=..{ar + 20}] at @s run function bm:p2/{d}/adoor_close',
                             f'function bm:p2/{d}/ina',
                             f'tag @a[tag=bm.ina_{d},distance=..{ar + 40}] add bm.f_{d}'])
        length, events = INTRO[d]
        it = ['scoreboard players add @s bm.bt 1']
        for t, lines in sorted(events.items()):
            for ln in lines:
                it.append(f'execute if score @s bm.bt matches {t} run ' + ln.replace('{A}', A))
        it.append(f'execute if score @s bm.bt matches {length}.. run function bm:p2/{d}/fight_begin')
        fn(f'p2/{d}/intro', it)
        fn(f'p2/{d}/fight_begin', ['scoreboard players set @s bm.bs 2', 'scoreboard players set @s bm.bt 0',
                                   f'execute as @e[tag=bm.newboss,distance=..40] run function bm:p2/boss/init_scores',
                                   f'bossbar set bm:boss_{d} max {dict(brood=360, frost=320, tide=420, hex=300, keep=500, hollow=700, lucky=260)[d]}',
                                   f'bossbar set bm:boss_{d} visible true'])
        # ---- fight loop (every second)
        boss = f'@e[tag=bm.boss_{d},distance=..{ar + 28}]'
        leash = (f'execute positioned ~ ~12 ~ as @e[tag=bm.boss_{d},distance=28..70] run tp @s {ar_sel.replace("distance=..64", "distance=..80")}' if d == 'hollow'
                 else f'execute as @e[tag=bm.boss_{d},distance={ar + 5}..{ar + 40}] run tp @s {ar_sel.replace("distance=..64", f"distance=..{ar + 48}")}')
        fn(f'p2/{d}/fight', [
            f'function bm:p2/{d}/ina',
            f'bossbar set bm:boss_{d} players @a[distance=..{ar + 10}]',
            f'execute store result bossbar bm:boss_{d} value run data get entity @e[tag=bm.boss_{d},distance=..{ar + 28},limit=1] Health',
            f'execute as {boss} at @s run function bm:p2/{d}/boss_tick',
            leash,
            f'execute store result score #pl bm.rng if entity @a[tag=bm.ina_{d},distance=..{ar + 40},gamemode=!spectator]',
            'execute if score #pl bm.rng matches 0 run scoreboard players add @s bm.ba 1',
            'execute if score #pl bm.rng matches 1.. run scoreboard players set @s bm.ba 0',
            f'execute if score @s bm.ba matches 30.. run return run function bm:p2/{d}/abandon',
            f'execute unless entity {boss} if score #pl bm.rng matches 1.. run function bm:p2/{d}/on_boss_gone'])
        if d != 'hollow':
            fn(f'p2/{d}/on_boss_gone', [f'function bm:p2/{d}/victory'])
        # ---- victory / aftermath / abandon
        fn(f'p2/{d}/victory', ['scoreboard players set @s bm.bs 3', 'scoreboard players set @s bm.bt 0',
                               f'bossbar set bm:boss_{d} visible false',
                               f'execute as @e[tag=bm.minion_{d},distance=..{ar + 40}] at @s run function bm:p2/util/vanish',
                               f'execute as @e[type=minecraft:marker,tag=bm.adoor,tag=bm.d_{d},distance=..{ar + 20}] at @s run function bm:p2/{d}/adoor_open',
                               f'execute as @e[type=minecraft:marker,tag=bm.xdoor,tag=bm.d_{d},distance=..{r2}] at @s run function bm:p2/{d}/xdoor_open',
                               f'title {A} times 10 70 20',
                               title(A, 'subtitle', T('The way out has opened.', 'gray', italic=True)),
                               title(A, 'title', T(f'{cfg["boss"]} has fallen', cfg['color'], bold=True)),
                               # 2.13: everyone in the arena when the boss falls is a victor too (not only those tagged as the fight began)
                               f'function bm:p2/{d}/ina', f'tag @a[tag=bm.ina_{d},distance=..{ar + 40}] add bm.f_{d}',
                               f'tag @a[distance=..{ar + 2},gamemode=!spectator] add bm.f_{d}',
                               f'execute as @a[tag=bm.f_{d}] run function bm:p2/{d}/credit',
                               f'tag @a remove bm.f_{d}',
                               f'execute as @e[type=minecraft:marker,tag=bm.dg,tag=bm.d_{d},distance=..{r2},sort=nearest,limit=1] at @s run function bm:p2/{d}/rearm'])
        fn(f'p2/{d}/after', ['scoreboard players add @s bm.bt 1',
                             f'execute if score @s bm.bt matches 2 as {A} at @s run playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1',
                             f'execute if score @s bm.bt matches 2 run particle minecraft:totem_of_undying ~ ~2 ~ 3 2 3 0.3 150',
                             'execute if score @s bm.bt matches 60.. run scoreboard players set @s bm.bs 0'])
        refund = [f'execute at @e[type=minecraft:marker,tag=bm.altar,tag=bm.d_{d},distance=..{r2},sort=nearest,limit=1] run loot spawn ~ ~1 ~ loot bm:items/{cfg["key"]}'] if cfg['key'] else []
        fn(f'p2/{d}/abandon', [f'execute as {boss} run tp @s ~ -400 ~', f'execute as @e[tag=bm.minion_{d},distance=..{ar + 40}] run tp @s ~ -400 ~',
                               f'bossbar set bm:boss_{d} visible false', 'scoreboard players set @s bm.bs 0', 'scoreboard players set @s bm.ba 0',
                               'scoreboard players set @s bm.at2 0',
                               f'execute as @e[type=minecraft:marker,tag=bm.adoor,tag=bm.d_{d},distance=..{ar + 20}] at @s run function bm:p2/{d}/adoor_open',
                               f'tag @a remove bm.f_{d}'] + refund + [
                               tellraw(f'@a[distance=..{r2}]', PREFIX + [T(f'{cfg["boss"]} sinks back into the dark.' + (' Your key clatters back onto the altar.' if cfg['key'] else ''), 'gray')])])
        fn(f'p2/{d}/arena', [f'execute if score @s bm.bs matches 2 run function bm:p2/{d}/fight',
                             f'execute if score @s bm.bs matches 3 run function bm:p2/{d}/after'])
        second.append(f'execute as @e[type=minecraft:marker,tag=bm.arena,tag=bm.d_{d}] at @s run function bm:p2/{d}/arena')
        tick.append(f'execute as @e[type=minecraft:marker,tag=bm.arena,tag=bm.d_{d},scores={{bm.bs=1}}] at @s run function bm:p2/{d}/intro')
        # ---- credit (conquest + emblem + lore + next map + victor's key)
        nxt = cfg['next_map']
        first = [f'scoreboard players set @s bm.conq {idx}'] if idx else []
        if idx:
            first += [give(f'emblem_{d}'), give(f'lore_{d}')]
            if nxt: first.append(give(nxt))
            if d == 'keep': first.append(give('hollow_gate'))       # 2.48: the Gate replaces the Shard
            first += [f'title @s times 10 80 20', title('@s', 'subtitle', T(f'Conquest {idx} of 6', 'gray')),
                      title('@s', 'title', T('CONQUEST', cfg['color'], bold=True)),
                      tellraw('@s', PREFIX + [T('Conquest recorded: ', 'gray'), T(cfg['boss'], cfg['color'], bold=True),
                                              T('. ' + ('A new map is yours.' if nxt else ('A Hollow Gate is yours: set your five Emblems in it. The King is waiting.' if d == 'keep' else '')), 'gray')])]
            if d == 'hollow':
                first.append(tellraw('@a', PREFIX + [{'selector': '@s', 'color': 'gold'}, T(' has defeated ', 'gray'),
                                                     T('THE HOLLOW KING', '#e5e4e2', bold=True), T('!', 'gray')]))
        common = [give(cfg['bkey'])]
        if idx:
            # branch on the record as it was BEFORE this victory
            fn(f'p2/{d}/credit', ['scoreboard players operation #c bm.rng = @s bm.conq',
                                  f'execute if score #c bm.rng matches {idx - 1} run function bm:p2/{d}/credit_first',
                                  f'execute if score #c bm.rng matches {idx}.. run function bm:p2/{d}/credit_again',
                                  f'execute unless score #c bm.rng matches {idx - 1}.. run function bm:p2/{d}/credit_none'] + common)
            fn(f'p2/{d}/credit_first', first)
            fn(f'p2/{d}/credit_again', [tellraw('@s', PREFIX + [T(f'Victory! ({cfg["boss"]} was already on your record.)', 'gray')])])
            fn(f'p2/{d}/credit_none', [tellraw('@s', PREFIX + [T('Victory - but your conquest record is incomplete', 'gray'),
                                                               T(f' (defeat {D[prev]["boss"] if prev else "the earlier bosses"} first)', 'red'), T('. No emblem this time.', 'gray')])])
        else:
            fn(f'p2/{d}/credit', [f'execute unless entity @s[tag=bm.lore_{d}] run ' + give(f'lore_{d}'), f'tag @s add bm.lore_{d}'] + common)

    fn('p2/boss/init_scores', ['scoreboard players set @s bm.at 0', 'scoreboard players set @s bm.at2 0', 'scoreboard players set @s bm.life 0',
                               'tag @s remove bm.newboss', 'execute if entity @s[type=!minecraft:chicken] run team join bm.blood @s'])
    # loot tables for bosses
    return dict(tick=tick, fast=fast, second=second, load=load)

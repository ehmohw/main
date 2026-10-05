"""Phase 1.11: the Bloodforge Sigil's blood price, a grappling hook, new scratch-card prizes (prime meat, tools,
weapons; rarer Medallions/Trophies), more prime animals, and animation for the Frog with Mustache and the rats.

Animation: item models can't bend, so each figure has several 3D POSES (frog: sit, breathe, blink, crouch, leap; rats:
sniff, ears, tail) chosen through the item's custom_model_data string (the resource pack's item definitions are
`select` models on it). Poses are swapped like flip-book frames and the display's transformation is interpolated for
bobbing / breathing (y only, so it is the same whatever way the figure faces).
Importing registers the items; generate(G) runs after phase20.generate."""
from nbt import snbt, B, F, Int, D
from items import item, gear, ench, attr, weapon_attrs, T, TOTEM

# ===================================================================== ITEMS
item('grappling_hook', 'minecraft:carrot_on_a_stick', 'Grappling Hook', 'gray',
     ['Right-click a block up to 32 blocks away', 'to reel in and hang there - walls, ceilings.', 'Right-click again (or sneak) to let go.', ("Won't bite in dungeons.", 'dark_gray')],
     model='bm:grappling_hook', stack=1, cat='builder', price=('token', 8))
PAXEL_TOOL = {'rules': [{'blocks': '#minecraft:incorrect_for_diamond_tool', 'correct_for_drops': False},
                        {'blocks': '#minecraft:mineable/pickaxe', 'speed': 9.0, 'correct_for_drops': True},
                        {'blocks': '#minecraft:mineable/shovel', 'speed': 9.0, 'correct_for_drops': True},
                        {'blocks': '#minecraft:mineable/axe', 'speed': 9.0, 'correct_for_drops': True}],
              'default_mining_speed': 1.0, 'damage_per_block': 1}
gear('prospector_paxel', 'diamond_pickaxe', "Prospector's Paxel", 'aqua',
     ['Pickaxe, shovel and axe in one.', ('Mines stone, dirt and wood at full speed.', 'blue'), ('Scratch-card prize.', 'dark_gray')],
     ench(efficiency=5, unbreaking=3), 2, model='bm:prospector_paxel', extra={'minecraft:tool': PAXEL_TOOL})
gear('snake_eyes', 'diamond_sword', 'Snake Eyes', '#c0392b',
     ['A gambler\'s dagger. Quick, quiet, lucky.', ('Faster swings, +2 Luck while held', 'blue'), ('Scratch-card prize.', 'dark_gray')],
     ench(sharpness=5, looting=4, unbreaking=3), 2,
     attrs=weapon_attrs('diamond_sword', -1, [attr('attack_speed', 0.8, 'mainhand'), attr('luck', 2, 'mainhand')]),
     model='minecraft:iron_sword')
gear('high_roller', 'crossbow', 'High Roller', '#ffb300',
     ['Bet everything on one shot. Then two more.', ('Multishot AND Piercing', 'blue'), ('Scratch-card prize.', 'dark_gray')],
     ench(quick_charge=3, multishot=1, piercing=4, unbreaking=3), 2)

MEATS = ['prime_beef', 'prime_pork', 'prime_mutton', 'prime_chicken', 'prime_rabbit']
FROG_POSES = [  # name, id, model pose, bob (y)
    ('sit', 1, 'sit', 0.0), ('breathe', 2, 'breathe', 0.0), ('blink', 3, 'blink', 0.0), ('crouch', 4, 'crouch', -0.04),
    ('leap', 5, 'leap', 0.14), ('leapr', 6, 'leap', 0.24), ('air', 7, 'leap', 0.05)]
FROG_BASE_Y, WEAP_BASE = 0.4 - 0.85, (0.42, 0.42 - 0.85, -0.05)


def extend_offers(O, offer):
    from items import PRICES
    O['outfitter'].append(offer(PRICES['grappling_hook'], ('grappling_hook', 1)))


def generate(G):
    fn, wjson, title, tellraw, give = G.fn, G.wjson, G.title, G.tellraw, G.give
    PREFIX = G.PREFIX
    tick, fast, second = [], [], []
    G.FUNCS['load'][0:0] = ['scoreboard objectives add bm.bdebt dummy', 'scoreboard objectives add bm.bdok dummy',
                            'scoreboard objectives add bm.grap minecraft.used:minecraft.carrot_on_a_stick',
                            'scoreboard objectives add bm.gcd dummy', 'scoreboard objectives add bm.gpt dummy', 'scoreboard objectives add bm.pid dummy',
                            'scoreboard objectives add bm.fa dummy', 'scoreboard objectives add bm.fp dummy', 'scoreboard objectives add bm.ra dummy',
                            'scoreboard objectives add bm.rb dummy', 'scoreboard objectives add bm.rs dummy',
                            'scoreboard players set #2 bm.rng 2', 'scoreboard players set #4 bm.rng 4', 'scoreboard players set #100 bm.rng 100']

    # ================================================================ Bloodforge Sigil: the blood price (one heart, forever)
    sig = G.FUNCS['blood/sigil']
    k = sig.index('item modify entity @s weapon.offhand bm:unbreakable')
    # 1.12: only under a Blood Moon, in the Overworld; never below one heart (max health 2)
    sig[k:k] = ['execute unless score #active bm.bm matches 1 run return run function bm:p21/sigil_moon',
                'execute unless dimension minecraft:overworld run return run function bm:p21/sigil_moon',
                'execute store result score @s bm.mh run attribute @s minecraft:max_health get',
                'execute if score @s bm.mh matches ..3 run return run function bm:p21/sigil_refuse']
    sig[k + 5:k + 5] = ['scoreboard players add @s bm.bdebt 1', 'function bm:p21/debt_apply', 'playsound minecraft:entity.player.hurt player @s ~ ~ ~ 1 0.7',
                        'particle minecraft:damage_indicator ~ ~1.2 ~ 0.3 0.3 0.3 0.1 8']
    for i, l in enumerate(sig):
        if 'Bloodforged! Your item will never break.' in l:
            sig[i] = title('@s', 'actionbar', T('Bloodforged. The sigil drank one of your hearts - forever.', 'dark_red'))
    fn('p21/sigil_refuse', [give('bloodforge_sigil'), title('@s', 'actionbar', T('Your heart has nothing left to give. (Refunded)', 'dark_red'))])
    fn('p21/sigil_moon', [give('bloodforge_sigil'), title('@s', 'actionbar', T('The sigil sleeps. It only wakes under a Blood Moon, in the Overworld. (Refunded)', 'red'))])
    fn('p21/debt_apply', ['attribute @s minecraft:max_health modifier remove bm:blood_price',
                          'execute store result storage bm:tmp bd.amt int -2 run scoreboard players get @s bm.bdebt',
                          'function bm:p21/debt_set with storage bm:tmp bd'])
    fn('p21/debt_set', ['$attribute @s minecraft:max_health modifier add bm:blood_price $(amt) add_value'])
    second += ['execute as @a[scores={bm.bdebt=1..}] store success score @s bm.bdok run attribute @s minecraft:max_health modifier value get bm:blood_price',
               'execute as @a[scores={bm.bdebt=1..,bm.bdok=0}] run function bm:p21/debt_apply']

    # ================================================================ scratch cards (1.11 prize table, per 1000)
    G.FUNCS['lucky/reveal'] = [
        'scoreboard players reset @s bm.sct',
        'execute store result score @s bm.rng run random value 1..1000',
        'execute if score @s bm.rng matches 1..120 run return run function bm:lucky/win_nothing',
        'execute if score @s bm.rng matches 121..400 run return run function bm:lucky/win_tokens',
        'execute if score @s bm.rng matches 401..520 run return run function bm:lucky/win_lucky',
        'execute if score @s bm.rng matches 521..680 run return run function bm:lucky/win_meat',
        'execute if score @s bm.rng matches 681..790 run return run function bm:lucky/win_goodie',
        'execute if score @s bm.rng matches 791..880 run return run function bm:lucky/win_gear',
        'execute if score @s bm.rng matches 881..930 run return run function bm:lucky/win_hook',
        'execute if score @s bm.rng matches 931..960 run return run function bm:lucky/win_medallion',
        'execute if score @s bm.rng matches 961..976 run return run function bm:lucky/win_paxel',
        'execute if score @s bm.rng matches 977..988 run return run function bm:lucky/win_snake',
        'execute if score @s bm.rng matches 989..994 run return run function bm:lucky/win_roller',
        'execute if score @s bm.rng matches 995..996 run return run function bm:lucky/win_heart',
        'execute if score @s bm.rng matches 997..998 run return run function bm:lucky/win_trophy',
        'function bm:lucky/win_lucky7']

    def win(name, rewards, msg, color, sound='minecraft:block.note_block.pling', pitch=1.6, shout=None):
        lines = rewards + ['title @s times 5 40 10', title('@s', 'title', T('', 'white')), title('@s', 'subtitle', T(msg, color)),
                           f'playsound {sound} player @s ~ ~ ~ 1 {pitch}', 'particle minecraft:wax_on ~ ~1.2 ~ 0.4 0.5 0.4 0 12']
        if shout: lines.append(tellraw('@a', PREFIX + [{'selector': '@s', 'color': 'yellow'}, T(' scratched ', 'gray'), T(shout, color, bold=True), T('!', 'gray')]))
        fn(f'lucky/{name}', lines)

    def pick(name, iids, n=1):
        fn(f'lucky/{name}', [f'execute store result score @s bm.rng run random value 1..{len(iids)}'] +
           [f'execute if score @s bm.rng matches {i} run {give(iid, n)}' for i, iid in enumerate(iids, 1)])
    pick('pick_meat', MEATS, 2)
    pick('pick_goodie', ['vial_clear', 'vial_rain', 'aged_cheddar', 'sanguine_tonic'])
    pick('pick_gear', ['kokiri_sword', 'cranky_pick', 'fairy_bow', 'hammer_bro_hatchet'])
    win('win_meat', ['function bm:lucky/pick_meat'], 'Winner! A pair of prime cuts!', 'gold', 'minecraft:entity.player.burp', 1.0)
    win('win_goodie', ['function bm:lucky/pick_goodie'], 'Winner! Something from the back shelf!', 'aqua', 'minecraft:entity.item.pickup', 1.2)
    win('win_gear', ['function bm:lucky/pick_gear'], 'Winner! A piece of Black Market gear!', 'green', 'minecraft:item.armor.equip_iron', 1.0)
    win('win_hook', [give('grappling_hook')], 'Winner! A Grappling Hook!', 'green', 'minecraft:item.crossbow.loading_end', 1.0)
    win('win_paxel', [give('prospector_paxel')], "RARE! A Prospector's Paxel!", 'aqua', 'minecraft:block.amethyst_block.chime', 0.8, "a Prospector's Paxel")
    win('win_snake', [give('snake_eyes')], 'RARE! Snake Eyes!', '#c0392b', 'minecraft:block.amethyst_block.chime', 0.8, 'Snake Eyes')
    win('win_roller', [give('high_roller')], 'RARE! The High Roller!', '#ffb300', 'minecraft:block.bell.use', 0.8, 'the High Roller')
    win('win_heart', [give('heartstone')], 'RARE! A Heartstone!', 'red', 'minecraft:block.respawn_anchor.charge', 1.0, 'a Heartstone')

    # ================================================================ more prime animals (1 in 25, was 1 in 100)
    for name, lines in G.FUNCS.items():
        if name.startswith('mobs/init/') and any('function bm:mobs/prime/' in l for l in lines):
            for i, l in enumerate(lines):
                if l == 'execute store result score #r bm.rng run random value 1..100':
                    lines[i] = 'execute store result score #r bm.rng run random value 1..25'

    # ================================================================ grappling hook
    wjson('bm/tags/block/grap_pass.json', {'values': ['#minecraft:replaceable']})
    hook = '*[minecraft:custom_data~{bm:"grappling_hook"}]'
    # 1.12.1 rework: no more per-tick player teleports (they fought the client and shook the camera). The hook now
    # reels you in on an invisible, weightless armour stand that you ride: the game moves it with Motion, so the
    # client interpolates smoothly and your view is untouched. Where the hook bites - a wall, a ceiling - the
    # carrier stops and you HANG there. Let go with right-click or sneak (the vanilla dismount); only then do you
    # get Slow Falling.
    car = snbt({'Tags': ['bm.gcar', 'bm.gnewcar', 'bm.seen'], 'Invisible': B(1), 'Small': B(1), 'NoBasePlate': B(1), 'Invulnerable': B(1),
                'Silent': B(1), 'DisabledSlots': Int(4144959),
                'attributes': [{'id': 'minecraft:gravity', 'base': D(0.0)}]})
    tick += ['execute as @a[scores={bm.grap=1..}] at @s run function bm:p21/grap/use',
             'execute as @a[tag=bm.grappling] at @s run function bm:p21/grap/pull',
             'execute as @e[type=minecraft:armor_stand,tag=bm.gcar] run function bm:p21/grap/orphan',
             'scoreboard players remove @a[scores={bm.gcd=1..}] bm.gcd 1']
    fn('p21/pid', ['scoreboard players add #next bm.pid 1', 'scoreboard players operation @s bm.pid = #next bm.pid'])
    fn('p21/grap/use', [
        'scoreboard players reset @s bm.grap',
        f'execute unless items entity @s weapon.mainhand {hook} unless items entity @s weapon.offhand {hook} run return 0',
        'execute if entity @s[tag=bm.grappling] run return run function bm:p21/grap/release',
        'execute if score @s bm.gcd matches 1.. run return 0',
        'execute if entity @s[tag=bm.adv] run return run ' + title('@s', 'actionbar', T("The hook won't bite in here.", 'gray')),
        'execute if predicate bm:p21/riding run return run ' + title('@s', 'actionbar', T("Get down from your mount first.", 'gray')),
        'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
        'scoreboard players set #gr bm.rng 64', 'scoreboard players set #ghit bm.rng 0',
        'execute anchored eyes positioned ^ ^ ^ run function bm:p21/grap/ray',
        'playsound minecraft:item.crossbow.shoot player @a[distance=..16] ~ ~ ~ 1 1.4',
        'execute if score #ghit bm.rng matches 0 run return run ' + title('@s', 'actionbar', T('Out of reach.', 'gray')),
        f'summon minecraft:armor_stand ~ ~ ~ {car}',
        'scoreboard players operation @e[type=minecraft:armor_stand,tag=bm.gnewcar] bm.pid = @s bm.pid',
        'ride @s mount @e[type=minecraft:armor_stand,tag=bm.gnewcar,limit=1]',
        'tag @e[type=minecraft:armor_stand,tag=bm.gnewcar] remove bm.gnewcar',
        'tag @s add bm.grappling', 'scoreboard players set @s bm.gpt 0', 'scoreboard players set @s bm.gcd 10',
        'playsound minecraft:block.chain.place player @a[distance=..16] ~ ~ ~ 1 0.8'])
    fn('p21/grap/ray', ['execute unless block ~ ~ ~ #bm:grap_pass run return run function bm:p21/grap/hit',
                        'scoreboard players remove #gr bm.rng 1',
                        'execute if score #gr bm.rng matches 1.. positioned ^ ^ ^0.5 run function bm:p21/grap/ray'])
    # the anchor sits half a block out from the face that was hit; the carrier's goal is set so your EYES end up at the
    # anchor (rider eyes are ~2.1 above a small stand), then nudged up until your body isn't inside a floor
    fn('p21/grap/hit', ['execute positioned ^ ^ ^-0.5 run summon minecraft:marker ~ ~ ~ {Tags:["bm.ganchor","bm.gnew"]}',
                        'execute positioned ^ ^ ^-0.5 run summon minecraft:marker ~ ~-2.1 ~ {Tags:["bm.gtgt","bm.gnew"]}',
                        'scoreboard players operation @e[type=minecraft:marker,tag=bm.gnew] bm.pid = @s bm.pid',
                        'execute as @e[type=minecraft:marker,tag=bm.gnew,tag=bm.gtgt] at @s run function bm:p21/grap/lift',
                        'tag @e[type=minecraft:marker,tag=bm.gnew] remove bm.gnew', 'scoreboard players set #ghit bm.rng 1',
                        'particle minecraft:crit ~ ~ ~ 0.1 0.1 0.1 0.2 8'])
    fn('p21/grap/lift', ['scoreboard players set #lift bm.rng 0'] + [
        f'execute if score #lift bm.rng matches 0 positioned ~ ~0.6 ~ unless block ~ ~{dy} ~ #bm:grap_pass run scoreboard players set #lift bm.rng 1'
        for dy in (0, 1)] + [
        'execute if score #lift bm.rng matches 1 run tp @s ~ ~1 ~',
        'scoreboard players add #lifts bm.rng 1',
        'execute if score #lift bm.rng matches 1 if score #lifts bm.rng matches ..3 at @s run function bm:p21/grap/lift',
        'scoreboard players set #lifts bm.rng 0'])
    fn('p21/grap/pull', [
        'scoreboard players add @s bm.gpt 1',
        'execute if entity @s[tag=bm.adv] run return run function bm:p21/grap/release',
        'tag @e[tag=bm.gmine] remove bm.gmine',
        'scoreboard players operation #me bm.pid = @s bm.pid',
        'execute as @e[type=minecraft:marker,tag=bm.ganchor] if score @s bm.pid = #me bm.pid run tag @s add bm.gmine',
        'execute as @e[type=minecraft:marker,tag=bm.gtgt] if score @s bm.pid = #me bm.pid run tag @s add bm.gmine',
        'execute on vehicle if entity @s[tag=bm.gcar] run tag @s add bm.gmine',
        # sneaking dismounts (vanilla) - that IS letting go
        'execute unless entity @e[type=minecraft:armor_stand,tag=bm.gmine] run return run function bm:p21/grap/release',
        'execute unless entity @e[type=minecraft:marker,tag=bm.gtgt,tag=bm.gmine] run return run function bm:p21/grap/release',
        'scoreboard players operation #gpt bm.rng = @s bm.gpt',
        'execute as @e[type=minecraft:armor_stand,tag=bm.gmine,limit=1] at @s run function bm:p21/grap/move',
        'scoreboard players set #rp bm.rng 40',
        'execute anchored eyes positioned ^ ^ ^ facing entity @e[type=minecraft:marker,tag=bm.ganchor,tag=bm.gmine,limit=1] feet run function bm:p21/grap/rope'])
    goal = '@e[type=minecraft:marker,tag=bm.gtgt,tag=bm.gmine,limit=1'
    fn('p21/grap/move', [
        f'execute if entity {goal},distance=..0.12] run return run data modify entity @s Motion set value [0.0d,0.0d,0.0d]',
        'execute if score #gpt bm.rng matches 100.. run return run data modify entity @s Motion set value [0.0d,0.0d,0.0d]',
        f'execute if entity {goal},distance=..0.9] positioned as {goal}] run return run function bm:p21/grap/vec',
        f'execute facing entity {goal}] feet positioned ^ ^ ^0.85 run function bm:p21/grap/vec'])
    # Motion = (here - carrier), read through a throwaway marker at "here"
    fn('p21/grap/vec', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.gvec"]}'] +
       [f'execute store result score #v{a} bm.rng run data get entity @e[type=minecraft:marker,tag=bm.gvec,limit=1] Pos[{i}] 1000' for i, a in enumerate('xyz')] +
       ['kill @e[type=minecraft:marker,tag=bm.gvec]'] +
       [f'execute store result score #c{a} bm.rng run data get entity @s Pos[{i}] 1000' for i, a in enumerate('xyz')] +
       [f'scoreboard players operation #v{a} bm.rng -= #c{a} bm.rng' for a in 'xyz'] +
       [f'execute store result entity @s Motion[{i}] double 0.001 run scoreboard players get #v{a} bm.rng' for i, a in enumerate('xyz')])
    fn('p21/grap/rope', ['particle minecraft:dust{color:[0.42,0.33,0.22],scale:0.6} ~ ~-0.3 ~ 0 0 0 0 1',
                         'scoreboard players remove #rp bm.rng 1',
                         'execute if entity @e[type=minecraft:marker,tag=bm.ganchor,tag=bm.gmine,distance=..1] run return 0',
                         'execute if score #rp bm.rng matches 1.. positioned ^ ^ ^1 run function bm:p21/grap/rope'])
    fn('p21/grap/release', ['tag @s remove bm.grappling', 'scoreboard players operation #me bm.pid = @s bm.pid',
                            'execute on vehicle if entity @s[tag=bm.gcar] run tag @s add bm.gdrop',
                            'ride @s dismount',
                            'kill @e[type=minecraft:armor_stand,tag=bm.gdrop]',
                            'execute as @e[type=minecraft:armor_stand,tag=bm.gcar] if score @s bm.pid = #me bm.pid run kill @s',
                            'execute as @e[type=minecraft:marker,tag=bm.ganchor] if score @s bm.pid = #me bm.pid run kill @s',
                            'execute as @e[type=minecraft:marker,tag=bm.gtgt] if score @s bm.pid = #me bm.pid run kill @s',
                            'scoreboard players set @s bm.gcd 10',
                            'playsound minecraft:block.chain.break player @a[distance=..16] ~ ~ ~ 0.8 1.2'])
    # a carrier nobody is riding (logged out, died) is cleared
    fn('p21/grap/orphan', ['scoreboard players set #p bm.rng 0', 'execute on passengers run scoreboard players set #p bm.rng 1',
                           'execute if score #p bm.rng matches 0 run kill @s'])
    wjson('bm/predicate/p21/riding.json', {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:vehicle': {}}})

    # ================================================================ animation: the Frog with Mustache (follower)
    tick.append('execute as @e[type=minecraft:wolf,tag=bm.frogpet] at @s if entity @a[distance=..48] run function bm:p21/frog/anim')
    wjson('bm/predicate/p21/airborne.json', {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:flags': {'is_on_ground': False}}})
    wjson('bm/predicate/p21/walking.json', {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:movement': {'horizontal_speed': {'min': 0.8}}}})
    wjson('bm/predicate/p21/running.json', {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:movement': {'horizontal_speed': {'min': 4.0}}}})
    fn('p21/frog/anim', ['scoreboard players add @s bm.fa 1', 'execute if score @s bm.fa matches 48.. run scoreboard players set @s bm.fa 0',
                         'scoreboard players operation #f bm.rng = @s bm.fa', 'scoreboard players operation #f bm.rng %= #2 bm.rng',
                         'execute unless score #f bm.rng matches 0 run return 0',
                         'execute if predicate bm:p21/airborne run return run function bm:p21/frog/pose_air',
                         'execute if predicate bm:p21/running run return run function bm:p21/frog/run',
                         'execute if predicate bm:p21/walking run return run function bm:p21/frog/walk',
                         'function bm:p21/frog/idle'])
    fn('p21/frog/walk', ['scoreboard players operation #w bm.rng = @s bm.fa', 'scoreboard players operation #w bm.rng /= #2 bm.rng',
                         'scoreboard players operation #w bm.rng %= #4 bm.rng',
                         'execute if score #w bm.rng matches 0 run return run function bm:p21/frog/pose_sit',
                         'execute if score #w bm.rng matches 2 run return run function bm:p21/frog/pose_leap',
                         'function bm:p21/frog/pose_crouch'])
    fn('p21/frog/run', ['scoreboard players operation #w bm.rng = @s bm.fa', 'scoreboard players operation #w bm.rng /= #2 bm.rng',
                        'scoreboard players operation #w bm.rng %= #2 bm.rng',
                        'execute if score #w bm.rng matches 0 run return run function bm:p21/frog/pose_crouch',
                        'function bm:p21/frog/pose_leapr'])
    fn('p21/frog/idle', ['execute if score @s bm.fa matches 0..11 run return run function bm:p21/frog/pose_breathe',
                         'execute if score @s bm.fa matches 30..31 run return run function bm:p21/frog/pose_blink',
                         'function bm:p21/frog/pose_sit'])
    for name, pid, model, bob in FROG_POSES:
        fy, (wx, wy, wz) = round(FROG_BASE_Y + bob, 3), WEAP_BASE
        fn(f'p21/frog/pose_{name}', [
            f'execute if score @s bm.fp matches {pid} run return 0', f'scoreboard players set @s bm.fp {pid}',
            f'execute on passengers if entity @s[tag=bm.fp_body] run data modify entity @s item.components."minecraft:custom_model_data".strings[0] set value "{model}"',
            f'execute on passengers if entity @s[tag=bm.fp_body] run data merge entity @s {{start_interpolation:0,interpolation_duration:2,transformation:{{translation:[0f,{fy}f,0f]}}}}',
            f'execute on passengers if entity @s[tag=bm.fp_weap] run data merge entity @s {{start_interpolation:0,interpolation_duration:2,transformation:{{translation:[{wx}f,{round(wy + bob, 3)}f,{wz}f]}}}}'])
    # 1.10 bodies/hut frogs used fixed models: switch them to the posable one (helm string set by the wolf's refresh)
    body_item = snbt({'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:frog', 'minecraft:custom_model_data': {'strings': ['sit', 'none']}}})
    hut_item = snbt({'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:frog', 'minecraft:custom_model_data': {'strings': ['sit', 'iron']}}})
    second += [f'execute as @e[type=minecraft:item_display,tag=bm.fp_body] unless items entity @s contents *[minecraft:item_model="bm:frog"] run data modify entity @s item set value {body_item}',
               'execute as @e[type=minecraft:wolf,tag=bm.frogpet,tag=!bm.f21] run function bm:p21/frog/migrate',
               f'execute as @e[type=minecraft:item_display,tag=bm.frog_hut] unless items entity @s contents *[minecraft:item_model="bm:frog"] run data modify entity @s item set value {hut_item}']
    fn('p21/frog/migrate', ['tag @s add bm.f21', 'tag @s add bm.fsel', 'function bm:p20/frog/refresh', 'tag @s remove bm.fsel'])
    # the hut frog just idles: breathes, blinks
    fast.append('execute as @e[type=minecraft:item_display,tag=bm.frog_hut] at @s if entity @a[distance=..24] run function bm:p21/frog/hut')
    fn('p21/frog/hut', ['execute store result score #h bm.rng run random value 1..12',
                        'execute if score #h bm.rng matches 1 run return run data modify entity @s item.components."minecraft:custom_model_data".strings[0] set value "blink"',
                        'execute if score #h bm.rng matches 2..4 run return run data modify entity @s item.components."minecraft:custom_model_data".strings[0] set value "breathe"',
                        'data modify entity @s item.components."minecraft:custom_model_data".strings[0] set value "sit"'])

    # ================================================================ animation: rats (idle: sniff, ear flick, tail swish, breathing)
    fast.append('execute as @e[type=minecraft:item_display,tag=bm.rat_sprite] at @s if entity @a[distance=..24] run function bm:p21/rat/anim')
    fn('p21/rat/anim', [
        'execute unless score @s bm.rs matches 1.. store result score @s bm.rs run data get entity @s transformation.scale[0] 1000',
        'scoreboard players add @s bm.rb 1', 'execute if score @s bm.rb matches 16.. run scoreboard players set @s bm.rb 0',
        'execute if score @s bm.rb matches 0 run function bm:p21/rat/breathe {k:103}',
        'execute if score @s bm.rb matches 8 run function bm:p21/rat/breathe {k:100}',
        'execute if score @s bm.ra matches 1.. run scoreboard players remove @s bm.ra 1',
        'execute if score @s bm.ra matches 0 run return run function bm:p21/rat/rest',
        'execute if score @s bm.ra matches 1.. run return 0',
        'execute store result score #h bm.rng run random value 1..24',
        'execute if score #h bm.rng matches 1 run return run function bm:p21/rat/pose {p:"sniff",t:3}',
        'execute if score #h bm.rng matches 2 run return run function bm:p21/rat/pose {p:"ears",t:2}',
        'execute if score #h bm.rng matches 3 run return run function bm:p21/rat/pose {p:"tail",t:4}'])
    fn('p21/rat/pose', ['$data modify entity @s item.components."minecraft:custom_model_data" set value {strings:["$(p)"]}',
                        '$scoreboard players set @s bm.ra $(t)'])
    fn('p21/rat/rest', ['data remove entity @s item.components."minecraft:custom_model_data"', 'scoreboard players set @s bm.ra -1'])
    fn('p21/rat/breathe', ['$scoreboard players set #k bm.rng $(k)',
                           'scoreboard players operation #sy bm.rng = @s bm.rs', 'scoreboard players operation #sy bm.rng *= #k bm.rng',
                           'scoreboard players operation #sy bm.rng /= #100 bm.rng',
                           'execute store result storage bm:tmp rb.sx float 0.001 run scoreboard players get @s bm.rs',
                           'execute store result storage bm:tmp rb.sy float 0.001 run scoreboard players get #sy bm.rng',
                           'execute store result storage bm:tmp rb.ty float 0.0005 run scoreboard players get #sy bm.rng',
                           'function bm:p21/rat/scale with storage bm:tmp rb'])
    fn('p21/rat/scale', ['$data merge entity @s {start_interpolation:0,interpolation_duration:38,transformation:{scale:[$(sx)f,$(sy)f,$(sx)f],translation:[0f,$(ty)f,0f]}}'])

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second

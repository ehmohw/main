"""2.4: Wilfrey, the Kind Lord - a hidden ally for those who felled the Hollow King.

His grave on Wilfrey's Rest (a pale islet beside the Hollow Throne, elytra only) gives Wilfrey's Locket. The locket
calls him; again to call him back; sneak + use to let him rest (gear returned). Like the Frog with Mustache he is an
invisible tamed wolf underneath (follows, fights, defends, teleports to you), carrying:
  - an invisible marker armour stand that WEARS his real gear (so you see the actual armour and weapon; empty slots
    show faint spectral leather), named "Wilfrey";
  - an interaction box over the stand (right-click him: hold a weapon/armour to swap it in, sneak + empty hand to take
    everything back, empty hand to make him hold position or follow);
  - an empty 'bag' display used as the swap slot (the frog's give/strip/drop functions are shared).
If he falls, his gear drops and the locket needs 30 minutes. Near you he lends a little Regeneration now and then."""
from nbt import snbt, B, F, Int, D as Dd
from items import T

GHOST = 'enchantment_glint_override=true,dyed_color=10475007'   # pale spectral blue leather
SLOTS = [('weapon.mainhand', None), ('armor.head', 'leather_helmet'), ('armor.chest', 'leather_chestplate'),
         ('armor.legs', 'leather_leggings'), ('armor.feet', 'leather_boots')]
TAGS = [('#bm:frog_weapon', 'weapon.mainhand'), ('#minecraft:head_armor', 'armor.head'), ('#minecraft:chest_armor', 'armor.chest'),
        ('#minecraft:leg_armor', 'armor.legs'), ('#minecraft:foot_armor', 'armor.feet')]


def generate(G):
    fn, title, tellraw, give = G.fn, G.title, G.tellraw, G.give
    PREFIX = G.PREFIX
    tick, fast, second = [], [], []
    ident = [F(0), F(0), F(0), F(1)]
    W = 'Wilfrey'
    sel = '@e[type=minecraft:wolf,tag=bm.fsel,limit=1,sort=nearest]'

    # ---------------- the grave
    # 2.6: the box covers the sarcophagus (x18-22, z16-19) and ends at the dais edge. Players who walk up to the tomb
    # stand OUTSIDE it - a click from inside an interaction box never registers (that was the 2.5 bug).
    box = {'Tags': ['bm.npc', 'bm.new', 'bm.wgrave_box', 'bm.wg3', 'bm.wg4'], 'width': F(5.6), 'height': F(2.4), 'response': B(1)}
    fn('npc/wil_grave', [f'summon minecraft:interaction ~ ~ ~ {snbt(box)}', 'tag @e[tag=bm.new,distance=..2] remove bm.new'])
    G.FUNCS['npc/spawn'][0:0] = ['execute if entity @s[tag=bm.npc.wil_grave] run function bm:npc/wil_grave']
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.wgrave_box] if data entity @s interaction at @s run function bm:p2/wil/grave_click')
    # worlds placed by 2.4/2.5: move the old box (centred in front of the tomb, on the dais) onto the sarcophagus
    fn('p2/wil/grave_box_fix', ['tp @s ~ ~1 ~-3.7', 'data merge entity @s[type=minecraft:interaction] {width:4.4f,height:2.2f}', 'tag @s add bm.wg3'])
    second.append('execute as @e[type=minecraft:interaction,tag=bm.wgrave_box,tag=!bm.wg3] at @s run function bm:p2/wil/grave_box_fix')
    # 2.9: a wider box that sticks out past the stone on every side (its faces used to sit flush with the sarcophagus,
    # and a tie between a block face and a box face goes to the block)
    second.append('execute as @e[type=minecraft:interaction,tag=bm.wgrave_box,tag=bm.wg3,tag=!bm.wg4] run function bm:p2/wil/grave_box_wide')
    fn('p2/wil/grave_box_wide', ['data merge entity @s[type=minecraft:interaction] {width:5.6f,height:2.4f}', 'tag @s add bm.wg4'])
    fast.append('execute as @e[type=minecraft:marker,tag=bm.wgfx] at @s if entity @a[distance=..40] run function bm:p2/wil/grave_fx')
    fn('p2/wil/grave_fx', ['particle minecraft:white_ash ~ ~4 ~ 9 3 9 0 6', 'particle minecraft:soul ~ ~ ~ 1.2 0.4 1.2 0.01 1',
                           'particle minecraft:soul ~ ~-1 ~ 1.5 0.2 1 0.01 1'])
    # 2.9: read the clicker (on target) BEFORE clearing the interaction - clearing it first made the tomb ignore every click
    fn('p2/wil/grave_click', ['execute on target at @s run function bm:p2/wil/grave', 'data remove entity @s interaction'])
    fn('p2/wil/grave', [
        'execute unless score @s bm.conq matches 6.. run return run ' + title('@s', 'actionbar', T('The grave is cold and quiet. (Only the Hollow King\'s conqueror can wake what sleeps here.)', 'gray', italic=True)),
        'execute if items entity @s container.* *[minecraft:custom_data~{bm:"wilfrey_locket"}] run return run ' + title('@s', 'actionbar', T("Wilfrey's locket is already with you.", 'gray')),
        'execute if items entity @s weapon.offhand *[minecraft:custom_data~{bm:"wilfrey_locket"}] run return run ' + title('@s', 'actionbar', T("Wilfrey's locket is already with you.", 'gray')),
        give('wilfrey_locket'),
        'title @s times 10 70 20', title('@s', 'subtitle', T('"You freed the Keep. Let me repay you, friend."', 'white', italic=True)),
        title('@s', 'title', T('Wilfrey stirs', '#f4f4f4', bold=True)),
        'playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 0.6', 'playsound minecraft:block.bell.resonate player @s ~ ~ ~ 0.6 1.2',
        'particle minecraft:end_rod ~ ~1 ~ 0.6 1 0.6 0.05 40'])

    # ---------------- the locket
    G.consume_adv('wilfrey_locket', 'bm:p2/wil/locket')
    back = ['execute unless items entity @s weapon.mainhand * run item replace entity @s weapon.mainhand with ' + G.item_arg('wilfrey_locket'),
            'execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"wilfrey_locket"}] run ' + give('wilfrey_locket')]
    fn('p2/wil/locket', ['advancement revoke @s only bm:consume/wilfrey_locket'] + back + [
        'execute unless score @s bm.conq matches 6.. run return run ' + title('@s', 'actionbar', T('The locket is cold.', 'gray')),
        'tag @s add bm.giver', 'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
        'execute as @e[type=minecraft:wolf,tag=bm.wilfrey] if function bm:p20/frog/is_givers run tag @s add bm.fsel',
        'execute if entity @e[type=minecraft:wolf,tag=bm.fsel] if predicate bm:p20/sneaking run function bm:p2/wil/dismiss',
        'execute if entity @e[type=minecraft:wolf,tag=bm.fsel] unless predicate bm:p20/sneaking run function bm:p2/wil/recall',
        'execute unless entity @e[type=minecraft:wolf,tag=bm.fsel] unless predicate bm:p20/sneaking run function bm:p2/wil/try_summon',
        'tag @e[tag=bm.fsel] remove bm.fsel', 'tag @e[tag=bm.fbag] remove bm.fbag', 'tag @s remove bm.giver'])
    fn('p2/wil/recall', [f'tp {sel} @s', 'particle minecraft:end_rod ~ ~1 ~ 0.4 0.8 0.4 0.03 20',
                         title('@s', 'actionbar', T('Wilfrey returns to your side.', 'white'))])
    fn('p2/wil/try_summon', [
        'execute if score @s bm.wlcd matches 1.. store result score #m bm.rng run scoreboard players get @s bm.wlcd',
        'execute if score @s bm.wlcd matches 1.. run scoreboard players operation #m bm.rng /= #60 bm.rng',
        'execute if score @s bm.wlcd matches 1.. run scoreboard players add #m bm.rng 1',
        'execute if score @s bm.wlcd matches 1.. run return run ' + title('@s', 'actionbar', [T("Wilfrey's spirit is still mending: about ", 'gray'),
                                                                                           {'score': {'name': '#m', 'objective': 'bm.rng'}, 'color': 'white'}, T(' min.', 'gray')]),
        'function bm:p2/wil/summon'])
    wolf = {'Tags': ['bm.wilfrey', 'bm.wnew', 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1),
            'CustomName': T('Wilfrey, the Kind Lord', '#f4f4f4', bold=True), 'CustomNameVisible': B(0), 'Health': F(80),
            'attributes': [{'id': 'minecraft:max_health', 'base': Dd(80)}, {'id': 'minecraft:attack_damage', 'base': Dd(7)},
                           {'id': 'minecraft:movement_speed', 'base': Dd(0.36)}, {'id': 'minecraft:follow_range', 'base': Dd(40)},
                           {'id': 'minecraft:armor', 'base': Dd(4)}, {'id': 'minecraft:step_height', 'base': Dd(1.0)}],
            'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0),
                                'show_icon': B(0), 'ambient': B(0)}],
            'drop_chances': {s: F(2.0) for s in ('mainhand', 'head', 'chest', 'legs', 'feet')}}
    # 2.10: his body is a wither skeleton knight (a frozen, invulnerable wither skeleton wearing his real gear) that is
    # moved onto the wolf every tick - it does not ride the wolf, because riders sit down. The click box follows too.
    body = {'Tags': ['bm.wil_body', 'bm.wnew'], 'NoAI': B(1), 'Invulnerable': B(1), 'Silent': B(1), 'PersistenceRequired': B(1),
            'NoGravity': B(1), 'CanPickUpLoot': B(0), 'CustomName': T('Wilfrey', '#f4f4f4', bold=True), 'CustomNameVisible': B(1),
            'drop_chances': {s_: F(0.0) for s_ in ('mainhand', 'offhand', 'head', 'chest', 'legs', 'feet')}}
    wbox = {'Tags': ['bm.wil_box', 'bm.wnew'], 'width': F(0.9), 'height': F(2.5), 'response': B(1)}
    bag = {'Tags': ['bm.wil_part', 'bm.wil_bag', 'bm.wnew'],
           'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0), F(0)], 'scale': [F(0)] * 3}}
    fn('p2/wil/summon', [
        f'summon minecraft:wolf ~ ~ ~ {snbt(wolf)}',
        'data modify entity @e[type=minecraft:wolf,tag=bm.wnew,limit=1,sort=nearest] Owner set from entity @s UUID',
        f'summon minecraft:item_display ~ ~ ~ {snbt(bag)}',
        'scoreboard players operation @e[tag=bm.wnew,distance=..2] bm.pid = @s bm.pid',
        'execute as @e[tag=bm.wil_part,tag=bm.wnew,distance=..2] run ride @s mount @e[type=minecraft:wolf,tag=bm.wnew,limit=1,sort=nearest]',
        'team join bm.wil @e[type=minecraft:wolf,tag=bm.wnew,limit=1,sort=nearest]',
        'execute as @e[type=minecraft:wolf,tag=bm.wnew,limit=1,sort=nearest] at @s run function bm:p2/wil/make_body',
        'tag @e[tag=bm.wnew,distance=..3] remove bm.wnew',
        'particle minecraft:soul ~ ~1 ~ 0.5 1 0.5 0.04 40', 'particle minecraft:white_ash ~ ~2 ~ 1 1 1 0 40',
        'playsound minecraft:block.bell.resonate neutral @a[distance=..20] ~ ~ ~ 1 0.9',
        'playsound minecraft:item.armor.equip_netherite neutral @a[distance=..20] ~ ~ ~ 1 0.8',
        'title @s times 10 60 15', title('@s', 'subtitle', T('"Lead on, friend. I will guard your back."', 'white', italic=True)),
        title('@s', 'title', T('Wilfrey rises', '#f4f4f4', bold=True)),
        tellraw('@s', PREFIX + [T('Wilfrey follows and fights for you. Right-click him holding a weapon or armour to equip it (he hands back what it replaces); ', 'white'),
                                T('empty-handed to make him hold or follow; sneak + right-click empty-handed to take everything back. ', 'gray'),
                                T('Sneak + use the locket to let him rest.', 'gray')])])
    # dismiss: gear back to you, then he fades (no death, no cooldown)
    fn('p2/wil/dismiss', [f'execute as {sel} on passengers if entity @s[tag=bm.wil_bag] run tag @s add bm.fbag',
                          'function bm:p20/frog/strip',
                          f'execute as {sel} at @s run function bm:p2/wil/fade',
                          title('@s', 'actionbar', T('Wilfrey bows, and fades until you call again.', 'white'))])
    fn('p2/wil/fade', ['particle minecraft:end_rod ~ ~1.5 ~ 0.4 0.9 0.4 0.04 40', 'execute on passengers run kill @s',
                       'scoreboard players operation #me bm.pid = @s bm.pid',
                       'execute as @e[type=minecraft:wither_skeleton,tag=bm.wil_body] if score @s bm.pid = #me bm.pid run tp @s ~ -500 ~',
                       'execute as @e[type=minecraft:wither_skeleton,tag=bm.wil_body] if score @s bm.pid = #me bm.pid run kill @s',
                       'execute as @e[type=minecraft:interaction,tag=bm.wil_box] if score @s bm.pid = #me bm.pid run kill @s',
                       'data remove entity @s Owner', 'tp @s ~ -500 ~', 'kill @s'])

    # ---------------- dressing the body from the wolf's real slots (bare bones where a slot is empty)
    fn('p2/wil/dress', [f'item replace entity @s {slot} from entity {sel} {slot}' for slot, _ in SLOTS])
    fn('p2/wil/refresh', ['scoreboard players operation #me bm.pid = @s bm.pid',
                          'execute as @e[type=minecraft:wither_skeleton,tag=bm.wil_body] if score @s bm.pid = #me bm.pid at @s run function bm:p2/wil/dress'])
    # (as the wolf) his body and click box - also rebuilds them for Wilfreys from 2.4-2.9, who wore an armour stand
    fn('p2/wil/make_body', ['execute on passengers if entity @s[type=minecraft:armor_stand] run kill @s',
                            'execute on passengers if entity @s[type=minecraft:interaction] run kill @s',
                            'scoreboard players operation #me bm.pid = @s bm.pid',
                            'execute as @e[type=minecraft:interaction,tag=bm.wil_box] if score @s bm.pid = #me bm.pid run kill @s',
                            f'summon minecraft:wither_skeleton ~ ~ ~ {snbt(body)}', f'summon minecraft:interaction ~ ~ ~ {snbt(wbox)}',
                            'scoreboard players operation @e[tag=bm.wnew,distance=..1] bm.pid = @s bm.pid',
                            'team join bm.wil @e[type=minecraft:wither_skeleton,tag=bm.wnew,distance=..1]', 'team join bm.wil @s',
                            'tag @e[tag=bm.wnew,distance=..1] remove bm.wnew',
                            'tag @s add bm.fsel', 'function bm:p2/wil/refresh', 'tag @s remove bm.fsel', 'scoreboard players set @s bm.wlg 0'])
    fn('p2/wil/has_body', ['scoreboard players operation #me bm.pid = @s bm.pid',
                           'execute as @e[type=minecraft:wither_skeleton,tag=bm.wil_body] if score @s bm.pid = #me bm.pid run return 1', 'return 0'])
    fn('p2/wil/has_wolf', ['scoreboard players operation #me bm.pid = @s bm.pid',
                           'execute as @e[type=minecraft:wolf,tag=bm.wilfrey] if score @s bm.pid = #me bm.pid run return 1', 'return 0'])
    fn('p2/wil/follow', ['scoreboard players operation #me bm.pid = @s bm.pid',
                         'execute as @e[type=minecraft:wither_skeleton,tag=bm.wil_body] if score @s bm.pid = #me bm.pid run tp @s ~ ~ ~ ~ 0',
                         'execute as @e[type=minecraft:interaction,tag=bm.wil_box] if score @s bm.pid = #me bm.pid run tp @s ~ ~ ~'])
    G.FUNCS['load'][-1:-1] = ['team add bm.wil', 'team modify bm.wil collisionRule never']
    G.FUNCS['p20/frog/refresh_more'] = ['execute if entity @s[tag=bm.wilfrey] run function bm:p2/wil/refresh']

    # ---------------- clicking Wilfrey (the interaction box follows him)
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.wil_box] if data entity @s interaction at @s run function bm:p2/wil/click')
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.wil_box] if data entity @s attack run data remove entity @s attack')
    fn('p2/wil/click', ['scoreboard players operation #me bm.pid = @s bm.pid',
                        'execute as @e[type=minecraft:wolf,tag=bm.wilfrey] if score @s bm.pid = #me bm.pid run tag @s add bm.fsel',
                        'execute as @e[type=minecraft:wolf,tag=bm.fsel] on passengers if entity @s[tag=bm.wil_bag] run tag @s add bm.fbag',
                        'execute on target at @s run function bm:p2/wil/click_player',
                        'tag @e[tag=bm.fsel] remove bm.fsel', 'tag @e[tag=bm.fbag] remove bm.fbag', 'tag @a remove bm.giver',
                        'data remove entity @s interaction'])
    route = ['tag @s add bm.giver',
             'scoreboard players set #own bm.rng 0',
             'execute as @e[type=minecraft:wolf,tag=bm.fsel] if function bm:p20/frog/is_givers run scoreboard players set #own bm.rng 1',
             'execute if score #own bm.rng matches 0 run return run ' + title('@s', 'actionbar', T('Wilfrey nods politely. He has sworn himself to another.', 'gray')),
             'scoreboard players set #did bm.rng 0',
             'execute if predicate bm:p20/sneaking unless items entity @s weapon.mainhand * run function bm:p20/frog/strip']
    route += [f'execute if score #did bm.rng matches 0 if items entity @s weapon.mainhand {tag} run function bm:p20/frog/give {{slot:"{slot}"}}' for tag, slot in TAGS]
    route += ['execute if score #did bm.rng matches 0 run function bm:p2/wil/sit']
    fn('p2/wil/click_player', route)
    fn('p2/wil/sit', [f'execute store result score #s bm.rng run data get entity {sel} Sitting',
                      f'execute if score #s bm.rng matches 1 run data modify entity {sel} Sitting set value 0b',
                      f'execute if score #s bm.rng matches 0 run data modify entity {sel} Sitting set value 1b',
                      'execute if score #s bm.rng matches 1 run ' + title('@s', 'actionbar', T('"With you, friend."', 'white', italic=True)),
                      'execute if score #s bm.rng matches 0 run ' + title('@s', 'actionbar', T('"I will hold here."', 'white', italic=True)),
                      'playsound minecraft:item.armor.equip_chain neutral @a[distance=..12] ~ ~ ~ 0.7 0.8'])

    # ---------------- every tick he faces where he walks; every second: fallen check, cooldowns, his kindness
    tick.append('execute as @e[type=minecraft:wolf,tag=bm.wilfrey] at @s on passengers run rotate @s ~ 0')
    tick.append('execute as @e[type=minecraft:wolf,tag=bm.wilfrey] at @s run function bm:p2/wil/follow')
    fn('p2/wil/fallen', ['scoreboard players operation #me bm.pid = @s bm.pid',
                         'execute as @a if score @s bm.pid = #me bm.pid run function bm:p2/wil/cooldown',
                         'particle minecraft:soul ~ ~1 ~ 0.4 0.8 0.4 0.03 30', 'kill @s'])
    fn('p2/wil/cooldown', ['scoreboard players set @s bm.wlcd 1800',
                           tellraw('@s', PREFIX + [T('Wilfrey has fallen. ', '#f4f4f4', bold=True), T('His gear lies where he fell; his spirit needs 30 minutes before the locket can call him again.', 'gray')])])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #60 bm.rng 60']
    # (3 seconds of grace either way, so a chunk edge loading one before the other never fakes a death or a double)
    second += ['execute as @e[type=minecraft:wither_skeleton,tag=bm.wil_body] if function bm:p2/wil/has_wolf run scoreboard players set @s bm.wlg 0',
               'execute as @e[type=minecraft:wither_skeleton,tag=bm.wil_body] unless function bm:p2/wil/has_wolf run scoreboard players add @s bm.wlg 1',
               'execute as @e[type=minecraft:wither_skeleton,tag=bm.wil_body,scores={bm.wlg=3..}] at @s run function bm:p2/wil/fallen',
               'execute as @e[type=minecraft:interaction,tag=bm.wil_box] unless function bm:p2/wil/has_wolf run kill @s',
               'execute as @e[type=minecraft:wolf,tag=bm.wilfrey] if function bm:p2/wil/has_body run scoreboard players set @s bm.wlg 0',
               'execute as @e[type=minecraft:wolf,tag=bm.wilfrey] unless function bm:p2/wil/has_body run scoreboard players add @s bm.wlg 1',
               'execute as @e[type=minecraft:wolf,tag=bm.wilfrey,scores={bm.wlg=3..}] at @s run function bm:p2/wil/make_body',
               'execute as @e[tag=bm.wil_part] unless function bm:p20/frog/has_vehicle run kill @s',
               'scoreboard players remove @a[scores={bm.wlcd=1..}] bm.wlcd 1',
               'execute as @e[type=minecraft:wolf,tag=bm.wilfrey] at @s run particle minecraft:end_rod ~ ~1.6 ~ 0.25 0.5 0.25 0.01 1',
               'execute as @e[type=minecraft:wolf,tag=bm.wilfrey] at @s if predicate bm:p20/croak on owner if entity @s[distance=..10] run effect give @s minecraft:regeneration 5 0 true']
    return dict(tick=tick, fast=fast, second=second)

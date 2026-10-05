"""Phase 1.10: Wings of the Elder Dragon, and the Frog with Mustache (a frog knight) - a companion you hire in his swamp hut.

The companion is an invisible tamed wolf (it follows you, fights what you fight, defends you, sits on command and
teleports to you) carrying three item displays as passengers: the 3D frog (wearing a helmet model to match what he
wears), the weapon in his hand, and an empty 'bag' display used as a swap slot. Hand him a weapon or armour (right-click
him while holding it) and he equips it - the item really sits in the wolf's equipment slot, so its damage, armour and
enchantments all count. Sneak + right-click empty-handed and he hands everything back. If he dies, his gear drops.
Importing registers the items; generate(G) runs after phase19.generate."""
from nbt import snbt, B, F, Int, D as Dd
from items import item, T, TOTEM, consumable, attr, ench

# ===================================================================== ITEMS
item('dragon_wings', 'minecraft:elytra', 'Wings of the Elder Dragon', '#b04ce0',
     ['Cut from a dragon that never saw the End.', ('Unbreakable. +5 Armor, +3 Toughness.', 'blue'),
      ('Fire Resistance while worn.', 'blue'), ('Trails violet flame while gliding.', 'dark_aqua')],
     model='bm:dragon_wings', bold=True, tier=3,
     comps={'minecraft:unbreakable': {},
            'minecraft:equippable': {'slot': 'chest', 'asset_id': 'bm:dragon_wings', 'equip_sound': 'minecraft:item.armor.equip_elytra',
                                     'damage_on_hurt': False},
            'minecraft:enchantments': ench(protection=4),
            'minecraft:attribute_modifiers': [attr('armor', 5, 'chest'), attr('armor_toughness', 3, 'chest'),
                                              attr('knockback_resistance', 0.1, 'chest')]},
     cat='gear', price=('trophy', 12))
item('sealed_map_frog', TOTEM, "Sealed Croaker's Map", 'green',
     ['Hold right-click to break the seal.', "Marks the nearest swamp hut of", 'the Frog with Mustache.'],
     model='minecraft:map', glint=True, stack=16,
     comps={'minecraft:consumable': consumable(0.8, 'none', 'minecraft:item.book.page_turn', False)}, cat='map')

HELMS = [('leather_helmet', 'leather'), ('chainmail_helmet', 'chain'), ('iron_helmet', 'iron'), ('golden_helmet', 'gold'),
         ('diamond_helmet', 'diamond'), ('netherite_helmet', 'netherite'), ('turtle_helmet', 'turtle'), ('copper_helmet', 'copper')]
SLOTS = [('#bm:frog_weapon', 'weapon.mainhand'), ('#minecraft:head_armor', 'armor.head'), ('#minecraft:chest_armor', 'armor.chest'),
         ('#minecraft:leg_armor', 'armor.legs'), ('#minecraft:foot_armor', 'armor.feet')]
FROG_SCALE = 0.8
WOLF_TOP = 0.85            # wolf passenger attachment height: the displays are pulled back down to the ground


def extend_offers(O, offer):
    O['outfitter'].append(offer(('trophy', 12), ('dragon_wings', 1), ('dragon_head', 1)))
    O['professor'].append(offer(('token', 2), ('sealed_map_frog', 1)))
    O['fence'].append(offer(('token', 2), ('sealed_map_frog', 1)))


def generate(G):
    fn, wjson, title, tellraw, give = G.fn, G.wjson, G.title, G.tellraw, G.give
    PREFIX = G.PREFIX
    tick, fast, second = [], [], []
    ident = [F(0), F(0), F(0), F(1)]

    # ---------------- Wings of the Elder Dragon
    worn = 'if items entity @s armor.chest *[minecraft:custom_data~{bm:"dragon_wings"}]'
    fast.append(f'execute as @a[gamemode=!spectator] {worn} run effect give @s minecraft:fire_resistance 3 0 true')
    fast.append(f'execute as @a[gamemode=!spectator] {worn} if predicate bm:gliding at @s run function bm:p20/dragon_trail')
    fn('p20/dragon_trail', ['particle minecraft:reverse_portal ~ ~0.4 ~ 0.4 0.2 0.4 0.03 8',
                            'particle minecraft:soul_fire_flame ~ ~0.3 ~ 0.3 0.1 0.3 0.01 2',
                            'particle minecraft:witch ~ ~0.5 ~ 0.5 0.2 0.5 0 2'])

    # ---------------- Frog with Mustache at home (hut marker -> figure + hire box + nameplate)
    frog = {'Tags': ['bm.npc', 'bm.new', 'bm.frog_hut'], 'teleport_duration': Int(6),
            'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:frog',
                                                                               'minecraft:custom_model_data': {'strings': ['sit', 'iron']}}},
            'item_display': 'fixed', 'billboard': 'fixed', 'shadow_radius': F(0.35),
            'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(FROG_SCALE / 2), F(0)],
                               'scale': [F(FROG_SCALE)] * 3}}
    box = {'Tags': ['bm.npc', 'bm.new', 'bm.frog_hire'], 'width': F(1.0), 'height': F(1.0), 'response': B(1)}
    plate = {'Tags': ['bm.npc', 'bm.new', 'bm.frog_plate'], 'billboard': 'center', 'default_background': B(0), 'background': Int(0x60000000),
             'text': [T('Frog with Mustache', 'green', bold=True), T('\nFrog Knight', 'gray', italic=True), T('\nright-click to hire: 1 Medallion', 'yellow')],
             'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(1.45), F(0)], 'scale': [F(0.6)] * 3}}
    fin = ['execute rotated as @s run tp @e[tag=bm.new,distance=..2] ~ ~ ~ ~ 0', 'tag @e[tag=bm.new,distance=..2] remove bm.new']
    fn('npc/frog_hut', [f'summon minecraft:item_display ~ ~ ~ {snbt(frog)}', f'summon minecraft:interaction ~ ~ ~ {snbt(box)}',
                        f'summon minecraft:text_display ~ ~ ~ {snbt(plate)}'] + fin)
    G.FUNCS['npc/spawn'][0:0] = ['execute if entity @s[tag=bm.npc.frog_hut] run function bm:npc/frog_hut']
    second.append('kill @e[type=minecraft:item_display,tag=bm.frog]')           # 1.9's market frog has moved out
    fn('admin/place_frog_hut', ['place template bm:frog_hut ~-7 ~-4 ~-7',
                                tellraw('@s', PREFIX + [T("The Frog with Mustache's hut placed (door faces south).", 'gray')])])

    # ---------------- hiring
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.frog_hire] if data entity @s interaction at @s run function bm:p20/frog/hire_click')
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.frog_hire] if data entity @s attack run data remove entity @s attack')
    fn('p20/frog/hire_click', ['execute on target at @s run function bm:p20/frog/hire', 'tag @a remove bm.giver', 'data remove entity @s interaction'])
    fn('p20/frog/is_givers', ['return run execute on owner if entity @s[tag=bm.giver]'])
    fn('p20/frog/hire', [
        'tag @s add bm.giver', 'tag @e[type=minecraft:wolf,tag=bm.fmine] remove bm.fmine',
        'execute as @e[type=minecraft:wolf,tag=bm.frogpet] if function bm:p20/frog/is_givers run tag @s add bm.fmine',
        'execute if entity @e[type=minecraft:wolf,tag=bm.fmine] run return run function bm:p20/frog/recall',
        'execute store result score #paid bm.rng run clear @s *[minecraft:custom_data~{bm:"medallion"}] 1',
        'execute if score #paid bm.rng matches 0 run return run function bm:p20/frog/broke',
        'function bm:p20/frog/summon'])
    fn('p20/frog/recall', ['tp @e[type=minecraft:wolf,tag=bm.fmine] @s', 'tag @e[type=minecraft:wolf,tag=bm.fmine] remove bm.fmine',
                           'playsound minecraft:entity.frog.long_jump neutral @a[distance=..16] ~ ~ ~ 1 1',
                           title('@s', 'actionbar', T('The Frog with Mustache is already sworn to you. He hops back to your side.', 'green'))])
    fn('p20/frog/broke', ['playsound minecraft:entity.frog.ambient neutral @a[distance=..16] ~ ~ ~ 1 0.6',
                          title('@s', 'actionbar', T('"One Medallion, friend. A knight has standards."', 'green', italic=True))])
    wolf = {'Tags': ['bm.frogpet', 'bm.fp_new', 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1),
            'CustomName': T('Frog with Mustache', 'green', bold=True), 'CustomNameVisible': B(0), 'Health': F(40),
            'attributes': [{'id': 'minecraft:max_health', 'base': Dd(40)}, {'id': 'minecraft:attack_damage', 'base': Dd(5)},
                           {'id': 'minecraft:movement_speed', 'base': Dd(0.34)}, {'id': 'minecraft:follow_range', 'base': Dd(32)}],
            'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0),
                                'show_icon': B(0), 'ambient': B(0)}],
            'drop_chances': {s: F(2.0) for s in ('mainhand', 'head', 'chest', 'legs', 'feet')}}
    body = {'Tags': ['bm.fp_disp', 'bm.fp_body', 'bm.fp_new'], 'teleport_duration': Int(2), 'shadow_radius': F(0.35),
            'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:frog',
                                                                               'minecraft:custom_model_data': {'strings': ['sit', 'none']}}},
            'item_display': 'fixed', 'billboard': 'fixed',
            'transformation': {'left_rotation': ident, 'right_rotation': ident,
                               'translation': [F(0), F(round(FROG_SCALE / 2 - WOLF_TOP, 3)), F(0)], 'scale': [F(FROG_SCALE)] * 3}}
    weap = {'Tags': ['bm.fp_disp', 'bm.fp_weap', 'bm.fp_new'], 'teleport_duration': Int(2), 'item_display': 'fixed', 'billboard': 'fixed',
            'transformation': {'left_rotation': [F(0), F(0.7071), F(0), F(0.7071)], 'right_rotation': ident,
                               'translation': [F(0.42), F(round(0.42 - WOLF_TOP, 3)), F(-0.05)], 'scale': [F(0.6)] * 3}}
    bag = {'Tags': ['bm.fp_disp', 'bm.fp_bag', 'bm.fp_new'],
           'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0), F(0)], 'scale': [F(0)] * 3}}
    fn('p20/frog/summon', [
        f'summon minecraft:wolf ~ ~ ~ {snbt(wolf)}',
        'data modify entity @e[type=minecraft:wolf,tag=bm.fp_new,limit=1,sort=nearest] Owner set from entity @s UUID',
        f'summon minecraft:item_display ~ ~ ~ {snbt(body)}', f'summon minecraft:item_display ~ ~ ~ {snbt(weap)}',
        f'summon minecraft:item_display ~ ~ ~ {snbt(bag)}',
        'execute as @e[type=minecraft:item_display,tag=bm.fp_new,distance=..2] run ride @s mount @e[type=minecraft:wolf,tag=bm.fp_new,limit=1,sort=nearest]',
        'tag @e[tag=bm.fp_new,distance=..3] remove bm.fp_new',
        'particle minecraft:happy_villager ~ ~0.5 ~ 0.5 0.4 0.5 0 15',
        'playsound minecraft:entity.frog.ambient neutral @a[distance=..16] ~ ~ ~ 1 1.2',
        'playsound minecraft:item.armor.equip_chain neutral @a[distance=..16] ~ ~ ~ 1 1',
        'title @s times 10 50 15', title('@s', 'subtitle', T('Hand him a blade or armour to equip him', 'gray', italic=True)),
        title('@s', 'title', T('The Frog with Mustache joins you!', 'green', bold=True)),
        tellraw('@s', PREFIX + [T('The Frog with Mustache follows you, fights what you fight and defends you. ', 'green'),
                                T('Right-click him holding a weapon or armour to equip it; empty-handed to make him wait or follow; ', 'gray'),
                                T('sneak + right-click empty-handed to take your gear back. Feed him any meat to heal him.', 'gray')])])

    # ---------------- equipping
    wjson('bm/tags/item/frog_weapon.json', {'values': ['#minecraft:swords', '#minecraft:axes', '#minecraft:spears', 'minecraft:trident', 'minecraft:mace']})
    wjson('bm/predicate/p20/sneaking.json', {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:flags': {'is_sneaking': True}}})
    wjson('bm/advancement/frog_interact.json', {'criteria': {'i': {'trigger': 'minecraft:player_interacted_with_entity', 'conditions': {
        'entity': [{'condition': 'minecraft:entity_properties', 'entity': 'this',
                    'predicate': {'minecraft:entity_type': 'minecraft:wolf', 'minecraft:nbt': '{Tags:["bm.frogpet"]}'}}]}}}, 'rewards': {'function': 'bm:p20/frog/interact'}})
    sel = '@e[type=minecraft:wolf,tag=bm.fsel,limit=1,sort=nearest]'
    fn('p20/frog/interact', [
        'advancement revoke @s only bm:frog_interact', 'tag @s add bm.giver',
        'execute as @e[type=minecraft:wolf,tag=bm.frogpet,distance=..8] if function bm:p20/frog/is_givers run tag @s add bm.fsel',
        f'execute as {sel} on passengers if entity @s[tag=bm.fp_bag] run tag @s add bm.fbag',
        f'execute if entity {sel} run function bm:p20/frog/route',
        'tag @e[tag=bm.fsel] remove bm.fsel', 'tag @e[tag=bm.fbag] remove bm.fbag', 'tag @s remove bm.giver'])
    route = ['execute if predicate bm:p20/sneaking unless items entity @s weapon.mainhand * run return run function bm:p20/frog/strip']
    route += [f'execute if items entity @s weapon.mainhand {tag} run return run function bm:p20/frog/give {{slot:"{slot}"}}' for tag, slot in SLOTS]
    fn('p20/frog/route', route)
    fn('p20/frog/give', [
        f'$item replace entity @e[type=minecraft:item_display,tag=bm.fbag,limit=1] contents from entity {sel} $(slot)',
        f'$item replace entity {sel} $(slot) from entity @s weapon.mainhand',
        'item replace entity @s weapon.mainhand from entity @e[type=minecraft:item_display,tag=bm.fbag,limit=1] contents',
        'item replace entity @e[type=minecraft:item_display,tag=bm.fbag,limit=1] contents with minecraft:air',
        f'execute as {sel} run function bm:p20/frog/refresh',
        f'data modify entity {sel} Sitting set value 0b',
        f'execute at {sel} run particle minecraft:wax_on ~ ~0.6 ~ 0.3 0.3 0.3 0 8',
        'playsound minecraft:item.armor.equip_iron neutral @a[distance=..16] ~ ~ ~ 1 1.1',
        f'execute as {sel} at @s run function bm:p20/frog/msg_give', 'scoreboard players set #did bm.rng 1'])
    fn('p20/frog/strip', [f'execute as {sel} at @s run function bm:p20/frog/drop {{slot:"{s}"}}' for _, s in SLOTS] + [
        f'execute as {sel} run function bm:p20/frog/refresh', f'data modify entity {sel} Sitting set value 0b',
        'playsound minecraft:item.armor.equip_leather neutral @a[distance=..16] ~ ~ ~ 1 0.8',
        f'execute as {sel} at @s run function bm:p20/frog/msg_strip', 'scoreboard players set #did bm.rng 1'])
    # messages / extra refresh per ally (the frog here; Wilfrey, the Phase 2 ally, has the same wolf-based body)
    fn('p20/frog/msg_give', ['execute if entity @s[tag=bm.frogpet] run playsound minecraft:entity.frog.ambient neutral @a[distance=..16] ~ ~ ~ 0.8 1.3',
                             'execute if entity @s[tag=bm.frogpet] run ' + title('@a[tag=bm.giver]', 'actionbar', T('The Frog with Mustache accepts it with a solemn croak.', 'green')),
                             'execute if entity @s[tag=bm.wilfrey] run ' + title('@a[tag=bm.giver]', 'actionbar', T('Wilfrey bows and takes it. "Thank you, friend."', 'white')),
                             'execute if entity @s[tag=bm.wilfrey] run function bm:p20/frog/refresh_more'])
    fn('p20/frog/msg_strip', ['execute if entity @s[tag=bm.frogpet] run ' + title('@a[tag=bm.giver]', 'actionbar', T('The Frog with Mustache hands back your gear.', 'green')),
                              'execute if entity @s[tag=bm.wilfrey] run ' + title('@a[tag=bm.giver]', 'actionbar', T('Wilfrey returns your gear, neatly folded.', 'white')),
                              'execute if entity @s[tag=bm.wilfrey] run function bm:p20/frog/refresh_more'])
    fn('p20/frog/refresh_more', ['return 0'])       # Phase 2 replaces this with Wilfrey's armour-stand dressing
    # as the wolf: drop one slot's item at the giver's feet (an item entity gets the exact stack)
    fn('p20/frog/drop', ['$execute unless items entity @s $(slot) * run return 0',
                         'execute at @a[tag=bm.giver,limit=1] run summon minecraft:item ~ ~0.3 ~ {Item:{id:"minecraft:stone",count:1},PickupDelay:5s,Tags:["bm.fdrop"]}',
                         '$item replace entity @e[type=minecraft:item,tag=bm.fdrop,limit=1] contents from entity @s $(slot)',
                         '$item replace entity @s $(slot) with minecraft:air',
                         'tag @e[type=minecraft:item,tag=bm.fdrop] remove bm.fdrop'])
    # as the wolf: the weapon he holds, the helmet he wears
    refresh = ['execute on passengers if entity @s[tag=bm.fp_weap] run item replace entity @s contents from entity @e[type=minecraft:wolf,tag=bm.fsel,limit=1] weapon.mainhand',
               'execute on passengers if entity @s[tag=bm.fp_body] run data modify entity @s item.components."minecraft:custom_model_data".strings[1] set value "none"',
               'execute if items entity @s armor.head * on passengers if entity @s[tag=bm.fp_body] run data modify entity @s item.components."minecraft:custom_model_data".strings[1] set value "iron"']
    refresh += [f'execute if items entity @s armor.head minecraft:{hid} on passengers if entity @s[tag=bm.fp_body] run data modify entity @s item.components."minecraft:custom_model_data".strings[1] set value "{m}"'
                for hid, m in HELMS]
    fn('p20/frog/refresh', refresh)

    # ---------------- every tick: displays face where he faces. Every second: tidy up, heal slowly, croak now and then
    tick.append('execute as @e[type=minecraft:wolf,tag=bm.frogpet] at @s on passengers run rotate @s ~ 0')
    fn('p20/frog/has_vehicle', ['return run execute on vehicle if entity @s[type=minecraft:wolf]'])
    second += ['execute as @e[type=minecraft:item_display,tag=bm.fp_disp] unless function bm:p20/frog/has_vehicle run kill @s',
               'effect give @e[type=minecraft:wolf,tag=bm.frogpet] minecraft:regeneration 3 0 true',
               'execute as @e[type=minecraft:wolf,tag=bm.frogpet] at @s if predicate bm:p20/croak run playsound minecraft:entity.frog.ambient neutral @a[distance=..16] ~ ~ ~ 0.8 1']
    wjson('bm/predicate/p20/croak.json', {'condition': 'minecraft:random_chance', 'chance': 0.04})

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second

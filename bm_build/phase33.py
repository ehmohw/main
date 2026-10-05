"""Phase 1.20 / 2.13: new goods.

- VACUUM SATCHEL (the Fence's back room... and Zorp): a satchel with 27 slots. Right-click: switch it ON or OFF; while ON
  and anywhere in your inventory it pulls dropped items within 6 blocks straight into itself (stacks merge). Sneak +
  right-click opens it (you sit in a little crate: press your inventory key; sneak to close).
- TOOL FUSION at the Xenite Altar: sneak + right-click with a pickaxe, shovel, axe or hoe in your main hand and a
  DIFFERENT tool in your off hand. The off-hand tool is melted in and the main tool also mines like it (at its own
  speed). Costs 8 levels. Two capabilities at most: a fused tool cannot be fused again.
- DIMENSION SHIFTER (Zorp): right-click for a menu - the Overworld, the Nether or the End, each to a safe spot. Never the
  Hollow Throne, never from inside a dungeon. 30 second recharge.
- TRIPLE JUMP BOOTS (Zorp): jump again straight after landing for a higher hop, and a third time for a big one.
- SPRING-LOADED BOOTS (Zorp): hold sneak on the ground to charge (up to 2 s), then jump: 2 to 5 blocks.
- VOID TOTEM (the Void Rat): if you fall into the void and start to take damage, it pulls you back to the last solid
  ground you stood on. Used up.
- EXPERIENCE FLASK (Prof. Whiskerton): right-click to pour in all your experience; sneak + right-click to drink it back.
- POCKET ENDER CHEST (the Void Rat): your ender chest, anywhere (sneak to close).
- VOID HINGE (the Void Rat): upgrades a shulker box (hold the box in your off hand, use the hinge). After that, sneak +
  right-click the air with the box in hand to open it without placing it.
- SANGUINE FANG (the Bloodbroker): in your off hand, every kill heals half a heart. The VAMPIRE LORD set now heals two
  full hearts per kill (it healed on hits before, and rarely seemed to).
- ROCKET BOOTS kick about twice as hard (~15 blocks a burst).
- THE RAT BANK keeps every currency: Blood Crystals, all four Xenite colours, Ember Scales and Void Shards too."""
from nbt import snbt, B, F, Int, D
from items import item, consumable, attr, T, TOTEM, ITEM_VERSION, ITEMS, DYNAMIC
from useitem import hold, HOLD
import phase22 as R22
import phase24 as R24
import phase31 as R31

BANK_EXTRA = [('blood_crystal', 'bm.bk_bld', 'Blood Crystals', 'dark_red'), ('ember_scale', 'bm.bk_emb', 'Ember Scales', '#ff7a1a'),
              ('void_shard', 'bm.bk_void', 'Void Shards', '#b05cff'), ('xenite_green', 'bm.bk_xg', 'Green Xenite', '#7dff6a'),
              ('xenite_violet', 'bm.bk_xv', 'Violet Xenite', '#c27dff'), ('xenite_cyan', 'bm.bk_xc', 'Cyan Xenite', '#6af2ff'),
              ('xenite_red', 'bm.bk_xr', 'Red Xenite', '#ff4a4a')]
R31.BANK += BANK_EXTRA

TOOLS = ('pickaxe', 'shovel', 'axe', 'hoe')
TIERS = ('wooden', 'stone', 'copper', 'golden', 'iron', 'diamond', 'netherite')
JUMP = {'triple': (0.62, 0.97), 'charge': (0.55, 0.69, 0.80, 0.91)}      # jump_strength per level (base 0.42 = 1.25 blocks)

# ===================================================================== items
item('vacuum_satchel', TOTEM, 'Vacuum Satchel', '#c8a050',
     ['A smuggler\'s bag with a hungry little engine.', ('Right-click: switch it ON or OFF.', 'blue'),
      ('ON: pulls dropped items within 6 blocks', 'blue'), ('straight into itself (27 slots).', 'blue'),
      ('Sneak + right-click: open it.', 'blue'), ('(Sneak again to close.)', 'gray')],
     model='bm:vacuum_satchel', stack=1, cat='builder', comps=dict(hold('bundle'), **{'minecraft:container': []}), price=('medallion', 4))
DYNAMIC.add('vacuum_satchel')
HOLD['vacuum_satchel'] = 'bm:p33/vac/use'
item('dimension_shifter', TOTEM, 'Dimension Shifter', '#b48cff',
     ['Donadian travel tech. Fragile. Loud.', ('Right-click: choose a dimension -', 'blue'), ('Overworld, Nether or End -', 'blue'),
      ('and arrive somewhere safe.', 'blue'), ('Never the Hollow Throne; never from a dungeon.', 'gray'), ('30 second recharge.', 'gray')],
     model='bm:dimension_shifter', stack=1, cat='alien', glint=True, comps=hold('spyglass'))
HOLD['dimension_shifter'] = 'bm:p33/shift/use'
item('triple_boots', 'minecraft:iron_boots', 'Triple Jump Boots', '#ff5555',
     ['Wahoo!', ('Jump again right after you land for a higher', 'blue'), ('hop - and a third time for a big one.', 'blue'),
      ('+6 Safe Fall', 'blue')], model='bm:triple_boots', stack=1, cat='alien',
     comps={'minecraft:attribute_modifiers': [attr('armor', 2, 'feet', ident='minecraft:armor.boots'), attr('safe_fall_distance', 6, 'feet')]})
item('spring_boots', 'minecraft:iron_boots', 'Spring-Loaded Boots', '#6af2ff',
     ['A coil in each heel.', ('Hold sneak on the ground to charge (up to 2 s),', 'blue'), ('then jump: 2 to 5 blocks.', 'blue'),
      ('+5 Safe Fall', 'blue')], model='bm:spring_boots', stack=1, cat='alien',
     comps={'minecraft:attribute_modifiers': [attr('armor', 2, 'feet', ident='minecraft:armor.boots'), attr('safe_fall_distance', 5, 'feet')]})
item('void_totem', TOTEM, 'Void Totem', '#b05cff',
     ['Carved from a shard of the outer End.', ('Keep it in your inventory: if you fall into', 'blue'), ('the void, it pulls you back to solid ground.', 'blue'),
      ('Used up when it saves you.', 'gray')], model='bm:void_totem', stack=16, cat='relic', glint=True)
item('xp_flask', TOTEM, 'Experience Flask', '#7cff4a',
     ['A bottle that remembers what you learned.', ('Right-click: pour in all your experience.', 'blue'), ('Sneak + right-click: drink it all back.', 'blue'),
      ('Stored: 0 XP', 'green')], model='bm:xp_flask', stack=1, cat='builder', comps=hold('drink'), custom_extra={'bm_xp': 0},
     price=('token', 6))
DYNAMIC.add('xp_flask')
HOLD['xp_flask'] = 'bm:p33/xp/use'
item('pocket_ender_chest', TOTEM, 'Pocket Ender Chest', '#2f8a7a',
     ['Your ender chest, in your pocket.', ('Right-click: open it (press your inventory key).', 'blue'), ('Sneak to close.', 'gray')],
     model='bm:pocket_ender_chest', stack=1, cat='relic', comps=hold('none'))
HOLD['pocket_ender_chest'] = 'bm:p33/pec/use'
item('void_hinge', TOTEM, 'Void Hinge', '#c08bff',
     ['A hinge that opens into the box from anywhere.', ('Hold a shulker box in your off hand and', 'blue'), ('use the hinge: from then on, sneak +', 'blue'),
      ('right-click the air with that box in hand to', 'blue'), ('open it without placing it.', 'blue')],
     model='bm:void_hinge', stack=16, cat='relic', comps={'minecraft:consumable': consumable(0.6, 'none', 'minecraft:block.iron_trapdoor.open', False)})
item('sanguine_fang', TOTEM, 'Sanguine Fang', '#b0002a',
     ['A tooth from a Blood Moon horror.', ('In your off hand: every kill heals', 'blue'), ('half a heart.', 'blue')],
     model='bm:sanguine_fang', stack=1, cat='blood', glint=True)

# Zorp sells the new boots and the shifter (their offers join his list at import, before phase24 builds his checksum)
_k = next(i for i, o in enumerate(R24.OFFERS) if o[2][0] == 'xenite_violet')
R24.OFFERS[_k:_k] = [(('xenite_violet', 14), ('xenite_green', 6), ('triple_boots', 1)), (('xenite_cyan', 14), ('xenite_green', 6), ('spring_boots', 1)),
                     (('xenite_cyan', 24), ('xenite_red', 6), ('dimension_shifter', 1)), (('xenite_green', 12), ('xenite_violet', 12), ('vacuum_satchel', 1))]
R22.VOID_OFFERS[-1:-1] = [(('void_shard', 14), ('void_totem', 1)), (('void_shard', 24), ('pocket_ender_chest', 1)), (('void_shard', 10), ('void_hinge', 1))]


def extend_offers(O, offer):
    O['professor'].append(offer(('token', 4), ('xp_flask', 1)))
    O['professor'].append(offer(('token', 2), ('sealed_map_mothership', 1)))     # 2.13: Zorp only waits aboard the motherships now
    O['blood'].append(offer(('blood_crystal', 14), ('sanguine_fang', 1)))


# ===================================================================== generation
def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    import phase28 as P28
    tick, fast, second, load = [], [], [], []
    objs = ['bm.jumps minecraft.custom:minecraft.jump', 'bm.tjc dummy', 'bm.tjg dummy', 'bm.tjm dummy', 'bm.cjc dummy', 'bm.cjg dummy', 'bm.cjm dummy',
            'bm.vx dummy', 'bm.vy dummy', 'bm.vz dummy', 'bm.vd dummy', 'bm.vok dummy', 'bm.shcd dummy', 'bm.pbx dummy', 'bm.xpn dummy']
    load += [f'scoreboard objectives add {o}' for o in objs]
    G.OBJECTIVES += [o.split()[0] for o in objs]
    holds = '*[minecraft:custom_data~{bm:"%s"}]'

    # ------------------------------------------------------------------ the crate trick: a chest boat you sit in (press E)
    # Opening moves the items INTO the boat (nothing is copied, so nothing can be duplicated); closing moves them back.
    # A boat whose rider is gone (sneak, death, logout) closes itself; one whose owner is offline waits for them.
    wjson('bm/tags/entity_type/p33_crates.json', {'values': ['minecraft:dark_oak_chest_boat']})
    crate = {'Tags': ['bm.crate', 'bm.cnew'], 'Invulnerable': B(1), 'Silent': B(1), 'CustomName': T('Satchel', '#c8a050')}
    def open_crate(kind, label):
        return [f'summon minecraft:dark_oak_chest_boat ~ ~ ~ {snbt(dict(crate, Tags=["bm.crate", "bm.cnew", f"bm.c_{kind}"], CustomName=T(label, "#c8a050")))}',
                'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                'scoreboard players operation @e[type=minecraft:dark_oak_chest_boat,tag=bm.cnew,distance=..1,limit=1] bm.pid = @s bm.pid']
    def mount():
        return ['ride @s mount @e[type=minecraft:dark_oak_chest_boat,tag=bm.cnew,distance=..1,limit=1]',
                'tag @e[type=minecraft:dark_oak_chest_boat,tag=bm.cnew] remove bm.cnew',
                'playsound minecraft:block.barrel.open player @s ~ ~ ~ 1 1',
                title('@s', 'actionbar', T('Press your inventory key to open it. Sneak to close.', '#c8a050'))]
    # a rider-less crate closes: hand its contents back to its owner (if online), then vanish
    second += ['execute as @e[type=minecraft:dark_oak_chest_boat,tag=bm.crate] unless function bm:p33/crate/ridden at @s run function bm:p33/crate/close']
    fn('p33/crate/ridden', ['execute on passengers if entity @s[type=minecraft:player] run return 1', 'return 0'])
    fn('p33/crate/close', ['scoreboard players operation #own bm.pid = @s bm.pid', 'tag @a remove bm.cown',
                           'execute as @a if score @s bm.pid = #own bm.pid run tag @s add bm.cown',
                           'execute unless entity @a[tag=bm.cown] run return 0',
                           'execute if entity @s[tag=bm.c_pec] run function bm:p33/pec/close',
                           'execute if entity @s[tag=bm.c_box] run function bm:p33/box/close',
                           'tag @a remove bm.cown', 'data modify entity @s Items set value []', 'tp @s ~ -400 ~', 'kill @s'])

    # ------------------------------------------------------------------ POCKET ENDER CHEST
    fn('p33/pec/use', open_crate('pec', 'Pocket Ender Chest') +
       [f'item replace entity @e[type=minecraft:dark_oak_chest_boat,tag=bm.cnew,distance=..1,limit=1] container.{i} from entity @s enderchest.{i}' for i in range(27)] +
       [f'item replace entity @s enderchest.{i} with minecraft:air' for i in range(27)] + mount())
    fn('p33/pec/close', [f'item replace entity @a[tag=bm.cown,limit=1] enderchest.{i} from entity @s container.{i}' for i in range(27)] +
       [f'item replace entity @s container.{i} with minecraft:air' for i in range(27)] +
       ['execute as @a[tag=bm.cown,limit=1] at @s run playsound minecraft:block.ender_chest.close player @s ~ ~ ~ 1 1'])

    # ------------------------------------------------------------------ boxes (the satchel and hinged shulker boxes): the item
    # itself is taken out of your hand and kept in storage while it's open; its contents go into the crate
    fn('p33/box/open', ['$data modify storage bm:tmp bx set value {path:"$(path)",slot:"$(slot)"}'] + open_crate('box', 'Satchel') + [
        'execute store result storage bm:tmp bx.pid int 1 run scoreboard players get @s bm.pid',
        'function bm:p33/box/open2 with storage bm:tmp bx'] + mount())
    fn('p33/box/open2', [
        '$data modify storage bm:pbox p$(pid) set from entity @s $(path)',
        '$data modify storage bm:tmp bx.src set from entity @s $(path).components."minecraft:container"',
        '$item replace entity @s $(slot) with minecraft:air',
        'function bm:p33/box/fill'])
    fn('p33/box/fill', ['execute unless data storage bm:tmp bx.src[0] run return 0',
                        'data modify storage bm:tmp bx.a set value {}', 'data modify storage bm:tmp bx.a.slot set from storage bm:tmp bx.src[0].slot',
                        'data modify storage bm:tmp bx.a.id set from storage bm:tmp bx.src[0].item.id', 'data modify storage bm:tmp bx.a.count set from storage bm:tmp bx.src[0].item.count',
                        'execute unless data storage bm:tmp bx.a.count run data modify storage bm:tmp bx.a.count set value 1',
                        'function bm:p33/box/fill_one with storage bm:tmp bx.a',
                        'data remove storage bm:tmp bx.src[0]', 'function bm:p33/box/fill'])
    fn('p33/box/fill_one', ['$data modify entity @e[type=minecraft:dark_oak_chest_boat,tag=bm.cnew,distance=..1,limit=1] Items append value {Slot:$(slot)b,id:"$(id)",count:$(count)}',
                            'execute if data storage bm:tmp bx.src[0].item.components run data modify entity @e[type=minecraft:dark_oak_chest_boat,tag=bm.cnew,distance=..1,limit=1] Items[-1].components set from storage bm:tmp bx.src[0].item.components'])
    fn('p33/box/close', ['execute store result storage bm:tmp bx.pid int 1 run scoreboard players get @s bm.pid', 'data modify storage bm:tmp bx.out set value []',
                         'data modify storage bm:tmp bx.src set from entity @s Items', 'function bm:p33/box/drain',
                         'function bm:p33/box/back with storage bm:tmp bx'])
    fn('p33/box/drain', ['execute unless data storage bm:tmp bx.src[0] run return 0',
                         'data modify storage bm:tmp bx.a set value {}', 'data modify storage bm:tmp bx.a.slot set from storage bm:tmp bx.src[0].Slot',
                         'data modify storage bm:tmp bx.a.id set from storage bm:tmp bx.src[0].id', 'data modify storage bm:tmp bx.a.count set from storage bm:tmp bx.src[0].count',
                         'function bm:p33/box/drain_one with storage bm:tmp bx.a', 'data remove storage bm:tmp bx.src[0]', 'function bm:p33/box/drain'])
    fn('p33/box/drain_one', ['$data modify storage bm:tmp bx.out append value {slot:$(slot),item:{id:"$(id)",count:$(count)}}',
                             'execute if data storage bm:tmp bx.src[0].components run data modify storage bm:tmp bx.out[-1].item.components set from storage bm:tmp bx.src[0].components'])
    fn('p33/box/back', ['$data modify storage bm:pbox p$(pid).components."minecraft:container" set from storage bm:tmp bx.out',
                        '$data modify storage bm:tmp give set from storage bm:pbox p$(pid)', '$data remove storage bm:pbox p$(pid)',
                        'execute as @a[tag=bm.cown,limit=1] at @s run function bm:p33/give_back'])
    # hand an exact item (storage bm:tmp give) to the player: into the main hand if it's empty, else at their feet
    fn('p33/give_back', ['summon minecraft:item_display ~ ~ ~ {Tags:["bm.gback"]}',
                         'data modify entity @e[type=minecraft:item_display,tag=bm.gback,distance=..1,limit=1] item set from storage bm:tmp give',
                         'scoreboard players set #gb bm.rng 0', 'execute unless items entity @s weapon.mainhand * run scoreboard players set #gb bm.rng 1',
                         'execute if score #gb bm.rng matches 1 run item replace entity @s weapon.mainhand from entity @e[type=minecraft:item_display,tag=bm.gback,distance=..1,limit=1] contents',
                         'execute if score #gb bm.rng matches 0 run function bm:p33/give_drop',
                         'kill @e[type=minecraft:item_display,tag=bm.gback,distance=..1]', 'playsound minecraft:block.barrel.close player @s ~ ~ ~ 1 1'])
    fn('p33/give_drop', ['summon minecraft:item ~ ~0.3 ~ {Tags:["bm.gdrop"],Item:{id:"minecraft:stone",count:1},PickupDelay:0s}',
                         'data modify entity @e[type=minecraft:item,tag=bm.gdrop,distance=..1,limit=1] Item set from storage bm:tmp give',
                         'tag @e[type=minecraft:item,tag=bm.gdrop] remove bm.gdrop'])

    # ------------------------------------------------------------------ VACUUM SATCHEL
    hand = lambda iid: ['scoreboard players set #hand bm.rng 0',
                        f'execute if items entity @s weapon.mainhand {holds % iid} run scoreboard players set #hand bm.rng 1',
                        f'execute if score #hand bm.rng matches 0 if items entity @s weapon.offhand {holds % iid} run scoreboard players set #hand bm.rng 2',
                        'execute if score #hand bm.rng matches 0 run return 0']
    on_model = 'bm:vacuum_satchel_on'
    wjson('bm/item_modifier/p33/vac_on.json', [{'function': 'minecraft:set_custom_data', 'tag': '{bm_vac:1b}'},
                                              {'function': 'minecraft:set_components', 'components': {'minecraft:item_model': on_model, 'minecraft:enchantment_glint_override': True}}])
    wjson('bm/item_modifier/p33/vac_off.json', [{'function': 'minecraft:set_custom_data', 'tag': '{bm_vac:0b}'},
                                               {'function': 'minecraft:set_components', 'components': {'minecraft:item_model': 'bm:vacuum_satchel', 'minecraft:enchantment_glint_override': False}}])
    fn('p33/vac/use', hand('vacuum_satchel') + [
        'execute if predicate bm:p20/sneaking if score #hand bm.rng matches 1 run return run function bm:p33/box/open {path:"equipment.mainhand",slot:"weapon.mainhand"}',
        'execute if predicate bm:p20/sneaking if score #hand bm.rng matches 2 run return run function bm:p33/box/open {path:"equipment.offhand",slot:"weapon.offhand"}',
        'execute if score #hand bm.rng matches 1 if items entity @s weapon.mainhand *[minecraft:custom_data~{bm_vac:1b}] run return run function bm:p33/vac/off {slot:"weapon.mainhand"}',
        'execute if score #hand bm.rng matches 2 if items entity @s weapon.offhand *[minecraft:custom_data~{bm_vac:1b}] run return run function bm:p33/vac/off {slot:"weapon.offhand"}',
        'execute if score #hand bm.rng matches 1 run return run function bm:p33/vac/on {slot:"weapon.mainhand"}',
        'function bm:p33/vac/on {slot:"weapon.offhand"}'])
    fn('p33/vac/on', ['$item modify entity @s $(slot) bm:p33/vac_on', 'playsound minecraft:block.beacon.power_select player @s ~ ~ ~ 0.6 1.6',
                      title('@s', 'actionbar', T('Vacuum Satchel: ON - dropped items nearby fly into it.', '#c8a050'))])
    fn('p33/vac/off', ['$item modify entity @s $(slot) bm:p33/vac_off', 'playsound minecraft:block.beacon.deactivate player @s ~ ~ ~ 0.6 1.6',
                       title('@s', 'actionbar', T('Vacuum Satchel: OFF.', 'gray'))])
    # collection: the first ON satchel in your inventory swallows nearby items (four per player per quarter second)
    on = '*[minecraft:custom_data~{bm:"vacuum_satchel",bm_vac:1b}]'
    fast += [f'execute as @a[gamemode=!spectator] if items entity @s container.* {on} at @s if entity @e[type=minecraft:item,distance=..6,nbt={{PickupDelay:0s}}] run function bm:p33/vac/pull']
    fn('p33/vac/pull', ['scoreboard players set #vs bm.rng -1'] +
       [f'execute if score #vs bm.rng matches -1 if items entity @s container.{i} {on} run scoreboard players set #vs bm.rng {i}' for i in range(36)] +
       ['execute if score #vs bm.rng matches -1 run return 0',
        'execute store result storage bm:tmp vac.n int 1 run scoreboard players get #vs bm.rng',
        'function bm:p33/vac/read with storage bm:tmp vac', 'scoreboard players set #vtak bm.rng 0', 'tag @s add bm.vacuser',
        'execute as @e[type=minecraft:item,distance=..6,nbt={PickupDelay:0s},limit=4,sort=nearest] unless items entity @s contents *[minecraft:custom_data~{bm:"vacuum_satchel"}] at @s run function bm:p33/vac/take',
        'tag @s remove bm.vacuser',
        'execute if score #vtak bm.rng matches 1.. run function bm:p33/vac/write with storage bm:tmp vac'])
    fn('p33/vac/read', ['data remove storage bm:tmp vac.c', '$data modify storage bm:tmp vac.c set from entity @s Inventory[{Slot:$(n)b}].components."minecraft:container"',
                        'execute unless data storage bm:tmp vac.c run data modify storage bm:tmp vac.c set value []'])
    fn('p33/vac/write', ['$item modify entity @s container.$(n) {function:"minecraft:set_components",components:{"minecraft:container":$(c)}}',
                         'playsound minecraft:entity.item.pickup player @s ~ ~ ~ 0.4 0.6'])
    # one item entity -> merge into matching stacks, then the first free slot; what doesn't fit stays on the ground
    fn('p33/vac/take', ['data modify storage bm:tmp vac.in set from entity @s Item', 'execute store result score #vn bm.rng run data get storage bm:tmp vac.in.count',
                        'scoreboard players set #vmax bm.rng 64', 'execute if items entity @s contents *[minecraft:max_stack_size=16] run scoreboard players set #vmax bm.rng 16',
                        'execute if items entity @s contents *[minecraft:max_stack_size=1] run scoreboard players set #vmax bm.rng 1',
                        'data modify storage bm:tmp vac.c2 set value []', 'function bm:p33/vac/merge',
                        'execute if score #vn bm.rng matches 1.. run function bm:p33/vac/newslot',
                        'data modify storage bm:tmp vac.c set from storage bm:tmp vac.c2',
                        'scoreboard players add #vtak bm.rng 1',
                        'execute if score #vn bm.rng matches ..0 run particle minecraft:poof ~ ~0.2 ~ 0.1 0.1 0.1 0.01 3',
                        'execute if score #vn bm.rng matches ..0 run return run kill @s',
                        'execute store result entity @s Item.count int 1 run scoreboard players get #vn bm.rng'])
    fn('p33/vac/merge', ['execute unless data storage bm:tmp vac.c[0] run return 0',
                         'execute if score #vn bm.rng matches 1.. if score #vmax bm.rng matches 2.. run function bm:p33/vac/try',
                         'data modify storage bm:tmp vac.c2 append from storage bm:tmp vac.c[0]', 'data remove storage bm:tmp vac.c[0]', 'function bm:p33/vac/merge'])
    fn('p33/vac/try', ['data modify storage bm:tmp vac.a set from storage bm:tmp vac.c[0].item', 'data modify storage bm:tmp vac.a.count set from storage bm:tmp vac.in.count',
                       'execute store success score #vd bm.rng run data modify storage bm:tmp vac.a set from storage bm:tmp vac.in',
                       'execute if score #vd bm.rng matches 1 run return 0',
                       'execute store result score #vc bm.rng run data get storage bm:tmp vac.c[0].item.count',
                       'scoreboard players operation #vsp bm.rng = #vmax bm.rng', 'scoreboard players operation #vsp bm.rng -= #vc bm.rng',
                       'scoreboard players operation #vsp bm.rng < #vn bm.rng', 'execute if score #vsp bm.rng matches ..0 run return 0',
                       'scoreboard players operation #vc bm.rng += #vsp bm.rng', 'scoreboard players operation #vn bm.rng -= #vsp bm.rng',
                       'execute store result storage bm:tmp vac.c[0].item.count int 1 run scoreboard players get #vc bm.rng'])
    fn('p33/vac/newslot', ['scoreboard players set #vf bm.rng -1'] +
       [f'execute if score #vf bm.rng matches -1 unless data storage bm:tmp vac.c2[{{slot:{k}}}] run scoreboard players set #vf bm.rng {k}' for k in range(27)] +
       ['execute if score #vf bm.rng matches -1 run return 0',
        'data modify storage bm:tmp vac.c2 append value {slot:0,item:{}}',
        'execute store result storage bm:tmp vac.c2[-1].slot int 1 run scoreboard players get #vf bm.rng',
        'data modify storage bm:tmp vac.c2[-1].item set from storage bm:tmp vac.in',
        'execute store result storage bm:tmp vac.c2[-1].item.count int 1 run scoreboard players get #vn bm.rng', 'scoreboard players set #vn bm.rng 0'])

    # ------------------------------------------------------------------ hinged shulker boxes
    wjson('bm/item_modifier/p33/hinge.json', [{'function': 'minecraft:set_components', 'components': hold('none')},
                                             {'function': 'minecraft:set_custom_data', 'tag': '{bm_quick:1b}'},
                                             {'function': 'minecraft:set_lore', 'mode': 'append', 'lore': [T('⚿ Void Hinge: sneak + right-click the air to open', '#c08bff')]}])
    G.consume_adv('void_hinge', 'bm:p33/hinge/use')
    fn('p33/hinge/use', ['advancement revoke @s only bm:consume/void_hinge',
                         'execute unless items entity @s weapon.offhand #minecraft:shulker_boxes run return run function bm:p33/hinge/refund',
                         'execute if items entity @s weapon.offhand *[minecraft:custom_data~{bm_quick:1b}] run return run function bm:p33/hinge/refund',
                         'item modify entity @s weapon.offhand bm:p33/hinge', 'playsound minecraft:block.iron_trapdoor.close player @s ~ ~ ~ 1 0.6',
                         title('@s', 'actionbar', T('Hinged! Sneak + right-click the air with that box in hand to open it.', '#c08bff'))])
    fn('p33/hinge/refund', [give('void_hinge'), title('@s', 'actionbar', T('Hold an un-hinged shulker box in your off hand. (Refunded)', 'red'))])
    wjson('bm/advancement/hold/shulker_quick.json', {'criteria': {'use': {'trigger': 'minecraft:using_item', 'conditions': {
        'item': {'items': '#minecraft:shulker_boxes', 'predicates': {'minecraft:custom_data': '{bm_quick:1b}'}}}}},
        'rewards': {'function': 'bm:p33/sbox/use'}})
    fn('p33/sbox/use', ['advancement revoke @s only bm:hold/shulker_quick',
                        'execute store result score #now bm.hnow run time query gametime', 'scoreboard players operation #gap bm.hnow = #now bm.hnow',
                        'scoreboard players operation #gap bm.hnow -= @s bm.huse', 'scoreboard players operation @s bm.huse = #now bm.hnow',
                        'execute if score #gap bm.hnow matches 0..2 run return 0',
                        'execute unless predicate bm:p20/sneaking run return run ' + title('@s', 'actionbar', T('Sneak + right-click to open the box.', 'gray')),
                        'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bm_quick:1b}] run return run function bm:p33/box/open {path:"equipment.mainhand",slot:"weapon.mainhand"}',
                        'function bm:p33/box/open {path:"equipment.offhand",slot:"weapon.offhand"}'])

    # ------------------------------------------------------------------ TOOL FUSION (Xenite Altar, sneak + right-click)
    wjson('bm/tags/item/p33_tools.json', {'values': [f'#minecraft:{t}s' for t in TOOLS]})
    import json
    from paths import MC
    comps = json.load(open(MC + 'item_components.json'))
    inf = G.FUNCS['p24/altar/infuse']
    inf.insert(0, 'execute if items entity @s weapon.mainhand #bm:p33_tools if items entity @s weapon.offhand #bm:p33_tools run return run function bm:p33/fuse/try')
    tryf = ['execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bm_fused:1b}] run return run ' +
            title('@s', 'actionbar', T('That tool already carries two tools\' worth. It can hold no more.', 'gray')),
            'execute unless entity @s[level=8..] run return run ' + title('@s', 'actionbar', T('Fusion costs 8 levels of experience.', 'gray'))]
    for donor in TOOLS:
        for base in TOOLS:
            if base == donor: continue
            tryf.append(f'execute if items entity @s weapon.offhand #minecraft:{donor}s if items entity @s weapon.mainhand #minecraft:{base}s run return run function bm:p33/fuse/{donor}')
    tryf.append(title('@s', 'actionbar', T('Two DIFFERENT tools: the one to keep in your hand, the one to melt in your off hand.', 'gray')))
    fn('p33/fuse/try', tryf)
    for donor in TOOLS:
        body = []
        for tier in TIERS:
            for base in TOOLS:
                bid = f'{tier}_{base}'
                if base == donor or bid not in comps: continue
                rules = list(comps[bid]['minecraft:tool']['rules'])
                speed = next(r['speed'] for r in rules if r.get('correct_for_drops'))
                rules.append({'blocks': f'#minecraft:mineable/{donor}', 'correct_for_drops': True, 'speed': speed})
                tool = dict(comps[bid]['minecraft:tool']); tool['rules'] = rules
                wjson(f'bm/item_modifier/p33/fuse/{bid}_{donor}.json', [
                    {'function': 'minecraft:set_components', 'components': {'minecraft:tool': tool}},
                    {'function': 'minecraft:set_custom_data', 'tag': f'{{bm_fused:1b,bm_fuse:"{donor}"}}'},
                    {'function': 'minecraft:set_lore', 'mode': 'append', 'lore': [T(f'⚒ Fused: also mines like a {donor}', '#6af2ff')]}])
                body.append(f'execute if items entity @s weapon.mainhand minecraft:{bid} run item modify entity @s weapon.mainhand bm:p33/fuse/{bid}_{donor}')
        body.append('execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{bm_fused:1b}] run return run ' + title('@s', 'actionbar', T('The altar cannot read that tool.', 'gray')))
        body.append('function bm:p33/fuse/do')
        fn(f'p33/fuse/{donor}', body)
    fn('p33/fuse/do', ['item replace entity @s weapon.offhand with minecraft:air', 'xp add @s -8 levels',
                       'playsound minecraft:block.anvil.use player @a[distance=..12] ~ ~ ~ 1 0.8', 'playsound minecraft:block.beacon.activate player @a[distance=..12] ~ ~ ~ 1 1.6',
                       'particle minecraft:end_rod ~ ~1.2 ~ 0.3 0.4 0.3 0.06 30',
                       title('@s', 'actionbar', T('Fused! The tool in your hand learned a new trade.', '#6af2ff'))])
    G.FUNCS['p24/altar/help'].append(tellraw('@s', [T('Tool fusion: ', '#6af2ff', bold=True), T('sneak + right-click with a tool in your hand and a different tool in your off hand (8 levels). Two capabilities at most.', 'gray')]))
    # restamps (phase18) rewrite Black Market tools: put their fusion back afterwards
    rsl = G.FUNCS['p18/refresh/slot']
    k = next(i for i, l in enumerate(rsl) if 'rf.iid set from entity' in l)
    rsl[k + 1:k + 1] = ['$data modify storage bm:tmp rf.fuse set from entity @s $(path).components."minecraft:custom_data".bm_fuse']
    for donor in TOOLS:
        rsl.append(f'execute if data storage bm:tmp rf.iid if data storage bm:tmp {{rf:{{fuse:"{donor}"}}}} run function bm:p33/fuse/re_{donor} with storage bm:tmp rf')
        lines = []
        for tier in TIERS:
            for base in TOOLS:
                bid = f'{tier}_{base}'
                if base != donor and bid in comps:
                    lines.append(f'$execute if items entity @s $(slot) minecraft:{bid} run item modify entity @s $(slot) bm:p33/fuse/{bid}_{donor}')
        fn(f'p33/fuse/re_{donor}', lines)

    # ------------------------------------------------------------------ DIMENSION SHIFTER
    MENU_SHIFT = 900
    P28.MENU['shift'] = MENU_SHIFT
    dlg = P28.multi([T('Dimension Shifter', '#b48cff', bold=True)],
                    [P28.body([T('Pick a dimension. You arrive somewhere safe. (Never the Hollow Throne.)', 'gray')])],
                    [P28.btn(T('The Overworld', 'green'), 7001, width=200), P28.btn(T('The Nether', 'red'), 7002, width=200),
                     P28.btn(T('The End', 'light_purple'), 7003, width=200)], columns=1)
    fn('p33/shift/use', ['execute if entity @s[tag=bm.adv] run return run ' + title('@s', 'actionbar', T('The Shifter refuses to work in a place like this.', 'gray')),
                         'execute if score @s bm.shcd matches 1.. run return run ' + title('@s', 'actionbar', [T('Recharging: ', 'gray'), {'score': {'name': '@s', 'objective': 'bm.shcd'}, 'color': 'white'}, T(' s', 'gray')]),
                         f'scoreboard players set @s bm.menu {MENU_SHIFT}', f'dialog show @s {P28.inline(dlg)}'])
    G.FUNCS['p28/act'].append('execute if score #act bm.pay matches 7001..7003 run return run function bm:p33/shift/act')
    fn('p33/shift/act', [f'execute unless score @s bm.menu matches {MENU_SHIFT} run return run function bm:p28/stale',
                         f'execute unless items entity @s container.* {holds % "dimension_shifter"} unless items entity @s weapon.offhand {holds % "dimension_shifter"} run return run function bm:p28/stale',
                         'execute if entity @s[tag=bm.adv] run return run function bm:p28/stale',
                         'execute if score @s bm.shcd matches 1.. run return run function bm:p28/stale',
                         'execute if score #act bm.pay matches 7001 if dimension minecraft:overworld run return run ' + title('@s', 'actionbar', T('You are already in the Overworld.', 'gray')),
                         'execute if score #act bm.pay matches 7002 if dimension minecraft:the_nether run return run ' + title('@s', 'actionbar', T('You are already in the Nether.', 'gray')),
                         'execute if score #act bm.pay matches 7003 if dimension minecraft:the_end run return run ' + title('@s', 'actionbar', T('You are already in the End.', 'gray')),
                         'scoreboard players set @s bm.shcd 30', 'particle minecraft:reverse_portal ~ ~1 ~ 0.4 0.9 0.4 0.1 80',
                         'playsound minecraft:block.portal.travel player @s ~ ~ ~ 0.4 1.6',
                         'execute store result score #sx bm.rng run data get entity @s Pos[0]', 'execute store result score #sz bm.rng run data get entity @s Pos[2]',
                         'execute if score #act bm.pay matches 7001 run function bm:p33/shift/to_ow',
                         'execute if score #act bm.pay matches 7002 run function bm:p33/shift/to_nether',
                         'execute if score #act bm.pay matches 7003 run function bm:p33/shift/to_end',
                         'effect give @s minecraft:darkness 2 0 true', 'effect give @s minecraft:resistance 5 4 true', 'effect give @s minecraft:slow_falling 5 0 true',
                         'scoreboard players set @s bm.menu 0'])
    load += ['scoreboard players set #8 bm.rng 8']
    fn('p33/shift/to_ow', ['execute if dimension minecraft:the_nether run scoreboard players operation #sx bm.rng *= #8 bm.rng',
                           'execute if dimension minecraft:the_nether run scoreboard players operation #sz bm.rng *= #8 bm.rng',
                           'execute unless dimension minecraft:the_nether run scoreboard players set #sx bm.rng 0',
                           'execute unless dimension minecraft:the_nether run scoreboard players set #sz bm.rng 0',
                           'execute store result storage bm:tmp sh.x int 1 run scoreboard players get #sx bm.rng',
                           'execute store result storage bm:tmp sh.z int 1 run scoreboard players get #sz bm.rng',
                           'function bm:p33/shift/ow with storage bm:tmp sh'])
    fn('p33/shift/ow', ['$execute in minecraft:overworld run spreadplayers $(x) $(z) 0 12 false @s'])
    fn('p33/shift/to_nether', ['execute if dimension minecraft:overworld run scoreboard players operation #sx bm.rng /= #8 bm.rng',
                               'execute if dimension minecraft:overworld run scoreboard players operation #sz bm.rng /= #8 bm.rng',
                               'execute unless dimension minecraft:overworld run scoreboard players set #sx bm.rng 0',
                               'execute unless dimension minecraft:overworld run scoreboard players set #sz bm.rng 0',
                               'execute store result storage bm:tmp sh.x int 1 run scoreboard players get #sx bm.rng',
                               'execute store result storage bm:tmp sh.z int 1 run scoreboard players get #sz bm.rng',
                               'function bm:p33/shift/nether with storage bm:tmp sh'])
    fn('p33/shift/nether', ['$execute in minecraft:the_nether run spreadplayers $(x) $(z) 0 24 under 118 false @s'])
    # the End: the obsidian platform at (100, 48, 0) is built (or rebuilt) under you the tick you arrive
    fn('p33/shift/to_end', ['execute in minecraft:the_end run tp @s 100.5 49 0.5 -90 0', 'tag @s add bm.endplat'])
    tick.append('execute as @a[tag=bm.endplat] at @s if dimension minecraft:the_end run function bm:p33/shift/platform')
    fn('p33/shift/platform', ['tag @s remove bm.endplat', 'fill 98 48 -2 102 48 2 minecraft:obsidian', 'fill 98 49 -2 102 51 2 minecraft:air',
                              'tp @s 100.5 49 0.5'])
    second.append('scoreboard players remove @a[scores={bm.shcd=1..}] bm.shcd 1')

    # ------------------------------------------------------------------ JUMP BOOTS (the jump uses the real jump_strength attribute)
    def jump_lines(kind):
        return f'execute as @a[gamemode=!spectator] if items entity @s armor.feet *[minecraft:custom_data~{{bm:"{kind}_boots"}}] at @s run function bm:p33/{kind}/tick'
    tick += [jump_lines('triple'), jump_lines('spring'),
             'execute as @a[scores={bm.tjm=1..}] unless items entity @s armor.feet *[minecraft:custom_data~{bm:"triple_boots"}] run function bm:p33/triple/clear',
             'execute as @a[scores={bm.cjm=1..}] unless items entity @s armor.feet *[minecraft:custom_data~{bm:"spring_boots"}] run function bm:p33/spring/clear',
             'scoreboard players reset @a bm.jumps']
    fn('p33/triple/tick', ['execute if score @s bm.jumps matches 1.. run function bm:p33/triple/jumped',
                           'execute if predicate bm:p21/airborne run return run scoreboard players set @s bm.tjg 0',
                           'scoreboard players add @s bm.tjg 1',
                           'execute if score @s bm.tjg matches 9.. if score @s bm.tjc matches 1.. run function bm:p33/triple/reset',
                           'execute if score @s bm.tjg matches 1 if score @s bm.tjc matches 1 run function bm:p33/triple/set {lv:1}',
                           'execute if score @s bm.tjg matches 1 if score @s bm.tjc matches 2 run function bm:p33/triple/set {lv:2}'])
    fn('p33/triple/jumped', ['scoreboard players add @s bm.tjc 1',
                             'execute if score @s bm.tjc matches 2 run playsound minecraft:entity.player.attack.sweep player @a[distance=..12] ~ ~ ~ 0.5 1.6',
                             'execute if score @s bm.tjc matches 3.. run function bm:p33/triple/big', 'function bm:p33/triple/clear'])
    fn('p33/triple/big', ['scoreboard players set @s bm.tjc 0', 'particle minecraft:firework ~ ~0.2 ~ 0.3 0 0.3 0.05 20',
                          'playsound minecraft:entity.firework_rocket.launch player @a[distance=..16] ~ ~ ~ 0.8 1.8', title('@s', 'actionbar', T('Wa-hoo!', '#ff5555', bold=True))])
    fn('p33/triple/reset', ['scoreboard players set @s bm.tjc 0', 'function bm:p33/triple/clear'])
    fn('p33/triple/clear', ['attribute @s minecraft:jump_strength modifier remove bm:triple', 'scoreboard players set @s bm.tjm 0'])
    tj = JUMP['triple']
    fn('p33/triple/set', ['attribute @s minecraft:jump_strength modifier remove bm:triple', '$scoreboard players set @s bm.tjm $(lv)',
                          f'execute if score @s bm.tjm matches 1 run attribute @s minecraft:jump_strength modifier add bm:triple {tj[0] - 0.42:.3f} add_value',
                          f'execute if score @s bm.tjm matches 2 run attribute @s minecraft:jump_strength modifier add bm:triple {tj[1] - 0.42:.3f} add_value'])
    cj = JUMP['charge']
    fn('p33/spring/tick', ['execute if score @s bm.jumps matches 1.. run return run function bm:p33/spring/jumped',
                           'execute if predicate bm:p21/airborne run return 0',
                           'execute if predicate bm:p20/sneaking run scoreboard players add @s bm.cjc 1',
                           'execute if predicate bm:p20/sneaking run scoreboard players set @s bm.cjg 0',
                           'execute unless predicate bm:p20/sneaking run scoreboard players add @s bm.cjg 1',
                           'execute if score @s bm.cjg matches 16.. if score @s bm.cjc matches 1.. run function bm:p33/spring/clear',
                           'execute if score @s bm.cjc matches 41.. run scoreboard players set @s bm.cjc 40',
                           'execute if score @s bm.cjc matches 8 run function bm:p33/spring/lv {lv:1}', 'execute if score @s bm.cjc matches 18 run function bm:p33/spring/lv {lv:2}',
                           'execute if score @s bm.cjc matches 28 run function bm:p33/spring/lv {lv:3}', 'execute if score @s bm.cjc matches 38 run function bm:p33/spring/lv {lv:4}',
                           'execute if score @s bm.cjc matches 8.. run particle minecraft:electric_spark ~ ~0.1 ~ 0.25 0 0.25 0 1'])
    lv = ['attribute @s minecraft:jump_strength modifier remove bm:spring', '$scoreboard players set @s bm.cjm $(lv)']
    for i, v in enumerate(cj, 1):
        lv.append(f'execute if score @s bm.cjm matches {i} run attribute @s minecraft:jump_strength modifier add bm:spring {v - 0.42:.3f} add_value')
    lv += ['playsound minecraft:block.note_block.hat player @s ~ ~ ~ 0.8 1', 'execute if score @s bm.cjm matches 4 run playsound minecraft:block.note_block.pling player @s ~ ~ ~ 0.8 1.6',
           title('@s', 'actionbar', [T('Spring charge: ', '#6af2ff'), {'score': {'name': '@s', 'objective': 'bm.cjm'}, 'color': 'white'}, T(' / 4', '#6af2ff')])]
    fn('p33/spring/lv', lv)
    fn('p33/spring/jumped', ['execute if score @s bm.cjm matches 1.. run particle minecraft:cloud ~ ~0.1 ~ 0.3 0 0.3 0.05 14',
                             'execute if score @s bm.cjm matches 1.. run playsound minecraft:block.piston.extend player @a[distance=..16] ~ ~ ~ 0.8 1.4',
                             'function bm:p33/spring/clear'])
    fn('p33/spring/clear', ['attribute @s minecraft:jump_strength modifier remove bm:spring', 'scoreboard players set @s bm.cjm 0', 'scoreboard players set @s bm.cjc 0',
                            'scoreboard players set @s bm.cjg 0'])

    # ------------------------------------------------------------------ ROCKET BOOTS kick harder (about 15 blocks a burst)
    rb = G.FUNCS['p26/rocket/boost']
    G.FUNCS['p26/rocket/boost'] = [l.replace('minecraft:levitation 1 26 true', 'minecraft:levitation 1 42 true') for l in rb]
    assert any('levitation 1 42' in l for l in G.FUNCS['p26/rocket/boost'])

    # ------------------------------------------------------------------ VOID TOTEM
    vt = '*[minecraft:custom_data~{bm:"void_totem"}]'
    second += ['execute as @a[gamemode=!spectator] at @s unless predicate bm:p21/airborne if function bm:p33/void/safe run function bm:p33/void/remember']
    fn('p33/void/safe', ['execute unless block ~ ~-0.5 ~ #minecraft:air unless block ~ ~-0.5 ~ minecraft:lava unless block ~ ~ ~ minecraft:lava run return 1', 'return 0'])
    fn('p33/void/remember', ['execute store result score @s bm.vx run data get entity @s Pos[0]', 'execute store result score @s bm.vy run data get entity @s Pos[1]',
                             'execute store result score @s bm.vz run data get entity @s Pos[2]', 'scoreboard players set @s bm.vd 0',
                             'execute if dimension minecraft:the_nether run scoreboard players set @s bm.vd 1', 'execute if dimension minecraft:the_end run scoreboard players set @s bm.vd 2',
                             'execute if dimension bm:hollow_throne run scoreboard players set @s bm.vd 3', 'scoreboard players set @s bm.vok 1'])
    # void damage starts 64 below a dimension's floor: y -128 in the Overworld, -64 in the Nether, the End and the Hollow Throne
    tick += ['execute as @a[gamemode=!spectator,gamemode=!creative] at @s if dimension minecraft:overworld if entity @s[y=-2000,dy=1872] if function bm:p33/void/has run function bm:p33/void/save',
             'execute as @a[gamemode=!spectator,gamemode=!creative] at @s unless dimension minecraft:overworld if entity @s[y=-2000,dy=1936] if function bm:p33/void/has run function bm:p33/void/save']
    fn('p33/void/has', [f'execute if items entity @s container.* {vt} run return 1', f'execute if items entity @s weapon.offhand {vt} run return 1', 'return 0'])
    fn('p33/void/save', ['clear @s ' + vt + ' 1',
                         'execute unless score @s bm.vok matches 1 run return run function bm:p33/void/fallback',
                         'execute store result storage bm:tmp vs.x int 1 run scoreboard players get @s bm.vx', 'execute store result storage bm:tmp vs.y int 1 run scoreboard players get @s bm.vy',
                         'execute store result storage bm:tmp vs.z int 1 run scoreboard players get @s bm.vz',
                         'data modify storage bm:tmp vs.d set value "minecraft:overworld"',
                         'execute if score @s bm.vd matches 1 run data modify storage bm:tmp vs.d set value "minecraft:the_nether"',
                         'execute if score @s bm.vd matches 2 run data modify storage bm:tmp vs.d set value "minecraft:the_end"',
                         'execute if score @s bm.vd matches 3 run data modify storage bm:tmp vs.d set value "bm:hollow_throne"',
                         'function bm:p33/void/tp with storage bm:tmp vs', 'function bm:p33/void/fx'])
    fn('p33/void/tp', ['$execute in $(d) run tp @s $(x).5 $(y) $(z).5'])
    fn('p33/void/fallback', ['execute if dimension minecraft:the_end run function bm:p33/shift/to_end',
                             'execute unless dimension minecraft:the_end in minecraft:overworld run spreadplayers 0 0 0 16 false @s', 'function bm:p33/void/fx'])
    fn('p33/void/fx', ['effect give @s minecraft:slow_falling 6 0 true', 'effect give @s minecraft:resistance 4 4 true',
                       'particle minecraft:reverse_portal ~ ~1 ~ 0.4 0.9 0.4 0.1 80', 'playsound minecraft:item.totem.use player @s ~ ~ ~ 0.8 1.4',
                       'title @s times 5 40 10', title('@s', 'subtitle', T('The Void Totem shatters and pulls you back.', '#b05cff', italic=True)),
                       title('@s', 'title', T('Saved!', '#b05cff', bold=True))])

    # ------------------------------------------------------------------ EXPERIENCE FLASK
    load += ['scoreboard players set #2 bm.xpn 2', 'scoreboard players set #6 bm.xpn 6', 'scoreboard players set #81 bm.xpn 81', 'scoreboard players set #720 bm.xpn 720',
             'scoreboard players set #325 bm.xpn 325', 'scoreboard players set #4440 bm.xpn 4440']
    fn('p33/xp/use', hand('xp_flask') + [
        'execute if score #hand bm.rng matches 1 run data modify storage bm:tmp xp.slot set value "weapon.mainhand"',
        'execute if score #hand bm.rng matches 2 run data modify storage bm:tmp xp.slot set value "weapon.offhand"',
        'execute if score #hand bm.rng matches 1 store result score #st bm.xpn run data get entity @s equipment.mainhand.components."minecraft:custom_data".bm_xp',
        'execute if score #hand bm.rng matches 2 store result score #st bm.xpn run data get entity @s equipment.offhand.components."minecraft:custom_data".bm_xp',
        'execute if predicate bm:p20/sneaking run return run function bm:p33/xp/drink', 'function bm:p33/xp/pour'])
    # total points of a level L: L<=16: L^2+6L; L<=31: (5L^2-81L+720)/2; else (9L^2-325L+4440)/2 - plus the bar's progress
    fn('p33/xp/total', ['execute store result score #L bm.xpn run experience query @s levels', 'execute store result score #p bm.xpn run experience query @s points',
                        'scoreboard players operation #t bm.xpn = #L bm.xpn', 'scoreboard players operation #t bm.xpn *= #L bm.xpn',
                        'execute if score #L bm.xpn matches ..16 run scoreboard players operation #a bm.xpn = #L bm.xpn',
                        'execute if score #L bm.xpn matches ..16 run scoreboard players operation #a bm.xpn *= #6 bm.xpn',
                        'execute if score #L bm.xpn matches ..16 run scoreboard players operation #t bm.xpn += #a bm.xpn',
                        'execute if score #L bm.xpn matches 17..31 run function bm:p33/xp/mid', 'execute if score #L bm.xpn matches 32.. run function bm:p33/xp/high',
                        'scoreboard players operation #t bm.xpn += #p bm.xpn'])
    fn('p33/xp/mid', ['scoreboard players set #k bm.xpn 5', 'scoreboard players operation #t bm.xpn *= #k bm.xpn',
                      'scoreboard players operation #a bm.xpn = #L bm.xpn', 'scoreboard players operation #a bm.xpn *= #81 bm.xpn',
                      'scoreboard players operation #t bm.xpn -= #a bm.xpn', 'scoreboard players operation #t bm.xpn += #720 bm.xpn', 'scoreboard players operation #t bm.xpn /= #2 bm.xpn'])
    fn('p33/xp/high', ['scoreboard players set #k bm.xpn 9', 'scoreboard players operation #t bm.xpn *= #k bm.xpn',
                       'scoreboard players operation #a bm.xpn = #L bm.xpn', 'scoreboard players operation #a bm.xpn *= #325 bm.xpn',
                       'scoreboard players operation #t bm.xpn -= #a bm.xpn', 'scoreboard players operation #t bm.xpn += #4440 bm.xpn', 'scoreboard players operation #t bm.xpn /= #2 bm.xpn'])
    fn('p33/xp/pour', ['function bm:p33/xp/total', 'execute if score #t bm.xpn matches ..0 run return run ' + title('@s', 'actionbar', T('You have no experience to pour in.', 'gray')),
                       'scoreboard players operation #st bm.xpn += #t bm.xpn', 'execute if score #st bm.xpn matches 2000000.. run scoreboard players set #st bm.xpn 2000000',
                       'experience set @s 0 levels', 'experience set @s 0 points', 'function bm:p33/xp/write',
                       'playsound minecraft:item.bottle.fill player @s ~ ~ ~ 1 0.8', 'playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.6 0.6'])
    fn('p33/xp/drink', ['execute if score #st bm.xpn matches ..0 run return run ' + title('@s', 'actionbar', T('The flask is empty.', 'gray')),
                        'execute store result storage bm:tmp xp.n int 1 run scoreboard players get #st bm.xpn', 'function bm:p33/xp/give with storage bm:tmp xp',
                        'scoreboard players set #st bm.xpn 0', 'function bm:p33/xp/write',
                        'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.8 1.2', 'playsound minecraft:entity.generic.drink player @s ~ ~ ~ 1 1'])
    fn('p33/xp/give', ['$experience add @s $(n) points'])
    fn('p33/xp/write', ['execute store result storage bm:tmp xp.n int 1 run scoreboard players get #st bm.xpn', 'function bm:p33/xp/stamp with storage bm:tmp xp',
                        title('@s', 'actionbar', [T('Experience Flask: ', '#7cff4a'), {'score': {'name': '#st', 'objective': 'bm.xpn'}, 'color': 'white'}, T(' XP stored', '#7cff4a')])])
    base_lore = [l for l in ITEMS['xp_flask']['comps']['minecraft:lore'] if 'Stored' not in l.get('text', '')]
    stamp_lore = snbt(base_lore[:-1]).rstrip(']') + ',{text:"Stored: $(n) XP",color:"green",italic:0b},' + snbt(base_lore[-1]) + ']'
    fn('p33/xp/stamp', ['$item modify entity @s $(slot) {function:"minecraft:sequence",functions:[{function:"minecraft:set_custom_data",tag:{bm_xp:$(n)}},{function:"minecraft:set_lore",mode:"replace_all",lore:' + stamp_lore + '}]}'])

    # ------------------------------------------------------------------ KILLS: Vampire Lord set (2 hearts) / Sanguine Fang (half a heart)
    wjson('bm/advancement/p33/kill.json', {'criteria': {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {
        'entity': [{'condition': 'minecraft:inverted', 'term': {'condition': 'minecraft:entity_properties', 'entity': 'this',
                                                                'predicate': {'minecraft:entity_type': 'minecraft:player'}}}]}}},
        'rewards': {'function': 'bm:p33/kill'}})
    fn('p33/kill', ['advancement revoke @s only bm:p33/kill',
                    'execute if function bm:sets/has/vampire run return run function bm:p33/leech {n:2}',
                    'execute if items entity @s weapon.offhand *[minecraft:custom_data~{bm:"sanguine_fang"}] run function bm:p33/leech {n:1}'])
    fn('p33/leech', ['$scoreboard players set #lh bm.rng $(n)',
                     'execute if score #lh bm.rng matches 2 run effect give @s minecraft:instant_health 1 0 true',
                     'execute if score #lh bm.rng matches 1 run effect give @s minecraft:regeneration 1 2 true',
                     'particle minecraft:dust{color:[0.6,0.0,0.05],scale:1.2} ~ ~1 ~ 0.4 0.6 0.4 0 10',
                     'playsound minecraft:entity.generic.drink player @s ~ ~ ~ 0.4 0.6'])
    # the old on-hit drain is retired (it healed on hits, on a 2 s cooldown); the set's lore now says "per kill"
    G.FUNCS['sets/vampire_drain'] = ['return 0']

    # ------------------------------------------------------------------ the Rat Bank keeps every currency (phase31 lays the dialog out from BANK)
    load += [f'scoreboard objectives add {obj} dummy' for (_, obj, _, _) in BANK_EXTRA]

    G.FUNCS['load'][-1:-1] = load
    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


# ===================================================================== resource pack
def rp(R):
    grid = R.grid
    I = {}
    I['vacuum_satchel'] = grid([
        '................', '.....KKKKKK.....', '....K......K....', '...KBBBBBBBBK...', '..KBBBBBBBBBBK..', '..KBLLLLLLLLBK..',
        '..KBBBBGGBBBBK..', '..KBBBGKKGBBBK..', '..KBBBGKKGBBBK..', '..KBBBBGGBBBBK..', '..KBBBBBBBBBBK..', '..KBBBBBBBBBBK..',
        '...KKKKKKKKKK...', '................', '................', '................'], dict(K='#3a2a1a', B='#c8a050', L='#e8c870', G='#8a8a96'))
    I['vacuum_satchel_on'] = grid([
        '.......Y........', '.....KKKKKK..Y..', '..Y.K......K....', '...KBBBBBBBBK...', '..KBBBBBBBBBBK..', '..KBLLLLLLLLBK..',
        '..KBBBBGGBBBBK..', '..KBBBGYYGBBBK..', '..KBBBGYYGBBBK..', '..KBBBBGGBBBBK..', '..KBBBBBBBBBBK..', '..KBBBBBBBBBBK..',
        '...KKKKKKKKKK...', '................', '................', '................'], dict(K='#3a2a1a', B='#c8a050', L='#e8c870', G='#8a8a96', Y='#fff27a'))
    I['dimension_shifter'] = grid([
        '................', '......SSSS......', '....SSPPPPSS....', '...SPPVVVVPPS...', '...SPVVKKVVPS...', '..SPVVKLLKVVPS..',
        '..SPVKLWWLKVPS..', '..SPVKLWWLKVPS..', '..SPVVKLLKVVPS..', '...SPVVKKVVPS...', '...SPPVVVVPPS...', '....SSPPPPSS....',
        '......SSSS......', '................', '................', '................'], dict(S='#b8bec8', P='#8a5ad8', V='#b48cff', K='#2a1a4a', L='#e0d0ff', W='#ffffff'))
    boots = lambda m, a: grid([
        '................', '................', '....MMM..MMM....', '....MAM..MAM....', '....MAM..MAM....', '....MAM..MAM....',
        '....MAM..MAM....', '....MAMM.MAMM...', '...MAAAM.MAAAM..', '..MAAAAMMAAAAM..', '..MMMMMMMMMMMM..', '...KK..KK.KK....',
        '..K..K....K.K...', '................', '................', '................'], dict(M=m, A=a, K='#3a3f4a'))
    I['triple_boots'] = boots('#b8bec8', '#ff5555')
    I['spring_boots'] = boots('#b8bec8', '#6af2ff')
    I['void_totem'] = grid([
        '................', '......PPPP......', '.....PKKKKP.....', '.....PKVVKP.....', '.....PPPPPP.....', '....PPVVVVPP....',
        '...PPVVLLVVPP...', '...PPVVLLVVPP...', '....PPVVVVPP....', '.....PPVVPP.....', '.....PPPPPP.....', '......PVVP......',
        '......PPPP......', '................', '................', '................'], dict(P='#5a2a8a', K='#1a0a2a', V='#b05cff', L='#f0dcff'))
    I['xp_flask'] = grid([
        '................', '......KKKK......', '......KCCK......', '.......GG.......', '......G..G......', '.....G....G.....',
        '....G.LLLL.G....', '....GLLYYLLG....', '....GLYYYYLG....', '....GLLYYLLG....', '....GLLLLLLG....', '.....GLLLLG.....',
        '......GGGG......', '................', '................', '................'], dict(K='#5a3a1a', C='#a87a4a', G='#c8f0ff', L='#7cff4a', Y='#e8ff8a'))
    I['pocket_ender_chest'] = grid([
        '................', '................', '...KKKKKKKKKK...', '..KDDDDDDDDDDK..', '..KDCCCCCCCCDK..', '..KDCCCCCCCCDK..',
        '..KKKKKGGKKKKK..', '..KDDDDGGDDDDK..', '..KDCCCCCCCCDK..', '..KDCCCCCCCCDK..', '..KDDDDDDDDDDK..', '...KKKKKKKKKK...',
        '................', '................', '................', '................'], dict(K='#0a1a1a', D='#1a3a3a', C='#2f8a7a', G='#a0f0d0'))
    I['void_hinge'] = grid([
        '................', '....SSSS........', '...SKKKKS.......', '...SK..KS.......', '...SKKKKSSSSSS..', '...SSSSSSVVVVS..',
        '........SVVVVS..', '........SVVVVS..', '...SSSSSSVVVVS..', '...SKKKKSSSSSS..', '...SK..KS.......', '...SKKKKS.......',
        '....SSSS........', '................', '................', '................'], dict(S='#8a8f98', K='#3a3f4a', V='#c08bff'))
    I['sanguine_fang'] = grid([
        '................', '................', '.....WWWWW......', '....WWWWWWW.....', '....WWWWWWW.....', '.....WWWWW......',
        '.....WWWWR......', '......WWWR......', '......WWRR......', '.......WRR......', '.......RR.......', '........R.......',
        '........R.......', '................', '................', '................'], dict(W='#f0e8d8', R='#b0002a'))
    for k, v in I.items(): R.ICONS[k] = v

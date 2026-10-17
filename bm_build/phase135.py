"""Phase 135 (2.77c): weapons on the wall. Tullius's blunderbuss and harpoon, Democratus' scythe and both of KillerWatt's tendril
sets hang on a wall: sneak + use one on a wall and it hangs there on a small wooden plaque - the very weapon (its name, its
enchantments, all of it) kept in the display. Sneak + punch it to take it down again (only whoever hung it). If the wall goes,
the weapon drops; it is never lost.

The blunderbuss and the harpoon hang only when no monster is near (in a fight, sneak + use is still a shot, or a throw). The scythe
gains a use for it. The tendrils' use still puts them on, as before - a hold item can't use the vanilla swap, so the use does the
swap itself.

Importing registers the use handlers and the lore; generate(G) runs after phase132 (whose blunderbuss use it extends)."""
from items import ITEMS, T
from useitem import hold, HOLD
from nbt import snbt, B, F, Int

# (each weapon laid flat on the wall, tilted, centred on its plaque, its back just off it - worked out from the models' boxes in
#  an item display's frame (it shows its model turned half round): left rotation, scale, translation. Previewed with tools/render.py)
XF = {'gun': ((-0.2126, 0.6744, 0.2126, 0.6744), 0.7115, (-0.1705, -0.0935, 0.1902)),
      'harpoon': ((-0.2126, 0.6744, 0.2126, 0.6744), 0.7982, (-0.3137, -0.1392, 0.1716)),
      'scythe': ((0.0, 0.0, -0.2419, 0.9703), 0.5950, (0.0754, -0.2486, 0.1230)),
      'tendrils': ((0.0, 0.0, 0.0, 1.0), 1.0283, (0.0, -0.1001, 0.2178)),
      # 2.78 (each model's long axis up the plaque's diagonal, its thin side to the wall, its back just off the board - the same sums,
      #  tools/mount_xf.py): Cecil's staff, Leo's trident (his own model now), Apophiss's mace (its horns flat to the
      #  wall), the Frisbee Shield, and every flat-art weapon (a sprite turned to face out, its blade up the diagonal)
      'staff': ((0.3827, 0.9239, 0.0, 0.0), 0.5594, (0.1098, 0.1098, 0.212)),
      'letri': ((0.3827, 0.9239, 0.0, 0.0), 0.5517, (-0.1365, -0.1365, 0.0934)),
      'apomace': ((-0.2706, -0.6533, -0.2706, 0.6533), 0.5379, (0.1423, 0.1423, 0.265)),
      'frisbee': ((0.2706, 0.6533, 0.6533, 0.2706), 0.62, (0.0, 0.0, 0.0991)),
      'sprite': ((0.0, 1.0, 0.0, 0.0), 0.74, (0.0, 0.0, 0.095))}
KIND = {'tul_blunderbuss': 'gun', 'tul_harpoon': 'harpoon', 'demo_scythe': 'scythe', 'killerwatt_tendrils': 'tendrils', 'ethereal_tendrils': 'tendrils'}
PLAQUE = {'gun': 0.62, 'harpoon': 0.62, 'scythe': 0.62, 'tendrils': 0.8}
DROP, DOBJ = {}, {}


def setup():
    """2.78: run once every item is registered (the Phase 2 ones too) - before the item tables are written"""
    # (2.80: once only - gen_dp is imported a second time under its own name (phase145 takes `offer` from it), which ran this
    #  again and doubled every hung weapon's "hang it there" line)
    if getattr(setup, 'done', False):
        return
    setup.done = True
    # 2.78: hung by sneak + drop (Q) facing a wall - every weapon has a drop, not all of them a use (a sword's right-click does nothing,
    # a trident's or a shield's is its own). If there's no wall, it simply drops.
    DROP.update({'cecil_staff': 'staff', 'leo_trident': 'letri', 'leo_spear': 'letri', 'apo_mace': 'apomace', 'frisbee_shield': 'frisbee'})
    DROP.update({k: 'apomace' for k in ITEMS if k.startswith('apo_mace_')})        # (2.80: the Serpent King's Mace's other forms)
    for _i in ('ray_gun', 'plasma_blaster', 'shrink_ray', 'growth_ray', 'tractor_beam', 'levitation_wand', 'vorn_drill', 'crescent_staff',
               'gravewell_staff', 'staff_of_sparks', 'golden_spear', 'treasurers_scepter', 'blue_marlin', 'enchanted_sword', 'gutter_cutlass',
               'heisters_shiv', 'quake_maul', 'sepulchre', 'thirsting_blade', 'vault_breaker'):
        DROP[_i] = 'sprite'
    KIND.update(DROP)
    PLAQUE.update({'gun': 0.62, 'harpoon': 0.62, 'scythe': 0.62, 'tendrils': 0.8, 'staff': 0.62, 'letri': 0.62, 'apomace': 0.62, 'frisbee': 0.62, 'sprite': 0.62})
    for _i in DROP:
        _b = ITEMS[_i]['base'].split(':')[-1]
        DOBJ.setdefault(_b, f'bm.mtq_{_b}')
    # (Leo's trident, both forms, wears the model he carries - not a vanilla trident's)
    for _i in ('leo_trident', 'leo_spear'):
        ITEMS[_i]['comps']['minecraft:item_model'] = 'bm:leo_trident'
    for _i in DROP:
        _L = ITEMS[_i]['comps']['minecraft:lore']
        _k = len(_L) - 1
        if _k > 0 and str(_L[_k - 1].get('text', '')).startswith('✦'): _k -= 1
        _L.insert(_k, T('Sneak + drop (Q) facing a wall: hang it there.', 'gray'))


CHEST = ('killerwatt_tendrils', 'ethereal_tendrils')
NEAR = 'entity @e[type=#bm:hostile,tag=!bm.npc,distance=..8]'
holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'

for _i in KIND:
    if _i in DROP: continue
    _L = ITEMS[_i]['comps']['minecraft:lore']
    _k = len(_L) - 1
    if _k > 0 and str(_L[_k - 1].get('text', '')).startswith('✦'): _k -= 1
    _L.insert(_k, T('Sneak + use on a wall: hang it there.' + (' (No monsters near.)' if KIND[_i] in ('gun', 'harpoon') else ''), 'gray'))
for _i in ('demo_scythe',) + CHEST:
    ITEMS[_i]['comps'].update(hold('none'))
HOLD['demo_scythe'] = 'bm:p135/scythe'
HOLD['tul_harpoon'] = 'bm:p135/harpoon'
for _i in CHEST:
    HOLD[_i] = 'bm:p135/tendrils'


def generate(G):
    fn, title = G.fn, G.title
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    loud = lambda txt: f'execute if score #mtl bm.rng matches 1 run ' + say(txt)
    second = []

    # ---- the uses: the blunderbuss and the harpoon only when no monster is near, and silently (else a shot, a throw); the scythe
    #      says why not; the tendrils go on instead
    G.FUNCS['p132/gun/use'].insert(0, f'execute if predicate bm:p20/sneaking unless {NEAR} if function bm:p135/try run return 0')
    G.FUNCS['p132/gun/use'].insert(0, 'scoreboard players set #mtl bm.rng 0')
    fn('p135/harpoon', ['scoreboard players set #mtl bm.rng 0', f'execute if predicate bm:p20/sneaking unless {NEAR} run function bm:p135/try'])
    fn('p135/scythe', ['execute unless predicate bm:p20/sneaking run return run ' + say('Sneak + use on a wall: hang it there.'),
                       'scoreboard players set #mtl bm.rng 1', 'function bm:p135/try'])
    tmp = '@e[type=minecraft:item_display,tag=bm.mttmp,distance=..2,limit=1]'
    fn('p135/tendrils', ['scoreboard players set #mtl bm.rng 0', 'execute if predicate bm:p20/sneaking if function bm:p135/try run return 0',
                         'execute unless entity @s[gamemode=creative] if items entity @s armor.chest *[minecraft:enchantments~[{enchantments:"minecraft:binding_curse"}]] '
                         'run return run ' + say("Whatever you're wearing won't come off."),
                         'scoreboard players set #mth bm.rng 2'] +
       [f'execute if items entity @s weapon.mainhand {holds(i)} run scoreboard players set #mth bm.rng 1' for i in CHEST] +
       ['summon minecraft:item_display ~ ~ ~ {Tags:["bm.mttmp"]}', f'item replace entity {tmp} contents from entity @s armor.chest',
        'execute if score #mth bm.rng matches 1 run function bm:p135/wear_main', 'execute if score #mth bm.rng matches 2 run function bm:p135/wear_off',
        f'kill {tmp}', 'playsound minecraft:item.armor.equip_chain player @a[distance=..16] ~ ~ ~ 1 1'])
    fn('p135/wear_main', ['item replace entity @s armor.chest from entity @s weapon.mainhand', f'item replace entity @s weapon.mainhand from entity {tmp} contents'])
    fn('p135/wear_off', ['item replace entity @s armor.chest from entity @s weapon.offhand', f'item replace entity @s weapon.offhand from entity {tmp} contents'])

    # ---- try: which weapon, in which hand; a wall in front within 3 blocks, room before it - then it hangs (1), or not (0)
    kinds = list(XF)
    pick = []
    for i, k in KIND.items():
        if i in DROP: continue
        n = kinds.index(k) + 1
        pick += [f'execute if score #mtk bm.rng matches 0 if items entity @s weapon.mainhand {holds(i)} run scoreboard players set #mth bm.rng 1',
                 f'execute if score #mtk bm.rng matches 0 if items entity @s weapon.mainhand {holds(i)} run scoreboard players set #mtk bm.rng {n}']
    for i, k in KIND.items():
        if i in DROP: continue
        n = kinds.index(k) + 1
        pick += [f'execute if score #mtk bm.rng matches 0 if items entity @s weapon.offhand {holds(i)} run scoreboard players set #mth bm.rng 2',
                 f'execute if score #mtk bm.rng matches 0 if items entity @s weapon.offhand {holds(i)} run scoreboard players set #mtk bm.rng {n}']
    fn('p135/try', ['scoreboard players set #mtk bm.rng 0', 'scoreboard players set #mth bm.rng 0'] + pick +
       ['execute if score #mtk bm.rng matches 0 run return 0', 'return run function bm:p135/hang'])
    # 2.78: sneak + drop facing a wall - the item just thrown (the nearest, in reach of the hand) is the one that hangs (#mth 3)
    src = '@e[type=minecraft:item,tag=bm.mtsrc,limit=1]'
    fn('p135/dropped', [f'scoreboard players set @s {o} 0' for o in DOBJ.values()] +
       ['execute unless predicate bm:p20/sneaking run return 0',
        'execute anchored eyes positioned ^ ^ ^ as @e[type=minecraft:item,distance=..2.5,sort=nearest,limit=1] run tag @s add bm.mtsrc',
        'scoreboard players set #mtk bm.rng 0', 'scoreboard players set #mth bm.rng 3'] +
       [f'execute if score #mtk bm.rng matches 0 if items entity {src} contents {holds(i)} run scoreboard players set #mtk bm.rng {kinds.index(k) + 1}' for i, k in DROP.items()] +
       ['scoreboard players set #mtl bm.rng 1', 'execute unless score #mtk bm.rng matches 0 run function bm:p135/hang',
        'tag @e[type=minecraft:item,tag=bm.mtsrc] remove bm.mtsrc'])
    fn('p135/hang', [
        loud('Not in the vault - hang it up out in the world.').replace('run ', 'if dimension bm:gutter run ', 1), 'execute if dimension bm:gutter run return 0',
        loud('Not here - hang it up out in the world.').replace('run ', 'if dimension bm:hollow_throne run ', 1), 'execute if dimension bm:hollow_throne run return 0',
        'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
        'scoreboard players set #placed bm.rng 0', 'scoreboard players set #ray bm.rng 16', 'tag @s add bm.mter',
        'execute if entity @s[x_rotation=-50..50] anchored eyes positioned ^ ^ ^ run function bm:p135/ray', 'tag @s remove bm.mter',
        loud('Look at a wall within 3 blocks, with room in front of it.').replace('run ', 'if score #placed bm.rng matches 0 run ', 1),
        'execute if score #placed bm.rng matches 0 run return 0',
        'execute unless entity @s[gamemode=creative] if score #mth bm.rng matches 1 run item replace entity @s weapon.mainhand with minecraft:air',
        'execute unless entity @s[gamemode=creative] if score #mth bm.rng matches 2 run item replace entity @s weapon.offhand with minecraft:air',
        f'execute if score #mth bm.rng matches 3 run kill {src}',
        'return 1'])
    fn('p135/ray', ['execute unless block ~ ~ ~ #minecraft:replaceable align xyz positioned ~0.5 ~0.5 ~0.5 run return run function bm:p135/face',
                    'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p135/ray'])
    # (the face it hangs on: the one turned toward you - looking south you see a wall's north face, and so on round)
    faces = [('if entity @s[y_rotation=-45..45]', (0, 0, -1), 180), ('if entity @s[y_rotation=45..135]', (1, 0, 0), -90),
             ('if entity @s[y_rotation=-135..-45]', (-1, 0, 0), 90), ('unless entity @s[y_rotation=-135..135]', (0, 0, 1), 0)]
    rel = lambda v: '~' if v == 0 else f'~{v:g}'
    face = []
    for cond, (dx, dy, dz), yaw in faces:
        face.append(f'execute {cond} positioned {rel(dx)} ~ {rel(dz)} if block ~ ~ ~ #minecraft:replaceable positioned {rel(-dx / 2)} ~ {rel(-dz / 2)} '
                    f'unless entity @e[type=minecraft:interaction,tag=bm.mtx,distance=..0.6] rotated {yaw} 0 run return run function bm:p135/put')
    fn('p135/face', face)
    fn('p135/put', [f'execute if score #mtk bm.rng matches {kinds.index(k) + 1} run function bm:p135/place_{k}' for k in kinds] +
       ['scoreboard players set #placed bm.rng 1'])

    # ---- a plaque (a dark rim, a lighter board, turned to a diamond) and the weapon on it, turned to face out from the wall
    # (2.82: the displays stand OUT blocks off the wall - on its face exactly, half the facings lit them from inside the wall
    #  block, black; the models are drawn back by the same amount, so they hang where they did)
    OUT = 0.05
    def board(block, size, depth, z):
        q = (0.0, 0.0, 0.3827, 0.9239)                       # (45 degrees round the wall's normal)
        # (a block display's box runs 0..1 from its corner: centre it on the face after the turn)
        c = 0.7071 * size
        return snbt({'Tags': ['bm.mtp', 'bm.mtnew', 'bm.mt282'], 'block_state': f'minecraft:{block}',
                     'transformation': {'left_rotation': [F(v) for v in q], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                        'translation': [F(0), F(-c), F(z - OUT)], 'scale': [F(size), F(size), F(depth)]}})
    for k, (q, s, t) in XF.items():
        p = PLAQUE[k]
        w = snbt({'Tags': ['bm.mtw', 'bm.mtnew', 'bm.mt282'], 'item': {'id': 'minecraft:stick', 'count': Int(1)}, 'item_display': 'none',
                  'transformation': {'left_rotation': [F(v) for v in q], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                     'translation': [F(t[0]), F(t[1]), F(t[2] - OUT)], 'scale': [F(s)] * 3}})
        fn(f'p135/place_{k}', [f'execute positioned ^ ^ ^{OUT} run summon minecraft:block_display ~ ~ ~ {board("dark_oak_planks", p + 0.1, 0.04, 0.002)}',
                               f'execute positioned ^ ^ ^{OUT} run summon minecraft:block_display ~ ~ ~ {board("spruce_planks", p, 0.06, 0.004)}',
                               f'execute positioned ^ ^ ^{OUT} run summon minecraft:item_display ~ ~ ~ {w}', 'function bm:p135/fill'])
    new_w = '@e[type=minecraft:item_display,tag=bm.mtw,tag=bm.mtnew,distance=..0.6,limit=1]'
    fn('p135/fill', [f'execute if score #mth bm.rng matches 1 run item replace entity {new_w} contents from entity @s weapon.mainhand',
                     f'execute if score #mth bm.rng matches 2 run item replace entity {new_w} contents from entity @s weapon.offhand',
                     f'execute if score #mth bm.rng matches 3 run item replace entity {new_w} contents from entity @e[type=minecraft:item,tag=bm.mtsrc,limit=1] contents',
                     'execute as @e[tag=bm.mtnew,distance=..0.6] positioned as @s run tp @s ~ ~ ~ ~ 0',
                     'summon minecraft:interaction ~ ~-0.45 ~ ' + snbt({'Tags': ['bm.mtx', 'bm.gvdeco', 'bm.mtnew'], 'width': F(0.9), 'height': F(0.9), 'response': B(1)}),
                     'scoreboard players operation @e[type=minecraft:interaction,tag=bm.mtnew,distance=..1] bm.pid = @s bm.pid',
                     'tag @e[tag=bm.mtnew,distance=..1] remove bm.mtnew',
                     'particle minecraft:wax_on ~ ~ ~ 0.3 0.3 0.1 0 10', 'playsound minecraft:entity.item_frame.add_item block @a[distance=..16] ~ ~ ~ 1 0.8',
                     'playsound minecraft:block.wood.place block @a[distance=..16] ~ ~ ~ 1 1',
                     title('@s', 'actionbar', [T('It hangs on the wall. ', 'white'), T('(Sneak + punch it to take it down.)', 'gray')])])

    # ---- sneak + punch: down again, into your hands - only whoever hung it
    G.FUNCS['p71/deco/pick'][0:0] = ['execute if entity @e[type=minecraft:interaction,tag=bm.gvdme,tag=bm.mtx] at @e[type=minecraft:interaction,tag=bm.gvdme,limit=1] '
                                     'positioned ~ ~0.45 ~ run return run function bm:p135/take']
    me_x = '@e[type=minecraft:interaction,tag=bm.gvdme,limit=1]'
    fn('p135/take', [f'execute if score {me_x} bm.pid matches 1.. unless score @s bm.pid = {me_x} bm.pid run return run ' + say("It isn't yours to take."),
                     'execute at @s run summon minecraft:item ~ ~0.4 ~ {Item:{id:"minecraft:stone",count:1},PickupDelay:0s,Tags:["bm.mtgive"]}',
                     'data modify entity @e[type=minecraft:item,tag=bm.mtgive,limit=1] Item set from entity @e[type=minecraft:item_display,tag=bm.mtw,distance=..0.3,limit=1] item',
                     'data modify entity @e[type=minecraft:item,tag=bm.mtgive,limit=1] Owner set from entity @s UUID',
                     'tag @e[type=minecraft:item,tag=bm.mtgive] remove bm.mtgive', 'function bm:p135/gone', f'kill {me_x}',
                     'playsound minecraft:entity.item_frame.remove_item block @a[distance=..16] ~ ~ ~ 1 0.8'])
    fn('p135/gone', ['kill @e[type=minecraft:item_display,tag=bm.mtw,distance=..0.3]', 'kill @e[type=minecraft:block_display,tag=bm.mtp,distance=..0.3]',
                     'particle minecraft:poof ~ ~ ~ 0.2 0.2 0.1 0.02 6'])
    # (its wall broken, or its box gone: it drops where it hung - never lost)
    second.append('execute as @e[type=minecraft:item_display,tag=bm.mtw] at @s run function bm:p135/check')
    fn('p135/check', ['scoreboard players set #mtd bm.rng 0',
                      'execute rotated as @s positioned ^ ^ ^-0.5 if block ~ ~ ~ #minecraft:replaceable run scoreboard players set #mtd bm.rng 1',
                      'execute positioned ~ ~-0.45 ~ unless entity @e[type=minecraft:interaction,tag=bm.mtx,distance=..0.3] run scoreboard players set #mtd bm.rng 1',
                      'execute if score #mtd bm.rng matches 1 run function bm:p135/drop'])
    fn('p135/drop', ['summon minecraft:item ~ ~ ~ {Item:{id:"minecraft:stone",count:1},Tags:["bm.mtgive"]}',
                     'data modify entity @e[type=minecraft:item,tag=bm.mtgive,distance=..0.5,limit=1] Item set from entity @s item',
                     'tag @e[type=minecraft:item,tag=bm.mtgive] remove bm.mtgive',
                     'execute positioned ~ ~-0.45 ~ run kill @e[type=minecraft:interaction,tag=bm.mtx,distance=..0.3]', 'function bm:p135/gone'])
    # (and the ones already hanging, once: stepped out, their models drawn back)
    second.append('execute as @e[type=#bm:p135_mount,tag=!bm.mt282,tag=!bm.mtnew] at @s rotated as @s run function bm:p135/nudge')
    G.wjson('bm/tags/entity_type/p135_mount.json', {'values': ['minecraft:item_display', 'minecraft:block_display']})
    fn('p135/nudge', ['tag @s add bm.mt282', 'execute unless entity @s[tag=bm.mtw] unless entity @s[tag=bm.mtp] run return 0',
                      f'tp @s ^ ^ ^{OUT}', 'execute store result score #t bm.rng run data get entity @s transformation.translation[2] 10000',
                      f'scoreboard players remove #t bm.rng {int(OUT * 10000)}',
                      'execute store result entity @s transformation.translation[2] float 0.0001 run scoreboard players get #t bm.rng'])
    G.FUNCS['loop/second'][-1:-1] = second
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} minecraft.dropped:minecraft.{b}' for b, o in DOBJ.items()]
    G.OBJECTIVES += list(DOBJ.values())
    G.FUNCS['tick'] += [f'execute as @a[scores={{{o}=1..}}] at @s run function bm:p135/dropped' for o in DOBJ.values()]
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.mtw]', 'kill @e[type=minecraft:block_display,tag=bm.mtp]',
                                       'kill @e[type=minecraft:interaction,tag=bm.mtx]']

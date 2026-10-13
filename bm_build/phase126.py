"""2.75 (late): true invisibility, Pearlman's bell, graveyards that sit in the land, one set of gems per world.

INVISIBLE MEANS INVISIBLE: while you have Invisibility (the Phantom Regalia, the Thief's Cowl, Shadowstep, the Phantom kit,
  a smoke bomb, a potion), the armour you wear isn't drawn either - helmet, chestplate, leggings, boots, elytra, even a
  pumpkin or a mob head. (Each worn piece is pointed at an empty equipment model, bm:none, and put back the moment the
  effect ends. A piece that leaves your armour slots - taken off, dropped, or dropped on death - is put back too.)
PEARLMAN'S BELL: a rare raid find (5% a won heist, any tier, every raider). Ring it and Pearlman, the Traveling
  Salespenguin, waddles over - wherever you are, if he isn't already out on his rounds. One ring.
GRAVEYARDS: new graveyards no longer stand on a cliff of their own foundation. The yard and the crypt are two jigsaw pieces
  (structures.graveyard_pieces): the yard blends into the land like a village does, and the crypt keeps only a shell of rock.
  The first time someone comes near a new graveyard, the land round it is graded: a stepped grassy bank where the yard
  stands over a drop, and the hill cut back in steps where it's dug in.
GEMS STAY WHERE THEY WERE GIVEN: the gem (or the Ethereal Gem) Cecil or KillerWatt carries in the heist lobby is a
  separate one from the one he carries in the overworld. Each world keeps its own, swapped as you come and go.
"""
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import B, snbt

PEARL = '#5ac8ff'
BELL_CHANCE = 5                     # % a won heist, every raider, any tier
SLOTS = ('head', 'chest', 'legs', 'feet')
GY_G = 17                           # the graveyard's floor, in template blocks (structures.build_graveyard)
GY_CTRL = (15, 2, 49)               # its crypt controller marker's block (the skirt is laid out from it)
GY_D = 16                           # rings of grading round the yard

item('pearl_bell', TOTEM, "Pearlman's Bell", PEARL, ['A little silver handbell with a blue bow.', ('Ring it: Pearlman, the Traveling', 'blue'),
                                                     ('Salespenguin, waddles over to you.', 'blue'), ('One ring - then it\'s just a bell.', 'gray'),
                                                     ('◆ Rare raid find', '#5ab0ff')],
     model='bm:pearl_bell', stack=16, comps=hold(), cat='relic')
HOLD['pearl_bell'] = 'bm:p126/bell/ring'

# vanilla wearables that carry their equippable as a default (not in their saved data): what to put back
PROTO = {}
for mat, asset, snd in (('leather', 'leather', 'equip_leather'), ('chainmail', 'chainmail', 'equip_chain'), ('iron', 'iron', 'equip_iron'),
                        ('golden', 'gold', 'equip_gold'), ('diamond', 'diamond', 'equip_diamond'), ('netherite', 'netherite', 'equip_netherite'),
                        ('copper', 'copper', 'equip_copper')):
    for piece, slot in (('helmet', 'head'), ('chestplate', 'chest'), ('leggings', 'legs'), ('boots', 'feet')):
        PROTO[f'{mat}_{piece}'] = (slot, f'{{slot:"{slot}",asset_id:"minecraft:{asset}",equip_sound:"minecraft:item.armor.{snd}"}}')
PROTO['turtle_helmet'] = ('head', '{slot:"head",asset_id:"minecraft:turtle_scute",equip_sound:"minecraft:item.armor.equip_turtle"}')
PROTO['elytra'] = ('chest', '{slot:"chest",asset_id:"minecraft:elytra",equip_sound:"minecraft:item.armor.equip_elytra",damage_on_hurt:false}')
PROTO['carved_pumpkin'] = ('head', '{slot:"head",swappable:false,camera_overlay:"minecraft:misc/pumpkinblur"}')
for h in ('player_head', 'zombie_head', 'skeleton_skull', 'creeper_head', 'wither_skeleton_skull', 'piglin_head', 'dragon_head'):
    PROTO[h] = ('head', '{slot:"head",swappable:false}')


def generate(G):
    fn, wjson, tellraw = G.fn, G.wjson, G.tellraw
    tick, second = [], []
    P = [T('[', 'dark_gray'), T('Black Market', 'dark_purple', bold=True), T('] ', 'dark_gray')]
    say = lambda txt, col='gray': tellraw('@s', P + [T(txt, col)])
    GH = '*[minecraft:custom_data~{bmg:1b}]'

    # ================================================================== INVISIBLE MEANS INVISIBLE
    wjson('bm/predicate/p126/invis.json', {'condition': 'minecraft:entity_properties', 'entity': 'this',
                                           'predicate': {'minecraft:effects': {'minecraft:invisibility': {}}}})
    tick += ['execute as @a[tag=!bm.ghost,predicate=bm:p126/invis] run function bm:p126/ghost/on',
             'execute as @a[tag=bm.ghost] run function bm:p126/ghost/keep']
    fn('p126/ghost/on', ['tag @s add bm.ghost', 'function bm:p126/ghost/hide_all'])
    fn('p126/ghost/keep', ['execute unless predicate bm:p126/invis run return run function bm:p126/ghost/off', 'function bm:p126/ghost/hide_all'])
    fn('p126/ghost/off', ['tag @s remove bm.ghost', 'function bm:p126/ghost/show_armor'])
    fn('p126/ghost/hide_all', [f'execute if items entity @s armor.{s} * unless items entity @s armor.{s} {GH} run function bm:p126/ghost/hide_{s}' for s in SLOTS])
    for s in SLOTS:
        fn(f'p126/ghost/hide_{s}', ['data remove storage bm:ghost e',
                                    f'data modify storage bm:ghost e set from entity @s equipment.{s}.components."minecraft:equippable"',
                                    f'execute unless data storage bm:ghost e run function bm:p126/ghost/proto_{s}',
                                    'execute unless data storage bm:ghost e run return 0',
                                    'data modify storage bm:ghost h set from storage bm:ghost e', 'data modify storage bm:ghost h.asset_id set value "bm:none"',
                                    'data modify storage bm:ghost t set value {}',
                                    f'data modify storage bm:ghost t set from entity @s equipment.{s}.components."minecraft:custom_data"',
                                    'data modify storage bm:ghost t.bmg set value 1b', 'data modify storage bm:ghost t.bmgeq set from storage bm:ghost e',
                                    f'data modify storage bm:ghost slot set value "armor.{s}"',
                                    'function bm:p126/ghost/put_hidden with storage bm:ghost'])
        fn(f'p126/ghost/proto_{s}', [f'execute if items entity @s armor.{s} minecraft:{iid} run return run data modify storage bm:ghost e set value {val}'
                                     for iid, (sl, val) in PROTO.items() if sl == s or (s == 'chest' and iid == 'elytra')])
    fn('p126/ghost/put_hidden', ['$item modify entity @s $(slot) {type:"minecraft:set_components",components:{"minecraft:equippable":$(h),"minecraft:custom_data":$(t)}}'])
    fn('p126/ghost/show_armor', [f'execute if items entity @s armor.{s} {GH} run function bm:p126/ghost/show {{slot:"armor.{s}",path:"equipment.{s}"}}' for s in SLOTS])
    # (put back: the piece's own equippable, and its custom data without the marks - none at all if that leaves it empty)
    fn('p126/ghost/show', ['data remove storage bm:ghost e', 'data remove storage bm:ghost cd',
                           '$data modify storage bm:ghost e set from entity @s $(path).components."minecraft:custom_data".bmgeq',
                           '$data modify storage bm:ghost cd set from entity @s $(path).components."minecraft:custom_data"',
                           'data remove storage bm:ghost cd.bmg', 'data remove storage bm:ghost cd.bmgeq', '$data modify storage bm:ghost slot set value "$(slot)"',
                           'execute if data storage bm:ghost e run function bm:p126/ghost/put_eq with storage bm:ghost',
                           'execute store result score #n bm.rng run data get storage bm:ghost cd',
                           'execute if score #n bm.rng matches 0 run return run function bm:p126/ghost/put_nocd with storage bm:ghost',
                           'function bm:p126/ghost/put_cd with storage bm:ghost'])
    fn('p126/ghost/put_eq', ['$item modify entity @s $(slot) {type:"minecraft:set_components",components:{"minecraft:equippable":$(e)}}'])
    fn('p126/ghost/put_cd', ['$item modify entity @s $(slot) {type:"minecraft:set_components",components:{"minecraft:custom_data":$(cd)}}'])
    fn('p126/ghost/put_nocd', ['$item modify entity @s $(slot) {type:"minecraft:set_components",components:{"!minecraft:custom_data":{}}}'])
    # a hidden piece anywhere but on an invisible player's body: put back (in a pack - the moment it lands there; on the ground - within a second)
    wjson('bm/advancement/p126/ghost_inv.json', {'criteria': {'g': {'trigger': 'minecraft:inventory_changed', 'conditions': {
        'items': [{'predicates': {'minecraft:custom_data': '{bmg:1b}'}}]}}}, 'rewards': {'function': 'bm:p126/ghost/inv'}})
    fn('p126/ghost/inv', ['advancement revoke @s only bm:p126/ghost_inv'] +
       [f'execute if items entity @s container.{n} {GH} run function bm:p126/ghost/show {{slot:"container.{n}",path:"Inventory[{{Slot:{n}b}}]"}}' for n in range(36)] +
       [f'execute if items entity @s weapon.offhand {GH} run function bm:p126/ghost/show {{slot:"weapon.offhand",path:"equipment.offhand"}}',
        'execute unless entity @s[tag=bm.ghost] run function bm:p126/ghost/show_armor'])
    second.append(f'execute as @e[type=minecraft:item] if items entity @s contents {GH} run function bm:p126/ghost/show {{slot:"contents",path:"Item"}}')

    # ================================================================== PEARLMAN'S BELL
    fn('p126/bell/ring', ['execute if dimension bm:gutter run return run ' + say('The bell rings... nobody waddles into a heist. Try it out in the world.', 'gray'),
                          'execute if entity @e[type=minecraft:villager,tag=bm.pearl] run return run ' +
                          tellraw('@s', P + [T('Pearlman ', PEARL, bold=True), T('is already out on his rounds - the bell can wait.', 'gray')]),
                          'playsound minecraft:block.bell.use player @a[distance=..24] ~ ~ ~ 1 1.8',
                          'particle minecraft:note ~ ~2.2 ~ 0.4 0.2 0.4 1 6',
                          'scoreboard players set #placed bm.rng 0',
                          'execute if dimension minecraft:overworld run function bm:p60/pm/arrive',
                          'execute if score #placed bm.rng matches 0 rotated ~ 0 positioned ^ ^ ^2 align xz positioned ~0.5 ~ ~0.5 run function bm:p60/pm/spawn',
                          'execute unless entity @s[gamemode=creative] run clear @s *[minecraft:custom_data~{bm:"pearl_bell"}] 1',
                          tellraw('@s', P + [T('Ding-a-ling! ', PEARL, bold=True), T('Pearlman\'s on his way.', 'gray')])])
    HA, HB = '-200 64 -197', '-198 64 -197'
    G.FUNCS['p105/finds'] += ['execute store result score #r bm.rng run random value 1..100',
                              f'execute if score #r bm.rng matches ..{BELL_CHANCE} run function bm:p126/bell/find']
    wjson('bm/loot_table/p126/bell.json', {'type': 'minecraft:chest', 'pools': [{'rolls': 1, 'entries': [G.loot_entry('pearl_bell')]}]})
    fn('p126/bell/find', [f'execute in bm:gutter unless data block {HA} Items[26] run loot insert {HA} loot bm:p126/bell',
                          f'execute in bm:gutter if data block {HA} Items[26] run loot insert {HB} loot bm:p126/bell',
                          tellraw('@s', [T('[', 'dark_gray'), T('Heist', '#ffcf40', bold=True), T('] ', 'dark_gray'), T('Rare find! ', '#5ab0ff', bold=True),
                                         T("Pearlman's Bell", PEARL, bold=True), T(' in your haul.', 'gray')]),
                          'playsound minecraft:block.bell.use player @s ~ ~ ~ 0.8 1.8'])
    fn('admin/pearl_bell', [G.give('pearl_bell')])

    # ================================================================== GRAVEYARDS: grade the land round a new one, once
    cx, cy, cz = GY_CTRL
    L = lambda x, y, z: '^{:g} ^{:g} ^{:g}'.format(x - cx, y - cy + 0.5, z - cz)     # (block centres: the marker sits at .5, rotated as the structure)
    wjson('bm/tags/block/gy_cut.json', {'values': [{'id': v, 'required': False} for v in (
        '#minecraft:dirt', '#minecraft:base_stone_overworld', '#minecraft:logs', '#minecraft:leaves', '#minecraft:sand', '#minecraft:flowers',
        '#minecraft:coal_ores', '#minecraft:iron_ores', '#minecraft:copper_ores', 'minecraft:gravel', 'minecraft:clay', 'minecraft:calcite',
        'minecraft:snow', 'minecraft:snow_block', 'minecraft:powder_snow', 'minecraft:short_grass', 'minecraft:tall_grass', 'minecraft:fern',
        'minecraft:large_fern', 'minecraft:dead_bush', 'minecraft:bush', 'minecraft:firefly_bush', 'minecraft:leaf_litter', 'minecraft:short_dry_grass',
        'minecraft:tall_dry_grass', 'minecraft:sweet_berry_bush', 'minecraft:vine', 'minecraft:glow_lichen', 'minecraft:moss_carpet',
        'minecraft:pale_moss_carpet', 'minecraft:pale_hanging_moss', 'minecraft:brown_mushroom', 'minecraft:red_mushroom', 'minecraft:pumpkin',
        'minecraft:sugar_cane')]})
    wjson('bm/tags/block/gy_soil.json', {'values': [{'id': v, 'required': False} for v in (
        '#minecraft:dirt', '#minecraft:base_stone_overworld', 'minecraft:gravel', 'minecraft:clay', 'minecraft:calcite',
        '#minecraft:coal_ores', '#minecraft:iron_ores', '#minecraft:copper_ores')]})
    G2 = GY_G
    def strips(d):
        return [(-d, 30 + d, -d, -d), (-d, 30 + d, 64 + d, 64 + d), (-d, -d, -d + 1, 63 + d), (30 + d, 30 + d, -d + 1, 63 + d)]
    for d in range(1, GY_D + 1):
        cmds = []
        for xa, xb, za, zb in strips(d):
            cmds += [f'fill {L(xa, G2 - 32, za)} {L(xb, G2 - d - 1, zb)} minecraft:dirt replace minecraft:air',
                     f'fill {L(xa, G2 - d, za)} {L(xb, G2 - d, zb)} minecraft:grass_block replace minecraft:air',
                     f'fill {L(xa, G2 + d + 1, za)} {L(xb, G2 + 28, zb)} minecraft:air replace #bm:gy_cut',
                     f'fill {L(xa, G2 + d, za)} {L(xb, G2 + d, zb)} minecraft:grass_block replace #bm:gy_soil']
        fn(f'p126/gy/r{d}', cmds)
    D = GY_D
    loaded = ' '.join(f'if loaded {L(x, G2, z)}' for x, z in ((-D, -D), (30 + D, -D), (-D, 64 + D), (30 + D, 64 + D)))
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.gysk dummy']
    G.OBJECTIVES += ['bm.gysk']
    second.append('execute as @e[type=minecraft:marker,tag=bm.gy2,tag=!bm.gyskd] at @s if entity @a[distance=..112] rotated as @s '
                  f'{loaded} run function bm:p126/gy/step')
    steps = (D + 1) // 2
    fn('p126/gy/step', ['scoreboard players add @s bm.gysk 1',
                        f'execute if score @s bm.gysk matches 1 run fill {L(0, G2 + 15, 0)} {L(30, G2 + 28, 64)} minecraft:air replace #bm:gy_cut',
                        # (over a lake or a river bank: no water under the yard - the crypt's own shell keeps it dry inside)
                        f'execute if score @s bm.gysk matches 1 run fill {L(0, G2 - 16, 0)} {L(30, G2 - 2, 64)} minecraft:dirt replace minecraft:water'] +
       [f'execute if score @s bm.gysk matches {k + 1} run function bm:p126/gy/r{d}' for k in range(steps) for d in (2 * k + 1, 2 * k + 2) if d <= D] +
       [f'execute if score @s bm.gysk matches {steps}.. run tag @s add bm.gyskd'])

    # ================================================================== GEMS STAY WHERE THEY WERE GIVEN (the lobby's, the world's)
    objs = ['bm.kxelo', 'bm.kxell', 'bm.cpelo', 'bm.cpell', 'bm.vgkl', 'bm.vgcl']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    tick += ['execute as @a[tag=!bm.gemlob] at @s if dimension bm:gutter run function bm:p126/gem/in',
             'execute as @a[tag=bm.gemlob] at @s unless dimension bm:gutter run function bm:p126/gem/out']
    def swap(save_to, load_from):
        out = []
        for cur, sv, ld in (('bm.kxel', f'bm.kxel{save_to}', f'bm.kxel{load_from}'), ('bm.cpel', f'bm.cpel{save_to}', f'bm.cpel{load_from}')):
            out += [f'scoreboard players set @s {sv} 0', f'execute if score @s {cur} matches 1.. run scoreboard players operation @s {sv} = @s {cur}',
                    f'scoreboard players set @s {cur} 0', f'execute if score @s {ld} matches 1.. run scoreboard players operation @s {cur} = @s {ld}']
        return out
    fn('p126/gem/in', ['tag @s add bm.gemlob'] + swap('o', 'l') +
       ['scoreboard players operation @s bm.vgk = @s bm.vgkl', 'scoreboard players operation @s bm.vgc = @s bm.vgcl', 'function bm:p126/gem/redress'])
    fn('p126/gem/out', ['tag @s remove bm.gemlob', 'scoreboard players operation @s bm.vgkl = @s bm.vgk', 'scoreboard players operation @s bm.vgcl = @s bm.vgc',
                        'scoreboard players set @s bm.vgk 0', 'scoreboard players set @s bm.vgc 0'] + swap('l', 'o') + ['function bm:p126/gem/redress'])
    # (whoever's already out takes the look of the world he's in)
    fn('p126/gem/redress', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #el bm.rng 0',
                            'execute if score @s bm.cpel matches 1.. run scoreboard players operation #el bm.rng = @s bm.cpel', 'function bm:p46/pet/dress',
                            'scoreboard players operation #kel0 bm.rng = @s bm.kxel',
                            'execute as @e[type=minecraft:wolf,tag=bm.kxpet] if score @s bm.pid = #me bm.pid at @s run function bm:p126/gem/kw'])
    fn('p126/gem/kw', ['scoreboard players operation @s bm.kxel = #kel0 bm.rng', 'function bm:p79/pet/redress'])

    # ================================================================== CECIL'S BOLTS: from his staff to the foe (they were drawn a fixed 13
    # blocks back from the foe, so anything closer had the beam running out behind him)
    import re
    beams = {}
    for name in list(G.FUNCS):
        body = G.FUNCS[name]
        for n in range(len(body) - 1, -1, -1):
            m = re.fullmatch(r'execute facing entity @e\[type=minecraft:wolf,tag=bm\.cpme,limit=1\] eyes run function bm:p46/pet/beam/(\w+)', body[n])
            if not m: continue
            k = m.group(1)
            beams[k] = re.match(r'(particle minecraft:dust\{[^}]*\}) ', G.FUNCS[f'p46/pet/beam/{k}'][0]).group(1)
            body[n:n + 1] = ['tag @s add bm.cptgt',
                             'execute as @e[type=minecraft:wolf,tag=bm.cpme,limit=1] at @s positioned ~ ~1.45 ~ facing entity @e[tag=bm.cptgt,limit=1] eyes '
                             f'positioned ^ ^ ^0.5 run function bm:p126/cbeam/{k}',
                             'tag @s remove bm.cptgt']
    assert len(beams) >= 10, beams
    for k, part in beams.items():
        G.FUNCS.pop(f'p46/pet/beam/{k}', None)
        fn(f'p126/cbeam/{k}', ['scoreboard players set #bs bm.rng 0', f'function bm:p126/cbeam/{k}_s'] +
           (['particle minecraft:end_rod ~ ~ ~ 0.05 0.05 0.05 0.02 3'] if k == 'ethereal' else []))
        fn(f'p126/cbeam/{k}_s', [f'{part} ~ ~ ~ 0 0 0 0 1', 'scoreboard players add #bs bm.rng 1',
                                 f'execute if score #bs bm.rng matches ..30 unless entity @e[tag=bm.cptgt,distance=..1.6] positioned ^ ^ ^0.5 run function bm:p126/cbeam/{k}_s'])

    # ================================================================== the tier functions, run by hand: spawn one (they used to dress YOU up)
    for name in list(G.FUNCS):
        m = re.fullmatch(r'mobs/(elite|champion|blood|jackpot|lucky|prime)/([a-z_]+)', name)
        if m:
            G.FUNCS[name].insert(0, f'execute if entity @s[type=minecraft:player] at @s rotated ~ 0 positioned ^ ^ ^3 run return run '
                                    f'execute summon minecraft:{m.group(2)} run function bm:{name}')
    for name in list(G.FUNCS):          # (which makes them positional: their callers run them where the mob is)
        G.FUNCS[name] = [re.sub(r'^(execute as @e\[[^\]]*\]) run (function bm:mobs/(?:elite|champion|blood|jackpot|lucky|prime)/)', r'\1 at @s run \2', l)
                         if isinstance(l, str) else l for l in G.FUNCS[name]]

    # ================================================================== THE LEDGER PLANS HEISTS (the Heist Plans folded into it)
    # (from the Fixer's Lounge too: the heist then starts from the lounge, and brings you back to it)
    lounge = 'unless function bm:p121/inside '
    for f in ('p70/plans', 'p70/pick_tier', 'p75/pick_lives', 'p77/pick_mode', 'p90/alarm_toggle'):
        L = G.FUNCS[f]
        for i, l in enumerate(L):
            for a in ('execute if dimension bm:gutter run return', 'execute unless entity @s[tag=bm.gvnext] if dimension bm:gutter run return',
                      'execute unless entity @s[tag=bm.gvnext] unless dimension minecraft:overworld unless dimension minecraft:the_nether',
                      'execute unless dimension minecraft:overworld unless dimension minecraft:the_nether'):
                if l.startswith(a):
                    L[i] = 'execute ' + lounge + l[len('execute '):]; break
    assert any('p121/inside' in l for l in G.FUNCS['p70/plans']) and any('p121/inside' in l for l in G.FUNCS['p70/pick_tier'])
    second.append('execute as @a[tag=!bm.lgadv,tag=!bm.gvp,gamemode=survival] at @s if dimension bm:gutter if function bm:p121/inside run function bm:p121/adv')
    # (old Heist Plans in a pack: gone into the Ledger - one Ledger each)
    oldp = '*[minecraft:custom_data~{bm:"heist_plans"}]'
    second.append(f'execute as @a if items entity @s container.* {oldp} run function bm:p126/retire/plans')
    fn('p126/retire/plans', [f'clear @s {oldp}',
                           'execute unless items entity @s container.* *[minecraft:custom_data~{bm:"fixers_ledger"}] unless items entity @s weapon.offhand *[minecraft:custom_data~{bm:"fixers_ledger"}] run ' + G.give('fixers_ledger'),
                           say("Your Heist Plans are part of the Fixer's Ledger now: open it and pick Plan a Heist.", '#ffcf40')])

    # ================================================================== PUZZLE SUPPLIES: the crafting and brewing rooms can't run dry
    # (the Tinker's Bench A/B/C and the Apothecary A/B/C hand out their parts once; now the room's barrels hold two more full
    #  sets, and if any part runs out - none in the barrels, none on the crew - the Fixer tops them up)
    import phase70_rooms as RM
    import phase112 as P112
    SUP = {'bench': [(x - 1, 4, z) for x, z in P112.BENCHES], 'apoth': [(10, 5, 20), (14, 5, 20)]}
    starts = {'p112/bench/start': 'bench', 'p114/benchb/start': 'bench', 'p114/benchc/start': 'bench', 'p115/apoth/start': 'apoth'}
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.stk dummy']
    G.OBJECTIVES += ['bm.stk']
    ONE = ('minecraft:potion', 'minecraft:splash_potion', 'minecraft:lingering_potion', 'minecraft:white_banner')
    sid, chk, has_done = 0, [], set()
    for sf, room in starts.items():
        L = G.FUNCS[sf]; add_l = []
        for l in L:
            m = re.fullmatch(r'execute (.*?) ?as (@a\[[^\]]*\]) run function bm:(\S+)', l)
            if not m or m.group(1) == '': continue
            items = [(a, int(n)) for gl in G.FUNCS[m.group(3)] for a, n in re.findall(r'^give @s (\S+) (\d+)$', gl)]
            if not items: continue
            sid += 1
            body = [f'scoreboard players set @s bm.stk {sid}']
            for bx, by, bz in SUP[room]:
                k = 0
                for spec, n in items:
                    base = spec.split('[')[0]
                    if base in ONE:
                        for _ in range(2 * n): body.append(f'item replace block {RM.rel(bx, by, bz)} container.{k} with {spec} 1'); k += 1
                    else:
                        body.append(f'item replace block {RM.rel(bx, by, bz)} container.{k} with {spec} {min(64, 2 * n)}'); k += 1
                assert k <= 27, (sf, k)
            fn(f'p126/stk/s{sid}', body)
            bases = sorted({spec.split('[')[0] for spec, _n in items})
            look = []
            for base in bases:
                key = base.split(':')[1]
                if key not in has_done:
                    has_done.add(key)
                    fn(f'p126/stk/has_{key}', [f'execute as @a[tag=bm.gvp,distance=..30] if items entity @s container.* {base} run return 1',
                                                f'execute as @a[tag=bm.gvp,distance=..30] if items entity @s weapon.offhand {base} run return 1', 'return 0'])
                cond = ' '.join(f'unless items block {RM.rel(*p_)} container.* {base}' for p_ in SUP[room])
                look.append(f'execute {cond} unless function bm:p126/stk/has_{key} run return run function bm:p126/stk/top{sid}')
            fn(f'p126/stk/c{sid}', look)
            fn(f'p126/stk/top{sid}', [f'function bm:p126/stk/s{sid}', 'playsound minecraft:block.barrel.open block @a[distance=..20] ~ ~ ~ 1 1',
                                      'title @a[tag=bm.gvp,distance=..30] actionbar ' + snbt(T('Short of something? The Fixer tops up the barrels.', '#ffcf40'))])
            chk.append(f'execute if score @s bm.stk matches {sid} run return run function bm:p126/stk/c{sid}')
            add_l.append(f'execute {m.group(1)} run function bm:p126/stk/s{sid}')
        assert add_l, sf
        L += add_l
    fn('p126/stk/chk', chk)
    second.append('execute as @e[type=minecraft:marker,scores={bm.stk=1..,bm.gvs=1}] at @s run function bm:p126/stk/chk')

    # ================================================================== (guard) every menu click is read before anything looks at it - 2.74's
    # lounge buttons sat above the read and matched the LAST click, so after one Go to the Lounge every menu on the server went dead
    pa = G.FUNCS['p28/act']
    k_read = pa.index('scoreboard players operation #act bm.pay = @s bm.act')
    assert not any('#act' in l for l in pa[:k_read]), 'p28/act: a button check above the read of the click'

    G.FUNCS['tick'] += tick
    s_ = G.FUNCS['loop/second']
    s_[-1:-1] = second


# ====================================================================== resource pack
def rp(R):
    from PIL import Image
    R.ICONS['pearl_bell'] = R.grid(['................', '.......kk.......', '......kwwk......', '.....kwssbk.....', '.....kwssbk.....', '....kwsssbbk....',
                                    '....kwsssbbk....', '...kwssssbbbk...', '...kwssssbbbk...', '..kkkkkkkkkkkk..', '..kBBBkddkBBBk..', '...kkkkggkkkk...',
                                    '.......kk.......', '................', '................', '................'],
                                   dict(k='#2a3a4a', w='#ffffff', s='#c8d4e0', b='#8a9aaa', B='#2a7ad0', d='#5ac8ff', g='#e0c060'))

    def post(R2):
        # the empty equipment model a hidden piece points at: a layer only a wolf would ever wear, so a player's draws nothing
        Image.new('RGBA', (64, 32)).save(R2.p('assets', 'bm', 'textures', 'entity', 'equipment', 'wolf_body', 'none.png'))
        R2.wj('assets/bm/equipment/none.json', {'layers': {'wolf_body': [{'texture': 'bm:none'}]}})
    R.POST.append(post)

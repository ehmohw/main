"""Phase 1.15: Donado and the Donadians (the Visitors, part 2).

- DONADO, a scrappy cream-coloured dog in a patched grey shirt, is being held in the holding pen of every alien
  MOTHERSHIP. Right-click him to free him and he becomes your companion, exactly like the Frog with Mustache: an
  invisible tamed wolf carries his 3D body, his weapon and a swap slot. Hand him a weapon or armour (right-click him
  holding it) and he equips it for real (his helmet shows on his head); sneak + right-click empty-handed takes it all
  back; right-click empty-handed to make him wait or follow. Flip-book animation: stand, breathe, blink, tail wag,
  walk (2 frames), run (2 frames), crouch and jump - chosen from how fast he's moving and whether he's airborne.
- THE DONADIANS, an alien race of Donado look-alikes (based on the player's own build: teal patterned skin, red
  eyes, black muzzle, pointy ears, antennae, a dark coat, a glowing hover-disc), are the main alien NPCs: Zorp now is
  one, and a crew of them (three outfits) runs every mothership. Idle animation: antennae wiggle, blink, talk.
- THE MOTHERSHIP (first version - the full dungeon with puzzles and the Overseer comes later): a huge saucer
  hovering ~200 blocks up. A green TRACTOR BEAM under it lifts you aboard; sneak in the beam to float back down.
  Inside: a holding pen (abducted animals and Donado), a Xenite reactor ringed with deposits, the bridge, a lab, crew
  quarters and a quartermaster (sells like Zorp). Zorp sells a Mothership Map.
Importing registers the items; generate(G) runs after phase24.generate. No existing trader changes except Zorp,
who gains the map trade (he re-syncs on his own checksum)."""
import math
import random
from nbt import snbt, B, F, Int, D
from items import item, consumable, T, TOTEM

DS = 0.85                  # Donado display scale
WOLF_TOP = 0.85
DON_POSES = [('stand', 1, 0.0), ('breathe', 2, 0.0), ('blink', 3, 0.0), ('wag', 4, 0.0), ('walk1', 5, 0.02), ('walk2', 6, 0.02),
             ('run1', 7, 0.05), ('run2', 8, 0.02), ('crouch', 9, -0.04), ('jump', 10, 0.1)]
DON_POSE_NAMES = [p for p, _, _ in DON_POSES]
ALIEN_VARIANTS = {'': 'coat', '_sci': 'labcoat', '_off': 'redcoat'}        # model suffix -> coat texture
ALIEN_POSES = ['sniff', 'ears', 'tail']                                    # driven by the 1.11 rat idle animation
# 1.16: gripped in his RIGHT paw, blade pointing forward and up. Item displays turn the model 180 degrees, so his right
# paw (model x 12.2) sits at display x -0.22, its grip (model y 5.8, z 8.4) at y -0.54, z -0.02; a sword sprite's
# handle is 0.17 below and 0.17 behind its centre once turned -90 degrees about Y (scale 0.55).
WEAP_ROT = [0.0, -0.7071, 0.0, 0.7071]


def weap_for(pose, bob=0.0):
    """The sword's display translation for a pose: follows his right paw wherever the pose puts it (in game a positive
    x rotation swings a limb's far end forward, toward -z in the model)."""
    import math
    paw = donado_pose(pose, parts=True)['armR'][2]
    c = [(paw['from'][i] + paw['to'][i]) / 2 for i in range(3)]
    r = paw.get('rotation')
    if r and r['axis'] == 'x':
        a = math.radians(r['angle']); o = r['origin']
        y, z = c[1] - o[1], c[2] - o[2]
        c[1], c[2] = o[1] + y * math.cos(a) - z * math.sin(a), o[2] + y * math.sin(a) + z * math.cos(a)
    gx, gy, gz = -(c[0] / 16 - 0.5) * DS, (c[1] / 16 - 0.5) * DS + DS / 2 - WOLF_TOP + bob, -(c[2] / 16 - 0.5) * DS
    return round(gx - 0.012, 3), round(gy + 0.17, 3), round(gz + 0.17, 3)

item('sealed_map_mothership', TOTEM, 'Sealed Mothership Chart', '#7dff6a',
     ['Hold right-click to break the seal.', 'Marks the nearest alien mothership.', ('Look up. Way up.', 'gray')],
     model='minecraft:map', glint=True, stack=16,
     comps={'minecraft:consumable': consumable(0.8, 'none', 'minecraft:item.book.page_turn', False)}, cat='map')

# Zorp gains the chart (at import, before phase 1.14 builds his offer list and its checksum: only he re-syncs)
import phase24 as _R24
_R24.OFFERS.insert(6, (('xenite_green', 4), ('xenite_cyan', 4), ('sealed_map_mothership', 1)))

DON_SAYS = ["*happy bark*", "Woof! (Thank you!)", "*wags tail furiously*", "Grr... (the aliens took my lunch)", "*sniff sniff*"]
CREW_SAYS = ["Earth-dog spotted.", "Do not touch the reactor.", "The Overseer is watching.", "Glorp.", "Your species smells of cheese.",
             "We come in peace. Mostly.", "Probe schedule: full.", "The cows were volunteers."]


def generate(G):
    fn, wjson, title, tellraw, give = G.fn, G.wjson, G.title, G.tellraw, G.give
    PREFIX = G.PREFIX
    tick, fast, second = [], [], []
    ident = [F(0), F(0), F(0), F(1)]
    fin = ['execute rotated as @s run tp @e[tag=bm.new,distance=..2] ~ ~ ~ ~ 0', 'tag @e[tag=bm.new,distance=..2] remove bm.new']
    from phase20 import HELMS, SLOTS
    spawn = G.FUNCS['npc/spawn']
    spawn[0:0] = ['execute if entity @s[tag=bm.npc.donado_pen] run function bm:npc/donado_pen',
                  'execute if entity @s[tag=bm.npc.acrew] run function bm:npc/acrew',
                  'execute if entity @s[tag=bm.npc.abductee] run function bm:npc/abductee',
                  'execute if entity @s[tag=bm.npc.xholo] run function bm:npc/xholo']

    # ================================================================ Zorp is a Donadian now; the crew
    # (Zorp's sprite already uses the bm:alien3d model - the resource pack swaps it for a Donadian.)
    objs = ['bm.dng', 'bm.gy']
    G.FUNCS['load'][0:0] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    crew = []
    for suf in ALIEN_VARIANTS:
        tag = 'bm.av_' + (suf[1:] or 'crew')
        crew.append(f'execute if entity @s[tag={tag}] run ' + G.rat_sprite(f'bm:alien3d{suf}', ['bm.npc', 'bm.new', 'bm.rat_sprite', 'bm.acrew', 'bm.td', 'bm.r3d'], 0.85))
    fn('npc/acrew', crew + fin)
    def bubble(text, col, h):
        d = {'Tags': ['bm.bubble', 'bm.bnew'], 'text': T(text, col), 'billboard': 'center', 'background': Int(1879048192),
             'line_width': Int(150), 'brightness': {'block': Int(15), 'sky': Int(15)},
             'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0), F(0)], 'scale': [F(0), F(0), F(0)]}}
        return f'summon minecraft:text_display ~ ~{h} ~ {snbt(d)}'
    fn('p25/crew_say', ['execute store result score #c bm.rng run random value 1..40', 'execute unless score #c bm.rng matches 1 run return 0',
                        'execute if entity @e[type=minecraft:text_display,tag=bm.bubble,distance=..3] run return 0',
                        f'execute store result score #l bm.rng run random value 1..{len(CREW_SAYS)}'] +
       [f'execute if score #l bm.rng matches {i} run {bubble(t, "#b8ffb0", 1.7)}' for i, t in enumerate(CREW_SAYS, 1)] +
       ['playsound minecraft:entity.allay.ambient_without_item neutral @a[distance=..8] ~ ~ ~ 0.3 0.6'])
    second.append('execute as @e[type=minecraft:item_display,tag=bm.acrew] at @s if entity @a[distance=..7,gamemode=!spectator] run function bm:p25/crew_say')
    for kind in ('cow', 'pig', 'sheep'):
        d = {'Tags': ['bm.abductee', 'bm.seen'], 'PersistenceRequired': B(1), 'CustomName': T('Abductee', 'gray'), 'CustomNameVisible': B(0)}
        fn(f'p25/abduct_{kind}', [f'summon minecraft:{kind} ~ ~ ~ {snbt(d)}'])
    fn('npc/abductee', [f'execute if entity @s[tag=bm.ab_{k}] run function bm:p25/abduct_{k}' for k in ('cow', 'pig', 'sheep')])
    holo = {'Tags': ['bm.xholo', 'bm.new'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:xenite_green'}},
            'item_display': 'fixed', 'billboard': 'fixed', 'brightness': {'block': Int(15), 'sky': Int(15)}, 'teleport_duration': Int(5),
            'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0), F(0)], 'scale': [F(2.2), F(2.2), F(2.2)]}}
    fn('npc/xholo', [f'summon minecraft:item_display ~ ~ ~ {snbt(holo)}', 'tag @e[tag=bm.new,distance=..1] remove bm.new'])
    fast.append('execute as @e[type=minecraft:item_display,tag=bm.xholo] at @s if entity @a[distance=..32] run function bm:p25/holo')
    fn('p25/holo', ['tp @s ~ ~ ~ ~9 0', 'particle minecraft:end_rod ~ ~ ~ 0.4 0.4 0.4 0.01 1'])

    # ================================================================ the mothership: tractor beam (up), sneak to float down
    fast += ['execute as @e[type=minecraft:marker,tag=bm.tbeam] at @s if entity @a[distance=..240] run function bm:p25/beam']
    # the beam only reaches down to the first solid block (or water) under the ship: miners in caves below are left alone
    beam = ['execute unless entity @s[tag=bm.tscan] run function bm:p25/beam_scan',
            'execute store result score #my bm.rng run data get entity @s Pos[1]',
            'scoreboard players operation #lim bm.rng = @s bm.gy',
            'execute positioned ~-1.5 ~-232 ~-1.5 as @a[dx=2,dy=231,dz=2,gamemode=!spectator] at @s run function bm:p25/beam_ride',
            'execute as @a[distance=..2.2,tag=bm.bup] at @s run function bm:p25/beam_arrive']
    for k in range(1, 30):
        beam.append(f'execute if score @s bm.gy matches {k * 7}.. run particle minecraft:dust{{color:[0.49,1.0,0.42],scale:2.0}} ~ ~-{k * 7} ~ 0.7 2 0.7 0 2 force @a[distance=..160]')   # 2.23: only down to the ground
    beam.append('particle minecraft:end_rod ~ ~-3 ~ 0.5 1.5 0.5 0.02 3 force @a[distance=..96]')
    fn('p25/beam', beam)
    # going up is the default; one tap of sneak in the beam switches you to a gentle fall until you land
    fn('p25/beam_scan', ['tag @s add bm.tscan', 'scoreboard players set @s bm.gy 6', 'execute positioned ~ ~-6 ~ run function bm:p25/beam_scan_step',
                         'scoreboard players add @s bm.gy 2'])
    fn('p25/beam_scan_step', ['execute unless block ~ ~ ~ #minecraft:air run return 0', 'scoreboard players add @s bm.gy 1',
                              'execute if score @s bm.gy matches 230.. run return 0', 'execute positioned ~ ~-1 ~ run function bm:p25/beam_scan_step'])
    fn('p25/beam_ride', ['execute store result score #py bm.rng run data get entity @s Pos[1]',
                         'scoreboard players operation #d bm.rng = #my bm.rng', 'scoreboard players operation #d bm.rng -= #py bm.rng',
                         'execute if score #d bm.rng > #lim bm.rng run return 0',
                         'execute if predicate bm:p20/sneaking run tag @s add bm.bdown',
                         'execute if entity @s[tag=bm.bdown] run return run function bm:p25/beam_down',
                         'effect give @s minecraft:levitation 1 9 true', 'effect clear @s minecraft:slow_falling', 'tag @s add bm.bup'])
    fn('p25/beam_down', ['effect clear @s minecraft:levitation', 'effect give @s minecraft:slow_falling 4 0 true', 'tag @s remove bm.bup'])
    second += ['execute as @a[tag=bm.bdown] unless predicate bm:p21/airborne run tag @s remove bm.bdown',
               'execute as @a[tag=bm.bup] unless predicate bm:p21/airborne run tag @s remove bm.bup']
    fn('p25/beam_arrive', ['tag @s remove bm.bup', 'effect clear @s minecraft:levitation', 'effect give @s minecraft:slow_falling 2 0 true',
                           'tp @s @e[type=minecraft:marker,tag=bm.tland,sort=nearest,limit=1]',
                           'playsound minecraft:block.beacon.activate player @s ~ ~ ~ 1 1.6',
                           title('@s', 'actionbar', T('You are aboard the mothership. (Sneak in the beam to go back down.)', '#7dff6a'))])

    # ================================================================ Donado in the holding pen
    def don_item(pose, helm): return {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:donado',
                                                                                              'minecraft:custom_model_data': {'strings': [pose, helm]}}}
    pen = {'Tags': ['bm.npc', 'bm.new', 'bm.don_pen'], 'teleport_duration': Int(6), 'item': don_item('stand', 'none'),
           'item_display': 'fixed', 'billboard': 'fixed', 'shadow_radius': F(0.35),
           'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(DS / 2), F(0)], 'scale': [F(DS)] * 3}}
    box = {'Tags': ['bm.npc', 'bm.new', 'bm.don_hire'], 'width': F(1.2), 'height': F(1.3), 'response': B(1)}
    plate = {'Tags': ['bm.npc', 'bm.new', 'bm.don_plate'], 'billboard': 'center', 'default_background': B(0), 'background': Int(0x60000000),
             'text': [T('Donado', '#e8d29a', bold=True), T('\nabducted Earth-dog', 'gray', italic=True), T('\nright-click to set him free', 'yellow')],
             'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(1.6), F(0)], 'scale': [F(0.6)] * 3}}
    fn('npc/donado_pen', [f'summon minecraft:item_display ~ ~ ~ {snbt(pen)}', f'summon minecraft:interaction ~ ~ ~ {snbt(box)}',
                          f'summon minecraft:text_display ~ ~ ~ {snbt(plate)}'] + fin)
    fast += ['execute as @e[type=minecraft:item_display,tag=bm.don_pen] at @s if entity @a[distance=..24] run function bm:p25/don/pen_idle',
             'execute as @e[type=minecraft:item_display,tag=bm.don_pen] at @s if entity @a[distance=..32] run function bm:p19/look',
             'execute as @e[type=minecraft:interaction,tag=bm.don_hire] if data entity @s interaction at @s run function bm:p25/don/hire_click',
             'execute as @e[type=minecraft:interaction,tag=bm.don_hire] if data entity @s attack run data remove entity @s attack']
    fn('p25/don/pen_idle', ['execute store result score #h bm.rng run random value 1..14',
                            'execute if score #h bm.rng matches 1 run return run data modify entity @s item.components."minecraft:custom_model_data".strings[0] set value "blink"',
                            'execute if score #h bm.rng matches 2..4 run return run data modify entity @s item.components."minecraft:custom_model_data".strings[0] set value "breathe"',
                            'execute if score #h bm.rng matches 5..6 run return run data modify entity @s item.components."minecraft:custom_model_data".strings[0] set value "wag"',
                            'data modify entity @s item.components."minecraft:custom_model_data".strings[0] set value "stand"'])
    fn('p25/don/hire_click', ['execute on target at @s run function bm:p25/don/hire', 'tag @a remove bm.giver', 'data remove entity @s interaction'])
    fn('p25/don/hire', [
        'tag @s add bm.giver', 'tag @e[type=minecraft:wolf,tag=bm.dmine] remove bm.dmine',
        'execute as @e[type=minecraft:wolf,tag=bm.donado] if function bm:p20/frog/is_givers run tag @s add bm.dmine',
        'execute if entity @e[type=minecraft:wolf,tag=bm.dmine] run return run function bm:p25/don/recall',
        'execute as @e[type=minecraft:item_display,tag=bm.don_pen,sort=nearest,limit=1] if score @s bm.dng matches 1.. run return run ' +
        title('@a[tag=bm.giver]', 'actionbar', T('The cell is empty - Donado already escaped with someone. (He is back in a few minutes.)', 'gray')),
        'execute at @e[type=minecraft:item_display,tag=bm.don_pen,sort=nearest,limit=1] run function bm:p25/don/summon',
        'execute as @e[type=minecraft:item_display,tag=bm.don_pen,sort=nearest,limit=1] at @s run function bm:p25/don/pen_empty'])
    # the pen stands empty for 10 minutes after he walks out (then the aliens catch another... or the same one)
    def plate_text(t): return snbt({'text': t})
    full = [T('Donado', '#e8d29a', bold=True), T('\nabducted Earth-dog', 'gray', italic=True), T('\nright-click to set him free', 'yellow')]
    gone = [T('Specimen 042', '#e8d29a', bold=True), T('\nhas escaped!', 'gray', italic=True)]
    fn('p25/don/pen_empty', ['scoreboard players set @s bm.dng 600',
                             'data merge entity @s[type=minecraft:item_display] {transformation:{scale:[0f,0f,0f]}}',
                             f'data merge entity @e[type=minecraft:text_display,tag=bm.don_plate,distance=..2,limit=1] {plate_text(gone)}'])
    fn('p25/don/pen_tick', ['scoreboard players remove @s bm.dng 1', 'execute if score @s bm.dng matches 1.. run return 0',
                            f'data merge entity @s[type=minecraft:item_display] {{transformation:{{scale:[{DS}f,{DS}f,{DS}f]}}}}',
                            f'data merge entity @e[type=minecraft:text_display,tag=bm.don_plate,distance=..2,limit=1] {plate_text(full)}'])
    second.append('execute as @e[type=minecraft:item_display,tag=bm.don_pen,scores={bm.dng=1..}] at @s run function bm:p25/don/pen_tick')
    fn('p25/don/recall', ['tp @e[type=minecraft:wolf,tag=bm.dmine] @s', 'tag @e[type=minecraft:wolf,tag=bm.dmine] remove bm.dmine',
                          'playsound minecraft:entity.wolf.ambient neutral @a[distance=..16] ~ ~ ~ 1 1.2',
                          title('@s', 'actionbar', T('Donado is already with you - he bounds back to your side.', '#e8d29a'))])
    wolf = {'Tags': ['bm.donado', 'bm.dn_new', 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1),
            'CustomName': T('Donado', '#e8d29a', bold=True), 'CustomNameVisible': B(0), 'Health': F(40),
            'attributes': [{'id': 'minecraft:max_health', 'base': D(40)}, {'id': 'minecraft:attack_damage', 'base': D(5)},
                           {'id': 'minecraft:movement_speed', 'base': D(0.36)}, {'id': 'minecraft:follow_range', 'base': D(32)},
                           {'id': 'minecraft:step_height', 'base': D(1.0)}],
            'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0),
                                'show_icon': B(0), 'ambient': B(0)}],
            'drop_chances': {s: F(2.0) for s in ('mainhand', 'head', 'chest', 'legs', 'feet')}}
    body = {'Tags': ['bm.fp_disp', 'bm.dn_body', 'bm.dn_new'], 'teleport_duration': Int(2), 'shadow_radius': F(0.35), 'item': don_item('stand', 'none'),
            'item_display': 'fixed', 'billboard': 'fixed',
            'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(round(DS / 2 - WOLF_TOP, 3)), F(0)], 'scale': [F(DS)] * 3}}
    weap = {'Tags': ['bm.fp_disp', 'bm.fp_weap', 'bm.dn_weap', 'bm.dn_new'], 'teleport_duration': Int(2), 'item_display': 'fixed', 'billboard': 'fixed',
            'transformation': {'left_rotation': [F(v) for v in WEAP_ROT], 'right_rotation': ident,
                               'translation': [F(v) for v in weap_for('stand')], 'scale': [F(0.55)] * 3}}
    bag = {'Tags': ['bm.fp_disp', 'bm.fp_bag', 'bm.dn_new'],
           'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0), F(0)], 'scale': [F(0)] * 3}}
    fn('p25/don/summon', [
        f'summon minecraft:wolf ~ ~ ~ {snbt(wolf)}',
        'data modify entity @e[type=minecraft:wolf,tag=bm.dn_new,limit=1,sort=nearest] Owner set from entity @s UUID',
        f'summon minecraft:item_display ~ ~ ~ {snbt(body)}', f'summon minecraft:item_display ~ ~ ~ {snbt(weap)}',
        f'summon minecraft:item_display ~ ~ ~ {snbt(bag)}',
        'execute as @e[type=minecraft:item_display,tag=bm.dn_new,distance=..2] run ride @s mount @e[type=minecraft:wolf,tag=bm.dn_new,limit=1,sort=nearest]',
        'tag @e[tag=bm.dn_new,distance=..3] remove bm.dn_new',
        'particle minecraft:happy_villager ~ ~0.5 ~ 0.5 0.4 0.5 0 15',
        'playsound minecraft:entity.wolf.ambient neutral @a[distance=..16] ~ ~ ~ 1 1.3',
        'title @s times 10 50 15', title('@s', 'subtitle', T('Hand him a weapon or armour to equip him', 'gray', italic=True)),
        title('@s', 'title', T('Donado is free!', '#e8d29a', bold=True)),
        tellraw('@s', PREFIX + [T('Donado follows you, fights what you fight and defends you. ', '#e8d29a'),
                                T('Right-click him holding a weapon or armour to equip it; empty-handed to make him wait or follow; ', 'gray'),
                                T('sneak + right-click empty-handed to take your gear back. Feed him any meat to heal him.', 'gray')])])

    # ================================================================ equipping: the shared ally pipeline (phase 1.10 frog)
    wjson('bm/advancement/donado_interact.json', {'criteria': {'i': {'trigger': 'minecraft:player_interacted_with_entity', 'conditions': {
        'entity': [{'condition': 'minecraft:entity_properties', 'entity': 'this',
                    'predicate': {'minecraft:entity_type': 'minecraft:wolf', 'minecraft:nbt': '{Tags:["bm.donado"]}'}}]}}}, 'rewards': {'function': 'bm:p25/don/interact'}})
    sel = '@e[type=minecraft:wolf,tag=bm.fsel,limit=1,sort=nearest]'
    fn('p25/don/interact', [
        'advancement revoke @s only bm:donado_interact', 'tag @s add bm.giver',
        'execute as @e[type=minecraft:wolf,tag=bm.donado,distance=..8] if function bm:p20/frog/is_givers run tag @s add bm.fsel',
        f'execute as {sel} on passengers if entity @s[tag=bm.fp_bag] run tag @s add bm.fbag',
        f'execute if entity {sel} run function bm:p20/frog/route',
        'tag @e[tag=bm.fsel] remove bm.fsel', 'tag @e[tag=bm.fbag] remove bm.fbag', 'tag @s remove bm.giver'])
    G.FUNCS['p20/frog/msg_give'] += [
        'execute if entity @s[tag=bm.donado] run playsound minecraft:entity.wolf.ambient neutral @a[distance=..16] ~ ~ ~ 0.8 1.4',
        'execute if entity @s[tag=bm.donado] run ' + title('@a[tag=bm.giver]', 'actionbar', T('Donado takes it and wags his tail. Good boy.', '#e8d29a')),
        'execute if entity @s[tag=bm.donado] run function bm:p25/don/refresh']
    G.FUNCS['p20/frog/msg_strip'] += [
        'execute if entity @s[tag=bm.donado] run ' + title('@a[tag=bm.giver]', 'actionbar', T('Donado drops your gear at your feet.', '#e8d29a')),
        'execute if entity @s[tag=bm.donado] run function bm:p25/don/refresh']
    refresh = ['execute on passengers if entity @s[tag=bm.dn_body] run data modify entity @s item.components."minecraft:custom_model_data".strings[1] set value "none"',
               'execute if items entity @s armor.head * on passengers if entity @s[tag=bm.dn_body] run data modify entity @s item.components."minecraft:custom_model_data".strings[1] set value "iron"']
    refresh += [f'execute if items entity @s armor.head minecraft:{hid} on passengers if entity @s[tag=bm.dn_body] run data modify entity @s item.components."minecraft:custom_model_data".strings[1] set value "{m}"'
                for hid, m in HELMS]
    fn('p25/don/refresh', refresh)

    # ================================================================ Donado's animation (as the wolf; every 2nd tick near players)
    tick += ['execute as @e[type=minecraft:wolf,tag=bm.donado] at @s on passengers run rotate @s ~ 0',
             'execute as @e[type=minecraft:wolf,tag=bm.donado] at @s if entity @a[distance=..48] run function bm:p25/don/anim']
    fn('p25/don/anim', ['scoreboard players add @s bm.fa 1', 'execute if score @s bm.fa matches 64.. run scoreboard players set @s bm.fa 0',
                        'scoreboard players operation #f bm.rng = @s bm.fa', 'scoreboard players operation #f bm.rng %= #2 bm.rng',
                        'execute unless score #f bm.rng matches 0 run return 0',
                        'execute if predicate bm:p21/airborne run return run function bm:p25/don/pose_jump',
                        'execute if data entity @s {Sitting:1b} run return run function bm:p25/don/pose_crouch',
                        'execute if predicate bm:p21/running run return run function bm:p25/don/run',
                        'execute if predicate bm:p21/walking run return run function bm:p25/don/walk',
                        'function bm:p25/don/idle'])
    fn('p25/don/walk', ['scoreboard players operation #w bm.rng = @s bm.fa', 'scoreboard players operation #w bm.rng /= #2 bm.rng',
                        'scoreboard players operation #w bm.rng %= #4 bm.rng',
                        'execute if score #w bm.rng matches 0 run return run function bm:p25/don/pose_walk1',
                        'execute if score #w bm.rng matches 2 run return run function bm:p25/don/pose_walk2',
                        'function bm:p25/don/pose_stand'])
    fn('p25/don/run', ['scoreboard players operation #w bm.rng = @s bm.fa', 'scoreboard players operation #w bm.rng /= #2 bm.rng',
                       'scoreboard players operation #w bm.rng %= #2 bm.rng',
                       'execute if score #w bm.rng matches 0 run return run function bm:p25/don/pose_run1',
                       'function bm:p25/don/pose_run2'])
    fn('p25/don/idle', ['execute if score @s bm.fa matches 0..11 run return run function bm:p25/don/pose_breathe',
                        'execute if score @s bm.fa matches 30..31 run return run function bm:p25/don/pose_blink',
                        'execute if score @s bm.fa matches 44..55 run return run function bm:p25/don/pose_wag',
                        'function bm:p25/don/pose_stand'])
    for name, pid, bob in DON_POSES:
        fy = round(DS / 2 - WOLF_TOP + bob, 3)
        wx, wy, wz = weap_for(name, bob)
        fn(f'p25/don/pose_{name}', [
            f'execute if score @s bm.fp matches {pid} run return 0', f'scoreboard players set @s bm.fp {pid}',
            f'execute on passengers if entity @s[tag=bm.dn_body] run data modify entity @s item.components."minecraft:custom_model_data".strings[0] set value "{name}"',
            f'execute on passengers if entity @s[tag=bm.dn_body] run data merge entity @s[type=minecraft:item_display] {{start_interpolation:0,interpolation_duration:2,transformation:{{translation:[0f,{fy}f,0f]}}}}',
            f'execute on passengers if entity @s[tag=bm.dn_weap] run data merge entity @s[type=minecraft:item_display] {{start_interpolation:0,interpolation_duration:2,transformation:{{left_rotation:[{WEAP_ROT[0]}f,{WEAP_ROT[1]}f,{WEAP_ROT[2]}f,{WEAP_ROT[3]}f],translation:[{wx}f,{wy}f,{wz}f]}}}}'])
    second += ['effect give @e[type=minecraft:wolf,tag=bm.donado] minecraft:regeneration 3 0 true',
               'execute as @e[type=minecraft:wolf,tag=bm.donado] at @s if predicate bm:p20/croak run playsound minecraft:entity.wolf.ambient neutral @a[distance=..16] ~ ~ ~ 0.7 1.3']

    # ================================================================ the mothership chart (sold by Zorp)
    G.consume_adv('sealed_map_mothership', 'bm:maps/open_mothership')
    fn('maps/open_mothership', ['advancement revoke @s only bm:consume/sealed_map_mothership', 'loot give @s loot bm:maps/mothership',
                                title('@s', 'actionbar', T('The seal cracks... the chart marks an alien mothership.', '#7dff6a'))])
    wjson('bm/loot_table/maps/mothership.json', {'type': 'minecraft:command', 'pools': [{'rolls': 1, 'entries': [{
        'type': 'minecraft:item', 'name': 'minecraft:filled_map', 'functions': [     # 26.3: exploration_map stamps the input item, so start from a filled map
            {'function': 'minecraft:exploration_map', 'destination': 'bm:mothership', 'decoration': 'minecraft:target_x', 'zoom': 2,
             'search_radius': 100, 'skip_existing_chunks': False},
            {'function': 'minecraft:set_name', 'target': 'item_name', 'name': T('Mothership Chart', '#7dff6a')}]}]}]})

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


def post_admin(G):
    G.FUNCS['admin/help'] += [
        G.tellraw('@s', [T('/function bm:admin/place_mothership', 'yellow'), T('  builds a mothership 40 blocks above you (stand in the beam)', 'gray')]),
        G.tellraw('@s', [T('/locate structure bm:mothership', 'yellow'), T('  finds the nearest mothership', 'gray')])]
    G.fn('admin/place_mothership', [f'execute positioned ~ ~40 ~ run place template bm:mothership ~-{MC} ~-2 ~-{MC}',
                                    G.tellraw('@s', G.PREFIX + [T('Mothership placed overhead. Its tractor beam is right where you stand.', 'gray')])])


# ===================================================================== the mothership structure
MS, MSY = 51, 30
MC = 25
SKY_Y = 196               # the template's floor; the beam's mouth hangs at ~y198, the decks at ~y203/208


def build_mothership(red=False):
    """red=True: the Vorn Dreadnought (2.13) - the same hull recoloured red, hostile guards instead of crew, red Xenite in the
    reactor, an armoury chest instead of the quartermaster and an abducted villager instead of Donado."""
    from structures import Build
    import market2
    rnd = random.Random(1947)
    Bd = Build(MS, MSY, MS)
    S = Bd.set
    UNDER = ['gray_concrete'] * 4 + ['cyan_terracotta', 'polished_andesite']
    FLOOR = ['smooth_quartz'] * 3 + ['white_concrete', 'polished_diorite']
    def r_of(x, z): return math.hypot(x - MC, z - MC)
    def ybot(r): return 2 + round(5 * (r / 24) ** 2)
    def ytop(r): return 19 - round(6 * (r / 22) ** 2)
    LD, MD = 6, 11            # lower-deck floor, main-deck floor
    # ---------------- hull
    for x in range(MS):
        for z in range(MS):
            r = r_of(x, z)
            if r > 24.4: continue
            yb = ybot(min(r, 24))
            yt = ytop(r) if r <= 21.6 else max(12, ytop(min(r - 1.0, 22)))     # the rim stands as tall as the deck inside it
            for y in range(yb, yt + 1):
                outer = (y == yb) or (y == yt) or r > 21.6
                if outer:                                            # panelled rings, with seams every 45 degrees
                    ring = int(r) % 5 == 0 or (abs(math.degrees(math.atan2(z - MC, x - MC))) % 45) < 1.4
                    S(x, y, z, ('gray_concrete' if not ring else 'cyan_terracotta') if y <= 8 else ('iron_block' if ring else 'light_gray_concrete'))
                else:
                    S(x, y, z, 'air')
            if 21.6 < r <= 24.4:                                     # the rim: a band of green running lights
                S(x, 9, z, 'verdant_froglight[axis=y]' if (x + z) % 3 == 0 else 'lime_stained_glass')
                S(x, 10, z, 'gray_concrete')
    # decks
    for x in range(MS):
        for z in range(MS):
            r = r_of(x, z)
            if r <= 21.6:
                for y in range(ybot(r) + 1, LD): S(x, y, z, rnd.choice(UNDER))      # solid belly under the lower deck
                S(x, LD, z, rnd.choice(FLOOR))
                S(x, MD, z, rnd.choice(FLOOR) if r > 8.5 else 'cyan_stained_glass')   # glass floor under the dome
    # the dome over the main deck centre
    def in_dome(x, y, z): return y >= ytop(0) and math.sqrt((x - MC) ** 2 + (z - MC) ** 2 + ((y - ytop(0)) * 1.15) ** 2) < 9.6
    for x in range(MS):
        for z in range(MS):
            for y in range(ytop(0), MSY):
                if not in_dome(x, y, z): continue
                if any(not in_dome(x + a, y + b, z + c) for a, b, c in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, -1))):
                    if r_of(x, z) > 8.6 or y > ytop(0): S(x, y, z, 'light_blue_stained_glass' if (y - ytop(0)) % 3 else 'smooth_quartz')
                else:
                    S(x, y, z, 'air')
    for x in range(MS):
        for z in range(MS):
            if r_of(x, z) <= 8.5:
                for y in range(MD + 1, ytop(0) + 1): S(x, y, z, 'air')
    # ---------------- tractor-beam shaft (3x3) through the belly into the lower deck
    for x in range(MC - 1, MC + 2):
        for z in range(MC - 1, MC + 2):
            for y in range(ybot(0), LD + 1): S(x, y, z, 'air')
    for x in range(MC - 2, MC + 3):
        for z in range(MC - 2, MC + 3):
            if max(abs(x - MC), abs(z - MC)) == 2:
                for y in range(ybot(0), LD): S(x, y, z, 'verdant_froglight[axis=y]' if (x + z) % 2 else 'lime_stained_glass')
                S(x, LD + 1, z, 'lime_stained_glass_pane' if (x, z) not in ((MC, MC + 2), (MC, MC - 2), (MC + 2, MC), (MC - 2, MC)) else 'air')
    Bd.marker(MC + 0.5, LD + 1.0, MC + 0.5, ['bm.tbeam'], 0)
    Bd.marker(MC + 0.5, LD + 1, MC + 5.5, ['bm.tland'], 180)
    Bd.sign(MC + 3, LD + 1, MC + 3, 'birch_sign[rotation=2,waterlogged=false]', ['TRACTOR BEAM', 'Step in to', 'leave. SNEAK', 'to float down.'], color='lime', glow=True)
    # ---------------- lower deck: holding pen (north), reactor (south), stores (east/west)
    def walls(x1, z1, x2, z2, y1, y2, st, door=None):
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1):
                if x in (x1, x2) or z in (z1, z2):
                    for y in range(y1, y2 + 1):
                        if door and (x, z) in door: continue
                        S(x, y, z, st)
    cells = [(15, 14, 'cow'), (20, 12, 'sheep'), (30, 12, 'pig'), (35, 14, 'donado')]
    for (cx, cz, who) in cells:
        x1, z1, x2, z2 = cx - 2, cz - 2, cx + 2, cz + 2
        walls(x1, z1, x2, z2, LD + 1, LD + 4, 'light_blue_stained_glass_pane' if who != 'donado' else 'iron_bars', door=None if who != 'donado' else {(cx, z2), (cx - 1, z2), (cx + 1, z2)})
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1): S(x, LD, z, 'hay_block[axis=y]' if who != 'donado' and (x + z) % 3 == 0 else 'polished_diorite')
        S(cx, MD, cz, 'sea_lantern')
        if who == 'donado':
            S(cx + 1, LD + 1, cz, 'red_bed[facing=north,occupied=false,part=foot]'); S(cx + 1, LD + 1, cz - 1, 'red_bed[facing=north,occupied=false,part=head]')
            S(cx - 1, LD + 1, cz - 1, 'cauldron'); S(cx - 1, LD + 1, cz, 'bone_block[axis=x]')
            Bd.marker(cx + 0.5, LD + 1, cz + 0.5, ['bm.npc_spawn', 'bm.npc.donado_pen'], 0)
            Bd.sign(cx + 2, LD + 1, z2 + 1, 'birch_sign[rotation=0,waterlogged=false]', ['SPECIMEN 042', 'Earth-dog', '(very good boy)', 'DO NOT RELEASE'], color='red', glow=True)
        else:
            for k in range(2): Bd.marker(cx + 0.5 - k, LD + 1, cz + 0.5, ['bm.npc_spawn', 'bm.npc.abductee', f'bm.ab_{who}'], 0)
    # reactor: a glowing core ringed by Xenite deposits
    for y in range(LD + 1, MD):
        S(MC, y, MC + 12, 'sea_lantern' if y % 2 else 'lime_stained_glass')
    for (dx, dz, c) in [(2, 0, 'green'), (-2, 0, 'violet'), (0, 2, 'cyan'), (0, -2, 'green'), (2, 2, 'violet'), (-2, -2, 'cyan')]:
        x, z = MC + dx, MC + 12 + dz
        S(x, LD + 1, z, 'amethyst_block')
        Bd.marker(x + 0.5, LD + 1.5, z + 0.5, ['bm.npc_spawn', 'bm.npc.xenite', f'bm.xc_{c}'], 0)
    walls(MC - 4, MC + 8, MC + 4, MC + 16, LD + 1, LD + 1, 'iron_bars', door={(MC, MC + 8), (MC - 1, MC + 8), (MC + 1, MC + 8)})
    Bd.sign(MC + 2, LD + 2, MC + 7, 'birch_sign[rotation=8,waterlogged=false]', ['REACTOR', 'Xenite core.', 'Do not lick.', ''], color='lime', glow=True)
    stores = 'bm:p32/dread_stores' if red else 'bm:p32/mothership_stores'
    for i, (x, z) in enumerate([(8, 25), (8, 26), (9, 24), (42, 25), (42, 26), (41, 27), (10, 31), (40, 20)]):
        pick = rnd.choice(['barrel[facing=up,open=false]', 'iron_block', 'light_gray_shulker_box[facing=up]'])
        if i in (0, 3, 6, 7):        # 2.13: four of them are supply barrels with loot (shards and supplies, never Zorp's goods)
            S(x, LD + 1, z, 'barrel[facing=up,open=false]', {'id': 'minecraft:barrel', 'LootTable': stores})
        else:
            S(x, LD + 1, z, pick)
    # ---------------- stairs up to the main deck (east): x37-38, rising north z30 (y7) -> z25 (y11)
    for k in range(5):
        z = 30 - k
        for x in (37, 38):
            S(x, LD + 1 + k, z, 'quartz_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]')
            for yy in range(LD + 1, LD + 1 + k): S(x, yy, z, 'smooth_quartz')
            for yy in range(LD + 2 + k, LD + 6 + k):
                if yy < MSY and Bd.b.get((x, yy, z)) != 'minecraft:air' and yy >= MD: S(x, yy, z, 'air')
    # ---------------- main deck: bridge (north), lab (west), quarters (east), the dome (centre)
    for x in range(MC - 7, MC + 8):                          # the bridge console arc
        z = 9 + round(abs(x - MC) ** 2 / 14)
        S(x, MD + 1, z, 'cyan_terracotta'); S(x, MD + 2, z, 'light_blue_stained_glass' if x % 2 else 'end_rod[facing=up]')
    S(MC, MD + 1, 12, 'quartz_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]')
    for (x, y, z), st in list(Bd.b.items()):              # a wrap-around viewport in the bow
        if y in (MD + 1, MD + 2) and z < MC - 12 and abs(x - MC) <= 7 and r_of(x, z) > 21.6:
            S(x, y, z, 'light_blue_stained_glass')
    for (x, z) in [(10, 22), (10, 24), (10, 26), (11, 28)]:  # the lab
        S(x, MD + 1, z, rnd.choice(['brewing_stand[has_bottle_0=true,has_bottle_1=false,has_bottle_2=true]', 'cauldron', 'tinted_glass', 'end_rod[facing=up]']))
    for (x, z) in [(12, 20), (12, 30)]:
        S(x, MD + 1, z, 'tinted_glass'); S(x, MD + 2, z, 'slime_block')                    # specimen jars
    for (x, z) in [(40, 18), (40, 20), (41, 30), (40, 32)]:  # crew quarters (bunks of light-grey beds)
        S(x, MD + 1, z, 'light_gray_bed[facing=east,occupied=false,part=foot]'); S(x + 1, MD + 1, z, 'light_gray_bed[facing=east,occupied=false,part=head]')
    # the mess hall (south): tables, stools and the quartermaster's counter
    for (tx, tz) in [(20, 36), (20, 40), (30, 36), (30, 40)]:
        for dx in (0, 1):
            S(tx + dx, MD + 1, tz, 'smooth_quartz_slab[type=top,waterlogged=false]')
            S(tx + dx, MD + 1, tz - 1, 'quartz_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]')
            S(tx + dx, MD + 1, tz + 1, 'quartz_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]')
    for x in range(MC - 2, MC + 3): S(x, MD + 1, 38, 'cyan_terracotta')
    S(MC - 2, MD + 2, 38, 'end_rod[facing=up]'); S(MC + 2, MD + 2, 38, 'end_rod[facing=up]')
    # rooms: a glass ring around the dome (doors at the four points) and stepped diagonal bulkheads between
    # bridge (N), lab (W), quarters (E) and mess (S)
    for x in range(MS):
        for z in range(MS):
            r = r_of(x, z); dx, dz = abs(x - MC), abs(z - MC)
            if 9.6 <= r < 10.6 and dx > 1 and dz > 1:
                for y in range(MD + 1, MD + 4):
                    if Bd.b.get((x, y, z)) == 'minecraft:air': S(x, y, z, 'white_stained_glass_pane')
            elif 10.6 <= r <= 21.6 and 0 <= dx - dz <= 1:
                for y in range(MD + 1, ytop(min(r, 22))):
                    if Bd.b.get((x, y, z)) == 'minecraft:air':
                        S(x, y, z, 'light_blue_stained_glass' if y == MD + 2 and 12 < r < 19 else 'smooth_quartz')
    # ceiling lights everywhere both decks
    for x in range(MS):
        for z in range(MS):
            r = r_of(x, z)
            if (x % 5 == 0 and z % 5 == 0) and r <= 19.5:
                if Bd.b.get((x, MD, z), '').endswith('quartz') or 'concrete' in Bd.b.get((x, MD, z), '') or 'diorite' in Bd.b.get((x, MD, z), ''):
                    S(x, MD, z, 'sea_lantern')
                t = ytop(min(r, 22))
                if r <= 18 and r > 8.6 and Bd.b.get((x, t, z), '') not in ('minecraft:air',): S(x, t, z, 'sea_lantern')
    # ---------------- crew, quartermaster, hologram
    crew = [(MC - 3, MD + 1, 11, 180, 'off'), (MC + 3, MD + 1, 11, 180, 'crew'), (MC, MD + 1, 13, 180, 'off'),     # bridge
            (11, MD + 1, 25, 90, 'sci'), (13, MD + 1, 21, 90, 'sci'),                                                   # lab
            (39, MD + 1, 25, -90, 'crew'), (MC + 3, LD + 1, MC + 10, 180, 'sci'), (MC - 3, LD + 1, MC + 9, 180, 'crew'),  # quarters, reactor
            (25, LD + 1, 16, 0, 'off'), (14, LD + 1, 25, 90, 'crew')]                                                   # pen guard, stores
    for (x, y, z, yaw, v) in crew:
        Bd.marker(x + 0.5, y, z + 0.5, ['bm.npc_spawn', 'bm.npc.acrew', f'bm.av_{v}'], yaw)
    Bd.marker(MC + 0.5, MD + 1, 39.5, ['bm.npc_spawn', 'bm.npc.alien'], 180)             # the quartermaster (Zorp's offers), behind his counter
    Bd.marker(MC + 0.5, MD + 3.5, MC + 0.5, ['bm.npc_spawn', 'bm.npc.xholo'], 0)
    for (x, z) in [(MC - 1, MC), (MC + 1, MC), (MC, MC - 1), (MC, MC + 1)]: S(x, MD + 1, z, 'end_rod[facing=up]')
    S(MC, MD + 1, MC, 'sea_lantern')
    if red: _vornify(Bd, MD, LD)
    lights = market2.spawnproof(Bd, fix=True)
    Bd.meta = {'lights': lights}
    return Bd


_RED_SWAP = {'lime_stained_glass': 'red_stained_glass', 'lime_stained_glass_pane': 'red_stained_glass_pane', 'verdant_froglight': 'shroomlight',
             'cyan_terracotta': 'red_terracotta', 'light_blue_stained_glass': 'red_stained_glass', 'cyan_stained_glass': 'red_stained_glass',
             'white_stained_glass_pane': 'red_stained_glass_pane', 'light_gray_concrete': 'gray_concrete', 'smooth_quartz': 'polished_deepslate',
             'white_concrete': 'black_concrete', 'polished_diorite': 'polished_blackstone'}


def _vornify(Bd, MD, LD):
    """Recolour the hull and swap the friendly crew for the Vorn (the Dreadnought)."""
    from structures import parse_state, state_str
    for pos, st in list(Bd.b.items()):
        name, props = parse_state(st)
        short = name.split(':')[1]
        if short in _RED_SWAP:
            new = _RED_SWAP[short]
            if new == 'shroomlight': props = {}
            Bd.b[pos] = state_str('minecraft:' + new, props if new not in ('red_stained_glass', 'polished_deepslate', 'black_concrete', 'polished_blackstone', 'gray_concrete', 'red_terracotta') else {})
    for (pos, nb) in list(Bd.nbt.items()):
        if nb.get('id') in ('minecraft:sign', 'minecraft:hanging_sign'):
            nb['front_text']['color'] = 'red'
    keep = []
    for e in Bd.ents:
        t = e['nbt']['Tags']
        if 'bm.npc.acrew' in t:
            e['nbt']['Tags'] = ['bm.vguard']
        elif 'bm.npc.alien' in t:
            e['nbt']['Tags'] = ['bm.vguard_boss']
        elif 'bm.npc.donado_pen' in t:
            e['nbt']['Tags'] = ['bm.npc_spawn', 'bm.npc.abductee', 'bm.ab_villager']
        elif 'bm.npc.xholo' in t:
            e['nbt']['Tags'] = ['bm.npc_spawn', 'bm.npc.xholo_red']
        elif 'bm.tbeam' in t:
            e['nbt']['Tags'] = ['bm.tbeam_red']
        elif 'bm.npc.xenite' in t:
            e['nbt']['Tags'] = ['bm.npc_spawn', 'bm.npc.xenite', 'bm.xc_red']
        keep.append(e)
    Bd.ents = keep
    Bd.marker(MC + 0.5, MD + 1, MC + 0.5, ['bm.dread_core'], 0)
    # the armoury: on the bridge, behind the captain's console
    Bd.set(MC, MD + 1, 10, 'chest[facing=south,type=single,waterlogged=false]', {'id': 'minecraft:chest', 'LootTable': 'bm:p32/dread_armory'})
    Bd.set(MC - 1, MD + 1, 10, 'redstone_block'); Bd.set(MC + 1, MD + 1, 10, 'redstone_block')
    for (pos, nb) in list(Bd.nbt.items()):
        if nb.get('id') in ('minecraft:sign',) and nb['front_text']['messages'][0]['text'] == 'SPECIMEN 042':
            nb['front_text']['messages'] = [{'text': 'SPECIMEN 117'}, {'text': 'Earth-farmer'}, {'text': 'for improvement'}, {'text': 'HIVE PROPERTY'}]


def check_mothership(Bd):
    """Static proofs: the beam lands you on the deck; Donado, the quartermaster and every crew member can be walked to
    from the landing; everything walkable is lit; the hull is closed except the beam shaft."""
    import market2
    import p2.verify as V
    from p2.verify import Grid, reach
    errs = []
    G = Grid(Bd, outside='void')
    V.GRID = G
    land = next(e['pos'] for e in Bd.ents if 'bm.tland' in e['nbt']['Tags'])
    seen = G.bfs([(int(land[0]), int(land[1]), int(land[2]))], margin=0)
    if len(seen) < 200: errs.append(f'landing area too small ({len(seen)} cells)')
    for e in Bd.ents:
        t = e['nbt']['Tags']; x, y, z = e['pos']
        if any(k in t for k in ('bm.npc.donado_pen', 'bm.npc.alien', 'bm.npc.acrew')):
            if not reach(seen, int(x), int(y), int(z), 4.5): errs.append(f'{[k for k in t if k.startswith("bm.npc.")][0]} at {(x, y, z)} not reachable from the landing')
    dark = market2.spawnproof(Bd, fix=False)
    if dark: errs.append(f'{len(dark)} dark walkable cells, e.g. {dark[:4]}')
    # sealed: open cells inside the hull never touch the sky, except via the beam shaft
    for (x, y, z), st in Bd.b.items():
        if not (st.endswith(':air') or ':light[' in st): continue
        if abs(x - MC) <= 1 and abs(z - MC) <= 1 and y <= 6: continue
        for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            n = (x + d[0], y + d[1], z + d[2])
            if n not in Bd.b: errs.append(f'open cell {(x, y, z)} {st} touches the sky'); break
    return sorted(set(errs))


# ===================================================================== resource pack
def textures():
    from PIL import Image
    rnd = random.Random(42)
    out = {}
    def tex(base, var=10, spots=None):
        im = Image.new('RGBA', (16, 16))
        for x in range(16):
            for y in range(16):
                n = rnd.randrange(-var, var + 1)
                im.putpixel((x, y), tuple(max(0, min(255, c + n)) for c in base) + (255,))
        for (x, y, c) in spots or []:
            im.putpixel((x, y), c + (255,))
        return im
    out['don_fur'] = tex((232, 210, 154), 8)
    out['don_muzzle'] = tex((246, 234, 200), 5)
    out['don_ear'] = tex((214, 182, 108), 8)
    out['don_dark'] = tex((24, 20, 18), 3)
    out['don_tongue'] = tex((226, 120, 140), 6)
    shirt = tex((128, 130, 136), 9)
    for x in range(16):                                  # stitched seams and a couple of holes: scrappy
        shirt.putpixel((x, 5), (96, 98, 104, 255))
        if x % 3 == 0: shirt.putpixel((x, 4), (176, 176, 170, 255))
    for (x, y) in ((3, 10), (4, 10), (3, 11), (11, 2), (12, 2)): shirt.putpixel((x, y), (60, 58, 56, 255))
    out['don_shirt'] = shirt
    patch = tex((86, 88, 96), 6)
    for i in range(16):
        patch.putpixel((i, 0), (200, 196, 180, 255)); patch.putpixel((0, i), (200, 196, 180, 255))
        if i % 2 == 0: patch.putpixel((i, 15), (200, 196, 180, 255)); patch.putpixel((15, i), (200, 196, 180, 255))
    out['don_patch'] = patch
    # the Donadians (from the player's build: prismarine-teal skin with darker patches, a dark coat)
    skin = tex((46, 178, 170), 10)
    for _ in range(26):
        x, y = rnd.randrange(16), rnd.randrange(16)
        skin.putpixel((x, y), (26, 112, 120, 255)); skin.putpixel(((x + 1) % 16, y), (26, 112, 120, 255))
    out['adon_skin'] = skin
    out['adon_dark'] = tex((22, 96, 104), 8)
    out['adon_eye'] = tex((255, 40, 30), 10, [(4, 4, (255, 200, 190)), (5, 4, (255, 200, 190))])
    out['adon_mouth'] = tex((14, 12, 18), 3)
    out['adon_antenna'] = tex((232, 232, 240), 6)
    out['adon_disc'] = tex((150, 255, 60), 14, [(x, 7, (230, 255, 200)) for x in range(16)])
    out['adon_coat'] = tex((58, 52, 66), 9)
    out['adon_labcoat'] = tex((226, 230, 236), 7)
    out['adon_redcoat'] = tex((120, 26, 36), 9)
    return out


def _c(fr, to, t, rot=None):
    from gen_rp import cube
    e = cube(fr, to, t)
    if rot: e['rotation'] = rot
    return e


def _mv(e, dx=0.0, dy=0.0, dz=0.0):
    import copy
    e = copy.deepcopy(e)
    e['from'] = [e['from'][0] + dx, e['from'][1] + dy, e['from'][2] + dz]
    e['to'] = [e['to'][0] + dx, e['to'][1] + dy, e['to'][2] + dz]
    if 'rotation' in e:
        o = e['rotation']['origin']; e['rotation']['origin'] = [o[0] + dx, o[1] + dy, o[2] + dz]
    return e


def _rot(e, axis, angle, origin):
    import copy
    e = copy.deepcopy(e)
    if angle: e['rotation'] = {'origin': list(origin), 'axis': axis, 'angle': angle}
    return e


def donado_parts():
    """Donado (faces -z): groups of cubes so poses can move limbs."""
    P = {}
    P['legL'] = [_c((5, 0, 7), (7.2, 5, 9.6), 'f'), _c((4.6, 0, 6), (7.4, 1, 9.8), 'm')]
    P['legR'] = [_c((8.8, 0, 7), (11, 5, 9.6), 'f'), _c((8.6, 0, 6), (11.4, 1, 9.8), 'm')]
    P['torso'] = [_c((4.6, 5, 6.5), (11.4, 12, 10.4), 's'),
                  _c((5, 4.4, 6.4), (6.2, 5.2, 10.5), 's'), _c((7.6, 4.6, 6.4), (8.6, 5.2, 10.5), 's'), _c((9.9, 4.3, 6.4), (11, 5.2, 10.5), 's'),  # ragged hem
                  _c((5.8, 8.2, 6.35), (7.8, 10.2, 6.5), 'p'), _c((8.6, 6.2, 10.4), (10.6, 8.2, 10.55), 'p')]       # patches
    P['armL'] = [_c((3, 8.8, 7.4), (4.6, 11.8, 9.4), 's'), _c((3.1, 6, 7.5), (4.5, 8.8, 9.3), 'f'), _c((3, 5.4, 7.4), (4.6, 6.2, 9.4), 'm')]
    P['armR'] = [_c((11.4, 8.8, 7.4), (13, 11.8, 9.4), 's'), _c((11.5, 6, 7.5), (12.9, 8.8, 9.3), 'f'), _c((11.4, 5.4, 7.4), (13, 6.2, 9.4), 'm')]
    P['head'] = [_c((3.6, 12, 5), (12.4, 19, 11), 'f'),
                 _c((5.8, 12.4, 3.4), (10.2, 15.2, 5), 'm'),                                    # muzzle
                 _c((7.1, 14.3, 3.2), (8.9, 15.4, 3.45), 'k'),                                  # nose
                 _c((6.7, 13.1, 3.32), (9.3, 13.35, 3.45), 'k'), _c((7.5, 12.5, 3.3), (8.5, 13.1, 3.42), 't'),   # smile + tongue
                 _c((2.4, 12.6, 6), (3.7, 18.4, 9.6), 'e'), _c((12.3, 12.6, 6), (13.6, 18.4, 9.6), 'e')]          # floppy ears
    P['eyes'] = [_c((5, 15.6, 4.88), (6.6, 17.3, 5.0), 'k'), _c((9.4, 15.6, 4.88), (11, 17.3, 5.0), 'k'),
                 _c((5.2, 16.6, 4.86), (5.7, 17.1, 4.9), 'm'), _c((9.6, 16.6, 4.86), (10.1, 17.1, 4.9), 'm')]
    P['tail'] = [_c((7.3, 6.2, 10.4), (8.7, 7.6, 13.4), 'f')]
    return P


DON_TEX = {'f': 'bm:block/don_fur', 'm': 'bm:block/don_muzzle', 'e': 'bm:block/don_ear', 'k': 'bm:block/don_dark',
           't': 'bm:block/don_tongue', 's': 'bm:block/don_shirt', 'p': 'bm:block/don_patch'}


def donado_pose(pose, parts=False):
    """-> (cubes, head dy, head dz), or the posed part groups with parts=True"""
    P = donado_parts()
    up = ('torso', 'armL', 'armR', 'head', 'eyes', 'tail')
    hip = (8, 5, 8.3); shL = (3.8, 11.6, 8.4); shR = (12.2, 11.6, 8.4)
    dy = dz = 0.0
    def move(names, ddy=0.0, ddz=0.0):
        for n in names: P[n] = [_mv(e, dy=ddy, dz=ddz) for e in P[n]]
    def swing(n, ang, origin): P[n] = [_rot(e, 'x', ang, origin) for e in P[n]]
    if pose == 'breathe':
        move(up, 0.25); dy = 0.25
    elif pose == 'blink':
        P['eyes'] = [_c((5, 16.1, 4.88), (6.6, 16.6, 5.0), 'k'), _c((9.4, 16.1, 4.88), (11, 16.6, 5.0), 'k')]
    elif pose == 'wag':
        P['tail'] = [_rot(e, 'y', 22.5, (8, 7, 10.4)) for e in P['tail']]
    elif pose in ('walk1', 'walk2'):
        a = 22.5 if pose == 'walk1' else -22.5
        swing('legL', a, hip); swing('legR', -a, hip); swing('armL', -a, shL); swing('armR', a, shR)
        move(up, 0.2); dy = 0.2
    elif pose in ('run1', 'run2'):
        a = 45 if pose == 'run1' else -45
        swing('legL', a, hip); swing('legR', -a, hip); swing('armL', -a, shL); swing('armR', a, shR)
        move(up, 0.3, -0.7); dy, dz = 0.3, -0.7
        P['tail'] = [_rot(e, 'y', 22.5 if pose == 'run1' else -22.5, (8, 7, 10.4)) for e in P['tail']]
    elif pose == 'crouch':
        move(up, -1.6); dy = -1.6                                   # sitting back on his haunches, legs out in front
        P['legL'] = [_mv(_rot(e, 'x', 45, hip), dy=-1.6) for e in P['legL']]      # (1.15 had -45: in game that knelt)
        P['legR'] = [_mv(_rot(e, 'x', 45, hip), dy=-1.6) for e in P['legR']]
    elif pose == 'jump':
        swing('legL', -22.5, hip); swing('legR', -22.5, hip)       # legs tucked back, arms flung forward
        swing('armL', 45, shL); swing('armR', 45, shR)
        move(('torso', 'head', 'eyes', 'tail'), 0.4); dy = 0.4
    elif pose != 'stand':
        raise ValueError(pose)
    if parts: return P
    return [e for n in ('legL', 'legR', 'torso', 'armL', 'armR', 'head', 'eyes', 'tail') for e in P[n]], dy, dz


def donado_helm(m, dy, dz):
    if m == 'none': return []
    h = [_c((3.3, 17.4, 4.6), (12.7, 19.6, 11.4), 'h'), _c((3.2, 13.8, 7.0), (3.6, 17.4, 11.4), 'h'), _c((12.4, 13.8, 7.0), (12.8, 17.4, 11.4), 'h'),
         _c((3.6, 13.8, 11.0), (12.4, 17.4, 11.4), 'h')]
    if m in ('iron', 'gold', 'diamond', 'netherite', 'copper'): h.append(_c((7.5, 19.6, 6), (8.5, 21, 10.5), 'r'))
    if m == 'leather': h.append(_c((10, 19.6, 9), (10.6, 22.4, 9.6), 'w'))
    return [_mv(e, dy=dy, dz=dz) for e in h]


def alien_model(coat):
    """2.13: a Donadian is Donado's own build in Donadian colours - teal fur with dark patches, a lighter muzzle, dark ears,
    red eyes, white antennae, a coat (crew / lab / officer) - and no hover-disc (that became the Vorn hoverboard). Faces -z."""
    P = donado_parts()
    E = {}
    E['legs'] = P['legL'] + P['legR']
    E['coat'] = P['torso'] + P['tail']
    E['arms'] = P['armL'] + P['armR']
    E['head'] = P['head']
    E['eyes'] = [_c((5, 15.6, 4.88), (6.6, 17.3, 5.0), 'r'), _c((9.4, 15.6, 4.88), (11, 17.3, 5.0), 'r'),
                 _c((5.2, 16.6, 4.86), (5.7, 17.1, 4.9), 'w'), _c((9.6, 16.6, 4.86), (10.1, 17.1, 4.9), 'w')]
    E['mouth'] = []
    E['ant'] = [_c((6.1, 19, 7.6), (6.7, 23, 8.2), 'a'), _c((5.8, 23, 7.3), (7.0, 24.2, 8.5), 'a'),
                _c((9.3, 19, 7.6), (9.9, 23, 8.2), 'a'), _c((9.0, 23, 7.3), (10.2, 24.2, 8.5), 'a')]
    tex = {'f': 'bm:block/adon_skin', 'm': 'bm:block/adon_muzzle', 'e': 'bm:block/adon_dark', 'k': 'bm:block/adon_mouth',
           't': 'bm:block/adon_tongue', 's': f'bm:block/adon_{coat}', 'p': 'bm:block/adon_dark', 'r': 'bm:block/adon_eye',
           'w': 'bm:block/adon_antenna', 'a': 'bm:block/adon_antenna'}
    return tex, E


def alien_pose(coat, pose):
    tex, E = alien_model(coat)
    if pose == 'sniff':                                         # antennae wiggle
        E['ant'] = [_rot(e, 'z', 22.5 if i < 2 else -22.5, (6.4 if i < 2 else 9.6, 19, 7.9)) for i, e in enumerate(E['ant'])]
    elif pose == 'ears':                                        # blink
        E['eyes'] = [_c((5, 16.1, 4.88), (6.6, 16.6, 5.0), 'e'), _c((9.4, 16.1, 4.88), (11, 16.6, 5.0), 'e')]
    elif pose == 'tail':                                        # talking: a wag and a breath
        E['coat'] = [_rot(e, 'y', 22.5, (8, 7, 10.4)) if i == len(E['coat']) - 1 else e for i, e in enumerate(E['coat'])]
        for k in ('coat', 'arms', 'head', 'eyes', 'ant'): E[k] = [_mv(e, dy=0.25) for e in E[k]]
    elif pose is not None:
        raise ValueError(pose)
    return tex, [e for k in ('legs', 'coat', 'arms', 'head', 'eyes', 'mouth', 'ant') for e in E[k]]


def models():
    from gen_rp import HELM_TEX
    M = {}
    helms = ['none'] + list(HELM_TEX)
    for p in DON_POSE_NAMES:
        cubes, dy, dz = donado_pose(p)
        for m in helms:
            M[f'donp_{p}_{m}'] = (dict(DON_TEX, h=HELM_TEX.get(m, 'minecraft:block/iron_block'), r='minecraft:block/iron_block', w='minecraft:block/white_wool'),
                                  cubes + donado_helm(m, dy, dz))
    for suf, coat in ALIEN_VARIANTS.items():
        M[f'alien3d{suf}'] = alien_pose(coat, None)
        for p in ALIEN_POSES:
            M[f'adonp{suf}_{p}'] = alien_pose(coat, p)
    return M


DISPLAY_3D = ('donp_', 'adonp', 'alien3d')


def item_defs(mdl):
    """Item definitions that pick poses from custom_model_data strings."""
    from gen_rp import HELM_TEX
    helms = ['none'] + list(HELM_TEX)
    def helm_sel(p): return {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 1,
                             'cases': [{'when': m, 'model': mdl(f'donp_{p}_{m}')} for m in helms], 'fallback': mdl(f'donp_{p}_none')}
    out = {'donado': {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                'cases': [{'when': p, 'model': helm_sel(p)} for p in DON_POSE_NAMES], 'fallback': helm_sel('stand')}}}
    for suf in ALIEN_VARIANTS:
        out[f'alien3d{suf}'] = {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                          'cases': [{'when': p, 'model': mdl(f'adonp{suf}_{p}')} for p in ALIEN_POSES], 'fallback': mdl(f'alien3d{suf}')}}
    return out

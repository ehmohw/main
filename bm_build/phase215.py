"""2.94: THE 8-BIT SERPENT KING - what happens when the pixel trio comes to the Hollow Throne.

Bring 8-BIT EMMA, 8-BIT LEO and 8-BIT CECIL (phase213) onto Apophiss's seal in the Hollow King's throne room, with someone who
has conquered the Hollow King: the seal doesn't break - it GLITCHES, and out of the static rears APOPHISS as an old cartridge
would have drawn him (a PixelLab sprite, ref/pixellab/chars/apo_boss: always facing you, every move frame by frame).
THE FIGHT (a boss bar; 480 health):
  BITE         he lunges at the nearest of you within 5 (14, and it withers).
  BLACK FIRE   he breathes a stream of black pixel fire ahead of him (3 a tick it touches you, and it burns).
  TAIL SLAM    his tail crashes down - everyone within 6 takes 10 and is thrown up.
  ROAR         below half, once in a while: the screen shakes - darkness and slowness on everyone near.
THE WIN: every player near when he falls shatters him into pixels - and wins THE 8-BIT CROWN (his crown, in pixels: a real 3D
crown you wear, every pixel a little block; the first time - after that, a Glitched Cartridge)."""
import os
from items import item, T, TOTEM, ITEMS
from nbt import snbt, B, F, Int, D
import pxart
import phase210 as FXS

HERE = os.path.dirname(os.path.abspath(__file__))
GRN, GRN_LT = '#3ad06a', '#b8ffc8'
HP = 480
HEIGHT = 4.6
ANIMS = ('idle', 'move', 'bite', 'breath', 'slam', 'roar', 'hurt', 'death')
CROWN_PNG = os.path.join(HERE, 'ref', 'pixellab', 'crown', 'px_crown.png')
_S = []
HAVE = os.path.isdir(os.path.join(HERE, 'ref', 'pixellab', 'chars', 'apo_boss'))     # (his sprite: built once PixelLab has drawn him)


def spr():
    if not _S:
        have = pxart.anims_of('apo_boss')
        _S.append(pxart.Sprite('apo_boss', 'pxa_', HEIGHT, {a: (a if a in have else 'idle', None) for a in ANIMS}))
    return _S[0]


def _attr(a, v, slot='head'):
    return {'type': f'minecraft:{a}', 'amount': D(v), 'operation': 'add_value', 'slot': slot, 'id': f'bm:px_crown_{a}'}


item('px_crown', TOTEM, 'The 8-Bit Crown', GRN,
     ["Apophiss's crown as an old cartridge drew it -", 'every pixel a little block. It still hums.',
      ('Worn: +4 armour, +2 toughness, +4 health, +5% speed.', 'blue'), ('With an 8-bit follower out: Luck, and you glow a little.', 'blue'),
      ('Use: wear it.', 'gray'), ('Won from the 8-Bit Serpent King.', 'dark_gray')],
     model='bm:px_crown', stack=1, cat='relic', glint=True, tier=3,
     comps={'minecraft:equippable': {'slot': 'head', 'swappable': True, 'equip_sound': 'minecraft:item.armor.equip_netherite'},
            'minecraft:attribute_modifiers': [_attr('armor', 4), _attr('armor_toughness', 2), _attr('max_health', 4),
                                              {'type': 'minecraft:movement_speed', 'amount': D(0.05), 'operation': 'add_multiplied_base', 'slot': 'head', 'id': 'bm:px_crown_speed'}]})


def _rot90(e):
    """an element turned a quarter round the model's middle (x, z) -> (z, 16 - x): north faces west, south east, east north, west south"""
    f, t = e['from'], e['to']
    x0, x1 = f[2], t[2]
    z0, z1 = 16 - t[0], 16 - f[0]
    fc = e['faces']
    return {'from': [x0, f[1], z0], 'to': [x1, t[1], z1],
            'faces': {'west': fc['north'], 'east': fc['south'], 'north': fc['east'], 'south': fc['west'], 'up': fc['up'], 'down': fc['down']}}


def crown_model():
    """the crown: its picture as four little walls of voxels - front, back and both sides - round the head"""
    from PIL import Image
    im = Image.open(CROWN_PNG).convert('RGBA')
    bb = im.getbbox(); w, h = bb[2] - bb[0], bb[3] - bb[1]
    side, d, base = 11.0, 0.7, 14.0
    tex, els, sq = pxart.voxel(im, 'px_crown_t', height=side * h / w, depth=d)
    walls = []
    for e in els:                                                      # (the front wall: from the middle to the north edge of the ring)
        f, t = list(e['from']), list(e['to'])
        f[1] += base; t[1] += base
        f[2] += 8 - side / 2 - (8 - d / 2); t[2] += 8 - side / 2 - (8 - d / 2)
        walls.append({'from': f, 'to': t, 'faces': e['faces']})
    ring = list(walls)
    cur = walls
    for _k in range(3):                                                # (and the same wall turned three times: west, south, east)
        cur = [_rot90(e) for e in cur]
        ring += cur
    for e in ring:
        e['from'] = [round(v, 3) for v in e['from']]; e['to'] = [round(v, 3) for v in e['to']]
    disp = {'gui': {'rotation': [30, 225, 0], 'translation': [0, -3, 0], 'scale': [0.7, 0.7, 0.7]}, 'ground': {'rotation': [0, 0, 0], 'translation': [0, -4, 0], 'scale': [0.5, 0.5, 0.5]},
            'fixed': {'rotation': [0, 180, 0], 'translation': [0, -4, 0], 'scale': [0.8, 0.8, 0.8]},
            'thirdperson_righthand': {'rotation': [75, 45, 0], 'translation': [0, -1, 0], 'scale': [0.375, 0.375, 0.375]},
            'firstperson_righthand': {'rotation': [0, 45, 0], 'translation': [0, -2, 0], 'scale': [0.4, 0.4, 0.4]}}
    return tex, ring, disp, sq


def textures():
    T_ = dict(spr().textures()) if HAVE else {}
    T_['px_crown_t'] = crown_model()[3]
    return T_


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    if HAVE:
        S = spr()
        for name, (tex, els) in S.models().items():
            R.HATS[name] = (tex, els)
        R.DISPLAY_3D_EXTRA = R.DISPLAY_3D_EXTRA + (S.prefix,)

    def post(R2):
        if HAVE:
            spr().item_def(R2, 'pxa_boss')
        tex, els, disp, _sq = crown_model()
        R2.wj('assets/bm/models/item/px_crown.json', {'textures': tex, 'elements': els, 'display': disp})
        R2.wj('assets/bm/items/px_crown.json', {'model': {'type': 'minecraft:model', 'model': 'bm:item/px_crown'}})
    R.POST.append(post)


def generate(G):
    import phase131 as P131
    fn, title, tellraw, give = G.fn, G.title, G.tellraw, G.give
    P = G.PREFIX
    if not HAVE:
        print('phase215: no sprite for the 8-bit Serpent King yet (ref/pixellab/chars/apo_boss) - left out')
        return
    S = spr()
    n = {a: len(S.frames[a]) for a in ANIMS}
    tick, second = [], []
    objs = ['bm.pxas', 'bm.pxat', 'bm.pxac', 'bm.pxaf', 'bm.pxah']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + \
        ['bossbar add bm:pxapo {"text":"The 8-Bit Serpent King","color":"green","bold":true}', 'bossbar set bm:pxapo color green', 'bossbar set bm:pxapo style notched_10',
         f'bossbar set bm:pxapo max {HP}']
    G.OBJECTIVES += objs
    host = '@e[type=minecraft:husk,tag=bm.pxapo]'
    sprite = '@e[type=minecraft:item_display,tag=bm.pxa_spr]'
    FOE = 'gamemode=!spectator,gamemode=!creative'
    up = round(S.size / 2 - 6 * S.size / S.N, 3)

    # ---- the seal glitches: the 8-bit trio on it (with a conqueror)
    near = lambda tag: f'@e[type=minecraft:wolf,tag={tag},distance=..9]'
    L = G.FUNCS['p131/seal/sec']
    k = next(i for i, l in enumerate(L) if l == 'scoreboard players set #sn bm.rng 0')
    L.insert(k, f'execute if entity {near("bm.xmpet")} if entity {near("bm.xlpet")} if entity {near("bm.xcpet")} '
                f'if entity @a[distance=..8,scores={{bm.conqb=6..}},gamemode=!spectator] unless entity {host} run return run function bm:p215/try')
    # (2.94k: bm.conqb, a conqueror ever - as the seal's own Apophiss; and after he falls, five minutes before the seal glitches again)
    fn('p215/try', ['execute store result score #gt bm.dbcd run time query gametime',
                    'execute if score #gt bm.dbcd < #pxacd bm.dbcd run return run ' + G.title('@a[distance=..10]', 'actionbar', T('The seal crackles with static... not yet.', GRN)),
                    'function bm:p215/wake'])
    hnbt = {'Tags': ['bm.pxapo', 'bm.seen', 'bm.boss'], 'Silent': B(1), 'PersistenceRequired': B(1), 'Health': F(HP), 'DeathLootTable': 'minecraft:empty',
            'CustomName': T('The 8-Bit Serpent King', GRN, bold=True), 'CustomNameVisible': B(0),
            'attributes': [{'id': f'minecraft:{a}', 'base': D(v)} for a, v in (('max_health', HP), ('armor', 10), ('attack_damage', 12), ('movement_speed', 0.24),
                                                                                ('follow_range', 48), ('knockback_resistance', 1.0), ('scale', 1.8))],
            'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}]}
    snbt_spr = snbt({'Tags': ['bm.pxa_spr'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:pxa_boss'}},
                     'item_display': 'fixed', 'teleport_duration': Int(1), 'view_range': F(3.0),
                     'brightness': {'block': Int(15), 'sky': Int(15)}, 'shadow_radius': F(1.6), 'shadow_strength': F(0.6),
                     'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)], 'translation': [F(0), F(0), F(0)],
                                        'scale': [F(round(S.size, 4))] * 3}})
    fn('p215/wake', [f'summon minecraft:husk ~ ~ ~ {snbt(hnbt)}', f'execute positioned ~ ~{up} ~ run summon minecraft:item_display ~ ~ ~ {snbt_spr}',
                     f'scoreboard players set {host} bm.pxac 60', f'scoreboard players set {host} bm.pxas 6', f'scoreboard players set {host} bm.pxat {3 * n["roar"]}',
                     f'scoreboard players set {sprite} bm.pxah {HP}',
                     'particle minecraft:electric_spark ~ ~2 ~ 2 2 2 0.4 120', 'particle minecraft:dust{color:[0.2,1.0,0.4],scale:2.0} ~ ~2 ~ 2 2 2 0 80',
                     'playsound minecraft:block.note_block.bit hostile @a[distance=..48] ~ ~ ~ 2 0.5', 'playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..48] ~ ~ ~ 1 1.6',
                     title('@a[distance=..32]', 'title', T('8-BIT SERPENT KING', GRN, bold=True)),
                     title('@a[distance=..32]', 'subtitle', T('the seal glitches...', GRN_LT, italic=True)),
                     tellraw('@a[distance=..32]', P + [T('The seal doesn\'t break - it ', 'gray'), T('glitches', GRN, bold=True),
                                                       T('. Colours smear across the floor, and out of the static rears a serpent king drawn in sixteen colours.', 'gray')])])

    # ---- every tick: the sprite on him, his state, his blows
    tick.append(f'execute in bm:hollow_throne as {host} at @s run function bm:p215/tick')
    tick.append(f'execute as {sprite} at @s unless entity @e[type=minecraft:husk,tag=bm.pxapo,distance=..24] run function bm:p215/gone')
    fn('p215/tick', ['execute store result score #hp bm.rng run data get entity @s Health',
                     f'scoreboard players operation {sprite} bm.pxah = #hp bm.rng',
                     'scoreboard players remove @s[scores={bm.pxac=1..}] bm.pxac 1',
                     'execute if score @s bm.pxat matches 1.. run function bm:p215/act',
                     'execute unless score @s bm.pxat matches 1.. run scoreboard players set @s bm.pxas 0',
                     f'execute unless score @s bm.pxac matches 1.. if entity @a[distance=..14,{FOE}] run function bm:p215/pick',
                     'scoreboard players add @s bm.pxaf 1', 'scoreboard players operation #me bm.rng = @s bm.pxas',
                     'scoreboard players operation #fi bm.rng = @s bm.pxaf',
                     # (idle or moving, by his motion; hurt for a moment when struck)
                     'execute if score #me bm.rng matches 0 store result score #vx bm.rng run data get entity @s Motion[0] 1000',
                     'execute if score #me bm.rng matches 0 store result score #vz bm.rng run data get entity @s Motion[2] 1000',
                     'execute if score #me bm.rng matches 0 run scoreboard players operation #vx bm.rng *= #vx bm.rng',
                     'execute if score #me bm.rng matches 0 run scoreboard players operation #vz bm.rng *= #vz bm.rng',
                     'execute if score #me bm.rng matches 0 run scoreboard players operation #vx bm.rng += #vz bm.rng',
                     'execute if score #me bm.rng matches 0 if score #vx bm.rng matches 300.. run scoreboard players set #me bm.rng 1',
                     'execute if score #me bm.rng matches 0..1 unless data entity @s {HurtTime:0s} run scoreboard players set #me bm.rng 7',
                     f'execute as {sprite} positioned ~ ~{up} ~ run function bm:p215/frame'])
    # the frame: (the sprite; #me the state, #fi the host's tick)
    order = ['idle', 'move', 'bite', 'breath', 'slam', 'roar', 'roar', 'hurt']        # (state 6: his coming - the roar)
    fr = ['tp @s ~ ~ ~ ~ 0', 'scoreboard players operation #f2 bm.rng = #fi bm.rng', 'scoreboard players operation #f2 bm.rng %= #2 bm.rng',
          'execute unless score #f2 bm.rng matches 0 run return 0', 'scoreboard players operation #fi bm.rng /= #2 bm.rng']
    for st, a in enumerate(order):
        fr += [f'execute if score #me bm.rng matches {st} run scoreboard players set #n bm.rng {n[a]}',
               f'execute if score #me bm.rng matches {st} run scoreboard players operation #fi bm.rng %= #n bm.rng']
        fr += [f'execute if score #me bm.rng matches {st} if score #fi bm.rng matches {i} run return run '
               f'data modify entity @s item.components."minecraft:custom_model_data" set value {{strings:["{a}_{i}"]}}' for i in range(n[a])]
    fn('p215/frame', fr)
    # (a blow: its state for its frames, two ticks each; its moment at the middle)
    dur = {2: 2 * n['bite'], 3: 2 * n['breath'], 4: 2 * n['slam'], 5: 2 * n['roar']}
    fn('p215/pick', ['execute store result score #r bm.rng run random value 1..10',
                     'execute store result score #hp bm.rng run data get entity @s Health',
                     f'execute if score #hp bm.rng matches ..{HP // 2} if score #r bm.rng matches 10 run return run function bm:p215/go {{s:5}}',
                     'execute if score #r bm.rng matches 1..4 if entity @a[distance=..5,gamemode=!spectator,gamemode=!creative] run return run function bm:p215/go {s:2}',
                     'execute if score #r bm.rng matches 1..6 run return run function bm:p215/go {s:3}',
                     'function bm:p215/go {s:4}'])
    fn('p215/go', ['$scoreboard players set @s bm.pxas $(s)', 'scoreboard players set @s bm.pxaf 0', 'scoreboard players set @s bm.pxac 50'] +
       [f'execute if score @s bm.pxas matches {s} run scoreboard players set @s bm.pxat {d}' for s, d in dur.items()] +
       ['execute if score @s bm.pxas matches 3 run playsound minecraft:entity.blaze.shoot hostile @a[distance=..32] ~ ~ ~ 1 0.6',
        'execute if score @s bm.pxas matches 5 run playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..32] ~ ~ ~ 1 1.8'])
    fn('p215/act', ['scoreboard players remove @s bm.pxat 1',
                    f'execute if score @s bm.pxas matches 2 if score @s bm.pxat matches {dur[2] // 2} run function bm:p215/bite',
                    f'execute if score @s bm.pxas matches 3 if score @s bm.pxat matches 2..{dur[3] - 4} facing entity @p[{FOE}] feet rotated ~ 0 run function bm:p215/breath',
                    f'execute if score @s bm.pxas matches 4 if score @s bm.pxat matches {dur[4] // 2} run function bm:p215/slam',
                    f'execute if score @s bm.pxas matches 5 if score @s bm.pxat matches {dur[5] // 2} run function bm:p215/roar'])
    fn('p215/bite', [f'execute as @p[distance=..5,{FOE}] at @s run function bm:p215/bitten', 'playsound minecraft:entity.evoker_fangs.attack hostile @a[distance=..24] ~ ~ ~ 1 0.6'])
    fn('p215/bitten', ['damage @s 14 minecraft:mob_attack by @e[type=minecraft:husk,tag=bm.pxapo,limit=1,sort=nearest]', 'effect give @s minecraft:wither 3 0',
                       FXS.fx('px_boom', 1.2, 1.0)])
    fn('p215/breath', ['scoreboard players operation #b bm.rng = @s bm.pxat', 'scoreboard players operation #b bm.rng %= #2 bm.rng',
                       'execute unless score #b bm.rng matches 0 run return 0'] +
       [f'execute positioned ^ ^1.6 ^{d} run particle minecraft:dust{{color:[0.12,0.12,0.12],scale:2.4}} ~ ~ ~ 0.4 0.4 0.4 0 6' for d in (2, 4, 6, 8, 10)] +
       ['execute positioned ^ ^1.6 ^6 run ' + FXS.fx('px_fireball', 1.2, 0.0),
        f'execute positioned ^ ^ ^5 as @a[distance=..4.5,{FOE}] at @s run function bm:p215/burnt'])
    fn('p215/burnt', ['damage @s 3 minecraft:mob_attack by @e[type=minecraft:husk,tag=bm.pxapo,limit=1,sort=nearest]', 'data merge entity @s {Fire:60s}'])
    fn('p215/slam', [FXS.fx('px_boom', 2.6, 0.4), 'particle minecraft:explosion ~ ~0.5 ~ 2 0.2 2 0 6', 'playsound minecraft:entity.generic.explode hostile @a[distance=..32] ~ ~ ~ 1 0.8',
                     f'execute as @a[distance=..6,{FOE}] at @s run function bm:p215/slammed'])
    fn('p215/slammed', ['damage @s 10 minecraft:mob_attack by @e[type=minecraft:husk,tag=bm.pxapo,limit=1,sort=nearest]', 'effect give @s minecraft:levitation 1 3 true'])
    fn('p215/roar', [f'effect give @a[distance=..24,{FOE}] minecraft:darkness 4 0', f'effect give @a[distance=..24,{FOE}] minecraft:slowness 4 1',
                     'particle minecraft:sonic_boom ~ ~3 ~ 0 0 0 0 1', title('@a[distance=..24]', 'actionbar', T('The screen shakes!', GRN, bold=True))])
    # ---- the boss bar: who's near, how he's doing
    second.append(f'execute in bm:hollow_throne as {host} at @s run function bm:p215/bar')
    second.append(f'execute unless entity {host} run bossbar set bm:pxapo players')
    fn('p215/bar', ['execute store result bossbar bm:pxapo value run data get entity @s Health', 'bossbar set bm:pxapo players @a[distance=..48]',
                    # (nobody left near for a while: he fades back into the seal)
                    'execute if entity @a[distance=..48,gamemode=!spectator] run return run scoreboard players set @s bm.pxah 0',
                    'scoreboard players add @s bm.pxah 1', 'execute if score @s bm.pxah matches 60.. run function bm:p215/fade'])
    fn('p215/fade', ['tag @e[type=minecraft:item_display,tag=bm.pxa_spr,distance=..24] add bm.pxa_faded', 'tp @s ~ -300 ~', 'kill @s'])
    # ---- he falls: shattered into pixels - the crown (or a cartridge) for everyone near
    # (2.94k: faded is not beaten - but a last blow from over 60 health is: he went from the sprite's last health to nothing in a tick)
    fn('p215/gone', ['execute if entity @s[tag=bm.pxa_faded] run return run kill @s',
                     'tag @s add bm.pxa_dying', 'tag @s remove bm.pxa_spr', 'scoreboard players set @s bm.pxaf 0'])
    tick.append('execute as @e[type=minecraft:item_display,tag=bm.pxa_dying] at @s run function bm:p215/dying')
    fn('p215/dying', ['scoreboard players add @s bm.pxaf 1', 'scoreboard players operation #fi bm.rng = @s bm.pxaf', 'scoreboard players operation #fi bm.rng /= #3 bm.rng'] +
       [f'execute if score #fi bm.rng matches {i} run data modify entity @s item.components."minecraft:custom_model_data" set value {{strings:["death_{i}"]}}' for i in range(n['death'])] +
       ['particle minecraft:dust{color:[0.2,1.0,0.4],scale:1.6} ~ ~1 ~ 1.5 1.5 1.5 0 6',
        f'execute if score @s bm.pxaf matches {3 * n["death"] + 6}.. run function bm:p215/won'])
    fn('p215/won', ['execute store result score #pxacd bm.dbcd run time query gametime', 'scoreboard players add #pxacd bm.dbcd 6000','particle minecraft:electric_spark ~ ~1.5 ~ 2 2 2 0.4 120', 'playsound minecraft:block.note_block.bit hostile @a[distance=..48] ~ ~ ~ 2 2',
                    'playsound minecraft:ui.toast.challenge_complete player @a[distance=..48] ~ ~ ~ 1 1.2',
                    'execute as @a[distance=..48,gamemode=!spectator] run function bm:p215/reward', 'kill @s'])
    fn('p215/reward', ['execute if entity @s[tag=bm.pxcrown] run return run function bm:p215/again', 'tag @s add bm.pxcrown', give('px_crown'),
                       'advancement grant @s only bm:story/px_crown',
                       tellraw('@s', P + [T('The 8-Bit Serpent King shatters into a thousand pixels - and one of them is a crown. ', 'gray'),
                                          T('The 8-Bit Crown', GRN, bold=True), T(' is yours.', 'gray')])])
    fn('p215/again', [give('glitch_cart'), tellraw('@s', P + [T('He shatters again - and leaves a ', 'gray'), T('Glitched Cartridge', '#7aff9a', bold=True), T(' behind.', 'gray')])])
    G.wjson('bm/advancement/story/px_crown.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
                                                   'display': {'icon': {'id': TOTEM, 'components': {'minecraft:item_model': 'bm:px_crown'}},
                                                               'title': T('Game Over, Serpent', 'yellow'), 'description': T('Beat the 8-Bit Serpent King with the pixel trio', 'gray'),
                                                               'frame': 'challenge', 'show_toast': True, 'announce_to_chat': True, 'hidden': True}})
    # ---- the crown: with an 8-bit follower out, Luck and a little glow
    worn = '@a[nbt={equipment:{head:{components:{"minecraft:custom_data":{bm:"px_crown"}}}}}]'
    second.append(f'execute as {worn} at @s run function bm:p215/crown')
    fn('p215/crown', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #px bm.rng 0'] +
       [f'execute as @e[type=minecraft:wolf,tag={t}] if score @s bm.pid = #me bm.pid run scoreboard players set #px bm.rng 1' for t in ('bm.xmpet', 'bm.xlpet', 'bm.xcpet')] +
       ['execute if score #px bm.rng matches 1 run effect give @s minecraft:luck 3 0 true',
        'execute if score #px bm.rng matches 1 run particle minecraft:dust{color:[0.3,1.0,0.5],scale:0.6} ~ ~2.2 ~ 0.25 0.05 0.25 0 2'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #2 bm.rng 2', 'scoreboard players set #3 bm.rng 3']
    G.FUNCS['tick'] += tick
    G.FUNCS['loop/second'][-1:-1] = second
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.pxa_spr]', 'kill @e[type=minecraft:item_display,tag=bm.pxa_dying]',
                                       'tp @e[type=minecraft:husk,tag=bm.pxapo] ~ -300 ~', 'bossbar remove bm:pxapo']
    fn('admin/px_apo', ['execute positioned ^ ^ ^6 run function bm:p215/wake'])
    fn('admin/px_crown', [give('px_crown')])
    G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/px_apo', 'yellow'), T('  the 8-Bit Serpent King, here;', 'gray'),
                                                T(' /function bm:admin/px_crown', 'yellow'), T(' his crown', 'gray')]))

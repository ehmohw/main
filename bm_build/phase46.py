"""Phase 2.24b: Cecil joins the fight, a portrait for the chef, the Emma doll.

- CECIL'S SUMMONING GEM (Cecil): use it and Cecil appears beside you and follows you. He fights from range - a
  poisoned bolt at the nearest monster every 2 seconds (5 damage + Poison II) - and heals you when you're hurt
  (every 5 seconds below 7 hearts). 60 health, 20 armour. Use the gem again to call him back to you; sneak + use to
  send him home. If he falls, he fades away and the gem needs 10 minutes to call him again.
- CHEF FROMAGE'S PORTRAIT (the chef): a 2x2 painting of the man himself.
- THE EMMA DOLL (Cecil, 3 Trophies - Black Market only): a chibi doll you can set down; right-click to make her twirl. While she
  stands, players within 10 blocks are cured of harmful effects.
- Every bow in the market is Cecil's now (the Fairy Bow moves over from Vinny)."""
from items import item, T, TOTEM, PRICES
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D

PET_CD = 600                     # seconds before a fallen Cecil can be called again
COMPANIONS = 'tag=!bm.wilfrey,tag=!bm.wil_body,tag=!bm.frogpet,tag=!bm.merc,tag=!bm.cecilpet'

item('cecil_gem', TOTEM, "Cecil's Summoning Gem", '#b48cff',
     ['A violet gem with two yellow eyes in it.', 'They blink.', ('Use: Cecil joins you in battle - poisoned', 'blue'),
      ('bolts at monsters, healing when you\'re hurt.', 'blue'), ('Use again: call him back to you.', 'blue'), ('Sneak + use: send him home.', 'blue'),
      ('If he falls: 10 minutes before he can return.', 'gray')],
     model='bm:cecil_gem', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
HOLD['cecil_gem'] = 'bm:p46/pet/use'
item('chef_painting', 'minecraft:painting', "Chef Fromage's Portrait", '#c8a050', ['A 2x2 painting, in a gilt frame.', ('He insists it does not flatter him.', 'gray')],
     stack=16, cat='relic', comps={'minecraft:painting/variant': 'bm:chef_fromage'})
item('emma_doll', TOTEM, 'Emma Doll', '#3d8fd0', ['A chibi doll of Emma, mid-twirl.', ('Right-click a block: set her down.', 'blue'),
                                                  ('While she stands, anyone within 10 blocks', 'blue'), ('is cured of harmful effects.', 'blue'),
                                                  ('Right-click her: she twirls.', 'blue'), ('Sneak + punch: pick her up.', 'gray')],
     model='bm:emma3d', stack=16, cat='fun', comps=hold('none'))
HOLD['emma_doll'] = 'bm:p46/emma/use'


def extend_offers(O, offer):
    O['wizard'].insert(0, offer(PRICES['fairy_bow'], ('fairy_bow', 1)))
    O['wizard'].append(offer(('trophy', 4), ('cecil_gem', 1)))
    O['chef'].append(offer(('token', 6), ('chef_painting', 1)))
    O['wizard'].append(offer(('trophy', 3), ('emma_doll', 1)))


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    import phase45 as P45
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    ident = [F(0), F(0), F(0), F(1)]
    tick, fast, second = [], [], []
    objs = ['bm.cpcd dummy', 'bm.cpg dummy', 'bm.cpt dummy', 'bm.cpa dummy', 'bm.cph dummy']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o}' for o in objs]
    G.OBJECTIVES += [o.split()[0] for o in objs]

    # ------------------------------------------------------------------ the chef's portrait (painting variant; texture in rp)
    wjson('bm/painting_variant/chef_fromage.json', {'asset_id': 'bm:chef_fromage', 'width': Int(2), 'height': Int(2),
                                                     'title': T("Chef Fromage's Portrait", 'yellow'), 'author': T('The Gnawed Flagon', 'gray')})

    # ------------------------------------------------------------------ CECIL, the companion: an invisible tamed wolf carrying his rig
    pet = {'Tags': ['bm.cecilpet', 'bm.cpnew', 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1), 'Health': F(60),
           'CustomName': T('Cecil', '#b48cff', bold=True), 'CustomNameVisible': B(0),
           'attributes': [{'id': 'minecraft:max_health', 'base': D(60)}, {'id': 'minecraft:armor', 'base': D(20)}, {'id': 'minecraft:attack_damage', 'base': D(2)},
                          {'id': 'minecraft:movement_speed', 'base': D(0.32)}, {'id': 'minecraft:follow_range', 'base': D(32)}, {'id': 'minecraft:step_height', 'base': D(1.0)}],
           'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}]}
    def part(model, tag, ty, bright):
        return snbt({'Tags': ['bm.cpet', tag, 'bm.cpnew'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': model}},
                     'item_display': 'fixed', 'teleport_duration': Int(2), 'brightness': {'block': Int(bright), 'sky': Int(bright)},
                     'interpolation_duration': Int(15), 'start_interpolation': Int(0),
                     'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(ty), F(0)], 'scale': [F(0)] * 3}})
    rig = [f'summon minecraft:item_display ~ ~ ~ {part("bm:cec_body", "bm.cp_body", 0.5, 13)}',
           f'summon minecraft:item_display ~ ~ ~ {part("bm:cec_head", "bm.cp_head", 0.0, 13)}',
           f'summon minecraft:item_display ~ ~ ~ {part("bm:cec_eyes", "bm.cp_eyes", 0.0, 15)}',
           f'summon minecraft:item_display ~ ~ ~ {part("bm:cec_arm", "bm.cp_arm", 0.0, 13)}']
    sel_pet = 'execute as @e[type=minecraft:wolf,tag=bm.cecilpet] if score @s bm.pid = #me bm.pid'
    fn('p46/pet/use', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                       f'{sel_pet} run tag @s add bm.cpsel',
                       'execute if entity @e[type=minecraft:wolf,tag=bm.cpsel] if predicate bm:p20/sneaking run function bm:p46/pet/dismiss',
                       'execute if entity @e[type=minecraft:wolf,tag=bm.cpsel] unless predicate bm:p20/sneaking run function bm:p46/pet/recall',
                       'execute unless entity @e[type=minecraft:wolf,tag=bm.cpsel] unless predicate bm:p20/sneaking run function bm:p46/pet/try_summon',
                       'execute unless entity @e[type=minecraft:wolf,tag=bm.cpsel] if predicate bm:p20/sneaking run ' + say('Cecil isn\'t with you. (Use the gem to call him.)'),
                       'tag @e[tag=bm.cpsel] remove bm.cpsel'])
    fn('p46/pet/recall', ['tp @e[type=minecraft:wolf,tag=bm.cpsel,limit=1] @s', 'particle minecraft:portal ~ ~1 ~ 0.4 0.8 0.4 0.4 30',
                          'data modify entity @e[type=minecraft:wolf,tag=bm.cpsel,limit=1] Sitting set value 0b', say('Cecil blinks back to your side.', '#b48cff')])
    fn('p46/pet/try_summon', ['execute if score @s bm.cpcd matches 1.. store result score #m bm.rng run scoreboard players get @s bm.cpcd',
                              'execute if score @s bm.cpcd matches 1.. run scoreboard players operation #m bm.rng /= #60 bm.rng',
                              'execute if score @s bm.cpcd matches 1.. run scoreboard players add #m bm.rng 1',
                              'execute if score @s bm.cpcd matches 1.. run return run ' + title('@s', 'actionbar', [T('Cecil is still pulling himself back together: about ', 'gray'),
                                                                                                                   {'score': {'name': '#m', 'objective': 'bm.rng'}, 'color': 'white'}, T(' min.', 'gray')]),
                              'execute unless function bm:p37/allowed run return run ' + say('Cecil won\'t come here.'),
                              'function bm:p46/pet/summon'])
    fn('p46/pet/summon', [f'summon minecraft:wolf ^ ^ ^1.2 {snbt(pet)}', 'data modify entity @e[type=minecraft:wolf,tag=bm.cpnew,limit=1,sort=nearest] Owner set from entity @s UUID',
                          # (a fresh wolf resets its max health on spawn, so set it afterwards)
                          'attribute @e[type=minecraft:wolf,tag=bm.cpnew,limit=1,sort=nearest] minecraft:max_health base set 60', 'data modify entity @e[type=minecraft:wolf,tag=bm.cpnew,limit=1,sort=nearest] Health set value 60f',
                          'execute positioned ^ ^ ^1.2 rotated ~180 0 run function bm:p46/pet/rig'] +
       ['scoreboard players operation @e[tag=bm.cpnew,distance=..4] bm.pid = @s bm.pid', 'tag @e[tag=bm.cpnew,distance=..4] remove bm.cpnew',
        'execute positioned ^ ^ ^1.2 run particle minecraft:portal ~ ~1 ~ 0.4 1 0.4 0.6 60', 'execute positioned ^ ^ ^1.2 run particle minecraft:witch ~ ~1 ~ 0.4 0.8 0.4 0.1 20',
        'playsound minecraft:entity.evoker.prepare_summon neutral @a[distance=..20] ~ ~ ~ 1 1.2', 'playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..20] ~ ~ ~ 1 0.8',
        say('"Hehehe... who are we hexing today?"', '#b48cff')])
    fn('p46/pet/rig', rig + ['tp @e[type=minecraft:item_display,tag=bm.cpnew,distance=..1] ~ ~ ~ ~ 0',
                             # grow in from nothing
                             'execute as @e[type=minecraft:item_display,tag=bm.cpnew,distance=..1] run data merge entity @s {start_interpolation:0,interpolation_duration:15,transformation:{scale:[1f,1f,1f]}}'])
    # every tick: the rig stands where the wolf is, turned its way (the head and eyes look at its target or its owner)
    tick.append('execute as @e[type=minecraft:wolf,tag=bm.cecilpet] at @s run function bm:p46/pet/tick')
    fn('p46/pet/tick', ['scoreboard players operation #me bm.pid = @s bm.pid',
                        'execute as @e[type=minecraft:item_display,tag=bm.cpet,tag=!bm.cpfade] if score @s bm.pid = #me bm.pid run tag @s add bm.cpsel',
                        'execute rotated as @s rotated ~ 0 run function bm:p46/pet/place', 'tag @e[tag=bm.cpsel] remove bm.cpsel'])
    fn('p46/pet/place', ['tp @e[type=minecraft:item_display,tag=bm.cpsel,tag=bm.cp_body] ~ ~ ~ ~ 0',
                         'execute positioned ^-0.31 ^1.28 ^0.06 run tp @e[type=minecraft:item_display,tag=bm.cpsel,tag=bm.cp_arm] ~ ~ ~ ~ 0',
                         'execute positioned ^ ^1.38 ^0.12 run tp @e[type=minecraft:item_display,tag=bm.cpsel,tag=bm.cp_head] ~ ~ ~ ~ 0',
                         'execute positioned ^ ^1.38 ^0.12 run tp @e[type=minecraft:item_display,tag=bm.cpsel,tag=bm.cp_eyes] ~ ~ ~ ~ 0'])
    # a rig whose wolf is gone (4 ticks running - never a chunk-edge blip): he fell. Fade, and the gem cools down.
    tick += ['execute as @e[type=minecraft:item_display,tag=bm.cp_body,tag=!bm.cpfade] at @s run function bm:p46/pet/check',
             'scoreboard players remove @e[type=minecraft:item_display,tag=bm.cpfade] bm.cpt 1',
             'kill @e[type=minecraft:item_display,tag=bm.cpfade,scores={bm.cpt=..0}]']
    fn('p46/pet/check', ['scoreboard players operation #me bm.pid = @s bm.pid',
                         f'{sel_pet.replace("@e[type=minecraft:wolf,tag=bm.cecilpet]", "@e[type=minecraft:wolf,tag=bm.cecilpet,distance=..16]")} run return run scoreboard players set @s bm.cpg 0',
                         'scoreboard players add @s bm.cpg 1', 'execute if score @s bm.cpg matches 4.. run function bm:p46/pet/fell'])
    fn('p46/pet/fell', ['function bm:p46/pet/fade', 'execute as @a if score @s bm.pid = #me bm.pid run function bm:p46/pet/cooldown'])
    fn('p46/pet/cooldown', [f'scoreboard players set @s bm.cpcd {PET_CD}',
                            tellraw('@s', PREFIX + [T('Cecil has fallen. ', '#b48cff', bold=True), T(f'He fades with a sulky hiss; the gem needs {PET_CD // 60} minutes before it can call him back.', 'gray')])])
    # (as anything at his spot, #me = his owner's id) every part of him shrinks away over a second, in a puff of magic
    fn('p46/pet/fade', ['execute as @e[type=minecraft:item_display,tag=bm.cpet,tag=!bm.cpfade] if score @s bm.pid = #me bm.pid run function bm:p46/pet/fade1',
                        'particle minecraft:witch ~ ~1 ~ 0.4 0.8 0.4 0.05 40', 'particle minecraft:portal ~ ~1 ~ 0.4 0.8 0.4 0.8 60', 'particle minecraft:soul ~ ~1.2 ~ 0.3 0.6 0.3 0.02 12',
                        'playsound minecraft:entity.illusioner.mirror_move neutral @a[distance=..20] ~ ~ ~ 1 0.8'])
    fn('p46/pet/fade1', ['tag @s add bm.cpfade', 'scoreboard players set @s bm.cpt 20',
                         'data merge entity @s {start_interpolation:0,interpolation_duration:20,transformation:{scale:[0f,0f,0f]}}'])
    fn('p46/pet/dismiss', ['execute as @e[type=minecraft:wolf,tag=bm.cpsel] at @s run function bm:p46/pet/fade',
                           'execute as @e[type=minecraft:wolf,tag=bm.cpsel] run data remove entity @s Owner',
                           'execute as @e[type=minecraft:wolf,tag=bm.cpsel] run tp @s ~ -500 ~', 'kill @e[type=minecraft:wolf,tag=bm.cpsel]',
                           say('Cecil bows - "Call me when there\'s hexing to do" - and fades away.', '#b48cff')])
    second.append('scoreboard players remove @a[scores={bm.cpcd=1..}] bm.cpcd 1')
    # every second: a poisoned bolt every 2 seconds at the nearest monster (14 blocks); a heal for his owner every 5 if they're hurt
    second.append('execute as @e[type=minecraft:wolf,tag=bm.cecilpet] at @s run function bm:p46/pet/act')
    foe = 'type=#bm:hostile,tag=!bm.npc,distance=..14'
    fn('p46/pet/act', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players add @s bm.cpa 1', 'scoreboard players add @s bm.cph 1',
                       'execute if score @s bm.cpa matches 1 run function bm:p46/pet/arm_down',
                       f'execute if score @s bm.cpa matches 2.. if entity @e[{foe}] run function bm:p46/pet/attack',
                       'execute if score @s bm.cph matches 5.. on owner if entity @s[distance=..12] run function bm:p46/pet/heal_check'])
    for nm, q in (('down', '[0.0523f,0f,0f,0.9986f]'), ('cast', '[0.3256f,0f,0f,0.9455f]')):
        fn(f'p46/pet/arm_{nm}', [f'execute as @e[type=minecraft:item_display,tag=bm.cp_arm,tag=!bm.cpfade] if score @s bm.pid = #me bm.pid run data merge entity @s '
                                 f'{{start_interpolation:0,interpolation_duration:5,transformation:{{left_rotation:{q}}}}}'])
    fn('p46/pet/attack', ['scoreboard players set @s bm.cpa 0', 'function bm:p46/pet/arm_cast', 'tag @s add bm.cpme',
                          f'execute as @e[{foe},sort=nearest,limit=1] at @s run function bm:p46/pet/bolt', 'tag @s remove bm.cpme',
                          'playsound minecraft:entity.evoker.cast_spell neutral @a[distance=..20] ~ ~ ~ 0.8 1.4'])
    fn('p46/pet/bolt', ['damage @s 5 minecraft:magic by @e[type=minecraft:wolf,tag=bm.cpme,limit=1]', 'effect give @s minecraft:poison 6 1',
                        'particle minecraft:dust{color:[0.45,0.9,0.2],scale:1.4} ~ ~1 ~ 0.3 0.5 0.3 0 16', 'particle minecraft:item_slime ~ ~1 ~ 0.3 0.4 0.3 0 8',
                        'execute facing entity @e[type=minecraft:wolf,tag=bm.cpme,limit=1] eyes run function bm:p46/pet/beam'])
    fn('p46/pet/beam', [f'particle minecraft:dust{{color:[0.6,0.3,0.9],scale:1}} ^ ^1.2 ^{d} 0 0 0 0 1' for d in (0.6, 1.2, 1.8, 2.4, 3, 3.6, 4.2, 4.8, 5.4, 6, 6.6, 7.2, 7.8, 8.4, 9, 9.6, 10.2, 10.8, 11.4, 12, 12.6, 13.2)])
    fn('p46/pet/heal_check', ['execute store result score #h bm.rng run data get entity @s Health', 'execute unless score #h bm.rng matches ..13 run return 0',
                              'effect give @s minecraft:instant_health 1 0 true', 'particle minecraft:heart ~ ~2 ~ 0.4 0.3 0.4 0 6',
                              'particle minecraft:dust{color:[1.0,0.45,0.8],scale:1.2} ~ ~1 ~ 0.4 0.6 0.4 0 14', 'playsound minecraft:block.amethyst_block.chime neutral @a[distance=..16] ~ ~ ~ 1 1.6',
                              'execute as @e[type=minecraft:wolf,tag=bm.cecilpet] if score @s bm.pid = #me bm.pid run scoreboard players set @s bm.cph 0'])

    # ------------------------------------------------------------------ the Emma doll (placed like the lava lamp)
    hit = snbt({'Tags': ['bm.emmahit', 'bm.p45hit', 'bm.p45new'], 'width': F(0.6), 'height': F(0.95), 'response': B(1)})
    d = snbt({'Tags': ['bm.emmad', 'bm.p45new'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:emma3d'}},
              'item_display': 'fixed', 'teleport_duration': Int(6),
              'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.5), F(0)], 'scale': [F(1)] * 3}})
    P45_placer = G.FUNCS['p45/lava_lamp/place']           # reuse the placer pattern: look at the top of a block within 5
    fn('p46/emma/use', [l.replace('p45/lava_lamp/ray', 'p46/emma/ray').replace('"lava_lamp"', '"emma_doll"') for l in P45_placer])
    fn('p46/emma/ray', [l.replace('p45/lava_lamp/', 'p46/emma/') for l in G.FUNCS['p45/lava_lamp/ray']])
    fn('p46/emma/hit', [l.replace('bm:p45/lava/spawn', 'bm:p46/emma/spawn') for l in G.FUNCS['p45/lava_lamp/hit']])
    fn('p46/emma/spawn', [f'summon minecraft:item_display ~ ~ ~ {d}', f'summon minecraft:interaction ~ ~ ~ {hit}', 'tp @e[tag=bm.p45new,distance=..0.5] ~ ~ ~ ~ 0',
                          'tag @e[tag=bm.p45new,distance=..0.5] remove bm.p45new', 'playsound minecraft:block.wool.place block @a[distance=..12] ~ ~ ~ 1 1.2'])
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.emmahit] if data entity @s interaction at @s run function bm:p46/emma/click')
    fn('p46/emma/click', ['execute as @e[type=minecraft:item_display,tag=bm.emmad,distance=..0.4] at @s run tp @s ~ ~ ~ ~120 0',
                          'playsound minecraft:block.note_block.chime block @a[distance=..12] ~ ~ ~ 0.8 1.4', 'playsound minecraft:block.note_block.bell block @a[distance=..12] ~ ~ ~ 0.5 1.8',
                          'particle minecraft:cherry_leaves ~ ~0.8 ~ 0.3 0.3 0.3 0 6', 'data remove entity @s interaction'])
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.emmahit] if data entity @s attack at @s run function bm:p46/emma/punch')
    fn('p46/emma/punch', ['tag @s add bm.p45me', 'execute on attacker if predicate bm:p20/sneaking run function bm:p46/emma/pick', 'tag @s remove bm.p45me', 'data remove entity @s attack'])
    fn('p46/emma/pick', [give('emma_doll'), 'execute as @e[type=minecraft:interaction,tag=bm.p45me] at @s run function bm:p46/emma/gone', 'playsound minecraft:entity.item.pickup player @s ~ ~ ~ 1 1'])
    fn('p46/emma/gone', ['kill @e[type=minecraft:item_display,tag=bm.emmad,distance=..0.6]', 'particle minecraft:poof ~ ~0.3 ~ 0.2 0.2 0.2 0.02 6', 'kill @s'])
    # her charm: every second, players within 10 blocks of a placed doll shake off harmful effects
    BAD = ['poison', 'wither', 'slowness', 'weakness', 'mining_fatigue', 'nausea', 'blindness', 'hunger', 'darkness', 'unluck', 'infested', 'oozing', 'weaving', 'wind_charged']
    second.append('execute as @e[type=minecraft:item_display,tag=bm.emmad] at @s as @a[distance=..10,gamemode=!spectator] at @s run function bm:p46/emma/cure')
    fn('p46/emma/cure', ['scoreboard players set #had bm.rng 0'] +
       sum(([f'execute store success score #c bm.rng run effect clear @s minecraft:{e}', 'execute if score #c bm.rng matches 1 run scoreboard players set #had bm.rng 1'] for e in BAD), []) +
       ['execute if score #had bm.rng matches 1 run particle minecraft:cherry_leaves ~ ~1.2 ~ 0.4 0.5 0.4 0 8',
        'execute if score #had bm.rng matches 1 run playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 0.6 1.6'])
    # (2.24: Black Market exclusive - Cecil sells her; no chest finds)

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


# ===================================================================== resource pack
def textures():
    from PIL import Image
    from gen_rp import hexc
    import random
    rnd = random.Random(46)
    def flat(c, var=4):
        im = Image.new('RGBA', (16, 16)); b = hexc(c)
        for y in range(16):
            for x in range(16):
                dd = rnd.randint(-var, var); im.putpixel((x, y), tuple(max(0, min(255, v + dd)) for v in b[:3]) + (255,))
        return im
    T_ = {k: flat(c) for k, c in (('em_blue', '#3d8fd0'), ('em_skirt', '#3e6d9e'), ('em_scarf', '#6fd6e0'), ('em_skin', '#f6cfa8'), ('em_hair', '#a8592a'),
                                  ('em_shoe', '#3c4f8a'), ('em_white', '#eeeeee'), ('em_belt', '#6a4a2a'), ('em_pink', '#e050c0'))}
    face = flat('#f6cfa8', 3)
    # 2.24: a simple pixel face - small dark teal eyes with a white glint, a tiny smile
    P = {'e': '#0f4a52', 'w': '#ffffff', 'm': '#7a2a2a'}
    rows = ['................', '................', '................', '................', '................', '................', '................',
            '...wee....wee...', '...eee....eee...', '...eee....eee...', '................',
            '................', '......m..m......', '.......mm.......', '................', '................']
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != '.': face.putpixel((x, y), hexc(P[ch]))
    T_['em_face'] = face
    return T_


def rp(R):
    import sys
    from PIL import Image
    R.TEXTURE_MODS.append(sys.modules[__name__])
    cube = R.cube
    def c(fr, to, t, rot=None):
        e = cube(fr, to, t)
        if rot: e['rotation'] = rot
        return e
    et = {k: f'bm:block/em_{k}' for k in ('blue', 'skirt', 'scarf', 'skin', 'hair', 'shoe', 'white', 'belt', 'pink', 'face')}
    up = {'origin': [5, 9.6, 8], 'axis': 'z', 'angle': 22.5}
    face = cube((4.2, 10.4, 4.5), (11.8, 17.2, 4.6), 'face', faces=('north',))
    face['faces']['north']['uv'] = [1, 1, 15, 15]              # the whole face texture on the front (the auto UV would crop it)
    R.HATS['emma3d'] = (et, [
        c((5, 0, 6.5), (7.5, 1.2, 9.5), 'shoe'), c((8.5, 0, 6.5), (11, 1.2, 9.5), 'shoe'),
        c((5.6, 1.2, 7.3), (7, 3.4, 8.7), 'white'), c((9, 1.2, 7.3), (10.4, 3.4, 8.7), 'white'),
        c((3, 3.2, 4.5), (13, 5, 11.5), 'skirt'), c((4, 5, 5.5), (12, 6.5, 10.5), 'skirt'),
        c((5, 6.5, 6.3), (11, 7.2, 9.7), 'belt'), c((7.2, 6.4, 6.1), (8.8, 7.3, 6.3), 'white'),
        c((5.3, 7.2, 6.5), (10.7, 10, 9.5), 'blue'), c((5, 9.5, 6.2), (11, 10.4, 9.8), 'scarf'), c((7.4, 8.2, 6.35), (8.6, 9.2, 6.5), 'pink'),
        c((3.6, 9, 7.3), (5.3, 14.5, 8.7), 'blue', up), c((3.6, 14.5, 7.3), (5.3, 15.6, 8.7), 'skin', up),
        c((10.7, 6.5, 7.3), (12.3, 9.8, 8.7), 'blue'), c((10.8, 5.6, 7.4), (12.2, 6.5, 8.6), 'skin'),
        c((4, 10.3, 4.6), (12, 17.6, 11.4), 'skin'), face,
        c((3.7, 16, 4.2), (12.3, 18.6, 11.8), 'hair'), c((3.7, 11, 9.5), (12.3, 18, 11.8), 'hair'), c((4, 15.5, 4.2), (12, 16.6, 5), 'hair'),
        c((3.4, 10.5, 4.8), (4.3, 15.5, 8), 'hair'), c((11.7, 10.5, 4.8), (12.6, 15.5, 8), 'hair'),
        c((1, 13, 8), (4, 17, 11), 'hair'), c((0, 11.5, 8.5), (2, 14.5, 10.5), 'hair'), c((2.8, 16.5, 7.8), (4.6, 18.2, 10.2), 'pink')])
    R.DISPLAY_3D_EXTRA = R.DISPLAY_3D_EXTRA + ('emma3d',)
    R.ICONS['cecil_gem'] = R.grid(['................', '.......PP.......', '......PLLP......', '.....PLPPPP.....', '....PPPPPPPP....', '...PPYYPPYYPP...',
                                   '...PPPYPPYPPP...', '...PPPPPPPPPP...', '....PKKKKKKP....', '....PPKPKPPP....', '.....PPPPPP.....', '......PPPP......',
                                   '.......PP.......', '................', '................', '................'],
                                  dict(P='#6a2aa8', L='#c8a0ff', Y='#f4dc6a', K='#1a0a2a'))
    # the chef's portrait: the reference art in a gilt frame (128 x 128 = 2 x 2 blocks)
    def post(R2):
        N, FR = 128, 8
        src = Image.open('/home/claude/bm_build/vendor/chef_ref.png').convert('RGB')
        w, h = src.size; s = min(w, h)
        src = src.crop(((w - s) // 2, 0, (w - s) // 2 + s, s)).resize((N - 2 * FR, N - 2 * FR), Image.LANCZOS)
        im = Image.new('RGBA', (N, N), R2.hexc('#c8a050'))
        im.paste(src, (FR, FR))
        for i in range(N):
            for (x, y) in ((i, 0), (i, 1), (i, N - 1), (i, N - 2), (0, i), (1, i), (N - 1, i), (N - 2, i)): im.putpixel((x, y), R2.hexc('#e8c870'))
            for (x, y) in ((i, 4), (i, N - 5), (4, i), (N - 5, i)): im.putpixel((x, y), R2.hexc('#a8803a'))
            for (x, y) in ((i, FR - 1), (i, N - FR), (FR - 1, i), (N - FR, i)):
                if FR - 1 <= i <= N - FR: im.putpixel((x, y), R2.hexc('#3a2410'))
        im.save(R2.p('assets', 'bm', 'textures', 'painting', 'chef_fromage.png'))
    R.POST.append(post)

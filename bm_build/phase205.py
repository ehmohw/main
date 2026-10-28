"""2.93: CHAMPIONS OF THE TIDE - a follower honoured to the height of all three of Queen Ava's honours (Vitality, Bulwark and
Might V) is her Champion.

  THE ADVANCEMENT       "Champion of the Tide", the first time one of your followers is made a Champion.
  CHAMPION'S MEDAL      a gold medal on their chest (a sapphire sea-star on a gold disc, on a ribbon)
  CHAMPION'S REGALIA    a new outfit worn over their own model, where one suits them - a cape, a knight's or a captain's
                        pauldrons, a dwarf's belt, crackling lightning down a beast's back (KillerWatt wears no clothes), a
                        ridge of bone spines - built for each follower on its own bones (champion_art.py), so it moves with
                        every animation. (2.93b) On the head: Emma's tiara, Bender's crown, Bones's pirate hat, Mr. Capshun's
                        doodled crown; those with a crown or hat already get no second one - an ornament on their own instead
                        (a crystal in their colour out of the crown, or a crystal or rose bud pinned to the hat)
  CHAMPION'S AURA       their own particles, always round them
  A CHAMPION'S MIGHT    tougher still: +20 health (doubled by Vitality V), +4 toughness, half knockback - enough to take
                        several blows from a Blood Moon's monsters and a few from the Dread's
  A NEW ABILITY         each Champion has a signature blow of their own (ABIL, below), every 15 s in a fight - scaled by
                        their Might like every follower attack
  THE CHAMPION'S RIBBON given with the first Champion: use it with Champions beside you to turn their medal, regalia and
                        aura on or off (each on its own, for good)"""
from items import item, T, ITEMS
from useitem import hold, HOLD
from nbt import snbt
import champion_art as CA

GOLD, AVA_C = '#ffd66a', '#6ad8e8'
MENU = 4200                                 # (its block: 4200-4299)
CD = 15                                     # an ability's rest (s)
PARTS = [('medal', 'Medal', 'md'), ('regalia', 'Regalia', 'rg'), ('aura', 'Aura', 'au')]
holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'

# a Champion's signature blow: (name, what it does, nova (damage, radius) or None, strike damage on the nearest monster or 0,
#   mob effect, owner effects, particle, sound)
ABIL = {
    'emma': ('Tidal Bloom', 'a ring of sea-light: 10 to monsters round her; you, Regeneration II and Absorption', (10, 5), 0, 'slowness 3 1',
             ['regeneration 8 1', 'absorption 20 1'], 'minecraft:bubble_pop', 'minecraft:entity.dolphin.splash'),
    'celi': ('Moonfall Spear', 'a spear of moonlight from above: 22 to one monster, frozen', None, 22, 'slowness 4 3', [], 'minecraft:snowflake', 'minecraft:block.glass.break'),
    'zib': ('Orbital Ping', 'a beam from orbit: 20 to one monster, glowing', None, 20, 'glowing 6 0', [], 'minecraft:electric_spark', 'minecraft:block.beacon.power_select'),
    'cecil': ('Arcane Cataclysm', 'an arcane blast: 14 to every monster round him', (14, 6), 0, 'weakness 5 1', [], 'minecraft:enchant', 'minecraft:entity.evoker.cast_spell'),
    'kw': ('Overcharge', 'a lightning burst: 14 to monsters round him; you, Speed II', (14, 5), 0, 'slowness 2 2', ['speed 8 1'], 'minecraft:electric_spark', 'minecraft:entity.lightning_bolt.thunder'),
    'leo': ("Knight's Oath", 'his oath: you and your followers Resistance II; 10 to monsters round him', (10, 4), 0, 'weakness 4 0', ['resistance 8 1'], 'minecraft:end_rod', 'minecraft:item.trident.return'),
    'demo': ('Reaping Storm', 'a scythe-storm: 16 to monsters round him', (16, 5), 0, 'slowness 3 1', [], 'minecraft:sweep_attack', 'minecraft:item.trident.thunder'),
    'apo': ('Black Flame Coil', 'a coil of black fire: 18 to monsters round him, withering', (18, 6), 0, 'wither 5 1', [], 'minecraft:soul_fire_flame', 'minecraft:entity.wither.shoot'),
    'tul': ('Frozen Broadside', 'a frozen broadside: 24 to one monster, slowed', None, 24, 'slowness 5 2', [], 'minecraft:snowflake', 'minecraft:entity.generic.explode'),
    'frog': ('Tongue Lash', 'a long tongue: 16 to one monster, pulled in', None, 16, 'slowness 2 4', ['regeneration 4 0'], 'minecraft:item_slime', 'minecraft:entity.frog.tongue'),
    'don': ('Death Ray', 'a full-power ray: 26 to one monster', None, 26, 'glowing 4 0', [], 'minecraft:end_rod', 'minecraft:block.beacon.deactivate'),
    'wil': ('Wail', 'a deathly wail: 12 to monsters round him, weakened', (12, 6), 0, 'weakness 6 1', [], 'minecraft:soul', 'minecraft:entity.wither.ambient'),
    'fishy': ('Bubble Burst', 'a burst of bubbles: 8 to monsters round him; you, Water Breathing and Dolphin\'s Grace', (8, 5), 0, 'levitation 1 0',
              ['water_breathing 30 0', 'dolphins_grace 10 0'], 'minecraft:bubble_pop', 'minecraft:block.bubble_column.upwards_inside'),
    'dennis': ('Gold Rush Quake', 'a golden quake: 14 to monsters round him; you, Haste II', (14, 5), 0, 'slowness 3 1', ['haste 15 1'], 'minecraft:wax_on', 'minecraft:block.anvil.land'),
    'pistachio': ('Haunting', 'a haunting: 12 to monsters round him, blinded', (12, 6), 0, 'blindness 4 0', [], 'minecraft:soul', 'minecraft:entity.vex.charge'),
    'omega': ('Soul Harvest', 'a harvest of souls: 18 to monsters round him; you, Regeneration II', (18, 6), 0, 'wither 4 0', ['regeneration 6 1'], 'minecraft:sculk_soul', 'minecraft:entity.warden.sonic_charge'),
    'ashur': ('Inferno', 'an inferno: 16 to monsters round him, set alight', (16, 5), 0, 'glowing 2 0', [], 'minecraft:flame', 'minecraft:entity.blaze.shoot'),
    'chef': ('Hot Plate', 'a sizzling plate: 10 to monsters round him; you, Saturation and Regeneration', (10, 4), 0, 'slowness 2 1',
             ['saturation 1 1', 'regeneration 6 0'], 'minecraft:flame', 'minecraft:block.campfire.crackle'),
    'neighbor': ('Battle Hymn', 'a battle hymn: you and your followers Strength II; 8 to monsters round him', (8, 6), 0, 'weakness 3 0', ['strength 10 1'], 'minecraft:note', 'minecraft:block.note_block.bell'),
    'ava': ('Tidal Grace', 'the tide\'s grace: you healed, Absorption II; 10 to monsters round her', (10, 5), 0, 'slowness 3 1',
            ['instant_health 1 1', 'absorption 20 1'], 'minecraft:end_rod', 'minecraft:block.conduit.activate'),
    'pearlq': ("Regent's Decree", 'a decree: 12 to monsters round her, weakened; you, Resistance', (12, 6), 0, 'weakness 6 1', ['resistance 8 0'], 'minecraft:glow', 'minecraft:block.bell.use'),
    'bloo': ('Feral Frenzy', 'a frenzy: 22 to one monster; you, Strength', None, 22, 'slowness 2 1', ['strength 6 0'], 'minecraft:crimson_spore', 'minecraft:entity.ravager.roar'),
    'stalker': ('Phantom Rend', 'a rend from nowhere: 24 to one monster, through its armour', None, 24, 'darkness 3 0', [], 'minecraft:squid_ink', 'minecraft:entity.warden.attack_impact'),
    'lantern': ('Pumpkin Barrage', 'a barrage of fire: 16 to monsters round him', (16, 6), 0, 'glowing 2 0', [], 'minecraft:small_flame', 'minecraft:entity.blaze.shoot'),
    'bender': ('Pounce', 'a pounce: 22 to one monster, pinned', None, 22, 'slowness 3 4', [], 'minecraft:crit', 'minecraft:entity.wolf.growl'),
    'bones': ('Riptide Frenzy', 'a frenzy of teeth: 22 to one monster; you, Dolphin\'s Grace', None, 22, 'slowness 2 1', ['dolphins_grace 10 0'], 'minecraft:bubble', 'minecraft:entity.guardian.attack'),
    'gem': ('Masterpiece', 'a masterpiece: 16 to monsters round it; you and your followers, Haste II and Regeneration', (16, 6), 0, 'glowing 3 0', ['regeneration 8 0', 'haste 15 1'], 'minecraft:end_rod', 'minecraft:block.amethyst_block.resonate'),
    'batty': ('Sonic Screech', 'a screech: 16 to monsters round him, dizzied', (16, 6), 0, 'nausea 5 0', [], 'minecraft:sonic_boom', 'minecraft:entity.bat.death'),
    'eggbert': ('Ooze Flood', 'a flood of ooze: 16 to monsters round him, stuck fast', (16, 5), 0, 'slowness 4 3', [], 'minecraft:squid_ink', 'minecraft:block.honey_block.slide'),
    'count': ('Checkmate', 'checkmate: 22 to one monster; you, Resistance', None, 22, 'weakness 5 1', ['resistance 10 0'], 'minecraft:enchanted_hit', 'minecraft:block.note_block.bell'),
    'dragon': ('Crayon Inferno', 'a roar of crayon fire: 16 to monsters round him, alight', (16, 6), 0, 'slowness 3 1', [], 'minecraft:flame', 'minecraft:entity.blaze.shoot'),
    'eraser': ('Clean Slate', 'it rubs one monster out: 22, weakened', None, 22, 'weakness 5 1', ['regeneration 6 0'], 'minecraft:cherry_leaves', 'minecraft:item.brush.brushing.sand'),
    'cursor': ('Select All', 'every monster round it selected: 16, glowing; you, Haste', (16, 7), 0, 'glowing 6 0', ['haste 10 1'], 'minecraft:electric_spark', 'minecraft:ui.button.click'),
    'inkblot': ('Ink Tsunami', 'a wave of ink: 16 to monsters round it, blinded', (16, 6), 0, 'blindness 3 0', [], 'minecraft:squid_ink', 'minecraft:entity.slime.squish'),
    'speech': ('KA-BOOM!', 'the loudest word there is: 16 to monsters round it, stunned', (16, 6), 0, 'slowness 3 3', [], 'minecraft:explosion', 'minecraft:entity.generic.explode'),
    'lightbringer': ('Judgment', 'a pillar of light: 22 to one monster; you and your followers, Regeneration II', None, 22, 'glowing 5 0', ['regeneration 8 1'], 'minecraft:end_rod', 'minecraft:entity.lightning_bolt.impact'),
    'dryad': ('Overgrowth', 'the ground bursts into roots: 16 to monsters round her, held fast', (16, 7), 0, 'slowness 4 4', [], 'minecraft:spore_blossom_air', 'minecraft:block.rooted_dirt.break'),
    'sovereign': ('Unmaking', 'its eye opens: a beam - 24 to one monster, withering; you, Strength', None, 24, 'wither 4 1', ['strength 8 0'], 'minecraft:sculk_soul', 'minecraft:entity.warden.sonic_boom'),
    'henry': ('Black Cat Crossing', 'he crosses its path: 22 to one monster, and it\'s cursed (slowed, weakened); you, Luck II', None, 22, 'weakness 4 1', ['luck 20 1'], 'minecraft:squid_ink', 'minecraft:entity.cat.hiss'),
    'nia': ('Bell of the Brave', 'her bell rings out: 16 to monsters round her; you and your followers, Regeneration II', (16, 6), 0, 'glowing 3 0', ['regeneration 8 1'], 'minecraft:end_rod', 'minecraft:block.bell.use'),
    'rufus': ('Bounty Collected', 'a bounty collected: 22 to one monster, pinned; you, Luck II', None, 22, 'slowness 3 4', ['luck 20 1'], 'minecraft:crit', 'minecraft:item.crossbow.shoot'),
    'kettle': ('Tag Team', 'tag, you\'re it: you and your followers Speed II and Strength; 8 to monsters round him', (8, 5), 0, 'slowness 3 1',
               ['speed 10 1', 'strength 10 0'], 'minecraft:happy_villager', 'minecraft:entity.experience_orb.pickup'),
    'capshun': ('Doodle Barrier', 'a doodled barrier: you and your followers Absorption III and Resistance; 6 round him', (6, 4), 0, 'slowness 2 1',
                ['absorption 20 2', 'resistance 8 0'], 'minecraft:end_rod', 'minecraft:item.book.page_turn'),
    'pxcecil': ('Game Over', 'the screen goes black: 16 to every monster round him, withered; you, Regeneration', (16, 7), 0, 'wither 3 0', ['regeneration 6 1'], 'minecraft:witch', 'minecraft:entity.evoker.cast_spell'),
    'pxleo': ('Spin Attack', 'a whirl of pixel steel: 14 to every monster round him; you, Resistance and Strength', (14, 6), 0, 'slowness 2 1', ['resistance 8 1', 'strength 10 0'], 'minecraft:sweep_attack', 'minecraft:entity.player.attack.sweep'),
    'pxemma': ('1-UP', 'a pixel heart bursts: 12 to every monster round her; you, Absorption and Regeneration', (12, 6), 0, 'glowing 3 0', ['absorption 20 1', 'regeneration 6 1'], 'minecraft:heart', 'minecraft:entity.player.levelup'),
    'sky': ('Clear Skies', 'the clouds part: 14 to every monster round them, lit up; you, Regeneration and Haste', (14, 6), 0, 'glowing 4 0', ['regeneration 6 1', 'haste 15 1'], 'minecraft:end_rod', 'minecraft:block.beacon.power_select'),
}
FIRE = {'ashur', 'lantern'}                 # (their blows set monsters alight)
BYPASS = {'stalker', 'apo'}                 # (their blows go through armour)

item('champion_ribbon', 'minecraft:paper', "Champion's Ribbon", GOLD,
     ['Queen Ava\'s ribbon, for those who keep Champions.', ('Use it with your Champions beside you:', 'yellow'),
      ('turn each one\'s medal, regalia and aura', 'yellow'), ('on or off.', 'yellow')],
     model='bm:champion_ribbon', stack=1, cat='misc', comps=hold())
HOLD['champion_ribbon'] = 'bm:p205/ribbon'


def generate(G):
    import phase28 as P28
    import phase173 as P173
    from phase125 import WHO
    fn, title, tellraw, give, P = G.fn, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    second, tick = G.FUNCS['loop/second'], G.FUNCS['tick']
    FOL = [w for w in P173.AR if w in WHO]
    IDX = {w: i + 1 for i, w in enumerate(FOL)}
    assert set(FOL) == set(ABIL), set(FOL) ^ set(ABIL)
    host = lambda w, x='': f'@e[type=minecraft:{P173.AR[w][1]},tag={P173.AR[w][2]}{"," + x if x else ""}]'
    objs = ['bm.chcd', 'bm.chs0', 'bm.chs1', 'bm.chs2']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs

    G.wjson('bm/advancement/story/champion_tide.json', {
        'parent': 'bm:story/root', 'criteria': {'made': {'trigger': 'minecraft:impossible'}},
        'display': {'icon': {'id': 'minecraft:paper', 'components': {'minecraft:item_model': 'bm:champion_ribbon'}},
                    'title': T('Champion of the Tide', GOLD), 'description': T("Honour a follower to the height of all three of Queen Ava's honours", 'gray'),
                    'frame': 'challenge'}})

    # ---------------------------------------------------------------- made a Champion (after a rank is bought; Apophiss's restraint)
    for w in FOL:
        nm, col = WHO[w][0], WHO[w][2]
        a = ABIL[w]
        fn(f'p205/check/{w}', [f'scoreboard players operation #hc bm.rng = @s bm.hn_{w}', 'scoreboard players operation #hc bm.rng %= #1000 bm.rng',
                               'execute unless score #hc bm.rng matches 555 run return 0',
                               f'execute if entity @s[tag=bm.chmp_{w}] run return 0',
                               f'tag @s add bm.chmp_{w}',
                               title('@a[distance=..32]', 'title', T('Champion of the Tide', GOLD, bold=True)),
                               title('@a[distance=..32]', 'subtitle', [T(nm, col, bold=True), T(' - at the height of every honour', AVA_C)]),
                               tellraw('@s', P + [T(nm, col, bold=True), T(' is Queen Ava\'s CHAMPION: ', GOLD, bold=True),
                                                  T('the medal, the regalia and the aura are theirs, and a new blow - ', 'gray'),
                                                  T(a[0], GOLD, bold=True), T(f': {a[1]}.', 'gray')]),
                               'advancement grant @s only bm:story/champion_tide',
                               f'execute unless entity @s[tag=bm.chrib] run {give("champion_ribbon")}', 'tag @s add bm.chrib',
                               'particle minecraft:totem_of_undying ~ ~1.2 ~ 0.6 0.8 0.6 0.4 60',
                               'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1.1'])
    G.FUNCS['p201/eth/apo'].append('function bm:p205/check/apo')
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #1000 bm.rng 1000', 'scoreboard players set #4 bm.rng 4']

    # ---------------------------------------------------------------- the Champion's toughness (p201/apply: on every change)
    G.FUNCS['p201/apply'][-2:-2] = [
        'attribute @s minecraft:max_health modifier remove bm:champion', 'attribute @s minecraft:armor_toughness modifier remove bm:champion',
        'attribute @s minecraft:knockback_resistance modifier remove bm:champion', 'tag @s remove bm.champ',
        'scoreboard players operation #hc bm.rng = #hv bm.rng', 'scoreboard players operation #hc bm.rng %= #1000 bm.rng',
        'execute if score #hc bm.rng matches 555 run tag @s add bm.champ',
        'execute if entity @s[tag=bm.champ] run attribute @s minecraft:max_health modifier add bm:champion 20 add_value',
        'execute if entity @s[tag=bm.champ] run attribute @s minecraft:armor_toughness modifier add bm:champion 4 add_value',
        'execute if entity @s[tag=bm.champ] run attribute @s minecraft:knockback_resistance modifier add bm:champion 0.5 add_value']

    # ---------------------------------------------------------------- each second: the pieces, the aura, the blow
    second.append('tag @e[type=minecraft:item_display,tag=bm.chp] add bm.chold')
    for w in FOL:
        second.append(f'execute as {host(w, "tag=bm.champ")} at @s run function bm:p205/sec/{w}')
        second.append(f'execute as {host(w, "tag=!bm.champ,tag=bm.chau")} run tag @s remove bm.chau')
    second.append('kill @e[type=minecraft:item_display,tag=bm.chold]')
    for w in FOL:
        on = [f'execute unless entity @s[tag=bm.no{c}_{w}] run scoreboard players set #{c} bm.rng 1' for _p, _n, c in PARTS]
        fn(f'p205/own/{w}', on)
        lines = ['execute unless score @s bm.pid matches 1.. run return 0', 'scoreboard players operation #me bm.pid = @s bm.pid'] + \
                [f'scoreboard players set #{c} bm.rng 0' for _p, _n, c in PARTS] + \
                [f'execute as @a if score @s bm.pid = #me bm.pid run function bm:p205/own/{w}',
                 'tag @s remove bm.chau', 'execute if score #au bm.rng matches 1 run tag @s add bm.chau']
        parts = [('medal', 'md')] + ([('body', 'rg')] if w != 'wil' and CA.STYLE[w][1] else []) + \
                ([('head', 'rg')] if w != 'wil' and (CA.STYLE[w][0] or w in CA.ORNAMENT) else [])   # (2.93b: a crown or hat of their own kept, or an ornament on it)
        for part, c in parts:
            lines += [f'scoreboard players set #hp bm.rng 0',
                      f'execute if score #{c} bm.rng matches 1 as @e[type=minecraft:item_display,tag=bm.chp_{w},tag=bm.chq_{part},distance=..12] '
                      f'if score @s bm.pid = #me bm.pid run function bm:p205/keep',
                      f'execute if score #{c} bm.rng matches 1 if score #hp bm.rng matches 0 run function bm:p205/put/{w}_{part}']
        lines += [f'execute if score @s bm.chcd matches 1.. run scoreboard players remove @s bm.chcd 1',
                  f'execute unless score @s bm.chcd matches 1.. if entity @e[type=#bm:hostile,tag=!bm.npc,tag=!bm.wil_body,distance=..{(ABIL[w][2] or (0, 8))[1] + 2}] run function bm:p205/ab/{w}']
        fn(f'p205/sec/{w}', lines)
        for part, _c in parts:
            if w == 'wil':
                tf = '[0f,1.62f,0f]'
                anchor = 'bm.wil_body'
                xf = f'transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:{tf},scale:[1.2f,1.2f,1.2f]}},'
            else:
                anchor = (CA.ANCHORS[w][0] if part == 'head' or (part == 'medal' and w in CA.MEDAL_FACE) else CA.ANCHORS[w][2]).replace('bm.', '')
                xf = ''
            fn(f'p205/put/{w}_{part}', [
                f'summon minecraft:item_display ~ ~ ~ {{Tags:["bm.chp","bm.chp_{w}","bm.chq_{part}","bm.chnew"],item_display:"fixed",teleport_duration:2,{xf}'
                f'item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"bm:champ_{w}_{part}","minecraft:custom_data":{{a:"bm.{anchor}"}}}}}}}}',
                'scoreboard players operation @e[type=minecraft:item_display,tag=bm.chnew,distance=..1] bm.pid = #me bm.pid',
                'tag @e[type=minecraft:item_display,tag=bm.chnew,distance=..1] remove bm.chnew'])
    fn('p205/keep', ['tag @s remove bm.chold', 'scoreboard players set #hp bm.rng 1'])

    # ---------------------------------------------------------------- each tick: the pieces wear their bones' place and pose
    tick += ['execute as @e[type=minecraft:item_display,tag=bm.chp,tag=!bm.chp_wil] at @s run function bm:p205/follow with entity @s item.components."minecraft:custom_data"',
             'execute as @e[type=minecraft:item_display,tag=bm.chp_wil] at @s at @e[type=minecraft:wither_skeleton,tag=bm.wil_body,distance=..8,sort=nearest,limit=1] rotated ~ 0 run tp @s ~ ~ ~ ~ 0',
             'scoreboard players add #cht bm.rng 1', 'execute if score #cht bm.rng matches 4.. run function bm:p205/auras']
    fn('p205/follow', ['$execute at @s run tp @s @e[type=minecraft:item_display,tag=$(a),distance=..8,sort=nearest,limit=1]',
                       '$execute at @s store success score #ch bm.rng run data modify entity @s transformation set from entity @e[type=minecraft:item_display,tag=$(a),distance=..1,sort=nearest,limit=1] transformation',
                       '$execute if score #ch bm.rng matches 1 run data modify entity @s interpolation_duration set from entity @e[type=minecraft:item_display,tag=$(a),distance=..1,sort=nearest,limit=1] interpolation_duration',
                       'execute if score #ch bm.rng matches 1 run data modify entity @s start_interpolation set value 0'])
    au = ['scoreboard players set #cht bm.rng 0']
    for w in FOL:
        au.append(f'execute as {host(w, "tag=bm.chau")} at @s run function bm:p205/aura/{w}')
        fn(f'p205/aura/{w}', [f'particle {p}' for p in CA.STYLE.get(w, CA.STYLE['pistachio'])[3]] if w != 'wil' else
           ['particle minecraft:soul ~ ~1.2 ~ 0.5 0.7 0.5 0.01 1', 'particle minecraft:smoke ~ ~1.2 ~ 0.5 0.7 0.5 0 2'])
    fn('p205/auras', au)

    # ---------------------------------------------------------------- the Champions' blows
    for w in FOL:
        nm, col = WHO[w][0], WHO[w][2]
        name, _desc, nova, strike, meff, own, part, snd = ABIL[w]
        dt = 'minecraft:magic' if w in BYPASS else 'minecraft:mob_attack'
        me = f'@e[type=minecraft:{P173.AR[w][1]},tag=bm.chme,limit=1]'
        L = [f'scoreboard players set @s bm.chcd {CD}', 'tag @s add bm.chme', f'playsound {snd} neutral @a[distance=..24] ~ ~ ~ 1 1']
        if nova:
            d, r = nova
            L += [f'particle {part} ~ ~0.6 ~ {r / 2:.1f} 0.3 {r / 2:.1f} 0.05 60', f'particle minecraft:dust{{color:[1.0,0.84,0.4],scale:1.4}} ~ ~0.4 ~ {r / 2:.1f} 0.1 {r / 2:.1f} 0 40',
                  f'execute as @e[type=#bm:hostile,tag=!bm.npc,tag=!bm.wil_body,distance=..{r}] at @s run function bm:p205/hit/{w}']
        if strike:
            L += [f'execute as @e[type=#bm:hostile,tag=!bm.npc,tag=!bm.wil_body,distance=..10,sort=nearest,limit=1] at @s run function bm:p205/hit/{w}']
        if own:
            L += ['scoreboard players operation #me bm.pid = @s bm.pid',
                  f'execute as @a[distance=..24] if score @s bm.pid = #me bm.pid at @s run function bm:p205/own_fx/{w}']
        L += ['tag @s remove bm.chme']
        fn(f'p205/ab/{w}', L)
        hit = [f'particle {part} ~ ~1 ~ 0.4 0.6 0.4 0.05 30', f'damage @s {nova[0] if nova else strike} {dt} by {me}']
        if strike: hit[1:1] = ['particle minecraft:flash{color:[1.0,0.9,0.5,1.0]} ~ ~1 ~ 0 0 0 0 1', f'particle {part} ~ ~6 ~ 0.1 3 0.1 0 40']
        if meff: hit.append(f'effect give @s minecraft:{meff.split()[0]} {meff.split()[1]} {meff.split()[2]}')
        if w in FIRE: hit.append('data merge entity @s {Fire:100s}')
        if w == 'frog': hit.append(f'execute facing entity {me} feet run tp @s ^ ^ ^1.5')
        fn(f'p205/hit/{w}', hit)
        if own:
            fx = [f'effect give @s minecraft:{e.split()[0]} {e.split()[1]} {e.split()[2]}' for e in own]
            if w in ('leo', 'neighbor', 'capshun', 'kettle', 'nia', 'gem'):     # (the whole party: your followers too)
                fx += [f'execute as {host(o, "distance=..16")} if score @s bm.pid = #me bm.pid run effect give @s minecraft:{e.split()[0]} {e.split()[1]} {e.split()[2]}'
                       for o in FOL for e in own[:1]]
            fn(f'p205/own_fx/{w}', fx + [title('@s', 'actionbar', [T(nm, col, bold=True), T(' - ', 'gray'), T(name, GOLD, bold=True)])])

    # ---------------------------------------------------------------- the Champion's Ribbon: medal, regalia, aura on/off
    def lbl(k, p):
        return f'r_{k}{p}'
    fn('p205/ribbon', ['scoreboard players set #ns bm.rng 0', 'scoreboard players operation #me bm.pid = @s bm.pid',
                       'scoreboard players set @s bm.chs0 0', 'scoreboard players set @s bm.chs1 0', 'scoreboard players set @s bm.chs2 0',
                       'data modify storage bm:ui ch set value {}'] +
       [f'data modify storage bm:ui ch.{lbl(k, c)} set value {snbt(T("—", "dark_gray"))}' for k in range(3) for _p, _n, c in PARTS] +
       [f'data modify storage bm:ui ch.r_n{k} set value {snbt(T("(no Champion)", "dark_gray"))}' for k in range(3)] +
       [f'execute if score #ns bm.rng matches ..2 as {host(w, "tag=bm.champ,distance=..24")} if score @s bm.pid = #me bm.pid run function bm:p205/slot/{w}' for w in FOL] +
       ['execute if score #ns bm.rng matches 0 run return run ' + say('Bring your Champions beside you - the ribbon is theirs to dress.', GOLD),
        f'scoreboard players set @s bm.menu {MENU}', 'function bm:p205/rib_dlg with storage bm:ui ch',
        'playsound minecraft:item.armor.equip_gold player @s ~ ~ ~ 0.8 1.2'])
    for w in FOL:
        nm, col = WHO[w][0], WHO[w][2]
        sl = ['scoreboard players add #ns bm.rng 1']
        for k in range(3):
            sl.append(f'execute if score #ns bm.rng matches {k + 1} as @a if score @s bm.pid = #me bm.pid run function bm:p205/fill/{w}_{k}')
        fn(f'p205/slot/{w}', sl)
        for k in range(3):
            f = [f'scoreboard players set @s bm.chs{k} {IDX[w]}', f'data modify storage bm:ui ch.r_n{k} set value {snbt(T(nm, col, bold=True))}']
            for _p, pn, c in PARTS:
                f += [f'data modify storage bm:ui ch.{lbl(k, c)} set value {snbt([T(pn + ": ", "gray"), T("ON", "green", bold=True)])}',
                      f'execute if entity @s[tag=bm.no{c}_{w}] run data modify storage bm:ui ch.{lbl(k, c)} set value {snbt([T(pn + ": ", "gray"), T("OFF", "red", bold=True)])}']
            fn(f'p205/fill/{w}_{k}', f)
    B_ = lambda lbl_, code: P28.btn(lbl_, code, width=110)
    dlg = P28.multi([T("THE CHAMPION'S RIBBON", GOLD, bold=True), T('  ·  your Champions beside you', 'gray')],
                    [P28.body([T('Each Champion\'s medal, regalia and aura, on or off - for good.', 'gray')], 340)] +
                    [P28.body([T('', 'gray'), '@@RAW:r_n%d@@' % k], 340) for k in range(3)],
                    [B_('@@RAW:%s@@' % lbl(k, c), MENU + 1 + 3 * k + i) for k in range(3) for i, (_p, _n, c) in enumerate(PARTS)], columns=3)
    fn('p205/rib_dlg', [f'$dialog show @s {P28.inline(dlg)}'])
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {MENU}..{MENU + 99} run return run function bm:p205/act')
    act = [f'execute unless score @s bm.menu matches {MENU} run return run function bm:p28/stale']
    for k in range(3):
        for i, (_p, _n, c) in enumerate(PARTS):
            code = MENU + 1 + 3 * k + i
            act.append(f'execute if score #act bm.pay matches {code} unless score @s bm.chs{k} matches 1.. run return run function bm:p205/ribbon')
            act += [f'execute if score #act bm.pay matches {code} if score @s bm.chs{k} matches {IDX[w]} run return run function bm:p205/tg/{w}_{c}' for w in FOL]
    fn('p205/act', act)
    for w in FOL:
        for _p, pn, c in PARTS:
            fn(f'p205/tg/{w}_{c}', [f'execute if entity @s[tag=bm.no{c}_{w}] run return run function bm:p205/tg/{w}_{c}_on',
                                    f'tag @s add bm.no{c}_{w}', 'function bm:p205/refresh', 'function bm:p205/ribbon'])
            fn(f'p205/tg/{w}_{c}_on', [f'tag @s remove bm.no{c}_{w}', 'function bm:p205/refresh', 'function bm:p205/ribbon'])
    # (a toggle takes at once: the pieces of a part switched off go now, a part switched on comes on the next second)
    fn('p205/refresh', ['scoreboard players operation #me bm.pid = @s bm.pid'] +
       [f'execute if entity @s[tag=bm.no{c}_{w}] as @e[type=minecraft:item_display,tag=bm.chp_{w},tag=bm.chq_{part}] if score @s bm.pid = #me bm.pid run kill @s'
        for w in FOL for part, c in (('medal', 'md'), ('body', 'rg'), ('head', 'rg'))])

    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.chp]']
    fn('admin/champion', ['# (as a player with a follower near: every honour of every follower at its height)'] +
       [f'scoreboard players set @s bm.hn_{w} 1555' for w in FOL] + [f'function bm:p205/check/{w}' for w in FOL])
    G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/champion', 'yellow'), T('  every follower of yours a Champion of the Tide (all honours V)', 'gray')]))

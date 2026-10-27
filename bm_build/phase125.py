"""2.75: THE FOLLOWERS' FIXES - Democratus bigger and fairly beaten, KillerWatt sits, Emma and KillerWatt pair up, menus that know who's
out, traders with one name, no ghostly mounts, and the Arachno-Lantern's awakening.

DEMOCRATUS   drawn bigger (0.92 -> 1.06: he stands over Leo now, and Leo over Emma); his seat on the ground (knees up, the hips on
             the ground - his legs used to sink into it) and his vigil's kneel sit on the ground too. THE DUEL: a blow big enough to
             go straight past his yield (a mace, a charged attack) killed him outright - "Defeated", no scythe, and his body left
             standing. Now he can't be killed in a duel (a hidden cushion under his 400 health), a win can't turn into a loss if
             you're low when he yields, and a duelist's body never outlives him.
KILLERWATT   right-click him: he sits down on his haunches (again: he stands) - his own seated poses. The Spark still mounts him.
SPARKS FLY   (Emma + KillerWatt, the pair that was missing): you're quicker (Speed, Haste) and a shield of sparks comes back every
             half minute (Absorption); KillerWatt is tougher and charges faster; Emma brightens (Regeneration).
             (2.95b: no friendship in it. KillerWatt is Democratus's sin with the conscience burnt out - a parasite. The shard in his
             chest was cut from the Ethereal Gem her family kept, and it hums at her light: he wants her, as a host. She keeps her
             guard up and burns brighter to spite him; he feeds on the glow. The bonus is the friction.)
MENUS        every follower's menu says "Call for <name>" when they're not out (it said "Send her home" either way) - and calls them.
THE HEIST PLANS  a "Fixer's Lounge" button (the den without a heist - no fee).
TRADERS      one name each: the Market's (and the den's) traders showed their nameplate AND the game's own name tag.
NO GHOSTS    a follower's invisible mount (Emma's cat, Leo's wolf...) showed through as a ghost to a party: a tamed animal counts as
             on its owner's team, and party teams could see invisible teammates. They can't now.
APPEARING    every follower appears whole in its burst of light - its parts used to grow from nothing, each on its own, for a
             moment after it was called. KillerWatt's last flash takes him at once (he shrank).
THE LANTERN  it waits as a plain pumpkin sitting in a field. Come close: it shudders and rumbles - its face catches fire - eight legs
             burst out of it and it hunkers down - it heaves itself up to its full height - and ROARS, fire swirling round it, the
             ground shaking under you. Every step it takes after that shakes the ground (closer: harder).
"""
import re
from items import T
from nbt import snbt
import phase28 as P28
import phase79_art as KA
import phase97_art as DA
import phase99 as P99

CUSH = 600                                          # (hidden health under the duel's 400: a single blow can't kill him)
STORM = '#7ad06a'
WHO = {   # follower: (name, pronoun, colour, host type, host tag, try (as you), home (as you))
    'emma': ('Emma', 'her', '#ff8ad8', 'cat', 'bm.emmapet', 'p57/try_summon', 'p98/home/emma'),
    'celi': ('Celi', 'her', '#9ad8ff', 'wolf', 'bm.celipet', 'p66/try_summon', 'p98/home/celi'),
    'zib': ('Zib', 'him', '#3ad8c8', 'wolf', 'bm.zibpet', 'p72/zb/try_summon', 'p98/home/zib'),
    'cecil': ('Cecil', 'him', '#b48cff', 'wolf', 'bm.cecilpet', 'p46/pet/try_summon', 'p98/home/cecil'),
    'kw': ('KillerWatt', 'him', '#ffe040', 'wolf', 'bm.kxpet', 'p79/pet/try', 'p98/home/killerwatt'),
    'leo': ('Leo', 'him', '#5ab8e0', 'wolf', 'bm.leopet', 'p96/try_summon', 'p98/home/leo'),
    'demo': ('Democratus', 'him', STORM, 'wolf', 'bm.dmpet', 'p97/try_summon', 'p97/send_home'),
    # 2.78: the wardrobes of the rest (phase138)
    'apo': ('Apophiss', 'him', '#3ad06a', 'wolf', 'bm.appet', 'p131/try_summon', 'p98/home/apo'),
    'tul': ('Tullius', 'him', '#7ad8ff', 'wolf', 'bm.tupet', 'p132/try_summon', 'p98/home/tul'),
    'frog': ('the Frog', 'him', '#6ac850', 'wolf', 'bm.frogpet,tag=!bm.fvault,tag=!bm.ffpet', 'p136/fg/try', 'p138/home/frog'),
    'don': ('Donado', 'him', '#e8d29a', 'wolf', 'bm.donado,tag=!bm.ffpet', 'p136/dn/try', 'p138/home/don'),
    'pearl': ('Pearlman', 'him', '#5ac8ff', 'cat', 'bm.pmpet,tag=!bm.ffpet', 'p128/pm/try', 'p138/home/pearl'),
    'wil': ('Wilfrey', 'him', '#f4f4f4', 'wolf', 'bm.wilfrey', 'p2/wil/try_summon', 'p138/home/wil'),
    'fishy': ('Fishy', 'him', '#ffa040', 'wolf', 'bm.fypet', 'p145/try_summon', 'p145/home'),
    'dennis': ('Dennis', 'him', '#e0a040', 'wolf', 'bm.dwpet', 'p163/dw/try_summon', 'p163/dw/home'),
    'pistachio': ('Pistachio', 'him', '#7ae890', 'wolf', 'bm.pipet', 'p163/pi/try_summon', 'p163/pi/home'),
    'omega': ('King Omega', 'him', '#9fb4ff', 'wolf', 'bm.ompet', 'p170/try_summon', 'p170/home'),
    'ashur': ('Ashur', 'her', '#ff7a2a', 'wolf', 'bm.aspet', 'p185/try_summon', 'p185/home'),          # (2.86)
    'chef': ('the Chef', 'him', '#ffd07a', 'wolf', 'bm.kkpet', 'p186/try_summon', 'p186/home'),
    'neighbor': ('the Neighbor', 'him', '#7ab8ff', 'wolf', 'bm.nbpet', 'p187/try_summon', 'p187/home'),
    'ava': ('Queen Ava', 'her', '#6ad8e8', 'wolf', 'bm.avpet', 'p189/try_summon', 'p189/home'),                    # (2.87)
    'pearlq': ('Queen Pearl', 'her', '#5ae0d8', 'wolf', 'bm.pqpet', 'p190/try_summon', 'p190/home'),
    'bloo': ('Bloo', 'him', '#5a9ae8', 'wolf', 'bm.bopet', 'p191/try_summon', 'p191/home'),
    'stalker': ('The Stalker', 'it', '#a8ac70', 'wolf', 'bm.svpet', 'p193/try_summon', 'p193/home'),
    'lantern': ('The Arachno-Lantern', 'it', '#ff8a2a', 'wolf', 'bm.lnpet', 'p194/try_summon', 'p194/home'),
    'bender': ('Bender', 'him', '#e0a860', 'wolf', 'bm.bvpet', 'p195/try_summon', 'p195/home'),
    'bones': ('Bones', 'him', '#8ab0c8', 'wolf', 'bm.bjpet', 'p196/try_summon', 'p196/home'),
    'capshun': ('Mr. Capshun', 'him', '#f0f0f0', 'wolf', 'bm.mzpet', 'p198/try_summon', 'p198/home'),
    'kettle': ('Kettle', 'him', '#8ad8ff', 'wolf', 'bm.ktpet', 'p227/try_summon', 'p227/home'),
    'pxcecil': ('8-Bit Cecil', 'him', '#b070ff', 'wolf', 'bm.xcpet', 'p213c/try_summon', 'p213c/home'),
    'pxleo': ('8-Bit Leo', 'him', '#4ab0ff', 'wolf', 'bm.xlpet', 'p213l/try_summon', 'p213l/home'),
    'pxemma': ('8-Bit Emma', 'her', '#ff6ac8', 'wolf', 'bm.xmpet', 'p213e/try_summon', 'p213e/home'),
    'sky': ('The Sky Buddies', 'them', '#ffd04a', 'wolf', 'bm.ybpet', 'p211/try_summon', 'p211/home'),
}


def generate(G):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    PREFIX = G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    tick, fast, second = [], [], []
    objs = ['bm.shk', 'bm.shka', 'bm.salw', 'bm.ekab']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs

    def insert_after(fname, pred, lines, at_end_ok=False):
        L = G.FUNCS[fname]
        k = next((i for i, l in enumerate(L) if pred(l)), None)
        assert k is not None or at_end_ok, (fname, 'anchor')
        L[(k + 1) if k is not None else len(L):(k + 1) if k is not None else len(L)] = lines

    # ================================================================== APPEARING: parts summoned at their final size
    # (a display's first state goes out the moment it's summoned; the pose that follows in the same tick interpolates - from 0)
    def target(fname, pick=lambda l: True):
        l = next(l for l in G.FUNCS[fname] if 'scale:[' in l and pick(l))
        return re.search(r'scale:\[([0-9.]+)f', l).group(1)
    sizes = [('"bm.emp"', lambda l: '"bm.ep_wing' not in l, target('p57/grow')),
             ('"bm.cep"', lambda l: True, target('p66/grow')),
             ('"bm.lep"', lambda l: True, target('p96/grow')),
             ('"bm.dmp"', lambda l: '"bm.dp_scythe"' not in l, target('p97/grow', lambda l: 'tag=!bm.dp_scythe' in l)),
             ('"bm.dmp"', lambda l: '"bm.dp_scythe"' in l, target('p97/grow', lambda l: 'tag=bm.dp_scythe]' in l)),
             ('"bm.cpet"', lambda l: True, '1')]
    zero = re.compile(r'scale:\[0(?:\.0)?f,0(?:\.0)?f,0(?:\.0)?f\]')
    n = 0
    for name, L in G.FUNCS.items():
        for i, l in enumerate(L):
            if not l.startswith('summon minecraft:item_display') or not zero.search(l):
                continue
            for tag, ok, sc in sizes:
                if tag in l and ok(l):
                    L[i] = re.sub(r'interpolation_duration:\d+', 'interpolation_duration:0', zero.sub(f'scale:[{sc}f,{sc}f,{sc}f]', l)); n += 1
                    break
    assert n >= 20, n
    fd = G.FUNCS['p79/fade']
    k = next(i for i, l in enumerate(fd) if 'interpolation_duration:3,transformation:{scale:[0f,0f,0f]}' in l)
    fd[k] = fd[k].replace('interpolation_duration:3', 'interpolation_duration:0')

    # ================================================================== DEMOCRATUS: bigger (existing ones grow to match, once)
    S, SK = DA.RIG_SCALE, round(DA.RIG_SCALE / DA.SCYTHE_K, 4)
    second.append('execute as @e[type=minecraft:item_display,tag=bm.dmp,tag=!bm.dm106] run function bm:p125/dm/rescale')
    fn('p125/dm/rescale', ['tag @s add bm.dm106', 'execute store result score #sc bm.rng run data get entity @s transformation.scale[0] 100',
                           'execute unless score #sc bm.rng matches 1.. run return 0',
                           f'execute if entity @s[tag=bm.dp_scythe] run return run data merge entity @s[type=minecraft:item_display] {{transformation:{{scale:[{SK}f,{SK}f,{SK}f]}}}}',
                           f'data merge entity @s[type=minecraft:item_display] {{transformation:{{scale:[{S}f,{S}f,{S}f]}}}}'])
    ah = G.FUNCS['p97/add_hit']
    ah[0] = ah[0].replace('width:0.9f,height:1.5f', 'width:1.0f,height:1.9f')
    assert 'height:1.9f' in ah[0]
    second.append('execute as @e[type=minecraft:interaction,tag=bm.dmhit,tag=!bm.dmh106] run function bm:p125/dm/hit_size')
    fn('p125/dm/hit_size', ['tag @s add bm.dmh106', 'data merge entity @s[type=minecraft:interaction] {width:1.0f,height:1.9f}'])

    # ================================================================== DEMOCRATUS' DUEL: he can't be killed; a win stays a win; no body left behind
    sp = G.FUNCS['p97/duel/spawn']
    sp[0] = re.sub(r'(max_health",base:)400(?:\.0)?d', rf'\g<1>{400 + CUSH}d', sp[0])
    sp[0] = re.sub(r'Health:400(?:\.0)?f', f'Health:{400 + CUSH}f', sp[0])
    assert f'base:{400 + CUSH}d' in sp[0] and f'Health:{400 + CUSH}f' in sp[0], sp[0][:200]
    insert_after('p97/duel/tick', lambda l: 'store result score #h bm.rng run data get entity @s Health' in l,
                 [f'execute unless entity @s[tag=bm.dmyield] run scoreboard players remove #h bm.rng {CUSH}'])
    insert_after('p97/duel/mind', lambda l: 'store result score #h bm.rng run data get entity @s Health' in l, [f'scoreboard players remove #h bm.rng {CUSH}'])
    s2 = G.FUNCS['loop/second']
    k = next(i for i, l in enumerate(s2) if 'store result bossbar bm:dmb value run data get entity @s Health' in l)
    s2[k] = 'execute as @e[type=minecraft:vindicator,tag=bm.dmboss,limit=1] run function bm:p125/dm/bar'
    fn('p125/dm/bar', ['execute store result score #bh bm.rng run data get entity @s Health', f'scoreboard players remove #bh bm.rng {CUSH}',
                       'execute if score #bh bm.rng matches ..-1 run scoreboard players set #bh bm.rng 0',
                       'execute store result bossbar bm:dmb value run scoreboard players get #bh bm.rng'])
    G.FUNCS['p97/duel/win'].append('tag @a[tag=bm.dmfoe] add bm.dmwon')
    G.FUNCS['p97/duel/you'].insert(1, 'execute if entity @s[tag=bm.dmwon] run return run function bm:p125/dm/won_wait')
    fn('p125/dm/won_wait', ['scoreboard players set #f bm.rng 0',
                            'execute as @e[type=minecraft:vindicator,tag=bm.dmboss] if score @s bm.pid = #me bm.pid run scoreboard players set #f bm.rng 1',
                            'execute if score #f bm.rng matches 0 run function bm:p97/duel/prize'])
    G.FUNCS['p97/duel/prize'].insert(0, 'tag @s remove bm.dmwon')
    G.FUNCS['p97/duel/lose'].insert(0, 'execute as @e[type=minecraft:item_display,tag=bm.dmbp] if score @s bm.pid = #me bm.pid run kill @s')
    second.append('execute as @e[type=minecraft:item_display,tag=bm.dmbp] at @s run function bm:p125/dm/orphan')
    fn('p125/dm/orphan', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #f bm.rng 0',
                          'execute as @e[type=minecraft:vindicator,tag=bm.dmboss] if score @s bm.pid = #me bm.pid run scoreboard players set #f bm.rng 1',
                          'execute if score #f bm.rng matches 0 at @s run particle minecraft:electric_spark ~ ~1 ~ 0.3 0.6 0.3 0.2 6',
                          'execute if score #f bm.rng matches 0 run kill @s'])

    # ================================================================== KILLERWATT SITS (a click box beside him - not riding him: his back is for you)
    mv = G.FUNCS['p79/pet/move']
    k = next(i for i, l in enumerate(mv) if l.startswith('execute unless score @s bm.kxs = #st bm.rng'))
    mv.insert(k, 'execute if data entity @s {Sitting:1b} unless entity @s[tag=bm.kxrd] if predicate bm:p39/on_ground run scoreboard players set #st bm.rng 4')
    mv += ['execute if score #st bm.rng matches 4 run scoreboard players operation #f bm.rng %= #160 bm.rng',
           'execute if score #st bm.rng matches 4 if score #f bm.rng matches 0 run function bm:p79/pet/pose/sit_a',
           'execute if score #st bm.rng matches 4 if score #f bm.rng matches 50 run function bm:p79/pet/pose/sit_b',
           'execute if score #st bm.rng matches 4 if score #f bm.rng matches 100 run function bm:p79/pet/pose/sit_look',
           'execute if score #st bm.rng matches 4 if score #f bm.rng matches 130 run function bm:p79/pet/pose/sit_a']
    G.FUNCS['p79/pet/tick'].append('function bm:p125/kw/box')
    fn('p125/kw/box', ['execute if entity @s[tag=bm.kxrd] as @e[type=minecraft:interaction,tag=bm.kxhit] if score @s bm.kxid = #kid bm.rng run kill @s',
                       'execute if entity @s[tag=bm.kxrd] run return 0',
                       'execute as @e[type=minecraft:interaction,tag=bm.kxhit] if score @s bm.kxid = #kid bm.rng run tag @s add bm.kxhs',
                       'execute unless entity @e[type=minecraft:interaction,tag=bm.kxhs] run summon minecraft:interaction ~ ~ ~ {Tags:["bm.kxhit","bm.kxhs","bm.kxhnew"],width:1.1f,height:2.3f,response:1b}',
                       'scoreboard players operation @e[type=minecraft:interaction,tag=bm.kxhnew] bm.kxid = #kid bm.rng', 'tag @e[type=minecraft:interaction,tag=bm.kxhnew] remove bm.kxhnew',
                       'tp @e[type=minecraft:interaction,tag=bm.kxhs] ~ ~ ~', 'tag @e[type=minecraft:interaction,tag=bm.kxhs] remove bm.kxhs'])
    second.append('execute as @e[type=minecraft:interaction,tag=bm.kxhit] run function bm:p125/kw/box_orphan')
    fn('p125/kw/box_orphan', ['scoreboard players operation #kid bm.rng = @s bm.kxid', 'scoreboard players set #f bm.rng 0',
                              'execute as @e[type=minecraft:wolf,tag=bm.kxpet] if score @s bm.kxid = #kid bm.rng run scoreboard players set #f bm.rng 1',
                              'execute if score #f bm.rng matches 0 run kill @s'])
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.kxhit] if data entity @s interaction at @s run function bm:p125/kw/click',
             'execute as @e[type=minecraft:interaction,tag=bm.kxhit] if data entity @s attack run data remove entity @s attack']
    fn('p125/kw/click', ['scoreboard players operation #kid bm.rng = @s bm.kxid', 'execute on target run function bm:p125/kw/clicker', 'data remove entity @s interaction'])
    gems = ['ethereal_gem'] + [f'gem_{k}' for k in KA.EL_KEYS]
    fn('p125/kw/clicker', ['execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"kw_spark"}] run return run function bm:p79/spark',
                           'execute if predicate bm:p20/sneaking unless items entity @s weapon.mainhand * run return run function bm:p79/el/interact'] +
       [f'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{{bm:"{g}"}}] run return run function bm:p79/el/interact' for g in gems] +
       ['scoreboard players operation #me bm.pid = @s bm.pid',
        'execute as @e[type=minecraft:wolf,tag=bm.kxpet] if score @s bm.kxid = #kid bm.rng if score @s bm.pid = #me bm.pid at @s run function bm:p125/kw/sit'])
    fn('p125/kw/sit', ['execute store success score #s bm.rng if data entity @s {Sitting:1b}',
                       'execute if score #s bm.rng matches 1 run data modify entity @s Sitting set value 0b',
                       'execute if score #s bm.rng matches 0 run data modify entity @s Sitting set value 1b',
                       'particle minecraft:electric_spark ~ ~1 ~ 0.6 0.6 0.6 0.2 14', 'playsound minecraft:entity.wolf.ambient neutral @a[distance=..16] ~ ~ ~ 0.8 0.5',
                       'scoreboard players set @s bm.kxs -1'])

    # ================================================================== SPARKS FLY: Emma + KillerWatt
    second.append('execute as @e[type=minecraft:cat,tag=bm.emmapet,tag=!bm.ffpet] at @s if entity @e[type=minecraft:wolf,tag=bm.kxpet,distance=..16] run function bm:p125/duo/ek')
    fn('p125/duo/ek', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #k bm.rng 0',
                       'execute as @e[type=minecraft:wolf,tag=bm.kxpet,distance=..16] if score @s bm.pid = #me bm.pid run scoreboard players set #k bm.rng 1',
                       'execute if score #k bm.rng matches 0 run return 0', 'scoreboard players set #o bm.rng 0',
                       'execute on owner if entity @s[distance=..24] run scoreboard players set #o bm.rng 1',
                       'execute if score #o bm.rng matches 0 run return 0',
                       'execute on owner run function bm:p125/duo/ek_you',
                       'execute as @e[type=minecraft:wolf,tag=bm.kxpet,distance=..16] if score @s bm.pid = #me bm.pid run function bm:p125/duo/ek_kw',
                       'execute unless predicate bm:p97/regen run effect give @s minecraft:regeneration 5 0 true',
                       'execute store result score #r bm.rng run random value 1..140', 'execute if score #r bm.rng matches 1 run function bm:p125/duo/ek_banter'])
    fn('p125/duo/ek_you', ['effect give @s minecraft:speed 3 0 true', 'effect give @s minecraft:haste 3 0 true', 'scoreboard players add @s bm.ekab 1',
                           'execute if score @s bm.ekab matches 30.. run effect give @s minecraft:absorption 30 0 true',
                           'execute if score @s bm.ekab matches 30.. at @s run particle minecraft:electric_spark ~ ~1 ~ 0.5 0.8 0.5 0.1 20',
                           'execute if score @s bm.ekab matches 30.. run scoreboard players set @s bm.ekab 0',
                           'execute unless entity @s[advancements={bm:story/emma_kw=true}] run function bm:p125/duo/ek_first'])
    fn('p125/duo/ek_kw', ['effect give @s minecraft:resistance 3 0 true', 'scoreboard players add @s bm.kxch 1'])
    EM, EML, KW, KWL = '#ff8ad8', '#ffd0ec', '#74d462', '#c8f0c0'
    fn('p125/duo/ek_first', ['advancement grant @s only bm:story/emma_kw', 'effect give @s minecraft:absorption 30 0 true',
                             tellraw('@s', PREFIX + [T('Sparks Fly! ', KW, bold=True), T('The shard in KillerWatt\'s chest hums at Emma\'s light, and he hasn\'t taken his eyes off her since. She won\'t give him the satisfaction of flinching. Between his hunger and her nerve: you\'re quicker on your feet and with your hands, a shield of sparks comes back every half minute; KillerWatt is tougher and charges faster - he feeds on her glow - and Emma burns brighter to spite him.', 'gray')]),
                             tellraw('@s', [T('Emma: ', EM, bold=True), T('"Keep your sparks to yourself. I know what that gem was before you got your claws on it."', EML)]),
                             tellraw('@s', [T('KillerWatt: ', KW, bold=True), T('*the shard in his chest pulses in time with her heartbeat - and he grins*', KWL, italic=True)])])
    banter = [('Emma', "Don't. Even. Think about it.", 'KillerWatt', '*a tendril of current creeps toward her hand - and snaps back when she glares*'),
              ('KillerWatt', '*he circles her slowly, the way he sizes up a host*', 'Emma', "Find another body to crawl into. This one's taken."),
              ('Emma', 'That gem used to sing. Now it just screams.', 'KillerWatt', '*the shard flares a sick green - he laughs without a sound*'),
              ('KillerWatt', '*a bat jerks in the air, eyes flashing green - and drops when he lets it go*', 'Emma', "You didn't have to do that. You never have to. You just like it."),
              ('Emma', 'Democratus at least believed he was saving us.', 'KillerWatt', '*a crackling hiss, like a laugh - whatever Democratus believed, none of it came with him*')]
    voice = {'Emma': (EM, EML), 'KillerWatt': (KW, KWL)}
    line = lambda w, txt: tellraw('@s', [T(f'{w}: ', voice[w][0], bold=True), T(txt if w == 'KillerWatt' else f'"{txt}"', voice[w][1], italic=w == 'KillerWatt')])
    fn('p125/duo/ek_banter', [f'execute store result score #b bm.rng run random value 1..{len(banter)}'] +
       [f'execute if score #b bm.rng matches {i} on owner if entity @s[tag=!bm.hush] run function bm:p125/duo/ekb{i}' for i in range(1, len(banter) + 1)])
    for i, (a, at_, b, bt) in enumerate(banter, 1):
        fn(f'p125/duo/ekb{i}', [line(a, at_), line(b, bt)])
    G.wjson('bm/advancement/story/emma_kw.json', {
        'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
        'display': {'icon': {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': 'bm:kw_spark'}},
                    'title': T('Sparks Fly', 'yellow'), 'description': T('Have Emma and KillerWatt at your side at once', 'gray'),
                    'frame': 'task', 'show_toast': True, 'announce_to_chat': True, 'hidden': True}})

    # ================================================================== MENUS: "Call for <name>" when they're not out
    home_re = re.compile(r'label:\[\{text:"Send (?:her|him|it|them) home",color:"gray",italic:false\}\]')
    for w, (nm, pron, col, host, tag, try_, home) in WHO.items():
        assert (try_ in G.FUNCS and home in G.FUNCS) or w in ('apo', 'tul', 'frog', 'don', 'pearl', 'wil', 'fishy', 'dennis', 'pistachio', 'omega', 'ashur', 'chef', 'neighbor', 'ava', 'pearlq', 'bloo', 'stalker', 'lantern', 'bender', 'bones', 'capshun', 'kettle', 'pxcecil', 'pxleo', 'pxemma', 'sky'), (w, try_, home)   # (2.78's six, 2.79's Fishy: built later)
        b = P99.BASE[w]
        dl = G.FUNCS[f'p99/dlg/{w}']
        assert home_re.search(dl[0]), w
        dl[0] = home_re.sub('label:$(r_home)', dl[0])
        out = [f'scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #out bm.rng 0',
               f'execute as @e[type=minecraft:{host},tag={tag}] if score @s bm.pid = #me bm.pid run scoreboard players set #out bm.rng 1']
        m = G.FUNCS[f'p99/menu/{w}']
        m[len(m) - 1:len(m) - 1] = out + [
            f'data modify storage bm:ui wd.r_home set value {snbt(T(f"Call for {nm}", col, bold=True))}',
            f'execute if score #out bm.rng matches 1 run data modify storage bm:ui wd.r_home set value {snbt(T(f"Send {pron} home", "gray"))}']
        a = G.FUNCS[f'p99/act/{w}']
        orig = P99.HOME[w]
        k = next(i for i, l in enumerate(a) if l == f'execute if score #act bm.pay matches {b} run return run function bm:{orig}')
        a[k] = f'execute if score #act bm.pay matches {b} run return run function bm:p125/hc/{w}'
        fn(f'p125/hc/{w}', out + [f'execute if score #out bm.rng matches 1 run return run function bm:{home}',
                                  'execute if entity @s[tag=bm.gvp] if dimension bm:gutter run return run ' + say("In the vault your crew answers the Fixer's Ledger - Raid Crew.", '#9ad0ff'),
                                  f'function bm:{try_}'])
    # (Democratus' challenge - sneak + use - has its own "Send him home")
    dm = G.FUNCS['p97/menu']
    shows = [l for l in dm if 'dialog show' in l]
    assert len(shows) == 2 and all('Send him home' in l for l in shows)
    call = lambda l: l.replace('text:"Send him home"', 'text:"Call for Democratus"')
    keep = [l for l in dm if 'dialog show' not in l]
    d_won, d_new = shows[0].split('run return run ', 1)[1], shows[1]       # (his scythe already yours / not yet)
    G.FUNCS['p97/menu'] = keep + [
        'scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #out bm.rng 0',
        'execute as @e[type=minecraft:wolf,tag=bm.dmpet] if score @s bm.pid = #me bm.pid run scoreboard players set #out bm.rng 1',
        'execute if score #out bm.rng matches 0 if score @s bm.dmsc matches 1.. run return run ' + call(d_won),
        'execute if score #out bm.rng matches 0 run return run ' + call(d_new),
        shows[0], shows[1]]
    da = G.FUNCS['p97/act']
    k = next(i for i, l in enumerate(da) if 'run function bm:p97/send_home' in l)
    da[k] = da[k].replace('function bm:p97/send_home', 'function bm:p125/hc/demo')

    # ================================================================== TRADERS: one name each (the nameplate stays; the game's own tag goes)
    G.FUNCS['load'][-1:-1] = ['team add bm.npcs', 'team modify bm.npcs nametagVisibility never', 'team modify bm.npcs collisionRule never']
    second += ['execute as @e[type=#bm:p56_traders,tag=bm.plated,team=] run team join bm.npcs @s',
               # (and never two plates on one trader)
               'execute as @e[type=#bm:p56_traders,tag=bm.plated] at @s if entity @e[type=minecraft:text_display,tag=bm.plate,distance=..0.7] run function bm:p125/one_plate']
    fn('p125/one_plate', ['tag @e[type=minecraft:text_display,tag=bm.plate,distance=..0.7,sort=nearest,limit=1] add bm.pkeep',
                          'kill @e[type=minecraft:text_display,tag=bm.plate,tag=!bm.pkeep,distance=..0.7]',
                          'tag @e[type=minecraft:text_display,tag=bm.pkeep] remove bm.pkeep'])

    # ================================================================== NO GHOSTS: a party can't see invisible "teammates" (a tamed mount counts as one)
    mk = G.FUNCS['p67/make']
    k = next(i for i, l in enumerate(mk) if 'seeFriendlyInvisibles true' in l)
    mk[k] = mk[k].replace('seeFriendlyInvisibles true', 'seeFriendlyInvisibles false')
    G.FUNCS['p67/sync1'].append('$execute if entity @s[tag=!bm.sfi0] run team modify bm.p$(id) seeFriendlyInvisibles false')
    G.FUNCS['p67/sync1'].append('tag @s add bm.sfi0')

    # ================================================================== THE SHAKE: a few ticks of the camera jolting (as the player)
    tick.append('execute as @a[scores={bm.shk=1..}] at @s run function bm:p125/shake')
    amp = {1: (0.35, 0.25), 2: (0.8, 0.55), 3: (1.5, 1.0)}
    fn('p125/shake', ['scoreboard players remove @s bm.shk 1', 'scoreboard players operation #sp bm.rng = @s bm.shk', 'scoreboard players operation #sp bm.rng %= #2 bm.rng'] +
       sum(([f'execute if score @s bm.shka matches {a} if score #sp bm.rng matches 0 run rotate @s ~{x} ~{y}',
             f'execute if score @s bm.shka matches {a} if score #sp bm.rng matches 1 run rotate @s ~-{x} ~-{y}'] for a, (x, y) in amp.items()), []) +
       ['execute if score @s bm.shk matches 0 run scoreboard players reset @s bm.shka'])
    def quake(r_in, r_out, t, a_in, a_out):
        return [f'execute as @a[distance=..{r_in},gamemode=!spectator] run function bm:p125/jolt {{t:{t},a:{a_in}}}',
                f'execute as @a[distance={r_in}..{r_out},gamemode=!spectator] run function bm:p125/jolt {{t:{t},a:{a_out}}}']
    fn('p125/jolt', ['$scoreboard players set @s bm.shk $(t)', '$execute unless score @s bm.shka matches $(a).. run scoreboard players set @s bm.shka $(a)'])

    # ================================================================== THE LANTERN: it waits as a plain pumpkin; it wakes when you come near
    sel = '@e[type=minecraft:item_display,tag=bm.salsel'
    body_model = lambda m: f'data modify entity {sel},tag=bm.salp_body,limit=1] item.components."minecraft:item_model" set value "bm:{m}"'
    ini = G.FUNCS['p82/init']
    k = next(i for i, l in enumerate(ini) if l == 'function bm:p82/rig')
    ini[k + 1:k + 1] = ['function bm:p82/pose/dorm', body_model('sal_body_plain'), 'tag @s add bm.saldorm', 'data merge entity @s {Invulnerable:1b}']
    tk = G.FUNCS['p82/tick']
    k = next(i for i, l in enumerate(tk) if l.startswith('scoreboard players operation #sid bm.rng = @s bm.salid'))
    tk[k + 1:k + 1] = ['execute if entity @s[tag=bm.saldorm] run return run function bm:p125/sal/dorm',
                       'execute if entity @s[tag=bm.salwake] run return run function bm:p125/sal/wake']
    near = 'gamemode=!creative,gamemode=!spectator'
    pick = ['execute as @e[type=minecraft:item_display,tag=bm.salp,tag=!bm.saldying] if score @s bm.salid = #sid bm.rng run tag @s add bm.salsel']
    fn('p125/sal/rig_dorm', ['function bm:p82/rig', 'function bm:p82/pose/dorm', body_model('sal_body_plain')])
    fn('p125/sal/dorm', pick + [f'execute unless entity {sel},tag=bm.salp_body] run function bm:p125/sal/rig_dorm',
                                f'execute rotated as @s rotated ~ 0 run tp {sel}] ~ ~ ~ ~ 0', 'function bm:p82/ground',
                                'execute store result score #r bm.rng run random value 1..120',
                                'execute if score #r bm.rng matches 1 if entity @a[distance=..40] run playsound minecraft:block.wood.place hostile @a[distance=..40] ~ ~2 ~ 1 0.4',
                                f'execute if entity @a[distance=..14,{near}] run function bm:p125/sal/wake_start', f'tag {sel}] remove bm.salsel'])
    fn('p125/sal/wake_start', ['tag @s remove bm.saldorm', 'tag @s add bm.salwake', 'scoreboard players set @s bm.salw 0'])
    # the awakening, tick by tick (as the host)
    W = []
    at = lambda t, cmd: W.append(f'execute if score @s bm.salw matches {t} run {cmd}')
    for i, t in enumerate(range(1, 22, 3)):                           # it shudders
        at(t, f'function bm:p82/pose/dorm_{"l" if i % 2 == 0 else "r"}')
    at(22, 'function bm:p82/pose/dorm')
    W += ['execute if score @s bm.salw matches 1..22 run particle minecraft:large_smoke ~ ~5.4 ~ 1.6 0.3 1.6 0.02 3',
          'execute if score @s bm.salw matches 6..22 run particle minecraft:small_flame ~ ~2.8 ~ 3 1.4 3 0.01 3']
    at(1, 'playsound minecraft:block.respawn_anchor.charge hostile @a[distance=..48] ~ ~2 ~ 2 0.5')
    at(1, 'playsound minecraft:entity.warden.heartbeat hostile @a[distance=..48] ~ ~2 ~ 2 0.6')
    for t in (8, 16): at(t, 'playsound minecraft:entity.zombie.attack_wooden_door hostile @a[distance=..48] ~ ~2 ~ 1.5 0.5')
    for c in quake(14, 32, 22, 1, 1): at(1, c)
    at(24, 'execute facing entity @p feet run tp @s ~ ~ ~ ~ 0')         # its face catches fire - turned on you
    at(24, f'execute rotated as @s rotated ~ 0 run tp {sel}] ~ ~ ~ ~ 0')
    at(24, body_model('sal_body'))
    at(24, 'function bm:p82/pose/dorm_lit')
    at(24, 'playsound minecraft:entity.blaze.shoot hostile @a[distance=..64] ~ ~3 ~ 2 0.5')
    at(24, 'playsound minecraft:item.firecharge.use hostile @a[distance=..64] ~ ~3 ~ 2 0.6')
    at(24, 'playsound minecraft:entity.ghast.warn hostile @a[distance=..64] ~ ~3 ~ 1.5 0.5')
    at(24, 'execute rotated as @s rotated ~ 0 positioned ^ ^2.8 ^3.4 run particle minecraft:flame ~ ~ ~ 2.4 1 0.3 0.15 140')
    at(24, 'execute rotated as @s rotated ~ 0 positioned ^ ^2.8 ^3.4 run particle minecraft:flash{color:[1.0,0.6,0.2,1.0]} ~ ~ ~ 0 0 0 0 1')
    at(34, 'function bm:p82/pose/crouch')                              # eight legs burst out; it hunkers down
    at(34, 'playsound minecraft:entity.spider.ambient hostile @a[distance=..64] ~ ~2 ~ 3 0.5')
    at(34, 'playsound minecraft:block.piston.extend hostile @a[distance=..64] ~ ~2 ~ 2 0.5')
    at(34, 'playsound minecraft:entity.zombie.break_wooden_door hostile @a[distance=..64] ~ ~2 ~ 2 0.6')
    at(34, 'particle minecraft:block{block_state:"minecraft:rooted_dirt"} ~ ~0.3 ~ 7 0.2 7 0 160')
    at(34, 'particle minecraft:large_smoke ~ ~1 ~ 5 0.5 5 0.05 60')
    for c in quake(16, 36, 10, 2, 1): at(34, c)
    at(46, 'function bm:p82/pose/rise')                                # it heaves itself up
    at(46, 'playsound minecraft:entity.iron_golem.repair hostile @a[distance=..64] ~ ~4 ~ 2 0.5')
    for t in (52, 62): at(t, 'playsound minecraft:entity.ravager.step hostile @a[distance=..64] ~ ~ ~ 2 0.5')
    for t in (52, 62): at(t, 'particle minecraft:block{block_state:"minecraft:rooted_dirt"} ~ ~0.3 ~ 9 0.2 9 0 60')
    at(74, 'function bm:p82/pose/flare')                               # and ROARS
    at(74, 'function bm:p82/intro')
    at(74, 'playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..96] ~ ~8 ~ 3 0.6')
    at(74, 'playsound minecraft:entity.ghast.scream hostile @a[distance=..96] ~ ~8 ~ 2 0.5')
    for c in quake(18, 40, 20, 3, 2): at(74, c)
    import math
    for kf in range(16):                                               # fire swirling up round it
        t = 74 + 2 * kf
        for j in range(3):
            a = math.radians(kf * 40 + j * 120); r = 7.5 - kf * 0.2; h = 0.8 + kf * 0.75
            W.append(f'execute if score @s bm.salw matches {t} rotated as @s rotated ~ 0 positioned ^{r * math.cos(a):.2f} ^{h:.2f} ^{r * math.sin(a):.2f} '
                     f'run particle minecraft:flame ~ ~ ~ 0.3 0.3 0.3 0.03 10')
        if kf % 3 == 0:
            W.append(f'execute if score @s bm.salw matches {t} run particle minecraft:lava ~ ~6 ~ 4 2 4 0 6')
    at(98, 'function bm:p82/pose/stand')
    fn('p125/sal/wake', ['scoreboard players add @s bm.salw 1'] + pick +
       [f'execute unless entity {sel},tag=bm.salp_body] run function bm:p82/rig', f'execute rotated as @s rotated ~ 0 run tp {sel}] ~ ~ ~ ~ 0'] + W +
       ['execute if score @s bm.salw matches 110.. run function bm:p125/sal/awake', f'tag {sel}] remove bm.salsel'])
    fn('p125/sal/awake', ['tag @s remove bm.salwake', 'data merge entity @s {Invulnerable:0b}', 'scoreboard players set @s bm.salc 30',
                          'scoreboard players set @s bm.sals -1', body_model('sal_body')])
    # (while it sleeps: no bar, no burning aura; it leaves at dawn - or once nobody's come within 96 blocks for two minutes)
    G.FUNCS['p82/sec'].insert(0, 'execute if entity @s[tag=bm.saldorm] run return run function bm:p125/sal/dorm_sec')
    fn('p125/sal/dorm_sec', ['execute if entity @a[distance=..96] run scoreboard players set @s bm.sallone 0', 'scoreboard players add @s bm.sallone 1',
                             'execute if score @s bm.sallone matches 120.. run function bm:p82/leave'])
    # every step it takes shakes the ground
    mv = G.FUNCS['p82/move']
    for f_ in (0, 20):
        k = next(i for i, l in enumerate(mv) if f'if score #f bm.rng matches {f_} run playsound minecraft:entity.iron_golem.step' in l)
        mv.insert(k + 1, f'execute if score #st bm.rng matches 1 if score #f bm.rng matches {f_} run function bm:p125/sal/step')
    fn('p125/sal/step', quake(12, 26, 4, 2, 1) + ['particle minecraft:block{block_state:"minecraft:rooted_dirt"} ~ ~0.2 ~ 8 0.1 8 0 24'])
    fn('admin/lantern_wake', ['execute as @e[type=minecraft:giant,tag=bm.saldorm] at @s run function bm:p125/sal/wake_start'])

    # ================================================================== FAINTING: they sink down, dizzy, for a second - then their own burst
    FT = 20
    FAINT = [  # (key, counter, fell, part tag, select tag, fade tag, the collapse, the sound)
        ('emma', 'bm.emz', 'p57/fell', 'bm.emp', 'bm.emsel', 'bm.emfade', 'p57/pose/sit_a', 'minecraft:entity.allay.hurt'),
        ('celi', 'bm.cez', 'p66/fell', 'bm.cep', 'bm.cesel', 'bm.cefade', 'p66/pose/sit_a', 'minecraft:entity.player.hurt_freeze'),
        ('leo', 'bm.lez', 'p96/fell', 'bm.lep', 'bm.lesel', 'bm.lefade', 'p96/pose/sit_a', 'minecraft:entity.player.hurt_drown'),
        ('demo', 'bm.dmz', 'p97/fell', 'bm.dmp', 'bm.dmsel', 'bm.dmfade', 'p97/pose/kneel', 'minecraft:entity.lightning_bolt.thunder'),
        ('cecil', 'bm.cpg', 'p46/pet/fell', 'bm.cpet', 'bm.cpsel', 'bm.cpfade', None, 'minecraft:entity.witch.hurt')]
    for key, cnt, fell, part, seltag, fade, collapse, snd in FAINT:
        old = f'execute if score @s {cnt} matches 4.. run function bm:{fell}'
        hits = [(nm, i) for nm, L in G.FUNCS.items() for i, l in enumerate(L) if l == old]
        assert len(hits) == 1, (key, hits)
        nm, i = hits[0]
        G.FUNCS[nm][i:i + 1] = [f'execute if score @s {cnt} matches 4 run function bm:p125/faint/{key}', f'execute if score @s {cnt} matches {4 + FT}.. run function bm:{fell}']
        fn(f'p125/faint/{key}', [f'execute as @e[type=minecraft:item_display,tag={part},tag=!{fade}] if score @s bm.pid = #me bm.pid run tag @s add {seltag}'] +
           ([f'function bm:{collapse}'] if collapse else
            [f'execute as @e[type=minecraft:item_display,tag={seltag}] run scoreboard players set @s bm.fsk 16', f'tag @e[type=minecraft:item_display,tag={seltag}] add bm.fsink']) +
           [f'tag @e[type=minecraft:item_display,tag={seltag}] remove {seltag}', 'tag @s add bm.fdizzy', f'scoreboard players set @s bm.fsk {FT}',
            f'playsound {snd} neutral @a[distance=..20] ~ ~ ~ 0.8 1.1', 'playsound minecraft:entity.generic.big_fall neutral @a[distance=..20] ~ ~ ~ 0.5 1.3'])
    objs2 = ['bm.fsk']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs2]
    G.OBJECTIVES += objs2
    tick += ['execute as @e[type=minecraft:item_display,tag=bm.fsink] at @s run function bm:p125/faint/sink',
             'execute as @e[type=minecraft:item_display,tag=bm.fdizzy] at @s run function bm:p125/faint/dizzy']
    fn('p125/faint/sink', ['tp @s ~ ~-0.025 ~', 'scoreboard players remove @s bm.fsk 1', 'execute if score @s bm.fsk matches ..0 run tag @s remove bm.fsink'])
    fn('p125/faint/dizzy', ['scoreboard players remove @s bm.fsk 1', 'execute if score @s bm.fsk matches ..0 run return run tag @s remove bm.fdizzy',
                            'scoreboard players operation #d bm.rng = @s bm.fsk', 'scoreboard players operation #d bm.rng %= #4 bm.rng',
                            'execute if score #d bm.rng matches 0 run particle minecraft:wax_off ~ ~1.6 ~ 0.25 0.08 0.25 0 2',
                            'execute if score #d bm.rng matches 2 run particle minecraft:crit ~ ~1.6 ~ 0.2 0.05 0.2 0 2'])

    # ================================================================== THE BUTTONS: read the click first
    # (2.74-2.75 codes were put in front of the line that reads the clicked code from the trigger - so they saw the last click's
    #  code, and a button only worked when clicked twice. They go after it now.)
    pa = G.FUNCS['p28/act']
    k = pa.index('scoreboard players operation #act bm.pay = @s bm.act')
    assert pa[k + 1] == 'scoreboard players set @s bm.act 0'
    early = pa[:k]
    assert early and all(l.startswith('execute if score #act bm.pay matches ') for l in early), early
    G.FUNCS['p28/act'] = pa[k:k + 2] + early + pa[k + 2:]

    # ================================================================== ETHEREAL KILLERWATT, RIDDEN: he walks on the ground (hops, climbs) - and flies
    # only when you take off: jump again in mid-air. Look up to rise, down to sink; touch down and he walks again.
    ETH = len(KA.EL_KEYS) + 1
    rd = G.FUNCS['p79/pet/ride']
    def swap(L, old, new):
        k = L.index(old); L[k:k + 1] = new if isinstance(new, list) else [new]
    swap(rd, f'execute if score #kel bm.rng matches {ETH} run data modify entity @s NoGravity set value 1b',
         [f'execute if score #kel bm.rng matches {ETH} if score #jp bm.rng matches 1 unless score @s bm.kxjp matches 1 unless predicate bm:p39/on_ground unless entity @s[tag=bm.kxfly] run function bm:p125/kw/takeoff',
          'execute if entity @s[tag=bm.kxfly] if predicate bm:p39/on_ground unless score #pitch bm.rng matches ..-25 run function bm:p125/kw/land',
          'execute if entity @s[tag=bm.kxfly] run data modify entity @s NoGravity set value 1b'])
    swap(rd, f'execute if score #kel bm.rng matches {ETH} run function bm:p79/pet/fly', 'execute if entity @s[tag=bm.kxfly] run function bm:p79/pet/fly')
    rd.insert(rd.index('execute if entity @s[tag=bm.kxfly] run data modify entity @s NoGravity set value 1b') + 1,
              'execute unless entity @s[tag=bm.kxfly] run data modify entity @s NoGravity set value 0b')
    # THUNDER LEAP's landing: the ride runs before his parts are picked for the tick - the landing pose and the arms' un-flexing
    # found nothing, and his arms stayed flexed (forearms up) in the leap's pose. The landing picks his parts itself now.
    lt = G.FUNCS['p79/pet/leap_tick']
    k = lt.index('function bm:p79/pet/pose/slam_dn'); assert lt[k + 1] == 'function bm:p79/unflex'
    lt[k:k + 2] = ['function bm:p125/kw/leap_land']
    fn('p125/kw/leap_land', ['scoreboard players operation #kel bm.rng = @s bm.kxel', 'scoreboard players operation #kid bm.rng = @s bm.kxid',
                             'execute as @e[type=minecraft:item_display,tag=bm.kxp_pet,distance=..12] if score @s bm.kxid = #kid bm.rng run tag @s add bm.kxsel',
                             'function bm:p79/pet/pose/slam_dn', 'function bm:p79/unflex', 'tag @e[type=minecraft:item_display,tag=bm.kxsel] remove bm.kxsel'])
    # (one already stuck that way from before: un-flexed the first time he's seen)
    second.append('execute as @e[type=minecraft:wolf,tag=bm.kxpet,tag=!bm.kxleap,tag=!bm.kxuf] at @s run function bm:p125/kw/unstick')
    fn('p125/kw/unstick', ['tag @s add bm.kxuf', 'execute unless score @s bm.kxatk matches 1.. unless score @s bm.kxho matches 1.. run function bm:p125/kw/leap_land'])
    swap(rd, f'execute unless score #kel bm.rng matches {ETH} if score #jp bm.rng matches 1 if predicate bm:p39/on_ground run data modify entity @s Motion[1] set value 0.62d',
         ['execute unless entity @s[tag=bm.kxfly] if score #jp bm.rng matches 1 if predicate bm:p39/on_ground run data modify entity @s Motion[1] set value 0.62d',
          'scoreboard players operation @s bm.kxjp = #jp bm.rng'])
    dv = G.FUNCS['p79/pet/drive']
    for i, l in enumerate(dv):
        if 'function bm:p79/pet/climb_up' in l:
            assert l.startswith(f'execute unless score #kel bm.rng matches {ETH} ')
            dv[i] = l.replace(f'execute unless score #kel bm.rng matches {ETH} ', 'execute unless entity @s[tag=bm.kxfly] ')
    G.FUNCS['p79/pet/unride'].append('tag @s remove bm.kxfly')
    fn('p125/kw/takeoff', ['tag @s add bm.kxfly', 'data modify entity @s NoGravity set value 1b', 'data modify entity @s Motion[1] set value 0.3d',
                           'particle minecraft:end_rod ~ ~0.4 ~ 0.6 0.2 0.6 0.08 24', 'particle minecraft:reverse_portal ~ ~0.4 ~ 0.6 0.2 0.6 0.05 30',
                           'playsound minecraft:entity.phantom.flap neutral @a[distance=..20] ~ ~ ~ 1 0.6', 'playsound minecraft:block.beacon.power_select neutral @a[distance=..20] ~ ~ ~ 0.4 1.6'])
    G.FUNCS['p79/pet/mount'].append(f'execute if score @s bm.kxel matches {ETH} run ' + title('@s', 'actionbar', [T('On his back. ', '#c8a0ff', bold=True),
        T('Walk to stride; jump to hop; walls - he climbs them. Jump again in mid-air: he FLIES (look up to rise, down to sink; touch down to walk). ', 'gray'),
        T('Sneak to get off.', 'dark_gray')]))
    fn('p125/kw/land', ['tag @s remove bm.kxfly', 'data modify entity @s NoGravity set value 0b', 'particle minecraft:end_rod ~ ~0.1 ~ 0.6 0.05 0.6 0.04 10'])
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.kxjp dummy']
    G.OBJECTIVES += ['bm.kxjp']

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second

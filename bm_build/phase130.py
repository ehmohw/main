"""2.76: WRAITHFIRE EMMA - her Wraithfire Form, on and off; she fights hard; she flies you.

THE FORM (she has the Wraithfire Heart): WRAITHFIRE FORM: ON / OFF in her menu (sneak + use her ribbon).
  On  - she stays ethereal in soul-blue armour, wings and blade, fights (below), can carry you, and everyone she watches
        over has Fire Resistance and Regeneration.
  Off - she's her usual self: her buffs, her charge, her own Ethereal Form now and then. The heart stays with her; take it
        back from the menu.
FIGHTING - a strike a second from up to 24 blocks (her Ethereal Form: 8 damage from 14):
  SOUL CRESCENT  14 to the target (18 with a gem), splashing everything round it; they burn.
  WRAITH LANCE   a piercing bolt down a line at the farthest foe: 16 to everything on it (walls stop it).
  SOUL WARD      monsters that come at you are seared and thrown back.
  YOUR MARK      whatever you hit, she goes for next.
  BATTLE STYLE (her menu):
    GUARDIAN  monsters near you first (10 blocks); a stronger ward (4 blocks, 8); surrounded, she whirls.
    HUNTRESS  28 blocks; a lance every second; the biggest threat (a boss) first.
    TEMPEST   every strike bursts wide (5 blocks, 9) and her charge fills twice as fast.
CHARGED ATTACKS: fighting fills her wraithfire (about 12 seconds; Tempest 6). Charged, she lets it go on the next foe:
  SOUL CYCLONE      blue fire whirls round you for 3 seconds: everything within 6 is cut (8 a turn) and dragged in.
  REQUIEM CRESCENT  she winds up and hurls a crescent wave 24 blocks: 22 to everything in its path.
  FALLING STAR      she climbs - then dives on the strongest foe: 40 to it (50 with a gem), 14 round it, all thrown up.
  (Which one: surrounded - the Cyclone; a boss about - the Star; otherwise the Crescent. Carrying you: not the Star.)
WINGS FOR TWO: use her ribbon right beside her, sneak + right-click her empty-handed (up you go as you let go of sneak), or
  FLY WITH ME in her menu: she wraps her arms round you from behind and lifts you off your feet - KillerWatt's ethereal flight: walk forward to fly, look up (or jump) to rise, look down to
  sink, let go of everything to hover. Sneak to be set down; let go high up and you drift down softly. She keeps fighting
  with her lances while she carries you.
"""
import math
from items import T, ITEMS
from nbt import snbt, F
import phase57 as P57
import phase57_art as EA
import phase127 as P127

SOUL, PINK = P127.SOUL, P127.PINK
FOE = 'type=#bm:hostile,tag=!bm.npc'
ME = '@e[type=minecraft:cat,tag=bm.emme,limit=1]'          # (the Emma whose turn it is)
BY = f'minecraft:magic by {ME}'
DMG, DMG_GEM, LANCE_D = 14, 18, 16
CYC_D, REQ_D, STAR_D, STAR_GEM, STAR_SPL = 8, 22, 40, 50, 14
FLY = 0.44                                                  # (KillerWatt's ethereal flight: blocks a tick)
# style: range, lance every n s, splash radius/damage, ward radius/damage, charge a second, foes round you for the Cyclone
STYLES = {1: dict(name='Guardian', col='#8ae4ff', r=16, lance=3, sr=4, sd=7, wr=4, wd=8, ch=8, cyc=2,
                  tip='Monsters near you first; a stronger Soul Ward round you; surrounded, she whirls.'),
          2: dict(name='Huntress', col=SOUL, r=28, lance=1, sr=3, sd=6, wr=3, wd=5, ch=8, cyc=4,
                  tip='28 blocks; a Wraith Lance every second; the biggest threat - a boss - first.'),
          3: dict(name='Tempest', col='#b8f4ff', r=24, lance=2, sr=5, sd=9, wr=3, wd=5, ch=16, cyc=3,
                  tip='Every strike bursts wide; her wraithfire charges twice as fast.')}
C_FLY, C_STYLE = 7310, 7311                                 # (her menu: 7311-7313 the styles)
# where she holds you from (the carry): her feet above her host's, and behind you
CARRY_DY, CARRY_BACK = 0.55, 0.45                         # (her eyes just over your head)

# (the heart's own words, and her ribbon's: her Wraithfire Form now)
for _iid, _old, _new in (('wraithfire_heart', 'Emma: she can stay ethereal.', 'Emma: her Wraithfire Form - she fights, she flies you.'),
                         ('emma_ribbon', 'Give her a Wraithfire Heart: she can stay ethereal.', 'Give her a Wraithfire Heart: her Wraithfire Form.')):
    if _iid in ITEMS:
        for _l in ITEMS[_iid]['comps']['minecraft:lore']:
            if isinstance(_l, dict) and _l.get('text') == _old: _l['text'] = _new


# ===================================================================== poses (her rig: see phase57_art)
P, torso, limb, wings = EA.P, EA.torso, EA.limb, EA.wings
CARRY_FRAMES = 8
POSES = {}
for _i in range(CARRY_FRAMES):
    _p = 2 * math.pi * _i / CARRY_FRAMES
    POSES[f'carry_{_i}'] = P(0.03 * math.sin(_p + 0.6),
                             body=torso(lean=8, tilt=1.2 * math.sin(_p)),
                             head=torso(lean=6, tilt=-5, turn=16),                       # (peeking over your right shoulder)
                             armr=limb(1, 30, 8), arml=limb(-1, 30, 8),                # (her hands under your arms, from behind)
                             legr=limb(1, -16 - 6 * math.sin(_p + 1)), legl=limb(-1, -26 + 6 * math.sin(_p + 1)),
                             **wings(10 + 24 * math.sin(_p), 6 + 32 * math.sin(_p - 1.1), -7 * math.cos(_p)))
POSES['cyc'] = P(0.05, body=torso(lean=4), head=torso(lean=-6), armr=limb(1, 10, 88), arml=limb(-1, 10, 88),
                 legr=limb(1, -12), legl=limb(-1, -24), **EA.WINGS_UP)
POSES['rq_up'] = P(0.16, body=torso(lean=-10), head=torso(lean=-12), armr=limb(1, 176, 4), arml=limb(-1, 150, -16),
                   legr=limb(1, -8), legl=limb(-1, -30), **EA.WINGS_UP)
POSES['rq_dn'] = P(0.0, body=torso(lean=22, turn=12), head=torso(lean=8), armr=limb(1, -36, -6), arml=limb(-1, -10, 44),
                   legr=limb(1, -36), legl=limb(-1, -12), **EA.WINGS_DN)
POSES['star_up'] = P(0.10, body=torso(lean=-14), head=torso(lean=-16), armr=limb(1, 168, 10), arml=limb(-1, 140, 30),
                     legr=limb(1, -4), legl=limb(-1, -16), **EA.WINGS_UP)
POSES['star_dn'] = P(0.0, body=torso(lean=56), head=torso(lean=18), armr=limb(1, 118, -4), arml=limb(-1, 90, 30),
                     legr=limb(1, -48), legl=limb(-1, -40), **wings(-30, -36, -12))
DUR = dict({f'carry_{i}': 3 for i in range(CARRY_FRAMES)}, cyc=3, rq_up=8, rq_dn=2, star_up=10, star_dn=2)

# the wraith look: her ethereal parts re-cast in soul fire (the head keeps its own model, so her faces still play)
WPARTS = ('body', 'armr', 'arml', 'legr', 'legl')
WINGS = ('wingr', 'wingl', 'wingro', 'winglo')


def generate(G):
    fn, wjson, title, tellraw, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    emsay = lambda txt: title('@s', 'actionbar', [T('Emma: ', PINK, bold=True), T(txt, '#ffd0ec')])
    objs = ['bm.emwc', 'bm.emsty', 'bm.emxa', 'bm.emxk', 'bm.emln', 'bm.emyaw', 'bm.emfo', 'bm.emlt']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + ['scoreboard players set #10 bm.rng 10', 'scoreboard players set #6 bm.rng 6']
    G.OBJECTIVES += objs
    tick, second = [], []
    S = EA.RIG_SCALE
    U = S / 16
    qf = lambda q: [F(round(v, 4)) for v in q]
    parts = lambda p: f'@e[type=minecraft:item_display,tag=bm.emsel,tag=bm.ep_{p}]'
    model = lambda p, m: f'execute as {parts(p)} run data modify entity @s item.components."minecraft:item_model" set value "bm:{m}"'
    cond = lambda pre, cmd: f'{pre} {cmd[len("execute "):]}' if cmd.startswith('execute ') else f'{pre} run {cmd}'     # (one execute, no 'run execute')

    # ================================================================== poses and placements
    for name, pose in POSES.items():
        lines = []
        for p in EA.PARTS:
            rot, tr = EA.part_xf(pose, p)
            lines.append(f'execute as {parts(p)} run data merge entity @s {{start_interpolation:0,interpolation_duration:{DUR[name]},'
                         f'transformation:{{left_rotation:{snbt(qf(rot))},translation:[{tr[0]:.4f}f,{tr[1]:.4f}f,{tr[2]:.4f}f]}}}}')
        fn(f'p130/pose/{name}', lines)
    def place(name, dy, back=0.0):
        out = []
        for p in EA.PARTS:
            x, y, z = EA.PIVOT[p]
            out.append(f'execute positioned ^{-x * U:.4f} ^{y * U + dy:.4f} ^{-z * U - back:.4f} run tp {parts(p)} ~ ~ ~ ~ 0')
        fn(name, out)
    place('p130/place_carry', CARRY_DY, CARRY_BACK)
    for k, dy in ((1, 1.6), (2, 2.4), (3, 3.3)):
        place(f'p130/place_lift{k}', dy)
    fn('p130/anim11', ['scoreboard players operation #f bm.rng = @s bm.emf', f'scoreboard players operation #f bm.rng %= #{3 * CARRY_FRAMES} bm.rng'] +
       [f'execute if score #f bm.rng matches {3 * i} run function bm:p130/pose/carry_{i}' for i in range(CARRY_FRAMES)])
    G.FUNCS['load'][-1:-1] = [f'scoreboard players set #{3 * CARRY_FRAMES} bm.rng {3 * CARRY_FRAMES}']

    # her state: 11 carrying you, 12 a charged attack (its own timeline poses her)
    st = G.FUNCS['p57/state']
    st[0:0] = ['execute if entity @s[tag=bm.emcar] run return run scoreboard players set #st bm.rng 11',
               'execute if score @s bm.emxa matches 1.. run return run scoreboard players set #st bm.rng 12']
    an = G.FUNCS['p57/anim']
    an[0:0] = ['execute if score @s bm.ems matches 11 run return run function bm:p130/anim11', 'execute if score @s bm.ems matches 12 run return 0']
    tk = G.FUNCS['p57/tick']
    k = tk.index('function bm:p57/anim')
    tk[k + 1:k + 1] = ['execute if score @s bm.emxa matches 1.. run function bm:p130/x/tick',
                       'execute if entity @s[tag=bm.emcar] run function bm:p130/carry/tick']
    end = tk.index('tag @a[tag=bm.emown] remove bm.emown')
    tk[end:end] = ['execute if score @s bm.ems matches 11 rotated as @s rotated ~ 0 run function bm:p130/place_carry',
                   'execute if score @s bm.ems matches 12 if score @s bm.emxk matches 3 if score @s bm.emxa matches 2..5 rotated as @s rotated ~ 0 run function bm:p130/place_lift1',
                   'execute if score @s bm.ems matches 12 if score @s bm.emxk matches 3 if score @s bm.emxa matches 6..9 rotated as @s rotated ~ 0 run function bm:p130/place_lift2',
                   'execute if score @s bm.ems matches 12 if score @s bm.emxk matches 3 if score @s bm.emxa matches 10..13 rotated as @s rotated ~ 0 run function bm:p130/place_lift3',
                   'execute if score @s bm.ems matches 12 unless score @s bm.emxk matches 3 rotated as @s rotated ~ 0 run function bm:p57/place_fly',
                   'execute if score @s bm.ems matches 12 if score @s bm.emxk matches 3 unless score @s bm.emxa matches 2..13 rotated as @s rotated ~ 0 run function bm:p57/place_fly']

    # ================================================================== the wraith look, on and off with the form
    def look(form, wing_form):
        return [model(p, f'{form}_{p}') for p in WPARTS] + [model(w, f'{wing_form}_{w}') for w in WINGS]
    sel_parts = 'execute as @e[type=minecraft:item_display,tag=bm.emp,tag=!bm.emfade] if score @s bm.pid = #me bm.pid run tag @s add bm.emsel'
    fn('p130/look/apply', look('ew', 'ew') + [cond('execute if entity @s[tag=bm.emcar]', model('armr', 'ew_armr_free')),
                                             'execute as @e[type=minecraft:item_display,tag=bm.emsel] run data merge entity @s {brightness:{block:15,sky:15},interpolation_duration:10}'])
    fn('p130/look/on', ['tag @s add bm.emwl', sel_parts, 'function bm:p130/look/apply', 'tag @e[type=minecraft:item_display,tag=bm.emsel] remove bm.emsel',
                        'particle minecraft:soul_fire_flame ~ ~1.6 ~ 0.5 0.9 0.5 0.06 40', 'particle minecraft:flash{color:[0.55,0.92,1.0,1.0]} ~ ~1.6 ~ 0 0 0 0 1',
                        'playsound minecraft:particle.soul_escape neutral @a[distance=..20] ~ ~ ~ 2 0.9'])
    fn('p130/look/off', ['tag @s remove bm.emwl', 'execute if entity @s[tag=bm.emcar] run function bm:p130/carry/drop', sel_parts,
                         'execute if score @s bm.eme matches 1.. run function bm:p130/look/eth', 'tag @e[type=minecraft:item_display,tag=bm.emsel] remove bm.emsel'])
    fn('p130/look/eth', look('ee', 'ee'))
    sec = G.FUNCS['p57/sec']
    k = sec.index('execute if score @s bm.eme matches 1.. run function bm:p57/ethereal')
    sec[k:k] = ['execute if entity @s[tag=bm.emwfs] unless entity @s[tag=bm.emwl] run function bm:p130/look/on',
                'execute unless entity @s[tag=bm.emwfs] if entity @s[tag=bm.emwl] run function bm:p130/look/off']
    G.FUNCS['p57/rerig'] += ['execute if entity @s[tag=bm.emwl] run function bm:p130/look/apply']

    # ================================================================== fighting: a turn a second, in her Wraithfire Form
    eth = G.FUNCS['p57/ethereal']
    eth.insert(0, 'execute if entity @s[tag=bm.emwfs] run return run function bm:p130/eth')
    fn('p130/eth', ['scoreboard players set @s bm.eme 30', 'effect give @s minecraft:resistance 3 2 true', 'tag @s add bm.emme',
                    'scoreboard players set #sty bm.rng 2', 'execute on owner run tag @s add bm.emo2',
                    'execute on owner if score @s bm.emsty matches 1..3 run scoreboard players operation #sty bm.rng = @s bm.emsty'] +
       [f'execute if score #sty bm.rng matches {s} run function bm:p130/st/{s}' for s in STYLES] +
       ['tag @s remove bm.emme', 'tag @a[tag=bm.emo2] remove bm.emo2'])
    fn('p130/is_big', ['execute if entity @s[tag=bm.boss] run return 1', 'execute if entity @s[tag=bm.salboss] run return 1',
                       'execute if entity @s[tag=bm.kxboss] run return 1', 'execute if entity @s[tag=bm.vboss] run return 1',
                       'execute if entity @s[type=#bm:p130_big] run return 1', 'return 0'])
    wjson('bm/tags/entity_type/p130_big.json', {'values': [f'minecraft:{m}' for m in ('wither', 'ender_dragon', 'warden', 'elder_guardian', 'ravager', 'giant')]})
    for s, c in STYLES.items():
        R = c['r']
        foe_r = f'@e[{FOE},distance=..{R}]'
        fn(f'p130/st/{s}', [f'execute if entity {foe_r} unless score @s bm.emwc matches 100.. run scoreboard players add @s bm.emwc {c["ch"]}',
                            f'execute if score @s bm.emwc matches 100.. run function bm:p130/st/{s}/charged',
                            'execute if score @s bm.emxa matches 1.. run return 0',
                            f'execute if entity @s[tag=bm.emcar] run return run function bm:p130/st/{s}/air',
                            f'function bm:p130/st/{s}/strike',
                            'scoreboard players add @s bm.emln 1',
                            f'execute if score @s bm.emln matches {c["lance"]}.. run function bm:p130/st/{s}/lance',
                            f'execute as @a[tag=bm.emo2] at @s run function bm:p130/st/{s}/ward'])
        # carrying you: no blade - the lance (from the air), and the ward round you
        fn(f'p130/st/{s}/air', ['scoreboard players add @s bm.emln 1', f'execute if score @s bm.emln matches {max(1, c["lance"] - 1)}.. run function bm:p130/st/{s}/lance',
                                f'execute as @a[tag=bm.emo2] at @s run function bm:p130/st/{s}/ward'])
        # the strike: your mark, else (Huntress) a boss, (Guardian) the nearest to you, else the nearest
        strike = [f'execute as @e[{FOE},tag=bm.emfoc,distance=..{R}] if score @s bm.emfo = #me bm.pid run tag @s add bm.emtgc',
                  f'execute as @e[tag=bm.emtgc,distance=..{R},sort=nearest,limit=1] run tag @s add bm.emtg',
                  'tag @e[tag=bm.emtgc,distance=..48] remove bm.emtgc']
        if s == 2:
            strike += [f'execute unless entity @e[tag=bm.emtg,distance=..48] as @e[{FOE},distance=..{R},sort=nearest] if function bm:p130/is_big run tag @s add bm.emtgc',
                       f'execute as @e[tag=bm.emtgc,distance=..{R},sort=nearest,limit=1] run tag @s add bm.emtg', 'tag @e[tag=bm.emtgc,distance=..48] remove bm.emtgc']
        if s == 1:
            strike += [f'execute unless entity @e[tag=bm.emtg,distance=..48] as @a[tag=bm.emo2] at @s as @e[{FOE},distance=..10,sort=nearest,limit=1] run tag @s add bm.emtg']
        strike += [f'execute unless entity @e[tag=bm.emtg,distance=..48] as @e[{FOE},distance=..{R},sort=nearest,limit=1] run tag @s add bm.emtg',
                   f'execute as @e[tag=bm.emtg,distance=..48,limit=1] at @s run function bm:p130/st/{s}/hit',
                   'tag @e[tag=bm.emtg,distance=..48] remove bm.emtg']
        fn(f'p130/st/{s}/strike', strike)
        fn(f'p130/st/{s}/hit', [f'execute as {ME} at @s run function bm:p130/swing', 'summon minecraft:marker ~ ~ ~ {Tags:["bm.emaim"]}', 'tag @s add bm.emtgt',
                                f'execute unless entity @e[type=minecraft:cat,tag=bm.emme,tag=bm.emgem] run damage @s {DMG} {BY}',
                                f'execute if entity @e[type=minecraft:cat,tag=bm.emme,tag=bm.emgem] run damage @s {DMG_GEM} {BY}',
                                'data merge entity @s {Fire:100s}',
                                f'execute as @e[{FOE},distance=..{c["sr"]},tag=!bm.emtgt] at @s run function bm:p130/splash{c["sd"]}',
                                'tag @s remove bm.emtgt',
                                'particle minecraft:sweep_attack ~ ~1 ~ 0.6 0.3 0.6 0 3', 'particle minecraft:soul_fire_flame ~ ~1 ~ 0.6 0.5 0.6 0.04 18',
                                f'particle minecraft:dust{{color:[0.35,0.88,1.0],scale:1.6}} ~ ~1 ~ {c["sr"] * 0.3:.1f} 0.4 {c["sr"] * 0.3:.1f} 0 24',
                                f'execute facing entity {ME} feet run function bm:p130/crescent',
                                f'scoreboard players add {ME} bm.emwc 4',
                                'playsound minecraft:entity.player.attack.sweep neutral @a[distance=..20] ~ ~ ~ 1 1.2',
                                'playsound minecraft:particle.soul_escape neutral @a[distance=..20] ~ ~ ~ 1.4 1.1'])
        # the lance: your mark, else the farthest - a piercing line, stopped by walls
        fn(f'p130/st/{s}/lance', ['scoreboard players set @s bm.emln 0',
                                  f'execute as @e[{FOE},tag=bm.emfoc,distance=4..{R}] if score @s bm.emfo = #me bm.pid run tag @s add bm.emltc',
                                  f'execute as @e[tag=bm.emltc,distance=..{R},sort=furthest,limit=1] run tag @s add bm.emlt',
                                  'tag @e[tag=bm.emltc,distance=..48] remove bm.emltc',
                                  f'execute unless entity @e[tag=bm.emlt,distance=..48] as @e[{FOE},distance=4..{R},sort=furthest,limit=1] run tag @s add bm.emlt',
                                  f'execute if entity @e[tag=bm.emlt,distance=..48] positioned ~ ~2.0 ~ facing entity @e[tag=bm.emlt,distance=..48,limit=1] eyes run function bm:p130/lance{R}',
                                  'execute if entity @e[tag=bm.emlt,distance=..48] run playsound minecraft:entity.blaze.shoot neutral @a[distance=..24] ~ ~ ~ 0.8 1.6',
                                  'execute if entity @e[tag=bm.emlt,distance=..48] run playsound minecraft:item.trident.throw neutral @a[distance=..24] ~ ~ ~ 1 1.4',
                                  'tag @e[tag=bm.emlt,distance=..48] remove bm.emlt', 'tag @e[tag=bm.emlh,distance=..48] remove bm.emlh'])
        fn(f'p130/st/{s}/ward', [f'execute as @e[{FOE},distance=..{c["wr"]}] at @s run function bm:p130/ward{c["wd"]}'])
        # charged: told once; the next foe, it goes
        pick = ['scoreboard players set @s bm.emxk 2',
                'scoreboard players set #n bm.rng 0', f'execute as @a[tag=bm.emo2] at @s store result score #n bm.rng if entity @e[{FOE},distance=..8]']
        star = [f'execute unless entity @s[tag=bm.emcar] as @e[{FOE},distance=..{R}] if function bm:p130/is_big run scoreboard players set #big bm.rng 1']
        if s == 2:        # (Huntress: the Star first)
            pick += ['scoreboard players set #big bm.rng 0'] + star + [f'execute unless score #big bm.rng matches 1 if score #n bm.rng matches {c["cyc"]}.. run scoreboard players set @s bm.emxk 1',
                                                                       'execute if score #big bm.rng matches 1 run scoreboard players set @s bm.emxk 3']
        elif s == 1:      # (Guardian: whirl round you, else the Star, else the Crescent)
            pick += [f'execute if score #n bm.rng matches {c["cyc"]}.. run scoreboard players set @s bm.emxk 1', 'scoreboard players set #big bm.rng 0'] + star + \
                    ['execute if score @s bm.emxk matches 2 if score #big bm.rng matches 1 run scoreboard players set @s bm.emxk 3']
        else:             # (Tempest: never the Star - the Cyclone or the Crescent)
            pick += [f'execute if score #n bm.rng matches {c["cyc"]}.. run scoreboard players set @s bm.emxk 1']
        fn(f'p130/st/{s}/charged', ['scoreboard players set @s bm.emwc 100', 'execute unless entity @s[tag=bm.emwcn] run function bm:p130/charged_note',
                                    'execute if score @s bm.emxa matches 1.. run return 0', f'execute unless entity {foe_r} run return 0'] + pick +
           ['scoreboard players set @s bm.emwc 0', 'tag @s remove bm.emwcn', 'scoreboard players set @s bm.emxa 1'])
        # the lance's path, a step at a time
        steps = math.ceil(R / 0.9)
        path = []
        for i in range(1, steps + 1):
            d = round(0.9 * i, 2)
            path += [f'execute positioned ^ ^ ^{d} unless block ~ ~ ~ #bm:grap_pass run return run particle minecraft:soul ~ ~ ~ 0.2 0.2 0.2 0.02 8',
                     f'particle minecraft:soul_fire_flame ^ ^ ^{d} 0.04 0.04 0.04 0.005 2']
            if i % 2 == 0: path.append(f'particle minecraft:end_rod ^ ^ ^{d} 0 0 0 0 1')
            path.append(f'execute positioned ^ ^ ^{d} as @e[{FOE},distance=..1.3,tag=!bm.emlh] at @s run function bm:p130/lance_hit')
        fn(f'p130/lance{R}', path)
    for d in sorted({c['sd'] for c in STYLES.values()}):
        fn(f'p130/splash{d}', [f'damage @s {d} {BY}', 'data merge entity @s {Fire:60s}', 'particle minecraft:soul_fire_flame ~ ~0.8 ~ 0.3 0.4 0.3 0.02 6'])
    for d in sorted({c['wd'] for c in STYLES.values()}):
        fn(f'p130/ward{d}', [f'damage @s {d} {BY}', 'data merge entity @s {Fire:60s}', 'particle minecraft:soul_fire_flame ~ ~1 ~ 0.4 0.5 0.4 0.08 14',
                             'particle minecraft:flash{color:[0.5,0.9,1.0,1.0]} ~ ~1 ~ 0 0 0 0 1', 'playsound minecraft:particle.soul_escape neutral @a[distance=..16] ~ ~ ~ 1.5 0.8'])
    fn('p130/lance_hit', ['tag @s add bm.emlh', f'damage @s {LANCE_D} {BY}', 'data merge entity @s {Fire:100s}',
                          'particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.5 0.3 0.06 12'])
    fn('p130/swing', ['scoreboard players set @s bm.emk 6', 'kill @e[type=minecraft:marker,tag=bm.emaim,distance=..48]'])
    fn('p130/crescent', [f'particle minecraft:dust{{color:[0.45,0.92,1.0],scale:1.3}} ^ ^{1.0 + 0.06 * i:.2f} ^{0.6 * i:.1f} 0 0 0 0 1' for i in range(1, 22)] +
       [f'particle minecraft:soul_fire_flame ^ ^{1.0 + 0.06 * i:.2f} ^{0.6 * i:.1f} 0 0 0 0 1' for i in range(2, 22, 3)])
    fn('p130/charged_note', ['tag @s add bm.emwcn', 'particle minecraft:soul_fire_flame ~ ~2 ~ 0.6 0.9 0.6 0.05 30',
                             'playsound minecraft:block.beacon.power_select neutral @a[distance=..16] ~ ~ ~ 0.8 1.7',
                             'execute on owner run ' + title('@s', 'actionbar', [T('✦ Emma\'s wraithfire is CHARGED', SOUL, bold=True),
                                                                                 T(' - she lets it go on the next foe.', 'gray')])])
    # what you hit, she goes for
    wjson('bm/advancement/p130/mark.json', {'criteria': {'h': {'trigger': 'minecraft:player_hurt_entity', 'conditions': {
        'entity': [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:entity_type': '#bm:hostile'}}]}}},
        'rewards': {'function': 'bm:p130/mark'}})
    fn('p130/mark', ['advancement revoke @s only bm:p130/mark', 'execute unless score @s bm.emwf matches 1 run return 0',
                     'execute unless score @s bm.emst matches 1 run return 0', 'scoreboard players operation #me bm.pid = @s bm.pid',
                     f'execute as @e[{FOE},distance=..8,nbt={{HurtTime:10s}},sort=nearest,limit=1] run function bm:p130/mark1'])
    fn('p130/mark1', ['tag @s add bm.emfoc', 'scoreboard players operation @s bm.emfo = #me bm.pid'])

    # ================================================================== the charged attacks (a timeline each, run every tick)
    fn('p130/x/tick', ['scoreboard players add @s bm.emxa 1', 'tag @s add bm.emme', 'execute on owner run tag @s add bm.emo3',
                       'execute if score @s bm.emxk matches 1 run function bm:p130/x/cyc', 'execute if score @s bm.emxk matches 2 run function bm:p130/x/req',
                       'execute if score @s bm.emxk matches 3 run function bm:p130/x/star',
                       'tag @s remove bm.emme', 'tag @a[tag=bm.emo3] remove bm.emo3'])
    name = lambda txt: 'execute on owner at @s run ' + title('@a[distance=..32]', 'actionbar', [T('Emma: ', PINK, bold=True), T(txt, SOUL, bold=True)])
    fn('p130/x/done', ['scoreboard players set @s bm.emxa 0', 'scoreboard players set @s bm.emxk 0', 'scoreboard players set @s bm.ems -1',
                       'execute as @e[type=minecraft:marker,tag=bm.emwave] if score @s bm.pid = #me bm.pid run kill @s',
                       'tag @e[tag=bm.emrqh,distance=..64] remove bm.emrqh', 'tag @e[tag=bm.emstar,distance=..64] remove bm.emstar'])
    # SOUL CYCLONE - round you: a whirl that cuts and drags
    ring = lambda r, a0, n: [f'particle minecraft:soul_fire_flame ^{r * math.cos(math.radians(a0 + 360 * j / n)):.2f} ^{0.4 + 0.25 * (j % 3):.2f} '
                             f'^{r * math.sin(math.radians(a0 + 360 * j / n)):.2f} 0.05 0.05 0.05 0.01 1' for j in range(n)]
    for f6 in range(6):
        fn(f'p130/x/cyc_fx{f6}', ring(2.2, f6 * 10, 8) + ring(4.4, -f6 * 12, 10) + ring(6.0, f6 * 15, 12) +
           ['particle minecraft:sweep_attack ^ ^1 ^3 0.4 0.3 0.4 0 1'])
    fn('p130/x/cyc', ['execute if score @s bm.emxa matches 2 run function bm:p130/x/cyc_start',
                      'execute unless entity @s[tag=bm.emcar] run scoreboard players add @s bm.emyaw 36',
                      'execute unless entity @s[tag=bm.emcar] store result entity @s Rotation[0] float 1 run scoreboard players get @s bm.emyaw',
                      'scoreboard players operation #t bm.rng = @s bm.emxa', 'scoreboard players operation #t bm.rng %= #6 bm.rng'] +
       [f'execute if score @s bm.emxa matches 2..61 if score #t bm.rng matches {f6} as @a[tag=bm.emo3] at @s rotated ~ 0 run function bm:p130/x/cyc_fx{f6}' for f6 in range(6)] +
       ['scoreboard players operation #t bm.rng = @s bm.emxa', 'scoreboard players operation #t bm.rng %= #10 bm.rng',
        'execute if score @s bm.emxa matches 3..61 if score #t bm.rng matches 1 as @a[tag=bm.emo3] at @s run function bm:p130/x/cyc_hit',
        'execute if score @s bm.emxa matches 62.. run function bm:p130/x/done'])
    fn('p130/x/cyc_start', [name('SOUL CYCLONE'), 'function bm:p130/pose/cyc', 'scoreboard players set @s bm.emyaw 0',
                            'playsound minecraft:item.trident.riptide_3 neutral @a[distance=..32] ~ ~ ~ 1 0.8',
                            'playsound minecraft:entity.blaze.shoot neutral @a[distance=..32] ~ ~ ~ 1 0.6'])
    fn('p130/x/cyc_hit', [f'execute as @e[{FOE},distance=..6] at @s run function bm:p130/x/cyc_one',
                          'particle minecraft:sweep_attack ~ ~1 ~ 3 0.4 3 0 12', 'playsound minecraft:entity.player.attack.sweep neutral @a[distance=..24] ~ ~ ~ 1 0.9'])
    fn('p130/x/cyc_one', [f'damage @s {CYC_D} {BY}', 'data merge entity @s {Fire:80s}',
                          'execute unless entity @a[tag=bm.emo3,distance=..1.8] facing entity @a[tag=bm.emo3,limit=1] feet positioned ^ ^ ^0.7 '
                          'if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~ ~'])
    # REQUIEM CRESCENT - a wind-up, then a wave down the line to the nearest foe
    fn('p130/x/req', ['execute if score @s bm.emxa matches 2 run function bm:p130/x/req_start',
                      'execute if score @s bm.emxa matches 3..13 run particle minecraft:soul_fire_flame ~ ~2.8 ~ 0.8 0.6 0.8 0.02 6',
                      'execute if score @s bm.emxa matches 3..13 run particle minecraft:end_rod ~ ~3.2 ~ 0.3 0.3 0.3 0.02 2',
                      'execute if score @s bm.emxa matches 14 run function bm:p130/x/req_go',
                      'execute if score @s bm.emxa matches 15..30 as @e[type=minecraft:marker,tag=bm.emwave] if score @s bm.pid = #me bm.pid at @s run function bm:p130/x/req_wave',
                      'execute if score @s bm.emxa matches 31.. run function bm:p130/x/done'])
    fn('p130/x/req_start', [name('REQUIEM CRESCENT'), 'function bm:p130/pose/rq_up',
                            f'execute unless entity @s[tag=bm.emcar] facing entity @e[{FOE},distance=..32,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0',
                            'playsound minecraft:block.beacon.activate neutral @a[distance=..32] ~ ~ ~ 1 1.6',
                            'playsound minecraft:entity.warden.sonic_charge neutral @a[distance=..32] ~ ~ ~ 0.6 1.6'])
    fn('p130/x/req_go', ['function bm:p130/pose/rq_dn',
                         'execute positioned ~ ~1.2 ~ run summon minecraft:marker ~ ~ ~ {Tags:["bm.emwave","bm.emwnew"]}',
                         'scoreboard players operation @e[type=minecraft:marker,tag=bm.emwnew,distance=..3] bm.pid = #me bm.pid',
                         f'execute if entity @e[{FOE},distance=..32] positioned ~ ~1.2 ~ facing entity @e[{FOE},distance=..32,sort=nearest,limit=1] feet run tp @e[type=minecraft:marker,tag=bm.emwnew,distance=..3,limit=1] ~ ~ ~ ~ 0',
                         f'execute unless entity @e[{FOE},distance=..32] positioned ~ ~1.2 ~ rotated as @s run tp @e[type=minecraft:marker,tag=bm.emwnew,distance=..3,limit=1] ~ ~ ~ ~ 0',
                         'tag @e[type=minecraft:marker,tag=bm.emwnew] remove bm.emwnew',
                         'playsound minecraft:entity.player.attack.sweep neutral @a[distance=..32] ~ ~ ~ 1.4 0.6',
                         'playsound minecraft:item.trident.riptide_1 neutral @a[distance=..32] ~ ~ ~ 1 1.2'])
    arc = [f'particle minecraft:soul_fire_flame ^{0.5 * j} ^{1.1 - 0.06 * j * j:.2f} ^ 0 0 0 0 1' for j in range(-5, 6)] + \
          [f'particle minecraft:dust{{color:[0.5,0.95,1.0],scale:1.8}} ^{0.5 * j} ^{1.0 - 0.06 * j * j:.2f} ^-0.3 0 0 0 0 1' for j in range(-5, 6)]
    fn('p130/x/req_wave', ['tp @s ^ ^ ^1.5', 'execute at @s run function bm:p130/x/req_wave2'])
    fn('p130/x/req_wave2', ['execute unless block ~ ~ ~ #bm:grap_pass run return run function bm:p130/x/req_wall'] + arc +
       ['particle minecraft:sweep_attack ~ ~1 ~ 0.6 0.2 0.6 0 2',
        f'execute as @e[{FOE},distance=..2.6,tag=!bm.emrqh] at @s run function bm:p130/x/req_hit'])
    fn('p130/x/req_hit', ['tag @s add bm.emrqh', f'damage @s {REQ_D} {BY}', 'data merge entity @s {Fire:100s}',
                          'particle minecraft:soul_fire_flame ~ ~1 ~ 0.4 0.6 0.4 0.08 16'])
    fn('p130/x/req_wall', ['particle minecraft:soul ~ ~1 ~ 0.6 0.6 0.6 0.05 20', 'playsound minecraft:particle.soul_escape neutral @a[distance=..20] ~ ~ ~ 2 0.6', 'kill @s'])
    # FALLING STAR - up she goes, then down on the strongest foe
    fn('p130/x/star', ['execute if score @s bm.emxa matches 2 run function bm:p130/x/star_start',
                       'execute if score @s bm.emxa matches 3..13 run particle minecraft:soul_fire_flame ~ ~3 ~ 0.4 0.8 0.4 0.03 6',
                       'execute if score @s bm.emxa matches 14 run function bm:p130/x/star_dive',
                       'execute if score @s bm.emxa matches 15 run function bm:p130/x/star_hit',
                       'execute if score @s bm.emxa matches 26.. run function bm:p130/x/done'])
    fn('p130/x/star_start', [name('FALLING STAR'), 'function bm:p130/pose/star_up',
                             f'execute as @e[{FOE},distance=..32,sort=nearest] if function bm:p130/is_big run tag @s add bm.emstc',
                             'execute as @e[tag=bm.emstc,distance=..32,sort=nearest,limit=1] run tag @s add bm.emstar', 'tag @e[tag=bm.emstc,distance=..48] remove bm.emstc',
                             f'execute unless entity @e[tag=bm.emstar,distance=..32] as @e[{FOE},distance=..32,sort=nearest,limit=1] run tag @s add bm.emstar',
                             'playsound minecraft:entity.phantom.flap neutral @a[distance=..32] ~ ~ ~ 1.2 0.6',
                             'playsound minecraft:block.beacon.power_select neutral @a[distance=..32] ~ ~ ~ 1 0.6'])
    fn('p130/x/star_dive', ['execute unless entity @e[tag=bm.emstar,distance=..40] run return run function bm:p130/x/done',
                            'function bm:p130/pose/star_dn',
                            'execute at @e[tag=bm.emstar,distance=..40,limit=1] run tp @s ~ ~ ~',
                            'particle minecraft:soul_fire_flame ~ ~3 ~ 0.2 2 0.2 0.05 40', 'playsound minecraft:entity.phantom.swoop neutral @a[distance=..32] ~ ~ ~ 1.4 0.8'])
    fn('p130/x/star_hit', ['execute as @e[tag=bm.emstar,distance=..6,limit=1] run tag @s add bm.emtgt',
                           f'execute unless entity @s[tag=bm.emgem] as @e[tag=bm.emtgt,distance=..6] run damage @s {STAR_D} {BY}',
                           f'execute if entity @s[tag=bm.emgem] as @e[tag=bm.emtgt,distance=..6] run damage @s {STAR_GEM} {BY}',
                           f'execute as @e[{FOE},distance=..5,tag=!bm.emtgt] run damage @s {STAR_SPL} {BY}',
                           f'execute as @e[{FOE},distance=..5] run data merge entity @s {{Fire:100s,Motion:[0.0d,0.7d,0.0d]}}',
                           'tag @e[tag=bm.emtgt,distance=..8] remove bm.emtgt',
                           'particle minecraft:flash{color:[0.5,0.92,1.0,1.0]} ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:soul_fire_flame ~ ~0.5 ~ 2.5 0.4 2.5 0.12 120',
                           'particle minecraft:soul ~ ~1 ~ 2 1 2 0.05 40', 'particle minecraft:explosion ~ ~0.5 ~ 1.5 0.3 1.5 0 6',
                           'playsound minecraft:entity.generic.explode neutral @a[distance=..40] ~ ~ ~ 1 1.2',
                           'playsound minecraft:item.mace.smash_ground_heavy neutral @a[distance=..40] ~ ~ ~ 1.2 0.8'])

    # ================================================================== WINGS FOR TWO: she carries you
    # (sneak + right-click: vanilla throws you off any mount while sneak is held - she lifts you the moment you let go of it)
    fn('p130/carry/click', ['scoreboard players operation #me bm.pid = @s bm.pid',
                            'execute as @e[type=minecraft:cat,tag=bm.emmapet,distance=..8] if score @s bm.pid = #me bm.pid run tag @s add bm.emsel2',
                            'execute unless entity @e[type=minecraft:cat,tag=bm.emsel2,tag=bm.emwfs] run return run tag @e[tag=bm.emsel2] remove bm.emsel2',
                            'tag @e[tag=bm.emsel2] remove bm.emsel2', 'tag @s add bm.emlift', 'scoreboard players set @s bm.emlt 60',
                            title('@s', 'actionbar', [T('Emma: ', PINK, bold=True), T('Let go of sneak - up we go~!', SOUL)])])
    tick.append('execute as @a[tag=bm.emlift] at @s run function bm:p130/carry/wait')
    fn('p130/carry/wait', ['scoreboard players remove @s bm.emlt 1', 'execute if score @s bm.emlt matches ..0 run return run tag @s remove bm.emlift',
                           'execute if predicate bm:p20/sneaking run return 0', 'tag @s remove bm.emlift',
                           'scoreboard players operation #me bm.pid = @s bm.pid',
                           'execute as @e[type=minecraft:cat,tag=bm.emmapet,distance=..8] if score @s bm.pid = #me bm.pid run tag @s add bm.emsel2',
                           'function bm:p130/carry/start', 'tag @e[tag=bm.emsel2] remove bm.emsel2'])
    # (her ribbon, used right beside her in her Wraithfire Form - as KillerWatt's Spark beside him)
    us = G.FUNCS['p57/use']
    k = us.index('execute if entity @e[type=minecraft:cat,tag=bm.emsel2] unless predicate bm:p20/sneaking run function bm:p57/recall')
    us.insert(k, 'execute if entity @e[type=minecraft:cat,tag=bm.emsel2,tag=bm.emwfs,tag=!bm.emcar,distance=..3.5] unless predicate bm:p20/sneaking run return run function bm:p130/carry/ribbon')
    fn('p130/carry/ribbon', ['function bm:p130/carry/start', 'tag @e[tag=bm.emsel2] remove bm.emsel2'])
    fn('p130/carry/start', ['execute unless entity @e[type=minecraft:cat,tag=bm.emsel2,tag=bm.emwfs] run return run ' +
                            emsay('I can only carry you in my Wraithfire Form - turn it on in my menu!'),
                            'execute if entity @e[type=minecraft:cat,tag=bm.emsel2,tag=bm.emcar] run return 0',
                            'execute if predicate bm:p21/riding run return run ' + say('Get off your mount first.'),
                            'tp @e[type=minecraft:cat,tag=bm.emsel2,distance=5..] @s',      # (out of reach: she comes to you first)
                            'ride @s mount @e[type=minecraft:cat,tag=bm.emsel2,limit=1]',
                            'execute unless function bm:p130/carry/on_emma run return run ' + emsay('Hmm, I can\'t get a grip here - try in the open!'),
                            'tag @s add bm.emcarried', 'tag @s remove bm.emsoft',
                            'attribute @s minecraft:fall_damage_multiplier modifier remove bm:em_carry',
                            'attribute @s minecraft:fall_damage_multiplier modifier add bm:em_carry -1 add_multiplied_total',
                            'execute as @e[type=minecraft:cat,tag=bm.emsel2] at @s run function bm:p130/carry/lift',
                            title('@s', 'actionbar', [T('Emma lifts you! ', SOUL, bold=True),
                                                      T('Walk forward to fly; look up (or jump) to rise, down to sink; let go to hover. ', 'gray'), T('Sneak to land.', 'dark_gray')]),
                            'playsound minecraft:entity.phantom.flap neutral @a[distance=..16] ~ ~ ~ 1 1.2'])
    fn('p130/carry/on_emma', ['execute on vehicle if entity @s[type=minecraft:cat,tag=bm.emmapet] run return 1', 'return 0'])
    fn('p130/carry/lift', ['tag @s add bm.emcar', 'data modify entity @s Sitting set value 1b', 'data modify entity @s NoGravity set value 1b',
                           'data modify entity @s Motion[1] set value 0.42d', 'scoreboard players operation #me bm.pid = @s bm.pid', sel_parts,
                           model('armr', 'ew_armr_free'), 'tag @e[type=minecraft:item_display,tag=bm.emsel] remove bm.emsel',
                           'particle minecraft:soul_fire_flame ~ ~1 ~ 0.5 0.4 0.5 0.06 30', 'particle minecraft:end_rod ~ ~1.5 ~ 0.6 0.4 0.6 0.05 16',
                           'playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..16] ~ ~ ~ 1 1.5'])
    # every tick, carrying: KillerWatt's ethereal flight
    fn('p130/carry/tick', ['scoreboard players set #rid bm.rng 0', 'execute on passengers if entity @s[type=minecraft:player] run scoreboard players set #rid bm.rng 1',
                           'execute if score #rid bm.rng matches 0 run return run function bm:p130/carry/end',
                           'execute unless entity @s[tag=bm.emwfs] run return run function bm:p130/carry/drop',
                           'data modify entity @s Sitting set value 1b', 'data modify entity @s NoGravity set value 1b',
                           'scoreboard players set #fw bm.rng 0', 'scoreboard players set #jp bm.rng 0',
                           'execute on passengers if predicate bm:p39/forward run scoreboard players set #fw bm.rng 1',
                           'execute on passengers if predicate bm:p26/jump_key run scoreboard players set #jp bm.rng 1',
                           'execute on passengers store result score #pitch bm.rng run data get entity @s Rotation[1]',
                           'execute on passengers store result score #yaw bm.rng run data get entity @s Rotation[0] 100',
                           'execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #yaw bm.rng',
                           'execute if score #fw bm.rng matches 1 run function bm:p130/carry/drive',
                           'execute if score #fw bm.rng matches 0 run data modify entity @s Motion[0] set value 0.0d',
                           'execute if score #fw bm.rng matches 0 run data modify entity @s Motion[2] set value 0.0d',
                           'scoreboard players set #vy bm.rng 0',
                           'execute if score #pitch bm.rng matches ..-25 run scoreboard players set #vy bm.rng 1',
                           'execute if score #jp bm.rng matches 1 run scoreboard players set #vy bm.rng 1',
                           'execute if score #pitch bm.rng matches 40.. run scoreboard players set #vy bm.rng -1',
                           'execute if score #vy bm.rng matches 1 unless block ~ ~2.3 ~ #bm:grap_pass run scoreboard players set #vy bm.rng 0',
                           'execute if score #vy bm.rng matches 1 run data modify entity @s Motion[1] set value 0.24d',
                           'execute if score #vy bm.rng matches -1 run data modify entity @s Motion[1] set value -0.24d',
                           'execute if score #vy bm.rng matches 0 run data modify entity @s Motion[1] set value 0.0d',
                           'particle minecraft:soul_fire_flame ~ ~0.9 ~ 0.35 0.1 0.35 0.005 1'])
    fn('p130/carry/drive', [f'function bm:p79/pet/dir {{s:{FLY}}}',
                            'execute store result entity @s Motion[0] double 0.001 run scoreboard players get #mx bm.rng',
                            'execute store result entity @s Motion[2] double 0.001 run scoreboard players get #mz bm.rng'])
    # she lets go (you sneaked; she lost the form; she fainted or went home): her axe back, gravity back
    fn('p130/carry/end', ['tag @s remove bm.emcar', 'data modify entity @s Sitting set value 0b', 'data modify entity @s NoGravity set value 0b',
                          'scoreboard players operation #me bm.pid = @s bm.pid', sel_parts,
                          cond('execute if entity @s[tag=bm.emwl]', model('armr', 'ew_armr')),
                          cond('execute unless entity @s[tag=bm.emwl] if score @s bm.eme matches 1..', model('armr', 'ee_armr')),
                          'tag @e[type=minecraft:item_display,tag=bm.emsel] remove bm.emsel', 'scoreboard players set @s bm.ems -1'])
    fn('p130/carry/drop', ['execute on passengers run ride @s dismount', 'function bm:p130/carry/end'])
    tick += ['execute as @a[tag=bm.emcarried] unless function bm:p130/carry/on_emma run function bm:p130/carry/let_go',
             'execute as @a[tag=bm.emsoft] if predicate bm:p39/on_ground run function bm:p130/carry/landed']
    fn('p130/carry/let_go', ['tag @s remove bm.emcarried', 'tag @s add bm.emsoft',
                             'execute unless predicate bm:p39/on_ground run effect give @s minecraft:slow_falling 10 0 true',
                             'execute unless predicate bm:p39/on_ground run ' + title('@s', 'actionbar', [T('Emma lets you down gently...', SOUL)])])
    fn('p130/carry/landed', ['tag @s remove bm.emsoft', 'effect clear @s minecraft:slow_falling',
                             'attribute @s minecraft:fall_damage_multiplier modifier remove bm:em_carry'])
    # sneak + right-click her, empty-handed
    ck = G.FUNCS['p127/em/click']
    k = ck.index('advancement revoke @s only bm:p127/emma_click')
    ck.insert(k + 1, 'execute unless items entity @s weapon.mainhand * if predicate bm:p20/sneaking run return run function bm:p130/carry/click')

    # ================================================================== her menu: the form, flying, her style, her charge
    import phase28 as P28
    btn = lambda m: P28.btn(T(P57.MODES[m][0], P57.MODES[m][1], bold=True), 7300 + m, tooltip=T({1: 'Speed + Jump Boost', 2: 'Strength', 3: 'Resistance',
                                                                                                4: 'Regeneration + quick heals', 5: 'Haste: dig and chop faster'}[m], 'gray'), width=120)
    sty = lambda s: P28.btn([T('Style: ', 'gray'), T(STYLES[s]['name'], STYLES[s]['col'], bold=True)], C_STYLE + s - 1, tooltip=T(STYLES[s]['tip'], 'gray'), width=120)
    dlg = P28.multi([T("Emma's Ribbon", PINK, bold=True), T('  ·  the Wraithfire Heart', SOUL)],
                    [P28.body([T('Buff: ', 'gray'), T('$(mode)', 'white', bold=True), T('     Wraithfire Form: ', 'gray'), T('$(st)', SOUL, bold=True)]),
                     P28.body([T('Battle style: ', 'gray'), T('$(sty)', SOUL, bold=True), T('     Wraithfire charge: ', 'gray'), T('$(ch)%', 'white', bold=True)]),
                     P28.body([T('Wraithfire Form on: she stays ethereal and fights hard - soul crescents, lances, a ward round you, ', 'gray'),
                               T('charged attacks', SOUL), T(' - and can carry you (her ribbon beside her, or sneak + right-click her). Off: she\'s her usual self. ', 'gray'),
                               T('(In the heist lobby she\'s always her usual self.)', 'dark_gray')], 320)],
                    [btn(1), btn(2), btn(3), btn(4), btn(5), P28.btn(T('Wardrobe', '#ff8ad8', bold=True), 7306, tooltip=T('Her ribbons, dresses and outfits', 'gray'), width=120),
                     P28.btn(T('Wraithfire Form: on / off', SOUL, bold=True), 7307, tooltip=T('Her Wraithfire Form - or her usual self.', 'gray'), width=120),
                     P28.btn(T('Fly with me', SOUL, bold=True), C_FLY, tooltip=T('She lifts you from behind and flies you. Sneak to land.', 'gray'), width=120),
                     sty(1), sty(2), sty(3),
                     P28.btn(T('Take back the heart', '#9ad8ff'), 7308, tooltip=T('She gives the Wraithfire Heart back to you.', 'gray'), width=120),
                     P28.btn(T('Send her home', 'gray'), 7309, width=120)], columns=2, exit_label='Close')
    G.FUNCS['p127/em/menu_show'] = [f'$dialog show @s {snbt(dlg)}']
    mn = G.FUNCS['p57/menu']
    k = mn.index('execute if score @s bm.emwf matches 1 run return run function bm:p127/em/menu_show with storage bm:tmp em')
    mn[k:k] = ['data modify storage bm:tmp em.sty set value "Huntress"'] + \
              [f'execute if score @s bm.emsty matches {s} run data modify storage bm:tmp em.sty set value "{c["name"]}"' for s, c in STYLES.items()] + \
              ['data modify storage bm:tmp em.ch set value 0',
               'execute if score @e[type=minecraft:cat,tag=bm.emsel2,limit=1] bm.emwc matches 0.. store result storage bm:tmp em.ch int 1 run scoreboard players get @e[type=minecraft:cat,tag=bm.emsel2,limit=1] bm.emwc']
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {C_FLY}..{C_STYLE + 2} run return run function bm:p57/act')
    ea = G.FUNCS['p57/act']
    k = ea.index('tag @e[tag=bm.emsel2] remove bm.emsel2')
    ea[k:k] = [f'execute if score #act bm.pay matches {C_FLY} run function bm:p130/menu_fly'] + \
              [f'execute if score #act bm.pay matches {C_STYLE + s - 1} run function bm:p130/style {{s:{s}}}' for s in STYLES]
    fn('p130/menu_fly', ['execute unless score @s bm.emwf matches 1 run return run function bm:p28/stale', 'function bm:p130/carry/start'])
    fn('p130/style', ['execute unless score @s bm.emwf matches 1 run return run function bm:p28/stale', '$scoreboard players set @s bm.emsty $(s)'] +
       [f'execute if score @s bm.emsty matches {s} run ' + emsay({1: 'Guardian - nothing gets near you. I\'ve got your back!',
                                                                  2: 'Huntress - I\'ll take them down before they reach us.',
                                                                  3: 'Tempest - let\'s blow them all away~!'}[s]) for s in STYLES] +
       ['playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1.5', 'function bm:p57/menu'])
    # the form's own words
    tg = G.FUNCS['p127/em/toggle']
    for i, l in enumerate(tg):
        tg[i] = l.replace("Okay! I'll stay like this - shining, just for you~", 'Wraithfire Form - on! Watch this~').replace(
            "Not here - the heart won't burn in the vault. Back home, though~!", "Not here - the heart won't burn in the vault. Back home, though~!")
    of = G.FUNCS['p127/em/off']
    for i, l in enumerate(of):
        of[i] = l.replace('Phew - okay, back to plain old me! Tell me when you want me shining again.', 'Wraithfire Form - off. Back to plain old me! Just say when~')
    of.insert(1, 'execute as @e[type=minecraft:cat,tag=bm.emsel2,tag=bm.emcar] run function bm:p130/carry/drop')
    G.FUNCS['p127/em/take'].insert(1, 'execute as @e[type=minecraft:cat,tag=bm.emsel2,tag=bm.emcar] run function bm:p130/carry/drop')
    # (only her own rider: another player's Emma flying close by keeps hers)
    G.FUNCS['p57/dismiss'].insert(0, 'execute as @e[type=minecraft:cat,tag=bm.emsel2,tag=bm.emcar] run function bm:p130/carry/drop')
    G.FUNCS['p57/fade'][0:0] = ['execute as @e[type=minecraft:cat,tag=bm.emmapet,tag=bm.emcar,distance=..2] if score @s bm.pid = #me bm.pid run function bm:p130/carry/drop',
                                # (she fainted: her host is dying - no selector finds it, and it would hold you a second
                                #  longer - so you're let go now, with her rig; the tick's let_go lets you down gently)
                                'execute as @a[tag=bm.emcarried] if score @s bm.pid = #me bm.pid run ride @s dismount']
    # (and she lets go the moment she faints - as she sinks, dazed - not a second later, when her burst comes)
    assert 'p125/faint/emma' in G.FUNCS
    G.FUNCS['p125/faint/emma'].insert(0, 'execute as @a[tag=bm.emcarried] if score @s bm.pid = #me bm.pid run ride @s dismount')

    G.FUNCS['tick'] += tick
    s_ = G.FUNCS['loop/second']
    s_[-1:-1] = second


# ===================================================================== resource pack: the wraith-forged armour, wings and blade
def _wraith(img, kind):
    """re-cast one of her ethereal textures in soul fire: dark steel lit cyan, white feathers frosted blue, a glowing blade"""
    import colorsys
    from PIL import Image
    out = Image.new('RGBA', img.size)
    ramp = [(0.0, (6, 12, 20)), (0.35, (20, 44, 64)), (0.62, (36, 96, 130)), (0.82, (70, 200, 240)), (1.0, (200, 250, 255))]
    def grad(t, stops):
        t = max(0.0, min(1.0, t))
        for (a, ca), (b, cb) in zip(stops, stops[1:]):
            if t <= b:
                u = (t - a) / (b - a) if b > a else 0
                return tuple(int(ca[i] + (cb[i] - ca[i]) * u) for i in range(3))
        return stops[-1][1]
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b, a = img.getpixel((x, y))
            if a == 0: out.putpixel((x, y), (0, 0, 0, 0)); continue
            h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            if kind == 'feather':
                c = grad(0.55 + 0.45 * l, [(0.55, (90, 190, 230)), (0.8, (170, 232, 255)), (1.0, (236, 252, 255))])
            elif kind == 'blade':
                c = grad(l, [(0.0, (10, 120, 180)), (0.6, (58, 220, 255)), (1.0, (232, 255, 255))])
            elif s > 0.35 and (h > 0.78 or h < 0.06):                    # (her magenta trim and star gems: soul cyan)
                c = grad(0.55 + 0.45 * l, [(0.55, (14, 140, 196)), (0.8, (58, 220, 255)), (1.0, (210, 252, 255))])
            elif s > 0.3 and 0.45 <= h <= 0.6 and l > 0.5:               # (the light-blue teardrop: a cold glow)
                c = grad(l, [(0.5, (60, 210, 250)), (1.0, (230, 255, 255))])
            else:
                c = grad(l * 0.9, ramp)
            out.putpixel((x, y), c + (a,))
    return out


def textures():
    T_ = EA.textures()
    kinds = {'ee_feather': 'feather', 'ee_down': 'feather', 'ee_blade': 'blade'}
    return {'ew' + k[2:]: _wraith(v, kinds.get(k, 'armour')) for k, v in T_.items() if k.startswith('ee_') and k != 'ee_face'}


def rp(R):
    import sys, copy
    R.TEXTURE_MODS.append(sys.modules[__name__])
    M = EA.models()
    glow = {'ee_blade', 'ee_feather', 'ee_down', 'ee_magenta'}
    def recast(tex, els):
        tex2 = {k: (v.replace('bm:block/ee_', 'bm:block/ew_') if k != 'ee_face' else v) for k, v in tex.items()}
        tex2 = {('ew' + k[2:] if k.startswith('ee_') and k != 'ee_face' else k): v for k, v in tex2.items()}
        els2 = []
        for e in copy.deepcopy(els):
            for f in e['faces'].values():
                t = f['texture'][1:]
                if t.startswith('ee_') and t != 'ee_face': f['texture'] = '#ew' + t[2:]
            if any(f['texture'][1:].replace('ew_', 'ee_') in glow for f in e['faces'].values()): e['light_emission'] = 12
            els2.append(e)
        return tex2, els2
    for p in WPARTS + WINGS:
        tex, els = M[f'ee_{p}']
        R.HATS[f'ew_{p}'] = recast(tex, els)
    # (carrying you: her right hand free - the arm without the axe, a thumb out like her left)
    tex, els = M['ee_armr']
    cx = EA.PIVOT['armr'][0]
    free = copy.deepcopy(els[:5]) + [EA._el((cx - 1.5, 13.4, -0.6), (cx - 0.6, 14.6, 0.2), 'ee_glove', EA.PIVOT['armr'])]
    used = sorted({f['texture'][1:] for e in free for f in e['faces'].values()})
    R.HATS['ew_armr_free'] = recast({k: tex.get(k, f'bm:block/{k}') for k in used}, free)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + ('ew_',)

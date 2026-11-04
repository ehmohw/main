"""3.1: THE GLITCH - the 53rd follower (glitch_pet_art.py draws it; fol5flag.GLITCH). Three sprites on one screen were more than
the old cartridge could draw: with 8-Bit Cecil, 8-Bit Leo and 8-Bit Emma all out at once, use a Glitched Cartridge anyway - the
screen tears and the leftover pixels climb out as a creature of their own. "H3LL0 PL4YER 0NE." Right-click it: it hands you
A CRACKED CARTRIDGE (its summoning item) and comes along.

HOW IT MOVES  (glitch_pet_art.MOTION, played tick by tick: p264/m/<clip>) - never smooth. Every pose SNAPS (interpolation 0);
             frames are held, doubled and DROPPED; on 'lag' frames the slices desync (the head and fists now, sl3 a tick late,
             sl2 two, sl1 and the trail three); an RGB split (a red and a cyan copy of the head and slices, a hair to either side,
             for 2 ticks) and ghost afterimages (left behind, fading over 4 ticks). On top: every tick, one slice in six jumps a
             hair sideways for a tick (a quarter as often while it sits); its body's ground motion lands in 2-tick steps; about
             one walk or fight in six ends in a REWIND (REW on its screen, the last frames played backwards, a step back and
             forward again); every 20-40 s its whole palette flickers to DMG green, Virtual Red or INVERTED for a few ticks. The
             one smooth thing it does is sit down (eased, like a sigh) - and sitting, its slices only fizz.
ITS WAYS      PUNCH (a foe within reach: both voxel fists, 6); TELEPORT-STUTTER (a foe 2.6-6 off, every 5 s: three jittery
             blinks to it and a double-fist punch, 8); CORRUPT (a foe within 7, every 12 s: an ERR cage snaps round it for 3 s -
             Weakness II and Slowness II); SEGFAULT (charged, every minute: it tears itself apart - 10 to every monster within 3,
             thrown back - then rewinds itself together).
EVERYTHING ELSE is every follower's: sitting (right-click: a happy heap of pixels; sneak + right-click: it dozes, dreaming in
snow), a wardrobe (its CRT Bezel: Beige 1989, Clear Purple, Atomic Teal - and the metals), a rare aura (the Dead Pixel Halo), a
shiny (Clean Signal: gold and pearl - its afterimages gold), the Partner Wheel, a frame (its cartridge flicks through the
channels), a display case, Cecil's doll, the honours, a Raid Contract; pairs with Bender, Mr. Capshun, Henry and Nia."""
from items import item, T, TOTEM
from useitem import hold
from nbt import snbt, F, Int, B
import fol5
import fol5art
import fol5wire as W5
import rigpet as RP
import rigface as RF2
import rigfol as RF
import phase235 as P235

S5 = fol5.SPEC['glitch']
A0 = fol5art.get('glitch')
COL, LINE = S5['COL'], S5['LINE']
ITEM = S5['item']
CYAN = '#3cf0ff'

item(ITEM, TOTEM, 'A Cracked Cartridge', COL,
     ['A grey cartridge, cracked across the label. The', 'picture on it keeps tearing into coloured lines.',
      ('Use: call the Glitch (again: call it over).', 'blue'), ('Sneak + use: its menu.', 'blue'),
      ('Teleport-stutter, Corrupt and SEGFAULT.', 'blue'), ('If it faints: 2 minutes before it can return.', 'gray'), ('"H3LL0 PL4YER 0NE"', 'dark_gray')],
     model=f'bm:{ITEM}', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)


class Glitch(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'glitch', 'The Glitch', COL, LINE, 'p264', 'gx', 'gz'
    A = RF2.art(A0)
    MENU, PET_HP, PET_CD, ITEM = 5700, 34, 120, ITEM
    pron, they = 'it', 'it'
    EXPR = RP.Cfg.EXPR + ('snow', 'rew', 'err')
    FACE = dict(A0.FACE_MAP, snow='snow', rew='rew', err='err')
    ATTRS = dict(armor=4, attack_damage=4, movement_speed=0.36, follow_range=32, step_height=1.1)
    SCALE, HIT = 0.8, W5.hit(A0)
    CYCLE = W5.cycle(A0, (80, [(0, 'idle_a'), (40, 'idle_b')]), (120, [(0, 'sit_a'), (60, 'sit_a2')]), (None, [(0, 'happy'), (10, 'idle_a')]),
                       {7: (None, [(0, 'strike')]), 8: (None, [(0, 'stutter_0')]), 11: (None, [(0, 'corrupt_h')]), 12: (None, [(0, 'segfault')])})
    DUR = dict(P235._DUR, sit_a=6, sit_a2=8, sit_b=6, sit_b2=8, strike=0, stutter_0=0, corrupt_h=0, segfault=0, happy=0, idle_a=0, idle_b=0)
    QUIPS = ['"H3LL0 PL4YER 0NE. ...H3LL0 PL4YER 0NE."', '"%%THANK Y0U%% for playing!!"', '(its screen shows a little heart. Then the heart tears in half. Then it\'s fine again.)',
             '"1 AM N0T A BUG. 1 AM A F3ATURE."', '(it rewinds the last two seconds, watches them again, and seems pleased)', '"PRESS START. PRESS START. PRESS ST-"']
    HELLO = ('(the Glitch skips three frames and is suddenly beside you)', '(the air tears into coloured lines - and the Glitch drops out of them) "R3ADY PL4YER 0NE!"',
             '(it rewinds itself out of existence, waving)')
    SIT = ('"C0NT1NU3?" (it shakes itself back together)', '(it settles into a happy little heap of pixels, fists either side)')
    FAINT = '"G4ME... 0VER..."'
    NOT_YOURS = '"ERR0R: PL4YER N0T F0UND." (it looks you over) "...y0u\'re n0t mine."'
    POWERS = [('Punch', 'a foe within reach: both voxel fists, 6'),
              ('Teleport-Stutter', 'a foe 2.6-6 off, every 5 s: three jittery blinks to it, an afterimage left at each, and a double-fist punch - 8'),
              ('Corrupt', 'a foe within 7, every 12 s: an ERR cage snaps round it for 3 s - Weakness II and Slowness II'),
              ('SEGFAULT', 'charged, every minute: it tears itself apart - 10 to every monster within 3, thrown back - then rewinds itself together'),
              ('Never Smooth', 'it stutter-steps, drops frames, desyncs and now and then rewinds - only sitting down is smooth')]
    INTRO = [T('The Glitch', COL, bold=True), T(' - the pixels left over when three 8-bit heroes shared one old cartridge. ', 'gray'),
             T('"H3LL0 PL4YER 0NE."', LINE, italic=True)]
    BURST = ['particle minecraft:electric_spark ~ ~0.8 ~ 0.4 0.5 0.4 0.3 20', 'particle minecraft:dust{color:[1.0,0.24,0.78],scale:1.2} ~ ~0.8 ~ 0.4 0.5 0.4 0 14',
             'particle minecraft:dust{color:[0.24,0.94,1.0],scale:1.2} ~ ~0.8 ~ 0.4 0.5 0.4 0 14']
    FADE_SOUND = 'playsound minecraft:block.note_block.bit neutral @a[distance=..20] ~ ~ ~ 1 0.5'
    SUMMON_EXTRA = ['playsound minecraft:block.note_block.bit neutral @a[distance=..24] ~ ~ ~ 0.8 1.6', 'playsound minecraft:block.note_block.bit neutral @a[distance=..24] ~ ~ ~ 0.8 0.7']
    ENC_POSES = [(0, 'idle_a'), (30, 'segfault'), (36, 'idle_b'), (60, 'happy')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 30 run particle minecraft:electric_spark ~ ~0.8 ~ 0.4 0.4 0.4 0.3 12'
    ADV = ('H3LL0 PL4YER 0NE', 'Use a Glitched Cartridge with 8-Bit Cecil, Leo and Emma all out - and meet what tears out of the screen')
    ADMIN_HINT = 'With 8-Bit Cecil, 8-Bit Leo and 8-Bit Emma all out, use a Glitched Cartridge: the screen tears and it climbs out.'
    MEET_HINT = 'Right-click it.'


A0.POSES['corrupt_h'] = {k: v for k, v in A0.POSES['corrupt'].items() if k != '_show'}       # (its cage goes round the FOE: p264/cage)
from fol5_kit import T as _T
A0.POSES['sit_a2'] = dict(A0.POSES['sit_a'], head=_T(0, 0, -5))                                # (seated, a little sway: its head tips, and back)
A0.POSES['sit_b2'] = dict(A0.POSES['sit_b'], head=_T(8, 0, 12), _face='snow')                # (dozing - and dreaming in snow)
_DOLL = 'A doll of the Glitch - a chunky little CRT with a torn corner, pixel eyes, and three slices of sprite for a body.'
_eff = W5.pair_fx
_PAIRS = {
    'gx_bender': ('glitch', 'bender', 'Good B0Y.exe', '#e0a860', 'The Glitch and Bender - he barks at its afterimages, and it copies him back',
                  _eff(('speed', 0), ('strength', 0)),
                  [('bender', '(barks at an afterimage. Chases it. It was never there.)'), ('glitch', '"G00D B0Y.exe. G00D B0Y.exe. G00D B0Y.exe."')],
                  [('glitch', '(a cyan ghost of Bender flickers up beside the real one)', 'bender', '(barks at himself, overjoyed)')]),
    'gx_capshun': ('glitch', 'capshun', 'Patch Notes', '#f0f0f0', 'The Glitch and Mr. Capshun - he keeps trying to draw it, and it keeps glitching off the page',
                   _eff(('strength', 0), ('haste', 0)),
                   [('capshun', '[Mr. Capshun narrates: "Hold STILL. He painted over its tear, very carefully."]'), ('glitch', '"...1 FEEL SM00TH. 1s this what s0lid feels like?"')],
                   [('glitch', '(slides clean off the page)', 'capshun', '[Mr. Capshun narrates: "It was, he decided, a very modern drawing."]')]),
}
W5.register(Glitch, A0, _DOLL, ('minecraft:electric_spark', 'minecraft:block.note_block.bit', 'minecraft:poof'), _PAIRS, 'the Glitch')

# (its clips' parts, by how late they take a 'lag' frame)
LAGGRP = {0: ('head', 'chunk', 'shards', 'fistr', 'fistl', 'err', 'core'), 1: ('sl3',), 2: ('sl2',), 3: ('sl1', 'trail')}
SHOWN = ('head', 'chunk', 'shards', 'sl1', 'sl2', 'sl3', 'fistr', 'fistl', 'trail')       # (the parts an afterimage copies)
RGBP = ('head', 'sl1', 'sl2', 'sl3')
FRAMES = ['glitch_rom_f0', 'glitch_rom_f1', 'glitch_rom_f2', 'glitch_rom_f3']


def extend_offers(O, offer):
    pass


def generate_early(G):
    RP.contract(Glitch, G)


# ---------------------------------------------------------------------------------------------------- the icons
def _icon(screen=None):
    """A Cracked Cartridge: a grey cartridge, a crack across its label; the label a little telly - its channel `screen`"""
    from sprites280 import S
    s = S()
    pal = {'k': '#2a2a32', 'g': '#7a7a86', 'l': '#a2a2ae', 'd': '#55555f', 'c': '#d8c070'}
    s.g(['..kkkkkkkkkkk..', '.kglllllllllgk.', '.kgdddddddddgk.', '.kgd.......dgk.', '.kgd.......dgk.', '.kgd.......dgk.', '.kgd.......dgk.',
         '.kgd.......dgk.', '.kgdddddddddgk.', '.kgggggggggggk.', '.kggkggggkggggk', '.kgggggggggggk.', '.kgcgcgcgcgcgk.', '.kkkkkkkkkkkkk.'], pal, 0, 1)
    scr = {None: ['#0a0a14'] * 35, 'snow': None, 'err': None, 'happy': None}
    import random
    r = random.Random(7)
    for y in range(5):
        for x in range(7):
            if screen == 'snow':
                c = r.choice(('#e8e8f0', '#9a9aa8', '#3a3a48', '#ffffff'))
            elif screen == 'err':
                c = '#ff3040' if (x, y) in ((1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (4, 1), (4, 2), (4, 3), (5, 1), (5, 2)) else '#1a0006'
            elif screen == 'happy':
                c = '#9ffcff' if (x, y) in ((1, 1), (2, 2), (0, 2), (5, 1), (4, 2), (6, 2), (2, 4), (3, 4), (4, 4)) else '#0a0a14'
            else:
                c = '#3cf0ff' if (x, y) in ((1, 1), (5, 1)) else ('#ff3cc8' if (x, y) in ((2, 3), (3, 3), (4, 3)) else '#0a0a14')
            s.px(4 + x, 4 + y, c)
    for x, y in ((9, 2), (10, 3), (10, 4), (11, 5), (12, 6)):
        s.px(x, y, '#ff3cc8')                                         # (the crack, glowing magenta along it)
    return s.render()


def rp(R):
    W5.rp(Glitch, R, _icon(), A0)
    for i, f in enumerate((None, 'snow', 'err', 'happy')):
        R.ICONS[FRAMES[i]] = _icon(f)


def textures():
    return A0.textures()


# ---------------------------------------------------------------------------------------------------- its ways
def _abilities(G, X):
    fn, pfx, foe, me, S = G.fn, X.pfx, X.foe, X.me, X.S
    snd = lambda s, v=0.6, p=1.0: f'playsound minecraft:{s} neutral @a[distance=..16] ~ ~ ~ {v} {p}'
    K = dict(melee=dict(st=7, x=8, at=4, cd=20, reach=2.6, face='serious', go=[snd('block.note_block.bit', 0.5, 1.4)]),
             ranged=dict(st=8, x=12, at=6, cd=100, near=2.6, far=6, face='serious', go=[snd('block.note_block.bit', 0.7, 0.6)]),
             crowd=dict(st=11, x=20, at=17, cd=240, r=7, n=1, face='err', go=[snd('block.note_block.bit', 0.7, 0.5)]),
             charged=dict(st=12, x=16, at=11, cd=1200, r=3, face='snow', go=[snd('block.respawn_anchor.deplete', 0.6, 1.8)]))
    lines = P235.kit(G, X, K)
    P235.melee(G, X, 6, 2.6, ['particle minecraft:electric_spark ~ ~0.8 ~ 0.2 0.2 0.2 0.2 8', 'particle minecraft:dust{color:[1.0,0.24,0.78],scale:1.0} ~ ~0.8 ~ 0.3 0.3 0.3 0 6'],
               'minecraft:block.note_block.bit')
    # TELEPORT-STUTTER: the blinks are its clip's (p264/blink); the double-fist punch lands on whatever is in reach after them
    fn(f'{pfx}/ranged', X.hit(8) + [f'execute as @e[{foe},distance=..3.2,sort=nearest,limit=1] at @s run function bm:{pfx}/meleed',
                                    'particle minecraft:electric_spark ~ ~0.8 ~ 0.4 0.4 0.4 0.4 16'] + X.end)
    fn(f'{pfx}/blink', [f'execute if entity @e[{foe},distance=..1.8] run return 0',
                        f'execute facing entity @e[{foe},distance=..9,sort=nearest,limit=1] feet rotated ~ 0 positioned ^ ^ ^1.6 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~ ~',
                        'particle minecraft:electric_spark ~ ~0.6 ~ 0.2 0.3 0.2 0.2 6', snd('block.note_block.bit', 0.4, 1.9)])
    # CORRUPT: an ERR cage round the nearest foe - snapping round a quarter turn every 4 ticks for 3 s; Weakness II, Slowness II
    cage = {'Tags': ['bm.gxcage', 'bm.gxcn'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:gl_err'}},
            'item_display': 'fixed', 'teleport_duration': Int(0), 'brightness': {'block': Int(15), 'sky': Int(15)},
            'transformation': {'left_rotation': RF.IDENT, 'right_rotation': RF.IDENT, 'translation': [F(0), F(0.1), F(0.48)], 'scale': [F(1.6)] * 3}}
    fn(f'{pfx}/crowd', X.hit(3) + [f'execute as @e[{foe},distance=..7.5,sort=nearest,limit=1] at @s run function bm:{pfx}/caged'] + X.end)
    fn(f'{pfx}/caged', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:weakness 3 1', 'effect give @s minecraft:slowness 3 1',
                        f'summon minecraft:item_display ~ ~0.5 ~ {snbt(cage)}', 'scoreboard players set @e[type=minecraft:item_display,tag=bm.gxcn] bm.gzcg 60',
                        'tag @e[type=minecraft:item_display,tag=bm.gxcn] remove bm.gxcn',
                        'particle minecraft:dust{color:[1.0,0.19,0.25],scale:1.2} ~ ~1 ~ 0.4 0.6 0.4 0 20', snd('block.note_block.bit', 1, 0.5)])
    X.tick += ['execute as @e[type=minecraft:item_display,tag=bm.gxcage] at @s run function bm:p264/cage']
    fn('p264/cage', ['scoreboard players remove @s bm.gzcg 1', 'execute if score @s bm.gzcg matches ..0 run return run kill @s',
                     'execute store result score #c bm.rng run scoreboard players get @s bm.gzcg', 'scoreboard players operation #c bm.rng %= #4 bm.rng',
                     'execute if score #c bm.rng matches 0 run tp @s ~ ~ ~ ~90 0'])
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.gzcg dummy', 'scoreboard players set #4 bm.rng 4', 'scoreboard players set #2 bm.rng 2']
    G.OBJECTIVES.append('bm.gzcg')
    # SEGFAULT: torn apart - 10 to every monster within 3, thrown back
    fn(f'{pfx}/charged', X.hit(10) + [f'execute as @e[{foe},distance=..3.2] at @s run function bm:{pfx}/torn',
                                      'particle minecraft:electric_spark ~ ~0.8 ~ 1.4 0.8 1.4 0.6 60',
                                      'particle minecraft:dust{color:[1.0,0.24,0.78],scale:1.6} ~ ~0.8 ~ 1.4 0.8 1.4 0 30',
                                      'particle minecraft:dust{color:[0.24,0.94,1.0],scale:1.6} ~ ~0.8 ~ 1.4 0.8 1.4 0 30',
                                      snd('entity.generic.explode', 0.4, 1.9), snd('block.note_block.bit', 1, 0.5)] + X.end)
    fn(f'{pfx}/torn', [f'function bm:{pfx}/hurt', f'execute facing entity @e[type=minecraft:wolf,tag={me},limit=1] feet rotated ~180 0 if block ^ ^ ^1.5 #bm:grap_pass if block ^ ^1 ^1.5 #bm:grap_pass run tp @s ^ ^ ^1.5'])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[tag=bm.gxcage]', 'kill @e[tag=bm.gxfx]']
    return lines


def _encounter(G, X):
    """a Glitched Cartridge used with all three of your 8-bit heroes near: the screen tears, and it climbs out"""
    fn, tellraw, title = G.fn, G.tellraw, G.title
    pets = [('bm.xmpet', '8-Bit Emma'), ('bm.xlpet', '8-Bit Leo'), ('bm.xcpet', '8-Bit Cecil')]
    fn('p264/enc/trio', ['scoreboard players set #tr bm.rng 0'] +
       [f'execute if entity @e[type=minecraft:wolf,tag={t},distance=..16] as @e[type=minecraft:wolf,tag={t},distance=..16] if score @s bm.pid = #me bm.pid run scoreboard players add #tr bm.rng 1' for t, _n in pets] +
       ['execute if score #tr bm.rng matches 3.. run return 1', 'return 0'])
    U = G.FUNCS['p214/use']
    k = U.index('scoreboard players set #done bm.rng 0')
    U.insert(k + 1, 'execute unless entity @s[tag=bm.gxmet] if function bm:p264/enc/trio run function bm:p264/enc/cart')
    fn('p264/enc/cart', ['scoreboard players set #done bm.rng 1',
                         'execute if entity @e[type=minecraft:interaction,tag=bm.gxenc,distance=..32] run return run ' + title('@s', 'actionbar', T('The screen tears again - the Glitch is already out, nearby.', COL)),
                         'clear @s *[minecraft:custom_data~{bm:"glitch_cart"}] 1',
                         'execute positioned ^ ^ ^2 run function bm:p264/enc/place',
                         'particle minecraft:electric_spark ^ ^1 ^2 0.6 0.8 0.6 0.4 60', 'playsound minecraft:block.note_block.bit player @a[distance=..16] ~ ~ ~ 1 0.5',
                         'playsound minecraft:block.respawn_anchor.deplete player @a[distance=..16] ~ ~ ~ 0.8 1.6',
                         tellraw('@a[distance=..16]', [T('Three sprites on one screen is more than the old cartridge can draw. The picture tears into coloured lines - ', '#c8c8ff', italic=True),
                                                       T('and the leftover pixels climb out, blinking. ', 'gray', italic=True), T('"H3LL0 PL4YER 0NE."', LINE)])])
    fn('p264/enc/place', ['execute if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass unless block ~ ~-1 ~ #bm:grap_pass run return run function bm:p264/enc/spawn',
                          'execute positioned ~ ~1 ~ if block ~ ~ ~ #bm:grap_pass run return run function bm:p264/enc/spawn',
                          'function bm:p264/enc/spawn'])
    csay = lambda txt: title('@s', 'actionbar', [T('The Glitch: ', COL, bold=True), T(txt, LINE)])
    fn('p264/enc/talk', [f'execute if items entity @s container.* {X.holds(ITEM)} run return run ' + csay('"Y0U ALR3ADY H4VE M3. Y0U CAN\'T H4VE TW0. ...can y0u?"'),
                         f'execute as {X.here} at @s run particle minecraft:electric_spark ~ ~1 ~ 0.4 0.5 0.4 0.3 20', 'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.8',
                         tellraw('@s', [T('It rewinds itself three times to be sure it heard you right - then pulls a cracked cartridge out of its screen and hands it over. ', '#c8c8ff', italic=True),
                                        T('"%%THANK Y0U%%. PL4YER 0NE. I AM C0MING."', LINE)]),
                         'function bm:p264/enc/joined'])


# ---------------------------------------------------------------------------------------------------- how it moves: MOTION
def _motion(G, C):
    """rigpet's animation (its cycles: sitting, swimming, riding) kept as p264/anim0; p264/anim plays the MOTION clips over it"""
    fn, pfx, ab = G.fn, C.pfx, C.ab
    S = lambda s: f'bm.{C.q}{s}'
    import phase95 as FX
    import shiny as SH
    A, SP = C.A, A0.RIG_SCALE
    sel = f'bm.{ab}sel'
    psel = lambda p=None: f'@e[type=minecraft:item_display,tag={sel}' + (f',tag=bm.{ab}p_{p}]' if p else ']')
    objs = [S('ps'), S('rw'), S('hu'), S('pt'), S('pd'), S('fl')]
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    G.FUNCS[f'{pfx}/anim0'] = G.FUNCS.pop(f'{pfx}/anim')
    made = set()

    def mp(pose, grp, dur):
        """a pose put on one lag group (or all), snapped (dur 0) or eased"""
        n = f'{pfx}/mp/{pose}_{grp}_{dur}'
        if n not in made:
            made.add(n)
            parts = [p for p in A.PARTS if grp == 'all' or p in LAGGRP[grp]]
            fn(n, RF.pose(A, A.POSES[pose], SP, dur, psel, swap=C.SWAP, keep=True, parts=parts))
        return f'function bm:{n}'
    MOOD = {'focus': 'serious', 'snow': 'snow', 'rew': 'rew', 'err': 'err', 'happy': 'happy', 'blink': 'blink', 'hurt': 'hurt', 'surprised': 'surprised'}

    def compile_clip(frames, period=None):
        ev, t = {}, 0
        add = lambda tt, l: ev.setdefault(tt % period if period else tt, []).append(l)
        for fr in frames:
            pose, ticks, how = fr[0], fr[1], fr[2]
            ex = fr[3:] if len(fr) > 3 else ()
            if how in ('snap', 'ease'):
                dur = ticks if how == 'ease' else 0
                if 'lag' in ex:
                    for d in LAGGRP:                     # (lag group d: its parts take the frame d ticks late)
                        add(t + d, mp(pose, d, dur))
                else:
                    add(t, mp(pose, 'all', dur))
                f = A0.POSES[pose].get('_face')
                if f and f in MOOD:
                    for l in FX.face_cmd(C.W, MOOD[f], max(2, ticks)):
                        add(t, l)
            if 'rgb' in ex:
                add(t, f'function bm:{pfx}/fx/rgb')
            if 'ghost' in ex:
                add(t, f'function bm:{pfx}/fx/ghost')
            t += ticks
        return ev, (period or t)

    def clip(name, frames, loop=True, extra=None):
        ev, per = compile_clip(frames, None)
        if loop:
            ev, per = compile_clip(frames, per)
        for tt, ls in (extra or {}).items():
            ev.setdefault(tt, []).extend(ls)
        lines = [f'scoreboard players operation #f bm.rng = @s {S("fr")}']
        if loop:
            lines.append(f'scoreboard players operation #f bm.rng %= #{per} bm.rng')
            G.FUNCS['load'][-1:-1] = [f'scoreboard players set #{per} bm.rng {per}']
        for tt in sorted(ev):
            fn(f'{pfx}/m/{name}/{tt}', ev[tt])
            lines.append(f'execute if score #f bm.rng matches {tt} run function bm:{pfx}/m/{name}/{tt}')
        fn(f'{pfx}/m/{name}', lines)
    M = A0.MOTION
    clip('idle', M['idle'])
    clip('walk', M['walk'])
    clip('run', M['run'])
    blink = [f'function bm:{pfx}/blink']
    clip('stutter', M['stutter'], loop=False, extra={0: blink, 2: blink, 4: blink})
    clip('corrupt', M['corrupt'], loop=False)
    clip('segfault', M['segfault'], loop=False)
    clip('strike', [('strike', 3, 'snap', 'rgb'), ('idle_a', 2, 'snap', 'lag')], loop=False)
    clip('happy', [('happy', 4, 'snap', 'rgb'), ('happy', 6, 'hold'), ('idle_a', 1, 'snap', 'lag')], loop=False)
    # (the overlays: hurt, and the REWIND - each counts down its own score; while it runs, the clip under it waits)
    for name, frames, sc in (('hurt', M['hurt'], 'hu'), ('rewind', [('rew', 1, 'snap', 'rgb'), ('walk_2', 1, 'snap'), ('walk_0', 1, 'snap'), ('rew', 1, 'snap'),
                                                                    ('idle_a', 1, 'snap', 'lag')], 'rw')):
        ev, per = compile_clip(frames)
        per = max(per, max(ev) + 1)                        # (its late slices land before it lets go)
        if name == 'rewind':
            ev.setdefault(0, []).append('execute rotated ~ 0 if block ^ ^ ^-0.3 #bm:grap_pass run tp @s ^ ^ ^-0.3')
            ev.setdefault(3, []).append('execute rotated ~ 0 if block ^ ^ ^0.3 #bm:grap_pass run tp @s ^ ^ ^0.3')
        lines = [f'scoreboard players remove @s {S(sc)} 1', f'scoreboard players set #f bm.rng {per}', f'scoreboard players operation #f bm.rng -= @s {S(sc)}',
                 'scoreboard players remove #f bm.rng 1']
        for tt in sorted(ev):
            fn(f'{pfx}/m/{name}/{tt}', ev[tt])
            lines.append(f'execute if score #f bm.rng matches {tt} run function bm:{pfx}/m/{name}/{tt}')
        fn(f'{pfx}/m/{name}', lines)
        LEN = per
        if name == 'hurt':
            HLEN = LEN
        else:
            RLEN = LEN
    fn(f'{pfx}/anim', [f'execute unless score @s {S("ps")} = @s {S("s")} run function bm:{pfx}/m/changed',
                       f'execute if score @s {S("s")} matches 4 run return run function bm:{pfx}/anim0',
                       f'execute if score @s {S("s")} matches 16..17 run return run function bm:{pfx}/anim0',
                       f'execute unless score @s {S("hu")} matches 1.. if data entity @s {{HurtTime:10s}} run scoreboard players set @s {S("hu")} {HLEN}',
                       f'execute if score @s {S("hu")} matches 1.. run return run function bm:{pfx}/m/hurt',
                       f'execute if score @s {S("rw")} matches 1.. run return run function bm:{pfx}/m/rewind',
                       f'execute if score @s {S("s")} matches 0 run return run function bm:{pfx}/m/idle',
                       f'execute if score @s {S("s")} matches 1 run return run function bm:{pfx}/m/walk',
                       f'execute if score @s {S("s")} matches 10 run return run function bm:{pfx}/m/walk',
                       f'execute if score @s {S("s")} matches 2..3 run return run function bm:{pfx}/m/run',
                       f'execute if score @s {S("s")} matches 6 run return run function bm:{pfx}/m/happy',
                       f'execute if score @s {S("s")} matches 7 run return run function bm:{pfx}/m/strike',
                       f'execute if score @s {S("s")} matches 8 run return run function bm:{pfx}/m/stutter',
                       f'execute if score @s {S("s")} matches 11 run return run function bm:{pfx}/m/corrupt',
                       f'execute if score @s {S("s")} matches 12 run return run function bm:{pfx}/m/segfault',
                       f'function bm:{pfx}/anim0'])
    # (a walk or a fight just ended - about one in six: a REWIND)
    fn(f'{pfx}/m/changed', [f'execute if score @s {S("s")} matches 0 if score @s {S("ps")} matches 1..3 run function bm:{pfx}/m/maybe_rew',
                            f'execute if score @s {S("s")} matches 0 if score @s {S("ps")} matches 7..12 run function bm:{pfx}/m/maybe_rew',
                            f'scoreboard players operation @s {S("ps")} = @s {S("s")}'])
    fn(f'{pfx}/m/maybe_rew', ['execute store result score #r bm.rng run random value 1..6', f'execute if score #r bm.rng matches 1 run scoreboard players set @s {S("rw")} {RLEN}'])
    # ---- the RGB split (a red and a cyan copy of the head and slices, a hair to either side, 2 ticks) and the afterimage (4)
    new = '@e[type=minecraft:item_display,tag=bm.gxfxn]'
    fx = lambda m, life, tags=(): snbt({'Tags': ['bm.gxfx', 'bm.gxfxn'] + list(tags), 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:{m}'}},
                                        'item_display': 'fixed', 'teleport_duration': Int(0), 'brightness': {'block': Int(15), 'sky': Int(15)}, 'view_range': F(1.2)})
    copy = [f'execute as {new} run data modify entity @s transformation set from entity @e[type=minecraft:item_display,tag=bm.gxsrc,limit=1] transformation',
            f'execute as {new} run data modify entity @s Rotation set from entity @e[type=minecraft:item_display,tag=bm.gxsrc,limit=1] Rotation']
    fn(f'{pfx}/fx/rgb', [f'execute as {psel(p)} at @s run function bm:{pfx}/fx/rgb_{p}' for p in RGBP])
    for p in RGBP:
        fn(f'{pfx}/fx/rgb_{p}', ['tag @s add bm.gxsrc', f'summon minecraft:item_display ^0.05 ^ ^ {fx(f"gl_{p}_gr", 2)}', f'summon minecraft:item_display ^-0.05 ^ ^ {fx(f"gl_{p}_gc", 2)}'] +
           copy + [f'scoreboard players set {new} {S("fl")} 2', f'tag {new} remove bm.gxfxn', 'tag @s remove bm.gxsrc'])
    key = SH.KEY.get(C.W, 7)
    fn(f'{pfx}/fx/ghost', ['scoreboard players set #wk bm.rng 0', f'execute on owner run scoreboard players operation #wk bm.rng = @s bm.cos{ab}'] +
       [f'execute as {psel(p)} at @s run function bm:{pfx}/fx/gh_{p}' for p in SHOWN])
    for p in SHOWN:
        k = A0.PART_K.get(p, 1.0) * SP * 0.9
        fn(f'{pfx}/fx/gh_{p}', ['tag @s add bm.gxsrc', f'execute unless score #wk bm.rng matches {key} run summon minecraft:item_display ~ ~ ~ {fx(f"gl_{p}_g", 4, ["bm.gxgh"])}',
                                f'execute if score #wk bm.rng matches {key} run summon minecraft:item_display ~ ~ ~ {fx(f"gl_{p}_gg", 4, ["bm.gxgh"])}'] + copy +
           [f'scoreboard players set {new} {S("fl")} 4', f'tag {new} remove bm.gxfxn', 'tag @s remove bm.gxsrc'])
    gsc = round(SP * 0.9, 4)
    G.FUNCS['tick'] += [f'scoreboard players remove @e[type=minecraft:item_display,tag=bm.gxfx] {S("fl")} 1',
                        f'execute as @e[type=minecraft:item_display,tag=bm.gxgh,scores={{{S("fl")}=3}}] run data merge entity @s {{start_interpolation:0,interpolation_duration:3,transformation:{{scale:[{gsc}f,{gsc}f,{gsc}f]}}}}',
                        f'kill @e[type=minecraft:item_display,tag=bm.gxfx,scores={{{S("fl")}=..0}}]']
    # ---- stepped ground motion (its parts teleport with no glide, placed every other tick while it moves) and the jitter
    for fnm in (f'{pfx}/rig_here', f'{pfx}/enc/spawn'):
        G.FUNCS[fnm] = [l.replace('teleport_duration:2', 'teleport_duration:0') for l in G.FUNCS[fnm]]
    T_ = G.FUNCS[f'{pfx}/tick']
    k = T_.index(f'execute unless entity @s[tag=bm.rdr] run function bm:{pfx}/places')
    T_[k] = f'execute unless entity @s[tag=bm.rdr] run function bm:{pfx}/places2'
    fn(f'{pfx}/places2', [f'execute if score @s {S("s")} matches 1..3 store result score #p bm.rng run scoreboard players get @s {S("fr")}',
                          f'execute if score @s {S("s")} matches 1..3 run scoreboard players operation #p bm.rng %= #2 bm.rng',
                          f'execute unless score @s {S("s")} matches 1..3 run scoreboard players set #p bm.rng 0',
                          f'execute if score #p bm.rng matches 0 run function bm:{pfx}/places',
                          'execute store result score #r bm.rng run random value 1..400',
                          f'execute unless score @s {S("s")} matches 4 if score #r bm.rng matches ..72 run function bm:{pfx}/jit',
                          f'execute if score @s {S("s")} matches 4 if score #r bm.rng matches ..18 run function bm:{pfx}/jit',
                          f'function bm:{pfx}/pal'])
    jit = []
    for i, p in enumerate(('sl1', 'sl2', 'sl3')):
        for j, dx in enumerate((0.022, -0.022, 0.055, -0.055)):
            jit.append(f'execute if score #j bm.rng matches {i * 4 + j + 1} as {psel(p)} at @s run tp @s ^{dx} ^ ^')
    fn(f'{pfx}/jit', ['execute store result score #j bm.rng run random value 1..12'] + jit)
    # ---- the palette flicker: every 20-40 s the whole model, for 3-6 ticks (one in eight: SNOW first); not while Nia sits on it
    pal = lambda n: [f'execute as {psel(p)} run data modify entity @s item.components."minecraft:item_model" set value "bm:gl_{p}{n}"' for p in A.PARTS if A0.R._els[p]] + \
        ['scoreboard players set #wk bm.rng 0', f'execute on owner run scoreboard players operation #wk bm.rng = @s bm.cos{ab}',
         f'execute if score #wk bm.rng matches 1.. as {psel()} run function bm:p138/sfx']
    for n in ('', '_p1', '_p2', '_p3'):
        fn(f'{pfx}/pal/set{n or "_0"}', pal(n))
    fn(f'{pfx}/pal', [f'execute if score @s {S("pd")} matches 1.. run scoreboard players remove @s {S("pd")} 1',
                      f'execute if score @s {S("pd")} matches 0 run function bm:{pfx}/pal/set_0', f'execute if score @s {S("pd")} matches 0 run scoreboard players set @s {S("pd")} -1',
                      f'execute unless score @s {S("pt")} matches 1.. run execute store result score @s {S("pt")} run random value 400..800',
                      f'scoreboard players remove @s {S("pt")} 1', f'execute if score @s {S("pt")} matches 0 run function bm:{pfx}/pal/go'])
    fn(f'{pfx}/pal/go', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #ni bm.rng 0',
                         'execute as @e[type=minecraft:wolf,tag=bm.nipet,distance=..4] if score @s bm.pid = #me bm.pid run scoreboard players set #ni bm.rng 1',
                         'execute if score #ni bm.rng matches 1 run return 0',
                         f'execute if score @s {S("s")} matches 4 run return 0',
                         'execute store result score #r bm.rng run random value 1..3',
                         f'execute if score #r bm.rng matches 1 run function bm:{pfx}/pal/set_p1', f'execute if score #r bm.rng matches 2 run function bm:{pfx}/pal/set_p2',
                         f'execute if score #r bm.rng matches 3 run function bm:{pfx}/pal/set_p3',
                         f'execute store result score @s {S("pd")} run random value 3..6',
                         'execute store result score #r bm.rng run random value 1..8'] +
       [f'execute if score #r bm.rng matches 1 run {l}' for l in FX.face_cmd(C.W, 'snow', 2)] +
       ['playsound minecraft:block.note_block.bit neutral @a[distance=..12] ~ ~ ~ 0.3 0.6'])


def generate(G):
    fn, title = G.fn, G.title
    frame = dict(models=FRAMES, every=2, click=['particle minecraft:electric_spark ~ ~ ~ 0.3 0.3 0.3 0.3 20',
                                                'particle minecraft:dust{color:[1.0,0.24,0.78],scale:0.8} ~ ~ ~ 0.3 0.3 0.3 0 10',
                                                'particle minecraft:dust{color:[0.24,0.94,1.0],scale:0.8} ~ ~ ~ 0.3 0.3 0.3 0 10',
                                                'playsound minecraft:block.note_block.bit block @a[distance=..12] ~ ~ ~ 0.8 1.4'])
    W5.build(Glitch, G, _abilities, _encounter, sitb=(120, [(0, 'sit_b'), (70, 'sit_b2')]), frame=frame)
    _motion(G, Glitch)
    fn('admin/glitch_reset', ['tag @s remove bm.gxmet', f'clear @s *[minecraft:custom_data~{{bm:"{ITEM}"}}]',
                              title('@s', 'actionbar', T('The Glitch has not met you yet: a Glitched Cartridge, with your 8-bit trio out.', COL))])

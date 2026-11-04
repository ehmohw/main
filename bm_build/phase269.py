"""3.1: THE HOLLOW STATUE KNIGHT - the 58th follower (hollowknight_pet_art.py; fol5flag.KNIGHT). An Undercrown Statue Knight's armour
with a soul serpent coiled inside it: SIR ALDOUS VANE, once Captain of King Omega's palace guard - Pistachio's old master.

MEETING HIM   set up a knight statue you've won (knight_statue_dread, phase245), and stand by it with Pistachio and King Omega out
              (yours, near). Pistachio BARKS - his first bark; Omega: "...Aldous? Is that you in there?" Two glowing yellow eyes
              open in the eye-slit, the serpent's head slides out of the visor and rests its chin on Pistachio's head; the armour
              stands beside the statue (the statue stays yours). Right-click him: the HOLLOW KNIGHT'S TOKEN, and he comes along.
TWO IN ONE    one follower, two rigs (fol5art.KnightArt): the armour (knight_art's, at companion size) and the serpent (hs_). Every
              pose of his is written here (COMBO): the armour's pose, the serpent's (or none: he's inside, only his eyes and the
              coils glimpsed through the plate), and where the serpent's root sits - in the helm's visor, over the shoulders, or out
              in front, round a foe.
HIS WAYS      THE MACE (a foe within 2.8: a swing, 7; 9 on a foe the serpent holds); HISS (two foes within 4, every 12 s: the head
              slides out, the jaw opens, cold mist - Slowness II for 3 s); COIL (a foe 3-8 off, every 6 s: the serpent streaks to it
              and winds round it - Slowness III and no jumping for 3 s, held); THE SPIN (charged, every minute: the giant mace swung
              round - 9 to every monster within 3.5); BROKEN (once his health falls under a third: the armour collapses, and for 30 s
              the serpent fights alone, snake-strikes of 5 - then it pours back into the helm and the armour stands, healed).
EVERYTHING ELSE is every follower's: sitting (right-click: the vigil - the armour kneels, the serpent draped over its shoulders;
sneak + right-click: the statue stance, only his eyes glowing), a wardrobe (FREED - earned, never sold: a Totem of Undying and a
golden apple handed to him - and the Crimson and Verdant Guard cloaks, the metal plate), a rare aura (the Candle Vigil), a shiny
(Starlit), the Partner Wheel, a frame, a display case, Cecil's doll (the serpent curled round the helm), the honours, a Raid
Contract; pairs with Bender, Mr. Capshun, Henry and Nia."""
from items import item, T, TOTEM
from useitem import hold
from nbt import snbt
import fol5
import fol5art
import fol5wire as W5
import rigpet as RP
import rigfol as RF
import rigkit as RK
import phase235 as P235
import shiny as SH

S5 = fol5.SPEC['knight']
A0 = fol5art.get('knight')
H, AR, SR = A0.H, A0.AR, A0.SR
COL, LINE = S5['COL'], S5['LINE']
ITEM = S5['item']
CS = A0.FULL                                  # (the armour's size: the statue knights' own - companion size is compsize's twin)
SS = SR.RIG_SCALE * A0.F                      # (the serpent's, with it)
CSZ_K = round(H.COMPANION / A0.FULL, 4)
HOST_BIG, HOST_SMALL = 1.6, 0.9                # (his host's scale: his own size, and companion)
VISOR = (0.0, 41.9, -5.4)                     # (the eye-slit, knight_art units, on the helm - the art's own choreography sheet's)
SHOULDER = (10.6, 37.2, -0.6)                 # (his right pauldron, on the arm: where the serpent's neck lies when he kneels)
SH.UNSOLD.add('cos_knight_1')                 # (Freed: earned, never sold)
SR.POSES['drape2'] = dict(SR.POSES['drape'], head=__import__('fol5_kit').T(8, -12, 10))
SR.POSES['hiss_g'] = SR.ground(dict(SR.POSES['hiss']))

# WHERE THE SERPENT IS, pose by pose (hollowknight_pet_art's two-in-one sheet): its root placed so that one of its own points lands
# on one of the armour's - ('on', serpent part, its point, armour part, its point, nudge (blocks)) - or stood at a spot by him
# ('at', (x, y, z) blocks, display frame: +z his front, -x his right); a yaw of 180 turns it to face him (diving back in).
PEEK = ('on', 'b_peek', (0, -0.6, 7.5), 'head', VISOR, (0.0, -0.03, -0.04))
INTO = ('on', 'root', (0, 0, 0), 'head', VISOR, (0.0, 0.03, -0.2))
OUT_ = ('on', 'root', (0, 0, 0), 'head', VISOR, (0.0, 0.0, 0.0))
DRAPE = ('on', 'root', (0, 0, 0), 'armr', SHOULDER, (0.0, 0.03, 0.0))
COILD = ('on', 'b_coil', (0, -14, 6), None, (0.0, 1.3, 3.0), (0.0, 0.0, 0.0))   # (round a foe out in front of him: its coil's middle at a foe's chest height)
BESIDE = ('at', (-1.2, 0.0, 1.7))           # (on the ground at his right front)
# name: (armour pose, serpent pose or None (inside: only its eyes in the slit and the coils glimpsed through the plate), where, yaw)
COMBO = {'idle_a': ('idle_a', None, None, 0), 'idle_b': ('idle_b', 'peek', PEEK, 0), 'idle_c': ('idle_b', 'emerge', PEEK, 0),
         'walk_0': ('walk_0', None, None, 0), 'walk_1': ('walk_1', None, None, 0), 'happy': ('wake_1', 'emerge', PEEK, 0), 'statue': ('statue', None, None, 0),
         'sit_a': ('sit_a', 'drape', DRAPE, 0), 'sit_a2': ('sit_a', 'drape2', DRAPE, 0), 'sit_b': ('sit_b', None, None, 0), 'sit_b2': ('statue', None, None, 0),
         'swing_0': ('swing_0', None, None, 0), 'swing_1': ('swing_1', None, None, 0), 'spin_0': ('spin_0', None, None, 0), 'spin_1': ('spin_1', None, None, 0),
         'hiss_up': ('idle_a', 'emerge', PEEK, 0), 'hiss': ('idle_a', 'hiss_g', BESIDE, 0), 'divein': ('idle_a', 'divein', INTO, 180),
         'coil_go': ('idle_a', 'dive', OUT_, 0), 'coil': ('idle_a', 'coil', COILD, 0),
         'heap': ('heap', 'idle_a', BESIDE, 0), 'heap_up': ('heap', 'strike_up', BESIDE, 0), 'heap_strike': ('heap', 'strike', BESIDE, 0),
         'hurt': ('stagger', None, None, 0), 'tired': ('heap', None, None, 0)}
for _n, (_a, _s, _w, _y) in COMBO.items():
    A0.POSES[_n] = {'_arm': AR.POSES[_a], '_serp': SR.POSES[_s] if _s else None, '_face': (SR.POSES[_s].get('_face') if _s else None)}
A0.DOLL_POSE = None

item(ITEM, TOTEM, "The Hollow Knight's Token", COL,
     ['A tarnished guard\'s token, Omega\'s crest worn smooth.', 'Two faint yellow lights glint in it, like eyes.',
      ('Use: call the Hollow Statue Knight (again: call him over).', 'blue'), ('Sneak + use: his menu.', 'blue'),
      ('The mace, the Hiss, the Coil - and the serpent alone, if he breaks.', 'blue'), ('If he faints: 2 minutes before he can return.', 'gray'),
      ('"Mind the door, Pip."', 'dark_gray')],
     model=f'bm:{ITEM}', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)


class Knight(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'knight', 'The Hollow Statue Knight', COL, LINE, 'p269', 'hx', 'iz'
    A = A0
    MENU, PET_HP, PET_CD, ITEM = 5950, 46, 120, ITEM
    pron, they = 'him', 'he'
    BODY_PART = 'body'
    TWEEN = False
    EXPR = RP.Cfg.EXPR + ('hiss',)
    FACE = dict(A0.FACE_MAP, hiss='hiss')
    ATTRS = dict(armor=10, attack_damage=5, movement_speed=0.3, follow_range=32, step_height=1.1)
    SCALE, HIT = HOST_BIG, (1.3, 3.0)               # (his body and helm, the statue knights' own size; the mace swings outside it)
    BOX_FIT = True
    BUTTONS = ((6, 'Companion Size: on / off', 'The Knight at a companion\'s size - about your height. Off: as tall as the statue knights.', 'p269/csz/toggle'),)
    CYCLE = W5.cycle(A0, (240, [(0, 'idle_a'), (90, 'idle_b'), (150, 'idle_a'), (190, 'idle_c'), (220, 'idle_a')]), (80, [(0, 'sit_a'), (40, 'sit_a2')]),
                     (None, [(0, 'happy'), (14, 'idle_a')]),
                     {7: (None, [(0, 'swing_0'), (4, 'swing_1'), (10, 'idle_a')]), 8: (None, [(0, 'coil_go'), (6, 'coil'), (60, 'divein'), (66, 'idle_a')]),
                      11: (None, [(0, 'hiss_up'), (4, 'hiss'), (16, 'divein'), (22, 'idle_a')]), 12: (None, [(0, 'spin_0'), (6, 'spin_1'), (14, 'idle_a')]),
                      13: (None, [(0, 'heap_up'), (4, 'heap_strike'), (8, 'heap')])}, wp=12, rp_=8)
    DUR = dict(P235._DUR, swing_0=4, swing_1=2, spin_0=6, spin_1=4, hiss_up=4, hiss=3, divein=5, coil_go=6, coil=4, heap=10, heap_up=4, heap_strike=3,
               sit_a=16, sit_a2=24, sit_b=16, statue=12, happy=8, walk_0=6, walk_1=6)
    QUIPS = ['"Mind the door, Pip." (he says it to no one; he says it often)', '(the yellow eyes in the slit narrow, pleased, as you pass)',
             '"Three hundred years in a suit of armour. One gets used to it."', '"Hold the stair. Always hold the stair."',
             '(the serpent\'s tail-flame peeks out under the cape, and flickers)', '"Omega was a good king. Is a good king. Forgive me - I lose track."']
    HELLO = ('(the Hollow Statue Knight strides back to you, plate ringing)', '(a clank of plate - the Knight steps out of the dark, two yellow eyes glowing in the slit) "Captain Vane, reporting."',
             '(he salutes, and his soul withdraws - the armour goes still, and is gone)')
    SIT = ('"On my feet. The watch goes on."', '(the armour kneels on one knee, the mace planted; the serpent drapes itself over its shoulders)')
    FAINT = '"...hold... the stair..."'
    NOT_YOURS = '(the yellow eyes regard you from the slit) "You are not my captain. ...I have no captain. Move along."'
    POWERS = [('The Mace', 'a foe within 2.8: a swing of the giant mace, 7 - and 9 on a foe the serpent holds'),
              ('Hiss', 'two foes within 4, every 12 s: the serpent slides out of the visor, jaw open - cold mist: Slowness II for 3 s'),
              ('Coil', 'a foe 3-8 off, every 6 s: the serpent streaks to it and winds round it - Slowness III and no jumping for 3 s'),
              ('The Spin', 'charged, every minute: the giant mace swung round - 9 to every monster within 3.5'),
              ('Broken', 'under a third of his health: the armour collapses, and for 30 s the serpent fights alone (bites of 5) - then the armour stands again, healed'),
              ('Companion Size', 'his menu: as tall as the statue knights, or about your height - his hitbox with it'),
              ('Freed', 'hand him a Totem of Undying, a golden apple in your pack and Pistachio by to serve it: the holy finish - silver, gold and a white cloak')]
    INTRO = [T('The Hollow Statue Knight', COL, bold=True), T(' - Sir Aldous Vane, Captain of Omega\'s guard, bound as a soul serpent in a statue\'s armour. ', 'gray'),
             T('"Mind the door, Pip."', LINE, italic=True)]
    BURST = ['particle minecraft:soul ~ ~1 ~ 0.4 0.7 0.4 0.02 16', 'particle minecraft:soul_fire_flame ~ ~1.4 ~ 0.3 0.4 0.3 0.01 8']
    FADE_SOUND = 'playsound minecraft:block.chain.break neutral @a[distance=..20] ~ ~ ~ 1 0.6'
    SUMMON_EXTRA = ['playsound minecraft:item.armor.equip_netherite neutral @a[distance=..24] ~ ~ ~ 1 0.8', 'playsound minecraft:entity.vex.ambient neutral @a[distance=..24] ~ ~ ~ 0.5 0.6']
    ENC_POSES = [(0, 'statue'), (30, 'idle_b'), (60, 'idle_c')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 30 run particle minecraft:soul ~ ~1.6 ~ 0.2 0.2 0.2 0.01 4'
    ADV = ('Mind the Door, Pip', 'Stand by a knight statue with Pistachio and King Omega - and meet the captain inside it')
    ADMIN_HINT = 'Set up a won knight statue, and stand by it with Pistachio and King Omega out.'
    MEET_HINT = 'Right-click him.'


_DOLL = 'A doll of the Hollow Statue Knight - the dark armour, and a soul serpent curled round its helm.'
_eff = W5.pair_fx
_PAIRS = {
    'hx_bender': ('knight', 'bender', 'Old Dog, New Tricks', '#e0a860', 'The Knight and Bender - a captain who had a dog once, and a dog who would like a captain',
                  _eff(('speed', 0), ('strength', 0)),
                  [('bender', '(sits at the Knight\'s heel, as if he\'d always done it)'), ('knight', '"...Good boy. Good. Mind the door."')],
                  [('knight', '(the serpent pats Bender with its chin)', 'bender', '(leans on the armour\'s leg, tail thumping)')]),
    'hx_capshun': ('knight', 'capshun', 'Restoration', '#f0f0f0', 'The Knight and Mr. Capshun - he paints over the chips in its plate',
                   _eff(('resistance', 0), ('haste', 0)),
                   [('capshun', '[Mr. Capshun narrates: "He painted the old plate as good as new."]'), ('knight', '"I have not looked this smart since the coronation."')],
                   [('knight', '(the serpent doodles a soul-flame on his page)', 'capshun', '[Mr. Capshun narrates: "It was, he admitted, rather good."]')]),
}
W5.register(Knight, A0, _DOLL, ('minecraft:soul', 'minecraft:item.armor.equip_netherite', 'minecraft:soul'), _PAIRS, 'the Hollow Statue Knight')


# ---------------------------------------------------------------------------------------------------- his poses, two rigs at once
def _root(apz, spz, where, yaw):
    """where the serpent's root stands (blocks, from the host, display frame) for this armour pose and serpent pose"""
    if where[0] == 'at':
        return where[1]
    _k, sp, spt, ap, apt, nudge = where
    tgt = RK.point(AR, apz, ap, apt, scale=CS) if ap else apt          # (no armour part: a spot by him, in blocks)
    w = RK.point(SR, spz, sp, spt, scale=SS, yaw=yaw)
    return tuple(tgt[i] + nudge[i] * A0.F - w[i] for i in range(3))     # (the art's nudges are at companion size)


def _turn(v, yaw):
    return (-v[0], v[1], -v[2]) if yaw == 180 else v


def serp_xf(apz, spz, where, yaw):
    """{serpent part: (rotation, translation (blocks, from the host))} - its displays all stand at the host"""
    anc = _root(apz, spz, where, yaw)
    xf = RK.solve(SR.PIVOT, SR.PARENT, spz)
    qy = RK.qa((0, 1, 0), 180) if yaw == 180 else None
    out = {}
    for p in SR.PARTS:
        if SR.HIDDEN(p, spz):
            continue
        q, t = xf[p]
        a = RK.D(SR.PIVOT[p])
        v = _turn(tuple((a[i] + t[i]) * SS / 16 for i in range(3)), yaw)
        out[p] = (RK.qmul(qy, q) if qy else q, tuple(anc[i] + v[i] for i in range(3)))
    return out


def combo_pose(name, dur):
    apn, spn, where, yaw = COMBO[name]
    apz = AR.POSES[apn]
    psel = lambda p: f'@e[type=minecraft:item_display,tag=bm.hxsel,tag=bm.hxp_{p}]'
    out = RF.pose(AR, apz, CS, dur, psel)
    spz = SR.POSES[spn] if spn else None
    xf = serp_xf(apz, spz, where, yaw) if spz else {}
    for p in SR.PARTS:
        sp = psel(f's_{p}')
        if p not in xf:
            out.append(f'execute as {sp} run data merge entity @s {{start_interpolation:0,interpolation_duration:{min(dur, 2)},transformation:{{scale:[0f,0f,0f]}}}}')
            continue
        q, tr = xf[p]
        sc = round(SS * SR.PART_K.get(p, 1.0), 4)
        out.append(f'execute as {sp} run data merge entity @s {{start_interpolation:0,interpolation_duration:{dur},transformation:{{left_rotation:{snbt(RF.qf(q))},'
                   f'translation:[{tr[0]:.4f}f,{tr[1]:.4f}f,{tr[2]:.4f}f],scale:[{sc}f,{sc}f,{sc}f]}}}}')
    return out


# (the display case's figure: the armour at rest, the serpent inside it - and the doll's: the serpent curled round the helm, as the art's)
import phase134 as P134  # noqa: E402
import phase141 as P141  # noqa: E402
_figs0 = P134.figures


def _doll_fig():
    apz, spz = AR.POSES['idle_a'], SR.POSES['helm']
    hc = RK.point(AR, apz, 'head', (0, 43.4, -0.4), scale=CS)
    w = RK.point(SR, spz, 'b_helm', H.HELM_C, scale=SS)
    off = tuple(hc[i] - w[i] for i in range(3))
    return P134._rigkit(AR, apz, CS) + [(m, tuple(t[i] + off[i] for i in range(3)), l, r, sc) for m, t, l, r, sc in P134._rigkit(SR, spz, SS)]


def _figures():
    F2 = _figs0()
    F2[ITEM] = (Knight.NAME, P134._rigkit(AR, AR.POSES['idle_a'], CS))
    F2[f'{ITEM}_doll'] = (Knight.NAME, _doll_fig())
    return F2


P134.figures = _figures
P134.FIT[f'{ITEM}_doll'] = P134.FIT[ITEM] = A0.FIT
P134.BAKE_ONLY.add(f'{ITEM}_doll')
_dg = {f'bm:{AR.model_name(p, {})}': g for p, g in H.DOLL_GROUPS.items()}
_dg.update({f'bm:{SR.model_name(p, SR.POSES["helm"])}': 'head' for p in SR.PARTS})
P141.DOLL_FROM['doll_knight'] = (f'{ITEM}_doll', dict(H.DOLL, groups=_dg))
FRAMES = [f'{ITEM}_f0', f'{ITEM}_f1']


def extend_offers(O, offer):
    pass


def generate_early(G):
    RP.contract(Knight, G)


def _icon(eyes=True):
    """The Hollow Knight's Token - a tarnished guard's token, Omega's crest worn smooth; two yellow eyes glint in it (shut, on a frame)"""
    from sprites280 import S
    s = S()
    pal = {'g': '#8a8a96', 'l': '#c4c4d0', 'd': '#3a3a48', 'k': '#14141c', 'y': '#ffe040', 'o': '#a08a3a', 'v': '#6a4aa0'}
    s.g(['...llll...', '..lggggd..', '.lgddddgd.', '.gdkkkkdd.', '.gdkkkkdd.', '.gdvvvvdd.', '..gdvvdd..', '...dddd...', '....oo....', '...o..o...'], pal, 3, 2)
    if eyes:
        s.px(6, 5, '#ffe040'); s.px(9, 5, '#ffe040')
    else:
        s.px(6, 5, '#2a2a34'); s.px(9, 5, '#2a2a34')
    return s.render()


def rp(R):
    W5.rp(Knight, R, _icon(), A0)
    R.ICONS[FRAMES[0]] = _icon(False)
    R.ICONS[FRAMES[1]] = _icon(True)


def textures():
    return A0.textures()


# ---------------------------------------------------------------------------------------------------- his ways
def _abilities(G, X):
    fn, pfx, foe, S = G.fn, X.pfx, X.foe, X.S
    snd = lambda s, v=0.6, p=1.0: f'playsound minecraft:{s} neutral @a[distance=..16] ~ ~ ~ {v} {p}'
    K = dict(melee=dict(st=7, x=12, at=6, cd=24, reach=2.8, face='serious', go=[snd('entity.iron_golem.attack', 0.6, 0.8)]),
             ranged=dict(st=8, x=70, at=62, cd=120, near=3, far=8, face='serious', go=[snd('entity.vex.charge', 0.6, 0.8)]),
             crowd=dict(st=11, x=24, at=18, cd=240, r=4, n=2, face='hiss', go=[snd('entity.cat.hiss', 0.8, 0.5)]),
             charged=dict(st=12, x=16, at=8, cd=1200, r=3.5, face='serious', go=[snd('entity.player.attack.sweep', 0.8, 0.5)]))
    lines = P235.kit(G, X, K)
    G.FUNCS.pop(f'{pfx}/near_owner', None)              # (no kindness of his own: nothing asks whether you're near)
    # THE MACE: 7 (9 on a foe the serpent holds)
    fn(f'{pfx}/melee', X.hit(7) + [f'execute as @e[{foe},distance=..3.2,sort=nearest,limit=1] at @s run function bm:{pfx}/maced'] + X.end)
    fn(f'{pfx}/maced', [f'execute if entity @s[tag=bm.hxheld] run scoreboard players set #pd bm.rng 9', f'function bm:{pfx}/hurt',
                        'particle minecraft:crit ~ ~1 ~ 0.3 0.3 0.3 0.2 10', snd('entity.iron_golem.damage', 0.6, 0.8)])
    # HISS: two foes near - the serpent out on the ground at his side, cold mist in a cone: Slowness II
    fn(f'{pfx}/crowd', X.hit(2) + [f'execute positioned ^ ^ ^2 as @e[{foe},distance=..2.8] at @s run function bm:{pfx}/hissed',
                                   'particle minecraft:snowflake ^-0.6 ^0.5 ^1.6 0.6 0.3 0.6 0.02 30'] + X.end)
    fn(f'{pfx}/hissed', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 3 1'])
    # COIL: a foe 3-8 off wound round - held 3 s (Slowness III, no jumping; tagged: the mace's 9)
    fn(f'{pfx}/ranged', [f'execute as @e[{foe},distance=..8.5,sort=nearest,limit=1] at @s run function bm:{pfx}/coiled'])
    fn(f'{pfx}/coiled', ['effect give @s minecraft:slowness 3 2', 'effect give @s minecraft:jump_boost 3 128', 'tag @s add bm.hxheld',
                         'scoreboard players set @s bm.izhd 60', 'particle minecraft:soul ~ ~1 ~ 0.4 0.6 0.4 0.02 20', snd('entity.vex.ambient', 0.8, 0.6)])
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.izhd dummy', 'scoreboard objectives add bm.izbk dummy']
    G.OBJECTIVES += ['bm.izhd', 'bm.izbk']
    X.tick += ['scoreboard players remove @e[tag=bm.hxheld] bm.izhd 1', 'tag @e[tag=bm.hxheld,scores={bm.izhd=..0}] remove bm.hxheld']
    # THE SPIN: 9 to every monster within 3.5
    fn(f'{pfx}/charged', X.hit(9) + [f'execute as @e[{foe},distance=..3.8] at @s run function bm:{pfx}/hurt', 'particle minecraft:sweep_attack ~ ~1 ~ 1.6 0.3 1.6 0 10',
                                     snd('entity.player.attack.sweep', 1.0, 0.6)] + X.end)
    # BROKEN: under a third of his health - the armour heaped for 30 s, the serpent fighting alone (a strike every 2 s); then he stands, healed
    say = lambda txt: 'execute on owner run ' + G.title('@s', 'actionbar', [T('The Hollow Statue Knight: ', COL, bold=True), T(txt, LINE)])
    X.second.append('execute as @e[type=minecraft:wolf,tag=bm.hxpet,tag=!bm.hxbrk] at @s run function bm:p269/broken_q')
    fn('p269/broken_q', ['execute store result score #h bm.rng run data get entity @s Health', f'execute if score #h bm.rng matches ..{Knight.PET_HP // 3} run function bm:p269/break'])
    fn('p269/break', ['tag @s add bm.hxbrk', 'scoreboard players set @s bm.izbk 30', 'effect give @s minecraft:slowness 30 2 true',
                      'particle minecraft:soul ~ ~1 ~ 0.5 0.8 0.5 0.03 30', snd('block.chain.break', 1.0, 0.5), say('(the armour falls apart - the soul fights on)'),
                      f'scoreboard players set @s {S("fr")} -1'])                 # (its cycle starts over: whichever pose it asks for, broken, is the heap)
    X.second.append('execute as @e[type=minecraft:wolf,tag=bm.hxpet,tag=bm.hxbrk] at @s run function bm:p269/broken_s')
    fn('p269/broken_s', ['scoreboard players remove @s bm.izbk 1', 'execute if score @s bm.izbk matches ..0 run return run function bm:p269/mend'] +
       [f'scoreboard players set @s {S(c)} 40' for c in ('mc', 'rc', 'k2', 'gc')] +
       ['execute store result score #r bm.rng run random value 1..2',
        f'execute if score #r bm.rng matches 1 if entity @e[{foe},distance=..3.4] unless score @s {S("x")} matches 1.. run function bm:p269/strike'])
    fn('p269/strike', X.go(13, 10, 'mc', 40) + X.hit(5) + [f'execute as @e[{foe},distance=..3.6,sort=nearest,limit=1] at @s run function bm:{pfx}/hurt',
                                                         snd('entity.vex.hurt', 0.6, 0.6)] + X.end)
    fn('p269/mend', ['tag @s remove bm.hxbrk', 'effect clear @s minecraft:slowness', f'data modify entity @s Health set value {Knight.PET_HP * 0.6:.1f}f',
                     'particle minecraft:soul_fire_flame ~ ~1 ~ 0.4 0.8 0.4 0.03 30', snd('item.armor.equip_netherite', 1.0, 0.8), say('"...On my feet. The watch goes on."'),
                     f'scoreboard players set @s {S("fr")} -1'] + [f'scoreboard players set @s {S(c)} 0' for c in ('mc', 'rc', 'k2')])
    return lines


def _encounter(G, X):
    """a won knight statue set up (phase245) - yours, and still - with Pistachio and Omega yours and near: the captain inside wakes"""
    fn, tellraw, title = G.fn, G.tellraw, G.title
    X.second.append('execute as @a[tag=!bm.hxmet,gamemode=!spectator] at @s if entity @e[type=minecraft:interaction,tag=bm.knst_dread,distance=..6] run function bm:p269/enc/q')
    fn('p269/enc/q', ['execute if entity @e[type=minecraft:interaction,tag=bm.hxenc,distance=..24] run return 0',
                      'execute unless score @s bm.pid matches 1.. run return 0', 'scoreboard players operation #me bm.pid = @s bm.pid',
                      'scoreboard players set #tr bm.rng 0',
                      'execute as @e[type=minecraft:wolf,tag=bm.pipet,distance=..10] if score @s bm.pid = #me bm.pid run scoreboard players add #tr bm.rng 1',
                      'execute as @e[type=minecraft:wolf,tag=bm.ompet,distance=..10] if score @s bm.pid = #me bm.pid run scoreboard players add #tr bm.rng 1',
                      'execute unless score #tr bm.rng matches 2.. run return 0',
                      'execute as @e[type=minecraft:interaction,tag=bm.knst_dread,distance=..6,sort=nearest,scores={bm.kgm=0}] if score @s bm.pid = #me bm.pid at @s run return run function bm:p269/enc/wake'])
    fn('p269/enc/wake', ['execute facing entity @p feet rotated ~ 0 positioned ^-1.0 ^ ^0.8 run function bm:p269/enc/spawn',
                         'scoreboard players operation @e[type=minecraft:interaction,tag=bm.hxenc,distance=..3] bm.pid = #me bm.pid',
                         'playsound minecraft:entity.wolf.ambient neutral @a[distance=..16] ~ ~ ~ 1 1.2', 'particle minecraft:soul ~ ~2 ~ 0.4 0.6 0.4 0.02 20',
                         'execute as @e[type=minecraft:wolf,tag=bm.pipet,distance=..10] if score @s bm.pid = #me bm.pid at @s run particle minecraft:note ~ ~1.2 ~ 0 0 0 1 1',
                         tellraw('@a[distance=..16]', [T('Pistachio sniffs the plinth - and BARKS. ', '#7ae890', italic=True), T('King Omega: ', '#9fb4ff', bold=True),
                                                       T('"...Aldous? Is that you in there?" ', '#d8e0ff'),
                                                       T('Two glowing yellow eyes open in the eye-slit. The armour steps down beside the statue.', 'gray', italic=True)])])
    csay = lambda txt: title('@s', 'actionbar', [T('The Hollow Statue Knight: ', COL, bold=True), T(txt, LINE)])
    fn('p269/enc/talk', [f'execute unless score @s bm.pid = {X.here} bm.pid run return run ' + csay('"You are not the one who brought Pip to me."'),
                         'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.0',
                         tellraw('@s', [T('The serpent slides out of the visor and rests its chin on Pistachio\'s head a long moment. ', LINE, italic=True),
                                        T('"Mind the door, Pip." Then the captain gives you his old guard\'s token. He will walk with you.', 'gray', italic=True)]),
                         'function bm:p269/enc/joined'])
    fn('admin/knight_meet_here', ['execute positioned ^ ^ ^2 run function bm:p269/enc/spawn',
                                  'scoreboard players operation @e[type=minecraft:interaction,tag=bm.hxenc,distance=..4] bm.pid = @s bm.pid'])


def generate(G):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    frame = dict(models=[FRAMES[1], FRAMES[0]], every=5,
                 click=['particle minecraft:soul ~ ~0.2 ~ 0.15 0.15 0.15 0.01 8', 'playsound minecraft:entity.vex.ambient block @a[distance=..12] ~ ~ ~ 0.4 0.6',
                        'execute on owner run ' + title('@s', 'actionbar', [T('(a whisper from the token) ', 'gray', italic=True), T('"Mind the door, Pip."', LINE)])])
    W5.build(Knight, G, _abilities, _encounter, sitb=(120, [(0, 'sit_b'), (60, 'sit_b2')]), frame=frame)
    pfx = Knight.pfx
    # ---- every pose: the two rigs at once (rigpet wrote one per cycle key: each rewritten here) - and broken, any pose but his own is the heap
    for n in [n for n in G.FUNCS if n.startswith(f'{pfx}/pose/')]:
        name = n[len(f'{pfx}/pose/'):]
        assert name in COMBO, name
        G.FUNCS[n] = ([] if name.startswith('heap') or name == 'tired' else [f'execute if entity @s[tag=bm.hxbrk] run return run function bm:{pfx}/pose/heap']) + \
            combo_pose(name, Knight.DUR.get(name, 6))
    for name in ['heap', 'happy'] + [p for _t, p in Knight.ENC_POSES]:          # (and the encounter's - the statue stance is in no cycle)
        if f'{pfx}/pose/{name}' not in G.FUNCS:
            G.FUNCS[f'{pfx}/pose/{name}'] = combo_pose(name, Knight.DUR.get(name, 6))
    # ---- COMPANION SIZE (compsize, as the Rat King's): his rig - armour and serpent, every pose - at CSZ_K, his host and click box with
    #      it; the owner's bm.hxcs, kept across recall
    import compsize as CSZ
    say = lambda txt: title('@s', 'actionbar', [T('The Hollow Statue Knight: ', COL, bold=True), T(txt, LINE)])
    hit_small = tuple(round(v * CSZ_K, 2) for v in Knight.HIT)
    CSZ.build(G, pfx, 'bm.hxcs', 'bm.hxcz', f'bm.{Knight.q}s', HOST_BIG, HOST_SMALL,
              say('"At ease. I can stand a little shorter - it was never the height that held the stair." (Companion Size: on)'),
              say('"Back to my post\'s full height. Hold the stair." (Companion Size: off)'), hit=('bm.hxhit', Knight.HIT, hit_small))
    CSZ.LATE.append((pfx, CSZ_K, 'bm.hxcz', ()))
    T_ = G.FUNCS[f'{pfx}/tick']
    assert T_[0] == 'scoreboard players operation #me bm.pid = @s bm.pid', T_[0]
    T_[1:1] = CSZ.sync(pfx, 'bm.hxcs', 'bm.hxcz', f'bm.{Knight.q}s', HOST_BIG, HOST_SMALL)
    fn(f'{pfx}/box_fit', [f'execute if entity @s[tag=bm.hxcz] run function bm:{pfx}/box/small'])
    fn(f'{pfx}/box/small', CSZ.resize('bm.hxhit', *hit_small))
    # ---- his displays' own models (two rigs: the armour's hk_hollow_<part>, the serpent's hs_<part> - not rigpet's <prefix><part>)
    names = {f'"bm:{A0.PREFIX}{p}"': f'"bm:{A0.model_name(p, {})}"' for p in A0.PARTS}
    for k, L in G.FUNCS.items():
        if any('"bm:hk_' in l for l in L):
            G.FUNCS[k] = [_named(l, names) for l in L]
    # ---- FREED: a Totem of Undying handed to him, a golden apple in your pack, Pistachio by to serve it (his dinner) - look 1, earned
    W_ = G.FUNCS[f'{pfx}/who']
    k = next(i for i, l in enumerate(W_) if 'bm.pid = #me bm.pid run return run' in l)
    W_.insert(k + 1, 'execute if items entity @s weapon.mainhand minecraft:totem_of_undying run return run function bm:p269/freed')
    csay = lambda txt: title('@s', 'actionbar', [T('The Hollow Statue Knight: ', COL, bold=True), T(txt, LINE)])
    fn('p269/freed', ['scoreboard players set #q bm.rng 0', 'execute if score @s bm.wuknight matches 0.. run function bm:p269/has1',
                      'execute if score #q bm.rng matches 1 run return run ' + csay('"I am free already, friend. I stay because I wish to."'),
                      'execute unless items entity @s container.* minecraft:golden_apple run return run ' + csay('"A totem... and something golden, to break the last of the binding. A golden apple."'),
                      'scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #pi bm.rng 0',
                      'execute as @e[type=minecraft:wolf,tag=bm.pipet,distance=..10] if score @s bm.pid = #me bm.pid run scoreboard players set #pi bm.rng 1',
                      'execute if score #pi bm.rng matches 0 run return run ' + csay('"...Not without Pip. He always laid the table for the last supper of a watch."'),
                      'item modify entity @s weapon.mainhand {type:"minecraft:set_count",count:-1,add:true}', 'clear @s minecraft:golden_apple 1',
                      'function bm:p99/unlock/knight1', 'scoreboard players set @s bm.coshx 1', 'function bm:p99/knight_now',
                      'playsound minecraft:block.beacon.activate player @s ~ ~ ~ 1 1.2',
                      tellraw('@s', [T('Pistachio: ', '#7ae890', bold=True), T('"Dinner is served, Captain." (he lifts his cloche: a golden apple, sliced, on a silver plate)', '#c8f0d0')]),
                      tellraw('@s', [T('The totem cracks; the apple glows. The last of Apophiss\'s binding falls away - ', LINE, italic=True),
                                     T('and the armour shines silver and gold. FREED. ', '#fff0c0', bold=True), T('(He stays because he wants to.)', 'gray')])])
    fn('p269/has1', ['scoreboard players operation #q bm.rng = @s bm.wuknight', 'scoreboard players set #bit bm.rng 2',
                     'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng'])
    fn('admin/knight_reset', ['tag @s remove bm.hxmet', f'clear @s *[minecraft:custom_data~{{bm:"{ITEM}"}}]',
                              title('@s', 'actionbar', T('The Hollow Statue Knight has not met you yet.', COL))])


def _named(line, names):
    for a, b in names.items():
        line = line.replace(a, b)
    return line

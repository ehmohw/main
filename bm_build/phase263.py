"""3.1: THE DOODLE MOB - the Doodle Dragon's new name (fol5flag.DOODLEMOB; his id stays 'dragon' / dd_ / p235d, so saves keep). Kettle
has started drawing him as Minecraft's own mobs (doodlemob_forms_art): a crayon costume per mob, each with its own moves.

HIS FORMS   one at a time (bm.ddf on his player: 0 the old drawings - the Ender Dragon, or the Doodle Creeper / Crayon Green as
            before; 1-6 a mob), each unlocked by handing him something (right-click him holding it), and switched to:
              the Doodle ZOMBIE           (the new default: every new friend of his meets him as one) - rotten flesh switches back
              the Doodle SKELETON         a bone
              the Doodle CHICKEN JOCKEY   an egg - once he has killed a baby zombie (bm.ddbz)
              the Doodle IRON GOLEM       a block of iron                      (his own pivots: a broad body, long arms)
              the Doodle AXOLOTL          a bucket of axolotl (he hugs it, lets it go, and gives you the bucket back)
              the Doodle ENDERMAN         an ender pearl                       (his own pivots: tall and thin)
              the Doodle ENDER DRAGON     a bottle of dragon's breath (anyone who befriended him before 3.1 has it already, and
                                          keeps it on: bm.ddend)
            Once unlocked, a form is a row of his wardrobe (switch to it there, or hand him its item again); the Creeper and
            Crayon Green are his dragon's, as before. Every look and the shiny recolour every form.
HOW         the dragon's rig wears the form's crayon cards (each part's model), and the form's own poses move it - solved on the
            form's pivots, each part shifted from the dragon's joint to the form's (p263/<f>/pose/<pose>); his host is tagged
            bm.ddmf<k>, and each of his moves goes that form's way (FORM_MOVES). His click box fits the form."""
from items import T
from nbt import snbt
import fol5flag as FL
import doodle_dragon_art as DA
import doodlemob_forms_art as FA
import rigkit as RK
import rigfol as RF

FORMS = ['zombie', 'skeleton', 'jockey', 'golem', 'axolotl', 'enderman']          # (bm.ddf 1..6)
K = {f: i + 1 for i, f in enumerate(FORMS)}
SHORT = {f: FA.FORMS[f].PREFIX[2:4] for f in FORMS}                              # (zo, sk, jo, go, ax, en)
NAME = {'zombie': 'Doodle Zombie', 'skeleton': 'Doodle Skeleton', 'jockey': 'Doodle Chicken Jockey', 'golem': 'Doodle Iron Golem',
        'axolotl': 'Doodle Axolotl', 'enderman': 'Doodle Enderman'}
FCOL = {'zombie': '#5aa84a', 'skeleton': '#e8e4d8', 'jockey': '#f6a23a', 'golem': '#d8d2c4', 'axolotl': '#ffa8c8', 'enderman': '#d86aff'}
HAND = {'zombie': 'minecraft:rotten_flesh', 'skeleton': 'minecraft:bone', 'jockey': 'minecraft:egg', 'golem': 'minecraft:iron_block',
        'axolotl': 'minecraft:axolotl_bucket', 'enderman': 'minecraft:ender_pearl'}
DRAGON_HAND = 'minecraft:dragon_breath'
CODES = {'dragon': 4630, 'zombie': 4631, 'skeleton': 4632, 'jockey': 4633, 'golem': 4634, 'axolotl': 4635, 'enderman': 4636}
SC, END, BZ, MOB = 'bm.ddf', 'bm.ddend', 'bm.ddbz', 'bm.ddmob'
UN = lambda f: f'bm.ddu_{SHORT[f]}'
MF = 'bm.ddmf'                     # (any mob form, on his host; bm.ddmf<k> its own)
MOB_NAME = 'The Doodle Mob'
DCOL = '#5ac048'
# (the faces: every mood of his to one of a form's three)
FACE = {'happy': 'happy', 'squint': 'happy', 'puff': 'happy', 'surprised': 'happy', 'blink': 'blink', 'sleepy': 'blink', 'dizzy': 'blink', 'hurt': 'blink',
        'serious': 'fierce', 'roar': 'fierce'}
from fol5_kit import T as _T  # noqa: E402
for _f, _R in FA.FORMS.items():
    _R.POSES['sit_a2'] = dict(_R.POSES['sit_a'], head=_T(0, 0, -6))
    _R.POSES['sit_a2'] = _R.ground(_R.POSES['sit_a2'])


# ---------------------------------------------------------------------------------------------------- his moves, form by form
# (event: name, what it does, damage, how ('near' the nearest in reach / 'aoe' all within r / 'shot' the nearest, a trail to it /
#  'blink' to the nearest's back first / 'you' his player and himself), r, the foe's effects, particles at it, a sound)
_d = lambda r, g, b, s=1.0: f'minecraft:dust{{color:[{r},{g},{b}],scale:{s}}}'
FORM_MOVES = {
    'zombie': {
        'melee': ('Grab', 'a foe within reach: arms up - and a hug-bite, 6, held (slowed) a moment', 6, 'near', 2.6, ['slowness 1 2'], [_d(0.35, 0.66, 0.29)], 'entity.zombie.attack_wooden_door'),
        'ranged': ('Shamble', 'a foe 2.5-8 off, every 4 s: a lurching lunge at it - and a bite, 6', 6, 'blink', 8, ['slowness 2 0'], [_d(0.35, 0.66, 0.29)], 'entity.zombie.ambient'),
        'crowd': ('Horde Hug', 'two or more foes within 3.5, every 12 s: a big group hug - 5 each, slowed', 5, 'aoe', 3.5, ['slowness 3 1'], [_d(0.17, 0.72, 0.75)], 'entity.zombie.ambient'),
        'charged': ('BRAAAINS', 'charged, every minute: a great crayon groan - 8 to every monster within 6, weakened', 8, 'aoe', 6, ['weakness 6 1'], [_d(0.35, 0.66, 0.29, 1.4)], 'entity.zombie.ambient'),
        'kind': ('Undead Hug', 'out of a fight beside you, every minute: a careful hug - Absorption and Regeneration for you', 0, 'you', 0, ['absorption 60 1', 'regeneration 10 0'], ['minecraft:heart ~ ~1.8 ~ 0.3 0.2 0.3 0 3'], 'entity.zombie.ambient')},
    'skeleton': {
        'melee': ('Bone Bonk', 'a foe within reach: a bonk with his bow, 5', 5, 'near', 2.6, [], ['minecraft:crit ~ ~1 ~ 0.2 0.2 0.2 0.2 6'], 'entity.skeleton.hurt'),
        'ranged': ('Bone Arrow', 'a foe 2.5-8 off, every 4 s: a crayon arrow, drawn and loosed - 7', 7, 'shot', 8, [], ['minecraft:crit ~ ~1 ~ 0.2 0.2 0.2 0.3 10'], 'entity.arrow.shoot'),
        'crowd': ('Rattle', 'two or more foes within 3.5, every 12 s: he rattles his bones at them - 4 each, slowed and shaken', 4, 'aoe', 3.5, ['slowness 2 0', 'weakness 3 0'], [_d(0.94, 0.93, 0.88)], 'entity.skeleton.ambient'),
        'charged': ('Volley', 'charged, every minute: two volleys of crayon arrows over every monster within 8 - 6 each, twice', 6, 'aoe', 8, [], ['minecraft:crit ~ ~1.4 ~ 0.3 0.3 0.3 0.2 8'], 'entity.arrow.shoot'),
        'kind': ('Lucky Bone', 'out of a fight beside you, every minute: he gives you a lucky bone - Luck and Haste', 0, 'you', 0, ['luck 120 0', 'haste 60 0'], [_d(0.94, 0.93, 0.88)], 'entity.skeleton.ambient')},
    'jockey': {
        'melee': ('Flap Charge', 'a foe within reach: a flapping charge - 5, knocked back', 5, 'near', 2.6, ['knock'], ['minecraft:cloud ~ ~0.4 ~ 0.3 0.1 0.3 0.02 6'], 'entity.chicken.hurt'),
        'ranged': ('Egg Toss', 'a foe 2.5-8 off, every 4 s: the baby zombie lobs a crayon egg - 4, slowed (it\'s sticky)', 4, 'shot', 8, ['slowness 2 1'], ['minecraft:item{item:{id:"minecraft:egg"}} ~ ~1 ~ 0.2 0.2 0.2 0.1 8'], 'entity.egg.throw'),
        'crowd': ('Peck Peck', 'two or more foes within 3, every 12 s: peck, peck, PECK - 4 each', 4, 'aoe', 3, [], ['minecraft:cloud ~ ~0.4 ~ 0.3 0.1 0.3 0.02 4'], 'entity.chicken.ambient'),
        'charged': ('Stampede', 'charged, every minute: a mad flapping stampede through every monster within 5 - 7 each, twice', 7, 'aoe', 5, ['knock'], ['minecraft:cloud ~ ~0.4 ~ 0.4 0.1 0.4 0.02 8'], 'entity.chicken.hurt'),
        'kind': ('Feather Fall', 'out of a fight beside you, every minute: a spare feather - Slow Falling and Speed for you', 0, 'you', 0, ['slow_falling 60 0', 'speed 30 0'], ['minecraft:cloud ~ ~1 ~ 0.3 0.3 0.3 0.02 6'], 'entity.chicken.egg')},
    'golem': {
        'melee': ('Iron Fist', 'a foe within reach: a big iron swing - 7', 7, 'near', 2.8, [], ['minecraft:crit ~ ~1 ~ 0.3 0.3 0.3 0.2 8'], 'entity.iron_golem.attack'),
        'ranged': ('Iron Toss', 'a foe 2.5-6 off, every 4 s: he stomps over and flings it up into the air - 6', 6, 'blink', 6, ['levitation 1 6'], ['minecraft:poof ~ ~0.3 ~ 0.4 0.1 0.4 0.02 8'], 'entity.iron_golem.attack'),
        'crowd': ('Ground Slam', 'two or more foes within 3.5, every 12 s: both fists into the ground - 6 each, slowed', 6, 'aoe', 3.5, ['slowness 3 1'], ['minecraft:poof ~ ~0.2 ~ 0.5 0.05 0.5 0.03 8'], 'entity.iron_golem.damage'),
        'charged': ('Big Toss', 'charged, every minute: every monster within 4 tossed sky-high - 9 each, twice', 9, 'aoe', 4, ['levitation 1 4'], ['minecraft:poof ~ ~0.3 ~ 0.5 0.1 0.5 0.03 10'], 'entity.iron_golem.attack'),
        'kind': ('A Poppy', 'out of a fight beside you, every minute: he gives you a crayon poppy - Regeneration II and Resistance', 0, 'you', 0, ['regeneration 8 1', 'resistance 30 0'], ['minecraft:heart ~ ~1.8 ~ 0.3 0.2 0.3 0 2'], 'entity.iron_golem.repair')},
    'axolotl': {
        'melee': ('Nibble', 'a foe within reach: a little nibble - 4', 4, 'near', 2.4, [], ['minecraft:bubble_pop ~ ~0.8 ~ 0.2 0.2 0.2 0 8'], 'entity.axolotl.attack'),
        'ranged': ('Bubble', 'a foe 2.5-8 off, every 4 s: a stream of crayon bubbles - 5, slowed', 5, 'shot', 8, ['slowness 2 1'], ['minecraft:bubble_pop ~ ~1 ~ 0.3 0.3 0.3 0 12'], 'entity.axolotl.splash'),
        'crowd': ('Splash', 'two or more foes within 3.5, every 12 s: a big splash - 4 each, weakened', 4, 'aoe', 3.5, ['weakness 3 0'], ['minecraft:splash ~ ~0.4 ~ 0.5 0.1 0.5 0 16'], 'entity.axolotl.splash'),
        'charged': ('Play Dead', 'charged, every minute: he flops over and plays dead - Regeneration II for you and him - then a bubble burst, 4 to every monster within 3', 4, 'aoe', 3, [], ['minecraft:bubble_pop ~ ~0.8 ~ 0.4 0.3 0.4 0 12'], 'entity.axolotl.idle_air'),
        'kind': ('Axolotl Hug', 'out of a fight beside you, every minute: a squishy hug - Regeneration and Water Breathing for you', 0, 'you', 0, ['regeneration 10 0', 'water_breathing 120 0'], ['minecraft:heart ~ ~1.8 ~ 0.3 0.2 0.3 0 3'], 'entity.axolotl.idle_air')},
    'enderman': {
        'melee': ('Swipe', 'a foe within reach: a long-armed swipe - 6', 6, 'near', 3.0, [], [_d(0.85, 0.42, 1.0)], 'entity.enderman.hurt'),
        'ranged': ('Blink', 'a foe 2.5-8 off, every 4 s: he blinks to its back in a ring of violet specks - and strikes, 8', 8, 'blink', 8, [], ['minecraft:portal ~ ~1 ~ 0.3 0.6 0.3 0.4 20'], 'entity.enderman.teleport'),
        'crowd': ('Stare', 'two or more foes within 4, every 12 s: the Stare - 3 each, and they freeze up (slowed hard)', 3, 'aoe', 4, ['slowness 3 3'], ['minecraft:reverse_portal ~ ~1 ~ 0.3 0.4 0.3 0.02 10'], 'entity.enderman.stare'),
        'charged': ('Void Rush', 'charged, every minute: he blinks through every monster within 5 - 9 each, twice, and they can\'t see straight', 9, 'aoe', 5, ['blindness 2 0'], ['minecraft:portal ~ ~1 ~ 0.4 0.6 0.4 0.4 24'], 'entity.enderman.teleport'),
        'kind': ('Grass Gift', 'out of a fight beside you, every minute: he hands you his crayon grass block - Haste and Night Vision', 0, 'you', 0, ['haste 60 0', 'night_vision 60 0'], [_d(0.35, 0.72, 0.29)], 'entity.enderman.ambient')},
}
_SPECK = {'zombie': _d(0.35, 0.66, 0.29, 1.2), 'skeleton': _d(0.94, 0.93, 0.88, 1.2), 'jockey': _d(0.98, 0.98, 0.96, 1.2), 'golem': _d(0.85, 0.82, 0.77, 1.2),
          'axolotl': _d(1.0, 0.66, 0.78, 1.2), 'enderman': _d(0.85, 0.42, 1.0, 1.2)}
FOE = 'type=#bm:hostile,tag=!bm.npc,tag=!bm.wil_body'
HOST = '@e[type=minecraft:wolf,tag=bm.ddpet]'


# ---------------------------------------------------------------------------------------------------- at phase235's import
def rename(C):
    """(phase235, before the dragon is registered) his new name, his words, his click box fitted per form"""
    C.NAME = MOB_NAME
    C.HELLO = ('(the Doodle Mob scrambles back to you, crayon flying)', '(a page flutters - and the Doodle Mob climbs out of it) "RAWR! ...or BRAINS! Or MOO? Hi!"',
               '(he folds himself back into a drawing, and is gone)')
    C.INTRO = [T('The Doodle Mob', DCOL, bold=True), T(' - Kettle\'s drawing, made real by the Gem. Kettle has started drawing him as every mob there is: ', 'gray'),
               T('hand him something of a mob\'s, and he scribbles himself into it.', 'white')]
    C.ADV = ('Here Be Dragons', 'Befriend the Doodle Mob, Kettle\'s drawing')
    C.BOX_FIT = True


def rows():
    """(phase235's import) his forms' rows in his wardrobe: locked - off - on"""
    import phase99 as P99
    P99.ROWS.setdefault('dragon', []).append(
        (CODES['dragon'], 'mf_dragon', 'Doodle Ender Dragon', '#9a6aff', 'Kettle\'s first big drawing - the black Ender Dragon. Hand him a bottle of dragon\'s breath to unlock it '
         '(you have it already if he joined you before the Doodle Mob). The Creeper and Crayon Green are this form\'s.',
         [(None, 'locked', 'dark_gray'), (f'entity @s[tag={END}]', 'off', 'gray'), (f'entity @s[tag={END}] unless score @s {SC} matches 1..', 'on', P99.GOLD)], 'p263/row/dragon'))
    for f in FORMS:
        item = HAND[f].split(':')[1].replace('_', ' ')
        need = f'Hand him {"an" if item[0] in "aeiou" else "a"} {item}' + (' - once he has killed a baby zombie' if f == 'jockey' else '') + ' to unlock it.'
        P99.ROWS['dragon'].append((CODES[f], f'mf_{SHORT[f]}', NAME[f], FCOL[f], f'The {NAME[f]}: {FA.NAMES[f]}. {need} His moves go {f} too.',
                                   [(None, 'locked', 'dark_gray'), (f'entity @s[tag={UN(f)}]', 'off', 'gray'), (f'score @s {SC} matches {K[f]}', 'on', P99.GOLD)],
                                   f'p263/row/{f}'))


# ---------------------------------------------------------------------------------------------------- the forms' poses on his rig
def fpose(f, pz, dur):
    """one pose of form f on the dragon's displays (tagged bm.ddsel): solved on the form's own pivots, each display shifted from
    the dragon's joint (where p235d/place puts it) to the form's; the form's 'fx' card is shown on his fire display"""
    F = FA.FORMS[f]
    S = DA.RIG_SCALE; U = S / 16
    xf = RK.solve(F.PIVOT, F.PARENT, pz)
    psel = lambda p: f'@e[type=minecraft:item_display,tag=bm.ddsel,tag=bm.ddp_{p}]'
    out = []
    for p in DA.PARTS:
        fp = 'fx' if p == 'fire' else p
        if p in ('slash', 'boom') or fp not in F.PARTS or F.HIDDEN(fp, pz):
            out.append(f'execute as {psel(p)} run data merge entity @s {{start_interpolation:0,interpolation_duration:{min(dur, 2)},transformation:{{scale:[0f,0f,0f]}}}}')
            continue
        q, t = xf[fp]
        a, b = RK.D(F.PIVOT[fp]), RK.D(DA.PIVOT[p])
        tr = [t[i] * U + (a[i] - b[i]) * U for i in range(3)]
        sc = round(S * F.PART_K.get(fp, 1.0), 4)
        out.append(f'execute as {psel(p)} run data merge entity @s {{start_interpolation:0,interpolation_duration:{dur},transformation:{{left_rotation:{snbt(RF.qf(q))},'
                   f'translation:[{tr[0]:.4f}f,{tr[1]:.4f}f,{tr[2]:.4f}f],scale:[{sc}f,{sc}f,{sc}f]}}}}')
    return out


DUR = {'idle_a': 16, 'idle_b': 14, 'walk_0': 4, 'walk_1': 4, 'atk_up': 3, 'atk': 2, 'sit_a': 14, 'sit_a2': 20, 'happy': 6}
# (state: (period or None, [(tick, pose)]) - as rigpet's: 0 idle, 1 walk, 2 run, 3 jump, 4 sit, 6 happy, 7/8/11/12/14 his moves, 10 swim)
ANIM = {0: (160, [(0, 'idle_a'), (80, 'idle_b')]), 1: (8, [(0, 'walk_0'), (4, 'walk_1')]), 10: (12, [(0, 'walk_0'), (6, 'walk_1')]),
        2: (6, [(0, 'walk_0'), (3, 'walk_1')]), 3: (None, [(0, 'walk_0')]), 4: (80, [(0, 'sit_a'), (40, 'sit_a2')]),
        16: (None, [(0, 'sit_a')]), 17: (None, [(0, 'sit_a')]), 6: (None, [(0, 'happy'), (12, 'idle_a')]),
        7: (None, [(0, 'atk_up'), (2, 'atk'), (6, 'idle_a')]), 8: (None, [(0, 'atk_up'), (5, 'atk'), (12, 'idle_a')]),
        11: (None, [(0, 'atk_up'), (4, 'atk'), (10, 'idle_a')]), 12: (None, [(0, 'atk_up'), (7, 'atk'), (14, 'atk_up'), (18, 'atk'), (26, 'idle_a')]),
        14: (None, [(0, 'happy'), (6, 'atk_up'), (11, 'atk'), (18, 'idle_a')])}


def generate(G):
    """(after phase235.generate) his forms: their dress, poses and cycles, his moves in each, the hand-ins, the rows, his old friends kept"""
    fn, title, tellraw = G.fn, G.title, G.tellraw
    import phase235 as P235
    import phase95 as FX
    import compsize as CS
    C, pfx = P235.Dragon, 'p235d'
    csay = lambda txt: title('@s', 'actionbar', [T(f'{MOB_NAME}: ', DCOL, bold=True), T(txt, C.LINE)])
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {SC} dummy'] + [f'scoreboard players set #{p} bm.rng {p}' for p in sorted({v[0] for v in ANIM.values() if v[0]})]
    G.OBJECTIVES.append(SC)
    psel = lambda p: f'@e[type=minecraft:item_display,tag=bm.ddsel,tag=bm.ddp_{p}]'
    mine = f'@e[type=minecraft:wolf,tag=bm.ddpet]'
    # ---- his old friends keep the Ender Dragon (it's on, and theirs); a new friend meets him, then he scribbles himself a zombie
    G.FUNCS['loop/second'].append(f'execute as @a[tag=bm.ddmet,tag=!{MOB}] run function bm:p263/old_friend')
    fn('p263/old_friend', [f'tag @s add {MOB}', f'tag @s add {END}', f'execute unless score @s {SC} matches 0.. run scoreboard players set @s {SC} 0'])
    G.FUNCS[f'{pfx}/enc/joined'][0:0] = [f'tag @s add {MOB}', f'tag @s add {UN("zombie")}', f'scoreboard players set @s {SC} 1', 'scoreboard players set @s bm.ddcr 0',
                                         'scoreboard players set @s bm.ddog 0',
                                         tellraw('@s', [T('Kettle: ', '#8ad8ff', bold=True), T('"Oh! Oh! I\'ve been practising MOBS! Look - "', '#d8f0ff'),
                                                        T(' (he scribbles over the dragon, and it\'s a zombie now - a happy crayon zombie, arms straight out)', 'gray', italic=True)])]
    # ---- his dress: after the dragon's own (Crayon Green, the Creeper), before the wardrobe's look - the form's cards, the host tagged
    D_ = G.FUNCS[f'{pfx}/dress']
    k = D_.index('scoreboard players set #wk bm.rng 0')
    tagl = [f'execute as {mine} if score @s bm.pid = #me bm.pid run tag @s remove {MF}{K[f]}' for f in FORMS] + [f'execute as {mine} if score @s bm.pid = #me bm.pid run tag @s remove {MF}']
    D_[k:k] = ['scoreboard players set #ddf bm.rng 0', f'execute as @a if score @s bm.pid = #me bm.pid run scoreboard players operation #ddf bm.rng = @s {SC}'] + tagl + \
              [f'execute if score #ddf bm.rng matches {K[f]} run function bm:p263/{SHORT[f]}/dress' for f in FORMS]
    for f in FORMS:
        F = FA.FORMS[f]
        lines = [f'execute as {mine} if score @s bm.pid = #me bm.pid run tag @s add {MF}', f'execute as {mine} if score @s bm.pid = #me bm.pid run tag @s add {MF}{K[f]}']
        for p in DA.PARTS:
            fp = 'fx' if p == 'fire' else p
            if fp in F.PARTS and F._els[fp]:
                lines.append(f'execute as {psel(p)} run data modify entity @s item.components."minecraft:item_model" set value "bm:{F.PREFIX}{fp}"')
        fn(f'p263/{SHORT[f]}/dress', lines + [f'execute as {mine} if score @s bm.pid = #me bm.pid run function bm:p263/{SHORT[f]}/box'])
        y0, h, x0, x1, z0, z1 = F.fit(F.POSES['idle_a'])
        fn(f'p263/{SHORT[f]}/box', CS.resize('bm.ddhit', round(max(0.7, (x1 - x0) * 0.85 + 0.1), 2), round(max(0.8, h + 0.15), 2)))
    fn('p263/box_dragon', CS.resize('bm.ddhit', *C.HIT))
    fn(f'{pfx}/box_fit', [f'execute if entity @s[tag={MF}{K[f]}] run return run function bm:p263/{SHORT[f]}/box' for f in FORMS])
    # ---- his animation: a form's own cycles (its poses on his displays), in place of the dragon's
    A_ = G.FUNCS[f'{pfx}/anim']
    A_[0:0] = [f'execute if entity @s[tag={MF}{K[f]}] run return run function bm:p263/{SHORT[f]}/anim' for f in FORMS]
    for f in FORMS:
        s = SHORT[f]
        F = FA.FORMS[f]
        for pose in {p for _per, fr in ANIM.values() for _t, p in fr}:
            fn(f'p263/{s}/pose/{pose}', fpose(f, F.POSES[pose], DUR.get(pose, 6)))
        top = []
        for st, (per, frames) in ANIM.items():
            L = [f'scoreboard players operation #f bm.rng = @s bm.dzfr'] + ([f'scoreboard players operation #f bm.rng %= #{per} bm.rng'] if per else [])
            L += [f'execute if score #f bm.rng matches {t} run function bm:p263/{s}/pose/{p}' for t, p in frames]
            fn(f'p263/{s}/anim/{st}', L)
            top.append(f'execute if score @s bm.dzs matches {st} run return run function bm:p263/{s}/anim/{st}')
        fn(f'p263/{s}/anim', top + [f'execute if score @s bm.dzfr matches 0 run function bm:p263/{s}/pose/idle_a'])
    # ---- his moves: each of his own goes the form's way while he wears one
    hit = lambda d: ['tag @s add bm.ddme', f'scoreboard players set #pd bm.rng {d}']
    end = ['tag @s remove bm.ddme', f'function bm:{pfx}/blow']
    for ev, fns in (('melee', ['melee']), ('ranged', ['ranged']), ('crowd', ['crowd']), ('charged', ['charged', 'charged2']), ('kind', ['kind'])):
        for fname in fns:
            G.FUNCS[f'{pfx}/{fname}'][0:0] = [f'execute if entity @s[tag={MF}{K[f]}] run return run function bm:p263/{SHORT[f]}/{fname}' for f in FORMS]
    for fname in ('ranged_tick', 'charged_tick'):
        G.FUNCS[f'{pfx}/{fname}'].insert(0, f'execute if entity @s[tag={MF}] run return 0')
    for f in FORMS:
        s = SHORT[f]
        for ev, (nm, _desc, dmg, how, r, eff, parts, sound) in FORM_MOVES[f].items():
            sn = f'playsound minecraft:{sound} neutral @a[distance=..16] ~ ~ ~ 0.8 1.3'
            at = [f'function bm:{pfx}/hurt'] if dmg else []
            for e in eff:
                if e == 'knock':
                    at.append(f'execute facing entity @e[type=minecraft:wolf,tag=bm.ddme,limit=1] feet rotated ~180 0 if block ^ ^ ^1.5 #bm:grap_pass if block ^ ^1 ^1.5 #bm:grap_pass run tp @s ^ ^ ^1.5')
                else:
                    at.append(f'effect give @s minecraft:{e}')
            at += [f'particle {p}' if ' ~' in p else f'particle {p} ~ ~1 ~ 0.3 0.4 0.3 0 8' for p in parts]
            if how != 'you':
                fn(f'p263/{s}/{ev}_at', at)
            near = f'@e[{FOE},distance=..{r + 0.4},sort=nearest,limit=1]'
            if how == 'you':
                body = [f'execute on owner if entity @s[distance=..8] run function bm:p263/{s}/{ev}_you']
                fn(f'p263/{s}/{ev}_you', [f'effect give @s minecraft:{e} true' for e in eff] + [f'particle {p}' for p in parts] +
                   [f'playsound minecraft:{sound} player @s ~ ~ ~ 0.6 1.4', 'execute unless entity @s[tag=bm.hush] run ' + csay(f'({nm}!)')])
            elif how == 'aoe':
                body = hit(dmg) + [f'execute as @e[{FOE},distance=..{r}] at @s run function bm:p263/{s}/{ev}_at', sn,
                                   f'particle {_SPECK[f]} ~ ~0.3 ~ {r / 2:.1f} 0.1 {r / 2:.1f} 0 30'] + end
            elif how == 'near':
                body = hit(dmg) + [f'execute as {near} at @s run function bm:p263/{s}/{ev}_at', sn] + end
            elif how == 'shot':
                trail = [f'particle {_SPECK[f]} ^ ^ ^{k} 0.05 0.05 0.05 0 2' for k in range(1, 8)]
                fn(f'p263/{s}/{ev}_trail', trail)
                body = hit(dmg) + [f'execute facing entity {near} eyes positioned ^ ^1 ^0.5 run function bm:p263/{s}/{ev}_trail',
                                   f'execute as {near} at @s run function bm:p263/{s}/{ev}_at', sn] + end
            else:                   # (blink: to its back - or as near as the ground lets him - then the blow)
                body = [f'execute as {near} at @s rotated as @s rotated ~ 0 positioned ^ ^ ^-1.2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run tp @e[type=minecraft:wolf,tag=bm.ddsel2b,limit=1] ~ ~ ~',
                        f'particle {_SPECK[f]} ~ ~1 ~ 0.3 0.5 0.3 0 16'] + hit(dmg) + \
                       [f'execute as @e[{FOE},distance=..{3.2},sort=nearest,limit=1] at @s run function bm:p263/{s}/{ev}_at', sn] + end
                body = ['tag @s add bm.ddsel2b'] + body + ['tag @s remove bm.ddsel2b']
            if f == 'axolotl' and ev == 'charged':
                body = ['effect give @s minecraft:regeneration 5 1 true', 'execute on owner if entity @s[distance=..12] run effect give @s minecraft:regeneration 5 1 true'] + body
            fn(f'p263/{s}/{ev}', body)
            if ev == 'charged':
                fn(f'p263/{s}/charged2', [] if f == 'axolotl' else body)
    # ---- his ways: the form's
    import phase28 as P28
    M = C.MENU
    for f in FORMS:
        pdlg = P28.multi([T(f"THE {NAME[f].upper()}'S WAYS", FCOL[f], bold=True)],
                         [P28.body([T(nm, FCOL[f], bold=True), T(f' - {d}.', 'gray')], 340) for nm, d, *_r in FORM_MOVES[f].values()],
                         [P28.btn([T('« Back', 'gray')], M + 5, width=150)], columns=1, exit_label='Close')
        fn(f'p263/{SHORT[f]}/powers', [f'scoreboard players set @s bm.menu {M}', f'dialog show @s {snbt(pdlg)}'])
    G.FUNCS[f'{pfx}/powers'][0:0] = [f'execute if score @s {SC} matches {K[f]} run return run function bm:p263/{SHORT[f]}/powers' for f in FORMS]
    # ---- the Creeper and Crayon Green are his dragon's: either turned on takes him out of a mob form
    for fname, sc in ((f'{pfx}/crf', 'bm.ddcr'), (f'{pfx}/form', 'bm.ddog')):
        F_ = G.FUNCS[fname]
        k = next(i for i, l in enumerate(F_) if l == 'scoreboard players operation #me bm.pid = @s bm.pid')
        F_.insert(k, f'execute if score @s {sc} matches 1 run scoreboard players set @s {SC} 0')
    G.FUNCS[f'{pfx}/cr/hand'].insert(1, f'scoreboard players set @s {SC} 0')
    # ---- the hand-ins (right-click him holding it: as the player, his host tagged bm.ddclk)
    W_ = G.FUNCS[f'{pfx}/who']
    k = next(i for i, l in enumerate(W_) if 'bm.pid = #me bm.pid run return run' in l)
    W_[k + 1:k + 1] = [f'execute if items entity @s weapon.mainhand {HAND[f]} run return run function bm:p263/hand/{f}' for f in FORMS] + \
                      [f'execute if items entity @s weapon.mainhand {DRAGON_HAND} run return run function bm:p263/hand/dragon']
    take = 'item modify entity @s weapon.mainhand {type:"minecraft:set_count",count:-1,add:true}'
    scribble = lambda f: [f'particle {_SPECK[f] if f != "dragon" else _d(0.6, 0.42, 1.0, 1.4)} ~ ~0.8 ~ 0.4 0.5 0.4 0 20',
                          __import__('phase235').item_particle('dd_fx_smoke', '~ ~0.8 ~', '0.4 0.5 0.4', 0.04, 10),
                          'playsound minecraft:item.book.page_turn neutral @a[distance=..16] ~ ~ ~ 1 1.2', 'playsound minecraft:entity.villager.work_cartographer neutral @a[distance=..16] ~ ~ ~ 0.6 1.4']
    for f in FORMS + ['dragon']:
        un = END if f == 'dragon' else UN(f)
        nm = 'Doodle Ender Dragon' if f == 'dragon' else NAME[f]
        hint = 'a bottle of dragon\'s breath' if f == 'dragon' else HAND[f].split(':')[1].replace('_', ' ')
        gate = []
        if f == 'jockey':
            gate = [f'execute unless entity @s[tag={un}] unless entity @s[tag={BZ}] run return run ' +
                    csay('(he looks at the egg, puzzled) "A chicken... and who rides it? I need to SEE one first." (Kill a baby zombie with him out.)')]
        first = ([f'item replace entity @s weapon.mainhand with minecraft:bucket',
                  f'execute at @e[type=minecraft:wolf,tag=bm.ddclk,limit=1] run summon minecraft:axolotl ~ ~0.5 ~ {{PersistenceRequired:1b}}',
                  f'execute at @e[type=minecraft:wolf,tag=bm.ddclk,limit=1] run particle minecraft:heart ~ ~1 ~ 0.4 0.4 0.4 0 6']
                 if f == 'axolotl' else [take])
        fn(f'p263/hand/{f}', gate + [f'execute if entity @s[tag={un}] run return run function bm:p263/to/{f}'] + first +
           [f'tag @s add {un}', tellraw('@s', [T(f'He takes the {hint.replace("a bottle of ", "")}, ', '#d4f4c8', italic=True), T('looks at it very hard - and scribbles himself over: ', 'gray', italic=True),
                                                T(f'the {nm}! ', FCOL.get(f, '#9a6aff'), bold=True), T('(Unlocked: switch in his wardrobe, or hand it to him again.)', 'gray')]),
            f'function bm:p263/to/{f}'])
        k_ = 0 if f == 'dragon' else K[f]
        fn(f'p263/to/{f}', [f'scoreboard players set @s {SC} {k_}', 'scoreboard players set @s bm.ddcr 0', 'scoreboard players set @s bm.ddog 0',
                            'scoreboard players operation #me bm.pid = @s bm.pid',
                            f'execute as {mine} if score @s bm.pid = #me bm.pid at @s run function bm:p263/now', csay(f'(he scribbles himself into the {nm})')])
        fn(f'p263/row/{f}', [f'execute unless entity @s[tag={un}] run return run function bm:p263/locked/{f}', f'function bm:p263/to/{f}',
                             'scoreboard players operation #me bm.pid = @s bm.pid',
                             f'execute as {mine} if score @s bm.pid = #me bm.pid run tag @s add bm.ddsel2', 'function bm:p99/menu/dragon', 'tag @e[tag=bm.ddsel2] remove bm.ddsel2'])
        fn(f'p263/locked/{f}', [say(f'Locked - hand him {hint}' + (' (once he has killed a baby zombie)' if f == 'jockey' else '') + ', and see what he draws himself as.', FCOL.get(f, '#9a6aff')),
                                'scoreboard players operation #me bm.pid = @s bm.pid',
                                f'execute as {mine} if score @s bm.pid = #me bm.pid run tag @s add bm.ddsel2', 'function bm:p99/menu/dragon', 'tag @e[tag=bm.ddsel2] remove bm.ddsel2'])
    fn('p263/now', [f'function bm:{pfx}/form2', 'function bm:p263/box_now', f'scoreboard players set @s bm.dzs -1'] + scribble('zombie') + FX.face_cmd('dragon', 'surprised', 20))
    fn('p263/box_now', [f'execute if entity @s[tag={MF}{K[f]}] run return run function bm:p263/{SHORT[f]}/box' for f in FORMS] + ['function bm:p263/box_dragon'])
    # ---- a baby zombie killed by one of his blows: the Chicken Jockey's egg will make sense to him now
    G.FUNCS[f'{pfx}/hurt'].append('execute if entity @s[type=#bm:p263_zombies] if data entity @s {IsBaby:1b} run function bm:p263/baby')
    fn('p263/baby', ['execute store result score #h bm.rng run data get entity @s Health', 'execute if score #h bm.rng matches 1.. run return 0',
                     f'execute as @e[type=minecraft:wolf,tag=bm.ddme,limit=1] on owner unless entity @s[tag={BZ}] run function bm:p263/baby_you'])
    fn('p263/baby_you', [f'tag @s add {BZ}', 'execute unless entity @s[tag=bm.hush] run ' + csay('"A baby zombie... riding a CHICKEN? Kettle drew one of those once!" (An egg will do it now.)')])
    G.wjson('bm/tags/entity_type/p263_zombies.json', {'values': ['minecraft:zombie', 'minecraft:husk', 'minecraft:drowned', 'minecraft:zombie_villager']})
    G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/doodle_forms', 'yellow'), T('  every Doodle Mob form unlocked', 'gray')]))
    fn('admin/doodle_forms', [f'tag @s add {UN(f)}' for f in FORMS] + [f'tag @s add {END}', f'tag @s add {BZ}', say('Every Doodle Mob form unlocked (his wardrobe).', DCOL)])


# ---------------------------------------------------------------------------------------------------- the resource pack
class _RecolArt:
    """(phase138.RECOL['dragon']) the dragon's recolour module, with every form's cards beside his own"""
    __name__ = 'f5art_doodlemob'

    def __getattr__(self, k):
        return getattr(DA, k)

    def textures(self):
        out = dict(DA.textures())
        for F in FA.FORMS.values():
            out.update(F.textures())
        return out


def recol_keys():
    """every form's textures but the Enderman's glowing eyes"""
    out = []
    for F in FA.FORMS.values():
        out += [n for n in F.textures() if not n.endswith('_eyes')]
    return tuple(out)


def own_sets():
    return {n: f'dm_{n[2:4]}' for n in recol_keys()}


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    names = set()
    for F in FA.FORMS.values():
        for name, (tex, els) in F.models().items():
            R.HATS[name] = (tex, els)
            names.add(name)
        R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (F.PREFIX,)
    import phase235 as P235

    def post(R2):
        mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
        for F in FA.FORMS.values():
            base = f'{F.PREFIX}head'
            cases = [{'when': e, 'model': mdl(f'{base}_x{FACE[e]}')} for e in P235.Dragon.EXPR if FACE.get(e) and f'{base}_x{FACE[e]}' in names]
            R2.wj(f'assets/bm/items/{base}.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0, 'cases': cases, 'fallback': mdl(base)}})
    R.POST.append(post)


def textures():
    out = {}
    for F in FA.FORMS.values():
        out.update(F.textures())
    return out


import sys as _sys  # noqa: E402
if FL.DOODLEMOB:
    _sys.modules['f5art_doodlemob'] = _RecolArt()

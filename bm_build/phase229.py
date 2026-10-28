"""2.97: HENRY AND NIA - two cats, the owner's own (nia_art.py / henry_art.py on cat_art_base.py; the machinery is rigpet's).
Henry is a black cat with a red collar and a silver tag; Nia a tortoiseshell with a lilac collar and a little gold bell.

Nia has passed away. She is honoured here as the owner asked: she comes to you on clear, starry nights - always first where Henry is,
because she was always waiting for him - and her bell carries her name: "In loving memory of Nia". Nothing in her story is sad to
play; she is simply, gently, there.

HENRY (Henry's Collar Tag)  he's found in a village at night, watching; offer him a fish (cod or salmon) and he's yours.
  (2.96c: a cat with flair and a temper - he fights.) SWIPE a foe within 2.2, every second (6) - or, annoyed, a BITE (8). POUNCE a
  foe 3-8 off, every 5 s (9). HISS two or more foes close, every 15 s: driven back, slowed and weakened (3). NINE LIVES FLURRY
  (charged, every minute): a choreographed flurry - onto a monster, swipe, swipe, rake, bite, a backflip onto the next (up to
  three), a landing and a strut; Luck II for you. With Bender beside him it's their DOG PILE instead (phase234): up onto Bender's
  back, fighting from there as Bender charges in, then off onto a monster as Bender bites it too. PURR out of a fight, every 45 s:
  Regeneration and Absorption for you. NIGHT PROWLER: by night his blows are harder (+2), and you see in the dark beside him.
NIA (Nia's Bell)  on a clear night under the open sky, with Henry beside you, now and then she's there in the grass - waiting for
  him. Stroke her (right-click) and she stays.
  (2.96c: gentle and cuddly - almost never scratching; a support follower.) COMFORT: in a fight, you hurt, every 4 s - she purrs
  against you (Regeneration, for your followers near too). GUARDIAN CURL: you at a third of your health, every minute - she runs to
  you and curls round your feet (Regeneration II, Resistance II, Absorption II). BELL CHIME (charged, every 45 s): you and your
  followers Regeneration II, Absorption for you; the monsters round her glow and slow - unhurt. SHOO: a soft hiss, pushing two or
  more foes back (no harm). GENTLE PAWS: only a monster that has just hurt her gets a soft swat (2). KNEAD out of a fight: Regeneration
  and a bite to eat. STARLIGHT: by night a soft starlight round her, soothing your followers.
THEIR BONDS: a pair with everyone (cat_bonds.py) - and her two special ones, with Emma ("The Princess's Kitty": every 30 s she
curls up in Emma's lap and a shower of petals heals you all) and with Queen Ava ("The Queen's Companion": every 30 s a glowing tide
heals you all, and the water lets you breathe). And the owner's eleven trios.
Every follower's list: sitting (a loaf, curled asleep), the collar wardrobe and a rare aura, a shiny collar, the Partner Wheel, a
frame, a display case, Cecil's doll, the honours (Champion blow and Piercing Blow), a Raid Contract."""
import math
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import nia_art as NA
import henry_art as HA
import rigpet as RP
import phase141 as P141
import phase134 as P134
import cat_bonds as CB

CYC = {0: (240, [(0, 'idle_a'), (60, 'idle_b'), (110, 'groom'), (150, 'idle_a'), (200, 'idle_b')]),
       1: (16, [(0, 'walk_0'), (4, 'walk_1'), (8, 'walk_2'), (12, 'walk_3')]),
       2: (12, [(0, 'run_0'), (3, 'run_1'), (6, 'run_2'), (9, 'run_3')]), 3: (None, [(0, 'jump')]),
       4: (480, [(0, 'sit_a'), (120, 'sit_b'), (240, 'sleep'), (420, 'sit_a')]),
       6: (None, [(0, 'happy'), (12, 'cuddle')]),
       7: (None, [(0, 'swipe_up'), (3, 'swipe')]),
       8: (None, [(0, 'pounce_up'), (6, 'pounce'), (14, 'idle_a')]),
       11: (None, [(0, 'hiss')]),
       12: (None, [(0, 'swipe_up'), (3, 'swipe'), (6, 'swipe_up'), (9, 'swipe'), (12, 'swipe_up'), (15, 'swipe'), (22, 'happy')]),
       14: (None, [(0, 'cuddle'), (10, 'knead_a'), (16, 'knead_b'), (22, 'knead_a'), (28, 'knead_b'), (34, 'cuddle')]),
       10: (16, [(2 * i, f'swim_{i}') for i in range(8)])}
DURS = {'idle_a': 20, 'idle_b': 16, 'groom': 14, 'walk_0': 4, 'walk_1': 4, 'walk_2': 4, 'walk_3': 4, 'run_0': 3, 'run_1': 3, 'run_2': 3, 'run_3': 3,
        'jump': 4, 'sit_a': 20, 'sit_b': 24, 'sleep': 30, 'happy': 6, 'cuddle': 10, 'swipe_up': 2, 'swipe': 2, 'pounce_up': 5, 'pounce': 3,
        'hiss': 4, 'knead_a': 5, 'knead_b': 5, 'hurt': 3}
FACE = {'happy': 'happy', 'surprised': 'alert', 'hurt': 'alert', 'sleepy': 'blink', 'blink': 'blink', 'squint': 'happy', 'serious': 'alert'}
# (2.96c) every cat curls up with Bender at night (17); then each their own: HENRY's bite (9), his flurry (15, played by its own clock -
#  the far-off frames only have its poses written out), on Bender's back (16) and their double act (18); NIA's bell (12), her comfort
#  (13) and her guardian curl (19)
CYC[17] = (120, [(0, 'sleep'), (60, 'sleep_b')])
_FL = ['pounce_up', 'pounce', 'rake', 'swipe_l', 'swipe_r', 'bite', 'land', 'strut'] + [f'flip_{k}' for k in range(4)]
H_CYC = dict(CYC)
H_CYC.update({9: (None, [(0, 'pounce_up'), (3, 'bite')]), 15: (None, [(0, 'pounce_up')] + [(9000 + i, p) for i, p in enumerate(_FL)]),
              16: (None, [(0, 'perch')]),
              17: (120, [(0, 'sleep_m'), (60, 'sleep_mb')]),     # (curled up on Bender's left: the curl mirrored, his head tucked in to him)
              18: (None, [(0, 'perch_hop')] + [(9100 + i, p) for i, p in enumerate(['perch', 'perch_l', 'perch_r', 'pounce', 'bite', 'land', 'strut'])])})
del H_CYC[12], H_CYC[14]
H_CYC[14] = CYC[14]
N_CYC = dict(CYC)
N_CYC.update({12: (None, [(0, 'happy'), (10, 'sit_a'), (22, 'happy')]), 13: (None, [(0, 'cuddle'), (10, 'happy')]),
              19: (None, [(0, 'run_1'), (6, 'cuddle'), (16, 'sleep'), (34, 'cuddle')])})
DURS.update({'swipe_l': 2, 'swipe_r': 2, 'rake': 3, 'bite': 2, 'land': 4, 'strut': 8, 'perch': 5, 'perch_l': 3, 'perch_r': 3, 'perch_hop': 3,
             'sleep_b': 30, 'sleep_m': 30, 'sleep_mb': 30, **{f'flip_{k}': 2 for k in range(4)}})
H_FACE = dict(FACE, serious='fierce', surprised='fierce')


class Henry(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'henry', 'Henry', CB.HENRY_C, CB.HENRY_LINE, 'p229', 'hy', 'hq'
    A = HA
    MENU = 4300
    PET_HP, PET_CD = 30, 120
    ITEM = 'henry_tag'
    pron, they = 'him', 'he'
    EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious')
    FACE = H_FACE
    ATTRS = dict(armor=2, attack_damage=5, movement_speed=0.4, follow_range=32, step_height=1.1)
    SCALE = 0.6
    HIT = (0.6, 0.7)
    CYCLE, DUR = H_CYC, DURS
    QUIPS = ['(Henry flicks his tail. That one\'s handled.)', '(Henry sits, and washes a paw, very pleased with himself.)', '(a low, satisfied "mrrp")',
             '(Henry looks back at you: did you see that?)', '(Henry yawns. Monsters are boring.)', '(slow blink. A cat\'s "I love you".)']
    HELLO = ('(Henry trots up with his tail high, and headbutts your leg)', '(Henry appears out of nowhere, the way black cats do. "Mrrp.")',
             '(Henry stretches, yawns, and saunters off home)')
    SIT = ('(Henry stands, stretches front and back, and is ready)', '(Henry folds himself into a loaf)')
    FAINT = '(Henry lies down, tired out)'
    NOT_YOURS = '(Henry looks at you. Henry looks away. Henry is somebody else\'s cat.)'
    POWERS = [('Swipe', 'a foe within 2.2, every second: 6 - and if it\'s really annoyed him, a bite instead (8)'),
              ('Pounce', 'a foe 3-8 off, every 5 s: a leap onto it (9)'),
              ('Hiss', 'two or more foes close, every 15 s: driven back, slowed and weakened (3)'),
              ('Nine Lives Flurry', 'charged, every minute: he leaps onto a monster - swipe, swipe, rake, bite (5, 7, 9) - backflips onto the next, up to three, and lands with a strut: Luck II for you'),
              ('Dog Pile', 'charged, instead, with Bender beside him: he springs onto Bender\'s back and fights from up there (6 a swipe) as Bender charges in - then leaps off onto a monster, Bender biting at the same moment (10). Bender holds his own charged moves for it'),
              ('Purr', 'out of a fight beside you, every 45 s: Regeneration and Absorption for you'),
              ('Night Prowler', 'by night his blows are harder (+2), and you see in the dark beside him')]
    INTRO = [T('Henry', CB.HENRY_C, bold=True), T(' - a black cat with a red collar and a silver tag. ', 'gray'),
             T('Lucky, whatever they say about black cats: he chose you.', 'white')]
    BUTTONS = ()
    BURST = ['particle minecraft:poof ~ ~0.3 ~ 0.3 0.2 0.3 0.02 8', 'particle minecraft:squid_ink ~ ~0.4 ~ 0.2 0.2 0.2 0.01 4']
    FADE_SOUND = 'playsound minecraft:entity.cat.ambient neutral @a[distance=..20] ~ ~ ~ 1 0.8'
    SUMMON_EXTRA = ['playsound minecraft:entity.cat.purreow neutral @a[distance=..24] ~ ~ ~ 0.8 0.9']
    ENC_POSES = [(0, 'sit_a'), (30, 'groom'), (60, 'idle_a')]
    ENC_PARTICLE = 'return 0'
    ADV = ('Black Cat', 'Win Henry over with a fish')
    ADMIN_HINT = 'In a village at night: offer him a cod or a salmon.'
    MEET_HINT = 'A village, at night. Bring a fish.'


class Nia(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'nia', 'Nia', CB.NIA_C, CB.NIA_LINE, 'p230', 'ni', 'nq'
    A = NA
    MENU = 4350
    PET_HP, PET_CD = 30, 120
    ITEM = 'nia_bell'
    pron, they = 'her', 'she'
    EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious')
    FACE = FACE
    ATTRS = dict(armor=2, attack_damage=1, movement_speed=0.4, follow_range=32, step_height=1.1)     # (2.96c: she hardly ever scratches)
    SCALE = 0.55
    HIT = (0.6, 0.7)
    CYCLE, DUR = N_CYC, DURS
    QUIPS = ['(Nia\'s bell jingles as she trots back to you)', '(Nia gives you a slow blink: all\'s well)', '(a small, proud "mew")',
             '(Nia washes behind one ear, entirely unbothered)', '(Nia flops over to show you her belly. It is a trap.)', '(Nia purrs)']
    HELLO = ('(Nia comes running, her bell jingling, and winds round your legs)', '(the grass rustles, a bell jingles, and Nia is there, purring)',
             '(Nia blinks at you slowly, and pads off under the stars)')
    SIT = ('(Nia uncurls, stretches, and is ready)', '(Nia tucks her paws in and settles down to knead)')
    FAINT = '(Nia curls up small, and rests)'
    NOT_YOURS = '(Nia sniffs your hand, kindly - but she\'s waiting for someone else)'
    POWERS = [('Comfort', 'in a fight, while you\'re hurt, every 4 s: she presses against you and purrs - Regeneration for you and your followers near'),
              ('Guardian Curl', 'you down to a third of your health, every minute: she runs to you and curls round your feet - Regeneration II, Resistance II and Absorption II'),
              ('Bell Chime', 'charged, every 45 s: you and your followers Regeneration II, and Absorption for you; the monsters round her glow and slow - she hurts none of them'),
              ('Shoo', 'two or more foes close, every 15 s: a soft hiss - they\'re pushed back and slowed, never hurt'),
              ('Gentle Paws', 'she almost never scratches: only a monster that has just hurt her gets a soft swat (2), at most every 8 s'),
              ('Knead', 'out of a fight beside you, every 45 s: Regeneration and a bite to eat'),
              ('Starlight', 'by night, a soft starlight round her - it soothes your followers near her')]
    INTRO = [T('Nia', CB.NIA_C, bold=True), T(' - a tortoiseshell with a lilac collar and a little gold bell. ', 'gray'),
             T('In loving memory of Nia: forever curious, forever loved.', 'white', italic=True)]
    BUTTONS = ()
    BURST = ['particle minecraft:end_rod ~ ~0.4 ~ 0.3 0.2 0.3 0.01 6', 'particle minecraft:poof ~ ~0.3 ~ 0.3 0.2 0.3 0.02 6']
    FADE_SOUND = 'playsound minecraft:block.amethyst_block.chime neutral @a[distance=..20] ~ ~ ~ 0.8 1.6'
    SUMMON_EXTRA = ['playsound minecraft:block.bell.resonate neutral @a[distance=..24] ~ ~ ~ 0.3 2.0',
                    'playsound minecraft:entity.cat.purr neutral @a[distance=..24] ~ ~ ~ 1 1.1']
    ENC_POSES = [(0, 'sleep'), (40, 'sit_a'), (70, 'cuddle')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 20 run particle minecraft:end_rod ~ ~0.6 ~ 0.4 0.3 0.4 0.005 3'
    ADV = ('Waiting Under the Stars', 'Find Nia, on a clear night, with Henry beside you')
    ADMIN_HINT = 'On a clear night under the open sky, with Henry beside you.'
    MEET_HINT = 'A clear, starry night, with Henry beside you.'


RP.register(Henry)
RP.register(Nia)
item('henry_tag', TOTEM, "Henry's Collar Tag", CB.HENRY_C,
     ['A little round silver tag, off a red collar.', 'It says HENRY on one side, and on the other: "If found, he\'s not lost - he\'s exploring."',
      ('Use: call Henry (again: call him over).', 'blue'), ('Sneak + use: his menu.', 'blue'), ('Swipes, bites, pounces, hisses - and purrs.', 'blue'),
      ('If he faints: 2 minutes before he can return.', 'gray')],
     model='bm:henry_tag', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
item('nia_bell', TOTEM, "Nia's Bell", CB.NIA_C,
     ['A little gold bell from a lilac collar.', 'It still rings, softly, when nobody touches it.', ('In loving memory of Nia.', 'light_purple'),
      ('Forever curious, forever loved.', 'light_purple'),
      ('Use: call Nia (again: call her over).', 'blue'), ('Sneak + use: her menu.', 'blue'), ('She comforts, she kneads - and her bell heals.', 'blue'),
      ('If she rests: 2 minutes before she can return.', 'gray')],
     model='bm:nia_bell', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
for _w, _nm, _c, _txt, _p, _s in (('henry', 'Henry', CB.HENRY_C, 'A doll of Henry - black as midnight, with his red collar.', 'minecraft:squid_ink', 'minecraft:entity.cat.ambient'),
                                  ('nia', 'Nia', CB.NIA_C, 'A doll of Nia - every one of her colours, and her little bell.', 'minecraft:end_rod', 'minecraft:entity.cat.purr')):
    item(f'doll_{_w}', TOTEM, f'{_nm} Doll', _c, [_txt, ('Right-click a block: set it down.', 'blue'), ('Right-click it: it twirls.', 'blue'),
                                                  ('Sneak + punch: pick it up.', 'gray')], model=f'bm:doll_{_w}', stack=16, cat='fun', comps=hold('none'))
    HOLD[f'doll_{_w}'] = f'bm:p141/doll_{_w}/use'
    P141.DOLLS.append((f'doll_{_w}', _nm, _c, _txt, _p, _s, 'minecraft:poof'))
P141.DOLL_FROM['doll_henry'] = ('henry_tag', {'kh': 1.55, 'kb': 0.82, 'kl': 0.62})
P141.DOLL_FROM['doll_nia'] = ('nia_bell', {'kh': 1.55, 'kb': 0.82, 'kl': 0.62})
P134.FIT['henry_tag'] = (0.0, 0.7, -0.3, 0.3, -0.55, 0.55)
P134.FIT['nia_bell'] = (0.0, 0.7, -0.3, 0.3, -0.55, 0.55)

# ---- THEIR BONDS: a pair with everyone (phase188 runs them) - and the trios (phase100)
import phase188 as P188
import phase100 as P100
_O = P188.O
P188.VNAME.update({'henry': 'Henry', 'nia': 'Nia'})


def fx_cmds(effects, secs=3):
    return [f'effect give {_O} minecraft:{e} {15 if e == "night_vision" else secs} {a} true' if e != 'saturation' else f'effect give {_O} minecraft:saturation 1 0 true'
            for e, a in effects]


def add_pairs():
    """(at the end of the imports: everyone who's registered by then gets a pair with each cat)"""
    for w, ((hn, hfx, hl, ha), (nn, nfx, nl, na)) in CB.B.items():
        if w not in P100.WHO: continue
        P188.PAIRS[f'hy_{w}'] = ('henry', w, hn, CB.HENRY_C, f'Henry and {P188.VNAME.get(w, w)}', fx_cmds(hfx), [(w, hl), ('henry', ha)],
                                 [('henry', '(Henry rubs against their leg and purrs)', w, '"...Alright, alright. Good cat."')])
        extra = ['scoreboard players add @s bm.p188 1', f'execute if score @s bm.p188 matches 30.. run function bm:{CB.SPECIAL[w]}',
                 'execute if score @s bm.p188 matches 30.. run scoreboard players set @s bm.p188 0'] if w in CB.SPECIAL else []     # (phase188 makes it the pair's own counter)
        extra = extra + [f'execute as {_O} at @s run function bm:p230/soothe']     # (2.96c: and she looks after your other followers too)
        P188.PAIRS[f'ni_{w}'] = ('nia', w, nn, CB.NIA_C, f'Nia and {P188.VNAME.get(w, w)}', fx_cmds(nfx) + extra, [(w, nl), ('nia', na)],
                                 [('nia', '(Nia\'s bell jingles as she trots over for a stroke)', w, '"Hello, little one."')])
        P188.ICON[f'hy_{w}'] = 'bm:henry_tag'; P188.ICON[f'ni_{w}'] = 'bm:nia_bell'
    tn, tfx, tl, ta = CB.TOGETHER
    P188.PAIRS['hy_nia'] = ('henry', 'nia', tn, CB.NIA_C, 'Henry and Nia, together again', fx_cmds(tfx), [('henry', tl), ('nia', ta)],
                            [('henry', '(Henry grooms the top of Nia\'s head)', 'nia', '(Nia purrs, eyes shut)'),
                             ('nia', '(Nia\'s bell jingles; Henry\'s ears turn to it, every time)', 'henry', '(Henry settles down beside her)')])
    P188.ICON['hy_nia'] = 'bm:nia_bell'
    for k, (nm, col, mem, fx) in CB.TRIOS.items():
        P100.TRIOS[k] = (nm, col, mem, nm, 'Walk with ' + ', '.join(P188.VNAME.get(m, m) for m in mem[:-1]) + ' and ' + P188.VNAME.get(mem[-1], mem[-1]) + ' at once')
        P188.ICON[k] = 'bm:nia_bell' if 'nia' in mem else 'bm:henry_tag'
    P100.BANTER.update(CB.BANTER)
    P100.VOICE.setdefault('Henry', (CB.HENRY_C, CB.HENRY_LINE)); P100.VOICE.setdefault('Nia', (CB.NIA_C, CB.NIA_LINE))


def extend_offers(O, offer):
    pass


def _icon(kind):
    """the summon items' icons (16 x 16, by hand): Henry's round silver tag on a red loop; Nia's gold bell on a lilac loop"""
    from PIL import Image, ImageDraw
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if kind == 'henry':
        d.arc((3, 0, 12, 7), 200, 340, fill=(200, 30, 40, 255), width=2)
        d.ellipse((4, 5, 11, 12), fill=(200, 205, 214, 255), outline=(110, 115, 125, 255))
        d.ellipse((5, 6, 8, 8), fill=(240, 244, 250, 255))
        d.line((6, 9, 9, 9), fill=(90, 95, 105, 255))
    else:
        d.arc((3, 0, 12, 7), 200, 340, fill=(190, 160, 230, 255), width=2)
        d.pieslice((3, 4, 12, 15), 180, 360, fill=(232, 182, 50, 255), outline=(150, 100, 20, 255))
        d.rectangle((3, 9, 12, 11), fill=(232, 182, 50, 255), outline=(150, 100, 20, 255))
        d.point((7, 12), fill=(120, 80, 10, 255)); d.point((5, 6), fill=(255, 240, 170, 255)); d.point((6, 6), fill=(255, 240, 170, 255))
    return im.resize((32, 32), 0)


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    RP.rp(Henry, R, _icon('henry'))
    RP.rp(Nia, R, _icon('nia'))


def textures():
    T_ = dict(HA.textures()); T_.update(NA.textures())
    return T_


def generate_early(G):
    RP.contract(Henry, G)
    RP.contract(Nia, G)


def _abilities(cat):
    """the cats' fighting - and how differently they go about it (2.96c): HENRY has flair and a temper - he swipes, bites, pounces
    and hisses, and his charged move is a choreographed flurry (or, with Bender beside him, their double act: phase234); NIA is
    gentle - she hardly ever scratches; she looks after you all (comfort, a guardian curl, her bell, a soft "shoo")"""
    def abilities(G, X):
        fn, S, go, end, face, foe, pfx = G.fn, X.S, X.go, X.end, X.face, X.foe, X.pfx
        idle = X.idle_fight
        lines = [f'execute if score @s {S("k")} matches 1.. run scoreboard players remove @s {S("k")} 1',
                 f'execute if score @s {S("k2")} matches 1.. run scoreboard players remove @s {S("k2")} 1']
        fn(f'{pfx}/near_owner', ['execute on owner if entity @s[distance=..6] run return 1', 'return 0'])
        fn(f'{pfx}/kind_go', go(14, 40, 'k', 900, face('happy', 40) + ['playsound minecraft:entity.cat.purr neutral @a[distance=..16] ~ ~ ~ 1 1']))
        if cat == 'henry':
            return lines + _henry(G, X, idle)
        return lines + _nia(G, X, idle)
    return abilities


def _hit(X, d):
    """(Henry) a blow of d - harder by night (Night Prowler)"""
    return X.hit(d) + ['execute if predicate bm:p229/night run scoreboard players add #pd bm.rng 2']


def _henry(G, X, idle):
    fn, S, go, end, face, foe, pfx = G.fn, X.S, X.go, X.end, X.face, X.foe, X.pfx
    lines = [f'execute {idle} unless score @s {S("gc")} matches 1.. if entity @e[{foe},distance=..8] if function bm:p234/duo/ok run function bm:p234/duo/go',
             f'execute {idle} unless score @s {S("gc")} matches 1.. if entity @e[{foe},distance=..6] run function bm:{pfx}/fl/go',
             f'execute store result score #nf bm.rng if entity @e[{foe},distance=..4]',
             f'execute {idle} unless score @s {S("k2")} matches 1.. if score #nf bm.rng matches 2.. run function bm:{pfx}/hiss_go',
             f'execute {idle} unless score @s {S("mc")} matches 1.. if entity @e[{foe},distance=..2.2] run function bm:{pfx}/swipe_go',
             f'execute {idle} unless score @s {S("rc")} matches 1.. unless entity @e[{foe},distance=..2.5] if entity @e[{foe},distance=..8] run function bm:{pfx}/pounce_go',
             f'execute {idle} unless score @s {S("k")} matches 1.. unless entity @e[{foe},distance=..12] if function bm:{pfx}/near_owner run function bm:{pfx}/kind_go']
    # SWIPE - and, one time in three, he bites instead (he's had enough)
    fn(f'{pfx}/swipe_go', ['execute store result score #r bm.rng run random value 1..3',
                           f'execute if score #r bm.rng matches 1 run return run function bm:{pfx}/bite_go'] +
       go(7, 6, 'mc', 20, ['playsound minecraft:entity.cat.hiss neutral @a[distance=..16] ~ ~ ~ 0.3 1.6']))
    fn(f'{pfx}/bite_go', go(9, 8, 'mc', 24, face('serious', 10) + ['playsound minecraft:entity.cat.hiss neutral @a[distance=..16] ~ ~ ~ 0.6 1.2']))
    fn(f'{pfx}/pounce_go', go(8, 16, 'rc', 100, face('serious', 14)))
    fn(f'{pfx}/hiss_go', go(11, 14, 'k2', 300, face('serious', 14) + ['playsound minecraft:entity.cat.hiss neutral @a[distance=..16] ~ ~ ~ 1 0.9']))
    fn(f'{pfx}/act_tick', [f'scoreboard players remove @s {S("x")} 1',
                           f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 3 run function bm:{pfx}/swipe',
                           f'execute if score @s {S("a")} matches 9 if score @s {S("x")} matches 4 run function bm:{pfx}/bite',
                           f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 4..10 run function bm:{pfx}/leap',
                           f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 3 run function bm:{pfx}/pounce',
                           f'execute if score @s {S("a")} matches 11 if score @s {S("x")} matches 10 run function bm:{pfx}/hiss',
                           f'execute if score @s {S("a")} matches 15 if score @s {S("x")} matches 2.. run function bm:{pfx}/fl/tick',
                           f'execute if score @s {S("a")} matches 18 if score @s {S("x")} matches 2.. run function bm:p234/duo/tick',
                           f'execute if score @s {S("a")} matches 14 if score @s {S("x")} matches 20 run function bm:{pfx}/kind'])
    fn(f'{pfx}/swipe', _hit(X, 6) + [f'execute as @e[{foe},distance=..2.6,sort=nearest,limit=1] at @s run function bm:{pfx}/swiped'] + end)
    fn(f'{pfx}/swiped', [f'function bm:{pfx}/hurt', 'particle minecraft:sweep_attack ~ ~0.6 ~ 0.1 0.1 0.1 0 1',
                         'playsound minecraft:entity.player.attack.sweep neutral @a[distance=..16] ~ ~ ~ 0.5 1.8'])
    fn(f'{pfx}/bite', _hit(X, 8) + [f'execute as @e[{foe},distance=..2.6,sort=nearest,limit=1] at @s run function bm:{pfx}/bitten'] + end)
    fn(f'{pfx}/bitten', [f'function bm:{pfx}/hurt', 'particle minecraft:crit ~ ~0.7 ~ 0.2 0.2 0.2 0.2 8',
                         'playsound minecraft:entity.player.attack.crit neutral @a[distance=..16] ~ ~ ~ 0.6 1.6'])
    fn(f'{pfx}/leap', [f'execute if entity @e[{foe},distance=1.4..9] facing entity @e[{foe},distance=..9,sort=nearest,limit=1] feet rotated ~ 0 '
                       f'positioned ^ ^ ^0.8 if block ~ ~ ~ #bm:grap_pass if block ~ ~0.6 ~ #bm:grap_pass run tp @s ~ ~ ~',
                       'particle minecraft:poof ~ ~0.2 ~ 0.1 0.05 0.1 0 1'])
    fn(f'{pfx}/pounce', _hit(X, 9) + [f'execute as @e[{foe},distance=..2.4,sort=nearest,limit=1] at @s run function bm:{pfx}/pounced'] + end)
    fn(f'{pfx}/pounced', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 2 1', 'particle minecraft:crit ~ ~0.8 ~ 0.3 0.3 0.3 0.2 10',
                          'playsound minecraft:entity.cat.hiss neutral @a[distance=..16] ~ ~ ~ 0.6 1.2'])
    fn(f'{pfx}/hiss', _hit(X, 3) + [f'execute as @e[{foe},distance=..4.5] at @s run function bm:{pfx}/hissed'] + end)
    fn(f'{pfx}/hissed', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 3 1', 'effect give @s minecraft:weakness 3 0',
                         f'execute facing entity @e[type=minecraft:wolf,tag={X.me},limit=1] feet rotated ~ 0 positioned ^ ^ ^-1.5 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~ ~',
                         'particle minecraft:angry_villager ~ ~1.4 ~ 0.2 0.1 0.2 0 1'])
    fn(f'{pfx}/kind', ['execute on owner if entity @s[distance=..8] run function bm:p229/purr_you'])
    fn('p229/purr_you', ['effect give @s minecraft:regeneration 10 0 true', 'effect give @s minecraft:absorption 30 0 true',
                         'particle minecraft:heart ~ ~1.2 ~ 0.3 0.3 0.3 0 3', 'playsound minecraft:entity.cat.purr player @s ~ ~ ~ 1 1'])
    flurry(G, X)
    return lines


FLURRY_CHAIN = 3


def flurry(G, X):
    """NINE LIVES FLURRY (2.96c; charged, every minute) - his own choreography, as Bender's Rage is his: a crouch and a leap onto a
    monster (fl/leap), clinging to its chest - swipe left, swipe right, a raking double, a bite (fl/combo: 5, -, 7, 9, harder by
    night) - then a backflip off it onto the next one near (fl/flip), up to FLURRY_CHAIN of them, and off the last a backflip
    away, a landing and a strut, tail high (fl/land): Luck II for you. His host is carried by hand (no gravity, no AI); the monster
    he's on is tagged bm.hyftg, those he's had bm.hyfhit. Phases (bm.hqfp): 1 leap, 2 combo, 3 flip to the next, 4 away and land;
    bm.hqft the ticks in one, bm.hqfn the monsters so far."""
    fn, S, foe, pfx, me = G.fn, X.S, X.foe, X.pfx, X.me
    objs = ['bm.hqfp', 'bm.hqft', 'bm.hqfn']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    T_ = '@e[tag=bm.hyftg,distance=..16,limit=1]'
    H = '@e[type=minecraft:wolf,tag=bm.hyfme,limit=1]'
    pose = lambda p: f'function bm:{pfx}/pose/{p}'
    step = lambda d: f'execute facing entity {T_} feet positioned ^ ^ ^{d} if block ~ ~ ~ #bm:grap_pass if block ~ ~0.4 ~ #bm:grap_pass run tp @s ~ ~ ~ ~ 0'
    fn(f'{pfx}/fl/go', [f'scoreboard players set @s {S("a")} 15', f'scoreboard players set @s {S("x")} 400', f'scoreboard players set @s {S("gc")} 1200',
                        'tag @e[tag=bm.hyfhit,distance=..32] remove bm.hyfhit', 'tag @e[tag=bm.hyftg,distance=..32] remove bm.hyftg',
                        f'tag @e[{foe},distance=..8,sort=nearest,limit=1] add bm.hyftg', 'tag @e[tag=bm.hyftg,distance=..8] add bm.hyfhit',
                        'scoreboard players set @s bm.hqfn 1', 'scoreboard players set @s bm.hqfp 1', 'scoreboard players set @s bm.hqft 0',
                        'data merge entity @s {NoGravity:1b,NoAI:1b,Motion:[0d,0d,0d]}',
                        'playsound minecraft:entity.cat.hiss neutral @a[distance=..24] ~ ~ ~ 1 0.8', 'particle minecraft:squid_ink ~ ~0.3 ~ 0.2 0.1 0.2 0.01 6'] +
       X.face('serious', 200) + ['execute on owner if entity @s[distance=..24,tag=!bm.hush] run ' + X.csay('(his ears go flat. His tail lashes once. Oh no.)')])
    fn(f'{pfx}/fl/tick', ['tag @s add bm.hyfme', f'function bm:{pfx}/fl/step', 'tag @s remove bm.hyfme'])
    fn(f'{pfx}/fl/step', ['scoreboard players add @s bm.hqft 1', 'data modify entity @s Motion set value [0d,0d,0d]',
                          f'execute if score @s bm.hqfp matches 1..3 unless entity {T_} run function bm:{pfx}/fl/next',
                          f'execute if score @s bm.hqfp matches 1 run function bm:{pfx}/fl/leap',
                          f'execute if score @s bm.hqfp matches 2 run function bm:{pfx}/fl/combo',
                          f'execute if score @s bm.hqfp matches 3 run function bm:{pfx}/fl/flip',
                          f'execute if score @s bm.hqfp matches 4 run function bm:{pfx}/fl/land',
                          f'execute if score @s bm.hqfp matches 1..3 if entity {T_} facing entity {T_} feet rotated ~ 0 run return run function bm:{pfx}/place',
                          f'execute rotated as @s rotated ~ 0 run function bm:{pfx}/place'])
    # the leap: down in a crouch, rear end wiggling - then off, paws out
    fn(f'{pfx}/fl/leap', [f'execute if score @s bm.hqft matches 1 run {pose("pounce_up")}', f'execute if score @s bm.hqft matches 5 run {pose("pounce")}',
                          'execute if score @s bm.hqft matches 2..4 run particle minecraft:poof ~ ~0.1 ~ 0.15 0.02 0.15 0.01 1',
                          'execute if score @s bm.hqft matches 5..7 if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~0.3 ~',
                          f'execute if score @s bm.hqft matches 5.. run {step(0.75)}',
                          f'execute if score @s bm.hqft matches 6.. as {T_} at @s if entity @e[type=minecraft:wolf,tag=bm.hyfme,distance=..1.4] run return run function bm:{pfx}/fl/latch_as',
                          f'execute if score @s bm.hqft matches 18.. run function bm:{pfx}/fl/latch'])
    fn(f'{pfx}/fl/latch_as', [f'execute as {H} at @s run function bm:{pfx}/fl/latch'])
    fn(f'{pfx}/fl/latch', ['scoreboard players set @s bm.hqfp 2', 'scoreboard players set @s bm.hqft 0', pose('rake'),
                           'playsound minecraft:entity.cat.hiss neutral @a[distance=..20] ~ ~ ~ 0.9 1.1'])
    # on it: clinging to its chest, his face to it - left, right, the rake, the bite
    # (a monster shrugs off a second blow inside half a second: the three that count land 11 ticks apart - the right paw between is a feint)
    hits = ((2, 'swipe_l', 1, 5), (None, 'swipe_r', 7, 0), (13, 'rake', 12, 7), (24, 'bite', 23, 9))
    fn(f'{pfx}/fl/combo', [f'execute as {T_} at @s facing entity {H} feet rotated ~ 0 anchored eyes positioned ^ ^ ^ positioned ~ ~-0.7 ~ positioned ^ ^ ^0.5 '
                           f'if block ~ ~ ~ #bm:grap_pass run tp {H} ~ ~ ~ facing entity @s feet'] +
       [f'execute if score @s bm.hqft matches {t} run {pose(p)}' for _h, p, t, _d in hits] +
       [f'execute if score @s bm.hqft matches {h} run function bm:{pfx}/fl/hit{d}' for h, _p, _t, d in hits if h] +
       [f'execute if score @s bm.hqft matches 30.. run function bm:{pfx}/fl/next'])
    for d in sorted({d for h, *_r, d in hits if h}):
        fn(f'{pfx}/fl/hit{d}', _hit(X, d) + [f'execute as {T_} at @s run function bm:{pfx}/fl/hurt', f'tag @s remove {me}'])
    fn(f'{pfx}/fl/hurt', [f'function bm:{pfx}/hurt', 'particle minecraft:sweep_attack ~ ~1 ~ 0.2 0.2 0.2 0 1', 'particle minecraft:crit ~ ~1.2 ~ 0.25 0.25 0.25 0.2 6',
                          'playsound minecraft:entity.player.attack.sweep neutral @a[distance=..16] ~ ~ ~ 0.5 1.9'])
    # the next: the nearest monster near he hasn't had - a backflip onto it; or (none left, or three done) the last flip, away
    fn(f'{pfx}/fl/next', ['scoreboard players set @s bm.hqft 0', 'tag @e[tag=bm.hyftg,distance=..32] remove bm.hyftg',
                          f'execute if score @s bm.hqfn matches {FLURRY_CHAIN}.. run return run function bm:{pfx}/fl/last',
                          f'tag @e[{foe},tag=!bm.hyfhit,distance=..7,sort=nearest,limit=1] add bm.hyftg',
                          f'execute unless entity {T_} run return run function bm:{pfx}/fl/last',
                          'tag @e[tag=bm.hyftg,distance=..8] add bm.hyfhit', 'scoreboard players add @s bm.hqfn 1', 'scoreboard players set @s bm.hqfp 3',
                          'playsound minecraft:entity.cat.ambient neutral @a[distance=..20] ~ ~ ~ 1 1.4'])
    fn(f'{pfx}/fl/last', ['scoreboard players set @s bm.hqfp 4', 'scoreboard players set @s bm.hqft 0',
                          'playsound minecraft:entity.cat.ambient neutral @a[distance=..20] ~ ~ ~ 1 1.2'])
    flips = [f'execute if score @s bm.hqft matches {1 + 2 * k} run {pose(f"flip_{k}")}' for k in range(4)]
    fn(f'{pfx}/fl/flip', flips + [f'execute if score @s bm.hqft matches 9 run {pose("pounce")}',
                                  'execute if score @s bm.hqft matches 1..4 if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~0.35 ~', step(0.7),
                                  f'execute if score @s bm.hqft matches 7.. as {T_} at @s if entity @e[type=minecraft:wolf,tag=bm.hyfme,distance=..1.4] run return run function bm:{pfx}/fl/latch_as',
                                  f'execute if score @s bm.hqft matches 18.. run function bm:{pfx}/fl/latch',
                                  'particle minecraft:squid_ink ~ ~0.3 ~ 0.1 0.1 0.1 0 1'])
    # away: backwards off it, over, and down - feet first, a crouch to take it, then the strut
    fn(f'{pfx}/fl/land', flips +
       ['execute if score @s bm.hqft matches 1..8 rotated as @s rotated ~ 0 positioned ^ ^ ^-0.3 if block ~ ~ ~ #bm:grap_pass if block ~ ~0.4 ~ #bm:grap_pass run tp @s ~ ~ ~',
        'execute if score @s bm.hqft matches 1..3 if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~0.3 ~',
        'execute if score @s bm.hqft matches 5..29 if block ~ ~-0.3 ~ #bm:grap_pass run tp @s ~ ~-0.3 ~',
        f'execute if score @s bm.hqft matches 5..29 unless block ~ ~-0.3 ~ #bm:grap_pass run function bm:{pfx}/fl/down',
        f'execute if score @s bm.hqft matches 24..29 run function bm:{pfx}/fl/down',
        f'execute if score @s bm.hqft matches 38 run {pose("strut")}',
        f'execute if score @s bm.hqft matches 58.. run function bm:{pfx}/fl/done'])
    fn(f'{pfx}/fl/down', ['scoreboard players set @s bm.hqft 30', 'data merge entity @s {NoGravity:0b}', pose('land'),
                          'particle minecraft:poof ~ ~0.1 ~ 0.2 0.03 0.2 0.02 6', 'playsound minecraft:entity.cat.ambient neutral @a[distance=..16] ~ ~ ~ 0.6 1.5'])
    fn(f'{pfx}/fl/done', [f'scoreboard players set @s {S("x")} 1', 'scoreboard players set @s bm.hqfp 0', 'data merge entity @s {NoGravity:0b,NoAI:0b}',
                          'tag @e[tag=bm.hyftg,distance=..32] remove bm.hyftg', 'tag @e[tag=bm.hyfhit,distance=..32] remove bm.hyfhit',
                          'execute on owner if entity @s[distance=..24] run effect give @s minecraft:luck 30 1 true',
                          'particle minecraft:squid_ink ~ ~0.4 ~ 0.3 0.2 0.3 0.02 10'] +
       X.face('happy', 40) + ['execute on owner if entity @s[distance=..24,tag=!bm.hush] run ' + X.csay('(he lands, flicks his tail, and strolls back without looking. He knows you saw.)')])
    # (a flurry cut short any way at all never leaves him without his wits)
    X.second.append(f'execute as @e[type=minecraft:wolf,tag={X.pet},nbt={{NoAI:1b}}] unless score @s bm.hqfp matches 1.. unless score @s bm.hqdp matches 1.. '
                    f'unless entity @s[tag=bm.rdr] unless entity @s[tag=bm.cdl] run data merge entity @s {{NoAI:0b,NoGravity:0b}}')


def _nia(G, X, idle):
    """NIA, the gentle one: she almost never scratches (only a monster that's just hurt her - a soft swat); she looks after you"""
    fn, S, go, end, face, foe, pfx = G.fn, X.S, X.go, X.end, X.face, X.foe, X.pfx
    lines = [f'execute {idle} unless score @s {S("gc")} matches 1.. if entity @e[{foe},distance=..8] run function bm:{pfx}/charge_go',
             f'execute {idle} unless score @s {S("bc")} matches 1.. if function bm:p230/owner_low run function bm:{pfx}/curl_go',
             f'execute {idle} unless score @s {S("sc")} matches 1.. if entity @e[{foe},distance=..12] if function bm:p230/owner_hurt run function bm:{pfx}/comfort_go',
             f'execute store result score #nf bm.rng if entity @e[{foe},distance=..4]',
             f'execute {idle} unless score @s {S("k2")} matches 1.. if score #nf bm.rng matches 2.. run function bm:{pfx}/shoo_go',
             f'execute {idle} unless score @s {S("mc")} matches 1.. unless data entity @s {{HurtTime:0s}} if entity @e[{foe},distance=..1.8] run function bm:{pfx}/swat_go',
             f'execute {idle} unless score @s {S("k")} matches 1.. unless entity @e[{foe},distance=..12] if function bm:{pfx}/near_owner run function bm:{pfx}/kind_go']
    # (you: hurt at all; low - a third of your health, or less)
    fn('p230/owner_hurt', ['execute on owner if entity @s[distance=..12] run return run function bm:p230/hurt_q', 'return 0'])
    fn('p230/hurt_q', ['execute store result score #h bm.rng run data get entity @s Health 10', 'execute store result score #mx bm.rng run attribute @s minecraft:max_health get 10',
                       'execute if score #h bm.rng < #mx bm.rng run return 1', 'return 0'])
    fn('p230/owner_low', ['execute on owner if entity @s[distance=..24] run return run function bm:p230/low_q', 'return 0'])
    fn('p230/low_q', ['execute store result score #h bm.rng run data get entity @s Health 10', 'execute store result score #mx bm.rng run attribute @s minecraft:max_health get 3.334',
                      'execute if score #h bm.rng <= #mx bm.rng run return 1', 'return 0'])
    fn(f'{pfx}/charge_go', go(12, 24, 'gc', 900, face('happy', 22)))
    fn(f'{pfx}/comfort_go', go(13, 16, 'sc', 80, face('happy', 16) + ['playsound minecraft:entity.cat.purr neutral @a[distance=..16] ~ ~ ~ 1 1.1']))
    fn(f'{pfx}/curl_go', go(16, 40, 'bc', 1200, face('surprised', 10) + ['playsound minecraft:entity.cat.purreow neutral @a[distance=..24] ~ ~ ~ 1 1.2']))
    fn(f'{pfx}/shoo_go', go(11, 14, 'k2', 300, face('serious', 14) + ['playsound minecraft:entity.cat.hiss neutral @a[distance=..16] ~ ~ ~ 0.5 1.4']))
    fn(f'{pfx}/swat_go', go(7, 6, 'mc', 160, []))
    fn(f'{pfx}/act_tick', [f'scoreboard players remove @s {S("x")} 1',
                           f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 3 run function bm:{pfx}/swat',
                           f'execute if score @s {S("a")} matches 11 if score @s {S("x")} matches 10 run function bm:{pfx}/shoo',
                           f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 21 run function bm:{pfx}/charge_a',
                           f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 9 run function bm:{pfx}/charge_b',
                           f'execute if score @s {S("a")} matches 13 if score @s {S("x")} matches 12 run function bm:{pfx}/comfort',
                           f'execute if score @s {S("a")} matches 16 if score @s {S("x")} matches 36.. run function bm:{pfx}/curl_run',
                           f'execute if score @s {S("a")} matches 16 if score @s {S("x")} matches 30 run function bm:{pfx}/curl',
                           f'execute if score @s {S("a")} matches 14 if score @s {S("x")} matches 20 run function bm:{pfx}/kind'])
    # GENTLE SWAT: only a monster that's just hurt her, right on top of her - a soft paw (2), and never more than once in 8 s
    fn(f'{pfx}/swat', X.hit(2) + [f'execute as @e[{foe},distance=..2.2,sort=nearest,limit=1] at @s run function bm:{pfx}/swatted'] + end)
    fn(f'{pfx}/swatted', [f'function bm:{pfx}/hurt', 'particle minecraft:sweep_attack ~ ~0.6 ~ 0.1 0.1 0.1 0 1'])
    # SHOO: a soft hiss - pushed back and slowed, never hurt
    fn(f'{pfx}/shoo', [f'execute as @e[{foe},distance=..4.5] at @s run function bm:{pfx}/shooed', 'particle minecraft:end_rod ~ ~0.5 ~ 0.6 0.2 0.6 0.02 6'])
    fn(f'{pfx}/shooed', ['effect give @s minecraft:slowness 3 1',
                         f'execute facing entity @e[type=minecraft:wolf,tag=bm.nipet,distance=..6,sort=nearest,limit=1] feet rotated ~ 0 positioned ^ ^ ^-1.5 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~ ~',
                         'particle minecraft:cloud ~ ~0.6 ~ 0.2 0.2 0.2 0.01 3'])
    # BELL CHIME (charged): her bell heals you all; the monsters round her glow and slow - and aren't hurt
    fn(f'{pfx}/charge_a', ['playsound minecraft:block.bell.use neutral @a[distance=..24] ~ ~ ~ 0.6 2.0', 'particle minecraft:end_rod ~ ~0.6 ~ 0.6 0.4 0.6 0.02 10'])
    fn(f'{pfx}/charge_b', [f'execute as @e[{foe},distance=..8] run function bm:{pfx}/chimed',
                           'scoreboard players operation #me bm.pid = @s bm.pid',
                           'execute as @a[distance=..24] if score @s bm.pid = #me bm.pid run function bm:p230/chime_you',
                           *[f'execute as @e[type=minecraft:{t},distance=..16] if score @s bm.pid = #me bm.pid run effect give @s minecraft:regeneration 8 1 true' for t in ('wolf', 'cat')],
                           'playsound minecraft:block.bell.resonate neutral @a[distance=..24] ~ ~ ~ 0.4 2.0',
                           'execute rotated 0 0 run particle minecraft:end_rod ~ ~0.5 ~ 2 0.3 2 0.01 30'])
    fn('p230/chime_you', ['effect give @s minecraft:regeneration 8 1 true', 'effect give @s minecraft:absorption 30 0 true'])
    fn(f'{pfx}/chimed', ['effect give @s minecraft:glowing 4 0', 'effect give @s minecraft:slowness 4 0'])
    # COMFORT (in a fight, you hurt, every 4 s): she presses against your legs and purrs
    fn(f'{pfx}/comfort', ['execute on owner if entity @s[distance=..12] at @s run function bm:p230/comfort_you',
                          'scoreboard players operation #me bm.pid = @s bm.pid',
                          *[f'execute as @e[type=minecraft:{t},distance=..8] if score @s bm.pid = #me bm.pid run effect give @s minecraft:regeneration 4 0 true' for t in ('wolf', 'cat')]])
    fn('p230/comfort_you', ['effect give @s minecraft:regeneration 4 0 true', 'particle minecraft:heart ~ ~1 ~ 0.3 0.3 0.3 0 2',
                            'playsound minecraft:entity.cat.purr player @s ~ ~ ~ 0.8 1.2'])
    # GUARDIAN CURL (you low, every minute): she runs to you and curls round your feet - you're held together till it passes
    fn(f'{pfx}/curl_run', ['execute on owner if entity @s[distance=1.5..24] at @s run tp @e[type=minecraft:wolf,tag=bm.nipet,tag=bm.nime,limit=1] ~ ~ ~',
                           'tag @s add bm.nime', 'execute on owner at @s run tp @e[type=minecraft:wolf,tag=bm.nime,limit=1] ^0.5 ^ ^0.4', 'tag @s remove bm.nime',
                           'particle minecraft:end_rod ~ ~0.4 ~ 0.2 0.2 0.2 0.01 2'])
    fn(f'{pfx}/curl', ['execute on owner if entity @s[distance=..24] at @s run function bm:p230/curl_you'])
    fn('p230/curl_you', ['effect give @s minecraft:regeneration 6 1 true', 'effect give @s minecraft:resistance 6 1 true', 'effect give @s minecraft:absorption 30 1 true',
                         'particle minecraft:heart ~ ~0.6 ~ 0.4 0.3 0.4 0 6', 'particle minecraft:end_rod ~ ~0.4 ~ 0.6 0.1 0.6 0.01 14',
                         'playsound minecraft:block.bell.resonate player @s ~ ~ ~ 0.4 1.8', 'playsound minecraft:entity.cat.purr player @s ~ ~ ~ 1 1',
                         'execute unless entity @s[tag=bm.hush] run ' + X.title('@s', 'actionbar', [T('Nia ', CB.NIA_C, bold=True), T('(curls round your feet, purring hard: you\'re not alone)', CB.NIA_LINE)])])
    fn(f'{pfx}/kind', ['execute on owner if entity @s[distance=..8] run function bm:p230/knead_you'])
    fn('p230/knead_you', ['effect give @s minecraft:regeneration 10 0 true', 'effect give @s minecraft:saturation 1 1 true',
                          'particle minecraft:heart ~ ~1.2 ~ 0.3 0.3 0.3 0 3', 'playsound minecraft:entity.cat.purr player @s ~ ~ ~ 1 1.2'])
    return lines


def generate(G):
    fn, wjson, tellraw, title = G.fn, G.wjson, G.tellraw, G.title
    G.wjson('bm/predicate/p229/night.json', {'condition': 'minecraft:time_check', 'clock': 'minecraft:overworld', 'value': {'min': 13000, 'max': 23000}, 'period': 24000})
    G.wjson('bm/predicate/p229/clear_night.json', {'condition': 'minecraft:all_of', 'terms': [
        {'condition': 'minecraft:time_check', 'clock': 'minecraft:overworld', 'value': {'min': 13000, 'max': 23000}, 'period': 24000},
        {'condition': 'minecraft:weather_check', 'raining': False},
        {'condition': 'minecraft:location_check', 'offsetY': 1.6, 'predicate': {'can_see_sky': True}}]})
    hsay = lambda txt: title('@s', 'actionbar', [T('Henry ', CB.HENRY_C, bold=True), T(txt, CB.HENRY_LINE)])
    nsay = lambda txt: title('@s', 'actionbar', [T('Nia ', CB.NIA_C, bold=True), T(txt, CB.NIA_LINE)])

    # ---- HENRY: in a village at night, watching; a fish wins him over
    def h_enc(G, X):
        X.second.append('execute as @a[tag=!bm.hymet,gamemode=!spectator] at @s if dimension minecraft:overworld if predicate bm:p229/night run function bm:p229/enc/check')
        fn('p229/enc/check', ['execute unless entity @e[type=minecraft:villager,distance=..32] run return 0',
                              'execute store result score #r bm.rng run random value 1..240', 'execute unless score #r bm.rng matches 1 run return 0',
                              'execute if entity @e[type=minecraft:interaction,tag=bm.hyenc,distance=..64] run return 0',
                              'execute positioned ^ ^ ^5 run function bm:p229/enc/place'])
        fn('p229/enc/place', ['execute if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass unless block ~ ~-1 ~ #bm:grap_pass run return run function bm:p229/enc/step',
                              'execute positioned ~ ~1 ~ if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run function bm:p229/enc/step'])
        fn('p229/enc/step', ['function bm:p229/enc/spawn', 'playsound minecraft:entity.cat.ambient neutral @a[distance=..24] ~ ~ ~ 1 0.8',
                             X.tellraw('@a[tag=!bm.hymet,distance=..16]', [T('Two yellow-green eyes in the dark: a black cat with a red collar is sitting in the lane, watching you. ', CB.HENRY_LINE, italic=True),
                                                                            T('His tag catches the moonlight.', 'gray', italic=True)])])
        fish = 'minecraft:cod', 'minecraft:salmon', 'minecraft:cooked_cod', 'minecraft:cooked_salmon'
        fn('p229/enc/talk', [f'execute if items entity @s container.* {X.holds("henry_tag")} run return run ' + hsay('(is already yours. He sits on your foot to prove it.)')] +
           [f'execute if items entity @s weapon.mainhand {f} run return run function bm:p229/enc/recruit' for f in fish] +
           [hsay('(sniffs your empty hand, and looks at you as if you\'ve forgotten something)'), 'playsound minecraft:entity.cat.ambient player @s ~ ~ ~ 1 1.2'])
        fn('p229/enc/recruit', ['item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
                                f'execute as {X.here} at @s run particle minecraft:heart ~ ~0.8 ~ 0.3 0.3 0.3 0 4',
                                f'execute as {X.here} at @s run playsound minecraft:entity.cat.eat neutral @a[distance=..16] ~ ~ ~ 1 1',
                                X.tellraw('@s', [T('He eats the fish delicately, washes his whiskers - and leaves his little silver tag at your feet. ', CB.HENRY_LINE, italic=True),
                                                 T('HENRY, it says. He\'s decided.', 'gray', italic=True)]),
                                'function bm:p229/enc/joined'])
    RP.build(Henry, G, _abilities('henry'), h_enc)

    # ---- NIA: a clear night under the sky, Henry beside you - she's waiting for him
    def n_enc(G, X):
        X.second.append('execute as @a[tag=!bm.nimet,tag=bm.hymet,gamemode=!spectator] at @s if dimension minecraft:overworld if predicate bm:p229/clear_night run function bm:p230/enc/check')
        fn('p230/enc/check', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #hy bm.rng 0',
                              'execute as @e[type=minecraft:wolf,tag=bm.hypet,distance=..16] if score @s bm.pid = #me bm.pid run scoreboard players set #hy bm.rng 1',
                              'execute if score #hy bm.rng matches 0 run return 0',
                              'execute store result score #r bm.rng run random value 1..180', 'execute unless score #r bm.rng matches 1 run return 0',
                              'execute if entity @e[type=minecraft:interaction,tag=bm.nienc,distance=..64] run return 0',
                              'execute positioned ^ ^ ^5 run function bm:p230/enc/place'])
        fn('p230/enc/place', ['execute if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass unless block ~ ~-1 ~ #bm:grap_pass run return run function bm:p230/enc/step',
                              'execute positioned ~ ~1 ~ if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run function bm:p230/enc/step'])
        fn('p230/enc/step', ['function bm:p230/enc/spawn', 'particle minecraft:end_rod ~ ~0.6 ~ 0.6 0.4 0.6 0.005 16',
                             'playsound minecraft:block.bell.resonate neutral @a[distance=..24] ~ ~ ~ 0.3 2.0',
                             X.tellraw('@a[tag=!bm.nimet,distance=..16]', [T('A little bell rings, somewhere in the grass. Henry stops dead, ears up - and runs. ', CB.NIA_LINE, italic=True),
                                                                            T('There, under the stars, a tortoiseshell cat is curled up, waiting. She was always waiting for him.', 'gray', italic=True)])])
        fn('p230/enc/talk', [f'execute if items entity @s container.* {X.holds("nia_bell")} run return run ' + nsay('(blinks at you slowly. She\'s right here.)'),
                             'function bm:p230/enc/recruit'])
        fn('p230/enc/recruit', [f'execute as {X.here} at @s run particle minecraft:end_rod ~ ~0.6 ~ 0.4 0.4 0.4 0.01 20',
                                f'execute as {X.here} at @s run playsound minecraft:entity.cat.purr neutral @a[distance=..16] ~ ~ ~ 1 1.1',
                                X.tellraw('@s', [T('You stroke her, and she leans into your hand, purring. Henry touches his nose to hers. ', CB.NIA_LINE, italic=True),
                                                 T('When she stands, there\'s a little gold bell in the grass where she lay - and she stays.', 'gray', italic=True)]),
                                X.tellraw('@s', [T('In loving memory of Nia. ', 'light_purple', italic=True), T('Forever curious, forever loved.', 'light_purple', italic=True)]),
                                'function bm:p230/enc/joined'])
    RP.build(Nia, G, _abilities('nia'), n_enc)

    # ---- NIGHT PROWLER (Henry): by night, Night Vision beside him; STARLIGHT (Nia): a soft starlight round her by night
    G.FUNCS['loop/second'] += ['execute as @e[type=minecraft:wolf,tag=bm.hypet,tag=!bm.ffpet] at @s if predicate bm:p229/night on owner if entity @s[distance=..16] run effect give @s minecraft:night_vision 15 0 true',
                               'execute as @e[type=minecraft:wolf,tag=bm.nipet,tag=!bm.ffpet] at @s if predicate bm:p229/night run function bm:p230/starlight']
    fn('p230/starlight', ['particle minecraft:end_rod ~ ~0.5 ~ 0.3 0.2 0.3 0.003 1', 'scoreboard players operation #me bm.pid = @s bm.pid',
                          'execute store result score #r bm.rng run random value 1..8', 'execute unless score #r bm.rng matches 1 run return 0',
                          *[f'execute as @e[type=minecraft:{t},distance=..8] if score @s bm.pid = #me bm.pid unless entity @s[tag=bm.nipet] run effect give @s minecraft:regeneration 3 0 true' for t in ('wolf', 'cat')]])
    # ---- NIA'S SPECIAL PAIRS (every 30 s): with Emma, she curls up in her lap - petals heal you all; with Queen Ava, a glowing tide
    fn('p230/sp/emma', [f'execute as {_O} at @s run function bm:p230/sp/heal',
                        'particle minecraft:cherry_leaves ~ ~1 ~ 1.2 0.6 1.2 0 40', 'playsound minecraft:entity.cat.purr neutral @a[distance=..16] ~ ~ ~ 1 1.2',
                        f'execute as {_O} unless entity @s[tag=bm.hush] run ' + title('@s', 'actionbar', [T('Emma: ', '#ff8ad8', bold=True), T('"She fell asleep in my lap again! Shh - nobody move."', '#ffd0ec')])])
    fn('p230/sp/ava', [f'execute as {_O} at @s run function bm:p230/sp/heal', f'execute as {_O} run effect give @s minecraft:water_breathing 60 0 true',
                       'particle minecraft:glow ~ ~0.5 ~ 1.5 0.3 1.5 0 30', 'particle minecraft:bubble ~ ~0.5 ~ 1.5 0.3 1.5 0.05 20',
                       f'execute as {_O} unless entity @s[tag=bm.hush] run ' + title('@s', 'actionbar', [T('Queen Ava: ', '#6ad8e8', bold=True), T('"Rest here, little one. The tide will keep you."', '#c8f4fa')])])
    # (2.96c) in any pair of hers, now and then: your followers near you soothed (Regeneration)
    fn('p230/soothe', ['execute store result score #r bm.rng run random value 1..4', 'execute unless score #r bm.rng matches 1 run return 0',
                       'scoreboard players operation #me bm.pid = @s bm.pid',
                       *[f'execute as @e[type=minecraft:{t},distance=..16] if score @s bm.pid = #me bm.pid run effect give @s minecraft:regeneration 4 0 true' for t in ('wolf', 'cat')]])
    fn('p230/sp/heal', ['effect give @s minecraft:regeneration 6 1 true', 'effect give @s minecraft:absorption 30 1 true',
                        'scoreboard players operation #me bm.pid = @s bm.pid',
                        *[f'execute as @e[type=minecraft:{t},distance=..16] if score @s bm.pid = #me bm.pid run effect give @s minecraft:regeneration 6 1 true' for t in ('wolf', 'cat')]])

    # ---- the trios (phase100 calls p100/<key> as the player)
    mine = lambda k: f'@e[type=minecraft:{P100.WHO[k][0]},tag={P100.WHO[k][1]},distance=..24]'
    REGEN = 'execute unless predicate bm:p100/regen run effect give @s minecraft:regeneration 5 0 true'
    for k, (nm, col, mem, fxs) in CB.TRIOS.items():
        fn(f'p100/{k}', [f'effect give @s minecraft:{e} {15 if e == "night_vision" else 3} {a} true' for e, a in fxs] +
           [f'execute as {mine(m)} if function bm:p100/is_mine run {REGEN}' for m in mem] + ['function bm:p100/banter_tick'])
        wjson(f'bm/advancement/story/trio_{k}.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
                                                     'display': {'icon': {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': P188.ICON[k]}},
                                                                 'title': T(nm, 'yellow'), 'description': T(P100.TRIOS[k][4], 'gray'), 'frame': 'goal', 'show_toast': True,
                                                                 'announce_to_chat': True, 'hidden': True}})


_O = P188.O

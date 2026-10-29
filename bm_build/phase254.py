"""3.0: THE KEEPER OF BONDS - the 51st follower, and the last: a spirit woven from the threads of every bond you've made
(keeper_art.py draws it; tools/preview/keeper.py previews it). Its home is the Loom Sanctuary (phase253): once you have met
every other follower the Compass of Bonds is yours, and the sanctuary is woven into the sky.

THE MEETING  whenever someone with the Compass (bm.kbcomp) is on the island and hasn't its thread yet (bm.tkmet), the Keeper
             stands on the dais at bm.kb_spawn, working its loom (tend_a / tend_b; it turns to you as you come near). Speak to it:
             a short send-off - it counts your friends ("fifty threads"), bows, weaves the last thread, and gives you the Bond
             Thread (its summoning item) - once. Anyone without the Compass who somehow stands before it is turned gently away.
             (The Compass needs everyone - the hard-mode followers too - so in practice the Keeper is a hard-mode world's.)

  TUG          a foe 2.5 to 10 off, every 3 s: a thread cast out, and the foe yanked in toward it (5).
  MEND         you, hurt in a fight, every 10 s: you and every follower of yours near (16) - Instant Health and Regeneration II.
  THE WEAVE    (charged, every minute) a web of threads over every foe within 8: bound (held fast, weakened), 7 - and as the
               web is pulled tight, 6 more.
  GIFT         out of a fight beside you, every minute: a small gift - a little useful thing, or a kindness.
  BOND         its passive: each of your OTHER followers out near you (16) is a thread pulled taut - one: Luck; two: and
               Regeneration; three (the most there can be: see the Fourth Thread): and Resistance and Strength. From two on,
               your followers near it hit a little harder (Strength) too.
  THE FOURTH THREAD (3.0e)  it is never counted among your followers: phase58's limit of three (p58/count) leaves it out,
               and its own call (try_summon, the meeting's "it joins you") never asks p58/full - so with it out, three others
               can walk with you too, four in all; and it comes whatever else is out. Every other way of calling a follower
               (the Partner Wheel, Keep up, a heist's comeback) goes through try_summon, so they agree. (The vault's own Raid
               Crew size - one each in a party, two alone - is a different rule: there it counts as anyone does.)
  LIFELINE (3.0e)  out and within 24 of you, once a Minecraft day (phase51's sunrise count, #day bm.bm): a blow that would
               kill you, its thread catches - you live, at 1 health, with Regeneration II and a little Absorption, a burst of
               rainbow threads and a word from it; then it rests until the next dawn (bm.qbld: the day it caught you). How:
               the game's own death protection, which only a hand can hold - so while it's ready and your OFF HAND IS EMPTY,
               an unseen thread (keeper_lifeline: death_protection, its model nothing but the totem flash - the Bond Thread
               - no tooltip, Curse of Vanishing) rests there, given up the moment you put anything in that hand (and swept
               from anywhere else it ends up). With the off hand full it can't rest there: then it catches you at the BRINK
               instead - two hearts or less after a hit - which a single blow from higher can't be caught by. Like a totem,
               nothing catches the void or /kill. Its menu shows "Lifeline: ready" or "resting until dawn".
SUNLIT (3.0d)  its costume, a row of its wardrobe (code 5288, free with it, as every follower's form is): its hood down - pearl
             hair in a high ponytail, a sunburst behind its head (rigpet's FORM on the head and body: keeper_art's '_h' models).
Its motes - the bonds - spin slowly round it (right_rotation about y, on the two ring displays; every pose's own small turn
rides on top). Everything else is every follower's: sitting, a wardrobe (its cloth's colour, per look), a rare aura (rainbow
threads), a shiny (a starlit weave), the Partner Wheel, a frame, a display case, Cecil's doll, the honours, a Raid Contract;
pairs with Bender, Mr. Capshun, Henry and Nia."""
import math
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, F, B, Int
import keeper_art as KA
import rigfol as RF
import rigpet as RP
import rigface as RF2
import phase141 as P141
import phase134 as P134
import phase235 as P235
import phase253 as P253

COL, LINE = '#ffd6f0', '#fff4e0'
GOLD = '#ffd878'
SPIN_N = 24                                     # (the motes' spin: SPIN_N steps a turn, one a second)
SEQ_END = 120                                   # (the send-off: ticks from the first word to the thread in your hands)

item('bond_thread', TOTEM, 'The Bond Thread', COL,
     ['A spool of golden thread, wound in every colour', 'of every friend you have walked beside.',
      ('Woven by the Keeper of Bonds, for you alone.', 'light_purple'),
      ('Use: call the Keeper (again: call it over).', 'blue'), ('Sneak + use: its menu.', 'blue'), ('A tug, a mending, and THE WEAVE.', 'blue'),
      ('The Fourth Thread: it never counts among', 'blue'), ('your three followers - four can walk with you.', 'blue'),
      ('Lifeline: once a day, near you, its thread', 'blue'), ('catches a blow that would kill you.', 'blue'),
      ('If it faints: 2 minutes before it can return.', 'gray')],
     model='bm:bond_thread', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)


class Keeper(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'keeper', 'The Keeper of Bonds', COL, LINE, 'p254', 'tk', 'qb'
    A = RF2.art(KA)
    MENU, PET_HP, PET_CD, ITEM = 5250, 40, 120, 'bond_thread'
    pron, they = 'it', 'it'
    FACE = dict(KA.FACE_MAP)
    ATTRS = dict(armor=6, attack_damage=4, movement_speed=0.36, follow_range=32, step_height=1.1)
    SCALE, HIT = 1.0, (0.9, 2.2)                # (3.0c: it stands 2.14 tall now - was 2.34)
    # (3.0d) SUNLIT - its costume, a row of its wardrobe (free with it, as every follower's form is): the hood down. rigpet's FORM:
    #        bm.qbhd on the owner picks the '_h' models of KA.HOOD_PARTS (the head - a model per face - and the body's cowl);
    #        the wardrobe's looks ride on top (phase138's '_c<k>', the hair recoloured with the cloth); the figurine, the doll
    #        and the frame keep the hood up
    FORM = ('bm.qbhd', KA.HOOD_SFX, 'Sunlit', None, '(it lowers its hood - pearl hair, combed back tight, and a sunburst of light behind it)',
            '(it draws its hood up again, and the sunlight folds away inside it)',
            'Its hood down: hair of pearl in a high ponytail, a sunburst of light behind its head.')
    FORM_PARTS = KA.HOOD_PARTS
    FORM_WARDROBE = (5288, GOLD, 'Sunlit - its hood down: hair of pearl in a high, tight ponytail, and a sunburst of light behind its head. '
                                 'Every look and every face still on it. On or off here.')
    CYCLE = P235.cycle((240, [(0, 'idle_a'), (80, 'idle_b'), (160, 'idle_c'), (210, 'idle_a')]), (240, [(0, 'sit_a'), (120, 'sit_b')]),
                       (None, [(0, 'happy')]),
                       {8: (None, [(0, 'tug_up'), (6, 'tug'), (14, 'idle_a')]),
                        12: (None, [(0, 'weave_up'), (6, 'weave'), (14, 'weave_hold'), (30, 'weave_end'), (38, 'idle_a')]),
                        13: (None, [(0, 'mend_a'), (6, 'mend'), (18, 'idle_a')]),
                        14: (None, [(0, 'gift'), (16, 'happy'), (28, 'idle_a')])})
    DUR = dict(P235._DUR, tug_up=4, tug=2, weave_up=6, weave=6, weave_hold=8, weave_end=8, mend_a=4, mend=6, gift=8,
               tend_a=30, tend_b=30, bow=12, rise=10)
    QUIPS = ['(it hums, and the motes round it turn a little faster)', '"Every one of them is still with you. I can feel the threads."',
             '(it tucks a loose thread back into its sleeve, very carefully)', '"You walk so far. The tapestry keeps getting longer."',
             '(its eyes of light crinkle into happy little crescents)', '"Shall I tell you a secret? Emma\'s thread was the first."']
    HELLO = ('(the Keeper glides back to your side, the motes round it settling)', '(a thread of light draws itself out of the air - and the Keeper of Bonds is there, its loom aglow)',
             '(it bows, unravels into a hundred bright threads, and is gone)')
    SIT = ('"Shall we go on? There are always more threads."', '(it kneels on its robe, folds its wings, and weaves a little while it waits)')
    FAINT = '"Only a loose thread... I will mend it..."'
    NOT_YOURS = '(it bows to you, kindly - but its thread runs to somebody else)'
    POWERS = [('Tug', 'a foe 2.5 to 10 off, every 3 s: a thread cast out - the foe yanked in toward it, 5'),
              ('Mend', 'you, hurt in a fight, every 10 s: you and every follower of yours near - Instant Health and Regeneration II'),
              ('The Weave', 'charged, every minute: a web of threads over every foe within 8 - bound fast and weakened, 7, and 6 more as it pulls tight'),
              ('Gift', 'out of a fight beside you, every minute: a small gift - a little useful thing, or a kindness'),
              ('Bond', 'each of your other followers out near you is a thread pulled taut: Luck, then Regeneration, and with three Resistance and Strength - '
                       'and from two on, your followers near it hit a little harder'),
              ('The Fourth Thread', 'it is never counted among your followers: with it out, three others can walk with you too - four in all'),
              ('Lifeline', 'out and within 24 of you, once a day: a blow that would kill you, its thread catches instead - you live, with Regeneration and a '
                           'little Absorption; then it rests until dawn. (It rests in an empty off hand, unseen; with that hand full it can only catch you at '
                           'the brink - two hearts or less)'),
              ('The Motes', 'fifty bonds circle it, each a friend\'s colour - slowly, always')]
    INTRO = [T('The Keeper of Bonds', COL, bold=True), T(' - woven from the threads of every bond you have made. ', 'gray'),
             T('The more friends beside you, the stronger it holds.', LINE, italic=True)]
    BURST = ['particle minecraft:end_rod ~ ~1.2 ~ 0.4 0.7 0.4 0.04 20', 'particle minecraft:dust{color:[1.0,0.84,0.94],scale:1.1} ~ ~1.2 ~ 0.5 0.7 0.5 0 12',
             'particle minecraft:dust{color:[0.6,0.8,1.0],scale:0.9} ~ ~1.4 ~ 0.5 0.7 0.5 0 8']
    FADE_SOUND = 'playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..20] ~ ~ ~ 0.8 1.4'
    SUMMON_EXTRA = ['playsound minecraft:block.amethyst_block.chime neutral @a[distance=..24] ~ ~ ~ 1 0.9',
                    'playsound minecraft:entity.allay.ambient_with_item neutral @a[distance=..24] ~ ~ ~ 0.7 1.2']
    ENC_POSES = [(0, 'tend_a'), (40, 'tend_b')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 20 run particle minecraft:end_rod ~ ~1.6 ~ 0.4 0.4 0.4 0.01 3'
    ADV = ('The Keeper of Bonds', 'Meet every friend there is to meet - and take the last thread from the Loom Sanctuary')
    ADMIN_HINT = 'Meet every other follower: the Compass of Bonds leads to the Loom Sanctuary in the sky, where it waits.'
    MEET_HINT = 'Meet every other follower, and follow the Compass of Bonds into the sky.'


RP.register(Keeper)
RF2.setup(Keeper, 'head')

_DOLL = 'A doll of the Keeper of Bonds - a big hood with two smiling eyes of light and a glowing blush, a little rainbow robe, and six tiny wings.'
item('doll_keeper', TOTEM, 'Keeper of Bonds Doll', COL, [_DOLL, ('Right-click a block: set it down.', 'blue'), ('Right-click it: it twirls.', 'blue'),
                                                         ('Sneak + punch: pick it up.', 'gray')], model='bm:doll_keeper', stack=16, cat='fun', comps=hold('none'))
HOLD['doll_keeper'] = 'bm:p141/doll_keeper/use'
P141.DOLLS.append(('doll_keeper', Keeper.NAME, COL, _DOLL, 'minecraft:end_rod', 'minecraft:block.amethyst_block.chime', 'minecraft:poof'))
P141.DOLL_FROM['doll_keeper'] = ('bond_thread', dict(KA.DOLL))         # (the default chibi warp; the skirt shortened as legs would be)
P134.FIT['bond_thread'] = KA.FIT                                        # (idle_a at RIG_SCALE)

# ---- its pairs with Bender and Mr. Capshun (Henry's and Nia's: cat_bonds)
import phase188 as P188
_O = P188.O
_eff = lambda *es: [f'effect give {_O} minecraft:{e} 3 {a} true' for e, a in es]
P188.VNAME.update({'keeper': 'the Keeper of Bonds'})
P188.PAIRS.update({
    'tk_bender': ('keeper', 'bender', 'The Goodest Thread', '#e0a860', 'The Keeper of Bonds and Bender - one of the very first threads, and one of the brightest',
                  _eff(('speed', 0), ('regeneration', 0)),
                  [('bender', '(chases a mote round and round it, tail going like mad)'), ('keeper', '"Yes, that one is yours. The brightest gold in the whole loom."')],
                  [('keeper', '(it ties a loose thread round his collar in a little bow)', 'bender', '(sits very straight. He is so proud.)')]),
    'tk_capshun': ('keeper', 'capshun', 'The Last Chapter', '#f0f0f0', 'The Keeper of Bonds and Mr. Capshun - the narrator, and the one who keeps every story',
                   _eff(('luck', 0), ('haste', 0)),
                   [('capshun', '[Mr. Capshun narrates: "And at the end of every story, a loom - and every thread of it, a friend."]'), ('keeper', '"You tell it well. I only weave it."')],
                   [('capshun', '[Mr. Capshun narrates: "He tried to count the threads. He lost count. He started again, happily."]', 'keeper', '"Fifty. Fifty-one, now - counting me."')]),
})
P188.ICON.update({'tk_bender': 'bm:bond_thread', 'tk_capshun': 'bm:bond_thread'})


def extend_offers(O, offer):
    pass


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    RP.rp(Keeper, R, KA.icon_bond_thread())
    RF2.faces(Keeper, 'head', R)

    def post(R2):                               # (the iridescent strips - wings, pearl cloth, gold trim: their .png.mcmeta, as mire_art's post pass writes them)
        for path, meta in KA.mcmeta().items():
            R2.wj(path, meta)
    R.POST.append(post)

    def post_ll(R2):                            # (3.0e) LIFELINE's unseen thread: nothing in the hand or the slot - the Bond Thread only in the totem flash (FIXED)
        R2.wj('assets/bm/items/keeper_lifeline.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:display_context',
                                                                 'cases': [{'when': 'fixed', 'model': {'type': 'minecraft:model', 'model': 'bm:item/bond_thread'}}],
                                                                 'fallback': {'type': 'minecraft:empty'}}})
    R.POST.append(post_ll)


def textures():
    return KA.textures()                        # (its own kb_* textures; the wings, the pearl cloth and its trim are animated strips - rp's post writes their .mcmeta)


def generate_early(G):
    RP.contract(Keeper, G)


def _words(n):
    ones = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen',
            'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
    tens = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
    if n < 20: return ones[n]
    return tens[n // 10] + ('' if n % 10 == 0 else '-' + ones[n % 10])


def _q(deg):
    h = math.radians(deg) / 2
    return [F(0.0), F(round(math.sin(h), 5)), F(0.0), F(round(math.cos(h), 5))]


def _followers(cmd, r=16):
    """(as anyone, #me bm.pid set) the lines running cmd as each of the owner's OTHER followers out within r"""
    return [f'execute as @e[type=minecraft:{t},tag=!bm.tkpet,tag=!bm.ffpet,distance=..{r}] if score @s bm.pid = #me bm.pid at @s run {cmd}' for t in ('wolf', 'cat')]


def _abilities(G, X):
    fn, pfx, foe, me = G.fn, X.pfx, X.foe, X.me
    snd = lambda s, v=0.6, p=1.0: f'playsound minecraft:{s} neutral @a[distance=..16] ~ ~ ~ {v} {p}'
    K = dict(ranged=dict(st=8, x=14, at=7, cd=60, near=2.5, far=10, face='serious', go=[snd('entity.fishing_bobber.throw', 0.8, 1.4)]),
             charged=dict(st=12, x=38, at=[26, 10], cd=1200, r=8, face='serious', during=(11, 25), go=[snd('block.amethyst_block.resonate', 1.0, 0.7)]),
             support=dict(st=13, x=18, at=9, cd=200, face='happy'),
             kind=dict(st=14, x=30, at=15, cd=1200, face='happy'))
    lines = P235.kit(G, X, K)
    thread = lambda r, g, b: f'particle minecraft:dust{{color:[{r},{g},{b}],scale:0.6}} ~ ~ ~ 0 0 0 0 1'
    RAINBOW = [(1.0, 0.42, 0.6), (1.0, 0.62, 0.2), (1.0, 0.88, 0.25), (0.4, 0.85, 0.4), (0.3, 0.7, 1.0), (0.62, 0.45, 1.0)]
    # TUG: a thread cast out to the foe - and the foe yanked in, three steps toward it
    fn(f'{pfx}/ranged', X.hit(5) + [f'execute as @e[{foe},distance=..10,sort=nearest,limit=1] at @s run function bm:{pfx}/tugged'] + X.end)
    host = f'@e[type=minecraft:wolf,tag={me},limit=1]'
    fn(f'{pfx}/tugged', [f'function bm:{pfx}/hurt'] +
       [f'execute facing entity {host} feet positioned ^ ^1 ^{d} run {thread(*RAINBOW[d % len(RAINBOW)])}' for d in range(1, 9)] +
       [f'execute at @s unless entity @e[type=minecraft:wolf,tag={me},distance=..2.2,limit=1] facing entity {host} feet if block ^ ^ ^0.8 #bm:grap_pass if block ^ ^1 ^0.8 #bm:grap_pass run tp @s ^ ^ ^0.8'
        for _ in range(3)] +
       ['particle minecraft:end_rod ~ ~1 ~ 0.2 0.4 0.2 0.04 8', 'playsound minecraft:item.lead.tied neutral @a[distance=..16] ~ ~ ~ 1 0.8'])
    # THE WEAVE: a web over every foe within 8 - bound (held fast, weakened), 7; while the web holds, its threads shimmer; pulled tight: 6 more
    fn(f'{pfx}/charged', ['tag @e[tag=bm.tkw,distance=..24] remove bm.tkw'] + X.hit(7) +
       [f'execute as @e[{foe},distance=..8] at @s run function bm:{pfx}/bound', f'tag @s remove {me}',
        'particle minecraft:end_rod ~ ~1.5 ~ 3 0.6 3 0.02 60', snd('block.amethyst_block.chime', 1.0, 0.6)])
    fn(f'{pfx}/bound', [f'function bm:{pfx}/hurt', 'tag @s add bm.tkw', 'effect give @s minecraft:slowness 5 6', 'effect give @s minecraft:weakness 5 0',
                        'particle minecraft:dust{color:[1.0,0.84,0.94],scale:1.2} ~ ~1 ~ 0.4 0.6 0.4 0 16'])
    fn(f'{pfx}/charged_tick', ['execute as @e[tag=bm.tkw,distance=..12] at @s run function bm:p254/web'])
    fn('p254/web', ['execute store result score #r bm.rng run random value 0..5'] +
       [f'execute if score #r bm.rng matches {i} run particle minecraft:dust{{color:[{r},{g},{b}],scale:0.8}} ~ ~1 ~ 0.5 0.6 0.5 0 3' for i, (r, g, b) in enumerate(RAINBOW)] +
       ['particle minecraft:end_rod ~ ~1 ~ 0.4 0.5 0.4 0.005 1'])
    fn(f'{pfx}/charged2', X.hit(6) + [f'execute as @e[tag=bm.tkw,distance=..12] at @s run function bm:{pfx}/pulled'] + X.end)
    fn(f'{pfx}/pulled', [f'function bm:{pfx}/hurt', 'tag @s remove bm.tkw', 'particle minecraft:end_rod ~ ~1 ~ 0.3 0.5 0.3 0.12 14',
                         'particle minecraft:crit ~ ~1 ~ 0.3 0.4 0.3 0.2 8', 'playsound minecraft:item.lead.break neutral @a[distance=..16] ~ ~ ~ 1 0.9'])
    # MEND: you and every follower of yours near - Instant Health and Regeneration II
    fn(f'{pfx}/support', ['execute on owner if entity @s[distance=..16] at @s run function bm:p254/mend_you'])
    fn('p254/mend_you', ['effect give @s minecraft:instant_health 1 0 true', 'effect give @s minecraft:regeneration 6 1 true',
                         'scoreboard players operation #me bm.pid = @s bm.pid'] +
       _followers('function bm:p254/mend_them') +
       ['particle minecraft:end_rod ~ ~1.2 ~ 0.4 0.7 0.4 0.03 16', 'particle minecraft:heart ~ ~1.8 ~ 0.3 0.2 0.3 0 2',
        'playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1.5'])
    fn('p254/mend_them', ['effect give @s minecraft:instant_health 1 0 true', 'effect give @s minecraft:regeneration 6 1 true',
                          'particle minecraft:dust{color:[1.0,0.84,0.94],scale:0.9} ~ ~1 ~ 0.3 0.5 0.3 0 8'])
    # GIFT: out of a fight, a small gift - one of six
    say = lambda line: 'execute unless entity @s[tag=bm.hush] run ' + G.title('@s', 'actionbar', [T('The Keeper of Bonds: ', COL, bold=True), T(line, LINE, italic=True)])
    GIFTS = [(['give @s minecraft:golden_carrot 3'], '(a little gift: three golden carrots, tied with a ribbon of thread)'),
             (['give @s minecraft:experience_bottle 4'], '(a little gift: four bottles of light it caught in its loom)'),
             (['give @s minecraft:arrow 16'], '(a little gift: a bundle of arrows, their fletching woven bright)'),
             (['give @s minecraft:emerald 2'], '(a little gift: two emeralds it found in the hem of its robe)'),
             (['effect give @s minecraft:speed 120 0 true', 'effect give @s minecraft:haste 120 0 true'], '(a little gift: it ties a thread round your wrist - your step is lighter)'),
             (['effect give @s minecraft:luck 300 0 true', 'effect give @s minecraft:hero_of_the_village 120 0 true'], '(a little gift: a kind word, woven into your cloak - folk will be kind to you)')]
    fn(f'{pfx}/kind', ['execute on owner if entity @s[distance=..8] at @s run function bm:p254/gift_you'])
    fn('p254/gift_you', [f'execute store result score #r bm.rng run random value 1..{len(GIFTS)}'] +
       [f'execute if score #r bm.rng matches {i + 1} run function bm:p254/gift/{i + 1}' for i in range(len(GIFTS))] +
       ['particle minecraft:end_rod ~ ~1.4 ~ 0.3 0.3 0.3 0.02 10', 'playsound minecraft:entity.allay.item_given player @s ~ ~ ~ 1 1.1'])
    for i, (cmds, line) in enumerate(GIFTS):
        fn(f'p254/gift/{i + 1}', cmds + [say(line)])
    return lines


def _encounter(G, X):
    """the Keeper at its loom on the dais, for a Compass-holder who hasn't its thread; the send-off; the Bond Thread - once"""
    fn, tellraw, title = G.fn, G.tellraw, G.title
    import phase125 as P125
    import phase220 as P220
    BOX = P253.BOX
    ENC = f'@e[type=minecraft:interaction,tag=bm.tkenc,{BOX}]'
    objs = ['bm.qbsq', 'bm.qbo', 'bm.qbn']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    holds = f'items entity @s container.* {X.holds("bond_thread")}'
    compass = f'items entity @s container.* {X.holds("bond_compass")}'
    # (the poses it takes only at the loom - the rest are the follower's own)
    for name in ('tend_a', 'tend_b', 'bow'):
        if f'p254/pose/{name}' not in G.FUNCS:
            fn(f'p254/pose/{name}', RF.pose(Keeper.A, KA.POSES[name], KA.RIG_SCALE, Keeper.DUR.get(name, 6), X.psel, swap=Keeper.SWAP, keep=True) +
               Keeper.POSE_EXTRA(name, X.psel))
    # ---- it's there: a Compass-holder on the island without its thread - and nobody's Keeper at the dais yet
    X.second.append(f'execute in minecraft:overworld as @a[{BOX},tag=bm.kbcomp,tag=!bm.tkmet,gamemode=!spectator] unless {holds} run function bm:p254/enc/want')
    fn('p254/enc/want', [f'execute in minecraft:overworld if entity {ENC} run return 0',
                         f'execute in minecraft:overworld as @e[type=minecraft:marker,tag=bm.kb_spawn,tag=bm.kbm,{BOX},limit=1] at @s rotated 180 0 run function bm:p254/enc/arrive'])
    fn('p254/enc/arrive', ['function bm:p254/enc/spawn', 'particle minecraft:end_rod ~ ~1.2 ~ 0.6 1 0.6 0.04 40',
                           'playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..32] ~ ~ ~ 1 0.8',
                           tellraw(f'@a[{BOX},tag=bm.kbcomp,tag=!bm.tkmet]', [T('On the dais, before the great loom, someone is weaving. ', LINE, italic=True),
                                                                               T('Fifty little lights turn slowly round it - and every one of them is a colour you know.', 'gray', italic=True)])])
    # ---- talking to it
    ksay = lambda txt: title('@s', 'actionbar', [T('The Keeper of Bonds: ', COL, bold=True), T(txt, LINE)])
    kchat = lambda parts: tellraw('@s', [T('The Keeper of Bonds: ', COL, bold=True)] + parts)
    fn('p254/enc/talk', [f'execute if score {X.here} bm.qbsq matches 1.. run return run ' + ksay('(it is weaving the last thread - only a moment more)'),
                         f'execute if entity @s[tag=bm.tkmet] run return run ' + ksay('"I am already with you. Feel the thread in your pack - it is warm."'),
                         f'execute if {holds} run return run ' + ksay('"I am already with you. Feel the thread in your pack - it is warm."'),
                         f'execute unless entity @s[tag=bm.kbcomp] unless {compass} run return run function bm:p254/enc/not_yet',
                         'function bm:p254/enc/farewell'])
    fn('p254/enc/not_yet', [kchat([T('(it looks up from the loom, and its eyes of light crinkle, kindly) ', 'gray', italic=True),
                                   T('"Not yet, little one. Your tapestry still has threads to spin - friends you have not met. '
                                     'When the compass finds you, come back. I will be here."', LINE)]),
                            'playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 0.6 1.6'])
    # (the send-off: how many friends you've made - every one of phase125.WHO but itself you've met)
    kinds = [w for w in P125.WHO if w != 'keeper']
    total = len(kinds)
    words = _words(total)
    count = ['scoreboard players set @s bm.qbn 0'] + \
        [f'execute if entity @s[advancements={{bm:met/{P220.MET_KEY.get(w, w)}=true}}] run scoreboard players add @s bm.qbn 1' for w in kinds]
    n = {'score': {'name': '@s', 'objective': 'bm.qbn'}, 'color': GOLD, 'bold': True}
    fn('p254/enc/farewell', count + ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                                     f'scoreboard players set {X.here} bm.qbsq 1', f'scoreboard players operation {X.here} bm.qbo = @s bm.pid',
                                     kchat([T('(it sets down its shuttle, and turns to you) ', 'gray', italic=True),
                                            T('"There you are. I have been weaving you for a long time, you know."', LINE)]),
                                     kchat([T('"Every friend you walked beside left a thread in my loom - Emma\'s pink first, and then the rest, one by one, '
                                              'each in its own colour."', LINE)]),
                                     f'execute if score @s bm.qbn matches {total}.. run ' +
                                     kchat([T(f'"{words.capitalize()} threads. ', GOLD, bold=True), T(f'{words.capitalize()} friends who were glad you came."', LINE)]),
                                     f'execute unless score @s bm.qbn matches {total}.. run ' +
                                     kchat([n, T(' threads, ', GOLD, bold=True), T('so far. Every one of them a friend who was glad you came."', LINE)]),
                                     kchat([T('"The tapestry is finished. All but one thread - and that one is yours. Let me weave it."', LINE)]),
                                     'playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 1.0'])
    # (the send-off as it plays out, ticked by the encounter: it bows, weaves the last thread, and holds it out)
    G.FUNCS['p254/enc/tick'].insert(0, 'execute if score @s bm.qbsq matches 1.. run return run function bm:p254/enc/seq')
    beat = {2: 'bow', 30: 'weave_up', 38: 'weave', 52: 'weave_hold', 84: 'weave_end', 96: 'gift'}
    fn('p254/enc/seq', ['scoreboard players add @s bm.qbsq 1',
                        'execute as @e[type=minecraft:item_display,tag=bm.tkencp,distance=..5] run tag @s add bm.tksel'] +
       [f'execute if score @s bm.qbsq matches {t} run function bm:p254/pose/{p}' for t, p in beat.items()] +
       ['execute if score @s bm.qbsq matches 2 run particle minecraft:end_rod ~ ~1.8 ~ 0.3 0.3 0.3 0.02 8',
        'execute if score @s bm.qbsq matches 40..84 run function bm:p254/enc/weaving',
        'execute if score @s bm.qbsq matches 84 run playsound minecraft:block.beacon.power_select neutral @a[distance=..24] ~ ~ ~ 0.8 1.6',
        'tag @e[tag=bm.tksel] remove bm.tksel',
        f'execute if score @s bm.qbsq matches {SEQ_END}.. run function bm:p254/enc/give'])
    fn('p254/enc/weaving', ['execute store result score #r bm.rng run random value 0..5'] +
       [f'execute if score #r bm.rng matches {i} run particle minecraft:dust{{color:[{r},{g},{b}],scale:0.7}} ~ ~1.7 ~-0.6 0.35 0.25 0.1 0 3'
        for i, (r, g, b) in enumerate([(1.0, 0.42, 0.6), (1.0, 0.62, 0.2), (1.0, 0.88, 0.25), (0.4, 0.85, 0.4), (0.3, 0.7, 1.0), (0.62, 0.45, 1.0)])] +
       ['particle minecraft:end_rod ~ ~1.7 ~ 0.3 0.2 0.3 0.005 1',      # (3.0c: at the web, now 0.2 lower)
        'execute if score @s bm.qbsq matches 40 run playsound minecraft:block.amethyst_block.chime neutral @a[distance=..24] ~ ~ ~ 1 0.8',
        'execute if score @s bm.qbsq matches 60 run playsound minecraft:block.amethyst_block.chime neutral @a[distance=..24] ~ ~ ~ 1 1.0',
        'execute if score @s bm.qbsq matches 76 run playsound minecraft:block.amethyst_block.chime neutral @a[distance=..24] ~ ~ ~ 1 1.3'])
    fn('p254/enc/give', ['scoreboard players set #kbg bm.rng 0', 'scoreboard players operation #kbo bm.rng = @s bm.qbo', 'tag @s add bm.tkhere',
                         'execute as @a if score @s bm.pid = #kbo bm.rng at @s run function bm:p254/enc/given',
                         'tag @s remove bm.tkhere',
                         'execute if score #kbg bm.rng matches 0 run scoreboard players set @s bm.qbsq 0'])          # (they left before it was done: it goes back to its loom)
    fn('p254/enc/given', ['scoreboard players set #kbg bm.rng 1',
                          kchat([T('(it draws the last thread out of the loom - gold, and every colour at once - winds it round a little spool, '
                                   'and puts it in your hands) ', 'gray', italic=True),
                                 T('"There. Wherever you go now, I go with you - and every bond you have made goes with us both."', LINE)]),
                          'particle minecraft:totem_of_undying ~ ~1 ~ 0.6 1 0.6 0.3 40',
                          'function bm:p254/enc/joined'])


def generate(G):
    fn = G.fn
    RP.build(Keeper, G, _abilities, _encounter)
    second = G.FUNCS['loop/second']
    # ---- the motes spin: both rings turned a step each second (right_rotation - every pose's own turn stays its left)
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.qbsp dummy']
    G.OBJECTIVES.append('bm.qbsp')
    second += ['scoreboard players add #t bm.qbsp 1', f'execute if score #t bm.qbsp matches {SPIN_N}.. run scoreboard players set #t bm.qbsp 0',
               'execute if entity @e[type=minecraft:item_display,tag=bm.tkp_motes,limit=1] run function bm:p254/spin']
    fn('p254/spin', [f'execute if score #t bm.qbsp matches {k} run function bm:p254/spin/{k}' for k in range(SPIN_N)])
    for k in range(SPIN_N):
        a = 360.0 * k / SPIN_N
        fn(f'p254/spin/{k}', [f'execute as @e[type=minecraft:item_display,tag=bm.tkp_{p},tag=!bm.tkfade] run data merge entity @s '
                              f'{{start_interpolation:0,interpolation_duration:20,transformation:{{right_rotation:{snbt(_q(s * a))}}}}}'
                              for p, s in (('motes', 1), ('motesb', -1))])
    # ---- BOND: each of your other followers out near you, a thread pulled taut
    second.append('execute as @e[type=minecraft:wolf,tag=bm.tkpet,tag=!bm.ffpet] at @s run function bm:p254/bond')
    fn('p254/bond', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #kn bm.rng 0'] +
       _followers('scoreboard players add #kn bm.rng 1') +
       ['execute if score #kn bm.rng matches 0 run return 0',
        'execute on owner if entity @s[distance=..16] at @s run function bm:p254/bond_you',
        'execute if score #kn bm.rng matches 2.. run function bm:p254/bond_kin'])
    fn('p254/bond_kin', _followers('effect give @s minecraft:strength 3 0 true', 8))
    fn('p254/bond_you', ['effect give @s minecraft:luck 3 0 true',
                         'execute if score #kn bm.rng matches 2.. run effect give @s minecraft:regeneration 3 0 true',
                         'execute if score #kn bm.rng matches 3.. run effect give @s minecraft:resistance 3 0 true',
                         'execute if score #kn bm.rng matches 3.. run effect give @s minecraft:strength 3 0 true',
                         'execute store result score #r bm.rng run random value 1..6',
                         'execute if score #r bm.rng matches 1 run particle minecraft:end_rod ~ ~1.2 ~ 0.3 0.5 0.3 0.01 2'])
    _fourth_thread(G)
    _lifeline(G)
    fn('admin/keeper_reset', ['tag @s remove bm.tkmet', 'clear @s *[minecraft:custom_data~{bm:"bond_thread"}]',
                              G.title('@s', 'actionbar', T('The Keeper has not met you yet: on the island with the Compass, it waits at its loom.', COL))])
    G.FUNCS['admin/help'].append(G.tellraw('@s', [T('/function bm:admin/keeper_reset', 'yellow'), T('  the Keeper forgets you (bm.tkmet, its thread taken back)', 'gray')]))


# ---------------------------------------------------------------- (3.0e) THE FOURTH THREAD and LIFELINE
GATE = 'execute if function bm:p58/full run return 0'
COUNT_ME = 'execute as @e[type=minecraft:wolf,tag=bm.tkpet] on owner if entity @s[tag=bm.fcme] run scoreboard players add #fc bm.rng 1'
LL_DAY = 'bm.qbld'                              # (the day - phase51's sunrise count, #day bm.bm - its thread last caught you)
LL_R = 24                                       # (how near it must be)
LL_BRINK = 4                                    # (the off hand full: caught at this much health or less - two hearts)


def _fourth_thread(G):
    """it never counts among your three: out of phase58's count, and its own calls never ask p58/full"""
    cnt = G.FUNCS['p58/count']
    assert COUNT_ME in cnt, 'rigpet no longer counts the Keeper the way the Fourth Thread expects'
    cnt.remove(COUNT_ME)
    ts = G.FUNCS['p254/try_summon']
    assert GATE in ts, ts
    ts.remove(GATE)
    J = G.FUNCS['p254/enc/joined']
    k = next(i for i, l in enumerate(J) if 'unless function bm:p58/full at @s run function bm:p254/summon' in l)
    J[k] = J[k].replace('unless function bm:p58/full at @s run', 'at @s run')
    for f, L in G.FUNCS.items():                # (nothing else of its own may still ask)
        if f.startswith('p254/'):
            assert not any('p58/full' in l for l in L), f


def lifeline_item():
    from items import ITEM_VERSION
    comps = {'minecraft:custom_data': {'bmll': B(1), 'bmv': Int(ITEM_VERSION)}, 'minecraft:item_model': 'bm:keeper_lifeline',
             'minecraft:item_name': T('Lifeline', COL), 'minecraft:max_stack_size': Int(1),
             'minecraft:tooltip_display': {'hide_tooltip': True}, 'minecraft:enchantments': {'minecraft:vanishing_curse': Int(1)},
             'minecraft:enchantment_glint_override': False,
             'minecraft:death_protection': {'death_effects': [{'type': 'minecraft:apply_effects', 'effects': [
                 {'id': 'minecraft:regeneration', 'amplifier': B(1), 'duration': Int(200)},
                 {'id': 'minecraft:absorption', 'amplifier': B(0), 'duration': Int(600)}]}]}}
    return 'minecraft:paper[' + ','.join(f'{k}={snbt(v)}' for k, v in comps.items()) + ']'


LL_TOK = '*[minecraft:custom_data~{bmll:1b}]'


def _lifeline(G):
    """once a day, near you: a blow that would kill you caught - the game's own death protection, from an unseen thread
    resting in an empty off hand; with that hand full, a catch at the brink instead"""
    fn, tellraw, title = G.fn, G.tellraw, G.title
    import phase28 as P28
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {LL_DAY} dummy']           # (bm.hp, the health objective: phase67's)
    G.OBJECTIVES.append(LL_DAY)
    second, tick = G.FUNCS['loop/second'], G.FUNCS['tick']
    tok = lifeline_item()
    # ---- who it covers (bm.tkll): its owner, within 24, not in creative or spectator, its thread not spent today
    second[-1:-1] = ['tag @a[tag=bm.tkll] remove bm.tkll',
                     'execute as @e[type=minecraft:wolf,tag=bm.tkpet,tag=!bm.ffpet] at @s run function bm:p254/life/near',
                     # (anyone it doesn't cover: no thread in the off hand; strays anywhere else, and dropped, swept)
                     f'execute as @a[tag=!bm.tkll] if items entity @s weapon.offhand {LL_TOK} run item replace entity @s weapon.offhand with minecraft:air',
                     f'execute as @a[tag=!bm.tkll] if items entity @s container.* {LL_TOK} run clear @s {LL_TOK}',
                     f'execute as @e[type=minecraft:item] if items entity @s contents {LL_TOK} run kill @s']
    fn('p254/life/near', ['scoreboard players operation #me bm.pid = @s bm.pid',
                          f'execute as @a[distance=..{LL_R},gamemode=!creative,gamemode=!spectator] if score @s bm.pid = #me bm.pid '
                          f'unless score @s {LL_DAY} = #day bm.bm run tag @s add bm.tkll'])
    # ---- every tick, for whoever it covers: strays cleared (put back from the cursor, swapped into the main hand), the thread in
    #      an empty off hand; that hand full - the brink
    tick.append('execute as @a[tag=bm.tkll] at @s run function bm:p254/life/hold')
    fn('p254/life/hold', [f'execute if items entity @s container.* {LL_TOK} run clear @s {LL_TOK}',
                          f'execute if items entity @s armor.* {LL_TOK} run clear @s {LL_TOK}',
                          f'execute unless items entity @s weapon.offhand * run item replace entity @s weapon.offhand with {tok}',
                          f'execute if items entity @s weapon.offhand {LL_TOK} run return 0',
                          f'execute if score @s bm.hp matches 1..{LL_BRINK} unless items entity @s weapon.* *[minecraft:death_protection] run function bm:p254/life/brink'])
    # ---- caught: the game's death protection spent the thread (used_totem, ours) - or the brink
    G.wjson('bm/advancement/p254/lifeline.json', {'criteria': {'used': {'trigger': 'minecraft:used_totem', 'conditions': {
        'item': {'items': 'minecraft:paper', 'predicates': {'minecraft:custom_data': '{bmll:1b}'}}}}}, 'rewards': {'function': 'bm:p254/life/caught'}})
    fn('p254/life/caught', ['advancement revoke @s only bm:p254/lifeline', 'execute at @s run function bm:p254/life/saved'])
    fn('p254/life/brink', ['effect give @s minecraft:instant_health 1 1 true', 'effect give @s minecraft:regeneration 10 1 true',
                           'effect give @s minecraft:absorption 30 0 true', 'playsound minecraft:item.totem.use player @a[distance=..16] ~ ~ ~ 0.6 1.3',
                           'execute at @s run function bm:p254/life/saved'])
    rainbow = [(1.0, 0.42, 0.6), (1.0, 0.62, 0.2), (1.0, 0.88, 0.25), (0.4, 0.85, 0.4), (0.3, 0.7, 1.0), (0.62, 0.45, 1.0)]
    fn('p254/life/saved', [f'scoreboard players operation @s {LL_DAY} = #day bm.bm', 'tag @s remove bm.tkll', f'clear @s {LL_TOK}'] +
       [f'particle minecraft:dust{{color:[{r},{g},{b}],scale:1.2}} ~ ~1 ~ 0.7 0.9 0.7 0 14' for r, g, b in rainbow] +
       ['particle minecraft:end_rod ~ ~1.2 ~ 0.5 0.8 0.5 0.12 30', 'particle minecraft:totem_of_undying ~ ~1 ~ 0.5 0.8 0.5 0.4 30',
        'playsound minecraft:block.amethyst_block.resonate player @a[distance=..16] ~ ~ ~ 1 1.2',
        'playsound minecraft:item.lead.tied player @a[distance=..16] ~ ~ ~ 1 0.7',
        tellraw('@s', [T('The Keeper of Bonds: ', COL, bold=True), T('(a thread snaps taut round you, and holds) ', 'gray', italic=True),
                       T('"Not yet. Your thread is not finished - I have you."', LINE)]),
        tellraw('@s', [T('(Lifeline: it rests now, until dawn.)', 'dark_gray', italic=True)])])
    # ---- its menu and its ways: "Lifeline: ready" / "resting until dawn"
    fn('p254/life/state', ['scoreboard players set #llr bm.rng 1', f'execute if score @s {LL_DAY} = #day bm.bm run scoreboard players set #llr bm.rng 0'])
    states = {1: [T('Lifeline: ', COL, bold=True), T('ready', '#9af09a', bold=True), T(' - its thread is with you today.', 'gray')],
              0: [T('Lifeline: ', COL, bold=True), T('resting until dawn', '#c8b0d8', italic=True), T(' - it caught you once today.', 'gray')]}

    def with_state(L, width):
        out = ['function bm:p254/life/state']
        for l in L:
            if 'dialog show @s ' not in l:
                out.append(l); continue
            head, d = l.split('dialog show @s ', 1)
            assert d.count('],actions:[') == 1, d[:80]
            for v in (1, 0):
                d2 = d.replace('],actions:[', ',' + snbt(P28.body(states[v], width)) + '],actions:[')
                h = (head or 'execute run return run ').replace('execute ', f'execute if score #llr bm.rng matches {v} ', 1)
                out.append(h + 'dialog show @s ' + d2)
        return out
    G.FUNCS['p254/menu'] = with_state(G.FUNCS['p254/menu'], 300)
    G.FUNCS['p254/powers'] = with_state(G.FUNCS['p254/powers'], 340)

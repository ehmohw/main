"""3.1: THE CAKE - the 54th follower (cake_pet_art.py draws it; fol5flag.CAKE). Queen Pearl always wanted someone to finish the
cake. With the Chef out, hand her a cake (right-click her holding one): "I am cake... I always wanted someone to finish the
cake." The Chef finishes it - a candle, a cherry, a swirl of frosting - and it hops off the plate. Right-click it: it hands you
THE CAKE'S CANDLE (its summoning item) and comes along.

ITS WAYS   TINY FORK (a foe within reach: a 5-tick wind-up, eyes wide, then a jab - 5); I AM CAKE: HOP + BOOP (a foe within 3,
           every 12 s: a hop 4 units up, and a frosting dollop on its nub boops the foe's nose - 3, Slowness II for 3 s, and it
           drops what it was holding: sweetened); LAYER SLAM (charged, every 20 s: a 9-unit bounce, hung a moment - then a plop,
           and frosting splashes out in a ring: 7 to every monster within 2.5, slowed); SPRINKLE SHOWER (you hurt, a monster near,
           every 25 s: the hat tips, nubs up, and sprinkles rain on its friends - a SUGAR RUSH: Regeneration I and Speed I, 5 s).
           It walks with a little hop every step, the flame lagging behind each bounce.
EVERYTHING ELSE is every follower's: sitting (right-click: plonked down, the flame flickering, the hat wobbling; sneak + right-
click: a doze, the hat slipped, a "z" on its face - "...frosting..."), a wardrobe (its Flavours, each a drawn cake of its own: Mint,
Lemon, Chocolate - and the metal icings), a rare aura (the Birthday Wish), a shiny (Midnight Velvet), the Partner Wheel, a frame (a
cake on a cake stand, its candle relighting), a display case, Cecil's doll, the honours, a Raid Contract; pairs with Bender, Mr.
Capshun, Henry and Nia."""
from items import item, T, TOTEM
from useitem import hold
from nbt import snbt
import fol5
import fol5art
import fol5wire as W5
import rigpet as RP
import rigface as RF2
import phase235 as P235
from fol5_kit import T as _T, limb as _limb

S5 = fol5.SPEC['cake']
A0 = fol5art.get('cake')
COL, LINE = S5['COL'], S5['LINE']
ITEM = S5['item']

item(ITEM, TOTEM, "The Cake's Candle", COL,
     ['A striped birthday candle, its wick still warm.', 'It smells of frosting. It always will.',
      ('Use: call the Cake (again: call it over).', 'blue'), ('Sneak + use: its menu.', 'blue'),
      ('Tiny Fork, Hop + Boop, Layer Slam and a Sprinkle Shower.', 'blue'), ('If it faints: 2 minutes before it can return.', 'gray'), ('"Make a wish!"', 'dark_gray')],
     model=f'bm:{ITEM}', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)

A0.POSES['sit_a2'] = dict(A0.POSES['sit_a'], hat=_T(0, 0, 4), flame=_T(0, 0, 12))           # (seated: the hat wobbles, the flame flickers)
A0.POSES['sit_b2'] = dict(A0.POSES['sit_b'], hat=_T(0, 0, 18), flame=_T(36), base=_T(-6, 0, 6))  # (dozing: a deeper breath)
A0.POSES['land'] = dict(A0.POSES['walk_1'], legr=_limb(1, 0, 10), legl=_limb(-1, 0, 10))     # (down from the hop)


class Cake(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'cake', 'The Cake', COL, LINE, 'p265', 'cz', 'kz'
    A = RF2.art(A0)
    MENU, PET_HP, PET_CD, ITEM = 5750, 30, 120, ITEM
    pron, they = 'it', 'it'
    FACE = dict(A0.FACE_MAP)
    ATTRS = dict(armor=3, attack_damage=3, movement_speed=0.34, follow_range=32, step_height=1.1)
    SCALE, HIT = 0.7, W5.hit(A0)
    CYCLE = W5.cycle(A0, (240, [(0, 'idle_a'), (80, 'idle_b'), (100, 'idle_a'), (160, 'idle_c'), (210, 'idle_a')]),
                     (6, [(0, 'sit_a'), (3, 'sit_a2')]), (None, [(0, 'happy'), (12, 'idle_a')]),
                     {7: (None, [(0, 'fork_up'), (5, 'fork'), (9, 'idle_a')]),
                      11: (None, [(0, 'hop'), (6, 'land'), (10, 'boop'), (14, 'idle_a')]),
                      12: (None, [(0, 'slam_up'), (10, 'slam'), (16, 'idle_a')]),
                      13: (None, [(0, 'sprinkle'), (14, 'happy'), (20, 'idle_a')])}, wp=8, rp_=6)
    DUR = dict(P235._DUR, walk_0=4, walk_1=4, run_0=3, sit_a=8, sit_a2=3, sit_b=12, sit_b2=40, fork_up=5, fork=2, hop=6, land=4, boop=2,
               slam_up=6, slam=2, sprinkle=6, happy=6)
    QUIPS = ['"I am cake. ...I am cake! Isn\'t that WONDERFUL?"', '"Nobody is eating me. Nobody. I checked."', '(its candle flickers happily)',
             '"Is it somebody\'s birthday? It\'s ALWAYS somebody\'s birthday."', '(a sprinkle falls off. It puts it back.)', '"Make a wish! No - a BIGGER one."']
    HELLO = ('(the Cake hops back to you, the candle bobbing)', '(a puff of icing sugar - and the Cake hops off its plate) "Make a wish!"',
             '(it blows out its own candle, and is gone)')
    SIT = ('"Up! Up! Places to hop!"', '(it plonks down on its plate, nub feet out front)')
    FAINT = '"...somebody... finish me..."'
    NOT_YOURS = '(it looks at you, then at the fork in its nub) "...you\'re not going to EAT me, are you?"'
    POWERS = [('Tiny Fork', 'a foe within reach: a little wind-up, eyes wide - then a jab, 5'),
              ('I Am Cake: Hop + Boop', 'a foe within 3, every 12 s: a happy hop, and a frosting dollop on the nose - 3, Slowness II for 3 s, and it drops what it holds: sweetened'),
              ('Layer Slam', 'charged, every 20 s: a great bounce, hung in the air - then a plop, and frosting splashes out in a ring: 7 to every monster within 2.5, slowed'),
              ('Sprinkle Shower', 'you hurt, a monster near, every 25 s: its hat tips and sprinkles rain on its friends - a SUGAR RUSH: Regeneration I and Speed I for 5 s'),
              ('A Little Hop', 'it walks with a hop every step - the flame always a bounce behind')]
    INTRO = [T('The Cake', COL, bold=True), T(' - Queen Pearl\'s cake, finished at last by the Chef, and very much alive. ', 'gray'),
             T('"I am cake!"', LINE, italic=True)]
    BURST = ['particle minecraft:dust{color:[1.0,0.61,0.8],scale:1.2} ~ ~0.6 ~ 0.4 0.4 0.4 0 16', 'particle minecraft:white_ash ~ ~0.8 ~ 0.4 0.4 0.4 0 12',
             'particle minecraft:small_flame ~ ~1.0 ~ 0.1 0.1 0.1 0 2']
    FADE_SOUND = 'playsound minecraft:block.candle.extinguish neutral @a[distance=..20] ~ ~ ~ 1 1.2'
    SUMMON_EXTRA = ['playsound minecraft:item.dye.use neutral @a[distance=..24] ~ ~ ~ 0.6 1.6', 'playsound minecraft:block.note_block.chime neutral @a[distance=..24] ~ ~ ~ 0.6 1.4']
    ENC_POSES = [(0, 'idle_a'), (30, 'idle_b'), (50, 'happy'), (66, 'idle_a')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 30 run particle minecraft:white_ash ~ ~0.8 ~ 0.3 0.3 0.3 0 6'
    ADV = ('I Am Cake', 'Hand Queen Pearl a cake while the Chef is out - and finish it, at last')
    ADMIN_HINT = 'With the Chef out, hand Queen Pearl a cake (right-click her holding it).'
    MEET_HINT = 'Right-click it.'


_DOLL = 'A doll of the Cake - a round pink tier with a cherry hat, a lit candle and a very small fork.'
_eff = W5.pair_fx
_PAIRS = {
    'cz_bender': ('cake', 'bender', 'Good Boy Gets Cake', '#e0a860', 'The Cake and Bender - he begs, and it always shares a crumb',
                  _eff(('speed', 0), ('regeneration', 0)),
                  [('bender', '(sits. Sits HARDER. Stares at the Cake.)'), ('cake', '"...just a crumb. ONE crumb. You\'re a very good boy."')],
                  [('cake', '(it shares a crumb)', 'bender', '(licks a little frosting off its plate, tail going like mad)')]),
    'cz_capshun': ('cake', 'capshun', 'Party Hat', '#f0f0f0', 'The Cake and Mr. Capshun - he draws it a party hat, and every day is a party',
                   _eff(('haste', 0), ('luck', 0)),
                   [('capshun', '[Mr. Capshun narrates: "He drew it a party hat. It was, obviously, a party."]'), ('cake', '"Is it MY birthday? Is it?!"')],
                   [('cake', '"Make a wish, Mr. Capshun!"', 'capshun', '[Mr. Capshun narrates: "He wished for a better narrator. Nothing happened."]')]),
}
W5.register(Cake, A0, _DOLL, ('minecraft:white_ash', 'minecraft:block.note_block.chime', 'minecraft:poof'), _PAIRS, 'the Cake')
FRAMES = ['cake_candle_f0', 'cake_candle_f1']


def extend_offers(O, offer):
    pass


def generate_early(G):
    RP.contract(Cake, G)


def _icon(lit=True):
    """The Cake's Candle - a striped candle, a flame (or, on a frame's stand, a puff of smoke)"""
    from sprites280 import S
    s = S()
    pal = {'w': '#ffffff', 'b': '#7ac8ff', 'k': '#3a2a20', 'o': '#ffc444', 'y': '#fff8d0', 'r': '#ff9a30', 'g': '#9a9aa8', 'p': '#ff9ccb', 'q': '#ec74b0'}
    s.g(['....ww....', '....bb....', '....ww....', '....bb....', '....ww....', '....bb....', '....ww....', '...pppp...', '..pqqqqp..', '.pppppppp.'], pal, 3, 5)
    s.px(7, 4, '#3a2a20'); s.px(8, 4, '#3a2a20')
    if lit:
        s.g(['..o..', '.oyo.', '.oyr.', '..o..'], pal, 5, 0)
    else:
        s.g(['.g...', '..g..', '.g...'], pal, 6, 1)
    return s.render()


def rp(R):
    W5.rp(Cake, R, _icon(), A0)
    R.ICONS[FRAMES[0]] = _icon(True)
    R.ICONS[FRAMES[1]] = _icon(False)


def textures():
    return A0.textures()


def _abilities(G, X):
    fn, pfx, foe, me = G.fn, X.pfx, X.foe, X.me
    snd = lambda s, v=0.6, p=1.0: f'playsound minecraft:{s} neutral @a[distance=..16] ~ ~ ~ {v} {p}'
    K = dict(melee=dict(st=7, x=12, at=6, cd=20, reach=2.4, face='surprised', go=[snd('item.trident.return', 0.3, 2.0)]),
             crowd=dict(st=11, x=16, at=4, cd=240, r=3, n=1, face='happy', go=[snd('entity.slime.jump', 0.6, 1.6)]),
             charged=dict(st=12, x=20, at=8, cd=400, r=2.5, face='surprised', go=[snd('entity.slime.jump', 1.0, 0.8)]),
             support=dict(st=13, x=22, at=14, cd=500, face='happy', go=[snd('block.amethyst_block.chime', 0.6, 1.6)]))
    lines = P235.kit(G, X, K)
    P235.melee(G, X, 5, 2.4, ['particle minecraft:crit ~ ~0.8 ~ 0.2 0.2 0.2 0.1 6', 'particle minecraft:dust{color:[0.9,0.9,0.95],scale:0.6} ~ ~0.8 ~ 0.2 0.2 0.2 0 4'],
               'minecraft:item.trident.hit')
    # HOP + BOOP: a frosting dollop on the nose - slowed, and what it held drops (sweetened)
    fn(f'{pfx}/crowd', X.hit(3) + [f'execute as @e[{foe},distance=..3.4,sort=nearest,limit=1] at @s run function bm:{pfx}/booped'] + X.end)
    fn(f'{pfx}/booped', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 3 1',
                         'particle minecraft:dust{color:[1.0,0.61,0.8],scale:1.3} ~ ~1.5 ~ 0.2 0.2 0.2 0 10', 'particle minecraft:heart ~ ~1.8 ~ 0.2 0.1 0.2 0 1',
                         snd('entity.slime.squish_small', 1.0, 1.4),
                         'execute if items entity @s weapon.mainhand * run function bm:p265/drop'])
    fn('p265/drop', ['summon minecraft:item ~ ~1 ~ {Item:{id:"minecraft:stick",count:1},PickupDelay:20s,Tags:["bm.czdrop"]}',
                     'data modify entity @e[type=minecraft:item,tag=bm.czdrop,limit=1,sort=nearest] Item set from entity @s equipment.mainhand',
                     'item replace entity @s weapon.mainhand with minecraft:air', 'tag @e[type=minecraft:item,tag=bm.czdrop] remove bm.czdrop'])
    # LAYER SLAM: a plop and a ring of frosting - 7 to every monster within 2.5, slowed
    fn(f'{pfx}/charged', X.hit(7) + [f'execute as @e[{foe},distance=..2.8] at @s run function bm:{pfx}/slammed',
                                     'particle minecraft:dust{color:[1.0,0.61,0.8],scale:1.8} ~ ~0.15 ~ 1.6 0.05 1.6 0 50',
                                     'particle minecraft:dust{color:[1.0,0.96,0.92],scale:1.4} ~ ~0.15 ~ 1.4 0.05 1.4 0 30',
                                     snd('entity.slime.squish', 1.0, 0.7), snd('block.honey_block.slide', 1.0, 0.8)] + X.end)
    fn(f'{pfx}/slammed', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 2 1'])
    # SPRINKLE SHOWER: a sugar rush for you, and its friends near you (other followers of yours)
    fn(f'{pfx}/support', ['execute on owner at @s run function bm:p265/rush',
                          'particle minecraft:dust{color:[1.0,0.35,0.48],scale:0.7} ~ ~1.6 ~ 0.8 0.6 0.8 0 16', 'particle minecraft:dust{color:[0.35,0.78,1.0],scale:0.7} ~ ~1.6 ~ 0.8 0.6 0.8 0 16',
                          'particle minecraft:dust{color:[1.0,0.88,0.35],scale:0.7} ~ ~1.6 ~ 0.8 0.6 0.8 0 16'])
    fn('p265/rush', ['effect give @s minecraft:regeneration 5 0 true', 'effect give @s minecraft:speed 5 0 true',
                     'scoreboard players operation #me bm.pid = @s bm.pid',
                     'execute as @e[type=minecraft:wolf,distance=..6] if score @s bm.pid = #me bm.pid run effect give @s minecraft:regeneration 5 0 true', 'execute as @e[type=minecraft:cat,distance=..6] if score @s bm.pid = #me bm.pid run effect give @s minecraft:regeneration 5 0 true',
                     'particle minecraft:dust{color:[0.48,1.0,0.48],scale:0.7} ~ ~2.2 ~ 0.6 0.3 0.6 0 20', 'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.4 1.8',
                     'execute unless entity @s[tag=bm.hush] run ' + G.title('@s', 'actionbar', [T('The Cake: ', COL, bold=True), T('"SUGAR RUSH!"', LINE)])])
    return lines


def _encounter(G, X):
    """hand Queen Pearl a cake, the Chef out: he finishes it, and it hops off the plate"""
    fn, tellraw, title = G.fn, G.tellraw, G.title
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    who = G.FUNCS['p190/who']
    k = next(i for i, l in enumerate(who) if 'bm.pid = #me bm.pid run return run' in l)
    who.insert(k + 1, 'execute unless entity @s[tag=bm.czmet] if items entity @s weapon.mainhand minecraft:cake run return run function bm:p265/enc/hand')
    fn('p265/enc/hand', ['scoreboard players set #hy bm.rng 0',
                         'execute as @e[type=minecraft:wolf,tag=bm.kkpet,distance=..16] if score @s bm.pid = #me bm.pid run scoreboard players set #hy bm.rng 1',
                         'execute if score #hy bm.rng matches 0 run return run ' +
                         title('@s', 'actionbar', [T('Queen Pearl: ', '#5ae0d8', bold=True), T('"A cake! ...but it isn\'t FINISHED. If only a chef were here."', '#d0fff4')]),
                         'execute if entity @e[type=minecraft:interaction,tag=bm.czenc,distance=..64] run return run ' + say('The Cake is already here, nearby - go and see.', LINE),
                         'execute at @e[type=minecraft:wolf,tag=bm.pqclk,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^1.6 run function bm:p265/enc/place',
                         'execute unless entity @e[type=minecraft:interaction,tag=bm.czenc,distance=..8] run return run ' + say('There\'s no room beside Queen Pearl here.'),
                         'item modify entity @s weapon.mainhand {type:"minecraft:set_count",count:-1,add:true}',
                         'playsound minecraft:block.note_block.chime player @a[distance=..16] ~ ~ ~ 1 1.4', 'playsound minecraft:item.dye.use player @a[distance=..16] ~ ~ ~ 1 1.2',
                         tellraw('@a[distance=..16]', [T('Queen Pearl: ', '#5ae0d8', bold=True), T('"I am cake... I always wanted someone to finish the cake." ', '#d0fff4'),
                                                       T('The Chef rolls up his sleeves - a swirl of frosting, a cherry, one candle - ', '#ffd07a', italic=True),
                                                       T('and the cake blinks, and hops off the plate.', 'gray', italic=True)])])
    fn('p265/enc/place', ['execute if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass unless block ~ ~-1 ~ #bm:grap_pass run return run function bm:p265/enc/spawn',
                          'execute positioned ~ ~1 ~ if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run function bm:p265/enc/spawn'])
    csay = lambda txt: title('@s', 'actionbar', [T('The Cake: ', COL, bold=True), T(txt, LINE)])
    fn('p265/enc/talk', [f'execute if items entity @s container.* {X.holds(ITEM)} run return run ' + csay('"You already have my candle! Don\'t blow it out."'),
                         f'execute as {X.here} at @s run particle minecraft:heart ~ ~1 ~ 0.3 0.3 0.3 0 4', 'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.6',
                         tellraw('@s', [T('It hops up and down, very pleased to be finished. Then it plucks out its candle and hands it to you - "make a wish!" - ', '#ffe6f0', italic=True),
                                        T('and a new one is already burning on its hat. It\'s coming with you.', 'gray', italic=True)]),
                         'function bm:p265/enc/joined'])


def generate(G):
    fn, title = G.fn, G.title
    frame = dict(models=FRAMES, every=15, click=['particle minecraft:firework ~ ~0.2 ~ 0.2 0.2 0.2 0.05 12', 'playsound minecraft:block.note_block.chime block @a[distance=..12] ~ ~ ~ 1 1.5',
                                                 'execute as @p[distance=..7] run ' + title('@s', 'actionbar', [T('The Cake: ', COL, bold=True), T('"Make a wish!"', LINE)])],
                 tick=['execute if score @s bm.kzft matches 0 run particle minecraft:smoke ~ ~0.25 ~ 0.05 0.1 0.05 0.01 6',
                       'execute if score @s bm.kzft matches 0 run playsound minecraft:block.candle.extinguish block @a[distance=..10] ~ ~ ~ 0.4 1.4',
                       'execute if score @s bm.kzft matches 15 run playsound minecraft:item.flintandsteel.use block @a[distance=..10] ~ ~ ~ 0.4 1.6'])
    W5.build(Cake, G, _abilities, _encounter, sitb=(200, [(0, 'sit_b'), (100, 'sit_b2')]), frame=frame)
    G.FUNCS['p265/pose/sit_b'].append('execute on owner if entity @s[distance=..12,tag=!bm.hush] run ' +
                                      title('@s', 'actionbar', [T('The Cake: ', COL, bold=True), T('"...frosting..." (it murmurs in its sleep)', LINE, italic=True)]))
    fn('admin/cake_reset', ['tag @s remove bm.czmet', f'clear @s *[minecraft:custom_data~{{bm:"{ITEM}"}}]',
                            title('@s', 'actionbar', T('The Cake has not met you yet: hand Queen Pearl a cake, with the Chef out.', COL))])

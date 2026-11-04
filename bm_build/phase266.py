"""3.1: THE SAPLING - the 55th follower (sapling_pet_art.py draws it, a rig per stage; fol5flag.SAPLING). It grows.

PLANTING     by DAY, with Kettle out, hand the Pale Dryad a Golden Apple (right-click her holding it). She bites it, finds the pip,
             and kneels: "Ooh. A seed with a heartbeat." - Kettle: "Can I water it?" - "With the WATERING can, Kettle." She plants
             it at your feet: STAGE 0, a mound of earth with a golden pip in it (yours: bm.szpd, the day it went in). Right-click
             the mound: "it's growing - ready in N days"; a water bottle used on it once skips a day.
GROWING      day 1 the SPROUT climbs out of the mound - right-click it: it hands you the GOLDEN PIP (its summoning item) and comes
             along. Day 3 the SAPLING, day 5 the TREE SPIRIT, wherever it is (each a burst of leaves, the old form popping into
             the new). The stage is yours (bm.szst): the Partner Wheel, a send-home and a call keep it. How far it follows grows
             with it: 8, then 16, then as far as anyone.
ONE FOLLOWER, THREE RIGS  its displays are the Tree Spirit's parts; a stage wears its own rig's models, and each pose is solved on
             that stage's own pivots (fol5wire.form_pose): the host tagged bm.sxs<stage>, every pose function asks it first.
ITS WAYS     ROOTSNARE (a foe within 9, every 10 s: a root foot stamped, roots burst up round it - Slowness IV and no jumping,
             1.5 / 2.5 / 3 s by stage); SEED SHOT (a foe 2.5-9 off, every 4 s: 1, 2 or 3 golden pips, 3 each - at stage 3 each one
             sprouts a tuft of grass under the foe, never a block); GOLDEN SAP (you hurt, a monster near, every 20 s: a golden
             drop - Regeneration II for 4 s and a little Absorption, for you and your followers near you).
EVERYTHING ELSE is every follower's: sitting (right-click: plopped down, swaying; sneak + right-click: it TAKES ROOT and dozes - by
night it slowly heals), a wardrobe (the Autumn Crown - drawn on every stage - and Frost and Twilight Crowns, the metal ones), a
rare aura (the Golden Bloom), a shiny (Cherry Blossom), the Partner Wheel, a frame (a pip that sprouts a day at a time into a
little potted Tree Spirit), a display case, Cecil's doll, the honours, a Raid Contract; pairs with Bender, Mr. Capshun, Henry
and Nia."""
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
from fol5_kit import T as _T

S5 = fol5.SPEC['sapling']
A0 = fol5art.get('sapling')
COL, LINE = S5['COL'], S5['LINE']
ITEM = S5['item']
GOLD = '#ffd23a'
RIGS = A0.STAGES
DAYS = {1: 1, 2: 3, 3: 5}                         # (the day after planting each stage arrives)
SNARE = {1: 1, 2: 2, 3: 3}                        # (Rootsnare's hold, s)
FOLLOW = {1: 8, 2: 16, 3: 32}
for _s, _R in RIGS.items():
    _R.POSES['sit_a2'] = _R.ground(dict(_R.POSES['sit_a'], head=_T(-6, 0, 12), crown=_T(-4, 0, 6)))
    _R.POSES['sit_b2'] = _R.ground(dict(_R.POSES['sit_b'], crown=_T(14, 0, 10)))

item(ITEM, TOTEM, 'The Golden Pip', GOLD,
     ['A little golden seed, warm to the touch.', 'Hold it to your ear: a heartbeat.',
      ('Use: call the Sapling (again: call it over).', 'blue'), ('Sneak + use: its menu.', 'blue'),
      ('Rootsnare, Seed Shot and Golden Sap.', 'blue'), ('It grows - a stage every few days.', 'blue'), ('If it faints: 2 minutes before it can return.', 'gray')],
     model=f'bm:{ITEM}', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)


class Sapling(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'sapling', 'The Sapling', COL, LINE, 'p266', 'sx', 'sz'
    A = RF2.art(A0)
    MENU, PET_HP, PET_CD, ITEM = 5800, 32, 120, ITEM
    pron, they = 'it', 'it'
    FACE = dict(A0.FACE_MAP)
    ATTRS = dict(armor=4, attack_damage=3, movement_speed=0.32, follow_range=32, step_height=1.1)
    SCALE, HIT = 0.8, W5.hit(A0)
    BOX_FIT = True
    CYCLE = W5.cycle(A0, (240, [(0, 'idle_a'), (80, 'idle_b'), (130, 'idle_a'), (170, 'idle_c'), (220, 'idle_a')]),
                     (120, [(0, 'sit_a'), (60, 'sit_a2')]), (None, [(0, 'happy') if 'happy' in A0.POSES else (0, 'idle_b'), (12, 'idle_a')]),
                     {7: (None, [(0, 'snare'), (10, 'idle_a')]), 8: (None, [(0, 'seeds'), (8, 'idle_a')]), 13: (None, [(0, 'sap'), (14, 'idle_a')])}, wp=10, rp_=8)
    DUR = dict(P235._DUR, snare=6, seeds=3, sap=8, sit_a=14, sit_a2=24, sit_b=24, sit_b2=40, walk_0=5, walk_1=5)
    QUIPS = ['"I\'m growing! I can feel it. Just a bit. Just now."', '(it turns its face to the sun, and its leaves rustle happily)',
             '"Kettle wanted to water me with a SANDWICH."', '"When I\'m big, I\'ll have apples. Golden ones. For you."',
             '(a leaf drifts down from it; it catches it and tucks it back)', '"Roots, then shoots. That\'s the rule."']
    HELLO = ('(the Sapling toddles back to you on its little roots)', '(a pop of earth - and the Sapling climbs out of it, shaking off soil) "Hello! I\'m still growing!"',
             '(it tucks its roots under, and sinks into the ground)')
    SIT = ('"Up! There\'s sun over there!"', '(it plops down on the grass, legs out, swaying)')
    FAINT = '"...need... water..."'
    NOT_YOURS = '(it peeks at you from under its leaves) "You didn\'t plant me."'
    POWERS = [('Rootsnare', 'a foe within 9, every 10 s: a root foot stamped - roots burst up round it: Slowness IV and no jumping, 1, 2 or 3 s as it grows'),
              ('Seed Shot', 'a foe 2.5-9 off, every 4 s: golden pips flicked from its crown - 1, 2 or 3 of them as it grows, 3 each (and at its biggest, each sprouts a tuft of grass)'),
              ('Golden Sap', 'you hurt, a monster near, every 20 s: a fat golden drop - Regeneration II for 4 s and a little Absorption, for you and your followers near you'),
              ('It Grows', 'a Sprout, then (day 3) a Sapling, then (day 5) a Tree Spirit - following you further each time: 8, 16, then as far as anyone'),
              ('Taking Root', 'sneak + right-click: it takes root and dozes - and by night, slowly heals')]
    INTRO = [T('The Sapling', COL, bold=True), T(' - the golden pip of the Pale Dryad\'s apple, planted, and growing. ', 'gray'),
             T('"Roots, then shoots."', LINE, italic=True)]
    BURST = ['particle minecraft:cherry_leaves ~ ~0.8 ~ 0.4 0.5 0.4 0 12', 'particle minecraft:composter ~ ~0.6 ~ 0.4 0.4 0.4 0 12',
             'particle minecraft:block{block_state:"minecraft:moss_block"} ~ ~0.2 ~ 0.3 0.1 0.3 0 10']
    FADE_SOUND = 'playsound minecraft:block.azalea_leaves.break neutral @a[distance=..20] ~ ~ ~ 1 1.2'
    SUMMON_EXTRA = ['playsound minecraft:block.rooted_dirt.break neutral @a[distance=..24] ~ ~ ~ 0.8 1.2', 'playsound minecraft:block.azalea.place neutral @a[distance=..24] ~ ~ ~ 0.8 1.4']
    ENC_POSES = [(0, 'idle_a'), (40, 'idle_b'), (60, 'idle_a')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 30 run particle minecraft:composter ~ ~0.6 ~ 0.3 0.3 0.3 0 4'
    ADV = ('Roots, Then Shoots', 'Plant the golden pip of the Pale Dryad\'s apple - and see what grows')
    ADMIN_HINT = 'By day, with Kettle out, hand the Pale Dryad a Golden Apple: she plants the pip at your feet. A day later, it sprouts.'
    MEET_HINT = 'Right-click it.'


_DOLL = 'A doll of the Sapling, grown into a Tree Spirit - a cloud of leaves, a big heartwood face, a golden apple at its cheek.'
_eff = W5.pair_fx
_PAIRS = {
    'sx_bender': ('sapling', 'bender', 'Good Boy, Good Soil', '#e0a860', 'The Sapling and Bender - he digs where it stands, to help it plant',
                  _eff(('regeneration', 0), ('speed', 0)),
                  [('bender', '(digs a little hole beside it, very helpfully)'), ('sapling', '"Thank you, Bender! ...I\'m already planted. But thank you!"')],
                  [('sapling', '(drips a little golden sap on his nose)', 'bender', '(sneezes, then lies down beside it, happy)')]),
    'sx_capshun': ('sapling', 'capshun', 'Still Life', '#f0f0f0', 'The Sapling and Mr. Capshun - he paints it, and its leaves flash red, yellow and blue',
                   _eff(('haste', 0), ('regeneration', 0)),
                   [('capshun', '[Mr. Capshun narrates: "Hold still. You\'re a tree."]'), ('sapling', '"I AM holding still! It\'s the wind!"')],
                   [('sapling', '(its leaves go red, then yellow, then blue)', 'capshun', '[Mr. Capshun narrates: "Primary colours. A masterpiece."]')]),
}
W5.register(Sapling, A0, _DOLL, ('minecraft:cherry_leaves', 'minecraft:block.azalea_leaves.place', 'minecraft:composter'), _PAIRS, 'the Sapling')
FRAMES = [f'{ITEM}_f{i}' for i in range(4)]


def extend_offers(O, offer):
    pass


def generate_early(G):
    RP.contract(Sapling, G)


# ---------------------------------------------------------------------------------------------------- the icons
def _icon(stage=None):
    """The Golden Pip - a little gold seed; in a frame (stage 0-3): a pot, and in it the pip, a sprout, a sapling, a Tree Spirit"""
    from sprites280 import S
    s = S()
    pal = {'g': '#efbd2c', 'l': '#ffdf6e', 'd': '#b8800e', 'w': '#fff6cc', 'p': '#b0602a', 'q': '#8a4a1e', 'e': '#4a3628',
           'n': '#64a250', 'm': '#4d8a44', 'b': '#8b7e70', 'h': '#f3e5c9', 'k': '#2e1a06'}
    if stage is None:
        s.g(['...ll...', '..lggl..', '.lgggggd', '.gggwggd', '.gggggdd', '..gggdd.', '...gdd..'], pal, 4, 4)
        return s.render()
    s.g(['.pppppppppp.', '.qpppppppppq', '..pppppppp..', '..qppppppq..', '...pppppp...'], pal, 2, 11)
    s.g(['.eeeeeeeeee.'], pal, 2, 10)
    if stage == 0:
        s.g(['..gl..', '.gggd.'], pal, 5, 8)
    elif stage == 1:
        s.g(['.n..n.', 'nnmmnn', '..hh..', '..hh..'], pal, 5, 6)
    elif stage == 2:
        s.g(['..nnnn..', '.nnmmnn.', '..nmmn..', '...hh...', '...bb...', '...bb...'], pal, 4, 4)
    else:
        s.g(['..nnnnnn..', '.nnnmmnnnn', 'nnnmnnmnnn', '.nhhhhhhn.', '..hkhhkh..', '..hhhhhh..', '...bbbb...', '...bbbb...'], pal, 3, 2)
        s.px(11, 6, '#efbd2c')
    return s.render()


def rp(R):
    W5.rp(Sapling, R, _icon(), A0)
    for i in range(4):
        R.ICONS[FRAMES[i]] = _icon(i)
    # (each stage's face part: an item definition picking the mood's face, as rigpet writes the Tree Spirit's)
    names = set(A0.models())

    def post(R2):
        mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
        for st in (1, 2):
            base = f'sp{st}_head'
            cases = [{'when': e, 'model': mdl(f'{base}_x{Sapling.FACE[e]}')} for e in Sapling.EXPR if Sapling.FACE.get(e) and f'{base}_x{Sapling.FACE[e]}' in names]
            R2.wj(f'assets/bm/items/{base}.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0, 'cases': cases, 'fallback': mdl(base)}})
    R.POST.append(post)


def textures():
    return A0.textures()


# ---------------------------------------------------------------------------------------------------- its ways
def _abilities(G, X):
    fn, pfx, foe, me = G.fn, X.pfx, X.foe, X.me
    snd = lambda s, v=0.6, p=1.0: f'playsound minecraft:{s} neutral @a[distance=..16] ~ ~ ~ {v} {p}'
    K = dict(melee=dict(st=7, x=16, at=10, cd=200, reach=9, face='serious', go=[snd('block.rooted_dirt.break', 1.0, 0.7)]),
             ranged=dict(st=8, x=12, at=7, cd=80, near=2.5, far=9, face='serious', go=[snd('block.azalea_leaves.break', 0.8, 1.6)]),
             support=dict(st=13, x=20, at=8, cd=400, face='happy', go=[snd('block.honey_block.place', 0.7, 1.4)]))
    lines = P235.kit(G, X, K)
    G.FUNCS.pop(f'{pfx}/near_owner', None)              # (no kindness of its own: nothing asks whether you're near)
    stage = lambda s: f'execute if entity @s[tag=bm.sxs{s}] run'
    # ROOTSNARE: roots burst up round the nearest foe within 9 - held (Slowness IV, no jumping) for the stage's time
    fn(f'{pfx}/melee', X.hit(3) + [f'execute as @e[{foe},distance=..9.4,sort=nearest,limit=1] at @s run function bm:{pfx}/snared'] + X.end)
    fn(f'{pfx}/snared', [f'function bm:{pfx}/hurt'] +
       [f'execute if entity @e[type=minecraft:wolf,tag={me},tag=bm.sxs{s},limit=1] run function bm:{pfx}/hold{s}' for s in (1, 2, 3)] +
       ['particle minecraft:block{block_state:"minecraft:rooted_dirt"} ~ ~0.2 ~ 0.6 0.1 0.6 0 24', 'particle minecraft:block{block_state:"minecraft:mangrove_roots"} ~ ~0.6 ~ 0.4 0.5 0.4 0 16',
        snd('block.mangrove_roots.place', 1.0, 0.8)])
    for s in (1, 2, 3):
        fn(f'{pfx}/hold{s}', [f'effect give @s minecraft:slowness {SNARE[s]} 3', f'effect give @s minecraft:jump_boost {SNARE[s]} 200'])
    # SEED SHOT: 1-3 golden pips by stage, 3 each; at stage 3 a tuft of grass (particles only) under the foe
    fn(f'{pfx}/ranged', X.hit(3) + [f'execute as @e[{foe},distance=..9.4,sort=nearest,limit=1] at @s run function bm:{pfx}/seeded'] + X.end)
    fn(f'{pfx}/seeded', [f'function bm:{pfx}/hurt', f'execute if entity @e[type=minecraft:wolf,tag={me},tag=bm.sxs2,limit=1] run function bm:{pfx}/hurt',
                         f'execute if entity @e[type=minecraft:wolf,tag={me},tag=bm.sxs3,limit=1] run function bm:{pfx}/hurt',
                         f'execute if entity @e[type=minecraft:wolf,tag={me},tag=bm.sxs3,limit=1] run function bm:{pfx}/tuft',
                         'particle minecraft:dust{color:[1.0,0.82,0.23],scale:1.0} ~ ~1 ~ 0.2 0.2 0.2 0 8', snd('entity.item.pickup', 0.6, 1.8)])
    fn(f'{pfx}/tuft', ['particle minecraft:block{block_state:"minecraft:short_grass"} ~ ~0.1 ~ 0.3 0.05 0.3 0 16', 'particle minecraft:composter ~ ~0.3 ~ 0.3 0.2 0.3 0 8'])
    # GOLDEN SAP: a fat golden drop over you - Regeneration II, a little Absorption; your followers near too
    fn(f'{pfx}/support', ['execute on owner at @s run function bm:p266/sap'])
    fn('p266/sap', ['effect give @s minecraft:regeneration 4 1 true', 'effect give @s minecraft:absorption 20 0 true',
                    'scoreboard players operation #me bm.pid = @s bm.pid',
                    'execute as @e[type=minecraft:wolf,distance=..6] if score @s bm.pid = #me bm.pid run effect give @s minecraft:regeneration 4 1 true',
                    'execute as @e[type=minecraft:cat,distance=..6] if score @s bm.pid = #me bm.pid run effect give @s minecraft:regeneration 4 1 true',
                    'particle minecraft:dripping_honey ~ ~2.4 ~ 0.2 0.1 0.2 0 6', 'particle minecraft:dust{color:[1.0,0.82,0.23],scale:1.4} ~ ~2.2 ~ 0.2 0.2 0.2 0 10',
                    'playsound minecraft:block.honey_block.slide player @s ~ ~ ~ 0.8 1.4'])
    # (taking root, at night: it heals slowly)
    X.second.append('execute as @e[type=minecraft:wolf,tag=bm.sxpet,tag=bm.sxsb] if data entity @s {Sitting:1b} at @s if predicate bm:p229/night run function bm:p266/night_heal')
    fn('p266/night_heal', ['effect give @s minecraft:regeneration 2 0 true', 'particle minecraft:composter ~ ~0.8 ~ 0.3 0.3 0.3 0 2'])
    return lines


def _encounter(G, X):
    """planted by the Pale Dryad (a Golden Apple, by day, Kettle out); a mound; a day later the Sprout climbs out of it"""
    fn, tellraw, title = G.fn, G.tellraw, G.title
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in ('bm.szpd', 'bm.szst', 'bm.szmd')]
    G.OBJECTIVES += ['bm.szpd', 'bm.szst', 'bm.szmd']
    who = G.FUNCS['p236p/who']
    k = next(i for i, l in enumerate(who) if 'bm.pid = #me bm.pid run return run' in l)
    who.insert(k + 1, 'execute unless entity @s[tag=bm.sxmet] if items entity @s weapon.mainhand minecraft:golden_apple run return run function bm:p266/enc/hand')
    pyq = lambda txt: [T('The Pale Dryad: ', '#6aa8f0', bold=True), T(txt, '#d8ecff')]
    fn('p266/enc/hand', ['execute if entity @s[tag=bm.sxplant] run return run ' + title('@s', 'actionbar', pyq('"You\'ve a pip in the ground already! Patience, little one."')),
                         'execute unless score #tod bm.bm matches 0..12000 run return run ' + title('@s', 'actionbar', pyq('"An apple! ...in the morning, love. Seeds like the sun."')),
                         'scoreboard players set #hy bm.rng 0',
                         'execute as @e[type=minecraft:wolf,tag=bm.ktpet,distance=..16] if score @s bm.pid = #me bm.pid run scoreboard players set #hy bm.rng 1',
                         'execute if score #hy bm.rng matches 0 run return run ' + title('@s', 'actionbar', pyq('"Ooh, a golden apple. ...Kettle would love to see what\'s inside. Where IS he?"')),
                         'item modify entity @s weapon.mainhand {type:"minecraft:set_count",count:-1,add:true}',
                         'tag @s add bm.sxplant', 'scoreboard players operation @s bm.szpd = #day bm.bm', 'scoreboard players set @s bm.szst 0',
                         'function bm:p266/mound/plant',
                         tellraw('@a[distance=..16]', [T('The Pale Dryad: ', '#6aa8f0', bold=True), T('"Ooh. A seed with a heartbeat." ', '#d8ecff'),
                                                       T('Kettle: ', '#8ad8ff', bold=True), T('"Can I water it?" ', '#d8f0ff'),
                                                       T('The Pale Dryad: ', '#6aa8f0', bold=True), T('"With the WATERING can, Kettle." ', '#d8ecff'),
                                                       T('(She kneels and plants the golden pip at your feet. It will sprout tomorrow.)', 'gray', italic=True)]),
                         'playsound minecraft:block.rooted_dirt.place player @a[distance=..16] ~ ~ ~ 1 1', 'playsound minecraft:block.amethyst_block.chime player @a[distance=..16] ~ ~ ~ 0.6 1.6'])
    # ---- the mound (stage 0): a prop at your feet - its display, and a box to right-click; it knows whose it is (bm.pid)
    mound = {'Tags': ['bm.sxmound', 'bm.sxmn'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:sp1_mound'}},
             'item_display': 'fixed', 'transformation': {'left_rotation': RF.IDENT, 'right_rotation': RF.IDENT, 'translation': [F(0), F(0.18), F(0)], 'scale': [F(0.8)] * 3}}
    box = {'Tags': ['bm.sxmound', 'bm.sxmbox', 'bm.sxmn'], 'width': F(0.9), 'height': F(0.5), 'response': B(1)}
    fn('p266/mound/plant', ['execute align xz positioned ~0.5 ~ ~0.5 run summon minecraft:item_display ~ ~ ~ ' + snbt(mound),
                            'execute align xz positioned ~0.5 ~ ~0.5 run summon minecraft:interaction ~ ~ ~ ' + snbt(box),
                            'scoreboard players operation @e[tag=bm.sxmn,distance=..2] bm.pid = @s bm.pid', 'tag @e[tag=bm.sxmn] remove bm.sxmn',
                            'particle minecraft:block{block_state:"minecraft:rooted_dirt"} ~ ~0.2 ~ 0.3 0.1 0.3 0 20'])
    X.fast.append('execute as @e[type=minecraft:interaction,tag=bm.sxmbox] if data entity @s interaction at @s run function bm:p266/mound/click')
    X.fast.append('execute as @e[type=minecraft:interaction,tag=bm.sxmbox] if data entity @s attack run data remove entity @s attack')
    fn('p266/mound/click', ['scoreboard players operation #o bm.rng = @s bm.pid', 'execute on target run function bm:p266/mound/clicked', 'data remove entity @s interaction'])
    fn('p266/mound/clicked', ['execute unless score @s bm.pid = #o bm.rng run return run ' + say('(Someone else\'s golden pip is growing here.)', GOLD),
                              'execute if items entity @s weapon.mainhand minecraft:potion[minecraft:potion_contents={potion:"minecraft:water"}] unless entity @s[tag=bm.sxwet] run return run function bm:p266/mound/water',
                              'function bm:p266/days', 'scoreboard players set #n bm.rng 1', 'scoreboard players operation #n bm.rng -= #d bm.rng',
                              title('@s', 'actionbar', [T('A golden pip, warm in the earth. ', GOLD), T("It's growing - ready in ", 'gray'), {'score': {'name': '#n', 'objective': 'bm.rng'}, 'color': 'white'},
                                                        T(' day(s).', 'gray')])])
    fn('p266/mound/water', ['item replace entity @s weapon.mainhand with minecraft:glass_bottle', 'tag @s add bm.sxwet', 'scoreboard players remove @s bm.szpd 1',
                            'particle minecraft:splash ~ ~1 ~ 0.4 0.3 0.4 0 20', 'playsound minecraft:item.bottle.empty player @s ~ ~ ~ 1 1',
                            title('@s', 'actionbar', T('You water the pip. The earth over it stirs - it will be a day sooner.', GOLD))])
    # (#d: days since it was planted, for the player running it)
    fn('p266/days', ['scoreboard players operation #d bm.rng = #day bm.bm', 'scoreboard players operation #d bm.rng -= @s bm.szpd'])
    X.second.append('execute as @e[type=minecraft:interaction,tag=bm.sxmbox] at @s run function bm:p266/mound/sec')
    fn('p266/mound/sec', ['scoreboard players operation #o bm.rng = @s bm.pid', 'scoreboard players set #rd bm.rng 0',
                          'execute as @a[distance=..24] if score @s bm.pid = #o bm.rng run function bm:p266/mound/ready',
                          'execute if score #rd bm.rng matches 1 run function bm:p266/mound/sprout'])
    fn('p266/mound/ready', ['function bm:p266/days', 'execute if score #d bm.rng matches 1.. run scoreboard players set #rd bm.rng 1'])
    fn('p266/mound/sprout', ['kill @e[type=minecraft:item_display,tag=bm.sxmound,distance=..0.6]', 'function bm:p266/enc/spawn',
                             'scoreboard players operation @e[type=minecraft:interaction,tag=bm.sxenc,distance=..0.6] bm.pid = #o bm.rng', 'kill @s',
                             'particle minecraft:cherry_leaves ~ ~0.6 ~ 0.4 0.4 0.4 0 20', 'particle minecraft:block{block_state:"minecraft:rooted_dirt"} ~ ~0.2 ~ 0.4 0.1 0.4 0 20',
                             'playsound minecraft:block.rooted_dirt.break neutral @a[distance=..16] ~ ~ ~ 1 1.2',
                             'execute as @a[distance=..24] if score @s bm.pid = #o bm.rng run ' + title('@s', 'actionbar', T('The golden pip has sprouted! Something small is climbing out of the earth...', GOLD))])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[tag=bm.sxmound]']
    # ---- the Sprout, out of its mound: yours, right-clicked - it comes along
    csay = lambda txt: title('@s', 'actionbar', [T('The Sapling: ', COL, bold=True), T(txt, LINE)])
    fn('p266/enc/talk', [f'execute unless score @s bm.pid = {X.here} bm.pid run return run ' + csay('(it hides behind its leaves) "...you\'re not the one who planted me."'),
                         f'execute if items entity @s container.* {X.holds(ITEM)} run return run ' + csay('"You\'ve got my pip already! It\'s ME."'),
                         'scoreboard players set @s bm.szst 1',
                         f'execute as {X.here} at @s run particle minecraft:heart ~ ~0.8 ~ 0.3 0.3 0.3 0 4', 'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.6',
                         tellraw('@s', [T('It shakes off the soil, blinks up at you with big amber eyes, and pats the golden husk on its head. ', LINE, italic=True),
                                        T('Then it taps the pip in its chest - and a little golden seed drops into your hand. It\'s coming with you.', 'gray', italic=True)]),
                         'tag @s remove bm.sxplant', 'function bm:p266/enc/joined'])


# ---------------------------------------------------------------------------------------------------- the stages
def _stages(G, C):
    fn, pfx, ab, title = G.fn, C.pfx, C.ab, G.title
    sel = f'bm.{ab}sel'
    psel = lambda p: f'@e[type=minecraft:item_display,tag={sel},tag=bm.{ab}p_{p}]'
    mine = f'@e[type=minecraft:wolf,tag=bm.{ab}pet]'
    # ---- every pose: the stage's own (solved on its rig's pivots), the Tree Spirit's as rigpet wrote it
    poses = [n[len(f'{pfx}/pose/'):] for n in G.FUNCS if n.startswith(f'{pfx}/pose/') and not n.startswith(f'{pfx}/pose/tw_')]
    for name in poses:
        for st in (1, 2):
            R = RIGS[st]
            pz = R.POSES.get(name) or R.POSES['idle_a']
            fn(f'{pfx}/s{st}/pose/{name}', W5.form_pose(A0, R, pz, C.DUR.get(name, 6), psel))
        G.FUNCS[f'{pfx}/pose/{name}'][0:0] = [f'execute if entity @s[tag=bm.sxs{st}] run return run function bm:{pfx}/s{st}/pose/{name}' for st in (1, 2)]
    # (the in-between keys of sitting down and getting up are the Tree Spirit's: for a smaller stage, its own pose at once)
    for n in [n for n in G.FUNCS if n.startswith(f'{pfx}/pose/tw_')]:
        tgt = n.rsplit('_', 1)[0][len(f'{pfx}/pose/tw_'):]
        G.FUNCS[n][0:0] = ['execute if entity @s[tag=bm.sxs1] run return 0', 'execute if entity @s[tag=bm.sxs2] run return 0']
    # ---- his dress: the stage's models (the owner's bm.szst), the host tagged, its follow range; then the wardrobe's look
    D_ = G.FUNCS[f'{pfx}/dress']
    k = D_.index('scoreboard players set #wk bm.rng 0')
    D_[k:k] = ['scoreboard players set #sst bm.rng 3', 'execute as @a if score @s bm.pid = #me bm.pid if score @s bm.szst matches 1..2 run scoreboard players operation #sst bm.rng = @s bm.szst'] + \
              [f'execute as {mine} if score @s bm.pid = #me bm.pid run tag @s remove bm.sxs{s}' for s in (1, 2, 3)] + \
              [f'execute if score #sst bm.rng matches {s} run function bm:{pfx}/s{s}/dress' for s in (1, 2, 3)]
    for s in (1, 2, 3):
        R = RIGS[s]
        fn(f'{pfx}/s{s}/dress', [f'execute as {mine} if score @s bm.pid = #me bm.pid run tag @s add bm.sxs{s}',
                                 f'execute as {mine} if score @s bm.pid = #me bm.pid run attribute @s minecraft:follow_range base set {FOLLOW[s]}',
                                 f'execute as {mine} if score @s bm.pid = #me bm.pid run function bm:{pfx}/s{s}/box'] +
           [f'execute as {psel(p)} run data modify entity @s item.components."minecraft:item_model" set value "bm:{R.PREFIX}{p}"' for p in A0.PARTS if R._els[p]])
        y0, h, x0, x1, z0, z1 = R.fit(R.POSES['idle_a'])
        import compsize as CS
        fn(f'{pfx}/s{s}/box', CS.resize(f'bm.{ab}hit', round(max(0.5, max(x1 - x0, z1 - z0) * 0.85 + 0.1), 2), round(max(0.5, h + 0.1), 2)))
    fn(f'{pfx}/box_fit', [f'execute if entity @s[tag=bm.sxs{s}] run return run function bm:{pfx}/s{s}/box' for s in (1, 2, 3)])
    # ---- the encounter's Sprout: stage 1's models and poses (its click box tagged, its parts the Sprout's)
    sp = G.FUNCS[f'{pfx}/enc/spawn']
    sp.insert(1, f'tag @e[type=minecraft:interaction,tag=bm.{ab}enew,distance=..1] add bm.sxs1')
    sp[:] = [l.replace(f'function bm:{pfx}/grow', f'execute as @e[type=minecraft:interaction,tag=bm.{ab}enew,distance=..1] run function bm:{pfx}/grow') for l in sp]
    G.FUNCS[f'{pfx}/enc/look'][0:0] = [f'execute as {psel(p)} run data modify entity @s item.components."minecraft:item_model" set value "bm:sp1_{p}"' for p in A0.PARTS if RIGS[1]._els[p]]
    # ---- growing: each second, a friend of its: the day it's reached - a new stage, a burst of leaves, the new form out
    G.FUNCS['loop/second'].append('execute as @a[tag=bm.sxmet,scores={bm.szst=1..2}] at @s run function bm:p266/grow_q')
    fn('p266/grow_q', ['function bm:p266/days', 'scoreboard players set #ns bm.rng 1', f'execute if score #d bm.rng matches {DAYS[2]}.. run scoreboard players set #ns bm.rng 2',
                       f'execute if score #d bm.rng matches {DAYS[3]}.. run scoreboard players set #ns bm.rng 3',
                       'execute if score #ns bm.rng > @s bm.szst run function bm:p266/grew'])
    fn('p266/grew', ['scoreboard players operation @s bm.szst = #ns bm.rng', 'scoreboard players operation #me bm.pid = @s bm.pid',
                     f'execute as {mine} if score @s bm.pid = #me bm.pid at @s run function bm:p266/grew_pet',
                     'execute if score @s bm.szst matches 2 run ' + title('@s', 'actionbar', [T('The Sapling has grown! ', COL, bold=True), T('A SAPLING now - a burl head, a crown of leaves.', LINE)]),
                     'execute if score @s bm.szst matches 3 run ' + title('@s', 'actionbar', [T('The Sapling has grown! ', COL, bold=True), T('A TREE SPIRIT now - all canopy, and a golden apple.', LINE)]),
                     'playsound minecraft:block.azalea.place player @s ~ ~ ~ 1 0.8', 'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.4 1.6'])
    fn('p266/grew_pet', [f'function bm:{pfx}/form2', f'function bm:{pfx}/box_fit', 'scoreboard players set @s bm.szs -1',
                         'particle minecraft:cherry_leaves ~ ~1 ~ 0.6 0.8 0.6 0 30', 'particle minecraft:composter ~ ~0.8 ~ 0.5 0.6 0.5 0 20'])
    # (form2: dress its parts again, as rigpet's FORM does - here without a form)
    if f'{pfx}/form2' not in G.FUNCS:
        fn(f'{pfx}/form2', ['scoreboard players operation #me bm.pid = @s bm.pid',
                            f'execute as @e[type=minecraft:item_display,tag=bm.{ab}p_pet,tag=!bm.{ab}fade] if score @s bm.pid = #me bm.pid run tag @s add {sel}',
                            f'function bm:{pfx}/dress', f'tag @e[tag={sel}] remove {sel}'])
    G.FUNCS['admin/help'].append(G.tellraw('@s', [T('/function bm:admin/sapling_grow', 'yellow'), T('  your Sapling a stage older (a day at a time: its planting day moved back two)', 'gray')]))
    fn('admin/sapling_grow', ['scoreboard players remove @s bm.szpd 2', title('@s', 'actionbar', T('Your Sapling\'s planting day moved back two days.', COL))])
    fn('admin/sapling_reset', ['tag @s remove bm.sxmet', 'tag @s remove bm.sxplant', 'tag @s remove bm.sxwet', 'scoreboard players set @s bm.szst 0', f'clear @s *[minecraft:custom_data~{{bm:"{ITEM}"}}]',
                               title('@s', 'actionbar', T('The Sapling has not been planted: a Golden Apple, by day, to the Pale Dryad, with Kettle out.', COL))])


def generate(G):
    fn, title = G.fn, G.title
    frame = dict(models=[], click=['particle minecraft:item{item:{id:"minecraft:golden_apple"}} ~ ~0.2 ~ 0.2 0.2 0.2 0.05 10',
                                   'playsound minecraft:block.azalea_leaves.place block @a[distance=..12] ~ ~ ~ 1 1.4'],
                 tick=['execute unless score @s bm.szmd matches 0.. run scoreboard players operation @s bm.szmd = #day bm.bm',
                       'scoreboard players operation #d bm.rng = #day bm.bm', 'scoreboard players operation #d bm.rng -= @s bm.szmd'] +
                      [f'execute if score #d bm.rng matches {lo} run data modify entity @s Item.components."minecraft:item_model" set value "bm:{FRAMES[i]}"'
                       for i, lo in enumerate(('..0', '1', '2..3', '4..'))])
    W5.build(Sapling, G, _abilities, _encounter, sitb=(200, [(0, 'sit_b'), (100, 'sit_b2')]), frame=frame)
    _stages(G, Sapling)

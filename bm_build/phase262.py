"""3.0k: THE RAT KING - the 52nd follower, and the Keeper of Bonds' counterpart (ratking_pet_art.py draws him; the heist's boss rig
redrawn as a follower). Where the Keeper weaves every bond you've made, the Rat King keeps count of them - "a debt is a bond too,
if you ask me." He is found only once all fifty others are (the owner: "only as the counterpart to the Keeper of Bonds - once all
the 50 other followers are recruited"); neither of them counts toward the other (phase253.COUNTERPARTS).

THE KING'S COIN   the Compass of Bonds' dark twin: with the compass (bm.kbcomp - every other follower met), the coin comes too,
             once (bm.rwcoin; anyone who had the compass before 3.0k gets it the next second). Its needle points DOWN - at the very
             spot the compass points up at: his COUNTING HOUSE, at the bottom of the world under the Loom Sanctuary (as above, so
             below; built the first time anyone needs it, from commands - p262/room/build).
THE WAY DOWN  stand in the column under the island holding the coin and SNEAK for three seconds: the floor gives way to a rat-run
             and you slide down to the Counting House (where you stood is kept, bm.rwbx/by/bz). THE WAY UP: the mouse hole in its
             east wall - step into it and you're back where you came down. Your followers near come with you, both ways. Nothing in it can be broken (adventure, as the island).
THE AUDIENCE  (rigpet's encounter, at his throne: whenever a coin-holder who hasn't his Marker (bm.rwmet) is in the hall, he lounges
             there at his full, imposing size.) Speak to him -
  THE TRIBUTE    "A king takes his cut." A dialog (menu 5500): 32 Gold Ingots, 16 Gutter Coins or a Golden Cheese Wheel (his own
                 prize: "MY cheese! Where did you - never mind."), whichever you can pay. Paid once (bm.rwpaid).
  THE SHELL OF RATS  "Loyalty, now. One of my court has pinched my favourite coin." Five court rats on the counting table: the
                 thief glints, the coin goes in its cheek, the five shuffle; punch the thief. A miss: "Pfah. Again." - a new thief,
                 a new shuffle, no cost. Caught: he stamps the ROYAL MARKER (his summoning item: an IOU sealed in gold wax, "The
                 bearer owes the Rat King one (1) adventure.") - and comes along.
HIS SIZE      his own is the heist boss's (RIG_SCALE 0.9, ~2.8 blocks; the owner: "large and imposing"); his menu's COMPANION SIZE
             (code 5456; compsize, the owner's bm.rwcs, kept across recall) twins his rig at ratking_pet_art.COMPANION (~1.55) - his
             host and click box shrink with it (compsize.resize).
HIS WAYS      SCEPTRE SWAT (a foe within 2.8: 7); SCEPTRE SLAM (two or more within 4, every 12 s: rearing up and slamming the
             sceptre down - 6 to each, knocked back, slowed); THE COURT (charged, every minute: a whistle - his court rats boil out
             round every foe within 8 and bite, 4 and then 4 more, weakened); A LOAN, WITH INTEREST (out of a fight, every minute:
             a coin's worth of something); THE KING'S CUT (passive: every monster you kill with him near, one in three pays a
             tithe - a few gold nuggets; now and then an emerald; very rarely a Black Market Token); BONDS AND DEBTS (with the
             Keeper out too: Luck and Haste for you, and a word between them). His Piercing Blow (Queen Ava's rank III, phase226)
             is THE ROYAL DECREE. He is a king, so he counts among your three.
EVERYTHING ELSE is every follower's: sitting (on his haunches, then counting his hoard), a wardrobe (his Cape - per look, the same
on both sizes), a rare aura (the Golden Hoard), a shiny (Moonlit Albino - drawn: ratking_pet_art.SHINY_TEX), the Partner Wheel (at
the END of its lists), a frame, a display case, Cecil's doll, the honours, a Raid Contract; pairs with Bender, Mr. Capshun, Henry
and Nia. In a heist, a crew with a friend of his in it never meets the Rat King in the Champion's Pit (he won't fight a friend's
crew: a Vault Ravager comes instead)."""
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, F, B, Int, IntArray
import ratking_pet_art as A
import rigfol as RF
import rigpet as RP
import rigface as RF2
import phase141 as P141
import phase134 as P134
import phase235 as P235
import phase253 as P253
import compsize as CS

COL, LINE = '#ffc23a', '#ffe8b0'
CRIMSON = '#c8384a'
ITEM, COIN = 'royal_marker', 'kings_coin'
AUD = 5500                                      # (the audience's tribute dialog: its menu; 5501-5503 the tributes)
CSZ_K = round(A.COMPANION / A.RIG_SCALE, 4)     # (his companion size, of his own)
HOST_BIG, HOST_SMALL = 1.6, 0.85                # (his host's scale: his own size, and companion)
HIT_BIG, HIT_SMALL = (1.5, 2.9), (0.85, 1.6)    # (his click box: the same)

# ---- the Counting House: under the Loom Sanctuary's landing circle, at the bottom of the world (absolute; built by commands)
CX, CZ = int(P253.AX // 1), int(P253.AZ // 1) - 6        # (its centre column: the throne north of it, the rat-run's landing south)
FY = -56                                                   # (its floor's standing y)
HALF, HIGH = 7, 7                                          # (inside: 15 x 15, 7 tall)
ROOM = f'x={CX - HALF},y={FY},z={CZ - HALF},dx={2 * HALF},dy={HIGH - 1},dz={2 * HALF}'
DOWNCOL = f'x={int(P253.AX // 1) - 3},y=-40,z={int(P253.AZ // 1) - 3},dx=6,dy=360,dz=6'    # (where you sneak to go down: the island's column)
LAND = (CX + 0.5, FY, CZ + 5.5)                            # (the rat-run's landing, facing the throne)
THRONE = (CX + 0.5, FY + 1, CZ - 5 + 0.5)                  # (his seat's top)
HOLE = (CX + HALF + 0.5, FY, CZ + 0.5)                     # (the mouse hole, in the east wall)
SLOTS = [(CX - 5 + i + 0.5, FY + 1.0, CZ + 0.5) for i in range(5)]    # (the five rats' places on the counting table)
RVER = 1

item(ITEM, TOTEM, 'The Royal Marker', COL,
     ['An IOU on thick vellum, sealed in gold wax:', '"The bearer owes the Rat King one (1) adventure."',
      ('Use: call the Rat King (again: call him over).', 'blue'), ('Sneak + use: his menu.', 'blue'),
      ('Sceptre, slam, his Court, and THE KING\'S CUT.', 'blue'), ('Companion Size, from his menu.', 'blue'),
      ('If he faints: 2 minutes before he can return.', 'gray')],
     model='bm:royal_marker', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
item(COIN, 'minecraft:compass', "The King's Coin", COL,
     ['A heavy gold coin, gnawed at the edge, a fat', 'crowned rat on its face. Its needle points down.',
      ('The Compass of Bonds\' twin: under the Loom Sanctuary,', 'gold'), ('at the bottom of the world, someone counts his hoard.', 'gold'),
      ('Stand beneath the island holding it, and sneak.', 'blue')],
     model=f'bm:{COIN}', glint=True, stack=1, cat='map',
     comps={'minecraft:lodestone_tracker': {'target': {'dimension': 'minecraft:overworld', 'pos': IntArray([int(THRONE[0]), FY, int(THRONE[2])])}, 'tracked': False}})


class RatKing(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'ratking', 'The Rat King', COL, LINE, 'p262', 'rw', 'qw'
    A = RF2.art(A)
    MENU, PET_HP, PET_CD, ITEM = 5450, 44, 120, ITEM
    pron, they = 'him', 'he'
    FACE = dict(A.FACE_MAP)
    ATTRS = dict(armor=8, attack_damage=5, movement_speed=0.34, follow_range=32, step_height=1.1)
    SCALE, HIT = HOST_BIG, HIT_BIG
    BOX_FIT = True
    BUTTONS = ((6, 'Companion Size: on / off', 'The Rat King at a companion\'s size - about a head shorter than you (his ego, as tall as ever). '
                                               'Off: as large and imposing as he sat on his throne.', 'p262/csz/toggle'),
               (7, 'Gifts: on / off', 'His loans now and then, and the King\'s Cut from your kills. Off: none (your pockets stay tidy).', 'p280/gift/rk'))
    CYCLE = P235.cycle((240, [(0, 'idle_a'), (80, 'idle_b'), (160, 'idle_c'), (210, 'idle_a')]), (240, [(0, 'sit_a'), (120, 'sit_b')]),
                       (None, [(0, 'happy')]),
                       {7: (None, [(0, 'swat_up'), (4, 'swat')]),
                        11: (None, [(0, 'decree_up'), (8, 'decree'), (16, 'idle_a')]),
                        12: (None, [(0, 'whistle_a'), (10, 'whistle'), (26, 'idle_a')]),
                        14: (None, [(0, 'gift'), (18, 'cut'), (28, 'idle_a')])})
    DUR = dict(P235._DUR, swat_up=4, swat=2, decree_up=6, decree=2, whistle_a=6, whistle=4, cut_a=4, cut=6, gift=8, bow=12,
               throne_a=30, throne_b=30, rise=10)
    QUIPS = ['"Bite it. Always bite it. That\'s how you know."', '(he counts the coins in his cape. He loses count. He starts again, happily.)',
             '"Everybody owes somebody. You owe ME, for a start."', '"A king never runs. A king... proceeds briskly."',
             '(he polishes his crown on his sleeve, then checks his reflection in it)', '"Fifty friends, and a king. Not a bad hoard, that."']
    HELLO = ('(the Rat King proceeds, briskly, back to your side)', '(a grate rattles somewhere - and the Rat King steps out of the dark, crown first)',
             '(he bows, sweeps his cape round himself, and is gone down some crack you hadn\'t noticed)')
    SIT = ('"Up, then. The hoard won\'t count itself."', '(he settles on his haunches, the sceptre across his lap, and starts counting)')
    FAINT = '"Put it... on my tab..."'
    NOT_YOURS = '(he looks you up and down) "You\'re not on my books. Yet."'
    POWERS = [('Sceptre Swat', 'a foe within reach: the cheese sceptre hauled back and brought down, 7'),
              ('Sceptre Slam', 'two or more foes near, every 12 s: he rears up and slams the sceptre into the floor - 6 to each, knocked back and slowed'),
              ('The Court', 'charged, every minute: a whistle - his court rats boil up out of the cracks round every foe within 8 and bite (4, and 4 more), weakened'),
              ('A Loan, With Interest', 'out of a fight beside you, every minute: a coin\'s worth of something - with a little bow'),
              ("The King's Cut", 'every monster you kill with him near: one in three pays a tithe - gold nuggets, now and then an emerald, very rarely a Token'),
              ('Bonds and Debts', 'with the Keeper of Bonds out too: Luck and Haste for you - one weaves the bonds, the other keeps the books'),
              ('Companion Size', 'his menu: as large and imposing as on his throne, or about a head shorter than you - his hitbox with it')]
    INTRO = [T('The Rat King', COL, bold=True), T(' - the Keeper\'s counterpart: where it weaves every bond, he keeps the books on them. ', 'gray'),
             T('"A debt is a bond too, if you ask me."', LINE, italic=True)]
    BURST = ['particle minecraft:dust{color:[1.0,0.78,0.2],scale:1.2} ~ ~1.2 ~ 0.5 0.8 0.5 0 20', 'particle minecraft:large_smoke ~ ~0.6 ~ 0.4 0.4 0.4 0.02 10',
             'particle minecraft:wax_on ~ ~1.4 ~ 0.5 0.7 0.5 0 10']
    FADE_SOUND = 'playsound minecraft:entity.rabbit.ambient neutral @a[distance=..20] ~ ~ ~ 0.8 0.6'
    SUMMON_EXTRA = ['playsound minecraft:block.chain.break neutral @a[distance=..24] ~ ~ ~ 0.6 0.7', 'playsound minecraft:entity.rabbit.ambient neutral @a[distance=..24] ~ ~ ~ 1 0.5']
    ENC_POSES = [(0, 'throne_a'), (40, 'throne_b')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 20 run particle minecraft:wax_on ~ ~2 ~ 0.5 0.5 0.5 0 3'
    ADV = ('The Rat King', 'Pay the Rat King tribute in his Counting House, under the Loom Sanctuary - and catch the thief in his court')
    ADMIN_HINT = 'Meet every other follower: the King\'s Coin, the Compass of Bonds\' twin, leads down to his Counting House.'
    MEET_HINT = 'Meet every other follower, then follow the King\'s Coin down, under the Loom Sanctuary.'


RP.register(RatKing)
RF2.setup(RatKing, 'head')

_DOLL = 'A doll of the Rat King - a big crowned head with beady ruby eyes and buck teeth, a little crimson cape, and a tiny cheese sceptre.'
item('doll_ratking', TOTEM, 'Rat King Doll', COL, [_DOLL, ('Right-click a block: set it down.', 'blue'), ('Right-click it: it twirls.', 'blue'),
                                                   ('Sneak + punch: pick it up.', 'gray')], model='bm:doll_ratking', stack=16, cat='fun', comps=hold('none'))
HOLD['doll_ratking'] = 'bm:p141/doll_ratking/use'
P141.DOLLS.append(('doll_ratking', RatKing.NAME, COL, _DOLL, 'minecraft:wax_on', 'minecraft:entity.rabbit.ambient', 'minecraft:poof'))
P141.DOLL_FROM['doll_ratking'] = (ITEM, dict(A.DOLL))      # (the default chibi warp)
P134.FIT[ITEM] = A.FIT

# ---- his pairs with Bender and Mr. Capshun (Henry's and Nia's: cat_bonds)
import phase188 as P188
_O = P188.O
_eff = lambda *es: [f'effect give {_O} minecraft:{e} 3 {a} true' for e, a in es]
P188.VNAME.update({'ratking': 'the Rat King'})
P188.PAIRS.update({
    'rw_bender': ('ratking', 'bender', 'Good Boy, Bad Debts', '#e0a860', 'The Rat King and Bender - a king, and the only one in the court who fetches',
                  _eff(('speed', 0), ('luck', 0)),
                  [('ratking', '"Fetch. FETCH. That is a gold coin, you beast, bring it - "'), ('bender', '(brings it back, very wet, tail going like mad)')],
                  [('bender', '(drops a stick at his feet, and waits)', 'ratking', '"...One throw. ONE. Kings do not play."')]),
    'rw_capshun': ('ratking', 'capshun', 'Royal Biographer', '#f0f0f0', 'The Rat King and Mr. Capshun - a king, and the narrator who keeps his legend',
                   _eff(('luck', 0), ('haste', 0)),
                   [('capshun', '[Mr. Capshun narrates: "And the Rat King, mightiest of all rats, stood exactly as tall as a medium dog."]'), ('ratking', '"STRIKE THAT."')],
                   [('ratking', '"Write that I was magnificent."', 'capshun', '[Mr. Capshun narrates: "He was, the narrator admits, fairly magnificent."]')]),
})
P188.ICON.update({'rw_bender': f'bm:{ITEM}', 'rw_capshun': f'bm:{ITEM}'})


def extend_offers(O, offer):
    pass


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    RP.rp(RatKing, R, A.icon_royal_marker())
    RF2.faces(RatKing, 'head', R)
    R.ICONS[COIN] = A.icon_kings_coin()


def textures():
    return A.textures()


def generate_early(G):
    RP.contract(RatKing, G)


def _abilities(G, X):
    fn, pfx, foe, me = G.fn, X.pfx, X.foe, X.me
    snd = lambda s, v=0.6, p=1.0: f'playsound minecraft:{s} neutral @a[distance=..16] ~ ~ ~ {v} {p}'
    K = dict(melee=dict(st=7, x=8, at=3, cd=22, reach=2.8, face='serious', go=[snd('entity.player.attack.sweep', 0.5, 0.7)]),
             crowd=dict(st=11, x=18, at=9, cd=240, r=4, n=2, face='serious', go=[snd('entity.rabbit.hurt', 0.8, 0.5)]),
             charged=dict(st=12, x=32, at=[20, 8], cd=1200, r=8, face='serious', go=[snd('entity.parrot.imitate.vex', 0.6, 1.6)]),
             kind=dict(st=14, x=30, at=12, cd=1200, face='happy'))
    lines = P235.kit(G, X, K)
    P235.melee(G, X, 7, 2.8, ['particle minecraft:sweep_attack ~ ~1 ~ 0.1 0.1 0.1 0 1', 'particle minecraft:wax_on ~ ~1 ~ 0.3 0.3 0.3 0 6'],
               'minecraft:entity.player.attack.strong')
    # SCEPTRE SLAM: the sceptre into the floor - every foe within 4: 6, thrown back and slowed; a ring of gold dust
    fn(f'{pfx}/crowd', X.hit(6) + [f'execute as @e[{foe},distance=..4] at @s run function bm:{pfx}/slammed',
                                   'particle minecraft:dust{color:[1.0,0.78,0.2],scale:1.6} ~ ~0.2 ~ 2 0.1 2 0 40', 'particle minecraft:explosion ~ ~0.3 ~ 0.4 0 0.4 0 1',
                                   snd('entity.iron_golem.attack', 1.0, 0.6), snd('block.anvil.land', 0.5, 1.4)] + X.end)
    fn(f'{pfx}/slammed', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 3 1', f'execute facing entity @e[type=minecraft:wolf,tag={me},limit=1] feet rotated ~180 0 if block ^ ^ ^1 #bm:grap_pass if block ^ ^1 ^1 #bm:grap_pass run tp @s ^ ^ ^1'])
    # THE COURT: a whistle - his rats boil up round every foe within 8 (court rats: displays a second and a half), and bite; again
    rat = {'Tags': ['bm.rwrat'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:rat3d_grey'}},
           'item_display': 'fixed', 'teleport_duration': Int(3),
           'transformation': {'left_rotation': RF.IDENT, 'right_rotation': RF.IDENT, 'translation': [F(0), F(0.25), F(0)], 'scale': [F(0.9)] * 3}}
    fn(f'{pfx}/charged', X.hit(4) + [f'execute as @e[{foe},distance=..8] at @s run function bm:{pfx}/courted', f'tag @s remove {me}',
                                     snd('entity.rabbit.ambient', 1.0, 0.5), snd('block.gravel.break', 1.0, 0.7)])
    fn(f'{pfx}/courted', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:weakness 6 0', 'tag @s add bm.rwct'] +
       [f'execute positioned ^{dx} ^ ^{dz} run summon minecraft:item_display ~ ~ ~ {snbt(rat)}' for dx, dz in ((0.7, 0.4), (-0.6, 0.5), (0.1, -0.7))] +
       ['particle minecraft:block{block_state:"minecraft:gravel"} ~ ~0.2 ~ 0.5 0.1 0.5 0 16'])
    fn(f'{pfx}/charged2', X.hit(4) + [f'execute as @e[tag=bm.rwct,distance=..14] at @s run function bm:{pfx}/bitten'] + X.end)
    fn(f'{pfx}/bitten', [f'function bm:{pfx}/hurt', 'tag @s remove bm.rwct', 'particle minecraft:crit ~ ~0.6 ~ 0.4 0.3 0.4 0.2 10',
                         'playsound minecraft:entity.rabbit.attack neutral @a[distance=..16] ~ ~ ~ 1 0.6'])
    # (the court's rats: they scurry round their foe, then go back down the cracks - a display lives 30 ticks)
    X.tick += ['execute as @e[type=minecraft:item_display,tag=bm.rwrat] at @s run function bm:p262/rat_tick']
    fn('p262/rat_tick', ['scoreboard players add @s bm.qwrl 1', 'tp @s ~ ~ ~ ~24 0',
                         'execute if score @s bm.qwrl matches 30.. run particle minecraft:block{block_state:"minecraft:gravel"} ~ ~0.1 ~ 0.2 0 0.2 0 6',
                         'execute if score @s bm.qwrl matches 30.. run kill @s'])
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.qwrl dummy']
    G.OBJECTIVES.append('bm.qwrl')
    # A LOAN, WITH INTEREST: out of a fight, a coin's worth of something - one of six
    say = lambda line: 'execute unless entity @s[tag=bm.hush] run ' + G.title('@s', 'actionbar', [T('The Rat King: ', COL, bold=True), T(line, LINE, italic=True)])
    LOANS = [(['give @s minecraft:gold_nugget 9'], '"A loan. Nine nuggets. With interest - I\'ll remember."'),
             (['give @s minecraft:gold_ingot 2'], '"Two ingots. Don\'t spend them all on one heist."'),
             (['give @s minecraft:emerald 1'], '"An emerald. Bit it myself. It\'s real."'),
             (['give @s minecraft:golden_carrot 4'], '"Golden carrots. The cheese is MINE, but these you can have."'),
             (['effect give @s minecraft:luck 300 0 true', 'effect give @s minecraft:hero_of_the_village 120 0 true'], '"I put in a word for you. The rats will treat you like family."'),
             (['effect give @s minecraft:haste 120 0 true'], '"Dig, dig. A good hoard doesn\'t find itself."')]
    fn(f'{pfx}/kind', ['execute on owner if entity @s[distance=..8,tag=!bm.nogift_rk] at @s run function bm:p262/loan'])
    fn('p262/loan', [f'execute store result score #r bm.rng run random value 1..{len(LOANS)}'] +
       [f'execute if score #r bm.rng matches {i + 1} run function bm:p262/loan/{i + 1}' for i in range(len(LOANS))] +
       ['particle minecraft:wax_on ~ ~1.4 ~ 0.3 0.3 0.3 0 10', 'playsound minecraft:entity.allay.item_given player @s ~ ~ ~ 1 0.8'])
    for i, (cmds, line) in enumerate(LOANS):
        fn(f'p262/loan/{i + 1}', cmds + [say(line)])
    return lines


def _encounter(G, X):
    """the Counting House: his audience - the tribute, the Shell of Rats, the Royal Marker"""
    fn, tellraw, title, give = G.fn, G.tellraw, G.title, G.give
    import phase28 as P28
    S = X.S
    ENC = f'@e[type=minecraft:interaction,tag=bm.rwenc,{ROOM}]'
    here = '@e[type=minecraft:interaction,tag=bm.rwenc,limit=1,sort=nearest]'
    objs = ['bm.qwg', 'bm.qwgt', 'bm.qwth', 'bm.qwo', 'bm.qwsl', 'bm.qwsa']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + ['scoreboard players set #5 bm.rng 5']
    G.OBJECTIVES += objs
    marker = f'items entity @s container.* {X.holds(ITEM)}'
    rsay = lambda txt: title('@s', 'actionbar', [T('The Rat King: ', COL, bold=True), T(txt, LINE)])
    rchat = lambda parts, who='@s': tellraw(who, [T('The Rat King: ', COL, bold=True)] + parts)
    q = lambda s: T(s, LINE)
    # (the poses only his throne asks for - the rest are the follower's own)
    for name in ('throne_a', 'throne_b', 'bow', 'cut', 'whistle_a', 'gift', 'happy'):
        if f'p262/pose/{name}' not in G.FUNCS:
            fn(f'p262/pose/{name}', RF.pose(RatKing.A, A.POSES[name], A.RIG_SCALE, RatKing.DUR.get(name, 6), X.psel, swap=RatKing.SWAP, keep=True) +
               RatKing.POSE_EXTRA(name, X.psel))
    # ---- he's there: a coin-holder in the hall without his Marker - and nobody's audience on yet
    X.second.append(f'execute in minecraft:overworld as @a[{ROOM},tag=bm.rwcoin,tag=!bm.rwmet,gamemode=!spectator] unless {marker} run function bm:p262/enc/want')
    fn('p262/enc/want', [f'execute in minecraft:overworld if entity {ENC} run return 0',
                         f'execute in minecraft:overworld positioned {THRONE[0]} {THRONE[1]} {THRONE[2]} rotated 0 0 run function bm:p262/enc/arrive'])
    fn('p262/enc/arrive', ['function bm:p262/enc/spawn', 'particle minecraft:large_smoke ~ ~1 ~ 0.6 0.8 0.6 0.02 30',
                           'playsound minecraft:entity.rabbit.ambient neutral @a[distance=..32] ~ ~ ~ 1 0.5',
                           'playsound minecraft:block.chain.place neutral @a[distance=..32] ~ ~ ~ 1 0.6',
                           tellraw(f'@a[{ROOM},tag=bm.rwcoin,tag=!bm.rwmet]', [T('On a throne of gold at the end of the hall, something very large and very pleased with itself ', LINE, italic=True),
                                                                              T('is counting coins. It does not look up. It knows you are here.', 'gray', italic=True)])])
    # ---- speaking to him
    fn('p262/enc/talk', [f'execute if score {X.here} bm.qwg matches 2.. unless score {X.here} bm.qwo = @s bm.pid run return run ' + rsay('"Wait your turn. A king holds one audience at a time."'),
                         'execute if entity @s[tag=bm.rwmet] run return run ' + rsay('"You have my Marker. Go on - I\'m right behind you. Briskly."'),
                         f'execute if {marker} run return run ' + rsay('"You have my Marker. Go on - I\'m right behind you. Briskly."'),
                         'execute unless entity @s[tag=bm.rwcoin] run return run function bm:p262/enc/not_yet',
                         f'execute if score {X.here} bm.qwg matches 2.. run return run ' + rsay('"Eyes on the TABLE. Find my coin."'),
                         'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                         'execute if entity @s[tag=bm.rwpaid] run return run function bm:p262/sh/begin',
                         'function bm:p262/aud/ask'])
    fn('p262/enc/not_yet', [rchat([T('(he squints at you over a coin) ', 'gray', italic=True),
                                   q('"How did YOU get down here? No, don\'t tell me. Come back when you\'ve a coin of mine - and fifty friends to show for it."')])])
    # ---- THE TRIBUTE: a dialog of what he'll take (whichever you can pay)
    trib = [(1, '32 Gold Ingots', 'minecraft:gold_ingot', 32, '"Gold. Good, honest, heavy gold." (he bites an ingot)'),
            (2, '16 Gutter Coins', '*[minecraft:custom_data~{bm:"gutter_coin"}]', 16, '"My own face on every one of them. Excellent taste."'),
            (3, 'A Golden Cheese Wheel', '*[minecraft:custom_data~{bm:"golden_cheese_wheel"}]', 1, '"MY cheese! Where did you - never mind. Never mind. It\'s home now."')]
    dlg = P28.multi([T('THE RAT KING\'S TRIBUTE', COL, bold=True)],
                    [P28.body([T('"A king takes his cut. Everyone pays - the market, the gutter, the rats in the walls. You too."', LINE)], 300),
                     P28.body([T('(Pay one tribute, once. Then the audience.)', 'gray')], 300)],
                    [P28.btn(T(nm, COL, bold=True), AUD + n, width=150, tooltip=T(f'Hand him {nm.lower()}.', 'gray')) for n, nm, *_r in trib],
                    columns=1, exit_label='Not today')
    fn('p262/aud/ask', [rchat([T('(he does not look up from his counting) ', 'gray', italic=True),
                               q('"Fifty friends? Fifty DEBTS, I call it. Everybody owes somebody. Now - you owe ME."')]),
                        f'scoreboard players set @s bm.menu {AUD}', f'dialog show @s {snbt(dlg)}'])
    G.FUNCS['p28/act'] += [f'execute if score #act bm.pay matches {AUD + n} run return run function bm:p262/aud/act' for n, *_r in trib]
    fn('p262/aud/act', [f'execute unless score @s bm.menu matches {AUD} run return run function bm:p28/stale',
                        f'execute unless entity @s[{ROOM}] run return run ' + title('@s', 'actionbar', T('(You are not in his hall.)', 'gray')),
                        'execute if entity @s[tag=bm.rwpaid] run return run function bm:p262/sh/begin'] +
       [f'execute if score #act bm.pay matches {AUD + n} run return run function bm:p262/aud/pay{n}' for n, *_r in trib])
    for n, nm, what, k, line in trib:
        fn(f'p262/aud/pay{n}', [f'execute store result score #n bm.rng run clear @s {what} 0',
                                f'execute if score #n bm.rng matches ..{k - 1} run return run ' + rsay(f'"{nm}? You haven\'t got {nm.lower()}. Don\'t waste a king\'s time."'),
                                f'clear @s {what} {k}', 'tag @s add bm.rwpaid', 'playsound minecraft:entity.villager.yes player @s ~ ~ ~ 1 0.6',
                                'playsound minecraft:block.chain.place player @s ~ ~ ~ 1 1.4', rchat([q(line)]),
                                f'execute as {here} at @s run function bm:p262/pose_at/cut', 'function bm:p262/sh/begin'])
    for name in ('cut', 'bow'):
        fn(f'p262/pose_at/{name}', ['execute as @e[type=minecraft:item_display,tag=bm.rwencp,distance=..6] run tag @s add bm.rwsel',
                                    f'function bm:p262/pose/{name}', 'tag @e[tag=bm.rwsel] remove bm.rwsel'])
    # ---- THE SHELL OF RATS (the hall's interaction keeps the game: bm.qwg its stage - 2 the reveal, 3 the shuffle, 4 your pick, 5 won;
    #      bm.qwgt its clock, bm.qwth the thief's place, bm.qwo whose game; the rats keep their place in bm.qwsl, the five cups too)
    ratd = lambda i: {'Tags': ['bm.rwsr', 'bm.rwshell'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:rat3d_grey'}},
                      'item_display': 'fixed', 'teleport_duration': Int(8), 'Rotation': [F(0), F(0)],      # (facing you, south, across the table)
                      'transformation': {'left_rotation': RF.IDENT, 'right_rotation': RF.IDENT, 'translation': [F(0), F(0.0), F(0)], 'scale': [F(0.8)] * 3}}
    cup = {'Tags': ['bm.rwcup', 'bm.rwshell'], 'width': F(0.7), 'height': F(0.7), 'response': B(1)}
    coin = {'Tags': ['bm.rwgc', 'bm.rwshell'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:{COIN}'}},
            'item_display': 'fixed', 'billboard': 'vertical', 'brightness': {'block': Int(15), 'sky': Int(15)},
            'transformation': {'left_rotation': RF.IDENT, 'right_rotation': RF.IDENT, 'translation': [F(0), F(0.9), F(0)], 'scale': [F(0.45)] * 3}}
    fn('p262/sh/begin', ['scoreboard players operation #o bm.rng = @s bm.pid',
                         f'execute as {here} at @s run function bm:p262/sh/start',
                         rchat([T('(he snaps his claws; five grey rats scurry up onto the counting table) ', 'gray', italic=True),
                                q('"Loyalty, now. One of my court has pinched my favourite coin. Watch closely. Find the thief - and you\'re on my books."')])])
    fn('p262/sh/start', ['scoreboard players operation @s bm.qwo = #o bm.rng', 'function bm:p262/sh/clear',
                         'execute as @e[type=minecraft:item_display,tag=bm.rwencp,distance=..6] run tag @s add bm.rwsel',
                         'function bm:p262/pose/whistle_a', 'tag @e[tag=bm.rwsel] remove bm.rwsel'] +
       [f'summon minecraft:item_display {x} {y} {z} {snbt(ratd(i))}' for i, (x, y, z) in enumerate(SLOTS)] +
       [f'summon minecraft:interaction {x} {y} {z} {snbt(cup)}' for i, (x, y, z) in enumerate(SLOTS)] +
       [f'scoreboard players set @e[tag=bm.rwshell,x={x},y={y},z={z},distance=..0.3] bm.qwsl {i}' for i, (x, y, z) in enumerate(SLOTS)] +
       ['function bm:p262/sh/round'])
    fn('p262/sh/round', ['scoreboard players set @s bm.qwg 2', 'scoreboard players set @s bm.qwgt 0',
                         'execute store result score @s bm.qwth run random value 0..4', 'scoreboard players operation #th bm.rng = @s bm.qwth',
                         'execute as @e[type=minecraft:item_display,tag=bm.rwsr] if score @s bm.qwsl = #th bm.rng at @s run summon minecraft:item_display ~ ~ ~ ' + snbt(coin)])
    X.tick.append(f'execute as @e[type=minecraft:interaction,tag=bm.rwenc] if score @s bm.qwg matches 2..5 at @s run function bm:p262/sh/tick')
    SW, NSW = 12, 6                             # (a swap every 12 ticks; six of them)
    fn('p262/sh/tick', ['scoreboard players add @s bm.qwgt 1', 'scoreboard players operation #th bm.rng = @s bm.qwth',
                        'execute if score @s bm.qwg matches 2 run function bm:p262/sh/reveal',
                        'execute if score @s bm.qwg matches 3 run function bm:p262/sh/shuffle',
                        'execute if score @s bm.qwg matches 4 if score @s bm.qwgt matches 1200.. run function bm:p262/sh/timeout',
                        'execute if score @s bm.qwg matches 5 run function bm:p262/sh/won_tick'])
    fn('p262/sh/reveal', ['execute if score @s bm.qwgt matches 1..30 as @e[type=minecraft:item_display,tag=bm.rwsr] if score @s bm.qwsl = #th bm.rng at @s run particle minecraft:wax_on ~ ~0.6 ~ 0.15 0.15 0.15 0 1',
                          'execute if score @s bm.qwgt matches 30 run kill @e[type=minecraft:item_display,tag=bm.rwgc,distance=..16]',
                          'execute if score @s bm.qwgt matches 30 as @e[type=minecraft:item_display,tag=bm.rwsr] if score @s bm.qwsl = #th bm.rng at @s run playsound minecraft:entity.generic.eat neutral @a[distance=..16] ~ ~ ~ 0.6 1.6',
                          'execute if score @s bm.qwgt matches 40.. run scoreboard players set @s bm.qwgt 0',
                          'execute if score @s bm.qwgt matches 0 run scoreboard players set @s bm.qwg 3'])
    fn('p262/sh/shuffle', [f'execute if score @s bm.qwgt matches {SW * k} run function bm:p262/sh/swap' for k in range(1, NSW + 1)] +
       [f'execute if score @s bm.qwgt matches {SW * NSW + 10} run function bm:p262/sh/pick_now'])
    fn('p262/sh/swap', ['execute store result score #a bm.rng run random value 0..4', 'execute store result score #b bm.rng run random value 1..4',
                        'scoreboard players operation #b bm.rng += #a bm.rng', 'scoreboard players operation #b bm.rng %= #5 bm.rng',
                        'execute if score @s bm.qwth = #a bm.rng run scoreboard players set #tf bm.rng 1',
                        'execute if score @s bm.qwth = #b bm.rng run scoreboard players set #tf bm.rng 2',
                        'execute as @e[type=minecraft:item_display,tag=bm.rwsr] if score @s bm.qwsl = #a bm.rng run tag @s add bm.rwsa',
                        'execute as @e[type=minecraft:item_display,tag=bm.rwsr] if score @s bm.qwsl = #b bm.rng run tag @s add bm.rwsb',
                        'execute as @e[tag=bm.rwsa] run scoreboard players operation @s bm.qwsl = #b bm.rng',
                        'execute as @e[tag=bm.rwsb] run scoreboard players operation @s bm.qwsl = #a bm.rng',
                        'execute as @e[tag=bm.rwsa] run function bm:p262/sh/go', 'execute as @e[tag=bm.rwsb] run function bm:p262/sh/go',
                        'tag @e[tag=bm.rwsa] remove bm.rwsa', 'tag @e[tag=bm.rwsb] remove bm.rwsb',
                        'execute if score #tf bm.rng matches 1 run scoreboard players operation @s bm.qwth = #b bm.rng',
                        'execute if score #tf bm.rng matches 2 run scoreboard players operation @s bm.qwth = #a bm.rng', 'scoreboard players set #tf bm.rng 0',
                        'playsound minecraft:entity.rabbit.jump neutral @a[distance=..16] ~ ~ ~ 0.6 1.4'])
    fn('p262/sh/go', [f'execute if score @s bm.qwsl matches {i} run tp @s {x} {y} {z}' for i, (x, y, z) in enumerate(SLOTS)])
    fn('p262/sh/pick_now', ['scoreboard players set @s bm.qwg 4', 'scoreboard players set @s bm.qwgt 0',
                            'scoreboard players operation #o bm.rng = @s bm.qwo',
                            'execute as @a[distance=..24] if score @s bm.pid = #o bm.rng run ' + rsay('"Well? Which one? Go on - give the thief a good poke."')])
    # (a poke: the cup tells its place; the one who poked is asked)
    X.fast += ['execute as @e[type=minecraft:interaction,tag=bm.rwcup] if data entity @s attack at @s run function bm:p262/sh/poked',
               'execute as @e[type=minecraft:interaction,tag=bm.rwcup] if data entity @s interaction at @s run function bm:p262/sh/poked']
    fn('p262/sh/poked', ['scoreboard players operation #pk bm.rng = @s bm.qwsl', 'execute on attacker run function bm:p262/sh/pick',
                         'execute on target run function bm:p262/sh/pick', 'data remove entity @s attack', 'data remove entity @s interaction'])
    fn('p262/sh/pick', [f'execute unless score {here} bm.qwg matches 4 run return 0', f'execute unless score {here} bm.qwo = @s bm.pid run return 0',
                        f'execute if score {here} bm.qwth = #pk bm.rng run return run function bm:p262/sh/right', 'function bm:p262/sh/wrong'])
    fn('p262/sh/wrong', [f'scoreboard players operation #th bm.rng = {here} bm.qwth',
                         'execute as @e[type=minecraft:item_display,tag=bm.rwsr] if score @s bm.qwsl = #th bm.rng at @s run particle minecraft:wax_on ~ ~0.6 ~ 0.2 0.2 0.2 0 12',
                         'playsound minecraft:entity.rabbit.hurt player @s ~ ~ ~ 1 1.4',
                         rchat([T('(the wrong rat squeaks, offended; the thief grins round a mouthful of gold) ', 'gray', italic=True), q('"Pfah. Again. Watch the TABLE this time."')]),
                         f'execute as {here} at @s run function bm:p262/sh/round'])
    fn('p262/sh/right', [f'execute as {here} run scoreboard players set @s bm.qwg 5', f'execute as {here} run scoreboard players set @s bm.qwgt 0',
                         'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.8 0.7', 'playsound minecraft:block.chain.break player @s ~ ~ ~ 1 1.2',
                         rchat([T('(the thief coughs up the coin; he catches it without looking, bites it, and - for the first time - looks straight at you) ', 'gray', italic=True),
                                q('"Sharp eyes. I like sharp eyes. Very well - you\'re on my books."')]),
                         f'execute as {here} at @s run function bm:p262/pose_at/bow'])
    fn('p262/sh/won_tick', ['execute if score @s bm.qwgt matches 10 run function bm:p262/sh/clear',
                            'execute if score @s bm.qwgt matches 40.. run function bm:p262/sh/give'])
    fn('p262/sh/give', ['scoreboard players set @s bm.qwg 0', 'scoreboard players operation #o bm.rng = @s bm.qwo', 'tag @s add bm.rwhere',
                        'execute as @a if score @s bm.pid = #o bm.rng at @s run function bm:p262/sh/given', 'tag @s remove bm.rwhere'])
    fn('p262/sh/given', [rchat([T('(he takes a sheet of vellum from his cape, writes on it with a flourish, and seals it with his signet in hot gold wax) ', 'gray', italic=True),
                                q('"The Royal Marker. You owe me one adventure. I\'ll be collecting - in person."')]),
                         'particle minecraft:wax_on ~ ~1 ~ 0.6 1 0.6 0 40', 'tag @s remove bm.rwpaid', 'function bm:p262/enc/joined'])
    fn('p262/sh/timeout', ['function bm:p262/sh/clear', 'scoreboard players set @s bm.qwg 0',
                           'scoreboard players operation #o bm.rng = @s bm.qwo', 'execute as @a if score @s bm.pid = #o bm.rng run ' + rsay('"Too slow. Speak to me again when you\'re awake."')])
    fn('p262/sh/clear', ['kill @e[tag=bm.rwshell,distance=..24]'])
    # (its clicks on the King's box run as the interaction: X.here tags it - rigpet's enc/click)
    G.FUNCS['p262/enc/gone'].insert(0, 'function bm:p262/sh/clear')
    X.second.append(f'execute in minecraft:overworld as @e[tag=bm.rwshell,{ROOM}] at @s unless entity @e[type=minecraft:interaction,tag=bm.rwenc,distance=..16] run kill @s')
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[tag=bm.rwshell]', 'kill @e[tag=bm.rwrat]']


def generate(G):
    fn, title, tellraw, give = G.fn, G.title, G.tellraw, G.give
    RP.build(RatKing, G, _abilities, _encounter)
    second, tick = G.FUNCS['loop/second'], G.FUNCS['tick']
    pfx = RatKing.pfx
    S = lambda s: f'bm.{RatKing.q}{s}'
    # ---- COMPANION SIZE (compsize): his rig at CSZ_K of its own size, his host and click box with it; the owner's bm.rwcs, kept
    say = lambda txt: title('@s', 'actionbar', [T('The Rat King: ', COL, bold=True), T(txt, LINE)])
    CS.build(G, pfx, 'bm.rwcs', 'bm.rwcz', S('s'), HOST_BIG, HOST_SMALL,
             say('"...Fine. Smaller. A king can be FUN-SIZED. Tell no one." (Companion Size: on)'),
             say('"Ahh. Room for a crown. A king should LOOM." (Companion Size: off)'), hit=('bm.rwhit', HIT_BIG, HIT_SMALL))
    CS.LATE.append((pfx, CSZ_K, 'bm.rwcz', ()))
    T_ = G.FUNCS[f'{pfx}/tick']
    assert T_[0] == 'scoreboard players operation #me bm.pid = @s bm.pid', T_[0]
    T_[1:1] = CS.sync(pfx, 'bm.rwcs', 'bm.rwcz', S('s'), HOST_BIG, HOST_SMALL)
    fn(f'{pfx}/box_fit', ['execute if entity @s[tag=bm.rwcz] run function bm:p262/box/small'])
    fn('p262/box/small', CS.resize('bm.rwhit', *HIT_SMALL))
    # ---- THE KING'S COIN: with the compass, once
    second.append('execute as @a[tag=bm.kbcomp,tag=!bm.rwcoin] at @s run function bm:p262/coin')
    fn('p262/coin', ['tag @s add bm.rwcoin', give(COIN), 'scoreboard players set #rwwant bm.p2 1',
                     'playsound minecraft:block.chain.place player @s ~ ~ ~ 1 0.6', 'playsound minecraft:entity.rabbit.ambient player @s ~ ~ ~ 1 0.5',
                     tellraw('@s', [T("The King's Coin ", COL, bold=True), T('is in your pack too - a fat gold coin, gnawed at the edge. Its needle points ', 'gray'),
                                    T('down', COL, bold=True), T('. Far beneath the Loom Sanctuary, someone is counting.', 'gray')])])
    G.FUNCS['load'][-1:-1] = ['execute if entity @a[tag=bm.rwcoin] run scoreboard players set #rwwant bm.p2 1']
    # ---- the Counting House: built from commands the first time it's wanted (or after a version bump)
    fl = f'{CX - HALF - 3} {CZ - HALF - 3} {CX + HALF + 3} {CZ + HALF + 3}'
    second.append(f'execute if score #rwwant bm.p2 matches 1 unless score #rwver bm.p2 matches {RVER} run function bm:p262/room/try')
    fn('p262/room/try', [f'execute in minecraft:overworld run forceload add {fl}',
                         f'execute in minecraft:overworld store success score #rwload bm.p2 if loaded {CX - HALF - 2} {FY} {CZ - HALF - 2} if loaded {CX + HALF + 2} {FY} {CZ + HALF + 2}',
                         'execute unless score #rwload bm.p2 matches 1 run return 0',
                         'execute in minecraft:overworld run function bm:p262/room/build', f'scoreboard players set #rwver bm.p2 {RVER}',
                         f'execute in minecraft:overworld run forceload remove {fl}'])
    fn('p262/room/build', _room())
    # ---- the way down (sneak, holding the coin, in the island's column - above the hall), and up (the mouse hole)
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in ('bm.qwd', 'bm.rwbx', 'bm.rwby', 'bm.rwbz')]
    G.OBJECTIVES += ['bm.qwd', 'bm.rwbx', 'bm.rwby', 'bm.rwbz']
    holds = f'items entity @s weapon.* *[minecraft:custom_data~{{bm:"{COIN}"}}]'
    second += [f'execute in minecraft:overworld as @a[{DOWNCOL}] if {holds} if predicate bm:p20/sneaking at @s run function bm:p262/down',
               f'execute in minecraft:overworld as @a[{DOWNCOL},scores={{bm.qwd=1..}}] unless predicate bm:p20/sneaking run scoreboard players set @s bm.qwd 0']
    fn('p262/down', ['execute unless score #rwver bm.p2 matches 1.. run return run ' + title('@s', 'actionbar', T('(Somewhere far below, something is still digging. A moment.)', 'gray', italic=True)),
                     'scoreboard players add @s bm.qwd 1', 'particle minecraft:block{block_state:"minecraft:gravel"} ~ ~0.1 ~ 0.4 0 0.4 0 12',
                     'playsound minecraft:block.gravel.break player @s ~ ~ ~ 1 0.6',
                     'execute if score @s bm.qwd matches ..2 run return run ' + title('@s', 'actionbar', T('The ground shifts under your feet... something is gnawing at it...', COL, italic=True)),
                     'scoreboard players set @s bm.qwd 0',
                     'execute store result score @s bm.rwbx run data get entity @s Pos[0] 100', 'execute store result score @s bm.rwby run data get entity @s Pos[1] 100',
                     'execute store result score @s bm.rwbz run data get entity @s Pos[2] 100',
                     'scoreboard players operation #me bm.pid = @s bm.pid', 'execute as @e[type=minecraft:wolf,tag=!bm.ffpet,distance=..32] if score @s bm.pid = #me bm.pid run tag @s add bm.rwcarry', 'execute as @e[type=minecraft:cat,tag=!bm.ffpet,distance=..32] if score @s bm.pid = #me bm.pid run tag @s add bm.rwcarry',
                     f'tp @s {LAND[0]} {LAND[1]} {LAND[2]} 180 0',
                     'tp @e[tag=bm.rwcarry] @s', 'tag @e[tag=bm.rwcarry] remove bm.rwcarry',
                     f'execute positioned {LAND[0]} {LAND[1]} {LAND[2]} run particle minecraft:large_smoke ~ ~1 ~ 0.5 1 0.5 0.03 30',
                     f'execute positioned {LAND[0]} {LAND[1]} {LAND[2]} run playsound minecraft:block.gravel.fall player @a[distance=..24] ~ ~ ~ 1 0.6',
                     title('@s', 'actionbar', T('The Counting House.', COL, bold=True))])
    second.append(f'execute in minecraft:overworld positioned {HOLE[0]} {HOLE[1]} {HOLE[2]} as @a[distance=..1.3] at @s run function bm:p262/up')
    fn('p262/up', ['execute store result storage bm:p262 up.x double 0.01 run scoreboard players get @s bm.rwbx',
                   'execute store result storage bm:p262 up.y double 0.01 run scoreboard players get @s bm.rwby',
                   'execute store result storage bm:p262 up.z double 0.01 run scoreboard players get @s bm.rwbz',
                   'scoreboard players operation #me bm.pid = @s bm.pid', 'execute as @e[type=minecraft:wolf,tag=!bm.ffpet,distance=..32] if score @s bm.pid = #me bm.pid run tag @s add bm.rwcarry', 'execute as @e[type=minecraft:cat,tag=!bm.ffpet,distance=..32] if score @s bm.pid = #me bm.pid run tag @s add bm.rwcarry',
                   'execute unless score @s bm.rwby matches -4000.. run return run function bm:p262/up_spawn',
                   'function bm:p262/up_to with storage bm:p262 up', 'tp @e[tag=bm.rwcarry] @s', 'tag @e[tag=bm.rwcarry] remove bm.rwcarry', 'playsound minecraft:block.gravel.break player @s ~ ~ ~ 1 0.8',
                   title('@s', 'actionbar', T('(back up the rat-run, into the light)', 'gray', italic=True))])
    fn('p262/up_to', ['$tp @s $(x) $(y) $(z)'])
    fn('p262/up_spawn', [f'tp @s {int(P253.AX // 1)} 100 {int(P253.AZ // 1)}', 'spreadplayers ~ ~ 0 4 false @s'] + ['tp @e[tag=bm.rwcarry] @s', 'tag @e[tag=bm.rwcarry] remove bm.rwcarry'])
    # ---- nothing in the hall can be broken (adventure while you're in it, as on the island)
    second += [f'execute in minecraft:overworld as @a[{ROOM},gamemode=survival] run function bm:p262/adv/in',
               'execute as @a[tag=bm.rwadv,gamemode=adventure] at @s unless function bm:p262/in_hall run function bm:p262/adv/out']
    fn('p262/in_hall', [f'execute in minecraft:overworld if entity @s[{ROOM}] run return 1', 'return 0'])
    fn('p262/adv/in', ['tag @s add bm.rwadv', 'gamemode adventure @s'])
    fn('p262/adv/out', ['tag @s remove bm.rwadv', 'gamemode survival @s'])
    # ---- THE KING'S CUT: every monster you kill with him near - one in three pays a tithe
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.rwmk minecraft.custom:minecraft.mob_kills']
    G.OBJECTIVES.append('bm.rwmk')
    second += ['execute as @a[scores={bm.rwmk=1..}] at @s run function bm:p262/cut/you']
    fn('p262/cut/you', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #rk bm.rng 0',
                        'execute as @e[type=minecraft:wolf,tag=bm.rwpet,tag=!bm.ffpet,distance=..16] if score @s bm.pid = #me bm.pid run scoreboard players set #rk bm.rng 1',
                        'execute if score #rk bm.rng matches 1 if score @s bm.rwmk matches 1.. unless entity @s[tag=bm.nogift_rk] run function bm:p262/cut/one',
                        'scoreboard players set @s bm.rwmk 0'])
    fn('p262/cut/one', ['scoreboard players remove @s bm.rwmk 1', 'execute store result score #r bm.rng run random value 1..300',
                        'execute if score #r bm.rng matches 1 run return run function bm:p262/cut/token',
                        'execute if score #r bm.rng matches 2..13 run return run function bm:p262/cut/emerald',
                        'execute if score #r bm.rng matches 14..100 run function bm:p262/cut/nuggets',
                        'execute if score @s bm.rwmk matches 1..8 run function bm:p262/cut/one'])
    cut = lambda what: ['particle minecraft:wax_on ~ ~1 ~ 0.3 0.4 0.3 0 6', 'playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.5 0.6',
                        'execute unless entity @s[tag=bm.hush] run ' + title('@s', 'actionbar', [T("The King's Cut: ", COL, bold=True), T(what, LINE, italic=True)])]
    fn('p262/cut/nuggets', ['execute store result score #n bm.rng run random value 2..5', 'execute if score #n bm.rng matches 2 run give @s minecraft:gold_nugget 2',
                            'execute if score #n bm.rng matches 3 run give @s minecraft:gold_nugget 3', 'execute if score #n bm.rng matches 4 run give @s minecraft:gold_nugget 4',
                            'execute if score #n bm.rng matches 5 run give @s minecraft:gold_nugget 5'] + cut('(he picks a few nuggets out of the remains, and tosses you your share)'))
    fn('p262/cut/emerald', ['give @s minecraft:emerald 1'] + cut('"An emerald! Bit it. Real. Yours - this once."'))
    fn('p262/cut/token', ['loot give @s loot bm:items/token'] + cut('"A TOKEN. Don\'t look at me like that. Fair\'s fair - it\'s yours."'))
    # ---- BONDS AND DEBTS: the Keeper out too, near you - Luck and Haste; now and then a word between them
    second.append('execute as @e[type=minecraft:wolf,tag=bm.rwpet,tag=!bm.ffpet] at @s run function bm:p262/bonds')
    fn('p262/bonds', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #kp bm.rng 0',
                      'execute as @e[type=minecraft:wolf,tag=bm.tkpet,tag=!bm.ffpet,distance=..16] if score @s bm.pid = #me bm.pid run scoreboard players set #kp bm.rng 1',
                      'execute if score #kp bm.rng matches 0 run return 0',
                      'execute on owner if entity @s[distance=..16] run function bm:p262/bonds_you'])
    lines = [('"Every bond, woven." - "Every bond, ACCOUNTED FOR."', ),
             ('"You keep the books, then?" - "Someone has to. You give them away for NOTHING."', ),
             ('"Fifty threads." - "Fifty debts. We\'re both right, it\'s infuriating."', )]
    fn('p262/bonds_you', ['effect give @s minecraft:luck 3 0 true', 'effect give @s minecraft:haste 3 0 true',
                          'execute store result score #r bm.rng run random value 1..240'] +
       [f'execute if score #r bm.rng matches {i + 1} unless entity @s[tag=bm.hush] run ' +
        title('@s', 'actionbar', [T('The Keeper and the King: ', COL, bold=True), T(l[0], LINE, italic=True)]) for i, l in enumerate(lines)])
    # ---- the Champion's Pit: a crew with a friend of his never draws him (a Vault Ravager instead)
    pit = G.FUNCS.get('p76/r/pit/call')
    k = next((i for i, l in enumerate(pit or []) if l.endswith('run return run function bm:p76/champ/ratking')), None)
    assert k is not None, 'the Champion\'s Pit no longer calls the Rat King the way phase262 expects'
    if pit:
        pit[k] = pit[k].replace('run return run function bm:p76/champ/ratking', 'run return run function bm:p262/pit')
        alt = 'ravager' if 'p76/champ/ravager' in G.FUNCS else next(l.rsplit('/', 1)[1] for l in pit if 'bm:p76/champ/' in l and not l.endswith('p262/pit'))
        fn('p262/pit', [f'execute if entity @a[tag=bm.gvp,tag=bm.rwmet,distance=..48] run return run function bm:p76/champ/{alt}', 'function bm:p76/champ/ratking'])
    fn('admin/ratking_reset', ['tag @s remove bm.rwmet', 'tag @s remove bm.rwpaid', f'clear @s *[minecraft:custom_data~{{bm:"{ITEM}"}}]',
                               title('@s', 'actionbar', T('The Rat King has not met you yet: in his Counting House, with the coin, he waits.', COL))])
    fn('admin/ratking_go', ['scoreboard players set #rwwant bm.p2 1', 'execute unless score #rwver bm.p2 matches 1.. run function bm:p262/room/try',
                            'tag @s add bm.rwcoin', f'execute in minecraft:overworld run tp @s {LAND[0]} {LAND[1]} {LAND[2]} 180 0'])
    G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/ratking_reset', 'yellow'), T('  the Rat King forgets you (his Marker taken back);', 'gray'),
                                                T(' /function bm:admin/ratking_go', 'yellow'), T(' to his Counting House', 'gray')]))


def _room():
    """the Counting House, in commands (run in the Overworld, its chunks loaded)"""
    x0, x1, z0, z1, y0, y1 = CX - HALF, CX + HALF, CZ - HALF, CZ + HALF, FY, FY + HIGH - 1
    L = [f'fill {x0 - 2} {y0 - 3} {z0 - 2} {x1 + 2} {y1 + 3} {z1 + 2} minecraft:deepslate_bricks',            # (a shell two thick: no cave, lava or water in)
         f'fill {x0} {y0 - 1} {z0} {x1} {y0 - 1} {z1} minecraft:polished_deepslate',
         f'fill {x0 + 1} {y0 - 1} {z0 + 1} {x1 - 1} {y0 - 1} {z1 - 1} minecraft:deepslate_tiles',
         f'fill {x0} {y0} {z0} {x1} {y1} {z1} minecraft:air',
         f'fill {x0} {y1 + 1} {z0} {x1} {y1 + 1} {z1} minecraft:polished_blackstone_bricks']
    for x in range(x0, x1 + 1, 4):                                             # (gold-capped pillars along the north and south walls)
        for z in (z0, z1):
            L += [f'fill {x} {y0} {z} {x} {y1} {z} minecraft:polished_blackstone', f'setblock {x} {y1} {z} minecraft:gold_block']
    for x in (x0 + 2, x1 - 2):                                                 # (crimson banners either side of the throne)
        L += [f'setblock {x} {y0 + 4} {z0 + 1} minecraft:red_wall_banner[facing=south]{{patterns:[{{pattern:"minecraft:border",color:"yellow"}},{{pattern:"minecraft:mojang",color:"yellow"}}]}}']
    # the throne: a dais of crimson, gold steps, a tall gold back with a ruby crest - on the hoard
    tx, tz = CX, CZ - 5
    L += [f'fill {tx - 2} {y0} {tz - 1} {tx + 2} {y0} {tz + 1} minecraft:red_wool', f'fill {tx - 1} {y0} {tz + 2} {tx + 1} {y0} {tz + 2} minecraft:gold_block',
          f'setblock {tx} {y0} {tz} minecraft:gold_block', f'fill {tx - 1} {y0 + 1} {tz - 1} {tx + 1} {y0 + 4} {tz - 1} minecraft:gold_block',
          f'setblock {tx} {y0 + 5} {tz - 1} minecraft:redstone_block', f'setblock {tx - 1} {y0 + 1} {tz} minecraft:gold_block', f'setblock {tx + 1} {y0 + 1} {tz} minecraft:gold_block']
    # the hoard round it: gold, raw gold, heaped coins (gold pressure plates), an emerald or two
    heap = [(-4, -5, 2), (-3, -5, 3), (3, -5, 3), (4, -5, 2), (-5, -6, 2), (5, -6, 2), (-3, -6, 3), (3, -6, 3), (-4, -4, 1), (4, -4, 1),
            (-6, -5, 1), (6, -5, 1), (-2, -6, 2), (2, -6, 2), (-5, -4, 1), (5, -4, 1)]
    for dx, dz, h in heap:
        b = 'minecraft:raw_gold_block' if (dx + dz) % 3 == 0 else 'minecraft:gold_block'
        L += [f'fill {CX + dx} {y0} {CZ + dz} {CX + dx} {y0 + h - 1} {CZ + dz} {b}', f'setblock {CX + dx} {y0 + h} {CZ + dz} minecraft:light_weighted_pressure_plate']
    for dx, dz in ((-2, -3), (2, -3), (-1, -2), (1, -2), (-3, -3), (3, -2), (0, -1), (-4, -2), (4, -3)):
        L.append(f'setblock {CX + dx} {y0} {CZ + dz} minecraft:light_weighted_pressure_plate')
    L += [f'setblock {CX - 4} {y0 + 2} {CZ - 5} minecraft:emerald_block', f'setblock {CX + 5} {y0 + 2} {CZ - 6} minecraft:emerald_block']
    # the counting table, its ledger and its candles (the five rats stand on it for the Shell of Rats)
    L += [f'fill {CX - 5} {y0} {CZ} {CX - 1} {y0} {CZ} minecraft:dark_oak_planks', f'fill {CX - 5} {y0} {CZ - 1} {CX - 1} {y0} {CZ - 1} minecraft:dark_oak_slab[type=top]',
          f'setblock {CX - 3} {y0 + 1} {CZ - 1} minecraft:lectern[facing=south]', f'setblock {CX - 5} {y0 + 1} {CZ - 1} minecraft:candle[candles=3,lit=true]',
          f'setblock {CX - 1} {y0 + 1} {CZ - 1} minecraft:candle[candles=2,lit=true]']
    # light: lanterns from the ceiling, candles in the corners, and the room's own unseen light
    for dx, dz in ((-4, -2), (4, -2), (-4, 4), (4, 4), (0, 2)):
        L += [f'setblock {CX + dx} {y1} {CZ + dz} minecraft:iron_chain', f'setblock {CX + dx} {y1 - 1} {CZ + dz} minecraft:lantern[hanging=true]']
    for x, z in ((x0, z0 + 1), (x1, z0 + 1), (x0, z1 - 1), (x1, z1 - 1)):
        L.append(f'setblock {x} {y0} {z} minecraft:candle[candles=4,lit=true]')
    for dx, dz in ((-3, 3), (3, 3), (0, 6), (-6, 0), (6, 0), (0, -2)):
        L.append(f'setblock {CX + dx} {y0 + 3} {CZ + dz} minecraft:light[level=12]')
    # the rat-run's landing (a ring of gold in the floor, the shaft dark above it) and the mouse hole home (east wall)
    lx, lz = int(LAND[0] // 1), int(LAND[2] // 1)
    L += [f'fill {lx - 1} {y0 - 1} {lz - 1} {lx + 1} {y0 - 1} {lz + 1} minecraft:gold_block', f'setblock {lx} {y0 - 1} {lz} minecraft:black_concrete',
          f'fill {lx - 1} {y1 + 1} {lz - 1} {lx + 1} {y1 + 1} {lz + 1} minecraft:black_concrete']
    hx, hz = int(HOLE[0] // 1), int(HOLE[2] // 1)
    L += [f'fill {hx} {y0} {hz} {hx + 1} {y0 + 1} {hz} minecraft:air', f'setblock {hx + 2} {y0} {hz} minecraft:black_concrete',
          f'setblock {hx + 2} {y0 + 1} {hz} minecraft:black_concrete', f'setblock {hx} {y0 + 2} {hz} minecraft:gold_block',
          f'setblock {hx - 1} {y0 + 2} {hz} minecraft:oak_wall_sign[facing=west]' + snbt({'front_text': {'has_glowing_text': B(1), 'color': 'yellow', 'messages': [
              {'text': ''}, {'text': 'MOUSE HOLE'}, {'text': '(the way up)'}, {'text': ''}]}})]
    return L

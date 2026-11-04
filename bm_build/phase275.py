"""3.1: THE GOLDEN DOODLE - the 64th follower, and the Lucky Nights' own boss (goldendoodle_pet_art.py, goldendoodle_boss_art.py,
goldendoodle_holy_art.py; fol5flag.GDOODLE). A gilded, sparkly goose - two waddly feet, a long neck, a goofy body - who bit the
wrong crown once, and turned into THE GILDED ELDRITCH; the Lightbringer cured her, and left her a third form of her own.

MEETING HER   the boss fight (phase275b): THE CLOVER POND, a room off the Gilded Roost's Counting House. On a LUCKY NIGHT, stand in
              its clover ring with your own Lightbringer, Keeper of Bonds and Bound Sovereign out: the gilded stone hatches with a
              HONK. Beat her (the goose, then the Eldritch), and the Lightbringer cures her: the Doodle Egg is yours, and she comes
              along - all three forms hers from that first win.
HER FORMS     her menu's Form button cycles the goose -> the Gilded Eldritch -> her Lightbringer form (the owner's bm.gqform, kept across
              recall, logout and a faint). ONE FOLLOWER, THREE RIGS: her displays are the union of the three rigs' parts, each form
              wearing its own models and solving its own poses on its own joints (fol5art.GoldenArt, fol5wire.form_pose); the host
              tagged bm.gqf1 (the Eldritch) or bm.gqf2 (the Lightbringer form), every pose asking it first. Her hitbox and her host's
              size follow the form; the two big forms have a Companion Size (compsize, as the Rat King's: ~2 blocks).
HER WAYS      by form - the goose: HONK (a foe within 4: 3, slowed), the NECK-WHIP SLAP (two foes near: 4 each), the WADDLE CHARGE (a
              foe 4-10 off: she charges, on screen, and bonks it - 5), the GOLDEN HONK (charged: 6 to all within 8, and the nearest
              armed monster loses its weapon - THE THIEF), the LUCKY COIN (you hurt: HEADS Absorption and Speed, TAILS Luck II for
              everyone near), the GOLDEN EGG (out of a fight, every 5 minutes, twice as often on a Lucky Night: a gold nugget - a
              Lucky Token 1 in 20, a Scratch Card 1 in 100). The Eldritch: the LUNGE (9), the WING SLAM (7 in a ring), the DREAD BEAM
              (8), the SHRIEK (charged: 8 to all within 8, weakened), its MENACE (monsters weakened, you steadied). The Lightbringer
              form: the WING GUST (3, thrown up), the HOLY BEAM (8, 14 to the undead, the struck mob outlined), the SUNBURST
              (charged), the BLESSING (Regeneration II for you and every follower near). Her Piercing Blow, on screen in every
              form: the LUCKY STREAK. Her Lucky passive: while she is out in the Overworld, the Lucky Night roll is 2 in 100.
EVERYTHING ELSE is every follower's: sitting (right-click: plopped down; sneak: her nest), a wardrobe (Rose Gold and Platinum - drawn,
on all three rigs - Midnight Gold, the metal feathers), a rare aura (Jackpot), a shiny (Four-Leaf), the Partner Wheel, a frame (a
right-click: HONK; once each Lucky Night a gold nugget at its foot), a display case, Cecil's doll (sneak + right-click the placed
doll: goose -> Eldritch -> Lightbringer form), the honours, a Raid Contract; pairs with Bender, Mr. Capshun, Henry and Nia."""
from items import item, T, TOTEM
from useitem import hold
import fol5
import fol5art
import fol5wire as W5
import rigpet as RP
import rigface as RF2
import phase235 as P235

S5 = fol5.SPEC['gdoodle']
A0 = fol5art.get('gdoodle')
Q, K, H = A0.Q, A0.K, A0.H
FORMS = A0.FORMS
COL, LINE = S5['COL'], S5['LINE']
ITEM = S5['item']
PRE = ('gq_', 'gk_', 'gh_')
FTAG = (None, 'bm.gqf1', 'bm.gqf2')
FOBJ = 'bm.gqform'                 # (the owner's: 0 the goose, 1 the Eldritch, 2 the Lightbringer form)
CSZ_K = round(K.COMPANION / K.R.RIG_SCALE, 4)
# (her hitbox and her host's size, by form - and the two big forms at Companion Size)
FIT = {'q': ((0.7, 1.3), 0.8), 'k': ((1.6, 3.2), 1.6), 'kc': ((1.0, 2.0), 1.0), 'h': ((1.6, 3.4), 1.6), 'hc': ((1.0, 2.1), 1.0)}

# THE POSES rigpet's cycles name, per form (the goose's, the Eldritch's, the Lightbringer form's own)
VMAP = {'idle_a': ('idle_a', 'idle_a', 'idle_a'), 'idle_b': ('idle_b', 'idle_b', 'idle_b'), 'idle_c': ('idle_c', 'menace', 'happy'),
        'walk_0': ('walk_0', 'walk_0', 'walk_0'), 'walk_1': ('walk_1', 'walk_1', 'walk_1'), 'walk_2': ('walk_2', 'walk_2', 'walk_2'),
        'walk_3': ('walk_3', 'walk_3', 'walk_3'), 'run_0': ('run_0', 'walk_1', 'run_0'), 'run_1': ('run_1', 'walk_3', 'run_1'),
        'sit_a': ('sit_a', 'sit_a', 'sit_a'), 'sit_b': ('sit_b', 'sit_b', 'sit_b'), 'happy': ('happy', 'idle_b', 'happy'), 'hurt': ('hurt', 'hurt', 'hurt'),
        'proud': ('proud', 'menace', 'happy'), 'alert': ('alert', 'menace', 'idle_b'),
        'm_up': ('honk_up', 'bite_up', 'gust_up'), 'm_hit': ('honk', 'bite', 'gust'),
        'c_up': ('slap_up', 'slam_up', 'gust_up'), 'c_hit': ('slap', 'slam', 'gust'),
        'r_up': ('charge', 'beam_up', 'beam_up'), 'r_hit': ('charge', 'beam', 'beam'),
        's_go': ('coin', 'menace', 'cure'), 'x_up': ('honk_up', 'shriek', 'beam_up'), 'x_hit': ('honk', 'shriek', 'beam'),
        'k_lay': ('lay', 'idle_a', 'idle_a'), 'k_eggs': ('eggs', 'idle_a', 'idle_a')}
for _n, _v in VMAP.items():
    for _f, _p in enumerate(_v):
        assert _p in FORMS[_f].POSES, (_n, _f, _p)
    A0.POSES[_n] = {}

item(ITEM, TOTEM, 'The Doodle Egg', COL,
     ['A gold egg with a clover-shaped crack in it, and a sparkle.', 'Something inside it honks, very quietly.',
      ('Use: call the Golden Doodle (again: call her over).', 'blue'), ('Sneak + use: her menu - her Form, Companion Size, her wardrobe.', 'blue'),
      ('If she faints: 2 minutes before she can return.', 'gray')],
     model=f'bm:{ITEM}', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)


class Doodle(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'gdoodle', 'The Golden Doodle', COL, LINE, 'p275', 'gq', 'gu'
    A = RF2.art(A0)
    MENU, PET_HP, PET_CD, ITEM = 2422, 48, 120, ITEM
    pron, they = 'her', 'she'
    TWEEN = False
    FACE = dict(A0.FACE_MAP)
    ATTRS = dict(armor=8, attack_damage=4, movement_speed=0.32, follow_range=32, step_height=1.1)
    SCALE, HIT = FIT['q'][1], FIT['q'][0]
    BOX_FIT = True
    BUTTONS = ((6, 'Form: goose / Eldritch / Lightbringer', 'Cycles her form: the Golden Doodle, the Gilded Eldritch, her Lightbringer form. She keeps it till you change it.', 'p275/form'),
               (7, 'Companion Size: on / off', 'Her two big forms at a companion\'s size, about 2 blocks (her hitbox with them). The goose is always her own size.', 'p275/csz/toggle'))
    CYCLE = W5.cycle(A0, (240, [(0, 'idle_a'), (90, 'idle_b'), (150, 'idle_a'), (200, 'idle_c')]), (120, [(0, 'sit_a'), (60, 'sit_a')]),
                     (None, [(0, 'happy'), (16, 'idle_a')]),
                     {7: (None, [(0, 'm_up'), (6, 'm_hit'), (14, 'idle_a')]), 8: (None, [(0, 'r_up'), (10, 'r_hit'), (22, 'idle_a')]),
                      11: (None, [(0, 'c_up'), (10, 'c_hit'), (18, 'idle_a')]), 12: (None, [(0, 'x_up'), (12, 'x_hit'), (24, 'idle_a')]),
                      13: (None, [(0, 's_go'), (22, 'idle_a')]), 14: (None, [(0, 'k_lay'), (16, 'k_eggs'), (32, 'proud'), (38, 'idle_a')])}, wp=16, rp_=8)
    DUR = dict(P235._DUR, m_up=6, m_hit=2, c_up=8, c_hit=2, r_up=8, r_hit=3, x_up=10, x_hit=2, s_go=8, k_lay=12, k_eggs=8, proud=8, alert=8,
               sit_a=14, sit_b=20, happy=8, idle_c=16, walk_0=4, walk_1=4, walk_2=4, walk_3=4, run_0=3, run_1=3)
    QUIPS = ['(HONK.)', '(she waddles beside you, very proud of herself)', '(she preens her gold leaf - a sparkle falls off it)',
             '(she pecks at your boot, then looks innocent)', '(she honks at a passing chicken. "A chicken with ambitions," you think.)',
             '(she flips a gold coin with her beak, catches it, and looks smug)']
    HELLO = ('(the Golden Doodle waddles back to you, honking)', '(a golden egg cracks open - HONK - and out waddles the Golden Doodle)',
             '(she honks goodbye, tucks herself into a golden egg, and is gone)')
    SIT = ('(she gets up, shakes out her feathers, and honks)', '(she plops down, big feet sticking out in front, toes up)')
    FAINT = '(a small, sad honk)'
    NOT_YOURS = '(she honks at you, outraged, and flaps)'
    POWERS = [('The Goose', 'HONK (a foe within 4: 3, slowed), the Neck-Whip Slap, the Waddle Charge (on screen: 5), the Golden Honk (charged: 6 to all near, the Thief), the Lucky Coin, the Golden Egg'),
              ('The Gilded Eldritch', 'the Lunge (9), the Wing Slam (7 in a ring), the Dread Beam (8), the Shriek (charged: 8 to all near, weakened), its Menace'),
              ('Her Lightbringer form', 'the Wing Gust (3, thrown up), the Holy Beam (8, 14 to the undead, the mob outlined), the Sunburst (charged), the Blessing (Regeneration II for all near)'),
              ('Form', 'her menu: the goose, the Gilded Eldritch, her Lightbringer form - kept till you change it'),
              ('Companion Size', 'her menu: the two big forms at about 2 blocks - her hitbox with them'),
              ('Lucky', 'while she is out in the Overworld, a Lucky Night is twice as likely; on a Lucky Night her eggs come twice as often')]
    INTRO = [T('The Golden Doodle', COL, bold=True), T(' - a gilded goose who bit the wrong crown once, and was cured by the light. ', 'gray'), T('(HONK.)', LINE, italic=True)]
    BURST = ['particle minecraft:wax_on ~ ~0.6 ~ 0.4 0.5 0.4 0 16', 'particle minecraft:end_rod ~ ~0.8 ~ 0.3 0.4 0.3 0.02 8']
    FADE_SOUND = 'playsound minecraft:entity.goat.screaming.ambient neutral @a[distance=..20] ~ ~ ~ 0.5 1.8'
    SUMMON_EXTRA = ['playsound minecraft:entity.goat.screaming.ambient neutral @a[distance=..24] ~ ~ ~ 0.7 1.7', 'playsound minecraft:block.amethyst_block.chime neutral @a[distance=..24] ~ ~ ~ 1 1.4']
    ENC_POSES = [(0, 'idle_a'), (30, 'happy'), (50, 'idle_b')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 30 run particle minecraft:wax_on ~ ~1 ~ 0.4 0.4 0.4 0 6'
    ADV = ('Honk If You\'re Lucky', 'Wake the Golden Doodle at the Clover Pond on a Lucky Night - and see her cured')
    ADMIN_HINT = 'On a Lucky Night, in the Gilded Roost\'s Clover Pond, with your Lightbringer, Keeper of Bonds and Bound Sovereign out (admin/gdoodle_boss).'
    MEET_HINT = 'Right-click her (once you have won her fight).'


_DOLL = 'A doll of the Golden Doodle - a little gold goose, very proud of herself. Sneak + right-click it, set down: her other forms.'
_eff = W5.pair_fx
_PAIRS = {
    'gq_bender': ('gdoodle', 'bender', 'Goose Chase', '#e0a860', 'The Golden Doodle and Bender - he tries to herd her; she honks, and he is chased round you',
                  _eff(('speed', 0), ('luck', 0)),
                  [('bender', '(tries to herd her, very seriously)'), ('gdoodle', '(HONK. She chases him round you, twice.)')],
                  [('gdoodle', '(she struts past him, head high)', 'bender', '(sits, good boy - he has decided she is in charge)')]),
    'gq_capshun': ('gdoodle', 'capshun', 'Subtitles Available', '#f0f0f0', 'The Golden Doodle and Mr. Capshun - he captions every honk',
                   _eff(('luck', 0), ('haste', 0)),
                   [('gdoodle', '(HONK)'), ('capshun', '[Mr. Capshun narrates: "[aggressive honking]"]')],
                   [('gdoodle', '(a small, polite honk)', 'capshun', '[Mr. Capshun narrates: "[honk, but polite]"]')]),
}
W5.register(Doodle, A0, _DOLL, ('minecraft:wax_on', 'minecraft:entity.goat.screaming.ambient', 'minecraft:end_rod'), _PAIRS, 'the Golden Doodle')

# ---- her display case and her dolls: the goose at rest in the case; one doll from Cecil, baked from each form's own doll pose
#      (each leans the neck back so the head's joint stands on the doll's axis - the head group grows about it); the placed doll,
#      sneak + right-clicked, cycles the goose -> the Eldritch -> the Lightbringer form
import phase134 as P134  # noqa: E402
import phase141 as P141  # noqa: E402
_figs0 = P134.figures
DOLLS3 = ('doll_gdoodle', 'doll_gdoodle_k', 'doll_gdoodle_h')


def _figures():
    F2 = _figs0()
    F2[ITEM] = (Doodle.NAME, P134._rigkit(Q.R, Q.R.POSES['idle_a'], Q.R.RIG_SCALE))
    for f, R in enumerate(FORMS):
        F2[f'{ITEM}_d{f}'] = (Doodle.NAME, P134._rigkit(R, R.POSES['doll'], R.RIG_SCALE))
    return F2


P134.figures = _figures
P134.FIT[ITEM] = Q.R.fit(Q.R.POSES['idle_a'])
for _f, (_R, _M) in enumerate(zip(FORMS, (Q, K, H))):
    P134.FIT[f'{ITEM}_d{_f}'] = _R.fit(_R.POSES['doll'])
    P134.BAKE_ONLY.add(f'{ITEM}_d{_f}')
    _dz = _R.POSES['doll']
    _g = {f'bm:{_R.model_name(p, _dz)}': g for p, g in _M.DOLL_GROUPS.items() if p in _R.PARTS and not _R.HIDDEN(p, _dz)}
    P141.DOLL_FROM[DOLLS3[_f]] = (f'{ITEM}_d{_f}', dict(Q.DOLL, width=19 if _f == 0 else 24, groups=_g))

# ---- her Piercing Blow, on screen in every form: THE LUCKY STREAK - wound up, the dash, three strikes running (the goose: honk, slap,
#      honk; the Eldritch: bite, slam, bite; the Lightbringer form: the gust, three times) and the jackpot
import phase226 as _P226  # noqa: E402
_imp = ['particle minecraft:crit ~ ~1 ~ 0.3 0.3 0.3 0.3 8', 'particle minecraft:wax_on ~ ~1 ~ 0.3 0.3 0.3 0 6']
_P226.ASSAULT['gdoodle'] = dict(pfx='p275', s_obj='bm.gus', anim='p275/anim', busy='bm.gux', end=40, dash=dict(reach=2.2, speed=0.9, lift=0), free=True,
                                hits={1: (3, _imp, 'minecraft:entity.goat.screaming.ambient', 1.7),
                                      2: (5, _imp + ['particle minecraft:totem_of_undying ~ ~1 ~ 0.4 0.5 0.4 0.4 30', 'data modify entity @s Motion[1] set value 0.4d'],
                                          'minecraft:block.note_block.bell', 0.8)},
                                tl={1: ['P r_up', 'S minecraft:entity.goat.screaming.ambient 0.8 1.4'], 4: ['DASH'], 6: ['P m_up'], 8: ['P m_hit', 'H1'], 12: ['P c_up'],
                                    14: ['P c_hit', 'H1'], 18: ['P m_up'], 20: ['P m_hit', 'H1'], 24: ['P x_up'], 30: ['P x_hit', 'H2', 'S minecraft:entity.player.levelup 0.6 1.6'],
                                    36: ['P proud']})
_P226.NAMES['gdoodle'] = ('Lucky Streak', 'charges the monster down and strikes it three times running, then hits the jackpot')


def extend_offers(O, offer):
    pass


def generate_early(G):
    RP.contract(Doodle, G)


def _icon():
    from sprites280 import S
    s = S()
    pal = {'g': '#ffd040', 'd': '#c8962a', 'w': '#fff6c0', 'c': '#3ab060'}
    s.g(['...gggg...', '..gwgggg..', '.gwggcgdg.', '.ggggccgd.', '.gggcgcgd.', '..ggggdd..', '...dddd...'], pal, 3, 4)
    return s.render()


def rp(R):
    W5.rp(Doodle, R, _icon(), A0)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + ('gk_', 'gh_')
    for d in DOLLS3[1:]:                                     # (a stand-in, so each form's doll has its item; phase141's bake replaces the model)
        R.HATS[d] = ({'s': 'minecraft:block/gold_block'}, [{'from': [6, 0, 6], 'to': [10, 8, 10], 'faces': {f: {'uv': [0, 0, 16, 16], 'texture': '#s'}
                                                                                                     for f in ('north', 'south', 'east', 'west', 'up', 'down')}}])
    names = set(A0.models())

    def post(R2):
        mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
        # (a part a form hasn't: its display wears that form's empty model)
        for f, r in enumerate(FORMS):
            for p in A0.PARTS:
                if p not in r.PARTS:
                    R2.wj(f'assets/bm/items/{r.PREFIX}{p}.json', {'model': {'type': 'minecraft:empty'}})
        # (the big forms' heads: an item definition picking the mood's face, as rigpet writes the goose's)
        for f in (1, 2):
            base = f'{PRE[f]}head'
            cases = [{'when': e, 'model': mdl(f'{base}_x{A0.FACE_MAPS[f][e]}')} for e in Doodle.EXPR if f'{base}_x{A0.FACE_MAPS[f].get(e)}' in names]
            R2.wj(f'assets/bm/items/{base}.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0, 'cases': cases, 'fallback': mdl(base)}})
    R.POST.append(post)
    import phase275b as B
    B.rp(R)


def textures():
    return A0.textures()


# ---------------------------------------------------------------------------------------------------- her ways, by form
def _abilities(G, X):
    fn, pfx, foe = G.fn, X.pfx, X.foe
    snd = lambda s, v=0.9, p=1.0: f'playsound minecraft:{s} neutral @a[distance=..24] ~ ~ ~ {v} {p}'
    honk = snd('entity.goat.screaming.ambient', 0.8, 1.7)
    K_ = dict(melee=dict(st=7, x=16, at=9, cd=100, reach=4.0, face='serious'),
              ranged=dict(st=8, x=24, at=12, cd=200, near=4, far=10, face='serious', during=(13, 21)),
              crowd=dict(st=11, x=20, at=10, cd=200, r=5, n=2, face='serious'),
              charged=dict(st=12, x=26, at=13, cd=1200, r=8, face='serious'),
              support=dict(st=13, x=24, at=12, cd=600, face='happy'),
              kind=dict(st=14, x=40, at=20, cd=6000, face='happy'))
    lines = P235.kit(G, X, K_)
    by_form = lambda ev: [f'execute if entity @s[tag=bm.gqf1] run return run function bm:{pfx}/k/{ev}', f'execute if entity @s[tag=bm.gqf2] run return run function bm:{pfx}/h/{ev}']
    near = lambda r: f'@e[{foe},distance=..{r},sort=nearest,limit=1]'
    # ---- the goose
    fn(f'{pfx}/melee', by_form('melee') + X.hit(3) + [f'execute as {near(4.4)} at @s run function bm:{pfx}/honked', honk,
                                                       'particle minecraft:note ^ ^1 ^1 0.4 0.3 0.4 1 6', 'particle minecraft:wax_on ^ ^1 ^1.2 0.5 0.4 0.5 0 8'] + X.end)
    fn(f'{pfx}/honked', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 2 0'])
    fn(f'{pfx}/crowd', by_form('crowd') + X.hit(4) + [f'execute as @e[{foe},distance=..4] at @s run function bm:{pfx}/hurt', 'particle minecraft:sweep_attack ~ ~0.8 ~ 1.2 0.2 1.2 0 4',
                                                       snd('entity.player.attack.sweep', 0.8, 1.4)] + X.end)
    # (the Waddle Charge: on screen - she runs at it, head low, a step a tick, and bonks it)
    fn(f'{pfx}/ranged_tick', ['execute if entity @s[tag=bm.gqf1] run return 0', 'execute if entity @s[tag=bm.gqf2] run return 0',
                              f'execute if entity @e[{foe},distance=..1.6] run return 0',
                              f'execute facing entity {near(11)} feet rotated ~ 0 positioned ^ ^ ^0.45 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~ ~ ~ ~',
                              'particle minecraft:wax_on ~ ~0.3 ~ 0.2 0.1 0.2 0 2'])
    fn(f'{pfx}/ranged', by_form('ranged') + X.hit(5) + [f'execute as {near(3)} at @s run function bm:{pfx}/bonked'] + X.end)
    fn(f'{pfx}/bonked', [f'function bm:{pfx}/hurt', 'particle minecraft:crit ~ ~1 ~ 0.3 0.3 0.3 0.3 12', 'particle minecraft:wax_on ~ ~1.4 ~ 0.3 0.2 0.3 0 8',
                         snd('entity.player.attack.knockback', 0.8, 1.2)])
    fn(f'{pfx}/charged', by_form('charged') + X.hit(6) + [f'execute as @e[{foe},distance=..8] at @s run function bm:{pfx}/honked',
                                                           'scoreboard players set #th bm.rng 0',
                                                           f'execute as @e[{foe},distance=..8,sort=nearest] if items entity @s weapon.mainhand * run function bm:{pfx}/thief',
                                                           honk, snd('entity.goat.screaming.ambient', 1.0, 1.2), 'particle minecraft:note ~ ~1.2 ~ 2 0.5 2 1 16'] + X.end)
    fn(f'{pfx}/thief', ['execute if score #th bm.rng matches 1 run return 0', 'scoreboard players set #th bm.rng 1', 'item replace entity @s weapon.mainhand with minecraft:air',
                        'particle minecraft:wax_on ~ ~1.2 ~ 0.3 0.3 0.3 0 10', snd('entity.item.pickup', 1.0, 0.8)])
    say = lambda txt: X.title('@s', 'actionbar', [T('The Golden Doodle: ', COL, bold=True), T(txt, LINE)])
    fn(f'{pfx}/support', by_form('support') + ['execute store result score #r bm.rng run random value 1..2', snd('entity.experience_orb.pickup', 1.0, 1.4),
                                                'particle minecraft:wax_on ~ ~1.4 ~ 0.2 0.4 0.2 0 10',
                                                f'execute if score #r bm.rng matches 1 on owner run function bm:{pfx}/heads',
                                                f'execute if score #r bm.rng matches 2 run function bm:{pfx}/tails'])
    fn(f'{pfx}/heads', ['effect give @s minecraft:absorption 10 0 true', 'effect give @s minecraft:speed 5 0 true', say('(she flips her lucky coin - HEADS!)')])
    fn(f'{pfx}/tails', ['effect give @a[distance=..8,gamemode=!spectator] minecraft:luck 10 1 true', f'execute on owner run {say("(she flips her lucky coin - TAILS. Luck for everyone!)")}'])
    fn(f'{pfx}/kind', ['execute if entity @s[tag=bm.gqf1] run return 0', 'execute if entity @s[tag=bm.gqf2] run return 0',
                       'execute if score #lnight bm.bm matches 1 run scoreboard players set @s bm.guk 3000',
                       'summon minecraft:item ~ ~0.3 ~ {Item:{id:"minecraft:gold_nugget",count:1}}',
                       'execute store result score #r bm.rng run random value 1..100',
                       'execute if score #r bm.rng matches 1..5 run loot spawn ~ ~0.3 ~ loot bm:items/lucky_token',
                       'execute if score #r bm.rng matches 6 run loot spawn ~ ~0.3 ~ loot bm:items/scratch_card',
                       'particle minecraft:wax_on ~ ~0.4 ~ 0.3 0.2 0.3 0 12', snd('entity.chicken.egg', 1.0, 0.8), honk,
                       f'execute on owner run {say("(she lays you a golden egg, and is VERY proud of it)")}'])
    # ---- the Gilded Eldritch
    fn(f'{pfx}/k/melee', X.hit(9) + [f'execute as {near(4.4)} at @s run function bm:{pfx}/k/bit', snd('entity.evoker_fangs.attack', 0.9, 0.7)] + X.end)
    fn(f'{pfx}/k/bit', [f'function bm:{pfx}/hurt', 'particle minecraft:dust{color:[0.85,0.1,0.15],scale:1.2} ~ ~1 ~ 0.3 0.4 0.3 0 12', 'particle minecraft:crit ~ ~1 ~ 0.3 0.3 0.3 0.3 8'])
    fn(f'{pfx}/k/crowd', X.hit(7) + [f'execute as @e[{foe},distance=..6] at @s run function bm:{pfx}/k/slammed', 'particle minecraft:explosion ~ ~0.3 ~ 2.5 0 2.5 0 6',
                                     'particle minecraft:dust{color:[0.85,0.1,0.15],scale:1.5} ~ ~0.2 ~ 3 0.1 3 0 40', snd('entity.generic.explode', 0.9, 0.6)] + X.end)
    fn(f'{pfx}/k/slammed', [f'function bm:{pfx}/hurt', 'data modify entity @s Motion[1] set value 0.4d'])
    fn(f'{pfx}/k/ranged', X.hit(8) + [f'execute facing entity {near(10.5)} eyes positioned ^ ^1.6 ^ run function bm:{pfx}/k/beamfx',
                                      f'execute as {near(10.5)} at @s run function bm:{pfx}/k/bit', snd('entity.guardian.attack', 1.0, 0.6)] + X.end)
    fn(f'{pfx}/k/beamfx', [f'particle minecraft:dust{{color:[0.95,0.15,0.2],scale:1.4}} ^ ^ ^{d} 0.05 0.05 0.05 0 3' for d in range(1, 11)])
    fn(f'{pfx}/k/charged', X.hit(8) + [f'execute as @e[{foe},distance=..8] at @s run function bm:{pfx}/k/shrieked', snd('entity.warden.roar', 0.8, 1.5),
                                       'particle minecraft:dust{color:[0.95,0.15,0.2],scale:1.6} ~ ~1 ~ 3 0.3 3 0 60', 'particle minecraft:sonic_boom ~ ~2 ~ 0 0 0 0 1'] + X.end)
    fn(f'{pfx}/k/shrieked', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:weakness 5 0'])
    fn(f'{pfx}/k/support', [f'effect give @e[{foe},distance=..10] minecraft:weakness 8 0', 'execute on owner run effect give @s minecraft:resistance 6 0 true',
                            snd('entity.ravager.roar', 0.7, 1.3), 'particle minecraft:dust{color:[0.85,0.1,0.15],scale:1.2} ~ ~1.5 ~ 1.5 0.6 1.5 0 30'])
    fn(f'{pfx}/k/kind', ['return 0'])
    # ---- her Lightbringer form
    fn(f'{pfx}/h/melee', X.hit(3) + [f'execute as @e[{foe},distance=..5] at @s run function bm:{pfx}/h/gusted', snd('entity.phantom.flap', 1.2, 0.8),
                                     'particle minecraft:cloud ^ ^1 ^1.5 0.8 0.4 0.8 0.1 16', 'particle minecraft:end_rod ^ ^1 ^1 0.6 0.4 0.6 0.05 8'] + X.end)
    fn(f'{pfx}/h/gusted', [f'function bm:{pfx}/hurt', 'data modify entity @s Motion[1] set value 0.5d', 'effect give @s minecraft:slowness 2 0'])
    fn(f'{pfx}/h/crowd', X.hit(3) + [f'execute as @e[{foe},distance=..6] at @s run function bm:{pfx}/h/gusted', snd('entity.phantom.flap', 1.4, 0.6),
                                     'particle minecraft:cloud ~ ~1 ~ 2 0.4 2 0.1 30'] + X.end)
    fn(f'{pfx}/h/ranged', X.hit(8) + [f'execute as {near(10.5)} at @s run function bm:{pfx}/h/beamed', snd('block.beacon.activate', 1.0, 1.6)] + X.end)
    fn(f'{pfx}/h/beamed', ['scoreboard players set #pd bm.rng 8', 'execute if entity @s[type=#minecraft:undead] run scoreboard players set #pd bm.rng 14',
                           f'function bm:{pfx}/hurt', 'execute unless predicate bm:p44/invis run effect give @s minecraft:glowing 4 0 true',
                           'particle minecraft:end_rod ~ ~2 ~ 0.3 2 0.3 0.02 30', 'particle minecraft:wax_on ~ ~0.2 ~ 0.6 0 0.6 0 12'])
    fn(f'{pfx}/h/charged', X.hit(8) + [f'execute as @e[{foe},distance=..8] at @s run function bm:{pfx}/h/beamed', snd('block.beacon.power_select', 1.2, 1.4),
                                       'particle minecraft:end_rod ~ ~0.3 ~ 3 0.1 3 0.02 60'] + X.end)
    fn(f'{pfx}/h/support', ['effect give @a[distance=..8,gamemode=!spectator] minecraft:regeneration 5 1 true', 'effect give @e[type=minecraft:wolf,distance=..8] minecraft:regeneration 5 1 true',
                            'particle minecraft:end_rod ~ ~0.2 ~ 2 0.1 2 0.02 40', 'particle minecraft:wax_on ~ ~1 ~ 1.5 0.6 1.5 0 20', snd('block.beacon.power_select', 1.0, 1.8)])
    fn(f'{pfx}/h/kind', ['return 0'])
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {FOBJ} dummy']
    G.OBJECTIVES.append(FOBJ)
    return lines


def _encounter(G, X):
    """she is met at her fight's end (phase275b): every winner who hasn't met her yet joins her there"""
    fn, title, tellraw = G.fn, G.title, G.tellraw
    csay = lambda txt: title('@s', 'actionbar', [T('The Golden Doodle: ', COL, bold=True), T(txt, LINE)])
    fn('p275/enc/talk', ['execute if entity @s[tag=bm.gqmet] run return run ' + csay('(HONK! She knows you - she nibbles your sleeve)'),
                         'execute unless entity @s[tag=bm.gdwin] run return run ' + csay('(she honks at you, suspicious - you weren\'t there when the light came)'),
                         tellraw('@s', [T('She shakes out her feathers, honks once, and rolls a golden egg to your feet.', LINE, italic=True)]), 'function bm:p275/enc/joined'])
    import phase275b as B
    B.build(G, X, Doodle)


# ---------------------------------------------------------------------------------------------------- her three forms
def _forms(G, C):
    fn, pfx, ab, title = G.fn, C.pfx, C.ab, G.title
    sel = f'bm.{ab}sel'
    psel = lambda p: f'@e[type=minecraft:item_display,tag={sel},tag=bm.{ab}p_{p}]'
    mine = f'@e[type=minecraft:wolf,tag=bm.{ab}pet]'
    say = lambda txt: title('@s', 'actionbar', [T('The Golden Doodle: ', COL, bold=True), T(txt, LINE)])
    # ---- every pose: the form's own, solved on its own rig's joints (rigpet wrote one per cycle key: each rewritten here)
    names = sorted(set([n[len(f'{pfx}/pose/'):] for n in G.FUNCS if n.startswith(f'{pfx}/pose/')]) | set(VMAP))
    for name in names:
        assert name in VMAP, name
        dur = C.DUR.get(name, 6)
        for f in (1, 2):
            fn(f'{pfx}/pose/{"-kh"[f]}/{name}', W5.form_pose(A0, FORMS[f], FORMS[f].POSES[VMAP[name][f]], dur, psel))
        fn(f'{pfx}/pose/{name}', [f'execute if entity @s[tag=bm.gqf1] run return run function bm:{pfx}/pose/k/{name}',
                                  f'execute if entity @s[tag=bm.gqf2] run return run function bm:{pfx}/pose/h/{name}'] +
           W5.form_pose(A0, FORMS[0], FORMS[0].POSES[VMAP[name][0]], dur, psel))
    # ---- her dress: the form's models (the owner's bm.gqform), the host tagged, her hitbox; then the wardrobe's look over them
    D_ = G.FUNCS[f'{pfx}/dress']
    k = D_.index('scoreboard players set #wk bm.rng 0')
    D_[k:k] = ['scoreboard players set #gf bm.rng 0', f'execute as @a if score @s bm.pid = #me bm.pid run scoreboard players operation #gf bm.rng = @s {FOBJ}',
               f'execute as {mine} if score @s bm.pid = #me bm.pid run tag @s remove bm.gqf1', f'execute as {mine} if score @s bm.pid = #me bm.pid run tag @s remove bm.gqf2',
               f'execute if score #gf bm.rng matches 1 as {mine} if score @s bm.pid = #me bm.pid run tag @s add bm.gqf1',
               f'execute if score #gf bm.rng matches 2 as {mine} if score @s bm.pid = #me bm.pid run tag @s add bm.gqf2',
               f'execute unless score #gf bm.rng matches 1..2 run function bm:{pfx}/f0/dress', f'execute if score #gf bm.rng matches 1 run function bm:{pfx}/f1/dress',
               f'execute if score #gf bm.rng matches 2 run function bm:{pfx}/f2/dress', f'execute as {mine} if score @s bm.pid = #me bm.pid run function bm:{pfx}/fit']
    for f in range(3):
        fn(f'{pfx}/f{f}/dress', [f'execute as {psel(p)} run data modify entity @s item.components."minecraft:item_model" set value "bm:{PRE[f]}{p}"' for p in A0.PARTS])
    # ---- her hitbox and her host's size: the form's (and the big forms' companion size)
    import compsize as CSZ
    fn(f'{pfx}/fit', [f'execute if entity @s[tag=bm.gqf1,tag=bm.gqcz] run return run function bm:{pfx}/fit/kc', f'execute if entity @s[tag=bm.gqf1] run return run function bm:{pfx}/fit/k',
                      f'execute if entity @s[tag=bm.gqf2,tag=bm.gqcz] run return run function bm:{pfx}/fit/hc', f'execute if entity @s[tag=bm.gqf2] run return run function bm:{pfx}/fit/h',
                      f'function bm:{pfx}/fit/q'])
    for nm, ((w, h), sc) in FIT.items():
        fn(f'{pfx}/fit/{nm}', CSZ.resize(f'bm.{ab}hit', w, h, sc))
    fn(f'{pfx}/box_fit', [f'function bm:{pfx}/fit'])
    # ---- COMPANION SIZE (compsize, as the Rat King's): the big forms' poses twinned at CSZ_K; never the goose (she is her own size)
    CSZ.build(G, pfx, 'bm.gucs', 'bm.gqcz', f'bm.{C.q}s', FIT['k'][1], FIT['kc'][1],
              say('(she settles down to about your size - Companion Size: on)'), say('(she rises to her full height - Companion Size: off)'))
    for o in ('on', 'off'):
        L = G.FUNCS[f'{pfx}/csz/{o}']
        G.FUNCS[f'{pfx}/csz/{o}'] = [l for l in L if not l.startswith('attribute ')] + [f'function bm:{pfx}/fit']
    CSZ.LATE.append((pfx, CSZ_K, 'bm.gqcz', ()))
    T_ = G.FUNCS[f'{pfx}/tick']
    assert T_[0] == 'scoreboard players operation #me bm.pid = @s bm.pid', T_[0]
    T_[1:1] = ['scoreboard players set #cz bm.rng 0', 'execute on owner if score @s bm.gucs matches 1 run scoreboard players set #cz bm.rng 1',
               'execute unless entity @s[tag=bm.gqf1] unless entity @s[tag=bm.gqf2] run scoreboard players set #cz bm.rng 0',
               f'execute if score #cz bm.rng matches 1 unless entity @s[tag=bm.gqcz] run function bm:{pfx}/csz/on',
               f'execute if score #cz bm.rng matches 0 if entity @s[tag=bm.gqcz] run function bm:{pfx}/csz/off']
    # ---- THE FORM BUTTON (as you): the next form - her host re-dressed, re-posed, re-fitted at once
    fn(f'{pfx}/form', [f'scoreboard players add @s {FOBJ} 1', f'execute if score @s {FOBJ} matches 3.. run scoreboard players set @s {FOBJ} 0',
                       f'execute if score @s {FOBJ} matches 0 run ' + say('(HONK. Just a goose again - the Golden Doodle.)'),
                       f'execute if score @s {FOBJ} matches 1 run ' + say('(the shard flares - and she is THE GILDED ELDRITCH. She remembers it; she wears it on purpose now.)'),
                       f'execute if score @s {FOBJ} matches 2 run ' + say('(a sunburst at her feet, a white flash - her LIGHTBRINGER FORM)'),
                       'scoreboard players operation #me bm.pid = @s bm.pid',
                       f'execute as {mine} if score @s bm.pid = #me bm.pid at @s run function bm:{pfx}/form_pet'])
    fn(f'{pfx}/form_pet', [f'execute as @e[type=minecraft:item_display,tag=bm.{ab}p_pet,tag=!bm.{ab}fade] if score @s bm.pid = #me bm.pid run tag @s add {sel}',
                           f'function bm:{pfx}/dress', f'tag @e[tag={sel}] remove {sel}', f'scoreboard players set @s bm.{C.q}s -1',
                           'execute if entity @s[tag=bm.gqf1] run particle minecraft:dust{color:[0.85,0.1,0.15],scale:1.6} ~ ~1.5 ~ 0.8 1.2 0.8 0 40',
                           'execute if entity @s[tag=bm.gqf1] run playsound minecraft:entity.warden.roar neutral @a[distance=..16] ~ ~ ~ 0.5 1.6',
                           'execute if entity @s[tag=bm.gqf2] run particle minecraft:end_rod ~ ~1.5 ~ 0.8 1.2 0.8 0.05 40',
                           'execute if entity @s[tag=bm.gqf2] run particle minecraft:totem_of_undying ~ ~1.5 ~ 0.6 1 0.6 0.3 30',
                           'execute if entity @s[tag=bm.gqf2] run playsound minecraft:block.beacon.activate neutral @a[distance=..16] ~ ~ ~ 1 1.6',
                           'execute unless entity @s[tag=bm.gqf1] unless entity @s[tag=bm.gqf2] run particle minecraft:wax_on ~ ~0.8 ~ 0.4 0.4 0.4 0 20',
                           'execute unless entity @s[tag=bm.gqf1] unless entity @s[tag=bm.gqf2] run playsound minecraft:entity.goat.screaming.ambient neutral @a[distance=..16] ~ ~ ~ 0.8 1.7'])
    # ---- her doll (Cecil's, set down): sneak + right-click it - the goose, the Eldritch, the Lightbringer form, round again
    Ck = G.FUNCS['p141/doll_gdoodle/click']
    Ck[0:0] = ['scoreboard players set #snk bm.rng 0', 'execute on target if predicate bm:p20/sneaking run scoreboard players set #snk bm.rng 1',
               f'execute if score #snk bm.rng matches 1 run return run function bm:{pfx}/doll/cycle']
    fn(f'{pfx}/doll/cycle', [f'execute as @e[type=minecraft:item_display,tag=bm.doll_gdoodled,distance=..0.4] run function bm:{pfx}/doll/next',
                             'playsound minecraft:block.amethyst_block.chime block @a[distance=..12] ~ ~ ~ 0.8 1.4', 'particle minecraft:wax_on ~ ~0.6 ~ 0.25 0.25 0.25 0 10',
                             'data remove entity @s interaction'])
    fn(f'{pfx}/doll/next', ['execute if items entity @s contents *[minecraft:item_model="bm:doll_gdoodle"] run return run data modify entity @s item.components."minecraft:item_model" set value "bm:doll_gdoodle_k"',
                            'execute if items entity @s contents *[minecraft:item_model="bm:doll_gdoodle_k"] run return run data modify entity @s item.components."minecraft:item_model" set value "bm:doll_gdoodle_h"',
                            'data modify entity @s item.components."minecraft:item_model" set value "bm:doll_gdoodle"'])
    fn('admin/gdoodle_reset', ['tag @s remove bm.gqmet', 'tag @s remove bm.gdwin', 'tag @s remove bm.gdbeat', f'scoreboard players set @s {FOBJ} 0',
                               f'clear @s *[minecraft:custom_data~{{bm:"{ITEM}"}}]', title('@s', 'actionbar', T('The Golden Doodle has not met you yet.', COL))])


def late(G):
    """(after phase34's Rabbit's Foot) her Lucky passive: out in the Overworld at dusk, tonight's Lucky Night roll is 2 in 100"""
    roll = G.FUNCS['p22/lucky/roll']
    k = roll.index('scoreboard players set #lchance bm.bm 1')
    roll.insert(k + 1, 'execute in minecraft:overworld positioned 0 0 0 if entity @e[type=minecraft:wolf,tag=bm.gqpet,distance=0..] run scoreboard players set #lchance bm.bm 2')


def generate(G):
    title = G.title
    frame = dict(models=[], click=['playsound minecraft:entity.goat.screaming.ambient block @a[distance=..12] ~ ~ ~ 0.7 1.8', 'particle minecraft:wax_on ~ ~0.2 ~ 0.2 0.1 0.2 0 10'],
                 tick=['execute unless score #lnight bm.bm matches 1 run tag @s remove bm.gqfnug',
                       'execute if score #lnight bm.bm matches 1 unless entity @s[tag=bm.gqfnug] run function bm:p275/frame/nugget'])
    W5.build(Doodle, G, _abilities, _encounter, sitb=(160, [(0, 'sit_b'), (80, 'sit_b')]), frame=frame)
    G.fn('p275/frame/nugget', ['tag @s add bm.gqfnug', 'summon minecraft:item ~ ~-0.3 ~ {Item:{id:"minecraft:gold_nugget",count:1}}',
                               'particle minecraft:wax_on ~ ~ ~ 0.2 0.2 0.2 0 10', 'playsound minecraft:entity.goat.screaming.ambient block @a[distance=..12] ~ ~ ~ 0.5 1.9'])
    _forms(G, Doodle)

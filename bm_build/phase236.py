"""2.97: THE LIGHTBRINGER AND THE PALE DRYAD (lightbringer_art, pale_dryad_art; the machinery is rigpet's, the abilities' shape
phase235's).

THE LIGHTBRINGER (The Herald's Feather) - HARD MODE ONLY   a herald of the Divine One, the light set against the Dread: translucent,
  in white and gold, royal blue and purple at the edges. She comes only in hard mode, and only BEFORE you face what stands behind
  the Dread (bm.dfin - the final reckoning; once that's done, she's no longer to be found). By day, under the open sky, wearing
  something holy (anything a Golden Cross has made holy), she may come down to you; speak to her and she stays.
  SMITE a foe within 12, every 3 s: a pillar of light (8; 14 to the undead). BLESS you, hurt in a fight, every 8 s: Regeneration II
  and Absorption, your followers healed too. WARD (charged, every minute): her wings close round you - you and your followers
  Resistance II and Absorption II; the monsters near pushed back (6, the undead set alight). PRAY out of a fight: a meal's worth and
  Regeneration. THE OPHANIM (2.99a; three or more monsters near, every 90 s): her true form, a wheel within a wheel, full of eyes -
  light falls three times on every monster within 16. SHE LOVES IT WHEN YOU WEAR HOLY THINGS: beside her, wearing something holy, she beams - Regeneration while you're
  near, her smite +4, her blessing and her prayer stronger.
  (3.0) SHE OR HE: the herald may be a woman or a man - the same light. The first time you meet the Lightbringer (however: the sky,
  the Summons' herald, an admin's meet, the feather got another way and first used) it's 50/50 which, and kept for you (bm.lhform:
  0 she, 1 he); the menu's "Form: Herald (she)" / "(he)" switches it (code MENU+3, rigpet's FORM). His look: lightbringer_art's '_m'
  twin of every part (the same rig, poses, faces, Ophanim). Whoever met her before this keeps her. Every line of hers that says
  she / her has a twin for him (gender_split); her bonds and her feather's lore say "the herald" instead.
THE PALE DRYAD (A Glowing Mushroom)   a little spirit of the Pale Garden, all blue and orange mushrooms; she GLOWS SOFTLY AT NIGHT.
  In a Pale Garden at night she may be there among the moss; offer her a mushroom and she comes along. SWIPE a foe within 2.4 (5).
  SPORES two or more foes within 4.5, every 12 s: drowsy spores (3, poisoned, slowed). ROOTS (charged, every minute): roots burst up
  under everything near (8, held fast). HEAL you, hurt in a fight, every 10 s: Regeneration II, your followers too. BLOOM out of a
  fight: a meal's worth and Regeneration.
Both: sitting, a wardrobe, a rare aura, a shiny, the Partner Wheel, a frame, a display case, Cecil's doll, the honours, a Raid
Contract, and a pair with Bender, Mr. Capshun, Henry and Nia."""
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import math
import lightbringer_art as LA, pale_dryad_art as PA, ophan_art as OA
import rigfol as RF
import rigpet as RP
import rigface as RF2
import phase141 as P141
import phase134 as P134
import phase235 as P235
import phase95 as FX

HOLY = '#ffe08a'
OPH_X, OPH_Y, OPH_K = 120, 3.9, 4          # (the Ophanim: 6 s; its centre 3.9 above her; a spin keyframe every 4 ticks)


def _q(axis, deg):
    h = math.radians(deg) / 2
    v = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}[axis]
    return [F(round(v[0] * math.sin(h), 5)), F(round(v[1] * math.sin(h), 5)), F(round(v[2] * math.sin(h), 5)), F(round(math.cos(h), 5))]
ANGEL = '*[minecraft:custom_data~{bm_angel:1b}]'
item_particle = P235.item_particle


class Lightbringer(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'lightbringer', 'The Lightbringer', '#ffe08a', '#fff4d0', 'p236l', 'lh', 'lz'
    A = RF2.art(LA)
    MENU, PET_HP, PET_CD, ITEM = 4850, 40, 120, 'herald_feather'
    pron, they = 'her', 'she'
    FACE = {'happy': 'happy', 'surprised': 'surprised', 'hurt': 'hurt', 'sleepy': 'blink', 'blink': 'blink', 'squint': 'happy', 'serious': 'fierce'}
    ATTRS = dict(armor=6, attack_damage=4, movement_speed=0.38, follow_range=32, step_height=1.1)
    SCALE, HIT = 0.9, (0.9, 1.9)
    SWAP = RF2.swapping(LA)
    SWAP_START = True
    CYCLE = P235.cycle((240, [(0, 'idle_a'), (80, 'idle_b'), (160, 'idle_c'), (210, 'idle_a')]), (240, [(0, 'sit_a'), (120, 'sit_b')]),
                       (None, [(0, 'happy'), (10, 'wings_spread_up'), (16, 'wings_spread'), (26, 'happy')]),
                       {8: (None, [(0, 'smite_up'), (6, 'smite'), (14, 'smite_end')]), 13: (None, [(0, 'bless_a'), (6, 'bless'), (20, 'idle_a')]),
                        12: (None, [(0, 'ward_up'), (6, 'ward'), (24, 'wings_spread')]), 15: (None, [(0, 'ward_up')]), 14: (None, [(0, 'pray'), (30, 'happy')])})
    DUR = dict(P235._DUR, smite_up=4, smite=2, smite_end=6, bless_a=4, bless=6, ward_up=4, ward=6, pray=10, wings_spread_up=4, wings_spread=6)
    QUIPS = ['"Light holds. It always holds."', '"The Divine One sees you. Walk on."', '"Be not afraid - I am only the herald."',
             '"The Dread cannot abide the dawn."', '"Rest a moment. I will keep watch."', '(she hums something very old and very kind)']
    HELLO = ('(the Lightbringer glides back to your side, her halo brightening)', '(a pillar of soft light - and the Lightbringer steps out of it) "I am here."',
             '(she bows, and rises into the light, and is gone)')
    SIT = ('"Shall we go on?"', '(she kneels and folds her wings, the staff across her lap)')
    FAINT = '"The light... dims, but it does not go out..."'
    NOT_YOURS = '"Peace to you, traveller. I walk with another."'
    POWERS = [('Smite', 'a foe within 12, every 3 s: a pillar of light comes down on it - 8, and 14 to the undead'),
              ('Bless', 'you, hurt in a fight, every 8 s: Regeneration II and Absorption - and your followers healed too'),
              ('Ward', 'charged, every minute: her wings close round you - you and your followers Resistance II and Absorption II; the monsters near pushed back (6, the undead set alight)'),
              ('Ophanim', 'three or more monsters near, every 90 s: she takes her true form - a wheel within a wheel, full of eyes - and light falls three times on every monster within 16 (14, and 20 to the undead)'),
              ('Pray', 'out of a fight beside you, every minute: a meal\'s worth, and Regeneration'),
              ('Light in the Dark', 'by night, underground or beyond the Overworld the herald shines - every feather of light'),
              ('Holy Favour', 'she loves it when you wear holy things (anything a Golden Cross has made holy): beside her, you heal; her smite strikes harder (+4); her blessing and her prayer are stronger')]
    INTRO = [T('The Lightbringer', HOLY, bold=True), T(' - a herald of the Divine One, the light against the Dread. ', 'gray'),
             T('She loves it when you wear holy things.', 'white')]
    BUTTONS = ()
    # (3.0: the owner - "a toggleable male variant", the first form met chosen at random: HE - lightbringer_art's '_m' twins of
    #  every part; bm.lhform 1 on the owner. The button's words follow the form shown: "Form: Herald (she)" / "(he)" - gender_split)
    FORM = ('bm.lhform', LA.MALE, 'Form: Herald (she)', None, '"As you would see me, so I am. The light wears many faces."',
            '"As I was, then. It is the same light."', 'How the herald appears to you - a woman or a man: the same light either way. (Kept for you.)')
    FORM_FX = ['particle minecraft:end_rod ~ ~1 ~ 0.4 0.8 0.4 0.05 24', 'particle minecraft:flash{color:[1.0,0.92,0.6,1.0]} ~ ~1 ~ 0 0 0 0 1',
               'playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..16] ~ ~ ~ 1 1.4']
    BURST = ['particle minecraft:end_rod ~ ~1 ~ 0.3 0.6 0.3 0.05 20', 'particle minecraft:dust{color:[1.0,0.86,0.42],scale:1.2} ~ ~1.2 ~ 0.4 0.6 0.4 0 16']
    FADE_SOUND = 'playsound minecraft:block.beacon.deactivate neutral @a[distance=..20] ~ ~ ~ 0.8 1.4'
    SUMMON_EXTRA = ['playsound minecraft:block.beacon.activate neutral @a[distance=..24] ~ ~ ~ 0.6 1.6', 'playsound minecraft:block.amethyst_block.chime neutral @a[distance=..24] ~ ~ ~ 1 1.2']
    ENC_POSES = [(0, 'pray'), (40, 'bless_a'), (60, 'idle_a')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 20 run particle minecraft:end_rod ~ ~2 ~ 0.3 0.3 0.3 0.01 4'
    ADV = ('Herald of the Light', 'Be found worthy by the Lightbringer, before the Dread\'s master')
    ADMIN_HINT = 'Hard mode, before the Dread\'s master is faced: by day, under the open sky, wearing something holy - she comes down.'
    MEET_HINT = 'Hard mode: by day, in the open, wearing something holy.'


class Dryad(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'dryad', 'The Pale Dryad', '#6aa8f0', '#d8ecff', 'p236p', 'py', 'qd'
    A = RF2.art(PA)
    MENU, PET_HP, PET_CD, ITEM = 4900, 28, 120, 'dryad_cap'
    pron, they = 'her', 'she'
    FACE = {'happy': 'happy', 'surprised': 'surprised', 'hurt': 'sad', 'sleepy': 'sleepy', 'blink': 'blink', 'squint': 'happy', 'serious': 'fierce'}
    ATTRS = dict(armor=3, attack_damage=4, movement_speed=0.38, follow_range=32, step_height=1.1)
    SCALE, HIT = 0.65, (0.7, 1.2)
    SWAP = RF2.swapping(PA)
    SWAP_START = True
    CYCLE = P235.cycle((240, [(0, 'idle_a'), (80, 'idle_b'), (150, 'idle_c'), (210, 'idle_a')]), (240, [(0, 'sit_a'), (120, 'sit_b')]),
                       (None, [(0, 'happy')]),
                       {7: (None, [(0, 'swipe_up'), (3, 'swipe')]), 11: (None, [(0, 'spore_up'), (5, 'spore')]),
                        12: (None, [(0, 'root_up'), (6, 'root'), (16, 'root_hold'), (30, 'happy')]), 13: (None, [(0, 'heal_up'), (6, 'heal'), (20, 'idle_a')]),
                        14: (None, [(0, 'bloom_up'), (8, 'bloom'), (22, 'happy')])})
    DUR = dict(P235._DUR, swipe_up=3, swipe=2, spore_up=4, spore=3, root_up=4, root=4, root_hold=6, heal_up=4, heal=6, bloom_up=4, bloom=6)
    QUIPS = ['(she twirls, and her little mushrooms glow)', '"The moss says thank you."', '(a puff of glittering spores - she giggles)',
             '"Shh. Listen. The garden is breathing."', '"Mushrooms are just flowers that like the dark, you know."', '(she pats a mushroom on her shoulder; it glows brighter)']
    HELLO = ('(the Pale Dryad pitter-patters back to you)', '(moss rustles, and a little mushroom-capped girl pops up beside you) "Hello again!"',
             '(she waves, and sinks back into the moss)')
    SIT = ('"Up we go!"', '(she sits down in a little ring of mushrooms)')
    FAINT = '"I need... a little sleep... in the moss..."'
    NOT_YOURS = '"You smell nice - like rain! But I\'m somebody else\'s."'
    POWERS = [('Swipe', 'a foe within 2.4, every second: 5'),
              ('Spores', 'two or more foes within 4.5, every 12 s: drowsy spores - 3, poisoned and slowed'),
              ('Roots', 'charged, every minute: roots burst up under every monster near - 8, and they\'re held fast'),
              ('Heal', 'you, hurt in a fight, every 10 s: Regeneration II - and your followers too'),
              ('Bloom', 'out of a fight beside you, every minute: a meal\'s worth, and Regeneration'),
              ('Night Glow', 'by night she glows softly - blue and orange, like her mushrooms')]
    INTRO = [T('The Pale Dryad', '#6aa8f0', bold=True), T(' - a little spirit of the Pale Garden. ', 'gray'),
             T('Blue and orange mushrooms, and a soft glow by night.', 'white')]
    BUTTONS = ()
    BURST = ['particle minecraft:spore_blossom_air ~ ~0.8 ~ 0.4 0.4 0.4 0 20', 'particle minecraft:dust{color:[0.4,0.66,1.0],scale:0.9} ~ ~0.8 ~ 0.3 0.4 0.3 0 10']
    FADE_SOUND = 'playsound minecraft:block.moss.break neutral @a[distance=..20] ~ ~ ~ 1 1.2'
    SUMMON_EXTRA = ['playsound minecraft:block.creaking_heart.idle neutral @a[distance=..24] ~ ~ ~ 0.4 1.6', 'playsound minecraft:block.moss.place neutral @a[distance=..24] ~ ~ ~ 1 1.2']
    ENC_POSES = [(0, 'sit_b'), (40, 'idle_c'), (60, 'happy')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 20 run particle minecraft:dust{color:[0.4,0.66,1.0],scale:0.7} ~ ~0.8 ~ 0.3 0.3 0.3 0 4'
    ADV = ('Moss and Moonlight', 'Make friends with the little spirit of the Pale Garden')
    ADMIN_HINT = 'In a Pale Garden at night she\'s among the moss now and then. Offer her a mushroom.'
    MEET_HINT = 'A Pale Garden, at night. Bring a mushroom.'


PAIR = (Lightbringer, Dryad)
for _C in PAIR:
    RP.register(_C)
    RF2.setup(_C, 'head')

item('herald_feather', TOTEM, "The Herald's Feather", HOLY,
     ['A long white feather, its tip dipped in gold light.', 'It is warm. It is always warm.', ('Hard mode: a herald of the Divine One.', '#9a7aff'),
      ('Use: call the herald (again: call to your side).', 'blue'), ('Sneak + use: the herald\'s menu.', 'blue'), ('The herald loves it when you wear holy things.', 'blue'),
      ('If the herald faints: 2 minutes before returning.', 'gray')],      # (3.0: said without she/he - the herald may be either)
     model='bm:herald_feather', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
item('dryad_cap', TOTEM, 'A Glowing Mushroom', '#6aa8f0',
     ['A little blue mushroom with orange spots,', 'from the Pale Garden. It glows softly in the dark.',
      ('Use: call the Pale Dryad (again: call her over).', 'blue'), ('Sneak + use: her menu.', 'blue'), ('Spores, roots, and healing.', 'blue'),
      ('If she faints: 2 minutes before she can return.', 'gray')],
     model='bm:dryad_cap', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
for _C, _txt in ((Lightbringer, 'A doll of the Lightbringer - white and gold, with a tiny halo.'), (Dryad, 'A doll of the Pale Dryad - a mushroom cap bigger than she is.')):
    _w = _C.W
    item(f'doll_{_w}', TOTEM, f'{_C.NAME[4:]} Doll', _C.COL, [_txt, ('Right-click a block: set it down.', 'blue'), ('Right-click it: it twirls.', 'blue'),
                                                            ('Sneak + punch: pick it up.', 'gray')], model=f'bm:doll_{_w}', stack=16, cat='fun', comps=hold('none'))
    HOLD[f'doll_{_w}'] = f'bm:p141/doll_{_w}/use'
    P141.DOLLS.append((f'doll_{_w}', _C.NAME, _C.COL, _txt, 'minecraft:end_rod', 'minecraft:block.amethyst_block.chime', 'minecraft:poof'))
    P134.FIT[_C.ITEM] = {'lightbringer': (0.071, 1.959, -0.918, 0.918, -0.669, 0.327), 'dryad': (0.000, 1.203, -0.307, 0.285, -0.300, 0.270)}[_w]   # (measured: phase134.measure)
P141.DOLL_FROM['doll_lightbringer'] = ('herald_feather', {'kh': 1.55, 'kb': 0.82, 'kl': 0.62})
P141.DOLL_FROM['doll_dryad'] = ('dryad_cap', {'kh': 1.4, 'kb': 0.85, 'kl': 0.7})       # (she's a chibi already: a little less warp)

# ---- their pairs with Bender and Mr. Capshun (Henry's and Nia's: cat_bonds)
import phase188 as P188
_O = P188.O
_eff = lambda *es: [f'effect give {_O} minecraft:{e} {15 if e == "night_vision" else 3} {a} true' for e, a in es]
P188.VNAME.update({'lightbringer': 'the Lightbringer', 'dryad': 'the Pale Dryad'})
P188.PAIRS.update({
    'lh_bender': ('lightbringer', 'bender', 'Blessed Boy', '#e0a860', 'The Lightbringer and Bender - the goodest boy, blessed',
                  _eff(('regeneration', 0), ('speed', 0)),
                  [('bender', '(sits, very straight, in the herald\'s light)'), ('lightbringer', '"Yes. You are a good boy. The best of them."')],
                  [('bender', '(brings the herald a stick, solemnly)', 'lightbringer', '"I shall treasure it." (and throws it anyway)')]),
    'lh_capshun': ('lightbringer', 'capshun', 'And There Was Light', '#f0f0f0', 'The Lightbringer and Mr. Capshun - the narrator meets a real angel',
                   _eff(('resistance', 0), ('haste', 0)),
                   [('capshun', '[Mr. Capshun narrates: "And there was light. Quite a lot of it, actually."]'), ('lightbringer', '"You tell it well, little one."')],
                   [('capshun', '[Mr. Capshun narrates: "He tried to draw the herald\'s halo. It came out a doughnut."]', 'lightbringer', '"I like doughnuts."')]),
    'py_bender': ('dryad', 'bender', 'Mushroom Hunt', '#e0a860', 'The Pale Dryad and Bender - he sniffs out the mushrooms, she makes them glow',
                  _eff(('luck', 0), ('speed', 0)),
                  [('bender', '(sniffs a mushroom on her shoulder, sneezes)'), ('dryad', '(giggles) "Bless you!"')],
                  [('dryad', '"Find one, Bender!"', 'bender', '(finds one. It glows. He is so proud.)')]),
    'py_capshun': ('dryad', 'capshun', 'Sketchbook Garden', '#f0f0f0', 'The Pale Dryad and Mr. Capshun - he draws the garden, she grows it',
                   _eff(('regeneration', 0), ('haste', 0)),
                   [('capshun', '[Mr. Capshun narrates: "In the pale garden, something small and kind."]'), ('dryad', '"That\'s me! Draw my mushrooms!"')],
                   [('capshun', '[Mr. Capshun narrates: "He drew her a mushroom. She made it glow."]', 'dryad', '"Now it\'s real!"')]),
})
P188.ICON.update({'lh_bender': 'bm:herald_feather', 'lh_capshun': 'bm:herald_feather', 'py_bender': 'bm:dryad_cap', 'py_capshun': 'bm:dryad_cap'})


def extend_offers(O, offer):
    pass


def _icon(w):
    from PIL import Image, ImageDraw
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if w == 'lightbringer':                            # a white feather, its tip gold
        d.line((3, 14, 12, 3), fill=(220, 190, 120, 255))
        for i in range(8):
            x, y = 4 + i, 12 - i
            d.line((x, y, x + 2, y - 3), fill=(250, 250, 255, 255)); d.line((x, y, x - 2, y - 2), fill=(236, 236, 248, 255))
        d.point((12, 3), fill=(255, 220, 110, 255)); d.point((11, 3), fill=(255, 220, 110, 255)); d.point((12, 4), fill=(255, 220, 110, 255))
        d.point((13, 2), fill=(255, 240, 170, 255))
    else:                                              # a blue mushroom with orange spots
        d.pieslice((2, 2, 13, 12), 180, 360, fill=(60, 110, 220, 255), outline=(30, 60, 140, 255))
        d.rectangle((6, 7, 9, 14), fill=(236, 226, 200, 255), outline=(170, 150, 120, 255))
        for x, y in ((5, 4), (9, 3), (11, 6), (4, 6)):
            d.point((x, y), fill=(250, 150, 50, 255))
        d.line((3, 7, 12, 7), fill=(240, 140, 60, 255))
    return im.resize((32, 32), 0)


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    for _C in PAIR:
        RP.rp(_C, R, _icon(_C.W))
        RF2.faces(_C, 'head', R)


def textures():
    T_ = {}
    for A in (LA, PA):
        T_.update(A.textures())
    return T_


def generate_early(G):
    for _C in PAIR:
        RP.contract(_C, G)


def _light(G, X):
    fn, pfx, foe, S = G.fn, X.pfx, X.foe, X.S
    K = dict(ranged=dict(st=8, x=18, at=12, cd=60, near=0.5, far=12, face='serious', go=['playsound minecraft:block.beacon.power_select neutral @a[distance=..16] ~ ~ ~ 0.5 1.8']),
             support=dict(st=13, x=22, at=14, cd=160, face='happy'),
             charged=dict(st=12, x=30, at=22, cd=1200, r=6, face='serious', go=['playsound minecraft:item.elytra.flying neutral @a[distance=..16] ~ ~ ~ 0.3 1.6']),
             kind=dict(st=14, x=34, at=16, cd=1200, face='happy'),
             crowd=dict(st=15, x=OPH_X, at=[84, 54, 24], cd=1800, r=12, n=3, face='serious', during=(1, OPH_X - 1),
                        go=['function bm:p236l/oph/up']))
    lines = P235.kit(G, X, K)
    holy = f'function bm:p236l/holy_q'
    tg = f'@e[{foe},distance=..12,sort=nearest,limit=1]'
    # SMITE: a pillar of light - 8, the undead 14; +4 when you wear something holy
    fn(f'{pfx}/ranged', X.hit(8) + [f'execute on owner if {holy} run scoreboard players add #pd bm.rng 4', f'execute as {tg} at @s run function bm:{pfx}/smitten'] + X.end)
    fn(f'{pfx}/smitten', ['execute if entity @s[type=#minecraft:undead] run scoreboard players add #pd bm.rng 6', f'function bm:{pfx}/hurt',
                          'execute if entity @s[type=#minecraft:undead] run scoreboard players remove #pd bm.rng 6',
                          'particle minecraft:end_rod ~ ~3 ~ 0.08 2 0.08 0 50', 'particle minecraft:flash{color:[1.0,0.92,0.6,1.0]} ~ ~1 ~ 0 0 0 0 1',
                          'particle minecraft:dust{color:[1.0,0.86,0.42],scale:1.6} ~ ~1 ~ 0.3 1.2 0.3 0 30',
                          'playsound minecraft:entity.lightning_bolt.impact neutral @a[distance=..20] ~ ~ ~ 0.4 2.0'])
    # BLESS: you hurt in a fight - Regeneration II, Absorption (holy: III and II); your followers healed
    fn(f'{pfx}/support', ['execute on owner if entity @s[distance=..16] at @s run function bm:p236l/bless_you'])
    fn('p236l/bless_you', ['scoreboard players set #hf bm.rng 0', f'execute if {holy} run scoreboard players set #hf bm.rng 1',
                           'execute if score #hf bm.rng matches 0 run effect give @s minecraft:regeneration 6 1 true', 'execute if score #hf bm.rng matches 0 run effect give @s minecraft:absorption 20 0 true',
                           'execute if score #hf bm.rng matches 1 run effect give @s minecraft:regeneration 6 2 true', 'execute if score #hf bm.rng matches 1 run effect give @s minecraft:absorption 20 1 true',
                           'scoreboard players operation #me bm.pid = @s bm.pid',
                           *[f'execute as @e[type=minecraft:{t},distance=..12] if score @s bm.pid = #me bm.pid run effect give @s minecraft:regeneration 6 1 true' for t in ('wolf', 'cat')],
                           'particle minecraft:end_rod ~ ~1.2 ~ 0.4 0.6 0.4 0.02 12', 'particle minecraft:heart ~ ~1.6 ~ 0.3 0.2 0.3 0 2',
                           'playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1.6'])
    # WARD: her wings close round you
    fn(f'{pfx}/charged', X.hit(6) + ['execute on owner if entity @s[distance=..16] at @s run function bm:p236l/ward_you'] + X.end)
    fn('p236l/ward_you', ['effect give @s minecraft:resistance 10 1 true', 'effect give @s minecraft:absorption 30 1 true', 'scoreboard players operation #me bm.pid = @s bm.pid',
                          *[f'execute as @e[type=minecraft:{t},distance=..16] if score @s bm.pid = #me bm.pid run effect give @s minecraft:resistance 10 1 true' for t in ('wolf', 'cat')],
                          'tag @s add bm.lhme', 'execute as @e[type=#bm:hostile,tag=!bm.npc,distance=..5] at @s run function bm:p236l/warded', 'tag @s remove bm.lhme',
                          'particle minecraft:end_rod ~ ~1 ~ 1.2 0.8 1.2 0.05 40', 'particle minecraft:dust{color:[1.0,0.86,0.42],scale:1.4} ~ ~1 ~ 1.4 0.8 1.4 0 30',
                          'playsound minecraft:block.beacon.power_select player @a[distance=..16] ~ ~ ~ 1 1.2'])
    fn('p236l/warded', ['function bm:p236l/hurt', 'execute if entity @s[type=#minecraft:undead] run data merge entity @s {Fire:80s}',
                        'execute facing entity @a[tag=bm.lhme,limit=1] feet positioned ^ ^0.2 ^-2.5 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~ ~',
                        'particle minecraft:end_rod ~ ~1 ~ 0.2 0.4 0.2 0.05 6'])
    # THE OPHANIM (2.99a): three or more foes near - she becomes what she truly is, a wheel within a wheel, full of eyes (ophan_art),
    # and three times over every foe within 16 is struck from above (14; 20 to the undead); then she is herself again
    for i in ('', '2', '3'):
        fn(f'{pfx}/crowd{i}', X.hit(14) + [f'execute as @e[{foe},distance=..16] at @s run function bm:{pfx}/smitten',
                                          'particle minecraft:flash{color:[1.0,0.95,0.7,1.0]} ~ ~4 ~ 0 0 0 0 1',
                                          'playsound minecraft:block.beacon.power_select neutral @a[distance=..32] ~ ~ ~ 1 0.6',
                                          'playsound minecraft:entity.lightning_bolt.thunder neutral @a[distance=..32] ~ ~ ~ 0.4 1.8'] + X.end)
    osel = lambda p=None: '@e[type=minecraft:item_display,tag=bm.ophsel' + (f',tag=bm.oph_{p}]' if p else ']')
    fn('p236l/oph/up', ['scoreboard players operation #me bm.pid = @s bm.pid',
                        'execute as @e[type=minecraft:item_display,tag=bm.oph] if score @s bm.pid = #me bm.pid run kill @s'] +
       [f'summon minecraft:item_display ~ ~{OPH_Y} ~ {RF.part_nbt(OA, p, ["bm.oph", f"bm.oph_{p}", "bm.ophnew"], OA.SCALE, scale0=True, extra=dict(view_range=F(4.0), brightness={"block": Int(15), "sky": Int(15)}, teleport_duration=Int(2)))}'
        for p in OA.PARTS] +
       ['scoreboard players operation @e[type=minecraft:item_display,tag=bm.ophnew] bm.pid = #me bm.pid', 'tag @e[type=minecraft:item_display,tag=bm.ophnew] remove bm.ophnew',
        'particle minecraft:end_rod ~ ~2 ~ 1 1.5 1 0.2 80', 'particle minecraft:flash{color:[1.0,0.95,0.7,1.0]} ~ ~2 ~ 0 0 0 0 1',
        'playsound minecraft:block.beacon.activate neutral @a[distance=..32] ~ ~ ~ 1 0.5', 'playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..32] ~ ~ ~ 1 0.5',
        'execute on owner run ' + G.title('@s', 'actionbar', T('Be not afraid.', HOLY, bold=True))])
    tl = [f'scoreboard players operation #me bm.pid = @s bm.pid',
          'execute as @e[type=minecraft:item_display,tag=bm.oph] if score @s bm.pid = #me bm.pid run tag @s add bm.ophsel',
          f'execute positioned ~ ~{OPH_Y} ~ run tp {osel()} ~ ~ ~',
          f'execute if score @s {S("x")} matches {OPH_X - 9}..{OPH_X - 1} run function bm:p236l/oph/hide',
          f'execute if score @s {S("x")} matches {OPH_X - 2} as {osel()} run data merge entity @s {{start_interpolation:0,interpolation_duration:10,transformation:{{scale:[{OA.SCALE}f,{OA.SCALE}f,{OA.SCALE}f]}}}}',
          f'execute if score @s {S("x")} matches 10 as {osel()} run data merge entity @s {{start_interpolation:0,interpolation_duration:8,transformation:{{scale:[0f,0f,0f]}}}}',
          f'execute if score @s {S("x")} matches 2 run function bm:p236l/oph/down',
          f'execute if score @s {S("x")} matches 1..{OPH_X - 2} run particle minecraft:end_rod ~ ~{OPH_Y} ~ 2 2 2 0.01 2']
    for n in range(OPH_X - 4, 8, -OPH_K):
        tl.append(f'execute if score @s {S("x")} matches {n} run function bm:p236l/oph/k{n}')
        t = OPH_X - n
        fn(f'p236l/oph/k{n}', [f'execute as {osel(p)} run data merge entity @s {{start_interpolation:0,interpolation_duration:{OPH_K},transformation:{{left_rotation:{snbt(_q(OA.SPIN_AXIS[p], OA.SPIN_RATE[p] * t))}}}}}'
                               for p in OA.PARTS])
    tl.append(f'tag {osel()} remove bm.ophsel')
    fn(f'{pfx}/crowd_tick', tl)
    # (3.0: her own parts - the rig's 'sel' tag, bm.lhsel: X.psel isn't hers yet while her abilities are built, and it had shrunk the
    #  last follower built before her - the Speech Bubble's bm.wbsel - so she never hid behind the wheel)
    fn('p236l/oph/hide', [f'execute as @e[type=minecraft:item_display,tag=bm.{Lightbringer.ab}sel] run data merge entity @s {{start_interpolation:0,interpolation_duration:3,transformation:{{scale:[0f,0f,0f]}}}}'])
    fn('p236l/oph/stray', [f'execute unless entity @e[type=minecraft:wolf,tag=bm.lhpet,distance=..8] run kill @s'])
    G.FUNCS['loop/second'].append('execute as @e[type=minecraft:item_display,tag=bm.oph] at @s run function bm:p236l/oph/stray')
    fn('p236l/oph/down', [f'kill {osel()}', 'function bm:p236l/pose/wings_spread', 'particle minecraft:end_rod ~ ~1 ~ 0.4 0.8 0.4 0.1 30',
                          'playsound minecraft:block.beacon.deactivate neutral @a[distance=..32] ~ ~ ~ 1 1.2'])
    # PRAY: out of a fight - a meal's worth and Regeneration (holy: a little health back too)
    fn(f'{pfx}/kind', ['execute on owner if entity @s[distance=..8] run function bm:p236l/pray_you'])
    fn('p236l/pray_you', ['effect give @s minecraft:saturation 1 2 true', 'effect give @s minecraft:regeneration 10 0 true',
                          f'execute if {holy} run effect give @s minecraft:instant_health 1 0 true',
                          'particle minecraft:end_rod ~ ~2 ~ 0.3 0.2 0.3 0.01 10', 'playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 1.4'])
    return lines


def _dryad(G, X):
    fn, pfx, foe = G.fn, X.pfx, X.foe
    K = dict(melee=dict(st=7, x=6, at=3, cd=20, reach=2.4),
             crowd=dict(st=11, x=12, at=6, cd=240, r=4.5, face='serious'),
             charged=dict(st=12, x=34, at=24, cd=1200, r=7, face='serious', go=['playsound minecraft:block.rooted_dirt.break neutral @a[distance=..16] ~ ~ ~ 1 0.6']),
             support=dict(st=13, x=22, at=14, cd=200, face='happy'),
             kind=dict(st=14, x=26, at=14, cd=1200, face='happy'))
    lines = P235.kit(G, X, K)
    spores = ['particle minecraft:spore_blossom_air ~ ~1 ~ 0.6 0.4 0.6 0 16', 'particle minecraft:dust{color:[0.4,0.66,1.0],scale:0.8} ~ ~1 ~ 0.5 0.4 0.5 0 8',
              'particle minecraft:dust{color:[1.0,0.6,0.25],scale:0.8} ~ ~1 ~ 0.5 0.4 0.5 0 6']
    P235.melee(G, X, 5, 2.4, ['particle minecraft:block{block_state:"minecraft:pale_moss_block"} ~ ~1 ~ 0.2 0.3 0.2 0 10'], 'minecraft:block.moss.hit')
    fn(f'{pfx}/crowd', X.hit(3) + [f'execute as @e[{foe},distance=..4.5] at @s run function bm:{pfx}/spored', 'particle minecraft:spore_blossom_air ~ ~1 ~ 1.5 0.6 1.5 0 50',
                                   'playsound minecraft:block.spore_blossom.break neutral @a[distance=..16] ~ ~ ~ 1 1.2'] + X.end)
    fn(f'{pfx}/spored', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:poison 3 0', 'effect give @s minecraft:slowness 4 1'] + spores)
    fn(f'{pfx}/charged', X.hit(8) + [f'execute as @e[{foe},distance=..7] at @s run function bm:{pfx}/rooted', 'playsound minecraft:block.rooted_dirt.break neutral @a[distance=..16] ~ ~ ~ 1 0.6'] + X.end)
    fn(f'{pfx}/rooted', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 5 4', 'effect give @s minecraft:weakness 4 0',
                         'particle minecraft:block{block_state:"minecraft:pale_oak_log"} ~ ~0.3 ~ 0.4 0.4 0.4 0 30', 'particle minecraft:block{block_state:"minecraft:pale_hanging_moss"} ~ ~0.6 ~ 0.3 0.6 0.3 0 16'])
    fn(f'{pfx}/support', ['execute on owner if entity @s[distance=..16] at @s run function bm:p236p/heal_you'])
    fn('p236p/heal_you', ['effect give @s minecraft:regeneration 6 1 true', 'scoreboard players operation #me bm.pid = @s bm.pid',
                          *[f'execute as @e[type=minecraft:{t},distance=..12] if score @s bm.pid = #me bm.pid run effect give @s minecraft:regeneration 6 1 true' for t in ('wolf', 'cat')]] +
       spores[:2] + ['playsound minecraft:block.azalea_leaves.place player @s ~ ~ ~ 1 1.4'])
    fn(f'{pfx}/kind', ['execute on owner if entity @s[distance=..8] run function bm:p236p/bloom_you'])
    fn('p236p/bloom_you', ['effect give @s minecraft:saturation 1 2 true', 'effect give @s minecraft:regeneration 10 0 true'] + spores +
       ['playsound minecraft:block.spore_blossom.place player @s ~ ~ ~ 1 1.2'])
    return lines


def generate(G):
    fn, wjson, tellraw, title = G.fn, G.wjson, G.tellraw, G.title
    fn('p236l/holy_q', [f'execute if items entity @s armor.* {ANGEL} run return 1', f'execute if items entity @s weapon.* {ANGEL} run return 1', 'return 0'])
    wjson('bm/predicate/p236/day_sky.json', {'condition': 'minecraft:all_of', 'terms': [
        {'condition': 'minecraft:time_check', 'clock': 'minecraft:overworld', 'value': {'min': 0, 'max': 12000}, 'period': 24000},
        {'condition': 'minecraft:location_check', 'offsetY': 1.6, 'predicate': {'can_see_sky': True}}]})
    wjson('bm/predicate/p236/pale_night.json', {'condition': 'minecraft:all_of', 'terms': [
        {'condition': 'minecraft:time_check', 'clock': 'minecraft:overworld', 'value': {'min': 13000, 'max': 23000}, 'period': 24000},
        {'condition': 'minecraft:location_check', 'predicate': {'biomes': 'minecraft:pale_garden'}}]})
    wjson('bm/predicate/p236/night.json', {'condition': 'minecraft:time_check', 'clock': 'minecraft:overworld', 'value': {'min': 13000, 'max': 23000}, 'period': 24000})

    def place(p):
        fn(f'{p}/enc/place', [f'execute if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass unless block ~ ~-1 ~ #bm:grap_pass run return run function bm:{p}/enc/step',
                              f'execute positioned ~ ~1 ~ if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run function bm:{p}/enc/step'])

    # ---- THE LIGHTBRINGER: hard mode, before the reckoning - by day, in the open, wearing something holy
    def e_light(G, X):
        X.second.append('execute if score #hard bm.cfg matches 1 as @a[tag=!bm.lhmet,tag=!bm.dfin,gamemode=!spectator] at @s if dimension minecraft:overworld '
                        'if predicate bm:p236/day_sky if function bm:p236l/holy_q run function bm:p236l/enc/check')
        fn('p236l/enc/check', ['execute store result score #r bm.rng run random value 1..240', 'execute unless score #r bm.rng matches 1 run return 0',
                               'execute if entity @e[type=minecraft:interaction,tag=bm.lhenc,distance=..64] run return 0',
                               'execute positioned ^ ^ ^4 run function bm:p236l/enc/place'])
        place('p236l')
        # (2.99a: the Sovereign's Summons granted - p237/summons - the Divine One sends her: no holy thing needed, any light, anywhere)
        fn('p236l/enc/herald', ['execute if entity @s[tag=bm.lhmet] run return 0', 'execute if entity @s[tag=bm.dfin] run return 0',
                                f'execute if items entity @s container.* {X.holds("herald_feather")} run return 0',
                                'execute if entity @e[type=minecraft:interaction,tag=bm.lhenc,distance=..64] run return 0',
                                X.tellraw('@s', [T('The Summons is barely in your hand when the air above you brightens. ', '#fff4d0', italic=True),
                                                 T('Something answers it - not from below. From above.', 'gray', italic=True)]),
                                'execute positioned ^ ^ ^4 run function bm:p236l/enc/place'])
        X.second.append('execute if score #hard bm.cfg matches 1 as @a[tag=bm.usum,tag=!bm.lhmet,tag=!bm.dfin,gamemode=!spectator] at @s '
                        'unless entity @e[type=minecraft:interaction,tag=bm.lhenc,distance=..64] run function bm:p236l/enc/herald_again')
        fn('p236l/enc/herald_again', ['execute store result score #r bm.rng run random value 1..15', 'execute unless score #r bm.rng matches 1 run return 0',
                                      'execute positioned ^ ^ ^4 run function bm:p236l/enc/place'])
        fn('p236l/enc/step', ['function bm:p236l/enc/spawn', 'particle minecraft:end_rod ~ ~6 ~ 0.2 6 0.2 0 120', 'particle minecraft:flash{color:[1.0,0.92,0.6,1.0]} ~ ~1 ~ 0 0 0 0 1',
                              'playsound minecraft:block.beacon.activate neutral @a[distance=..32] ~ ~ ~ 1 1.2',
                              X.tellraw('@a[tag=!bm.lhmet,distance=..24]', [T('The sky opens a little, like a door. A pillar of light comes down - and in it, wings. ', '#fff4d0', italic=True),
                                                                             T('A herald of the Divine One kneels on the grass, and looks at what you\'re wearing, and smiles.', 'gray', italic=True)])])
        lsay = lambda txt: title('@s', 'actionbar', [T('The Lightbringer: ', HOLY, bold=True), T(txt, '#fff4d0')])
        fn('p236l/enc/talk', [f'execute if items entity @s container.* {X.holds("herald_feather")} run return run ' + lsay('"I am already with you, child of the light."'),
                              'execute if entity @s[tag=bm.dfin] run return run ' + lsay('"My work here is finished. Go in peace."'),
                              'execute unless score #hard bm.cfg matches 1 run return run ' + lsay('"Not yet. Not until the Dread rises."'),
                              'execute if entity @s[tag=bm.usum] run return run function bm:p236l/enc/recruit',
                              'execute unless function bm:p236l/holy_q run return run ' + lsay('"Wear the light, and I will walk beside you."'),
                              'function bm:p236l/enc/recruit'])
        fn('p236l/enc/recruit', [f'execute as {X.here} at @s run particle minecraft:end_rod ~ ~1.5 ~ 0.5 0.8 0.5 0.05 40', 'playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 1.2',
                                 'execute if entity @s[tag=bm.usum] run ' + X.tellraw('@s', [T('"The Divine One has heard the Summons too. What waits under the Nether will not be faced alone - '
                                                                                                 'I am sent to see it unmade." ', '#fff4d0', italic=True)]),
                                 X.tellraw('@s', [T('"The Divine One sees the light you carry. The Dread is rising - you will not face it alone." ', '#fff4d0', italic=True),
                                                  T('She plucks a feather from her wing, its tip still glowing, and puts it in your hand.', 'gray', italic=True)]),
                                 'function bm:p236l/enc/joined'])
        # (3.0) SHE OR HE: the first time she's met (any way: this encounter, the Summons' herald, an admin's meet - the herald
        # stands there already in the form chosen - or the feather got some other way and first used) it's 50/50 which, kept on
        # the player (bm.lhform: 0 she, 1 he; the menu's Form button switches it). Whoever had her before this keeps her.
        fn('p236l/form_roll', ['execute if score @s bm.lhform matches 0..1 run return 0',
                               'execute if entity @s[tag=bm.lhmet] run return run scoreboard players set @s bm.lhform 0',
                               f'execute if items entity @s container.* {X.holds("herald_feather")} run return run scoreboard players set @s bm.lhform 0',
                               'execute store result score @s bm.lhform run random value 0..1'])
        fn('p236l/enc/look', ['function bm:p236l/form_roll', 'execute unless score @s bm.lhform matches 1 run return 0'] +
           [f'execute as {X.psel(p)} run data modify entity @s item.components."minecraft:item_model" set value "bm:{LA.PREFIX}{p}{LA.MALE}"' for p in LA.PARTS])
    # ---- THE PALE DRYAD: a Pale Garden, at night - a mushroom wins her over
    def e_dryad(G, X):
        X.second.append('execute as @a[tag=!bm.pymet,gamemode=!spectator] at @s if dimension minecraft:overworld if predicate bm:p236/pale_night run function bm:p236p/enc/check')
        fn('p236p/enc/check', ['execute store result score #r bm.rng run random value 1..150', 'execute unless score #r bm.rng matches 1 run return 0',
                               'execute if entity @e[type=minecraft:interaction,tag=bm.pyenc,distance=..64] run return 0',
                               'execute positioned ^ ^ ^4 run function bm:p236p/enc/place'])
        place('p236p')
        fn('p236p/enc/step', ['function bm:p236p/enc/spawn', 'particle minecraft:spore_blossom_air ~ ~1 ~ 1 0.6 1 0 40',
                              'playsound minecraft:block.creaking_heart.idle neutral @a[distance=..24] ~ ~ ~ 0.6 1.6',
                              X.tellraw('@a[tag=!bm.pymet,distance=..16]', [T('Something glows in the pale moss - blue, and orange. ', '#d8ecff', italic=True),
                                                                             T('A little girl with a mushroom for a hat sits up, rubs her eyes, and waves at you.', 'gray', italic=True)])])
        dsay = lambda txt: title('@s', 'actionbar', [T('The Pale Dryad: ', '#6aa8f0', bold=True), T(txt, '#d8ecff')])
        fn('p236p/enc/talk', [f'execute if items entity @s container.* {X.holds("dryad_cap")} run return run ' + dsay('"You\'ve got my mushroom! That means we\'re friends!"')] +
           [f'execute if items entity @s weapon.mainhand {m} run return run function bm:p236p/enc/recruit' for m in ('minecraft:red_mushroom', 'minecraft:brown_mushroom')] +
           [dsay('"Do you have a mushroom? I like mushrooms. They\'re my friends."')])
        fn('p236p/enc/recruit', ['item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
                                 f'execute as {X.here} at @s run particle minecraft:spore_blossom_air ~ ~1 ~ 0.6 0.6 0.6 0 30', 'playsound minecraft:block.moss.place player @s ~ ~ ~ 1 1.4',
                                 X.tellraw('@s', [T('She holds the mushroom up to her cheek, very pleased - and it starts to glow, blue, with orange spots. ', '#d8ecff', italic=True),
                                                  T('She gives it back to you. "Now it\'s ours. Call me with it!"', 'gray', italic=True)]),
                                 'function bm:p236p/enc/joined'])
    RP.build(Lightbringer, G, _light, e_light)
    RP.build(Dryad, G, _dryad, e_dryad)
    G.FUNCS['admin/lightbringer'].insert(0, 'function bm:p236l/form_roll')          # (3.0: handed the feather - or first calling her - she or he)
    G.FUNCS['p236l/summon_here'].insert(0, 'function bm:p236l/form_roll')
    # ---- HOLY FAVOUR (the Lightbringer): wearing something holy beside her, you heal, and she beams
    G.FUNCS['loop/second'] += ['execute as @e[type=minecraft:wolf,tag=bm.lhpet,tag=!bm.ffpet] at @s run function bm:p236l/sec']
    fn('p236l/sec', ['scoreboard players set #hf bm.rng 0', 'execute on owner if entity @s[distance=..16] if function bm:p236l/holy_q run scoreboard players set #hf bm.rng 1',
                     'execute if score #hf bm.rng matches 0 run return 0', 'execute on owner run effect give @s minecraft:regeneration 3 0 true',
                     'particle minecraft:dust{color:[1.0,0.86,0.42],scale:0.8} ~ ~2.1 ~ 0.3 0.1 0.3 0 3', 'particle minecraft:end_rod ~ ~1.4 ~ 0.4 0.6 0.4 0.005 1',
                     'execute on owner unless entity @s[tag=bm.lhseen] run function bm:p236l/noticed',
                     'execute store result score #r bm.rng run random value 1..30', 'execute if score #r bm.rng matches 1 run function bm:p236l/beam'])
    fn('p236l/noticed', ['tag @s add bm.lhseen', tellraw('@s', [T('The Lightbringer: ', HOLY, bold=True), T('"Oh - you wear the light! It suits you. Stay near me."', '#fff4d0')])])
    fn('p236l/beam', FX.face_cmd('lightbringer', 'happy', 40) +
       ['execute on owner if entity @s[tag=!bm.hush] run ' + title('@s', 'actionbar', [T('The Lightbringer: ', HOLY, bold=True), T('(she beams at your holy raiment)', '#fff4d0')])])
    # ---- (the final reckoning - facing what stands behind the Dread - tags you bm.dfin; till it's built, an admin can set it, to stage it)
    fn('admin/reckoned', ['tag @s add bm.dfin', title('@s', 'actionbar', T('Marked: you have faced what stands behind the Dread. (The Lightbringer is no longer to be found.)', HOLY))])
    fn('admin/unreckoned', ['tag @s remove bm.dfin', title('@s', 'actionbar', T('Unmarked: the final reckoning is still ahead of you.', HOLY))])
    G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/reckoned', 'yellow'), T(' / ', 'gray'), T('unreckoned', 'yellow'),
                                                T('  mark the final reckoning faced (or not) - the Lightbringer comes only before it', 'gray')]))
    # ---- (3.0) THE LIGHTBRINGER SHINES IN THE DARK: by night, out of the Overworld or under a roof she glows all over (every
    #      part at full brightness, both forms); by day under the open sky she's lit by the world again
    wjson('bm/predicate/p236/daylit.json', {'condition': 'minecraft:all_of', 'terms': [
        {'condition': 'minecraft:inverted', 'term': {'condition': 'minecraft:time_check', 'clock': 'minecraft:overworld', 'value': {'min': 13000, 'max': 23000}, 'period': 24000}},
        {'condition': 'minecraft:location_check', 'offsetY': 1.0, 'predicate': {'can_see_sky': True, 'dimension': 'minecraft:overworld'}}]})
    G.FUNCS['loop/second'] += ['execute as @e[type=minecraft:wolf,tag=bm.lhpet,tag=!bm.ffpet] at @s run function bm:p236l/shine']
    fn('p236l/shine', ['scoreboard players operation #me bm.pid = @s bm.pid',
                       'execute unless predicate bm:p236/daylit as @e[type=minecraft:item_display,tag=bm.lhp,tag=!bm.lhglow,distance=..8] if score @s bm.pid = #me bm.pid run function bm:p236l/shine_on',
                       'execute if predicate bm:p236/daylit as @e[type=minecraft:item_display,tag=bm.lhglow,distance=..8] if score @s bm.pid = #me bm.pid run function bm:p236l/shine_off'])
    fn('p236l/shine_on', ['tag @s add bm.lhglow', 'data merge entity @s {brightness:{block:15,sky:15}}'])
    fn('p236l/shine_off', ['tag @s remove bm.lhglow', 'data remove entity @s brightness'])
    # ---- NIGHT GLOW (the Pale Dryad): blue and orange, soft, round her mushrooms by night
    G.FUNCS['loop/second'] += ['execute as @e[type=minecraft:wolf,tag=bm.pypet,tag=!bm.ffpet] at @s if predicate bm:p236/night run function bm:p236p/glow']
    fn('p236p/glow', ['particle minecraft:dust{color:[0.4,0.66,1.0],scale:0.6} ~ ~0.9 ~ 0.3 0.35 0.3 0 2', 'particle minecraft:dust{color:[1.0,0.6,0.25],scale:0.5} ~ ~0.7 ~ 0.3 0.3 0.3 0 1',
                      'particle minecraft:glow ~ ~0.8 ~ 0.25 0.3 0.25 0 1'])
    # ---- (3.0) SHE OR HE: every line of the Lightbringer's own that says she / her gets a twin for him, picked by the form
    print('3.0: the Lightbringer, he - %d lines given his words' % gender_split(G))


# ====================================================================== (3.0) the Lightbringer's words, for him
import re as _re
FEM = _re.compile(r'\b(she|her|hers|herself)\b', _re.I)
_TXT = _re.compile(r'text:"((?:[^"\\]|\\.)*)"')
_OBJ = {'home', 'to', 'and', 'in', 'on', 'with', 'over', 'from', 'back', 'again', 'up', 'down', 'out', 'a', 'an', 'the', 'is', 'was', 'as',
        'for', 'at', 'by', 'into', 'when', 'while', 'if', 'so', 'that', 'now', 'go', 'be', 'or', 'but', 'away', 'off', 'here', 'there', 'too'}


def he(t):
    """her words, said of him: she -> he, herself -> himself, hers -> his; her -> his before a noun ('her halo', 'her menu'), him
    otherwise ('call her over', 'Send her home', 'from her.')"""
    cap = lambda w, m: m.capitalize() if w[0].isupper() else m
    t = _re.sub(r'\b([Hh]erself)\b', lambda m: cap(m.group(1), 'himself'), t)
    t = _re.sub(r'\b([Hh]ers)\b', lambda m: cap(m.group(1), 'his'), t)
    t = _re.sub(r'\b([Ss]he)\b', lambda m: cap(m.group(1), 'he'), t)

    def her(m):
        rest = m.string[m.end():]
        nxt = _re.match(r"\s*([A-Za-z']*)", rest).group(1).lower()
        return cap(m.group(1), 'him' if (not rest[:1].isspace() or not nxt or nxt in _OBJ) else 'his')
    return _re.sub(r'\b([Hh]er)\b', her, t)


def gender_split(G, names=None):
    """each line of hers (the Lightbringer's functions: p236l/*, her wardrobe's 'wear it now', the admin's) whose words say she or her
    becomes two: his words when the form is his (#lhm, set by p236l/mk just before, from whoever runs it - the player, or her host's
    owner), hers otherwise. Run once, after she's built."""
    G.fn('p236l/mk', ['scoreboard players set #lhm bm.rng 0',
                      'execute if entity @s[type=minecraft:player] if score @s bm.lhform matches 1 run return run scoreboard players set #lhm bm.rng 1',
                      'execute if entity @s[type=minecraft:player] run return 0',
                      'execute on owner if score @s bm.lhform matches 1 run scoreboard players set #lhm bm.rng 1'])
    names = names or sorted(n for n in G.FUNCS if n.startswith('p236l/')) + ['p99/lightbringer_now', 'admin/lightbringer', 'admin/lightbringer_meet', 'p103/fol/wait_lightbringer']
    n = 0
    for name in names:
        out = []
        for l in G.FUNCS[name]:
            if not any(FEM.search(x) for x in _TXT.findall(l)):
                out.append(l); continue
            assert not l.startswith('$') and 'give ' not in l, (name, l)
            m = _TXT.sub(lambda mm: 'text:"' + he(mm.group(1)) + '"', l)
            assert not any(FEM.search(x) for x in _TXT.findall(m)), (name, m)
            when = lambda c, x: f'execute {c} {x[len("execute "):]}' if x.startswith('execute ') else f'execute {c} run {x}'
            out += ['function bm:p236l/mk', when('if score #lhm bm.rng matches 1', m), when('unless score #lhm bm.rng matches 1', l)]
            n += 1
        G.FUNCS[name] = out
    return n

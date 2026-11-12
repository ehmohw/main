"""3.1: THE FERRO - the 60th follower (ferro_pet_art.py; fol5flag.FERRO). A metallic, sheeny black ferrofluid creature: friendly,
cute, a bit terrifying - and it MIMICS: it learns a follower by meeting it once, and turns into a sludgy, oddly cute goo copy of it.

MEETING IT    deep under the deepslate (below y -40, in the dark, standing on deepslate), with KillerWatt and the Ink Blot - or the
              Mireling - out: now and then (every 30 s, 1 in 30; 1 in 15 in the Deep Dark) a SECOND Ink Blot falls in behind yours
              - the Ferro, wearing it. It tails you, three blocks back. Walk up to it: KillerWatt crackles, its spikes BRISTLE out
              of its top - "...that's not mine." - and it melts out of the disguise, rising out of its puddle as itself, with a grin
              a little too wide. Right-click it: the LODESTONE VIAL, and it comes along - KillerWatt and the Ink Blot learned at once.
ITS OWN WAYS  LASH (a foe within 3, every 3 s: a beaded pseudopod whip, 5); SPIKE BURST (a foe within 2, every 8 s: a ring of spikes
              out of the floor round it - 4 to all in 2, knocked up); MAGNETIC PULL (a foe 3-8 off, every 10 s: every spike leans at
              it, field lines string out - yanked 4 blocks in, 1; its lash ready at once); ENGULF (charged, every 20 s: a lumpy goo
              shell closes over one foe - hidden in it, 1 every half second for 2 s - then SPAT 4 blocks for 6; never a boss or a
              player).
MIMICRY       LEARNING: another of your followers within 6 blocks for 3 s - and one you've met yourself - is studied: a puff of beads,
              a word, and the advancement bm:ferro/learned/<kind> (saved by name: the set never renumbers). THE FORMS PAGE (its menu,
              "Forms"): every learned follower; pressed, it turns into it (a 17-tick morph: up, a column, the form filling out of the
              puddle - and back). IN A FORM it follows, idles and fights as that follower's silhouette in black goo, wearing that
              follower's OWN eyes, oil-slick (or its own, on the nine with none to find); it waddles like a goo puppet. Its move is a
              SIMPLIFIED one (bite, slam, shot, spin, kindness or a curse, by who it is), at 60%. A form taller than 3.4 blocks is
              mimicked at 3.4 ("it can't make that much of itself"). Called, sent home or taken back, it comes as itself.
EVERYTHING ELSE is every follower's: sitting (right-click: it melts into a puddle and rises into a little goo armchair it lounges
in; sneak + right-click: it dozes as a puddle, slowly healing), a wardrobe (Quicksilver and Gold Leaf - drawn - Deep Violet, the
metal goos; every form wears them too), a rare aura (Magnetar), a shiny (Oil Slick), the Partner Wheel, a frame (it climbs out;
a right-click bristles its spikes), a display case, Cecil's doll, the honours, a Raid Contract, a Piercing Blow played out on
screen (Spike Tide: a wave of goo across the ground to the monster, spikes bursting up round it, two lashes and an engulf);
pairs with Bender, Mr. Capshun, Henry and Nia."""
import json
import os
from items import item, T, TOTEM
from useitem import hold
from nbt import snbt, F, Int
import fol5
import fol5art
import fol5wire as W5
import rigpet as RP
import rigface as RF2
import phase235 as P235

S5 = fol5.SPEC['ferro']
A0 = fol5art.get('ferro')
FA = A0.FM
COL, LINE = S5['COL'], S5['LINE']
ITEM = S5['item']
FORMS_MENU = 7620                       # (the Forms page: 7621 back to its own shape, 7630 + i the form at FORM_ORDER[i])
FORM0 = 7630
SIDECAR = 'fe_forms.json'               # (the resource pack's measure of every form - F, k, its eyes: the datapack reads it, as metal_looks.json)
# what each mimicked form's move is (the design's MOVES, and every other follower by what it is) - at 60% of these numbers
ARCH = {'bite': 1, 'slam': 2, 'shot': 3, 'spin': 4, 'kind': 5, 'curse': 6}
MOVE_OF = {'bender': 'bite', 'bloo': 'bite', 'bones': 'bite', 'henry': 'bite', 'nia': 'bite', 'stalker': 'bite', 'lantern': 'bite', 'batty': 'bite',
           'mireling': 'bite', 'dragon': 'bite', 'frog': 'bite', 'eggbert': 'bite', 'mimic': 'bite', 'fishy': 'bite', 'rufus': 'shot',
           'dennis': 'slam', 'ashur': 'slam', 'ava': 'slam', 'sovereign': 'slam', 'demo': 'slam', 'knight': 'slam', 'cairn': 'slam', 'cake': 'slam',
           'chef': 'slam', 'neighbor': 'slam', 'ratking': 'curse', 'gem': 'slam', 'zib': 'shot', 'tul': 'shot', 'kw': 'shot', 'speech': 'shot',
           'cursor': 'shot', 'glitch': 'shot', 'pxleo': 'shot', 'pxcecil': 'shot', 'pxemma': 'spin', 'spawner': 'shot', 'kettle': 'shot',
           'capshun': 'shot', 'sapling': 'shot', 'emma': 'spin', 'celi': 'spin', 'leo': 'spin', 'dryad': 'spin', 'don': 'spin', 'wil': 'spin',
           'lightbringer': 'kind', 'keeper': 'kind', 'pearlq': 'kind', 'pistachio': 'kind', 'sky': 'kind', 'pearl': 'kind',
           'inkblot': 'curse', 'omega': 'curse', 'apo': 'curse', 'cecil': 'curse', 'count': 'curse', 'eraser': 'curse', 'vexis': 'curse'}

item(ITEM, TOTEM, 'The Lodestone Vial', COL,
     ['A little glass vial with a black bead inside.', 'Hold it, and the bead stands up in spikes.',
      ('Use: call the Ferro (again: call it over).', 'blue'), ('Sneak + use: its menu - and its Forms.', 'blue'),
      ('A lash, a spike burst, a pull and an engulf - and every friend it has met.', 'blue'), ('If it faints: 2 minutes before it can return.', 'gray'),
      ('"...hello. I\'m you. No - I\'m me. Hello."', 'dark_gray')],
     model=f'bm:{ITEM}', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)

P = A0.POSES
P['sit_a2'] = dict(P['sit_a'], body=FA.T(-4, 0, 2))           # (lounging: the back ripples)
P['sit_b2'] = dict(P['sit_b'], _face='blink')                  # (dozing: a bead surfaces and pops)


class Ferro(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'ferro', 'The Ferro', COL, LINE, 'p271', 'fe', 'fq'
    A = RF2.art(A0)
    MENU, PET_HP, PET_CD, ITEM = 5520, 32, 120, ITEM
    pron, they = 'it', 'it'
    EXPR = RP.Cfg.EXPR + ('grin', 'maw', 'look')
    FACE = dict(A0.FACE_MAP, grin='grin', maw='maw', look='look')
    ATTRS = dict(armor=6, attack_damage=4, movement_speed=0.34, follow_range=32, step_height=1.1)
    SCALE, HIT = 0.6, (0.9, 0.85)                  # (its body, not its arms; 0.75 tall)
    BOX_FIT = True
    BUTTONS = ((6, 'Forms', 'Every follower it has met: press one, and it turns into a goo copy of them - or back into itself.', 'p271/forms/open'),)
    CYCLE = W5.cycle(A0, (240, [(0, 'idle_a'), (80, 'idle_b'), (110, 'idle_a'), (170, 'idle_c'), (210, 'idle_a')]),
                     (160, [(0, 'melt'), (10, 'sit_a'), (80, 'sit_a2'), (100, 'sit_a')]), (None, [(0, 'happy'), (14, 'idle_a')]),
                     {7: (None, [(0, 'lash_up'), (4, 'lash'), (11, 'idle_a')]), 11: (None, [(0, 'burst_up'), (5, 'burst'), (11, 'alert'), (17, 'idle_a')]),
                      8: (None, [(0, 'alert'), (6, 'pull'), (16, 'alert'), (20, 'idle_a')]),
                      12: (None, [(0, 'engulf_up'), (20, 'engulf'), (62, 'spit'), (68, 'idle_a')])}, wp=10, rp_=6)
    DUR = dict(P235._DUR, lash_up=4, lash=2, burst_up=5, burst=2, alert=6, pull=8, engulf_up=20, engulf=4, spit=6, melt=10, sit_a=10, sit_a2=30,
               sit_b=12, sit_b2=30, happy=6, walk_0=5, walk_1=5)
    QUIPS = ['"...hello. I\'m you. No - I\'m me. Hello."', '(its spikes stand up, just for a second, and lie down again)', '"I met a friend of yours. I can be them now. Want to see?"',
             '(a droplet falls off it, and rolls back in)', '"Iron! Iron somewhere. Mm."', '(its eyes slide sideways, and back)']
    HELLO = ('(the Ferro pours itself back to you, beading as it comes)', '(a puddle of mirror-black goo rises into a little gumdrop - and grins) "...hello."',
             '(it melts into a puddle, the puddle into a bead - and it\'s gone)')
    SIT = ('"Up! The goo is up!"', '(it melts into a puddle - and rises into a little goo armchair, and lounges in it)')
    FAINT = '"...I\'m... I\'m just a puddle..."'
    NOT_YOURS = '(its spikes stand up all at once) "...you\'re not mine."'
    POWERS = [('Lash', 'a foe within 3, every 3 s: a beaded pseudopod whip, a star of spikes at its tip - 5'),
              ('Spike Burst', 'a foe within 2, every 8 s: a ring of spikes out of the floor round it - 4 to all within 2, knocked up'),
              ('Magnetic Pull', 'a foe 3-8 off, every 10 s: every spike leans at it - yanked 4 blocks in, 1, and the lash ready'),
              ('Engulf', 'charged, every 20 s: a goo shell closes over one foe - 1 every half second for 2 s - then spat 4 blocks for 6 (never a boss)'),
              ('Mimicry', 'another of your followers within 6 for 3 s is learned for good; its menu\'s Forms turn it into any of them - with their own eyes, oil-slick, and a move of theirs at 60%')]
    INTRO = [T('The Ferro', COL, bold=True), T(' - a ferrofluid thing from under the deepslate that answers to a magnet, and to you. ', 'gray'),
             T('"...hello. I\'m you."', LINE, italic=True)]
    BURST = ['particle minecraft:dust{color:[0.06,0.06,0.1],scale:1.4} ~ ~0.5 ~ 0.4 0.3 0.4 0 20', 'particle minecraft:electric_spark ~ ~0.8 ~ 0.3 0.3 0.3 0.02 6']
    FADE_SOUND = 'playsound minecraft:block.honey_block.slide neutral @a[distance=..20] ~ ~ ~ 1 0.6'
    SUMMON_EXTRA = ['playsound minecraft:entity.slime.squish neutral @a[distance=..24] ~ ~ ~ 0.8 0.7', 'playsound minecraft:block.respawn_anchor.charge neutral @a[distance=..24] ~ ~ ~ 0.4 1.6']
    ENC_POSES = [(0, 'idle_a'), (30, 'grin'), (50, 'idle_c'), (66, 'idle_a')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 30 run particle minecraft:dust{color:[0.06,0.06,0.1],scale:1.0} ~ ~0.3 ~ 0.3 0.1 0.3 0 4'
    ADV = ('That\'s Not Mine', 'Deep under the deepslate with KillerWatt and the Ink Blot out - meet the Ink Blot that isn\'t')
    ADMIN_HINT = 'Below y -40, in the dark on deepslate, with KillerWatt and the Ink Blot (or the Mireling) out (admin/ferro_meet_here: now).'
    MEET_HINT = 'Walk up to the Ink Blot that isn\'t yours; then right-click it.'


_DOLL = 'A doll of the Ferro - a glossy black gumdrop with two big oil-slick eyes, a little too cute.'
_eff = W5.pair_fx
_PAIRS = {
    'fe_bender': ('ferro', 'bender', 'Who\'s a Good Goo?', '#e0a860', 'The Ferro and Bender - it turns into a goo Bender, and they chase each other\'s tails',
                  _eff(('speed', 0), ('strength', 0)),
                  [('bender', '(barks at it. It barks back - in Bender\'s voice, slightly wet.)'), ('ferro', '(a goo Bender, wagging a goo tail) "...woof?"')],
                  [('ferro', '(it chases its own tail, as Bender does)', 'bender', '(chases it right back, delighted)')]),
    'fe_capshun': ('ferro', 'capshun', 'Life Drawing', '#f0f0f0', 'The Ferro and Mr. Capshun - he draws a friend on his page, and it becomes the drawing',
                   _eff(('haste', 0), ('luck', 0)),
                   [('capshun', '[Mr. Capshun narrates: "Hold still. You\'re a... what ARE you?"]'), ('ferro', '(it becomes the drawing. Slightly smudged.)')],
                   [('ferro', '(it holds a pose for him, very still)', 'capshun', '[Mr. Capshun narrates: "Paint slides off chrome. He drew instead."]')]),
}
W5.register(Ferro, A0, _DOLL, ('minecraft:end_rod', 'minecraft:entity.slime.squish', 'minecraft:poof'), _PAIRS, 'the Ferro')

# ---- its Piercing Blow, on screen (never a vanish - the owner's rule): SPIKE TIDE - it pours itself across the ground to the monster
#      as a wave of goo (its own melt pose, eased - an on-screen dash), its spikes burst up round it, it lashes it twice and engulfs it
import phase226 as _P226  # noqa: E402
_P226.ASSAULT['ferro'] = dict(pfx='p271', s_obj='bm.fqs', anim='p271/anim', busy='bm.fqx', end=34, dash=dict(reach=1.5, speed=0.9, lift=0), free=True,
                              hits={1: (4, ['particle minecraft:dust{color:[0.06,0.06,0.1],scale:1.4} ~ ~0.2 ~ 0.6 0.1 0.6 0 20', 'particle minecraft:crit ~ ~0.6 ~ 0.5 0.3 0.5 0.3 12',
                                            'effect give @s minecraft:slowness 2 3 true'], 'minecraft:block.pointed_dripstone.land', 0.6),
                                    2: (3, ['particle minecraft:sweep_attack ~ ~1 ~ 0.2 0.1 0.2 0 1', 'particle minecraft:crit ~ ~1 ~ 0.3 0.3 0.3 0.3 8'], 'minecraft:entity.player.attack.sweep', 1.6),
                                    3: (4, ['particle minecraft:dust{color:[0.06,0.06,0.1],scale:1.6} ~ ~1 ~ 0.4 0.5 0.4 0 24', 'particle minecraft:electric_spark ~ ~1 ~ 0.3 0.4 0.3 0.05 10'],
                                        'minecraft:entity.slime.squish', 0.6)},
                              tl={1: ['P melt', 'S minecraft:block.honey_block.slide 1 0.6'], 3: ['DASH'], 10: ['P burst_up'], 12: ['P burst', 'H1'],
                                  16: ['P lash_up'], 18: ['P lash', 'H2'], 20: ['P lash_up'], 22: ['P lash', 'H2'],
                                  24: ['P engulf_up', 'S minecraft:entity.slime.squish 1 0.5'], 27: ['P spit', 'H3'], 31: ['P idle_a']})
_P226.NAMES['ferro'] = ('Spike Tide', 'pours itself across the ground at the monster as a wave of goo, bursts its spikes up round it, lashes it twice and engulfs it')


def extend_offers(O, offer):
    pass


def generate_early(G):
    RP.contract(Ferro, G)


# ---------------------------------------------------------------------------------------------------- the resource pack: its forms
def _icon(spiky=False):
    """The Lodestone Vial: a little glass vial, a black bead inside (standing up in spikes, in a frame's bristle)"""
    from sprites280 import S
    s = S()
    pal = {'g': '#c8d8e8', 'w': '#ffffff', 'k': '#0a0a12', 'v': '#4a3a9a', 'c': '#8a6a3a'}
    s.g(['...cccc...', '...gwwg...', '..g....g..', '..g....g..', '..g.kk.g..', '..gkvvkg..', '..gkkkkg..', '..g.kk.g..', '...gggg...'], pal, 3, 3)
    if spiky:
        s.g(['.k..k..k.', '..k.k.k..'], pal, 3, 5)
    return s.render()


def figure_items():
    """the figures a form is made of: every follower's display-case figure (phase134), by its item - not the Ferro's own, nor a doll's source"""
    import phase134 as P134
    return {iid: parts for iid, (_nm, parts) in P134.figures().items() if iid not in P134.BAKE_ONLY and iid != ITEM}


def rp(R):
    W5.rp(Ferro, R, _icon(), A0)
    R.ICONS[f'{ITEM}_f1'] = _icon(True)

    def late(R2):
        R2.POST.append(_forms)            # (after every other hook: the forms are made of everyone's finished models)
    R.POST.append(late)


def _forms(R2):
    """every follower's ferro form (ferro_form: one merged model, its sheen projected, softened, dripping, in a puddle; its own eyes
    in oil-slick), a colour of every look (a parent model on the look's copy of the shared set - p138 recoloured them), the eyes'
    mood definitions - and the sidecar the datapack reads (F, k, the eyes, its box)"""
    import phase99 as P99
    import shiny as SH
    rp_root = R2.p()
    looks = sorted(P99.NEW['ferro'][3])
    shk = SH.KEY.get('ferro')
    PAL_OF = {1: '_qs', 2: '_au', shk: '_sh'}
    side = {}
    mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
    tdir = R2.p('assets', 'bm', 'textures', 'block')
    for iid, parts in sorted(figure_items().items()):
        key = iid
        try:
            model, extra, info = FA.ferro_form(rp_root, parts, key)
        except Exception as e:                                 # (a figure it can't read - say so in the build, carry on)
            print(f'ferro: no form for {iid}: {e!r}')
            continue
        R2.wj(f'assets/bm/models/item/fm_{key}.json', model)
        R2.wj(f'assets/bm/items/fm_{key}.json', {'model': mdl(f'fm_{key}')})
        for nm, im in extra.items():
            im.save(os.path.join(tdir, f'{nm}.png'))
        for k in looks:
            R2.wj(f'assets/bm/models/item/fm_{key}_c{k}.json', {'parent': f'bm:item/fm_{key}',
                                                              'textures': {t: f'bm:block/fe_{t}_c{k}' for t in ('sx', 'sxd', 'up', 'dn')} | {'particle': f'bm:block/fe_sx_c{k}'}})
            R2.wj(f'assets/bm/items/fm_{key}_c{k}.json', {'model': mdl(f'fm_{key}_c{k}')})
        em = info.pop('eye_models', {})
        for n, m in em.items():
            R2.wj(f'assets/bm/models/item/{n}.json', m)
        if em:                                                 # (its eyes' mood definitions, in every look: the Ferro's moods -> its own faces)
            for k in [0] + looks:
                ps = PAL_OF.get(k, '')
                nm = lambda face: f'fm_{key}_eyes' + (f'_x{face}' if face else '') + ps
                base = nm('') if nm('') in em or not ps else f'fm_{key}_eyes'
                cases = []
                for e in Ferro.EXPR:
                    f2 = FA.form_face(info, Ferro.FACE.get(e) or e)
                    if f2 and nm(f2) in em:
                        cases.append({'when': e, 'model': mdl(nm(f2))})
                R2.wj(f'assets/bm/items/fm_{key}_eyes' + (f'_c{k}' if k else '') + '.json',
                      {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0, 'cases': cases, 'fallback': mdl(base)}})
        side[iid] = {kk: info[kk] for kk in ('F', 'k', 'eyes', 'eye_w', 'own_eyes', 'height', 'n')}
    json.dump(side, open(os.path.join(os.path.dirname(rp_root.rstrip('/')), SIDECAR), 'w'), indent=0)
    print(f'ferro: {len(side)} forms')


def textures():
    return A0.textures()


# ---------------------------------------------------------------------------------------------------- its ways
BIG = 'tag=!bm.boss,type=!minecraft:ender_dragon,type=!minecraft:wither,type=!minecraft:warden,type=!minecraft:elder_guardian,type=!minecraft:ravager'


def _abilities(G, X):
    fn, pfx, foe, S = G.fn, X.pfx, X.foe, X.S
    snd = lambda s, v=0.6, p=1.0: f'playsound minecraft:{s} neutral @a[distance=..16] ~ ~ ~ {v} {p}'
    K = dict(melee=dict(st=7, x=12, at=7, cd=60, reach=3.0, face='serious', go=[snd('entity.slime.jump', 0.6, 0.6)]),
             crowd=dict(st=11, x=17, at=11, cd=160, r=2.4, n=1, face='maw', go=[snd('block.pointed_dripstone.land', 0.8, 0.6)]),
             ranged=dict(st=8, x=20, at=13, cd=200, near=3, far=8, face='surprised', go=[snd('block.respawn_anchor.charge', 0.6, 1.6)]),
             charged=dict(st=12, x=68, at=[48, 6], cd=400, r=3, face='maw', go=[snd('entity.slime.squish', 1.0, 0.5)]))
    lines = P235.kit(G, X, K)
    G.FUNCS.pop(f'{pfx}/near_owner', None)
    inform = lambda ev: f'execute if entity @s[tag=bm.fexf] run return run function bm:p271/arch/go'
    # LASH: 5 to the first foe within 3
    fn(f'{pfx}/melee', [inform('melee')] + X.hit(5) + [f'execute as @e[{foe},distance=..3.4,sort=nearest,limit=1] at @s run function bm:{pfx}/lashed'] + X.end)
    fn(f'{pfx}/lashed', [f'function bm:{pfx}/hurt', 'particle minecraft:crit ~ ~0.8 ~ 0.3 0.3 0.3 0.2 8', snd('entity.player.attack.sweep', 0.6, 1.6)])
    # SPIKE BURST: 4 to every foe within 2, knocked up
    fn(f'{pfx}/crowd', [inform('crowd')] + X.hit(4) + [f'execute as @e[{foe},distance=..2.4] at @s run function bm:{pfx}/spiked',
                                                       'particle minecraft:dust{color:[0.06,0.06,0.1],scale:1.4} ~ ~0.2 ~ 1.0 0.1 1.0 0 30'] + X.end)
    fn(f'{pfx}/spiked', [f'function bm:{pfx}/hurt', 'data modify entity @s Motion[1] set value 0.4d', 'particle minecraft:crit ~ ~0.4 ~ 0.3 0.2 0.3 0.3 8'])
    # MAGNETIC PULL: a foe 3-8 off yanked 4 blocks in, 1 - its lash ready at once
    fn(f'{pfx}/ranged', [inform('ranged')] + X.hit(1) + [f'execute as @e[{foe},distance=..8.5,sort=nearest,limit=1] at @s facing entity @e[type=minecraft:wolf,tag=bm.feme,limit=1] feet run function bm:{pfx}/pulled',
                                                         f'scoreboard players set @s {S("mc")} 0'] + X.end)
    fn(f'{pfx}/pulled', [f'function bm:{pfx}/hurt', 'tp @s ^ ^ ^2', 'execute at @s if block ^ ^ ^2 #bm:grap_pass run tp @s ^ ^ ^2',
                         'particle minecraft:electric_spark ~ ~1 ~ 0.3 0.4 0.3 0.05 12'])
    # ENGULF: the nearest foe within 3 (not a boss) inside, hidden and still - 1 every half second - then spat 4 blocks for 6
    fn(f'{pfx}/charged', [inform('charged'), 'tag @s add bm.fegp', f'execute as @e[{foe},{BIG},distance=..3.4,sort=nearest,limit=1] at @s run function bm:{pfx}/gulped',
                          'tag @s remove bm.fegp', snd('entity.slime.squish', 1.0, 0.4)])
    fn(f'{pfx}/gulped', ['tag @s add bm.fein', 'scoreboard players set @s bm.fqin 48', 'tag @s remove bm.fenoai', 'execute if data entity @s {NoAI:1b} run tag @s add bm.fenoai',
                         'data merge entity @s {NoAI:1b}', 'effect give @s minecraft:invisibility 3 0 true', 'tp @s @e[type=minecraft:wolf,tag=bm.fegp,limit=1]'])
    fn(f'{pfx}/charged2', X.hit(6) + [f'execute as @e[tag=bm.fein,distance=..4,limit=1] at @s run function bm:{pfx}/spat',
                                      'particle minecraft:dust{color:[0.06,0.06,0.1],scale:1.2} ^ ^0.5 ^1 0.6 0.3 0.6 0 30'] + X.end)
    fn(f'{pfx}/spat', [f'function bm:{pfx}/release', 'execute at @e[type=minecraft:wolf,tag=bm.feme,limit=1] positioned ^ ^0.3 ^4 if block ~ ~ ~ #minecraft:air run tp @s ~ ~ ~',
                       'execute at @s run function bm:p271/hurt_here'])
    fn('p271/hurt_here', [f'function bm:{pfx}/hurt'])
    fn(f'{pfx}/release', ['tag @s remove bm.fein', 'scoreboard players reset @s bm.fqin', 'execute unless entity @s[tag=bm.fenoai] run data merge entity @s {NoAI:0b}',
                          'tag @s remove bm.fenoai', 'effect clear @s minecraft:invisibility'])
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.fqin dummy']
    G.OBJECTIVES += ['bm.fqin']
    X.tick += ['execute as @e[tag=bm.fein] at @s run function bm:p271/held']
    fn('p271/held', ['scoreboard players remove @s bm.fqin 1', 'execute if score @s bm.fqin matches ..0 run return run function bm:p271/release',
                     'execute unless entity @e[type=minecraft:wolf,tag=bm.fepet,distance=..6] run return run function bm:p271/release',
                     'execute store result score #q bm.rng run scoreboard players get @s bm.fqin', 'scoreboard players operation #q bm.rng %= #10 bm.rng',
                     'execute if score #q bm.rng matches 0 run damage @s 1 minecraft:generic',
                     'execute at @e[type=minecraft:wolf,tag=bm.fepet,distance=..6,sort=nearest,limit=1] run tp @s ~ ~0.1 ~'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #10 bm.rng 10']
    # IN A FORM: its move is the form's (an archetype, 60%): bite, slam, shot, spin, kindness, a curse
    fn('p271/arch/go', [f'execute if score @s bm.fqa matches {n} run return run function bm:p271/arch/{a}' for a, n in ARCH.items()] + ['function bm:p271/arch/bite'])
    fn('p271/arch/bite', X.hit(3) + [f'execute as @e[{foe},distance=..3,sort=nearest,limit=1] at @s run function bm:{pfx}/hurt', 'function bm:p271/fm/squash',
                                     'particle minecraft:dust{color:[0.06,0.06,0.1],scale:1.0} ^ ^0.6 ^1 0.2 0.2 0.2 0 8', snd('entity.fox.bite', 0.6, 0.8)] + X.end)
    fn('p271/arch/slam', X.hit(2) + [f'execute as @e[{foe},distance=..2.6] at @s run function bm:{pfx}/hurt', 'function bm:p271/fm/squash',
                                     'particle minecraft:dust{color:[0.06,0.06,0.1],scale:1.4} ~ ~0.1 ~ 1.0 0.05 1.0 0 24', snd('entity.generic.big_fall', 0.8, 0.6)] + X.end)
    fn('p271/arch/shot', X.hit(3) + [f'execute as @e[{foe},distance=..8.5,sort=nearest,limit=1] at @s run function bm:p271/arch/shot_hit', 'function bm:p271/fm/squash',
                                     snd('entity.slime.jump', 0.8, 1.4)] + X.end)
    fn('p271/arch/shot_hit', [f'function bm:{pfx}/hurt', 'particle minecraft:dust{color:[0.06,0.06,0.1],scale:1.2} ~ ~1 ~ 0.3 0.3 0.3 0 14'])
    fn('p271/arch/spin', X.hit(2) + [f'execute as @e[{foe},distance=..2.4] at @s run function bm:{pfx}/hurt', 'function bm:p271/fm/squash',
                                     'particle minecraft:dust{color:[0.06,0.06,0.1],scale:1.0} ~ ~0.6 ~ 1.0 0.3 1.0 0 30', snd('entity.player.attack.sweep', 0.8, 0.7)] + X.end)
    fn('p271/arch/kind', ['execute on owner run effect give @s minecraft:regeneration 3 0 true', 'function bm:p271/fm/squash',
                          'particle minecraft:heart ~ ~1 ~ 0.3 0.3 0.3 0 2', snd('entity.slime.squish_small', 0.8, 1.4)])
    fn('p271/arch/curse', [f'execute as @e[{foe},distance=..6,sort=nearest,limit=1] at @s run function bm:p271/arch/cursed', 'function bm:p271/fm/squash', snd('entity.slime.squish', 0.6, 0.5)])
    fn('p271/arch/cursed', ['effect give @s minecraft:weakness 3 0', 'effect give @s minecraft:slowness 2 0', 'particle minecraft:dust{color:[0.2,0.1,0.35],scale:1.2} ~ ~1.2 ~ 0.3 0.4 0.3 0 14'])
    return lines


def _encounter(G, X):
    """under the deepslate, in the dark, with KillerWatt and the Ink Blot (or the Mireling) out: the Ink Blot that isn't"""
    import phase125 as P125
    fn, tellraw, title = G.fn, G.tellraw, G.title
    host = lambda w: f'@e[type=minecraft:{P125.WHO[w][3]},tag={P125.WHO[w][4]},distance=..16]'
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.fqe dummy', 'scoreboard objectives add bm.fqet dummy']
    G.OBJECTIVES += ['bm.fqe', 'bm.fqet']
    G.wjson('bm/predicate/p271/dark.json', {'condition': 'minecraft:location_check', 'predicate': {'light': {'light': {'max': 0}}}})
    G.wjson('bm/predicate/p271/deep_dark.json', {'condition': 'minecraft:location_check', 'predicate': {'biomes': 'minecraft:deep_dark'}})
    G.wjson('bm/tags/block/p271_deepslate.json', {'values': ['minecraft:deepslate', 'minecraft:cobbled_deepslate', 'minecraft:polished_deepslate', 'minecraft:deepslate_bricks',
                                                              'minecraft:deepslate_tiles', 'minecraft:chiseled_deepslate', 'minecraft:cracked_deepslate_bricks',
                                                              'minecraft:cracked_deepslate_tiles', 'minecraft:sculk', 'minecraft:deepslate_iron_ore',
                                                              'minecraft:deepslate_coal_ore', 'minecraft:deepslate_copper_ore', 'minecraft:deepslate_gold_ore',
                                                              'minecraft:deepslate_redstone_ore', 'minecraft:deepslate_lapis_ore', 'minecraft:deepslate_diamond_ore',
                                                              'minecraft:deepslate_emerald_ore', 'minecraft:tuff', 'minecraft:reinforced_deepslate']})
    X.second.append('execute as @a[tag=!bm.femet,gamemode=!spectator] at @s if dimension minecraft:overworld if entity @s[y=-64,dy=23] run function bm:p271/enc/q')
    fn('p271/enc/q', ['scoreboard players add @s bm.fqet 1', 'execute unless score @s bm.fqet matches 30.. run return 0', 'scoreboard players set @s bm.fqet 0',
                      'execute unless block ~ ~-1 ~ #bm:p271_deepslate run return 0', 'execute unless predicate bm:p271/dark run return 0',
                      'execute if entity @e[type=minecraft:interaction,tag=bm.feenc,distance=..48] run return 0',
                      'execute unless score @s bm.pid matches 1.. run return 0', 'scoreboard players operation #me bm.pid = @s bm.pid',
                      'scoreboard players set #tr bm.rng 0', f'execute as {host("kw")} if score @s bm.pid = #me bm.pid run scoreboard players add #tr bm.rng 1',
                      'scoreboard players set #ti bm.rng 0', f'execute as {host("inkblot")} if score @s bm.pid = #me bm.pid run scoreboard players set #ti bm.rng 1',
                      f'execute as {host("mireling")} if score @s bm.pid = #me bm.pid run scoreboard players set #ti bm.rng 1',
                      'scoreboard players operation #tr bm.rng += #ti bm.rng', 'execute unless score #tr bm.rng matches 2.. run return 0',
                      'execute store result score #r bm.rng run random value 1..30',
                      'execute if predicate bm:p271/deep_dark if score #r bm.rng matches 16.. run scoreboard players remove #r bm.rng 15',
                      'execute unless score #r bm.rng matches 1 run return 0', 'function bm:p271/enc/arrive'])
    # (it falls in behind you: the Ferro's rig, wearing the Ink Blot - a FORM display over it, the rig hidden; three blocks back)
    fn('p271/enc/arrive', ['execute rotated ~ 0 positioned ^ ^ ^-3 run function bm:p271/enc/spawn',
                           'scoreboard players operation @e[type=minecraft:interaction,tag=bm.feenc,distance=..5] bm.pid = @s bm.pid',
                           'scoreboard players set @e[type=minecraft:interaction,tag=bm.feenc,distance=..5] bm.fqe 1',
                           'execute as @e[type=minecraft:interaction,tag=bm.feenc,distance=..5,limit=1] at @s run function bm:p271/enc/disguise',
                           'playsound minecraft:entity.slime.squish_small neutral @s ~ ~ ~ 0.4 0.8'])
    fn('admin/ferro_meet_here', ['function bm:p271/enc/arrive'])
    fn('p271/enc/disguise', ['execute as @e[type=minecraft:item_display,tag=bm.feencp,distance=..3] run data merge entity @s {transformation:{scale:[0f,0f,0f]}}',
                             'function bm:p271/fm/enc_form'])
    # (each tick, while disguised: it tails you three blocks back; walk up to it - KillerWatt crackles, it bristles, melts out of it)
    G.FUNCS['p271/enc/tick'].insert(0, 'execute if score @s bm.fqe matches 1 run return run function bm:p271/enc/tail')
    fn('p271/enc/tail', ['execute if entity @p[distance=..3.2,gamemode=!spectator] run return run function bm:p271/enc/reveal',
                         'scoreboard players add @s bm.fqet 1', 'execute if score @s bm.fqet matches 800.. run return run function bm:p271/enc/reveal',
                         'scoreboard players operation #f bm.rng = @s bm.fqet', 'scoreboard players operation #f bm.rng %= #10 bm.rng',
                         'execute if score #f bm.rng matches 0 if entity @p[distance=4.5..16,gamemode=!spectator] facing entity @p[gamemode=!spectator] feet rotated ~ 0 positioned ^ ^ ^0.6 '
                         'if block ~ ~ ~ #bm:grap_pass run function bm:p271/enc/step'])
    fn('p271/enc/step', ['tp @e[type=minecraft:interaction,tag=bm.feenc,distance=..1,limit=1,sort=nearest] ~ ~ ~ ~ 0',
                         'execute as @e[type=minecraft:item_display,tag=bm.feencf,distance=..2] run tp @s ~ ~ ~ ~ 0',
                         'execute as @e[type=minecraft:item_display,tag=bm.feencp,distance=..3] run tp @s ~ ~ ~ ~ 0'])      # (its hidden rig comes too)
    fn('p271/enc/reveal', ['scoreboard players set @s bm.fqe 2', 'playsound minecraft:entity.creeper.primed neutral @a[distance=..16] ~ ~ ~ 0.4 2.0',
                           'particle minecraft:electric_spark ~ ~1 ~ 0.4 0.5 0.4 0.1 30', 'particle minecraft:dust{color:[0.06,0.06,0.1],scale:1.6} ~ ~0.4 ~ 0.5 0.3 0.5 0 40',
                           tellraw('@a[distance=..16]', [T('KillerWatt crackles - and the Ink Blot behind you BRISTLES, spikes standing out of its top. ', '#c8d8ff', italic=True),
                                                         T('The Ink Blot: ', '#3a3aa0', bold=True), T('"...that\'s not mine."', '#a0a0ff')]),
                           'kill @e[type=minecraft:item_display,tag=bm.feencf,distance=..3]', 'playsound minecraft:block.honey_block.slide neutral @a[distance=..16] ~ ~ ~ 1 0.6',
                           'execute as @e[type=minecraft:item_display,tag=bm.feencp,distance=..3] run tag @s add bm.fesel', 'execute rotated as @s run function bm:p271/place',
                           'function bm:p271/pose/grin',
                           'tag @e[tag=bm.fesel] remove bm.fesel',
                           tellraw('@a[distance=..16]', [T('It melts out of the disguise and rises out of its puddle as itself - a glossy black gumdrop, ', LINE, italic=True),
                                                         T('with a grin a little too wide. "...hello."', 'gray', italic=True)])])
    csay = lambda txt: title('@s', 'actionbar', [T('The Ferro: ', COL, bold=True), T(txt, LINE)])
    fn('p271/enc/talk', [f'execute unless score @s bm.pid = {X.here} bm.pid run return run ' + csay('"...you\'re not mine."'),
                         f'execute if score {X.here} bm.fqe matches 1 run return run function bm:p271/enc/reveal_here',
                         'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.4',
                         tellraw('@s', [T('It flows up your arm, cold and tickly, and leaves a little glass vial in your hand - a black bead inside it. ', LINE, italic=True),
                                        T('"I met your friends. I can be them now. Want to see?"', 'gray', italic=True)]),
                         'function bm:p271/enc/joined', 'function bm:p271/learn/i_kw', 'function bm:p271/learn/i_inkblot'])
    fn('p271/enc/reveal_here', [f'execute as {X.here} at @s run function bm:p271/enc/reveal'])


# ---------------------------------------------------------------------------------------------------- MIMICRY
def _forms_dp(G, X):
    """the datapack's half: the form table in storage, learning, the Forms page, the morph and the form's motion"""
    import phase125 as P125
    import phase179 as P179
    import phase220 as P220
    fn, title, tellraw = G.fn, G.title, G.tellraw
    pfx, ab = Ferro.pfx, Ferro.ab
    csay = lambda txt: title('@s', 'actionbar', [T('The Ferro: ', COL, bold=True), T(txt, LINE)])
    # ---- which follower is which form: FORM_ORDER is phase179.SLOTS (append-only - a world remembers its form by number)
    item_of = {}
    for w, (nm, pron, col, host, tag, try_, home) in P125.WHO.items():
        e = P179.FOLLOW.get(tag.split(',')[0])
        item_of[w] = e[3] if e else ('wilfrey_locket' if w == 'wil' else None)
    figs = figure_items()
    order = [w for w in P179.SLOTS if w != 'ferro' and w in P125.WHO and item_of.get(w) in figs]
    side_p = os.path.join(G.OUTROOT, SIDECAR)
    side = json.load(open(side_p)) if os.path.exists(side_p) else {}
    if not side:
        print(f'ferro: no {side_p} yet (build the resource pack first) - its forms take their figures\' own sizes')
    import phase134 as P134
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.fqf dummy', 'scoreboard objectives add bm.fqa dummy', 'scoreboard objectives add bm.fqm dummy',
                              'scoreboard objectives add bm.fqk dummy', 'scoreboard objectives add bm.fqlk dummy', 'scoreboard objectives add bm.fqn dummy', 'scoreboard objectives add bm.fqo dummy']
    G.OBJECTIVES += ['bm.fqf', 'bm.fqa', 'bm.fqm', 'bm.fqk', 'bm.fqlk', 'bm.fqn', 'bm.fqo']
    table = []
    for i, w in enumerate(order, 1):
        iid = item_of[w]
        inf = side.get(iid, {})
        lo, h, x0, x1, z0, z1 = P134.FIT.get(iid, (0.0, 1.5, -0.4, 0.4, -0.4, 0.4))
        k = inf.get('k', FA.MIMIC_K)
        Fd = round(inf.get('F', 1.0) * k, 4)
        hh = round(min(FA.CAP_H, max(0.6, (inf.get('height') or h) * k)), 2)
        ww = round(max(0.6, min(3.0, max(x1 - x0, z1 - z0) * k * 0.85)), 2)
        own = 1 if inf.get('own_eyes') else 0
        if own:
            te = None
        else:
            pos, ek = FA.eyes_xf(inf, k=k) if inf.get('eyes') else ((0.0, hh * 0.8, 0.25), 0.6)
            te = (pos, ek)
        tr = lambda sx, sy, sz, rz=0.0: snbt({'left_rotation': [F(0), F(0), F(round(__import__('math').sin(__import__('math').radians(rz) / 2), 5)),
                                                                F(round(__import__('math').cos(__import__('math').radians(rz) / 2), 5))],
                                              'right_rotation': [F(0), F(0), F(0), F(1)], 'translation': [F(0), F(round(1.5 * Fd * sy, 4)), F(0)],
                                              'scale': [F(round(Fd * sx, 4)), F(round(Fd * sy, 4)), F(round(Fd * sz, 4))]})
        ent = (f'{{i:{i},m:"fm_{iid}",own:{own},a:{ARCH[MOVE_OF.get(w, "bite")]},w:{ww}f,h:{hh}f,'
               f'k0:{tr(1, 1, 1)},t1:{tr(1.04, 0.96, 1.04, 6)},k2:{tr(1.04, 0.96, 1.04, -6)},k3:{tr(1.12, 0.78, 1.12)},k4:{tr(1.15, 0.5, 1.15)},k5:{tr(1.15, 0.22, 1.15)},'
               f'kz:{tr(0.01, 0.01, 0.01)}' +
               (f',e:{snbt({"left_rotation": [F(0), F(0), F(0), F(1)], "right_rotation": [F(0), F(0), F(0), F(1)], "translation": [F(round(te[0][0], 4)), F(round(te[0][1], 4)), F(round(te[0][2], 4))], "scale": [F(round(te[1], 4))] * 3})}' if te else '') + '}')
        table.append(f'data modify storage bm:fe f{i} set value {ent}')
    fn('p271/fm/table', table)
    G.FUNCS['load'][-1:-1] = ['function bm:p271/fm/table']
    # ---- LEARNING: another of your followers within 6 for 3 s (one you've met) - for good, as an advancement
    for i, w in enumerate(order, 1):
        G.wjson(f'bm/advancement/ferro/learned/{w}.json', {'criteria': {'learned': {'trigger': 'minecraft:impossible'}}})
        met = f'bm:met/{P220.MET_KEY.get(w, w)}'
        fn(f'p271/learn/i_{w}', [f'execute if entity @s[advancements={{bm:ferro/learned/{w}=true}}] run return 0',
                                 f'execute unless entity @s[advancements={{{met}=true}}] run return 0', f'advancement grant @s only bm:ferro/learned/{w}',
                                 tellraw('@s', [T('The Ferro: ', COL, bold=True), T(f'(a puff of beads) "...I can be {P125.WHO[w][0]} now. Want to see?" ', LINE),
                                                T('(Its menu - Forms.)', 'dark_gray')])])
    X.second.append('execute as @e[type=minecraft:wolf,tag=bm.fepet,tag=!bm.ffpet,tag=!bm.fexf] at @s run function bm:p271/study')
    # (3.1z: the follower it's studying is bm.fqlk - it was bm.fqk, which its tick counts down as a move's cooldown, so the study
    #  reset every second and MIMICRY never learned anyone. And only a follower its owner has met and it hasn't learned yet: the first
    #  in the list within 6 won, so a learned one beside it kept it from learning anyone after it. Its own owner tag, bm.festu)
    fn('p271/study', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #k bm.rng 0', 'execute on owner run tag @s add bm.festu'] +
       [f'execute if score #k bm.rng matches 0 if entity @a[tag=bm.festu,advancements={{bm:ferro/learned/{w}=false,bm:met/{P220.MET_KEY.get(w, w)}=true}}] '
        f'as @e[type=minecraft:{P125.WHO[w][3]},tag={P125.WHO[w][4]},tag=!bm.ffpet,distance=..6] if score @s bm.pid = #me bm.pid run scoreboard players set #k bm.rng {i}'
        for i, w in enumerate(order, 1)] +
       ['tag @a[tag=bm.festu] remove bm.festu',
        'execute if score #k bm.rng matches 0 run return run scoreboard players set @s bm.fqn 0',
        'execute unless score @s bm.fqlk = #k bm.rng run scoreboard players set @s bm.fqn 0', 'scoreboard players operation @s bm.fqlk = #k bm.rng',
        'scoreboard players add @s bm.fqn 1', 'execute if score @s bm.fqn matches 3 run function bm:p271/studied'])
    fn('p271/studied', ['particle minecraft:dust{color:[0.06,0.06,0.1],scale:1.0} ~ ~0.8 ~ 0.4 0.4 0.4 0 20', 'playsound minecraft:entity.slime.squish_small neutral @a[distance=..12] ~ ~ ~ 0.6 1.4'] +
       [f'execute if score #k bm.rng matches {i} on owner run function bm:p271/learn/i_{w}' for i, w in enumerate(order, 1)])
    # ---- THE FORMS PAGE (its menu's "Forms"): the forms you've taught it; pressed, the owner's choice (bm.fqo, kept), the host follows
    from phase28 import btn, multi, body
    import phase28 as P28
    b_self = btn([T('◆ ', '#7a6aff'), T('Its own shape', COL, bold=True)], FORMS_MENU + 1, width=150, tooltip=T('Back into a glossy black gumdrop.', 'gray'))
    page = multi([T('The Ferro', COL, bold=True), T('  »  ', 'dark_gray'), T('Forms', LINE, bold=True)],
                 [body([T('Every friend of yours it has met: press one, and it turns into a goo copy of them - with their own eyes, oil-slick.', 'gray')], 300)], '@@ACTS@@', columns=3)
    fn('p271/forms/show', ['$dialog show @s ' + snbt(page).replace('"@@ACTS@@"', '$(acts)')])
    fn('p271/forms/open', [f'scoreboard players set @s bm.menu {FORMS_MENU}', 'data modify storage bm:tmp fe.acts set value []',
                           f'data modify storage bm:tmp fe.acts append value {snbt(b_self)}'] +
       [f'execute if entity @s[advancements={{bm:ferro/learned/{w}=true}}] run data modify storage bm:tmp fe.acts append value '
        f'{snbt(btn(T(P125.WHO[w][0][0].upper() + P125.WHO[w][0][1:], P125.WHO[w][2]), FORM0 + i, width=150, tooltip=T("Turn into them.", "gray")))}'
        for i, w in enumerate(order, 1)] +
       ['function bm:p271/forms/show with storage bm:tmp fe', 'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 0.8 1.4'])
    assert FORM0 + len(order) < 7710, len(order)
    G.FUNCS['p28/act'] += [f'execute if score #act bm.pay matches {FORMS_MENU + 1} run return run function bm:p271/forms/act',
                           f'execute if score #act bm.pay matches {FORM0 + 1}..{FORM0 + len(order)} run return run function bm:p271/forms/act']
    fn('p271/forms/act', [f'execute unless score @s bm.menu matches {FORMS_MENU} run return run function bm:p28/stale',
                          f'execute if score #act bm.pay matches {FORMS_MENU + 1} run return run function bm:p271/forms/pick0'] +
       [f'execute if score #act bm.pay matches {FORM0 + i} if entity @s[advancements={{bm:ferro/learned/{w}=true}}] run return run function bm:p271/forms/pick {{i:{i}}}'
        for i, w in enumerate(order, 1)])
    fn('p271/forms/pick0', ['scoreboard players set @s bm.fqo 0', csay('(its copy melts away - and it rises out of the puddle as itself)')])
    fn('p271/forms/pick', ['$scoreboard players set @s bm.fqo $(i)', csay('(it stretches up, goes all to column - and fills out into somebody else)')])
    # ---- the host follows its owner's choice (each tick): changed, it morphs - 17 ticks (bm.fqm counts them)
    X.tick.append('execute as @e[type=minecraft:wolf,tag=bm.fepet,tag=!bm.ffpet] at @s run function bm:p271/fm/sync')
    fn('p271/fm/sync', ['execute unless score @s bm.fqf matches 0.. run function bm:p271/fm/fresh',
                        'scoreboard players set #fo bm.rng 0', 'execute on owner run scoreboard players operation #fo bm.rng = @s bm.fqo',
                        'execute if score @s bm.fqm matches 0 if score @s bm.fqf = #fo bm.rng run return 0',
                        'scoreboard players operation #me bm.pid = @s bm.pid',            # (its own displays picked out: the tick's, here)
                        'execute as @e[type=minecraft:item_display,tag=bm.fep_pet,tag=!bm.fefade] if score @s bm.pid = #me bm.pid run tag @s add bm.fesel',
                        'function bm:p271/fm/sync2', 'tag @e[type=minecraft:item_display,tag=bm.fesel] remove bm.fesel'])
    fn('p271/fm/sync2', ['execute if score @s bm.fqm matches 1.. run return run function bm:p271/fm/step',
                         'execute unless score @s bm.fqf = #fo bm.rng run function bm:p271/fm/begin'])
    fn('p271/fm/fresh', ['scoreboard players set @s bm.fqf 0', 'scoreboard players set @s bm.fqm 0', 'execute on owner run scoreboard players set @s bm.fqo 0'])   # (called, sent home and back: it comes as itself)
    fn('p271/fm/begin', ['scoreboard players operation @s bm.fqf = #fo bm.rng', 'scoreboard players set @s bm.fqm 1',
                         'particle minecraft:dust{color:[0.06,0.06,0.1],scale:1.4} ~ ~0.5 ~ 0.4 0.5 0.4 0 24', 'playsound minecraft:entity.slime.squish neutral @a[distance=..16] ~ ~ ~ 0.8 0.7'])
    sel = '@e[type=minecraft:item_display,tag=bm.fesel'
    rig = f'{sel},tag=!bm.fep_form,tag=!bm.fep_feyes]'
    fn('p271/fm/step', ['scoreboard players add @s bm.fqm 1',
                        f'execute if score @s bm.fqm matches 2 run execute as {rig} run data merge entity @s {{start_interpolation:0,interpolation_duration:6,transformation:{{scale:[0.3f,1.2f,0.3f]}}}}',
                        'execute if score @s bm.fqm matches 8 run function bm:p271/fm/swap',
                        'execute if score @s bm.fqm matches 8 if score @s bm.fqf matches 1.. run function bm:p271/fm/kf {k:5,d:1}',
                        'execute if score @s bm.fqm matches 9 if score @s bm.fqf matches 1.. run function bm:p271/fm/kf {k:3,d:4}',
                        'execute if score @s bm.fqm matches 13 if score @s bm.fqf matches 1.. run function bm:p271/fm/kf {k:1,d:3}',
                        'execute if score @s bm.fqm matches 16 if score @s bm.fqf matches 1.. run function bm:p271/fm/kf {k:0,d:3}',
                        'execute if score @s bm.fqm matches 17.. run scoreboard players set @s bm.fqm 0'])
    # (the swap: into a form - its displays (form, eyes) out of the puddle, the rig gone; back - the displays gone, the rig re-posed)
    fn('p271/fm/swap', [f'kill {sel},tag=bm.fep_form]', f'kill {sel},tag=bm.fep_feyes]',
                        'execute if score @s bm.fqf matches 0 run return run function bm:p271/fm/self',
                        'execute store result storage bm:tmp fe.i int 1 run scoreboard players get @s bm.fqf', 'function bm:p271/fm/load with storage bm:tmp fe'])
    fn('p271/fm/self', ['tag @s remove bm.fexf', 'scoreboard players set @s bm.fqa 0', f'scoreboard players set @s {X.S("fr")} -1',
                        f'execute on passengers run data merge entity @s[type=minecraft:interaction,tag=bm.fehit] {{width:{Ferro.HIT[0]}f,height:{Ferro.HIT[1]}f}}'])
    fn('p271/fm/load', ['$execute unless data storage bm:fe f$(i) run return run function bm:p271/fm/self', '$data modify storage bm:tmp fe.f set from storage bm:fe f$(i)',
                        'tag @s add bm.fexf', f'execute as {rig} run data merge entity @s {{start_interpolation:0,interpolation_duration:2,transformation:{{scale:[0f,0f,0f]}}}}',
                        'execute store result score @s bm.fqa run data get storage bm:tmp fe.f.a',
                        'scoreboard players set #fk bm.rng 0', 'execute on owner run scoreboard players operation #fk bm.rng = @s bm.cosfe',
                        'execute store result storage bm:tmp fe.f.c int 1 run scoreboard players get #fk bm.rng',
                        'scoreboard players operation #me bm.pid = @s bm.pid',
                        'function bm:p271/fm/put with storage bm:tmp fe.f',
                        'execute store result storage bm:tmp fe.p int 1 run scoreboard players get @s bm.pid', 'function bm:p271/fm/keep with storage bm:tmp fe'])
    fn('p271/fm/keep', ['$data modify storage bm:fe p$(p) set from storage bm:tmp fe.f'])
    disp = lambda tags, model: ('summon minecraft:item_display ~ ~ ~ ' + snbt({'Tags': tags, 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': model}},
                                                                             'item_display': 'fixed', 'teleport_duration': Int(2), 'interpolation_duration': Int(4),
                                                                             'transformation': {'left_rotation': [F(0)] * 3 + [F(1)], 'right_rotation': [F(0)] * 3 + [F(1)],
                                                                                                'translation': [F(0)] * 3, 'scale': [F(0)] * 3}}))
    tags = lambda p: ['bm.fep', f'bm.fep_{p}', 'bm.fep_pet', 'bm.fenew']
    fn('p271/fm/put', ['$execute if score #fk bm.rng matches 0 run ' + disp(tags('form'), 'bm:$(m)'),
                       '$execute if score #fk bm.rng matches 1.. run ' + disp(tags('form'), 'bm:$(m)_c$(c)'),
                       '$execute if score #fk bm.rng matches 0 unless data storage bm:tmp fe.f.e run ' + disp(tags('feyes') + ['bm.fep_eyes'], 'bm:$(m)_eyes'),
                       '$execute if score #fk bm.rng matches 1.. unless data storage bm:tmp fe.f.e run ' + disp(tags('feyes') + ['bm.fep_eyes'], 'bm:$(m)_eyes_c$(c)'),
                       'execute if data storage bm:tmp fe.f.e run ' + disp(tags('feyes') + ['bm.fep_eyes'], 'bm:fe_meyes'),
                       'scoreboard players operation @e[type=minecraft:item_display,tag=bm.fenew,distance=..1] bm.pid = #me bm.pid',
                       'tag @e[type=minecraft:item_display,tag=bm.fenew,distance=..1] add bm.fesel', 'tag @e[type=minecraft:item_display,tag=bm.fenew,distance=..1] remove bm.fenew',
                       '$execute on passengers run data merge entity @s[type=minecraft:interaction,tag=bm.fehit] {width:$(w)f,height:$(h)f}'])
    # (a keyframe of the form's motion: its transformation from its entry, eased over d ticks - the eyes on the same one, or their own spot)
    fn('p271/fm/kf', ['$data modify storage bm:tmp fe.kf set value {k:$(k),d:$(d)}', 'execute store result storage bm:tmp fe.kf.p int 1 run scoreboard players get @s bm.pid',
                      'function bm:p271/fm/kf2 with storage bm:tmp fe.kf'])
    fn('p271/fm/kf2', [f'$execute as {sel},tag=bm.fep_form] run data modify entity @s transformation set from storage bm:fe p$(p).k$(k)',
                       f'$execute as {sel},tag=bm.fep_form] run data merge entity @s {{start_interpolation:0,interpolation_duration:$(d)}}',
                       f'$execute unless data storage bm:fe p$(p).e as {sel},tag=bm.fep_feyes] run data modify entity @s transformation set from storage bm:fe p$(p).k$(k)',
                       f'$execute if data storage bm:fe p$(p).e as {sel},tag=bm.fep_feyes] run data modify entity @s transformation set from storage bm:fe p$(p).e',
                       f'$execute as {sel},tag=bm.fep_feyes] run data merge entity @s {{start_interpolation:0,interpolation_duration:$(d)}}'])
    fn('p271/fm/squash', ['execute if entity @s[tag=bm.fexf] run function bm:p271/fm/kf {k:3,d:2}'])
    # (its displays follow it - rigpet's place puts the rig's; these two stand on the host, turned with it)
    G.FUNCS[f'{pfx}/place'] += [f'tp {sel},tag=bm.fep_form] ~ ~ ~ ~ 0', f'tp {sel},tag=bm.fep_feyes] ~ ~ ~ ~ 0']
    W5.poses_for(Ferro, G, ['grin'])
    fn(f'{pfx}/box_fit', ['execute unless entity @s[tag=bm.fexf] run return 0', 'execute store result storage bm:tmp fe.p int 1 run scoreboard players get @s bm.pid',
                          'function bm:p271/fm/refit with storage bm:tmp fe'])
    fn('p271/fm/refit', ['$function bm:p271/fm/refit2 with storage bm:fe p$(p)'])
    fn('p271/fm/refit2', ['$execute on passengers run data merge entity @s[type=minecraft:interaction,tag=bm.fehit] {width:$(w)f,height:$(h)f}'])
    # ---- in a form, every pose of its own is a keyframe of the goo puppet instead (a waddle, a lean, a squash, a slump)
    KEYS = {'walk_0': 't1', 'walk_1': 't2', 'run_0': 't1', 'happy': 't3', 'melt': 't4', 'sit_a': 't4', 'sit_a2': 't4', 'sit_b': 't4', 'sit_b2': 't4', 'tired': 't5',
            'hurt': 't3', 'alert': 't3', 'grin': 't3'}
    for n in [n for n in G.FUNCS if n.startswith(f'{pfx}/pose/') and '/tw' not in n]:
        name = n[len(f'{pfx}/pose/'):]
        k = KEYS.get(name, 't0' if name.startswith('idle') else 't3')
        G.FUNCS[n] = [f'execute if entity @s[tag=bm.fexf] run return run function bm:p271/fm/kf {{k:{k[1:]},d:4}}'] + G.FUNCS[n]
    # ---- the encounter's disguise: the Ink Blot's form over its hidden rig (the encounter's box: as it)
    ib = order.index('inkblot') + 1 if 'inkblot' in order else 0
    ibm = f'fm_{item_of["inkblot"]}' if ib else 'fe_body'
    fn('p271/fm/enc_form', ([f'data modify storage bm:tmp fe.e set from storage bm:fe f{ib}'] if ib else []) +
       [disp(['bm.feencf', 'bm.fenew'], f'bm:{ibm}'), ('execute as @e[type=minecraft:item_display,tag=bm.fenew,distance=..1] run data modify entity @s transformation set from storage bm:tmp fe.e.k0' if ib else 'tag @s add bm.fenoform'),
        'tag @e[type=minecraft:item_display,tag=bm.fenew,distance=..1] remove bm.fenew'])
    G.FUNCS['p271/enc/gone'].insert(0, 'kill @e[type=minecraft:item_display,tag=bm.feencf,distance=..4]')
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.feencf]']
    fn('admin/ferro_learn_all', [f'advancement grant @s only bm:ferro/learned/{w}' for w in order])
    return order


def generate(G):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    frame = dict(models=[], click=[f'data modify entity @s Item.components."minecraft:item_model" set value "bm:{ITEM}_f1"',
                                   'playsound minecraft:block.respawn_anchor.charge block @a[distance=..12] ~ ~ ~ 0.5 1.8',
                                   'particle minecraft:dust{color:[0.06,0.06,0.1],scale:0.8} ~ ~0.2 ~ 0.15 0.15 0.15 0 10',
                                   'scoreboard players set @s bm.fqft 2'],
                 tick=['execute if score @s bm.fqft matches 1.. run scoreboard players remove @s bm.fqft 1',
                       f'execute if score @s bm.fqft matches 0 run data modify entity @s Item.components."minecraft:item_model" set value "bm:{ITEM}"',
                       'execute if score @s bm.fqft matches 0 run scoreboard players reset @s bm.fqft'])
    W5.build(Ferro, G, _abilities, _encounter, sitb=(120, [(0, 'sit_b'), (60, 'sit_b2')]), frame=frame)
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.fqft dummy']
    G.OBJECTIVES.append('bm.fqft')

    class _X:                                   # (what _forms_dp needs of rigpet's kit)
        S = staticmethod(lambda s: f'bm.{Ferro.q}{s}')
        tick, second = G.FUNCS['tick'], G.FUNCS['loop/second']
    _forms_dp(G, _X)
    # (the meyes face definitions: the shared eyes worn by the nine forms with none of their own)
    fn('admin/ferro_reset', ['tag @s remove bm.femet', 'scoreboard players set @s bm.fqo 0', f'clear @s *[minecraft:custom_data~{{bm:"{ITEM}"}}]',
                             title('@s', 'actionbar', T('The Ferro has not met you yet.', COL))])

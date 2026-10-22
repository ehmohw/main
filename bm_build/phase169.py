"""2.82: KING OMEGA - the Omega Palace, his tomb, his coming, his fight, his peace - and the King at court (phase170: the follower).

THE OMEGA PALACE (palace.py): a grey castle in a dark wood, rare in Dappled Forests, Dark Oak Forests and Pale Gardens - not
  hidden: you'll know it when you see it (black spires, yellow windows, the round crossed windows in its tower, a dead tree by
  the path, soul wisps round the towers). It is haunted, and it sounds it: its own waltz on a music box in the empty halls
  (THE OMEGA PALACE, tools/boss_music.py), whispers, a far-off organ, chains, a clock that strikes thirteen; candles that
  gutter, souls drifting through the rooms, and two soul serpents circling the central tower at night.
THE TOMB: in the throne room behind the great door, a black sarcophagus ringed by six pedestals - one for each Conquest Emblem
  (the Broodmother's, the Frost Marksman's, the Drowned Tyrant's, the Archmage's, Bobbery's and the Hollow King's Crown of
  Conquest). Right-click a pedestal with its emblem to seat it; sneak + punch to take it back. All six seated AND Apophiss
  (a follower) by the tomb: the King of the Dead wakes.
HIS COMING (12 s): the lights die, a heartbeat, soul fire spirals out of the floor and the six emblems pour their light into
  it - then claws break up through the flagstones and he CRAWLS out of the ground, dragging himself up, maw wide, and roars.
  He knows exactly who woke him.
THE FIGHT (KING OF THE DEAD, his theme): CLAW (a raking sweep), SOUL FLAME (the fire off his tail, thrown - it bursts), SOUL
  SERPENTS (two at a time, never more than three - cute, and they bite), the PILLARS OF THE DEAD (a ring of soul fire under
  each of you erupts a breath later - step out); at three-quarters, his GHOST GUARD; at half, GRIEF - he wails, the dark comes
  down, and he vanishes, to strike from behind three times before he shows himself again, faster now, throwing his flame in
  threes. Every player within 40 makes him tougher (phase67).
HIS PEACE: beaten low, he kneels. The brothers talk - and it ends well. Everyone in the throne room is given OMEGA'S MONOCLE
  (phase170: he walks with you), and he takes his throne: from then on the King holds court in every Omega Palace. Seat the six
  again with Apophiss by and he'll gladly have a rematch (a hoard, favour, a Monocle for anyone without one).
AT COURT (right-click him on his throne):
  THE PEERAGE - favour with the King: the fight (60, a rematch 20), each new gift (40), a tithe of 4 Tokens (10, five a day),
    your Omega's Soul Court (2 a soul). Ranks: Squire 40 (a title over your head - on/off - and the Garrison opens), Knight 120
    (Soul-Edged: your blows burn the undead), Baron 250 (the Royal Ward: your braziers turn away hostile spawns), Duke 450
    (the undead near you falter), Warden of the Dead 700 (two soul serpents escort you, striking what comes near; and once a
    day at two hearts or less, the Royal Pardon - you're restored).
  THE GHOST GARRISON - a SOUL BRAZIER (8 Tokens; three each): set it down and a soul serpent keeps it - by night it circles
    the brazier and bites anything hostile that comes within 16 (and plays tricks on you now and then: a BOO, a cookie, a
    spin). With the Royal Ward, no hostile mob spawns within 24 of it. Break the fire: it comes back to you.
  THE CHRONICLE - he tells his story only to friends who bring him something: ten gifts, ten chapters (a hint for each in the
  book), re-read any time."""
import math
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import omega_art as OA
import soulserp_art as SA
import palace as PAL
import rigfol as RF
import rigkit as RK
from rigkit import qs
import phase67 as P67
import phase152 as P152

OM_C, OM_LINE, SOUL = '#9fb4ff', '#e4ecff', '#5ad8ff'
GRN, GRN_LT = '#3ad06a', '#c8f0b0'
GOLD = '#ffcf40'
BOSS_HP = 900
SB = OA.BOSS_SCALE
UB = SB / 16
SS = SA.RIG_SCALE
USS = SS / 16
COURT = 2320                         # the King at court (bm.menu); his buttons 2321..2379
EMB = PAL.EMBLEMS
EMB_NAME = {'brood': 'the Broodmother', 'frost': 'the Frost Marksman', 'tide': 'the Drowned Tyrant', 'hex': 'the Archmage', 'keep': 'Bobbery',
            'hollow': 'the Hollow King'}
EMB_COL = {'brood': '#7d8f3a', 'frost': '#a8d8ff', 'tide': '#2fa39b', 'hex': '#9b59d0', 'keep': '#b0705a', 'hollow': '#e5e4e2'}
RANKS = [(0, 'Commoner', 'gray'), (40, 'Squire', '#c0c8d8'), (120, 'Knight', '#9fb4ff'), (250, 'Baron', '#b48cff'), (450, 'Duke', '#ffcf40'),
         (700, 'Warden of the Dead', '#5ad8ff')]
PERKS = ['', 'a title over your head; the Ghost Garrison opens', 'Soul-Edged: your blows burn the undead',
         'the Royal Ward: your Soul Braziers turn away hostile spawns', 'the undead near you falter',
         'a soul serpent escort; the Royal Pardon, once a day']
TITHE, TITHE_DAY, BRAZIER_COST, BRAZIER_MAX = 4, 5, 8, 3
# the gifts he'll accept (the plain item, not anything of the pack's made from it) and the chapter each opens
GIFTS = [
    ('minecraft:golden_apple', 'something golden to eat', 'I. Two Eggs in the Sun',
     ['Two eggs on a warm black rock at the edge of Omega Island. Mine hatched first - by an hour, and I never let him forget it.',
      'He was the clever one. I was the one who shared. Our mother said that between us we made one sensible serpent.',
      'We ate golden apples from the palace orchard until we were sick. He always took the bigger one. I always let him.']),
    ('minecraft:spyglass', "a lens for an old king's eye", 'II. The Monocle',
     ['I could never see past the end of my own snout. Apophiss thought this was the funniest thing in the world.',
      'For my hundredth birthday he gave me this monocle, as a joke. I wore it to dinner. I wore it to bed. I wore it to war.',
      'He never knew I kept it. I never told him. I suppose I am telling you instead.']),
    ('minecraft:cake', 'something for a feast', 'III. The Feast of Crowns',
     ["When the old king died, the island chose. Not the cleverer brother - the kinder one. Their word, not mine.",
      'There was a feast. Apophiss smiled all night and carved the cake and toasted me twice.',
      'I should have known. He never smiled at a cake he was not allowed to eat all of.']),
    ('minecraft:book', 'a book to keep', 'IV. The Library of Small Things',
     ['A king should know his people. So I wrote them down - every fisher, every baker, every child who brought me a shell.',
      'The library in the west wing holds them still. Thousands of small lives, and every one of them mattered.',
      'Apophiss called it a waste of ink. He wanted a library of victories. It would have been a very short book.']),
    ('minecraft:soul_lantern', 'a light that burns blue', 'V. The Light to Lead Them',
     ['The flame on my tail was always blue. In storms the island followed it home - fishing boats, lost children, my soldiers.',
      'I am told it still burns over the palace on dark nights. I am told the old fishermen still steer by it.',
      'A light is only worth something if someone else can see by it. Remember that, when you carry one.']),
    ('minecraft:iron_sword', "a soldier's blade", 'VI. The War of Brothers',
     ['An island was not enough for him. He wanted the sea, then the land beyond it, then everything with a crown on it.',
      'I would not give him the army. So he raised his own, out of shadow and promises, and came for the palace.',
      'We fought on the great stair, he and I. This wound on my chest is his. I gave him the scar on his pride. We both lost.']),
    ('minecraft:poppy', 'a flower for a grave', 'VII. The Last Night',
     ['I held the great door until the last of my people were out of the back gate. Then I could not hold it any more.',
      'My last words to him were "Look after them." He did not. He went away to make other kings - hollow ones.',
      'But I find I am not angry now. Death is very long. Anger is very tiring.']),
    ('minecraft:echo_shard', 'an echo of something lost', 'VIII. The Long Quiet',
     ['For three hundred years I lay in the dark under my own throne and listened to the palace forget me.',
      'One by one the lights went out. The banners faded. The orchard went wild. Only one voice came every evening.',
      '"Dinner is at seven, Your Majesty. As always." Pistachio never once missed a night. I never once answered. I am sorry for that.']),
    ('minecraft:honey_bottle', 'something sweet for the tea', 'IX. The Butler and the Boy',
     ['One winter Pistachio found a boy asleep on the palace steps - a hood, a staff, and a spark in his fingers he could not control.',
      'Pistachio gave him soup, then a room, then a scolding about his boots. The boy was Cecil. The palace had a child in it again.',
      'He thinks I do not know he lives in my west wing. I have heard him practising spells at midnight for years. He is getting better.']),
    ('minecraft:nether_star', 'a star from a dead thing', 'X. What the Dead King Wants',
     ['Not my crown back. Not my island. Not even revenge - I have had three hundred years to want it, and found I did not.',
      'I want my brother to be the serpent our mother hoped for. I want the palace full of noise. I want someone to finish the cake.',
      'And I want friends who bring an old ghost strange presents. It seems I have one. Thank you.'])]

# the boss theme (phase152): KING OF THE DEAD - and silent while he crawls out and while he kneels
P152.THEMES[13] = ('omega', 64)
P152.WHO_LATE.append((13, 'type=minecraft:husk,tag=bm.omboss,tag=!bm.omcalm'))
P67.BOSSES.append(('bm.omboss', 'bm:omegab'))

# ------------------------------------------------------------------------------------------------ items
item('om_brazier', TOTEM, 'Soul Brazier', SOUL,
     ['A black iron bowl of blue fire from the', "King of the Dead's own hearth.", ('Use on a block: set it down - a soul serpent keeps it.', 'blue'),
      ('By night it bites anything hostile within 16.', 'blue'), ('(The Royal Ward: no hostile spawns within 24.)', 'gray'),
      ('Break the fire: the brazier comes back to you.', 'gray'), ('"Mind the little ones. They bite. Affectionately."', 'dark_gray')],
     model='bm:om_brazier', stack=1, cat='magic', glint=True, comps=hold('none'))
HOLD['om_brazier'] = 'bm:p169/bz/use'


# ------------------------------------------------------------------------------------------------ the rigs (rigfol's view of the art)
class OArt:
    PIVOT, PARENT, PARTS, PART_K, PREFIX = OA.PIVOT, OA.PARENT, OA.PARTS, OA.PART_K, OA.PREFIX
    HIDDEN = staticmethod(OA.HIDDEN)
    model_name = staticmethod(OA.model_name)


class SArt:
    PIVOT, PARENT, PARTS, PART_K, PREFIX = SA.PIVOT, SA.PARENT, SA.PARTS, SA.PART_K, SA.PREFIX
    HIDDEN = staticmethod(SA.HIDDEN)
    model_name = staticmethod(SA.model_name)


POSES = {k: dict(v) for k, v in OA.POSES.items()}
SPOSES = {k: dict(v) for k, v in SA.POSES.items()}
DUR_B = {'idle_a': 30, 'idle_b': 30, 'glide_a': 6, 'glide_m': 6, 'glide_b': 6, 'battle': 6, 'claw_up': 7, 'claw': 3, 'flame_up': 10, 'flame_swing': 2,
         'flame_throw': 3, 'rally': 8, 'summon': 12, 'tired': 20, 'kneel': 30, 'welcome': 14, 'bow': 14, 'monocle': 12, 'shock': 6, 'fade': 18,
         'crawl_a': 20, 'crawl_b': 24, 'crawl_c': 20}
DUR_S = {'idle_a': 14, 'idle_b': 14, 'float_a': 6, 'float_m': 6, 'float_b': 6, 'cackle': 5, 'grin': 6, 'sneak': 8, 'boo': 3, 'swipe_up': 5,
         'swipe': 3, 'lunge': 3, 'hurt': 4, 'fade': 14, 'salute': 8}
FACE_CASES = {f: f for f in OA.FACES}                               # (the boss and the King: the art's own faces)
FOL_FACE = {'happy': 'warm', 'surprised': 'shock', 'hurt': 'tired', 'sleepy': 'tired', 'blink': 'blink', 'squint': 'warm', 'serious': None}
loc = lambda v: f'^{v[0]:.2f} ^{v[1]:.2f} ^{v[2]:.2f}'
FLAME_AT = RK.point(OArt, POSES['flame_throw'], 'flame', (OA.PIVOT['flame'][0], OA.PIVOT['flame'][1] + 8, OA.PIVOT['flame'][2]), scale=SB)


# ================================================================================================= resource pack
def _banner():
    """the hall's banners: deep purple, a gold border, the gold Omega - and the swallow-tail foot (16 x 32, in the left half of a
    32 x 32 sheet: atlas textures are square)"""
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pur, pur2, gold, gold2 = hexc('#7a1aa8'), hexc('#5c1080'), hexc('#e8c838'), hexc('#a88a18')
    d.polygon([(0, 0), (15, 0), (15, 31), (8, 24), (0, 31)], fill=gold)
    d.polygon([(2, 2), (13, 2), (13, 27), (8, 21), (2, 27)], fill=pur)
    for y in range(2, 26, 3): d.line((2, y, 13, y), fill=pur2)
    d.arc((4, 6, 11, 14), 140, 400, fill=gold, width=2)                       # the Omega: a ring open at the foot,
    d.line((3, 15, 6, 15), fill=gold, width=1); d.line((9, 15, 12, 15), fill=gold, width=1)    # its two feet
    d.point((4, 7), fill=gold2); d.line((0, 0, 15, 0), fill=gold2)
    return im


def _brazier_icon():
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(2, 8), (13, 8), (11, 12), (4, 12)], fill=hexc('#2a2a30'), outline=hexc('#0c0c10'))
    d.rectangle((6, 12, 9, 15), fill=hexc('#1a1a20'))
    d.polygon([(4, 8), (6, 3), (7, 6), (8, 1), (10, 6), (11, 4), (12, 8)], fill=hexc('#5ad8ff'))
    d.polygon([(6, 8), (8, 4), (10, 8)], fill=hexc('#e6fbff'))
    d.point((3, 9), fill=hexc('#6a6a74')); d.point((12, 9), fill=hexc('#6a6a74'))
    return im


def textures():
    out = OA.textures()
    out.update(SA.textures())
    out['om_banner'] = _banner()
    return out


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    for art in (OA, SA):
        for name, (tex, els) in art.models().items():
            R.HATS[name] = (tex, els)
        R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (art.PREFIX,)
    face = {'uv': [0, 0, 8, 16], 'texture': '#b'}
    back = {'uv': [8, 0, 0, 16], 'texture': '#b'}
    R.HATS['om_guard'] = ({'x': 'minecraft:block/stone'}, [])          # (nothing to see: the King's off-hand ward)
    R.HATS['om_banner'] = ({'b': 'bm:block/om_banner'}, [{'from': [4, -8, 8], 'to': [12, 8, 8.1], 'faces': {'north': back, 'south': face}}])
    R.HATS['om_brazier'] = ({'s': 'minecraft:block/soul_fire_0', 'k': 'minecraft:block/polished_blackstone'},
                            [{'from': [4, 0, 4], 'to': [12, 4, 12], 'faces': {f: {'uv': [0, 0, 16, 8], 'texture': '#k'} for f in ('north', 'south', 'east', 'west', 'up', 'down')}},
                             {'from': [5, 4, 5], 'to': [11, 10, 11], 'light_emission': 15, 'faces': {f: {'uv': [0, 0, 16, 16], 'texture': '#s'} for f in ('north', 'south', 'east', 'west')}}])
    R.ICONS['om_brazier'] = _brazier_icon()

    def post(R2):
        mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
        cases = [{'when': f, 'model': mdl(f'om_head_x{m}')} for f, m in FACE_CASES.items()] + \
                [{'when': e, 'model': mdl(f'om_head_x{m}')} for e, m in FOL_FACE.items() if m and e not in FACE_CASES]   # (2.82b: a case listed twice - 'blink' - and the game threw the whole head out: a missing-model cube)
        R2.wj('assets/bm/items/om_head.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                           'cases': cases, 'fallback': mdl('om_head')}})
        for cr in SA.CRESTS:
            R2.wj(f'assets/bm/items/ss_head_{cr}.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                                     'cases': [{'when': f, 'model': mdl(f'ss_head_{cr}_x{f}')} for f in SA.FACES],
                                                                     'fallback': mdl(f'ss_head_{cr}')}})
    R.POST.insert(0, post)                      # (first: phase138 copies these item definitions for the recoloured looks)

    def post_snd(R2):                           # the palace's waltz (the boss theme is phase152's, from THEMES)
        import json, os, shutil
        here = os.path.dirname(os.path.abspath(__file__))
        sj = R2.p('assets', 'bm', 'sounds.json')
        snd = json.load(open(sj)) if os.path.exists(sj) else {}
        os.makedirs(R2.p('assets', 'bm', 'sounds', 'music'), exist_ok=True)
        shutil.copy(os.path.join(here, 'vendor', 'boss_palace.ogg'), R2.p('assets', 'bm', 'sounds', 'music', 'boss_palace.ogg'))
        snd['music.boss_palace'] = {'sounds': [{'name': 'bm:music/boss_palace', 'stream': True}]}
        R2.wj('assets/bm/sounds.json', snd)
    R.POST.append(post_snd)


# ================================================================================================= the datapack
class _C:
    """what every part of this phase shares"""
    def __init__(self, G):
        self.G, self.fn, self.title, self.tellraw, self.give, self.PREFIX = G, G.fn, G.title, G.tellraw, G.give, G.PREFIX
        self.tick, self.fast, self.second = [], [], []
        self.say = lambda txt, col='gray', who='@s': G.title(who, 'actionbar', T(txt, col))
        self.omsay = lambda txt, who='@s': G.title(who, 'actionbar', [T('King Omega: ', OM_C, bold=True), T(txt, OM_LINE)])
        self.omchat = lambda txt, who='@s': G.tellraw(who, [T('King Omega: ', OM_C, bold=True), T(f'"{txt}"', OM_LINE)])
        self.apchat = lambda txt, who='@s': G.tellraw(who, [T('Apophiss: ', GRN, bold=True), T(f'"{txt}"', GRN_LT)])

    def objs(self, *names):
        self.G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in names]
        self.G.OBJECTIVES += list(names)


def generate(G):
    C = _C(G)
    C.objs('bm.ompin', 'bm.ommu', 'bm.omclk', 'bm.omst', 'bm.omt', 'bm.ssid', 'bm.ssf', 'bm.sss', 'bm.sst', 'bm.ssk', 'bm.omid', 'bm.omatk', 'bm.omc',
           'bm.omph', 'bm.omr', 'bm.omlone', 'bm.omf', 'bm.oms', 'bm.omfav', 'bm.omlore', 'bm.omtd', 'bm.omtn', 'bm.omtt', 'bm.ompd', 'bm.omhc',
           'bm.omwin', 'bm.omseen', 'bm.omgd', 'bm.omrd')
    G.FUNCS['load'][-1:-1] = [f'scoreboard players set #{n} bm.rng {n}' for n in (2, 3, 4, 6, 8, 10, 12, 14, 20, 24, 28, 40, 60, 100, 1000)]
    _palace(C)
    _serpents(C)
    _tomb(C)
    _boss(C)
    _court(C)
    G.FUNCS['tick'] += C.tick
    G.FUNCS['loop/fast'][-1:-1] = C.fast
    G.FUNCS['loop/second'][-1:-1] = C.second


# ------------------------------------------------------------------------------------------------ the palace in the world
OX, OY, OZ = -32, -(PAL.FY + 1), -39                                       # (the template's corner, from the seed's block)
rel = lambda p: (p[0] - PAL.CENTER[0], p[1] - PAL.CENTER[1], p[2] - PAL.CENTER[2])   # (template point -> from the palace's marker)
BOX = (f'~{-PAL.CENTER[0]:.1f} ~{-PAL.CENTER[1]:.1f} ~{-PAL.CENTER[2]:.1f}', f'dx={PAL.SX - 1},dy={PAL.SY - 1},dz={PAL.SZ - 1}')


def _palace(C):
    G, fn, second, fast = C.G, C.fn, C.second, C.fast
    wj = G.wjson
    wj('bm/tags/worldgen/biome/has_structure/om_palace.json', {'values': ['minecraft:dark_forest', 'minecraft:dappled_forest', 'minecraft:pale_garden']})
    wj('bm/worldgen/structure/om_palace.json', {'type': 'minecraft:jigsaw', 'biomes': '#bm:has_structure/om_palace', 'step': 'surface_structures',
                                               'spawn_overrides': {}, 'terrain_adaptation': 'none', 'start_pool': 'bm:om_palace/start', 'size': 1,
                                               'start_height': {'absolute': 0}, 'project_start_to_heightmap': 'WORLD_SURFACE_WG',
                                               'max_distance_from_center': 80, 'use_expansion_hack': False, 'liquid_settings': 'ignore_waterlogging'})
    wj('bm/worldgen/template_pool/om_palace/start.json', {'fallback': 'minecraft:empty', 'elements': [
        {'weight': 1, 'element': {'element_type': 'minecraft:single_pool_element', 'location': 'bm:om_palace_seed', 'projection': 'rigid', 'processors': 'minecraft:empty'}}]})
    wj('bm/worldgen/structure_set/om_palace.json', {'structures': [{'structure': 'bm:om_palace', 'weight': 1}],
                                                   'placement': {'type': 'minecraft:random_spread', 'spacing': 72, 'separation': 28, 'salt': 82002411}})
    from structures import Build
    Bs = Build(1, 1, 1)
    Bs.marker(0.5, 0.0, 0.5, ['bm.omseed'], 0)
    Bs.export(G.path('data', 'bm', 'structure', 'om_palace_seed.nbt'))
    B = PAL.build()
    errs = PAL.check(B)
    assert not errs, errs[:10]
    B.export(G.path('data', 'bm', 'structure', 'p169_palace.nbt'))
    x0, z0, x1, z1 = OX, OZ, OX + PAL.SX - 1, OZ + PAL.SZ - 1
    corners = ' '.join(f'if loaded ~{x} ~ ~{z}' for x in (x0, x1) for z in (z0, z1))
    second.append(f'execute as @e[type=minecraft:marker,tag=bm.omseed] at @s if entity @a[distance=..112] {corners} run function bm:p169/pal/build')
    # (on land: a seed that came down in a lake is dropped; the ground under the box is made good, ten deep, where it fell away)
    skirt = [f'fill ~{x} ~{OY - 10} ~{z0} ~{min(x + 11, x1)} ~{OY - 1} ~{z1} minecraft:stone replace #bm:grap_pass' for x in range(x0, x1 + 1, 12)]
    fn('p169/pal/build', ['kill @s', 'execute if block ~ ~-1 ~ minecraft:water run return 0', 'execute if block ~ ~-1 ~ minecraft:lava run return 0',
                          f'place template bm:p169_palace ~{OX} ~{OY} ~{OZ}'] + skirt +
       [f'execute positioned ~{PAL.CENTER[0] + OX:.1f} ~{PAL.CENTER[1] + OY:.1f} ~{PAL.CENTER[2] + OZ:.1f} as @e[type=minecraft:marker,tag=bm.omnew,distance=..2] at @s run function bm:p169/pal/init'])
    # (2.82c) palaces already standing: the great door's arch cut down to its doors (it was 4 x 4 round 2 x 2 doors - see palace.py)
    cx, cy, cz = PAL.CENTER
    drel = lambda x, y, z: f'~{x - cx + 0.5:g} ~{y - cy:g} ~{z - cz + 0.5:g}'
    hz1, tz0 = PAL.HALL[3], PAL.THRONE[2]
    door = []
    for x in range(31, 35):
        for y in range(PAL.TY + 1, PAL.TY + 6):
            if 32 <= x <= 33 and y <= PAL.TY + 2: continue              # (the doors themselves)
            door.append(f'setblock {drel(x, y, hz1)} minecraft:' + ('stripped_spruce_log[axis=x]' if y == PAL.TY + 3 else 'spruce_planks'))
            if y <= PAL.TY + 4: door.append(f'setblock {drel(x, y, tz0)} minecraft:stone_bricks')
    fn('p169/pal/door282c', ['tag @s add bm.omdoor2'] + door)
    second.append(f'execute as @e[type=minecraft:marker,tag=bm.ompal,tag=!bm.omdoor2] at @s if loaded {drel(31, PAL.TY + 1, hz1)} if loaded {drel(34, PAL.TY + 1, tz0)} '
                  'run function bm:p169/pal/door282c')
    fn('p169/pal/init', ['tag @s remove bm.omnew', 'tag @s add bm.omdoor2', 'scoreboard players set @s bm.omst 0',
                         'execute as @e[type=minecraft:marker,tag=bm.omtomb,distance=..60] run scoreboard players set @s bm.omst 0',   # (the tomb asleep: it's what wakes)
                         'execute as @e[type=minecraft:marker,tag=bm.omsockm,distance=..60] at @s run function bm:p169/sock/make',
                         'execute positioned ~ ~ ~ run playsound minecraft:ambient.soul_sand_valley.mood ambient @a[distance=..96] ~ ~ ~ 1 0.6'])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:marker,tag=bm.omseed]', 'kill @e[type=minecraft:item_display,tag=bm.omban]']
    # (admin: a palace here, now - for testing and for servers that want one)
    fn('admin/omega_palace', ['execute align xyz positioned ~0.5 ~ ~0.5 run function bm:p169/pal/build_here',
                              C.say('The Omega Palace rises from the dark wood.', OM_C)])
    fn('p169/pal/build_here', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.omseed","bm.omadm"]}',
                               'execute as @e[type=minecraft:marker,tag=bm.omadm,distance=..0.5,limit=1] at @s run function bm:p169/pal/build'])
    G.FUNCS['admin/help'].append(C.tellraw('@s', [T('/function bm:admin/omega_palace', 'yellow'), T('  build an Omega Palace here (it faces north: the door at the low z)', 'gray')]))

    # ---- who's inside (every second): the waltz, the ambience, a title the first time in a while
    bx, bd = BOX
    second += ['tag @a remove bm.ominp',
               f'execute as @e[type=minecraft:marker,tag=bm.ompal] at @s positioned {bx} run tag @a[{bd},gamemode=!spectator] add bm.ominp',
               'execute as @a[tag=bm.ominp] at @s run function bm:p169/amb/in',
               'execute as @a[tag=!bm.ominp,scores={bm.ompin=1..}] run function bm:p169/amb/out',
               'execute as @e[type=minecraft:marker,tag=bm.ompal] at @s if entity @a[distance=..96] run function bm:p169/amb/pal']
    fn('p169/amb/in', ['execute unless score @s bm.ompin matches 1.. run function bm:p169/amb/enter', 'scoreboard players set @s bm.ompin 1',
                       # the waltz: not while a boss theme plays; again when it ends
                       'execute if score @s bm.bmt matches 1.. run return run function bm:p169/amb/hush',
                       'scoreboard players remove @s[scores={bm.ommu=1..}] bm.ommu 1',
                       'execute unless score @s bm.ommu matches 1.. run function bm:p169/amb/waltz',
                       'stopsound @s music',
                       'execute store result score #r bm.rng run random value 1..14',
                       'execute if score #r bm.rng matches 1 run playsound minecraft:entity.allay.ambient_without_item ambient @s ^2 ^1 ^-3 0.35 0.45',
                       'execute if score #r bm.rng matches 2 run playsound minecraft:block.chain.place ambient @s ^-4 ^2 ^2 0.5 0.6',
                       'execute if score #r bm.rng matches 3 run playsound minecraft:block.wooden_door.open ambient @s ^5 ^ ^4 0.4 0.5',
                       'execute if score #r bm.rng matches 4 run playsound minecraft:entity.ghast.ambient ambient @s ^-6 ^3 ^-6 0.12 0.5',
                       'execute if score #r bm.rng matches 5 run playsound minecraft:ambient.cave ambient @s ~ ~ ~ 0.5 0.8',
                       'execute if score #r bm.rng matches 6 run playsound minecraft:block.sculk_sensor.clicking ambient @s ^3 ^ ^-2 0.4 0.6',
                       'execute if score #r bm.rng matches 7 run particle minecraft:soul ^ ^1.5 ^3 0.6 0.6 0.6 0.01 3',
                       'execute if score #r bm.rng matches 8 run playsound minecraft:entity.vex.ambient ambient @s ^-3 ^2 ^3 0.25 0.4',
                       'execute store result score #r bm.rng run random value 1..400',
                       'execute if score #r bm.rng matches 1 unless score @s bm.omclk matches 1.. run scoreboard players set @s bm.omclk 13',
                       'execute if score @s bm.omclk matches 1.. run function bm:p169/amb/clock'])
    fn('p169/amb/clock', ['playsound minecraft:block.bell.use ambient @s ^8 ^6 ^-8 0.5 0.5', 'scoreboard players remove @s bm.omclk 1',
                          'execute if score @s bm.omclk matches 0 run ' + C.say('...thirteen. The clock in the tower has struck thirteen.', 'dark_gray')])
    fn('p169/amb/waltz', ['playsound bm:music.boss_palace record @s ~ ~ ~ 0.6 1', 'scoreboard players set @s bm.ommu 60'])
    fn('p169/amb/hush', ['stopsound @s record bm:music.boss_palace', 'scoreboard players set @s bm.ommu 0'])
    fn('p169/amb/out', ['function bm:p169/amb/hush', 'scoreboard players set @s bm.ompin 0'])
    fn('p169/amb/enter', ['title @s times 10 50 20', C.title('@s', 'subtitle', T('"Welcome to Omega Palace!"', OM_LINE, italic=True)),
                          C.title('@s', 'title', T('THE OMEGA PALACE', OM_C, bold=True)), 'playsound minecraft:block.bell.resonate ambient @s ~ ~ ~ 0.6 0.5'])
    G.FUNCS['p152/play'].insert(0, 'function bm:p169/amb/hush')
    G.FUNCS['p104/login'] += ['scoreboard players set @s bm.ompin 0', 'scoreboard players set @s bm.ommu 0']
    G.FUNCS['admin/uninstall'][0:0] = ['stopsound @a record bm:music.boss_palace']
    # (the rooms: souls drifting, candles guttering, the tomb breathing)
    emit = {'hall': ['particle minecraft:soul ~ ~1 ~ 6 2 8 0.01 2', 'particle minecraft:small_flame ~ ~3 ~ 7 2 9 0 1'],
            'library': ['particle minecraft:soul ~ ~ ~ 4 1.5 6 0.01 1', 'particle minecraft:enchant ~ ~ ~ 4 1 6 0.3 3'],
            'dining': ['particle minecraft:soul ~ ~ ~ 4 1.5 6 0.01 1', 'particle minecraft:small_flame ~ ~ ~ 4 0.5 6 0 1'],
            'tomb': ['particle minecraft:sculk_soul ~ ~-2 ~ 3 0.3 3 0.02 3', 'particle minecraft:soul_fire_flame ~ ~-2 ~ 5 0.2 5 0.005 2'],
            'gate': ['particle minecraft:soul ~ ~4 ~ 4 3 2 0.02 2'],
            'cecil': ['particle minecraft:witch ~ ~ ~ 2 1 2 0 1'], 'guest': ['particle minecraft:soul ~ ~ ~ 3 1 4 0.01 1']}
    # (2.82b: those were a particle or two a second across a whole hall - nobody saw them. Four times a second now, from anywhere in
    #  the room, and fuller: wisps that drift and rise, motes of grave-dust hanging in the air, candle smoke, ash falling, soul
    #  fire breathing out of the tomb's floor)
    emit = {'hall': ['particle minecraft:soul ~ ~1 ~ 6 2 8 0.015 2', 'particle minecraft:white_ash ~ ~3 ~ 7 3 9 0 6',
                     'particle minecraft:dust{color:[0.55,0.85,0.95],scale:0.8} ~ ~2 ~ 7 2.5 9 0 2', 'particle minecraft:small_flame ~ ~3 ~ 7 2 9 0 1',
                     'particle minecraft:smoke ~ ~3.5 ~ 7 1.5 9 0.005 1'],
            'library': ['particle minecraft:soul ~ ~ ~ 4 1.5 6 0.01 1', 'particle minecraft:enchant ~ ~ ~ 4 1.5 6 0.4 6', 'particle minecraft:white_ash ~ ~2 ~ 4 2 6 0 3',
                        'particle minecraft:dust{color:[0.55,0.85,0.95],scale:0.7} ~ ~1 ~ 4 1.5 6 0 1'],
            'dining': ['particle minecraft:soul ~ ~ ~ 4 1.5 6 0.01 1', 'particle minecraft:small_flame ~ ~ ~ 4 0.5 6 0 1', 'particle minecraft:smoke ~ ~0.5 ~ 4 0.5 6 0.005 1',
                       'particle minecraft:white_ash ~ ~2 ~ 4 2 6 0 3'],
            'tomb': ['particle minecraft:sculk_soul ~ ~-2 ~ 3 0.3 3 0.02 2', 'particle minecraft:soul_fire_flame ~ ~-2 ~ 5 0.2 5 0.005 3',
                     'particle minecraft:soul ~ ~ ~ 5 2 5 0.02 2', 'particle minecraft:ash ~ ~2 ~ 6 2 6 0 6',
                     'particle minecraft:dust{color:[0.35,0.95,0.9],scale:1.0} ~ ~ ~ 5 2 5 0 2'],
            'gate': ['particle minecraft:soul ~ ~4 ~ 4 3 2 0.02 2', 'particle minecraft:white_ash ~ ~4 ~ 5 3 3 0 3'],
            'cecil': ['particle minecraft:witch ~ ~ ~ 2 1 2 0 1', 'particle minecraft:enchant ~ ~ ~ 2 1 2 0.3 2'],
            'guest': ['particle minecraft:soul ~ ~ ~ 3 1 4 0.01 1', 'particle minecraft:white_ash ~ ~1 ~ 3 1.5 4 0 2']}
    fast.append('execute as @e[type=minecraft:marker,tag=bm.omamb] at @s if entity @a[distance=..24] run function bm:p169/amb/emit')
    fn('p169/amb/emit', [f'execute if entity @s[tag=bm.omamb_{k}] run {l}' for k, ls in emit.items() for l in ls])
    # (the palace: wisps round the towers; by night two soul serpents circle the central tower)
    tw = rel((32.5, PAL.FY + 31, 12.0))
    fn('p169/amb/pal', [f'particle minecraft:soul ~{tw[0]:.1f} ~{tw[1] - 6:.1f} ~{tw[2]:.1f} 4 6 4 0.02 10', 'particle minecraft:soul ~ ~4 ~ 22 4 22 0.015 8', 'particle minecraft:white_ash ~ ~6 ~ 24 6 24 0 14',
                        f'particle minecraft:soul_fire_flame ~{tw[0]:.1f} ~{tw[1]:.1f} ~{tw[2]:.1f} 1 1 1 0.01 2',
                                                f'execute if score #tod bm.bm matches 13000..23000 positioned ~{tw[0]:.1f} ~{tw[1]:.1f} ~{tw[2]:.1f} unless entity @e[type=minecraft:marker,tag=bm.ssbig,distance=..2] run function bm:p169/amb/tower',
                        f'execute unless score #tod bm.bm matches 13000..23000 positioned ~{tw[0]:.1f} ~{tw[1]:.1f} ~{tw[2]:.1f} as @e[type=minecraft:marker,tag=bm.ssbig,distance=..2] at @s run function bm:p169/ss/go'])
    fn('p169/amb/tower', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.sshost","bm.ssorb","bm.ssbig","bm.ssnew"],Rotation:[0f,0f]}',
                          'summon minecraft:marker ~ ~ ~ {Tags:["bm.sshost","bm.ssorb","bm.ssbig","bm.ssnew"],Rotation:[180f,0f]}',
                          'execute as @e[type=minecraft:marker,tag=bm.ssnew,distance=..1] at @s run function bm:p169/ss/born'])


# ------------------------------------------------------------------------------------------------ soul serpents (shared: the boss's, the garrison's, the King's escort, the tower's; phase170's squad)
def ssel(p=None):
    return '@e[type=minecraft:item_display,tag=bm.sssel' + (f',tag=bm.ssp_{p}]' if p else ']')


SCYCLE = {0: (24, [(0, 'float_a'), (6, 'float_m'), (12, 'float_b'), (18, 'float_m')]), 1: (28, [(0, 'idle_a'), (14, 'idle_b')]),
          2: (14, [(0, 'swipe_up'), (5, 'swipe'), (10, 'idle_a')]), 3: (20, [(0, 'cackle'), (6, 'idle_b'), (12, 'cackle')]),
          4: (30, [(0, 'sneak'), (12, 'boo'), (20, 'cackle')]), 5: (16, [(0, 'sneak'), (6, 'lunge'), (12, 'idle_a')]), 6: (None, [(0, 'hurt'), (5, 'fade')]),
          7: (30, [(0, 'idle_a'), (8, 'salute')])}
SS_FACE = {2: 'grin', 3: 'grin', 4: 'shriek', 5: 'shriek', 6: 'hurt'}


def _serpents(C):
    G, fn, tick, second = C.G, C.fn, C.tick, C.second
    # a host is anything tagged bm.sshost with a bm.ssid; its rig's twelve parts carry the same id. bm.sss is its state
    # (SCYCLE), bm.ssf the ticks in it; a host sets #sst and calls p169/ss/state to change state.
    for cr in SA.CRESTS:
        fn(f'p169/ss/rig_{cr}', [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(SArt, p, ["bm.ssp", f"bm.ssp_{p}", "bm.ssnew"], SS, model=(f"ss_head_{cr}" if p == "head" else None), extra={"view_range": F(1.2), "brightness": {"block": Int(13), "sky": Int(13)}})}'
                                 for p in SArt.PARTS])
    fn('p169/ss/born', ['tag @s remove bm.ssnew', 'scoreboard players add #ssn bm.ssid 1', 'scoreboard players operation @s bm.ssid = #ssn bm.ssid',
                        'scoreboard players set @s bm.sss 0', 'scoreboard players set @s bm.ssf 0',
                        'execute store result score #r bm.rng run random value 1..3'] +
       [f'execute if score #r bm.rng matches {i + 1} run function bm:p169/ss/rig_{cr}' for i, cr in enumerate(SA.CRESTS)] +
       ['scoreboard players operation @e[type=minecraft:item_display,tag=bm.ssnew,distance=..1] bm.ssid = @s bm.ssid',
        'tag @e[type=minecraft:item_display,tag=bm.ssnew,distance=..1] remove bm.ssnew',
        'particle minecraft:soul ~ ~0.6 ~ 0.3 0.4 0.3 0.04 14', 'playsound minecraft:entity.vex.charge neutral @a[distance=..16] ~ ~ ~ 0.5 1.6'])
    fn('p169/ss/place', RF.place(SArt, USS, ssel))
    for name in {p for _per, fr in SCYCLE.values() for _t, p in fr}:
        fn(f'p169/ss/pose/{name}', RF.pose(SArt, SPOSES[name], SS, DUR_S.get(name, 5), ssel))
    RF.cycles(fn, 'p169/ss', SCYCLE, 'bm.ssf', 'bm.sss', lambda p: f'p169/ss/pose/{p}')
    face = lambda f: (f'data modify entity {ssel("head")[:-1]},limit=1] item.components."minecraft:custom_model_data" set value {{strings:["{f}"]}}' if f
                      else f'data remove entity {ssel("head")[:-1]},limit=1] item.components."minecraft:custom_model_data"')
    fn('p169/ss/state', ['execute if score #sst bm.rng = @s bm.sss run return 0', 'scoreboard players operation @s bm.sss = #sst bm.rng',
                         'scoreboard players set @s bm.ssf 0', 'function bm:p169/ss/sel'] +
       [f'execute if score @s bm.sss matches {st} run {face(f)}' for st, f in SS_FACE.items()] +
       [f'execute if score @s bm.sss matches 0..1 run {face(None)}', f'execute if score @s bm.sss matches 7 run {face(None)}', 'tag @e[tag=bm.sssel] remove bm.sssel'])
    fn('p169/ss/sel', ['scoreboard players operation #sid bm.rng = @s bm.ssid',
                       'execute as @e[type=minecraft:item_display,tag=bm.ssp,distance=..20] if score @s bm.ssid = #sid bm.rng run tag @s add bm.sssel'])
    # (each tick, as the host, at the spot and facing the serpent should have): its rig there, its frame on
    fn('p169/ss/at', ['function bm:p169/ss/sel', 'function bm:p169/ss/place', 'function bm:p169/ss/anim', 'scoreboard players add @s bm.ssf 1',
                      'execute if score @s bm.sss matches 2..5 if score @s bm.ssf matches 30.. run function bm:p169/ss/calm',
                      'tag @e[tag=bm.sssel] remove bm.sssel'])
    fn('p169/ss/calm', ['scoreboard players set #sst bm.rng 0', 'function bm:p169/ss/state'])
    # (gone: a hurt look, a fade, a puff of souls - then the rig and the host)
    fn('p169/ss/go', ['function bm:p169/ss/sel', 'function bm:p169/ss/pose/fade', 'particle minecraft:soul ~ ~0.6 ~ 0.3 0.4 0.3 0.03 12',
                      'playsound minecraft:entity.vex.death neutral @a[distance=..16] ~ ~ ~ 0.5 1.4', 'kill @e[tag=bm.sssel]',
                      'execute if entity @s[type=!minecraft:player] run tp @s ~ -400 ~', 'kill @s[type=!minecraft:player]'])
    # the orbiting kind (the tower's, the garrison's): the host turns where it is; the serpent rides the circle, facing along it
    tick += ['execute as @e[type=minecraft:marker,tag=bm.ssorb] at @s if entity @a[distance=..64] run function bm:p169/ss/orbit']
    fn('p169/ss/orbit', ['execute if entity @s[tag=bm.ssbig] run tp @s ~ ~ ~ ~1.2 0', 'execute unless entity @s[tag=bm.ssbig] run tp @s ~ ~ ~ ~4 0',
                         'execute if entity @s[tag=bm.ssbig] rotated as @s positioned ^ ^ ^10 rotated ~90 0 run function bm:p169/ss/at',
                         'execute unless entity @s[tag=bm.ssbig] rotated as @s positioned ^ ^ ^3 rotated ~90 0 run function bm:p169/ss/at'])
    # strays: a rig whose host is gone
    second.append('execute as @e[type=minecraft:item_display,tag=bm.ssp,tag=bm.ssp_coil] at @s run function bm:p169/ss/orphan')
    fn('p169/ss/orphan', ['scoreboard players operation #sid bm.rng = @s bm.ssid',
                          'execute as @e[tag=bm.sshost,distance=..24] if score @s bm.ssid = #sid bm.rng run return 0',
                          'execute as @e[type=minecraft:item_display,tag=bm.ssp,distance=..24] if score @s bm.ssid = #sid bm.rng run kill @s',
                          'particle minecraft:soul ~ ~0.5 ~ 0.3 0.3 0.3 0.02 6'])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.ssp]', 'kill @e[tag=bm.sshost,type=!minecraft:player]']


# ------------------------------------------------------------------------------------------------ the tomb: six emblems and Apophiss
def _tomb(C):
    G, fn, fast, second, say = C.G, C.fn, C.fast, C.second, C.say
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    tomb = lambda r=12: f'@e[type=minecraft:marker,tag=bm.omtomb,distance=..{r},limit=1,sort=nearest]'
    lab = lambda d: snbt({'Tags': ['bm.omskt'], 'billboard': 'center', 'view_range': F(0.3), 'default_background': B(0), 'background': Int(0x50000000),
                          'transformation': {'left_rotation': RF.IDENT, 'right_rotation': RF.IDENT, 'translation': [F(0)] * 3, 'scale': [F(0.5)] * 3},
                          'text': [T(EMB_NAME[d].replace('the ', '').title() if d != 'keep' else 'Bobbery', EMB_COL[d], bold=True)]})
    fn('p169/sock/make', [f'execute if entity @s[tag=bm.omsk_{d}] unless entity @e[type=minecraft:interaction,tag=bm.omsock,distance=..1] run '
                          f'summon minecraft:interaction ~ ~-0.5 ~ {{Tags:["bm.omsock","bm.omsk_{d}"],width:0.9f,height:0.9f,response:1b}}' for d in EMB] +
       [f'execute if entity @s[tag=bm.omsk_{d}] unless entity @e[type=minecraft:text_display,tag=bm.omskt,distance=..2] positioned ~ ~1.5 ~ run summon minecraft:text_display ~ ~ ~ {lab(d)}'
        for d in EMB])
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.omsock] if data entity @s interaction at @s run function bm:p169/sock/click',
             'execute as @e[type=minecraft:interaction,tag=bm.omsock] if data entity @s attack at @s run function bm:p169/sock/punch']
    fn('p169/sock/click', ['tag @a remove bm.omu', 'execute on target run tag @s add bm.omu', 'data remove entity @s interaction'] +
       [f'execute if entity @s[tag=bm.omsk_{d}] run function bm:p169/sock/put_{d}' for d in EMB] + ['tag @a remove bm.omu'])
    fn('p169/sock/punch', ['tag @a remove bm.omu', 'execute on attacker run tag @s add bm.omu', 'data remove entity @s attack',
                           'execute unless entity @a[tag=bm.omu,predicate=bm:p20/sneaking] run return run ' +
                           C.title('@a[tag=bm.omu]', 'actionbar', T('Sneak + punch: take an Emblem back.', 'gray')),
                           f'execute if score {tomb(9)} bm.omst matches 1 run return run ' + C.title('@a[tag=bm.omu]', 'actionbar', T('Not now - HE is awake.', OM_C)),
                           'execute if entity @s[tag=bm.omfull] run function bm:p169/sock/takeback', 'tag @a remove bm.omu'])
    for i, d in enumerate(EMB):
        col = EMB_COL[d]
        r, g, b = (int(col[k:k + 2], 16) / 255 for k in (1, 3, 5))
        disp = snbt({'Tags': ['bm.ome', 'bm.omenew'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:emblem_{d}'}},
                     'item_display': 'fixed', 'billboard': 'vertical', 'brightness': {'block': Int(15), 'sky': Int(15)},
                     'transformation': {'left_rotation': RF.IDENT, 'right_rotation': RF.IDENT, 'translation': [F(0)] * 3, 'scale': [F(0.6)] * 3}})
        fn(f'p169/sock/put_{d}', [
            'execute if entity @s[tag=bm.omfull] run return run ' + C.title('@a[tag=bm.omu]', 'actionbar', T('This pedestal already holds its Emblem.', 'gray')),
            f'execute unless items entity @a[tag=bm.omu,limit=1] weapon.mainhand {holds("emblem_" + d)} run return run ' +
            C.title('@a[tag=bm.omu]', 'actionbar', [T('This pedestal is carved for the Conquest Emblem of ', 'gray'), T(EMB_NAME[d], col, bold=True), T('.', 'gray')]),
            'item modify entity @a[tag=bm.omu,limit=1] weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
            'tag @s add bm.omfull', f'summon minecraft:item_display ~ ~1.0 ~ {disp}', 'tag @e[tag=bm.omenew,distance=..2] remove bm.omenew',
            f'particle minecraft:dust{{color:[{r:.2f},{g:.2f},{b:.2f}],scale:1.4}} ~ ~1 ~ 0.2 0.3 0.2 0 24',
            f'playsound minecraft:block.end_portal_frame.fill block @a[distance=..24] ~ ~ ~ 1 {0.6 + i * 0.1:.2f}',
            'playsound minecraft:block.sculk_shrieker.shriek ambient @a[distance=..24] ~ ~ ~ 0.15 0.5',
            f'execute as {tomb()} at @s run function bm:p169/tomb/check'])
        fn(f'p169/sock/give_{d}', [f'loot give @a[tag=bm.omu,limit=1] loot bm:items/emblem_{d}'])
    fn('p169/sock/takeback', [f'execute if entity @s[tag=bm.omsk_{d}] run function bm:p169/sock/give_{d}' for d in EMB] +
       ['tag @s remove bm.omfull', 'kill @e[type=minecraft:item_display,tag=bm.ome,distance=..1.6]',
        'playsound minecraft:block.deepslate.break block @a[distance=..16] ~ ~ ~ 1 1.2', 'particle minecraft:soul ~ ~1 ~ 0.1 0.2 0.1 0.02 8',
        f'execute as {tomb()} if score @s bm.omst matches 2 run scoreboard players set @s bm.omst 0'])
    # (as the tomb) six seated - and Apophiss here?
    ap = '@e[type=minecraft:wolf,tag=bm.appet,distance=..24]'
    fn('p169/tomb/check', ['execute unless score @s bm.omst matches 0 run return 0',
                           'execute store result score #n bm.rng if entity @e[type=minecraft:interaction,tag=bm.omsock,tag=bm.omfull,distance=..8]',
                           'execute unless score #n bm.rng matches 6 run return 0',
                           'execute unless score #hard bm.cfg matches 1 run return run function bm:p169/tomb/not_hard',   # (2.87: a hard-mode exclusive)
                           f'execute if entity {ap} run return run function bm:p169/tomb/wake',
                           'scoreboard players add @s bm.omt 1', 'execute unless score @s bm.omt matches 6.. run return 0', 'scoreboard players set @s bm.omt 0',
                           C.title('@a[distance=..20]', 'actionbar', [T('The six crowns of conquest burn on their pedestals. The tomb is waiting... ', OM_LINE, italic=True),
                                                                     T('(Apophiss must be here.)', 'gray')])])
    fn('p169/tomb/not_hard', ['scoreboard players add @s bm.omt 1', 'execute unless score @s bm.omt matches 6.. run return 0', 'scoreboard players set @s bm.omt 0',
                              C.title('@a[distance=..20]', 'actionbar', [T('The six crowns burn - but the dead do not stir for a world that has not yet woken. ', OM_LINE, italic=True),
                                                                        T('(Hard mode only.)', 'gray')])])
    second.append('execute as @e[type=minecraft:marker,tag=bm.omtomb] at @s if entity @a[distance=..24] run function bm:p169/tomb/sec')
    fn('p169/tomb/sec', ['execute unless score @s bm.omst = @s bm.omst run scoreboard players set @s bm.omst 0',   # (a tomb never set asleep: asleep)
                         'execute if score @s bm.omst matches 1 unless entity @e[type=minecraft:husk,tag=bm.omboss,distance=..40] run scoreboard players set @s bm.omst 2',
                         'function bm:p169/tomb/check',
                         'execute if score @s bm.omst matches 0 run particle minecraft:sculk_soul ~ ~0.2 ~ 1 0.1 2 0.01 1'])
    sp = rel(PAL.SPAWN)
    tp_ = rel(PAL.TOMB)
    off = (sp[0] - tp_[0], sp[1] - tp_[1], sp[2] - tp_[2])
    fn('p169/tomb/wake', ['scoreboard players set @s bm.omst 1', 'scoreboard players set @s bm.omt 0',
                          'execute as @e[type=minecraft:marker,tag=bm.omnpc,distance=..30] at @s run function bm:p169/npc/remove',
                          f'execute positioned ~{off[0]:.1f} ~{off[1]:.1f} ~{off[2]:.1f} run function bm:p169/b/spawn'])


# ------------------------------------------------------------------------------------------------ the boss
def bsel(p=None):
    return '@e[type=minecraft:item_display,tag=bm.ombsel' + (f',tag=bm.omb_{p}]' if p else ']')


def _boss(C):
    G, fn, tick, fast, second, title, tellraw = C.G, C.fn, C.tick, C.fast, C.second, C.title, C.tellraw
    omchat, apchat = C.omchat, C.apchat
    G.FUNCS['load'][-1:-1] = ['bossbar add bm:omegab {text:"King Omega, the King of the Dead",color:"blue"}', 'bossbar set bm:omegab color blue',
                              'bossbar set bm:omegab style notched_10']
    pl = lambda r: f'@a[distance=..{r},gamemode=!creative,gamemode=!spectator]'
    me = '@e[type=minecraft:husk,tag=bm.omme,limit=1]'
    at = lambda t, cmd: f'execute if score @s bm.omt matches {t} run {cmd}'
    aud = '@a[distance=..48]'
    hit = lambda n, who: f'execute as {who} run damage @s {n} minecraft:mob_attack by {me}'
    bface = lambda e: (f'data modify entity {bsel("head")[:-1]},limit=1] item.components."minecraft:custom_model_data" set value {{strings:["{e}"]}}' if e
                       else f'data remove entity {bsel("head")[:-1]},limit=1] item.components."minecraft:custom_model_data"')
    # ---- the rig
    fn('p169/b/rig', [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(OArt, p, ["bm.omb", f"bm.omb_{p}", "bm.ombnew"], SB, scale0=True, extra={"view_range": F(3.0), "brightness": {"block": Int(13), "sky": Int(13)}, "shadow_radius": F(1.6 if p == "coil" else 0.0), "shadow_strength": F(0.5)})}'
                      for p in OArt.PARTS] +
       ['scoreboard players operation @e[type=minecraft:item_display,tag=bm.ombnew,distance=..1] bm.omid = @s bm.omid',
        'tag @e[type=minecraft:item_display,tag=bm.ombnew,distance=..1] add bm.ombsel', 'tag @e[type=minecraft:item_display,tag=bm.ombnew] remove bm.ombnew'])
    fn('p169/b/rerig', ['scoreboard players operation #oid bm.rng = @s bm.omid',
                        'execute as @e[type=minecraft:item_display,tag=bm.omb] if score @s bm.omid = #oid bm.rng run kill @s', 'function bm:p169/b/rig',
                        'function bm:p169/b/pose/battle'])
    fn('p169/b/place', RF.place(OArt, UB, bsel))
    for name in DUR_B:
        fn(f'p169/b/pose/{name}', RF.pose(OArt, POSES[name], SB, DUR_B[name], bsel))
    fn('p169/b/hide', [f'execute as {bsel(p)} run data merge entity @s {{start_interpolation:0,interpolation_duration:4,transformation:{{scale:[0f,0f,0f]}}}}' for p in OArt.PARTS])
    fn('p169/b/unrig', ['scoreboard players operation #oid bm.rng = @s bm.omid',
                        'execute as @e[type=minecraft:item_display,tag=bm.omb,distance=..48] if score @s bm.omid = #oid bm.rng run kill @s'])

    # ---- the host
    bnbt = {'Tags': ['bm.omboss', 'bm.omcalm', 'bm.npc', 'bm.omnew', 'bm.seen'], 'PersistenceRequired': B(1), 'Silent': B(1), 'NoAI': B(1), 'Invulnerable': B(1),
            'CustomName': T('King Omega', OM_C, bold=True), 'IsBaby': B(0), 'CanBreakDoors': B(0), 'DeathLootTable': 'minecraft:empty', 'Health': F(BOSS_HP),
            'attributes': [{'id': f'minecraft:{k}', 'base': D(v)} for k, v in dict(scale=2.6, max_health=BOSS_HP, attack_damage=10, armor=14, armor_toughness=8,
                                                                                  movement_speed=0.24, follow_range=40, knockback_resistance=1.0,
                                                                                  spawn_reinforcements=0.0, step_height=2.0, jump_strength=0.0).items()],
            'active_effects': [{'id': f'minecraft:{e}', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}
                               for e in ('invisibility', 'fire_resistance', 'water_breathing')],
            'drop_chances': {s: F(0.0) for s in ('mainhand', 'offhand', 'head', 'chest', 'legs', 'feet')},
            # (2.82: a blow big enough to skip past his six-percent yield would kill him outright - no peace, no Monocle for anyone. An
            #  unseen ward in his off hand takes that blow - he's left at a sliver, and yields)
            'equipment': {'offhand': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:om_guard',
                                                                                              'minecraft:death_protection': {'death_effects': []}}}}}
    fn('p169/b/spawn', [f'summon minecraft:husk ~ ~ ~ {snbt(bnbt)}', 'execute as @e[type=minecraft:husk,tag=bm.omnew,distance=..2,limit=1] at @s run function bm:p169/b/init'])
    fn('p169/b/init', ['tag @s remove bm.omnew', 'tp @s ~ ~ ~ 180 0', 'scoreboard players add #omn bm.omid 1', 'scoreboard players operation @s bm.omid = #omn bm.omid',
                       'scoreboard players set @s bm.omt 0', 'scoreboard players set @s bm.omc 40', 'scoreboard players set @s bm.omph 1', 'scoreboard players set @s bm.omr 0',
                       'scoreboard players set @s bm.omlone 0', 'scoreboard players set @s bm.oms -1', 'scoreboard players set @s bm.omf 0',
                       'bossbar set bm:omegab visible false', 'function bm:p169/b/rig', 'team join bm.blood @s',
                       'scoreboard players set @s bm.omatk 9', 'execute if score #omfree bm.omwin matches 1 run scoreboard players set @s bm.omatk 8',
                       'execute if score #omfree bm.omwin matches 1 run tag @s add bm.omre', 'tag @e[tag=bm.ombsel] remove bm.ombsel'])
    tick.append('execute as @e[type=minecraft:husk,tag=bm.omboss] at @s run function bm:p169/b/tick')
    fn('p169/b/tick', ['scoreboard players operation #oid bm.rng = @s bm.omid',
                       'execute as @e[type=minecraft:item_display,tag=bm.omb,distance=..40] if score @s bm.omid = #oid bm.rng run tag @s add bm.ombsel',
                       f'execute unless entity {bsel("coil")} run function bm:p169/b/rerig',
                       f'execute unless entity {bsel("flame")} run function bm:p169/b/rerig',
                       'execute unless score @s bm.omatk matches 7 rotated as @s rotated ~ 0 run function bm:p169/b/place',
                       'execute if score @s bm.omph matches 1..2 unless score @s bm.omatk matches 7..9 unless score @s bm.omatk matches 20 run function bm:p169/b/thresholds',
                       'tag @s add bm.omme',
                       'execute if score @s bm.omatk matches 1.. run function bm:p169/b/attack',
                       'execute unless score @s bm.omatk matches 1.. run function bm:p169/b/move',
                       'execute unless score @s bm.omatk matches 1.. run function bm:p169/b/mind',
                       'tag @s remove bm.omme', 'tag @e[tag=bm.ombsel] remove bm.ombsel'])
    # (his health, tick by tick: beaten low he yields at once; at half, Grief; at three-quarters, his Ghost Guard)
    fn('p169/b/thresholds', ['execute store result score #hp bm.rng run data get entity @s Health 100',
                             'execute store result score #mx bm.rng run attribute @s minecraft:max_health get 100',
                             'scoreboard players operation #q bm.rng = #mx bm.rng', 'scoreboard players operation #q bm.rng /= #100 bm.rng',
                             'scoreboard players operation #q bm.rng *= #6 bm.rng',
                             'execute if score #hp bm.rng <= #q bm.rng run return run function bm:p169/b/start {a:20}',
                             'scoreboard players operation #q bm.rng = #mx bm.rng', 'scoreboard players operation #q bm.rng /= #2 bm.rng',
                             'execute if score @s bm.omph matches 1 if score #hp bm.rng <= #q bm.rng run return run function bm:p169/b/start {a:7}',
                             'scoreboard players operation #q bm.rng = #mx bm.rng', 'scoreboard players operation #q bm.rng /= #4 bm.rng',
                             'scoreboard players operation #q bm.rng *= #3 bm.rng',
                             'execute if score @s bm.omr matches 0 if score #hp bm.rng <= #q bm.rng unless score @s bm.omatk matches 1.. run function bm:p169/b/start {a:6}'])
    fn('p169/b/start', ['$scoreboard players set @s bm.omatk $(a)', 'scoreboard players set @s bm.omt 0', 'scoreboard players set @s bm.omc 3',
                        'execute if score @s bm.omph matches 2 run scoreboard players set @s bm.omc 2'])
    fn('p169/b/done', ['scoreboard players set @s bm.omatk 0', 'scoreboard players set @s bm.oms -1', 'scoreboard players set @s bm.omf 0'])
    # moving: the husk's own feet; he glides, or hovers and breathes
    fn('p169/b/move', ['scoreboard players add @s bm.omf 1', 'scoreboard players set #st bm.rng 0', 'execute if predicate bm:p21/walking run scoreboard players set #st bm.rng 1',
                       'execute unless score @s bm.oms = #st bm.rng run scoreboard players set @s bm.omf 0', 'scoreboard players operation @s bm.oms = #st bm.rng',
                       'scoreboard players operation #f bm.rng = @s bm.omf',
                       'execute if score #st bm.rng matches 1 run scoreboard players operation #f bm.rng %= #24 bm.rng',
                       'execute if score #st bm.rng matches 0 run scoreboard players operation #f bm.rng %= #60 bm.rng',
                       'execute if score #st bm.rng matches 1 if score #f bm.rng matches 0 run function bm:p169/b/pose/glide_a',
                       'execute if score #st bm.rng matches 1 if score #f bm.rng matches 6 run function bm:p169/b/pose/glide_m',
                       'execute if score #st bm.rng matches 1 if score #f bm.rng matches 12 run function bm:p169/b/pose/glide_b',
                       'execute if score #st bm.rng matches 1 if score #f bm.rng matches 18 run function bm:p169/b/pose/glide_m',
                       'execute if score #st bm.rng matches 0 if score #f bm.rng matches 0 run function bm:p169/b/pose/battle',
                       'execute if score #st bm.rng matches 0 if score #f bm.rng matches 30 run function bm:p169/b/pose/idle_b',
                       'execute if score #f bm.rng matches 0 run particle minecraft:soul ~ ~3 ~ 1.2 2 1.2 0.02 3'])
    # the leash: never out of his throne room
    tb = rel(PAL.TOMB); sp = rel(PAL.SPAWN)
    second.append(f'execute as @e[type=minecraft:marker,tag=bm.omtomb] at @s as @e[type=minecraft:husk,tag=bm.omboss,distance=17..60] run tp @s ~{sp[0] - tb[0]:.1f} ~{sp[1] - tb[1]:.1f} ~{sp[2] - tb[2]:.1f}')

    # ---- the mind: every second he isn't mid-attack, maybe one
    fn('p169/b/mind', ['scoreboard players remove @s bm.omc 1', 'execute if score @s bm.omc matches 1.. run return 0', 'scoreboard players set @s bm.omc 20',
                       'execute store result score #r bm.rng run random value 1..100',
                       'execute store result score #vx bm.rng if entity @e[type=minecraft:vex,tag=bm.ssvex,distance=..48]',
                       f'execute if score @s bm.omph matches 2 if score #r bm.rng matches 1..25 if entity {pl(30)} run return run function bm:p169/b/start {{a:5}}',
                       f'execute if score #r bm.rng matches 1..16 if entity {pl(24)} run return run function bm:p169/b/start {{a:4}}',
                       f'execute if score #r bm.rng matches 17..28 if score #vx bm.rng matches ..1 run return run function bm:p169/b/start {{a:3}}',
                       f'execute if score #r bm.rng matches 29..70 if entity {pl(6)} run return run function bm:p169/b/start {{a:1}}',
                       f'execute if entity {pl(28)} run return run function bm:p169/b/start {{a:2}}'])
    names = {1: 'claw', 2: 'flame', 3: 'serpents', 4: 'pillars', 5: 'volley', 6: 'guard', 7: 'grief', 8: 'rematch', 9: 'coming', 20: 'peace'}
    fn('p169/b/attack', ['scoreboard players add @s bm.omt 1'] + [f'execute if score @s bm.omatk matches {n} run function bm:p169/b/a_{w}' for n, w in names.items()])
    face_t = 'execute facing entity @p[gamemode=!creative,gamemode=!spectator] feet run tp @s ~ ~ ~ ~ 0'
    # CLAW: wound up to his right - a raking sweep across his front
    fn('p169/b/a_claw', [at(1, face_t), at(1, 'function bm:p169/b/pose/claw_up'), at(1, 'playsound minecraft:entity.ravager.attack hostile @a[distance=..32] ~ ~ ~ 1 0.5'),
                         at(8, 'function bm:p169/b/pose/claw'), at(9, 'function bm:p169/b/claw_hit'), at(20, 'function bm:p169/b/pose/battle'), at('26..', 'function bm:p169/b/done')])
    fn('p169/b/claw_hit', [f'particle minecraft:sweep_attack ^{x} ^3 ^{z} 0 0 0 0 1' for x, z in ((-3, 2), (-1.5, 3.5), (0, 4), (1.5, 3.5), (3, 2))] +
       ['particle minecraft:soul ^ ^3 ^3 2 1 1 0.03 16', 'playsound minecraft:entity.player.attack.sweep hostile @a[distance=..32] ~ ~ ~ 1.4 0.5',
        f'execute rotated as @s rotated ~ 0 positioned ^ ^ ^3 run {hit(18, pl(4.5))}'])
    # SOUL FLAME: the fire off his tail, thrown - it bursts where it lands
    fn('p169/b/a_flame', [at(1, face_t), at(1, 'function bm:p169/b/pose/flame_up'), at(1, 'playsound minecraft:item.firecharge.use hostile @a[distance=..32] ~ ~ ~ 1 0.5'),
                          at('2..11', f'execute rotated as @s rotated ~ 0 positioned {loc(FLAME_AT)} run particle minecraft:soul_fire_flame ~ ~ ~ 0.4 0.4 0.4 0.02 4'),
                          at(12, 'function bm:p169/b/pose/flame_swing'), at(14, 'function bm:p169/b/pose/flame_throw'),
                          at(15, f'execute rotated as @s rotated ~ 0 positioned {loc(FLAME_AT)} facing entity @p[gamemode=!creative,gamemode=!spectator] eyes run function bm:p169/b/fl_make'),
                          at(26, 'function bm:p169/b/pose/battle'), at('30..', 'function bm:p169/b/done')])
    fn('p169/b/a_volley', [at(1, 'function bm:p169/b/pose/flame_up'), at(1, 'playsound minecraft:entity.blaze.shoot hostile @a[distance=..32] ~ ~ ~ 1 0.5'),
                           at(10, 'function bm:p169/b/pose/flame_throw'), at(16, 'function bm:p169/b/pose/flame_up'), at(22, 'function bm:p169/b/pose/flame_throw'),
                           at(28, 'function bm:p169/b/pose/flame_up'), at(34, 'function bm:p169/b/pose/flame_throw')] +
       [at(t, f'execute rotated as @s rotated ~ 0 positioned {loc(FLAME_AT)} facing entity @r[distance=..30,gamemode=!creative,gamemode=!spectator] eyes run function bm:p169/b/fl_make')
        for t in (11, 23, 35)] + [at(44, 'function bm:p169/b/pose/battle'), at('48..', 'function bm:p169/b/done')])
    fn('p169/b/fl_make', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.omfl","bm.omflnew"]}', 'tp @e[type=minecraft:marker,tag=bm.omflnew,distance=..1] ~ ~ ~ ~ ~',
                          'scoreboard players set @e[type=minecraft:marker,tag=bm.omflnew,distance=..1] bm.omt 0', 'tag @e[tag=bm.omflnew] remove bm.omflnew',
                          'playsound minecraft:entity.ghast.shoot hostile @a[distance=..32] ~ ~ ~ 0.8 0.6'])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.omfl] at @s run function bm:p169/b/fl_tick')
    fn('p169/b/fl_tick', ['scoreboard players add @s bm.omt 1', 'tp @s ^ ^ ^0.8', 'particle minecraft:soul_fire_flame ~ ~ ~ 0.15 0.15 0.15 0.01 4',
                          'particle minecraft:soul ~ ~ ~ 0.1 0.1 0.1 0.01 1',
                          'execute if entity @a[distance=..1.6,gamemode=!creative,gamemode=!spectator] run return run function bm:p169/b/fl_burst',
                          'execute unless block ~ ~ ~ #bm:grap_pass run return run function bm:p169/b/fl_burst',
                          'execute if score @s bm.omt matches 40.. run function bm:p169/b/fl_burst'])
    fn('p169/b/fl_burst', ['particle minecraft:soul_fire_flame ~ ~ ~ 1.2 1.2 1.2 0.1 60', 'particle minecraft:flash{color:[0.4,0.85,1.0,1.0]} ~ ~ ~ 0 0 0 0 1',
                           'playsound minecraft:entity.generic.explode hostile @a[distance=..32] ~ ~ ~ 0.8 1.4',
                           'execute as @a[distance=..3,gamemode=!creative,gamemode=!spectator] run damage @s 14 minecraft:mob_attack by @e[type=minecraft:husk,tag=bm.omboss,sort=nearest,limit=1]',
                           'effect give @a[distance=..3,gamemode=!creative,gamemode=!spectator] minecraft:slowness 2 1', 'kill @s'])
    # SOUL SERPENTS: claws low, palms up - two of them out of the dark
    vexn = {'Tags': ['bm.sshost', 'bm.ssvex', 'bm.ssnew', 'bm.seen'], 'PersistenceRequired': B(1), 'Silent': B(0), 'CustomName': T('Soul Serpent', SOUL),
            'DeathLootTable': 'minecraft:empty', 'Health': F(14), 'attributes': [{'id': 'minecraft:max_health', 'base': D(14)}, {'id': 'minecraft:attack_damage', 'base': D(5)}],
            'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}]}
    fn('p169/b/a_serpents', [at(1, 'function bm:p169/b/pose/summon'), at(1, bface('shock')),
                             at(1, 'playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..48] ~ ~ ~ 1.5 0.7'),
                             at('2..12', 'particle minecraft:soul ~ ~3 ~ 2 1 2 0.05 6'),
                             at(12, f'execute positioned ^2.5 ^3 ^1.5 run summon minecraft:vex ~ ~ ~ {snbt(vexn)}'),
                             at(12, f'execute positioned ^-2.5 ^3 ^1.5 run summon minecraft:vex ~ ~ ~ {snbt(vexn)}'),
                             at(12, 'execute as @e[type=minecraft:vex,tag=bm.ssnew,distance=..8] at @s run function bm:p169/ss/born'),
                             at(14, omchat('Up, little ones! Show them how we play!', aud)),
                             at(20, bface(None)), at(24, 'function bm:p169/b/pose/battle'), at('28..', 'function bm:p169/b/done')])
    tick.append('execute as @e[type=minecraft:vex,tag=bm.ssvex] at @s run function bm:p169/ss/vex')
    fn('p169/ss/vex', ['scoreboard players set #sst bm.rng 0', 'execute if entity @a[distance=..3] run scoreboard players set #sst bm.rng 2',
                       'execute if score @s bm.sss matches 3 if score @s bm.ssf matches ..19 run scoreboard players set #sst bm.rng 3',
                       'function bm:p169/ss/state', 'execute rotated as @s rotated ~ 0 positioned ~ ~-0.5 ~ run function bm:p169/ss/at'])
    second.append('execute as @e[type=minecraft:vex,tag=bm.ssvex] at @s unless entity @e[type=minecraft:husk,tag=bm.omboss,distance=..64] run function bm:p169/ss/go')
    # (a serpent's bite on you: it cackles)
    G.wjson('bm/advancement/p169/bitten.json', {'criteria': {'h': {'trigger': 'minecraft:entity_hurt_player', 'conditions': {'damage': {'source_entity': {'minecraft:entity_type': 'minecraft:vex', 'minecraft:nbt': '{Tags:["bm.ssvex"]}'}}}}},
                                               'rewards': {'function': 'bm:p169/bitten'}})
    fn('p169/bitten', ['advancement revoke @s only bm:p169/bitten',
                       'execute at @s as @e[type=minecraft:vex,tag=bm.ssvex,distance=..5,sort=nearest,limit=1] at @s run function bm:p169/ss/giggle'])
    fn('p169/ss/giggle', ['scoreboard players set #sst bm.rng 3', 'function bm:p169/ss/state', 'playsound minecraft:entity.allay.ambient_with_item hostile @a[distance=..16] ~ ~ ~ 0.6 1.8'])
    # THE PILLARS OF THE DEAD: a ring of soul fire under each of you - a breath later it erupts (nothing turns it: step out)
    fn('p169/b/a_pillars', [at(1, 'function bm:p169/b/pose/rally'), at(1, bface('roar')), at(1, 'playsound minecraft:entity.warden.roar hostile @a[distance=..48] ~ ~ ~ 1 0.8'),
                            at(4, f'execute as {pl(24)} at @s run summon minecraft:marker ~ ~ ~ {{Tags:["bm.ompil"]}}'), at(4, omchat('KNEEL!', aud)),
                            at(20, bface(None)), at(24, 'function bm:p169/b/pose/battle'), at('30..', 'function bm:p169/b/done')])
    ring = lambda r, n, y: [f'particle minecraft:soul_fire_flame ~{r * math.cos(2 * math.pi * k / n):.2f} ~{y} ~{r * math.sin(2 * math.pi * k / n):.2f} 0 0.02 0 0 1' for k in range(n)]
    tick.append('execute as @e[type=minecraft:marker,tag=bm.ompil] at @s run function bm:p169/b/pil')
    fn('p169/b/pil', ['scoreboard players add @s bm.omt 1', 'execute if score @s bm.omt matches ..29 run function bm:p169/b/pil_ring',
                      'execute if score @s bm.omt matches 30 run function bm:p169/b/pil_go', 'execute if score @s bm.omt matches 30..36 run particle minecraft:soul_fire_flame ~ ~2 ~ 0.6 2 0.6 0.08 20',
                      'execute if score @s bm.omt matches 38.. run kill @s'])
    fn('p169/b/pil_ring', ring(1.8, 16, 0.1) + ['particle minecraft:soul ~ ~0.2 ~ 1 0 1 0 1'])
    fn('p169/b/pil_go', ['playsound minecraft:entity.evoker_fangs.attack hostile @a[distance=..24] ~ ~ ~ 1 0.5', 'playsound minecraft:block.soul_sand.break hostile @a[distance=..24] ~ ~ ~ 1 0.5',
                         'particle minecraft:sculk_soul ~ ~1 ~ 0.6 1.5 0.6 0.05 30',
                         'execute positioned ~-1.8 ~ ~-1.8 as @a[dx=2.6,dy=3,dz=2.6,gamemode=!creative,gamemode=!spectator] run function bm:p169/b/pilhit'])
    fn('p169/b/pilhit', ['damage @s 18 minecraft:magic', 'effect give @s minecraft:levitation 1 2'])
    # HIS GHOST GUARD (three-quarters): soldiers of the old palace guard, up out of the floor
    gnbt = {'Tags': ['bm.omguard', 'bm.seen'], 'PersistenceRequired': B(1), 'CustomName': T('Ghost of the Guard', SOUL), 'DeathLootTable': 'minecraft:empty',
            'drop_chances': {s: F(0.0) for s in ('mainhand', 'offhand', 'head', 'chest', 'legs', 'feet')},
            'equipment': {'head': {'id': 'minecraft:chainmail_helmet', 'count': Int(1)}, 'mainhand': {'id': 'minecraft:iron_sword', 'count': Int(1)}}}
    fn('p169/b/a_guard', [at(1, 'scoreboard players set @s bm.omr 1'), at(1, 'function bm:p169/b/pose/rally'), at(1, bface('roar')),
                          at(1, 'playsound minecraft:event.raid.horn hostile @a[distance=..64] ~ ~ ~ 1 0.6'), at(2, omchat('GUARD! To your king!', aud))] +
       [at(14, f'execute positioned ^{x} ^ ^{z} run summon minecraft:stray ~ ~ ~ {snbt(gnbt)}') for x, z in ((4, 2), (-4, 2), (4, -3), (-4, -3))] +
       [at(14, 'execute as @e[type=minecraft:stray,tag=bm.omguard,distance=..8] at @s run particle minecraft:soul ~ ~1 ~ 0.4 0.8 0.4 0.03 20'),
        at(24, bface(None)), at(26, 'function bm:p169/b/pose/battle'), at('30..', 'function bm:p169/b/done')])
    second.append('execute as @e[type=minecraft:stray,tag=bm.omguard] at @s unless entity @e[type=minecraft:husk,tag=bm.omboss,distance=..64] run function bm:p169/b/guard_go')
    fn('p169/b/guard_go', ['particle minecraft:soul ~ ~1 ~ 0.3 0.6 0.3 0.03 16', 'tp @s ~ -400 ~', 'kill @s'])
    # GRIEF (half): a wail, the dark - he vanishes, and strikes from behind three times; then he shows himself, faster
    behind = (f'execute as @r[distance=..32,gamemode=!creative,gamemode=!spectator] at @s rotated ~ 0 positioned ^ ^ ^-3.2 '
              f'if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run tp {me} ~ ~ ~ facing entity @s feet')
    grief = [at(1, 'scoreboard players set @s bm.omph 2'), at(1, 'data merge entity @s {NoAI:1b,Invulnerable:1b}'), at(1, 'function bm:p169/b/pose/shock'), at(1, bface('roar')),
             at(8, 'function bm:p169/b/pose/rally'),
             at(1, 'playsound minecraft:entity.ghast.scream hostile @a[distance=..64] ~ ~ ~ 1.5 0.5'), at(1, 'playsound minecraft:entity.warden.heartbeat hostile @a[distance=..64] ~ ~ ~ 1.5 0.5'),
             at(2, omchat('Three hundred years in the dark - and you come to dance on my GRAVE?', aud)),
             at(10, 'effect give @a[distance=..48] minecraft:darkness 9 0 true'), at(14, 'function bm:p169/b/hide'),
             at(14, 'particle minecraft:soul ~ ~3 ~ 1.5 2.5 1.5 0.06 80'), at(14, 'tag @s add bm.omgone')]
    for k, t0 in enumerate((40, 70, 100)):
        grief += [at(t0, behind), at(t0, 'function bm:p169/b/pose/claw_up'), at(t0, 'playsound minecraft:entity.vex.charge hostile @a[distance=..32] ~ ~ ~ 1.5 0.5'),
                  at(t0 + 6, 'function bm:p169/b/pose/claw'), at(t0 + 7, 'function bm:p169/b/claw_hit'), at(t0 + 16, 'function bm:p169/b/hide')]
    grief += [at(126, f'execute as @e[type=minecraft:marker,tag=bm.omtomb,distance=..40,sort=nearest,limit=1] at @s run tp {me} ~{sp[0] - tb[0]:.1f} ~{sp[1] - tb[1]:.1f} ~{sp[2] - tb[2]:.1f}'),
              at(128, 'function bm:p169/b/pose/rally'), at(128, 'tag @s remove bm.omgone'), at(128, 'particle minecraft:soul_fire_flame ~ ~3 ~ 2 2.5 2 0.1 80'),
              at(128, 'playsound minecraft:entity.wither.spawn hostile @a[distance=..64] ~ ~ ~ 0.6 0.8'),
              at(132, omchat('...I am not finished with you.', aud)), at(140, bface(None)),
              at(140, 'data merge entity @s {NoAI:0b,Invulnerable:0b}'), at(140, 'function bm:p169/b/pose/battle'), at('144..', 'function bm:p169/b/done')]
    fn('p169/b/a_grief', grief)
    # (while he's vanished the rig mustn't follow the host about: it stays hidden where it is - the tick skips placing during a=7 and
    #  places it only when he strikes)
    G.FUNCS['p169/b/tick'].insert(5, 'execute if score @s bm.omatk matches 7 unless entity @s[tag=bm.omgone] rotated as @s rotated ~ 0 run function bm:p169/b/place')
    G.FUNCS['p169/b/a_grief'] += [f'execute if entity @s[tag=bm.omgone] if score @s bm.omt matches {t0}..{t0 + 15} rotated as @s rotated ~ 0 run function bm:p169/b/place' for t0 in (40, 70, 100)]

    # ---- HIS COMING (a=9; 14 s): the dark, a heartbeat, soul fire spiralling out of the floor, the six emblems pouring their light
    #      into it - then claws through the flagstones, and he crawls up out of the ground and roars
    streams = []
    for i in range(6):
        x, y, z = PAL.socket_pos(i)
        dx, dy, dz = x - PAL.SPAWN[0], y + 0.8 - PAL.SPAWN[1], z - PAL.SPAWN[2]
        streams += [f'particle minecraft:dust{{color:[{int(EMB_COL[EMB[i]][1:3], 16) / 255:.2f},{int(EMB_COL[EMB[i]][3:5], 16) / 255:.2f},{int(EMB_COL[EMB[i]][5:7], 16) / 255:.2f}],scale:1.1}} '
                    f'~{dx * k / 8:.2f} ~{dy * k / 8 + 0.6:.2f} ~{dz * k / 8:.2f} 0.05 0.05 0.05 0 1 force @a[distance=..64]' for k in range(1, 8)]
    fn('p169/b/streams', streams)
    fn('p169/b/vx', ['tp @s ~ ~ ~ ~14 0'] +
       [f'execute rotated as @s rotated ~{arm + 40 * k} 0 positioned ^ ^{0.2 + 0.7 * k:.1f} ^{3.6 - 0.45 * k:.2f} run particle minecraft:soul_fire_flame ~ ~ ~ 0.05 0.1 0.05 0.01 2 force @a[distance=..64]'
        for arm in (0, 120, 240) for k in range(6)] + ['particle minecraft:sculk_soul ~ ~0.3 ~ 2.5 0.2 2.5 0.02 3 force @a[distance=..64]'])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.omvx] at @s run function bm:p169/b/vx')
    second.append('execute as @e[type=minecraft:marker,tag=bm.omvx] at @s unless entity @e[type=minecraft:husk,tag=bm.omboss,distance=..4] run kill @s')
    beats = (1, 16, 30, 42, 52, 60, 68, 75, 81, 86, 91, 95, 99, 103)
    burst = ['particle minecraft:flash{color:[0.4,0.85,1.0,1.0]} ~ ~4 ~ 0 0 0 0 1 force @a[distance=..64]',
             'particle minecraft:soul_fire_flame ~ ~3 ~ 1 2 1 0.5 200 force @a[distance=..64]', 'particle minecraft:soul ~ ~3 ~ 2 2 2 0.3 120 force @a[distance=..64]',
             'playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..64] ~ ~ ~ 1.5 0.6', 'playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..64] ~ ~ ~ 1.5 0.7']
    fn('p169/b/burst', burst)
    fn('p169/b/a_coming', [at(1, 'effect give @a[distance=..48] minecraft:darkness 7 0 true'), at(1, 'playsound minecraft:block.beacon.deactivate hostile @a[distance=..64] ~ ~ ~ 2 0.5'),
                           at(1, 'playsound minecraft:ambient.soul_sand_valley.mood ambient @a[distance=..64] ~ ~ ~ 2 0.5'), at(1, 'function bm:p169/b/hide'),
                           at(1, 'summon minecraft:marker ~ ~ ~ {Tags:["bm.omvx"]}')] +
       [at(t, f'playsound minecraft:entity.warden.heartbeat hostile @a[distance=..64] ~ ~ ~ {0.8 + j * 0.08:.2f} {0.5 + j * 0.03:.2f}') for j, t in enumerate(beats)] +
       [at(t, 'function bm:p169/b/streams') for t in range(10, 60, 4)] +
       [at(t, 'playsound minecraft:entity.allay.death hostile @a[distance=..64] ~ ~ ~ 0.6 0.4') for t in (20, 44)] +
       [at(30, 'playsound minecraft:entity.ghast.ambient hostile @a[distance=..64] ~ ~ ~ 1 0.4'),
        at(40, 'particle minecraft:block{block_state:"minecraft:deepslate_tiles"} ~ ~0.2 ~ 1.6 0.1 1.6 0 80 force @a[distance=..64]'),
        at(40, 'playsound minecraft:block.deepslate.break block @a[distance=..64] ~ ~ ~ 2 0.5'),
        at(60, 'function bm:p169/b/pose/crawl_a'), at(60, bface('roar')), at(60, 'playsound minecraft:entity.warden.emerge hostile @a[distance=..64] ~ ~ ~ 2 0.6'),
        at('60..120', 'particle minecraft:block{block_state:"minecraft:deepslate_tiles"} ~ ~0.2 ~ 1.4 0.1 1.4 0 6 force @a[distance=..64]'),
        at(70, 'playsound minecraft:entity.warden.dig hostile @a[distance=..64] ~ ~ ~ 2 0.6'),
        at(84, 'function bm:p169/b/pose/crawl_b'), at(84, 'playsound minecraft:block.gravel.break block @a[distance=..64] ~ ~ ~ 2 0.4'),
        at(90, 'playsound minecraft:entity.zombie.break_wooden_door hostile @a[distance=..64] ~ ~ ~ 1 0.5'),
        at(108, 'function bm:p169/b/pose/crawl_c'), at(108, 'playsound minecraft:entity.warden.dig hostile @a[distance=..64] ~ ~ ~ 2 0.5'),
        at(128, 'function bm:p169/b/pose/battle'), at(136, 'function bm:p169/b/pose/rally'), at(136, 'function bm:p169/b/burst'),
        at(136, 'kill @e[type=minecraft:marker,tag=bm.omvx,distance=..4]'),
        at(136, 'title @a[distance=..48] times 6 60 20'), at(136, title('@a[distance=..48]', 'title', T('KING OMEGA', OM_C, bold=True))),
        at(136, title('@a[distance=..48]', 'subtitle', T('the King of the Dead', OM_LINE))),
        at(150, 'function bm:p169/b/pose/idle_a'), at(150, bface('shock')),
        at(152, omchat('Who dares disturb-- ...YOU.', aud)),
        at(182, omchat('Of all the tombs in all the world, little brother, you slither into MINE. With my own crowns of conquest, no less!', aud)),
        at(224, apchat('Hsss... hello, Omega. You look... dead.', aud)), at(224, bface(None)),
        at(252, 'function bm:p169/b/pose/rally'), at(252, bface('roar')),
        at(252, omchat('And WHOSE fault is THAT? Get out of my house. GET OUT OF MY HOUSE!', aud)),
        at(252, 'playsound minecraft:entity.ravager.roar hostile @a[distance=..64] ~ ~ ~ 2 0.6'), at(270, bface(None)), at(272, 'function bm:p169/b/begin')])
    fn('p169/b/a_rematch', [at(1, 'function bm:p169/b/pose/bow'), at(1, 'function bm:p169/b/burst'),
                            at(4, omchat('A rematch, little brother? Very well - for old times\' sake. Do try to keep up.', aud)),
                            at(40, 'function bm:p169/b/pose/rally'), at(40, 'playsound minecraft:entity.ravager.roar hostile @a[distance=..64] ~ ~ ~ 2 0.7'),
                            at(56, 'function bm:p169/b/begin')])
    fn('p169/b/begin', ['data merge entity @s {NoAI:0b,Invulnerable:0b}', 'tag @s remove bm.omcalm', 'tag @s remove bm.npc', 'bossbar set bm:omegab visible true',
                        'function bm:p169/b/done', 'scoreboard players set @s bm.omc 30', 'function bm:p169/b/pose/battle'])

    # ---- HIS PEACE (a=20): beaten low, he kneels - and the brothers talk
    calm = ['data merge entity @s {NoAI:1b,Invulnerable:1b}', 'tag @s add bm.omcalm', 'tag @s add bm.npc', 'bossbar set bm:omegab visible false',
            'execute as @e[type=minecraft:vex,tag=bm.ssvex,distance=..64] at @s run function bm:p169/ss/go',
            'execute as @e[type=minecraft:stray,tag=bm.omguard,distance=..64] at @s run function bm:p169/b/guard_go',
            'kill @e[type=minecraft:marker,tag=bm.ompil,distance=..64]', 'kill @e[type=minecraft:marker,tag=bm.omfl,distance=..64]',
            'function bm:p169/b/pose/tired', bface('tired'), 'playsound minecraft:entity.wither.death hostile @a[distance=..64] ~ ~ ~ 0.4 1.6',
            'particle minecraft:soul ~ ~2 ~ 2 1.5 2 0.04 60']
    first = [at(1, f) for f in calm] + [at(16, 'function bm:p169/b/pose/kneel'),
        at(20, omchat('Enough... enough. I yield, little brother.', aud)),
        at(60, apchat('Yield? YOU? The great King Omega - beaten by his baby brother?', aud)),
        at(100, omchat('Beaten by your FRIENDS, Apophiss. You never could win a fight on your own.', aud)),
        at(140, apchat('...Hss. I did not come to fight. I came to say a thing. It is not an easy thing to say.', aud)),
        at(185, apchat('The war. The palace. You. I was wrong, brother. I wanted everything - and I broke the only thing that mattered.', aud)),
        at(235, 'function bm:p169/b/pose/welcome'), at(235, bface('warm')),
        at(236, omchat('Three hundred years I waited to hear that. You could have WRITTEN.', aud)),
        at(280, omchat('You have new friends - good ones, by the look of them. Then I shall walk with you all. Someone must keep you honest.', aud)),
        at(325, 'function bm:p169/b/pose/monocle'),
        at(326, omchat('Take this, my friends. Wear it, and call - and the King of the Dead will come.', aud)),
        at(330, 'execute as @a[distance=..48,gamemode=!spectator] at @s run function bm:p169/peace/claim'),
        at(370, 'function bm:p169/b/pose/bow'),
        at(372, omchat('And do visit. Pistachio will be insufferable if nobody comes to dinner.', aud)),
        at(410, 'function bm:p169/b/pose/fade'), at(410, 'particle minecraft:soul ~ ~3 ~ 1.5 2.5 1.5 0.05 100'),
        at(410, 'playsound minecraft:block.beacon.power_select ambient @a[distance=..64] ~ ~ ~ 1 0.6'),
        at(428, 'function bm:p169/b/peace_end')]
    again = [at(1, f) for f in calm] + [at(16, 'function bm:p169/b/pose/kneel'),
        at(20, omchat('Ha! Well fought, all of you - WELL fought! My brother\'s friends are worth ten of my old guard.', aud)),
        at(60, 'function bm:p169/b/pose/welcome'), at(60, bface('warm')),
        at(70, 'execute as @a[distance=..48,gamemode=!spectator] at @s run function bm:p169/peace/claim'),
        at(100, omchat('Again tomorrow? I shall have Pistachio set the table.', aud)),
        at(130, 'function bm:p169/b/pose/fade'), at(130, 'particle minecraft:soul ~ ~3 ~ 1.5 2.5 1.5 0.05 100'),
        at(148, 'function bm:p169/b/peace_end')]
    fn('p169/b/a_peace', ['execute unless entity @s[tag=bm.omre] run function bm:p169/b/peace1', 'execute if entity @s[tag=bm.omre] run function bm:p169/b/peace2'])
    fn('p169/b/peace1', first)
    fn('p169/b/peace2', again)
    fn('p169/b/peace_end', ['scoreboard players set #omfree bm.omwin 1', 'function bm:p169/b/unrig',
                            'execute as @e[type=minecraft:marker,tag=bm.omtomb,distance=..40] run scoreboard players set @s bm.omst 2',
                            'tp @s ~ -400 ~', 'kill @s'])
    # (each player in the room when he yields)
    G.wjson('bm/loot_table/chests/p169_hoard.json', {'type': 'minecraft:chest', 'pools': [
        {'rolls': {'min': 3, 'max': 5, 'type': 'minecraft:uniform'}, 'entries': [
            {'type': 'minecraft:item', 'name': n, 'weight': w, 'functions': [{'function': 'minecraft:set_count', 'count': {'min': a, 'max': b, 'type': 'minecraft:uniform'}}]}
            for n, w, a, b in (('minecraft:gold_ingot', 4, 3, 8), ('minecraft:soul_lantern', 3, 2, 4), ('minecraft:diamond', 2, 1, 3), ('minecraft:emerald', 3, 3, 8),
                               ('minecraft:echo_shard', 1, 1, 2), ('minecraft:golden_apple', 2, 1, 2), ('minecraft:experience_bottle', 3, 4, 10))]},
        {'rolls': 1, 'entries': [G.loot_entry('token', G.uni(3, 6))]}]})
    fn('p169/peace/claim', ['scoreboard players add @s bm.omwin 1', 'execute if score @s bm.omwin matches 1 run scoreboard players add @s bm.omfav 60',
                            'execute if score @s bm.omwin matches 2.. run scoreboard players add @s bm.omfav 20',
                            'execute if score @s bm.omwin matches 2.. run loot give @s loot bm:chests/p169_hoard',
                            'execute if score @s bm.omwin matches 2.. run loot give @s loot bm:items/om_monocle',               # (2.87: a rematch won - another Monocle)
                            'function bm:p170/reissue', 'advancement grant @s only bm:story/om_peace',
                            'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.8 1.0'])
    G.wjson('bm/advancement/story/om_peace.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
            'display': {'icon': {'id': TOTEM, 'components': {'minecraft:item_model': 'bm:om_monocle'}}, 'title': T('The King of the Dead', OM_C),
                        'description': T('Wake King Omega in his tomb - and make peace between the brothers', 'gray'), 'frame': 'challenge', 'show_toast': True,
                        'announce_to_chat': True, 'hidden': False}})

    # ---- every second: the bar, and whether anyone's still here
    second += ['bossbar set bm:omegab players', 'execute as @e[type=minecraft:husk,tag=bm.omboss] at @s run function bm:p169/b/sec']
    fn('p169/b/sec', ['execute store result score #now bm.rng run time query gametime',
                      'execute unless score @s bm.omseen matches 1.. run scoreboard players operation @s bm.omseen = #now bm.rng',
                      'scoreboard players operation #gap bm.rng = #now bm.rng', 'scoreboard players operation #gap bm.rng -= @s bm.omseen',
                      'scoreboard players operation @s bm.omseen = #now bm.rng', 'execute if score #gap bm.rng matches 1200.. at @s run return run function bm:p169/b/leave',
                      'execute store result bossbar bm:omegab value run data get entity @s Health', 'execute store result bossbar bm:omegab max run attribute @s minecraft:max_health get',
                      'execute unless entity @s[tag=bm.omcalm] run bossbar set bm:omegab players @a[distance=..48]',
                      'execute if entity @a[distance=..48,gamemode=!spectator] run scoreboard players set @s bm.omlone 0',
                      'execute unless entity @a[distance=..48,gamemode=!spectator] run scoreboard players add @s bm.omlone 1',
                      'execute if score @s bm.omlone matches 30.. at @s run function bm:p169/b/leave'])
    fn('p169/b/leave', ['bossbar set bm:omegab visible false', 'function bm:p169/b/unrig', 'kill @e[type=minecraft:marker,tag=bm.omvx,distance=..8]',
                        'particle minecraft:soul ~ ~2 ~ 1.5 2 1.5 0.03 40', 'tp @s ~ -400 ~', 'kill @s'])
    G.FUNCS['admin/uninstall'][0:0] = ['bossbar remove bm:omegab', 'kill @e[type=minecraft:item_display,tag=bm.omb]', 'kill @e[type=minecraft:marker,tag=bm.omfl]',
                                       'kill @e[type=minecraft:marker,tag=bm.ompil]', 'kill @e[type=minecraft:marker,tag=bm.omvx]',
                                       'execute as @e[type=minecraft:husk,tag=bm.omboss] at @s run function bm:p169/b/leave',
                                       'kill @e[type=minecraft:interaction,tag=bm.omsock]', 'kill @e[type=minecraft:text_display,tag=bm.omskt]',
                                       'kill @e[type=minecraft:item_display,tag=bm.ome]']
    # (a rig left with no host - he left mid-coming, or was removed)
    second.append('execute as @e[type=minecraft:item_display,tag=bm.omb,tag=bm.omb_coil] at @s run function bm:p169/b/orphan')
    fn('p169/b/orphan', ['scoreboard players operation #oid bm.rng = @s bm.omid',
                         'execute as @e[type=minecraft:husk,tag=bm.omboss,distance=..40] if score @s bm.omid = #oid bm.rng run return 0',
                         'execute as @e[type=minecraft:item_display,tag=bm.omb,distance=..40] if score @s bm.omid = #oid bm.rng run kill @s'])
    # each blow on him: a groan (he's Silent - these are his own)
    G.wjson('bm/advancement/p169/hit.json', {'criteria': {'h': {'trigger': 'minecraft:player_hurt_entity', 'conditions': {'entity': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["bm.omboss"]}'}}]}}}, 'rewards': {'function': 'bm:p169/hit'}})
    fn('p169/hit', ['advancement revoke @s only bm:p169/hit', 'execute at @s as @e[type=minecraft:husk,tag=bm.omboss,distance=..48,limit=1,sort=nearest] at @s run function bm:p169/b/ouch'])
    fn('p169/b/ouch', ['playsound minecraft:entity.wither_skeleton.hurt hostile @a[distance=..32] ~ ~ ~ 0.8 0.5', 'playsound minecraft:entity.allay.hurt hostile @a[distance=..32] ~ ~ ~ 0.6 0.5',
                       'particle minecraft:soul ~ ~3.5 ~ 0.8 1.2 0.8 0.02 6'])
    fn('admin/omega_boss', ['function bm:p169/b/spawn', C.say('King Omega (a test fight: no tomb).', OM_C)])


# ------------------------------------------------------------------------------------------------ the King at court
def nsel(p=None):
    return '@e[type=minecraft:item_display,tag=bm.omnsel' + (f',tag=bm.omn_{p}]' if p else ']')


DUR_N = {'idle_a': 40, 'idle_b': 40, 'monocle': 16, 'bow': 16, 'welcome': 20}
COURT = '^ ^0.9 ^3'                         # (2.88: where he holds court, from his throne's marker - clear of the seat, the purple back and the near pedestal)
# (2.88) at court his tail swings out to his left and leans away from him, the flame held up beside him, clear of his arm (the
# bow's lies out long, so it only swings - leaned, it went through the floor) - see COURT
_TAIL_N = lambda k: RK.qs(('y', -100)) if k == 'bow' else RK.qs(('z', -45), ('y', -80))
NPOSES = {k: dict(POSES[k], tail1=RK.qmul(_TAIL_N(k), POSES[k].get('tail1', RK.I))) for k in DUR_N}


def _court(C):
    import phase28 as P28
    G, fn, tick, fast, second, title, tellraw, say, omsay, omchat = C.G, C.fn, C.tick, C.fast, C.second, C.title, C.tellraw, C.say, C.omsay, C.omchat
    give = C.give
    # ---- the King on his throne: a rig, a host marker, a click box
    th = rel(PAL.THRONE_AT)
    # (2.88) he holds court three blocks out from his throne and a little higher, his tail curled up at his side, not behind him:
    # stood at the throne's foot, his coil sat in the seat and his tail and its flame went through the purple back. Kings already
    # at the throne's foot are moved out (the old spot cleared, the new one filled the next second)
    second.append('execute as @e[type=minecraft:marker,tag=bm.omthrone] at @s as @e[type=minecraft:marker,tag=bm.omnpc,distance=..0.5] at @s run function bm:p169/npc/remove')
    second.append(f'execute if score #omfree bm.omwin matches 1 as @e[type=minecraft:marker,tag=bm.omthrone] at @s if entity @a[distance=..48] positioned {COURT} '
                  'unless entity @e[type=minecraft:marker,tag=bm.omnpc,distance=..2] unless entity @e[type=minecraft:husk,tag=bm.omboss,distance=..40] run function bm:p169/npc/make')
    fn('p169/npc/make', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.omnpc","bm.omnnew"]}', 'tp @e[type=minecraft:marker,tag=bm.omnnew,distance=..1] ~ ~ ~ ~ 0',
                         'execute as @e[type=minecraft:marker,tag=bm.omnnew,distance=..1] at @s run function bm:p169/npc/init'])
    fn('p169/npc/init', ['tag @s remove bm.omnnew', 'scoreboard players add #omn bm.omid 1', 'scoreboard players operation @s bm.omid = #omn bm.omid', 'scoreboard players set @s bm.omf 0'] +
       [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(OArt, p, ["bm.omn", f"bm.omn_{p}", "bm.omnnew"], SB, scale0=True, extra={"view_range": F(3.0), "brightness": {"block": Int(13), "sky": Int(13)}})}'
        for p in OArt.PARTS] +
       ['scoreboard players operation @e[type=minecraft:item_display,tag=bm.omnnew,distance=..1] bm.omid = @s bm.omid',
        'tag @e[type=minecraft:item_display,tag=bm.omnnew,distance=..1] add bm.omnsel', 'tag @e[tag=bm.omnnew] remove bm.omnnew',
        'execute rotated as @s rotated ~ 0 run function bm:p169/npc/place', 'function bm:p169/npc/pose/idle_a',
        'summon minecraft:interaction ~ ~0.5 ~ {Tags:["bm.omnhit"],width:3.2f,height:7.0f,response:1b}',
        'particle minecraft:soul ~ ~3 ~ 1.5 2.5 1.5 0.03 60', 'tag @e[tag=bm.omnsel] remove bm.omnsel'])
    fn('p169/npc/place', RF.place(OArt, UB, nsel))
    for name, dur in DUR_N.items():
        fn(f'p169/npc/pose/{name}', RF.pose(OArt, NPOSES[name], SB, dur, nsel))
    nface = lambda e: (f'data modify entity {nsel("head")[:-1]},limit=1] item.components."minecraft:custom_model_data" set value {{strings:["{e}"]}}' if e
                       else f'data remove entity {nsel("head")[:-1]},limit=1] item.components."minecraft:custom_model_data"')
    second.append('execute as @e[type=minecraft:marker,tag=bm.omnpc] at @s if entity @a[distance=..48] run function bm:p169/npc/sec')
    fn('p169/npc/sec', ['scoreboard players add @s bm.omf 1', 'scoreboard players operation #oid bm.rng = @s bm.omid',
                        'execute as @e[type=minecraft:item_display,tag=bm.omn,distance=..12] if score @s bm.omid = #oid bm.rng run tag @s add bm.omnsel',
                        f'execute unless entity {nsel("head")} run return run function bm:p169/npc/remove',
                        'execute unless entity @e[type=minecraft:interaction,tag=bm.omnhit,distance=..2] run summon minecraft:interaction ~ ~0.5 ~ {Tags:["bm.omnhit"],width:3.2f,height:7.0f,response:1b}',
                        'scoreboard players operation #f bm.rng = @s bm.omf', 'scoreboard players operation #f bm.rng %= #24 bm.rng',
                        'execute if score #f bm.rng matches 0 run function bm:p169/npc/pose/idle_a', 'execute if score #f bm.rng matches 4 run function bm:p169/npc/pose/idle_b',
                        'execute if score #f bm.rng matches 8 run function bm:p169/npc/pose/idle_a', 'execute if score #f bm.rng matches 12 run function bm:p169/npc/pose/monocle',
                        'execute if score #f bm.rng matches 15 run function bm:p169/npc/pose/idle_b',
                        'execute if score #f bm.rng matches 7 run ' + nface('blink'), 'execute if score #f bm.rng matches 8 run ' + nface(None),
                        'execute if score #f bm.rng matches 19 run ' + nface('blink'), 'execute if score #f bm.rng matches 20 run ' + nface('warm'),
                        'particle minecraft:soul ~ ~3 ~ 1 2 1 0.01 1', 'tag @e[tag=bm.omnsel] remove bm.omnsel'])
    fn('p169/npc/remove', ['scoreboard players operation #oid bm.rng = @s bm.omid',
                           'execute as @e[type=minecraft:item_display,tag=bm.omn,distance=..12] if score @s bm.omid = #oid bm.rng run kill @s',
                           'kill @e[type=minecraft:interaction,tag=bm.omnhit,distance=..2]', 'particle minecraft:soul ~ ~3 ~ 1.5 2.5 1.5 0.03 40', 'kill @s'])
    second.append('execute as @e[type=minecraft:interaction,tag=bm.omnhit] at @s unless entity @e[type=minecraft:marker,tag=bm.omnpc,distance=..2] run kill @s')
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.omnhit] if data entity @s interaction at @s run function bm:p169/npc/click',
             'execute as @e[type=minecraft:interaction,tag=bm.omnhit] if data entity @s attack run data remove entity @s attack']
    fn('p169/npc/click', ['execute as @e[type=minecraft:marker,tag=bm.omnpc,distance=..2,limit=1] at @s run function bm:p169/npc/greet_welcome',
                          'execute on target run function bm:p169/court/open', 'data remove entity @s interaction'])
    # (a visitor's click: he spreads his arms in welcome; a gift: a bow - then back to his idling)
    for g in ('welcome', 'bow'):
        fn(f'p169/npc/greet_{g}', ['scoreboard players operation #oid bm.rng = @s bm.omid',
                                   'execute as @e[type=minecraft:item_display,tag=bm.omn,distance=..12] if score @s bm.omid = #oid bm.rng run tag @s add bm.omnsel',
                                   f'function bm:p169/npc/pose/{g}', 'scoreboard players set @s bm.omf 1', 'tag @e[tag=bm.omnsel] remove bm.omnsel'])
    tick.append('scoreboard players remove @a[scores={bm.omhc=1..}] bm.omhc 1')
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.omn]', 'kill @e[type=minecraft:interaction,tag=bm.omnhit]', 'kill @e[type=minecraft:marker,tag=bm.omnpc]']

    # ---- his favour (bm.omfav) and your rank
    fn('p169/rank', ['scoreboard players set #rk bm.rng 0'] +
       [f'execute if score @s bm.omfav matches {lo}.. run scoreboard players set #rk bm.rng {i}' for i, (lo, _n, _c) in enumerate(RANKS) if i])
    second.append('execute as @a[scores={bm.omfav=1..}] at @s run function bm:p169/rank_sec')
    fn('p169/rank_sec', ['function bm:p169/rank', 'execute unless score @s bm.ompd matches 0.. run scoreboard players set @s bm.ompd 0',
                         'execute if score #rk bm.rng > @s bm.ompd run function bm:p169/rank_up', 'scoreboard players operation @s bm.ompd = #rk bm.rng',
                         'execute if score #rk bm.rng matches 1.. if score @s bm.omtt matches 1 run function bm:p169/ttl/want',
                         'execute if score #rk bm.rng matches 4.. run function bm:p169/perk/falter',
                         'execute if score #rk bm.rng matches 5 run function bm:p169/perk/warden'])
    fn('p169/rank_up', ['kill @e[type=minecraft:text_display,tag=bm.omttl,distance=..4]', 'execute unless score @s bm.omtt matches 0.. run scoreboard players set @s bm.omtt 1'] +
       [f'execute if score #rk bm.rng matches {i} run ' + tellraw('@s', C.PREFIX + [T('The King of the Dead names you ', 'gray'), T(n, c, bold=True), T(f'! ({PERKS[i]})', 'gray')])
        for i, (lo, n, c) in enumerate(RANKS) if i] +
       ['playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.8 0.8', 'execute if score #rk bm.rng matches 5 run advancement grant @s only bm:story/om_warden'])
    G.wjson('bm/advancement/story/om_warden.json', {'parent': 'bm:story/om_peace', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
            'display': {'icon': {'id': 'minecraft:soul_lantern'}, 'title': T('Warden of the Dead', SOUL), 'description': T("Rise to the King of the Dead's highest rank", 'gray'),
                        'frame': 'challenge', 'show_toast': True, 'announce_to_chat': True, 'hidden': False}})
    # (your title over your head - Squire and up, on by default, off in his menu)
    for i, (lo, n, c) in enumerate(RANKS):
        if not i: continue
        tnbt = snbt({'Tags': ['bm.omttl', 'bm.omtnew'], 'billboard': 'center', 'view_range': F(0.5), 'teleport_duration': Int(1), 'default_background': B(0),
                     'background': Int(0x40000000), 'transformation': {'left_rotation': RF.IDENT, 'right_rotation': RF.IDENT, 'translation': [F(0)] * 3, 'scale': [F(0.6)] * 3},
                     'text': [T('✦ ', SOUL), T(n, c, bold=True), T(' ✦', SOUL)]})
        fn(f'p169/ttl/make{i}', [f'summon minecraft:text_display ~ ~2.4 ~ {tnbt}'])
    fn('p169/ttl/want', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #has bm.rng 0',
                         'execute as @e[type=minecraft:text_display,tag=bm.omttl] if score @s bm.pid = #me bm.pid run scoreboard players set #has bm.rng 1',
                         'execute if score #has bm.rng matches 1 run return 0'] +
       [f'execute if score #rk bm.rng matches {i} run function bm:p169/ttl/make{i}' for i in range(1, len(RANKS))] +
       ['scoreboard players operation @e[type=minecraft:text_display,tag=bm.omtnew,distance=..4] bm.pid = @s bm.pid', 'tag @e[tag=bm.omtnew] remove bm.omtnew'])
    tick.append('execute as @e[type=minecraft:text_display,tag=bm.omttl] at @s run function bm:p169/ttl/tick')
    fn('p169/ttl/tick', ['scoreboard players operation #me bm.pid = @s bm.pid', 'tag @a remove bm.omto',
                         'execute as @a[scores={bm.omtt=1}] if score @s bm.pid = #me bm.pid run tag @s add bm.omto',
                         'execute unless entity @a[tag=bm.omto] run return run kill @s', 'execute at @a[tag=bm.omto,limit=1] run tp @s ~ ~2.4 ~', 'tag @a remove bm.omto'])

    # ---- the perks
    # KNIGHT: Soul-Edged - your blows on the undead burn blue
    G.wjson('bm/advancement/p169/edge.json', {'criteria': {'h': {'trigger': 'minecraft:player_hurt_entity', 'conditions': {
        'player': [{'condition': 'minecraft:entity_scores', 'entity': 'this', 'scores': {'bm.omfav': {'min': RANKS[2][0]}}}],
        'entity': [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:entity_type': '#minecraft:undead'}}]}}}, 'rewards': {'function': 'bm:p169/perk/edge'}})
    fn('p169/perk/edge', ['advancement revoke @s only bm:p169/edge',
                          'execute at @s as @e[type=#minecraft:undead,distance=..6,nbt={HurtTime:10s},tag=!bm.omboss,limit=1,sort=nearest] at @s run function bm:p169/perk/edge2'])
    fn('p169/perk/edge2', ['damage @s 3 minecraft:magic', 'particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.5 0.3 0.03 10'])
    # DUKE: the undead near you falter
    fn('p169/perk/falter', ['effect give @e[type=#minecraft:undead,distance=..10,tag=!bm.omraised,tag=!bm.npc,tag=!bm.omboss] minecraft:weakness 2 0',
                            'effect give @e[type=#minecraft:undead,distance=..10,tag=!bm.omraised,tag=!bm.npc,tag=!bm.omboss] minecraft:slowness 2 0'])
    # WARDEN: a soul serpent escort; the Royal Pardon (once a day, at two hearts or less)
    fn('p169/perk/warden', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #has bm.rng 0',
                            'execute as @e[type=minecraft:marker,tag=bm.ssesc] if score @s bm.pid = #me bm.pid run scoreboard players set #has bm.rng 1',
                            'execute if score #has bm.rng matches 0 unless dimension bm:gutter run function bm:p169/perk/esc_new',
                            'execute if score @s bm.hp matches 1..4 unless score @s bm.omgd = #day bm.bm run function bm:p169/perk/pardon'])
    fn('p169/perk/esc_new', ['summon minecraft:marker ~ ~1.4 ~ {Tags:["bm.sshost","bm.ssorb","bm.ssesc","bm.ssnew"]}',
                             'scoreboard players operation @e[type=minecraft:marker,tag=bm.ssnew,distance=..2] bm.pid = @s bm.pid',
                             'execute as @e[type=minecraft:marker,tag=bm.ssnew,distance=..2] at @s run function bm:p169/ss/born'])
    tick.insert(0, 'execute as @e[type=minecraft:marker,tag=bm.ssesc] at @s run function bm:p169/perk/esc_tick')
    fn('p169/perk/esc_tick', ['scoreboard players operation #me bm.pid = @s bm.pid', 'tag @a remove bm.omto',
                              'execute as @a if score @s bm.pid = #me bm.pid run tag @s add bm.omto',
                              'execute unless entity @a[tag=bm.omto,scores={bm.omfav=700..}] at @s run return run function bm:p169/ss/go',
                              'execute at @a[tag=bm.omto,limit=1] unless entity @s[distance=..12] run return run function bm:p169/ss/go',
                              'execute at @a[tag=bm.omto,limit=1] run tp @s ~ ~1.4 ~', 'tag @a remove bm.omto'])
    second.append('execute as @e[type=minecraft:marker,tag=bm.ssesc] at @s run function bm:p169/perk/esc_sec')
    fn('p169/perk/esc_sec', ['scoreboard players add @s bm.omt 1', 'execute unless score @s bm.omt matches 3.. run return 0',
                             'execute unless entity @e[type=#bm:hostile,tag=!bm.npc,distance=..7] run return 0', 'scoreboard players set @s bm.omt 0',
                             'scoreboard players set #sst bm.rng 2', 'function bm:p169/ss/state',
                             'execute as @e[type=#bm:hostile,tag=!bm.npc,tag=!bm.omboss,distance=..7,sort=nearest,limit=1] at @s run function bm:p169/ss/nip'])
    fn('p169/ss/nip', ['damage @s 4 minecraft:magic', 'particle minecraft:soul ~ ~1 ~ 0.3 0.4 0.3 0.03 8', 'playsound minecraft:entity.vex.charge neutral @a[distance=..12] ~ ~ ~ 0.5 1.8'])
    fn('p169/perk/pardon', ['scoreboard players operation @s bm.omgd = #day bm.bm', 'effect give @s minecraft:regeneration 5 3 true', 'effect give @s minecraft:absorption 30 2 true',
                            'effect give @s minecraft:resistance 4 2 true', 'effect clear @s minecraft:wither', 'effect clear @s minecraft:poison',
                            'particle minecraft:soul_fire_flame ~ ~1 ~ 0.6 1 0.6 0.05 60', 'playsound minecraft:item.totem.use player @a[distance=..16] ~ ~ ~ 0.6 1.4',
                            title('@s', 'actionbar', [T('THE ROYAL PARDON - ', SOUL, bold=True), T('"Not today, my Warden. Not on my watch."', OM_LINE)])])

    # ---- his menus (all on bm.menu COURT)
    codes = {'peer': COURT + 1, 'garr': COURT + 2, 'gift': COURT + 3, 'chron': COURT + 4, 'title': COURT + 5, 'rematch': COURT + 6, 'back': COURT + 9,
             'tithe': COURT + 11, 'souls': COURT + 12, 'buy': COURT + 21}
    chap = lambda i: COURT + 30 + i
    rk_names = [n for _lo, n, _c in RANKS]
    fn('p169/court/open', ['execute if score @s bm.omhc matches 1.. run return 0', 'scoreboard players set @s bm.omhc 10',
                           'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'function bm:p169/court/main'])
    fn('p169/court/vals', ['function bm:p169/rank', 'execute store result storage bm:tmp om.fav int 1 run scoreboard players get @s bm.omfav'] +
       [f'execute if score #rk bm.rng matches {i} run data modify storage bm:tmp om.rk set value "{n}"' for i, n in enumerate(rk_names)])
    main = P28.multi([T('KING OMEGA', OM_C, bold=True)],
                     [P28.body([T('"Ah - a visitor! Come in, come in. Mind the ghosts; they mind you." ', OM_LINE, italic=True)], 300),
                      P28.body([T('Your standing at court: ', 'gray'), T('$(rk)', SOUL, bold=True), T(' - favour ', 'gray'), T('$(fav)', 'white')], 300)],
                     [P28.btn(T('The Peerage', '#ffcf40', bold=True), codes['peer'], width=150, tooltip=T('Your rank at court - and how to rise.', 'gray')),
                      P28.btn(T('The Ghost Garrison', SOUL, bold=True), codes['garr'], width=150, tooltip=T('Soul Braziers: his serpents keep your home.', 'gray')),
                      P28.btn(T('Offer a gift', OM_C, bold=True), codes['gift'], width=150, tooltip=T('Hand him what you hold. He tells stories to friends.', 'gray')),
                      P28.btn(T('The Chronicle', '#d0b8ff', bold=True), codes['chron'], width=150, tooltip=T('The chapters he has told you - and hints for the rest.', 'gray')),
                      P28.btn(T('My title on / off', 'gray'), codes['title'], width=150, tooltip=T('Your rank over your head (Squire and up).', 'gray')),
                      P28.btn(T('Re-challenge the King', '#ff6a6a', bold=True), codes['rematch'], width=150,
                              tooltip=T('Hard mode, once a day: fight him again in his tomb - every peace made wins another Monocle.', 'gray'))],
                     columns=2, exit_label='Take your leave')
    fn('p169/court/main', [f'scoreboard players set @s bm.menu {COURT}', 'function bm:p169/court/vals', 'function bm:p169/court/main_show with storage bm:tmp om'])
    fn('p169/court/main_show', [f'$dialog show @s {snbt(main)}'])
    peer = P28.multi([T('THE PEERAGE', '#ffcf40', bold=True)],
                     [P28.body([T('You are ', 'gray'), T('$(rk)', SOUL, bold=True), T(' - favour ', 'gray'), T('$(fav)', 'white'), T('.', 'gray')], 320)] +
                     [P28.body([T(f'{n} ', c, bold=True), T(f'({lo}) - {PERKS[i]}.', 'gray')], 320) for i, (lo, n, c) in enumerate(RANKS) if i] +
                     [P28.body([T('Favour: waking him (60, a rematch 20), each new gift (40), a tithe (10), your Omega\'s Soul Court (2 a soul).', 'dark_gray')], 320)],
                     [P28.btn([T(f'Tithe {TITHE} Tokens', GOLD, bold=True), T('  +10', 'gray')], codes['tithe'], width=150, tooltip=T(f'Up to {TITHE_DAY} a day.', 'gray')),
                      P28.btn(T("Offer your Court's souls", SOUL, bold=True), codes['souls'], width=150, tooltip=T('Your Omega must be with you: 2 favour a soul.', 'gray')),
                      P28.btn(T('« Back', 'gray'), codes['back'], width=150)], columns=1, exit_label='Close')
    fn('p169/court/peer', [f'scoreboard players set @s bm.menu {COURT}', 'function bm:p169/court/vals', 'function bm:p169/court/peer_show with storage bm:tmp om'])
    fn('p169/court/peer_show', [f'$dialog show @s {snbt(peer)}'])
    garr = P28.multi([T('THE GHOST GARRISON', SOUL, bold=True)],
                     [P28.body([T('"My little ones need something to do. Give them a fire to keep and they will keep it - and you."', OM_LINE, italic=True)], 320),
                      P28.body([T('A Soul Brazier', SOUL, bold=True), T(f' ({BRAZIER_COST} Tokens; {BRAZIER_MAX} each, Squire and up): set it down and a soul serpent keeps it. '
                                                                         'By night it circles the fire and bites anything hostile within 16 - and plays the odd trick on you. '
                                                                         'Barons and up: no hostile mob spawns within 24 of it. Break the fire and the brazier comes back to you.', 'gray')], 320)],
                     [P28.btn([T('Buy a Soul Brazier', SOUL, bold=True), T(f'  {BRAZIER_COST} Tokens', 'gray')], codes['buy'], width=200),
                      P28.btn(T('« Back', 'gray'), codes['back'], width=200)], columns=1, exit_label='Close')
    fn('p169/court/garr', [f'scoreboard players set @s bm.menu {COURT}', f'dialog show @s {snbt(garr)}'])
    G.FUNCS['p28/act'] += [f'execute if score #act bm.pay matches {c} run return run function bm:p169/court/act' for c in list(codes.values()) + [chap(i) for i in range(len(GIFTS))]]
    fn('p169/court/act', [f'execute unless score @s bm.menu matches {COURT} run return run function bm:p28/stale',
                          f'execute if score #act bm.pay matches {codes["back"]} run return run function bm:p169/court/main',
                          f'execute if score #act bm.pay matches {codes["peer"]} run return run function bm:p169/court/peer',
                          f'execute if score #act bm.pay matches {codes["garr"]} run return run function bm:p169/court/garr',
                          f'execute if score #act bm.pay matches {codes["gift"]} run return run function bm:p169/court/gift',
                          f'execute if score #act bm.pay matches {codes["chron"]} run return run function bm:p169/court/chron',
                          f'execute if score #act bm.pay matches {codes["title"]} run return run function bm:p169/court/title',
                          f'execute if score #act bm.pay matches {codes["rematch"]} run return run function bm:p169/court/rematch',
                          f'execute if score #act bm.pay matches {codes["tithe"]} run return run function bm:p169/court/tithe',
                          f'execute if score #act bm.pay matches {codes["souls"]} run return run function bm:p170/tithe_souls',
                          f'execute if score #act bm.pay matches {codes["buy"]} run return run function bm:p169/court/buy'] +
       [f'execute if score #act bm.pay matches {chap(i)} run return run function bm:p169/court/read{i}' for i in range(len(GIFTS))])
    fn('p169/court/title', ['function bm:p169/rank', 'execute if score #rk bm.rng matches 0 run return run ' + omsay('A title? Earn one first, friend. Squires start at forty favour.'),
                            'execute if score @s bm.omtt matches 1 run return run function bm:p169/court/title_off', 'scoreboard players set @s bm.omtt 1',
                            omsay('There - let everyone see whose friend you are.')])
    # (2.87) a rematch, from his menu: hard mode, once a day - he goes down to his tomb and wakes again, fighting (and every peace
    # made after a rematch wins its maker another Monocle - phase169's peace/claim)
    tomb_near = '@e[type=minecraft:marker,tag=bm.omtomb,distance=..64,sort=nearest,limit=1]'
    fn('p169/court/rematch', ['execute unless score #hard bm.cfg matches 1 run return run ' + omsay('A rematch? Not in a world this gentle, friend. Come back when it has woken to its harder self.'),
                              'execute if score @s bm.omrd = #day bm.bm run return run ' + omsay('Once a day, friend - even a dead king needs his rest. Tomorrow!'),
                              f'execute unless entity {tomb_near} run return run ' + omsay('My tomb is too far from here to fight properly. Come to the palace.'),
                              f'execute as {tomb_near} if score @s bm.omst matches 1 run return run ' + omsay('I am ALREADY up and fighting, friend. Look behind you.'),
                              'scoreboard players operation @s bm.omrd = #day bm.bm', 'dialog clear @s',
                              omchat('A rematch! Splendid. Down to the tomb with you - I shall be waiting. Do try to keep up.', '@s'),
                              f'execute as {tomb_near} at @s run function bm:p169/tomb/wake'])
    fn('p169/court/title_off', ['scoreboard players set @s bm.omtt 0', omsay('Modest! I like that in a peer.')])
    fn('p169/court/tithe', ['execute unless score @s bm.omtd = #day bm.bm run scoreboard players set @s bm.omtn 0', 'scoreboard players operation @s bm.omtd = #day bm.bm',
                            f'execute if score @s bm.omtn matches {TITHE_DAY}.. run return run ' + omsay('Enough for today, friend! The treasury overflows. Come back tomorrow.')] +
       P28.pay_lines('token', TITHE, omsay(f'Generous of you - but that is fewer than {TITHE} Tokens.')) +
       ['scoreboard players add @s bm.omtn 1', 'scoreboard players add @s bm.omfav 10', 'playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 0.8',
        omsay('For the palace roof. Pistachio thanks you; the rain thanks you less.'), 'function bm:p169/court/peer'])
    fn('p169/court/buy', ['function bm:p169/rank', 'execute if score #rk bm.rng matches 0 run return run ' + omsay('The Garrison is for my peers, friend. Squire first - forty favour.')] +
       P28.pay_lines('token', BRAZIER_COST, omsay(f'A Soul Brazier is {BRAZIER_COST} Tokens, friend.')) +
       [give('om_brazier'), 'playsound minecraft:block.soul_sand.place player @s ~ ~ ~ 1 0.8', omsay('Set it down somewhere you love. My little ones will see to the rest.')])
    # ---- gifts and the Chronicle
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #1024 bm.rng 1024'] + [f'scoreboard players set #{2 ** i} bm.rng {2 ** i}' for i in range(10)]
    bit = lambda i: ['scoreboard players operation #q bm.rng = @s bm.omlore', f'scoreboard players operation #q bm.rng /= #{2 ** i} bm.rng',
                     'scoreboard players operation #q bm.rng %= #2 bm.rng']
    fn('p169/court/gift', [f'execute if items entity @s weapon.mainhand {iid}[!minecraft:custom_data] run return run function bm:p169/court/gift{i}' for i, (iid, *_r) in enumerate(GIFTS)] +
       ['execute if items entity @s weapon.mainhand * run return run ' + omsay('How... thoughtful. *He turns it over politely and hands it back.* (The Chronicle has hints.)'),
        omsay('Your hand is empty, friend. Hold the gift you mean to give him.')])
    for i, (iid, hint, ttl, text) in enumerate(GIFTS):
        fn(f'p169/court/gift{i}', bit(i) + ['execute if score #q bm.rng matches 1 run return run ' + omsay('Another? You are kind - but I treasure the first one too much to need two.'),
                                            'item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
                                            f'scoreboard players add @s bm.omlore {2 ** i}', 'scoreboard players add @s bm.omfav 40',
                                            'playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 1 0.8', 'particle minecraft:soul ~ ~1.5 ~ 0.5 0.5 0.5 0.02 20',
                                            omchat(f'For me? ...Oh, that takes me back. Sit down - let me tell you about {ttl.split(". ", 1)[1]}.'),
                                            'execute if score @s bm.omlore matches 1023 run advancement grant @s only bm:story/om_lore',
                                            'execute as @e[type=minecraft:marker,tag=bm.omnpc,distance=..24,sort=nearest,limit=1] at @s run function bm:p169/npc/greet_bow',
                                            f'function bm:p169/court/read{i}'])
        note = P28.notice([T(ttl, OM_C, bold=True)], [P28.body([T(f'"{p}"', OM_LINE)], 320) for p in text] +
                          [P28.body([T('- from the Chronicle of King Omega', 'dark_gray', italic=True)], 320)], label='Close')
        fn(f'p169/court/read{i}', bit(i) + ['execute if score #q bm.rng matches 0 run return run ' + omsay(f'That chapter? I only tell it to friends who bring me {hint}.'),
                                            f'scoreboard players set @s bm.menu {COURT}', f'dialog show @s {snbt(note)}'])
    G.wjson('bm/advancement/story/om_lore.json', {'parent': 'bm:story/om_peace', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
            'display': {'icon': {'id': 'minecraft:book'}, 'title': T('The Chronicle of King Omega', OM_C), 'description': T('Hear every chapter of the dead king\'s story', 'gray'),
                        'frame': 'goal', 'show_toast': True, 'announce_to_chat': True, 'hidden': False}})
    btn_open = lambda i: snbt(P28.btn(T(GIFTS[i][2], '#d0b8ff', bold=True), chap(i), width=260))
    btn_shut = lambda i: snbt(P28.btn([T(GIFTS[i][2].split('.')[0] + '. ', 'dark_gray'), T('???', 'dark_gray')], None, width=260,
                                      tooltip=T(f'He would tell it to a friend who brought him {GIFTS[i][1]}.', 'gray')))
    fn('p169/court/chron', [f'scoreboard players set @s bm.menu {COURT}', 'data modify storage bm:tmp om.acts set value []'] +
       [l for i in range(len(GIFTS)) for l in bit(i) + [f'execute if score #q bm.rng matches 1 run data modify storage bm:tmp om.acts append value {btn_open(i)}',
                                                         f'execute if score #q bm.rng matches 0 run data modify storage bm:tmp om.acts append value {btn_shut(i)}']] +
       [f'data modify storage bm:tmp om.acts append value {snbt(P28.btn(T("« Back", "gray"), codes["back"], width=260))}',
        'function bm:p169/court/chron_show with storage bm:tmp om'])
    chron = P28.multi([T('THE CHRONICLE OF KING OMEGA', '#d0b8ff', bold=True)],
                      [P28.body([T('"Every gift, a chapter. I am an old ghost; I have a great many chapters."', OM_LINE, italic=True)], 300)], '@@ACTS@@', columns=1, exit_label='Close')
    fn('p169/court/chron_show', ['$dialog show @s ' + snbt(chron).replace('"@@ACTS@@"', '$(acts)')])

    # ---- the Ghost Garrison: Soul Braziers
    fn('p169/bz/use', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                       'scoreboard players set #n bm.rng 0', 'execute as @e[type=minecraft:marker,tag=bm.ombz] if score @s bm.pid = #me bm.pid run scoreboard players add #n bm.rng 1',
                       f'execute if score #n bm.rng matches {BRAZIER_MAX}.. run return run ' + say(f'You keep {BRAZIER_MAX} Soul Braziers already - break one to move it.', SOUL),
                       'scoreboard players set #placed bm.rng 0', 'scoreboard players set #ray bm.rng 25', 'tag @s add bm.omplacer',
                       'execute anchored eyes positioned ^ ^ ^ run function bm:p169/bz/ray', 'tag @s remove bm.omplacer',
                       'execute if score #placed bm.rng matches 1 run item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}'])
    fn('p169/bz/ray', ['execute unless block ~ ~ ~ #minecraft:replaceable run return run function bm:p169/bz/hit',
                       'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p169/bz/ray'])
    fn('p169/bz/hit', ['execute align xyz positioned ~0.5 ~1 ~0.5 unless block ~ ~ ~ #minecraft:replaceable run return run ' + say('No room for a brazier there.'),
                       'execute align xyz positioned ~0.5 ~1 ~0.5 if entity @e[type=minecraft:marker,tag=bm.ombz,distance=..6] run return run ' + say('Too close to another Soul Brazier.'),
                       'execute align xyz positioned ~0.5 ~1 ~0.5 run function bm:p169/bz/place'])
    fn('p169/bz/place', ['setblock ~ ~ ~ minecraft:soul_campfire[lit=true,signal_fire=false,waterlogged=false,facing=north]',
                         'summon minecraft:marker ~ ~ ~ {Tags:["bm.ombz","bm.ombznew"]}', 'scoreboard players operation @e[type=minecraft:marker,tag=bm.ombznew,distance=..1] bm.pid = #me bm.pid',
                         'tag @e[tag=bm.ombznew] remove bm.ombznew', 'scoreboard players set #placed bm.rng 1',
                         'particle minecraft:soul ~ ~0.8 ~ 0.3 0.5 0.3 0.04 30', 'playsound minecraft:block.respawn_anchor.set_spawn block @a[distance=..16] ~ ~ ~ 0.8 1.2',
                         C.title('@a[tag=bm.omplacer]', 'actionbar', T('A Soul Brazier - by night a soul serpent keeps it.', SOUL))])
    second.append('execute as @e[type=minecraft:marker,tag=bm.ombz] at @s if entity @a[distance=..48] run function bm:p169/bz/sec')
    serp = '@e[type=minecraft:marker,tag=bm.ssorb,tag=!bm.ssbig,tag=!bm.ssesc,distance=..2]'
    fn('p169/bz/sec', ['execute unless block ~ ~ ~ minecraft:soul_campfire run return run function bm:p169/bz/broken',
                       # (the Royal Ward: its owner a Baron or more)
                       'scoreboard players operation #me bm.pid = @s bm.pid', 'tag @s remove bm.omward',
                       f'execute as @a[scores={{bm.omfav={RANKS[3][0]}..}}] if score @s bm.pid = #me bm.pid run tag @e[type=minecraft:marker,tag=bm.ombz,distance=..0.5] add bm.omward',
                                              'execute unless score #tod bm.bm matches 13000..23000 positioned ~ ~1.5 ~ as ' + serp + ' at @s run function bm:p169/ss/go',
                       'execute unless score #tod bm.bm matches 13000..23000 run return 0',
                       f'execute positioned ~ ~1.5 ~ unless entity {serp} run function bm:p169/bz/serpent',
                       'scoreboard players add @s bm.omt 1',
                       'execute if score @s bm.omt matches 3.. if entity @e[type=#bm:hostile,tag=!bm.npc,distance=..16] run function bm:p169/bz/bite',
                       'execute store result score #r bm.rng run random value 1..90',
                       'execute if score #r bm.rng matches 1 as @a[distance=..10,gamemode=!spectator] if score @s bm.pid = #me bm.pid at @s run function bm:p169/bz/prank'])
    fn('p169/bz/serpent', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.sshost","bm.ssorb","bm.ssnew"]}',
                           'execute as @e[type=minecraft:marker,tag=bm.ssnew,distance=..1] at @s run function bm:p169/ss/born'])
    fn('p169/bz/bite', ['scoreboard players set @s bm.omt 0',
                        f'execute positioned ~ ~1.5 ~ as {serp} at @s run function bm:p169/bz/lunge',
                        'execute as @e[type=#bm:hostile,tag=!bm.npc,tag=!bm.omboss,distance=..16,sort=nearest,limit=1] at @s run function bm:p169/bz/bitten'])
    fn('p169/bz/lunge', ['scoreboard players set #sst bm.rng 5', 'function bm:p169/ss/state'])
    fn('p169/bz/bitten', ['damage @s 5 minecraft:magic', 'effect give @s minecraft:slowness 2 1', 'particle minecraft:soul ~ ~1 ~ 0.3 0.5 0.3 0.04 12',
                          'playsound minecraft:entity.vex.charge neutral @a[distance=..16] ~ ~ ~ 0.7 1.6'])
    fn('p169/bz/prank', ['execute store result score #r bm.rng run random value 1..3',
                         'execute if score #r bm.rng matches 1 run function bm:p169/bz/boo', 'execute if score #r bm.rng matches 2 run function bm:p169/bz/cookie',
                         'execute if score #r bm.rng matches 3 run function bm:p169/bz/spin'])
    fn('p169/bz/boo', ['playsound minecraft:entity.ghast.scream neutral @s ^ ^1 ^-1 0.4 1.6', 'effect give @s minecraft:levitation 1 3 true',
                       say('BOO! ...a soul serpent shrieks right behind you - and cackles all the way back to its brazier.', SOUL)])
    fn('p169/bz/cookie', ['give @s minecraft:cookie 1', 'playsound minecraft:entity.allay.item_given neutral @s ~ ~ ~ 0.7 1.4',
                          say('A soul serpent drops a cookie in your hand and zips off giggling. (Where did it GET that?)', SOUL)])
    fn('p169/bz/spin', ['tp @s ~ ~ ~ ~180 ~', 'playsound minecraft:entity.allay.ambient_with_item neutral @s ~ ~ ~ 0.7 1.8',
                        say('Something cold tugs your sleeve and spins you right round. A soul serpent, very pleased with itself.', SOUL)])
    fn('p169/bz/broken', ['loot spawn ~ ~0.5 ~ loot bm:items/om_brazier', 'execute positioned ~ ~1.5 ~ as ' + serp + ' at @s run function bm:p169/ss/go',
                          'particle minecraft:soul ~ ~0.5 ~ 0.3 0.3 0.3 0.03 16', 'kill @s'])
    # (the Royal Ward: no hostile mob is born within 24 of a warded brazier - caught the second it appears, before anything else sees it)
    G.FUNCS['loop/second'].insert(0, 'execute as @e[type=#bm:hostile,tag=!bm.seen] at @s if entity @e[type=minecraft:marker,tag=bm.omward,distance=..24] run function bm:p169/bz/spurn')
    # (2.88) nothing spawns in the Omega Palace: a monster (or a bat) that has just come into being anywhere in its walls is
    # turned away before the mob hooks see it (his own - the guard's ghosts, the soul serpents - are born seen; anything that
    # walks in from outside was seen out there)
    pb, pd = BOX
    G.FUNCS['loop/second'].insert(0, f'execute as @e[type=minecraft:marker,tag=bm.ompal] at @s if entity @a[distance=..128] positioned {pb} '
                                     f'as @e[type=#bm:hostile,tag=!bm.seen,{pd}] at @s run function bm:p169/bz/spurn')
    G.FUNCS['loop/second'].insert(0, f'execute as @e[type=minecraft:marker,tag=bm.ompal] at @s if entity @a[distance=..128] positioned {pb} '
                                     f'run kill @e[type=minecraft:bat,{pd}]')
    fn('p169/bz/spurn', ['particle minecraft:soul ~ ~1 ~ 0.3 0.5 0.3 0.02 6', 'tp @s ~ -400 ~', 'kill @s'])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:marker,tag=bm.ombz]', 'kill @e[type=minecraft:text_display,tag=bm.omttl]']
    fn('admin/omega_favour', ['scoreboard players add @s bm.omfav 100', C.say('+100 favour with King Omega.', OM_C)])

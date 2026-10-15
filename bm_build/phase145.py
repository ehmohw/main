"""2.79: FISHY'S CABINET OF CURIOSITIES - and Fishy, the gentleman goldfish who keeps it.

THE CABINET   a hall off the Fixer's Lounge (its east doorway, the gilded one), where Fishy keeps his museum: six wings - the
              Hollow, the Gutter, the Skies, the Deep, the Wilds and the Court - of twenty exhibits each (cabinet_data.py).
SHOW HIM      hold one of the pack's rare things and right-click Fishy (at his desk, or your own Fishy anywhere): he makes a
              REPLICA for his cabinet. You keep the thing itself - nothing is ever taken. Each exhibit is recorded once, for the
              whole world, with the name of whoever showed it; every player's progress is the same cabinet.
THE MENU      right-click Fishy empty-handed (or his menu's THE CABINET): a page per wing - every exhibit shown as itself with who
              gave it, or veiled, with a riddle for where it is found. SET IT OUT IN THE HALL lays that wing's twenty replicas in
              the hall's cases, each with its plaque.
A WING DONE   all twenty in: everyone who gave to it gets that wing's stained-glass ROSETTE (sneak + use on a block: set it up)
              and its challenge - and FISHY LEARNS A POWER (every Fishy, the world's cabinet). All six: THE GOLDEN BOWL.
FISHY         met at his desk - talk to him and he gives you his POCKET BOWL (use it to call him; sneak + use: his menu). Early on
              he's a poor fighter (a slap of his claws); each wing finished teaches him more and toughens him:
              HOLLOW GRIP (withering claws), COIN TOSS (gold coins at range), RAY ZAP (a Vorn ray), BOWL SPLASH (a water jet; quick
              in water, and you breathe), THUNDER EXHIBIT (every sixth blow a thunderclap), GRAND COMPANY (you and your followers
              mend and stand firm near him); all six: THE GOLDEN BOWL - his bowl and limbs gilded, far tougher, and now and then a
              GRAND EXHIBITION (spectral replicas wheel round him and burst on every foe near).
              Right-click him: sit / stand (holding an exhibit: show it to him). A frame keeps him, a display case shows him as a
              figurine, Cecil sells his doll, the Tailor his top hats (and his Bubble Halo), the Recruiter his Raid Contract.
"""
import math
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import fishy_art as ART
import cabinet_data as CAB
import rigfol as RF
import rigkit as RK
from rigkit import qs, I
import phase95 as FX
import phase46 as P46
import phase89 as P89
import phase68 as P68
import phase98 as P98
import phase100 as P100
import phase121 as P121
import phase134 as P134
import phase141 as P141
import allies

ORANGE, LINE_C, GOLD, BOWL = '#ffa040', '#ffe0b0', '#ffcf40', '#9ad8ff'
PET_HP0, PET_CD = 30, 300
SP = ART.RIG_SCALE
UP = SP / 16
MENU, CABM = 9140, 9150                    # his menu 9140-9149 (p145/act); the Cabinet's pages 9150-9179 (p145/cab/act)
WINGS = [w for w, *_ in CAB.WINGS]
WNAME = {w: n for w, n, c, d in CAB.WINGS}
WCOL = {w: c for w, n, c, d in CAB.WINGS}
WDESC = {w: d for w, n, c, d in CAB.WINGS}
# the hall: east of the lounge, through its gilded gateway (the lounge's template corner OX, OY, OZ; its floor at OY+3)
OX, OY, OZ = P121.OX, P121.OY, P121.OZ
HX0, HX1, HZ0, HZ1 = OX + 25, OX + 42, OZ + 5, OZ + 19         # the hall's shell (walls included)
HALL_VER = 2
COLS = [OX + 27, OX + 29, OX + 31, OX + 33, OX + 35]            # the cases' columns, both long walls
DESK = (OX + 39.5, OY + 4, OZ + 12.5)                          # Fishy just behind his desk, facing the doorway (west)
# (the lounge's own region grows to take the hall in: adventure mode there too, and its rebuild leaves the hall be)
P121.BOX = (OX - 1, OY - 4, OZ - 1, 45, 20, 26)

# ------------------------------------------------------------------------------------------------ items
item('fy_bowl', TOTEM, "Fishy's Pocket Bowl", ORANGE,
     ['A thimble of a fishbowl; a painted goldfish', 'in a painted top hat looks out of it.', ('Use: call Fishy (again: call him over).', 'blue'),
      ('Sneak + use: his menu.', 'blue'), ('Show him a rare thing (right-click him with it):', 'blue'), ('a replica for his Cabinet - you keep yours.', 'blue'),
      ('If he faints: 5 minutes before he can return.', 'gray'), ('"Curiosity, dear friend, is the finest armour."', 'dark_gray')],
     model='bm:fy_bowl', stack=1, cat='magic', glint=True, comps=hold('none'))
HOLD['fy_bowl'] = 'bm:p145/use'
item('fcontract_fishy', TOTEM, 'Raid Contract: Fishy', ORANGE,
     ['Signed with a flourish - and a splash.', ('Use once: from then on Fishy', 'blue'), ('will come into the vault with you.', 'blue')],
     model='minecraft:paper', glint=True, stack=1, cat='magic', comps=hold('none'))
HOLD['fcontract_fishy'] = 'bm:p145/sign'
for _w, _n, _c, _d in CAB.WINGS + [('grand', 'the Whole Cabinet', GOLD, '')]:
    item(f'cab_rosette_{_w}', TOTEM, f'Rosette of {_n}' if _w != 'grand' else 'The Grand Rosette', _c,
         [f'Stained glass: the Cabinet\'s {_n} wing.' if _w != 'grand' else 'Stained glass: every wing of the Cabinet at once.',
          ('Given by Fishy to those who helped fill it.', 'gray'), ('Sneak + use on a block: set it up.', 'blue'), ('Sneak + punch it: take it back.', 'gray')],
         model=f'bm:cab_rosette_{_w}', stack=1, cat='relic', glint=_w == 'grand' or None, comps=hold('none'))
    HOLD[f'cab_rosette_{_w}'] = f'bm:p145/ros/place_{_w}'
# his doll (Cecil sells it with the rest - phase141)
item('doll_fishy', TOTEM, 'Fishy Doll', ORANGE, ['A doll of Fishy - bowl, hat, monocle and all.', ('Right-click a block: set it down.', 'blue'),
                                                 ('Right-click it: it twirls.', 'blue'), ('Sneak + punch: pick it up.', 'gray')],
     model='bm:doll_fishy', stack=16, cat='fun', comps=hold('none'))
HOLD['doll_fishy'] = 'bm:p141/doll_fishy/use'
P141.DOLLS.append(('doll_fishy', 'Fishy', ORANGE, 'A doll of Fishy - bowl, hat, monocle and all.', 'minecraft:splash', 'minecraft:entity.tropical_fish.flop',
                   'minecraft:bubble_pop'))
P141.DOLL_FROM['doll_fishy'] = ('fy_bowl', {'kh': 1.0, 'kb': 1.0, 'kl': 0.7})

# ------------------------------------------------------------------------------------------------ the registries
P46.COMPANIONS += ',tag=!bm.fypet'
allies.ALLIES.append('bm.fypet')
BIT = 2 ** len(P89.BIT)
P89.BIT['fishy'] = BIT
P68.KINDS['fishy'] = (max(v[0] for v in P68.KINDS.values()) + 1, 'fy_bowl', 'wolf', 'bm.fypet', 'p145/summon', 'p145/dismiss', 'bm.fysel2', 'Fishy', ORANGE)
P68.HE.add('fishy')
P98.CALLED.append(('fishy', 'Fishy', ORANGE, 'wolf', 'bm.fypet', 'bm.fysel2', 'bm.fycd', 'p145/try_summon', 'p145/dismiss', 'p145/recall', 'p145/go'))
P100.WHO['fishy'] = ('wolf', 'bm.fypet')
P100.VOICE['Fishy'] = (ORANGE, LINE_C)
EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious')
FACE_MODEL = {'happy': 'happy', 'surprised': 'shock', 'hurt': 'squint', 'sleepy': 'blink', 'blink': 'blink', 'squint': 'squint', 'serious': 'squint'}
FX.FOLK['fishy'] = ('minecraft:wolf', 'bm.fypet', 'type=minecraft:item_display,tag=bm.fyp,tag=bm.fyp_fish,tag=bm.fyp_pet,tag=!bm.fyfade', EXPR,
                    (60, 140), [('happy', 30, 3), ('squint', 26, 6)], ('happy', 40), 'hurt', 'serious')


class _Art:                                  # (the art module as rigfol and phase134 want it)
    PIVOT, PARENT, PARTS, PART_K, PREFIX = ART.PIVOT, ART.PARENT, ART.PARTS, ART.PART_K, ART.PREFIX
    HIDDEN = staticmethod(ART.HIDDEN)
    model_name = staticmethod(ART.model_name)


A = _Art
_figures0 = P134.figures


def _figures():
    F_ = _figures0()
    F_['fy_bowl'] = ('Fishy', P134._rigkit(A, ART.POSES['idle_a'], SP))
    return F_


P134.figures = _figures
P134.FIT['fy_bowl'] = (0.000, 1.716, -0.837, 0.869, -0.482, 0.482)      # (measured: phase134.measure)

# ------------------------------------------------------------------------------------------------ poses
limb = ART.limb
P = dict
POSES = {k: dict(v) for k, v in ART.POSES.items()}
POSES['run_a'] = P(ART.POSES['walk_a'], _off=(0, 0.5, 0), body=qs(('z', 5), ('x', 6)), legr=limb(1, 36), legl=limb(-1, -34),
                   armr=limb(1, -28, 6), arml=limb(-1, 28, 6), forer=limb(1, 30), forel=limb(-1, 34))
POSES['run_b'] = P(ART.POSES['walk_b'], _off=(0, 0.5, 0), body=qs(('z', -5), ('x', 6)), legr=limb(1, -34), legl=limb(-1, 36),
                   armr=limb(1, 28, 6), arml=limb(-1, -28, 6), forer=limb(1, 34), forel=limb(-1, 30))
POSES['air'] = P(ART.POSES['shock'], _face=None)
POSES['sit_b'] = P(ART.POSES['sit'], armr=limb(1, 22, 14), forer=limb(1, 58), fish=qs(('y', 10), ('x', -6)), weed=qs(('z', 8)))
POSES['strike_back'] = P(armr=limb(1, -40, 18), forer=limb(1, 70), arml=limb(-1, 10, 8), forel=limb(-1, 20), body=qs(('y', 14)), fish=qs(('y', 18)),
                         weed=qs(('z', -6)))
POSES['strike'] = P(armr=limb(1, 96, -6), forer=limb(1, 4), arml=limb(-1, -12, 10), forel=limb(-1, 16), body=qs(('y', -18), ('x', 6)), fish=qs(('y', -14), ('x', 8)),
                    weed=qs(('z', 8)))
POSES['toss'] = P(arml=limb(-1, 150, 10), forel=limb(-1, 30), armr=limb(1, 6, 8), forer=limb(1, 14), body=qs(('y', 10)), fish=qs(('y', 16)))
POSES['zap'] = P(ART.POSES['point'], body=qs(('x', 10)), fish=qs(('y', 0), ('x', 14)))
POSES['splash'] = P(_off=(0, -0.4, 0), body=qs(('x', 26)), legr=limb(1, -16), legl=limb(-1, -16), armr=limb(1, 30, 30), forer=limb(1, 40), arml=limb(-1, 30, 30),
                    forel=limb(-1, 40), fish=qs(('x', 20)))
POSES['thunder_up'] = P(armr=limb(1, 160, 20), forer=limb(1, 10), arml=limb(-1, 160, 20), forel=limb(-1, 10), _off=(0, 0.6, 0), fish=qs(('x', -16)))
POSES['thunder'] = P(armr=limb(1, 40, 60), forer=limb(1, 30), arml=limb(-1, 40, 60), forel=limb(-1, 30), _off=(0, -0.8, 0), body=qs(('x', 6)),
                     legr=limb(1, 20, 8), legl=limb(-1, 20, 8), fish=qs(('x', 10)))
POSES['ult'] = P(armr=limb(1, 90, 80), forer=limb(1, 0), arml=limb(-1, 90, 80), forel=limb(-1, 0), _off=(0, 1.2, 0), fish=qs(('y', 30)),
                 weed=qs(('z', 12)))
POSES['paddle_a'] = P(_off=(0, -2.0, 0), legr=limb(1, 30, 10), legl=limb(-1, -10, 10), armr=limb(1, 60, 40), forer=limb(1, 20), arml=limb(-1, -20, 40),
                      forel=limb(-1, 40), fish=qs(('z', -10)), weed=qs(('z', 14)))
POSES['paddle_b'] = P(_off=(0, -1.6, 0), legr=limb(1, -10, 10), legl=limb(-1, 30, 10), armr=limb(1, -20, 40), forer=limb(1, 40), arml=limb(-1, 60, 40),
                      forel=limb(-1, 20), fish=qs(('z', 10)), weed=qs(('z', -14)))
DUR = {'idle_a': 20, 'idle_b': 20, 'walk_a': 6, 'walk_b': 6, 'run_a': 4, 'run_b': 4, 'air': 5, 'sit': 14, 'sit_b': 18, 'bow': 10, 'wave_a': 6, 'wave_b': 6,
       'point': 6, 'shock': 3, 'tired': 18, 'strike_back': 4, 'strike': 2, 'toss': 4, 'zap': 3, 'splash': 4, 'thunder_up': 6, 'thunder': 2, 'ult': 10,
       'paddle_a': 10, 'paddle_b': 10} | {f'swim_{i}': 6 for i in range(ART.LAP)}


def solve(pz):
    """rigkit's solve - and the fish's laps of his bowl: his display moved round inside it (as tools/preview/fishy.py)"""
    xf = RK.solve(ART.PIVOT, ART.PARENT, pz)
    if '_fish_at' in pz:
        q, t = xf['fish']
        d = RK.qrot(xf['body'][0], RK.D(pz['_fish_at']))
        xf['fish'] = (q, tuple(t[i] + d[i] for i in range(3)))
    return xf


def pose_lines(pz, dur, sel, swap_face=False):
    U = SP / 16
    xf = solve(pz)
    out = []
    for p in ART.PARTS:
        q, t = xf[p]
        k = ART.PART_K.get(p, 1.0)
        sc = round(SP * k, 4)
        extra = ''
        if swap_face and p == 'fish':
            extra = f',item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"bm:{ART.model_name(p, pz)}"}}}}'
        out.append(f'execute as {sel(p)} run data merge entity @s {{start_interpolation:0,interpolation_duration:{dur},transformation:{{left_rotation:'
                   f'{snbt(RF.qf(q))},translation:[{t[0] * U:.4f}f,{t[1] * U:.4f}f,{t[2] * U:.4f}f],scale:[{sc}f,{sc}f,{sc}f]}}{extra}}}')
    return out


def extend_offers(O, offer):
    pass


# ================================================================================================= resource pack
def _bowl_icon():
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((2, 3, 13, 14), fill=hexc('#bfe6fa'), outline=hexc('#5a8aa8'))
    d.rectangle((3, 3, 12, 4), fill=(0, 0, 0, 0)); d.line((4, 4, 11, 4), fill=hexc('#ffffff'))        # the open lip
    d.ellipse((5, 7, 10, 11), fill=hexc('#f6a11e'), outline=hexc('#b05a10'))                             # the goldfish
    d.polygon([(10, 9), (12, 7), (12, 11)], fill=hexc('#f39220'))
    d.rectangle((6, 5, 8, 6), fill=hexc('#1c1c22')); d.line((5, 7, 9, 7), fill=hexc('#1c1c22'))         # his hat
    im.putpixel((7, 8), hexc('#121212')); im.putpixel((8, 8), hexc('#e2b42c'))
    d.line((4, 13, 11, 13), fill=hexc('#e4d6bb'))
    d.line((3, 6, 3, 10), fill=hexc('#ffffff'))
    return im


def _veiled_icon():
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(8, 1), (13, 6), (14, 14), (2, 14), (3, 6)], fill=hexc('#5a1830'), outline=hexc('#2a0812'))   # a velvet cloth over something
    d.line((5, 6, 4, 13), fill=hexc('#7a2a48')); d.line((11, 6, 12, 13), fill=hexc('#7a2a48'))
    d.rectangle((2, 13, 14, 14), fill=hexc('#c89a3a'))
    for x, y in ((7, 4), (8, 4), (9, 5), (9, 6), (8, 7), (8, 8), (8, 10)):                                 # a gold question mark
        im.putpixel((x, y), hexc('#ffd860'))
    return im


def _rosette_icon(col, grand=False):
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((1, 1, 14, 14), fill=hexc('#2a2a30'))
    cols = [hexc(c)[:3] for c, *_ in [(x[2],) for x in CAB.WINGS]] if grand else [hexc(col)[:3]]
    for k in range(8):
        a0, a1 = k * 45, k * 45 + 40
        c = cols[k % len(cols)]
        shade = tuple(min(255, int(v * (1.0 if k % 2 else 0.75) + (40 if k % 2 else 0))) for v in c)
        d.pieslice((2, 2, 13, 13), a0, a1, fill=shade + (255,))
    d.ellipse((5, 5, 10, 10), fill=hexc('#ffe08a' if grand else '#f4f0e0'), outline=hexc('#2a2a30'))
    d.ellipse((1, 1, 14, 14), outline=hexc('#c89a3a'))
    return im


def textures():
    """the shipped textures: the draft's, with clear glass - opaque glints and a solid lip, nothing half see-through (a
    half-clear texture on a display hides what's drawn after it behind it, and darkens where two overlap), and gilded metal
    for the Golden Bowl"""
    from PIL import Image
    from tullius_art import _shine
    T_ = ART.textures()
    def clear(im, keep=200):
        o = Image.new('RGBA', im.size, (0, 0, 0, 0))
        for y in range(im.height):
            for x in range(im.width):
                r, g, b, a = im.getpixel((x, y))
                if a >= keep:
                    o.putpixel((x, y), (r, g, b, 255))
        return o
    T_['fy_glass'] = clear(T_['fy_glass'], 140)
    T_['fy_glass_b'] = clear(T_['fy_glass_b'], 255)
    T_['fy_lens'] = clear(T_['fy_lens'], 190)
    for k in ('fy_rim', 'fy_bubble'):
        im = T_[k].copy()
        for y in range(im.height):
            for x in range(im.width):
                r, g, b, a = im.getpixel((x, y))
                im.putpixel((x, y), (r, g, b, 255))
        T_[k] = im
    T_.update({'fy_gmetal': _shine('#c8962a', '#ffe070', 931), 'fy_gband': _shine('#e8b830', '#fff4b0', 932), 'fy_gdark': _shine('#8a6414', '#d8a42a', 933),
               'fy_gjoint': _shine('#f0c84a', '#fffbe0', 934)})
    return T_


GILD = {'fy_metal': 'fy_gmetal', 'fy_band': 'fy_gband', 'fy_dark': 'fy_gdark', 'fy_joint': 'fy_gjoint'}
GILT = ('body', 'legr', 'legl', 'armr', 'forer', 'arml', 'forel')          # (the Golden Bowl: these wear gold; the fish keeps his hat)


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    for name, (tex, els) in ART.models().items():
        R.HATS[name] = (tex, els)
        if name[len(ART.PREFIX):] in GILT:
            R.HATS[name + '_g'] = ({a: (f'bm:block/{GILD[v.split("/")[-1]]}' if v.split('/')[-1] in GILD else v) for a, v in tex.items()}, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (ART.PREFIX,)
    R.ICONS['fy_bowl'] = _bowl_icon()
    R.ICONS['cab_veiled'] = _veiled_icon()
    for w, n, c, d in CAB.WINGS:
        R.ICONS[f'cab_rosette_{w}'] = _rosette_icon(c)
    R.ICONS['cab_rosette_grand'] = _rosette_icon(GOLD, grand=True)
    cases = [(e, f'fy_fish_x{m}') for e, m in FACE_MODEL.items()]

    def post(R2):
        mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
        R2.wj('assets/bm/items/fy_fish.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                         'cases': [{'when': e, 'model': mdl(m)} for e, m in cases], 'fallback': mdl('fy_fish')}})
    R.POST.append(post)


# ================================================================================================= the datapack
def generate_early(G):
    """(after phase132, before phase137 reads the Recruiter's stock) his Raid Contract on the Recruiter's books"""
    fn, title, tellraw = G.fn, G.title, G.tellraw
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    # ---- his raid contract (the Recruiter: 1 Gutter Trophy + 3 Medallions)
    def signed():
        return ['scoreboard players operation #q bm.rng = @s bm.fcon', f'scoreboard players set #bit bm.rng {BIT}',
                'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng']
    GP = [T('[', 'dark_gray'), T('Heist', '#ffcf40', bold=True), T('] ', 'dark_gray')]
    fn('p145/sign', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                     'execute unless score @s bm.fcon matches 0.. run scoreboard players set @s bm.fcon 0'] + signed() +
       ['execute if score #q bm.rng matches 1 run return run ' + say('Fishy is already under contract.', 'gray'),
        f'scoreboard players add @s bm.fcon {BIT}', 'clear @s *[minecraft:custom_data~{bm:"fcontract_fishy"}] 1',
        'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.8', 'playsound minecraft:block.anvil.use player @s ~ ~ ~ 0.4 1.6',
        tellraw('@s', GP + [T('Signed! ', '#ffcf40', bold=True), T('Fishy', ORANGE, bold=True), T(' will answer your call in the vault from now on.', 'gray')])])
    fn('p145/ok', ['execute unless dimension bm:gutter run return run function bm:p74/fol_ok', 'execute unless entity @s[tag=bm.gvp] run return 0'] + signed() +
       ['execute if score #q bm.rng matches 1 run return 1',
        tellraw('@s', GP + [T('Fishy', ORANGE), T(' needs a ', 'gray'), T('Raid Contract', '#ffcf40'), T(' to come into the vault. The Recruiter in the den sells them.', 'gray')]), 'return 0'])

    from gen_dp import offer
    import phase103 as P103
    Lr = G.FUNCS['p70/r/lobby/init']
    k = next(i for i, l in enumerate(Lr) if l.startswith('summon minecraft:villager') and 'bm.gvrec' in l and 'Recipes:[' in l)
    o = offer(('gutter_trophy', 1), ('fcontract_fishy', 1), ('gutter_medallion', 3))
    Lr[k] = Lr[k].replace('Recipes:[', 'Recipes:[' + snbt(o) + ',', 1)
    P103.RECRUITER_OFFERS.append(o)


def generate(G):
    import phase28 as P28
    import phase73 as P73
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    fysay = lambda txt, who='@s': title(who, 'actionbar', [T('Fishy: ', ORANGE, bold=True), T(txt, LINE_C)])
    fychat = lambda txt, who='@s': tellraw(who, [T('Fishy: ', ORANGE, bold=True), T(f'"{txt}"', LINE_C)])
    CP = [T('[', 'dark_gray'), T('Cabinet', GOLD, bold=True), T('] ', 'dark_gray')]
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    tick, fast, second = [], [], []
    objs = ['bm.fys', 'bm.fyf', 'bm.fyx', 'bm.fya', 'bm.fym', 'bm.fyr', 'bm.fyu', 'bm.fysl', 'bm.fyz', 'bm.fyq', 'bm.fyh', 'bm.fycl', 'bm.fycd',
            'bm.fyfg', 'bm.fyl', 'bm.fyn', 'bm.fyns', 'bm.fynx', 'bm.cab', 'bm.cabc', 'bm.cabr', 'bm.cabp', 'bm.cabi']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + \
        [f'scoreboard players set #{n} bm.rng {n}' for n in (2, 6, 10, 16, 20, 24, 40, 48, 60, 64)]
    G.OBJECTIVES += objs
    foe = 'type=#bm:hostile,tag=!bm.npc'
    CAB.check(ITEMS)
    EX = [(w, i, k, ids, r) for w in WINGS for i, (k, ids, r) in enumerate(CAB.EXHIBITS[w])]
    NAME = {k: ITEMS[ids[0]]['name'] for w, i, k, ids, r in EX}
    WI = {w: n + 1 for n, w in enumerate(WINGS)}
    bitf = lambda obj, b: [f'scoreboard players operation #q bm.rng = @s {obj}', f'scoreboard players set #bit bm.rng {2 ** b}',
                           'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng']

    # ================================================================== THE RECORD (the world's: bm:cab got.<exhibit> = {by: "who showed it"})
    NUM = {k: j + 1 for j, (w, n, k, ids, r) in enumerate(EX)}
    cat = {i: Int(NUM[k]) for w, n, k, ids, r in EX for i in ids}
    fn('p145/recount', ['scoreboard players set #all bm.cab 0', 'scoreboard players set #done bm.cab 0'] +
       [l for w in WINGS for l in [f'scoreboard players set #{w} bm.cab 0'] +
        [f'execute if data storage bm:cab got.{k} run scoreboard players add #{w} bm.cab 1' for k, ids, r in CAB.EXHIBITS[w]] +
        [f'scoreboard players operation #all bm.cab += #{w} bm.cab', f'execute if score #{w} bm.cab matches 20.. run scoreboard players add #done bm.cab 1']])
    # (a wing's power, as a flag Fishy reads every tick: #f_<wing> 1 once all twenty are in; #cap, all six)
    fn('p145/flags', [l for w in WINGS for l in [f'scoreboard players set #f_{w} bm.cab 0', f'execute if score #{w} bm.cab matches 20.. run scoreboard players set #f_{w} bm.cab 1']] +
       ['scoreboard players set #cap bm.cab 0', 'execute if score #done bm.cab matches 6.. run scoreboard players set #cap bm.cab 1'])
    G.FUNCS['load'][-1:-1] = [f'data modify storage bm:cab cat set value {snbt(cat)}', 'function bm:p145/recount', 'function bm:p145/flags',
                              'execute unless score #hall bm.cab matches 1..6 run scoreboard players set #hall bm.cab 1']

    # ---- show him (as the player, holding it): a replica for the cabinet - the thing itself stays with you
    #      returns 1 if it was an exhibit (shown now, or shown before), 0 if not
    fn('p145/show', ['data remove storage bm:tmp cab', 'data modify storage bm:tmp cab.id set from entity @s SelectedItem.components."minecraft:custom_data".bm',
                     'execute unless data storage bm:tmp cab.id run return 0', 'function bm:p145/show_look with storage bm:tmp cab',
                     'execute unless data storage bm:tmp cab.k run return 0', 'function bm:p145/show_go with storage bm:tmp cab', 'return 1'])
    fn('p145/show_look', ['$data modify storage bm:tmp cab.k set from storage bm:cab cat."$(id)"'])
    fn('p145/show_go', ['$function bm:p145/ex/$(k)'])
    LINES = ['Magnificent! A perfect replica for the Cabinet - and the original stays with you, of course.',
             'Oh my. OH my. Hold still - I shall make a copy at once.', 'A splendid specimen! The Cabinet thanks you.',
             'I have dreamt of this one. Truly. One replica, coming up!', 'Exquisite. Into the Cabinet it goes - well, its twin does.']
    for w, i, k, ids, r in EX:
        col = WCOL[w]
        fn(f'p145/ex/{NUM[k]}', [f'execute if data storage bm:cab got.{k} run return run function bm:p145/already {{k:"{k}",n:"{NAME[k]}"}}',
                            'function bm:p28/name/of', f'data modify storage bm:cab got.{k}.by set from storage bm:tmp nm.name',
                            'execute unless data storage bm:cab got.' + k + '.by run data modify storage bm:cab got.' + k + '.by set value "someone"',
                            'function bm:p145/recount',
                            f'execute unless score @s bm.cabc matches 0.. run scoreboard players set @s bm.cabc 0'] + bitf('bm.cabc', WI[w] - 1) +
           [f'execute if score #q bm.rng matches 0 run scoreboard players add @s bm.cabc {2 ** (WI[w] - 1)}',
            'advancement grant @s only bm:story/cab_first',
            tellraw('@a', CP + [{'selector': '@s', 'color': 'white'}, T(' showed Fishy ', 'gray'), T(NAME[k], col, bold=True),
                                T(' - a replica stands in ', 'gray'), T(WNAME[w], col), T(' (', 'gray'), {'score': {'name': f'#{w}', 'objective': 'bm.cab'}, 'color': 'white'},
                                T(' of 20).', 'gray')]),
            f'execute store result score #r bm.rng run random value 0..{len(LINES) - 1}'] +
           [f'execute if score #r bm.rng matches {n} run ' + fychat(ln) for n, ln in enumerate(LINES)] +
           ['function bm:p145/replica_fx', f'execute if score #hall bm.cab matches {WI[w]} run function bm:p145/hall/show/{w}',
            f'execute if score #{w} bm.cab matches 20.. unless score #f_{w} bm.cab matches 1 run function bm:p145/wing_done/{w}'])
    fn('p145/already', ['$data modify storage bm:tmp cab.by set from storage bm:cab got."$(k)".by', '$data modify storage bm:tmp cab.n set value "$(n)"',
                        'function bm:p145/already2 with storage bm:tmp cab'])
    fn('p145/already2', ['$' + tellraw('@s', CP + [T('Fishy: ', ORANGE, bold=True), T('"Ah! $(n) - already in the Cabinet; $(by) showed me one. Lovely to see another."', LINE_C)]),
                         'playsound minecraft:entity.tropical_fish.flop neutral @s ~ ~ ~ 0.6 1.4'])
    # (the replica: a shimmer where Fishy is - at his desk, or your Fishy - and on you)
    fn('p145/replica_fx', ['particle minecraft:wax_on ~ ~1.2 ~ 0.4 0.5 0.4 0 20', 'particle minecraft:end_rod ~ ~1.2 ~ 0.3 0.4 0.3 0.05 14',
                           'playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..16] ~ ~ ~ 1 1.3',
                           'playsound minecraft:entity.villager.work_cartographer neutral @a[distance=..16] ~ ~ ~ 0.8 1.2',
                           'execute as @e[type=minecraft:interaction,tag=bm.fynhit,distance=..12,limit=1] run function bm:p145/npc/react_shock',
                           'execute as @e[type=minecraft:wolf,tag=bm.fypet,distance=..12] run function bm:p145/pet_shock'])

    # ---- a wing done: Fishy learns its power (every Fishy - the world's cabinet); everyone who gave to it, its rosette
    for w in WINGS:
        pw, pdesc = CAB.POWERS[w]
        fn(f'p145/wing_done/{w}', [f'scoreboard players set #f_{w} bm.cab 1', 'function bm:p145/flags',
                                   tellraw('@a', CP + [T(WNAME[w].upper(), WCOL[w], bold=True), T(' WING IS COMPLETE! ', WCOL[w], bold=True),
                                                       T('Every one of its twenty stands in Fishy\'s Cabinet.', 'gray')]),
                                   tellraw('@a', CP + [T('Fishy learns ', 'gray'), T(pw, ORANGE, bold=True), T(f' - {pdesc}. ', 'gray'),
                                                       T('Everyone who gave to it earns its rosette.', 'dark_gray')]),
                                   'execute as @a at @s run playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.8 1.1',
                                   'execute as @e[type=minecraft:interaction,tag=bm.fynhit,limit=1] run function bm:p145/npc/react_bow',
                                   'execute as @a[scores={bm.cabc=1..}] at @s run function bm:p145/claim_w',
                                   'execute if score #done bm.cab matches 6.. run function bm:p145/all_done'])
    fn('p145/all_done', [tellraw('@a', CP + [T('EVERY WING IS FULL. ', GOLD, bold=True), T('The Cabinet of Curiosities is complete - and Fishy\'s bowl turns to gold: ', 'gray'),
                                             T(CAB.CAPSTONE[0], GOLD, bold=True), T('.', 'gray')]),
                         'execute as @e[type=minecraft:wolf,tag=bm.fypet] at @s run function bm:p145/redress_any',
                         'execute as @a[scores={bm.cabc=1..}] at @s run function bm:p145/claim'])
    # (claims: as a player who gave something - each finished wing they gave to, once; the grand one, once, for anyone who gave at all)
    claim = []
    for w in WINGS:
        b = WI[w] - 1
        fn(f'p145/claim/{w}', [f'scoreboard players add @s bm.cabr {2 ** b}', f'advancement grant @s only bm:story/cab_{w}', give(f'cab_rosette_{w}'),
                               tellraw('@s', CP + [T('Fishy: ', ORANGE, bold=True), T(f'"You helped fill {WNAME[w]}. This rosette is yours - with my deepest bow."', LINE_C)]),
                               'playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1.2'])
        claim += [f'execute unless score #f_{w} bm.cab matches 1 run scoreboard players set #c{b} bm.rng 0', f'execute if score #f_{w} bm.cab matches 1 run scoreboard players set #c{b} bm.rng 1'] + \
            bitf('bm.cabc', b) + [f'execute if score #q bm.rng matches 0 run scoreboard players set #c{b} bm.rng 0'] + bitf('bm.cabr', b) + \
            [f'execute if score #q bm.rng matches 1 run scoreboard players set #c{b} bm.rng 0', f'execute if score #c{b} bm.rng matches 1 run function bm:p145/claim/{w}']
    fn('p145/claim/grand', [f'scoreboard players add @s bm.cabr {2 ** 6}', 'advancement grant @s only bm:story/cab_all', give('cab_rosette_grand'),
                            tellraw('@s', CP + [T('Fishy: ', ORANGE, bold=True), T('"The whole Cabinet, complete. I have no words. Well - one: THANK YOU."', LINE_C)])])
    fn('p145/claim_w', ['execute unless score @s bm.cabr matches 0.. run scoreboard players set @s bm.cabr 0'] + claim)
    fn('p145/claim', ['function bm:p145/claim_w', 'execute unless score #cap bm.cab matches 1 run return 0'] + bitf('bm.cabr', 6) +
       ['execute if score #q bm.rng matches 0 run function bm:p145/claim/grand'])
    second.append('execute if score #done bm.cab matches 1.. as @a[scores={bm.cabc=1..}] at @s run function bm:p145/claim')
    # the advancements
    wjson('bm/advancement/story/cab_first.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
          'display': {'icon': {'id': TOTEM, 'components': {'minecraft:item_model': 'bm:fy_bowl'}}, 'title': T('A Curious Mind', ORANGE),
                      'description': T('Show Fishy something for his Cabinet of Curiosities', 'gray'), 'frame': 'task', 'show_toast': True, 'announce_to_chat': True,
                      'hidden': False}})
    for w in WINGS:
        wjson(f'bm/advancement/story/cab_{w}.json', {'parent': 'bm:story/cab_first', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
              'display': {'icon': {'id': TOTEM, 'components': {'minecraft:item_model': f'bm:cab_rosette_{w}'}}, 'title': T(f'Curator of {WNAME[w]}', WCOL[w]),
                          'description': T(f'Help fill the Cabinet\'s {WNAME[w]} wing - all twenty', 'gray'), 'frame': 'goal', 'show_toast': True,
                          'announce_to_chat': True, 'hidden': False}})
    wjson('bm/advancement/story/cab_all.json', {'parent': 'bm:story/cab_first', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
          'display': {'icon': {'id': TOTEM, 'components': {'minecraft:item_model': 'bm:cab_rosette_grand'}}, 'title': T('The Golden Bowl', GOLD),
                      'description': T('Every wing of Fishy\'s Cabinet complete', 'gray'), 'frame': 'challenge', 'show_toast': True, 'announce_to_chat': True,
                      'hidden': False}})

    # ================================================================== THE MENU: the cabinet's pages (menu CABM)
    def ibody(i):
        return {'type': 'minecraft:item', 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'$(m_{i})',
                                                                                                            'minecraft:item_name': f'@@RAW:r_n{i}@@'}},
                'description': {'contents': f'@@RAW:r_d{i}@@', 'width': Int(250)}, 'show_decorations': B(0), 'show_tooltip': B(1), 'width': Int(22), 'height': Int(22)}
    # (each exhibit's three slots on its wing's page: m_<i> its model, r_n<i> its name, r_d<i> the line beside it)
    for w, i, k, ids, r in EX:
        col = WCOL[w]
        mdl = ITEMS[ids[0]]['comps'].get('minecraft:item_model', ITEMS[ids[0]]['base'])
        fn(f'p145/pg/x/{k}', [f'data modify storage bm:ui cab.m_{i} set value "{mdl}"', f'data modify storage bm:ui cab.r_n{i} set value {snbt(T(NAME[k], col, bold=True))}',
                              f'data modify storage bm:ui cab.r_d{i} set value {snbt([T(NAME[k], col, bold=True), T(chr(10) + "given by ", "gray"), T("", "white")])}',
                              f'data modify storage bm:ui cab.r_d{i}[2].text set from storage bm:cab got.{k}.by'])
        fn(f'p145/pg/v/{k}', [f'data modify storage bm:ui cab.m_{i} set value "bm:cab_veiled"', f'data modify storage bm:ui cab.r_n{i} set value {snbt(T("A veiled plinth", "dark_gray"))}',
                              f'data modify storage bm:ui cab.r_d{i} set value {snbt([T("? ? ?", "dark_gray", bold=True), T(chr(10) + r, "gray", italic=True)])}'])
    back = P28.btn([T('« The Cabinet', 'gray')], CABM, width=150)
    for w in WINGS:
        dlg = P28.multi([T(WNAME[w].upper(), WCOL[w], bold=True), T('  ·  ', 'gray'), T('$(n)', 'white', bold=True), T(' of 20', 'gray')],
                        [P28.body([T(WDESC[w] + ' ', 'gray'), T('Veiled ones carry a riddle - where such a thing is found.', 'dark_gray')], 330)] +
                        [ibody(i) for i in range(20)],
                        [P28.btn([T('Set it out in the hall', GOLD, bold=True)], CABM + 8, width=150,
                                 tooltip=T('Lay this wing\'s replicas in the cases of Fishy\'s hall (off the Fixer\'s Lounge).', 'gray')), back], columns=2, exit_label='Close')
        fn(f'p145/pg/{w}', [f'scoreboard players set @s bm.menu {CABM}', f'scoreboard players set @s bm.cabp {WI[w]}', 'data remove storage bm:ui cab',
                            f'execute store result storage bm:ui cab.n int 1 run scoreboard players get #{w} bm.cab'] +
           [l for k, ids, r in CAB.EXHIBITS[w] for l in (f'execute if data storage bm:cab got.{k} run function bm:p145/pg/x/{k}',
                                                         f'execute unless data storage bm:cab got.{k} run function bm:p145/pg/v/{k}')] +
           [f'function bm:p145/pg/{w}_dlg with storage bm:ui cab'])
        fn(f'p145/pg/{w}_dlg', [f'$dialog show @s {P28.inline(dlg)}'])
    # the front page: the wings, how full each is
    rows = []
    for w in WINGS:
        rows += [f'execute store result storage bm:ui cab.c_{w} int 1 run scoreboard players get #{w} bm.cab',
                 f'data modify storage bm:ui cab.r_{w} set value ""',
                 f'execute if score #f_{w} bm.cab matches 1 run data modify storage bm:ui cab.r_{w} set value {snbt(T("  ✔", "#7aff7a", bold=True))}']
    main = P28.multi([T("FISHY'S CABINET OF CURIOSITIES", GOLD, bold=True)],
                     [P28.body([T('Show Fishy one of the rare things of this world and he makes a replica for his cabinet - ', 'gray'),
                                T('you keep the thing itself.', 'white'), T(' One cabinet for the whole world: whoever shows him first, their name on the plaque.', 'gray')], 340),
                      P28.body([T('Exhibits: ', 'gray'), T('$(all)', 'white', bold=True), T(' of 120.  Wings complete: ', 'gray'), T('$(done)', 'white', bold=True),
                                T(' of 6.', 'gray')], 340)],
                     [P28.btn([T(WNAME[w], WCOL[w], bold=True), T('  '), T(f'$(c_{w})', 'white', bold=True), T(' of 20', 'gray'), f'@@RAW:r_{w}@@'], CABM + WI[w], width=170) for w in WINGS] +
                     [P28.btn([T("Fishy's powers", ORANGE, bold=True)], CABM + 7, width=170, tooltip=T('What each finished wing has taught him.', 'gray'))],
                     columns=2, exit_label='Close')
    fn('p145/cab/main', [f'scoreboard players set @s bm.menu {CABM}', 'data remove storage bm:ui cab',
                         'execute store result storage bm:ui cab.all int 1 run scoreboard players get #all bm.cab',
                         'execute store result storage bm:ui cab.done int 1 run scoreboard players get #done bm.cab'] + rows + ['function bm:p145/cab/main_dlg with storage bm:ui cab'])
    fn('p145/cab/main_dlg', [f'$dialog show @s {P28.inline(main)}'])
    # the powers page
    prow = []
    for w in WINGS:
        pw, pd = CAB.POWERS[w]
        prow += [f'data modify storage bm:ui cab.r_p{w} set value {snbt([T("locked", "dark_gray"), T(f" - finish {WNAME[w]}", "dark_gray")])}',
                 f'execute if score #f_{w} bm.cab matches 1 run data modify storage bm:ui cab.r_p{w} set value {snbt(T("LEARNED", "#7aff7a", bold=True))}']
    prow += [f'data modify storage bm:ui cab.r_pcap set value {snbt(T("locked - every wing", "dark_gray"))}',
             f'execute if score #cap bm.cab matches 1 run data modify storage bm:ui cab.r_pcap set value {snbt(T("HIS", GOLD, bold=True))}']
    pdlg = P28.multi([T("FISHY'S POWERS", ORANGE, bold=True), T('  ·  taught by the Cabinet', 'gray')],
                     [P28.body([T('A curator, not a brawler - at first. Every wing of the Cabinet finished teaches every Fishy something new, and toughens him.', 'gray')], 340)] +
                     [P28.body([T(CAB.POWERS[w][0], WCOL[w], bold=True), T(f' ({WNAME[w]}): {CAB.POWERS[w][1]}.  ', 'gray'), f'@@RAW:r_p{w}@@'], 340) for w in WINGS] +
                     [P28.body([T(CAB.CAPSTONE[0], GOLD, bold=True), T(f' (all six): {CAB.CAPSTONE[1]}.  ', 'gray'), '@@RAW:r_pcap@@'], 340)],
                     [back], columns=1, exit_label='Close')
    fn('p145/cab/powers', [f'scoreboard players set @s bm.menu {CABM}', 'data remove storage bm:ui cab'] + prow + ['function bm:p145/cab/powers_dlg with storage bm:ui cab'])
    fn('p145/cab/powers_dlg', [f'$dialog show @s {P28.inline(pdlg)}'])
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {CABM}..{CABM + 8} run return run function bm:p145/cab/act')
    fn('p145/cab/act', [f'execute unless score @s bm.menu matches {CABM} run return run function bm:p28/stale',
                        f'execute if score #act bm.pay matches {CABM} run return run function bm:p145/cab/main'] +
       [f'execute if score #act bm.pay matches {CABM + WI[w]} run return run function bm:p145/pg/{w}' for w in WINGS] +
       [f'execute if score #act bm.pay matches {CABM + 7} run return run function bm:p145/cab/powers',
        f'execute if score #act bm.pay matches {CABM + 8} run return run function bm:p145/cab/set_out'])
    fn('p145/cab/set_out', [f'execute if score @s bm.cabp matches {WI[w]} run function bm:p145/hall/show/{w}' for w in WINGS] +
       [say('The hall\'s cases now show that wing (Fishy\'s hall, off the Fixer\'s Lounge).', GOLD), 'playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 0.8 1.1'])

    # ================================================================== THE HALL (off the Fixer's Lounge, through its gilded gateway)
    lo, hi = f'{HX0} {OY + 3} {HZ0}', f'{HX1} {OY + 10} {HZ1}'
    slots = []                                    # (index 1-20, item-display position, yaw, label position)
    for row, y in enumerate((OY + 5, OY + 7)):
        for c, x in enumerate(COLS):
            slots.append((row * 5 + c + 1, (x + 0.5, y + 0.5, HZ0 + 0.55), 0, (x + 0.5, y - 0.42, HZ0 + 1.02)))
    for row, y in enumerate((OY + 5, OY + 7)):
        for c, x in enumerate(COLS):
            slots.append((10 + row * 5 + c + 1, (x + 0.5, y + 0.5, HZ1 + 0.45), 180, (x + 0.5, y - 0.42, HZ1 - 0.02)))
    ident = [F(0), F(0), F(0), F(1)]
    def disp(tags, extra=None):
        n = {'Tags': tags, 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:cab_veiled'}}, 'item_display': 'fixed',
             'brightness': {'block': Int(15), 'sky': Int(15)}, 'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0)] * 3, 'scale': [F(0.55)] * 3}}
        n.update(extra or {})
        return snbt(n)
    def label(tags, text, sc=0.32, width=150):
        return snbt({'Tags': tags, 'billboard': 'fixed', 'line_width': Int(width), 'background': Int(0x60000000), 'text': text, 'shadow': B(0),
                     'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0)] * 3, 'scale': [F(sc)] * 3}})
    build = [f'kill @e[tag=bm.cabprop,x={HX0 - 2},y={OY},z={HZ0 - 2},dx={HX1 - HX0 + 4},dy=14,dz={HZ1 - HZ0 + 4}]',
             f'fill {lo} {hi} minecraft:dark_oak_planks hollow',
             f'fill {HX0 + 1} {OY + 3} {HZ0 + 1} {HX1 - 1} {OY + 3} {HZ1 - 1} minecraft:polished_deepslate',
             f'fill {HX0 + 1} {OY + 3} {OZ + 11} {HX1 - 4} {OY + 3} {OZ + 13} minecraft:polished_blackstone_bricks',
             f'fill {HX0 + 1} {OY + 4} {OZ + 11} {HX1 - 5} {OY + 4} {OZ + 13} minecraft:red_carpet',
             # (the doorway: the lounge's gilded gate opened, and the hall's own wall)
             f'fill {OX + 24} {OY + 4} {OZ + 11} {OX + 25} {OY + 7} {OZ + 13} minecraft:air',
             f'fill {OX + 25} {OY + 8} {OZ + 10} {OX + 25} {OY + 8} {OZ + 14} minecraft:gold_block',
             f'fill {OX + 25} {OY + 4} {OZ + 10} {OX + 25} {OY + 7} {OZ + 10} minecraft:gold_block',
             f'fill {OX + 25} {OY + 4} {OZ + 14} {OX + 25} {OY + 7} {OZ + 14} minecraft:gold_block']
    # the long walls: dark oak, stripped-log pillars between the cases, a bookshelf frieze; each case a lit niche, quartz behind
    for z, zb in ((HZ0, HZ0 - 1), (HZ1, HZ1 + 1)):
        build += [f'fill {HX0 + 1} {OY + 4} {z} {HX1 - 1} {OY + 4} {z} minecraft:polished_blackstone_bricks',
                  f'fill {HX0 + 1} {OY + 9} {z} {HX1 - 1} {OY + 9} {z} minecraft:bookshelf']
        for x in range(COLS[0] - 1, COLS[-1] + 2, 2):
            build.append(f'fill {x} {OY + 5} {z} {x} {OY + 8} {z} minecraft:stripped_dark_oak_log[axis=y]')
        for x in COLS:
            for y in (OY + 5, OY + 7):
                build += [f'setblock {x} {y} {z} minecraft:light[level=11,waterlogged=false]', f'setblock {x} {y} {zb} minecraft:smooth_quartz']
    # Fishy's corner: his desk, a stained-glass window behind him, a lantern each side
    build += [f'fill {OX + 38} {OY + 4} {OZ + 10} {OX + 38} {OY + 4} {OZ + 14} minecraft:dark_oak_planks',
              f'fill {OX + 38} {OY + 5} {OZ + 10} {OX + 38} {OY + 5} {OZ + 14} minecraft:dark_oak_slab[type=bottom,waterlogged=false]',
              f'setblock {OX + 38} {OY + 4} {OZ + 9} minecraft:dark_oak_planks', f'setblock {OX + 38} {OY + 4} {OZ + 15} minecraft:dark_oak_planks',
              f'setblock {OX + 38} {OY + 5} {OZ + 9} minecraft:lantern[hanging=false,waterlogged=false]',
              f'setblock {OX + 38} {OY + 5} {OZ + 15} minecraft:lantern[hanging=false,waterlogged=false]']
    glass = ['orange', 'yellow', 'light_blue', 'cyan', 'magenta', 'lime', 'pink', 'purple']
    for dz in range(-2, 3):
        for dy in range(0, 3):
            build += [f'setblock {HX1} {OY + 6 + dy} {OZ + 12 + dz} minecraft:{glass[(dz + 2 + dy * 3) % len(glass)]}_stained_glass',
                      f'setblock {HX1 + 1} {OY + 6 + dy} {OZ + 12 + dz} minecraft:sea_lantern']
    for x in (OX + 30, OX + 34):
        build += [f'setblock {x} {OY + 9} {OZ + 12} minecraft:iron_chain[axis=y,waterlogged=false]', f'setblock {x} {OY + 8} {OZ + 12} minecraft:lantern[hanging=true,waterlogged=false]']
    # the cases' replicas and plaques, the banner over Fishy, the sign over the doorway
    for i, (x, y, z), yaw, (lx, ly, lz) in slots:
        build += [f'summon minecraft:item_display {x:.2f} {y:.2f} {z:.2f} {disp(["bm.cabprop", "bm.cabslot", "bm.cabnew"])}',
                  f'summon minecraft:text_display {lx:.2f} {ly:.2f} {lz:.2f} {label(["bm.cabprop", "bm.cablbl", "bm.cabnew"], T("? ? ?", "dark_gray"))}',
                  f'scoreboard players set @e[tag=bm.cabnew] bm.cabi {i}', f'execute as @e[tag=bm.cabnew] at @s run tp @s ~ ~ ~ {yaw} 0', 'tag @e[tag=bm.cabnew] remove bm.cabnew']
    build += [f'summon minecraft:text_display {HX1 - 0.02:.2f} {OY + 5.6:.2f} {OZ + 12.5:.2f} {label(["bm.cabprop", "bm.cabban"], T("THE CABINET", GOLD, bold=True), 0.6, 220)}',
              f'execute as @e[type=minecraft:text_display,tag=bm.cabban] run tp @s ~ ~ ~ 90 0',
              f'summon minecraft:text_display {OX + 23.9:.2f} {OY + 8.4:.2f} {OZ + 12.5:.2f} ' +
              label(['bm.cabprop', 'bm.cabsign'], [T("FISHY'S CABINET\n", GOLD, bold=True), T('of Curiosities ›', '#e8c070')], 0.55, 200),
              f'execute as @e[type=minecraft:text_display,tag=bm.cabsign] run tp @s ~ ~ ~ 90 0',
              f'summon minecraft:text_display {HX0 + 0.98:.2f} {OY + 8.1:.2f} {OZ + 12.5:.2f} ' +
              label(['bm.cabprop', 'bm.cabsign2'], [T('Show Fishy a rare thing: a replica for his cabinet. ', 'gray'), T('You keep yours.', 'white')], 0.4, 200),
              f'execute as @e[type=minecraft:text_display,tag=bm.cabsign2] run tp @s ~ ~ ~ -90 0',
              f'execute positioned {DESK[0]} {DESK[1]} {DESK[2]} rotated 90 0 run function bm:p145/npc/spawn',
              f'data modify storage bm:cab built set value {HALL_VER}', 'function bm:p145/hall/now']
    fn('p145/hall/build', build)
    fn('p145/hall/now', [f'execute if score #hall bm.cab matches {WI[w]} run function bm:p145/hall/show/{w}' for w in WINGS])
    G.FUNCS['load'][-1:-1] = [f'execute in bm:gutter run forceload add {HX0 - 1} {HZ0 - 1} {HX1 + 2} {HZ1 + 2}']
    second.append(f'execute in bm:gutter if loaded {HX0} {OY} {HZ0} if data storage bm:lg {{built:{P121.VER}}} unless data storage bm:cab {{built:{HALL_VER}}} run function bm:p145/hall/build')
    # (the lounge rebuilt: the hall's doorway opened again; the lounge's own prop that walled it up, gone)
    G.FUNCS['p121/build'].append('data remove storage bm:cab built')
    pr = G.FUNCS['p121/props']
    gate = [i for i, l in enumerate(pr) if l.startswith('fill ~13 ~ ~-3 ~13 ~5 ~3 ')]       # (x 25 of the template: the way on into a heist)
    assert len(gate) == 1, "the lounge's walled-up gateway was not found"
    pr.pop(gate[0])
    # the replicas: as the wing's page - the thing itself, or the veil; and the plaque under it
    for w, i, k, ids, r in EX:
        s = i + 1
        sel_i = f'@e[type=minecraft:item_display,tag=bm.cabslot,scores={{bm.cabi={s}}},limit=1]'
        sel_l = f'@e[type=minecraft:text_display,tag=bm.cablbl,scores={{bm.cabi={s}}},limit=1]'
        fn(f'p145/hall/x/{k}', [f'execute as {sel_i} run loot replace entity @s contents loot bm:items/{ids[0]}',
                                f'data modify storage bm:ui lbl set value {snbt([T(NAME[k], WCOL[w], bold=True), T(chr(10) + "given by ", "gray"), T("", "white")])}',
                                f'data modify storage bm:ui lbl[2].text set from storage bm:cab got.{k}.by', f'data modify entity {sel_l} text set from storage bm:ui lbl'])
        fn(f'p145/hall/v/{k}', [f'item replace entity {sel_i} contents with minecraft:paper[minecraft:item_model="bm:cab_veiled"]',
                                f'data modify entity {sel_l} text set value {snbt([T("? ? ?", "dark_gray", bold=True), T(chr(10) + r, "gray", italic=True)])}'])
    for w in WINGS:
        fn(f'p145/hall/show/{w}', [f'scoreboard players set #hall bm.cab {WI[w]}'] +
           [l for k, ids, r in CAB.EXHIBITS[w] for l in (f'execute if data storage bm:cab got.{k} run function bm:p145/hall/x/{k}',
                                                         f'execute unless data storage bm:cab got.{k} run function bm:p145/hall/v/{k}')] +
           [f'execute store result storage bm:ui ban.n int 1 run scoreboard players get #{w} bm.cab', f'function bm:p145/hall/ban_{w} with storage bm:ui ban'])
        fn(f'p145/hall/ban_{w}', ['$data modify entity @e[type=minecraft:text_display,tag=bm.cabban,limit=1] text set value ' +
                                  snbt([T(WNAME[w].upper(), WCOL[w], bold=True), T('\n$(n)', 'white'), T(' of 20', 'gray')])])

    # ================================================================== FISHY AT HIS DESK (his rig, still; his click box)
    nsel = lambda p=None: '@e[type=minecraft:item_display,tag=bm.fyn' + (f',tag=bm.fyp_{p}' if p else '') + ',distance=..4]'
    fn('p145/npc/spawn', [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, ["bm.fyp", f"bm.fyp_{p}", "bm.fyn", "bm.cabprop"], SP, extra={"brightness": {"block": Int(14), "sky": Int(14)}, "shadow_radius": F(0.5 if p == "body" else 0.0), "shadow_strength": F(0.5)})}'
                          for p in A.PARTS] +
       [f'summon minecraft:interaction ~ ~ ~ {snbt({"Tags": ["bm.fynhit", "bm.cabprop"], "width": F(1.2), "height": F(1.9), "response": B(1)})}',
        'function bm:p145/npc/place', 'scoreboard players set @e[type=minecraft:interaction,tag=bm.fynhit,distance=..1] bm.fyns 0'])
    fn('p145/npc/place', RF.place(A, UP, nsel))
    # his states: 0 idle (the fish laps his bowl), 1 points (the menu), 2 shocked (the monocle pops: a new exhibit), 3 bows (a wing done), 4 waves (hello)
    NCYC = {0: (8 * 6, [(6 * i, f'swim_{i}') for i in range(ART.LAP)]), 1: (None, [(0, 'point')]), 2: (None, [(0, 'shock'), (16, 'idle_a')]),
            3: (None, [(0, 'bow'), (24, 'idle_a')]), 4: (None, [(0, 'wave_a'), (6, 'wave_b'), (12, 'wave_a'), (18, 'wave_b'), (24, 'idle_a')])}
    used_n = {p for _per, frames in NCYC.values() for _t, p in frames}
    for name in used_n:
        fn(f'p145/npc/pose/{name}', pose_lines(POSES[name], DUR.get(name, 6), nsel, swap_face=True))
    RF.cycles(fn, 'p145/npc', NCYC, 'bm.fyn', 'bm.fyns', lambda p: f'p145/npc/pose/{p}')
    G.FUNCS['load'][-1:-1] = [f'scoreboard players set #{n} bm.rng {n}' for n in RF.periods(NCYC) if n not in (2, 6, 10, 16, 20, 24, 40, 48, 60, 64)]
    tick.append('execute as @e[type=minecraft:interaction,tag=bm.fynhit] at @s if entity @a[distance=..24] run function bm:p145/npc/tick')
    fn('p145/npc/tick', ['scoreboard players add @s bm.fyn 1', 'execute if score @s bm.fynx matches 1.. run scoreboard players remove @s bm.fynx 1',
                         'execute if score @s bm.fyns matches 1.. unless score @s bm.fynx matches 1.. run function bm:p145/npc/calm',
                         'execute if score @s bm.fyns matches 0 if entity @a[distance=..6,tag=!bm.fyseen] run function bm:p145/npc/hello',
                         'tag @a[distance=12..40,tag=bm.fyseen] remove bm.fyseen',
                         'function bm:p145/npc/anim',
                         'execute if score @s bm.fyns matches 0 if score #fxk bm.fxt matches 0 if predicate bm:p141/now_and_then run particle minecraft:bubble_pop ~ ~2.0 ~ 0.2 0.2 0.2 0 2'])
    fn('p145/npc/calm', ['scoreboard players set @s bm.fyns 0', 'scoreboard players set @s bm.fyn 0'])
    fn('p145/npc/hello', ['tag @a[distance=..6] add bm.fyseen', 'scoreboard players set @s bm.fyns 4', 'scoreboard players set @s bm.fyn 0', 'scoreboard players set @s bm.fynx 30',
                          'playsound minecraft:entity.tropical_fish.flop neutral @a[distance=..12] ~ ~ ~ 0.6 1.5'])
    for st, t, nm in ((1, 40, 'point'), (2, 30, 'shock'), (3, 40, 'bow')):
        fn(f'p145/npc/react_{nm}', [f'scoreboard players set @s bm.fyns {st}', 'scoreboard players set @s bm.fyn 0', f'scoreboard players set @s bm.fynx {t}'])
    # his click box: empty-handed - the menu (and the first time, he joins you); holding one of the rare things - shown; anything else - a word
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.fynhit] if data entity @s interaction at @s run function bm:p145/npc/clicked',
             'execute as @e[type=minecraft:interaction,tag=bm.fynhit] if data entity @s attack run data remove entity @s attack']
    fn('p145/npc/clicked', ['execute on target run function bm:p145/npc/click', 'data remove entity @s interaction'])
    fn('p145/npc/click', ['execute if score @s bm.fycl matches 1.. run return 0', 'scoreboard players set @s bm.fycl 8',
                          'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                          'execute if function bm:p145/show run return 1',
                          'execute if data entity @s SelectedItem.components."minecraft:custom_data".bm unless function bm:p145/hand_free run return run function bm:p145/not_ex',
                          'execute unless entity @s[tag=bm.fymet] run return run function bm:p145/recruit',
                          'function bm:p145/reissue',
                          'execute as @e[type=minecraft:interaction,tag=bm.fynhit,distance=..8,limit=1] run function bm:p145/npc/react_point',
                          'function bm:p145/cab/main'])
    tick.append('scoreboard players remove @a[scores={bm.fycl=1..}] bm.fycl 1')
    # (what the lounge puts in your hand - its Locker Key - your Ledger, his own bowl: as good as an empty hand)
    fn('p145/hand_free', [f'execute if items entity @s weapon.mainhand {holds(i)} run return 1' for i in ('locker_key', 'fixers_ledger', 'fy_bowl')] + ['return 0'])
    NOT_EX = ['Charming! But not quite a Cabinet piece. Keep looking!', 'Hmm. Useful, certainly. Rare? Not rare enough, I fear.',
              'A fine thing - but the Cabinet wants stranger things than this.']
    fn('p145/not_ex', [f'execute store result score #r bm.rng run random value 0..{len(NOT_EX) - 1}'] +
       [f'execute if score #r bm.rng matches {n} run ' + fysay(ln) for n, ln in enumerate(NOT_EX)] +
       ['playsound minecraft:entity.tropical_fish.flop neutral @s ~ ~ ~ 0.5 1.2'])
    fn('p145/recruit', ['tag @s add bm.fymet', give('fy_bowl'),
                        tellraw('@s', [T('Fishy: ', ORANGE, bold=True), T('"A visitor! Welcome, welcome to my Cabinet of Curiosities. Such a lot of empty plinths, I\'m afraid."', LINE_C)]),
                        tellraw('@s', [T('Fishy: ', ORANGE, bold=True), T('"Here - my Pocket Bowl. Call me, and I shall come along with you: a curator must see the world. '
                                                                          'I am no fighter, mind - not yet. But show me the rare things you find, and the Cabinet will teach me."', LINE_C)]),
                        tellraw('@s', [T('Fishy ', ORANGE, bold=True), T('tips his hat and presses a tiny fishbowl into your hand. (Use it to call him; sneak + use: his menu. '
                                                                         'Right-click him empty-handed here: the Cabinet.)', 'gray', italic=True)]),
                        'execute as @e[type=minecraft:interaction,tag=bm.fynhit,distance=..8,limit=1] run function bm:p145/npc/react_bow',
                        'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.4'])
    has = lambda iid: [f'execute if items entity @s container.* {holds(iid)} run scoreboard players set #has bm.rng 1',
                       f'execute if items entity @s weapon.offhand {holds(iid)} run scoreboard players set #has bm.rng 1',
                       f'execute if items entity @s enderchest.* {holds(iid)} run scoreboard players set #has bm.rng 1']
    fn('p145/reissue', ['scoreboard players set #has bm.rng 0'] + has('fy_bowl') +
       ['scoreboard players operation #me bm.pid = @s bm.pid', 'execute as @e[type=minecraft:wolf,tag=bm.fypet] if score @s bm.pid = #me bm.pid run scoreboard players set #has bm.rng 1',
        'execute if score #has bm.rng matches 1 run return 0', give('fy_bowl'), fychat('Lost my Pocket Bowl? I always carry a spare. Do keep this one safe.')])

    # ================================================================== FISHY, THE FOLLOWER (a tamed wolf under his rig)
    def psel(p=None):
        return '@e[type=minecraft:item_display,tag=bm.fysel' + (f',tag=bm.fyp_{p}]' if p else ']')
    sel_pet = 'execute as @e[type=minecraft:wolf,tag=bm.fypet] if score @s bm.pid = #me bm.pid'
    face = lambda e, t: FX.face_cmd('fishy', e, t)
    rig = [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, ["bm.fyp", f"bm.fyp_{p}", "bm.fyp_pet", "bm.fynew"], SP, extra={"shadow_radius": F(0.5 if p == "body" else 0.0), "shadow_strength": F(0.5)})}'
           for p in A.PARTS]
    fn('p145/place', RF.place(A, UP, psel))
    fn('p145/burst', ['particle minecraft:splash ~ ~1 ~ 0.4 0.8 0.4 0.1 40', 'particle minecraft:bubble_pop ~ ~1 ~ 0.4 0.6 0.4 0.05 30',
                      'particle minecraft:flash{color:[1.0,0.7,0.3,1.0]} ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:wax_on ~ ~1.2 ~ 0.4 0.5 0.4 0 12'])
    # states: 0 idle (laps), 1 walk, 2 run, 3 air, 4 sit, 6 arriving (his bow), 7 strike, 8 coin toss, 9 splash, 10 swim, 11 thunder, 12 the Grand Exhibition, 13 zap
    CYCLE = {0: (8 * 6, [(6 * i, f'swim_{i}') for i in range(ART.LAP)]), 1: (16, [(0, 'walk_a'), (8, 'walk_b')]), 2: (10, [(0, 'run_a'), (5, 'run_b')]),
             3: (None, [(0, 'air')]), 4: (40, [(0, 'sit'), (20, 'sit_b')]), 6: (None, [(0, 'bow')]), 7: (None, [(0, 'strike_back'), (4, 'strike')]),
             8: (None, [(0, 'toss')]), 9: (None, [(0, 'splash')]), 10: (24, [(0, 'paddle_a'), (12, 'paddle_b')]), 11: (None, [(0, 'thunder_up'), (6, 'thunder')]),
             12: (None, [(0, 'ult')]), 13: (None, [(0, 'point'), (5, 'zap')])}
    RF.cycles(fn, 'p145', CYCLE, 'bm.fyf', 'bm.fys', lambda p: f'p145/pose/{p}')
    used = {p for _per, frames in CYCLE.values() for _t, p in frames}
    for name in used:
        fn(f'p145/pose/{name}', pose_lines(POSES[name], DUR.get(name, 6), psel))
    G.FUNCS['load'][-1:-1] = [f'scoreboard players set #{n} bm.rng {n}' for n in RF.periods(CYCLE) if n not in (2, 6, 10, 16, 20, 24, 40, 48, 60, 64)]
    fn('p145/state', ['execute if score @s bm.fysl matches 1.. run return run scoreboard players set #st bm.rng 6',
                      'execute if score @s bm.fyx matches 1.. run return run scoreboard players operation #st bm.rng = @s bm.fya',
                      'execute if data entity @s {Sitting:1b} run return run scoreboard players set #st bm.rng 4',
                      'execute store result score #og bm.rng run data get entity @s OnGround',
                      'execute if score #og bm.rng matches 0 if predicate bm:swim run return run scoreboard players set #st bm.rng 10',
                      'execute if score #og bm.rng matches 0 run scoreboard players add @s bm.fyz 1', 'execute if score #og bm.rng matches 1 run scoreboard players set @s bm.fyz 0',
                      'execute if score @s bm.fyz matches 4.. unless block ~ ~ ~ minecraft:water run return run scoreboard players set #st bm.rng 3',
                      'execute store result score #vx bm.rng run data get entity @s Motion[0] 1000', 'execute store result score #vz bm.rng run data get entity @s Motion[2] 1000',
                      'scoreboard players operation #vx bm.rng *= #vx bm.rng', 'scoreboard players operation #vz bm.rng *= #vz bm.rng',
                      'scoreboard players operation #vx bm.rng += #vz bm.rng',
                      'execute if score #vx bm.rng matches 30000.. run return run scoreboard players set #st bm.rng 2',
                      'execute if score #vx bm.rng matches 500.. run return run scoreboard players set #st bm.rng 1',
                      'scoreboard players set #st bm.rng 0'])
    tick.append('execute as @e[type=minecraft:wolf,tag=bm.fypet] at @s run function bm:p145/tick')
    idle_fight = 'unless score @s bm.fyx matches 1.. unless data entity @s {Sitting:1b}'
    fn('p145/tick', ['scoreboard players operation #me bm.pid = @s bm.pid',
                     'execute as @e[type=minecraft:item_display,tag=bm.fyp_pet,tag=!bm.fyfade] if score @s bm.pid = #me bm.pid run tag @s add bm.fysel',
                     f'execute unless entity {psel("fish")} run function bm:p145/rerig',
                     'execute if score @s bm.fyx matches 1.. run function bm:p145/act_tick',
                     'execute if score @s bm.fym matches 1.. run scoreboard players remove @s bm.fym 1',
                     'execute if score @s bm.fyr matches 1.. run scoreboard players remove @s bm.fyr 1',
                     'execute if score @s bm.fyu matches 1.. run scoreboard players remove @s bm.fyu 1',
                     'execute if score @s bm.fysl matches 1.. run scoreboard players remove @s bm.fysl 1',
                     # his fights: the Grand Exhibition (the Golden Bowl); the splash when they crowd him (the Deep); his claws up close; at range, coins or the ray
                     f'execute if score #cap bm.cab matches 1 {idle_fight} unless score @s bm.fyu matches 1.. if entity @e[{foe},distance=..7] run function bm:p145/ult_go',
                     f'execute if score #f_deep bm.cab matches 1 {idle_fight} unless score @s bm.fyr matches 1.. if entity @e[{foe},distance=..3.5] run function bm:p145/splash_go',
                     f'execute {idle_fight} unless score @s bm.fym matches 1.. if entity @e[{foe},distance=..2.8] run function bm:p145/strike_go',
                     f'execute if score #f_skies bm.cab matches 1 {idle_fight} unless score @s bm.fyr matches 1.. unless entity @e[{foe},distance=..2.8] if entity @e[{foe},distance=..16] run function bm:p145/zap_go',
                     f'execute if score #f_gutter bm.cab matches 1 {idle_fight} unless score @s bm.fyr matches 1.. unless entity @e[{foe},distance=..2.8] if entity @e[{foe},distance=..10] run function bm:p145/toss_go',
                     'function bm:p145/state',
                     'execute if score #st bm.rng = @s bm.fys run scoreboard players add @s bm.fyf 1',
                     'execute unless score #st bm.rng = @s bm.fys run scoreboard players set @s bm.fyf 0',
                     'scoreboard players operation @s bm.fys = #st bm.rng',
                     'function bm:p145/anim',
                     'execute on owner run tag @s add bm.fyown',
                     f'execute if score @s bm.fys matches 7..9 if entity @e[{foe},distance=..17] facing entity @e[{foe},distance=..17,sort=nearest,limit=1] feet rotated ~ 0 run function bm:p145/place',
                     f'execute if score @s bm.fys matches 11..13 if entity @e[{foe},distance=..17] facing entity @e[{foe},distance=..17,sort=nearest,limit=1] feet rotated ~ 0 run function bm:p145/place',
                     f'execute if score @s bm.fys matches 7..9 unless entity @e[{foe},distance=..17] rotated as @s rotated ~ 0 run function bm:p145/place',
                     f'execute if score @s bm.fys matches 11..13 unless entity @e[{foe},distance=..17] rotated as @s rotated ~ 0 run function bm:p145/place',
                     'execute if score @s bm.fys matches 0 run function bm:p145/face_you', 'execute if score @s bm.fys matches 4 run function bm:p145/face_you',
                     'execute if score @s bm.fys matches 6 run function bm:p145/face_you',
                     'execute if score @s bm.fys matches 1..3 rotated as @s rotated ~ 0 run function bm:p145/place',
                     'execute if score @s bm.fys matches 10 rotated as @s rotated ~ 0 positioned ~ ~0.2 ~ run function bm:p145/place',
                     'function bm:p145/box',
                     'tag @a[tag=bm.fyown] remove bm.fyown', 'tag @e[tag=bm.fysel] remove bm.fysel'])
    fn('p145/face_you', ['execute if entity @a[tag=bm.fyown,distance=1.5..10] facing entity @a[tag=bm.fyown,limit=1] feet rotated ~ 0 run return run function bm:p145/place',
                         'execute rotated as @s rotated ~ 0 run function bm:p145/place'])
    # ---- his blows: weak at first (2), 1 more for every wing finished; the Hollow's withering claws +3
    fn('p145/strike_go', ['scoreboard players set @s bm.fya 7', 'scoreboard players set @s bm.fyx 9', 'scoreboard players set @s bm.fym 24',
                          'playsound minecraft:entity.player.attack.sweep neutral @a[distance=..12] ~ ~ ~ 0.5 1.4'])
    fn('p145/toss_go', ['scoreboard players set @s bm.fya 8', 'scoreboard players set @s bm.fyx 10', 'scoreboard players set @s bm.fyr 40'])
    fn('p145/zap_go', ['scoreboard players set @s bm.fya 13', 'scoreboard players set @s bm.fyx 12', 'scoreboard players set @s bm.fyr 60',
                       'playsound minecraft:block.beacon.power_select neutral @a[distance=..16] ~ ~ ~ 0.5 1.8'])
    fn('p145/splash_go', ['scoreboard players set @s bm.fya 9', 'scoreboard players set @s bm.fyx 10', 'scoreboard players set @s bm.fyr 100'])
    fn('p145/thunder_go', ['scoreboard players set @s bm.fyh 0', 'scoreboard players set @s bm.fya 11', 'scoreboard players set @s bm.fyx 14', 'scoreboard players set @s bm.fym 30'] +
       face('surprised', 14))
    fn('p145/ult_go', ['scoreboard players set @s bm.fya 12', 'scoreboard players set @s bm.fyx 30', 'scoreboard players set @s bm.fyu 600',
                       'playsound minecraft:block.beacon.activate neutral @a[distance=..24] ~ ~ ~ 1 1.4'] + face('happy', 30))
    fn('p145/act_tick', ['scoreboard players remove @s bm.fyx 1',
                         'execute if score @s bm.fya matches 7 if score @s bm.fyx matches 4 run function bm:p145/strike_hit',
                         'execute if score @s bm.fya matches 8 if score @s bm.fyx matches 5 run function bm:p145/toss_hit',
                         'execute if score @s bm.fya matches 13 if score @s bm.fyx matches 6 run function bm:p145/zap_hit',
                         'execute if score @s bm.fya matches 9 if score @s bm.fyx matches 6 run function bm:p145/splash_hit',
                         'execute if score @s bm.fya matches 11 if score @s bm.fyx matches 7 run function bm:p145/thunder_hit',
                         'execute if score @s bm.fya matches 12 if score @s bm.fyx matches 20..29 run function bm:p145/ult_spin',
                         'execute if score @s bm.fya matches 12 if score @s bm.fyx matches 18 run function bm:p145/ult_hit'])
    dmg = ['scoreboard players set #pd bm.rng 2', 'scoreboard players operation #pd bm.rng += #done bm.cab']
    fn('p145/strike_hit', ['tag @s add bm.fyme'] + dmg + ['execute if score #f_hollow bm.cab matches 1 run scoreboard players add #pd bm.rng 3',
                                                          'playsound minecraft:entity.tropical_fish.flop neutral @a[distance=..12] ~ ~ ~ 0.8 0.8',
                                                          f'execute as @e[{foe},distance=..3.4,sort=nearest,limit=1] at @s run function bm:p145/clawed',
                                                          'tag @s remove bm.fyme', 'function bm:p145/blow'])
    fn('p145/clawed', ['function bm:p145/hurt', 'particle minecraft:crit ~ ~1 ~ 0.3 0.3 0.3 0.2 6',
                       'execute if score #f_hollow bm.cab matches 1 run effect give @s minecraft:wither 3 0',
                       'execute if score #f_hollow bm.cab matches 1 run particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.4 0.3 0.02 6'])
    fn('p145/hurt', ['execute store result storage bm:tmp fy.d int 1 run scoreboard players get #pd bm.rng', 'function bm:p145/dmg with storage bm:tmp fy'])
    fn('p145/dmg', ['$damage @s $(d) minecraft:mob_attack by @e[type=minecraft:wolf,tag=bm.fyme,limit=1]'])
    # the Gutter: gold coins flung at a foe (a little trail of them, a clink)
    fn('p145/toss_hit', ['tag @s add bm.fyme', 'scoreboard players set #pd bm.rng 4', 'scoreboard players operation #pd bm.rng += #done bm.cab',
                         'playsound minecraft:entity.experience_orb.pickup neutral @a[distance=..16] ~ ~ ~ 0.6 0.6',
                         f'execute facing entity @e[{foe},distance=..11,sort=nearest,limit=1] eyes positioned ^ ^1.4 ^ run function bm:p145/coin_trail',
                         f'execute as @e[{foe},distance=..11,sort=nearest,limit=1] at @s run function bm:p145/coined', 'tag @s remove bm.fyme', 'function bm:p145/blow'])
    fn('p145/coin_trail', [f'particle minecraft:item{{item:"minecraft:gold_nugget"}} ^ ^ ^{d} 0.05 0.05 0.05 0.02 2' for d in range(1, 11)])
    fn('p145/coined', ['function bm:p145/hurt', 'particle minecraft:item{item:"minecraft:gold_ingot"} ~ ~1.2 ~ 0.3 0.3 0.3 0.1 8',
                       'playsound minecraft:block.chain.hit neutral @a[distance=..16] ~ ~ ~ 0.8 1.6'])
    # the Skies: a Vorn ray from his bowl
    fn('p145/zap_hit', ['tag @s add bm.fyme', 'scoreboard players set #pd bm.rng 6', 'scoreboard players operation #pd bm.rng += #done bm.cab',
                        'playsound minecraft:entity.guardian.attack neutral @a[distance=..16] ~ ~ ~ 0.4 2',
                        f'execute facing entity @e[{foe},distance=..17,sort=nearest,limit=1] eyes positioned ^ ^1.5 ^ run function bm:p145/ray',
                        f'execute as @e[{foe},distance=..17,sort=nearest,limit=1] at @s run function bm:p145/rayed', 'tag @s remove bm.fyme', 'function bm:p145/blow'])
    fn('p145/ray', [f'particle minecraft:dust{{color:[0.3,1.0,0.5],scale:0.8}} ^ ^ ^{d / 2:.1f} 0 0 0 0 1' for d in range(1, 33)])
    fn('p145/rayed', ['function bm:p145/hurt', 'particle minecraft:glow ~ ~1 ~ 0.3 0.4 0.3 0.02 10', 'effect give @s minecraft:glowing 3 0 true'])
    # the Deep: a jet of water from his bowl - foes round him shoved back and slowed
    fn('p145/splash_hit', ['tag @s add bm.fyme', 'scoreboard players set #pd bm.rng 3', 'scoreboard players operation #pd bm.rng += #done bm.cab',
                           'particle minecraft:splash ~ ~1.6 ~ 1.5 0.4 1.5 0.3 80', 'particle minecraft:bubble_pop ~ ~1.2 ~ 1.5 0.5 1.5 0.05 30',
                           'playsound minecraft:entity.player.splash.high_speed neutral @a[distance=..16] ~ ~ ~ 1 1.1',
                           f'execute as @e[{foe},distance=..4.5] at @s run function bm:p145/splashed', 'tag @s remove bm.fyme', 'function bm:p145/blow'])
    fn('p145/splashed', ['function bm:p145/hurt', 'effect give @s minecraft:slowness 4 2',
                         'execute facing entity @e[type=minecraft:wolf,tag=bm.fyme,limit=1] feet positioned ^ ^ ^-1.4 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~ ~'])
    # the Wilds: every sixth blow, a thunderclap round him
    fn('p145/blow', ['scoreboard players add @s bm.fyh 1', 'scoreboard players add @s bm.fyq 1', 'execute if score @s bm.fyq matches 8.. run function bm:p145/quip',
                     'execute if score #f_wilds bm.cab matches 1 if score @s bm.fyh matches 6.. run function bm:p145/thunder_go'])
    fn('p145/thunder_hit', ['tag @s add bm.fyme', 'scoreboard players set #pd bm.rng 8', 'scoreboard players operation #pd bm.rng += #done bm.cab',
                            'particle minecraft:electric_spark ~ ~1 ~ 2.5 0.6 2.5 0.4 80', 'particle minecraft:flash{color:[0.9,0.9,1.0,1.0]} ~ ~1 ~ 0 0 0 0 1',
                            'playsound minecraft:entity.lightning_bolt.thunder neutral @a[distance=..32] ~ ~ ~ 0.6 1.6',
                            'playsound minecraft:entity.lightning_bolt.impact neutral @a[distance=..24] ~ ~ ~ 0.8 1.2',
                            f'execute as @e[{foe},distance=..5.5] at @s run function bm:p145/thundered', 'tag @s remove bm.fyme',
                            'execute on owner if entity @s[distance=..24] run ' + fysay('Behold - the Thunder Exhibit!')])
    fn('p145/thundered', ['function bm:p145/hurt', 'particle minecraft:electric_spark ~ ~1 ~ 0.3 0.6 0.3 0.2 12'])
    # the Golden Bowl: the GRAND EXHIBITION - spectral replicas of the cabinet's pieces wheel round him, then burst on every foe near
    fn('p145/ult_spin', [f'particle minecraft:end_rod ^{2.2 * math.cos(a):.2f} ^{1.0 + 0.4 * math.sin(3 * a):.2f} ^{2.2 * math.sin(a):.2f} 0 0 0 0 1'
                         for a in [k * math.pi / 6 for k in range(12)]] +
       ['particle minecraft:wax_on ~ ~1 ~ 2 0.6 2 0 6', 'execute if score @s bm.fyx matches 29 run function bm:p145/ult_replicas'])
    REPLICAS = ['bm:apo_true_crown', 'bm:demo_scythe', 'bm:tul_harpoon', 'bm:horseman_head', 'bm:ray_gun', 'bm:pearl_statue']
    for j, m in enumerate(REPLICAS):
        a = j * 2 * math.pi / len(REPLICAS)
        fn(f'p145/ult_r{j}', [f'summon minecraft:item_display ^{1.8 * math.cos(a):.2f} ^1.2 ^{1.8 * math.sin(a):.2f} ' +
                              snbt({'Tags': ['bm.fyrep'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': ITEMS[m[3:]]['comps'].get('minecraft:item_model', m) if m[3:] in ITEMS else m}},
                                    'item_display': 'fixed', 'billboard': 'vertical', 'Glowing': B(1), 'glow_color_override': Int(0xffcf40), 'brightness': {'block': Int(15), 'sky': Int(15)},
                                    'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0)] * 3, 'scale': [F(0.6)] * 3}})])
    fn('p145/ult_replicas', [f'function bm:p145/ult_r{j}' for j in range(len(REPLICAS))] + ['scoreboard players set @e[type=minecraft:item_display,tag=bm.fyrep,distance=..4] bm.fyl 12'])
    tick += ['scoreboard players remove @e[type=minecraft:item_display,tag=bm.fyrep] bm.fyl 1', 'kill @e[type=minecraft:item_display,tag=bm.fyrep,scores={bm.fyl=..0}]']
    fn('p145/ult_hit', ['tag @s add bm.fyme', 'scoreboard players set #pd bm.rng 14', 'scoreboard players operation #pd bm.rng += #done bm.cab',
                        'execute at @e[type=minecraft:item_display,tag=bm.fyrep,distance=..4] run particle minecraft:flash{color:[1.0,0.85,0.3,1.0]} ~ ~ ~ 0 0 0 0 1',
                        'particle minecraft:totem_of_undying ~ ~1.2 ~ 2.5 0.8 2.5 0.4 120',
                        'playsound minecraft:entity.generic.explode neutral @a[distance=..32] ~ ~ ~ 0.8 1.4',
                        'playsound minecraft:ui.toast.challenge_complete neutral @a[distance=..24] ~ ~ ~ 0.6 1.6',
                        f'execute as @e[{foe},distance=..7] at @s run function bm:p145/exhibited', 'tag @s remove bm.fyme',
                        'execute on owner if entity @s[distance=..24] run ' + fysay('The GRAND EXHIBITION! Admission: free. Survival: not included.')])
    fn('p145/exhibited', ['function bm:p145/hurt', 'effect give @s minecraft:levitation 1 3', 'particle minecraft:wax_on ~ ~1 ~ 0.3 0.5 0.3 0 8'])
    QUIPS = ['Ha! Take that, you ruffian!', 'Not the monocle - never the monocle!', 'A curator defends his collection!', 'Oh! I did that? Splendid!',
             'Mind the glass, mind the glass!', 'For science! And for the Cabinet!', 'Bubbles and bravery, my friend.']
    fn('p145/quip', ['scoreboard players set @s bm.fyq 0', f'execute store result score #r bm.rng run random value 1..{len(QUIPS)}'] +
       [f'execute if score #r bm.rng matches {n + 1} on owner if entity @s[distance=..20,tag=!bm.hush] run ' + fysay(q) for n, q in enumerate(QUIPS)] + face('happy', 30))
    # (a new exhibit shown near him: the monocle pops)
    fn('p145/pet_shock', face('surprised', 24) + ['scoreboard players set @s bm.fysl 16'])
    # ---- the Court: you and your followers near him mend and stand firm; the Deep: in water, you breathe
    second.append('execute as @e[type=minecraft:wolf,tag=bm.fypet,tag=!bm.ffpet] at @s run function bm:p145/sec')
    fn('p145/sec', ['scoreboard players operation #me bm.pid = @s bm.pid',
                    'execute if score #f_court bm.cab matches 1 run function bm:p145/court',
                    'execute if score #f_deep bm.cab matches 1 on owner if entity @s[distance=..14] at @s if block ~ ~1 ~ minecraft:water run effect give @s minecraft:water_breathing 12 0 true',
                    'execute if score #f_deep bm.cab matches 1 if predicate bm:swim run effect give @s minecraft:dolphins_grace 3 0 true'])
    fn('p145/court', ['execute as @a[distance=..8,gamemode=!spectator] if score @s bm.pid = #me bm.pid run function bm:p145/court_you',
                      'execute as @e[type=#bm:p145_hosts,distance=..8] if score @s bm.pid = #me bm.pid run effect give @s minecraft:regeneration 4 0 true'])
    fn('p145/court_you', ['effect give @s minecraft:regeneration 4 0 true', 'effect give @s minecraft:resistance 4 0 true'])
    wjson('bm/tags/entity_type/p145_hosts.json', {'values': ['minecraft:wolf', 'minecraft:cat']})

    # ---- his Pocket Bowl: call, call over, sneak for his menu
    def pet_nbt():
        return {'Tags': ['bm.fypet', 'bm.fynew', 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1), 'Health': F(PET_HP0),
                'CustomName': T('Fishy', ORANGE, bold=True), 'CustomNameVisible': B(0),
                'attributes': [{'id': f'minecraft:{k}', 'base': D(v)} for k, v in dict(max_health=PET_HP0, armor=4, attack_damage=1, knockback_resistance=0.3,
                                                                                       movement_speed=0.33, follow_range=32, step_height=1.0, water_movement_efficiency=0.6,
                                                                                       oxygen_bonus=1000).items()],
                'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}]}
    in_heist = 'execute if entity @s[tag=bm.gvp] if dimension bm:gutter'
    fn('p145/use', [f'{in_heist} run return run ' + say("In the vault your crew answers the Fixer's Ledger - Raid Crew.", '#9ad0ff'),
                    'execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                    'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                    f'{sel_pet} run tag @s add bm.fysel2',
                    'scoreboard players set #am bm.rng 0',
                    'execute if predicate bm:p20/sneaking run scoreboard players set #am bm.rng 2',
                    'execute if score #am bm.rng matches 0 if entity @e[type=minecraft:wolf,tag=bm.fysel2] run scoreboard players set #am bm.rng 4',
                    'execute if score #am bm.rng matches 2 run function bm:p145/menu', 'execute if score #am bm.rng matches 4 run function bm:p145/recall',
                    'execute if score #am bm.rng matches 0 run function bm:p145/try_summon',
                    'tag @e[tag=bm.fysel2] remove bm.fysel2'])
    fn('p145/recall', ['tp @e[type=minecraft:wolf,tag=bm.fysel2,limit=1] @s', 'data modify entity @e[type=minecraft:wolf,tag=bm.fysel2,limit=1] Sitting set value 0b',
                       'particle minecraft:splash ~ ~1 ~ 0.4 0.8 0.4 0.1 30', 'playsound minecraft:entity.tropical_fish.flop neutral @a[distance=..16] ~ ~ ~ 0.6 1.3',
                       fysay('Coming, coming! These legs were made for strolling, not sprinting.')])
    fn('p145/try_summon', ['execute if score @s bm.fycd matches 1.. store result score #m bm.rng run scoreboard players get @s bm.fycd',
                           'execute if score @s bm.fycd matches 1.. run scoreboard players add #m bm.rng 59', 'execute if score @s bm.fycd matches 1.. run scoreboard players operation #m bm.rng /= #60 bm.rng',
                           'execute if score @s bm.fycd matches 1.. run return run ' + title('@s', 'actionbar', [T('Fishy is still catching his breath: about ', 'gray'),
                                                                                                              {'score': {'name': '#m', 'objective': 'bm.rng'}, 'color': 'white'}, T(' min.', 'gray')]),
                           'execute unless function bm:p145/ok run return run ' + say("Fishy won't come here."),
                           'execute if function bm:p58/full run return 0',
                           'function bm:p145/summon'])
    fn('p145/summon', ['execute positioned ^ ^ ^1.2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:p145/summon_here',
                       'execute positioned ^ ^1 ^1.2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:p145/summon_here',
                       'function bm:p145/summon_here'])
    fn('p145/summon_here', [f'summon minecraft:wolf ~ ~ ~ {snbt(pet_nbt())}',
                            'data modify entity @e[type=minecraft:wolf,tag=bm.fynew,limit=1,sort=nearest] Owner set from entity @s UUID',
                            'execute as @e[type=minecraft:wolf,tag=bm.fynew,limit=1,sort=nearest] run function bm:p145/toughen',
                            'scoreboard players set @e[type=minecraft:wolf,tag=bm.fynew,limit=1,sort=nearest] bm.fys -1',
                            'scoreboard players set @e[type=minecraft:wolf,tag=bm.fynew,limit=1,sort=nearest] bm.fysl 24',
                            'execute rotated ~180 0 run function bm:p145/rig_here',
                            'scoreboard players operation @e[tag=bm.fynew,distance=..4] bm.pid = @s bm.pid',
                            'execute as @e[type=minecraft:item_display,tag=bm.fynew,distance=..4] run tag @s add bm.fysel', 'function bm:p145/dress',
                            'execute at @e[type=minecraft:item_display,tag=bm.fysel,tag=bm.fyp_body,limit=1] run function bm:p145/burst',
                            'tag @e[tag=bm.fysel] remove bm.fysel', 'tag @e[tag=bm.fynew,distance=..4] remove bm.fynew',
                            'playsound minecraft:entity.player.splash neutral @a[distance=..20] ~ ~ ~ 0.8 1.4', 'playsound minecraft:block.note_block.chime neutral @a[distance=..20] ~ ~ ~ 0.6 1.6',
                            fysay('Fishy, curator, at your service! Do point out anything curious.')])
    # (his health: 30, +10 a wing finished, +40 the Golden Bowl; his armour 4, +1 a wing)
    fn('p145/toughen', ['scoreboard players set #hp bm.rng 10', 'scoreboard players operation #hp bm.rng *= #done bm.cab', f'scoreboard players add #hp bm.rng {PET_HP0}',
                        'execute if score #cap bm.cab matches 1 run scoreboard players add #hp bm.rng 40',
                        'scoreboard players operation #ar bm.rng = #done bm.cab', 'scoreboard players add #ar bm.rng 4',
                        'execute store result storage bm:tmp fy.h int 1 run scoreboard players get #hp bm.rng', 'execute store result storage bm:tmp fy.a int 1 run scoreboard players get #ar bm.rng',
                        'function bm:p145/toughen2 with storage bm:tmp fy'])
    fn('p145/toughen2', ['$attribute @s minecraft:max_health base set $(h)', '$data modify entity @s Health set value $(h)f', '$attribute @s minecraft:armor base set $(a)'])
    fn('p145/rig_here', rig + ['tp @e[type=minecraft:item_display,tag=bm.fynew,distance=..1] ~ ~ ~ ~ 0'])
    fn('p145/rerig', ['kill @e[type=minecraft:item_display,tag=bm.fysel]', 'execute rotated as @s rotated ~ 0 run function bm:p145/rig_here',
                      'scoreboard players operation @e[type=minecraft:item_display,tag=bm.fynew,distance=..2] bm.pid = #me bm.pid',
                      'tag @e[type=minecraft:item_display,tag=bm.fynew,distance=..2] add bm.fysel', 'tag @e[type=minecraft:item_display,tag=bm.fynew,distance=..2] remove bm.fynew',
                      'function bm:p145/dress', 'scoreboard players set @s bm.fys -1'])
    # (his look: the Golden Bowl's gilding on his limbs and bowl, then the hat his owner picked - the "_c<k>" suffix, phase138)
    fn('p145/dress', ['scoreboard players set #wk bm.rng 0', 'execute as @a if score @s bm.pid = #me bm.pid run scoreboard players operation #wk bm.rng = @s bm.cosfy'] +
       [l for p in GILT for l in (f'execute unless score #cap bm.cab matches 1 as {psel(p)} run data modify entity @s item.components."minecraft:item_model" set value "bm:fy_{p}"',
                                  f'execute if score #cap bm.cab matches 1 as {psel(p)} run data modify entity @s item.components."minecraft:item_model" set value "bm:fy_{p}_g"')] +
       ['execute as @e[type=minecraft:item_display,tag=bm.fysel] run function bm:p138/sfx'])
    fn('p145/redress_any', ['scoreboard players operation #me bm.pid = @s bm.pid',
                            'execute as @e[type=minecraft:item_display,tag=bm.fyp_pet,tag=!bm.fyfade] if score @s bm.pid = #me bm.pid run tag @s add bm.fysel',
                            'function bm:p145/dress', 'function bm:p145/toughen', 'execute at @s run particle minecraft:wax_on ~ ~1 ~ 0.4 0.6 0.4 0 30',
                            'tag @e[tag=bm.fysel] remove bm.fysel'])
    fn('p99/fishy_now', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #has bm.rng 0',
                         'execute as @e[type=minecraft:wolf,tag=bm.fypet] if score @s bm.pid = #me bm.pid at @s run function bm:p145/now2',
                         'execute if score #has bm.rng matches 0 run return run ' + say('Fishy isn\'t with you - he\'ll wear it next time.', ORANGE)])
    fn('p145/now2', ['scoreboard players set #has bm.rng 1', 'function bm:p145/redress_any', 'particle minecraft:end_rod ~ ~1 ~ 0.4 0.6 0.4 0.02 14'])
    fn('p145/dismiss', ['execute as @e[type=minecraft:wolf,tag=bm.fysel2] at @s run function bm:p145/fade',
                        'execute as @e[type=minecraft:wolf,tag=bm.fysel2] on passengers run kill @s[type=!minecraft:player]',
                        'execute as @e[type=minecraft:wolf,tag=bm.fysel2] run data remove entity @s Owner',
                        'execute as @e[type=minecraft:wolf,tag=bm.fysel2] run tp @s ~ -500 ~', 'kill @e[type=minecraft:wolf,tag=bm.fysel2]',
                        fysay('Back to the Cabinet, then. Do bring me something marvellous!')])
    fn('p145/home', ['execute as @e[type=minecraft:wolf,tag=bm.fypet] if score @s bm.pid = #me bm.pid run tag @s add bm.fysel2',
                     'execute if entity @e[tag=bm.fysel2] run function bm:p145/dismiss', 'tag @e[tag=bm.fysel2] remove bm.fysel2'])
    # his menu (sneak + use the bowl)
    dlg = lambda out: P28.multi([T("Fishy's Pocket Bowl", ORANGE, bold=True)],
                                [P28.body([T('Fishy', ORANGE, bold=True), T(' - gentleman, goldfish, curator. ', 'gray'),
                                           T('Show him the rare things you find (right-click him holding one): a replica for his Cabinet; you keep yours.', 'white')]),
                                 P28.body([T('Every wing of the Cabinet finished teaches him a power - see ', 'gray'), T("Fishy's powers", ORANGE, bold=True), T('.', 'gray')], 300)],
                                ([P28.btn(T('Sit / follow', 'white', bold=True), MENU + 1, width=150), P28.btn(T('Send him home', 'gray'), MENU + 9, width=150)] if out else
                                 [P28.btn(T('Call for Fishy', ORANGE, bold=True), MENU + 8, width=150)]) +
                                [P28.btn(T('The Cabinet', GOLD, bold=True), MENU + 3, width=150, tooltip=T('Every wing, every exhibit - shown or veiled.', 'gray')),
                                 P28.btn(T("Fishy's powers", ORANGE, bold=True), MENU + 4, width=150, tooltip=T('What the Cabinet has taught him.', 'gray')),
                                 P28.btn(T('Wardrobe', ORANGE, bold=True), MENU + 2, width=150, tooltip=T('His top hats - and his aura, if you have it.', 'gray'))],
                                columns=2, exit_label='Close')
    fn('p145/menu', [f'scoreboard players set @s bm.menu {MENU}', 'scoreboard players set #out bm.rng 0',
                     'execute if entity @e[type=minecraft:wolf,tag=bm.fysel2] run scoreboard players set #out bm.rng 1',
                     f'execute if score #out bm.rng matches 1 run return run dialog show @s {snbt(dlg(True))}', f'dialog show @s {snbt(dlg(False))}'])
    G.FUNCS['p28/act'] += [f'execute if score #act bm.pay matches {MENU + n} run return run function bm:p145/act' for n in (1, 2, 3, 4, 8, 9)]
    fn('p145/act', [f'execute unless score @s bm.menu matches {MENU} run return run function bm:p28/stale',
                    f'execute if score #act bm.pay matches {MENU + 2} run return run function bm:p119/plain/fishy',
                    f'execute if score #act bm.pay matches {MENU + 3} run return run function bm:p145/cab/main',
                    f'execute if score #act bm.pay matches {MENU + 4} run return run function bm:p145/cab/powers',
                    'scoreboard players operation #me bm.pid = @s bm.pid', f'{sel_pet} run tag @s add bm.fysel2',
                    f'execute if score #act bm.pay matches {MENU + 8} unless entity @e[type=minecraft:wolf,tag=bm.fysel2] run function bm:p145/try_summon',
                    f'execute if score #act bm.pay matches {MENU + 8} if entity @e[type=minecraft:wolf,tag=bm.fysel2] run function bm:p145/recall',
                    f'execute if score #act bm.pay matches {MENU + 1} if entity @e[type=minecraft:wolf,tag=bm.fysel2] run function bm:p145/sit',
                    f'execute if score #act bm.pay matches {MENU + 9} if entity @e[type=minecraft:wolf,tag=bm.fysel2] run function bm:p145/dismiss',
                    'tag @e[tag=bm.fysel2] remove bm.fysel2'])
    tw = '@e[type=minecraft:wolf,tag=bm.fysel2,limit=1]'
    fn('p145/sit', [f'execute store success score #s0 bm.rng if data entity {tw} {{Sitting:1b}}',
                    f'execute if score #s0 bm.rng matches 1 run data modify entity {tw} Sitting set value 0b',
                    f'execute if score #s0 bm.rng matches 0 run data modify entity {tw} Sitting set value 1b',
                    'execute if score #s0 bm.rng matches 1 run ' + fysay('Onward! Adventure awaits - and possibly exhibits.'),
                    'execute if score #s0 bm.rng matches 0 run ' + fysay('I shall rest my legs here. Do not be long.')])
    # ---- his click box (riding him): right-click him to sit / stand - or, holding one of the rare things, show it to him (anyone's Fishy)
    fn('p145/box', ['execute if entity @s[tag=bm.ffpet] run return 0', 'execute if function bm:p145/has_hit run return 0',
                    'summon minecraft:interaction ~ ~ ~ {Tags:["bm.fyhit","bm.fyhnew"],width:1.0f,height:1.9f,response:1b}',
                    'ride @e[type=minecraft:interaction,tag=bm.fyhnew,limit=1,sort=nearest] mount @s', 'tag @e[tag=bm.fyhnew] remove bm.fyhnew'])
    fn('p145/has_hit', ['execute on passengers if entity @s[type=minecraft:interaction,tag=bm.fyhit] run return 1', 'return 0'])
    second.append('execute as @e[type=minecraft:interaction,tag=bm.fyhit] unless function bm:p20/frog/has_vehicle run kill @s')
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.fyhit] if data entity @s interaction run function bm:p145/click',
             'execute as @e[type=minecraft:interaction,tag=bm.fyhit] if data entity @s attack run data remove entity @s attack']
    fn('p145/click', ['execute on vehicle run tag @s add bm.fyclk', 'execute on target at @s run function bm:p145/who', 'tag @e[tag=bm.fyclk] remove bm.fyclk',
                      'data remove entity @s interaction'])
    cw = '@e[type=minecraft:wolf,tag=bm.fyclk,limit=1]'
    fn('p145/who', ['execute if score @s bm.fycl matches 1.. run return 0', 'scoreboard players set @s bm.fycl 10', 'scoreboard players operation #me bm.pid = @s bm.pid',
                    'execute if function bm:p145/show run return 1',
                    f'execute unless score {cw} bm.pid = #me bm.pid run return run ' + fysay('Delighted to meet you! But I am out with someone else today.'),
                    f'execute store success score #s0 bm.rng if data entity {cw} {{Sitting:1b}}',
                    f'execute if score #s0 bm.rng matches 1 run data modify entity {cw} Sitting set value 0b',
                    f'execute if score #s0 bm.rng matches 0 run data modify entity {cw} Sitting set value 1b',
                    'execute if score #s0 bm.rng matches 1 run ' + fysay('Onward! Adventure awaits - and possibly exhibits.'),
                    'execute if score #s0 bm.rng matches 0 run ' + fysay('I shall rest my legs here. Do not be long.')])
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[type=minecraft:interaction,tag=bm.fyhit]')
    # ---- fainting
    tick += ['execute as @e[type=minecraft:item_display,tag=bm.fyp_pet,tag=bm.fyp_body,tag=!bm.fyfade] at @s run function bm:p145/check',
             'scoreboard players remove @e[type=minecraft:item_display,tag=bm.fyfade] bm.fyl 1',
             'kill @e[type=minecraft:item_display,tag=bm.fyfade,scores={bm.fyl=..0}]']
    fn('p145/check', ['scoreboard players operation #me bm.pid = @s bm.pid',
                      f'{sel_pet.replace("tag=bm.fypet]", "tag=bm.fypet,distance=..16]")} run return run scoreboard players set @s bm.fyz 0',
                      'scoreboard players add @s bm.fyz 1', 'execute if score @s bm.fyz matches 4.. run function bm:p145/fell'])
    fn('p145/fell', ['function bm:p145/fade', 'execute as @a if score @s bm.pid = #me bm.pid run function bm:p145/cooldown'])
    fn('p145/cooldown', [f'scoreboard players set @s bm.fycd {PET_CD}',
                         tellraw('@s', PREFIX + [T('Fishy faints! ', ORANGE, bold=True), T('"Oh dear... the water\'s gone all wobbly..." ', LINE_C),
                                                 T(f'The Pocket Bowl needs {PET_CD // 60} minutes before he can come back.', 'gray')])])
    fn('p145/fade', ['execute as @e[type=minecraft:item_display,tag=bm.fyp_pet,tag=!bm.fyfade] if score @s bm.pid = #me bm.pid run function bm:p145/fade1',
                     'particle minecraft:splash ~ ~1 ~ 0.5 1 0.5 0.2 60', 'particle minecraft:bubble_pop ~ ~1 ~ 0.5 0.8 0.5 0.05 40',
                     'particle minecraft:flash{color:[1.0,0.7,0.3,1.0]} ~ ~1 ~ 0 0 0 0 1',
                     'playsound minecraft:entity.player.splash neutral @a[distance=..20] ~ ~ ~ 0.8 1.2', 'playsound minecraft:block.glass.break neutral @a[distance=..20] ~ ~ ~ 0.4 1.6'])
    fn('p145/fade1', ['tag @s add bm.fyfade', 'scoreboard players set @s bm.fyl 3',
                      'data merge entity @s[type=minecraft:item_display] {brightness:{block:15,sky:15},Glowing:1b,glow_color_override:16752704}'])
    second.append('scoreboard players remove @a[scores={bm.fycd=1..}] bm.fycd 1')
    G.FUNCS['p62/died'].insert(-1, 'execute as @e[type=minecraft:wolf,tag=bm.fypet] if score @s bm.pid = #me bm.pid at @s run function bm:p145/go')
    fn('p145/go', ['scoreboard players add #gone bm.rng 1', 'function bm:p145/fade', 'execute on passengers run kill @s[type=!minecraft:player]',
                   'data remove entity @s Owner', 'tp @s ~ -500 ~', 'kill @s'])
    P73.follow_rules(G, ('fishy', 'wolf', 'bm.fypet', 'fy_bowl', 'p145/go', 'Fishy', 'bm.fyfg', 'p145/summon_here'), second)
    L = G.FUNCS['p73/fol/fishy']
    j = next(i for i, l in enumerate(L) if ' if items entity ' in l)
    L.insert(j, 'execute if entity @a[tag=bm.fown,tag=bm.gvp] run return run scoreboard players set @s bm.fmis 0')
    G.FUNCS['p58/count'][-1:-1] = ['execute as @e[type=minecraft:wolf,tag=bm.fypet] on owner if entity @s[tag=bm.fcme] run scoreboard players add #fc bm.rng 1']
    G.FUNCS['p57/pulse'] += [l.replace('tag=bm.celipet', 'tag=bm.fypet') for l in G.FUNCS['p57/pulse'] if 'tag=bm.celipet' in l]
    # (going into a heist without him: he waits outside the vault, and is back with you when you're home - as the others, phase136)
    far = G.FUNCS['p73/fol/fishy_far']
    assert far[0] == 'function bm:p145/go', far[0]
    far.insert(0, 'execute if entity @a[tag=bm.fown,tag=bm.gvp] run return run function bm:p103/fol/wait_fishy')
    fn('p103/fol/wait_fishy', ['tag @a[tag=bm.fown] add bm.ow_fishy', 'function bm:p145/go',
                               tellraw('@a[tag=bm.fown]', PREFIX + [T('Fishy waits outside the vault', ORANGE), T(' - your Raid Crew answers inside. ', 'gray'),
                                                                    T('(Back with you when you\'re home.)', 'dark_gray')]), 'tag @a remove bm.fown'])
    fn('p103/fol/back_fishy', ['tag @s remove bm.ow_fishy', 'function bm:p145/try_summon'])
    G.FUNCS['p103/fol/tick'].append('execute if entity @s[tag=bm.ow_fishy] run function bm:p103/fol/back_fishy')

    # ---- his rosettes: sneak + use on a block (the placeables' way, phase71); sneak + punch to take back
    for w in WINGS + ['grand']:
        iid = f'cab_rosette_{w}'
        fn(f'p145/ros/place_{w}', ['execute unless predicate bm:p20/sneaking run return run ' + say('Sneak + use on a block to set it up.'),
                                   'scoreboard players set #placed bm.rng 0', 'scoreboard players set #ray bm.rng 25', 'tag @s add bm.placer',
                                   f'execute anchored eyes positioned ^ ^ ^ run function bm:p145/ros/ray_{w}', 'tag @s remove bm.placer',
                                   'execute if score #placed bm.rng matches 0 run return run ' + say('Look at the top of a block within 5 blocks.'),
                                   f'execute unless entity @s[gamemode=creative] run clear @s {holds(iid)} 1'])
        fn(f'p145/ros/ray_{w}', [f'execute unless block ~ ~ ~ #minecraft:replaceable run return run function bm:p145/ros/hit_{w}',
                                 'scoreboard players remove #ray bm.rng 1', f'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p145/ros/ray_{w}'])
        fn(f'p145/ros/hit_{w}', ['execute align xyz positioned ~0.5 ~1 ~0.5 unless block ~ ~ ~ #minecraft:replaceable run return 0',
                                 'execute align xyz positioned ~0.5 ~1 ~0.5 if entity @e[type=minecraft:interaction,tag=bm.gvdeco,distance=..0.6] run return 0',
                                 f'execute align xyz positioned ~0.5 ~1 ~0.5 rotated as @a[tag=bm.placer,limit=1] rotated ~180 0 run function bm:p145/ros/spawn_{w}',
                                 'scoreboard players set #placed bm.rng 1'])
        rd = {'Tags': ['bm.gvdecod', 'bm.gvdnew', 'bm.cabros'], 'item': G.stack(iid), 'item_display': 'fixed', 'brightness': {'block': Int(15), 'sky': Int(15)},
              'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.55), F(0)], 'scale': [F(0.95)] * 3}}
        fn(f'p145/ros/spawn_{w}', [f'summon minecraft:item_display ~ ~ ~ {snbt(rd)}',
                                   f'summon minecraft:interaction ~ ~ ~ {snbt({"Tags": ["bm.gvdeco", "bm.gvdnew", "bm.gvdk_" + iid], "width": F(0.8), "height": F(1.0), "response": B(1)})}',
                                   'tp @e[tag=bm.gvdnew,distance=..0.5] ~ ~ ~ ~ 0', 'tag @e[tag=bm.gvdnew,distance=..0.5] remove bm.gvdnew',
                                   'playsound minecraft:block.glass.place block @a[distance=..16] ~ ~ ~ 1 1', 'particle minecraft:wax_on ~ ~0.6 ~ 0.3 0.4 0.3 0 12'])
        G.FUNCS['p71/deco/pick'][0:0] = [f'execute if entity @e[type=minecraft:interaction,tag=bm.gvdme,tag=bm.gvdk_{iid}] run loot give @s loot bm:items/{iid}']
    second.append('execute as @e[type=minecraft:item_display,tag=bm.cabros] at @s if predicate bm:p141/now_and_then run particle minecraft:end_rod ~ ~0.6 ~ 0.25 0.3 0.25 0 1')

    # ================================================================== admin
    fn('admin/fishy', [give('fy_bowl'), 'tag @s add bm.fymet', say('Fishy\'s Pocket Bowl. (He\'s at his desk in the Cabinet, off the Fixer\'s Lounge.)', ORANGE)])
    fn('admin/cabinet', ['function bm:p145/cab/main'])
    for w in WINGS:
        fn(f'admin/cabinet_fill_{w}', ['function bm:p28/name/of'] + [f'execute unless data storage bm:cab got.{k} run data modify storage bm:cab got.{k}.by set from storage bm:tmp nm.name'
                                                                      for k, ids, r in CAB.EXHIBITS[w]] +
           ['function bm:p145/recount'] + bitf('bm.cabc', WI[w] - 1) +
           [f'execute if score #q bm.rng matches 0 run scoreboard players add @s bm.cabc {2 ** (WI[w] - 1)}',
            f'execute unless score #f_{w} bm.cab matches 1 run function bm:p145/wing_done/{w}', f'function bm:p145/hall/show/{w}'])
    fn('admin/cabinet_fill', [f'function bm:admin/cabinet_fill_{w}' for w in WINGS])
    fn('admin/cabinet_reset', ['data remove storage bm:cab got', 'function bm:p145/recount', 'function bm:p145/flags', 'scoreboard players reset * bm.cabc',
                               'scoreboard players reset * bm.cabr', 'function bm:p145/hall/now', say('Fishy\'s Cabinet is empty again (and every claim forgotten).', ORANGE)])
    fn('admin/cabinet_hall', ['data remove storage bm:cab built', 'execute in bm:gutter run function bm:p145/hall/build'])
    G.FUNCS['admin/help'] += [tellraw('@s', [T('/function bm:admin/fishy', 'yellow'), T("  Fishy's Pocket Bowl (meet him in the Cabinet off the Fixer's Lounge)", 'gray')]),
                              tellraw('@s', [T('/function bm:admin/cabinet_fill[_<wing>]', 'yellow'), T('  fill the Cabinet (or one wing) in your name; admin/cabinet_reset empties it', 'gray')])]
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.fyp]', 'kill @e[tag=bm.cabprop]', 'kill @e[type=minecraft:item_display,tag=bm.fyrep]']
    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    f[-1:-1] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second
